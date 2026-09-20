"""
prepare.py - Groundwater Abstraction Return Reconciliation

Deterministic split of the raw corpus into public/ and private/. It splits,
copies series files, assigns fresh sequential ids and writes the sample
submission. It runs no simulation.

  1. Read raw scenes.csv (one row per monitored area and return period).
  2. Split on the scene's background pool tag, so no real USGS monitoring well
     contributes background to both a train and a test scene.
  3. Deterministically shuffle within each split before assigning ids, so
     neither the ids nor the row order carry generation order.
  4. Write public train/test CSVs, a sample submission, and private answers.
     The declared returns, the private score group and the signal-strength
     band live in private/answers.csv; the score group drives the grader's
     group-mean chain.

`prepare(raw, public, private)` is the platform-standard signature.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import exp1

SPLIT_SALT = "gw-abstraction-reconciliation-v1"
SHUFFLE_TRAIN = 481207
SHUFFLE_TEST = 913553
N_GROUPS = 8

NT = 224
STEP_H = 3.0
NDAYS = 28.0
KB = 7
BLOCK_D = NDAYS / KB
RMIN = 30.0
LOGT_LO, LOGT_HI = 1.477, 2.903
LOGS_LO, LOGS_HI = -3.301, -1.523

T_DAYS = np.arange(NT) * (STEP_H / 24.0)

MIN_TRAIN, MIN_TEST = 1200, 350
MIN_TRAIN_FAMILIES, MIN_TEST_FAMILIES = 200, 100

PROMPT = (
    "One monitored groundwater area over a single 28-day abstraction return "
    "period. You are given: the plan coordinates of every registered borehole "
    "in the area and the abstraction return each operator DECLARED for that "
    "period, as seven consecutive four-day blocks in cubic metres per day; the "
    "plan coordinates of the observation wells; and each observation well's "
    "water-level series, 224 samples at three-hour spacing in metres relative "
    "to its own mean. The levels respond to what was ACTUALLY abstracted, not "
    "to what was declared, and they also carry the real background fluctuation "
    "a monitoring well records. Report, for every borehole in the order given, "
    "the actual abstraction ledger over the same seven blocks, together with "
    "log10 transmissivity in square metres per day and log10 storage "
    "coefficient for the aquifer. Some declarations are accurate and some are "
    "not; recover what the observed drawdown supports."
)


def _split_of(bg_pool: str) -> str:
    return "train" if str(bg_pool).strip().upper() == "A" else "test"


def _group_of(scene_id: str) -> int:
    h = hashlib.sha256(("%s:%s" % (SPLIT_SALT, scene_id)).encode("utf-8")).hexdigest()
    return int(h[:8], 16) % N_GROUPS


def _rho_band(rho: float) -> str:
    if rho < 6.0:
        return "weak"
    if rho < 13.0:
        return "moderate"
    return "clear"


def _theis_unit_many(R, T, S):
    """[n_r, KB, NT] unit-rate response for many radii at once."""
    R = np.maximum(np.asarray(R, float), RMIN)
    step = np.zeros((len(R), KB + 1, NT))
    for k in range(KB + 1):
        dt = T_DAYS - k * BLOCK_D
        m = dt > 1e-9
        if not m.any():
            continue
        u = (R[:, None] ** 2 * S) / (4.0 * T * dt[None, m])
        step[:, k, m] = exp1(u) / (4.0 * np.pi * T)
    return step[:, :KB, :] - step[:, 1:, :]


def _reference_fit(series, obs, bhs, n_t=10, n_s=8, dec=4):
    """Cheap reference estimate of the aquifer parameters: assume the declared
    returns are correct and pick the (T, S) pair whose predicted drawdown best
    matches the observations. This is the weak baseline shipped as the sample
    submission; it never sees the private answers."""
    O = np.array([[o["x"], o["y"]] for o in obs], float)
    B = np.array([[b["x"], b["y"]] for b in bhs], float)
    D = np.array([b["declared"] for b in bhs], float)
    R = np.maximum(np.hypot(O[:, None, 0] - B[None, :, 0],
                            O[:, None, 1] - B[None, :, 1]), RMIN)
    y = series[:, ::dec]
    y = y - y.mean(axis=1, keepdims=True)
    best = (np.inf, 0.5 * (LOGT_LO + LOGT_HI), 0.5 * (LOGS_LO + LOGS_HI))
    for lt in np.linspace(LOGT_LO, LOGT_HI, n_t):
        for ls in np.linspace(LOGS_LO, LOGS_HI, n_s):
            U = _theis_unit_many(R.ravel(), 10.0 ** lt, 10.0 ** ls)
            U = U.reshape(R.shape[0], R.shape[1], KB, NT)
            pred = -np.einsum("objt,bj->ot", U, D)
            pred = pred[:, ::dec]
            pred = pred - pred.mean(axis=1, keepdims=True)
            sse = float(((y - pred) ** 2).sum())
            if sse < best[0]:
                best = (sse, lt, ls)
    return float(best[1]), float(best[2])


def prepare(raw, public, private) -> None:
    raw, public, private = Path(raw), Path(public), Path(private)
    if not (raw / "scenes.csv").exists() and (raw / "raw_upload" / "scenes.csv").exists():
        raw = raw / "raw_upload"          # platform-rebuilt layout
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    scenes = pd.read_csv(raw / "scenes.csv", dtype={"scene_id": str, "bg_pool": str})
    scenes = scenes.sort_values("scene_id").reset_index(drop=True)
    scenes["split"] = scenes["bg_pool"].map(_split_of)

    train = scenes[scenes["split"] == "train"].sample(frac=1.0, random_state=SHUFFLE_TRAIN).reset_index(drop=True)
    test = scenes[scenes["split"] == "test"].sample(frac=1.0, random_state=SHUFFLE_TEST).reset_index(drop=True)
    if len(train) < MIN_TRAIN or len(test) < MIN_TEST:
        raise SystemExit("split too small: %d train / %d test (need %d / %d)"
                         % (len(train), len(test), MIN_TRAIN, MIN_TEST))

    for sub in ("train", "test"):
        (public / sub / "series").mkdir(parents=True, exist_ok=True)

    train_rows, test_rows, sample_rows, answer_rows = [], [], [], []

    def emit(df, split, offset):
        for k, r in df.iterrows():
            rid = offset + k
            name = "%06d.csv" % rid
            shutil.copyfile(raw / r["series_file"], public / split / "series" / name)
            common = {"id": rid, "series": "series/%s" % name,
                      "n_boreholes": int(r["n_boreholes"]), "n_obs": int(r["n_obs"]),
                      "boreholes": r["boreholes_json"], "obs": r["obs_json"],
                      "prompt": PROMPT}
            if split == "train":
                train_rows.append(common | {"actual": r["actual_json"],
                                            "log_t": float(r["log_t"]),
                                            "log_s": float(r["log_s"])})
            else:
                test_rows.append(common)
                bhs = json.loads(r["boreholes_json"])
                obs = json.loads(r["obs_json"])
                ser = pd.read_csv(raw / r["series_file"])
                arr = ser[[c for c in ser.columns if c != "obs_id"]].to_numpy(float)
                lt, ls = _reference_fit(arr, obs, bhs)
                sample_rows.append({"id": rid,
                                    "actual": json.dumps([b["declared"] for b in bhs],
                                                         separators=(",", ":")),
                                    "log_t": round(lt, 4), "log_s": round(ls, 4)})
                answer_rows.append({"id": rid,
                                    "actual": r["actual_json"],
                                    "declared": json.dumps([b["declared"] for b in bhs],
                                                           separators=(",", ":")),
                                    "log_t": float(r["log_t"]), "log_s": float(r["log_s"]),
                                    "score_group": _group_of(str(r["scene_id"])),
                                    "signal_band": _rho_band(float(r["rho"])),
                                    "n_boreholes": int(r["n_boreholes"])})
        return offset + len(df)

    off = emit(train, "train", 0)
    emit(test, "test", off)

    pd.DataFrame(train_rows).to_csv(public / "train.csv", index=False)
    pd.DataFrame(test_rows).to_csv(public / "test.csv", index=False)
    pd.DataFrame(sample_rows).to_csv(public / "sample_submission.csv", index=False)
    pd.DataFrame(answer_rows).to_csv(private / "answers.csv", index=False)

    ans = pd.DataFrame(answer_rows)
    if ans["score_group"].nunique() < 4:
        raise SystemExit("too few score groups in the hidden test")
    print("train %d / test %d rows, %d score groups, %d signal bands"
          % (len(train_rows), len(test_rows), ans["score_group"].nunique(),
             ans["signal_band"].nunique()))


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="raw_data")
    ap.add_argument("--public", default="public")
    ap.add_argument("--private", default="private")
    a = ap.parse_args()
    prepare(a.raw, a.public, a.private)

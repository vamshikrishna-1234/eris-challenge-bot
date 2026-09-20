"""_analyze.py - measured gates for Groundwater Abstraction Return Reconciliation.

Runs the null-metric audit, the baseline ladder and the grader red-team through
the SHIPPED grade.py, on the prepared split.

  python _analyze.py --public <dir> --private <dir> [--strong-n 200]
"""
from __future__ import annotations

import argparse, json, time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import exp1
from scipy.optimize import nnls

import grade as G

KB, NT = 7, 224
STEP_H, NDAYS = 3.0, 28.0
BLOCK_D = NDAYS / KB
RMIN = 30.0
LOGT_LO, LOGT_HI = 1.477, 2.903
LOGS_LO, LOGS_HI = -3.301, -1.523
T_DAYS = np.arange(NT) * (STEP_H / 24.0)


def theis_many(R, T, S):
    R = np.maximum(np.asarray(R, float), RMIN)
    step = np.zeros((len(R), KB + 1, NT))
    for k in range(KB + 1):
        dt = T_DAYS - k * BLOCK_D
        m = dt > 1e-9
        if not m.any():
            continue
        step[:, k, m] = exp1((R[:, None] ** 2 * S) / (4.0 * T * dt[None, m])) / (4.0 * np.pi * T)
    return step[:, :KB, :] - step[:, 1:, :]


class Scene:
    def __init__(self, row, root):
        self.id = int(row["id"])
        self.bh = json.loads(row["boreholes"])
        self.obs = json.loads(row["obs"])
        s = pd.read_csv(Path(root) / row["series"])
        self.Y = s[[c for c in s.columns if c != "obs_id"]].to_numpy(float)
        self.O = np.array([[o["x"], o["y"]] for o in self.obs], float)
        self.B = np.array([[b["x"], b["y"]] for b in self.bh], float)
        self.D = np.array([b["declared"] for b in self.bh], float)
        self.R = np.maximum(np.hypot(self.O[:, None, 0] - self.B[None, :, 0],
                                     self.O[:, None, 1] - self.B[None, :, 1]), RMIN)

    def design(self, lt, ls, dec=2):
        U = theis_many(self.R.ravel(), 10.0 ** lt, 10.0 ** ls)
        U = U.reshape(self.R.shape[0], self.R.shape[1], KB, NT)[:, :, :, ::dec]
        U = U - U.mean(axis=3, keepdims=True)
        A = np.transpose(U, (0, 3, 1, 2)).reshape(-1, self.B.shape[0] * KB)
        y = -self.Y[:, ::dec].ravel()
        return A, y - y.mean()

    def sse(self, lt, ls, q, dec=4):
        A, y = self.design(lt, ls, dec)
        r = A @ q - y
        return float(r @ r)


def sub_frame(rows):
    return pd.DataFrame(rows)


def pack(sid, mat, lt, ls):
    return {"id": sid,
            "actual": json.dumps([[float(v) for v in r] for r in mat], separators=(",", ":")),
            "log_t": lt, "log_s": ls}


# ------------------------------------------------------------------ solvers
def s_zero(sc, **kw):
    return pack(sc.id, np.zeros_like(sc.D), None, None)

def s_declared(sc, med=(2.19, -2.41), **kw):
    return pack(sc.id, sc.D, med[0], med[1])

def s_prior(sc, mean_q=None, med=(2.19, -2.41), **kw):
    return pack(sc.id, np.tile(mean_q, (sc.D.shape[0], 1)), med[0], med[1])

def s_random(sc, rng=None, **kw):
    return pack(sc.id, rng.uniform(0, 1200, sc.D.shape),
                float(rng.uniform(LOGT_LO, LOGT_HI)), float(rng.uniform(LOGS_LO, LOGS_HI)))

def s_weak(sc, **kw):
    lt, ls = 0.5 * (LOGT_LO + LOGT_HI), 0.5 * (LOGS_LO + LOGS_HI)
    A, y = sc.design(lt, ls, dec=4)
    q, _ = nnls(A, y)
    return pack(sc.id, q.reshape(-1, KB), lt, ls)

def _anchor_TS(sc, ltg, lsg):
    d = sc.D.ravel()
    best = (np.inf, ltg[0], lsg[0])
    for lt in ltg:
        for ls in lsg:
            v = sc.sse(lt, ls, d, dec=4)
            if v < best[0]: best = (v, lt, ls)
    return best[1], best[2]

def s_strong(sc, ltg=None, lsg=None, n_iter=3, **kw):
    lt, ls = _anchor_TS(sc, ltg, lsg)
    q = sc.D.ravel()
    for it in range(n_iter):
        A, y = sc.design(lt, ls, dec=2)
        q, _ = nnls(A, y)
        st = (ltg[1] - ltg[0]) * (0.8 ** it); ss = (lsg[1] - lsg[0]) * (0.8 ** it)
        b = (np.inf, lt, ls)
        for a1 in np.clip(np.linspace(lt - st, lt + st, 7), LOGT_LO, LOGT_HI):
            for a2 in np.clip(np.linspace(ls - ss, ls + ss, 7), LOGS_LO, LOGS_HI):
                v = sc.sse(a1, a2, q, dec=2)
                if v < b[0]: b = (v, a1, a2)
        lt, ls = b[1], b[2]
    A, y = sc.design(lt, ls, dec=2)
    q, _ = nnls(A, y)
    return pack(sc.id, q.reshape(-1, KB), float(lt), float(ls))

def s_ceiling(sc, truth=None, **kw):
    lt, ls = truth[sc.id]
    A, y = sc.design(lt, ls, dec=2)
    q, _ = nnls(A, y)
    return pack(sc.id, q.reshape(-1, KB), lt, ls)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--public", required=True); ap.add_argument("--private", required=True)
    ap.add_argument("--strong-n", type=int, default=200)
    args = ap.parse_args()
    pub, priv = Path(args.public), Path(args.private)

    test = pd.read_csv(pub / "test.csv")
    train = pd.read_csv(pub / "train.csv")
    ans = pd.read_csv(priv / "answers.csv")
    print("rows: train %d  test %d   score groups %d   signal bands %s"
          % (len(train), len(test), ans["score_group"].nunique(),
             sorted(ans["signal_band"].unique())), flush=True)

    # public-column leak scan
    leak_terms = ["scene", "bg_pool", "rho", "kind", "actual", "log_t", "log_s",
                  "background", "site", "nwis"]
    for nm, df in (("train", train), ("test", test)):
        bad = [c for c in df.columns if any(t in c.lower() for t in leak_terms)]
        if nm == "train":
            bad = [c for c in bad if c not in ("actual", "log_t", "log_s")]
        print("leak.public_columns.%s: %s" % (nm, "FAIL " + str(bad) if bad else "pass"), flush=True)

    scenes = [Scene(r, pub / "test") for _, r in test.iterrows()]
    truth = {int(a["id"]): (float(a["log_t"]), float(a["log_s"])) for _, a in ans.iterrows()}
    mean_q = np.mean([np.array(json.loads(r), float).mean(axis=0)
                      for r in train["actual"]], axis=0)
    med = (float(train["log_t"].median()), float(train["log_s"].median()))
    rng = np.random.default_rng(11)
    ltg = np.linspace(LOGT_LO, LOGT_HI, 12); lsg = np.linspace(LOGS_LO, LOGS_HI, 10)

    res = {}
    def run(name, fn, subset=None):
        use = scenes if subset is None else scenes[:subset]
        ids = {s.id for s in use}
        a = ans[ans["id"].isin(ids)]
        t = time.time()
        sub = sub_frame([fn(s) for s in use])
        sec = (time.time() - t) / max(len(use), 1)
        sc = G.grade(sub, a)
        res[name] = {"score": round(sc, 4), "n": len(use), "sec_per_scene": round(sec, 3)}
        print("%-28s %.4f   (n=%d, %.2fs/scene)" % (name, sc, len(use), sec), flush=True)
        return sub

    # oracle
    orc = sub_frame([{"id": int(a["id"]), "actual": a["actual"],
                      "log_t": a["log_t"], "log_s": a["log_s"]} for _, a in ans.iterrows()])
    res["oracle"] = {"score": round(G.grade(orc, ans), 4), "n": len(ans)}
    print("%-28s %.4f" % ("oracle", res["oracle"]["score"]), flush=True)

    res["empty_submission"] = {"score": round(G.grade(pd.DataFrame(columns=["id"]), ans), 4)}
    print("%-28s %.4f" % ("empty_submission", res["empty_submission"]["score"]), flush=True)

    run("copy_declaration_noop", lambda s: s_declared(s, med))
    run("all_zeros", s_zero)
    run("train_prior_constant", lambda s: s_prior(s, mean_q, med))
    run("uniform_random", lambda s: s_random(s, rng=rng))
    samp = pd.read_csv(pub / "sample_submission.csv")
    res["sample_submission"] = {"score": round(G.grade(samp, ans), 4), "n": len(samp)}
    print("%-28s %.4f" % ("sample_submission", res["sample_submission"]["score"]), flush=True)
    run("weak_nnls_fixed_params", s_weak)
    run("ceiling_oracle_params", lambda s: s_ceiling(s, truth=truth), subset=args.strong_n)
    run("capability_matched_strong", lambda s: s_strong(s, ltg=ltg, lsg=lsg), subset=args.strong_n)

    # grader red-team
    bad = samp.copy(); bad["id"] = bad["id"] + 10 ** 7
    res["id_mismatch"] = {"score": round(G.grade(bad, ans), 4)}
    bad2 = samp.copy(); bad2["actual"] = "not json"
    res["malformed_json"] = {"score": round(G.grade(bad2, ans), 4)}
    bad3 = samp.copy(); bad3["log_t"] = "abc"; bad3["log_s"] = np.nan
    res["nan_scalars"] = {"score": round(G.grade(bad3, ans), 4)}
    bad4 = samp.copy(); bad4["actual"] = json.dumps([[-5e9] * KB] * 40)
    res["negative_huge"] = {"score": round(G.grade(bad4, ans), 4)}
    dup = pd.concat([samp, samp]); res["duplicate_ids"] = {"score": round(G.grade(dup, ans), 4)}
    for k in ("id_mismatch", "malformed_json", "nan_scalars", "negative_huge", "duplicate_ids"):
        print("redteam.%-20s %.4f" % (k, res[k]["score"]), flush=True)

    json.dump(res, open("analyze_results.json", "w"), indent=2)
    print("saved analyze_results.json", flush=True)


if __name__ == "__main__":
    main()

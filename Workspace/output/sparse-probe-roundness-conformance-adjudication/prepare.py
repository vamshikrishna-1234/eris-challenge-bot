#!/usr/bin/env python3
"""Deterministic preparation: raw corpus -> public/ and private/answers.csv.

Splits by MACHINE so that no machine, and therefore no part, appears on both sides. Public
identifiers are salted opaque hashes and every ordering is re-randomised, so the public split cannot
be joined back to raw row order, part numbering or machine numbering.
"""
import hashlib
import json
import os
import sys

import numpy as np
import pandas as pd

SALT = "spr-adj-20260920"
TEST_MACHINE_FRACTION = 0.35
SPLIT_SEED = 20260920
MIN_TRAIN_ROWS = 20000
MIN_TEST_ROWS = 8000
MIN_TRAIN_MACHINES = 300
MIN_TEST_MACHINES = 150
SIG_NAMES = ["three_jaw_chuck", "clamp_ovality", "spindle_bearing_order",
             "centreless_five_lobe", "fine_ground_smooth", "worn_tool_chatter"]


def find_raw(base):
    """Accept the organiser layout raw/<file> and the platform layout raw/raw_upload/<file>."""
    for cand in (base, os.path.join(base, "raw_upload"), os.path.join(base, "raw"),
                 os.path.join(base, "raw", "raw_upload")):
        if os.path.exists(os.path.join(cand, "features.csv")):
            return cand
    raise SystemExit("features.csv not found under %s" % base)


def opaque(kind, *parts):
    h = hashlib.sha256((SALT + "|" + kind + "|" + "|".join(str(p) for p in parts)).encode())
    return h.hexdigest()[:12 if kind == "row" else 10]


def main():
    raw_base = sys.argv[1] if len(sys.argv) > 1 else "raw_data"
    out = sys.argv[2] if len(sys.argv) > 2 else "."
    raw = find_raw(raw_base)

    feats = pd.read_csv(os.path.join(raw, "features.csv"))
    pts = pd.read_csv(os.path.join(raw, "points.csv"))
    for col in ("machine_index", "part_index", "feature_index", "feature_kind", "n_probe",
                "nominal_diameter_mm", "roundness_tol_um", "ront_um", "conform", "signature_class"):
        assert col in feats.columns, "raw features.csv missing column %s" % col
    assert set(feats.signature_class.unique()) <= set(SIG_NAMES), "unexpected signature class"
    assert feats.duplicated(["part_index", "feature_index"]).sum() == 0, "duplicate raw feature key"
    assert np.isfinite(feats.ront_um).all() and (feats.ront_um > 0).all()
    assert np.isfinite(pts[["x_mm", "y_mm"]].to_numpy()).all()

    # one machine per part
    assert feats.groupby("part_index").machine_index.nunique().max() == 1

    rng = np.random.default_rng(SPLIT_SEED)
    machines = np.sort(feats.machine_index.unique())
    perm = rng.permutation(machines)
    n_test = int(round(TEST_MACHINE_FRACTION * len(perm)))
    test_machines = set(int(m) for m in perm[:n_test])
    feats["is_test"] = feats.machine_index.isin(test_machines)

    pt_groups = {k: v for k, v in pts.groupby(["part_index", "feature_index"])}
    rows = []
    for rec in feats.itertuples(index=False):
        g = pt_groups[(rec.part_index, rec.feature_index)]
        xy = g.sort_values("point_index")[["x_mm", "y_mm"]].to_numpy()
        assert len(xy) == rec.n_probe, "probe count mismatch"
        # re-randomise probe order so raw point ordering carries no information
        order = np.random.default_rng(
            int(hashlib.sha256(("pt" + SALT + str(rec.part_index) + "_"
                                + str(rec.feature_index)).encode()).hexdigest()[:8], 16)
        ).permutation(len(xy))
        xy = xy[order]
        rows.append(dict(
            row_id=opaque("row", rec.part_index, rec.feature_index),
            part_id=opaque("part", rec.part_index),
            feature_kind=rec.feature_kind,
            n_probe=int(rec.n_probe),
            nominal_diameter_mm=float(rec.nominal_diameter_mm),
            roundness_tol_um=float(rec.roundness_tol_um),
            points_xy_mm=json.dumps([[round(float(a), 6), round(float(b), 6)] for a, b in xy]),
            ront_um=float(rec.ront_um), conform=int(rec.conform),
            signature_class=rec.signature_class, is_test=bool(rec.is_test),
            _machine=int(rec.machine_index), _part=int(rec.part_index),
        ))
    df = pd.DataFrame(rows)
    assert df.row_id.duplicated().sum() == 0, "opaque row id collision"

    # feature slot inside a part, assigned after a deterministic per-part shuffle
    df["feature_slot"] = (df.groupby("part_id").cumcount())
    df = df.sample(frac=1.0, random_state=SPLIT_SEED).reset_index(drop=True)

    train = df[~df.is_test].copy()
    test = df[df.is_test].copy()
    assert set(train._machine) & set(test._machine) == set(), "machine leaked across the split"
    assert set(train.part_id) & set(test.part_id) == set(), "part leaked across the split"
    assert len(train) >= MIN_TRAIN_ROWS, "train rows %d below minimum" % len(train)
    assert len(test) >= MIN_TEST_ROWS, "test rows %d below minimum" % len(test)
    assert train._machine.nunique() >= MIN_TRAIN_MACHINES
    assert test._machine.nunique() >= MIN_TEST_MACHINES
    for name in SIG_NAMES:
        assert (train.signature_class == name).sum() >= 200, "train class %s too small" % name
        assert (test.signature_class == name).sum() >= 100, "test class %s too small" % name

    pub_cols = ["row_id", "part_id", "feature_slot", "feature_kind", "n_probe",
                "nominal_diameter_mm", "roundness_tol_um", "points_xy_mm"]
    ans_cols = ["ront_um", "conform", "signature_class"]
    ans_extra = ["n_probe"]   # private subgroup key for the worst-band term in grade.py
    os.makedirs(os.path.join(out, "public"), exist_ok=True)
    os.makedirs(os.path.join(out, "private"), exist_ok=True)

    train_out = train[pub_cols + ans_cols].sort_values("row_id").reset_index(drop=True)
    test_out = test[pub_cols].sort_values("row_id").reset_index(drop=True)
    ans_out = test[["row_id"] + ans_cols + ans_extra].sort_values("row_id").reset_index(drop=True)
    train_out.to_csv(os.path.join(out, "public", "train.csv"), index=False)
    test_out.to_csv(os.path.join(out, "public", "test.csv"), index=False)
    ans_out.to_csv(os.path.join(out, "private", "answers.csv"), index=False)
    assert list(ans_out.row_id) == list(test_out.row_id), "answers/test id mismatch"

    # sample submission: label priors only, never an empty or degenerate submission
    q10, q50, q90 = np.quantile(train_out.ront_um, [0.10, 0.50, 0.90])
    base = float(train_out.conform.mean())
    majority = train_out.signature_class.value_counts().idxmax()
    pd.DataFrame(dict(row_id=test_out.row_id,
                      ront_p10_um=round(float(q10), 4), ront_p50_um=round(float(q50), 4),
                      ront_p90_um=round(float(q90), 4), p_conform=round(base, 4),
                      signature_class=majority)).to_csv(
        os.path.join(out, "public", "sample_submission.csv"), index=False)

    print("train rows %d  test rows %d" % (len(train_out), len(test_out)))
    print("train machines %d  test machines %d"
          % (train._machine.nunique(), test._machine.nunique()))
    print("train parts %d  test parts %d" % (train.part_id.nunique(), test.part_id.nunique()))
    print("conform base rate train %.4f test %.4f" % (base, ans_out.conform.mean()))
    print("GRADER REFERENCE CONSTANTS (prior baseline on the prepared test split):")
    y = ans_out.ront_um.to_numpy()
    lo, md, hi = float(q10), float(q50), float(q90)
    iscore = float(np.mean((hi - lo) + 10 * np.maximum(lo - y, 0) + 10 * np.maximum(y - hi, 0)
                           + 2 * np.abs(y - md)))
    brier = float(np.mean((base - ans_out.conform.to_numpy()) ** 2))
    acc = float((ans_out.signature_class == majority).mean())
    print("  prior interval loss  %.6f  -> REF_Q = %.6f" % (iscore, iscore / 0.85))
    print("  prior brier          %.6f  -> REF_B = %.6f" % (brier, brier / 0.85))
    print("  prior sig accuracy   %.6f  -> REF_S = %.6f" % (acc, (acc - 0.15) / 0.85))


if __name__ == "__main__":
    main()

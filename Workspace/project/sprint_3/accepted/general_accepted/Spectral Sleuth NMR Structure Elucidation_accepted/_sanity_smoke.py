"""Smoke test + audit. Runs prepare() on the raw nmrshiftdb2 SDF (small slice)
and checks grade() baselines plus the five review gates: data leakage, baseline
not too high, class distribution, no missing data, and oracle solvability.

Organiser-side only; not shipped. Set SDF_RAW to the folder holding the raw
.sd file (default: _devdata)."""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import grade as G
import prepare as P

RAW = Path(os.environ.get("SDF_RAW", "_devdata"))


def _perfect(ans):
    rows = []
    for _, r in ans.iterrows():
        sub = {"id": int(r["id"])}
        for k in range(G.K):
            sub[f"pred_prob_{k+1}"] = 1.0 if (k + 1) == int(r["true_isomer_idx"]) else 0.0
        rows.append(sub)
    return pd.DataFrame(rows)


def _uniform(ans):
    rows = []
    for _, r in ans.iterrows():
        sub = {"id": int(r["id"])}
        for k in range(G.K):
            sub[f"pred_prob_{k+1}"] = 1.0 / G.K
        rows.append(sub)
    return pd.DataFrame(rows)


def _confident_const(ans, slot):
    rows = []
    for _, r in ans.iterrows():
        sub = {"id": int(r["id"])}
        for k in range(G.K):
            sub[f"pred_prob_{k+1}"] = 1.0 if k == slot else 0.0
        rows.append(sub)
    return pd.DataFrame(rows)


def _random(ans, seed):
    rng = np.random.default_rng(seed)
    rows = []
    for _, r in ans.iterrows():
        sub = {"id": int(r["id"])}
        p = rng.random(G.K)
        p = p / p.sum()
        for k in range(G.K):
            sub[f"pred_prob_{k+1}"] = float(p[k])
        rows.append(sub)
    return pd.DataFrame(rows)


def main():
    P.N_TRAIN = 400
    P.N_TEST = 200
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        pub, priv = td / "pub", td / "priv"
        P.prepare(RAW, pub, priv)

        train = pd.read_csv(pub / "train.csv")
        test = pd.read_csv(pub / "test.csv")
        ans = pd.read_csv(priv / "answers.csv")
        cand_cols = [f"candidate_{k+1}" for k in range(G.K)]

        # ---- baselines ----
        s_perfect = G.grade(_perfect(ans), ans)
        s_uniform = G.grade(_uniform(ans), ans)
        s_const = G.grade(_confident_const(ans, 0), ans)
        s_random = G.grade(_random(ans, 7), ans)
        print(f"perfect      = {s_perfect:.4f}  (expect ~1.00)")
        print(f"uniform      = {s_uniform:.4f}  (expect ~0.03)")
        print(f"const slot1  = {s_const:.4f}   (confident-always-1)")
        print(f"random probs = {s_random:.4f}")
        assert s_perfect > 0.99, f"oracle not solvable: {s_perfect}"

        # robustness
        dup = pd.concat([_perfect(ans), _perfect(ans).head(1)], ignore_index=True)
        assert G.grade(dup, ans) == 0.0, "dup ids must score 0"
        miss = _perfect(ans).drop(columns=["pred_prob_1"])
        assert G.grade(miss, ans) == 0.0, "missing col must score 0"
        short = _perfect(ans).iloc[:-3].copy()
        assert G.grade(short, ans) == 0.0, "id mismatch must score 0"
        print("robustness (dup/missing/short) -> 0.0  OK")

        # ---- 1. DATA LEAKAGE: no test SMILES (target or distractor) seen in train ----
        train_smiles = set()
        for c in cand_cols:
            train_smiles |= set(train[c].tolist())
        test_smiles = set()
        for c in cand_cols:
            test_smiles |= set(test[c].tolist())
        overlap = train_smiles & test_smiles
        assert not overlap, f"LEAK: {len(overlap)} SMILES shared train/test"
        # also formula-disjoint
        assert set(train["molecular_formula"]).isdisjoint(set(test["molecular_formula"])), "formula overlap"
        print(f"[1] leakage: {len(train_smiles)} train / {len(test_smiles)} test SMILES, disjoint OK")

        # ---- 2. BASELINE not too high ----
        assert s_uniform < 0.10 and s_const < 0.15 and s_random < 0.15, "baseline too high"
        print("[2] baselines all < 0.15  OK")

        # ---- 3. CLASS DISTRIBUTION: true index roughly uniform over 1..K ----
        dist = ans["true_isomer_idx"].value_counts(normalize=True).sort_index()
        print(f"[3] true_isomer_idx dist: {dist.round(3).to_dict()}")
        assert dist.min() > 0.5 / G.K, "an index class is severely under-represented"
        # every row has exactly K distinct candidates
        for _, r in test.iterrows():
            cs = [r[c] for c in cand_cols]
            assert len(set(cs)) == G.K, "candidates not distinct"

        # ---- 4. NO MISSING DATA ----
        for name, df in [("train", train), ("test", test), ("answers", ans)]:
            assert df.isnull().sum().sum() == 0, f"NULL in {name}"
        for _, r in test.iterrows():
            assert (pub / "test" / r["image_path"]).exists(), "missing test image"
        print("[4] no nulls; all test images present  OK")

        print("\nAUDIT PASSED")


if __name__ == "__main__":
    main()

"""Smoke test for FragmentFold.

Runs prepare() on the real MassBank-derived spectra.csv, then verifies:
  1. data leakage  -> train/test id disjoint; answers match test id set;
                      NO scaffold appears in both train and test (the core
                      anti-library-lookup property).
  2. baselines     -> perfect = 1.0; all-zeros = 0.0; train-majority bits and
                      random bits are well below the realistic-learning band.
  3. distribution  -> adduct / ion-mode coverage in train and test.
  4. no missing    -> no NULLs / blank fingerprints in any output CSV.
  5. robustness    -> dup-id / missing-col / short submissions return 0.0.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import grade as G  # noqa: E402
import prepare as P  # noqa: E402

RAW = Path(__file__).parent / "raw_data"
N_BITS = P.N_BITS


def _bits(s):
    t = str(s).strip()
    if t[:1] in ("b", "B"):
        t = t[1:]
    return np.frombuffer(t.encode("ascii"), dtype=np.uint8) - ord("0")


def _fp(bits_arr):
    return "b" + "".join(str(int(b)) for b in bits_arr)


def _probs(arr):
    return ";".join(f"{float(b):.4f}" for b in arr)


def main() -> None:
    out = Path(__file__).parent / "_smoke_out"
    pub = out / "public"
    priv = out / "private"
    import shutil
    if out.exists():
        shutil.rmtree(out, ignore_errors=True)
    P.prepare(RAW, pub, priv)

    train = pd.read_csv(pub / "train.csv")
    test = pd.read_csv(pub / "test.csv")
    sample = pd.read_csv(pub / "sample_submission.csv")
    ans = pd.read_csv(priv / "answers.csv")

    print("\n=== AUDIT REPORT ===")
    print(f"train={len(train)}  test={len(test)}  answers={len(ans)}  bits={N_BITS}")

    # 1. leakage
    tr_ids, te_ids, an_ids = set(train["id"]), set(test["id"]), set(ans["id"])
    print("\n1. DATA LEAKAGE")
    print(f"   train/test id overlap: {len(tr_ids & te_ids)} (expect 0)")
    print(f"   test/answers id match: {te_ids == an_ids} (expect True)")
    assert len(tr_ids & te_ids) == 0
    assert te_ids == an_ids

    # scaffold disjointness: re-derive scaffolds from raw + re-run split logic
    rows = P._load_and_featurise(P._find_spectra_csv(RAW))
    train_idx, test_idx = P._scaffold_split(rows)
    tr_scaf = {rows[i]["scaffold"] for i in train_idx}
    te_scaf = {rows[i]["scaffold"] for i in test_idx}
    print(f"   scaffold overlap train/test: {len(tr_scaf & te_scaf)} (expect 0)")
    assert len(tr_scaf & te_scaf) == 0, "SCAFFOLD LEAKAGE"

    # 4. no missing
    print("\n4. NO MISSING DATA")
    for name, df in [("train", train), ("test", test), ("answers", ans), ("sample", sample)]:
        n_null = int(df.isnull().sum().sum())
        print(f"   {name}: {n_null} NULLs (expect 0)")
        assert n_null == 0, f"{name} has NULLs"
    assert (train["fingerprint"].str.len() == N_BITS + 1).all()
    assert (ans["fingerprint"].str.len() == N_BITS + 1).all()

    # 3. distribution
    print("\n3. DISTRIBUTION")
    print(f"   train adducts: {dict(Counter(train['adduct']).most_common(5))}")
    print(f"   test  adducts: {dict(Counter(test['adduct']).most_common(5))}")
    print(f"   train ion_mode: {dict(Counter(train['ion_mode']))}")
    bits_mat = np.stack([_bits(s) for s in ans["fingerprint"]])
    print(f"   mean bits set per molecule: {bits_mat.sum(1).mean():.1f} / {N_BITS}")

    # 2. baselines
    print("\n2. BASELINES (target: trivial << learning << 1.0)")

    perfect = pd.DataFrame({"id": ans["id"], "pred_probs": [_probs(_bits(s)) for s in ans["fingerprint"]]})
    s_perfect = G.grade(perfect, ans)
    print(f"   perfect:            {s_perfect:.4f} (expect 1.0)")

    allzero = pd.DataFrame({"id": ans["id"], "pred_probs": [_probs(np.zeros(N_BITS))] * len(ans)})
    s_zero = G.grade(allzero, ans)
    print(f"   all-zeros:          {s_zero:.4f} (expect 0.0)")

    flat = pd.DataFrame({"id": ans["id"], "pred_probs": [_probs(np.full(N_BITS, 0.5))] * len(ans)})
    s_flat = G.grade(flat, ans)
    print(f"   flat-0.5:           {s_flat:.4f} (expect 0.0)")

    # train marginal frequencies as PROBABILITIES = the climatological baseline.
    # Under the scaffold-disjoint split this should score NEAR 0 (the doc claim).
    tr_bits = np.stack([_bits(s) for s in train["fingerprint"]])
    tr_marg = tr_bits.mean(0)
    s_marg = G.grade(pd.DataFrame({"id": ans["id"], "pred_probs": [_probs(tr_marg)] * len(ans)}), ans)
    print(f"   train-marginal:     {s_marg:.4f} (climatology; want near 0)")

    # train-majority hard fingerprint (bits set if frequency > 0.5 in train)
    maj = (tr_bits.mean(0) > 0.5).astype(np.uint8)
    s_maj = G.grade(pd.DataFrame({"id": ans["id"], "pred_probs": [_probs(maj)] * len(ans)}), ans)
    print(f"   train-majority fp:  {s_maj:.4f} (trivial constant; want < 0.45)")

    rng = np.random.default_rng(0)
    p_set = float(tr_bits.mean())
    rnd = [_probs((rng.random(N_BITS) < p_set).astype(np.uint8)) for _ in range(len(ans))]
    s_rnd = G.grade(pd.DataFrame({"id": ans["id"], "pred_probs": rnd}), ans)
    print(f"   random (matched p): {s_rnd:.4f} (want < 0.30)")

    # 5. robustness
    print("\n5. ROBUSTNESS (expect 0.0)")
    dup = pd.concat([perfect, perfect.head(1)], ignore_index=True)
    s_dup = G.grade(dup, ans)
    print(f"   duplicate-id:       {s_dup:.4f}")
    assert s_dup == 0.0
    miss = perfect.drop(columns=["pred_probs"])
    s_miss = G.grade(miss, ans)
    print(f"   missing-col:        {s_miss:.4f}")
    assert s_miss == 0.0
    short = perfect.iloc[:-3]
    s_short = G.grade(short, ans)
    print(f"   short-set:          {s_short:.4f}")
    assert s_short == 0.0

    # 6. determinism: re-running prepare yields identical public id ordering
    print("\n6. DETERMINISM (id order stable across runs)")
    out2 = Path(__file__).parent / "_smoke_out2"
    if out2.exists():
        shutil.rmtree(out2, ignore_errors=True)
    P.prepare(RAW, out2 / "public", out2 / "private")
    test2 = pd.read_csv(out2 / "public" / "test.csv")
    same_order = test["id"].tolist() == test2["id"].tolist()
    print(f"   test id order identical: {same_order} (expect True)")
    assert same_order, "prepare is not deterministic"
    shutil.rmtree(out2, ignore_errors=True)

    assert s_perfect > 0.999
    assert s_zero == 0.0
    assert s_flat == 0.0
    assert s_marg < 0.10, f"climatology baseline not near 0: {s_marg}"
    assert s_maj < 0.45, f"majority baseline too high: {s_maj}"
    assert s_rnd < 0.30

    print("\nOK: smoke test passed.")
    shutil.rmtree(out, ignore_errors=True)


if __name__ == "__main__":
    main()

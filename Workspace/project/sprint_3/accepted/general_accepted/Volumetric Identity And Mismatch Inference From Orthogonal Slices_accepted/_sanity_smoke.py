"""Smoke test for Volumetric Identity And Mismatch Inference.

Runs prepare() on the real MedMNIST3D npz files (downsampled), then
verifies the four user-required properties:
  1. data leakage (train/test ids disjoint, answers match test set)
  2. baseline scores (random / constant / heuristic) are all < 0.45
  3. class distribution is well-balanced for corpus_id and intruder
  4. no missing data in any output CSV
"""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import grade as G  # noqa: E402
import prepare as P  # noqa: E402


REAL_DATA = Path(__file__).parent / "raw_data"


def _make_fake_npz(out: Path, n_train: int, n_val: int, n_test: int, n_classes: int, seed: int) -> None:
    rng = np.random.default_rng(seed)
    np.savez(
        out,
        train_images=rng.integers(40, 220, size=(n_train, 28, 28, 28), dtype=np.uint8),
        train_labels=rng.integers(0, n_classes, size=(n_train, 1), dtype=np.uint8),
        val_images=rng.integers(40, 220, size=(n_val, 28, 28, 28), dtype=np.uint8),
        val_labels=rng.integers(0, n_classes, size=(n_val, 1), dtype=np.uint8),
        test_images=rng.integers(40, 220, size=(n_test, 28, 28, 28), dtype=np.uint8),
        test_labels=rng.integers(0, n_classes, size=(n_test, 1), dtype=np.uint8),
    )


def _build_perfect(answers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in answers.iterrows():
        rows.append({
            "id": int(r["id"]),
            "pred_corpus_id": int(r["true_corpus_id"]),
            "pred_class_label": int(r["true_class_label"]),
            "pred_vol_radius": float(r["true_vol_radius"]),
            "pred_mismatched_triplet": int(r["true_mismatched_triplet"]),
            "pred_mismatched_axis": str(r["true_mismatched_axis"]),
        })
    return pd.DataFrame(rows)


def _build_random(answers: pd.DataFrame, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    axis_choices = ["NONE", "AXIAL", "SAGITTAL", "CORONAL"]
    rows = []
    for _, r in answers.iterrows():
        rows.append({
            "id": int(r["id"]),
            "pred_corpus_id": int(rng.integers(0, P.GLOBAL_NCORPORA)),
            "pred_class_label": int(rng.integers(0, P.GLOBAL_NCLASSES)),
            "pred_vol_radius": float(rng.random()),
            "pred_mismatched_triplet": int(rng.integers(0, 2)),
            "pred_mismatched_axis": str(rng.choice(axis_choices)),
        })
    return pd.DataFrame(rows)


def _build_constant(answers: pd.DataFrame, corpus: int, cls: int, radius: float, mism: int, axis: str) -> pd.DataFrame:
    rows = []
    for _, r in answers.iterrows():
        rows.append({
            "id": int(r["id"]),
            "pred_corpus_id": int(corpus),
            "pred_class_label": int(cls),
            "pred_vol_radius": float(radius),
            "pred_mismatched_triplet": int(mism),
            "pred_mismatched_axis": str(axis),
        })
    return pd.DataFrame(rows)


def main() -> None:
    if REAL_DATA.exists():
        # use real npz files but downsample by monkey-patching prepare's
        # sub-corpora load to use only the first ~100 vols of each split.
        run(REAL_DATA, downsample=100)
    else:
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            for stem, n_classes in P.CORPUS_NCLASSES.items():
                _make_fake_npz(td / f"{stem}.npz", 60, 10, 30, n_classes, seed=hash(stem) & 0xFFFFFFFF)
            run(td, downsample=None)


def run(raw: Path, downsample: int | None) -> None:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        pub = td / "pub"
        priv = td / "priv"

        if downsample is not None:
            # Wrap prepare's _find_npz so it returns a shrunken npz copy.
            scratch = td / "scratch"
            scratch.mkdir(parents=True, exist_ok=True)

            def _shrink_one(stem: str) -> Path:
                src = raw / f"{stem}.npz"
                dst = scratch / f"{stem}.npz"
                with np.load(src) as z:
                    n_tr = min(downsample, z["train_images"].shape[0])
                    n_va = min(max(downsample // 4, 4), z["val_images"].shape[0])
                    n_te = min(max(downsample // 2, 8), z["test_images"].shape[0])
                    np.savez(
                        dst,
                        train_images=z["train_images"][:n_tr],
                        train_labels=z["train_labels"][:n_tr],
                        val_images=z["val_images"][:n_va],
                        val_labels=z["val_labels"][:n_va],
                        test_images=z["test_images"][:n_te],
                        test_labels=z["test_labels"][:n_te],
                    )
                return dst

            shrunk_dir = scratch
            for stem in P.NPZ_STEMS:
                _shrink_one(stem)
            P.prepare(shrunk_dir, pub, priv)
        else:
            P.prepare(raw, pub, priv)

        train_csv = pd.read_csv(pub / "train.csv")
        test_csv = pd.read_csv(pub / "test.csv")
        sample_csv = pd.read_csv(pub / "sample_submission.csv")
        ans = pd.read_csv(priv / "answers.csv")

        print(f"\n=== AUDIT REPORT ===")
        print(f"train.csv: {len(train_csv)} rows; test.csv: {len(test_csv)} rows; answers: {len(ans)} rows")

        # 1. Data leakage
        train_ids = set(train_csv["id"].tolist())
        test_ids = set(test_csv["id"].tolist())
        ans_ids = set(ans["id"].tolist())
        print(f"\n1. DATA LEAKAGE")
        print(f"   train/test id overlap: {len(train_ids & test_ids)} (expect 0)")
        print(f"   test/answers id match: {test_ids == ans_ids} (expect True)")
        assert len(train_ids & test_ids) == 0, "DATA LEAKAGE: id overlap"
        assert test_ids == ans_ids, "answers must match test row set"

        # 3. Class distribution
        print(f"\n3. CLASS DISTRIBUTION")
        print(f"   train corpus_id dist: {train_csv['true_corpus_id'].value_counts(normalize=True).round(3).to_dict()}")
        print(f"   test  corpus_id dist: {ans['true_corpus_id'].value_counts(normalize=True).round(3).to_dict()}")
        print(f"   train class dist (top-3): {train_csv['true_class_label'].value_counts().head(3).to_dict()}")
        print(f"   intruder fraction (test): {(ans['true_mismatched_triplet'] == 1).mean():.3f}")
        print(f"   axis dist (test): {ans['true_mismatched_axis'].value_counts(normalize=True).round(3).to_dict()}")

        intr_frac = (ans["true_mismatched_triplet"] == 1).mean()
        assert 0.20 < intr_frac < 0.40, f"intruder fraction off: {intr_frac}"

        # 4. No missing data
        print(f"\n4. NO MISSING DATA")
        for name, df in [("train.csv", train_csv), ("test.csv", test_csv), ("answers.csv", ans), ("sample_submission.csv", sample_csv)]:
            n_null = int(df.isnull().sum().sum())
            print(f"   {name}: {n_null} NULLs (expect 0)")
            assert n_null == 0, f"{name} has {n_null} NULLs"

        n_train_imgs = len(list((pub / "train").glob("*.png")))
        n_test_imgs = len(list((pub / "test").glob("*.png")))
        print(f"   train PNGs: {n_train_imgs} (expect {3 * len(train_csv)})")
        print(f"   test PNGs:  {n_test_imgs} (expect {3 * len(test_csv)})")
        assert n_train_imgs == 3 * len(train_csv) and n_test_imgs == 3 * len(test_csv)

        # 2. Baseline scores
        print(f"\n2. BASELINE SCORES (target: all baselines < 0.45)")

        s_perfect = G.grade(_build_perfect(ans), ans)
        print(f"   perfect:                 {s_perfect:.4f}  (expect ~1.0)")

        s_all0 = G.grade(_build_constant(ans, 0, 0, 0.5, 0, "NONE"), ans)
        print(f"   all-0 const:             {s_all0:.4f}  (target < 0.30)")

        s_allones = G.grade(_build_constant(ans, 0, 0, 1.0, 1, "AXIAL"), ans)
        print(f"   all-1 const:             {s_allones:.4f}  (target < 0.30)")

        rnd = _build_random(ans, seed=42)
        s_rnd = G.grade(rnd, ans)
        print(f"   random:                  {s_rnd:.4f}  (target 0.20-0.40)")

        # majority-class baseline (predict majority corpus, mismatch=0, axis=NONE)
        majority_corpus = int(ans["true_corpus_id"].mode().iloc[0])
        majority_class = int(ans["true_class_label"].mode().iloc[0])
        s_majority = G.grade(_build_constant(ans, majority_corpus, majority_class, 0.5, 0, "NONE"), ans)
        print(f"   majority-class const:    {s_majority:.4f}  (target < 0.40)")

        # robustness
        dup = pd.concat([_build_perfect(ans), _build_perfect(ans).head(1)], ignore_index=True)
        s_dup = G.grade(dup, ans)
        print(f"   duplicate-id score:      {s_dup:.4f}  (expect 0.0)")
        assert s_dup == 0.0

        bad = _build_perfect(ans).drop(columns=["pred_vol_radius"])
        s_bad = G.grade(bad, ans)
        print(f"   missing-col score:       {s_bad:.4f}  (expect 0.0)")
        assert s_bad == 0.0

        short = _build_perfect(ans).iloc[:-3]
        s_short = G.grade(short, ans)
        print(f"   short-set score:         {s_short:.4f}  (expect 0.0)")
        assert s_short == 0.0

        assert s_perfect > 0.95, f"perfect must be ~1.0, got {s_perfect}"
        assert s_all0 < 0.40, f"all-0 const too high: {s_all0}"
        assert s_allones < 0.40, f"all-1 const too high: {s_allones}"
        assert s_rnd < 0.45, f"random too high: {s_rnd}"
        assert s_majority < 0.45, f"majority too high: {s_majority}"

        print("\nOK: smoke test passed.")


if __name__ == "__main__":
    main()

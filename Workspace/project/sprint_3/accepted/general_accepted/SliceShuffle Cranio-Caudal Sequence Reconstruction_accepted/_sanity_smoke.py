"""Smoke test: synthesise tiny fake .nii.gz files, run prepare(), then
verify perfect / random / weak baselines against grade().

Not shipped to the platform; for organiser-side validation only.
"""

from __future__ import annotations

import gzip
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import grade as G  # noqa: E402


def _make_fake_nifti_dir(n_subjects: int, out_dir: Path) -> None:
    """Create n_subjects fake .nii.gz files that nibabel can read."""
    try:
        import nibabel as nib
    except ImportError:
        import subprocess
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "nibabel"],
        )
        import nibabel as nib

    out_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(42)
    for i in range(n_subjects):
        shape = (64, 64, 110)
        arr = np.zeros(shape, dtype=np.float32)
        for z in range(shape[2]):
            band_y = int(8 + z * 0.45)
            lo = max(0, band_y - 3)
            hi = min(shape[0], band_y + 3)
            arr[lo:hi, :, z] = 200.0
        arr += rng.normal(0, 4, arr.shape).astype(np.float32)
        arr = np.clip(arr, 0, 500)
        img = nib.Nifti1Image(arr, affine=np.eye(4))
        fname = out_dir / f"FAKE{i:03d}-Site-0000-T1.nii.gz"
        nib.save(img, str(fname))


def _build_perfect_submission(answers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in answers.iterrows():
        rows.append({
            "row_id": r["row_id"],
            "volume_id": int(r["volume_id"]),
            "presented_index": int(r["presented_index"]),
            "pred_rank": int(r["true_rank"]),
            "pred_missing_mask": r["true_missing_mask"],
        })
    return pd.DataFrame(rows)


def _build_random_submission(answers: pd.DataFrame, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    by_vol: dict = {}
    for _, r in answers.iterrows():
        by_vol.setdefault(int(r["volume_id"]), []).append(r)
    for vol_id, vol_rows in by_vol.items():
        ranks = rng.permutation(G.SLICES_PRESENTED).tolist()
        positions = rng.choice(
            G.SLICES_PER_VOLUME,
            size=G.SLICES_PER_VOLUME - G.SLICES_PRESENTED,
            replace=False,
        )
        bits = ["0"] * G.SLICES_PER_VOLUME
        for p in positions:
            bits[int(p)] = "1"
        mask_str = "M" + "".join(bits)
        for k, r in enumerate(sorted(vol_rows, key=lambda r: int(r["presented_index"]))):
            rows.append({
                "row_id": int(r["row_id"]),
                "volume_id": int(r["volume_id"]),
                "presented_index": int(r["presented_index"]),
                "pred_rank": ranks[k],
                "pred_missing_mask": mask_str,
            })
    return pd.DataFrame(rows)


def main() -> None:
    import prepare as P

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        raw = td / "raw"
        pub = td / "public"
        priv = td / "private"
        _make_fake_nifti_dir(120, raw)
        P.prepare(raw, pub, priv)
        ans = pd.read_csv(priv / "answers.csv")
        n_test_volumes = int(ans["volume_id"].nunique())
        print(f"prepared: {n_test_volumes} test volumes, {len(ans)} answer rows")

        perfect = _build_perfect_submission(ans)
        s_perfect = G.grade(perfect, ans)
        print(f"perfect score    = {s_perfect:.4f}  (expect ~1.00)")

        random_sub = _build_random_submission(ans, seed=7)
        s_random = G.grade(random_sub, ans)
        print(f"random score     = {s_random:.4f}  (expect <0.15 with squared metrics)")

        rows = []
        n_miss = G.SLICES_PER_VOLUME - G.SLICES_PRESENTED
        identity_mask = "M" + "1" * n_miss + "0" * (G.SLICES_PER_VOLUME - n_miss)
        for _, r in ans.iterrows():
            rows.append({
                "row_id": int(r["row_id"]),
                "volume_id": int(r["volume_id"]),
                "presented_index": int(r["presented_index"]),
                "pred_rank": int(r["presented_index"]),
                "pred_missing_mask": identity_mask,
            })
        identity = pd.DataFrame(rows)
        s_id = G.grade(identity, ans)
        print(f"identity score   = {s_id:.4f}  (rank=presented, mask=M11..0..)")

        dup_rows = identity.copy()
        dup_rows = pd.concat([dup_rows, identity.head(1)], ignore_index=True)
        s_dup = G.grade(dup_rows, ans)
        print(f"duplicate score  = {s_dup:.4f}  (expect 0.00, dup rows rejected)")

        bad_cols = identity.drop(columns=["pred_rank"])
        s_bad = G.grade(bad_cols, ans)
        print(f"missing-col score= {s_bad:.4f}  (expect 0.00, schema violation)")

        assert s_perfect > 0.95, f"perfect should score ~1.0, got {s_perfect}"
        assert s_random < 0.20, f"random unexpected: {s_random}"
        assert s_dup == 0.0, f"duplicate should score 0.0, got {s_dup}"
        assert s_bad == 0.0, f"missing-col should score 0.0, got {s_bad}"
        print("OK: smoke test passed.")


if __name__ == "__main__":
    main()

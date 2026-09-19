"""
prepare.py - SliceShuffle: Cranio-Caudal Sequence Reconstruction

Consumes raw_data/ containing IXI T1 brain MRI NIfTI files (*.nii.gz)
and produces deterministic public/ + private/ splits.

PHASE 1 - NIfTI ingestion:
  For each .nii.gz file in raw_data/:
    1. Load with nibabel, reorient to canonical RAS so axis 2 is the
       cranio-caudal (z) axis.
    2. Find the axial z-range containing brain tissue.
    3. Uniformly sample 48 axial slices from the central 75% of that
       z-range (the cranial / caudal extremes are excluded so that
       adjacent visible slices have more similar anatomy and pairwise
       ranking is harder).
    4. Intensity-normalise (1st-99th percentile of in-brain voxels),
       resize in-plane to 192x192, quantise to uint8.
    5. Subjects with fewer than 60 in-brain axial slices are skipped.
  Result: an in-memory (N, 48, 192, 192) uint8 tensor.

PHASE 2 - Challenge-specific curation:
  Per volume (48 contiguous axial slices from each subject's brain):
    1. Pick 16 axial indices (out of 48) to be "missing", sampled with a
       mild edge bias.
    2. The 32 surviving slices are permuted into a random presentation
       order presented_index in {0..31}.
    3. Each presented slice is written as a 192x192 PNG after a stronger,
       irreversible pixel-domain transform (per-slice 50/50 horizontal
       flip, per-slice random in-plane rotation, wide gamma jitter,
       small brightness shift, Gaussian noise, JPEG round-trip, then
       PNG save). Applied identically on train and test so the
       pixel-statistic distributions match across splits.
    4. true_rank in {0..31} is the cranio-caudal rank of the slice at
       presented_index, rank 0 = most caudal visible.
    5. true_missing_mask is "M" + 48 chars "0"/"1" indicating which of
       the original 48 axial positions were dropped (exactly 16 ones).

  Train-side label noise (test labels stay clean):
    * A small fraction of training volumes have an adjacent rank pair
      swapped on `true_rank`.
    * A small fraction of training volumes have a single bit flipped in
      `true_missing_mask`.

OUTPUT LAYOUT
-------------
    public/train/<volume_id_4d>/s00.png ... s31.png
    public/test/<volume_id_4d>/s00.png ... s31.png
    public/train.csv              row_id, volume_id, presented_index,
                                  true_rank, true_missing_mask
    public/test.csv               row_id, volume_id, presented_index
    public/sample_submission.csv  row_id, volume_id, presented_index,
                                  pred_rank, pred_missing_mask
    private/answers.csv           row_id, volume_id, presented_index,
                                  true_rank, true_missing_mask
"""

from __future__ import annotations

import io
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

# ---------- Phase-1 constants (NIfTI ingestion) ----------

INGEST_HW = 192
INGEST_SLICES = 48
MIN_BRAIN_SLICES = 60
BRAIN_THRESHOLD_FRAC = 0.05
MAX_SUBJECTS = 600
NARROW_Z_KEEP_FRAC = 0.75

# ---------- Phase-2 constants (challenge curation) ----------

SLICES_PER_VOLUME = 48
SLICES_PRESENTED = 32
SLICES_MISSING = SLICES_PER_VOLUME - SLICES_PRESENTED  # = 16
TARGET_HW = 192
TEST_FRACTION = 0.18

EDGE_BANDS = list(range(0, 6)) + list(range(42, 48))   # 12 positions
MIDDLE_BAND = list(range(6, 42))                       # 36 positions
EDGE_SHARE = 0.50

JPEG_Q = 60
NOISE_SIGMA = 5.0 / 255.0
GAMMA_LO, GAMMA_HI = 0.70, 1.40
ROT_DEG = 12.0

ADJACENT_SWAP_FRAC = 0.15
MASK_BITFLIP_FRAC = 0.08

MASK_PREFIX = "M"

SPLIT_SEED = 0xA1B2C3D4
DROP_SEED = 0xB2C3D4E5
PERM_SEED = 0xC3D4E5F6
PERTURB_SEED = 0xD4E5F607
LABEL_NOISE_SEED = 0xE5F60718


# ===== Phase 1: NIfTI ingestion helpers =====

def _ensure_nibabel():
    """Import nibabel, installing it first if missing."""
    try:
        import nibabel  # noqa: F401
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "nibabel"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )


def _load_nifti(path: Path) -> np.ndarray:
    import nibabel as nib

    img = nib.load(str(path))
    img = nib.as_closest_canonical(img)
    arr = np.asarray(img.get_fdata(dtype=np.float32))
    if arr.ndim == 4:
        arr = arr[..., 0]
    if arr.ndim != 3:
        raise ValueError(f"Expected 3D NIfTI, got shape {arr.shape}")
    return arr


def _resize_2d(slice2d: np.ndarray, size: int) -> np.ndarray:
    a = slice2d.astype(np.float32)
    img = Image.fromarray(a, mode="F")
    img = img.resize((size, size), resample=Image.BICUBIC)
    return np.asarray(img, dtype=np.float32)


def _extract_volume(arr: np.ndarray) -> np.ndarray | None:
    if arr.size == 0:
        return None
    vmax = float(arr.max())
    if vmax <= 0:
        return None
    thresh = BRAIN_THRESHOLD_FRAC * vmax
    nz_per_z = (arr > thresh).reshape(-1, arr.shape[2]).sum(axis=0)
    valid_z = np.where(nz_per_z > 0.005 * arr.shape[0] * arr.shape[1])[0]
    if valid_z.size < MIN_BRAIN_SLICES:
        return None

    z_lo, z_hi = int(valid_z.min()), int(valid_z.max())
    span = z_hi - z_lo + 1
    if span < INGEST_SLICES:
        return None

    # Sample slices from the central NARROW_Z_KEEP_FRAC of the brain
    # z-range so adjacent visible slices have more similar anatomy
    # (harder pairwise ranking).
    margin = int(span * (1.0 - NARROW_Z_KEEP_FRAC) * 0.5)
    z_lo_n = z_lo + margin
    z_hi_n = z_hi - margin
    if z_hi_n - z_lo_n + 1 < INGEST_SLICES:
        z_lo_n, z_hi_n = z_lo, z_hi
    idxs = np.linspace(z_lo_n, z_hi_n, INGEST_SLICES).round().astype(int)

    in_brain = arr[..., z_lo:z_hi + 1]
    flat = in_brain[in_brain > thresh]
    if flat.size == 0:
        return None
    p1, p99 = np.percentile(flat, [1.0, 99.0])
    if p99 <= p1:
        return None

    out = np.empty((INGEST_SLICES, INGEST_HW, INGEST_HW), dtype=np.uint8)
    for k, z in enumerate(idxs):
        s = arr[:, :, int(z)].T
        s = _resize_2d(s, INGEST_HW)
        s = np.clip((s - p1) / (p99 - p1), 0.0, 1.0)
        out[k] = (s * 255.0 + 0.5).astype(np.uint8)
    return out


def _ingest_nifti_dir(raw: Path) -> np.ndarray:
    """Read all .nii.gz files from raw/, return (N, 32, 256, 256) uint8."""
    _ensure_nibabel()
    nifti_files = sorted(raw.rglob("*.nii.gz"))
    if not nifti_files:
        raise FileNotFoundError(
            f"No .nii.gz files found under {raw}. Upload the IXI T1 "
            f"NIfTI archive as the raw dataset."
        )

    volumes: list[np.ndarray] = []
    skipped = 0
    for p in nifti_files:
        if len(volumes) >= MAX_SUBJECTS:
            break
        try:
            arr = _load_nifti(p)
        except Exception:
            skipped += 1
            continue
        vol = _extract_volume(arr)
        if vol is None:
            skipped += 1
            continue
        volumes.append(vol)
        if len(volumes) % 50 == 0:
            print(f"  [ingest] processed {len(volumes)} subjects "
                  f"(skipped {skipped})")

    if len(volumes) < 100:
        raise RuntimeError(
            f"Only {len(volumes)} valid subjects found; need >= 100."
        )

    print(f"  [ingest] total: {len(volumes)} valid subjects, "
          f"{skipped} skipped")
    return np.stack(volumes, axis=0)


# ===== Phase 2: Challenge curation helpers =====

def _stable_rng(seed: int, key: int) -> np.random.Generator:
    mixed = (int(seed) ^ ((int(key) * 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF)) & 0xFFFFFFFFFFFFFFFF
    return np.random.default_rng(mixed)


def _pick_missing_indices(rng: np.random.Generator) -> np.ndarray:
    weights = np.empty(SLICES_PER_VOLUME, dtype=np.float64)
    n_edge = len(EDGE_BANDS)
    n_mid = len(MIDDLE_BAND)
    w_edge = EDGE_SHARE / n_edge
    w_mid = (1.0 - EDGE_SHARE) / n_mid
    for i in range(SLICES_PER_VOLUME):
        weights[i] = w_edge if i in EDGE_BANDS else w_mid
    weights = weights / weights.sum()
    chosen = rng.choice(
        SLICES_PER_VOLUME, size=SLICES_MISSING, replace=False, p=weights
    )
    return np.sort(chosen)


def _missing_mask_string(missing: np.ndarray) -> str:
    bits = ["0"] * SLICES_PER_VOLUME
    for i in missing:
        bits[int(i)] = "1"
    return MASK_PREFIX + "".join(bits)


def _perturb_slice(slice_uint8: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    pil = Image.fromarray(slice_uint8, mode="L")
    if rng.random() < 0.5:
        pil = pil.transpose(Image.FLIP_LEFT_RIGHT)
    angle = float(rng.uniform(-ROT_DEG, ROT_DEG))
    pil = pil.rotate(angle, resample=Image.BICUBIC, fillcolor=0)
    s = np.asarray(pil, dtype=np.float32) / 255.0
    gamma = float(rng.uniform(GAMMA_LO, GAMMA_HI))
    s = np.power(np.clip(s, 0.0, 1.0), gamma)
    bright = float(rng.uniform(-0.10, 0.10))
    s = np.clip(s + bright, 0.0, 1.0)
    s = s + rng.normal(0.0, NOISE_SIGMA, size=s.shape).astype(np.float32)
    s = np.clip(s, 0.0, 1.0)
    s_uint8 = (s * 255.0 + 0.5).astype(np.uint8)
    buf = io.BytesIO()
    Image.fromarray(s_uint8, mode="L").save(buf, format="JPEG", quality=JPEG_Q)
    buf.seek(0)
    return np.asarray(Image.open(buf).convert("L"), dtype=np.uint8)


def _maybe_swap_ranks(
    true_rank: np.ndarray, rng: np.random.Generator
) -> np.ndarray:
    if rng.random() >= ADJACENT_SWAP_FRAC:
        return true_rank
    k = int(rng.integers(0, SLICES_PRESENTED - 1))
    pos_k = int(np.where(true_rank == k)[0][0])
    pos_k1 = int(np.where(true_rank == k + 1)[0][0])
    out = true_rank.copy()
    out[pos_k] = k + 1
    out[pos_k1] = k
    return out


def _maybe_flip_mask_bit(mask: str, rng: np.random.Generator) -> str:
    if rng.random() >= MASK_BITFLIP_FRAC:
        return mask
    j = int(rng.integers(0, SLICES_PER_VOLUME))
    body = list(mask[len(MASK_PREFIX):])
    body[j] = "1" if body[j] == "0" else "0"
    return MASK_PREFIX + "".join(body)


def _save_volume(
    out_dir: Path,
    volume_id: int,
    presented_slices: np.ndarray,
    rng_perturb: np.random.Generator,
) -> None:
    sub = out_dir / f"{volume_id:04d}"
    sub.mkdir(parents=True, exist_ok=True)
    for k in range(SLICES_PRESENTED):
        out = _perturb_slice(presented_slices[k], rng_perturb)
        Image.fromarray(out, mode="L").save(sub / f"s{k:02d}.png", format="PNG")


# ===== Main prepare =====

def prepare(raw: Path, public: Path, private: Path) -> None:
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    # Phase 1: ingest raw .nii.gz -> in-memory (N, 48, 192, 192) uint8
    slices = _ingest_nifti_dir(raw)

    n_total = int(slices.shape[0])
    n_test = int(round(n_total * TEST_FRACTION))
    n_train = n_total - n_test
    # n_test floor is 15 to stay consistent with the >= 100 subject minimum
    # enforced at ingest time: round(100 * 0.18) = 18 test volumes, which must
    # not trip this guard. (A 109-subject floor would be needed for a cutoff
    # of 20, so we lower the cutoff instead.)
    if n_train < 50 or n_test < 15:
        raise RuntimeError(
            f"Refusing to build splits with n_train={n_train}, n_test={n_test}."
        )

    rng_id = np.random.default_rng(SPLIT_SEED)
    permuted_volume_ids = rng_id.permutation(n_total)
    # Use a native Python int for the XOR; mixing a Python int with a
    # np.uint64 raises TypeError in modern NumPy.
    rng_split = np.random.default_rng(SPLIT_SEED ^ 0x1111_1111)
    order = rng_split.permutation(n_total)
    train_subject_idx = order[:n_train]

    train_dir = public / "train"
    test_dir = public / "test"
    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    train_rows: list[dict] = []
    test_rows: list[dict] = []
    answer_rows: list[dict] = []
    sample_sub_rows: list[dict] = []
    row_id = 0

    rng_label_noise = np.random.default_rng(LABEL_NOISE_SEED)

    train_set = set(train_subject_idx.tolist())
    for subj_idx in range(n_total):
        is_train = subj_idx in train_set
        volume_id = int(permuted_volume_ids[subj_idx])

        rng_drop = _stable_rng(DROP_SEED, volume_id)
        rng_perm = _stable_rng(PERM_SEED, volume_id)
        rng_perturb = _stable_rng(PERTURB_SEED, volume_id)

        missing = _pick_missing_indices(rng_drop)
        kept = np.array(
            [i for i in range(SLICES_PER_VOLUME) if i not in set(missing.tolist())],
            dtype=np.int64,
        )
        rank_of_kept = np.argsort(np.argsort(kept))

        present_perm = rng_perm.permutation(SLICES_PRESENTED)
        presented_orig_idx = kept[present_perm]
        presented_rank = rank_of_kept[present_perm]

        presented_slices = slices[subj_idx][presented_orig_idx]
        out_dir = train_dir if is_train else test_dir
        _save_volume(out_dir, volume_id, presented_slices, rng_perturb)

        clean_mask = _missing_mask_string(missing)
        rank_arr = presented_rank.astype(np.int64).copy()
        if is_train:
            rank_arr = _maybe_swap_ranks(rank_arr, rng_label_noise)
            train_mask = _maybe_flip_mask_bit(clean_mask, rng_label_noise)
        else:
            train_mask = clean_mask

        for k in range(SLICES_PRESENTED):
            common = {
                "row_id": row_id,
                "volume_id": volume_id,
                "presented_index": k,
            }
            if is_train:
                train_rows.append(
                    {
                        **common,
                        "true_rank": int(rank_arr[k]),
                        "true_missing_mask": train_mask,
                    }
                )
            else:
                test_rows.append(common)
                answer_rows.append(
                    {
                        **common,
                        "true_rank": int(presented_rank[k]),
                        "true_missing_mask": clean_mask,
                    }
                )
                sample_sub_rows.append(
                    {
                        **common,
                        "pred_rank": k,
                        "pred_missing_mask": MASK_PREFIX
                        + "1" * SLICES_MISSING
                        + "0" * (SLICES_PER_VOLUME - SLICES_MISSING),
                    }
                )
            row_id += 1

    pd.DataFrame(train_rows).to_csv(public / "train.csv", index=False)
    pd.DataFrame(test_rows).to_csv(public / "test.csv", index=False)
    pd.DataFrame(sample_sub_rows).to_csv(
        public / "sample_submission.csv", index=False
    )
    pd.DataFrame(answer_rows).to_csv(private / "answers.csv", index=False)
    print(f"  [prepare] done: {n_train} train volumes, {n_test} test volumes, "
          f"{row_id} total rows.")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=Path("raw_data"))
    ap.add_argument("--public", type=Path, default=Path("pub"))
    ap.add_argument("--private", type=Path, default=Path("priv"))
    args = ap.parse_args()
    prepare(args.raw.resolve(), args.public.resolve(), args.private.resolve())
    print("OK: prepare complete.")

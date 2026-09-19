"""
generate.py - SliceShuffle: Cranio-Caudal Sequence Reconstruction

Builds raw_data/ from the IXI brain MRI T1 archive (Information eXtraction
from Images, Imperial College London / Brain Development project).

DATA SOURCE (organiser-side; the agent never sees these names because
prepare.py emits anonymised numeric volume_id / presented_index columns
and re-encodes pixels):
  Primary: https://brain-development.org/ixi-dataset/
  Direct:  https://biomedic.doc.ic.ac.uk/brain-development/downloads/IXI/IXI-T1.tar
  Licence: CC BY-SA 3.0 (Information eXtraction from Images, IXI).
           Attribution + ShareAlike of derivatives. Suitable for an open
           challenge that itself ships under the same licence.

WHAT THIS SCRIPT DOES
---------------------
1. Reads every IXI-T1 NIfTI file (.nii.gz) found under --ixi-dir, or
   extracts them on-the-fly from --ixi-tar (the upstream IXI-T1.tar).
2. For each subject, reorients to canonical RAS axes, finds the axial
   z-range that actually contains brain tissue, and extracts the
   *central 32 axial slices* of that range (uniformly sampled if the
   brain spans more than 32 slices).
3. Each slice is z-percentile-normalised against the brain mask
   (1st-99th percentile in-brain voxels), resized to 256x256, and
   stored as uint8.
4. Subjects that produce fewer than 32 valid axial slices are skipped.
5. All surviving (subject, 32-slice window) tuples are stacked into a
   single numpy array of shape (N, 32, 256, 256) uint8 and saved as
   raw_data/volumes.npz alongside raw_data/manifest.csv.

NO challenge-specific transforms happen here -- no shuffling, no slice
dropping, no label generation, no train/test split. All of that lives
in prepare.py so the platform raw upload is a clean pre-processed
mirror of IXI-T1 (resized + intensity-normalised, nothing else).

USAGE
-----
    pip install nibabel numpy pillow scipy
    # Option A: you already extracted IXI-T1.tar somewhere
    python generate.py --ixi-dir D:/datasets/IXI-T1 --out raw_data
    # Option B: pass the tar directly (no full extraction, streamed)
    python generate.py --ixi-tar D:/datasets/IXI-T1.tar --out raw_data
    python zip_raw_for_upload.py

generate.py is deterministic: same input NIfTI files -> byte-identical
volumes.npz / manifest.csv.
"""

from __future__ import annotations

import argparse
import io
import sys
import tarfile
from pathlib import Path

import numpy as np


TARGET_HW = 256
SLICES_PER_VOLUME = 32
MIN_BRAIN_SLICES = 40  # subjects with fewer in-brain slices are skipped
BRAIN_THRESHOLD_FRAC = 0.05  # voxel > frac*max counts as brain-ish


def _load_nifti(data: bytes) -> np.ndarray:
    """Decode a NIfTI .nii.gz byte string into a float32 ndarray
    reoriented to canonical RAS so axis 2 is the cranio-caudal (z) axis
    increasing from caudal -> cranial."""
    try:
        import nibabel as nib  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "nibabel is required to read IXI NIfTI files. Install with:\n"
            "    pip install nibabel"
        ) from exc

    fobj = nib.FileHolder(fileobj=io.BytesIO(data))
    img = nib.Nifti1Image.from_file_map({"header": fobj, "image": fobj})
    img = nib.as_closest_canonical(img)
    arr = np.asarray(img.get_fdata(dtype=np.float32))
    if arr.ndim == 4:
        arr = arr[..., 0]
    if arr.ndim != 3:
        raise ValueError(f"Expected 3D NIfTI, got shape {arr.shape}")
    return arr


def _resize_2d(slice2d: np.ndarray, size: int) -> np.ndarray:
    """Bicubic resize a 2D float array to (size, size)."""
    from PIL import Image

    a = slice2d.astype(np.float32)
    img = Image.fromarray(a, mode="F")
    img = img.resize((size, size), resample=Image.BICUBIC)
    return np.asarray(img, dtype=np.float32)


def _extract_volume(arr: np.ndarray) -> np.ndarray | None:
    """Return a (32, 256, 256) uint8 array of central axial slices for
    one subject, or None if the volume is too thin / empty."""
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
    if span < SLICES_PER_VOLUME:
        return None

    if span >= SLICES_PER_VOLUME:
        idxs = np.linspace(z_lo, z_hi, SLICES_PER_VOLUME).round().astype(int)

    in_brain = arr[..., z_lo:z_hi + 1]
    flat = in_brain[in_brain > thresh]
    if flat.size == 0:
        return None
    p1, p99 = np.percentile(flat, [1.0, 99.0])
    if p99 <= p1:
        return None

    out = np.empty((SLICES_PER_VOLUME, TARGET_HW, TARGET_HW), dtype=np.uint8)
    for k, z in enumerate(idxs):
        # Axial slice; transpose so rows = anterior->posterior, cols = L->R.
        s = arr[:, :, int(z)].T
        s = _resize_2d(s, TARGET_HW)
        s = np.clip((s - p1) / (p99 - p1), 0.0, 1.0)
        out[k] = (s * 255.0 + 0.5).astype(np.uint8)
    return out


def _iter_nifti_from_dir(root: Path):
    for p in sorted(root.rglob("*.nii.gz")):
        yield p.stem.replace(".nii", ""), p.read_bytes()


def _iter_nifti_from_tar(tar_path: Path):
    with tarfile.open(tar_path, "r") as tf:
        names = sorted(
            m.name for m in tf.getmembers()
            if m.isfile() and m.name.endswith(".nii.gz")
        )
        for name in names:
            member = tf.getmember(name)
            f = tf.extractfile(member)
            if f is None:
                continue
            data = f.read()
            stem = Path(name).name.replace(".nii.gz", "")
            yield stem, data


def main() -> None:
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument(
        "--ixi-dir",
        type=Path,
        help="Directory containing extracted IXI-T1 *.nii.gz files.",
    )
    src.add_argument(
        "--ixi-tar",
        type=Path,
        help="Path to upstream IXI-T1.tar (streamed, no full extract).",
    )
    ap.add_argument("--out", type=Path, default=Path("raw_data"))
    ap.add_argument(
        "--max-subjects",
        type=int,
        default=600,
        help="Hard cap; defaults to 600 to keep the upload <2 GB.",
    )
    args = ap.parse_args()

    out: Path = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    if args.ixi_dir is not None:
        if not args.ixi_dir.is_dir():
            print(f"ERROR: --ixi-dir not found: {args.ixi_dir}", file=sys.stderr)
            sys.exit(1)
        iterator = _iter_nifti_from_dir(args.ixi_dir.resolve())
    else:
        if not args.ixi_tar.is_file():
            print(f"ERROR: --ixi-tar not found: {args.ixi_tar}", file=sys.stderr)
            sys.exit(1)
        iterator = _iter_nifti_from_tar(args.ixi_tar.resolve())

    subject_ids: list[str] = []
    volumes: list[np.ndarray] = []
    skipped = 0

    for stem, data in iterator:
        if len(subject_ids) >= args.max_subjects:
            break
        try:
            arr = _load_nifti(data)
        except Exception as exc:
            print(f"  skip {stem}: load error {exc}", file=sys.stderr)
            skipped += 1
            continue
        vol = _extract_volume(arr)
        if vol is None:
            skipped += 1
            continue
        subject_ids.append(stem)
        volumes.append(vol)
        if len(subject_ids) % 25 == 0:
            print(f"  processed {len(subject_ids)} subjects (skipped {skipped})")

    if len(subject_ids) < 100:
        print(
            f"ERROR: only {len(subject_ids)} valid subjects; need >=100 to "
            f"build a meaningful train/test split. Check --ixi-dir / "
            f"--ixi-tar.",
            file=sys.stderr,
        )
        sys.exit(1)

    slices = np.stack(volumes, axis=0)
    np.savez_compressed(
        out / "volumes.npz",
        slices=slices,
        subject_ids=np.array(subject_ids, dtype=np.str_),
    )

    manifest_lines = ["subject_id,n_axial_slices,height,width\n"]
    for sid in subject_ids:
        manifest_lines.append(f"{sid},{SLICES_PER_VOLUME},{TARGET_HW},{TARGET_HW}\n")
    (out / "manifest.csv").write_text("".join(manifest_lines), encoding="utf-8")

    size_gb = (out / "volumes.npz").stat().st_size / 1e9
    print(
        f"OK: wrote {out / 'volumes.npz'} "
        f"({slices.shape}, {size_gb:.2f} GB) "
        f"and {out / 'manifest.csv'} "
        f"({len(subject_ids)} subjects, skipped {skipped})."
    )


if __name__ == "__main__":
    main()

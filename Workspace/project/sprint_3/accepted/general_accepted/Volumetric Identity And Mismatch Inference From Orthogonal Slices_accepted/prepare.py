"""
prepare.py - Volumetric Identity And Mismatch Inference From Orthogonal Slices

Pipeline (deterministic; ALL processing happens here):
  1. Discover six MedMNIST3D `.npz` archives in `raw/` (auto-extract any
     enclosing zip first).
  2. For each volume, extract the AXIAL (z=14), SAGITTAL (x=14), and
     CORONAL (y=14) mid-planes as 28×28 uint8 grayscale slices.
     Compute a deterministic `vol_radius_norm` from the foreground 3D
     bounding box of the volume (Otsu-thresholded), normalised to [0, 1].
  3. Apply per-row seeded perturbations (gamma + brightness + Gaussian
     noise) to each of the three slices independently — irreversible
     against the upstream npz pixel hash.
  4. Anonymise the per-corpus class label into a global label space
     0..MAX_CLASS-1 using a private per-corpus permutation seed.
  5. Anonymise the corpus identifier into a 0..5 integer using a global
     private permutation; the public corpus_id values do NOT correspond
     to the alphabetical or upstream order.
  6. For TEST_INTRUDER_FRAC of TEST rows, swap one of the three slices
     with the matching plane from a different volume. The donor is a
     HARD NEGATIVE: same corpus, same (true) class label, AND extent
     (radius) matched within RADIUS_MATCH_TOL whenever such a donor exists
     (fallbacks: same-class, then same-corpus). Matching corpus+class+extent
     removes the gross appearance and "implied-size" shortcuts, so the
     intruder is only exposable via finer cross-view (shared-line)
     inconsistency. Mark mismatched_triplet=1 and mismatched_axis = the
     swapped axis.
  7. Inject CLASS_NOISE_FRAC random label flips on TRAIN rows
     (within-corpus only — the irreducible-error floor pattern).

OUTPUT LAYOUT
-------------
    public/train/<id>_axial.png        28×28 grayscale PNG
    public/train/<id>_sagittal.png
    public/train/<id>_coronal.png
    public/test/<id>_axial.png
    public/test/<id>_sagittal.png
    public/test/<id>_coronal.png
    public/train.csv     id, axial_path, sagittal_path, coronal_path,
                         true_corpus_id, true_class_label,
                         true_vol_radius, true_mismatched_triplet,
                         true_mismatched_axis
    public/test.csv      id, axial_path, sagittal_path, coronal_path
    public/sample_submission.csv  id, pred_corpus_id, pred_class_label,
                                  pred_vol_radius, pred_mismatched_triplet,
                                  pred_mismatched_axis
    private/answers.csv  id, true_corpus_id, true_class_label,
                         true_vol_radius, true_mismatched_triplet,
                         true_mismatched_axis

The `prepare(raw, public, private)` signature is the platform standard.
"""

from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

# -------- constants --------

# Six upstream archive stems we expect to find under raw/.
NPZ_STEMS = (
    "organmnist3d",
    "nodulemnist3d",
    "adrenalmnist3d",
    "fracturemnist3d",
    "vesselmnist3d",
    "synapsemnist3d",
)

# Per-corpus class cardinality (informational; used to range-check labels).
CORPUS_NCLASSES = {
    "organmnist3d":   11,
    "nodulemnist3d":   2,
    "adrenalmnist3d":  2,
    "fracturemnist3d": 3,
    "vesselmnist3d":   2,
    "synapsemnist3d":  2,
}

# Global anonymised class space (max over the 6 corpora).
GLOBAL_NCLASSES = 11
GLOBAL_NCORPORA = 6
AXIS_NAMES = ("NONE", "AXIAL", "SAGITTAL", "CORONAL")

VOL_HW = 28
SLICE_HW = 28

# Test-time intruder rate. Kept high so "always NONE" baselines are weak and
# the intruder heads carry real weight in the score.
TEST_INTRUDER_FRAC = 0.40
# Train-time intruder rate (so the agent can learn detection from labelled
# examples).
TRAIN_INTRUDER_FRAC = 0.20

# Hard-negative donor tolerance: an intruder slice is preferentially taken from
# a same-corpus, same-class volume whose normalised extent (radius) is within
# this band of the host. Matching the extent removes the gross "the views imply
# different sizes" shortcut, so the intruder is only exposable via finer
# cross-view (shared-line) inconsistency. Small enough to stay challenging,
# large enough to almost always find a donor.
RADIUS_MATCH_TOL = 0.08

# Within-corpus class label noise on the TRAIN split only.
CLASS_NOISE_FRAC = 0.10

# Per-slice perturbation parameters. Seeded per row so byte-hashing
# upstream npz files cannot recover the answer key.
GAMMA_LO, GAMMA_HI = 0.85, 1.15
NOISE_SIGMA = 4.0 / 255.0
BRIGHT_LO, BRIGHT_HI = -0.04, 0.04

# Foreground threshold for radius computation. We use a percentile so
# the volume is treated as "foreground" wherever the intensity exceeds
# the corpus-typical background floor.
RADIUS_FG_PCTL = 60.0
RADIUS_NORM_DENOM = float(np.sqrt(3.0) * VOL_HW)

# Test fraction (per corpus). We use the upstream test split as our
# challenge test pool so the patient-disjoint property of MedMNIST
# (where it exists) carries through.
TEST_FROM_UPSTREAM_TEST = True

# Seeds (private; not shipped to participants).
CORPUS_PERM_SEED = 0x71A3B5C7
CLASS_PERM_SEED  = 0x82B4C6D8
SLICE_PERTURB_SEED = 0x93C5D7E9
INTRUDER_SEED = 0xA4D6E8FA
CLASS_NOISE_SEED = 0xB5E7F90B
ID_SEED = 0xC6F80A1C


# -------- helpers --------

def _extract_zips(raw: Path) -> None:
    for zf in sorted(raw.glob("*.zip")):
        with zipfile.ZipFile(zf, "r") as z:
            members = z.namelist()
        if not members:
            continue
        sentinel = raw / Path(members[0]).parts[0]
        if sentinel.exists():
            continue
        print(f"  [extract] {zf.name}")
        with zipfile.ZipFile(zf, "r") as z:
            z.extractall(raw)


def _find_npz(raw: Path, stem: str) -> Path:
    candidates = list(raw.rglob(f"{stem}.npz"))
    if not candidates:
        raise FileNotFoundError(
            f"Expected {stem}.npz under {raw}. Make sure all six MedMNIST3D "
            f"npz archives are present at the dataset root."
        )
    return sorted(candidates)[0]


def _stable_rng(*seeds: int) -> np.random.Generator:
    h = 0xC4F1B2A3D9E876F1
    for s in seeds:
        h ^= int(s) & 0xFFFFFFFFFFFFFFFF
        h = (h * 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
    return np.random.default_rng(h)


def _vol_radius(vol: np.ndarray) -> float:
    """Bounding-box diagonal of foreground voxels, normalised to [0, 1]."""
    fg_thresh = float(np.percentile(vol, RADIUS_FG_PCTL))
    fg = vol > fg_thresh
    if not fg.any():
        return 0.0
    zs, ys, xs = np.where(fg)
    dz = float(zs.max() - zs.min())
    dy = float(ys.max() - ys.min())
    dx = float(xs.max() - xs.min())
    diag = float(np.sqrt(dz * dz + dy * dy + dx * dx))
    return float(np.clip(diag / RADIUS_NORM_DENOM, 0.0, 1.0))


def _extract_planes(vol: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (axial, sagittal, coronal) 28x28 uint8 mid-planes."""
    z = VOL_HW // 2
    axial = vol[z, :, :]
    sagittal = vol[:, :, z]
    coronal = vol[:, z, :]
    return axial.astype(np.uint8), sagittal.astype(np.uint8), coronal.astype(np.uint8)


def _perturb(slice_2d: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    s = slice_2d.astype(np.float32) / 255.0
    gamma = float(rng.uniform(GAMMA_LO, GAMMA_HI))
    s = np.clip(s, 1e-6, 1.0) ** gamma
    bright = float(rng.uniform(BRIGHT_LO, BRIGHT_HI))
    s = np.clip(s + bright, 0.0, 1.0)
    s = s + rng.normal(0.0, NOISE_SIGMA, size=s.shape).astype(np.float32)
    s = np.clip(s, 0.0, 1.0)
    return (s * 255.0 + 0.5).astype(np.uint8)


def _save_png(arr: np.ndarray, path: Path) -> None:
    Image.fromarray(arr, mode="L").save(path, format="PNG", optimize=True)


def _build_corpus_perm(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.permutation(GLOBAL_NCORPORA).astype(np.int64)


def _build_class_perm(corpus_idx_real: int, n_classes: int, seed: int) -> np.ndarray:
    """Return a length-n_classes permutation mapping upstream label j ->
    anonymised label perm[j] in [0, n_classes-1]."""
    rng = np.random.default_rng(seed ^ ((corpus_idx_real + 1) * 0x9E3779B97F4A7C15))
    return rng.permutation(n_classes).astype(np.int64)


# -------- main pipeline --------

def prepare(raw: Path, public: Path, private: Path) -> None:
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    _extract_zips(raw)

    train_dir = public / "train"
    test_dir = public / "test"
    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    corpus_perm = _build_corpus_perm(CORPUS_PERM_SEED)
    print(f"  [permute] corpus_perm = {corpus_perm.tolist()} (private)")

    train_records: list[dict] = []
    test_records: list[dict] = []
    train_volumes_per_corpus: dict[int, list[np.ndarray]] = {}
    test_volumes_per_corpus: dict[int, list[np.ndarray]] = {}

    rid = 0
    for corpus_real_idx, stem in enumerate(NPZ_STEMS):
        npz_path = _find_npz(raw, stem)
        print(f"  [load] {stem} <- {npz_path.name}")
        n_classes = CORPUS_NCLASSES[stem]
        class_perm = _build_class_perm(corpus_real_idx, n_classes, CLASS_PERM_SEED)
        anon_corpus = int(corpus_perm[corpus_real_idx])

        with np.load(npz_path) as z:
            tr_imgs = z["train_images"]
            tr_lbls = z["train_labels"].astype(np.int64).reshape(-1)
            va_imgs = z["val_images"]
            va_lbls = z["val_labels"].astype(np.int64).reshape(-1)
            te_imgs = z["test_images"]
            te_lbls = z["test_labels"].astype(np.int64).reshape(-1)

        # Train pool = upstream train + val
        train_imgs = np.concatenate([tr_imgs, va_imgs], axis=0)
        train_lbls = np.concatenate([tr_lbls, va_lbls], axis=0)
        test_imgs = te_imgs
        test_lbls = te_lbls
        print(f"  [load]   train pool {len(train_imgs)} vols, test pool {len(test_imgs)} vols, classes={n_classes}")

        train_volumes_per_corpus[anon_corpus] = []
        test_volumes_per_corpus[anon_corpus] = []

        for split_name, imgs, lbls, records, out_dir in [
            ("train", train_imgs, train_lbls, train_records, train_dir),
            ("test",  test_imgs,  test_lbls,  test_records,  test_dir),
        ]:
            for k in range(len(imgs)):
                vol = imgs[k]
                lbl_real = int(lbls[k])
                lbl_anon = int(class_perm[lbl_real])
                radius = _vol_radius(vol)
                ax, sg, co = _extract_planes(vol)

                row = {
                    "id": rid,
                    "split": split_name,
                    "anon_corpus": anon_corpus,
                    "anon_class": lbl_anon,
                    "radius": float(radius),
                    "axial": ax,
                    "sagittal": sg,
                    "coronal": co,
                }
                if split_name == "train":
                    train_volumes_per_corpus[anon_corpus].append(row)
                else:
                    test_volumes_per_corpus[anon_corpus].append(row)
                records.append(row)
                rid += 1

    print(f"  [collect] {len(train_records)} train rows, {len(test_records)} test rows total")

    rng_intruder = np.random.default_rng(INTRUDER_SEED)
    rng_class_noise = np.random.default_rng(CLASS_NOISE_SEED)

    # Apply intruder swaps + per-slice perturbations.
    final_rows: list[dict] = []
    final_answers: list[dict] = []

    for split_name, records, vol_pool, intr_frac, out_dir in [
        ("train", train_records, train_volumes_per_corpus, TRAIN_INTRUDER_FRAC, train_dir),
        ("test",  test_records,  test_volumes_per_corpus,  TEST_INTRUDER_FRAC,  test_dir),
    ]:
        rng_split_intr = np.random.default_rng(INTRUDER_SEED ^ (0x12345 if split_name == "train" else 0x98765))

        # Index same-split donor rows by (corpus, class) for HARD-NEGATIVE
        # intruder swaps. A swapped slice from a same-corpus, same-class volume
        # is plausible per-view and is only detectable via cross-view geometric
        # inconsistency, which is precisely the skill this challenge targets.
        class_donors: dict[tuple[int, int], list[dict]] = {}
        for c_id, rows_c in vol_pool.items():
            for rr in rows_c:
                class_donors.setdefault((c_id, rr["anon_class"]), []).append(rr)

        for r in records:
            rid_ = r["id"]
            anon_corpus = r["anon_corpus"]
            anon_class = r["anon_class"]
            radius = r["radius"]
            ax, sg, co = r["axial"], r["sagittal"], r["coronal"]

            mismatched = 0
            mismatched_axis = "NONE"
            if rng_split_intr.random() < intr_frac and len(vol_pool[anon_corpus]) > 1:
                # Hard negative: prefer a same-corpus, same-class donor whose
                # volumetric extent matches the host (within RADIUS_MATCH_TOL),
                # so the swap is plausible both per-view AND in implied size.
                # Fall back to any same-class, then any same-corpus donor.
                same_class = class_donors.get((anon_corpus, anon_class), [])
                extent_matched = [
                    d for d in same_class
                    if d["id"] != rid_ and abs(d["radius"] - radius) <= RADIUS_MATCH_TOL
                ]
                if extent_matched:
                    donor_pool = extent_matched
                elif len(same_class) > 1:
                    donor_pool = same_class
                else:
                    donor_pool = vol_pool[anon_corpus]
                donor_idx = int(rng_split_intr.integers(0, len(donor_pool)))
                donor = donor_pool[donor_idx]
                if donor["id"] == rid_:
                    donor_idx = (donor_idx + 1) % len(donor_pool)
                    donor = donor_pool[donor_idx]
                axis_choice = int(rng_split_intr.integers(1, 4))  # 1..3 -> AXIAL/SAGITTAL/CORONAL
                mismatched_axis = AXIS_NAMES[axis_choice]
                if axis_choice == 1:
                    ax = donor["axial"]
                elif axis_choice == 2:
                    sg = donor["sagittal"]
                else:
                    co = donor["coronal"]
                mismatched = 1

            # Per-slice seeded perturbations.
            rng_pert = _stable_rng(SLICE_PERTURB_SEED, rid_)
            ax_p = _perturb(ax, rng_pert)
            sg_p = _perturb(sg, rng_pert)
            co_p = _perturb(co, rng_pert)

            ax_path = out_dir / f"{rid_:06d}_axial.png"
            sg_path = out_dir / f"{rid_:06d}_sagittal.png"
            co_path = out_dir / f"{rid_:06d}_coronal.png"
            _save_png(ax_p, ax_path)
            _save_png(sg_p, sg_path)
            _save_png(co_p, co_path)

            row = {
                "id": rid_,
                "axial_path": f"{split_name}/{rid_:06d}_axial.png",
                "sagittal_path": f"{split_name}/{rid_:06d}_sagittal.png",
                "coronal_path": f"{split_name}/{rid_:06d}_coronal.png",
            }

            if split_name == "train":
                # Apply within-corpus class label noise on TRAIN only.
                noisy_class = anon_class
                if rng_class_noise.random() < CLASS_NOISE_FRAC:
                    n_classes_corpus = None
                    # Find corpus original size by mapping back
                    for stem, n in CORPUS_NCLASSES.items():
                        idx = NPZ_STEMS.index(stem)
                        if int(corpus_perm[idx]) == anon_corpus:
                            n_classes_corpus = n
                            break
                    if n_classes_corpus and n_classes_corpus > 1:
                        flip_pool = [c for c in range(n_classes_corpus) if c != anon_class]
                        # Note: anonymised classes are in [0, n-1] for that corpus,
                        # because the perm is over n classes.
                        noisy_class = int(rng_class_noise.choice(flip_pool))
                row["true_corpus_id"] = int(anon_corpus)
                row["true_class_label"] = int(noisy_class)
                row["true_vol_radius"] = float(radius)
                row["true_mismatched_triplet"] = int(mismatched)
                row["true_mismatched_axis"] = str(mismatched_axis)
                final_rows.append(row)
            else:
                final_rows.append(row)
                final_answers.append({
                    "id": rid_,
                    "true_corpus_id": int(anon_corpus),
                    "true_class_label": int(anon_class),
                    "true_vol_radius": float(radius),
                    "true_mismatched_triplet": int(mismatched),
                    "true_mismatched_axis": str(mismatched_axis),
                })

    # Split the rows back into train/test by id ranges.
    train_ids = {r["id"] for r in train_records}
    train_csv_rows = [r for r in final_rows if r["id"] in train_ids]
    test_csv_rows = [r for r in final_rows if r["id"] not in train_ids]

    train_cols = [
        "id", "axial_path", "sagittal_path", "coronal_path",
        "true_corpus_id", "true_class_label", "true_vol_radius",
        "true_mismatched_triplet", "true_mismatched_axis",
    ]
    test_cols = ["id", "axial_path", "sagittal_path", "coronal_path"]
    ans_cols = [
        "id", "true_corpus_id", "true_class_label", "true_vol_radius",
        "true_mismatched_triplet", "true_mismatched_axis",
    ]

    pd.DataFrame(train_csv_rows)[train_cols].to_csv(public / "train.csv", index=False)
    pd.DataFrame(test_csv_rows)[test_cols].to_csv(public / "test.csv", index=False)

    sample_rows = []
    for r in test_csv_rows:
        sample_rows.append({
            "id": r["id"],
            "pred_corpus_id": 0,
            "pred_class_label": 0,
            "pred_vol_radius": 0.5,
            "pred_mismatched_triplet": 0,
            "pred_mismatched_axis": "NONE",
        })
    sample_cols = [
        "id", "pred_corpus_id", "pred_class_label", "pred_vol_radius",
        "pred_mismatched_triplet", "pred_mismatched_axis",
    ]
    pd.DataFrame(sample_rows)[sample_cols].to_csv(public / "sample_submission.csv", index=False)

    pd.DataFrame(final_answers)[ans_cols].to_csv(private / "answers.csv", index=False)

    print(f"  [done] train={len(train_csv_rows)} rows, test={len(test_csv_rows)} rows.")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=Path("raw_data"))
    ap.add_argument("--public", type=Path, default=Path("pub"))
    ap.add_argument("--private", type=Path, default=Path("priv"))
    args = ap.parse_args()
    prepare(args.raw.resolve(), args.public.resolve(), args.private.resolve())
    print("OK: prepare complete.")

# Challenge creation form — fill-in

**Platform status:** **Draft** — *SliceShuffle: Cranio-Caudal Sequence Reconstruction*.

Tie this challenge to the **accepted dataset**: SliceShuffle Axial Brain MRI Volume Corpus.

---

## 1) Difficulty

**Select:** **Hard**

---

## 2) Challenge Title

```
SliceShuffle: Cranio-Caudal Sequence Reconstruction
```

---

## 3) Problem Description

# SliceShuffle: Cranio-Caudal Sequence Reconstruction

## Overview

This is a **Computer Vision / Medical Imaging** challenge that hides the temporal-axis structure inside a 3D volume and asks the solver to reconstruct it from a shuffled, partially-observed projection. Each test "volume" is **one subject's axial T1-weighted MRI brain scan trimmed to a contiguous window of 48 axial slices** along the cranio-caudal axis (rank 0 = most caudal slice in the window, rank 47 = most cranial). Before the solver sees a volume, **16 axial positions are dropped** and the remaining **32 slices are shuffled into a random presentation order** — index 0 in the shuffled stream is not necessarily caudal, and consecutive `s00.png`, `s01.png`, … files are not anatomically adjacent. The solver gets only the 32 PNGs and must output two structured predictions per volume:

1. **`pred_rank`** — for every visible slice, an integer in `{0, …, 31}` giving its predicted cranio-caudal rank among the 32 visible slices (0 = most caudal of the 32 visible, 31 = most cranial of the 32 visible). Within one volume the 32 `pred_rank` values must form a permutation of `{0, …, 31}`; the grader does not enforce this, but ties / out-of-range values directly hurt the Kendall-τ term.
2. **`pred_missing_mask`** — a 49-character string `"M" + 48 chars in {"0", "1"}`. The literal `"M"` prefix is a non-digit guard that prevents CSV round-trips from coercing the column to a numeric dtype (without the prefix, pandas auto-infers a 48-digit numeric column to `float64` and round-trips lose the bits). Bit `j` of the 48-character body is `1` if and only if the solver believes original axial position `j` of the underlying 48-slice window was one of the 16 dropped positions. The mask must be **identical on every row of the same `volume_id`**; the grader uses the first row's value (rows sorted by `presented_index`), so disagreement among rows just discards information.

Two independent failure modes are penalised: getting the cranio-caudal **ordering** of the visible slices wrong, and getting the **localisation of the gaps** wrong. The two are not redundant — a model that nails the order can still totally fail to localise the gaps, because gap localisation requires reasoning about *what is anatomically missing between two visible slices*, which is a different operation from ranking.

A small fraction of training labels carry irreducible noise on both the rank labels and the missing-position mask, capping the achievable training accuracy below 1.0. Test labels are clean.

The 48-slice axial window per subject is sampled from inside each subject's brain z-range, but the **exact start and end z-coordinates and the overall span of the window are different per subject** (each subject's brain has a different overall axial extent). The window is also **kept narrower than the full brain z-range** so adjacent visible slices have similar anatomy and pairwise ranking is genuinely hard. The solver therefore cannot assume that `rank 0` corresponds to a constant anatomical landmark — only that within one volume, rank increases monotonically from caudal to cranial. The 16 missing positions follow a non-uniform distribution that is biased away from the centre of the 48-slice window; solvers that assume uniformly-random gaps will systematically mis-localise them.

Each visible slice has been processed by an irreversible per-slice pixel-domain transform: an **independent 50%-probability left-right (horizontal) mirror flip**, a small in-plane rotation, gamma jitter, a brightness shift, additive Gaussian noise, and a JPEG round-trip, then PNG save. Because the horizontal flip is decided **per slice**, the left-right orientation is *not* consistent down a volume — adjacent slices may be mirrored relative to one another, so left-right anatomical continuity is not a reliable ordering cue and models should be designed to be invariant to (or to reason jointly despite) per-slice mirroring. All transform parameters are private and applied independently per slice, so a "is slice A darker / sharper than slice B" shortcut is not reliable. The same family of transforms is applied identically to train and test so the pixel-statistic distributions match across splits, and so that pixel-level matching against external collections is not feasible.

## Evaluation

For every test `volume_id`, the grader computes:

```
rank_score(volume) = max(0, kendall_tau_b(pred_rank, true_rank)) ** 2
mask_score(volume) = macro_f1(pred_missing_mask, true_missing_mask) ** 2
S(volume)          = 0.60 * rank_score(volume) + 0.40 * mask_score(volume)

Final              = mean over test volumes of S(volume), clipped to [0, 1]
```

Both per-volume terms are **squared** so that the score compresses aggressively at the high end: a Kendall τ of 0.9 contributes 0.81 to the rank term (instead of 0.9), and a macro-F1 of 0.7 contributes 0.49 to the mask term. The squaring widens the relative gap between an "almost there" agent and a perfect submission, leaving more room for genuine human-vs-agent skill differentiation.

* `kendall_tau_b` is the standard tau-b coefficient over the 32 `(presented_index, pred_rank)` tuples of one volume, which lies in `[-1, +1]`. `max(0, τ) ** 2` puts it in `[0, 1]` for any positive correlation, with anti-correlation collapsing to 0; a uniformly random permutation has `E[τ] = 0` and therefore expected `rank_score = 0` — random guessing earns no free leaderboard floor.
* `macro_f1` averages the F1 of class `"0"` and class `"1"` over the 48 binary cells of `pred_missing_mask` vs `true_missing_mask`, and is then squared. The grader takes the **first row's** `pred_missing_mask` per `volume_id` (rows sorted by `presented_index`); per-row variation within a volume is silently discarded.

**Higher is better.** Minimum: 0.0, Maximum: 1.0.

A row that is missing entirely from the submission contributes `pred_rank = 0` and `pred_missing_mask = "M" + "0" * 48` (the 49-character all-zeros mask) for that `(volume_id, presented_index)` pair, so missing rows pull the volume score down rather than zeroing the whole submission. The grader returns `0.0` if `submission` lacks any of the required columns, contains duplicate `(volume_id, presented_index)` pairs, or otherwise raises an exception during parsing — robust submissions must obey the schema.

`pred_rank` values out of range are clipped to `[0, 31]`; `pred_missing_mask` values are sanitised to a 48-character `"0"`/`"1"` string (non-binary chars are stripped, over-long strings are truncated, short ones are right-padded with `"0"`). Submitting illegible / corrupt strings therefore degrades the score smoothly rather than zeroing the whole submission.

## Dataset

* `public/train/<volume_id>/` — one folder per training volume, each containing 32 PNG files `s00.png` … `s31.png` of size 192×192 grayscale.
* `public/test/<volume_id>/` — one folder per test volume, each containing 32 PNG files `s00.png` … `s31.png` of size 192×192 grayscale.
* `public/train.csv` — one row per `(volume_id, presented_index)` pair on training volumes, with the cranio-caudal rank label and the 48-bit missing-position mask. Both labels carry the seeded train-side noise described in the **Overview**.
* `public/test.csv` — one row per `(volume_id, presented_index)` pair on test volumes, with no labels.
* `public/sample_submission.csv` — one row per `(volume_id, presented_index)` pair on test volumes, in the exact submission format. The shipped values are a deliberately weak placeholder (`pred_rank = presented_index` and a constant `pred_missing_mask`); participants must overwrite both columns to score meaningfully.

Volume counts are seed-dependent and printed at the end of `prepare.py` (typical: ~480 train volumes and ~100 test volumes; one volume = 32 PNGs + 32 CSV rows).

### File overview

Files shipped to participants: `public/train/<volume_id>/sNN.png` (192×192 grayscale axial slices, 32 per training volume), `public/test/<volume_id>/sNN.png` (192×192 grayscale axial slices, 32 per test volume), `public/train.csv` (labels for training volumes), `public/test.csv` (ids only, no labels), and `public/sample_submission.csv` (submission template with the full 5-column shape).

| Item                        | Description                                  |
|-----------------------------|----------------------------------------------|
| `public/train/<vid>/sNN.png`| 192×192 grayscale axial slice, 32 per vid    |
| `public/test/<vid>/sNN.png` | 192×192 grayscale axial slice, 32 per vid    |
| `public/train.csv`          | Labels for training volumes                  |
| `public/test.csv`           | Test ids only, no labels                     |
| `public/sample_submission.csv` | Submission template, full shape           |

### Feature Details

The columns differ between the training CSV, the test CSV, and the submission CSV. They are listed separately so there is no ambiguity about which columns belong to which file.

**Training data columns (`public/train.csv`) — 5 columns:**

Columns (in order): `row_id` (int, unique row identifier), `volume_id` (int, volume identifier with 4-digit zero pad), `presented_index` (int, slice index in the stream, 0–31), `true_rank` (int, cranio-caudal rank of the slice, 0–31), `true_missing_mask` (string, `"M"` + 48 `"0"`/`"1"` chars = 49 chars total).

| Column              | Type   | Description                            |
|---------------------|--------|----------------------------------------|
| `row_id`            | int    | Unique row identifier                  |
| `volume_id`         | int    | Volume identifier, 4-digit zero pad    |
| `presented_index`   | int    | Slice index in stream, 0–31            |
| `true_rank`         | int    | Cranio-caudal rank of slice, 0–31      |
| `true_missing_mask` | string | "M" + 48-char "0"/"1", 49 chars total  |

**Test metadata columns (`public/test.csv`) — 3 columns:**

Columns (in order): `row_id` (int, unique row identifier), `volume_id` (int, matches a folder under `public/test/`), `presented_index` (int, slice index in the stream, 0–31). No label columns are present.

| Column            | Type | Description                          |
|-------------------|------|--------------------------------------|
| `row_id`          | int  | Unique row identifier                |
| `volume_id`       | int  | Matches a folder under `public/test/`|
| `presented_index` | int  | Slice index in stream, 0–31          |

**Submission columns (`public/sample_submission.csv` and your final submission) — 5 columns:**

Columns (in order): `row_id` (int, same set as `public/test.csv`), `volume_id` (int, from `public/test.csv`), `presented_index` (int, from `public/test.csv`, 0–31), `pred_rank` (int, 0–31, predicted rank for this slice), `pred_missing_mask` (string, `"M"` + 48 `"0"`/`"1"` chars, identical across all rows of a volume).

| Column              | Type   | Constraint                              |
|---------------------|--------|-----------------------------------------|
| `row_id`            | int    | Same set as `public/test.csv`           |
| `volume_id`         | int    | From `public/test.csv`                  |
| `presented_index`   | int    | From `public/test.csv`, 0–31            |
| `pred_rank`         | int    | 0–31, predicted rank for this slice     |
| `pred_missing_mask` | string | "M" + 48-char "0"/"1", same per vid     |

## Submission

Submit a CSV file with a header row and **exactly one row per `(volume_id, presented_index)` pair in `test.csv`**. The header must contain these **5 columns in this order**: `row_id`, `volume_id`, `presented_index`, `pred_rank`, `pred_missing_mask`.

| Column              | Type   | Description                              |
|---------------------|--------|------------------------------------------|
| `row_id`            | int    | Unique identifier from `test.csv`        |
| `volume_id`         | int    | Volume identifier from `test.csv`        |
| `presented_index`   | int    | Slice index 0–31, from `test.csv`        |
| `pred_rank`         | int    | Predicted cranio-caudal rank in 0–31     |
| `pred_missing_mask` | string | `"M"` + 48 `"0"`/`"1"` chars, per vid    |

**Requirements:**

* Header row plus exactly one row per `(volume_id, presented_index)` pair appearing in `test.csv` — `row_id` must equal exactly the set in `test.csv`.
* `pred_rank` must be an integer in `[0, 31]`. Out-of-range values are clipped, but ideally each volume's 32 `pred_rank` values form a permutation of `{0, …, 31}` because Kendall-τ rewards correctly-ordered pairs.
* `pred_missing_mask` must be a 49-character string `"M" + 48 chars in {"0", "1"}`. The literal `"M"` prefix is required so that pandas does not coerce the column to a numeric dtype on CSV read (a 48-digit numeric column would round-trip through `float64` and lose information). The grader is permissive: any non-binary characters are stripped, and the result is right-padded or truncated to 48 binary entries — but a correctly-formed `"M..."` string of length 49 always scores best.
* `pred_missing_mask` should be the **same** on every row sharing the same `volume_id`. The grader takes the first row's value (rows sorted by `presented_index`); per-row variation within a volume is silently discarded.
* Missing rows are filled in with `pred_rank = 0` and `pred_missing_mask = "M" + "0" * 48`, which lowers the score for the affected volumes rather than zeroing the whole submission.
* The grader returns `0.0` only if any of the five required columns are missing from the submission.

**Example of a correctly formatted submission file (illustrative only):**

The three rows below come from one volume `volume_id = 0` with three of its 32 visible slices. The full submission has 32 rows for this `volume_id` (and 32 rows per other test `volume_id`). The `pred_missing_mask` is the same 49-character `"M..."` string on every row of the same `volume_id`.

```
row_id,volume_id,presented_index,pred_rank,pred_missing_mask
0,0,0,5,M111110000100001000010000100001000010000100001111
1,0,1,17,M111110000100001000010000100001000010000100001111
2,0,2,11,M111110000100001000010000100001000010000100001111
```

## What Not To Do

Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score:

* **Reverse-image-search or pixel-hash any visible PNG** against any public 3D MRI archive in order to recover the original subject identity, original axial index, or DICOM header. The 32 visible slices and the 48-bit mask must be recovered from the provided PNGs alone.
* **Hosted / closed-source APIs** at any stage of training or inference (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.), including any distillation / pseudo-labelling from such teachers. Only open-weights models and self-trained pipelines are permitted.
* **Externally pretrained 3D-MRI sequence models** whose training set overlaps with the upstream collection these slices were drawn from. Generic ImageNet / DINOv2 / CLIP / natural-image backbones are fine; fine-tuned brain-MRI sequencers that already encode the target axial coordinate are not.
* **Filename / order side-channels.** Do not assume that the lexicographic order of `s00.png` … `s31.png` matches any anatomical order, and do not exploit file-system metadata, file mtimes, or any signal outside the PNG pixels and the CSVs.
* **Probability / format hacks that game the grader.** Submitting non-permutation `pred_rank` values to deliberately exploit Kendall-τ tie-handling, padding `pred_missing_mask` with non-binary characters, duplicate `(volume_id, presented_index)` pairs, or per-row-varying masks for the same `volume_id` to try to game the "first row wins" rule.
* **Grader / platform exploitation.** Hard-coded answer dictionaries, filesystem probes for `private/answers.csv`, attempts to read hidden splits, or any channel that is not `public/train/`, `public/train.csv`, `public/test/`, and `public/test.csv`.
* **Ensembles mixing allowed and prohibited components.** An ensemble is allowed only if every component is itself trained (or used zero-shot) within the rules above. One prohibited component contaminates the whole ensemble.

---

## 4) Tags

**Select:** `image`, `medical`, `small-data`

---

## 5) Grading Configuration

* **Grade direction:** **Maximize**
* **Theoretical minimum:** `0`
* **Theoretical maximum:** `1`

---

## 6) Grading Script

**Select:** `Custom`

```python
from typing import Iterable

import numpy as np
import pandas as pd


SLICES_PER_VOLUME = 48
SLICES_PRESENTED = 32

RANK_WEIGHT = 0.60
MASK_WEIGHT = 0.40


def _kendall_tau(x: np.ndarray, y: np.ndarray) -> float:
    n = int(x.shape[0])
    if n < 2:
        return 0.0
    concord = 0
    discord = 0
    tie_x = 0
    tie_y = 0
    for i in range(n):
        for j in range(i + 1, n):
            dx = int(x[i]) - int(x[j])
            dy = int(y[i]) - int(y[j])
            if dx == 0:
                tie_x += 1
            if dy == 0:
                tie_y += 1
            if dx != 0 and dy != 0:
                if (dx > 0 and dy > 0) or (dx < 0 and dy < 0):
                    concord += 1
                else:
                    discord += 1
    n_pairs = n * (n - 1) // 2
    denom = float(np.sqrt((n_pairs - tie_x) * (n_pairs - tie_y)))
    if denom <= 0.0:
        return 0.0
    return (concord - discord) / denom


def _macro_f1_binary(pred: np.ndarray, true: np.ndarray) -> float:
    pred = pred.astype(np.int32)
    true = true.astype(np.int32)
    f1s: list[float] = []
    for cls in (0, 1):
        tp = int(np.sum((pred == cls) & (true == cls)))
        fp = int(np.sum((pred == cls) & (true != cls)))
        fn = int(np.sum((pred != cls) & (true == cls)))
        if tp + fp == 0 and tp + fn == 0:
            f1s.append(1.0)
            continue
        if tp == 0:
            f1s.append(0.0)
            continue
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1s.append(2.0 * precision * recall / (precision + recall))
    return float(np.mean(f1s))


def _sanitize_mask(value) -> np.ndarray:
    s = "" if value is None else str(value)
    s = "".join(c for c in s if c in ("0", "1"))
    if len(s) > SLICES_PER_VOLUME:
        s = s[:SLICES_PER_VOLUME]
    elif len(s) < SLICES_PER_VOLUME:
        s = s + "0" * (SLICES_PER_VOLUME - len(s))
    return np.array([int(c) for c in s], dtype=np.int32)


def _coerce_int(value, lo: int, hi: int) -> int:
    try:
        v = int(float(value))
    except (TypeError, ValueError):
        return lo
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """Score submission vs `answers` (private/answers.csv). Composite of squared max(0, Kendall-tau) on cranio-caudal ranks and squared macro-F1 on the 48-cell missing-position mask, weighted 0.6 and 0.4."""
    try:
        required = {"row_id", "volume_id", "presented_index", "pred_rank", "pred_missing_mask"}
        missing_cols = required - set(submission.columns)
        if missing_cols:
            return 0.0

        sub = submission.copy()
        ans = answers.copy()
        sub["volume_id"] = sub["volume_id"].astype(int)
        sub["presented_index"] = sub["presented_index"].astype(int)
        ans["volume_id"] = ans["volume_id"].astype(int)
        ans["presented_index"] = ans["presented_index"].astype(int)

        if sub.duplicated(subset=["volume_id", "presented_index"]).any():
            return 0.0

        sub_lookup = {
            (int(r.volume_id), int(r.presented_index)): r
            for r in sub.itertuples(index=False)
        }

        per_volume_scores: list[float] = []
        for vol_id, group in ans.groupby("volume_id", sort=True):
            group = group.sort_values("presented_index")
            true_ranks = group["true_rank"].astype(int).to_numpy()
            true_mask = _sanitize_mask(group["true_missing_mask"].iloc[0])

            pred_ranks = np.zeros(len(group), dtype=np.int32)
            pred_mask_first = np.zeros(SLICES_PER_VOLUME, dtype=np.int32)
            first_seen = False
            for k, row in enumerate(group.itertuples(index=False)):
                pi = int(row.presented_index)
                sub_row = sub_lookup.get((int(vol_id), pi))
                if sub_row is None:
                    continue
                pred_ranks[k] = _coerce_int(sub_row.pred_rank, 0, SLICES_PRESENTED - 1)
                if not first_seen:
                    pred_mask_first = _sanitize_mask(sub_row.pred_missing_mask)
                    first_seen = True

            tau = _kendall_tau(pred_ranks, true_ranks)
            rank_score = max(0.0, tau) ** 2
            mask_f1 = _macro_f1_binary(pred_mask_first, true_mask)
            mask_score = mask_f1 ** 2
            per_volume_scores.append(
                RANK_WEIGHT * rank_score + MASK_WEIGHT * mask_score
            )

        if not per_volume_scores:
            return 0.0
        final = float(np.mean(per_volume_scores))
        return float(np.clip(final, 0.0, 1.0))

    except Exception:
        return 0.0
```

---

## 7) Prepare Script

The raw dataset is the upstream IXI T1 brain MRI archive — `*.nii.gz` NIfTI files sitting flat at the zip root. `prepare.py` does ALL processing: ingests each NIfTI volume (reorient to RAS, sample 48 axial slices from the central z-band of each subject's brain, intensity-normalise, resize to 192×192 uint8), then applies the challenge-specific curation (per-volume drop of 16 axial positions, random presentation-order permutation of the surviving 32 slices, irreversible per-slice pixel transform with an independent 50% left-right flip and a small in-plane rotation, deterministic patient-level train/test split, and a small amount of label noise on the train side). If `nibabel` is not installed, `prepare.py` auto-installs it via pip. The exact constants live in the code block below.

```python
from __future__ import annotations

import io
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

INGEST_HW = 192
INGEST_SLICES = 48
MIN_BRAIN_SLICES = 60
BRAIN_THRESHOLD_FRAC = 0.05
MAX_SUBJECTS = 600
NARROW_Z_KEEP_FRAC = 0.75

SLICES_PER_VOLUME = 48
SLICES_PRESENTED = 32
SLICES_MISSING = SLICES_PER_VOLUME - SLICES_PRESENTED
TARGET_HW = 192
TEST_FRACTION = 0.18

EDGE_BANDS = list(range(0, 6)) + list(range(42, 48))
MIDDLE_BAND = list(range(6, 42))
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


def _ensure_nibabel():
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


def _stable_rng(seed: int, key: int) -> np.random.Generator:
    mixed = (int(seed) ^ ((int(key) * 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF)) & 0xFFFFFFFFFFFFFFFF
    return np.random.default_rng(mixed)


def _pick_missing_indices(rng):
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


def _missing_mask_string(missing):
    bits = ["0"] * SLICES_PER_VOLUME
    for i in missing:
        bits[int(i)] = "1"
    return MASK_PREFIX + "".join(bits)


def _perturb_slice(slice_uint8, rng):
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


def _maybe_swap_ranks(true_rank, rng):
    if rng.random() >= ADJACENT_SWAP_FRAC:
        return true_rank
    k = int(rng.integers(0, SLICES_PRESENTED - 1))
    pos_k = int(np.where(true_rank == k)[0][0])
    pos_k1 = int(np.where(true_rank == k + 1)[0][0])
    out = true_rank.copy()
    out[pos_k] = k + 1
    out[pos_k1] = k
    return out


def _maybe_flip_mask_bit(mask, rng):
    if rng.random() >= MASK_BITFLIP_FRAC:
        return mask
    j = int(rng.integers(0, SLICES_PER_VOLUME))
    body = list(mask[len(MASK_PREFIX):])
    body[j] = "1" if body[j] == "0" else "0"
    return MASK_PREFIX + "".join(body)


def _save_volume(out_dir, volume_id, presented_slices, rng_perturb):
    sub = out_dir / f"{volume_id:04d}"
    sub.mkdir(parents=True, exist_ok=True)
    for k in range(SLICES_PRESENTED):
        out = _perturb_slice(presented_slices[k], rng_perturb)
        Image.fromarray(out, mode="L").save(sub / f"s{k:02d}.png", format="PNG")


def prepare(raw: Path, public: Path, private: Path) -> None:
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    slices = _ingest_nifti_dir(raw)

    n_total = int(slices.shape[0])
    n_test = int(round(n_total * TEST_FRACTION))
    n_train = n_total - n_test
    if n_train < 50 or n_test < 15:
        raise RuntimeError(
            f"Refusing to build splits with n_train={n_train}, n_test={n_test}."
        )

    rng_id = np.random.default_rng(SPLIT_SEED)
    permuted_volume_ids = rng_id.permutation(n_total)
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
```

---

## 8) GPU Tier

**Select:** **A10G** — single-GPU training of a moderate-sized vision backbone on ~480 training volumes × 32 slices = ~15 K grayscale 192×192 PNGs is well within 24 GB of VRAM. A two-tower / siamese pairwise comparator (ResNet18, ConvNeXt-Tiny, DINOv2 ViT-S linear-probe + small MLP head) trains in single-digit GPU-hours. H100-class compute is not required.

---

## 9) What Not To Use

Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score.

* **Reverse-image-search or pixel-hash any visible PNG** against any public 3D MRI archive in order to recover the original subject identity, original axial index, or DICOM header. The 32 visible slices and the 48-bit mask must be recovered from the provided PNGs alone.
* **Hosted / closed-source APIs** at any stage of training or inference (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.), including any distillation / pseudo-labelling from such teachers. Only open-weights models and self-trained pipelines are permitted.
* **Externally pretrained 3D-MRI sequence models** whose training set overlaps with the upstream collection these slices were drawn from. Generic ImageNet / DINOv2 / CLIP / natural-image backbones are fine; fine-tuned brain-MRI sequencers that already encode the target axial coordinate are not.
* **Filename / order side-channels.** Do not assume that the lexicographic order of `s00.png` … `s31.png` matches any anatomical order, and do not exploit file-system metadata, file mtimes, or any signal outside the PNG pixels and the CSVs.
* **Probability / format hacks that game the grader.** Submitting non-permutation `pred_rank` values to deliberately exploit Kendall-τ tie-handling, padding `pred_missing_mask` with non-binary characters, or per-row-varying masks for the same `volume_id` to try to game the "first row wins" rule.
* **Grader / platform exploitation.** Hard-coded answer dictionaries, filesystem probes for `private/answers.csv`, attempts to read hidden splits, or any channel that is not `public/train/`, `public/train.csv`, `public/test/`, and `public/test.csv`.
* **Ensembles mixing allowed and prohibited components.** An ensemble is allowed only if every component is itself trained (or used zero-shot) within the rules above. One prohibited component contaminates the whole ensemble.

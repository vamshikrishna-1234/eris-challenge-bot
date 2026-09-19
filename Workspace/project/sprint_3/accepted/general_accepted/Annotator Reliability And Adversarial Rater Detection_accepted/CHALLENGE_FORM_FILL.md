# Challenge creation form — fill-in (paired with `DATASET_FORM_FILL.md`)

**Platform status:** **Draft** — sibling of *PolypEditAttribution: Mask Provenance Forensics On Endoscopy* and *SliceShuffle: Cranio-Caudal Sequence Reconstruction*.

---

## 1) Difficulty

**Select:** **Hard**

This challenge requires solvers to *jointly* reason about an image and a structured tabular table of 5 noisy votes per row in order to reconstruct (a) a binary class label, (b) a 5-dim calibrated reliability vector, and (c) a categorical adversarial-rater identity. The composite score rewards calibrated probabilistic outputs and identification of an unreliable annotator — neither is achievable with a vanilla image classifier or with a vanilla majority-vote aggregator. Pre-trained vision backbones (ResNet / ConvNeXt / DINOv2) help on the image-only sub-problem but cannot solve the reliability or adversarial heads on their own; combining the image embedding with the rater table requires a non-trivial multi-input architecture.

---

## 2) Challenge Title

```
Annotator Reliability And Adversarial Rater Detection
```

---

## 3) Problem Description

# Annotator Reliability And Adversarial Rater Detection

## Overview

This is a **Computer Vision / Medical Imaging** challenge that breaks the standard "image → label" supervised setup by adding a per-row **annotator-roster table**. For every test patch the solver receives a 96×96 RGB H&E (Hematoxylin & Eosin) histology tile **plus** five noisy binary votes — each cast by a synthetic annotator with a private, fixed reliability profile, and each accompanied by a self-stated confidence score in `[0, 1]`. The solver's job is to recover three structured outputs per row:

1. **`pred_consensus`** — a binary class label in `{0, 1}` predicting whether the centre 32×32 region of the patch contains metastatic tumour tissue (the gold-standard binary label for the patch).
2. **`pred_rel_1, …, pred_rel_5`** — five floats in `[0, 1]` estimating each rater's **intrinsic reliability**: that rater's long-run probability of voting correctly, a fixed property of the (hidden) profile it was drawn from. This target is **not** a function of the gold consensus on this row — a reliable rater can be wrong on a given patch and an unreliable one can be right — so it cannot be recovered by simply comparing the observable rater labels to a consensus guess. It must be inferred from the image, the rater's stated confidence, and the cross-rater agreement pattern.
3. **`pred_adversarial_idx`** — a categorical value in `{"1", "2", "3", "4", "5", "NONE"}` naming which rater (if any) is from a deliberately-confident-but-wrong "adversarial" pool. Some rows contain one adversarial rater; the rest contain none. The exact frequency at test time is not advertised but is observable in the training labels.

The five raters per row are sampled from a **private pool of fixed reliability profiles** with different accuracy and confidence signatures. The pool includes one **adversarial** profile — a rater that casts its vote with high stated confidence but is mostly wrong — alongside several non-adversarial profiles of varying skill. Profile names and the rule that maps a profile to its behaviour are **never** in the public CSVs — the solver sees only the per-row labels, confidences, and (on training rows) the gold consensus, the float `true_rel_i` reliability targets, and the `true_adversarial_idx`.

This problem is fundamentally a **joint image + tabular** task. Important property of the rater pool: the non-adversarial raters are **noisy enough on their own that a closed-form majority vote over the five rater labels is barely better than chance** at recovering the gold consensus. A solver that ignores the image and only aggregates the rater table will under-perform a solver that consumes both. Likewise, a solver that ignores the rater table (image-only binary classification) cannot recover the per-row reliability or the adversarial rater identity.

A small fraction of training consensus labels carry irreducible noise — the rate is **not** advertised — and the test labels stay clean.

The H&E patches have been processed so that pixel-level matching against external collections is not feasible, and the same processing is applied identically to train and test so the pixel-statistic distributions match.

## Evaluation

The grader computes, over the full test set:

```
S_consensus    = mean over rows of [1 if pred_consensus == true_consensus else 0]

S_reliability  = Brier Skill Score of the reliability predictions
                 against a climatological reference. Over all
                 (row, rater) pairs:
                   MSE_model = mean (pred_rel_i - true_rel_i)^2
                   ref       = mean(true_rel_i)        (climatology)
                   MSE_ref   = mean (ref - true_rel_i)^2
                   S_reliability = clip(1 - MSE_model / MSE_ref, 0, 1)
                 true_rel_i is each rater's intrinsic reliability in
                 [0, 1] (NOT a function of this row's gold consensus).

S_adversarial  = macro-F1 across the adversarial classes
                 {"1", "2", "3", "4", "5", "NONE"}, computed over the
                 entire test set. "NONE" is always an equally-weighted
                 scored class; the numeric slot classes are included
                 when they occur in the ground truth.

Final          = 0.25 * S_consensus^2
               + 0.25 * S_reliability^2
               + 0.50 * S_adversarial^2
                 clipped to [0, 1]
```

* `S_consensus` is straightforward classification accuracy: 1 for an exact match on the binary class, 0 otherwise.
* `S_reliability` is a **Brier Skill Score**: the mean squared error of your reliability estimates is normalised against the error of the climatological baseline (predicting the dataset-wide mean reliability for every rater). A constant predictor — `0.5` everywhere, or the mean itself — scores exactly **0**, so there is no "guess a constant" floor; a perfect estimate scores **1**. Because `true_rel_i` is the rater's intrinsic profile reliability rather than its per-row agreement with the gold label, this head is **independent of the consensus head** and cannot be reconstructed by comparing the observable rater labels to a consensus guess.
* `S_adversarial` is **macro-averaged F1** across the adversarial identities (5 rater slots + `"NONE"`), aggregated once over the test set. `"NONE"` is **always** an equally-weighted scored class — it is never dropped and never up-weighted for being the majority. A numeric slot class absent from the ground truth is excluded from the average so it cannot inflate the score with a spurious perfect 1.0. A trivial "predict NONE everywhere" submission scores only about 0.14 (only the `"NONE"` class is recovered, the numeric-position classes are F1 = 0), well below what a learned model achieves. Identifying the adversarial rater is the genuinely hard, non-image-only part of the task, so it carries the dominant **0.50** weight.
* **Each sub-score is squared before weighting.** Squaring compresses the high end (e.g. an 0.85 sub-score contributes as 0.72), so a strong image-only classifier cannot coast to a high composite on the consensus and reliability heads. A perfect solution (all three sub-scores 1.0) is unaffected and still reaches the maximum 1.0.

**Higher is better.** Minimum: 0.0, Maximum: 1.0.

A row that is missing entirely from the submission — or whose `id` does not appear in `test.csv` — causes the grader to return `0.0`. Likewise, the grader returns `0.0` if the submission contains duplicate `id`s, is missing any required column, or otherwise raises an exception during parsing.

`pred_rel_i` values out of range are clipped to `[0, 1]`. Non-binary `pred_consensus` values are coerced to `0` (worst case) by the grader. `pred_adversarial_idx` values that don't match the canonical six-class set are coerced to `"NONE"`. Submitting illegible / corrupt cells therefore degrades the score smoothly rather than zeroing the whole submission.

## Dataset

* `public/train/images/<id>.jpg` — 96×96 RGB JPEG, one per training row.
* `public/test/images/<id>.jpg` — 96×96 RGB JPEG, one per test row.
* `public/train.csv` — labels and rater table for training rows, including the gold `true_consensus`, the float `true_rel_1..5` reliability targets in `[0, 1]`, and the `true_adversarial_idx`. A small fraction of `true_consensus` values carries irreducible noise.
* `public/test.csv` — the same `id`, `image_path`, and rater table for test rows. **No labels**.
* `public/sample_submission.csv` — one row per test `id` in the exact submission format. The shipped values are deliberately weak placeholders (`pred_consensus = 0`, `pred_rel_i = 0.5`, `pred_adversarial_idx = "NONE"`); participants must overwrite all three heads to score meaningfully.

Row counts are seed-dependent and printed at the end of `prepare.py` (typical: ~8,000 train rows and ~4,000 test rows; one row = 1 JPEG + 1 CSV row).

### File overview

Files shipped to participants: `public/train/images/*.jpg` (96×96 RGB H&E patches, one per training row), `public/test/images/*.jpg` (96×96 RGB H&E patches, one per test row), `public/train.csv` (labels + rater table for training rows), `public/test.csv` (ids + rater table only, no labels), and `public/sample_submission.csv` (submission template with the full 8-column shape).

| Item                          | Description                              |
|-------------------------------|------------------------------------------|
| `public/train/images/*.jpg`   | 96×96 RGB H&E patch                      |
| `public/test/images/*.jpg`    | 96×96 RGB H&E patch                      |
| `public/train.csv`            | Labels + rater table for training rows   |
| `public/test.csv`             | Ids + rater table only, no labels        |
| `public/sample_submission.csv`| Submission template, full shape          |

### Feature Details

The columns differ between the training CSV, the test CSV, and the submission CSV. They are listed separately so there is no ambiguity about which columns belong to which file.

**Training data columns (`public/train.csv`) — 19 columns:**

Columns (in order): `id` (int), `image_path` (string), `rater_1_label` (int), `rater_2_label` (int), `rater_3_label` (int), `rater_4_label` (int), `rater_5_label` (int), `rater_1_conf` (float), `rater_2_conf` (float), `rater_3_conf` (float), `rater_4_conf` (float), `rater_5_conf` (float), `true_consensus` (int), `true_rel_1` (float), `true_rel_2` (float), `true_rel_3` (float), `true_rel_4` (float), `true_rel_5` (float), `true_adversarial_idx` (string).

| Column                 | Type   | Description                              |
|------------------------|--------|------------------------------------------|
| `id`                   | int    | Unique row identifier                    |
| `image_path`           | string | Relative path to the patch JPEG          |
| `rater_1_label`        | int    | Rater 1 binary vote (0 or 1)             |
| `rater_2_label`        | int    | Rater 2 binary vote (0 or 1)             |
| `rater_3_label`        | int    | Rater 3 binary vote (0 or 1)             |
| `rater_4_label`        | int    | Rater 4 binary vote (0 or 1)             |
| `rater_5_label`        | int    | Rater 5 binary vote (0 or 1)             |
| `rater_1_conf`         | float  | Rater 1 confidence in `[0, 1]`           |
| `rater_2_conf`         | float  | Rater 2 confidence in `[0, 1]`           |
| `rater_3_conf`         | float  | Rater 3 confidence in `[0, 1]`           |
| `rater_4_conf`         | float  | Rater 4 confidence in `[0, 1]`           |
| `rater_5_conf`         | float  | Rater 5 confidence in `[0, 1]`           |
| `true_consensus`       | int    | Gold binary class (0 or 1)               |
| `true_rel_1`           | float  | Rater 1 intrinsic reliability `[0,1]`    |
| `true_rel_2`           | float  | Rater 2 intrinsic reliability `[0,1]`    |
| `true_rel_3`           | float  | Rater 3 intrinsic reliability `[0,1]`    |
| `true_rel_4`           | float  | Rater 4 intrinsic reliability `[0,1]`    |
| `true_rel_5`           | float  | Rater 5 intrinsic reliability `[0,1]`    |
| `true_adversarial_idx` | string | "1", "2", "3", "4", "5", or "NONE"       |

**Test metadata columns (`public/test.csv`) — 12 columns:**

Columns (in order): `id` (int), `image_path` (string), `rater_1_label` (int), `rater_2_label` (int), `rater_3_label` (int), `rater_4_label` (int), `rater_5_label` (int), `rater_1_conf` (float), `rater_2_conf` (float), `rater_3_conf` (float), `rater_4_conf` (float), `rater_5_conf` (float). No label columns are present.

| Column                 | Type   | Description                              |
|------------------------|--------|------------------------------------------|
| `id`                   | int    | Unique row identifier                    |
| `image_path`           | string | Relative path to the patch JPEG          |
| `rater_1_label`        | int    | Rater 1 binary vote (0 or 1)             |
| `rater_2_label`        | int    | Rater 2 binary vote (0 or 1)             |
| `rater_3_label`        | int    | Rater 3 binary vote (0 or 1)             |
| `rater_4_label`        | int    | Rater 4 binary vote (0 or 1)             |
| `rater_5_label`        | int    | Rater 5 binary vote (0 or 1)             |
| `rater_1_conf`         | float  | Rater 1 confidence in `[0, 1]`           |
| `rater_2_conf`         | float  | Rater 2 confidence in `[0, 1]`           |
| `rater_3_conf`         | float  | Rater 3 confidence in `[0, 1]`           |
| `rater_4_conf`         | float  | Rater 4 confidence in `[0, 1]`           |
| `rater_5_conf`         | float  | Rater 5 confidence in `[0, 1]`           |

**Submission columns (`public/sample_submission.csv` and your final submission) — 8 columns:**

Columns (in order): `id` (int), `pred_consensus` (int, 0 or 1), `pred_rel_1` (float in `[0,1]`), `pred_rel_2` (float in `[0,1]`), `pred_rel_3` (float in `[0,1]`), `pred_rel_4` (float in `[0,1]`), `pred_rel_5` (float in `[0,1]`), `pred_adversarial_idx` (string, one of "1","2","3","4","5","NONE").

| Column                 | Type   | Constraint                               |
|------------------------|--------|------------------------------------------|
| `id`                   | int    | Same set as `public/test.csv`            |
| `pred_consensus`       | int    | Binary 0 or 1                            |
| `pred_rel_1`           | float  | Reliability of rater 1 in `[0, 1]`       |
| `pred_rel_2`           | float  | Reliability of rater 2 in `[0, 1]`       |
| `pred_rel_3`           | float  | Reliability of rater 3 in `[0, 1]`       |
| `pred_rel_4`           | float  | Reliability of rater 4 in `[0, 1]`       |
| `pred_rel_5`           | float  | Reliability of rater 5 in `[0, 1]`       |
| `pred_adversarial_idx` | string | One of "1","2","3","4","5","NONE"        |

## Submission

Submit a CSV file with a header row and **exactly one row per `id` in `test.csv`**. The header must contain these **8 columns in this order**: `id`, `pred_consensus`, `pred_rel_1`, `pred_rel_2`, `pred_rel_3`, `pred_rel_4`, `pred_rel_5`, `pred_adversarial_idx`.

| Column                 | Type   | Description                              |
|------------------------|--------|------------------------------------------|
| `id`                   | int    | Identifier from `test.csv`               |
| `pred_consensus`       | int    | Binary class prediction (0 or 1)         |
| `pred_rel_1`           | float  | Reliability of rater 1 in `[0, 1]`       |
| `pred_rel_2`           | float  | Reliability of rater 2 in `[0, 1]`       |
| `pred_rel_3`           | float  | Reliability of rater 3 in `[0, 1]`       |
| `pred_rel_4`           | float  | Reliability of rater 4 in `[0, 1]`       |
| `pred_rel_5`           | float  | Reliability of rater 5 in `[0, 1]`       |
| `pred_adversarial_idx` | string | One of "1","2","3","4","5","NONE"        |

**Requirements:**

* Header row plus exactly one row per `id` in `test.csv` — `id` must equal exactly the set in `test.csv`. Duplicate `id`s cause the grader to return `0.0`.
* `pred_consensus` must be an integer in `{0, 1}`. Non-binary values are coerced to `0` (worst case) by the grader.
* `pred_rel_1` … `pred_rel_5` must be floats in `[0, 1]`. Out-of-range values are clipped; non-numeric cells default to `0.5`.
* `pred_adversarial_idx` must be one of the six strings `"1"`, `"2"`, `"3"`, `"4"`, `"5"`, `"NONE"`. Anything else (including `0`, blank, or a numeric out of `1..5`) is coerced to `"NONE"` by the grader.
* Missing rows are not silently filled in — a row-set mismatch causes the grader to return `0.0`.
* The grader returns `0.0` if any of the eight required columns are missing from the submission, if the submission contains duplicate `id`s, or if it raises any exception during parsing.

**Example of a correctly formatted submission file (illustrative only):**

The three rows below come from three different test `id`s. The full submission has one row per test `id`. The placeholders show the column layout — real submissions will have informative per-row predictions.

```
id,pred_consensus,pred_rel_1,pred_rel_2,pred_rel_3,pred_rel_4,pred_rel_5,pred_adversarial_idx
8000,1,0.91,0.62,0.74,0.08,0.55,4
8001,0,0.83,0.71,0.66,0.79,0.69,NONE
8002,1,0.40,0.86,0.92,0.29,0.51,1
```

## What Not To Do

Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score:

* **Submit closed-form rule-only outputs that ignore the image.** A formula like `pred_rel_i = mean(|rater_i_label - majority_label|)` or a pure rater-agreement statistic with no learned image component is out of scope — the challenge is meant to be solved by joint image + tabular reasoning.
* **Isolate the adversarial rater from stated confidence alone.** Any heuristic or rule-based system that picks `pred_adversarial_idx` purely from the self-stated confidence scores (e.g. "the rater with the highest confidence is the adversary") without processing the image patch is out of scope. The adversarial profile's confidence band deliberately overlaps an honest specialist's, so confidence alone cannot separate them — telling an adversary apart from an honest-but-wrong expert requires reasoning jointly over the image evidence and the full rater pattern.
* **Hosted / closed-source APIs** at any stage of training or inference (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.), including any distillation / pseudo-labelling from such teachers. Only open-weights models and self-trained pipelines are permitted.
* **Externally pretrained classifiers used as a black-box consensus head** — i.e., loading any third-party H&E-tile checkpoint that was already fine-tuned for binary metastasis classification on a public corpus, and submitting its argmax as `pred_consensus` while ignoring the rater table. Generic ImageNet / DINOv2 / CLIP backbones are fine; any solution that does not consume the rater-roster columns is rejected on review.
* **Pixel-hash any visible JPEG against any public H&E archive** in order to recover the underlying patch identity or gold consensus. The patches have been processed so byte-level lookup is not reliable; the consensus and rater-roster labels must be recovered from the provided JPEG pixels and the CSV columns alone.
* **Filename / order side-channels.** Do not assume anatomical adjacency, slide order, or any other structure in the lexicographic ordering of `<id>.jpg` files; do not exploit file-system metadata, file mtimes, or any signal outside the JPEG pixels and the CSV columns.
* **Format / range hacks that game the grader.** Submitting non-binary `pred_consensus` values, padding `pred_adversarial_idx` with non-canonical strings, or supplying out-of-range `pred_rel_i` values to deliberately exploit the grader's clipping behaviour.
* **Grader / platform exploitation.** Hard-coded answer dictionaries, filesystem probes for `private/answers.csv`, attempts to read hidden splits, or any channel that is not `public/train/`, `public/train.csv`, `public/test/`, and `public/test.csv`.

---

## 4) Tags

Suggested platform tags: `image`, `medical`, `feature-engineering`, `multimodal`, `small-data`.

---

## 5) Grading Configuration

* **Direction:** Maximize
* **Theoretical minimum:** `0.0`
* **Theoretical maximum:** `1.0`

---

## 6) Grading Script

**Select:** `Custom`

```python
import numpy as np
import pandas as pd


N_RATERS = 5

W_CONSENSUS = 0.25
W_RELIABILITY = 0.25
W_ADVERSARIAL = 0.50

SCORE_POWER = 2.0

ADV_CLASSES = ["1", "2", "3", "4", "5", "NONE"]
ADV_VALID = set(ADV_CLASSES)


def _coerce_consensus(v) -> int:
    try:
        x = int(round(float(v)))
    except (TypeError, ValueError):
        return 0
    return 1 if x == 1 else 0


def _coerce_rel(v) -> float:
    try:
        x = float(v)
    except (TypeError, ValueError):
        return 0.5
    if not np.isfinite(x):
        return 0.5
    return float(np.clip(x, 0.0, 1.0))


def _coerce_adv(v) -> str:
    if v is None:
        return "NONE"
    s = str(v).strip()
    if s in ADV_VALID:
        return s
    try:
        f = float(s)
        if np.isfinite(f):
            n = int(round(f))
            if 1 <= n <= N_RATERS:
                return str(n)
    except (TypeError, ValueError):
        pass
    return "NONE"


def _macro_f1_multiclass(y_true, y_pred) -> float:
    # Macro-F1 averaged with EQUAL weight. "NONE" is always a scored class
    # (never dropped, never up-weighted for being the majority); numeric slot
    # classes {1..5} are included only when they occur in y_true, since an
    # absent class's degenerate tp+fp==0 case would otherwise inflate the
    # average with a spurious perfect 1.0.
    true_set = set(y_true)
    present = [c for c in ADV_CLASSES if c in true_set]
    if "NONE" not in present:
        present.append("NONE")
    if not present:
        return 0.0
    f1s = []
    for cls in present:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p == cls)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != cls and p == cls)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p != cls)
        if tp == 0:
            f1s.append(0.0); continue
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1s.append(2.0 * precision * recall / (precision + recall))
    return float(np.mean(f1s))


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """Composite: 0.25*consensus^2 + 0.25*reliability_BSS^2 + 0.50*adversarial_F1^2."""
    try:
        rel_cols_pred = [f"pred_rel_{k+1}" for k in range(N_RATERS)]
        rel_cols_true = [f"true_rel_{k+1}" for k in range(N_RATERS)]
        required_sub = {"id", "pred_consensus", "pred_adversarial_idx"} | set(rel_cols_pred)
        required_ans = {"id", "true_consensus", "true_adversarial_idx"} | set(rel_cols_true)

        if not required_sub.issubset(set(submission.columns)):
            return 0.0
        if not required_ans.issubset(set(answers.columns)):
            return 0.0

        sub = submission.copy()
        ans = answers.copy()
        try:
            sub["id"] = sub["id"].astype(int)
            ans["id"] = ans["id"].astype(int)
        except (TypeError, ValueError):
            return 0.0

        if sub["id"].duplicated().any():
            return 0.0
        if set(sub["id"].tolist()) != set(ans["id"].tolist()):
            return 0.0

        # Single indexed alignment (O(N)); checks above guarantee a clean 1:1.
        sub = sub.set_index("id").reindex(ans["id"].to_numpy()).reset_index()

        # consensus head
        pred_cons = np.array([_coerce_consensus(v) for v in sub["pred_consensus"]], dtype=int)
        true_cons = ans["true_consensus"].astype(int).to_numpy()
        s_consensus = float(np.mean(pred_cons == true_cons))

        # reliability head: Brier Skill Score over all (row, rater) pairs
        pred_rel = np.column_stack([
            [_coerce_rel(v) for v in sub[col]] for col in rel_cols_pred
        ]).astype(float)
        true_rel = ans[rel_cols_true].to_numpy(dtype=float)
        flat_pred = pred_rel.reshape(-1)
        flat_true = true_rel.reshape(-1)
        mse_model = float(np.mean((flat_pred - flat_true) ** 2))
        ref = float(np.mean(flat_true))
        mse_ref = float(np.mean((ref - flat_true) ** 2))
        if mse_ref <= 1e-12:
            s_reliability = 1.0 if mse_model <= 1e-12 else 0.0
        else:
            s_reliability = float(np.clip(1.0 - mse_model / mse_ref, 0.0, 1.0))

        # adversarial head: macro-F1 over present classes
        adv_pred = [_coerce_adv(v) for v in sub["pred_adversarial_idx"]]
        adv_true = [
            (str(v).strip() if str(v).strip() in ADV_VALID else "NONE")
            for v in ans["true_adversarial_idx"]
        ]
        s_adversarial = _macro_f1_multiclass(adv_true, adv_pred)

        final = (
            W_CONSENSUS * (s_consensus ** SCORE_POWER)
            + W_RELIABILITY * (s_reliability ** SCORE_POWER)
            + W_ADVERSARIAL * (s_adversarial ** SCORE_POWER)
        )
        return float(np.clip(final, 0.0, 1.0))

    except Exception:
        return 0.0
```

---

## 7) Prepare Script

The raw dataset is the upstream PatchCamelyon Parquet shards sitting in `raw/` (multiple `train-*.parquet`, `valid-*.parquet`, `test-*.parquet`). `prepare.py` does ALL processing: it discovers the Parquet shards, sub-samples a 50/50-balanced 8,000 train + 4,000 test set from disjoint upstream shards, decodes each patch, downsamples and re-upsamples it to discard fine texture, and re-encodes it as a moderate-quality 96×96 JPEG, generates 5-rater predictions per row from a private set of fixed rater profiles (one of which is the adversarial profile that fires on roughly 30% of rows), saves the per-row `(image, 5 rater labels, 5 rater confidences)` and the gold targets, performs a deterministic train/test split with non-overlapping `id`s, and injects a small fraction of train-side label noise on `true_consensus`. If `pyarrow` is not installed, the platform's pandas typically pulls it in transitively; the script uses `pandas.read_parquet` directly.

```python
from __future__ import annotations

import hashlib
import io
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

N_TRAIN = 8000
N_TEST = 4000
PATCH_HW = 96
DOWNSCALE_HW = 72
JPEG_Q = 75

N_RATERS = 5
ADVERSARIAL_FRACTION = 0.30
LABEL_NOISE_FRACTION = 0.05

SPLIT_SEED = 0xA7C3D4E5
TEST_SPLIT_SEED = 0xF2E1D0C9
RATER_SEED = 0xB1C2D3E4
ADVERSARY_SEED = 0xC2D3E4F5
NOISE_SEED = 0xD3E4F506
SAMPLE_SEED = 0xE4F50617

PROFILE_BIASES = {
    "specialist":     {"acc": 0.62, "conf_mean": 0.78, "conf_jit": 0.05},
    "novice_recall":  {"acc_pos": 0.50, "acc_neg": 0.45, "conf_mean": 0.55, "conf_jit": 0.06},
    "novice_prec":    {"acc_pos": 0.45, "acc_neg": 0.50, "conf_mean": 0.55, "conf_jit": 0.06},
    "random":         {"acc": 0.50, "conf_mean": 0.50, "conf_jit": 0.06},
    "adversarial":    {"acc": 0.22, "conf_mean": 0.86, "conf_jit": 0.04},
}
NON_ADV_PROFILES = ["specialist", "novice_recall", "novice_prec", "random"]


# Intrinsic per-profile reliability (marginal accuracy of the profile). This
# is the `true_rel_i` target - a property of the rater profile, NOT of the
# per-row gold consensus, so it cannot be reconstructed from the observable
# rater label plus a consensus guess.
def _profile_reliability(profile: str) -> float:
    p = PROFILE_BIASES[profile]
    acc = p["acc"] if "acc" in p else 0.5 * (p["acc_pos"] + p["acc_neg"])
    return round(float(acc), 4)


PROFILE_RELIABILITY = {prof: _profile_reliability(prof) for prof in PROFILE_BIASES}


def _extract_zips(raw: Path) -> None:
    for zf in sorted(raw.glob("*.zip")):
        with zipfile.ZipFile(zf, "r") as z:
            members = z.namelist()
        sentinel = raw / Path(members[0]).parts[0] if members else None
        if sentinel is not None and sentinel.exists():
            continue
        with zipfile.ZipFile(zf, "r") as z:
            z.extractall(raw)


def _find_parquet_shards(raw: Path) -> list[Path]:
    candidates = [p for p in raw.rglob("*.parquet")]
    if not candidates:
        raise FileNotFoundError(
            f"No *.parquet shards found under {raw}. "
            "Expected upstream PatchCamelyon Parquet shards."
        )
    return sorted(candidates)


def _stable_rng(seed: int, key: int) -> np.random.Generator:
    """Deterministic, statistically-independent per-row stream.

    A SHA-256 digest of (seed, key) gives 32 bytes of high-quality entropy;
    feeding all 256 bits to ``np.random.SeedSequence`` yields well-separated,
    decorrelated streams for each (seed, key) pair - far safer than an ad-hoc
    64-bit XOR/multiply mix, which can leave low-order correlations between the
    per-row streams.
    """
    digest = hashlib.sha256(f"{int(seed)}:{int(key)}".encode("utf-8")).digest()
    seed_seq = np.random.SeedSequence(int.from_bytes(digest, "big"))
    return np.random.default_rng(seed_seq)


def _decode_image_bytes(rec) -> np.ndarray:
    if isinstance(rec, dict) and "bytes" in rec:
        b = rec["bytes"]
    elif isinstance(rec, (bytes, bytearray)):
        b = bytes(rec)
    elif hasattr(rec, "tobytes"):
        b = rec.tobytes()
    else:
        b = bytes(rec)
    img = Image.open(io.BytesIO(b)).convert("RGB")
    return np.asarray(img, dtype=np.uint8)


def _save_jpeg(arr: np.ndarray, dst: Path) -> None:
    img = Image.fromarray(arr, mode="RGB")
    if DOWNSCALE_HW < PATCH_HW:
        img = img.resize((DOWNSCALE_HW, DOWNSCALE_HW), resample=Image.BILINEAR)
        img = img.resize((PATCH_HW, PATCH_HW), resample=Image.BILINEAR)
    img.save(dst, format="JPEG", quality=JPEG_Q)


def _sample_balanced(df_label: np.ndarray, n_total: int, rng: np.random.Generator) -> np.ndarray:
    n_each = n_total // 2
    pos_idx = np.where(df_label == True)[0]
    neg_idx = np.where(df_label == False)[0]
    if pos_idx.size < n_each or neg_idx.size < n_each:
        raise RuntimeError("not enough positives/negatives in pool")
    pos_pick = rng.choice(pos_idx, size=n_each, replace=False)
    neg_pick = rng.choice(neg_idx, size=n_each, replace=False)
    out = np.concatenate([pos_pick, neg_pick])
    rng.shuffle(out)
    return out


def _draw_label_for_profile(profile: str, true_label: int, rng) -> int:
    p = PROFILE_BIASES[profile]
    if profile in ("specialist", "random", "adversarial"):
        acc = p["acc"]
    else:
        acc = p["acc_pos"] if true_label == 1 else p["acc_neg"]
    return int(true_label if rng.random() < acc else 1 - true_label)


def _draw_conf_for_profile(profile: str, rng) -> float:
    p = PROFILE_BIASES[profile]
    c = float(p["conf_mean"] + rng.normal(0.0, p["conf_jit"]))
    return float(np.clip(c, 0.05, 0.99))


def _build_row_raters(true_label, rng_p, rng_l, rng_c):
    # Draw a full non-adversarial roster, then overwrite ONE uniformly-chosen
    # slot with the adversarial profile in ADVERSARIAL_FRACTION of rows. Keeps
    # the adversarial slot exactly uniform with no insert/pop length juggling.
    profiles = rng_p.choice(NON_ADV_PROFILES, size=N_RATERS, replace=True).tolist()
    if rng_p.random() < ADVERSARIAL_FRACTION:
        adv_slot = int(rng_p.integers(0, N_RATERS))
        profiles[adv_slot] = "adversarial"
        adv_idx_1 = adv_slot + 1
    else:
        adv_idx_1 = 0
    labels = [_draw_label_for_profile(prof, true_label, rng_l) for prof in profiles]
    confs = [_draw_conf_for_profile(prof, rng_c) for prof in profiles]
    return labels, confs, profiles, adv_idx_1


def _materialise_split(df_subset, out_img_dir, id_offset, is_train, rng_label_noise):
    out_img_dir.mkdir(parents=True, exist_ok=True)
    rows_full = []; answers = []
    for local_i, (_, src) in enumerate(df_subset.iterrows()):
        rid = id_offset + local_i
        true_label = int(bool(src["label"]))
        arr = _decode_image_bytes(src["image"])
        if arr.shape != (PATCH_HW, PATCH_HW, 3):
            arr = np.asarray(
                Image.fromarray(arr, mode="RGB").resize((PATCH_HW, PATCH_HW), resample=Image.BILINEAR),
                dtype=np.uint8,
            )
        img_name = f"{rid:06d}.jpg"
        img_rel = f"images/{img_name}"
        _save_jpeg(arr, out_img_dir / img_name)
        rng_p = _stable_rng(RATER_SEED, rid)
        rng_l = _stable_rng(RATER_SEED ^ 0x1111, rid)
        rng_c = _stable_rng(RATER_SEED ^ 0x2222, rid)
        labels, confs, profiles, adv_1 = _build_row_raters(true_label, rng_p, rng_l, rng_c)
        true_rels = [PROFILE_RELIABILITY[p] for p in profiles]
        adv_str = "NONE" if adv_1 == 0 else str(adv_1)
        train_consensus = true_label
        if is_train and rng_label_noise.random() < LABEL_NOISE_FRACTION:
            train_consensus = 1 - train_consensus
        full = {"id": rid, "image_path": img_rel}
        for k in range(N_RATERS):
            full[f"rater_{k+1}_label"] = int(labels[k])
            full[f"rater_{k+1}_conf"] = float(confs[k])
        if is_train:
            full["true_consensus"] = int(train_consensus)
            for k in range(N_RATERS):
                full[f"true_rel_{k+1}"] = float(true_rels[k])
            full["true_adversarial_idx"] = adv_str
        rows_full.append(full)
        if not is_train:
            ar = {"id": rid, "true_consensus": int(true_label), "true_adversarial_idx": adv_str}
            for k in range(N_RATERS):
                ar[f"true_rel_{k+1}"] = float(true_rels[k])
            answers.append(ar)
    return rows_full, answers


def prepare(raw: Path, public: Path, private: Path) -> None:
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    _extract_zips(raw)
    shards = _find_parquet_shards(raw)
    train_shards = [p for p in shards if "train" in p.name.lower()]
    test_shards = [p for p in shards if "test" in p.name.lower()]
    valid_shards = [p for p in shards if "valid" in p.name.lower()]
    if not train_shards or not test_shards:
        train_shards = shards[: max(1, len(shards) // 2)]
        test_shards = shards[max(1, len(shards) // 2):]
    train_df = pd.concat([pd.read_parquet(p) for p in train_shards], ignore_index=True)
    test_pool = test_shards if test_shards else valid_shards
    test_df = pd.concat([pd.read_parquet(p) for p in test_pool], ignore_index=True)
    rng_split_train = np.random.default_rng(SPLIT_SEED)
    rng_split_test = np.random.default_rng(TEST_SPLIT_SEED)
    train_pick = _sample_balanced(train_df["label"].to_numpy(), N_TRAIN, rng_split_train)
    test_pick = _sample_balanced(test_df["label"].to_numpy(), N_TEST, rng_split_test)
    train_subset = train_df.iloc[train_pick].reset_index(drop=True)
    test_subset = test_df.iloc[test_pick].reset_index(drop=True)
    train_dir = public / "train"; test_dir = public / "test"
    train_dir.mkdir(parents=True, exist_ok=True); test_dir.mkdir(parents=True, exist_ok=True)
    rng_noise = np.random.default_rng(NOISE_SEED)
    train_rows, _ = _materialise_split(train_subset, train_dir / "images", 0, True, rng_noise)
    test_rows, ans_rows = _materialise_split(test_subset, test_dir / "images", N_TRAIN, False, rng_noise)
    train_cols = ["id", "image_path"]
    for k in range(N_RATERS):
        train_cols += [f"rater_{k+1}_label", f"rater_{k+1}_conf"]
    train_cols.append("true_consensus")
    for k in range(N_RATERS):
        train_cols.append(f"true_rel_{k+1}")
    train_cols.append("true_adversarial_idx")
    pd.DataFrame(train_rows)[train_cols].to_csv(public / "train.csv", index=False)
    test_cols = ["id", "image_path"]
    for k in range(N_RATERS):
        test_cols += [f"rater_{k+1}_label", f"rater_{k+1}_conf"]
    pd.DataFrame(test_rows)[test_cols].to_csv(public / "test.csv", index=False)
    sample = []
    for row in test_rows:
        sub = {"id": row["id"], "pred_consensus": 0}
        for k in range(N_RATERS):
            sub[f"pred_rel_{k+1}"] = 0.5
        sub["pred_adversarial_idx"] = "NONE"
        sample.append(sub)
    sample_cols = ["id", "pred_consensus"] + [f"pred_rel_{k+1}" for k in range(N_RATERS)] + ["pred_adversarial_idx"]
    pd.DataFrame(sample)[sample_cols].to_csv(public / "sample_submission.csv", index=False)
    ans_cols = ["id", "true_consensus"] + [f"true_rel_{k+1}" for k in range(N_RATERS)] + ["true_adversarial_idx"]
    pd.DataFrame(ans_rows)[ans_cols].to_csv(private / "answers.csv", index=False)
```

---

## 8) GPU Tier

**Select:** **A10G** — 8K training rows × 96×96 RGB JPEGs is a small workload by any image-classification standard. A two-tower model that combines a small image encoder (ResNet18 / ConvNeXt-Tiny / DINOv2 ViT-S linear-probe) with a small per-rater MLP that ingests `(image_embedding, rater_label, rater_confidence)` trains end-to-end in single-digit GPU-hours on a 24 GB A10G. H100-class compute is not required.

---

## 9) What Not To Use

Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score.

* **Closed-form rule-only outputs that ignore the image.** A formula like `pred_rel_i = mean(|rater_i_label - majority_label|)` or any pure rater-agreement statistic with no learned image component is out of scope — the challenge is meant to be solved by joint image + tabular reasoning.
* **Hosted / closed-source APIs** (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.) at any stage of training or inference, including any distillation / pseudo-labelling from such teachers.
* **Externally pretrained classifiers** used as a black-box consensus head while ignoring the rater table. Generic ImageNet / DINOv2 / CLIP backbones are fine; checkpoints already fine-tuned for binary metastasis classification on any public H&E corpus are not.
* **Pixel-hash matching** of any visible JPEG against any public H&E archive in order to recover the underlying patch identity or gold consensus.
* **Filename / order side-channels.** Do not assume any structure in the lexicographic ordering of `<id>.jpg` files; do not exploit file-system metadata, file mtimes, or any signal outside the JPEG pixels and the CSV columns.
* **Format / range hacks** — non-binary `pred_consensus` values, non-canonical `pred_adversarial_idx` strings, or out-of-range `pred_rel_i` values intended to game the grader's clipping behaviour.
* **Grader / platform exploitation** — hard-coded answer dictionaries, filesystem probes for `private/answers.csv`, or any channel that is not `public/train/`, `public/train.csv`, `public/test/`, and `public/test.csv`.

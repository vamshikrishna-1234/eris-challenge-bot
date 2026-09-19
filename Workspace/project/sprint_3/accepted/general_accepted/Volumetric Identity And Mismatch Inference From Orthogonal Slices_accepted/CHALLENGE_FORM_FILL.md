# Challenge creation form — fill-in (paired with `DATASET_FORM_FILL.md`)

**Platform status:** **Draft**

---

## 1) Difficulty

**Select:** **Hard**

This challenge requires solvers to *jointly* reason about three orthogonal 2D cross-sections in order to recover (a) a 6-way structural-type identity, (b) a within-corpus class label whose space is anonymised, (c) a continuous volumetric extent (a true 2D→3D inference), (d) a binary "is-this-a-coherent-triplet?" decision, and (e) a categorical "which view is the intruder?" identity. The composite score punishes constant predictions on every head — a vanilla 2D classifier with concatenated views cannot solve the volumetric or intruder-detection sub-problems, and a vanilla 3D backbone cannot be applied because the underlying 3D volume is never provided.

---

## 2) Challenge Title

```
Volumetric Identity And Mismatch Inference From Orthogonal Slices
```

---

## 3) Problem Description

### Overview

# Volumetric Identity And Mismatch Inference From Orthogonal Slices

This is a **Computer Vision / 3D Medical Imaging** challenge that breaks the standard "2D image → label" supervised setup. For every test sample the solver receives **three** 28×28 grayscale PNGs — labelled `axial`, `sagittal`, `coronal` — that were extracted from the mid-planes of a small 3D medical volume. The original 3D volume is **never** provided.

The solver's job is to recover **five** structured outputs per row:

1. **`pred_corpus_id`** — an integer in `{0, 1, 2, 3, 4, 5}` naming which of six anatomical *structural types* the underlying volume belongs to. The mapping from integer to structural type is a private fixed permutation; the solver only sees integers in the training labels and must learn the partition from there.
2. **`pred_class_label`** — a non-negative integer giving the within-corpus class label of the underlying volume. Different corpora have different label cardinalities and label spaces are also anonymised; the solver must learn, per `corpus_id`, which integer labels are valid.
3. **`pred_vol_radius`** — a float in `[0, 1]` giving the volumetric extent of the underlying 3D volume — defined as the bounding-box diagonal length of the volume's foreground voxels normalised by `28 √3`. This requires inferring 3D extent from three orthogonal 2D cross-sections.
4. **`pred_mismatched_triplet`** — a binary value in `{0, 1}` flagging whether the three slices are **not** from the same volume. Some test rows are **incoherent triplets** in which one of the three slices does not belong to the same underlying volume as the other two. The intruder slice is visually plausible on its own, so it cannot be reliably caught by inspecting any single view in isolation — only by detecting that the three views are no longer mutually consistent as cross-sections of a single volume. A per-view appearance classifier cannot catch it; cross-view reasoning can.
5. **`pred_mismatched_axis`** — a categorical value in `{"NONE", "AXIAL", "SAGITTAL", "CORONAL"}` naming which slice is the intruder. Must be `"NONE"` whenever `pred_mismatched_triplet == 0`.

The three slices have been processed so that pixel-level matching against external public corpora is not feasible. Training labels for `class_label` carry an irreducible noise floor; test labels are clean.

This problem is fundamentally a **multi-head, multi-task** inference over a partial volumetric observation. A solver that ignores the inter-view relationship cannot answer the intruder or radius heads; a solver that ignores per-view content cannot answer the corpus or class heads.

**What Not To Do** (using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score):

* **Constant-prediction or rule-only solutions.** Submissions that predict a fixed value for any head with no learned image component are out of scope.
* **Hosted / closed-source APIs** at any stage of training or inference (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.), including any distillation / pseudo-labelling from such teachers. Only open-weights models and self-trained pipelines are permitted.
* **Pixel-hashing or perceptual-hashing the visible PNGs** against any public 3D medical-volume archive in order to recover the underlying volume identity, structural-type label, or class label. The slices have been processed so byte-level lookup is not reliable; the labels must be recovered from the provided PNG pixels and the CSV columns alone.
* **Externally pretrained classifiers fine-tuned on the same upstream corpora** at the volume level. Generic ImageNet / DINOv2 / CLIP-style 2D backbones are fine; checkpoints already fine-tuned on overlapping public 3D collections are not.
* **Filename / order side-channels.** Do not assume any structure in the lexicographic ordering of `<id>_*.png` files; do not exploit file-system metadata, file mtimes, or any signal outside the PNG pixels and the CSV columns.
* **Format / range hacks that game the grader.** Submitting non-integer `pred_corpus_id`, negative `pred_class_label`, out-of-range `pred_vol_radius`, non-binary `pred_mismatched_triplet`, or non-canonical `pred_mismatched_axis` values. The grader validates every cell strictly and scores the whole submission `0.0` on any malformed value — there is no clipping/coercion behaviour left to exploit.
* **Grader / platform exploitation.** Hard-coded answer dictionaries, filesystem probes for `private/answers.csv`, attempts to read hidden splits, or any channel that is not `public/train/`, `public/train.csv`, `public/test/`, and `public/test.csv`.

### Evaluation

The grader computes, over the full test set:

```
S_corpus     = macro-F1 across the 6 corpus_id classes {0, 1, 2, 3, 4, 5}
S_class      = mean over CLEAN rows (true_mismatched_triplet == 0) of
                 [1 if pred_class_label == true_class_label else 0]
S_radius     = mean over rows of
                 max(0, 1 - 40 * (pred_vol_radius - true_vol_radius)^2)
S_mismatch   = mean over rows of
                 [1 if pred_mismatched_triplet == true_mismatched_triplet
                    else 0]
S_axis       = macro-F1 across {NONE, AXIAL, SAGITTAL, CORONAL},
               computed once over the entire test set

S_partial    = 0.05*S_corpus + 0.25*S_class + 0.20*S_radius
             + 0.20*S_mismatch + 0.30*S_axis

S_joint      = fraction of test rows for which EVERY head is correct on
               that SAME row: corpus exact, radius within 0.10, coherence
               flag correct, and axis correct; plus class exact on clean
               rows (class is excluded on intruder rows, where it is
               undefined)

Final = 0.5 * S_partial + 0.5 * S_joint     clipped to [0, 1]
```

* The score blends two views of quality. **`S_partial`** is a weighted average of per-head accuracy (smooth partial credit). **`S_joint`** is the fraction of samples where *all* heads are correct simultaneously — a far stricter bar that rewards coherent, fully-correct reconstructions rather than being "pretty good on each head separately."
* Within `S_partial`, `S_corpus` is a **token 0.05** (the six corpora are visually distinct, so corpus identification is nearly free), `S_axis` carries the **most weight (0.30)** as the hardest head, with `S_class` 0.25 and `S_radius`/`S_mismatch` 0.20.
* `S_corpus` and `S_axis` are **macro-averaged F1** (not accuracy), so always-predict-majority submissions are not rewarded for the majority class alone.
* `S_class` is scored on **CLEAN rows only**; on intruder rows the underlying class is undefined.
* `S_radius` is a **Brier-style** squared-error term scaled by 40: a constant `pred_vol_radius = 0.5` predictor scores `S_radius ≈ 0`, and a prediction must be within ≈ 0.05 of the true extent to score ~0.9.

**Higher is better.** Minimum: 0.0, Maximum: 1.0.

A row that is missing entirely from the submission — or whose `id` does not appear in `test.csv` — causes the grader to return `0.0`. Likewise, the grader returns `0.0` if the submission contains duplicate `id`s, is missing any required column, or otherwise raises an exception during parsing.

**Predictions are validated strictly — malformed values are not silently coerced.** The submission format is fully specified, so a working solution always emits valid, in-domain values. To avoid masking solution bugs, the grader returns `0.0` for the **entire submission** if **any** predicted cell is invalid, namely:

* `pred_corpus_id` not an integer in `{0, 1, 2, 3, 4, 5}`;
* `pred_class_label` not a non-negative integer;
* `pred_vol_radius` not a finite float in `[0, 1]` (a tiny float-rounding epsilon is tolerated and then clamped to the interval);
* `pred_mismatched_triplet` not exactly `0` or `1`;
* `pred_mismatched_axis` not one of `NONE` / `AXIAL` / `SAGITTAL` / `CORONAL` (case-insensitive).

This replaces the earlier behaviour that coerced illegible cells to defaults; sloppy or corrupt output now fails fast rather than being smoothed over.

### Dataset

* `public/train/<id>_axial.png` — 28×28 grayscale axial mid-plane PNG.
* `public/train/<id>_sagittal.png` — 28×28 grayscale sagittal mid-plane PNG.
* `public/train/<id>_coronal.png` — 28×28 grayscale coronal mid-plane PNG.
* `public/test/<id>_{axial,sagittal,coronal}.png` — same layout for test rows.
* `public/train.csv` — labels for training rows: `true_corpus_id`, `true_class_label`, `true_vol_radius`, `true_mismatched_triplet`, `true_mismatched_axis`. Training labels for `true_class_label` carry irreducible noise.
* `public/test.csv` — the same `id` and three image-path columns for test rows. **No labels**.
* `public/sample_submission.csv` — one row per test `id` in the exact submission format. Shipped values are deliberately weak placeholders (`pred_corpus_id = 0`, `pred_class_label = 0`, `pred_vol_radius = 0.5`, `pred_mismatched_triplet = 0`, `pred_mismatched_axis = "NONE"`); participants must overwrite all five heads to score meaningfully.

Row counts are printed at the end of `prepare.py` (typical: ~7,800 train rows and ~2,200 test rows; one row = 3 PNGs + 1 CSV row).

#### File overview

| Item                          | Description                              |
|-------------------------------|------------------------------------------|
| `public/train/*.png`          | 28×28 grayscale per view, 3 per row      |
| `public/test/*.png`           | 28×28 grayscale per view, 3 per row      |
| `public/train.csv`            | Labels for training rows                 |
| `public/test.csv`             | Ids + image paths only, no labels        |
| `public/sample_submission.csv`| Submission template, full shape          |

#### Feature Details

The columns differ between the training CSV, the test CSV, and the submission CSV. They are listed separately so there is no ambiguity.

**Training data columns (`public/train.csv`) — 9 columns:**

Columns (in order): `id` (int, unique row identifier), `axial_path` (string, relative path to axial PNG), `sagittal_path` (string), `coronal_path` (string), `true_corpus_id` (int in 0–5), `true_class_label` (non-negative int), `true_vol_radius` (float in [0, 1]), `true_mismatched_triplet` (int 0 or 1), `true_mismatched_axis` (one of NONE / AXIAL / SAGITTAL / CORONAL).

| Column                     | Type   | Description                            |
|----------------------------|--------|----------------------------------------|
| `id`                       | int    | Unique row identifier                  |
| `axial_path`               | string | Relative path to axial PNG             |
| `sagittal_path`            | string | Relative path to sagittal PNG          |
| `coronal_path`             | string | Relative path to coronal PNG           |
| `true_corpus_id`           | int    | Anonymised corpus tag in {0..5}        |
| `true_class_label`         | int    | Within-corpus class id, non-negative   |
| `true_vol_radius`          | float  | Volumetric extent in [0, 1]            |
| `true_mismatched_triplet`  | int    | 1 if any view is an intruder, else 0   |
| `true_mismatched_axis`     | string | Intruder axis or "NONE"                |

**Test metadata columns (`public/test.csv`) — 4 columns:**

Columns (in order): `id` (int), `axial_path` (string), `sagittal_path` (string), `coronal_path` (string). No label column is present.

| Column           | Type   | Description                            |
|------------------|--------|----------------------------------------|
| `id`             | int    | Unique row identifier                  |
| `axial_path`     | string | Relative path to axial PNG             |
| `sagittal_path`  | string | Relative path to sagittal PNG          |
| `coronal_path`   | string | Relative path to coronal PNG           |

**Submission columns (`public/sample_submission.csv` and your final submission) — 6 columns:**

Columns (in order): `id` (int, same set as `public/test.csv`), `pred_corpus_id` (int in 0–5), `pred_class_label` (non-negative int), `pred_vol_radius` (float in [0, 1]), `pred_mismatched_triplet` (int 0 or 1), `pred_mismatched_axis` (one of NONE / AXIAL / SAGITTAL / CORONAL).

| Column                    | Type   | Constraint                              |
|---------------------------|--------|-----------------------------------------|
| `id`                      | int    | Same set as `public/test.csv`           |
| `pred_corpus_id`          | int    | Integer in {0, 1, 2, 3, 4, 5}           |
| `pred_class_label`        | int    | Non-negative integer                    |
| `pred_vol_radius`         | float  | In `[0, 1]` (clipped at grade time)     |
| `pred_mismatched_triplet` | int    | Binary 0 or 1                           |
| `pred_mismatched_axis`    | string | One of NONE / AXIAL / SAGITTAL / CORONAL|

### Submission

Submit a CSV file with **exactly one row per `id` in `test.csv`**, a header row, and the 6 columns above:

| Column                    | Type   | Description                              |
|---------------------------|--------|------------------------------------------|
| `id`                      | int    | Identifier from `test.csv`               |
| `pred_corpus_id`          | int    | Anonymised corpus prediction in {0..5}   |
| `pred_class_label`        | int    | Within-corpus class label, ≥ 0           |
| `pred_vol_radius`         | float  | Volumetric extent in `[0, 1]`            |
| `pred_mismatched_triplet` | int    | Binary intruder flag                     |
| `pred_mismatched_axis`    | string | NONE / AXIAL / SAGITTAL / CORONAL        |

**Requirements:**

* Header row plus exactly one row per `id` in `test.csv` — `id` must equal exactly the set in `test.csv`. Duplicate `id`s cause the grader to return `0.0`.
* `pred_corpus_id` must be an integer in `{0, 1, 2, 3, 4, 5}`. Any other value makes the whole submission score `0.0`.
* `pred_class_label` must be a non-negative integer. Negative or non-integer values make the whole submission score `0.0`.
* `pred_vol_radius` must be a finite float in `[0, 1]` (a tiny float-rounding epsilon is tolerated and clamped). Non-numeric or out-of-range values make the whole submission score `0.0`.
* `pred_mismatched_triplet` must be exactly `0` or `1`. Anything else makes the whole submission score `0.0`.
* `pred_mismatched_axis` must be one of the four strings `"NONE"`, `"AXIAL"`, `"SAGITTAL"`, `"CORONAL"` (case-insensitive). Anything else makes the whole submission score `0.0`.
* Missing rows are not silently filled in — a row-set mismatch causes the grader to return `0.0`.
* The grader returns `0.0` if any of the six required columns are missing from the submission, if the submission contains duplicate `id`s, or if it raises any exception during parsing.

**Validation is strict by design:** malformed predictions are never coerced to defaults, so confirm your output matches the documented domains before submitting.

**Example of a correctly formatted submission file (illustrative only):**

The three rows below come from three different test `id`s. The full submission has one row per test `id`. The placeholders show the column layout — real submissions will have informative per-row predictions.

```
id,pred_corpus_id,pred_class_label,pred_vol_radius,pred_mismatched_triplet,pred_mismatched_axis
9000,2,4,0.61,0,NONE
9001,5,0,0.34,1,SAGITTAL
9002,1,1,0.78,0,NONE
```

---

## 4) Tags

```
medical-imaging, computer-vision, 3d, multi-task, multi-head, multimodal
```

---

## 5) Grading Configuration

- **Scoring direction:** Higher is better
- **Theoretical minimum:** 0.0
- **Theoretical maximum:** 1.0

---

## 6) Grading Script

**Select:** `Custom`

See `PASTE_THIS_GRADE.txt` for the full script (identical to `grade.py` in this folder).

---

## 7) Prepare Script

**Select:** `Custom`

See `PASTE_THIS_PREPARE.txt` for the full script (identical to `prepare.py` in this folder).

---

## 8) GPU Tier

**Select:** **A10G** — 28×28 PNGs at ~10K rows is a tiny image-classification workload. A small three-tower ConvNet (one ResNet-blocks-stack per view) feeding into a shared MLP that fans out to the five heads trains end-to-end in single-digit GPU-hours on a 24 GB A10G. H100-class compute is not required.

---

## 9) Raw data upload notes (organiser only)

**License:** CC-BY 4.0 — select **Creative Commons → CC-BY 4.0** on the platform.

**Source attribution (CC-BY requirement):** Yang J., Shi R., Wei D., Liu Z., Zhao L., Ke B., Pfister H., Ni B. "MedMNIST v2 — A Large-Scale Lightweight Benchmark for 2D and 3D Biomedical Image Classification." Scientific Data, 2023. DOI: 10.1038/s41597-022-01721-8. Original release: https://zenodo.org/records/10519652

**Raw zip:** run `python generate.py --out raw_data` (downloads ~104 MB from Zenodo) then `python zip_raw_for_upload.py` → upload `VolumetricIdentity_RAW_upload.zip` (flat root: 6 `.npz` archives, ~104 MB).

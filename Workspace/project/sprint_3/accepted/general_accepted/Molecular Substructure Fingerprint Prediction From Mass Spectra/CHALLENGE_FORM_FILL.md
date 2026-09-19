# Challenge creation form — fill-in (paired with `DATASET_FORM_FILL.md`)

**Platform status:** **Draft**

---

## 1) Difficulty

**Select:** **Hard**

Solvers must read a tandem mass spectrum — a sparse list of fragment-ion `(m/z, intensity)` peaks — and produce **calibrated per-bit probabilities** for each of 512 molecular substructure bits, estimating how likely the unknown molecule is to contain each substructure. The training and test molecules share **no Bemis–Murcko scaffold**, so the dominant approach (matching the spectrum against a reference library) is defeated by construction. There is no public spectrum→structure foundation model to fine-tune. The molecular formula is withheld, and the proper scoring rule (Brier Skill Score) penalises both under-confident and over-confident predictions — the solver must genuinely calibrate its uncertainty about substructure presence under scaffold shift. This requires joint fragment-to-substructure reasoning with quantified uncertainty, which remains an open problem in computational metabolomics.

---

## 2) Challenge Title

```
Molecular Substructure Fingerprint Prediction From Mass Spectra
```

---

## 3) Problem Description

### Overview

# Molecular Substructure Fingerprint Prediction From Mass Spectra

You are given a **tandem mass spectrometry (MS/MS) spectrum** of a single unknown small molecule: a list of fragment-ion peaks, each a `(m/z, relative_intensity)` pair, together with the **precursor m/z**, the **adduct type** (e.g. `[M+H]+`, `[M-H]-`), and the **ion mode**. Your job is to produce **calibrated probability estimates** for each of **512 molecular substructure bits** — how likely is the molecule to contain each specific circular atom-environment substructure (Morgan / ECFP fingerprint of radius 2, folded to 512 bits)?

This is **not** standard binary fingerprint prediction. You must output a **probability** for each bit (a float in [0, 1]), and your predictions are evaluated with a **proper scoring rule** (the Brier Skill Score). This means:

* A solver that is confident and correct scores high.
* A solver that is confident and wrong scores very low (much worse than hedging).
* A solver that outputs the training marginal bit frequencies for every row (the "climatological" baseline) scores **near 0.0** — it matches the fixed reference by construction and adds no molecule-specific signal.
* Only solvers that learn molecule-specific substructure probabilities **better than the marginal baseline** score positively.

This breaks the standard "input → binary label" setup in three ways:

1. **Calibrated uncertainty output.** You predict 512 probabilities, not 512 hard bits. A neutral loss of 18 Da should increase your hydroxyl-group probability, but the magnitude depends on how diagnostic that loss is for the specific molecular context.
2. **Proper scoring rule evaluation.** The Brier Skill Score rewards calibration, not just discrimination. A model that outputs 0.99 for a bit that is wrong loses far more than one that outputs 0.55 — hedging is rational when evidence is ambiguous.
3. **Generalisation under scaffold shift.** The training and test molecules share **no common scaffold**. On novel scaffolds, a well-calibrated model should output moderate probabilities rather than blindly extrapolating high confidence from seen scaffolds.

The molecular formula is **not** provided — only the precursor m/z and adduct, exactly as in a real unknown-identification workflow. The displayed peaks have been processed (intensity renormalisation and jitter, small m/z jitter, low-intensity dropout, and a few inserted spurious peaks), so byte-level matching of the peak list against any external spectral record is not reliable.

**What Not To Do** (using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score):

* **Spectral-library / nearest-neighbour lookup.** Matching the provided spectrum against any external library of recorded spectra to retrieve a candidate structure or fingerprint — including CSI:FingerID-style or spectral-database-search pipelines — is disallowed.
* **External structure-database retrieval.** Looking up the precursor m/z / adduct against public compound databases to enumerate and rank candidate structures is disallowed. The predictions must be learned from `public/train.csv`.
* **Hosted / closed-source APIs** at any stage of training or inference (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.), including distillation / pseudo-labelling from such teachers. Only open-weights models and self-trained pipelines are permitted.
* **Pretrained spectrum→structure checkpoints** trained on overlapping public MS/MS collections. Generic ML libraries (RDKit for feature engineering on your own training data, scikit-learn, PyTorch, etc.) are fine.
* **Byte / hash lookup** of the peak list against public spectral records.
* **Filename / ordering side-channels.** Do not exploit `id` ordering, row order, or any signal outside the peak list and the precursor metadata columns.
* **Format / range hacks.** Submitting malformed probability strings or values engineered to exploit the grader's parsing or clipping behaviour.

### Evaluation

For each test row the solver submits **512 probability values** (one per substructure bit). The grader evaluates using the **Brier Skill Score (BSS)** — a proper scoring rule normalised against a **fixed climatological baseline derived from the training set**:

```
Brier score:  BS     = mean over all (row, bit) of (pred - true)^2
Fixed ref:    BS_ref = mean over bits j of  p_hat_train_j * (1 - p_hat_train_j)
              where p_hat_train_j is the marginal frequency of bit j on the
              TRAINING split (a constant, precomputed in prepare.py and embedded
              in grade.py as P_HAT_TRAIN — never the hidden test marginals).

BSS = clip(1 - BS / BS_ref, 0.0, 1.0)
```

* **Higher is better.** Minimum: 0.0, Maximum: 1.0.
* A perfect submission (predict p=1.0 for every set bit, p=0.0 for every unset bit on every row) scores `1.0`.
* The reference is a **static standard fixed at preparation time** from the training bit frequencies, so it cannot shift with the particular test rows being graded. Predicting the overall training marginal on every row (pure climatology) scores essentially `0.0`; the shipped sample submission uses a slightly richer conditional marginal (see below) and lands just above `0.0`. Solvers must learn molecule-specific probabilities to score meaningfully positive.
* Predicting a flat p=0.5 for all bits scores `0.0` (clipped from negative BSS).
* Overconfident wrong predictions (e.g. p=0.99 for a bit that is 0) dramatically increase BS, potentially pushing BSS below 0 → clipped to 0.
* The Brier Skill Score rewards calibration: outputting p=0.7 when a bit is set 70% of the time in similar molecules is optimal, rather than always guessing 1 or 0.

The grader returns `0.0` if the submission is missing any required column, contains duplicate `id`s, has an `id` set that does not match `test.csv`, or raises any exception. A `pred_probs` cell longer than 20,000 characters, malformed, or of the wrong length is treated as all-0.5 (uninformative) for that row.

### Dataset

* `public/train.csv` — one row per training spectrum: precursor metadata, the peak list, and the **true 512-bit binary fingerprint** label.
* `public/test.csv` — the same fields for test spectra, **without** the fingerprint label.
* `public/sample_submission.csv` — one row per test `id` in the exact submission format, pre-filled with a per-`(ion_mode, adduct, precursor-m/z bin)` training marginal (shrunk toward the overall training marginal). It uses only public metadata and scores just above BSS = 0.0 — a weak baseline participants must beat.
* `private/answers.csv` — the held-out true fingerprints (not shipped to participants).

Row counts are seed-dependent and printed at the end of `prepare.py` (typical: ~15,600 train rows and ~4,000 test rows). Train and test never share a molecular scaffold, so no molecule seen at test time — and no member of its scaffold family — appears in training.

#### File overview

| Item                          | Description                                    |
|-------------------------------|------------------------------------------------|
| `public/train.csv`            | Labelled training spectra (binary fingerprints)|
| `public/test.csv`             | Test spectra, no fingerprint label             |
| `public/sample_submission.csv`| Submission template (conditional marginal)     |

#### Feature Details

**Training data columns (`public/train.csv`) — 7 columns:**

Columns (in order): `id` (int, unique row identifier), `adduct` (string, e.g. `[M+H]+`), `ion_mode` (string, `POSITIVE`/`NEGATIVE`), `precursor_mz` (float), `n_peaks` (int, number of peaks in the list), `peaks` (string, `m/z,intensity` pairs separated by `;`), `fingerprint` (string label: the letter `b` followed by 512 `0`/`1` characters).

| Column         | Type   | Description                          |
|----------------|--------|--------------------------------------|
| `id`           | int    | Unique row identifier                |
| `adduct`       | string | Precursor adduct type                |
| `ion_mode`     | string | `POSITIVE` or `NEGATIVE`             |
| `precursor_mz` | float  | Precursor ion m/z                    |
| `n_peaks`      | int    | Number of peaks in `peaks`           |
| `peaks`        | string | `m/z,intensity;…` ascending in m/z   |
| `fingerprint`  | string | `b` + 512 bits (the label)           |

Note: the training labels are **binary** fingerprints. The solver must learn to convert these into calibrated probabilities for test molecules it has never seen (and whose scaffolds never appear in training).

**Test metadata columns (`public/test.csv`) — 6 columns:**

| Column         | Type   | Description                          |
|----------------|--------|--------------------------------------|
| `id`           | int    | Unique row identifier                |
| `adduct`       | string | Precursor adduct type                |
| `ion_mode`     | string | `POSITIVE` or `NEGATIVE`             |
| `precursor_mz` | float  | Precursor ion m/z                    |
| `n_peaks`      | int    | Number of peaks in `peaks`           |
| `peaks`        | string | `m/z,intensity;…` ascending in m/z   |

**Submission columns (`public/sample_submission.csv` and your final submission) — 2 columns:**

Columns (in order): `id` (int, same set as `public/test.csv`), `pred_probs` (string: 512 float values separated by `;`, each in [0, 1]).

| Column       | Type   | Constraint                                            |
|--------------|--------|-------------------------------------------------------|
| `id`         | int    | Same set as `public/test.csv`                         |
| `pred_probs` | string | 512 floats separated by `;`, each in [0.0, 1.0]      |

### Submission

Submit a CSV file with a header row and **exactly one row per `id` in `test.csv`**. The header must contain these **2 columns in this order**: `id`, `pred_probs`.

| Column       | Type   | Description                                              |
|--------------|--------|----------------------------------------------------------|
| `id`         | int    | Identifier from `test.csv`                               |
| `pred_probs` | string | 512 predicted substructure probabilities, `;`-separated  |

**Requirements:**

* Header row plus exactly one row per `id` in `test.csv` — the `id` set must match exactly. Duplicate `id`s cause the grader to return `0.0`.
* `pred_probs` must be exactly **512** float values separated by semicolons (`;`). Each value is clipped to [0, 1] by the grader. Values are the solver's estimated probability that substructure bit *k* is present (Morgan / ECFP radius 2, 512-bit fold).
* A row whose `pred_probs` is blank, has wrong count, or contains non-numeric values is treated as all-0.5 (uninformative) for that row.
* The grader returns `0.0` if the `pred_probs` column is missing, if there are duplicate `id`s, or if the `id` set does not match `test.csv`.

**Example of a correctly formatted submission file (illustrative only):**

The three rows below come from three different test `id`s. The full submission has one row per test `id`. Each `pred_probs` value is exactly 512 semicolons-separated floats; the values are abbreviated with `…` here purely for display.

```
id,pred_probs
1000000,0.92;0.03;0.14;0.87;0.01;…;0.65;0.02
1000001,0.05;0.88;0.21;0.03;0.44;…;0.11;0.99
1000002,0.71;0.06;0.33;0.59;0.02;…;0.84;0.07
```

---

## 4) Tags

```
chemistry, mass-spectrometry, metabolomics, calibration, uncertainty-quantification, multi-label, proper-scoring-rules
```

---

## 5) Grading Configuration

- **Scoring direction:** Higher is better
- **Theoretical minimum:** 0.0
- **Theoretical maximum:** 1.0

---

## 6) Grading Script

**Select:** `Custom`

```python
# See PASTE_THIS_GRADE.txt for the full, identical grade.py source.
# Key properties:
#   * Brier Skill Score against a FIXED training-derived reference
#     (P_HAT_TRAIN, the per-bit training marginal embedded as a constant);
#     the reference never uses the hidden test marginals.
#   * BSS = clip(1 - BS / BS_ref, 0, 1); perfect submission -> 1.0,
#     pure-climatology -> ~0.0.
#   * pred_probs cells over 20,000 chars are rejected BEFORE the split (memory /
#     parse-cost bound); a malformed / wrong-length cell -> all-0.5 for that row.
#   * Returns 0.0 on missing column, duplicate ids, id-set mismatch, or any
#     exception (defensive contract).
```

---

## 7) Prepare Script

**Select:** `Custom`

The raw dataset is a single `spectra.csv` (canonical SMILES + adduct + precursor + peaks). `prepare.py` does ALL processing: it derives the ground-truth 512-bit Morgan fingerprint and the Bemis–Murcko scaffold per molecule, performs a scaffold-disjoint train/test split, applies mild per-row peak perturbation, and writes the public split, the submission template (with marginal-frequency probabilities), and the private answers. The full script is mirrored in `PASTE_THIS_PREPARE.txt` in this folder.

```python
# See PASTE_THIS_PREPARE.txt for the full, identical prepare.py source.
# Key properties enforced by the script:
#   * 512-bit Morgan/ECFP (radius 2) fingerprint per molecule (RDKit).
#   * Bemis-Murcko scaffold grouping; acyclic molecules grouped by SMILES.
#   * Scaffold-DISJOINT split: no scaffold appears in both train and test.
#   * Per-row-seeded peak perturbation (intensity renorm + jitter, m/z jitter,
#     low-intensity dropout, a few spurious peaks) -> lookup-resistant.
#   * Fingerprints written as 'b' + 512 bits (string-safe in CSV readers).
#   * Emits the overall training marginal (private/p_hat_train.txt) for embedding
#     into grade.py as the fixed P_HAT_TRAIN Brier reference.
#   * Sample submission = per-(ion_mode, adduct, precursor-m/z bin) training
#     marginal, shrunk toward the overall marginal (weak BSS ~ 0.02 baseline).
#   * Train/test indices are shuffled (seeded) before id assignment -> no row-order leak.
#   * Deterministic: byte-identical public/ and private/ across runs.
#   * Standard signature: prepare(raw: Path, public: Path, private: Path).
```

---

## 8) GPU Tier

**Select:** **A10G** — the workload is small and numeric: ~15,600 training rows, each a short peak list plus a 512-bit target. A solution that featurises peaks (binned m/z spectra, neutral-loss features) and trains a multi-label probabilistic model (gradient boosting with calibration or a small MLP with 512 sigmoid outputs + temperature scaling) runs in single-digit GPU-hours on a 24 GB A10G. H100-class compute is not required.

---

## 9) What Not To Use

Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score.

* **Spectral-library / nearest-neighbour lookup** of the provided spectrum against external recorded-spectrum collections (including CSI:FingerID-style fingerprint prediction backed by spectral search). The peaks are perturbed and test molecules share no scaffold with training; library transfer is unreliable and out of scope.
* **External compound-database retrieval** from precursor m/z / adduct to enumerate candidate structures and emit a retrieved fingerprint. The mapping must be learned from `public/train.csv`.
* **Hosted / closed-source APIs** (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.) at any stage, including distillation / pseudo-labelling from such teachers.
* **Pretrained spectrum→structure checkpoints** trained on overlapping public MS/MS collections. Generic libraries (RDKit, scikit-learn, PyTorch) used on your own training data are fine.
* **Byte / hash lookup** of the peak list against public spectral records.
* **Ordering / metadata side-channels** — `id` order and row order carry no signal.
* **Grader format hacks** — malformed probability strings or values engineered to exploit parsing / clipping.

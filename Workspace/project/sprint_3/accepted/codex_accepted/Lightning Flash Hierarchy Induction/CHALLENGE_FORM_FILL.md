# Challenge creation form - fill-in

## 1) Difficulty

Hard

## 2) Challenge Title

```
Lightning Flash Hierarchy Induction
```

## 3) Problem Description

# Lightning Flash Hierarchy Induction

## Overview

Your task is to recover the group-and-flash hierarchy of anonymized local lightning point sets. In plain language: decide which tiny satellite lightning detections happened together, which short-lived groups belong to the same larger flash, and which boundary detections are too ambiguous to assign with high certainty. Lightning flashes are not single points: a satellite records many tiny optical detections, nearby detections are combined into short-lived **groups**, and several groups can belong to the same larger **flash**.

Each row is one compact case containing real optical lightning detections after source-neutral redaction. The public features preserve local relative geometry, timing, energy rank, and neighborhood density while withholding absolute time, absolute location, source-object metadata, and operational identifiers. In difficult local windows, neighboring lightning activity can overlap in space and time, so the task is not just applying a fixed distance threshold.

This is a structured hierarchy problem, not one independent class prediction per detection. The output is a JSON hierarchy: detection-to-group partition, group-to-flash partition, optional boundary/ambiguous detections, and a confidence value.

Every solution must run on CPU. The execution environment provides 10 CPU cores and 62 GB RAM, with a maximum runtime of 1.5 hours. GPU/CUDA libraries and large pretrained models are neither required nor permitted as dependencies.

## Task

For each test case, infer the hidden two-level hierarchy from the public point-set evidence:

1. assign every detection id in the case to exactly one predicted group;
2. assign every predicted group to exactly one predicted flash;
3. mark detections whose membership is genuinely ambiguous under the redacted local evidence;
4. report a confidence value estimating your row-level structural quality.

Your group and flash names are local aliases. They do not need to match training aliases or hidden native labels. The grader compares the implied partitions, not the literal strings.

## Generalization Contract

Train and test cases come from disjoint source windows, so related lightning activity is not split between public training rows and private scoring rows. Public ids are opaque, rows are sorted by opaque id, and the test set does not provide source-window labels or operational sequence context.

A successful solution should learn reusable local hierarchy cues: how relative time, local geometry, energy rank, and point density interact when groups merge into flashes or when neighboring flashes overlap. It should not rely on knowing where or when the original satellite observations occurred.

## Intended Approach And Allowed Methods

Strong CPU solutions can train compact models directly on the provided `train.csv` cases. Reasonable approaches include:

- pairwise same-group and same-flash classifiers over detection pairs, followed by a consistency-aware clustering or graph-partition decoder;
- permutation-invariant point-set models such as Deep Sets, Set Transformer-style blocks small enough for CPU, or message-passing networks over k-nearest-neighbor graphs built from the public features;
- multi-head training that predicts group affinity, flash affinity, boundary ambiguity, and confidence/calibration from training labels only;
- train-only validation splits by case or source-neutral case properties to tune thresholds, clustering regularization, and confidence calibration;
- deterministic post-processing that repairs invalid partitions, as long as the learned point-set evidence remains the primary signal.

Simple geometric clustering, DBSCAN-like rules, or operational-threshold surrogates may be useful as diagnostic baselines, but they are not sufficient as the primary intended solution. The challenge rewards learned hierarchy induction under redaction and overlap, not reconstruction of a known operational algorithm.

Allowed tooling is ordinary offline CPU machine learning on the released public files: NumPy, pandas, scikit-learn, PyTorch/JAX/TensorFlow CPU builds, LightGBM/XGBoost, custom clustering decoders, and similar open-source local libraries. External raw-source lookup, private files, hosted closed-source APIs, and GPU-only dependencies are out of scope.

## What Not To Use

- Do not use source-object or archive lookup, reconstructed absolute time/location, native clustering identifiers, filename or scan matching, external operational neighbors, private files, answer dictionaries, hard-coded public ids, or native hierarchy traversal.
- Do not use row order, opaque-id hashes, CSV/JSON byte length, filesystem metadata, or other non-physical metadata as a substitute for point-set inference.
- Do not use published fixed clustering thresholds, DBSCAN-only or rule-only pipelines, TF-IDF, n-grams, regex-only logic, metadata-only priors, hosted closed-source APIs, GPU-only methods, or grader/platform exploitation as the primary solution.

Enforcement on Invalid Approaches: a submission may be rejected before payout if it is built around prohibited lookup, private-data access, platform exploitation, hard-coded ids, native graph traversal, or a rule-only shortcut that bypasses the intended public point-set inference, even if it obtains a leaderboard score.

## Evaluation

The metric is label-invariant. For a hierarchy, let `P_group` be the set of unordered detection pairs placed in the same group and let `P_flash` be the set of unordered detection pairs placed in the same flash. For a predicted count `n_pred` and true count `n_true`, define `C(n_pred,n_true) = min(n_pred,n_true) / max(n_pred,n_true)`. Define:

- `S_group`: pair F1 between predicted and true `P_group`, multiplied by `C(predicted group count,true group count)`;
- `S_flash`: pair F1 between predicted and true `P_flash`, multiplied by `C(predicted flash count,true flash count)`;
- `S_uncertain`: set F1 for `uncertain_detections`;
- `S_exact`: 1 only when both partitions and the uncertainty set are completely correct, up to arbitrary group/flash aliases, and 0 otherwise.

When both compared pair sets are empty, their F1 is 1. The uncalibrated structural quality used as the confidence target is

`Q = (0.55*S_group + 0.10*S_flash + 0.15*S_uncertain + 0.15*S_exact) / 0.95`.

This `Q` value is normalized to `[0,1]` only so confidence has a comparable target. Calibration is `S_cal = 1 - abs(confidence - Q)`. The final row score then uses the raw structural credit plus the calibration term:

`0.55*S_group + 0.10*S_flash + 0.15*S_uncertain + 0.15*S_exact + 0.05*S_cal`.

The final score is the mean row score. Higher is better; the theoretical minimum is `0.0` and maximum is `1.0`. A perfect hierarchy with confidence `1.0` scores exactly `1.0`.

Submission-level schema failures receive score `0.0`: missing, extra, or reordered columns; missing, extra, or duplicate ids; non-string/empty ids; row-set mismatch; and non-finite or out-of-range confidence. `prediction_json` is limited to 200,000 characters. Malformed or structurally invalid JSON affects that row only and scores zero rather than crashing the grader or exposing private information.

## Dataset

The public dataset contains 210 labeled training cases and 140 unlabeled test cases. Related source windows are never split across train and test. Rows and embedded detections are sorted by opaque ids. Public data contains no native filenames, absolute timestamps, coordinates, scan identifiers, event/group/flash identifiers, or source-window labels.

| Item | Description |
|---|---|
| `train.csv` | Labeled public cases |
| `test.csv` | Public cases without labels |
| `sample_submission.csv` | Valid weak structured submission |

In prose: `train.csv` contains the public input for each training case plus its hidden hierarchy label; `test.csv` contains the same public input columns but no label column; `sample_submission.csv` shows the exact required output columns and a weak valid JSON structure.

### train.csv columns

| Column | Type | Description |
|---|---|---|
| `id` | string | Opaque case id |
| `case_json` | JSON string | Case id and detection point set |
| `prompt` | string | Row instruction |
| `target_json` | JSON string | Training hierarchy and ambiguity labels |

The `train.csv` columns are: `id`, an opaque case identifier; `case_json`, a JSON string containing the local detection point set; `prompt`, the row-specific instruction text; and `target_json`, the training-only hierarchy label with groups, flashes, and uncertain detections.

### test.csv columns

| Column | Type | Description |
|---|---|---|
| `id` | string | Opaque case id |
| `case_json` | JSON string | Case id and detection point set |
| `prompt` | string | Row instruction |

The `test.csv` columns are: `id`, an opaque case identifier; `case_json`, a JSON string containing the local detection point set; and `prompt`, the row-specific instruction text. There is no `target_json` column in `test.csv`.

Each `case_json` has a `case_id` matching the CSV `id` and a `detections` list. Each detection contains:

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Opaque detection id |
| `x_rel` | float | Local horizontal coordinate |
| `y_rel` | float | Local vertical coordinate |
| `t_rel` | float | Normalized relative timing coordinate |
| `energy_norm` | float | Within-case normalized optical-energy rank |
| `local_density` | float | Local neighbor fraction |
| `temporal_density` | float | Temporal neighbor fraction |

The detection-level fields inside `case_json` are: `id` for the opaque detection id, `x_rel` and `y_rel` for local normalized geometry, `t_rel` for normalized relative timing, `energy_norm` for within-case optical-energy rank, `local_density` for nearby spatial crowding, and `temporal_density` for nearby temporal crowding.

`target_json` and submitted `prediction_json` use the same exact structure:

```json
{
  "groups": [
    {"group_id": "g1", "detections": ["d01", "d02"]},
    {"group_id": "g2", "detections": ["d03"]}
  ],
  "flashes": [
    {"flash_id": "f1", "groups": ["g1", "g2"]}
  ],
  "uncertain_detections": ["d03"]
}
```

Every detection must occur in exactly one non-empty group. Group ids must be unique. Every group must occur in exactly one non-empty flash, and flash ids must be unique. `uncertain_detections` must contain unique detection ids from the case; an empty list is valid. Alias strings may differ from the training aliases.

In `test.csv`, `id`, `case_json`, and `prompt` are the complete public input columns; no label column is present.

## Submission

Submit one CSV at `./working/submission.csv` with exactly these columns in exactly this order: `id`, `prediction_json`, `confidence`.

| Column | Type | Constraint |
|---|---|---|
| `id` | string | Must exactly match the test id set |
| `prediction_json` | JSON string | Complete valid hierarchy for the case |
| `confidence` | float | Estimate of `Q` in `[0,1]` |

Example:

```csv
id,prediction_json,confidence
case_a1b2c3,"{""groups"":[{""group_id"":""g1"",""detections"":[""d01"",""d02""]},{""group_id"":""g2"",""detections"":[""d03""]}],""flashes"":[{""flash_id"":""f1"",""groups"":[""g1"",""g2""]}],""uncertain_detections"":[""d03""]}",0.64
case_d4e5f6,"{""groups"":[{""group_id"":""g1"",""detections"":[""d01""]},{""group_id"":""g2"",""detections"":[""d02"",""d03""]}],""flashes"":[{""flash_id"":""f1"",""groups"":[""g1""]},{""flash_id"":""f2"",""groups"":[""g2""]}],""uncertain_detections"":[]}",0.41
```

## 4) Tags

`structured-prediction`, `point-sets`, `clustering`, `earth-science`, `uncertainty`, `small-data`

## 5) Grading Configuration

Direction: Maximize

Theoretical minimum: `0.0`

Theoretical maximum: `1.0`

## 6) Grading Script

Select Custom and paste the exact contents of `PASTE_THIS_GRADE.txt`.

## 7) Prepare Script

Paste the exact contents of `PASTE_THIS_PREPARE.txt`.

## 8) GPU Tier

CPU only

## 9) What Not To Use

Do not use source lookup, absolute time/location reconstruction, native ids or hierarchy traversal, filename/scan matching, row order, opaque-id hashes, file/JSON length, filesystem metadata, external operational neighbors, private files, answer dictionaries, fixed-threshold or DBSCAN-only pipelines, TF-IDF/n-grams/regex-only logic, metadata-only priors, hosted closed-source APIs, GPU-only dependencies, or grader/platform exploitation.

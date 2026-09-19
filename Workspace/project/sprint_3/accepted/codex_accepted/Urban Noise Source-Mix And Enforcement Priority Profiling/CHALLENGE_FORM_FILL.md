# Challenge creation form - fill-in

## Difficulty

Hard

## Challenge Title

Urban Noise Source-Mix And Enforcement Priority Profiling

## Problem Description

Urban noise monitoring teams do not only need to know whether a sound tag is present. They need a compact view of the source mixture, whether the event looks like traffic, construction, social sound, animal/other impact, or alert activity, and how urgently a nuisance or enforcement follow-up should be prioritized.

### Overview

You are given short real urban acoustic-monitor WAV clips with opaque ids and no source metadata. For each test clip, predict a source-mix profile over broad source families, the dominant source family, a nuisance pattern, an enforcement-priority tier, and a calibrated confidence value.

The task is not a plain urban sound tagging benchmark. A useful model must summarize mixtures and triage follow-up priority from audio evidence, including construction machinery, saw-like activity, alert signals, engines, music, human voice, dogs, and other impact sounds. The public test rows do not expose original filenames, sensor ids, source split labels, annotator ids, location/time fields, row order, or source annotation columns.

What not to use: external source-corpus lookup, public annotation search, audio fingerprinting against the upstream recordings, row-order or filename side channels, recovered sensor/time/location metadata, hosted commercial audio-tagging APIs, hardcoded id-to-answer maps, manual labeling of hidden test rows, or grader/filesystem exploitation are prohibited. The intended route is to train a CPU-compatible audio model or audio-feature model from the public training examples.

### Task Specification

`source_mix_json` is a JSON object with exactly these eight keys: `engine`, `machinery_impact`, `powered_saw`, `alert_signal`, `music`, `human_voice`, `dog`, and `other_impact`. Each value must be a numeric source-strength estimate in `[0,1]`.

`dominant_source` is one of `engine`, `machinery_impact`, `powered_saw`, `alert_signal`, `music`, `human_voice`, `dog`, `other_impact`, or `mixed_uncertain`.

`enforcement_priority` is one of `low`, `moderate`, `high`, or `urgent`. The priority reflects the nuisance/enforcement profile implied by the source mix, fine-source severity, proximity evidence, and label reliability conventions learned from training data.

`nuisance_pattern` is one of `traffic_dominant`, `construction_dominant`, `alert_dominant`, `social_music_voice`, `animal_or_other`, or `mixed_uncertain`.

`confidence` is a float in `[0,1]` estimating the reliability of the submitted row-level profile.

## Dataset

The public dataset contains `train.csv`, `test.csv`, `sample_submission.csv`, and WAV clips under `train/audio/` and `test/audio/`. Audio paths are relative to the `public/` directory. Prepared public WAVs are 16 kHz mono clips with opaque filenames and no source-identifying path tokens.

### Public Files

| Item | Description |
|---|---|
| `train.csv` | labeled training rows |
| `test.csv` | hidden-label rows |
| `sample_submission.csv` | valid dummy template |
| `train/audio/` | train WAV clips |
| `test/audio/` | test WAV clips |

`train.csv` has 701 rows and `test.csv` has 299 rows in this prepared split.

### train.csv Columns

| Column | Type | Description |
|---|---|---|
| `id` | string | opaque clip id |
| `audio_path` | string | relative WAV path |
| `clip_duration_s` | float | public clip length |
| `monitoring_context` | string | generic context |
| `source_mix_json` | JSON string | source strengths |
| `dominant_source` | string | dominant source |
| `enforcement_priority` | string | priority tier |
| `nuisance_pattern` | string | pattern label |
| `confidence` | float | label reliability |

The train-only label columns are `source_mix_json`, `dominant_source`, `enforcement_priority`, `nuisance_pattern`, and `confidence`; these are withheld from `test.csv`.

### test.csv Columns

| Column | Type | Description |
|---|---|---|
| `id` | string | opaque clip id |
| `audio_path` | string | relative WAV path |
| `clip_duration_s` | float | public clip length |
| `monitoring_context` | string | generic context |

`test.csv` contains only public inputs. It does not include source filenames, sensor ids, exact time/location fields, original split labels, annotator ids, annotation columns, hidden group labels, or target values.

In prose, `test.csv` contains `id`, `audio_path`, `clip_duration_s`, and `monitoring_context`.

### Submission Format

| Column | Type | Constraint |
|---|---|---|
| `id` | string | exact test id |
| `source_mix_json` | JSON object | exact 8 keys |
| `dominant_source` | string | allowed label |
| `enforcement_priority` | string | allowed tier |
| `nuisance_pattern` | string | allowed pattern |
| `confidence` | float | 0 to 1 |

Submit exactly one row for every test id, with the columns in the exact order shown above. JSON key order is not scored, but the key set and numeric range are required.

In prose, `sample_submission.csv` contains `id`, `source_mix_json`, `dominant_source`, `enforcement_priority`, `nuisance_pattern`, and `confidence`, and the final submission must use the same columns in the same order.

Example submission rows:

| id | source_mix_json | dominant_source | enforcement_priority | nuisance_pattern | confidence |
|---|---|---|---|---|---|
| `un_01a70d37a94af6` | `{"engine":0.2,...}` | alert_signal | high | alert_dominant | 0.50 |
| `un_01f4ddc7ae778b` | `{"engine":0.2,...}` | alert_signal | high | alert_dominant | 0.50 |
| `un_02182fb9b31e8e` | `{"engine":0.2,...}` | alert_signal | high | alert_dominant | 0.50 |

### Evaluation

Structural invalid submissions are rejected. Structural invalidity includes missing, extra, or reordered columns; duplicate ids; an id set different from `test.csv`; NaN values; non-finite confidence; and confidence outside `[0,1]`. Oversized row-local JSON or categorical strings are also rejected. A row-local malformed `source_mix_json` value, wrong JSON key set, nonnumeric mix value, invalid dominant source, invalid priority, or invalid nuisance string receives zero for that affected head without crashing the grader.

For each row, `MixScore = max(0, 1 - RMSE(predicted source mix, true source mix) / 0.35)`. `DominantScore` is exact-match correctness for `dominant_source`. `PriorityScore` gives full credit for the exact enforcement tier and partial credit for one-tier or two-tier distance on the ordered scale `low < moderate < high < urgent`. `NuisanceScore` is exact-match correctness for `nuisance_pattern`. `ConfidenceScore = max(0, 1 - abs(predicted confidence - target confidence) / 0.5)` multiplied by the row's non-confidence core quality, so confidence cannot rescue a row whose substantive profile is wrong.

The row score is `0.38*MixScore + 0.16*DominantScore + 0.22*PriorityScore + 0.16*NuisanceScore + 0.08*ConfidenceScore^2`.

The final score is `0.58*mean(RowScore) + 0.14*mean(MixScore) + 0.08*macroF1(DominantSource) + 0.10*macroF1(EnforcementPriority) + 0.05*macroF1(NuisancePattern) + 0.05*WorstHiddenGroup`. Hidden groups cover priority tier, nuisance pattern, broad source family, source-pressure band, and mixture-complexity band. These hidden axes are not public because they would leak target information, but they ensure a solution works beyond the easiest traffic or social-noise cases.

The theoretical minimum is `0.0`, the theoretical maximum is `1.0`, and higher is better. A perfect submission with all hidden labels and target confidence values scores exactly `1.0`.

### Intended Solution

Strong solutions should run within the CPU-only environment by computing compact audio representations from the public WAV clips and training calibrated lightweight models such as regularized linear models, tree ensembles, nearest-neighbor models over audio embeddings, or small CPU-trained spectrogram models. The public split is intentionally small enough for 10 CPU cores and 62 GB RAM within a 1.5 hour solution limit.

### Enforcement On Invalid Approaches

Submissions based on source-corpus lookup, recovered original annotations, audio fingerprint matching, sensor/time/location reconstruction, hosted commercial audio-tagging APIs, row-order/id/path side channels, hardcoded answer maps, manual hidden-test labeling, or grader/filesystem exploitation may be rejected before payout even if the CSV is structurally valid. The competition rewards learned urban-audio source-mix and triage modeling from the provided public training data.

This is not a single-label classifier, a plain upstream tag-vector task, or a canonical urban sound tagging benchmark with renamed columns. Final submissions must estimate continuous source-family strengths, nuisance/priority decisions, and calibrated reliability for each mixture; reducing the task to only a class label or the original sound-tag taxonomy is an invalid task framing.

## Tags

audio, urban-sound, environmental-monitoring, cpu, calibration

## Grading Configuration

Grade direction: Maximize

Theoretical minimum: 0.0

Theoretical maximum: 1.0

## Grading Script

Use `PASTE_THIS_GRADE.txt`.

## Prepare Script

Use `PASTE_THIS_PREPARE.txt`.

## GPU Tier

CPU only: 10 CPU cores, 62 GB RAM, 1.5 hour solution limit.

## What Not To Use

Do not use external source lookup, public annotation search, upstream audio fingerprinting, hosted commercial audio-tagging APIs, sensor/time/location reconstruction, original filename or row-order side channels, manual labeling, hardcoded id-to-answer maps, single-label-only classification, canonical upstream tag-vector prediction, or grader/filesystem exploitation.

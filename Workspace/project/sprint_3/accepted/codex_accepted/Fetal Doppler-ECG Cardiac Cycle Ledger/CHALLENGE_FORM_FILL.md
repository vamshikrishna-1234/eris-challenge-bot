# Challenge creation form - fill-in

**Platform status:** **Draft**

---

## 1) Difficulty

**Select:** **Hard**

This is a CPU-only multimodal medical signal challenge. Solvers must align a Doppler strip image with multichannel ECG and maternal respiration, then produce a structured fetal cardiac-cycle evidence ledger rather than a single heart-rate number. A fetal QRS detector, a Doppler envelope extractor, or a metadata lookup is not sufficient because the score combines event timing, cycle boundaries, envelope geometry, quality flags, calibration, and hidden subgroup robustness.

---

## 2) Challenge Title

```text
Fetal Doppler-ECG Cardiac Cycle Ledger
```

---

## 3) Problem Description

# Fetal Doppler-ECG Cardiac Cycle Ledger

## Overview

Plain language objective: for each six-second antenatal recording segment, infer the fetal cardiac cycles that are supported by both the Doppler strip image and the synchronized physiological signals, then submit a compact clinical-style ledger for that row.

Each public row contains two aligned inputs. The `image` file is a 512 x 192 Doppler ultrasound strip crop that shows the row-local velocity trace morphology. The `signal_npy` file is a 10 x 1536 float32 signal array sampled at 256 Hz over the same six seconds: six abdominal ECG channels, three thoracic maternal ECG channels, and one maternal respiration channel. A correct prediction identifies the fetal beat/evidence time for each cycle, the start and end of that cycle, the Doppler envelope bounds visible in the strip, whether each cycle is clinically usable or uncertain, and a row-level confidence value.

The raw corpus behind the challenge contains roughly sixty antenatal recording sessions from about forty pregnant volunteers. The prepared challenge turns those sessions into hundreds of short row-local examples. The public view preserves the clinical morphology needed for multimodal modeling while removing direct source identifiers and simple byte-size/source-file matching cues. The original record number, source filename, subject/session identity, and exact source time are not public. The target ledger is derived from agreement and disagreement between Doppler-trace evidence and signal evidence, so ignoring either modality should leave accuracy and quality-flag headroom.

For every test row, predict:

1. `ledger_json`: a JSON list of cycle objects. Each object has row-local seconds `t`, `start`, and `end`, where `t` is the fetal beat/evidence time and `start`/`end` bound the cardiac cycle.
2. `envelope_json`: a Doppler evidence envelope array with rows `[x, lower_y, upper_y]`, all normalized to `[0, 1]`.
3. `quality_json`: one quality flag per predicted cycle, using `usable`, `uncertain`, or `artifact`.
4. `confidence`: your calibrated probability in `[0, 1]` that the row-level ledger is correct.

This is a CPU-only challenge. Solutions must run within 1.5 hours on 10 CPU cores and 62 GB RAM. No GPU is required or allowed for the official run. A reasonable approach is a compact CPU pipeline: image filtering for Doppler envelopes, signal-processing features from abdominal/thoracic channels, respiration-aware artifact handling, and a structured decoder for cycle events and uncertainty.

Train and validate only from the provided public challenge files. The private test rows are grouped so that solutions must generalize across unseen source recordings and across rows with different signal quality, respiration interference, and Doppler visibility. The task remains learnable from the training examples because the same physical relationship between Doppler strip morphology, fetal/maternal electrophysiology, and cycle timing is present in both splits; what changes is the row, record context, and artifact mix.

## Task

Build a multimodal cardiac-cycle ledger for each unseen segment. The submitted ledger should identify row-local fetal cardiac-cycle evidence times, mark cycle start and end boundaries, attach a Doppler envelope trace, label whether each predicted cycle is usable, uncertain, or artifact-dominated, and calibrate row-level confidence. The output is intentionally structured because the useful clinical question is not only "what is the fetal heart rate?", but which cycles are supported by which sensor evidence and which cycles should be treated cautiously.

## Intended Approach

Strong CPU-only solutions will likely combine image and signal evidence rather than solve a single subproblem. Useful ingredients include classical Doppler-strip preprocessing, ridge/envelope extraction, robust peak proposals, band-limited ECG features, multi-channel agreement checks, respiration/motion artifact features, compact tree/linear/gradient-boosted models, sequence decoding, and train-only calibration. Offline open-source libraries such as NumPy, SciPy, scikit-image, OpenCV, scikit-learn, WFDB readers, and small CPU-trained models are appropriate. Any auxiliary pretrained component must be usable fully offline within the public environment and may not depend on hosted inference or external source-row lookup.

## What Not To Do

Using any of the approaches below is grounds for rejection on review, regardless of leaderboard score.

* Do not reduce the task to fetal heart-rate regression, fetal QRS detection, or a single Doppler envelope extraction.
* Do not use source-row lookup, raw record-id reconstruction, original source filenames, source start times, hidden source metadata, or source checksums to recover answers.
* Do not hardcode row ids, file ordering, file sizes, mtimes, or split-specific rules.
* Do not use external APIs, hosted LLMs, hosted vision models, or closed remote inference services.
* Do not train or infer from data outside the public challenge files except generally available offline open-source tools.
* Do not read private files, exploit the grader, or build a direct formula from hidden preparation details.
* Do not submit malformed JSON, negative times, impossible cycle boundaries, overlong arrays, or out-of-range confidence values as a format hack.

Enforcement on invalid approaches: submissions that score by lookup, metadata reconstruction, private-file access, external hosted models, or rule-only shortcuts that ignore the multimodal ledger task may be rejected even if the CSV passes the grader.

## Evaluation

The primary metric is **Mean Robust Ledger Score**. Each row receives a score in `[0, 1]`, then the leaderboard blends the mean row score with three private worst-axis terms: cycle-count regime, respiration motion, and Doppler-envelope visibility.

Events are matched greedily by absolute beat/evidence time error. A predicted cycle can match at most one reference cycle, and a reference cycle can match at most one predicted cycle. A match is allowed only when `abs(pred_t - true_t) <= 0.08` seconds. Event precision or recall with a zero denominator is treated as `0.0`.

Per row:

```
precision      = matched_events / predicted_events
recall         = matched_events / reference_events
event_score    = F1(precision, recall), or 0 if no events can be matched

timing_score   = mean over matched events of max(0, 1 - abs(pred_t - true_t) / 0.08)
boundary_score = mean over matched events of
                 max(0, 1 - (abs(pred_start - true_start) + abs(pred_end - true_end)) / 0.16)

raw_envelope_score = compare submitted and reference lower/upper envelopes at
                     64 evenly spaced x positions in [0, 1]:
                     mae = mean(abs(pred_lower - true_lower) + abs(pred_upper - true_upper)) / 2
                     raw_envelope_score = clip(1 - mae / 0.22, 0, 1)
envelope_score     = event_score * raw_envelope_score

quality_score  = mean matched-cycle flag agreement:
                 exact flag match = 1.0,
                 usable/uncertain confusion = 0.5,
                 artifact mismatch = 0.0,
                 and 0.0 if no events match
count_score    = event_score * max(0, 1 - abs(predicted_count - reference_count) / max(1, reference_count))

correctness = 0.40 event_score
            + 0.16 timing_score
            + 0.12 boundary_score
            + 0.17 envelope_score
            + 0.10 quality_score
            + 0.05 count_score

confidence_factor = 1 - 0.08 * abs(confidence - correctness)
row_score         = correctness * confidence_factor
```

Final score:

```
Final = 0.70 * mean(row_score)
      + 0.12 * lowest cycle-count subgroup mean
      + 0.10 * lowest respiration-motion subgroup mean
      + 0.08 * lowest Doppler-visibility subgroup mean
```

The three subgroup terms are distinct. The `0.12` term is the lowest mean score across private cycle-count regimes, the `0.10` term is the lowest mean score across private respiration-motion regimes, and the `0.08` term is the lowest mean score across private Doppler-visibility regimes. These subgroup labels correspond to real prepared acquisition/quality axes, so a solution must work on difficult rows rather than only on clean strips.

The envelope, quality, and count heads are gated by event recovery, so a row cannot score highly by submitting a plausible-looking envelope or fixed count without matching cardiac-cycle events. Confidence only modulates earned task credit and never adds standalone points to a wrong row.

The grader returns `0.0` for structural submission errors: missing, extra, or reordered columns; duplicate ids; row-set mismatch; non-integer ids; non-finite or out-of-range confidence. Row-local malformed JSON, negative times, impossible boundaries, overlong arrays, and invalid quality flags set that row's score to `0.0` instead of leaking labels or crashing.

Higher is better. Theoretical minimum: `0.0`. Theoretical maximum: `1.0`.

## Dataset

The public data contains transformed row-local segments only. It does not expose original raw record ids, source filenames, subject/session identifiers, raw start times, split groups, private answer metadata, or compressed file-size encodings of source rows. Each row is one six-second segment. Typical prepared splits contain hundreds of rows; the exact counts are printed by `prepare.py` after it processes the official raw files.

`train.csv` includes the input columns `id`, `image`, `signal_npy`, `segment_duration_sec`, `n_signal_channels`, `signal_fs_hz`, and `prompt`. It also includes the train-only labels `ledger_json`, `envelope_json`, and `quality_json`. `test.csv` has the same input columns and no label columns. `sample_submission.csv` is a valid weak placeholder template and should be overwritten.

### File overview

| Item | Description |
|---|---|
| `public/train/strips/*.bmp` | Doppler strip crops |
| `public/test/strips/*.bmp` | Test strip crops |
| `public/train/signals/*.npy` | Train signal snippets |
| `public/test/signals/*.npy` | Test signal snippets |
| `public/train.csv` | Inputs plus labels |
| `public/test.csv` | Inputs only |
| `public/sample_submission.csv` | Submission template |

### train.csv columns

| Column | Type | Description |
|---|---|---|
| `id` | int | Opaque segment id with no source-row meaning |
| `image` | string | 512 x 192 BMP strip path |
| `signal_npy` | string | 10 x 1536 float32 NPY path |
| `segment_duration_sec` | float | Segment duration in seconds |
| `n_signal_channels` | int | Public channel count |
| `signal_fs_hz` | float | Public sample rate in Hz |
| `prompt` | string | Constant task text |
| `ledger_json` | string | Train-only cycle list |
| `envelope_json` | string | Train-only envelope |
| `quality_json` | string | Train-only cycle flags |

### test.csv columns

| Column | Type | Description |
|---|---|---|
| `id` | int | Opaque segment id with no source-row meaning |
| `image` | string | 512 x 192 BMP strip path |
| `signal_npy` | string | 10 x 1536 float32 NPY path |
| `segment_duration_sec` | float | Segment duration in seconds |
| `n_signal_channels` | int | Public channel count |
| `signal_fs_hz` | float | Public sample rate in Hz |
| `prompt` | string | Constant task text |

### signal_npy channel order

Every public `signal_npy` array has shape `(10, 1536)`. Rows are channels and columns are samples.

| Channel index | Channel name | Meaning |
|---|---|---|
| 0 | `uni_abd1` | Abdominal ECG/electrophysiology channel |
| 1 | `uni_abd4` | Abdominal ECG/electrophysiology channel |
| 2 | `uni_abd8` | Abdominal ECG/electrophysiology channel |
| 3 | `uni_abd12` | Abdominal ECG/electrophysiology channel |
| 4 | `uni_abd16` | Abdominal ECG/electrophysiology channel |
| 5 | `uni_abd20` | Abdominal ECG/electrophysiology channel |
| 6 | `bi_tho1` | Thoracic maternal ECG channel |
| 7 | `bi_tho2` | Thoracic maternal ECG channel |
| 8 | `bi_tho3` | Thoracic maternal ECG channel |
| 9 | `matrsp` | Maternal respiration channel |

The `image` and `signal_npy` paths are relative to `public/`. The `prompt` value is the same task instruction on every row and contains no hidden metadata or answer text.

`ledger_json` is a JSON list of objects such as `{"t": 1.24, "start": 1.02, "end": 1.48}`. All times are row-local seconds inside `[0, segment_duration_sec]`, and each object represents one predicted or reference cardiac cycle. `envelope_json` is a JSON list of normalized triples `[x, lower_y, upper_y]`; `x` is horizontal position across the strip, while `lower_y` and `upper_y` bound the visible Doppler evidence band. `quality_json` is aligned to the cycle list: `usable` means the cycle is supported clearly enough for clinical-style use, `uncertain` means the cycle has partial or conflicting image/signal evidence, and `artifact` means the proposed cycle is dominated by artifact or weak evidence.

## Submission

Submit `./working/submission.csv` with a header row and exactly one row per `id` in `test.csv`. The header must contain these five columns in this exact order: `id`, `ledger_json`, `envelope_json`, `quality_json`, `confidence`.

| Column | Type | Constraint |
|---|---|---|
| `id` | int | Same set as test |
| `ledger_json` | string | JSON cycle list |
| `envelope_json` | string | JSON envelope array |
| `quality_json` | string | JSON flag list |
| `confidence` | float | In `[0, 1]` |

`ledger_json` must be a JSON list. Each item should be an object like `{"t":1.24,"start":1.02,"end":1.48}` with non-negative row-local seconds inside the segment duration. `envelope_json` should contain up to 96 normalized triples `[x, lower_y, upper_y]`, where `0 <= x <= 1` and `0 <= lower_y <= upper_y <= 1`. `quality_json` should be a JSON list of quality flags aligned to the predicted cycles.

Example:

```csv
id,ledger_json,envelope_json,quality_json,confidence
101,"[{""t"":0.52,""start"":0.31,""end"":0.73}]","[[0.0,0.42,0.58],[1.0,0.41,0.59]]","[""usable""]",0.63
102,"[]","[[0.0,0.45,0.55],[1.0,0.45,0.55]]","[]",0.25
```

---

## 4) Tags

Suggested platform tags: `medical`, `multimodal`, `signal-processing`, `computer-vision`, `cpu-only`.

---

## 5) Grading Configuration

* **Direction:** Maximize
* **Theoretical minimum:** `0.0`
* **Theoretical maximum:** `1.0`

---

## 6) Grading Script

**Select:** `Custom`

Paste the contents of `PASTE_THIS_GRADE.txt`.

---

## 7) Prepare Script

Paste the contents of `PASTE_THIS_PREPARE.txt`.

The raw input should be the official raw ZIP from the dataset source URL, or an unchanged official download/upload containing `pwd_images/` and `wfdb_format_ecg_and_respiration/`. Do not use a directory-index URL as a single-file platform import if it produces only a tiny `downloaded-file`; that is the HTML listing, not the dataset.

---

## 8) GPU Tier

**Select:** **CPU only / no GPU**. The official solver budget is 10 CPU cores, 62 GB RAM, and 1.5 hours. This challenge is designed for compact image/signal processing and small CPU-trained models, not GPU training.

---

## 9) What Not To Use

Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score.

* Source-row lookup, raw source filename reconstruction, or hidden record/timing recovery.
* Treating the task as direct fetal heart-rate regression or one-channel QRS detection.
* Hardcoded row ids, source ids, file ordering, file sizes, or split-specific dictionaries.
* External hosted APIs, hosted LLMs, closed remote inference, or private pretrained services.
* Access to private files, grader exploitation, or any channel beyond the public train/test files.
* Malformed JSON, negative time values, impossible boundaries, invalid confidence, or overlong fields intended to game validation.

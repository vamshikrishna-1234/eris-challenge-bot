# Challenge creation form - fill-in

## Difficulty

Hard

## Challenge Title

Killer Whale Conservation Bioacoustic Profiling From Hydrophone Audio

## Problem Description

Marine conservation teams, field scientists, and monitoring systems often need to decide whether a short underwater recording should trigger a killer whale follow-up alert: is there likely killer whale or orca activity, is it sparse or dense, are other biological sounds dominating, and how reliable is the clip for conservation response? This is an audio and bioacoustics challenge: build a multi-head encounter profile from short hydrophone clips. It is not a plain call/no-call detector and it is not an ecotype-only recognizer.

### Overview

You are given short mono WAV clips prepared from real underwater hydrophone recordings. The raw recordings come from an official public marine-bioacoustic archive of Northeast Pacific coastal and island hydrophone monitoring, collected by multiple field recording programs in habitats where killer whales and other biological sounds occur. The original source files vary by hydrophone site, recording date, sample rate, channel layout, ambient noise, vessel noise, and biological confounders. Prepared challenge clips are short source-redacted windows rendered as mono WAV audio; raw filenames, exact timestamps, provider names, locations, annotation ids, and frequency metadata are not public.

For each hidden test clip, produce a killer whale/orca encounter profile: presence, activity density, broad ecotype/context, confounder type, call-band bucket, and calibrated confidence. The public inputs are intentionally minimal: an opaque `id`, a non-source-revealing `audio_path`, a coarse `clip_duration_bucket`, and a generic prompt.

What not to use: do not attempt to recover upstream recording filenames, timestamps, locations, providers, annotation rows, or raw source paths; do not use audio fingerprint lookup against public archives; do not use filename/order/id side channels; do not submit a binary detector as if it solved the full triage task. Strong solutions should learn from the provided public training audio and labels, using acoustic evidence such as call density, spectral band, confounders, and uncertainty.

### Task Specification

Submit exactly these values for every test `id`: `orca_presence`, `encounter_activity`, `ecotype_context`, `confounder_type`, `call_band_bucket`, and `confidence`. The allowed values are listed in the submission table below. The task rewards the whole acoustic profile, not only whether an orca is present.

### Dataset

The public dataset contains labeled training clips, hidden-label test clips, and a sample submission. Audio paths are relative to the `public/` directory. The audio comes from fixed underwater hydrophone recordings made in real coastal monitoring conditions, including quiet background periods, killer whale calls, other biological calls, and mixed or weak evidence. Clips were extracted around annotated sound windows and nearby background/confounder windows, then converted to a consistent short mono WAV format for modeling.

#### Public Files

| Item | Description |
|---|---|
| `train.csv` | labeled clips |
| `test.csv` | hidden-label clips |
| `sample_submission.csv` | schema example |
| `train/audio/` | train WAV clips |
| `test/audio/` | test WAV clips |

`train.csv` includes the public inputs and all target columns. `test.csv` includes only public inputs. Public ids and paths are opaque and do not encode recording names, timestamps, providers, locations, source annotation ids, raw paths, or frequency labels.

#### train.csv Columns

| Column | Type | Description |
|---|---|---|
| `id` | string | opaque clip id |
| `audio_path` | string | WAV path |
| `clip_duration_bucket` | string | coarse duration |
| `prompt` | string | generic prompt |
| `orca_presence` | string | presence label |
| `encounter_activity` | string | activity label |
| `ecotype_context` | string | context label |
| `confounder_type` | string | confounder label |
| `call_band_bucket` | string | band label |
| `confidence` | float | label reliability |

`orca_presence` is one of `yes`, `no`, or `uncertain`. `encounter_activity` is one of `quiet_background`, `single_call`, `multiple_calls`, `dense_calling`, or `confuser_dominant`. `ecotype_context` is one of `SRKW`, `TKW`, `NRKW`, `OKW`, or `not_orca_or_unknown`. `confounder_type` is one of `humpback_or_other_bio`, `ambient_background`, `unidentified_bio`, `mixed_or_uncertain`, or `none`. `call_band_bucket` is one of `low_band`, `mid_band`, `high_band`, `broad_band`, or `no_call`. `confidence` is a float in `[0, 1]`.

#### test.csv Columns

| Column | Type | Description |
|---|---|---|
| `id` | string | opaque clip id |
| `audio_path` | string | WAV path |
| `clip_duration_bucket` | string | coarse duration |
| `prompt` | string | generic prompt |

The test file withholds all target columns. Use the audio clip and the public training labels to infer the hidden triage profile.

### Submission Format

| Column | Type | Constraint |
|---|---|---|
| `id` | string | exact test id |
| `orca_presence` | string | allowed value |
| `encounter_activity` | string | allowed value |
| `ecotype_context` | string | allowed value |
| `confounder_type` | string | allowed value |
| `call_band_bucket` | string | allowed value |
| `confidence` | float | 0 to 1 |

Submit exactly one row for every test id, with columns in the exact order shown above.

Example submission rows:

```csv
id,orca_presence,encounter_activity,ecotype_context,confounder_type,call_band_bucket,confidence
oet_04cce1b2a9935b,yes,multiple_calls,SRKW,none,mid_band,0.82
oet_7a299f0b651923,no,confuser_dominant,not_orca_or_unknown,humpback_or_other_bio,no_call,0.61
oet_f6ed99a26b7a81,uncertain,single_call,OKW,mixed_or_uncertain,high_band,0.54
```

### Evaluation

Invalid submissions raise an error rather than receiving a valid numeric score. Structural invalidity includes missing, extra, or reordered columns; duplicate ids; an id set different from `test.csv`; invalid categorical values; non-numeric confidence; non-finite confidence; and confidence outside `[0, 1]`.

For valid submissions, the grader computes `FinalScore` from six component scores and one hidden robustness term. All formulas below use only rows in the hidden test set.

For each discrete output head `h`, the grader first computes macro-F1 over the answer classes that appear in that hidden set. For each class `c`, `Precision_c = TP_c / (TP_c + FP_c)`, `Recall_c = TP_c / (TP_c + FN_c)`, and `F1_c = 2*Precision_c*Recall_c / (Precision_c + Recall_c)`, with `F1_c = 0` when there are no true positives. Then `MacroF1_h` is the mean of `F1_c` across classes, and `HeadScore_h = MacroF1_h^2`.

For the confidence column, each row receives `ConfRow_i = max(0, 1 - abs(pred_confidence_i - true_confidence_i) / 0.5)`. The confidence component is `ConfidenceScore = mean(ConfRow_i)^2`.

The normalized base profile is:

`BaseProfile = (8/49)*OrcaPresenceScore + (11/49)*EncounterActivityScore + (9/49)*EcotypeContextScore + (8/49)*ConfounderTypeScore + (8/49)*CallBandBucketScore + (5/49)*ConfidenceScore`

These six normalized weights sum exactly to `1.0`.

The hidden robustness axes are provider-family, ecotype/context group, activity group, confounder group, call-band group, and clip-quality group. For every hidden bucket on those axes, the grader recomputes `BaseProfile` on only that bucket's rows. `WorstGroup = min(bucket BaseProfile)`.

The final score is:

`FinalScore = 0.95*BaseProfile + 0.05*WorstGroup`

The two top-level weights sum to `1.0`, and the final score is clipped to `[0, 1]`.

The theoretical minimum is `0.0`; the theoretical maximum is `1.0`; higher is better. A perfect submission with every hidden label and target confidence value exactly correct scores `1.0`.

### Intended Solution

Strong approaches should train or fine-tune audio models, spectrogram CNNs, open audio encoders, or calibrated classical models over learned and hand-built acoustic features. Useful evidence includes repeated call structure, call spacing, band-limited energy, broad-band events, non-orca biological confounders, ambient-only clips, and uncertainty from weak or mixed evidence.

### Enforcement On Invalid Approaches

Submissions based on upstream-source row lookup, recovered recording names or timestamps, external answer tables, exact audio fingerprinting against public archives, hosted commercial audio-recognition APIs, manual labeling of hidden test rows, hardcoded id-to-answer maps, or binary detector-only systems may be rejected before payout even if the CSV is structurally valid. The competition rewards learned multi-head hydrophone encounter triage from the provided training split.

## Tags

audio, bioacoustics, signal-processing, conservation, calibration

## Grading Configuration

Grade direction: Maximize

Theoretical minimum: 0.0

Theoretical maximum: 1.0

## Grading Script

Use `PASTE_THIS_GRADE.txt`.

## Prepare Script

Use `PASTE_THIS_PREPARE.txt`.

## GPU Tier

A10G

## What Not To Use

Do not use hosted commercial audio-recognition APIs, public-source row lookup, upstream recording metadata reconstruction, external labeled answer tables, exact audio fingerprint matching, filename/order/id side channels, manual test labeling, hardcoded answer maps, or binary call/no-call detector-only submissions that ignore the required multi-head triage profile.

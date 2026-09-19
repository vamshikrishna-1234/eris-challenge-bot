# Challenge creation form - fill-in

## Difficulty

Hard

## Challenge Title

Blind Room-Scale And Echo-Zone Inference From Reverberant Speech

## Problem Description

Voice agents, far-field ASR systems, conferencing devices, and room-aware audio processors need to infer what kind of acoustic environment they are hearing before they decide how aggressively to denoise, dereverberate, beamform, or trust a speech segment. This is not generic blind T60/DRR estimation and it is not exact room-shape inference. The task is to infer a practical multi-head acoustic environment profile from reverberant speech.

### Overview

You are given short mono WAV clips of speech that have passed through measured room impulse responses and measured room noise. The public clips also include mild deterministic speech-preserving perturbations so exact source-audio matching is not a valid shortcut. For each test clip, predict the room-scale bucket, reverberation bucket, source-microphone distance bucket, echo-zone category, and a confidence value.

The public inputs are deliberately minimal: an opaque `sample_id`, a non-source-revealing `audio_path`, and a generic prompt. Room ids, source/microphone positions, RIR ids, speaker ids, utterance filenames, SNR, raw room dimensions, measured T60, and measured DRR are not public. The intended approach is to train or fine-tune an open audio model, speech encoder, or acoustic-feature model on the provided training clips and labels.

What not to use: do not solve this as a T60/DRR-only benchmark, do not attempt to recover the upstream corpus rows or room ids, do not match audio fingerprints to public source files, and do not use filename/order/id shortcuts. The scoring rewards the full acoustic profile, calibrated uncertainty, and hidden subgroup robustness.

### Task Specification

Predict exactly these columns for every test `sample_id`:

- `room_volume_bucket`: one of `small`, `medium`, `large`, `very_large`.
- `rt60_bucket`: one of `dry`, `moderate`, `reverberant`, `very_reverberant`.
- `source_mic_distance_bucket`: one of `near`, `mid`, `far`, `unknown_or_uncertain`.
- `echo_zone`: one of `direct_dominant`, `balanced`, `reverberant_dominant`, `noisy_uncertain`.
- `confidence`: a float in `[0, 1]` estimating the reliability of the submitted acoustic profile for that row.

The labels are bucketed from measured acoustic metadata and deliberately include uncertainty around physically ambiguous boundaries. The prepared split ensures that every hidden test category has labeled training coverage, including the dry RT60 class. Do not overclaim exact room geometry: the target is room scale and echo-zone behavior useful to speech systems.

### Dataset

The public dataset contains `train.csv`, `test.csv`, `sample_submission.csv`, and WAV clips under `train/audio/` and `test/audio/`. Audio paths are relative to the `public/` directory.

#### Public Files

| Item | Description |
|---|---|
| `train.csv` | labeled training clips |
| `test.csv` | hidden-label test clips |
| `sample_submission.csv` | dummy submission format |
| `train/audio/` | train WAV clips |
| `test/audio/` | test WAV clips |

`train.csv` includes the public inputs and all five labels. `test.csv` includes only public inputs. The sample submission is a weak train-prior style file for schema validation, not a competitive solution.

#### train.csv Columns

| Column | Type | Description |
|---|---|---|
| `sample_id` | string | opaque clip id |
| `audio_path` | string | public WAV path |
| `prompt` | string | generic task prompt |
| `room_volume_bucket` | string | scale label |
| `rt60_bucket` | string | reverb label |
| `source_mic_distance_bucket` | string | distance label |
| `echo_zone` | string | echo-zone label |
| `confidence` | float | label reliability |

The training labels are bucketed acoustic-environment targets. Public paths and ids are salted and do not contain room, RIR, source, microphone, speaker, utterance, SNR, or noise identifiers.

#### test.csv Columns

| Column | Type | Description |
|---|---|---|
| `sample_id` | string | opaque clip id |
| `audio_path` | string | public WAV path |
| `prompt` | string | generic task prompt |

The test file has the same public input fields as the training file and withholds all targets.

### Submission Format

| Column | Type | Constraint |
|---|---|---|
| `sample_id` | string | exact test id |
| `room_volume_bucket` | string | allowed bucket |
| `rt60_bucket` | string | allowed bucket |
| `source_mic_distance_bucket` | string | allowed bucket |
| `echo_zone` | string | allowed category |
| `confidence` | float | 0 to 1 |

Submit exactly one row for every test id, with the columns in the exact order shown above.

Example submission rows:

| sample_id | room_volume_bucket | rt60_bucket | source_mic_distance_bucket | echo_zone | confidence |
|---|---|---|---|---|---|
| brs_03a91d4c2e1b | medium | reverberant | mid | balanced | 0.71 |
| brs_8d3f09ac61aa | large | moderate | far | reverberant_dominant | 0.64 |
| brs_f18c725a4320 | small | dry | near | direct_dominant | 0.82 |

### Evaluation

Invalid submissions raise an error rather than receiving a valid numeric score. Structural invalidity includes missing, extra, or reordered columns; duplicate ids; an id set different from `test.csv`; invalid categorical values; non-finite confidence; and confidence outside `[0, 1]`.

For valid submissions, the grader computes macro-F1 over the hidden test classes represented in each categorical head:

- `RoomF1 = macro_f1(room_volume_bucket)^2`
- `Rt60F1 = macro_f1(rt60_bucket)^2`
- `DistanceF1 = macro_f1(source_mic_distance_bucket)^2`
- `EchoF1 = macro_f1(echo_zone)^2`
- `ConfCal = mean(max(0, 1 - abs(pred_confidence - target_confidence) / 0.5))^2`

The normalized base profile uses the five head terms with relative weights `25/95`, `25/95`, `20/95`, `15/95`, and `10/95`:

`BaseProfile = (25/95) * RoomF1 + (25/95) * Rt60F1 + (20/95) * DistanceF1 + (15/95) * EchoF1 + (10/95) * ConfCal`.

`WorstHidden` is the minimum `BaseProfile` over hidden room-scale, RT60, distance, noise-condition, speech-split, and mic/source-configuration groups.

`Final = 0.95 * BaseProfile(all rows) + 0.05 * WorstHidden`.

The top-level weights are intentionally `0.95` for overall acoustic-profile quality and `0.05` for worst hidden-subgroup robustness, so they sum to `1.0`.

The theoretical minimum is `0.0`; the theoretical maximum is `1.0`; higher is better. A perfect submission with all hidden labels and target confidence values scores exactly `1.0`.

### Intended Solution

Strong solutions should train or fine-tune open audio/speech models such as wav2vec2/HuBERT-style encoders, Whisper-family encoders used as feature extractors, conformers, audio spectrogram CNNs, or calibrated gradient-boosted models over acoustic features. Useful evidence includes decay-envelope behavior, direct-to-reverberant balance, late-tail coloration, speech/noise masking, spectral tilt, and how those cues interact across labels.

Prompt-only systems, transcript-only approaches, and T60-only estimators are not expected to solve the full multi-head profile. The training set teaches the bucket definitions and uncertainty conventions.

### Enforcement On Invalid Approaches

Submissions based on public-source row lookup, recovered upstream room/RIR/speech identifiers, external labeled room-acoustics answer tables, audio fingerprint matching against the official source archives, hosted commercial speech APIs, manual labeling of hidden test rows, hardcoded id-to-answer maps, or rule-only T60/DRR estimation may be rejected before payout even if the CSV is structurally valid. The competition rewards learned blind acoustic-environment inference from the provided public training split.

## Tags

audio, speech, room-acoustics, uncertainty, calibration

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

Do not use hosted commercial speech/audio APIs, public-source row lookup, upstream corpus metadata reconstruction, external labeled room-acoustics answer tables, exact audio fingerprint matching, transcript/speaker/utterance lookup, filename/order/id side channels, manual test labeling, hardcoded answer maps, or generic blind T60/DRR-only estimators that ignore the multi-head room-scale and echo-zone task.

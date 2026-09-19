# Challenge creation form - fill-in

## Difficulty

Hard

## Challenge Title

Disfluency Reparandum-Repair Structure Recovery From Speech

## Problem Description

People often restart themselves in meetings: "move the red, uh, move the blue box" means the first phrase was abandoned and the corrected phrase begins later. Meeting captioners, ASR post-processors, and speech-assistive tools need to preserve this structure instead of only outputting a cleaned transcript. This challenge gives real meeting-speech audio plus the already-tokenized transcript and asks you to mark the abandoned words, filler/edit words, repair start, and whether a real self-correction happened.

### Overview

Each row contains a short 16 kHz mono WAV clip from a licensed public meeting-speech corpus and a JSON token transcript with implicit 0-based token indices. The words are already transcribed; the task is not to recover missing words, choose among minimal-pair candidates, or run full ASR. For every test row, predict five outputs: the abandoned token span, the filler/edit span, the repair onset token, a 0/1 disfluency flag, and a calibrated confidence.

In this challenge, `reparandum` means the words the speaker started and then abandoned. `interregnum` means filler or edit material between the abandoned phrase and the correction, such as `uh` or `I mean`. `repair_onset` is the first token of the corrected phrase. Rows can also be non-disfluent foils, such as ordinary emphasis, filler without a repair, or clean speech.

The audio comes from real multi-speaker meeting recordings with headset-mix audio and aligned transcript/disfluency annotation sources. This setting mirrors practical caption cleanup, meeting-assistant transcription, and speech-interface post-processing, where a model must use transcript context plus acoustic cues such as timing, cutoff, hesitation, and prosody.

What not to use: hosted or commercial speech/language APIs, external ASR or disfluency APIs, external labeled disfluency corpora, source lookup of original meeting clips or annotations, transcript-only/rule-only shortcuts, filename/timestamp/speaker-id leakage, row-order side channels, hardcoded answer maps, manual test labeling, and grader/filesystem exploitation are prohibited. The intended route is to fine-tune or train an open speech/audio-text model with span heads using the public training examples.

This benchmark is distinct from accent-robust word recovery. Here the transcript words are already visible, and the model must decide which visible tokens belong to the abandoned phrase, filler/edit term, and repair onset.

### Task Specification

`reparandum_span` is the abandoned token span as `[start,end]`, inclusive, or `NONE` when there is no structured self-repair. `interregnum_span` is the filler or edit material between reparandum and repair, also inclusive, or `NONE`. `repair_onset` is the token index where the fluent repair starts, written as an integer string, or `NONE`. `is_disfluency` is `1` for a structured self-repair target and `0` for no structured repair target, including emphasis, filler-only, and clean-speech foils. `confidence` is a float in `[0,1]` calibrated to the row-level structural correctness of the prediction.

The training labels are benchmark labels aligned to real meeting speech and real transcript timing. They are not a clinical stuttering diagnosis and should not be interpreted as human-gold discourse analysis beyond the stated span-recovery contract.

## Dataset

The public dataset contains `train.csv`, `test.csv`, `sample_submission.csv`, and WAV clips under `train/audio/` and `test/audio/`. Audio paths in the CSVs are relative to the `public/` directory. Public test rows do not expose original meeting ids, speaker ids, raw timestamps, source word ids, annotation ids, split groups, repair types, or hidden subgroup names.

### Public Files

| Item | Description |
|---|---|
| `train.csv` | labeled rows |
| `test.csv` | hidden-label rows |
| `sample_submission.csv` | valid template |
| `train/audio/` | train WAV clips |
| `test/audio/` | test WAV clips |

`train.csv` has 439 rows in this prepared split, and `test.csv` has 261 rows. The WAV clips are short context windows around real spontaneous-speech candidates.

### train.csv Columns

| Column | Type | Description |
|---|---|---|
| `id` | int | opaque row id |
| `audio_path` | string | relative WAV path |
| `token_transcript` | JSON string | token list |
| `token_timing_json` | JSON string | token times |
| `reparandum_span` | string | `[start,end]` or NONE |
| `interregnum_span` | string | `[start,end]` or NONE |
| `repair_onset` | string | index or NONE |
| `is_disfluency` | int | 0 or 1 |
| `confidence` | float | gold confidence |

The `token_transcript` value is a compact JSON list of normalized tokens. The `token_timing_json` value gives token start and end offsets in milliseconds relative to the clip, but it does not expose source timestamps or annotation ids.

The train-only label columns are `reparandum_span`, `interregnum_span`, `repair_onset`, `is_disfluency`, and `confidence`; these are withheld from `test.csv`.

Example `token_transcript`: `["move","the","red","uh","move","the","blue","box","left"]`.

Example `token_timing_json`: `[{"token":"move","start_ms":180,"end_ms":430},{"token":"the","start_ms":440,"end_ms":540},{"token":"red","start_ms":550,"end_ms":820}]`.

### test.csv Columns

| Column | Type | Description |
|---|---|---|
| `id` | int | opaque row id |
| `audio_path` | string | relative WAV path |
| `token_transcript` | JSON string | token list |
| `token_timing_json` | JSON string | token times |

The test file has the same public input fields as the training file and withholds all target columns.

In prose, `test.csv` contains `id`, `audio_path`, `token_transcript`, and `token_timing_json`. It does not contain labels, source meeting identifiers, source speaker identifiers, raw timestamps, repair-type groups, or annotation ids.

## Submission Format

| Column | Type | Constraint |
|---|---|---|
| `id` | int | exact test id |
| `reparandum_span` | string | `[start,end]` or NONE |
| `interregnum_span` | string | `[start,end]` or NONE |
| `repair_onset` | string | index or NONE |
| `is_disfluency` | int | 0 or 1 |
| `confidence` | float | 0 to 1 |

Submit exactly one row for every test id, with the columns in the exact order shown above.

In prose, `sample_submission.csv` contains `id`, `reparandum_span`, `interregnum_span`, `repair_onset`, `is_disfluency`, and `confidence`, and the final submission must use the same columns in the same order.

Example submission rows:

| id | reparandum_span | interregnum_span | repair_onset | is_disfluency | confidence |
|---|---|---|---|---|---|
| 100000 | NONE | NONE | NONE | 0 | 0.6 |
| 100005 | NONE | NONE | NONE | 0 | 0.6 |
| 100014 | NONE | NONE | NONE | 0 | 0.6 |

## Evaluation

Invalid submissions score `0.0`. Structural invalidity includes missing, extra, or reordered columns; duplicate ids; an id set different from `test.csv`; invalid `is_disfluency`; non-finite or out-of-range `confidence`; impossible or out-of-range parsed spans; and impossible or out-of-range parsed repair-onset indices. A malformed row-local span string such as `[oops]` zeros that span head for that row without crashing the grader.

For each row, `S_reparandum` is inclusive token-span IoU, with `NONE` vs `NONE` equal to `1` and one `NONE` equal to `0`. `S_interregnum` uses the same IoU and `NONE` handling. `S_onset` is `1` for exact repair-onset match and `0` otherwise, with `NONE` vs `NONE` equal to `1`. `S_isdisf` is exact `is_disfluency` correctness. If the gold row is a true repair but the submission predicts `is_disfluency=0`, then `S_reparandum`, `S_interregnum`, and `S_onset` are set to `0` for that row so an all-NONE prediction cannot receive accidental structure credit. `S_joint` is `1` only when `S_reparandum`, `S_interregnum`, `S_onset`, and `S_isdisf` are all exactly `1`; otherwise it is `0`. `S_calib = max(0, 1 - abs(confidence - mean(S_reparandum, S_interregnum, S_onset, S_isdisf)))`.

The row score is `0.70*S_joint + 0.10*S_reparandum^2 + 0.05*S_interregnum^2 + 0.03*S_onset^2 + 0.07*S_isdisf^2 + 0.05*S_calib^2`.

The final score is `0.45*mean(row_score) + 0.15*worst_mean_by_hidden_source_group + 0.25*worst_mean_by_hidden_repair_group + 0.15*mean_true_repair_row_score`. Hidden source groups are coarse recording/source-family buckets such as meeting-family groups; they are used only to ensure the model works across different meeting sources. Hidden repair groups are coarse target-type buckets such as structured repairs and non-repair foils; they are used only to ensure the model does not perform well on one repair type while failing another. `mean_true_repair_row_score` is the mean row score over gold rows with `is_disfluency=1`, included so a trivial all-NONE submission is weak. These group labels are not included in public test rows because they would leak target information, but the grouping axes are described here so the robustness term is clear. The theoretical minimum is `0.0`, the theoretical maximum is `1.0`, and higher is better.

### Intended Solution

Strong solutions should fine-tune or train open speech/audio-text models such as wav2vec2, HuBERT, Whisper-family encoders, conformer encoders, or multimodal speech-text models, with a token-level text encoder and span/onset heads. Useful models should learn acoustic timing, prosody, cutoff, hesitation, and repetition cues together with the transcript; prompt-only and transcript-only approaches are not the intended solution.

### Enforcement On Invalid Approaches

Submissions based on hosted commercial APIs, external labeled disfluency corpora, direct source lookup, recovered original meeting annotations, transcript-only rules, filename or timestamp leakage, hardcoded id-to-answer maps, or grader/filesystem exploitation may be rejected before payout even if the CSV is structurally valid. The competition rewards learned speech/NLP modeling from the provided public training data.

## Tags

audio, speech, nlp, fine-tuning, multimodal

## Grading Configuration

Grade direction: Maximize

Theoretical minimum: 0.0

Theoretical maximum: 1.0

## Grading Script

Use `PASTE_THIS_GRADE.txt`.

## Prepare Script

Use `PASTE_THIS_PREPARE.txt`.

## GPU Tier

H100

## What Not To Use

Do not use hosted commercial speech or language APIs, external ASR/disfluency APIs, external labeled disfluency corpora, source lookup of original meeting clips/annotations, transcript-only or rule-only shortcuts, filename/timestamp/speaker-id leakage, row-order tricks, manual labeling, hardcoded answer maps, or grader/filesystem exploitation.

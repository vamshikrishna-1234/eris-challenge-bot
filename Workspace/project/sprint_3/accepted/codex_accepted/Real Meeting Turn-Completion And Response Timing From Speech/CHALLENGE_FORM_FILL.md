# Challenge creation form - fill-in

## Difficulty

Hard

## Challenge Title

Real Meeting Turn-Completion And Response Timing From Speech

## Problem Description

Live meeting assistants, captioners, and voice agents need to decide when a speaker has actually finished a turn, when the same speaker is only pausing mid-thought, when another person is giving a short acknowledgement, and when an overlapping start is competing for the floor. Text context alone often misses the timing and prosody that drive those decisions, so this challenge asks you to model real meeting speech clips together with lossy token-shape context.

### Overview

You are given short 16 kHz mono WAV clips from real multi-party meetings. Each public clip is an opaque de-identified excerpt that ends at or near a candidate current-speaker boundary and is paired with a redacted token-shape window, token timings inside the clip, and coarse anonymized speaker context.

For every test row, predict the turn-taking state at the boundary, the timing of the next speech event, the next-speaker relation, and an honest confidence value. The target is a practical endpointing and response-timing task for speech/NLP systems, not a transcript parser.

What not to use: hosted commercial speech or language APIs, external labeled meeting corpora, source lookup of public meeting annotation files or test meeting identities, transcript-only rule shortcuts, filename/timestamp/meeting-id reconstruction, row-order tricks, and hardcoded answer maps are prohibited. The intended route is to train or fine-tune an open speech, audio-text, or multimodal model on the provided training examples.

### Task Specification

The allowed `turn_state` values are `COMPLETE`, `CONTINUE`, `BACKCHANNEL`, `OVERLAP`, and `UNCERTAIN`. `COMPLETE` means the current speaker yields the floor and another speaker takes a substantive next turn. `CONTINUE` means the same speaker resumes after the boundary before another substantive turn. `BACKCHANNEL` means another speaker gives a short acknowledgement while the current speaker keeps or quickly regains the floor. `OVERLAP` means another speaker starts during or nearly on top of current speech in a competing way. `UNCERTAIN` is used only for rows where the annotation/timing region does not support a clear near-term event.

`next_response_ms` is an integer in `[0, 3000]` measuring the clipped time from the candidate boundary to the next speech event or continuation. `next_speaker_relation` is one of `SAME`, `OTHER`, `MULTI`, or `NONE_OR_UNCLEAR`. `confidence` is a float in `[0, 1]` that should reflect how likely the row-level prediction is to be correct.

## Dataset

The public dataset contains `train.csv`, `test.csv`, `sample_submission.csv`, and WAV clips under `train/audio/` and `test/audio/`. `train.csv` has the input columns `id`, `audio_path`, `transcript_window`, `token_timing_json`, and `speaker_context_json`, plus the train-only label columns `turn_state`, `next_response_ms`, `next_speaker_relation`, and `confidence`. `test.csv` has only the input columns `id`, `audio_path`, `transcript_window`, `token_timing_json`, and `speaker_context_json`. `sample_submission.csv` is a dummy format file with the required columns `id`, `turn_state`, `next_response_ms`, `next_speaker_relation`, and `confidence`.

### Public Files

| Item | Description |
|---|---|
| `train.csv` | labeled training rows |
| `test.csv` | hidden-label test rows |
| `sample_submission.csv` | dummy format file |
| `train/audio/` | train WAV clips |
| `test/audio/` | test WAV clips |

The audio paths in the CSVs are relative to the `public/` directory. Training rows include labels; test rows include only public inputs.

### train.csv Columns

| Column | Type | Description |
|---|---|---|
| `id` | int | opaque row id |
| `audio_path` | string | relative WAV path |
| `transcript_window` | string | token-shape window |
| `token_timing_json` | JSON string | redacted token times |
| `speaker_context_json` | JSON string | coarse context |
| `turn_state` | string | target class |
| `next_response_ms` | int | target latency |
| `next_speaker_relation` | string | target relation |
| `confidence` | float | gold confidence |

The transcript window is redacted to coarse token-shape values rather than verbatim words. The JSON timing field carries token indices, token-shape values, and relative timing, not raw lexical tokens. The JSON context uses anonymized local descriptors and does not expose meeting ids, original speaker ids, timestamps, annotation ids, future events, or source filenames.

### test.csv Columns

| Column | Type | Description |
|---|---|---|
| `id` | int | opaque row id |
| `audio_path` | string | relative WAV path |
| `transcript_window` | string | token-shape window |
| `token_timing_json` | JSON string | redacted token times |
| `speaker_context_json` | JSON string | coarse context |

The test file has the same public input fields as the training file and withholds all targets.

### Submission Format

| Column | Type | Constraint |
|---|---|---|
| `id` | int | exact test id |
| `turn_state` | string | allowed class |
| `next_response_ms` | int | 0 to 3000 |
| `next_speaker_relation` | string | allowed relation |
| `confidence` | float | 0 to 1 |

Submit exactly one row for every test id, with the columns in the exact order shown above.

```csv
id,turn_state,next_response_ms,next_speaker_relation,confidence
102341,COMPLETE,420,OTHER,0.74
487221,CONTINUE,610,SAME,0.68
750812,BACKCHANNEL,120,OTHER,0.57
```

### Evaluation

Invalid submissions score `0.0`. Structural invalidity includes missing, extra, or reordered columns; duplicate ids; an id set different from `test.csv`; invalid categorical values; non-integer or out-of-range `next_response_ms`; and non-finite or out-of-range `confidence`.

For valid submissions, the grader computes row heads for state correctness, next-speaker relation correctness, timing similarity, calibration, and joint exactness. Timing similarity is `max(0, 1 - abs(pred_ms - true_ms) / tolerance)`, with tolerance determined by the true latency band. Calibration is `max(0, 1 - abs(confidence - row_correctness))`, where row correctness blends state, relation, and timing evidence.

For any group of rows, `GroupScore = 0.45 * mean(state_correct)^2 + 0.20 * mean(relation_correct)^2 + 0.20 * mean(timing_similarity)^2 + 0.10 * mean(calibration)^2 + 0.05 * mean(joint_exact)^2`.

The final score is `0.70 * GroupScore(all rows) + 0.15 * worst GroupScore by hidden meeting family + 0.15 * worst GroupScore by hidden turn type`. The theoretical minimum is `0.0`; the theoretical maximum is `1.0`; higher is better.

### Intended Solution

Strong solutions should train or fine-tune open-weight speech or audio-text models such as wav2vec2/HuBERT-style encoders, Whisper-family encoders, conformer encoders, or multimodal speech-text models, with optional text encoders over the transcript and token timing fields. Prompt-only or transcript-only approaches are not expected to handle pauses, energy decay, overlap, acknowledgement timing, and speaker dynamics reliably.

### Enforcement On Invalid Approaches

Submissions based on hosted commercial APIs, external labeled meeting datasets, direct source lookup, manually recovered public-source test annotations, hardcoded id-to-answer maps, or rule-only parsing of the redacted text fields may be rejected before payout even if the CSV is structurally valid. The competition rewards learned speech/NLP modeling from the provided public training set.

## Tags

audio, multimodal, nlp, fine-tuning

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

Do not use hosted commercial speech or language APIs, external labeled meeting corpora, source lookup of public meeting annotation files/test meetings, transcript-only rule systems, filename/timestamp/meeting-id leakage, row-order/id tricks, manual labeling, or hardcoded answer maps.

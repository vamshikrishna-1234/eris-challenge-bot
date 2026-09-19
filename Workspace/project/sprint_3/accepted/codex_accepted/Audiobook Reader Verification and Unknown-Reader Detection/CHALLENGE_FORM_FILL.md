# Challenge creation form - fill-in

## Difficulty

Hard

## Challenge Title

Audiobook Reader Verification and Unknown-Reader Detection

## Problem Description

Voice verification and audio-source triage systems often need to decide whether a clip belongs to a known enrolled reader or to a previously unseen voice. This challenge uses real audiobook speech and asks for open-set reader provenance from audio, with no source speaker ids, chapter ids, transcripts, or original filenames exposed in the public test rows.

### Overview

Objective: for each test audio clip, predict whether it belongs to one of the reader identities represented in public training or to an unseen reader, then output the matching reader token or `UNKNOWN` with calibrated confidence.

Each row contains a short mono WAV clip derived from clean read-audiobook recordings by human readers. Public training rows include a JSON verdict for the reader provenance. Public test rows hide the verdict and include a mix of clips from readers seen in public training and clips from readers absent from public training, where the required provenance is `UNKNOWN`.

The default preparation is a few-shot open-set enrollment problem. Each known reader has only a small number of labeled enrollment clips in `train.csv`, while `test.csv` contains additional clips from those readers plus acoustically similar unseen readers that must be labeled `UNKNOWN`. The exact number of known reader tokens is visible in `train.csv` by counting unique `provenance` values, and the exact row counts are visible in the released CSV files. Audio is standardized as short mono 16 kHz WAV clips, usually under 2.5 seconds after deterministic speech-preserving channel rendering; natural reader, channel, book, and passage variation remain in the speech signal.

The public inputs are deliberately minimal: an opaque `id`, a non-source-revealing `audio_path`, `duration_sec`, and a coarse `utterance_length_bucket`. Public files do not expose original paths, source split names, speaker ids, chapter ids, book ids, transcript text, or raw row order. Audio is rewritten under opaque filenames with mild speech-preserving de-identification so exact source-file matching is not the intended route.

What not to use: do not recover original corpus rows, speaker ids, chapter ids, book ids, transcripts, or source filenames; do not match audio fingerprints against public audiobook archives; do not use hosted commercial speaker-recognition APIs; and do not use row-order, filename, or id shortcuts. The intended route is to train or fine-tune open audio or speaker-embedding models on the provided public training examples.

### Task Specification

Submit one `verdict_json` object for every test `id`. The object must have exactly these keys:

- `known_reader_score`: a float in `[0,1]`, where higher means the clip belongs to one of the public training readers.
- `provenance`: one of the reader tokens observed in public training, such as `reader_000`, or `UNKNOWN` for an unseen reader.
- `confidence`: a float in `[0,1]` estimating row-level reliability of the verdict.

Use a reader token only when the audio matches that enrolled reader from the public training examples. Use `UNKNOWN` when the clip is from a reader not represented by any public training token. Do not put transcripts, speaker ids, chapter ids, paths, or explanations inside the JSON.

### Dataset

The public dataset contains `train.csv`, `test.csv`, `sample_submission.csv`, and WAV clips under `train/audio/` and `test/audio/`. Audio paths are relative to the `public/` directory.

#### Public Files

| Item | Description |
|---|---|
| `train.csv` | labeled train rows |
| `test.csv` | hidden test rows |
| `sample_submission.csv` | valid template |
| `train/audio/` | train WAV clips |
| `test/audio/` | test WAV clips |

`train.csv` includes public input columns and the train-only `verdict_json` label. `test.csv` has the same public input fields without the label. The sample submission is a weak prior-style file for schema validation, not a competitive solution.

#### train.csv Columns

| Column | Type | Description |
|---|---|---|
| `id` | string | opaque row id |
| `audio_path` | string | relative WAV path |
| `duration_sec` | float | clip duration |
| `utterance_length_bucket` | string | word-count bin |
| `verdict_json` | JSON string | train verdict |

The training verdict JSON is the only target column. Reader tokens in the training verdicts define the known provenance classes available to participants. `utterance_length_bucket` is a coarse transcript word-count bin with values `unknown`, `short`, `medium`, or `long`: `unknown` means no transcript text was available during preparation, `short` means fewer than 12 words, `medium` means 12 to 24 words, and `long` means at least 25 words. Transcript text itself is never public.

#### test.csv Columns

| Column | Type | Description |
|---|---|---|
| `id` | string | opaque row id |
| `audio_path` | string | relative WAV path |
| `duration_sec` | float | clip duration |
| `utterance_length_bucket` | string | word-count bin |

The test file withholds all labels and does not include original speaker, chapter, book, transcript, or source-path information. Test uses the same `utterance_length_bucket` values and definitions as train.

### Submission Format

| Column | Type | Constraint |
|---|---|---|
| `id` | string | exact test id |
| `verdict_json` | JSON string | exact keys |

Submit exactly one row for every test id, with the CSV columns in the exact order shown above. Each JSON string must be shorter than 256 characters and must contain exactly the keys `known_reader_score`, `provenance`, and `confidence`; JSON key order is not scored, but extra or missing keys make that row schema-invalid.

Example submission rows:

```csv
id,verdict_json
rasp_03a91d4c2e1b,"{""confidence"":0.66,""known_reader_score"":0.84,""provenance"":""reader_004""}"
rasp_8d3f09ac61aa,"{""confidence"":0.62,""known_reader_score"":0.21,""provenance"":""UNKNOWN""}"
rasp_f18c725a4320,"{""confidence"":0.72,""known_reader_score"":0.79,""provenance"":""reader_017""}"
```

### Evaluation

Structural invalidity is rejected with an invalid-submission error: missing, extra, or reordered columns; duplicate ids; an id set different from `test.csv`; missing `verdict_json`; or any parsed confidence that is non-finite or outside `[0,1]`. Malformed or schema-invalid JSON in an individual row does not crash the grader, but that row receives no credit for JSON-dependent heads. JSON strings longer than 256 characters are treated as malformed.

The primary metric rewards open-set reader provenance and makes row-level mistakes expensive: good submissions rank known-reader clips above unseen-reader clips, assign the exact known reader token or `UNKNOWN`, avoid any known/unknown side errors, stay consistent across utterances from the same hidden reader, work across hidden robustness groups, and report confidence that matches row-level correctness.

`Knownness` measures how well `known_reader_score` separates known-reader test clips from unseen-reader test clips. It is `max(0, 2*AUROC(known_reader_score, is_known_reader)-1) * KnownScoreValidRate`, where `KnownScoreValidRate` is the fraction of rows whose `known_reader_score` is finite and in `[0,1]`.

`ProvenanceF1` is macro-F1 over the hidden provenance classes represented in the test set, including known reader tokens and `UNKNOWN`.

`ReaderConsistency` averages exact provenance correctness within hidden same-reader groups that contain at least two test utterances. A row is provenance-correct only when the submitted `provenance` is a valid reader token or `UNKNOWN` and exactly equals the hidden provenance for that clip.

`StrictRow` is a heavily penalized exact row score. A row is exact only when `provenance` exactly equals the hidden value and `known_reader_score` is on the correct side of 0.5 for known versus unseen readers. Let `ExactRate` be the fraction of exact rows; then `StrictRow = max(0, 1 - 14*(1 - ExactRate))`. This means each wrong row costs fourteen times its share of the test set for this component.

`WorstStrictGroup` applies the same exact-row penalty inside hidden robustness groups and then takes the minimum group score. The group axes are source partition with two hidden partitions, speaker-sex metadata with values `M`, `F`, or `unknown` when available, and duration groups defined from clip duration as `short` for less than 1.0 second, `medium` for 1.0 to under 1.35 seconds, and `long` for 1.35 seconds or longer.

`RowCore` is used only for calibration. It is `0.50 * known_reader_score_quality + 0.50 * provenance_exact`, where score quality is `max(0, 1 - abs(known_reader_score - is_known_reader))` and `provenance_exact` is 1 only for an exactly correct valid provenance string.

`Calibration` is the mean `max(0, 1 - abs(confidence - row_core))` over rows with valid knownness and provenance fields, so confidence should be high only when the row-level knownness and provenance evidence is likely correct.

The final score is `0.41*StrictRow + 0.20*WorstStrictGroup + 0.10*ProvenanceF1 + 0.10*Knownness + 0.05*ReaderConsistency + 0.14*Calibration`.

The theoretical minimum is `0.0`; the theoretical maximum is `1.0`; higher is better. A perfect submission with all hidden verdicts and confidence `1.0` scores exactly `1.0`.

### Intended Solution

Strong solutions should train or fine-tune open audio encoders, speaker-verification models, wav2vec2/HuBERT/Whisper-style feature extractors, ECAPA-style embeddings, or calibrated shallow models over robust acoustic features. Useful evidence includes timbre, pitch range, prosody, channel coloration, and reader-stable speech characteristics learned from the public examples, but the few-shot enrollment and short shifted clips require careful open-set calibration rather than simple closed-set matching.

Metadata-only, transcript-only, row-order, and filename approaches are intentionally weak. Closed-set speaker classification alone is incomplete because the test set includes readers absent from public training and requires calibrated `UNKNOWN` decisions.

### Enforcement On Invalid Approaches

Submissions based on direct source lookup, recovered original filenames, speaker ids, chapter ids, book ids, transcript search, exact or robust fingerprint matching against public audiobook archives, hosted commercial speaker-recognition APIs, manual hidden-test labeling, hardcoded id-to-answer maps, or grader/filesystem exploitation may be rejected before payout even if the CSV is structurally valid. The competition rewards learned open-set speech provenance modeling from the provided public training split.

## Tags

audio, speech, speaker-recognition, open-set, calibration

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

Do not use hosted commercial speech or speaker-recognition APIs, direct source row lookup, original filename/path/speaker/chapter/book reconstruction, transcript search, exact or robust audio fingerprint matching against public audiobook archives, row-order/id shortcuts, manual test labeling, hardcoded answer maps, or closed-set-only reader classification that cannot output `UNKNOWN`.

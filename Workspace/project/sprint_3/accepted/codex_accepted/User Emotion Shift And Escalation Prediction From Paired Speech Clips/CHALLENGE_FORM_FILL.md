# Challenge creation form - fill-in

## Difficulty

Hard

## Challenge Title

User Emotion Shift And Escalation Prediction From Paired Speech Clips

## Problem Description

Voice assistants often need to notice when a user sounds different from an earlier same-speaker baseline: calmer, more upset, more energetic, or more likely to require escalation. This challenge gives paired real speech clips and asks for a baseline-calibrated decision from the audio itself. The target is expressed or perceived affect from speech prosody, not a claim about the speaker's true internal emotion.

### Overview

Objective: for each baseline/current speech pair, listen to both clips and predict the current expressed affect, the direction of valence change, the direction of arousal change, the escalation tier, and a confidence for that complete row-level decision.

The audio is real English speech from multiple human actors recorded in controlled prompted-utterance sessions. Each public example is presented as a pair of short mono WAV clips with opaque paths and source-neutral channel rendering; original speaker ids, utterance ids, file names, sentence ids, source labels, and demographic fields are not public.

Each row contains two clips from the same speaker: a baseline/reference clip and a current/later clip. Pairs are built to cover stable, escalating, recovering, and cross-affect cases, so the model must compare the baseline and current prosody rather than classify a single clip in isolation. The split is speaker-held-out: no speaker appears in both public train and hidden test.

This setup is different from broad relative voice-impression scoring, where the goal is usually to rank which of two clips sounds more like a single attribute. It is also different from utterance-level escalation or intensity labeling, where one clip is classified in isolation or placed on a call trajectory. Here the baseline is a within-speaker reference point, and the submission must produce one complete monitoring decision: current expressed affect, valence direction, arousal direction, escalation tier, and confidence for the same row. A solution that only recognizes the current clip's affect, only estimates intensity, or only ranks "which clip sounds higher" leaves important parts of the target unresolved.

The central modeling problem is baseline-calibrated change detection with a consistency-constrained output bundle. The grader mainly rewards rows where all four categorical decisions are correct together, so a model must connect the baseline/current comparison to the final operational action instead of solving separate single-purpose subtasks.

For every test row, predict the current expressed affect category, whether valence shifted relative to the baseline, whether arousal shifted relative to the baseline, whether operational escalation is required, and an honest confidence. This is not a single-clip speech-emotion-recognition task: the required judgment is paired and relative, with a current-state label plus shift and escalation heads.

What not to use: hosted commercial speech or language APIs, external labeled emotion or speech-affect datasets, source-corpus lookup, audio fingerprint matching against public corpora, original filename reconstruction, speaker-id reconstruction, row-order/id tricks, manual test labeling, and hardcoded answer maps are prohibited. The intended route is to train or fine-tune an open speech, audio-text, or multimodal model on the public training pairs.

### Task Specification

`affect_label` is the perceived current-clip expressed affect category and must be one of `angry`, `sad`, `happy`, `neutral_or_unclear`, or `other_negative`. `other_negative` covers negative affect that is not cleanly anger or sadness in this schema.

`valence_shift` compares the current clip against the baseline clip and must be `positive`, `negative`, or `no_clear_shift`. `arousal_shift` compares the current clip against the baseline clip and must be `higher`, `lower`, or `no_clear_shift`. `escalation_tier` must be `none`, `monitor`, or `urgent`, reflecting the practical voice-agent decision from the paired speech evidence. `confidence` is a finite float in `[0, 1]` calibrated to the complete row-level prediction.

## Dataset

The public dataset contains `train.csv`, `test.csv`, `sample_submission.csv`, and WAV clips under `train/audio/` and `test/audio/`. Audio paths are relative to the public directory. Training rows include labels; test rows include only public inputs. `id` and `sample_id` are both opaque row identifiers and have the same value; both are included to satisfy platform row-id conventions and the pair-oriented task schema.

Exact `train.csv` columns are `id`, `sample_id`, `baseline_audio`, `current_audio`, `pair_duration_bucket`, `affect_label`, `valence_shift`, `arousal_shift`, `escalation_tier`, and `confidence`.

Exact `test.csv` columns are `id`, `sample_id`, `baseline_audio`, `current_audio`, and `pair_duration_bucket`.

`pair_duration_bucket` can be `short_pair`, `medium_pair`, or `long_pair`. It is based only on the combined duration of the baseline and current clips: `short_pair` is under 4.5 seconds, `medium_pair` is 4.5 to under 7.6 seconds, and `long_pair` is 7.6 seconds or longer.

### Public Files

| Item | Description |
|---|---|
| `train.csv` | labeled pair rows |
| `test.csv` | hidden-label pairs |
| `sample_submission.csv` | dummy format file |
| `train/audio/` | train WAV clips |
| `test/audio/` | test WAV clips |

The same public clip may appear in more than one pair within a split, but no speaker or source clip crosses between train and test. Public filenames are opaque and do not contain source labels.

### train.csv Columns

| Column | Type | Description |
|---|---|---|
| `id` | int | opaque row id |
| `sample_id` | int | opaque pair id |
| `baseline_audio` | string | baseline WAV path |
| `current_audio` | string | current WAV path |
| `pair_duration_bucket` | string | coarse duration bin |
| `affect_label` | string | current affect |
| `valence_shift` | string | valence change |
| `arousal_shift` | string | arousal change |
| `escalation_tier` | string | action tier |
| `confidence` | float | gold confidence |

The training labels use the allowed values listed in the task specification. `pair_duration_bucket` is a coarse public descriptor with values `short_pair`, `medium_pair`, or `long_pair`; it is not sufficient to solve the task without the paired speech clips.

### test.csv Columns

| Column | Type | Description |
|---|---|---|
| `id` | int | opaque row id |
| `sample_id` | int | opaque pair id |
| `baseline_audio` | string | baseline WAV path |
| `current_audio` | string | current WAV path |
| `pair_duration_bucket` | string | coarse duration bin |

The test file withholds all labels. The `id` and `sample_id` columns identify the row, `baseline_audio` points to the earlier reference clip, `current_audio` points to the later/current clip, and `pair_duration_bucket` gives only a coarse duration bin with values `short_pair`, `medium_pair`, or `long_pair`.

### Submission Format

| Column | Type | Constraint |
|---|---|---|
| `id` | int | exact test id |
| `sample_id` | int | exact test id |
| `affect_label` | string | allowed affect |
| `valence_shift` | string | allowed shift |
| `arousal_shift` | string | allowed shift |
| `escalation_tier` | string | allowed tier |
| `confidence` | float | 0 to 1 |

Submit exactly one row for every test `id` and `sample_id`, with columns in the exact order shown above. In each row `id` and `sample_id` must match. Missing, extra, or reordered columns make the submission structurally invalid.

```csv
id,sample_id,affect_label,valence_shift,arousal_shift,escalation_tier,confidence
102341,102341,angry,negative,higher,urgent,0.77
487221,487221,neutral_or_unclear,no_clear_shift,lower,none,0.61
750812,750812,sad,negative,no_clear_shift,monitor,0.58
```

The example rows are illustrative schema examples, not answer hints. In the first example, the submission says that the current clip sounds angry relative to the baseline, with a negative valence shift, higher arousal, and urgent escalation; `0.77` is the participant's self-estimated confidence in that complete row prediction.

### Evaluation

The official metric is `PairedDecisionScore`, a 0-to-1 composite score for paired speech monitoring. Its weights are fixed up front: `75%` strict full-row exactness, `10%` per-head macro-F1 bundle, and `15%` confidence calibration. In plain terms, most of the score comes from making the whole row correct: the current affect label, both shift directions, and the escalation tier should agree with each other for the same baseline/current pair. A perfect submission scores `1.0`; the theoretical minimum for a valid scored submission is `0.0`; the provided dummy/sample-style weak baseline is expected to score around `0.14` on this split.

Malformed submissions raise a validation error and are not scored. Invalidity includes missing, extra, or reordered columns; duplicate ids; mismatched `id` and `sample_id`; an id set different from `test.csv`; non-finite, missing, or out-of-range confidence; missing rows; and categorical values outside the allowed label sets. Valid submissions with wrong but well-formed labels are scored normally.

For valid submissions, the grader computes three transparent terms: a normalized categorical head bundle, a strict full-row exactness term, and a calibration term. Let `F1_affect`, `F1_valence`, `F1_arousal`, and `F1_escalation` be macro-F1 scores over the allowed classes for their respective heads. Define `CategoricalBundle = (0.18 * F1_affect + 0.17 * F1_valence + 0.16 * F1_arousal + 0.14 * F1_escalation) / 0.65`. The `0.65` divisor is the sum of the four head weights and normalizes the bundle into `[0, 1]`.

For row `i`, define exact-match indicators `A_i`, `V_i`, `R_i`, and `E_i`, each equal to `1` when the submitted `affect_label`, `valence_shift`, `arousal_shift`, or `escalation_tier` matches the hidden answer, and `0` otherwise. The row correctness used for calibration is `row_correctness_i = (0.18 * A_i + 0.17 * V_i + 0.16 * R_i + 0.14 * E_i) / 0.65`. Calibration is `mean_i(max(0, 1 - abs(confidence_i - row_correctness_i)))`.

Define `J_i = A_i * V_i * R_i * E_i`, so `J_i` is `1` only when all four categorical heads are correct for the same row. `StrictRowScore = (mean_i J_i)^5`; the fifth power intentionally punishes submissions that get many individual heads right but do not recover complete paired decisions.

Final score is `PairedDecisionScore = 0.10 * CategoricalBundle + 0.75 * StrictRowScore + 0.15 * Calibration`. These three final-score weights sum to `1.00`. The theoretical minimum for a valid scored submission is `0.0`; the theoretical maximum is `1.0`; higher is better. A perfect submission with confidence `1.0` scores exactly `1.0`.

### Intended Solution

Strong solutions should train or fine-tune open-weight speech or audio-text models such as wav2vec2/HuBERT-style encoders, Whisper-family encoders, conformers, or multimodal speech encoders on the provided paired examples. A good model should compare baseline and current prosody, energy, pitch contour, tempo, and voice quality rather than treating each current clip as an isolated emotion tag.

### Enforcement On Invalid Approaches

Submissions based on hosted commercial APIs, external labeled speech-affect corpora, direct source lookup, audio fingerprint matching, recovered source filenames, manual hidden-test labeling, hardcoded id-to-answer maps, or rule-only use of public metadata may be rejected before payout even if the CSV is structurally valid. The competition rewards learned paired speech modeling from the provided public training data.

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

Do not use hosted commercial speech or language APIs, external labeled speech-affect datasets, source-corpus lookup, audio fingerprint matching, original filename/speaker reconstruction, row-order/id tricks, manual test labeling, or hardcoded answer maps.

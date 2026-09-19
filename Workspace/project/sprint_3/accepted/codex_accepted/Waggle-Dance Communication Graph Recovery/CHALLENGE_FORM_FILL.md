# Challenge creation form - fill-in

## 1) Difficulty

Hard

## 2) Challenge Title

Waggle-Dance Communication Graph Recovery

## 3) Problem Description

# Waggle-Dance Communication Graph Recovery

## Overview

Plain language objective: recover who communicated with whom during a short honey-bee waggle-dance episode.

Each row is a short observation-hive episode containing many anonymized bees moving at once. The public input is a compressed trajectory file with relative public-clock time, local bee index, privacy-transformed x/y position, body orientation, tracking confidence, and local crowding summaries. The hidden record says which local bee was the dancer, when the waggle intervals occurred, which nearby bees were genuine followers versus attendees, and which directed dancer-to-follower communication edges were present.

This is a real animal-behavior reconstruction problem. A waggle dance is a brief communication signal embedded in dense social traffic: the dancer changes motion rhythm and heading, potential receivers track or inspect it for only part of the episode, and many nearby bees are incidental passersby. Useful predictions must recover the communication record from trajectory evidence rather than assign a single frame label.

This is not a single behavior label and not coordinate-value prediction. A valid answer is a structured communication record: dancer identity, ordered temporal intervals, participant roles, directed graph edges, and row confidence.

You must submit these five prediction fields for every test episode:

* `dancer_id`: one local bee ID such as `B17`.
* `waggle_intervals_json`: ordered interval objects.
* `roles_json`: follower or attendee roles.
* `edges_json`: directed dancer-to-follower edges.
* `confidence`: numeric row confidence in `[0,1]`.

Only CPU solutions are allowed. The solution runtime limit is 1.5 hours on 10 CPU cores and 62 GB RAM. Runtime internet use, source-data lookup, hidden-answer access, external hosted animal-tracking APIs, and private annotation lookup are not allowed.

## Task

For each test row, load the referenced episode NPZ and output one communication record. Identify the local dancer, segment the ordered waggle intervals on the public episode clock, separate true followers from attendees or passersby, and report the directed dancer-to-follower edges. The role and edge heads should be consistent with the dancer and intervals you predict: a row that names a follower should have trajectory evidence that this local bee attended the dancer during the waggle portion of the episode, not merely that it was nearby once.

The held-out rows are designed to test generalization across recording conditions, crowding, tracking quality, local bee identities, and dance structure. Public row IDs, file paths, row order, local bee IDs, and public-clock values are not source keys. A strong solution should learn reusable movement and interaction patterns from the labeled training episodes.

## Intended Approach

A practical CPU solution is to featurize the dense per-bee time series from the NPZ files, score dancer candidates from oscillatory motion, orientation changes, and repeated waggle-like bursts, then decode a compact set of temporal intervals. Follower and attendee candidates can be modeled from distance, relative orientation, motion synchrony, dwell time near the dancer, and before/during/after interval context. After those heads are predicted, construct edges from the predicted dancer to the follower candidates and postprocess the JSON so intervals, roles, and edges remain row-local and internally consistent.

Reasonable CPU methods include gradient-boosted trees or random forests over hand-built trajectory features, dynamic programming or HMM/CRF-style interval decoding, k-nearest or metric features for bee-pair interactions, and compact temporal neural models that run fully on CPU. Use only the released training labels for model selection. Build train-only validation folds that check crowding, tracking-confidence, comb-side, duration, and waggle-count behavior; calibrate the confidence column on those folds; and validate the exact submission format before scoring.

**What Not To Use / What Not To Do**:

* Do not look up original source files, dates, timestamps, raw bee IDs, frame IDs, track IDs, feeder IDs, or source annotations for hidden rows.
* Do not use runtime internet access or external copies of the raw source to identify test episodes.
* Do not use private files, hidden answers, row order, opaque-ID hashes, file sizes, filesystem metadata, or JSON length as answer channels.
* Do not submit a metadata-only, fixed-template, or rule-only solution that ignores the trajectory arrays.
* Do not reduce the task to one bee label, one interval count, or full continuous-coordinate prediction.
* Do not use closed-source teacher APIs, hosted tracking APIs, or external biological-behavior services for hidden-row interpretation.
* Do not exploit malformed JSON floods, duplicate IDs, extra columns, non-finite numbers, or grader/platform side channels.

Enforcement on invalid approaches: submissions may be reviewed for source lookup, runtime network use, hidden-file access, metadata-only behavior, and solutions that avoid the structured graph-recovery contract. Prohibited approaches can be rejected before payout even if the CSV is structurally valid.

## Dataset

The public prepared data contains labeled training episodes, hidden-label test episodes, and a sample submission. Episode files are compressed NumPy `.npz` files referenced from the CSVs. Public IDs are opaque and sorted; local bee IDs are remapped independently within each episode.

Prepared files:

| Item | Description |
|---|---|
| `train.csv` | Labeled train rows |
| `test.csv` | Test inputs only |
| `train/episodes/` | Train NPZ files |
| `test/episodes/` | Test NPZ files |
| `sample_submission.csv` | Valid weak template |

Each episode NPZ contains these arrays with equal length:

* `t_sec`: relative seconds in the public episode clock.
* `bee_index`: local integer bee index; `17` corresponds to `B17`.
* `x_mm`, `y_mm`: transformed relative hive-plane coordinates.
* `orientation_rad`: body orientation in radians after the same episode transform.
* `tracking_confidence`: tracker confidence in `[0,1]`.
* `neighbor_count_20mm`, `neighbor_count_40mm`: local crowding summaries.
* `dense_features`: bee-by-frame tensor with x, y, orientation, confidence, 20 mm count, and 40 mm count.
* `dense_mask`: `1` where the dense tensor has an observed detection.
* `dense_frame_hz`: dense tensor frame rate, always `6.0`.

`train.csv` contains the public input columns plus train-only target columns.

| Column | Type | Description |
|---|---|---|
| `id` | string | Opaque row id |
| `episode_npz` | path | Trajectory file |
| `duration_sec` | float | Episode length |
| `bee_count` | int | Local bee count |
| `comb_side` | string | Side A or B |
| `crowding_level` | string | Coarse crowding |
| `tracking_confidence_level` | string | Coarse quality |
| `dancer_id` | string | Train target |
| `waggle_intervals_json` | JSON | Train intervals |
| `roles_json` | JSON | Train roles |
| `edges_json` | JSON | Train edges |
| `label_quality` | float | Train weight |

Plain train column definitions: `id` is the opaque episode key; `episode_npz` points to the trajectory NPZ; `duration_sec` is the public-clock episode length; `bee_count` is the local bee count; `comb_side` is the anonymized side label; `crowding_level` is a coarse local-density bucket; `tracking_confidence_level` is a coarse trajectory-quality bucket; `dancer_id`, `waggle_intervals_json`, `roles_json`, and `edges_json` are train-only targets; `label_quality` is a train-only reliability weight.

`test.csv` has the same public input columns and none of the target columns.

| Column | Type | Description |
|---|---|---|
| `id` | string | Opaque row id |
| `episode_npz` | path | Trajectory file |
| `duration_sec` | float | Episode length |
| `bee_count` | int | Local bee count |
| `comb_side` | string | Side A or B |
| `crowding_level` | string | Coarse crowding |
| `tracking_confidence_level` | string | Coarse quality |

Plain test column definitions: `id` is the opaque episode key; `episode_npz` points to the trajectory NPZ; `duration_sec` is the public-clock episode length; `bee_count` is the local bee count; `comb_side` is the anonymized side label; `crowding_level` is a coarse local-density bucket; `tracking_confidence_level` is a coarse trajectory-quality bucket.

Target JSON schemas:

* `waggle_intervals_json` is a list of objects with exactly `start` and `end`, measured in relative seconds.
* `roles_json` is a list of objects with exactly `bee_id` and `role`. Role is `follower` or `attendee`.
* `edges_json` is a list of objects with exactly `source` and `target`, where the source should be the predicted dancer and the target should be a follower.

Local bee IDs use the format `B00`, `B01`, ... up to the episode bee count minus one. Intervals must satisfy `0 <= start <= end <= duration_sec`.

## Submission

Write the final CSV to `./working/submission.csv`. It must contain exactly these columns in this order and exactly one row for every test ID.

| Column | Type | Constraint |
|---|---|---|
| `id` | string | Same set as test |
| `dancer_id` | string | Local `Bxx` id |
| `waggle_intervals_json` | JSON | Max 30 intervals |
| `roles_json` | JSON | Max 48 roles |
| `edges_json` | JSON | Max 48 edges |
| `confidence` | float | In `[0,1]` |

Example:

```csv
id,dancer_id,waggle_intervals_json,roles_json,edges_json,confidence
wdg_0123456789abcd,B17,"[{""start"":2.15,""end"":2.82},{""start"":6.31,""end"":7.04}]","[{""bee_id"":""B04"",""role"":""follower""},{""bee_id"":""B12"",""role"":""attendee""}]","[{""source"":""B17"",""target"":""B04""}]",0.42
wdg_fedcba98765432,B03,"[{""start"":1.4,""end"":2.1}]","[{""bee_id"":""B08"",""role"":""follower""}]","[{""source"":""B03"",""target"":""B08""}]",0.31
```

Wrong columns, reordered columns, missing IDs, extra IDs, duplicate IDs, nonnumeric confidence, non-finite confidence, confidence outside `[0,1]`, oversized CSVs, or unreadable CSVs raise `InvalidSubmissionError`. Malformed row-local JSON, overlong JSON cells, invalid local bee IDs, invalid intervals, duplicate role IDs, or invalid edges give zero for the affected row rather than crashing the whole submission.

## Evaluation

Minimum score: `0.0`. Maximum score: `1.0`. Higher is better. A perfect submission with `confidence = 1.0` scores exactly `1.0`.

Each row receives component scores:

```
D = 1 if dancer_id is exact, else 0
I = greedy soft-F1 over waggle intervals
R = role F1 over follower/attendee objects
E = directed edge F1
K = graph consistency and joint credit

core = 0.18*D + 0.30*I + 0.22*R + 0.20*E + 0.10*K
powered = core ** 0.80
calibration = max(0, 1 - abs(confidence - powered))
count_score = geometric mean over interval, role, and edge count precision
count_penalty = 0.35 + 0.65*count_score
row_score = powered * (0.86 + 0.14*calibration) * count_penalty
```

Interval matching uses greedy one-to-one matching. A predicted and true interval can match only if interval IoU is at least `0.18`; the pair score combines IoU with center and length timing error. Role scoring rewards exact role recovery, participant identification, and follower identification. Edge scoring rewards exact directed dancer-to-follower edges and follower targets. The consistency term rewards edges whose source is the predicted dancer and whose targets are predicted followers, with extra joint credit when dancer, interval, role, and edge evidence agree.

The count precision term penalizes overbroad records that flood a row with too many intervals, roles, or edges. For each of the interval, role, and edge heads, the count ratio is `min(1, (true_count + slack) / max(true_count + slack, predicted_count + slack))`, with slack `2` for intervals, `2` for roles, and `1` for edges. `count_score` is the geometric mean of those three ratios. Underprediction is already handled by F1; this term mainly prevents valid-but-spammy submissions from receiving excessive recall credit.

The final score combines mean row performance with hidden worst-group robustness:

```
Final = 0.78 * mean(row_score)
      + 0.22 * mean(worst_group_scores)
```

Hidden groups cover crowding level, tracking-confidence level, dance duration, waggle-count bucket, comb side, and recording-session bucket. The grouping terms reward methods that work across sparse/crowded scenes, lower/higher tracking confidence, short/long dances, and both comb sides.

## 4) Tags

feature-engineering, small-data

## 5) Grading Configuration

Direction: higher is better

Theoretical minimum: 0.0

Theoretical maximum: 1.0

## 6) Grading Script

Paste the contents of `PASTE_THIS_GRADE.txt`.

## 7) Prepare Script

Paste the contents of `PASTE_THIS_PREPARE.txt`.

## 8) GPU Tier

CPU only. The maximum solution runtime is 1.5 hours on 10 CPU cores and 62 GB RAM.

## 9) What Not To Use

Do not use runtime internet, original source-file lookup, raw timestamp/date/bee/frame/track/dance/feeder ID reconstruction, external hidden annotations, private answers, metadata-only shortcuts, row-order or file-metadata side channels, hosted tracking APIs, closed-source teacher APIs, fixed templates that ignore trajectories, malformed submission exploits, or approaches that avoid the required temporal participant graph record.

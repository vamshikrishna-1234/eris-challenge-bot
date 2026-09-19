# Challenge creation form - fill-in

## 1) Difficulty

Hard

## 2) Challenge Title

Real Robot Handover Command Timeline Reconstruction

## 3) Problem Description

# Real Robot Handover Command Timeline Reconstruction

## Overview

In plain language, the objective is to reconstruct a short robot handover command timeline for each real robot demonstration video.

The data comes from lab demonstrations with Panda-style robot arms. During each demonstration, the arms perform a handover-like motion while synchronized RGB video, depth video, joint trajectories, and Cartesian end-effector trajectories are recorded. Participants receive prepared RGB/depth clips and a coarse state sketch; the hidden labels are derived from the real robot trajectories.

A command timeline is a compact summary of the robot behavior. It says when the robot is moving or waiting, which arm is involved, where important binned waypoints occur, which event frames look like motion start, handover pause, release, or motion stop, and how confident the reconstruction is. This is not a task about predicting every continuous coordinate and it is not a single action label.

You must predict four fields: `controller_segments_json`, `key_waypoints_json`, `event_frames_json`, and `confidence`.

The four required prediction fields are:

* `controller_segments_json`: an ordered JSON list of motion intervals.
* `key_waypoints_json`: a JSON list of important binned waypoints.
* `event_frames_json`: a JSON list of key event frames.
* `confidence`: a numeric confidence value from 0 to 1.

| Output | What it represents |
|---|---|
| `controller_segments_json` | Ordered motion intervals |
| `key_waypoints_json` | Binned waypoint list |
| `event_frames_json` | Key event-frame list |
| `confidence` | Row confidence in `[0,1]` |

Prepared videos are 48-frame MP4 clips at 160 x 120 resolution and 12 fps, so each clip covers about four seconds on a common frame timeline numbered 0 through 47. RGB and depth clips for the same row are aligned to that timeline.

The challenge is CPU-only. The runtime has 10 CPU cores and 62 GB RAM with a maximum runtime of 1.5 hours. Practical solutions can use frame sampling, optical flow or frame differences, robot-arm motion features, the binned state sketch, compact multi-head models, and constrained decoding to produce valid ordered JSON.

The source trajectories do not include explicit gripper-width labels, so the target does not ask for true gripper-open or gripper-close events. The event fields are derived from motion timing and trajectory pauses.

## Dataset

The prepared split contains 120 training rows and 40 test rows. Every prepared RGB and depth clip has 48 frames at 160 x 120 resolution and 12 fps.

| Item | Value |
|---|---:|
| Training rows | 120 |
| Test rows | 40 |
| Frames per video | 48 |
| Video size | 160 x 120 |
| Frame rate | 12 fps |

Prepared files:

The public prepared files are:

* `train.csv`: labeled training rows with video paths, state inputs, and target fields.
* `test.csv`: held-out test rows with video paths and state inputs only.
* `train/videos/`: MP4 clips referenced by `train.csv`.
* `test/videos/`: MP4 clips referenced by `test.csv`.
* `sample_submission.csv`: a correctly formatted submission template.

| Item | Description |
|---|---|
| `train.csv` | Labeled train rows |
| `test.csv` | Test rows, no labels |
| `train/videos/` | Train MP4 clips |
| `test/videos/` | Test MP4 clips |
| `sample_submission.csv` | Submission template |

`train.csv` and `test.csv` input columns:

Both `train.csv` and `test.csv` contain exactly these input columns:

* `id`: opaque row ID.
* `rgb_video`: relative path to the 48-frame RGB MP4 clip.
* `depth_video`: relative path to the aligned 48-frame depth MP4 clip.
* `state_observation_json`: JSON state sketch input with `observed_frames` and `state_sketch_bins`.
* `duration_frames`: integer clip duration, always 48.

| Column | Type | Description |
|---|---|---|
| `id` | string | Opaque row ID |
| `rgb_video` | path | 48-frame RGB MP4 |
| `depth_video` | path | 48-frame depth MP4 |
| `state_observation_json` | JSON | State sketch input |
| `duration_frames` | int | Always 48 |

Training target columns in `train.csv`:

The train-only target columns are:

* `controller_segments_json`: target segment-object list.
* `key_waypoints_json`: target waypoint-object list.
* `event_frames_json`: target event-object list.
* `trace_quality`: training-only label-quality float in `[0, 1]`.

| Column | Type | Description |
|---|---|---|
| `controller_segments_json` | JSON | Segment-object list |
| `key_waypoints_json` | JSON | Waypoint-object list |
| `event_frames_json` | JSON | Event-object list |
| `trace_quality` | float | Label quality in `[0,1]` |

`test.csv` has only the input columns. `train.csv` has the input columns plus the four training target columns.

`state_observation_json` is an input JSON object with two keys. `observed_frames` is a list of public frame indices from 0 through 47. `state_sketch_bins` is a 16-integer coarse summary of early robot state, with each integer from 0 to 15. This is partial state context, not the full trajectory.

Target value details:

| Field | Valid structure |
|---|---|
| Segment object | `mode`, `arm`, `start_frame`, `end_frame` |
| Waypoint object | `arm`, `kind`, `frame`, `xyz_bins` |
| Event object | `event`, `arm`, `frame` |

Allowed segment modes are `joint_move`, `cartesian_move`, `wait`, and `contact_like_pause`. Segment arms are `giver`, `receiver`, or `both`. Segment frame values must be integers from 0 through 47, with `end_frame >= start_frame`.

Allowed waypoint kinds are `start`, `approach`, `handover`, `retreat`, and `end`. Waypoint arms are `giver` or `receiver`. `xyz_bins` is a length-3 integer list; each bin is from 0 through 9.

Allowed event types are `motion_start`, `handover_pause`, `release_like`, and `motion_stop`. Event arms are `giver`, `receiver`, or `both`. Event frames are integers from 0 through 47.

`trace_quality` is a training-only float in `[0, 1]`. It is derived from motion strength and handover-like trajectory geometry. Higher values mean the derived command summary is clearer; it may be used as an optional training weight.

## Submission

Write the final CSV to `./working/submission.csv`. The submission must contain exactly these columns in this order: `id`, `controller_segments_json`, `key_waypoints_json`, `event_frames_json`, and `confidence`.

Required submission columns:

* `id`: copied from `test.csv`.
* `controller_segments_json`: JSON list with at most 12 segment objects.
* `key_waypoints_json`: JSON list with at most 12 waypoint objects.
* `event_frames_json`: JSON list with at most 8 event objects.
* `confidence`: finite float from 0 to 1.

| Column | Type | Constraint |
|---|---|---|
| `id` | string | From `test.csv` |
| `controller_segments_json` | JSON | Max 12 objects |
| `key_waypoints_json` | JSON | Max 12 objects |
| `event_frames_json` | JSON | Max 8 objects |
| `confidence` | float | 0 to 1 |

Every `id` from `test.csv` must appear exactly once. Extra columns, missing columns, reordered columns, duplicate IDs, wrong row count, missing test IDs, extra IDs, nonnumeric confidence, or confidence outside `[0, 1]` cause the submission to score 0.0.

Example:

```csv
id,controller_segments_json,key_waypoints_json,event_frames_json,confidence
rctr_a1b2c3d4e5f6,"[{""mode"":""wait"",""arm"":""both"",""start_frame"":0,""end_frame"":3}]","[{""arm"":""giver"",""kind"":""start"",""frame"":0,""xyz_bins"":[3,1,4]}]","[{""event"":""motion_start"",""arm"":""both"",""frame"":3}]",0.25
rctr_f6e5d4c3b2a1,"[{""mode"":""cartesian_move"",""arm"":""giver"",""start_frame"":2,""end_frame"":22}]","[{""arm"":""receiver"",""kind"":""handover"",""frame"":18,""xyz_bins"":[4,5,6]}]","[{""event"":""handover_pause"",""arm"":""both"",""frame"":18}]",0.35
```

## Evaluation

Minimum score: 0.0. Maximum score: 1.0. Higher is better. A perfect label submission with `confidence = 1.0` scores exactly 1.0.

The final score is `mean(row_score over test rows)`, clipped to `[0, 1]`.

Component weights are: segments `0.55`, waypoints `0.25`, events `0.20`, and a confidence multiplier worth at most `0.15` of already-earned structured-output credit.

For each of the three object-list heads, the grader computes a greedy soft-F1. All positive prediction/gold pair scores are sorted from high to low. Each prediction and each gold object may be matched once. Precision is `matched_sum / max(1, number_of_predictions)`, recall is `matched_sum / max(1, number_of_gold_objects)`, and `greedy_f1 = 2 * precision * recall / (precision + recall)`. If both lists are empty, that head score is 1.0; if only one list is empty, it is 0.0.

Segment pair score: mode and arm must match. The frame intervals use inclusive interval IoU. If IoU is below `0.55`, the pair score is `0`. Otherwise `segment_pair = 0.75 * interval_iou + 0.25 * max(0, 1 - (abs(start_error) + abs(end_error)) / 12)`.

Waypoint pair score: arm and kind must match. `frame_score = max(0, 1 - abs(frame_error) / 6)`. `bin_score = max(0, 1 - L1(xyz_bins_error) / 4)`. The pair score is `0.5 * frame_score + 0.5 * bin_score`, but it is set to `0` if below `0.60`.

Event pair score: event type and arm must match. Otherwise the pair score is `max(0, 1 - abs(frame_error) / 5)`.

Row score formula: `core = 0.55 * segment_score + 0.25 * waypoint_score + 0.20 * event_score`; `powered_core = core ** 3.20`; `calibration = max(0, 1 - abs(confidence - powered_core))`; `row_score = powered_core * (0.85 + 0.15 * calibration)`.

Confidence can only multiply earned structured-output credit. If the command reconstruction is all wrong, `powered_core` is 0 and the row scores 0 regardless of confidence.

Malformed row-local JSON, wrong object schemas, overlong JSON cells, too many objects, invalid frame values, invalid bins, or invalid labels give zero for the affected row. Structural CSV errors such as wrong columns, missing IDs, duplicate IDs, mismatched rows, nonnumeric confidence, or out-of-range confidence make the whole submission score 0.0.

## What Not To Use / What Not To Do

Using these approaches can cause solution rejection regardless of score:

* Do not look up original source filenames, trial IDs, raw archive row IDs, or source annotations for hidden rows.
* Do not use external hosted video, robotics, or robot-foundation-model APIs.
* Do not solve the task as full continuous trajectory regression only; the submission must provide the structured command-timeline fields.
* Do not submit a rule-only template that ignores the video and state evidence.
* Do not use hidden/private answers, raw source lookup, metadata-only matching, row-order side channels, opaque-ID hashes, path strings, file sizes, filesystem metadata, or JSON length as answer channels.
* Do not use closed-source teacher APIs for labels, distillation, pseudo-labeling, or hidden-row interpretation.
* Do not exploit malformed JSON floods, duplicate IDs, extra columns, non-finite numbers, or grader/platform side channels.

Enforcement on invalid approaches: invalid or prohibited approaches may be rejected before payout even if they produce a score. The task is meant to reward learned reconstruction of robot handover commands from the provided video and state evidence.

## 4) Tags

robotics, computer-vision, multimodal, sequence-modeling, structured-prediction, real-data

## 5) Grading Configuration

Direction: higher is better

Theoretical minimum: 0.0

Theoretical maximum: 1.0

## 6) Grading Script

Paste the contents of `PASTE_THIS_GRADE.txt`.

## 7) Prepare Script

Paste the contents of `PASTE_THIS_PREPARE.txt`.

## 8) GPU Tier

CPU only

## 9) What Not To Use

Do not use original source filename/trial-ID lookup, source annotation lookup for hidden rows, metadata-only solutions, rule-only template decoding, row-order or file-metadata side channels, external hosted video/robotics APIs, closed-source teacher APIs, hidden/private answer leakage, grader exploits, or approaches that reduce the task to continuous trajectory regression only.

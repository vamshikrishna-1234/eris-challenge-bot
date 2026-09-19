# Challenge form - fill-in

## 1) Difficulty

Medium

## 2) Challenge Title

Visual-Inertial Tracking Failure Detection and Localization

## 3) Problem Description

# Visual-Inertial Tracking Failure Detection and Localization

## Overview

Plain language objective: look at a real headset camera-and-motion window, find where tracking went bad, and write the repair ledger an AR/VR runtime would need. An AR/VR headset must keep a stable estimate of where it is in a room even when rapid motion, texture loss, or temporary visual-inertial disagreement makes tracking unreliable.

For each short real headset window, infer a compact failure and repair ledger: which keyframes are trustworthy, where the tracking trace drifted or was lost, which earlier anchor should be used to reconnect the path, the dominant failure state, and the row uncertainty.

This is not a plain SLAM trajectory benchmark, continuous pose regression task, or single scene label. The public input includes real camera evidence, real inertial summaries, and a degraded partial pose trace. The output is a discrete structured audit record whose pieces must agree with one another.

Only CPU solutions are allowed. Submissions must be reproducible within 1.5 hours on 10 CPU cores and 62 GB RAM. The intended solution is a learned visual-inertial audit model trained only on the released training rows, not a lookup against the upstream archive or a hand-coded reconstruction of hidden reference trajectories.

What Not To Use / What Not To Do, violation may cause rejection regardless of score:

- Do not reverse-map rows to original recording names, timestamps, frame filenames, or source archive paths.
- Do not download, index, or search the upstream visual-inertial archive to recover hidden reference trajectories.
- Do not use source-row lookup, perceptual frame matching, raw image hashes, ZIP member order, file sizes, row order, salted IDs, or path strings as answer channels.
- Do not inspect private answers, grader internals, filesystem side channels, hidden platform state, or prepare-script outputs that are not in `public/`.
- Do not submit a metadata-only solution that ignores camera panels, IMU evidence, and degraded pose.
- Do not reduce the task to continuous pose regression or a single failure-type label; all ledger heads are required.
- Do not use GPU computation, hosted APIs, remote inference services, closed-source teacher APIs, external labels, runtime-downloaded model weights, or challenge-specific pretrained checkpoints.
- Do not exploit malformed JSON, duplicate IDs, extra columns, non-finite values, or other grader attacks.

Enforcement on invalid approaches: solutions may be reviewed for actual use of visual and inertial evidence, source-lookup code, remote calls, hidden-answer access, and rule-only behavior. The goal is to reward learned operational tracking-audit models, not lookup tables or format exploits.

## Task

For each test row, read the frame panel, the IMU trace, and the degraded pose trace. Submit:

- `reliable_keyframes_json`: keyframe indices that remain trustworthy.
- `failure_spans_json`: contiguous unreliable frame ranges with failure type and severity.
- `anchor_edges_json`: repair links from a current keyframe to an earlier anchor keyframe.
- `failure_type`: the dominant row state.
- `uncertainty`: calibrated uncertainty in the ledger.

Keyframe indices are integers from 0 through 17. The four images in each panel are ordered top-left, top-right, bottom-left, bottom-right and correspond to keyframes 0, 5, 11, and 17. The IMU and degraded pose JSON arrays provide one object per keyframe.

The test rows are not a lookup exercise. Related source recordings are kept out of the opposite split, and public IDs, panel filenames, paths, and row order are opaque, so useful models need to generalize from the labelled training windows to unseen headset motion and room appearances.

## Intended Approach

A practical CPU solution is to build a compact multimodal model from `train.csv`. Decode the IMU and degraded-pose arrays into per-keyframe time-series features, extract visual evidence from the four panel tiles, and train models that estimate keyframe reliability, failure-span probabilities, anchor candidates, dominant failure state, and uncertainty. Reasonable visual features include local texture, edge density, blur/contrast cues, tile-to-tile differences, ORB/SIFT-style descriptors, optical-flow-like summaries, small CPU CNN features, or lightweight self-supervised embeddings computed locally.

Another reasonable route is a two-stage ledger pipeline. First predict per-keyframe reliability and failure likelihood from image-panel, IMU, and degraded-pose evidence using random forests, gradient boosting, k-nearest-neighbor features, compact 1D sequence models, or shallow CPU neural networks. Then decode those probabilities into contiguous spans, backward anchor edges, a row-level failure type, and a calibrated uncertainty value. The submitted heads should be mutually consistent: reliable keyframes should not sit inside failure spans, anchor edges should repair or reconnect to earlier stable keyframes, and the dominant failure type should agree with the span evidence.

Use only the released training labels for model selection. Make validation folds from `train.csv` that are robust to row-order and metadata shortcuts, for example by stratifying on `device_family`, `motion_hint`, failure type, and coarse visual clusters parsed from `window_meta_json` and the public panels. Check both the individual heads and the final ledger score on training-only validation folds. Calibrate numeric uncertainty and span severity on validation predictions so values stay in `[0,1]` and reflect actual ambiguity rather than acting as constants. Open-source local CV and time-series libraries, classical features, and generic offline pretrained vision features are allowed if they run under the CPU limit and do not use upstream source annotations, hidden test information, hosted APIs, or runtime downloads.

## Evaluation

Each row receives six head scores. Higher is better.

```
S_reliable = F1 over reliable keyframe sets
S_spans    = greedy interval IoU-F1 for failure spans
S_edges    = F1 over (current, anchor) repair edges
S_type     = exact dominant failure state with small related-state credit
S_uncert   = exp(-abs(pred - true) / 0.18)
S_consist  = internal ledger consistency score

raw = 0.22*S_reliable + 0.30*S_spans + 0.18*S_edges
    + 0.16*S_type + 0.10*S_uncert + 0.04*S_consist
row_score = raw ** 1.55
```

Span matching uses greedy one-to-one matches with interval IoU at least 0.25. Span severity contributes to matched-span credit. `S_consist` checks that reliable keyframes do not fall inside submitted failure spans, repair anchors point backward, and row failure type is compatible with the span list.

The final score uses worst-group aggregation, blending mean row quality with the lowest private subgroup minimum mean:

```
Final = 0.78 * mean(row_score)
      + 0.08 * worst_device_group
      + 0.08 * worst_motion_group
      + 0.06 * worst_failure_group
```

The theoretical minimum is 0.0 and the theoretical maximum is 1.0. A perfect submission scores exactly 1.0. A structural submission failure returns 0.0. Malformed row-local content, invalid enums, or over-long JSON make the affected row score zero without crashing the grader.

The grader requires exactly the submission columns in the listed order, one row per test ID, unique IDs, and the exact test ID set. `uncertainty` must be finite and in `[0,1]`.

## Dataset

The prepared data is under `public/`. Image paths are relative to the `public/` root. The frame panels are redacted, low-fidelity visual evidence derived from short real headset-camera neighborhoods; they are not raw upstream frame copies.

File overview:

| Item | Description |
|---|---|
| `train.csv` | Inputs and labels |
| `test.csv` | Test inputs only |
| `sample_submission.csv` | Weak valid template |
| `train/panels/*.jpg` | Train frame panels |
| `test/panels/*.jpg` | Test frame panels |

`train.csv` has 328 rows. `test.csv` has 479 rows. Entire source recordings are held out, so no recording contributes windows to both train and test. Public IDs, panel filenames, and paths are opaque and salted.

`train.csv` columns:

| Column | Type | Description |
|---|---|---|
| `id` | string | Opaque row ID |
| `image` | string | Panel image path |
| `imu_trace_json` | string | IMU evidence array |
| `degraded_pose_json` | string | Partial pose array |
| `window_meta_json` | string | Coarse row context |
| `prompt` | string | Task instruction |
| `reliable_keyframes_json` | string | Train label set |
| `failure_spans_json` | string | Train span labels |
| `anchor_edges_json` | string | Train repair edges |
| `failure_type` | string | Train row state |
| `uncertainty` | float | Train uncertainty |

`test.csv` columns:

| Column | Type | Description |
|---|---|---|
| `id` | string | Opaque row ID |
| `image` | string | Panel image path |
| `imu_trace_json` | string | IMU evidence array |
| `degraded_pose_json` | string | Partial pose array |
| `window_meta_json` | string | Coarse row context |
| `prompt` | string | Task instruction |

The test input columns are `id`, `image`, `imu_trace_json`, `degraded_pose_json`, `window_meta_json`, and `prompt`. `sample_submission.csv` is a weak valid template for the required output schema.

`imu_trace_json` is an array of 18 objects. Each object has `k`, `gyro_mean`, `gyro_peak`, `acc_dev`, and `frame_delta`. Values are finite real numbers derived from the headset sensor stream and neighboring camera frames.

`degraded_pose_json` is an array of 18 objects. Each object has `k` and `observed`. If `observed` is true it also has `x`, `y`, `z`, and `yaw`, all in row-local coordinates. If `observed` is false the pose is unavailable for that keyframe.

`window_meta_json` has `device_family`, `motion_hint`, `keyframe_count`, and `panel_order`. Device and motion hints are coarse anonymous context fields; they are not stable row identities and test recordings are held out.

Train-only labels use these schemas:

- `reliable_keyframes_json`: JSON list of unique integers from 0 to 17.
- `failure_spans_json`: JSON list of up to five objects with `start`, `end`, `type`, and `severity`.
- `anchor_edges_json`: JSON list of up to five objects with `current` and `anchor`.
- `failure_type`: one of `ok`, `drift`, `lost_tracking`, `relocalized`, or `uncertain`.
- `uncertainty`: finite float in `[0,1]`.

## Submission

Write the final submission CSV to exactly `./working/submission.csv`. It must contain exactly these six columns in this order and exactly one row for every test ID.

| Column | Type | Constraint |
|---|---|---|
| `id` | string | Same set as test |
| `reliable_keyframes_json` | string | JSON keyframe list |
| `failure_spans_json` | string | JSON span list |
| `anchor_edges_json` | string | JSON edge list |
| `failure_type` | string | Allowed enum |
| `uncertainty` | float | In `[0,1]` |

Example:

```csv
id,reliable_keyframes_json,failure_spans_json,anchor_edges_json,failure_type,uncertainty
hvit_0123456789abcdef01,"[0,4,9,14]","[{""start"":7,""end"":11,""type"":""drift"",""severity"":0.52}]","[{""current"":12,""anchor"":4}]",drift,0.47
hvit_abcdef012345678901,"[1,6,12,17]","[]","[]",ok,0.18
```

Requirements are strict: start from `sample_submission.csv` or write the same header yourself, preserve exactly one row per test `id`, keep the columns in the table order, and do not add extra columns. Duplicate IDs, missing IDs, extra IDs, reordered columns, non-finite uncertainty, or uncertainty outside `[0,1]` make the whole submission score `0.0`. Malformed or over-long row-local JSON, invalid keyframe/span/edge ranges, invalid span types, or invalid `failure_type` values make the affected row score zero.

## 4) Tags

Computer Vision, Sensor Fusion, Robotics, Structured Prediction, CPU

## 5) Grading Configuration

Direction: Higher is better

Theoretical minimum: 0.0

Theoretical maximum: 1.0

## 6) Grading Script

Use the contents of `PASTE_THIS_GRADE.txt`.

## 7) Prepare Script

Use the contents of `PASTE_THIS_PREPARE.txt`.

## 8) GPU Tier

None / CPU-only. The solver runtime limit is 1.5 hours on 10 CPU cores and 62 GB RAM.

## 9) What Not To Use

Do not use GPU computation, hosted APIs, runtime-downloaded model weights, source archive lookup, upstream trajectory files, source-row matching, raw filenames, original timestamps, hidden answer files, grader probing, metadata-only shortcuts, malformed JSON exploits, or any approach that ignores the required visual-inertial ledger contract.

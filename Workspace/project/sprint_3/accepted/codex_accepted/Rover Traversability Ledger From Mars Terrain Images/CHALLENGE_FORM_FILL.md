# Challenge creation form — fill-in

## 1) Difficulty

**Select: Hard**

The solver must recover a compact terrain map from real grayscale Mars imagery and use the supplied image-plane route corridor to produce mutually consistent hazards, a route decision, and four geometric/reliability measures. Unknown expert coverage and small rock components make the output more demanding than a single terrain class, while the compact 526-image corpus rewards CPU-efficient modelling and calibrated spatial priors rather than scale.

## 2) Challenge Title

```
Mars Rover Route Safety Ledger from Real Terrain Images
```

## 3) Problem Description

# Mars Rover Route Safety Ledger from Real Terrain Images

## Overview

Plain language objective: infer which ground patches are safe, where the hazards are, and whether the proposed corridor should be driven.

You receive a real Mars rover Navcam image, coarse real mission/camera context, and a normalized image-plane route corridor. Predict an operational traversability evidence ledger that shows terrain regions, locates major rock or unknown hazards, decides whether the queried corridor is safe, slow, avoid, or uncertain, and quantifies clearance, blockage, connected safe width, and annotation uncertainty.

This is not plain terrain classification or a segmentation-only task. A valid answer contains a compact region map plus route-conditioned structured and numeric evidence. The mask uses the real source taxonomy `0=soil`, `1=bedrock`, `2=sand`, `3=big_rock`, and `255=unknown`. There is no wheel-track, slope, GPS, depth, rover-pose, or synthetic route-outcome label.

The route query is normalized to the image: `(0,0)` is the top-left and `(1,1)` is the bottom-right. `route_query_json` contains `route_name`, `start_x`, `start_y`, `end_x`, `end_y`, and `half_width`. The corridor is the set of pixels no farther than `half_width` from the supplied line segment.

For every row, submit these seven outputs:

1. `terrain_mask_rle`: a row-major 32 × 32 region map over the five allowed class values.
2. `hazard_boxes_json`: up to eight normalized boxes around connected `big_rock` or substantial `unknown` regions.
3. `route_safety_class`: one of `safe_to_drive`, `drive_slowly`, `avoid_area`, or `uncertain`.
4. `clearance_score`: mean route passability in `[0,1]`.
5. `obstacle_coverage`: fraction of route pixels that are `big_rock`.
6. `safe_corridor_width`: robust connected nonblocked width in `[0,1]`.
7. `uncertainty_score`: reliability penalty from real unknown-mask coverage in `[0,1]`.

The compact mask JSON has exactly this schema:

```json
{"shape":[32,32],"counts":[[255,120],[0,450],[1,300],[2,150],[3,4]]}
```

`counts` is a list of `[class_value,run_length]` pairs whose positive lengths sum to 1024. Runs are row-major and class values must be in `{0,1,2,3,255}`.

Each hazard box is an object with exactly `kind,x,y,w,h`. `kind` is `big_rock` or `unknown`; coordinates and sizes are normalized finite values in `[0,1]`; width and height are positive; and each box must remain inside the image. Example:

```json
[{"kind":"big_rock","x":0.44,"y":0.57,"w":0.12,"h":0.09}]
```

The reference ledger is deterministic from the real mask. `clearance_score` is the corridor mean with weights soil `1.00`, bedrock `0.95`, sand `0.55`, big rock `0.00`, and unknown `0.25`. `obstacle_coverage` is the big-rock fraction in the corridor. `uncertainty_score = 0.75 * route_unknown_fraction + 0.25 * full_mask_unknown_fraction`. `safe_corridor_width` samples 15 points along the route, measures the horizontal connected run of pixels that are neither big rock nor unknown around each point, normalizes by image width, and takes the 20th percentile.

The route class is `uncertain` when uncertainty is at least `0.32`; otherwise it is `avoid_area` when obstacle coverage is at least `0.14`, clearance is below `0.44`, or safe width is below `0.08`; otherwise it is `drive_slowly` when obstacle coverage is at least `0.035`, sand coverage is at least `0.32`, clearance is below `0.76`, or safe width is below `0.18`; remaining rows are `safe_to_drive`.

`hazard_boxes_json` contains 4-connected component boxes from the 32 × 32 map: big-rock components require at least two cells and unknown components require at least 20 cells. The eight largest qualifying components are retained.

Only CPU solutions are allowed. The maximum solution time is 1.5 hours on 10 CPU cores and 62 GB RAM. Credible approaches include 384-pixel image features, classical texture/superpixel models, random forests, compact CPU segmentation networks, shallow encoder-decoders, and train-time feature extraction. GPU foundation-model fine-tuning is neither required nor allowed.

**What Not To Use / What Not To Do** (violation may cause rejection regardless of score):

* Do not use an original AI4MARS filename, image-id, product-id, or source-annotation lookup for hidden rows.
* Do not download or index the upstream masks to recover private answers, including perceptual image retrieval against the named source.
* Do not submit a metadata-only solution that ignores image pixels.
* Do not decode salted IDs, row order, file order, mtimes, JPEG sizes, or path strings as answer channels.
* Do not use a rule-only template that predicts one fixed mask/ledger without learning from images.
* Do not reduce the task to one scene-level terrain class or only `route_safety_class`; all spatial and numeric heads are required.
* Do not use external hosted image, segmentation, vision-language, or inference APIs.
* Do not use closed-source teacher APIs for labels, distillation, or pseudo-labelling.
* Do not inspect `private/answers.csv`, grader internals, filesystem side channels, or hidden platform state.
* Do not use malformed JSON floods, non-finite numbers, extra columns, duplicate IDs, or other format/grader exploits.

**Enforcement on invalid approaches:** solutions may be reviewed for actual image use, source-lookup code, external calls, and rule-only behaviour. Metadata-only models, source retrieval, hosted APIs, hidden-answer access, or submissions that avoid the required spatial evidence contract may be rejected before payout.

## Task

For each test row, read the rover image and the route corridor, then output a route-conditioned terrain evidence ledger. The central object is the 32 × 32 terrain map: the hazard boxes, route class, and numeric route measures should be consistent with the terrain you predict, not independent guesses. A strong submission should identify sand/soil/bedrock texture, isolate rock or unknown components, and reason about whether the specific corridor has enough clear connected ground for a rover to traverse.

The test rows are not a lookup exercise. Related rover/source image families are kept together, and the public IDs and file paths are opaque, so useful models need to generalize from the labelled training images to unseen rover terrain appearances and route placements.

## Intended Approach and Validation

A practical CPU solution is to train a compact image-to-mask model on `train.csv`: decode the training `terrain_mask_rle` labels, resize or featurize each image, and learn a 32 × 32 terrain predictor using a lightweight U-Net, shallow encoder-decoder, random forest over patch features, superpixel classifier, or k-nearest/gradient-boosted texture model. After predicting the terrain map, derive hazard boxes and route metrics from that predicted map using the public geometry definitions, optionally with small calibration models for the route class and numeric heads.

Another reasonable route is a two-stage CPU pipeline: first produce per-cell terrain probabilities from local intensity, texture, gradient, and neighborhood features; then apply connected-component cleanup and route-corridor postprocessing to produce `hazard_boxes_json`, `clearance_score`, `obstacle_coverage`, `safe_corridor_width`, `uncertainty_score`, and `route_safety_class`. This is still a visual modeling task: the route text tells you where to evaluate the image, but it does not contain the answer.

Use only the released training labels for model selection. Make your own validation folds from `train.csv`—for example stratified by mission, route family, and visual texture clusters—and check both mask quality and the downstream ledger heads. Calibrate numeric outputs on training-only validation folds so they stay in `[0,1]` and remain consistent with the predicted mask. Open-source local CV libraries, classical features, and generic offline pretrained vision features are allowed if they run under the CPU limit and do not use AI4MARS source annotations or hidden test information.

## Evaluation

Each row receives seven head scores. Higher is better.

```
S_mask   = mean IoU over present classes 0,1,2,3,255
S_boxes  = class-aware greedy IoU-F1 for boxes with IoU >= 0.30
S_route  = 1 for exact route class, else 0
S_clear  = exp(-abs(error) / 0.14)
S_block  = exp(-abs(error) / 0.07)
S_width  = exp(-abs(error) / 0.14)
S_uncert = exp(-abs(error) / 0.14)

independent = 0.34*S_mask + 0.14*S_boxes + 0.15*S_route
            + 0.10*S_clear + 0.10*S_block + 0.09*S_width
            + 0.08*S_uncert

joint = sqrt(S_mask * (0.45*S_route
             + 0.55*min(S_clear,S_block,S_width,S_uncert)))

row_score = independent * (0.70 + 0.30*joint)
```

The final score combines mean performance with the weakest real private subgroup along mission, terrain condition, and route family:

```
Final = 0.76 * mean(row_score)
      + 0.10 * worst_mission(row_score)
      + 0.08 * worst_terrain(row_score)
      + 0.06 * worst_route(row_score)
```

The worst-group terms are the lowest minimum mean row score over the private mission, terrain-family, and route-family buckets.

The minimum is `0.0` and the maximum is `1.0`. A perfect submission scores exactly `1.0`.

The grader requires exactly the listed columns in the listed order, one row per test ID, unique IDs, and the exact test ID set. A structural failure, any non-finite numeric field, or any numeric value outside `[0,1]` raises `InvalidSubmissionError`. Malformed or over-long row-local mask/box JSON, or an invalid route class string, scores zero for that row and does not crash the grader.

## Dataset

The public corpus contains prepared 384 × 384 grayscale JPEGs with opaque salted IDs. `mission` is Curiosity, Spirit, or Opportunity; `camera` is Navcam. Related rover/time/product sequence families stay in one split. Original source filenames and product IDs are absent.

### File overview

| Item | Description |
|---|---|
| `train/images/*.jpg` | Training images |
| `test/images/*.jpg` | Test images |
| `train.csv` | Inputs and labels |
| `test.csv` | Test inputs |
| `sample_submission.csv` | Weak constant template |

### train.csv columns

`train.csv` contains the eight public input columns and all seven target columns.

| Column | Type | Description |
|---|---|---|
| `id` | string | Opaque row id |
| `image` | string | JPEG path |
| `mission` | string | Rover mission |
| `camera` | string | Camera family |
| `image_width` | int | Prepared width |
| `image_height` | int | Prepared height |
| `route_query_json` | string | Corridor query |
| `prompt` | string | Task contract |
| `terrain_mask_rle` | string | 32x32 mask RLE |
| `hazard_boxes_json` | string | Hazard boxes |
| `route_safety_class` | string | Route decision |
| `clearance_score` | float | Route passability |
| `obstacle_coverage` | float | Rock fraction |
| `safe_corridor_width` | float | Safe width |
| `uncertainty_score` | float | Unknown fraction |

The input fields are `id` (opaque row key), `image` (public-relative JPEG path), `mission` (Curiosity, Spirit, or Opportunity), `camera` (Navcam), `image_width` and `image_height` (prepared pixel dimensions), `route_query_json` (normalized corridor object), and `prompt` (the shared task instruction). The train-only labels are `terrain_mask_rle` (32 × 32 terrain RLE), `hazard_boxes_json` (component boxes), `route_safety_class` (four-way route decision), `clearance_score` (weighted route passability), `obstacle_coverage` (route big-rock fraction), `safe_corridor_width` (robust connected safe width), and `uncertainty_score` (unknown-area measure).

### test.csv columns

`test.csv` contains exactly the same eight input columns as training data and none of the target columns.

| Column | Type | Description |
|---|---|---|
| `id` | string | Opaque row id |
| `image` | string | JPEG path |
| `mission` | string | Rover mission |
| `camera` | string | Camera family |
| `image_width` | int | Prepared width |
| `image_height` | int | Prepared height |
| `route_query_json` | string | Corridor query |
| `prompt` | string | Task contract |

In `test.csv`, `id` is the opaque row key; `image` is the public-relative JPEG path; `mission` is Curiosity, Spirit, or Opportunity; `camera` is Navcam; `image_width` and `image_height` are the prepared pixel dimensions; `route_query_json` is the normalized corridor object; and `prompt` is the shared task instruction. No target column is present in test data. `sample_submission.csv` is the submission template and contains one weak constant placeholder row for every test ID.

## Submission

Write the final submission CSV to exactly `./working/submission.csv`. It must contain exactly these eight columns in this order and exactly one row for every test ID.

| Column | Type | Constraint |
|---|---|---|
| `id` | string | Same set as test |
| `terrain_mask_rle` | string | Valid 32x32 RLE |
| `hazard_boxes_json` | string | Up to 8 boxes |
| `route_safety_class` | string | Four allowed values |
| `clearance_score` | float | In [0,1] |
| `obstacle_coverage` | float | In [0,1] |
| `safe_corridor_width` | float | In [0,1] |
| `uncertainty_score` | float | In [0,1] |

Example formatting:

```csv
id,terrain_mask_rle,hazard_boxes_json,route_safety_class,clearance_score,obstacle_coverage,safe_corridor_width,uncertainty_score
rvr_0123456789abcd,"{""shape"":[32,32],""counts"":[[0,1024]]}",[],safe_to_drive,0.91,0.00,0.44,0.05
rvr_fedcba98765432,"{""shape"":[32,32],""counts"":[[255,80],[2,900],[3,44]]}","[{""kind"":""big_rock"",""x"":0.4,""y"":0.6,""w"":0.1,""h"":0.1}]",drive_slowly,0.61,0.04,0.22,0.09
```

Requirements are strict: the submitted IDs must exactly match the test IDs, the column order must match the table above, duplicate or missing IDs are invalid, numeric values must be finite and in `[0,1]`, and malformed row-local mask, box, or route content receives zero for that row.

## 4) Tags

Suggested tags: `computer-vision`, `robotics`, `multimodal`, `small-data`, `structured-prediction`.

## 5) Grading Configuration

* Direction: Maximize
* Theoretical minimum: `0.0`
* Theoretical maximum: `1.0`

## 6) Grading Script

Select `Custom` and paste the exact contents of `PASTE_THIS_GRADE.txt`.

## 7) Prepare Script

Paste the exact contents of `PASTE_THIS_PREPARE.txt`.

## 8) GPU Tier

**CPU only / no GPU.** The hard platform limit is 1.5 hours on 10 CPU cores and 62 GB RAM.

## 9) What Not To Use

Do not use original AI4MARS filename/image-id or annotation lookup, source-image retrieval for hidden rows, metadata-only prediction, rule-only templates, external hosted image/segmentation APIs, closed-source teachers, hidden/private answer access, filename/order/mtime/size side channels, or grader/format exploits. The platform-visible Overview contains the full enforceable list.

# Challenge form - fill-in

## Difficulty

Hard

## Challenge Title

Opaque Security Clip Action Ledger Recovery

## Problem Description

### Overview

For each 8-second surveillance clip, predict a JSON list of the actions that happen in the clip. Each predicted action record must say:

- when the action starts and ends within the 32-frame clip,
- who or what performs the action,
- what action is being performed,
- what object, place, or context the action involves,
- and how this action record connects to other action records in the same clip.

The output is called an activity ledger. In plain language, a ledger is just an ordered set of action segments plus links between related segments. For example, if a person opens a vehicle door and then enters the vehicle, the desired output should contain two time-span records and a link showing that the records are adjacent or belong to a documented action pair.

The videos are real fixed-camera surveillance-style recordings from a licensed activity-recognition collection. The scenes show ordinary outdoor security-camera views with pedestrians, vehicles, doors, packages, carried objects, phones, bicycles, documents, and scene structures. The labels come from human-created activity annotations that mark action names, frame spans, actor identifiers, and actor types. During preparation, the original files are cropped, resized, metadata-stripped, re-encoded, and assigned opaque IDs so participants see only neutral short clips and relative paths.

This is not a whole-video classification task. A submission must recover the structured per-clip action ledger: multiple possible records, their frame ranges, their state fields, and their typed links.

### Task

Given one 32-frame MP4, output one canonical `graph_json` object. The JSON has two top-level lists:

- `nodes`: action records. Each record has a frame span and a state tuple.
- `edges`: links between records. Each link says whether two records overlap, occur next to one another, or form a documented activity pair.

The training set provides videos and their full `graph_json` ledgers. The test set provides only videos. Learn from the training videos and ledgers, then predict ledgers for held-out recording sessions. The test video is the only test-time signal.

The task is CPU-only. A practical solution can use 32-frame MobileNetV3/ResNet18 embeddings followed by a small GRU, temporal-convolution network, or transformer-lite decoder with constrained JSON generation. End-to-end large video transformers are unnecessary. The reference CPU pipeline plus inference and preparation is designed for at most 90 minutes on 10 CPU cores and 62 GB RAM.

### Public files

| Item | Description |
|---|---|
| `train.csv` | labeled videos |
| `test.csv` | unlabeled videos |
| `sample_submission.csv` | schema example |
| `train/videos/` | 256px MP4 clips |
| `test/videos/` | 256px MP4 clips |

All public IDs are opaque and all video paths are relative. No source filename, timestamp, session name, annotation ID, or group label is provided.

### train.csv columns

| Column | Type | Description |
|---|---|---|
| `id` | string | opaque item ID |
| `video` | string | relative MP4 path |
| `graph_json` | string | canonical target ledger |

`graph_json` is only a training label. It is a JSON object with `nodes` and `edges`. Each node has an integer `id` (0-based canonical order), inclusive `start` and `end` frame bins in `[0,31]`, and a `state` object. A state contains `agent`, `action`, `context`, and a sorted unique `roles` list. Allowed values are listed in the schema section below.

### test.csv columns

| Column | Type | Description |
|---|---|---|
| `id` | string | opaque item ID |
| `video` | string | relative MP4 path |

Each test row has exactly 32 effective frames at 4 FPS. The video is the only test-time signal.

Example test row: `item_001edae916ee264964,test/videos/item_001edae916ee264964.mp4`.

Example submission (the first three rows of the provided template):

```csv
id,graph_json
item_001edae916ee264964,"{""edges"":[],""nodes"":[]}"
item_0053f6e879a2f2083c,"{""edges"":[],""nodes"":[{""end"":25,""id"":0,""start"":7,""state"":{""action"":""enters"",""agent"":""person"",""context"":""scene_structure"",""roles"":[""person""]}}]}"
item_00be7ca4bc0ed7ac86,"{""edges"":[],""nodes"":[]}"
```

### Ledger JSON schema

Each node is one action segment. Node `state.agent` is in `{hand, person, vehicle}`. `state.action` is in `{abandons, carries, closes, drops_off, embraces, enters, exits, interacts, loads, makes_u_turn, opens, picks_up, purchases, puts_down, reads, reverses, rides, sits, stands, starts, steals, stops, talks, texts, transfers, turns, unloads}`. `state.context` is in `{bicycle, document, facility_door, heavy_object, laptop, left, none, object, package, person, phone, right, scene_structure, trunk, vehicle, vehicle_door}`. Every role is one of `{bag, bicycle, other, person, receptacle, vehicle}` and roles are sorted without duplicates.

`agent` is the acting category, `action` is the activity verb, `context` is the object/location cue, and `roles` lists participating object categories.

An edge has integer `from < to` node indices and one `type` from `{documented_pair, temporal_next, temporal_overlap}`. `documented_pair` means the two source activity labels are linked by the preparation-time activity-pair table and their spans overlap or are within 30 source frames. `temporal_overlap` means source spans overlap when no documented pair applies; `temporal_next` is the next canonical non-overlapping activity record when neither other type applies. Edges are unique and sorted by `(from,to,type)`. Empty ledgers are valid when no annotated activity record intersects the clip. The canonical JSON form uses UTF-8 JSON, sorted keys, compact separators, and no NaN, Infinity, duplicate keys, or extra fields.

The parser caps each ledger JSON at 20,000 characters, 32 nodes, and 256 edges. Node IDs must be consecutive; a `(from,to)` pair cannot repeat even with a different edge type. These caps are hard validation limits, not suggestions.

### Submission format

| Column | Type | Constraint |
|---|---|---|
| `id` | string | exact test IDs |
| `graph_json` | string | valid ledger JSON |

Submit one row per test ID, in any order. The grader aligns by opaque ID, but rejects missing/extra/repeated IDs or wrong/reordered columns. A malformed ledger cell is row-local and receives score zero; a structurally malformed file raises `InvalidSubmissionError`.

### What Not To Do

Do not use filename, ID, row order, path depth, file size, modification time, MP4 encoding, archive order, perceptual hashes, reverse-video lookup, or any other side channel. Do not use external annotations or private answers to recover labels, hard-code per-ID ledgers, or use a constant ledger template. Do not solve this with regex, timestamp parsing, motion-only frame differencing, color/shape thresholds, a detector-only pipeline, object-box relation proposals, or a rule table copied from the annotation vocabulary. External task-specific pretrained weights, hosted/closed-source APIs, teacher labeling, transductive use of hidden test labels, and inference-only pre-baked answers are prohibited.

Generic ImageNet-pretrained backbones, ordinary augmentations, optical flow as an auxiliary feature, classical CV features used inside a learned model, CPU multiprocessing, and learned temporal/structured decoders are allowed. The solution must learn from the provided videos and training ledgers and must remain CPU feasible.

### Enforcement

Submissions are checked for exact columns and row set, duplicate IDs, finite bounded JSON, canonical node/edge ordering, duplicate keys, node/edge caps, and legal vocabulary. Structural failures raise `InvalidSubmissionError`; malformed row content contributes zero for that row. Rule-only, source-lookup, metadata-only, or hard-coded solutions can be rejected even if they produce numerically valid JSON.

Enforcement on invalid approaches: any submission that relies on external media retrieval, external annotation lookup, ID/file-size side channels, or inference-only pre-baked answers is invalid and may be rejected.

### Evaluation

For each test row, the grader first parses and validates the submitted JSON. If both the predicted and true ledgers are empty, the row score is 1.0. If exactly one is empty, the row score is 0.0. Otherwise, predicted nodes and true nodes are matched one-to-one by maximizing:

`0.55 * span_credit + 0.45 * tuple_credit`

where `span_credit = max(span_iou, boundary_credit)`. `span_iou` is the inclusive frame-span intersection-over-union. `boundary_credit = max(0, 1 - (abs(pred_start - true_start) + abs(pred_end - true_end)) / 8)`. `tuple_credit = 0.20 * agent_match + 0.35 * action_match + 0.25 * context_match + 0.20 * role_set_f1`.

After matching, the row components are:

| Component | Definition | Weight in core score |
|---|---|---|
| Temporal span | matched span accuracy | 0.28 |
| State F1 | exact state-token F1 | 0.27 |
| Sequence edit | ordered state edit similarity | 0.17 |
| Typed edge F1 | typed link F1 after node mapping | 0.20 |
| Completeness | node-count and edge-count accuracy | 0.08 |

Temporal span is the mean matched `span_credit` divided by `max(pred_node_count, true_node_count)`. State F1 uses exact state-token matches; a matched node counts only when span credit is at least 0.25 and the full state token matches. Sequence edit is `1 - levenshtein_distance / max(sequence_length)` over ordered state tokens. Typed edge F1 is computed over `(from,to,type)` edges after matched predicted node IDs are mapped to true node IDs. Completeness is `0.65 * node_count_credit + 0.35 * edge_count_credit`, where count credit is `1 - abs(pred_count - true_count) / max(pred_count, true_count, 1)`.

The core score is the weighted sum of the five table components. The joint score is the geometric mean:

`joint = (temporal * state_f1 * sequence_edit * typed_edge_f1) ** 0.25`

The final row score is:

`row_score = clip(0.65 * core + 0.35 * joint, 0, 1)`

The overall score uses all private rows:

`balanced_mean = 0.80 * mean(rows with at least one true node) + 0.20 * mean(rows with no true nodes)`

`final_score = clip(0.88 * balanced_mean + 0.12 * worst_session_mean, 0, 1)`

`worst_session_mean` is the lowest mean row score among the five held-out recording-session groups. Each private session group has at least 30 rows. A perfect private ledger submission scores exactly 1.0. The declared theoretical minimum is 0.0 and maximum is 1.0. The sample submission is a weak train-prior schema baseline and is intentionally below 0.5 while above the platform validation floor.

### Dataset

The participant-visible dataset contains 479 labeled training clips and 175 unlabeled test clips. Each clip is a 256x256 MP4 with 32 frames sampled at 4 FPS from one longer fixed-camera recording. The visible content is source-neutral surveillance footage: pedestrians, vehicles, doors, packages, carried objects, phones, bicycles, and scene structures in outdoor security-camera views.

The ledgers are derived from human activity annotations, not from synthetic labels. The preparation script reads activity packets, converts source frame spans into 32-frame clip coordinates, maps activity names into the allowed `agent/action/context` vocabulary, and uses actor-type packets to populate the `roles` list. Edges are derived deterministically from source span overlap, source temporal order, and a documented action-pair table.

A recording-session group is the strongest available hidden grouping that could leak nearby footage: usually one original continuous camera recording, or a same-time or adjacent-camera recording group when multiple cameras observe related activity. Train and test are split by these groups. No original session group, neighboring window, or directly related camera recording appears in both train and test.

## Tags

video, structured-output, temporal-reasoning

## Grading Configuration

- Direction: maximize
- Theoretical minimum: 0.0
- Theoretical maximum: 1.0

## Grading Script

Paste the complete contents of `grade.py`.

## Prepare Script

Paste the complete contents of `prepare.py`.

## GPU Tier

CPU-only; no GPU is required or permitted. The intended machine has 10 CPU cores and 62 GB RAM, with a 90-minute wall-clock limit per submission.

## What Not To Use

See the inline `What Not To Do` and `Enforcement` paragraphs in the Problem Description above; those participant-visible restrictions are authoritative.

# Challenge creation form — fill-in (paired with `DATASET_FORM_FILL.md`)

**Platform status:** **Draft**

---

## 1) Difficulty

**Select:** **Hard**

Each clip is an **active multi-probe sensing** task, not passive scene understanding: several balls are launched from different top-edge ports and ricochet through a square arena whose solid obstacles are painted the same colour as the floor and therefore **invisible**. You must invert three coupled quantities from the motion alone — a full 12×12 occupancy map, the count of distinct 4-connected obstacle blobs, and a **counterfactual forecast** for a fresh straight-down drop from a column that is **never probed in the video** (`query_port`). Evidence comes from two complementary channels: brief contact flashes (positive boundary hits) and **free-space carving** (any cell a ball's fading trail passes through must be empty). Flashes mark contact **points**, not obstacle extents, so one bounce never reveals a whole block; trails fade, so no single frame holds the answer. Regions no probe ever reaches stay honestly under-determined, which caps the ceiling below perfection and separates careful integrators from flash-only guessers. The score also rewards consistent accuracy across hidden layout subgroups.

---

## 2) Challenge Title

```
Hidden Obstacle-Field Reconstruction From Probe-Ball Deflections
```

---

## 3) Problem Description

# Hidden Obstacle-Field Reconstruction From Probe-Ball Deflections

## Overview

Recovering a hidden occupancy grid from how **active probes** bounce off unseen solids is the core of bump-sensor robot mapping, cave sonar with multiple ping headings, and classic "shoot billiard balls to find where the cushions are" puzzles: the layout is never seen directly, but every trajectory is a measurement — cells the ball **passes through** must be free, and every **kink** in the path means it struck a hidden boundary somewhere. This challenge packages that inverse active-probing problem as a fixed-top-down video benchmark with exact grid labels.

This is **not** mirror/reflection geometry, hidden linkage graphs, cross-camera re-identification, dye-timing pipe routing, or static layout read-off from a single frame. The skill under test is **occupancy tomography from multi-probe ballistics**: integrate positive evidence (deflections and sparse contact flashes) with negative evidence (free-space carved by trajectories), then extrapolate to a column the clip never launched from.

You are given short **top-down** videos of a square arena overlaid with a fixed **12×12 cell grid** (the four coloured corner dots mark the grid corners; columns are numbered `0..11` left-to-right and rows `0..11` top-to-bottom). Several **probe balls** are launched from marked ports along the top edge and ricochet around the arena. Hidden inside the arena are a few **solid obstacles**, each made of one or more whole grid cells, rendered the **same colour as the floor** so they are completely invisible. You can only tell they are there because the balls **deflect** off them, and because a brief yellow **flash** marks each point where a ball touches a hidden obstacle.

Four properties make this a genuine **active inverse-sensing** task rather than a perception shortcut:

* **Contact flashes mark boundary POINTS, not obstacle extent.** A single flash tells you a ball touched *somewhere on the boundary* of a hidden block — it does not reveal the block's size, interior, or full footprint. You must fuse many deflections to pin down which cells are solid.
* **Free-space carving from trajectories.** Any grid cell a ball's trail visibly passes through must be **empty**. This negative evidence is as important as the flashes; marking only flash cells recovers a thin shell and scores poorly.
* **Trails fade.** Each ball leaves only a short, fading trail, so no single frame shows the full set of trajectories. The hidden layout lives only in motion **integrated over the whole clip** from **multiple launch ports**.
* **Counterfactual query on an un-probed column.** `query_port` names a launch column where **no ball is dropped in the video**; you must still forecast what a fresh straight-down probe from that column would hit. That head tests whether you reconstructed a physically consistent field, not just memorized visible bounces.

There is also a deliberate, honest source of difficulty: **regions that no ball ever visits are under-determined.** You cannot know what is in a corner that no probe reached. A good solution recovers what the deflections *determine* and accepts that the rest is ambiguous — which is exactly why the achievable ceiling is below a perfect score and why careful solvers separate from careless ones.

Each clip's inputs also include:

* **`num_probes`** — how many probe balls are launched in the clip.
* **`query_port`** — the x-coordinate (in grid units) of a single **un-shown** launch column. No ball is launched from this column in the video; you must *forecast* what a fresh probe dropped straight down it would do.

For each video you must produce four fields: a dense occupancy map, a topological obstacle count, a counterfactual hit forecast, and a confidence score:

1. **`occupancy`** — a **144-character string of `0`/`1`** giving the 12×12 grid in **row-major order** (row 0 = top, col 0 = left; index `= row*12 + col`). Put `1` where a cell is solid (part of a hidden obstacle) and `0` where it is empty.
2. **`n_obstacles`** — the number of **distinct** obstacles, i.e. the number of 4-connected groups of solid cells.
3. **`query_hit_row`** — imagine a fresh probe dropped **straight down** the query column (the column containing `query_port`). Report the **row index** (0 = top) of the first solid cell it would strike, or **`-1`** if that column is clear all the way to the bottom.
4. **`confidence`** — your self-estimated probability in `[0, 1]` that the whole row is correct.

The conventions are identical across every clip; you are expected to **infer them from the labelled training clips** (which give `occupancy`, `n_obstacles`, and `query_hit_row`). A horizontally mirrored scene is answered with the mirrored map and the mirrored query column — the grid frame is always read as it appears on screen.

**What Not To Do** (any of these is grounds for rejection on review, regardless of leaderboard score):

* **Judge from a single frame.** The layout is a property of motion over time; no still frame contains it (every frame shows only a few short trail segments). A solution that predicts from one frame is not solving the task.
* **Mark obstacles only where the flashes are.** Flashes are sparse near-side contact points, not obstacle extents; equating "flash cell" with "solid cell" recovers only a fraction of the field and scores poorly. You must reason about free space (cells balls pass through are empty) and obstacle interiors.
* **Hosted / closed-source APIs** at any stage of training or inference (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.), including any distillation or pseudo-labelling from such teachers. Only open-weights models and self-trained pipelines are permitted.
* **Reverse-image or hash lookups** of frames against any external collection to recover a layout. Predictions must come from the shipped video pixels and the public CSVs alone.
* **Filename / order side-channels.** Do not assume any structure in the lexicographic ordering of `<id>.mp4`, and do not exploit file-system metadata, mtimes, or row order.
* **Format hacks.** Out-of-range confidence, malformed cells, or other values meant to game the grader.
* **Grader / platform exploitation.** Hard-coded answer dictionaries, filesystem probes for `private/answers.csv`, or any channel that is not `public/train/`, `public/train.csv`, and `public/test/`, `public/test.csv`.

**Enforcement on invalid approaches:** rule-only solutions, or approaches that do not match the challenge domain (for example reading a single frame in isolation rather than integrating motion across the clip), may be rejected before payout. The intent is to reward genuine learned inverse reasoning over rendered motion, not score-chasing shortcuts.

## Evaluation

Each test clip is scored in `[0, 1]` (higher is better) by checking three coupled reconstructions from the probe motion — occupancy tomography (map), topological blob count, and the un-probed-column counterfactual — then blending the mean across clips with the weakest hidden subgroup.

```
map_score   = F1 (Dice) on the OCCUPIED class between your 144-cell map and the
              truth: with tp/fp/fn counted over solid cells,
              map_score = 2*tp / (2*tp + fp + fn).
              An all-empty map scores 0; the empty background is not rewarded.

count_score = max(0, 1 - |pred_n_obstacles - true_n_obstacles| / 4).

query_score = both clear (true == -1 and pred == -1)            : 1
              exactly one clear (one is -1, the other is not)    : 0
              otherwise                                          : exp(-|pred - true| / 1.5).

correctness = 0.65*map_score + 0.15*count_score + 0.20*query_score

calibration = 1 - |confidence - correctness|

row_score   = 0.90 * correctness + 0.10 * calibration
```

The final score blends the mean row score with the **worst-performing hidden subgroup** along three axes, so balanced accuracy across layout types matters:

```
Final = 0.68 * mean(row_score)
      + 0.14 * worst_subgroup(row_score)      # over the layout-family × variant axis
      + 0.10 * worst_subgroup(row_score)      # over an out-of-distribution axis
      + 0.08 * worst_subgroup(row_score)      # over a render-style axis
```

The subgroup labels are **private** evaluation metadata; they are not columns in `train.csv` or `test.csv`. They are used only by the grader to reward solutions that perform consistently rather than only on the easiest clips. **Higher is better. Minimum: 0.0, Maximum: 1.0.**

The grader returns `0.0` if the submission is missing any required column, contains duplicate `id`s, does not cover exactly the `id` set in `test.csv`, or has a missing / non-finite / out-of-range `confidence`. Other malformed values degrade gracefully: an occupancy field of the wrong length or with bad characters is treated as all-empty, and an unparseable `n_obstacles` / `query_hit_row` simply fails to match. (Because many CSV readers load an all-digit field as an integer and drop leading zeros, the grader left-pads a short all-digit `occupancy` back to 144 cells before scoring — so a clean round-trip of a valid 144-char map is always scored correctly.)

## Dataset

The dataset ships as two splits under a `public/` directory.

* `public/train/videos/<id>.mp4` — one arena clip per training row.
* `public/test/videos/<id>.mp4` — one arena clip per test row.
* `public/train.csv` — per training clip: the input columns plus the three labels (`occupancy`, `n_obstacles`, `query_hit_row`).
* `public/test.csv` — per test clip: input columns only.
* `public/sample_submission.csv` — one row per test `id` in the submission format, filled with weak placeholders that must be overwritten.

Every clip is `480 x 480`, `12` FPS, `90` frames (about 7.5 seconds), H.264 MP4. Row counts are seed-dependent and printed by `prepare.py`.

### File overview

The `public/` directory contains five items: `train/videos/*.mp4` are the per-clip arena videos for the training split; `test/videos/*.mp4` are the per-clip videos for the test split; `train.csv` holds one row per training clip with all input columns plus the three labels; `test.csv` holds one row per test clip with input columns only; and `sample_submission.csv` is a ready-to-edit submission template with one row per test `id`.

| Item                      | Description            |
|---------------------------|------------------------|
| `train/videos/*.mp4`      | Arena clip (train)     |
| `test/videos/*.mp4`       | Arena clip (test)      |
| `train.csv`               | Inputs + labels        |
| `test.csv`                | Inputs only            |
| `sample_submission.csv`   | Submission template    |

### train.csv columns

`train.csv` has eight columns. The first five are inputs (identical in `test.csv`): `id` (int) is the unique clip id; `video` (string) is the relative path to the clip's mp4; `num_probes` (int) is the number of probe balls launched; `query_port` (float) is the x-coordinate, in grid units, of the un-shown query launch column; and `prompt` (string) is the natural-language task instruction. The last three columns are the labels you predict for the test clips: `occupancy` (string) is the 144-character row-major 0/1 grid; `n_obstacles` (int) is the number of distinct 4-connected obstacles; and `query_hit_row` (int) is the row of the first solid cell a fresh straight-down probe from the query column would strike, or -1 if the column is clear.

| Column          | Type   | Description                                |
|-----------------|--------|--------------------------------------------|
| `id`            | int    | Unique clip id                             |
| `video`         | string | Path to mp4                                |
| `num_probes`    | int    | Number of probe balls launched             |
| `query_port`    | float  | x-coordinate (grid units) of query column  |
| `prompt`        | string | Task instruction                           |
| `occupancy`     | string | 144-char row-major 0/1 grid                |
| `n_obstacles`   | int    | Count of distinct obstacles                |
| `query_hit_row` | int    | First-hit row in query column, or -1       |

### test.csv columns

`test.csv` has the same five input columns as `train.csv` and no labels: `id` (int) is the unique clip id; `video` (string) is the relative path to the clip's mp4; `num_probes` (int) is the number of probe balls launched; `query_port` (float) is the query column's x-coordinate in grid units; and `prompt` (string) is the natural-language task instruction.

| Column       | Type   | Description                               |
|--------------|--------|-------------------------------------------|
| `id`         | int    | Unique clip id                            |
| `video`      | string | Path to mp4                               |
| `num_probes` | int    | Number of probe balls launched            |
| `query_port` | float  | x-coordinate (grid units) of query column |
| `prompt`     | string | Task instruction                          |

## Submission

Submit a CSV with a header row and **exactly one row per `id` in `test.csv`**, with these **5 columns in this order**: `id`, `occupancy`, `n_obstacles`, `query_hit_row`, `confidence`.

| Column          | Type   | Constraint                          |
|-----------------|--------|-------------------------------------|
| `id`            | int    | Same set as `test.csv`              |
| `occupancy`     | string | 144 chars of `0`/`1`, row-major     |
| `n_obstacles`   | int    | >= 0                                |
| `query_hit_row` | int    | -1, or 0..11                        |
| `confidence`    | float  | In [0, 1]                           |

**Requirements:**

* Header row plus exactly one row per test `id`; the `id` set must match `test.csv` exactly. Duplicate `id`s cause the grader to return `0.0`.
* `occupancy` is a 144-character string of `0`/`1` in row-major order (row 0 = top, col 0 = left). A wrong-length or non-binary value is treated as an all-empty map (scores 0 on the map head). If your CSV writer strips leading zeros from this field, the grader left-pads it back to 144, but you should still write the full 144 characters.
* `n_obstacles` is a non-negative integer (the count of 4-connected solid groups).
* `query_hit_row` is an integer in `0..11`, or `-1` if the query column is clear.
* `confidence` must be a finite number in `[0, 1]`; a missing, non-finite, or out-of-range value causes the grader to return `0.0`.
* A missing required column, a row-set mismatch, or a duplicate `id` causes the grader to return `0.0`.

**Example of a correctly formatted submission file (illustrative only; occupancy abbreviated):**

```
id,occupancy,n_obstacles,query_hit_row,confidence
500,000000000000000000000000...(144 chars total),4,5,0.71
501,000000000110000000000000...(144 chars total),3,-1,0.58
502,000000001100000000000011...(144 chars total),6,8,0.49
```

---

## 4) Tags

Suggested platform tags: `video`, `multimodal`, `small-data`.

---

## 5) Grading Configuration

* **Direction:** Maximize
* **Theoretical minimum:** `0.0`
* **Theoretical maximum:** `1.0`

---

## 6) Grading Script

**Select:** `Custom`

```python
import numpy as np
import pandas as pd

GRID = 12
N_CELLS = GRID * GRID

W_MAP = 0.65
W_COUNT = 0.15
W_QUERY = 0.20

W_CALIB = 0.10
COUNT_WIN = 4.0
QUERY_WIN = 1.5

MAX_OCC_LEN = 400

W_MEAN = 0.68
W_WORST_SPLIT = 0.14
W_WORST_OOD = 0.10
W_WORST_STYLE = 0.08


def _coerce_conf(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(x):
        return None
    if x < 0.0 or x > 1.0:
        return None
    return float(x)


def _occ_bool(v):
    s = str(v).strip()
    if len(s) > MAX_OCC_LEN:
        return np.zeros(N_CELLS, dtype=bool)
    if s.isdigit() and len(s) < N_CELLS:
        s = s.zfill(N_CELLS)
    if len(s) != N_CELLS:
        return np.zeros(N_CELLS, dtype=bool)
    arr = np.zeros(N_CELLS, dtype=bool)
    for i, c in enumerate(s):
        if c == "1":
            arr[i] = True
        elif c != "0":
            return np.zeros(N_CELLS, dtype=bool)
    return arr


def _int_or(v, default):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return default
    if not np.isfinite(x):
        return default
    return int(round(x))


def _occ_f1(pred, true):
    tp = int(np.sum(pred & true)); fp = int(np.sum(pred & ~true)); fn = int(np.sum(~pred & true))
    if tp == 0 and fp == 0 and fn == 0:
        return 1.0
    if tp == 0:
        return 0.0
    prec = tp / (tp + fp); rec = tp / (tp + fn)
    return float(2 * prec * rec / (prec + rec))


def _s_query(pred, true):
    if pred is None:
        return 0.0
    if true == -1 and pred == -1:
        return 1.0
    if (true == -1) != (pred == -1):
        return 0.0
    return float(np.exp(-abs(pred - true) / QUERY_WIN))


def _worst_group(rows, group_vals):
    if group_vals is None:
        return None
    buckets = {}
    for s, g in zip(rows, group_vals):
        buckets.setdefault(g, []).append(s)
    if not buckets:
        return None
    return min(float(np.mean(v)) for v in buckets.values())


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        req_sub = {"id", "occupancy", "n_obstacles", "query_hit_row", "confidence"}
        req_ans = {"id", "occupancy", "n_obstacles", "query_hit_row"}
        if not req_sub.issubset(set(submission.columns)):
            return 0.0
        if not req_ans.issubset(set(answers.columns)):
            return 0.0

        sub = submission.copy()
        ans = answers.copy()
        try:
            sub["id"] = sub["id"].astype(int)
            ans["id"] = ans["id"].astype(int)
        except (TypeError, ValueError):
            return 0.0

        if sub["id"].duplicated().any():
            return 0.0
        if set(sub["id"].tolist()) != set(ans["id"].tolist()):
            return 0.0

        sub_by_id = {int(r["id"]): r for _, r in sub.iterrows()}

        row_scores = []
        split_g, ood_g, style_g = [], [], []
        have_split = "split_group" in ans.columns
        have_ood = "ood_axis" in ans.columns
        have_style = "floor_style" in ans.columns

        for _, arow in ans.iterrows():
            srow = sub_by_id[int(arow["id"])]

            conf = _coerce_conf(srow["confidence"])
            if conf is None:
                return 0.0

            true_map = _occ_bool(arow["occupancy"])
            pred_map = _occ_bool(srow["occupancy"])
            s_map = _occ_f1(pred_map, true_map)

            true_n = _int_or(arow["n_obstacles"], 0)
            pred_n = _int_or(srow["n_obstacles"], None)
            if pred_n is None:
                s_count = 0.0
            else:
                s_count = max(0.0, 1.0 - abs(pred_n - true_n) / COUNT_WIN)

            true_q = _int_or(arow["query_hit_row"], -1)
            pred_q = _int_or(srow["query_hit_row"], None)
            s_query = _s_query(pred_q, true_q)

            correctness = W_MAP * s_map + W_COUNT * s_count + W_QUERY * s_query
            calib = 1.0 - abs(conf - correctness)
            row = (1.0 - W_CALIB) * correctness + W_CALIB * calib
            row_scores.append(row)

            if have_split:
                split_g.append(arow["split_group"])
            if have_ood:
                ood_g.append(arow["ood_axis"])
            if have_style:
                style_g.append(arow["floor_style"])

        if not row_scores:
            return 0.0

        mean_row = float(np.mean(row_scores))
        w_split = _worst_group(row_scores, split_g if have_split else None)
        w_ood = _worst_group(row_scores, ood_g if have_ood else None)
        w_style = _worst_group(row_scores, style_g if have_style else None)

        total_w = W_MEAN
        acc = W_MEAN * mean_row
        if w_split is not None:
            acc += W_WORST_SPLIT * w_split; total_w += W_WORST_SPLIT
        if w_ood is not None:
            acc += W_WORST_OOD * w_ood; total_w += W_WORST_OOD
        if w_style is not None:
            acc += W_WORST_STYLE * w_style; total_w += W_WORST_STYLE
        final = acc / total_w
        return float(np.clip(final, 0.0, 1.0))

    except Exception:
        return 0.0
```

---

## 7) Prepare Script

The raw dataset is a self-rendered corpus of arena clips plus `scenes.csv` (one row per clip with inputs, answer fields, and private grouping fields). `prepare.py` only splits by base scenario, copies videos, and anonymises ids — it performs no rendering or simulation.

```python
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import pandas as pd

SPLIT_SALT = "probemap-hidden-field-v1"
TEST_PER_1000 = 333
SHUFFLE_TRAIN = 718241
SHUFFLE_TEST = 305617

GRID = 12

PROMPT = (
    "Top-down view of a square arena overlaid with a fixed 12x12 cell grid "
    "(the four coloured corner dots mark the grid corners; cell columns are "
    "numbered 0..11 left-to-right and rows 0..11 top-to-bottom). Several probe "
    "balls are launched from marked ports along the top edge and bounce around. "
    "The arena hides a few solid obstacles, each made of one or more whole grid "
    "cells, rendered the SAME colour as the floor so they are invisible; you can "
    "only infer them from how the balls deflect. A brief yellow FLASH marks each "
    "point where a ball touches a hidden obstacle (it marks the contact POINT, "
    "not the obstacle's full extent). Trails fade, so no single frame shows the "
    "whole picture -- you must integrate motion across the clip. Report: "
    "(1) occupancy, a 144-character string of '0'/'1' giving the 12x12 grid in "
    "row-major order (row 0 = top, col 0 = left), '1' where a cell is solid; "
    "(2) n_obstacles, the number of distinct obstacles (4-connected groups of "
    "solid cells); (3) query_hit_row, for a fresh probe dropped straight down "
    "the query column (given by query_port), the row index (0=top) of the first "
    "solid cell it would strike, or -1 if that column is clear all the way down; "
    "and (4) a confidence in [0,1]. Regions no ball ever visits are genuinely "
    "ambiguous; recover what the deflections determine."
)


def _split_of(base_scenario_id: str) -> str:
    h = hashlib.sha256(f"{SPLIT_SALT}:{base_scenario_id}".encode("utf-8")).hexdigest()
    return "test" if (int(h[:8], 16) % 1000) < TEST_PER_1000 else "train"


def _ood_axis(family: str, variant: str, num_probes: int, n_obstacles: int) -> str:
    if variant == "mirror":
        return "mirrored_layout"
    if num_probes <= 10:
        return "few_probes"
    if n_obstacles >= 6:
        return "dense_field"
    return f"layout_{family}"


def prepare(raw: Path, public: Path, private: Path) -> None:
    raw = Path(raw); public = Path(public); private = Path(private)
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    scenes = pd.read_csv(raw / "scenes.csv", dtype={"scene_hash": str,
                                                    "base_scenario_id": str,
                                                    "occupancy_json": str})
    scenes = scenes.sort_values(["base_scenario_id", "variant", "scene_hash"]).reset_index(drop=True)
    scenes["split"] = scenes["base_scenario_id"].map(_split_of)

    train = (scenes[scenes["split"] == "train"]
             .sample(frac=1.0, random_state=SHUFFLE_TRAIN).reset_index(drop=True))
    test = (scenes[scenes["split"] == "test"]
            .sample(frac=1.0, random_state=SHUFFLE_TEST).reset_index(drop=True))

    id_map = {}
    for i, h in enumerate(train["scene_hash"].tolist()):
        id_map[h] = i
    offset = len(train)
    for i, h in enumerate(test["scene_hash"].tolist()):
        id_map[h] = offset + i

    train_dir = public / "train" / "videos"
    test_dir = public / "test" / "videos"
    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    train_rows, test_rows, sample_rows, answer_rows = [], [], [], []

    for _, r in train.iterrows():
        rid = id_map[r["scene_hash"]]
        vid_name = f"{rid:06d}.mp4"
        shutil.copyfile(raw / r["video"], train_dir / vid_name)
        train_rows.append({
            "id": rid, "video": f"videos/{vid_name}", "num_probes": int(r["num_probes"]),
            "query_port": float(r["query_port"]), "prompt": PROMPT,
            "occupancy": str(r["occupancy_json"]), "n_obstacles": int(r["n_obstacles"]),
            "query_hit_row": int(r["query_hit_row"]),
        })

    for _, r in test.iterrows():
        rid = id_map[r["scene_hash"]]
        vid_name = f"{rid:06d}.mp4"
        shutil.copyfile(raw / r["video"], test_dir / vid_name)
        test_rows.append({
            "id": rid, "video": f"videos/{vid_name}", "num_probes": int(r["num_probes"]),
            "query_port": float(r["query_port"]), "prompt": PROMPT,
        })
        sample_rows.append({
            "id": rid, "occupancy": "0" * (GRID * GRID), "n_obstacles": 0,
            "query_hit_row": -1, "confidence": 0.5,
        })
        answer_rows.append({
            "id": rid, "occupancy": str(r["occupancy_json"]),
            "n_obstacles": int(r["n_obstacles"]), "query_hit_row": int(r["query_hit_row"]),
            "num_probes": int(r["num_probes"]), "layout_family": r["layout_family"],
            "floor_style": r["floor_style"], "variant": r["variant"],
            "split_group": f"{r['layout_family']}__{r['variant']}",
            "ood_axis": _ood_axis(r["layout_family"], r["variant"],
                                  int(r["num_probes"]), int(r["n_obstacles"])),
        })

    train_cols = ["id", "video", "num_probes", "query_port", "prompt",
                  "occupancy", "n_obstacles", "query_hit_row"]
    test_cols = ["id", "video", "num_probes", "query_port", "prompt"]
    sample_cols = ["id", "occupancy", "n_obstacles", "query_hit_row", "confidence"]
    ans_cols = ["id", "occupancy", "n_obstacles", "query_hit_row", "num_probes",
                "layout_family", "floor_style", "variant", "split_group", "ood_axis"]

    pd.DataFrame(train_rows)[train_cols].to_csv(public / "train.csv", index=False)
    pd.DataFrame(test_rows)[test_cols].to_csv(public / "test.csv", index=False)
    pd.DataFrame(sample_rows)[sample_cols].to_csv(public / "sample_submission.csv", index=False)
    pd.DataFrame(answer_rows)[ans_cols].to_csv(private / "answers.csv", index=False)

    print(f"  [done] {len(train_rows)} train clips, {len(test_rows)} test clips.")
```

---

## 8) GPU Tier

**Select:** **A10G** — a few hundred short `480 x 480` clips is a small video-understanding workload. A frame-sampling video encoder with structured per-clip prediction heads (a 144-way occupancy decoder plus count and query heads) trains in single-digit GPU-hours on a 24 GB A10G. No language-model training is involved, so H100 is unnecessary.

---

## 9) What Not To Use

Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score.

* **Single-frame prediction** — reading the layout from one frame in isolation. Trails fade, so no single frame contains the layout; it lives only in motion across the clip.
* **Flash-cell shortcut** — marking solid cells only where contact flashes appear. Flashes are sparse near-side contact points, not obstacle extents, and recover only a fraction of the field.
* **Hosted / closed-source APIs** (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.) at any stage, including distillation / pseudo-labelling from such teachers.
* **Reverse-image / hash lookup** of frames against an external collection to recover a layout.
* **Filename / order side-channels** — any structure in the lexicographic ordering of `<id>.mp4`, file-system metadata, or mtimes.
* **Format hacks** — out-of-range confidence, malformed cells, or other values meant to game the grader.
* **Grader / platform exploitation** — hard-coded answer dictionaries, filesystem probes for `private/answers.csv`, or any channel that is not the public train/test files.
```

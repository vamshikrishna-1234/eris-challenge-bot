# Challenge creation form — fill-in (paired with `DATASET_FORM_FILL.md`)

**Platform status:** **Draft**

---

## 1) Difficulty

**Select:** **Hard**

Each clip is a short fixed-camera video of a board of colour-coded rotors (discs), each with a painted radial tick so its rotation is visible. No physical couplings are ever shown: the drive linkage is hidden. One or two source rotors turn on their own; through the hidden coupling, a driven rotor's motion follows its driver's, while decoy rotors spin independently and drive nothing, and a driver that stops also stops everything it drives. From the video alone the solver must recover, per clip: the directed drive graph (which rotor drives which), which rotors are still turning in the final frame, and which rotor moved first. Onset order alone is a deliberate trap, because decoys start interleaved with real driven rotors, so the graph can only be recovered by attending to how each rotor actually moves across the whole clip. The score also rewards consistent accuracy across hidden subgroups, so a solver that only does well on the easy scenes is capped.

---

## 2) Challenge Title

```
Hidden Linkage Mechanism Inference
```

---

## 3) Problem Description

# Hidden Linkage Mechanism Inference

## Overview

You are given short rendered videos of a flat board seen from one fixed oblique camera. On the board sit several **rotors** — short discs, each painted a distinct colour and carrying a dark radial **tick mark** so that its rotation is visible. The set of rotor colour-ids present in a clip is given by the `rotors` column (for example `["red", "green", "blue", "amber"]`). Rotors are identified by colour, which is unchanged by horizontal flips.

There are **no visible belts, gears, shafts, or contacts** between rotors. The drive linkage is internal and hidden. At the start, one or two **source** rotors begin to turn on their own. Through the hidden coupling, a **driven** rotor's rotation follows its driver's rotation over time. Some rotors are **decoys**: they spin on their own schedule and drive nothing. A source that stops part-way through also stops every rotor it drives, directly or indirectly. You must recover the drive linkage from the observed motion alone.

For each video you must produce four things:

1. **`edges_json`** — a JSON list of directed couplings `[driver_id, driven_id]` (each a pair of rotor colour-ids). Every driven rotor has **exactly one** direct driver; when a rotor's motion is the downstream result of a chain of drivers, report only its single **most immediate** driver. A clip with no couplings maps to `[]`.
2. **`moving_at_end_json`** — a JSON list of the rotor colour-ids that are **still rotating in the final frame**.
3. **`first_mover`** — the colour-id of the rotor that **begins rotating first**.
4. **`confidence`** — your self-estimated probability in `[0, 1]` that the row is correct.

The coupling rules are the same across every clip; you are expected to **infer them from the labelled training clips** (which give `edges_json`, `moving_at_end_json`, and `first_mover`). Rotor ids are always assigned by colour, so a horizontally flipped scene is answered with the same colour-ids — only the on-screen layout and the apparent spin direction flip.

**What Not To Do** (any of these is grounds for rejection on review, regardless of leaderboard score):

* **Infer couplings from onset order alone.** "Rotor B started just after rotor A, so A drives B" is a trap: decoys start interleaved with real driven rotors. Couplings must be inferred from how each rotor actually moves throughout the clip, not from which rotor happens to start first.
* **Read couplings from a single frame.** The graph is a property of motion over time; no still frame contains it.
* **Hosted / closed-source APIs** at any stage of training or inference (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.), including any distillation or pseudo-labelling from such teachers. Only open-weights models and self-trained pipelines are permitted.
* **Reverse-image or hash lookups** of frames against any external collection to recover an identity or label. Predictions must come from the shipped video pixels and the public CSVs alone.
* **Filename / order side-channels.** Do not assume any structure in the lexicographic ordering of `<id>.mp4`, and do not exploit file-system metadata, mtimes, or row order.
* **Format hacks.** Malformed JSON, self-loops, or out-of-range confidence meant to game the grader.
* **Grader / platform exploitation.** Hard-coded answer dictionaries, filesystem probes for `private/answers.csv`, or any channel that is not `public/train/`, `public/train.csv`, and `public/test/`, `public/test.csv`.

## Evaluation

Every test clip is scored in `[0, 1]` (higher is better) by combining three heads into a per-clip correctness, then blending mean and worst-subgroup performance.

```
edge_score   = F1 of the predicted directed edge set against the true edge set,
               where each edge is an ordered (driver_id, driven_id) pair;
               precision = |pred ∩ true| / |pred|, recall = |pred ∩ true| / |true|.
               Two empty edge sets match perfectly (score 1); predicting edges
               when there are none, or none when there are some, scores 0.

moving_score = fraction of the clip's rotors whose final-frame motion state
               (moving / not moving) is predicted correctly, over the full set
               of rotor ids in the clip.

first_score  = 1 if predicted first_mover == true first_mover, else 0.

correctness  = 0.70 * edge_score + 0.20 * moving_score + 0.10 * first_score

calibration  = 1 - |confidence - correctness|

row_score    = 0.90 * correctness + 0.10 * calibration
```

The final score blends the mean row score with the **worst-performing hidden subgroup** along three axes, so balanced accuracy across scene types matters:

```
Final = 0.68 * mean(row_score)
      + 0.14 * worst_subgroup(row_score)      # over a held-out scene-grouping axis
      + 0.10 * worst_subgroup(row_score)      # over an out-of-distribution axis
      + 0.08 * worst_subgroup(row_score)      # over a render-style axis
```

The subgroup labels are **private** evaluation metadata; they are not columns in `train.csv` or `test.csv`. They are used only by the grader to reward solutions that perform consistently rather than only on the easiest clips. **Higher is better. Minimum: 0.0, Maximum: 1.0.**

The grader returns `0.0` if the submission is missing any required column, contains duplicate `id`s, does not cover exactly the `id` set in `test.csv`, or has a missing / non-finite / out-of-range `confidence`. Other malformed values degrade gracefully: an unparseable `edges_json` or `moving_at_end_json` is treated as empty.

## Dataset

* `public/train/videos/<id>.mp4` — one board clip per training row.
* `public/test/videos/<id>.mp4` — one board clip per test row.
* `public/train.csv` — per training clip: inputs plus the labels `edges_json`, `moving_at_end_json`, `first_mover`.
* `public/test.csv` — per test clip: inputs only.
* `public/sample_submission.csv` — one row per test `id` in the submission format, filled with weak placeholders that must be overwritten.

Every clip is `640 x 384`, `12` FPS, `96` frames (about 8 seconds), H.264 MP4. Row counts are seed-dependent and printed by `prepare.py`.

### File overview

The `public/` directory contains five items: `train/videos/*.mp4` are the per-clip board videos for the training split; `test/videos/*.mp4` are the per-clip board videos for the test split; `train.csv` holds one row per training clip with all input columns plus the three labels; `test.csv` holds one row per test clip with input columns only; and `sample_submission.csv` is a ready-to-edit submission template with one row per test `id`.

| Item                            | Description            |
|---------------------------------|------------------------|
| `public/train/videos/*.mp4`     | Board clip (train)     |
| `public/test/videos/*.mp4`      | Board clip (test)      |
| `public/train.csv`              | Inputs + labels        |
| `public/test.csv`               | Inputs only            |
| `public/sample_submission.csv`  | Submission template    |

### train.csv columns

`train.csv` has eight columns. The first five are inputs (identical in `test.csv`): `id` (int) is the unique clip id; `video` (string) is the relative path to the clip's mp4; `num_rotors` (int) is the number of rotors on the board; `rotors` (string) is a JSON list of the rotor colour-ids present in the clip (for example `["red", "green", "blue", "amber"]`); and `prompt` (string) is the natural-language task instruction. The last three columns are the labels you predict for the test clips: `edges_json` (string) is a JSON list of directed `[driver_id, driven_id]` couplings; `moving_at_end_json` (string) is a JSON list of the rotor ids still rotating in the final frame; and `first_mover` (string) is the colour-id of the rotor that begins rotating first.

| Column               | Type   | Description           |
|----------------------|--------|-----------------------|
| `id`                 | int    | Unique clip id        |
| `video`              | string | Path to mp4           |
| `num_rotors`         | int    | Rotor count           |
| `rotors`             | string | JSON list of ids      |
| `prompt`             | string | Task instruction      |
| `edges_json`         | string | `[driver, driven]` list |
| `moving_at_end_json` | string | Ids moving at end     |
| `first_mover`        | string | First rotor to move   |

### test.csv columns

`test.csv` has the same five input columns as `train.csv` and no labels: `id` (int) is the unique clip id; `video` (string) is the relative path to the clip's mp4; `num_rotors` (int) is the number of rotors on the board; `rotors` (string) is a JSON list of the rotor colour-ids present in the clip; and `prompt` (string) is the natural-language task instruction.

| Column       | Type   | Description      |
|--------------|--------|------------------|
| `id`         | int    | Unique clip id   |
| `video`      | string | Path to mp4      |
| `num_rotors` | int    | Rotor count      |
| `rotors`     | string | JSON list of ids |
| `prompt`     | string | Task instruction |

## Submission

Submit a CSV with a header row and **exactly one row per `id` in `test.csv`**, with these **5 columns in this order**: `id`, `edges_json`, `moving_at_end_json`, `first_mover`, `confidence`.

| Column               | Type   | Constraint                        |
|----------------------|--------|-----------------------------------|
| `id`                 | int    | Same set as `test.csv`  |
| `edges_json`         | string | `[driver, driven]` pairs |
| `moving_at_end_json` | string | List of rotor ids       |
| `first_mover`        | string | One rotor id            |
| `confidence`         | float  | In [0, 1]               |

**Requirements:**

* Header row plus exactly one row per test `id`; the `id` set must match `test.csv` exactly. Duplicate `id`s cause the grader to return `0.0`.
* `edges_json` is a JSON list of two-element `[driver_id, driven_id]` lists of rotor colour-ids; self-loops and non-pairs are ignored. A clip with no couplings is `[]`.
* `moving_at_end_json` is a JSON list of rotor colour-ids; ids not present in the clip are ignored.
* `confidence` must be a finite number in `[0, 1]`; a missing, non-finite, or out-of-range value causes the grader to return `0.0`.
* A missing required column, a row-set mismatch, or a duplicate `id` causes the grader to return `0.0`.

**Example of a correctly formatted submission file (illustrative only):**

```
id,edges_json,moving_at_end_json,first_mover,confidence
300,"[[""red"", ""blue""], [""red"", ""green""]]","[""red"", ""blue"", ""green""]",amber,0.78
301,"[]","[""cyan""]",cyan,0.5
302,"[[""violet"", ""orange""]]","[""violet""]",blue,0.61
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
import json

import numpy as np
import pandas as pd

W_EDGES = 0.70
W_MOVING = 0.20
W_FIRST = 0.10

W_CALIB = 0.10

MAX_JSON_LEN = 2000

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


def _norm_id(x):
    return str(x).strip().lower()


def _parse_list(cell):
    if cell is None:
        return []
    if isinstance(cell, float) and not np.isfinite(cell):
        return []
    s = str(cell).strip()
    if s == "" or s.lower() in ("nan", "none", "[]") or len(s) > MAX_JSON_LEN:
        return []
    try:
        data = json.loads(s)
    except (ValueError, TypeError):
        return []
    if not isinstance(data, (list, tuple)):
        return []
    return [_norm_id(x) for x in data if _norm_id(x) != ""]


def _parse_edges(cell):
    if cell is None:
        return set()
    if isinstance(cell, float) and not np.isfinite(cell):
        return set()
    s = str(cell).strip()
    if s == "" or s.lower() in ("nan", "none", "[]") or len(s) > MAX_JSON_LEN:
        return set()
    try:
        data = json.loads(s)
    except (ValueError, TypeError):
        return set()
    if not isinstance(data, (list, tuple)):
        return set()
    out = set()
    for e in data:
        if isinstance(e, (list, tuple)) and len(e) == 2:
            a, b = _norm_id(e[0]), _norm_id(e[1])
            if a != "" and b != "" and a != b:
                out.add((a, b))
    return out


def _edge_f1(pred, true):
    if not pred and not true:
        return 1.0
    if not pred or not true:
        return 0.0
    inter = len(pred & true)
    prec = inter / len(pred)
    rec = inter / len(true)
    if prec + rec == 0:
        return 0.0
    return 2 * prec * rec / (prec + rec)


def _moving_score(pred_list, true_list, universe):
    uni = set(universe)
    if not uni:
        uni = set(pred_list) | set(true_list)
        if not uni:
            return 1.0
    pset = set(pred_list) & uni
    tset = set(true_list) & uni
    correct = sum(1 for r in uni if (r in pset) == (r in tset))
    return correct / len(uni)


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
        req_sub = {"id", "edges_json", "moving_at_end_json", "first_mover", "confidence"}
        req_ans = {"id", "edges_json", "moving_at_end_json", "first_mover"}
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
        have_style = "board_style" in ans.columns
        have_rotors = "rotors" in ans.columns

        for _, arow in ans.iterrows():
            srow = sub_by_id[int(arow["id"])]

            true_edges = _parse_edges(arow["edges_json"])
            true_moving = _parse_list(arow["moving_at_end_json"])
            true_first = _norm_id(arow["first_mover"])
            universe = _parse_list(arow["rotors"]) if have_rotors else []

            pred_edges = _parse_edges(srow["edges_json"])
            pred_moving = _parse_list(srow["moving_at_end_json"])
            pred_first = _norm_id(srow["first_mover"])
            conf = _coerce_conf(srow["confidence"])
            if conf is None:
                return 0.0

            e_s = _edge_f1(pred_edges, true_edges)
            m_s = _moving_score(pred_moving, true_moving, universe)
            f_s = 1.0 if pred_first == true_first and true_first != "" else 0.0
            correctness = W_EDGES * e_s + W_MOVING * m_s + W_FIRST * f_s
            calib = 1.0 - abs(conf - correctness)
            row = (1.0 - W_CALIB) * correctness + W_CALIB * calib
            row_scores.append(row)

            if have_split:
                split_g.append(arow["split_group"])
            if have_ood:
                ood_g.append(arow["ood_axis"])
            if have_style:
                style_g.append(arow["board_style"])

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

The raw dataset is a self-rendered corpus of board clips plus `scenes.csv` (one row per clip with inputs, answer fields, and private grouping fields). `prepare.py` only splits by base scenario, copies videos, and anonymises ids — it performs no rendering or simulation.

```python
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import pandas as pd

SPLIT_SALT = "cogchain-linkage-v1"
TEST_PER_1000 = 333
SHUFFLE_TRAIN = 514477
SHUFFLE_TEST = 233719

PROMPT = (
    "Watch the clip of a board of colour-coded spinning rotors (identified by the "
    "ids in 'rotors'). No physical couplings are shown: the drive linkage is "
    "hidden, so some rotors' motion follows other rotors' motion over time while "
    "decoy rotors spin on their own, and a driver that stops also stops everything "
    "it drives. Report: (1) edges_json, a JSON list of [driver_id, driven_id] "
    "directed couplings (each driven rotor has exactly one direct driver; report "
    "only its most immediate driver); (2) moving_at_end_json, a JSON list of the "
    "ids still rotating in the final frame; (3) first_mover, the id of the rotor "
    "that begins rotating first; and (4) a confidence in [0,1]. Onset order alone "
    "is a trap: decoys start interleaved with real driven rotors, so couplings "
    "must be inferred from how each rotor actually moves across the clip."
)


def _split_of(base_scenario_id: str) -> str:
    h = hashlib.sha256(f"{SPLIT_SALT}:{base_scenario_id}".encode("utf-8")).hexdigest()
    return "test" if (int(h[:8], 16) % 1000) < TEST_PER_1000 else "train"


def _ood_axis(topology_family: str, variant: str, num_rotors: int) -> str:
    if variant == "mirror":
        return "mirrored_layout"
    if num_rotors >= 7:
        return "many_rotors"
    return f"family_{topology_family}"


def prepare(raw: Path, public: Path, private: Path) -> None:
    raw = Path(raw); public = Path(public); private = Path(private)
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    scenes = pd.read_csv(raw / "scenes.csv", dtype={"scene_hash": str,
                                                    "base_scenario_id": str})
    scenes = scenes.sort_values(["base_scenario_id", "variant", "scene_hash"]).reset_index(drop=True)
    scenes["split"] = scenes["base_scenario_id"].map(_split_of)

    # Deterministically shuffle within each split so neither the sequential ids
    # nor the output row order carry scenario/variant grouping.
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
        h = r["scene_hash"]; rid = id_map[h]
        vid_name = f"{rid:06d}.mp4"; vid_rel = f"videos/{vid_name}"
        shutil.copyfile(raw / r["video"], train_dir / vid_name)
        train_rows.append({
            "id": rid, "video": vid_rel, "num_rotors": int(r["num_rotors"]),
            "rotors": r["rotors"], "prompt": PROMPT, "edges_json": r["edges_json"],
            "moving_at_end_json": r["moving_at_end_json"], "first_mover": r["first_mover"],
        })

    for _, r in test.iterrows():
        h = r["scene_hash"]; rid = id_map[h]
        vid_name = f"{rid:06d}.mp4"; vid_rel = f"videos/{vid_name}"
        shutil.copyfile(raw / r["video"], test_dir / vid_name)
        num_rotors = int(r["num_rotors"])
        test_rows.append({
            "id": rid, "video": vid_rel, "num_rotors": num_rotors,
            "rotors": r["rotors"], "prompt": PROMPT,
        })
        sample_rows.append({
            "id": rid, "edges_json": "[]", "moving_at_end_json": "[]",
            "first_mover": "", "confidence": 0.5,
        })
        answer_rows.append({
            "id": rid, "edges_json": r["edges_json"],
            "moving_at_end_json": r["moving_at_end_json"],
            "first_mover": r["first_mover"], "rotors": r["rotors"],
            "num_rotors": num_rotors,
            "topology_family": r["topology_family"], "board_style": r["board_style"],
            "variant": r["variant"],
            "split_group": f"{r['topology_family']}__{r['variant']}",
            "ood_axis": _ood_axis(r["topology_family"], r["variant"], num_rotors),
        })

    train_cols = ["id", "video", "num_rotors", "rotors", "prompt",
                  "edges_json", "moving_at_end_json", "first_mover"]
    test_cols = ["id", "video", "num_rotors", "rotors", "prompt"]
    sample_cols = ["id", "edges_json", "moving_at_end_json", "first_mover", "confidence"]
    ans_cols = ["id", "edges_json", "moving_at_end_json", "first_mover", "rotors",
                "num_rotors", "topology_family", "board_style", "variant",
                "split_group", "ood_axis"]

    pd.DataFrame(train_rows)[train_cols].to_csv(public / "train.csv", index=False)
    pd.DataFrame(test_rows)[test_cols].to_csv(public / "test.csv", index=False)
    pd.DataFrame(sample_rows)[sample_cols].to_csv(public / "sample_submission.csv", index=False)
    pd.DataFrame(answer_rows)[ans_cols].to_csv(private / "answers.csv", index=False)

    print(f"  [done] {len(train_rows)} train clips, {len(test_rows)} test clips.")
```

---

## 8) GPU Tier

**Select:** **A10G** — a few hundred short `640 x 384` clips is a small video-understanding workload. A frame-sampling video encoder with structured per-rotor prediction heads trains in single-digit GPU-hours on a 24 GB A10G. No language-model training is involved, so H100 is unnecessary.

---

## 9) What Not To Use

Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score.

* **Onset-order inference** — attributing a coupling because one rotor started shortly after another, instead of judging it from how each rotor actually moves across the whole clip. Decoys start interleaved with real driven rotors, so onset order is a trap.
* **Single-frame inference** — the drive graph is a property of motion over time and is absent from any still frame.
* **Hosted / closed-source APIs** (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.) at any stage, including distillation / pseudo-labelling from such teachers.
* **Reverse-image / hash lookup** of frames against an external collection to recover a label.
* **Filename / order side-channels** — any structure in the lexicographic ordering of `<id>.mp4`, file-system metadata, or mtimes.
* **Format hacks** — malformed JSON, self-loops, or out-of-range confidence meant to game the grader.
* **Grader / platform exploitation** — hard-coded answer dictionaries, filesystem probes for `private/answers.csv`, or any channel that is not the public train/test files.

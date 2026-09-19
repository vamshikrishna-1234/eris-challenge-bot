# Challenge creation form — fill-in (paired with `DATASET_FORM_FILL.md`)

**Platform status:** **Draft**

---

## 1) Difficulty

**Select:** **Hard**

Each image is a rendered cable-board scene with labelled cable endpoints, textured backgrounds, shadows, marker variation, distractor scraps, and visible over/under occlusions. You must trace which top endpoint connects to which bottom endpoint through the crossings, count the genuine interlocks, and then answer a counterfactual that no single crossing reveals: if you pull one named endpoint, does its cable lock or slip free, and in what order do the other cables get dragged taut. That pull cascade is a property of the whole over/under contact structure, so a solution has to visually parse the cable board and propagate tension through it. Some cables are buried too deep in the dense core to trace at all; there the honest answer is "unknown", and confident guessing is penalised. The score weights the pull cascade far above the directly-traceable parts and rewards consistent accuracy across hidden scene subgroups.

---

## 2) Challenge Title

```
Tangle Trace: Cable Connectivity And Counterfactual Pull
```

---

## 3) Problem Description

# Tangle Trace: Cable Connectivity And Counterfactual Pull

## Overview

Aircraft wiring looms, server-room cable bundles, surgical-robot tethers, and marine rigging all arrive as tangles where a technician has to know which end connects to which, whether a crossing is a real interlock or just lies flat, and — before touching anything — what happens if you pull one end: does the bundle cinch into a knot that catches, or does the cable slip free, and which other lines get dragged along. This challenge packages that cable-tracing-and-pull problem as a fixed-image benchmark with exact labels.

You are given a rendered **cable-board image** of N visually distinct **cables** running from labelled **top endpoints** (`T0`, `T1`, ...) down through a central **tangle** to labelled **bottom endpoints** (`X0`, `X1`, ...). The scenes vary in palette, endpoint marker shape, board texture, cable shadows, mild camera jitter, and distractor cable scraps. At every real crossing one cable passes **over** the other and visibly occludes it; there is no fixed colour or uniform gap convention that can be relied on across the dataset. Cables routed through the dense core may be occluded so heavily that their path cannot be followed.

The decisive part of the task is a **counterfactual about pulling a cable**, governed by this rule:

> Pulling a top endpoint tensions its cable. Wherever that cable passes **under** another cable, the pull **drags** the over-cable so it goes taut. That cable in turn drags any cable **it** passes under, and so on — a cascade. The pulled cable **locks** (will not pull free) if this dragging chains back to it (a mutual interlock); otherwise it **slips** free.

This is **not** a single-frame object-recognition task, a knot-type classifier, or a colour-matching exercise. The skill under test is **tracing connectivity through occluding crossings and propagating a pull through the whole over/under contact structure** — building the cascade and detecting whether it closes into a lock.

**Relation to prior work.** Cable-untangling robotics (e.g. autonomously untangling long cables; learning task-relevant keypoints for dense knots) builds a cable graph in order to *plan manipulation actions*, not to output a scored endpoint-correspondence and a pull cascade. Knot-recognition work classifies the *type* of a knot or counts crossings from an image. Studies of human knot perception (e.g. "Tangled Physics") test whether people can judge if a knot holds, but as a cognition experiment with no connectivity or per-cable cascade output. The combination here — recover the endpoint pairing (with calibrated **"unknown"** for buried cables), distinguish genuine interlocks from illusory crossings, and answer a **counterfactual pull** as an **ordered drag cascade** plus lock/slip — is the capability axis those lines of work do not cover.

For each image you must produce four fields plus a confidence:

1. **`pairing_json`** — a JSON object mapping each top endpoint to the bottom endpoint it connects to, e.g. `{"T0":"X2","T1":"X0",...}`; use the string `"unknown"` for any cable buried too deep in the tangle to trace.
2. **`n_true_locks`** — the number of genuine **pairwise interlocks** (a clasp: two cables that each pass under the other), as opposed to illusory crossings where one cable is always on top.
3. **`pull_outcome`** — for the cable at the endpoint named by `pull_endpoint`, whether it `locks` or `slips`, or `unknown` if that cable is buried.
4. **`pull_taut_json`** — a JSON list of the **other** cables (named by their top endpoint, e.g. `["T3","T1"]`) that go taut when `pull_endpoint` is pulled, **in the order tension reaches them**; an empty list `[]` if none go taut.

Each image's inputs also include `n_cables` (how many cables there are) and `pull_endpoint` (which top endpoint the counterfactual pulls). The conventions are identical across every image; infer them from the labelled training images.

**What Not To Do** (any of these is grounds for rejection on review, regardless of leaderboard score):

* **Stop at a single crossing.** Lock/slip and the taut order are properties of the whole contact structure; reading one crossing does not give them.
* **Guess instead of abstaining.** A cable buried in the dense core is genuinely untraceable — its pairing is `"unknown"` and pulling it gives `pull_outcome = "unknown"`; emitting a concrete answer there scores zero on those parts.
* **Equate any crossing with an interlock.** Most crossings are illusory (one cable always over); only a mutual clasp counts as a true lock.
* **Use deterministic line parsing as the solution.** Fixed colour thresholding, gap-template detection, skeletonization plus graph traversal, OCR-only endpoint matching, or other brittle diagram parsers are not valid substitutes for learned visual reasoning over the rendered cable-board images.
* **Hosted / closed-source APIs** at any stage of training or inference (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.), including any distillation or pseudo-labelling from such teachers. Only open-weights models and self-trained pipelines are permitted.
* **Reverse-image or hash lookups** of images against any external collection. Predictions must come from the shipped image pixels and the public CSVs alone.
* **Filename / order side-channels.** Do not assume any structure in the ordering of `<id>.jpg`, file-system metadata, mtimes, or row order.
* **Format hacks.** Extra columns, negative lock counts, out-of-range confidence, malformed cells, or other values meant to game the grader.
* **Grader / platform exploitation.** Hard-coded answer dictionaries, filesystem probes for `private/answers.csv`, or any channel that is not `public/train/`, `public/train.csv`, `public/test/`, and `public/test.csv`.

**Enforcement on invalid approaches:** rule-only solutions, deterministic image-parser plus graph-traversal pipelines, or approaches that do not match the challenge domain (for example reporting a fixed answer rather than visually parsing the cable board and tracing the tangle), may be rejected before payout. The intent is to reward genuine learned tracing-and-pull reasoning, not score-chasing shortcuts.

## Evaluation

Each test image is scored in `[0, 1]` (higher is better) across four heads, with most of the weight on the counterfactual pull, blended with a calibration term and then with the weakest hidden subgroup.

```
pair_score = fraction of top endpoints whose mapping is exactly correct
             (a correct "unknown" on a buried cable counts as correct).
lock_score = max(0, 1 - |pred_n_true_locks - true_n_true_locks| / 2).
pull_score = 1 if pull_outcome matches (including a correct "unknown"), else 0.
casc_score = if the pulled cable is buried (true outcome "unknown"): 1 only if
             pull_outcome was predicted "unknown", else 0.
             otherwise, comparing the predicted and true ordered taut lists:
             0.5 * set_F1 + 0.5 * (leading-prefix agreement / true length);
             when the true list is empty, 1 only if the prediction is empty.

correctness = 0.20*pair_score + 0.10*lock_score
            + 0.22*pull_score + 0.48*casc_score

calibration = 1 - |confidence - correctness|

row_score   = 0.90 * correctness + 0.10 * calibration
```

The final score blends the mean row score with the **worst-performing hidden subgroup** along three axes, so balanced accuracy across tangle types matters:

```
Final = 0.68 * mean(row_score)
      + 0.14 * worst_subgroup(row_score)      # over a tangle-family axis
      + 0.10 * worst_subgroup(row_score)      # over an out-of-distribution axis
      + 0.08 * worst_subgroup(row_score)      # over a render-style axis
```

The subgroup labels are **private** evaluation metadata; they are not columns in `train.csv` or `test.csv`. They are used only by the grader to reward solutions that perform consistently rather than only on the easiest images. **Higher is better. Minimum: 0.0, Maximum: 1.0.**

The grader returns `0.0` if the submission columns are not exactly `id,pairing_json,n_true_locks,pull_outcome,pull_taut_json,confidence` in that order, if any `n_true_locks` value is negative or non-integer, if the submission contains duplicate `id`s, if it does not cover exactly the `id` set in `test.csv`, or if `confidence` is missing, non-finite, or outside `[0,1]`. Other malformed values degrade gracefully: an unparseable or over-long JSON cell simply fails to match its head (scores zero there) without crashing the grader.

## Dataset

The dataset ships as two splits under a `public/` directory.

* `public/train/images/<id>.jpg` — one cable-board image per training row.
* `public/test/images/<id>.jpg` — one cable-board image per test row.
* `public/train.csv` — per training image: the input columns plus the four labels.
* `public/test.csv` — per test image: input columns only.
* `public/sample_submission.csv` — one row per test `id` in the submission format, filled with weak placeholders that must be overwritten.

Every image is a `640 x 480` JPEG. Row counts are seed-dependent and printed by `prepare.py`.

### File overview

The `public/` directory contains five items: `train/images/*.jpg` are the per-image cable-board renders for the training split; `test/images/*.jpg` are the per-image renders for the test split; `train.csv` holds one row per training image with all input columns plus the four labels; `test.csv` holds one row per test image with input columns only; and `sample_submission.csv` is a ready-to-edit submission template with one row per test `id`.

| Item                     | Description            |
|--------------------------|------------------------|
| `train/images/*.jpg`     | Cable board (train)    |
| `test/images/*.jpg`      | Cable board (test)     |
| `train.csv`              | Inputs + labels        |
| `test.csv`               | Inputs only            |
| `sample_submission.csv`  | Submission template    |

### train.csv columns

`train.csv` has nine columns. The first five are inputs (identical in `test.csv`): `id` (int) is the unique image id; `image` (string) is the relative path to the image; `n_cables` (int) is the number of cables in the tangle; `pull_endpoint` (string) names the top endpoint the counterfactual pulls (e.g. `T2`); and `prompt` (string) is the natural-language task instruction. The last four columns are the labels you predict for the test images: `pairing_json` (string) is a JSON object mapping each top endpoint to its bottom endpoint or `"unknown"`; `n_true_locks` (int) is the count of genuine interlocks; `pull_outcome` (string) is `locks`, `slips`, or `unknown`; and `pull_taut_json` (string) is a JSON list of the cables dragged taut, in order.

| Column           | Type   | Description                                  |
|------------------|--------|----------------------------------------------|
| `id`             | int    | Unique image id                              |
| `image`          | string | Path to jpg                                  |
| `n_cables`       | int    | Number of cables                             |
| `pull_endpoint`  | string | Top endpoint the pull acts on                |
| `prompt`         | string | Task instruction                             |
| `pairing_json`   | string | Endpoint mapping                            |
| `n_true_locks`   | int    | Count of genuine interlocks                  |
| `pull_outcome`   | string | locks / slips / unknown                      |
| `pull_taut_json` | string | Taut cable list                             |

### test.csv columns

`test.csv` has the same five input columns as `train.csv` and no labels: `id` (int) is the unique image id; `image` (string) is the relative path to the image; `n_cables` (int) is the number of cables; `pull_endpoint` (string) names the top endpoint the counterfactual pulls; and `prompt` (string) is the natural-language task instruction.

| Column          | Type   | Description                    |
|-----------------|--------|--------------------------------|
| `id`            | int    | Unique image id                |
| `image`         | string | Path to jpg                    |
| `n_cables`      | int    | Number of cables               |
| `pull_endpoint` | string | Top endpoint the pull acts on  |
| `prompt`        | string | Task instruction               |

## Submission

Submit a CSV with a header row and **exactly one row per `id` in `test.csv`**, with these **6 columns in this order**: `id`, `pairing_json`, `n_true_locks`, `pull_outcome`, `pull_taut_json`, `confidence`.

| Column           | Type   | Constraint                                   |
|------------------|--------|----------------------------------------------|
| `id`             | int    | Same set as `test.csv`                       |
| `pairing_json`   | string | Endpoint mapping                            |
| `n_true_locks`   | int    | >= 0                                         |
| `pull_outcome`   | string | locks / slips / unknown                      |
| `pull_taut_json` | string | Taut cable list                             |
| `confidence`     | float  | In [0, 1]                                    |

**Requirements:**

* Header row plus exactly one row per test `id`; the `id` set must match `test.csv` exactly. Duplicate `id`s cause the grader to return `0.0`.
* The submission must contain exactly the six listed columns in the listed order; extra columns or reordered columns cause the grader to return `0.0`.
* `pairing_json` must be a JSON object whose keys are the top endpoints `T0..` and whose values are bottom endpoints `X0..` or the string `"unknown"`. A malformed or over-long value scores zero on the pairing head.
* `n_true_locks` must be a non-negative integer; negative, fractional, missing, or non-finite values cause the grader to return `0.0`.
* `pull_outcome` is one of `locks`, `slips`, `unknown` (case-insensitive); any other value scores zero on that head.
* `pull_taut_json` must be a JSON list of top-endpoint labels in taut order; an empty list `[]` means no cables are dragged.
* `confidence` must be a finite number in `[0, 1]`; a missing, non-finite, or out-of-range value causes the grader to return `0.0`.
* A missing required column, a row-set mismatch, or a duplicate `id` causes the grader to return `0.0`.

**Example of a correctly formatted submission file (illustrative only):**

```
id,pairing_json,n_true_locks,pull_outcome,pull_taut_json,confidence
500,"{""T0"":""X2"",""T1"":""X0"",""T2"":""X3"",""T3"":""unknown""}",1,locks,"[""T2"",""T1""]",0.66
501,"{""T0"":""X1"",""T1"":""X0"",""T2"":""X2""}",0,slips,"[]",0.52
502,"{""T0"":""unknown"",""T1"":""unknown"",""T2"":""X0"",""T3"":""X3"",""T4"":""X4""}",2,unknown,"[]",0.40
```

---

## 4) Tags

Suggested platform tags: `image`, `multimodal`, `small-data`.

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

# correctness heads (sum to 1.0). The counterfactual pull (outcome + the ORDERED
# taut cascade) carries 0.60 of the weight; the cascade head alone is dominant at
# 0.40 because it requires tracing the whole under/over contact graph and ordering
# the chain - something no single-frame read or local cue provides.
W_PAIR = 0.20      # endpoint-pairing permutation (with "unknown" for buried cables)
W_LOCK = 0.10      # count of genuine interlocks (clasps) vs illusory crossings
W_PULL = 0.22      # COUNTERFACTUAL: pulled endpoint locks / slips / unknown
W_CASC = 0.48      # COUNTERFACTUAL cascade: ordered list of cables dragged taut

W_CALIB = 0.10     # calibration share of the row score (correctness gets 0.90)

# robustness aggregation (sum to 1.0)
W_MEAN = 0.68
W_WORST_SPLIT = 0.14
W_WORST_OOD = 0.10
W_WORST_STYLE = 0.08

MAX_JSON_LEN = 4000
MAX_ITEMS = 32

PULL_CLASSES = {"locks", "slips", "unknown"}
SUBMISSION_COLUMNS = ["id", "pairing_json", "n_true_locks", "pull_outcome",
                      "pull_taut_json", "confidence"]


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


def _norm(v):
    return str(v).strip().lower()


def _parse_obj(v):
    s = str(v).strip()
    if len(s) > MAX_JSON_LEN:
        return None
    try:
        d = json.loads(s)
    except (json.JSONDecodeError, ValueError):
        return None
    if not isinstance(d, dict) or len(d) > MAX_ITEMS:
        return None
    return {str(k).strip().lower(): str(val).strip().lower() for k, val in d.items()}


def _parse_list(v):
    s = str(v).strip()
    if len(s) > MAX_JSON_LEN:
        return None
    try:
        lst = json.loads(s)
    except (json.JSONDecodeError, ValueError):
        return None
    if not isinstance(lst, list) or len(lst) > MAX_ITEMS:
        return None
    return [str(x).strip().lower() for x in lst]


def _int_or(v, default):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return default
    if not np.isfinite(x):
        return default
    return int(round(x))


def _nonneg_int_or_none(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(x):
        return None
    if abs(x - round(x)) > 1e-9:
        return None
    x = int(round(x))
    if x < 0:
        return None
    return x


def _s_pair(pred_d, true_d):
    if true_d is None or len(true_d) == 0:
        return 0.0
    if pred_d is None:
        return 0.0
    correct = sum(1 for k, tv in true_d.items() if pred_d.get(k) == tv)
    return correct / len(true_d)


def _s_lock(pred_n, true_n):
    if pred_n is None:
        return 0.0
    return max(0.0, 1.0 - abs(pred_n - true_n) / 2.0)


def _s_casc(pred_l, true_l):
    """Ordered-cascade similarity: half set-F1, half ordered-prefix agreement.
    When the true cascade is empty (buried/unknown query), only an empty
    prediction earns credit."""
    if true_l is None or pred_l is None:
        return 0.0
    if len(true_l) == 0:
        return 1.0 if len(pred_l) == 0 else 0.0
    tset, pset = set(true_l), set(pred_l)
    tp = len(tset & pset)
    prec = tp / len(pset) if pset else 0.0
    rec = tp / len(tset) if tset else 0.0
    f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) > 0 else 0.0
    prefix = 0
    for a, b in zip(pred_l, true_l):
        if a == b:
            prefix += 1
        else:
            break
    return 0.5 * f1 + 0.5 * (prefix / len(true_l))


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
        req_ans = {"id", "pairing_json", "n_true_locks", "pull_outcome",
                   "pull_taut_json"}
        if list(submission.columns) != SUBMISSION_COLUMNS:
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
        have_style = "render_style" in ans.columns

        for _, arow in ans.iterrows():
            srow = sub_by_id[int(arow["id"])]

            conf = _coerce_conf(srow["confidence"])
            if conf is None:
                return 0.0

            s_pair = _s_pair(_parse_obj(srow["pairing_json"]), _parse_obj(arow["pairing_json"]))
            pred_locks = _nonneg_int_or_none(srow["n_true_locks"])
            if pred_locks is None:
                return 0.0
            s_lock = _s_lock(pred_locks, _int_or(arow["n_true_locks"], 0))

            true_pull = _norm(arow["pull_outcome"])
            pred_pull = _norm(srow["pull_outcome"])
            s_pull = 1.0 if (pred_pull in PULL_CLASSES and pred_pull == true_pull) else 0.0

            # When the pulled cable is buried, the cascade is unanswerable: credit
            # is given only for correctly recognising it (pull_outcome == unknown),
            # not for a blanket empty list. Otherwise score the ordered cascade.
            if true_pull == "unknown":
                s_casc = 1.0 if pred_pull == "unknown" else 0.0
            else:
                s_casc = _s_casc(_parse_list(srow["pull_taut_json"]),
                                 _parse_list(arow["pull_taut_json"]))

            correctness = (W_PAIR * s_pair + W_LOCK * s_lock
                           + W_PULL * s_pull + W_CASC * s_casc)
            calib = 1.0 - abs(conf - correctness)
            row = (1.0 - W_CALIB) * correctness + W_CALIB * calib
            row_scores.append(row)

            if have_split:
                split_g.append(arow["split_group"])
            if have_ood:
                ood_g.append(arow["ood_axis"])
            if have_style:
                style_g.append(arow["render_style"])

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


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--submission", required=True)
    ap.add_argument("--answers", required=True)
    args = ap.parse_args()
    sub = pd.read_csv(args.submission)
    ans = pd.read_csv(args.answers)
    print(f"score={grade(sub, ans):.6f}")
```

---

## 7) Prepare Script

The raw dataset is a self-rendered corpus of cable-board images plus `scenes.csv` (one row per image with inputs, answer fields, and private grouping fields). `prepare.py` only splits by base scenario, copies images, assigns anonymised ids from one global shuffled pool, and writes the public/private files — it performs no rendering or simulation.

```python
"""
prepare.py - Tangle Trace: Cable Connectivity And Counterfactual Pull

Deterministic split of the self-rendered raw corpus into public/private. It only
splits, copies images, and anonymises ids - no rendering or simulation.

  1. Read raw scenes.csv (one row per rendered image).
  2. Hash-based train/test split keyed on base_scenario_id, so both variants
     (base, recolor) of one scenario land in the SAME split.
  3. Assign anonymised ids from one global shuffled id pool before routing rows
     into train/test outputs, so integer id ranges do not reveal the split.
  4. Copy images, write public train/test/sample CSVs and private answers.csv.

`prepare(raw, public, private)` is the platform-standard signature.
"""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import pandas as pd

SPLIT_SALT = "tangle-trace-v1"
TEST_PER_1000 = 333
GLOBAL_ID_SEED = 503117
MIN_GROUP_TEST = 30

PROMPT = (
    "A rendered cable-board image shows several visually distinct cables running "
    "from labelled top endpoints (T0, T1, ...) down through a central tangle to "
    "labelled bottom endpoints (X0, X1, ...). The board may include shadows, mild "
    "camera jitter, marker variation, distractor scraps, and textured backgrounds; "
    "use the cable geometry, endpoint labels, and visible over/under occlusions "
    "rather than fixed colour thresholds or file-order cues. At every real crossing "
    "one cable passes OVER the other. Pull rule: pulling a top endpoint tensions "
    "its cable; wherever that cable passes UNDER another cable, the pull drags the "
    "over-cable so it goes taut, which in turn drags any cable IT passes under, "
    "and so on (a cascade); the pulled cable LOCKS if this dragging chains back "
    "to it (a mutual interlock), otherwise it SLIPS free. Report: (1) pairing_json "
    "- a JSON object mapping each top "
    "endpoint to the bottom endpoint it connects to, e.g. {\"T0\":\"X2\",...}, or "
    "\"unknown\" for a cable buried too deep in the tangle to trace; "
    "(2) n_true_locks - the number of genuine pairwise interlocks (a clasp, where "
    "two cables each pass under the other) as opposed to illusory crossings; "
    "(3) pull_outcome - for the endpoint named by pull_endpoint, \"locks\" or "
    "\"slips\", or \"unknown\" if that cable is buried; (4) pull_taut_json - a "
    "JSON list of the OTHER cables (by their top endpoint, e.g. [\"T3\",\"T1\"]) "
    "that go taut when pull_endpoint is pulled, in the order tension reaches them "
    "(an empty list if none, or if the pulled cable is buried); and a confidence "
    "in [0,1]. Cables buried in the dense core are genuinely untraceable - answer "
    "\"unknown\" there rather than guessing."
)


def _split_of(base_scenario_id: str) -> str:
    h = hashlib.sha256(f"{SPLIT_SALT}:{base_scenario_id}".encode("utf-8")).hexdigest()
    return "test" if (int(h[:8], 16) % 1000) < TEST_PER_1000 else "train"


def prepare(raw: Path, public: Path, private: Path) -> None:
    raw = Path(raw); public = Path(public); private = Path(private)
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    scenes = pd.read_csv(raw / "scenes.csv", dtype={"scene_hash": str,
                                                    "base_scenario_id": str,
                                                    "pairing_json": str,
                                                    "pull_taut_json": str})
    scenes = scenes.sort_values(
        ["base_scenario_id", "variant", "scene_hash"]).reset_index(drop=True)
    scenes["split"] = scenes["base_scenario_id"].map(_split_of)

    shuffled = scenes.sample(frac=1.0, random_state=GLOBAL_ID_SEED).reset_index(drop=True)
    id_map = {h: i for i, h in enumerate(shuffled["scene_hash"].tolist())}

    train = scenes[scenes["split"] == "train"].copy()
    test = scenes[scenes["split"] == "test"].copy()

    train_dir = public / "train" / "images"
    test_dir = public / "test" / "images"
    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    train_rows, test_rows, sample_rows, answer_rows = [], [], [], []

    def _src(h):
        return raw / "images" / f"{h}.jpg"

    for _, r in train.iterrows():
        rid = id_map[r["scene_hash"]]
        fn = f"{rid:06d}.jpg"
        shutil.copyfile(_src(r["scene_hash"]), train_dir / fn)
        train_rows.append({
            "id": rid, "image": f"train/images/{fn}", "n_cables": int(r["n_cables"]),
            "pull_endpoint": str(r["pull_endpoint"]), "prompt": PROMPT,
            "pairing_json": str(r["pairing_json"]), "n_true_locks": int(r["n_true_locks"]),
            "pull_outcome": str(r["pull_outcome"]), "pull_taut_json": str(r["pull_taut_json"]),
        })

    for _, r in test.iterrows():
        rid = id_map[r["scene_hash"]]
        fn = f"{rid:06d}.jpg"
        shutil.copyfile(_src(r["scene_hash"]), test_dir / fn)
        test_rows.append({
            "id": rid, "image": f"test/images/{fn}", "n_cables": int(r["n_cables"]),
            "pull_endpoint": str(r["pull_endpoint"]), "prompt": PROMPT,
        })
        nc = int(r["n_cables"])
        sample_rows.append({
            "id": rid,
            "pairing_json": "{" + ", ".join(f'"T{i}": "unknown"' for i in range(nc)) + "}",
            "n_true_locks": 1, "pull_outcome": "slips", "pull_taut_json": "[]",
            "confidence": 0.3,
        })
        answer_rows.append({
            "id": rid,
            "pairing_json": str(r["pairing_json"]), "n_true_locks": int(r["n_true_locks"]),
            "pull_outcome": str(r["pull_outcome"]), "pull_taut_json": str(r["pull_taut_json"]),
            "tangle_family": str(r["tangle_family"]), "render_style": str(r["render_style"]),
            "split_group": f"{r['tangle_family']}__{r['variant']}",
            "ood_axis": str(r["ood_axis"]),
        })

    train_cols = ["id", "image", "n_cables", "pull_endpoint", "prompt",
                  "pairing_json", "n_true_locks", "pull_outcome", "pull_taut_json"]
    test_cols = ["id", "image", "n_cables", "pull_endpoint", "prompt"]
    sample_cols = ["id", "pairing_json", "n_true_locks", "pull_outcome",
                   "pull_taut_json", "confidence"]
    ans_cols = ["id", "pairing_json", "n_true_locks", "pull_outcome", "pull_taut_json",
                "tangle_family", "render_style", "split_group", "ood_axis"]

    train_df = pd.DataFrame(train_rows)[train_cols].sort_values("id").reset_index(drop=True)
    test_df = pd.DataFrame(test_rows)[test_cols].sort_values("id").reset_index(drop=True)
    sample_df = pd.DataFrame(sample_rows)[sample_cols].sort_values("id").reset_index(drop=True)
    ans_df = pd.DataFrame(answer_rows)[ans_cols].sort_values("id").reset_index(drop=True)

    if len(ans_df) >= 120:
        for col in ["split_group", "ood_axis", "render_style"]:
            counts = ans_df[col].value_counts()
            if int(counts.min()) < MIN_GROUP_TEST:
                raise SystemExit(f"TEST subgroup {col} too small: {counts.to_dict()}")

    train_df.to_csv(public / "train.csv", index=False)
    test_df.to_csv(public / "test.csv", index=False)
    sample_df.to_csv(public / "sample_submission.csv", index=False)
    ans_df.to_csv(private / "answers.csv", index=False)

    print(f"  [done] {len(train_rows)} train images, {len(test_rows)} test images.")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=Path("raw_data"))
    ap.add_argument("--public", type=Path, default=Path("pub"))
    ap.add_argument("--private", type=Path, default=Path("priv"))
    args = ap.parse_args()
    prepare(args.raw.resolve(), args.public.resolve(), args.private.resolve())
    print("OK: prepare complete.")
```

---

## 8) GPU Tier

**Select:** **A10G** — a few thousand `640 x 480` JPEGs is a small image-understanding workload. An image encoder with a few structured prediction heads (a permutation/pairing decoder, a small count head, a three-way pull classifier, and an ordered-cascade decoder) trains in single-digit GPU-hours on a 24 GB A10G. No language-model training is involved, so H100 is unnecessary.

---

## 9) What Not To Use

Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score.

* **Single-crossing or single-region prediction** — reading lock/slip or the taut order from one part of the diagram. They are properties of the whole over/under contact structure.
* **Guessing instead of abstaining** — emitting a concrete pairing or pull answer for a cable buried in the dense core, where `"unknown"` is correct.
* **Crossing-equals-interlock shortcut** — counting every crossing as a lock. Only a mutual clasp is a true interlock.
* **Deterministic line-parser shortcuts** — fixed colour thresholding, gap-template detection, skeletonization plus graph traversal, OCR-only endpoint matching, or other brittle diagram parsers.
* **Hosted / closed-source APIs** (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.) at any stage, including distillation / pseudo-labelling from such teachers.
* **Reverse-image / hash lookup** of images against an external collection.
* **Filename / order side-channels** — any structure in the lexicographic ordering of `<id>.jpg`, file-system metadata, or mtimes.
* **Format hacks** — extra columns, negative lock counts, out-of-range confidence, malformed cells, or other values meant to game the grader.
* **Grader / platform exploitation** — hard-coded answer dictionaries, filesystem probes for `private/answers.csv`, or any channel that is not the public train/test files.

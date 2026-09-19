# Challenge creation form — fill-in (paired with `DATASET_FORM_FILL.md`)

**Platform status:** **Draft**

---

## 1) Difficulty

**Select:** **Hard**

The solver must, from a single still of a block stack at rest, predict not just *whether* the stack collapses once released, but *which* block first triggers the failure and *which* single block is the highest-leverage counterfactual ("keystone"). The two causal heads require an internal forward model of contact physics plus counterfactual reasoning — neither is recoverable from appearance features, and a binary stability classifier scores near zero on them.

---

## 2) Challenge Title

```
Collapse Attribution And Counterfactual Fragility
```

---

## 3) Problem Description

# Collapse Attribution And Counterfactual Fragility

## Overview

You are given a single photoreal still of a freshly-built **stack of coloured blocks** standing on a flat surface, captured the instant **before** it is released under gravity. Each stack is built close to its stability boundary, so whether it stands or topples is genuinely uncertain from the image alone. For every scene you must produce three coupled predictions:

1. **`will_collapse`** — a probability in `[0, 1]` that the stack collapses (i.e. at least one block moves appreciably) once released.
2. **`initiator_block_id`** — the id of the block that **first** loses support and triggers the cascade, or `"NONE"` if the stack is stable.
3. **`keystone_block_id`** — the id of the single **counterfactual keystone**: the one block whose removal would most change the outcome (turning a collapsing stack stable, or a stable stack into a collapsing one). `"NONE"` if no single-block removal would flip the outcome.

Each scene ships with a small roster table listing the blocks by `block_id`, each with the block's **pixel centroid** in the image and its **RGB colour**, so you can refer to a specific block unambiguously in your answer. You see only the rendered pixels and this roster — the masses, friction, and the physics of the release are never given and must be reasoned about.

The initiator and keystone questions are deliberately the hard part: they are not "is this stable?" but "who causes the failure?" and "which removal is the highest-leverage intervention?" — a causal, counterfactual judgement that a plain stability classifier cannot make.

**What Not To Do** (any of these is grounds for rejection on review, regardless of leaderboard score):

* **Treat it as a pure stability classifier.** Predicting only `will_collapse` and leaving `initiator_block_id` / `keystone_block_id` at a constant is out of scope — the causal heads carry the majority of the score and must be reasoned, not stubbed.
* **Hosted / closed-source APIs** at any stage of training or inference (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.), including any distillation or pseudo-labelling from such teachers. Only open-weights models and self-trained pipelines are permitted.
* **Pixel-hash or reverse-image-lookup** any still against any external image collection to recover an identity or outcome. The images have been processed so byte-level matching is not reliable; predictions must come from the shipped pixels and the roster columns alone.
* **Filename / order side-channels.** Do not assume any structure in the lexicographic ordering of `<id>.jpg` files, and do not exploit file-system metadata, mtimes, or any signal outside the image pixels and the CSV columns.
* **Format / range hacks.** Submitting out-of-range `will_collapse` values or non-canonical block-id strings to game the grader's clipping/coercion is not allowed.
* **Grader / platform exploitation.** Hard-coded answer dictionaries, filesystem probes for `private/answers.csv`, or any channel that is not `public/train/`, `public/train.csv`, `public/blocks_train.csv`, `public/test/`, `public/test.csv`, and `public/blocks_test.csv`.

## Evaluation

The grader computes, over the full test set:

```
S_collapse   = Brier Skill Score of will_collapse vs a static climatology
                 p = predicted P(collapse), y = true outcome in {0,1}
                 MSE_model = mean (p - y)^2
                 ref       = 0.5                    (static climatology)
                 MSE_ref   = mean (ref - y)^2 = 0.25
                 S_collapse = clip(1 - MSE_model / MSE_ref, 0, 1)

S_initiator  = macro-F1 over the initiator classes (block ids + "NONE"),
               computed over the whole test set. "NONE" is always an
               equally-weighted scored class; numeric block-id classes
               are scored when they occur in the ground truth.

S_keystone   = mean keystone accuracy. Per scene: 1.0 if the predicted
               keystone equals the true top-1 keystone, 0.5 if it equals
               the second-most-impactful block, else 0.0.

Final        = 0.30 * S_collapse^2
             + 0.35 * S_initiator^2
             + 0.35 * S_keystone^2          clipped to [0, 1]
```

* `S_collapse` is a **Brier Skill Score**: a constant predictor (the base rate, or `0.5` everywhere) scores **0**; a perfectly calibrated set of outcomes scores **1**.
* `S_initiator` is **macro-averaged F1** over the block-id classes plus `"NONE"`. `"NONE"` is always scored with equal weight, so an "always NONE" submission cannot coast; a block-id class absent from the ground truth is excluded so it cannot inflate the average.
* `S_keystone` rewards the counterfactual judgement, with partial credit for the second-best block.
* **Each sub-score is squared before weighting**, so a strong-but-naive model cannot coast to a high composite; a perfect solution (all three sub-scores 1.0) still reaches the maximum 1.0. The two causal heads carry the dominant **0.70** weight.

**Higher is better.** Minimum: 0.0, Maximum: 1.0.

A row missing from the submission — or whose `id` is not in `test.csv` — causes the grader to return `0.0`. The grader also returns `0.0` on duplicate `id`s, a missing required column, or any exception during parsing. Out-of-range `will_collapse` values are clipped to `[0, 1]` (non-numeric → `0.5`); block-id values that are not a non-negative integer or `"NONE"` are coerced to `"NONE"`.

## Dataset

* `public/train/images/<id>.jpg` — one RGB still per training scene.
* `public/test/images/<id>.jpg` — one RGB still per test scene.
* `public/train.csv` — per training scene: `id`, `image_path`, `n_blocks`, and the three targets `will_collapse`, `initiator_block_id`, `keystone_block_id`.
* `public/test.csv` — per test scene: `id`, `image_path`, `n_blocks`. No targets.
* `public/blocks_train.csv`, `public/blocks_test.csv` — one row per `(scene, block)` giving the block roster (id, pixel centroid, colour).
* `public/sample_submission.csv` — one row per test `id` in the submission format, filled with weak placeholders that must be overwritten.

Row counts are seed-dependent and printed by `prepare.py` (typical: a few thousand train scenes and ~half as many test scenes).

### File overview

| Item                          | Description                       |
|-------------------------------|-----------------------------------|
| `public/train/images/*.jpg`   | Block-stack still (train)         |
| `public/test/images/*.jpg`    | Block-stack still (test)          |
| `public/train.csv`            | Scene targets (train)             |
| `public/test.csv`             | Scene ids only (test)             |
| `public/blocks_train.csv`     | Block roster (train)              |
| `public/blocks_test.csv`      | Block roster (test)               |
| `public/sample_submission.csv`| Submission template               |

### `train.csv` columns

| Column               | Type   | Description                |
|----------------------|--------|----------------------------|
| `id`                 | int    | Unique scene id            |
| `image_path`         | string | Relative path to the still |
| `n_blocks`           | int    | Number of blocks in scene  |
| `will_collapse`      | int    | 1 if stack collapses       |
| `initiator_block_id` | string | Block id or "NONE"         |
| `keystone_block_id`  | string | Block id or "NONE"         |

### `test.csv` columns

| Column       | Type   | Description                |
|--------------|--------|----------------------------|
| `id`         | int    | Unique scene id            |
| `image_path` | string | Relative path to the still |
| `n_blocks`   | int    | Number of blocks in scene  |

### `blocks_train.csv` / `blocks_test.csv` columns

| Column     | Type | Description              |
|------------|------|--------------------------|
| `id`       | int  | Scene id                 |
| `block_id` | int  | Block id within scene    |
| `cx`       | int  | Block centroid x (pixel) |
| `cy`       | int  | Block centroid y (pixel) |
| `color_r`  | int  | Block colour R (0-255)   |
| `color_g`  | int  | Block colour G (0-255)   |
| `color_b`  | int  | Block colour B (0-255)   |

## Submission

Submit a CSV with a header row and **exactly one row per `id` in `test.csv`**, with these **4 columns in this order**: `id`, `will_collapse`, `initiator_block_id`, `keystone_block_id`.

| Column               | Type   | Constraint               |
|----------------------|--------|--------------------------|
| `id`                 | int    | Same set as `test.csv`   |
| `will_collapse`      | float  | P(collapse) in `[0, 1]`  |
| `initiator_block_id` | string | Block id or "NONE"       |
| `keystone_block_id`  | string | Block id or "NONE"       |

**Requirements:**

* Header row plus exactly one row per test `id`; the `id` set must match `test.csv` exactly. Duplicate `id`s cause the grader to return `0.0`.
* `will_collapse` is a float in `[0, 1]`; out-of-range values are clipped and non-numeric cells default to `0.5`.
* `initiator_block_id` and `keystone_block_id` are a non-negative integer block id (as a string) or `"NONE"`. Anything else is coerced to `"NONE"`.
* A row-set mismatch, a missing required column, or any parsing exception causes the grader to return `0.0`.

**Example of a correctly formatted submission file (illustrative only):**

```
id,will_collapse,initiator_block_id,keystone_block_id
4000,0.92,5,4
4001,0.07,NONE,NONE
4002,0.61,2,2
```

---

## 4) Tags

Suggested platform tags: `image`, `feature-engineering`, `multimodal`,
`small-data`.

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

W_COLLAPSE = 0.30
W_INITIATOR = 0.35
W_KEYSTONE = 0.35
SCORE_POWER = 2.0


def _coerce_prob(v) -> float:
    try:
        x = float(v)
    except (TypeError, ValueError):
        return 0.5
    if not np.isfinite(x):
        return 0.5
    return float(np.clip(x, 0.0, 1.0))


def _coerce_label(v) -> str:
    if v is None:
        return "NONE"
    s = str(v).strip()
    if s == "" or s.upper() == "NONE":
        return "NONE"
    try:
        f = float(s)
        if np.isfinite(f):
            n = int(round(f))
            if n >= 0:
                return str(n)
    except (TypeError, ValueError):
        pass
    return "NONE"


def _macro_f1(y_true, y_pred) -> float:
    present = sorted({c for c in y_true if c != "NONE"}, key=lambda s: int(s))
    present.append("NONE")
    f1s = []
    for cls in present:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p == cls)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != cls and p == cls)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p != cls)
        # absent from both truth and predictions -> undefined, exclude it
        if tp + fp + fn == 0:
            continue
        if tp == 0:
            f1s.append(0.0)
            continue
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1s.append(2.0 * precision * recall / (precision + recall))
    return float(np.mean(f1s)) if f1s else 0.0


def _brier_skill(p, y) -> float:
    # static climatology of 0.5 -> mse_ref is a fixed 0.25, never zero-variance
    mse_model = float(np.mean((p - y) ** 2))
    ref = 0.5
    mse_ref = float(np.mean((ref - y) ** 2))
    if mse_ref <= 1e-12:
        return 1.0 if mse_model <= 1e-12 else 0.0
    return float(np.clip(1.0 - mse_model / mse_ref, 0.0, 1.0))


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        required_sub = {"id", "will_collapse", "initiator_block_id", "keystone_block_id"}
        required_ans = {"id", "will_collapse", "initiator_block_id",
                        "keystone_block_id", "keystone_alt_block_id"}
        if not required_sub.issubset(set(submission.columns)):
            return 0.0
        if not required_ans.issubset(set(answers.columns)):
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

        sub = sub.set_index("id").reindex(ans["id"].to_numpy()).reset_index()

        p = np.array([_coerce_prob(v) for v in sub["will_collapse"]], dtype=float)
        y = ans["will_collapse"].astype(float).to_numpy()
        s_collapse = _brier_skill(p, y)

        init_pred = [_coerce_label(v) for v in sub["initiator_block_id"]]
        init_true = [_coerce_label(v) for v in ans["initiator_block_id"]]
        s_initiator = _macro_f1(init_true, init_pred)

        key_pred = [_coerce_label(v) for v in sub["keystone_block_id"]]
        key_true = [_coerce_label(v) for v in ans["keystone_block_id"]]
        key_alt = [_coerce_label(v) for v in ans["keystone_alt_block_id"]]
        kscores = []
        for pr, kt, ka in zip(key_pred, key_true, key_alt):
            if pr == kt:
                kscores.append(1.0)
            elif ka != "NONE" and pr == ka:
                kscores.append(0.5)
            else:
                kscores.append(0.0)
        s_keystone = float(np.mean(kscores)) if kscores else 0.0

        final = (
            W_COLLAPSE * (s_collapse ** SCORE_POWER)
            + W_INITIATOR * (s_initiator ** SCORE_POWER)
            + W_KEYSTONE * (s_keystone ** SCORE_POWER)
        )
        return float(np.clip(final, 0.0, 1.0))

    except Exception:
        return 0.0
```

---

## 7) Prepare Script

The raw dataset is a self-rendered, self-simulated corpus of block-stack stills
plus `scenes.csv` (per-scene outcomes) and `blocks.csv` (per-block roster).
`prepare.py` only splits, re-encodes, and anonymises — it performs no physics.

```python
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

IMG_SIZE = 256
JPEG_Q = 85
SPLIT_SALT = "collapse-attr-v1"
TEST_PER_1000 = 333
ID_SHUFFLE_SEED = int(hashlib.sha256(f"{SPLIT_SALT}:idmap".encode("utf-8")).hexdigest()[:8], 16)


def _split_of(scene_hash: str) -> str:
    h = hashlib.sha256(f"{SPLIT_SALT}:{scene_hash}".encode("utf-8")).hexdigest()
    return "test" if (int(h[:8], 16) % 1000) < TEST_PER_1000 else "train"


def _none_or_int(v) -> str:
    try:
        n = int(round(float(v)))
    except (TypeError, ValueError):
        return "NONE"
    return "NONE" if n < 0 else str(n)


def _reencode(src: Path, dst: Path) -> tuple[float, float]:
    img = Image.open(src).convert("RGB")
    ow, oh = img.size
    if img.size != (IMG_SIZE, IMG_SIZE):
        img = img.resize((IMG_SIZE, IMG_SIZE), resample=Image.BILINEAR)
    img.save(dst, format="JPEG", quality=JPEG_Q)
    return IMG_SIZE / ow, IMG_SIZE / oh  # pixel-scale factors for centroids


def _find_image(raw: Path, scene_hash: str) -> Path:
    matches = sorted(raw.glob(f"images/{scene_hash}.[pj]*"))  # png/jpg/jpeg only
    if not matches:
        raise FileNotFoundError(f"No image for scene {scene_hash}")
    return matches[0]


def prepare(raw: Path, public: Path, private: Path) -> None:
    raw = Path(raw); public = Path(public); private = Path(private)
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    scenes = pd.read_csv(raw / "scenes.csv", dtype={"scene_hash": str})
    blocks = pd.read_csv(raw / "blocks.csv", dtype={"scene_hash": str})
    scenes = scenes.sort_values("scene_hash").reset_index(drop=True)
    scenes["split"] = scenes["scene_hash"].map(_split_of)
    train_hashes = scenes.loc[scenes["split"] == "train", "scene_hash"].tolist()
    test_hashes = scenes.loc[scenes["split"] == "test", "scene_hash"].tolist()

    # shuffle deterministically so public ids are detached from scene_hash order
    rng = np.random.default_rng(ID_SHUFFLE_SEED)
    train_hashes = [train_hashes[i] for i in rng.permutation(len(train_hashes))]
    test_hashes = [test_hashes[i] for i in rng.permutation(len(test_hashes))]

    id_map = {}
    for i, h in enumerate(train_hashes):
        id_map[h] = i
    offset = len(train_hashes)
    for i, h in enumerate(test_hashes):
        id_map[h] = offset + i

    blocks_by_scene = {h: g for h, g in blocks.groupby("scene_hash")}
    train_dir = public / "train" / "images"
    test_dir = public / "test" / "images"
    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    train_rows = []; test_rows = []; blocks_train = []; blocks_test = []
    sample_rows = []; answer_rows = []

    for _, srow in scenes.iterrows():
        h = srow["scene_hash"]; rid = id_map[h]
        is_train = srow["split"] == "train"
        img_name = f"{rid:06d}.jpg"; img_rel = f"images/{img_name}"
        scale_x, scale_y = _reencode(_find_image(raw, h), (train_dir if is_train else test_dir) / img_name)

        n_blocks = int(srow["n_blocks"])
        will_collapse = int(srow["will_collapse"])
        init_str = _none_or_int(srow["initiator_block_id"])
        key_str = _none_or_int(srow["keystone_block_id"])
        key_alt_str = _none_or_int(srow["keystone_alt_block_id"])

        for _, brow in blocks_by_scene[h].sort_values("block_id").iterrows():
            (blocks_train if is_train else blocks_test).append({
                "id": rid, "block_id": int(brow["block_id"]),
                "cx": int(round(float(brow["cx"]) * scale_x)), "cy": int(round(float(brow["cy"]) * scale_y)),
                "color_r": int(brow["color_r"]), "color_g": int(brow["color_g"]),
                "color_b": int(brow["color_b"]),
            })

        if is_train:
            train_rows.append({
                "id": rid, "image_path": img_rel, "n_blocks": n_blocks,
                "will_collapse": will_collapse, "initiator_block_id": init_str,
                "keystone_block_id": key_str,
            })
        else:
            test_rows.append({"id": rid, "image_path": img_rel, "n_blocks": n_blocks})
            sample_rows.append({"id": rid, "will_collapse": 0.5,
                                "initiator_block_id": "NONE", "keystone_block_id": "NONE"})
            answer_rows.append({"id": rid, "will_collapse": will_collapse,
                                "initiator_block_id": init_str, "keystone_block_id": key_str,
                                "keystone_alt_block_id": key_alt_str})

    train_cols = ["id", "image_path", "n_blocks", "will_collapse",
                  "initiator_block_id", "keystone_block_id"]
    test_cols = ["id", "image_path", "n_blocks"]
    block_cols = ["id", "block_id", "cx", "cy", "color_r", "color_g", "color_b"]
    sample_cols = ["id", "will_collapse", "initiator_block_id", "keystone_block_id"]
    ans_cols = ["id", "will_collapse", "initiator_block_id",
                "keystone_block_id", "keystone_alt_block_id"]

    pd.DataFrame(train_rows)[train_cols].to_csv(public / "train.csv", index=False)
    pd.DataFrame(test_rows)[test_cols].to_csv(public / "test.csv", index=False)
    pd.DataFrame(blocks_train)[block_cols].to_csv(public / "blocks_train.csv", index=False)
    pd.DataFrame(blocks_test)[block_cols].to_csv(public / "blocks_test.csv", index=False)
    pd.DataFrame(sample_rows)[sample_cols].to_csv(public / "sample_submission.csv", index=False)
    pd.DataFrame(answer_rows)[ans_cols].to_csv(private / "answers.csv", index=False)

    print(f"  [done] {len(train_rows)} train scenes, {len(test_rows)} test scenes.")
```

---

## 8) GPU Tier

**Select:** **A10G** — a few thousand 256×256 stills with a per-block roster is a small image + tabular workload. A two-tower model (a compact image encoder plus a per-block MLP over roster features) trains in single-digit GPU-hours on a 24 GB A10G. No language-model training is involved, so H100 is unnecessary.

---

## 9) What Not To Use

Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score.

* **Stability-classifier-only solutions** that stub the two causal heads (`initiator_block_id`, `keystone_block_id`) at constants instead of reasoning about them.
* **Hosted / closed-source APIs** (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.) at any stage, including distillation / pseudo-labelling from such teachers.
* **Pixel-hash / reverse-image lookup** of any still against an external collection to recover an identity or outcome.
* **Filename / order side-channels** — any structure in the lexicographic ordering of `<id>.jpg`, file-system metadata, or mtimes.
* **Format / range hacks** — out-of-range `will_collapse` or non-canonical block-id strings meant to game the grader's coercion.
* **Grader / platform exploitation** — hard-coded answer dictionaries, filesystem probes for `private/answers.csv`, or any channel that is not the public train/test files.

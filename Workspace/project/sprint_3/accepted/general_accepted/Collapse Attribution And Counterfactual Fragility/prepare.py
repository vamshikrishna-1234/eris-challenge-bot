"""
prepare.py - Collapse Attribution And Counterfactual Fragility

Deterministic split of a pre-rendered, self-simulated block-stack corpus into
public/ and private/ splits. ALL physics + rendering happens upstream in
generate.py; this script only splits, re-encodes, and anonymizes.

RAW INPUT LAYOUT (produced by generate.py; passed as `raw`)
-----------------------------------------------------------
    raw/images/<scene_hash>.png        one t=0 still per scene
    raw/scenes.csv                     one row per scene:
        scene_hash, n_blocks, will_collapse (0/1),
        initiator_block_id (int, -1 = none),
        keystone_block_id (int, -1 = none),
        keystone_alt_block_id (int, -1 = none)
    raw/blocks.csv                     one row per (scene, block):
        scene_hash, block_id, cx, cy, color_r, color_g, color_b
        (cx, cy = pixel centroid of the block in the still; colour is the
         block's RGB - both observable from the image, given only so a solver
         can reference each block by a stable id.)

OUTPUT LAYOUT
-------------
    public/train/images/<id>.jpg
    public/test/images/<id>.jpg
    public/train.csv          id, image_path, n_blocks, will_collapse,
                              initiator_block_id, keystone_block_id
    public/test.csv           id, image_path, n_blocks
    public/blocks_train.csv   id, block_id, cx, cy, color_r, color_g, color_b
    public/blocks_test.csv    id, block_id, cx, cy, color_r, color_g, color_b
    public/sample_submission.csv  id, will_collapse, initiator_block_id,
                                  keystone_block_id
    private/answers.csv       id, will_collapse, initiator_block_id,
                              keystone_block_id, keystone_alt_block_id

Targets (will_collapse / initiator / keystone) are written to public/train.csv
for TRAIN scenes only; for TEST scenes they live solely in private/answers.csv.
The split is a deterministic hash of scene_hash, so re-running the script
produces byte-identical outputs.

The `prepare(raw, public, private)` signature is the platform standard.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

# -------- constants --------

IMG_SIZE = 256
JPEG_Q = 85

# Deterministic split: ~1/3 of scenes go to test. The salt makes the split
# specific to this challenge so it cannot be guessed from scene_hash alone.
SPLIT_SALT = "collapse-attr-v1"
TEST_PER_1000 = 333
# deterministic seed used to shuffle scenes before assigning sequential ids, so
# the public id carries no information about the scene_hash / generation order.
ID_SHUFFLE_SEED = int(hashlib.sha256(f"{SPLIT_SALT}:idmap".encode("utf-8")).hexdigest()[:8], 16)


def _split_of(scene_hash: str) -> str:
    h = hashlib.sha256(f"{SPLIT_SALT}:{scene_hash}".encode("utf-8")).hexdigest()
    return "test" if (int(h[:8], 16) % 1000) < TEST_PER_1000 else "train"


def _none_or_int(v) -> str:
    """Map a raw integer label (-1 == none) to the canonical string form."""
    try:
        n = int(round(float(v)))
    except (TypeError, ValueError):
        return "NONE"
    return "NONE" if n < 0 else str(n)


def _reencode(src: Path, dst: Path) -> tuple[float, float]:
    """Re-encode to a fixed-size JPEG. Strips any source metadata and makes
    byte-level matching against any external copy useless. Returns the
    (x, y) pixel-scale factors applied so block centroids can be rescaled
    consistently when the source is not already IMG_SIZE x IMG_SIZE."""
    img = Image.open(src).convert("RGB")
    ow, oh = img.size
    if img.size != (IMG_SIZE, IMG_SIZE):
        img = img.resize((IMG_SIZE, IMG_SIZE), resample=Image.BILINEAR)
    img.save(dst, format="JPEG", quality=JPEG_Q)
    return IMG_SIZE / ow, IMG_SIZE / oh


def _find_image(raw: Path, scene_hash: str) -> Path:
    # Restrict to image extensions (png / jpg / jpeg) so an unrelated sidecar
    # file sharing the scene_hash stem can never be picked up by the glob.
    matches = sorted(raw.glob(f"images/{scene_hash}.[pj]*"))
    if not matches:
        raise FileNotFoundError(f"No image for scene {scene_hash} under {raw/'images'}")
    return matches[0]


def prepare(raw: Path, public: Path, private: Path) -> None:
    raw = Path(raw)
    public = Path(public)
    private = Path(private)
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    scenes = pd.read_csv(raw / "scenes.csv", dtype={"scene_hash": str})
    blocks = pd.read_csv(raw / "blocks.csv", dtype={"scene_hash": str})

    # Deterministic ordering + split.
    scenes = scenes.sort_values("scene_hash").reset_index(drop=True)
    scenes["split"] = scenes["scene_hash"].map(_split_of)
    train_hashes = scenes.loc[scenes["split"] == "train", "scene_hash"].tolist()
    test_hashes = scenes.loc[scenes["split"] == "test", "scene_hash"].tolist()

    # Shuffle (deterministically) before assigning sequential ids so the public
    # id is detached from the scene_hash ordering / generation sequence.
    rng = np.random.default_rng(ID_SHUFFLE_SEED)
    train_hashes = [train_hashes[i] for i in rng.permutation(len(train_hashes))]
    test_hashes = [test_hashes[i] for i in rng.permutation(len(test_hashes))]

    id_map: dict[str, int] = {}
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

    train_rows: list[dict] = []
    test_rows: list[dict] = []
    blocks_train: list[dict] = []
    blocks_test: list[dict] = []
    sample_rows: list[dict] = []
    answer_rows: list[dict] = []

    for _, srow in scenes.iterrows():
        h = srow["scene_hash"]
        rid = id_map[h]
        is_train = srow["split"] == "train"
        img_name = f"{rid:06d}.jpg"
        img_rel = f"images/{img_name}"
        dst_dir = train_dir if is_train else test_dir
        scale_x, scale_y = _reencode(_find_image(raw, h), dst_dir / img_name)

        n_blocks = int(srow["n_blocks"])
        will_collapse = int(srow["will_collapse"])
        init_str = _none_or_int(srow["initiator_block_id"])
        key_str = _none_or_int(srow["keystone_block_id"])
        key_alt_str = _none_or_int(srow["keystone_alt_block_id"])

        # per-block observable rows
        bsub = blocks_by_scene.get(h)
        if bsub is None:
            raise ValueError(f"scene {h} has no block rows in blocks.csv")
        for _, brow in bsub.sort_values("block_id").iterrows():
            entry = {
                "id": rid,
                "block_id": int(brow["block_id"]),
                "cx": int(round(float(brow["cx"]) * scale_x)),
                "cy": int(round(float(brow["cy"]) * scale_y)),
                "color_r": int(brow["color_r"]),
                "color_g": int(brow["color_g"]),
                "color_b": int(brow["color_b"]),
            }
            (blocks_train if is_train else blocks_test).append(entry)

        if is_train:
            train_rows.append({
                "id": rid,
                "image_path": img_rel,
                "n_blocks": n_blocks,
                "will_collapse": will_collapse,
                "initiator_block_id": init_str,
                "keystone_block_id": key_str,
            })
        else:
            test_rows.append({
                "id": rid,
                "image_path": img_rel,
                "n_blocks": n_blocks,
            })
            sample_rows.append({
                "id": rid,
                "will_collapse": 0.5,
                "initiator_block_id": "NONE",
                "keystone_block_id": "NONE",
            })
            answer_rows.append({
                "id": rid,
                "will_collapse": will_collapse,
                "initiator_block_id": init_str,
                "keystone_block_id": key_str,
                "keystone_alt_block_id": key_alt_str,
            })

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


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=Path("raw_data"))
    ap.add_argument("--public", type=Path, default=Path("pub"))
    ap.add_argument("--private", type=Path, default=Path("priv"))
    args = ap.parse_args()
    prepare(args.raw.resolve(), args.public.resolve(), args.private.resolve())
    print("OK: prepare complete.")

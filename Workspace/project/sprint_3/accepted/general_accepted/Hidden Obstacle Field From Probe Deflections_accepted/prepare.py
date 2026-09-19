"""
prepare.py - Hidden Obstacle-Field Reconstruction From Probe-Ball Deflections

Deterministic split of the self-rendered raw corpus into public/private. It only
splits, copies videos, and anonymises ids; it runs NO rendering or simulation.

  1. Read raw scenes.csv (one row per rendered clip).
  2. Deterministic, hash-based train/test split SALTED on base_scenario_id, so
     every variant (base / relight / mirror) of one scenario lands in the SAME
     split -- near-duplicate clips never straddle train and test.
  3. Deterministically SHUFFLE within each split before assigning fresh
     sequential ids, so neither the ids nor the output row order carry any
     scenario / variant / chronological grouping.
  4. Copy each clip to public/<split>/videos/<id>.mp4 and write public
     train/test/sample CSVs plus the private answers.csv. Hidden grouping fields
     (layout_family, floor_style, split_group, variant, ood_axis) live ONLY in
     private/answers.csv and drive the grader's worst-group robustness terms.

`prepare(raw, public, private)` is the platform-standard signature.
"""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import pandas as pd

SPLIT_SALT = "probemap-hidden-field-v1"
TEST_PER_1000 = 333     # ~1/3 of base scenarios to test
SHUFFLE_TRAIN = 718241  # fixed seeds: deterministic but grouping-breaking shuffle
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
    """Coarse private OOD-axis tag used only for worst-group scoring."""
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


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=Path("raw_data"))
    ap.add_argument("--public", type=Path, default=Path("pub"))
    ap.add_argument("--private", type=Path, default=Path("priv"))
    args = ap.parse_args()
    prepare(args.raw.resolve(), args.public.resolve(), args.private.resolve())
    print("OK: prepare complete.")

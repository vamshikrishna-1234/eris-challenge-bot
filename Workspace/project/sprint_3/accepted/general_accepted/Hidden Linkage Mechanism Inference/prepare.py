"""
prepare.py - Hidden Linkage Mechanism Inference

Deterministic split of the self-rendered raw corpus into public/private. It only
splits, copies videos, and anonymises ids; it runs NO rendering or simulation.

  1. Read raw scenes.csv (one row per rendered clip).
  2. Deterministic, hash-based train/test split SALTED on base_scenario_id, so
     every variant (base / relight / mirror) of one scenario lands in the SAME
     split -- near-duplicate clips never straddle train and test.
  3. Copy each clip to public/<split>/videos/<id>.mp4 with a fresh sequential id
     (train first, then test) so nothing about the original hash or the
     base/variant grouping leaks through filenames or ordering.
  4. Write public train/test/sample CSVs and the private answers.csv. Hidden
     grouping fields (topology_family, board_style, split_group, variant,
     ood_axis) live ONLY in private/answers.csv and drive the grader's
     worst-group robustness terms.

`prepare(raw, public, private)` is the platform-standard signature.
"""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import pandas as pd

SPLIT_SALT = "cogchain-linkage-v1"
TEST_PER_1000 = 333    # ~1/3 of base scenarios to test
SHUFFLE_TRAIN = 514477  # fixed seeds: deterministic but grouping-breaking shuffle
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
    """Coarse private OOD-axis tag used only for worst-group scoring."""
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

    # Deterministically SHUFFLE within each split so neither the sequential ids
    # nor the output row order carry any scenario/variant grouping: variants of a
    # base scenario are scattered, not adjacent. The split itself stays grouped by
    # base scenario so near-duplicate variants never straddle train and test.
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


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=Path("raw_data"))
    ap.add_argument("--public", type=Path, default=Path("pub"))
    ap.add_argument("--private", type=Path, default=Path("priv"))
    args = ap.parse_args()
    prepare(args.raw.resolve(), args.public.resolve(), args.private.resolve())
    print("OK: prepare complete.")

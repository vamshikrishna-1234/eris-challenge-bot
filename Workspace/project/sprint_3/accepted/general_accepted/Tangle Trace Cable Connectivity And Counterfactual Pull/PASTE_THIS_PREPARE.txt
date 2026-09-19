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

"""
prepare.py - Hidden Control Panel Circuit Induction

Deterministic split of the self-rendered raw corpus into public/private. Splits,
re-encodes the clips, and anonymises ids; runs NO rendering.

  1. Read raw scenes.csv (one row per panel clip) + the raw videos.
  2. Deterministic salted hash split on scene_hash (~1/3 to test).
  3. Shuffle scenes with a fixed seed BEFORE assigning sequential integer ids, so
     the public id carries no scene_hash / generation-order signal.
  4. Re-encode each MP4 (strips container metadata + byte-level identity).
  5. Emit public train/test + submission template; the labels for TEST scenes and
     ALL hidden grouping columns live ONLY in private/answers.csv. The initial
     switch positions are visible in the clip and are NOT exposed in any CSV.

OUTPUT
    public/train/videos/<id>.mp4        public/test/videos/<id>.mp4
    public/train.csv  id, video, n_switches, n_lamps, flip_log_json, query_config,
                      prompt, wiring_json, query_pattern
    public/test.csv   id, video, n_switches, n_lamps, flip_log_json, query_config,
                      prompt
    public/sample_submission.csv  id, wiring_json, query_pattern, confidence
    private/answers.csv  id, wiring_json, query_pattern, n_lamps, split_group,
                         ood_axis, render_style
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

SPLIT_SALT = "panel-circuit-v1"
TEST_PER_1000 = 333
ID_SHUFFLE_SEED = int(hashlib.sha256(f"{SPLIT_SALT}:idmap".encode("utf-8")).hexdigest()[:8], 16)

PROMPT = ("Induce each lamp's wiring (logic gate + the switch ids that drive it) from the "
          "panel clip and the flip log, then predict the on/off pattern of all lamps for the "
          "held-out query switch configuration.")


def _split_of(scene_hash: str) -> str:
    h = hashlib.sha256(f"{SPLIT_SALT}:{scene_hash}".encode("utf-8")).hexdigest()
    return "test" if (int(h[:8], 16) % 1000) < TEST_PER_1000 else "train"


def _reencode(src: Path, dst: Path) -> None:
    # Stream frames one at a time so the whole clip is never materialised in
    # memory (the re-encode stays O(1) in frame count). We drive the ffmpeg
    # backend through imageio's streaming reader/writer rather than the pyav
    # write plugin: pyav's write path is not available on the grader image
    # (imopen(..., plugin="pyav") raises there), whereas the ffmpeg backend is
    # the same one that decodes these clips, so it is always present.
    import imageio.v2 as iio2
    reader = iio2.get_reader(src)
    try:
        fps = float(reader.get_meta_data().get("fps", 10) or 10)
    except Exception:
        fps = 10.0
    writer = iio2.get_writer(dst, fps=fps, codec="libx264",
                             quality=7, macro_block_size=16)
    try:
        for frame in reader:            # lazy ffmpeg pipe -> one frame at a time
            writer.append_data(frame)
    finally:
        writer.close()
        reader.close()


def _find_video(raw: Path, scene_hash: str) -> Path:
    m = sorted(raw.glob(f"videos/{scene_hash}.[mM][pP]4"))
    if not m:
        raise FileNotFoundError(f"No video for {scene_hash}")
    return m[0]


def prepare(raw: Path, public: Path, private: Path) -> None:
    raw = Path(raw); public = Path(public); private = Path(private)
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    scenes = pd.read_csv(raw / "scenes.csv", dtype={"scene_hash": str})
    scenes = scenes.sort_values("scene_hash").reset_index(drop=True)
    scenes["split"] = scenes["scene_hash"].map(_split_of)
    train_h = scenes.loc[scenes["split"] == "train", "scene_hash"].tolist()
    test_h = scenes.loc[scenes["split"] == "test", "scene_hash"].tolist()

    rng = np.random.default_rng(ID_SHUFFLE_SEED)
    train_h = [train_h[i] for i in rng.permutation(len(train_h))]
    test_h = [test_h[i] for i in rng.permutation(len(test_h))]

    id_map = {h: i for i, h in enumerate(train_h)}
    id_map.update({h: len(train_h) + i for i, h in enumerate(test_h)})

    tr_dir = public / "train" / "videos"
    te_dir = public / "test" / "videos"
    tr_dir.mkdir(parents=True, exist_ok=True)
    te_dir.mkdir(parents=True, exist_ok=True)

    train_rows, test_rows, sample_rows, answer_rows = [], [], [], []
    by_hash = {r["scene_hash"]: r for _, r in scenes.iterrows()}

    for h, rid in sorted(id_map.items(), key=lambda kv: kv[1]):
        srow = by_hash[h]
        is_train = srow["split"] == "train"
        name = f"{rid:06d}.mp4"
        _reencode(_find_video(raw, h), (tr_dir if is_train else te_dir) / name)
        L = int(srow["n_lamps"])

        # carry the split prefix so the path resolves relative to the public/
        # root where the CSV lives (public/train/videos/<id>.mp4 etc.).
        split_dir = "train" if is_train else "test"
        common = {
            "id": rid, "video": f"{split_dir}/videos/{name}", "n_switches": int(srow["n_switches"]),
            "n_lamps": L, "flip_log_json": srow["flip_log_json"],
            "query_config": srow["query_config"], "prompt": PROMPT,
        }
        wiring = srow["wiring_json"]; qpat = srow["query_pattern"]

        if is_train:
            row = dict(common)
            row.update({"wiring_json": wiring, "query_pattern": qpat})
            train_rows.append(row)
        else:
            test_rows.append(common)
            sample_rows.append({
                "id": rid,
                "wiring_json": json.dumps({str(j): {"gate": "OR", "inputs": [0]} for j in range(L)}),
                "query_pattern": json.dumps([0] * L), "confidence": 0.5,
            })
            answer_rows.append({
                "id": rid, "wiring_json": wiring, "query_pattern": qpat, "n_lamps": L,
                "split_group": f"{srow['circuit_family']}_{srow['variant']}",
                "ood_axis": str(srow["ood_axis"]), "render_style": str(srow["render_style"]),
            })

    train_cols = ["id", "video", "n_switches", "n_lamps", "flip_log_json", "query_config",
                  "prompt", "wiring_json", "query_pattern"]
    test_cols = ["id", "video", "n_switches", "n_lamps", "flip_log_json", "query_config", "prompt"]
    sample_cols = ["id", "wiring_json", "query_pattern", "confidence"]
    ans_cols = ["id", "wiring_json", "query_pattern", "n_lamps", "split_group", "ood_axis",
                "render_style"]

    def _w(rows, cols, path):
        pd.DataFrame(rows, columns=cols).sort_values("id").reset_index(drop=True).to_csv(path, index=False)

    _w(train_rows, train_cols, public / "train.csv")
    _w(test_rows, test_cols, public / "test.csv")
    _w(sample_rows, sample_cols, public / "sample_submission.csv")
    _w(answer_rows, ans_cols, private / "answers.csv")

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

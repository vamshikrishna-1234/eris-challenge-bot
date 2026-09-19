import json
import pickle
import shutil
import tempfile
from pathlib import Path

import cv2
import numpy as np
import pandas as pd

from grade import REQUIRED_COLUMNS, grade
from prepare import prepare


def _write_video(path: Path, seed: int, depth: bool = False):
    rng = np.random.default_rng(seed)
    path.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"MJPG"), 30.0, (96, 72))
    for t in range(36 + seed % 18):
        frame = np.zeros((72, 96, 3), dtype=np.uint8)
        x = int(12 + (t * (1 + seed % 4)) % 70)
        y = int(22 + 10 * np.sin(t / 7 + seed))
        color = (80 + seed % 120, 180, 230) if not depth else (30 + t * 3 % 200, 30 + t * 2 % 200, 30 + t % 200)
        cv2.rectangle(frame, (x, max(0, y - 5)), (min(95, x + 18), min(71, y + 8)), color, -1)
        noise = rng.normal(0, 4, frame.shape).astype(np.int16)
        frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        writer.write(frame)
    writer.release()


def _traj(n: int, seed: int, cart: bool):
    x = np.linspace(0, 1, n)
    phase = seed * 0.07
    if cart:
        data = {
            "x": -0.55 + 0.22 * x + 0.04 * np.sin(phase + x * np.pi * 2),
            "y": -0.35 + 0.55 * x + 0.03 * np.cos(phase + x * np.pi * 3),
            "z": 0.85 + 0.25 * np.sin(x * np.pi),
            "qx": -0.8 + 0.05 * np.sin(x + phase),
            "qy": 0.1 + 0.2 * x,
            "qz": 0.2 * np.cos(x + phase),
            "qw": 0.4 + 0.1 * np.sin(2 * x + phase),
        }
    else:
        data = {f"Panda_joint{i}": np.sin(x * (i + 1) + phase) * (0.4 + i / 20) for i in range(1, 8)}
    return pd.DataFrame(data)


def _build_fixture(raw: Path, n: int = 96):
    root = raw / "PandaHandover_Real_Val"
    root.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        sid = f"{10000 + i}"
        _write_video(root / f"panda_pyrep_rgb_{sid}.avi", i, False)
        _write_video(root / f"panda_pyrep_depth_{sid}.avi", i + 1000, True)
        rows = 150 + (i % 25)
        for prefix, cart in [
            ("giver_joint_trajectories", False),
            ("receiver_joint_trajectories", False),
            ("giver_cartesian_trajectories", True),
            ("receiver_cartesian_trajectories", True),
        ]:
            df = _traj(rows, i + (13 if "receiver" in prefix else 0), cart)
            with (root / f"panda_pyrep_{prefix}_{sid}.pkl").open("wb") as f:
                pickle.dump(df, f)


def main():
    base = Path(tempfile.mkdtemp(prefix="rctr_smoke_"))
    try:
        raw = base / "raw"
        public = base / "public"
        private = base / "private"
        _build_fixture(raw)
        prepare(raw, public, private)
        answers = pd.read_csv(private / "answers.csv")
        perfect = pd.DataFrame(
            {
                "id": answers["id"],
                "controller_segments_json": answers["controller_segments_json"],
                "key_waypoints_json": answers["key_waypoints_json"],
                "event_frames_json": answers["event_frames_json"],
                "confidence": 1.0,
            }
        )
        perfect_path = base / "perfect.csv"
        perfect.to_csv(perfect_path, index=False)
        perfect_score = grade(str(perfect_path), str(private / "answers.csv"))
        assert abs(perfect_score - 1.0) < 1e-12, perfect_score

        sample_score = grade(str(public / "sample_submission.csv"), str(private / "answers.csv"))
        # The synthetic fixture is intentionally small and more varied than the real
        # Panda handover subset; the real prepared split baseline is checked in
        # _analyze.py. Here we only require a valid, non-perfect sample file.
        assert 0.0 <= sample_score < 0.5, sample_score

        malformed = perfect.copy()
        malformed.loc[0, "controller_segments_json"] = "{bad json"
        malformed_path = base / "malformed.csv"
        malformed.to_csv(malformed_path, index=False)
        malformed_score = grade(str(malformed_path), str(private / "answers.csv"))
        assert 0.0 < malformed_score < 1.0, malformed_score

        bad_cols = perfect[REQUIRED_COLUMNS[:-1]]
        bad_path = base / "bad_cols.csv"
        bad_cols.to_csv(bad_path, index=False)
        assert grade(str(bad_path), str(private / "answers.csv")) == 0.0

        duplicate = perfect.copy()
        duplicate.loc[1, "id"] = duplicate.loc[0, "id"]
        duplicate_path = base / "duplicate.csv"
        duplicate.to_csv(duplicate_path, index=False)
        assert grade(str(duplicate_path), str(private / "answers.csv")) == 0.0

        missing = perfect.iloc[:-1].copy()
        missing_path = base / "missing.csv"
        missing.to_csv(missing_path, index=False)
        assert grade(str(missing_path), str(private / "answers.csv")) == 0.0

        bad_conf = perfect.copy()
        bad_conf.loc[0, "confidence"] = 1.5
        bad_conf_path = base / "bad_conf.csv"
        bad_conf.to_csv(bad_conf_path, index=False)
        assert grade(str(bad_conf_path), str(private / "answers.csv")) == 0.0

        nul_path = base / "nul.csv"
        nul_path.write_bytes(perfect_path.read_bytes() + b"\x00")
        assert grade(str(nul_path), str(private / "answers.csv")) == 0.0

        print(json.dumps({"perfect": perfect_score, "sample": sample_score, "malformed": malformed_score}, indent=2))
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    main()

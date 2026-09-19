from __future__ import annotations

import hashlib
import os
import shutil
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd


os.environ.setdefault("WAGGLE_MIN_GROUP_TEST", "1")
os.environ.setdefault("WAGGLE_MAX_EPISODES", "48")

from grade import InvalidSubmissionError, REQUIRED_COLUMNS, grade  # noqa: E402
from prepare import SUBMISSION_COLUMNS, prepare  # noqa: E402


TRAIN_DATES = ["2019-08-25", "2019-08-27"]
TEST_DATES = ["2019-09-05", "2019-09-11"]


def _iso(base: pd.Timestamp, seconds: float) -> str:
    return (base + pd.Timedelta(seconds=float(seconds))).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _write_tiny_raw(root: Path) -> None:
    raw = root
    tracks_dir = raw / "Berlin2019_tracks"
    tracks_dir.mkdir(parents=True, exist_ok=True)
    dances = []
    followers = []
    waggles = []
    verified = []
    feeder = [
        {
            "date": "2019-08-25",
            "feeder_cam_id": 1,
            "coordinates": "",
            "time_opened": "2019-08-25T12:00:00.000000Z",
            "time_closed": "2019-08-25T17:00:00.000000Z",
            "sucrose_solution": "varying",
        }
    ]
    dance_no = 0
    for date in TRAIN_DATES + TEST_DATES:
        track_rows = []
        base_day = pd.Timestamp(f"{date}T12:00:00Z")
        for i in range(16):
            start = base_day + pd.Timedelta(seconds=90 * i)
            dur = 22.0 + (i % 5) * 4.0
            cam = i % 2
            dancer = f"{date.replace('-', '')}{1000 + i}"
            dance_id = str(10_000_000_000_000_000_000 + dance_no)
            mx = 120.0 + (i % 4) * 28.0
            my = 145.0 + (i % 3) * 18.0
            dances.append(
                {
                    "dancer_id": dancer,
                    "dance_id": dance_id,
                    "ts_from": _iso(start, 0),
                    "ts_to": _iso(start, dur),
                    "cam_id": cam,
                    "median_x": mx,
                    "median_y": my,
                    "feeder_cam_id": 1,
                }
            )
            if date == "2019-09-05" and i < 3:
                verified.append(
                    {
                        "dance_id": dance_id,
                        "dancer_id": dancer,
                        "cam_id": cam,
                        "feeder_cam_id": 1,
                        "dance_start": _iso(start, 0),
                        "dance_end": _iso(start, dur),
                    }
                )
            bee_ids = [dancer] + [f"{date.replace('-', '')}{2000 + i * 20 + j}" for j in range(20)]
            followers.append(
                {
                    "dance_id": dance_id,
                    "follower_id": bee_ids[1],
                    "ts_from": _iso(start, 2),
                    "ts_to": _iso(start, min(dur, 12)),
                    "label": "follower",
                    "cam_id": cam,
                }
            )
            followers.append(
                {
                    "dance_id": dance_id,
                    "follower_id": bee_ids[2],
                    "ts_from": _iso(start, 4),
                    "ts_to": _iso(start, min(dur, 14)),
                    "label": "attendance",
                    "cam_id": cam,
                }
            )
            for k in range(5 + (i % 4)):
                tt = 1.5 + k * (dur - 3.0) / max(1, 4 + (i % 4))
                waggles.append(
                    {
                        "timestamp": _iso(start, tt),
                        "cam_id": cam,
                        "x_median": mx + np.sin(k) * 8.0,
                        "y_median": my + np.cos(k) * 7.0,
                        "waggle_angle": 0.2 * k,
                    }
                )
            frames = np.arange(0, int(dur * 6), dtype=int)
            for b_idx, bee in enumerate(bee_ids):
                offset_x = (b_idx % 7 - 3) * 13.0
                offset_y = (b_idx // 7 - 1) * 14.0
                for frame in frames:
                    t = frame / 6.0
                    wiggle = 2.0 * np.sin(0.7 * t + b_idx)
                    if bee == dancer:
                        wiggle += 4.0 * np.sin(3.5 * t)
                    x = mx + offset_x + wiggle + 0.03 * frame
                    y = my + offset_y + 1.8 * np.cos(0.5 * t + b_idx)
                    orientation = np.arctan2(0.2 + np.cos(0.5 * t + b_idx), 0.3 + np.sin(0.7 * t + b_idx))
                    track_rows.append(
                        {
                            "cam_id": cam,
                            "timestamp": _iso(start, t).replace("Z", "+00:00"),
                            "frame_id": str(90_000_000_000_000_000 + dance_no * 1000 + frame),
                            "track_id": str(80_000_000_000_000_000 + dance_no * 100 + b_idx),
                            "bee_id": bee,
                            "bee_id_confidence": round(0.72 + 0.02 * ((b_idx + i) % 12), 6),
                            "x_pos_hive": round(x, 3),
                            "y_pos_hive": round(y, 3),
                            "orientation_hive": round(float(orientation), 6),
                        }
                    )
            dance_no += 1
        pd.DataFrame(track_rows).to_csv(tracks_dir / f"{date}.csv", index=False)

    pd.DataFrame(dances).to_csv(raw / "Berlin2019_dances.csv", index=False)
    pd.DataFrame(followers).to_csv(raw / "Berlin2019_followers.csv", index=False)
    pd.DataFrame(waggles).to_csv(raw / "Berlin2019_waggle_phases.csv", index=False)
    pd.DataFrame(verified).to_csv(raw / "Berlin2019_dances_with_manually_verified_times.csv", index=False)
    pd.DataFrame(feeder).to_csv(raw / "Berlin2019_feeder_experiment_log.csv", index=False)
    pd.DataFrame(
        [
            {
                "timestamp": _iso(pd.Timestamp("2019-08-25T12:00:00Z"), 0),
                "frame_id": "1",
                "bee_id": "1",
                "label": "nothing",
            }
        ]
    ).to_csv(raw / "Berlin2019_dance_classifier_labels.csv", index=False)


def _hash_tree(path: Path) -> str:
    h = hashlib.sha256()
    for file in sorted(p for p in path.rglob("*") if p.is_file()):
        h.update(file.relative_to(path).as_posix().encode())
        h.update(file.read_bytes())
    return h.hexdigest()


def _perfect_from_answers(answers: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id": answers["id"].astype(str),
            "dancer_id": answers["dancer_id"].astype(str),
            "waggle_intervals_json": answers["waggle_intervals_json"].astype(str),
            "roles_json": answers["roles_json"].astype(str),
            "edges_json": answers["edges_json"].astype(str),
            "confidence": 1.0,
        },
        columns=SUBMISSION_COLUMNS,
    )


def main() -> None:
    here = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        raw = tmp / "raw"
        public = tmp / "public"
        private = tmp / "private"
        _write_tiny_raw(raw)
        prepare(raw, public, private)
        digest1 = _hash_tree(public) + _hash_tree(private)
        public2 = tmp / "public2"
        private2 = tmp / "private2"
        prepare(raw, public2, private2)
        digest2 = _hash_tree(public2) + _hash_tree(private2)
        if digest1 != digest2:
            raise AssertionError("prepare.py is not deterministic on the tiny fixture")

        answers = pd.read_csv(private / "answers.csv")
        sample = pd.read_csv(public / "sample_submission.csv")
        perfect = _perfect_from_answers(answers)
        perfect_score = grade(perfect, answers)
        sample_score = grade(sample, answers)
        if abs(perfect_score - 1.0) > 1e-12:
            raise AssertionError(f"perfect score should be 1.0, got {perfect_score}")
        if not (0.0 <= sample_score < 1.0):
            raise AssertionError(f"sample score out of range: {sample_score}")

        malformed = perfect.copy()
        malformed.loc[0, "roles_json"] = "{not-json"
        malformed_score = grade(malformed, answers)
        if not (0.0 <= malformed_score < 1.0):
            raise AssertionError(f"malformed row-local JSON did not degrade cleanly: {malformed_score}")

        invalid = perfect[REQUIRED_COLUMNS[:-1]].copy()
        try:
            grade(invalid, answers)
        except InvalidSubmissionError:
            pass
        else:
            raise AssertionError("invalid structural submission should raise InvalidSubmissionError")

        df_call_score = grade(pd.read_csv(public / "sample_submission.csv"), pd.read_csv(private / "answers.csv"))
        path_call_score = grade(public / "sample_submission.csv", private / "answers.csv")
        if abs(df_call_score - path_call_score) > 1e-12:
            raise AssertionError("DataFrame-call and path-call scores differ")

        if os.environ.get("WAGGLE_KEEP_SMOKE_OUTPUT"):
            dest = here / "_smoke_output"
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(tmp, dest)

        print(f"tiny rows: train={len(pd.read_csv(public / 'train.csv'))} test={len(answers)}")
        print(f"perfect_score={perfect_score:.12f}")
        print(f"tiny_fixture_sample_score={sample_score:.12f}")
        print(f"malformed_score={malformed_score:.12f}")
        print("determinism=pass")
        print("dataframe_call=pass")

    real_public = Path(__file__).resolve().parent / "public"
    real_private = Path(__file__).resolve().parent / "private"
    if (real_public / "sample_submission.csv").exists() and (real_private / "answers.csv").exists():
        real_sample = pd.read_csv(real_public / "sample_submission.csv")
        real_answers = pd.read_csv(real_private / "answers.csv")
        real_score = grade(real_sample, real_answers)
        if not (0.12 <= real_score < 0.5):
            raise AssertionError(f"real sample score should be weak but above platform floor, got {real_score}")
        print(f"real_sample_score={real_score:.12f}")


if __name__ == "__main__":
    main()

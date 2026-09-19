import json
import shutil
import tempfile
from pathlib import Path

import pandas as pd

import grade as grade_module
from _sanity_smoke import _build_fixture
from grade import grade
from prepare import prepare


def _score(rows, answers_path: Path, path: Path) -> float:
    pd.DataFrame(rows).to_csv(path, index=False)
    return grade(str(path), str(answers_path))


def _generic_row(pid, confidence=0.3):
    return {
        "id": pid,
        "controller_segments_json": json.dumps(
            [{"mode": "cartesian_move", "arm": "both", "start_frame": 0, "end_frame": 47}],
            separators=(",", ":"),
        ),
        "key_waypoints_json": json.dumps(
            [
                {"arm": "giver", "kind": "start", "frame": 0, "xyz_bins": [4, 4, 4]},
                {"arm": "giver", "kind": "handover", "frame": 24, "xyz_bins": [4, 4, 4]},
                {"arm": "receiver", "kind": "handover", "frame": 24, "xyz_bins": [4, 4, 4]},
                {"arm": "receiver", "kind": "end", "frame": 47, "xyz_bins": [4, 4, 4]},
            ],
            separators=(",", ":"),
        ),
        "event_frames_json": json.dumps(
            [
                {"event": "motion_start", "arm": "both", "frame": 0},
                {"event": "handover_pause", "arm": "both", "frame": 24},
                {"event": "motion_stop", "arm": "both", "frame": 47},
            ],
            separators=(",", ":"),
        ),
        "confidence": confidence,
    }


def _best_head_template(train: pd.DataFrame, column: str, item_score):
    golds = [json.loads(x) for x in train[column].astype(str)]
    unique = []
    seen = set()
    for obj in golds:
        key = json.dumps(obj, sort_keys=True, separators=(",", ":"))
        if key not in seen:
            seen.add(key)
            unique.append(obj)
    best_obj, best_score = unique[0], -1.0
    for cand in unique:
        score = sum(grade_module._match_f1(cand, gold, item_score) for gold in golds) / len(golds)
        if score > best_score:
            best_obj, best_score = cand, score
    return best_obj


def main():
    base = Path(tempfile.mkdtemp(prefix="rctr_grade_redteam_"))
    try:
        raw = base / "raw"
        public = base / "public"
        private = base / "private"
        _build_fixture(raw, 96)
        prepare(raw, public, private)
        train = pd.read_csv(public / "train.csv")
        test = pd.read_csv(public / "test.csv")
        answers = pd.read_csv(private / "answers.csv")
        answers_path = private / "answers.csv"

        results = {}
        results["sample"] = grade(str(public / "sample_submission.csv"), str(answers_path))

        results["empty_lists"] = _score(
            [
                {
                    "id": r.id,
                    "controller_segments_json": "[]",
                    "key_waypoints_json": "[]",
                    "event_frames_json": "[]",
                    "confidence": 0.0,
                }
                for r in test.itertuples(index=False)
            ],
            answers_path,
            base / "empty.csv",
        )

        results["generic_broad"] = _score(
            [_generic_row(r.id) for r in test.itertuples(index=False)],
            answers_path,
            base / "generic.csv",
        )

        segs = [
            {"mode": mode, "arm": arm, "start_frame": 0, "end_frame": 47}
            for mode in ["joint_move", "cartesian_move", "wait", "contact_like_pause"]
            for arm in ["giver", "receiver", "both"]
        ]
        wps = [
            {"arm": arm, "kind": kind, "frame": 24, "xyz_bins": [4, 4, 4]}
            for arm in ["giver", "receiver"]
            for kind in ["start", "approach", "handover", "retreat", "end"]
        ]
        evs = [
            {"event": event, "arm": arm, "frame": 24}
            for event in ["motion_start", "handover_pause", "release_like", "motion_stop"]
            for arm in ["both", "giver"]
        ]
        results["shotgun_template"] = _score(
            [
                {
                    "id": r.id,
                    "controller_segments_json": json.dumps(segs, separators=(",", ":")),
                    "key_waypoints_json": json.dumps(wps, separators=(",", ":")),
                    "event_frames_json": json.dumps(evs, separators=(",", ":")),
                    "confidence": 0.4,
                }
                for r in test.itertuples(index=False)
            ],
            answers_path,
            base / "shotgun.csv",
        )

        first_train = train.iloc[0]
        results["first_train_copy"] = _score(
            [
                {
                    "id": r.id,
                    "controller_segments_json": first_train.controller_segments_json,
                    "key_waypoints_json": first_train.key_waypoints_json,
                    "event_frames_json": first_train.event_frames_json,
                    "confidence": 0.4,
                }
                for r in test.itertuples(index=False)
            ],
            answers_path,
            base / "first_train.csv",
        )

        best_single = 0.0
        for _, tr in train.iterrows():
            best_single = max(
                best_single,
                _score(
                    [
                        {
                            "id": r.id,
                            "controller_segments_json": tr.controller_segments_json,
                            "key_waypoints_json": tr.key_waypoints_json,
                            "event_frames_json": tr.event_frames_json,
                            "confidence": 0.4,
                        }
                        for r in test.itertuples(index=False)
                    ],
                    answers_path,
                    base / "single_train.csv",
                ),
            )
        results["best_single_train_template_oracle"] = best_single

        best_segments = _best_head_template(train, "controller_segments_json", grade_module._segment_item_score)
        best_waypoints = _best_head_template(train, "key_waypoints_json", grade_module._waypoint_item_score)
        best_events = _best_head_template(train, "event_frames_json", grade_module._event_item_score)
        best_constant_heads = 0.0
        for conf in [i / 20 for i in range(21)]:
            best_constant_heads = max(
                best_constant_heads,
                _score(
                    [
                        {
                            "id": r.id,
                            "controller_segments_json": json.dumps(best_segments, separators=(",", ":")),
                            "key_waypoints_json": json.dumps(best_waypoints, separators=(",", ":")),
                            "event_frames_json": json.dumps(best_events, separators=(",", ":")),
                            "confidence": conf,
                        }
                        for r in test.itertuples(index=False)
                    ],
                    answers_path,
                    base / f"constant_heads_{int(conf * 100):03d}.csv",
                ),
            )
        results["train_optimized_constant_heads"] = best_constant_heads

        bad = pd.DataFrame([_generic_row(r.id) for r in test.itertuples(index=False)])
        bad[["id", "controller_segments_json", "key_waypoints_json", "confidence"]].to_csv(base / "bad_columns.csv", index=False)
        results["bad_columns"] = grade(str(base / "bad_columns.csv"), str(answers_path))

        dup = pd.DataFrame([_generic_row(r.id) for r in test.itertuples(index=False)])
        dup.loc[1, "id"] = dup.loc[0, "id"]
        dup.to_csv(base / "duplicate.csv", index=False)
        results["duplicate_id"] = grade(str(base / "duplicate.csv"), str(answers_path))

        malformed = pd.DataFrame(
            [
                {
                    "id": r.id,
                    "controller_segments_json": r.controller_segments_json,
                    "key_waypoints_json": r.key_waypoints_json,
                    "event_frames_json": r.event_frames_json,
                    "confidence": 1.0,
                }
                for r in answers.itertuples(index=False)
            ]
        )
        malformed.loc[0, "event_frames_json"] = '[{"event":"motion_start","arm":"both","frame":true}]'
        malformed_score = _score(malformed.to_dict("records"), answers_path, base / "malformed.csv")
        results["one_row_invalid_schema"] = malformed_score

        print(json.dumps(results, indent=2, sort_keys=True))
        assert 0.0 <= results["sample"] < 0.30
        assert results["empty_lists"] == 0.0
        assert results["bad_columns"] == 0.0
        assert results["duplicate_id"] == 0.0
        assert results["generic_broad"] < 0.08
        assert results["shotgun_template"] < 0.02
        assert results["first_train_copy"] < 0.25
        assert results["best_single_train_template_oracle"] < 0.35
        assert results["train_optimized_constant_heads"] < 0.60
        expected_one_bad_row = (len(answers) - 1) / len(answers)
        assert abs(results["one_row_invalid_schema"] - expected_one_bad_row) < 0.02
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    main()

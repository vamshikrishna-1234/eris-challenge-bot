import argparse
import json
import re
from pathlib import Path

import pandas as pd

import grade as grade_module
from grade import grade


RAW_ID_RE = re.compile(r"(panda_pyrep|PandaHandover|Real_Val|Real_Test|Real_Train|_\d{4,}\.)")


def _check_public_leaks(public: Path):
    train = pd.read_csv(public / "train.csv")
    test = pd.read_csv(public / "test.csv")
    issues = []
    forbidden_cols = {"source_id", "raw_id", "filename", "trial", "source_file", "source_path"}
    for name, df in [("train", train), ("test", test)]:
        overlap = forbidden_cols & set(df.columns)
        if overlap:
            issues.append(f"{name} has forbidden columns: {sorted(overlap)}")
        text = "\n".join(df.astype(str).agg(" ".join, axis=1).head(200).tolist())
        if RAW_ID_RE.search(text):
            issues.append(f"{name} contains raw-id-like text in public CSV values")
    public_ids = pd.concat([train["id"], test["id"]]).astype(str).tolist()
    if len(public_ids) != len(set(public_ids)):
        issues.append("duplicate public IDs across train/test")
    if not all(x.startswith("rctr_") for x in public_ids):
        issues.append("public IDs do not use the opaque rctr_ prefix")
    if any(re.fullmatch(r"rctr_\d+", x) for x in public_ids):
        issues.append("public IDs are purely numeric rather than hash-like tokens")
    for video_col in ["rgb_video", "depth_video"]:
        for name, df in [("train", train), ("test", test)]:
            bad = df[video_col].astype(str).map(lambda x: bool(RAW_ID_RE.search(x))).sum()
            if bad:
                issues.append(f"{name}.{video_col} has raw-id-like filenames")
    train_paths = set(train["rgb_video"].astype(str)) | set(train["depth_video"].astype(str))
    test_paths = set(test["rgb_video"].astype(str)) | set(test["depth_video"].astype(str))
    if train_paths & test_paths:
        issues.append("train/test video paths overlap")
    public_root = public
    sizes = []
    for df in [train, test]:
        for col in ["rgb_video", "depth_video"]:
            for rel in df[col].astype(str):
                p = public_root / rel
                if not p.exists():
                    issues.append(f"missing public video path: {rel}")
                else:
                    sizes.append(p.stat().st_size)
    if sizes and len(set(sizes)) != 1:
        issues.append(f"public video file sizes are not fixed: {min(sizes)}..{max(sizes)}")
    state_text = "\n".join(pd.concat([train["state_observation_json"], test["state_observation_json"]]).astype(str).tolist())
    if re.search(r"\d+\.\d{3,}", state_text):
        issues.append("state observations appear to expose high-precision raw floats")
    return issues, train, test


def _duration_transfer_baseline(train: pd.DataFrame, test: pd.DataFrame, out_path: Path):
    rows = []
    train_dur = train["duration_frames"].to_numpy()
    for _, row in test.iterrows():
        j = int(abs(train_dur - row["duration_frames"]).argmin())
        src = train.iloc[j]
        rows.append(
            {
                "id": row["id"],
                "controller_segments_json": src["controller_segments_json"],
                "key_waypoints_json": src["key_waypoints_json"],
                "event_frames_json": src["event_frames_json"],
                "confidence": 0.30,
            }
        )
    pd.DataFrame(rows).to_csv(out_path, index=False)


def _state_exact_transfer_baseline(train: pd.DataFrame, test: pd.DataFrame, out_path: Path):
    rows = []
    by_state = {}
    for _, row in train.iterrows():
        by_state.setdefault(row["state_observation_json"], row)
    fallback = train.iloc[0]
    for _, row in test.iterrows():
        src = by_state.get(row["state_observation_json"], fallback)
        rows.append(
            {
                "id": row["id"],
                "controller_segments_json": src["controller_segments_json"],
                "key_waypoints_json": src["key_waypoints_json"],
                "event_frames_json": src["event_frames_json"],
                "confidence": 0.30,
            }
        )
    pd.DataFrame(rows).to_csv(out_path, index=False)


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


def _train_optimized_constant_heads_baseline(train: pd.DataFrame, test: pd.DataFrame, answers_path: Path, out_prefix: Path):
    best_segments = _best_head_template(train, "controller_segments_json", grade_module._segment_item_score)
    best_waypoints = _best_head_template(train, "key_waypoints_json", grade_module._waypoint_item_score)
    best_events = _best_head_template(train, "event_frames_json", grade_module._event_item_score)
    best_score = 0.0
    for conf in [i / 20 for i in range(21)]:
        out_path = out_prefix.with_name(f"{out_prefix.name}_{int(conf * 100):03d}.csv")
        rows = [
            {
                "id": row.id,
                "controller_segments_json": json.dumps(best_segments, separators=(",", ":")),
                "key_waypoints_json": json.dumps(best_waypoints, separators=(",", ":")),
                "event_frames_json": json.dumps(best_events, separators=(",", ":")),
                "confidence": conf,
            }
            for row in test.itertuples(index=False)
        ]
        pd.DataFrame(rows).to_csv(out_path, index=False)
        best_score = max(best_score, grade(str(out_path), str(answers_path)))
        out_path.unlink(missing_ok=True)
    return best_score


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--public", type=Path, default=Path("public"))
    parser.add_argument("--private", type=Path, default=Path("private"))
    args = parser.parse_args()
    public = args.public
    private = args.private
    if not (public / "train.csv").exists() or not (private / "answers.csv").exists():
        raise SystemExit("run prepare.py first, then pass --public and --private if needed")

    issues, train, test = _check_public_leaks(public)
    sample_score = grade(str(public / "sample_submission.csv"), str(private / "answers.csv"))
    duration_path = public / "_duration_transfer_submission.csv"
    _duration_transfer_baseline(train, test, duration_path)
    duration_score = grade(str(duration_path), str(private / "answers.csv"))
    duration_path.unlink(missing_ok=True)
    state_path = public / "_state_exact_transfer_submission.csv"
    _state_exact_transfer_baseline(train, test, state_path)
    state_score = grade(str(state_path), str(private / "answers.csv"))
    state_path.unlink(missing_ok=True)
    constant_score = _train_optimized_constant_heads_baseline(
        train,
        test,
        private / "answers.csv",
        public / "_train_constant_heads_submission",
    )
    report = {
        "n_train": int(len(train)),
        "n_test": int(len(test)),
        "sample_score": sample_score,
        "duration_only_transfer_score": duration_score,
        "state_exact_transfer_score": state_score,
        "train_optimized_constant_heads_score": constant_score,
        "public_leak_issues": issues,
        "checks": {
            "sample_non_degenerate_and_weak": 0.12 <= sample_score < 0.30,
            "duration_shortcut_not_saturated": duration_score < 0.35,
            "state_exact_shortcut_not_saturated": state_score < 0.40,
            "train_constant_heads_below_agent_ceiling": constant_score < 0.60,
            "no_public_raw_id_leaks": not issues,
        },
    }
    print(json.dumps(report, indent=2))
    if issues:
        raise SystemExit("public leak checks failed")
    if not (0.12 <= sample_score < 0.30):
        raise SystemExit("sample baseline is degenerate or too strong")
    if duration_score >= 0.35:
        raise SystemExit("duration-only shortcut is too strong")
    if state_score >= 0.40:
        raise SystemExit("state-exact shortcut is too strong")
    if constant_score >= 0.60:
        raise SystemExit("train-optimized constant-head shortcut is too strong")


if __name__ == "__main__":
    main()

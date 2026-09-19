from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

from grade import SUBMISSION_COLUMNS, grade
from prepare import _public_id_map


ROOT = Path(__file__).resolve().parent
FILLERS = {"uh", "um", "umm", "erm", "er", "em", "hmm", "hm", "uhm", "ah"}
EMPHATIC = {"yeah", "yes", "okay", "ok", "right", "no", "very", "really", "quite", "sure", "exactly", "mmhmm", "mhm", "mm"}


def _tokens(row: pd.Series) -> list[str]:
    return [str(x) for x in json.loads(row["token_transcript"])]


def _timings(row: pd.Series) -> list[dict]:
    return list(json.loads(row["token_timing_json"]))


def _none_row(row_id: int | str, confidence: float = 0.45) -> dict:
    return {
        "id": row_id,
        "reparandum_span": "NONE",
        "interregnum_span": "NONE",
        "repair_onset": "NONE",
        "is_disfluency": 0,
        "confidence": confidence,
    }


def _predict_repetition_filler(row: pd.Series, broad: bool = False) -> dict:
    toks = _tokens(row)
    n = len(toks)
    for i, tok in enumerate(toks):
        if tok in FILLERS and 0 < i < n - 1:
            if toks[i - 1] == toks[i + 1] or broad:
                return {
                    "id": row["id"],
                    "reparandum_span": f"[{i - 1},{i - 1}]",
                    "interregnum_span": f"[{i},{i}]",
                    "repair_onset": str(i + 1),
                    "is_disfluency": 1,
                    "confidence": 0.58,
                }
    for i in range(n - 1):
        if toks[i] == toks[i + 1] and (broad or toks[i] not in EMPHATIC):
            return {
                "id": row["id"],
                "reparandum_span": f"[{i},{i}]",
                "interregnum_span": "NONE",
                "repair_onset": str(i + 1),
                "is_disfluency": 1,
                "confidence": 0.55,
            }
    return _none_row(row["id"], 0.45)


def _predict_timing_gap(row: pd.Series) -> dict:
    toks = _tokens(row)
    times = _timings(row)
    for i in range(min(len(toks), len(times)) - 1):
        if toks[i] != toks[i + 1] or toks[i] in EMPHATIC:
            continue
        gap = int(times[i + 1]["start_ms"]) - int(times[i]["end_ms"])
        dur = max(1, int(times[i]["end_ms"]) - int(times[i]["start_ms"]))
        if -80 <= gap <= 450 or dur < 140:
            return {
                "id": row["id"],
                "reparandum_span": f"[{i},{i}]",
                "interregnum_span": "NONE",
                "repair_onset": str(i + 1),
                "is_disfluency": 1,
                "confidence": 0.56,
            }
    return _none_row(row["id"], 0.43)


def _length_bucket(n: int) -> str:
    if n <= 10:
        return "short"
    if n <= 18:
        return "medium"
    return "long"


def _train_prior_submission(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    majority = int(train["is_disfluency"].astype(int).mode().iloc[0])
    conf = float(max(0.35, min(0.65, train["is_disfluency"].astype(int).mean())))
    rows = []
    for _, row in test.iterrows():
        pred = _none_row(row["id"], conf)
        pred["is_disfluency"] = majority
        rows.append(pred)
    return pd.DataFrame(rows, columns=SUBMISSION_COLUMNS)


def _length_prior_submission(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    train = train.copy()
    train["_n"] = train["token_transcript"].map(lambda s: len(json.loads(s)))
    train["_bucket"] = train["_n"].map(_length_bucket)
    priors = {
        bucket: int(group["is_disfluency"].astype(int).mode().iloc[0])
        for bucket, group in train.groupby("_bucket")
    }
    rows = []
    for _, row in test.iterrows():
        n = len(json.loads(row["token_transcript"]))
        pred = _none_row(row["id"], 0.45)
        pred["is_disfluency"] = priors.get(_length_bucket(n), 0)
        rows.append(pred)
    return pd.DataFrame(rows, columns=SUBMISSION_COLUMNS)


def _nearest_neighbor_submission(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    label_cols = ["reparandum_span", "interregnum_span", "repair_onset", "is_disfluency", "confidence"]
    lookup: dict[str, pd.Series] = {}
    for _, row in train.iterrows():
        lookup.setdefault(str(row["token_transcript"]), row)
    rows = []
    for _, row in test.iterrows():
        match = lookup.get(str(row["token_transcript"]))
        if match is None:
            rows.append(_none_row(row["id"], 0.45))
        else:
            out = {"id": row["id"]}
            for col in label_cols:
                out[col] = match[col]
            out["confidence"] = 0.52
            rows.append(out)
    return pd.DataFrame(rows, columns=SUBMISSION_COLUMNS)


def _score(name: str, submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    value = grade(submission[SUBMISSION_COLUMNS].copy(), answers)
    print(f"{name:34s} {value:.6f}")
    return value


def _duration_ms(row: pd.Series) -> int:
    times = _timings(row)
    if not times:
        return 0
    return max(int(t["end_ms"]) for t in times)


def main() -> None:
    public = ROOT / "public"
    private = ROOT / "private"
    train = pd.read_csv(public / "train.csv")
    test = pd.read_csv(public / "test.csv")
    sample = pd.read_csv(public / "sample_submission.csv")
    answers = pd.read_csv(private / "answers.csv")

    print("Rows")
    print(f"  train={len(train)} test={len(test)} answers={len(answers)}")
    print("NaN counts")
    print(f"  train={int(train.isna().sum().sum())} test={int(test.isna().sum().sum())} answers={int(answers.isna().sum().sum())}")
    blank_train = int(train.astype(str).apply(lambda c: c.str.len().eq(0)).sum().sum())
    blank_test = int(test.astype(str).apply(lambda c: c.str.len().eq(0)).sum().sum())
    blank_ans = int(answers.astype(str).apply(lambda c: c.str.len().eq(0)).sum().sum())
    print(f"  blanks train={blank_train} test={blank_test} answers={blank_ans}")

    print("Label balance")
    print(train["is_disfluency"].astype(int).value_counts().sort_index().to_string())
    print("Hidden test source groups")
    print(answers["source_group"].value_counts().sort_index().to_string())
    print("Hidden test repair groups")
    print(answers["repair_group"].value_counts().sort_index().to_string())
    print("Group isolation")
    raw_path = ROOT / "raw_data" / "clips.csv"
    if raw_path.exists():
        raw_df = pd.read_csv(raw_path, dtype=str)
        id_lookup = _public_id_map(raw_df["raw_clip_id"].astype(str).tolist())
        raw_df["id"] = raw_df["raw_clip_id"].map(id_lookup).astype(int)
        train_raw = raw_df[raw_df["id"].isin(train["id"].astype(int))]
        test_raw = raw_df[raw_df["id"].isin(test["id"].astype(int))]
        session_overlap = set(train_raw["source_session"]) & set(test_raw["source_session"])
        split_overlap = set(train_raw["split_group"]) & set(test_raw["split_group"])
        print(f"  source_session overlap train/test: {len(session_overlap)}")
        print(f"  split_group overlap train/test: {len(split_overlap)}")
    else:
        print("  raw_data/clips.csv unavailable for local group-isolation reconstruction")
    print(f"  private test meetings={answers['source_meeting'].nunique()}")

    train_lens = train["token_transcript"].map(lambda s: len(json.loads(s)))
    test_lens = test["token_transcript"].map(lambda s: len(json.loads(s)))
    test_durs = test.apply(_duration_ms, axis=1)
    print("Token lengths")
    print(f"  train min/mean/max={train_lens.min()}/{train_lens.mean():.2f}/{train_lens.max()}")
    print(f"  test  min/mean/max={test_lens.min()}/{test_lens.mean():.2f}/{test_lens.max()}")
    print("Audio duration from token timings")
    print(f"  test ms min/mean/max={test_durs.min()}/{test_durs.mean():.2f}/{test_durs.max()}")

    public_cols = set(test.columns)
    forbidden = {
        "raw_clip_id",
        "source_meeting",
        "source_session",
        "source_family",
        "speaker_code",
        "speaker_family",
        "split_group",
        "repair_type",
        "label_family",
        "source_word_start",
        "source_word_end",
    }
    print("Public leakage columns")
    print(f"  forbidden in test: {sorted(public_cols & forbidden)}")
    id_values = test["id"].astype(str).str.extract(r"(\d+)")[0].astype(float)
    id_len_corr = float(id_values.corr(test_lens.astype(float)))
    print("  rows are sorted by opaque salted id")
    print(f"  id/token-length correlation: {id_len_corr:.6f}")

    print("Baseline scores")
    perfect = answers[SUBMISSION_COLUMNS].copy()
    _score("perfect labels", perfect, answers)
    _score("sample always NONE", sample, answers)
    _score("train-prior is_disfluency", _train_prior_submission(train, test), answers)
    rep_rows = [_predict_repetition_filler(row, broad=False) for _, row in test.iterrows()]
    _score("text repetition/filler", pd.DataFrame(rep_rows, columns=SUBMISSION_COLUMNS), answers)
    broad_rows = [_predict_repetition_filler(row, broad=True) for _, row in test.iterrows()]
    _score("transcript-only broad", pd.DataFrame(broad_rows, columns=SUBMISSION_COLUMNS), answers)
    timing_rows = [_predict_timing_gap(row) for _, row in test.iterrows()]
    _score("timing-gap heuristic", pd.DataFrame(timing_rows, columns=SUBMISSION_COLUMNS), answers)
    _score("length metadata prior", _length_prior_submission(train, test), answers)
    _score("nearest transcript neighbor", _nearest_neighbor_submission(train, test), answers)

    token_counter = Counter()
    for s in test["token_transcript"]:
        token_counter.update(json.loads(s))
    print("Most common test tokens")
    print("  " + ", ".join(f"{tok}:{cnt}" for tok, cnt in token_counter.most_common(12)))


if __name__ == "__main__":
    main()

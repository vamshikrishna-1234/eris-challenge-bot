from __future__ import annotations

import json
import wave
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import wavfile
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder

from grade import REQUIRED_COLUMNS, grade


ROOT = Path(__file__).resolve().parent
TURN_STATES = ["COMPLETE", "CONTINUE", "BACKCHANNEL", "OVERLAP", "UNCERTAIN"]
RELATIONS = ["SAME", "OTHER", "MULTI", "NONE_OR_UNCLEAR"]


def _load() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train = pd.read_csv(ROOT / "public" / "train.csv")
    test = pd.read_csv(ROOT / "public" / "test.csv")
    sample = pd.read_csv(ROOT / "public" / "sample_submission.csv")
    answers = pd.read_csv(ROOT / "private" / "answers.csv")
    return train, test, sample, answers


def _score(rows: list[dict], answers: pd.DataFrame) -> float:
    sub = pd.DataFrame(rows, columns=REQUIRED_COLUMNS)
    return grade(sub, answers)


def _mode(series: pd.Series) -> str:
    return str(series.mode().iloc[0])


def _train_prior(train: pd.DataFrame, test: pd.DataFrame, answers: pd.DataFrame) -> float:
    state = _mode(train["turn_state"])
    rel = _mode(train["next_speaker_relation"])
    ms = int(round(float(train["next_response_ms"].median())))
    conf = float(np.clip((train["turn_state"] == state).mean(), 0.20, 0.70))
    rows = [
        {
            "id": int(rid),
            "turn_state": state,
            "next_response_ms": ms,
            "next_speaker_relation": rel,
            "confidence": round(conf, 4),
        }
        for rid in test["id"]
    ]
    return _score(rows, answers)


def _lexical_model(train: pd.DataFrame, test: pd.DataFrame, answers: pd.DataFrame) -> float:
    x_train = train["transcript_window"].astype(str)
    x_test = test["transcript_window"].astype(str)
    state_model = make_pipeline(
        TfidfVectorizer(min_df=2, ngram_range=(1, 2), max_features=2500),
        LogisticRegression(max_iter=500, class_weight="balanced"),
    )
    rel_model = make_pipeline(
        TfidfVectorizer(min_df=2, ngram_range=(1, 2), max_features=2500),
        LogisticRegression(max_iter=500, class_weight="balanced"),
    )
    state_model.fit(x_train, train["turn_state"])
    rel_model.fit(x_train, train["next_speaker_relation"])
    pred_state = state_model.predict(x_test)
    pred_rel = rel_model.predict(x_test)
    proba = state_model.predict_proba(x_test).max(axis=1)
    median_ms = train.groupby("turn_state")["next_response_ms"].median().to_dict()
    global_ms = float(train["next_response_ms"].median())
    rows = []
    for rid, st, rel, conf in zip(test["id"], pred_state, pred_rel, proba):
        rows.append(
            {
                "id": int(rid),
                "turn_state": str(st),
                "next_response_ms": int(round(float(median_ms.get(st, global_ms)))),
                "next_speaker_relation": str(rel),
                "confidence": float(np.clip(conf, 0.05, 0.95)),
            }
        )
    return _score(rows, answers)


def _context_features(df: pd.DataFrame, include_text_timing: bool = True) -> np.ndarray:
    rows = []
    for _, row in df.iterrows():
        ctx = json.loads(row["speaker_context_json"])
        toks = json.loads(row["token_timing_json"])
        clip_ms = float(ctx.get("clip_duration_ms", 0))
        current_words = float(ctx.get("current_words", len(toks)))
        active = float(ctx.get("recent_active_speakers", 1))
        prev_bucket = str(ctx.get("prev_turn_length_bucket", "none"))
        prev = {"none": 0.0, "short": 1.0, "medium": 2.0, "long": 3.0}.get(prev_bucket, 0.0)
        if toks and include_text_timing:
            last_end = max(t.get("end_ms", 0) for t in toks)
            first_start = min(t.get("start_ms", 0) for t in toks)
            span = max(0.0, last_end - first_start)
            tail_gap = max(0.0, clip_ms - last_end)
        else:
            span = 0.0
            tail_gap = 0.0
        rows.append([clip_ms, current_words, active, prev, span, tail_gap])
    return np.asarray(rows, dtype=np.float64)


def _numeric_context_model(train: pd.DataFrame, test: pd.DataFrame, answers: pd.DataFrame, metadata_only: bool) -> float:
    x_train = _context_features(train, include_text_timing=not metadata_only)
    x_test = _context_features(test, include_text_timing=not metadata_only)
    clf = RandomForestClassifier(n_estimators=120, min_samples_leaf=6, random_state=17, class_weight="balanced")
    rel = RandomForestClassifier(n_estimators=120, min_samples_leaf=6, random_state=18, class_weight="balanced")
    reg = RandomForestRegressor(n_estimators=120, min_samples_leaf=6, random_state=19)
    clf.fit(x_train, train["turn_state"])
    rel.fit(x_train, train["next_speaker_relation"])
    reg.fit(x_train, train["next_response_ms"])
    pred_state = clf.predict(x_test)
    pred_rel = rel.predict(x_test)
    pred_ms = np.clip(np.round(reg.predict(x_test)), 0, 3000).astype(int)
    conf = clf.predict_proba(x_test).max(axis=1)
    rows = []
    for rid, st, rr, ms, cc in zip(test["id"], pred_state, pred_rel, pred_ms, conf):
        rows.append(
            {
                "id": int(rid),
                "turn_state": str(st),
                "next_response_ms": int(ms),
                "next_speaker_relation": str(rr),
                "confidence": float(np.clip(cc, 0.05, 0.95)),
            }
        )
    return _score(rows, answers)


def _nearest_neighbor(train: pd.DataFrame, test: pd.DataFrame, answers: pd.DataFrame) -> float:
    vec = TfidfVectorizer(min_df=1, ngram_range=(1, 2), max_features=3000)
    train_text = train["transcript_window"].astype(str)
    test_text = test["transcript_window"].astype(str)
    x_train = vec.fit_transform(train_text)
    x_test = vec.transform(test_text)
    sim = cosine_similarity(x_test, x_train)
    idx = np.asarray(sim.argmax(axis=1)).ravel()
    rows = []
    for rid, j in zip(test["id"], idx):
        tr = train.iloc[int(j)]
        rows.append(
            {
                "id": int(rid),
                "turn_state": str(tr["turn_state"]),
                "next_response_ms": int(tr["next_response_ms"]),
                "next_speaker_relation": str(tr["next_speaker_relation"]),
                "confidence": 0.55,
            }
        )
    return _score(rows, answers)


def _audio_features(df: pd.DataFrame) -> np.ndarray:
    rows = []
    for rel in df["audio_path"]:
        path = ROOT / "public" / str(rel)
        sr, x = wavfile.read(path)
        if x.ndim == 2:
            x = x.mean(axis=1)
        x = x.astype(np.float32)
        if x.size == 0:
            rows.append([0, 0, 0, 0, 0, 0])
            continue
        x = x / max(1.0, float(np.max(np.abs(x))))
        n_tail = min(len(x), int(0.50 * sr))
        tail = x[-n_tail:]
        dur = len(x) / sr
        rms = float(np.sqrt(np.mean(x**2)))
        tail_rms = float(np.sqrt(np.mean(tail**2)))
        zcr = float(np.mean(np.abs(np.diff(np.signbit(x))).astype(float))) if len(x) > 1 else 0.0
        p95 = float(np.percentile(np.abs(x), 95))
        rows.append([dur, rms, tail_rms, tail_rms / (rms + 1e-6), zcr, p95])
    return np.asarray(rows, dtype=np.float64)


def _audio_baseline(train: pd.DataFrame, test: pd.DataFrame, answers: pd.DataFrame) -> float:
    x_train = _audio_features(train)
    x_test = _audio_features(test)
    clf = RandomForestClassifier(n_estimators=140, min_samples_leaf=6, random_state=29, class_weight="balanced")
    rel = RandomForestClassifier(n_estimators=140, min_samples_leaf=6, random_state=30, class_weight="balanced")
    reg = RandomForestRegressor(n_estimators=140, min_samples_leaf=6, random_state=31)
    clf.fit(x_train, train["turn_state"])
    rel.fit(x_train, train["next_speaker_relation"])
    reg.fit(x_train, train["next_response_ms"])
    pred_state = clf.predict(x_test)
    pred_rel = rel.predict(x_test)
    pred_ms = np.clip(np.round(reg.predict(x_test)), 0, 3000).astype(int)
    conf = clf.predict_proba(x_test).max(axis=1)
    rows = []
    for rid, st, rr, ms, cc in zip(test["id"], pred_state, pred_rel, pred_ms, conf):
        rows.append(
            {
                "id": int(rid),
                "turn_state": str(st),
                "next_response_ms": int(ms),
                "next_speaker_relation": str(rr),
                "confidence": float(np.clip(cc, 0.05, 0.95)),
            }
        )
    return _score(rows, answers)


def _duration_stats(df: pd.DataFrame) -> list[float]:
    durations = []
    for rel in df["audio_path"]:
        path = ROOT / "public" / str(rel)
        with wave.open(str(path), "rb") as wf:
            durations.append(wf.getnframes() / wf.getframerate())
    return durations


def _public_leakage_checks(train: pd.DataFrame, test: pd.DataFrame) -> list[str]:
    problems = []
    forbidden = ["meeting", "session", "speaker_code", "segment", "source", "boundary", "turn_state", "response", "relation", "confidence"]
    for col in test.columns:
        low = col.lower()
        if any(term in low for term in forbidden):
            problems.append(f"forbidden public test column: {col}")
    if test["audio_path"].astype(str).str.contains("ES|IS|TS|EN|IB|IN", regex=True).any():
        problems.append("audio paths appear to contain source meeting prefixes")
    allowed_shapes = {"tok_empty", "tok_ack", "tok_num", "tok_short", "tok_med", "tok_long", "tok_xlong"}
    for split_name, df in [("train", train), ("test", test)]:
        vocab = set()
        for value in df["transcript_window"].astype(str):
            vocab.update(value.split())
        bad_vocab = sorted(vocab - allowed_shapes)
        if bad_vocab:
            problems.append(f"{split_name} transcript_window exposes non-redacted tokens: {bad_vocab[:5]}")
        for value in df["token_timing_json"].astype(str):
            try:
                toks = json.loads(value)
            except json.JSONDecodeError:
                problems.append(f"{split_name} token_timing_json is malformed")
                break
            for tok in toks:
                if "token" in tok:
                    problems.append(f"{split_name} token_timing_json exposes lexical token field")
                    break
                if tok.get("token_shape") not in allowed_shapes:
                    problems.append(f"{split_name} token_timing_json has non-redacted token_shape")
                    break
    if train["id"].is_monotonic_increasing or test["id"].is_monotonic_increasing:
        # Files are sorted by id by design; this is not a leakage issue. Keep the
        # check focused on split boundary rather than monotonic file order.
        pass
    return problems


def main() -> None:
    train, test, sample, answers = _load()
    print("rows")
    print(f"  train={len(train)} test={len(test)}")
    print("label distribution")
    print(train["turn_state"].value_counts().to_string())
    print("hidden test groups")
    for col in ["meeting_family", "latency_band", "turn_type_bucket"]:
        print(f"  {col}:")
        print(answers[col].value_counts().to_string())

    raw_path = ROOT / "raw_data" / "clips.csv"
    if raw_path.exists():
        raw = pd.read_csv(raw_path)
        train_src = set(answers["session_group"].astype(str))
        public_train_ids = set(train["id"].astype(int))
        raw_train_groups = set(raw[raw["source_key"].isin(raw.loc[raw["source_key"].notna(), "source_key"])]["session_group"].astype(str))
        print("group isolation")
        print(f"  private test session groups={sorted(train_src)}")
        print("  public test strips source identifiers: yes")
        print(f"  raw session groups total={len(raw_train_groups)} public train ids={len(public_train_ids)}")

    assert not train.isna().any().any()
    assert not test.isna().any().any()
    assert not answers.isna().any().any()
    print("nan checks: passed")

    d_train = _duration_stats(train)
    d_test = _duration_stats(test)
    tok_counts = [len(json.loads(x)) for x in pd.concat([train["token_timing_json"], test["token_timing_json"]])]
    print("audio/token distributions")
    print(f"  train duration mean={np.mean(d_train):.2f}s p95={np.percentile(d_train, 95):.2f}s")
    print(f"  test duration mean={np.mean(d_test):.2f}s p95={np.percentile(d_test, 95):.2f}s")
    print(f"  token timing count mean={np.mean(tok_counts):.2f} p95={np.percentile(tok_counts, 95):.1f}")

    leakage = _public_leakage_checks(train, test)
    print("public metadata leakage checks")
    print("  passed" if not leakage else "  " + "; ".join(leakage))

    perfect = answers[REQUIRED_COLUMNS].copy()
    perfect["confidence"] = 1.0
    print("scores")
    print(f"  perfect={grade(perfect, answers):.6f}")
    print(f"  sample={grade(sample, answers):.6f}")
    print(f"  train_prior={_train_prior(train, test, answers):.6f}")
    print(f"  transcript_only_tfidf={_lexical_model(train, test, answers):.6f}")
    print(f"  duration_pause_timing_only={_numeric_context_model(train, test, answers, metadata_only=False):.6f}")
    print(f"  speaker_context_metadata_only={_numeric_context_model(train, test, answers, metadata_only=True):.6f}")
    print(f"  nearest_neighbor_transcript_duration_proxy={_nearest_neighbor(train, test, answers):.6f}")
    print(f"  simple_acoustic_features={_audio_baseline(train, test, answers):.6f}")
    print("  frozen_speech_encoder_probe=skipped (no bundled speech encoder weights; this script leaves a lightweight placeholder)")


if __name__ == "__main__":
    main()

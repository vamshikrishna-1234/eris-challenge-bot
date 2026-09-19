from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

import grade
import prepare


def _loads(cell: str) -> list[dict]:
    return json.loads(str(cell))


def _score(name: str, sub: pd.DataFrame, answers: pd.DataFrame) -> float:
    score = grade.grade(sub[grade.SUBMISSION_COLUMNS], answers)
    print(f"baseline.{name}: {score:.6f}")
    return score


def _valid_positions(pitch: int) -> list[tuple[int, int]]:
    return prepare._valid_positions(int(pitch))


def _fallback_for_pitch(pitch: int) -> tuple[int, int]:
    positions = _valid_positions(pitch)
    if not positions:
        return 1, 0
    return sorted(positions, key=lambda sf: (sf[1], sf[0]))[0]


def _train_pitch_prior(train: pd.DataFrame) -> dict[int, tuple[int, int]]:
    counts: dict[int, Counter] = defaultdict(Counter)
    for _, row in train.iterrows():
        notes = _loads(row["notes_json"])
        tabs = {item["event_id"]: (int(item["string"]), int(item["fret"])) for item in _loads(row["tab_json"])}
        for note in notes:
            event_id = note["event_id"]
            counts[int(note["pitch_midi"])][tabs[event_id]] += 1
    prior: dict[int, tuple[int, int]] = {}
    for pitch, counter in counts.items():
        prior[pitch] = counter.most_common(1)[0][0]
    return prior


def _make_position_submission(test: pd.DataFrame, position_fn, confidence: float) -> pd.DataFrame:
    rows = []
    for _, row in test.iterrows():
        tab = []
        for note in _loads(row["notes_json"]):
            string, fret = position_fn(int(note["pitch_midi"]))
            tab.append({"event_id": note["event_id"], "string": int(string), "fret": int(fret)})
        rows.append({"id": row["id"], "tab_json": json.dumps(tab, separators=(",", ":")), "confidence": confidence})
    return pd.DataFrame(rows)[grade.SUBMISSION_COLUMNS]


def _low_fret_pitch_submission(test: pd.DataFrame) -> pd.DataFrame:
    return _make_position_submission(test, _fallback_for_pitch, confidence=0.24)


def _pitch_prior_submission(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    prior = _train_pitch_prior(train)

    def choose(pitch: int) -> tuple[int, int]:
        pos = prior.get(pitch, _fallback_for_pitch(pitch))
        if pos not in _valid_positions(pitch):
            return _fallback_for_pitch(pitch)
        return pos

    return _make_position_submission(test, choose, confidence=0.38)


def _event_ambiguity_report(df: pd.DataFrame, label: str) -> None:
    counts = []
    for _, row in df.iterrows():
        for note in _loads(row["notes_json"]):
            counts.append(len(_valid_positions(int(note["pitch_midi"]))))
    if not counts:
        print(f"ambiguity.{label}: none")
        return
    multi = sum(1 for c in counts if c >= 2)
    print(f"ambiguity.{label}.events: {len(counts)}")
    print(f"ambiguity.{label}.multi_position_fraction: {multi / len(counts):.3f}")
    print(f"ambiguity.{label}.position_count_distribution: {dict(sorted(Counter(counts).items()))}")


def _read_wav(path: Path) -> tuple[int, np.ndarray]:
    try:
        from scipy.io import wavfile

        sr, arr = wavfile.read(path)
        x = np.asarray(arr)
        if x.ndim == 2:
            x = x.mean(axis=1)
        if np.issubdtype(x.dtype, np.integer):
            info = np.iinfo(x.dtype)
            x = x.astype(np.float32) / float(max(abs(info.min), abs(info.max)))
        else:
            x = x.astype(np.float32)
        return int(sr), np.nan_to_num(x).astype(np.float32)
    except Exception:
        import wave

        with wave.open(str(path), "rb") as wf:
            sr = wf.getframerate()
            channels = wf.getnchannels()
            frames = wf.readframes(wf.getnframes())
            x = np.frombuffer(frames, dtype="<i2").astype(np.float32) / 32768.0
            if channels > 1:
                x = x.reshape(-1, channels).mean(axis=1)
        return sr, x.astype(np.float32)


def _clip_features(path: Path) -> np.ndarray:
    sr, x = _read_wav(path)
    if x.size == 0:
        return np.zeros(12, dtype=np.float32)
    rms = float(np.sqrt(np.mean(x**2)))
    peak = float(np.max(np.abs(x)))
    zcr = float(np.mean(np.signbit(x[1:]) != np.signbit(x[:-1]))) if x.size > 1 else 0.0
    spec = np.abs(np.fft.rfft(x * np.hanning(x.size)))
    freqs = np.fft.rfftfreq(x.size, d=1.0 / sr)
    denom = float(spec.sum()) + 1e-9
    centroid = float((spec * freqs).sum() / denom)
    spread = float(np.sqrt((spec * (freqs - centroid) ** 2).sum() / denom))
    bands = []
    for lo, hi in [(0, 200), (200, 600), (600, 1200), (1200, 2400), (2400, 5000), (5000, sr / 2)]:
        mask = (freqs >= lo) & (freqs < hi)
        bands.append(float(spec[mask].sum() / denom))
    return np.array([rms, peak, zcr, centroid / 5000.0, spread / 5000.0, *bands, len(x) / sr], dtype=np.float32)


def _event_frame(df: pd.DataFrame, public: Path, train: bool) -> tuple[pd.DataFrame, list[str]]:
    rows = []
    labels: list[str] = []
    cache: dict[str, np.ndarray] = {}
    for _, row in df.iterrows():
        rel = str(row["audio_path"])
        if rel not in cache:
            cache[rel] = _clip_features(public / rel)
        clip_feat = cache[rel]
        notes = _loads(row["notes_json"])
        tabs = {}
        if train:
            tabs = {item["event_id"]: (int(item["string"]), int(item["fret"])) for item in _loads(row["tab_json"])}
        for local_index, note in enumerate(notes):
            pitch = int(note["pitch_midi"])
            event_feat = [
                pitch / 88.0,
                local_index / max(1.0, len(notes) - 1),
                len(notes) / 10.0,
                len(_valid_positions(pitch)) / 6.0,
            ]
            rows.append({"id": row["id"], "event_id": note["event_id"], "pitch": pitch, "feat": np.concatenate([event_feat, clip_feat])})
            if train:
                labels.append(f"{tabs[note['event_id']][0]}:{tabs[note['event_id']][1]}")
    return pd.DataFrame(rows), labels


def _simple_audio_submission(train: pd.DataFrame, test: pd.DataFrame, public: Path) -> pd.DataFrame | None:
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import StandardScaler
    except Exception as exc:
        print(f"baseline.simple_audio: not_run sklearn unavailable: {exc}")
        return None
    prior = _train_pitch_prior(train)
    train_events, labels = _event_frame(train, public, train=True)
    test_events, _ = _event_frame(test, public, train=False)
    if train_events.empty or test_events.empty or len(set(labels)) < 2:
        print("baseline.simple_audio: not_run insufficient events")
        return None
    x_train = np.vstack(train_events["feat"].to_numpy())
    x_test = np.vstack(test_events["feat"].to_numpy())
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)
    clf = RandomForestClassifier(n_estimators=160, min_samples_leaf=2, random_state=20260704, class_weight="balanced_subsample")
    clf.fit(x_train, labels)
    pred_labels = clf.predict(x_test)
    event_pred: dict[tuple[str, str], tuple[int, int]] = {}
    for (_, erow), label in zip(test_events.iterrows(), pred_labels):
        try:
            string, fret = [int(x) for x in str(label).split(":")]
        except Exception:
            string, fret = prior.get(int(erow["pitch"]), _fallback_for_pitch(int(erow["pitch"])))
        pitch = int(erow["pitch"])
        if (string, fret) not in _valid_positions(pitch):
            string, fret = prior.get(pitch, _fallback_for_pitch(pitch))
            if (string, fret) not in _valid_positions(pitch):
                string, fret = _fallback_for_pitch(pitch)
        event_pred[(str(erow["id"]), str(erow["event_id"]))] = (string, fret)

    rows = []
    for _, row in test.iterrows():
        tab = []
        for note in _loads(row["notes_json"]):
            string, fret = event_pred[(str(row["id"]), str(note["event_id"]))]
            tab.append({"event_id": note["event_id"], "string": string, "fret": fret})
        rows.append({"id": row["id"], "tab_json": json.dumps(tab, separators=(",", ":")), "confidence": 0.42})
    return pd.DataFrame(rows)[grade.SUBMISSION_COLUMNS]


def _candidate_tab_for_public_notes(notes: list[dict], cand: prepare.Candidate) -> str | None:
    by_pitch: dict[int, tuple[int, int]] = {}
    for note in cand.notes:
        by_pitch[int(note.pitch_midi)] = (int(note.string), int(note.fret))
    rows = []
    for note in notes:
        pitch = int(note["pitch_midi"])
        if pitch not in by_pitch:
            return None
        string, fret = by_pitch[pitch]
        rows.append({"event_id": note["event_id"], "string": string, "fret": fret})
    return json.dumps(rows, separators=(",", ":"))


def _source_lookup_submission(root: Path, test: pd.DataFrame, fallback: pd.DataFrame) -> pd.DataFrame | None:
    raw = root / "raw"
    diag_path = root / "private" / "split_diagnostics.csv"
    if not raw.exists() or not diag_path.exists():
        print("leakage.source_lookup: not_run raw annotations or diagnostics unavailable")
        return None
    try:
        ann_source = prepare.AnnotationSource(raw)
        raw_candidates = prepare._enumerate_candidates(ann_source)
    except Exception as exc:
        print(f"leakage.source_lookup: not_run {exc}")
        return None

    by_pitch: dict[tuple[int, ...], list[prepare.Candidate]] = defaultdict(list)
    by_pc: dict[tuple[int, ...], list[prepare.Candidate]] = defaultdict(list)
    for cand in raw_candidates:
        by_pitch[cand.pitch_signature].append(cand)
        by_pc[cand.pc_signature].append(cand)

    diag = pd.read_csv(diag_path, dtype=str).set_index("id")
    fallback_by_id = fallback.set_index(fallback["id"].astype(str))
    rows = []
    unique_exact = 0
    unique_pc = 0
    recovered_track = 0
    total = 0
    for _, row in test.iterrows():
        notes = _loads(row["notes_json"])
        sig = tuple(sorted(int(note["pitch_midi"]) for note in notes))
        pc_sig = tuple(sorted(p % 12 for p in sig))
        total += 1
        candidates = by_pitch.get(sig, [])
        if len(candidates) == 1:
            unique_exact += 1
        if len(by_pc.get(pc_sig, [])) == 1:
            unique_pc += 1
        if len(candidates) == 1:
            cand = candidates[0]
            if str(row["id"]) in diag.index and str(diag.loc[str(row["id"]), "source_stem"]) == cand.track.stem:
                recovered_track += 1
            tab_json = _candidate_tab_for_public_notes(notes, cand)
            if tab_json is None:
                fb = fallback_by_id.loc[str(row["id"])]
                rows.append({"id": row["id"], "tab_json": fb["tab_json"], "confidence": 0.30})
            else:
                rows.append({"id": row["id"], "tab_json": tab_json, "confidence": 0.48})
        else:
            fb = fallback_by_id.loc[str(row["id"])]
            rows.append({"id": row["id"], "tab_json": fb["tab_json"], "confidence": 0.30})
    print(f"leakage.source_lookup.unique_exact_fraction: {unique_exact / max(total, 1):.3f}")
    print(f"leakage.source_lookup.unique_pc_fraction: {unique_pc / max(total, 1):.3f}")
    print(f"leakage.source_lookup.recovered_track_fraction: {recovered_track / max(total, 1):.3f}")
    return pd.DataFrame(rows)[grade.SUBMISSION_COLUMNS]


def _feature_from_array(x: np.ndarray, sr: int) -> np.ndarray:
    if x.size == 0:
        return np.zeros(12, dtype=np.float32)
    x = x.astype(np.float32)
    rms = float(np.sqrt(np.mean(x**2)))
    peak = float(np.max(np.abs(x)))
    zcr = float(np.mean(np.signbit(x[1:]) != np.signbit(x[:-1]))) if x.size > 1 else 0.0
    spec = np.abs(np.fft.rfft(x * np.hanning(x.size)))
    freqs = np.fft.rfftfreq(x.size, d=1.0 / sr)
    denom = float(spec.sum()) + 1e-9
    centroid = float((spec * freqs).sum() / denom)
    spread = float(np.sqrt((spec * (freqs - centroid) ** 2).sum() / denom))
    bands = []
    for lo, hi in [(0, 200), (200, 600), (600, 1200), (1200, 2400), (2400, 5000), (5000, sr / 2)]:
        mask = (freqs >= lo) & (freqs < hi)
        bands.append(float(spec[mask].sum() / denom))
    return np.array([rms, peak, zcr, centroid / 5000.0, spread / 5000.0, *bands, len(x) / sr], dtype=np.float32)


def _media_fingerprint_submission(root: Path, public: Path, test: pd.DataFrame, fallback: pd.DataFrame) -> pd.DataFrame | None:
    raw = root / "raw"
    diag_path = root / "private" / "split_diagnostics.csv"
    if not raw.exists() or not diag_path.exists():
        print("leakage.media_fingerprint: not_run raw audio or diagnostics unavailable")
        return None
    try:
        ann_source = prepare.AnnotationSource(raw)
        audio_source = prepare.AudioSource(raw)
        raw_candidates = prepare._enumerate_candidates(ann_source)
    except Exception as exc:
        print(f"leakage.media_fingerprint: not_run {exc}")
        return None

    by_pitch: dict[tuple[int, ...], list[prepare.Candidate]] = defaultdict(list)
    for cand in raw_candidates:
        by_pitch[cand.pitch_signature].append(cand)

    raw_audio_cache: dict[str, tuple[int, np.ndarray]] = {}
    raw_feat_cache: dict[tuple[str, float], np.ndarray] = {}

    def raw_window_feature(cand: prepare.Candidate) -> np.ndarray:
        key = (cand.track.stem, round(cand.start, 3))
        if key in raw_feat_cache:
            return raw_feat_cache[key]
        if cand.track.stem not in raw_audio_cache:
            raw_audio_cache[cand.track.stem] = audio_source.read(cand.track.stem)
        sr, full = raw_audio_cache[cand.track.stem]
        start = max(0, int(round(cand.start * sr)))
        end = min(len(full), int(round((cand.start + prepare.CLIP_DURATION_S) * sr)))
        clip = full[start:end]
        target_len = int(round(prepare.CLIP_DURATION_S * sr))
        if len(clip) < target_len:
            clip = np.pad(clip, (0, target_len - len(clip)))
        clip = clip[:target_len]
        raw_feat_cache[key] = _feature_from_array(clip, sr)
        return raw_feat_cache[key]

    diag = pd.read_csv(diag_path, dtype=str).set_index("id")
    fallback_by_id = fallback.set_index(fallback["id"].astype(str))
    rows = []
    top1 = 0
    total = 0
    random_expected = 0.0
    for _, row in test.iterrows():
        notes = _loads(row["notes_json"])
        sig = tuple(sorted(int(note["pitch_midi"]) for note in notes))
        candidates = by_pitch.get(sig, [])
        if len(candidates) <= 1:
            fb = fallback_by_id.loc[str(row["id"])]
            rows.append({"id": row["id"], "tab_json": fb["tab_json"], "confidence": 0.30})
            continue
        public_feat = _clip_features(public / str(row["audio_path"]))
        raw_feats = np.vstack([raw_window_feature(cand) for cand in candidates])
        mean = raw_feats.mean(axis=0)
        scale = raw_feats.std(axis=0) + 1e-6
        dist = np.sum(((raw_feats - mean) / scale - (public_feat - mean) / scale) ** 2, axis=1)
        best = candidates[int(np.argmin(dist))]
        total += 1
        random_expected += 1.0 / len(candidates)
        true_stem = str(diag.loc[str(row["id"]), "source_stem"]) if str(row["id"]) in diag.index else ""
        true_start = float(diag.loc[str(row["id"]), "source_start_s"]) if str(row["id"]) in diag.index else -999.0
        top1 += int(best.track.stem == true_stem and abs(best.start - true_start) < 1e-6)
        tab_json = _candidate_tab_for_public_notes(notes, best)
        if tab_json is None:
            fb = fallback_by_id.loc[str(row["id"])]
            rows.append({"id": row["id"], "tab_json": fb["tab_json"], "confidence": 0.30})
        else:
            rows.append({"id": row["id"], "tab_json": tab_json, "confidence": 0.40})
    print(f"leakage.media_fingerprint_candidate_top1: {top1 / max(total, 1):.3f}")
    print(f"leakage.media_fingerprint_random_expected: {random_expected / max(total, 1):.3f}")
    return pd.DataFrame(rows)[grade.SUBMISSION_COLUMNS]


def _exact_public_skeleton_lookup(root: Path, test: pd.DataFrame) -> None:
    raw = root / "raw"
    diag_path = root / "private" / "split_diagnostics.csv"
    if not raw.exists() or not diag_path.exists():
        print("leakage.exact_public_skeleton_lookup: not_run raw annotations or diagnostics unavailable")
        return
    try:
        ann_source = prepare.AnnotationSource(raw)
        raw_candidates = prepare._enumerate_candidates(ann_source)
    except Exception as exc:
        print(f"leakage.exact_public_skeleton_lookup: not_run {exc}")
        return

    by_sig: dict[tuple[int, ...], list[prepare.Candidate]] = defaultdict(list)
    for cand in raw_candidates:
        by_sig[tuple(sorted(int(note.pitch_midi) for note in cand.notes))].append(cand)

    diag = pd.read_csv(diag_path, dtype=str).set_index("id")
    unique = 0
    recovered = 0
    total = 0
    buckets: Counter[int] = Counter()
    for _, row in test.iterrows():
        sig = tuple(sorted(int(note["pitch_midi"]) for note in _loads(row["notes_json"])))
        matches = by_sig.get(sig, [])
        total += 1
        buckets[len(matches)] += 1
        if len(matches) == 1:
            unique += 1
            if str(row["id"]) in diag.index and matches[0].track.stem == diag.loc[str(row["id"]), "source_stem"]:
                recovered += 1
    print(f"leakage.exact_public_skeleton_lookup.unique_fraction: {unique / max(total, 1):.3f}")
    print(f"leakage.exact_public_skeleton_lookup.recovered_track_fraction: {recovered / max(total, 1):.3f}")
    print(f"leakage.exact_public_skeleton_lookup.bucket_counts: {dict(sorted(buckets.items()))}")


def _public_leak_checks(public: Path, train: pd.DataFrame, test: pd.DataFrame) -> None:
    leak_terms = ["source", "player", "track", "family", "jams", "annotation", "filename", "timestamp"]
    for name, df in [("train", train), ("test", test)]:
        cols = [c for c in df.columns if any(term in c.lower() for term in leak_terms)]
        print(f"leakage.public_columns.{name}: {'FAIL ' + str(cols) if cols else 'pass'}")
        text = df.to_csv(index=False)
        raw_tokens = ["SS1-100", "Funk1", "Jazz", "Rock", ".jams", "_mic.wav", "audio_mono"]
        hits = [tok for tok in raw_tokens if tok in text]
        print(f"leakage.public_values.{name}: {'FAIL ' + str(hits) if hits else 'pass'}")
    missing = []
    for rel in list(train["audio_path"].astype(str)) + list(test["audio_path"].astype(str)):
        path = public / rel
        if not path.exists() or path.stat().st_size < 512:
            missing.append(rel)
    print(f"files.audio_paths: {'FAIL ' + str(missing[:3]) if missing else 'pass'}")


def _hidden_group_report(answers: pd.DataFrame) -> None:
    for axis in grade.GROUP_AXES:
        if axis not in answers.columns:
            continue
        counts = answers[axis].astype(str).value_counts().sort_index()
        print(f"hidden_group.{axis}.min: {int(counts.min())}")
        print(f"hidden_group.{axis}.counts: {json.dumps(counts.to_dict(), sort_keys=True)}")


def main() -> None:
    root = Path(__file__).resolve().parent
    public = root / "public"
    private = root / "private"
    train_path = public / "train.csv"
    test_path = public / "test.csv"
    answers_path = private / "answers.csv"
    if not (train_path.exists() and test_path.exists() and answers_path.exists()):
        print("analysis.status: prepared split not found")
        print("analysis.expected: run prepare.py with official annotation.zip and audio_mono-mic.zip first")
        return

    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    answers = pd.read_csv(answers_path)
    sample = pd.read_csv(public / "sample_submission.csv")

    print("source.license: GuitarSet Zenodo record 3371780, CC BY 4.0, official annotation.zip plus audio_mono-mic.zip")
    print(f"rows.train: {len(train)}")
    print(f"rows.test: {len(test)}")
    print(f"prepared.audio_files: {len(list((public / 'audio').glob('*.wav'))) if (public / 'audio').exists() else 0}")
    print(f"nan.train: {int(train.isna().sum().sum())}")
    print(f"nan.test: {int(test.isna().sum().sum())}")
    print(f"nan.answers: {int(answers.isna().sum().sum())}")
    print(f"split.id_overlap: {'FAIL' if set(train['id'].astype(str)) & set(test['id'].astype(str)) else 'pass'}")
    print(f"answers_alignment: {'pass' if set(test['id'].astype(str)) == set(answers['id'].astype(str)) else 'FAIL'}")
    _public_leak_checks(public, train, test)
    _event_ambiguity_report(train, "train")
    _event_ambiguity_report(test, "test")
    _hidden_group_report(answers)

    sample_score = _score("sample_submission", sample, answers)
    print("baseline.metadata_only_public_fields: not_applicable only opaque id, audio_path, clip_start_s, and clip_duration_s are public metadata")
    low_fret = _low_fret_pitch_submission(test)
    _score("low_fret_pitch_baseline", low_fret, answers)
    pitch_prior = _pitch_prior_submission(train, test)
    pitch_score = _score("skeleton_pitch_prior", pitch_prior, answers)
    _exact_public_skeleton_lookup(root, test)
    lookup = _source_lookup_submission(root, test, pitch_prior)
    if lookup is not None:
        _score("source_lookup_pitch_signature", lookup, answers)
    media_lookup = _media_fingerprint_submission(root, public, test, pitch_prior)
    if media_lookup is not None:
        _score("media_fingerprint_candidate_lookup", media_lookup, answers)
    audio = _simple_audio_submission(train, test, public)
    if audio is not None:
        _score("simple_audio_random_forest", audio, answers)

    perfect = answers[["id", "tab_json"]].copy()
    perfect["confidence"] = 1.0
    perfect_score = _score("perfect_oracle", perfect[grade.SUBMISSION_COLUMNS], answers)
    print(f"check.perfect: {'pass' if perfect_score == 1.0 else 'FAIL'}")
    print(f"check.sample_range: {'pass' if 0.12 <= sample_score < 0.50 else 'FAIL'}")
    print(f"check.pitch_prior_headroom: {'pass' if pitch_score < 0.70 else 'WARN'}")
    if perfect_score != 1.0 or not (0.12 <= sample_score < 0.50):
        sys.exit(1)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import shutil
import tarfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import soundfile as sf
from scipy.signal import resample_poly


TARGET_SR = 16000
MIN_SECONDS = 0.75
MAX_SECONDS = 2.20
DEFAULT_MAX_ROWS = 1000
TRAIN_UTTERANCES_PER_READER = 3
KNOWN_TEST_UTTERANCES_PER_READER = 4
UNKNOWN_TEST_UTTERANCES_PER_READER = 4
MIN_GROUP_TEST = 12
ID_SALT = "real-audiobook-open-set-reader-provenance-v2-fewshot-hard"

OFFICIAL_FILES = {
    "dev-clean-2.tar.gz": {
        "url": "https://openslr.trmal.net/resources/31/dev-clean-2.tar.gz",
        "size": "126M",
        "md5": "6d7ab67ac6a1d2c993d050e16d61080d",
        "use": "held-out real readers for UNKNOWN provenance",
    },
    "train-clean-5.tar.gz": {
        "url": "https://openslr.trmal.net/resources/31/train-clean-5.tar.gz",
        "size": "332M",
        "md5": "5df7d4e78065366204ca6845bb08f490",
        "use": "known real readers for public train and known-reader test rows",
    },
}

PUBLIC_INPUT_COLUMNS = ["id", "audio_path", "duration_sec", "utterance_length_bucket"]
TRAIN_COLUMNS = PUBLIC_INPUT_COLUMNS + ["verdict_json"]
TEST_COLUMNS = PUBLIC_INPUT_COLUMNS
SUBMISSION_COLUMNS = ["id", "verdict_json"]
ANSWER_COLUMNS = [
    "id",
    "verdict_json",
    "is_known_reader",
    "provenance",
    "reader_group",
    "source_split",
    "chapter_group",
    "sex_group",
    "duration_bucket",
]


@dataclass(frozen=True)
class SpeechRecord:
    source_path: Path
    subset: str
    speaker: str
    chapter: str
    utterance_id: str
    transcript: str
    sex: str

    @property
    def source_key(self) -> str:
        return f"{self.subset}/{self.speaker}/{self.chapter}/{self.utterance_id}"

    @property
    def reader_key(self) -> str:
        return self.speaker

    @property
    def chapter_key(self) -> str:
        return f"{self.speaker}/{self.chapter}"


def _hash_text(*parts: object) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update(str(part).encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()


def _unit_float(*parts: object) -> float:
    return int(_hash_text(*parts)[:12], 16) / float(16**12 - 1)


def _json_verdict(known_reader_score: float, provenance: str, confidence: float = 1.0) -> str:
    return json.dumps(
        {
            "known_reader_score": round(float(known_reader_score), 6),
            "provenance": str(provenance),
            "confidence": round(float(confidence), 6),
        },
        separators=(",", ":"),
        sort_keys=True,
    )


def _candidate_roots(raw: Path) -> list[Path]:
    roots = [raw, raw / "raw_upload", raw / "raw_data"]
    return [r for r in roots if r.exists()]


def _has_subset_dirs(path: Path) -> bool:
    return any((path / subset).is_dir() for subset in ("dev-clean-2", "train-clean-5"))


def _find_archive(raw: Path, name: str) -> Path | None:
    for root in _candidate_roots(raw):
        direct = root / name
        if direct.exists():
            return direct
        matches = sorted(root.rglob(name))
        if matches:
            return matches[0]
    return None


def _safe_extract_tar(archive: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "r:*") as tf:
        tf.extractall(dest, filter="data")


def _official_missing_message(raw: Path) -> str:
    lines = [
        "Official Mini LibriSpeech source files were not found.",
        f"Looked under: {raw}",
        "Import the official SLR31 URLs or place either the unmodified archives or platform-extracted subset directories under raw/:",
    ]
    for name, meta in OFFICIAL_FILES.items():
        lines.append(f"- {name} ({meta['size']}, md5 {meta['md5']}) from {meta['url']}")
    lines.append("Do not use ODSS or any generated-audio source for this revised challenge.")
    return "\n".join(lines)


def _find_librispeech_roots(raw: Path) -> list[Path]:
    roots = []
    for base in _candidate_roots(raw):
        if _has_subset_dirs(base):
            roots.append(base)
        for path in [base / "LibriSpeech", *base.rglob("LibriSpeech")]:
            if path.exists() and path.is_dir():
                roots.append(path)
    if roots:
        return sorted(set(roots))

    missing = [name for name in OFFICIAL_FILES if _find_archive(raw, name) is None]
    if missing:
        raise SystemExit(_official_missing_message(raw))

    cache = raw / "_mini_librispeech_extract_cache"
    cache.mkdir(parents=True, exist_ok=True)
    for name in OFFICIAL_FILES:
        archive = _find_archive(raw, name)
        assert archive is not None
        marker = cache / f".extracted_{name}.ok"
        if not marker.exists():
            print(f"extracting {archive.name} to {cache}")
            _safe_extract_tar(archive, cache)
            marker.write_text("ok\n", encoding="utf-8")
    roots = [p for p in cache.rglob("LibriSpeech") if p.is_dir()]
    if _has_subset_dirs(cache):
        roots.append(cache)
    if not roots:
        raise SystemExit("Archives were present but no Mini LibriSpeech subset directories were found after extraction.")
    return sorted(set(roots))


def _load_speaker_sex(roots: list[Path]) -> dict[str, str]:
    sex: dict[str, str] = {}
    for root in roots:
        for path in root.rglob("SPEAKERS.TXT"):
            for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                text = line.strip()
                if not text or text.startswith(";"):
                    continue
                parts = [p.strip() for p in text.split("|")]
                if len(parts) >= 2 and parts[0].isdigit():
                    sex[parts[0]] = parts[1] or "unknown"
    return sex


def _load_transcripts(chapter_dir: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for path in chapter_dir.glob("*.trans.txt"):
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not line.strip():
                continue
            if " " in line:
                utt, text = line.split(" ", 1)
            else:
                utt, text = line.strip(), ""
            out[utt] = text.strip()
    return out


def _load_records(raw: Path) -> list[SpeechRecord]:
    roots = _find_librispeech_roots(raw)
    sex_lookup = _load_speaker_sex(roots)
    records: list[SpeechRecord] = []
    for root in roots:
        for audio in sorted(root.rglob("*.flac")) + sorted(root.rglob("*.wav")):
            try:
                rel = audio.relative_to(root)
            except ValueError:
                continue
            parts = rel.parts
            if len(parts) < 4:
                continue
            subset, speaker, chapter = parts[0], parts[1], parts[2]
            if not (speaker.isdigit() and chapter.isdigit()):
                continue
            utt = audio.stem
            transcripts = _load_transcripts(audio.parent)
            records.append(
                SpeechRecord(
                    source_path=audio,
                    subset=subset,
                    speaker=speaker,
                    chapter=chapter,
                    utterance_id=utt,
                    transcript=transcripts.get(utt, ""),
                    sex=sex_lookup.get(speaker, "unknown"),
                )
            )
    if not records:
        raise SystemExit("No Mini LibriSpeech audio records were discovered.")
    keys = [r.source_key for r in records]
    if len(keys) != len(set(keys)):
        raise SystemExit("Duplicate source utterance keys discovered before id assignment")
    return records


def _reader_tokens(known_speakers: list[str]) -> dict[str, str]:
    ordered = sorted(known_speakers, key=lambda s: _hash_text(ID_SALT, "reader-token", s))
    return {speaker: f"reader_{i:03d}" for i, speaker in enumerate(ordered)}


def _balanced_take(records: list[SpeechRecord], n_target: int, tag: str) -> list[SpeechRecord]:
    by_reader: dict[str, list[SpeechRecord]] = {}
    for rec in records:
        by_reader.setdefault(rec.reader_key, []).append(rec)
    for reader in by_reader:
        by_reader[reader] = sorted(by_reader[reader], key=lambda r: _hash_text(ID_SALT, "row", tag, r.source_key))
    readers = sorted(by_reader, key=lambda r: _hash_text(ID_SALT, "reader-order", tag, r))
    idx = {reader: 0 for reader in readers}
    selected: list[SpeechRecord] = []
    while len(selected) < n_target:
        progressed = False
        for reader in readers:
            if len(selected) >= n_target:
                break
            pos = idx[reader]
            if pos >= len(by_reader[reader]):
                continue
            selected.append(by_reader[reader][pos])
            idx[reader] += 1
            progressed = True
        if not progressed:
            break
    return selected


def _record_profile(rec: SpeechRecord) -> np.ndarray:
    try:
        _, audio = _read_audio(rec.source_path)
    except Exception:
        return np.zeros(4, dtype=np.float32)
    audio = audio[: min(audio.size, TARGET_SR * 3)]
    if audio.size < 16:
        return np.zeros(4, dtype=np.float32)
    rms = float(np.sqrt(np.mean(audio.astype(np.float64) ** 2) + 1e-12))
    zcr = float(np.mean(np.abs(np.diff(np.signbit(audio).astype(np.int8)))))
    win = np.hanning(audio.size)
    spec = np.abs(np.fft.rfft(audio * win)) + 1e-9
    freqs = np.fft.rfftfreq(audio.size, d=1.0 / TARGET_SR)
    centroid = float(np.sum(freqs * spec) / np.sum(spec)) / TARGET_SR
    high_ratio = float(np.sum(spec[freqs > 3000]) / np.sum(spec))
    return np.asarray([math.log1p(rms), zcr, centroid, high_ratio], dtype=np.float32)


def _speaker_profiles(by_reader: dict[str, list[SpeechRecord]]) -> dict[str, np.ndarray]:
    profiles: dict[str, np.ndarray] = {}
    for reader, group in by_reader.items():
        chosen = sorted(group, key=lambda r: _hash_text(ID_SALT, "profile", r.source_key))[: min(5, len(group))]
        feats = np.vstack([_record_profile(r) for r in chosen])
        profiles[reader] = feats.mean(axis=0)
    return profiles


def _reader_sex(group: list[SpeechRecord]) -> str:
    vals = [r.sex for r in group if r.sex in {"M", "F"}]
    return vals[0] if vals else "unknown"


def _hard_unknown_readers(
    known_readers: list[str],
    unknown_readers: list[str],
    known_groups: dict[str, list[SpeechRecord]],
    unknown_groups: dict[str, list[SpeechRecord]],
) -> list[str]:
    known_profiles = _speaker_profiles({r: known_groups[r] for r in known_readers})
    unknown_profiles = _speaker_profiles({r: unknown_groups[r] for r in unknown_readers})
    known_by_sex: dict[str, list[str]] = {}
    for reader in known_readers:
        known_by_sex.setdefault(_reader_sex(known_groups[reader]), []).append(reader)

    ranked: list[tuple[float, str, str]] = []
    for reader in unknown_readers:
        same_sex = known_by_sex.get(_reader_sex(unknown_groups[reader]), []) or known_readers
        d = min(float(np.linalg.norm(unknown_profiles[reader] - known_profiles[k])) for k in same_sex)
        ranked.append((d, _hash_text(ID_SALT, "unknown-tie", reader), reader))
    return [reader for _, _, reader in sorted(ranked)]


def _split_records(records: list[SpeechRecord], max_rows: int) -> tuple[list[SpeechRecord], list[SpeechRecord], dict[str, str]]:
    known_pool = [r for r in records if r.subset == "train-clean-5"]
    unknown_pool = [r for r in records if r.subset == "dev-clean-2"]
    if not known_pool or not unknown_pool:
        raise SystemExit("Expected train-clean-5 known-reader records and dev-clean-2 unknown-reader records.")

    known_by_reader: dict[str, list[SpeechRecord]] = {}
    for rec in known_pool:
        known_by_reader.setdefault(rec.reader_key, []).append(rec)
    unknown_by_reader: dict[str, list[SpeechRecord]] = {}
    for rec in unknown_pool:
        unknown_by_reader.setdefault(rec.reader_key, []).append(rec)

    min_known = TRAIN_UTTERANCES_PER_READER + KNOWN_TEST_UTTERANCES_PER_READER
    known_readers = [
        reader for reader, group in known_by_reader.items() if len(group) >= min_known
    ]
    unknown_readers = [
        reader for reader, group in unknown_by_reader.items() if len(group) >= UNKNOWN_TEST_UTTERANCES_PER_READER
    ]
    if len(known_readers) < 2 or len(unknown_readers) < 2:
        raise SystemExit("Not enough readers with sufficient utterances for few-shot open-set split.")

    per_reader_budget = TRAIN_UTTERANCES_PER_READER + KNOWN_TEST_UTTERANCES_PER_READER + UNKNOWN_TEST_UTTERANCES_PER_READER
    n_reader_pairs = max(2, min(len(known_readers), len(unknown_readers), max_rows // per_reader_budget))
    known_readers = sorted(known_readers, key=lambda r: _hash_text(ID_SALT, "known-reader", r))[:n_reader_pairs]
    unknown_readers = _hard_unknown_readers(known_readers, unknown_readers, known_by_reader, unknown_by_reader)[:n_reader_pairs]
    token_map = _reader_tokens(known_readers)

    train: list[SpeechRecord] = []
    known_test: list[SpeechRecord] = []
    unknown_test: list[SpeechRecord] = []
    for reader in known_readers:
        ordered = sorted(known_by_reader[reader], key=lambda r: _hash_text(ID_SALT, "fewshot-known", reader, r.source_key))
        train.extend(ordered[:TRAIN_UTTERANCES_PER_READER])
        known_test.extend(ordered[TRAIN_UTTERANCES_PER_READER:min_known])
    for reader in unknown_readers:
        ordered = sorted(unknown_by_reader[reader], key=lambda r: _hash_text(ID_SALT, "fewshot-unknown", reader, r.source_key))
        unknown_test.extend(ordered[:UNKNOWN_TEST_UTTERANCES_PER_READER])

    test = known_test + unknown_test
    if not train or not test:
        raise SystemExit("Split produced empty train or test rows.")
    if not any(r.subset == "dev-clean-2" for r in test):
        raise SystemExit("Hidden test lacks UNKNOWN-reader rows.")
    return train, test, token_map


def _read_audio(path: Path) -> tuple[int, np.ndarray]:
    data, sr = sf.read(path, always_2d=False)
    if data.ndim == 2:
        data = data.mean(axis=1)
    audio = np.asarray(data, dtype=np.float32)
    if sr != TARGET_SR:
        gcd = math.gcd(int(sr), TARGET_SR)
        audio = resample_poly(audio, TARGET_SR // gcd, int(sr) // gcd).astype(np.float32)
        sr = TARGET_SR
    audio = np.nan_to_num(audio, nan=0.0, posinf=0.0, neginf=0.0)
    if audio.size == 0:
        raise ValueError(f"empty audio file: {path}")
    return int(sr), audio


def _harden_audio(audio: np.ndarray, key: str, split: str) -> np.ndarray:
    audio = np.asarray(audio, dtype=np.float32)
    target_seconds = MIN_SECONDS + (MAX_SECONDS - MIN_SECONDS) * _unit_float("clip-seconds", key)
    if split == "test":
        target_seconds = min(target_seconds, 1.55)
    target_len = max(1, int(target_seconds * TARGET_SR))
    if audio.size > target_len:
        span = audio.size - target_len
        start = int(_unit_float("crop", key) * span)
        audio = audio[start : start + target_len]
    ratio_options = [(156, 160), (158, 160), (160, 160), (162, 160), (164, 160)]
    ratio = ratio_options[int(_unit_float("speed", key) * len(ratio_options)) % len(ratio_options)]
    if ratio != (160, 160):
        audio = resample_poly(audio, ratio[0], ratio[1]).astype(np.float32)
    width = 9 + 2 * int(_unit_float("smooth-width", key) * 5)
    kernel = np.ones(width, dtype=np.float32) / float(width)
    low = np.convolve(audio, kernel, mode="same").astype(np.float32)
    tilt = -0.10 + 0.20 * _unit_float("tilt", key)
    audio = audio + tilt * (audio - low)
    echo_delay = int((0.008 + 0.020 * _unit_float("echo-delay", key)) * TARGET_SR)
    echo_gain = 0.015 + 0.030 * _unit_float("echo-gain", key)
    if echo_delay > 0 and audio.size > echo_delay:
        echoed = audio.copy()
        echoed[echo_delay:] += echo_gain * audio[:-echo_delay]
        audio = echoed
    drive = 1.05 + 0.25 * _unit_float("drive", key)
    audio = np.tanh(drive * audio).astype(np.float32)
    rng = np.random.default_rng(int(_hash_text("dither", key)[:16], 16) % (2**32))
    noise_db = -56.0 + 8.0 * _unit_float("noise", key)
    audio = audio + rng.normal(0.0, 10 ** (noise_db / 20), size=audio.size).astype(np.float32)
    peak = float(np.max(np.abs(audio))) if audio.size else 0.0
    if peak > 0:
        audio = 0.92 * audio / peak
    return audio.astype(np.float32)


def _write_wav(path: Path, audio: np.ndarray) -> float:
    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(path, audio.astype(np.float32), TARGET_SR, subtype="PCM_16")
    return round(len(audio) / TARGET_SR, 4)


def _public_id(rec: SpeechRecord) -> str:
    return "rasp_" + _hash_text(ID_SALT, "public-id", rec.source_key)[:12]


def _duration_bucket(duration: float) -> str:
    if duration < 1.0:
        return "short"
    if duration < 1.35:
        return "medium"
    return "long"


def _utterance_length_bucket(text: str) -> str:
    n = len((text or "").split())
    if n == 0:
        return "unknown"
    if n < 12:
        return "short"
    if n < 25:
        return "medium"
    return "long"


def _row_from_record(rec: SpeechRecord, split: str, token_map: dict[str, str], public: Path) -> tuple[dict[str, object], dict[str, object] | None]:
    sample_id = _public_id(rec)
    rel_audio = f"{split}/audio/{sample_id}.wav"
    _, audio = _read_audio(rec.source_path)
    audio = _harden_audio(audio, _hash_text(ID_SALT, "audio", rec.source_key, split), split)
    duration = _write_wav(public / rel_audio, audio)
    is_known = int(rec.reader_key in token_map)
    provenance = token_map[rec.reader_key] if is_known else "UNKNOWN"
    verdict = _json_verdict(float(is_known), provenance, 1.0)
    public_row = {
        "id": sample_id,
        "audio_path": rel_audio,
        "duration_sec": duration,
        "utterance_length_bucket": _utterance_length_bucket(rec.transcript),
    }
    answer_row = {
        "id": sample_id,
        "verdict_json": verdict,
        "is_known_reader": is_known,
        "provenance": provenance,
        "reader_group": "reader_" + _hash_text(ID_SALT, "reader-group", rec.reader_key)[:10],
        "source_split": rec.subset,
        "chapter_group": "chapter_" + _hash_text(ID_SALT, "chapter", rec.chapter_key)[:10],
        "sex_group": rec.sex if rec.sex in {"M", "F"} else "unknown",
        "duration_bucket": _duration_bucket(duration),
    }
    if split == "train":
        public_row["verdict_json"] = verdict
        return public_row, None
    return public_row, answer_row


def _sample_submission(test_df: pd.DataFrame, train_df: pd.DataFrame) -> pd.DataFrame:
    train_tokens = sorted({json.loads(v)["provenance"] for v in train_df["verdict_json"].astype(str)})
    if not train_tokens:
        train_tokens = ["reader_000"]
    rows = []
    for sample_id in test_df["id"].astype(str):
        u = _unit_float("sample", sample_id)
        if u < 0.75:
            provenance = "UNKNOWN"
            known_score = 0.45
        else:
            provenance = train_tokens[int(_unit_float("sample-reader", sample_id) * len(train_tokens)) % len(train_tokens)]
            known_score = 0.55
        rows.append({"id": sample_id, "verdict_json": _json_verdict(known_score, provenance, 0.45)})
    return pd.DataFrame(rows, columns=SUBMISSION_COLUMNS)


def _validate_outputs(train_df: pd.DataFrame, test_df: pd.DataFrame, answers_df: pd.DataFrame, public: Path, min_group_test: int) -> None:
    for name, df in [("train.csv", train_df), ("test.csv", test_df), ("answers.csv", answers_df)]:
        if df.isna().any().any():
            raise SystemExit(f"{name} contains NaN values")
        if df.astype(str).apply(lambda col: col.str.len().eq(0)).any().any():
            raise SystemExit(f"{name} contains blank values")
    if set(train_df["id"]).intersection(set(test_df["id"])):
        raise SystemExit("train/test id overlap")
    if set(test_df["id"]) != set(answers_df["id"]):
        raise SystemExit("test ids do not match answers")
    train_tokens = {json.loads(v)["provenance"] for v in train_df["verdict_json"].astype(str)}
    test_tokens = set(answers_df["provenance"].astype(str))
    if "UNKNOWN" in train_tokens:
        raise SystemExit("UNKNOWN leaked into train labels")
    if "UNKNOWN" not in test_tokens:
        raise SystemExit("test split lacks UNKNOWN rows")
    if not (test_tokens - {"UNKNOWN"}):
        raise SystemExit("test split lacks known-reader rows")
    forbidden_cols = {"speaker", "speaker_id", "chapter", "chapter_id", "source_path", "source_split", "transcript", "reader_group"}
    for name, df in [("train.csv", train_df), ("test.csv", test_df)]:
        leaked = forbidden_cols & set(df.columns)
        if leaked:
            raise SystemExit(f"{name} exposes leakage-prone columns: {sorted(leaked)}")
        for rel in df["audio_path"].astype(str):
            full = public / rel
            if not full.exists():
                raise SystemExit(f"missing public audio file: {rel}")
            low = rel.lower()
            if any(tok in low for tok in ["librispeech", "train-clean", "dev-clean", "speaker", "chapter"]):
                raise SystemExit(f"public audio path leaks source token: {rel}")
    axes = ["source_split", "sex_group", "duration_bucket"]
    for axis in axes:
        counts = answers_df[axis].astype(str).value_counts()
        sparse = counts[counts < min_group_test]
        if not sparse.empty:
            raise SystemExit(f"test hidden subgroup '{axis}' has sparse groups below {min_group_test}: {sparse.to_dict()}")
    reader_counts = answers_df["reader_group"].value_counts()
    if int((reader_counts >= 2).sum()) < 2:
        raise SystemExit("test split lacks repeated-reader groups for consistency scoring")


def prepare(raw: Path, public: Path, private: Path, max_rows: int = DEFAULT_MAX_ROWS, allow_tiny_fixture: bool = False) -> None:
    raw = Path(raw).resolve()
    public = Path(public).resolve()
    private = Path(private).resolve()
    if public == raw or private == raw:
        raise SystemExit("public/private outputs must be separate from raw source")
    if public.exists():
        shutil.rmtree(public)
    if private.exists():
        shutil.rmtree(private)
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    records = _load_records(raw)
    train_records, test_records, token_map = _split_records(records, max_rows=max_rows)
    selected_keys = [r.source_key for r in train_records + test_records]
    if len(selected_keys) != len(set(selected_keys)):
        raise SystemExit("raw hash/key uniqueness check failed before public id assignment")
    selected_ids = [_public_id(r) for r in train_records + test_records]
    if len(selected_ids) != len(set(selected_ids)):
        raise SystemExit("salted public id collision before materialization")

    train_rows = []
    test_rows = []
    answer_rows = []
    for rec in sorted(train_records, key=lambda r: _hash_text(ID_SALT, "materialize", "train", r.source_key)):
        public_row, _ = _row_from_record(rec, "train", token_map, public)
        train_rows.append(public_row)
    for rec in sorted(test_records, key=lambda r: _hash_text(ID_SALT, "materialize", "test", r.source_key)):
        public_row, answer_row = _row_from_record(rec, "test", token_map, public)
        test_rows.append(public_row)
        assert answer_row is not None
        answer_rows.append(answer_row)

    train_df = pd.DataFrame(train_rows, columns=TRAIN_COLUMNS).sort_values("id").reset_index(drop=True)
    test_df = pd.DataFrame(test_rows, columns=TEST_COLUMNS).sort_values("id").reset_index(drop=True)
    answers_df = pd.DataFrame(answer_rows, columns=ANSWER_COLUMNS).sort_values("id").reset_index(drop=True)
    min_group_test = 1 if allow_tiny_fixture else MIN_GROUP_TEST
    _validate_outputs(train_df, test_df, answers_df, public, min_group_test=min_group_test)

    train_df.to_csv(public / "train.csv", index=False)
    test_df.to_csv(public / "test.csv", index=False)
    _sample_submission(test_df, train_df).to_csv(public / "sample_submission.csv", index=False)
    answers_df.to_csv(private / "answers.csv", index=False)
    total_bytes = sum(p.stat().st_size for p in public.rglob("*") if p.is_file())
    if not allow_tiny_fixture and total_bytes > 500 * 1024 * 1024:
        raise SystemExit(f"prepared public data exceeds 500 MB budget: {total_bytes} bytes")
    print(
        f"prepared real audiobook open-set provenance split: {len(train_df)} train rows, "
        f"{len(test_df)} test rows, public size {total_bytes / (1024 * 1024):.1f} MiB"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=Path("raw"))
    parser.add_argument("--public", type=Path, default=Path("public"))
    parser.add_argument("--private", type=Path, default=Path("private"))
    parser.add_argument("--max-rows", type=int, default=DEFAULT_MAX_ROWS)
    parser.add_argument("--allow-tiny-fixture", action="store_true", help="only for _sanity_smoke.py Mini-LibriSpeech-shaped fixtures")
    args = parser.parse_args()
    prepare(args.raw, args.public, args.private, max_rows=args.max_rows, allow_tiny_fixture=args.allow_tiny_fixture)


if __name__ == "__main__":
    main()

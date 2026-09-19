from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import wave
import zipfile
from collections import Counter, defaultdict, OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ANNOTATION_URL = "https://zenodo.org/api/records/3371780/files/annotation.zip/content"
AUDIO_URL = "https://zenodo.org/api/records/3371780/files/audio_mono-mic.zip/content"

ID_SALT = "audio-grounded-guitar-tab-recovery-v1"
SPLIT_TEST_PLAYERS = {"04", "05"}
MIN_GROUP_TEST = 10
MIN_TRAIN_ROWS = 100
MIN_TEST_ROWS = 80

TUNING_LOW_TO_HIGH = [40, 45, 50, 55, 59, 64]
OPEN_MIDI_BY_STRING = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}

CLIP_DURATION_S = 2.40
WINDOW_STEP_S = 0.55
WINDOW_EDGE_S = 0.08
MIN_EVENTS = 4
MAX_EVENTS = 8
MIN_AMBIGUOUS_FRACTION = 0.65
MAX_CLIPS_PER_TRACK = 16
MIN_NONOVERLAP_S = 1.20
MIN_EXACT_SIGNATURE_COUNT = 4
MIN_TAB_VARIANTS_PER_SIGNATURE = 2
TRAIN_COLUMNS = [
    "id",
    "audio_path",
    "notes_json",
    "clip_start_s",
    "clip_duration_s",
    "tab_json",
    "confidence_label",
]
TEST_COLUMNS = ["id", "audio_path", "notes_json", "clip_start_s", "clip_duration_s"]
ANSWER_COLUMNS = [
    "id",
    "tab_json",
    "notes_json",
    "player_group",
    "style_group",
    "polyphony_band",
    "ambiguity_band",
    "fret_range_band",
    "note_density_band",
]
SUBMISSION_COLUMNS = ["id", "tab_json", "confidence"]


@dataclass
class TrackMeta:
    stem: str
    annotation_member: str
    player: str
    family: str
    style: str
    tempo: str
    key: str
    take_type: str
    duration: float


@dataclass
class Note:
    time: float
    duration: float
    pitch_midi: int
    string: int
    fret: int


@dataclass
class Candidate:
    track: TrackMeta
    start: float
    notes: list[Note]
    scene_hash: str
    pc_signature: tuple[int, ...]
    pitch_signature: tuple[int, ...]
    max_polyphony: int
    ambiguous_fraction: float
    lookup_bucket: int = 1
    id: str = ""
    audio_path: str = ""
    split: str = ""
    hidden: dict[str, str] = field(default_factory=dict)


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _stable_rng(key: str) -> np.random.Generator:
    digest = hashlib.sha256(f"{ID_SALT}:rng:{key}".encode("utf-8")).digest()
    seed = int.from_bytes(digest[:8], "little")
    return np.random.default_rng(seed)


def _json_dumps_compact(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=True, separators=(",", ":"))


def _valid_positions(pitch_midi: int) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for string, open_midi in OPEN_MIDI_BY_STRING.items():
        fret = pitch_midi - open_midi
        if 0 <= fret <= 24:
            out.append((string, fret))
    return out


def _parse_track_name(member: str) -> dict[str, str]:
    stem = Path(member).stem
    match = re.match(r"(?P<player>\d{2})_(?P<body>.+)_(?P<take>comp|solo)$", stem)
    if match is None:
        raise ValueError(f"Unexpected GuitarSet annotation filename: {member}")
    body = match.group("body")
    parts = body.split("-")
    if len(parts) >= 3:
        family = "-".join(parts[:-2])
        tempo = parts[-2]
        key = parts[-1]
    else:
        family = body
        tempo = ""
        key = ""
    style_match = re.match(r"[A-Za-z]+", family)
    style = style_match.group(0) if style_match else family
    return {
        "stem": stem,
        "player": match.group("player"),
        "family": family,
        "style": style,
        "tempo": tempo,
        "key": key,
        "take_type": match.group("take"),
    }


def _find_zip_by_content(raw: Path, wanted: str) -> Path | None:
    preferred = raw / f"{wanted}.zip"
    if preferred.exists():
        return preferred
    for candidate in sorted(raw.rglob("*")):
        if not candidate.is_file():
            continue
        if candidate.suffix.lower() != ".zip" and "zip" not in candidate.name.lower():
            continue
        try:
            with zipfile.ZipFile(candidate) as zf:
                names = zf.namelist()
        except zipfile.BadZipFile:
            continue
        if wanted == "annotation" and any(name.lower().endswith(".jams") for name in names):
            return candidate
        if wanted == "audio_mono-mic" and any(name.lower().endswith(".wav") for name in names):
            return candidate
    return None


class AnnotationSource:
    def __init__(self, raw: Path) -> None:
        self.zip_path = _find_zip_by_content(raw, "annotation")
        self.root: Path | None = None
        if self.zip_path is None:
            matches = sorted(raw.rglob("*.jams"))
            if not matches:
                raise FileNotFoundError(
                    "No GuitarSet JAMS annotations found. Import annotation.zip from "
                    f"{ANNOTATION_URL}"
                )
            self.root = raw

    def members(self) -> list[str]:
        if self.zip_path is not None:
            with zipfile.ZipFile(self.zip_path) as zf:
                return sorted(name for name in zf.namelist() if name.lower().endswith(".jams"))
        assert self.root is not None
        return sorted(str(path.relative_to(self.root)) for path in self.root.rglob("*.jams"))

    def read_json(self, member: str) -> dict[str, Any]:
        if self.zip_path is not None:
            with zipfile.ZipFile(self.zip_path) as zf:
                with zf.open(member) as fh:
                    return json.loads(fh.read().decode("utf-8"))
        assert self.root is not None
        return json.loads((self.root / member).read_text(encoding="utf-8"))


def _normalise_audio_stem(path_name: str) -> str:
    stem = Path(path_name).stem
    for suffix in ["_mic", "_mono-mic", "_mono_mic", "-mic"]:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    return stem


class AudioSource:
    def __init__(self, raw: Path) -> None:
        self.zip_path = _find_zip_by_content(raw, "audio_mono-mic")
        self.root: Path | None = None
        self.index: dict[str, str | Path] = {}
        if self.zip_path is not None:
            with zipfile.ZipFile(self.zip_path) as zf:
                for name in zf.namelist():
                    if not name.lower().endswith(".wav"):
                        continue
                    safe_name = Path(name).name
                    norm = _normalise_audio_stem(safe_name)
                    self.index.setdefault(norm, name)
                    self.index.setdefault(Path(safe_name).stem, name)
        else:
            wavs = sorted(raw.rglob("*.wav"))
            if not wavs:
                raise FileNotFoundError(
                    "No GuitarSet mono-mic WAV files found. Import audio_mono-mic.zip from "
                    f"{AUDIO_URL}"
                )
            self.root = raw
            for path in wavs:
                safe_name = Path(path).name
                norm = _normalise_audio_stem(safe_name)
                self.index.setdefault(norm, path)
                self.index.setdefault(Path(safe_name).stem, path)

    def _resolve(self, stem: str) -> str | Path:
        if stem in self.index:
            return self.index[stem]
        for key, value in self.index.items():
            if key.startswith(stem) or stem.startswith(key) or stem in key:
                return value
        raise FileNotFoundError(f"No mono-mic audio file found for annotation stem {stem}")

    def read(self, stem: str) -> tuple[int, np.ndarray]:
        ref = self._resolve(stem)
        if self.zip_path is not None:
            with zipfile.ZipFile(self.zip_path) as zf:
                raw_bytes = zf.read(str(ref))
            return _read_wav_bytes(raw_bytes)
        return _read_wav_path(Path(ref))


def _read_wav_bytes(raw_bytes: bytes) -> tuple[int, np.ndarray]:
    try:
        from scipy.io import wavfile

        sr, arr = wavfile.read(io.BytesIO(raw_bytes))
        return int(sr), _to_mono_float(arr)
    except Exception:
        with wave.open(io.BytesIO(raw_bytes), "rb") as wf:
            sr = wf.getframerate()
            channels = wf.getnchannels()
            width = wf.getsampwidth()
            frames = wf.readframes(wf.getnframes())
        return sr, _pcm_bytes_to_float(frames, width, channels)


def _read_wav_path(path: Path) -> tuple[int, np.ndarray]:
    try:
        from scipy.io import wavfile

        sr, arr = wavfile.read(path)
        return int(sr), _to_mono_float(arr)
    except Exception:
        with wave.open(str(path), "rb") as wf:
            sr = wf.getframerate()
            channels = wf.getnchannels()
            width = wf.getsampwidth()
            frames = wf.readframes(wf.getnframes())
        return sr, _pcm_bytes_to_float(frames, width, channels)


def _pcm_bytes_to_float(frames: bytes, width: int, channels: int) -> np.ndarray:
    if width == 1:
        arr = (np.frombuffer(frames, dtype=np.uint8).astype(np.float32) - 128.0) / 128.0
    elif width == 2:
        arr = np.frombuffer(frames, dtype="<i2").astype(np.float32) / 32768.0
    elif width == 3:
        raw = np.frombuffer(frames, dtype=np.uint8).reshape(-1, 3)
        vals = raw[:, 0].astype(np.int32) | (raw[:, 1].astype(np.int32) << 8) | (raw[:, 2].astype(np.int32) << 16)
        vals = np.where(vals & 0x800000, vals - 0x1000000, vals)
        arr = vals.astype(np.float32) / 8388608.0
    else:
        arr = np.frombuffer(frames, dtype="<i4").astype(np.float32) / 2147483648.0
    if channels > 1:
        arr = arr.reshape(-1, channels).mean(axis=1)
    return arr.astype(np.float32)


def _to_mono_float(arr: np.ndarray) -> np.ndarray:
    x = np.asarray(arr)
    if x.ndim == 2:
        x = x.mean(axis=1)
    if np.issubdtype(x.dtype, np.integer):
        info = np.iinfo(x.dtype)
        scale = max(abs(info.min), abs(info.max))
        x = x.astype(np.float32) / float(scale)
    else:
        x = x.astype(np.float32)
    return np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0).astype(np.float32)


def _write_wav(path: Path, sr: int, samples: np.ndarray) -> None:
    y = np.clip(samples, -1.0, 1.0)
    pcm = (y * 32767.0).astype("<i2")
    try:
        from scipy.io import wavfile

        wavfile.write(path, sr, pcm)
    except Exception:
        with wave.open(str(path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(pcm.tobytes())


def _extract_notes(track_json: dict[str, Any]) -> list[Note]:
    notes: list[Note] = []
    for ann in track_json.get("annotations", []):
        if ann.get("namespace") != "note_midi":
            continue
        source = ann.get("annotation_metadata", {}).get("data_source")
        try:
            source_idx = int(source)
        except Exception:
            continue
        if not (0 <= source_idx < 6):
            continue
        string = 6 - source_idx
        open_midi = TUNING_LOW_TO_HIGH[source_idx]
        for item in ann.get("data", []):
            try:
                onset = float(item["time"])
                duration = float(item["duration"])
                pitch = int(round(float(item["value"])))
            except Exception:
                continue
            fret = pitch - open_midi
            if duration <= 0.03:
                continue
            if 0 <= fret <= 24:
                notes.append(Note(onset, duration, pitch, string, fret))
    notes.sort(key=lambda n: (n.time, n.string, n.fret))
    return notes


def _onset_groups(notes: list[Note], start: float) -> list[list[int]]:
    groups: list[list[int]] = []
    group_times: list[float] = []
    for idx, note in enumerate(notes):
        rel = note.time - start
        if not group_times or abs(rel - group_times[-1]) > 0.055:
            groups.append([idx])
            group_times.append(rel)
        else:
            groups[-1].append(idx)
    return groups


def _candidate_from_window(track: TrackMeta, start: float, notes: list[Note]) -> Candidate | None:
    window_notes = [
        note
        for note in notes
        if start + WINDOW_EDGE_S <= note.time <= start + CLIP_DURATION_S - WINDOW_EDGE_S
    ]
    if not (MIN_EVENTS <= len(window_notes) <= MAX_EVENTS):
        return None

    notes_by_pitch: dict[int, Note] = {}
    for note in window_notes:
        existing = notes_by_pitch.get(note.pitch_midi)
        if existing is not None and (existing.string, existing.fret) != (note.string, note.fret):
            return None
        notes_by_pitch.setdefault(note.pitch_midi, note)
    target_notes = sorted(notes_by_pitch.values(), key=lambda n: (n.pitch_midi, n.string, n.fret))
    if not (MIN_EVENTS <= len(target_notes) <= MAX_EVENTS):
        return None

    ambiguous = [len(_valid_positions(note.pitch_midi)) >= 2 for note in target_notes]
    ambiguous_fraction = float(np.mean(ambiguous))
    if ambiguous_fraction < MIN_AMBIGUOUS_FRACTION:
        return None
    groups = _onset_groups(window_notes, start)
    max_polyphony = max((len(group) for group in groups), default=1)
    pitch_signature = tuple(note.pitch_midi for note in target_notes)
    pc_signature = tuple(sorted(note.pitch_midi % 12 for note in target_notes))
    scene_hash = _sha256_text(
        f"{track.stem}|{start:.3f}|{','.join(map(str, pitch_signature))}|"
        f"{','.join(f'{n.pitch_midi}:{n.string}:{n.fret}' for n in target_notes)}"
    )
    return Candidate(
        track=track,
        start=float(start),
        notes=target_notes,
        scene_hash=scene_hash,
        pc_signature=pc_signature,
        pitch_signature=pitch_signature,
        max_polyphony=max_polyphony,
        ambiguous_fraction=ambiguous_fraction,
    )


def _enumerate_candidates(annotation_source: AnnotationSource) -> list[Candidate]:
    candidates: list[Candidate] = []
    for member in annotation_source.members():
        meta_bits = _parse_track_name(member)
        data = annotation_source.read_json(member)
        duration = float(data.get("file_metadata", {}).get("duration") or 0.0)
        track = TrackMeta(
            stem=meta_bits["stem"],
            annotation_member=member,
            player=meta_bits["player"],
            family=meta_bits["family"],
            style=meta_bits["style"],
            tempo=meta_bits["tempo"],
            key=meta_bits["key"],
            take_type=meta_bits["take_type"],
            duration=duration,
        )
        notes = _extract_notes(data)
        start = 0.0
        while start + CLIP_DURATION_S <= duration:
            cand = _candidate_from_window(track, start, notes)
            if cand is not None:
                candidates.append(cand)
            start += WINDOW_STEP_S
    return candidates


def _load_candidates(annotation_source: AnnotationSource) -> list[Candidate]:
    candidates = _enumerate_candidates(annotation_source)
    pitch_counts = Counter(c.pitch_signature for c in candidates)
    tab_variants: dict[tuple[int, ...], Counter] = defaultdict(Counter)
    for cand in candidates:
        tab_signature = tuple((note.pitch_midi, note.string, note.fret) for note in cand.notes)
        tab_variants[cand.pitch_signature][tab_signature] += 1
    for cand in candidates:
        cand.lookup_bucket = pitch_counts[cand.pitch_signature]

    candidates = [
        cand
        for cand in candidates
        if pitch_counts[cand.pitch_signature] >= MIN_EXACT_SIGNATURE_COUNT
        and len(tab_variants[cand.pitch_signature]) >= MIN_TAB_VARIANTS_PER_SIGNATURE
    ]

    by_track: dict[str, list[Candidate]] = defaultdict(list)
    for cand in candidates:
        by_track[cand.track.stem].append(cand)

    selected: list[Candidate] = []
    for track_stem, items in by_track.items():
        ranked = sorted(
            items,
            key=lambda c: (
                -(1 if c.lookup_bucket >= 2 else 0),
                -len(tab_variants[c.pitch_signature]),
                -c.ambiguous_fraction,
                -min(c.max_polyphony, 3),
                -len(c.notes),
                _sha256_text(f"{ID_SALT}:rank:{track_stem}:{c.start:.3f}"),
            ),
        )
        chosen: list[Candidate] = []
        for cand in ranked:
            if len(chosen) >= MAX_CLIPS_PER_TRACK:
                break
            if all(abs(cand.start - other.start) >= MIN_NONOVERLAP_S for other in chosen):
                chosen.append(cand)
        selected.extend(chosen)

    if not selected:
        raise SystemExit("No suitable GuitarSet windows found after ambiguity filtering.")
    return selected


def _hashed_id_map(scene_hashes: list[str]) -> dict[str, str]:
    assert len(set(scene_hashes)) == len(scene_hashes), "scene_hash values must be unique before id mapping"
    hashed = [(_sha256_text(f"{ID_SALT}:id:{scene_hash}"), scene_hash) for scene_hash in scene_hashes]
    assert len({digest for digest, _ in hashed}) == len(hashed), "hashed id digests must be unique"
    id_map = {scene_hash: f"gt_{digest[:16]}" for digest, scene_hash in sorted(hashed)}
    return id_map


def _event_payloads(cand: Candidate) -> tuple[str, str]:
    notes_json = []
    tab_json = []
    ordered_notes = sorted(
        cand.notes,
        key=lambda note: (
            _sha256_text(f"{ID_SALT}:event-order:{cand.scene_hash}:{note.pitch_midi}:{note.string}:{note.fret}"),
            note.pitch_midi,
        ),
    )
    for note in ordered_notes:
        event_id = "n_" + _sha256_text(
            f"{ID_SALT}:event-id:{cand.scene_hash}:{note.pitch_midi}:{note.string}:{note.fret}"
        )[:10]
        notes_json.append(
            OrderedDict(
                [
                    ("event_id", event_id),
                    ("pitch_midi", int(note.pitch_midi)),
                ]
            )
        )
        tab_json.append(OrderedDict([("event_id", event_id), ("string", int(note.string)), ("fret", int(note.fret))]))
    return _json_dumps_compact(notes_json), _json_dumps_compact(tab_json)


def _polyphony_band(max_polyphony: int) -> str:
    if max_polyphony <= 1:
        return "single_only"
    if max_polyphony == 2:
        return "dyads"
    return "triads_plus"


def _ambiguity_band(cand: Candidate) -> str:
    mean_positions = float(np.mean([len(_valid_positions(note.pitch_midi)) for note in cand.notes]))
    if mean_positions >= 4.0:
        return "very_high"
    if mean_positions >= 3.0:
        return "high"
    return "medium"


def _fret_range_band(cand: Candidate) -> str:
    frets = [note.fret for note in cand.notes]
    mean_fret = float(np.mean(frets))
    if mean_fret <= 4.0:
        return "low_fret"
    if mean_fret <= 8.5:
        return "mid_fret"
    return "upper_fret"


def _density_band(cand: Candidate) -> str:
    event_count = len(cand.notes)
    if event_count <= 4:
        return "sparse"
    if event_count <= 5:
        return "medium"
    return "dense"


def _assign_hidden_groups(candidates: list[Candidate]) -> None:
    for cand in candidates:
        cand.hidden = {
            "player_group": f"player_{cand.track.player}",
            "style_group": cand.track.style,
            "take_type": cand.track.take_type,
            "polyphony_band": _polyphony_band(cand.max_polyphony),
            "ambiguity_band": _ambiguity_band(cand),
            "fret_range_band": _fret_range_band(cand),
            "note_density_band": _density_band(cand),
        }


def _merge_sparse_test_groups(candidates: list[Candidate], axis: str) -> None:
    test_rows = [cand for cand in candidates if cand.split == "test"]
    counts = Counter(cand.hidden[axis] for cand in test_rows)
    if not counts:
        return
    rare = {label for label, count in counts.items() if count < MIN_GROUP_TEST}
    if not rare:
        return
    rare_total = sum(counts[label] for label in rare)
    majority = counts.most_common(1)[0][0]
    replacement = f"other_{axis}" if rare_total >= MIN_GROUP_TEST else majority
    for cand in test_rows:
        if cand.hidden[axis] in rare:
            cand.hidden[axis] = replacement
    repaired = Counter(cand.hidden[axis] for cand in test_rows)
    if min(repaired.values()) < MIN_GROUP_TEST:
        raise SystemExit(f"Hidden group axis {axis} still has sparse test groups: {dict(repaired)}")


def _assign_ids_and_splits(candidates: list[Candidate]) -> list[Candidate]:
    scene_hashes = [cand.scene_hash for cand in candidates]
    id_map = _hashed_id_map(scene_hashes)
    for cand in candidates:
        cand.id = id_map[cand.scene_hash]
        cand.audio_path = f"audio/{cand.id}.wav"
        cand.split = "test" if cand.track.player in SPLIT_TEST_PLAYERS else "train"
    _assign_hidden_groups(candidates)
    for axis in [
        "player_group",
        "style_group",
        "take_type",
        "polyphony_band",
        "ambiguity_band",
        "fret_range_band",
        "note_density_band",
    ]:
        _merge_sparse_test_groups(candidates, axis)
    train_count = sum(c.split == "train" for c in candidates)
    test_count = sum(c.split == "test" for c in candidates)
    if train_count < MIN_TRAIN_ROWS or test_count < MIN_TEST_ROWS:
        raise SystemExit(f"Prepared split too small: train={train_count} test={test_count}")
    return sorted(candidates, key=lambda c: c.id)


def _fallback_position_for_pitch(pitch_midi: int) -> tuple[int, int]:
    valid = _valid_positions(pitch_midi)
    if not valid:
        return 1, 0
    return sorted(valid, key=lambda sf: (sf[1], sf[0]))[0]


def _sample_tab(notes_json: str) -> str:
    notes = json.loads(notes_json)
    out = []
    for item in notes:
        string, fret = _fallback_position_for_pitch(int(item["pitch_midi"]))
        out.append(OrderedDict([("event_id", item["event_id"]), ("string", string), ("fret", fret)]))
    return _json_dumps_compact(out)


def _materialize_rows(candidates: list[Candidate]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train_rows: list[dict[str, Any]] = []
    test_rows: list[dict[str, Any]] = []
    answer_rows: list[dict[str, Any]] = []
    sample_rows: list[dict[str, Any]] = []
    diag_rows: list[dict[str, Any]] = []
    for cand in candidates:
        notes_json, tab_json = _event_payloads(cand)
        base = {
            "id": cand.id,
            "audio_path": cand.audio_path,
            "notes_json": notes_json,
            "clip_start_s": 0.0,
            "clip_duration_s": CLIP_DURATION_S,
        }
        diag_rows.append(
            {
                "id": cand.id,
                "split": cand.split,
                "source_stem": cand.track.stem,
                "annotation_member": cand.track.annotation_member,
                "source_start_s": round(cand.start, 3),
                "player": cand.track.player,
                "family": cand.track.family,
                "style": cand.track.style,
                "tempo": cand.track.tempo,
                "key": cand.track.key,
                "take_type": cand.track.take_type,
                "event_count": len(cand.notes),
                "lookup_bucket": cand.lookup_bucket,
                "scene_hash": cand.scene_hash,
            }
        )
        if cand.split == "train":
            row = dict(base)
            row["tab_json"] = tab_json
            row["confidence_label"] = 1.0
            train_rows.append(row)
        else:
            test_rows.append(dict(base))
            answer = {"id": cand.id, "tab_json": tab_json, "notes_json": notes_json}
            answer.update(cand.hidden)
            answer_rows.append(answer)
            sample_rows.append({"id": cand.id, "tab_json": _sample_tab(notes_json), "confidence": 0.24})

    train_df = pd.DataFrame(train_rows, columns=TRAIN_COLUMNS).sort_values("id").reset_index(drop=True)
    test_df = pd.DataFrame(test_rows, columns=TEST_COLUMNS).sort_values("id").reset_index(drop=True)
    answer_df = pd.DataFrame(answer_rows, columns=ANSWER_COLUMNS).sort_values("id").reset_index(drop=True)
    sample_df = pd.DataFrame(sample_rows, columns=SUBMISSION_COLUMNS).sort_values("id").reset_index(drop=True)
    diag_df = pd.DataFrame(diag_rows).sort_values("id").reset_index(drop=True)
    return train_df, test_df, answer_df, sample_df, diag_df


def _assert_no_nan_blank(name: str, df: pd.DataFrame) -> None:
    if df.isna().any().any():
        raise SystemExit(f"{name} contains NaN values")
    object_cols = [
        col
        for col in df.columns
        if pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col])
    ]
    for col in object_cols:
        if df[col].astype(str).str.strip().eq("").any():
            raise SystemExit(f"{name}.{col} contains blank string values")


class SmallAudioCache:
    def __init__(self, source: AudioSource, max_items: int = 4) -> None:
        self.source = source
        self.max_items = max_items
        self.cache: OrderedDict[str, tuple[int, np.ndarray]] = OrderedDict()

    def get(self, stem: str) -> tuple[int, np.ndarray]:
        if stem in self.cache:
            self.cache.move_to_end(stem)
            return self.cache[stem]
        value = self.source.read(stem)
        self.cache[stem] = value
        self.cache.move_to_end(stem)
        while len(self.cache) > self.max_items:
            self.cache.popitem(last=False)
        return value


def _write_audio_clips(candidates: list[Candidate], audio_source: AudioSource, public: Path) -> None:
    audio_dir = public / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    cache = SmallAudioCache(audio_source)
    for cand in candidates:
        sr, full = cache.get(cand.track.stem)
        start_frame = max(0, int(round(cand.start * sr)))
        end_frame = min(len(full), int(round((cand.start + CLIP_DURATION_S) * sr)))
        clip = full[start_frame:end_frame]
        expected_len = int(round(CLIP_DURATION_S * sr))
        if len(clip) < expected_len:
            clip = np.pad(clip, (0, expected_len - len(clip)))
        elif len(clip) > expected_len:
            clip = clip[:expected_len]
        _write_wav(audio_dir / Path(cand.audio_path).name, sr, clip.astype(np.float32))


def _write_csvs(public: Path, private: Path, train: pd.DataFrame, test: pd.DataFrame, answers: pd.DataFrame, sample: pd.DataFrame, diag: pd.DataFrame) -> None:
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    train.to_csv(public / "train.csv", index=False)
    test.to_csv(public / "test.csv", index=False)
    sample.to_csv(public / "sample_submission.csv", index=False)
    answers.to_csv(private / "answers.csv", index=False)
    diag.to_csv(private / "split_diagnostics.csv", index=False)


def _write_prepare_report(private: Path, candidates: list[Candidate], train: pd.DataFrame, test: pd.DataFrame, answers: pd.DataFrame) -> None:
    report = {
        "source_urls": [ANNOTATION_URL, AUDIO_URL],
        "rows_train": int(len(train)),
        "rows_test": int(len(test)),
        "test_players": sorted(SPLIT_TEST_PLAYERS),
        "clip_duration_s": CLIP_DURATION_S,
        "audio_materialization": "source-rate clipped excerpts with no added noise, EQ, phase randomization, or perturbation",
        "hidden_group_counts": {
            axis: answers[axis].astype(str).value_counts().sort_index().to_dict()
            for axis in GROUP_AXES_FOR_REPORT
            if axis in answers.columns
        },
        "lookup_bucket_counts": Counter(str(c.lookup_bucket) for c in candidates),
    }
    (private / "prepare_report.json").write_text(_json_dumps_compact(report), encoding="utf-8")


GROUP_AXES_FOR_REPORT = [
    "player_group",
    "style_group",
    "polyphony_band",
    "ambiguity_band",
    "fret_range_band",
    "note_density_band",
]


def prepare(raw: Path, public: Path, private: Path) -> None:
    raw = Path(raw)
    public = Path(public)
    private = Path(private)
    annotation_source = AnnotationSource(raw)
    audio_source = AudioSource(raw)
    candidates = _assign_ids_and_splits(_load_candidates(annotation_source))
    train, test, answers, sample, diag = _materialize_rows(candidates)
    for name, df in [("train", train), ("test", test), ("answers", answers), ("sample", sample)]:
        _assert_no_nan_blank(name, df)
        if not df["id"].is_unique:
            raise SystemExit(f"{name}.id is not unique")
    if set(test["id"]) != set(answers["id"]) or set(test["id"]) != set(sample["id"]):
        raise SystemExit("test, answers, and sample ids do not match")
    if set(train["id"]) & set(test["id"]):
        raise SystemExit("train/test id overlap detected")
    _write_audio_clips(candidates, audio_source, public)
    _write_csvs(public, private, train, test, answers, sample, diag)
    _write_prepare_report(private, candidates, train, test, answers)
    print(f"prepared rows: train={len(train)} test={len(test)} audio_clips={len(candidates)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=Path("raw"))
    ap.add_argument("--public", type=Path, default=Path("public"))
    ap.add_argument("--private", type=Path, default=Path("private"))
    args = ap.parse_args()
    prepare(args.raw, args.public, args.private)

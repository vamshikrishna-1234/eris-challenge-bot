from __future__ import annotations

import hashlib
import html
import json
import math
import re
import shutil
import tempfile
import zipfile
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np
import pandas as pd
from scipy.io import wavfile
from scipy.signal import resample_poly


ID_SALT = "disfluency-reparandum-repair-public-id-v1"
TEST_FRACTION = 0.25
MIN_GROUP_TEST = 20
SAMPLE_CONFIDENCE = 0.60
GENERATION_SEED = 20260702
GENERATION_MAX_SAMPLES = 700
TARGET_POSITIVE_FRACTION = 0.65

MANUAL_URL = "https://groups.inf.ed.ac.uk/ami/AMICorpusAnnotations/ami_public_manual_1.6.2.zip"
AUTO_URL = "https://groups.inf.ed.ac.uk/ami/AMICorpusAnnotations/ami_public_auto_1.5.1.zip"
AUDIO_URL_TEMPLATE = "https://groups.inf.ed.ac.uk/ami/AMICorpusMirror/amicorpus/{meeting}/audio/{meeting}.Mix-Headset.wav"

DEFAULT_MEETINGS = [
    "ES2012c",
    "ES2002b",
    "ES2006c",
    "IS1002b",
    "IS1004b",
    "TS3006b",
    "TS3009b",
    "TS3008c",
    "TS3009d",
    "IS1004c",
    "ES2012b",
    "ES2002c",
]

TYPE_MAP = {
    "ami_dsfl_1": "delete",
    "ami_dsfl_2": "disrupt",
    "ami_dsfl_3": "dm",
    "ami_dsfl_4": "eet",
    "ami_dsfl_5": "hesit",
    "ami_dsfl_6": "insert",
    "ami_dsfl_7": "mistake",
    "ami_dsfl_8": "omiss",
    "ami_dsfl_9": "order",
    "ami_dsfl_11": "other",
    "ami_dsfl_12": "repeat",
    "ami_dsfl_13": "replace",
    "ami_dsfl_14": "restart",
    "ami_dsfl_15": "sot",
    "ami_dsfl_16": "stutter",
    "ami_dsfl_17": "repair",
    "ami_dsfl_18": "reparans",
    "ami_dsfl_19": "reparandum",
}

NITE_NS = "{http://nite.sourceforge.net/}"
TARGET_SR = 16000
MAX_TOKENS = 34
MAX_CLIP_SEC = 12.0
MIN_CLIP_SEC = 0.70
GEN_ID_SALT = "ami-disfluency-repair-structure-v1"
FILLER_TOKENS = {"uh", "um", "umm", "erm", "er", "em", "hmm", "hm", "uhm", "ah"}
EMPHATIC_REPEAT_TOKENS = {
    "yeah",
    "yes",
    "okay",
    "ok",
    "right",
    "no",
    "very",
    "really",
    "quite",
    "sure",
    "exactly",
    "mmhmm",
    "mhm",
    "mm",
}

REQUIRED_RAW_COLUMNS = [
    "raw_clip_id",
    "audio_path",
    "token_transcript",
    "token_timing_json",
    "reparandum_span",
    "interregnum_span",
    "repair_onset",
    "is_disfluency",
    "confidence",
    "repair_type",
    "label_family",
    "source_meeting",
    "source_session",
    "source_family",
    "speaker_code",
    "speaker_family",
    "split_group",
    "recording_condition",
    "clip_start_sec",
    "clip_end_sec",
    "source_word_start",
    "source_word_end",
    "annotation_kind",
    "source_url",
]

PUBLIC_INPUT_COLUMNS = ["id", "audio_path", "token_transcript", "token_timing_json"]
LABEL_COLUMNS = ["reparandum_span", "interregnum_span", "repair_onset", "is_disfluency", "confidence"]
SUBMISSION_COLUMNS = ["id", "reparandum_span", "interregnum_span", "repair_onset", "is_disfluency", "confidence"]
ANSWER_COLUMNS = [
    "id",
    "reparandum_span",
    "interregnum_span",
    "repair_onset",
    "is_disfluency",
    "confidence",
    "token_count",
    "source_group",
    "repair_group",
    "source_meeting",
    "speaker_family",
    "split_group",
    "raw_clip_id",
]


def _local_name(tag: str) -> str:
    return tag.split("}", 1)[-1]


def _stable_hex(*parts: object, n: int = 24) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update(str(part).encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:n]


def _rng_for(seed: int, *parts: object) -> np.random.Generator:
    digest = hashlib.sha256(("|".join([str(seed), *map(str, parts)])).encode("utf-8")).digest()
    return np.random.default_rng(np.random.SeedSequence(int.from_bytes(digest, "big")))


def _normalize_token(text: str) -> str:
    text = html.unescape(text or "").strip().lower()
    text = text.replace("&apos;", "'").replace("'", "")
    text = re.sub(r"[^a-z0-9]+", "", text)
    return text


def _source_family(meeting: str) -> str:
    match = re.match(r"[A-Z]+", meeting)
    return match.group(0) if match else "UNK"


def _source_session(meeting: str) -> str:
    match = re.match(r"([A-Z]+\d+)", meeting)
    return match.group(1) if match else meeting


def _speaker_family(meeting: str, speaker: str) -> str:
    return f"{_source_family(meeting)}_{speaker}"


def _word_range_from_href(href: str) -> list[int]:
    nums = [int(x) for x in re.findall(r"words(\d+)\)", href)]
    if not nums:
        return []
    if len(nums) >= 2:
        lo, hi = nums[0], nums[1]
        if hi < lo:
            lo, hi = hi, lo
        return list(range(lo, hi + 1))
    return [nums[0]]


def _dsfl_type(el: ET.Element) -> str | None:
    for child in el:
        if _local_name(child.tag) == "pointer" and child.attrib.get("role") == "dsfl-type":
            match = re.search(r"id\(([^)]+)\)", child.attrib.get("href", ""))
            if match:
                return TYPE_MAP.get(match.group(1), match.group(1))
    return None


def _direct_word_ids(el: ET.Element) -> list[int]:
    ids: list[int] = []
    for child in el:
        if _local_name(child.tag) == "child":
            ids.extend(_word_range_from_href(child.attrib.get("href", "")))
    return sorted(set(ids))


def _node_word_ids(el: ET.Element) -> list[int]:
    ids = set(_direct_word_ids(el))
    for child in el:
        if _local_name(child.tag) == "dsfl":
            ids.update(_node_word_ids(child))
    return sorted(ids)


def _child_nodes_of_type(el: ET.Element, type_name: str) -> list[ET.Element]:
    return [child for child in el if _local_name(child.tag) == "dsfl" and _dsfl_type(child) == type_name]


class _AnnotationReader:
    def __init__(self, path: Path):
        self.path = Path(path)
        self._zip: zipfile.ZipFile | None = None

    def __enter__(self) -> "_AnnotationReader":
        if self.path.is_file():
            self._zip = zipfile.ZipFile(self.path, "r")
        elif not self.path.is_dir():
            raise FileNotFoundError(f"Missing annotation source {self.path}")
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        if self._zip is not None:
            self._zip.close()

    def exists(self, rel_path: str) -> bool:
        if self._zip is not None:
            return rel_path in self._zip.namelist()
        return (self.path / rel_path).exists()

    def read(self, rel_path: str) -> bytes:
        if self._zip is not None:
            return self._zip.read(rel_path)
        return (self.path / rel_path).read_bytes()


def _load_words(manual: _AnnotationReader, meeting: str, speaker: str) -> list[dict]:
    path = f"words/{meeting}.{speaker}.words.xml"
    if not manual.exists(path):
        return []
    root = ET.fromstring(manual.read(path))
    words: list[dict] = []
    for el in root:
        if _local_name(el.tag) != "w" or el.attrib.get("punc") == "true":
            continue
        token = _normalize_token(el.text or "")
        if not token:
            continue
        nite_id = el.attrib.get(NITE_NS + "id") or el.attrib.get("nite:id") or el.attrib.get("id", "")
        match = re.search(r"words(\d+)$", nite_id)
        if not match:
            continue
        try:
            start = float(el.attrib["starttime"])
            end = float(el.attrib["endtime"])
        except (KeyError, ValueError):
            continue
        if not (math.isfinite(start) and math.isfinite(end)) or end < start:
            continue
        words.append(
            {
                "idx": int(match.group(1)),
                "token": token,
                "raw": html.unescape(el.text or "").strip(),
                "start": start,
                "end": end,
            }
        )
    return sorted(words, key=lambda w: w["idx"])


def _load_disfluency_roots(auto: _AnnotationReader, meeting: str, speaker: str) -> list[ET.Element]:
    path = f"disfluency/automaticSG_MAN/{meeting}.{speaker}.disfluency.xml"
    if not auto.exists(path):
        return []
    root = ET.fromstring(auto.read(path))
    return [el for el in root if _local_name(el.tag) == "dsfl"]


def _span_label(ids: list[int], idx_to_local: dict[int, int]) -> str:
    if not ids:
        return "NONE"
    positions = sorted(idx_to_local[i] for i in ids if i in idx_to_local)
    if not positions:
        return "NONE"
    return f"[{positions[0]},{positions[-1]}]"


def _token_timing_json(window: list[dict], clip_start: float) -> str:
    payload = [
        {
            "token": w["token"],
            "start_ms": int(round(max(0.0, w["start"] - clip_start) * 1000)),
            "end_ms": int(round(max(0.0, w["end"] - clip_start) * 1000)),
        }
        for w in window
    ]
    return json.dumps(payload, separators=(",", ":"))


def _window_bounds(n_words: int, start_pos: int, end_pos: int, rng: np.random.Generator) -> tuple[int, int]:
    pre = int(rng.integers(4, 8))
    post = int(rng.integers(6, 11))
    lo = max(0, start_pos - pre)
    hi = min(n_words - 1, end_pos + post)
    while hi - lo + 1 > MAX_TOKENS:
        if start_pos - lo > hi - end_pos:
            lo += 1
        else:
            hi -= 1
    return lo, hi


def _make_row(
    *,
    meeting: str,
    speaker: str,
    words: list[dict],
    lo: int,
    hi: int,
    source_key: str,
    reparandum_ids: list[int],
    interregnum_ids: list[int],
    repair_ids: list[int],
    is_disfluency: int,
    repair_type: str,
    label_family: str,
    annotation_kind: str,
) -> dict | None:
    window = words[lo : hi + 1]
    if not window:
        return None
    clip_start = max(0.0, min(w["start"] for w in window) - 0.35)
    clip_end = max(w["end"] for w in window) + 0.55
    duration = clip_end - clip_start
    if duration < MIN_CLIP_SEC or duration > MAX_CLIP_SEC:
        return None
    idx_to_local = {w["idx"]: i for i, w in enumerate(window)}
    if is_disfluency:
        if not all(i in idx_to_local for i in reparandum_ids):
            return None
        if not all(i in idx_to_local for i in repair_ids):
            return None
        repair_onset = str(min(idx_to_local[i] for i in repair_ids))
    else:
        repair_onset = "NONE"
    raw_clip_id = "clip_" + _stable_hex(GEN_ID_SALT, source_key, n=20)
    return {
        "raw_clip_id": raw_clip_id,
        "audio_path": f"audio/{raw_clip_id}.wav",
        "token_transcript": json.dumps([w["token"] for w in window], separators=(",", ":")),
        "token_timing_json": _token_timing_json(window, clip_start),
        "reparandum_span": _span_label(reparandum_ids, idx_to_local) if is_disfluency else "NONE",
        "interregnum_span": _span_label(interregnum_ids, idx_to_local) if is_disfluency else "NONE",
        "repair_onset": repair_onset,
        "is_disfluency": int(is_disfluency),
        "confidence": 1.0,
        "repair_type": repair_type,
        "label_family": label_family,
        "source_meeting": meeting,
        "source_session": _source_session(meeting),
        "source_family": _source_family(meeting),
        "speaker_code": speaker,
        "speaker_family": _speaker_family(meeting, speaker),
        "split_group": f"{meeting}_{speaker}",
        "recording_condition": "headset_mix",
        "clip_start_sec": round(float(clip_start), 3),
        "clip_end_sec": round(float(clip_end), 3),
        "source_word_start": int(window[0]["idx"]),
        "source_word_end": int(window[-1]["idx"]),
        "annotation_kind": annotation_kind,
        "source_url": AUDIO_URL_TEMPLATE.format(meeting=meeting),
    }


def _extract_positive_rows(
    meeting: str,
    speaker: str,
    words: list[dict],
    roots: list[ET.Element],
    seed: int,
) -> tuple[list[dict], set[int], set[int]]:
    idx_to_pos = {w["idx"]: i for i, w in enumerate(words)}
    structured_events: list[dict] = []
    standalone_ids: set[int] = set()
    for root in roots:
        reparandum_nodes = _child_nodes_of_type(root, "reparandum")
        reparans_nodes = _child_nodes_of_type(root, "reparans")
        if reparandum_nodes and reparans_nodes:
            reparandum_ids = sorted({i for node in reparandum_nodes for i in _node_word_ids(node) if i in idx_to_pos})
            repair_ids = sorted({i for node in reparans_nodes for i in _node_word_ids(node) if i in idx_to_pos})
            if not reparandum_ids or not repair_ids or max(reparandum_ids) >= min(repair_ids):
                continue
            if len(reparandum_ids) > 5 or len(repair_ids) > 6:
                continue
            between = [
                w["idx"]
                for w in words
                if max(reparandum_ids) < w["idx"] < min(repair_ids)
                and w["idx"] not in reparandum_ids
                and w["idx"] not in repair_ids
            ]
            if len(between) > 5:
                continue
            source_key = root.attrib.get(NITE_NS + "id") or root.attrib.get("nite:id") or _stable_hex(
                meeting, speaker, reparandum_ids, repair_ids
            )
            r_tokens = [words[idx_to_pos[i]]["token"] for i in reparandum_ids]
            p_tokens = [words[idx_to_pos[i]]["token"] for i in repair_ids]
            if between:
                repair_type = "repeat_with_edit"
            elif len(reparandum_ids) > 1 or len(repair_ids) > 1:
                repair_type = "phrase_repeat"
            elif r_tokens == p_tokens:
                repair_type = "single_repeat"
            else:
                repair_type = "restart_repeat"
            structured_events.append(
                {
                    "source_key": source_key,
                    "reparandum_ids": reparandum_ids,
                    "interregnum_ids": between,
                    "repair_ids": repair_ids,
                    "repair_type": repair_type,
                    "range_ids": set(reparandum_ids + between + repair_ids),
                }
            )
        else:
            standalone_ids.update(i for i in _node_word_ids(root) if i in idx_to_pos)

    structured_id_owner: dict[int, str] = {}
    for event in structured_events:
        for idx in event["range_ids"]:
            structured_id_owner[idx] = event["source_key"]

    rows: list[dict] = []
    for event in structured_events:
        all_ids = event["reparandum_ids"] + event["interregnum_ids"] + event["repair_ids"]
        start_pos = min(idx_to_pos[i] for i in all_ids)
        end_pos = max(idx_to_pos[i] for i in all_ids)
        rng = _rng_for(seed, meeting, speaker, event["source_key"])
        lo, hi = _window_bounds(len(words), start_pos, end_pos, rng)
        window_ids = {w["idx"] for w in words[lo : hi + 1]}
        other_structured = {
            structured_id_owner[i]
            for i in window_ids
            if i in structured_id_owner and structured_id_owner[i] != event["source_key"]
        }
        if other_structured:
            continue
        row = _make_row(
            meeting=meeting,
            speaker=speaker,
            words=words,
            lo=lo,
            hi=hi,
            source_key=f"positive:{event['source_key']}",
            reparandum_ids=event["reparandum_ids"],
            interregnum_ids=event["interregnum_ids"],
            repair_ids=event["repair_ids"],
            is_disfluency=1,
            repair_type=event["repair_type"],
            label_family="disfluent_repeat_repair",
            annotation_kind="AMI automaticSG_MAN repeat reparandum/reparans",
        )
        if row is not None:
            rows.append(row)
    return rows, set(structured_id_owner), standalone_ids


def _make_negative_rows(
    meeting: str,
    speaker: str,
    words: list[dict],
    structured_ids: set[int],
    standalone_ids: set[int],
    seed: int,
) -> dict[str, list[dict]]:
    rows: dict[str, list[dict]] = {
        "emphatic_foil": [],
        "nonrepair_repeat_foil": [],
        "filler_no_repair": [],
        "clean_none": [],
    }
    n = len(words)
    if n < 8:
        return rows

    def add_window(kind: str, center_lo: int, center_hi: int, extra_key: object) -> None:
        rng = _rng_for(seed, meeting, speaker, kind, extra_key)
        lo, hi = _window_bounds(n, center_lo, center_hi, rng)
        window_ids = {w["idx"] for w in words[lo : hi + 1]}
        if window_ids & structured_ids:
            return
        row = _make_row(
            meeting=meeting,
            speaker=speaker,
            words=words,
            lo=lo,
            hi=hi,
            source_key=f"negative:{kind}:{meeting}:{speaker}:{extra_key}",
            reparandum_ids=[],
            interregnum_ids=[],
            repair_ids=[],
            is_disfluency=0,
            repair_type=kind,
            label_family="non_disfluent_foil",
            annotation_kind="AMI transcript window without structured repair target",
        )
        if row is not None:
            rows[kind].append(row)

    seen_centers: set[tuple[str, int]] = set()
    for i in range(n - 1):
        a, b = words[i]["token"], words[i + 1]["token"]
        if a == b and a in EMPHATIC_REPEAT_TOKENS:
            key = ("emphatic", words[i]["idx"])
            if key not in seen_centers:
                seen_centers.add(key)
                add_window("emphatic_foil", i, i + 1, words[i]["idx"])
        elif a == b and a not in {"a", "the", "to", "of", "and"}:
            key = ("nonrepair_repeat", words[i]["idx"])
            if key not in seen_centers:
                seen_centers.add(key)
                add_window("nonrepair_repeat_foil", i, i + 1, words[i]["idx"])
        if i + 2 < n and words[i]["token"] == words[i + 2]["token"] and words[i + 1]["token"] in {"and", "or"}:
            key = ("emphatic_gap", words[i]["idx"])
            if key not in seen_centers:
                seen_centers.add(key)
                add_window("emphatic_foil", i, i + 2, words[i]["idx"])

    standalone_positions = [i for i, w in enumerate(words) if w["idx"] in standalone_ids or w["token"] in FILLER_TOKENS]
    for i in standalone_positions:
        window_ids = {w["idx"] for w in words[max(0, i - 2) : min(n, i + 3)]}
        if window_ids & structured_ids:
            continue
        add_window("filler_no_repair", i, i, words[i]["idx"])

    for i in range(3, n - 4, 5):
        window = words[i - 3 : i + 5]
        toks = [w["token"] for w in window]
        ids = {w["idx"] for w in window}
        if ids & structured_ids:
            continue
        if any(t in FILLER_TOKENS for t in toks):
            continue
        if any(toks[j] == toks[j + 1] for j in range(len(toks) - 1)):
            continue
        add_window("clean_none", i, i + 1, words[i]["idx"])
    return rows


def _collect_rows(manual_source: Path, auto_source: Path, meetings: list[str], seed: int) -> tuple[list[dict], dict[str, list[dict]]]:
    positives: list[dict] = []
    negatives: dict[str, list[dict]] = {
        "emphatic_foil": [],
        "nonrepair_repeat_foil": [],
        "filler_no_repair": [],
        "clean_none": [],
    }
    with _AnnotationReader(manual_source) as manual, _AnnotationReader(auto_source) as auto:
        for meeting in meetings:
            for speaker in ["A", "B", "C", "D"]:
                words = _load_words(manual, meeting, speaker)
                if not words:
                    continue
                roots = _load_disfluency_roots(auto, meeting, speaker)
                pos_rows, structured_ids, standalone_ids = _extract_positive_rows(meeting, speaker, words, roots, seed)
                positives.extend(pos_rows)
                neg = _make_negative_rows(meeting, speaker, words, structured_ids, standalone_ids, seed)
                for key, value in neg.items():
                    negatives[key].extend(value)
    return positives, negatives


def _choose_rows(positives: list[dict], negatives: dict[str, list[dict]], max_samples: int, seed: int) -> list[dict]:
    rng = np.random.default_rng(seed)
    for rows in [positives, *negatives.values()]:
        rng.shuffle(rows)
    target = max_samples if max_samples > 0 else len(positives) + sum(len(v) for v in negatives.values())
    target_pos = min(len(positives), int(round(target * TARGET_POSITIVE_FRACTION)))
    by_pos_type: dict[str, list[dict]] = defaultdict(list)
    for row in positives:
        by_pos_type[str(row["repair_type"])].append(row)
    chosen: list[dict] = []
    hard_pos = by_pos_type["phrase_repeat"] + by_pos_type["repeat_with_edit"]
    rng.shuffle(hard_pos)
    chosen.extend(hard_pos[: min(len(hard_pos), target_pos)])
    remaining_pos = by_pos_type["single_repeat"] + hard_pos[min(len(hard_pos), target_pos) :]
    rng.shuffle(remaining_pos)
    if len(chosen) < target_pos:
        chosen.extend(remaining_pos[: target_pos - len(chosen)])
    quotas = {
        "nonrepair_repeat_foil": 107,
        "emphatic_foil": 60,
        "filler_no_repair": target,
        "clean_none": 0,
    }
    remaining_neg: list[dict] = []
    neg_needed = max(0, target - len(chosen))
    for kind, quota in quotas.items():
        if neg_needed <= 0:
            break
        take = min(len(negatives[kind]), max(0, quota), neg_needed)
        chosen.extend(negatives[kind][:take])
        remaining_neg.extend(negatives[kind][take:])
        neg_needed -= take
    rng.shuffle(remaining_neg)
    if len(chosen) < target:
        chosen.extend(remaining_neg[: target - len(chosen)])
    if len(chosen) < min(target, 200):
        raise RuntimeError(f"Only {len(chosen)} rows available; source annotations are insufficient for this build.")
    rng.shuffle(chosen)
    by_id: dict[str, dict] = {}
    for row in chosen:
        by_id[row["raw_clip_id"]] = row
    return list(by_id.values())[:target]


def _read_audio(path: Path) -> tuple[int, np.ndarray]:
    sr, data = wavfile.read(path)
    if data.ndim == 2:
        data = data.mean(axis=1)
    if not np.issubdtype(data.dtype, np.floating):
        data = data.astype(np.float32) / float(np.iinfo(data.dtype).max)
    else:
        data = data.astype(np.float32)
    if sr != TARGET_SR:
        gcd = math.gcd(int(sr), TARGET_SR)
        data = resample_poly(data, TARGET_SR // gcd, int(sr) // gcd).astype(np.float32)
        sr = TARGET_SR
    return sr, np.asarray(data, dtype=np.float32)


def _write_clip(audio: np.ndarray, sr: int, start_sec: float, end_sec: float, dest: Path) -> None:
    start = max(0, int(round(start_sec * sr)))
    end = min(len(audio), int(round(end_sec * sr)))
    if end <= start:
        raise ValueError(f"Empty audio clip for {dest}")
    clip = np.asarray(audio[start:end], dtype=np.float32)
    peak = float(np.max(np.abs(clip))) if clip.size else 0.0
    if peak > 0.98:
        clip = clip / peak * 0.98
    pcm = np.clip(clip * 32767.0, -32768, 32767).astype(np.int16)
    dest.parent.mkdir(parents=True, exist_ok=True)
    wavfile.write(dest, sr, pcm)


def _materialize_audio(rows: list[dict], audio_paths: dict[str, Path], out_dir: Path) -> None:
    by_meeting: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_meeting[str(row["source_meeting"])].append(row)
    audio_out = out_dir / "audio"
    if audio_out.exists():
        shutil.rmtree(audio_out)
    audio_out.mkdir(parents=True, exist_ok=True)
    for meeting, group in sorted(by_meeting.items()):
        sr, audio = _read_audio(audio_paths[meeting])
        for row in group:
            dest = out_dir / str(row["audio_path"])
            _write_clip(audio, sr, float(row["clip_start_sec"]), float(row["clip_end_sec"]), dest)


def _write_text_files(out_dir: Path, meetings: list[str]) -> None:
    (out_dir / "LICENSE.txt").write_text(
        "Derived audio clips, transcript windows, and annotation-derived labels are redistributed under Creative Commons Attribution 4.0 International (CC BY 4.0) from the AMI Meeting Corpus.\n"
        "License URL: https://creativecommons.org/licenses/by/4.0/\n"
        "No additional restrictions are applied by this challenge dataset.\n",
        encoding="utf-8",
    )
    (out_dir / "ATTRIBUTION.txt").write_text(
        "Source: AMI Meeting Corpus, University of Edinburgh and AMI consortium.\n"
        "Please cite the AMI Meeting Corpus when using these derived clips and labels.\n"
        "This derived dataset clips headset-mix meeting audio and aligns transcript windows with AMI automaticSG_MAN disfluency annotations and manual word timings.\n"
        "Modifications: selected bounded meeting subset; clipped WAV windows; normalized token transcripts; derived inclusive token-index spans for reparandum/interregnum/repair onset.\n",
        encoding="utf-8",
    )
    urls = [MANUAL_URL, AUTO_URL] + [AUDIO_URL_TEMPLATE.format(meeting=m) for m in meetings]
    (out_dir / "SOURCE_URLS.txt").write_text("\n".join(urls) + "\n", encoding="utf-8")
    (out_dir / "README.txt").write_text(
        "This raw directory contains real AMI meeting-speech clips for a disfluency repair-structure benchmark.\n"
        "clips.csv has one row per clipped WAV in audio/. Token transcripts are normalized word lists with implicit 0-based indices.\n"
        "Positive labels come from AMI automaticSG_MAN repeat annotations with explicit reparandum and reparans nodes aligned to manual word timings.\n"
        "Negative rows are real transcript windows without a structured repeat-repair target, including emphatic repeats, filler-only windows, and clean speech windows.\n",
        encoding="utf-8",
    )


def _resolve_clipped_raw_root(raw: Path) -> Path:
    for candidate in [raw, raw / "raw_upload", raw / "raw_data"]:
        if (candidate / "clips.csv").exists() and (candidate / "audio").exists():
            return candidate
    raise FileNotFoundError("Expected clips.csv and audio/ in raw, raw/raw_upload, or raw/raw_data.")


def _find_one(root: Path, pattern: str) -> Path | None:
    matches = sorted(p for p in root.rglob(pattern) if "public" not in p.parts and "private" not in p.parts)
    return matches[0] if matches else None


def _find_source_path(root: Path, names: list[str]) -> Path | None:
    search_roots = [root, root / "raw_upload", root / "raw_data"]
    for base in search_roots:
        for name in names:
            direct = base / name
            if direct.exists():
                return direct
    for name in names:
        found = _find_one(root, name)
        if found is not None:
            return found
    return None


def _derive_clipped_raw_from_ami_sources(raw: Path, temp_parent: Path) -> Path:
    manual_source = _find_source_path(raw, ["ami_public_manual_1.6.2", "ami_public_manual_1.6.2.zip"])
    auto_source = _find_source_path(raw, ["ami_public_auto_1.5.1", "ami_public_auto_1.5.1.zip"])
    if manual_source is None or auto_source is None:
        raise FileNotFoundError(
            "Expected official AMI manual and automatic annotation sources in raw/. "
            "The platform may provide them as extracted directories or original zip files."
        )
    meetings = list(DEFAULT_MEETINGS)
    audio_paths: dict[str, Path] = {}
    for meeting in meetings:
        wav = _find_one(raw, f"{meeting}.Mix-Headset.wav")
        if wav is None:
            raise FileNotFoundError(f"Missing official AMI headset-mix WAV for {meeting}")
        audio_paths[meeting] = wav
    positives, negatives = _collect_rows(manual_source, auto_source, meetings, GENERATION_SEED)
    rows = _choose_rows(positives, negatives, GENERATION_MAX_SAMPLES, GENERATION_SEED)
    out_dir = temp_parent / "derived_raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    _materialize_audio(rows, audio_paths, out_dir)
    df = pd.DataFrame(rows)[REQUIRED_RAW_COLUMNS].sort_values("raw_clip_id").reset_index(drop=True)
    df.to_csv(out_dir / "clips.csv", index=False)
    _write_text_files(out_dir, meetings)
    return out_dir


def _parse_tokens(value: object) -> list[str]:
    parsed = json.loads(str(value))
    if not isinstance(parsed, list) or not parsed:
        raise ValueError("token_transcript must be a non-empty JSON list")
    tokens = [str(x).strip() for x in parsed]
    if any(not t for t in tokens):
        raise ValueError("token_transcript contains blank tokens")
    if len(tokens) > 80:
        raise ValueError("token_transcript is unexpectedly long")
    return tokens


def _validate_span(span: object, token_count: int) -> None:
    text = str(span).strip()
    if text == "NONE":
        return
    match = re.fullmatch(r"\[(\d+),(\d+)\]", text)
    if not match:
        raise ValueError(f"Invalid span format: {text}")
    start, end = int(match.group(1)), int(match.group(2))
    if start > end or start < 0 or end >= token_count:
        raise ValueError(f"Span out of range: {text}")


def _validate_onset(onset: object, token_count: int) -> None:
    text = str(onset).strip()
    if text == "NONE":
        return
    if not re.fullmatch(r"\d+", text):
        raise ValueError(f"Invalid repair_onset: {text}")
    idx = int(text)
    if idx < 0 or idx >= token_count:
        raise ValueError(f"repair_onset out of range: {text}")


def _validate_raw(df: pd.DataFrame, raw_root: Path) -> pd.DataFrame:
    missing = [c for c in REQUIRED_RAW_COLUMNS if c not in df.columns]
    if missing:
        raise SystemExit(f"clips.csv missing required columns: {missing}")
    if df[REQUIRED_RAW_COLUMNS].isna().any().any():
        raise SystemExit("clips.csv contains NaN values in required columns")
    for col in REQUIRED_RAW_COLUMNS:
        if df[col].astype(str).str.len().eq(0).any():
            raise SystemExit(f"clips.csv contains blank values in {col}")
    if df["raw_clip_id"].duplicated().any():
        raise SystemExit("raw_clip_id must be unique before id assignment")
    out = df.copy()
    token_counts = []
    for _, row in out.iterrows():
        tokens = _parse_tokens(row["token_transcript"])
        token_count = len(tokens)
        token_counts.append(token_count)
        _validate_span(row["reparandum_span"], token_count)
        _validate_span(row["interregnum_span"], token_count)
        _validate_onset(row["repair_onset"], token_count)
        is_disf = int(row["is_disfluency"])
        if is_disf not in {0, 1}:
            raise SystemExit("is_disfluency must be 0 or 1")
        if is_disf == 0 and (
            str(row["reparandum_span"]) != "NONE"
            or str(row["interregnum_span"]) != "NONE"
            or str(row["repair_onset"]) != "NONE"
        ):
            raise SystemExit("non-disfluent rows must use NONE spans/onset")
        audio_path = raw_root / "audio" / Path(str(row["audio_path"])).name
        if not audio_path.exists():
            raise FileNotFoundError(f"Missing raw audio clip {audio_path}")
    out["token_count"] = token_counts
    out["is_disfluency"] = out["is_disfluency"].astype(int)
    out["confidence"] = pd.to_numeric(out["confidence"], errors="raise").astype(float)
    if not np.isfinite(out["confidence"]).all() or not out["confidence"].between(0, 1).all():
        raise SystemExit("confidence must be finite and in [0, 1]")
    return out


def _public_id_map(raw_ids: list[str]) -> dict[str, int]:
    pairs = [(hashlib.sha256(f"{ID_SALT}:{rid}".encode("utf-8")).hexdigest(), rid) for rid in raw_ids]
    if len({digest for digest, _ in pairs}) != len(pairs):
        raise SystemExit("Public id hash collision")
    return {rid: 100000 + i for i, (_, rid) in enumerate(sorted(pairs))}


def _split_penalty(df: pd.DataFrame, test_groups: set[str]) -> tuple[int, float]:
    test = df[df["source_session"].isin(test_groups)]
    if test.empty or len(test) == len(df):
        return 10_000_000, float("inf")
    penalty = 0
    for axis in ["is_disfluency", "label_family", "source_family", "repair_type"]:
        counts = test[axis].astype(str).value_counts()
        for count in counts.tolist():
            if count < MIN_GROUP_TEST:
                penalty += (MIN_GROUP_TEST - int(count)) * 100
        if axis in {"is_disfluency", "source_family", "repair_type"} and counts.shape[0] < df[axis].nunique():
            penalty += (df[axis].nunique() - counts.shape[0]) * 300
    target = len(df) * TEST_FRACTION
    size_penalty = abs(len(test) - target) / max(1.0, target)
    digest = hashlib.sha256(("|".join(sorted(test_groups)) + ID_SALT).encode("utf-8")).hexdigest()
    jitter = int(digest[:6], 16) / 16**6 * 0.001
    return penalty, size_penalty + jitter


def _choose_group_split(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    groups = sorted(df["source_session"].astype(str).unique().tolist())
    if len(groups) < 2:
        raise SystemExit("Need at least two source sessions for a grouped split")
    target_k = max(1, int(round(len(groups) * TEST_FRACTION)))
    candidate_ks = sorted({max(1, target_k - 1), target_k, min(len(groups) - 1, target_k + 1)})
    best: tuple[int, float, set[str]] | None = None
    for k in candidate_ks:
        for combo in combinations(groups, k):
            test_groups = set(combo)
            penalty, size_penalty = _split_penalty(df, test_groups)
            if best is None or (penalty, size_penalty) < (best[0], best[1]):
                best = (penalty, size_penalty, test_groups)
    if best is None:
        raise SystemExit("Could not choose a valid grouped split")
    train = df[~df["source_session"].isin(best[2])].copy()
    test = df[df["source_session"].isin(best[2])].copy()
    if train.empty or test.empty:
        raise SystemExit("Grouped split produced an empty train or test set")
    for col in ["source_meeting", "source_session", "split_group"]:
        overlap = set(train[col].astype(str)) & set(test[col].astype(str))
        if overlap:
            raise SystemExit(f"{col} leakage across train/test: {len(overlap)} shared values")
    for label in [0, 1]:
        if int((test["is_disfluency"] == label).sum()) < MIN_GROUP_TEST:
            raise SystemExit("Test split underfills disfluency/non-disfluency labels")
    return train, test


def _repair_sparse_axis(values: pd.Series, min_count: int) -> pd.Series:
    counts = values.astype(str).value_counts()
    if counts.empty:
        return values.astype(str)
    rare = set(counts[counts < min_count].index.astype(str))
    if not rare:
        return values.astype(str)
    majority = str(counts.idxmax())
    rare_total = int(values.astype(str).isin(rare).sum())
    replacement = "OTHER" if rare_total >= min_count else majority
    return values.astype(str).map(lambda x: replacement if x in rare else x)


def _copy_audio(raw_root: Path, split_dir: Path, frame: pd.DataFrame) -> pd.Series:
    audio_out = split_dir / "audio"
    audio_out.mkdir(parents=True, exist_ok=True)
    rel_paths = []
    for _, row in frame.iterrows():
        src = raw_root / "audio" / Path(str(row["audio_path"])).name
        dst_name = f"{int(row['id'])}.wav"
        shutil.copy2(src, audio_out / dst_name)
        rel_paths.append(f"{split_dir.name}/audio/{dst_name}")
    return pd.Series(rel_paths, index=frame.index)


def _sample_submission(test: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "id": int(row["id"]),
            "reparandum_span": "NONE",
            "interregnum_span": "NONE",
            "repair_onset": "NONE",
            "is_disfluency": 0,
            "confidence": SAMPLE_CONFIDENCE,
        }
        for _, row in test.iterrows()
    ]
    return pd.DataFrame(rows, columns=SUBMISSION_COLUMNS)


def _write_sorted(df: pd.DataFrame, path: Path, columns: list[str]) -> None:
    frame = df[columns].copy().sort_values("id").reset_index(drop=True)
    frame.to_csv(path, index=False)


def prepare(raw: Path, public: Path, private: Path) -> None:
    raw = Path(raw)
    temp_ctx: tempfile.TemporaryDirectory[str] | None = None
    try:
        raw_root = _resolve_clipped_raw_root(raw)
    except FileNotFoundError:
        temp_ctx = tempfile.TemporaryDirectory(prefix="ami_disfluency_prepare_")
        raw_root = _derive_clipped_raw_from_ami_sources(raw, Path(temp_ctx.name))
    public = Path(public)
    private = Path(private)
    try:
        if public.exists():
            shutil.rmtree(public)
        if private.exists():
            shutil.rmtree(private)
        public.mkdir(parents=True, exist_ok=True)
        private.mkdir(parents=True, exist_ok=True)

        raw_df = pd.read_csv(raw_root / "clips.csv", dtype=str)
        df = _validate_raw(raw_df, raw_root)
        id_lookup = _public_id_map(df["raw_clip_id"].astype(str).tolist())
        df["id"] = df["raw_clip_id"].map(id_lookup).astype(int)

        train, test = _choose_group_split(df)
        train = train.copy()
        test = test.copy()
        train["audio_path"] = _copy_audio(raw_root, public / "train", train)
        test["audio_path"] = _copy_audio(raw_root, public / "test", test)

        train["confidence"] = 1.0
        _write_sorted(train, public / "train.csv", PUBLIC_INPUT_COLUMNS + LABEL_COLUMNS)
        _write_sorted(test, public / "test.csv", PUBLIC_INPUT_COLUMNS)
        _write_sorted(_sample_submission(test), public / "sample_submission.csv", SUBMISSION_COLUMNS)

        answers = test.copy()
        answers["confidence"] = 1.0
        answers["source_group"] = _repair_sparse_axis(answers["source_family"], MIN_GROUP_TEST)
        answers["repair_group"] = _repair_sparse_axis(answers["repair_type"], MIN_GROUP_TEST)
        for axis in ["source_group", "repair_group"]:
            counts = answers[axis].value_counts()
            if counts.empty or int(counts.min()) < MIN_GROUP_TEST:
                raise SystemExit(f"Underfilled hidden subgroup {axis}: {counts.to_dict()}")
        _write_sorted(answers, private / "answers.csv", ANSWER_COLUMNS)

        leakage_cols = {
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
            "annotation_kind",
            "source_url",
        }
        for pub_file in [public / "train.csv", public / "test.csv"]:
            pub_cols = set(pd.read_csv(pub_file, nrows=0).columns)
            if pub_file.name == "test.csv" and leakage_cols & pub_cols:
                raise SystemExit(f"Leakage-prone columns present in {pub_file.name}")
        for frame, name in [
            (pd.read_csv(public / "train.csv"), "train"),
            (pd.read_csv(public / "test.csv"), "test"),
            (pd.read_csv(private / "answers.csv"), "answers"),
        ]:
            if frame.isna().any().any():
                raise SystemExit(f"{name} contains NaN values")
            if frame.astype(str).apply(lambda col: col.str.len().eq(0)).any().any():
                raise SystemExit(f"{name} contains blank values")
    finally:
        if temp_ctx is not None:
            temp_ctx.cleanup()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=Path("raw_data"))
    parser.add_argument("--public", type=Path, default=Path("public"))
    parser.add_argument("--private", type=Path, default=Path("private"))
    args = parser.parse_args()
    prepare(args.raw, args.public, args.private)
    print("OK: prepare complete.")

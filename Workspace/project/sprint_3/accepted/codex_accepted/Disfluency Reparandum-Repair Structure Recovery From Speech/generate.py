from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import re
import shutil
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np
import pandas as pd
from scipy.io import wavfile
from scipy.signal import resample_poly


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
QUICK_MEETINGS = ["ES2002b", "IS1002b", "TS3006b"]

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
ID_SALT = "ami-disfluency-repair-structure-v1"
TARGET_POSITIVE_FRACTION = 0.65
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

RAW_COLUMNS = [
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


def _ensure_download(url: str, dest: Path, skip_download: bool) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        return
    if skip_download:
        raise FileNotFoundError(
            f"Missing required source file {dest}. Re-run without --skip-download or place it in --source-cache."
        )
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".partial")
    print(f"Downloading {url}")
    urllib.request.urlretrieve(url, tmp)
    tmp.replace(dest)


def _ensure_source_cache(cache: Path, meetings: list[str], skip_download: bool) -> tuple[Path, Path, dict[str, Path]]:
    cache.mkdir(parents=True, exist_ok=True)
    manual_zip = cache / "ami_public_manual_1.6.2.zip"
    auto_zip = cache / "ami_public_auto_1.5.1.zip"
    _ensure_download(MANUAL_URL, manual_zip, skip_download)
    _ensure_download(AUTO_URL, auto_zip, skip_download)
    audio_dir = cache / "audio"
    audio_dir.mkdir(exist_ok=True)
    audio_paths: dict[str, Path] = {}
    for meeting in meetings:
        candidates = [
            audio_dir / f"{meeting}.Mix-Headset.wav",
            cache / f"{meeting}.Mix-Headset.wav",
        ]
        found = next((p for p in candidates if p.exists() and p.stat().st_size > 0), None)
        if found is None:
            found = audio_dir / f"{meeting}.Mix-Headset.wav"
            _ensure_download(AUDIO_URL_TEMPLATE.format(meeting=meeting), found, skip_download)
        audio_paths[meeting] = found
    return manual_zip, auto_zip, audio_paths


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


def _load_words(manual: zipfile.ZipFile, meeting: str, speaker: str) -> list[dict]:
    path = f"words/{meeting}.{speaker}.words.xml"
    if path not in manual.namelist():
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


def _load_disfluency_roots(auto: zipfile.ZipFile, meeting: str, speaker: str) -> list[ET.Element]:
    path = f"disfluency/automaticSG_MAN/{meeting}.{speaker}.disfluency.xml"
    if path not in auto.namelist():
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
    raw_clip_id = "clip_" + _stable_hex(ID_SALT, source_key, n=20)
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
        root_type = _dsfl_type(root)
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
            source_key = root.attrib.get(NITE_NS + "id") or root.attrib.get("nite:id") or _stable_hex(meeting, speaker, reparandum_ids, repair_ids)
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
        source_key = f"negative:{kind}:{meeting}:{speaker}:{extra_key}"
        row = _make_row(
            meeting=meeting,
            speaker=speaker,
            words=words,
            lo=lo,
            hi=hi,
            source_key=source_key,
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


def _collect_rows(manual_zip: Path, auto_zip: Path, meetings: list[str], seed: int) -> tuple[list[dict], dict[str, list[dict]]]:
    positives: list[dict] = []
    negatives: dict[str, list[dict]] = {
        "emphatic_foil": [],
        "nonrepair_repeat_foil": [],
        "filler_no_repair": [],
        "clean_none": [],
    }
    with zipfile.ZipFile(manual_zip, "r") as manual, zipfile.ZipFile(auto_zip, "r") as auto:
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
        "This raw upload contains real AMI meeting-speech clips for a disfluency repair-structure benchmark.\n"
        "clips.csv has one row per clipped WAV in audio/. Token transcripts are normalized word lists with implicit 0-based indices.\n"
        "Positive labels come from AMI automaticSG_MAN repeat annotations with explicit reparandum and reparans nodes aligned to manual word timings.\n"
        "Negative rows are real transcript windows without a structured repeat-repair target, including emphatic repeats, filler-only windows, and clean speech windows.\n",
        encoding="utf-8",
    )


def build_raw_dataset(args: argparse.Namespace) -> None:
    meetings = QUICK_MEETINGS if args.quick else DEFAULT_MEETINGS
    max_samples = args.max_samples
    if args.quick:
        max_samples = min(max_samples, 240)
    manual_zip, auto_zip, audio_paths = _ensure_source_cache(Path(args.source_cache), meetings, args.skip_download)
    positives, negatives = _collect_rows(manual_zip, auto_zip, meetings, args.seed)
    print(
        "Candidate rows:",
        f"positive={len(positives)}",
        " ".join(f"{k}={len(v)}" for k, v in negatives.items()),
    )
    rows = _choose_rows(positives, negatives, max_samples, args.seed)
    out_dir = Path(args.output)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    _materialize_audio(rows, audio_paths, out_dir)
    df = pd.DataFrame(rows)
    df = df[RAW_COLUMNS].sort_values("raw_clip_id").reset_index(drop=True)
    if df["raw_clip_id"].duplicated().any():
        raise RuntimeError("raw_clip_id collision")
    df.to_csv(out_dir / "clips.csv", index=False)
    _write_text_files(out_dir, meetings)
    print(f"Wrote {len(df)} rows to {out_dir / 'clips.csv'}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Acquire and preprocess AMI disfluency repair clips.")
    parser.add_argument("--source-cache", type=Path, default=Path("_source_cache"), help="Directory holding AMI zips and source WAVs.")
    parser.add_argument("--output", type=Path, default=Path("raw_data"), help="Output raw_data directory.")
    parser.add_argument("--max-samples", type=int, default=700, help="Maximum clipped rows to write.")
    parser.add_argument("--seed", type=int, default=20260702, help="Deterministic sampling seed.")
    parser.add_argument("--quick", action="store_true", help="Use a smaller meeting subset and cap row count for smoke testing.")
    parser.add_argument("--skip-download", action="store_true", help="Require all source files to already exist in --source-cache.")
    return parser.parse_args()


if __name__ == "__main__":
    build_raw_dataset(parse_args())

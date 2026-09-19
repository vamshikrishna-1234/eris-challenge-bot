"""Prepare source-neutral MEVA activity videos and hidden activity ledgers."""

from __future__ import annotations

import contextlib
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import math
import os
import shutil
import subprocess
import tempfile
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterator

import numpy as np


ID_SALT = "hidden-ledger-public-id-v2-6c72d8b94f31"
TRANSFORM_SALT = "hidden-ledger-render-v2-2a16e84d91f7"
FPS = 30.0
WINDOW_FRAMES = 240
STRIDE_FRAMES = 255  # 8.0 seconds plus a 0.5-second no-neighbour guard.
OUTPUT_FRAMES = 32
OUTPUT_FPS = 4
OUTPUT_SIZE = 256
CRF_VALUE = "12"
MAX_PUBLIC_VIDEO_BYTES = 1_000_000
EXPECTED_TRAIN = 479
EXPECTED_TEST = 175
MIN_GROUP_TEST = 30


# base, exact official bytes, split, windows, strongest available leakage group, modality
SOURCE_SPECS = [
    ("2018-03-12.11-05-01.11-10-01.school.G423", 71953582, "train", 35, "eo_20180312_g423_1105", "eo"),
    ("2018-03-12.10-00-00.10-05-00.school.G420", 70660918, "test", 35, "eo_20180312_g420_1000", "eo"),
    ("2018-03-11.11-50-00.11-54-59.school.G423", 81534972, "test", 35, "eo_20180311_g423_1150", "eo"),
    ("2018-03-11.17-10-01.17-15-01.school.G419", 85201548, "test", 35, "eo_20180311_g419_1710", "eo"),
    ("2018-03-11.14-05-00.14-10-00.school.G420", 73922476, "train", 35, "eo_20180311_g420_1405", "eo"),
    ("2018-03-09.10-10-00.10-15-00.school.G423", 96453698, "train", 35, "eo_20180309_g423_1010", "eo"),
    ("2018-03-09.10-30-01.10-35-01.school.G420", 58329782, "train", 35, "eo_20180309_g420_1030", "eo"),
    ("2018-03-07.17-20-06.17-25-06.school.G424", 108761812, "train", 35, "eo_20180307_g424_1720", "eo"),
    ("2018-03-07.11-10-00.11-15-00.school.G420", 61610642, "test", 35, "eo_20180307_g420_1110", "eo"),
    ("2018-03-13.16-30-00.16-35-00.school.G423", 81810710, "train", 35, "eo_20180313_g423_1630", "eo"),
    ("2018-03-15.15-15-00.15-20-00.school.G424", 92024426, "test", 35, "eo_20180315_g424_1515", "eo"),
    ("2018-03-05.13-20-01.13-25-01.bus.G331", 67181226, "train", 35, "eo_20180305_g331_1320", "eo"),
    ("2018-03-11.11-40-00.11-45-00.school.G474", 3102474, "train", 26, "ir_20180311_g474_1140_1150", "ir"),
    ("2018-03-11.11-45-00.11-50-00.school.G474", 2777382, "train", 26, "ir_20180311_g474_1140_1150", "ir"),
    ("2018-03-11.16-15-00.16-20-00.hospital.G479", 1903990, "train", 26, "ir_20180311_g479_1615_1625", "ir"),
    ("2018-03-11.16-20-00.16-25-00.hospital.G479", 2025392, "train", 26, "ir_20180311_g479_1615_1625", "ir"),
    ("2018-03-11.16-30-00.16-35-00.bus.G475", 1819848, "train", 26, "ir_20180311_multicam_1630_1640", "ir"),
    ("2018-03-11.16-30-00.16-35-00.hospital.G476", 2048456, "train", 26, "ir_20180311_multicam_1630_1640", "ir"),
    ("2018-03-11.16-30-00.16-35-00.hospital.G479", 2049446, "train", 26, "ir_20180311_multicam_1630_1640", "ir"),
    ("2018-03-11.16-30-00.16-35-00.school.G474", 2315510, "train", 26, "ir_20180311_multicam_1630_1640", "ir"),
    ("2018-03-11.16-35-00.16-40-00.hospital.G479", 1991690, "train", 26, "ir_20180311_multicam_1630_1640", "ir"),
]


# Exact deterministic decomposition of the official activity-name vocabulary.
LABEL_STATE = {
    "hand_interacts_with_person": ("hand", "interacts", "person"),
    "person_abandons_package": ("person", "abandons", "package"),
    "person_carries_heavy_object": ("person", "carries", "heavy_object"),
    "person_closes_facility_door": ("person", "closes", "facility_door"),
    "person_closes_trunk": ("person", "closes", "trunk"),
    "person_closes_vehicle_door": ("person", "closes", "vehicle_door"),
    "person_embraces_person": ("person", "embraces", "person"),
    "person_enters_scene_through_structure": ("person", "enters", "scene_structure"),
    "person_enters_vehicle": ("person", "enters", "vehicle"),
    "person_exits_scene_through_structure": ("person", "exits", "scene_structure"),
    "person_exits_vehicle": ("person", "exits", "vehicle"),
    "person_interacts_with_laptop": ("person", "interacts", "laptop"),
    "person_loads_vehicle": ("person", "loads", "vehicle"),
    "person_opens_facility_door": ("person", "opens", "facility_door"),
    "person_opens_trunk": ("person", "opens", "trunk"),
    "person_opens_vehicle_door": ("person", "opens", "vehicle_door"),
    "person_picks_up_object": ("person", "picks_up", "object"),
    "person_purchases": ("person", "purchases", "object"),
    "person_puts_down_object": ("person", "puts_down", "object"),
    "person_reads_document": ("person", "reads", "document"),
    "person_rides_bicycle": ("person", "rides", "bicycle"),
    "person_sits_down": ("person", "sits", "none"),
    "person_stands_up": ("person", "stands", "none"),
    "person_steals_object": ("person", "steals", "object"),
    "person_talks_on_phone": ("person", "talks", "phone"),
    "person_talks_to_person": ("person", "talks", "person"),
    "person_texts_on_phone": ("person", "texts", "phone"),
    "person_transfers_object": ("person", "transfers", "object"),
    "person_unloads_vehicle": ("person", "unloads", "vehicle"),
    "vehicle_drops_off_person": ("vehicle", "drops_off", "person"),
    "vehicle_makes_u_turn": ("vehicle", "makes_u_turn", "none"),
    "vehicle_picks_up_person": ("vehicle", "picks_up", "person"),
    "vehicle_reverses": ("vehicle", "reverses", "none"),
    "vehicle_starts": ("vehicle", "starts", "none"),
    "vehicle_stops": ("vehicle", "stops", "none"),
    "vehicle_turns_left": ("vehicle", "turns", "left"),
    "vehicle_turns_right": ("vehicle", "turns", "right"),
}


def _coupled_pairs() -> set[frozenset[str]]:
    """The official MEVA Annotation Definitions coupled-activities table."""
    out: set[frozenset[str]] = set()

    def add(left: str, rights: list[str]) -> None:
        for right in rights:
            out.add(frozenset((left, right)))

    structure = ["person_enters_scene_through_structure", "person_exits_scene_through_structure"]
    vehicle_events = ["person_enters_vehicle", "person_exits_vehicle", "person_loads_vehicle",
                      "person_unloads_vehicle", "vehicle_picks_up_person", "vehicle_drops_off_person"]
    facility_close_events = ["person_enters_vehicle", "person_exits_vehicle",
                             "person_loads_vehicle", "person_unloads_vehicle"]
    add("person_opens_facility_door", structure)
    add("person_closes_facility_door", facility_close_events)
    add("person_opens_vehicle_door", vehicle_events)
    add("person_closes_vehicle_door", ["vehicle_picks_up_person", "vehicle_drops_off_person"])
    add("person_opens_trunk", ["person_loads_vehicle", "person_unloads_vehicle"])
    add("person_closes_trunk", ["person_loads_vehicle", "person_unloads_vehicle"])
    add("vehicle_picks_up_person", ["vehicle_starts", "vehicle_stops", "person_opens_vehicle_door",
                                     "person_closes_vehicle_door"])
    add("vehicle_drops_off_person", ["vehicle_starts", "vehicle_stops", "person_opens_vehicle_door",
                                      "person_closes_vehicle_door"])
    return out


DOCUMENTED_PAIRS = _coupled_pairs()


def _digest_seed(text: str) -> np.random.Generator:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return np.random.default_rng(np.random.SeedSequence(list(digest)))


def _public_id(base: str, start: int) -> str:
    token = hashlib.sha256(f"{ID_SALT}|{base}|{start}".encode("utf-8")).hexdigest()[:18]
    return f"item_{token}"


def _window_indices(count: int) -> list[int]:
    if count == 35:
        return list(range(35))
    if count == 26:
        values = [round(i * 34 / 25) for i in range(26)]
        if len(set(values)) != 26:
            raise RuntimeError("Internal window schedule is invalid")
        return values
    raise RuntimeError("Unsupported source window count")


def _sample_indices(base: str, start: int) -> list[int]:
    rng = _digest_seed(f"{TRANSFORM_SALT}|sample|{base}|{start}")
    values = np.rint(np.linspace(start, start + WINDOW_FRAMES - 1, OUTPUT_FRAMES)).astype(int)
    values += rng.integers(-2, 3, size=OUTPUT_FRAMES)
    values[0] = max(start, values[0])
    values[-1] = min(start + WINDOW_FRAMES - 1, values[-1])
    for i in range(1, len(values)):
        values[i] = max(values[i], values[i - 1] + 1)
    if values[-1] > start + WINDOW_FRAMES - 1:
        shift = values[-1] - (start + WINDOW_FRAMES - 1)
        values -= shift
    return values.tolist()


def _find_unique(root: Path, name: str) -> Path:
    matches = [p for p in root.rglob(name) if p.is_file()]
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected exactly one untouched official file named {name}")
    return matches[0]


@contextlib.contextmanager
def _materialized_raw(raw: Path) -> Iterator[Path]:
    # Accept URL-imported/extracted trees, a retained official zip, or a one-level wrapper.
    if list(raw.rglob("*.r13.avi")):
        yield raw
        return
    zips = ([raw] if raw.is_file() and raw.name == "OFFICIAL_RAW_FILES_ONLY.zip" else
            [p for p in raw.rglob("OFFICIAL_RAW_FILES_ONLY.zip") if p.is_file()])
    if len(zips) != 1:
        raise FileNotFoundError("The official raw MEVA files or OFFICIAL_RAW_FILES_ONLY.zip are missing")
    with tempfile.TemporaryDirectory(prefix="meva_official_raw_") as tmp:
        target = Path(tmp)
        with zipfile.ZipFile(zips[0], "r") as archive:
            for info in archive.infolist():
                rel = Path(info.filename.replace("\\", "/"))
                if rel.is_absolute() or ".." in rel.parts:
                    raise RuntimeError("Unsafe path in official raw archive")
            archive.extractall(target)
        yield target


def _video_name(base: str) -> str:
    return f"{base}.r13.avi"


def _annotation_name(base: str, suffix: str) -> str:
    return f"{base}.{suffix}.yml"


def _load_annotations(root: Path, base: str) -> list[dict[str, Any]]:
    import yaml
    activities_path = _find_unique(root, _annotation_name(base, "activities"))
    types_path = _find_unique(root, _annotation_name(base, "types"))
    activities = yaml.safe_load(activities_path.read_text(encoding="utf-8")) or []
    type_packets = yaml.safe_load(types_path.read_text(encoding="utf-8")) or []
    type_map: dict[int, str] = {}
    for packet in type_packets:
        data = packet.get("types") if isinstance(packet, dict) else None
        if not data:
            continue
        labels = data.get("cset3", {})
        if not labels:
            continue
        type_map[int(data["id1"])] = max(labels, key=labels.get)

    events: list[dict[str, Any]] = []
    for packet in activities:
        act = packet.get("act") if isinstance(packet, dict) else None
        if not act:
            continue
        labels = act.get("act2", {})
        if not labels:
            continue
        label = max(labels, key=labels.get)
        if label == "empty_37":
            continue
        if label not in LABEL_STATE:
            raise RuntimeError(f"Unmapped official activity label in {base}")
        span = act.get("timespan", [{}])[0].get("tsr0")
        if not isinstance(span, list) or len(span) != 2:
            raise RuntimeError(f"Malformed official activity span in {base}")
        actor_ids = sorted({int(x["id1"]) for x in act.get("actors", []) if "id1" in x})
        roles = sorted({type_map[x] for x in actor_ids if x in type_map})
        if actor_ids and not roles:
            raise RuntimeError(f"Official actor types do not link for {base}")
        events.append({"label": label, "frame_start": int(span[0]), "frame_end": int(span[1]),
                       "roles": roles, "actor_ids": actor_ids,
                       "event_id": int(act.get("id2", len(events)))})
    return events


def _graph_for_window(events: list[dict[str, Any]], start: int) -> dict[str, Any]:
    end = start + WINDOW_FRAMES - 1
    internal = []
    for event in events:
        if event["frame_end"] < start or event["frame_start"] > end:
            continue
        clipped_start = max(start, event["frame_start"])
        clipped_end = min(end, event["frame_end"])
        start_bin = int(math.floor((clipped_start - start) * 31 / (WINDOW_FRAMES - 1)))
        end_bin = int(math.ceil((clipped_end - start) * 31 / (WINDOW_FRAMES - 1)))
        agent, action, context = LABEL_STATE[event["label"]]
        internal.append({
            "start": max(0, min(31, start_bin)), "end": max(0, min(31, end_bin)),
            "state": {"agent": agent, "action": action, "context": context, "roles": event["roles"]},
            "_label": event["label"], "_frame_start": event["frame_start"],
            "_frame_end": event["frame_end"], "_event_id": event["event_id"],
            "_actor_ids": tuple(event["actor_ids"]),
        })
    internal.sort(key=lambda n: (n["start"], n["end"], n["state"]["agent"], n["state"]["action"],
                                 n["state"]["context"], tuple(n["state"]["roles"]), n["_event_id"]))

    nodes = []
    for idx, node in enumerate(internal):
        nodes.append({"id": idx, "start": node["start"], "end": node["end"], "state": node["state"]})
    edges = []
    for i, left in enumerate(internal):
        for j in range(i + 1, len(internal)):
            right = internal[j]
            overlap = max(left["_frame_start"], right["_frame_start"]) <= min(left["_frame_end"], right["_frame_end"])
            gap = max(0, right["_frame_start"] - left["_frame_end"])
            edge_type = None
            if frozenset((left["_label"], right["_label"])) in DOCUMENTED_PAIRS and (overlap or gap <= 30):
                edge_type = "documented_pair"
            elif overlap:
                edge_type = "temporal_overlap"
            elif j == i + 1:
                edge_type = "temporal_next"
            if edge_type is not None:
                edges.append({"from": i, "to": j, "type": edge_type})
    edges.sort(key=lambda e: (e["from"], e["to"], e["type"]))
    if len(nodes) > 32 or len(edges) > 256:
        raise RuntimeError("Derived official graph exceeds the documented schema caps")
    return {"nodes": nodes, "edges": edges}


def _canonical_json(graph: dict[str, Any]) -> str:
    return json.dumps(graph, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def _motion_center(frames: list[np.ndarray]) -> tuple[float, float]:
    import cv2
    h, w = frames[0].shape[:2]
    scale = 320.0 / max(h, w)
    small = [cv2.resize(frame, (max(2, round(w * scale)), max(2, round(h * scale))),
                        interpolation=cv2.INTER_AREA) for frame in frames[::4]]
    energy = np.zeros(small[0].shape[:2], dtype=np.float32)
    for left, right in zip(small, small[1:]):
        diff = cv2.cvtColor(cv2.absdiff(left, right), cv2.COLOR_BGR2GRAY).astype(np.float32)
        energy += cv2.GaussianBlur(diff, (9, 9), 0)
    threshold = float(np.percentile(energy, 82.0))
    mask = np.maximum(0.0, energy - threshold)
    total = float(mask.sum())
    if total <= 1e-6:
        return w / 2.0, h / 2.0
    ys, xs = np.indices(mask.shape)
    return float((xs * mask).sum() / total / scale), float((ys * mask).sum() / total / scale)


def _transform_frames(frames: list[np.ndarray], base: str, start: int) -> list[np.ndarray]:
    import cv2
    if len(frames) != OUTPUT_FRAMES or any(frame is None for frame in frames):
        raise RuntimeError("Could not decode all required source frames")
    h, w = frames[0].shape[:2]
    if any(frame.shape[:2] != (h, w) for frame in frames):
        raise RuntimeError("Source dimensions changed inside one official video")
    rng = _digest_seed(f"{TRANSFORM_SALT}|pixels|{base}|{start}")
    cx, cy = _motion_center(frames)
    side = int(round(min(h, w) * rng.uniform(0.88, 0.98)))
    cx += float(rng.uniform(-0.035, 0.035) * side)
    cy += float(rng.uniform(-0.025, 0.025) * side)
    x0 = int(np.clip(round(cx - side / 2), 0, max(0, w - side)))
    y0 = int(np.clip(round(cy - side / 2), 0, max(0, h - side)))
    flip = bool(rng.integers(0, 2))

    margin = 10.0
    src = np.float32([[0, 0], [OUTPUT_SIZE - 1, 0], [OUTPUT_SIZE - 1, OUTPUT_SIZE - 1], [0, OUTPUT_SIZE - 1]])
    dst = src + rng.uniform(-margin, margin, size=(4, 2)).astype(np.float32)
    perspective = cv2.getPerspectiveTransform(src, dst)
    gamma = float(rng.uniform(0.82, 1.18))
    gains = rng.uniform(0.88, 1.12, size=3).astype(np.float32)
    lut = np.clip((np.arange(256, dtype=np.float32) / 255.0) ** gamma * 255.0, 0, 255).astype(np.uint8)

    resized = []
    for frame in frames:
        crop = frame[y0:y0 + side, x0:x0 + side]
        out = cv2.resize(crop, (OUTPUT_SIZE, OUTPUT_SIZE), interpolation=cv2.INTER_AREA)
        if flip:
            out = cv2.flip(out, 1)
        out = cv2.warpPerspective(out, perspective, (OUTPUT_SIZE, OUTPUT_SIZE),
                                  flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
        out = cv2.LUT(out, lut)
        out = np.clip(out.astype(np.float32) * gains.reshape(1, 1, 3), 0, 255).astype(np.uint8)
        resized.append(out)

    stack = np.stack(resized, axis=0)
    median = np.median(stack, axis=0).astype(np.uint8)
    abstract_background = cv2.GaussianBlur(median, (41, 41), 0)
    abstract_background = (abstract_background // 12) * 12
    output = []
    # The public clip must retain human-action signal while resisting exact-frame
    # retrieval against the named upstream videos.  In addition to the crop and
    # background abstraction above, apply deterministic per-frame sensor jitter,
    # mild down/up-sampling, and a smooth displacement field.  These operations
    # are source-neutral and are reproducible from the hidden transform salt.
    noise_sigma = float(rng.uniform(1.4, 3.6))
    displacement = rng.uniform(-4.0, 4.0, size=(3, 3, 2)).astype(np.float32)
    coarse = cv2.resize(displacement, (OUTPUT_SIZE, OUTPUT_SIZE), interpolation=cv2.INTER_CUBIC)
    yy, xx = np.mgrid[0:OUTPUT_SIZE, 0:OUTPUT_SIZE].astype(np.float32)
    base_map_x = xx + coarse[..., 0]
    base_map_y = yy + coarse[..., 1]
    for idx, frame in enumerate(resized):
        motion = cv2.cvtColor(cv2.absdiff(frame, median), cv2.COLOR_BGR2GRAY)
        motion = cv2.GaussianBlur(motion, (9, 9), 0)
        mask = np.clip((motion.astype(np.float32) - 5.0) / 18.0, 0.0, 1.0)
        mask = cv2.dilate(mask, np.ones((11, 11), np.uint8), iterations=1)
        mask = cv2.GaussianBlur(mask, (15, 15), 0)[..., None]
        softened = np.clip(0.63 * frame.astype(np.float32) + 0.37 * abstract_background.astype(np.float32), 0, 255)
        mixed = mask * frame.astype(np.float32) + (1.0 - mask) * softened
        jitter_x = float(rng.uniform(-2.5, 2.5))
        jitter_y = float(rng.uniform(-2.5, 2.5))
        map_x = np.clip(base_map_x + jitter_x, 0, OUTPUT_SIZE - 1)
        map_y = np.clip(base_map_y + jitter_y, 0, OUTPUT_SIZE - 1)
        mixed = cv2.remap(mixed.astype(np.uint8), map_x, map_y,
                          interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
        if idx % 7 == 3:
            small = cv2.resize(mixed, (128, 128), interpolation=cv2.INTER_AREA)
            mixed = cv2.resize(small, (OUTPUT_SIZE, OUTPUT_SIZE), interpolation=cv2.INTER_LINEAR)
        noise = rng.normal(0.0, noise_sigma, size=mixed.shape).astype(np.float32)
        mixed = np.clip(mixed + noise, 0, 255).astype(np.uint8)
        if idx % 11 == 5:
            mixed = cv2.GaussianBlur(mixed, (3, 3), 0)
        output.append(mixed)
    return output


def _find_ffmpeg() -> str:
    executable = shutil.which("ffmpeg")
    if executable:
        return executable
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except (ImportError, RuntimeError):
        raise RuntimeError("FFmpeg with libx264 is required for deterministic public MP4 creation")


def _encode_mp4(frames: list[np.ndarray], destination: Path, ffmpeg: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_name(destination.name + ".partial.mp4")
    command = [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-fflags", "+bitexact", "-flags:v", "+bitexact",
        "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{OUTPUT_SIZE}x{OUTPUT_SIZE}",
        "-r", str(OUTPUT_FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast",
        "-tune", "fastdecode", "-crf", CRF_VALUE,
        "-x264-params", "keyint=32:min-keyint=32:scenecut=0:open-gop=0:force-cfr=1", "-threads", "1",
        "-pix_fmt", "yuv420p", "-map_metadata", "-1", "-metadata", "title=",
        "-metadata", "comment=", "-movflags", "+faststart", str(partial),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    assert process.stdin is not None
    assert process.stderr is not None
    try:
        for frame in frames:
            process.stdin.write(np.ascontiguousarray(frame).tobytes())
        process.stdin.close()
        error = process.stderr.read().decode("utf-8", errors="replace")
        code = process.wait()
    except Exception:
        process.kill()
        process.wait()
        partial.unlink(missing_ok=True)
        raise
    if code != 0:
        partial.unlink(missing_ok=True)
        raise RuntimeError(f"FFmpeg failed to create a public clip: {error[-600:]}")
    os.replace(partial, destination)
    size = destination.stat().st_size
    if size > MAX_PUBLIC_VIDEO_BYTES:
        destination.unlink(missing_ok=True)
        raise RuntimeError(f"Encoded clip exceeded public size budget: {size}")


def _validate_public_video(path: Path) -> None:
    import cv2
    cap = cv2.VideoCapture(str(path))
    try:
        frames = int(round(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
        width = int(round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
        height = int(round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fps = float(cap.get(cv2.CAP_PROP_FPS))
    finally:
        cap.release()
    if frames != OUTPUT_FRAMES or (width, height) != (OUTPUT_SIZE, OUTPUT_SIZE) or abs(fps - OUTPUT_FPS) > 0.05:
        raise RuntimeError("A prepared public video failed frame/dimension/FPS validation")
    if path.stat().st_size > MAX_PUBLIC_VIDEO_BYTES:
        raise RuntimeError("A prepared public video failed the public size-budget check")


def _decode_source_windows(video: Path, base: str, starts: list[int], destinations: list[Path], ffmpeg: str) -> None:
    import cv2
    cap = cv2.VideoCapture(str(video))
    if not cap.isOpened():
        raise RuntimeError("Could not open an official source video")
    source_fps = float(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(round(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    width = int(round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    height = int(round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    if not (29.5 <= source_fps <= 30.5 and 8970 <= frame_count <= 9020 and width >= 320 and height >= 200):
        cap.release()
        raise RuntimeError("Official video properties do not match the documented five-minute source contract")

    current_index = -1
    current_frame = None
    try:
        for start, destination in zip(starts, destinations):
            chosen = []
            for wanted in _sample_indices(base, start):
                while current_index < wanted:
                    ok, current_frame = cap.read()
                    current_index += 1
                    if not ok or current_frame is None:
                        raise RuntimeError("Official video ended before a requested source frame")
                chosen.append(current_frame.copy())
            transformed = _transform_frames(chosen, base, start)
            _encode_mp4(transformed, destination, ffmpeg)
            _validate_public_video(destination)
    finally:
        cap.release()


def _clean_outputs(public: Path, private: Path) -> None:
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    for path in [public / "train", public / "test"]:
        if path.exists():
            shutil.rmtree(path)
    for path in [public / "train.csv", public / "test.csv", public / "sample_submission.csv",
                 private / "answers.csv"]:
        path.unlink(missing_ok=True)
    (public / "train" / "videos").mkdir(parents=True, exist_ok=True)
    (public / "test" / "videos").mkdir(parents=True, exist_ok=True)


def _sample_graph_from_train(train_rows: list[dict[str, Any]]) -> dict[str, Any]:
    states = Counter()
    starts, ends = [], []
    for row in train_rows:
        graph = json.loads(row["graph_json"])
        for node in graph["nodes"]:
            state = node["state"]
            key = (state["agent"], state["action"], state["context"], tuple(state["roles"]))
            states[key] += 1
            starts.append(node["start"])
            ends.append(node["end"])
    if not states:
        raise RuntimeError("Training split contains no graph nodes")
    agent, action, context, roles = states.most_common(1)[0][0]
    start = int(round(float(np.median(starts))))
    end = max(start, int(round(float(np.median(ends)))))
    return {"nodes": [{"id": 0, "start": start, "end": min(31, end),
                       "state": {"agent": agent, "action": action, "context": context,
                                 "roles": list(roles)}}], "edges": []}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _verify_source_contract(root: Path) -> dict[str, Path]:
    license_path = _find_unique(root, "LICENSE")
    license_text = license_path.read_text(encoding="utf-8", errors="strict")
    if "Creative Commons Attribution 4.0 International" not in license_text:
        raise RuntimeError("Official MEVA license text did not match CC BY 4.0")
    clips_path = _find_unique(root, "list-of-annotated-meva-clips.txt")
    annotated = set(line.strip() for line in clips_path.read_text(encoding="utf-8").splitlines() if line.startswith("2018-"))

    videos: dict[str, Path] = {}
    hashes = set()
    source_bytes = 0
    for base, expected_bytes, _, _, _, _ in SOURCE_SPECS:
        if base not in annotated:
            raise RuntimeError("A selected official video is absent from the official annotated-clip list")
        video = _find_unique(root, _video_name(base))
        if video.stat().st_size != expected_bytes:
            raise RuntimeError("Official source video byte count mismatch")
        digest = _sha256(video)
        if digest in hashes:
            raise RuntimeError("Duplicate official source videos detected")
        hashes.add(digest)
        videos[base] = video
        source_bytes += expected_bytes
        for suffix in ("activities", "types"):
            annotation = _find_unique(root, _annotation_name(base, suffix))
            if annotation.stat().st_size <= 0:
                raise RuntimeError("Official annotation file is empty")
            source_bytes += annotation.stat().st_size
    for required in ["MEVA-Annotation-Definitions.pdf", "KPF-specification-v4.pdf", "activity-names.txt"]:
        source_bytes += _find_unique(root, required).stat().st_size
    if source_bytes >= 1_000_000_000:
        raise RuntimeError("Selected official source upload is not below 1 GB")
    return videos


def prepare(raw: Path, public: Path, private: Path) -> None:
    """Build all derived clips, graphs, groups, splits, and public/private assets."""
    import pandas as pd

    raw, public, private = Path(raw), Path(public), Path(private)
    _clean_outputs(public, private)
    ffmpeg = _find_ffmpeg()
    train_rows: list[dict[str, Any]] = []
    test_rows: list[dict[str, Any]] = []
    answer_rows: list[dict[str, Any]] = []
    all_ids = set()
    total_nodes = total_edges = positive_rows = multi_rows = documented_edges = 0

    split_groups: dict[str, set[str]] = {"train": set(), "test": set()}
    for _, _, split, _, group, _ in SOURCE_SPECS:
        split_groups[split].add(group)
    if split_groups["train"] & split_groups["test"]:
        raise RuntimeError("A strongest-available source group crosses train/test")
    if len(split_groups["train"] | split_groups["test"]) != 15:
        raise RuntimeError("The selected source subset does not provide exactly 15 independent groups")

    with _materialized_raw(raw) as source_root:
        video_paths = _verify_source_contract(source_root)
        decode_jobs: list[tuple[Path, str, list[int], list[Path], str]] = []
        for base, _, split, n_windows, group, _modality in SOURCE_SPECS:
            events = _load_annotations(source_root, base)
            starts = [15 + index * STRIDE_FRAMES for index in _window_indices(n_windows)]
            destinations = []
            local_rows = []
            for start in starts:
                item_id = _public_id(base, start)
                if item_id in all_ids:
                    raise RuntimeError("Opaque public id collision")
                all_ids.add(item_id)
                graph = _graph_for_window(events, start)
                graph_json = _canonical_json(graph)
                video_rel = f"{split}/videos/{item_id}.mp4"
                destination = public / video_rel
                destinations.append(destination)
                row = {"id": item_id, "video": video_rel, "graph_json": graph_json}
                local_rows.append(row)
                total_nodes += len(graph["nodes"])
                total_edges += len(graph["edges"])
                documented_edges += sum(e["type"] == "documented_pair" for e in graph["edges"])
                positive_rows += bool(graph["nodes"])
                multi_rows += len(graph["nodes"]) >= 2
                if split == "train":
                    train_rows.append(row)
                else:
                    test_rows.append({"id": item_id, "video": video_rel})
                    answer_rows.append({"id": item_id, "graph_json": graph_json,
                                        "session_group": group, "event_presence": int(bool(graph["nodes"]))})
            decode_jobs.append((video_paths[base], base, starts, destinations, ffmpeg))

        # Decode/transform/encode independent source videos concurrently. Each
        # ffmpeg worker uses two threads; two workers avoid codec-handle
        # contention on the low-resolution AVI files while remaining well below
        # the 10-core CPU limit and reducing preparation wall time.
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(_decode_source_windows, *job) for job in decode_jobs]
            for job, future in zip(decode_jobs, futures):
                future.result()
                print(f"prepared {job[1]}: {len(job[2])} source-disjoint clips")

    if (len(train_rows), len(test_rows)) != (EXPECTED_TRAIN, EXPECTED_TEST):
        raise RuntimeError("Prepared row counts do not match the frozen challenge contract")
    if positive_rows < 250 or multi_rows < 200 or documented_edges < 80:
        raise RuntimeError("Source-derived graph transition gate failed")

    train_rows.sort(key=lambda row: row["id"])
    test_rows.sort(key=lambda row: row["id"])
    answer_rows.sort(key=lambda row: row["id"])
    if [row["id"] for row in test_rows] != [row["id"] for row in answer_rows]:
        raise RuntimeError("Private/public test alignment failed")
    if set(row["id"] for row in train_rows) & set(row["id"] for row in test_rows):
        raise RuntimeError("Train/test public id overlap")

    group_counts = Counter(row["session_group"] for row in answer_rows)
    if len(group_counts) != 5 or min(group_counts.values()) < MIN_GROUP_TEST:
        raise RuntimeError("Held-out recording-session groups are not statistically supportable")

    # The sample is a source-independent schema dummy: a train-only modal graph alternated
    # with a valid empty graph. It never examines test media or private answers.
    modal_graph_json = _canonical_json(_sample_graph_from_train(train_rows))
    empty_graph_json = _canonical_json({"nodes": [], "edges": []})
    sample_rows = []
    for row in test_rows:
        selector = int(hashlib.sha256(row["id"].encode("utf-8")).hexdigest()[:8], 16) % 2
        sample_rows.append({"id": row["id"], "graph_json": empty_graph_json if selector == 0 else modal_graph_json})

    train_df = pd.DataFrame(train_rows, columns=["id", "video", "graph_json"])
    test_df = pd.DataFrame(test_rows, columns=["id", "video"])
    sample_df = pd.DataFrame(sample_rows, columns=["id", "graph_json"])
    answers_df = pd.DataFrame(answer_rows, columns=["id", "graph_json", "session_group", "event_presence"])
    for frame in [train_df, test_df, sample_df, answers_df]:
        if frame.isna().any().any():
            raise RuntimeError("Prepared output contains missing values")

    train_df.to_csv(public / "train.csv", index=False, lineterminator="\n")
    test_df.to_csv(public / "test.csv", index=False, lineterminator="\n")
    sample_df.to_csv(public / "sample_submission.csv", index=False, lineterminator="\n")
    answers_df.to_csv(private / "answers.csv", index=False, lineterminator="\n")

    for frame in [train_df, test_df]:
        for rel in frame["video"]:
            if not (public / rel).is_file():
                raise RuntimeError("A public CSV video path does not resolve from the public root")
    media_bytes = sum(path.stat().st_size for path in public.rglob("*.mp4"))
    if not (300_000_000 <= media_bytes <= 500_000_000):
        raise RuntimeError(f"Prepared public media is outside the 300-500 MB design band: {media_bytes}")
    print(f"prepared train={len(train_df)} test={len(test_df)} nodes={total_nodes} edges={total_edges}")
    print(f"event_rows={positive_rows} multi_event_rows={multi_rows} documented_pair_edges={documented_edges}")
    print(f"public_media_bytes={media_bytes}")


def _main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw", type=Path)
    parser.add_argument("public", type=Path)
    parser.add_argument("private", type=Path)
    args = parser.parse_args()
    prepare(args.raw, args.public, args.private)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())

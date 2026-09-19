import hashlib
import io
import json
import os
import pickle
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

import cv2
import numpy as np
import pandas as pd


ID_SALT = "robot-controller-trace-recovery-v1"
SPLIT_SEED = 20260717
MIN_GROUP_TEST = 20
VIDEO_SIZE = (160, 120)
TARGET_FPS = 12.0
PREPARED_FRAMES = 48
PADDED_VIDEO_BYTES = 786_432
MAX_SAMPLES = 160
PREPARE_STAGE = int(os.environ.get("PREPARE_STAGE", "4"))

KINDS = {
    "rgb": "avi",
    "depth": "avi",
    "giver_joint_trajectories": "pkl",
    "giver_cartesian_trajectories": "pkl",
    "receiver_joint_trajectories": "pkl",
    "receiver_cartesian_trajectories": "pkl",
}
JOINT_COLUMNS = [f"Panda_joint{i}" for i in range(1, 8)]
CARTESIAN_COLUMNS = ["x", "y", "z", "qx", "qy", "qz", "qw"]


class _PandasCompatUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "pandas.core.indexes.numeric" and name in {"Int64Index", "UInt64Index", "Float64Index"}:
            return pd.Index
        return super().find_class(module, name)


def _stable_hash(text: str) -> str:
    return hashlib.sha256(f"{ID_SALT}:{text}".encode("utf-8")).hexdigest()


def _json(obj) -> str:
    return json.dumps(obj, separators=(",", ":"), sort_keys=True)


def _find_raw_root(raw: Path) -> Path:
    raw = Path(raw)
    candidates = [
        raw,
        raw / "raw_upload",
        raw / "PandaHandover_Real_Val",
        raw / "raw_upload" / "PandaHandover_Real_Val",
    ]
    for cand in candidates:
        if cand.exists() and any(cand.rglob("panda_pyrep_rgb_*.avi")):
            return cand
    return raw


def _find_source_zip(raw: Path):
    raw = Path(raw)
    candidates = []
    if raw.is_file():
        candidates.append(raw)
    elif raw.exists():
        preferred = [
            raw / "PandaHandover_Real_Val.zip",
            raw / "raw_upload" / "PandaHandover_Real_Val.zip",
        ]
        candidates.extend(preferred)
        candidates.extend(p for p in raw.rglob("*") if p.is_file())
    seen = set()
    ordered = []
    for path in candidates:
        try:
            resolved = path.resolve()
        except OSError:
            continue
        if resolved in seen or not path.exists() or not path.is_file():
            continue
        seen.add(resolved)
        ordered.append(path)
    for path in ordered:
        if "PandaHandover_Real_Val" in path.name and zipfile.is_zipfile(path):
            return path
    for path in ordered:
        if zipfile.is_zipfile(path):
            return path
    return None


def _index_members(raw: Path):
    raw = Path(raw)
    source_zip = _find_source_zip(raw)
    if source_zip is not None:
        zf = zipfile.ZipFile(source_zip)
        names = [n for n in zf.namelist() if not n.endswith("/")]

        def read_member(name):
            return zf.read(name)

        source_name = source_zip.name
    else:
        root = _find_raw_root(raw)
        files = [p for p in root.rglob("*") if p.is_file()]
        names = [str(p.relative_to(root)).replace("\\", "/") for p in files]
        file_map = {str(p.relative_to(root)).replace("\\", "/"): p for p in files}

        def read_member(name):
            return file_map[name].read_bytes()

        source_name = root.name

    pattern = re.compile(
        r"(?:^|/)panda_pyrep_(rgb|depth|giver_joint_trajectories|receiver_joint_trajectories|giver_cartesian_trajectories|receiver_cartesian_trajectories)_(\d+)\.(avi|pkl)$"
    )
    groups = {}
    for name in names:
        m = pattern.search(name)
        if not m:
            continue
        kind, sid, ext = m.group(1), m.group(2), m.group(3)
        groups.setdefault(sid, {})[kind] = name
    complete = {sid: g for sid, g in groups.items() if set(g) == set(KINDS)}
    if len(complete) < 80:
        preview = ", ".join(names[:8])
        raise SystemExit(
            f"expected at least 80 complete raw samples, found {len(complete)} in {source_name}; "
            f"first discovered members/files: {preview}"
        )
    return complete, read_member, source_name


def _load_pickle(data: bytes, expected_columns) -> pd.DataFrame:
    obj = _PandasCompatUnpickler(io.BytesIO(data)).load()
    if not isinstance(obj, pd.DataFrame):
        raise ValueError("trajectory pickle is not a DataFrame")
    if list(obj.columns) != list(expected_columns):
        raise ValueError(f"trajectory columns do not match expected schema: {list(obj.columns)}")
    if obj.isna().any().any():
        raise ValueError("trajectory contains NaN")
    return obj.astype(float)


def _read_video_info(data: bytes):
    with tempfile.NamedTemporaryFile(suffix=".avi", delete=False) as tmp:
        tmp.write(data)
        tmp_path = Path(tmp.name)
    cap = cv2.VideoCapture(str(tmp_path))
    if not cap.isOpened():
        tmp_path.unlink(missing_ok=True)
        raise ValueError("could not open video")
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 30.0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    tmp_path.unlink(missing_ok=True)
    return frames, fps, width, height


def _reencode_video(data: bytes, out_path: Path, salt: str, is_depth: bool):
    rng = np.random.default_rng(int(_stable_hash(salt)[:16], 16))
    with tempfile.NamedTemporaryFile(suffix=".avi", delete=False) as tmp:
        tmp.write(data)
        tmp_path = Path(tmp.name)
    cap = cv2.VideoCapture(str(tmp_path))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_count < 8:
        cap.release()
        tmp_path.unlink(missing_ok=True)
        raise ValueError("too few raw video frames")
    target_indices = np.rint(np.linspace(0, frame_count - 1, PREPARED_FRAMES)).astype(int)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(out_path), fourcc, TARGET_FPS, VIDEO_SIZE)
    kept = 0
    crop_scale_x = float(rng.uniform(0.48, 0.72))
    crop_scale_y = float(rng.uniform(0.50, 0.76))
    crop_center_x = float(rng.uniform(0.40, 0.60))
    crop_center_y = float(rng.uniform(0.42, 0.58))
    do_flip = bool(rng.random() < 0.5)
    gain = float(rng.uniform(0.70, 1.30))
    bias = float(rng.uniform(-24, 24))
    gamma = float(rng.uniform(0.70, 1.35))
    angle = float(rng.uniform(-5.0, 5.0))
    scale = float(rng.uniform(0.94, 1.08))
    tx_base = float(rng.uniform(-8.0, 8.0))
    ty_base = float(rng.uniform(-6.0, 6.0))
    drift_phase = float(rng.uniform(0.0, 2.0 * np.pi))
    channel_gain = rng.uniform(0.80, 1.20, size=(1, 1, 3)).astype(np.float32)
    jpeg_quality = int(rng.integers(34, 58))
    last_frame = None
    last_prepared = None
    for out_i, frame_i in enumerate(target_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_i))
        ok, frame = cap.read()
        if not ok and last_frame is None:
            continue
        if not ok:
            frame = last_frame
        last_frame = frame
        h, w = frame.shape[:2]
        crop_w = max(80, int(round(w * crop_scale_x)))
        crop_h = max(70, int(round(h * crop_scale_y)))
        cx = int(round(w * crop_center_x + 12.0 * np.sin(out_i * 0.23 + drift_phase)))
        cy = int(round(h * crop_center_y + 8.0 * np.cos(out_i * 0.19 + drift_phase)))
        x0 = max(0, min(w - crop_w, cx - crop_w // 2))
        x1 = min(w, x0 + crop_w)
        y0 = max(0, min(h - crop_h, cy - crop_h // 2))
        y1 = min(h, y0 + crop_h)
        crop = frame[y0:y1, x0:x1] if x1 > x0 + 50 and y1 > y0 + 50 else frame
        crop = cv2.resize(crop, VIDEO_SIZE, interpolation=cv2.INTER_AREA)
        if do_flip:
            crop = cv2.flip(crop, 1)
        if is_depth:
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            crop = cv2.applyColorMap(gray, cv2.COLORMAP_VIRIDIS)
        center = (VIDEO_SIZE[0] / 2.0, VIDEO_SIZE[1] / 2.0)
        drift = np.sin(out_i * 0.45 + drift_phase)
        affine = cv2.getRotationMatrix2D(center, angle, scale)
        affine[0, 2] += tx_base + 1.15 * drift
        affine[1, 2] += ty_base + 0.75 * np.cos(out_i * 0.37 + drift_phase)
        crop = cv2.warpAffine(
            crop,
            affine,
            VIDEO_SIZE,
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REFLECT_101,
        )
        crop_f = crop.astype(np.float32)
        if not is_depth:
            crop_f *= channel_gain
        crop_f = np.clip(crop_f * gain + bias, 0, 255)
        crop_f = np.power(np.clip(crop_f / 255.0, 0, 1), gamma) * 255.0
        crop = np.clip(crop_f, 0, 255).astype(np.uint8)
        crop = cv2.GaussianBlur(crop, (3, 3), 0)
        noise = rng.normal(0.0, 8.0, crop.shape).astype(np.float32)
        crop = np.clip(crop.astype(np.float32) + noise, 0, 255).astype(np.uint8)
        crop = ((crop // 8) * 8).astype(np.uint8)
        if last_prepared is not None:
            motion = cv2.absdiff(crop, last_prepared)
            motion = cv2.convertScaleAbs(motion, alpha=1.9)
            crop = cv2.addWeighted(crop, 0.66, motion, 0.34, 0)
        last_prepared = crop.copy()
        ok_jpeg, encoded = cv2.imencode(".jpg", crop, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
        if ok_jpeg:
            crop = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
        writer.write(crop)
        kept += 1
    cap.release()
    writer.release()
    tmp_path.unlink(missing_ok=True)
    if kept != PREPARED_FRAMES:
        raise ValueError("could not normalize video to fixed frame count")
    if out_path.stat().st_size > PADDED_VIDEO_BYTES:
        raise ValueError(f"encoded video exceeded fixed padding budget: {out_path.stat().st_size}")
    with out_path.open("ab") as f:
        f.write(b"\0" * (PADDED_VIDEO_BYTES - out_path.stat().st_size))
    return kept


def _interp_rows(df: pd.DataFrame, n_frames: int) -> np.ndarray:
    arr = df.to_numpy(dtype=float)
    if len(arr) == n_frames:
        return arr
    x_old = np.linspace(0.0, 1.0, len(arr))
    x_new = np.linspace(0.0, 1.0, n_frames)
    return np.vstack([np.interp(x_new, x_old, arr[:, j]) for j in range(arr.shape[1])]).T


def _smooth(x, k=5):
    if len(x) < k:
        return x
    kernel = np.ones(k) / k
    return np.convolve(x, kernel, mode="same")


def _speed(arr):
    d = np.diff(arr, axis=0, prepend=arr[[0]])
    return np.linalg.norm(d, axis=1)


def _norm_speed(x):
    p = np.percentile(x, 90) if len(x) else 1.0
    return np.clip(x / max(p, 1e-9), 0, 2)


def _frame_from_index(idx: int, n: int, frames: int) -> int:
    if n <= 1:
        return 0
    return int(round(idx * (frames - 1) / (n - 1)))


def _merge_segments(labels):
    segs = []
    start = 0
    last = labels[0]
    for i, lab in enumerate(labels[1:], 1):
        if lab != last:
            if i - start >= 3:
                segs.append((last, start, i - 1))
            elif segs:
                old = segs[-1]
                segs[-1] = (old[0], old[1], i - 1)
            start = i
            last = lab
    segs.append((last, start, len(labels) - 1))
    return segs[:8]


def _bins_from_xyz(xyz: np.ndarray) -> list:
    mins = np.array([-0.75, -0.85, 0.55])
    maxs = np.array([0.15, 0.35, 1.50])
    bins = np.floor((np.clip(xyz[:3], mins, maxs) - mins) / (maxs - mins + 1e-9) * 10).astype(int)
    return [int(np.clip(v, 0, 9)) for v in bins]


def _joint_bins(vals: np.ndarray) -> list:
    mins = np.array([-3.0] * 7)
    maxs = np.array([3.0] * 7)
    bins = np.floor((np.clip(vals[:7], mins, maxs) - mins) / (maxs - mins + 1e-9) * 4).astype(int)
    return [int(np.clip(v, 0, 3)) for v in bins]


def _coarse_xyz_bins(vals: np.ndarray) -> list:
    fine = np.array(_bins_from_xyz(vals[:3]))
    return [int(np.clip(v // 4, 0, 2)) for v in fine]


def _derive_trace(gj: pd.DataFrame, gc: pd.DataFrame, rj: pd.DataFrame, rc: pd.DataFrame, n_frames: int):
    gj_f = _interp_rows(gj, n_frames)
    gc_f = _interp_rows(gc, n_frames)
    rj_f = _interp_rows(rj, n_frames)
    rc_f = _interp_rows(rc, n_frames)

    gj_s = _norm_speed(_smooth(_speed(gj_f)))
    rj_s = _norm_speed(_smooth(_speed(rj_f)))
    gc_s = _norm_speed(_smooth(_speed(gc_f[:, :3])))
    rc_s = _norm_speed(_smooth(_speed(rc_f[:, :3])))
    giver_s = 0.55 * gj_s + 0.45 * gc_s
    receiver_s = 0.55 * rj_s + 0.45 * rc_s
    both_s = np.maximum(giver_s, receiver_s)
    distance = np.linalg.norm(gc_f[:, :3] - rc_f[:, :3], axis=1)
    min_dist_i = int(np.argmin(distance))

    labels = []
    for i in range(n_frames):
        if abs(i - min_dist_i) <= max(3, n_frames // 18) and both_s[i] < 0.38:
            labels.append(("contact_like_pause", "both"))
        elif both_s[i] < 0.16:
            labels.append(("wait", "both"))
        else:
            arm = "giver" if giver_s[i] > receiver_s[i] * 1.12 else "receiver" if receiver_s[i] > giver_s[i] * 1.12 else "both"
            cart_ratio = max(gc_s[i], rc_s[i]) / max(max(gj_s[i], rj_s[i]), 1e-6)
            mode = "cartesian_move" if cart_ratio > 0.52 else "joint_move"
            labels.append((mode, arm))

    segments = []
    for (mode, arm), s, e in _merge_segments(labels):
        segments.append({"mode": mode, "arm": arm, "start_frame": int(s), "end_frame": int(e)})

    active = np.where(both_s > 0.20)[0]
    start_i = int(active[0]) if len(active) else 0
    stop_i = int(active[-1]) if len(active) else n_frames - 1
    release_i = int(min(n_frames - 1, min_dist_i + max(3, n_frames // 12)))
    events = [
        {"event": "motion_start", "arm": "both", "frame": start_i},
        {"event": "handover_pause", "arm": "both", "frame": min_dist_i},
        {"event": "release_like", "arm": "giver", "frame": release_i},
        {"event": "motion_stop", "arm": "both", "frame": stop_i},
    ]

    waypoint_specs = [
        ("giver", "start", 0, gc_f),
        ("giver", "approach", max(0, min_dist_i - n_frames // 5), gc_f),
        ("giver", "handover", min_dist_i, gc_f),
        ("giver", "retreat", release_i, gc_f),
        ("receiver", "start", 0, rc_f),
        ("receiver", "handover", min_dist_i, rc_f),
        ("receiver", "end", n_frames - 1, rc_f),
    ]
    waypoints = [
        {"arm": arm, "kind": kind, "frame": int(frame), "xyz_bins": _bins_from_xyz(arr[int(frame), :3])}
        for arm, kind, frame, arr in waypoint_specs
    ]
    quality = float(np.clip(0.55 + 0.25 * (np.percentile(both_s, 90) > 0.35) + 0.20 * (distance[min_dist_i] < np.percentile(distance, 25)), 0, 1))
    return segments, waypoints, events, quality


def _state_observation(gj: pd.DataFrame, gc: pd.DataFrame, rj: pd.DataFrame, rc: pd.DataFrame, n_frames: int):
    frames = sorted(set([0, max(0, n_frames // 6), max(0, n_frames // 4), max(0, n_frames // 3)]))
    raw_parts = []
    for frame in frames:
        def sample(df):
            idx = int(round(frame * (len(df) - 1) / max(1, n_frames - 1)))
            return df.iloc[idx].to_numpy(dtype=float)
        gj_vals = sample(gj)
        gc_vals = sample(gc)
        rj_vals = sample(rj)
        rc_vals = sample(rc)
        raw_parts.extend(gj_vals[:7])
        raw_parts.extend(gc_vals[:3])
        raw_parts.extend(rj_vals[:7])
        raw_parts.extend(rc_vals[:3])
    vec = np.asarray(raw_parts, dtype=float)
    rng = np.random.default_rng(9173)
    proj = rng.normal(0, 1, size=(16, len(vec)))
    sketch = np.tanh(proj.dot(vec) / max(1.0, np.sqrt(len(vec))))
    bins = np.floor((sketch + 1.0) * 8.0).astype(int)
    bins = [int(np.clip(v, 0, 15)) for v in bins]
    return _json({"observed_frames": [int(x) for x in frames], "state_sketch_bins": bins, "note": "coarse projected state sketch; not raw trajectory values"})


def _split_ids(source_ids):
    hashed = [(_stable_hash(sid), sid) for sid in source_ids]
    if len({digest for digest, _ in hashed}) != len(hashed):
        raise SystemExit("hash collision while building split IDs")
    ordered = [sid for _, sid in sorted(hashed)]
    rng = np.random.default_rng(SPLIT_SEED)
    rng.shuffle(ordered)
    n_test = max(MIN_GROUP_TEST, int(round(0.25 * len(ordered))))
    test = set(ordered[:n_test])
    return test


def _public_id_map(source_ids):
    hashed = [(_stable_hash("public:" + sid), sid) for sid in source_ids]
    if len({digest for digest, _ in hashed}) != len(hashed):
        raise SystemExit("hash collision while building public IDs")
    tokens = {}
    for _, sid in hashed:
        token = "rctr_x" + _stable_hash("token:" + sid)[:12]
        if token in tokens.values():
            raise SystemExit("public ID token collision")
        tokens[sid] = token
    return tokens


def prepare(raw: Path, public: Path, private: Path) -> None:
    raw = Path(raw)
    public = Path(public)
    private = Path(private)
    if public.resolve() == private.resolve():
        raise SystemExit("public and private outputs must differ")
    shutil.rmtree(public, ignore_errors=True)
    shutil.rmtree(private, ignore_errors=True)
    (public / "train" / "videos").mkdir(parents=True, exist_ok=True)
    (public / "test" / "videos").mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    if PREPARE_STAGE <= 1:
        pd.DataFrame(
            [
                {
                    "id": "debug_stage_1",
                    "rgb_video": "train/videos/debug_rgb.mp4",
                    "depth_video": "train/videos/debug_depth.mp4",
                    "state_observation_json": _json({"observed_frames": [], "state_sketch_bins": []}),
                    "duration_frames": 0,
                    "controller_segments_json": "[]",
                    "key_waypoints_json": "[]",
                    "event_frames_json": "[]",
                    "trace_quality": 0.0,
                }
            ]
        ).to_csv(public / "train.csv", index=False)
        pd.DataFrame(
            [
                {
                    "id": "debug_stage_1",
                    "rgb_video": "test/videos/debug_rgb.mp4",
                    "depth_video": "test/videos/debug_depth.mp4",
                    "state_observation_json": _json({"observed_frames": [], "state_sketch_bins": []}),
                    "duration_frames": 0,
                }
            ]
        ).to_csv(public / "test.csv", index=False)
        pd.DataFrame(
            [
                {
                    "id": "debug_stage_1",
                    "controller_segments_json": "[]",
                    "key_waypoints_json": "[]",
                    "event_frames_json": "[]",
                    "trace_quality": 0.0,
                }
            ]
        ).to_csv(private / "answers.csv", index=False)
        pd.DataFrame(
            [
                {
                    "id": "debug_stage_1",
                    "controller_segments_json": "[]",
                    "key_waypoints_json": "[]",
                    "event_frames_json": "[]",
                    "confidence": 0.0,
                }
            ]
        ).to_csv(public / "sample_submission.csv", index=False)
        (private / "prepare_metadata.json").write_text(_json({"debug_stage": 1}), encoding="utf-8")
        return

    groups, read_member, source_name = _index_members(raw)
    if PREPARE_STAGE <= 2:
        summary = {
            "debug_stage": 2,
            "source_name": source_name,
            "complete_samples": len(groups),
            "selected_samples": min(len(groups), MAX_SAMPLES or len(groups)),
            "first_source_ids": sorted(groups)[:5],
        }
        (private / "prepare_metadata.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        pd.DataFrame([summary]).to_csv(public / "raw_index_summary.csv", index=False)
        return
    source_ids = sorted(groups)
    if MAX_SAMPLES:
        source_ids = source_ids[:MAX_SAMPLES]
    test_ids = _split_ids(source_ids)
    if len(test_ids) < MIN_GROUP_TEST:
        raise SystemExit("test split below MIN_GROUP_TEST")
    id_map = _public_id_map(source_ids)
    train_rows, test_rows, answer_rows, source_map_rows = [], [], [], []

    for raw_id in source_ids:
        members = groups[raw_id]
        gj = _load_pickle(read_member(members["giver_joint_trajectories"]), JOINT_COLUMNS)
        gc = _load_pickle(read_member(members["giver_cartesian_trajectories"]), CARTESIAN_COLUMNS)
        rj = _load_pickle(read_member(members["receiver_joint_trajectories"]), JOINT_COLUMNS)
        rc = _load_pickle(read_member(members["receiver_cartesian_trajectories"]), CARTESIAN_COLUMNS)
        raw_rgb = read_member(members["rgb"])
        raw_depth = read_member(members["depth"])
        raw_frames, fps, _, _ = _read_video_info(raw_rgb)
        if raw_frames < 20:
            continue
        subset = "test" if raw_id in test_ids else "train"
        pid = id_map[raw_id]
        source_map_rows.append({"id": pid, "raw_id": raw_id, "subset": subset})
        rgb_path = f"{subset}/videos/{pid}_rgb.mp4"
        depth_path = f"{subset}/videos/{pid}_depth.mp4"
        if PREPARE_STAGE <= 3:
            n_frames = PREPARED_FRAMES
        else:
            rgb_frames = _reencode_video(raw_rgb, public / rgb_path, pid + ":rgb", False)
            depth_frames = _reencode_video(raw_depth, public / depth_path, pid + ":depth", True)
            n_frames = min(rgb_frames, depth_frames)
        segments, waypoints, events, quality = _derive_trace(gj, gc, rj, rc, n_frames)
        base = {
            "id": pid,
            "rgb_video": rgb_path,
            "depth_video": depth_path,
            "state_observation_json": _state_observation(gj, gc, rj, rc, n_frames),
            "duration_frames": int(n_frames),
        }
        label = {
            "controller_segments_json": _json(segments),
            "key_waypoints_json": _json(waypoints),
            "event_frames_json": _json(events),
            "trace_quality": round(quality, 4),
        }
        if subset == "train":
            train_rows.append({**base, **label})
        else:
            test_rows.append(base)
            answer_rows.append({"id": pid, **label})

    if len(train_rows) < 50 or len(test_rows) < MIN_GROUP_TEST:
        raise SystemExit("prepared split too small")
    train = pd.DataFrame(train_rows).sort_values("id").reset_index(drop=True)
    test = pd.DataFrame(test_rows).sort_values("id").reset_index(drop=True)
    answers = pd.DataFrame(answer_rows).sort_values("id").reset_index(drop=True)
    source_map = pd.DataFrame(source_map_rows).sort_values("id").reset_index(drop=True)
    for df_name, df in [("train", train), ("test", test), ("answers", answers), ("source_map", source_map)]:
        if df.isna().any().any():
            raise SystemExit(f"{df_name} contains missing values")

    train.to_csv(public / "train.csv", index=False)
    test.to_csv(public / "test.csv", index=False)
    answers.to_csv(private / "answers.csv", index=False)
    source_map.to_csv(private / "source_map.csv", index=False)
    if PREPARE_STAGE <= 3:
        pd.DataFrame(
            {
                "id": test["id"],
                "controller_segments_json": "[]",
                "key_waypoints_json": "[]",
                "event_frames_json": "[]",
                "confidence": 0.0,
            }
        ).to_csv(public / "sample_submission.csv", index=False)
        metadata = {
            "debug_stage": 3,
            "source_name": source_name,
            "n_train": int(len(train)),
            "n_test": int(len(test)),
            "videos_encoded": False,
        }
        (private / "prepare_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        return

    def sample_interval_iou(a0, a1, b0, b1):
        inter = max(0, min(a1, b1) - max(a0, b0) + 1)
        union = max(a1, b1) - min(a0, b0) + 1
        return inter / union if union else 0.0

    def sample_match_f1(pred, gold, item_score):
        if not pred and not gold:
            return 1.0
        if not pred or not gold:
            return 0.0
        scores = []
        for i, p in enumerate(pred):
            for j, g in enumerate(gold):
                s = item_score(p, g)
                if s > 0:
                    scores.append((s, i, j))
        scores.sort(reverse=True)
        used_p, used_g, total = set(), set(), 0.0
        for s, i, j in scores:
            if i in used_p or j in used_g:
                continue
            used_p.add(i)
            used_g.add(j)
            total += s
        precision = total / max(1, len(pred))
        recall = total / max(1, len(gold))
        return 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)

    def sample_segment_score(p, g):
        if p.get("mode") != g.get("mode") or p.get("arm") != g.get("arm"):
            return 0.0
        iou = sample_interval_iou(int(p["start_frame"]), int(p["end_frame"]), int(g["start_frame"]), int(g["end_frame"]))
        if iou < 0.55:
            return 0.0
        boundary = max(
            0.0,
            1.0 - (abs(p["start_frame"] - g["start_frame"]) + abs(p["end_frame"] - g["end_frame"])) / 12.0,
        )
        return 0.75 * iou + 0.25 * boundary

    def sample_event_score(p, g):
        if p.get("event") != g.get("event") or p.get("arm") != g.get("arm"):
            return 0.0
        return max(0.0, 1.0 - abs(int(p["frame"]) - int(g["frame"])) / 5.0)

    def best_training_template(column, item_score):
        parsed = [json.loads(x) for x in train[column].astype(str)]
        unique = []
        seen = set()
        for item in parsed:
            key = _json(item)
            if key not in seen:
                seen.add(key)
                unique.append(item)
        best_item, best_score = unique[0], -1.0
        for cand in unique:
            score = float(np.mean([sample_match_f1(cand, gold, item_score) for gold in parsed]))
            if score > best_score:
                best_item, best_score = cand, score
        return best_item

    sample_segments = best_training_template("controller_segments_json", sample_segment_score)
    sample_events = best_training_template("event_frames_json", sample_event_score)

    sample = pd.DataFrame(
        {
            "id": test["id"],
            "controller_segments_json": [_json(sample_segments) for _ in test["id"]],
            "key_waypoints_json": "[]",
            "event_frames_json": [_json(sample_events) for _ in test["id"]],
            "confidence": 0.22,
        }
    )
    sample.to_csv(public / "sample_submission.csv", index=False)
    metadata = {
        "source_name": source_name,
        "n_train": int(len(train)),
        "n_test": int(len(test)),
        "raw_source_ids_stripped": True,
        "gripper_state_available": False,
    }
    (private / "prepare_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("raw", type=Path)
    parser.add_argument("public", type=Path)
    parser.add_argument("private", type=Path)
    args = parser.parse_args()
    prepare(args.raw, args.public, args.private)


if __name__ == "__main__":
    main()

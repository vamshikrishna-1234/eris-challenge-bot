#!/usr/bin/env python3
"""Prepare the Headset Visual-Inertial Tracking Failure Ledger challenge."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import zipfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


ID_SALT = "hvit_failure_ledger_v3_cpu_real_split"
MIN_GROUP_TEST = 20
WINDOW = 18
STRIDE = 2
PANEL_FRAME_IX = [0, 5, 11, 17]
PANEL_PAD_BYTES = 18000
PROMPT = "Audit this headset tracking window and submit a failure/repair ledger."

SEQ_META = {
    "MIO09_short_1_updown": {
        "device": "dual_wide",
        "motion": "vertical_scan",
        "split": "train",
        "zip": "MIO09_short_1_updown.zip",
    },
    "MIO10_short_2_panorama": {
        "device": "dual_wide",
        "motion": "rotation_scan",
        "split": "train",
        "zip": "MIO10_short_2_panorama.zip",
    },
    "MIO11_short_3_backandforth": {
        "device": "dual_wide",
        "motion": "translation_return",
        "split": "test",
        "zip": "MIO11_short_3_backandforth.zip",
    },
    "MGO09_short_1_updown": {
        "device": "quad_compact",
        "motion": "vertical_scan",
        "split": "train",
        "zip": "MGO09_short_1_updown.zip",
    },
    "MGO10_short_2_panorama": {
        "device": "quad_compact",
        "motion": "rotation_scan",
        "split": "test",
        "zip": "MGO10_short_2_panorama.zip",
    },
}


@dataclass
class WindowRecord:
    scene_key: str
    split: str
    source_seq: str
    device: str
    motion: str
    start: int
    cam_names: list[str]
    cam_ts: np.ndarray
    pos: np.ndarray
    quat: np.ndarray
    gyro_mean: np.ndarray
    gyro_max: np.ndarray
    acc_dev: np.ndarray
    visual_blur: np.ndarray
    visual_delta: np.ndarray
    degraded: list[dict]
    reliable: list[int]
    spans: list[dict]
    anchors: list[dict]
    failure_type: str
    uncertainty: float


def _read_zip_csv(z: zipfile.ZipFile, member: str) -> pd.DataFrame:
    with z.open(member) as f:
        df = pd.read_csv(f)
    first = df.columns[0]
    if first.startswith("#timestamp"):
        df = df.rename(columns={first: "timestamp"})
    return df


def _read_folder_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    first = df.columns[0]
    if first.startswith("#timestamp"):
        df = df.rename(columns={first: "timestamp"})
    return df


def _find_raw_dir(raw_dir: Path) -> Path:
    candidates = [
        raw_dir,
        raw_dir / "raw_upload",
        raw_dir / "raw_sources",
        raw_dir / "raw_data",
    ]
    for c in candidates:
        if c.exists() and (
            any((c / meta["zip"]).exists() for meta in SEQ_META.values())
            or any((c / seq / "mav0").exists() for seq in SEQ_META)
        ):
            return c
    raise SystemExit(
        "Could not find official Monado source ZIPs. Expected them directly under "
        f"{raw_dir}, {raw_dir / 'raw_upload'}, or {raw_dir / 'raw_sources'}."
    )


def _json_dumps(obj) -> str:
    return json.dumps(obj, separators=(",", ":"), sort_keys=True)


def _stable_int(key: str) -> int:
    return int.from_bytes(hashlib.sha256(key.encode()).digest()[:8], "big")


def _row_id(scene_key: str) -> str:
    return "hvit_" + hashlib.sha256(f"{ID_SALT}:{scene_key}".encode()).hexdigest()[:18]


def _global_id_map(keys: list[str]) -> dict[str, str]:
    scene_hash = pd.Series(keys, dtype=str)
    assert scene_hash.is_unique
    hashed = [(hashlib.sha256(f"{ID_SALT}:id:{k}".encode()).hexdigest(), k) for k in scene_hash.tolist()]
    assert len({h for h, _ in hashed}) == len(hashed)
    return {k: _row_id(k) for _, k in sorted(hashed)}


def _assert_no_missing_raw(df: pd.DataFrame, label: str) -> None:
    if df.isna().any().any():
        raise SystemExit(f"{label}: raw CSV contains NaN")
    object_cols = [c for c in df.columns if df[c].dtype == object]
    obj = df[object_cols]
    if object_cols and obj.apply(lambda col: col.astype(str).str.strip().eq("")).any().any():
        raise SystemExit(f"{label}: raw CSV contains blank string values")


def _norm_rows(arr: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(arr, axis=1, keepdims=True)
    n[n == 0] = 1.0
    return arr / n


def _quat_angle(q: np.ndarray) -> np.ndarray:
    qn = _norm_rows(q)
    dots = np.abs(np.sum(qn[1:] * qn[:-1], axis=1))
    dots = np.clip(dots, -1.0, 1.0)
    return np.concatenate([[0.0], 2.0 * np.arccos(dots)])


def _yaw_from_quat(q: np.ndarray) -> np.ndarray:
    qn = _norm_rows(q)
    w, x, y, z = qn[:, 0], qn[:, 1], qn[:, 2], qn[:, 3]
    return np.arctan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))


def _interp_pose(gt: pd.DataFrame, ts: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    t = gt["timestamp"].to_numpy(dtype=np.float64)
    pos_cols = [" p_RS_R_x [m]", " p_RS_R_y [m]", " p_RS_R_z [m]"]
    quat_cols = [" q_RS_w []", " q_RS_x []", " q_RS_y []", " q_RS_z []"]
    pos = np.column_stack([np.interp(ts, t, gt[c].to_numpy(dtype=np.float64)) for c in pos_cols])
    quat = np.column_stack([np.interp(ts, t, gt[c].to_numpy(dtype=np.float64)) for c in quat_cols])
    quat = _norm_rows(quat)
    return pos, quat


def _aggregate_imu(imu: pd.DataFrame, ts: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    it = imu["timestamp"].to_numpy(dtype=np.int64)
    gyro = imu[["w_RS_S_x [rad s^-1]", "w_RS_S_y [rad s^-1]", "w_RS_S_z [rad s^-1]"]].to_numpy(float)
    acc = imu[["a_RS_S_x [m s^-2]", "a_RS_S_y [m s^-2]", "a_RS_S_z [m s^-2]"]].to_numpy(float)
    gyro_norm = np.linalg.norm(gyro, axis=1)
    acc_dev = np.abs(np.linalg.norm(acc, axis=1) - 9.80665)
    mean_v, max_v, acc_v = [], [], []
    for i, t0 in enumerate(ts):
        t1 = ts[min(i + 1, len(ts) - 1)] if i < len(ts) - 1 else t0 + int(np.median(np.diff(ts)))
        mask = (it >= t0) & (it < t1)
        if not mask.any():
            j = int(np.argmin(np.abs(it - t0)))
            vals = gyro_norm[j : j + 1]
            avals = acc_dev[j : j + 1]
        else:
            vals = gyro_norm[mask]
            avals = acc_dev[mask]
        mean_v.append(float(np.mean(vals)))
        max_v.append(float(np.max(vals)))
        acc_v.append(float(np.mean(avals)))
    return np.asarray(mean_v), np.asarray(max_v), np.asarray(acc_v)


def _image_stats(z: zipfile.ZipFile, member: str) -> tuple[float, Image.Image]:
    with z.open(member) as f:
        img = Image.open(f).convert("L")
        img.load()
    small = ImageOps.autocontrast(img.resize((96, 72), Image.Resampling.BILINEAR))
    edge = small.filter(ImageFilter.FIND_EDGES)
    arr = np.asarray(edge, dtype=np.float32) / 255.0
    return float(np.var(arr)), img


def _image_stats_path(path: Path) -> tuple[float, Image.Image]:
    img = Image.open(path).convert("L")
    img.load()
    small = ImageOps.autocontrast(img.resize((96, 72), Image.Resampling.BILINEAR))
    edge = small.filter(ImageFilter.FIND_EDGES)
    arr = np.asarray(edge, dtype=np.float32) / 255.0
    return float(np.var(arr)), img


def _blend_motion_context(images: list[Image.Image]) -> Image.Image:
    arrays = [np.asarray(img.convert("L"), dtype=np.float32) for img in images]
    if len(arrays) == 1:
        blended = arrays[0]
    elif len(arrays) == 2:
        blended = 0.65 * arrays[0] + 0.35 * arrays[1]
    else:
        blended = 0.55 * arrays[1] + 0.225 * arrays[0] + 0.225 * arrays[2]
    return Image.fromarray(np.clip(blended, 0, 255).astype(np.uint8), mode="L")


def _read_zip_image(z: zipfile.ZipFile, member: str) -> Image.Image:
    with z.open(member) as f:
        img = Image.open(f).convert("L")
        img.load()
    return img


def _read_folder_image(path: Path) -> Image.Image:
    img = Image.open(path).convert("L")
    img.load()
    return img


def _make_tile(img: Image.Image, key: str) -> Image.Image:
    rng = np.random.default_rng(_stable_int(key))
    w, h = img.size
    crop_w = int(w * 0.56)
    crop_h = int(h * 0.56)
    max_x = max(1, w - crop_w)
    max_y = max(1, h - crop_h)
    left = int(rng.integers(0, max_x))
    top = int(rng.integers(0, max_y))
    tile = img.crop((left, top, left + crop_w, top + crop_h))
    fill = int(np.asarray(tile, dtype=np.uint8).mean())
    tile = tile.rotate(float(rng.uniform(-2.8, 2.8)), resample=Image.Resampling.BILINEAR, expand=False, fillcolor=fill)
    tile = ImageOps.autocontrast(tile)
    tile = ImageEnhance.Contrast(tile).enhance(float(rng.uniform(0.82, 1.28)))
    tile = ImageEnhance.Brightness(tile).enhance(float(rng.uniform(0.88, 1.14)))
    tile = tile.filter(ImageFilter.GaussianBlur(radius=float(rng.uniform(0.65, 1.1))))
    tile = tile.resize((88, 66), Image.Resampling.BILINEAR).resize((160, 120), Image.Resampling.BILINEAR)
    arr = np.asarray(tile, dtype=np.float32)
    arr += rng.normal(0.0, float(rng.uniform(7.0, 11.0)), arr.shape)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), mode="L")


def _save_panel(z: zipfile.ZipFile, top: str, row: pd.Series, rec: WindowRecord, out_path: Path) -> None:
    tiles = []
    for local_ix in PANEL_FRAME_IX:
        ctx = []
        for ctx_ix in sorted({max(0, local_ix - 1), local_ix, min(len(rec.cam_names) - 1, local_ix + 1)}):
            fname = rec.cam_names[ctx_ix]
            member = f"{top}/mav0/cam0/data/{fname}"
            ctx.append(_read_zip_image(z, member))
        img = _blend_motion_context(ctx)
        tiles.append(_make_tile(img, f"{rec.scene_key}:panel:{local_ix}"))
    panel = Image.new("L", (320, 240), color=0)
    panel.paste(tiles[0], (0, 0))
    panel.paste(tiles[1], (160, 0))
    panel.paste(tiles[2], (0, 120))
    panel.paste(tiles[3], (160, 120))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    panel.save(out_path, format="JPEG", quality=68, optimize=True)
    _pad_panel_file(out_path)


def _save_panel_folder(seq_dir: Path, rec: WindowRecord, out_path: Path) -> None:
    tiles = []
    for local_ix in PANEL_FRAME_IX:
        ctx = []
        for ctx_ix in sorted({max(0, local_ix - 1), local_ix, min(len(rec.cam_names) - 1, local_ix + 1)}):
            fname = rec.cam_names[ctx_ix]
            ctx.append(_read_folder_image(seq_dir / "mav0" / "cam0" / "data" / fname))
        img = _blend_motion_context(ctx)
        tiles.append(_make_tile(img, f"{rec.scene_key}:panel:{local_ix}"))
    panel = Image.new("L", (320, 240), color=0)
    panel.paste(tiles[0], (0, 0))
    panel.paste(tiles[1], (160, 0))
    panel.paste(tiles[2], (0, 120))
    panel.paste(tiles[3], (160, 120))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    panel.save(out_path, format="JPEG", quality=68, optimize=True)
    _pad_panel_file(out_path)


def _pad_panel_file(path: Path) -> None:
    size = path.stat().st_size
    if size > PANEL_PAD_BYTES:
        raise SystemExit(f"panel file exceeds fixed padding budget: {path} has {size} bytes")
    if size < PANEL_PAD_BYTES:
        with path.open("ab") as f:
            f.write(b"\0" * (PANEL_PAD_BYTES - size))


def _contiguous_spans(mask: np.ndarray, span_types: list[str], severity: np.ndarray) -> list[dict]:
    spans = []
    i = 0
    while i < len(mask):
        if not mask[i]:
            i += 1
            continue
        j = i
        while j + 1 < len(mask) and mask[j + 1]:
            j += 1
        labels = span_types[i : j + 1]
        typ = max(sorted(set(labels)), key=labels.count)
        spans.append(
            {
                "start": int(i),
                "end": int(j),
                "type": typ,
                "severity": round(float(np.clip(np.mean(severity[i : j + 1]), 0.0, 1.0)), 3),
            }
        )
        i = j + 1
    return spans[:3]


def _build_degraded_and_targets(
    scene_key: str,
    pos: np.ndarray,
    quat: np.ndarray,
    gyro_max: np.ndarray,
    acc_dev: np.ndarray,
    visual_blur: np.ndarray,
    visual_delta: np.ndarray,
    motion: str,
) -> tuple[list[dict], list[int], list[dict], list[dict], str, float]:
    rng = np.random.default_rng(_stable_int(scene_key))
    rel_pos = pos - pos[0]
    yaw = _yaw_from_quat(quat)
    yaw = np.unwrap(yaw - yaw[0])
    step = np.concatenate([[0.0], np.linalg.norm(np.diff(rel_pos, axis=0), axis=1)])
    rot = _quat_angle(quat)
    stress = (
        0.38 * (gyro_max / (np.percentile(gyro_max, 85) + 1e-6))
        + 0.22 * (acc_dev / (np.percentile(acc_dev, 85) + 1e-6))
        + 0.20 * (visual_delta / (np.percentile(visual_delta, 85) + 1e-6))
        + 0.20 * (step / (np.percentile(step, 85) + 1e-6))
    )
    stress = np.clip(stress, 0.0, 2.0)
    stress_norm = np.clip(stress / 1.4, 0.0, 1.0)

    drift_axis = np.asarray([math.cos(rng.uniform(-math.pi, math.pi)), math.sin(rng.uniform(-math.pi, math.pi)), rng.uniform(-0.3, 0.3)])
    drift_axis = drift_axis / (np.linalg.norm(drift_axis) + 1e-9)
    start_candidates = np.arange(4, WINDOW - 4)
    weights = stress_norm[start_candidates] + 0.15
    drift_start = int(rng.choice(start_candidates, p=weights / weights.sum()))
    family_gain = {"vertical_scan": 0.78, "rotation_scan": 1.05, "translation_return": 1.18}[motion]
    stress_gain = float(np.mean(np.sort(stress_norm)[-5:]))
    total_drift = family_gain * (0.035 + 0.16 * stress_gain + 0.045 * rng.random())
    lost_threshold = 0.70 if motion != "vertical_scan" else 0.82
    lost_mask = (stress_norm > lost_threshold) & (visual_blur < np.percentile(visual_blur, 55))
    if lost_mask.sum() < 2 and stress_gain > 0.58:
        lost_mask[drift_start : min(WINDOW, drift_start + int(rng.integers(2, 5)))] = True

    degraded = []
    degraded_pos = rel_pos.copy()
    degraded_yaw = yaw.copy()
    for k in range(WINDOW):
        frac = max(0.0, (k - drift_start + 1) / max(1, WINDOW - drift_start))
        wobble = 0.008 * np.asarray([math.sin(k * 0.7), math.cos(k * 0.53), math.sin(k * 0.31)])
        degraded_pos[k] = rel_pos[k] + drift_axis * total_drift * frac + wobble * stress_norm[k]
        degraded_yaw[k] = yaw[k] + (0.06 + 0.16 * stress_gain) * frac + 0.015 * math.sin(k)
        observed = not bool(lost_mask[k])
        if observed:
            degraded.append(
                {
                    "k": int(k),
                    "x": round(float(degraded_pos[k, 0]), 4),
                    "y": round(float(degraded_pos[k, 1]), 4),
                    "z": round(float(degraded_pos[k, 2]), 4),
                    "yaw": round(float(degraded_yaw[k]), 4),
                    "observed": True,
                }
            )
        else:
            degraded.append({"k": int(k), "observed": False})

    pos_error = np.linalg.norm(degraded_pos - rel_pos, axis=1)
    yaw_error = np.abs(degraded_yaw - yaw)
    severity = np.clip((pos_error / 0.17) + (yaw_error / 0.42) + 0.25 * lost_mask.astype(float), 0.0, 1.0)
    unreliable = lost_mask | (pos_error > 0.070) | ((pos_error > 0.048) & (stress_norm > 0.55))
    reliable_mask = (~unreliable) & (visual_blur >= np.percentile(visual_blur, 30))
    reliable = [int(k) for k in range(WINDOW) if reliable_mask[k]]
    if len(reliable) > 7:
        keep = np.linspace(0, len(reliable) - 1, 7).round().astype(int)
        reliable = [reliable[i] for i in sorted(set(keep))]
    if not reliable:
        reliable = [int(np.argmin(pos_error + 0.2 * stress_norm))]

    span_types = []
    for k in range(WINDOW):
        if lost_mask[k]:
            span_types.append("lost_tracking")
        elif k > drift_start and k > 2 and pos_error[k] < max(0.055, pos_error[k - 1] * 0.72):
            span_types.append("relocalized")
        elif pos_error[k] > 0.050:
            span_types.append("drift")
        else:
            span_types.append("uncertain")
    spans = _contiguous_spans(unreliable, span_types, severity)

    anchors = []
    for sp in spans:
        current = min(WINDOW - 1, int(sp["end"]) + 1)
        earlier = [r for r in reliable if r < int(sp["start"])]
        if not earlier:
            continue
        distances = [(np.linalg.norm(rel_pos[current] - rel_pos[a]) + 0.08 * abs(yaw[current] - yaw[a]), a) for a in earlier]
        anchor = int(min(distances)[1])
        if current != anchor:
            anchors.append({"current": int(current), "anchor": anchor})
    if len(anchors) > 2:
        anchors = anchors[:2]

    if not spans:
        ftype = "ok"
    elif any(sp["type"] == "lost_tracking" for sp in spans):
        ftype = "lost_tracking"
    elif any(sp["type"] == "relocalized" for sp in spans) and anchors:
        ftype = "relocalized"
    elif float(np.mean(pos_error)) > 0.060 or float(np.max(pos_error)) > 0.13:
        ftype = "drift"
    else:
        ftype = "uncertain"
    uncertainty = float(np.clip(0.12 + 0.50 * np.mean(severity) + 0.28 * np.mean(stress_norm) + 0.10 * np.mean(lost_mask), 0, 1))
    return degraded, reliable, spans, anchors, ftype, round(uncertainty, 4)


def _records_from_zip(zip_path: Path) -> list[WindowRecord]:
    seq = zip_path.stem
    meta = SEQ_META[seq]
    records = []
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
        top = seq
        gt = _read_zip_csv(z, f"{top}/mav0/gt/data.csv")
        imu = _read_zip_csv(z, f"{top}/mav0/imu0/data.csv")
        cam = _read_zip_csv(z, f"{top}/mav0/cam0/data.csv").sort_values("timestamp").reset_index(drop=True)
        needed = {"timestamp", "filename"}
        if not needed.issubset(cam.columns):
            raise SystemExit(f"{zip_path.name}: missing camera columns")
        _assert_no_missing_raw(gt, f"{zip_path.name}:gt")
        _assert_no_missing_raw(imu, f"{zip_path.name}:imu")
        _assert_no_missing_raw(cam, f"{zip_path.name}:cam")
        ts_all = cam["timestamp"].to_numpy(dtype=np.int64)
        pos_all, quat_all = _interp_pose(gt, ts_all.astype(np.float64))
        gyro_mean_all, gyro_max_all, acc_dev_all = _aggregate_imu(imu, ts_all)
        blur_all = []
        delta_all = []
        prev = None
        for fname in cam["filename"].astype(str).tolist():
            member = f"{top}/mav0/cam0/data/{Path(fname).name}"
            blur, img = _image_stats(z, member)
            small = np.asarray(img.resize((32, 24), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
            blur_all.append(blur)
            delta_all.append(0.0 if prev is None else float(np.mean(np.abs(small - prev))))
            prev = small
        blur_all = np.asarray(blur_all)
        delta_all = np.asarray(delta_all)
        for start in range(0, len(cam) - WINDOW + 1, STRIDE):
            scene_key = f"{seq}:{start}:{WINDOW}"
            sl = slice(start, start + WINDOW)
            degraded, reliable, spans, anchors, ftype, uncertainty = _build_degraded_and_targets(
                scene_key,
                pos_all[sl],
                quat_all[sl],
                gyro_max_all[sl],
                acc_dev_all[sl],
                blur_all[sl],
                delta_all[sl],
                meta["motion"],
            )
            records.append(
                WindowRecord(
                    scene_key=scene_key,
                    split=meta["split"],
                    source_seq=seq,
                    device=meta["device"],
                    motion=meta["motion"],
                    start=start,
                    cam_names=[Path(x).name for x in cam.loc[sl, "filename"].astype(str).tolist()],
                    cam_ts=ts_all[sl],
                    pos=pos_all[sl],
                    quat=quat_all[sl],
                    gyro_mean=gyro_mean_all[sl],
                    gyro_max=gyro_max_all[sl],
                    acc_dev=acc_dev_all[sl],
                    visual_blur=blur_all[sl],
                    visual_delta=delta_all[sl],
                    degraded=degraded,
                    reliable=reliable,
                    spans=spans,
                    anchors=anchors,
                    failure_type=ftype,
                    uncertainty=uncertainty,
                )
            )
    return records


def _records_from_folder(seq_dir: Path) -> list[WindowRecord]:
    seq = seq_dir.name
    meta = SEQ_META[seq]
    records = []
    gt = _read_folder_csv(seq_dir / "mav0" / "gt" / "data.csv")
    imu = _read_folder_csv(seq_dir / "mav0" / "imu0" / "data.csv")
    cam = _read_folder_csv(seq_dir / "mav0" / "cam0" / "data.csv").sort_values("timestamp").reset_index(drop=True)
    needed = {"timestamp", "filename"}
    if not needed.issubset(cam.columns):
        raise SystemExit(f"{seq}: missing camera columns")
    _assert_no_missing_raw(gt, f"{seq}:gt")
    _assert_no_missing_raw(imu, f"{seq}:imu")
    _assert_no_missing_raw(cam, f"{seq}:cam")
    ts_all = cam["timestamp"].to_numpy(dtype=np.int64)
    pos_all, quat_all = _interp_pose(gt, ts_all.astype(np.float64))
    gyro_mean_all, gyro_max_all, acc_dev_all = _aggregate_imu(imu, ts_all)
    blur_all = []
    delta_all = []
    prev = None
    for fname in cam["filename"].astype(str).tolist():
        blur, img = _image_stats_path(seq_dir / "mav0" / "cam0" / "data" / Path(fname).name)
        small = np.asarray(img.resize((32, 24), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
        blur_all.append(blur)
        delta_all.append(0.0 if prev is None else float(np.mean(np.abs(small - prev))))
        prev = small
    blur_all = np.asarray(blur_all)
    delta_all = np.asarray(delta_all)
    for start in range(0, len(cam) - WINDOW + 1, STRIDE):
        scene_key = f"{seq}:{start}:{WINDOW}"
        sl = slice(start, start + WINDOW)
        degraded, reliable, spans, anchors, ftype, uncertainty = _build_degraded_and_targets(
            scene_key,
            pos_all[sl],
            quat_all[sl],
            gyro_max_all[sl],
            acc_dev_all[sl],
            blur_all[sl],
            delta_all[sl],
            meta["motion"],
        )
        records.append(
            WindowRecord(
                scene_key=scene_key,
                split=meta["split"],
                source_seq=seq,
                device=meta["device"],
                motion=meta["motion"],
                start=start,
                cam_names=[Path(x).name for x in cam.loc[sl, "filename"].astype(str).tolist()],
                cam_ts=ts_all[sl],
                pos=pos_all[sl],
                quat=quat_all[sl],
                gyro_mean=gyro_mean_all[sl],
                gyro_max=gyro_max_all[sl],
                acc_dev=acc_dev_all[sl],
                visual_blur=blur_all[sl],
                visual_delta=delta_all[sl],
                degraded=degraded,
                reliable=reliable,
                spans=spans,
                anchors=anchors,
                failure_type=ftype,
                uncertainty=uncertainty,
            )
        )
    return records


def _imu_trace_json(rec: WindowRecord) -> str:
    vals = []
    for k in range(WINDOW):
        vals.append(
            {
                "k": k,
                "gyro_mean": round(float(rec.gyro_mean[k]), 5),
                "gyro_peak": round(float(rec.gyro_max[k]), 5),
                "acc_dev": round(float(rec.acc_dev[k]), 5),
                "frame_delta": round(float(rec.visual_delta[k]), 5),
            }
        )
    return _json_dumps(vals)


def _meta_json(rec: WindowRecord) -> str:
    return _json_dumps(
        {
            "device_family": rec.device,
            "motion_hint": rec.motion,
            "keyframe_count": WINDOW,
            "panel_order": "top_left,top_right,bottom_left,bottom_right",
        }
    )


def _make_sample(train_df: pd.DataFrame, test_df: pd.DataFrame) -> pd.DataFrame:
    majority_type = str(train_df["failure_type"].mode().iloc[0])
    median_uncert = float(train_df["uncertainty"].median())
    # Weak label-prior template. It is intentionally valid and non-degenerate.
    type_to_span = {
        "ok": [],
        "drift": [{"start": 8, "end": 13, "type": "drift", "severity": 0.45}],
        "lost_tracking": [{"start": 7, "end": 11, "type": "lost_tracking", "severity": 0.55}],
        "relocalized": [{"start": 7, "end": 12, "type": "relocalized", "severity": 0.5}],
        "uncertain": [{"start": 8, "end": 10, "type": "uncertain", "severity": 0.35}],
    }
    rows = []
    for _, r in test_df.iterrows():
        h = _stable_int(str(r["id"]))
        rel = [0, 4, 9, 14] if h % 2 else [1, 6, 12, 17]
        span = type_to_span.get(majority_type, type_to_span["drift"])
        anchors = [{"current": 13, "anchor": 4}] if span else []
        rows.append(
            {
                "id": r["id"],
                "reliable_keyframes_json": _json_dumps(rel),
                "failure_spans_json": _json_dumps(span),
                "anchor_edges_json": _json_dumps(anchors),
                "failure_type": majority_type,
                "uncertainty": round(float(np.clip(median_uncert, 0, 1)), 4),
            }
        )
    return pd.DataFrame(rows)


def _prepare_impl(raw: Path, public: Path, private: Path, manifest_path: Path | None = None, max_rows: int = 0) -> None:
    raw_base = _find_raw_dir(Path(raw))
    public = Path(public)
    private = Path(private)
    public_resolved = public.resolve()
    private_resolved = private.resolve()
    raw_resolved = raw_base.resolve()
    if public_resolved == private_resolved:
        raise SystemExit("public and private output directories must be different")
    if public_resolved == raw_resolved or private_resolved == raw_resolved:
        raise SystemExit("output directories must not overwrite the raw input directory")
    if public_resolved in private_resolved.parents or private_resolved in public_resolved.parents:
        raise SystemExit("public and private output directories must not be nested")
    for d in [public / "train" / "panels", public / "test" / "panels", private]:
        d.mkdir(parents=True, exist_ok=True)

    all_records = []
    for seq, meta in SEQ_META.items():
        zip_path = raw_base / meta["zip"]
        seq_dir = raw_base / seq
        if zip_path.exists():
            all_records.extend(_records_from_zip(zip_path))
        elif seq_dir.exists():
            all_records.extend(_records_from_folder(seq_dir))
        else:
            raise SystemExit(f"missing source ZIP or directory: {zip_path} / {seq_dir}")
    if max_rows:
        train = [r for r in all_records if r.split == "train"][:max_rows]
        test = [r for r in all_records if r.split == "test"][:max_rows]
        all_records = train + test
    if len({r.scene_key for r in all_records}) != len(all_records):
        raise SystemExit("duplicate raw scene keys")
    if {r.source_seq for r in all_records if r.split == "train"} & {r.source_seq for r in all_records if r.split == "test"}:
        raise SystemExit("source sequence leaked across train/test")

    id_map = _global_id_map([r.scene_key for r in all_records])
    train_rows, test_rows, answers = [], [], []
    source_map_rows = []
    for rec in all_records:
        rid = id_map[rec.scene_key]
        zip_path = raw_base / SEQ_META[rec.source_seq]["zip"]
        seq_dir = raw_base / rec.source_seq
        rel_panel = f"{rec.split}/panels/{rid}.jpg"
        if zip_path.exists():
            with zipfile.ZipFile(zip_path) as z:
                _save_panel(z, rec.source_seq, pd.Series(dtype=object), rec, public / rel_panel)
        else:
            _save_panel_folder(seq_dir, rec, public / rel_panel)
        base = {
            "id": rid,
            "image": rel_panel,
            "imu_trace_json": _imu_trace_json(rec),
            "degraded_pose_json": _json_dumps(rec.degraded),
            "window_meta_json": _meta_json(rec),
            "prompt": PROMPT,
        }
        targets = {
            "reliable_keyframes_json": _json_dumps(rec.reliable),
            "failure_spans_json": _json_dumps(rec.spans),
            "anchor_edges_json": _json_dumps(rec.anchors),
            "failure_type": rec.failure_type,
            "uncertainty": rec.uncertainty,
        }
        if rec.split == "train":
            train_rows.append({**base, **targets})
        else:
            test_rows.append(base)
            answers.append(
                {
                    "id": rid,
                    **targets,
                    "group_device": rec.device,
                    "group_motion": rec.motion,
                    "group_failure_type": rec.failure_type,
                }
            )
        source_map_rows.append(
            {
                "id": rid,
                "source_seq": rec.source_seq,
                "start_keyframe": rec.start,
                "split": rec.split,
                "first_raw_timestamp_ns": int(rec.cam_ts[0]),
                "last_raw_timestamp_ns": int(rec.cam_ts[-1]),
            }
        )

    train_df = pd.DataFrame(train_rows).sort_values("id").reset_index(drop=True)
    test_df = pd.DataFrame(test_rows).sort_values("id").reset_index(drop=True)
    ans_df = pd.DataFrame(answers).sort_values("id").reset_index(drop=True)
    for name, df in [("train", train_df), ("test", test_df), ("answers", ans_df)]:
        if df.isna().any().any():
            raise SystemExit(f"{name} contains NaN")
        if df["id"].duplicated().any():
            raise SystemExit(f"{name} contains duplicate ids")
    for axis in ["group_device", "group_motion", "group_failure_type"]:
        counts = ans_df[axis].value_counts()
        if counts.min() < MIN_GROUP_TEST:
            raise SystemExit(f"test subgroup {axis} below MIN_GROUP_TEST={MIN_GROUP_TEST}: {counts.to_dict()}")

    train_df.to_csv(public / "train.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    test_df.to_csv(public / "test.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    ans_df.to_csv(private / "answers.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    _make_sample(train_df, test_df).to_csv(public / "sample_submission.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    pd.DataFrame(source_map_rows).sort_values("id").to_csv(private / "source_map_audit_only.csv", index=False)
    manifest = {
        "train_rows": int(len(train_df)),
        "test_rows": int(len(test_df)),
        "source_sequences_train": sorted({r.source_seq for r in all_records if r.split == "train"}),
        "source_sequences_test": sorted({r.source_seq for r in all_records if r.split == "test"}),
        "test_group_counts": {c: ans_df[c].value_counts().to_dict() for c in ["group_device", "group_motion", "group_failure_type"]},
    }
    if manifest_path is not None:
        Path(manifest_path).write_text(_json_dumps(manifest), encoding="utf-8")
    print(_json_dumps(manifest))


def prepare(raw: Path, public: Path, private: Path) -> None:
    """Platform entrypoint: materialize public files and private answers."""
    _prepare_impl(Path(raw), Path(public), Path(private))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", default="raw_sources")
    parser.add_argument("--output-dir", default=".")
    parser.add_argument("--max-rows", type=int, default=0, help="Optional tiny smoke cap after record construction.")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    _prepare_impl(
        Path(args.raw_dir),
        out_dir / "public",
        out_dir / "private",
        out_dir / "PREPARE_MANIFEST.json",
        max_rows=args.max_rows,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

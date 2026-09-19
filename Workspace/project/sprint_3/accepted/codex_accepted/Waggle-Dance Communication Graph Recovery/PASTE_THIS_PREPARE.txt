from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


TITLE = "Waggle-Dance Communication Graph Recovery"
ID_SALT = "waggle_graph_recovery_v1_20260719"
SELECTED_TRACK_DATES = (
    "2019-08-25",
    "2019-08-27",
    "2019-08-28",
    "2019-08-29",
    "2019-09-02",
    "2019-09-05",
    "2019-09-10",
    "2019-09-11",
)
TEST_DATES = {"2019-09-05", "2019-09-11"}
MIN_EPISODE_SEC = 15.0
MAX_EPISODE_SEC = 60.0
MIN_WAGGLES = 3
MAX_WAGGLES = 30
MAX_BEES = 48
MIN_BEES = 14
MIN_POINTS_PER_BEE = 8
WAGGLE_RADIUS_MM = 75.0
MIN_GROUP_TEST = int(os.environ.get("WAGGLE_MIN_GROUP_TEST", "12"))
MAX_TOTAL_EPISODES = int(os.environ.get("WAGGLE_MAX_EPISODES", "0"))

INPUT_COLUMNS = [
    "id",
    "episode_npz",
    "duration_sec",
    "bee_count",
    "comb_side",
    "crowding_level",
    "tracking_confidence_level",
]
LABEL_COLUMNS = [
    "dancer_id",
    "waggle_intervals_json",
    "roles_json",
    "edges_json",
    "label_quality",
]
SUBMISSION_COLUMNS = [
    "id",
    "dancer_id",
    "waggle_intervals_json",
    "roles_json",
    "edges_json",
    "confidence",
]


@dataclass
class EpisodeCandidate:
    raw_key: str
    dance_id: str
    dancer_id: str
    date: str
    cam_id: int
    start: pd.Timestamp
    end: pd.Timestamp
    duration_sec: float
    median_x: float
    median_y: float
    waggle_times: list[pd.Timestamp]
    roles_by_raw_bee: dict[str, str]
    fingerprint: str


def _stable_int(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], 16)


def _episode_public_id(fingerprint: str) -> str:
    digest = hashlib.sha256(f"{ID_SALT}:public-id:{fingerprint}".encode("utf-8")).hexdigest()
    return f"wdg_{digest[:14]}"


def _json_dumps(obj) -> str:
    return json.dumps(obj, ensure_ascii=True, separators=(",", ":"))


def _wrap_angle(x: np.ndarray) -> np.ndarray:
    return ((x + np.pi) % (2.0 * np.pi)) - np.pi


def _bucket(value: float, cuts: tuple[float, float], labels: tuple[str, str, str]) -> str:
    if value < cuts[0]:
        return labels[0]
    if value < cuts[1]:
        return labels[1]
    return labels[2]


def _clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def _find_raw_root(raw: Path) -> Path:
    candidates = [
        raw,
        raw / "raw_upload",
        raw / "waggle_dance_raw_subset",
        raw / "Waggle-Dance Communication Graph Recovery Raw Subset",
    ]
    required = [
        "Berlin2019_dances.csv",
        "Berlin2019_followers.csv",
        "Berlin2019_waggle_phases.csv",
    ]
    for cand in candidates:
        if all((cand / name).exists() for name in required):
            return cand
    raise FileNotFoundError(
        "Could not find the Zenodo CSV files. Expected Berlin2019_dances.csv, "
        "Berlin2019_followers.csv, and Berlin2019_waggle_phases.csv in raw/ "
        "or raw/raw_upload/."
    )


def _require_columns(df: pd.DataFrame, name: str, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise SystemExit(f"{name} is missing required columns: {missing}")
    bad = [c for c in cols if df[c].isna().all()]
    if bad:
        raise SystemExit(f"{name} has all-null required columns: {bad}")


def _read_source_tables(root: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    dances = pd.read_csv(
        root / "Berlin2019_dances.csv",
        dtype={"dance_id": str, "dancer_id": str, "cam_id": int},
    )
    followers = pd.read_csv(
        root / "Berlin2019_followers.csv",
        dtype={"dance_id": str, "follower_id": str, "cam_id": int, "label": str},
    )
    waggles = pd.read_csv(root / "Berlin2019_waggle_phases.csv", dtype={"cam_id": int})
    verified_path = root / "Berlin2019_dances_with_manually_verified_times.csv"
    verified = (
        pd.read_csv(verified_path, dtype={"dance_id": str, "dancer_id": str, "cam_id": int})
        if verified_path.exists()
        else pd.DataFrame()
    )

    _require_columns(
        dances,
        "Berlin2019_dances.csv",
        ["dancer_id", "dance_id", "ts_from", "ts_to", "cam_id", "median_x", "median_y"],
    )
    _require_columns(
        followers,
        "Berlin2019_followers.csv",
        ["dance_id", "follower_id", "ts_from", "ts_to", "label", "cam_id"],
    )
    _require_columns(
        waggles,
        "Berlin2019_waggle_phases.csv",
        ["timestamp", "cam_id", "x_median", "y_median", "waggle_angle"],
    )
    if not verified.empty:
        _require_columns(
            verified,
            "Berlin2019_dances_with_manually_verified_times.csv",
            ["dance_id", "dancer_id", "cam_id", "dance_start", "dance_end"],
        )

    dances["start"] = pd.to_datetime(dances["ts_from"], utc=True, errors="coerce")
    dances["end"] = pd.to_datetime(dances["ts_to"], utc=True, errors="coerce")
    dances["median_x"] = pd.to_numeric(dances["median_x"], errors="coerce")
    dances["median_y"] = pd.to_numeric(dances["median_y"], errors="coerce")
    dances = dances.dropna(subset=["start", "end", "median_x", "median_y"]).copy()

    if not verified.empty:
        verified = verified.copy()
        verified["manual_start"] = pd.to_datetime(verified["dance_start"], utc=True, errors="coerce")
        verified["manual_end"] = pd.to_datetime(verified["dance_end"], utc=True, errors="coerce")
        manual = verified.dropna(subset=["manual_start", "manual_end"]).set_index("dance_id")
        for dance_id, row in manual.iterrows():
            mask = dances["dance_id"] == str(dance_id)
            dances.loc[mask, "start"] = row["manual_start"]
            dances.loc[mask, "end"] = row["manual_end"]

    dances["duration_sec"] = (dances["end"] - dances["start"]).dt.total_seconds()
    dances["date"] = dances["start"].dt.strftime("%Y-%m-%d")
    dances["cam_id"] = dances["cam_id"].astype(int)

    followers["start"] = pd.to_datetime(followers["ts_from"], utc=True, errors="coerce")
    followers["end"] = pd.to_datetime(followers["ts_to"], utc=True, errors="coerce")
    followers = followers.dropna(subset=["start", "end"]).copy()
    followers["label"] = followers["label"].str.strip().str.lower()
    followers = followers[followers["label"].isin(["attendance", "follower"])].copy()

    waggles["time"] = pd.to_datetime(waggles["timestamp"], utc=True, errors="coerce")
    waggles["x_median"] = pd.to_numeric(waggles["x_median"], errors="coerce")
    waggles["y_median"] = pd.to_numeric(waggles["y_median"], errors="coerce")
    waggles = waggles.dropna(subset=["time", "x_median", "y_median"]).copy()
    waggles["date"] = waggles["time"].dt.strftime("%Y-%m-%d")
    waggles["cam_id"] = waggles["cam_id"].astype(int)

    return dances, followers, waggles, verified


def _build_candidates(dances: pd.DataFrame, followers: pd.DataFrame, waggles: pd.DataFrame) -> list[EpisodeCandidate]:
    dances = dances[
        dances["date"].isin(SELECTED_TRACK_DATES)
        & (dances["duration_sec"] >= MIN_EPISODE_SEC)
    ].copy()
    dances = dances.sort_values(["date", "cam_id", "start", "dance_id"]).reset_index(drop=True)
    followers_by_dance = {k: g.copy() for k, g in followers.groupby("dance_id", sort=False)}
    waggle_by_date_cam = {
        (date, int(cam)): g.sort_values("time").reset_index(drop=True)
        for (date, cam), g in waggles[waggles["date"].isin(SELECTED_TRACK_DATES)].groupby(["date", "cam_id"])
    }

    out: list[EpisodeCandidate] = []
    for row in dances.itertuples(index=False):
        ep_start = row.start
        ep_end = min(row.end, row.start + pd.Timedelta(seconds=MAX_EPISODE_SEC))
        ep_duration = (ep_end - ep_start).total_seconds()
        if ep_duration < MIN_EPISODE_SEC:
            continue
        wg = waggle_by_date_cam.get((row.date, int(row.cam_id)))
        if wg is None or wg.empty:
            continue
        window = wg[(wg["time"] >= ep_start) & (wg["time"] <= ep_end)].copy()
        if window.empty:
            continue
        dist = np.hypot(window["x_median"].to_numpy() - row.median_x, window["y_median"].to_numpy() - row.median_y)
        window = window[dist <= WAGGLE_RADIUS_MM]
        if not (MIN_WAGGLES <= len(window) <= MAX_WAGGLES):
            continue

        roles: dict[str, str] = {}
        fg = followers_by_dance.get(str(row.dance_id), pd.DataFrame())
        if not fg.empty:
            fg = fg[(fg["cam_id"].astype(int) == int(row.cam_id)) & (fg["end"] >= ep_start) & (fg["start"] <= ep_end)]
            for follower_id, gg in fg.groupby("follower_id", sort=False):
                labels = set(gg["label"].tolist())
                roles[str(follower_id)] = "follower" if "follower" in labels else "attendee"
        if "follower" not in set(roles.values()):
            continue

        raw_key = f"{row.date}:{row.cam_id}:{row.dance_id}:{row.dancer_id}:{ep_start.value}:{ep_end.value}"
        fingerprint = hashlib.sha256(f"{ID_SALT}:{raw_key}".encode("utf-8")).hexdigest()
        out.append(
            EpisodeCandidate(
                raw_key=raw_key,
                dance_id=str(row.dance_id),
                dancer_id=str(row.dancer_id),
                date=str(row.date),
                cam_id=int(row.cam_id),
                start=ep_start,
                end=ep_end,
                duration_sec=float(ep_duration),
                median_x=float(row.median_x),
                median_y=float(row.median_y),
                waggle_times=window["time"].tolist(),
                roles_by_raw_bee=roles,
                fingerprint=fingerprint,
            )
        )

    out.sort(key=lambda e: e.fingerprint)
    return out


def _split_candidates(candidates: list[EpisodeCandidate]) -> tuple[list[EpisodeCandidate], list[EpisodeCandidate]]:
    test = [e for e in candidates if e.date in TEST_DATES]
    test_dancers = {e.dancer_id for e in test}
    train = [e for e in candidates if e.date not in TEST_DATES and e.dancer_id not in test_dancers]
    if MAX_TOTAL_EPISODES > 0:
        target_test = max(8, int(round(MAX_TOTAL_EPISODES * 0.42)))
        target_train = max(8, MAX_TOTAL_EPISODES - target_test)
        train = train[:target_train]
        test = test[:target_test]
    if {e.dancer_id for e in train} & {e.dancer_id for e in test}:
        raise SystemExit("raw dancer identity leaked across split")
    return train, test


def _track_csv_path(root: Path, date: str) -> Path | None:
    for p in [root / "Berlin2019_tracks" / f"{date}.csv", root / f"{date}.csv"]:
        if p.exists():
            return p
    return None


def _read_track_csv(root: Path, date: str) -> pd.DataFrame:
    path = _track_csv_path(root, date)
    dtype = {"cam_id": int, "track_id": str, "bee_id": str, "frame_id": str}
    if path is not None:
        return pd.read_csv(path, dtype=dtype)

    zip_path = root / "Berlin2019_tracks.zip"
    if zip_path.exists():
        member = f"Berlin2019_tracks/{date}.csv"
        with zipfile.ZipFile(zip_path) as zf:
            if member not in zf.namelist():
                raise FileNotFoundError(f"{member} not found in {zip_path}")
            with zf.open(member) as fh:
                return pd.read_csv(fh, dtype=dtype)
    raise FileNotFoundError(
        f"Missing track CSV for {date}. Expected Berlin2019_tracks/{date}.csv, "
        f"{date}.csv, or Berlin2019_tracks.zip containing Berlin2019_tracks/{date}.csv."
    )


def _standardize_tracks(df: pd.DataFrame, date: str) -> pd.DataFrame:
    required = [
        "cam_id",
        "timestamp",
        "frame_id",
        "track_id",
        "bee_id",
        "bee_id_confidence",
        "x_pos_hive",
        "y_pos_hive",
        "orientation_hive",
    ]
    _require_columns(df, f"track CSV for {date}", required)
    out = df[required].copy()
    out["time"] = pd.to_datetime(out["timestamp"], utc=True, errors="coerce")
    out["cam_id"] = pd.to_numeric(out["cam_id"], errors="coerce")
    out["bee_id_confidence"] = pd.to_numeric(out["bee_id_confidence"], errors="coerce")
    out["x_pos_hive"] = pd.to_numeric(out["x_pos_hive"], errors="coerce")
    out["y_pos_hive"] = pd.to_numeric(out["y_pos_hive"], errors="coerce")
    out["orientation_hive"] = pd.to_numeric(out["orientation_hive"], errors="coerce")
    out = out.dropna(subset=["time", "cam_id", "bee_id", "bee_id_confidence", "x_pos_hive", "y_pos_hive"]).copy()
    out["cam_id"] = out["cam_id"].astype(int)
    out["bee_id"] = out["bee_id"].astype(str)
    return out.sort_values(["time", "bee_id"]).reset_index(drop=True)


def _fill_orientation(df: pd.DataFrame) -> np.ndarray:
    orientation = np.full(len(df), np.nan, dtype=np.float32)
    for _, idx in df.groupby("bee_id", sort=False).groups.items():
        g = df.loc[list(idx)].sort_values("time")
        pos = df.index.get_indexer(g.index)
        ori = g["orientation_hive"].to_numpy(dtype=float)
        x = g["x_pos_hive"].to_numpy(dtype=float)
        y = g["y_pos_hive"].to_numpy(dtype=float)
        if len(g) >= 2:
            dx = np.gradient(x)
            dy = np.gradient(y)
            est = np.arctan2(dy, dx)
        else:
            est = np.zeros(len(g), dtype=float)
        ori = np.where(np.isfinite(ori), ori, est)
        ori = np.where(np.isfinite(ori), ori, 0.0)
        orientation[pos] = ori.astype(np.float32)
    return np.where(np.isfinite(orientation), orientation, 0.0).astype(np.float32)


def _choose_bees(ep: EpisodeCandidate, slice_df: pd.DataFrame) -> list[str]:
    counts = slice_df.groupby("bee_id").size()
    valid = counts[counts >= MIN_POINTS_PER_BEE]
    primary = [ep.dancer_id] + sorted(ep.roles_by_raw_bee)
    chosen: list[str] = []
    for bee in primary:
        if bee in valid.index and bee not in chosen:
            chosen.append(bee)
    if ep.dancer_id not in chosen:
        return []

    med = slice_df[slice_df["bee_id"].isin(valid.index)].groupby("bee_id")[["x_pos_hive", "y_pos_hive"]].median()
    med["dist"] = np.hypot(med["x_pos_hive"] - ep.median_x, med["y_pos_hive"] - ep.median_y)
    med["count"] = valid.reindex(med.index).fillna(0).astype(float)
    med["score"] = med["dist"] - 0.015 * med["count"]
    for bee in med.sort_values("score").index.astype(str):
        if bee not in chosen:
            chosen.append(bee)
        if len(chosen) >= MAX_BEES:
            break
    return chosen


def _relative_waggle_intervals(ep: EpisodeCandidate, time_warp=None, public_duration: float | None = None) -> list[dict[str, float]]:
    intervals = []
    if public_duration is None:
        public_duration = ep.duration_sec
    half_width = max(0.24, 0.35 * public_duration / max(ep.duration_sec, 1e-6))
    for ts in sorted(ep.waggle_times):
        raw_rel = (ts - ep.start).total_seconds()
        rel = float(time_warp(raw_rel)) if time_warp is not None else raw_rel
        start = max(0.0, rel - half_width)
        end = min(public_duration, rel + half_width)
        if end > start:
            intervals.append({"start": round(start, 3), "end": round(end, 3)})
    merged: list[dict[str, float]] = []
    for item in intervals:
        if merged and item["start"] - merged[-1]["end"] <= 0.18:
            merged[-1]["end"] = max(merged[-1]["end"], item["end"])
        else:
            merged.append(item)
    return merged[:MAX_WAGGLES]


def _neighbor_counts(t: np.ndarray, x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    frame = np.round(t * 6.0).astype(np.int32)
    n20 = np.zeros(len(t), dtype=np.uint8)
    n40 = np.zeros(len(t), dtype=np.uint8)
    for _, idx in pd.Series(np.arange(len(t))).groupby(frame).groups.items():
        ids = np.asarray(list(idx), dtype=int)
        if len(ids) <= 1:
            continue
        dx = x[ids, None] - x[ids][None, :]
        dy = y[ids, None] - y[ids][None, :]
        dist = np.sqrt(dx * dx + dy * dy)
        n20[ids] = np.maximum(0, (dist <= 20.0).sum(axis=1) - 1).astype(np.uint8)
        n40[ids] = np.maximum(0, (dist <= 40.0).sum(axis=1) - 1).astype(np.uint8)
    return n20, n40


def _materialize_episode(
    ep: EpisodeCandidate,
    tracks: pd.DataFrame,
    split_name: str,
    public_root: Path,
) -> dict | None:
    slice_df = tracks[
        (tracks["cam_id"] == ep.cam_id)
        & (tracks["time"] >= ep.start)
        & (tracks["time"] <= ep.end)
    ].copy()
    if slice_df.empty:
        return None

    chosen = _choose_bees(ep, slice_df)
    if len(chosen) < MIN_BEES:
        return None
    role_bees = {bee: role for bee, role in ep.roles_by_raw_bee.items() if bee in chosen and bee != ep.dancer_id}
    if "follower" not in set(role_bees.values()):
        return None

    rng = np.random.default_rng(_stable_int(f"{ID_SALT}:episode-rng:{ep.fingerprint}"))
    public_duration = float(rng.uniform(35.0, 55.0))
    warp_phase_1 = float(rng.uniform(-math.pi, math.pi))
    warp_phase_2 = float(rng.uniform(-math.pi, math.pi))
    warp_amp_1 = float(rng.uniform(0.16, 0.28))
    warp_amp_2 = float(rng.uniform(0.07, 0.14))

    def warp_time(raw_seconds) -> np.ndarray:
        raw_arr = np.asarray(raw_seconds, dtype=float)
        u = np.clip(raw_arr / max(ep.duration_sec, 1e-6), 0.0, 1.0)
        warped = (
            u
            + warp_amp_1 / (2.0 * math.pi) * (math.cos(warp_phase_1) - np.cos(2.0 * math.pi * u + warp_phase_1))
            + warp_amp_2 / (4.0 * math.pi) * (math.cos(warp_phase_2) - np.cos(4.0 * math.pi * u + warp_phase_2))
        )
        return np.clip(warped, 0.0, 1.0) * public_duration

    local_order = chosen.copy()
    rng.shuffle(local_order)
    local_map = {raw_bee: f"B{i:02d}" for i, raw_bee in enumerate(local_order)}
    if ep.dancer_id not in local_map:
        return None

    df = slice_df[slice_df["bee_id"].isin(chosen)].copy()
    df = df.sort_values(["bee_id", "time"]).reset_index(drop=True)

    keep = rng.random(len(df)) < float(rng.uniform(0.42, 0.58))
    for _, idx in df.groupby("bee_id", sort=False).groups.items():
        ids = np.asarray(list(idx), dtype=int)
        min_keep = min(len(ids), max(5, int(math.ceil(0.25 * len(ids)))))
        if int(keep[ids].sum()) < min_keep:
            keep[ids] = False
            forced = rng.choice(ids, size=min_keep, replace=False)
            keep[forced] = True
    df = df.loc[keep].sort_values(["bee_id", "time"]).reset_index(drop=True)

    t_raw = (df["time"] - ep.start).dt.total_seconds().to_numpy(dtype=np.float32)
    bee_time_shift = {raw_bee: float(rng.normal(0.0, 0.80)) for raw_bee in local_order}
    time_shifts = np.array([bee_time_shift[str(bee)] for bee in df["bee_id"].astype(str)], dtype=float)
    t = np.clip(
        warp_time(t_raw)
        + time_shifts
        + 0.38 * np.sin(2.0 * math.pi * np.asarray(t_raw, dtype=float) / max(ep.duration_sec, 1e-6) + warp_phase_2)
        + rng.normal(0.0, 0.18, size=len(df)),
        0.0,
        public_duration,
    )
    x_raw = df["x_pos_hive"].to_numpy(dtype=np.float32)
    y_raw = df["y_pos_hive"].to_numpy(dtype=np.float32)
    conf = np.clip(df["bee_id_confidence"].to_numpy(dtype=np.float32), 0.0, 1.0)
    orientation = _fill_orientation(df)

    center_x = float(np.nanmedian(x_raw))
    center_y = float(np.nanmedian(y_raw))
    angle = float(rng.uniform(-math.pi, math.pi))
    scale_x = float(rng.uniform(0.88, 1.12))
    scale_y = float(rng.uniform(0.88, 1.12))
    shear_xy = float(rng.uniform(-0.10, 0.10))
    shear_yx = float(rng.uniform(-0.10, 0.10))
    ca, sa = math.cos(angle), math.sin(angle)
    xc = x_raw - center_x
    yc = y_raw - center_y
    xa = scale_x * xc + shear_xy * yc
    ya = scale_y * yc + shear_yx * xc
    local_offset = {
        raw_bee: rng.normal(0.0, 20.0, size=2)
        for raw_bee in local_order
    }
    offsets = np.vstack([local_offset[str(bee)] for bee in df["bee_id"].astype(str)])
    phase_x = float(rng.uniform(-math.pi, math.pi))
    phase_y = float(rng.uniform(-math.pi, math.pi))
    phase_t = float(rng.uniform(-math.pi, math.pi))
    time_phase = 2.0 * math.pi * np.asarray(t, dtype=float) / max(public_duration, 1e-6)
    x = (
        xa * ca
        - ya * sa
        + 18.0 * np.sin(yc / 58.0 + phase_x)
        + 5.0 * np.sin(time_phase + phase_t)
        + offsets[:, 0]
        + rng.normal(0.0, 6.00, size=len(df))
    )
    y = (
        xa * sa
        + ya * ca
        + 18.0 * np.sin(xc / 61.0 + phase_y)
        + 5.0 * np.cos(time_phase + phase_t)
        + offsets[:, 1]
        + rng.normal(0.0, 6.00, size=len(df))
    )
    o = _wrap_angle(orientation + angle + rng.normal(0.0, 0.130, size=len(df))).astype(np.float32)
    t = np.round(t, 3).astype(np.float32)
    local_idx = np.array([int(local_map[str(bee)][1:]) for bee in df["bee_id"].astype(str)], dtype=np.uint16)
    n20, n40 = _neighbor_counts(t, x.astype(np.float32), y.astype(np.float32))

    order = np.lexsort((t, local_idx))
    n_frames = int(math.floor(public_duration * 6.0)) + 1
    frame_bin = np.clip(np.round(t * 6.0).astype(np.int32), 0, max(0, n_frames - 1))
    dense = np.zeros((len(local_order), n_frames, 6), dtype=np.float32)
    dense_mask = np.zeros((len(local_order), n_frames), dtype=np.uint8)
    dense[local_idx, frame_bin, 0] = x.astype(np.float32)
    dense[local_idx, frame_bin, 1] = y.astype(np.float32)
    dense[local_idx, frame_bin, 2] = o.astype(np.float32)
    dense[local_idx, frame_bin, 3] = conf.astype(np.float32)
    dense[local_idx, frame_bin, 4] = n20.astype(np.float32)
    dense[local_idx, frame_bin, 5] = n40.astype(np.float32)
    dense_mask[local_idx, frame_bin] = 1
    episode_id = _episode_public_id(ep.fingerprint)
    rel_path = f"{split_name}/episodes/{episode_id}.npz"
    out_path = public_root / rel_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out_path,
        t_sec=t[order],
        bee_index=local_idx[order],
        x_mm=np.round(x[order], 3).astype(np.float32),
        y_mm=np.round(y[order], 3).astype(np.float32),
        orientation_rad=o[order],
        tracking_confidence=np.round(conf[order], 4).astype(np.float32),
        neighbor_count_20mm=n20[order],
        neighbor_count_40mm=n40[order],
        dense_features=dense,
        dense_mask=dense_mask,
        dense_frame_hz=np.float32(6.0),
    )

    intervals = _relative_waggle_intervals(ep, time_warp=warp_time, public_duration=public_duration)
    roles = [
        {"bee_id": local_map[raw_bee], "role": role}
        for raw_bee, role in sorted(role_bees.items(), key=lambda kv: local_map[kv[0]])
    ]
    edges = [
        {"source": local_map[ep.dancer_id], "target": local_map[raw_bee]}
        for raw_bee, role in sorted(role_bees.items(), key=lambda kv: local_map[kv[0]])
        if role == "follower"
    ]
    if not edges:
        return None

    avg_crowding = float(np.mean(n40)) if len(n40) else 0.0
    med_conf = float(np.median(conf)) if len(conf) else 0.0
    track_coverage = len(df) / max(1.0, len(local_order) * public_duration * 6.0)
    crowding_level = _bucket(avg_crowding, (3.5, 10.0), ("low", "medium", "high"))
    tracking_level = _bucket(track_coverage, (0.26, 0.40), ("low", "medium", "high"))
    duration_bucket = _bucket(public_duration, (40.0, 48.0), ("short", "medium", "long"))
    waggle_count_bucket = _bucket(len(intervals), (7.0, 14.0), ("few", "moderate", "many"))
    label_quality = float(np.clip(0.50 + 0.25 * med_conf + 0.15 * min(1.0, len(edges) / 4.0) + 0.10 * min(1.0, len(intervals) / 10.0), 0, 1))

    return {
        "id": episode_id,
        "episode_npz": rel_path,
        "duration_sec": round(public_duration, 3),
        "bee_count": len(local_order),
        "comb_side": "side_a" if ep.cam_id == 0 else "side_b",
        "crowding_level": crowding_level,
        "tracking_confidence_level": tracking_level,
        "dancer_id": local_map[ep.dancer_id],
        "waggle_intervals_json": _json_dumps(intervals),
        "roles_json": _json_dumps(roles),
        "edges_json": _json_dumps(edges),
        "label_quality": round(label_quality, 6),
        "duration_bucket": duration_bucket,
        "waggle_count_bucket": waggle_count_bucket,
        "date_group": f"session_{hashlib.sha256((ID_SALT + ep.date).encode()).hexdigest()[:6]}",
    }


def _heuristic_prediction(npz_path: Path, duration_sec: float) -> dict:
    data = np.load(npz_path)
    t = data["t_sec"].astype(float)
    bee = data["bee_index"].astype(int)
    x = data["x_mm"].astype(float)
    y = data["y_mm"].astype(float)
    ori = data["orientation_rad"].astype(float)
    n40 = data["neighbor_count_40mm"].astype(float)
    unique = np.unique(bee)
    scores = []
    for b in unique:
        idx = np.where(bee == b)[0]
        if len(idx) < 4:
            scores.append((-1.0, b))
            continue
        order = np.argsort(t[idx])
        ii = idx[order]
        dt = np.maximum(np.diff(t[ii]), 1e-3)
        speed = np.hypot(np.diff(x[ii]), np.diff(y[ii])) / dt
        turn = np.abs(np.diff(np.unwrap(ori[ii]))) / dt
        obs_frac = min(1.0, len(ii) / max(1.0, duration_sec * 6.0))
        crowd = float(np.nanmean(n40[ii])) / 20.0
        score = 0.45 * float(np.nanpercentile(speed, 90)) + 0.20 * float(np.nanpercentile(turn, 90)) + 1.2 * obs_frac + crowd
        scores.append((score, b))
    dancer = max(scores)[1] if scores else 0

    idx = np.where(bee == dancer)[0]
    intervals: list[dict[str, float]] = []
    if len(idx) >= 8:
        order = np.argsort(t[idx])
        ii = idx[order]
        dt = np.maximum(np.diff(t[ii]), 1e-3)
        speed = np.hypot(np.diff(x[ii]), np.diff(y[ii])) / dt
        turn = np.abs(np.diff(np.unwrap(ori[ii]))) / dt
        signal = speed / (float(np.nanmedian(speed)) + 1e-6) + 0.30 * turn / (float(np.nanmedian(turn)) + 1e-6)
        thresh = float(np.nanpercentile(signal, 68)) if len(signal) else 0.0
        active = np.r_[False, signal >= thresh]
        starts = []
        current = None
        for tt, flag in zip(t[ii], active):
            if flag and current is None:
                current = float(tt)
            if not flag and current is not None:
                starts.append((current, float(tt)))
                current = None
        if current is not None:
            starts.append((current, float(t[ii][-1])))
        for a, b in starts:
            if b - a >= 0.20:
                intervals.append({"start": round(max(0.0, a - 0.18), 3), "end": round(min(duration_sec, b + 0.18), 3)})
            if len(intervals) >= 12:
                break
    if not intervals:
        step = max(2.0, duration_sec / 6.0)
        intervals = [{"start": round(step * i + 0.2, 3), "end": round(min(duration_sec, step * i + 0.9), 3)} for i in range(1, 4)]

    role_scores = []
    dancer_idx = np.where(bee == dancer)[0]
    if len(dancer_idx):
        for b in unique:
            if b == dancer:
                continue
            idx_b = np.where(bee == b)[0]
            if len(idx_b) < 4:
                continue
            # Nearest asynchronous time match is enough for a deliberately weak template.
            sample = idx_b[:: max(1, len(idx_b) // 32)]
            dist_vals = []
            for j in sample:
                k = dancer_idx[np.argmin(np.abs(t[dancer_idx] - t[j]))]
                dist_vals.append(math.hypot(float(x[j] - x[k]), float(y[j] - y[k])))
            if dist_vals:
                role_scores.append((float(np.percentile(dist_vals, 20)), int(b)))
    role_scores.sort()
    roles = []
    for rank, (_, b) in enumerate(role_scores[:16]):
        roles.append({"bee_id": f"B{b:02d}", "role": "follower" if rank < 10 else "attendee"})
    edges = [{"source": f"B{dancer:02d}", "target": r["bee_id"]} for r in roles if r["role"] == "follower"]
    return {
        "dancer_id": f"B{dancer:02d}",
        "waggle_intervals_json": _json_dumps(intervals),
        "roles_json": _json_dumps(roles),
        "edges_json": _json_dumps(edges),
        "confidence": 0.28,
    }


def _write_sample_submission(public: Path, train_df: pd.DataFrame, test_df: pd.DataFrame) -> None:
    interval_counts = train_df["waggle_intervals_json"].map(lambda s: len(json.loads(s))).to_numpy()
    role_counts = train_df["roles_json"].map(lambda s: len(json.loads(s))).to_numpy()
    edge_counts = train_df["edges_json"].map(lambda s: len(json.loads(s))).to_numpy()
    n_intervals = int(np.clip(round(float(np.median(interval_counts))), 3, 10))
    n_roles = int(np.clip(round(float(np.median(role_counts))), 2, 8))
    n_edges = int(np.clip(round(float(np.median(edge_counts))), 1, 4))
    rows = []
    for row in test_df.itertuples(index=False):
        duration = float(row.duration_sec)
        step = duration / (n_intervals + 1)
        intervals = [
            {"start": round(max(0.0, step * (i + 1) - 0.50), 3), "end": round(min(duration, step * (i + 1) + 0.50), 3)}
            for i in range(n_intervals)
        ]
        roles = [
            {"bee_id": f"B{i + 1:02d}", "role": "follower" if i < n_edges else "attendee"}
            for i in range(n_roles)
        ]
        edges = [{"source": "B00", "target": f"B{i + 1:02d}"} for i in range(n_edges)]
        rows.append(
            {
                "id": row.id,
                "dancer_id": "B00",
                "waggle_intervals_json": _json_dumps(intervals),
                "roles_json": _json_dumps(roles),
                "edges_json": _json_dumps(edges),
                "confidence": 0.18,
            }
        )
    sample = pd.DataFrame(rows, columns=SUBMISSION_COLUMNS).sort_values("id")
    sample.to_csv(public / "sample_submission.csv", index=False)


def _validate_group_counts(answers: pd.DataFrame) -> None:
    group_cols = [
        "crowding_level",
        "tracking_confidence_level",
        "duration_bucket",
        "waggle_count_bucket",
        "comb_side",
        "date_group",
    ]
    for col in group_cols:
        counts = answers[col].value_counts()
        if (counts < MIN_GROUP_TEST).any():
            raise SystemExit(f"test group {col} has underfilled buckets: {counts.to_dict()}")


def prepare(raw: Path, public: Path, private: Path) -> None:
    raw = Path(raw)
    public = Path(public)
    private = Path(private)
    root = _find_raw_root(raw)
    _clean_dir(public)
    _clean_dir(private)
    (public / "train" / "episodes").mkdir(parents=True, exist_ok=True)
    (public / "test" / "episodes").mkdir(parents=True, exist_ok=True)

    dances, followers, waggles, _ = _read_source_tables(root)
    candidates = _build_candidates(dances, followers, waggles)
    train_candidates, test_candidates = _split_candidates(candidates)
    if len(train_candidates) < 20 or len(test_candidates) < 20:
        raise SystemExit(f"Not enough candidates after split: train={len(train_candidates)} test={len(test_candidates)}")

    by_date: dict[str, list[tuple[str, EpisodeCandidate]]] = {}
    for ep in train_candidates:
        by_date.setdefault(ep.date, []).append(("train", ep))
    for ep in test_candidates:
        by_date.setdefault(ep.date, []).append(("test", ep))

    rows: dict[str, list[dict]] = {"train": [], "test": []}
    for date in SELECTED_TRACK_DATES:
        eps = by_date.get(date, [])
        if not eps:
            continue
        tracks = _standardize_tracks(_read_track_csv(root, date), date)
        for split_name, ep in eps:
            item = _materialize_episode(ep, tracks, split_name, public)
            if item is not None:
                rows[split_name].append(item)
        del tracks

    train_df = pd.DataFrame(rows["train"])
    test_full = pd.DataFrame(rows["test"])
    if train_df.empty or test_full.empty:
        raise SystemExit("No materialized rows; check track files and selected dates")
    if set(train_df["id"]) & set(test_full["id"]):
        raise SystemExit("public IDs overlap across train/test")
    if train_df["id"].duplicated().any() or test_full["id"].duplicated().any():
        raise SystemExit("duplicate public IDs")

    # Keep a compact, deterministic prepared split.
    train_df = train_df.sort_values("id").reset_index(drop=True)
    test_full = test_full.sort_values("id").reset_index(drop=True)
    answers = test_full[
        [
            "id",
            "dancer_id",
            "waggle_intervals_json",
            "roles_json",
            "edges_json",
            "duration_sec",
            "bee_count",
            "crowding_level",
            "tracking_confidence_level",
            "duration_bucket",
            "waggle_count_bucket",
            "comb_side",
            "date_group",
        ]
    ].copy()
    _validate_group_counts(answers)

    train_public = train_df[INPUT_COLUMNS + LABEL_COLUMNS].copy()
    test_public = test_full[INPUT_COLUMNS].copy()
    for df_name, df in [("train", train_public), ("test", test_public), ("answers", answers)]:
        if df.isna().any().any():
            raise SystemExit(f"{df_name} contains NaN values")

    train_public.to_csv(public / "train.csv", index=False)
    test_public.to_csv(public / "test.csv", index=False)
    answers.to_csv(private / "answers.csv", index=False)
    _write_sample_submission(public, train_public, test_public)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare the Waggle-Dance Communication Graph Recovery challenge.")
    parser.add_argument("raw", type=Path)
    parser.add_argument("public", type=Path)
    parser.add_argument("private", type=Path)
    args = parser.parse_args()
    prepare(args.raw, args.public, args.private)


if __name__ == "__main__":
    main()

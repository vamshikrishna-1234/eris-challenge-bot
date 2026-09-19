#!/usr/bin/env python3
"""Baseline and leakage probes for the prepared challenge."""

from __future__ import annotations

import json
import re
import zipfile
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageFilter, ImageOps

from grade import REQUIRED_COLUMNS, grade


ROOT = Path(__file__).resolve().parent
ENUMS = ["ok", "drift", "lost_tracking", "relocalized", "uncertain"]


def jdumps(obj) -> str:
    return json.dumps(obj, separators=(",", ":"), sort_keys=True)


def parse(v):
    return json.loads(v)


def feature_row(r: pd.Series) -> np.ndarray:
    imu = parse(r["imu_trace_json"])
    pose = parse(r["degraded_pose_json"])
    gyro = np.array([x["gyro_peak"] for x in imu], dtype=float)
    acc = np.array([x["acc_dev"] for x in imu], dtype=float)
    delta = np.array([x["frame_delta"] for x in imu], dtype=float)
    obs = np.array([1.0 if x.get("observed") else 0.0 for x in pose], dtype=float)
    xyz = np.array([[x.get("x", 0.0), x.get("y", 0.0), x.get("z", 0.0)] for x in pose], dtype=float)
    meta = parse(r["window_meta_json"])
    return np.array(
        [
            gyro.mean(),
            gyro.max(),
            gyro.std(),
            acc.mean(),
            acc.max(),
            delta.mean(),
            delta.max(),
            obs.mean(),
            np.linalg.norm(xyz[-1] - xyz[0]),
            float(meta["device_family"] == "quad_compact"),
            float(meta["motion_hint"] == "rotation_scan"),
            float(meta["motion_hint"] == "translation_return"),
        ],
        dtype=float,
    )


def train_prior_submission(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    majority = str(train["failure_type"].mode().iloc[0])
    med_unc = float(train["uncertainty"].median())
    rel = [0, 4, 9, 14]
    spans = [{"start": 8, "end": 13, "type": majority if majority != "ok" else "drift", "severity": 0.45}]
    edges = [{"current": 13, "anchor": 4}]
    rows = []
    for _, r in test.iterrows():
        rows.append(
            {
                "id": r["id"],
                "reliable_keyframes_json": jdumps(rel),
                "failure_spans_json": jdumps(spans if majority != "ok" else []),
                "anchor_edges_json": jdumps(edges if majority != "ok" else []),
                "failure_type": majority,
                "uncertainty": round(med_unc, 4),
            }
        )
    return pd.DataFrame(rows)


def degraded_pose_only(test: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in test.iterrows():
        pose = parse(r["degraded_pose_json"])
        obs = np.array([bool(x.get("observed")) for x in pose])
        xyz = np.array([[x.get("x", 0.0), x.get("y", 0.0), x.get("z", 0.0)] for x in pose], dtype=float)
        step = np.concatenate([[0.0], np.linalg.norm(np.diff(xyz, axis=0), axis=1)])
        big = step > max(0.025, np.percentile(step, 75) * 1.35)
        bad = (~obs) | big
        spans = []
        i = 0
        while i < len(bad):
            if not bad[i]:
                i += 1
                continue
            j = i
            while j + 1 < len(bad) and bad[j + 1]:
                j += 1
            typ = "lost_tracking" if (~obs[i : j + 1]).sum() >= max(1, (j - i + 1) // 2) else "drift"
            spans.append({"start": int(i), "end": int(j), "type": typ, "severity": 0.5})
            i = j + 1
        reliable = [int(k) for k in range(18) if obs[k] and not bad[k]]
        if len(reliable) > 6:
            reliable = [reliable[i] for i in np.linspace(0, len(reliable) - 1, 6).round().astype(int)]
        ftype = "lost_tracking" if any(s["type"] == "lost_tracking" for s in spans) else ("drift" if spans else "ok")
        rows.append(
            {
                "id": r["id"],
                "reliable_keyframes_json": jdumps(reliable),
                "failure_spans_json": jdumps(spans[:3]),
                "anchor_edges_json": jdumps([{"current": min(17, spans[0]["end"] + 1), "anchor": max(0, spans[0]["start"] - 3)}] if spans else []),
                "failure_type": ftype,
                "uncertainty": round(float(np.clip(0.28 + 0.4 * bad.mean(), 0, 1)), 4),
            }
        )
    return pd.DataFrame(rows)


def nearest_neighbor(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    xtr = np.vstack([feature_row(r) for _, r in train.iterrows()])
    xte = np.vstack([feature_row(r) for _, r in test.iterrows()])
    mu = xtr.mean(axis=0)
    sd = xtr.std(axis=0)
    sd[sd == 0] = 1.0
    xtr = (xtr - mu) / sd
    xte = (xte - mu) / sd
    rows = []
    for i, (_, r) in enumerate(test.iterrows()):
        j = int(np.argmin(np.linalg.norm(xtr - xte[i], axis=1)))
        src = train.iloc[j]
        rows.append({c: src[c] for c in REQUIRED_COLUMNS if c != "id"} | {"id": r["id"]})
    return pd.DataFrame(rows)[REQUIRED_COLUMNS]


def _copy_nearest(train: pd.DataFrame, test: pd.DataFrame, xtr: np.ndarray, xte: np.ndarray) -> pd.DataFrame:
    mu = xtr.mean(axis=0)
    sd = xtr.std(axis=0)
    sd[sd == 0] = 1.0
    xtr = (xtr - mu) / sd
    xte = (xte - mu) / sd
    rows = []
    for i, (_, r) in enumerate(test.iterrows()):
        j = int(np.argmin(np.linalg.norm(xtr - xte[i], axis=1)))
        src = train.iloc[j]
        rows.append({c: src[c] for c in REQUIRED_COLUMNS if c != "id"} | {"id": r["id"]})
    return pd.DataFrame(rows)[REQUIRED_COLUMNS]


def id_hash_only(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    def feat(df: pd.DataFrame) -> np.ndarray:
        vals = []
        for s in df["id"].astype(str):
            hx = s.replace("hvit_", "")
            vals.append([int(hx[i : i + 3], 16) / 4095.0 for i in range(0, min(len(hx), 18), 3)])
        return np.asarray(vals, dtype=float)

    return _copy_nearest(train, test, feat(train), feat(test))


def file_size_only(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    def feat(df: pd.DataFrame) -> np.ndarray:
        vals = []
        for _, r in df.iterrows():
            p = ROOT / "public" / str(r["image"])
            vals.append([float(p.stat().st_size)])
        return np.asarray(vals, dtype=float)

    return _copy_nearest(train, test, feat(train), feat(test))


def path_hash_only(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    def feat(df: pd.DataFrame) -> np.ndarray:
        vals = []
        for _, r in df.iterrows():
            h = int.from_bytes(str(r["image"]).encode("utf-8"), "little", signed=False)
            vals.append([float(h % 9973) / 9973.0, float(h % 65537) / 65537.0])
        return np.asarray(vals, dtype=float)

    return _copy_nearest(train, test, feat(train), feat(test))


def source_lookup_probe(train: pd.DataFrame, test: pd.DataFrame) -> dict:
    forbidden = re.compile(r"MIO\\d+|MGO\\d+|short_|\\d{10,}|\\.png|\\.zip", re.I)
    public_text = "\n".join(train.astype(str).agg(" ".join, axis=1).tolist() + test.astype(str).agg(" ".join, axis=1).tolist())
    exact_panel_names = [Path(p).name for p in train["image"].tolist() + test["image"].tolist()]
    return {
        "forbidden_public_tokens": bool(forbidden.search(public_text)),
        "panel_name_count": len(exact_panel_names),
        "panel_names_unique": len(exact_panel_names) == len(set(exact_panel_names)),
        "train_test_ids_overlap": bool(set(train["id"]) & set(test["id"])),
    }


def image_feature(img: Image.Image) -> np.ndarray:
    gray = ImageOps.autocontrast(img.convert("L").resize((64, 48), Image.Resampling.BILINEAR))
    arr = np.asarray(gray, dtype=np.float32) / 255.0
    edge = np.asarray(gray.filter(ImageFilter.FIND_EDGES), dtype=np.float32) / 255.0
    hist = np.histogram(arr, bins=24, range=(0, 1), density=True)[0].astype(np.float32)
    ehist = np.histogram(edge, bins=16, range=(0, 1), density=True)[0].astype(np.float32)
    feat = np.concatenate([hist, ehist, [arr.mean(), arr.std(), edge.mean(), edge.std()]]).astype(np.float32)
    norm = np.linalg.norm(feat)
    return feat / norm if norm else feat


def dense_image_feature(img: Image.Image) -> np.ndarray:
    gray = ImageOps.autocontrast(img.convert("L").resize((32, 24), Image.Resampling.BILINEAR))
    arr = np.asarray(gray, dtype=np.float32) / 255.0
    edge = np.asarray(gray.filter(ImageFilter.FIND_EDGES), dtype=np.float32) / 255.0
    feat = np.concatenate([arr.ravel(), edge.ravel()]).astype(np.float32)
    feat -= float(feat.mean())
    norm = np.linalg.norm(feat)
    return feat / norm if norm else feat


def crop_variants(img: Image.Image):
    gray = img.convert("L")
    w, h = gray.size
    for frac in [0.56, 0.72, 0.88]:
        crop_w, crop_h = int(w * frac), int(h * frac)
        xs = [0, max(0, (w - crop_w) // 2), max(0, w - crop_w)]
        ys = [0, max(0, (h - crop_h) // 2), max(0, h - crop_h)]
        for y in ys:
            for x in xs:
                yield gray.crop((x, y, x + crop_w, y + crop_h)).resize((160, 120), Image.Resampling.BILINEAR)
    yield gray.resize((160, 120), Image.Resampling.BILINEAR)


def _read_zip_csv(z: zipfile.ZipFile, member: str) -> pd.DataFrame:
    with z.open(member) as f:
        df = pd.read_csv(f)
    first = df.columns[0]
    if first.startswith("#timestamp"):
        df = df.rename(columns={first: "timestamp"})
    return df


def _raw_frame_features(raw_dir: Path) -> tuple[list[str], np.ndarray, dict[str, list[str]]]:
    keys, feats, seq_names = [], [], {}
    for zip_path in sorted(raw_dir.glob("*.zip")):
        seq = zip_path.stem
        with zipfile.ZipFile(zip_path) as z:
            cam = _read_zip_csv(z, f"{seq}/mav0/cam0/data.csv").sort_values("timestamp").reset_index(drop=True)
            seq_names[seq] = [Path(x).name for x in cam["filename"].astype(str).tolist()]
            for fname in seq_names[seq]:
                member = f"{seq}/mav0/cam0/data/{fname}"
                with z.open(member) as f:
                    img = Image.open(BytesIO(f.read()))
                    img.load()
                keys.append(f"{seq}/{fname}")
                feats.append(image_feature(img))
    if not feats:
        return [], np.zeros((0, 1), dtype=np.float32), {}
    return keys, np.vstack(feats), seq_names


def _raw_crop_features(raw_dir: Path) -> tuple[dict[str, list[np.ndarray]], dict[str, list[str]]]:
    seq_feats: dict[str, list[np.ndarray]] = {}
    seq_names: dict[str, list[str]] = {}
    for zip_path in sorted(raw_dir.glob("*.zip")):
        seq = zip_path.stem
        feats = []
        with zipfile.ZipFile(zip_path) as z:
            cam = _read_zip_csv(z, f"{seq}/mav0/cam0/data.csv").sort_values("timestamp").reset_index(drop=True)
            names = [Path(x).name for x in cam["filename"].astype(str).tolist()]
            seq_names[seq] = names
            for fname in names:
                member = f"{seq}/mav0/cam0/data/{fname}"
                with z.open(member) as f:
                    img = Image.open(BytesIO(f.read()))
                    img.load()
                feats.append(np.vstack([dense_image_feature(v) for v in crop_variants(img)]).astype(np.float32))
        seq_feats[seq] = feats
    return seq_feats, seq_names


def visual_source_retrieval_probe(train: pd.DataFrame, test: pd.DataFrame, raw_dir: Path, max_rows: int = 160) -> dict:
    source_map_path = ROOT / "private" / "source_map_audit_only.csv"
    if not raw_dir.exists() or not source_map_path.exists():
        return {"available": False}
    source_map = pd.read_csv(source_map_path).set_index("id")
    public_rows = pd.concat(
        [train[["id", "image"]].assign(split="train"), test[["id", "image"]].assign(split="test")],
        ignore_index=True,
    )
    public_rows = public_rows.sort_values("id").head(max_rows)
    raw_keys, raw_feats, seq_names = _raw_frame_features(raw_dir)
    if not raw_keys:
        return {"available": False}
    raw_index = {k: i for i, k in enumerate(raw_keys)}
    top1 = top5 = total = missing_truth = 0
    for _, r in public_rows.iterrows():
        if r["id"] not in source_map.index:
            continue
        sm = source_map.loc[r["id"]]
        seq = str(sm["source_seq"])
        start = int(sm["start_keyframe"])
        names = seq_names.get(seq, [])
        panel = Image.open(ROOT / "public" / str(r["image"])).convert("L")
        tiles = [
            panel.crop((0, 0, 160, 120)),
            panel.crop((160, 0, 320, 120)),
            panel.crop((0, 120, 160, 240)),
            panel.crop((160, 120, 320, 240)),
        ]
        for tile, local_ix in zip(tiles, [0, 5, 11, 17]):
            truth_ix = start + local_ix
            if truth_ix >= len(names):
                missing_truth += 1
                continue
            truth_key = f"{seq}/{names[truth_ix]}"
            if truth_key not in raw_index:
                missing_truth += 1
                continue
            q = image_feature(tile)
            dist = np.linalg.norm(raw_feats - q[None, :], axis=1)
            order = np.argpartition(dist, min(5, len(dist) - 1))[:5]
            order = order[np.argsort(dist[order])]
            total += 1
            if raw_index[truth_key] == int(order[0]):
                top1 += 1
            if raw_index[truth_key] in {int(x) for x in order[:5]}:
                top5 += 1
    return {
        "available": True,
        "queries": total,
        "missing_truth": missing_truth,
        "exact_frame_top1": round(top1 / total, 4) if total else None,
        "exact_frame_top5": round(top5 / total, 4) if total else None,
    }


def visual_window_retrieval_probe(train: pd.DataFrame, test: pd.DataFrame, raw_dir: Path, max_rows: int = 120) -> dict:
    source_map_path = ROOT / "private" / "source_map_audit_only.csv"
    if not raw_dir.exists() or not source_map_path.exists():
        return {"available": False}
    source_map = pd.read_csv(source_map_path).set_index("id")
    public_rows = pd.concat(
        [train[["id", "image"]].assign(split="train"), test[["id", "image"]].assign(split="test")],
        ignore_index=True,
    )
    public_rows = public_rows.sort_values("id").head(max_rows)
    seq_feats, seq_names = _raw_crop_features(raw_dir)
    if not seq_feats:
        return {"available": False}
    offsets = [0, 5, 11, 17]
    window_top1 = window_top5 = sequence_top1 = total = missing_truth = 0
    for _, r in public_rows.iterrows():
        if r["id"] not in source_map.index:
            continue
        sm = source_map.loc[r["id"]]
        truth = (str(sm["source_seq"]), int(sm["start_keyframe"]))
        if truth[0] not in seq_feats or truth[1] + max(offsets) >= len(seq_feats[truth[0]]):
            missing_truth += 1
            continue
        panel = Image.open(ROOT / "public" / str(r["image"])).convert("L")
        tiles = [
            panel.crop((0, 0, 160, 120)),
            panel.crop((160, 0, 320, 120)),
            panel.crop((0, 120, 160, 240)),
            panel.crop((160, 120, 320, 240)),
        ]
        q_feats = [dense_image_feature(tile) for tile in tiles]
        candidates = []
        for seq, frame_feats in seq_feats.items():
            max_start = len(frame_feats) - max(offsets) - 1
            for start in range(max_start + 1):
                score = 0.0
                for q, off in zip(q_feats, offsets):
                    score += float((frame_feats[start + off] @ q).max())
                candidates.append((score, seq, start))
        candidates.sort(reverse=True)
        pred = [(seq, start) for _, seq, start in candidates[:5]]
        total += 1
        if pred and pred[0] == truth:
            window_top1 += 1
        if pred and pred[0][0] == truth[0]:
            sequence_top1 += 1
        if truth in pred:
            window_top5 += 1
    return {
        "available": True,
        "rows": total,
        "missing_truth": missing_truth,
        "window_top1": round(window_top1 / total, 4) if total else None,
        "window_top5": round(window_top5 / total, 4) if total else None,
        "sequence_top1": round(sequence_top1 / total, 4) if total else None,
    }


def main() -> int:
    train = pd.read_csv(ROOT / "public" / "train.csv")
    test = pd.read_csv(ROOT / "public" / "test.csv")
    answers = pd.read_csv(ROOT / "private" / "answers.csv")
    sample = pd.read_csv(ROOT / "public" / "sample_submission.csv")
    baselines = {
        "sample": sample,
        "metadata_train_prior": train_prior_submission(train, test),
        "degraded_pose_only": degraded_pose_only(test),
        "simple_cpu_feature_nn": nearest_neighbor(train, test),
        "id_hash_only": id_hash_only(train, test),
        "file_size_only": file_size_only(train, test),
        "path_hash_only": path_hash_only(train, test),
        "perfect": answers[REQUIRED_COLUMNS],
    }
    print("Scores")
    for name, sub in baselines.items():
        print(f"{name}: {grade(sub, answers):.6f}")
    print("\nPrivate subgroup counts")
    for c in ["group_device", "group_motion", "group_failure_type"]:
        print(c, answers[c].value_counts().to_dict())
    print("\nSource lookup probe")
    print(json.dumps(source_lookup_probe(train, test), indent=2, sort_keys=True))
    print("\nVisual source retrieval probe")
    print(json.dumps(visual_source_retrieval_probe(train, test, ROOT / "raw_sources"), indent=2, sort_keys=True))
    print("\nCrop-aware window retrieval probe")
    print(json.dumps(visual_window_retrieval_probe(train, test, ROOT / "raw_sources"), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

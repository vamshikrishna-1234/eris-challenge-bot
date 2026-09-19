import argparse
import json
import re
import tempfile
import zipfile
from pathlib import Path

import cv2
import numpy as np
import pandas as pd


RGB_RE = re.compile(r"(?:^|/)panda_pyrep_rgb_(\d+)\.avi$")
CROP_VARIANTS = ("full", "center", "left", "right")
SIGNATURE_FRAMES = 12
SIGNATURE_SIZE = (32, 24)


def _find_raw_zip(root: Path) -> Path | None:
    if root.is_file() and root.suffix.lower() == ".zip":
        return root
    if root.is_dir():
        candidates = sorted(root.rglob("*.zip"))
        for candidate in candidates:
            if "PandaHandover" in candidate.name or "Real_Val" in candidate.name:
                return candidate
        if len(candidates) == 1:
            return candidates[0]
    return None


def _raw_reader(raw: Path):
    raw = Path(raw)
    raw_zip = _find_raw_zip(raw)
    if raw_zip is not None:
        zf = zipfile.ZipFile(raw_zip)
        members = {}
        for name in zf.namelist():
            match = RGB_RE.search(name.replace("\\", "/"))
            if match:
                members[match.group(1)] = name
        if not members:
            zf.close()
            raise SystemExit(f"no source RGB videos found in {raw_zip}")

        def read_video(raw_id: str) -> bytes:
            return zf.read(members[raw_id])

        return sorted(members), read_video, zf.close

    if not raw.is_dir():
        raise SystemExit(f"raw path is not a ZIP or directory: {raw}")
    paths = {}
    for path in raw.rglob("panda_pyrep_rgb_*.avi"):
        match = RGB_RE.search(path.as_posix())
        if match:
            paths[match.group(1)] = path
    if not paths:
        raise SystemExit(f"no source RGB videos found under {raw}")

    def read_video(raw_id: str) -> bytes:
        return paths[raw_id].read_bytes()

    return sorted(paths), read_video, lambda: None


def _sample_frames(path: Path, n_frames: int = SIGNATURE_FRAMES):
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError(f"could not open video: {path}")
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if count <= 0:
        cap.release()
        raise ValueError(f"video has no frames: {path}")
    indices = np.rint(np.linspace(0, count - 1, n_frames)).astype(int)
    frames = []
    last = None
    for frame_i in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_i))
        ok, frame = cap.read()
        if not ok:
            frame = last
        if frame is None:
            continue
        last = frame
        frames.append(frame)
    cap.release()
    if len(frames) < max(4, n_frames // 3):
        raise ValueError(f"too few readable frames: {path}")
    return frames


def _crop(frame, mode: str):
    h, w = frame.shape[:2]
    if mode == "center":
        x0, x1 = int(0.12 * w), int(0.88 * w)
        y0, y1 = int(0.08 * h), int(0.92 * h)
    elif mode == "left":
        x0, x1 = 0, int(0.78 * w)
        y0, y1 = int(0.05 * h), int(0.95 * h)
    elif mode == "right":
        x0, x1 = int(0.22 * w), w
        y0, y1 = int(0.05 * h), int(0.95 * h)
    else:
        x0, x1 = 0, w
        y0, y1 = 0, h
    if x1 <= x0 + 16 or y1 <= y0 + 16:
        return frame
    return frame[y0:y1, x0:x1]


def _signature_from_frames(frames, crop_mode: str):
    parts = []
    for frame in frames:
        cropped = _crop(frame, crop_mode)
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, SIGNATURE_SIZE, interpolation=cv2.INTER_AREA).astype(np.float32)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        edge_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        edge_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        edge = cv2.magnitude(edge_x, edge_y)
        for arr in (gray, edge):
            arr = arr - float(arr.mean())
            arr = arr / (float(arr.std()) + 1e-6)
            parts.append(arr.reshape(-1))
    vec = np.concatenate(parts).astype(np.float32)
    return vec / (float(np.linalg.norm(vec)) + 1e-6)


def _signatures_from_bytes(data: bytes, suffix: str, crop_modes):
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(data)
        tmp_path = Path(tmp.name)
    try:
        frames = _sample_frames(tmp_path)
        return [_signature_from_frames(frames, mode) for mode in crop_modes]
    finally:
        tmp_path.unlink(missing_ok=True)


def _signature_from_public_video(path: Path):
    frames = _sample_frames(path)
    return _signature_from_frames(frames, "full")


def _load_public_rows(public: Path, private: Path, split: str):
    source_map_path = private / "source_map.csv"
    if not source_map_path.exists():
        raise SystemExit("private/source_map.csv is required; rerun prepare.py from the updated challenge")
    source_map = pd.read_csv(source_map_path, dtype=str)
    if set(source_map.columns) != {"id", "raw_id", "subset"}:
        raise SystemExit("private/source_map.csv has unexpected columns")
    frames = []
    for name in ("train", "test"):
        csv_path = public / f"{name}.csv"
        if csv_path.exists():
            df = pd.read_csv(csv_path, dtype=str)
            df["subset"] = name
            frames.append(df[["id", "rgb_video", "subset"]])
    if not frames:
        raise SystemExit("public train/test CSVs are missing")
    rows = pd.concat(frames, ignore_index=True).merge(source_map, on=["id", "subset"], how="inner")
    if split != "all":
        rows = rows[rows["subset"] == split].reset_index(drop=True)
    if rows.empty:
        raise SystemExit(f"no public rows available for split={split}")
    return rows


def main():
    parser = argparse.ArgumentParser(description="Probe prepared video source lookup against official raw RGB videos.")
    parser.add_argument("--raw", type=Path, required=True, help="Official ZIP or extracted raw directory.")
    parser.add_argument("--public", type=Path, required=True, help="Prepared public directory.")
    parser.add_argument("--private", type=Path, required=True, help="Prepared private directory with source_map.csv.")
    parser.add_argument("--split", choices=["test", "train", "all"], default="test")
    parser.add_argument("--limit-public", type=int, default=0, help="Optional row cap for quick local probes.")
    parser.add_argument("--max-raw", type=int, default=0, help="Optional raw-source cap for debugging only.")
    parser.add_argument("--top1-threshold", type=float, default=0.10)
    parser.add_argument("--top5-threshold", type=float, default=0.25)
    parser.add_argument("--no-fail", action="store_true", help="Report rates without failing threshold breaches.")
    args = parser.parse_args()

    raw_ids, read_raw_video, close_raw = _raw_reader(args.raw)
    try:
        if args.max_raw:
            raw_ids = raw_ids[: args.max_raw]
        raw_vectors = []
        raw_variant_ids = []
        for i, raw_id in enumerate(raw_ids, 1):
            vectors = _signatures_from_bytes(read_raw_video(raw_id), ".avi", CROP_VARIANTS)
            raw_vectors.extend(vectors)
            raw_variant_ids.extend([raw_id] * len(vectors))
            if i % 100 == 0:
                print(f"indexed {i} raw RGB videos", flush=True)
    finally:
        close_raw()
    raw_matrix = np.vstack(raw_vectors).astype(np.float32)

    rows = _load_public_rows(args.public, args.private, args.split)
    if args.limit_public:
        rows = rows.iloc[: args.limit_public].reset_index(drop=True)
    raw_id_set = set(raw_ids)
    rows = rows[rows["raw_id"].isin(raw_id_set)].reset_index(drop=True)
    if rows.empty:
        raise SystemExit("no public rows have raw IDs present in the indexed source pool")

    top1_hits = 0
    top5_hits = 0
    examples = []
    for _, row in rows.iterrows():
        public_video = args.public / str(row["rgb_video"])
        vec = _signature_from_public_video(public_video)
        similarities = raw_matrix @ vec
        order = np.argsort(-similarities)
        ranked = []
        seen = set()
        for idx in order:
            raw_id = raw_variant_ids[int(idx)]
            if raw_id in seen:
                continue
            ranked.append(raw_id)
            seen.add(raw_id)
            if len(ranked) >= 10:
                break
        gold = str(row["raw_id"])
        top1_hits += int(ranked[:1] == [gold])
        top5_hits += int(gold in ranked[:5])
        if len(examples) < 8:
            examples.append(
                {
                    "public_id": row["id"],
                    "gold_raw_id": gold,
                    "top5_raw_ids": ranked[:5],
                    "hit_top1": ranked[:1] == [gold],
                    "hit_top5": gold in ranked[:5],
                }
            )

    n = int(len(rows))
    report = {
        "n_public_rows": n,
        "n_raw_videos_indexed": int(len(raw_ids)),
        "raw_variants_per_video": len(CROP_VARIANTS),
        "split": args.split,
        "top1_recovery_rate": top1_hits / n,
        "top5_recovery_rate": top5_hits / n,
        "top1_threshold": args.top1_threshold,
        "top5_threshold": args.top5_threshold,
        "examples": examples,
    }
    print(json.dumps(report, indent=2))
    if not args.no_fail:
        if report["top1_recovery_rate"] > args.top1_threshold or report["top5_recovery_rate"] > args.top5_threshold:
            raise SystemExit("source lookup probe exceeded configured recovery thresholds")


if __name__ == "__main__":
    main()

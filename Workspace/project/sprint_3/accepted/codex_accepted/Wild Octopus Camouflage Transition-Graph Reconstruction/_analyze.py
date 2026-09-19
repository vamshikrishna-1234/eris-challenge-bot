"""Shortcut, integrity, and CPU-baseline audit for the prepared MEVA split."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import tempfile
import zipfile
from pathlib import Path

import cv2
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
ID_RE = re.compile(r"^item_[0-9a-f]{18}$")
SOURCE_RE = re.compile(r"2018-|G3|G4|\.r13|\.avi|activities|types|school|hospital|bus")


def _grade_module():
    spec = importlib.util.spec_from_file_location("meva_grade", ROOT / "grade.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _frame_signature(path: Path) -> np.ndarray:
    cap = cv2.VideoCapture(str(path))
    ok, frame = cap.read()
    cap.release()
    if not ok or frame is None:
        raise RuntimeError(f"cannot decode {path}")
    gray = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (16, 16), interpolation=cv2.INTER_AREA)
    return (gray >= np.median(gray)).astype(np.uint8).reshape(-1)


def _hamming(a: np.ndarray, b: np.ndarray) -> int:
    return int(np.count_nonzero(a != b))


def audit(raw: Path | None = None) -> dict[str, object]:
    public = ROOT / "prepared" / "public"
    private = ROOT / "prepared" / "private" / "answers.csv"
    train = pd.read_csv(public / "train.csv")
    test = pd.read_csv(public / "test.csv")
    sample = pd.read_csv(public / "sample_submission.csv")
    answers = pd.read_csv(private)
    ids = list(test["id"].astype(str))
    source_tokens = [str(x) for x in train["video"].tolist() + test["video"].tolist()]
    public_tokens = "\n".join(train.astype(str).to_numpy().ravel().tolist() + test.astype(str).to_numpy().ravel().tolist())
    public_paths = [public / str(x) for x in train["video"].tolist() + test["video"].tolist()]
    public_sizes = [p.stat().st_size for p in public_paths if p.is_file()]
    result: dict[str, object] = {
        "rows": {"train": len(train), "test": len(test)},
        "id_format_ok": all(ID_RE.fullmatch(x) for x in ids) and len(set(ids)) == len(ids),
        "source_tokens_in_public_csv": bool(SOURCE_RE.search(public_tokens)),
        "absolute_paths": any(":\\" in x or x.startswith("/") for x in source_tokens),
        "public_media_bytes": sum(p.stat().st_size for p in (public / "train" / "videos").glob("*.mp4")) +
                              sum(p.stat().st_size for p in (public / "test" / "videos").glob("*.mp4")),
        "public_media_count": len(list((public / "train" / "videos").glob("*.mp4"))) +
                              len(list((public / "test" / "videos").glob("*.mp4"))),
        "public_size_bytes": {
            "count": len(public_sizes),
            "min": min(public_sizes) if public_sizes else None,
            "max": max(public_sizes) if public_sizes else None,
            "all_equal": bool(public_sizes) and len(set(public_sizes)) == 1,
        },
    }
    # A metadata-only prediction is an empty graph for every row. It is scored
    # only against the private answers and is a deliberately weak lower baseline.
    grade = _grade_module()
    empty = pd.DataFrame({"id": ids, "graph_json": [json.dumps({"nodes": [], "edges": []}, separators=(",", ":"))] * len(ids)})
    result["empty_graph_score"] = float(grade.grade(empty, answers))
    result["sample_score"] = float(grade.grade(sample, answers))

    # Perceptual retrieval probe: transformed public frames should not be near
    # exact matches to the raw source frames. This optional path is intentionally
    # small and reports a distance rather than a score used by grade.py.
    if raw is not None:
        raw = Path(raw)
        public_paths = [public / str(x) for x in test["video"].head(24)]
        public_sigs = [_frame_signature(p) for p in public_paths]
        raw_sigs: list[np.ndarray] = []
        with tempfile.TemporaryDirectory(prefix="meva_lookup_probe_") as td:
            td_path = Path(td)
            if raw.is_file() and raw.suffix.lower() == ".zip":
                with zipfile.ZipFile(raw) as z:
                    members = [n for n in z.namelist() if n.lower().endswith((".avi", ".mp4"))]
                    for name in members[:6]:
                        target = td_path / Path(name).name
                        with z.open(name) as src, target.open("wb") as dst:
                            dst.write(src.read())
                        cap = cv2.VideoCapture(str(target))
                        for _ in range(0, 9000, 180):
                            cap.set(cv2.CAP_PROP_POS_FRAMES, _)
                            ok, frame = cap.read()
                            if ok and frame is not None:
                                gray = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (16, 16), interpolation=cv2.INTER_AREA)
                                raw_sigs.append((gray >= np.median(gray)).astype(np.uint8).reshape(-1))
                        cap.release()
            else:
                for path in sorted(raw.rglob("*.avi"))[:6]:
                    cap = cv2.VideoCapture(str(path))
                    for _ in range(0, 9000, 180):
                        cap.set(cv2.CAP_PROP_POS_FRAMES, _)
                        ok, frame = cap.read()
                        if ok and frame is not None:
                            gray = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (16, 16), interpolation=cv2.INTER_AREA)
                            raw_sigs.append((gray >= np.median(gray)).astype(np.uint8).reshape(-1))
                    cap.release()
        distances = [min((_hamming(sig, raw_sig) for raw_sig in raw_sigs), default=256) for sig in public_sigs]
        result["retrieval_probe"] = {"public_samples": len(distances), "raw_samples": len(raw_sigs),
                                      "min_hamming": min(distances, default=None),
                                      "median_hamming": float(np.median(distances)) if distances else None,
                                      "near_exact_lt_8": sum(d < 8 for d in distances)}
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=None, help="optional raw tree or OFFICIAL_RAW_FILES_ONLY.zip")
    parser.add_argument("--out", type=Path, default=ROOT / "ANALYSIS.json")
    args = parser.parse_args()
    result = audit(args.raw)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

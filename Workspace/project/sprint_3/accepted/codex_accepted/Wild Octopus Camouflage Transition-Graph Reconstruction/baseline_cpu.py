"""Tiny CPU reference: motion score + train-only modal graph prior."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import cv2
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent


def motion_score(path: Path) -> float:
    cap = cv2.VideoCapture(str(path))
    prev = None
    values = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        gray = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (64, 64), interpolation=cv2.INTER_AREA)
        if prev is not None:
            values.append(float(np.mean(cv2.absdiff(gray, prev))))
        prev = gray
    cap.release()
    return float(np.median(values)) if values else 0.0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "baseline_submission.csv")
    args = parser.parse_args()
    public = ROOT / "prepared" / "public"
    train = pd.read_csv(public / "train.csv")
    test = pd.read_csv(public / "test.csv")
    graphs = train["graph_json"].map(json.loads).tolist()
    modal = max(graphs, key=lambda g: (len(g["nodes"]), len(g["edges"])))
    modal_json = json.dumps(modal, sort_keys=True, separators=(",", ":"))
    empty_json = json.dumps({"nodes": [], "edges": []}, separators=(",", ":"))
    t0 = time.perf_counter()
    train_motion = np.asarray([motion_score(public / str(p)) for p in train["video"]], dtype=float)
    test_motion = np.asarray([motion_score(public / str(p)) for p in test["video"]], dtype=float)
    threshold = float(np.median(train_motion))
    pred = [modal_json if value >= threshold else empty_json for value in test_motion]
    pd.DataFrame({"id": test["id"], "graph_json": pred}).to_csv(args.out, index=False, lineterminator="\n")
    print(json.dumps({"seconds": round(time.perf_counter() - t0, 3), "threshold": threshold,
                      "train_items": len(train), "test_items": len(test)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

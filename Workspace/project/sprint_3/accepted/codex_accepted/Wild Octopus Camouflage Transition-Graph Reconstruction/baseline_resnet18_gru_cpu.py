"""Frozen ResNet-18 frame embeddings plus a small GRU graph-prototype decoder.

This is an organizer-side runtime probe for CPU feasibility. It intentionally
emits only valid graph JSON by decoding to train-derived graph prototypes.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from collections import Counter
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from torchvision.models import ResNet18_Weights, resnet18


ROOT = Path(__file__).resolve().parent
EMPTY_GRAPH = json.dumps({"nodes": [], "edges": []}, separators=(",", ":"))


def _read_video_tensor(path: Path, frames_per_clip: int) -> torch.Tensor:
    cap = cv2.VideoCapture(str(path))
    frames: list[np.ndarray] = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
        frames.append(frame)
    cap.release()
    if not frames:
        frames = [np.zeros((224, 224, 3), dtype=np.uint8)]
    if len(frames) >= frames_per_clip:
        idx = np.linspace(0, len(frames) - 1, frames_per_clip).round().astype(int)
        frames = [frames[i] for i in idx]
    else:
        frames = frames + [frames[-1]] * (frames_per_clip - len(frames))
    arr = np.stack(frames).astype(np.float32) / 255.0
    arr = (arr - np.array([0.485, 0.456, 0.406], dtype=np.float32)) / np.array(
        [0.229, 0.224, 0.225], dtype=np.float32
    )
    return torch.from_numpy(arr).permute(0, 3, 1, 2).contiguous()


def _make_encoder(weights_name: str) -> nn.Module:
    weights = None
    if weights_name == "imagenet":
        weights = ResNet18_Weights.DEFAULT
    model = resnet18(weights=weights)
    model.fc = nn.Identity()
    model.eval()
    for param in model.parameters():
        param.requires_grad_(False)
    return model


@torch.inference_mode()
def _extract_features(
    rows: pd.DataFrame,
    public: Path,
    encoder: nn.Module,
    frames_per_clip: int,
    batch_size: int,
) -> np.ndarray:
    features: list[np.ndarray] = []
    pending: list[torch.Tensor] = []
    lengths: list[int] = []
    for video in rows["video"].tolist():
        tensor = _read_video_tensor(public / str(video), frames_per_clip)
        pending.append(tensor)
        lengths.append(tensor.shape[0])
        stacked = torch.cat(pending, dim=0)
        if stacked.shape[0] >= batch_size:
            encoded = []
            for start in range(0, stacked.shape[0], batch_size):
                encoded.append(encoder(stacked[start : start + batch_size]).cpu())
            encoded_tensor = torch.cat(encoded, dim=0)
            offset = 0
            for length in lengths:
                features.append(encoded_tensor[offset : offset + length].numpy())
                offset += length
            pending.clear()
            lengths.clear()
    if pending:
        stacked = torch.cat(pending, dim=0)
        encoded = []
        for start in range(0, stacked.shape[0], batch_size):
            encoded.append(encoder(stacked[start : start + batch_size]).cpu())
        encoded_tensor = torch.cat(encoded, dim=0)
        offset = 0
        for length in lengths:
            features.append(encoded_tensor[offset : offset + length].numpy())
            offset += length
    return np.stack(features).astype(np.float32)


class TinyGRUDecoder(nn.Module):
    def __init__(self, feature_dim: int, hidden_dim: int, classes: int) -> None:
        super().__init__()
        self.gru = nn.GRU(feature_dim, hidden_dim, batch_first=True)
        self.head = nn.Linear(hidden_dim, classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        _, hidden = self.gru(x)
        return self.head(hidden[-1])


def _canonical(value: str) -> str:
    return json.dumps(json.loads(value), sort_keys=True, separators=(",", ":"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=6)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--frames", type=int, default=32)
    parser.add_argument("--threads", type=int, default=min(10, os.cpu_count() or 1))
    parser.add_argument("--hidden", type=int, default=64)
    parser.add_argument("--top-prototypes", type=int, default=16)
    parser.add_argument("--weights", choices=["none", "imagenet"], default="none")
    parser.add_argument("--out", type=Path, default=ROOT / "resnet18_gru_submission.csv")
    args = parser.parse_args()

    torch.set_num_threads(args.threads)
    torch.manual_seed(20260715)
    np.random.seed(20260715)
    t0 = time.perf_counter()

    public = ROOT / "prepared" / "public"
    private = ROOT / "prepared" / "private"
    train = pd.read_csv(public / "train.csv")
    test = pd.read_csv(public / "test.csv")
    answers = pd.read_csv(private / "answers.csv")

    encoder = _make_encoder(args.weights)
    t_features = time.perf_counter()
    x_train = _extract_features(train, public, encoder, args.frames, args.batch_size)
    x_test = _extract_features(test, public, encoder, args.frames, args.batch_size)
    feature_seconds = time.perf_counter() - t_features

    mean = x_train.mean(axis=(0, 1), keepdims=True)
    std = x_train.std(axis=(0, 1), keepdims=True) + 1e-6
    x_train = (x_train - mean) / std
    x_test = (x_test - mean) / std

    counts = Counter(_canonical(v) for v in train["graph_json"].tolist())
    positives = [g for g, _ in counts.most_common() if g != EMPTY_GRAPH]
    prototypes = [EMPTY_GRAPH] + positives[: max(1, args.top_prototypes - 1)]
    proto_to_idx = {g: i for i, g in enumerate(prototypes)}
    fallback_positive = 1 if len(prototypes) > 1 else 0
    y = np.array([proto_to_idx.get(_canonical(v), fallback_positive) for v in train["graph_json"]], dtype=np.int64)

    x_tensor = torch.from_numpy(x_train)
    y_tensor = torch.from_numpy(y)
    dataset = TensorDataset(x_tensor, y_tensor)
    loader = DataLoader(dataset, batch_size=32, shuffle=True, generator=torch.Generator().manual_seed(20260715))

    model = TinyGRUDecoder(x_train.shape[-1], args.hidden, len(prototypes))
    class_counts = np.bincount(y, minlength=len(prototypes)).astype(np.float32)
    weights = 1.0 / np.sqrt(np.maximum(class_counts, 1.0))
    weights = weights / weights.mean()
    loss_fn = nn.CrossEntropyLoss(weight=torch.from_numpy(weights))
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3, weight_decay=1e-3)

    t_train = time.perf_counter()
    model.train()
    for _ in range(args.epochs):
        for xb, yb in loader:
            opt.zero_grad(set_to_none=True)
            loss = loss_fn(model(xb), yb)
            loss.backward()
            opt.step()
    train_seconds = time.perf_counter() - t_train

    model.eval()
    with torch.inference_mode():
        logits = model(torch.from_numpy(x_test))
        pred_idx = logits.argmax(dim=1).cpu().numpy().tolist()
    pred_graphs = [prototypes[i] for i in pred_idx]
    pd.DataFrame({"id": test["id"], "graph_json": pred_graphs}).to_csv(args.out, index=False, lineterminator="\n")

    import grade

    score = grade.grade(pd.read_csv(args.out), answers)
    result = {
        "batch_size": args.batch_size,
        "epochs": args.epochs,
        "feature_seconds": round(feature_seconds, 3),
        "frames_per_clip": args.frames,
        "hidden_dim": args.hidden,
        "score": round(float(score), 12),
        "test_items": int(len(test)),
        "threads": args.threads,
        "total_seconds": round(time.perf_counter() - t0, 3),
        "train_items": int(len(train)),
        "train_seconds": round(train_seconds, 3),
        "weights": args.weights,
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

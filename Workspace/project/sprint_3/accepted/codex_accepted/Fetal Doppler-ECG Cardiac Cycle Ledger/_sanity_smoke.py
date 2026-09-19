from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw

from grade import grade
from prepare import prepare


ROOT = Path(__file__).resolve().parent


def _write_record(root: Path, rec: int, fs: int = 256, duration: float = 18.0) -> None:
    n_sig = 34
    n = int(fs * duration)
    t = np.arange(n) / fs
    rng = np.random.default_rng(1000 + rec)
    maternal_rate = 1.25 + 0.05 * np.cos(rec)
    maternal_phase = (t * maternal_rate + 0.11 * rec) % 1.0
    beat_times = []
    bt = 0.35 + 0.12 * rng.random()
    while bt < duration - 0.2:
        beat_times.append(bt)
        bt += float(rng.uniform(0.34, 0.68) + 0.08 * np.sin(1.9 * bt + rec))
    fetal_peaks = np.zeros_like(t)
    beat_strength = {}
    for k, beat_t in enumerate(beat_times):
        strength = float(rng.uniform(0.45, 1.15))
        if (k + rec) % 9 == 0:
            strength *= 0.25
        beat_strength[beat_t] = strength
        fetal_peaks += strength * np.exp(-0.5 * ((t - beat_t) / 0.018) ** 2)
    maternal_peaks = np.exp(-0.5 * ((maternal_phase - 0.03) / 0.030) ** 2)
    data = rng.normal(0, 1200, size=(n, n_sig)).astype(np.int32)
    for ch in range(24):
        data[:, ch] += (9000 * fetal_peaks + 2500 * maternal_peaks + rng.normal(0, 500, n)).astype(np.int32)
    for ch in range(24, 27):
        data[:, ch] += (9000 * maternal_peaks + rng.normal(0, 700, n)).astype(np.int32)
    data[:, 31] = (50000 * np.sin(2 * np.pi * 0.25 * t) + rng.normal(0, 1000, n)).astype(np.int32)
    data[:, 32] = np.linspace(-10000, 10000, n).astype(np.int32)
    data[:, 33] = 0
    (root / "wfdb_format_ecg_and_respiration").mkdir(parents=True, exist_ok=True)
    data.astype("<i4").tofile(root / "wfdb_format_ecg_and_respiration" / f"{rec}.dat")

    names = [f"uni_abd{i}" for i in range(1, 25)] + ["bi_tho1", "bi_tho2", "bi_tho3", "dc1", "dc2", "dc3", "dc4", "matrsp", "saw", "sync"]
    lines = [f"{rec} {n_sig} {fs} {n}"]
    for name in names:
        lines.append(f"{rec}.dat 32 1000(0)/uV 0 0 0 0 0 {name}")
    (root / "wfdb_format_ecg_and_respiration" / f"{rec}.hea").write_text("\n".join(lines) + "\n", encoding="utf-8")

    (root / "pwd_images").mkdir(parents=True, exist_ok=True)
    w, h = 1440, 260
    img = Image.new("L", (w, h), 18)
    draw = ImageDraw.Draw(img)
    for x in range(0, w, 80):
        draw.line((x, 0, x, h), fill=38, width=1)
    for y in range(30, h, 40):
        draw.line((0, y, w, y), fill=34, width=1)
    for beat_t in beat_times:
        x = int(beat_t / duration * w)
        amp = int(34 + 12 * np.sin(beat_t * 1.7 + rec))
        fill_hi = int(120 + 110 * min(1.0, beat_strength[beat_t]))
        if beat_strength[beat_t] < 0.35:
            fill_hi = 80
        y0 = h // 2 - amp
        y1 = h // 2 + amp
        draw.ellipse((x - 8, y0 - 5, x + 8, y0 + 5), fill=fill_hi)
        draw.ellipse((x - 7, y1 - 4, x + 7, y1 + 4), fill=max(65, fill_hi - 25))
        draw.line((x, y0, x, y1), fill=max(60, fill_hi - 50), width=2)
    img.save(root / "pwd_images" / f"{rec}.bmp")


def _build_raw(root: Path, n_records: int = 36) -> Path:
    raw = root / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    (raw / "LICENSE.txt").write_text("ODC-By official fixture placeholder for smoke only\n", encoding="utf-8")
    records = []
    for rec in range(1, n_records + 1):
        _write_record(raw, rec)
        records.append(f"wfdb_format_ecg_and_respiration/{rec}")
    (raw / "RECORDS").write_text("\n".join(records) + "\n", encoding="utf-8")
    (raw / "SHA256SUMS.txt").write_text("smoke fixture\n", encoding="utf-8")
    return raw


def _perfect(answers: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "id": answers["id"].astype(int),
        "ledger_json": answers["ledger_json"],
        "envelope_json": answers["envelope_json"],
        "quality_json": answers["quality_json"],
        "confidence": 1.0,
    })


def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="ninfea_ledger_smoke_"))
    try:
        raw = _build_raw(tmp)
        public = tmp / "public"
        private = tmp / "private"
        prepare(raw, public, private)
        train = pd.read_csv(public / "train.csv")
        test = pd.read_csv(public / "test.csv")
        sample = pd.read_csv(public / "sample_submission.csv")
        answers = pd.read_csv(private / "answers.csv")
        assert len(train) > 0 and len(test) > 0
        perfect_score = grade(_perfect(answers), answers)
        sample_score = grade(sample, answers)
        assert abs(perfect_score - 1.0) < 1e-12, perfect_score
        assert 0.02 <= sample_score < 0.35, sample_score
        bad = sample.copy()
        bad = bad[["id", "confidence", "ledger_json", "envelope_json", "quality_json"]]
        assert grade(bad, answers) == 0.0
        malformed = _perfect(answers)
        malformed.loc[malformed.index[0], "ledger_json"] = "{not-json"
        malformed_score = grade(malformed, answers)
        assert 0.0 <= malformed_score < 1.0
        print(json.dumps({
            "train_rows": int(len(train)),
            "test_rows": int(len(test)),
            "perfect_score": perfect_score,
            "sample_score": sample_score,
            "malformed_score": malformed_score,
        }, indent=2))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()

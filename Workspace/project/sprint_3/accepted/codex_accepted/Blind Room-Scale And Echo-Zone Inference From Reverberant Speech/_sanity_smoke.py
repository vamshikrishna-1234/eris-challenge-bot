from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import soundfile as sf

from grade import InvalidSubmissionError, REQUIRED_COLUMNS, grade


ROOT = Path(__file__).resolve().parent


def _write_wav(path: Path, data: np.ndarray, sr: int = 16000) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(path, data.astype(np.float32), sr, subtype="PCM_16")


def _build_fixture(raw: Path) -> None:
    rng = np.random.default_rng(123)
    sr = 16000
    t = np.linspace(0, 1.2, int(sr * 1.2), endpoint=False)
    speech_ids = [f"tr_s{i}" for i in range(6)] + [f"te_s{i}" for i in range(5)]
    for i, sid in enumerate(speech_ids):
        tone = 0.35 * np.sin(2 * np.pi * (160 + 35 * i) * t)
        env = np.minimum(1.0, np.linspace(0, 8, len(t))) * np.minimum(1.0, np.linspace(8, 0, len(t)))
        _write_wav(raw / "speech" / f"{sid}.wav", tone * env)

    conditions = [
        ("train", 1001, "502", "Office_1", "1", "Short", 47.3, 0.32, 8.0),
        ("train", 1002, "503", "Meeting_Room_1", "2", "Long", 99.6, 0.46, 2.5),
        ("train", 1003, "508", "Lecture_Room_1", "2", "Long", 202.0, 0.64, 3.0),
        ("train", 1004, "403a", "Lecture_Room_2", "1", "Short", 370.0, 1.20, 8.5),
        ("test", 2001, "803", "Office_2", "1", "Short", 48.3, 0.39, 2.2),
        ("test", 2002, "611", "Meeting_Room_2", "2", "Long", 246.0, 0.38, 8.4),
        ("test", 2003, "EE_lobby", "Building_Lobby", "2", "Long", 72.9, 0.74, 6.4),
        ("test", 2004, "403a", "Lecture_Room_2", "2", "Long", 370.0, 1.25, 4.5),
    ]

    rows = []
    for idx, (split, session_id, room_id, room_name, room_config, dist, volume, rt60, drr) in enumerate(conditions):
        decay = np.exp(-np.arange(int(sr * 0.75)) / (sr * max(rt60 / 5.0, 0.05)))
        rir = np.zeros_like(decay)
        rir[0] = 1.0
        rir[180 + idx * 7 : 180 + idx * 7 + len(decay) - 180 - idx * 7] += 0.25 * decay[: len(decay) - 180 - idx * 7]
        _write_wav(raw / "rirs" / f"fixture_{session_id}_rir.wav", rir)
        noise = rng.normal(0, 0.08, sr * 3)
        _write_wav(raw / "noise" / f"fixture_{session_id}_noise.wav", noise)
        split_speech = [s for s in speech_ids if s.startswith("tr_")] if split == "train" else [s for s in speech_ids if s.startswith("te_")]
        for j, sid in enumerate(split_speech[:4]):
            if j % 3 == 0:
                noise_type, snr = "Ambient", 18
            elif j % 3 == 1:
                noise_type, snr = "Fan", 12
            else:
                noise_type, snr = "Babble", -1
            rows.append(
                {
                    "split": split,
                    "speech_id": sid,
                    "speech_path": f"speech/{sid}.wav",
                    "rir_path": f"rirs/fixture_{session_id}_rir.wav",
                    "noise_path": f"noise/fixture_{session_id}_noise.wav",
                    "noise_type": noise_type,
                    "snr_db": snr,
                    "session_id": session_id,
                    "room_id": room_id,
                    "room_name": room_name,
                    "room_config": room_config,
                    "distance_label": dist,
                    "volume_m3": volume,
                    "rt60": rt60,
                    "drr": drr,
                }
            )
    pd.DataFrame(rows).to_csv(raw / "fixture_manifest.csv", index=False)


def _tree_hash(root: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        h.update(path.relative_to(root).as_posix().encode("utf-8"))
        h.update(path.read_bytes())
    return h.hexdigest()


def _run_prepare(raw: Path, public: Path, private: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "prepare.py"),
            "--raw",
            str(raw),
            "--public",
            str(public),
            "--private",
            str(private),
            "--allow-fixture",
        ],
        check=True,
        cwd=ROOT,
    )


def _assert_invalid_raises(submission: pd.DataFrame, answers: pd.DataFrame, message: str) -> None:
    try:
        grade(submission, answers)
    except InvalidSubmissionError:
        return
    raise AssertionError(message)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="brs_fixture_") as td:
        base = Path(td)
        raw = base / "raw_fixture"
        raw.mkdir()
        _build_fixture(raw)

        public1 = base / "public1"
        private1 = base / "private1"
        public2 = base / "public2"
        private2 = base / "private2"
        _run_prepare(raw, public1, private1)
        _run_prepare(raw, public2, private2)
        assert _tree_hash(public1) == _tree_hash(public2), "public outputs are not deterministic"
        assert _tree_hash(private1) == _tree_hash(private2), "private outputs are not deterministic"

        answers = pd.read_csv(private1 / "answers.csv")
        sample = pd.read_csv(public1 / "sample_submission.csv")
        perfect = answers[REQUIRED_COLUMNS].copy()

        perfect_score = grade(perfect, answers)
        sample_score = grade(sample, answers)
        assert abs(perfect_score - 1.0) < 1e-12, perfect_score
        assert 0.0 <= sample_score < 0.80, sample_score

        bad = perfect.copy()
        bad = bad[["confidence", "sample_id", "room_volume_bucket", "rt60_bucket", "source_mic_distance_bucket", "echo_zone"]]
        _assert_invalid_raises(bad, answers, "reordered columns should fail")

        bad = pd.concat([perfect, perfect.iloc[[0]]], ignore_index=True)
        _assert_invalid_raises(bad, answers, "duplicate ids should fail")

        bad = perfect.iloc[:-1].copy()
        _assert_invalid_raises(bad, answers, "row-set mismatch should fail")

        bad = perfect.copy()
        bad.loc[0, "echo_zone"] = "lookup_zone"
        _assert_invalid_raises(bad, answers, "invalid categories should fail")

        bad = perfect.copy()
        bad.loc[0, "confidence"] = 1.5
        _assert_invalid_raises(bad, answers, "out-of-range confidence should fail")

        assert list(pd.read_csv(public1 / "train.csv").columns) == [
            "sample_id",
            "audio_path",
            "prompt",
            "room_volume_bucket",
            "rt60_bucket",
            "source_mic_distance_bucket",
            "echo_zone",
            "confidence",
        ]
        assert list(pd.read_csv(public1 / "test.csv").columns) == ["sample_id", "audio_path", "prompt"]
        print(f"fixture smoke passed: perfect={perfect_score:.6f}, sample={sample_score:.6f}")


if __name__ == "__main__":
    main()

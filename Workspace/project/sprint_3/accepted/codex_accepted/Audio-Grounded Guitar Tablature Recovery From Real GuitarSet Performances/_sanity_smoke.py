from __future__ import annotations

import json
import math
import sys
import tempfile
import wave
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

import grade
import prepare


def _note_ann(source_idx: int, events: list[tuple[float, float, int]]) -> dict:
    return {
        "annotation_metadata": {"data_source": str(source_idx)},
        "namespace": "note_midi",
        "data": [
            {"time": t, "duration": d, "value": float(p), "confidence": None}
            for t, d, p in events
        ],
        "sandbox": {},
        "time": 0.0,
        "duration": 7.2,
    }


def _make_jams(stem: str, shift: float) -> dict:
    # Notes are deliberately played away from the lowest-fret position so the
    # sample fallback is valid but not perfect.
    ev2 = [(0.35 + shift, 0.28, 64), (1.10 + shift, 0.22, 67), (2.05 + shift, 0.26, 69), (3.05 + shift, 0.24, 71)]
    ev3 = [(0.36 + shift, 0.18, 62), (1.60 + shift, 0.20, 65), (2.55 + shift, 0.21, 67), (4.10 + shift, 0.25, 69)]
    annotations = [_note_ann(i, []) for i in range(6)]
    annotations[4] = _note_ann(4, ev2)  # string 2
    annotations[3] = _note_ann(3, ev3)  # string 3
    annotations.append(
        {
            "annotation_metadata": {},
            "namespace": "tempo",
            "data": [{"time": 0.0, "duration": 7.2, "value": 100.0, "confidence": 1.0}],
            "sandbox": {},
        }
    )
    return {
        "annotations": annotations,
        "file_metadata": {"title": stem, "duration": 7.2, "jams_version": "0.3.4"},
        "sandbox": {},
    }


def _wav_bytes(freq: float = 220.0, sr: int = 22050, duration: float = 7.2) -> bytes:
    t = np.arange(int(sr * duration), dtype=np.float32) / sr
    y = 0.25 * np.sin(2 * math.pi * freq * t) + 0.04 * np.sin(2 * math.pi * 2.01 * freq * t)
    pcm = (np.clip(y, -1, 1) * 32767).astype("<i2")
    import io

    bio = io.BytesIO()
    with wave.open(bio, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())
    return bio.getvalue()


def _build_raw_fixture(raw: Path) -> None:
    stems = [
        "00_SS1-100-C_comp",
        "01_Funk1-114-Ab_solo",
        "04_SS1-100-C_comp",
        "05_Funk1-114-Ab_solo",
    ]
    with zipfile.ZipFile(raw / "annotation.zip", "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for i, stem in enumerate(stems):
            zf.writestr(f"{stem}.jams", json.dumps(_make_jams(stem, 0.01 * i)))
    with zipfile.ZipFile(raw / "audio_mono-mic.zip", "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for i, stem in enumerate(stems):
            zf.writestr(f"{stem}_mic.wav", _wav_bytes(220.0 + 11 * i))


def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        raw = root / "raw"
        public = root / "public"
        private = root / "private"
        raw.mkdir()
        _build_raw_fixture(raw)

        prepare.MIN_GROUP_TEST = 1
        prepare.MIN_TRAIN_ROWS = 1
        prepare.MIN_TEST_ROWS = 1
        prepare.MIN_EXACT_SIGNATURE_COUNT = 1
        prepare.MIN_TAB_VARIANTS_PER_SIGNATURE = 1
        prepare.MAX_CLIPS_PER_TRACK = 1
        prepare.SPLIT_TEST_PLAYERS = {"04", "05"}
        prepare.prepare(raw, public, private)

        train = pd.read_csv(public / "train.csv")
        test = pd.read_csv(public / "test.csv")
        answers = pd.read_csv(private / "answers.csv")
        sample = pd.read_csv(public / "sample_submission.csv")

        assert len(train) >= 1 and len(test) >= 1
        assert set(test["id"].astype(str)) == set(answers["id"].astype(str)) == set(sample["id"].astype(str))
        assert not set(train["id"].astype(str)) & set(test["id"].astype(str))
        assert all((public / p).exists() for p in train["audio_path"].tolist() + test["audio_path"].tolist())
        public_text = (public / "train.csv").read_text(encoding="utf-8") + (public / "test.csv").read_text(encoding="utf-8")
        assert "SS1-100" not in public_text and "Funk1" not in public_text and ".jams" not in public_text

        perfect = answers[["id", "tab_json"]].copy()
        perfect["confidence"] = 1.0
        perfect = perfect[grade.SUBMISSION_COLUMNS]
        perfect_score = grade.grade(perfect, answers)
        assert perfect_score == 1.0, perfect_score

        sample_score = grade.grade(sample, answers)
        assert 0.0 <= sample_score < 0.95, sample_score

        malformed = perfect.copy()
        malformed.loc[malformed.index[0], "tab_json"] = "{bad json"
        malformed_score = grade.grade(malformed, answers)
        assert 0.0 <= malformed_score < 1.0, malformed_score

        duplicate = pd.concat([perfect, perfect.iloc[[0]]], ignore_index=True)
        assert grade.grade(duplicate, answers) == 0.0
        wrong_cols = perfect[["tab_json", "id", "confidence"]]
        assert grade.grade(wrong_cols, answers) == 0.0
        bad_conf = perfect.copy()
        bad_conf.loc[bad_conf.index[0], "confidence"] = 1.5
        assert grade.grade(bad_conf, answers) == 0.0

        print(f"smoke.ok train={len(train)} test={len(test)} sample_score={sample_score:.6f} malformed_score={malformed_score:.6f}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"smoke.FAIL {exc}", file=sys.stderr)
        raise

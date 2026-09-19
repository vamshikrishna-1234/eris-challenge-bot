from __future__ import annotations

import hashlib
import math
import shutil
import tempfile
import wave
from pathlib import Path

import numpy as np
import pandas as pd

import grade as grade_mod
import prepare as prep


def _write_wav(path: Path, actor: int, sentence_idx: int, emotion: str, intensity: str) -> None:
    sr = 16000
    duration = 0.22 + 0.025 * sentence_idx
    if emotion == "ANG":
        duration += 0.03
    if emotion == "SAD":
        duration += 0.05
    n = int(round(sr * duration))
    t = np.arange(n, dtype=np.float32) / sr
    emotion_freq = {"NEU": 180, "ANG": 310, "SAD": 145, "HAP": 260, "FEA": 330, "DIS": 210}[emotion]
    intensity_gain = {"LO": 0.28, "MD": 0.42, "HI": 0.58, "XX": 0.34}[intensity]
    actor_shift = (actor % 11) * 3.0
    y = intensity_gain * np.sin(2.0 * math.pi * (emotion_freq + actor_shift) * t)
    y += 0.08 * np.sin(2.0 * math.pi * (emotion_freq * 2.1) * t)
    y *= np.linspace(0.2, 1.0, n, dtype=np.float32)
    y[:80] *= np.linspace(0.0, 1.0, 80, dtype=np.float32)
    y[-80:] *= np.linspace(1.0, 0.0, 80, dtype=np.float32)
    pcm = np.clip(y * 32767.0, -32768, 32767).astype("<i2")
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


def _make_fixture(root: Path) -> None:
    (root / "AudioWAV").mkdir(parents=True, exist_ok=True)
    (root / "SMOKE_FIXTURE_ONLY.txt").write_text(
        "Synthetic tiny fixture for local prepare/grade smoke tests only. Do not upload as challenge source.\n",
        encoding="utf-8",
    )
    (root / "LICENSE.txt").write_text("Smoke fixture only; official challenge source is CREMA-D.\n", encoding="utf-8")
    sentences = ["IEO", "TAI", "IOM"]
    clips = [
        ("NEU", "XX"),
        ("ANG", "LO"),
        ("ANG", "MD"),
        ("ANG", "HI"),
        ("SAD", "LO"),
        ("HAP", "LO"),
        ("HAP", "HI"),
        ("FEA", "HI"),
        ("DIS", "HI"),
    ]
    demo_rows = []
    for actor in range(1001, 1009):
        demo_rows.append(
            {
                "ActorID": str(actor),
                "Age": "30",
                "Sex": "Male" if actor % 2 else "Female",
                "Race": "Unknown",
                "Ethnicity": "Unknown",
            }
        )
        for sidx, sentence in enumerate(sentences):
            for emotion, intensity in clips:
                name = f"{actor}_{sentence}_{emotion}_{intensity}.wav"
                _write_wav(root / "AudioWAV" / name, actor, sidx, emotion, intensity)
    pd.DataFrame(demo_rows).to_csv(root / "VideoDemographics.csv", index=False)
    pd.DataFrame({"FileName": sorted(p.name for p in (root / "AudioWAV").glob("*.wav"))}).to_csv(
        root / "SentenceFilenames.csv", index=False
    )


def _tree_digest(path: Path) -> str:
    h = hashlib.sha256()
    for file_path in sorted(p for p in path.rglob("*") if p.is_file()):
        rel = file_path.relative_to(path).as_posix()
        if "__pycache__" in rel:
            continue
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(file_path.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def _perfect_submission(answers: pd.DataFrame) -> pd.DataFrame:
    return answers[
        ["id", "sample_id", "affect_label", "valence_shift", "arousal_shift", "escalation_tier"]
    ].assign(confidence=1.0)[prep.SUBMISSION_COLUMNS]


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="cremad_affect_smoke_") as tmp:
        root = Path(tmp)
        raw = root / "raw"
        public1 = root / "public1"
        private1 = root / "private1"
        public2 = root / "public2"
        private2 = root / "private2"
        _make_fixture(raw)

        prep.prepare(raw, public1, private1)
        prep.prepare(raw, public2, private2)
        digest1 = _tree_digest(public1) + _tree_digest(private1)
        digest2 = _tree_digest(public2) + _tree_digest(private2)
        assert digest1 == digest2, "prepare is not deterministic on the smoke fixture"

        train = pd.read_csv(public1 / "train.csv")
        test = pd.read_csv(public1 / "test.csv")
        answers = pd.read_csv(private1 / "answers.csv")
        sample = pd.read_csv(public1 / "sample_submission.csv")
        assert len(train) > 0 and len(test) > 0 and len(answers) == len(test)
        assert not set(train["sample_id"]) & set(test["sample_id"])
        assert list(test.columns) == prep.PUBLIC_TEST_COLUMNS
        assert list(sample.columns) == prep.SUBMISSION_COLUMNS

        perfect = _perfect_submission(answers)
        perfect_score = grade_mod.grade(perfect, answers)
        assert perfect_score == 1.0, f"perfect score should be exactly 1.0, got {perfect_score}"

        sample_score = grade_mod.grade(sample, answers)
        assert 0.05 <= sample_score < 0.50, f"sample score should be weak but nonzero, got {sample_score}"

        def assert_invalid(frame: pd.DataFrame) -> None:
            try:
                grade_mod.grade(frame, answers)
            except ValueError:
                return
            raise AssertionError("malformed submissions should raise ValueError")

        missing_col = sample.drop(columns=["confidence"])
        assert_invalid(missing_col)
        duplicate = pd.concat([sample.iloc[[0]], sample.iloc[[0]], sample.iloc[2:]], ignore_index=True)
        assert_invalid(duplicate)
        bad_conf = sample.copy()
        bad_conf.loc[bad_conf.index[0], "confidence"] = 1.2
        assert_invalid(bad_conf)
        bad_cat = perfect.copy()
        bad_cat.loc[bad_cat.index[0], "affect_label"] = "furious"
        assert_invalid(bad_cat)
        wrong_valid = perfect.copy()
        wrong_valid.loc[wrong_valid.index[0], "affect_label"] = next(
            label for label in grade_mod.AFFECT_LABELS if label != str(wrong_valid.loc[wrong_valid.index[0], "affect_label"])
        )
        wrong_valid_score = grade_mod.grade(wrong_valid, answers)
        assert 0.0 < wrong_valid_score < 1.0, f"one valid-but-wrong label should reduce score without invalidating, got {wrong_valid_score}"
        row_mismatch = sample.copy()
        row_mismatch.loc[row_mismatch.index[0], "sample_id"] = int(row_mismatch["sample_id"].max()) + 99
        assert_invalid(row_mismatch)

        for rel in pd.concat([train["baseline_audio"], train["current_audio"], test["baseline_audio"], test["current_audio"]]):
            assert (public1 / str(rel)).exists(), f"missing public audio {rel}"

        print(f"OK smoke: train={len(train)} test={len(test)} sample_score={sample_score:.6f} perfect=1.000000")


if __name__ == "__main__":
    main()

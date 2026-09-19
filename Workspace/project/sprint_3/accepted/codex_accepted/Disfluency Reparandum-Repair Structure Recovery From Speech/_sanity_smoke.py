from __future__ import annotations

import hashlib
import shutil
import tempfile
from pathlib import Path

import pandas as pd

from grade import SUBMISSION_COLUMNS, grade
from prepare import prepare


ROOT = Path(__file__).resolve().parent


def _file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _perfect_submission(answers: pd.DataFrame) -> pd.DataFrame:
    return answers[SUBMISSION_COLUMNS].copy()


def _run_prepare(raw: Path, base: Path) -> tuple[Path, Path]:
    public = base / "public"
    private = base / "private"
    prepare(raw, public, private)
    return public, private


def main() -> None:
    raw = ROOT / "raw_data"
    if not (raw / "clips.csv").exists():
        raise SystemExit("raw_data/clips.csv is missing. Rebuild it from official AMI source files through prepare.py.")
    with tempfile.TemporaryDirectory(prefix="disfluency_smoke_") as d1, tempfile.TemporaryDirectory(prefix="disfluency_smoke_") as d2:
        public1, private1 = _run_prepare(raw, Path(d1))
        public_hashes = {rel: _file_hash(public1 / rel) for rel in ["train.csv", "test.csv", "sample_submission.csv"]}
        answers_hash = _file_hash(private1 / "answers.csv")
        for audio_dir in [public1 / "train" / "audio", public1 / "test" / "audio"]:
            if audio_dir.exists():
                shutil.rmtree(audio_dir)
        public2, private2 = _run_prepare(raw, Path(d2))
        for rel in ["train.csv", "test.csv", "sample_submission.csv"]:
            if public_hashes[rel] != _file_hash(public2 / rel):
                raise AssertionError(f"prepare is not deterministic for {rel}")
        if answers_hash != _file_hash(private2 / "answers.csv"):
            raise AssertionError("prepare is not deterministic for answers.csv")

        answers = pd.read_csv(private1 / "answers.csv")
        sample = pd.read_csv(public1 / "sample_submission.csv")
        perfect = _perfect_submission(answers)

        perfect_score = grade(perfect, answers)
        if perfect_score != 1.0:
            raise AssertionError(f"perfect labels should score exactly 1.0, got {perfect_score}")
        sample_score = grade(sample, answers)
        if not (0.12 <= sample_score < 0.50):
            raise AssertionError(f"sample score should be in [0.12, 0.50), got {sample_score}")

        wrong_cols = sample[["id", "reparandum_span", "interregnum_span", "repair_onset", "confidence", "is_disfluency"]].copy()
        if grade(wrong_cols, answers) != 0.0:
            raise AssertionError("reordered columns should score 0")
        dup = pd.concat([sample, sample.iloc[[0]]], ignore_index=True)
        if grade(dup, answers) != 0.0:
            raise AssertionError("duplicate ids should score 0")
        bad_conf = sample.copy()
        bad_conf.loc[0, "confidence"] = 1.7
        if grade(bad_conf, answers) != 0.0:
            raise AssertionError("bad confidence should score 0")
        bad_id = sample.copy()
        bad_id.loc[0, "id"] = int(sample["id"].max()) + 999999
        if grade(bad_id, answers) != 0.0:
            raise AssertionError("id-set mismatch should score 0")

        malformed_span = sample.copy()
        malformed_span.loc[0, "reparandum_span"] = "[oops]"
        malformed_score = grade(malformed_span, answers)
        if malformed_score <= 0.0 or malformed_score >= sample_score + 0.20:
            raise AssertionError("malformed row-local span should degrade without becoming structural success/failure")

    print(f"OK: perfect={perfect_score:.6f} sample={sample_score:.6f} malformed_span={malformed_score:.6f}")


if __name__ == "__main__":
    main()

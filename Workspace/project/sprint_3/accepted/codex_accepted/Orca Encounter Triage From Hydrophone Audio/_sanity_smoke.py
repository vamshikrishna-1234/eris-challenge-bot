from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

from grade import InvalidSubmissionError, grade


ROOT = Path(__file__).resolve().parent


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    raw = ROOT / "_smoke_raw"
    if not raw.exists():
        raise SystemExit(
            "Smoke raw folder not found. Create it with official URL-imported Annotations.csv, CC-BY-4.0.txt, "
            "and a small subset of selected official WAV/FLAC files under _smoke_raw/."
        )

    with tempfile.TemporaryDirectory(prefix="orca_triage_smoke_") as tmp:
        tmp_path = Path(tmp)
        public = tmp_path / "public"
        private = tmp_path / "private"
        _run(
            [
                sys.executable,
                "prepare.py",
                "--raw",
                str(raw),
                "--public",
                str(public),
                "--private",
                str(private),
                "--min-group-test",
                "1",
                "--min-rows",
                "20",
            ]
        )
        train = pd.read_csv(public / "train.csv")
        test = pd.read_csv(public / "test.csv")
        sample = pd.read_csv(public / "sample_submission.csv")
        answers = pd.read_csv(private / "answers.csv")
        assert not train.empty and not test.empty and not answers.empty
        assert set(test["id"]) == set(answers["id"])
        assert not set(train["id"]).intersection(set(test["id"]))
        for rel in pd.concat([train["audio_path"], test["audio_path"]]).astype(str):
            assert (public / rel).exists(), rel

        perfect = answers[[
            "id",
            "orca_presence",
            "encounter_activity",
            "ecotype_context",
            "confounder_type",
            "call_band_bucket",
            "confidence",
        ]].copy()
        perfect_score = grade(perfect, answers)
        sample_score = grade(sample, answers)
        assert abs(perfect_score - 1.0) < 1e-12, perfect_score
        assert 0.0 <= sample_score < 0.6, sample_score

        wrong_cols = sample[["id", "orca_presence"]].copy()
        try:
            grade(wrong_cols, answers)
            raise AssertionError("wrong columns should have raised InvalidSubmissionError")
        except InvalidSubmissionError:
            pass
        dup = pd.concat([sample, sample.iloc[[0]]], ignore_index=True)
        try:
            grade(dup, answers)
            raise AssertionError("duplicate ids should have raised InvalidSubmissionError")
        except InvalidSubmissionError:
            pass
        bad = sample.copy()
        bad.loc[bad.index[0], "confidence"] = 1.5
        try:
            grade(bad, answers)
            raise AssertionError("out-of-range confidence should have raised InvalidSubmissionError")
        except InvalidSubmissionError:
            pass

        print(f"smoke ok: train={len(train)} test={len(test)} sample={sample_score:.6f} perfect={perfect_score:.6f}")
        shutil.rmtree(public, ignore_errors=True)
        shutil.rmtree(private, ignore_errors=True)


if __name__ == "__main__":
    main()

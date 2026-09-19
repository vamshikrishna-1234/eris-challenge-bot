"""Deterministic local smoke tests for the MEVA challenge artifact."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent


def _load_grade():
    spec = importlib.util.spec_from_file_location("meva_grade", ROOT / "grade.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    public = ROOT / "prepared" / "public"
    private = ROOT / "prepared" / "private" / "answers.csv"
    train = pd.read_csv(public / "train.csv")
    test = pd.read_csv(public / "test.csv")
    sample = pd.read_csv(public / "sample_submission.csv")
    answers = pd.read_csv(private)
    assert len(train) == 479 and len(test) == 175 and len(answers) == 175
    assert list(test.columns) == ["id", "video"]
    assert list(sample.columns) == ["id", "graph_json"]
    assert set(test.id) == set(sample.id) == set(answers.id)
    for rel in list(train.video) + list(test.video):
        path = public / rel
        assert path.is_file() and path.stat().st_size >= 100_000

    grade = _load_grade()
    perfect = answers[["id", "graph_json"]].copy()
    oracle = grade.grade(perfect, answers)
    sample_score = grade.grade(sample, answers)
    assert abs(oracle - 1.0) < 1e-12, oracle
    assert 0.12 <= sample_score < 0.5, sample_score

    malformed = perfect.copy()
    malformed.loc[0, "graph_json"] = "{not-json"
    malformed_score = grade.grade(malformed, answers)
    assert malformed_score < oracle

    duplicate = perfect.copy()
    duplicate.loc[1, "id"] = duplicate.loc[0, "id"]
    try:
        grade.grade(duplicate, answers)
    except grade.InvalidSubmissionError:
        pass
    else:
        raise AssertionError("duplicate IDs must raise InvalidSubmissionError")

    wrong_columns = perfect.rename(columns={"graph_json": "prediction"})
    try:
        grade.grade(wrong_columns, answers)
    except grade.InvalidSubmissionError:
        pass
    else:
        raise AssertionError("wrong columns must raise InvalidSubmissionError")

    print({"oracle": oracle, "sample": sample_score, "malformed_row": malformed_score,
           "train": len(train), "test": len(test)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

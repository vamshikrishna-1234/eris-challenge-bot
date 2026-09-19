from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

import grade


ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
PRIVATE = ROOT / "private"
RAW = ROOT / "raw_data"


def _load() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train = pd.read_csv(PUBLIC / "train.csv")
    test = pd.read_csv(PUBLIC / "test.csv")
    sample = pd.read_csv(PUBLIC / "sample_submission.csv")
    answers = pd.read_csv(PRIVATE / "answers.csv")
    return train, test, sample, answers


def _assert_raises_invalid(df: pd.DataFrame, answers: pd.DataFrame, name: str) -> None:
    try:
        grade.grade(df, answers)
    except grade.InvalidSubmissionError:
        return
    raise AssertionError(f"{name} should raise InvalidSubmissionError")


def _leak_checks(train: pd.DataFrame, test: pd.DataFrame, sample: pd.DataFrame) -> None:
    forbidden_cols = {
        "sensor_id",
        "audio_filename",
        "annotator_id",
        "split",
        "borough",
        "block",
        "latitude",
        "longitude",
        "year",
        "week",
        "day",
        "hour",
        "source_filename",
        "source_key",
    }
    for name, df in [("train", train), ("test", test), ("sample", sample)]:
        overlap = forbidden_cols & set(c.lower() for c in df.columns)
        assert not overlap, f"{name} exposes forbidden source columns: {overlap}"
    id_re = re.compile(r"^un_[0-9a-f]{14}$")
    path_re = re.compile(r"^(train|test)/audio/un_[0-9a-f]{14}\.wav$")
    for df_name, df in [("train", train), ("test", test)]:
        assert df["id"].astype(str).map(lambda s: bool(id_re.match(s))).all(), f"{df_name} has non-opaque ids"
        assert df["audio_path"].astype(str).map(lambda s: bool(path_re.match(s))).all(), f"{df_name} has non-opaque paths"
    if (RAW / "annotations.csv").exists():
        raw_names = set(pd.read_csv(RAW / "annotations.csv", usecols=["audio_filename"])["audio_filename"].astype(str))
        public_text = "\n".join(
            [
                (PUBLIC / "train.csv").read_text(encoding="utf-8"),
                (PUBLIC / "test.csv").read_text(encoding="utf-8"),
                (PUBLIC / "sample_submission.csv").read_text(encoding="utf-8"),
            ]
        )
        hits = [name for name in raw_names if name in public_text]
        assert not hits, f"public CSVs contain raw source filenames: {hits[:5]}"


def main() -> None:
    train, test, sample, answers = _load()
    assert len(train) == 701, len(train)
    assert len(test) == 299, len(test)
    assert set(test["id"]) == set(answers["id"])
    assert not train.isna().any().any()
    assert not test.isna().any().any()
    assert not answers.isna().any().any()
    _leak_checks(train, test, sample)

    perfect = answers[grade.REQUIRED_COLUMNS].copy()
    perfect_score = grade.grade(perfect, answers)
    assert abs(perfect_score - 1.0) < 1e-12, perfect_score

    sample_score = grade.grade(sample, answers)
    assert 0.12 <= sample_score < 0.5, sample_score

    malformed = sample.copy()
    malformed["source_mix_json"] = "{bad"
    malformed["dominant_source"] = "not_allowed"
    malformed["enforcement_priority"] = "not_allowed"
    malformed["nuisance_pattern"] = "not_allowed"
    malformed["confidence"] = 0.0
    malformed_score = grade.grade(malformed, answers)
    assert malformed_score == 0.0, malformed_score

    row_local_bad_json = sample.copy()
    row_local_bad_json.loc[row_local_bad_json.index[:10], "source_mix_json"] = "{bad"
    row_bad_score = grade.grade(row_local_bad_json, answers)
    assert 0.0 <= row_bad_score <= sample_score, row_bad_score

    wrong_cols = sample.drop(columns=["confidence"])
    _assert_raises_invalid(wrong_cols, answers, "wrong columns")

    extra_cols = sample.copy()
    extra_cols["extra"] = 1
    _assert_raises_invalid(extra_cols, answers, "extra columns")

    dup = pd.concat([sample, sample.iloc[[0]]], ignore_index=True)
    _assert_raises_invalid(dup, answers, "duplicate ids")

    missing = sample.iloc[:-1].copy()
    _assert_raises_invalid(missing, answers, "missing id")

    bad_conf = sample.copy()
    bad_conf.loc[bad_conf.index[0], "confidence"] = 1.5
    _assert_raises_invalid(bad_conf, answers, "invalid confidence")

    # Ensure sample JSON is structurally valid and complete.
    for text in sample["source_mix_json"].head(3):
        obj = json.loads(text)
        assert set(obj) == set(grade.SOURCE_FAMILIES)
        assert all(0.0 <= float(v) <= 1.0 for v in obj.values())

    print(
        json.dumps(
            {
                "train_rows": len(train),
                "test_rows": len(test),
                "sample_score": sample_score,
                "perfect_score": perfect_score,
                "malformed_score": malformed_score,
                "public_size_bytes": sum(p.stat().st_size for p in PUBLIC.rglob("*") if p.is_file()),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

from __future__ import annotations

import filecmp
import shutil
from pathlib import Path

import pandas as pd

from grade import REQUIRED_COLUMNS, grade
from prepare import prepare


ROOT = Path(__file__).resolve().parent


def _rm(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


def _ensure_raw() -> Path:
    raw = ROOT / "raw_data"
    required = [raw / "ami_public_manual_1.6.2.zip", raw / "audio"]
    if not all(p.exists() for p in required):
        raise FileNotFoundError("raw_data must contain direct AMI source files before smoke testing")
    return raw


def _perfect_submission(answers: pd.DataFrame) -> pd.DataFrame:
    perfect = answers[REQUIRED_COLUMNS].copy()
    # Confidence is calibrated to row correctness, not copied as a gold scalar.
    # A fully correct oracle should be maximally confident.
    perfect["confidence"] = 1.0
    return perfect


def main() -> None:
    raw = _ensure_raw()
    pub1, priv1 = ROOT / "_smoke_public1", ROOT / "_smoke_private1"
    pub2, priv2 = ROOT / "_smoke_public2", ROOT / "_smoke_private2"
    for path in [pub1, priv1, pub2, priv2]:
        _rm(path)

    prepare(raw, pub1, priv1)
    prepare(raw, pub2, priv2)

    for rel in ["train.csv", "test.csv", "sample_submission.csv"]:
        assert filecmp.cmp(pub1 / rel, pub2 / rel, shallow=False), f"nondeterministic {rel}"
    assert filecmp.cmp(priv1 / "answers.csv", priv2 / "answers.csv", shallow=False), "nondeterministic answers.csv"

    answers = pd.read_csv(priv1 / "answers.csv")
    perfect = _perfect_submission(answers)
    perfect_score = grade(perfect, answers)
    assert abs(perfect_score - 1.0) < 1e-12, perfect_score

    sample = pd.read_csv(pub1 / "sample_submission.csv")
    sample_score = grade(sample, answers)
    assert 0.0 < sample_score < 0.12, sample_score

    wrong_cols = sample[["id", "turn_state", "next_speaker_relation", "next_response_ms", "confidence"]]
    assert grade(wrong_cols, answers) == 0.0

    duplicate = sample.copy()
    duplicate.loc[duplicate.index[0], "id"] = duplicate.loc[duplicate.index[1], "id"]
    assert grade(duplicate, answers) == 0.0

    bad_state = sample.copy()
    bad_state.loc[bad_state.index[0], "turn_state"] = "DONE"
    assert grade(bad_state, answers) == 0.0

    bad_ms = sample.copy()
    bad_ms.loc[bad_ms.index[0], "next_response_ms"] = 9999
    assert grade(bad_ms, answers) == 0.0

    bad_conf = sample.copy()
    bad_conf.loc[bad_conf.index[0], "confidence"] = float("nan")
    assert grade(bad_conf, answers) == 0.0

    for path in [pub1, priv1, pub2, priv2]:
        _rm(path)

    print(f"perfect_score={perfect_score:.12f}")
    print(f"sample_score={sample_score:.6f}")
    print("OK: sanity smoke passed")


if __name__ == "__main__":
    main()

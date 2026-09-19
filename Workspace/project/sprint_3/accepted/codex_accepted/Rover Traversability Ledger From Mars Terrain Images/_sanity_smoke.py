from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from grade import InvalidSubmissionError, SUBMISSION_COLUMNS, grade
from prepare import prepare


ROOT = Path(__file__).resolve().parent


def _expect_invalid(submission: pd.DataFrame, answers: pd.DataFrame) -> None:
    try:
        grade(submission, answers)
    except InvalidSubmissionError:
        return
    raise AssertionError("expected InvalidSubmissionError")


def main() -> None:
    raw = ROOT / "raw_data"
    public = ROOT / "public"
    private = ROOT / "private"
    if not (public / "train.csv").is_file() or not (private / "answers.csv").is_file():
        prepare(raw, public, private)
    answers = pd.read_csv(private / "answers.csv", dtype={"id": str})
    sample = pd.read_csv(public / "sample_submission.csv", dtype={"id": str})
    perfect = answers[SUBMISSION_COLUMNS].copy()
    perfect_score = grade(perfect, answers)
    sample_score = grade(sample, answers)
    assert perfect_score == 1.0, perfect_score
    assert 0.12 <= sample_score < 0.50, sample_score

    malformed = perfect.copy()
    malformed.loc[malformed.index[0], "terrain_mask_rle"] = "{bad"
    malformed.loc[malformed.index[0], "hazard_boxes_json"] = "[bad"
    malformed_score = grade(malformed, answers)
    assert 0.0 < malformed_score < 1.0, malformed_score

    all_malformed = perfect.copy()
    all_malformed["terrain_mask_rle"] = "{bad"
    all_malformed["hazard_boxes_json"] = "[bad"
    all_malformed["route_safety_class"] = "teleport"
    all_malformed_score = grade(all_malformed, answers)
    assert all_malformed_score == 0.0, all_malformed_score

    wrong_columns = perfect.drop(columns=["uncertainty_score"])
    _expect_invalid(wrong_columns, answers)
    reordered = perfect[SUBMISSION_COLUMNS[::-1]]
    _expect_invalid(reordered, answers)
    duplicate = pd.concat([perfect, perfect.iloc[[0]]], ignore_index=True)
    _expect_invalid(duplicate, answers)
    missing = perfect.iloc[:-1].copy()
    _expect_invalid(missing, answers)
    nonfinite = perfect.copy()
    nonfinite.loc[nonfinite.index[0], "clearance_score"] = np.inf
    _expect_invalid(nonfinite, answers)
    out_of_range = perfect.copy()
    out_of_range.loc[out_of_range.index[0], "uncertainty_score"] = -0.1
    _expect_invalid(out_of_range, answers)
    missing_path = subprocess.run(
        [
            sys.executable,
            str(ROOT / "grade.py"),
            "--submission",
            str(ROOT / "does_not_exist.csv"),
            "--answers",
            str(private / "answers.csv"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert missing_path.returncode != 0
    assert "InvalidSubmissionError" in missing_path.stderr
    assert "Traceback" not in missing_path.stderr
    local_bad_route = perfect.copy()
    local_bad_route.loc[local_bad_route.index[0], "route_safety_class"] = "teleport"
    local_score = grade(local_bad_route, answers)
    assert 0.0 < local_score < 1.0
    print(
        f"PASS perfect={perfect_score:.12f} sample={sample_score:.6f} "
        f"malformed_row={malformed_score:.6f} all_malformed={all_malformed_score:.6f} "
        f"invalid_structure_raises=True"
    )


if __name__ == "__main__":
    main()

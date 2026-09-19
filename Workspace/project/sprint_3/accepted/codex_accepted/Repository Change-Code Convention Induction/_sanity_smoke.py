from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

from grade import SUBMISSION_COLUMNS, grade


ROOT = Path(__file__).resolve().parent


def _run(cmd: list[str]) -> None:
    subprocess.check_call(cmd, cwd=ROOT)


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _perfect_submission(answers: pd.DataFrame) -> pd.DataFrame:
    out = answers[["row_id", "change_code", "behavior_changing", "rollback_safe", "required_followup"]].copy()
    out["confidence"] = 1.0
    return out[SUBMISSION_COLUMNS]


def _diff_text(cell: object) -> str:
    try:
        obj = json.loads(str(cell))
        return str(obj.get("diff", "")).strip()
    except Exception:
        return str(cell).strip()


def _assert_no_test_context_target_overlap(test: pd.DataFrame) -> None:
    targets = {_diff_text(v) for v in test["target_diff"].tolist()}
    targets.discard("")
    for _, row in test.iterrows():
        items = json.loads(str(row["repo_context_examples"]))
        assert isinstance(items, list)
        for item in items:
            assert str(item.get("diff", "")).strip() not in targets, row["row_id"]


def main() -> None:
    raw = ROOT / "raw_data"
    if not (raw / "records.csv").exists():
        _run([sys.executable, str(ROOT / "generate.py"), "--quick", "--output", str(raw)])
    with tempfile.TemporaryDirectory(prefix="repo_real_smoke_") as td:
        base = Path(td)
        pub1 = base / "public1"
        priv1 = base / "private1"
        pub2 = base / "public2"
        priv2 = base / "private2"
        _run([sys.executable, str(ROOT / "prepare.py"), "--raw", str(raw), "--public", str(pub1), "--private", str(priv1)])
        _run([sys.executable, str(ROOT / "prepare.py"), "--raw", str(raw), "--public", str(pub2), "--private", str(priv2)])
        for rel in ["train.csv", "test.csv", "sample_submission.csv"]:
            assert _hash_file(pub1 / rel) == _hash_file(pub2 / rel), f"prepare nondeterministic for {rel}"
        assert _hash_file(priv1 / "answers.csv") == _hash_file(priv2 / "answers.csv")

        answers = pd.read_csv(priv1 / "answers.csv")
        sample = pd.read_csv(pub1 / "sample_submission.csv")
        perfect = _perfect_submission(answers)
        perfect_score = grade(perfect, answers)
        sample_score = grade(sample, answers)
        assert abs(perfect_score - 1.0) < 1e-12, perfect_score
        assert 0.12 <= sample_score < 0.50, sample_score

        assert grade(sample.drop(columns=["confidence"]), answers) == 0.0
        extra = sample.copy()
        extra["extra_col"] = "x"
        assert grade(extra, answers) == 0.0
        reordered = sample[["confidence", "row_id", "change_code", "behavior_changing", "rollback_safe", "required_followup"]]
        assert grade(reordered, answers) == 0.0
        dup = sample.copy()
        dup.loc[1, "row_id"] = dup.loc[0, "row_id"]
        assert grade(dup, answers) == 0.0
        bad_id = sample.copy()
        bad_id.loc[0, "row_id"] = -1
        assert grade(bad_id, answers) == 0.0
        bad_cat = sample.copy()
        bad_cat.loc[0, "change_code"] = "T_99"
        assert grade(bad_cat, answers) == 0.0
        bad_conf = sample.copy()
        bad_conf.loc[0, "confidence"] = 1.5
        assert grade(bad_conf, answers) == 0.0

        train = pd.read_csv(pub1 / "train.csv")
        test = pd.read_csv(pub1 / "test.csv")
        leaky = {"repo_key", "repo_family", "repo_split", "row_role", "template_id", "event_key", "archetype", "semantic_group"}
        assert not leaky & set(train.columns)
        assert not leaky & set(test.columns)
        assert train["row_id"].is_unique and test["row_id"].is_unique
        _assert_no_test_context_target_overlap(test)
        print(f"perfect={perfect_score:.6f}")
        print(f"sample={sample_score:.6f}")
        print("OK: sanity smoke passed")


if __name__ == "__main__":
    main()

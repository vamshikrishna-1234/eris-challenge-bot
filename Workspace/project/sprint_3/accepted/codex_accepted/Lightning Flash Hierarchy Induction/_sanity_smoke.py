"""End-to-end deterministic preparation and grading smoke tests."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import re
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


PREP = _load("lightning_prepare", ROOT / "prepare.py")
GR = _load("lightning_grade", ROOT / "grade.py")


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _tree_hash(root: Path) -> dict[str, str]:
    return {
        str(p.relative_to(root)).replace("\\", "/"): _sha(p)
        for p in sorted(root.rglob("*")) if p.is_file()
    }


def _expect_invalid(frame: pd.DataFrame, answers: pd.DataFrame, label: str):
    try:
        GR.score_details(frame, answers)
    except GR.InvalidSubmissionError:
        assert GR.grade(frame, answers) == 0.0
        return
    raise AssertionError(f"Expected InvalidSubmissionError for {label}")


def _relabel(cell: str) -> str:
    obj = json.loads(cell)
    gm = {g["group_id"]: f"local_group_{i + 91}" for i, g in enumerate(obj["groups"])}
    fm = {f["flash_id"]: f"local_flash_{i + 47}" for i, f in enumerate(obj["flashes"])}
    for g in obj["groups"]:
        g["group_id"] = gm[g["group_id"]]
    for f in obj["flashes"]:
        f["flash_id"] = fm[f["flash_id"]]
        f["groups"] = [gm[g] for g in f["groups"]]
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def _all_one_prediction(case_json: str, uncertain: bool) -> str:
    obj = json.loads(case_json)
    ids = sorted(d["id"] for d in obj["detections"])
    return json.dumps(
        {
            "groups": [{"group_id": "g1", "detections": ids}],
            "flashes": [{"flash_id": "f1", "groups": ["g1"]}],
            "uncertain_detections": ids if uncertain else [],
        },
        sort_keys=True,
        separators=(",", ":"),
    )


def _singleton_prediction(case_json: str, one_flash: bool) -> str:
    obj = json.loads(case_json)
    ids = sorted(d["id"] for d in obj["detections"])
    groups = [{"group_id": f"g{i + 1}", "detections": [d]} for i, d in enumerate(ids)]
    if one_flash:
        flashes = [{"flash_id": "f1", "groups": [g["group_id"] for g in groups]}]
    else:
        flashes = [{"flash_id": f"f{i + 1}", "groups": [g["group_id"]]} for i, g in enumerate(groups)]
    return json.dumps(
        {"groups": groups, "flashes": flashes, "uncertain_detections": []},
        sort_keys=True,
        separators=(",", ":"),
    )


def main():
    raw_before = _tree_hash(ROOT / "raw_data")
    timings = []
    with tempfile.TemporaryDirectory(prefix="lightning_smoke_") as tmp:
        tmp = Path(tmp)
        hashes = []
        for run in (1, 2):
            public = tmp / f"run{run}" / "public"
            private = tmp / f"run{run}" / "private"
            started = time.perf_counter()
            PREP.prepare(ROOT / "raw_data", public, private)
            timings.append(time.perf_counter() - started)
            hashes.append({**_tree_hash(public), **{f"private/{k}": v for k, v in _tree_hash(private).items()}})
        assert hashes[0] == hashes[1], "prepare.py is not byte deterministic"
        assert raw_before == _tree_hash(ROOT / "raw_data"), "prepare.py mutated raw inputs"

        public = tmp / "run1" / "public"
        private = tmp / "run1" / "private"
        train = pd.read_csv(public / "train.csv")
        test = pd.read_csv(public / "test.csv")
        sample = pd.read_csv(public / "sample_submission.csv")
        answers = pd.read_csv(private / "answers.csv")

        assert list(train.columns) == ["id", "case_json", "prompt", "target_json"]
        assert list(test.columns) == ["id", "case_json", "prompt"]
        assert list(sample.columns) == GR.SUBMISSION_COLUMNS
        assert len(train) == 210 and len(test) == len(answers) == 140
        assert train.id.is_monotonic_increasing and test.id.is_monotonic_increasing
        assert not (set(train.id) & set(test.id))
        assert set(test.id) == set(sample.id) == set(answers.id)
        assert not train.isna().any().any() and not test.isna().any().any()
        for axis in ("source_window", "density_bucket", "ambiguity_bucket"):
            assert answers[axis].value_counts().min() >= PREP.MIN_GROUP_TEST

        public_inputs = "\n".join(train.case_json.tolist() + train.prompt.tolist() + test.case_json.tolist() + test.prompt.tolist())
        forbidden = r"OR_GLM|GLM-L2-LCFA|s2024\d+|window_[a-e]|event_parent|group_parent|latitude|longitude|scan_id"
        assert re.search(forbidden, public_inputs, flags=re.IGNORECASE) is None

        detection_ids = []
        for frame in (train, test):
            for row in frame.itertuples(index=False):
                obj = json.loads(row.case_json)
                assert obj["case_id"] == row.id
                assert 12 <= len(obj["detections"]) <= 40
                assert obj["detections"] == sorted(obj["detections"], key=lambda x: x["id"])
                for d in obj["detections"]:
                    assert set(d) == {
                        "id", "x_rel", "y_rel", "t_rel", "energy_norm", "local_density", "temporal_density"
                    }
                    assert re.fullmatch(r"d[0-9a-f]{10}", d["id"])
                    assert all(math.isfinite(float(d[k])) for k in d if k != "id")
                    detection_ids.append(d["id"])
        assert len(detection_ids) == len(set(detection_ids))

        perfect = answers[["id", "target_json"]].rename(columns={"target_json": "prediction_json"})
        perfect["confidence"] = 1.0
        perfect = perfect[GR.SUBMISSION_COLUMNS]
        perfect_score = GR.grade(perfect, answers)
        sample_score = GR.grade(sample, answers)
        assert perfect_score == 1.0
        assert 0.12 <= sample_score < 0.50

        relabelled = perfect.copy()
        relabelled["prediction_json"] = relabelled.prediction_json.map(_relabel)
        assert GR.grade(relabelled, answers) == 1.0, "metric depends on alias strings"

        test_by_id = test.set_index("id")
        all_one = pd.DataFrame({
            "id": answers.id,
            "prediction_json": [
                _all_one_prediction(test_by_id.loc[i, "case_json"], uncertain=True)
                for i in answers.id
            ],
            "confidence": 0.20,
        }, columns=GR.SUBMISSION_COLUMNS)
        singleton_one_flash = pd.DataFrame({
            "id": answers.id,
            "prediction_json": [
                _singleton_prediction(test_by_id.loc[i, "case_json"], one_flash=True)
                for i in answers.id
            ],
            "confidence": 0.20,
        }, columns=GR.SUBMISSION_COLUMNS)
        singleton_many_flash = pd.DataFrame({
            "id": answers.id,
            "prediction_json": [
                _singleton_prediction(test_by_id.loc[i, "case_json"], one_flash=False)
                for i in answers.id
            ],
            "confidence": 0.0,
        }, columns=GR.SUBMISSION_COLUMNS)
        assert GR.grade(all_one, answers) < 0.25
        assert GR.grade(singleton_one_flash, answers) < 0.25
        assert GR.grade(singleton_many_flash, answers) <= 0.05 + 1e-12

        malformed = perfect.copy()
        bad_id = malformed.loc[0, "id"]
        malformed.loc[0, "prediction_json"] = "{not valid json"
        malformed_score, malformed_details = GR.score_details(malformed, answers)
        assert malformed_details.loc[malformed_details.id == bad_id, "row_score"].item() == 0.0
        assert 0.98 < malformed_score < 1.0

        oversized = perfect.copy()
        oversized.loc[0, "prediction_json"] = "x" * (GR.MAX_JSON_LEN + 1)
        _, oversized_details = GR.score_details(oversized, answers)
        assert oversized_details.loc[oversized_details.id == oversized.loc[0, "id"], "row_score"].item() == 0.0

        invalid_structure = perfect.copy()
        obj = json.loads(invalid_structure.loc[0, "prediction_json"])
        obj["groups"][0]["detections"].append(obj["groups"][0]["detections"][0])
        invalid_structure.loc[0, "prediction_json"] = json.dumps(obj)
        _, bad_details = GR.score_details(invalid_structure, answers)
        assert bad_details.loc[bad_details.id == invalid_structure.loc[0, "id"], "row_score"].item() == 0.0

        wrong_columns = perfect.rename(columns={"confidence": "certainty"})
        _expect_invalid(wrong_columns, answers, "wrong columns")
        _expect_invalid(perfect.assign(extra=1), answers, "extra column")
        _expect_invalid(perfect.iloc[:-1].copy(), answers, "missing id")
        duplicate = pd.concat([perfect.iloc[:-1], perfect.iloc[[0]]], ignore_index=True)
        _expect_invalid(duplicate, answers, "duplicate id")
        extra = perfect.copy()
        extra.loc[0, "id"] = "case_not_in_test"
        _expect_invalid(extra, answers, "extra id")
        for value in (np.nan, np.inf, -0.01, 1.01, "not-a-number"):
            bad = perfect.copy()
            if isinstance(value, str):
                bad["confidence"] = bad["confidence"].astype(object)
            bad.loc[0, "confidence"] = value
            _expect_invalid(bad, answers, f"confidence={value}")

        grade_started = time.perf_counter()
        for _ in range(20):
            assert GR.grade(sample, answers) == sample_score
        grade_seconds = (time.perf_counter() - grade_started) / 20.0

    peak_mib = None
    try:
        import psutil
        mem = psutil.Process().memory_info()
        peak_mib = getattr(mem, "peak_wset", mem.rss) / (1024 ** 2)
    except Exception:
        pass
    result = {
        "status": "PASS",
        "train_cases": 210,
        "test_cases": 140,
        "perfect_score": perfect_score,
        "sample_score": sample_score,
        "prepare_seconds": timings,
        "grade_mean_seconds": grade_seconds,
        "process_peak_mib": peak_mib,
        "deterministic": True,
        "raw_untouched": True,
        "strict_submission_checks": True,
        "malformed_row_local": True,
        "degenerate_partition_scores_capped": True,
        "label_invariant": True,
    }
    (ROOT / "SMOKE_RESULTS.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

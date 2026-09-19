from __future__ import annotations

import json
import math

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "id",
    "source_mix_json",
    "dominant_source",
    "enforcement_priority",
    "nuisance_pattern",
    "confidence",
]

SOURCE_FAMILIES = [
    "engine",
    "machinery_impact",
    "powered_saw",
    "alert_signal",
    "music",
    "human_voice",
    "dog",
    "other_impact",
]
DOMINANT_ALLOWED = {
    "engine",
    "machinery_impact",
    "powered_saw",
    "alert_signal",
    "music",
    "human_voice",
    "dog",
    "other_impact",
    "mixed_uncertain",
}
PRIORITY_ALLOWED = ["low", "moderate", "high", "urgent"]
NUISANCE_ALLOWED = {
    "traffic_dominant",
    "construction_dominant",
    "alert_dominant",
    "social_music_voice",
    "animal_or_other",
    "mixed_uncertain",
}
HIDDEN_GROUP_AXES = [
    "priority_group_hidden",
    "nuisance_group_hidden",
    "source_family_hidden",
    "pressure_band_hidden",
    "mix_complexity_hidden",
]
MAX_JSON_LEN = 900
MAX_CAT_LEN = 80


class InvalidSubmissionError(ValueError):
    """Raised when a submitted CSV violates required structural constraints."""


def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip().lstrip("\ufeff") for c in out.columns]
    return out


def _validate_submission(submission: pd.DataFrame, answers: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    sub = _clean_columns(submission)
    ans = _clean_columns(answers)
    if list(sub.columns) != REQUIRED_COLUMNS:
        raise InvalidSubmissionError(f"submission columns must be exactly {REQUIRED_COLUMNS}")
    if not set(REQUIRED_COLUMNS).issubset(set(ans.columns)):
        raise ValueError("answers file is missing required grading columns")
    if sub.isna().any().any():
        raise InvalidSubmissionError("submission contains NaN or blank values")
    if ans[REQUIRED_COLUMNS].isna().any().any():
        raise ValueError("answers file contains NaN values")

    sub["id"] = sub["id"].astype(str)
    ans["id"] = ans["id"].astype(str)
    if sub["id"].duplicated().any():
        raise InvalidSubmissionError("submission contains duplicate id values")
    if ans["id"].duplicated().any():
        raise ValueError("answers file contains duplicate id values")
    if set(sub["id"]) != set(ans["id"]):
        raise InvalidSubmissionError("submission id set does not match the test set")

    for col in ["source_mix_json", "dominant_source", "enforcement_priority", "nuisance_pattern"]:
        lengths = sub[col].astype(str).str.len()
        if (lengths > max(MAX_JSON_LEN, MAX_CAT_LEN)).any():
            raise InvalidSubmissionError(f"submission column {col} contains oversized strings")

    conf = pd.to_numeric(sub["confidence"], errors="coerce")
    true_conf = pd.to_numeric(ans["confidence"], errors="coerce")
    if conf.isna().any() or true_conf.isna().any():
        raise InvalidSubmissionError("confidence values must be numeric and non-missing")
    conf_arr = conf.to_numpy(dtype=float)
    true_conf_arr = true_conf.to_numpy(dtype=float)
    if not np.isfinite(conf_arr).all() or not np.isfinite(true_conf_arr).all():
        raise InvalidSubmissionError("confidence values must be finite")
    if (conf_arr < 0).any() or (conf_arr > 1).any() or (true_conf_arr < 0).any() or (true_conf_arr > 1).any():
        raise InvalidSubmissionError("confidence values must be in [0, 1]")
    sub["confidence"] = conf_arr
    ans["confidence"] = true_conf_arr
    return sub.set_index("id").sort_index(), ans.set_index("id").sort_index()


def _parse_mix(value: object) -> dict[str, float] | None:
    text = str(value)
    if len(text) > MAX_JSON_LEN:
        return None
    try:
        obj = json.loads(text)
    except Exception:
        return None
    if not isinstance(obj, dict):
        return None
    if set(obj.keys()) != set(SOURCE_FAMILIES):
        return None
    out: dict[str, float] = {}
    for key in SOURCE_FAMILIES:
        try:
            val = float(obj[key])
        except Exception:
            return None
        if not math.isfinite(val) or val < 0.0 or val > 1.0:
            return None
        out[key] = val
    return out


def _mix_score(pred: dict[str, float] | None, gold: dict[str, float] | None) -> float:
    if pred is None or gold is None:
        return 0.0
    err = np.array([pred[k] - gold[k] for k in SOURCE_FAMILIES], dtype=float)
    rmse = float(np.sqrt(np.mean(err * err)))
    return float(np.clip(1.0 - rmse / 0.35, 0.0, 1.0))


def _priority_score(pred: str, gold: str) -> float:
    if pred not in PRIORITY_ALLOWED:
        return 0.0
    if gold not in PRIORITY_ALLOWED:
        raise ValueError(f"answers contain invalid enforcement_priority {gold}")
    diff = abs(PRIORITY_ALLOWED.index(pred) - PRIORITY_ALLOWED.index(gold))
    return float(max(0.0, 1.0 - diff / 3.0))


def _categorical_exact(pred: str, gold: str, allowed: set[str]) -> float:
    if pred not in allowed:
        return 0.0
    if gold not in allowed:
        raise ValueError(f"answers contain invalid categorical value {gold}")
    return 1.0 if pred == gold else 0.0


def _macro_f1(pred: pd.Series, true: pd.Series, allowed: set[str] | list[str]) -> float:
    labels = sorted(set(true.astype(str).tolist()))
    allowed_set = set(allowed)
    scores: list[float] = []
    pred_arr = pred.astype(str).to_numpy()
    true_arr = true.astype(str).to_numpy()
    for label in labels:
        if label not in allowed_set:
            raise ValueError(f"answers contain invalid label {label}")
        tp = int(np.sum((pred_arr == label) & (true_arr == label)))
        fp = int(np.sum((pred_arr == label) & (true_arr != label)))
        fn = int(np.sum((pred_arr != label) & (true_arr == label)))
        if tp == 0 and fp == 0 and fn == 0:
            scores.append(1.0)
        elif tp == 0:
            scores.append(0.0)
        else:
            precision = tp / (tp + fp)
            recall = tp / (tp + fn)
            scores.append(2.0 * precision * recall / (precision + recall))
    return float(np.mean(scores)) if scores else 0.0


def _row_scores(sub: pd.DataFrame, ans: pd.DataFrame) -> pd.DataFrame:
    rows = ans.copy()
    pred_mix = [_parse_mix(v) for v in sub["source_mix_json"]]
    gold_mix = [_parse_mix(v) for v in ans["source_mix_json"]]
    mix_scores = np.array([_mix_score(p, g) for p, g in zip(pred_mix, gold_mix)], dtype=float)
    dom_scores = np.array(
        [
            _categorical_exact(str(p), str(g), DOMINANT_ALLOWED)
            for p, g in zip(sub["dominant_source"], ans["dominant_source"])
        ],
        dtype=float,
    )
    priority_scores = np.array(
        [_priority_score(str(p), str(g)) for p, g in zip(sub["enforcement_priority"], ans["enforcement_priority"])],
        dtype=float,
    )
    nuisance_scores = np.array(
        [
            _categorical_exact(str(p), str(g), NUISANCE_ALLOWED)
            for p, g in zip(sub["nuisance_pattern"], ans["nuisance_pattern"])
        ],
        dtype=float,
    )
    core = 0.38 * mix_scores + 0.16 * dom_scores + 0.22 * priority_scores + 0.16 * nuisance_scores
    core_norm = core / 0.92
    conf_scores = np.maximum(0.0, 1.0 - np.abs(sub["confidence"].to_numpy(float) - ans["confidence"].to_numpy(float)) / 0.5)
    conf_scores *= core_norm
    rows["mix_score"] = mix_scores
    rows["dominant_score"] = dom_scores
    rows["priority_score"] = priority_scores
    rows["nuisance_score"] = nuisance_scores
    rows["confidence_score"] = conf_scores
    rows["row_score"] = np.clip(core + 0.08 * (conf_scores**2), 0.0, 1.0)
    rows["pred_dominant_source"] = sub["dominant_source"].astype(str)
    rows["pred_enforcement_priority"] = sub["enforcement_priority"].astype(str)
    rows["pred_nuisance_pattern"] = sub["nuisance_pattern"].astype(str)
    return rows


def _worst_hidden_group(rows: pd.DataFrame) -> float:
    scores = []
    for axis in HIDDEN_GROUP_AXES:
        if axis not in rows.columns:
            continue
        for _, group in rows.groupby(axis):
            if not group.empty:
                scores.append(float(group["row_score"].mean()))
    return float(min(scores)) if scores else float(rows["row_score"].mean())


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    sub, ans = _validate_submission(submission, answers)
    rows = _row_scores(sub, ans)
    mean_row = float(rows["row_score"].mean())
    mix_mean = float(rows["mix_score"].mean())
    dom_f1 = _macro_f1(rows["pred_dominant_source"], rows["dominant_source"], DOMINANT_ALLOWED)
    pri_f1 = _macro_f1(rows["pred_enforcement_priority"], rows["enforcement_priority"], PRIORITY_ALLOWED)
    nui_f1 = _macro_f1(rows["pred_nuisance_pattern"], rows["nuisance_pattern"], NUISANCE_ALLOWED)
    worst = _worst_hidden_group(rows)
    final = 0.58 * mean_row + 0.14 * mix_mean + 0.08 * dom_f1 + 0.10 * pri_f1 + 0.05 * nui_f1 + 0.05 * worst
    if not math.isfinite(final):
        raise ValueError("computed score is not finite")
    return float(np.clip(final, 0.0, 1.0))


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("--submission", type=Path, required=True)
    parser.add_argument("--answers", type=Path, required=True)
    args = parser.parse_args()
    print(grade(pd.read_csv(args.submission), pd.read_csv(args.answers)))

from __future__ import annotations

import json
import math
from collections import defaultdict
from typing import Any

import numpy as np
import pandas as pd


SUBMISSION_COLUMNS = ["id", "tab_json", "confidence"]
ANSWER_REQUIRED_COLUMNS = {"id", "tab_json", "notes_json"}
MAX_JSON_LEN = 20000

OPEN_MIDI_BY_STRING = {
    6: 40,  # low E
    5: 45,
    4: 50,
    3: 55,
    2: 59,
    1: 64,  # high E
}
MIN_FRET = 0
MAX_FRET = 24

GROUP_AXES = [
    "player_group",
    "style_group",
    "polyphony_band",
    "ambiguity_band",
    "fret_range_band",
    "note_density_band",
]


def _loads_json_cell(cell: Any) -> Any | None:
    if cell is None:
        return None
    text = str(cell)
    if len(text) > MAX_JSON_LEN:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


def _to_int(value: Any) -> int | None:
    try:
        if isinstance(value, bool):
            return None
        f = float(value)
        if not math.isfinite(f):
            return None
        i = int(round(f))
        if abs(f - i) > 1e-6:
            return None
        return i
    except Exception:
        return None


def _valid_positions(pitch_midi: int) -> set[tuple[int, int]]:
    positions: set[tuple[int, int]] = set()
    for string, open_midi in OPEN_MIDI_BY_STRING.items():
        fret = pitch_midi - open_midi
        if MIN_FRET <= fret <= MAX_FRET:
            positions.add((string, fret))
    return positions


def _normalise_notes(notes_cell: Any) -> tuple[dict[str, int], dict[str, list[str]]] | None:
    raw = _loads_json_cell(notes_cell)
    if not isinstance(raw, list) or not raw:
        return None
    pitches: dict[str, int] = {}
    groups: dict[str, list[str]] = defaultdict(list)
    for item in raw:
        if not isinstance(item, dict):
            return None
        event_id = str(item.get("event_id", "")).strip()
        if not event_id or event_id in pitches:
            return None
        pitch = _to_int(item.get("pitch_midi"))
        if pitch is None:
            return None
        group_id = str(item.get("group_id", event_id)).strip() or event_id
        pitches[event_id] = pitch
        groups[group_id].append(event_id)
    return pitches, dict(groups)


def _normalise_tab(tab_cell: Any) -> dict[str, tuple[int, int]] | None:
    raw = _loads_json_cell(tab_cell)
    if not isinstance(raw, list):
        return None
    out: dict[str, tuple[int, int]] = {}
    for item in raw:
        if not isinstance(item, dict):
            return None
        event_id = str(item.get("event_id", "")).strip()
        if not event_id or event_id in out:
            return None
        string = _to_int(item.get("string"))
        fret = _to_int(item.get("fret"))
        if string is None or fret is None:
            return None
        out[event_id] = (string, fret)
    return out


def _row_scores(pred_cell: Any, gold_cell: Any, notes_cell: Any) -> dict[str, float]:
    notes = _normalise_notes(notes_cell)
    gold = _normalise_tab(gold_cell)
    pred = _normalise_tab(pred_cell)
    zero = {
        "event": 0.0,
        "chord": 0.0,
        "row_exact": 0.0,
        "valid": 0.0,
        "row_tab": 0.0,
    }
    if notes is None or gold is None:
        return zero
    pitches, groups = notes
    expected_ids = set(pitches)
    if set(gold) != expected_ids:
        return zero
    if pred is None or set(pred) != expected_ids:
        return zero

    event_scores: list[float] = []
    exact_flags: dict[str, float] = {}
    valid_flags: list[float] = []
    for event_id in sorted(expected_ids):
        pitch = pitches[event_id]
        valid_positions = _valid_positions(pitch)
        pred_pos = pred[event_id]
        gold_pos = gold[event_id]
        string, fret = pred_pos
        if not (1 <= string <= 6 and MIN_FRET <= fret <= MAX_FRET):
            valid_flags.append(0.0)
            event_scores.append(0.0)
            exact_flags[event_id] = 0.0
            continue
        if pred_pos not in valid_positions:
            valid_flags.append(0.0)
            event_scores.append(0.0)
            exact_flags[event_id] = 0.0
            continue

        valid_flags.append(1.0)
        exact = 1.0 if pred_pos == gold_pos else 0.0
        exact_flags[event_id] = exact
        string_part = 1.0 if string == gold_pos[0] else 0.0
        fret_part = max(0.0, 1.0 - min(abs(fret - gold_pos[1]), 5) / 5.0)
        event_scores.append(0.84 * exact + 0.08 * string_part + 0.08 * fret_part)

    if not event_scores:
        return zero

    group_scores: list[float] = []
    for event_ids in groups.values():
        if not event_ids:
            continue
        gold_set = {gold[eid] for eid in event_ids}
        pred_set = {pred[eid] for eid in event_ids}
        if pred_set == gold_set:
            group_scores.append(1.0)
        else:
            group_scores.append(float(np.mean([exact_flags.get(eid, 0.0) for eid in event_ids])))
    if not group_scores:
        group_scores = [float(np.mean(list(exact_flags.values())))]

    event_mean = float(np.mean(event_scores))
    chord_mean = float(np.mean(group_scores))
    valid_mean = float(np.mean(valid_flags))
    row_exact = 1.0 if all(v == 1.0 for v in exact_flags.values()) and valid_mean == 1.0 else 0.0
    row_tab = 0.74 * event_mean + 0.20 * chord_mean + 0.06 * valid_mean
    return {
        "event": event_mean,
        "chord": chord_mean,
        "row_exact": row_exact,
        "valid": valid_mean,
        "row_tab": float(np.clip(row_tab, 0.0, 1.0)),
    }


def _worst_group_score(row_scores: pd.Series, answers: pd.DataFrame) -> float:
    group_means: list[float] = []
    tmp = answers.copy()
    tmp["_row_tab_score"] = row_scores.to_numpy(dtype=float)
    for axis in GROUP_AXES:
        if axis not in tmp.columns:
            continue
        means = tmp.groupby(axis, dropna=False)["_row_tab_score"].mean()
        if not means.empty:
            group_means.append(float(means.min()))
    if not group_means:
        return float(row_scores.mean())
    return float(min(group_means))


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    try:
        if list(submission.columns) != SUBMISSION_COLUMNS:
            return 0.0
        if not ANSWER_REQUIRED_COLUMNS.issubset(set(answers.columns)):
            return 0.0

        sub = submission.copy()
        ans = answers.copy()
        sub["id"] = sub["id"].astype(str)
        ans["id"] = ans["id"].astype(str)

        if sub["id"].duplicated().any() or ans["id"].duplicated().any():
            return 0.0
        if set(sub["id"]) != set(ans["id"]):
            return 0.0

        conf = pd.to_numeric(sub["confidence"], errors="coerce")
        if conf.isna().any() or not np.isfinite(conf.to_numpy(dtype=float)).all():
            return 0.0
        if ((conf < 0.0) | (conf > 1.0)).any():
            return 0.0
        sub["confidence"] = conf.astype(float)

        sub = sub.set_index("id").reindex(ans["id"].to_numpy())

        event_terms: list[float] = []
        chord_terms: list[float] = []
        row_exact_terms: list[float] = []
        valid_terms: list[float] = []
        row_tab_terms: list[float] = []
        calib_terms: list[float] = []

        for (_, arow), (_, srow) in zip(ans.iterrows(), sub.iterrows()):
            scores = _row_scores(srow["tab_json"], arow["tab_json"], arow["notes_json"])
            event_terms.append(scores["event"])
            chord_terms.append(scores["chord"])
            row_exact_terms.append(scores["row_exact"])
            valid_terms.append(scores["valid"])
            row_tab_terms.append(scores["row_tab"])
            conf_value = float(srow["confidence"])
            calib_terms.append(max(0.0, 1.0 - abs(conf_value - scores["row_exact"])))

        if not event_terms:
            return 0.0

        event_score = float(np.mean(event_terms))
        chord_score = float(np.mean(chord_terms))
        row_exact = float(np.mean(row_exact_terms))
        valid_score = float(np.mean(valid_terms))
        calibration = float(np.mean(calib_terms))
        row_tab_series = pd.Series(row_tab_terms, index=ans["id"].to_numpy())
        worst_group = _worst_group_score(row_tab_series, ans)

        final = (
            0.30 * (event_score ** 2.25)
            + 0.10 * (chord_score ** 1.90)
            + 0.30 * row_exact
            + 0.06 * (calibration ** 1.70)
            + 0.20 * (worst_group ** 1.90)
            + 0.04 * (valid_score ** 1.30)
        )
        return float(np.clip(final, 0.0, 1.0))

    except Exception:
        return 0.0


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    ap = argparse.ArgumentParser()
    ap.add_argument("--submission", type=Path, required=True)
    ap.add_argument("--answers", type=Path, required=True)
    args = ap.parse_args()
    submission_df = pd.read_csv(args.submission)
    answers_df = pd.read_csv(args.answers)
    print(f"score={grade(submission_df, answers_df):.6f}")

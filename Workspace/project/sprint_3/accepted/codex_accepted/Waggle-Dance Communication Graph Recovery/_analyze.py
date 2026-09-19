from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd

from grade import GROUP_COLUMNS, InvalidSubmissionError, MAX_JSON_LEN, REQUIRED_COLUMNS, grade
from prepare import SUBMISSION_COLUMNS, _heuristic_prediction, _json_dumps


FORBIDDEN_PUBLIC_PATTERNS = [
    re.compile(r"2019-[0-9]{2}-[0-9]{2}"),
    re.compile(r"Berlin2019", re.IGNORECASE),
    re.compile(r"track_id", re.IGNORECASE),
    re.compile(r"frame_id", re.IGNORECASE),
    re.compile(r"dance_id", re.IGNORECASE),
    re.compile(r"timestamp", re.IGNORECASE),
    re.compile(r"feeder", re.IGNORECASE),
]


def _perfect_from_answers(answers: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id": answers["id"].astype(str),
            "dancer_id": answers["dancer_id"].astype(str),
            "waggle_intervals_json": answers["waggle_intervals_json"].astype(str),
            "roles_json": answers["roles_json"].astype(str),
            "edges_json": answers["edges_json"].astype(str),
            "confidence": 1.0,
        },
        columns=SUBMISSION_COLUMNS,
    )


def _empty_baseline(test: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id": test["id"].astype(str),
            "dancer_id": "B00",
            "waggle_intervals_json": "[]",
            "roles_json": "[]",
            "edges_json": "[]",
            "confidence": 0.05,
        },
        columns=SUBMISSION_COLUMNS,
    )


def _train_prior_baseline(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    interval_counts = train["waggle_intervals_json"].map(lambda s: len(json.loads(s))).to_numpy()
    role_counts = train["roles_json"].map(lambda s: len(json.loads(s))).to_numpy()
    edge_counts = train["edges_json"].map(lambda s: len(json.loads(s))).to_numpy()
    n_intervals = int(np.clip(round(float(np.median(interval_counts))), 3, 10))
    n_roles = int(np.clip(round(float(np.median(role_counts))), 2, 8))
    n_edges = int(np.clip(round(float(np.median(edge_counts))), 1, 4))
    rows = []
    for row in test.itertuples(index=False):
        duration = float(row.duration_sec)
        step = duration / (n_intervals + 1)
        intervals = [
            {"start": round(max(0.0, step * (i + 1) - 0.50), 3), "end": round(min(duration, step * (i + 1) + 0.50), 3)}
            for i in range(n_intervals)
        ]
        roles = []
        for i in range(n_roles):
            roles.append({"bee_id": f"B{i + 1:02d}", "role": "follower" if i < n_edges else "attendee"})
        edges = [{"source": "B00", "target": f"B{i + 1:02d}"} for i in range(n_edges)]
        rows.append(
            {
                "id": row.id,
                "dancer_id": "B00",
                "waggle_intervals_json": _json_dumps(intervals),
                "roles_json": _json_dumps(roles),
                "edges_json": _json_dumps(edges),
                "confidence": 0.18,
            }
        )
    return pd.DataFrame(rows, columns=SUBMISSION_COLUMNS)


def _metadata_only_baseline(test: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for row in test.itertuples(index=False):
        bee_count = int(row.bee_count)
        crowd = str(row.crowding_level)
        duration = float(row.duration_sec)
        dancer_idx = {"low": 0, "medium": max(0, bee_count // 3), "high": max(0, bee_count // 2)}.get(crowd, 0)
        dancer_idx = min(max(0, dancer_idx), max(0, bee_count - 1))
        n_intervals = {"low": 4, "medium": 6, "high": 8}.get(crowd, 5)
        n_roles = {"low": 2, "medium": 4, "high": 6}.get(crowd, 3)
        intervals = []
        for i in range(n_intervals):
            c = (i + 1) * duration / (n_intervals + 1)
            intervals.append({"start": round(max(0.0, c - 0.3), 3), "end": round(min(duration, c + 0.3), 3)})
        roles = []
        for i in range(n_roles):
            b = (dancer_idx + i + 1) % max(1, bee_count)
            roles.append({"bee_id": f"B{b:02d}", "role": "follower" if i < 2 else "attendee"})
        edges = [{"source": f"B{dancer_idx:02d}", "target": r["bee_id"]} for r in roles if r["role"] == "follower"]
        rows.append(
            {
                "id": row.id,
                "dancer_id": f"B{dancer_idx:02d}",
                "waggle_intervals_json": _json_dumps(intervals),
                "roles_json": _json_dumps(roles),
                "edges_json": _json_dumps(edges),
                "confidence": 0.18,
            }
        )
    return pd.DataFrame(rows, columns=SUBMISSION_COLUMNS)


def _spam_everything_baseline(test: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for row in test.itertuples(index=False):
        duration = float(row.duration_sec)
        bee_count = int(row.bee_count)
        intervals = []
        for i in range(30):
            center = (i + 1) * duration / 31.0
            intervals.append({"start": round(max(0.0, center - 0.4), 3), "end": round(min(duration, center + 0.4), 3)})
        roles = [{"bee_id": f"B{i:02d}", "role": "follower"} for i in range(bee_count) if i != 0]
        edges = [{"source": "B00", "target": f"B{i:02d}"} for i in range(bee_count) if i != 0]
        rows.append(
            {
                "id": row.id,
                "dancer_id": "B00",
                "waggle_intervals_json": _json_dumps(intervals),
                "roles_json": _json_dumps(roles),
                "edges_json": _json_dumps(edges),
                "confidence": 0.20,
            }
        )
    return pd.DataFrame(rows, columns=SUBMISSION_COLUMNS)


def _safe_json_loads(value):
    try:
        return json.loads(value)
    except Exception:
        return []


def _clamp_local_bee_id(value: str, bee_count: int) -> str:
    try:
        idx = int(str(value)[1:])
    except Exception:
        idx = 0
    idx = min(max(0, idx), max(0, int(bee_count) - 1))
    return f"B{idx:02d}"


def _label_copy_nearest_baseline(train: pd.DataFrame, test: pd.DataFrame, public: Path, use_file_size: bool) -> pd.DataFrame:
    train_feat = train.copy()
    test_feat = test.copy()
    for df in (train_feat, test_feat):
        sizes = []
        observations = []
        for row in df.itertuples(index=False):
            path = public / row.episode_npz
            sizes.append(path.stat().st_size)
            with np.load(path) as data:
                observations.append(int(len(data["t_sec"])))
        df["_file_size"] = sizes
        df["_n_obs"] = observations

    for col in ["duration_sec", "bee_count", "_file_size", "_n_obs"]:
        mean = float(train_feat[col].mean())
        std = float(train_feat[col].std() or 1.0)
        train_feat[f"z_{col}"] = (train_feat[col] - mean) / std
        test_feat[f"z_{col}"] = (test_feat[col] - mean) / std

    rows = []
    for _, row in test_feat.iterrows():
        cost = np.zeros(len(train_feat), dtype=float)
        columns = [("duration_sec", 1.3), ("bee_count", 1.2)]
        if use_file_size:
            columns.extend([("_file_size", 1.0), ("_n_obs", 0.8)])
        for col, weight in columns:
            cost += weight * np.abs(train_feat[f"z_{col}"].to_numpy() - row[f"z_{col}"])
        cost += (train_feat["comb_side"].to_numpy() != row["comb_side"]) * 0.5
        cost += (train_feat["crowding_level"].to_numpy() != row["crowding_level"]) * 0.4
        cost += (train_feat["tracking_confidence_level"].to_numpy() != row["tracking_confidence_level"]) * 0.4

        src = train_feat.iloc[int(cost.argmin())]
        bee_count = int(row["bee_count"])
        dancer = _clamp_local_bee_id(src["dancer_id"], bee_count)
        source_duration = max(float(src["duration_sec"]), 1e-6)
        target_duration = float(row["duration_sec"])
        intervals = []
        for item in _safe_json_loads(src["waggle_intervals_json"]):
            if isinstance(item, dict):
                start = max(0.0, min(target_duration, float(item.get("start", 0.0)) * target_duration / source_duration))
                end = max(start, min(target_duration, float(item.get("end", start)) * target_duration / source_duration))
                intervals.append({"start": round(start, 3), "end": round(end, 3)})

        roles = []
        used_bees = set()
        for item in _safe_json_loads(src["roles_json"]):
            if not isinstance(item, dict):
                continue
            bee = _clamp_local_bee_id(item.get("bee_id", "B00"), bee_count)
            role = item.get("role", "attendee")
            if bee != dancer and bee not in used_bees and role in {"follower", "attendee"}:
                roles.append({"bee_id": bee, "role": role})
                used_bees.add(bee)

        edges = []
        follower_ids = {item["bee_id"] for item in roles if item["role"] == "follower"}
        for item in _safe_json_loads(src["edges_json"]):
            if not isinstance(item, dict):
                continue
            target = _clamp_local_bee_id(item.get("target", "B00"), bee_count)
            if target != dancer and target in follower_ids:
                edge = {"source": dancer, "target": target}
                if edge not in edges:
                    edges.append(edge)

        rows.append(
            {
                "id": row["id"],
                "dancer_id": dancer,
                "waggle_intervals_json": _json_dumps(intervals),
                "roles_json": _json_dumps(roles),
                "edges_json": _json_dumps(edges),
                "confidence": 0.27,
            }
        )
    return pd.DataFrame(rows, columns=SUBMISSION_COLUMNS)


def _heuristic_baseline(public: Path, test: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for row in test.itertuples(index=False):
        pred = _heuristic_prediction(public / row.episode_npz, float(row.duration_sec))
        rows.append({"id": row.id, **pred})
    return pd.DataFrame(rows, columns=SUBMISSION_COLUMNS)


def _grade_or_invalid(submission: pd.DataFrame, answers: pd.DataFrame) -> float | str:
    try:
        return grade(submission, answers)
    except InvalidSubmissionError:
        return "InvalidSubmissionError"


def _strict_submission_checks(sample: pd.DataFrame, answers: pd.DataFrame) -> dict[str, float | str]:
    checks: dict[str, float | str] = {
        "sample": grade(sample, answers),
        "shuffled_rows": grade(sample.sample(frac=1, random_state=17).reset_index(drop=True), answers),
        "wrong_order": _grade_or_invalid(sample[list(reversed(REQUIRED_COLUMNS))], answers),
        "extra_column": _grade_or_invalid(sample.assign(extra=1), answers),
        "missing_column": _grade_or_invalid(sample.drop(columns=["edges_json"]), answers),
        "missing_row": _grade_or_invalid(sample.iloc[:-1].copy(), answers),
        "extra_row": _grade_or_invalid(pd.concat([sample, sample.iloc[[0]]], ignore_index=True), answers),
        "nan_confidence": _grade_or_invalid(sample.assign(confidence=[np.nan] + sample["confidence"].iloc[1:].tolist()), answers),
        "inf_confidence": _grade_or_invalid(sample.assign(confidence=[np.inf] + sample["confidence"].iloc[1:].tolist()), answers),
        "out_of_range_confidence": _grade_or_invalid(sample.assign(confidence=[1.1] + sample["confidence"].iloc[1:].tolist()), answers),
    }
    if len(sample) >= 2:
        duplicate = sample.copy()
        duplicate.loc[duplicate.index[1], "id"] = duplicate.loc[duplicate.index[0], "id"]
        checks["duplicate_id"] = _grade_or_invalid(duplicate, answers)
    bad = sample.copy()
    bad.loc[bad.index[0], "waggle_intervals_json"] = "{bad-json"
    checks["one_bad_json"] = grade(bad, answers)
    bad = sample.copy()
    bad.loc[bad.index[0], "waggle_intervals_json"] = "[" + ("0" * (MAX_JSON_LEN + 1)) + "]"
    checks["one_overlong_json"] = grade(bad, answers)
    bad = sample.copy()
    first_bee_count = int(answers.set_index("id").loc[str(bad.loc[bad.index[0], "id"]), "bee_count"])
    bad.loc[bad.index[0], "dancer_id"] = f"B{first_bee_count:02d}"
    checks["one_invalid_dancer"] = grade(bad, answers)
    bad = sample.copy()
    bad.loc[bad.index[0], "waggle_intervals_json"] = _json_dumps([{"start": 20.0, "end": 1.0}])
    checks["one_invalid_interval"] = grade(bad, answers)
    bad = sample.copy()
    bad.loc[bad.index[0], "roles_json"] = _json_dumps(
        [{"bee_id": "B00", "role": "follower"}, {"bee_id": "B00", "role": "attendee"}]
    )
    checks["one_duplicate_role"] = grade(bad, answers)
    bad = sample.copy()
    bad.loc[bad.index[0], "edges_json"] = _json_dumps([{"source": "B00", "target": "B00"}])
    checks["one_self_edge"] = grade(bad, answers)
    return checks


def _file_size_correlations(public: Path, test: pd.DataFrame, answers: pd.DataFrame) -> tuple[dict, dict]:
    augmented = test.copy()
    sizes = []
    observations = []
    for row in augmented.itertuples(index=False):
        path = public / row.episode_npz
        sizes.append(path.stat().st_size)
        with np.load(path) as data:
            observations.append(int(len(data["t_sec"])))
    augmented["_file_size"] = sizes
    augmented["_n_obs"] = observations
    answer_map = answers.set_index("id")
    augmented["_waggle_count"] = augmented["id"].map(lambda value: len(_safe_json_loads(answer_map.loc[value, "waggle_intervals_json"])))
    augmented["_role_count"] = augmented["id"].map(lambda value: len(_safe_json_loads(answer_map.loc[value, "roles_json"])))
    augmented["_edge_count"] = augmented["id"].map(lambda value: len(_safe_json_loads(answer_map.loc[value, "edges_json"])))

    correlations = {}
    for xcol in ["_file_size", "_n_obs", "duration_sec", "bee_count"]:
        for ycol in ["_waggle_count", "_role_count", "_edge_count"]:
            pearson = float(pd.to_numeric(augmented[xcol]).corr(pd.to_numeric(augmented[ycol]), method="pearson"))
            spearman = float(pd.to_numeric(augmented[xcol]).corr(pd.to_numeric(augmented[ycol]), method="spearman"))
            correlations[f"{xcol}_vs_{ycol}"] = {
                "pearson": pearson if math.isfinite(pearson) else None,
                "spearman": spearman if math.isfinite(spearman) else None,
            }
    summary = {
        "test_bytes_min_median_max": [
            int(augmented["_file_size"].min()),
            int(augmented["_file_size"].median()),
            int(augmented["_file_size"].max()),
        ],
        "strongest_abs_hidden_target_correlation": max(
            abs(v)
            for pair in correlations.values()
            for v in pair.values()
            if v is not None
        ),
    }
    return correlations, summary


def _raw_coordinate_overlap_probe(root: Path, public: Path, train: pd.DataFrame, test: pd.DataFrame) -> dict:
    raw_dir = root / "official_raw_subset" / "Berlin2019_tracks"
    if not raw_dir.exists():
        return {"status": "skipped", "reason": "official_raw_subset/Berlin2019_tracks not present"}
    raw_pairs = set()
    for csv_path in sorted(raw_dir.glob("*.csv")):
        try:
            for chunk in pd.read_csv(csv_path, usecols=["x_pos_hive", "y_pos_hive"], chunksize=300000):
                chunk = chunk.dropna()
                if len(chunk) > 5000:
                    seed = sum(map(ord, csv_path.name)) % (2**32)
                    chunk = chunk.sample(n=5000, random_state=seed)
                for x, y in zip(chunk["x_pos_hive"].to_numpy(), chunk["y_pos_hive"].to_numpy()):
                    raw_pairs.add((round(float(x), 2), round(float(y), 2)))
        except Exception:
            continue

    public_pairs = []
    for df in (train.head(50), test.head(50)):
        for row in df.itertuples(index=False):
            with np.load(public / row.episode_npz) as data:
                x = np.asarray(data["x_mm"], dtype=float)
                y = np.asarray(data["y_mm"], dtype=float)
                if len(x) == 0:
                    continue
                idx = np.linspace(0, len(x) - 1, min(len(x), 120), dtype=int)
                public_pairs.extend((round(float(x[i]), 2), round(float(y[i]), 2)) for i in idx)
    hits = sum(1 for pair in public_pairs if pair in raw_pairs)
    return {
        "status": "measured",
        "public_pairs_checked": int(len(public_pairs)),
        "sampled_raw_pairs": int(len(raw_pairs)),
        "exact_round2_hits": int(hits),
        "hit_rate": float(hits / len(public_pairs)) if public_pairs else 0.0,
    }


def _shortcut_audit(public: Path, private: Path, train: pd.DataFrame, test: pd.DataFrame, answers: pd.DataFrame, sample: pd.DataFrame) -> dict:
    all_ids = pd.concat([train["id"], test["id"]], ignore_index=True).astype(str)
    labels_by_id = pd.Series(
        ["train"] * len(train) + ["test"] * len(test),
        index=pd.concat([train["id"], test["id"]], ignore_index=True).astype(str).to_numpy(),
    ).sort_index()
    id_checks = {
        "all_match_pattern": bool(all(re.match(r"^wdg_[0-9a-f]{14}$", value) for value in all_ids)),
        "unique_across_train_test": int(all_ids.nunique()) == int(len(all_ids)),
        "lexicographic_train_fraction_first_100": float(labels_by_id.iloc[:100].eq("train").mean()),
        "lexicographic_train_fraction_last_100": float(labels_by_id.iloc[-100:].eq("train").mean()),
    }
    correlations, size_summary = _file_size_correlations(public, test, answers)
    metadata_nn = _label_copy_nearest_baseline(train, test, public, use_file_size=False)
    file_size_nn = _label_copy_nearest_baseline(train, test, public, use_file_size=True)
    return {
        "id_checks": id_checks,
        "strict_submission_checks": _strict_submission_checks(sample, answers),
        "metadata_nearest_labelcopy_score": grade(metadata_nn, answers),
        "file_size_nearest_labelcopy_score": grade(file_size_nn, answers),
        "file_size_summary": size_summary,
        "file_size_correlations": correlations,
        "raw_coordinate_overlap_probe": _raw_coordinate_overlap_probe(public.parent, public, train, test),
    }


def _score_by_group(sub: pd.DataFrame, answers: pd.DataFrame) -> dict[str, float]:
    out = {}
    for col in GROUP_COLUMNS:
        if col not in answers.columns:
            continue
        vals = {}
        for value, idx in answers.groupby(col, sort=True).groups.items():
            local_answers = answers.loc[list(idx)].copy()
            local_sub = sub[sub["id"].astype(str).isin(set(local_answers["id"].astype(str)))].copy()
            vals[str(value)] = grade(local_sub, local_answers)
        if vals:
            out[col] = min(vals.values())
    return out


def _source_reversibility_scan(public: Path, train: pd.DataFrame, test: pd.DataFrame) -> list[str]:
    findings = []
    for name, df in [("train.csv", train), ("test.csv", test)]:
        if list(df["id"]) != sorted(df["id"]):
            findings.append(f"{name}: ids are not sorted")
        for col in df.columns:
            if col in {"comb_side", "crowding_level", "tracking_confidence_level"}:
                continue
            text = "\n".join(df[col].astype(str).head(200).tolist())
            for pat in FORBIDDEN_PUBLIC_PATTERNS:
                if pat.search(col) or pat.search(text):
                    findings.append(f"{name}: forbidden source token pattern in {col}")
    for rel in list(train["episode_npz"]) + list(test["episode_npz"]):
        path = public / rel
        if not path.exists():
            findings.append(f"missing episode file: {rel}")
            continue
        data = np.load(path)
        keys = set(data.files)
        expected = {
            "t_sec",
            "bee_index",
            "x_mm",
            "y_mm",
            "orientation_rad",
            "tracking_confidence",
            "neighbor_count_20mm",
            "neighbor_count_40mm",
            "dense_features",
            "dense_mask",
            "dense_frame_hz",
        }
        if keys != expected:
            findings.append(f"{rel}: unexpected npz keys {sorted(keys)}")
        if any(np.asarray(data[k]).dtype.kind in {"U", "S", "O"} for k in data.files):
            findings.append(f"{rel}: string/object arrays could carry raw ids")
        for key in data.files:
            arr = np.asarray(data[key])
            if arr.dtype.kind in {"f", "i", "u"} and not np.isfinite(arr.astype(float)).all():
                findings.append(f"{rel}: non-finite values in {key}")
        if np.max(data["bee_index"]) >= 100:
            findings.append(f"{rel}: local bee index exceeds expected range")
        if np.min(data["t_sec"]) < -1e-6:
            findings.append(f"{rel}: negative relative time")
    findings.extend(_feature_overlap_scan(public, train, test))
    return findings


def _npz_signature(path: Path, rounded: bool) -> str:
    data = np.load(path)
    h = hashlib.sha256()
    for key in [
        "t_sec",
        "bee_index",
        "x_mm",
        "y_mm",
        "orientation_rad",
        "tracking_confidence",
        "neighbor_count_20mm",
        "neighbor_count_40mm",
    ]:
        arr = np.asarray(data[key])
        if rounded and arr.dtype.kind == "f":
            arr = np.nan_to_num(np.round(arr.astype(float), 1), nan=-9999.0).astype(np.float32)
        h.update(key.encode("utf-8"))
        h.update(str(arr.shape).encode("utf-8"))
        h.update(arr.tobytes())
    return h.hexdigest()


def _coarse_signature(public: Path, row) -> tuple:
    data = np.load(public / row.episode_npz)
    x = np.asarray(data["x_mm"], dtype=float)
    y = np.asarray(data["y_mm"], dtype=float)
    t = np.asarray(data["t_sec"], dtype=float)
    bee = np.asarray(data["bee_index"], dtype=int)
    return (
        int(row.bee_count),
        round(float(row.duration_sec), 0),
        round(float(np.nanmean(x)), 0),
        round(float(np.nanmean(y)), 0),
        round(float(np.nanstd(x)), 0),
        round(float(np.nanstd(y)), 0),
        round(float(np.nanmax(t) - np.nanmin(t)), 0),
        int(len(np.unique(bee))),
    )


def _feature_overlap_scan(public: Path, train: pd.DataFrame, test: pd.DataFrame) -> list[str]:
    findings = []
    train_exact = {_npz_signature(public / r.episode_npz, rounded=False) for r in train.itertuples(index=False)}
    test_exact = {_npz_signature(public / r.episode_npz, rounded=False) for r in test.itertuples(index=False)}
    overlap = train_exact & test_exact
    if overlap:
        findings.append(f"exact train/test NPZ feature signature overlap: {len(overlap)}")

    train_round = {_npz_signature(public / r.episode_npz, rounded=True) for r in train.itertuples(index=False)}
    test_round = {_npz_signature(public / r.episode_npz, rounded=True) for r in test.itertuples(index=False)}
    overlap = train_round & test_round
    if overlap:
        findings.append(f"rounded train/test NPZ feature signature overlap: {len(overlap)}")

    train_coarse = {_coarse_signature(public, r) for r in train.itertuples(index=False)}
    test_coarse = [_coarse_signature(public, r) for r in test.itertuples(index=False)]
    coarse_hits = sum(sig in train_coarse for sig in test_coarse)
    if coarse_hits > max(5, int(0.03 * len(test))):
        findings.append(f"coarse public-feature lookup has too many train/test hits: {coarse_hits}/{len(test)}")
    return findings


def _format_score_value(value: float | str) -> str:
    return f"{value:.12f}" if isinstance(value, (int, float)) else str(value)


def _format_scores(scores: dict[str, float | str]) -> str:
    return "\n".join(f"- {name}: {_format_score_value(value)}" for name, value in scores.items())


def analyze(public: Path, private: Path, write_report: bool = True) -> dict:
    train = pd.read_csv(public / "train.csv")
    test = pd.read_csv(public / "test.csv")
    answers = pd.read_csv(private / "answers.csv")
    sample = pd.read_csv(public / "sample_submission.csv")
    perfect = _perfect_from_answers(answers)
    empty = _empty_baseline(test)
    train_prior = _train_prior_baseline(train, test)
    metadata_only = _metadata_only_baseline(test)
    spam_everything = _spam_everything_baseline(test)

    start = time.perf_counter()
    heuristic = _heuristic_baseline(public, test)
    elapsed = time.perf_counter() - start

    malformed = perfect.copy()
    if len(malformed):
        malformed.loc[malformed.index[0], "waggle_intervals_json"] = "{bad-json"

    scores = {
        "perfect": grade(perfect, answers),
        "sample": grade(sample, answers),
        "empty_no_track": grade(empty, answers),
        "train_graph_prior": grade(train_prior, answers),
        "metadata_only": grade(metadata_only, answers),
        "spam_everything_no_track": grade(spam_everything, answers),
        "simple_trajectory_heuristic": grade(heuristic, answers),
        "row_malformed_json": grade(malformed, answers),
    }
    invalid = perfect.drop(columns=["confidence"])
    scores["invalid_missing_column"] = _grade_or_invalid(invalid, answers)
    subgroup_counts = {col: answers[col].value_counts().to_dict() for col in GROUP_COLUMNS if col in answers.columns}
    subgroup_scores = {
        "sample": _score_by_group(sample, answers),
        "simple_trajectory_heuristic": _score_by_group(heuristic, answers),
    }
    source_findings = _source_reversibility_scan(public, train, test)
    shortcut_audit = _shortcut_audit(public, private, train, test, answers, sample)
    timing = {
        "heuristic_rows": int(len(test)),
        "heuristic_seconds": elapsed,
        "heuristic_seconds_per_1000_rows": elapsed / max(1, len(test)) * 1000.0,
        "compact_solver_cpu_estimate": "Feature extraction plus a compact CPU model should fit well under 1.5 hours for this prepared split.",
    }
    report = {
        "rows": {"train": int(len(train)), "test": int(len(test))},
        "scores": scores,
        "subgroup_counts": subgroup_counts,
        "subgroup_scores": subgroup_scores,
        "source_reversibility_findings": source_findings,
        "shortcut_audit": shortcut_audit,
        "timing": timing,
    }
    if write_report:
        lines = [
            "# Analysis Results",
            "",
            f"Rows: train={len(train)}, test={len(test)}",
            "",
            "## Scores",
            "",
            _format_scores(scores),
            "",
            "## Subgroup Counts",
            "",
        ]
        for col, counts in subgroup_counts.items():
            lines.append(f"- {col}: {counts}")
        lines.extend(["", "## Worst Subgroup Scores", ""])
        for name, vals in subgroup_scores.items():
            lines.append(f"- {name}: {vals}")
        lines.extend(["", "## Source Reversibility Scan", ""])
        if source_findings:
            lines.extend(f"- WARN: {x}" for x in source_findings)
        else:
            lines.append("- PASS: no raw source ids, timestamps, dates, filenames, or object/string NPZ fields found in public prepared files.")
        lines.extend(["", "## Shortcut And Reverse-Engineering Audit", ""])
        lines.append(f"- Metadata nearest-label-copy score: {shortcut_audit['metadata_nearest_labelcopy_score']:.12f}")
        lines.append(f"- File-size nearest-label-copy score: {shortcut_audit['file_size_nearest_labelcopy_score']:.12f}")
        lines.append(f"- File-size summary: {shortcut_audit['file_size_summary']}")
        lines.append(f"- Public ID checks: {shortcut_audit['id_checks']}")
        lines.append(f"- Raw coordinate overlap probe: {shortcut_audit['raw_coordinate_overlap_probe']}")
        lines.append("- Strict submission checks:")
        for name, value in shortcut_audit["strict_submission_checks"].items():
            lines.append(f"  - {name}: {_format_score_value(value)}")
        lines.extend(
            [
                "",
                "## CPU Timing",
                "",
                f"- Heuristic rows: {len(test)}",
                f"- Heuristic seconds: {elapsed:.3f}",
                f"- Seconds per 1000 rows: {timing['heuristic_seconds_per_1000_rows']:.3f}",
                f"- Estimate: {timing['compact_solver_cpu_estimate']}",
                "",
            ]
        )
        (public.parent / "ANALYSIS_RESULTS.md").write_text("\n".join(lines), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze prepared waggle-dance graph recovery challenge outputs.")
    parser.add_argument("--public", type=Path, default=Path("public"))
    parser.add_argument("--private", type=Path, default=Path("private"))
    parser.add_argument("--no-report", action="store_true")
    args = parser.parse_args()
    report = analyze(args.public, args.private, write_report=not args.no_report)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

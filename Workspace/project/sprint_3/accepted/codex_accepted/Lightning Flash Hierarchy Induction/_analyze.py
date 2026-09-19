"""Feasibility, shortcut, leakage, and CPU analysis for the challenge.

This script deliberately evaluates attacks before presenting the task.  It uses
only public features for every non-oracle prediction.  Native labels are used
only for fitting on train and scoring on the held-out source windows.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import re
import sys
import time
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering, DBSCAN
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


ROOT = Path(__file__).resolve().parent
FEATURES = ["x_rel", "y_rel", "t_rel", "energy_norm", "local_density", "temporal_density"]


def _load_grade():
    spec = importlib.util.spec_from_file_location("lightning_grade", ROOT / "grade.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _load_prepare():
    spec = importlib.util.spec_from_file_location("lightning_prepare_for_audit", ROOT / "prepare.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


GR = _load_grade()
PREP = _load_prepare()


@dataclass
class Case:
    case_id: str
    ids: list[str]
    x: np.ndarray
    group: np.ndarray | None
    flash: np.ndarray | None
    uncertain: set[str] | None


def _truth_labels(case_obj: dict, target: dict):
    ids = [d["id"] for d in case_obj["detections"]]
    pos = {d: i for i, d in enumerate(ids)}
    group = np.empty(len(ids), dtype=np.int32)
    flash = np.empty(len(ids), dtype=np.int32)
    gid_to_num = {}
    for gnum, g in enumerate(target["groups"]):
        gid_to_num[g["group_id"]] = gnum
        for did in g["detections"]:
            group[pos[did]] = gnum
    for fnum, f in enumerate(target["flashes"]):
        for gid in f["groups"]:
            flash[group == gid_to_num[gid]] = fnum
    return group, flash, set(target["uncertain_detections"])


def _load_cases(frame: pd.DataFrame, labelled: bool) -> list[Case]:
    out = []
    for row in frame.itertuples(index=False):
        obj = json.loads(row.case_json)
        detections = obj["detections"]
        ids = [d["id"] for d in detections]
        x = np.asarray([[float(d[k]) for k in FEATURES] for d in detections], dtype=np.float64)
        if labelled:
            group, flash, uncertain = _truth_labels(obj, json.loads(row.target_json))
        else:
            group = flash = uncertain = None
        out.append(Case(str(row.id), ids, x, group, flash, uncertain))
    return out


def _relabel(labels: np.ndarray) -> np.ndarray:
    mapping = {}
    return np.asarray([mapping.setdefault(int(v), len(mapping)) for v in labels], dtype=np.int32)


def _hierarchy_json(case: Case, group: np.ndarray, flash: np.ndarray, uncertain: set[str]) -> str:
    group = _relabel(group)
    # Every group must belong to exactly one flash. Majority resolution makes
    # arbitrary event-level flash predictions a valid hierarchy.
    group_flash = {}
    for g in sorted(set(group)):
        vals, counts = np.unique(flash[group == g], return_counts=True)
        group_flash[g] = int(vals[np.argmax(counts)])
    flash_values = {v: i for i, v in enumerate(sorted(set(group_flash.values())))}
    groups = []
    for g in sorted(set(group)):
        groups.append({
            "group_id": f"g{g + 1}",
            "detections": sorted(case.ids[i] for i in np.where(group == g)[0]),
        })
    flashes = []
    for old_f, fnum in flash_values.items():
        members = [f"g{g + 1}" for g in sorted(group_flash) if group_flash[g] == old_f]
        flashes.append({"flash_id": f"f{fnum + 1}", "groups": members})
    return json.dumps(
        {"groups": groups, "flashes": flashes, "uncertain_detections": sorted(uncertain)},
        sort_keys=True,
        separators=(",", ":"),
    )


def _submission(cases: list[Case], predictions: list[tuple[np.ndarray, np.ndarray, set[str]]], confidence=0.35):
    return pd.DataFrame([
        {
            "id": c.case_id,
            "prediction_json": _hierarchy_json(c, g, f, u),
            "confidence": confidence,
        }
        for c, (g, f, u) in zip(cases, predictions)
    ], columns=GR.SUBMISSION_COLUMNS)


def _answer_frame(frame: pd.DataFrame) -> pd.DataFrame:
    return frame[["id", "target_json"]].copy()


def _score(name: str, submission: pd.DataFrame, answers: pd.DataFrame, results: dict):
    score, details = GR.score_details(submission, answers)
    results[name] = {
        "score": round(float(score), 6),
        "group_pair_f1": round(float(details.group_pair_f1.mean()), 6),
        "flash_pair_f1": round(float(details.flash_pair_f1.mean()), 6),
        "uncertain_f1": round(float(details.uncertain_f1.mean()), 6),
        "exact_rate": round(float(details.exact.mean()), 6),
    }


def _dbscan_prediction(case: Case, geps: float, gtw: float, feps: float, ftw: float):
    z = case.x[:, :3].copy()
    z[:, 2] *= gtw
    group = DBSCAN(eps=geps, min_samples=1, metric="euclidean").fit_predict(z)
    unique = sorted(set(group))
    centroids = np.asarray([case.x[group == g, :3].mean(axis=0) for g in unique])
    centroids[:, 2] *= ftw
    gf = DBSCAN(eps=feps, min_samples=1, metric="euclidean").fit_predict(centroids)
    flash = np.asarray([gf[unique.index(int(g))] for g in group], dtype=np.int32)
    # A fixed public-density rule is included, but it receives no native labels.
    k = max(1, int(round(0.24 * len(case.ids))))
    boundary = np.argsort(-case.x[:, 4])[:k]
    return group, flash, {case.ids[i] for i in boundary}


def _tune_dbscan(train_cases: list[Case], train_answers: pd.DataFrame):
    best = (-1.0, None)
    # Modest grid: enough to mount a serious public-feature threshold attack,
    # but intentionally CPU-cheap and fully reproducible.
    for geps in (0.08, 0.14, 0.22, 0.30):
        for gtw in (0.6, 1.4):
            for feps in (0.28, 0.46, 0.70):
                for ftw in (0.45, 1.1):
                    pred = [_dbscan_prediction(c, geps, gtw, feps, ftw) for c in train_cases]
                    sub = _submission(train_cases, pred, 0.35)
                    score = GR.grade(sub, train_answers)
                    if score > best[0]:
                        best = (score, (geps, gtw, feps, ftw))
    return best


def _pair_features(x: np.ndarray, i: int, j: int) -> np.ndarray:
    delta = np.abs(x[i] - x[j])
    return np.r_[
        delta,
        math.hypot(delta[0], delta[1]),
        math.sqrt(delta[0] ** 2 + delta[1] ** 2 + (0.72 * delta[2]) ** 2),
        np.minimum(x[i], x[j]),
        np.maximum(x[i], x[j]),
    ]


def _pair_dataset(cases: list[Case]):
    rows, yg, yf = [], [], []
    for c in cases:
        assert c.group is not None and c.flash is not None
        for i, j in combinations(range(len(c.ids)), 2):
            rows.append(_pair_features(c.x, i, j))
            yg.append(int(c.group[i] == c.group[j]))
            yf.append(int(c.flash[i] == c.flash[j]))
    return np.asarray(rows), np.asarray(yg), np.asarray(yf)


def _probability_matrix(model, case: Case):
    n = len(case.ids)
    p = np.eye(n, dtype=np.float64)
    pairs = list(combinations(range(n), 2))
    feats = np.asarray([_pair_features(case.x, i, j) for i, j in pairs])
    values = model.predict_proba(feats)[:, 1]
    for (i, j), v in zip(pairs, values):
        p[i, j] = p[j, i] = v
    return p


def _agglomerate(distance: np.ndarray, threshold: float) -> np.ndarray:
    if len(distance) == 1:
        return np.zeros(1, dtype=np.int32)
    model = AgglomerativeClustering(
        n_clusters=None,
        metric="precomputed",
        linkage="average",
        distance_threshold=1.0 - threshold,
    )
    return model.fit_predict(distance)


def _event_features(case: Case) -> np.ndarray:
    z = case.x[:, :3].copy()
    z[:, 2] *= 0.72
    distance = np.linalg.norm(z[:, None, :] - z[None, :, :], axis=2)
    np.fill_diagonal(distance, np.inf)
    nearest = np.sort(distance, axis=1)[:, : min(3, len(case.ids) - 1)]
    if nearest.shape[1] < 3:
        nearest = np.pad(nearest, ((0, 0), (0, 3 - nearest.shape[1])), constant_values=2.0)
    ncol = np.full((len(case.ids), 1), len(case.ids) / 40.0)
    return np.column_stack([case.x, nearest, ncol])


def _learned_prediction(case: Case, group_model, flash_model, uncertain_model, gthr: float, fthr: float):
    pg = _probability_matrix(group_model, case)
    pf = _probability_matrix(flash_model, case)
    group = _agglomerate(1.0 - pg, gthr)
    unique = sorted(set(group))
    group_pf = np.eye(len(unique), dtype=np.float64)
    for ai, ga in enumerate(unique):
        ia = np.where(group == ga)[0]
        for bi, gb in enumerate(unique):
            if bi <= ai:
                continue
            ib = np.where(group == gb)[0]
            value = float(np.mean(pf[np.ix_(ia, ib)]))
            group_pf[ai, bi] = group_pf[bi, ai] = value
    group_flash = _agglomerate(1.0 - group_pf, fthr)
    flash = np.asarray([group_flash[unique.index(int(g))] for g in group], dtype=np.int32)

    # A tiny event-level classifier learns which public-space neighborhoods
    # were boundary-ambiguous in the training hierarchy.
    boundary_probability = uncertain_model.predict_proba(_event_features(case))[:, 1]
    k = max(1, int(round(0.24 * len(case.ids))))
    uncertain = {case.ids[i] for i in np.argsort(-boundary_probability)[:k]}
    return group, flash, uncertain


def _fit_and_tune_model(train_cases: list[Case], train_answers: pd.DataFrame):
    x, yg, yf = _pair_dataset(train_cases)
    group_model = HistGradientBoostingClassifier(
        max_iter=110, learning_rate=0.065, max_leaf_nodes=19, l2_regularization=0.8, random_state=1729
    ).fit(x, yg)
    flash_model = HistGradientBoostingClassifier(
        max_iter=110, learning_rate=0.065, max_leaf_nodes=23, l2_regularization=0.8, random_state=1730
    ).fit(x, yf)
    xu = np.vstack([_event_features(c) for c in train_cases])
    yu = np.concatenate([
        np.asarray([int(d in c.uncertain) for d in c.ids], dtype=np.int32)
        for c in train_cases
    ])
    uncertain_model = HistGradientBoostingClassifier(
        max_iter=90, learning_rate=0.06, max_leaf_nodes=15, l2_regularization=1.0, random_state=1731
    ).fit(xu, yu)
    best = (-1.0, None)
    for gthr in (0.34, 0.54, 0.74):
        for fthr in (0.34, 0.54, 0.74):
            pred = [_learned_prediction(c, group_model, flash_model, uncertain_model, gthr, fthr) for c in train_cases]
            score = GR.grade(_submission(train_cases, pred, 0.55), train_answers)
            if score > best[0]:
                best = (score, (gthr, fthr))
    return group_model, flash_model, uncertain_model, best, len(x)


def _metadata_predictions(cases: list[Case]):
    out = []
    for c in cases:
        n = len(c.ids)
        # No geometry/energy/time: opaque-id order only, six groups, two flashes.
        group = np.arange(n) % 6
        flash = group % 2
        out.append((group, flash, set()))
    return out


def _hash_predictions(cases: list[Case]):
    out = []
    for c in cases:
        h = np.asarray([int(hashlib.sha256(d.encode()).hexdigest()[:8], 16) for d in c.ids])
        group = h % 6
        flash = (h // 7) % 2
        out.append((group, flash, set()))
    return out


def _order_predictions(cases: list[Case]):
    out = []
    for c in cases:
        order = np.argsort(c.ids)
        group = np.empty(len(c.ids), dtype=int)
        group[order] = np.arange(len(c.ids)) // 3
        flash = group % 2
        out.append((group, flash, set()))
    return out


def _length_count_predictions(cases: list[Case]):
    out = []
    for c in cases:
        # Approximate a CSV/JSON-length attack using only point count and opaque
        # order; numeric values and native hierarchy evidence are ignored.
        n_groups = 4 + (len(c.ids) % 5)
        order = np.argsort(c.ids)
        group = np.empty(len(c.ids), dtype=int)
        group[order] = np.arange(len(c.ids)) % n_groups
        flash = group % 2
        out.append((group, flash, set()))
    return out


def _signature_from_arrays(x: np.ndarray, y: np.ndarray, t: np.ndarray, energy: np.ndarray) -> np.ndarray:
    n = len(x)
    z = np.column_stack([x, y, 0.72 * t])
    spatial, temporal, energy_delta = [], [], []
    for i, j in combinations(range(n), 2):
        spatial.append(float(np.linalg.norm(z[i] - z[j])))
        temporal.append(abs(float(t[i] - t[j])))
        energy_delta.append(abs(float(energy[i] - energy[j])))

    def quantiles(values: list[float] | np.ndarray) -> list[float]:
        arr = np.asarray(values, dtype=np.float64)
        if arr.size == 0:
            return [0.0] * 7
        return [float(v) for v in np.quantile(arr, [0.0, 0.10, 0.25, 0.50, 0.75, 0.90, 1.0])]

    return np.asarray(
        [n / 40.0]
        + quantiles(spatial)
        + quantiles(temporal)
        + quantiles(energy_delta)
        + quantiles(energy),
        dtype=np.float64,
    )


def _native_bundle_signature(events) -> np.ndarray:
    lat = np.asarray([e.lat for e in events], dtype=np.float64)
    lon = np.asarray([e.lon for e in events], dtype=np.float64)
    tim = np.asarray([e.time_s for e in events], dtype=np.float64)
    energy = np.asarray([max(e.energy, 0.0) for e in events], dtype=np.float64)
    lat0 = float(np.mean(lat))
    x = 111.32 * math.cos(math.radians(lat0)) * (lon - float(np.mean(lon)))
    y = 110.57 * (lat - float(np.mean(lat)))
    scale = max(float(np.percentile(np.hypot(x, y), 90)), 8.0)
    x = np.tanh(x / (1.15 * scale))
    y = np.tanh(y / (1.15 * scale))
    span = max(float(np.percentile(tim, 95) - np.percentile(tim, 5)), 0.25)
    t = np.clip((tim - float(np.percentile(tim, 5))) / span, -0.2, 1.2)
    order = np.argsort(np.argsort(np.log1p(energy), kind="stable"), kind="stable")
    erank = (order + 0.5) / len(events)
    return _signature_from_arrays(x, y, t, erank)


def _public_case_signature(case: Case) -> np.ndarray:
    return _signature_from_arrays(case.x[:, 0], case.x[:, 1], case.x[:, 2], case.x[:, 3])


def _raw_signature_lookup_attack(raw: Path, private: Path, test_cases: list[Case]) -> dict:
    """Try to map public cases back to raw event bundles using invariant sketches.

    This is intentionally stronger than a normal metadata probe: it uses the official
    raw files and the organizer-side candidate construction family, but it does not
    use public ids, private labels, exact redaction noise, or native hierarchy labels
    when ranking candidates.
    """
    answers = pd.read_csv(private / "answers.csv").set_index("id")
    candidates: list[tuple[str, str, np.ndarray]] = []
    for item, path in PREP._locate_sources(raw):
        flashes = PREP._load_flashes(item, path)
        pairs = PREP._pair_flashes(flashes, str(item["key"]))
        built = 0
        for pair_no, (fa, fb) in enumerate(pairs):
            selected = []
            for flash in (fa, fb):
                selected.extend(PREP._select_group_events(flash, str(item["key"]), pair_no))
            events = [event for group in selected for event in group]
            if not (PREP.MIN_DETECTIONS <= len(events) <= PREP.MAX_DETECTIONS):
                continue
            if len({e.gid for e in events}) < 5 or len({e.fid for e in events}) != 2:
                continue
            if sum(len(v) >= 2 for v in selected) < 2:
                continue
            events = sorted(events, key=lambda e: (e.fid, e.gid, e.eid))
            case_id = PREP._alias("case_", str(item["key"]), pair_no, fa.fid, fb.fid, n=14)
            candidates.append((case_id, str(item["key"]), _native_bundle_signature(events)))
            built += 1
            if built >= PREP.CASES_PER_SOURCE:
                break

    candidate_ids = [c[0] for c in candidates]
    candidate_source = [c[1] for c in candidates]
    candidate_signatures = np.vstack([c[2] for c in candidates])
    mu = candidate_signatures.mean(axis=0)
    sd = candidate_signatures.std(axis=0) + 1e-6
    candidate_z = (candidate_signatures - mu) / sd

    ranks, margins = [], []
    top1_exact = 0
    top1_source = 0
    for case in test_cases:
        public_z = (_public_case_signature(case) - mu) / sd
        distances = np.linalg.norm(candidate_z - public_z, axis=1)
        order = np.argsort(distances)
        true_idx = candidate_ids.index(case.case_id)
        ranks.append(int(np.where(order == true_idx)[0][0]) + 1)
        top1_exact += int(candidate_ids[order[0]] == case.case_id)
        top1_source += int(candidate_source[order[0]] == answers.loc[case.case_id, "source_window"])
        margins.append(float(distances[order[1]] - distances[order[0]]))

    exact_rate = top1_exact / max(1, len(test_cases))
    source_rate = top1_source / max(1, len(test_cases))
    report = {
        "candidate_pool_size": len(candidates),
        "test_cases": len(test_cases),
        "top1_exact_case_recovery_rate": round(float(exact_rate), 6),
        "top1_source_window_rate": round(float(source_rate), 6),
        "median_true_case_rank": round(float(np.median(ranks)), 3),
        "p90_true_case_rank": round(float(np.quantile(ranks, 0.90)), 3),
        "median_top2_distance_margin": round(float(np.median(margins)), 9),
        "min_top2_distance_margin": round(float(np.min(margins)), 9),
        "passes": bool(exact_rate <= 0.05 and source_rate <= 0.60 and float(np.median(ranks)) >= 50.0),
    }
    return report


def _leakage_checks(public: Path, private: Path, test_cases: list[Case]):
    train_public = pd.read_csv(public / "train.csv", usecols=["case_json", "prompt"])
    test_public = pd.read_csv(public / "test.csv", usecols=["case_json", "prompt"])
    raw_text = "\n".join(
        train_public.case_json.tolist() + train_public.prompt.tolist()
        + test_public.case_json.tolist() + test_public.prompt.tolist()
    )
    forbidden_patterns = {
        "native_filename": r"OR_GLM|GLM-L2-LCFA|s2024\d{10}|e2024\d{10}|c2024\d{10}",
        "coordinate_schema": r'"(?:lat|latitude|lon|longitude)"',
        "native_hierarchy_ids": r'"(?:event_parent_group|group_parent_flash|event|group|flash)_id"',
        "source_window": r"window_[a-e]|source_window|granule|scan_id|platform_ID",
    }
    hits = {name: bool(re.search(pattern, raw_text, flags=re.IGNORECASE)) for name, pattern in forbidden_patterns.items()}
    id_ok = all(re.fullmatch(r"case_[0-9a-f]{14}", c.case_id) for c in test_cases)
    did_ok = all(re.fullmatch(r"d[0-9a-f]{10}", d) for c in test_cases for d in c.ids)
    all_vectors = [tuple(np.round(row, 4)) for c in test_cases for row in c.x]
    duplicate_vectors = len(all_vectors) - len(set(all_vectors))

    answers = pd.read_csv(private / "answers.csv")
    test = pd.read_csv(public / "test.csv")
    meta = pd.DataFrame({
        "n": [len(json.loads(s)["detections"]) for s in test.case_json],
        "json_len": test.case_json.str.len(),
        "id_prefix": test.id.str[5:9].map(lambda s: int(s, 16)),
    })
    y = answers.set_index("id").loc[test.id, "source_window"].to_numpy()
    cv = StratifiedKFold(5, shuffle=True, random_state=1729)
    source_acc = cross_val_score(
        make_pipeline(StandardScaler(), LogisticRegression(max_iter=500, random_state=1729)),
        meta,
        y,
        cv=cv,
        scoring="accuracy",
    ).mean()
    feature_summary = []
    for c in test_cases:
        row = [len(c.ids)]
        for j in range(c.x.shape[1]):
            row.extend([
                float(np.mean(c.x[:, j])), float(np.std(c.x[:, j])),
                float(np.quantile(c.x[:, j], 0.10)), float(np.quantile(c.x[:, j], 0.90)),
            ])
        feature_summary.append(row)
    feature_source_acc = cross_val_score(
        make_pipeline(StandardScaler(), LogisticRegression(max_iter=500, random_state=1732)),
        np.asarray(feature_summary),
        y,
        cv=cv,
        scoring="accuracy",
    ).mean()
    train_ids = pd.read_csv(public / "train.csv", usecols=["id"]).id.astype(str).tolist()
    test_ids = test.id.astype(str).tolist()
    lexical_split_boundary = max(train_ids) < min(test_ids) or max(test_ids) < min(train_ids)
    n_only_acc = cross_val_score(
        make_pipeline(StandardScaler(), LogisticRegression(max_iter=500, random_state=1733)),
        meta[["n"]],
        y,
        cv=cv,
        scoring="accuracy",
    ).mean()
    json_len_acc = cross_val_score(
        make_pipeline(StandardScaler(), LogisticRegression(max_iter=500, random_state=1734)),
        meta[["json_len"]],
        y,
        cv=cv,
        scoring="accuracy",
    ).mean()
    return {
        "forbidden_public_hits": hits,
        "opaque_case_ids": id_ok,
        "opaque_detection_ids": did_ok,
        "train_test_lexical_id_boundary": bool(lexical_split_boundary),
        "duplicate_public_feature_vectors": duplicate_vectors,
        "metadata_source_window_cv_accuracy": round(float(source_acc), 6),
        "point_count_source_window_cv_accuracy": round(float(n_only_acc), 6),
        "json_length_source_window_cv_accuracy": round(float(json_len_acc), 6),
        "public_feature_source_window_cv_accuracy": round(float(feature_source_acc), 6),
        "metadata_source_window_chance": 0.5,
    }


def main(public: Path, private: Path, output: Path):
    started = time.perf_counter()
    train_df = pd.read_csv(public / "train.csv")
    test_df = pd.read_csv(public / "test.csv")
    answers = pd.read_csv(private / "answers.csv")
    train_cases = _load_cases(train_df, True)
    test_cases = _load_cases(test_df, False)
    train_answers = _answer_frame(train_df)
    results = {}

    perfect = answers[["id", "target_json"]].rename(columns={"target_json": "prediction_json"})
    perfect["confidence"] = 1.0
    _score("native_hierarchy_oracle_sanity_only", perfect, answers, results)
    sample = pd.read_csv(public / "sample_submission.csv")
    _score("sample_submission", sample, answers, results)

    _score("metadata_only", _submission(test_cases, _metadata_predictions(test_cases), 0.20), answers, results)
    _score("lexical_schema_only", _submission(test_cases, _metadata_predictions(test_cases), 0.20), answers, results)
    _score("opaque_id_order", _submission(test_cases, _order_predictions(test_cases), 0.15), answers, results)
    _score("opaque_id_hash", _submission(test_cases, _hash_predictions(test_cases), 0.15), answers, results)
    _score("json_length_count_attack", _submission(test_cases, _length_count_predictions(test_cases), 0.15), answers, results)

    dbscan_started = time.perf_counter()
    fixed = [_dbscan_prediction(c, 0.16, 1.0, 0.50, 0.7) for c in test_cases]
    _score("fixed_operational_threshold_surrogate", _submission(test_cases, fixed, 0.35), answers, results)
    db_train_score, db_params = _tune_dbscan(train_cases, train_answers)
    db_pred = [_dbscan_prediction(c, *db_params) for c in test_cases]
    _score("train_tuned_dbscan", _submission(test_cases, db_pred, 0.42), answers, results)
    results["train_tuned_dbscan"]["train_score"] = round(float(db_train_score), 6)
    results["train_tuned_dbscan"]["parameters"] = list(db_params)
    results["train_tuned_dbscan"]["fixed_and_grid_test_seconds"] = round(
        time.perf_counter() - dbscan_started, 3
    )

    fit_start = time.perf_counter()
    gm, fm, um, model_train, pair_rows = _fit_and_tune_model(train_cases, train_answers)
    model_pred = [_learned_prediction(c, gm, fm, um, *model_train[1]) for c in test_cases]
    _score("small_cpu_pairwise_model", _submission(test_cases, model_pred, 0.58), answers, results)
    results["small_cpu_pairwise_model"]["train_score"] = round(float(model_train[0]), 6)
    results["small_cpu_pairwise_model"]["thresholds"] = list(model_train[1])
    results["small_cpu_pairwise_model"]["training_pairs"] = int(pair_rows)
    results["small_cpu_pairwise_model"]["fit_tune_test_seconds"] = round(time.perf_counter() - fit_start, 3)

    elapsed = time.perf_counter() - started
    peak_mib = None
    try:
        import psutil
        memory = psutil.Process().memory_info()
        peak_mib = getattr(memory, "peak_wset", memory.rss) / (1024 ** 2)
    except Exception:
        pass

    report = {
        "cases": {"train": len(train_cases), "test": len(test_cases)},
        "scores": results,
        "leakage": _leakage_checks(public, private, test_cases),
        "raw_reverse_lookup": _raw_signature_lookup_attack(ROOT / "raw_data", private, test_cases),
        "difficulty_gate": {
            "best_shortcut_score": max(
                results[k]["score"] for k in (
                    "metadata_only", "lexical_schema_only", "opaque_id_order", "opaque_id_hash",
                    "json_length_count_attack",
                    "fixed_operational_threshold_surrogate", "train_tuned_dbscan"
                )
            ),
            "headroom_to_perfect": round(1.0 - max(
                results[k]["score"] for k in (
                    "metadata_only", "lexical_schema_only", "opaque_id_order", "opaque_id_hash",
                    "json_length_count_attack",
                    "fixed_operational_threshold_surrogate", "train_tuned_dbscan"
                )
            ), 6),
            "required_headroom": 0.30,
        },
        "runtime": {
            "analysis_total_seconds": round(elapsed, 3),
            "process_peak_mib": None if peak_mib is None else round(float(peak_mib), 3),
            "logical_cpu_only": True,
        },
    }
    report["difficulty_gate"]["passes"] = report["difficulty_gate"]["headroom_to_perfect"] >= 0.30
    report["leakage"]["passes"] = (
        not any(report["leakage"]["forbidden_public_hits"].values())
        and report["leakage"]["opaque_case_ids"]
        and report["leakage"]["opaque_detection_ids"]
        and not report["leakage"]["train_test_lexical_id_boundary"]
        and report["leakage"]["public_feature_source_window_cv_accuracy"] < 0.75
        and report["raw_reverse_lookup"]["passes"]
    )
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["difficulty_gate"]["passes"] or not report["leakage"]["passes"]:
        raise SystemExit("Analysis gate failed; redesign before handoff.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--public", type=Path, default=ROOT / "public")
    parser.add_argument("--private", type=Path, default=ROOT / "private")
    parser.add_argument("--output", type=Path, default=ROOT / "ANALYSIS_RESULTS.json")
    args = parser.parse_args()
    main(args.public, args.private, args.output)

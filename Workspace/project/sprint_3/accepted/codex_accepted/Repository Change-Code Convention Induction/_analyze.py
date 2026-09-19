from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OrdinalEncoder

from grade import SUBMISSION_COLUMNS, grade


LABEL_COLS = ["change_code", "behavior_changing", "rollback_safe", "required_followup"]
LEAKY_PUBLIC_NAMES = {"event_key", "repo_key", "repo_family", "repo_split", "row_role", "template_id", "archetype", "semantic_group"}
ARCH_TO_SEM = {
    "tests_only": "tests",
    "docs_only": "docs",
    "dependency_config": "config",
    "typing_api": "interface",
    "validation_error": "interface",
    "logging_observability": "observability",
    "async_io": "runtime",
    "cache_perf": "runtime",
    "security_auth": "security",
    "serialization_schema": "data_model",
    "api_contract": "interface",
    "core_logic": "core_logic",
}


def _mode_label(frame: pd.DataFrame) -> dict[str, str]:
    return {col: str(frame[col].astype(str).value_counts().index[0]) for col in LABEL_COLS}


def _bundle_acc(frame: pd.DataFrame, pred: dict[str, str]) -> float:
    ok = np.ones(len(frame), dtype=bool)
    for col in LABEL_COLS:
        ok &= frame[col].astype(str).to_numpy() == pred[col]
    return float(ok.mean()) if len(frame) else 0.2


def _diff_obj(cell: object) -> dict[str, object]:
    try:
        obj = json.loads(str(cell))
        return obj if isinstance(obj, dict) else {"summary": "", "diff": str(cell), "files": []}
    except Exception:
        return {"summary": "", "diff": str(cell), "files": []}


def _diff_text(cell: object) -> str:
    obj = _diff_obj(cell)
    return f"{obj.get('summary', '')}\n{obj.get('diff', '')}"


def parse_archetype(cell: object) -> str:
    obj = _diff_obj(cell)
    text = f"{obj.get('summary', '')}\n{obj.get('diff', '')}".lower()
    files = [str(f).lower() for f in obj.get("files", []) if isinstance(f, str)]
    if files and all(("test" in f or "testing" in f) for f in files):
        return "tests_only"
    if files and all(f.endswith((".md", ".rst")) or "docs/" in f for f in files):
        return "docs_only"
    if any(x in text for x in ["pyproject.toml", "requirements", "setup.cfg", "setup.py", "pre-commit", "ruff", "mypy", "tox.ini", ".github/workflows", "dependabot"]):
        return "dependency_config"
    if any(x in text for x in ["password", "token", "secret", "auth", "credential", "csrf", "scope", "permission"]):
        return "security_auth"
    if any(x in text for x in ["logger.", "logging", "log.", "warning.warn", "deprecated"]):
        return "logging_observability"
    if any(x in text for x in ["async def", "await ", "asyncio", "trio", "anyio"]):
        return "async_io"
    if any(x in text for x in ["cache", "cached", "lru_cache", "memo"]):
        return "cache_perf"
    if any(x in text for x in ["typing", "typevar", "protocol", "literal[", "annotated", "optional[", "mypy", "py.typed"]):
        return "typing_api"
    if any(x in text for x in ["json", "schema", "model_dump", "dict(", "serialize", "deserialize", "field("]):
        return "serialization_schema"
    if any(x in text for x in ["raise ", "valueerror", "typeerror", "validation", "invalid", "error message", "bad request"]):
        return "validation_error"
    if any(x in text for x in ["api", "public", "interface", "parameter", "argument", "return ", "signature"]):
        return "api_contract"
    return "core_logic"


def _extract_lane(profile: str) -> str:
    m = re.search(r"release lane=([^;]+)", str(profile))
    return m.group(1) if m else "unknown"


def _context_items(cell: object) -> list[dict[str, str]]:
    try:
        data = json.loads(str(cell))
    except Exception:
        return []
    out = []
    if not isinstance(data, list):
        return out
    for item in data:
        if not isinstance(item, dict):
            continue
        row = {col: str(item.get(col, "")) for col in LABEL_COLS}
        row["summary"] = str(item.get("summary", ""))
        row["diff"] = str(item.get("diff", ""))
        row["archetype"] = parse_archetype(json.dumps({"summary": row["summary"], "diff": row["diff"], "files": item.get("files", [])}))
        row["semantic"] = ARCH_TO_SEM.get(row["archetype"], "unknown")
        out.append(row)
    return out


def _submission_from_preds(test: pd.DataFrame, preds: list[dict[str, object]]) -> pd.DataFrame:
    rows = []
    for rid, pred in zip(test["row_id"].tolist(), preds):
        row = {"row_id": int(rid)}
        for col in LABEL_COLS:
            row[col] = pred[col]
        row["confidence"] = float(pred.get("confidence", 0.25))
        rows.append(row)
    return pd.DataFrame(rows)[SUBMISSION_COLUMNS]


def _train_group_modes(train: pd.DataFrame, keys: list[str], default: dict[str, str]):
    tmp = train.copy()
    tmp["_key"] = keys
    groups = {}
    confs = {}
    for key, group in tmp.groupby("_key"):
        pred = _mode_label(group)
        groups[key] = pred
        confs[key] = max(0.12, min(0.75, _bundle_acc(group, pred) + 0.08))
    return groups, confs


def score_prior(train: pd.DataFrame, test: pd.DataFrame, answers: pd.DataFrame):
    pred = _mode_label(train)
    conf = max(0.12, min(0.30, _bundle_acc(train, pred) + 0.08))
    return grade(_submission_from_preds(test, [{**pred, "confidence": conf} for _ in range(len(test))]), answers)


def score_by_key(train: pd.DataFrame, test: pd.DataFrame, answers: pd.DataFrame, train_keys: list[str], test_keys: list[str]) -> float:
    default = _mode_label(train)
    default_conf = max(0.12, min(0.30, _bundle_acc(train, default) + 0.08))
    groups, confs = _train_group_modes(train, train_keys, default)
    preds = []
    for key in test_keys:
        pred = dict(groups.get(key, default))
        pred["confidence"] = confs.get(key, default_conf)
        preds.append(pred)
    return grade(_submission_from_preds(test, preds), answers)


def score_context_rule(train: pd.DataFrame, test: pd.DataFrame, answers: pd.DataFrame, semantic: bool = False) -> float:
    default = _mode_label(train)
    arch_train = [parse_archetype(v) for v in train["target_diff"].tolist()]
    by_arch, arch_conf = _train_group_modes(train, arch_train, default)
    preds = []
    for _, row in test.iterrows():
        arch = parse_archetype(row["target_diff"])
        sem = ARCH_TO_SEM.get(arch, "unknown")
        ctx = _context_items(row["repo_context_examples"])
        matches = [c for c in ctx if c["archetype"] == arch]
        if not matches and semantic:
            matches = [c for c in ctx if c["semantic"] == sem]
        if matches:
            pred = {col: Counter(c[col] for c in matches).most_common(1)[0][0] for col in LABEL_COLS}
            pred["confidence"] = 0.62 if len(matches) == 1 else 0.72
        else:
            pred = dict(by_arch.get(arch, default))
            pred["confidence"] = arch_conf.get(arch, 0.22)
        preds.append(pred)
    return grade(_submission_from_preds(test, preds), answers)


def _feature_row(profile: str, diff_cell: object) -> dict[str, str]:
    obj = _diff_obj(diff_cell)
    text = f"{obj.get('summary', '')}\n{obj.get('diff', '')}".lower()
    files = " ".join(str(f).lower() for f in obj.get("files", []))
    return {
        "lane": _extract_lane(profile),
        "archetype": parse_archetype(diff_cell),
        "has_tests": str("test" in files),
        "has_docs": str(".md" in files or ".rst" in files or "docs/" in files),
        "has_config": str(any(x in text for x in ["pyproject", "tox", "workflow", "pre-commit"])),
        "has_security": str(any(x in text for x in ["token", "auth", "secret", "password"])),
        "has_async": str("async" in text or "await " in text),
        "has_typing": str(any(x in text for x in ["typing", "typevar", "protocol", "annotated"])),
        "length_bin": str(min(5, len(text) // 700)),
    }


def score_public_parser_model(train: pd.DataFrame, test: pd.DataFrame, answers: pd.DataFrame) -> float:
    train_features = pd.DataFrame([_feature_row(r["repo_profile"], r["target_diff"]) for _, r in train.iterrows()])
    test_features = pd.DataFrame([_feature_row(r["repo_profile"], r["target_diff"]) for _, r in test.iterrows()])[train_features.columns]
    pred_frame = pd.DataFrame({"row_id": test["row_id"].astype(int).tolist()})
    for col in LABEL_COLS:
        clf = make_pipeline(
            OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
            ExtraTreesClassifier(n_estimators=200, random_state=17),
        )
        clf.fit(train_features.astype(str), train[col].astype(str))
        pred_frame[col] = clf.predict(test_features.astype(str))
    pred_frame["confidence"] = 0.50
    return grade(pred_frame[SUBMISSION_COLUMNS], answers)


def score_hidden_proxy(test: pd.DataFrame, answers: pd.DataFrame) -> float:
    modes = {}
    for key, group in answers.groupby(["repo_policy_group", "target_archetype"]):
        modes[key] = _mode_label(group)
    default = _mode_label(answers)
    preds = []
    for _, a in answers.iterrows():
        pred = dict(modes.get((a["repo_policy_group"], a["target_archetype"]), default))
        pred["confidence"] = 0.78
        preds.append(pred)
    return grade(_submission_from_preds(test, preds), answers)


def raw_leakage_report(raw: Path | None, public: Path) -> None:
    if raw is None:
        return
    records = raw / "records.csv"
    if not records.exists() and (raw / "raw_upload" / "records.csv").exists():
        records = raw / "raw_upload" / "records.csv"
    if not records.exists():
        return
    raw_df = pd.read_csv(records, dtype=str)
    train = pd.read_csv(public / "train.csv")
    test = pd.read_csv(public / "test.csv")
    target_diffs = {_diff_text(v).strip() for v in test["target_diff"].tolist()}
    target_diffs.discard("")
    overlap = 0
    for cell in test["repo_context_examples"].tolist():
        for item in _context_items(cell):
            if str(item.get("diff", "")).strip() in target_diffs:
                overlap += 1
    print(f"raw_check_repo_split_isolated={raw_df.groupby('repo_key')['repo_split'].nunique().max() == 1}")
    print(f"raw_check_row_role_counts={raw_df['row_role'].value_counts().to_dict()}")
    print(f"raw_check_min_support_per_repo={int(raw_df[raw_df['row_role'].eq('support')].groupby('repo_key').size().min())}")
    print(f"public_test_context_target_diff_overlap={overlap}")
    print(f"public_train_leak_columns={sorted(LEAKY_PUBLIC_NAMES & set(train.columns))}")
    print(f"public_test_leak_columns={sorted(LEAKY_PUBLIC_NAMES & set(test.columns))}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--public", type=Path, default=Path("public"))
    ap.add_argument("--private", type=Path, default=Path("private"))
    ap.add_argument("--raw", type=Path, default=None)
    args = ap.parse_args()
    train = pd.read_csv(args.public / "train.csv")
    test = pd.read_csv(args.public / "test.csv")
    answers = pd.read_csv(args.private / "answers.csv")
    print("== prepared split ==")
    print(f"train_rows={len(train)} test_rows={len(test)}")
    print(f"train_missing={int(train.isna().sum().sum())} test_missing={int(test.isna().sum().sum())} answers_missing={int(answers.isna().sum().sum())}")
    print(f"row_id_overlap={len(set(train['row_id']) & set(test['row_id']))}")
    print("test_difficulty_counts=", answers["difficulty_bucket"].value_counts().to_dict())
    print("test_policy_counts=", answers["split_group"].value_counts().to_dict())
    print("test_semantic_counts=", answers["semantic_group"].value_counts().to_dict())
    raw_leakage_report(args.raw, args.public)

    prior = score_prior(train, test, answers)
    sample = grade(pd.read_csv(args.public / "sample_submission.csv"), answers)
    lane = score_by_key(train, test, answers, [_extract_lane(v) for v in train["repo_profile"]], [_extract_lane(v) for v in test["repo_profile"]])
    lengths_train = [str(min(5, len(_diff_text(v)) // 700)) for v in train["target_diff"]]
    lengths_test = [str(min(5, len(_diff_text(v)) // 700)) for v in test["target_diff"]]
    length = score_by_key(train, test, answers, lengths_train, lengths_test)
    arch_train = [parse_archetype(v) for v in train["target_diff"]]
    arch_test = [parse_archetype(v) for v in test["target_diff"]]
    regex = score_by_key(train, test, answers, arch_train, arch_test)
    parser = score_public_parser_model(train, test, answers)
    ctx_exact = score_context_rule(train, test, answers, semantic=False)
    ctx_sem = score_context_rule(train, test, answers, semantic=True)
    hidden = score_hidden_proxy(test, answers)
    perfect = answers[["row_id", *LABEL_COLS]].copy()
    perfect["confidence"] = 1.0
    perfect_score = grade(perfect[SUBMISSION_COLUMNS], answers)
    scores = {
        "sample_submission": sample,
        "train_prior": prior,
        "metadata_lane_only": lane,
        "length_only": length,
        "regex_archetype_global": regex,
        "public_profile_diff_parser": parser,
        "calibration_exact_match": ctx_exact,
        "calibration_semantic_rule": ctx_sem,
        "hidden_repo_archetype_proxy": hidden,
        "perfect_labels": perfect_score,
    }
    print("\n== baseline and skill sweep ==")
    for k, v in scores.items():
        print(f"{k}={v:.6f}")
    assert abs(perfect_score - 1.0) < 1e-12
    assert 0.12 <= sample < 0.50
    assert parser < 0.75
    assert regex < perfect_score
    print("OK: analyze checks passed")


if __name__ == "__main__":
    main()

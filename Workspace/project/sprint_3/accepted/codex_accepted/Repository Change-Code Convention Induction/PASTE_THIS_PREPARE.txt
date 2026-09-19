from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


ID_SALT = "real-repo-change-code-convention-v2"
ID_SPACE = 100_000_000
MIN_GROUP_TEST = 20

REQUIRED_RAW_COLUMNS = [
    "event_key",
    "repo_key",
    "repo_split",
    "row_role",
    "repo_domain",
    "repo_profile",
    "event_index",
    "target_summary",
    "target_diff",
]
PRIVATE_FAMILIES = [
    "compatibility_guard",
    "release_safety",
    "test_contracts",
    "config_ops",
    "api_stability",
    "security_runtime",
    "ops_canary",
]
DIFFICULTIES = [
    "direct_calibration_match",
    "near_paraphrase",
    "code_semantic_variant",
    "convention_inverted_family",
    "underdetermined_latent_state",
]
CODES = [f"T_{i:02d}" for i in range(1, 12)]
SEMANTIC_GROUP = {
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
TRAIN_COLUMNS = [
    "row_id",
    "repo_profile",
    "repo_context_examples",
    "target_diff",
    "change_code",
    "behavior_changing",
    "rollback_safe",
    "required_followup",
]
TEST_COLUMNS = ["row_id", "repo_profile", "repo_context_examples", "target_diff"]
SUBMISSION_COLUMNS = [
    "row_id",
    "change_code",
    "behavior_changing",
    "rollback_safe",
    "required_followup",
    "confidence",
]
ANSWER_COLUMNS = [
    "row_id",
    "change_code",
    "behavior_changing",
    "rollback_safe",
    "required_followup",
    "difficulty_bucket",
    "split_group",
    "semantic_group",
    "target_archetype",
    "repo_policy_group",
]


def _raw_root(raw: Path) -> Path:
    if (raw / "records.csv").exists():
        return raw
    if (raw / "raw_upload" / "records.csv").exists():
        return raw / "raw_upload"
    raise FileNotFoundError(f"Could not find records.csv under {raw} or {raw / 'raw_upload'}")


def _validate_raw(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_RAW_COLUMNS if c not in df.columns]
    if missing:
        raise SystemExit(f"records.csv missing required columns: {missing}")
    required = df[REQUIRED_RAW_COLUMNS]
    if required.isna().any().any():
        bad = required.columns[required.isna().any()].tolist()
        raise SystemExit(f"records.csv has missing values in {bad}")
    blank = [c for c in REQUIRED_RAW_COLUMNS if required[c].astype(str).str.strip().eq("").any()]
    if blank:
        raise SystemExit(f"records.csv has blank values in {blank}")
    if df["event_key"].duplicated().any():
        raise SystemExit("records.csv contains duplicate event_key values")
    if int(df.groupby("repo_key")["repo_split"].nunique().max()) != 1:
        raise SystemExit("A repo_key appears in more than one split")
    bad_split = sorted(set(df["repo_split"]) - {"train", "test"})
    bad_role = sorted(set(df["row_role"]) - {"target", "support"})
    if bad_split:
        raise SystemExit(f"Unexpected repo_split values: {bad_split}")
    if bad_role:
        raise SystemExit(f"Unexpected row_role values: {bad_role}")
    role_counts = df.groupby(["repo_key", "row_role"]).size().unstack(fill_value=0)
    support_counts = role_counts["support"] if "support" in role_counts else pd.Series(0, index=role_counts.index)
    target_counts = role_counts["target"] if "target" in role_counts else pd.Series(0, index=role_counts.index)
    if (support_counts < 3).any():
        raise SystemExit("Every repo must have at least three support rows")
    if (target_counts < 1).any():
        raise SystemExit("Every repo must have target rows")


def _id_from_event(event_key: str) -> int:
    digest = hashlib.sha256(f"{ID_SALT}:{event_key}".encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big") % ID_SPACE


def _hash_order(salt: str, key: str) -> str:
    return hashlib.sha256(f"{salt}:{key}".encode("utf-8")).hexdigest()


def _stable_int(*parts: object) -> int:
    digest = hashlib.sha256("::".join(map(str, parts)).encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def _repo_policy(repo_key: str, family: str) -> dict[str, str]:
    codes = CODES[:]
    seed = _stable_int("private_policy", repo_key, family)
    for i in range(len(codes) - 1, 0, -1):
        j = seed % (i + 1)
        seed //= 11
        codes[i], codes[j] = codes[j], codes[i]
    groups = ["tests", "docs", "config", "interface", "observability", "runtime", "security", "data_model", "core_logic"]
    return {g: codes[i % len(codes)] for i, g in enumerate(groups)}


def _diff_obj(cell: object) -> dict[str, object]:
    try:
        obj = json.loads(str(cell))
        return obj if isinstance(obj, dict) else {"summary": "", "diff": str(cell), "files": []}
    except Exception:
        return {"summary": "", "diff": str(cell), "files": []}


def _diff_text(cell: object) -> str:
    obj = _diff_obj(cell)
    return f"{obj.get('summary', '')}\n{obj.get('diff', '')}".lower()


def _classify_archetype(cell: object) -> str:
    obj = _diff_obj(cell)
    text = f"{obj.get('summary', '')}\n{obj.get('diff', '')}".lower()
    files = [str(f).lower() for f in obj.get("files", []) if isinstance(f, str)]
    summary = str(obj.get("summary", "")).lower()
    if "regression coverage" in summary or (files and all(("test" in f or "testing" in f) for f in files)):
        return "tests_only"
    if "documentation" in summary or (files and all(f.endswith((".md", ".rst")) or "docs/" in f for f in files)):
        return "docs_only"
    if "dependency" in summary or "tooling" in summary or "ci configuration" in summary:
        return "dependency_config"
    if "authentication" in summary or "permission" in summary or any(x in text for x in ["password", "token", "secret", "auth", "credential", "csrf", "scope", "permission"]):
        return "security_auth"
    if "logging" in summary or "observability" in summary or any(x in text for x in ["logger.", "logging", "log.", "warning.warn", "deprecated"]):
        return "logging_observability"
    if "asynchronous" in summary or any(x in text for x in ["async def", "await ", "asyncio", "trio", "anyio"]):
        return "async_io"
    if "caching" in summary or any(x in text for x in ["cache", "cached", "lru_cache", "memo"]):
        return "cache_perf"
    if "typing" in summary or any(x in text for x in ["typing", "typevar", "protocol", "literal[", "annotated", "optional[", "mypy", "py.typed"]):
        return "typing_api"
    if "serialization" in summary or "schema" in summary or any(x in text for x in ["json", "schema", "model_dump", "dict(", "serialize", "deserialize", "field("]):
        return "serialization_schema"
    if "validation" in summary or "error-handling" in summary or any(x in text for x in ["raise ", "valueerror", "typeerror", "validation", "invalid", "error message", "bad request"]):
        return "validation_error"
    if "api contract" in summary or any(x in text for x in ["api", "public", "interface", "parameter", "argument", "return ", "signature"]):
        return "api_contract"
    return "core_logic"


def _classify_labels(policy: dict[str, str], family: str, archetype: str, difficulty: str, diff_cell: object) -> tuple[str, str, str, str]:
    sem = SEMANTIC_GROUP[archetype]
    code = policy[sem]
    low = _diff_text(diff_cell)
    if archetype in {"validation_error", "api_contract"} and ("signature" in low or "parameter" in low):
        code = CODES[(CODES.index(code) + 1) % len(CODES)]
    if archetype == "dependency_config" and any(x in low for x in ["workflow", "tox", "pre-commit", "dependabot"]):
        code = CODES[(CODES.index(code) + 2) % len(CODES)]
    if archetype == "typing_api" and family in {"api_stability", "compatibility_guard"}:
        code = CODES[(CODES.index(code) + 1) % len(CODES)]
    under = difficulty == "underdetermined_latent_state" and archetype in {"core_logic", "dependency_config", "async_io"}
    if under:
        behavior = "abstain"
        rollback = "abstain"
    elif archetype in {"tests_only", "docs_only", "typing_api"}:
        behavior = "no"
        rollback = "yes"
    elif archetype == "logging_observability":
        behavior = "yes" if family in {"security_runtime", "ops_canary"} else "no"
        rollback = "yes"
    elif archetype in {"security_auth", "api_contract", "serialization_schema", "core_logic"}:
        behavior = "yes"
        rollback = "no" if family in {"release_safety", "api_stability", "security_runtime"} else "yes"
    else:
        behavior = "yes"
        rollback = "yes"
    if archetype == "security_auth":
        follow = "security_review"
    elif archetype in {"cache_perf", "async_io"}:
        follow = "perf_review"
    elif archetype == "dependency_config":
        follow = "config_review"
    elif archetype in {"validation_error", "api_contract", "serialization_schema"}:
        follow = "add_test"
    elif archetype == "core_logic" or under:
        follow = "owner_review"
    else:
        follow = "none"
    return code, behavior, rollback, follow


def _add_private_overlay(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    repo_order = sorted(df["repo_key"].astype(str).unique(), key=lambda k: _hash_order("private_family", k))
    family_map = {repo: PRIVATE_FAMILIES[i % len(PRIVATE_FAMILIES)] for i, repo in enumerate(repo_order)}
    df["repo_family"] = df["repo_key"].astype(str).map(family_map)
    df["archetype"] = df["target_diff"].map(_classify_archetype)
    df["semantic_group"] = df["archetype"].map(SEMANTIC_GROUP)
    df["difficulty_bucket"] = [
        DIFFICULTIES[(int(event_idx) + (2 if str(role) == "support" else 0)) % len(DIFFICULTIES)]
        for event_idx, role in zip(df["event_index"].tolist(), df["row_role"].tolist())
    ]
    labels = []
    for r in df.to_dict("records"):
        policy = _repo_policy(str(r["repo_key"]), str(r["repo_family"]))
        labels.append(_classify_labels(policy, str(r["repo_family"]), str(r["archetype"]), str(r["difficulty_bucket"]), r["target_diff"]))
    df[["change_code", "behavior_changing", "rollback_safe", "required_followup"]] = pd.DataFrame(labels, index=df.index)
    return df


def _context_item(r: dict[str, object]) -> dict[str, object]:
    obj = json.loads(str(r["target_diff"]))
    return {
        "summary": str(r["target_summary"]),
        "files": obj.get("files", []),
        "diff": obj.get("diff", ""),
        "change_code": str(r["change_code"]),
        "behavior_changing": str(r["behavior_changing"]),
        "rollback_safe": str(r["rollback_safe"]),
        "required_followup": str(r["required_followup"]),
    }


def _pick_context(row: dict[str, object], support_records: list[dict[str, object]]) -> str:
    if len(support_records) < 3:
        raise SystemExit(f"Repo {row['repo_key']} has too few support rows")
    target_arch = str(row["archetype"])
    target_sem = str(row["semantic_group"])
    difficulty = str(row["difficulty_bucket"])
    chosen: list[str] = []
    by_key = {str(r["event_key"]): r for r in support_records}

    def add_from(records: list[dict[str, object]], limit: int) -> None:
        ordered = sorted(records, key=lambda r: (_hash_order(str(row["event_key"]), str(r["event_key"])), str(r["event_key"])))
        for cand in ordered:
            key = str(cand["event_key"])
            if key not in chosen:
                chosen.append(key)
            if len(chosen) >= limit or len(chosen) >= 6:
                break

    same_arch = [r for r in support_records if str(r["archetype"]) == target_arch]
    same_sem = [r for r in support_records if str(r["semantic_group"]) == target_sem]
    different_arch = [r for r in support_records if str(r["archetype"]) != target_arch]
    same_sem_different_arch = [r for r in same_sem if str(r["archetype"]) != target_arch]
    if difficulty == "direct_calibration_match":
        add_from(same_arch, 2)
    if difficulty == "near_paraphrase":
        add_from(same_sem_different_arch, 3)
    if difficulty == "code_semantic_variant":
        add_from(same_sem_different_arch, 3)
    if difficulty == "convention_inverted_family":
        add_from([r for r in support_records if str(r["semantic_group"]) in {"interface", "config", "runtime", "security"}], 4)
    if difficulty == "underdetermined_latent_state":
        add_from([r for r in support_records if str(r["behavior_changing"]) == "abstain" or str(r["rollback_safe"]) == "abstain"], 2)
        add_from([r for r in support_records if str(r["semantic_group"]) in {"core_logic", "config", "runtime"}], 4)
    if difficulty == "direct_calibration_match":
        add_from(same_sem, 4)
        add_from(support_records, 6)
    else:
        add_from(same_sem_different_arch, 4)
        add_from(different_arch, 6)

    desired = 3 + (hashlib.sha256(str(row["event_key"]).encode()).digest()[0] % 4)
    chosen = chosen[:desired]
    if len(chosen) < 3:
        add_from(support_records, 3)
        chosen = chosen[:3]
    return json.dumps([_context_item(by_key[k]) for k in chosen], sort_keys=True, separators=(",", ":"))


def _target_diff_text(cell: object) -> str:
    try:
        obj = json.loads(str(cell))
        return str(obj.get("diff", "")).strip()
    except Exception:
        return str(cell).strip()


def _assert_no_target_context_overlap(test_out: pd.DataFrame) -> None:
    target_diffs = {_target_diff_text(v) for v in test_out["target_diff"].tolist()}
    target_diffs.discard("")
    leaking: list[int] = []
    for _, row in test_out.iterrows():
        items = json.loads(str(row["repo_context_examples"]))
        if not isinstance(items, list):
            raise SystemExit("repo_context_examples must be a JSON list")
        for item in items:
            if str(item.get("diff", "")).strip() in target_diffs:
                leaking.append(int(row["row_id"]))
                break
    if leaking:
        raise SystemExit(f"Test target diff appears inside public calibration context: {leaking[:10]}")


def _mode(series: pd.Series) -> str:
    return str(series.astype(str).value_counts().index[0])


def _coarsen_sparse_axis(df: pd.DataFrame, col: str, fallback: str) -> pd.DataFrame:
    counts = df[col].astype(str).value_counts()
    rare = counts[counts < MIN_GROUP_TEST].index.tolist()
    if not rare:
        return df
    df.loc[df[col].astype(str).isin(rare), col] = fallback
    updated = df[col].astype(str).value_counts()
    if fallback in updated.index and int(updated[fallback]) < MIN_GROUP_TEST:
        majority = updated.drop(index=fallback, errors="ignore").idxmax()
        df.loc[df[col].astype(str) == fallback, col] = majority
    return df


def _enforce_group_floor(df: pd.DataFrame) -> None:
    for col in ["difficulty_bucket", "split_group", "semantic_group"]:
        counts = df[col].astype(str).value_counts()
        if len(counts) == 0 or int(counts.min()) < MIN_GROUP_TEST:
            raise SystemExit(f"TEST subgroup {col} too small: {counts.to_dict()}")


def prepare(raw: Path, public: Path, private: Path) -> None:
    raw_root = _raw_root(Path(raw))
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(raw_root / "records.csv", dtype=str)
    _validate_raw(df)
    df["event_index"] = df["event_index"].astype(int)
    df = _add_private_overlay(df)
    df = df.sort_values(["repo_key", "row_role", "event_index", "event_key"]).reset_index(drop=True)
    id_map = {str(k): _id_from_event(str(k)) for k in df["event_key"].tolist()}
    if len(set(id_map.values())) != len(id_map):
        raise SystemExit("Hash-derived row_id collision; change ID_SALT")
    df["row_id"] = df["event_key"].map(id_map).astype(int)

    target_df = df[df["row_role"].eq("target")].copy()
    support_df = df[df["row_role"].eq("support")].copy()
    train_df = target_df[target_df["repo_split"].eq("train")].copy()
    test_df = target_df[target_df["repo_split"].eq("test")].copy()
    if train_df.empty or test_df.empty:
        raise SystemExit("Both train and test target splits must be non-empty")
    if set(train_df["repo_key"]) & set(test_df["repo_key"]):
        raise SystemExit("Repo split leakage: repo_key appears in both train and test")
    support_groups = {repo: g.to_dict("records") for repo, g in support_df.groupby("repo_key", sort=False)}

    train_rows = []
    test_rows = []
    answer_rows = []
    for r in train_df.to_dict("records"):
        train_rows.append({
            "row_id": int(r["row_id"]),
            "repo_profile": str(r["repo_profile"]),
            "repo_context_examples": _pick_context(r, support_groups[str(r["repo_key"])]),
            "target_diff": str(r["target_diff"]),
            "change_code": str(r["change_code"]),
            "behavior_changing": str(r["behavior_changing"]),
            "rollback_safe": str(r["rollback_safe"]),
            "required_followup": str(r["required_followup"]),
        })
    for r in test_df.to_dict("records"):
        test_rows.append({
            "row_id": int(r["row_id"]),
            "repo_profile": str(r["repo_profile"]),
            "repo_context_examples": _pick_context(r, support_groups[str(r["repo_key"])]),
            "target_diff": str(r["target_diff"]),
        })
        answer_rows.append({
            "row_id": int(r["row_id"]),
            "change_code": str(r["change_code"]),
            "behavior_changing": str(r["behavior_changing"]),
            "rollback_safe": str(r["rollback_safe"]),
            "required_followup": str(r["required_followup"]),
            "difficulty_bucket": str(r["difficulty_bucket"]),
            "split_group": str(r["repo_family"]),
            "semantic_group": str(r["semantic_group"]),
            "target_archetype": str(r["archetype"]),
            "repo_policy_group": str(r["repo_family"]),
        })

    train_out = pd.DataFrame(train_rows)[TRAIN_COLUMNS].sort_values("row_id").reset_index(drop=True)
    test_out = pd.DataFrame(test_rows)[TEST_COLUMNS].sort_values("row_id").reset_index(drop=True)
    answers = pd.DataFrame(answer_rows)[ANSWER_COLUMNS].sort_values("row_id").reset_index(drop=True)
    answers = _coarsen_sparse_axis(answers, "semantic_group", "other_semantics")
    _enforce_group_floor(answers)
    _assert_no_target_context_overlap(test_out)

    modes = {
        "change_code": _mode(train_out["change_code"]),
        "behavior_changing": _mode(train_out["behavior_changing"]),
        "rollback_safe": _mode(train_out["rollback_safe"]),
        "required_followup": _mode(train_out["required_followup"]),
    }
    bundle = (
        (train_out["change_code"].astype(str) == modes["change_code"])
        & (train_out["behavior_changing"].astype(str) == modes["behavior_changing"])
        & (train_out["rollback_safe"].astype(str) == modes["rollback_safe"])
        & (train_out["required_followup"].astype(str) == modes["required_followup"])
    )
    conf = float(max(0.12, min(0.30, bundle.mean() + 0.08)))
    sample = pd.DataFrame([{
        "row_id": int(rid),
        **modes,
        "confidence": round(conf, 4),
    } for rid in test_out["row_id"]])[SUBMISSION_COLUMNS].sort_values("row_id").reset_index(drop=True)

    for name, frame in [("train", train_out), ("test", test_out), ("answers", answers), ("sample", sample)]:
        if frame.isna().any().any():
            raise SystemExit(f"{name}.csv has missing values")
    train_out.to_csv(public / "train.csv", index=False)
    test_out.to_csv(public / "test.csv", index=False)
    sample.to_csv(public / "sample_submission.csv", index=False)
    answers.to_csv(private / "answers.csv", index=False)
    print(f"  [done] {len(train_out)} train rows, {len(test_out)} test rows.")
    print(f"  [groups] difficulty={answers['difficulty_bucket'].value_counts().to_dict()}")
    print(f"  [groups] policy={answers['split_group'].value_counts().to_dict()}")
    print(f"  [groups] semantic={answers['semantic_group'].value_counts().to_dict()}")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=Path("raw_data"))
    ap.add_argument("--public", type=Path, default=Path("public"))
    ap.add_argument("--private", type=Path, default=Path("private"))
    args = ap.parse_args()
    prepare(args.raw.resolve(), args.public.resolve(), args.private.resolve())
    print("OK: prepare complete.")

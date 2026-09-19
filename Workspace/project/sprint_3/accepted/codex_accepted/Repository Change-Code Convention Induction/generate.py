from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path


REPOS = [
    ("pallets/flask", "BSD-3-Clause", "train"),
    ("pallets/werkzeug", "BSD-3-Clause", "train"),
    ("pallets/click", "BSD-3-Clause", "train"),
    ("pytest-dev/pytest", "MIT", "train"),
    ("psf/requests", "Apache-2.0", "train"),
    ("pydantic/pydantic", "MIT", "test"),
    ("psf/black", "MIT", "test"),
]

CODES = [f"T_{i:02d}" for i in range(1, 12)]
FAMILIES = [
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
FIELDNAMES = [
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


def _run(cmd: list[str], timeout: int = 180) -> str:
    return subprocess.check_output(cmd, text=True, errors="replace", timeout=timeout)


def stable_hex(*parts: object, n: int = 16) -> str:
    return hashlib.sha256("::".join(map(str, parts)).encode("utf-8")).hexdigest()[:n]


def stable_int(*parts: object) -> int:
    return int(stable_hex(*parts, n=16), 16)


def ensure_clone(repo: str, cache: Path) -> Path:
    dst = cache / repo.replace("/", "__")
    if (dst / ".git").exists():
        return dst
    if dst.exists():
        raise RuntimeError(f"Clone destination exists but is not a git repo: {dst}")
    _run([
        "git",
        "clone",
        "--no-checkout",
        "--depth",
        "280",
        "--filter=blob:none",
        "--single-branch",
        f"https://github.com/{repo}.git",
        str(dst),
    ], timeout=300)
    return dst


def parse_log(text: str) -> list[tuple[str, str, str]]:
    commits: list[tuple[str, str, str]] = []
    cur: tuple[str, str] | None = None
    patch: list[str] = []
    for line in text.splitlines():
        if line.startswith("@@COMMIT@@"):
            if cur and patch:
                commits.append((cur[0], cur[1], "\n".join(patch)))
            payload = line[len("@@COMMIT@@"):]
            if "\x1f" in payload:
                sha, subject = payload.split("\x1f", 1)
                cur = (sha.strip(), subject.strip())
                patch = []
            else:
                cur = None
                patch = []
        elif cur:
            patch.append(line)
    if cur and patch:
        commits.append((cur[0], cur[1], "\n".join(patch)))
    return commits


def compact_patch(patch: str) -> str:
    blocks: list[str] = []
    cur: list[str] = []
    for line in patch.replace("\r\n", "\n").splitlines():
        if line.startswith("diff --git "):
            if cur:
                blocks.append("\n".join(cur))
            cur = [line]
        elif cur:
            cur.append(line)
    if cur:
        blocks.append("\n".join(cur))

    kept: list[str] = []
    for block in blocks:
        head = block.split("\n", 1)[0].lower()
        if not any(ext in head for ext in [".py", ".toml", ".yaml", ".yml", ".md", ".rst", ".cfg", ".ini"]):
            continue
        if any(skip in head for skip in ["poetry.lock", "pdm.lock", "package-lock"]):
            continue
        kept.append(block)

    out: list[str] = []
    for line in "\n".join(kept).splitlines():
        if line.startswith(("index ", "similarity index", "new file mode", "deleted file mode")):
            continue
        out.append(line[:260])
        if len("\n".join(out)) > 4200:
            break
    return "\n".join(out).strip()


def classify_archetype(subject: str, patch: str) -> str:
    low = f"{subject}\n{patch}".lower()
    files = re.findall(r"diff --git a/([^ ]+)", patch)
    if files and all(("test" in f.lower() or "testing" in f.lower()) for f in files):
        return "tests_only"
    if files and all(f.lower().endswith((".md", ".rst")) or "docs/" in f.lower() for f in files):
        return "docs_only"
    if any(x in low for x in ["pyproject.toml", "requirements", "setup.cfg", "setup.py", "pre-commit", "ruff", "mypy", "tox.ini", ".github/workflows", "dependabot"]):
        return "dependency_config"
    if any(x in low for x in ["password", "token", "secret", "auth", "credential", "csrf", "scope", "permission"]):
        return "security_auth"
    if any(x in low for x in ["logger.", "logging", "log.", "warning.warn", "deprecated"]):
        return "logging_observability"
    if any(x in low for x in ["async def", "await ", "asyncio", "trio", "anyio"]):
        return "async_io"
    if any(x in low for x in ["cache", "cached", "lru_cache", "memo"]):
        return "cache_perf"
    if any(x in low for x in ["typing", "typevar", "protocol", "literal[", "annotated", "optional[", "mypy", "py.typed"]):
        return "typing_api"
    if any(x in low for x in ["json", "schema", "model_dump", "dict(", "serialize", "deserialize", "field("]):
        return "serialization_schema"
    if any(x in low for x in ["raise ", "valueerror", "typeerror", "validation", "invalid", "error message", "bad request"]):
        return "validation_error"
    if any(x in low for x in ["api", "public", "interface", "parameter", "argument", "return ", "signature"]):
        return "api_contract"
    return "core_logic"


def anonymize_path(path: str, repo_idx: int) -> str:
    low = path.lower()
    suffix = Path(path).suffix or ".txt"
    if "test" in low or "testing" in low:
        area = "tests"
    elif low.endswith((".md", ".rst")) or "docs/" in low:
        area = "docs"
    elif any(x in low for x in ["pyproject", "setup", "tox", "workflow", "requirements", "pre-commit"]):
        area = "config"
    else:
        area = "src"
    return f"{area}/module_{repo_idx}_{stable_hex(path, n=8)}{suffix}"


def anonymize_patch_paths(patch: str, repo_idx: int) -> tuple[str, list[str]]:
    path_map: dict[str, str] = {}

    def mapped(path: str) -> str:
        if path in {"/dev/null", ""}:
            return path
        path_map.setdefault(path, anonymize_path(path, repo_idx))
        return path_map[path]

    out: list[str] = []
    for line in patch.splitlines():
        m = re.match(r"diff --git a/(.*?) b/(.*)$", line)
        if m:
            left = mapped(m.group(1))
            right = mapped(m.group(2))
            out.append(f"diff --git a/{left} b/{right}")
            continue
        m = re.match(r"(---|\+\+\+) ([ab])/(.*)$", line)
        if m:
            out.append(f"{m.group(1)} {m.group(2)}/{mapped(m.group(3))}")
            continue
        out.append(line)
    files = list(dict.fromkeys(path_map.values()))
    return "\n".join(out), files


def public_summary(archetype: str, event_index: int) -> str:
    phrases = {
        "tests_only": "Adjust regression coverage for a repository behavior",
        "docs_only": "Update documentation around a public workflow",
        "dependency_config": "Change dependency, tooling, or CI configuration",
        "typing_api": "Refine typing annotations or compatibility surface",
        "validation_error": "Revise validation or error-handling behavior",
        "logging_observability": "Change logging, warning, or observability behavior",
        "async_io": "Adjust asynchronous or I/O control flow",
        "cache_perf": "Change caching or performance-related behavior",
        "security_auth": "Modify authentication, token, or permission handling",
        "serialization_schema": "Change serialization, schema, or structured output behavior",
        "api_contract": "Modify an API contract or public call surface",
        "core_logic": "Change core repository logic",
    }
    return f"{phrases.get(archetype, 'Change repository behavior')} [{event_index % 17}]"


def repo_policy(repo_idx: int) -> dict[str, str]:
    codes = CODES[:]
    seed = stable_int("policy", repo_idx)
    for i in range(len(codes) - 1, 0, -1):
        j = seed % (i + 1)
        seed //= 11
        codes[i], codes[j] = codes[j], codes[i]
    groups = ["tests", "docs", "config", "interface", "observability", "runtime", "security", "data_model", "core_logic"]
    return {g: codes[i % len(codes)] for i, g in enumerate(groups)}


def classify_labels(policy: dict[str, str], family: str, archetype: str, difficulty: str, patch: str) -> tuple[str, str, str, str]:
    sem = SEMANTIC_GROUP[archetype]
    code = policy[sem]
    low = patch.lower()
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


def license_text(repo_path: Path) -> str:
    for name in ["LICENSE", "LICENSE.txt", "LICENSE.md", "LICENSE.rst", "COPYING", "COPYING.rst"]:
        try:
            proc = subprocess.run(
                ["git", "-C", str(repo_path), "show", f"HEAD:{name}"],
                text=True,
                errors="replace",
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                timeout=30,
                check=False,
            )
            text = proc.stdout if proc.returncode == 0 else ""
            if text.strip():
                return text.strip()
        except Exception:
            continue
    return "License file not found in sampled shallow clone."


def build_rows(args: argparse.Namespace) -> tuple[list[dict[str, object]], list[dict[str, object]], str]:
    cache = Path(args.cache)
    cache.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    attributions: list[dict[str, object]] = []
    license_sections: list[str] = [
        "Dataset compilation labels/profiles are CC0 1.0.",
        "Original code diffs remain under the upstream permissive licenses listed below. Preserve upstream notices when redistributing.",
    ]

    for repo_idx, (repo, license_id, split) in enumerate(REPOS):
        repo_path = ensure_clone(repo, cache)
        log_text = _run([
            "git",
            "-C",
            str(repo_path),
            "log",
            "--no-merges",
            "--format=@@COMMIT@@%H%x1f%s",
            "-p",
            "--unified=3",
            "-n",
            str(args.log_limit),
            "--",
            ":*.py",
            ":*.toml",
            ":*.yml",
            ":*.yaml",
            ":*.md",
            ":*.rst",
            ":*.cfg",
            ":*.ini",
        ], timeout=300)

        candidates: list[tuple[str, str, str, str]] = []
        seen: set[str] = set()
        for sha, subject, patch in parse_log(log_text):
            compact = compact_patch(patch)
            if len(compact) < 250 or len(compact) > 4500 or compact in seen:
                continue
            seen.add(compact)
            candidates.append((sha, subject, compact, classify_archetype(subject, compact)))
        candidates = sorted(candidates, key=lambda item: stable_hex(repo, item[0]))

        support_n = min(args.support_per_repo, max(8, len(candidates) // 5))
        target_n = min(args.target_per_repo, len(candidates) - support_n)
        if support_n < 8 or target_n < 30:
            raise RuntimeError(f"Not enough usable commits from {repo}: {len(candidates)} candidates")
        selected = candidates[:support_n + target_n]

        repo_key = f"realrepo_{stable_hex(repo, n=12)}"
        profile = (
            "Repository profile: real permissively licensed Python project; "
            "infer private change-code policy from labeled support examples. Repo/source names are withheld from public rows."
        )

        for i, (sha, subject, patch, archetype) in enumerate(selected):
            role = "support" if i < support_n else "target"
            event_index = i if role == "support" else i - support_n
            public_patch, files = anonymize_patch_paths(patch, repo_idx)
            summary = public_summary(archetype, event_index)
            target_diff = json.dumps({"summary": summary, "files": files[:8], "diff": public_patch}, sort_keys=True)
            rows.append({
                "event_key": f"real_evt_{stable_hex(repo, sha, role, n=18)}",
                "repo_key": repo_key,
                "repo_split": split,
                "row_role": role,
                "repo_domain": "real_python",
                "repo_profile": profile,
                "event_index": event_index,
                "target_summary": summary,
                "target_diff": target_diff,
            })

        attributions.append({
            "repo_slug": repo,
            "license": license_id,
            "source_url": f"https://github.com/{repo}",
            "sampled_commits": support_n + target_n,
        })
        license_sections.append(f"\n--- {repo} ({license_id}) ---\n{license_text(repo_path)}")
        print(f"{repo}: {support_n} support + {target_n} targets")

    return rows, attributions, "\n".join(license_sections) + "\n"


def write_outputs(rows: list[dict[str, object]], attributions: list[dict[str, object]], license_notice: str, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    with (output / "records.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    with (output / "attributions.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["repo_slug", "license", "source_url", "sampled_commits"])
        writer.writeheader()
        writer.writerows(attributions)
    manifest = {
        "dataset": "Permissive Python Repository Commit Diffs",
        "rows": len(rows),
        "target_rows": sum(1 for r in rows if r["row_role"] == "target"),
        "support_rows": sum(1 for r in rows if r["row_role"] == "support"),
        "sources": attributions,
        "label_note": "Raw rows contain real/anonymized commit diff inputs only. Private house-code and release-policy labels are derived by prepare.py.",
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    (output / "LICENSE.txt").write_text(license_notice, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=Path("raw_data"))
    ap.add_argument("--cache", type=Path, default=Path("real_source_repos"))
    ap.add_argument("--log-limit", type=int, default=260)
    ap.add_argument("--target-per-repo", type=int, default=120)
    ap.add_argument("--support-per-repo", type=int, default=24)
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    if args.quick:
        args.log_limit = min(args.log_limit, 90)
        args.target_per_repo = min(args.target_per_repo, 36)
        args.support_per_repo = min(args.support_per_repo, 12)
    return args


def main() -> None:
    args = parse_args()
    rows, attributions, notice = build_rows(args)
    write_outputs(rows, attributions, notice, args.output)
    print(
        f"Wrote {len(rows)} rows to {args.output} "
        f"({sum(r['row_role'] == 'target' for r in rows)} targets, {sum(r['row_role'] == 'support' for r in rows)} support)."
    )


if __name__ == "__main__":
    main()

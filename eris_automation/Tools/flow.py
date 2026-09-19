#!/usr/bin/env python3
"""Durable local controller for Project Eris challenge batches."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_AUTOMATION_ROOT = SCRIPT_PATH.parents[1]
AUTOMATION_ROOT = Path(os.environ.get("ERIS_AUTOMATION_HOME", DEFAULT_AUTOMATION_ROOT)).resolve()
PROJECT_ROOT = Path(os.environ.get("ERIS_PROJECT_ROOT", AUTOMATION_ROOT.parent)).resolve()
STATE_ROOT = AUTOMATION_ROOT / "State"
BATCH_ROOT = STATE_ROOT / "batches"
TASK_ROOT = STATE_ROOT / "tasks"
CONTROLLER_PATH = STATE_ROOT / "controller.json"
REGISTRY_ROOT = PROJECT_ROOT / "challenge_registry"

ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,79}$")
SHIPD_DATASET_URL_RE = re.compile(
    r"^https://shipd\.ai/quests/eris/datasets/([a-z0-9]+)(?:[/?#].*)?$", re.IGNORECASE
)
SHIPD_PROBLEM_URL_RE = re.compile(
    r"^https://shipd\.ai/quests/eris/(?:problems|challenges)/([a-z0-9]+)(?:[/?#].*)?$",
    re.IGNORECASE,
)
SUCCESS_STATES = {"agent_runs_started", "accepted"}
LEGACY_TERMINAL_STATES = {"agent_runs_started", "accepted", "rejected", "abandoned"}
TASK_STATES = {
    "queued",
    "scouting",
    "pilot",
    "build_ready",
    "building",
    "dataset_draft",
    "dataset_ready",
    "challenge_draft",
    "challenge_checks_passed",
    "agent_runs_started",
    "revision_requested",
    "accepted",
    "rejected",
    "abandoned",
    "blocked",
    "retry_wait",
}
PLATFORM_TO_TASK = {
    "unknown": None,
    "dataset_draft": "dataset_draft",
    "dataset_checking": "dataset_draft",
    "dataset_needs_revision": "revision_requested",
    "dataset_ready": "dataset_ready",
    "challenge_draft": "challenge_draft",
    "challenge_checking": "challenge_draft",
    "challenge_needs_revision": "revision_requested",
    "challenge_checks_passed": "challenge_checks_passed",
    "run_agents_available": "challenge_checks_passed",
    "agent_runs_started": "agent_runs_started",
    "accepted": "accepted",
    "rejected": "rejected",
}

ALLOWED_TRANSITIONS = {
    "queued": {"scouting", "blocked", "retry_wait", "rejected", "abandoned"},
    "scouting": {"pilot", "build_ready", "blocked", "retry_wait", "rejected", "abandoned"},
    "pilot": {"scouting", "build_ready", "blocked", "retry_wait", "rejected", "abandoned"},
    "build_ready": {"building", "blocked", "retry_wait", "rejected", "abandoned"},
    "building": {"dataset_draft", "revision_requested", "blocked", "retry_wait", "rejected", "abandoned"},
    "dataset_draft": {"dataset_ready", "revision_requested", "blocked", "retry_wait", "rejected", "abandoned"},
    "dataset_ready": {"challenge_draft", "revision_requested", "blocked", "retry_wait", "rejected", "abandoned"},
    "challenge_draft": {"challenge_checks_passed", "revision_requested", "blocked", "retry_wait", "rejected", "abandoned"},
    "challenge_checks_passed": {"agent_runs_started", "revision_requested", "blocked", "retry_wait", "rejected", "abandoned"},
    "agent_runs_started": {"accepted", "revision_requested", "blocked", "retry_wait", "rejected"},
    "revision_requested": {
        "building",
        "dataset_draft",
        "dataset_ready",
        "challenge_draft",
        "challenge_checks_passed",
        "blocked",
        "retry_wait",
        "rejected",
        "abandoned",
    },
    "blocked": TASK_STATES - {"queued", "accepted"},
    "retry_wait": TASK_STATES - {"queued", "accepted"},
    "accepted": set(),
    "rejected": set(),
    "abandoned": set(),
}


class FlowError(RuntimeError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def validate_id(value: str, label: str) -> str:
    if not ID_RE.fullmatch(value):
        raise FlowError(f"Invalid {label}: {value!r}. Use lowercase letters, numbers, '_' or '-'.")
    return value


def shipd_id_from_url(value: str, label: str, pattern: re.Pattern[str]) -> str:
    match = pattern.fullmatch(value.strip())
    if not match:
        raise FlowError(f"Invalid Shipd {label} URL: {value!r}")
    return match.group(1).lower()


def ensure_state() -> None:
    BATCH_ROOT.mkdir(parents=True, exist_ok=True)
    TASK_ROOT.mkdir(parents=True, exist_ok=True)
    if not CONTROLLER_PATH.exists():
        write_json(
            CONTROLLER_PATH,
            {"schema_version": 1, "active_batch_id": None, "history": [], "updated_at": now_iso()},
        )


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FlowError(f"Missing state file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise FlowError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise FlowError(f"Expected a JSON object in {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def controller() -> dict[str, Any]:
    ensure_state()
    return read_json(CONTROLLER_PATH)


def batch_path(batch_id: str) -> Path:
    return BATCH_ROOT / f"{validate_id(batch_id, 'batch ID')}.json"


def task_path(task_id: str) -> Path:
    return TASK_ROOT / f"{validate_id(task_id, 'task ID')}.json"


def load_task(task_id: str) -> dict[str, Any]:
    return read_json(task_path(task_id))


def load_batch(batch_id: str) -> dict[str, Any]:
    return read_json(batch_path(batch_id))


def transition(task: dict[str, Any], new_state: str, note: str | None = None) -> None:
    if new_state not in TASK_STATES:
        raise FlowError(f"Unknown task state: {new_state}")
    current = task["state"]
    if new_state != current and new_state not in ALLOWED_TRANSITIONS[current]:
        raise FlowError(f"Invalid transition: {current} -> {new_state}")
    if new_state == "revision_requested" and current != "revision_requested":
        task["revision_count"] = int(task.get("revision_count", 0)) + 1
    if new_state in {"blocked", "retry_wait"} and current not in {"blocked", "retry_wait"}:
        task["resume_state"] = current
    goal_stage = task.get("goal_stage", "agent_runs_started")
    if new_state in {goal_stage, "agent_runs_started"} and not task.get("goal_achieved_at"):
        task["goal_achieved_at"] = now_iso()
    if new_state != current:
        task.setdefault("state_history", []).append(
            {"from": current, "to": new_state, "at": now_iso(), "note": note}
        )
        task["state"] = new_state
    task["updated_at"] = now_iso()


def active_context() -> tuple[dict[str, Any], dict[str, Any] | None, list[dict[str, Any]]]:
    ctl = controller()
    batch_id = ctl.get("active_batch_id")
    if not batch_id:
        return ctl, None, []
    batch = load_batch(batch_id)
    tasks = [load_task(task_id) for task_id in batch["task_ids"]]
    return ctl, batch, tasks


def cmd_create(args: argparse.Namespace) -> dict[str, Any]:
    if args.count <= 0:
        raise FlowError("Task count must be a positive integer.")
    ctl, active, _ = active_context()
    if active is not None:
        raise FlowError(f"Batch {active['batch_id']} is still active. Run 'ready' after it is terminal.")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    batch_id = validate_id(args.batch_id or f"batch-{stamp}", "batch ID")
    if batch_path(batch_id).exists():
        raise FlowError(f"Batch already exists: {batch_id}")
    created_at = now_iso()
    task_ids = [f"{batch_id}-task-{index:03d}" for index in range(1, args.count + 1)]
    batch = {
        "schema_version": 2,
        "batch_id": batch_id,
        "requested_tasks": args.count,
        "completion_contract": "successful_goal_target",
        "completion_stage": args.completion_stage,
        "authorization": args.authorization,
        "created_at": created_at,
        "updated_at": created_at,
        "task_ids": task_ids,
    }
    for task_id in task_ids:
        task = {
            "schema_version": 2,
            "task_id": task_id,
            "batch_id": batch_id,
            "state": "queued",
            "revision_count": 0,
            "goal_achieved_at": None,
            "goal_stage": args.completion_stage,
            "resume_state": None,
            "candidate_attempts": [],
            "transient_failures": [],
            "registry_key": None,
            "codex_task_id": None,
            "worker_thread_id": None,
            "worker_host_id": None,
            "worker_title": None,
            "worker_bound_at": None,
            "worker_history": [],
            "dataset_id": None,
            "problem_id": None,
            "dataset_url": None,
            "problem_url": None,
            "platform_url": None,
            "observations": [],
            "state_history": [],
            "created_at": created_at,
            "updated_at": created_at,
        }
        write_json(task_path(task_id), task)
    write_json(batch_path(batch_id), batch)
    ctl["active_batch_id"] = batch_id
    ctl["updated_at"] = created_at
    write_json(CONTROLLER_PATH, ctl)
    return {"created": True, "batch_id": batch_id, "requested_tasks": args.count, "task_ids": task_ids}


def status_payload() -> dict[str, Any]:
    _, batch, tasks = active_context()
    if batch is None:
        return {
            "active_batch": None,
            "live_check_performed": False,
            "message": "Controller is ready for a new batch.",
        }
    counts = Counter(task["state"] for task in tasks)
    successful = sum(goal_achieved(task) for task in tasks)
    return {
        "active_batch": batch["batch_id"],
        "requested_tasks": batch["requested_tasks"],
        "completion_contract": batch.get("completion_contract", "legacy_attempt_count"),
        "completion_stage": batch.get("completion_stage", "challenge_checks_passed"),
        "state_counts": dict(sorted(counts.items())),
        "successful_tasks": successful,
        "remaining_to_goal": max(0, int(batch["requested_tasks"]) - successful),
        "goal_complete": successful >= int(batch["requested_tasks"]),
        "revision_total": sum(int(task.get("revision_count", 0)) for task in tasks),
        "live_check_performed": False,
        "tasks": tasks,
        "message": "Local ledger only. Perform a fresh authenticated Shipd inspection for live status.",
    }


def cmd_status(_: argparse.Namespace) -> dict[str, Any]:
    return status_payload()


def cmd_ready(_: argparse.Namespace) -> dict[str, Any]:
    ctl, batch, tasks = active_context()
    if batch is None:
        return {"ready": True, "cleared": False, "message": "No active batch."}
    modern_contract = batch.get("completion_contract") in {
        "run_agents_success_target",
        "successful_goal_target",
    }
    pending = (
        [task for task in tasks if not goal_achieved(task)]
        if modern_contract
        else [task for task in tasks if task["state"] not in LEGACY_TERMINAL_STATES]
    )
    if pending:
        return {
            "ready": False,
            "cleared": False,
            "batch_id": batch["batch_id"],
            "pending": [{"task_id": task["task_id"], "state": task["state"]} for task in pending],
            "message": (
                f"Active work was preserved; every slot must visibly reach its configured completion stage ({batch.get('completion_stage', 'challenge_checks_passed')}) before this batch can clear."
                if modern_contract
                else "Active legacy work was preserved; resolve or terminally close it first."
            ),
        }
    cleared_at = now_iso()
    ctl.setdefault("history", []).append(
        {
            "batch_id": batch["batch_id"],
            "requested_tasks": batch["requested_tasks"],
            "cleared_at": cleared_at,
            "final_counts": dict(Counter(task["state"] for task in tasks)),
        }
    )
    ctl["active_batch_id"] = None
    ctl["updated_at"] = cleared_at
    write_json(CONTROLLER_PATH, ctl)
    return {
        "ready": True,
        "cleared": True,
        "batch_id": batch["batch_id"],
        "message": (
            "Successful batch pointer archived. Evidence and task files were preserved."
            if modern_contract
            else "Legacy batch pointer archived under its original completion contract. Evidence and task files were preserved."
        ),
    }


def goal_achieved(task: dict[str, Any]) -> bool:
    goal_stage = task.get("goal_stage", "agent_runs_started")
    state = task.get("state")
    if state == goal_stage or state in SUCCESS_STATES:
        return True
    # A retryable infrastructure failure after the goal checkpoint does not
    # invalidate the already verified platform state. Revisions and blockers do.
    if state == "retry_wait" and task.get("resume_state") in {goal_stage, "agent_runs_started", "accepted"}:
        return True
    return False


def cmd_replace_candidate(args: argparse.Namespace) -> dict[str, Any]:
    task = load_task(args.task_id)
    if goal_achieved(task):
        raise FlowError("This task already reached its configured completion stage; do not replace its successful candidate.")
    evidence = None
    if args.evidence:
        evidence_path = Path(args.evidence).resolve()
        if not evidence_path.is_file():
            raise FlowError(f"Evidence file does not exist: {evidence_path}")
        evidence = str(evidence_path)
    attempt = {
        "candidate": args.candidate,
        "verdict": args.verdict,
        "reason": args.reason,
        "evidence": evidence,
        "registry_key": task.get("registry_key"),
        "codex_task_id": task.get("codex_task_id"),
        "state_at_replacement": task.get("state"),
        "recorded_at": now_iso(),
    }
    task.setdefault("candidate_attempts", []).append(attempt)
    current = task["state"]
    task.setdefault("state_history", []).append(
        {
            "from": current,
            "to": "scouting",
            "at": now_iso(),
            "note": f"Candidate {args.verdict}; replacement search required: {args.reason}",
        }
    )
    task["state"] = "scouting"
    task["registry_key"] = None
    task["codex_task_id"] = None
    task["resume_state"] = None
    task["updated_at"] = now_iso()
    write_json(task_path(args.task_id), task)
    return {
        "replacement_required": True,
        "task_id": args.task_id,
        "state": task["state"],
        "candidate_attempt_count": len(task["candidate_attempts"]),
        "goal_achieved": False,
        "message": "Candidate evidence preserved. Continue scouting this same slot until a candidate reaches Run Agents.",
    }


def cmd_record_transient(args: argparse.Namespace) -> dict[str, Any]:
    task = load_task(args.task_id)
    event = {
        "kind": args.kind,
        "message": args.message,
        "retry_after_seconds": args.retry_after,
        "recorded_at": now_iso(),
    }
    task.setdefault("transient_failures", []).append(event)
    if task["state"] not in {"blocked", "retry_wait"}:
        transition(task, "retry_wait", f"Temporary {args.kind} failure; resume from checkpoint")
    elif not task.get("resume_state"):
        for item in reversed(task.get("state_history", [])):
            if item.get("to") in {"blocked", "retry_wait"} and item.get("from"):
                task["resume_state"] = item["from"]
                break
    task["updated_at"] = now_iso()
    write_json(task_path(args.task_id), task)
    return {
        "recorded": True,
        "task_id": args.task_id,
        "kind": args.kind,
        "state": task["state"],
        "retry_required": True,
        "goal_achieved": goal_achieved(task),
    }


def cmd_resume_incomplete(_: argparse.Namespace) -> dict[str, Any]:
    _, batch, tasks = active_context()
    if batch is None:
        return {"active_batch": None, "resumed": []}
    resumed = []
    for task in tasks:
        if goal_achieved(task):
            continue
        current = task["state"]
        if current in {"blocked", "retry_wait"}:
            target = task.get("resume_state")
            if not target:
                for item in reversed(task.get("state_history", [])):
                    if item.get("to") in {"blocked", "retry_wait"} and item.get("from"):
                        target = item["from"]
                        break
            target = target or "scouting"
        elif current in {"rejected", "abandoned"}:
            task.setdefault("candidate_attempts", []).append(
                {
                    "candidate": task.get("registry_key") or "legacy candidate",
                    "verdict": current,
                    "reason": "Migrated incomplete slot from legacy terminal semantics",
                    "evidence": None,
                    "registry_key": task.get("registry_key"),
                    "codex_task_id": task.get("codex_task_id"),
                    "state_at_replacement": current,
                    "recorded_at": now_iso(),
                }
            )
            task["registry_key"] = None
            task["codex_task_id"] = None
            target = "scouting"
        else:
            continue
        task.setdefault("state_history", []).append(
            {"from": current, "to": target, "at": now_iso(), "note": "Resumed incomplete success slot"}
        )
        task["state"] = target
        task["resume_state"] = None
        task["updated_at"] = now_iso()
        write_json(task_path(task["task_id"]), task)
        resumed.append({"task_id": task["task_id"], "from": current, "to": target})
    return {
        "active_batch": batch["batch_id"],
        "resumed": resumed,
        "message": "Continue all incomplete slots; rejected candidates do not reduce the success target.",
    }


def cmd_upgrade_success_contract(_: argparse.Namespace) -> dict[str, Any]:
    _, batch, tasks = active_context()
    if batch is None:
        raise FlowError("There is no active batch to upgrade.")
    previous = batch.get("completion_contract", "legacy_attempt_count")
    if previous == "run_agents_success_target":
        return {
            "upgraded": False,
            "batch_id": batch["batch_id"],
            "completion_contract": previous,
            "message": "The active batch already uses Run Agents outcome counting.",
        }
    changed_at = now_iso()
    batch["schema_version"] = 2
    batch["completion_contract"] = "run_agents_success_target"
    batch.setdefault("completion_stage", "agent_runs_started")
    batch.setdefault("contract_history", []).append(
        {"from": previous, "to": "run_agents_success_target", "at": changed_at}
    )
    batch["updated_at"] = changed_at
    write_json(batch_path(batch["batch_id"]), batch)
    for task in tasks:
        task["schema_version"] = 2
        task.setdefault("goal_achieved_at", None)
        task.setdefault("goal_stage", batch["completion_stage"])
        task.setdefault("resume_state", None)
        task.setdefault("candidate_attempts", [])
        task.setdefault("transient_failures", [])
        task.setdefault("worker_thread_id", None)
        task.setdefault("worker_host_id", None)
        task.setdefault("worker_title", None)
        task.setdefault("worker_bound_at", None)
        task.setdefault("worker_history", [])
        task["updated_at"] = changed_at
        write_json(task_path(task["task_id"]), task)
    successful = sum(goal_achieved(task) for task in tasks)
    return {
        "upgraded": True,
        "batch_id": batch["batch_id"],
        "completion_contract": batch["completion_contract"],
        "successful_tasks": successful,
        "remaining_to_goal": max(0, int(batch["requested_tasks"]) - successful),
        "message": "This batch now requires one visible Run Agents launch for every requested slot.",
    }


def cmd_set_completion_stage(args: argparse.Namespace) -> dict[str, Any]:
    _, batch, tasks = active_context()
    if batch is None:
        raise FlowError("There is no active batch.")
    changed_at = now_iso()
    batch["completion_stage"] = args.stage
    batch["completion_contract"] = "successful_goal_target"
    batch["updated_at"] = changed_at
    write_json(batch_path(batch["batch_id"]), batch)
    for task in tasks:
        task["goal_stage"] = args.stage
        if not goal_achieved(task):
            task["goal_achieved_at"] = None
        task["updated_at"] = changed_at
        write_json(task_path(task["task_id"]), task)
    successful = sum(goal_achieved(task) for task in tasks)
    return {
        "updated": True,
        "batch_id": batch["batch_id"],
        "completion_contract": batch["completion_contract"],
        "completion_stage": args.stage,
        "successful_tasks": successful,
        "remaining_to_goal": max(0, int(batch["requested_tasks"]) - successful),
    }


def cmd_bind(args: argparse.Namespace) -> dict[str, Any]:
    task = load_task(args.task_id)
    registry_key = validate_id(args.registry_key, "registry key")
    registry_path = REGISTRY_ROOT / f"{registry_key}.json"
    if not registry_path.is_file():
        raise FlowError(f"Registry record does not exist: {registry_path}")
    dataset_id = args.dataset_id
    problem_id = args.problem_id
    if args.dataset_url:
        derived = shipd_id_from_url(args.dataset_url, "dataset", SHIPD_DATASET_URL_RE)
        if dataset_id and dataset_id.lower() != derived:
            raise FlowError("Dataset ID does not match the supplied dataset URL")
        dataset_id = derived
    if args.problem_url:
        derived = shipd_id_from_url(args.problem_url, "problem/challenge", SHIPD_PROBLEM_URL_RE)
        if problem_id and problem_id.lower() != derived:
            raise FlowError("Problem ID does not match the supplied challenge URL")
        problem_id = derived

    task["registry_key"] = registry_key
    if args.codex_task_id:
        task["codex_task_id"] = args.codex_task_id
    if dataset_id:
        task["dataset_id"] = dataset_id
    if problem_id:
        task["problem_id"] = problem_id
    if args.dataset_url:
        task["dataset_url"] = args.dataset_url
    if args.problem_url:
        task["problem_url"] = args.problem_url
        task["platform_url"] = args.problem_url
    if args.url:
        task["platform_url"] = args.url
    task["updated_at"] = now_iso()
    write_json(task_path(args.task_id), task)
    return {
        "bound": True,
        "task_id": args.task_id,
        "registry_key": registry_key,
        "dataset_id": task.get("dataset_id"),
        "problem_id": task.get("problem_id"),
        "dataset_url": task.get("dataset_url"),
        "problem_url": task.get("problem_url"),
    }


def cmd_bind_worker(args: argparse.Namespace) -> dict[str, Any]:
    task = load_task(args.task_id)
    if not args.thread_id.strip():
        raise FlowError("Worker thread ID cannot be empty")
    previous = task.get("worker_thread_id")
    if previous and previous != args.thread_id:
        task.setdefault("worker_history", []).append(
            {
                "thread_id": previous,
                "host_id": task.get("worker_host_id"),
                "title": task.get("worker_title"),
                "bound_at": task.get("worker_bound_at"),
                "replaced_at": now_iso(),
            }
        )
    task["worker_thread_id"] = args.thread_id
    task["worker_host_id"] = args.host_id
    task["worker_title"] = args.title
    task["worker_bound_at"] = now_iso()
    task["updated_at"] = now_iso()
    write_json(task_path(args.task_id), task)
    return {
        "bound": True,
        "task_id": args.task_id,
        "worker_thread_id": task["worker_thread_id"],
        "worker_host_id": task["worker_host_id"],
        "worker_title": task["worker_title"],
    }


def cmd_set_state(args: argparse.Namespace) -> dict[str, Any]:
    task = load_task(args.task_id)
    transition(task, args.state, args.note)
    write_json(task_path(args.task_id), task)
    return {
        "updated": True,
        "task_id": args.task_id,
        "state": task["state"],
        "revision_count": task["revision_count"],
        "goal_achieved": goal_achieved(task),
    }


def cmd_record_live(args: argparse.Namespace) -> dict[str, Any]:
    task = load_task(args.task_id)
    if args.platform_state not in PLATFORM_TO_TASK:
        raise FlowError(f"Unknown platform state: {args.platform_state}")
    evidence = None
    if args.evidence:
        evidence_path = Path(args.evidence).resolve()
        if not evidence_path.is_file():
            raise FlowError(f"Evidence file does not exist: {evidence_path}")
        evidence = str(evidence_path)
    observed_at = args.observed_at or now_iso()
    try:
        datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise FlowError("--observed-at must be an ISO-8601 timestamp") from exc
    observation = {
        "platform_state": args.platform_state,
        "observed_at": observed_at,
        "recorded_at": now_iso(),
        "dataset_id": args.dataset_id or task.get("dataset_id"),
        "problem_id": args.problem_id or task.get("problem_id"),
        "url": args.url or task.get("platform_url"),
        "evidence": evidence,
        "note": args.note,
    }
    if not any([observation["dataset_id"], observation["problem_id"], observation["url"]]):
        raise FlowError("A live observation requires a dataset ID, problem ID, or exact platform URL.")
    task["dataset_id"] = observation["dataset_id"]
    task["problem_id"] = observation["problem_id"]
    task["platform_url"] = observation["url"]
    task.setdefault("observations", []).append(observation)
    mapped_state = PLATFORM_TO_TASK[args.platform_state]
    if mapped_state is not None:
        transition(task, mapped_state, args.note)
    task["updated_at"] = now_iso()
    write_json(task_path(args.task_id), task)
    return {
        "recorded": True,
        "task_id": args.task_id,
        "platform_state": args.platform_state,
        "local_state": task["state"],
        "revision_count": task["revision_count"],
    }


def cmd_status_fix(_: argparse.Namespace) -> dict[str, Any]:
    _, batch, tasks = active_context()
    if batch is None:
        return {"active_batch": None, "repair_queue": [], "fresh_live_check_required": True}
    queue = []
    for task in tasks:
        if not goal_achieved(task):
            queue.append(
                {
                    "task_id": task["task_id"],
                    "state": task["state"],
                    "registry_key": task.get("registry_key"),
                    "latest_observation": (task.get("observations") or [None])[-1],
                    "candidate_attempt_count": len(task.get("candidate_attempts", [])),
                    "action": (
                        "replace_candidate"
                        if task["state"] in {"rejected", "abandoned"}
                        else "retry_from_checkpoint"
                        if task["state"] in {"blocked", "retry_wait"}
                        else "continue"
                    ),
                }
            )
    return {
        "active_batch": batch["batch_id"],
        "repair_queue": queue,
        "fresh_live_check_required": True,
        "message": "Run the authenticated Status workflow before making repairs.",
    }


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--json", action="store_true", dest="as_json", help="Emit JSON only")
    sub = root.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="Create an immutable batch of task slots")
    create.add_argument("count", type=int)
    create.add_argument("--batch-id")
    create.add_argument("--authorization", required=True)
    create.add_argument(
        "--completion-stage",
        choices=["challenge_checks_passed", "agent_runs_started"],
        default="challenge_checks_passed",
    )
    create.set_defaults(handler=cmd_create)

    status = sub.add_parser("status", help="Read the local ledger")
    status.add_argument("--json", action="store_true", dest="as_json")
    status.set_defaults(handler=cmd_status)

    ready = sub.add_parser("ready", help="Safely clear a terminal active batch")
    ready.add_argument("--json", action="store_true", dest="as_json")
    ready.set_defaults(handler=cmd_ready)

    bind = sub.add_parser("bind", help="Bind a slot to exact registry/platform IDs")
    bind.add_argument("task_id")
    bind.add_argument("--registry-key", required=True)
    bind.add_argument("--codex-task-id")
    bind.add_argument("--dataset-id")
    bind.add_argument("--problem-id")
    bind.add_argument("--dataset-url")
    bind.add_argument("--problem-url")
    bind.add_argument("--url")
    bind.set_defaults(handler=cmd_bind)

    worker = sub.add_parser("bind-worker", help="Bind a visible Codex worker task to one immutable slot")
    worker.add_argument("task_id")
    worker.add_argument("--thread-id", required=True)
    worker.add_argument("--host-id")
    worker.add_argument("--title", required=True)
    worker.set_defaults(handler=cmd_bind_worker)

    replace = sub.add_parser("replace-candidate", help="Reject one candidate without rejecting its success slot")
    replace.add_argument("task_id")
    replace.add_argument("--candidate", required=True)
    replace.add_argument("--verdict", choices=["hold", "rejected"], required=True)
    replace.add_argument("--reason", required=True)
    replace.add_argument("--evidence")
    replace.set_defaults(handler=cmd_replace_candidate)

    transient = sub.add_parser("record-transient", help="Record a retryable runtime failure")
    transient.add_argument("task_id")
    transient.add_argument("--kind", choices=["rate_limit", "reconnect", "browser_auth"], required=True)
    transient.add_argument("--message", required=True)
    transient.add_argument("--retry-after", type=float)
    transient.set_defaults(handler=cmd_record_transient)

    resume = sub.add_parser("resume-incomplete", help="Resume legacy rejected or temporarily blocked success slots")
    resume.set_defaults(handler=cmd_resume_incomplete)

    upgrade = sub.add_parser("upgrade-success-contract", help="Migrate the active batch to Run Agents outcome counting")
    upgrade.set_defaults(handler=cmd_upgrade_success_contract)

    completion = sub.add_parser("set-completion-stage", help="Choose stop-before-Run-Agents or launch-through-Run-Agents completion")
    completion.add_argument("--stage", choices=["challenge_checks_passed", "agent_runs_started"], required=True)
    completion.set_defaults(handler=cmd_set_completion_stage)

    state = sub.add_parser("set-state", help="Record a validated local lifecycle transition")
    state.add_argument("task_id")
    state.add_argument("--state", choices=sorted(TASK_STATES), required=True)
    state.add_argument("--note")
    state.set_defaults(handler=cmd_set_state)

    observe = sub.add_parser("record-live", help="Record a fresh authenticated platform observation")
    observe.add_argument("task_id")
    observe.add_argument("--platform-state", choices=sorted(PLATFORM_TO_TASK), required=True)
    observe.add_argument("--observed-at")
    observe.add_argument("--dataset-id")
    observe.add_argument("--problem-id")
    observe.add_argument("--url")
    observe.add_argument("--evidence")
    observe.add_argument("--note")
    observe.set_defaults(handler=cmd_record_live)

    fix = sub.add_parser("status-fix", help="List recorded revision/blocker work")
    fix.add_argument("--json", action="store_true", dest="as_json")
    fix.set_defaults(handler=cmd_status_fix)
    return root


def render(payload: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main() -> int:
    args = parser().parse_args()
    try:
        payload = args.handler(args)
        render(payload, args.as_json)
        if args.command == "ready" and not payload.get("ready", False):
            return 2
        return 0
    except FlowError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

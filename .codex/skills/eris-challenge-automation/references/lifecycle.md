# Batch Lifecycle

## Layers

1. **Controller:** local batch/task ledger under `eris_automation/State`.
2. **Registry:** the authoritative per-challenge evidence and ownership record under `challenge_registry`.
3. **Package:** the verified local challenge folder containing source material, preparation/grading code, forms, and audit evidence.
4. **Platform:** fresh authenticated Shipd dataset, problem, checks, agents, and reviewer state.

Never collapse these layers into one status claim.

## Task States

- `queued`: batch slot exists.
- `scouting`: dataset/idea discovery and evidence collection.
- `pilot`: bounded viability work; not a build-ready challenge.
- `build_ready`: the registry readiness verdict is `Proceed`.
- `building`: canonical package construction and local audits.
- `dataset_draft`: bound live dataset exists but is not ready.
- `dataset_ready`: dataset checks are green and Mark as Ready is confirmed.
- `challenge_draft`: challenge form exists but required checks are not all green.
- `challenge_checks_passed`: all required red/yellow findings are resolved and Run Agents is available.
- `agent_runs_started`: Run Agents was confirmed and the submission workflow stopped.
- `revision_requested`: platform/reviewer revision requires work on the same task.
- `accepted`: a post-launch accepted outcome.
- `rejected`, `abandoned`: legacy closure states only. Before Run Agents they do not satisfy the slot and must be resumed/replaced unless the user explicitly cancels the batch.
- `blocked`: a reversible external or implementation blocker with an evidence note.

## Counting

`requested_tasks` is the immutable success target. Task IDs and supplied Shipd pairs are immutable. Dataset ideas are candidate attempts inside a task. A task succeeds at its configured `goal_stage`: `challenge_checks_passed` by default, or `agent_runs_started` only when launch was explicitly requested. When an idea fails a gate, preserve it in `candidate_attempts`, keep the same task ID/pair, and continue searching. The batch is complete only when `successful_tasks == requested_tasks`.

## Evidence Rules

- Store exact registry key and Codex task ID after handoff.
- Store exact dataset ID, problem ID, and platform URL after draft creation.
- Timestamp each live observation.
- Attach a durable evidence file when practical; otherwise record a concise factual note and URL.
- Local status always says `live_check_performed: false`. Only a just-completed browser inspection may be described as fresh live status.
- Do not overwrite historical observations; the task record keeps an observation list.

## Recovery

If automation stops mid-run, read controller, batch, task, registry, package checkpoint, and fresh platform state before continuing. Resume the same task ID. Do not recreate already completed platform objects or count recovery as a new task.

Run `resume-incomplete` after upgrading a legacy batch or after a temporary browser block. It revives unsuccessful legacy rejected slots for replacement search and returns browser-blocked slots to their saved checkpoint stage.

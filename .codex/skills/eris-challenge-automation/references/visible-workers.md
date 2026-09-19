# Visible Worker Orchestration

Use one persistent, user-visible Codex task per immutable success slot. These are not hidden subagents. The coordinator owns batch counting and supervision; each worker owns only its slot, fixed Shipd dataset/problem pair, local package/checkpoint, and in-app browser tabs.

## Create and bind workers

1. List existing Codex tasks first and reuse a worker already bound to the exact slot when it is healthy. Never create duplicates blindly.
2. Create a separate local Codex task for every unbound slot. Prefer the portable Eris project when it resolves to the bot root. Otherwise create a lightweight projectless task whose self-contained prompt names `E:\Eris Challenge Bot` as the authoritative root; all durable files still go under that root.
3. Give the worker its controller task ID, exact dataset URL, exact challenge/problem URL, current state/checkpoint, registry/package when present, and candidate-attempt history. Do not send the full five-task conversation.
4. Bind the returned task/thread ID using `eris_automation/run.ps1 bind-worker <task-id> --thread-id <id> --host-id <host> --title <title>`.
5. If a worker must be replaced, preserve the former ID in `worker_history` and bind the replacement. Never lose the slot or Shipd pair.

## Mandatory browser bootstrap inside each worker

The user explicitly requires the Codex in-app browser. Each worker must load the installed in-app Browser skill, explicitly select `iab`, read its complete browser documentation, set browser visibility to true, and create/reuse two tabs:

- dataset tab: exact fixed Shipd dataset URL;
- challenge tab: exact fixed Shipd problem/challenge URL.

Verify the displayed IDs/URLs and authenticated editor state. Mark both tabs for handoff on every turn so they survive and remain visible when the user opens that worker task. Never substitute Chrome, Edge, an extension profile, web search, or raw HTTP for authenticated platform editing. Read the browser's file-upload documentation before the first upload.

## Worker execution

- A `scouting` worker searches and pilots replacements until one reaches `Proceed`, then builds it and uses the same fixed Shipd pair.
- A `retry_wait` worker resumes the saved phase after checking the visible in-app browser; do not redo completed local work.
- A dataset/challenge worker completes the bundled submission-pool workflow and resolves every yellow/red finding substantively.
- Default completion is `challenge_checks_passed`: all checks green and Run Agents visibly available, without clicking it. Use `agent_runs_started` only when the current invocation explicitly requests launch.
- Every worker writes checkpoint/state updates before ending a turn or waiting on an external service.

Workers do not ask the user ordinary permission questions. For an always-confirm browser action such as cloud-file deletion, record the exact imminent action and notify the supervisor. The supervisor groups compatible pending deletions into one action-time question and relays the user's answer to each worker. Never mislabel ordinary draft edits as requiring confirmation.

## Coordinator supervision

Use Codex task wait/status tools to follow workers; avoid repeatedly loading full histories. If a worker returns final text before its configured goal stage, send it a checkpoint-based follow-up and keep the slot active. If a worker rate-limits or disconnects, allow recovery; if it remains stopped, continue it or create a fresh visible replacement worker bound to the same slot.

Stagger heavy workers under TPM pressure. Keep other independent workers progressing. The coordinator may report progress, but must not finish the batch or call `Ready` until the controller reports `successful_tasks == requested_tasks`.

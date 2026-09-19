# Dedicated Task Handoff

Create a separate Codex task only after the user explicitly approves an idea and asks for a new task.

## Before Creating The Task

1. Sync the shared workspace and scan output folders.
2. Confirm no equivalent challenge or active claim exists.
3. Create a status record with `scripts/new_challenge_status.ps1` using status `claimed`.
4. Use the exact challenge title for both task title and output folder.

## Task Creation

Use the Codex thread tools when available:

1. List projects.
2. Choose the project containing the synchronized live rules.
3. Create a local project task unless the user asks for a worktree.
4. Set the task title exactly.
5. Send a self-contained build prompt using [build-task-template.md](build-task-template.md). The handoff bundle also contains an editable human-facing copy under `templates\BUILD_TASK_START.md`.

The task prompt must include:

- exact title and output folder;
- plain-language task and concrete input/output;
- official source URL, version, license claim, and known caveats;
- source-size and raw-package rules;
- current CPU/RAM/runtime/novelty constraints;
- closest benchmark and novelty risk;
- mandatory pilot and rejection gates;
- split, leakage, source-fingerprinting, and metadata rules;
- strict grader requirements;
- live rule/checkpoint/review/example paths;
- data acquisition and handover requirements;
- instruction to stop honestly when a mandatory gate fails.

Do not tell a child task merely to "follow the usual template." New tasks may not possess this conversation's context.

## After Creation

Record the returned task ID in the challenge status JSON. Do not continue building the same challenge in the idea task. The idea task may continue scouting other ideas while the child task owns implementation.

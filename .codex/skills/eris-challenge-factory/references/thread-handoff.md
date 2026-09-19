# Dedicated Task Handoff

Create a separate Codex task only after the user explicitly approves an idea and asks for a new task.

Exception for the Eris automation's explicit `Create X Task(s)` outcome contract: the coordinator may create X visible slot workers at batch start. Such a worker is a Scout/Pilot worker, not a claimed full Build task. It may own multiple rejected candidate attempts sequentially, but it must not create a full challenge package, claim a registry entry, or enter Build until one candidate passes `Proceed`.

## Before Creating The Task

1. Sync the shared workspace and scan output folders.
2. Confirm no equivalent challenge or active claim exists.
3. Read the Scout source-to-target evidence card. Create a build task only when its verdict is **Proceed** and label provenance, access, post-filter scale, raw size, lookup resistance, and a simple baseline are measured. The card must be saved in `challenge_registry` and include exact measured counts, independent split-family counts, official file URLs/bytes, license evidence, representative native label rows, and baseline results.
4. Require a `readiness` object and run `scripts/validate_handoff_readiness.ps1 -StatusFile <registry-json>`. Do not create a full build task unless it exits successfully.
5. Read the reviewer premortem. Confirm that the source's canonical task, platform semantic duplicate cluster, modality ablations, no-op score, capable domain attack, import route, and hidden split groups have all been tested rather than deferred.
6. If the verdict is **Pilot** or **Hold**, do not create a full challenge folder or claim it as a build. Create a clearly titled bounded pilot task only when the user explicitly asks to run that pilot.
7. Create a status record with `scripts/new_challenge_status.ps1` using status `claimed`.
8. Use the exact challenge title for both task title and output folder.

Do not create a full build task whose prompt asks the child to discover whether the source has enough usable examples. Measure that in Scout mode first. A proposed threshold such as "find 60 sites" is not evidence that 60 sites exist.

Likewise, do not create a full build task whose prompt leaves a stronger lookup attack, exact label audit, source import test, semantic duplicate decision, or capability-matched baseline as a pass/fail gate. Reproducing measured evidence is build work; discovering whether the challenge is viable is pilot work.

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

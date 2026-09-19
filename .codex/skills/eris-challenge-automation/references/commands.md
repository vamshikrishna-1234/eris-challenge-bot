# Command Contract

## Ready

Purpose: safely prepare the controller for a new batch.

1. Run `eris_automation/run.ps1 ready`.
2. If no batch is active, report ready.
3. If the active batch contains queued, working, blocked, or revision-requested tasks, do not clear it. Report those tasks and their next action.
4. If every task is terminal, archive only the active pointer into controller history. Keep all task, batch, registry, package, and evidence files.

`Ready` never changes Shipd and never means that an accepted or submitted challenge was deleted.

## Status

Purpose: give a fresh, read-only report.

1. Read `status --json` to discover the active tasks and exact dataset/problem bindings.
2. Open the authenticated Shipd pages for every bound active task.
3. Inspect dataset readiness, validation findings, challenge checks, Run Agents state, agent-run state, and reviewer/revision messages as applicable.
4. Save a timestamped observation with `record-live`, including the exact platform state, IDs, URL, and an evidence path or concise note.
5. Run `status --json` again and report:
   - live state and observed-at timestamp;
   - local lifecycle state;
   - passed, yellow, and red findings;
   - whether user action or action-time confirmation is required.

If a page cannot be checked, say `live status unavailable`. Never substitute the local ledger.

## Status & Fix

Purpose: inspect and substantively repair revisions or warnings.

1. Perform the complete `Status` procedure first.
2. Generate the local queue with `status-fix --json`.
3. For build/reviewer changes, use `eris-challenge-factory` revision mode and update the canonical package plus synchronized paste files.
4. For dataset or challenge form/check failures on a verified draft pair, use `eris-submission-pool`.
5. Diagnose each yellow or red result, change the underlying data/code/form configuration, rerun relevant local checks, upload/paste the synchronized artifact, then rerun the platform check.
6. Repeat until all required checks are green or a genuine external blocker is documented.
7. Do not launch agents unless the user gives the action-time confirmation required by the submission skill.

## Create X Task(s)

Purpose: create and pursue exactly `X` distinct Eris challenge slots.

1. Validate `X` is a positive integer. Run `create X` once; do not start a second active batch.
2. Create exactly X visible Codex worker tasks using [visible-workers.md](visible-workers.md), bind each worker thread ID to its slot, and give it only its fixed Shipd pair and slot-specific checkpoint. Do not use hidden subagents as the primary workers.
3. In each worker, explicitly select the in-app browser, make it visible, open the exact dataset and challenge links in separate persistent tabs, and verify their IDs before work.
4. For each slot, execute the factory Scout workflow and bounded pilots. Use user suggestions first, then search independently and broaden sources/domains as needed.
5. `X` is the required number of successful agent launches, not the number of dataset attempts. Revisions, retries, rejected candidates, renamed versions, and reviewer cycles never increase or satisfy the requested count.
6. Only a measured `Proceed` candidate may enter full Build and bind a registry package.
7. Run the complete factory Build and final-audit workflow.
8. Bind exact dataset/problem IDs when live drafts exist. Then use the submission-pool workflow.
9. Record every state transition. When a candidate is Hold/Reject, run `replace-candidate` with its evidence, keep the same task ID, visible worker, and Shipd pair, and immediately scout the next candidate.
10. Stop each successful worker at the first confirmed agent launch. The coordinator continues supervising all remaining workers until X/X.

If the same request supplies exactly `X` challenge/dataset link pairs, preserve the supplied order, bind one pair to each immutable slot after it reaches `Proceed`, and execute the Linked Draft Finisher role for every slot.

The command authorizes creation of the requested Codex build tasks for candidates that pass `Proceed`; it does not waive source, license, novelty, leakage, baseline, CPU/runtime, or validation gates.

Do not deliver a final batch-complete report while `remaining_to_goal` is nonzero. A temporary rate limit, reconnect, or authentication failure is not completion; follow [resilience.md](resilience.md), preserve checkpoints, and resume.

## Finish X Linked Tasks

Purpose: populate and finish already-created Shipd dataset/problem drafts using verified local packages.

1. Read [linked-drafts.md](linked-drafts.md).
2. Require exactly one dataset URL and one challenge/problem URL per task. Accept `/problems/` or `/challenges/` challenge URLs. Map pairs in the order supplied unless the user explicitly labels them.
3. Treat existing alphabetic/default titles, empty descriptions, placeholder metadata, and default compute values as disposable. Inspect them for identity only; never ask why a placeholder exists.
4. Bind both URLs and derived IDs to the durable task record. Match each pair uniquely to its verified `Proceed` registry/package before the first website write.
5. Run the complete dataset-to-agent workflow, including genuine repair of every yellow and red result.
6. An invocation that explicitly asks to finish or submit the exact supplied pairs through Run Agents authorizes the in-scope platform edits and a single agent launch per pair. Do not request confirmation after each field or phase.
7. Stop each task immediately after the page visibly confirms its agent run started. Report completed and genuinely blocked pairs separately.

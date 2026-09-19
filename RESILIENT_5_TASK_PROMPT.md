# Resilient Five-Task Prompt

Create 5 Tasks and finish all five autonomously until every check is green and the Run Agents button is visibly available. Do not click Run Agents unless I explicitly say "through Run Agents" in this invocation.

Create one immutable worker assignment per task slot: one visible Codex worker task when running in Codex, or one `eris-slot-worker` project subagent when running in Claude Code. If runtime concurrency is lower than five, run workers in waves without reducing the five-task target.

The number 5 is a success target, not an attempt limit. The batch is complete only after five distinct Shipd challenge drafts pass every dataset and challenge check with no yellow or red result and visibly expose Run Agents. If any proposed dataset or formulation fails a source, license, novelty, scale, truth, leakage, shortcut, metric, stability, or runtime gate, preserve the evidence as a rejected candidate attempt and immediately search for a distinct replacement in the same task slot. Do not count the failed candidate toward the five, do not discard or remap that slot's supplied Shipd pair, and do not weaken any quality gate.

Evaluate my suggested datasets first, then independently search official sources for better replacements or additional candidates as necessary. Continue scouting, piloting, building, and replacing candidates until all five slots have valid `Proceed` packages and all five are check-clean with Run Agents available.

My suggested candidate datasets (suggestions, not mandatory choices):

1. [DATASET NAME AND OFFICIAL URL]
2. [DATASET NAME AND OFFICIAL URL]
3. [DATASET NAME AND OFFICIAL URL]
4. [DATASET NAME AND OFFICIAL URL]
5. [CONTINUE THROUGH ALL SUGGESTIONS]

Shipd draft pairs:

Task 1:
Challenge: [REAL SHIPD CHALLENGE/PROBLEM URL]
Dataset: [REAL SHIPD DATASET URL]

Task 2:
Challenge: [REAL SHIPD CHALLENGE/PROBLEM URL]
Dataset: [REAL SHIPD DATASET URL]

Task 3:
Challenge: [REAL SHIPD CHALLENGE/PROBLEM URL]
Dataset: [REAL SHIPD DATASET URL]

Task 4:
Challenge: [REAL SHIPD CHALLENGE/PROBLEM URL]
Dataset: [REAL SHIPD DATASET URL]

Task 5:
Challenge: [REAL SHIPD CHALLENGE/PROBLEM URL]
Dataset: [REAL SHIPD DATASET URL]

For each pair, replace every default value and placeholder; upload/import verified raw files; rebuild; set title, complete dataset description, file/column documentation, verified license, and canonical source URL; clear every yellow and red dataset check genuinely; Mark as Ready; set measured difficulty and CPU/A10G/H100 compute; populate the final challenge title, description, tags, grading configuration, `grade.py`, and `prepare.py`; run Prepare and inspect outputs; and clear every yellow and red challenge check genuinely. Then verify that Run Agents is available, record the result, and stop that successful slot without clicking it.

The supplied Shipd dataset and challenge URLs identify editable draft records. Within those exact drafts, ordinary title/description/license/source/script edits, replacing placeholder files, uploading files, rebuilding, running validation, Mark as Ready, Prepare, and challenge checks are pre-authorized. Do not ask me for permission before these routine actions. If browser safety requires an action-time confirmation for an irreversible cloud deletion, checkpoint every ready-to-delete target and ask one concise grouped confirmation through the supervisor; do not have five workers ask separately. After confirmation, resume automatically. For future zero-interruption runs, leave draft file slots empty instead of uploading disposable placeholder archives.

Treat TPM/rate-limit errors, reconnects, and temporary browser-control failures as retryable infrastructure events. Checkpoint first, wait the indicated retry interval, reduce concurrency/context if they repeat, and resume the same step. Do not reject a candidate or finish the task because of infrastructure throttling. If Shipd authentication expires, continue all possible local and independent work, retry the session, keep the slot pending, and ask me only for the precise login action if authentication or CAPTCHA truly requires me. Resume automatically afterward.

Do not give a final “finished” response while the controller reports fewer than 5 successful tasks or `remaining_to_goal > 0`. Progress reports must preserve the active batch and state the exact next retry/replacement action. Only an invocation that explicitly says “through Run Agents” changes the completion stage to `agent_runs_started`; otherwise the completion stage is `challenge_checks_passed`.

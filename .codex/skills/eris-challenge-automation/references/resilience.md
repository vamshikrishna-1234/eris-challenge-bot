# Persistent Success and Runtime Recovery

The requested count is an outcome target. For `Create 5 Tasks`, the batch remains active until five distinct challenge slots visibly reach Run Agents. Five attempted datasets, five local packages, or five terminal-looking records are not sufficient.

## Candidate replacement loop

When an idea fails any genuine gate, preserve the candidate name, registry/build task, exact reason, and evidence with `replace-candidate`. Keep the immutable slot and its supplied Shipd dataset/problem pair. Clear only candidate-specific bindings, return the slot to `scouting`, search the user's remaining suggestions, and then search independently across credible official sources. Continue through pilot and `Proceed` again. Do not weaken gates or repair a fundamentally invalid candidate merely to retain it.

Do not impose a small arbitrary attempt limit. Vary domain, modality, target formulation, source family, and search queries rather than repeatedly testing near-duplicates. Deduplicate every new idea against prior attempts, the registry, accepted examples, and platform archive.

## Token/model rate limits

Rate-limit messages such as TPM exhaustion are infrastructure events, not task results. Before retrying, persist the current slot phase, artifact paths, last completed gate, and next action. Record the event with `record-transient --kind rate_limit`. Wait at least the server-provided retry interval, then resume the same action.

If rate limits repeat, stagger task execution, reduce simultaneous model calls, load only the references needed for the current phase, shorten duplicated context, and use one bounded scouting/pilot action at a time. Never mark a dataset or slot rejected because the model service is throttled.

Use separate visible worker tasks to isolate context. The coordinator should dispatch at most two heavy research/build workers simultaneously when TPM pressure is observed; browser-only workers may continue independently. If a worker ends its turn before success, the coordinator sends a concise checkpoint-based follow-up rather than replaying the entire batch prompt.

## Reconnects and browser-control failures

For a reconnect or temporary browser-control error, record `record-transient --kind reconnect`, preserve the checkpoint, refresh/reopen the exact URL, and retry with increasing bounded delays. Continue local work and other independent slots while the browser is unavailable.

If Shipd authentication has genuinely expired, record `record-transient --kind browser_auth`. Do not invent live state or bypass authentication/CAPTCHA. Continue all possible local and independent work, periodically retry the signed-in session, and keep the affected slot pending. If a user login is ultimately required, report one precise action—restore the Shipd session—then `resume-incomplete` and continue automatically. Authentication never turns a candidate or slot into Reject.

Before reporting authentication failure, the worker must have selected the in-app browser explicitly, made it visible, opened both exact URLs, and inspected the resulting page. Do not treat a Chrome extension/API-key failure as evidence that Shipd or the in-app browser is unavailable.

## Reporting and stopping

Status must show `successful_tasks`, `remaining_to_goal`, each slot's current phase, candidate-attempt count, and retryable blockers. Do not write “finished” while `remaining_to_goal > 0`. A progress update may explain a temporary blocker, but the active batch and its recovery checkpoint must remain intact.

Stop normally only when every requested slot has `goal_achieved_at`, or when the user explicitly cancels the unfinished batch. Quality, truth, licensing, and platform controls remain mandatory throughout persistence.

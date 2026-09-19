# Linked Draft Finisher Role

Use this role when the user supplies Shipd dataset and challenge/problem links, including batches of five or more pairs. It is the platform-completion stage of the existing factory workflow, not a shortcut around the factory's evidence gates.

## Input and mapping

- Parse one dataset URL and one challenge/problem URL per task. Accept challenge paths containing either `/problems/` or `/challenges/`.
- Preserve explicit labels; otherwise map pairs by the order in which the user supplied them.
- The pair count must equal the requested task count. Do not silently drop, duplicate, or reuse a link.
- Default titles such as a letter, number, or temporary label are expected placeholders. Replace them with the verified package values without asking why they are present.
- Bind the exact URLs and IDs in the controller. Refresh both pages and verify their IDs before editing.
- Match each pair to exactly one local `Proceed` package and registry record. If the bot is also creating the tasks, finish the package first, then bind the corresponding pair.
- In the slot's visible Codex worker, explicitly select the Codex in-app browser (`iab`), make it visible to the user, and open the dataset URL and challenge/problem URL in two separate tabs. Mark both tabs for handoff every turn so they remain available. Do not route this workflow through Chrome extension profiles.

## Autonomous execution contract

A current user instruction that supplies the exact pairs and says to create, finish, submit, or work autonomously is direct authorization for ordinary draft actions: edit every form field, upload/import verified source files, rebuild, run validations, Mark as Ready, paste/run canonical scripts, run Prepare and all checks, and apply substantive fixes. Do not pause to reconfirm these actions. Stop with every check green and Run Agents visibly available unless the current invocation explicitly says to launch Run Agents.

Do not ask questions whose answer is already established by the verified package or page, including why a placeholder title is present, whether an empty placeholder should be replaced, which canonical script to use, or whether red/yellow checks should be fixed. Make the evidence-backed choice and continue.

Browser safety may require action-time confirmation for a narrow always-confirm action such as deleting an existing cloud file. A worker must not ask the user directly. Record the exact filename, dataset ID, and reason, then let the supervisor group all currently imminent deletions into one confirmation. After the supervisor relays confirmation, proceed immediately. This exception does not apply to ordinary editing, uploads, rebuilds, validation, Mark as Ready, Prepare, or checks.

Pause only when work cannot safely continue: authentication or CAPTCHA is required; the URL pair is invalid or duplicated; no unique `Proceed` package matches; required source/license rights are unverified; a genuine novelty, truth, leakage, metric, runtime, or evaluator gate fails; the platform requires a user-only action; or the requested link count is inconsistent and cannot be inferred.

## Dataset checklist

1. Replace the placeholder title with the package's final dataset title.
2. Replace the description with the complete dataset-only description, including file overview and every public column's type and meaning.
3. Upload/import every verified raw source asset required by the package, preserving formats such as `.csv`, `.json`, `.fq`, `.zip`, or `.tar.gz`. Never upload prepared answers, private targets, caches, or the whole challenge folder.
4. Wait for transfer completion and verify filenames, sizes, hashes when exposed, and extracted layout.
5. Run Rebuild and inspect the rebuilt files, schema, counts, missingness, duplicates, and representative contents.
6. Set the exact verified license and canonical source URL in their dedicated controls.
7. Run every dataset validation. Record exact red/yellow findings, fix the underlying data or documentation issue, rebuild when affected, and rerun the full suite until it has no red or yellow result.
8. Recheck title, description, files, license, source URL, rebuild, and validations; click Mark as Ready and verify the ready state.

## Challenge checklist

1. Replace every placeholder value with the canonical package value.
2. Choose difficulty from measured baselines and agent headroom.
3. Choose compute from measured dependencies, memory, and runtime: use CPU when the verified workload fits CPU; use A10G only when GPU acceleration is genuinely required; use H100 only when the measured model or memory requirement needs it. Never preserve a default compute choice without testing it.
4. Set the final title, complete participant description, supported tags, grading direction, and exact theoretical minimum/maximum from `grade.py`.
5. Paste the synchronized canonical `grade.py` and `prepare.py`; verify editor contents and hashes.
6. Run Prepare and inspect every public/private output, IDs, schemas, counts, subgroup coverage, missingness, bounds, and leakage properties.
7. Run all challenge checks. Treat yellow and red equally as unfinished. Reproduce each issue, correct its real cause in canonical files/data/forms, rerun affected local tests, synchronize the platform, rerun Prepare when necessary, and rerun the complete platform suite.
8. Continue only when the dataset and challenge are both genuinely zero-warning and local quality gates remain `Proceed`.
9. Default: verify Run Agents is available, record `challenge_checks_passed`, and stop before clicking it. If the current invocation explicitly requests launch, click it exactly once, verify a queued/running/nonzero-round state, record the evidence and timestamp, then stop without monitoring.

## Batch behavior

Work through every pair autonomously. Keep a separate checkpoint and evidence trail for each immutable task. A failed dataset idea triggers replacement research for the same pair; it never discards the pair or satisfies the slot. A runtime failure in one pair must not corrupt, remap, or stop independent progress on the others. Never count a revision or rejected candidate as an extra task. Finish only when every pair reaches its configured goal stage.

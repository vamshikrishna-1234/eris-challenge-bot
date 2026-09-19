# Shipd Dataset-to-Agent-Run Workflow

Use this reference only after the admission gate in `SKILL.md` passes.

## Persistent pool checkpoint

Create `SUBMISSION_POOL_STATE.json` from the bundled template in the matched challenge folder before changing the website. Keep it synchronized with the live pages and registry throughout the run. At minimum it must preserve:

- exact problem and dataset IDs, URLs, versions, titles, and visible draft/ready states;
- the uniquely matched local challenge folder and registry path, plus description hashes so later runs can detect silent draft drift;
- admission verdict, owner match, missing artifacts, unresolved gates, and whether any website write occurred;
- dataset title/description, uploaded or imported source files with names, extensions, sizes and hashes, license, source URL, rebuild attempts/result, validation rerun count, every red/yellow check and its genuine fix, and Mark as Ready state;
- challenge difficulty, compute tier, title, description, tags, grading direction/bounds, script hashes, Run Prepare outputs/rerun count, check rerun count, and every red/yellow check and its genuine fix;
- the single Run Agents click, authoritative queued/running state, timestamp, and terminal stop reason.

Write a blocked checkpoint even when admission fails. Never use a checkpoint to override a failed readiness gate.

## 1. Snapshot and reconcile

Read the complete dataset and problem pages before editing. Capture current titles, descriptions, source files, prepared files, license, source URL, difficulty, compute tier, tags, score direction/bounds, scripts, pipeline version, existing checks, warnings, agent rounds, and version status.

Compare every value with the local form-fill files and canonical scripts. The local challenge package is authoritative only when it matches a current `Proceed` registry. Preserve unrelated user edits and do not create a new version unless the requested change actually requires one.

## 2. Dataset phase

Apply the dataset form exactly:

1. Set the proper dataset title.
2. Set a pure dataset description: overview, validator-visible file structure, every column with type and meaning, license, source, and factual notes. Do not mention challenge scoring, grading, or split mechanics.
3. Add only raw official assets, untouched permitted source files, or approved deterministic generator artifacts. The data-files control may receive formats such as `.csv`, `.json`, `.fq`, `.zip`, `.tar.gz`, and other platform-supported corpus formats; preserve the intended filenames and extensions. Prefer verified official direct URL import when practical. Never upload prepared splits, private answers, transformed targets, the challenge folder, caches, or source lookup indexes.
4. Wait for each import/upload to finish and verify every displayed filename, extension, byte size, hash when exposed, and extracted layout. Do not assume an initial row means the storage object exists; exercise the file through the rebuild path.
5. Rebuild the dataset. Inspect the resulting file tree and representative data: columns, types, counts, finite values, duplicates, missingness, and sensitive fields.
6. Select the exact verified license and enter the canonical source URL in their dedicated fields. Do not use a default placeholder license or bury either value only in prose.
7. Run dataset validation. For every warning or failure, preserve its exact text, identify the real source/documentation/data problem, fix it locally and in the draft, rebuild when affected, and rerun all dataset checks.
8. Continue only when the page has no yellow or red findings, the checkpoint records `all_checks_green: true`, and the local source/data checks still pass.
9. Immediately before Mark as Ready, verify title, description, files, license, source URL, rebuild success, and zero-warning checks again. If the current invocation explicitly authorized autonomous completion of the exact linked pair, continue without a redundant confirmation; otherwise follow the active browser tool's confirmation policy. Click Mark as Ready and verify the dataset visibly enters the ready/accepted state required by the linked problem.

If the platform says “ready” while required fields or files are absent, treat the check as a false negative. Do not mark the dataset ready.

## 3. Challenge configuration phase

Return to the exact linked problem and apply the canonical challenge form:

1. Choose Easy/Medium/Hard from measured solver difficulty, not payout preference.
2. Choose CPU, A10G, or H100 from tested dependency, memory, and runtime needs. Do not request a GPU when the challenge is designed for CPU.
3. Set the title in Title Case.
4. Paste the complete participant-visible description. Include the operational objective, public files, train/test column tables, submission schema and constraints, evaluation metric and direction, runtime/dependency contract, and What Not To Use. Exclude hidden split details, private weights, source fingerprints, answer-bearing transforms, and lookup-sensitive breadcrumbs.
5. Choose only tags supported by the actual modalities and learning problem.
6. Set grade direction and exact theoretical min/max to the real range of `grade.py`.
7. Paste canonical `grade.py` and `prepare.py` from synchronized local paste files. Verify the editor content rather than assuming paste succeeded.
8. Run Prepare. Inspect public train/test/sample files and private answers, row counts, ID equality, columns/order, paths, subgroup sizes, missingness, finite/range constraints, opacity, and absence of leakage.

If any live value differs from the local verified package, reconcile and rerun all affected local tests before continuing.

## 4. Challenge checks and genuine repair loop

Open Checks & evaluation and run pre-submission checks. Treat red and yellow equally as unfinished work.

For each finding:

1. Save the exact message and the challenge version.
2. Reproduce or inspect the underlying issue using real prepared artifacts.
3. Fix the substantive source, schema, script, description, split, metric, dependency, runtime, novelty, or leakage problem.
4. Synchronize canonical files and paste copies.
5. Rerun affected local smoke, baseline, lookup, malformed-submission, perfect-score, sample-score, and runtime tests.
6. Rebuild or rerun Prepare if inputs or preparation changed.
7. Rerun the complete platform check suite, not just one check.

Do not continue when a warning is waived only because the UI permits it. If novelty is below the platform threshold, a capable solver exceeds the intended headroom, public retrieval recovers answers, native truth is missing, groups are unstable, or a grader contract cannot be made honest, return to Scout/Build and mark Hold/Reject as appropriate.

## 5. Stop ready, or Run Agents when explicitly requested

When dataset readiness, preparation, local audits, and every platform check are clean, with `all_checks_green: true` recorded for both phases:

1. Verify the current version and that no autosave/rebuild/check operation is pending.
2. If the current invocation does not explicitly request agent launch, record `challenge_checks_passed`, verify Run Agents is enabled, and stop without clicking it.
3. If launch is explicitly requested, click Run Agents exactly once without an extra ordinary-permission question, subject only to any confirmation the active browser tool itself mandates.
4. Refresh the page and verify a queued/running state, nonzero round count, or equivalent authoritative confirmation.
5. Record the timestamp, problem/dataset IDs, version, and visible run state; set registry `stage` to `agent_runs_started` without inventing a new status.
6. Set the pool checkpoint stop reason to `agent_runs_started_stop_without_monitoring`.
7. Stop. Do not poll, submit further versions, or attempt to influence the agents unless the user separately requests monitoring or revision.

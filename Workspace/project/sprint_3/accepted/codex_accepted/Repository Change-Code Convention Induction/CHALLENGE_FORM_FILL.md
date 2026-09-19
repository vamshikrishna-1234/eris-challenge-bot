# Challenge creation form - fill-in

## Difficulty

Hard

## Challenge Title

Repository Release Policy Record Induction From Code Diffs

## Problem Description

# Repository Release Policy Record Induction From Code Diffs

## Overview

In plain language, the objective is to read real Python commit diffs and same-repository calibration examples, then produce a compact release-policy record for each held-out diff.

Large software organizations often convert merged diffs into release-policy records that drive gating, rollback handling, reviewer routing, and mandatory follow-up work. In this code/NLP challenge, the code-change text comes from real permissively licensed Python repositories, while the private release policy is derived during preparation: each repository has its own opaque convention that must be inferred from same-repo examples.

Each row is a repository-onboarding packet: a compact `repo_profile`, 3 to 6 annotated `repo_context_examples` from non-scored support commits in the same repository, and one target commit diff. The output is a structured release-policy record for that target diff. The same broad edit type can map to different `T_..` codes and policy fields across repositories and release lanes, so solvers must infer local convention from examples plus code semantics. The task is designed to be solvable on CPU within 1.5 hours using retrieval, traditional NLP/code features, lightweight local models, or small CPU-friendly ensembles.

The raw code diffs are real upstream commits sampled from MIT, BSD-3-Clause, and Apache-2.0 repositories. Public rows do not expose repo names, URLs, commit SHAs, raw repo ids, private family ids, or split markers. The calibration examples are intended input, not leakage: they come from separate support rows and are never answers for another scored `test.csv` target.

Within a repository, visible code subtypes matter. For example, a dependency workflow change, a public API signature change, a validation error change, a typing-only compatibility edit, and a security/auth-related edit can trigger different private policies under different release lanes. Strong solutions should learn the repo-local mapping from the support examples rather than relying on a single global keyword table.

What not to use: GPU-only training or inference pipelines, zero-shot/few-shot prompting without learning from the public training split, regex/keyword-only systems, public repository lookup, commit matching, row-order/id/metadata tricks, hardcoded hidden rule tables, manual hidden-test annotation, hosted closed-source APIs, and grader/filesystem exploitation are prohibited. The intended route is CPU-feasible code/NLP policy-record induction from the public training rows and same-repo support examples.

### Task Specification

For each target row, produce a five-field release-policy record:

1. `change_code`: one opaque house code from `T_01` through `T_11`.
2. `behavior_changing`: one of `yes`, `no`, or `abstain`.
3. `rollback_safe`: one of `yes`, `no`, or `abstain`.
4. `required_followup`: one of `none`, `add_test`, `add_migration_note`, `security_review`, `perf_review`, `config_review`, or `owner_review`.
5. `confidence`: a finite float in `[0, 1]` estimating the probability that all four policy fields are correct.

`abstain` is a real target value only for rows where the public diff and same-repo support examples do not reveal enough policy state to make a yes/no decision. It is not a generic fallback for uncertainty.

## Evaluation

Each submitted row provides four policy fields and a confidence value. The confidence is interpreted as the submitted probability that the whole four-field decision bundle is correct.

```
S_code     = 1 if change_code matches, else 0
S_behavior = 1 if behavior_changing matches, else 0
S_rollback = 1 if rollback_safe matches, else 0
S_followup = 1 if required_followup matches, else 0
S_bundle   = 1 if all four heads match, else 0

correctness = 0.40*S_code + 0.08*S_behavior + 0.08*S_rollback + 0.08*S_followup + 0.36*S_bundle
calibration = 1 - abs(confidence - S_bundle)
row_score   = 0.92*correctness + 0.08*calibration
```

The final score blends mean row performance with worst hidden-subgroup performance:

```
Final = 0.70 * mean(row_score)
      + 0.10 * worst_difficulty_bucket(row_score)
      + 0.10 * worst_repo_policy_group(row_score)
      + 0.10 * worst_semantic_group(row_score)
```

The hidden subgroup fields are private evaluation metadata and are not columns in `train.csv` or `test.csv`. Higher is better. Theoretical minimum: `0.0`. Theoretical maximum: `1.0`.

The grader returns `0.0` if the submission columns are missing, extra, or reordered; if any `row_id` is duplicated; if the submitted row set differs from the test row set; if any submitted value is outside the allowed vocabulary; or if any confidence is missing, non-finite, or outside `[0, 1]`.

### Intended Solution

Strong CPU-only solutions should build compact code/NLP features from the target diff, repository profile, and same-repo support examples, then train calibrated lightweight models such as regularized linear models, nearest-neighbor retrieval over code-change features, tree ensembles, small CPU-friendly transformer embeddings, or hybrid calibration-rule systems learned from `train.csv`. The public split is intentionally small enough for 10 CPU cores and 62 GB RAM within a 1.5 hour solution limit.

### Enforcement On Invalid Approaches

Submissions based on GPU-dependent pipelines, public repository lookup, commit SHA reconstruction, matching target diffs against GitHub, hosted closed-source APIs, prompt-only inference, regex-only rules, metadata/order/id side channels, hardcoded answer maps, manual hidden-test annotation, or grader/filesystem exploitation may be rejected before payout even if the CSV is structurally valid. The competition rewards learned repo-convention induction over real code-change text.

## Dataset

The dataset ships as CSV files under `public/`. The raw corpus is built from real compact commit diffs sampled from permissively licensed Python projects, then anonymized; private release-policy records are derived during preparation.

### File overview

The `public/` directory contains three CSV files: `train.csv` has target diffs with observed release-policy records and same-repo support calibration examples, `test.csv` has target diffs with same-repo support calibration examples but no target records, and `sample_submission.csv` is a weak train-prior submission template.

| Item | Description |
|---|---|
| `train.csv` | Inputs plus outputs |
| `test.csv` | Inputs only |
| `sample_submission.csv` | Submission template |

### train.csv columns

`train.csv` contains one row per observed target commit diff. `repo_context_examples` is a JSON string containing annotated support examples from the same repository; each example includes summary, files, diff text, and the four policy fields. `target_diff` is a JSON object with summary, changed files, and compact unified-diff text.

| Column | Type | Description |
|---|---|---|
| `row_id` | int | Public row id |
| `repo_profile` | string | Compact repo notes |
| `repo_context_examples` | JSON string | Annotated repo examples |
| `target_diff` | JSON string | Target commit diff |
| `change_code` | string | Opaque policy code |
| `behavior_changing` | string | yes/no/abstain |
| `rollback_safe` | string | yes/no/abstain |
| `required_followup` | string | Follow-up action |

Allowed `change_code` values are `T_01` through `T_11`. Allowed `behavior_changing` and `rollback_safe` values are `yes`, `no`, and `abstain`. Allowed `required_followup` values are `none`, `add_test`, `add_migration_note`, `security_review`, `perf_review`, `config_review`, and `owner_review`.

Plain column definitions: `row_id` is the salted public row identifier; `repo_profile` is visible repository context; `repo_context_examples` is the JSON support calibration set from the same repository; `target_diff` is the target real commit diff; the four output columns are train-only policy fields.

### test.csv columns

`test.csv` has the same public input columns as `train.csv` and omits the four target policy fields. Each row includes annotated support calibration examples from the same repository as the target diff; these support examples are not other scored test targets.

| Column | Type | Description |
|---|---|---|
| `row_id` | int | Public row id |
| `repo_profile` | string | Compact repo notes |
| `repo_context_examples` | JSON string | Annotated repo examples |
| `target_diff` | JSON string | Target commit diff |

The public row ids are salted hash-derived integers. They do not encode raw repository id, family, source project, template, split, or row order.

Plain test column definitions: `row_id` is the public identifier to use in the submission; `repo_profile` is compact visible repo context; `repo_context_examples` is the public same-repo annotated support JSON; `target_diff` is the JSON object containing the target summary, files, and diff text.

## Submission

Submit a CSV with a header row and exactly one row per `row_id` in `test.csv`, with these six columns in this exact order: `row_id`, `change_code`, `behavior_changing`, `rollback_safe`, `required_followup`, `confidence`.

| Column | Type | Constraint |
|---|---|---|
| `row_id` | int | Same set as test |
| `change_code` | string | `T_01` to `T_11` |
| `behavior_changing` | string | yes/no/abstain |
| `rollback_safe` | string | yes/no/abstain |
| `required_followup` | string | Allowed value |
| `confidence` | float | Finite in `[0,1]` |

`confidence` should be calibrated to the probability that all four policy fields are correct for that row.

**Example of a correctly formatted submission file:**

```csv
row_id,change_code,behavior_changing,rollback_safe,required_followup,confidence
1042201,T_03,yes,no,add_test,0.71
```

## Tags

code-understanding, nlp, cpu, real-world-data, repository-reasoning, structured-output, fine-tuning

## Grading Configuration

Grade direction: Maximize

Theoretical minimum: `0.0`

Theoretical maximum: `1.0`

## Grading Script

Use `PASTE_THIS_GRADE.txt`.

## Prepare Script

Use `PASTE_THIS_PREPARE.txt`.

## GPU Tier

CPU only: 10 CPU cores, 62 GB RAM, 1.5 hour solution limit.

## What Not To Use

Do not use GPU-only training/inference, public repository lookup, commit matching, hidden rule-table reconstruction, metadata/order/id exploits, manual hidden-test annotation, hosted closed-source APIs, or prompt-only/regex-only solutions.

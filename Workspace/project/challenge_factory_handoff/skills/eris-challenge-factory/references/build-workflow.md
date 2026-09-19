# Build Workflow

## Start

1. Resolve project/output paths and run `scripts/workspace_probe.ps1`.
2. Read the live rules, checkpoints, previous reviews, relevant accepted examples, idea handoff, and challenge status file.
3. Confirm the challenge folder is owned by this machine/task.
4. Re-run the novelty, source/license, source-size, CPU, and lookup-leak gates before implementation.
5. Write `SOURCE_VERIFICATION.md` early. Stop if a mandatory claim cannot be verified.

## Source Acquisition

- Prefer official direct URLs when there are few practical files.
- When many official files are needed, permit a clean source bundle only when it contains untouched official files plus license/provenance. Do not place prepared arrays, train/test splits, transformed media, derived labels, or answer files in the raw bundle.
- Keep source and prepared sizes within current limits.
- Record URLs, versions, checksums, expected names, extraction layout, attribution, and a fallback upload procedure in `DATA_ACQUISITION.md`.
- Inspect actual source files before writing parsers.

## Design

- Make the scored target the real operational object, not a decorative ledger around an ordinary benchmark.
- Ensure every output head adds independent source-grounded information.
- Define unknown/abstention only where source evidence is genuinely insufficient.
- Split by complete source families before creating public IDs.
- Keep hidden subgroup axes physical or semantic, not random hash buckets.
- Put the CPU/runtime contract and complete public task contract inside the platform-visible problem description.

## Implement

Create all files required by the live rules. Normally include:

- canonical `prepare.py` and `grade.py`;
- synchronized `PASTE_THIS_PREPARE.txt` and `PASTE_THIS_GRADE.txt`;
- `CHALLENGE_FORM_FILL.md` and `DATASET_FORM_FILL.md`;
- `SOURCE_VERIFICATION.md` and `DATA_ACQUISITION.md`;
- analysis, smoke, red-team, baseline, and packaging scripts appropriate to the challenge;
- the permitted clean source subset/package when required.

Use deterministic preparation. Assert raw schema, required values, raw-key uniqueness, group separation, ID opacity, path existence, answer/test ID equality, subgroup minimums, and sorted outputs.

## Validate Difficulty And Leakage

Run on the real prepared split:

- sample and train-prior baselines;
- metadata-only and path/order attacks;
- modality-specific source fingerprint/retrieval attack;
- no-model template/copy attack;
- simple hand-feature/parser/DSP baseline;
- intended lightweight CPU baseline;
- one-head mutation tests;
- skill/noise sweep;
- perfect and malformed submissions.

Require natural headroom and stable ranking. Do not hide a weak design behind nonlinear score suppression.

## Validate The Grader

Check exact columns and order, full ID set, duplicates, missing/extra rows, NaN/Inf, numeric bounds, legal enums, JSON size/depth/count limits, malformed JSON, impossible references, negative values, failure return 0, independent-head failure behavior, sample score, and perfect score exactly 1.0.

## Final Audit

Run the challenge-builder audit helper when available, then manually check every live checkpoint. Inspect real prepared artifacts and representative media/signals. Verify raw upload contents and platform-visible extracted layout. Update status to `ready_for_review` only when no required work remains; otherwise use `blocked` with evidence.

## Reviewer Revisions

Append each review to the shared previous-review memory using its required format. Make the substantive fix first, synchronize paste files, rerun affected smoke/baseline/audit checks, and update the challenge status. Never erase unrelated user or other-machine changes.

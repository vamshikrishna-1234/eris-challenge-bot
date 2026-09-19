# Build Task Template

Use the `eris-challenge-factory` skill in Build mode.

Challenge title: `{{CHALLENGE_TITLE}}`

Final output folder: `{{OUTPUT_ROOT}}\{{CHALLENGE_TITLE}}`

Owner machine: `{{OWNER_MACHINE}}`

Registry status file: `{{STATUS_FILE}}`

## Task Contract

Plain-language task:

`{{TASK_SUMMARY}}`

Exact input:

`{{INPUT_CONTRACT}}`

Exact output:

`{{OUTPUT_CONTRACT}}`

## Source

- Official URL: `{{SOURCE_URL}}`
- Version: `{{SOURCE_VERSION}}`
- Claimed license: `{{LICENSE}}`
- Known source size: `{{SOURCE_SIZE}}`

Closest benchmark/local challenge and substantive difference:

`{{NOVELTY_NOTE}}`

Known risks and mandatory pilot/rejection gates:

`{{PILOT_GATES}}`

Measured Scout evidence and reviewer premortem:

`{{READINESS_EVIDENCE}}`

## Required Work

Before implementation, reproduce the measured Scout evidence and fail closed if it does not reproduce. The full-build handoff must already have passed source access, native-label, post-filter scale, split-stability, semantic-duplicate, lookup, capability-matched baseline, no-op metric, and import-route gates. Do not treat missing pre-handoff evidence as ordinary build discovery.

Build the complete challenge end to end under the exact final output folder. Use only permitted source data. Keep raw source and prepared data within current limits. Provide a preferred official URL-import procedure and a clean untouched-source upload fallback when needed. Do not package prepared train/test data as raw source.

Read the configured live rules, checkpoints, previous reviews, accepted examples, idea inventories, registry, and all existing challenge roots. Put current CPU, RAM, runtime, novelty, and prohibited-task constraints inside the platform-visible problem description.

Use natural data/split difficulty. Run metadata, lookup, fingerprinting, parser/hand-feature, simple open-source, intended CPU, skill-sweep, malformed, sample, and perfect baselines. Do not force low scores with arbitrary grade shaping. Require grouped leakage-safe splits and strict malformed-submission handling.

Create all mandatory files, synchronize canonical and PASTE_THIS scripts, materialize permitted source acquisition/package artifacts, run smoke tests and final audits, update the status record, and give the exact data acquisition/upload procedure at handover.

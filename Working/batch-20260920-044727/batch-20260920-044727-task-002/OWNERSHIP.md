# Slot ownership — batch-20260920-044727-task-002

**Single writer: the candidate-4 worker** (dispatched 2026-09-20T11:10Z, pursuing a private
parameterised transformation over a real corpus). It owns every file under this slot folder,
this slot's registry entry, and this slot's controller task.

**The candidate-1-to-3 worker is stood down as of 2026-09-20T12:30Z.** It completed its
replacement search (three measured rejections) and then returned once more to correct an
evidence-integrity error. It will not be resumed and must not write here again. Its final act
was correct and is preserved: see `scout3/ARTIFACT_CORRECTION.md`.

## Why this file exists

The supervisor dispatched the candidate-4 worker while the earlier worker could still be
resumed, so both wrote this slot's shared files in overlapping windows (11:47Z to 12:26Z). That
violated the one-writer-per-slot rule in
`.codex/skills/eris-challenge-automation/references/visible-workers.md`, which makes ownership
slot-based rather than process-based. No data was lost: the earlier worker performed its
correction under explicit guards (asserting target strings present and mtime unchanged before
writing) and confined itself to `CANDIDATE3_REJECTION_EVIDENCE.md` and `scout3/`. Verified
afterwards: `CHECKPOINT.md` and `SCOUT_NOTES.md` kept their successor-written timestamps.

## Standing rule for this batch

One worker per slot at a time. Before dispatching a successor into a slot, the supervisor stands
the predecessor down in writing here and never resumes it. A predecessor with a correction to
make routes it through the supervisor rather than writing shared files directly.

## Correction carried forward (verified by the supervisor)

`scout3/pilot_ceiling.json` never existed: `pilot_ceiling.py` completed its unit-size-600 arm and
printed those results, then its unit-size-1500 arm was killed at timeout (exit 124), so the
closing `json.dump` never ran. The quoted unit-600 numbers are genuine and are preserved with
provenance as `scout3/pilot_ceiling_unit600.json` and `scout3/pilot_ceiling.stdout.log`. The
candidate-3 Reject verdict and every number in its rejection tables stand; `pilot_difficulty`,
`pilot_leakage`, `pilot_harden` and `pilot_rescue` all completed and wrote their JSON.

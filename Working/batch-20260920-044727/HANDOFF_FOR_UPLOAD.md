# Upload handoff — batch-20260920-044727

Three complete local packages, one per supplied Shipd pair. Every local gate that can be
measured offline has been measured and passed. Nothing has been written to Shipd: this
container has no authenticated session, so all three slots sit at `retry_wait`.

The controller reads `successful 0 / 3` because success is defined as green checks on the
platform with Run Agents available. That is the only work left.

## The three packages

| Slot | Package folder under `Workspace/output/` | Challenge |
|---|---|---|
| 1 | `groundwater-abstraction-return-reconciliation` | Recover each borehole's actual abstraction ledger and aquifer parameters from nearby water levels and the declared return |
| 2 | `sparse-probe-roundness-conformance-adjudication` | Recover calibrated roundness quantiles, conformance probability and machine signature from sparse probe points |
| 3 | `rail-corridor-incident-and-dispatch-ledger-recovery` | Recover the incident and dispatch ledger from planned versus realized stop times |

Pair bindings are in `pairs.json` and in each slot's controller task. They are immutable:
slot 1 uses pair 1, slot 2 pair 2, slot 3 pair 3, in the order supplied.

## Per package, what to upload where

Each folder is self-contained. The dataset page takes `generate.py` and `raw_upload.zip`
(slot 3 ships only the archive). The challenge page takes `PASTE_THIS_PREPARE.txt` and
`PASTE_THIS_GRADE.txt` verbatim. Field values come from `DATASET_FORM_FILL.md` and
`CHALLENGE_FORM_FILL.md`. Licence and source URL are in `SOURCE_VERIFICATION.md`.

All three are difficulty Hard, compute CPU on measured runtime, grading maximize, theoretical
minimum 0.0 and maximum 1.0.

`SUBMISSION_POOL_STATE.json` in each folder carries both exact Shipd IDs and both URLs, with
`website_writes_performed: false`. Update it as you go so a later run can resume.

## Order of work on the platform

1. Open the exact dataset and challenge URLs in separate tabs and verify the IDs before writing.
2. Dataset: replace title and description, upload the files, rebuild, set licence and canonical
   source URL, clear every red and yellow finding genuinely, then Mark as Ready.
3. Challenge: set title, description, tags, difficulty, compute, grading direction and bounds,
   paste both scripts, run Prepare, inspect outputs.
4. Run the full check suite and resolve every finding at its cause.
5. Stop with all checks green and Run Agents visibly available. Do not click it: this batch did
   not request a launch.

## What is not verified, and cannot be here

Live platform novelty and duplicate validation. The Problem Research and Novelty Assessment
reports need an authenticated session, so no package in this batch is platform-verified for
novelty. Slot 1 records this in its readiness object and its validator correctly returns
NOT BUILD READY for that reason alone; slots 2 and 3 omitted the same caveat. Treat a local
build-ready verdict here as "ready to upload and be checked", never as "novelty confirmed".
Local duplicate audits against the archived platform titles and the registry were run and passed
for all three.

## Regenerating what git does not carry

Prepared splits, answers and bulk raw data are excluded deliberately. `prepare.py` regenerates
them deterministically, and each run was verified byte-identical on a second pass. Official
source URLs and checksums are in each `DATA_ACQUISITION.md`.

## Record of the search

Nine candidates were measured and rejected or held across the three slots before these three
passed. Each carries an evidence file with numbers. The design rules derived from those failures
are at the end of `WORKER_BRIEF.md` and are what the three survivors were built against.

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

---

# How to run the upload from your own machine

This cloud container cannot reach your `E:` drive and has no signed-in browser. Everything below
runs on your machine, in your local clone of this bot.

## 1. Get the work onto your machine

In your existing local bot folder (the one holding `run-claude.ps1`):

```powershell
git fetch origin claude/wonderful-bohr-b7u814
git checkout claude/wonderful-bohr-b7u814
git pull origin claude/wonderful-bohr-b7u814
```

That brings the three package folders under `Workspace\output\` and, just as important, the
controller ledger under `eris_automation\State\`, so the batch resumes with all three slots
already bound to their exact Shipd pairs.

## 2. Where to work, and a note on `to_be_uploaded`

Work from the bot folder itself. `Workspace\output\` is the authoritative location, and the bot's
own portability rule forbids depending on anything under the old `create_challenge_synthetic`
roots on `C:`, `D:` or `E:`; `validate-portable.ps1` fails the bundle if a core file references
them.

If you want a staging copy at `E:\create_challenge_synthetic_output_folder\sprint_5\to_be_uploaded`
purely for your own convenience while clicking through the site, copy it, do not move it:

```powershell
$dst = "E:\create_challenge_synthetic_output_folder\sprint_5\to_be_uploaded"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item -Recurse -Force `
  "Workspace\output\groundwater-abstraction-return-reconciliation", `
  "Workspace\output\sparse-probe-roundness-conformance-adjudication", `
  "Workspace\output\rail-corridor-incident-and-dispatch-ledger-recovery" `
  -Destination $dst
```

Keep the copies read-only in practice: make every edit in the repo, so the ledger, the registry
and the packages never disagree.

## 3. Start the bot and give it this prompt

```powershell
.\validate-portable.ps1
.\run-claude.ps1
```

Then send, as a single message:

> Status & Fix. Batch batch-20260920-044727 is already active with three bound slots and three
> verified local packages built in a previous cloud session; the ledger under
> eris_automation\State is authoritative. Nothing has been written to Shipd yet.
> For each slot in order, open its exact dataset and challenge URLs in separate tabs in the
> visible Playwright browser and verify the IDs before any write, then run the submission-pool
> workflow from the package in Workspace\output\: upload the listed source files, rebuild, set
> the licence and canonical source URL, clear every red and yellow finding genuinely, Mark as
> Ready, then paste the challenge form values and both PASTE_THIS_*.txt scripts, run Prepare,
> and run the full check suite until everything is green.
> Stop each slot with all checks green and Run Agents visibly available. Do not click Run Agents.
> Update SUBMISSION_POOL_STATE.json and the controller after each phase.

Add `through Run Agents` to that message only if you also want each challenge launched. Without
those words the run stops with the button available and untouched, which is what the original
request asked for.

## 4. Do not start a new project

Use your existing local bot folder. A fresh Claude project or a claude.ai web chat would not have
the repository, the controller ledger, the bundled skills or the Playwright browser, and a second
active batch is exactly what the controller is designed to prevent. A new session inside this same
folder is fine and expected; the ledger carries the state, not the conversation.

## 5. What to upload per package

| Package | Dataset page files | Challenge page scripts |
|---|---|---|
| `groundwater-abstraction-return-reconciliation` | `generate.py`, `raw_upload.zip` | `PASTE_THIS_PREPARE.txt`, `PASTE_THIS_GRADE.txt` |
| `sparse-probe-roundness-conformance-adjudication` | `generate.py`, `raw_upload.zip` | same two files |
| `rail-corridor-incident-and-dispatch-ledger-recovery` | `raw_upload.zip` | same two files |

Field values come from `DATASET_FORM_FILL.md` and `CHALLENGE_FORM_FILL.md` in each folder. All
three are Hard, CPU, maximize, minimum 0.0, maximum 1.0.

## 6. If a check fails

That is expected work, not a defect in the handoff. `Status & Fix` authorises genuine repair:
fix the underlying data, script, form value or documentation, rerun the affected local test, and
rerun the platform suite. Never suppress a check or weaken a grader. The local evidence files in
each package say what was measured and why, which is usually enough to diagnose a finding fast.

# CHECKPOINT — batch-20260920-044727-task-002 (slot 2 of 3)

- Worker label: claude:batch-20260920-044727:batch-20260920-044727-task-002
- Immutable pair: problem jx76g5p2hkwy4bt7etrft14cb18eeh26 / dataset jd7bk5e37hvhjg6q7vrm1z4jnx8efe0a
  (UNCHANGED, never remapped)
- Goal stage: challenge_checks_passed. Run Agents NOT requested, never clicked.
- Shipd: NOT authenticated in this container. **NEVER OPENED this session.** No page load, no draft
  edit, no check run, no Mark as Ready, no Run Agents, no website write of any kind.
- Updated: 2026-09-20T12:50:00+00:00
- Controller state: **retry_wait**, candidate #4 measured **Proceed**, package complete, bound.

## Ownership reconciliation (from the supervisor, 2026-09-20T12:27Z)
This worker is now the sole writer for the slot. The earlier slot-2 worker overlapped between
11:47Z and 12:26Z and is stood down permanently; details in `OWNERSHIP.md`. It touched only
`CANDIDATE3_REJECTION_EVIDENCE.md` and `scout3/`. `CHECKPOINT.md` and `SCOUT_NOTES.md` were not
modified by it. Candidate 3's Reject verdict stands and is not revived.

Correction carried into this file: the line in the previous revision saying a `scout3/pilot_ceiling.py`
process was still running is **withdrawn**. That process exited 124 at its timeout and no
candidate-3 process remains (verified). Candidate 3's ceiling evidence is
`scout3/pilot_ceiling_unit600.json` plus `scout3/pilot_ceiling.stdout.log`; `scout3/pilot_ceiling.json`
never existed because the script's single closing `json.dump` never ran after the later arm was
killed. The generalisable lesson — **write each arm's result as it completes, never only at the end**
— was already applied in this session's harnesses (`scout4/pilot_all.py` and `scout4/pilot_v3.py`
re-dump their results file after every stage via `say()`), which is why the v1 ABC ceiling failure
still left a complete record.

## Phase
Package complete and audited locally. Waiting on an authenticated Shipd browser, which this
container does not have.

## Candidate attempts (all recorded via `replace-candidate`, all with measured evidence)
1. `facade-photo-elevation-drawing-correspondence` (LoC HABS/HAER) — REJECTED.
2. `gmn-meteor-station-view-cone-and-sensitivity` (Global Meteor Network, CC BY 4.0) — REJECTED.
3. `small-area-joint-composition-recovery` (ACS 2023 1-Year PUMS, CC0) — REJECTED.
4. `sparse-probe-roundness-conformance-adjudication` — **PROCEED (measured)**.

## Candidate #4 — measured result
Registry key `sparse-probe-roundness-conformance-adjudication`, bound to the immutable pair in the
controller ledger. Package: `Workspace/output/sparse-probe-roundness-conformance-adjudication/`.

Score ladder with the shipped `grade.py` on the REAL prepared split (35,311 train / 18,643 test rows,
7,854 / 4,146 parts, 585 / 315 disjoint machines):

| Rung | score |
|---|---|
| sample_submission (label priors) | 0.1485 |
| all-zero quantiles | 0.0299 |
| very wide hedging interval | 0.0805 |
| metadata only | 0.2050 |
| 1-NN part-level retrieval over the released train split | 0.3382 |
| copied input (naive sparse peak-to-valley) | 0.3996 |
| capability-matched domain method | 0.5118 |
| learned route (GBM + part pooling) | 0.6976 |
| learned route, pooling ablated | 0.6492 |
| perfect | 1.0000 |

Exact achievable ceiling (latent-oracle conditional, measured on the v3 pilot corpus): 0.8616, i.e.
**ceiling minus capability-matched = +0.367** and ceiling minus a plain GBM = +0.210.
Grader robustness: 20 of 20 checks pass. `prepare.py` verified byte-identical on a rerun.

## Next action
Shipd phase, which needs an authenticated browser this container does not have:
1. open the two exact URLs in separate tabs and verify both IDs before any write;
2. dataset: upload `generate.py` and `raw_upload.zip`, paste `DATASET_FORM_FILL.md`, rebuild, resolve
   every red and yellow finding, Mark as Ready;
3. challenge: paste `CHALLENGE_FORM_FILL.md`, `PASTE_THIS_PREPARE.txt`, `PASTE_THIS_GRADE.txt`,
   difficulty Hard, CPU tier, min 0.0 / max 1.0, higher-is-better, Prepare, run checks to all green;
4. stop with Run Agents visibly available. Do NOT click it — this invocation did not request it.
`SUBMISSION_POOL_STATE.json` is prepared with both IDs, both description hashes and both script
hashes, `website_writes_performed: false`.

## Artifacts
- Package: `Workspace/output/sparse-probe-roundness-conformance-adjudication/` (generate.py,
  zip_raw_for_upload.py, prepare.py, grade.py, _analyze.py, _sanity_smoke.py, CHALLENGE_FORM_FILL.md,
  DATASET_FORM_FILL.md, SOURCE_VERIFICATION.md, PASTE_THIS_*.txt, SUBMISSION_POOL_STATE.json,
  raw_upload.zip, raw_data/, public/, private/, _analyze_results.json)
- Registry: `Workspace/project/challenge_registry/sparse-probe-roundness-conformance-adjudication.json`
  (status ready_for_review, readiness verdict Proceed, validator passes)
- Gates: `scout4/pilot_v3.py` + `pilot_v3_results.json` (definitive), `pilot_v1_results.json`,
  `pilot_extra.py` + `pilot_extra.json`, `pilot_lib.py`, `real_spectrum_fit.json`
- Docs: `SCOUT_NOTES.md`, `PILOT_NOTES_CAND4.md`, `REVIEWER_PREMORTEM_CAND4.md`,
  `DATA_ACQUISITION.md`, `CANDIDATE{1,2,3}_REJECTION_EVIDENCE.md`, `OWNERSHIP.md`
- Disk: slot folder ~95 MB, package ~33 MB. No other slot touched.

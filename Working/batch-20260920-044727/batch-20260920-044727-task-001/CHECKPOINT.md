# CHECKPOINT — batch-20260920-044727-task-001 (slot 1 of 3)

- Worker label: claude:batch-20260920-044727:batch-20260920-044727-task-001
- Immutable pair (never remapped): problem jx7fc5d8gbp3hd9zt4pye0ywgd8efc5e /
  dataset jd71ktmw09xmcbpd8k2rwqc4v18efhft — now BOUND in the controller ledger to registry key
  `groundwater-abstraction-return-reconciliation` (local ledger binding only, no website write).
- Goal stage: challenge_checks_passed. Run Agents NOT requested and NOT clicked.
- Controller state: **retry_wait**, candidate_attempt_count = 4, goal_achieved = false.
- Updated: 2026-09-20T16:45Z
- Shipd: **never opened this run.** The container's Playwright profile has no authenticated Shipd
  session. No page was read, no draft written, no check run, no Mark as Ready, no Run Agents.

## Where the slot stands
Candidate 5 reached a measured **Proceed** and the full local package is built and audited.
The only unresolved gate is live platform novelty/duplicate validation, which needs an
authenticated Shipd session.

## Candidate history (all recorded via replace-candidate with measured evidence)
1. baseball-baserunner-advancement-ledger (Retrosheet) — rejected, saturation (skill 0.713).
2. photo-exposure-decision-ledger (MIRFLICKR-1M) — rejected, 46% dHash source recovery + null skill.
3. half-inning-play-order-reconstruction (Retrosheet) — rejected, ceiling minus capability 0.028.
4. multi-step-reaction-route-recovery (Lowe USPTO, CC0) — rejected, 98.03% full-route recovery by
   public lookup at bundle size 4000 vs chance floor 0.000641. Evidence cand4/pilot/route_attack.json.
5. **Groundwater Abstraction Return Reconciliation — PROCEED.**

## Candidate 5 measured gates (all through the shipped grade.py)
- Prepared split: 1,814 train / 686 test scenes, 8 hidden score groups, 3 signal bands.
- Background families disjoint: 394 real USGS wells feed train scenes, 154 feed test scenes.
- Ladder: oracle 1.0000 | ceiling with true aquifer params 0.6024 | capability-matched alternating
  solver 0.3152 (5.11 s/scene) | shipped sample 0.1451 | weak fixed-param NNLS 0.0301 |
  uniform random 0.0055 | copy-declaration 0.0001 | train-prior 0.0001 | all-zeros 0.0000 |
  empty 0.0000. Ceiling minus capability 0.2872; capability minus best trivial 0.3097.
- Retrieval attack at bundle size: top-1 background source recovery 0.00217 vs 0.00182 chance.
- Grader red-team: id-mismatch 0.0000, NaN scalars 0.0000, duplicate ids 0.1451 (= clean sample),
  malformed JSON / huge-negative ledgers 0.1451 (expected: ledger head 0, valid aquifer columns keep
  their credit).
- prepare.py determinism: second independent run byte-identical on all four outputs.
- raw_upload.zip: flat, 2,503 members, 17.4 MB,
  sha256 c2040ecc948377a101bc1e5fc743f7c228bf5a66fd7bdace99ceafe23bcac15c.
- _sanity_smoke.py: 14/14 pass.

## Next action (needs an authenticated Shipd session)
1. Open the two exact URLs in separate tabs and verify the ids before any write.
2. Dataset tab: upload `generate.py` and `raw_upload.zip`, set licence CC0 1.0 Universal, paste
   DATASET_FORM_FILL.md content, rebuild, resolve every red and yellow finding, Mark as Ready.
3. Challenge tab: paste PASTE_THIS_PREPARE.txt and PASTE_THIS_GRADE.txt, CHALLENGE_FORM_FILL.md
   content, difficulty Hard, compute CPU, theoretical min 0.0 / max 1.0, Prepare, run checks.
4. Stop with every check green and Run Agents visibly available. Do NOT click it.
5. Keep SUBMISSION_POOL_STATE.json updated at each step.

## Blocker
Unauthenticated Shipd browser session (recorded as a transient, not a candidate rejection).

## Disk
Slot total ~1.2 GB: cand5 raw_data 54 MB, raw_upload.zip 17 MB, prepared split, NWIS pulls ~85 MB,
cand4 evidence 18 MB. No archive left resident beyond the upload zip.

## Artifact paths (absolute)
- Package: /home/user/eris-challenge-bot/Workspace/output/groundwater-abstraction-return-reconciliation/
- Registry: /home/user/eris-challenge-bot/Workspace/project/challenge_registry/groundwater-abstraction-return-reconciliation.json
- Pool state: .../groundwater-abstraction-return-reconciliation/SUBMISSION_POOL_STATE.json
- Corpus + split: /home/user/eris-challenge-bot/Working/batch-20260920-044727/batch-20260920-044727-task-001/cand5/{raw_data,public,private,raw_upload.zip}
- Pilot evidence: .../cand5/pilot/ and .../cand4/pilot/

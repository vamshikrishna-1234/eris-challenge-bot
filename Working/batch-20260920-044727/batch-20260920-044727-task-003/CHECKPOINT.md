# CHECKPOINT — batch-20260920-044727-task-003 (slot 3 of 3)

- Worker label: claude:batch-20260920-044727:batch-20260920-044727-task-003
- Immutable pair: problem jx7d7hc2kwrxdxn9r0eg4pjq4h8eebx9 / dataset jd7bgzt14yjrdhr55hvybg8kjn8ef7y5 (NEVER bound; no website write)
- Goal stage: challenge_checks_passed (Run Agents NOT requested, never clicked)
- Updated: 2026-09-20T11:40Z (replacement worker resumed)
- Controller state: scouting
- Shipd: never opened; not authenticated in this container.

## Candidate 1 — wind-turbine-stop-ledger-recovery — VERDICT: HOLD (do not revive)
Public-source reversibility: adaptive retrieval recovered origin window rank-1 for 12.5% of cases
(workspace pass bar ~2.5-3%). Full evidence: LOOKUP_GATE_EVIDENCE.md. Registry entry status=hold.

## Candidate 2 — crss-crash-event-ledger-reconstruction — VERDICT: REJECTED (recorded 2026-09-20T11:05Z)
Measured during scouting BEFORE any build, per the transferable lesson.
NHTSA CRSS 2016-2023, 417,335 crashes, native analyst-coded sequence of events. Source access,
public-domain redistribution, native targets and scale all passed. Public-source reversibility failed:
exact-match attacker over the full public pool identifies the origin crash for 100% (rich repr) down to
8.8% at the design floor (unit counts + unordered event-type multiset only), with 33.7% exact hidden-
ledger recovery by retrieval alone. Pass bar ~2.5-3%. Evidence: LOOKUP_GATE_EVIDENCE_CRSS.md,
pilot_crss/lookup_v1.json, pilot_crss/lookup_v2.json. Bulk CRSS data deleted; hashes kept.

### Transferable rule derived from candidates 1 and 2
A public-source candidate passes the lookup gate only via (1) ephemeral supervision that never persists
publicly, (2) non-joinable supervision (a private construction over real inputs), or (3) a public
representation carrying <= ~log2(N)-5 bits of record-identifying information. Rich per-record evidence
from a fully public corpus can never satisfy (3).

## Candidate 3 — UNDER PILOT/BUILD: rail-corridor-incident-and-dispatch-ledger-recovery
Package: Workspace/output/rail-corridor-incident-and-dispatch-ledger-recovery
Updated 2026-09-20T12:10Z. Controller state: pilot.

### Compliance with the four binding batch rules (supervisor message 2026-09-20T11:5xZ)
- Rule 1 universal signal: the structure a solver must learn is the generative/physical one -
  delay propagation under headway and single-track capacity, and dispatcher response. It is computed
  privately by prepare.py over the corpus and is taught exactly as well by the released training split
  as by the full public source; the public source contains no realized-operations model at all. The
  learning signal is NOT the identity or per-group structure of an identifiable public item.
- Rule 2 bundle-size two-stage attack: implemented in _lookup_attack.py. Bundle = one case
  (~56 public rows, ~14 whole services). Stage 1 de-anonymises the bundle to its real corridor/date/
  window; stage 2 assumes the origin is known FOR FREE and re-attacks with the real recorded delays
  and the real official cause records. Measured stage 2: pearson(published delay, real recorded delay)
  = -0.0076 over 38,626 matched rows; de-anonymised real-corpus attacker scores 0.1619 versus the
  0.1685 label-prior floor, i.e. the attacker does not even reach the floor. Stage 1 is being
  re-measured with a stronger anchor-based enumerator (the first version was too weak to be honest).
- Rule 3 ceiling minus capability: measuring the capability-matched GBM and, for the identical hidden
  programs, the same solver on a noise-free dropout-free observation channel as the achievable ceiling.
- Rule 4 order of work: duplicate audit, retrieval attack, floor-relative baselines, null audit and
  premortem are all being completed before the registry readiness object is written.

### Measured so far (canonical grader, real prepared split)
- prepare.py: 2,400 train cases / 322,506 rows; 800 test cases / 55,781 rows; 49 usable corridors
  split 29 train / 20 hidden; byte-identical on re-run.
- oracle 1.0000 exactly; chance floor (empty/all-NONE) 0.1237; label prior / shipped sample 0.1685;
  one-head oracles: incidents 0.6237, interventions 0.3522, primary 0.2716.
- grader robustness 16/17 then 17/17 after the sample band was corrected.
- Source: Fintraffic Digitraffic, CC BY 4.0 with commercial use and redistribution explicitly
  permitted; 10 official responses, ~200 MB, SHA-256 recorded.

### Measured gates — FINAL SPLIT (canonical grader, real prepared split, 2026-09-20T12:55Z)
Design fix applied after the first ceiling probe: only disruptions and control actions that left a
trace in the published rows are scored. Before the fix 14.7% of incidents were unobservable and the
observability ceiling was 0.9375; after it, 1.4% and 0.9938.
- Scale: 2,400 train cases / 322,506 rows; 800 test cases / 55,781 rows; 49 usable corridors split
  29 train / 20 hidden; 1.90 scored incidents and 4.61 scored interventions per case; all five
  incident types and all eight primary classes present in the hidden split.
- Lookup gate PASS at shipped bundle size (1 case = median 56 rows / 7 whole services). Stage 1
  de-anonymisation GRANTED at 1.000. Stage 2, with the true corridor/date/window/service numbers and
  the real recorded delays and official cause records, scores 0.1681 against a 0.1668 label-prior
  floor and 0.1575 chance floor: +0.0013 for full origin knowledge. Pearson(published, real delay)
  = -0.0076 over 38,626 rows.
- Floors and attacks: chance floor 0.1575; label prior / shipped sample 0.1668; metadata-only 0.1668
  (identical to the prior, so the published plan carries no signal); domain rule/DSP 0.3126;
  oracle exactly 1.0000; observability ceiling 0.9938.
- One-head oracles: incidents 0.6237, interventions 0.3859, primary 0.3053 - no decorative head.
- Red team (all at or below the prior): max-size spam 0.0854, all-CANCEL 0.0609, HOLD everywhere
  0.1612, shotgun 0.1553, copy commonest train ledger 0.1575, copy random train ledger 0.1403,
  true first incident duplicated 12x 0.2286.
- Grader: 17/17 robustness checks; perfect exactly 1.0; 0.1 s for 800 cases, 0.7 s worst case;
  self-contained assignment solver, no scipy dependency.
- Deterministic re-prepare byte-identical; leakage scan of all public artifacts clean.
- Capability-matched GBM 0.4004; achievable ceiling (observability bound) 0.9938;
  **headroom ceiling - capability = 0.5934**; capability - chance floor = 0.2429.
  Clean-channel probe 0.4205, only +0.0202 over the solver, so the gap to the ceiling is modelling
  difficulty rather than measurement noise.

### Status: COMPLETE LOCALLY, verdict Proceed, blocked only on Shipd authentication
Controller: state `retry_wait`; slot bound to registry key
`rail-corridor-incident-and-dispatch-ledger-recovery` and to the two exact URLs; a `browser_auth`
transient is recorded. Registry status `ready_for_review`, readiness verdict Proceed with zero
unresolved gates; the Python reimplementation of validate_handoff_readiness prints BUILD READY.

Package files (Workspace/output/rail-corridor-incident-and-dispatch-ledger-recovery):
prepare.py, grade.py, PASTE_THIS_PREPARE.txt, PASTE_THIS_GRADE.txt (hash-identical to their sources),
CHALLENGE_FORM_FILL.md, DATASET_FORM_FILL.md, SOURCE_VERIFICATION.md, DATA_ACQUISITION.md,
NOVELTY_AND_DUPLICATE_AUDIT.md, REVIEWER_PREMORTEM.md, LOOKUP_GATE_EVIDENCE_RAIL.md, FINAL_AUDIT.md,
raw_upload.zip (8.3 MB, 14 flat members), public/ (train.csv, train_answers.csv, test.csv,
sample_submission.csv), private/answers.csv, and the audit scripts _sanity_smoke.py, _baselines.py,
_analyze.py, _ceiling.py, _lookup_attack.py, _redteam.py with their JSON results.

### Exact next action when a Shipd session is confirmed
1. Open the two exact URLs in separate tabs and verify the IDs before any write.
2. Dataset page: title and description from DATASET_FORM_FILL.md, upload raw_upload.zip, set licence
   CC BY 4.0 and source URL https://rata.digitraffic.fi/api/v1/, rebuild, run validation, resolve every
   red and yellow finding genuinely, then Mark as Ready.
3. Challenge page: Hard / CPU, title, description body from CHALLENGE_FORM_FILL.md, tags, maximize with
   min 0.0 and max 1.0, paste PASTE_THIS_PREPARE.txt and PASTE_THIS_GRADE.txt, Run Prepare, then the
   full check suite.
4. Stop with every check green and Run Agents visibly available. Run Agents was NOT requested for this
   slot and must not be clicked.
5. Keep SUBMISSION_POOL_STATE.json synchronized throughout.

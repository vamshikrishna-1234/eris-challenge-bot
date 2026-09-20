# Final audit — Rail Corridor Incident And Dispatch Ledger Recovery

Slot `batch-20260920-044727-task-003`, candidate 3. Audited locally on 2026-09-20. No Shipd page was
opened: this container has no authenticated session, so every statement below is about local artifacts
and is explicitly not a claim about the live platform.

PowerShell is unavailable in this container, so `scripts/workspace_probe.ps1` and
`scripts/validate_handoff_readiness.ps1` were reimplemented in Python under the slot folder
(`workspace_probe.py`, `validate_handoff_readiness.py`) and both were run. The workspace probe passes
15/15 checks.

## 0. Design fix applied during the audit

The first ceiling probe showed that 14.7 % of scored incidents had left no trace in the published rows
- a restriction on a section that no reported service used, for instance - so no solver could ever
recover them, and the observability ceiling was only 0.9375. `prepare.py` now scores only the
disruptions and control actions that actually touched an observed movement. The split was regenerated
and every measurement below was re-run on it; the ceiling is now 0.9938 and the participant-visible
description states the rule. Nothing about the physics changed: unreported disruptions still happen in
the modelled world, they are simply not charged to the solver.

## 1. Source, licence and provenance

| Check | Result |
|---|---|
| Official endpoints reachable without credentials | Yes, 12 responses, all HTTP 200 |
| Licence | CC BY 4.0, commercial use and redistribution explicitly permitted |
| Attribution carried in the bundle | `LICENSE.txt`, "Source: Fintraffic / digitraffic.fi, license CC 4.0 BY" |
| Modification notice carried in the bundle | `PROVENANCE.txt` |
| Per-file SHA-256 recorded | Yes, in `DATA_ACQUISITION.md` and `PROVENANCE.txt` |
| Real vs modelled stated explicitly | Yes, in `SOURCE_VERIFICATION.md`, the dataset card and the participant description |
| Real `actualTime` / `causes` used anywhere | No, deliberately excluded |

## 2. Scale and split stability

| Quantity | Measured |
|---|---|
| Usable corridors after filtering | 49 |
| Scored incidents / interventions per case | 1.90 / 4.61 |
| Train / hidden corridors (disjoint) | 29 / 20 |
| Train cases / public rows | 2,400 / 322,506 |
| Hidden cases / public rows | 800 / 55,781 |
| Services per case | 6 to 27 |
| Corridor length | 5 to 16 stations |
| Hard minimums asserted in `prepare.py` | >= 24 usable corridors, >= 10 hidden corridors, >= 25 hidden occurrences of every incident type and of NONE, SHORT_TURNED, CANCELLED |
| Deterministic re-prepare | Byte-identical on all five output files |

## 3. Reversibility, measured at the shipped bundle size

| Check | Result |
|---|---|
| Shipped bundle | 1 case = 1 corridor-window bundle, median 56 rows / 7 whole services |
| Stage 1 de-anonymisation | **Granted to the attacker at 1.000** (worst case) |
| Stage 2, origin known, real recorded delays and real official causes | **0.1681** |
| Label-prior floor for comparison | 0.1668 |
| Chance floor for comparison | 0.1575 |
| Domain rule applied to the published rows, for scale | 0.3126 |
| Pearson(published delay, real recorded delay), 38,626 matched rows | **-0.0076** |

Handing the attacker the true corridor, date, window and real service numbers, plus the entire real
operating record of that day, is worth **+0.0013 over guessing the modal incident type**, on a scale
where the same rule applied to the published rows scores 0.3126 and the perfect ledger scores 1.0. The
scored ledger is a private construction and exists in no public record.

## 4. Floors, attacks, capability and ceiling

| Submission | Score |
|---|---|
| Chance floor (empty / all-NONE) | 0.1575 |
| Label prior (shipped sample submission) | 0.1668 |
| Metadata-only (plan and corridor structure, no realized times) | 0.1668 |
| Domain rule / DSP baseline | 0.3126 |
| Capability-matched GBM (the route a capable agent takes) | **0.4004** |
| Achievable ceiling (observability bound) | **0.9938** |
| Clean-channel probe (same solver, no measurement noise or dropout) | 0.4205 |
| Oracle | 1.0000 |

The achievable ceiling is measured by removing from the truth every entry that left no trace in the
published rows, since no predictor that never sees the scored answer could report it. After the
design fix in section 0 only 1.4 % of scored incidents remain unrecoverable, so the ceiling is 0.9938
and headroom is judged as `0.9938 - capability`, not as skill above zero. The clean-channel probe is
a separate diagnostic: it re-runs the identical hidden programs through a noise-free, dropout-free
observation channel and re-scores the same solver, which isolates how much of the solver's residual
error is measurement noise rather than modelling difficulty. That probe returns 0.4205, only +0.0202
over the solver's 0.4004, so almost none of the gap to the ceiling is measurement noise: the solver
simply cannot invert the propagation, and a better one has 0.59 of room.

**Headroom = ceiling - capability = 0.9938 - 0.4004 = 0.5934**, against `capability - chance floor` of
0.2429. The task is therefore neither saturated for a capable solver nor unachievable.

The metadata-only attack lands exactly on the label prior, which confirms the published operating plan
carries no information about the hidden program: the incidents are drawn independently of the plan.

The modelled world is more disrupted than the real Finnish railway - published delays have a median of
4.4 minutes and a 90th percentile of 26.2, against 0 and 4 in the real recorded data. That is a
deliberate calibration choice, so that a 180-minute window carries enough evidence to be informative,
and it is stated rather than implied.

## 5. Metric-null and one-head audit

| Submission | Score |
|---|---|
| Empty ledger | 0.1575 |
| Incident head oracle only | 0.6237 |
| Intervention head oracle only | 0.3859 |
| Primary head oracle only | 0.3053 |

Each head returns its full declared weight when solved and nothing when ignored, so no head is
decorative and none can be skipped for free.

## 6. Red team

| Adversarial submission | Score |
|---|---|
| Max-size random spam (12 incidents, 120 interventions) | 0.0854 |
| All-CANCEL / all-CANCELLED | 0.0609 |
| HOLD at every train-stop pair | 0.1612 |
| Shotgun: every incident type at every early location | 0.1553 |
| Copy the commonest training ledger | 0.1575 |
| Copy a random training ledger | 0.1403 |
| True first incident duplicated twelve times | 0.2286 |

Every shortcut lands at or below the label-prior floor and far below the rule baseline. Flooding the
ledger is punished by the soft-F1 denominator rather than rewarded.

## 7. Grader contract

`_sanity_smoke.py`: **17/17 checks pass**.

- Perfect submission scores exactly 1.0.
- Sample submission 0.1668, comfortably above the declared minimum of 0.0 and inside the band the live
  rules ask for.
- Missing, extra or duplicated case ids score 0.0; a renamed column scores 0.0; an unreadable file
  scores 0.0.
- Malformed JSON, NaN cells, oversized JSON, wrongly typed fields, out-of-range indices and unknown
  enum values are all row-local and never fatal.
- Degrading a perfect submission strictly lowers the score and still beats the sample, so the metric is
  monotone in the right direction.
- Runtime: 0.1 s for a perfect submission over 800 cases, 0.7 s for a worst-case-size submission.
- The grader has no third-party dependency beyond `pandas`; the assignment solver is self-contained.

## 8. Novelty

Railway, timetable, headway, junction, disruption and outage score zero hits across 3,087 extracted
platform titles and the 92-entry registry. Nearest neighbours and the substantive differences are set
out in `NOVELTY_AND_DUPLICATE_AUDIT.md`. The source has no canonical ML benchmark task attached, and
the two quantities a benchmark would reuse are deliberately unused.

## 9. Compliance with the four binding batch rules

1. **Universal signal.** What a solver must learn is generative and physical - delay propagation under
   headway and single-track capacity, and the dispatcher's response. It is computed privately across
   the corpus and is taught as well by the released training split as by the whole public source. It is
   not the identity or per-group structure of an identifiable public item, so hardening does not trade
   against the learning signal.
2. **Bundle-size two-stage attack.** Run and reported above, with stage 1 granted to the attacker.
3. **Ceiling minus capability.** Reported above against the chance floor for the restricted choice and
   the achievable ceiling, not as skill above zero.
4. **Order of work.** The duplicate audit, retrieval attack, floor-relative baselines, ceiling, null
   audit and premortem were all completed before the registry readiness object was written.

## 10. Outstanding

The only outstanding item is the platform phase. Shipd is not authenticated in this container, so no
dataset or challenge page was opened, no value was written, nothing was marked ready and Run Agents was
never clicked. `SUBMISSION_POOL_STATE.json` records
`stage = local_package_ready_awaiting_authenticated_session` and
`stop_reason = blocked_no_authenticated_shipd_session`, with `website_writes_performed = false`.

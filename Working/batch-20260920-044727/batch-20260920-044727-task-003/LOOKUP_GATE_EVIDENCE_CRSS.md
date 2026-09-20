# Lookup-gate evidence — candidate 2 `crss-crash-event-ledger-reconstruction` (slot task-003)

Measured verdict: **Reject** (public-source reversibility). Measured during scouting, before any package
was built, per the transferable lesson from candidate 1.

## Source and pool

NHTSA Crash Report Sampling System (CRSS) annual CSV releases 2016-2023, all HTTP 200 from
`https://static.nhtsa.gov/nhtsa/downloads/CRSS/<year>/CRSS<year>CSV.zip`; SHA-256 in
`pilot_crss/archive_sha256.txt`. US federal government work (public domain, redistributable).

Native target: `cevent.csv`, the officially coded crash sequence of events - ordered `EVENTNUM` with
`VNUMBER1`, `AOI1` (area of impact, clock point), `SOE` (event type), `VNUMBER2`, `AOI2`.

Measured pool: **417,335 crashes**, 693,506 coded events; 143,313 crashes with >= 2 events,
68,663 with >= 3 events. Scale was never the problem.

## Attack

The whole public corpus is the attack surface: an attacker downloads the same 8 CRSS releases, rebuilds
the planned public representation for all 417,335 crashes, and matches. Because the representation is
purely categorical, **exact match is the optimal attacker** - no fuzzy method can beat it - so the
measurement is exact rather than an approximation.

Two numbers per representation, over the full 417,335-crash pool:
- `unique_repr` - fraction of eligible cases whose public representation occurs exactly once in the
  public pool, i.e. the origin crash is identified outright and the hidden ledger is read verbatim;
- `answer_recovery` - probability that a crash drawn from the matched group carries the identical
  ledger. This is simultaneously the **strongest obvious solver baseline** (exact-representation
  retrieval), so it doubles as the capability-matched attack.

Scripts: `pilot_crss/repr_build.py`, `pilot_crss/run_lookup.py` (V ladder),
`pilot_crss/run_lookup2.py` (W floor ladder). Results: `pilot_crss/lookup_v1.json`,
`pilot_crss/lookup_v2.json`, logs `lookup_run.log`, `lookup2_run.log`.

## Measured reversibility ladder (cases with >= 2 coded events, n = 143,313)

| Representation | Public content | unique_repr | answer_recovery |
|---|---|---|---|
| V1_rich | full crash context + 24 per-vehicle fields incl. damaged-area set | **1.000** | 1.000 |
| V2_mid | 10 crash fields + 14 per-vehicle fields incl. damaged-area set | 0.9855 | 0.9922 |
| V3_lean | 6 crash fields + 7 per-vehicle fields incl. damaged-area set | 0.8515 | 0.9047 |
| V4_min | 4 crash fields + 4 per-vehicle fields incl. damaged-area set | 0.5103 | 0.6281 |
| W4_dmg_nosoe | 6 crash fields + body/deformation/damaged-area set | 0.4831 | 0.6040 |
| W5_pcrash_nosoe | 6 crash fields + body/deformation/pre-crash movement, **no damage set** | 0.3114 | 0.4366 |
| W1_set+body+def | 6 crash fields + body/deformation + unordered event-type multiset | 0.4638 | 0.7092 |
| W2_set+body | 4 crash fields + body group + unordered event-type multiset | 0.2100 | 0.4922 |
| W3_set_only | unit counts only + unordered event-type multiset | **0.0877** | 0.3367 |

(For cases with >= 3 events, n = 68,663, every number is equal or worse: W3_set_only reaches
`unique_repr` 0.1807 / `answer_recovery` 0.3653.)

## Why this is intrinsic, not a tuning problem

The workspace precedent for a passing lookup gate is ~2.5-3 % rank-1
(`anonymous-storm-episode-partition-recovery` 0.026, `gas-chamber-exposure-program-recovery` 0.025).

`W3_set_only` is the **floor** of the design: it keeps only the number of vehicles, parked vehicles and
non-motorists plus the unordered multiset of event types, and discards every piece of physical evidence
(damaged-area sets, deformation extent, pre-crash movement, roadway geometry, lighting, injuries) that
the reconstruction task depends on. At that floor the gate still fails by 3x on origin identification
(8.8 %) and the exact-representation retrieval baseline already reproduces the exact hidden ledger for
34 % of cases - so the same representation fails the shortcut/headroom gate as well.

The cause is quantitative and general: the per-vehicle damaged-area set alone is a near-unique
fingerprint (up to 2^14 states per vehicle), and the categorical evidence vector needed for the task
carries far more bits than `log2(417,335) ~= 18.7` minus the ~5-bit margin the gate requires. For a
fully public record-level corpus of size N, the public representation must carry no more than about
`log2(N) - 5` bits of record-identifying information. No CRSS representation that still supports crash
event-order reconstruction comes close.

Per `pre-handoff-gate.md` ("Public answer reversibility") the verdict is Reject, and no re-tuning of the
field list can rescue it.

## Transferable rule derived (applies to every future public-source candidate in this workspace)

A public-source candidate can only pass the lookup gate by one of:

1. **Ephemeral supervision** - the labels never persist on the public internet (live feed with no public
   archive), so origin recovery is impossible by construction;
2. **Non-joinable supervision** - the hidden answer is a private construction (e.g. a privately
   randomized processing chain applied to real public inputs) that never existed in any public record,
   so recovering the origin record yields nothing;
3. **Bit-budget compliance** - the public representation carries <= ~`log2(N) - 5` bits of
   record-identifying information, which in practice means the difficulty must come from combinatorial
   structure over a handful of coarse attributes, not from rich per-record evidence.

Candidate 1 (wind SCADA, 12.5 %) and candidate 2 (CRSS, 8.8 % at the design floor) both failed because
they relied on rich per-record evidence from a fully public corpus, i.e. they violated rule 3 and
satisfied neither 1 nor 2.

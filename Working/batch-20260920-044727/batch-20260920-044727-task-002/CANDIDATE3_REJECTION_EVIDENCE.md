# Candidate #3 — Small-Area Joint Composition Recovery (ACS PUMS) — VERDICT: REJECT (measured)

Slot `batch-20260920-044727-task-002`. All numbers measured locally 2026-09-20 in this container.
Scripts and raw JSON under `scout3/`: `pilot_lib.py`, `pilot_difficulty.py|.json`,
`pilot_ceiling.py` + `pilot_ceiling_unit600.json` + `pilot_ceiling.stdout.log`, `pilot_leakage.py|.json`, `pilot_harden.py|.json`, `pilot_rescue.py|.json`.

## Candidate

Family: **aggregate inversion / disaggregation** — measured as having **zero** archived platform
challenges (grep over the full 818-challenge archive body for disaggregation, ecological inference,
iterative proportional fitting, small-area estimation, population synthesis) and **zero** of 84
registry entries. Source: **ACS 2023 1-Year PUMS** person files, CC0 / U.S. public domain.

Each scored instance is a **reporting unit**: a private mixture of real person records drawn from
several source PUMAs with private Dirichlet weights, records consumed without replacement. The unit
releases marginal tables only; the scored target is the unit's **edu x occ x inc joint composition**,
derived by the preparation pipeline across hundreds of source rows. Chance floor is the best constant
table, so skill = 1 - SSE(pred)/SSE(best constant) is exactly 0 at the floor.

## Gates that PASSED

| Gate | Result |
|---|---|
| Licence / redistribution | CC0 / U.S. public domain (data.gov catalogue record for ACS 1-Year PUMS). |
| Official access | Direct HTTPS from census.gov, no credentials; 8 state person files, 274 MB. |
| Native labels | All attributes are native PUMS fields (SCHL, OCCP, PINCP, AGEP); no invented truth. |
| Post-filter scale | 1,256,063 adult records; 1,482 train units / 624 test units at unit size 600. |
| Independent groups | **1,114 PUMAs**, split 779 train / 335 test, so test units use only held-out areas. |
| Novelty | 0 of 818 archived challenges, 0 of 84 registry entries in this family. |
| CPU / size | Categorical tables only; compacted corpus is 17 MB. |
| Not near-chance | Unlike candidate #1, every method beats the chance floor by a wide margin. |

## Gate that FAILED — leakage vs. difficulty are the same quantity

### Step 1 — baseline ladder at the natural setting (unit size 600, 2-4 source areas)

> **Artifact note (evidence integrity, added after the run).** `pilot_ceiling.py` printed the
> unit-size-600 block below and was then killed by its 5000 s timeout during a second, unit-size-1500
> arm (exit code 124), so the script's own `json.dump` never executed and **`pilot_ceiling.json` does
> not exist**. The completed measurement was captured verbatim from the task stdout and is preserved
> as `scout3/pilot_ceiling.stdout.log` and `scout3/pilot_ceiling_unit600.json`. Only the unit-600
> numbers from this script were ever cited anywhere. Ceilings at unit sizes 600, 1500 and 2500 were
> independently measured by `pilot_harden.py` and `pilot_rescue.py`, both of which completed and
> wrote their JSON, so **no cited number and no verdict changes**.

| Method | Skill |
|---|---|
| best constant (chance floor) | 0.0000 |
| training-mean constant | -0.0096 |
| IPF with a uniform seed (naive independence) | -0.8979 |
| **IPF with a global seed — capability-matched attack** | **0.5354** |
| ridge on released margins, then raked | 0.5634 |
| mixture-oracle ceiling (knows the private source mixture) | 0.7107 |
| oracle (exact answer) | 1.0000 |

The ceiling is 0.711 because the target is the unit's *empirical* joint; the rest is irreducible
sampling noise. The usable competition band is therefore ceiling minus capability-matched = **0.175**.

### Step 2 — source-retrieval attack (the leakage gate)

The solver identifies the corpus as PUMS, downloads it, and fits a non-negative mixture of the 1,114
**real public areas** to each unit's released margin vector, then reads the joint off those areas'
public microdata. The held-out areas are present in the public corpus while being absent from the
challenge's training split, so this is strictly more than the honest task.

| Unit size | Capability-matched | Best honest | **Source-retrieval attack** | Gain |
|---|---|---|---|---|
| 600 | 0.545 | 0.563 | **0.661** | **+0.098** |
| 1500 | 0.662 | 0.693 | **0.855** | **+0.162** |

The attack recovers 93% of the achievable ceiling at unit size 600 and beats every honest method.

### Step 3 — hardening sweep (`pilot_harden.json`): the trade-off is one-for-one

More source areas per unit and disclosure-control rounding of the released counts do close the leak,
and close the competition band by the same amount.

| Unit size | Sources | Rounding | Capability | Ceiling | Attack | Attack - best honest | **Ceiling - capability** |
|---|---|---|---|---|---|---|---|
| 600 | 2-4 | none | 0.545 | 0.727 | 0.667 | **+0.091** | 0.182 |
| 600 | 6-12 | none | 0.389 | 0.506 | 0.420 | +0.013 | 0.117 |
| 600 | 6-12 | to 10 | 0.378 | 0.494 | 0.397 | +0.003 | 0.117 |
| 600 | 6-12 | to 25 | 0.321 | 0.436 | 0.304 | -0.030 | 0.115 |
| 600 | 10-20 | to 25 | 0.247 | 0.332 | 0.202 | -0.051 | 0.086 |
| 900 | 10-20 | to 25 | 0.328 | 0.441 | 0.311 | -0.031 | 0.113 |

### Step 4 — rescue test (`pilot_rescue.json`): bigger units and a coarser target do not help

| Config | Cells | Capability | Ceiling | Attack | Attack - best honest | Ceiling - capability |
|---|---|---|---|---|---|---|
| 1500 records, 6-12 sources, round 10, full target | 150 | 0.527 | 0.698 | 0.599 | **+0.054** | 0.170 |
| 1500 records, coarse target | 60 | **0.776** | 0.859 | 0.802 | +0.017 | **0.083** |
| 2500 records, coarse target | 60 | **0.812** | 0.908 | 0.856 | +0.034 | **0.096** |

Coarsening the target lifts the *standard domain method* to 0.78-0.81, i.e. IPF alone nearly solves
the challenge — the saturation failure mode that already caused a sibling slot to reject its
baserunning candidate at a 0.16 residual headroom.

## Verdict

**Reject.** Across the whole swept design space the two mandatory gates are mutually exclusive:

- every configuration with a competition band >= 0.17 hands the source-retrieval attack >= +0.054;
- every configuration whose attack gain is <= +0.02 has a band <= 0.12, or a capability-matched
  baseline of 0.78-0.81, which is saturated.

There is no configuration in this corpus that satisfies both. Source, licence, native labels, scale,
independent-group count and novelty all pass, so the failure is in the learning problem, not the data.

## Generalisable lesson for the batch (added to the Scout gate)

**If the only signal that beats the standard domain method is a property of identifiable public
source groups, then the learning signal and the leakage channel are the same quantity, and hardening
trades them one-for-one.** Measured here: closing the source-retrieval gain from +0.098 to +0.003
also closed the competition band from 0.182 to 0.117, and every attempt to reopen the band reopened
the leak.

**Design rule for the next candidate: the predictable structure must be UNIVERSAL — a physical,
signal-level or generative regularity that the training split teaches just as well as the full source
would — not group-specific structure that retrieval supplies.** When the signal is universal,
downloading the source gives a solver no edge over the released training data, so the leakage gate
and the difficulty gate stop competing. Candidates #1, #2 and #3 all failed because their signal or
their target was tied to the identity of a public source item or group (a photograph's caption, a
camera station's roster, an area's association structure).

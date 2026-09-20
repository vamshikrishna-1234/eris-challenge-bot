# Lookup-gate evidence — candidate `wind-turbine-stop-ledger-recovery` (slot task-003)

Measured verdict: **Hold** (public-source reversibility). All other gates passed.

## Attack

Adaptive full-corpus retrieval against the complete official raw corpus that the dataset itself must ship:
92 turbine-year series, 4,323,440 ten-minute steps. The attacker re-derives every public channel from the raw
archives with the same coding family and smoothing, then matches each public case with FFT sliding-window
normalised cross-correlation per channel (whole window plus chunked alignment with +-8 step shifts), a global
stretch grid (0.70-1.40 to undo the time warp), and banded-DTW re-ranking of the top 20 candidates.
A hit means the rank-1 candidate is the true turbine-year within +-12 steps (2 h) of the true offset — enough to
read the hidden status log for that window straight out of the public archive.

Scripts: `pilot_kelmarsh/attack2.py` (raw-channel representations), `attack3.py`/`attack4.py`/`attack5.py`
(coded representations, adaptive attacker).

## Measured rank-1 origin recovery per public representation

| Version | Public representation | Rank-1 | Log |
|---|---|---|---|
| v1 | raw channels, warp +-12 %, gain 3 %, noise 2 %, drop 5 % | 5/10 | `attack2_production_v1_partial.log` |
| v2 | warp +-32 %, pre-smoothing, noise 5 %, drift 10 %, drop 8 % | 3/11 | `attack2_v2.log` |
| v4 | coded channels, still carrying site wind/production regimes and temperature trajectories | 4/7 | `attack3_v4_partial.log` |
| v5 | no site weather series; fleet-relative `dP`/`drpm` (0.25 steps), temperature bands | 0/12 seed 2026, 4/18 seed 7 = **4/30** | `attack4_seed2026_n12.log`, `attack4_seed7_n18.log` |
| v6 | fully ordinal: 3-level fleet state, 4-level production/rotor state, all excursions as 5-level bands | 1/12 seed 2026, 2/12 seed 7 = **3/24** | `attack5_seed2026_n12.log`, `attack5_seed7_n12.log` |

A conservative transform-strength sweep on a 12-series candidate pool (`xform.log`, `xform2.log`, 16 queries)
gave the same ordering: v1 81 %, T1 50 %, T2/T4/T5 12.5 %, T6 19 %, T3 0 %.

Workspace precedent for a passing gate is about 2.5-3 % rank-1
(`anonymous-storm-episode-partition-recovery` 0.026, `gas-chamber-exposure-program-recovery` 0.025;
`electrical-tree-growth-order-reconstruction` was held at 1/33). v6 at 12.5 % is four to five times that.

## Why this is intrinsic, not a tuning problem

The same windows recover in every version (`K05 2017-02-23`, `K05 2020-02-27`, `P06 2016`): turbine-days whose
fleet-relative behaviour is unusual, which are exactly the days that carry the scored stop events. The scored
supervision (the controller status log) ships inside the dataset the challenge must publish, and it is also
freely downloadable from the two public Zenodo records, so any recovered origin hands the solver the exact
answer. Coarsening further (below four ordinal levels, or shorter windows) removes the evidence the ledger task
itself depends on; the sweep shows the only variant that reached 0 % (T3) was also the most destructive.

Per `pre-handoff-gate.md`, "public answer reversibility" requires a private or unpublished holdout, or a measured
transformation that defeats a strong modality-specific retrieval attack without destroying the task. Neither is
available here: both farms are public, and the labels are public for every timestamp in the corpus.

## What would make a related candidate viable

A wind-fleet formulation needs supervision that is **not** publicly joinable to the published inputs — for
example an operator log that is not redistributed, or a target that is a genuine forecast/counterfactual rather
than a record that exists verbatim in the public archive.

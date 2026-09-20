# Challenge form — Groundwater Abstraction Return Reconciliation

## Title
Groundwater Abstraction Return Reconciliation

## Difficulty
Hard

## Compute tier
**CPU.** Measured: the strongest reference solution is pure NumPy/SciPy and
runs at 5.11 s per scene on a single core, so the full 686-scene hidden test
completes in about 58 minutes inside a 1.5-hour budget; a competent lighter
route runs at 0.03 s per scene. Peak memory is under 1 GB. There is no dense
network to train and no measured benefit from a GPU, so an A10G or H100 tier
would be idle hardware.

## Overview

A water regulator receives an abstraction *return* from every licensed borehole
in a monitored area: how much water the operator says they took, period by
period. Returns are not always right. Some operators under-report, some
over-report, some report the right volume in the wrong weeks, and some pump
without declaring anything at all. The aquifer, however, keeps an honest
record: every cubic metre actually abstracted shows up as drawdown in the
observation wells, spread out in space and smeared in time by the aquifer's
transmissivity and storage coefficient.

This challenge is that reconciliation. For each monitored area you are given
the declared returns, the geometry, and the observed water levels, and you must
recover what was **actually** abstracted from each borehole — and the two
aquifer properties that control how abstraction turns into drawdown.

The water-level series carry a real background: these are the fluctuations a
groundwater monitoring well genuinely records — barometric response, earth
tides, recharge events, ambient regional pumping — taken from USGS National
Water Information System instantaneous groundwater-level data, which are in the
public domain. The abstraction scenes and the aquifer response are simulated
from the Theis solution with superposition in time and space; the corpus is a
procedurally generated benchmark over that real measured background, and it is
described as such throughout.

## What you get

| Item | Description |
|---|---|
| `train.csv` | 1,814 scenes with the public evidence **and** the answers |
| `test.csv` | 686 scenes with the public evidence only |
| `sample_submission.csv` | a valid, weak, non-degenerate submission in the required format |
| `train/series/<id>.csv`, `test/series/<id>.csv` | one water-level file per scene |

### `train.csv` / `test.csv` columns

| Column | Type | Description |
|---|---|---|
| `id` | int | scene identifier; also the submission key |
| `series` | string | path to this scene's water-level file, relative to its split folder |
| `n_boreholes` | int | number of registered boreholes in the area |
| `n_obs` | int | number of observation wells |
| `boreholes` | JSON string | list of objects `{bh_id, x, y, declared}`; `x`, `y` in metres in the scene's own local frame; `declared` is the declared abstraction return as 7 consecutive four-day blocks in m³/day |
| `obs` | JSON string | list of objects `{obs_id, x, y}` for the observation wells, same frame and units |
| `prompt` | string | the task statement, identical on every row |
| `actual` | JSON string | **train only.** The true abstraction ledger, one list of 7 block rates per borehole, in the same order as `boreholes` |
| `log_t` | float | **train only.** log10 transmissivity in m²/day |
| `log_s` | float | **train only.** log10 storage coefficient (dimensionless) |

### Water-level file columns

| Column | Type | Description |
|---|---|---|
| `obs_id` | string | observation well, matching an `obs_id` in the scene's `obs` list |
| `t000` … `t223` | float | water level in metres relative to that well's own mean over the period, sampled every 3 hours for 28 days |

## Submission format

One row per `id` in `test.csv`.

| Column | Type | Description |
|---|---|---|
| `id` | int | scene identifier from `test.csv` |
| `actual` | JSON string | the recovered abstraction ledger: a list with one entry per borehole, in the order the scene's `boreholes` list gives, each entry a list of 7 non-negative block rates in m³/day |
| `log_t` | float | recovered log10 transmissivity in m²/day |
| `log_s` | float | recovered log10 storage coefficient |

Example row:

```
id,actual,log_t,log_s
1814,"[[0,0,0,0,0,0,0],[412.5,412.5,0,0,388.1,388.1,0],[0,0,730.0,730.0,730.0,0,0]]",2.104,-2.663
```

Rows whose `id` does not appear in the hidden test are ignored. A malformed or
missing `actual` is read as an all-zero ledger; a malformed `log_t` or `log_s`
scores zero on the aquifer head. The grader never crashes on bad input.

## Scoring

The hidden test is partitioned into 8 held-out groups. A score is computed for
each group and the reported score is the **mean of the group scores**. Each
group score combines two heads:

| Head | Weight | What it measures |
|---|---|---|
| Ledger | 0.62 | On every borehole whose declared return is materially wrong (total block error above 100 m³/day), the fraction of the declaration's volume error that your ledger removes — expressed as **skill over the best trivial strategy**, so both keeping the declaration and reporting no abstraction at all score 0 |
| Aquifer | 0.38 | Accuracy of `log_t` and `log_s`, `0.5·exp(−|Δlog10 T|/0.12) + 0.5·exp(−|Δlog10 S|/0.18)`, expressed as **skill over the best constant predictor** |

Theoretical minimum **0.0**, theoretical maximum **1.0**.

Measured reference points on the prepared split: perfect answers 1.0000; an
achievable ceiling using the true aquifer parameters 0.6024; a strong reference
solution 0.3152; the shipped sample submission 0.1451; a uniform-random
submission 0.0055; copying the declared returns 0.0001; an all-zero or empty
submission 0.0000.

## What not to use

- Do not submit the declared returns unchanged, an all-zero ledger, or a
  constant ledger. Each is a measured null and scores at the floor by design.
- Do not try to identify the underlying public monitoring wells behind the
  background fluctuation. It was measured: an attacker holding the entire pool
  of real segments recovers the source of a published series 0.2% of the time
  against a 0.18% chance rate, and even a perfect match would only remove
  noise — the abstraction scenes and aquifer parameters appear in no public
  record.
- Do not fine-tune a large language model. This is a physical inverse problem
  on numeric series; solutions that ignore the aquifer response and pattern-match
  the declaration will not clear the trivial floor.

## Tags
hydrogeology, groundwater, inverse problem, time series, deconvolution,
regulatory compliance, physical modelling, CPU

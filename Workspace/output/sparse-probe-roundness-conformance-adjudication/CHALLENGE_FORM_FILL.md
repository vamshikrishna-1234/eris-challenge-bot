# Challenge creation form — fill-in (paired with `DATASET_FORM_FILL.md`)

**Platform status:** **Draft**

---

## 1) Difficulty

**Select:** **Hard**

A production inspection plan probes only four to eleven points around each circular feature, and a
sparse plan is blind to part of the form error by construction: with `n` equally spaced points an
undulation that repeats `k` times per revolution is indistinguishable from one that repeats `k mod n`
times, so whole components of the deviation fold onto others or vanish into the fitted circle. The
true peak-to-valley roundness of the full surface is therefore **not identifiable** from one feature's
probe points, and the honest answer is a distribution, not a number. Measured on the released split,
the ratio between the true roundness and the sparse peak-to-valley spans more than a factor of four
between its quartiles on the sparsest plans. The features of one part were cut in one set-up, and
different features carry different probe counts, so evidence has to be combined across a part before
the hidden structure resolves. A calibrated least-squares route with an empirical per-plan correction
reaches 0.512; a strong tree model over hand-built residual features reaches 0.698; a predictor that
is handed the private machine parameters and conditions exactly reaches 0.862.

---

## 2) Challenge Title

```
Sparse-Probe Roundness Adjudication
```

---

## 3) Problem Description

# Sparse-Probe Roundness Adjudication

## Overview

On a machining line, finished parts are checked on a coordinate measuring machine. Touch-trigger
probing is slow and the line does not stop, so an inspection plan takes only a handful of points
around each circular feature — a bore, a shaft, a journal, a seat. From those few points an inspector
has to answer three questions that a production engineer actually asks:

* **How round is this feature really?** Not the spread of the few points that were touched, but the
  peak-to-valley roundness deviation of the whole surface — and with an honest interval, because a
  sparse plan cannot pin it down exactly.
* **Does it pass?** The drawing carries a roundness tolerance. The decision has to be made from the
  same few points, so it is a probability, not a certainty.
* **Where is it coming from?** Form error on a machined circle is not white noise. Fixturing, spindle
  condition and tooling each leave their own characteristic pattern, and naming that pattern is what
  turns a rejected part into a corrected process.

This is the inverse problem that makes sparse dimensional inspection hard. A machined circular
surface deviates from a perfect circle in a small number of undulations per revolution, and a plan
of `n` equally spaced points cannot separate an undulation that repeats `k` times per revolution from
one that repeats `k` modulo `n` times. Some of the deviation therefore folds onto other components
and some disappears into the circle that gets fitted, so the sparse points systematically understate
the true deviation by an amount that depends on structure the plan cannot see. Every feature of one
part was produced in one set-up, and the features of a part do not all carry the same probe count,
which is where the missing structure can be recovered from.

**Relation to prior work.** Reference-data programmes for coordinate metrology software, such as the
NIST Algorithm Testing and Evaluation Program for Coordinate Measuring Systems, score how accurately
a program reproduces a reference **fit** from a given point set; the sampling-strategy literature for
form error, and the ISO documents for roundness and for decision rules with measurement uncertainty,
produce **point** estimates and conservative guard bands. None of those asks for a calibrated
predictive distribution under a deliberately aliasing plan, a conformance probability, and an
attribution of the underlying set-up condition. Nor is this the recovery of a hidden field from
ballistic probe trajectories in a rendered scene: there is no image here, the geometry is exact, and
what is hidden is the spectral content of a surface rather than the layout of a room.

You are given, for each inspected feature, the probe coordinates in the machine frame together with
the drawing nominal diameter and roundness tolerance. The feature centre is offset from the frame
origin by the set-up centring error, so the circle has to be fitted before any form deviation can be
read. Features that belong to the same part share a `part_id`.

## Evaluation

For every row in `test.csv` you submit five values. The score is the weighted sum of three heads,
each expressed as skill against a fixed reference:

| Head | Weight | What is scored |
|---|---|---|
| Roundness interval | 0.45 | Interval score for the central 80% interval, plus median error |
| Conformance | 0.35 | Brier score of `p_conform` |
| Set-up signature | 0.20 | Accuracy over six classes |

The roundness head uses the standard interval score for an 80% central interval: the interval width,
plus ten times any amount by which the truth falls outside it, plus twice the absolute error of the
median. A zero-width interval is therefore not a safe answer, and neither is a very wide one.

The reported score is `0.82` times the overall result plus `0.18` times the **worst** result over the
three probe-density bands (four to five points, six to eight points, nine or more), so a solution
cannot buy its score on the denser plans alone. The bands are evaluated privately.

Theoretical minimum **0.0**, theoretical maximum **1.0**. A submission with missing or extra rows,
duplicate identifiers, non-numeric or non-finite values, negative roundness quantiles, a probability
outside `[0, 1]`, or a signature class outside the six listed values scores exactly `0.0`.
`sample_submission.csv`, which answers with training label priors only, scores about `0.148`.

## Dataset

| Item | Description |
|---|---|
| `train.csv` | Labelled inspected features |
| `test.csv` | Scored features, no labels |
| `sample_submission.csv` | Prior-only example submission |

`train.csv`

| Column | Type | Description |
|---|---|---|
| `row_id` | string | Unique feature id |
| `part_id` | string | Part the feature belongs to |
| `feature_slot` | int | Index within the part |
| `feature_kind` | string | bore, shaft, counterbore, journal, seat |
| `n_probe` | int | Probed points on this feature |
| `nominal_diameter_mm` | float | Drawing nominal diameter |
| `roundness_tol_um` | float | Drawing tolerance, micrometres |
| `points_xy_mm` | json | List of `[x, y]` probe points |
| `ront_um` | float | True roundness deviation |
| `conform` | int | 1 if within tolerance else 0 |
| `signature_class` | string | Set-up signature class |

`test.csv`

| Column | Type | Description |
|---|---|---|
| `row_id` | string | Unique feature id |
| `part_id` | string | Part the feature belongs to |
| `feature_slot` | int | Index within the part |
| `feature_kind` | string | bore, shaft, counterbore, journal, seat |
| `n_probe` | int | Probed points on this feature |
| `nominal_diameter_mm` | float | Drawing nominal diameter |
| `roundness_tol_um` | float | Drawing tolerance, micrometres |
| `points_xy_mm` | json | List of `[x, y]` probe points |

`ront_um` is the peak-to-valley of the least-squares-circle profile after the standard Gaussian
roundness filter with a fifteen undulations-per-revolution cutoff, in micrometres. `points_xy_mm`
holds the probe coordinates in millimetres in the machine frame, in no meaningful order.

The six values of `signature_class` are `three_jaw_chuck`, `clamp_ovality`,
`spindle_bearing_order`, `centreless_five_lobe`, `fine_ground_smooth` and `worn_tool_chatter`.
All features of one part share one class.

## Submission

| Column | Type | Constraint |
|---|---|---|
| `row_id` | string | Every test id once |
| `ront_p10_um` | float | >= 0, finite |
| `ront_p50_um` | float | >= 0, finite |
| `ront_p90_um` | float | >= 0, finite |
| `p_conform` | float | In `[0, 1]` |
| `signature_class` | string | One of the six values |

**Compute contract.** Training and inference share an offline budget of 10 CPU cores, 62 GB RAM and
90 minutes. No GPU is required or provided. No hosted or closed-source APIs at any stage, including
distillation or pseudo-labelling from such a teacher. No external task-specific data.

**What Not To Do** (any of these is grounds for rejection on review, regardless of score):

* **Answer with a point estimate three times.** Setting `ront_p10_um`, `ront_p50_um` and
  `ront_p90_um` to the same number is a zero-width interval and the interval score charges it for
  every miss. Reporting the spread of the probed points as if it were the roundness of the surface is
  the specific failure this challenge is built around.
* **Hedge with a very wide interval.** The interval score charges the width directly; a submission
  that covers everything scores close to the floor.
* **Ignore the part.** Treating each row independently discards the shared set-up, which is where the
  signature class and much of the missing spectral structure come from.
* **Hosted / closed-source APIs** at any stage of training or inference.
* **Identifier or ordering side-channels.** `row_id` and `part_id` are salted opaque hashes, row order
  and probe order are randomised, and there is nothing to recover from them. Do not probe the
  filesystem for `private/answers.csv` or any other channel outside `public/`.
* **Format hacks.** Out-of-range probabilities, invented class names, or values meant to game the
  grader. These return a zero.

**Enforcement on invalid approaches:** rule-only solutions, or approaches that do not match the
challenge domain — for example returning a fixed multiple of the probed spread rather than learning
the conditional distribution — may be rejected before payout. The intent is to reward a genuine
learned inverse model of a sparse measurement, not score-chasing shortcuts.

---

## 4) Tags

```
metrology, manufacturing, quality-control, inverse-problems, uncertainty-quantification, calibration, geometry, tabular
```

---

## 5) Grading Configuration

* Direction: **higher is better**
* Theoretical minimum: **0.0**
* Theoretical maximum: **1.0**
* Custom grading script: **yes**, `grade.py` (see `PASTE_THIS_GRADE.txt`)
* Sample submission score on the prepared split: **0.1485**

---

## 6) Grading Script

Paste the contents of `PASTE_THIS_GRADE.txt`.

---

## 7) Prepare Script

Paste the contents of `PASTE_THIS_PREPARE.txt`.

---

## 8) GPU Tier

**CPU.**

Measured on the real prepared split (35,311 training rows, 18,643 scored rows): the full intended
route — parse the probe points, fit the least-squares circle, build residual and part-level features,
then fit three quantile models and two classifiers — trains and predicts in under three minutes on
two threads. Peak memory stays under 1 GB. There is no image, no audio and no sequence model; the
input is a few hundred thousand coordinate pairs. Neither an A10G nor an H100 would be used by any
credible solution, so a GPU tier would be a waste of the allocation.

---

## 9) What Not To Use

Hosted or closed-source LLM/vision APIs at any stage, including distillation or pseudo-labelling.
External task-specific datasets. Reverse lookups of any kind against outside collections. Filesystem
or platform probing for the private answers. Degenerate zero-width or unbounded prediction intervals
submitted as a scoring tactic.

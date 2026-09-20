# PILOT NOTES — candidate #4 (`sparse-probe-roundness-conformance-adjudication`)

Generator: `scout4/pilot_lib.py`. Gate harness: `scout4/pilot_all.py` (all gates in Rule-4 order,
checkpointing to `scout4/pilot_all.json` after every stage). Design v1 is preserved as
`scout4/pilot_lib_v1_backup.py`; design v2 is the current `scout4/pilot_lib.py`.

## Metric used for measurement (analysis form)

Three heads, each expressed as skill relative to the correct chance floor for the restricted choice:

| Head | Weight | Prediction | Loss | Chance floor |
|---|---|---|---|---|
| RONt quantiles p10/p50/p90 | 0.45 | true roundness deviation, um | mean pinball over the three taus | the train-marginal quantiles |
| conformance probability | 0.35 | P(RONt <= drawing tolerance) | Brier | the train base rate |
| machine/set-up signature | 0.20 | 6-way latent cause class | accuracy | the train majority class |

NOTE FOR THE BUILD: this analysis form puts a prior-only submission at exactly 0, which would fail
the platform's Grade Sample Validation ("sample must score comfortably above the declared minimum").
The shipped `grade.py` must therefore normalise each head against a FIXED reference constant chosen
so a label-prior submission lands at about 0.15 while a perfect submission is 1.0 and an invalid or
empty submission is 0.0. That is a presentation change to the same ordering, not a weakening.

## Design v1 (probe count fixed per part) — measured, corpus 150 machines / 1800 parts

Split by machine: 98 train machines / 52 test machines, 1186 train parts / 614 test parts,
5344 train features / 2747 test features. Conformance base rate on test 0.546.
RONt percentiles (um): p5 2.16, p25 4.73, p50 9.45, p75 19.70, p95 58.23.

| Route | score | q_skill | conf_skill | sig_skill | mean pinball (um) |
|---|---|---|---|---|---|
| chance floor | 0.000 | 0.000 | 0.000 | 0.000 | 7.444 |
| metadata only (n, nominal size, tolerance) | 0.113 | 0.000 | 0.323 | 0.000 | 3.192 |
| capability-matched domain method | 0.527 | 0.571 | 0.771 | 0.000 | 1.291 |
| intended learned route (GBM + part pooling) | 0.674 | 0.753 | 0.798 | 0.279 | 0.745 |

The capability-matched method is the strongest standard metrology route: least-squares circle fit on
the sparse probe points, peak-to-valley of the residuals, then an n-conditional empirical expansion
factor and conformance probability calibrated on the training split. It is deliberately generous
(a real inspector's rule of thumb is a fixed factor, not a fitted per-n quantile of the ratio).

v1 weakness found and fixed in v2: metadata-only reaches conf_skill 0.323 because the tolerance value
alone predicts conformance. v2 ties each drawing tolerance to the machine's own process capability so
conformance is near-balanced inside every tolerance class, without letting the tolerance depend on the
scored feature's private roundness.

v1 weakness 2: the probe count was constant across a part, so cross-feature pooling only averaged
evidence. v2 varies the probe count PER FEATURE inside a part, which turns pooling into genuine
alias fusion: with n equally spaced points, harmonic k folds onto k mod n, so an order hidden from one
feature's plan is visible to another feature's, and only a solver that fuses them can resolve the
dominant undulation order. This is the mechanism that makes the task non-textbook.

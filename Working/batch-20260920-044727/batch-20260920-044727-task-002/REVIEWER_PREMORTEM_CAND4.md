# Reviewer premortem — candidate #4 `sparse-probe-roundness-conformance-adjudication`

All numbers are from `scout4/pilot_v3_results.json` (design v3, 160 machines / 2000 parts, split by
machine) and `scout4/pilot_extra.json` (three independent corpus seeds).

**1. Closest source benchmark, and why this is a different learning problem.**
The nearest established work is coordinate-metrology *fitting-software testing* (NIST's Algorithm
Testing and Evaluation Program for Coordinate Measuring Systems, which distributes generated point
sets with known reference fits) and the sampling-strategy literature for form-error evaluation
(harmonic roundness modelling verified on real turned and ground profiles; ISO 12181 for roundness,
ISO 14253 for conformance decisions with measurement uncertainty). Those evaluate how accurately a
fitting algorithm reproduces a reference fit on given points, or report a point estimate of form
error. This task scores a calibrated predictive distribution for the true filtered roundness value
under deliberately aliasing sparse probe plans, a conformance probability, and attribution of the
latent machine/set-up signature. None of those three is the NIST ATS task, and none is obtainable by
running a better circle fit.

**2. Closest local/platform semantic cluster, and why originality survives.**
Measured: 0 of 830 archived platform titles and 0 of 823 archived description blocks are about
roundness, flatness, cylindricity, CMM, coordinate measuring, form error, tolerance zones,
conformance decisions, guard banding, GD&T or datum reference frames; the 4 incidental body hits are
in unrelated domains. The nearest *conceptual* archived neighbour is the accepted synthetic
"Hidden Obstacle-Field Reconstruction From Probe-Ball Deflections" (top-down video, ballistic probes,
occupancy grid) — different modality, target and solver family. The challenge description will carry
an explicit cite-and-distinguish paragraph naming it and the metrology literature, which is the
recorded fix for a low novelty score. Registry (86 entries) has no metrology entry; the nearest are
`machine-sensed-cutting-edge-reconstruction` (microscope imagery, blocked) and
`bulk-crystal-slip-system-program-recovery` (crystal plasticity, blocked).

**3. What native artefact supplies every scored field.**
`generate.py` holds the full harmonic field of every feature. RONt is the peak-to-valley of the
least-squares-circle, 15-UPR Gaussian-filtered profile evaluated on a 360-point grid (ISO 12181-2
filter definition); conformance is RONt <= the drawing tolerance; the signature class is the machine
latent that selected the enhanced undulation orders. All three are exact deterministic functions of
generator state. No parser, no heuristic, no model-generated truth.

**4. Usable rows and independent hidden groups after every filter.**
Measured at 160 machines / 2000 parts: 5,928 train and 3,072 test features, over 104 train and
56 test machines and 1,312 train / 688 test parts, with machines disjoint across the split.
Conformance base rate on test 0.516. The corpus is a few MB, so the shipped size scales up freely.

**5. Why every input is necessary. Ablations.**
Metadata only (probe count, nominal size, tolerance) scores 0.037 of 1.0 — the probe readings carry
essentially all the signal. Removing the cross-feature pooling features costs 0.052 (0.654 -> 0.602),
so the part-level alias-fusion axis is real and measurable without being the only signal.

**6. No-op, copied input, empty, one-head-only.**
empty/all-zero 0.000; prior-constant 0.000; a very wide hedging interval 0.006; oracle on one head
only 0.450 / 0.350 / 0.200 (exactly the head weights); perfect 1.000. A copied-input submission that
reports the sparse peak-to-valley as all three quantiles scores 0.332 — this is the naive textbook
point estimate, one rung below the calibrated textbook route (0.492), not a metric-null shortcut;
plain pinball scoring let it reach 0.404, which is why the head was changed to a proper interval
score.

**7. The capable solver most likely to break the task, and its measured score.**
The calibrated standard metrology route: least-squares circle fit, peak-to-valley of the residuals,
an n-conditional empirical expansion factor fitted on the training split, and a conformance
probability from the same empirical ratio distribution. Measured 0.492, which is 0.367 below the
exact achievable ceiling of 0.862.

**8. Can the public source recover hidden answers by exact, fuzzy, geometric, temporal or signal
retrieval?** There is no public source to retrieve: the corpus is generated under a private seed and
exists nowhere else. Measured anyway at the shipped bundle size (one part, 3-6 features, 12-66 probe
points): top-1 source-machine recovery 0.000, nearest-neighbour target-copy attack 0.052 with
q_skill 0.000 and conf_skill 0.000.

**9. Can the exact raw package be imported now, within size and licence rules?**
Yes. The platform supports generated corpora as `generate.py` plus a flat `raw_upload.zip`
(`rules/LATEST.md`). A corpus of this scale is a few MB, far inside the <=2 GB guidance. The only
external dependency is the CC BY 4.0 calibration dataset (Zenodo 7004548), which is cited rather than
redistributed; SHA-256 recorded in `DATA_ACQUISITION.md`.

**10. The single result that would still force rejection.**
If an agent-realistic solver reached the latent-oracle ceiling, the private machine latents would be
identifiable from a released bundle and the headroom would vanish. The measured gap between the
ceiling (0.862) and a plain gradient-boosting route (0.654) is 0.210, so that is not the current
state, but the build must re-measure it on the real prepared split. Secondarily, a platform novelty
score below 5/10 after the cite-and-distinguish paragraph would force a redesign, not a reword.

## Score ladder and stability (answers the recorded "synthetic gives low-variance scoring" warning)

Across three independent corpus seeds: chance floor 0.000 +/- 0.000, copied input 0.295 +/- 0.041,
capability-matched 0.469 +/- 0.024, learned route 0.628 +/- 0.017, perfect 1.000 +/- 0.000. The gap
between the capability-matched and learned rungs (0.16) is about seven times the run-to-run standard
deviation. Blending a submission from the chance floor to the oracle gives a smooth, monotone,
near-linear curve: 0.000, 0.133, 0.258, 0.375, 0.484, 0.590, 0.687, 0.776, 0.858, 0.932, 1.000 —
no flat regions and no nonlinear score suppression.

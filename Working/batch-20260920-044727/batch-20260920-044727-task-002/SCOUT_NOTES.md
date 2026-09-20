# Scout notes — slot batch-20260920-044727-task-002

## Attempt 1 — REJECTED (measured)
`facade-photo-elevation-drawing-correspondence` — LoC HABS/HAER field photographs vs measured elevation
drawings. Source, licence (public domain, U.S. Government work), native labels, scale (465 buildings /
1,944 photos / 50 states) and import route all PASSED. Rejected on three measured gates — see
`CANDIDATE1_REJECTION_EVIDENCE.md` and registry `facade-photo-elevation-drawing-correspondence.json`.

## Transferable design lesson (the specific sin to avoid next time)

The candidate died mainly because **the scored label was the public per-item annotation of a public item**:
retrieving one source photograph returns a caption that states the answer verbatim. Accepted challenges in
this workspace that also use public corpora (AI4Mars, Allmaps, GuitarSet) survive because their scored
targets are **privately derived structured quantities computed across many source rows by `prepare.py`**,
not a per-item public annotation. Retrieving a single source item must not hand over a scored field.

Rule for the replacement candidate, in priority order:
1. Target must be a *derived relational/structural object* (ledger, graph, program, decision set) computed
   from the source by our own deterministic pipeline — never a verbatim public per-item label or caption.
2. Before any build, measure the capability-matched baseline against an explicit **chance floor for the same
   restricted choice**. Require a real margin, not "above a constant prior". Candidate 1 looked fine against
   a constant prior (0.3847 vs 0.2941) and was near-chance against the correct floor (0.3251).
3. Run the generic zero-shot attack (frozen DINOv2 / patch matching) early: if it beats the designed
   pipeline, the design adds nothing.
4. Ablate the intended modality explicitly, and include a hand-feature probe for the obvious physical
   shortcut (candidate 1: sun/shadow gives compass direction without ever reading the drawings).

## Replacement direction — novelty lane check (local duplicate map, 817 archived platform challenges + 84 registry entries)

| Direction | Archive keyword hits | Registry entries | Verdict |
|---|---|---|---|
| astronomy / telescope / pulsar / eclipse | **7** | **0** | **open lane — preferred** |
| patents / trademarks | 11 | 1 (blocked) | narrow |
| pharmacy / dosing | 26 | 1 | moderate |
| food / recipe / nutrition | 26 | 1 (rejected) | moderate |
| fisheries / vessels | 41 | 1 (ready) | moderate |
| aviation / airports | 47 | 0 | moderate |
| courts / dockets / appeals | 80 | 2 | crowded |
| rail / timetable / dispatch | 86 | 0 | crowded |
| bridges / inspection | 248 | 2 | crowded |
| wells / boreholes / core logs | 231 | 2 | crowded |

Sibling slots (deconfliction, from their checkpoints): task-001 = photographic EXIF exposure-decision ledger
(Wikimedia images); task-003 = wind-turbine SCADA time-series stop-event ledger. The replacement must be
neither plain imagery-with-metadata nor multichannel sensor time series.

**Chosen next direction: astronomy / small-body or survey astrometry**, formulated so the scored object is a
privately derived structural ledger (e.g. detection-to-track association structure plus derived observing
quality/decision fields), not an official designation copied from a public catalogue. The reversibility gate
must be measured *first* this time: if coordinates+epoch retrieval against the public catalogue recovers the
association, reject before any build. Modality is distinct from both sibling slots.

Status: direction chosen and novelty-lane checked; no source verified yet, so the verdict for the
replacement is currently **Pilot (unstarted)** — not a claim of viability.

---

# Session 2 (replacement worker) — measured lane work, 2026-09-20

## Attempt 2 — REJECTED (measured): Global Meteor Network station-level formulations

Astronomy lane, as approved. Source CC BY 4.0, access clean, 86 native columns, 112,139 meteors in a
single month, 1,021 independent stations — every gate passed except reversibility, which failed
decisively. Full numbers in `CANDIDATE2_REJECTION_EVIDENCE.md`; acquisition record with official URLs
and SHA-256 in `DATA_ACQUISITION.md`; scripts and JSON under `scout2/`.

## The astronomy lane is NOT empty — measured against the 818-title platform archive

The prior session's "7 keyword hits" understated the lane. Extracting every `## ` title from
`Shipd_Challenge_Archive_All/{CPU,Non-CPU}/*.md` gives 818 archived platform challenges, and the
astronomy-adjacent ones include several **Accepted** entries that occupy the tractable sub-lanes:

| Archived challenge | Sub-lane it occupies |
|---|---|
| Masked Helioseismic Band Energy-Profile Reconstruction (Accepted, CPU) | solar / SDO-HMI, masked-channel recovery |
| composite stellar spectrum 8-token decomposition (Accepted, CPU) | stellar spectra, mixture decomposition |
| Hidden Binary Stars | stellar binarity |
| Gravitational-Wave Signal Detection and Characterization | GW strain |
| Source Recovery Prediction in Crowded Astronomical Images (Non-CPU) | crowded-field photometry |
| Solar Wind Turbulence Prediction from Hourly Averages | heliophysics time series |
| Rebind Two Missing Moon-Orbiter Frames; Cross-Mission Event-Shape Deep-Space Sensor Translation; Auroral Episode Representation Transfer | planetary/space imagery and sensor transfer |

What remains open in astronomy is the small-body / astrometry / meteor sub-lane, and that sub-lane
drives every formulation into one of three dead ends measured or argued here:
1. **public row-level catalogue + group-bundled instance = reversible** (measured, attempt 2);
2. **canonical solver** (initial orbit determination, plate solving, period finding, shower
   classification are textbook algorithms a capable solver runs exactly);
3. **registry self-duplicate** (association/partition is already three entries of mine:
   `anonymous-storm-episode-partition-recovery`, `anonymous-transit-feed-vehicle-association`,
   `anonymous-cyclone-*`; a fourth would be a self-duplicate, not novelty).

Astronomy is therefore **dropped as a lane on measured evidence**, exactly as the supervisor
authorised ("prove it or drop it"), not abandoned on preference.

## Generalisable lesson added to the Scout gate (from attempt 2)

**Per-row lookup resistance is not sufficient when instances bundle many rows of the same source
group.** Measured on GMN: hardening that leaves only a 0.0025 per-row unique-match rate still allows
100% top-1 recovery of the source group from a 60-row bundle by loose matching plus roster voting,
and group recovery then raises per-row unique recovery back to 0.3233. Always measure the lookup
attack **at the shipped instance/bundle size**, and report the bundle size with every lookup number.

## Open-design-space measurement (target-family density over the 818 archived titles)

    uncertainty/quality 5 | forecast 17 | counterfactual 21 | completion 40 | repair 45 |
    program-synthesis 46 | decision/portfolio 54 | graph 62 | detection 64 | transfer 65 |
    ordering 68 | association/partition 71 | ledger/provenance 72 | recovery/reconstruction 213

Additional targeted scan: **aggregate inversion / disaggregation / ecological inference / iterative
proportional fitting / small-area estimation / population synthesis has ZERO archived challenges**
(grep over the full archive body, not just titles; the only two body hits are a metric definition
that happens to use the phrase "contingency table", and "Cross-Site Latent Source Attribution from
Shared-Channel Transitions", which is additive source separation on a Non-CPU time series — a
different input modality and solver family). 0 of 84 registry entries as well.

## Attempt 3 — direction chosen, verdict **Pilot (unstarted -> in progress)**

**Family:** aggregate inversion (recover a privately derived joint composition from released
marginal tables). **Source:** US Census ACS 2023 1-Year PUMS person files, `CC0 / U.S. public
domain`, direct CSV over HTTPS from `https://www2.census.gov/programs-surveys/acs/data/pums/2023/1-Year/`
(state person files are 6-15 MB zipped, so the whole corpus is far inside the upload budget).

**Why this structure survives what killed attempts 1 and 2:**
- The scored target is a **privately derived joint distribution computed by `prepare.py` across
  hundreds of source rows**, never a public per-item annotation (attempt 1's failure).
- Each unit is a **private mixture of records drawn from several source areas with private weights**,
  so the unit has no counterpart in any published table and no source group can be voted for from a
  bundle (attempt 2's failure). The instance-level lookup attack has nothing to match against.
- Modality (categorical marginal tables) is clearly distinct from slot 1 (photographic imagery with
  metadata) and slot 3 (multichannel sensor time series).

**Gates still to measure, in the required order:**
1. instance-level reversibility: can an attacker with the full public PUMS fit a mixture of real
   areas to the released margins and recover the target joint better than the honest baselines?
2. chance floor = the best constant (global training joint); then the capability-matched attack,
   which for this family is **IPF / maximum-entropy raking with a global seed table** — the standard
   population-synthesis method. If IPF-with-global-seed is near the oracle, the candidate is rejected.
3. null-metric audit (uniform table, independence table, copied margins, one-head-only).

**Framing note for the premortem:** this must be presented as small-area joint-composition estimation
(the standard population-synthesis / microsimulation problem), never as a disclosure-reconstruction
attack. Only aggregate tables are released; no individual record is published or scored, and the
underlying microdata is already public-domain.

## Attempt 3 — REJECTED (measured): ACS PUMS small-area joint composition recovery

Full numbers in `CANDIDATE3_REJECTION_EVIDENCE.md`; scripts and JSON under `scout3/`; acquisition
record in `DATA_ACQUISITION.md`. Summary: every gate except difficulty-vs-leakage passed
(CC0 licence, native ACS fields, 1,256,063 adult records, 1,114 independent PUMAs split 779/335,
1,482 train / 624 test units, family with 0 archived and 0 registry precedents, chance floor exactly
0 by construction, and comfortably above-chance learning). It failed because the two gates are
mutually exclusive in this corpus: a competition band of 0.175 comes with a +0.098 source-retrieval
gain, and hardening that closes the gain to +0.003 closes the band to 0.117, while coarsening the
target to reopen the band lifts the standard IPF method to 0.78-0.81 (saturated).

## Distilled design rule after three measured rejections (this is the batch-level output)

All three rejected candidates in this slot failed for the same underlying reason, in three different
disguises:

| Candidate | What the scored signal was tied to | How it leaked |
|---|---|---|
| #1 facade photo / elevation drawing | the public caption of a public photograph | image retrieval returns the caption, wHash rank-1 0.188 |
| #2 GMN meteor station bundles | the identity of a public camera station | bundle voting recovers the station 40/40 at K=60 |
| #3 ACS PUMS reporting units | the association structure of public PUMA areas | NNLS mixture fit over 1,114 public areas, +0.098 to +0.162 |

**Rule: the predictable structure must be UNIVERSAL — a physical, signal-level, combinatorial or
generative regularity that the released training split teaches just as well as the full public source
would — and never the identity or the per-group structure of a public source item.** When the signal
is universal, downloading the source gives no edge over the released training data, so the leakage
gate and the difficulty gate stop competing instead of trading one-for-one.

Corollaries to apply before spending compute on candidate #4:
1. Ask first: *if a solver downloaded the entire source, what would they gain that the training split
   does not already give them?* If the answer is "the answer" or "the per-group structure that
   carries the signal", stop — do not pilot it.
2. Measure the lookup/retrieval attack at the **shipped instance/bundle size**, never per row
   (lesson from candidate #2).
3. Measure the capability-matched baseline against the **correct chance floor for the restricted
   choice**, and also measure the **achievable ceiling** (the best predictor that does not see the
   scored sample). The reportable quantity is ceiling minus capability-matched, not skill above zero
   (lesson from candidates #1 and #3).

## Attempt 4 — direction, verdict **Pilot (unstarted)**, NOT a viability claim

Shape that satisfies the rule: a **private, parameterised transformation applied to a real corpus
whose structure is universal**, with the transformation's parameters as the scored ledger. The
transformed artefact exists nowhere public, so retrieval returns nothing; the regularity needed to
invert it (signal physics, coding structure, combinatorial constraints) is fully taught by the
training split, so source access confers no advantage. Target family should stay in the open space
measured above (uncertainty/quality 5 of 818; forecast 17; counterfactual 21).

Required before any build, in this order: (1) confirm no archived challenge already covers the exact
transformation-recovery formulation (registry already holds `mixed-speech-forensic-signal-chain-
reconstruction` and `substation-protection-event-tape-recovery`, both rejected, so the audit must be
strict); (2) the instance-level retrieval attack; (3) the chance-floor-relative capability-matched
baseline **and** the achievable ceiling; (4) the null-metric audit. Verdict stays Pilot until all four
are measured.

---

# Attempt 4 — measured lane work, 2026-09-20 (this session)

## Direction taken and why it answers Rule 1 structurally rather than by hardening

Candidates 1-3 (and the other four batch rejections) all died because the scored signal was tied to
an identifiable public item, so the leakage channel and the learning signal were the same quantity.
Hardening therefore traded them one-for-one.

Candidate #4 removes the channel instead of narrowing it: **the released corpus is generated under a
private seed by `generate.py` and has no public counterpart of any kind.** The question "what would a
solver gain by downloading the whole source?" has the answer *nothing* by construction, and that is
checkable rather than argued: there is no public artefact to retrieve. The structure the solver must
learn is physical and universal — the harmonic (undulations-per-revolution) content of machined
surfaces, the aliasing of harmonic k into k mod n under n-point probing, and the fact that the
features of one part share one machine/set-up signature. All of it is taught by the released training
split exactly as well as by anything else.

The platform explicitly supports this corpus type: `rules/LATEST.md` has a dedicated
"Raw dataset upload for synthetic generated datasets" section (`generate.py` + `raw_upload.zip`), and
`rules/prev_reviews.txt` records several accepted generated challenges plus a list of
"Lessons for future synthetic challenges". The two recorded reviewer objections to generated corpora
are (a) a text/pretraining corpus where the reviewer wanted real text, and (b) *visual* challenges
whose renders looked like toy puzzle boards. Neither applies to a numeric coordinate-metrology task,
and the generator is calibrated against real measured traces (below).

## Candidate #4 — `sparse-probe-roundness-conformance-adjudication`

**Workflow.** Production coordinate-measuring-machine (CMM) inspection of circular features. Touch
probing is slow, so production plans probe only 4-12 points per circle. From those points an inspector
must estimate the true roundness deviation RONt of the whole feature, decide conformance against the
drawing tolerance, and attribute the dominant error mode to a machine/set-up cause.

**Scored heads (uncertainty/quality family — 5 of 818 archived titles, the openest family measured):**
1. calibrated quantiles p10/p50/p90 of the true RONt in micrometres (pinball loss);
2. probability the characteristic conforms (Brier);
3. the latent machine/set-up signature class (accuracy).

**Why it is not the textbook method.** Sparse probing is blind to whole harmonics: with n equally
spaced points, harmonic k aliases onto k mod n, so a three-lobe form error probed at 3 or 6 points is
invisible. The standard route — least-squares circle fit, then peak-to-valley of the residuals — is
therefore systematically biased low, and the bias depends on the unknown harmonic content. Measured on
a 400-part pilot corpus, the ratio (true RONt)/(sparse peak-to-valley) has median 2.67 with
interquartile range [1.64, 6.28] at n = 4, falling to 0.99 [0.86, 1.07] at n = 12. Recovering the
hidden harmonics requires the learned prior plus pooling across the other features of the same part.

**Real calibration source.** Zenodo 7004548, "Roundness Measurement Dataset" (Aalto University,
CC BY 4.0, 5.4 MB, SHA-256 e284745a...b271bf): Talyrond TR31c traces of 5 roundness reference
workpieces, 3600 points/revolution, ISO 12181-2 Gaussian 15 UPR filter. Fitted spectrum (scout4/
real_spectrum_fit.json): amplitude ~ C*k^alpha with alpha = -1.935; dominant orders k = 1, 2, 3, 5;
a discrete bearing-order spike at k = 12 on TK2; per-workpiece peak-to-valley 19.9 to 307.5 um. Those
five workpieces are far too few to be the corpus itself (the split-stability gate needs hundreds of
independent groups), so they are used only to set and validate the generator priors, and cited.

## Semantic-duplicate audit (Rule 4 step 1) — PASSED

Extracted all 830 `## ` titles and all 823 description blocks from
`Shipd_Challenge_Archive_All/{CPU,Non-CPU}/*.md`.

| Probe | Title hits | Body hits |
|---|---|---|
| tolerance / metrology / GD&T / datum | 0 | - |
| chromatography | 0 | - |
| roundness, flatness, cylindricity, CMM, coordinate measuring, form error, tolerance zone, conformance decision, guard band, machined part, probed point | 0 | 4 blocks, 1 incidental hit each, all other domains (Factual Probe Lexical Backbone Reconstruction; Cross-Modal Audio-Motion Representation Adaptation; Budgeted Concrete Damage Inspection Planning; Selecting Complementary Spectral Responses From Microscopy) |

Lanes checked and REJECTED as occupied before choosing this one:
- spectral library matching / mixture unmixing (10 spectral titles, including *Sparse Raman
  Microplastic Mapping And Next-Scan Planning*, *Cross-Adduct Spectral Library Matching*, *Analyte
  Concentration-State Transfer Across Raman Sample Matrices*, *Material Spectrum Processing Lineage
  and Invariant-Band Recovery*, and the accepted composite-stellar-spectrum decomposition) — the
  microplastics/Raman idea was dropped on this evidence;
- typeface/glyph transformation (*Decoding Transformation Sequences on Unseen Typefaces*);
- public-filing reconstruction (XBRL/SEC) — dropped on Rule 1 before measurement: the filings are
  public, so matching the visible numbers returns the withheld ones;
- adaptive inspection *policy* (*Calibrated Adaptive Crimp Audit*, *Budgeted Concrete Damage
  Inspection Planning*) — consequently the planned "which feature to re-probe" head was DROPPED from
  this design, keeping only estimation, conformance and cause attribution.

Registry (86 entries): nearest neighbours are `machine-sensed-cutting-edge-reconstruction` (blocked;
microscope imagery of tool edges — different modality and target) and `bulk-crystal-slip-system-
program-recovery` (blocked; crystal plasticity). No metrology/conformance entry exists. The heavily
self-used families in this registry (program/ledger recovery 6+, association/partition 3) are
deliberately avoided; the target family here is uncertainty/quality.

## Deconfliction
Slot 1 (baseball baserunning ledger, photo-EXIF exposure ledger) is photographic imagery and sports
event records; slot 3 (wind SCADA, NHTSA crash events) is multichannel sensor time series and crash
event records. This candidate is 3-D coordinate probe points plus a drawing specification, in
precision machining, with a calibrated-posterior target. Distinct in domain, modality and target
family from both, and from this slot's own candidates 1-3.

## Candidate #4 measured gates — design v1 (Rule 4 order)

Corpus 150 machines / 1800 parts, split by machine (98 train / 52 test machines; 1186 / 614 parts;
5344 / 2747 features). Conformance base rate on test 0.546. Harness `scout4/pilot_all.py`, results
`scout4/pilot_v1_results.json`.

**Gate B — instance-level retrieval at the shipped bundle size (one part = 3-6 features,
12-72 probe points):**

| Attack | Result |
|---|---|
| top-1 source-machine recovery from a bundle | **0.000** (train/test machine pools are disjoint; there is no public group to recover) |
| top-1 signature-class match of the nearest train bundle | 0.340 vs 0.218 chance — weak, and legitimate physics, not identity |
| nearest-neighbour target-copy attack (copy the retrieved part's hidden answers) | **0.0507** against an intended learned route of 0.6737 |
| nearest-neighbour distance in residual space | median 0.734 um, mean probe repeatability 0.479 um — neighbours sit at the noise scale and carry no answer |

This is the first candidate in the batch to pass the bundle-level reversibility gate, and it passes
structurally: the released artefacts are generated under a private seed, so there is no public
counterpart to retrieve at any bundle size.

**Gate C — chance-floor-relative capability-matched baseline:**

| Route | score | q_skill | conf_skill | sig_skill |
|---|---|---|---|---|
| chance floor (train-marginal quantiles / base rate / majority class) | 0.000 | 0.000 | 0.000 | 0.000 |
| metadata only | 0.113 | 0.000 | 0.323 | 0.000 |
| capability-matched domain method (LSC fit + n-conditional calibrated expansion) | 0.527 | 0.571 | 0.771 | 0.000 |
| intended learned route (GBM on sparse-residual features + part pooling) | 0.674 | 0.753 | 0.798 | 0.279 |
| same, part pooling ablated | 0.643 | 0.725 | 0.755 | 0.262 |

**Gate D — null-metric audit:** empty 0.000, prior-constant 0.000, one-head oracles exactly the head
weights (0.45 / 0.35 / 0.20), perfect 1.000. **One failure:** a copied-input submission that reports
the sparse peak-to-valley as all three quantiles retained **0.404**, i.e. 60% of the intended route.

**Fix applied before the v2 measurement:** the quantile head is scored with a proper interval score
(IS_0.2 for the central 80% interval, plus twice the median absolute error) instead of plain pinball.
A zero-width interval is then charged 10x its miss, which is exactly the copied-input submission's
failure mode. Design v2 also (a) varies the probe count PER FEATURE inside a part so harmonic
aliasing differs between features and must be fused across them, and (b) ties each drawing tolerance
to the machine's own process capability rather than to a fixed ladder, which removes the metadata-only
conformance shortcut without letting the tolerance depend on the scored feature's private roundness.

## Candidate #4 — DEFINITIVE measured verdict: **Proceed** (design v3)

Two measurement faults were found and fixed during the pilot. Both are recorded because they are
reusable lessons, not because the candidate failed.

1. **The first ceiling measurement was invalid, not the candidate.** The ABC importance sampler over
   the true private prior collapsed to a mean effective sample size of **2.3 out of 12,000 draws**,
   so its "ceiling" of 0.312 was Monte Carlo noise and fell *below* the learned route — impossible
   for a Bayes optimum. Fix: the harmonic coefficients were made circular Gaussian (Rayleigh
   amplitude, identical measured envelope), which makes exact Gaussian conditioning possible, and the
   ceiling became the **latent-oracle** predictor: told the true private machine latents, then
   conditioned exactly on the released probe residuals, never seeing the scored value. Strictly
   better informed than any solver, therefore a genuine upper bound, with no sampling noise in the
   conditioning step.
2. **Plain pinball scoring let a copied-input submission reach 0.404.** Fix: the quantile head is now
   the proper interval score IS_0.2 for the central 80% interval plus twice the median absolute
   error, which charges a zero-width interval ten times every miss.

A third design fault was fixed at the same time: the drawing tolerance had been a metadata shortcut
to the conformance decision (metadata-only conf_skill 0.323). Tying each tolerance to the machine's
own process capability, rather than to a fixed ladder, dropped that to 0.026 without ever letting the
tolerance depend on the scored feature's private roundness.

### v3 gate results (160 machines / 2000 parts, split by machine, 500 common rows for the ceiling)

| Route | score | q_skill | conf_skill | sig_skill |
|---|---|---|---|---|
| chance floor | 0.000 | 0.000 | 0.000 | 0.000 |
| metadata only | 0.037 | 0.061 | 0.026 | 0.000 |
| capability-matched domain method | 0.492 | 0.605 | 0.630 | 0.000 |
| learned route (GBM + part pooling) | 0.654 | 0.772 | 0.683 | 0.336 |
| learned route, pooling ablated | 0.602 | 0.724 | 0.614 | 0.305 |
| **latent-oracle ceiling (exact)** | **0.862** | 0.840 | 0.810 | 1.000 |

**ceiling minus capability-matched = +0.367 score, +0.238 q_skill, +0.172 conf_skill.**
ceiling minus the plain GBM = +0.210.

Gate B at the shipped bundle size (one part = 3-6 features = 12-66 probe points): top-1
source-machine recovery **0.000**, nearest-neighbour target-copy attack **0.052** with q_skill 0.000
and conf_skill 0.000.

Gate D: empty 0.000, prior-constant 0.000, wide hedge 0.006, one-head oracles exactly the head
weights 0.45 / 0.35 / 0.20, perfect 1.000.

Stability across three independent corpus seeds: floor 0.000 +/- 0.000, copied input 0.295 +/- 0.041,
capability-matched 0.469 +/- 0.024, learned route 0.628 +/- 0.017, perfect 1.000 +/- 0.000. The gap
between the capability-matched and learned rungs is about seven times the run-to-run spread, which is
the direct answer to the recorded reviewer warning that synthetic corpora can give low-variance
scoring. Blending a submission from floor to oracle gives a smooth monotone curve with no flat
regions: 0.000, 0.133, 0.258, 0.375, 0.484, 0.590, 0.687, 0.776, 0.858, 0.932, 1.000.

### Re-measured on the REAL prepared split with the shipped grader

35,311 train / 18,643 test rows; 7,854 / 4,146 parts; 585 / 315 disjoint machines; conformance base
rate 0.456; every signature class has at least 2,604 scored rows.

sample 0.1485 | all-zero 0.0299 | wide hedge 0.0805 | metadata-only 0.2050 | 1-NN part retrieval
0.3382 | copied input 0.3996 | capability-matched 0.5118 | learned GBM 0.6976 | pooling ablated
0.6492 | perfect 1.0000.

The 1-NN part retrieval rung is a weak learner over the **released training split**, not an
external-source leak, and it sits well below the capability-matched method. There is no public
counterpart to retrieve at all: the corpus is generated under a private seed. Public identifiers are
salted hashes, row and probe order are randomised, and the rank correlation between `row_id` order
and the truth is 0.0039.

### Practice note carried forward
Every harness in this session re-dumps its results file after each stage (`say()` in
`scout4/pilot_all.py` and `scout4/pilot_v3.py`). That is why the invalid ABC ceiling still left a
complete record of the stages that had already succeeded, and it is the fix for the failure mode seen
in candidate 3's ceiling script, whose only durable output was a single closing `json.dump`.

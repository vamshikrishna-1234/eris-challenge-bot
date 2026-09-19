# Non-CPU From Scratch Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed Non-CPU examples in this document: 78

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.

## Cross-Session Aphid Species Recognition

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74yhg0rc4p0fx31c7a2gmksx8bhvjn
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> The instrument that made this data does not listen. An LED array shines across a small flight chamber and a photodiode watches the light on the far side. When an insect flies through, its body and beating wings cast a moving shadow, and the flicker of that shadow, wings crossing the beam hundreds of times a second, is what gets recorded. The trace looks like audio, 8,000 samples a second, but it is a record of how much light was blocked, moment by moment. What survives in it is the wingbeat frequency and the silhouette the wing sweeps, and those differ between insects.
> You are given 0.625 seconds of that trace for a single free flight, and must name which of four aphid species it was. They are the hard, fine-grained half of the problem, and the half that matters: each is a distinct carrier of a different plant virus, so a trap that could name the aphid crossing it would be announcing which virus has arrived, not just "an aphid". Their flight traces are genuinely close, and the four are wildly unequal in number, one of them about thirty times as common as the rarest.
> The difficulty is not only the signal. It is that a recording betrays where it was made.
> Each colony was flown on its own days, so the sitting is nearly the answer. Recordings made in one session share a colony, an insect batch, and the chamber's condition that day. A model that keys on any of that scores high on recordings from sessions it trained on and collapses on new ones. So the split holds whole sessions out: the sessions you are scored on were never in training, and only something genuinely about the insect, not its sitting, carries over. The obvious session-fingerprint cues have already been removed from the data: no timestamp, no temperature, no humidity. Measured on the source's insects, a simple model given only those two temperature and humidity numbers, with no signal at all, could name the insect well above chance purely by memorizing which sitting a recording came from. They are gone. Only the trace remains.
> The counts are very uneven, and that is the point. The commonest aphid appears about thirty times as often as the rarest. The imbalance is real to the problem, and because the score weights each species equally, a model that quietly collapses to naming only the common one is punished hard by the three rare ones.
> Task
> For every recording_id in test.csv, predict the aphid. The label is one of exactly these four common names, spelled as here: sycamore aphid, grain aphid, black bean aphid, maple aphid. One label per flight.
> Data
> All inputs are under dataset/public/.
> train_waveforms.npy: a float32 array of shape (N, 5000), flight by sample. 5,000 samples is 0.625 s at 8 kHz. Load with numpy.load(..., mmap_mode="r").
> train.csv: one row per training flight. Columns:
> recording_id (string): the flight.
> window (int): its row index into train_waveforms.npy.
> label (string): the aphid's common name, one of four.
> test_waveforms.npy and test.csv: the same, over the test flights, with no label.
> sample_submission.csv: a correctly formatted submission for every test flight, at chance.
> Training and test flights come from entirely separate recording sessions, and all four aphids are present in both. Each trace is re-derived rather than copied: it is normalised, given a small time warp, an amplitude scale and low-amplitude noise, so a published flight is not value-identical to any public recording, while the wingbeat frequency and the wing silhouette are preserved.
> Evaluation
> Submissions are scored by macro-averaged F1 over the four aphids, the mean of the per-species F1 scores, so the rarest counts as much as the commonest and predicting one label for everything cannot win:
> for each aphid L:   F1_L = 2*TP / (2*TP + FP + FN)
> score = mean(F1_L over the four aphids)                         (higher is better, 0 to 1)
> Measured on this exact session-held-out split: predicting one aphid for everything scores about 0.12, the supplied random sample about 0.21, and a class-balanced gradient-boosted model over the log-spectrum of the trace, the reference here, reaches about 0.36. A deep model trained on the raw trace that reads the wingbeat and wing shape, holds up on sessions it never saw, and does not abandon the rare species, has room above that, and the distance to 1.0 is the challenge.
> Submission format
> Write ./working/submission.csv with exactly these columns:
> recording_id,label
> f_1a2b3c4d5e6f,sycamore aphid
> f_2b3c4d5e6f7a,maple aphid
> ...
> One row per recording_id in test.csv, and no others. A submission that omits a flight, repeats one, or names an unknown one is rejected.
> label is one of the four common names in train.csv.
> Start from sample_submission.csv to guarantee the correct id set, and write with index=False.
> Constraints
> Read the challenge inputs only from ./dataset/public/. Write your output only to ./working/submission.csv.
> One A10G GPU (24 GB), plus CPU cores and 62 GB of memory, and a hard limit of 1.5 hours for the whole run. The traces are short, so a model over the raw signal trains comfortably in that budget; the reference itself finishes in a couple of minutes.
> Train from scratch. No pretrained weights of any kind. Do not download a checkpoint from a model hub and do not initialise from anything trained elsewhere. Every parameter you use must be fitted on the provided training flights. Nothing is pretrained on light-extinction traces, and learning the representation is the point.
> No package installs (no pip or conda install). You may use the preinstalled libraries (numpy, scipy, pandas, scikit-learn, pytorch, and so on).
> What Not To Use
> Do not try to identify the source recordings or look up their insect from any public archive. The timestamp, temperature and humidity were removed and the traces re-derived for exactly this reason. Decide from the provided signal.
> Do not hardcode outputs or otherwise bypass learning from the data.
> A learning-based approach is expected, on the raw trace. The wingbeat frequency and its harmonics sit in the spectrum, and the amplitude envelope carries the insect's size and the shape of the wing's passage through the beam. Features of those, or a small model trained on the raw signal, is the natural line of attack. The real test is that it must generalise to sessions it has never seen, and must not quietly collapse to naming only the commonest aphid while ignoring the three rare ones, which the score weights just as heavily.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Twin-Trace Motor Controller Program Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70kp93pbmqqbtkr4tdp60zj58bk8wk
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Twin-Trace Motor Controller Program Recovery
> Overview
> Motor and cooling-fan controllers are often commissioned once and then operated
> for years. A configuration fault can alter several controller settings while the
> original source program is no longer available. The surviving evidence may be a
> healthy commissioning trace, a new faulty service trace, and the broken program
> currently installed on the drive.
> Your task is to recover the six-token controller program that produced the
> healthy behaviour. Each case contains two aligned-length multichannel traces:
> a healthy commissioning run whose direct PWM channel is withheld; and
> a faulty service run whose PWM channel and broken program are visible.
> The two runs use different reference and load profiles on the same hidden plant.
> This prevents direct sample subtraction. A useful system must identify temporal
> response characteristics, compare the two control regimes, and decode a valid
> controller program.
> The benchmark is derived deterministically from the 2026 OpenMCT physical DC
> motor measurements. Preparation fits bounded plant prototypes to separate
> acquisition logs and then performs closed-loop simulations. The simulated
> benchmark cases are not represented as additional physical measurements.
> Cooling-fan drives use the same PWM motor-control structure, but the source
> bench itself is a DC motor.
> Task
> For every test case_id, generate exactly one program:
> KP_nn KI_nn AW_nn SL_nn FL_nn UP_nn
> The fields are:
> KP: proportional-gain code, 00 through 15.
> KI: integral-gain code, 00 through 15.
> AW: anti-windup code, 00 through 04.
> SL: command slew-limit code, 00 through 04.
> FL: measurement-filter code, 00 through 04.
> UP: controller update-period code, 00 through 02.
> Fields and token order are fixed. Codes are absolute recovered settings, not
> offsets from the broken program.
> Dataset
> Files
> train.csv - 6,000 labeled cases.
> test.csv - 1,000 held-out cases without repair_program.
> train_sequences.npz - training tensors and integer program codes.
> test_sequences.npz - test tensors and visible integer codes.
> sample_submission.csv - random valid programs in the required format.
> CSV columns
> case_id string) - opaque 16-character case identifier.
> requirement_json JSON object) - operating-context classes for response,
> current budget, smoothness, and sensor noise.
> broken_program string) - the six-token program installed during the
> faulty service run.
> repair_program string, train only) - the original healthy program to
> recover.
> NPZ arrays
> Rows in each NPZ file are sorted by case_id, matching the corresponding CSV.
> case_id - shape (N,), case identifiers.
> trace - shape (N, 256, 10), float16.
> broken_codes - shape (N, 6), integer codes for broken_program.
> requirements - shape (N, 4), integer operating-context codes.
> target_codes - shape (N, 6), training only.
> The ten trace channels are:
> | Index | Channel |
> |---:|---|
> | 0 | healthy reference |
> | 1 | healthy measured speed |
> | 2 | healthy current |
> | 3 | healthy saturation indicator |
> | 4 | faulty reference |
> | 5 | faulty measured speed |
> | 6 | faulty current |
> | 7 | faulty PWM |
> | 8 | faulty saturation indicator |
> | 9 | normalized time |
> The healthy PWM channel is intentionally absent. The number of differing
> program fields is variable by case: every row has exactly four or exactly five
> of the six fields changed, never any other count. Target code frequencies are
> balanced independently of the public operating-context metadata.
> Physical code grids
> KP_nn = 0.08 + 0.08 * nn
> KI_nn = 1.5 + 1.1 * nn
> AW = [0.00, 0.10, 0.25, 0.50, 0.80]
> SL = [0.015, 0.030, 0.060, 0.120, 0.250]
> FL = [0.00, 0.25, 0.50, 0.75, 0.90]
> UP = [1, 2, 4] base control steps
> The train/test split is disjoint by the physical acquisition log used to fit the
> plant prototype. No source acquisition family contributes cases to both splits.
> Evaluation
> The grader parses the submitted program and applies it to three private
> 384-step reference/load rollouts on the case's hidden plant. It also executes
> the true program on the same rollouts. This allows functionally equivalent
> repairs to receive substantial credit.
> For each rollout:
> trajectory_similarity =
> exp(
> -11.0 * MAE(pred_speed, true_speed)
> - 1.8 * MAE(pred_current, true_current)
> - 0.8 * MAE(pred_pwm, true_pwm)
> )
> Let trajectory be the mean similarity over the three rollouts:
> trajectory_skill = trajectory ** 2
> The control cost for one rollout is:
> control_cost =
> tracking_MAE
> + 1.8 * overshoot
> + 0.8 * current_excess
> + 0.20 * mean_absolute_PWM_change
> The current budget is 0.95 - 0.12 * current_budget_class. For each rollout,
> regret = max(0, predicted_cost - true_cost). Then:
> quality = mean(exp(-7.0 * regret))
> quality_skill = clip((quality - 0.72) / 0.28, 0, 1)
> field_accuracy = mean(predicted_code == true_code over six fields)
> exact_program = 1 if all six codes are exact, otherwise 0
> row_score =
> 0.75 * trajectory_skill
> + 0.10 * quality_skill
> + 0.10 * field_accuracy
> + 0.05 * exact_program
> score = mean(row_score)
> Higher is better. The score is bounded from 0 to 1.
> Submission
> Submit a UTF-8 CSV with exactly these columns:
> case_id,repair_program
> 0a12bc34de56f789,KP_04 KI_11 AW_02 SL_03 FL_01 UP_00
> 1b23cd45ef67089a,KP_09 KI_07 AW_04 SL_01 FL_03 UP_02
> Requirements:
> Include every test case_id exactly once.
> Do not include unknown or duplicate IDs.
> Use exactly six single-space-separated tokens in the documented order.
> Use two decimal digits in every token.
> Every code must be within its field's valid range.
> Compute and Modelling Requirements
> This is a GPU from-scratch sequence-modelling challenge. The execution
> environment provides GPU compute. A submitted solution must train at least one
> temporal neural component from random initialization on
> train_sequences.npz, and that component must contribute to the final
> predictions. Temporal CNNs, recurrent networks, Transformers, and state-space
> models are all valid. Controller-aware analytic features, system
> identification, constrained decoding, and ensembling may be combined with the
> learned temporal component.
> Prohibited Resources and Methods
> No external motor, fan, control-trace, or controller-tuning dataset.
> No pretrained sequence, time-series, control, or foundation-model weights.
> No hosted model API, remote inference service, or network retrieval at run
> time.
> No matching against an external copy of the OpenMCT source archive.
> No hardcoded test-ID programs, row-order rules, cached answers, or private
> plant parameters.
> No generator inversion, grader exploitation, filesystem side channel, or
> probing of private rollouts.
> A rule-only, lookup-only, search-only, or classical tabular model without a
> trained temporal neural component is not a compliant primary solution.
> Everything learned by the submitted system must come from the provided public
> training cases.
> Expected Output
> The solution script receives the public dataset directory and exact output CSV
> path as two positional arguments:
> python [solution.py](http://solution.py) <public_dir> <submission_out>

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Molecular Stratification of Brain Tumors from H&E Patch Bags

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70t04sfp45ygb29h4bztf8nd8a2mg5
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> GliomaImmunoStratify — Molecular Stratification of Brain Tumors from H&E Patch Bags
> Overview
> Each example is a bag of H&E histopathology patches tiled from one patient's diffuse-
> glioma whole-slide image. From the bag, infer the patient's tumor molecular class — the
> information that stratifies patients for brain-tumor immunotherapy:
> idh_wildtype — the probability that the tumor is IDH-wildtype. IDH-wildtype gliomas
> (typically glioblastoma) are the aggressive, "immunologically active/target" group enrolled
> in most glioblastoma immunotherapy trials; IDH-mutant gliomas are the immunologically "cold"
> group with a different microenvironment and treatment path. This is the dominant target.
> subtype — the integrated diagnostic subtype: glioblastoma, astrocytoma, or
> oligodendroglioma.
> grade_high — the probability that the tumor is high grade (CNS WHO grade 3–4).
> These three targets are slide-level properties of the whole tumor. A single field of view
> of a spatially heterogeneous, reduced-resolution slide only weakly determines the molecular
> class, so a bag of several patches is provided per example and even a strong model is bounded
> well below a perfect score — the task ranks solvers rather than being solved outright. Patches
> are real human histology; labels come from the tumor's clinical work-up.
> Evaluation
> The score is a weighted composite in [0, 1] (higher is better):
> score = 0.50 * S_idh  +  0.30 * S_grade  +  0.20 * S_subtype
> S_idh and S_grade reward discrimination via a rescaled ranking score. Let
> A = AUC(prob, truth) — the probability that a random positive bag (IDH-wildtype, or
> high-grade) is ranked above a random negative bag. Then
> S = clip(0.30 + 1.80 * (A - 0.5), 0, 1).
> A ranking score is used because a single bag only weakly determines a molecular class: it
> rewards ordering the bags by risk and is agnostic to probability calibration, so a fitted
> model always beats the constant baseline (which scores A = 0.5, i.e. S = 0.30). A
> prediction that is NaN, infinite, or outside [0, 1] is treated as rank-neutral (0.5) for
> that bag — it neither helps nor hurts.
> S_subtype is the difficulty-weighted balanced recall over the three subtypes. Each bag
> has a difficulty weight — easy = 1, medium = 2, hard = 3 — by diagnostic ambiguity
> (glioblastoma easy, oligodendroglioma medium, astrocytoma hard). For each true subtype c,
> recall_c = sum(weight for correctly-predicted bags of class c) / sum(weight for all bags of class c), and S_subtype = mean(recall_c). A constant guess floors near 1/3.
> Reference evaluate(y_true, y_pred) for the ranking components (the authoritative
> implementation is grade.py):
> import numpy as np, pandas as pd
> def s_rank(prob, y):
> p = np.where(np.isfinite(prob) & (prob >= 0) & (prob <= 1), prob, 0.5)
> y = np.asarray(y, float); npos = (y == 1).sum(); nneg = (y == 0).sum()
> if npos == 0 or nneg == 0: A = 0.5
> else:
> r = pd.Series(p).rank(method="average").to_numpy()
> A = (r[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg)
> return min(1.0, max(0.0, 0.30 + 1.80 * (A - 0.5)))
> Invalid or missing predictions never crash the grader; they take the neutral/worst per-bag
> outcome.
> Dataset
> The prepared data is under public/:
> train.csv — one row per training bag, with columns:
> id (string) — unique bag id.
> images (string) — the bag's patch PNGs as a ;-separated list of paths, e.g.
> images/p000246.png;images/p000250.png;... (up to 8 patches per bag).
> idh_wildtype (integer 0/1) — 1 if the patient's tumor is IDH-wildtype.
> subtype (string) — glioblastoma / astrocytoma / oligodendroglioma.
> grade_high (integer 0/1) — 1 if CNS WHO grade 3–4.
> All bags from one patient share the same three labels (they are slide-level).
> test.csv — one row per test bag, with columns id and images only.
> images/ — the patch PNGs referenced by the bags (160×160 RGB).
> There are 1,956 training bags and 1,015 test bags. Train and test patients are
> disjoint (146 train patients, 79 test patients, 0 overlap): every test bag comes from a
> patient with no bags in the training set, so the molecular class must be inferred from
> morphology, not memorized per patient.
> Submission
> Write ./working/submission.csv with exactly these four columns and one row per id in
> **test.csv** (1,015 rows):
> id — the test bag id.
> idh_wildtype — probability in [0, 1] that the tumor is IDH-wildtype.
> subtype — one of glioblastoma, astrocytoma, oligodendroglioma.
> grade_high — probability in [0, 1] that the tumor is high grade (WHO 3–4).
> Example (the first rows, using real test ids):
> id,idh_wildtype,subtype,grade_high
> gb000002,0.82,glioblastoma,0.88
> gb000005,0.20,oligodendroglioma,0.55
> gb000007,0.34,astrocytoma,0.40
> Requirements
> Output exactly 1,015 rows, one per id in test.csv; ids must match the test set
> exactly (no missing, extra, foreign, or duplicate ids).
> The header must be exactly id,idh_wildtype,subtype,grade_high — no extra columns.
> idh_wildtype and grade_high are probabilities in [0, 1]; NaN, infinite, or out-of-range
> values are scored as the neutral/worst outcome for that bag (not dropped).
> subtype must be one of the three strings above (case-insensitive); any other value scores
> as wrong for that bag.
> A label-free sample_submission.csv (constant baseline) is provided; it is a valid, if weak,
> submission that scores above the platform floor.
> What not to use
> No pretrained weights and no foundation models. Train from the provided patches only.
> Histopathology foundation models and ImageNet-pretrained backbones are not permitted — they
> defeat the intended skill and must be blocked at the harness level.
> No external data.
> Prior work
> The nearest public neighbors are (a) IPD-Brain's own benchmark, which does whole-slide subtype / IHC classification with multiple-instance learning over an entire gigapixel slide, and (b) tumor-infiltrating-lymphocyte patch classifiers (e.g. Saltz et al.). This task is a different mechanism: it grades a small-bag, held-out inference of the patient's slide-level molecular immunotherapy-stratification class under a strict patient group split, on reduced-resolution patches, with a ranking-based, difficulty-weighted composite that deliberately caps the ceiling. It is neither whole-slide MIL (you get a handful of patches, not the gigapixel slide) nor patch-label classification (the graded targets are properties of the whole tumor, not of any patch), and the metric rewards ranking bags by molecular risk rather than a single calibrated label. The result spreads solvers across a graded band instead of saturating.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Missing Sentence Identification in Literary Texts

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cesq2ccenamyx1dg8yxr9rh8bjg0d
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat supegirl's score of 0.940!

Full challenge description from page:

> Meridian Ashes: Missing Sentence Identification in Literary Texts
> Overview
> Objective: Predict the original missing sentence for each of three gaps.
> For every test row, select three original sentences from six labelled candidates. Return their candidate letters in gap_1, gap_2, gap_3 order. For example, D>A>F means candidate D belongs in gap_1, candidate A belongs in gap_2, and candidate F belongs in gap_3.
> Meridian Ashes is the fictional name of this benchmark. No source story was recovered from an actual fire. Narrative Bridge Authentication means deciding which candidate is the unmodified sentence that originally connected the text on both sides of a gap. This models a real text-integrity problem: detecting and repairing local word-order corruption in literary archives, OCR restoration pipelines, and document collections.
> The data describes the texts as short stories but does not provide normalized subgenre labels or publication years. It also does not document a formal sampling frame for selecting the linked pages. The corpus therefore spans a heterogeneous literary collection and should not be treated as a balanced genre sample or a precisely time-bounded benchmark.
> The challenge transformation is synthetic and deterministic. Three sentences are removed from each selected story excerpt. The six candidates contain:
> Three original missing sentences.
> Three counterfeits created by moving a short phrase inside an original sentence.
> One counterfeit for each original, with exactly the same whitespace-separated tokens and the same length as that original.
> Word counts and candidate length cannot identify which member of a matched pair is original. A solver must use word order, sentence fluency, the text on both sides of each gap, and a one-to-one assignment across all three gaps.
> Evaluation
> MeridianScore is the mean row quality and ranges from 0 to 1. Higher is better.
> For one row, let the prediction be
> 𝑝
> =
> (
> 𝑝
> 1
> ,
> 𝑝
> 2
> ,
> 𝑝
> 3
> )
> p=(p1,p2,p3) and the hidden answer be
> 𝑡
> =
> (
> 𝑡
> 1
> ,
> 𝑡
> 2
> ,
> 𝑡
> 3
> )
> t=(t1,t2,t3).
> Position accuracy is the number of exact gap assignments divided by three. It checks
> 𝑝
> 1
> =
> 𝑡
> 1
> p1=t1,
> 𝑝
> 2
> =
> 𝑡
> 2
> p2=t2, and
> 𝑝
> 3
> =
> 𝑡
> 3
> p3=t3.
> Membership quality is the number of hidden letters selected anywhere in the prediction divided by three.
> Precedence quality evaluates exactly three pairs:
> (
> 𝑡
> 1
> ,
> 𝑡
> 2
> )
> (t1,t2),
> (
> 𝑡
> 1
> ,
> 𝑡
> 3
> )
> (t1,t3), and
> (
> 𝑡
> 2
> ,
> 𝑡
> 3
> )
> (t2,t3). A pair earns one hit only if both letters occur in the prediction and the first appears before the second. The number of hits is divided by three.
> Exact quality is 1 only when the complete ordered prediction equals the hidden answer. Otherwise it is 0.
> For example, if the hidden answer is D>A>F and the prediction is D>F>A, the precedence pairs are D before A, D before F, and A before F. The first two are correct and the last is wrong, so precedence quality is 2/3.
> The row quality is:
> 𝑞
> 𝑟
> 𝑜
> 𝑤
> =
> 0.30
> ∗
> 𝑝
> 𝑜
> 𝑠
> 𝑖
> 𝑡
> 𝑖
> 𝑜
> 𝑛
> 𝑎
> 𝑐
> 𝑐
> 𝑢
> 𝑟
> 𝑎
> 𝑐
> 𝑦
> +
> 0.15
> ∗
> 𝑚
> 𝑒
> 𝑚
> 𝑏
> 𝑒
> 𝑟
> 𝑠
> ℎ
> 𝑖
> 𝑝
> 𝑞
> 𝑢
> 𝑎
> 𝑙
> 𝑖
> 𝑡
> 𝑦
> +
> 0.05
> ∗
> 𝑝
> 𝑟
> 𝑒
> 𝑐
> 𝑒
> 𝑑
> 𝑒
> 𝑛
> 𝑐
> 𝑒
> 𝑞
> 𝑢
> 𝑎
> 𝑙
> 𝑖
> 𝑡
> 𝑦
> +
> 0.50
> ∗
> 𝑒
> 𝑥
> 𝑎
> 𝑐
> 𝑡
> 𝑞
> 𝑢
> 𝑎
> 𝑙
> 𝑖
> 𝑡
> 𝑦
> qrow=0.30∗positionaccuracy+0.15∗membershipquality+0.05∗precedencequality+0.50∗exactquality
> The final score is:
> 𝑀
> 𝑒
> 𝑟
> 𝑖
> 𝑑
> 𝑖
> 𝑎
> 𝑛
> 𝑆
> 𝑐
> 𝑜
> 𝑟
> 𝑒
> =
> 𝑚
> 𝑒
> 𝑎
> 𝑛
> (
> 𝑞
> 𝑟
> 𝑜
> 𝑤
> over all test rows
> )
> MeridianScore=mean(qrow over all test rows)
> The exact-match component carries half of the score. A prediction with the right candidates in the wrong order receives no exact-match credit.
> A malformed, repeated-letter, missing, non-finite, or out-of-alphabet binding receives 0 row quality. A submission in which every binding is invalid receives score 0. A perfect submission receives score 1.
> The grader merges rows on id. Missing rows, duplicate ids, foreign ids, missing or renamed columns, and extra columns raise a clean ValueError.
> Dataset
> The prepared public data contains 10,925 distinct rows derived from 3,722 eligible source stories.
> train.csv contains 8,261 labelled rows from 151 author groups.
> test.csv contains 2,664 unlabelled rows from 55 different author groups.
> sample_submission.csv contains every test id and a constant format-valid example binding.
> An author group is the whitespace-normalized value of the source workbook's author field. Every prepared row derived from stories with the same author value belongs to the same group. All rows from one author group are assigned entirely to train or entirely to test before the author field is removed. Author-group overlap between train and test is exactly zero. Author names and group labels are not public model inputs.
> train.csv
> id (integer) is an independently randomized opaque 15-digit identifier.
> gap_1 (string) contains two original sentences before and two after the first missing sentence.
> gap_2 (string) contains two original sentences before and two after the second missing sentence.
> gap_3 (string) contains two original sentences before and two after the third missing sentence.
> candidates (string) contains six newline-separated records. Each record begins with [A] through [F] followed by one candidate sentence.
> binding (string) contains the three original candidate letters in gap_1, gap_2, gap_3 order.
> The candidates string has this exact layout:
> [A] First candidate sentence.
> [B] Second candidate sentence.
> [C] Third candidate sentence.
> [D] Fourth candidate sentence.
> [E] Fifth candidate sentence.
> [F] Sixth candidate sentence.
> test.csv
> id (integer) is an independently randomized opaque 15-digit identifier.
> gap_1 (string) contains two original sentences before and two after the first missing sentence.
> gap_2 (string) contains two original sentences before and two after the second missing sentence.
> gap_3 (string) contains two original sentences before and two after the third missing sentence.
> candidates (string) uses the same six-line [A] through [F] layout as the training file.
> The hidden binding is absent from test.csv. Author, author group, title, source URL, original row number, and split indicator are also absent.
> Submission
> Write exactly one file to ./working/submission.csv.
> The file must contain exactly these columns:
> id (integer) contains every test id exactly once.
> binding (string) contains three distinct uppercase letters from A through F, separated by >.
> The submission must contain exactly 2,664 data rows. Row order does not matter because grading merges on id.
> Example using real test ids:
> Code snippet
> id,binding
> 239107279958705,D>A>F
> 794116194461966,B>E>A
> 340251000425690,F>C>D
> Requirements
> Submit exactly 2,664 predictions and cover every test id exactly once.
> Use only letters A through F and do not repeat a letter within one binding.
> Preserve gap_1>gap_2>gap_3 order.
> Do not add columns or omit, duplicate, or invent ids.
> A missing, malformed, repeated-letter, non-finite, or out-of-alphabet binding receives zero row quality.
> Treat the candidates as one constrained assignment problem rather than three unrestricted choices.
> Use the provided GPU for the primary learned sequence model.
> Finish within 90 minutes.
> What not to use
> Do not use pretrained weights, external corpora, plot summaries, source-story lookup, internet access, or runtime downloads.
> Do not retrieve stories from source URLs.
> Do not fit vocabularies, normalizers, or learned representations on test text.
> Harness-side network and filesystem isolation are required because the grader cannot detect external knowledge by itself.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Enzyme Catalytic Residue and Role Prediction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dc6ksmht9dw61dyh8ydf7pd8am5qq
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat samluu206's score of 0.173!

Full challenge description from page:

> Overview
> Most of a protein does nothing chemical. Out of hundreds of residues, only a small crew, usually somewhere between two and eight, actually performs the reaction, and they do it by sitting in exactly the right places relative to one another in a three-dimensional active site. Within that crew, every member has a distinct job:
> the nucleophile makes the attack on the substrate;
> an acid/base passes protons in and out;
> a metal ligand pins a catalytic ion where the chemistry needs it;
> an electrostatic residue steadies the charge that builds up in the transition state.
> Working out who does what is the difference between knowing a protein's shape and knowing its chemistry. It underpins enzyme engineering, mechanism studies, and structure-based drug design alike.
> Your inputs are real enzyme structures, single chains taken from the PDB. The corresponding catalytic annotations are drawn from M-CSA (the Mechanism and Catalytic Site Atlas), where the machinery of each enzyme has been curated by hand. Your job, enzyme by enzyme, is to rebuild that machinery.
> What makes this hard
> Nearly every convenient shortcut has been taken away, which is what makes this a from-scratch structural reasoning problem:
> One structure per enzyme, and nothing else. No homologues, no conservation scores, nothing evolutionary to lean on.
> No multiple sequence alignment, so you cannot borrow an answer from a related family.
> Substrate and organic cofactors are gone, so "whatever the ligand is touching" is not an option.
> Metal ions do survive the cleaning, so coordination geometry is one signal you can still exploit.
> What remains is geometry and chemistry. Generic active-site detectors can often tell you where a pocket is, but none of them will tell you what each residue is doing there, and that mechanistic assignment is where this task lives. The pipeline is yours to build end to end.
> Data
> train/structures/<enzyme_id>.pdb   # 237 enzymes (labeled)
> test/structures/<enzyme_id>.pdb    # 554 enzymes (predict these)
> train_labels.csv                   # enzyme_id, resid, role
> train_enzymes.csv                  # enzyme_id, num_residues, num_catalytic
> test_enzymes.csv                   # enzyme_id, num_residues, num_catalytic
> sample_submission.csv              # format example
> Structures
> Each <enzyme_id>.pdb is a cleaned single protein chain:
> standard ATOM records for the 20 amino acids;
> HETATM records for any metal ions;
> waters, substrates, and organic cofactors removed;
> residues renumbered 1..num_residues in chain order (resid refers to this numbering, in chain A);
> headers and the source accession stripped.
> Roles
> Every catalytic residue carries exactly one of four mechanistic roles.
> nucleophile -- attacks the substrate or forms a covalent intermediate (also nucleofuge, covalent catalysis).
> acid_base -- donates or accepts a proton: general acid/base, proton shuttle/relay.
> metal_ligand -- coordinates a catalytic metal ion.
> electrostatic -- stabilises charge or the transition state, activates or tunes a partner's pKa.
> num_catalytic, the number N of catalytic residues to find, is given for every enzyme, train and test.
> Note. Some enzymes contain a few additional M-CSA residues with purely structural (other) roles. These are not graded: predicting them neither helps nor hurts.
> Task
> For each test enzyme, output a ranked list of residues, each tagged with the mechanistic role you predict and a confidence score.
> Evaluation
> Submissions are scored by mean partial-credit, role-aware precision@N.
> For each test enzyme with N = num_catalytic graded catalytic residues, your predictions are sorted by descending score (ties broken by smaller resid). Residues M-CSA marks as ungraded (other) are skipped and do not consume the budget. Over the first N remaining predictions, each residue earns:
> 0.5 if it is a true catalytic residue (correct location), and
> another 0.5 if its predicted role also matches the true role.
> The enzyme score is total credit divided by N. The final score is the mean over all test enzymes, in the range [0, 1]. Higher is better. A missing enzyme scores 0.
> def grade(submission, answers):
> scores = []
> for eid, g in answers.groupby("enzyme_id"):
> N = int(g.num_catalytic.iloc[0])
> truth  = dict(zip(g[g.graded == 1].resid, g[g.graded == 1].role))
> ignore = set(g[g.graded == 0].resid)
> sub = (submission[submission.enzyme_id == eid]
> .sort_values(["score", "resid"], ascending=[False, True]))
> credit = taken = 0.0
> seen = set()
> for rid, role in zip(sub.resid, sub.role):
> if rid in seen:
> continue
> seen.add(rid)
> if rid in ignore:
> continue
> if taken >= N:
> break
> taken += 1
> if rid in truth:
> credit += 0.5 + (0.5 if role == truth[rid] else 0.0)
> scores.append(credit / N)
> return sum(scores) / len(scores)
> Submission Format
> A single CSV, submission.csv:
> enzyme_id (str) -- test enzyme id, e.g. enz_0a1b2c3d4e.
> resid (int) -- residue number (1..num_residues) in the structure.
> role (str) -- one of nucleophile, acid_base, metal_ligand, electrostatic.
> score (float) -- confidence this residue is catalytic; higher = more confident.
> Requirements
> Include a header row.
> For every test enzyme, submit at least num_catalytic residues. Submitting more (e.g. your top ~30 by score) is safe, since the grader only reads down to the first N graded residues.
> score is used only for ranking within each enzyme.
> Rules
> This is a from-scratch structural-reasoning challenge.
> Allowed
> Standard Kaggle-image libraries: numpy, scipy, pandas, scikit-learn, and similar general-purpose numeric / ML packages.
> Any features and models you build yourself from the structure: geometric descriptors, pocket/cavity analysis, residue graphs, side-chain orientation, contact density, distances to metals, hand-crafted scorers, or classifiers trained on train_labels.csv.
> Using train_labels.csv freely for training, validation, and tuning.
> Not Allowed
> Off-the-shelf active-site / catalytic-residue tools or their outputs (CSA/M-CSA lookups, THEMATICS, POOL, EXIA, ConSurf, firestar, PDBe/UniProt active-site annotations).
> Pretrained protein language or structure models (ESM, AlphaFold, ProtBERT, SaProt, …), pretrained weights, or embeddings derived from them.
> Any external lookup: identifying an enzyme by sequence or structure search (BLAST, Foldseek, DALI, …) and retrieving its known catalytic residues from M-CSA, the PDB, UniProt, or elsewhere; or hard-coding answers for specific enzyme_ids. Work only from the provided public/ files.
> Fetching additional data or model weights at solve time.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## SAR-Optical Cross-Modal Retrieval and Orientation Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7eqw1bwb335hfjj9nck8nh8d8bnr9z
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> The Nightwatch Mosaic: SAR-Optical Cross-Modal Retrieval and Orientation Recovery
> Objective
> Rank seven Sentinel-2 optical candidates for each Sentinel-1 radar patch so the true co-registered optical footprint is first, then recover the quarter-turn orientation of that top-ranked patch.
> An emergency mapping relay called Nightwatch preserved its radar echoes but detached the matching optical tiles. Every candidate bank comes from one hidden city and one hidden Local Climate Zone stratum, so land-cover recognition alone cannot solve the case. The optical tiles were also rotated before storage. You must learn the visual correspondence between radar structure and multispectral appearance across cities that never appear in training.
> This is a GPU computer-vision challenge. Train all neural weights from random initialization on the supplied data. The full solution, including inference and CSV creation, must finish within 90 minutes.
> Evaluation
> The Nightwatch score is the mean of a rotation-aware reciprocal-rank quality over all test rows.
> For row i, let r_i be the one-based position of the true optical candidate in rank_1 through rank_7. Let b_i equal 1 only when the true candidate is in rank_1 and quarter_turns correctly restores that stored optical patch to north-up orientation. Otherwise b_i is 0.
> The valid-row score is:
> q_i = 0.85 / r_i + 0.15 * b_i
> score = mean(q_i)
> A valid row must rank every slot from 0 through 6 exactly once and must give an integer quarter_turns from 0 through 3. Any NaN, infinity, fractional value, out-of-range value, duplicated rank slot, or missing rank slot makes that row worth 0. Structural submission errors raise ValueError.
> The score is finite and lies in [0, 1]. Higher is better. A perfect ranking with correct orientation scores 1.0.
> Dataset
> All files are under ./dataset/public/.
> train.csv has 12,383 rows.
> id (int64) — randomized row identifier with no source or target information.
> region_group (string) — opaque city-group token. The seven training tokens do not occur in test.
> sar_index (int64) — row index into train_sar.npy.
> candidate_0 through candidate_6 (int64) — row indices into train_optical.npy.
> match_slot (int64) — zero-based candidate slot containing the co-registered optical patch.
> quarter_turns (int64) — number of 90-degree counter-clockwise turns needed to restore the matching stored optical patch to north-up orientation.
> test.csv has 5,306 rows and the same input columns, without match_slot or quarter_turns.
> train_sar.npy has shape 12383 x 4 x 32 x 32 and dtype float32.
> test_sar.npy has shape 5306 x 4 x 32 x 32 and dtype float32.
> train_optical.npy has shape 12383 x 6 x 32 x 32 and dtype float32.
> test_optical.npy has shape 5306 x 6 x 32 x 32 and dtype float32.
> sample_submission.csv is a label-free fixed ranking in the required format.
> The equal CSV, radar-array, and optical-array row counts are intentional. Each prepared observation contributes one stored radar patch and one stored optical counterpart. The candidate columns do not address a separate array with seven new patches per query. Instead, each seven-observation cohort reuses its seven optical indices as the candidate bank for every radar query in that cohort. Consequently, every valid optical index appears in candidate columns exactly seven times. Train candidate indices span 0 through 12,382, and test candidate indices span 0 through 5,305; both optical arrays therefore have the correct size.
> The radar channels are Lee-filtered VH intensity, Lee-filtered VV intensity, covariance real, and covariance imaginary. The optical channels are B2, B3, B4, B8, B11, and B12. Array indices are independently permuted. A radar index is not aligned by position with an optical index.
> Seven-way candidate cohorts contain real patches from the same hidden source city and hidden LCZ class. No cohort contains byte-identical candidates. A source city belongs wholly to train or wholly to test. There are seven train cities and three test cities with zero city overlap.
> Submission
> Write ./working/submission.csv with exactly these columns in exactly this order:
> id
> rank_1
> rank_2
> rank_3
> rank_4
> rank_5
> rank_6
> rank_7
> quarter_turns
> Each row must contain a permutation of candidate slots 0 through 6. quarter_turns applies to the optical patch named in rank_1 and must be 0, 1, 2, or 3 counter-clockwise quarter turns.
> id,rank_1,rank_2,rank_3,rank_4,rank_5,rank_6,rank_7,quarter_turns
> 100000078565,0,1,2,3,4,5,6,0
> 100000298769,0,1,2,3,4,5,6,0
> Requirements
> Submit exactly 5,306 rows, one for every test id and no others.
> IDs may appear in any row order. Scoring merges on id.
> IDs must be unique and integer-valued. Numeric-string forms of valid IDs are accepted.
> Column names and order must match the submission contract exactly. Extra, renamed, or missing columns are rejected.
> Every valid ranking must use each integer from 0 through 6 exactly once.
> Any invalid prediction content makes its complete row worth 0.
> Use the supplied train rows only to fit normalization or learned parameters.
> Neural training and inference must run on a GPU. CPU use is limited to data loading, orchestration, and writing the submission.
> The complete solution has a 90-minute limit.
> What Not to Use
> Do not use pretrained weights, foundation models, external datasets, external geolocation, maps, or downloaded checkpoints.
> Do not use network access or runtime downloads.
> Do not acces hidden city names, LCZ labels, upstream row positions, or any path outside ./dataset/public/.
> Do not infer targets from IDs, file order, or array indices. Those values are independently randomized.
> Do not fit normalization, thresholds, or model selection criteria on test sensor values.
> Do not submit a CPU-only heuristic as the solution. The reference notebook refuses to train without an available GPU.
> The CSV grader cannot enforce hardware, network, or training provenance. Those restrictions require execution-harness and trajectory review.
> Extra Modelling Info
> Cross-modal remote-sensing retrieval usually searches a broad gallery or estimates geometric registration. Nightwatch defines a different mechanism: each query receives a seven-way cohort matched on hidden city and hidden land-cover stratum, every optical item has an unknown quarter-turn, and all source cities are held out as complete groups.
> This removes the ordinary class-recognition shortcut and tests category-controlled cross-sensor instance rebinding plus orientation recovery under geographic shift. The target is not an LCZ label, coordinate, or source field. Novelty self-assessment: 8/10. The nearest public family is SAR-optical retrieval; the hidden-stratum cohort construction, city-disjoint evaluation, and joint rank-orientation output are the material differences.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Matching Electronic-Nose Measurements Across Sensor Drift

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72jm4yv4ag6pd0g7srbg0m918bg0zq
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top Score | 0.368 | Created | Jul 31, 2026 | Start New Solution

Full challenge description from page:

> Matching Electronic-Nose Measurements Across Sensor Drift
> Overview
> An electronic nose is an array of gas sensors. Each metal-oxide sensor changes its resistance when a gas reaches it, and the pattern of resistance across the array is how the device tells one substance from another. The trouble is that the sensors do not stay the same. They age, week by week, and the same substance at the same concentration reads differently as the months pass. That slow change, sensor drift, is why these devices are hard to rely on: a description of a substance learned on one day quietly stops fitting the readings a few months later.
> This challenge is about seeing through that drift. You are given one 20-minute measurement, the query, and a list of 40 candidate measurements. Exactly one candidate is the same substance as the query, the same analyte at the same concentration, but recorded on a different day, when the sensors had aged into a different state. The other 39 are different substances. You must find the same-substance one.
> Everything that would let you cheat is taken away.
> The day cannot help. Every candidate, including the true match, comes from a day the query does not. The true match is never a same-day near-copy; it is the same substance seen through a fresh layer of drift, so a measurement that looks most like the query at a glance is often a different substance whose drift happens to resemble it.
> Counting cannot help. Candidates are drawn from the same pool the true match comes from, so how often a measurement appears across the benchmark says nothing about whether it is a match. A ranker that only counts appearances scores at chance, and so does one that never looks at the query.
> There is nothing to look up. The recording dates are gone, the temperature and humidity that fingerprint a day are gone, the raw resistances are re-derived, and every identity is an opaque code. What survives is the response pattern across the 62 sensors.
> The days you are scored on are ones you never trained on. The split is by day, so the sensor states you match across were never in training. What carries over has to be a sense of a substance that holds up as the array ages, not a memory of any one day.
> Task
> For every (query_id, candidate_id) pair in test_pairs.csv, output a real-valued score. Within a query, a higher score means more likely to be the same substance as the query. Only the ranking inside each query is read, so the scale is free and scores are never compared across queries.
> Data
> All inputs are under dataset/public/. A measurement is one 20-minute cycle, resampled to 500 timesteps, across the 62 sensor channels: float32, shape (500, 62).
> train_windows.npy: float32 array of shape (Ntr, 500, 62). Load with numpy.load(..., mmap_mode="r").
> train.csv: one row per training measurement. Columns:
> recording_id (string): the measurement.
> window (int): its row index into train_windows.npy.
> substance (string): the analyte and concentration, for example diacetyl_1ppm, that produced it. This is the supervision you learn a drift-robust similarity from.
> test_windows.npy and test.csv: the same, over the test measurements, with no substance.
> test_pairs.csv: the candidate lists, one row per (query_id, candidate_id).
> sample_submission.csv: a correctly formatted submission for every pair, scoring at chance.
> Each query has exactly 40 candidates and exactly one true match, always recorded on a different day than the query. The days in the test set appear nowhere in training.
> Evaluation
> Submissions are scored by mean reciprocal rank. Within each query the candidates are ranked by your score, and the query contributes the reciprocal of the rank of its true match:
> MRR = mean over queries of 1 / rank(true match)
> Candidates you give equal scores share their averaged reciprocal rank, so a constant submission scores exactly chance. With 40 candidates:
> A constant score, or a random ordering, scores 0.11 (chance). With one true match among 40 candidates the match is equally likely at any rank, so the chance MRR is the average of 1/rank over ranks 1 to 40, which is H(40) / 40 = 0.107, not 1 / 40.
> Ranking by how often a candidate appears scores 0.13.
> Cosine similarity of simple per-sensor response features, no training and no drift correction, the reference here, scores 0.33.
> Finding the true match first every time scores 1.00.
> The reference does nothing about the drift; the distance from 0.33 to 1.00 is what learning a drift-robust similarity from the training substances buys you.
> Submission format
> Write ./working/submission.csv with exactly these columns:
> query_id,candidate_id,score
> q_1a2b3c4d5e6f,c_9f8e7d6c5b4a,0.02
> q_1a2b3c4d5e6f,c_3c4d5e6f7a8b,0.91
> ...
> One row for every (query_id, candidate_id) pair in test_pairs.csv, and no others. A submission that drops a pair, repeats one, or invents one is rejected.
> score is any finite real number; only the order within each query is used.
> Start from sample_submission.csv to guarantee the correct pair set, and write with index=False.
> Constraints
> Read the challenge inputs only from ./dataset/public/. Write your output only to ./working/submission.csv.
> One A10G GPU (24 GB), plus CPU cores and 62 GB of memory, and a hard limit of 1.5 hours for the whole run. The measurements are short multi-channel time-series, so a model over the raw signal trains comfortably in that budget; the reference finishes in a couple of minutes.
> Train from scratch. No pretrained weights of any kind. Do not download a checkpoint from a model hub and do not initialise from anything trained elsewhere. Every parameter you use must be fitted on the provided training measurements. Nothing is pretrained on metal-oxide sensor arrays, and building the representation is the point.
> No package installs (no pip or conda install). You may use the preinstalled libraries (numpy, scipy, pandas, scikit-learn, pytorch, and so on).
> What Not To Use
> Do not try to identify the source measurements or their substance from any public archive. The dates, ambient conditions and raw resistances were removed or re-derived for exactly this reason. Decide from the provided signal.
> Do not hardcode outputs or otherwise bypass learning from the data.
> A learning-based approach is expected. The signal is in which sensors respond and how their responses relate to each other, which is more stable across the array's ageing than any single sensor's absolute level. A similarity trained on the labelled training measurements, where you know which share a substance, or an embedding trained to pull a substance's own measurements together across days and push different substances of a similar-looking day apart, is the natural line of attack. The whole difficulty is that a day you have never seen has drifted somewhere your training days did not.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Nano-Finance: The 10M Parameter Edge AI Challenge

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78hs7etxzpegkp9wb5zb3ntx8564x6
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, finance, large-scale
- Best/top context found: Top Score | — | Created | Apr 20, 2026 | Start New Solution

Full challenge description from page:

> Nano-Finance: The 10M Parameter Edge AI Challenge
> Overview
> As AI scales, the hardware required to run it balloons. But what if we need complex financial reasoning on an offline edge node, a smartwatch, or a resource-constrained automotive infotainment system?
> In this challenge, you are tasked with creating a highly capable, generative financial assistant with a strict architectural limitation: Your trained Large Language Model (LLM) must contain fewer than 10,000,000 parameters. Given a financial instruction and supplementary input context, your micro-model must generate a coherent, factually accurate response. You will need to push the boundaries of efficient model architectures, INT8/INT4 quantization, and high-quality data distillation to make a model this small perform like an expert financial advisor.
> Data Provenance & Integrity
> The data consists of approximately 68,000 curated financial scenarios, spanning complex economic concepts, market mechanics, and technical indicators. These scenarios originate from a specialized financial instruction-tuning corpus originally compiled to train language models as domain-expert financial advisors. To ensure competition integrity and prevent test-set leakage, the dataset has been rigorously normalized and anonymized:
> All sequential row identifiers have been replaced with deterministic cryptographic UUIDs.
> The core text has undergone case-preserving lexical obfuscation (automatically substituting key financial terminology with exact-case synonyms) to permanently break exact-string matching against public open-source data repositories.
> Method Requirements & Restrictions
> Mandatory: You must train or fine-tune an autoregressive Language Model from scratch or from a foundational micro-model.
> Parameter Limit: The final model weights used to generate your submission must total < 10,000,000 parameters.
> Prohibited: API calls to external models, models exceeding the parameter limit, basic rule-based NLP templates, or pure Retrieval-Augmented Generation (RAG) that copies the exact training text without generating novel responses.
> Evaluation
> Submissions are scored using a custom Financial Overlap & Numeric Fidelity Metric, designed to evaluate both the semantic meaning of the generated text and the strict accuracy of financial figures.
> The score is calculated per row and averaged across the test set using the following formula:
> 𝑆
> 𝑐
> 𝑜
> 𝑟
> 𝑒
> =
> (
> 0.7
> ×
> 𝑆
> 𝑠
> 𝑒
> 𝑚
> 𝑎
> 𝑛
> 𝑡
> 𝑖
> 𝑐
> )
> +
> (
> 0.3
> ×
> 𝑆
> 𝑛
> 𝑢
> 𝑚
> 𝑒
> 𝑟
> 𝑖
> 𝑐
> )
> Score=(0.7×S
> semantic
> ​
> )+(0.3×S
> numeric
> ​
> )
> 1. Semantic Similarity (
> 𝑆
> 𝑠
> 𝑒
> 𝑚
> 𝑎
> 𝑛
> 𝑡
> 𝑖
> 𝑐
> S
> semantic
> ​
> )
> Calculated using the cosine similarity of TF-IDF vectors (capped at 10,000 features, English stop-words removed) between your prediction (
> 𝑃
> P) and the ground truth (
> 𝑇
> T):
> 𝑆
> 𝑠
> 𝑒
> 𝑚
> 𝑎
> 𝑛
> 𝑡
> 𝑖
> 𝑐
> =
> 𝑃
> ⋅
> 𝑇
> ∣
> ∣
> 𝑃
> ∣
> ∣
> ∣
> ∣
> 𝑇
> ∣
> ∣
> S
> semantic
> ​
> =
> ∣∣P∣∣∣∣T∣∣
> P⋅T
> ​
> 2. Numeric Fidelity (
> 𝑆
> 𝑛
> 𝑢
> 𝑚
> 𝑒
> 𝑟
> 𝑖
> 𝑐
> S
> numeric
> ​
> )
> Evaluates the exact overlap of numbers/digits between the predicted text (
> 𝑁
> 𝑝
> N
> p
> ​
> ) and ground truth text (
> 𝑁
> 𝑡
> N
> t
> ​
> ) using the Jaccard Index:
> 𝑆
> 𝑛
> 𝑢
> 𝑚
> 𝑒
> 𝑟
> 𝑖
> 𝑐
> =
> ∣
> 𝑁
> 𝑝
> ∩
> 𝑁
> 𝑡
> ∣
> ∣
> 𝑁
> 𝑝
> ∪
> 𝑁
> 𝑡
> ∣
> S
> numeric
> ​
> =
> ∣N
> p
> ​
> ∪N
> t
> ​
> ∣
> ∣N
> p
> ​
> ∩N
> t
> ​
> ∣
> ​
> Edge Cases in Evaluation:
> If the ground truth contains no numbers and the prediction contains no numbers, the numeric score is automatically scored as 1.0.
> If the ground truth contains no numbers but the prediction hallucinated a number, the numeric score is heavily penalized to 0.0.
> If the prediction misses all numbers present in the ground truth, the numeric score is 0.0.
> Blank or null predictions receive a baseline fallback score of 0.001 to prevent absolute zero math errors.
> Dataset
> File Structure
> public/train.csv (approx. 58,500 rows): The training set containing labeled examples.
> public/test.csv (approx. 10,300 rows): The test set. You must predict the missing output for these rows.
> public/sample_submission.csv: A valid example of the expected submission format.
> Column Descriptions & Data Types
> The dataset files contain the following columns:
> id
> Type: string
> Description: A unique, deterministic cryptographic UUID assigned to each row.
> Example: a1b2c3d4-e5f6-7890-1234-56789abcdef0
> instruction
> Type: string
> Description: A natural language prompt, question, or command requesting financial analysis, definitions, or explanations.
> Example: "Explain the mechanics of a 0% financing deceptive practice."
> input
> Type: string
> Description: Supplementary financial context or specific data parameters to condition the model's response. This is frequently an empty string if the instruction is self-contained.
> Example: "Client is looking at a 60-month auto financing."
> output
> Type: string
> Description: (Target Variable - Present in train.csv ONLY). A detailed, free-form text response representing the factual financial answer and expert analysis.
> Example: "The dealership profits by burying the cost in the backend..."
> Submission
> Submit a CSV file containing your model's predictions. The file must contain exactly the same number of rows as test.csv (approx. 10,300 rows) and include a header row.
> Important Column Naming: While the target variable in the training data is named "output", your submission file must name the column containing your generated text "prediction"
> Format Specification:
> id (Type: string): The exact cryptographic identifier matching the row from test.csv.
> prediction (Type: string): Your micro-model's generated financial text response (representing the missing output). Cannot be empty or null.
> Example submission.csv format:
> id,prediction
> 550e8400-e29b-41d4-a716-446655440000,"A 0% financing deceptive practice works by burying the cost..."
> 7b2c9930-388f-4d26-9d35-312911294812,"ETFs are traded on exchanges like stocks..."```

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Scientific Abstract Context Span Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76v1ts9bj273y6d6rwaxq2j58bqaw3
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: text, generative, Dataset source is visible after the challenge closes., Leaderboard
- Best/top context found: Beat douglas's score of 0.333!

Full challenge description from page:

> Overview
> You are given the left and right context around an omitted sentence span from a scientific abstract. Your task is to infer the hidden span record: the sentence text and a compact list of technical terms that appear in that sentence.
> This is a pretraining-style challenge over research writing. The training file provides many examples of local abstract context, scientific terminology, and claim phrasing. Strong submissions should train on the provided corpus to learn how methods, findings, constraints, and comparisons are expressed in nearby abstract sentences.
> Dataset
> The public files are:
> train.csv: labeled examples.
> test.csv: unlabeled examples to solve.
> sample_submission.csv: schema-valid example submission.
> Columns:
> id (string): anonymized row id.
> prompt (string): task instruction.
> context_json (JSON string): abstract context.
> answer_format_json (JSON string): required answer schema.
> answer_json (JSON string, train only): target answer.
> context_json fields:
> abstract_prefix (string): one or two sentences before the omitted span.
> abstract_suffix (string): one or two sentences after the omitted span.
> claim_word_count_hint (integer): number of whitespace-separated words in the omitted span.
> term_count_hint (integer): number of target technical terms.
> answer_json fields:
> claim_sentence (string): the omitted abstract sentence.
> technical_terms (array of strings): lowercase technical terms from the omitted sentence.
> Submission
> Submit a CSV with exactly two columns:
> id (string): id from test.csv.
> answer_json (JSON string): predicted answer object.
> Example:
> id,answer_json
> abs_11111111111111,"{""claim_sentence"":""The proposed estimator remains consistent under bounded noise."",""technical_terms"":[""bounded"",""consistent"",""estimator""]}"
> abs_22222222222222,"{""claim_sentence"":""Experiments show improved accuracy on the held out benchmark."",""technical_terms"":[""accuracy"",""benchmark"",""experiments""]}"
> Evaluation
> Each row is scored from 0 to 1:
> row_score = 0.70 * sentence_f1 + 0.24 * term_f1 + 0.06 * length_score
> sentence_f1 is duplicate-aware word F1 between the predicted claim_sentence and the true sentence after lowercasing and tokenizing on letters, digits, underscores, plus signs, and hyphens. Precision is the number of matched predicted tokens divided by the total number of predicted tokens. Recall is the number of matched predicted tokens divided by the total number of true tokens. When both sides contain tokens, F1 = 2 * precision * recall / (precision + recall).
> term_f1 is duplicate-aware F1 over the technical_terms strings. length_score = exp(-abs(predicted_word_count - true_word_count) / 12).
> Malformed JSON or a structurally invalid answer_json receives 0 for that row. The leaderboard score is the mean row score across all test rows.
> What Not To Use
> Do not use external datasets, source mirrors, or held-out answer files.
> Do not search for test rows on the internet.
> Do not use pretrained language models, pretrained embeddings, hosted LLM APIs, or checkpoint-derived features.
> Do not hard-code test ids or answer dictionaries.
> Do not manually annotate the test set.
> Do not use internet access during solution execution.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Forest Chorus: Fine-Band Activity Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77qbbqfksbcnqky0ww23nd7n8bqqgz
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: audio, large-scale, feature-engineering, Dataset source is visible after the challenge closes.
- Best/top context found: Beat singhking's score of 67.277!

Full challenge description from page:

> Forest Chorus: Fine-Band Activity Recovery
> Overview
> Remote ecological recorders can capture rich sound continuously, but transmitting or storing every raw waveform is often impractical. A low-bandwidth monitoring system may preserve only broad frequency summaries. Those summaries reveal when the soundscape changes, but they merge distinct narrow frequency regions that may contain different calls, insects, wind, rain, or other acoustic events.
> In this challenge, every row represents a two-second window from a real tropical-forest passive-acoustic recording. You receive quantized energy and energy-change streams for six broad frequency bands, plus a broadband energy stream. Eight of the 48 time bins are unavailable. The original fine spectral representation is withheld.
> Your objective is to recover a fixed activity barcode for 12 fine frequency bands. For each fine band, predict:
> its overall activity level, from 0 through 3;
> the start octile of its strongest sustained activity interval; and
> the end octile of that interval.
> In plain language: for each test row, predict how active every hidden fine frequency band was and where its dominant activity occurred within the two-second window.
> This is a From Scratch signal-learning challenge. Every learned embedding, temporal encoder, attention block, convolution, and prediction head must be initialized from random weights and trained only with the supplied competition files. Pretrained audio, speech, music, ecological, vision, language, or general-purpose representation models are not permitted.
> The cases come from 189 real five-minute mono recordings collected at 24 kHz by seven autonomous field sensors on nine separated recording dates and three fixed daily sessions. All original filenames, timestamps, dates, recorder identifiers, geographic references, raw waveforms, and source-side detector outputs have been removed from the competition files. Sensor identifiers are replaced by seven shuffled opaque codes.
> What You Must Predict
> The hidden representation contains 12 logarithmically spaced fine frequency bands between 300 Hz and 10,500 Hz. The bands are named f00 through f11 in increasing frequency order.
> For each band fXX, predict three integer columns:
> level_fXX: overall fine-band salience quartile.
> 0: lowest activity tier
> 1: lower-middle activity tier
> 2: upper-middle activity tier
> 3: highest activity tier
> start_fXX: start of the dominant activity interval, from octile 0 through octile 7.
> end_fXX: end of the same interval, from octile 0 through octile 7.
> An octile divides the two-second case into eight equal consecutive regions. Every submitted interval must satisfy start_fXX <= end_fXX. A one-octile event therefore has equal start and end values.
> The target frequency-band edges, in hertz, are approximately:
> 300.0, 403.5, 542.6, 729.7, 981.3, 1319.7, 1774.8, 2386.9, 3210.0, 4316.9, 5805.6, 7807.6, 10500.0
> For each fine band, the target interval is the strongest contiguous elevated-energy run after short temporal smoothing. The activity level is determined from that band's high-salience energy. Targets are computed from the fine short-time spectrum before adjacent fine bands are merged into the visible inputs.
> Why It Is Difficult
> Each visible broad frequency band combines two target fine bands. A high value in one visible channel does not reveal which member of the pair produced it, and simultaneous fine-band events can produce nearly identical broad summaries. Quantization removes small amplitude distinctions. Eight complete time bins are unavailable in all three input streams, so interval boundaries may fall inside missing regions.
> The 56,511 cases use overlapping two-second windows, but every window from a sensor-date group remains entirely in one split. The test set contains 14 complete groups that never appear in training. Overlap therefore increases temporal training density without placing neighboring windows on opposite sides of the split. Fresh identifiers and shuffled row order remove chronological shortcuts.
> A useful solution must learn fine-band asymmetries, temporal shapes, cross-band dependencies, missing-bin behavior, and sensor-specific acoustics. Directly copying each broad channel to both fine bands provides a meaningful baseline but cannot fully resolve the hidden structure.
> Dataset
> train.csv
> Contains 43,953 training cases with the five input columns and all 36 target columns.
> test.csv
> Contains 12,558 cases from 14 held-out sensor-date groups. It contains only the five input columns.
> sample_submission.csv
> Contains all 12,558 test identifiers and the 36 target columns in the required order, initialized to zero.
> metadata.json
> Documents row counts, stream dimensions, allowed token values, target columns, missing-value marker, and split-group counts. It contains no source filenames, dates, or held-out group identifiers.
> Input Columns
> id — string — fresh opaque identifier for one two-second case.
> sensor_code — string — shuffled code for one of seven recording sensors.
> energy_stream — string — 288 space-separated integers encoding 48 time bins by six broad frequency bands.
> flux_stream — string — 288 space-separated integers encoding signed energy change for the same 48-by-6 layout.
> broadband_stream — string — 48 space-separated integers encoding overall energy through time.
> Both two-dimensional streams use time-major order. Token position 6 × t + b corresponds to time bin t and broad band b.
> energy_stream and broadband_stream use ordered values 0 through 7, from lower to higher energy. flux_stream uses values -3 through 3, from a strong decrease to a strong increase. The value 9 is the unavailable marker in all three streams; it is never a measured energy or flux value. Exactly eight time positions per row use 9, and all six channels are unavailable at those positions.
> Broad band b00 combines target bands f00 and f01, b01 combines f02 and f03, and so on through b05, which combines f10 and f11.
> Target Columns
> The 36 targets are ordered as follows:
> level_f00 through level_f11, each an integer in {0, 1, 2, 3};
> start_f00 through start_f11, each an integer in {0, ..., 7}; and
> end_f00 through end_f11, each an integer in {0, ..., 7}.
> For every band, the start value must not exceed the corresponding end value.
> Evaluation
> The Fine-Band Persistence Score combines balanced activity-level recovery, interval overlap, and relative temporal-order recovery.
> 1. Balanced activity term
> For fine-band column j and activity state s, let
> R(j,s) = correctly predicted rows whose true state is s / rows whose true state is s.
> Let S_j be the activity states present in the hidden answers for column j. The activity term is
> A = mean over the 12 level columns j of [mean over s in S_j of R(j,s)].
> This is macro recall across states and bands, so common activity tiers cannot dominate the score.
> 2. Interval-overlap term
> For row i and fine band j, the true interval and predicted interval are inclusive discrete octile ranges. Their intersection-over-union is
> IoU(i,j) = number of octiles in both intervals / number of octiles in either interval.
> The interval term is
> I = mean over all rows i and all 12 bands j of IoU(i,j).
> Exact one-octile intervals are handled normally because both endpoints are inclusive.
> 3. Temporal-order term
> For each row, compare the predicted start octiles of every unordered pair of fine bands. There are 66 pairs. A pair receives:
> 1 when the predicted relation—earlier, tied, or later—matches the true relation;
> 0.5 when exactly one relation is tied; and
> 0 when the predicted and true orders are opposite.
> O is the mean pair score over all rows and all 66 band pairs.
> Final score
> Score = 100 × (0.45 × A + 0.35 × I + 0.20 × O)
> The score ranges from 0 to 100, and higher is better. There is no score cap or hidden multiplier.
> Submission Format
> Submit one CSV with exactly 37 columns in the order used by sample_submission.csv: id, the 12 level columns, the 12 start columns, and the 12 end columns. Include every test identifier exactly once.
> All predictions must be finite integers in their stated ranges. Every predicted start must be less than or equal to its matching end. A row containing any missing, non-integer, infinite, out-of-range, or reversed-interval value receives zero credit for all three metric components. Extra columns, reordered columns, missing rows, duplicate identifiers, or unknown identifiers are rejected.
> Example using real test identifiers:
> id,level_f00,level_f01,level_f02,level_f03,level_f04,level_f05,level_f06,level_f07,level_f08,level_f09,level_f10,level_f11,start_f00,start_f01,start_f02,start_f03,start_f04,start_f05,start_f06,start_f07,start_f08,start_f09,start_f10,start_f11,end_f00,end_f01,end_f02,end_f03,end_f04,end_f05,end_f06,end_f07,end_f08,end_f09,end_f10,end_f11
> FC000D92E74383,2,1,3,2,0,1,2,3,1,0,2,1,0,1,2,2,3,1,4,3,5,0,6,2,1,2,4,3,3,5,6,4,7,1,7,5
> FC00105CA4984B,1,0,2,3,1,2,1,2,3,1,0,2,2,0,1,3,4,2,5,1,6,2,4,0,3,1,3,5,6,4,7,3,7,4,6,2
> From-Scratch Rules
> Train only on the supplied competition files.
> Initialize every learned representation and prediction component from random weights.
> Do not use pretrained audio, speech, music, ecological, vision, language, multimodal, or foundation-model encoders or embeddings.
> Do not use external datasets, source-recording searches, waveform matching, removed metadata, or source-side detections.
> Original neural architectures, learned token embeddings, hand-engineered signal features, and classical models trained solely on train.csv are permitted.
> GPU training is recommended: the training set contains 43,953 rows, 624 ordered temporal tokens per row, and 36 coupled targets.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Speech Mixture Speaker Attribution

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75c9c3s5twfc44ec3sgfsbrx8bjt1h
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat haidang's score of 0.467!

Full challenge description from page:

> Speech Mixture Speaker Attribution
> Overview
> Four people are speaking at the same time, recorded as one signal. You are told who two of
> them are — you are given a clean recording of each. Your task is to work out who the other
> two are, choosing from a lineup of ten clean recordings.
> So a row hands you three things:
> the mixture — four voices overlapping, as a single signal
> two shown voices — a clean excerpt of each of two of the four speakers in that mixture
> a lineup of ten clean excerpts — exactly two of which are the two speakers you were
> not shown
> Name those two.
> The shown voices are not decoration. They are the part of the mixture you can already account
> for, and accounting for them is what lets you hear what is left.
> Four properties of how each row is put together decide what can and cannot work:
> The lineup contains voices that resemble the ones you were shown. Two of the eight wrong
> answers were picked because they sound like the two speakers you were given. Those two people
> are genuinely audible in the mixture, so anyone who merely asks "which lineup voices can I
> hear in this recording?" will find these convincing and choose them. They are wrong. Ruling
> them out is exactly what the shown excerpts are for.
> Nothing in the lineup is the same recording that went into the mixture. Every clean
> excerpt is a different passage, spoken at a different time, by that person. There is no
> waveform to line up and no fragment to match; you have to recognise the speaker, not the
> recording.
> Everyone in a row is the same gender. Voice pitch range therefore separates nobody.
> Every excerpt is individually normalised. Loudness carries nothing.
> Task constraints
> The speakers are unseen. Nobody appearing in training appears in the test rows. What
> transfers is the general skill, not any particular voice.
> No metadata is published. Speaker identity, the words spoken, the recording session and
> the source of every excerpt are withheld. A row is thirteen signals and nothing else.
> Position carries nothing. The two correct lineup positions are spread evenly over 0…9,
> so always naming the same pair scores near the floor.
> The two unshown speakers are not the loudest. They sit at or below the level of the two
> you were shown, so picking out whoever is most prominent will not find them.
> Data
> Every signal is published as a time–frequency picture: 48 frequency bands spaced by ear,
> against successive moments in time, as uint8 values from 0 to 255.
> The mixture covers about 5 seconds — 48 × 160.
> Each shown excerpt and each lineup excerpt covers about 2.5 seconds — 48 × 80.
> Files provided:
> train.npz — training inputs; holds the arrays ids, mixture, shown and pool
> described below, with N = 6,000 rows
> train.csv — training answers; two columns, id and prediction, described below
> test.npz — test inputs; the same four arrays as train.npz, with N = 4,000 rows
> sample_submission.csv — a correctly-formatted but deliberately weak example submission,
> with the same two columns as train.csv (id and prediction) and one row for each of the
> 4,000 test ids. It names the same pair of lineup positions for every row, scores about 0.20,
> and exists to show the exact expected format rather than as a useful starting point.
> Arrays in train.npz / test.npz:
> ids — type str, shape (N,) — the row id, e.g. row_0a1b2c3d4e5f6071
> mixture — type uint8, shape (N, 48, 160) — the four-voice mixture; mixture[i] is the
> picture for row i
> shown — type uint8, shape (N, 2, 48, 80) — the two revealed speakers; shown[i, j] is
> revealed speaker j of row i, for j in 0…1
> pool — type uint8, shape (N, 10, 48, 80) — the lineup; pool[i, k] is lineup entry k
> of row i, for k in 0…9
> Columns in train.csv:
> id — type string, e.g. row_0a1b2c3d4e5f6071 — matches an entry of ids in train.npz
> prediction — type string, e.g. 3 7 — the two lineup positions, in 0…9, holding the two
> speakers who were in the mixture but not shown. Two distinct whole numbers separated by a
> space
> You are given 6,000 training rows (each with the answer) and must give an answer for each
> of the 4,000 test rows.
> Data provenance
> The speech comes from public-domain audiobook readings distributed through OpenSLR and
> released under the Creative Commons Attribution 4.0 (CC BY 4.0) licence. The readings are
> volunteer recordings of books that are out of copyright, made available for open speech
> research.
> The published signals are excerpted, mixed, converted to a time–frequency picture, normalised,
> quantised and perturbed before release.
> Evaluation
> Getting one of the two right is worth half. For each row, comparing your pair against the true
> pair:
> row_score = (number of your two positions that are correct) / 2
> so naming both correctly scores 1.0, one of the two scores 0.5, and neither scores 0. The
> score is the mean over the test rows:
> score = mean(row_score) over the 4,000 test rows
> Range 0–1, higher is better. Naming two lineup positions at random scores about 0.20, which
> is what the provided sample_submission.csv achieves.
> Submission format
> Submit submission.csv with exactly these two columns, in this order, one row per test id:
> id, prediction
> Example:
> id,prediction
> row_0a1b2c3d4e5f6071,3 7
> row_112233445566778a,0 4
> prediction must name exactly two distinct whole numbers in 0…9, separated by a space. A
> structural error (missing, extra or duplicate ids, wrong or extra columns, the wrong count of
> positions, a repeated position, a non-numeric, non-integer or out-of-range position) makes the
> whole submission score 0.
> Rules — what you may and may not use
> The intended solution learns, from the released training rows alone, to account for the voices
> it has been shown and identify the ones it has not. Everything below either protects that
> intent or protects the integrity of the test answers. A submission that breaks any
> prohibited rule is invalid regardless of score.
> Data — prohibited
> No external data of any kind. Do not fetch, download or otherwise bring in any speech
> corpus, audiobook collection, or any other audio. The released train.npz and train.csv
> are the only permitted training material.
> No pretrained or third-party weights. Do not use any model whose parameters were fitted
> on data other than the released training rows, and do not download weights from anywhere.
> Every learned parameter in your solution must be fitted by you, here, on the released
> training rows. Ordinary library code that contains no fitted parameters is unrestricted.
> No identifying the source. Do not attempt to locate, name or download the collection the
> speech was taken from, and do not try to match a published excerpt back to any public
> recording or to identify any speaker. The excerpts are cut, mixed, transformed, normalised,
> quantised and perturbed specifically to prevent this.
> No recovering the withheld metadata. Speaker identity, spoken content and recording
> session are deliberately withheld. Do not reconstruct them from an outside source, and do not
> obtain them from anywhere other than what the released arrays themselves contain.
> Labels — prohibited
> No test answers. The answers for the test rows are withheld and must stay that way. Do
> not source them, guess at them from outside the released data, or hand-write them.
> No labelling test rows by hand. Answers must come from a procedure that runs on the test
> inputs. Do not listen to, inspect and annotate test rows yourself, individually or in bulk,
> and do not have any person or outside service annotate them for you.
> Answer each row from its own thirteen signals. A row is answered using the mixture, the
> two shown excerpts and the ten lineup excerpts given in that row. Do not compare signals
> across different rows, and do not carry an answer from one row to another. Anything derived
> from how the rows happen to sit together in the release exploits the packaging rather than
> solving the task.
> No probing the score. Do not use repeated scored submissions to infer individual test
> answers, and do not tune anything against a score obtained that way.
> No answers baked into the submission. Predictions must be produced by your model at
> inference time. A submission.csv containing hard-coded, per-id or manually adjusted entries
> is invalid.
> Process — required
> The solution must be a learned model. Predictions must come from a model whose parameters
> were fitted on the released training rows and their answers. A fixed rule, a hand-tuned
> formula, or a similarity score with constants chosen by hand is not an acceptable solution
> even if it scores above the floor — the training answers exist to be learned from, and a
> method that does not use them is out of scope.
> Train only on training rows. Model fitting uses train.npz and train.csv only. You may
> read the test inputs to predict on them, but the test rows must never contribute to fitting
> parameters, selecting a model, or tuning anything.
> Hold out honestly. Any validation split you make must be drawn from the training rows,
> and the test answers must play no part in choosing between approaches.
> Reproducible inference. Fixed seeds and deterministic decoding — re-running your solution
> on test.npz must reproduce the same submission.csv and the same score.
> Documented method. The approach should be described clearly enough that a reader can see
> how a row is turned into a prediction and can re-run it.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Multimodal Roadside Audit Slate

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx741ver2cx3jn387z1tfe2a1h8bnv86
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat ai_baseline's score of 0.423!

Full challenge description from page:

> Multimodal Roadside Audit Slate
> Overview
> This is a from-scratch multimodal modelling task on roadside photographs and language prompts. You are
> given labelled image–prompt–response claims and must build and train a model from scratch to prioritise
> four claims from each new ten-claim panel for a limited human audit. No pretrained or foundation model
> knows the mapping: validity, roadside context and the final slate must be learned entirely from the provided
> training examples.
> Every claim combines three pieces: a transformed Indian-road photograph, a natural-language prompt and an
> opaque candidate response code. Some candidates answer their prompt correctly and some are deliberately hard
> false alternatives. You submit both a credence that each claim is valid and a priority that induces the
> four-claim audit slate. A useful slate must contain valid claims while covering varied response concepts,
> roadside contexts and context–response pairings. This is therefore a constrained set decision, not a request
> for one label or one number per photograph.
> The two output heads are mandatory. Credences without a non-constant slate score 0.0; an oracle slate with
> blind credences also scores 0.0. The grader computes every possible four-of-ten slate, giving each panel an
> exact blind expectation and an exact oracle bound.
> Real-world grounding
> The photographs show genuine traffic markers in Indian urban, rural and highway settings, including clutter,
> viewpoint changes, partial occlusion and varied illumination. The language prompt determines which fact about
> the same pixels is under review: a road message, an action, a geometric form, a colour detail, a direction or
> a setting. The response codes are opaque, so their meaning has to be learned from the training pairs.
> The multimodal grounding follows Antol et al. (2015), VQA: Visual Question Answering, Proceedings of ICCV,
> where an image and a question jointly determine a short response. The budgeted coverage component is grounded
> in Nemhauser, Wolsey and Fisher (1978), An Analysis of Approximations for Maximizing Submodular Set
> Functions—I, Mathematical Programming 14, 265–294.
> What you are given
> A public/ directory:
> public/
> train_images/              748 transformed RGB JPEG photographs
> test_images/               321 transformed RGB JPEG photographs
> train_claims.csv           4,298 labelled training claims
> test_claims.csv              880 unlabelled claims in 88 panels
> sample_submission.csv        880 rows from a weak train-only baseline
> Every served image is a 160 × 160 RGB JPEG. A private, deterministic crop, mild rotation and photometric
> change are followed by a 3 × 3 patch rearrangement, quantisation, small occlusions, noise and JPEG
> re-encoding. No served file is a byte-copy of a source image. Multiple claims may reference the same image;
> the photograph must be read together with each claim's prompt and candidate code.
> File 1 — public/train_images/ (748 files)
> <image_id>.jpg — RGB JPEG, 160 × 160 pixels. The transformed training photograph named by
> image_id in train_claims.csv.
> File 2 — public/test_images/ (321 files)
> <image_id>.jpg — RGB JPEG, 160 × 160 pixels. The transformed held-out photograph named by
> image_id in test_claims.csv. No source photograph appears on both sides of the split.
> File 3 — public/train_claims.csv (4,298 rows)
> claim_id — string. Opaque training-claim identifier; carries no information.
> image_id — string. Names train_images/<image_id>.jpg.
> prompt — string. One of six natural-language roadside queries.
> candidate_code — string. An opaque proposed response, one of rsp_00 through rsp_39.
> target_valid — integer, 0 or 1. Whether candidate_code correctly answers this image–prompt pair.
> target_context — string. The opaque roadside-context code, one of ctx_0, ctx_1, ctx_2.
> target_response — string. The correct response code for this image–prompt pair. On a valid row this
> equals candidate_code; on a false row it differs.
> File 4 — public/test_claims.csv (880 rows)
> panel_id — string. Opaque panel identifier. Each panel has exactly ten claims.
> claim_id — string. Opaque test-claim identifier; unique within the test set.
> image_id — string. Names test_images/<image_id>.jpg.
> prompt — string. The natural-language query to interpret with the photograph.
> candidate_code — string. The proposed opaque response whose validity you must assess.
> Each panel contains exactly five valid and five false claims, but which five are valid is hidden. The five
> valid claims span at least two roadside contexts and at least three response concepts.
> File 5 — public/sample_submission.csv (880 rows)
> panel_id — string. Copied from test_claims.csv.
> claim_id — string. Copied from test_claims.csv.
> priority — float. Weak train-only priority; larger values enter the four-claim slate first.
> credence — float in [0,1]. Weak train-only belief that the claim is valid.
> What you must submit
> A CSV with a header and exactly 880 rows, one per (panel_id, claim_id) pair in test_claims.csv:
> panel_id,claim_id,priority,credence
> pn_0f214ac4670ee209,cl_c36c2caf13e4bb91,1.82,0.73
> pn_0f214ac4670ee209,cl_f835cd65ac486b44,0.31,0.19
> panel_id — string. Copied from test_claims.csv.
> claim_id — string. Copied from test_claims.csv.
> priority — float. Any finite real scale is allowed; only within-panel order matters. The four largest
> values are selected. An all-identical panel has zero slate skill.
> credence — float. Your probability that the claim is valid. Values are clipped to [10^-12,1-10^-12];
> non-finite values become 0.5.
> All four columns are required. A missing required column raises ValueError. Failing to cover every claim of
> any graded panel returns 0.0. Duplicate (panel_id, claim_id) rows are tolerated and the last one wins.
> Extra rows are ignored, which lets the same file be used when the platform grades a hidden subset of panels.
> How the submission is scored
> Scoring is one deterministic grade(submission, answers) -> float using numpy and pandas only. Higher is
> better. It returns a finite number in [0,1].
> Constants:
> PANEL_SIZE = 10       # claims in every panel
> SLATE_SIZE = 4        # claims selected by priority
> CONTEXT_COUNT = 3     # fixed roadside-context vocabulary
> RESPONSE_COUNT = 40   # fixed opaque response vocabulary
> QUALITY_POWER = 3     # false-claim penalty exponent
> W_RESPONSE = 0.35     # response-coverage weight
> W_CONTEXT = 0.25      # context-coverage weight
> W_JOINT = 0.40        # context-response coverage weight
> LOWER_FRACTION = 0.75 # fraction used by the robust panel aggregate
> LOG_BASE = ln(2)      # blind credence loss; each panel is five/five
> DB = 0.035            # measured no-skill dead-band after fusion
> RAMP_POWER = 0.5      # post-correction response ramp
> TIE = 1e-10           # deterministic tie perturbation for non-constant priorities
> EPS = 1e-12           # numerical guard and perfect tolerance
> Facet A — exact-oracle audit slate
> For a selected four-claim set A, let G be the valid selected claims. Let context_i be the hidden context
> and response_i the candidate response code. Response coverage, context coverage and joint coverage are:
> q   = |G| / 4
> C_r = number of distinct response_i among G / 4
> C_c = number of distinct context_i among G / 3
> C_j = number of distinct (context_i, response_i) pairs among G / 4
> U(A) = q^3 * (0.35*C_r + 0.25*C_c + 0.40*C_j)
> The cubic q gate makes false claims expensive. Redundant valid claims also lose utility because coverage
> saturates after the first occurrence of a response, context or joint pairing.
> For each panel, the grader enumerates all choose(10,4) = 210 possible slates. It computes U_0, the exact
> mean utility over those 210 blind slates, and U_star, their exact maximum. If your priority selects A_hat:
> s_panel = clip((U(A_hat) - U_0) / (U_star - U_0), 0, 1)
> All-identical or non-finite priorities give that panel slate skill 0. Other exact ties receive a tiny
> hash-derived perturbation independent of the truth. For P graded panels, define:
> M = mean of all s_panel
> R = mean of the smallest ceil(0.75*P) values of s_panel
> S = sqrt(M * R)
> R prevents a few excellent panels from hiding weak performance across the rest.
> Facet B — claim credence
> Let y_i be hidden validity and c_i submitted credence after sanitisation. Each complete panel contains five
> valid and five false claims, so a blind c_i = 0.5 has exact loss ln(2):
> L = -mean(y_i*ln(c_i) + (1-y_i)*ln(1-c_i))
> V = clip(1 - L/ln(2), 0, 1)
> Blind, constant or anti-informative credences give V = 0; exact credences give V = 1.
> Fusion and response ramp
> Z = sqrt(S * V)
> score = 0                                      if Z <= 0.035
> score = ((Z - 0.035) / (1 - 0.035))^0.5       otherwise
> The geometric fusion makes the set decision and credence non-tradeable. An exact oracle slate on every panel
> with exact credences returns 1.0. Every measured no-skill baseline returns 0.0. There is no hard cap or
> banding, and the post-correction response is continuous.
> What different submissions score
> These values are measured with the shipped data and exact grader.
> 0.000000 — constant, independent random, all-zero and all-one submissions.
> 0.000000 — an oracle slate with blind 0.5 credences, and perfect credences with constant priorities.
> 0.111108 — a train-only language-side comparator that does not read the photographs.
> 0.129248 — a learned linear image-plus-language comparator.
> 0.136087 — the shipped small train-only multimodal baseline.
> 0.210135 — a stronger model trained from scratch on both provided modalities.
> 1.0 — an exact maximum-utility slate in every panel with exact claim credences.
> The score is invariant to CSV row order and to any common monotone rescaling of non-tied priorities within a
> panel.
> What not to use
> You must solve this with a model you build and train from scratch on the provided photographs and training
> claims. Any submission that reaches its answer by other means is disqualified.
> Banned — rule-based and non-learned approaches.
> No hand-written rules, fixed formulae, hard-coded thresholds, hand-authored decision trees or manually
> measured image/text features used as the predictor. Examples include fixed colour/shape recipes, keyword
> lookups, response-frequency rules or a hand-coded mapping from a prompt to a response code.
> No constant, near-constant or id-derived priority or credence, and nothing parsed from an opaque
> panel_id, claim_id, image_id, JPEG artefact or row order.
> No manual or human labelling of test claims, no visual answering by a person and no outsourcing to an
> annotation service.
> Banned — pretrained weights and outside data.
> No pretrained or foundation models of any kind, and no features, backbones, token representations, weights,
> pseudo-labels or initialisation learned from other data. Every learned parameter must start randomly and be
> trained only on the provided public/ data.
> No external images, road-sign collections, language corpora, catalogues or label sources; no reverse search,
> source matching or outside lookup to recover a response, context, claim validity or provenance.
> Allowed. Any model you design, train and validate yourself from scratch on the provided data; you choose
> the representation, architecture and training procedure. Unsupervised or self-supervised training on the
> provided data alone is allowed.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Reciprocal-Space Lineage Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f4jv5chcg8tstwwwcm26tc989t1za
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat alba's score of 0.718!

Full challenge description from page:

> Reciprocal-Space Lineage Reconstruction
> Overview
> An in-situ diffraction experiment does not produce one static fingerprint. As
> temperature, pressure, or composition changes, reflections move, cross, fade,
> appear, and disappear. In a multiphase specimen, the central forensic problem
> is not merely recognizing a phase: it is determining which peaks across
> experimental frames are observations of the same latent reflection and which
> reflection lineages belong to the same evolving phase.
> This challenge asks you to reconstruct that hidden hierarchy. Every row
> contains five unordered powder-diffraction peak sets measured along a monotone
> intervention coordinate. The specimen contains two to four anonymous phases.
> Peak IDs are frame-local, some true reflections are missing, and each frame
> contains artifacts. Your model must:
> identify artifact peaks;
> connect real peaks across frames into reflection tracks;
> group reflection tracks into latent phases; and
> extrapolate every recovered track to a withheld future intervention.
> This is a from-scratch structured set-tracking challenge. Phase and track
> names are arbitrary and evaluated permutation-invariantly. Strong solutions
> may use hierarchical set transformers, graph neural networks, differentiable
> matching, multi-object tracking objectives, or physics-aware latent-state
> models trained from random initialization on the released supervision.
> Benchmark Boundary
> This task is deliberately different from established diffraction benchmarks:
> | Adjacent task | Typical prediction | Difference here |
> |---|---|---|
> | Single-pattern COD/PXRD benchmarks | Space group, unit cell, coordinates, or another crystal property | No crystal property or source identity is predicted. The output is a cross-frame correspondence hierarchy. |
> | CrystalXRD-style peak indexing | Miller indices for one peak in one known structure | Source CIFs and Miller indices are absent; every row is an anonymous counterfactual multiphase series. |
> | Multiphase phase identification | Known phase labels or reference-pattern retrieval | Hidden phases have no database labels and are scored only through relational membership. |
> | Fixed-q trajectory clustering | Cluster intensity trajectories sampled at predetermined reciprocal points | Peaks move and cross, IDs are not shared across frames, and reflection correspondence must be recovered before phase grouping. |
> The benchmark unit is therefore latent reflection and phase lineage under an
> intervention, followed by out-of-frame continuation. It is not
> classification, database retrieval, static peak indexing, or image
> segmentation.
> Task
> For each test example, submit one lineage_prediction JSON object:
> {
> "assignments": [
> ["abc012def345", "phase_A", "track_07"],
> ["fed987cba654", "noise", "noise"]
> ],
> "future_q": [
> ["track_07", 0.7215]
> ]
> }
> assignments must contain exactly one record for every public peak:
> [peak_id, predicted_phase_label, predicted_track_label]
> future_q must contain exactly one record for every predicted real track:
> [predicted_track_label, q_at_future_u]
> Phase and track labels are invented by the solver. Their literal names do not
> need to match training labels. Only the induced relationships matter.
> Input Representation
> series_json has this structure:
> {
> "fields": ["peak_id", "q", "log_intensity", "width"],
> "frames": [
> {
> "u": -1.0,
> "peaks": [
> ["abc012def345", 0.7142, -0.38, 0.0019],
> ["fed987cba654", 0.8901, -1.42, 0.0031]
> ]
> }
> ],
> "future_u": 1.4
> }
> Every series contains five frames with:
> u = -1.0, -0.5, 0.0, 0.5, 1.0
> peak_id - anonymous 12-character identifier unique within the example.
> q - measured reciprocal spacing in inverse angstroms.
> log_intensity - log-scaled observed peak intensity.
> width - observed peak width in reciprocal-spacing units.
> u - dimensionless monotone intervention coordinate.
> future_u - intervention coordinate for the required extrapolation.
> Peak order has no meaning. IDs do not correspond across frames. One latent
> reflection can be absent from one or more frames.
> Output Constraints
> Every public peak ID must occur exactly once in assignments.
> An artifact must use ["peak_id", "noise", "noise"].
> A real track may contain peaks from multiple frames but must belong to one
> predicted phase.
> A predicted phase may contain multiple tracks.
> future_q must contain every predicted real track exactly once.
> Every future q must be finite and between 0.001 and 20.0.
> Labels must match [A-Za-z0-9_-]{1,32}.
> The complete prediction string may contain at most 80,000 characters.
> The number of predicted phases and tracks is not supplied. It must be inferred.
> Difficulty Regimes
> The hidden set is balanced across five regimes:
> two_phase_smooth - two phases under moderately smooth strain with missing
> reflections and artifacts.
> three_phase_crossing - three phases with frequent cross-phase peak-order
> crossings.
> four_phase_sparse - four phases with severe dropout and many artifacts.
> metric_twin_overlap - three phases with closely related reciprocal
> fingerprints occupying overlapping q ranges.
> birth_death_transition - one phase fades while another emerges.
> The regime label is available in training but hidden in test.
> Dataset
> train.csv
> | Column | Type | Description |
> |---|---|---|
> | `example_id` | string | Unique 16-character row ID. |
> | `series_json` | JSON string | Five public intervention frames. |
> | `lineage_json` | JSON string | Target assignments and future continuation. |
> | `family` | string | Training difficulty regime. |
> There are 6,000 training rows, exactly 1,200 per regime.
> test.csv
> | Column | Type | Description |
> |---|---|---|
> | `example_id` | string | Unique 16-character row ID. |
> | `series_json` | JSON string | Five public intervention frames. |
> There are 1,500 hidden rows, exactly 300 per regime.
> sample_submission.csv
> The sample assigns every peak to its own phase and track. It is structurally
> valid but encodes no lineage and scores exactly 0.0.
> Source Construction and Leakage Controls
> Each latent phase is built by:
> selecting two different source lattices from one crystal system;
> interpolating their normalized direct metrics with nonzero weight;
> counterfactually rescaling the resulting cell;
> applying a nonzero initial strain; and
> evolving it through a phase-specific linear-plus-quadratic strain path.
> Reciprocal-shape source groups are split before example generation. There are
> 5,925 eligible training groups and 1,484 held-out groups with zero overlap.
> Prepared solver files exclude COD accessions, formulas, source groups,
> space-group labels, Miller indices, and generation parameters.
> External COD matching therefore cannot return a generated phase or its target
> lineage.
> Evaluation
> The Reciprocal Lineage Score is higher-is-better and lies in [0, 1].
> All relational metrics are invariant to phase and track label renaming.
> 1. Reflection-track pair F1
> Every unordered pair of observed peaks is considered positive when both peaks
> belong to the same real reflection track. Artifact peaks behave as independent
> singletons.
> TrackPairF1 =
> 2 * correctly_co_tracked_pairs
> /
> (true_co_tracked_pairs + predicted_co_tracked_pairs)
> This penalizes both broken lineages and incorrect mergers.
> 2. Phase pair F1
> The same pairwise calculation is applied to latent phase membership:
> PhasePairF1 =
> 2 * correctly_co_phased_pairs
> /
> (true_co_phased_pairs + predicted_co_phased_pairs)
> It rewards hierarchical recovery without requiring arbitrary phase IDs to
> match.
> 3. Artifact F1
> ArtifactF1 is ordinary binary F1 over peaks assigned to noise.
> 4. Future continuation
> Predicted and true tracks are aligned one-to-one in descending public-overlap
> order. A match is eligible only when its public overlap is at least:
> max(2, ceil(0.40 * true_track_observations))
> For an eligible track:
> relative_error =
> abs(predicted_future_q - true_future_q) / true_future_q
> ContinuationTrack =
> exp(-(relative_error / 0.015)^2)
> Unmatched or insufficiently supported true tracks receive zero.
> FutureContinuation is the mean over all true tracks.
> 5. Joint lineage consistency
> JointLineage =
> TrackPairF1 * PhasePairF1 * FutureContinuation
> This term requires reflection identity, phase hierarchy, and physical
> continuation to succeed together.
> Row score
> RowScore =
> 0.25 * TrackPairF1
> + 0.15 * PhasePairF1
> + 0.10 * ArtifactF1
> + 0.15 * FutureContinuation
> + 0.35 * JointLineage
> Weak-regime robustness
> Mean RowScore is computed for each hidden regime. WeakRegime is the mean
> of the two lowest regime scores.
> Final formula
> score =
> 0.85 * mean(RowScore)
> + 0.15 * WeakRegime
> An exact oracle scores 1.0. Relabeling every phase and track leaves its score
> at 1.0. Invalid prediction JSON scores zero for its individual row;
> structurally invalid CSV submissions are rejected.
> Submission Workflow Checklist
> To avoid a no-score run, build and submit the file in this exact shape:
> Read test.csv.
> For every row, parse series_json and collect every public peak_id.
> Create one JSON object with keys assignments and future_q.
> Store that JSON object as one CSV cell in the lineage_prediction column.
> Write a file named submission.csv with exactly two columns:
> example_id,lineage_prediction. 6. Validate the file with the platform submission checker. 7. After validation succeeds, submit the same submission.csv for grading.
> Important: validation only checks that the file is acceptable. Validation is
> not the final graded submission.
> If modeling fails, sample_submission.csv is a valid fallback format. It
> scores 0.0, but it proves the required CSV and JSON structure.
> Submission
> Submit submission.csv with exactly these columns in this order:
> | Column | Type | Description |
> |---|---|---|
> | `example_id` | string | ID copied from `test.csv`. |
> | `lineage_prediction` | JSON string | Complete lineage and continuation prediction. |
> Example:
> example_id,lineage_prediction
> 001122aabbccddee,"{""assignments"":[[""abc012def345"",""phase_A"",""track_07""]],""future_q"":[[""track_07"",0.7215]]}"
> Requirements:
> exactly 1,500 rows;
> every test ID exactly once;
> no missing or extra IDs;
> exact column order: example_id,lineage_prediction;
> CSV format only.
> From-Scratch Rule
> Trainable models must be initialized from scratch using released supervision.
> Do not use pretrained diffraction, spectroscopy, materials, vision, or
> foundation-model encoders as the main predictor. Physics-based features,
> matching algorithms, and crystallographic calculations may be used as
> components of a from-scratch learned system.
> What Not To Use
> Do not recover or search for hidden COD source records.
> Do not key predictions to example IDs, peak IDs, JSON order, or CSV order.
> Do not manually assign hidden examples.
> Do not treat the regime name, phase count, track count, or source structure
> as a hidden class to retrieve.
> Do not assume nearest q is a complete lineage solution: peaks cross,
> disappear, emerge, and overlap across phases.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Multimodal Actuator Translation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx705rgpfre1mw2gtawhyjmd1d8bntew
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Easy
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: multimodal, Dataset source is visible after the challenge closes., Leaderboard, (5)
- Best/top context found: Beat douglas's score of 0.808!

Full challenge description from page:

> Multimodal Actuator Translation
> Overview
> Modern robots, scientific instruments, and adaptive machines often inherit hardware that was not
> designed to share a control language. One device accepts an optical control vector, another exposes
> an acoustic interface, and a third is driven through a load controller. Their numeric commands are
> not aligned, yet equivalent interventions can sometimes be recognized from what the system does.
> This challenge turns that problem into a controlled research benchmark for multimodal system
> identification. Every object family has three private actuator dialects named optic, sonic, and
> load. A four-value command in any dialect produces one underlying physical intervention and an
> eight-value canonical response. You never observe that canonical response directly at test time.
> Instead, you receive one of three very different measurements:
> optic observations are four-frame, four-channel spatial fields.
> sonic observations are time-frequency response maps.
> load observations are six-channel temporal traces.
> Six calibration interventions are shown for all three interfaces of each family. Matching
> anchor_id values identify measurements caused by the same intervention, but the commands differ
> across interfaces. A query then gives a source command and source observation and asks you to act
> through a different target interface.
> Your system must solve four linked problems:
> Decode a modality-specific observation into a shared behavioral representation.
> Infer a new family's hidden actuator dialect from only six cross-interface demonstrations.
> Produce a target command whose executed behavior matches the source behavior.
> Detect when exact translation is impossible and certify the closest achievable response.
> This is not ordinary cross-modal retrieval. The predicted command is executed by a sealed simulator
> inside the evaluator. A plausible-looking code receives no credit if it causes the wrong behavior.
> Conversely, multiple commands that cause equivalent behavior receive equivalent credit. This makes
> the task a benchmark for behavior-level alignment, few-shot inverse control, reachability
> estimation, and calibrated counterfactual prediction.
> The research object is the translator itself. Standard multimodal benchmarks usually classify,
> retrieve, or predict one sensory view from another. Cross-embodiment alignment usually learns a
> shared action representation with a fixed embodiment mapping. Here every evaluation family creates
> a new actuator language, the submitted intervention is executed, exact translation may be
> physically impossible, and the model must quantify that impossibility against the target actuator's
> reachable set. Success requires learning reusable system-identification machinery rather than a
> single global alignment.
> Why This Is Difficult
> The three sensing channels do not share pixels, frequency bins, channel layouts, or summary
> statistics. Information is encoded in spatial motion, joint time-frequency geometry, and temporal
> event order. Global averages and nearest-neighbor lookup discard important structure.
> Every family has fresh private permutations, signs, offsets, ranges, nonlinear warps, and
> cross-coordinate couplings. Family identifiers are opaque and the test families never occur in the
> training set. The test set also occupies a held-out physical regime, so memorizing the training
> population is insufficient.
> The target interface may not be able to reproduce the source response. About one third of queries
> are constructed to be unreachable. A useful model therefore cannot always force a command match;
> it must distinguish translation error from a genuine boundary of the target actuator and estimate
> the irreducible gap.
> Finally, each interface folds one disclosed control coordinate: positive and negative roots on that
> coordinate execute exactly the same latent intervention. Actions are therefore explicitly
> many-to-one and inverse translations can be one-to-many. target_code is a witness, not necessarily
> the only correct command. Regressing directly to that one witness can be inferior to learning the
> response manifold and solving for behavioral equivalence.
> Dataset
> The prepared participant data contains 720 disjoint object families, with 576 training families and
> 144 test families. Each family has six anchors observed through all three interfaces and eighteen
> translation queries. This produces 10,368 training queries, 2,592 test queries, 12,960 calibration
> rows, and 25,920 float16 observation arrays.
> train_calibrations.csv contains 10,368 calibration rows. Its columns are family_id as a string
> family identifier, anchor_id as a string equivalence-group identifier, interface as one of
> optic, sonic, or load, action_code as four space-separated floating-point values,
> observation_id as a string observation identifier, and media_path as the relative path to the
> matching NumPy array.
> test_calibrations.csv contains 2,592 calibration rows with the same six columns and the same
> meaning. These are legitimate per-family demonstrations and should be used for system
> identification at inference time.
> train_queries.csv contains 10,368 labeled queries. Its input columns are id, family_id,
> source_interface, target_interface, source_code, source_observation_id, and
> source_media_path. It also contains the four training targets reachable, target_code,
> response, and gap.
> test_queries.csv contains 2,592 unlabeled queries with the seven input columns only. The id
> column is the required submission key.
> sample_submission.csv contains one valid row for every test query and demonstrates the exact CSV
> schema. Its first row is a real answer so the file always produces a valid nonzero score; it is not
> evidence about any other row.
> metric_config.json records the public score constants and vector sizes.
> The media/train/ and media/test/ folders contain the observation arrays. An optic file has shape
> (4, 4, 48, 48) and values in [0, 1]. A sonic file has shape (64, 64) and values in [0, 1].
> A load file has shape (128, 6) and values in [-1, 1]. Every array uses NumPy float16 storage and
> must be loaded with allow_pickle=False.
> Targets
> For every test query, predict all four target fields.
> reachable is a floating-point probability in [0, 1] that the target interface can match the
> source response within the benchmark tolerance.
> target_code is a single string containing exactly four space-separated floating-point values in
> [-1, 1]. It is the command that the sealed evaluator will execute through the target interface.
> response is a single string containing exactly eight space-separated floating-point values in
> [-1, 1]. It is your estimate of the canonical response represented by the source observation.
> gap is a floating-point value in [0, 2]. It estimates the root-mean-square response distance
> between the source behavior and the best behavior reachable through the target interface.
> Evaluation
> Let p be the submitted reachability probability and y the true reachability label. Let r_hat
> be the submitted response, r_star the desired canonical response, c_hat the submitted target
> code, and E(c_hat) the canonical response obtained by executing that code in the hidden target
> interface. Let g_hat be the submitted gap and g_star the oracle best-achievable gap.
> The evaluator computes four row-level losses:
> reachability_loss = (p - y)^2
> response_loss = RMSE(r_hat, r_star) / 2
> execution_loss = max(0, RMSE(E(c_hat), r_star) - g_star - 0.000002) / 2
> gap_loss = abs(g_hat - g_star) / 2
> Subtracting g_star from the execution distance is essential. A reachable query has a near-zero
> oracle gap, so the submitted command must closely reproduce the desired behavior. For an
> unreachable query, any command that reaches the oracle boundary is treated as optimal even when it
> differs from the stored witness code. This is how behaviorally equivalent and equally optimal codes
> receive equivalent credit.
> The weighted row loss is
> L_row = 0.25 * reachability_loss + 0.25 * response_loss + 0.40 * execution_loss + 0.10 * gap_loss.
> The final loss L is the arithmetic mean of L_row over all test queries. The leaderboard score is
> score = clip(exp(-8 * L), 0.0001, 1.0).
> Higher is better. The minimum reported score is 0.0001 and the maximum is 1.0. An exact answer-key
> submission scores 1.0.
> Submission Format
> Submit a CSV with exactly 2,592 rows and exactly these columns in this order:
> id,reachable,target_code,response,gap
> Identifiers must match test_queries.csv exactly. Vector cells must be plain space-separated
> decimal numbers, not JSON arrays, commas, brackets, or NumPy displays. A valid example is:
> id,reachable,target_code,response,gap
> qry_example,0.73124500,"0.11400000 -0.22000000 0.50800000 0.03100000","0.12000000 -0.08000000 0.44000000 0.31000000 -0.27000000 0.52000000 0.09000000 -0.11000000",0.04200000
> Malformed columns, duplicate or missing identifiers, nonnumeric tokens, non-finite values, incorrect
> vector lengths, or out-of-range values are rejected.
> Research Directions
> Promising approaches include modality-specific convolutional or transformer encoders, contrastive
> alignment across anchor triples, set encoders over the six demonstrations, amortized system
> identification, differentiable inverse control, conditional density estimation, and calibrated
> reachability heads. The code output can be produced directly or refined by an optimizer over a
> learned behavioral surrogate.
> The strongest organizer check deliberately tested a generator-aware, fold-aware structural
> translator on the official 144-family test split. A global mean scored 0.3278, code-only
> interpolation scored 0.3256, a handcrafted-summary Ridge and response-space RBF pipeline scored
> 0.4884, and a calibration-only structural polynomial attack scored 0.5991. A trained
> position-preserving multimodal encoder paired with the same structural translator scored 0.6852.
> These measurements show both a serious non-neural attack and a material benefit from genuine
> multimodal training. The trained system reduced remaining score error by 21.5 percent and underlying
> weighted prediction error by 26.2 percent relative to the strongest simple attack.
> Compute Environment
> This Diamond Challenge is configured for one NVIDIA A10G GPU with 24 GB VRAM, 10 CPU cores, 64 GB
> system RAM, and a six-hour total budget for training and inference. The intended solution tier is
> from-scratch GPU training over all three modalities; CPU components may be used, but CPU-only
> execution is not the target provision.
> Allowed And Prohibited
> Allowed:
> Train models from scratch using the provided training queries and calibration observations.
> Condition on all provided test calibration rows, including per-family interpolation, optimization,
> or system identification based on those labeled demonstrations.
> Use ensembles, learned surrogates, differentiable solvers, and deterministic post-processing within
> the compute budget.
> Prohibited:
> Use external datasets, pretrained weights, foundation-model APIs, or network services.
> Recover, infer, or obtain the hidden test labels or private family states from files outside the
> prepared participant data.
> Update a global representation using unlabeled test query observations, perform transductive
> training on the test queries, or use leaderboard feedback as supervision.
> Manually encode test answers, exploit evaluator infrastructure, or submit outputs not produced by
> the declared pipeline.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Anchor-Conditioned Emission Peak Drift

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dqycbv11k0gvjsw6q5rcrqd8bqma9
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: feature-engineering, large-scale, Dataset source is visible after the challenge closes., Leaderboard
- Best/top context found: Beat dp2406's score of 66.034!

Full challenge description from page:

> Anchor-Conditioned Emission Peak Drift
> Overview
> Remote laser spectrometers often compare multiple statistical summaries of repeated measurements. A detailed reference analysis may already exist for one aggregate, while a newly computed aggregate is retained only as compressed telemetry. The scientific question is then not “what is the entire new spectrum?” but how did its important peak morphology move relative to the trusted reference?
> Every challenge row contains an anchor aggregate and a query aggregate from the same real planetary-rover laser-spectroscopy target. The anchor includes its known 12-zone peak signature. For both aggregates, you receive masked 96-bin intensity and curvature streams plus 12 zone loads. No query morphology sketch is provided: its fine peak properties must be inferred from changes in the compressed physical signals.
> Your objective is to predict a directed 12-zone drift field from anchor to query. For each wavelength zone, determine whether the hidden query peak moved left or right, whether the peak became more or less prominent, and whether it became sharper or broader.
> In plain language: use a known anchor signature and two compressed aggregate spectra to predict how the query peak changed in every wavelength zone.
> This is a From Scratch paired-signal challenge. Every learned embedding, encoder, attention layer, convolution, and prediction head must be initialized from random weights and trained only with the supplied competition files. Pretrained spectroscopy, chemistry, materials, planetary-science, remote-sensing, vision, language, or general-purpose representations are not permitted.
> The data comes from real calibrated laser-induced breakdown spectroscopy measurements. Original measurement names, source filenames, mission timestamps, coordinates, elemental annotations, composition estimates, and high-resolution test spectra are absent. Participant identifiers are fresh opaque codes.
> Anchor and Query Views
> Each physical measurement target has two statistical aggregate spectra, represented by direction codes:
> V00: the first aggregate is the anchor and the second is the query;
> V01: the second aggregate is the anchor and the first is the query.
> Training contains both reciprocal directions for every training target. This teaches how a transition reverses when anchor and query are exchanged.
> Test contains only one deterministic direction for each held-out physical target. The reverse test view is not provided, because its detailed anchor signature would disclose the hidden query morphology. All examples from one physical target stay in one split.
> What You Must Predict
> The spectrum is divided into 12 fixed wavelength zones, z00 through z11, ordered from lower to higher wavelength. Predict three signed transition columns for every zone.
> Peak migration state
> migration_state_zXX is an integer in {-2, -1, 0, 1, 2}:
> -2: the query peak moved left by at least three fine slots;
> -1: the query peak moved left by one or two fine slots;
> 0: the strongest fine peak remained in the same slot;
> 1: the query peak moved right by one or two fine slots;
> 2: the query peak moved right by at least three fine slots.
> “Left” means toward a lower wavelength, and “right” means toward a higher wavelength. Each hidden fine slot spans 32 calibrated source channels.
> Prominence direction
> prominence_direction_zXX is an integer in {-1, 0, 1}:
> -1: prominence decreased;
> 0: prominence tier was unchanged;
> 1: prominence increased.
> Sharpness direction
> sharpness_direction_zXX is an integer in {-1, 0, 1}:
> -1: sharpness decreased and the peak became broader or less distinct;
> 0: sharpness tier was unchanged;
> 1: sharpness increased.
> Together, the 36 integers form a fixed-width directed peak-drift field.
> Input Columns
> id — string — fresh identifier for one directed anchor-query case.
> pair_code — string — opaque physical-target key. It occurs twice per training pair and once per test pair.
> direction_code — string — V00 or V01, identifying the anchor-query orientation.
> anchor_location_stream — string — 12 known fine peak slots, each from 0 through 15.
> anchor_prominence_stream — string — 12 known anchor prominence tiers, each from 0 through 3.
> anchor_sharpness_stream — string — 12 known anchor sharpness tiers, each from 0 through 3.
> anchor_intensity_stream — string — 96 quantized anchor-intensity values.
> query_intensity_stream — string — 96 quantized query-intensity values.
> anchor_curvature_stream — string — 96 signed anchor-curvature values.
> query_curvature_stream — string — 96 signed query-curvature values.
> anchor_zone_load_stream — string — 12 relative anchor zone loads.
> query_zone_load_stream — string — 12 relative query zone loads.
> The 96-position streams contain 12 consecutive zones of eight bins each. Position 8 × z + b corresponds to coarse bin b of zone z.
> Intensity and zone-load values range from 0 through 7. Curvature values range from -3 through 3. In the 96-position streams, 9 marks one unavailable bin per zone. Anchor and query masking patterns may differ.
> Why It Is Difficult
> The query's fine peak locations, prominence tiers, and sharpness tiers are not supplied, even in low-bit form. They must be inferred from spectral changes and cross-zone structure relative to the known anchor.
> Each visible spectral bin averages 64 hidden calibrated channels, while one fine peak slot spans 32 channels. The observed bins therefore cannot directly reveal a one- or two-slot movement. Prominence and sharpness transitions depend on sub-bin structure removed during compression.
> Training supplies reciprocal directions, but test supplies only one orientation per unseen target. Memorizing pair codes or copying the anchor cannot recover the query transition.
> Dataset
> train.csv
> Contains 48,926 directed rows from 24,463 physical targets. Both reciprocal directions are present for every training target. The file contains the 12 input columns and all 36 transition targets.
> test.csv
> Contains 6,116 rows from 6,116 held-out physical targets. Only one direction is present for each target, and the file contains the 12 input columns.
> sample_submission.csv
> Contains every test identifier and all 36 target columns in the required order, initialized to zero.
> metadata.json
> Documents stream dimensions, token grammars, transition states, masking counts, and split sizes. It contains no source name, source link, original target identifier, or held-out group list.
> Evaluation
> The Anchor-Conditioned Drift Score combines class-balanced migration recovery, class-balanced morphology-direction recovery, and exact local transition agreement.
> Migration term
> For migration column j and state s, define
> R_m(j,s) = correctly predicted rows whose true migration state is s / rows whose true migration state is s.
> Let S_j be the migration states present in the hidden answers for column j. Then
> M = mean over the 12 migration columns j of [mean over s in S_j of R_m(j,s)].
> Prominence-direction term
> Using the same macro-recall construction over the states -1, 0, and 1:
> P = mean balanced recall over the 12 prominence-direction columns.
> Sharpness-direction term
> H = mean balanced recall over the 12 sharpness-direction columns.
> Joint transition term
> For row i and zone z, let T(i,z) = 1 only when migration, prominence direction, and sharpness direction are all predicted exactly; otherwise T(i,z) = 0.
> T = mean over all rows i and zones z of T(i,z).
> Final score
> Score = 100 × (0.25 × M + 0.175 × P + 0.175 × H + 0.40 × T)
> The metric ranges from 0 to 100, and higher is better. Balanced terms prevent unchanged transitions from dominating, while the 40% joint term rewards physically coherent recovery of the complete local transition rather than 36 disconnected guesses. There is no score cap, hidden multiplier, or test-dependent remapping.
> Submission Format
> Submit one CSV with exactly 37 columns in the order shown by sample_submission.csv: id, the 12 migration-state columns, the 12 prominence-direction columns, and the 12 sharpness-direction columns. Include every test identifier exactly once.
> All values must be finite integers in their stated ranges. A row containing any missing, non-integer, infinite, or out-of-range value receives zero credit for every component. Extra columns, reordered columns, missing rows, duplicate identifiers, and unknown identifiers are rejected.
> Example using real test identifiers:
> id,migration_state_z00,migration_state_z01,migration_state_z02,migration_state_z03,migration_state_z04,migration_state_z05,migration_state_z06,migration_state_z07,migration_state_z08,migration_state_z09,migration_state_z10,migration_state_z11,prominence_direction_z00,prominence_direction_z01,prominence_direction_z02,prominence_direction_z03,prominence_direction_z04,prominence_direction_z05,prominence_direction_z06,prominence_direction_z07,prominence_direction_z08,prominence_direction_z09,prominence_direction_z10,prominence_direction_z11,sharpness_direction_z00,sharpness_direction_z01,sharpness_direction_z02,sharpness_direction_z03,sharpness_direction_z04,sharpness_direction_z05,sharpness_direction_z06,sharpness_direction_z07,sharpness_direction_z08,sharpness_direction_z09,sharpness_direction_z10,sharpness_direction_z11
> AD0006E0A276F9B5,0,-1,1,0,2,-2,0,1,0,-1,2,0,1,0,-1,1,0,1,-1,0,1,0,-1,0,0,1,0,-1,1,0,1,-1,0,1,0,-1
> AD000C4B223FAF4C,1,0,-1,2,0,1,-2,0,1,0,-1,0,0,-1,1,0,1,-1,0,1,0,-1,1,0,-1,0,1,0,-1,1,0,1,-1,0,1,0
> From-Scratch Rules
> Train only on the supplied competition files.
> Initialize every learned representation and prediction component from random weights.
> Do not use pretrained spectroscopy, chemistry, materials, planetary-science, remote-sensing, vision, language, multimodal, or foundation-model encoders or embeddings.
> Do not use external datasets, spectral libraries, atomic-line databases, source-recording searches, removed metadata, or high-resolution source spectra.
> Original neural architectures, learned token embeddings, hand-engineered spectral features, categorical lookup models, and classical models trained solely on train.csv are permitted.
> GPU training is recommended: training contains 48,926 directed cases, 444 ordered signal values per row, and 36 coupled transition targets.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Wrapped Phase Closure Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7274k4m5qjdy2tdyph6fqht18bqft9
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: image, text, multimodal, Dataset source is visible after the challenge closes.
- Best/top context found: Beat jesuisnadi's score of 0.529!

Full challenge description from page:

> Overview
> Recover the spatial closure structure of a slowly moving terrain region from three synchronized interferometric views. For every case, predict a 6 by 6 signed phase-flow tensor, a 4 by 4 connectivity matrix between image quadrants, and one closure state. The three input files encode the same observation as wrapped phase, phase sine, and phase cosine.
> Wrapped radar phase contains discontinuities whenever values cross the phase boundary. A coherent creeping region can therefore look fragmented in one encoding while remaining connected across another. The task is to learn a phase-aware representation that distinguishes a real spatial boundary from a wrapping discontinuity and then summarizes the region's topology. Models are trained using only the supplied examples, so the benchmark measures whether useful phase structure can be learned from scratch rather than imported from ordinary natural-image features.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Labeled interferometric cases. |
> | `test.csv` | Interferometric cases whose targets are withheld. |
> | `sample_submission.csv` | Submission schema and baseline values. |
> | `phase_views/` | Opaque TIFF images for the three synchronized phase encodings. |
> The three paths in one row refer to the same geographic observation. Every prepared view is a 128 by 128 RGB TIFF. TIFF encoding retains phase contrast without JPEG artifacts.
> All three public views receive the same deterministic crop, rotation, and mirror transform so their pixels remain spatially registered. Mild view-specific radiometric calibration removes source-byte identity without changing the phase relationship.
> Prepared Data Summary
> | Quantity | Value |
> |---|---:|
> | Training rows | 6,746 |
> | Test rows | 1,641 |
> | Training `closed` | 1,956 |
> | Training `single_breach` | 4,498 |
> | Training `fragmented` | 292 |
> | Test `closed` | 466 |
> | Test `single_breach` | 1,086 |
> | Test `fragmented` | 89 |
> The split keeps perceptually related wrapped-phase observations together. No TIFF payload hash occurs in both splits.
> CSV Columns
> | Column | Present in | Data type | Description |
> |---|---|---|---|
> | `case_id` | Train and test | String | Opaque unique identifier. |
> | `wrapped_phase_path` | Train and test | String | Relative path to the wrapped-phase TIFF. |
> | `sine_phase_path` | Train and test | String | Relative path to the sine-of-phase TIFF. |
> | `cosine_phase_path` | Train and test | String | Relative path to the cosine-of-phase TIFF. |
> | `phase_flow_tensor` | Train only | JSON integer matrix, shape 6 by 6 | Dominant signed wrapped-phase progression inside the moving region. `-1` is negative progression, `1` is positive progression, and `0` means insufficient moving-region coverage. Rows run top to bottom and columns left to right. |
> | `island_connectivity_matrix` | Train only | JSON integer matrix, shape 4 by 4 | Connectivity among top-left, top-right, bottom-left, and bottom-right quadrants, in that order. Entry `[i,j]` is `1` when one labeled moving-region component touches both quadrants, else `0`. Diagonal entries mark whether that quadrant contains moving-region evidence. |
> | `closure_state` | Train only | Categorical string | `closed`, `single_breach`, or `fragmented`. |
> closed means the region does not touch the image boundary. single_breach means the region reaches the image boundary. fragmented means four or more disconnected region components are present.
> Example targets:
> phase_flow_tensor = [[0,0,0,0,0,0],[0,1,1,-1,0,0],[0,1,1,-1,-1,0],[0,-1,-1,1,1,0],[0,0,-1,1,0,0],[0,0,0,0,0,0]]
> island_connectivity_matrix = [[1,1,0,0],[1,1,0,1],[0,0,0,0],[0,1,0,1]]
> closure_state = single_breach
> Evaluation
> The Phase Closure Reconstruction Score is:
> Score = 0.42 * PhaseFlowScore
> + 0.40 * ConnectivityScore
> + 0.18 * ClosureStateScore
> Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> PhaseFlowScore
> For one sample, hidden phase-flow tensor Y and prediction P use entry weight 3.0 where Y is nonzero and 1.0 elsewhere.
> entry_agreement = sum(w[i,j] * I(Y[i,j] = P[i,j])) / sum(w[i,j])
> sign_agreement = mean(I(sign(Y[i,j]) = sign(P[i,j]))) over cells where Y[i,j] != 0
> sample_phase_flow = 0.24 * entry_agreement
> + 0.16 * sign_agreement
> + 0.60 * I(Y = P)
> If a hidden tensor has no nonzero cells, sign_agreement is 1.0. PhaseFlowScore is the mean sample score.
> ConnectivityScore
> Only the six entries above the diagonal are used for partial agreement because the matrix is symmetric.
> pair_agreement = mean(I(Y[i,j] = P[i,j])) for i < j
> sample_connectivity = 0.30 * pair_agreement + 0.70 * I(Y = P)
> ConnectivityScore is the mean sample score.
> ClosureStateScore
> Compute recall independently for every closure state present in the hidden answers, then average those recalls equally. Invalid states are incorrect.
> Malformed matrices receive zero for their component.
> Submission Format
> Save predictions to ./working/submission.csv with exactly:
> case_id,phase_flow_tensor,island_connectivity_matrix,closure_state
> Example:
> case_id,phase_flow_tensor,island_connectivity_matrix,closure_state
> pc42c10f645a77c008a229,"[[0,0,0,0,0,0],[0,1,1,-1,0,0],[0,1,1,-1,-1,0],[0,-1,-1,1,1,0],[0,0,-1,1,0,0],[0,0,0,0,0,0]]","[[1,1,0,0],[1,1,0,1],[0,0,0,0],[0,1,0,1]]",single_breach
> The grader requires exact column order and the exact hidden ID set. It rejects duplicate IDs, extra rows, extra columns, and unknown IDs. Matrix text is limited to 360 characters and must contain integer values in the documented shape and range.
> Method Requirements
> Learn model parameters only from the supplied training examples. Pretrained image weights and external phase datasets are not permitted. GPU training is appropriate for learning the joint wrapped, sine, and cosine representation within the 30-minute A10G runtime.
> What Not To Use
> Do not use external source matching, geographic lookup, reverse image search, or source archive identifiers.
> Do not derive answers from case_id, path names, row order, TIFF byte size, or file hashes.
> Do not retrieve labels from public mirrors or reconstruct source filenames from image content.
> Do not hardcode hidden-region templates or hidden-answer patterns.
> Do not exploit malformed submissions, duplicate IDs, extra columns, or grader edge cases.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Drum Feel Microtiming Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79s18n5jzkytyxknhx21vcwd8bqfxf
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat zzz_grs's score of 0.341!

Full challenge description from page:

> Drum Feel Microtiming Reconstruction
> Overview
> This is a from-scratch / fine-tuning sequence-modeling challenge over expressive drum performances. For each row, you are given a two-bar drum pattern after it has been snapped to a simple sixteenth-note grid, plus noisy per-hit controller probes. Your task is to reconstruct the hidden human feel for every visible hit: whether that hit was played early or late, and how softly or strongly it was played.
> In plain terms: the notes are already visible, but the groove is missing. You must denoise shifted timing and energy clues, then predict the timing and velocity residuals that make a quantized drum pattern feel like a human performance.
> The source data consists of real MIDI drum performances recorded from drummers playing to a click track on an electronic drum kit. The challenge uses the MIDI-only release, not audio. Prepared rows hide all source filenames, drummer IDs, session IDs, and exact MIDI positions. Train and hidden test rows come from disjoint source performances, and hidden targets are built from source-new matched residual mosaics rather than directly exposing the original public grid window.
> This is not audio transcription, beat tracking, genre classification, or ordinary next-token language modeling. It is an expressive-performance reconstruction task: learn timing and dynamics from quantized symbolic rhythm, style hints, tempo, local drum context, and training examples.
> Dataset files
> train.csv contains 4,500 rows.
> id: string. Unique training row ID.
> pattern_strip: string. Compact 32-slot drum grid summary. Each row segment is Dxx:.... and row segments are separated by |.
> grid_shape: string. Always drumsx32, meaning drum aliases by 32 sixteenth-note slots.
> drum_cards: JSON list. Row-local drum aliases and their public drum roles.
> hit_cards: JSON list. One visible hit card for every hit that must be predicted.
> tempo_bpm: integer. Source performance tempo.
> tempo_bucket: string. One of slow, medium, bright, or fast.
> style_hint: string. Coarse source style label such as funk, rock, or latin.
> beat_type: string. beat or fill.
> density_bucket: string. sparse, medium, busy, or dense.
> max_hits: integer. Number of hit tokens required in the answer for this row.
> target_feel: string. Training-only answer ledger.
> test.csv contains 1,000 rows and has the same columns except target_feel.
> sample_submission.csv contains:
> id: string. Test row ID.
> predicted_feel: string. Empty dummy value. The sample scores 0.
> Input field schemas
> pattern_strip is a compact grid display:
> Each segment has the form Dxx:cccccccccccccccccccccccccccccccc.
> Dxx is a row-local drum alias from drum_cards.
> The 32 characters after : correspond to slots 0 through 31.
> . means no hit from that drum in that slot.
> 1 means one hit from that drum in that slot.
> 2 means two or more hits from that drum in that slot.
> drum_cards is a JSON list. Each item has:
> drum: string. Row-local drum alias such as D01.
> role: string. Public drum role, for example kick, snare, closed_hat, open_hat, ride, crash, high_tom, mid_tom, low_tom, or pedal_hat.
> description: string. Short readable version of the role.
> hit_cards is a JSON list. Each item has:
> hit: string. Hit alias such as H00. Every hit alias must appear exactly once in the submitted ledger.
> slot: integer. Sixteenth-note slot from 0 to 31 within the two-bar window.
> drum: string. Row-local drum alias from drum_cards.
> slot_phase: string. bar_downbeat, beat, eighth, or off_sixteenth.
> simultaneous_hits: integer. Number of visible hits sharing this slot.
> prev_slot_gap: integer. Slot distance to the previous hit, capped at 9.
> next_slot_gap: integer. Slot distance to the next hit, capped at 9.
> timing_probe: integer from 0 to 31. A noisy timing-side-channel code. Higher values usually indicate later hits, but the distribution is shifted by drum role, phase, style, tempo, density, and deterministic noise.
> energy_probe: integer from 0 to 31. A noisy velocity-side-channel code. Higher values usually indicate stronger hits, but the distribution is shifted by drum role, phase, style, tempo, density, and deterministic noise.
> Output grammar
> Submit one predicted_feel string per test row.
> A prediction is a space-separated ledger with exactly one token for every hit in that row.
> Token format:
> H00:O-1:V3
> The token means:
> H00: the row-local hit alias.
> O-1: timing-offset tier.
> V3: velocity tier.
> Valid timing tiers are:
> O-3: very early.
> O-2: early.
> O-1: slightly early.
> O0: near the grid.
> O+1: slightly late.
> O+2: late.
> O+3: very late.
> Valid velocity tiers are:
> V0: ghost or very soft.
> V1: soft.
> V2: medium.
> V3: strong.
> V4: accent or very strong.
> Rules:
> Use only hit aliases present in the row.
> Include every hit exactly once.
> Do not invent extra hits.
> Do not submit JSON, MIDI, natural language, comma-separated lists, or audio files.
> An empty prediction is structurally allowed but scores 0 for the row.
> Example:
> id,predicted_feel 0a12bc34de56f789,H00:O-1:V3 H01:O0:V1 H02:O+1:V4
> ## **Evaluation**
> Structurally invalid submission files are rejected. Structural errors include missing columns, extra columns, duplicate IDs, unknown IDs, missing IDs, wrong row count, or wrong column order. Rows are aligned by `id`, not by row order.
> Malformed row-level ledgers score 0 for that row. A row-level ledger is malformed if it has invalid tokens, duplicated hit aliases, missing hit aliases, unknown hit aliases, or unsupported timing/velocity labels.
> For each valid row, the grader compares the predicted ledger to the hidden target ledger over the same hit aliases.
> For each hit:
> OffsetHitScore = 1.00 if predicted offset tier equals true offset tier 0.20 if predicted offset tier is adjacent to the true tier 0.00 otherwise
> The offset tier order is:
> O-3, O-2, O-1, O0, O+1, O+2, O+3
> For each hit:
> VelocityHitScore = 1.00 if predicted velocity tier equals true velocity tier 0.15 if predicted velocity tier is adjacent to the true tier 0.00 otherwise
> The velocity tier order is:
> V0, V1, V2, V3, V4
> For each row:
> OffsetScore = mean(OffsetHitScore over all hits) VelocityScore = mean(VelocityHitScore over all hits) JointExact = fraction of hits with both exact offset tier and exact velocity tier
> `AccentBoundaryF1` is F1 over the set of hit aliases whose velocity tier is extreme (`V0` or `V4`).
> AccentBoundaryF1 = 1 if both predicted and true extreme-hit sets are empty 0 if exactly one of the two sets is empty 2 * precision * recall / (precision + recall) otherwise
> `GrooveTransitionScore` measures whether the predicted feel is coherent across adjacent visible hits. Sort hit aliases numerically from `H00` to the last hit in the row. For every adjacent pair `(left_hit, right_hit)`, compare this exact four-field transition:
> (left_offset_tier, left_velocity_tier, right_offset_tier, right_velocity_tier)
> Then:
> GrooveTransitionScore = number of adjacent hit-pair transitions exactly matched / number of adjacent hit-pair transitions
> The row score is:
> row_score = 0.30 * OffsetScore
> 0.22 * VelocityScore
> 0.16 * JointExact
> 0.08 * AccentBoundaryF1
> 0.24 * GrooveTransitionScore
> Hidden rows are balanced across five private generation families, 200 rows per family:
> - `backbeat_style`
> - `cross_style_pulse`
> - `dense_drive`
> - `hat_syncopation`
> - `tom_fill_motion`
> The family label is not present in public files. It is used only to prevent solutions from ignoring difficult rhythmic conditions.
> overall_mean = mean(row_score over all hidden rows) worst_family_mean = minimum family mean over the five private families bottom_20_mean = mean(row_score over the lowest-scoring 20% of hidden rows)
> final_score = 0.60 * overall_mean
> 0.25 * worst_family_mean
> 0.15 * bottom_20_mean
> Scores are finite and bounded in `[0, 1]`. The sample submission scores 0. A perfect oracle scores 1.
> ## **Recommended solution approach**
> Reasonable approaches include training a sequence model, temporal convolution, transformer encoder, or hit-level classifier/regressor from scratch on the public rows. Strong solutions should model drum role, slot phase, tempo, style, local density, polyphony, neighboring-hit context, and the shifted noisy timing/energy probes jointly. Because the metric includes adjacent-hit transition consistency, independent hit-level classifiers usually need sequence-aware decoding, smoothing, or a learned structured model to be competitive. GPU use is appropriate for training compact neural sequence models within the 50-minute A10G limit.
> ## **What not to use**
> Do not use source filenames, drummer IDs, session IDs, raw MIDI file order, or source split labels. They are absent from solver-facing files.
> Do not assume every hit is on the grid or medium velocity. Constant middle-tier predictions are valid but intentionally weak.
> Do not treat `timing_probe` or `energy_probe` as direct labels. They are noisy, shifted side-channel codes whose mapping changes with public row context.
> Do not key predictions to row IDs, row order, fixed drum-alias identities, or fixed hit aliases. Drum aliases and hit aliases are row-local.
> Do not submit the visible quantized pattern as the answer. The target is the hidden human feel residual ledger.
> ## **Benchmark boundary**
> The source corpus has been used for groove modeling and performance humanization research. This benchmark changes the evaluation contract: solvers submit a fixed, auditable residual ledger for each row-local hit, with source-performance-disjoint splits, row-local aliases, hidden source-new residual mosaics, exact grammar validation, and robust family/tail scoring.
> It is therefore not ordinary drum transcription, not genre tagging, not audio classification, and not free-form MIDI generation. It is a constrained expressive-performance reconstruction benchmark for from-scratch or fine-tuned sequence models.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Support-Conditioned Tumor Contour Segmentation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f0cgrcdr8rjkyxsq3563w798bmb1n
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: image, medical, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Neurocartographer: Support-Conditioned Tumor Contour Segmentation
> Overview
> A damaged neuro-oncology archive contains many contrast-enhanced MRI slices, but most of their tumor contours have disappeared. One verified slice and its manual tumor mask remain for each patient. Your task is to build a neural segmentation model from random initialization, use each surviving image-mask pair as patient-specific support, and reconstruct the missing masks on the other slices.
> This is support-conditioned medical image segmentation, not tumor-type classification and not mask copying. Every scored patient is absent from training. The model must learn from the provided training patients how the query image, support image, and support contour interact, then transfer that relationship to unseen patients. Predictions should recover fine tumor boundaries and preserve the ordering of lesion burden across each patient's query slices.
> From-scratch learning contract
> Every learnable parameter used to produce the submission must begin from a fresh random initialization and be trained during the submitted run. Training may use only the supplied labeled training partition. Pretrained encoders, foundation models, externally trained weights, cached feature extractors, downloaded checkpoints, and parameters copied from another run are prohibited.
> Evaluation
> Each prediction is a binary 256 by 256 mask encoded as row-major run-length encoding. Runs are 1-indexed start length integer pairs separated by spaces.
> The grader computes three quantities for every hidden patient case:
> Difficulty-weighted Dice overlap, worth 65 percent of case utility.
> Difficulty-weighted boundary F1, worth 25 percent. Boundaries match when they fall within a Chebyshev radius of two pixels.
> Pairwise lesion-burden concordance, worth 10 percent. Every pair of query slices earns one when predicted mask areas have the same strict ordering as true mask areas. A true tie earns one only when the prediction is also tied.
> For query i, the hidden difficulty weight uses the native-resolution annotated query and support mask areas before resizing:
> w_i = 1 + min(1, abs(log((query_area_i + 1) / (support_area_i + 1))) / 1.5)
> Within a patient, Dice and boundary F1 are weighted means using w_i. Let D_c, B_c, and R_c be the three case quantities. Case utility and final score are:
> U_c = 0.65  *D_c + 0.25*  B_c + 0.10 * R_c
> U   = mean(U_c over patient cases)
> score = 0.11 + 0.34 * (U / 0.25)                       when U <= 0.25
> score = 0.45 + 0.15 * ((U - 0.25) / 0.40)             when 0.25 < U <= 0.65
> score = 0.60 + 0.40 * ((U - 0.65) / 0.35)             when U > 0.65
> The calibrated transform is continuous and strictly increasing. At the first knot, U = 0.25, the first branch gives 0.11 + 0.34 (0.25 / 0.25) = 0.45, and the second branch approaches the same value from above. At the second knot, U = 0.65, the middle branch gives 0.45 + 0.15 ((0.65 - 0.25) / 0.40) = 0.60, and the third branch approaches the same value from above. A perfect submission scores 1.0. The all-empty label-free sample scores approximately 0.110080, safely above the platform sample floor. The small excess over 0.11 comes from rare true area ties that an all-tied prediction matches. The patient-level mean prevents patients with many slices from dominating. The two calibration knots keep useful honest solvers in a discriminating middle band while preserving substantial headroom to the oracle.
> The following compact function is the exact aggregation after ID validation, RLE decoding, and the per-case quantities above have been computed:
> import numpy as np
> def evaluate(case_dice, case_boundary_f1, case_burden_concordance):
> case_utility = (
> 0.65 * np.asarray(case_dice, dtype=float)
> + 0.25 * np.asarray(case_boundary_f1, dtype=float)
> + 0.10 * np.asarray(case_burden_concordance, dtype=float)
> )
> utility = float(np.clip(np.mean(case_utility), 0.0, 1.0))
> if utility <= 0.25:
> return float(0.11 + 0.34 * (utility / 0.25))
> if utility <= 0.65:
> return float(0.45 + 0.15 * ((utility - 0.25) / 0.40))
> return float(0.60 + 0.40 * ((utility - 0.65) / 0.35))
> Dataset
> The public dataset contains 2,116 labeled training queries from 162 patients and 705 unlabeled test queries from 54 different patients. Train and test patient groups have zero overlap. Every query image is distinct. Images and masks are 256 by 256 grayscale PNG files.
> train.csv contains id, case_token, query_image, support_image, support_mask, and target_mask_rle.
> test.csv contains id, case_token, query_image, support_image, and support_mask.
> sample_submission.csv contains id and mask_rle with label-free empty-mask predictions.
> images/ contains query and support MRI slices. Paths are randomized and contain no source identity, class, split, or target information.
> support_masks/ contains one trusted binary support contour per patient case.
> Column meanings:
> id (integer) — independently randomized row identifier used only for grading joins.
> case_token (string) — independently randomized patient-group token. It reveals which query rows share a support case, but no patient identity or target.
> query_image (string) — relative path to the MRI slice whose mask must be predicted.
> support_image (string) — relative path to a different MRI slice from the same patient.
> support_mask (string) — relative path to the trusted binary mask aligned to support_image.
> target_mask_rle (string, training only) — true query mask in row-major RLE.
> The median prepared tumor occupies 856.5 pixels, or about 1.31 percent of a training image. Modeling foreground imbalance and fine boundaries is therefore essential.
> Submission
> Submit one CSV with exactly these columns and exactly 705 rows:
> id — each test ID exactly once. Row order does not matter.
> mask_rle — row-major 1-indexed RLE for a binary 256 by 256 mask.
> A mask with foreground pixels 10 through 14 and 300 through 301 would be encoded as 10 5 300 2. An empty string encodes an empty mask.
> Example using real test IDs:
> id,mask_rle
> 406291685957637,""
> 541106358386397,"12001 8 12257 10"
> 911465444310659,"30120 4"
> Requirements
> Use exactly the 705 test IDs with no missing, duplicate, or foreign IDs.
> Include exactly id and mask_rle; renamed, missing, or extra columns are rejected.
> RLE starts must be in 1 through 65,536. Lengths must be positive. Runs must be non-overlapping and remain within the image.
> Blank, NaN, non-finite, malformed, overlapping, odd-length, oversized, or out-of-range RLE cells are treated as empty masks, the worst content prediction. Structural submission errors raise a clean ValueError.
> Follow the from-scratch learning contract: initialize, train, and infer the neural image model on GPU during the submitted run. There is no CPU-training fallback.
> Complete the full run within 90 minutes.
> Train preprocessing, threshold selection, and model selection using training patients only. Do not fit any statistic or threshold on test images.
> What not to use
> Do not use pretrained weights, foundation models, external datasets, external annotations, imported embeddings, cached features, or checkpoints from another run.
> Do not use network downloads at runtime or install packages from the notebook.
> Do not access hidden labels, source patient identifiers, or source tumor categories.
> Do not reverse-engineer randomized IDs, tokens, filenames, file order, or preparation logic.
> Do not use the benchmark for clinical diagnosis or treatment decisions.
> Extra Modelling Information
> Neurocartographer instead holds out entire patients, gives one same-patient contour anchor, scores many query slices as a patient set, weights the harder contour changes, and adds patient-wise lesion-burden ordering to boundary-aware segmentation.
> The source MRI collection is commonly used for tumor classification or retrieval; this contour-relay mechanism is neither task.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## From-Scratch Acoustic Evidence Chain Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7eetrez8tyxep87rt3mkrfxs8bkscv
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Train a model from the supplied labeled JPEG evidence boards to reconstruct how shuffled acoustic fragments should be assembled. For every board, predict exactly three structured outputs: source grouping and time order, local flip direction for each fragment, and a six-row numeric witness matrix that verifies the reconstructed joins.
> The public challenge data is not the raw acoustic plot archive. Participants receive anonymous rendered boards with randomized fragment labels, transformed spectrogram shards, and opaque IDs. The task is to learn the reconstruction rule from the labeled training boards and apply it to hidden boards.
> source_partition: divide the eight labeled shards into one four-shard target chain and two two-shard donor chains, with every chain in chronological order.
> orientation_word: state which of the eight displayed shards must be flipped horizontally before assembly.
> spectral_witness_matrix: report the frequency-band changes across the five reconstructed joins and between the target chain and its reference spectrum.
> The first prediction answers source membership and time order. The second restores local time direction. The third is a numeric certificate of the completed reconstruction. These three fields describe one chain-recovery result rather than unrelated subtasks.
> Acoustic evidence is often exported into separate figures for reports, monitoring archives, and incident reviews. When filenames or timestamps are lost, visually plausible fragments can be attached to the wrong recording or displayed backward in time. A useful reconstruction must therefore solve three connected questions: which recording produced each fragment, where the fragment belongs on that recording's timeline, and whether its local time direction was reversed during export.
> The evidence images are built from paired acoustic measurements of real environmental recordings. A spectrum summarizes energy across frequency bands. A spectrogram shows how that energy evolves over time. The prepared boards use recordings from many environmental sound families, including mechanical, traffic, weather, animal, human, and music sources. Each prepared case uses three distinct source recordings. Every recording is used in at most one case, and complete sound families are held out from training.
> This is a from-scratch structured reconstruction task. It does not ask for the sound category, binary tamper detection, or independent labels for eight panels. The model must learn how shard continuity and the reference spectrum identify the three directed chains.
> Training Regime
> Domain: From Scratch. All fitted parameters, thresholds, and decoders must be learned or calibrated from the supplied training split. Models must start from random initialization or use non-pretrained algorithms fitted only on the public training boards and labels.
> External pretrained image or audio encoders, foundation-model inference, downloaded embeddings, external labeled examples, and hosted model APIs are not allowed. Compact neural networks trained from scratch, classical image features, dynamic programming, constrained decoding, and ensembles of eligible methods are allowed. Solutions must run in the available CPU environment within 1.5 hours.
> Dataset
> The prepared challenge contains 1,000 training examples and 400 test examples. Each example has one 1240 x 760 RGB JPEG evidence board. The CSV files and JPEG boards are generated from the raw acoustic plot collection by the supplied preparation script; solvers do not receive raw category names, raw filenames, source timestamps, or source recording identifiers in the public challenge files.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Input columns and all three target columns for 1,000 labeled cases |
> | `test.csv` | Input columns only for 400 hidden cases |
> | `sample_submission.csv` | A schema-valid constant baseline with one row per test case |
> | `images/` | The 1,400 evidence-board JPEG files referenced by the CSV rows |
> CSV Columns
> | Column | Data type | Train | Test | Meaning |
> |---|---|---:|---:|---|
> | `case_id` | string | yes | yes | Opaque identifier matching `^ac[0-9a-f]{22}$` |
> | `evidence_image_path` | string | yes | yes | Relative path such as `images/49b76df0ccff4b3ef70abe45.jpg` |
> | `source_partition` | canonical string | yes | no | Target chain followed by two anonymous donor chains |
> | `orientation_word` | fixed-length string | yes | no | Eight reversal bits in label order `A` through `H` |
> | `spectral_witness_matrix` | JSON integer matrix | yes | no | Six rows by eight frequency bands, with entries from `-2` to `2` |
> Evidence Board Layout
> The upper panel is the reference spectrum. It is divided into eight equal coarse frequency bands labeled b1 through b8, from low to high frequency.
> The lower panel contains eight tall spectrogram shards labeled A through H. Four shards are consecutive quarters of the spectrogram paired with the reference spectrum. Two shards are consecutive quarters from a second recording, and two are consecutive quarters from a third recording. Their displayed order is randomized. Between two and six shards are independently mirrored along the time axis. Mild contrast, brightness, and sensor-noise variation is applied independently to prevent simple pixel-edge equality from solving the assembly.
> The two donor recordings are selected for similarity to the target in both aggregate spectrum shape and coarse time-frequency texture. This makes color or texture clustering alone insufficient for identifying the target chain.
> Source Partition
> source_partition has exactly three branches:
> T:<four labels in time order>|D:<two labels in time order>|D:<two labels in time order>
> T is the chain belonging to the reference spectrum. Each D branch is one donor recording. Every label from A through H must occur exactly once. The two complete donor branch strings must be in ascending lexicographic order because donor identities are otherwise interchangeable.
> Valid example:
> T:F>G>C>E|D:B>H|D:D>A
> This example says that F, G, C, and E form the target timeline. The donor timelines are B then H, and D then A.
> Orientation Word
> orientation_word is b followed by eight bits in fixed label order A,B,C,D,E,F,G,H.
> 0 means the displayed shard already runs forward in source time.
> 1 means the displayed shard is horizontally mirrored and must be reversed before joining it to its chain.
> For example, b10110110 means that A, C, D, F, and G require reversal.
> Spectral Witness Matrix
> spectral_witness_matrix is a 6 x 8 JSON matrix. Columns correspond to b1 through b8.
> In plain language, rows 0 through 4 describe what happens at the five joins after the shards are oriented and ordered. Row 5 compares the completed target chain with the reference spectrum. A negative value means the measured band decreases, 0 means it remains close, and a positive value means it increases. Magnitude 2 represents a larger change than magnitude 1.
> | Row | Meaning |
> |---:|---|
> | 0 | Boundary transition at the first target-chain join |
> | 1 | Boundary transition at the second target-chain join |
> | 2 | Boundary transition at the third target-chain join |
> | 3 | Boundary transition in the lexicographically first donor branch |
> | 4 | Boundary transition in the lexicographically second donor branch |
> | 5 | Difference between the assembled target profile and the reference spectrum shape |
> For rows 0 through 4, each shard is first corrected according to orientation_word. For each frequency band, L is the mean grayscale value in the final seven columns of the left shard and R is the mean in the first seven columns of the right shard. Let:
> d = (R - L) / max(18, standard_deviation(concatenate(L, R)))
> The stored code is:
> | Condition | Code |
> |---|---:|
> | `d <= -0.75` | `-2` |
> | `-0.75 < d <= -0.22` | `-1` |
> | `-0.22 < d < 0.22` | `0` |
> | `0.22 <= d < 0.75` | `1` |
> | `d >= 0.75` | `2` |
> For row 5, the corrected target shards are concatenated in predicted time order. Their eight-band mean grayscale profile and the eight-band reference spectrum profile are independently min-max normalized. The shard profile minus the reference profile is encoded with thresholds -0.28, -0.08, 0.08, and 0.28, producing the same five integer codes.
> Target Diversity
> | Property | Train | Test |
> |---|---:|---:|
> | Cases | 1,000 | 400 |
> | Distinct raw recordings used | 3,000 | 1,200 |
> | Distinct `source_partition` strings | 974 | 395 |
> | Distinct `orientation_word` values | 231 | 194 |
> | Distinct witness matrices | 1,000 | 400 |
> All five matrix values occur thousands of times in both splits. The test categories are absent from training, and no raw recording or rendered image crosses the split boundary.
> Submission Format
> Write the final submission to exactly:
> ./working/submission.csv
> The file must contain exactly these columns in exactly this order:
> case_id,source_partition,orientation_word,spectral_witness_matrix
> | Column | Required serialization | Limit |
> |---|---|---:|
> | `case_id` | opaque string copied from `test.csv` | 24 characters |
> | `source_partition` | canonical three-branch string | 48 characters |
> | `orientation_word` | `b` plus eight binary digits | 9 characters |
> | `spectral_witness_matrix` | JSON `6 x 8` integer matrix | 180 characters |
> Nontrivial example:
> case_id,source_partition,orientation_word,spectral_witness_matrix
> ac003dce63e81f661377c0b5,T:F>G>C>E|D:B>H|D:D>A,b10110110,"[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[-1,-1,-1,0,-1,-1,-1,-1],[-2,-2,1,2,2,0,0,-2],[-2,-1,-2,-1,2,-1,-2,-2],[1,2,-1,-2,-2,-1,2,1]]"
> Every hidden case_id must occur exactly once. Extra columns, reordered columns, duplicate column names, missing or extra rows, duplicate IDs, unknown IDs, and malformed IDs are rejected before scoring. The platform may append one backend-managed visibility column; the grader removes that column before enforcing the schema.
> Malformed target values receive zero for their affected component. Length bounds are checked before JSON parsing or sequence work, so oversized fields cannot exhaust grader memory.
> Evaluation
> Submissions are scored with the Acoustic Provenance Reconstruction Score:
> Score =
> 0.52 * SourcePartitionScore
> + 0.18 * OrientationScore
> + 0.30 * SpectralWitnessScore
> Each component is first averaged across all hidden examples. Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> | Component | Weight | What it rewards |
> |---|---:|---|
> | `SourcePartitionScore` | 0.52 | Correct source grouping and chronological order |
> | `OrientationScore` | 0.18 | Correct flip decision for all eight shards |
> | `SpectralWitnessScore` | 0.30 | Correct band-change certificate for the reconstructed chains |
> SourcePartitionScore
> For one sample, let T_Y and T_P be the sets of target-chain labels in the truth and prediction. Let E_Y and E_P be directed adjacent-edge sets. Edge tokens include the branch kind, so target edge T:F>G differs from donor edge D:F>G.
> set_F1(A, B) = 2 * |A intersection B| / (|A| + |B|)
> target_membership_F1 = set_F1(T_Y, T_P)
> directed_edge_F1 = set_F1(E_Y, E_P)
> exact_partition = 1 if all three ordered branches match exactly, else 0
> row_partition_score =
> 0.15 * target_membership_F1
> + 0.20 * directed_edge_F1
> + 0.65 * exact_partition
> If only one compared set is empty, its F1 is 0. If both are empty, its F1 is 1. SourcePartitionScore is the mean row partition score.
> OrientationScore
> For valid eight-bit words:
> bit_accuracy = matching bit positions / 8
> exact_word = 1 if all eight bits match, else 0
> row_orientation_score = 0.25 * bit_accuracy + 0.75 * exact_word
> OrientationScore is the mean row orientation score.
> SpectralWitnessScore
> Let Y[i,j] be the hidden matrix and P[i,j] the submitted matrix. Entry weights are derived from the hidden truth:
> w[i,j] = 2 if Y[i,j] is nonzero, else 1
> w[5,j] = 1.5 * w[5,j]
> weighted_agreement =
> sum(w[i,j] * I(Y[i,j] = P[i,j])) / sum(w[i,j])
> exact_matrix = 1 if all 48 entries match, else 0
> row_witness_score = 0.25 * weighted_agreement + 0.75 * exact_matrix
> I(condition) is 1 when the condition is true and 0 otherwise. The final row receives extra weight because it links the selected target chain to the independent reference spectrum. SpectralWitnessScore is the mean row witness score.
> Malformed partitions, words, or matrices score 0 for that component. Hidden answers are validated separately and are never clipped or repaired.
> What Makes This Interesting
> The benchmark asks for a latent provenance forest, not a class label, raw-source lookup, or a list of suspicious regions. The target recording is anonymous among three spectrally similar sources. Time direction is also local rather than global, because any subset of shards may be mirrored. A successful method must jointly solve reference-conditioned source attribution, temporal ordering, local orientation recovery, and quantitative boundary verification.
> This changes the research question from detecting inconsistent figures to reconstructing lost custody structure. The source partition cannot be recovered from one panel independently, and the orientation bits cannot be inferred from labels or layout. Whole acoustic categories are held out, so the intended capability is cross-category structural generalization.
> What Not To Use
> Do not derive targets from case_id, image filename, row order, file size, compression size, or archive order.
> Do not match prepared images against external copies of the source figures or build source-record lookup tables.
> Do not use pretrained encoders, foundation models, external embeddings, external labeled data, or hosted inference APIs. This is a From Scratch challenge.
> Do not exploit duplicate payloads, split artifacts, hidden-answer feedback, or submission-system behavior.
> Do not tune on test labels, adapt parameters using private feedback, or construct per-test memorized mappings.
> Do not use malformed, duplicated, oversized, reordered, or extra-column submissions to probe the grader.
> Reference Validation
> | Check | Result |
> |---|---:|
> | Exact hidden answers | 1.000000 |
> | Constant sample submission | 0.080958 |
> | Train-mode structured baseline | 0.087174 |
> | Public image-statistics 1-nearest-neighbor baseline | 0.090622 |
> | Train/test raw recording overlap | 0 |
> | Train/test rendered-image hash overlap | 0 |
> | Duplicate rendered images | 0 |
> Preparation is deterministic from the source archive. All public identifiers and media filenames are opaque hashes, and the grader rejects schema and identifier exploits before metric computation.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Bengali Fragment Continuity and Entity Graph Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74yvfd6s47rkgwa8p577taw98bn648
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Long Bengali narratives are useful for search, summarization, and document intelligence only when a system can follow an entity across separated passages. A person or object may first appear by name, reappear through a description or pronoun, and continue after the surrounding text has been split or reordered. Recovering this structure is especially valuable in Bengali, where labeled resources are limited.
> Each case contains three shuffled fragments from one real Bengali narrative and a shuffled set of candidate mention spans. The lexical surface has been replaced by case-local anonymous token codes, but repeated local patterns, pronoun categories, syntax markers, and context remain available. Recover all three coupled structures:
> the chronological continuity chain among the three fragments;
> the candidate nodes that are genuine entity mentions; and
> directed links from each later mention to an earlier mention of the same entity.
> The output is a variable-size structured graph. JSON is only its serialization format; valid syntax alone earns no credit.
> This is a from-scratch structured NLP and graph-learning challenge. The input is a variable-length collection of token sequences and candidate spans, not a fixed feature table. The output is a constrained graph over visible fragment and mention ids, not generated text or a token sequence. Models must learn the token, span, fragment, and relation representations from the released training split; the case-local token vocabulary is not compatible with ordinary pretrained-language-model lookup.
> Task
> For every test case_id, submit graph_json with exactly this schema:
> {
> "active_nodes": [node_id, ...],
> "edges": [[child_node_id, parent_node_id], ...],
> "continuity_edges": [[later_fragment_id, earlier_fragment_id], ...]
> }
> active_nodes must include every genuine mention candidate and exclude distractors. An entity edge [child, parent] means that the later child mention continues the entity represented by the earlier parent. Every entity-edge endpoint must be active, each child may have at most one parent, and the entity graph must be acyclic.
> continuity_edges must form one complete chain over all displayed fragments. [later_fragment, earlier_fragment] means the later fragment immediately follows the earlier fragment. With three fragments, exactly two continuity edges are required. Entity edges must agree with the submitted fragment order; within one fragment, the parent span must precede the child.
> Every id must be a JSON integer in the visible case-local range; booleans, floats, negative values, and unknown ids are invalid. The serialized graph_json value may contain at most 40,000 characters. The parser also enforces conservative maxima of 96 active nodes, 192 entity edges, and 16 continuity edges, all above the structure required by any released case.
> LEX_xxxxx values are anonymous case-local lexical codes. Repetition is meaningful only within a case. P* values are coarse pronoun codes; FUNC, REL, EOS, and SEP are non-lexical markers. Node ids, fragment ids, and list order are shuffled. Use fragment_id, start, and end to locate a candidate, but infer chronology from context.
> Dataset
> The modeling examples are the variable-length JSON case files described below. The small CSV files are manifests that map opaque case ids to JSON paths; they are not tabular feature matrices and contain no predictive attributes.
> Item                         Description
> train.csv                    Training index
> validation.csv               Tuning index
> test.csv                     Test index
> train/cases/*.json           Training inputs
> validation/cases/*.json      Tuning inputs
> test/cases/*.json            Test inputs
> train/targets/*.json         Training graphs
> validation/targets/*.json    Tuning graphs
> sample_submission.csv        Valid weak test submission
> train.csv and validation.csv contain:
> Column       Type      Description
> case_id      string    Opaque case id
> input_path   string    Relative case JSON path
> target_path  string    Relative target JSON path
> test.csv contains:
> Column       Type      Description
> case_id      string    Opaque case id
> input_path   string    Relative case JSON path
> Each case JSON contains:
> Field                    Type          Description
> fragments                list[object]  Three shuffled context fragments
> fragments[].fragment_id  integer       Shuffled case-local fragment id
> fragments[].tokens       list[string]  Anonymous tokens in that fragment
> nodes                    list[object]  Shuffled candidate mention spans
> nodes[].node_id          integer       Shuffled case-local node id
> nodes[].fragment_id      integer       Fragment containing this candidate span
> nodes[].start            integer       Inclusive offset within the node's fragment
> nodes[].end              integer       Exclusive offset within the node's fragment
> Each public training or validation target contains:
> Field               Type              Description
> active_nodes        list[integer]     Genuine mention node ids
> edges               list[[int,int]]   Directed child-parent entity links
> continuity_edges    list[[int,int]]   Directed later-earlier fragment links
> Whole source documents are assigned to train, validation, or test before cases are constructed. No source document occurs in more than one split, and hidden test references never occur in participant-facing files.
> Evaluation
> Let M_pred and M_gold be the predicted and reference active-node sets. Let E_pred and E_gold be the directed entity-edge sets, and let T_pred and T_gold be the directed fragment-continuity edge sets. For each entity graph, convert every connected component into all unordered pairs of nodes in that component; call those pair sets C_pred and C_gold.
> For any predicted set A and reference set B:
> F1(A,B) = 2 * |A intersect B| / (|A| + |B|)
> If both sets are empty, this term is defined as 0, not 1. This is intentional: an empty relation or component prediction is an abstention rather than affirmative recovery, so it must not earn agreement credit merely because a case contains no corresponding positive pair.
> mention_F1      = F1(M_pred, M_gold)
> edge_F1         = F1(E_pred, E_gold)
> cluster_pair_F1 = F1(C_pred, C_gold)
> continuity_F1   = F1(T_pred, T_gold)
> case_score = 0.30*continuity_F1 + 0.25*mention_F1 + 0.30*mention_F1*edge_F1 + 0.15*mention_F1*cluster_pair_F1
> final_score  = mean(case_score over all test cases)
> The four maximum contributions sum to 0.30 + 0.25 + 0.30 + 0.15 = 1.00, so the score is bounded in [0,1]. Exact recovery scores 1.0. The 0.65-0.70 agent threshold is a challenge-readiness criterion, not a score cap and not part of the grader. The mention factor prevents a relation graph over the wrong node roster from receiving full entity credit. Wrong entity links reduce both exact-edge and component-pair agreement, while wrong fragment order reduces continuity credit and may make entity links structurally invalid.
> Submission
> Write ./working/submission.csv with exactly these columns in this order:
> Column       Type       Constraint
> case_id      string     Every test id exactly once
> graph_json   JSON text  Exact three-key graph object
> Valid example rows from sample_submission.csv:
> case_id,graph_json
> berg_031fb02c026aee32,"{""active_nodes"":[0,1],""edges"":[],""continuity_edges"":[[1,0],[2,1]]}"
> berg_063de5c759e2692b,"{""active_nodes"":[0],""edges"":[],""continuity_edges"":[[1,0],[2,1]]}"
> The sample is a weak train-derived mention-count prior with a fixed fragment chain and no entity links. Wrong columns or column order, missing or extra ids, and duplicate ids raise InvalidSubmissionError. A malformed row-local graph, including invalid JSON, unknown ids, duplicates, invalid ranges, an incomplete continuity chain, inconsistent chronology, or a cycle, receives zero for that row only. Grader errors do not expose private labels or component scores.
> Intended Approach And Allowed Methods
> Train the model from scratch on the released training cases. A competitive A10G solution can learn token embeddings and contextual fragment encoders, score the six possible directed fragment pairs, select the best valid continuity chain, classify genuine mention candidates from contextual span representations, rank compatible antecedents under that chain, and decode an acyclic entity forest. Joint or multitask training, learned token and span encoders, graph attention, pair ranking, contrastive objectives, and sparse pair batching are appropriate within the approximate 1.5-hour budget. The model predicts node and edge sets over ids already present in each case; it never generates Bengali text or an output token sequence. Fit and tune only on public training and validation files.
> What Not To Do
> Do not retrieve, match, reconstruct, or transfer answers from external copies of source documents or annotations. Do not use source titles, authors, original ids, source order, private files, grader internals, or hidden labels. Do not replace modeling with source lookup, id hashing, row-order tricks, fixed answer templates, or hand-written label recovery. Do not submit invented ids, inactive edge endpoints, reversed within-fragment links, an incomplete fragment chain, or cyclic graphs.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Laundry Resource-State Reconstruction From Sound and Vibration

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx777c8mny9v0q9wtjv8bva9s18bnfxq
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: multimodal
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> A washing machine can be monitored cheaply with a microphone and an accelerometer, while direct electricity and water meters are more intrusive. Given synchronized appliance sound, three-axis vibration, and coarse safe room context, reconstruct how power and water change through the cycle and recover the ordered operating-state ledger.
> Each example is a contiguous portion of a real appliance cycle rendered onto one normalized timeline. The hidden test set holds out a complete appliance family, and every portion and modality from one physical cycle stays in one split. The challenge therefore tests cross-device generalization, multi-rate sensor fusion, temporal boundaries, resource accounting, and calibrated ambiguity. It is not appliance/program classification, object detection, computer vision, or single-scalar regression.
> Current platform announcement: “We’ll be reviewing GPU challenges only going forward, so please focus on creating GPU challenges. For the coming week, all challenges pushed for solving will also be GPU challenges only.” This challenge is designed and measured as a GPU challenge.
> Task
> For every test id, predict all of the following:
> Three fixed 96-bin profiles: electrical power, inlet water flow, and outlet water flow.
> Whether water channels are measured or not applicable.
> An ordered event ledger covering bins [0,96) with idle, active, fill, drain, fill_drain, heat, spin, or uncertain.
> Per-state energy and water accounting.
> Ambiguous intervals plus event-level and row-level confidence.
> The profiles and ledger are the central outputs. The totals and uncertainty must remain consistent with them.
> Intended Approach
> Train a compact multi-rate model from random initialization on GPU. A strong starting point uses separate strided one-dimensional encoders for the 1 kHz audio and 50 Hz three-axis vibration arrays, maps both into 96 normalized-time tokens, fuses those tokens with safe numeric context, and decodes continuous resource profiles, state logits, boundaries, and confidence. Useful training losses include robust profile regression, class-balanced state loss, boundary loss, confidence calibration, and differentiable accounting consistency. Validation should group all rows from a physical cycle and preserve appliance-family separation.
> The measured baseline has 174,700 trainable parameters and no pretrained weights. On an NVIDIA GeForce RTX 3050 6 GB Laptop GPU with a CUDA-enabled PyTorch build, 30 epochs took 144.78 seconds, inference for 33 test rows took 6.33 seconds, and peak allocated VRAM was 12.27 MiB. The participant reference environment is stable PyTorch 2.3.0 with CUDA 12.1. The baseline score was 0.382461, versus 0.341108 for the strongest single-modality model, an absolute fusion gain of 0.041353. The oracle is 1.0. A measured pairwise/head-mixing ensemble stress test reached only 0.472299, leaving 0.177701 below the 0.65 review threshold; this is evidence, not a promise about every future solver.
> What Not To Use
> Do not identify the original recordings, fingerprint them against external corpora, retrieve hidden meter traces, or copy answers from any external dataset.
> Do not infer answers from opaque IDs, file names, hashes, file sizes, row order, directory layout, or recovered metadata.
> Do not use pretrained audio, vibration, embedding, foundation, or generative-model weights. Train only from the provided training set.
> Do not reduce the task to appliance/program recognition, a lookup table, a nearest-template-only system, or one scalar consumption estimate.
> Do not use runtime downloads, hosted APIs, private files, the answer file, or grader internals.
> Do not hard-code test answers, manually label the fixed test set, or exploit malformed/non-finite/oversized submissions.
> Evaluation
> The score is bounded to [0,1], and a perfect valid submission scores exactly 1.0. Scores are averaged within hidden complete physical-cycle groups and then macro-averaged, preventing long cycles from dominating because they contain more portions.
> | Component | Weight | Rewarded behavior |
> |---|---:|---|
> | Power profile | 0.20 | 96-bin fidelity |
> | Water profiles | 0.16 | Flows and valid mode |
> | State path | 0.20 | Bin accuracy and macro-F1 |
> | Event matching | 0.18 | One-to-one timed matches |
> | State totals | 0.12 | Energy/water accounting |
> | Uncertainty | 0.06 | Ambiguous-bin F1 |
> | Calibration | 0.04 | Confidence accuracy |
> | Consistency | 0.04 | Agreement across outputs |
> Profile fidelity combines the full trace, resource-active bins, and temporal first differences so long zero intervals cannot dominate. Per-state totals similarly score only resource-active predicted/truth state cells. Event matching is same-state, one-to-one, and allows a four-bin boundary tolerance (4.17% of the normalized timeline). The metric remains additive: an error in one head does not erase unrelated correct outputs, and no arbitrary exponent, hard score cap, or hidden subgroup weight is used.
> Global structural faults—wrong or reordered columns, duplicate/missing/foreign IDs, an invalid row count, oversized CSV/cells, or non-finite/out-of-range top-level confidence—raise InvalidSubmissionError. A row-local JSON/schema/value fault gives that row zero while valid rows remain scoreable.
> Dataset
> All paths in the CSV files are relative to public/.
> Public Files
> | Item | Description |
> |---|---|
> | `train.csv` | Inputs and labels |
> | `test.csv` | Test inputs only |
> | `sample_submission.csv` | Valid output template |
> | `audio/*.wav` | Mono 1 kHz audio |
> | `vibration/*.npy` | 50 Hz XYZ vibration |
> There are 101 training rows from 21 physical cycles and 33 test rows from 10 cycles in one held-out appliance family. Public data are 185,695,616 bytes. The prepared inputs contain no timestamps, original paths, cycle identifiers, appliance/model names, program names, or load labels.
> Each WAV is mono PCM16 with 600,000 samples at 1 kHz. Each vibration file is a float16 NumPy array of shape (30000,3) at 50 Hz. Both represent the same normalized complete portion. Context fields are opaque row id and group group_id, a coarse duration bucket, sample rates/counts, integer ambient temperature, and humidity rounded to 5%.
> train.csv Columns
> train.csv contains public inputs followed by eight train-only target columns.
> | Column | Type | Description |
> |---|---|---|
> | `id` | string | Opaque row ID |
> | `group_id` | string | Opaque cycle group |
> | `audio_path` | string | Relative WAV path |
> | `vibration_path` | string | Relative NPY path |
> | `duration_s` | float seconds | Duration bucket |
> | `audio_sample_rate` | integer Hz | Audio sample rate |
> | `audio_samples` | integer | Audio sample count |
> | `vibration_sample_rate` | integer Hz | Vibration rate |
> | `vibration_samples` | integer | Vibration row count |
> | `ambient_temperature_c` | float Celsius | Rounded room temp |
> | `ambient_humidity_pct` | float percent | Rounded room humidity |
> | `power_profile_json` | JSON list | 96 power bins |
> | `water_in_profile_json` | JSON list | 96 inlet-flow bins |
> | `water_out_profile_json` | JSON list | 96 outlet-flow bins |
> | `water_mode` | string | Water availability |
> | `ledger_json` | JSON list | Ordered state events |
> | `totals_json` | JSON list | Per-state resources |
> | `uncertainty_json` | JSON list | Ambiguous intervals |
> | `confidence` | float `[0,1]` | Label confidence |
> test.csv Columns
> test.csv contains the same eleven public input columns and no target values.
> Column	Type	Description
> id	string	Opaque row ID
> group_id	string	Opaque cycle group
> audio_path	string	Relative WAV path
> vibration_path	string	Relative NPY path
> duration_s	float seconds	Duration bucket
> audio_sample_rate	integer Hz	Audio sample rate
> audio_samples	integer	Audio sample count
> vibration_sample_rate	integer Hz	Vibration rate
> vibration_samples	integer	Vibration row count
> ambient_temperature_c	float Celsius	Rounded room temp
> ambient_humidity_pct	float percent	Rounded room humidity
> ### Submission
> Write `./working/submission.csv` with exactly one row per test ID and exactly these columns in this order.
> Column	Type	Constraint
> id	string	Exact test ID set
> power_profile_json	JSON list	Exactly 96 values
> water_in_profile_json	JSON list	Exactly 96 values
> water_out_profile_json	JSON list	Exactly 96 values
> water_mode	string	Allowed enum
> ledger_json	JSON list	Covers bins 0 to 96
> totals_json	JSON list	All eight states
> uncertainty_json	JSON list	Up to 48 intervals
> confidence	float	Finite in [0,1]
> - Each profile cell is a JSON list of exactly 96 finite numbers. Power must be in `[0,4000]` watts; flows must be in `[0,500]` millilitres per second.
> - `water_mode` is `MEASURED` or `NOT_APPLICABLE`; the latter requires both submitted water profiles to be zero.
> - `ledger_json` is a JSON list of contiguous, ordered, non-overlapping events covering `[0,96)`. Each event has exactly `state`, `start_bin`, `end_bin`, and `confidence`; end bins are exclusive.
> - `totals_json` contains every allowed state exactly once. Each object has exactly `state`, `energy_wh`, `water_in_l`, and `water_out_l`.
> - `uncertainty_json` is an ordered, non-overlapping list of objects with exactly `start_bin` and `end_bin`.
> - Row and event confidence values must be finite and in `[0,1]`. Standard JSON is required; `NaN` and infinities are invalid.
> Use `sample_submission.csv` as the serialization template.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Smartphone Acoustic-To-Vibration Motor State Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7621pvh43s4ae3papgddk75n8bnvne
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> A maintenance engineer can often place a phone near an induction motor even when a dedicated vibration probe cannot be attached. In this challenge, infer what the phone's synchronized three-axis accelerometer would have measured from its microphone recording and a few real calibration recordings made with the same phone and rigid mounting family.
> This is an inverse cross-sensor reconstruction task. Continuous three-axis vibration and ordered vibration evidence are the central outputs; clip-level operating state is a supporting structured output.
> Dataset
> The public data contains 80 labeled training episodes, 40 unlabeled test episodes, and 40 calibration records shared only through episode-local support lists.
> File overview
> Item	Description
> train.csv	80 labeled episodes
> test.csv	40 test episodes
> sample_submission.csv	valid weak example
> train/audio/	query WAV files
> train/targets/	target vibration NPYs
> test/audio/	test query WAV files
> calibration/audio/	support WAV files
> calibration/vibration/	support vibration NPYs
> train.csv columns
> COLUMN                   TYPE       DESCRIPTION
> episode_id               string     opaque episode ID
> group_id                 string     opaque physical-condition group ID
> split_role               string     always train
> query_audio               path       query WAV path
> calibration_json         JSON       exactly three support records
> audio_rate_hz            integer    always 8000
> audio_samples            integer    always 80000
> vibration_rate_hz        integer    always 96
> vibration_samples        integer    always 960 per axis
> evidence_steps           integer    always 32
> prompt                    string     generic task text
> target_vibration         path       target NPY path with shape (3, 960)
> target_evidence_json     JSON       32 ordered target tokens
> fault_major              string     major motor-condition label
> fault_minor              string     minor motor-condition label
> speed_condition          string     speed label
> load_condition           string     load label
> Training rows contain both the multimodal inputs and every supervised target.
> test.csv columns
> COLUMN                   TYPE       DESCRIPTION
> episode_id               string     opaque episode ID
> group_id                 string     opaque physical-condition group ID
> query_audio               path       query WAV path
> calibration_json         JSON       exactly three support records
> audio_rate_hz            integer    always 8000
> audio_samples            integer    always 80000
> vibration_rate_hz        integer    always 96
> vibration_samples        integer    always 960 per axis
> evidence_steps           integer    always 32
> prompt                    string     generic task text
> Test rows contain the same input contract but omit all target paths, evidence targets, and operating-state labels.
> Inputs
> Each test episode supplies:
> INPUT                         SHAPE OR FORMAT                         MEANING
> query_audio                   mono PCM16 WAV; 8000 Hz; 80000 samples anonymized 10-second query microphone signal
> calibration_json              JSON list of exactly 3 supports        episode-local calibration index
> each support.audio            mono PCM16 WAV; 8000 Hz; 80000 samples real same-device calibration microphone signal
> each support.vibration        float32 NPY; shape (3, 960)             synchronized x/y/z acceleration in m/s^2 at 96 Hz
> episode_id/group_id/support_id opaque strings                          source-neutral identifiers
> The query row supplies the query_audio path and calibration_json. Every object inside calibration_json supplies one support audio path and one support vibration path; exactly three support objects are present.
> All examples use one declared rigid mounting family. Device names and device descriptors are withheld; the real calibration signals are the solver-visible device calibration. Calibration supports never expose their fault, speed, or load labels.
> Required output
> Submit one row per test episode with:
> FIELD                     REQUIREMENT
> vibration_i16_b64         base64 of little-endian int16 values; shape (3, 960); row-major x/y/z;
> divide decoded values by 1024 to obtain acceleration in m/s^2
> evidence_json             JSON list of exactly 32 legal ordered vibration-evidence tokens
> fault_major/fault_minor   one legal hierarchical motor-condition pair
> speed_condition           one of 15_hz, 20_hz, 25_hz, 30_hz
> load_condition            loaded or unloaded
> confidence                finite scalar in [0,1] estimating overall content quality
> uncertainty_json          {"axis_nrmse":[x,y,z],"state_error_probability":p};
> axis values in [0,2] and p in [0,1]
> The 32 evidence tokens correspond to consecutive 0.3125-second blocks. For each block, the token identifies the x/y/z axis and one of eight fixed dominant-power bands with edges [3, 8.625, 14.25, 19.875, 25.5, 31.125, 36.75, 42.375, 48.001] Hz. Training targets are derived deterministically from the measured acceleration by prepare.py; no language model labels are used.
> Legal hierarchical condition pairs are:
> healthy/healthy, rotor/unbalance, rotor/misalignment, stator/winding,
> voltage/unbalance, bowed/rotor, broken/rotor_bars, faulty/bearing
> These are whole-clip states. The source provides condition recordings, not within-clip event boundaries; do not invent onset or offset intervals.
> What Not To Do
> Using any of the following is grounds for rejection even if a CSV passes the grader:
> Do not look up public source recordings, recover original filenames, fingerprint against the source corpus, or copy hidden acceleration from any external source.
> Do not use source paths, device names, original file IDs, timestamps, row order, fault-code strings, or private answer metadata.
> Do not reduce the task to condition labels, scalar vibration magnitude, or a condition-template-only solution. The (3,960) reconstruction and 32-step evidence are required.
> Do not ignore the query audio or the calibration signal contents.
> Do not use hosted APIs, closed remote models, private files, or internet access at inference time.
> Do not use pretrained weights. Train the signal encoders and decoder from scratch on the supplied public data.
> Do not access private/answers.csv, grader internals, file-system metadata, or malformed payload behavior.
> Do not submit missing, extra, duplicate, or blank IDs; reordered columns; non-finite values; invalid tokens; impossible condition pairs; wrong sequence lengths; or oversized payloads.
> Intended approach
> Train a GPU model from scratch on the supplied multimodal training data. This is a multi-input sequence-to-sequence learning problem in the From Scratch domain. Pretrained weights and hosted models are not permitted.
> Evaluation
> Higher is better. The theoretical range is 0.0 to 1.0; a perfect valid submission scores exactly 1.0.
> ROW COMPONENT                                      WEIGHT
> three-axis waveform fidelity W                    0.52
> ordered evidence sequence E                       0.18
> hierarchical condition, speed, and load S          0.14
> cross-output consistency C                         0.08
> confidence calibration K                           0.04
> explicit uncertainty quality U                     0.04
> All means below are arithmetic means and every similarity is clipped to [0,1]. For each axis, let p be the submitted 960-sample sequence and t the measured target:
> scale       = std(t) + 0.25
> nrmse       = sqrt(mean((p - t)^2)) / scale
> error_sim   = exp(-nrmse)
> corr        = dot(p-mean(p), t-mean(t)) / (||p-mean(p)|| * ||t-mean(t)||)
> corr_score  = clip(corr, 0, 1)^2; corr is 0 when the denominator is at most 1e-12
> mean_score  = exp(-abs(mean(p) - mean(t)) / 1.5)
> temporal_a  = 0.55*error_sim + 0.35*corr_score + 0.10*mean_score
> For spectral similarity, center each axis, compute magnitude STFTs with a 192-sample Hann window and 96-sample hop, and set L_p=log1p(|STFT(p)|) and L_t=log1p(|STFT(t)|):
> relative_a  = mean(abs(L_p - L_t)) / (mean(abs(L_t)) + 0.25)
> spectral_a  = exp(-1.5 * relative_a)
> temporal    = mean_a(temporal_a)
> spectral    = mean_a(spectral_a)
> W           = 0.60*temporal + 0.40*spectral
> Evidence position accuracy is the fraction of the 32 submitted tokens equal to the target at the same position. macroF1 is the unweighted mean token F1 over token classes present in the target. Thus E = 0.70*position_accuracy + 0.30*macroF1.
> State score is S = 0.40*I(fault_major) + 0.25*I(fault_minor) + 0.20*I(speed) + 0.15*I(load), where each indicator is 1 only when that field exactly matches the target.
> Let A be the fraction of submitted evidence tokens equal to the tokens deterministically re-derived from the submitted vibration. Cross-output consistency is:
> C = 0.65*(W*E*A)^(1/3) + 0.35*sqrt(spectral*S)
> content = 0.52*W + 0.18*E + 0.14*S + 0.08*C
> For confidence, quality = clip(content/0.92,0,1) and K = clip(1-abs(confidence-quality),0,1). For uncertainty, the grader compares the three declared axis_nrmse values with the clipped realized per-axis NRMSE values and compares state_error_probability with 0 when all four state fields are correct or 1 otherwise:
> axis_calibration  = clip(1 - mean(abs(declared_axis_nrmse - realized_axis_nrmse))/2, 0, 1)
> state_calibration = clip(1 - abs(state_error_probability - state_error_target), 0, 1)
> U                 = 0.75*axis_calibration + 0.25*state_calibration
> episode_score     = content + 0.04*K + 0.04*U
> The final score is:
> 0.85 * mean episode score
> + 0.075 * worst hidden sensor-group mean
> + 0.075 * worst hidden speed-group mean
> Global structural errors raise InvalidSubmissionError. A malformed vibration, evidence, or uncertainty payload is contained to that row/head and scores zero for that head.
> Submission format
> Submit ./working/submission.csv with exactly these columns in exactly this order.
> COLUMN                 TYPE      MEANING AND VALIDATION
> episode_id             string    one occurrence of every episode_id from test.csv; no extras
> vibration_i16_b64      base64    little-endian int16 array with exact shape (3,960), x/y/z row-major
> evidence_json          JSON      ordered list of exactly 32 legal axis-band tokens
> fault_major            string    legal major motor-condition token
> fault_minor            string    legal minor token paired with fault_major
> speed_condition        string    one of 15_hz, 20_hz, 25_hz, 30_hz
> load_condition         string    loaded or unloaded
> confidence             float     finite overall-quality estimate in [0,1]
> uncertainty_json       JSON      exact keys axis_nrmse and state_error_probability with bounded values
> Use sample_submission.csv as the serialization reference. It is valid but deliberately weak.
> Example: first five rows of sample_submission.csv
> The five rows below are the actual first five sample-submission rows. The two long sequence payloads are shortened only in this visible table so the row structure is readable; the exact, unshortened CSV rows follow immediately afterward.
> episode_id	vibration_i16_b64	evidence_json	fault_major	fault_minor	speed_condition	load_condition	confidence	uncertainty_json
> ep_06580faf7cb2db7c53	<7680-char base64 payload>	<32 ordered evidence tokens>	rotor	unbalance	15_hz	loaded	0.2	{"axis_nrmse":[1.0,1.0,1.0],"state_error_probability":0.75}
> ep_0795720dcfc59730ad	<7680-char base64 payload>	<32 ordered evidence tokens>	rotor	unbalance	15_hz	loaded	0.2	{"axis_nrmse":[1.0,1.0,1.0],"state_error_probability":0.75}
> ep_0c4b1c98482497f079	<7680-char base64 payload>	<32 ordered evidence tokens>	rotor	unbalance	15_hz	loaded	0.2	{"axis_nrmse":[1.0,1.0,1.0],"state_error_probability":0.75}
> ep_161bf9e52ffb341026	<7680-char base64 payload>	<32 ordered evidence tokens>	rotor	unbalance	15_hz	loaded	0.2	{"axis_nrmse":[1.0,1.0,1.0],"state_error_probability":0.75}
> ep_1e629e5114f8fee70c	<7680-char base64 payload>	<32 ordered evidence tokens>	rotor	unbalance	15_hz	loaded	0.2	{"axis_nrmse":[1.0,1.0,1.0],"state_error_probability":0.75}
> Exact CSV header and five complete rows
> The complete file contains one row for every test episode and uses the same nine-column order.
> Columns, in order: episode_id, vibration_i16_b64, evidence_json, fault_major, fault_minor, speed_condition, load_condition, confidence, uncertainty_json.
> <!-- SAMPLE_SUBMISSION_PREVIEW_START -->
> episode_id,vibration_i16_b64,evidence_json,fault_major,fault_minor,speed_condition,load_condition,confidence,uncertainty_json
> ep_06580faf7cb2db7c53,/wGV/sAAcgAO/8wApAA4AKj+YADIATn/yP+9AFn/hwGp/v8AVf8kAfT/Jf8GAcn//f9zAC0Bmv4HAD4ApQF1/l8AdADq/6oAI/+xAKX/XQEA/y8AOwAZALj/LQGNACL+VAEYAAsBUf5TAbb/SgA/AEv/PgDPAFsAIP+zAHj/XwCJ/1oC2P1nAHUAhAD7/zn/UgH+/oMBKf+w/8QA7QDw/n0ASACz/8T/ZwFTABT+owGl/5IAw/9RAO7/TQDzAED+6gDQAL3/Wf9WAfL+8v+GAHsBWv5/AGcA0/+oANf/7f/z/3EBhP58/14BKwAw/wMBZADN/kkAqAFW/5z/rABp/8IAFQDz/6z/FwFkAO796wFMAH//MQAcATD/eP/VANAA1v4JAT//RQC/AMX/EgDM/6YBY/7h//wBvv5FAJYAZQA1/4D//wEf/0UAfADe/lYB4P/A/5kA1f8tAaP9VAK0/zT/sgBDAG8At/6yAC4BSf+mAGv/zf/nAKL/TAAhAEwA/v+9/sYCQf4WAKIAvQBt//n+wAG2/04A4//8/5D/bwHx/uIAz/9nAOL+DgEmARf+6QC9AF8Aiv7MAKQAx/9xAKf/GQDU/3ABQ/7tAQL/KwCE/xcCNf+z/qYBnwAj/2b/aQEh/7AB5v7cAPP+oQF1/63/twFR/l0AxwAVAQP+ZQC4AXP/b/9/ABUAEQA7AWP+JgEI/8sBQf7yAbj/av6hAZ4Atf+T/twBbwBv/87/yAAm/7YBMv+//3cAAwBYAH7/2wH8/T8A5gFq/2j/dP8qAvL+XwCS/4IA6P8FAdv+yAD5/wIAEgDAAGgAGv7dAYoAcP8v/xkB1wAa/1sAwP+2ABAANQC4/5kA3/+v/9EAOwCN/zX/CwJJ//T/Jv9UAvn+JQDD/18AZACX/5AAsv+aAHT/SQDiAOH/XP9/ACwBOv9c//8A4wDH/pEA3v/bAH//FwDPAGn//ADA/p8Bl//p/7n/OQHj/3T/4/+9ASr/2v9NAHUAPgAs//sAsP+AAKr/q/9oAfX+OQA+ALoAoP8y/6kB4f+F/0MAIACeAJP/t//3ALr/mwAI/3IBlv+c/5wAkwC3/53/WgAdAfL+jACo/wQBBABW/3YAUwA9AIb/cwCiAAn/VgAlAYD/FgDR/1ABQ/8IAPj/FgAYAUX/1//dACUALABP/7oBpP4eANIAiQDs/k4ASQCfAFz/ZwCl/9YAdQDH/rkAJABpAED/VAHH/x7/1gAJAT//nP95AMYAov87AL7/QQCnABYAD/8wAX7/oABk/4sBjP5lANcAXABF//7/7wDm/ycAm/92AAoAvAAx/2wAMAD5/ysAUgBJABP/BwGeALn/cP+KAMAAT/+QAHH/LwEz/zIB3v4OAXz/cQBJAEgAsP+m/zsB+v99/3//jQFh/3YArP+hAOj/DQC8AAn/HgFF/8IAAwDu//n/0/8mAWT/z/9cAO4ALf/qAC//bgHC/jEBqP/p/78AKv9VAVf/NQDh/8kAIgA8/0IA4QCF/3UAt/8lALYAC/9HARz/2QCX/woAJgGR/h0Bvv/fAFX/IQCJACYA0/95AGj/HAGR/+T/1wCN/64AEP+RAVT/t/9HAar/OQBy/94A1/9hAPn/DQAIAOMAHv96AMEAbv9AACoA7ACW/iwBfACe/73/YgBDAOH/awCZ/1MAXAAWAEv/RQEKACr/iQBxANn/Wv+qAXn/tP/h/zkB9f4AAYn/KgBwAN//MwB7/6UB3/4BAMAA4f91/9cAgQDF/yr/NgHn/9P/hABc/xEBnf8ZABwAdwDdAJT+MgHe/8T/4v81Acf/4P96/5cB6v6MAB8A4P/eAOf+CgFT/ycBjf/U/6kACQBU/yMB6v9VAP/+7QBwAOz+0gC8/54Aqv+w/9QAof/tADf/mAAhAL3/1v8nAdb/0P+c/1UBOP+1/ycBo/+YAOj+CAGG/zUBXP9CAA4AowD6/hYBLgAKAHT/BAHG/5X/SQDyAMf/7v+l/5EAOAByAET/nwAbAOj/0P/FACAAIv8ZAdb/JQA0/3sBxv9nAN/+uwDk/0EB5/6ZAO3/QgCC/8oA8//b/9n/MwHx/nQAqv9WAdj/6P9S/5kA0wDD/9z/GgChACL/QgFl/wQBx/6lARD/vgDp/j4BXABBAPH+KwDaAFgAmv81ANj/SADL/9YAff+GAI7/DwFN/y8ASP/AAeb/u/8c/40AHwE4/0cBZP6fAe3+IwFV/+4ABf9DAX//zQAt/pQBuAC8/8n/bP8NAQoASgAaAPv+nwEJ/7oALADe/7v/AAEHAKP/4v6XAjb/7P8NADX/0gH7/oYBTv5DAfX/4v8xAP0AMf6sAcz/sQAQ/mQBLAEH/2oAbf8mAOkA+P8cAGP/9wDE/7z/RAFH/1H/4QGD/+j/jf6TApf/m/+WAAv/5wAdAJoAQP+3AM7/QgCo/4YB4P1nAXEA6v8M/1wAbwFU/ysA9/+y/2cAzABl/wsAcwDO/x0ADgACASX+CwItAGf/Rv9DAaYAOv9pAEUAev+mALwADf8KAaL/HgC4/xQBsv///ioCaf/5/ocA/P0v/5L+bf5L/ln/0v4b/pL9xQCM/l39q/9r/i3/2v2p/3X+5P0zAPf8KgBr/ScAIf3OAEr9Uv75/q3/of6p/M0AEf0RAH39xP+G/UH/w/4M/kb/2P2+/0T9NAF7+7AAvP1hAFb9hP7y/zb9QgDe/OIAWfw3Aff7RAHG++kA6fx0AK39vf0vAGv9GgFL+5MBsvwyAIX9Cv8n/xr+W//g/b//K/2KAP/80gDe+70AHP1NAPz97v1uAKr8SgFV+/oBSPxlAC39KQAO/b//8f3E/7/9Yv5w/6n9EAGx+z0BzPxbAHX9Vv4MAGD9rv+n/d//dv1j/9z+Ov/U/NwAs/yCAMj9lf7n//38VAFN+2sBvf3k/nf+x/6W/iT+Lv9b/1b9D/8f/3X9mQDo/BQAYP2O/8/+pPxEAvX7kv+B/ur+Xf7r/YQAuf3X/UIAR/1B/3f/Uv04AJD8LAE3/Mz/EQDV+ycBAf0PALT8DwAG/9T9Kf+F/i3+EP9h/7f9x/9T/WUA/vu8ARX9yP1QAFL9DABG/JcBtvyM/4j+e/4M/k//+f5x/W0Auvx6AFP8hQKV+lwBLf0KADf9U//f/5j8RwGu+zUB+vsTAsf7PABW/uH9kP8E/s0AGvvRAcn8agAv/DIB1PwPAKX+i/3B/4H8eALp+YIDKvqiAcv88QAj/eb9pAAj/YD/Pf3LAC78jwEI/DwAKf1oAHf+lf1KAcz6BQKm/AQBtPufAMn+zf3h/nz+U/+S/bwAnfsLAX38sAGf+2wB1/xO/lcAu/14/zb8vQEX/cf+zP5f/mr/+f2x/7v8AQAD/pf/hP1yAGD8CwA3/+X9yv6F/e0BR/tGAWP8lwCl/aP/H/4R/rf/7/1y/0f+8f5A/YEABP6l/tv9sP+N/z788QAg/IUBIPwRAQj9I/8n/wb+AwBM/Xf/Iv0pAaP8nP9Y/UQBMvz+/0P+9P5W/2P9qAA3/IgAv/2m/4j+kP3P/9T9FwAb/WH/gf7Q/xn92P+W/S8AIf2l/wH/Mv1wAMX8VQH++z4Azf36/gL/uf19/+H+D/48/8L94f/H/bH+df/q/QT/S/5U/8L+Lv17ANf9LP82/nn+vf+0/X//if0f/yL/yP1h/37+cv7D/kb+BwDm/Gr/Pf8l/oj+3f6q/i3/c/2CAGH8vwCq/W3+of/V/YP/+Px8AF/9U/5n/xv/mP0D/6f+GP/4/Tz/mf5k/tr/Of19/1r+Ef8f/o/+2v9j/CUAS/5C/8/8EwBc/sT+Xf4W/1j+l/6q/zv98P+8/bj/U/0cAAH+5/3U/3n+pf5z/ZIAif1h/839Kv86/o/+Yf85/SkAL/0vAPb8kQDH/Ob/7P69/vv9gf54AIr8gwDN/PYAoPxAACv+OP6c/3v9UAAf/TsAn/zVAMv9Xf93/NkA8/2W/jL/t/3DAHv7PQKh+wgB/vyi/9L+mP0LAH39awCH/fv+rP3nABL95f93/TcA3P3P/T8BgPu0AWr7BQId/J7/m/67/kP/nf3g/oH+n/+g/bX/Iv1HAV77JgH+/WD+S/+G/V8BDfs6AYn9W//B/g/+af/j/eb/W/1t/1z+4v/D+2gCsvtHAD79nwC7/WP9GgHI/CMAPf0FAJP9cP94/v/9P//u/gP+4P0FAXD8o/9y/gsA3Pze/pEANPy1AMD8HAHp+1YBSvw2ABP+WP85/R8AHP8B/bH/cP55/0j8lAHi/Oj+Of7S/1f+7/1IAJr8vgBG/Zj/T/0mAED+z/wSASf98f4+/XABDvz//5D94wDT+zYByPze/4r+5P1//4f9lAEf++oAJf4d/4L9RwA1/vP9vf6s/y7+Bv6d/x/9NwDA/ev+cv79/oz/LvyTAe38Sf/n/aAAz/xs/33+FADN/K//W/5p/tX/G/0hAD/9CwH2+7QA8v3j/ov99wBB/eX+/v1mAFH9Nf8C//z9rv/t/bT+ov4g/5j+X/2BAKX9Z/4f/z3/4v1H/or/fv48/sT+3f5b/r3/OP3Q/+P9WQDb+y8BQf2X/xD9+wAX/dP+n/6v/4v9Lf8r/kr/gf6i/in+Cv+K/4H9sP40/77+Rv34/4j+ef50/ekA2/waAF39RABd/S0AyPwCAGH+jP/U/Pv/P/4E/7/9eQDZ/WT+5/7M/zP9uf+t/SIAe/2N/0D9xv9Y/2r9NP9//ub/PfxHATD9uv8z/EsCs/sAAS38QgH7/A4AlP3z/bYAaf0T/xL+bv/R/Wf+IQCh/V/+sP5ZAHv8VgCb/NwBlfs2AbP7ggAK/279m//p/PgAIPyTAez88P8C/FYCwfvqAPD7MgEX/sf9BwBg/NABmPz4/7L95P6t/mj+RP/8/aH+5v3dAO37IwFi+08DxPr+AMf86f/h/hT+5v/x/DAASv2iALH87wBM++0B3PzD/wL9vP8PAML73ACS/PoA2fzbAJf9Y/5Q/zX+jf+m/cP//ft4AkP7OQG3+7YCFfyN/9r9Of+v/of+h//9/A0AbP2KAAf97f+V/Sz/5P8g/UL//f2nAOj8+P7p/t7+6v51/iz/Q/06ADP9lABn/CEB9PsTAZ39uf47/kv9miSAJpElVyZOJl8l7iUlJsEm6ySaJeYmFyWXJqQl4CXiJfwliCbCJCYnXSVNJlAlziahJJcmayboJYIlqSVgJ7EkKif7JEwmAiZwJo0lpCXTJnQlgSZsJdEmICTMJyUlNyYxJUUmZSYbJQ8noiQRJy4lBidWJKYnpSSCJwEl5ib6JO0lMye6JPomWCSjJ5kkACcZJQkmUCacJfoldyXMJgglFSfTJBMnSiSYJyclfCZvJc4leSYSJQknSCTBJ5YkCCfoJBQnBCXRJrklUyZWJQwmgSZMJaUmaSRxJ8gkASf1JGYmzCY3JZAmSiWoJgwltyanJfQlUiX/Js4kOCf9JCEmQCYvJfYmRCTVJ70kRCbeJecl+yXTJVsmxyW4JWMm+yWAJfcmiCT5JkMlbCbIJWslhSfPI20njSXJJQAm/yVoJlol9CWcJuYkzCbiJQ8lJyfXJCknqCT7JvElviTfJ3Mk7yZxJbUmlCXAJRUm1iXaJZUm2SVLJd8mASX4Js0kmCeYJFUm+ybGJNkmHSU9J8ckziZyJd0lQCaCJpclnCX7JpEkUifFJKcnlyM7KLMkiSZuJXkm6CVBJR4nTSTAJ7EkdicDJJgnRSW5JdwmViV+JnokIihBJBEn3yRrJ8EkHicSJXolNyfMJJ4niyPqKCQjbyjDJLsm7iSUJrUm8yTFJlQl7ibkJIQn1CO2J18lgCZoJakl8ib2I4coHyTtJs8kYicyJeYlVSbAJWgmliW/JkUkOChkJFUnVSR9J5wkoSapJs0kdyaaJUgnsCSNJsYl8iVdJo8lQSZRJWUn3CSpJloloibTJConlSVHJY4mpSXkJisknSdwJGYnECU/Jj8lYSY3JkQlgCaWJSImsCXlJgwlLibsJVImuCUTJWcnjyTbJ0YkMCfGJOkmoCWIJZsmGyV4Jnsl9iZ9JBEnWCXjJnokPScmJUomGSYaJcYm3iQxJ9IkXibLJZglniZ1JXImIiXPJn4lUybxJNAmKSXvJuwkjCbTJYkl4SatJG0ndiQ4J1IlXCbiJbclTSbcJZglNyZ2JZEmmSX5JSImpSVBJrMlICbxJZ4l8SbsJGAmtiUcJjAmgCU8JqMliCb/JV0lZSboJfElGia0JWwmMCXlJp4lriUoJgomkyU/Jmwlpib9JHMn3SQZJnEmXiVFJlwl1CYxJW0mbyZ3JcIliybWJS0m4yUYJrQlGSZNJhAlpib7JfAl5SUKJlQmDiVoJ0AlOialJekmUyVmJtIlCibKJXUm9SUgJe0mgyVUJoElmSZZJR0mpSY1JR0m7yWWJh0lmiZ1JUUmGiY0Ju4lYSU4J/Qk2iY6Je0m3CT4Jn8loCUAJkYmMyYLJSknzyQCJ/wk1SYUJTYmiiYSJeQmBCWzJgslSyfVJEMmvSU2J/okOiYgJj0l8ia2JKEn4yPLJ88kgybmJbklciZKJbsmECV2JuMllCajJPUmHiWGJo0l8yWjJlwkISj9I7UnmCTZJqQlCyYSJnglmCYOJgomXSW8JvIkWyeAJI0nxSRQJmUmHiUSJ24kqifpJI8mnyWpJXQmsCUtJnMlpSZvJZAm3CSqJ+4jwCfjJG0mbSUEJrgmwyTlJgIlpCZ4JYAmZiU0JjEmvSXvJegloSafJDknRCUiJmslkSYeJu4kOifIJDMnzCRJJ1skbycIJXgmeyWuJmUlmCXoJmUlQCZQJSknkiTzJq0lUSaBJQomeCb5JG4nkiTsJmklqyZhJe0lGSe7JAAnqCW9JokkZyfkJCcngCSeJ2MkLCeHJcolvSYzJcsmOCTNJ/IkVCa0JYomMCVFJhIm9CXZJc4luiYsJSEn+SRuJh4mzyUtJg0lhid2JPomcSWrJsQkIycyJZomFSUHJ7Ul7CWgJu4kKycOJdcmnCRTJ/skZiaoJbom1iSNJr8lRyZ5JVIm7SXMJUMmhyUcJl4m2CXwJYkl9yb6JIom2iUGJoslSiYiJqQlLSYhJhEmwCUpJi0l9SZuJWUm4CR/J9IksyZyJb0mBCW/JrwlMCZdJawmbiWiJlElEybXJa4mnyWcJVwmMiamJQ4mmiZJJUYm6SWtJtEk+CYRJbwmUiVPJgwlQidPJRQmeyX4JkwlTyZyJZ0m2CSuJo4lZCYZJekmMCX1JtwkZiaPJfYmaCWAJaEmfCVlJiIlViduJAMnJiVKJ0AkWifAJG4n0SR1Jh4lyyanJtEkXybFJRsmISblJX4mBSW2JtYlQSbeJFMn0yS2J9UjiCelJLAnbCVdJcsmMiUyJ/AkFyeiJOAmMCWVJ+cjsCeEJLEn7yTLJZomEiWlJ1wkkSavJUgmPibCJR8m0yUwJuYlyyZ8JM4nGCR/KFMj1yfIJAwn0yWTJS4mZCXlJkklwCbDJFgnSyQ+KAok9CZrJbImMiZSJLAnrCRuJ+YknSbIJI4mISazJUgmcyXOJvgkJih1IxgoKCQCKN4jBieNJXIm9CXpJQkmOCVRJ+Ek7Sa9JCknOSVOJkkmtST9JmolzSalJLgm0CX7Jd0l9CXTJcAl3iapJE8npSSHJyMkySfAJB0mNyYzJvom,"[""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b6"",""y_b6"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b6"",""y_b6"",""y_b6"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b6"",""y_b7"",""y_b7"",""y_b6"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7""]",rotor,unbalance,15_hz,loaded,0.2,"{""axis_nrmse"":[1.0,1.0,1.0],""state_error_probability"":0.75}"
> ep_0795720dcfc59730ad,/wGV/sAAcgAO/8wApAA4AKj+YADIATn/yP+9AFn/hwGp/v8AVf8kAfT/Jf8GAcn//f9zAC0Bmv4HAD4ApQF1/l8AdADq/6oAI/+xAKX/XQEA/y8AOwAZALj/LQGNACL+VAEYAAsBUf5TAbb/SgA/AEv/PgDPAFsAIP+zAHj/XwCJ/1oC2P1nAHUAhAD7/zn/UgH+/oMBKf+w/8QA7QDw/n0ASACz/8T/ZwFTABT+owGl/5IAw/9RAO7/TQDzAED+6gDQAL3/Wf9WAfL+8v+GAHsBWv5/AGcA0/+oANf/7f/z/3EBhP58/14BKwAw/wMBZADN/kkAqAFW/5z/rABp/8IAFQDz/6z/FwFkAO796wFMAH//MQAcATD/eP/VANAA1v4JAT//RQC/AMX/EgDM/6YBY/7h//wBvv5FAJYAZQA1/4D//wEf/0UAfADe/lYB4P/A/5kA1f8tAaP9VAK0/zT/sgBDAG8At/6yAC4BSf+mAGv/zf/nAKL/TAAhAEwA/v+9/sYCQf4WAKIAvQBt//n+wAG2/04A4//8/5D/bwHx/uIAz/9nAOL+DgEmARf+6QC9AF8Aiv7MAKQAx/9xAKf/GQDU/3ABQ/7tAQL/KwCE/xcCNf+z/qYBnwAj/2b/aQEh/7AB5v7cAPP+oQF1/63/twFR/l0AxwAVAQP+ZQC4AXP/b/9/ABUAEQA7AWP+JgEI/8sBQf7yAbj/av6hAZ4Atf+T/twBbwBv/87/yAAm/7YBMv+//3cAAwBYAH7/2wH8/T8A5gFq/2j/dP8qAvL+XwCS/4IA6P8FAdv+yAD5/wIAEgDAAGgAGv7dAYoAcP8v/xkB1wAa/1sAwP+2ABAANQC4/5kA3/+v/9EAOwCN/zX/CwJJ//T/Jv9UAvn+JQDD/18AZACX/5AAsv+aAHT/SQDiAOH/XP9/ACwBOv9c//8A4wDH/pEA3v/bAH//FwDPAGn//ADA/p8Bl//p/7n/OQHj/3T/4/+9ASr/2v9NAHUAPgAs//sAsP+AAKr/q/9oAfX+OQA+ALoAoP8y/6kB4f+F/0MAIACeAJP/t//3ALr/mwAI/3IBlv+c/5wAkwC3/53/WgAdAfL+jACo/wQBBABW/3YAUwA9AIb/cwCiAAn/VgAlAYD/FgDR/1ABQ/8IAPj/FgAYAUX/1//dACUALABP/7oBpP4eANIAiQDs/k4ASQCfAFz/ZwCl/9YAdQDH/rkAJABpAED/VAHH/x7/1gAJAT//nP95AMYAov87AL7/QQCnABYAD/8wAX7/oABk/4sBjP5lANcAXABF//7/7wDm/ycAm/92AAoAvAAx/2wAMAD5/ysAUgBJABP/BwGeALn/cP+KAMAAT/+QAHH/LwEz/zIB3v4OAXz/cQBJAEgAsP+m/zsB+v99/3//jQFh/3YArP+hAOj/DQC8AAn/HgFF/8IAAwDu//n/0/8mAWT/z/9cAO4ALf/qAC//bgHC/jEBqP/p/78AKv9VAVf/NQDh/8kAIgA8/0IA4QCF/3UAt/8lALYAC/9HARz/2QCX/woAJgGR/h0Bvv/fAFX/IQCJACYA0/95AGj/HAGR/+T/1wCN/64AEP+RAVT/t/9HAar/OQBy/94A1/9hAPn/DQAIAOMAHv96AMEAbv9AACoA7ACW/iwBfACe/73/YgBDAOH/awCZ/1MAXAAWAEv/RQEKACr/iQBxANn/Wv+qAXn/tP/h/zkB9f4AAYn/KgBwAN//MwB7/6UB3/4BAMAA4f91/9cAgQDF/yr/NgHn/9P/hABc/xEBnf8ZABwAdwDdAJT+MgHe/8T/4v81Acf/4P96/5cB6v6MAB8A4P/eAOf+CgFT/ycBjf/U/6kACQBU/yMB6v9VAP/+7QBwAOz+0gC8/54Aqv+w/9QAof/tADf/mAAhAL3/1v8nAdb/0P+c/1UBOP+1/ycBo/+YAOj+CAGG/zUBXP9CAA4AowD6/hYBLgAKAHT/BAHG/5X/SQDyAMf/7v+l/5EAOAByAET/nwAbAOj/0P/FACAAIv8ZAdb/JQA0/3sBxv9nAN/+uwDk/0EB5/6ZAO3/QgCC/8oA8//b/9n/MwHx/nQAqv9WAdj/6P9S/5kA0wDD/9z/GgChACL/QgFl/wQBx/6lARD/vgDp/j4BXABBAPH+KwDaAFgAmv81ANj/SADL/9YAff+GAI7/DwFN/y8ASP/AAeb/u/8c/40AHwE4/0cBZP6fAe3+IwFV/+4ABf9DAX//zQAt/pQBuAC8/8n/bP8NAQoASgAaAPv+nwEJ/7oALADe/7v/AAEHAKP/4v6XAjb/7P8NADX/0gH7/oYBTv5DAfX/4v8xAP0AMf6sAcz/sQAQ/mQBLAEH/2oAbf8mAOkA+P8cAGP/9wDE/7z/RAFH/1H/4QGD/+j/jf6TApf/m/+WAAv/5wAdAJoAQP+3AM7/QgCo/4YB4P1nAXEA6v8M/1wAbwFU/ysA9/+y/2cAzABl/wsAcwDO/x0ADgACASX+CwItAGf/Rv9DAaYAOv9pAEUAev+mALwADf8KAaL/HgC4/xQBsv///ioCaf/5/ocA/P0v/5L+bf5L/ln/0v4b/pL9xQCM/l39q/9r/i3/2v2p/3X+5P0zAPf8KgBr/ScAIf3OAEr9Uv75/q3/of6p/M0AEf0RAH39xP+G/UH/w/4M/kb/2P2+/0T9NAF7+7AAvP1hAFb9hP7y/zb9QgDe/OIAWfw3Aff7RAHG++kA6fx0AK39vf0vAGv9GgFL+5MBsvwyAIX9Cv8n/xr+W//g/b//K/2KAP/80gDe+70AHP1NAPz97v1uAKr8SgFV+/oBSPxlAC39KQAO/b//8f3E/7/9Yv5w/6n9EAGx+z0BzPxbAHX9Vv4MAGD9rv+n/d//dv1j/9z+Ov/U/NwAs/yCAMj9lf7n//38VAFN+2sBvf3k/nf+x/6W/iT+Lv9b/1b9D/8f/3X9mQDo/BQAYP2O/8/+pPxEAvX7kv+B/ur+Xf7r/YQAuf3X/UIAR/1B/3f/Uv04AJD8LAE3/Mz/EQDV+ycBAf0PALT8DwAG/9T9Kf+F/i3+EP9h/7f9x/9T/WUA/vu8ARX9yP1QAFL9DABG/JcBtvyM/4j+e/4M/k//+f5x/W0Auvx6AFP8hQKV+lwBLf0KADf9U//f/5j8RwGu+zUB+vsTAsf7PABW/uH9kP8E/s0AGvvRAcn8agAv/DIB1PwPAKX+i/3B/4H8eALp+YIDKvqiAcv88QAj/eb9pAAj/YD/Pf3LAC78jwEI/DwAKf1oAHf+lf1KAcz6BQKm/AQBtPufAMn+zf3h/nz+U/+S/bwAnfsLAX38sAGf+2wB1/xO/lcAu/14/zb8vQEX/cf+zP5f/mr/+f2x/7v8AQAD/pf/hP1yAGD8CwA3/+X9yv6F/e0BR/tGAWP8lwCl/aP/H/4R/rf/7/1y/0f+8f5A/YEABP6l/tv9sP+N/z788QAg/IUBIPwRAQj9I/8n/wb+AwBM/Xf/Iv0pAaP8nP9Y/UQBMvz+/0P+9P5W/2P9qAA3/IgAv/2m/4j+kP3P/9T9FwAb/WH/gf7Q/xn92P+W/S8AIf2l/wH/Mv1wAMX8VQH++z4Azf36/gL/uf19/+H+D/48/8L94f/H/bH+df/q/QT/S/5U/8L+Lv17ANf9LP82/nn+vf+0/X//if0f/yL/yP1h/37+cv7D/kb+BwDm/Gr/Pf8l/oj+3f6q/i3/c/2CAGH8vwCq/W3+of/V/YP/+Px8AF/9U/5n/xv/mP0D/6f+GP/4/Tz/mf5k/tr/Of19/1r+Ef8f/o/+2v9j/CUAS/5C/8/8EwBc/sT+Xf4W/1j+l/6q/zv98P+8/bj/U/0cAAH+5/3U/3n+pf5z/ZIAif1h/839Kv86/o/+Yf85/SkAL/0vAPb8kQDH/Ob/7P69/vv9gf54AIr8gwDN/PYAoPxAACv+OP6c/3v9UAAf/TsAn/zVAMv9Xf93/NkA8/2W/jL/t/3DAHv7PQKh+wgB/vyi/9L+mP0LAH39awCH/fv+rP3nABL95f93/TcA3P3P/T8BgPu0AWr7BQId/J7/m/67/kP/nf3g/oH+n/+g/bX/Iv1HAV77JgH+/WD+S/+G/V8BDfs6AYn9W//B/g/+af/j/eb/W/1t/1z+4v/D+2gCsvtHAD79nwC7/WP9GgHI/CMAPf0FAJP9cP94/v/9P//u/gP+4P0FAXD8o/9y/gsA3Pze/pEANPy1AMD8HAHp+1YBSvw2ABP+WP85/R8AHP8B/bH/cP55/0j8lAHi/Oj+Of7S/1f+7/1IAJr8vgBG/Zj/T/0mAED+z/wSASf98f4+/XABDvz//5D94wDT+zYByPze/4r+5P1//4f9lAEf++oAJf4d/4L9RwA1/vP9vf6s/y7+Bv6d/x/9NwDA/ev+cv79/oz/LvyTAe38Sf/n/aAAz/xs/33+FADN/K//W/5p/tX/G/0hAD/9CwH2+7QA8v3j/ov99wBB/eX+/v1mAFH9Nf8C//z9rv/t/bT+ov4g/5j+X/2BAKX9Z/4f/z3/4v1H/or/fv48/sT+3f5b/r3/OP3Q/+P9WQDb+y8BQf2X/xD9+wAX/dP+n/6v/4v9Lf8r/kr/gf6i/in+Cv+K/4H9sP40/77+Rv34/4j+ef50/ekA2/waAF39RABd/S0AyPwCAGH+jP/U/Pv/P/4E/7/9eQDZ/WT+5/7M/zP9uf+t/SIAe/2N/0D9xv9Y/2r9NP9//ub/PfxHATD9uv8z/EsCs/sAAS38QgH7/A4AlP3z/bYAaf0T/xL+bv/R/Wf+IQCh/V/+sP5ZAHv8VgCb/NwBlfs2AbP7ggAK/279m//p/PgAIPyTAez88P8C/FYCwfvqAPD7MgEX/sf9BwBg/NABmPz4/7L95P6t/mj+RP/8/aH+5v3dAO37IwFi+08DxPr+AMf86f/h/hT+5v/x/DAASv2iALH87wBM++0B3PzD/wL9vP8PAML73ACS/PoA2fzbAJf9Y/5Q/zX+jf+m/cP//ft4AkP7OQG3+7YCFfyN/9r9Of+v/of+h//9/A0AbP2KAAf97f+V/Sz/5P8g/UL//f2nAOj8+P7p/t7+6v51/iz/Q/06ADP9lABn/CEB9PsTAZ39uf47/kv9miSAJpElVyZOJl8l7iUlJsEm6ySaJeYmFyWXJqQl4CXiJfwliCbCJCYnXSVNJlAlziahJJcmayboJYIlqSVgJ7EkKif7JEwmAiZwJo0lpCXTJnQlgSZsJdEmICTMJyUlNyYxJUUmZSYbJQ8noiQRJy4lBidWJKYnpSSCJwEl5ib6JO0lMye6JPomWCSjJ5kkACcZJQkmUCacJfoldyXMJgglFSfTJBMnSiSYJyclfCZvJc4leSYSJQknSCTBJ5YkCCfoJBQnBCXRJrklUyZWJQwmgSZMJaUmaSRxJ8gkASf1JGYmzCY3JZAmSiWoJgwltyanJfQlUiX/Js4kOCf9JCEmQCYvJfYmRCTVJ70kRCbeJecl+yXTJVsmxyW4JWMm+yWAJfcmiCT5JkMlbCbIJWslhSfPI20njSXJJQAm/yVoJlol9CWcJuYkzCbiJQ8lJyfXJCknqCT7JvElviTfJ3Mk7yZxJbUmlCXAJRUm1iXaJZUm2SVLJd8mASX4Js0kmCeYJFUm+ybGJNkmHSU9J8ckziZyJd0lQCaCJpclnCX7JpEkUifFJKcnlyM7KLMkiSZuJXkm6CVBJR4nTSTAJ7EkdicDJJgnRSW5JdwmViV+JnokIihBJBEn3yRrJ8EkHicSJXolNyfMJJ4niyPqKCQjbyjDJLsm7iSUJrUm8yTFJlQl7ibkJIQn1CO2J18lgCZoJakl8ib2I4coHyTtJs8kYicyJeYlVSbAJWgmliW/JkUkOChkJFUnVSR9J5wkoSapJs0kdyaaJUgnsCSNJsYl8iVdJo8lQSZRJWUn3CSpJloloibTJConlSVHJY4mpSXkJisknSdwJGYnECU/Jj8lYSY3JkQlgCaWJSImsCXlJgwlLibsJVImuCUTJWcnjyTbJ0YkMCfGJOkmoCWIJZsmGyV4Jnsl9iZ9JBEnWCXjJnokPScmJUomGSYaJcYm3iQxJ9IkXibLJZglniZ1JXImIiXPJn4lUybxJNAmKSXvJuwkjCbTJYkl4SatJG0ndiQ4J1IlXCbiJbclTSbcJZglNyZ2JZEmmSX5JSImpSVBJrMlICbxJZ4l8SbsJGAmtiUcJjAmgCU8JqMliCb/JV0lZSboJfElGia0JWwmMCXlJp4lriUoJgomkyU/Jmwlpib9JHMn3SQZJnEmXiVFJlwl1CYxJW0mbyZ3JcIliybWJS0m4yUYJrQlGSZNJhAlpib7JfAl5SUKJlQmDiVoJ0AlOialJekmUyVmJtIlCibKJXUm9SUgJe0mgyVUJoElmSZZJR0mpSY1JR0m7yWWJh0lmiZ1JUUmGiY0Ju4lYSU4J/Qk2iY6Je0m3CT4Jn8loCUAJkYmMyYLJSknzyQCJ/wk1SYUJTYmiiYSJeQmBCWzJgslSyfVJEMmvSU2J/okOiYgJj0l8ia2JKEn4yPLJ88kgybmJbklciZKJbsmECV2JuMllCajJPUmHiWGJo0l8yWjJlwkISj9I7UnmCTZJqQlCyYSJnglmCYOJgomXSW8JvIkWyeAJI0nxSRQJmUmHiUSJ24kqifpJI8mnyWpJXQmsCUtJnMlpSZvJZAm3CSqJ+4jwCfjJG0mbSUEJrgmwyTlJgIlpCZ4JYAmZiU0JjEmvSXvJegloSafJDknRCUiJmslkSYeJu4kOifIJDMnzCRJJ1skbycIJXgmeyWuJmUlmCXoJmUlQCZQJSknkiTzJq0lUSaBJQomeCb5JG4nkiTsJmklqyZhJe0lGSe7JAAnqCW9JokkZyfkJCcngCSeJ2MkLCeHJcolvSYzJcsmOCTNJ/IkVCa0JYomMCVFJhIm9CXZJc4luiYsJSEn+SRuJh4mzyUtJg0lhid2JPomcSWrJsQkIycyJZomFSUHJ7Ul7CWgJu4kKycOJdcmnCRTJ/skZiaoJbom1iSNJr8lRyZ5JVIm7SXMJUMmhyUcJl4m2CXwJYkl9yb6JIom2iUGJoslSiYiJqQlLSYhJhEmwCUpJi0l9SZuJWUm4CR/J9IksyZyJb0mBCW/JrwlMCZdJawmbiWiJlElEybXJa4mnyWcJVwmMiamJQ4mmiZJJUYm6SWtJtEk+CYRJbwmUiVPJgwlQidPJRQmeyX4JkwlTyZyJZ0m2CSuJo4lZCYZJekmMCX1JtwkZiaPJfYmaCWAJaEmfCVlJiIlViduJAMnJiVKJ0AkWifAJG4n0SR1Jh4lyyanJtEkXybFJRsmISblJX4mBSW2JtYlQSbeJFMn0yS2J9UjiCelJLAnbCVdJcsmMiUyJ/AkFyeiJOAmMCWVJ+cjsCeEJLEn7yTLJZomEiWlJ1wkkSavJUgmPibCJR8m0yUwJuYlyyZ8JM4nGCR/KFMj1yfIJAwn0yWTJS4mZCXlJkklwCbDJFgnSyQ+KAok9CZrJbImMiZSJLAnrCRuJ+YknSbIJI4mISazJUgmcyXOJvgkJih1IxgoKCQCKN4jBieNJXIm9CXpJQkmOCVRJ+Ek7Sa9JCknOSVOJkkmtST9JmolzSalJLgm0CX7Jd0l9CXTJcAl3iapJE8npSSHJyMkySfAJB0mNyYzJvom,"[""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b6"",""y_b6"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b6"",""y_b6"",""y_b6"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b6"",""y_b7"",""y_b7"",""y_b6"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7""]",rotor,unbalance,15_hz,loaded,0.2,"{""axis_nrmse"":[1.0,1.0,1.0],""state_error_probability"":0.75}"
> ep_0c4b1c98482497f079,/wGV/sAAcgAO/8wApAA4AKj+YADIATn/yP+9AFn/hwGp/v8AVf8kAfT/Jf8GAcn//f9zAC0Bmv4HAD4ApQF1/l8AdADq/6oAI/+xAKX/XQEA/y8AOwAZALj/LQGNACL+VAEYAAsBUf5TAbb/SgA/AEv/PgDPAFsAIP+zAHj/XwCJ/1oC2P1nAHUAhAD7/zn/UgH+/oMBKf+w/8QA7QDw/n0ASACz/8T/ZwFTABT+owGl/5IAw/9RAO7/TQDzAED+6gDQAL3/Wf9WAfL+8v+GAHsBWv5/AGcA0/+oANf/7f/z/3EBhP58/14BKwAw/wMBZADN/kkAqAFW/5z/rABp/8IAFQDz/6z/FwFkAO796wFMAH//MQAcATD/eP/VANAA1v4JAT//RQC/AMX/EgDM/6YBY/7h//wBvv5FAJYAZQA1/4D//wEf/0UAfADe/lYB4P/A/5kA1f8tAaP9VAK0/zT/sgBDAG8At/6yAC4BSf+mAGv/zf/nAKL/TAAhAEwA/v+9/sYCQf4WAKIAvQBt//n+wAG2/04A4//8/5D/bwHx/uIAz/9nAOL+DgEmARf+6QC9AF8Aiv7MAKQAx/9xAKf/GQDU/3ABQ/7tAQL/KwCE/xcCNf+z/qYBnwAj/2b/aQEh/7AB5v7cAPP+oQF1/63/twFR/l0AxwAVAQP+ZQC4AXP/b/9/ABUAEQA7AWP+JgEI/8sBQf7yAbj/av6hAZ4Atf+T/twBbwBv/87/yAAm/7YBMv+//3cAAwBYAH7/2wH8/T8A5gFq/2j/dP8qAvL+XwCS/4IA6P8FAdv+yAD5/wIAEgDAAGgAGv7dAYoAcP8v/xkB1wAa/1sAwP+2ABAANQC4/5kA3/+v/9EAOwCN/zX/CwJJ//T/Jv9UAvn+JQDD/18AZACX/5AAsv+aAHT/SQDiAOH/XP9/ACwBOv9c//8A4wDH/pEA3v/bAH//FwDPAGn//ADA/p8Bl//p/7n/OQHj/3T/4/+9ASr/2v9NAHUAPgAs//sAsP+AAKr/q/9oAfX+OQA+ALoAoP8y/6kB4f+F/0MAIACeAJP/t//3ALr/mwAI/3IBlv+c/5wAkwC3/53/WgAdAfL+jACo/wQBBABW/3YAUwA9AIb/cwCiAAn/VgAlAYD/FgDR/1ABQ/8IAPj/FgAYAUX/1//dACUALABP/7oBpP4eANIAiQDs/k4ASQCfAFz/ZwCl/9YAdQDH/rkAJABpAED/VAHH/x7/1gAJAT//nP95AMYAov87AL7/QQCnABYAD/8wAX7/oABk/4sBjP5lANcAXABF//7/7wDm/ycAm/92AAoAvAAx/2wAMAD5/ysAUgBJABP/BwGeALn/cP+KAMAAT/+QAHH/LwEz/zIB3v4OAXz/cQBJAEgAsP+m/zsB+v99/3//jQFh/3YArP+hAOj/DQC8AAn/HgFF/8IAAwDu//n/0/8mAWT/z/9cAO4ALf/qAC//bgHC/jEBqP/p/78AKv9VAVf/NQDh/8kAIgA8/0IA4QCF/3UAt/8lALYAC/9HARz/2QCX/woAJgGR/h0Bvv/fAFX/IQCJACYA0/95AGj/HAGR/+T/1wCN/64AEP+RAVT/t/9HAar/OQBy/94A1/9hAPn/DQAIAOMAHv96AMEAbv9AACoA7ACW/iwBfACe/73/YgBDAOH/awCZ/1MAXAAWAEv/RQEKACr/iQBxANn/Wv+qAXn/tP/h/zkB9f4AAYn/KgBwAN//MwB7/6UB3/4BAMAA4f91/9cAgQDF/yr/NgHn/9P/hABc/xEBnf8ZABwAdwDdAJT+MgHe/8T/4v81Acf/4P96/5cB6v6MAB8A4P/eAOf+CgFT/ycBjf/U/6kACQBU/yMB6v9VAP/+7QBwAOz+0gC8/54Aqv+w/9QAof/tADf/mAAhAL3/1v8nAdb/0P+c/1UBOP+1/ycBo/+YAOj+CAGG/zUBXP9CAA4AowD6/hYBLgAKAHT/BAHG/5X/SQDyAMf/7v+l/5EAOAByAET/nwAbAOj/0P/FACAAIv8ZAdb/JQA0/3sBxv9nAN/+uwDk/0EB5/6ZAO3/QgCC/8oA8//b/9n/MwHx/nQAqv9WAdj/6P9S/5kA0wDD/9z/GgChACL/QgFl/wQBx/6lARD/vgDp/j4BXABBAPH+KwDaAFgAmv81ANj/SADL/9YAff+GAI7/DwFN/y8ASP/AAeb/u/8c/40AHwE4/0cBZP6fAe3+IwFV/+4ABf9DAX//zQAt/pQBuAC8/8n/bP8NAQoASgAaAPv+nwEJ/7oALADe/7v/AAEHAKP/4v6XAjb/7P8NADX/0gH7/oYBTv5DAfX/4v8xAP0AMf6sAcz/sQAQ/mQBLAEH/2oAbf8mAOkA+P8cAGP/9wDE/7z/RAFH/1H/4QGD/+j/jf6TApf/m/+WAAv/5wAdAJoAQP+3AM7/QgCo/4YB4P1nAXEA6v8M/1wAbwFU/ysA9/+y/2cAzABl/wsAcwDO/x0ADgACASX+CwItAGf/Rv9DAaYAOv9pAEUAev+mALwADf8KAaL/HgC4/xQBsv///ioCaf/5/ocA/P0v/5L+bf5L/ln/0v4b/pL9xQCM/l39q/9r/i3/2v2p/3X+5P0zAPf8KgBr/ScAIf3OAEr9Uv75/q3/of6p/M0AEf0RAH39xP+G/UH/w/4M/kb/2P2+/0T9NAF7+7AAvP1hAFb9hP7y/zb9QgDe/OIAWfw3Aff7RAHG++kA6fx0AK39vf0vAGv9GgFL+5MBsvwyAIX9Cv8n/xr+W//g/b//K/2KAP/80gDe+70AHP1NAPz97v1uAKr8SgFV+/oBSPxlAC39KQAO/b//8f3E/7/9Yv5w/6n9EAGx+z0BzPxbAHX9Vv4MAGD9rv+n/d//dv1j/9z+Ov/U/NwAs/yCAMj9lf7n//38VAFN+2sBvf3k/nf+x/6W/iT+Lv9b/1b9D/8f/3X9mQDo/BQAYP2O/8/+pPxEAvX7kv+B/ur+Xf7r/YQAuf3X/UIAR/1B/3f/Uv04AJD8LAE3/Mz/EQDV+ycBAf0PALT8DwAG/9T9Kf+F/i3+EP9h/7f9x/9T/WUA/vu8ARX9yP1QAFL9DABG/JcBtvyM/4j+e/4M/k//+f5x/W0Auvx6AFP8hQKV+lwBLf0KADf9U//f/5j8RwGu+zUB+vsTAsf7PABW/uH9kP8E/s0AGvvRAcn8agAv/DIB1PwPAKX+i/3B/4H8eALp+YIDKvqiAcv88QAj/eb9pAAj/YD/Pf3LAC78jwEI/DwAKf1oAHf+lf1KAcz6BQKm/AQBtPufAMn+zf3h/nz+U/+S/bwAnfsLAX38sAGf+2wB1/xO/lcAu/14/zb8vQEX/cf+zP5f/mr/+f2x/7v8AQAD/pf/hP1yAGD8CwA3/+X9yv6F/e0BR/tGAWP8lwCl/aP/H/4R/rf/7/1y/0f+8f5A/YEABP6l/tv9sP+N/z788QAg/IUBIPwRAQj9I/8n/wb+AwBM/Xf/Iv0pAaP8nP9Y/UQBMvz+/0P+9P5W/2P9qAA3/IgAv/2m/4j+kP3P/9T9FwAb/WH/gf7Q/xn92P+W/S8AIf2l/wH/Mv1wAMX8VQH++z4Azf36/gL/uf19/+H+D/48/8L94f/H/bH+df/q/QT/S/5U/8L+Lv17ANf9LP82/nn+vf+0/X//if0f/yL/yP1h/37+cv7D/kb+BwDm/Gr/Pf8l/oj+3f6q/i3/c/2CAGH8vwCq/W3+of/V/YP/+Px8AF/9U/5n/xv/mP0D/6f+GP/4/Tz/mf5k/tr/Of19/1r+Ef8f/o/+2v9j/CUAS/5C/8/8EwBc/sT+Xf4W/1j+l/6q/zv98P+8/bj/U/0cAAH+5/3U/3n+pf5z/ZIAif1h/839Kv86/o/+Yf85/SkAL/0vAPb8kQDH/Ob/7P69/vv9gf54AIr8gwDN/PYAoPxAACv+OP6c/3v9UAAf/TsAn/zVAMv9Xf93/NkA8/2W/jL/t/3DAHv7PQKh+wgB/vyi/9L+mP0LAH39awCH/fv+rP3nABL95f93/TcA3P3P/T8BgPu0AWr7BQId/J7/m/67/kP/nf3g/oH+n/+g/bX/Iv1HAV77JgH+/WD+S/+G/V8BDfs6AYn9W//B/g/+af/j/eb/W/1t/1z+4v/D+2gCsvtHAD79nwC7/WP9GgHI/CMAPf0FAJP9cP94/v/9P//u/gP+4P0FAXD8o/9y/gsA3Pze/pEANPy1AMD8HAHp+1YBSvw2ABP+WP85/R8AHP8B/bH/cP55/0j8lAHi/Oj+Of7S/1f+7/1IAJr8vgBG/Zj/T/0mAED+z/wSASf98f4+/XABDvz//5D94wDT+zYByPze/4r+5P1//4f9lAEf++oAJf4d/4L9RwA1/vP9vf6s/y7+Bv6d/x/9NwDA/ev+cv79/oz/LvyTAe38Sf/n/aAAz/xs/33+FADN/K//W/5p/tX/G/0hAD/9CwH2+7QA8v3j/ov99wBB/eX+/v1mAFH9Nf8C//z9rv/t/bT+ov4g/5j+X/2BAKX9Z/4f/z3/4v1H/or/fv48/sT+3f5b/r3/OP3Q/+P9WQDb+y8BQf2X/xD9+wAX/dP+n/6v/4v9Lf8r/kr/gf6i/in+Cv+K/4H9sP40/77+Rv34/4j+ef50/ekA2/waAF39RABd/S0AyPwCAGH+jP/U/Pv/P/4E/7/9eQDZ/WT+5/7M/zP9uf+t/SIAe/2N/0D9xv9Y/2r9NP9//ub/PfxHATD9uv8z/EsCs/sAAS38QgH7/A4AlP3z/bYAaf0T/xL+bv/R/Wf+IQCh/V/+sP5ZAHv8VgCb/NwBlfs2AbP7ggAK/279m//p/PgAIPyTAez88P8C/FYCwfvqAPD7MgEX/sf9BwBg/NABmPz4/7L95P6t/mj+RP/8/aH+5v3dAO37IwFi+08DxPr+AMf86f/h/hT+5v/x/DAASv2iALH87wBM++0B3PzD/wL9vP8PAML73ACS/PoA2fzbAJf9Y/5Q/zX+jf+m/cP//ft4AkP7OQG3+7YCFfyN/9r9Of+v/of+h//9/A0AbP2KAAf97f+V/Sz/5P8g/UL//f2nAOj8+P7p/t7+6v51/iz/Q/06ADP9lABn/CEB9PsTAZ39uf47/kv9miSAJpElVyZOJl8l7iUlJsEm6ySaJeYmFyWXJqQl4CXiJfwliCbCJCYnXSVNJlAlziahJJcmayboJYIlqSVgJ7EkKif7JEwmAiZwJo0lpCXTJnQlgSZsJdEmICTMJyUlNyYxJUUmZSYbJQ8noiQRJy4lBidWJKYnpSSCJwEl5ib6JO0lMye6JPomWCSjJ5kkACcZJQkmUCacJfoldyXMJgglFSfTJBMnSiSYJyclfCZvJc4leSYSJQknSCTBJ5YkCCfoJBQnBCXRJrklUyZWJQwmgSZMJaUmaSRxJ8gkASf1JGYmzCY3JZAmSiWoJgwltyanJfQlUiX/Js4kOCf9JCEmQCYvJfYmRCTVJ70kRCbeJecl+yXTJVsmxyW4JWMm+yWAJfcmiCT5JkMlbCbIJWslhSfPI20njSXJJQAm/yVoJlol9CWcJuYkzCbiJQ8lJyfXJCknqCT7JvElviTfJ3Mk7yZxJbUmlCXAJRUm1iXaJZUm2SVLJd8mASX4Js0kmCeYJFUm+ybGJNkmHSU9J8ckziZyJd0lQCaCJpclnCX7JpEkUifFJKcnlyM7KLMkiSZuJXkm6CVBJR4nTSTAJ7EkdicDJJgnRSW5JdwmViV+JnokIihBJBEn3yRrJ8EkHicSJXolNyfMJJ4niyPqKCQjbyjDJLsm7iSUJrUm8yTFJlQl7ibkJIQn1CO2J18lgCZoJakl8ib2I4coHyTtJs8kYicyJeYlVSbAJWgmliW/JkUkOChkJFUnVSR9J5wkoSapJs0kdyaaJUgnsCSNJsYl8iVdJo8lQSZRJWUn3CSpJloloibTJConlSVHJY4mpSXkJisknSdwJGYnECU/Jj8lYSY3JkQlgCaWJSImsCXlJgwlLibsJVImuCUTJWcnjyTbJ0YkMCfGJOkmoCWIJZsmGyV4Jnsl9iZ9JBEnWCXjJnokPScmJUomGSYaJcYm3iQxJ9IkXibLJZglniZ1JXImIiXPJn4lUybxJNAmKSXvJuwkjCbTJYkl4SatJG0ndiQ4J1IlXCbiJbclTSbcJZglNyZ2JZEmmSX5JSImpSVBJrMlICbxJZ4l8SbsJGAmtiUcJjAmgCU8JqMliCb/JV0lZSboJfElGia0JWwmMCXlJp4lriUoJgomkyU/Jmwlpib9JHMn3SQZJnEmXiVFJlwl1CYxJW0mbyZ3JcIliybWJS0m4yUYJrQlGSZNJhAlpib7JfAl5SUKJlQmDiVoJ0AlOialJekmUyVmJtIlCibKJXUm9SUgJe0mgyVUJoElmSZZJR0mpSY1JR0m7yWWJh0lmiZ1JUUmGiY0Ju4lYSU4J/Qk2iY6Je0m3CT4Jn8loCUAJkYmMyYLJSknzyQCJ/wk1SYUJTYmiiYSJeQmBCWzJgslSyfVJEMmvSU2J/okOiYgJj0l8ia2JKEn4yPLJ88kgybmJbklciZKJbsmECV2JuMllCajJPUmHiWGJo0l8yWjJlwkISj9I7UnmCTZJqQlCyYSJnglmCYOJgomXSW8JvIkWyeAJI0nxSRQJmUmHiUSJ24kqifpJI8mnyWpJXQmsCUtJnMlpSZvJZAm3CSqJ+4jwCfjJG0mbSUEJrgmwyTlJgIlpCZ4JYAmZiU0JjEmvSXvJegloSafJDknRCUiJmslkSYeJu4kOifIJDMnzCRJJ1skbycIJXgmeyWuJmUlmCXoJmUlQCZQJSknkiTzJq0lUSaBJQomeCb5JG4nkiTsJmklqyZhJe0lGSe7JAAnqCW9JokkZyfkJCcngCSeJ2MkLCeHJcolvSYzJcsmOCTNJ/IkVCa0JYomMCVFJhIm9CXZJc4luiYsJSEn+SRuJh4mzyUtJg0lhid2JPomcSWrJsQkIycyJZomFSUHJ7Ul7CWgJu4kKycOJdcmnCRTJ/skZiaoJbom1iSNJr8lRyZ5JVIm7SXMJUMmhyUcJl4m2CXwJYkl9yb6JIom2iUGJoslSiYiJqQlLSYhJhEmwCUpJi0l9SZuJWUm4CR/J9IksyZyJb0mBCW/JrwlMCZdJawmbiWiJlElEybXJa4mnyWcJVwmMiamJQ4mmiZJJUYm6SWtJtEk+CYRJbwmUiVPJgwlQidPJRQmeyX4JkwlTyZyJZ0m2CSuJo4lZCYZJekmMCX1JtwkZiaPJfYmaCWAJaEmfCVlJiIlViduJAMnJiVKJ0AkWifAJG4n0SR1Jh4lyyanJtEkXybFJRsmISblJX4mBSW2JtYlQSbeJFMn0yS2J9UjiCelJLAnbCVdJcsmMiUyJ/AkFyeiJOAmMCWVJ+cjsCeEJLEn7yTLJZomEiWlJ1wkkSavJUgmPibCJR8m0yUwJuYlyyZ8JM4nGCR/KFMj1yfIJAwn0yWTJS4mZCXlJkklwCbDJFgnSyQ+KAok9CZrJbImMiZSJLAnrCRuJ+YknSbIJI4mISazJUgmcyXOJvgkJih1IxgoKCQCKN4jBieNJXIm9CXpJQkmOCVRJ+Ek7Sa9JCknOSVOJkkmtST9JmolzSalJLgm0CX7Jd0l9CXTJcAl3iapJE8npSSHJyMkySfAJB0mNyYzJvom,"[""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b6"",""y_b6"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b6"",""y_b6"",""y_b6"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b6"",""y_b7"",""y_b7"",""y_b6"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7""]",rotor,unbalance,15_hz,loaded,0.2,"{""axis_nrmse"":[1.0,1.0,1.0],""state_error_probability"":0.75}"
> ep_161bf9e52ffb341026,OAGk/ygB8wAX/qcBgAIQALz+ggBFAff+1f8YAGsBFf85Apz/iQBzADkBpf47AeL/TgATAqb/lAHbAEj/YQF2/mT/bABKAqX+9QCi/4kBFQAgAaUBCf8IAAYBmv/Z/u4ALAC1/5gAvQAuAan/xACk/mwAKAGQAcz+OwANAKoASP+SAaL/mwDN/2QAkf8EAHsBMP8GAuMACACm/owCZf/vAU0BdQAkAcsAhQAyABkA9//5/vf/mP/FAKH/CgKW/7AASQCiAKH+AABIAKQBAf/U/xUAc//VAIb/nAB9/88ApAFv/4YADwA0AEsBdQBeAWAA1f5UAWcACABbAKwBWADVALj/TABlAWUBFgA8ACAAi/+3AWf/2gC0/uIA5v9DANABaf+tANIA7wDJ/7wAQwDE/p/+oACp/i0A5AKN/2kAewKHAGMAUv+zAEwADACz/8//wACvAcsA2/9UAOj/bQEUAJsA3P7cAQf/vwB/AMz/cQAJAKAB1P8/As7/VAFf/80Ar/+/AJ0AkgB7/6L+BAAC//4Bg/9M/8EBzf+hAFAAAQFUABkAVQB4/mEAaABHAa/+wQFhAHQAygCpABUBk//tAcYAYACk/33/5gBn/0EBIf8tALEAeADpAHcAJQDjAUsAgwEX/ikBUgFX/1YAYQCs/3f/qAB4AM3/wf9fASUARwGh/30A6v9eAEb/ogAEAbL/qABLANT/5gCy/0IAUQJnAAAAuP4tAiQAq/9tApP/HwBPAGsBJv+JAa7+6gD7/20B+P5lATwC/P0dAXX//ACI/lQCtgANAL0BjP/TAAf/kAFWAPP+2QHJ/+b/+v/CAEMAYwC2ARIAuf/AAI4Ai/8QAUcBlwD+ALsBowA8AR0ADv/MAIIBlP/U/+z/ewKBAFAAYf48AU0Bqf96/r8AWAFt/wUAmADTAIcAYwA8AoX/HgBWAFMAAgBKAMsBGP80AgUA8gCg/j8AbgC+AEYAvQAiAEgBLAAiAOf/fwDS/xIAkQDTALH/lwAnAewAawGd/xcCCP+3ANn/QwDn/yYB5v+5ANkBAAG4AGMAqABW/0IAJAEw/00BlQA0/1D/ggHJAHkAugCnAN8AVQBb/ycArv/LATT+cAAuAS8AC/9d/zsAZABK/28A5gApAFoBX/9VAJIAAADS/+IALgCNAA8AJP8yAYAAOwBWAH4A0f9A/rgAdf+cAtD+6wAZAGUBAgC5AFsAf/8bAA4BeQF3/zsBHwD5AEEBaQG7AHsCDv8ZABD/QAF1/34ABwJX/xMBhv8lAgUADv++AKQAPgFCABMC/f8NAEYAaAG2/77/4P8KAV8AiP8iAOgAoQAyAcgBzf/o/+L/7f9p/7f/ewAZAtX+IgITAjH/WgFp/+//JwBv/w8BSQDUAJH+7gEvAZ4BBwCBAE8A8v+P//j/VQCC/+EA3wD1APj/VgAKAL0AKgE8AE0BMAGMAAUAGAOcAEAA1/8MAnwA5P8OAB//DQFt/5EA5//wAdcAPP97AZwAJwDDALQBBP+H/5gBmgCLAOD/TP9QAl4AQQHNANIBMAAKAJz/ZgDw/kAADP/MAOAAhf+9Ab8AEv/P/h8B9wCZ/iABdABa/4gAIAEAAG8AowBK/4sBfQB7/5b/TQE/AV7/DwFbANgAvP+9AND+VwGN/1T/fv8WAa4A0AB8Aa0A4v+4AIwA0v+/AD8BUwCv/zYAkwH0/wICugB8AGEAJQAyAJf/WP/L/tr/hwEj/kIBMABbAm4AhADgAJD/HAGA/y4Cyf7dANT/GQK5/isA5AEN/zUANv9zAmsAZwCw/m8BRQCh/0//rgEaAO//eAFzAJn/igDn/xMBb/9JAZkAEgEZAWQABADmAN3+2wADAbL/2v9SAKkAIQBIAcT+r/9oAB4BHf7JALcBz/9D/zsAkAECAckAjgA9/y8AAgKq/pkAcwA9/9oAav/eAQn/YgDe/x4AvP/dAc//4AAWAXIABQDR/5ACRf48AWD/rwBCACAA+QAV/54ABQGk/wEA7f/rAMkA6P8aAOL/KgHB/8H/agHs/47/GQCtAJgBH/8mAbYB5ABLAMkA3QG2/uUAcQAgALr/sf/lAq7+YgFOAC0ADgAZAAQABACkAAQBzAAVAIwAbf+6Aen+yAD+ACMAUQGJ/7EC5P8IAfT/ZQASACoBMQAXAFYBbwARARn/EgJa/zMBPwB2Ac0AtQCrAJP/2AKt/wUB1v9qAYv+h/9pAC4ALgFM/5P/MwGYAKb/pf9EALkARP9fAKQAFwEIAXkAYQG5/pYAsAEWAPIA+f+PACYA+AF+AGUBWgCgAIsArAE/Aaj/igA2//QAGQBkAJQAsAH4APH+cwKd/5H/QQALAdz/FADUAccAwgBUAGYBWABG/2X+QQGtAY0A//8GAM4B8f48Abn+dQA6ANz+Z/8IATn/pv+Y/9gAqf+kAcEAgQHs/sUAZ//c/tgB1f8/ADkAGwOO/lMB3gBC/yIA0QBk//cAR//M/8/+wgFAAMf/yQAKAej/yP9YAcn/vwBjASAAlgB4Aun/w//x/w4BK/85/0ECGP6AAKkAP/9u/zADwP4Y/8IBlvxr/00A/f3U/xT+fAFV/g8Bivu1Aff++ASV/Q7+9ACV/ysAFf1f/1n/SQNwAOn/ZAAnACMB3f+Q//f9tAIb/c7/3QAF/ysDLvuNBeH7ZwKf/G8CwvqDAfH/bf6v/7f+iQDH/usAF/7G/f//AQGp/9z/pP7X/j/+S/+u/oz/nP4P/lgCQf+6BT/9fgHw/hQCGfza/Xz+pP1lAV3/MQLS/0ABVv8q//QBn/5J/WX+mgH6/EoCVv45AU7+FgBh/d7+GwBv/Mz/yP1HAbr7VwLU/TH/mP7q/+n+EgEm/vn/dv15AGIAIwAWApP9GAAV/6UBX/2G/qL/Bf2fAO39aQGtAIEBIP8gBMf9CQJ9/nz+O/3L/mD/Hv3DApD8NQIm/z8BIgG6AbL+bf4a/2j+tP5r/pcD6f7Z/UcDa/5iAqX8UgIk/l//1P6a/DoAeP1RAeL+Sf5q/kIACv/5ABb/xP3/AKL9TQAP/scCKPunAcL7Cv+P/Mn/Wf++//sAlv2RBCT9BQHv+XkA6Pw2Aa3+//tpAkr7dgEx/uD/YAGb/R8Ch/2+/4z8EwHY/ZT+wv+G/KsANvzVAOb9mv+9Arj9HAEk/soA/gCF/30Bgf8xALcA4/+E/Mj8PQB8/rv+HQI+AVEB6f3lAGv8u/8o/jH9Vv2v/mH8DQAX/RcAOQCAAV3/j/8mAFP9YAF3/ZIAEf/x/tL+Sf/U/PwCMf0EAOr9CABKAYP+6QR2/W8Bvf7cAQ/8SgK1/uT9YgCG/QwCEf26BRP7FgGw/hQAlfyy/pQAV/oeA179KQLL/sD+PAEK/QUApvwwAvn/vfw+AYf+4ACpAUX/Of77/wz8zgAS/8v9av7fAir/AABR/2v9jf1M/vL+lP7t/7v+eQIn/XkBBf6HA2D/TQDA/Z3/R/6R/bb/rfyGAdP9qgFBAdn9iwJ//pYAaPvqAeT+7gBr/pX/g/7l/Yn/mgBsAOD/Wf6sASkAN/9Z/7cA5P8q/x0A7fwW/3z9NgCo+mADyfzmAfD9VgC7/qb9PQBb/p4AUP1oANP/of+R/tP9JP+F/WoA6v3c//L+x//a/o4CLAF4AQECPgDV/Q3/NP/V/yL+9AC3/on9FwGS/jQB3PwfARj9Yv8b/j3+l/4wADf+t/8H/x7/Bf4SAH39R/8MAfH7fwBGAf78bwCK/fYAwfkpAWj8nf+Q/ev/8v4D/3ECa/3KAmP8FAPS/uUBAv4gAU78Pv/A/uT+dvsFAnf//vvk/8AAyQPB+aMC9v3dAer77/+n/+/5Bf8B/lMCUf51A9gAwwBv/2T/PAA1/dP/d/6m/xX9oP5Z/0QAmQGhAIr+AAFUANr96f67/ZD98f1q/u7/TAIi/oQAxPyP/3gDDf7NAMX+qQEy/Jf+QgFk/L0B3P2GAHr+cwIqAC8AQgC+/qP/+ADp/pn9k/4p/f0Ax/5pAfL9df/g/IUAEgJE/9H+xf2UALH+MAOj/B0CGf29/Uj/7v0iArz81QISAQgBxABe/3QAYP0S/nMAI/5zANv9KAFY/33/CP+m/23/7P47AD3/U/5H/goARP49Aof+1ACV/0j+Yv99/98B6v4+AFUA2v2o/lL/YwG7/vMB2v6t/z8CUPxwAAL89f8E/MwBFQACAf7/zwJMAGUAg/0SAMT8HP4SARP/AwJf/jwCQP/yAP/+p/6YARj8+wBW/oD/bP+oAVYB4f6R/g//Tf1G/kX9p/0g/wcCnfyEAKf/gAE9AR/9MgP1+sUFsPmuAZz/d//f/Nr+BAK6+iIDw/waBHL7XAGM/iL/2P2d/n8Bhv3p/fT+YABt/MYBS/50/tL+qv++AAH+3/9cANQA8f/9AE0AwACC/378lQDS+00BhP64AZX/BgGH/gr+0v4XAIX9uP5q/8ABOAI2/2YAUAD8/gQAT/6O/vkAxP/1AF0A9vx7ASb/eACC/rf/AAIp/JkCWP2dAxT6GgN4/NUCgPs5BO39OQBi/xwAMwEq/gYCkf1S/4f/mAHN/ST+OQIl/cP/6/4B/jMAsf01/rgBgv/v/isAwP++/638OgGPAID/evx8AJAAVv42/OMBl/xI/739SwRR/tL7tQDt/mIBdvt7/5v+uAEI/agDmfyn/0H8yAFyAJH8YgFB/ggBk/wHAvz8OACjAI3/ZANO/hwB7PoyAzP76gSV+h0Dff4DAHAAX/pqA3X7fwGm+9cCDf4C/zj/3f1QAKb8CAKx+5v/Yv+p+/EAyv7T/sn/cv2x//3/qf0HAIr99QAY/VcC/P0eAHwEofz0ASX9xADY/F0BHgBe/94ByAA8AN39ngBR/SoAN/92/RX/v/89ABj/aQEX/aABbP24AVr9Vf/IACr+9gKj/uUBOP4bARABY/4H/sn+eQIf/W0B8v2bAFr9Uf/O/sP8RwWp+5QBKgCQ/j3/Kf9QADv9dwHrABAA//0f/9gBL/wSAz/6FwJf/YYBgv95/dsAgfvdAhgDk/z2/gL/Sv/J/Bv+lv8b+jADEP6LApf/ygFi/rkADgDB/xQArQQx/+//wP6y/nYBAf+YAbr9Yf9TAJD9Z/4xACQD1CWwJjYlhScRJkUmHScQJkomZSbQJsskoidGJYwm8CMiJ3gmaiU1JuUlFCdBJiMmrSSIJfEl7CVwJhwlGSaCJtgmMiUpJ3QmDSbwJa4kCSfGJNIm3yQ1J9YlVSdBJSkmjyaRJj4mNyYFJu4lxia/JsAlnCVuJkUmpCY8JlImVSZLJvwlVCZsJnAlOSYzJMEmOiWZJiUlWSe4JgIncSbTJV0mZyXQJfAlcCY8JoQlyiYwJ30mqyWTJoIlAiaFJWAmHSbYJj8mIyYyJ/MlsSaYJXUnpSTkJkAm3CUpJrAm8CWUJjsmUyZAJicmHSbhJAwnfybUJZ8luibBJjsm7iYPJuwmviUCJsEltCZyJOMmLSWUJngm4ibtJjMmwyZNJewm2yRcJqElFib+JMImkCaVJiMnOyY/JtckeSb+Jc0ksyZgJUcnXyUsJ3AmlyZsJ6cl3CZ5JeMlTCaoJiEmNyaSJasmNifaJaAmvSXRJiwlXydSJhEoMiaTJw4mHiYKJtol6ybbJH8nLyUTKF4mGidSJX0mAyiOJUwnpyUzJuol2SX5JsElGCdeJvsmkSWOJl4mGCZdJ4IlLicSJtMmcyb1JLcmCiV4JjMm0iUiJuclCiYFJlYm+CYaJ9omLSZKJscmUyWaJY4lXCZzJSsncSZOJx0nriYYJqgmziXtJuYl2CXtJZsmAiYDJsUmvSW1JpklUiacJpEm7CVsJ18lyCYNJi0nRiY8JY8mLSTJJjAlASacJYEn8SS7JuwmCCakJk0lwybeI8UniyUsJn8mUCekJtkl/Cd1JbwmAyVyJoUm7CXBJuIlGSeTJUom0iZrJuwmyiXHJY4mIybwJUQnkSVXJmInxCZqJawmNiYeJuAmxCaZJuAl+yW8JZcmvyVwJ8IlxCaXJU4m9yWrJrklcyaUJmYm1yZ0JTInRiXFJXYmTyWmJs0lcycYJXQmByZgJl4m4CaKJjEmTyWlJTgmiyZHJfklXCZYJrcl+SVOJl0mGSfrJd0mAyaeJ8oktCfCJdEm7CXZJr0mNiZmJsgl3SaHJVcmbya4JoEmhCbEJpclvSY0JqcmhSahJs4ldyZ1Jf0kDSaOJlomViZwJsomjCVvJu4m4SV0JlIl7yaUJckmRyarJnsmnSbcJcom9CW+JksmZibkJf4mZSa3JYonfiZ1JeEmQiakJo0loiedJVwnEya9JsolkCZtJn8lSidoJWonQSVzJq8lHyanJeQnWSaUJnQmrydgJTwmgyfuJaMljCQLKFIlvyZ9JUcnDCZJJqonDCZcJuYk2yZyJMIl6iVgJmMm/SXKJhAmwSYCJhEnUiZOJq8lZyVpJm8mYyWjJuMmaSbBJscm4yZ8Jv0lGyW5JtQlFicUJpgksSbtJWkmiCWFJ9cmVSWgJnYl3SblJdYmLSXrJU8m5CUOJhgmsiWIJsAm5CbxJi8mBiZ4JdcmWSY4J0glliWVJiImoSY4Jn8m1iS9J54lICf4Js8lRSbCJKYm9ySLJbElnSV9Jj4moSbNJvwlByfGJeAm/iXiJT0m0iVlJqQm1yWtJiYmLSaeJgUmaiZbJWMmzyX+JQQneibyJbklICbvJf8loiZ7JmAmHSYcJiIlUCfWJS0lGSfMJTwn5yUwJxwlVyYGJu0lACU+JuglPCYVJu4mTCagJTEmjyWwJmclASYqJjwmHSYrJv8nmSWlJgAm7iUTJqglwiZ2JlgmuyaaJp8m6iWHJlklaSfHJSkm3iWFJdwmcCWxJxckNCj6JBMmBCbvJoYm0iXHJ78kdCfJJDQnciVwJowmqSaXJtElAycqJzAmniUjJ54l1yaUJswm3iYaJrkmXybuJSkl2iUcJvkliiVoJq0nySU0J8YljSaAJc8leiWeJu4mqCb3JdEmjSZxJl4lJCVAJsYlZiYRJkgmWCaKJiIm/iXHJUUmhSfJJRwmLyaOJpolaiXkJgIl6CaYJIMoFiVRJ0Aloye5JN8l7CVGJiQmgSWgJtMlzSaSJi8mpSWvJnsmdSWOJuYlUCa1JmwmxCZhJvcl3iXMJnsm7SURJlgnlSUlJiMmYCfqJbkl5yZHJ5IliCcWJvImeyR6JpInzyVxJoQlyCcpJvMl8SU2J0AkvyavJv8mzCT5JYInfCWCJhEm4SYxJTsmOSYVJvUlCiWCJvwlFSiUJOYnSyTKJ6IkeiZRJiQm/ifPJLonpiWwJ2Ml9CZQJqEmGCfjJTcniiV1J9wlFyaCJ08lOCarJncmhCb8JVQmsyayJQsmCia0JkElECeuJfAk0yclJU4nzyXOJq8lBCYvJmElaCZ3JhYnvyUaJ6wlDiYRJ8cmSybRJVwmCCbQJkglRCc9JSkn8yXgJc4m3STAJlQlayZnJVUmvCYWJ0UmFyb4JlclsyY6JpkmWya1JuImNyQQJyUm/iXFJmAmTyYHJq4mpiV2JTcmhSZvJqUl6ibCJIAnqyXDJj4myCYdJ/klDieGJMkkHScpJmomySbGJ9omryYZJ5UkuybMJBkmeSWuJmMlfyZoJr8lJCXvJuklVCaqJgQmzyVjJfgm8CVsJjAnTyZsJnQl,"[""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b6"",""y_b6"",""y_b6"",""y_b0"",""y_b7"",""y_b5"",""y_b7"",""y_b7"",""y_b0"",""y_b7"",""y_b7"",""y_b0"",""y_b6"",""y_b6"",""y_b6"",""y_b7"",""y_b6"",""y_b7"",""y_b7"",""y_b7"",""y_b4"",""y_b7"",""y_b6"",""y_b6"",""y_b6"",""y_b6"",""y_b7""]",rotor,unbalance,15_hz,loaded,0.2,"{""axis_nrmse"":[1.0,1.0,1.0],""state_error_probability"":0.75}"
> ep_1e629e5114f8fee70c,/wGV/sAAcgAO/8wApAA4AKj+YADIATn/yP+9AFn/hwGp/v8AVf8kAfT/Jf8GAcn//f9zAC0Bmv4HAD4ApQF1/l8AdADq/6oAI/+xAKX/XQEA/y8AOwAZALj/LQGNACL+VAEYAAsBUf5TAbb/SgA/AEv/PgDPAFsAIP+zAHj/XwCJ/1oC2P1nAHUAhAD7/zn/UgH+/oMBKf+w/8QA7QDw/n0ASACz/8T/ZwFTABT+owGl/5IAw/9RAO7/TQDzAED+6gDQAL3/Wf9WAfL+8v+GAHsBWv5/AGcA0/+oANf/7f/z/3EBhP58/14BKwAw/wMBZADN/kkAqAFW/5z/rABp/8IAFQDz/6z/FwFkAO796wFMAH//MQAcATD/eP/VANAA1v4JAT//RQC/AMX/EgDM/6YBY/7h//wBvv5FAJYAZQA1/4D//wEf/0UAfADe/lYB4P/A/5kA1f8tAaP9VAK0/zT/sgBDAG8At/6yAC4BSf+mAGv/zf/nAKL/TAAhAEwA/v+9/sYCQf4WAKIAvQBt//n+wAG2/04A4//8/5D/bwHx/uIAz/9nAOL+DgEmARf+6QC9AF8Aiv7MAKQAx/9xAKf/GQDU/3ABQ/7tAQL/KwCE/xcCNf+z/qYBnwAj/2b/aQEh/7AB5v7cAPP+oQF1/63/twFR/l0AxwAVAQP+ZQC4AXP/b/9/ABUAEQA7AWP+JgEI/8sBQf7yAbj/av6hAZ4Atf+T/twBbwBv/87/yAAm/7YBMv+//3cAAwBYAH7/2wH8/T8A5gFq/2j/dP8qAvL+XwCS/4IA6P8FAdv+yAD5/wIAEgDAAGgAGv7dAYoAcP8v/xkB1wAa/1sAwP+2ABAANQC4/5kA3/+v/9EAOwCN/zX/CwJJ//T/Jv9UAvn+JQDD/18AZACX/5AAsv+aAHT/SQDiAOH/XP9/ACwBOv9c//8A4wDH/pEA3v/bAH//FwDPAGn//ADA/p8Bl//p/7n/OQHj/3T/4/+9ASr/2v9NAHUAPgAs//sAsP+AAKr/q/9oAfX+OQA+ALoAoP8y/6kB4f+F/0MAIACeAJP/t//3ALr/mwAI/3IBlv+c/5wAkwC3/53/WgAdAfL+jACo/wQBBABW/3YAUwA9AIb/cwCiAAn/VgAlAYD/FgDR/1ABQ/8IAPj/FgAYAUX/1//dACUALABP/7oBpP4eANIAiQDs/k4ASQCfAFz/ZwCl/9YAdQDH/rkAJABpAED/VAHH/x7/1gAJAT//nP95AMYAov87AL7/QQCnABYAD/8wAX7/oABk/4sBjP5lANcAXABF//7/7wDm/ycAm/92AAoAvAAx/2wAMAD5/ysAUgBJABP/BwGeALn/cP+KAMAAT/+QAHH/LwEz/zIB3v4OAXz/cQBJAEgAsP+m/zsB+v99/3//jQFh/3YArP+hAOj/DQC8AAn/HgFF/8IAAwDu//n/0/8mAWT/z/9cAO4ALf/qAC//bgHC/jEBqP/p/78AKv9VAVf/NQDh/8kAIgA8/0IA4QCF/3UAt/8lALYAC/9HARz/2QCX/woAJgGR/h0Bvv/fAFX/IQCJACYA0/95AGj/HAGR/+T/1wCN/64AEP+RAVT/t/9HAar/OQBy/94A1/9hAPn/DQAIAOMAHv96AMEAbv9AACoA7ACW/iwBfACe/73/YgBDAOH/awCZ/1MAXAAWAEv/RQEKACr/iQBxANn/Wv+qAXn/tP/h/zkB9f4AAYn/KgBwAN//MwB7/6UB3/4BAMAA4f91/9cAgQDF/yr/NgHn/9P/hABc/xEBnf8ZABwAdwDdAJT+MgHe/8T/4v81Acf/4P96/5cB6v6MAB8A4P/eAOf+CgFT/ycBjf/U/6kACQBU/yMB6v9VAP/+7QBwAOz+0gC8/54Aqv+w/9QAof/tADf/mAAhAL3/1v8nAdb/0P+c/1UBOP+1/ycBo/+YAOj+CAGG/zUBXP9CAA4AowD6/hYBLgAKAHT/BAHG/5X/SQDyAMf/7v+l/5EAOAByAET/nwAbAOj/0P/FACAAIv8ZAdb/JQA0/3sBxv9nAN/+uwDk/0EB5/6ZAO3/QgCC/8oA8//b/9n/MwHx/nQAqv9WAdj/6P9S/5kA0wDD/9z/GgChACL/QgFl/wQBx/6lARD/vgDp/j4BXABBAPH+KwDaAFgAmv81ANj/SADL/9YAff+GAI7/DwFN/y8ASP/AAeb/u/8c/40AHwE4/0cBZP6fAe3+IwFV/+4ABf9DAX//zQAt/pQBuAC8/8n/bP8NAQoASgAaAPv+nwEJ/7oALADe/7v/AAEHAKP/4v6XAjb/7P8NADX/0gH7/oYBTv5DAfX/4v8xAP0AMf6sAcz/sQAQ/mQBLAEH/2oAbf8mAOkA+P8cAGP/9wDE/7z/RAFH/1H/4QGD/+j/jf6TApf/m/+WAAv/5wAdAJoAQP+3AM7/QgCo/4YB4P1nAXEA6v8M/1wAbwFU/ysA9/+y/2cAzABl/wsAcwDO/x0ADgACASX+CwItAGf/Rv9DAaYAOv9pAEUAev+mALwADf8KAaL/HgC4/xQBsv///ioCaf/5/ocA/P0v/5L+bf5L/ln/0v4b/pL9xQCM/l39q/9r/i3/2v2p/3X+5P0zAPf8KgBr/ScAIf3OAEr9Uv75/q3/of6p/M0AEf0RAH39xP+G/UH/w/4M/kb/2P2+/0T9NAF7+7AAvP1hAFb9hP7y/zb9QgDe/OIAWfw3Aff7RAHG++kA6fx0AK39vf0vAGv9GgFL+5MBsvwyAIX9Cv8n/xr+W//g/b//K/2KAP/80gDe+70AHP1NAPz97v1uAKr8SgFV+/oBSPxlAC39KQAO/b//8f3E/7/9Yv5w/6n9EAGx+z0BzPxbAHX9Vv4MAGD9rv+n/d//dv1j/9z+Ov/U/NwAs/yCAMj9lf7n//38VAFN+2sBvf3k/nf+x/6W/iT+Lv9b/1b9D/8f/3X9mQDo/BQAYP2O/8/+pPxEAvX7kv+B/ur+Xf7r/YQAuf3X/UIAR/1B/3f/Uv04AJD8LAE3/Mz/EQDV+ycBAf0PALT8DwAG/9T9Kf+F/i3+EP9h/7f9x/9T/WUA/vu8ARX9yP1QAFL9DABG/JcBtvyM/4j+e/4M/k//+f5x/W0Auvx6AFP8hQKV+lwBLf0KADf9U//f/5j8RwGu+zUB+vsTAsf7PABW/uH9kP8E/s0AGvvRAcn8agAv/DIB1PwPAKX+i/3B/4H8eALp+YIDKvqiAcv88QAj/eb9pAAj/YD/Pf3LAC78jwEI/DwAKf1oAHf+lf1KAcz6BQKm/AQBtPufAMn+zf3h/nz+U/+S/bwAnfsLAX38sAGf+2wB1/xO/lcAu/14/zb8vQEX/cf+zP5f/mr/+f2x/7v8AQAD/pf/hP1yAGD8CwA3/+X9yv6F/e0BR/tGAWP8lwCl/aP/H/4R/rf/7/1y/0f+8f5A/YEABP6l/tv9sP+N/z788QAg/IUBIPwRAQj9I/8n/wb+AwBM/Xf/Iv0pAaP8nP9Y/UQBMvz+/0P+9P5W/2P9qAA3/IgAv/2m/4j+kP3P/9T9FwAb/WH/gf7Q/xn92P+W/S8AIf2l/wH/Mv1wAMX8VQH++z4Azf36/gL/uf19/+H+D/48/8L94f/H/bH+df/q/QT/S/5U/8L+Lv17ANf9LP82/nn+vf+0/X//if0f/yL/yP1h/37+cv7D/kb+BwDm/Gr/Pf8l/oj+3f6q/i3/c/2CAGH8vwCq/W3+of/V/YP/+Px8AF/9U/5n/xv/mP0D/6f+GP/4/Tz/mf5k/tr/Of19/1r+Ef8f/o/+2v9j/CUAS/5C/8/8EwBc/sT+Xf4W/1j+l/6q/zv98P+8/bj/U/0cAAH+5/3U/3n+pf5z/ZIAif1h/839Kv86/o/+Yf85/SkAL/0vAPb8kQDH/Ob/7P69/vv9gf54AIr8gwDN/PYAoPxAACv+OP6c/3v9UAAf/TsAn/zVAMv9Xf93/NkA8/2W/jL/t/3DAHv7PQKh+wgB/vyi/9L+mP0LAH39awCH/fv+rP3nABL95f93/TcA3P3P/T8BgPu0AWr7BQId/J7/m/67/kP/nf3g/oH+n/+g/bX/Iv1HAV77JgH+/WD+S/+G/V8BDfs6AYn9W//B/g/+af/j/eb/W/1t/1z+4v/D+2gCsvtHAD79nwC7/WP9GgHI/CMAPf0FAJP9cP94/v/9P//u/gP+4P0FAXD8o/9y/gsA3Pze/pEANPy1AMD8HAHp+1YBSvw2ABP+WP85/R8AHP8B/bH/cP55/0j8lAHi/Oj+Of7S/1f+7/1IAJr8vgBG/Zj/T/0mAED+z/wSASf98f4+/XABDvz//5D94wDT+zYByPze/4r+5P1//4f9lAEf++oAJf4d/4L9RwA1/vP9vf6s/y7+Bv6d/x/9NwDA/ev+cv79/oz/LvyTAe38Sf/n/aAAz/xs/33+FADN/K//W/5p/tX/G/0hAD/9CwH2+7QA8v3j/ov99wBB/eX+/v1mAFH9Nf8C//z9rv/t/bT+ov4g/5j+X/2BAKX9Z/4f/z3/4v1H/or/fv48/sT+3f5b/r3/OP3Q/+P9WQDb+y8BQf2X/xD9+wAX/dP+n/6v/4v9Lf8r/kr/gf6i/in+Cv+K/4H9sP40/77+Rv34/4j+ef50/ekA2/waAF39RABd/S0AyPwCAGH+jP/U/Pv/P/4E/7/9eQDZ/WT+5/7M/zP9uf+t/SIAe/2N/0D9xv9Y/2r9NP9//ub/PfxHATD9uv8z/EsCs/sAAS38QgH7/A4AlP3z/bYAaf0T/xL+bv/R/Wf+IQCh/V/+sP5ZAHv8VgCb/NwBlfs2AbP7ggAK/279m//p/PgAIPyTAez88P8C/FYCwfvqAPD7MgEX/sf9BwBg/NABmPz4/7L95P6t/mj+RP/8/aH+5v3dAO37IwFi+08DxPr+AMf86f/h/hT+5v/x/DAASv2iALH87wBM++0B3PzD/wL9vP8PAML73ACS/PoA2fzbAJf9Y/5Q/zX+jf+m/cP//ft4AkP7OQG3+7YCFfyN/9r9Of+v/of+h//9/A0AbP2KAAf97f+V/Sz/5P8g/UL//f2nAOj8+P7p/t7+6v51/iz/Q/06ADP9lABn/CEB9PsTAZ39uf47/kv9miSAJpElVyZOJl8l7iUlJsEm6ySaJeYmFyWXJqQl4CXiJfwliCbCJCYnXSVNJlAlziahJJcmayboJYIlqSVgJ7EkKif7JEwmAiZwJo0lpCXTJnQlgSZsJdEmICTMJyUlNyYxJUUmZSYbJQ8noiQRJy4lBidWJKYnpSSCJwEl5ib6JO0lMye6JPomWCSjJ5kkACcZJQkmUCacJfoldyXMJgglFSfTJBMnSiSYJyclfCZvJc4leSYSJQknSCTBJ5YkCCfoJBQnBCXRJrklUyZWJQwmgSZMJaUmaSRxJ8gkASf1JGYmzCY3JZAmSiWoJgwltyanJfQlUiX/Js4kOCf9JCEmQCYvJfYmRCTVJ70kRCbeJecl+yXTJVsmxyW4JWMm+yWAJfcmiCT5JkMlbCbIJWslhSfPI20njSXJJQAm/yVoJlol9CWcJuYkzCbiJQ8lJyfXJCknqCT7JvElviTfJ3Mk7yZxJbUmlCXAJRUm1iXaJZUm2SVLJd8mASX4Js0kmCeYJFUm+ybGJNkmHSU9J8ckziZyJd0lQCaCJpclnCX7JpEkUifFJKcnlyM7KLMkiSZuJXkm6CVBJR4nTSTAJ7EkdicDJJgnRSW5JdwmViV+JnokIihBJBEn3yRrJ8EkHicSJXolNyfMJJ4niyPqKCQjbyjDJLsm7iSUJrUm8yTFJlQl7ibkJIQn1CO2J18lgCZoJakl8ib2I4coHyTtJs8kYicyJeYlVSbAJWgmliW/JkUkOChkJFUnVSR9J5wkoSapJs0kdyaaJUgnsCSNJsYl8iVdJo8lQSZRJWUn3CSpJloloibTJConlSVHJY4mpSXkJisknSdwJGYnECU/Jj8lYSY3JkQlgCaWJSImsCXlJgwlLibsJVImuCUTJWcnjyTbJ0YkMCfGJOkmoCWIJZsmGyV4Jnsl9iZ9JBEnWCXjJnokPScmJUomGSYaJcYm3iQxJ9IkXibLJZglniZ1JXImIiXPJn4lUybxJNAmKSXvJuwkjCbTJYkl4SatJG0ndiQ4J1IlXCbiJbclTSbcJZglNyZ2JZEmmSX5JSImpSVBJrMlICbxJZ4l8SbsJGAmtiUcJjAmgCU8JqMliCb/JV0lZSboJfElGia0JWwmMCXlJp4lriUoJgomkyU/Jmwlpib9JHMn3SQZJnEmXiVFJlwl1CYxJW0mbyZ3JcIliybWJS0m4yUYJrQlGSZNJhAlpib7JfAl5SUKJlQmDiVoJ0AlOialJekmUyVmJtIlCibKJXUm9SUgJe0mgyVUJoElmSZZJR0mpSY1JR0m7yWWJh0lmiZ1JUUmGiY0Ju4lYSU4J/Qk2iY6Je0m3CT4Jn8loCUAJkYmMyYLJSknzyQCJ/wk1SYUJTYmiiYSJeQmBCWzJgslSyfVJEMmvSU2J/okOiYgJj0l8ia2JKEn4yPLJ88kgybmJbklciZKJbsmECV2JuMllCajJPUmHiWGJo0l8yWjJlwkISj9I7UnmCTZJqQlCyYSJnglmCYOJgomXSW8JvIkWyeAJI0nxSRQJmUmHiUSJ24kqifpJI8mnyWpJXQmsCUtJnMlpSZvJZAm3CSqJ+4jwCfjJG0mbSUEJrgmwyTlJgIlpCZ4JYAmZiU0JjEmvSXvJegloSafJDknRCUiJmslkSYeJu4kOifIJDMnzCRJJ1skbycIJXgmeyWuJmUlmCXoJmUlQCZQJSknkiTzJq0lUSaBJQomeCb5JG4nkiTsJmklqyZhJe0lGSe7JAAnqCW9JokkZyfkJCcngCSeJ2MkLCeHJcolvSYzJcsmOCTNJ/IkVCa0JYomMCVFJhIm9CXZJc4luiYsJSEn+SRuJh4mzyUtJg0lhid2JPomcSWrJsQkIycyJZomFSUHJ7Ul7CWgJu4kKycOJdcmnCRTJ/skZiaoJbom1iSNJr8lRyZ5JVIm7SXMJUMmhyUcJl4m2CXwJYkl9yb6JIom2iUGJoslSiYiJqQlLSYhJhEmwCUpJi0l9SZuJWUm4CR/J9IksyZyJb0mBCW/JrwlMCZdJawmbiWiJlElEybXJa4mnyWcJVwmMiamJQ4mmiZJJUYm6SWtJtEk+CYRJbwmUiVPJgwlQidPJRQmeyX4JkwlTyZyJZ0m2CSuJo4lZCYZJekmMCX1JtwkZiaPJfYmaCWAJaEmfCVlJiIlViduJAMnJiVKJ0AkWifAJG4n0SR1Jh4lyyanJtEkXybFJRsmISblJX4mBSW2JtYlQSbeJFMn0yS2J9UjiCelJLAnbCVdJcsmMiUyJ/AkFyeiJOAmMCWVJ+cjsCeEJLEn7yTLJZomEiWlJ1wkkSavJUgmPibCJR8m0yUwJuYlyyZ8JM4nGCR/KFMj1yfIJAwn0yWTJS4mZCXlJkklwCbDJFgnSyQ+KAok9CZrJbImMiZSJLAnrCRuJ+YknSbIJI4mISazJUgmcyXOJvgkJih1IxgoKCQCKN4jBieNJXIm9CXpJQkmOCVRJ+Ek7Sa9JCknOSVOJkkmtST9JmolzSalJLgm0CX7Jd0l9CXTJcAl3iapJE8npSSHJyMkySfAJB0mNyYzJvom,"[""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b6"",""y_b6"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b6"",""y_b6"",""y_b6"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b6"",""y_b7"",""y_b7"",""y_b6"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7"",""y_b7""]",rotor,unbalance,15_hz,loaded,0.2,"{""axis_nrmse"":[1.0,1.0,1.0],""state_error_probability"":0.75}"
> <!-- SAMPLE_SUBMISSION_PREVIEW_END -->

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Hidden-Rebuild Canonicalization Policy Induction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ah2kfzkb59sbv7182qkgyp58bpsr7
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: large-scale
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Independent rebuilds of the same software release can differ even when their executable meaning is unchanged. Archive timestamps, entry order, file modes, manifest fields, compression choices, embedded paths, service-file order, SBOM metadata, and build-tool strings can all prevent byte-for-byte verification. A naive repair can make several rebuilds identical by rewriting everything to an arbitrary value or by deleting payloads, but that destroys provenance or semantics.
> Your task is to train a model from scratch that induces a minimal, artifact-specific canonicalization policy.
> For every case, you receive:
> A real Apache-2.0 JAR release from Maven Central.
> A heterogeneous graph derived from that artifact.
> Three public rebuild variants represented as field-state arrays.
> Public divergence witnesses.
> Candidate canonicalization actions with matched wrong-parameter, wrong-scope, wrong-mechanism, public-only, and unsafe alternatives.
> Semantic-probe nodes and masks.
> You must select three sets of IDs:
> actions: canonicalization actions that should be executed on unseen rebuilds.
> causes: public divergence witnesses that identify persistent root causes.
> frontier: artifact entries at the earliest affected scope of those persistent causes.
> The selected actions are executed by the private grader on three hidden counterfactual rebuilds. A strong policy must make those hidden rebuilds agree, restore the canonical provenance values derived from the real artifact, preserve semantic payloads, and avoid unnecessary edits.
> This is a structured policy-induction task in the From Scratch category. It is not ordinary row classification, regression, retrieval, or fixed rule execution. The number of candidate actions and target IDs changes from case to case.
> Why the task is difficult
> Public disagreement is not sufficient evidence that a repair is needed. Some public divergences are transient and do not recur in the hidden rebuilds. Persistent and transient mechanisms use overlapping recurrence patterns and structurally matched candidate families.
> For a single plausible scope, the graph may contain:
> The correct canonical action.
> Several actions with the same opcode and scope but incorrect canonical values.
> An action with the correct opcode but the wrong entry scope.
> An action using a different mechanism.
> A public-only action that repairs an observed difference but has no hidden benefit.
> An unsafe shortcut that improves superficial agreement by damaging semantic content.
> Test projects are disjoint from training projects. The test set therefore measures generalization to unseen artifact families rather than memorization of a release or repository.
> Dataset origin
> The artifact content is real public open-source data. The dataset includes 34 pinned Apache-2.0 JAR releases downloaded from Maven Central. Exact project names, versions, URLs, licenses, and split assignments are recorded in source_manifest.json.
> The rebuild variants, intervention states, candidate counterfactual actions, persistent-cause labels, and hidden grader contexts are synthetic and were generated from scratch. Generation is deterministic with seed 20260802. The complete generator and configuration are included in the raw dataset. No private build logs, credentials, personal data, or copied benchmark labels are used.
> Prepared public files
> train.csv
> Each row is a labeled training case with these columns:
> case_id string): unique case identifier such as RBC-00086A56D61CC44E9C2B.
> graph_path string): relative path to the case NPZ graph under the public directory.
> artifact_id string): pinned artifact identifier and version.
> artifact_path string): relative path to the source JAR under upstream_artifacts/.
> source_url string): exact Maven Central URL for the source artifact.
> target_json string): canonical target policy with the three keys actions, causes, and frontier.
> test.csv
> The test file has the same columns as train.csv except that target_json is absent. It contains no private state, case weight, split label, persistent-cause count, or hidden rebuild answer.
> sample_submission.csv
> case_id string): one ID for every test case.
> policy_json string): a valid policy object. The sample uses empty lists.
> graphs/*.npz
> There is one heterogeneous graph per case. Array row positions define the IDs used in a submission.
> node_features float32, shape [N, 128]): normalized node features. Channels encode node kind, field or action kind, entry-path byte histograms, entry-content byte histograms, archive statistics, public disagreement statistics, scope information, parameter sketches, and small deterministic noise channels.
> node_kind uint8, shape [N]): 0 for a public rebuild variant, 1 for an artifact entry, 2 for a divergence witness, 3 for a candidate action, and 4 for a semantic probe.
> edge_index int32, shape [2, R]): directed graph edges.
> edge_type uint8, shape [R]): relation code aligned with edge_index.
> action_nodes int32, shape [A]): graph-node indices for candidate actions. Row i is submission ID A followed by three zero-padded digits, for example row 7 is A007.
> divergence_nodes int32, shape [D]): graph-node indices for public divergence witnesses. Row i is ID D followed by three zero-padded digits.
> entry_nodes int32, shape [B]): graph-node indices for artifact entries. Row i is ID E followed by four zero-padded digits.
> variant_nodes int32, shape [3]): graph-node indices for the three public rebuild variants.
> semantic_probe_nodes int32, shape [P]): graph-node indices for semantic-retention probes.
> action_descriptor float32, shape [A, 8]): action opcode, owner entry, execution stage, number of updated fields, field kind, global-scope flag, and two canonical-parameter sketches.
> divergence_descriptor float32, shape [D, 8]): field index, field kind, owner entry, field weight, three public values, and the number of distinct public values.
> entry_descriptor float32, shape [B, 10]): uncompressed size, compressed size, CRC token, compression type, file mode, ZIP flags, extra-field length, comment length, extension code, and path length.
> public_field_values int64, shape [3, F]): field values for the three public rebuild variants.
> field_owner int16, shape [F]): entry-row owner for each field.
> field_kind uint8, shape [F]): field-kind opcode for each field.
> field_weight float32, shape [F]): importance weight used by executable evaluation.
> semantic_mask uint8, shape [F]): 1 for semantic payload fields and 0 otherwise.
> The edge relation codes are:
> 0: public variant to artifact entry; 1 is the reverse relation.
> 2: artifact entry to divergence witness; 3 is the reverse relation.
> 4: divergence witness to plausible action; 5 is the reverse relation.
> 6: action to owned entry; 7 is the reverse relation.
> 8: action to semantic probe; 9 is the reverse relation.
> 10: entry to the next archive entry; 11 is the reverse relation.
> 12: public variant to divergence witness; 13 is the reverse relation.
> upstream_artifacts/*.jar
> These are the 34 pinned real Apache-2.0 release artifacts. They are supplied so a model may learn from artifact structure and canonical metadata without internet access. Deterministic parsing may be used as preprocessing, but final policy selection must be produced by a genuinely trained model.
> Supporting files
> action_catalog.json: the 20 action opcodes, their field kinds, execution stages, and safety flags.
> graph_schema.json: machine-readable NPZ array definitions and ID rules.
> task_schema.json: submission keys, list limits, metric name, and score direction.
> source_manifest.json: exact Maven Central source URLs, licenses, projects, artifact IDs, and split assignments.
> DATASET_DESCRIPTION.md: dataset provenance and raw-file documentation.
> LICENSE.md: Apache License 2.0 notice and upstream attribution.
> Action vocabulary
> Safe candidate opcodes cover these canonicalization mechanisms:
> FIX_ENTRY_TIME
> SORT_ARCHIVE_ENTRIES
> NORMALIZE_FILE_MODE
> STRIP_ZIP_EXTRA
> CLEAR_ARCHIVE_COMMENT
> REMOVE_MANIFEST_VOLATILE
> SORT_MANIFEST_LIST
> SORT_PROPERTIES
> NORMALIZE_EMBEDDED_PATH
> NORMALIZE_LINE_ENDINGS
> NORMALIZE_SBOM_TIMESTAMP
> NORMALIZE_SBOM_SERIAL
> SORT_SERVICE_LINES
> REWRITE_CREATED_BY
> NORMALIZE_COMPRESSION
> DROP_VOLATILE_GIT_PROPERTIES
> NORMALIZE_DEBUG_PATH
> NORMALIZE_ZIP_FLAGS
> Two unsafe shortcut opcodes are included as hard negatives:
> DROP_ENTRY_PAYLOAD
> ZERO_CLASS_CONTENT
> Unsafe actions can make values look more uniform while reducing semantic retention.
> Target policy grammar
> Each target_json and policy_json must decode to one JSON object with exactly these keys:
> {"actions":["A016","A025"],"causes":["D003","D022"],"frontier":["E0000","E0025"]}
> Rules:
> actions is a list of at most 16 unique IDs matching A plus three digits.
> causes is a list of at most 20 unique IDs matching D plus three digits.
> frontier is a list of at most 24 unique IDs matching E plus four digits.
> Every numeric index must be within the corresponding case array.
> JSON key order and list order do not affect scoring.
> Duplicate IDs, unknown keys, incorrect prefixes, out-of-range indices, excessive list length, malformed JSON, or a non-object value make that row invalid.
> For each persistent mechanism, the cause target is its designated lowest-index visible divergence witness. Its frontier target is the lowest-index affected artifact entry. Repeated frontier entries are included only once.
> Train and test design
> The public data contains 1,008 training cases and 252 test cases from 34 artifacts. The test-to-train row ratio is exactly 25 percent.
> Training uses 28 artifacts from Apache projects represented only in training.
> Test uses 6 artifacts from Apache Groovy, Kafka, Flink, Calcite, Iceberg, and Parquet.
> No project appears in both partitions.
> Training cases contain 2 to 5 persistent causes.
> Test cases contain 5 to 8 persistent causes and a larger public-only distractor burden.
> Candidate lists are shuffled deterministically, so candidate row position is not a label.
> Use artifact- or project-disjoint validation. A random row split leaks artifact family characteristics across folds and will overstate generalization.
> Declared distribution shift
> The private partition intentionally tests both family generalization and policy-cardinality extrapolation. These aggregate split statistics are disclosed so participants do not have to infer the expected policy size from leaderboard feedback:
> Training targets contain 2 to 5 actions, with mean 3.4464; test targets contain 5 to 8 actions, with mean 6.4008.
> Cause-list cardinality follows the same ranges and means as action-list cardinality.
> Training frontier targets have mean 2.8194; test frontier targets have mean 4.1944.
> Public training graphs contain a mean of 51.0099 candidate actions; public test graphs contain a mean of 111.2579, a 2.1811x increase.
> Of the 1,613 action slots in private targets, 397, or 24.6125%, use a local action index that never occurs in any training target.
> Action, cause, and frontier IDs are case-local row indices, not global semantic labels. An unseen local index therefore does not introduce a new opcode; it requires a model that scores variable-size candidate sets instead of memorizing frequently selected row positions. Solvers should validate on held-out artifacts and use a count-aware set decoder capable of extrapolating beyond training target cardinalities.
> Evaluation
> The leaderboard uses the Hidden-Rebuild Canonical Policy Score. It is a case-weighted composite in the range from 0 to 1, and higher is better.
> Step 1: Execute the submitted policy
> The grader applies the selected actions, in canonical action-ID order, to three private hidden rebuild states. Candidate effects are private. An action can update one field, an entry scope, or a global scope.
> An audited field is a hidden field whose baseline values are not identical across all hidden rebuilds. All weighted quality fractions below are computed only over audited fields.
> Step 2: Hidden rebuild quality
> For each audited field:
> Agreement succeeds when all patched hidden rebuilds have the same value.
> Provenance fidelity succeeds when every patched hidden rebuild equals the canonical value derived from the pinned real artifact.
> Exact audited success is 1 only when every audited field has both agreement and provenance fidelity; otherwise it is 0.
> Weighted fractions use the public field_weight values.
> RebuildQuality = 0.15 x Agreement
> + 0.70 x ProvenanceFidelity
> + 0.15 x ExactAuditedSuccess
> Let Q0 be RebuildQuality before applying any submitted action and let Qp be the quality after applying the policy.
> NormalizedGain = clip((Qp - Q0) / (1 - Q0), 0, 1)
> If Q0 is already numerically equal to 1, NormalizedGain falls back to action-set F1.
> The action budget discourages broad policies:
> ActionBudget = min(1, 1.5 x TrueActionCount / max(1, PredictedActionCount))
> Semantic retention is the unweighted fraction of hidden semantic field values that still equal their canonical semantic references after action execution.
> PolicyGain = NormalizedGain x ActionBudget x SemanticRetention
> This design distinguishes genuine canonicalization from two shortcuts. Choosing many actions is budget-penalized, and forcing rebuilds to agree on an arbitrary or destructive value receives little provenance or semantic credit.
> Step 3: Structured set components
> For any predicted set P and target set T:
> SetF1(P,T) = 1                                      when P and T are both empty
> SetF1(P,T) = 0                                      when exactly one is empty
> SetF1(P,T) = 2 x |P intersection T| / (|P| + |T|) otherwise
> The grader computes ActionF1, CauseF1, and FrontierF1 with this definition.
> CardinalityMatch = min(PredictedActionCount, TrueActionCount)
> / max(1, max(PredictedActionCount, TrueActionCount))
> Minimality = ActionF1 x CardinalityMatch
> ExactPolicy is 1 when all three normalized ID sets exactly match the answer, and 0 otherwise. ValidSyntax is 1 for a valid policy object and 0 for an invalid row.
> Step 4: Per-case score
> CaseScore = 0.75 x PolicyGain
> + 0.08 x ActionF1
> + 0.04 x CauseF1
> + 0.03 x FrontierF1
> + 0.04 x Minimality
> + 0.05 x ExactPolicy
> + 0.01 x ValidSyntax
> The component weights sum to 1.00. PolicyGain is deliberately dominant because the primary task is executable hidden-rebuild repair. Exact matching is a high standard, but it is not the dominant component; meaningful partial canonicalization receives graded credit.
> Step 5: Case weights and leaderboard score
> Each private case weight is defined by:
> CaseWeight = 1
> + 0.06 x PersistentCauseCount
> + 0.001 x PublicDivergenceCount
> + 0.02
> The final 0.02 is the fixed private-test shift term applied equally to all test cases. Harder cases with more persistent causes and more public divergence evidence therefore receive modestly greater weight.
> LeaderboardScore = sum(CaseWeight x CaseScore) / sum(CaseWeight)
> The theoretical minimum is 0 and the theoretical maximum is 1. A perfect submission scores 1 exactly.
> Public score calibration
> The following creator-side measurements provide landmarks for interpreting the score scale. They are aggregate measurements, not case answers:
> Empty valid policy: 0.0100. This is the do-nothing floor produced by syntax credit alone.
> Fixed first-five-action diagnostic: 0.0590.
> Public graph-degree diagnostic: 0.1011.
> Exhaustively tuned training-target frequency-table diagnostic: 0.1206. This creator-side sweep evaluates all 8,925 global output-cardinality triples allowed by the grammar; its best setting emits 12 actions, 8 causes, and 2 frontier IDs.
> Six-epoch relation-aware GNN trained from scratch: 0.2065.
> Oracle with 25 percent of true actions and no witnesses: 0.2631.
> Oracle with 50 percent of true actions and no witnesses: 0.4283.
> Oracle with all but one true action and complete witnesses: 0.7240.
> Oracle with every true action and no witnesses: 0.8800.
> Perfect policy: 1.0000.
> The fixed-ID, graph-degree, and frequency-table measurements are non-compliant diagnostic baselines because the From Scratch rules require learned policy decisions. They are published only to expose the low-skill floor. The compliant reference GNN is separated from the strongest swept frequency diagnostic by 0.0859, while the higher oracle bands leave substantial headroom for stronger learned systems.
> Submission format
> Submit one CSV with exactly two columns in this exact order:
> case_id
> policy_json
> Every test case_id must appear exactly once. Row order does not matter.
> Example:
> case_id,policy_json
> RBC-00086A56D61CC44E9C2B,"{""actions"":[""A016"",""A025""],""causes"":[""D003"",""D022""],""frontier"":[""E0000"",""E0025""]}"
> Submission-level errors raise a clear grading error:
> Missing or additional CSV columns.
> Missing, duplicate, or unknown case_id values.
> Missing policy_json cells.
> A structurally complete submission can still contain an invalid policy row. That row receives a case score of 0 without crashing the grader.
> From Scratch rules
> This challenge must be solved with genuine model training performed inside the submitted script.
> Train only on the supplied public training data.
> Start all learned model weights from scratch.
> Do not use pretrained models, pretrained embeddings, knowledge distillation teachers, external datasets, or self-generated training data.
> Do not use TF-IDF, IDF-like weighting, n-gram or Markov lookup systems, nearest-neighbor target copying, hardcoded policy templates, or a pure rule-based solver.
> Deterministic parsing of supplied NPZ and JAR files is allowed as preprocessing, but a trained model must make the policy decisions.
> Do not pseudo-label, fit, calibrate, or adapt using the aggregate test set. Test processing must be ordinary per-case or per-batch inference.
> Training, inference, and submission generation must occur in one independent end-to-end script.
> Runtime contract
> The platform invokes the solution as:
> python3 [solution.py](http://solution.py) <public_dir> <submission_out>
> Read all data from the first positional path and write the final CSV exactly to the second positional path. Create the output directory when needed.
> The environment provides an NVIDIA A10G. The absolute runtime limit is 90 minutes. Use a training guard near 75 to 80 minutes so inference and CSV validation can finish safely.
> Research and real-world context
> The benchmark is motivated by reproducible-build and software-supply-chain research. Prior work studies taxonomies of unreproducibility and evaluates fixed canonicalization tools. This challenge instead asks a learned system to induce a minimal artifact-specific policy from a public rebuild ensemble and tests that policy by execution on hidden counterfactual rebuilds.
> Relevant background:
> Canonicalization for Unreproducible Builds in Java: https://arxiv.org/abs/2504.21679
> Reproducible Builds and software-supply-chain integrity: https://arxiv.org/abs/2104.06020
> SLSA Build provenance requirements: https://slsa.dev/spec/v1.2/build-track-basics
> Reproducible Builds guidance: https://reproducible-builds.org/docs/plans/

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Hidden Finger Contact Graph Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78xa6svfqj36r8rdkjcyg2p18bp28r
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Dexterous manipulation depends on where contact occurs across the fingers, not only on how much total force each hand applies. A low-bandwidth wearable system may retain wrist motion and whole-hand pressure while losing the detailed readings from individual tactile cells. Your objective is to reconstruct that missing finger-level contact structure.
> Each row contains a one-second window from a real bimanual tabletop-manipulation recording. You receive coarsened left-wrist, right-wrist, and head inertial changes; normalized total tactile load for each hand; and five opaque context codes. You must predict a fixed graph describing how long each of ten fingers was active and how fifteen predefined finger pairs were temporally related.
> In plain language: for every test window, predict the state of all ten finger nodes and all fifteen contact-relation edges.
> This is a From Scratch graph-learning challenge. All learned encoders, embeddings, and prediction heads must be initialized from random weights and trained only with the provided files. Pretrained tactile, motion, robotics, language, vision, or general-purpose representation models are not permitted.
> The measurements come from a commercially licensed real-world sensor study of people performing tabletop manipulation activities. The recording system used tactile gloves with five fixed finger patches per hand, sixteen tactile cells per patch, six inertial channels at each wrist, and nine inertial channels at the head. The competition files contain only curated windows and opaque context codes; source recording names, links, timestamps, episode identifiers, annotation text, and detailed test tactile measurements are not provided.
> What You Must Predict
> The graph has ten nodes, L0 through L4 for the left glove and R0 through R4 for the right glove. Finger numbers preserve the source glove's fixed sensor order.
> For one finger at one frame, contact is active when the sum of its sixteen tactile values is at least 256. A node target summarizes the number of active frames in the 30-frame window:
> 0: active for 0 to 2 frames
> 1: active for 3 to 13 frames
> 2: active for 14 to 25 frames
> 3: active for 26 to 30 frames
> Fifteen fixed graph edges connect adjacent fingers within each glove, corresponding fingers across gloves, and two endpoint cross-links. Each edge has one state:
> 0: sparse or separated activity
> 1: the first named node leads the second by at least two frames
> 2: the second named node leads the first by at least two frames
> 3: coupled activity, with contact-frame intersection over union of at least 0.45
> For a non-coupled pair, the lead direction is determined by the difference between the mean active-frame positions. Pairs with fewer than four union-active frames, insufficient activity on either node, or no qualifying lead are assigned state 0.
> The scored edges are:
> L0-L1, L1-L2, L2-L3, L3-L4, R0-R1, R1-R2, R2-R3, R3-R4, L0-R0, L1-R1, L2-R2, L3-R3, L4-R4, L0-R4, and L4-R0.
> Why It Is Difficult
> The detailed 160-taxel measurements are withheld from test inputs. The two load streams reveal only normalized whole-hand pressure, so different finger arrangements can produce similar visible values. Inertial inputs contain only per-window normalized, quantized changes. Six independently selected frames in every visible stream are unavailable and use the marker 9. Wrist motion, head motion, manipulation context, contact duration, and cross-hand coordination each provide incomplete evidence. A useful model must combine those clues across time.
> All windows from one recording episode remain in the same split. Test rows therefore come from eighteen complete episodes absent from training. Fresh identifiers and shuffled row order remove source position and temporal-order shortcuts.
> Dataset
> train.csv
> Contains 6,682 training windows with the input columns and all 25 graph targets.
> test.csv
> Contains 2,456 windows from 18 held-out episodes. It contains only id and the ten input columns.
> sample_submission.csv
> Contains the required 2,456 identifiers and all target columns initialized to zero.
> metadata.json
> Records window construction, graph nodes and edges, state values, split counts, and code cardinalities.
> Input Columns
> id - string - fresh identifier for one window.
> left_wrist_stream - string - 180 space-separated integers representing 30 frames by 6 left-wrist change channels.
> right_wrist_stream - string - 180 space-separated integers representing 30 frames by 6 right-wrist change channels.
> head_imu_stream - string - 270 space-separated integers representing 30 frames by 9 head-inertial change channels.
> left_total_load_stream - string - 30 space-separated normalized whole-left-hand load levels.
> right_total_load_stream - string - 30 space-separated normalized whole-right-hand load levels.
> anchor_code - string - opaque code for the interaction phase; 6 possible values.
> grasp_code - string - opaque code for the recorded grasp family; 5 possible values.
> hand_code - string - opaque code for hand participation; 4 possible values.
> object_code - string - opaque code for the manipulated object; 89 possible values.
> action_code - string - opaque code for the high-level recorded action; 214 possible values.
> The code-to-meaning maps are intentionally not published. Their useful associations must be learned from training examples, and the codes do not preserve lexical ordering.
> For each inertial channel, consecutive-frame differences are divided by that window's 75th-percentile absolute change, multiplied by 2, rounded, and clipped to -3 through 3. Each load stream is divided by its own window maximum and quantized to levels 0 through 7. Exactly six frame positions per stream are replaced by the unavailable marker 9; all channels at a masked inertial frame use that marker. Masking is deterministic and independent across the five streams.
> Target Columns
> Every target is an integer in {0, 1, 2, 3}.
> Node columns: node_L0, node_L1, node_L2, node_L3, node_L4, node_R0, node_R1, node_R2, node_R3, node_R4.
> Edge columns: edge_L0_L1, edge_L1_L2, edge_L2_L3, edge_L3_L4, edge_R0_R1, edge_R1_R2, edge_R2_R3, edge_R3_R4, edge_L0_R0, edge_L1_R1, edge_L2_R2, edge_L3_R3, edge_L4_R4, edge_L0_R4, edge_L4_R0.
> Evaluation
> The Contact Graph Recovery Score combines balanced node-state recovery, balanced edge-state recovery, and row-level topology overlap.
> For target column j, let S_j be the states that occur in the hidden answers. For state s, its recall is
> R(j,s) = correctly predicted rows whose true state is s / rows whose true state is s.
> The node term is
> N = mean over the 10 node columns of [mean over s in S_j of R(j,s)].
> The edge term is
> E = mean over the 15 edge columns of [mean over s in S_j of R(j,s)].
> For each row i, form the set of nonzero predicted node states and the corresponding true set. Let their Jaccard similarity be J_node(i). Do the same for nonzero edge states to obtain J_edge(i). When both compared sets are empty, their Jaccard similarity is 1.
> T = mean over rows i of [0.5 × J_node(i) + 0.5 × J_edge(i)].
> The final score is
> Score = 100 × (0.45 × N + 0.35 × E + 0.20 × T).
> The score ranges from 0 to 100, and higher is better. The state-balanced terms prevent common inactive states from dominating the evaluation while the topology term provides continuous partial credit for recovering the correct active subgraph.
> Submission Format
> Submit one CSV with exactly 26 columns in the order shown by sample_submission.csv: id, followed by the ten node columns, followed by the fifteen edge columns. Every prediction must be an integer from 0 through 3. The file must contain every test identifier exactly once.
> Example using real test identifiers:
> id,node_L0,node_L1,node_L2,node_L3,node_L4,node_R0,node_R1,node_R2,node_R3,node_R4,edge_L0_L1,edge_L1_L2,edge_L2_L3,edge_L3_L4,edge_R0_R1,edge_R1_R2,edge_R2_R3,edge_R3_R4,edge_L0_R0,edge_L1_R1,edge_L2_R2,edge_L3_R3,edge_L4_R4,edge_L0_R4,edge_L4_R0
> FG10006171,3,1,0,0,2,3,2,0,1,3,1,0,0,2,3,0,0,1,3,0,0,2,3,1,2
> FG10002691,0,0,0,1,1,2,0,0,2,3,0,0,1,3,0,0,0,2,0,0,0,1,3,0,1
> Malformed values, missing values, non-integers, infinities, and states outside 0 through 3 receive worst-case treatment. Extra columns, missing rows, duplicate identifiers, unknown identifiers, and reordered columns are rejected.
> Rules
> Train only on the supplied competition files.
> Initialize every learned representation and prediction component from scratch.
> Do not use pretrained encoders, pretrained embeddings, foundation-model features, or external datasets.
> Do not attempt to identify or match the originating recordings, recover removed annotations, or reconstruct hidden tactile arrays through external data.
> Hand-engineered signal processing and original neural architectures are permitted.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Mosquito Wingbeat Dictionary Learning

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bx1csvyhn2nnc128dvpcseh8bvzk7
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> This is a from-scratch audio representation challenge. Your task is to submit one compact dictionary of 16 acoustic motif atoms that can reconstruct hidden mosquito wingbeat spectrogram patches.
> In plain terms: learn a small reusable set of mosquito wingbeat shapes. The same dictionary must work for clear lab recordings, field-like noisy recordings, short bursts, rare species conditions, and different recording-device responses.
> The source corpus is HumBugDB, a large acoustic mosquito dataset released on Zenodo. HumBugDB contains mosquito and background audio recordings collected across several countries, recording devices, and capture contexts, including controlled insect-culture recordings and noisier field or semi-field conditions. The full source audio archive is multi-gigabyte. The uploaded raw dataset package contains the official HumBugDB metadata table and source audit, and the preparation script uses those metadata distributions to generate compact benchmark patches.
> The public patch_code values are deterministic metadata-conditioned wingbeat sketches. They are not raw WAV clips and they are not direct crops that can be looked up by filename. Each patch is a 24 by 32 quantized log-spectral window generated from source attributes such as species, country, capture context, device type, feeding/sex hints, recording length, and signal-quality condition. Train and hidden evaluation patches use disjoint source groups.
> This is not mosquito species classification, audio tagging, or event detection. The submitted object is a learned model artifact: a compact acoustic dictionary.
> Dataset files
> train.csv has 3,900 public motif rows.
> id: string. Public motif row ID.
> patch_code: string. A 24 by 32 quantized log-spectral patch encoded with 64 printable symbols.
> patch_shape: string. Always 24x32.
> source_country: string. Country-level source context from the official metadata.
> capture_context: string. Broad source context, such as culture, field, or another source location type.
> device_group: string. Recording device group from the official metadata.
> mosquito_attribute_hint: string. Coarse feeding and sex hints when available.
> snr_tier: string. Public signal-quality tier: low, mid, or high.
> test.csv has 24 artifact rows.
> id: string. Private evaluation fold ID.
> artifact_type: string. Always wingbeat_dictionary.
> required_atoms: integer. Always 16.
> patch_shape: string. Always 24x32.
> fold_hint: string. Structural fold label such as eval_fold_03. It only identifies which private patch bundle is scored by that row. It does not encode a species, site, device, or target value.
> sample_submission.csv has:
> id: string. Test fold ID.
> predicted_dictionary: string. A valid JSON dictionary containing 16 all-zero atoms. It is intentionally useless and scores 0.
> Patch decoding
> The alphabet is:
> 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_
> Each character maps to an integer from 0 to 63. Decode patch_code row-major into a 24 by 32 matrix and divide by 63.
> Interpretation:
> Rows are coarse frequency bins.
> Columns are short time frames.
> Larger values mean stronger log-spectral energy.
> The patch represents a short wingbeat-like acoustic motif, not a full audio recording.
> How benchmark patches are generated
> The generator is deterministic and uses no network access during preparation.
> For each selected source metadata row, the generator:
> assigns the row to train or hidden evaluation by stable source group;
> chooses one private motif family;
> creates a base wingbeat spectral prototype with harmonic structure and time modulation;
> conditions that prototype on source metadata such as species, country, device type, capture context, recording length, feeding state, and sex hints;
> applies deterministic family-specific transformations such as noise, short-burst gating, device-response tilt, or rare-species spectral shift;
> quantizes the resulting 24 by 32 log-spectral patch into patch_code.
> Source groups are built from species, country, place, device type, and location type. Public training rows and hidden evaluation rows use disjoint source groups.
> Private motif families
> Private evaluation patches are drawn from six motif families. These labels are not present in solver-facing test rows, but they are used inside the metric for robust scoring.
> culture_clear: clean culture-style wingbeat motifs with relatively high SNR.
> field_noisy: noisier field-like motifs with stronger background variation.
> fed_shift: motifs whose spectral energy is shifted according to feeding-state metadata.
> device_response: motifs with device-dependent frequency-response tilt.
> rare_species: long-tail species-conditioned motifs with shifted harmonic structure.
> short_burst: truncated or gated motifs where only a short wingbeat burst is visible.
> Each private fold contains a mixture of these families. The family-balanced metric prevents a dictionary from fitting only clear or common motifs.
> Output format
> Submit the same best dictionary in every test row.
> Each predicted_dictionary value must be a JSON list of exactly 16 atom objects. Each object must have exactly:
> id: string. One of A00, A01, ..., A15.
> code: string. Exactly 768 alphabet characters encoding one 24 by 32 atom.
> Example with shortened codes:
> [{"id":"A00","code":"000...000"},{"id":"A01","code":"123...abc"}]
> The real submission must include all 16 atoms and full-length 768-character codes. Atom order inside the JSON list does not matter because the grader aligns by id.
> Evaluation
> Malformed dictionaries score 0 for that artifact row. Structural CSV errors such as missing IDs, duplicate IDs, unknown IDs, extra columns, wrong row count, or wrong column order are rejected.
> For each private patch, the grader compares the patch with the best submitted atom under small time shifts of -1, 0, and +1 frame. For each shifted atom, the grader fits one scalar gain clipped to [0.70, 1.35] and computes mean squared error.
> BestMSE = minimum shifted gain-fitted MSE over submitted atoms
> Each private case stores three calibration errors:
> BaselineMSE: MSE from an all-zero dictionary.
> AnchorMSE: MSE from a fixed pooled k-means anchor trained on the public patches. This represents the straightforward public-only dictionary-learning shortcut.
> ReferenceMSE: MSE from the private reference dictionary.
> Case score:
> RawCase = clip((AnchorMSE - BestMSE) / (AnchorMSE - ReferenceMSE), 0, 1)
> CaseScore = RawCase * RawCase
> A submitted dictionary receives positive credit only when it beats the pooled k-means anchor on that private case. Squaring prevents a barely-above-anchor dictionary from receiving most of the score.
> For each artifact row:
> overall_mean = mean(CaseScore over private patches in that fold)
> worst_family_mean = minimum mean CaseScore over the six private motif families in that fold
> bottom_20_mean = mean of the lowest-scoring 20% of private patches in that fold
> low_snr_mean = mean CaseScore over private patches whose snr_tier is low
> If a fold has no low-SNR private patches, low_snr_mean is set to bottom_20_mean.
> Artifact score:
> artifact_score =
> 0.50 * overall_mean
> + 0.20 * worst_family_mean
> + 0.20 * bottom_20_mean
> + 0.10 * low_snr_mean
> Final score:
> final_score = mean(artifact_score over submitted artifact rows)
> Scores are finite and bounded in [0, 1]. The sample scores 0. The private reference dictionary scores 1.
> Participants can evaluate dictionary reconstruction on public training patches, but cannot exactly compute the hidden score without the private fold payloads.
> Submission format
> Submit exactly two columns in this order:
> id: string. Test fold ID from test.csv.
> predicted_dictionary: string. JSON list containing the 16 atom objects.
> CSV example with shortened JSON:
> id,predicted_dictionary
> F000,"[{""id"":""A00"",""code"":""000...000""},{""id"":""A01"",""code"":""123...abc""}]"
> Use normal CSV quote escaping. Do not submit separate model files, WAV files, NumPy arrays, Python code, or natural-language explanations.
> What not to use
> Do not use source recording IDs, filenames, row order, or fixed artifact IDs. They are absent or structural.
> Do not optimize only clear culture-style recordings. The hidden score includes rare-species, field-noise, short-burst, low-SNR, and device-shift cases.
> Do not submit a species classifier. Species labels are only source context; they are not the target.
> Do not assume fold_hint carries target information. It only identifies a platform scoring fold.
> Recommended solution approach
> A basic solution can learn dictionary atoms from public patch_code matrices. Stronger solutions should consider metadata-balanced sampling, low-SNR denoising, robust clustering, nonnegative matrix factorization, autoencoders, or tail-aware dictionary learning. The A10G budget is intended for representation-learning approaches that train and validate multiple candidate dictionaries.
> Benchmark boundary
> Prior mosquito-acoustics tasks usually detect mosquito events or classify mosquito species from audio. This benchmark instead asks for a compact executable motif dictionary and scores reconstruction quality on private source-disjoint wingbeat patches. It is a robust audio representation-learning and codebook-design task, not ordinary acoustic classification or event detection.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Formula Context Span Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75km8zkeq74by9bbmsg343mh8bqykf
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> You are given the left and right context around a missing span from a math-heavy document. Your task is to reconstruct the missing span and report a small amount of formula structure: how many displayed or inline formula groups it contains and which math symbols appear in it.
> The rows are drawn from real mathematical web documents. This is a pretraining-style challenge: the training file provides many examples of local mathematical prose, notation, and discourse patterns. Good solutions should learn the style of formula-bearing text from the provided corpus rather than relying on generic language completion.
> Dataset
> The public files are:
> train.csv: labeled context-gap examples.
> test.csv: held-out examples without answer_json.
> sample_submission.csv: valid format example.
> Columns in train.csv:
> id (string): row identifier.
> left_context (string): text before the missing span.
> right_context (string): text after the missing span.
> gap_word_count_hint (integer): approximate number of words in the missing span.
> answer_format_json (JSON string): required output schema.
> answer_json (JSON string): target missing-span record.
> Columns in test.csv:
> id (string): row identifier.
> left_context (string): text before the missing span.
> right_context (string): text after the missing span.
> gap_word_count_hint (integer): approximate missing-span word count.
> answer_format_json (JSON string): required output schema.
> The required answer_json has:
> missing_span (string): reconstructed missing text.
> formula_count_bin (string): one, two, or many. Every row in this task has at least one displayed or inline formula group in the missing span, so zero is not a valid value. Use many for three or more formula groups.
> symbol_tokens (array of strings): short math symbols or command tokens appearing in the missing span.
> Submission
> Submit a CSV with exactly:
> id (string)
> answer_json (JSON string)
> Example:
> id,answer_json
> owm_example_001,"{""missing_span"":""The polynomial is $$x^2+1$$, so the roots are complex."",""formula_count_bin"":""one"",""symbol_tokens"":[""x"",""^"",""+""]}"
> owm_example_002,"{""missing_span"":""By substituting $a=b$ above, we obtain the desired bound."",""formula_count_bin"":""one"",""symbol_tokens"":[""a"",""b"",""=""]}"
> Each test row must appear exactly once. Missing IDs, extra IDs, duplicate IDs, or wrong columns are rejected. Invalid JSON or invalid field values receive zero for that row.
> Evaluation
> The final score is the mean row score.
> For each row:
> span_score is duplicate-aware token F1 between normalized predicted and true missing_span.
> symbol_score is duplicate-aware F1 between predicted and true symbol_tokens.
> bin_score = 1 if formula_count_bin exactly matches the target, else 0.
> Text tokens are extracted from words, numbers, LaTeX command names, and math operators. For an F1 field:
> precision = matched_tokens / predicted_tokens
> recall = matched_tokens / true_tokens
> F1 = 2 * precision * recall / (precision + recall)
> If one side is empty and the other is not, F1 is 0.
> The row score is:
> row_score = 0.72 * span_score + 0.18 * symbol_score + 0.10 * bin_score
> Scores are clipped to [0, 1]; a perfect submission scores 1.0.
> What Not To Use
> Do not use external copies of the source math corpus.
> Do not search the web for held-out contexts or spans.
> Do not use pretrained language models, pretrained embeddings, hosted LLM APIs, or checkpoint-derived features.
> Do not hard-code test IDs or answer dictionaries.
> Do not manually annotate the test rows.
> Do not use internet access during solution execution.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Repository Boundary Echo Modeling

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f9729mm2gk4c3x69xf217518bqeq1
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Each row gives a compact two-sided neighborhood from an MIT-licensed software repository file. Infer the boundary record that belongs between the two sides: the exact local boundary text and the identifier-like echo tokens that appear in that text.
> The examples come from real repository material, including notebooks, scripts, JSON-like records, web assets, and documentation. This is a training-from-scratch task over software-text neighborhoods. Good solutions need to learn local syntax, indentation, markup, naming style, comments, and short-range file structure from the provided examples. The echo-token inventory is scored separately, so a fluent but identifier-poor answer receives limited credit.
> Dataset
> The public files are:
> train.csv: labeled repository-neighborhood examples.
> test.csv: held-out examples without answer_json.
> sample_submission.csv: valid format example.
> Columns in train.csv:
> id (string): anonymized row identifier.
> prompt (string): task instruction.
> neighborhood_json (JSON string): input neighborhood and row metadata.
> answer_format_json (JSON string): required output schema.
> answer_json (JSON string): target boundary record.
> Columns in test.csv are the same except answer_json is absent.
> neighborhood_json contains:
> before (string): text immediately before the boundary slot.
> after (string): text immediately after the boundary slot.
> source_kind (string): coarse source type, such as notebook, javascript, json, html, css, java, c, or documentation.
> license_family (string): source license family; every row is MIT.
> boundary_token_hint (integer): approximate number of whitespace-separated tokens in the target boundary text.
> The required answer_json contains:
> boundary_text (string): text that belongs in the boundary slot.
> echo_tokens (array of strings): identifier-like tokens that appear in boundary_text.
> Submission
> Submit a CSV with exactly:
> id (string)
> answer_json (JSON string)
> Example:
> id,answer_json
> code_11111111111111,"{""boundary_text"":""def load_config(path): return json.load(open(path))"",""echo_tokens"":[""load_config"",""path"",""json""]}"
> code_22222222222222,"{""boundary_text"":""The command writes output files into the build directory."",""echo_tokens"":[""command"",""output"",""build""]}"
> Every test row must appear exactly once. Missing IDs, extra IDs, duplicate IDs, or wrong columns are rejected. Invalid JSON or invalid row content receives zero for that row.
> Evaluation
> The final score is the mean row score.
> For each row:
> boundary_text_score is duplicate-aware token F1 between normalized predicted and true boundary_text.
> echo_score is duplicate-aware F1 between predicted and true echo_tokens.
> For either F1 field:
> precision = matched_items / total_predicted_items
> recall = matched_items / total_true_items
> F1 = 2 * precision * recall / (precision + recall)
> If one side is empty and the other is not, F1 is 0. If both sides are empty, F1 is 1.
> The row score is:
> row_score = 0.76 * boundary_text_score + 0.24 * echo_score
> Scores are clipped to [0, 1]; a perfect submission scores 1.0.
> What Not To Use
> Do not use external source-code corpora or external copies of this dataset.
> Do not search the web for held-out repository snippets.
> Do not use pretrained language models, code models, pretrained embeddings, hosted LLM APIs, or checkpoint-derived features.
> Do not hard-code test IDs or answer dictionaries.
> Do not manually annotate the test rows.
> Do not use internet access during solution execution.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Directional Sea-State System Estimation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79b5m0rd2jvkrd9g4m4fe9bd8bq93f
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> This is a from-scratch scientific modeling challenge built from real ocean buoy directional wave spectra. Each row gives 18 hours of anonymized frequency-by-time sea-state history. Your task is to estimate the three strongest wave systems that will dominate the next 6 hours.
> In plain terms: look at recent ocean-wave energy, direction, and spread patterns, then fill fixed prediction columns for the future dominant swell/wind-sea systems. A good model identifies each future system's frequency band, travel direction sector, energy tier, spectral width, and growth/fade trend.
> The public rows are not raw station tables. The preparation script aggregates source spectra into 24 frequency bands, mixes a nuisance source window, applies row-local direction rotation and spectral perturbations, and removes station IDs, timestamps, filenames, and raw frequency labels. Train and hidden test rows use disjoint buoy stations.
> This is not text generation, wave-height regression, weather classification, or ordinary scalar time-series forecasting. The submission is a fixed-column structured state estimate over future directional spectra.
> Dataset files
> train.csv contains:
> id: string. Unique training row ID.
> energy_history: string. A 36 by 24 quantized wave-energy history encoded with 64 printable symbols.
> direction_history: string. A 36 by 24 direction-sector history encoded with the same alphabet; only values 0 through 15 are meaningful.
> spread_history: string. A 36 by 24 directional-spread history encoded with 64 printable symbols.
> history_shape: string. Always 36x24.
> frequency_cards: JSON list. Row-local frequency-band aliases and period metadata.
> direction_sectors: string. Always 16.
> max_systems: integer. Always 3.
> target_p0_frequency, target_p1_frequency, target_p2_frequency: strings. Training-only future frequency aliases, such as F07.
> target_p0_direction, target_p1_direction, target_p2_direction: strings. Training-only future direction sectors, such as D12.
> target_p0_energy, target_p1_energy, target_p2_energy: strings. Training-only energy tiers, E0 through E3.
> target_p0_width, target_p1_width, target_p2_width: strings. Training-only spectral-width tiers, W0 through W2.
> target_p0_growth, target_p1_growth, target_p2_growth: strings. Training-only growth/fade tiers, G0 through G2.
> test.csv has the same public columns but omits all target_* columns.
> sample_submission.csv contains:
> id: string. Test row ID.
> p0_frequency, p1_frequency, p2_frequency: strings. Future frequency aliases to predict.
> p0_direction, p1_direction, p2_direction: strings. Future direction sectors to predict.
> p0_energy, p1_energy, p2_energy: strings. Future energy tiers to predict.
> p0_width, p1_width, p2_width: strings. Future width tiers to predict.
> p0_growth, p1_growth, p2_growth: strings. Future growth/fade tiers to predict.
> There are 6,000 training rows and 2,400 hidden test rows. Hidden rows are balanced across five private scenario families with 480 rows per family.
> Input field schemas
> energy_history, direction_history, and spread_history:
> Type: string.
> Length: 864 characters.
> Decoding alphabet: 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_.
> Decoding method: map each character to an integer from 0 to 63, then reshape row-major to 36 time steps by 24 frequency bands.
> Meaning: energy_history is normalized spectral energy; direction_history is a 16-sector mean direction; spread_history is a directional-spread proxy.
> frequency_cards is a JSON list of exactly 24 objects. Each object has:
> frequency: string. Row-local alias from F01 through F24.
> band_index: integer. Position of the frequency band in the history arrays.
> period_seconds: number. Approximate representative period for the band.
> band_type: string. One of long_swell, swell, wind_sea, or short_chop.
> Example frequency_cards item:
> {"frequency":"F07","band_index":6,"period_seconds":11.43,"band_type":"swell"}
> Output fields
> Submit fixed columns for exactly three ranked future wave systems. Rank p0 is the strongest future system, p1 is second strongest, and p2 is third strongest.
> For each rank, the allowed values are:
> p*_frequency: F01 through F24.
> p*_direction: D00 through D15.
> p*_energy: E0 through E3.
> p*_width: W0 through W2.
> p*_growth: G0 through G2, where lower means fading and higher means growing.
> Example row values:
> p0_frequency = F07
> p0_direction = D12
> p0_energy = E2
> p0_width = W1
> p0_growth = G2
> Evaluation
> Structurally invalid submission files are rejected. Structural errors include missing columns, extra columns, duplicate IDs, unknown IDs, missing IDs, wrong row count, or wrong column order.
> Malformed row-level predictions score 0 for that row instead of crashing the grader. Rows are aligned by id, not row order.
> For each ranked system:
> FrequencyScore =
> 1.00 if predicted frequency equals true frequency
> 0.10 if the predicted frequency band is adjacent to the true band
> 0.00 otherwise
> DirectionScore =
> 1.00 if predicted direction sector equals true sector
> 0.15 if circular sector distance is 1
> 0.00 otherwise
> TierScore =
> 1.00 if predicted tier equals true tier
> 0.05 if the tier differs by 1
> 0.00 otherwise
> For each rank:
> SystemScore =
> 0.40 * FrequencyScore
> + 0.34 * DirectionScore
> + 0.08 * EnergyTierScore
> + 0.04 * WidthTierScore
> + 0.04 * GrowthTierScore
> + 0.10 * FrequencyDirectionExact
> FrequencyDirectionExact is 1 when the frequency and direction are both exactly correct for that rank, else 0.
> RankedFDExact is the mean of FrequencyDirectionExact over p0, p1, and p2.
> SystemExact is 1 for a rank only when all five fields for that rank are exactly correct. MeanSystemExact is the mean of SystemExact over the three ranks.
> UnorderedFDF1 is an unordered soft F1 over the three frequency-direction pairs. A predicted pair receives matching credit 0.62 * FrequencyScore + 0.38 * DirectionScore against its best unused true pair.
> AllSystemsExact is 1 only when all fifteen prediction fields match the hidden answer exactly.
> The row score is:
> row_score =
> 0.40 * mean(SystemScore over p0,p1,p2)
> + 0.20 * RankedFDExact
> + 0.18 * MeanSystemExact
> + 0.12 * UnorderedFDF1
> + 0.10 * AllSystemsExact
> If AllSystemsExact is 1, row_score is exactly 1.
> The hidden set is balanced across five private families:
> long_swell_arrival
> crossing_seas
> windsea_growth
> fading_swell
> broadening_mix
> Family labels are not present in solver-facing files. They are used only for robust hidden scoring.
> Final score:
> overall_mean = mean(row_score over all hidden rows)
> worst_family_mean = minimum family mean over the five private families
> bottom_20_mean = mean(row_score over the lowest-scoring 20% of hidden rows)
> final_score =
> 0.66 * overall_mean
> + 0.22 * worst_family_mean
> + 0.12 * bottom_20_mean
> Scores are finite and bounded in [0, 1]. The sample submission scores 0. A perfect oracle scores 1.
> Submission format
> Submit a CSV with exactly these columns in this order:
> id: test row ID.
> p0_frequency
> p0_direction
> p0_energy
> p0_width
> p0_growth
> p1_frequency
> p1_direction
> p1_energy
> p1_width
> p1_growth
> p2_frequency
> p2_direction
> p2_energy
> p2_width
> p2_growth
> Example:
> id,p0_frequency,p0_direction,p0_energy,p0_width,p0_growth,p1_frequency,p1_direction,p1_energy,p1_width,p1_growth,p2_frequency,p2_direction,p2_energy,p2_width,p2_growth
> 0a12bc34de56f789,F07,D12,E2,W1,G2,F14,D03,E1,W0,G1,F03,D09,E1,W2,G0
> What not to use
> Do not use station IDs, years, timestamps, source filenames, row order, or fixed frequency meanings. These are absent from solver-facing rows or are row-local.
> Do not submit raw spectra, JSON, natural-language explanations, multiple alternatives, generated strings, or extra columns.
> Do not optimize only the strongest visible historical band. Hidden scoring includes crossing seas, fading systems, broadening systems, and long-swell arrivals.
> Do not assume public-source lookup can recover hidden targets. Public rows are transformed source-new spectral mixtures and hidden test stations are disjoint from train stations.
> Recommended solution approach
> A basic solution can decode the histories, locate recent spectral peaks, and extrapolate frequency-direction trends. Stronger solutions should train from-scratch temporal convolution, transformer-encoder, gradient-boosted, or ensemble models that jointly estimate rank, frequency, direction, width, energy, and trend under station-disjoint validation.
> Benchmark boundary
> Nearest prior work includes wave-height forecasting, ocean-wave spectral partitioning algorithms, and buoy quality-control studies. Those tasks usually output continuous wave parameters, classify sea states, or partition a single observed spectrum. This benchmark instead asks solvers to estimate a fixed-column future sea-state system table from anonymized spectral histories with row-local frequency aliases, direction rotations, source-station-disjoint splits, mixed nuisance spectra, and robust family/tail scoring.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Joint Cardiac-Pulmonary Audio Classification

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72ht639md2fdnr1rxqan001x8bnqz6
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> This is a from-scratch raw-audio modelling task. Each six-second digital-stethoscope clip contains a newly
> constructed heart-plus-lung mixture. From the labelled training clips, learn to produce one coherent joint
> probability distribution over ten cardiac acoustic states and four pulmonary acoustic phenotypes for every
> test clip. Pretrained or foundation models and outside data are prohibited.
> An answer is a 10 × 4 posterior surface, not two unrelated classifications. Its 40 cells express joint mass
> for every cardiac-pulmonary pairing. Summing the surface along either axis produces the corresponding organ
> marginal, so the two predictions cannot contradict one another. The grader reads this single surface at exact,
> organ, physiologic-family, adventitious-presence, and cross-organ resolutions. Cardiac, pulmonary, and joint
> skill are all mandatory.
> Human-biology grounding
> Chest auscultation contains overlapping activity from the cardiovascular and respiratory systems. Rhythms,
> murmurs, added heart sounds, continuous airway sounds, crackles, and pleural friction can coexist in one
> stethoscope channel.
> The construction corpus combines cardiac and pulmonary research recordings whose annotations can be mapped
> to a medically honest shared set of acoustic phenotypes. Recordings with simultaneous continuous and
> discontinuous pulmonary events are excluded rather than forced into a single target. These targets describe
> audible phenotypes, not diagnoses or medical advice.
> Every served clip is a fresh transformed mixture. Recording- and participant/session-level source groups are
> kept disjoint between construction and held-out data. Every one of the 801 globally unique source WAVs is
> exercised at least once. The linked dataset includes the attribution, label mapping, global deduplication, and
> construction audit needed to verify that process.
> What you are given
> public/
> train_audio/              1,200 labelled WAV clips
> test_audio/                 480 unlabelled WAV clips
> train_labels.csv          1,200 training rows
> test_index.csv              480 test rows
> sample_submission.csv    19,200 long-form probability rows
> Audio — public/train_audio/ and public/test_audio/ (1,680 files)
> All files are mono, 4,000 Hz, 16-bit PCM, exactly 24,000 samples, and 6.0 seconds long.
> Each file is named <clip_id>.wav; the keyed opaque identifier carries no state information.
> Each split is exactly balanced over all 40 cardiac-pulmonary target cells: 30 training and 12 test clips per
> cell.
> Every clip independently crops and mildly time-warps its two sources, normalises energy, applies a shared
> smooth device-response perturbation, varies relative organ gain, adds faint noise and a circular shift,
> softly limits, and freshly encodes the result. No served WAV is a byte-copy of a deposited recording.
> public/train_labels.csv (1,200 rows)
> clip_id — string. Names public/train_audio/<clip_id>.wav.
> heart_code — string. One of h00 through h09.
> lung_code — string. One of l00 through l03.
> Cardiac code register
> h00 — atrioventricular block.
> h01 — atrial fibrillation.
> h02 — early systolic murmur.
> h03 — late diastolic murmur.
> h04 — late systolic murmur.
> h05 — mid systolic murmur.
> h06 — normal heart sound.
> h07 — third heart sound, S3.
> h08 — fourth heart sound, S4.
> h09 — tachycardia.
> Pulmonary code register
> l00 — baseline: no annotated adventitious event, or a normal lung sound.
> l01 — continuous: wheeze, rhonchus, or stridor event.
> l02 — discontinuous: fine or coarse crackle event.
> l03 — friction: pleural-friction/rub sound.
> public/test_index.csv (480 rows)
> clip_id — string. Names public/test_audio/<clip_id>.wav; every value must be covered by the
> submission.
> public/sample_submission.csv (19,200 rows)
> clip_id — string. Each test identifier appears in exactly 40 rows.
> heart_code — string. One of the ten cardiac codes.
> lung_code — string. One of the four pulmonary codes.
> mass — float. Non-negative joint belief for this exact pairing.
> The sample is a deterministic, fixed signal-processing format illustration. It reads two preselected spectral
> summary coordinates, converts distances from fixed reference points into soft weights, and blends the joint
> surface with uniform mass. It does not read training labels, fit an estimator, or use ML/DL, and scores
> approximately 0.012494. It is supplied to demonstrate output construction, not as an admissible competitive
> method; submissions must still follow the What not to use rules.
> What you must submit
> Submit a long-form CSV with a header and exactly 19,200 rows: all 40 pairings for each of the 480 test
> clips.
> clip_id,heart_code,lung_code,mass
> te_0a1b2c3d4e5f6789,h00,l00,0.004
> te_0a1b2c3d4e5f6789,h00,l01,0.012
> te_0a1b2c3d4e5f6789,h00,l02,0.021
> clip_id — copied from test_index.csv; each appears in 40 rows.
> heart_code — h00 through h09; each appears four times per clip.
> lung_code — l00 through l03; each appears ten times per clip.
> mass — non-negative joint mass for this exact pairing; it need not already sum to one.
> For every submitted identifier, all 40 normalized (heart_code, lung_code) keys must occur exactly once.
> Duplicate normalized keys, unknown codes, incomplete surfaces, negative masses, and non-finite masses make the
> submission invalid and return 0.0. The grader safely rescales each valid surface; an all-zero but otherwise
> valid surface becomes uniform. Harmless extra columns, row reordering, UTF-8 BOMs, and surrounding whitespace
> are accepted. A missing required column raises ValueError. Complete rows for identifiers outside the current
> graded answer subset are ignored so that partial evaluation remains well-defined.
> How scoring works
> For clip i, let P_i(h,l) be the normalised submitted 10 × 4 surface and Y_i(h,l) the one-hot truth.
> The grader derives seven mutually consistent views from the same surface:
> H(P) — ten-state cardiac marginal;
> L(P) — four-state pulmonary marginal;
> FH(P) — four cardiac families;
> A(P) — pulmonary baseline versus any adventitious sound;
> C(P) — cardiac-family × exact-pulmonary-state 4 × 4 surface;
> D(P) — cardiac-family × adventitious-presence 4 × 2 surface;
> P itself — all 40 exact joint cells.
> The cardiac families are baseline {h06}, murmur {h02,h03,h04,h05}, rhythm {h00,h01,h09}, and added
> sound {h07,h08}. Pulmonary baseline is {l00} and adventitious is {l01,l02,l03}.
> For arrays A and B, pooled quadratic loss is:
> Brier(A, B) = (1 / n) * sum_i ||A_i - B_i||^2
> Three multiresolution losses are evaluated:
> E_H(P,Y) = 1.00 * Brier(H(P),  H(Y))  + 0.30 * Brier(FH(P), FH(Y))
> E_L(P,Y) = 1.00 * Brier(L(P),  L(Y))  + 0.30 * Brier(A(P),  A(Y))
> E_J(P,Y) = 1.00 * Brier(P,     Y)     + 0.70 * Brier(C(P),  C(Y))
> + 0.35 * Brier(D(P),  D(Y))
> Let M = mean_i Y_i, the optimal blind constant surface on the exact graded answer subset. For
> k in {H,L,J}:
> r_k  = clip(1 - E_k(P,Y) / E_k(M,Y), 0, 1)
> d(n) = max(0.015, 0.45 / sqrt(n - 1))
> s_k  = clip((r_k - d(n)) / (1 - d(n)), 0, 1)
> This empirical-constant correction makes every blind fixed surface non-positive before clipping. The
> count-aware deadband removes accidental finite-sample skill. Degenerate projections receive 1 only for an
> exact match and 0 otherwise; a one-answer subset behaves the same way.
> The final score is a bottleneck-breadth fusion:
> bottleneck = min(s_H, s_L, s_J)
> breadth    = (s_H + s_L + s_J) / 3
> score      = bottleneck * (0.5 + 0.5 * breadth)
> Solving only one organ therefore scores 0.0; balanced improvement is rewarded only after all three heads
> show skill. The score is continuous, uncapped inside [0,1], and perfect joint surfaces score exactly 1.0.
> Constants
> HEART_STATES       = 10
> LUNG_STATES        = 4
> CARDIAC_FAMILIES   = 4
> LUNG_SUPERSTATES   = 2
> ORGAN_WEIGHTS      = (1.0, 0.3)
> JOINT_WEIGHTS      = (1.0, 0.7, 0.35)
> DB_MIN             = 0.015
> NULL_Z             = 0.45
> EPS                = 1e-12
> SNAP               = 1e-10
> What not to use
> You must solve this with a model you build and train from scratch on the provided training audio. Any
> submission that reaches its answer by other means is disqualified.
> Banned — rule-based and non-learned approaches.
> No hand-written rules, fixed formulae, hard-coded thresholds, hand-authored decision trees, or a manually
> measured audio property used as the predictor. A fixed low-versus-high energy recipe is prohibited; the
> overlapping states must be learned from the training pairs.
> No constant, near-constant, or id-derived mass, and nothing parsed from opaque clip_id values, file order,
> row order, or encoding artefacts. The answer must come from a model learned on the supplied examples.
> No manual or human listening to label the test clips, and no outsourcing to an annotation service.
> Banned — pretrained weights and outside data (disqualifying).
> No pretrained or foundation models of any kind, and no audio embeddings, feature extractors, weights,
> pseudo-labels, or initialisation learned from other data. Every learned parameter must start randomly and
> be trained only on the provided data. Unsupervised or self-supervised learning on the provided audio is
> allowed.
> No external audio, catalogs, diagnostic references, or label sources, and no reverse search or matching of
> served clips against any outside collection to recover states or provenance.
> Allowed. Any model you design, train, and validate yourself from scratch on the provided data; you choose
> the representation, architecture, and training procedure. Every learned parameter must come only from these
> training examples.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Voice Matrix Sketch Completion

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77bhs66aczhqh24ymkdfhdbx8bps8j
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> This is a from-scratch audio modeling challenge. Each row gives a tiny matrix of encoded sound sketches from two voices:
> a reference voice with three known non-speech sounds;
> a target voice with two of those sounds shown;
> one missing target-voice sound that you must predict.
> In plain terms: learn how the target person's voice changes the acoustic sketch of a sound, then draw the missing target-style sketch for the requested third sound.
> The source sounds are real 16 kHz human non-speech recordings: coughs, laughs, sighs, sneezes, sniffs, and throat-clearing sounds. The public data is not raw audio; each clip is converted into a 64 by 48 quantized spectral sketch. The hidden target sketch is a deterministic voice-conditioned completion built from real source sketches: the reference voice's query sound is transformed using the target voice style estimated from the two shown target/reference sound pairs, with a small amount of source-recording texture retained. Speakers used for hidden test rows are disjoint from speakers used for training rows.
> This is not single-clip labeling, word recognition, or timeline detection. The intended solution is to train or fine-tune an audio/spectrogram model that performs cross-voice acoustic sketch completion.
> Dataset files
> train.csv contains:
> id: string. Unique training row ID.
> reference_voice_cards: JSON list. Three known sound sketches from a reference voice.
> target_voice_cards: JSON list. Two known sound sketches from the target voice.
> query_slot: string. Row-local slot, such as S2, for the missing target-voice sound.
> strip_shape: string. Always 64x48.
> alphabet: string. The 64-symbol quantization alphabet.
> target_strip: string. Training-only answer sketch for the missing target-style completion. It has exactly 3,072 characters using the alphabet in alphabet.
> test.csv has the same public columns but omits target_strip.
> sample_submission.csv contains:
> id: string. Test row ID.
> predicted_strip: string. Dummy invalid value that scores 0.
> There are 4,200 training rows and 1,800 hidden test rows. Hidden rows are balanced across six private scenario families with 300 rows per family.
> JSON field schemas
> Each reference_voice_cards item has:
> slot: string. Row-local sound slot such as S1, S2, or S3.
> sound_hint: string. Plain-language description of the non-speech sound.
> reference_voice_strip: string. Encoded 64 by 48 spectral sketch for the reference voice making this sound.
> Each target_voice_cards item has:
> slot: string. Row-local sound slot shown for the target voice.
> known_target_strip: string. Encoded 64 by 48 spectral sketch for the target voice making this known sound.
> The missing target is the query_slot. For example, if the reference voice shows S1, S2, S3, and the target voice shows only S1 and S3, then query_slot = S2 asks for the target voice's S2 sketch.
> Strip encoding
> Every strip string has exactly 3,072 characters.
> Decode it by mapping each character through:
> 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_
> to an integer from 0 to 63, then reshape row-major to 64 spectral bands by 48 time frames. Larger values mean stronger log spectral energy.
> Output format
> Submit one predicted 64 by 48 strip per test row.
> Rules:
> predicted_strip must be exactly 3,072 characters.
> Every character must be in the provided 64-symbol alphabet.
> Do not submit JSON, WAV files, natural-language text, comma-separated numbers, or extra columns.
> Evaluation
> Structurally invalid submission files are rejected. Structural errors include missing columns, extra columns, duplicate IDs, unknown IDs, missing IDs, wrong row count, or wrong column order.
> Malformed row-level strips score 0 for that row instead of crashing the grader.
> For each valid row, let P be the predicted 64 by 48 integer strip and T be the hidden target strip. The metric intentionally emphasizes active acoustic structure rather than the silent background.
> Active target cells are cells where T >= 8. If that would select fewer than 12% of cells, the grader instead uses the highest-energy 12% of cells in T.
> ActiveExact = mean(abs(P - T) <= 2 over active target cells)
> PeakF1 = F1 between:
> predicted peak cells = highest-energy 12% of cells in P
> target peak cells = highest-energy 12% of cells in T
> WeightedValue =
> max(0, 1 - weighted_mean(abs(P - T)) / 8)
> where each cell weight is:
> weight = 1 + 4 * (T / 63)^1.5
> FrameEnergy =
> max(0, 1 - weighted_mean(abs(mean_frequency(P) - mean_frequency(T))) / 6)
> where each frame weight is:
> frame_weight = 1 + mean_frequency(T)
> BandEnergy =
> max(0, 1 - weighted_mean(abs(mean_time(P) - mean_time(T))) / 6)
> where each frequency-band weight is:
> band_weight = 1 + mean_time(T)
> EnergyMass =
> max(0, 1 - abs(sum(P) - sum(T)) / (0.75 * max(sum(T), 1)))
> If P exactly equals T, row_score = 1. Otherwise:
> row_score =
> 0.45 * ActiveExact
> + 0.20 * PeakF1
> + 0.15 * WeightedValue
> + 0.08 * FrameEnergy
> + 0.07 * BandEnergy
> + 0.05 * EnergyMass
> The hidden set is balanced across six private families:
> breath_to_burst
> burst_to_breath
> same_gender_bridge
> cross_gender_bridge
> quiet_target
> long_tail_voice
> Family labels are not present in solver-facing files.
> Final score:
> overall_mean = mean(row_score over all hidden rows)
> worst_family_mean = minimum family mean over the six private families
> bottom_20_mean = mean(row_score over the lowest-scoring 20% of hidden rows)
> final_score =
> 0.70 * overall_mean
> + 0.20 * worst_family_mean
> + 0.10 * bottom_20_mean
> Scores are finite and bounded in [0, 1]. The sample submission scores 0. A perfect oracle scores 1.
> Submission format
> Submit a CSV with exactly two columns in this order:
> id: test row ID.
> predicted_strip: encoded 64 by 48 target sketch.
> Example:
> id,predicted_strip
> 0a12bc34de56f789,0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_012...
> The example is schematic; a real prediction must contain exactly 3,072 valid characters.
> What not to use
> Do not use source filenames, source speaker IDs, row order, or fixed slot meanings. These are absent from solver-facing rows or row-local.
> Do not copy one public card blindly. The hidden target is the target voice making the query sound, not the reference voice and not a known target card.
> Do not submit raw audio, images, JSON arrays, model files, or explanatory text.
> Do not rely on similar or trivial approaches; use diverse, compliant methods rather than optimizing purely for score.
> Recommended solution approach
> A basic solution can decode strips and train a compact spectrogram autoencoder or conditional image model from scratch. Stronger solutions may fine-tune an audio/spectrogram encoder-decoder, condition jointly on reference-voice and target-voice cards, and validate with speaker-disjoint folds.
> Benchmark boundary
> Nearby audio task families usually label isolated clips, compare identities, detect events on a timeline, or generate raw waveforms. This benchmark instead asks for conditional spectral sketch completion in a two-voice matrix with row-local sound slots, held-out target speakers, hidden sound slots, and robust family/tail scoring.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Occluded Handwritten Digit Circuit Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76ta53y6d8a61qm0vwrn45j58bq57r
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Each image is a corrupted six-node circuit. The six nodes lie at fixed canonical positions around a hexagon. Every node contains a handwritten digit with an independently chosen quarter-turn rotation. Every adjacent node pair is connected by either a solid positive edge or a dashed negative edge. One node is marked as the traversal start, and a central arrow specifies clockwise or counter-clockwise traversal.
> Your task is to reconstruct the complete latent circuit from each 96×96 grayscale image. This is a from-scratch structured vision task: all trainable weights must be initialized from scratch during the submitted run. Pretrained checkpoints, external datasets, internet access, and models that embed pretrained weights are prohibited.
> Every diagram contains substantial partial occlusion across three to five distinct digit nodes, selected without replacement. Each selected node is crossed by a dark 7–10 pixel primary band, together with blur, contrast changes, distractor strokes, pixel noise, geometric jitter, and occasional foreground/background inversion. No prepared image is unoccluded. The hidden test diagrams use digit glyph sources from style clusters that are disjoint from the sources used to generate training diagrams.
> Canonical Geometry and Labels
> n0 is the node at 12 o'clock.
> n1, n2, ..., n5 continue clockwise.
> Edge e0 joins n0 to n1; e1 joins n1 to n2; ...; e5 joins n5 to n0.
> rotation_ni is the number of 90-degree counter-clockwise quarter turns applied to the source glyph before rendering: 0, 1, 2, or 3.
> edge_sign_ei = 1 means a solid positive edge.
> edge_sign_ei = 0 means a dashed negative edge.
> direction = 0 means clockwise.
> direction = 1 means counter-clockwise.
> Circuit Checksum
> The checksum is deterministic and must be predicted as an integer in 0–96. Let:
> d[i] be digit_ni
> r[i] be rotation_ni
> s[i] be edge_sign_ei
> a be start_node
> q be direction
> step = +1 when q = 0, otherwise step = -1
> Initialize:
> total = 11  *a + 13*  q
> For t = 0, 1, ..., 5:
> node = (a + step * t) mod 6
> edge = node                    when q = 0
> edge = (node - 1) mod 6        when q = 1
> sign = +1                      when s[edge] = 1
> sign = -1                      when s[edge] = 0
> total += sign  *(2*  t + 1) * d[node]
> total += 7  *(t + 1)*  r[node]
> Finally:
> checksum = total mod 97
> Python's non-negative modulo convention is used, so checksum always lies in 0–96.
> Prepared Dataset
> All solver inputs are under ./dataset/public/.
> | File | Type | Description |
> |---|---|---|
> | train_images.npy | NumPy uint8, shape (18000, 96, 96) | Training images. |
> | test_images.npy | NumPy uint8, shape (4500, 96, 96) | Test images. |
> | train.csv | CSV | sample_id, image_index, and all 21 target columns. |
> | test.csv | CSV | sample_id and image_index; no targets. |
> | sample_submission.csv | CSV | Exact required submission columns and row identifiers. |
> | label_schema.json | JSON | Machine-readable ranges and canonical semantics. |
> image_index is only an array-row locator. For a CSV row, read the corresponding image as images[image_index]. Do not infer labels from sample_id, image_index, filenames, or row order.
> Training Columns
> | Column | Type | Valid values | Meaning |
> |---|---|---|---|
> | sample_id | string | unique | Stable row key. |
> | image_index | integer | 0–17999 | Row in train_images.npy. |
> | digit_n0 ... digit_n5 | integer | 0–9 | Digit at each canonical node. |
> | rotation_n0 ... rotation_n5 | integer | 0–3 | Quarter-turn rotation at each node. |
> | edge_sign_e0 ... edge_sign_e5 | integer | 0 or 1 | Dashed/negative or solid/positive edge. |
> | start_node | integer | 0–5 | Double-ringed traversal start node. |
> | direction | integer | 0 or 1 | Clockwise or counter-clockwise central marker. |
> | checksum | integer | 0–96 | Modular checksum defined above. |
> Test Columns
> | Column | Type | Meaning |
> |---|---|---|
> | sample_id | string | Stable row key required in the submission. |
> | image_index | integer | Row in test_images.npy. |
> Evaluation
> Submissions are ranked by the Weighted Structured Reconstruction Score. Higher is better.
> For each target family, accuracy is calculated over all relevant positions and test samples. ExactCircuitAccuracy is the fraction of samples for which all 21 target values are correct.
> Score = 0.40 * DigitAccuracy
> + 0.15 * RotationAccuracy
> + 0.10 * EdgeAccuracy
> + 0.10 * StartNodeAccuracy
> + 0.05 * DirectionAccuracy
> + 0.15 * ChecksumAccuracy
> + 0.05 * ExactCircuitAccuracy
> The seven component weights intentionally sum to exactly 1.00; no scoring component, residual weight, or additional normalization factor is omitted. The score is bounded to [0.0, 1.0], and a perfect submission receives 1.0.
> Submission
> The submitted file must be written to:
> ./working/submission.csv
> It must contain exactly 4,500 rows and exactly these columns, in this order:
> sample_id,
> digit_n0,digit_n1,digit_n2,digit_n3,digit_n4,digit_n5,
> rotation_n0,rotation_n1,rotation_n2,rotation_n3,rotation_n4,rotation_n5,
> edge_sign_e0,edge_sign_e1,edge_sign_e2,edge_sign_e3,edge_sign_e4,edge_sign_e5,
> start_node,direction,checksum
> The line breaks above are for readability; the CSV header is one row.
> Example:
> sample_id,digit_n0,digit_n1,digit_n2,digit_n3,digit_n4,digit_n5,rotation_n0,rotation_n1,rotation_n2,rotation_n3,rotation_n4,rotation_n5,edge_sign_e0,edge_sign_e1,edge_sign_e2,edge_sign_e3,edge_sign_e4,edge_sign_e5,start_node,direction,checksum
> 5c3a01f4a12f6e9be001,7,2,9,0,4,1,0,1,3,2,0,1,1,0,1,1,0,1,4,0,62
> Submission Requirements
> Include every hidden sample_id exactly once.
> Do not include unknown IDs, duplicate IDs, extra columns, or an index column.
> Every prediction must be finite and integer-valued within its specified range.
> The grader aligns rows by sample_id; submission row order does not affect the score.
> Invalid schema, IDs, non-integer predictions, non-finite values, or out-of-range values cause grading failure.
> Runtime and Implementation Rules
> Domain: From scratch.
> Compute tier: GPU.
> The solution must run end to end without internet access or manual intervention.
> Read only from ./dataset/public/.
> Write only inside ./working/, with final predictions at ./working/submission.csv.
> Use only libraries already present in the configured Kaggle-style runtime.
> Do not install packages during execution.
> Do not use pretrained weights, downloaded checkpoints, external datasets, hidden/private files, or test labels.
> Do not fit supervised targets on the test set or derive predictions from IDs, filenames, or row ordering.
> The same learned or algorithmic pipeline must be applied uniformly to every test sample.
> Complete within the configured Project Eris GPU runtime.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Scholarly Reference Linking

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx754x4y71hwbphp4h9s19jz4589fkej
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Every research paper stands on earlier work, and which earlier works it builds on is a strong,
> structured signal: a paper's own words hint at the foundational studies behind it, even when it
> never names them. This challenge asks you to recover that hidden bibliography from the prose.
> You are given a query work's abstract and a fixed CATALOG of frequently-cited works, each shown
> only as an opaque id together with its own (redacted) abstract text. Your job is to return the
> SET of catalog works that the query work cites. The label space is the open catalog, not a
> fixed class list, so this is a LINKING problem, not a classification one.
> The task is hard on purpose. Most of a paper's citations are not spelled out in its abstract at
> all -- you have to infer them from topic, method, and framing. A large share of the correct
> links share little vocabulary with the query abstract, so string or keyword overlap reaches only
> the easy citations; the rest must be learned from how abstracts and the works they cite are
> related across the training set. The scoring weights those hard, non-lexical links more heavily.
> Evaluation
> For one query, let Pred be your predicted set of catalog ids and True the correct set. The
> standard set-F1 is:
> F1 = 0                          if Pred or True is empty, or they do not intersect
> F1 = 2*p*r / (p + r)            otherwise, with p = |Pred and True| / |Pred|, r = |Pred and True| / |True|
> Each query i carries a weight w_i:
> w_i = 2.5   if at least one cited catalog work is lexically hidden -- its text barely overlaps
> the query abstract, so string matching cannot reach it
> w_i = 1.0   otherwise
> The weight depends on the hidden answer and is not derivable from the public data. The final
> score is the weighted mean set-F1:
> score = sum_i ( w_i * F1_i ) / sum_i ( w_i )
> The weighting is binary at query level. One or more lexically hidden citations gives the query
> weight 2.5; additional hidden citations do not create intermediate or larger weights.
> Recovering every set perfectly scores 1.0; predicting nothing scores 0. Range is 0 to 1.
> Duplicate catalog ids in one prediction cell are ignored first. The grader then scores at most
> the first 200 unique predicted ids, preserving their first-occurrence order.
> Dataset
> The public data consists of the files below.
> train.csv — labeled query works, with columns:
> id — type string: opaque query-work identifier.
> abstract — type string: the redacted abstract of the query work.
> cited — type string: the answer, a space-separated set of catalog_id values the query
> work cites. This column appears only in train.csv.
> test.csv — the query works to predict on, with the same id and abstract columns but with
> NO cited.
> catalog.csv — the candidate vocabulary you answer in, with columns:
> catalog_id — type string: opaque identifier of a frequently-cited work.
> text — type string: that work's own redacted abstract, so you can represent it by content.
> sample_submission.csv — a valid example submission in exactly the format the grader expects.
> task_manifest.json — documentation only: task, inputs, target, submission columns, and metric.
> Query works are split so that whole subfields are held out: the test queries come from research
> subfields not present in the training queries, so memorizing which text goes with which citation
> does not transfer -- you have to learn how to link.
> Example train.csv rows:
> id,abstract,cited
> w0a1b2c3d4e5q,coral calcification declines under thermal stress ...,w11aa22bb33cc w4455dd66ee7
> w19f8e7d6c5b4q,reef fish assemblages shift with habitat complexity ...,w778899aabbcc
> The matching test.csv rows drop the final cited column.
> Submission
> Submit a CSV with exactly these columns:
> id — type string: test query id.
> cited — type string: the set of catalog ids you predict, space-separated, each copied from
> catalog.csv. Use an empty string to predict nothing. Ids outside the catalog can never match
> and only dilute precision.
> Example:
> id,cited
> w0a1b2c3d4e5q,w11aa22bb33cc w4455dd66ee7
> w19f8e7d6c5b4q,w778899aabbcc
> Appropriate Approaches
> Train a learned text encoder or cross-encoder inside your solution that maps the query
> abstract and the catalog works into a shared space, and optimize it with a ranking or
> contrastive objective on the training citation pairs. This is the load-bearing component.
> Plain lexical similarity (TF-IDF, BM25) between the query abstract and catalog text reaches
> the easy, lexically-named citations, but the weighted metric rewards the hidden ones that only
> a learned model recovers. Use lexical similarity for candidate generation, not as the final
> ranker.
> Tune how many ids to output per query -- precision and recall trade off -- on a
> subfield-disjoint split of the training queries.
> Runtime and environment rules
> The environment that runs your solution has these limits; design your solution to fit them:
> Compute is provided by one NVIDIA A10G GPU.
> The complete solution must finish within 1.5 hours.
> There is no internet access at runtime: no downloading of data, models, or weights, and no
> installing packages. Only libraries already provided in the execution image may be used.
> Train everything you use from the provided training data. No pretrained model weights or
> embeddings of any kind.
> What Must Not Be Used
> No pretrained model weights or embeddings; train from the provided data.
> No external data or network access.
> The ids are opaque and the abstracts are redacted. Do not attempt to de-anonymize a work,
> recover its original identifier, or look up its real bibliography in any external or offline
> resource; reconstructing the sources is out of scope and treated as cheating.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Residue Contact Shell Record Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71t349a6ryztd36g0zk3zr218bss85
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: generative
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> You are given local sequence and backbone-geometry context for a residue in a protein chain. Your task is to recover the residue's nonlocal spatial contact-shell record: how many other residues fall within the contact radius, how those contacts distribute by sequence separation and residue chemistry, and a compact set of nearest-contact cards.
> This is a training-from-scratch structural biology challenge. The training set provides many examples of local residue environments and their derived contact shells. Strong solutions should learn patterns of protein packing from the provided examples rather than search for source structures.
> Dataset
> The public files are:
> train.csv: labeled residue examples.
> test.csv: unlabeled residue examples to solve.
> sample_submission.csv: schema-valid example submission.
> Columns:
> id (string): anonymized row id.
> residue_context_json (JSON string): local residue context.
> target_schema_json (JSON string): required answer schema.
> answer_json (JSON string, train only): target contact-shell record.
> residue_context_json fields:
> center_residue (string): one-letter amino-acid code for the central residue.
> local_sequence_23 (string): 23-residue sequence window centered on the residue.
> chain_length_bucket (integer): chain length rounded down to a 50-residue bucket, capped at 500.
> ca_angle_degrees_m3_to_p3 (array of numbers): seven C-alpha bend angles around offsets -3 through +3.
> ca_neighbor_distances (array of numbers): C-alpha distances from the center residue to offsets -5, -4, -3, +3, +4, and +5.
> local_aa_group_counts (object): counts of amino-acid chemistry groups in the 23-residue window.
> answer_json fields:
> total_contacts (integer): count of nonlocal residues whose C-alpha atom is within 8.0 Angstroms of the center residue.
> sequence_separation_counts (object): integer counts for sep_04_12, sep_13_48, and sep_49_plus.
> contact_group_counts (object): integer counts for hydrophobic, polar, positive, negative, and special.
> nearest_contact_cards (array): up to eight nearest-contact objects. Each object has seq_sep_bin, side, aa_group, and distance_bin.
> Allowed card values:
> seq_sep_bin: one of sep_04_12, sep_13_48, sep_49_plus.
> side: one of n_terminal, c_terminal.
> aa_group: one of hydrophobic, polar, positive, negative, special.
> distance_bin: one of d_lt_5p5, d_5p5_6p8, d_6p8_8p0.
> Submission
> Submit a CSV with exactly two columns:
> id (string): id from test.csv.
> answer_json (JSON string): predicted contact-shell record.
> Example:
> id,answer_json
> prs_1111111111111111,"{""total_contacts"":7,""sequence_separation_counts"":{""sep_04_12"":2,""sep_13_48"":3,""sep_49_plus"":2},""contact_group_counts"":{""hydrophobic"":3,""polar"":2,""positive"":1,""negative"":1,""special"":0},""nearest_contact_cards"":[{""seq_sep_bin"":""sep_13_48"",""side"":""c_terminal"",""aa_group"":""hydrophobic"",""distance_bin"":""d_5p5_6p8""}]}"
> Evaluation
> Each row receives a score from 0 to 1:
> row_score = 0.18 * total_score + 0.24 * separation_score + 0.24 * chemistry_score + 0.34 * card_f1
> For each numeric count, count_score = 1 - min(1, abs(predicted - true) / max(1, predicted + true)). total_score applies this formula to total_contacts. separation_score is the mean count score over the three sequence-separation bins. chemistry_score is the mean count score over the five chemistry groups.
> card_f1 is duplicate-aware multiset F1 over the nearest-contact card tuples (seq_sep_bin, side, aa_group, distance_bin). Malformed JSON or invalid field values receive 0 for that row. The leaderboard score is the mean row score across all test rows.
> What Not To Use
> Do not use external structure databases, source mirrors, or source coordinate files.
> Do not search for test rows on the internet.
> Do not use pretrained protein language models, structure models, embeddings, hosted APIs, or checkpoint-derived features.
> Do not hard-code test ids or answer dictionaries.
> Do not manually annotate the test set.
> Do not use internet access during solution execution.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Electronic Nose Exposure Field Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7736jv8bd9b068j8ze53wged8bv59c
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> This is a from-scratch scientific sensor-modeling challenge. For each row, you are given a compact recording from a small electronic nose: twelve time channels showing slow gas-sensor responses, mixed flow timing, heater state, row-local gas cards, and calibration snippets. Your task is to reconstruct the hidden fast gas exposure field that caused those slow sensor responses.
> In plain terms: the sensors smear together short odour exposures. Instead of naming a class or writing an event list, you must recover a fixed gas-by-time image showing which row-local gas aliases were present at each time frame and with what relative intensity.
> The challenge is grounded in a real high-speed electronic-nose source dataset. The source contains e-nose and fast PID odour measurements. The prepared benchmark uses the same odour-channel and protocol structure to create deterministic sensor-inversion examples. Public rows do not contain source trial IDs, filenames, or hidden exposure fields.
> This is not odour classification, anomaly detection, or scalar regression. The scored output is a fixed-size multichannel exposure raster.
> Dataset files
> train.csv contains 4,320 rows.
> id: string. Unique training row ID.
> sensor_strip: string. Encoded 12 by 192 sensor-response strip.
> flow_total_code: string. Encoded length-192 mixed flow monitor.
> strip_shape: string. Always 12x192.
> frame_step_ms: integer. Always 10.
> heater_mode: string. Sensor heater regime.
> gas_cards: JSON list. Six row-local gas aliases and coarse response hints.
> sensor_cards: JSON list. Eight sensor-channel descriptions.
> calibration_cards: JSON list. Four known single-pulse response snippets from the same row-local condition.
> exposure_shape: string. Always 6x192.
> target_exposure_code: string. Training-only encoded hidden exposure field.
> test.csv contains 1,500 rows and the same public columns, excluding target_exposure_code.
> sample_submission.csv contains every test ID with a documented zero-information dummy code. The dummy is structurally valid and scores 0.
> Hidden test rows are balanced across six private sensor conditions, with 250 rows per condition.
> Input encodings
> The 64-character alphabet is:
> 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_
> For sensor_strip, map each character to an integer from 0 to 63, divide by 63, and reshape row-major to 12x192.
> Channels 1–8 are gas-resistance sensor responses.
> Channels 9–12 are heater/environment context channels.
> For flow_total_code, decode the same way into a length-192 vector. It helps locate exposure timing but does not identify gas aliases.
> JSON field schemas
> gas_cards is a JSON list of exactly six objects. Each object has:
> gas: string. Row-local gas alias from G01 through G06.
> volatility_hint: string. low, medium, or high.
> polarity_hint: string. weak, mixed, or strong.
> response_family: string. fast_rise, slow_tail, or broad_tail.
> sensor_cards is a JSON list of eight objects. Each object has:
> sensor: string. Sensor alias from S1 through S8.
> readout: string. Source-schema readout name such as R_gas_3.
> sensitivity_hint: string. Coarse response pattern hint.
> noise_tier: string. low, medium, or high.
> calibration_cards is a JSON list of exactly four objects. Each object has:
> known_pulse: string. A small known calibration exposure descriptor using row-local gas aliases.
> response_shape: string. Always 8x80.
> response_code: string. Encoded eight-sensor calibration response.
> Calibration cards are public examples of how this row-local condition responds to known exposures. They are hints for deconvolution, not scored targets.
> Output format
> Submit one fixed-length predicted_exposure_code per test row.
> The prediction must be exactly 1,152 characters long because it encodes a 6x192 matrix:
> rows are gas aliases G01, G02, G03, G04, G05, G06 in that order;
> columns are time frames 0 through 191;
> values use the same 64-symbol alphabet;
> larger values mean stronger hidden gas exposure for that gas alias and time frame.
> Do not submit JSON, event tokens, numeric arrays, Python code, natural-language explanations, or strings with separators. The field is one continuous encoded raster string.
> Evaluation
> Structurally invalid submission files are rejected. Structural errors include missing columns, extra columns, duplicate IDs, unknown IDs, missing IDs, wrong row count, or wrong column order.
> Malformed row-level predictions score 0 for that row. A malformed row prediction is any value that is not exactly 1,152 allowed alphabet characters.
> The provided sample uses a fixed dummy code:
> 1151 copies of `0`, followed by `_`
> This dummy is accepted by the parser and assigned row score 0.
> Rows are aligned by id, not by row order.
> For each row, the grader decodes the predicted and hidden exposure fields as 6x192 matrices with values in [0, 1].
> FieldSkill measures improvement over predicting an all-zero field:
> ZeroMSE = mean((0 - TrueField)^2)
> PredMSE = mean((PredField - TrueField)^2)
> RawField = clip(1 - PredMSE / ZeroMSE, 0, 1)
> FieldSkill = RawField * RawField
> SupportF1 is F1 over active gas-time cells:
> PredActive = cells where PredField >= 0.12
> TrueActive = cells where TrueField >= 0.12
> SupportF1 = F1(PredActive, TrueActive)
> DoseScore compares total exposure per gas alias. For every true-active gas, the score is:
> GasDoseScore = max(0, 1 - abs(PredDose - TrueDose) / max(TrueDose, 0.15))
> An additional inactive-gas penalty reduces credit when predicted exposure appears on gases that are not present in the hidden field. DoseScore is the mean of active-gas dose scores plus this inactive-gas score.
> PeakTimingScore compares the strongest exposure frame for each true-active gas:
> PeakTimingScore = 1.0 if peak distance <= 2 frames
> PeakTimingScore = 0.5 if peak distance is 3 to 6 frames
> PeakTimingScore = 0.0 otherwise
> ExactCode is 1 only when the 1,152-character prediction exactly equals the hidden code.
> Row score:
> row_score =
> 0.46 * FieldSkill
> + 0.24 * SupportF1
> + 0.15 * DoseScore
> + 0.10 * PeakTimingScore
> + 0.05 * ExactCode
> The hidden set is balanced across six private sensor conditions:
> single_pulse
> overlap_duet
> rapid_switch
> low_concentration
> sensor_saturation
> baseline_drift
> Each condition has 250 hidden rows. Condition labels are not present in solver-facing files.
> Final score:
> overall_mean = mean(row_score over all hidden rows)
> worst_family_mean = minimum family mean over the six private conditions
> bottom_20_mean = mean(row_score over the lowest-scoring 20% of hidden rows)
> final_score =
> 0.64 * overall_mean
> + 0.22 * worst_family_mean
> + 0.14 * bottom_20_mean
> Scores are finite and bounded in [0, 1]. The sample submission scores 0. A perfect oracle scores 1.
> Submission format
> Submit a CSV file with exactly two columns in this order:
> id: string. Test row ID from test.csv.
> predicted_exposure_code: string. Exactly 1,152 allowed alphabet characters.
> Example with shortened code for display only:
> id,predicted_exposure_code
> 0a12bc34de56f789,000000000000000000000000000000000000000000000000000000000000...
> The real CSV value must contain the full 1,152-character code.
> Recommended solution approach
> A basic solution can learn a sensor-to-exposure inverse model from the training fields. Stronger solutions should use calibration cards to estimate row-local sensor kernels, separate overlapping gas responses, model heater/environment channels, and handle weak, saturated, drifting, and rapidly switching conditions. GPU-friendly approaches include temporal CNNs, U-Nets over gas-time fields, small Transformers, differentiable deconvolution, and calibration-conditioned neural decoders.
> What not to use
> Do not use row IDs, row order, fixed gas aliases, source filenames, or hidden condition labels. Gas aliases are row-local.
> Do not submit token lists or operation programs. This challenge scores dense exposure-field reconstruction only.
> Do not optimize only total timing from flow_total_code; gas identity and per-gas dose matter.
> Do not assume the strongest sensor response marks the exposure time. Sensor lag, overlap, saturation, and drift are intentionally present.
> Benchmark boundary
> Prior electronic-nose benchmarks usually classify odour identity or estimate concentration from whole trials. This benchmark instead asks solvers to reconstruct a dense fast gas exposure field from slow multichannel sensor responses and row-local calibration snippets. It is a from-scratch sensor-field inversion benchmark, not a sequence-generation or odour-classification task.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Cocktail-Party Brainstream Binding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ec3pw691s9rqarp8b0qjf6s8brzk6
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> This is a from-scratch signal-learning challenge based on mobile EEG from a cocktail-party listening experiment. In each row, you see a compact EEG response strip and four anonymous candidate speech-stream cards. Your task is to identify which candidate stream is most consistent with the listener's neural tracking response, and also predict the response-lag tier and disruption tier.
> In plain terms: the listener heard competing speech while sitting or walking. The EEG strip is a compressed trace of brain activity. The stream cards are anonymous speech-envelope candidates. Submit the stream that the brain trace appears to be following.
> The source study recorded 20 participants with 24-channel mobile EEG at 250 Hz. Participants completed two-competing-speaker listening blocks while sitting or walking indoors, and the experiment included salient events intended to disturb attention. Public challenge rows are controlled source-new composites derived from real EEG windows and source-derived modulation traces; they are not raw source clips and they do not expose source participant IDs.
> The scored target is the candidate stream deliberately embedded by the benchmark generator into the compact neural composite, plus its lag and disruption tier. It should be interpreted as a controlled neural-signal binding benchmark, not as a medical or clinical claim about a participant's original attended speaker.
> This is not image classification, speech recognition, sequence-to-sequence generation, or tabular regression. The submitted answer is one fixed grammar token describing neural stream binding.
> Dataset files
> train.csv contains:
> id: string. Unique training row ID.
> neural_strip: string. A 12 by 96 compact EEG strip encoded with 64 printable symbols.
> strip_shape: string. Always 12x96.
> stream_cards: JSON list. Four anonymous candidate stream cards, S1 through S4.
> channel_group_cards: JSON list. Twelve EEG channel-group descriptors.
> candidate_count: integer. Always 4.
> max_lag_tier: string. Always L4.
> target_attention: string. Training-only answer token.
> test.csv has the same columns except target_attention.
> sample_submission.csv contains:
> id: string. Test row ID.
> predicted_attention: string. Empty dummy prediction. The sample scores 0.
> There are 4,500 training rows and 1,200 hidden test rows. Hidden test rows are balanced across five private scenario families, with 240 rows per family.
> Input field schemas
> neural_strip:
> Type: string.
> Length: 1,152 characters.
> Decoding alphabet: 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_.
> Decoding method: map each character to an integer from 0 to 63 and reshape row-major to 12 channel groups by 96 time frames.
> Meaning: larger values indicate stronger normalized compact EEG activity in that channel group and frame.
> Each stream_cards item has:
> stream: string. Row-local stream alias: S1, S2, S3, or S4.
> modulation_code: string. A 64-character source-derived speech-modulation proxy encoded with the same 64-symbol alphabet.
> speech_rate_tier: string. Coarse rate descriptor: slow, medium, or fast.
> envelope_peakiness: string. Coarse modulation shape descriptor: flat, mixed, or peaky.
> Each channel_group_cards item has:
> group: string. Channel-group alias such as G01.
> region: string. Approximate scalp region.
> quality: string. Coarse quality descriptor: clean, ok, or noisy.
> target_attention, present only in train.csv, has the same grammar as predicted_attention.
> Output grammar
> Submit one token per row:
> S#:L#:D#
> Where:
> S# is the attended stream alias: S1, S2, S3, or S4.
> L# is the neural lag tier: L0, L1, L2, L3, or L4.
> D# is the disruption tier: D0, D1, D2, or D3.
> Example valid predictions:
> S3:L2:D1
> S1:L0:D0
> Invalid examples:
> S5:L2:D1 S2 L2 D1 {"stream":"S2","lag":"L2","disruption":"D1"}
> ## **Evaluation**
> Structurally invalid submission files are rejected. Structural errors include missing columns, extra columns, duplicate IDs, unknown IDs, missing IDs, wrong row count, or wrong column order.
> Malformed row-level predictions score 0 for that row. Rows are aligned by `id`, not row order.
> For each row, parse the predicted and hidden answer as `(stream, lag, disruption)`.
> If the predicted stream is wrong:
> row_score = 0
> If the predicted stream is correct:
> StreamExact = 1
> LagScore = 1.00 if predicted lag equals hidden lag 0.35 if predicted lag is adjacent to hidden lag 0.00 otherwise
> DisruptionScore = 1.00 if predicted disruption equals hidden disruption 0.25 if predicted disruption is adjacent to hidden disruption 0.00 otherwise
> JointExact = 1 if stream, lag, and disruption all exactly match 0 otherwise
> Lag adjacency uses the order:
> L0, L1, L2, L3, L4
> Disruption adjacency uses the order:
> D0, D1, D2, D3
> The row score is:
> row_score = 0.55 * StreamExact
> 0.18 * LagScore
> 0.12 * DisruptionScore
> 0.15 * JointExact
> The hidden test set is balanced across five private scenario families:
> - `clean_tracking`
> - `walking_artifact`
> - `salient_drop`
> - `low_snr`
> - `lag_shift`
> Family labels are not present in public files. They are used only for robust hidden scoring. The `D#` disruption tier is not the same thing as the private family: each family contains a deterministic, mixed distribution of `D0` through `D3` rows, and spatial response profiles are row-specific mixtures rather than fixed family templates.
> For each family:
> family_mean = mean(row_score for rows in that family)
> Then:
> overall_mean = mean(row_score over all hidden rows) worst_family_mean = minimum family_mean over the five private families bottom_20_mean = mean(row_score over the lowest-scoring 20% of hidden rows)
> The final score is:
> final_score = 0.70 * overall_mean
> 0.20 * worst_family_mean
> 0.10 * bottom_20_mean
> Scores are finite and bounded in `[0, 1]`. The sample submission scores 0. A perfect oracle scores 1.
> ## **Submission format**
> Submit a CSV with exactly two columns in this order:
> - `id`: string. Test row ID.
> - `predicted_attention`: string. One output token following the grammar above.
> Example:
> id,predicted_attention 0a12bc34de56f789,S3:L2:D1
> ## **Recommended solution approach**
> A simple baseline can compute correlations between the EEG strip and the candidate modulation codes at several lag tiers. Stronger solutions should learn channel-group weights, artifact-robust temporal pooling, disruption-aware temporal signatures, and subject-disjoint calibration from the training rows.
> GPU use is appropriate for compact temporal convolution, transformer, or Siamese matching models over thousands of row-local EEG/candidate examples. The challenge is still small enough for fast iteration.
> ## **What not to use**
> Do not use row IDs, row order, source participant IDs, source motion labels, salience labels, or fixed stream aliases. Stream aliases are regenerated per row, and public rows intentionally omit source-motion and salience labels because those metadata fields are not the task.
> Do not assume the largest EEG peak is the answer. Walking artifacts, salient-event drops, and low-SNR rows intentionally break that shortcut.
> Do not submit JSON, natural-language explanations, multiple guesses, or extra columns.
> Do not optimize only the clean rows. Worst-family and bottom-tail scoring penalize ignoring walking, low-SNR, and disruption-heavy cases.
> ## **Benchmark boundary**
> Nearest prior work studies auditory attention decoding, EEG speech-envelope tracking, brain-computer interface classification, and saliency detection from mobile EEG. This benchmark differs by requiring row-local stream binding among anonymous candidate modulation cards, compact source-new EEG composites, explicit lag/disruption prediction, and robust family/tail scoring. It is a neural stream-binding benchmark, not ordinary EEG condition classification or speech transcription.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Math Solution Checkpoint Modeling

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dcgfr5n5jp6y5g70nmtgn4n8bsgy8
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Train a model from the released math-solution corpus and infer four checkpoint fields for each held-out problem: the final answer, a coarse hidden-solution length bin, important numeric tokens, and operation terms used later in the solution.
> Each row contains a math problem and the visible beginning of one worked solution. The missing portion is not a free-form essay target; it is summarized as a compact checkpoint record. The task measures whether a model trained from scratch on the provided examples can learn mathematical solution structure, connect partial derivations to final answers, and identify the later calculation vocabulary.
> Dataset
> The public files are:
> train.csv: labeled checkpoint examples.
> test.csv: held-out checkpoint examples without answer_json.
> sample_submission.csv: valid submission-format example.
> Columns in train.csv:
> id (string): anonymized row identifier.
> problem_text (string): math problem statement.
> visible_solution_prefix (string): first part of the worked solution.
> checkpoint_json (JSON string): public context object with hidden_suffix_char_hint (integer approximate hidden-character count), visible_prefix_char_count (integer), and allowed_step_bins (array of allowed strings).
> answer_format_json (JSON string): required target schema and allowed values.
> answer_json (JSON string): target checkpoint record.
> Columns in test.csv:
> id (string)
> problem_text (string)
> visible_solution_prefix (string)
> checkpoint_json (JSON string)
> answer_format_json (JSON string)
> Target JSON
> answer_json must contain:
> step_count_bin (string): one of short, medium, or long.
> final_answer (string): final answer as written in the source solution after normalization.
> numeric_trace (array of strings): up to 8 numeric tokens that appear in the hidden continuation or final answer.
> operation_terms (array of strings): up to 6 calculation or domain words from the hidden continuation.
> Submission
> Submit a CSV with exactly two columns:
> id (string)
> answer_json (JSON string)
> Example:
> id,answer_json
> case_0000000000000000,"{""step_count_bin"":""short"",""final_answer"":""42"",""numeric_trace"":[""42""],""operation_terms"":[""equation""]}"
> case_1111111111111111,"{""step_count_bin"":""long"",""final_answer"":""x=3"",""numeric_trace"":[""3""],""operation_terms"":[""factor"",""equation""]}"
> Evaluation
> The final score is the mean row score.
> For each row:
> step_count_bin_match = 1 if the submitted bin exactly matches the true bin after lowercasing and trimming whitespace; otherwise 0.
> final_answer_score = 1 if normalized submitted and true answers match exactly. Otherwise it is token F1 over alphanumeric and math tokens.
> numeric_trace_f1 is duplicate-aware F1 over the submitted and true numeric-token lists.
> operation_terms_f1 is duplicate-aware F1 over the submitted and true operation-term lists.
> For any duplicate-aware F1 list, count repeated values separately. Let matched be the sum, over all values, of the smaller submitted count and true count. Then:
> precision = matched / number_of_submitted_items
> recall = matched / number_of_true_items
> F1 = 2 * precision * recall / (precision + recall)
> If both lists are empty, F1 is 1. If exactly one list is empty, F1 is 0.
> The row score is:
> row_score = 0.10 * step_count_bin_match + 0.55 * final_answer_score + 0.20 * numeric_trace_f1 + 0.15 * operation_terms_f1
> Malformed row JSON scores zero for that row. Missing IDs, duplicate IDs, extra IDs, wrong columns, or wrong row count reject the submission.
> What Not To Use
> Do not use external copies of the source data to identify held-out rows.
> Do not search the web for test-row text, prompts, snippets, records, or metadata.
> Do not hard-code test IDs, answer dictionaries, or source-row lookup tables.
> Do not use hosted APIs or manual annotation of test rows.
> Do not use pretrained language models, pretrained embeddings, or challenge-specific checkpoints.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Financial Context Resolution

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78rv2adh9xy0kd35pm1sqs818bt9mc
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: finance
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Financial Context Resolution is a from-scratch language modeling challenge about resolving the meaning of highlighted expressions in professional financial reports.
> Each sample is an interpretation panel. It contains a tokenized sentence, one highlighted target span, and eight opaque interpretation codes. Exactly one code is consistent with the target in its full context.
> A code such as ROLE_4f91c2a8 carries no readable definition. It does not reveal whether the target describes an operating result, an obligation, a share quantity, a rate, a cash movement, a period comparison, or another reporting concept. Participants must recover the hidden interpretation system entirely from labeled examples.
> The benchmark is deliberately contrastive. Participants are not asked to generate a label from an unrestricted vocabulary. They must compare a compact portfolio of credible alternatives and determine which interpretation best fits the sentence, target boundaries, units, surrounding events, and reporting period.
> For every test sample, participants submit one score for each of the eight candidates. Higher scores indicate stronger support for that interpretation.
> Challenge Type
> This is a from-scratch neural modeling challenge.
> The primary predictive system must be a learned neural sequence model trained end to end on the released training data. All trainable parameters, including token embeddings, contextual encoders, target-span representations, and opaque-code representations, must begin from random initialization.
> Eligible primary architectures include transformers, recurrent neural networks, convolutional sequence encoders, state-space sequence models, or comparable trainable contextual architectures.
> The submitted candidate scores must be produced primarily by the learned neural model. Rule systems, lexical lookup tables, TF-IDF matching, nearest-neighbor retrieval, frequency tables, and classical machine-learning classifiers are not valid primary models.
> Tokenizers and vocabularies must be learned only from train.jsonl, unless they use fixed character-level or byte-level rules with no externally learned statistics.
> The challenge tests whether a neural model can learn contextual financial representations and induce a hidden interpretation system without pretrained language knowledge.
> Top solutions may be required to provide training code, checkpoints, dependency files, tokenizer artifacts, parameter counts, optimization logs, and evidence that the submitted model was trained from random initialization.
> Motivation
> A financial sentence can support several locally plausible interpretations.
> The target may be surrounded by multiple values, comparison periods, units, accounting terms, and related events. A nearby noun is not always the correct semantic anchor. The same surface form may describe different concepts in different sentences, while different surface forms may express the same underlying reporting role.
> The practical problem is therefore not merely detecting that an expression is important. It is deciding which structured interpretation should be trusted when several alternatives remain credible.
> A successful system must reason about distinctions such as:
> Current versus non-current obligations.
> Revenue, operating results, profit, and cash movement.
> Basic versus diluted share quantities.
> Absolute values versus per-unit values.
> Closing balances versus changes during a period.
> Rates, margins, ownership percentages, and growth percentages.
> Expenses, liabilities, commitments, and settlements.
> Values associated with different reporting dates or comparison periods.
> This benchmark isolates that arbitration step. The model receives a compact candidate panel and must identify the interpretation that is globally consistent with the target and its context.
> Task
> Each sample contains:
> A unique sample_id.
> A tokenized financial sentence.
> The inclusive start position of a highlighted target.
> The exclusive end position of that target.
> The reconstructed target text.
> Eight opaque candidate interpretation codes.
> The released field containing those codes is named candidate_roles.
> Exactly one candidate is correct.
> Participants submit eight finite numeric scores for every test sample. The highest-scored candidate is treated as the prediction.
> Scores do not need to be probabilities. They do not need to lie between zero and one or sum to one. Scores are compared only within the same sample.
> Prepared Dataset
> The released package contains:
> train.jsonl
> test.jsonl
> roles.json
> sample_submission.csv
> There is no separate validation file. Participants should create a local validation split from train.jsonl.
> The original training and development material is combined into the released training set. Test answers are hidden.
> train.jsonl
> Each line contains one JSON object.
> sample_id
> Type: string.
> A hashed identifier used only for row matching. It must not be used as a predictive feature.
> tokens
> Type: list of strings.
> The tokenized financial sentence. Long sentences may be cropped around the target, but the complete target span is retained.
> target_start
> Type: integer.
> The inclusive token position at which the target begins.
> target_end
> Type: integer.
> The exclusive token position at which the target ends.
> The target occupies the half-open interval from target_start to target_end.
> target_text
> Type: string.
> The target span reconstructed from the released tokens. It is included for convenience and can also be recreated from tokens.
> candidate_roles
> Type: list of eight strings.
> The eight opaque interpretation codes assigned to the sample's candidate panel.
> The list order has no semantic meaning.
> best_candidate
> Type: integer from 1 through 8.
> The position of the correct code inside candidate_roles.
> A value of 1 means that the first candidate is correct. A value of 8 means that the eighth candidate is correct.
> test.jsonl
> The test file contains the same public input fields as train.jsonl, but it does not include best_candidate.
> It does not expose the correct interpretation, readable code meanings, original label identifiers, source row numbers, source split names, candidate difficulty values, or hard-case flags.
> roles.json
> roles.json lists the complete opaque code inventory and the fixed candidate count.
> The codes are not ordered by frequency, similarity, or meaning. No natural-language definitions are provided.
> Participants must infer each code's behavior from its labeled training occurrences and its contrasts with competing candidates.
> Interpretation Panel Construction
> Each correct code is placed in a panel with the seven codes that a training-only lexical reference model treats as its strongest competing interpretations for that specific target and sentence.
> The alternatives are therefore not random distractors. They form a local confusion neighborhood around the example.
> Several candidates may be compatible with the same units or surface shape. They may occur in similar reporting language, share nearby financial terms, or differ only through a distant phrase, target boundary, event type, or reporting period.
> Test selection prioritizes examples where the reference model prefers an incorrect interpretation. Easier examples are retained only when needed to preserve coverage across the hidden code inventory.
> Test examples are also filtered against full-sentence, local-context, and bag-of-context target-masked patterns found in training. This reduces direct phrase-template reuse and emphasizes contextual transfer to unfamiliar formulations.
> Candidate positions are randomized and balanced during preparation, so candidate order is not a useful shortcut.
> Submission Format
> Submit a CSV with exactly these columns in exactly this order:
> sample_id
> candidate_1_score
> candidate_2_score
> candidate_3_score
> candidate_4_score
> candidate_5_score
> candidate_6_score
> candidate_7_score
> candidate_8_score
> The value in candidate_1_score corresponds to the first code in that sample's candidate_roles. The value in candidate_8_score corresponds to the eighth code.
> Example submission:
> sample_id,candidate_1_score,candidate_2_score,candidate_3_score,candidate_4_score,candidate_5_score,candidate_6_score,candidate_7_score,candidate_8_score
> TS_71ab24c0,0.08,0.72,0.14,0.31,0.11,0.93,0.27,0.05
> TS_c83f092e,0.64,0.18,0.06,0.41,0.79,0.12,0.33,0.25
> Every sample_id must appear exactly once. All candidate scores must be finite numeric values.
> Invalid submissions include missing or extra samples, duplicate IDs, missing or extra columns, columns in the wrong order, non-numeric values, missing values, NaN values, and infinite values.
> Tied scores are resolved deterministically by candidate position. Participants should submit distinct scores where possible.
> Evaluation
> Submissions are evaluated using the Strict Context Resolution Score on a scale from 0 to 100. Higher is better.
> The evaluator computes:
> Top1Accuracy
> MeanReciprocalRank
> MacroRoleAccuracy
> TailRoleAccuracy
> HardCaseScore
> The Quality Multiplier is:
> Quality Multiplier = 0.40 + 0.15 × MeanReciprocalRank + 0.15 × MacroRoleAccuracy + 0.15 × TailRoleAccuracy + 0.15 × HardCaseScore
> The final score is:
> Strict Context Resolution Score = 100 × Top1Accuracy × Quality Multiplier
> All five components and the hard-case membership rule are defined below. There are no undisclosed metric weights, role-frequency weights, score transformations, or post-processing steps.
> The multiplicative accuracy gate makes the first choice decisive. Ranking the correct interpretation near the top improves the quality multiplier, but it cannot compensate for repeatedly selecting the wrong candidate.
> Top1Accuracy
> For each sample, the candidate with the highest submitted score is selected.
> Top1Accuracy is the number of exactly correct first choices divided by the total number of evaluated samples.
> Ties are resolved by the original candidate position because the evaluator uses a stable descending sort. Among candidates with identical submitted scores, the candidate appearing earlier in candidate_roles ranks first.
> MeanReciprocalRank
> For each sample, all eight candidates are sorted by submitted score from highest to lowest.
> If the correct candidate appears at rank r, its reciprocal rank is 1 / r.
> A correct candidate ranked first receives 1.0. One ranked second receives 0.5. One ranked eighth receives 0.125.
> MeanReciprocalRank is the arithmetic mean of reciprocal rank over all evaluated samples.
> MacroRoleAccuracy
> Let R be the set of opaque role codes that occur as correct answers in the evaluated test set.
> For each role in R, the evaluator computes Top-1 accuracy using only test samples whose correct answer has that role code.
> MacroRoleAccuracy is the unweighted arithmetic mean of those per-role accuracies.
> Every represented role contributes exactly one equal-weight value, regardless of how many test samples it has. Roles with no correct-answer examples in the evaluated set are not included. No additional frequency weighting, smoothing, or minimum-count rule is applied.
> The correct-answer role codes are hidden during the competition because they are test labels. The formula itself is fully deterministic. Participants can reproduce it exactly on any labeled local validation split by grouping examples by their known correct role code.
> TailRoleAccuracy
> TailRoleAccuracy is calculated from the same per-role Top-1 accuracies used for MacroRoleAccuracy.
> Let R_count be the number of represented correct-answer roles. The evaluator calculates:
> Tail count = max(1, ceil(0.25 × R_count))
> The per-role accuracies are sorted from lowest to highest. TailRoleAccuracy is the arithmetic mean of the first Tail count values.
> There is no hidden definition of a tail role. Tail membership depends only on the submitted predictions and the resulting per-role accuracies. A role can enter or leave the lowest quarter for different submissions.
> For example, when 100 roles are represented, the lowest 25 per-role accuracies are averaged. When 139 roles are represented, the lowest 35 are averaged.
> Deterministic Reference Model
> The hard-case flag is produced once during dataset preparation by a fixed training-only lexical reference model. This reference model is used only to construct and characterize the evaluation data. It is not part of a participant submission and does not change after submissions are received.
> The reference model is a multinomial naive-Bayes scorer with:
> A hashed feature space of 32,768 dimensions.
> Additive smoothing alpha equal to 0.35.
> Role priors estimated from source training-span frequencies.
> Feature likelihoods estimated only from the source training partitions.
> Stable SHA-based feature hashing.
> For a target span, its feature set contains:
> The normalized target-shape category.
> The target token count, capped at eight.
> Up to eight normalized target tokens.
> Normalized context-token presence features within 18 tokens of the target.
> Left-context and right-context token features with distance buckets capped at eight.
> Adjacent context-token bigrams.
> Digits are normalized to #. Four-digit years beginning with 19 or 20 are normalized to <year>. Letter case is removed.
> For each example, the reference model produces one raw score for every opaque role.
> The following deterministic quantities are then calculated:
> true_rank: the one-based rank of the correct role among all 139 role scores, sorted from highest to lowest using stable tie handling.
> margin: the raw score of the correct role minus the highest raw score among all incorrect roles.
> Candidate panel: the correct role together with the seven highest-scoring incorrect roles.
> true_probability: the softmax-normalized support assigned to the correct role within that eight-code candidate panel.
> The softmax is calculated by subtracting the maximum panel score, exponentiating the eight shifted scores, and dividing by their sum.
> HardCaseScore
> A test sample is marked as a hard case when at least one of the following exact conditions is true:
> true_rank is at least 4.
> true_probability is below 0.10.
> margin is below -1.0.
> These thresholds are fixed during preparation and are identical for every submission.
> HardCaseScore is:
> HardCaseScore = 0.80 × HardTop1Accuracy + 0.20 × HardMeanReciprocalRank
> HardTop1Accuracy is Top1Accuracy calculated only over samples whose hard-case flag equals 1.
> HardMeanReciprocalRank is MeanReciprocalRank calculated over the same samples.
> If the prepared test set contains no hard cases, the evaluator uses every test sample for both hard-case components.
> Participants do not receive test hard-case flags because those flags depend on hidden correct roles. However, the membership algorithm is fully disclosed and can be reproduced exactly on a labeled local validation split by fitting the specified reference model on the corresponding local training partition.
> Reproducing the Metric Locally
> To reproduce the complete metric on a labeled validation set:
> Retain the correct role code and correct candidate position for each validation example.
> Calculate Top1Accuracy and MeanReciprocalRank from the submitted candidate scores.
> Group examples by their correct role code to calculate MacroRoleAccuracy.
> Sort the per-role accuracies and average the lowest max(1, ceil(0.25 × R_count)) values for TailRoleAccuracy.
> Fit the disclosed reference model on the local training portion.
> Calculate true_rank, true_probability, and margin for every validation example.
> Apply the three published hard-case conditions.
> Calculate HardCaseScore.
> Apply the published Quality Multiplier and final-score formulas.
> The official evaluator performs the same calculations using the hidden test answers and the hard-case flags generated during official preparation.
> Intended Methods
> The primary model must contain a trainable contextual encoder and must be optimized through gradient-based learning on train.jsonl.
> Eligible approaches include:
> Transformers initialized and trained entirely from scratch.
> Bidirectional recurrent sequence encoders.
> Convolutional sequence models with learned token representations.
> State-space or other neural sequence architectures initialized from scratch.
> Character, byte, word, or subword embeddings learned during challenge training.
> Target-span pooling and learned boundary representations.
> Learned embeddings for the opaque interpretation codes.
> Neural contrastive prototypes.
> Pairwise or listwise neural ranking losses.
> Multi-task contextual, span, and panel-level objectives.
> Ensembles composed only of eligible from-scratch neural models.
> A valid baseline may train a tokenizer on train.jsonl, initialize a compact transformer or bidirectional recurrent model randomly, encode the sentence and highlighted target, and compare the resulting representation with learned code embeddings.
> A stronger system may combine direct neural classification, contrastive code learning, role-balanced optimization, and panel-level ranking.
> Handcrafted numeric-shape, unit, punctuation, and relative-position indicators may be supplied as auxiliary inputs to the neural model. They must not replace the learned contextual encoder or independently determine the final predictions.
> Compute
> The intended environment provides one NVIDIA A10G-class GPU with approximately 24 GB of GPU memory.
> The benchmark is designed for neural models that meaningfully use this compute budget while remaining trainable on a single GPU.
> Practical configurations may include:
> Four to eight transformer layers.
> Hidden dimensions from approximately 256 to 512.
> Learned token and position embeddings.
> Mixed-precision training.
> Dynamic padding.
> Gradient accumulation.
> Shared sentence encoding.
> Character-level or byte-level neural tokenization.
> A subword tokenizer trained only from the released training text.
> Multi-GPU training is not required.
> A solution is not required to consume the entire GPU memory, but it must train a genuine neural predictive model rather than substitute a non-neural heuristic or retrieval pipeline.
> From-Scratch Requirements
> All trainable predictive parameters must be randomly initialized.
> A valid solution must include:
> A trainable neural contextual encoder.
> Trainable token, byte, character, or subword representations.
> Trainable target-span representations.
> Trainable output or opaque-code representations.
> Gradient-based optimization using the released training examples.
> A saved neural checkpoint used to produce the submitted scores.
> The neural model must be the principal source of predictive performance. Auxiliary handcrafted features are allowed only when fused into the neural architecture or used as a minor calibration input.
> Allowed resources include:
> The released challenge files.
> A tokenizer or vocabulary learned only from train.jsonl.
> Fixed character-level or byte-level segmentation rules.
> Public neural architecture implementations without pretrained weights.
> Standard tensor, numerical, and optimization libraries.
> Handcrafted features derived only from released files and used as auxiliary neural inputs.
> Finalists may be asked to demonstrate that removing the neural checkpoint substantially degrades the solution and that the remaining heuristic components cannot independently reproduce the submitted predictions.
> Disallowed Methods
> The following methods are prohibited:
> Pretrained language models, embeddings, encoders, adapters, or checkpoints.
> External corpora used for additional pretraining.
> Teacher predictions or pseudo-labels produced by pretrained systems.
> Externally learned tokenizer vocabularies or embedding tables.
> TF-IDF, BM25, bag-of-words, or lexical-similarity systems used as the primary predictor.
> Logistic regression, linear SVMs, tree ensembles, nearest-neighbor classifiers, or other classical models used as the primary predictor.
> Rule-based scoring, hand-authored phrase dictionaries, frequency lookup tables, or memorized role templates used as the primary predictor.
> Retrieval-only systems that copy labels or scores from similar training examples.
> Ensembles whose performance is primarily produced by prohibited non-neural components.
> Neural models that receive no meaningful training update or whose predictions are effectively determined by fixed heuristics.
> Hidden test answers, leaked labels, or manual test annotation.
> Matching test text against an external copy of the source collection.
> Recovering readable meanings for the opaque code inventory from outside the released files.
> Using sample_id, row order, candidate position, or hard-coded test answers as shortcuts.
> Solutions must learn their primary predictive function through an eligible neural model trained from scratch on the released data.
> Limitations
> The challenge is limited to English professional financial reporting and a fixed hidden interpretation inventory.
> Some codes are more frequent than others, and reporting language can vary across documents. The constructed candidate panels approximate difficult interpretation choices but cannot reproduce every error made by a production extraction system.
> Opaque codes make qualitative analysis less convenient. Models developed for this benchmark may not transfer directly to other languages, accounting regimes, or informal financial writing.
> Expected Outcome
> A successful neural system should learn contextual financial representations from scratch, induce a hidden interpretation schema, resolve close alternatives, transfer beyond repeated report phrasing, and maintain useful performance across its weakest codes.
> The benchmark measures latent-schema induction, contrastive contextual arbitration, and strict panel ranking under a realistic single-GPU budget.
> Submissions
> 32

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Cross-Witness Lacuna Repair in an Opaque Script

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7em80yqdkhyqw09mjhqrp8h58bvyjx
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Medieval books often preserve several witnesses of a short poem. Copyists changed spelling, replaced words, omitted material, and transmitted related lines in different forms. A textual scholar repairing a damaged witness therefore cannot simply copy the visible word at the same position in another manuscript. The surrounding context and recurring substitution patterns across the corpus both matter.
> This challenge presents that problem through an opaque script. Every lexical item has been replaced by an anonymous token such as z004281; these codes have no linguistic meaning outside the supplied data. Each docket contains two complementary lacuna panels. In each panel you receive:
> a damaged query with one <GAP>;
> a related witness passage from another manuscript;
> eight candidate opaque tokens that could fill the gap.
> Recover both missing tokens. The target passages in the evaluation set come from held-out manuscripts, while the visible witness passages come from the known witness tradition. No completed evaluation passage occurs verbatim in either the labeled training dockets or corpus.csv. Panel A uses a substitution pair that does not occur in the labeled training dockets, so it must be recovered from the damaged query's learned language context and the structure of its related witness. Panel B uses a substitution pair observed during training but sampled from an ambiguous family in which one visible witness token has several possible repairs. Success therefore requires both contextual induction and cross-manuscript transfer; exact passage retrieval and a direct substitution dictionary are insufficient.
> This is a from-scratch neural sequence-learning challenge. Pretrained models and external corpora are not allowed.
> What Makes This Different From Ordinary Cloze Recovery
> The lexical inventory is opaque, so pretrained language knowledge cannot supply the answers.
> Every repair is conditioned on a second, related witness rather than on one damaged sequence alone.
> Panel A measures contextual generalization to a substitution pair absent from labeled training dockets; every answer token still occurs in the supplied train-side corpus.
> Panel B measures disambiguation among several repairs previously associated with the same visible witness token.
> Completed evaluation passages are absent from the public corpus and labeled training passages.
> The exact-docket term requires both forms of reasoning to succeed together.
> Task
> For every row in test.csv:
> Read panel A: query_a, witness_a, and candidates_a.
> Select exactly one token from candidates_a for the <GAP> in query_a.
> Repeat for panel B.
> Submit both choices as one repair ledger.
> The required ledger grammar is:
> A=z######|B=z######
> The six # characters represent decimal digits. Candidate order is randomized independently for every panel and carries no target information.
> Dataset
> The public dataset contains four files.
> train.csv: 2,500 labeled two-panel repair dockets, containing 5,000 repair decisions.
> test.csv: 500 unlabeled dockets, containing 1,000 repair decisions from held-out target manuscripts.
> corpus.csv: train-side opaque witness sequences for learning token representations from scratch.
> sample_submission.csv: one valid example prediction for every test docket.
> train.csv Columns
> case_id (string): anonymous docket identifier.
> query_a (string): whitespace-separated opaque tokens for panel A with exactly one <GAP>.
> witness_a (string): related complete witness sequence for panel A.
> candidates_a (string): eight unique space-separated opaque tokens allowed for panel A.
> query_b (string): whitespace-separated opaque tokens for panel B with exactly one <GAP>.
> witness_b (string): related complete witness sequence for panel B.
> candidates_b (string): eight unique space-separated opaque tokens allowed for panel B.
> repair_ledger (string): target ledger in the form A=z######|B=z######.
> test.csv Columns
> case_id (string): anonymous docket identifier.
> query_a (string): damaged panel-A sequence.
> witness_a (string): related panel-A witness sequence.
> candidates_a (string): eight allowed panel-A tokens.
> query_b (string): damaged panel-B sequence.
> witness_b (string): related panel-B witness sequence.
> candidates_b (string): eight allowed panel-B tokens.
> test.csv omits repair_ledger.
> corpus.csv Columns
> sequence_id (string): anonymous train-side witness identifier.
> token_sequence (string): complete whitespace-separated opaque token sequence.
> sample_submission.csv Columns
> case_id (string): test docket identifier.
> repair_ledger (string): one panel-A and one panel-B candidate in the required grammar.
> The same opaque token code always denotes the same train-vocabulary item. zUNK marks a non-target item outside the train vocabulary. It never appears as a valid repair candidate.
> Evaluation
> The score is bounded in [0, 1], and higher is better.
> For each docket, let correct_A equal 1 when the submitted panel-A token is correct and 0 otherwise. Define correct_B in the same way.
> GapTokenAccuracy = sum(correct_A + correct_B) / (2 * number_of_dockets)
> ExactDocketAccuracy = number_of_dockets_with_both_tokens_correct / number_of_dockets
> The final score is:
> Score = 0.45 * GapTokenAccuracy + 0.55 * ExactDocketAccuracy
> Each component appears exactly once in this formula. A perfect submission scores 1.0.
> Submission
> Submit a CSV with exactly two columns: case_id and repair_ledger.
> Example header and row:
> case_id,repair_ledger
> DCKTST_31f6a8ce9b07d2,A=z001842|B=z000317
> Submission rules:
> Include every required case_id exactly once.
> Use exactly A=z######|B=z######; do not add spaces or commentary.
> The panel-A token must be one of that row's candidates_a values.
> The panel-B token must be one of that row's candidates_b values.
> Nulls, duplicate IDs, malformed ledgers, missing IDs, extra columns, and out-of-candidate tokens are invalid.
> Allowed And Prohibited Methods
> Allowed:
> Neural sequence models initialized from random weights.
> Tokenizers and vocabularies learned only from the supplied public files.
> Self-supervised pretraining on corpus.csv.
> Validation grouped by the patterns available in the public data.
> Prohibited:
> Pretrained language models, pretrained embeddings, or pretrained tokenizers.
> External corpora, manuscript databases, source matching, or attempts to decode the anonymous token vocabulary.
> Hardcoded test labels, row-order shortcuts, source-path recovery, or manually authored lookup tables.
> A heuristic-only or non-ML system used as the primary solver.
> Submissions
> 24

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Portal Leaf Fault Trace Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7d3qa94zcrvzk0wn3f4hfkxh8bj4af
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: medical, large-scale, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.596

Full challenge description from page:

> Portal Leaf Fault Trace Recovery
> Overview
> Radiotherapy treatment machines shape each beam with two moving banks of multileaf collimator leaves. In this synthetic QA benchmark, a planned aperture delivery is paired with simulated portal fluence arrays after hidden leaf-bank faults have been applied. Small leaf-bank faults can produce clinically meaningful dose-like fluence differences, but the measured arrays alone do not directly reveal which leaf, bank, time interval, and signed motion caused the discrepancy.
> Each example contains a planned dynamic aperture tensor and a twelve-frame, three-channel portal fluence tensor. For each control point, the portal channels are the expected fluence, the measured fluence after three hidden machine faults, and a centered residual array. Your task is to estimate the three hidden structured fault records that explain the measured portal fluence.
> This is a GPU From-Scratch benchmark for structured physical-parameter recovery. It is not fluence prediction, treatment-plan optimization, scalar gamma-pass prediction, or ordinary MLC error classification. Strong solutions should build custom aperture/fluence reasoning, aggregate residual evidence over leaf-time coordinates, and decode three fixed-size fault records.
> Target Parameters
> The submission stores the three fixed-size fault records in the fault_trace CSV field. This field is a compact serialization of structured categorical and ordinal parameters. Every submitted value must contain exactly three fault records in canonical order by start control point, then leaf index, then bank:
> BEGIN E1 <op> <bank> <leaf> <start> <length> <delta> E2 <op> <bank> <leaf> <start> <length> <delta> E3 <op> <bank> <leaf> <start> <length> <delta> END
> Allowed operation values:
> | Operation | Meaning |
> |---|---|
> | SHIFT | The selected leaf-bank boundary is displaced by the signed delta for the full interval. |
> | DRIFT | The selected boundary ramps from a one-column displacement toward the signed delta over the interval. |
> | LAG | The selected boundary follows an earlier control-point position with the signed residual delta. |
> | BACKLASH | The selected boundary initially sticks, then catches up toward the signed delta late in the interval. |
> Other parameter values:
> | Field | Allowed values | Meaning |
> |---|---|---|
> | bank | BA, BB | Left-bank or right-bank boundary. |
> | leaf | L01 through L14 | Addressable interior leaf row. The stored aperture grid has 16 rows; rows 0 and 15 are guard rows and are never selected as fault origins. |
> | start | T00 through T10 | First affected control point. Valid starts also depend on length: Q02 allows T00T10, Q03 allows T00T09, Q04 allows T00T08, and Q05 allows T00T07. |
> | length | Q02 through Q05 | Number of affected consecutive control points. The decoded zero-based interval [start, start + length) must stay inside the 12 control points. |
> | delta | DN04, DN03, DN02, DN01, DP01, DP02, DP03, DP04 | Signed boundary displacement in aperture-grid columns. |
> The planned aperture tensor has 12 control points, 16 stored leaf rows, and 48 columns. Fault records may target only the 14 interior rows L01 through L14; the outer rows are retained in the arrays as guard rows for aperture geometry. A fault edits one bank boundary for one interior leaf row over one time interval, then the faulty aperture tensor is rendered into portal fluence. Some deliveries also include small neighboring-leaf coupling with randomized coupling strength and low-frequency detector artifacts, so solvers must separate recoverable fault parameters from portal measurement nuisance structure.
> Evaluation
> The score is maximized and ranges from 0 to 1. Structurally invalid submissions, such as missing IDs or wrong columns, are rejected. A malformed fault_trace serialization receives zero row credit.
> For each row:
> row_score =
> 0.45 * exact_trace
> + 0.30 * ordered_field_accuracy
> + 0.05 * ordered_leaf_time_proximity
> + 0.20 * best_matched_physical_similarity
> exact_trace is 1 only when all three fault records match exactly. ordered_field_accuracy is the fraction of operation, bank, leaf, start, length, and delta fields that match in the three ordered records. ordered_leaf_time_proximity gives partial credit for nearby leaf rows and overlapping time intervals at the same ordered position. best_matched_physical_similarity matches predicted fault records to gold records without requiring the same order and combines operation, bank, leaf proximity, interval IoU, and signed-delta closeness.
> The final score is the mean row score over all test examples.
> The provided sample_submission.csv is a valid constant-format baseline, not a zero baseline. On the hidden test set it scores 0.17934280498866212, mostly from incidental partial field matches.
> Dataset
> Public files:
> | File | Shape or rows | Dtype | Description |
> |---|---:|---|---|
> | train.csv | 2400 rows | CSV | Training IDs, aperture constants, and gold structured fault records serialized in fault_trace. |
> | test.csv | 700 rows | CSV | Test IDs and aperture constants without labels. |
> | sample_submission.csv | 700 rows | CSV | Valid constant-format submission template. |
> | train_plans.npy | (2400, 12, 16, 48) | uint8 | Planned binary aperture masks in train row order. |
> | test_plans.npy | (700, 12, 16, 48) | uint8 | Planned binary aperture masks in test row order. |
> | train_portal.npy | (2400, 12, 96, 96, 3) | uint8 | Training portal fluence tensors in train row order. |
> | test_portal.npy | (700, 12, 96, 96, 3) | uint8 | Test portal fluence tensors in test row order. |
> The dataset is synthetic. It does not contain patient records, clinical treatment plans, or measured hospital portal acquisitions.
> Portal tensor axes are:
> sample, control_point, detector_y, detector_x, channel
> Portal channel order:
> expected_fluence measured_fluence centered_residual
> The first two channels are scaled fluence arrays on 0..255. The third channel stores the centered measured-minus-expected residual, also on 0..255.
> CSV Columns
> train.csv columns:
> | Column | Type | Meaning |
> |---|---|---|
> | id | string | Unique sample ID. |
> | n_control_points | integer | Always 12. |
> | n_leaves | integer | Always 16 stored rows, with fault origins restricted to interior rows L01 through L14. |
> | n_columns | integer | Always 48. |
> | fault_trace | string | Gold serialization of three fixed-size fault records. |
> test.csv contains the first four columns only.
> Submission
> Submit exactly these columns, in this order:
> id,fault_trace
> test_9e710c65e91c8196,BEGIN E1 SHIFT BA L07 T02 Q04 DP01 E2 DRIFT BB L08 T04 Q03 DN02 E3 BACKLASH BA L10 T07 Q03 DP03 END
> test_12d15cd45b7d9a52,BEGIN E1 LAG BB L04 T01 Q05 DP01 E2 SHIFT BA L12 T05 Q03 DN04 E3 DRIFT BA L03 T08 Q02 DP02 END
> Requirements:
> Include exactly one row for every test ID.
> Use the exact column order shown above.
> Each fault_trace value must contain exactly three fault records and the required BEGIN, E1, E2, E3, and END markers.
> Use only the allowed parameter values and keep records in canonical order.
> Missing values, duplicate IDs, extra IDs, extra columns, invalid values, invalid intervals, or malformed serializations are rejected or receive zero row credit as described above.
> Save the file as ./working/submission.csv.
> Restrictions
> Use only the released public files and generally available methods. Do not use private answers, row order, file order, hashes, generated IDs, private generator state, or grader internals. From-scratch aperture renderers, differentiable or heuristic search, structured parameter decoding, ensembling, and learned residual aggregation are allowed.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Thai–English Grapheme Streams

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ekztt24re9dy9g7s50w03rx8c5pyj
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; challenge detail page timed out
- Difficulty: Medium
- Compute: Not displayed; challenge detail page timed out
- GPU: Not displayed; challenge detail page timed out
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage card score context: Beat ninjastar69's score of 0.768!

Full challenge description from page:

> Background Scene-text recognition in multilingual environments presents unique computer vision and natural language processing challenges. In regions like Thailand, everyday signage, commercial storefronts, traffic notices, and consumer packaging regularly interweave the Thai script, Latin alphabet, Arabic numerals, and diverse punctuation marks within single lines of text. Unlike Latin-based scripts that follow a linear horizontal sequence of discrete characters separated by regular spaces, Thai is an abugida script characterized by complex multi-tiered orthography: Vertical Vowel and Tone Stacking: Vowels, tone marks, and diacritics can appear above, below, before, or after base consonants across four distinct horizontal display tiers. Absence of Word Boundaries: Thai text is written continuously without spaces between words; spaces are reserved primarily to denote clause, sentence, or phrase boundaries. Multiscript Interleaving: Sentences frequently transition dynamically between Thai phonology and English brand names, loanwords, or acronyms within a single text stream. Standard character-level tokenization frequently fractures Thai characters into non-renderable codepoints. Framing transcription around extended Unicode grapheme clusters ensures that visually and phonologically unified orthographic units—including base consonants combined with their suprasegmental tone marks and diacritics—are recognized and evaluated as coherent linguistic units. Overview The Thai–English Grapheme Streams challenge tasks you with transcribing cropped scene-text images containing Thai, English, digits, and mixed scripts directly into ordered streams of NFC-normalized Unicode grapheme clusters. Given an RGB image crop of fixed height (48 pixels) and variable width (up to 768 pixels), your solution must output an ordered JSON array of strings, where each element represents exactly one extended Unicode grapheme cluster. This is a GPU-only, train-from-scratch benchmark. You must initialize all neural weights randomly and train your architecture on CUDA within the evaluation environment using only the supplied training samples. The complete offline pipeline—preprocessing, training, inference, and submission generation—must execute within a strict 90-minute budget on a single NVIDIA A10G GPU. Dataset Information (Public Files) All participant-facing assets are provided in the public/ directory. The dataset contains 3,925 supervised training examples and 1,007 evaluation cases. Plaintext +-----------------------+--------------------------------------------------------------+ | File / Directory | Description | +-----------------------+--------------------------------------------------------------+ | images/ | Directory containing cropped RGB PNG images (height = 48 px).| | train.csv | Supervised training set with IDs, image paths, and targets. | | test.csv | Evaluation set containing IDs and image paths without targets| | sample_submission.csv | Template demonstrating the required CSV submission format. | +-----------------------+--------------------------------------------------------------+ Feature Schema train.csv and test.csv Plaintext +-----------+--------+-----------------------------------------------------------------+ | Column | Type | Description | +-----------+--------+-----------------------------------------------------------------+ | id | String | Opaque unique case identifier (24-character hex string). | | image | String | Relative path to the image crop (e.g., images/.png). | | graphemes | JSON | (train.csv only) JSON array of Unicode grapheme cluster strings.| +-----------+--------+-----------------------------------------------------------------+ Split and Generalization Guarantee To ensure the evaluation metric measures genuine optical character recognition (generalization) rather than string memorization, strict boundaries were enforced during the creation of the train and test splits: Transcription Isolation: All native transcriptions were case-folded and normalized into unified groups. The splits were assigned based on these groups. If a specific phrase or word appears in the evaluation set, it is mathematically guaranteed not to appear anywhere in the training set. Visual Hash De-duplication: To prevent visual leakage where nearly identical physical signs span both splits, a perceptual hashing algorithm (scipy.ndimage) scanned all images. Any training image with a perceptual hash collision (fewer than 12 pixel differences on a $17 \times 16$ spatial grid) against the test set was permanently purged. This guarantees that solutions must learn the underlying orthography rather than memorizing frequent phrases or visually matching duplicate crops. Image Specifications & Text Representation Image Dimensions: All images are normalized to a uniform vertical height of 48 pixels. Image widths vary proportionally according to text length, ranging between 8 and 768 pixels (aspect-ratio preserved using Lanczos resampling). Target Cluster Boundaries: Target annotations contain up to 160 grapheme clusters. Each string in the array corresponds to exactly one extended grapheme cluster matching the Unicode regular expression \X under Canonical Composition (NFC). Spacing and Punctuation: Spaces, Latin letters, Arabic numerals, and punctuation symbols are distinct individual grapheme clusters. Data Sanitization: Ambiguous transcriptions (e.g., filenames with sanitized underscore punctuation) and visually confirmed native label mismatches have been excluded to preserve ground-truth fidelity. Evaluation Metrics Submissions are evaluated on character-level structural accuracy using the Normalized Levenshtein Similarity over NFC-normalized grapheme cluster sequences. 1. Grapheme Normalization & Validation Before computing distances, every predicted cluster $g$ is converted into Unicode Normalization Form C (NFC). Each element must constitute exactly one extended grapheme cluster (\X) and contain no ASCII or Unicode control characters (Cc). 2. Levenshtein Edit Distance Let $P = [p_1, p_2, \dots, p_{\vert{}P\vert{}}]$ denote the sequence of predicted grapheme clusters, and let $T = [t_1, t_2, \dots, t_{\vert{}T\vert{}}]$ denote the ground-truth target sequence. The edit distance $D(P, T)$ is computed using standard unit costs: Insertion: Cost = 1 Deletion: Cost = 1 Substitution: Cost = 1 (if $p_i \ne t_j$) Case and punctuation are strictly evaluated: capitalization differences in Latin letters (e.g., "A" vs. "a") and distinct punctuation marks count as substitutions. 3. Row Score For each individual image row, the score measures the normalized edit similarity: $$\text{Row Score} = \max\left(0.0,\, 1.0 - \frac{D(P, T)}{\max(1, \vert{}T\vert{})}\right)$$ If the predicted grapheme list matches the target sequence perfectly ($D(P, T) = 0$), the row receives a score of 1.0. If the edit distance equals or exceeds the length of the ground-truth sequence $\vert{}T\vert{}$, the score floors at 0.0. An empty prediction paired with an empty target scores 1.0. 4. Final Score The overall competition metric is the arithmetic mean of the row scores across all 1,007 evaluation cases: $$\text{Final Score} = \frac{1}{N} \sum_{k=1}^N \text{Row Score}_k$$ The score is bounded within $[0.0, 1.0]$, where higher is better. Sample Submission Format Submit a UTF-8 encoded CSV file with exactly two columns in this order: id,graphemes. Every evaluation ID from test.csv must appear exactly once. The graphemes column must contain a JSON-encoded list of strings. Use standard CSV quoting rules (wrapping JSON strings in double quotes and escaping internal quotes with ""). Code snippet id,graphemes 00a12f5d78b9412c90e53a10,"[""ก"",""า"",""ร"",""ท"",""ด"",""ล"",""อ"",""ง""]" 01b89c4e22f719aa0182dd45,"[""T"",""e"",""s"",""t"","" "",""1"",""2"",""3""]" 02c34a1b90f482bb7763ef11,"[]" Structural Limits & Parsing Rejection Rules ID Set Integrity: The file must contain the exact set of test IDs with no duplicates, omissions, or extraneous rows. An invalid ID set invalidates the entire submission (scores 0.0). Length Limits: The JSON string in graphemes must not exceed 30,000 characters. Cluster Capacity: A single prediction list may contain at most 320 grapheme strings. Grapheme Conformance: Each string must have a length of at most 32 code points, must match exactly one extended grapheme cluster (len(regex.findall(r'\X', g)) == 1), and must not contain any control characters (Cc). Row-Level Penalties: A malformed JSON string, illegal schema, out-of-bounds cluster length, or invalid grapheme token scores 0.0 for that specific row; remaining valid rows are graded normally. What Not To Use To guarantee a fair evaluation of architecture design and training efficiency from raw pixels, the following approaches are strictly prohibited: No Pretrained Weights or Embeddings: Do not use pretrained vision backbones, linguistic checkpoints, or OCR weights (e.g., ImageNet checkpoints, TrOCR, CRNN pre-trained weights, PaddleOCR, CLIP, DINO, or Vision Transformers trained on external corpora). All network weights must be initialized randomly. No Pretrained Tokenizers or Dictionaries: Tokenizers, vocabularies, and character dictionaries must be constructed strictly from the provided public training set. No External Data or Synthetic Generators: Do not ingest external font collections, synthetic text generators (e.g., SynthText, TextRecognitionDataGenerator), or external bilingual corpora. No Source Reverse-Engineering: Do not scrape, download, or cross-reference files from the upstream Thai–English Multiscript Text Image (TEMS) repository. No CPU-Only Predictors: Purely rule-based heuristics or CPU-only architectures are invalid. No Test-Time Transduction: Test images may only be processed during forward inference. Test-set pseudo-labeling, transductive normalization, and test-time training routines are prohibited. &nbsp;
> $700 Pool
> 2 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Meteorological Station Neighborhood Inference

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx729x31nt6xt5psxtn21hsr7s8bwt65
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; challenge detail page timed out
- Difficulty: Hard
- Compute: Not displayed; challenge detail page timed out
- GPU: Not displayed; challenge detail page timed out
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage card score context: Beat dev_natha's score of 0.347!

Full challenge description from page:

> Meteorological Station Neighborhood Inference Overview Surface-weather reports can arrive late or contain missing fields. Nearby stations provide useful evidence because wind, temperature, moisture, and pressure vary coherently across local weather systems. Each example is a 54 x 54 numeric neighborhood array containing eight encoded station-model reports around a masked center position. Predict five binned fields for the hidden center station: wind direction, wind speed, air temperature, dewpoint, and pressure. This is a CPU from-scratch benchmark. Train models or feature pipelines directly on the provided arrays and labels. Files | File | Shape / rows | Description | |---|---:|---| | train_images.npy | (5000, 54, 54) | Training neighborhood arrays stored as uint8. | | test_images.npy | (1200, 54, 54) | Test neighborhood arrays stored as uint8. | | train.csv | 5,000 | Training IDs and five target columns. | | test.csv | 1,200 | Test IDs in the same order as test_images.npy. | | sample_submission.csv | 1,200 | Valid submission template. | Array axis order is (example, row, column). Values range from 0 to 255; lower values represent darker encoded station marks. Row i of each array corresponds to row i of its CSV file. Columns | Column | Type and range | Description | |---|---|---| | id | string | Opaque example identifier. | | wind_dir_sector | integer, 0-7 | Wind direction sector, ordered clockwise in 45-degree bins. | | wind_speed_bin | integer, 0-7 | Wind speed bucket, ordered from calm/light to strongest. | | temp_bin | integer, 0-11 | Air-temperature bucket, ordered from coldest to hottest. | | dewpoint_bin | integer, 0-11 | Dewpoint bucket, ordered from driest/coldest to warmest/most humid. | | pressure_bin | integer, 0-9 | Altimeter-pressure bucket, ordered from lowest to highest. | train.csv contains all six columns. test.csv contains only id. sample_submission.csv contains id followed by the five prediction columns. Split Design The split is grouped by the masked center station and its observation event. No target station or target station-time event appears in both train and test, and every test row uses a distinct target station and event. This prevents exact target-station or repeated-event memorization. Examples may still come from the same broad observation window, so performance measures transfer to unseen stations within that weather snapshot rather than transfer across seasons. Reviewer-only opaque group and time fields are retained for auditing but are excluded from every solver-visible file. Evaluation For each target field, field accuracy is the fraction of test rows predicted exactly. The weighted field accuracy is: weighted_field_accuracy = 0.24 * wind_dir_sector_accuracy 0.22 * wind_speed_bin_accuracy 0.20 * temp_bin_accuracy 0.18 * dewpoint_bin_accuracy 0.16 * pressure_bin_accuracy exact_row_accuracy is the fraction of test rows where all five fields are correct. The final score is: final_score = 0.92 weighted_field_accuracy + 0.08 exact_row_accuracy The field weights prioritize the two local wind quantities, followed by the coupled temperature and dewpoint fields. Pressure receives the smallest field weight because it is typically smoother across nearby stations and has the most concentrated marginal distribution in this build. The 0.92 field component measures useful per-variable inference, while the 0.08 exact-row component rewards coherent joint predictions without dominating the score. These weights define this benchmark's evaluation priorities; they are not operational safety weights. The score is maximized and ranges from 0 to 1. Measured reference scores on this exact split are: | Submission | Score | |---|---:| | Uniform random labels, mean over 1,000 fixed seeds | 0.0967 | | All-zero sample submission | 0.1062 | | Per-field modal constant learned from train.csv | 0.1729 | | Local feature-neighbor baseline using only public files | 0.2225 | Compute The full public arrays occupy about 18 MB uncompressed. Classical feature methods and compact neural models fit comfortably within the CPU tier. Submission Format Submit exactly 1,200 rows with these columns in this order: id,wind_dir_sector,wind_speed_bin,temp_bin,dewpoint_bin,pressure_bin test_0000000000000000,3,4,7,6,5 Every test ID must appear exactly once. Prediction values must be integers in the documented ranges. Missing values, duplicate IDs, extra IDs, extra columns, and out-of-range labels are invalid. Save the file as ./working/submission.csv. Rules Use only train_images.npy, test_images.npy, train.csv, test.csv, and sample_submission.csv. Do not use outside weather archives, raw report feeds, station metadata, observation times, coordinates, source lookup, private labels, or grader internals. The public files intentionally omit source station identifiers, timestamps, coordinates, raw reports, and split-provenance fields. &nbsp;
> $700 Pool
> Ranks finalizing

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Reassemble Interleaved Handwritten Line Strips

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74vrfkcfrpdhc6yd2jvm481n8dw0wg
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat neutro's score of 0.489!

Full challenge description from page:

> Background In digital document recovery and historical forensics, fragmented documents often lose their original spatial context and orientation. Recovering the original text requires parsing disorganized image fragments, establishing reading-order continuity across torn edges, and deciphering the underlying handwriting. Physical stroke continuity aids in bridging cuts through letters, while linguistic syntax and handwriting styles provide evidence for cuts through whitespace. Overview Recover readable handwritten lines from a shuffled mixture of narrow image strips. A given packet contains pieces of two or three real handwritten lines (German language) originating from the same page. Individual pieces may be upside down. The objective is to partition the strips into their original lines, arrange each line's pieces into reading order, turn them upright (0 or 180 degrees), and accurately transcribe the reconstructed line. Every piece of each selected line is present in the packet; there are no blank regions to hallucinate. Line order within the final output is irrelevant, but the internal ordering and orientation of strips within each line are essential. This is a From Scratch challenge. Initialize all weights randomly and train the visual neural architecture within a single offline script using one NVIDIA A10G. The complete run, including preprocessing, training, inference, and writing the submission, must finish within 90 minutes. Dataset Information (Public Files) The dataset comprises handwritten German text with occasional foreign names, symbols, and punctuation. The public directory contains all files necessary for local development and prediction. Inputs consist of 8 to 18 total strips per packet (4 to 6 strips per line). Original aspect ratios differ, and each strip is resized to a common 128×64 pixel shape. Mild Gaussian noise, intensity quantization, and sparse white-pixel dropouts have been applied. +-----------------------+--------------------------------------------------------------+ | File / Directory | Purpose | +-----------------------+--------------------------------------------------------------+ | strips/ | Directory of 128x64-pixel grayscale PNG images. | | train.csv | Packets of shuffled strips with target line annotations. | | test.csv | Packets of shuffled strips requiring reconstruction. | | sample_submission.csv | Empty format demonstration for evaluations. | +-----------------------+--------------------------------------------------------------+ Feature Schema train.csv and test.csv +--------------+---------+-------------------------------------------------------------+ | Column | Type | Description | +--------------+---------+-------------------------------------------------------------+ | id | String | Opaque packet identifier. | | strips_json | JSON | Array of relative image paths for the packet's strips. | | target_json | JSON | (train.csv only) Structured target reconstruction. | +--------------+---------+-------------------------------------------------------------+ Target JSON Schema The target_json contains exactly one key, lines, whose value is a nonempty array. Each reconstructed line object requires these precise fields: tiles: A nonempty array of distinct integer strip indices (based on their position in strips_json, counted from 0), arranged in left-to-right reading order. turns: An integer array of the same length as tiles; each value must be 0 or 180, representing the counterclockwise rotation applied to make the observed strip upright. text: The full line transcription (a nonempty Unicode string of at most 200 characters, devoid of control characters). All strip indices must appear exactly once across the output lines. A single line can contain at most 24 strips, and the output can contain at most 24 lines. These generous limits allow imperfect partitions to receive partial credit. Generalization & Leakage Controls To prevent architectural memorization and guarantee evaluation on unseen handwriting styles, strict leakage controls are applied during preparation as this will help in understanding what exactly is the aim of this challenge: Source Grouping: Documents are clustered into "families" via the union of full-page origins, article URLs, demographic pairs (gender and year of birth), and exact repeated line texts. Strict Isolation: Entire families are held out for the test split. No single source page or demographically paired writer crosses the train/test boundary. Target Fidelity: Known annotation errors in the native dataset remain uncorrected; the benchmark strictly tests alignment with the supplied human annotations, not ground-truth linguistic perfection. Evaluation Metrics Reconstructions are evaluated on a combined metric assessing structural alignment (grouping, order, orientation) and transcription accuracy. 1. Normalized Similarity Let an oriented chain be a sequence of tuples [(tile_index, turn), ...]. Let $d(a, b)$ be the unit-cost Levenshtein edit distance, applied either to the chain's oriented tokens or to the transcription's Unicode characters. The normalized similarity is defined as: $$\text{Similarity}(a, b) = 1 - \frac{d(a, b)}{\max(\vert{}a\vert{}, \vert{}b\vert{})}$$ (Matching empty sequences score $1.0$; an empty sequence versus a nonempty sequence scores $0.0$.) 2. Line Reward For a predicted line $p$ and a reference line $t$, the reward is the product of their chain similarity and text similarity: $$\text{Reward}(p, t) = \text{Similarity}(p_{\text{chain}}, t_{\text{chain}}) \times \text{Similarity}(p_{\text{text}}, t_{\text{text}})$$ (Transcriptions are normalized to Unicode NFC with collapsed whitespace runs before comparison; casing and punctuation remain significant.) 3. Packet Score The evaluator computes a maximum-weight one-to-one assignment $M$ between predicted lines ($P$) and target lines ($T$). Unmatched lines receive $0.0$. $$\text{Packet Score} = \frac{2 \sum_{(p,t) \in M} \text{Reward}(p, t)}{\vert{}P\vert{} + \vert{}T\vert{}}$$ The final competition score is the unweighted arithmetic mean over all test IDs. Scores are maximized in [0, 1]. Sample Submission Format Write a UTF-8 CSV with exactly the columns id,target_json in that order. Include every test ID exactly once. The JSON limit is 20,000 characters per row. id,target_json example_id,"{""lines"":[{""tiles"":[3,0,2,1],""turns"":[0,180,0,180],""text"":""Eine kurze handschriftliche Zeile.""},{""tiles"":[6,4,7,5],""turns"":[180,0,0,0],""text"":""Hier beginnt eine zweite Zeile.""}]}" Parsing Bounds & Rejection: Malformed JSON, duplicate JSON keys, extra target fields, invalid rotation values, missing/repeated strip indices, invalid text, or oversized row JSON assigns 0.0 to that specific row. Wrong CSV columns/order, malformed quoting, missing/extra/duplicate IDs, an incorrect row count, or a CSV file larger than 64,000,000 bytes yields 0.0 for the entire submission. What Not To Use To ensure equitable assessment of training efficiency and algorithmic design: No Pretrained Weights: No pretrained encoders, external text corpora, or source archive copies are allowed. No External Services: No internet access, hosted APIs, reverse image search, or manual annotation of test packets. No Test-Time Transduction: Do not train on test data, generate test pseudo-labels, fit preprocessing to test statistics, or perform test-time adaptation. Use test excerpts only for forward inference. (Label-preserving augmentation of training images is permitted.) No Source Reverse-Engineering: No prediction based on IDs, filenames, or row order. No Heuristics-Only Solutions: A rules-only or retrieval-only reconstruction without a trained visual neural architecture is not compliant. You must train the architecture inside the submission script. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Grain Contact Separation from Images

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx794w1x5p3x7h0pqp1jmr7fp58dr6wj
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat demon's score of 0.811!

Full challenge description from page:

> Grain Contact Separation from Images Background In granular physics, geology, and material science, analyzing the contact networks of sediment assemblies or particle aggregates is crucial for understanding structural stability, force transmission, and porosity. Extracting these relationships directly from images involves moving beyond simple object detection to rigorous topological reasoning. When a specific subset of particles is identified, determining the pathways of contact between them allows researchers to simulate material failure or permeability. By pinpointing the critical "bottleneck" grains—those whose removal breaks the continuous chain of contact across a sample—we can identify structural vulnerabilities entirely through visual inspection. Overview The Grain Contact Separation challenge tasks you with recovering the near-boundary contact graph of marked sediment grains in an image, and subsequently choosing a small set of grains whose removal completely disconnects marked grain 0 from marked grain 1. Here, contact has a precise two-dimensional image definition: the minimum Euclidean distance between pixels belonging to two annotated grains is at most four pixels in the supplied $512 \times 512$ coordinate system. It is a near-boundary relationship in a projected image, not a measurement of mechanical forces or three-dimensional physical contact. Your model must: Process a $512 \times 512$ image alongside a set of seed coordinates locating the marked grains. Predict the undirected contact graph (edges) between these specific grains. Identify a valid "removal set" (a list of non-terminal grains) that breaks all paths between grain 0 and grain 1 in the true underlying graph. You must train a visual model from random initialization in a single submitted script. The absolute budget is 90 minutes total on one NVIDIA A10G, which strictly includes preprocessing, training, inference, and output generation. Dataset Information (Public Files) All participant-facing data is stored in the public/ directory. Related source collections are strictly partitioned so that they do not cross the train/test split. +-----------------------+--------------------------------------------------------------+ | File / Directory | Description | +-----------------------+--------------------------------------------------------------+ | images/ | Directory containing RGB PNG images of size 512 x 512. | | train.csv | Training set containing images, seeds, and ground-truth JSON.| | test.csv | Evaluation set containing inputs without targets. | | sample_submission.csv | Template showing the required CSV submission format. | +-----------------------+--------------------------------------------------------------+ Feature Schema train.csv and test.csv +---------+--------+-------------------------------------------------------------------------+ | Feature | Type | Description | +---------+--------+-------------------------------------------------------------------------+ | id | String | Opaque case identifier. | | image | String | Relative path to the visual asset (e.g., images/.png). | | seeds | JSON | Array of integer pairs representing a point inside each marked grain. | | | | Ordered [x, y], with both coordinates in [0, 511]. The array index | | | | corresponds to the grain ID. Grains 0 and 1 are fixed terminals. | | target | JSON | (train.csv only) Object containing the ground-truth contacts list | | | | and an optimal remove list. | +---------+--------+-------------------------------------------------------------------------+ Image Perturbations Images contain real sediment particles derived from photographic and CT section imagery. To prevent trivial thresholding and overfitting, inputs undergo aggressive dynamic perturbations designed to obscure high-frequency boundary details: Random Gaussian Blur: A $5 \times 5$ blur filter is applied with a dynamically sampled radius ($\sigma \in [1.0, 2.5]$) to make touching and near-touching boundaries highly ambiguous. Gaussian Sensor Noise: High-intensity additive noise ($\sigma \approx 0.06$). Harsh Intensity Quantization: Image values are binned to a 4-bit equivalent (15 discrete levels) to destroy subtle gradient and shading cues between grains. Heavy Spatial Context Dropout: Twelve large, randomized black occlusion patches ($32 \times 32$ pixels each) are applied to force the model to infer massive missing sections of the contact graph. Note: The clean native annotation still defines the target, regardless of localized dropouts or boundary obfuscation. Evaluation Metrics For each row, the evaluation calculates a Contact Score ($F$) and a Separation Score ($C$). 1. Contact Score ($F$): Measures the F1 score of the predicted edge set ($P$) against the ground-truth annotated edge set ($T$). $$F = \frac{2 \times \vert{}P \cap T\vert{}}{\vert{}P\vert{} + \vert{}T\vert{}}$$ (If both edge sets are empty, $F = 1.0$. If exactly one is empty, $F = 0.0$.) 2. Separation Score ($C$): Let $R$ be the submitted removal set and $k^$ be the minimum number of non-terminal vertices required to disconnect vertex 0 and vertex 1 in the *annotated (ground-truth)** graph. $$C = \frac{k^*}{\vert{}R\vert{}}$$ (This applies only if $R$ is nonempty and successfully disconnects the terminals in the true graph. Otherwise, $C = 0.0$.) Final Row Score: The row score combines the graph accuracy and the separation efficiency: $$\text{Row Score} = 0.6 \times F + 0.4 \times C$$ The overall Final Score is the arithmetic mean of the row scores across all test cases. The maximum possible score is 1.0. Sample Submission Format Submit a CSV file with exactly two columns, in this order: id, target. Include each test ID exactly once. The target column must contain a strictly formatted JSON string with exactly two keys: contacts and remove. contacts: A list of distinct undirected edges [a, b] with integer indices $0 \le a < b < N$. No self-loops or repeated edges are allowed. (Maximum 496 edges). remove: A list of distinct integer indices representing the grains to remove. Must be in the range $[2, N-1]$ (you cannot remove terminals 0 or 1). (Maximum 30 removals). id,target example_case_1,"{""contacts"":[[0,2],[1,3],[2,3]],""remove"":[2]}" example_case_2,"{""contacts"":[],""remove"":[]}" Note: Any malformed target, duplicate/out-of-bounds index, or extra JSON key will result in a $0.0$ for that row. Violating the CSV schema limits will fail the entire submission. What Not To Use To ensure a fair evaluation of model architecture and training efficiency, the following are strictly prohibited: No External Data or Weights: Do not use external datasets, pre-trained image embeddings (e.g., ImageNet weights, CLIP), hosted APIs, or web access. The model must be trained entirely from scratch. No Source Exploitation: Do not attempt source archive matching, reverse image search, or manual test annotation. No Hard-coding: Hard-coded predictions based on IDs, filenames, row order, or recovered source identity are forbidden. No Test-time Leaks: Test-time training, pseudo-labeling, aggregate test calibration, or fitting preprocessing parameters on test data is prohibited. No Pure-Metadata Bypasses: A genuinely trained visual model must be central to your solution. Using a metadata-only geometric graph (like distance thresholds on the seeds) as the complete solver without visual reasoning is invalid. (However, utilizing a standard graph search or min-cut algorithm to decode the removal plan from your model's visual edge predictions is perfectly valid and encouraged). &nbsp;
> $700 Pool
> Closes in 2h 37m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Social-Response Prediction Under Genetic Pair Shift

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75mfr5jgn89m94w35sdn55e98c5y3t
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Social-Response Prediction Under Genetic Pair Shift
> Loom Leader Forecast: Social-Response Prediction Under Genetic Pair Shift Overview A looming stimulus reaches every fly in an arena at essentially the same time, but the six individuals do not respond identically. One may accelerate sharply, another may remain near-stationary, and another may change course only after nearby movement changes the local social geometry. The interesting question is not whether a fly can be detected or classified from a video frame. It is whether a model can infer, from the preceding group dynamics alone, which member of a six-agent system will become the strongest immediate mover after a shared aversive event. Each item in this challenge is a five-second pre-stimulus trajectory history for six individually tracked Drosophila melanogaster flies. The model must predict the response leader: the fly with the greatest average frame-to-frame displacement during the first 1.2 seconds after the looming onset. The label is derived deterministically from held-back future coordinates; it is not an annotation supplied by the source collection. The split is deliberately genetic-pair-disjoint. Training contains examples from sixteen mixed genetic pairings. Test contains eight pairings never represented in training, while all six-fly trajectories remain available as model input. A solution cannot succeed merely by fitting the repeated dynamics of one known pairing; it must learn a neural representation of individual motion, relative position, and group interaction that survives a compositional change in the group. This is a from-scratch neural temporal modelling challenge, not a tabular classification exercise. The input remains a structured six-agent trajectory; no supplied feature identifies the strain pairing, recording session, sex, loom number, or source file. The target is future movement, not an object-detection or image-recognition label. Task For every row in test.csv, submit one response-leader prediction: Fly1, Fly2, Fly3, Fly4, Fly5, or Fly6. Each row contains the corrected (x, y) trajectory of six flies from -5.0 seconds through 0.0 seconds relative to looming onset, at 10 Hz. The 612 numeric features are ordered as six flies × 51 time positions × two coordinates. No post-loom coordinate appears in train.csv or test.csv. The true leader is derived organizer-side as follows: post positions: 0.1, 0.2, ..., 1.2 seconds after looming onset for each fly i: response_i = mean over the 11 adjacent intervals of EuclideanDistance(position_i[t + 0.1], position_i[t]) leader_id = Fly( argmax_i response_i ) The 11 displacement intervals have midpoints from 0.15 through 1.15 seconds. Exact ties are resolved by the fixed tracker order Fly1 through Fly6. No source behavioural label is used. Evaluation The official metric is macro top-1 accuracy, higher is better, with a range from 0 to 1. Recall_c = correct predictions among examples whose true leader is class c ---------------------------------------------------------------- number of examples whose true leader is class c LoomScore = (Recall_Fly1 + Recall_Fly2 + ... + Recall_Fly6) / 6 Each possible leader receives equal weight regardless of its frequency. Always predicting one tracker ID therefore scores exactly 1 / 6 = 0.1667, not that ID's raw prevalence. Public and private leaderboard rows use the same formula; the private result is final. Baseline gate All reference methods below were trained only on public/train.csv and evaluated on the actual held-out genetic-pair test set. They use no source metadata, external data, or test-set adaptation. Always predict Fly1 — LoomScore 0.1667 Linear softmax classifier — LoomScore 0.1566 Two-layer 64-hidden-unit MLP, from scratch — LoomScore 0.2598 The release requirement for all three is the same: a reference method must score below 0.65. The compact MLP is a deliberately weak neural reference: it flattens the trajectory and has no temporal-convolution, recurrence, graph, or set-attention inductive bias. Its score establishes a real but limited learnable signal under the held-out-pair shift. A competitive solution should model the trajectories as six interacting time series rather than as unrelated scalar columns. Dataset All participant-visible files are in public/: train.csv — 6,382 rows. Pre-loom coordinates plus the training-only leader_id. test.csv — 3,188 rows. Pre-loom coordinates only; leader_id is withheld. sample_submission.csv — 3,188 rows. The required submission schema, with Fly1 placeholders. README.md — compact participant-facing format documentation. Each row has this layout: Column group Type Count Description sample_id string 1 Opaque competition identifier; not a feature. fly{1..6}t{00..50}{x,y} float 612 Pixel coordinates at 10 Hz, -5.0 to 0.0 s. leader_id categorical 1 Train only: Fly1 through Fly6. test.csv has 613 columns including sample_id; train.csv has 614 columns including sample_id and leader_id. Every coordinate is finite. Participant-visible files contain no strain pair, sex, session, absolute timestamp, loom index, source filename, future coordinate, or behavioural-score field. Rows are deterministically shuffled. Adjacent CSV rows are not adjacent moments in a recording and should not be interpreted as one long sequence. Split Train — 16 genetic pairings, 6,382 events. Learn individual and social motion. Test — 8 genetic pairings, 3,188 events. Unseen genetic-pair generalisation. All looming events from the same recording session remain in one partition. No genetic pairing appears in both train and test. The pair identity itself is withheld from participants, so it cannot be used as a categorical shortcut. The private answer file may carry a visibility column used by the platform to select public and private leaderboard rows; it is evaluator metadata, not a prediction target. Submission Submit a CSV named submission.csv with exactly these columns: sample_id,leader_id test_00000,Fly3 test_00001,Fly6 Requirements: Exactly one row for every sample_id in test.csv. The submitted sample_id set must match test.csv exactly; order is irrelevant. leader_id must be exactly one of Fly1, Fly2, Fly3, Fly4, Fly5, Fly6. Duplicate IDs, missing IDs, extra IDs, blank predictions, and extra columns are rejected. Compute The prepared participant dataset is approximately 60 MB uncompressed and fits comfortably in memory. A temporal-convolutional network, recurrent network, temporal Transformer, graph neural network, or set-attention model in the 0.5–5 million parameter range can train within 90 minutes on 10 CPU cores and 62.5 GB RAM. A GPU is optional, not required. Method requirements Every submission must train a neural model using the released training partition. Use a trainable neural architecture implemented in PyTorch, TensorFlow, JAX, or an equivalent framework. Initialise model weights randomly and train them within the submission run. Document architecture, parameter count, optimizer, schedule, seed, and validation method. Use only the released participant files for data and labels. Derive validation data only from training rows; do not tune on test rows or leaderboard feedback. Suitable approaches include temporal convolutional networks, recurrent encoders, temporal Transformers, graph neural networks over the six flies, neural set encoders, and hybrid temporal-graph architectures. What not to use Classical-only, rule-based, nearest-neighbour, lookup-table, or hand-engineered final predictors. Pretrained checkpoints, externally trained weights, or external trajectory/behaviour datasets. Source-specific raw archives, source-file lookup, reconstruction of withheld future coordinates, or labels obtained outside the released public files. Test-set adaptation, pseudo-labelling, calibration using the full test distribution, or training on test rows. Synthetic labelled trajectories or manually constructed response-leader labels. Routine parsing, coordinate scaling, rotation/translation augmentation, missing-value handling, and neural-compatible geometric features are allowed. Classical preprocessing is acceptable only when a trainable neural model performs the final prediction.
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Georgian Syntactic Avalanche Ledgers

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx788rbs7jbxw2j2d91yadk91n8bv2vj
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Georgian Syntactic Avalanche Ledgers
> Georgian Syntactic Avalanche Ledgers Overview From Scratch, predict the results of eight chip spreading experiments for every Georgian sentence. Each experiment tells you which word positions receive chips. Your submission must report what happens after the chips finish spreading through hidden grammatical links between the words. The task can be read as four steps: Treat every public word position as a container. Add the chip amounts listed in one public intervention. A container holding at least as many chips as it has links sends one chip through every link. This continues until no container can send again. Predict eight summary measurements of the finished experiment. The links are the missing information. Adjacent words are always linked, while human corrected grammatical parent and dependent annotations add hidden links. A special exit receives chips that leave the graph. It never sends chips back. For each of the eight interventions, predict exactly these fields: | Field | Plain meaning | | --- | --- | | total_firings | Total number of chip sending events across all words | | touched_nodes | Number of word positions that sent chips at least once | | sink_absorbed | Number of chips that left through the special exit | | retained_chips | Number of chips still held by words at the end | | peak_firings | Largest number of sending events produced by one word | | center | Average sentence position of the sending activity | | spread | How widely that activity is distributed across the sentence | | entropy | How evenly the activity is shared among word positions | Example: if an intervention adds 20 chips at word position 4, nearby and grammatically connected words may begin sending chips. A prediction might report that 6 words sent chips, there were 35 sending events in total, 3 chips reached the exit, and 17 remained. The three geometry fields then describe where those 35 events occurred. This transformation turns real grammatical annotation into a deterministic graph experiment. A model is not asked to output dependency parents or relation labels. It must learn enough grammatical connectivity from training examples to predict the eight experiment summaries for unseen sentences. Permitted learning and simulation boundary The organizer, not the contestant, generated each supplied training target by running the deterministic chip-firing process on the hidden human-annotated graph. Those completed ledgers are already present in train_labels.csv; contestants are not required to recreate labels or know the hidden graph. Two concrete solution designs are expressly permitted: A randomly initialized neural network may map token_packets and the eight public interventions directly to the 64 response values. Training compares those outputs with the supplied ledgers. This design never runs a chip simulator at inference. A randomly initialized neural network may predict a graph, edge probabilities followed by learned decoding, node degrees, or another explicit latent connectivity representation. A deterministic implementation of the chip-firing rule in this specification may then run on exactly that model-produced representation and the public interventions to compile the eight output responses. In the second design, simulation is a permitted physical output layer: it does not decide which grammatical links exist. The learned model makes that decision. Implementations may use ordinary loops, queues, integer arithmetic, automatic differentiation, or a differentiable relaxation of the same process. The prohibited system is one in which a person supplies Georgian grammar, fixed dependency rules, decoded-symbol mappings, or graph heuristics that infer the links instead of fitting them from the public training supervision. Thus a chip-firing engine is not intrinsically rule based under this contract; only using hand-authored linguistic or graph decisions as the predictor is banned. The sentences come from two versioned Georgian language resources containing fiction, nonfiction, news, and scientific material. Their grammatical analyses were reviewed or corrected by people. Exact resource names, release links, contributor credits, and licences remain in the dataset documentation. Public inputs contain stable anonymous symbols; dependency heads, relation names, lemmas, sentence identifiers, and original text are hidden. Training uses upstream training records. Held out cases use upstream development and test records. No public token packet is duplicated across the boundary. Why this challenge is different The nearest established language benchmark is multilingual dependency parsing, including the CoNLL 2017 shared task. A parser predicts one parent and usually one relation for every word. Graph property prediction normally asks for a single graph statistic. This challenge asks for neither parents nor relation labels. A hidden human corrected syntactic graph is placed inside the chip firing game studied by Björner, Lovász, and Shor. The model receives eight nested interventions and must emit eight coupled conservation ledgers. The evaluator combines target accuracy with chip conservation, feasible firing geometry, and monotonicity under larger injections. The decision object is therefore an intervention response law over a hidden language graph. It tests whether a model has learned global syntactic connectivity without requiring a preferred parse. It is not a text generator, token tagger, repair task, path lattice, probability matrix, polynomial, automaton, or coalition cut game. Hidden graph construction Let a prepared case contain n public word nodes numbered 0 through n-1. Every prepared case has between 10 and 28 nodes. The hidden undirected simple graph is constructed as follows: punctuation nodes are removed each remaining word is connected to its nearest remaining syntactic ancestor if a word has no remaining ancestor, it is connected to a special sink node each pair of adjacent public word positions is connected duplicate edges are collapsed The sink receives chips and never fires. It is not included in token_packets. Chip firing rule A non sink node with degree d is unstable when it holds at least d chips. One firing removes d chips from that node and sends one chip along each incident edge. Chips sent to the sink are absorbed. Legal firings continue until every non sink node holds fewer chips than its degree. This process is Abelian: every legal firing order reaches the same stable state and the same number of firings at every node. The builder uses bulk legal firings for efficiency, but the result is identical to firing one legal node at a time. Public interventions Two distinct public positions, called a and b here, are selected for each case. The exact positions and chip counts are supplied in interventions. Let n be the node count. The eight slots are: | Slot | Chips at a | Chips at b | | ---: | ---: | ---: | | 0 | n | 0 | | 1 | 2n | 0 | | 2 | 0 | n | | 3 | 0 | 2n | | 4 | n | n | | 5 | 2n | 2n | | 6 | 2n | n | | 7 | n | 2n | Contestants should read the supplied intervention objects rather than assume positions or counts. Avalanche response fields For one intervention, let u_i be the number of times node i fires. Let c_i be the chips remaining at node i after stabilisation. | Field | Definition | | --- | --- | | total_firings | sum over i of u_i | | touched_nodes | number of nodes for which u_i > 0 | | sink_absorbed | total chips delivered to the sink | | retained_chips | sum over i of c_i | | peak_firings | max over i of u_i | | center | firing weighted mean of normalised public word position | | spread | firing weighted standard deviation of normalised public word position | | entropy | entropy of the normalised firing counts, divided by log(n) | For geometry, position i is represented by x_i = i / (n-1). When total_firings > 0, define p_i = u_i / total_firings. center = sum over i of p_i * x_i spread = sqrt(sum over i of p_i * (x_i - center)^2) entropy = -sum over positive p_i of p_i * log(p_i) / log(n) If no node fires, all three geometry fields are 0. Evaluation The reported score ranges from 0 to 1, and higher is better. Each prediction value may be a floating point estimate. Count fields do not have to be integers. Target error For field f, define: e_f = min(1, |P_f - T_f| / scale_f) The scales are listed completely below. They are response-specific numeric denominators computed from the visible node count n, visible injected-chip total C, and that response's private target where explicitly shown. There is no omitted global scale vector, fitted scale, or additional hidden constant. | Field | Scale | | --- | --- | | total_firings | max(T_total_firings, n^2 / 4, 1) | | touched_nodes | n | | sink_absorbed | total injected chips | | retained_chips | total injected chips | | peak_firings | max(T_peak_firings, n / 4, 1) | | center | 1 | | spread | 0.5 | | entropy | 1 | The weighted error for one response is: E_response = 0.22 e_total + 0.12 e_touched + 0.13 e_absorbed + 0.09 e_retained + 0.12 e_peak + 0.10 e_center + 0.10 e_spread + 0.12 e_entropy E_target is the mean response error over the eight slots. Conservation error For a response with C injected chips: E_conservation_response = min(1, |P_absorbed + P_retained - C| / C) E_conservation is the mean over the eight responses. Feasibility error For each response, let s = max(P_total_firings, n, 1). The grader computes these six nonnegative residuals: excess touched nodes: max(0, P_touched - n) / n peak larger than total: max(0, P_peak - P_total) / s too little mass for the reported peak and touched count: max(0, P_peak + P_touched - 1 - P_total) / s too much mass for the reported peak and touched count: max(0, P_total - P_peak * P_touched) / s absorbed chips above C: max(0, P_absorbed - C) / C retained chips above C: max(0, P_retained - C) / C The third residual is treated as zero if either predicted peak or predicted touched count is zero. E_feasible is the mean of all residuals over all responses, clipped to [0,1]. Intervention monotonicity One intervention dominates another when it injects at least as many chips at every public node and strictly more at one or more nodes. For every ordered dominance pair, the grader checks total_firings, touched_nodes, sink_absorbed, and peak_firings. For checked field f, the residual is: max(0, P_smaller_f - P_larger_f) / max(P_larger_f, n, 1) E_monotone is the mean residual, clipped to [0,1]. Case loss and final score L_case = clip(0.78 E_target + 0.10 E_conservation + 0.06 E_feasible + 0.06 E_monotone, 0, 1) Submission loss L is the mean case loss. The fixed no skill ledger is derived only from train.csv. For every slot, it uses the median training value of seven normalised quantities: total_firings / n^3, touched_nodes / n, sink_absorbed / C, peak_firings / n^2, center, spread, and entropy. Here, n is the sentence node count and C is the total chips injected in that slot. The exact training medians are listed completely below. These 56 decimal constants are hard-coded in the grader and are the only median values used; the grader does not recompute or tune the prior from private answers. | Slot | Total divided by n^3 | Touched divided by n | Absorbed divided by C | Peak divided by n^2 | Center | Spread | Entropy | | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | | 0 | 0.0081787230 | 0.4285714286 | 0.0526315789 | 0.0469832064 | 0.5118832246 | 0.1055449031 | 0.5904831586 | | 1 | 0.0557114000 | 1.0000000000 | 0.2916666667 | 0.1527777778 | 0.5362482433 | 0.2451334850 | 0.9054223546 | | 2 | 0.0081018519 | 0.4285714286 | 0.0500000000 | 0.0459183673 | 0.4870107962 | 0.1046792598 | 0.5945163973 | | 3 | 0.0546352923 | 1.0000000000 | 0.2870879121 | 0.1479289941 | 0.5168746724 | 0.2452845087 | 0.9067290655 | | 4 | 0.0522351529 | 1.0000000000 | 0.2717803030 | 0.1074380165 | 0.5267720513 | 0.2741162199 | 0.9521042249 | | 5 | 0.2415634470 | 1.0000000000 | 0.6315789474 | 0.3609467456 | 0.5307250310 | 0.2979940415 | 0.9874966294 | | 6 | 0.1469738967 | 1.0000000000 | 0.5061728395 | 0.2426035503 | 0.5314915971 | 0.2936988176 | 0.9811172824 | | 7 | 0.1470186618 | 1.0000000000 | 0.5083542189 | 0.2400000000 | 0.5277695177 | 0.2932163775 | 0.9815307494 | For one slot, call the first four applicable constants r_total, r_touched, r_absorbed, and r_peak. The prior constructs its count fields as follows: prior_touched = clip(r_touched * n, 1, n) prior_peak = max(1, r_peak * n^2) raw_total = max(1, r_total * n^3) prior_total = clip(raw_total, prior_peak + prior_touched - 1, prior_peak * prior_touched) prior_absorbed = clip(r_absorbed * C, 0, C) prior_retained = C - prior_absorbed The prior uses the slot's center, spread, and entropy constants directly. These definitions fully specify the fixed ledger used to obtain L0. Let L0 be the fixed ledger's private loss. gain = (L0 - L) / L0 The score is: 0 when gain <= 0.02 clip(((gain - 0.02) / 0.98)^1.04, 0, 1) otherwise The supplied prior, all zero output, a constant ledger, the packaged random reference, and malformed output score 0. An exact submission scores exactly 1. Submission Submit one CSV with exactly two columns: | Column | Type | Description | | --- | --- | --- | | case_id | string | Identifier copied from test.csv | | predicted_avalanche_ledger | JSON object encoded as a string | Object with exactly one responses field containing eight response objects | Every response object must contain exactly the eight fields defined above. Count fields must be finite and between 0 and 1,000,000,000. center and entropy must be within [0,1]. spread must be within [0,0.5]. Boolean values are rejected. One complete valid prediction cell is: {"responses":[{"total_firings":47.698312536,"touched_nodes":7.7142857148,"sink_absorbed":0.9473684202,"retained_chips":17.0526315798,"peak_firings":15.2225588736,"center":0.5118832246,"spread":0.1055449031,"entropy":0.5904831586},{"total_firings":324.9088848,"touched_nodes":18.0,"sink_absorbed":10.5000000012,"retained_chips":25.4999999988,"peak_firings":49.5000000072,"center":0.5362482433,"spread":0.245133485,"entropy":0.9054223546},{"total_firings":47.2500002808,"touched_nodes":7.7142857148,"sink_absorbed":0.9,"retained_chips":17.1,"peak_firings":14.8775510052,"center":0.4870107962,"spread":0.1046792598,"entropy":0.5945163973},{"total_firings":318.6330246936,"touched_nodes":18.0,"sink_absorbed":10.3351648356,"retained_chips":25.6648351644,"peak_firings":47.9289940884,"center":0.5168746724,"spread":0.2452845087,"entropy":0.9067290655},{"total_firings":304.6354117128,"touched_nodes":18.0,"sink_absorbed":9.784090908,"retained_chips":26.215909092,"peak_firings":34.809917346,"center":0.5267720513,"spread":0.2741162199,"entropy":0.9521042249},{"total_firings":1408.798022904,"touched_nodes":18.0,"sink_absorbed":45.4736842128,"retained_chips":26.5263157872,"peak_firings":116.9467455744,"center":0.530725031,"spread":0.2979940415,"entropy":0.9874966294},{"total_firings":857.1517655544,"touched_nodes":18.0,"sink_absorbed":27.333333333,"retained_chips":26.666666667,"peak_firings":78.6035502972,"center":0.5314915971,"spread":0.2936988176,"entropy":0.9811172824},{"total_firings":857.4128356176,"touched_nodes":18.0,"sink_absorbed":27.4511278206,"retained_chips":26.5488721794,"peak_firings":77.76,"center":0.5277695177,"spread":0.2932163775,"entropy":0.9815307494}]} The file must contain exactly one row for every identifier in test.csv. CSV row order is unrestricted because rows are aligned by case_id. Missing graded identifiers, blank identifiers, or duplicate submission identifiers score 0. Extra identifiers are ignored when the platform evaluates a public or private answer partition, so the same complete test submission can be used for both scores. Extra or missing columns are rejected. Any malformed response cell for a graded identifier scores 0 for the complete graded partition. Dataset train.csv Contains 1,600 feature cases: | Column | Type | Description | | --- | --- | --- | | case_id | string | Unique anonymous training identifier | | token_packets | JSON list of objects | Between 10 and 28 non punctuation word packets in observed order | | interventions | JSON list of objects | Eight chip injection descriptions in response order | The three feature columns above occur in the same order and with the same types in test.csv. train_labels.csv Contains 1,600 rows and joins one to one with train.csv by case_id: | Column | Type | Description | | --- | --- | --- | | case_id | string | Identifier matching exactly one training feature row | | target_avalanche_ledger | JSON object encoded as a string | Object with eight target response records | Each token packet has: | Field | Type | Description | | --- | --- | --- | | surface | JSON list of strings | Ordered anonymous character symbols | | pos_hint | string | Anonymous broad grammatical category | | native_hint | string | Anonymous native grammatical analysis | | feature_hints | JSON list of strings | Anonymous morphological feature identities | | joined_right | boolean | Whether the original token was written without a following space | Each intervention has one sources list. A source contains integer position and integer chips fields. One real public token packet looks like: {"surface":["c_108","c_104","c_097","c_112","c_169","c_097","c_169","c_072","c_026","c_060","c_169","c_033","c_108","c_169"],"pos_hint":"p_05","native_hint":"x_578","feature_hints":["f_045","f_087","f_078"],"joined_right":false} The public symbol domains are: | Field | Symbol form | Observed vocabulary | Interpretation of an equal symbol | | --- | --- | ---: | --- | | surface items | identifiers from c_000 through c_208 | 169 observed symbols | The same symbol represents the same written character | | pos_hint | p_00 through p_15 | 16 symbols | The same symbol represents the same broad grammatical category | | native_hint | identifiers from x_00 through x_1830 | 1,119 observed symbols | The same symbol represents the same source grammatical analysis | | feature_hints items | identifiers from f_000 through f_097 | 95 observed symbols | The same symbol represents the same morphological feature and value | | joined_right | true or false | 2 values | Whether the original word lacked a following space | Identifiers can have gaps because anonymous codebooks were built before final case selection. They are stable across training and test but do not reveal the original category names. A surface list contains from 1 to 26 character symbols. A feature_hints list contains from 0 to 11 symbols. One real intervention list begins with {"sources":[{"position":1,"chips":21}]}. position is a zero based index into token_packets, and chips is the positive integer amount added at that position. test.csv Contains 500 cases with case_id, token_packets, and interventions using the same types as training. It does not contain target_avalanche_ledger. sample_submission.csv Contains all 500 test identifiers and valid predicted_avalanche_ledger cells implementing the documented fixed prior. Its score is 0. Prepared-data safety review The prepared files contain linguistic examples, but they do not expose the source sentences or personal records. train.csv and test.csv contain only opaque case identifiers, anonymous symbol packets, integer chip interventions, and JSON field names. train_labels.csv, sample_submission.csv, and the private answer file contain only opaque identifiers and numeric ledgers. Preparation explicitly omits original sentence text, lemmas, source sentence identifiers, record identifiers, dependency heads, dependency relation names, treebank contributor metadata, email addresses, URLs, and source README text. No passwords, API tokens, account identifiers, authentication credentials, or other operational secrets are present in any generated public or private CSV. The author-side file named serving_secret.json contains deterministic random assignment material used only while preparing opaque symbols and case IDs; its values are build parameters rather than account credentials, and neither the file nor any of its values is copied into prepared data. The named scholars and contact information required for attribution remain only in the licensed organizer-side provenance documentation. They describe public dataset authorship and are not observations, prediction targets, or contestant features. The source corpora consist of previously published fiction, nonfiction, news, and scientific language rather than private user, medical, financial, employment, or customer records. This is the explicit personal- and secret-data review for the generated challenge files. What not to use All hand-authored predictive approaches are banned. Do not use hand-written Georgian grammar, fixed parent rules, deterministic dependency parsing, lexical lookup tables, manually decoded symbols, graph reconstruction heuristics, memorised sentences, or source matching. A deterministic chip-firing implementation is allowed when it operates only on a graph or latent connectivity representation predicted by the trained model, as specified in the permitted boundary above; it is prohibited when paired with hand-authored rules that choose that graph. Pretrained models, pretrained embeddings, pretrained tokenizers, external corpora, external dictionaries, language descriptions, external parsers, internet retrieval, source identification, manual relabelling, and human annotation are prohibited. Training, self supervision, feature normalisation, centering, clustering, calibration, reweighting, and adaptation must use only train.csv joined one to one with train_labels.csv. At inference, a model may use only token_packets and interventions from the current test row. It may not use other test rows, pooled test statistics, cross case retrieval, or test time adaptation. The predictive mapping from anonymous linguistic inputs to response values or latent graph decisions must be neural. Every trainable parameter must begin from random initialisation and be learned only from train.csv joined with train_labels.csv. Deterministic JSON parsing, anonymous symbol indexing, padding, masking, batching without cross-row interaction, numerical stabilisation, learned-logit decoding, chip firing on model-predicted connectivity, calculation of the documented response fields, clipping to documented bounds, enforcing conservation identities, and CSV or JSON writing are allowed. These mechanical operations may represent the model's decisions but may not add hand-authored linguistic decisions. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## SilentEcho: Cross-Vocalization Identity Matching

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72qyhaqahmzcmnkgr4w4x9jn8e1gk0
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat jesuisnadi's score of 0.367!

Full challenge description from page:

> Overview A person's active voice and their quiet body-conducted acoustic activity are two very different observations of the same physical system. In this challenge, each query is recorded while the subject is not speaking, while every candidate is an active-speech recording. Exactly one of eight candidates belongs to the query subject. Your model must identify that candidate. This is not ordinary speaker identification. The evaluation identities never occur in training, query and candidate signals occupy different vocalization states, and public inputs contain no speaker labels, recording names, or group IDs. A useful solution must learn which cross-sensor resonances persist when phonetic content disappears. The closed eight-way retrieval contract makes the task materially different from same-state speaker verification, binary pair classification, and environmental noise robustness benchmarks. This is a From Scratch challenge on one NVIDIA A10G. All model weights must be initialized during the run. Preprocessing, training, inference, and writing submission.csv must finish within 90 minutes. Objective For every test case, identify which candidate recording comes from the same unseen person as the passive query. Output the integer slot of the matching candidate, from 0 through 7. Dataset Information The public feature store contains 9,070 anonymized four-channel log-mel tensors. Every tensor has shape 4 × 48 × 128 and is stored as float16. CSV rows refer to tensors by integer index. spectrograms.npy contains the feature tensor with shape (9070, 4, 48, 128). train.csv contains 4,768 labeled active-to-passive matching cases. test.csv contains 1,248 unlabeled cases from held-out people. sample_submission.csv contains all test IDs and the required prediction columns. The four channels are synchronized contact-acoustic measurements. Each channel was resampled to a common rate, converted deterministically to a 48-bin log-mel representation, robustly centered and scaled within the segment, and clipped to a fixed numeric range. Raw audio, filenames, timestamps, speaker identifiers, and demographic attributes are not included. Feature Schema train.csv and test.csv share these input columns: id is the opaque string case identifier. query_index is the integer tensor index for the passive, non-speaking query. candidate_0_index through candidate_7_index are the integer tensor indices for the eight active-speech candidates. train.csv additionally contains target, the integer slot of the matching candidate from 0 through 7. Each slot is correct exactly 596 times in training and 156 times in test. Generalization and Leakage Controls The independent split unit is the person, not the CSV row or audio segment. Training uses 149 people; test uses 39 different people. No person, feature index, or source recording crosses the train/test boundary. All 32 passive segments from a test person share one hidden leaderboard visibility. Ten people are public and 29 are private. Public/private stratification retains five provider-validation and five provider-test people on the public side and balances preregistered baseline difficulty. Feature indices are globally permuted, case IDs are keyed hashes, candidate order is randomized, and the correct slot is exactly balanced. Candidate selection is independent of row order and contains one positive identity plus seven distinct negative identities. These controls remove filename lookup, row-order guessing, majority-slot rules, same-person train/test retrieval, and repeated-feature leakage. Hand-engineered spectral and temporal summaries score at the floor; the useful signal requires a learned cross-vocalization representation. Evaluation Metric Submissions are scored by multiclass accuracy: the fraction of evaluated rows for which prediction equals the hidden target. A perfect submission scores 1.0; a completely incorrect submission scores 0.0. Because every correct slot has identical support in the complete test set, no slot receives extra weight. Submission Format Submit a UTF-8 CSV containing exactly these columns in this order: id,prediction Include every test ID exactly once. Row order does not matter. prediction must be an integer from 0 through 7. Extra columns, missing or duplicate IDs, nonnumeric values, non-integer values, and out-of-range labels invalidate the submission. Compute and Method Constraints Use the assigned NVIDIA A10G and complete the run within 90 minutes. Train the submitted neural model from random initialization during the run. Do not use pretrained audio/speech encoders, external corpora, hosted APIs, internet access, source-dataset copies, or reverse lookup. Do not infer targets from IDs, row order, array indices, or hidden metadata. Do not manually label test cases or fit preprocessing/model parameters to test examples. Test tensors may be used only for forward inference. Purely rule-based, handcrafted-threshold, or retrieval-only submissions are outside the challenge contract. Learned preprocessing from training data is allowed. Responsible Use This benchmark measures research performance on anonymized contact-acoustic signals. It is not a production biometric system and must not be used for surveillance, authentication, medical inference, or identity decisions without independent consent, security, fairness, and privacy review. &nbsp;
> $700 Pool
> 3 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Prescription Route Automaton Induction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77t353av91mymsehetp6w2jh8br7w7
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat ahmedtambal's score of 0.633!

Full challenge description from page:

> Prescription Route Automaton Induction Overview This is a from scratch modelling task. Predict one deterministic acyclic route machine for each case. The machine must accept exactly the distinct semantic routes expressed by the coded clinical attempts in that case. A case contains two to six coded attempts from one French prescription session. Each attempt is an ordered list of anonymous word codes. Speakers can repeat an instruction while changing the wording, omitting a concept, or moving a concept to another position. The output is not a label for the whole case and it is not one restored text. It is a compact machine that describes the full family of valid semantic routes across the attempts. Shared beginnings and shared endings can occupy the same machine states. Everything needed for learning is in train.csv and train_labels.csv. Join them one to one by case_id. All model weights and representations must be initialized randomly and learned from these provided training cases only. Real world setting The underlying material contains real French clinical instruction recordings with human checked transcripts and token aligned semantic annotations. A route records the order in which concepts such as medicine identity, amount, form, administration rhythm, duration, route, and safety conditions appear. The public codes conceal the words and the concept names. Repeated instructions are useful because two attempts can express the same prescription through different semantic routes. The target machine preserves those alternatives while merging identical future behavior. The source is PxCorpus version 4, *A Spoken Drug Prescription Dataset in French for Spoken Language Understanding and Dialogue*, Zenodo record 10080490, DOI 10.5281/zenodo.10080490. It is distributed under Creative Commons Attribution 4.0. This challenge uses its human-checked transcript and token-aligned semantic annotation layer and does not expose participant metadata. Split design and duplicate control The source path identifies a prescription recording session. Sessions are never divided between training and evaluation. Before assigning a side, preparation selects one recording for each distinct nonempty route and encodes its word packet. It then joins sessions into dependency components whenever any selected coded attempt packet is identical. Every component is kept wholly on one side, so an exact attempt and its route supervision cannot cross from training into evaluation. Evaluation sessions are selected only from singleton dependency components. Exactly one case is constructed for each evaluation session, using its deterministic full bundle of up to six distinct routes. Consequently, any row-level public/private leaderboard division is also session-disjoint: no prescription session can occur in two evaluation rows. The realized evaluation set contains 121 sessions, 121 cases, and 320 attempt occurrences; all 320 coded attempt packets are distinct and none occurs in training. Training contains 246 sessions and retains up to three route-subset cases per session to provide more graph supervision. This produces 494 training cases and 1,290 attempt occurrences. All cases derived from one training session remain on the training side. Opaque identifiers are created only after this grouped split and carry no visibility or route information. The realized case split is 494:121, or approximately 80.3:19.7. Research context and structural novelty Spoken language understanding benchmarks usually predict an utterance intent or one label per token. A representative example is Goo et al. (2018), Slot Gated Modeling for Joint Slot Filling and Intent Prediction. Grammatical inference benchmarks such as Lang et al. (1998), Results of the Abbadingo One DFA Learning Competition learn a machine from explicit accepted and rejected symbol strings. This challenge uses a different decision object. A model must infer a minimal behavioral route machine directly from several anonymized natural language attempts. It is never given rejected routes at prediction time. The score combines complete route behavior with residual state distinctions, so matching a list of routes without learning their shared future structure is not enough. We found no cited benchmark with this combination of repeated human language, anonymous semantic routes, machine valued output, and residual quotient scoring. Machine format Each machine is a JSON object with three fields: start: integer. The start state identifier. accept: JSON list[int]. The accepting state identifiers. edges: JSON list[list]. Every inner list is [source_state, route_symbol, target_state]. The route symbols are r00 through r11. Example machine: {"start":0,"accept":[2],"edges":[[0,"r01",1],[1,"r03",2],[0,"r04",2]]} This machine accepts two routes: r01 r03 r04 Reading begins at start. Every route symbol follows one matching edge. The route is accepted only when reading ends in a state listed in accept. A valid submitted machine must satisfy all of these conditions: It has at most 64 reachable states. State identifiers are integers from 0 through 63. Booleans are not integers here. It has at most 128 edges. Every pair of source state and route symbol has at most one outgoing edge. It is acyclic. Every listed state is reachable from start. It uses only r00 through r11 as edge symbols. Every accepted route has at most 24 symbols. It accepts at most 512 distinct routes. State identifiers have no meaning. Renaming states, reordering edges, or reordering accepting states does not change the score when machine behavior stays the same. Files public/ train.csv train_labels.csv test.csv sample_submission.csv train.csv The realized file has 494 rows from 246 source sessions. case_id: string. Opaque identifier matching c_[0-9a-f]{16}. attempt_packets: string containing JSON list[list[string]]. The outer list contains two to six attempts. Each inner list contains anonymous word codes from w_000 through w_383 in their original order. The same two feature columns, in the same order and with the same types, appear in test.csv. train_labels.csv The realized file has 494 rows and joins one to one with train.csv by case_id. case_id: string. The corresponding training identifier. training_walks: string containing JSON list[list[string]]. One route walk is aligned with each attempt in attempt_packets. Each walk contains codes from r00 through r11. target_machine: string containing one machine JSON object. It is the minimal deterministic acyclic machine accepting the distinct training walks in that case. The training labels contain 1,290 aligned attempt walks. Packet lengths range from 1 through 43 codes. Training walks range from 1 through 16 route symbols. Target machines contain 2 through 36 states and 2 through 39 edges. test.csv The realized file has 121 rows from 121 source sessions that do not occur in training. Each session contributes exactly one evaluation case. case_id: string. Opaque identifier matching the training format. attempt_packets: string containing JSON list[list[string]]. It follows the training input schema and contains two to six attempts. The test file contains 320 attempts. Packet lengths range from 1 through 48 codes. All test packets are unique, and no test packet exactly matches a packet in training. sample_submission.csv The realized file has 121 rows. Its train-only learner applies a fixed seeded random projection to normalized packet-token and length features, fits the route-position readout by ridge regression on the public training walks, and mechanically minimizes its predicted walks into machines. It scores 0.063834 on the complete evaluation set. case_id: string. Copied from test.csv. predicted_machine: string containing one machine JSON object. The file is produced by a small randomly initialized train only learner. Submission Submit one UTF 8 CSV with exactly these logical columns: case_id: string. Every graded identifier must appear exactly once. predicted_machine: string containing one valid machine JSON object. Example: case_id,predicted_machine c_0123456789abcdef,"{""start"":0,""accept"":[2],""edges"":[[0,""r01"",1],[1,""r03"",2]]}" Malformed JSON, an oversized cell, an invalid edge, a cycle, an unreachable listed state, or any other invalid machine makes that row an empty rejecting machine. A cell can contain at most 16,384 characters. Duplicate submitted identifiers or failure to include every graded identifier returns 0.0. Extra identifiers are ignored. A missing required logical column raises ValueError. CSV row order does not affect the score. Evaluation The metric is route language and residual quotient skill. Higher is better. The score range is [0,1]. Why this metric measures route machine quality A deterministic route machine has two essential properties. First, it defines a language: which complete semantic routes are valid and which nearby routes are not. Second, it defines a state quotient: two prefixes belong in the same state exactly when they permit the same valid continuations. The target minimal machine is therefore characterized by both its accepted routes and these prefix equivalence classes. The route score R measures the first property. Positive probes check that every observed prescription route is retained. The edited probes are evaluator-generated structural contrasts: deletion, insertion, replacement, adjacent exchange, and early stopping test whether a machine overgeneralizes around its observed route language. They are not asserted to be clinically invalid, unsafe, or impossible prescriptions. Combining positive acceptance and contrast rejection as P_i + N_i - 1 rewards sensitivity and specificity together. A machine cannot score by accepting every route or by rejecting every route. The quotient score D measures the second property independently of arbitrary state numbers. Its merge term rewards placing prefixes together when the reference says their possible future routes are identical. Its separation term rewards keeping prefixes apart when their possible futures differ. This captures whether the predicted machine has learned the reusable clinical continuation structure rather than merely storing each training route as a separate branch or collapsing unrelated instructions into one state. Finally, Q = sqrt(R * D) is a geometric mean, so strong route recognition cannot compensate for an incorrect state structure, and a well compressed graph cannot compensate for accepting the wrong routes. A score near one consequently requires the submitted machine to reproduce both the semantic route language and the shared future behavior that defines its minimal deterministic structure. The finite case floor removes small apparent gains that can arise from a limited number of cases rather than consistent induction quality. Route behavior For a reference machine, let T be all routes it accepts. These are the positive probes. The grader creates structural contrast probes from every route in T by applying each of these one-step changes: Delete one symbol. Replace one symbol with any of the other eleven symbols. Insert any of the twelve symbols at any position. Swap two adjacent unequal symbols. Stop at any strict prefix. Routes already in T are removed. These generated alternatives are used only as structural evaluator probes; the benchmark makes no clinical-validity claim about them. The remaining routes are ordered by a fixed BLAKE2b digest and the first 256 are kept. The public digest key is the ASCII text c6-negative-v1. For case i, let P_i be the fraction of observed-route probes accepted by the submitted machine. Let N_i be the fraction of structural contrast probes rejected by it. R_i = max(P_i + N_i - 1, 0) R = mean_i(R_i) Always rejecting and always accepting therefore receive zero route skill. Residual quotient A residual describes what can still be accepted after a route prefix has already been read. For each case, the grader builds a prefix set from every prefix of every observed route. It then adds altered contrast prefixes in fixed digest order until there are at least 56 prefixes. The key for this order is c6-prefix-v1. All observed-route prefixes are retained even if their count already exceeds 56. Each probe prefix is read through a machine. The result is the reached state identifier. A prefix with no matching edge reaches one shared dead state. The minimal reference machine groups prefixes that have identical valid futures into the same state. The submitted machine must reproduce both kinds of state decision: Prefixes merged by the reference should reach the same submitted state. Prefixes separated by the reference should reach different submitted states. For every nondead reference state reached by at least two prefixes, compute the fraction of within state prefix pairs that also share one submitted state. Average these fractions across eligible reference states to obtain M_i. If there is no eligible reference state, M_i is 1. For every pair of different reference states, including the dead state when present, compute the fraction of cross state prefix pairs that reach different submitted states. Average these fractions across reference state pairs to obtain S_i. If fewer than two reference states are present, S_i is 0. D_i = clip(M_i + S_i - 1, 0, 1) D = mean_i(D_i) An unmerged trie can accept the correct routes while splitting prefixes that should share a residual state. It therefore loses quotient skill. A machine that merges everything also loses quotient skill because it fails the cross state checks. Fusion and finite case floor Q = sqrt(R * D) F = max(0.170, 0.45 / sqrt(max(number_of_cases - 1, 1))) score = 0 if Q <= F score = ((Q - F) / (1 - F)) ^ 1.12 otherwise All constants are: N_SYMBOLS = 12 MAX_STATES = 64 MAX_EDGES = 128 MAX_ROUTE_LENGTH = 24 MAX_ACCEPTED_ROUTES = 512 NEGATIVE_LIMIT = 256 PREFIX_LIMIT = 56 MAX_CELL_CHARS = 16384 DEADBAND = 0.170 NULL_Z = 0.45 RAMP_POWER = 1.12 EPS = 1e-12 A machine with the exact route behavior and exact residual state quotient for every case scores exactly 1.0. Any global renaming of its state identifiers preserves that score. Empty, fixed most common, and random blind machines score exactly 0.0 on the prepared test cases. Method restrictions Do not use pretrained models, pretrained tokenizers, pretrained embeddings, transferred weights, foundation model services, or features produced by another model. Do not use external corpora, dictionaries, grammars, medical resources, web results, alternate data releases, manually added labels, or information outside the provided public files. All rule based prediction approaches are banned. This includes handwritten token rules, regular expression mappings, dictionaries, lookup or memorization systems, tries that infer routes from test packets, hand built semantic finite state systems, edit templates, fixed route patterns, count heuristics, and manually specified linguistic constraints. Hybrid systems combining a learned model with any banned component are also banned. This includes rule based generation, correction, reranking, filtering, or fallback logic. Do not search for the original records or reconstruct readable words from public codes. Do not use case_id, CSV row position, file order, packet length alone, or grader edge behavior as predictors. Submissions may be audited. A high score does not make a prohibited method eligible. &nbsp;
> $700 Pool
> 3 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## The Thinning Chorus

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7b8jxz9q80j5dd5zb7v6h8618dwbe6
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat passbaseline's score of 0.602!

Full challenge description from page:

> The Thinning Chorus Overview Every June since 1966, volunteers have driven the same fifty-stop roadside routes across North America at dawn, counting every bird they see or hear. Played back across the decades, those counts are a slow-motion recording of a continent changing: some birds fade year over year, others surge into new country, whole guilds thin while a few generalists swell. An ecologist reading two censuses of the same countryside can usually say which came first. Now hide the species names, hide the route, blur the counts to coarse levels, and hold the survey loudness fixed. The decades are still in the data. Each row of this dataset shows you six anonymous roadside bird-survey profiles — counts over a fixed list of 120 anonymous species tokens, quantised to coarse levels — from six different survey routes of one region, surveyed in six different years between 1990 and 2023, in shuffled order. Consecutive surveys in the true chronological order are at least 5 years apart. Your job is to order the profiles from the earliest survey to the latest. The answer for a row is a string of six letters, a permutation of abcdef, listing the published positions from earliest to latest. What Makes This Hard The species are anonymous. Every species is a fixed token, s001 through s120, consistent across the whole dataset — but which token is which bird is withheld. Whatever you know about published bird trends cannot be pasted in; which tokens rise and which fall must be learned from the training rows. The counts are blurred and the loudness is banded. Counts are quantised to four coarse levels, and each row's six surveys lie inside one total-count band, so "the quiet survey is the recent one" is matched away — the untuned richness rule lands at the random floor on this composition. The routes are different and cold. The six profiles in a row come from six different roadsides of one region — habitat noise is real — and the split is by route: every test profile is from a roadside the training rows never showed you. What transfers is the drift of a regional community, not the character of particular roads. One token is not a clock. The best single-token rule, tuned with full knowledge of the training labels, clears the middle of the ladder but stays far below the trained reference: the era lives in how many species move together, not in any one bird. Where The Answers Come From Every answer is a recorded fact of a public national survey archive: each profile is one real standard-quality survey run of one real route, and the ordering label is the survey's calendar year, withheld with route, region, observer and species identities. Only main runs meeting the archive's own data-quality standard are used, and the 5-year minimum gap between chronological neighbours puts the ordering far above year-to-year noise. From-Scratch Requirement Every submitted solution must train a genuine predictive component using the released training rows, and that component must materially determine the submitted orderings. The training must happen inside solution.py during the graded run: loading weights fitted beforehand, or shipping a model with the submission, does not satisfy this. Network access is disabled during evaluation. Allowed approaches include: a pairwise comparator — two profiles in, which survey is later out — trained on the fifteen ordered pairs each training row provides, decoded by Borda count or sorting; per-token level vectors and profile statistics feeding any standard model; pointwise year regression with a monotone decode; small neural networks over the token-level vectors, initialised with random weights and trained only on the released rows; and standard numerical and machine-learning libraries already present in the evaluation environment. What Not To Use No external datasets, and in particular no bird-survey archive, trend publication, species database or range map. Do not attempt to identify the underlying routes, years or species, or to recover the species-token mapping, by matching the published profiles against any external resource. This is grounds for automatic disqualification. No pretrained weights of any kind, and no features, embeddings or labels produced by a pretrained model. No external APIs, no network calls at grading time, and no remote inference. No use of the test set beyond ordinary per-row inference: no training on test rows, no pseudo-labelling, and no fitting, calibrating, thresholding or normalising with statistics pooled across the test set. No linking across test rows: matching profiles between different test rows, or carrying any information from one test row into another, is test-set use and is prohibited. Each row must be resolved from that row's own six profiles plus what was learned from the training rows. No fixed hand-written pipeline that has no component fitted from the released labels. No hardcoded lookup tables, no fingerprinting of row identifiers or row order, and no manually supplied answers. Row identifiers are opaque and row order is randomised; both carry nothing. Evidence Every row is one JSON file holding a single key. profiles — type: array; six objects in answer order, each mapping anonymous species tokens s001 to s120, listed in SPECIES.json) to quantised levels 1 to 4. A token absent from a profile was not recorded on that survey. Each profile carries at least 10 tokens. Twin-content profiles were never used. One further public column matters for scoring: blend_band, a letter from a to d banding each row by the mean pairwise distance between its six normalised level vectors. It groups rows by how alike the row's profiles look, and the metric uses the bands so that easy varied rows cannot carry the score alone. It carries nothing beyond what the published profiles already show. Evaluation The row credit is pairwise order accuracy — the fraction of the fifteen pairs put in the right relative order — mapped to a skill score: random or constant orderings expect one half of the pairs right, so the row score is $$ R = \max(0, 2(\text{accuracy} - 0.5)), $$ and a perfect ordering scores one. Because each row is clipped at zero, a random submission still averages about 0.14 over many rows rather than exactly zero; that floor is a property of the clipping, stated here so nobody mistakes it for skill. Let $M_{\text{all}}$ be the mean row score over all test rows and $M_{\text{alike}}$ the unweighted mean of the per-band means, where rows are grouped by blend_band. The final score is $$ \operatorname{Score} = 0.80M_{\text{all}} + 0.20M_{\text{alike}}, $$ bounded to $[0,1]$. There are no hidden buckets. Dataset The prepared public data contains: train.csv — labeled training rows; test.csv — unlabeled test rows; sample_submission.csv — submission template; SPECIES.json — the fixed anonymous species-token list; task_manifest.json — public dimensions and scoring constants; and payload/ — one JSON file per row holding that row's six profiles. train.csv id — type: string; opaque unique row identifier. evidence_file — type: string; relative path to this row's JSON file. blend_band — type: string; a letter from a to d, the row's look-alike band. order — type: string; the gold ordering, a permutation of abcdef from earliest to latest. test.csv test.csv contains the same columns except order. sample_submission.csv id — type: string; one required test identifier per row. order — type: string; the identity permutation abcdef. It uses no evidence and scores about 0.16, the clipping floor. SPECIES.json tokens — type: array of strings; the 120 fixed anonymous species tokens, s001 to s120. size — type: integer; the token-list length. task_manifest.json task — type: string; stable task identifier. split — type: object; row counts, the leakage unit and the route-disjoint guarantee. signals — type: object; profiles per row, the token count, the level cap, the profile form and the composition rule. target — type: object; the permutation grammar and the minimum year gap. metric — type: object; the row formula, the two aggregation weights, the bucket column and the clipping-floor note. submission — type: object; required columns and the string length. evaluation_environment — type: object; CPU, memory, GPU and network configuration. from_scratch — type: object; training requirement and pretrained-weight policy. Submission Format Submit one CSV with exactly these columns in this order: id — type: string; must match the test identifiers exactly, with no missing, extra or duplicate values. order — type: string; exactly 6 characters, a permutation of abcdef, listing the published positions from the earliest survey to the latest. A prediction that is not a permutation of abcdef scores zero for that row and leaves other rows unaffected. A concrete two-row CSV example is shown below without a fenced code block: Header: id,order First row: 0a1b2c3d4e5f6071,ecafdb Second row: 9f8e7d6c5b4a3021,abcdef The example identifiers are illustrative and are not release rows. A Practical Starting Point A reasonable first system can be built in four stages: Load SPECIES.json and turn every profile into a normalised 120-dimensional level vector. Train a pairwise gradient-boosted comparator on the ordered pairs of the training rows — vectors of profile A, profile B and their difference in, "is B later" out. Decode each test row by Borda count over its thirty pairwise calls. Respect the split: validate on held-out routes, because the test routes are ones the model never saw. Two findings from building the reference solution are worth passing on. One token is not an era. The obvious single reads — richness, any one token's level — sit at or just above the random floor once the loudness band does its work; the best tuned single token clears the floor but plateaus far below the reference. The chorus moves together. What the learned comparator reads is the joint drift — which tokens rise and fall together across the decades, region by region. That joint reading is what transfers to unseen roadsides, and the headroom above the published reference belongs to models that read token interactions rather than marginal levels. Compute Environment Submitted solutions run in a CPU-only environment with 10 CPU cores and 62 GB of RAM. No GPU or network access is available. Training, inference and decoding must all fit within those limits. Expected Output Your script receives the public dataset directory and exact submission CSV path as two positional arguments. It may read only the files listed under Dataset above, all of which live inside that directory. No answer or label file for the test rows exists anywhere the script can reach. It must write only the submission CSV at the given path, and must not depend on any file left behind by an earlier run. &nbsp;
> $700 Pool
> Closes in 3h 35m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Constrained CJEU Citation-Profile Assignment

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cad0vt3crezmm62vg8fe3hn8bxg96
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat civil_dept's score of 0.468!

Full challenge description from page:

> Overview A legal paragraph can rely on one recent authority, repeat several paragraphs from the same case, or combine a broad set of older and newer precedents. In this challenge, the citations themselves are masked. Your task is to infer which anonymous citation profile belongs to each masked paragraph. The test set is divided into episodes. Every episode contains eight citation-masked Court of Justice of the European Union paragraphs and twelve anonymous citation profiles. Exactly eight profiles are true, one per query, and four are deliberately similar hard decoys. You must assign one candidate to every query. The assignment is one-to-one inside an episode: the same candidate may not be used for two queries. Candidate profiles expose structural and temporal citation statistics, but never cited case identities or cited text. This is an episodic constrained-matching task under chronological distribution shift. Public training judgments are dated 2018–2021. Hidden judgments are dated 2022–2025. Independent row classification is insufficient because candidate choices compete inside each episode. The modeling domain is From Scratch. The configured compute tier is CPU. Candidate Profile Meaning For a citing paragraph, let L be its set of distinct cited paragraph links and C its set of distinct cited cases. Let n_c be the number of cited paragraph links belonging to cited case c. Precedent age is the elapsed time between the citing and cited judgment dates. Each cited case contributes once to age statistics. The ten candidate fields are: link_load — float in [0,1]. Defined as min(log(1 + count(L)) / log(13), 1). case_breadth — float in [0,1]. Defined as min(log(1 + count(C)) / log(9), 1). dominant_case_share — float in [0,1]. Defined as max(n_c) / count(L). repeated_case_share — float in [0,1]. Fraction of cited cases contributing more than one cited paragraph. precedent_age_mean — float in [0,1]. Mean cited-case age divided by 50 years and capped at 1. precedent_age_median — float in [0,1]. Median cited-case age divided by 50 years and capped at 1. precedent_age_span — float in [0,1]. Oldest-minus-newest cited-case age divided by 50 years and capped at 1. precedent_age_dispersion — float in [0,1]. Population standard deviation of cited-case ages divided by 25 years and capped at 1. recent_precedent_share — float in [0,1]. Fraction of cited cases no more than five years older than the citing judgment. old_precedent_share — float in [0,1]. Fraction of cited cases at least twenty years older than the citing judgment. Evaluation Higher is better. The score is bounded to [0,1]. Every scored episode contains exactly eight queries and twelve candidates. Public and private leaderboard scoring preserve complete episodes; an episode is never intentionally divided between visibility partitions. Pair component Let A be the fraction of queries assigned to their exact true candidate. A random injective assignment has expected exact accuracy 1 / 12. P = clip((A - 1 / 12) / (1 - 1 / 12), 0, 1) Candidate-set component For each complete episode, let R_e be the number of selected candidates that belong to the episode's eight true candidates, divided by 8. Let R be the mean of R_e across complete scored episodes. A random selection of eight candidates from twelve has expected true-candidate recall 8 / 12 = 2 / 3. S = clip((R - 2 / 3) / (1 - 2 / 3), 0, 1) Perfect-episode component Let E be the fraction of complete episodes in which all eight query-to-candidate assignments are correct. Final score Score = 0.72 * P + 0.23 * S + 0.05 * E A perfect submission scores exactly 1.0. Performance at or below the stated random baselines receives no credit from the corresponding normalized component. Candidate reuse is evaluated across all eight rows of the full episode. A reused candidate cannot receive correct-assignment credit on its duplicated uses. Dataset All participant-visible files are under ./dataset/public/. train_queries.csv Contains 9,696 masked paragraphs across 1,212 training episodes. Its columns are: episode_id — string. Opaque episode identifier. query_id — string. Opaque query identifier. query — string. Citation-masked legal paragraph. query_year — integer. Year of the citing judgment. All queries in one episode share this year. paragraph_number — integer. Paragraph number inside the source judgment. word_count — integer. Whitespace-token count. character_count — integer. Character count. train_candidates.csv Contains 14,544 candidate rows, exactly twelve candidates for each training episode. Its columns are episode_id, candidate_id, and the ten profile fields defined above. train_matches.csv Contains 9,696 correct training assignments. Its columns are: episode_id — training episode identifier. query_id — query identifier from train_queries.csv. candidate_id — correct same-episode candidate from train_candidates.csv. test_queries.csv Contains 14,488 masked paragraphs across 1,811 hidden episodes. It uses the same query columns as train_queries.csv. test_candidates.csv Contains 21,732 candidate rows, exactly twelve candidates for each hidden episode. It uses the same candidate columns as train_candidates.csv. sample_submission.csv Contains all 14,488 required test query_id values and demonstrates a valid label-free injective assignment. Its participant schema is exactly query_id, episode, candidate_id. Split properties Training judgments are dated 2018–2021. Hidden judgments are dated 2022–2025. No source citing case appears in both periods. Every episode has eight distinct citing cases and eight distinct true profile vectors. Four signature-distinct hard decoys are selected from the same chronological side. Leaderboard visibility is assigned at complete-episode granularity so all eight answer rows from an episode remain together. Submission Write exactly one file to ./working/submission.csv. The file must contain exactly 14,488 rows and exactly these three participant columns, in this order: query_id — string. Globally unique row identifier. It must match one query_id from test_queries.csv exactly once. episode — string. It must equal that query's episode_id value from test_queries.csv. candidate_id — string. It must be a candidate from that query's episode in test_candidates.csv. Additional validity requirements: Every test query_id appears exactly once. No unknown or missing query identifiers are allowed. The eight selected candidate identifiers in an episode must be distinct for a valid final assignment. Participant submissions must not contain extra columns. Platform-only metadata such as answer visibility is not a participant submission column. Illustrative CSV:csv query_id,episode,candidate_id qry_0123456789abcdef01,ep_001122334455667788,cand_1234567890abcdef12 qry_fedcba9876543210fe,ep_001122334455667788,cand_abcdef0123456789ab The identifiers above are illustrative only. Use the identifiers in the public test files. Runtime and Modeling Requirements Compute tier: CPU. Domain: From Scratch. Read only from ./dataset/public/. Write only to ./working/, with the final file at ./working/submission.csv. Complete the full run within approximately one hour on the configured Project Eris CPU runtime. Use only libraries already available in the standard Kaggle Python environment. Do not access the internet or install packages during the run. Train every learned representation and model parameter during the submitted run using only public training files. Do not use pretrained language models, pretrained embeddings, foundation models, external checkpoints, cached features, external legal corpora, or external annotations. Do not use unmasked source text, raw citation links, source case titles, hidden labels, or files outside ./dataset/public/. Do not derive predictions from opaque identifiers, CSV order, filenames, hash behavior, or attempts to reconstruct source CELEX identifiers. Apply one uniform pipeline to all hidden episodes. Do not hard-code per-query or per-episode answers. Recommended Validation Use training-only validation that holds out whole episodes and evaluates the same full eight-query constrained assignment used at test time. Measure pair skill, candidate-set skill, perfect-episode rate, and the final weighted score. A useful system generally needs both a text-to-profile model and a global assignment method such as minimum-cost bipartite matching because independent predictions can reuse the same candidate. &nbsp;
> $700 Pool
> Closes in 4h 48m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Guitar Note Continuation Under Delayed Monitoring

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7csg65mr8tt6bcpt2jbw5ewh8dwby4
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat samluu206's score of 0.201!

Full challenge description from page:

> Background In live music performance and real-time remote collaboration, latency is an unavoidable physical constraint. Musicians constantly predict the immediate musical future, anticipating the next notes before they actually sound. For automated accompaniment, transcription, or robotic instrument play, an architecture cannot wait for an entire note to finish before deciding what to play next. Predicting musical continuation under delayed monitoring requires statistical forecasting. It forces the architecture to map a truncated acoustic history to a high-dimensional symbolic future. Because improvisation allows multiple valid continuations, this is not a deterministic transcription task—it is a probabilistic forecasting challenge where the target is the specific recorded continuation. Overview Train an architecture that listens to a recent three-second guitar recording and predicts the notes that will begin in a short future interval. The monitor is explicitly delayed: the last audible sample precedes the forecast start by 100, 200, or 300 milliseconds. Submissions must output a sequence of future note events detailing their string, pitch, onset, and end. A solution cannot simply recover future notes by transcribing audio; that audio has not been supplied. This is a From Scratch challenge. Train from random initialization in a single offline script using one NVIDIA A10G. The complete run, including preprocessing, training, inference, and writing the submission, must finish within 5,400 seconds. File loading and ordinary host preprocessing are permitted; a trained GPU neural architecture must be central. Time and Event Contract The input waveform contains exactly 48,000 mono PCM samples at 16,000 Hz. Let forecast time zero be the beginning of the requested future interval. Observation window: [-3 - latency_ms/1000, -latency_ms/1000) seconds. Target window: Predict note attacks in [0, 0.6) seconds. Temporal bins: There are 24 temporal bins in the target window, each 25 milliseconds long. An event is defined as the integer array [start_bin, string, pitch, end_bin]: start_bin: 0 through 23, inclusive. end_bin: start_bin+1 through 24, inclusive; the exclusive end of the event within the forecast interval. string: 0 through 5, ordered from lowest-pitched to highest-pitched open string. pitch: integer MIDI note number. The allowed ranges by string are respectively 40–64, 45–69, 50–74, 55–79, 59–83, and 64–88. Onsets are rounded down to their temporal bin, while ends are rounded up and clipped to the horizon. Only notes beginning within the horizon are targets; a note already sounding before zero does not become a new event. Continuous MIDI pitches are rounded to the nearest semitone. Predict at most 64 events per excerpt. Exact duplicate event arrays are invalid. Each observation receives deterministic seeded monitoring perturbations: additive Gaussian noise at 32–40 dB SNR relative to clean RMS; one or two quiet sinusoidal tones at 50–3,000 Hz, each with amplitude 0.5–1.5% of clean RMS; one 20–40 ms echo with gain 0.03–0.08; a low-pass blend with coefficient 0.02–0.05; one 5–10 ms dropout; and amplitude quantization with step 1/8192. Peaks above 0.98 are scaled down. Perturbations use only the observed history and preserve the future event labels. Numerical stability: Compute spectral power, mel features, and logarithms in FP32 outside mixed-precision autocast. Clamp power to a positive floor (for example 1e-5) before taking logarithms, and verify that features and losses remain finite. Mixed-precision neural layers may still be used. Dataset Information (Public Files) All files necessary for development and prediction are located in the public/ directory. There are 1,511 training requests (derived from 238 distinct source recordings) and 330 evaluation requests (derived from 113 distinct source recordings). +-----------------------+--------------------------------------------------------------+ | File / Directory | Purpose | +-----------------------+--------------------------------------------------------------+ | audio/ | Directory of mono PCM16 waveforms (3-second observations). | | train.csv | Labeled monitoring excerpts. | | test.csv | Excerpts requiring a continuation. | | sample_submission.csv | Empty event-list format examples. | +-----------------------+--------------------------------------------------------------+ Feature Schema train.csv and test.csv +------------+---------+-------------------------------------------------------------+ | Column | Type | Description | +------------+---------+-------------------------------------------------------------+ | id | String | Opaque unique identifier prefixed with g_. | | audio | String | Relative path to the audio asset (e.g., audio/.wav). | | latency_ms | Integer | The delay gap: 100, 200, or 300 milliseconds. | | events | JSON | (train.csv only) Array of target note event arrays. | +------------+---------+-------------------------------------------------------------+ Generalization & Leakage Controls To guarantee that solutions cannot memorize future sequences by associating them with other excerpts from the same performance, the following strict disjointness guarantees apply: Strict Performer & Recording Isolation: Training data includes excerpts from four performers, while evaluation data includes excerpts from two completely different performers. Consequently, no single source recording ever crosses the train/test split. The 238 training recordings and 113 evaluation recordings are mutually exclusive sets. Shared Cutoff Constraints: Within the evaluation set, a single source recording provides only one shared temporal observation cutoff. Up to three test requests may use the identical audio history but with different requested latencies (and therefore different future target intervals). No other public excerpt supplies later context from that specific held-out recording. Evaluation Metrics Submissions are evaluated using a continuous Intersection-over-Union (IoU) metric solved via a maximum total-credit bipartite assignment. 1. Eligible Edge Credit An edge can match a predicted event p to an annotated target event t only if: Their string values match exactly. Their pitch values match exactly. Their start_bin values differ by at most 4 bins (100 milliseconds). If eligible, the edge receives a credit score based on temporal overlap: Credit(p,t)=0.7+0.3×IoU(p,t) Where IoU(p,t) is the intersection-over-union of their half-open temporal intervals. 2. Bipartite Assignment Let P and T be the total numbers of predicted and annotated events. The evaluator computes a one-to-one matching M using the Hungarian algorithm to maximize the total credit. M contains only eligible matches with positive credit. Unmatched events earn 0.0. 3. Row Score From the optimal matching M, two components are derived: F-measure surrogate: F = 2 * |M| / (P + T) Quality surrogate: Q = 2 * sum(IoU(p,t) for (p,t) in M) / (P + T) The final row score is the weighted combination: Row Score=0.7×F+0.3×Q If one event list is empty and the other is not, the row scores 0.0. If both are empty, the row scores 1.0. A perfect continuation scores exactly 1.0. Extra and missing notes reduce both components symmetrically. 4. Final Score The final competition score is the unweighted arithmetic mean over all row scores. Higher is better. Sample Submission Format Submit a UTF-8 CSV file containing exactly two columns in this order: id,events. Include one row per test ID and do not include an index column. The events column must be a quoted JSON array of integer arrays. id,events g_0a1b2c3d4e5f6a7b8c9d0e1f,"[[2,0,43,8],[3,1,48,12]]" g_1b2c3d4e5f6a7b8c9d0e1f2a,"[[12,4,72,24]]" g_2c3d4e5f6a7b8c9d0e1f2a3b,"[]" Parsing Bounds & Rejection: Wrong column names/order, wrong row count, duplicate IDs, missing/extra IDs, malformed CSV syntax, or a CSV file larger than 64,000,000 bytes result in a file-level score of 0.0. Malformed JSON, invalid bounds, noninteger values, repeated events, or JSON cells longer than 12,000 characters result in 0.0 only for that specific row. Booleans are not integers. What Not To Use To ensure equitable assessment of training efficiency and algorithmic design: No Pretrained Weights: No pretrained encoders, pretrained weights, external music/audio data, or cached embeddings are allowed. No External Services: No internet access, hosted APIs, audio fingerprint matching against external archives, or manual annotation of test excerpts. No Test-Time Transduction: No fitting normalization, clustering, calibration, pseudo-labels, or network updates on test data. Use test excerpts only for forward inference. No Source Reverse-Engineering: No hard-coded test IDs, filename-derived answers, source-recording lookup, or reconstruction of source ordering. No External Corpora: No separately generated training corpus. Label-preserving augmentation of the provided training audio is allowed. No Heuristics-Only Solutions: No rule-only or inference-only solutions. Train the neural architecture inside the submitted script and reserve time to produce the CSV. &nbsp;
> $700 Pool
> Closes in 5h 55m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Recovering Stethoscope Position From A Heart-Sound Clip

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71ngv8y3e8vscb5c4g7ktcc18dsmbd
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat douglas's score of 0.703!

Full challenge description from page:

> Background When a clinician auscultates a heart, they move the stethoscope between a small number of standard chest positions. Each position listens to the heart through a different acoustic path: a different thickness and composition of tissue, a different distance and angle to each valve, and a different amount of lung between the chest wall and the heart. The same heartbeat therefore sounds materially different at each position — the balance of the two main heart sounds shifts, low-frequency energy is attenuated differently, and murmurs radiate towards some positions and away from others. Automatic recovery of the recording position matters for unsupervised and self-administered auscultation, where nobody records where the device was held, and for auditing archives of recordings whose position metadata is missing or wrong. You are given short heart-sound clips and must recover which of four standard chest positions each clip was recorded at. The four positions are: APEX — the cardiac apex, low on the left chest LLSB — the lower left sternal border LUSB — the upper left sternal border RUSB — the upper right sternal border What makes this hard The training and test clips come from two independent cohorts. Test clips were recorded in a separate clinical data collection from the training clips, with different patients and different recording circumstances. A model that latches onto cohort-specific characteristics rather than the acoustics of chest position will transfer poorly. This is the intended difficulty of the challenge, not an accident of the split. Loudness is a trap, not a solution. No normalisation of any kind is applied to the clips — they are copied sample-for-sample from the source recordings, so absolute level is whatever the recording gain and contact pressure happened to be. That level is not pure noise: a baseline built only from loudness features (log RMS, plus its z-score and rank within a subject) scores about 0.07-0.10, clearly above the floor. But it is a recording-condition artifact rather than acoustics of position, it varies between the two cohorts, and it caps out far below what the waveform itself supports. Normalising each clip before modelling is the recommended starting point. Five seconds is roughly four to seven heartbeats. There is no long-term context to average over, and a clip may be contaminated by breathing, handling noise or a poor seal. You must be competent at all four positions, not three. Half of the score depends on your worst position, so a model that quietly gives up on the hardest one scores far below a model with the same average accuracy spread evenly. Requirement: train a model from scratch Solutions must train their model from randomly initialised weights inside the run. Do not load pretrained audio encoders or other pretrained checkpoints. The signal here is a 4 kHz biomedical waveform whose content sits almost entirely below 500 Hz, which is far outside the domain of general-purpose pretrained audio models; a compact network trained from scratch on the provided training clips is the intended approach and is achievable well inside the runtime budget. What not to use The clips are excerpts of real recordings that exist in a public archive, and in that archive the auscultation position is written into each source file's name. The label is therefore recoverable by identifying the source files rather than by listening to the audio. That is not the task, it does not generalise to a new recording, and solutions that do it are not solving the problem. The following are out of bounds: Searching for, downloading, or otherwise consulting any external archive, repository, dataset or mirror in an attempt to locate the recordings these clips came from. Waveform or spectral fingerprint matching, cross-correlation, or any other audio-identity matching of the provided clips against material obtained from outside this challenge. Recovering or using source filenames, source subject identifiers, acquisition dates, cohort names or any other provenance metadata. The identifiers you are given are opaque hashes and carry no recoverable information; treating them as anything but arbitrary keys is misuse. Any construction artifact of how the pool was built — excerpt ordering, file byte layout, file size, directory order or timestamps — as a predictive feature. Everything you need is in the waveforms, the training labels, and the group_id structure. A solution should be one that would still work on a newly recorded clip from a new clinic. Data Four files and two audio directories are provided. train.csv 8,000 rows, one per training clip. Columns: clip_id — string. Opaque identifier of the clip. The matching audio file is train/.wav. group_id — string. Opaque identifier of the subject the clip came from. Sixteen clips share each group_id. Use it to build an honest validation split: clips from one subject must never appear on both sides of your validation split, or your validation score will be optimistic. site — string. The training label; one of APEX, LLSB, LUSB, RUSB. test.csv 1,920 rows, one per test clip. Columns: clip_id — string. Opaque identifier of the clip. The matching audio file is test/.wav. group_id — string. Opaque identifier of the subject the clip came from, in the same namespace as the training column. No group_id appears in both train.csv and test.csv. sample_submission.csv 1,920 rows, a valid but unskilled submission. Its columns are exactly the columns of the answer key, in the same order. Columns: clip_id — string. Matches a row of test.csv. site — string. The predicted position; one of APEX, LLSB, LUSB, RUSB. The placeholder simply cycles through the four labels, which scores at the floor. train/ and test/ One WAV file per clip, named .wav. Every file is exactly 5.000 seconds of single-channel 16-bit PCM sampled at 4,000 Hz, i.e. 20,000 samples. Files in train/ correspond to rows of train.csv; files in test/ correspond to rows of test.csv. Submission format Produce a CSV with exactly two columns, in this order: clip_id, site. One row per clip_id in test.csv — 1,920 rows plus a header. Every test clip_id must be present, and no clip_id may appear twice. (The grader is evaluated separately on public and private subsets of the test set, so it requires every id it is currently scoring to be present and ignores ids outside that subset; submit the full 1,920 rows and this is automatic.) site must be one of the four literal strings APEX, LLSB, LUSB, RUSB. Matching is exact and case-sensitive; empty values and any other string are rejected. Row order does not matter. Submissions that violate any of the above are rejected rather than scored. Evaluation Let K = 4 be the number of positions. Two quantities are computed from the submission: accuracy — the fraction of all test clips whose predicted position is correct. worst_position_recall — the smallest of the four per-position recalls, where the recall of a position is the fraction of the test clips truly recorded at that position which the submission assigns to it. Each is turned into a chance-normalised skill: skill(a) = (a - 1/K) / (1 - 1/K) and the final score is score = 0.5 * skill(accuracy) + 0.5 * skill(worst_position_recall) clipped into the range 0.01 to 1.0. Higher is better. &nbsp;
> All-solver grace
> Grace ends in 18m
> $700 Pool
> Lockdown

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Living Mycelium Propagation Field Estimation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx748x8b6v4nez1brrbj2mfbch8dwwj5
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat minipeepee's score of 0.800!

Full challenge description from page:

> Living Mycelium Propagation Field Estimation Overview Predict six signed electrical-propagation strengths from incomplete multichannel recordings of living fungal mycelium. Each example contains one hour of simultaneous measurements from four anonymous differential electrode channels. Two high-resolution views show only half of that hour. A third, lower-resolution view covers the full hour. The required answer is a six-number vector: one directed coupling value for each pair of channels. A positive value means the first channel in a pair tends to lead the second. A negative value means the second tends to lead the first. Larger absolute values indicate stronger and more directionally consistent delayed activity. This is a from-scratch scientific signal-modeling challenge. It is not future forecasting, waveform completion, sequence generation, or ordinary scalar regression. The model must estimate a fixed graph-valued summary of one recorded interval. Real-world collection process The source measurements come from two compatible open laboratory collections of living fungi. Pairs of iridium-coated stainless-steel subdermal needle electrodes were inserted into colonized substrate or fungal tissue. A high-resolution data logger measured the potential difference across each electrode pair. The logger internally averaged rapid measurements and stored approximately one differential value per second. Most sessions recorded seven or eight channels simultaneously and lasted from hours to several days. The combined source pool contains 21 unique recording files from 20 recording groups after one byte-identical duplicate is removed. It includes spontaneous electrical activity from oyster-fungus substrate recordings and four additional fungal species recorded with the same differential-electrode method. The traces contain slow excursions, long quiet periods, baseline drift, quantization, channel dropouts, and recording-condition changes. The prepared benchmark uses: 600 training examples from 15 contributing train-only recording groups; 150 test examples from 3 contributing test-only recording groups; exactly 750 distinct source intervals; one public example per source interval; no overlapping source intervals within any recording file. Each example begins with a non-overlapping one-hour interval. Four channels with sufficient finite data and measurable variation are selected once. Their order is permuted locally. Voltage polarity is independently reversed per channel to model arbitrary differential-lead orientation. The nonnegative activity view and the propagation target are invariant to that nuisance polarity. The hour is divided into four 15-minute blocks. Two blocks retain high-resolution samples and two blocks are withheld. Short telemetry gaps are also placed inside the retained blocks. A complete 30-second-resolution overview remains available for all four blocks. Prediction objective For every test row, submit a JSON list of six finite numbers in [-1,1]. The entries correspond to these row-local channel pairs in this fixed order: index 0: C1,C2 index 1: C1,C3 index 2: C1,C4 index 3: C2,C3 index 4: C2,C4 index 5: C3,C4 The objective is to infer the directed coupling field of the complete one-hour interval from the complementary high- and low-resolution evidence. Dataset files The public preparation output contains four files. train.csv train.csv contains 600 training inputs and no target column. Its columns are: id: string. Anonymous 20-character row identifier. voltage_code: string. Encoded 4 x 3600 normalized slow-voltage view. Unavailable positions use ~. activity_code: string. Encoded 4 x 3600 nonnegative activity view with exactly the same unavailable positions. context_code: string. Encoded 4 x 120 activity overview covering the complete hour at 30-second resolution. train_targets.csv train_targets.csv contains the 600 training labels: id: string. Matches exactly one train.csv row. predicted_propagation: string. JSON list of six reference propagation values. Keeping labels separate makes the feature columns of train.csv and test.csv identical. test.csv test.csv contains 150 unlabeled examples. It has exactly the same four columns and field schemas as train.csv. It contains no target, source identifier, session label, timestamp, source coordinate, split flag, target statistic, or audit field. sample_submission.csv sample_submission.csv contains: id: string. Every test ID exactly once. predicted_propagation: string. The dummy value []. The dummy is intentionally malformed at row level and scores 0 without creating missing CSV cells. Input decoding The 64-symbol value alphabet is: 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_ The zero-based alphabet index is q, from 0 through 63. voltage_code Length: exactly 14,400 characters. Layout: channel-major; four consecutive rows of 3,600 one-second samples. Decode a value symbol as approximately q / 6.3 - 5. Decode ~ as unavailable. Reshape the result to (4,3600). The values are robustly normalized slow-voltage residuals clipped to approximately [-5,5]. Public voltage sign is not a stable physical lead convention because polarity is independently reversed per row-local channel. activity_code Length: exactly 14,400 characters. Layout: channel-major and time-aligned with voltage_code. Decode a value symbol as approximately q / 12.6. Decode ~ as unavailable. Reshape the result to (4,3600). Activity is a nonnegative smoothed magnitude of the normalized slow-voltage excursion. Its unavailable-value mask is identical to the voltage mask. context_code Length: exactly 480 characters. Layout: channel-major; four rows of 120 bins. Each bin summarizes 30 seconds. Decode each symbol as approximately q / 12.6. Reshape the result to (4,120). ~ is not permitted. This coarse view covers the complete hour, including the two blocks unavailable at one-second resolution. Row-local aliases After decoding, matrix row 0 is C1, row 1 is C2, row 2 is C3, and row 3 is C4. These aliases are local to one example. C1 in different rows does not identify the same source electrode. Reference target construction The target is computed from the recorded activity values, not from a random label generator, filename, species name, session name, or split family. For each 15-minute block and channel pair (Ci,Cj), use: LagSet = {30, 60, 90, 120, 180, 240, 300} seconds EnvelopeForward = maximum positive-lag correlation from Ci to Cj over LagSet EnvelopeReverse = maximum positive-lag correlation from Cj to Ci over LagSet EventSignal(channel,time) = 1 if activity is at or above that channel's block-wise 88th percentile 0 otherwise EventForward = maximum positive-lag EventSignal correlation from Ci to Cj over LagSet EventReverse = maximum positive-lag EventSignal correlation from Cj to Ci over LagSet DirectionalAsymmetry = 0.62 * (EnvelopeForward - EnvelopeReverse) 0.38 * (EventForward - EventReverse) AssociationEvidence = 0.62 * max(EnvelopeForward, EnvelopeReverse) 0.38 * max(EventForward, EventReverse) BlockPairValue = clip(DirectionalAsymmetry / 0.16, -1, 1) clip((AssociationEvidence - 0.02) / 0.30, 0, 1) The reference value for a pair is the arithmetic mean of BlockPairValue over all four blocks. Therefore, the high-resolution inputs provide direct evidence for two blocks, while the complete coarse view provides weaker timing evidence for every block. Submission format Submit a CSV with exactly two columns in this order: id,predicted_propagation predicted_propagation must be a JSON list containing exactly six finite JSON numbers. Each number must lie in [-1,1]. Scientific notation is allowed. Valid example: id,predicted_propagation 4a1c2b3d4e5f60718293,"[0.42,-0.18,0.07,0.63,-0.31,0.11]" Invalid row-level values include: []: wrong length; [0,0,0,0,0]: wrong length; [0,0,0,0,0,NaN]: not finite JSON; [0,0,0,0,0,1.4]: value outside [-1,1]; {"C1,C2":0.4}: wrong JSON type; 0.1,0.2,0.3,0.4,0.5,0.6: not one JSON list. Rows may appear in any order because the grader aligns them by id. Evaluation Structural submission errors raise ValueError. These include wrong columns or column order, wrong row count, missing IDs, duplicate IDs, unknown IDs, and extra IDs. A malformed row-level prediction receives a row score of 0. Empty strings, missing cells, booleans, NaN, infinity, wrong list lengths, nonnumeric list members, and out-of-range values are malformed. There is no abstention advantage. Let P be the submitted six-vector and T the hidden target. For pair index k: weight_k = 0.20 + 0.80 * abs(T_k) ZeroError = sum_k weight_k * abs(T_k) / sum_k weight_k PredictionError = sum_k weight_k * abs(P_k - T_k) / sum_k weight_k AmplitudeSkill = clip((ZeroError - PredictionError) / ZeroError, 0, 1) All catalog targets have positive ZeroError. A valid all-zero vector receives AmplitudeSkill = 0 by arithmetic. For direction, select the two target entries with greatest absolute magnitude. The fixed pair index resolves exact magnitude ties. A selected sign is correct only if the prediction is nonzero and has the same sign as the target. SignAccuracy = correct selected signs / 2 SignSkill = clip(2 * SignAccuracy - 1, 0, 1) For relative edge strength, compute average ranks of abs(P) and abs(T) over the six entries and then their Pearson correlation. Tied values receive their average rank. If either rank vector is constant, correlation is defined as 0. RankSkill = clip(rank_correlation, 0, 1) The row score is: row_score = AmplitudeSkill ( 0.70 0.18 * SignSkill 0.12 * RankSkill ) If all six values match the hidden target within absolute tolerance 5e-7, the row score is exactly 1. This only stabilizes serialization at the oracle point. For an answer partition with N rows: bottom_count = max(1, ceil(0.20 * N)) overall_mean = mean(row_score over all N rows) bottom_20_mean = mean(the bottom_count smallest row scores) final_score = 0.82 * overall_mean 0.18 * bottom_20_mean All clipping is inclusive. The score is finite and bounded in [0,1]. The sample submission scores exactly 0. The known-answer submission scores exactly 1. Split, independence, and leakage controls The leakage unit is a complete recording group. A group corresponds to one laboratory acquisition session or a set of files exported from the same acquisition setup. Complete groups are assigned to train or test before intervals are constructed. The three held-out test groups contain four source files and never contribute training rows. Fifteen distinct train-only groups contribute selected training rows. Train and test share no group, source-file hash, interval, row ID, or transformed trace hash. Source files are divided into fixed, non-overlapping one-hour intervals. Exactly one channel selection, one mask, and one public row are released for each selected interval. No interval is reused, and no two selected intervals from one file overlap. Consequently, a high-resolution sample hidden in one test row is never exposed at high resolution in another public test row. One byte-identical source export is removed before row generation. IDs are hashes of the transformed public representation. They do not encode source names, file hashes, dates, offsets, channel identities, targets, or ordering. Prepared rows are sorted by those anonymous IDs. Public test data contain none of the private provenance fields used by the audit. What not to use Do not infer targets from row order or ID prefixes; both are independent of source order and target values. Do not treat C1 through C4 as stable electrodes across rows; aliases are permuted independently. Do not use source filenames, session names, species labels, original channel numbers, or timestamps. They are absent from prepared inputs. Do not search for another public view of the same interval. The revised dataset releases one view per interval and selected intervals never overlap. Do not interpret ~ as zero activity. It marks an unavailable high-resolution sample. Do not predict the propagation field from context_code alone. It covers the full hour but discards fine lag information. Do not submit reconstructed waveforms, channel labels, JSON objects, explanations, or extra columns. Submit only the required six-number JSON list in the CSV field. Recommended modeling directions A useful baseline can decode the activity view, compute lead-lag statistics on the retained blocks, and shrink those estimates toward zero. Stronger systems can combine: multiresolution temporal convolutions; cross-channel attention; mask-aware encoders; pairwise heads shared across the six channel pairs; event and envelope correlation features; complete-group holdout during local validation; calibration against the relative-error component of the metric. The public training set contains 8.64 million encoded high-resolution scalar positions per view, plus 288,000 coarse context values. Decode in batches or cache compact numeric tensors. Resource limit Hardware: one NVIDIA A10G GPU. The GPU budget supports mask-aware one-dimensional convolution or attention over 3,600-step multichannel inputs and complete-group-aware model selection. Benchmark boundary Published fungal-electrophysiology analyses commonly detect spikes, summarize inter-spike intervals, estimate transfer entropy, or report propagation within one experiment. This benchmark does not ask whether a spike exists, classify fungal species, or reproduce a published table. The benchmark instead estimates a calibrated six-edge directed field from complementary high- and low-resolution views, with half of the fine timing withheld, row-local electrode identities, polarity nuisance, multispecies training coverage, and complete recording-group holdout. The required capability is masked multirate representation learning with pairwise directional calibration.
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Australian Lexical Reliability Polynomials

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bqrej0y08znmxt9dpgevmq58bvsm4
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat zerovibe's score of 0.524!

Full challenge description from page:

> Overview From Scratch, predict eleven counts for every case. Each case contains word forms from six Australian language varieties. Ten word panels must be evaluated. For every k from 0 through 10, your output at position k estimates how many selections of exactly k panels would connect all six varieties. A word panel contains the six forms used for one basic meaning. A panel links two varieties when their forms share a historical origin. Several selected panels connect all six varieties when their links form a chain that lets every variety reach every other variety. For example, there are 120 different ways to select three of the ten panels. If exactly 12 of those selections connect all six varieties, the correct coefficient at position 3 is c_3 = 12. The complete answer contains one such count for each selection size from 0 through 10. The relationship labels for the ten evaluated panels are not provided. Instead, each case includes eighteen calibration panels where the historical groupings are shown. A model learns a trainable comparison function from those worked examples and uses it to estimate the eleven counts for the ten unlabelled panels. It does not submit the missing groupings themselves. No external phonological knowledge is required. Segment symbols are anonymous but stable throughout the public data. Each calibration packet supplies fifteen labelled form-pair comparisons: equality of two relation_pattern integers is a positive label and inequality is a negative label. A single packet need not contain both classes. In the realized 27,000 training packets, 13,995 are all-negative, 291 are all-positive, and 12,714 contain both classes. Aggregated across the 1,500 training cases there are 34,360 positive and 370,640 negative comparisons, and every complete eighteen-packet training case contains at least one label of each class. Class-balanced sampling or a class-weighted loss is therefore appropriate. A compliant model can initialize segment embeddings randomly, encode each ordered form pair with a recurrent, convolutional, attention, or transformer network, learn pair scores through gradient based training, and condition its query predictions on the labelled calibration pairs through attention or another learned set encoder. The stable anonymous vocabulary, case-level two-class supervision, and end-to-end polynomial targets are the learning signal. A concrete permitted model One compliant implementation can be built as follows. Assign every anonymous segment code a trainable embedding initialized from random values. Encode each form list with a bidirectional recurrent network or transformer. For each pair of varieties in a calibration packet, combine the two form encodings with cross attention and an MLP. Create the pair target mechanically from the supplied calibration label: it is 1 when the two relation_pattern entries are equal and 0 otherwise. Train the pair logit with class-weighted binary cross entropy or balanced minibatches across the 405,000 labelled calibration pairs. For one case, give a learned set encoder the calibration pair representations, their supplied pair targets, and the query form representations. Cross attention lets the model infer which comparison behavior demonstrated by that case's eighteen labelled panels applies to its ten query panels. Either pass the resulting case representation to an eleven value neural readout trained against target_polynomial, or produce fifteen learned pair logits per query panel and compile their decoded relations with the documented connectivity calculation. Every mapping from segment sequences to a score in this example is controlled by trainable parameters learned from the supplied labels. The segment identities need no readable meaning and the test varieties need no external description. The stable segment codes let the global encoder learn recurring sequence evidence, while the labelled calibration panels provide the within case evidence needed for a source variety combination not seen during training. Learned soft alignment, learned edit style neural modules, contrastive losses, and a decision threshold selected only on a training validation split are also permitted alternatives. The packaged starter demonstrates a lighter train-only alternative. It computes generic sequence-comparison features, summarizes those features together with the supplied calibration labels, selects an attention temperature on a held-out portion of the training cases, and predicts each test polynomial as a fitted attention-weighted combination of training polynomials. No fixed similarity cutoff creates a relation label. Generic string features are allowed in this role because the target mapping and calibration are fitted from training supervision; a hand-authored linguistic correspondence or a fixed feature-to-relation decision remains prohibited. Historical linguists compare basic vocabulary to study relationships among language varieties. A single related word group may connect only part of a family, while several meanings together can connect the whole family. The eleven requested counts measure how much independent and redundant connection evidence is present across the ten evaluated meanings. The cases come from a licensed comparative lexicon of Pama Nyungan varieties spoken across Australia. Training and test use different source varieties. The six positions in every forms list are local slots v0 through v5, while meanings and word segments use stable anonymous symbols. The complete field schemas appear in the Dataset section. Split integrity and calibration sufficiency The split is made by source variety before any six variety case is constructed. The eligible varieties are placed in a deterministic order and assigned wholly to either training or test. The realized training side uses 97 source varieties and the test side uses 29 different source varieties, with zero variety identifiers shared. Every language specific form record and every cognate assignment belonging to a variety therefore stays on one side. A case is then built using six varieties from only its own partition, so no test variety, six variety panel, or language specific source row can occur in training. Local slot order is shuffled independently for each case, and case_id is an opaque keyed digest. Memorizing a training slot, variety combination, case order, or identifier cannot identify a test target. Test files expose neither the ten query relation patterns nor target_polynomial. Meaning and segment codes remain stable across the split on purpose. They serve as the shared input alphabet, like token identifiers in a language model, but do not contain a cognate label or polynomial value. Shared symbols therefore permit representation learning without sharing the held out varieties or their labelled records. The 18 calibration panels are not an arbitrary unlabeled sample. Each panel labels all 15 unordered pairs of the six local slots, so every case provides 18 * 15 = 270 observed relation decisions for exactly the same slot pairs used by its queries. Individual panels may be all-negative, all-positive, or mixed; the builder verifies that the full 18-panel calibration set in every realized train and test case contains both classes. The ten query panels contain 10 * 15 = 150 hidden pair decisions. Calibration and query meanings are drawn without replacement from the concepts shared by all six varieties, so a query panel is never duplicated among that case's calibration panels. The model receives more within case labelled pair observations than hidden pair decisions, while still having to transfer comparison behavior to new word forms. The benchmark does not assume that 18 panels mathematically determine every query relation. Ambiguity is part of the task, which is why real valued coefficient estimates are accepted. The calibration budget is sufficient as an episodic conditioning signal: during training, the model sees 1,500 complete episodes with the same 18 calibration and 10 query structure and learns how calibration evidence predicts held out coefficients. At test time it applies that learned inference procedure to 270 fresh labels from an unseen variety combination. Because every test variety is absent from training, success cannot come from memorizing training variety combinations; it requires transfer through the stable segment representations and the current case's labelled calibration evidence. Why this challenge is different The nearest established tasks are the SIGTYP 2023 Shared Task on Cognate and Derivative Detection and the SIGTYP 2022 Shared Task on Prediction of Cognate Reflexes. Those tasks predict pair relations or missing word forms. This challenge asks for neither. It combines within case calibration, sealed query relations, a six vertex union process, and an eleven coefficient graph reliability law. The decision object measures uncertainty over all 1,024 subsets of query evidence. This creates a research adaptation at the intersection of automatic cognate learning, episodic neural inference, and network reliability rather than a renamed version of an existing linguistic benchmark. Polynomial definition There are ten query layers, indexed from 1 through 10. Within one layer, varieties whose reference relation integers are equal are joined. Selecting several layers means taking the union of all joins in those layers. A selected set is connected when all six varieties can reach one another through that union. The empty selection contains no relation layers, so it leaves six isolated vertices and is not connected. Therefore every reference target has c_0 = 0. For k from 0 through 10, the target coefficient c_k is the number of connected selections containing exactly k query layers: c_k = number of connected S with S contained in {1,...,10} and |S| = k Therefore: the output has exactly eleven coefficients c_0 must equal 0 for k from 1 through 10, 0 <= c_k <= C(10,k) the accepted coefficient maxima are [0,10,45,120,210,252,210,120,45,10,1] The associated reliability curve is: R_c(p) = sum from k=0 to 10 of c_k * p^k * (1-p)^(10-k) If every query layer is independently available with probability p, this curve is the probability that the six variety network is connected. Submissions may use real valued coefficients. You are estimating a conditional target, so coefficients do not have to be integers. Evaluation The reported score ranges from 0 to 1, and higher is better. The grader first measures how closely the eleven predicted counts match the target counts, how closely both polynomials behave across different availability probabilities, and whether the predicted shape has the required endpoints and order. These three checks form one mean loss. The grader then converts the loss reduction over one fixed constant reference into the final score. A score of 0 means there is no meaningful improvement over that reference, while 1 means every target polynomial is exact. The formulas below implement this scoring summary. Let b_k = C(10,k), let q_k = c_k / b_k, and let t_k be the target coefficient. The eleven normalisation denominators are [1,10,45,120,210,252,210,120,45,10,1]. The first denominator remains one even though valid predictions and targets have c_0 = 0. Coefficient error E_coefficient = mean over k of |c_k / b_k - t_k / b_k| Reliability curve error The grader evaluates both curves at nineteen probabilities: P = {0.05, 0.10, ..., 0.95} E_curve = mean over p in P of |R_c(p) - R_t(p)| Shape error A valid reliability profile has a zero left endpoint, a one right endpoint, and nondecreasing normalised coefficients. The penalty is: E_shape = (|q_0| + |q_10 - 1| + sum from k=0 to 9 of max(q_k - q_(k+1), 0)) / 12 The denominator is 12 because this expression contains twelve penalty terms: two endpoint terms and ten adjacent coefficient comparisons. It is not the number of coefficients. Case loss and overall loss L_case = clip(0.42 * E_coefficient + 0.46 * E_curve + 0.12 * E_shape, 0, 1) The submission loss L is the mean case loss. The three component errors are each normalized to the interval from zero to one, so their weights state their maximum influence directly. The two fidelity terms receive 0.42 + 0.46 = 0.88 of the loss because the main objective is accurate polynomial estimation. Coefficient error receives 0.42 to reward accuracy of every reported count, including errors that may have little effect at a particular availability probability. Curve error receives the slightly larger weight 0.46 because the polynomial's intended use is the probability that the language network remains connected across different panel availability rates. The four point difference breaks close comparisons in favor of predictions with more faithful reliability behavior while keeping the two fidelity views nearly balanced. Shape error receives 0.12 as a structural safeguard. It detects impossible endpoints and decreases in the normalized reliability profile, but it is deliberately unable to outweigh an accurate or inaccurate target match by itself. This prevents a generic monotone polynomial from scoring well merely because it has a valid shape. Thus the weighting makes direct target fidelity primary, functional curve fidelity marginally primary within that pair, and structural validity a secondary regularizer. These constants are fixed for every case and submission; they are not fitted, recalibrated, or selected from the private answer values. No skill reference and final score Before release, the organizer took the position-wise median of the 1,500 normalized targets in train_labels.csv, projected it to the valid monotone shape, and converted it back to coefficient counts. This produced the fixed train-only polynomial: N = [0,0,1,8,28,56,70,56,28,8,1] The grader stores this exact vector and uses it unchanged for every evaluation row and every public or private answer slice. It does not recompute a baseline from hidden answers or contestant predictions. Let its mean loss on the graded answers be L0. gain = (L0 - L) / L0 The reported score is: 0 when gain <= 0 sqrt(clip(gain, 0, 1)) otherwise The square-root transform preserves the ordering of every positive-gain model while making modest improvements over the strong fixed polynomial visible at leaderboard precision. It introduces no threshold above the reference: a submission that does no better than the fixed reference scores 0, while every genuine positive loss reduction receives positive credit. A perfect submission scores exactly 1. Submission Submit a CSV with exactly two columns: | Column | Type | Description | | --- | --- | --- | | case_id | string | One identifier copied from test.csv | | predicted_polynomial | JSON object encoded as a string | An object with one key, connected_subsets, whose value is a list of eleven finite numbers | A valid prediction cell looks like {"connected_subsets":[0,0,2.4,11.8,35,71,103,88,42,9,1]}. The first coefficient must be exactly zero. Every other coefficient must be nonnegative and no greater than its corresponding binomial limit. The grader accepts any CSV row order because rows are matched by case_id. The file must contain exactly one row for every test identifier. Missing, extra, unknown, or duplicate identifiers produce a score of zero. Extra or missing columns are rejected. An invalid prediction cell is replaced by the all zero polynomial for that row. Dataset train.csv Contains 1,500 cases and these columns: | Column | Type | Description | | --- | --- | --- | | case_id | string | Unique training case identifier | | concept_packets | JSON list of objects | Eighteen calibration packets with forms and relation patterns | | query_packets | JSON list of objects | Ten query packets with forms and no relation patterns | These three feature columns appear in the same order and with the same types in test.csv. The redundant constant language_slots field is not stored. Positions zero through five in every forms list always correspond to v0 through v5. train_labels.csv Contains 1,500 rows and joins one to one with train.csv by case_id. | Column | Type | Description | | --- | --- | --- | | case_id | string | Identifier matching exactly one training feature row | | target_polynomial | JSON object encoded as a string | Eleven integer target coefficients | Fields inside concept_packets | Field | Type | Description | | --- | --- | --- | | meaning | string | Stable anonymous basic meaning symbol such as m_083 | | forms | JSON list of six JSON lists of strings | One ordered anonymous segment list for each local variety slot | | relation_pattern | JSON list of six integers | Local grouping labels; equal integers mark historically related forms in this packet | The integers in relation_pattern are canonical within a packet and carry no meaning across packets. Fields inside query_packets | Field | Type | Description | | --- | --- | --- | | meaning | string | Stable anonymous basic meaning symbol | | forms | JSON list of six JSON lists of strings | One ordered anonymous segment list for each local variety slot | Query packets do not contain relation_pattern. test.csv Contains 250 cases: | Column | Type | Description | | --- | --- | --- | | case_id | string | Unique test case identifier | | concept_packets | JSON list of objects | Eighteen calibration packets using the field schema above | | query_packets | JSON list of objects | Ten query packets using the field schema above | sample_submission.csv Contains all 250 test identifiers: | Column | Type | Description | | --- | --- | --- | | case_id | string | Identifier copied from test.csv | | predicted_polynomial | JSON object encoded as a string | Object with eleven numeric values in connected_subsets | What not to use All rule based prediction approaches are banned. In this challenge, rule based means that a solver hand authors a linguistic or semantic decision procedure that substitutes for fitting that decision from the supplied training supervision. Prohibited examples include hand written sound laws, manually authored segment substitution tables, dictionaries, target lookup tables, fixed identity based relation mappings, case specific human decisions, fixed similarity-to-relation cutoffs, and hard coded polynomial templates. Model operations are not treated as rule based merely because their execution is deterministic. Trainable attention, dynamic programming alignment with learned costs, learned similarity or distance functions, differentiable clustering, gradient based losses, and argmax or sampling from model logits are permitted when their predictive parameters are initialized randomly and fitted only with the public training cases. Generic task-independent form features such as segment n-grams or normalized edit similarity may also be inputs to a fitted neural, regression, kernel, or attention model; they may not directly decide a relation through a person-chosen cutoff. A threshold or other hyperparameter selected solely through a training validation split is permitted. The prohibited counterpart is a linguistic score, correspondence, cutoff, or complete prediction procedure chosen by a person or imported from outside data. Pretrained models, pretrained token embeddings, pretrained tokenizers, external corpora, external lexicons, external language tools, internet retrieval, source identification, and manual relabelling are also banned. Training, self supervision, normalisation, centering, clustering, calibration, reweighting, and adaptation must use only train.csv joined with train_labels.csv. At inference, process one test case using only that case's calibration and query packets. Do not use information or aggregate statistics from other test cases. &nbsp;
> $700 Pool
> Closes in 3h 4m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Placing Sterile Grass Specimens by Vegetative Morphology

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ammv5bad4d0sh3d9310md9x8dyqyj
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat singhking's score of 0.755!

Full challenge description from page:

> Identifying a Grass That Is Not in Flower Overview This is a from-scratch modelling challenge over a sparse categorical character matrix, and its output is a ranked shortlist rather than a single label. No pretrained model applies to it and none may be used. A grass in flower can be identified. Its spikelets carry the characters the whole classification was built on, and a specialist with a key will usually place it. A grass that is not in flower is a different problem entirely. All you have is leaves, culms, roots and habit, and those are the characters that vary least between lineages and most within them. Sterile grass material is among the hardest routine identification problems in botany. That is the problem posed here. Each record is one species described by 145 characters, every one of them readable from a specimen that is not in flower. For each species you must produce a ranked shortlist of three lineages, best guess first. The lineage is not a restatement of the features. The morphology was coded from taxonomic literature between 1986 and 2016; the lineage placement is the current classification, which rests largely on molecular evidence and was aligned to a modern taxonomic backbone in 2026. Morphology and molecules are known to disagree in this family, and convergent evolution is common - similar vegetative form has arisen repeatedly in unrelated lineages. The species you are scored on come from 245 genera that appear nowhere in your training data. No genus contributes to both halves. A genus-to-lineage lookup learned in training therefore cannot be applied at test time, and what has to transfer is a sense of which vegetative characters carry lineage signal across the whole family rather than within one group of close relatives. Everything here must be built from scratch. No pretrained model applies to an anonymised matrix of coded morphological states - there is no text, no image, no audio and no external representation to transfer from - and none may be used. The characters are opaque coded states, the lineage labels are opaque tokens, and nothing outside the released files describes either. The whole task is to design, from nothing, a representation of a sparse categorical character matrix and to fit a model to it using only the provided species. Nor is this a single-label classification problem. The required output is an ordered shortlist, and the score is a rank-based quantity: what is measured is how well a method orders candidate lineages against each other, not whether one label is right. A method that emits a single best guess forfeits the credit carried by second and third place. Solve it using only the provided data, and see the note on one-sample inference below. What the 145 characters are, and what is not there Every released character is an observation a sterile specimen supports: 97 leaf characters, 46 root and culm characters, and 2 of life cycle - annual against perennial, and whether the perennating organs persist or are short-lived. Both of the latter are judged from the base of the plant, not from a flower. Nothing reproductive is released, and that is enforced character by character, not merely by category: The whole spikelet apparatus was never in this corpus. No lemma, palea, glume, floret, awn, rachilla, synflorescence or inflorescence character exists in any released file. Six further characters that a sterile specimen cannot support are removed as well: plant sexuality, plant sexuality if monoecious, cleistogenes (concealed spikelets of different appearance), vegetative proliferation of the spikelet, vivipary (germination on the culm), and a database field recording whether flowering parts were described for that species at all. The first five require flowering material. The sixth is a fact about what the compiler had on the herbarium sheet rather than about the plant, and it would leak the source flora. The source-and-year-of-coding metadata is withheld for the same reason. Two entries in the state glossary mention reproductive structures, and both are declared here so their presence is not mistaken for an oversight. culms_fragility state 2 reads disarticulating at the nodes , and leafSheaths_looseness state 4 reads inflated . In both cases the observation is vegetative - a culm that breaks at its nodes, a sheath that is inflated - and the parenthesis is the original coders' note saying which structure they meant. Neither character records anything about a flower, and those two glossary lines are the only place a reproductive word appears anywhere in the release. Evaluation For each species you submit an ordered shortlist of three lineages. The score is the reciprocal rank of the true lineage: 1 if you put it first, 1/2 if second, 1/3 if third, and 0 if it is not in your shortlist. Those reciprocal ranks are averaged within each true lineage first, and the score is the mean of those per-lineage averages. This macro-averaging is deliberate and is the main thing the metric rewards. The lineages are wildly uneven - the largest holds more than thirty-five times as many species as the smallest - so a submission that simply favours the common ones scores badly however many individual species it gets right. Every lineage counts the same. All 13 lineages are scored, and they are scored on both halves of the leaderboard. The grader has no support floor: every lineage present in the answer key contributes one term to the average, so none is ever dropped. The public and private halves are formed by splitting the held-out genera whole, never row by row, and the split is constructed so that each half holds at least 10 species of every one of the 13 lineages - the smallest such cell is 11. The public score therefore measures the same quantity the private score measures, over the same 13 lineages, and is honest feedback rather than a partial view. Writing r for the position of the true lineage in your shortlist: The contribution for one species is 1/r if the true lineage is in its shortlist, and 0 otherwise. The score is the mean over lineages of the mean contribution for that lineage. Range 0 to 1, higher is better. Duplicated entries within one shortlist are collapsed, keeping the first, so a ranking cannot be padded to buy extra chances. Entries after the third are ignored. Row order never affects the score. Measured reference points, all produced by the shipped grader on the shipped files: The disclosed lazy answer, the three commonest training lineages in that order for every species, which is sample_submission.csv: 0.1410 A random shortlist per species: 0.1318 Random forest on the vegetative characters: 0.6146 Logistic regression on the vegetative characters: 0.6690 True lineage ranked first for every species: 1.0000 Two of those are worth reading carefully. The lazy answer scores 0.1410 and random scores 0.1318 - almost identical. That is what macro-averaging buys: favouring the common lineages gains essentially nothing over guessing, because the rare lineages count just as much. There is little artefact to exploit. Besides the characters, test.csv carries only the record identifier and group_id, and group_id is useless as a predictor: the test genera are disjoint from the training genera, so a test group_id matches nothing that was learned. Any predictive signal must come from the morphology. For orientation on how much the missing spikelets cost: the same logistic regression, given the full character set including every reproductive character, reaches 0.9161 on the same split and the same metric. The gap between that and 0.669 is the price of the specimen being sterile, and it is the part of the problem this challenge is about. Dataset The public folder contains: train.csv, 6,943 rows. Labelled species from 446 genera. test.csv, 2,976 rows. Species from 245 different genera. This is what you are scored on. characters.csv, 145 rows. What each character means. character_states.csv, 535 rows. What each coded state means. sample_submission.csv, 2,976 rows. The required output format, filled with the disclosed lazy answer. train.csv All columns are strings: record_id. Opaque species token. Randomly assigned; carries no signal and no ordering information. group_id. Opaque genus token. Species sharing a token are congeners. Provided so you can build a grouped validation split of your own. It must not be used as a predictive feature: training and test genera are disjoint, so a test group_id matches nothing learned in training, and pooling predictions across test rows sharing one is prohibited by the one-sample rule below. The 145 character columns. The coded state for that character, written as v followed by the state code, for example v1, v2, v1/2, or NA where the character was not scored for that species. The v prefix is there so that every character column is unambiguously categorical text rather than a number. ranking. The target: an opaque token for the lineage the species is placed in, one of 13. It is named ranking because train.csv, the answer key and your submission all use one name for this column; see Submission. test.csv The same columns as train.csv except ranking, which is withheld: record_id, group_id and the same 145 character columns. characters.csv and character_states.csv characters.csv gives each character's name, the description its original coders wrote, its type (114 discrete-unordered, 17 numeric, 8 discrete-ordered, 6 integer) and its category (leaves, roots and stems, or life cycle). character_states.csv gives the botanical meaning of every coded state. Both are provided so the characters can be reasoned about rather than treated as anonymous columns, and both describe exactly the 145 released characters and nothing else. The matrix is sparse and the sparsity is real. On average 59 percent of characters are unscored for a species; the median species has 58 of 145 scored, the least-described 46 and the best-described 100. The original coders recorded what their sources reported, and different floras report different things. NA means not scored, not absent. Submission Submit a CSV with the columns record_id and ranking, one row per species in test.csv. The first line is the header record_id,ranking, and each following line is one species, for example s00003,L09 L06 L05 then s00004,L02 L11 L09. One column name is used for the label throughout: train.csv, the private answer key and your submission all call it ranking. In train.csv and in the key it holds the single true lineage for that species - a correct shortlist of length one. In a submission it holds your ordered shortlist of up to three. Nothing has to be renamed between reading train.csv and writing your answer. Requirements One row per record_id in test.csv, plus the header. Every test record_id must be present; a missing id makes the submission invalid. No duplicate record_id values; a duplicate makes the submission invalid. The columns record_id and ranking must both be present. Any further columns are ignored rather than treated as an error. ranking is a space-separated list of lineage tokens, best first. Up to three are scored; anything after the third is ignored. A blank, missing or unparseable ranking scores 0 for that species rather than invalidating the submission. Rows whose record_id is not being scored are ignored, never an error. What not to use One-sample inference is required. Your method must be able to produce the shortlist for a single unseen species without the rest of the test split existing. Fit every encoder, vocabulary, scaler, imputer, decomposition and summary statistic on train.csv alone, then transform test rows through the frozen objects. Do not fit anything on train and test concatenated, do not pool statistics across test rows, and do not solve the test set jointly as one problem. That the test labels are never touched does not make such a method acceptable. No internet access at solve time, and no external data, corpora or pretrained checkpoints beyond the provided files. Do not attempt to identify the species, genera or lineages behind the tokens, and do not use upstream source repositories, provenance lookup, source identifiers, deterministic generation artifacts, or any other artefact of how this dataset was constructed to recover a lineage. Recovering an answer from anything other than the released characters is out of scope, however it is obtained. Do not attempt to reconstruct the private answer key. Do not hard-code per-species answers; the method must be derived from the provided data. record_id, group_id and the lineage tokens are randomly assigned. Do not rely on their order or on any pattern in them, and do not use row order as a feature. Why this is hard The vegetative characters are the ones evolution reuses. Tussock habit, rolled leaves, rhizomes and stolons, hairy ligules - each has arisen independently in lineages that are not close relatives, because each is an answer to a habitat rather than a mark of ancestry. The characters that would settle the question are exactly the ones withheld. The classes are severely unbalanced and the metric refuses to let you ignore it. The largest lineage holds more than thirty-five times the species of the smallest, and both contribute equally to the score. Getting the small lineages right, from genera you have never seen, is most of the task. More than half the matrix is unscored, and not at random. A species described from a brief regional flora has far fewer characters recorded than one revised in a monograph, so the pattern of what is missing is itself uneven across the family. A method that treats NA as a value, or that imputes it carelessly, will be misled by that unevenness. Two neighbouring lines of work exist and are worth stating precisely. Machine learning has been applied to morphological data in systematics, but for different purposes: scoring characters from images, extracting character matrices from published literature, and testing species-level hypotheses from morphometric measurements. Those operate on different inputs and answer different questions. Separately, the conflict between morphological and molecular evidence in the grasses is a well-documented topic in systematics, studied through phylogenetic analysis rather than as a prediction task. What is specific here is the formulation: sterile-only characters as input, a modern lineage placement as the target, whole genera held out, and a ranked shortlist scored so that rare lineages count as much as common ones.
> $700 Pool
> Closes in 6h 41m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Analyte Concentration-State Transfer Across Raman Sample Matrices

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73s4635p0tggtz14vxq77zj98dsr2d
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat abhi404's score of 0.460!

Full challenge description from page:

> Analyte Concentration-State Transfer Across Raman Sample Matrices Overview A Raman probe is the cheapest way to watch a bioprocess, and the hard part is never the first calibration. It is that the calibration is built on clean designed mixtures and then has to read a real, evolving, cell-free broth on the same probe. Concentrations that a model learned as sharp bands in a mineral-salt medium arrive buried in a background of metabolites nobody put there. Read the analytes anyway. Each spectrum is one liquid sample, and for each of eight analytes - glucose, glycerol, acetate, EnPump, nitrate, yeast extract, phosphate and sulfate - report which concentration state that sample was in. This is a from-scratch challenge. No pretrained model, no pretrained embedding, no spectral library and no externally fitted chemometric model may be used. Every parameter must be learned from the spectra provided, during the run - deep models fitted to these very corpora are published, which is exactly why they are excluded. What the targets are Every target in this challenge is the concentration of that analyte in the sample the spectrum was measured from, in g/L, discretised. It is a property of the liquid, not a record of any instruction. The three corpora reach that number by different routes, and the difference is the whole point of the task: Designed mixtures (substratemix, ecolimetab). The sample was built to a specification by a Tecan liquid handler, so the reference concentration is the prepared composition. Replicate spectra exist per mixture. Fermentation supernatant (broth). The sample is an hourly draw from a real Escherichia coli fermentation, centrifuged to remove cells, and its glucose and acetate were measured afterwards on a Cedex HT analyser. These are the concentrations biology left behind: glucose was consumed as the culture grew and acetate was produced by it. Nothing dispensed them, and there is no command trace to recover. So a 0 in the fermentation stratum means this analyte was at or below the detection floor when the sample was drawn, which for glucose usually means the culture had eaten it. It does not mean anything was skipped. The transfer question is whether a state boundary learned on prepared mixtures still lands in the right place on a matrix that was produced biologically. Why discrete states rather than regression The public work on these corpora is continuous concentration regression, and a regression metric hides exactly the failure this benchmark is about. Absolute intensity is arbitrary and corpus-specific, so a regressor can score respectably on the mixture range while placing every fermentation sample in one narrow slab near the training mean - and RMSE will barely notice, because the fermentation range is compressed. Discretising, then scoring by macro-F1 with every state weighted equally, prices the decisions instead of the arithmetic: the absent versus band 1 boundary counts as much as the top band, and a model that collapses onto the prior scores like the prior. The band edges are a fixed, published part of the task definition, derived from the training corpus alone, so a sample placed in a neighbouring band is simply wrong. The state space For each analyte, emit one integer: 0 - at or below the detection floor for that analyte 1 to 5 - present, concentration band 1 (lowest) to 5 (highest) The floor and all four interior cut points are published per analyte in concentration_bands.csv. They were computed from the training half of the mixture corpus only, and they are part of the task definition: you may use them freely. The two strata The test set pools two strata that are scored separately. Which stratum a row belongs to is not distributed, and the rows are pooled and shuffled. Held-out mixtures - designed mixtures whose exact composition, and every replicate of it, is absent from training. Same instrument, same sample matrix. All eight analytes are scored. Fermentation supernatant - the hourly draws described above (batch phase plus a glucose-limited feed). This matrix appears nowhere in the training data: it is spent, evolving medium rather than a designed mixture, and it is full of metabolites the calibration never saw. Only glucose and acetate were assayed here, so only those two are scored. The second stratum is where the challenge lives, and no split of the training corpora reproduces it. The final score weights the average stratum against the worse one, because a reader that only works on clean standards has not demonstrated transfer. Evaluation Each (stratum, analyte) pair with assayed truth is one cell. A cell is scored by macro-F1 over a frozen list of states. That list is published in scored_states.csv: it is the set of states that cell has at least 20 examples of, computed once over the whole test key. It is frozen rather than recomputed per evaluation so that every subset of the test set - each leaderboard half included - scores the same cells and the same states, and so that you can see exactly what you are being scored on. A stratum's score is the mean over its cells. import numpy as np import pandas as pd from sklearn.metrics import f1_score ANALYTES = ['glucose', 'glycerol', 'acetate', 'enpump', 'nitrate', 'yeast_extract', 'phosphate', 'sulfate'] MIXTURE_ONLY = ['glycerol', 'enpump', 'nitrate', 'yeast_extract', 'phosphate', 'sulfate'] N_BANDS, W_MEAN, W_WORST, NOT_ASSAYED = 5, 0.6, 0.4, -1 published verbatim in scored_states.csv SCORED_STATES = { ('fermentation_supernatant', 'glucose'): [0, 1, 2], ('fermentation_supernatant', 'acetate'): [0, 1], ('held_out_mixtures', 'glucose'): [0, 1, 2, 3, 4, 5], ('held_out_mixtures', 'glycerol'): [0, 1, 2, 3, 4, 5], ('held_out_mixtures', 'acetate'): [0, 1, 2, 3, 4, 5], ('held_out_mixtures', 'enpump'): [0, 1, 2, 3, 4, 5], ('held_out_mixtures', 'nitrate'): [0, 1, 2, 3, 4, 5], ('held_out_mixtures', 'yeast_extract'): [0, 1, 2, 3, 4, 5], ('held_out_mixtures', 'phosphate'): [0, 1, 2, 3, 4, 5], ('held_out_mixtures', 'sulfate'): [0, 1, 2, 3, 4, 5], } def grade(submission, answers): if submission.spectrum_id.duplicated().any(): raise ValueError('submission repeats a spectrum_id') if set(submission.spectrum_id) != set(answers.spectrum_id): raise ValueError('submission ids do not match the test set exactly') sub = submission.set_index('spectrum_id').reindex(answers.spectrum_id) the stratum is implied by which analytes the key assays, so it is never distributed ferm = (answers[MIXTURE_ONLY].to_numpy(dtype=int) == NOT_ASSAYED).all(axis=1) source = np.where(ferm, 'fermentation_supernatant', 'held_out_mixtures') per_stratum = {} for (stratum, analyte), labels in SCORED_STATES.items(): y = answers[analyte].to_numpy(dtype=int) keep = (source == stratum) & (y != NOT_ASSAYED) if not keep.any(): continue p = pd.to_numeric(sub[analyte], errors='coerce').to_numpy(dtype=float)[keep] p = np.clip(np.rint(np.where(np.isfinite(p), p, 0)), 0, N_BANDS).astype(int) per_stratum.setdefault(stratum, []).append( f1_score(y[keep], p, labels=labels, average='macro', zero_division=0)) scores = [float(np.mean(v)) for v in per_stratum.values()] return float(W_MEAN * np.mean(scores) + W_WORST * np.min(scores)) The test set holds one spectrum per physical sample. The mixture corpus carries up to six replicate spectra of a mixture and the fermentation corpus two per draw; only one of each is kept, so every test row is its own group. Any split of these rows into a public and a private half is therefore group-disjoint by construction - no sample, and no replicate of one, can sit on both sides - and no ordering trick is needed to achieve it. The rows are then ordered by a hash of the spectrum id and nothing else. That order is deliberately not stratified: an order that spread the rare states evenly through the file would encode the labels in row position, and a solver reading position would recover them. Because every row is a distinct sample, any contiguous or random half is a uniform sample of the whole, proportional in expectation, and the frozen scored list above guarantees that both halves score the same cells and the same states however the rows happen to fall. That fixes the resolution of the leaderboard, which is worth stating plainly. Measured over 400 random halves of the reference submissions, a half-test score differs from the full-test score with a standard deviation of about 0.010 to 0.020: 0.008 from the 1,523-sample mixture stratum and 0.030 from the fermentation stratum, which is only 189 samples and is the resolution limit of the source corpus rather than of this split. Read a leaderboard gap smaller than roughly 0.04 as noise rather than as a result. Predictions are rounded and clipped into the state space and non-finite values are read as 0, so there is nothing to gain from emitting anything outside {0..5}. Duplicate spectrum_ids and ids that are not in the test set are rejected outright rather than silently dropped. Score range 0.0 to 1.0, higher is better. Reference points measured on this split: submission mixtures fermentation score sample_submission.csv (training mode) 0.099 0.080 0.086 every analyte predicted absent 0.088 0.208 0.124 per-analyte logistic, SNV, largest corpus only, 0.581 0.251 0.350 in-distribution model selection the same pipeline with a Savitzky-Golay 0.602 0.564 0.575 first derivative perfect prediction 1.000 1.000 1.000 The gap between the last two rows is a single preprocessing choice. It moves the fermentation stratum far more than the mixtures - which is the shape of this problem: the decisions that matter are close to invisible to any in-distribution measurement you can make. Dataset Three Raman corpora. Every intensity column is named by its Raman shift in wavenumbers (cm^-1). The training corpora keep their native, non-uniform spectrograph axes - the step varies along each axis and differs between corpora - so they cannot simply be concatenated. The test spectra are resampled onto one uniform documented grid and pooled. public/ train_spectra_substratemix.csv 3,872 spectra, 1,870 channels, 390.63-3384.70 cm^-1 train_spectra_ecolimetab.csv 1,920 spectra, 594 channels, 402.05-1598.60 cm^-1 train_spectra_axp.csv 344 spectra, 2,048 channels, -32.15-3384.70 cm^-1 train_labels.csv 5,792 rows: spectrum_id, source, the eight analyte states test_spectra.csv 1,712 spectra, 1,451 channels, 400-3300 cm^-1 at 2 cm^-1 concentration_bands.csv detection floor and all four band cut points, per analyte scored_states.csv the frozen scored states, per (stratum, analyte) cell sample_submission.csv 1,712 rows, the training mode of each analyte Columns: spectrum_id - string, row identifier, unique across the dataset. source - string, which training corpus a spectrum came from; in train_labels.csv only. the eight analyte names - int, concentration state 0-5, or -1 where that corpus did not assay the analyte. numeric column names - float, Raman intensity at that wavenumber, in that corpus' own arbitrary units. The test set holds one spectrum per physical sample. The mixture corpus has up to six replicate spectra of a mixture and the fermentation corpus has two per draw; only the first of each is used, and no sample is represented twice. Nothing about a sample can therefore appear on both sides of any later split of these rows. Properties that drive the task: Intensity units are arbitrary and differ between corpora. Absolute intensity is a nuisance variable; band shape and relative structure carry the signal. The mixture corpus additionally varies its antifoam content, which changes overall signal strength independently of composition. Analyte coverage is ragged. substratemix assays all eight, ecolimetab assays only glucose and acetate, and axp assays none and appears in no row of train_labels.csv. A -1 means not assayed, never absent - training an analyte on -1 rows silently teaches it that the analyte was missing. train_spectra_axp.csv is an auxiliary corpus of nucleotide mixtures in a deep-eutectic solvent. It carries none of the eight analytes and is offered for representation learning; it may be ignored. States are imbalanced, and imbalanced differently per analyte. EnPump, nitrate and yeast extract are absent from most mixtures; glucose and acetate are present in nearly all of them. Macro-F1 gives the rare states equal weight. ecolimetab covers only 402-1599 cm^-1 and cannot contribute outside that window. Submission A CSV with one row per test spectrum_id, and exactly those ids. spectrum_id - string, matching test_spectra.csv. glucose, glycerol, acetate, enpump, nitrate, yeast_extract, phosphate, sulfate - int, predicted state 0-5. Must contain exactly 1,712 rows plus a header, with no duplicated and no unknown spectrum_id. Expected Methods Suitable approaches include row-local scatter and baseline correction (standard normal variate, polynomial or asymmetric-least-squares detrending, Savitzky-Golay smoothing and derivatives), interpolation of the training corpora onto a shared wavenumber grid, per-analyte multiclass or ordinal classifiers, latent-variable models used as features, and 1D convolutional or attention networks trained from scratch. Because the fermentation shift cannot be reproduced by any split of the training data, the productive uses of validation are leave-one-corpus-out and augmentation that imitates instrument and matrix variation: intensity rescaling, smooth multiplicative and additive baselines, wavenumber shift and stretch, resolution blur and added interferent bands. Note that the preprocessing that wins one cell frequently loses another, that an in-distribution split and a leave-one-corpus-out split do not rank the same recipes, and that the boundary separating absent from band 1 is the single most transferable decision you have to get right. What Not To Use From scratch only. No pretrained model, pretrained embedding, spectral library, reference database or externally fitted chemometric model. Deep models fitted to these very corpora are published; every parameter here must be learned from the supplied spectra during the run. Each test spectrum must be read independently from its own intensities. Do not pool any statistic across test rows, do not fit or refit any transform, scaler, decomposition, normaliser or model on the test split, do not cluster or group the test rows, and do not feed a prediction for one test row into another. Normalisation computed from a single row's own values is fine, and anything fitted on the training corpora and merely applied to test is fine. This rules out the transductive calibration-transfer toolkit - piecewise direct standardisation, test-set derived orthogonal signal correction, correlation alignment on the test batch, test-time batch-norm adaptation and pseudo-labelling the test set - which is the first family a solver reaches for on a transfer task, and which would turn a transfer benchmark into a batch-alignment exercise. No external spectra or additional training data, no runtime downloads, no hosted LLM or inference APIs. Do not infer targets from row ids, row order, file offsets or any other artefact of how the files were written. Do not hardcode states, decision boundaries or coefficients obtained by inspecting the answers. Every constant must be computed in code from the training files at run time. The published edges in concentration_bands.csv and the published cells in scored_states.csv are part of the task definition and may be used freely. Published Raman band assignments are acceptable if cited in a comment. Constraints The solution must train and predict end-to-end from the provided files within the configured runtime. No internet access during execution. Attribution The spectra are redistributed unchanged from four openly licensed (CC BY 4.0) corpora. The mixture, fermentation and nucleotide corpora are from the automated Raman high-throughput platform described in Lange, C., Seidel, S., Altmann, M., Stors, D., Kemmer, A., Cai, L., Born, S., Neubauer, P., Cruz Bournazou, M. N. (2025), A Setup for Automatic Raman Measurements in High-Throughput Experimentation, Biotechnology and Bioengineering 122(10), 2751-2769; the mixture design is documented in doi:10.1016/j.measurement.2025.118884. The two-analyte metabolite panel is the HTW-KI-Werkstatt RamanSpectraEcoliMetabolites corpus. Those sources publish these data for continuous concentration regression and calibration transfer; the discrete state space, the two-strata worst-stratum metric, the frozen scored cells and the from-scratch and per-row constraints are specific to this challenge.
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Grid Balancing Action Portfolio

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7d292pgq3wpbkqsvrtvgw0qh8ds0r9
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview At the close of each half-hour electricity-market planning window, a system operator sees hundreds of generating and demand-side units, each with a submitted physical plan, operating limits, and a ladder of bid/offer prices and levels. The operator may then accept a variable portfolio of actions: increase some units, decrease others, issue instructions at different times, and revise the physical target trajectory within the period. For each real Great Britain balancing-market episode, predict that complete portfolio. This is not a scalar imbalance-price forecast and not an independent yes/no classification of one bid. One output row is an ordered, variable-length JSON list of unit/direction action choices. Every chosen action also needs its instruction time and accepted physical-level trajectory. The candidate universe is provided as a compressed NumPy set. Candidate IDs are episode-local and opaque. Stable pseudonymous unit tokens let a model learn a unit's behavior across training episodes without exposing the upstream unit name. All physical values are MW and all bid/offer prices are GBP/MWh. Task For every test episode: decide which candidate action_id values are accepted; estimate the first instruction time in minutes relative to period start; estimate the accepted absolute physical level over one or more within-period trajectory segments; and order non-concurrent actions by predicted instruction time. An offer means increasing net generation or reducing demand, represented by direction = +1. A bid means decreasing net generation or increasing demand, represented by direction = -1. Accepted levels are **absolute target physical levels**, not changes from zero. Use pn_mean_mw, the full PN trajectory summaries, and the direction when reasoning about action magnitude. Training rows include the full target portfolio_json. Test rows include only their candidate archive. Learn one model from the supplied training set and produce one portfolio per test ID. This is a From Scratch challenge. Model weights must be randomly initialized and trained only on the supplied public training data. The requested platform tier is one NVIDIA A10G GPU. The runtime budget is 90 minutes with 10 CPU cores and 62 GB RAM. A small set/candidate encoder plus an autoregressive or ranking-and-regression head is sufficient; giant foundation models are neither needed nor allowed. The recorded dispatch is not claimed to be the unique solution of a fully observed optimization problem. Network, security, reserve, and operator constraints are not all present in these feeds. The learning goal is the historical conditional distribution of recorded actions, and the metric gives partial credit for correct portfolio members, time, trajectory, and order. Public files | Item | Description | |---|---| | train.csv | labeled training episodes | | test.csv | unlabeled test episodes | | sample_submission.csv | valid learned train-prior submission and exact CSV/JSON schema | | train/*.npz | candidate-set tensors for training episodes | | test/*.npz | candidate-set tensors for test episodes | | DATA_README.md | compact loading note | The final frozen split has 668 training periods from 14 contiguous days and 240 test periods from five later contiguous days. IDs are salted and source-neutral. CSV files are sorted by ID; row order carries no chronology. CSV columns train.csv: | Column | Type | Description | |---|---|---| | id | string | opaque episode ID | | episode_path | string | relative path to one training NPZ | | portfolio_json | string | canonical target action portfolio | test.csv: | Column | Type | Description | |---|---|---| | id | string | opaque episode ID | | episode_path | string | relative path to one test NPZ | Load an episode with numpy.load(path, allow_pickle=False). Each NPZ contains: | Key | Shape/type | Description | |---|---|---| | features | [n_candidates, 29] float32 | candidate feature matrix | | candidate_ids | [n_candidates] Unicode | legal action_id values for this row | | unit_tokens | [n_candidates] Unicode | stable pseudonymous unit identities | | directions | [n_candidates] int8 | +1 offer or -1 bid | | context | [6] float32 | period and system context | | feature_names | [29] Unicode | column names for features | | context_names | [6] Unicode | element names for context | The 29 candidate features, in order, are: direction, pn_mean_mw, pn_start_mw, pn_end_mw, pn_range_mw, mel_max_mw, mil_min_mw, headroom_mw, footroom_mw, directional_flex_mw, best_price_gbp_mwh, worst_price_gbp_mwh, weighted_price_gbp_mwh, available_pair_count, then five pair_k_capacity_mw fields, five pair_k_price_gbp_mwh fields, and five pair_k_available mask fields for k=1..5. The six context values are period_sin, period_cos, weekday_sin, weekday_cos, pn_system_total_gw, and candidate_flex_total_gw. Portfolio JSON schema portfolio_json is a JSON list with zero to 256 action objects. Every action has exactly these keys: { "action_id": "a_0123456789abcdef0123", "instruction_minute": -12.0, "trajectory": [ {"t0": 0.0, "t1": 12.0, "level0": 420.0, "level1": 420.0}, {"t0": 12.0, "t1": 30.0, "level0": 438.0, "level1": 438.0} ] } action_id must match one of the row's supplied candidate IDs and the grader requires the opaque format a_ plus 20 lowercase hexadecimal characters. instruction_minute is finite and lies in [-90, 30]. Negative values are valid instructions issued after the feature cutoff but before period start. trajectory contains 1–32 sorted, non-overlapping segments. Segment t0 and t1 are finite minutes with 0 <= t0 < t1 <= 30. level0 and level1 are finite absolute MW values in [-10000, 10000]. Actions are sorted by (instruction_minute, action_id). Repeated IDs are syntactically allowed, but the native target contains one consolidated action per unit/direction candidate. JSON is capped at 250,000 characters. Duplicate keys, extra keys, NaN, Infinity, and non-canonical list order are invalid. Submit a CSV with exactly id,portfolio_json, in that order. Include every test ID exactly once. File-level structural errors (wrong/reordered columns, duplicate IDs, missing/extra IDs) raise InvalidSubmissionError. A malformed JSON cell is row-local and scores zero for that row. What Not To Use Do not use external data, the internet, Elexon/BMRS/IRIS source lookup, exact or fuzzy temporal fingerprinting, raw archive matching, source filenames, timestamps, modification times, file sizes, row/archive order, public test-label retrieval, hard-coded per-ID outputs, private answers, or any other side channel. Do not use pretrained weights, foundation-model embeddings, hosted/closed APIs, teacher-generated labels, pseudo-labels derived from hidden test outcomes, transductive access to test labels, or inference-only answer caches. Do not reduce the task to a constant portfolio, a fixed top-N merit-order rule, an ID/unit lookup table without learned market-state features, independent thresholding with no portfolio/count/order model, or a parser that copies a target-bearing field. Do not infer offer/bid direction by taking the sign of an accepted level relative to zero: accepted levels are absolute and direction is relative to PN. Do not train on embargo/test periods or use amended, corrected, deemed, at-cutoff, or future acceptance messages. Allowed methods include randomly initialized neural set encoders, temporal models, candidate rankers, constrained decoders, ordinary loss functions and augmentations for numeric data, and classical features computed solely from the provided training inputs. Solutions must fit the stated A10G/CPU/RAM/time budget. Enforcement The grader enforces the complete CSV row set, exact columns/order, unique IDs, JSON length and object-count caps, duplicate-key rejection, finite numeric bounds, action/segment schemas, segment order, and canonical action order. Prohibited external lookup, pretrained models, answer retrieval, hard-coded test outputs, or future/corrected data remain grounds for rejection even when a submission is syntactically valid. Evaluation Actions are matchable only when action_id agrees. Repeated instances of the same ID are paired greedily by a similarity of 45% instruction time and 55% trajectory. For each row: | Component | Definition | Weight | |---|---|---| | Action multiset F1 | 2 * matched / (predicted_count + true_count) | 0.40 | | Instruction similarity | mean max(0, 1 - absolute_minute_error / 20) over matches | 0.15 | | Trajectory similarity | one-minute temporal IoU plus scale-aware absolute-level accuracy over matches | 0.25 | | Tie-aware ordering | concordant matched pairs; true instructions within one minute are ignored as ties | 0.15 | | Count similarity | 1 - abs(predicted_count - true_count) / max(predicted_count, true_count, 1) | 0.05 | Trajectory comparison samples minute midpoints. Its temporal term is the intersection-over-union of predicted and true covered minutes. On intersecting minutes, the level term is max(0, 1 - MAE / (2 * scale)), where scale = max(25, 0.15 * mean(abs(true_level)) + 25). Trajectory similarity is 0.45 temporal_iou + 0.55 temporal_iou * level_similarity. If both portfolios are empty, the row score is 1. If only one is empty, the row score is 0. Otherwise the row score is the direct weighted sum in the table, clipped to [0,1]. The overall score is the arithmetic mean over all private rows. There is no nonlinear score cap, exponent, or leaderboard shaping. A perfect submission scores exactly 1.0; the theoretical minimum is 0.0. Frozen full-split checks gave 1.000000 for exact answers, 0.000000 for no action, 0.440820 for the generated learned sample, 0.472539 for a frequency/merit CPU baseline, and 0.470553 for a compact eight-epoch from-scratch CUDA MLP. The CUDA run took 158.9 seconds on a local RTX 3050 6GB, not an A10G. Dataset The inputs are derived from official Great Britain Balancing Mechanism BOD, PN, MELS, and MILS snapshots available at Gate Closure. Native labels are original BOALF acceptance instructions whose acceptance timestamps are strictly after the latest input snapshot. Later amendments/corrections, deemed acceptances, and target-bearing fields are excluded from inputs. The final split is chronological by complete settlement date, with a two-day gap between train and test. No official payload or episode crosses partitions. The public files omit settlement dates, source filenames, raw BM-unit names, acceptance numbers, feature-publication timestamps, and source URLs.
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Manuscript Fragment Collation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7drch7k60ars88y7eectypns8e27z9
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat mrnguyen's score of 0.475!

Full challenge description from page:

> Background Comparing historical manuscript fragments often requires literal, character-level collation rather than mere translation or interpretation. By extracting and aligning transcribed handwritten text, models can explicitly document insertions, deletions, and replacements between related fragments. This task focuses on identifying these literal written differences in handwritten Ethiopic line fragments to produce an executable, canonical edit program. Overview Given paired grayscale images of related handwritten Ethiopic text lines, transcribe the left fragment and generate a structured edit program that transforms its text into the right fragment's text. The comparison requires identifying exact character insertions, deletions, and replacements. Copying shared material alone earns no credit. Pairs are constructed strictly for this computational alignment benchmark; they do not assert historical revisions or manuscript genealogy. From Scratch GPU Task: All trainable parameters must be initialized randomly. Neural training, neural inference, and algorithmic edit decoding must use GPU tensor computation within a single self-contained offline session (90-minute limit). Ordinary host image decoding and CSV serialization are permitted. Dataset Information (Public Files) The public dataset contains pairs of grayscale $48 \times 512$ PNG images. Scaling preserves the aspect ratio with white padding to center the text. The images feature seeded Gaussian noise, contrast changes, and brightness shifts that alter appearance without affecting the underlying text labels or positions. +-----------------------+------------------------------------------------------------------------+ | File / Directory | Purpose | +-----------------------+------------------------------------------------------------------------+ | images/ | Two single-channel uint8 PNGs per comparison (48x512). | | train.csv | 4,000–6,000 training comparison queries; see train.csv. | | test.csv | 700–1,000 evaluation queries; see test.csv. | | train_answers.csv | Ground-truth targets (anchor_text and edit_program) for training rows. | | sample_submission.csv | Format-example rows for test IDs with placeholder targets. | +-----------------------+------------------------------------------------------------------------+ Split and reuse controls: training and evaluation are built from separate image pools before pairs are formed. Evaluation uses an older-manuscript pool; the random evaluation pool is excluded. Every evaluation image is screened against all training-pool normalized transcriptions and decoded grayscale pixel hashes, including training records that are later filtered out. Any exact text or pixel match is excluded. Within each pool, duplicate texts and decoded images are removed, and each retained image is used in at most one pair, on either side. Thus no left or right evaluation image is reused in training pairs, and no evaluation anchor transcription is an exact training-pool transcription. Pair selection requires shared words and a character-sequence similarity ratio between 0.35 and 0.85. These are exact-duplicate and image-reuse guarantees; writer- or page-disjointness is not established. Common characters and words can occur in both splits. The CSV row counts are authoritative; preparation requires at least 4,000 training pairs and 700 evaluation pairs. Feature Schema train.csv and test.csv +---------------+--------+--------------------------------------------------------+ | Column | Type | Description | +---------------+--------+--------------------------------------------------------+ | comparison_id | String | Opaque unique identifier for the line-pair comparison. | | left_image | String | Relative path to the left fragment image. | | right_image | String | Relative path to the right fragment image. | +---------------+--------+--------------------------------------------------------+ train_answers.csv +---------------+--------+-----------------------------------------------------------------------------+ | Column | Type | Description | +---------------+--------+-----------------------------------------------------------------------------+ | comparison_id | String | Opaque unique query identifier matching the input CSVs. | | anchor_text | String | The NFC Unicode transcription of the left image. | | edit_program | JSON | A structured array of instructions mapping the left text to the right text. | +---------------+--------+-----------------------------------------------------------------------------+ Target JSON Schema The output must supply the anchor_text (left fragment transcription) and the edit_program. anchor_text: A string of at most 160 NFC-normalized Unicode codepoints. Outer whitespace is trimmed; internal whitespace and punctuation are preserved. Control characters below U+0020 are prohibited. edit_program: A JSON array of two-item instructions [opcode, argument] transforming the anchor into the target text. ["=", n]: Copy the next n anchor characters unchanged and consume them. ["-", n]: Delete the next n anchor characters and consume them. ["+", text]: Insert text before the current anchor position; consume nothing. ["~", text]: Replace the next length-of-text anchor characters with text and consume them. Instruction Constraints: n must be a positive integer ($1 \le n \le 160$). Booleans and decimals are invalid. text must be a nonempty NFC-normalized string (at most 160 codepoints) containing no control characters below U+0020. Empty instructions are not permitted. The complete program must strictly consume the entire anchor, produce a target of at most 160 characters, and contain at most 320 instructions and 6,000 JSON characters per row. Canonical Minimum-Cost Alignment: The edit program must be mathematically canonical. Cost rule: Copy costs 0; insert, delete, and replace cost 1. Tie-breaking order: Trace the suffix edit cost matrix $D(i,j)$ breaking ties in the following order: match (=), replace (~), delete (-), insert (+). Merging: Adjacent instructions of the same type must be merged (add counts for = and -; concatenate literals for + and ~). Note: A noncanonical program is invalid and yields a score of zero, even if it reconstructs the correct text. Evaluation Metrics Predictions are decoded into change-atoms representing specific edits relative to zero-based anchor positions. Deletion: ('-', anchor_position) Replacement: ('~', anchor_position, replacement_character) Insertion: ('+', anchor_position, insertion_offset, inserted_character) (Copied characters yield no change atoms. insertion_offset preserves character order within a single insertion site.) Let $P$ and $T$ be the predicted and true sets of change-atoms, and $M = \vert{}P \cap T\vert{}$. The reference always contains at least one changed character; therefore, a copy-only or empty prediction receives zero change credit. 1. Precision-Weighted Change Score ($F_{0.5}$) $$F_{0.5} = \frac{1.25 \times M}{\vert{}P\vert{} + 0.25 \times \vert{}T\vert{}}$$ 2. Anchor Quality ($A$) Let $E$ be the ordinary unit-cost character edit distance between the predicted anchor ($PA$) and the true anchor ($TA$). $$A = \max\left(0, 1 - \frac{E}{\max(\text{len}(PA), \text{len}(TA), 1)}\right)$$ 3. Row Score and Final Score $$\text{Row Score} = A \times F_{0.5}$$ The final competition metric is the unweighted arithmetic mean of all row scores across the test set. Scores range from $0.0$ to $1.0$ (higher is better). A perfect reconstruction scores exactly $1.0$. Sample Submission Format Submit a UTF-8 encoded CSV file containing exactly three columns in this order: comparison_id,anchor_text,edit_program. Include every test ID exactly once. Quote JSON strings according to standard CSV formatting rules. Empty anchor text is represented by an empty string. comparison_id,anchor_text,edit_program example_comparison,,[] 123abc456def789,"ሀሁ","[[""="",1],[""~"",""ሂ""]]" Parsing Bounds & Rejection: - Malformed text, illegal opcodes, out-of-range counts, noncanonical programs, or JSON exceeding size bounds score 0.0 for that specific row. - Wrong columns, missing/extra/duplicate IDs, unreadable CSVs, or a file larger than 64 MiB result in a global score of 0.0. - Row order does not affect grading. What Not To Use To rigorously evaluate from-scratch visual architecture efficiency and character-level alignment mapping: Train-From-Scratch Only: All learned parameters must be randomly initialized. Pretrained weights, foundational models, or external checkpoints are strictly prohibited. No External Data or Transcriptions: Use only the public training examples. No external datasets, dictionaries, or internet lookups may be used. No Exploitation: Do not use matching against external image collections, hosted inference APIs, manual test transcription, hard-coded test IDs, or test-answer-driven model selection. Test images are for forward inference only. &nbsp;
> $700 Pool
> Closes in 7h 11m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Water Optical Reference Matching

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fqmwz5m9qhe7a3jxxarsqb58c2q3w
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat jlm99's score of 0.594!

Full challenge description from page:

> Water Optical Reference Matching Overview For each test measurement, predict which of six reference cards best approximates its missing optical window, and which of five water-clarity bands contains its measured Secchi depth. The inputs come from real, co-located aquatic reflectance and water-quality observations. Reflectance describes how the water's optical signal varies across wavelengths. Secchi depth measures how far a visibility disk can be lowered before it disappears. Optical spectra can help estimate this clarity, but pigments, particles and dissolved material make the relationship imperfect. Each query exposes 16 values from the outer parts of a spectrum. Its 16-value middle window is hidden. Six cards contain middle-window sequences from a separate reference bank. The selected card is the unique closest approximation to the hidden measured window, as defined below. The cards are references, not six proposed identities for the original measurement. No card comes from a test query. This is a CPU From-Scratch learning task. Train a model on the public labeled sequences and generalize to measurements from held-out contributors. No pretrained models or external datasets are needed or permitted. Dataset Files | File | Contents | | --- | --- | | train.csv | Query features and the training target answer_json. | | test.csv | The same query feature columns, without answer_json. | | sample_submission.csv | Valid independently generated example predictions with the required output schema. | | dataset_metadata.json | Generated counts, feature/target/submission column lists, packet dimensions, token vocabularies, clarity boundaries, reference-selection policy and shared instruction. | The supplied source snapshot contains 2,739 measurements. The original contributor split is preserved: 1,893 measurements on the training side and 846 on the held-out side. From the training side, 284 measurements belonging to three contributors are reserved exclusively for references. They never become training or test queries. Training queries come from the remaining 16 training contributors; held-out queries come from 11 different contributors. The verified snapshot produces 1,539 training queries and 786 test queries. Generation excludes equal-best-distance ties and removes redundant or conflicting identical public inputs. Five held-out measurements in a sparsely represented water context are not evaluated. dataset_metadata.json records the actual generated counts and exclusion categories; counts are not inferred from the former challenge version. The reference bank is fitted and selected entirely from the original training side. Its donor membership does not depend on test spectra, Secchi values, answers, or the number of other test queries. The same frozen bank serves both splits. Candidate vectors can recur, but each card within a row is distinct. All six cards have the same training-reference origin, including the correct one, so "find the only unseen bridge" does not identify the answer. Columns | Column | Type | Meaning | | --- | --- | --- | | id | string | Unique case identifier. Its wow2 prefix identifies this format; two short tags encode the already-public water and difficulty groups. The digest does not encode either answer. | | validation_group | string | Opaque contributor grouping key. Use it for grouped validation, not as a model feature. | | water_context | string | Broad nominal water-body stratum: WATER_CLASS_ALPHA, WATER_CLASS_BETA, or WATER_CLASS_GAMMA. These are categorical aliases, not an ordered clarity scale. | | slate_difficulty | string | HARD or MIXED, describing how the reference slate was assembled. | | packet_json | JSON-encoded string | Outer optical tokens and six candidate reference windows, with the schema below. | | answer_json | JSON-encoded string; training only | Exactly selected_card and clarity_token. Neither field is present as a test column. | All available per-query modeling information is in water_context, slate_difficulty, and packet_json. Raw identities, contributor names, dates, coordinates, exact Secchi measurements and raw reflectance are not participant features. Do not split related training rows at random: use GroupKFold or GroupShuffleSplit on validation_group. Reference contributors are separate from every query contributor, including contributors used for local validation. The official test retains previously held-out contributors; old training queries have not been moved into test. Packet Schema Every packet_json object contains: outer_positions: 16 ordered strings, OUTER_00 through OUTER_15. outer_tokens: 16 integers from 0 through 31. The first ten are the shorter-wavelength section and the last six are the separated red-edge section. bridge_positions: 16 ordered strings, BRIDGE_00 through BRIDGE_15. candidate_cards: six objects, in CARD_A through CARD_F order. Each contains card_id (string) and bridge_tokens (16 integers from 0 through 31). token_min: integer 0. token_max: integer 31. Wavelength-wise log-reflectance centering and scaling are fitted on the original training side only. Standardized values are clipped to -3,3] and placed into 32 equal bins. Identical transformations apply to queries and references; no statistic is fitted on test measurements. For HARD rows, the cards are the six nearest same-context reference observations by outer-window distance. For MIXED rows, two are the nearest references and four are sampled without replacement from the remaining same-context references. Outer-window distance is mean squared distance between the 16 standardized outer values, before tokenization. Candidate ordering uses an independent deterministic shuffle for each query, not a cycle based on row rank. Exact position counts are not forced to balance. The shared instruction is stored once in metadata: Choose the reference card closest to the missing measured optical window, then predict the measured clarity band. dataset_metadata.json also provides feature_columns, public_columns (an alias of feature columns), train_columns, test_columns, target_columns, and submission_columns. The shared answer_format object is: { "required_keys": ["selected_card", "clarity_token"], "selected_card_values": ["CARD_A", "CARD_B", "CARD_C", "CARD_D", "CARD_E", "CARD_F"], "clarity_token_values": ["CLARITY_0", "CLARITY_1", "CLARITY_2", "CLARITY_3", "CLARITY_4"] } There are no constant prompt or answer_format_json columns repeated across the CSV files. Targets Let h[j] be the query's hidden measured bridge token at position j, and let b[c,j] be card c's visible reference token. The correct selected_card uniquely minimizes: reference_error(c) = sum((b[c,j] - h[j]) ** 2 for j in 0..15) This is squared error in the released token representation, not a distance in metres or raw reflectance. Exact equal-best ties are excluded rather than accepting one arbitrary card. The hidden query bridge is not released. Reference selection uses the visible-side outer measurements; hidden bridge values are used only to assign the supervised target and identify ties. Clarity Bands The clarity target comes from the query's own measured Secchi depth, not from a reference donor: | Token | Measured Secchi depth | | --- | --- | | CLARITY_0 | Less than 0.4 m. | | CLARITY_1 | At least 0.4 m and less than 0.8 m. | | CLARITY_2 | At least 0.8 m and less than 1.5 m. | | CLARITY_3 | At least 1.5 m and less than 3.0 m. | | CLARITY_4 | At least 3.0 m. | Evaluation The metric is chance-corrected weighted accuracy with weakest-group components, between 0 and 1; higher is better. Row Score For one row: card_score is 1 for the exact selected card and 0 otherwise. clarity_score is 1 for an exact clarity token, 0.55 for one band away, 0.20 for two bands away, and 0 for larger errors. joint_score is 1 only when both predictions are exact. raw_row = 0.45 card_score + 0.45 clarity_score + 0.10 * joint_score The two main terms give equal importance to selecting a useful optical reference and estimating measured clarity. The smaller joint bonus rewards getting both right. Its overlap is intentional: a perfect row scores exactly 1, not more than 1. Clarity adjacency gives graded credit for an ordered measurement rather than treating every wrong band equally. Chance Correction For true clarity token y, the uniform-guessing reference is: clarity_chance(y) = mean(clarity_score(k, y) for k in the five clarity tokens) row_chance(y) = 0.45 / 6 + 0.45 * clarity_chance(y) + 0.10 / 30 Group Aggregation For a nonempty set of scored rows S: corrected(S) = clip( (mean(raw_row over S) - mean(row_chance over S)) / (1 - mean(row_chance over S)), 0, 1 ) score = 0.75 * corrected(all scored rows) 0.15 * min(corrected(each present water_context group)) 0.10 * min(corrected(each present slate_difficulty group)) The overall term dominates. The smaller group terms discourage sacrificing an entire water stratum or the harder reference slates. min means the smallest corrected group mean, not a per-row minimum. Only groups present in the evaluated partition are included; absent groups contribute no artificial zero. A partition with one present group uses that group's score. These conventions also apply to small evaluator fixtures. Every component is in [0,1], so their weighted sum is also in [0,1]. A known-answer submission scores 1. Uniform random guesses have score near zero, but clipping and finite samples mean that a random or sample submission need not score exactly zero. This is a uniform-guessing correction, not correction against a learned majority baseline. The same formula is applied separately to public and private leaderboard subsets. Backend-supplied answer visibility takes precedence; the standalone evaluator has a deterministic 40%/60% case-hash fallback. That fallback splits cases, not contributors, between leaderboard subsets. Train/test contributors remain disjoint. Predictions cannot change their evaluation groups or board membership. Submission Write a CSV with exactly id,answer_json in that order. Both fields are strings. Include every required test ID exactly once, with no extra rows or columns. answer_json must parse as one object with exactly two string-valued keys, selected_card and clarity_token, using the allowed vocabularies above. Example formatting: id,answer_json wow2_a_h_0123456789abcdef01234567,"{""selected_card"":""CARD_D"",""clarity_token"":""CLARITY_2""}" The example ID illustrates syntax; use the real test IDs. The CSV uses doubled quotes inside a quoted field. Missing or duplicate IDs, invalid tokens, repeated JSON keys, malformed JSON, multiple card selections and unexpected fields are rejected. Row order does not affect the score. Do not add scoring-group columns to your submission. The grader tolerates a reserved visibility column only when a backend supplies it; its prediction-side values are ignored. Runtime and Method Rules Train and infer on CPU within the configured platform limit. Learn from the released training labels using a model initialized from scratch. CPU sequence encoders, metric-learning models, tree models or other supervised algorithms are permitted. Do not use pretrained weights, external training data, hosted inference APIs, online services, raw upload files, private answers or preparation scripts as prediction oracles. Do not search optical archives to recover source measurements or exact hidden Secchi values. Opaque IDs and source-derived fingerprints must not be reverse-mapped. Do not hardcode test answers, IDs, card positions or known packet-to-answer maps. Do not fit a model to the unlabeled test collection or use cross-test candidate-frequency rules to infer answers. Use validation_group only for grouped validation. Learn the spectral mapping from training examples rather than predicting from identifier digests or row order. Expected Output The solution entrypoint is: python3 ./[solution.py PUBLIC_DIR SUBMISSION_OUT Read the public files from the first argument and write the two-column submission to the exact second-argument path. There is no participant need for the creator's reference provenance or hidden measured bridge values. &nbsp;
> $700 Pool
> Closes in 7h 47m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## COVID-Era Cough, Breath, and Voice Session Matching

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7amasb27bwyfnwst13d458xd8bmjfp
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat nsndtrai's score of 0.436!

Full challenge description from page:

> COVID-Era Cough, Breath, and Voice Session Matching Overview The objective is to restore which breathing and vowel recordings belong to each of four anonymous cough recordings. For every case, predict four BREATH_i+VOICE_j tokens in COUGH_0, COUGH_1, COUGH_2, COUGH_3 order. Every breath card and every voice card must be used exactly once. The recordings come from an authentic crowdsourced respiratory-sound study created during the COVID-19 pandemic. A participant contributed cough, breathing, and sustained-vowel recordings in one collection session. During a research archive migration, the three views from four metadata-matched participants were detached and independently shuffled. This is not a COVID-19 diagnosis task. COVID status and all demographic fields are withheld and are used only during preparation to make the four participants in a case difficult to distinguish through population-level shortcuts. Solvers must learn cross-view acoustic identity and respiratory consistency from the released training allocations. Dataset Files train.csv - 266 labeled four-participant allocation cases. test.csv - 103 held-out participant cases without allocation_sequence. sample_submission.csv - Random valid allocations in the required format. train_case_ids.npy and test_case_ids.npy - Case IDs aligned to the first axis of the corresponding map arrays. train_cough_maps.npy and test_cough_maps.npy - Four cough maps per case. train_breath_maps.npy and test_breath_maps.npy - Four independently shuffled breathing maps per case. train_voice_maps.npy and test_voice_maps.npy - Four independently shuffled sustained-vowel maps per case. Every map array has shape (cases, 4, 64, 128) and dtype uint8. Values are deterministically derived from authentic audio by resampling, active-region cropping, log-mel conversion, and per-recording channel normalization. The normalization suppresses static microphone equalization while retaining time-frequency respiratory structure. No generated audio or synthetic target label is used. The visible source index contains 1,476 eligible participants from 15 authentic collection batches. The source is split by participant before cases are built: 1,064 participants form 266 training cases and 412 different participants form 103 test cases. Every participant occurs in exactly one case; none is reused or excluded. The private preparation audit reports source count, split counts, participant usage, and the zero-unassigned coverage assertion. Train and test participants are disjoint, so the same person, cough, breath, or voice recording cannot be linked across rows or splits. The hidden leaderboard split contains 36 public and 67 private test cases. Both boards use the same flat per-case metric and fixed four-participant case structure. CSV Columns case_id string) - Opaque case identifier. cough_card_ids_json JSON list) - The four cough anchor IDs in map-array order. They are always COUGH_0 through COUGH_3. breath_card_ids_json JSON list) - The four row-local breathing IDs in map-array order. They are always BREATH_0 through BREATH_3. voice_card_ids_json JSON list) - The four row-local voice IDs in map-array order. They are always VOICE_0 through VOICE_3. answer_format_json JSON object) - Machine-readable output constraints. It specifies the output field, four-token count, token pattern, and the one-to-one rule for both detached views. allocation_sequence string, train only) - Four paired card tokens in cough-anchor order. The participant IDs, original filenames, collection dates, locations, ages, sex values, health records, COVID statuses, selected native modality names, and source archive paths are not released in the challenge files. Evaluation For one case: BreathCardAccuracy is the fraction of the four cough positions assigned the correct breathing card. VoiceCardAccuracy is the fraction assigned the correct voice card. CompleteTripletAccuracy is the fraction for which both detached cards are correct for the same cough anchor. ExactReconstruction is 1 only when all eight card assignments are correct. The final score is the flat mean across cases: Score = 0.30 * mean(BreathCardAccuracy) 0.30 * mean(VoiceCardAccuracy) 0.25 * mean(CompleteTripletAccuracy) 0.15 * mean(ExactReconstruction) The components are calculated independently. Every case has equal weight. The score ranges from 0 through 1, and higher is better. Submission Submit a UTF-8 CSV with exactly these columns in this order: case_id,allocation_sequence CTR_0123456789abcdef01,BREATH_2+VOICE_1 BREATH_0+VOICE_3 BREATH_3+VOICE_0 BREATH_1+VOICE_2 CTR_fedcba9876543210ab,BREATH_1+VOICE_3 BREATH_3+VOICE_0 BREATH_0+VOICE_2 BREATH_2+VOICE_1 Requirements: Include every test case_id exactly once. Use exactly four space-separated BREATH_i+VOICE_j tokens per row. Token position corresponds to COUGH_0 through COUGH_3. Use each of BREATH_0 through BREATH_3 exactly once per row. Use each of VOICE_0 through VOICE_3 exactly once per row. Do not include missing, duplicate, or unknown IDs. Do not add columns. Compute And Modeling Requirements Compute tier: CPU, using at most 10 CPU cores and the platform memory limit. The full run must finish within 1.5 hours. Train a joint cross-view audio model from scratch on the provided training cases. Every learned parameter must be fitted on these files. The effective prediction path must use cough, breath, and voice maps. Train a compact encoder or matching model within the CPU runtime. Constrained bipartite or multi-view assignment decoding is permitted. Prohibited Pretrained weights of any kind, including speaker-verification, biometric, respiratory, speech, audio-foundation, or image backbones. External cough, COVID-19, respiratory, speech, voice, or speaker datasets. Network access, hosted APIs, remote inference, or package installation at run time. Matching released maps against the underlying source archive, mirrors, cached audio, participant records, or source filenames. Recovering source participant IDs, dates, locations, health records, or archive batches. Using case IDs, CSV row order, array position across cases, or fixed card positions as predictive features. Exact-duplicate lookup, hardcoded answers, private files, grader exploitation, or filesystem side channels. A single-view, card-position, metadata-only, fixed-rule, nearest-duplicate, or constant-permutation system as the primary solution. Source And License The prepared maps are modified derivatives of an authentic public respiratory-sound research corpus distributed under the Creative Commons Attribution 4.0 International license. The exact repository and pinned source revision are intentionally omitted from this participant-facing description to prevent reverse matching. Complete provenance, attribution, transformation, and license evidence is supplied to platform reviewers with the source dataset. This benchmark supports research evaluation only. It is not a medical device and must not be interpreted as clinical advice or a COVID-19 diagnostic test. Expected Output Your script receives ` and ` as two positional arguments. Write the result to `` as a CSV with exactly the columns case_id,allocation_sequence. Each allocation must contain four space-separated BREATH_i+VOICE_j tokens. Detailed validity rules are listed in Submission. &nbsp;
> $700 Pool
> Closes in 7h 51m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Sorani Reference-Guided Writer Disentanglement

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71x46zfdzwyt5bemd5yzxkr98dwqgw
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Background Recover a requested writer's complete Sorani lines from a shuffled board of image fragments. Sorani uses an Arabic-derived script written right-to-left. A fragment may contain only part of a word, so identifying a writer, grouping fragments into lines and recognizing text must be solved together. The input does not contain intact candidate lines. Overview The first two strips show independent handwriting references from one writer. Below a gray divider, a board mixes fragments from exactly two writers, with two or three lines per writer. Each line is cut into three contiguous vertical pieces, covering the entire line image without deletion or overlap. All twelve or eighteen pieces are shuffled independently onto a three-column board. Pieces remain upright; their original left/middle/right roles, line membership and writer are not labeled. Use the reference handwriting to select the requested writer's fragments, reconstruct that writer's two or three complete lines and transcribe them. Return exactly line_count strings. Order reconstructed lines by the row-major position of their rightmost original fragment on the displayed board. The rightmost fragment is the third piece when the intact image is partitioned from left to right; it is the physical right edge of the line, irrespective of Unicode character ordering. Determining which tile has this role is part of reconstruction. Within each string preserve the normal logical text order. Do not transcribe references or the other writer. Each board has two reference-swapped queries with identical fragment pixels and positions, requesting opposite writers. An unconditional transcription of the board cannot satisfy both. A whole-line writer classifier followed by ordinary line recognition is insufficient because line boundaries, fragment order and line membership are absent. Reconstruction must use handwriting style, cut-edge continuity and textual evidence. Every selected line's three pieces are present, although image corruption can obscure strokes. This is a From Scratch task on one NVIDIA A10G within the configured offline runtime. Initialize model weights randomly and train a visual neural architecture using only the supplied training data. Dataset Information (Public Files) RGB JPEG panels are 768 pixels wide and 792 or 1,048 pixels high. References occupy y=0..255; the gray divider occupies y=256..279. Tile t starts at x=256(t mod 3), y=280+128floor(t/3), with zero-based row-major indices. Each tile measures 256×128 pixels; there are four or six board rows. Each line is fitted within 736×104 pixels before applying light-to-moderate appearance changes on the 0–255 intensity scale: gain 0.9–1.1, offset ±8, one sinusoidal band with amplitude 3–6, zero or one smoothing pass with weight 0.05–0.15, and zero or one faint blotch or one-pixel horizontal artifact with intensity reduction 10–25. Gaussian noise has standard deviation 3–7. White dropout affects 0.05% of channel values, and quantization uses steps of 4. Values are clipped to [0,255]. These changes preserve the text labels and spatial geometry. The line is then cut at floor(width/3) and floor(2*width/3). Each piece fits within 240×104 pixels and is centered on a white 256×128 tile. References receive the same appearance changes but remain intact, right-aligned in 768×128 strips. Panels use JPEG quality 96 without chroma subsampling. images/ Reference-conditioned fragment panels train.csv id,image,line_count,lines test.csv id,image,line_count sample_submission.csv id,lines Feature Schema id is an opaque query identifier; image is the relative JPEG path; line_count is the number of complete lines to return (2 or 3). Training lines is a JSON string array of complete transcriptions ordered by the displayed position of each line's rightmost fragment. There is no public fragment-to-line mapping. Generalization & Leakage Controls A deterministic 80/20 writer split is applied before reference selection and board construction. Both writers and references in an episode belong to the same split. Evaluation writers never appear in training. Two distinct lines are reserved as references per writer; remaining lines are each used in at most one board. Reference strips may recur in different boards for their writer. Both reference-swapped queries stay within one split. Repeated copied paragraphs are omitted. Evaluation text matching normalized training-pool text is excluded, and duplicate decoded image pixels are excluded within and across splits. Reference and candidate texts from the two writers are distinct within each board. Writer identities, fragment mappings, selected tiles and audit records remain private. For internal validation keep all queries involving a writer together. Training and evaluation use the same cutting and rendering rules. Evaluation Metrics Submissions are evaluated using a per-line character Levenshtein distance combined with an exact-match component. 1. Per-Line Credit For each line $i$, the character-level accuracy $A_i$ is computed using normalized Levenshtein distance after NFC and repeated-whitespace normalization: $$A_i = \max\left(0, 1 - \frac{d(p_i, t_i)}{\max(1, \vert{}t_i\vert{})}\right)$$ Where $p_i$ is the predicted line text, $t_i$ is the target line text, and $d(\cdot, \cdot)$ is the character Levenshtein distance. 2. Row Score With $n$ selected candidate lines required by line_count, the row score is a weighted combination of average per-line accuracy and exact line matching: $$\text{Row Score} = 0.8 \times \frac{1}{n}\sum_{i=1}^{n} A_i + 0.2 \times \frac{1}{n}\sum_{i=1}^{n} \mathbb{I}(p_i = t_i)$$ Where $\mathbb{I}(p_i = t_i)$ is $1.0$ if the predicted line exactly matches the target line (after normalization), and $0.0$ otherwise. A wrong array length or non-string line makes the row invalid, scoring $0.0$. 3. Final Score The final competition score is the arithmetic mean of row scores across all test IDs, ranging from $0.0$ to $1.0$ (higher is better). Sample Submission Format Submit a UTF-8 encoded CSV file containing exactly two columns in this order: id,lines. Include one row per test ID with no extra or duplicate IDs. Quote JSON cells and double internal quotation marks. id,lines 9f498f08a388e353b4647e6b,"[""گۆتم کوی"",""گۆتت باشم""]" Parsing Bounds & Rejection: Broken CSV structure, mismatched ID sets, or missing/extra evaluation IDs result in a file-level score of 0.0. A malformed target cell or wrong array length scores 0.0 only for that row. Row order does not affect grading. What Not To Use To ensure fair evaluation of training efficiency and algorithmic design: No External Datasets: Use only the supplied public training data. All trainable model weights must be randomly initialized; pretrained weights and external text corpora are prohibited. No External Services: No internet access, web lookup, hosted inference APIs, or external databases. No Hidden-Label Access: No manual annotation of test rows, hard-coded test-ID answers, external archive copies, or challenge-specific pretrained checkpoints. Train at least one visual neural model on the supplied training examples. Deterministic cropping, writer-matching postprocessors, and decoding are permitted. Test images and the two unlabeled queries of a board may be processed jointly, but no hidden labels or human transcriptions may be used.
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## FareWeave: Hidden Flight-Program In-Context Regression

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74rh0gdf0wpdmfwe7esdmg2989qrc0
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat spyrant's score of 0.795!

Full challenge description from page:

> Overview The same route and booking lead time can produce very different prices under different hidden flight programs. Conventional row-wise fare regression handles part of that variation by using a visible flight identifier. FareWeave removes that identifier and replaces it with case-local evidence: every query arrives with 24 labeled observations drawn from the same anonymous flight program. Your model must infer the local pricing behavior represented by those context records and estimate the normalized log fare of the query record. Evaluation flight programs never occur in training, so memorizing carrier-flight codes or fitting one global route table is insufficient. The task measures conditional regression from an unfamiliar set of examples. The closest standard task family is airline-fare tabular regression, where each observation is predicted independently and carrier or flight codes remain usable features. Set-conditioned meta-regression also consumes demonstrations, but typical benchmarks define synthetic functions or sampled classes rather than hiding a real operational grouping key inside a large relational table. FareWeave combines a group-disjoint operational split, per-query labeled context, reserved query-only records, anonymous categorical vocabularies, and a strictly ordered anchored score. The scored object is therefore not an ordinary fare row: it is a complete hidden-program regression episode. Objective Train a model from scratch using only the released training data. For every row in test.csv, predict the query's normalized log price as one real number from 0.0 through 1.0. Each case contains one query token without a price and 24 context tokens with observed prices. The query and every context token come from the same hidden flight-number group. Context order is independently generated for every case and has no temporal, quality, or ranking meaning. From-Scratch Formulation This is a from-scratch set-conditioned regression challenge. No pretrained fare model, pretrained tabular encoder, external route embedding, or outside price history is required or permitted. A practical model embeds the anonymous categorical codes, combines them with the normalized numerical values, applies one shared encoder to the 24 context tokens, and aggregates the resulting set before conditioning the query prediction. Attention, Deep Sets, or another permutation-invariant architecture can learn which demonstrations are relevant to the query. Use train_groups.csv to validate by complete flight program: every training ID has an anonymous group_id and a predefined fold from 0 through 4. The challenge uses the A10G compute tier. One epoch processes more than 1.5 million context tokens before batching or augmentation. A 50-100 epoch set model therefore evaluates roughly 75-150 million token presentations, making GPU batching the intended route for iteration within the agent time budget. Case Construction Eligible flight programs contain at least 40 source observations. Every source record is deterministically encoded using vocabularies and numerical bounds established by the preparation pipeline. Prices are converted to normalized log space: normalized_log_price = (log(price) - log_price_min) / (log_price_max - log_price_min) Within each flight program, 16 source records are reserved as a query-only pool. The remaining records form a separate context-only pool. A case selects one reserved query and 24 context records from that program. Membership and ordering are keyed deterministically by the program and case index. Query records never appear as context in any case, including another case from the same flight program. Flight number, upstream row index, and source order are removed before release. Case IDs and training group IDs are independently keyed hashes and do not encode a flight program, query record, target value, or fold assignment. Dataset Split Flight program is the independent split unit. Complete programs are assigned to training or evaluation before cases are constructed. The prepared release contains 1,004 independent flight programs: 803 training programs and 201 evaluation programs. Eighty cases are generated per program, producing 64,240 training rows and 16,080 test rows. The test-to-train unit ratio is 25.0%. No source record, flight program, query role, context role, or derived case crosses the training/evaluation boundary. The five supplied training folds are also group-disjoint and approximately balanced by carrier and flight-program price quartile. Files The release contains: train.csv — 64,240 training cases with model inputs and the observed prediction response column. test.csv — 16,080 evaluation cases with the same model inputs and no target. sample_submission.csv — the exact required id,prediction submission schema. train_groups.csv — a training-only id,group_id,fold mapping for leakage-safe validation. data_manifest.json — categorical cardinalities, normalization bounds, row counts, unit counts, fold counts, format version, and metric anchor. Feature Layout Every CSV row is one complete episode. Query columns use the prefix q_. Context columns use prefixes ctx00_ through ctx23_. Each query or context token contains anonymous integer codes for airline, source city, destination city, departure period, stop pattern, arrival period, and cabin class. Each token also contains min-max normalized days_left and duration. A context token additionally contains price, the normalized log price observed for that demonstration. The categorical codes are local release vocabularies, not original names. The categorical cardinalities are 6 airlines, 6 source cities, 6 destination cities, 6 departure periods, 3 stop patterns, 6 arrival periods, and 2 cabin classes. The model must treat each block of 24 context records as a set. Expected Output For every test ID, return exactly one finite prediction in the closed interval [0, 1]. The value must be the normalized log fare of the query token, not a raw currency amount, untransformed log price, context rank, or class label. Submission row order does not affect scoring, but every required ID must occur exactly once. Evaluation The metric is Anchored Exponential MAE. First compute mean absolute error on the normalized log-price targets in the answer subset being evaluated. Then convert that error to a bounded maximize score: score = 10 ** (-MAE / 0.1314) The anchor 0.1314 is the reproducible training-set MAE of the constant training-median predictor, rounded to four decimal places. A perfect prediction scores 1.0; a no-model median forecast scores approximately 0.1; and every increase in MAE strictly lowers the score without a clipped performance floor. Measured release diagnostics establish the intended range. The constant training-median submission scores 0.115, a case-local context-median rule scores 0.177, and a CPU histogram-gradient baseline using the query plus five aggregate context statistics scores 0.553. The exact answer scores 1.0. Progressively degraded predictions are strictly ordered from 1.0 toward zero, and equal-quality group-level perturbations have score standard deviation below 0.00013. Validation Contract File-level structural faults raise a validation error with a specific reason. These faults include missing, extra, duplicated, unknown, or reordered columns; missing, extra, or duplicated IDs; non-finite predictions; non-numeric predictions; and values outside [0, 1]. The grader is deterministic and aligns rows by ID, so reordering valid submission rows cannot change the score. Submission Format Submit a CSV with exactly these two columns in this order: id,prediction fw_0123456789abcdef0123,0.4132 fw_abcdef01234567890123,0.7821 Every id from test.csv must appear exactly once. Predictions must be ordinary finite decimal values in [0, 1]. What Not to Use Do not use external fare histories, live pricing APIs, route databases, web retrieval, or prices copied from another release of the parent table. Do not use pretrained model weights, pretrained tabular representations, or a model trained on an external fare dataset. Do not attempt to recover hidden flight numbers from opaque IDs, row order, CSV byte layout, floating-point representations, or repeated-submission probing. Do not infer evaluation labels from leaderboard probing, submission feedback, or manual test labeling. Do not predict raw currency prices. The required output is the normalized log-price target defined by this release. &nbsp;
> $700 Pool
> Closes in 5h 45m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Annotation Import Fault Attribution from Scratch

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73jwjmksjwv1wvaws4marpkd8amzr8
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat storm's score of 0.883!

Full challenge description from page:

> Annotation Import Fault Attribution from Scratch Overview An annotation importer must decide which records to correct and which to leave alone before they enter a training dataset. This benchmark models a specific failure: an export writes bounding boxes in an offset coordinate frame while the corresponding image files remain unchanged. Several exports are then concatenated without retaining their job identifiers. The resulting boxes have valid numeric ranges and correct class labels, so ordinary schema checks pass even though some annotations are displaced. Your task is fault attribution followed by executable repair. Learn image-to-annotation compatibility within each intact photograph, use that evidence to attribute records to shared export faults, and return an import correction manifest. This is a controlled simulation of the failure mode, not a claim that these incidents occurred in the source corpus. An annotation import queue has merged six images from three export jobs and lost the job membership records. Two jobs used different incorrect coordinate settings, affecting two images each. The remaining two images used the correct setting. Recover two incident records, each linking an affected image pair to its shared repair, and a preservation record for the unaffected images. A shared fault can link visually dissimilar scenes; visual similarity alone does not establish a shared fault. Each case contains six real waste-scene photographs, their observed box ledgers, and nine translation candidates. One candidate is identity, meaning zero translation. Exactly two distinct nonidentity candidates generated the two affected pairs. The images and class labels remain fixed. All nine executions produce legal boxes on every panel, so range checks cannot resolve either the grouping or the repair. Repairs are discrete executable choices, not freely estimated coordinates. Each candidate translates all endpoints in a panel and then snaps them to the 640-pixel grid using round(640 * (raw + offset)) / 640. The selected repair must explain both members of an affected pair, and the submitted ledger must execute it exactly within the stated tolerance. The task does not alter image pixels or discover new boxes: it recovers which supplied coordinate correction accounts for the annotations and which panels share that correction. The photographs depict unrelated scenes. The association to recover is a shared coordinate-setting error, not a common depicted object, fragment adjacency, or a spatial arrangement between images. A solver must infer both the fault partition and its repair: pooling all images assumes a common fault that is absent here, while independent panel choices need not satisfy the shared-job constraints. The learning question is whether image–annotation compatibility learned on training scenes can recover shared fault membership on unseen scenes. Each panel provides evidence for several possible repairs, but the final decision must reconcile that evidence into two distinct shared faults and an unchanged pair. There are 2,520 legal complete assignments. A plausible repair for one image can conflict with the evidence for its proposed partner; choosing the grouping and choosing its repairs are therefore one coupled decision. The executed ledger records the consequences of that decision; serialization itself is not the learned task. The domain is From Scratch. Learn the image–annotation compatibility signal using only the 3,600 released training photographs and their labeled cases. Fit learned representations, feature transforms, calibration, and model parameters only on the training split. Hand-engineered image features are permitted. Pretrained detectors, pretrained weights or features, external training data, hosted inference, and GPU use are prohibited. This isolates learning under the released data and CPU budget; it does not make runtime restrictions or serialization an additional prediction task. Solutions have 90 minutes, 10 CPU cores, and 62 GB RAM. Dataset The prepared release contains: train.csv: 600 labeled six-panel cases, covering 3,600 images. test.csv: 200 unlabeled cases, covering 1,200 images. sample_submission.csv: 200 valid abstentions. images/: 4,800 distinct 640×640 JPEG images. common.py: public reference arithmetic, output construction, and schema validation. Public input columns, in order, are id (opaque string), candidates (JSON array of nine objects), and panels (JSON array of six objects). Training adds incident_repair, a JSON object containing the correct partition and its executed ledger. Test has no target column. A candidate has exactly contract_id (string), dx (finite number), and dy (finite number). Offsets are normalized image coordinates. The row uses a complete 3×3 grid with x and y offsets in {-d,0,+d}, where d is 8/640 or 9/640. The zero-offset candidate has ID identity. Other IDs are case-specific. Candidate order does not indicate the hidden choices. A panel has exactly panel_id (string), image_path (relative JPEG path), class_name (string), and raw_boxes (one to six x1,y1,x2,y2] arrays of finite normalized numbers). Panel order defines the canonical order used in outputs. A panel's supplied class applies to every listed box; it need not describe every visible object in the image. Construction and provenance The source is [keremberke/garbage-object-detection(https://huggingface.co/datasets/keremberke/garbage-object-detection)), revision d8ad1490da2686d7af5c6a7f3d8844f0f9542b0f, under CC BY 4.0(https://creativecommons.org/licenses/by/4.0/)). Source and archive checksums are documented in the creator provenance record. COCO XYWH annotations are converted to XYXY. Source images are perceptually deduplicated before selection and directly resized to 640×640. The retained boxes are at least 3% from the image boundary. Sources are allocated to train and test before grouping into cases, and each selected image appears once. For each case, two distinct nonidentity translations are sampled and assigned to disjoint pairs; the remaining pair uses identity. Hidden source endpoints receive independent subpixel dither in [-0.49,0.49]/640 before inverse translation. Identity panels receive the same dither. Thus even unchanged annotations use the same serialization process, and every candidate's pre-snap distance to the 640-pixel lattice is equal up to floating-point error. The hidden candidate snaps to the source-derived gold endpoint. Repair execution For a candidate and a raw endpoint, execute in this order: x_out = round(640 * (x_raw + dx)) / 640 y_out = round(640 * (y_raw + dy)) / 640 Use Python 3 round-to-nearest-even behavior, including exact halfway cases. Apply the same translation to both corners of every box in an affected panel. Identity has zero offsets and still applies this common snap. Do not snap before translating, clip boxes, change classes, add objects, or reorder boxes. The public common.py implements the arithmetic and output construction. Submitted coordinates must match execution within absolute tolerance 1e-6. Why this execution contract exists The translation grid models a bounded list of possible exporter offsets. Its 8- or 9-pixel spacing is a benchmark parameter, not a claimed industry standard. Snapping expresses how the importer writes recovered endpoints to its 640-pixel annotation ledger. It is applied to every candidate, including identity, and therefore is not a signal that identifies the correct fault. The generated target and the submitted correction use the same reversible protocol. For a source-derived grid endpoint g, a selected repair offset t, and subpixel dither u in [-0.49,0.49], the generator releases raw = g + u/640 - t. The importer executes round(640 * (raw + t)) / 640, recovering g. Each affected pair shares t; the preserved pair has t = 0. The source split is fixed before cases are assembled, and preparation validates the released targets by executing this protocol. The output fields are the import operation's manifest: groups assigns shared correction settings to records, preserve marks records requiring no offset correction, panels supplies the resulting ledger, and context binds that decision to its input. The grader checks that the ledger is the declared operation's consequence before awarding fault-attribution credit. A perfect arithmetic implementation alone does not identify the correct manifest; that decision requires learned visual evidence. Output contract Submit one incident_repair JSON object with exactly these keys. JSON object key order is ignored at every nesting level; array order remains significant. The following is the helper's canonical serialization: groups: two objects, each with contract_id then panel_ids. Use two distinct nonidentity candidate IDs. Each group's panel_ids contains two panel IDs in released panel order. Sort the groups lexicographically by contract_id. preserve: the remaining two panel IDs in released order. panels: six executed panel objects in released order. Each has panel_id then boxes; each box has class_name then bbox. Preserve all counts, classes, and box order. context: exactly candidates and panels, copied from the parsed public input arrays with values and array order unchanged. Nested object key order may differ. Every panel must occur exactly once across groups and preserve. The groups and preserve arrays explicitly declare the inferred job membership; the executed ledger proves the arithmetic consequence of that assignment. Copied context is validated against the private answer before any scoring. For example, construct a complete prediction using the public helper: from common import context, prediction, dumps ctx = context(row) # row is a CSV row mapping learned_choices has six IDs in released panel order: identity twice, and each of two distinct fault IDs twice. cell = dumps(prediction(ctx, learned_choices)) The only abstention has empty groups, preserve, and panels, together with the complete unchanged context. dumps(prediction(ctx)) builds it. Abstention means no decision and earns zero row contributions; it does not declare every image unaffected. Evaluation Invalid JSON, malformed context, invalid partition structure, or non-executed coordinates invalidates the submission. A structurally valid ledger whose context differs from the assigned row must still execute correctly against its supplied context, but earns zero panel and group contributions for that row. This includes a complete prediction copied from another row. It never earns credit for accidentally matching hidden fields. A valid but incorrect partition in the correct context is scored normally. Duplicate JSON keys remain invalid; reordering object keys or adding JSON whitespace does not change a score. For N test cases, let h_ij be 1 if panel j in case i is assigned its hidden contract (including identity), else 0. Let m_i be the number of the two hidden fault groups recovered with both the exact panel pair and exact contract ID. Abstentions contribute zero to both counts. A = sum_i sum_j h_ij / (6*N) G = sum_i m_i / (2*N) panel_skill = max(0, (A - 1/3) / (2/3)) incident_skill = max(0, (G - 1/60) / (59/60)) score = 0.70 panel_skill + 0.30 incident_skill The panel floor is the conservative accuracy of preserving every panel when two of six are unaffected; such an assignment is not a legal completed partition. The incident floor is the expected exact-group match fraction for a uniformly sampled legal partition: a true pair is one of the two selected fault pairs with probability 2/15, and receives its particular nonidentity candidate with probability 1/8, giving 1/60. Normalization occurs after aggregation, not separately per row. Correct grouping with an incorrect decoder earns no group credit. Correct single-panel assignments can earn panel credit even when the complete incident is not recovered. All-correct predictions score 1.0. The official sample abstains and scores 0.0. Coordinates have no approximate-overlap credit because execution is a validity requirement. Submission format The CSV has exactly id,incident_repair in that order, with every test ID once. The sample and private answers use identical columns and ID order. The sample is a complete format example. The grader aligns by ID, permits row reordering, and returns one float per aligned partition. Requirements and prohibited data Train and calibrate only on released training cases, keeping all six panels of a case together in validation. Use both images in a proposed fault group when selecting its shared repair. Stay within the CPU, memory, and runtime limits. Do not retrieve source annotations, reverse-search images, use creator artifacts, exploit opaque IDs or row order, access external training data, or use pretrained representations. The upstream citation is attribution, not permission to access its labels during solving. &nbsp;
> $700 Pool
> Closes in 5h 53m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Auditory Cortex Coactivity Change Estimation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx709jemzt1bmvj11qzg7f1vsd8e4wqa
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat gpt6astra's score of 0.335!

Full challenge description from page:

> Auditory Cortex Coactivity Change Estimation Overview Predict how communication between small regions of auditory cortex changes across two laboratory imaging sessions. For every row, you receive two short calcium-imaging calibration movies from the same mouse, field of view, and auditory stimulus condition. The first movie was recorded at an earlier experience phase and the second at a later phase. Eight requested cortical regions are identified by row-local names such as N01 and N07. Your prediction is a vector of 28 numbers: one change value for every unordered pair of the eight requested regions. The target is a static coactivity-change graph measured from frames that are not released. A positive value means two regions became more correlated in the later session; a negative value means they became less correlated. In plain language, use two brief scans to estimate the reliable network change that would have been obtained from the longer recordings. The recordings come from an open laboratory study of experience-dependent auditory processing in adult female mice. Head-fixed animals heard pup calls, temporally altered pup calls, pitch-shifted calls, and tone sequences while a two-photon microscope recorded calcium-dependent fluorescence in auditory cortex. Original movies contain 256 by 256 pixels sampled at approximately 3.90625 frames per second. Some animals were recorded before pup-care experience, near the first observed pup-retrieval behavior, one day later, and at later follow-up sessions. Other animals contributed repeated-session controls. This is a From Scratch challenge. A practical solution trains a shared spatiotemporal encoder for the earlier and later calcium movies, uses the requested node coordinates to pool regional representations, and predicts graph-edge changes. Fine-tuning a suitable scientific video encoder is also allowed. The output is a fixed static graph fragment, not a future movie, a class label, or a generated sequence. Exact Objective For each test row: Load the earlier and later calibration movies referenced by the two movie indices. Decode the eight node cards into positions on the common 8 by 8 cortical grid. Estimate the hidden-session coactivity change for every node pair. Submit 28 finite values in the required edge order. Every target value is computed from measured fluorescence frames withheld from the public movie bank. No target component is selected from a family template or generated from a row ID. Data Collection and Derived Input Views Each source recording is an aligned two-photon fluorescence movie from one auditory-cortex imaging session. Selected recordings contain at least 420 frames. Longitudinal pairs are formed only when two recordings share the same animal, imaging round, and stimulus signature but belong to different experience phases. Each source movie is processed once: A mean-image phase-correlation step aligns sessions from the same animal and imaging round. A central 224 by 224 region is retained and block-averaged to 112 by 112 pixels. One fixed set of 256 calibration frames is selected as sixteen 16-frame windows distributed through the recording. The same calibration-frame mask is used everywhere that source recording appears. The calibration frames, plus two neighboring frames on either side, are excluded from target computation. A deterministic rotation and optional reflection are shared by every session from the same animal and imaging round. This removes source-coordinate lookup while preserving longitudinal geometry. The public movie bank has shape 251 x 2 x 256 x 112 x 112 and data type uint8. Axis 0 selects an anonymous source movie. Axis 1 contains two channels. Axis 2 contains 256 calibration frames in chronological window order. Axes 3 and 4 are cortical image coordinates. Channel 0 is robustly scaled log fluorescence. Channel 1 is robustly scaled positive frame-to-frame fluorescence change. The first frame of each 16-frame calibration window has zero change. Both channels use the integer range 0 through 255. Per-recording robust scaling removes absolute microscope gain as a shortcut. Models may map integers to the interval [0, 1] by dividing by 255. How the Hidden Graph Is Defined The 112 by 112 aligned field is divided into an 8 by 8 grid. Each grid node contains a 14 by 14 pixel region. For one source recording, target construction uses only the withheld frames: Average fluorescence within each of the 64 grid regions at every withheld frame. Apply log(1 + x) to each regional time series. Keep the withheld frames grouped by the same sixteen evenly spaced temporal segments used for calibration sampling. Within each segment and each regional series, subtract the segment mean and divide by the segment standard deviation plus 0.000001. Clip standardized values to [-6, 6], concatenate the sixteen segments in source order, and compute the Pearson correlation matrix between the 64 regional series. Segment-wise standardization makes the hidden measurement estimate short-timescale cofluctuation rather than global brightness drift. The public calibration movie supplies one independent 16-frame window from each of the same temporal segments, so it is a noisy but relevant measurement of the same session-level quantity. The exact held-out frames remain unavailable. Let R_early[i,j] and R_late[i,j] be the withheld-frame correlations for grid nodes i and j. The hidden change is: Change[i,j] = clip((R_late[i,j] - R_early[i,j]) / 2, -1, 1) Division by two maps the full possible correlation difference from [-2, 2] into [-1, 1]. Each longitudinal pair produces eight challenge rows. Its 64 grid nodes are deterministically shuffled and partitioned into eight disjoint groups of eight nodes. Therefore the eight rows cover disjoint node sets and do not duplicate target edges. Dataset Files The prepared package contains 944 training rows and 240 test rows. These rows come from 148 longitudinal recording pairs across 24 animals: 118 pairs from 18 train-only animals and 30 pairs from 6 test-only animals. train.csv id: string. Unique anonymous 20-character training-row ID. earlier_movie_index: integer. Axis-0 index of the earlier calibration movie in calcium_movies.npy. later_movie_index: integer. Axis-0 index of the later calibration movie in calcium_movies.npy. node_cards: JSON list describing the eight requested grid nodes. transition_card: JSON object describing the known experience-phase interval between the two scans. stimulus_class: string. One of prototype_set, temporal_morph, pitch_shift, or tone_sequence. test.csv test.csv has exactly the same six feature columns and field schemas as train.csv. It contains no answer, target proxy, source subject, source filename, source session identifier, split marker, hidden-frame count, graph statistic, or audit field. train_targets.csv id: string. Training-row ID. coactivity_change: string containing a JSON list of exactly 28 target values. calcium_movies.npy Data type: uint8. Shape: 251 x 2 x 256 x 112 x 112. Use memory mapping to avoid loading the full bank at once. import numpy as np movies = np.load("calcium_movies.npy", mmap_mode="r") early = movies[17] sample_submission.csv id: every test ID exactly once. coactivity_change: a JSON list of 28 zeros. The zero vector is the scientifically natural no-change anchor. It is structurally valid and scores exactly 0. JSON Field Schemas node_cards node_cards is a JSON list of exactly eight objects. Each object has: node: string. A row-local alias from N01 through N08. grid_row: integer from 0 through 7. grid_column: integer from 0 through 7. Aliases are reassigned for every row. A fixed meaning for N01 does not exist. Example: [ {"node":"N01","grid_row":5,"grid_column":2}, {"node":"N02","grid_row":0,"grid_column":7}, {"node":"N03","grid_row":4,"grid_column":4} ] The example is abbreviated; real rows contain all eight cards. transition_card transition_card is a JSON object with: earlier_phase: string. Earlier experimental phase. later_phase: string. Later experimental phase. transition_kind: string. Coarse scientific interval such as retrieval_onset, one_day_consolidation, long_term_followup, pre_retrieval_exposure, or repeat_session. The card states when the scans were collected. It does not contain the measured graph change. Output Grammar and Edge Order coactivity_change must be a JSON list of exactly 28 finite numbers. Every number must lie in [-1, 1]. The vector follows lexicographic unordered-pair order over aliases N01 through N08: N01-N02, N01-N03, N01-N04, N01-N05, N01-N06, N01-N07, N01-N08, N02-N03, N02-N04, N02-N05, N02-N06, N02-N07, N02-N08, N03-N04, N03-N05, N03-N06, N03-N07, N03-N08, N04-N05, N04-N06, N04-N07, N04-N08, N05-N06, N05-N07, N05-N08, N06-N07, N06-N08, N07-N08 A valid prediction is: [0.12,-0.08,0.03,0.21,-0.14,0.05,0.01,-0.04,0.09,0.16,-0.11,0.02,0.07,-0.03,0.10,0.08,-0.05,0.04,0.06,-0.02,0.13,-0.08,0.05,-0.09,0.07,0.01,-0.04,0.02] Invalid row-level predictions include malformed JSON, a non-list value, any length other than 28, booleans, strings, NaN, infinity, or a number outside [-1, 1]. An invalid prediction receives 0 for that row and does not crash the grader. Evaluation The metric rewards improvement over the no-change prediction and gives no free credit for merely formatting a vector. For one row, let T be the 28-value target and P the prediction. MagnitudeGain AnchorError = mean(abs(T)) PredictionError = mean(abs(P - T)) if AnchorError > 0: MagnitudeGain = clip((AnchorError - PredictionError) / AnchorError, 0, 1) else: MagnitudeGain = 1 if PredictionError = 0 else 0 Thus the all-zero no-change vector has MagnitudeGain = 0, and the exact target has MagnitudeGain = 1. The normalization is row-specific and contains no fitted or hidden constant. SignScore Select the 14 target edges with largest abs(T); ties are resolved by the published edge order. SignScore is the fraction of these 14 edges for which P is nonzero and has the same sign as T. If a selected target is exactly zero, it is correct only when the prediction is also exactly zero. SignScore = correctly_signed_selected_edges / 14 Zero predictions receive no sign credit. CorrelationScore Center both vectors by subtracting their means and compute Pearson correlation. If either centered vector has zero norm, CorrelationScore = 1 only when the two complete vectors are exactly equal; otherwise it is 0. CorrelationScore = clip(PearsonCorrelation(P, T), 0, 1) TopChangeSkill Select the seven largest-magnitude edges in P and in T, with ties resolved by edge order. Seven is exactly one quarter of the 28 edges. The expected overlap fraction for two unrelated size-seven subsets is therefore 7 / 28 = 0.25. OverlapFraction = shared_top_edges / 7 TopChangeSkill = clip((OverlapFraction - 0.25) / 0.75, 0, 1) Row Score UngatedScore = 0.55 * MagnitudeGain 0.20 * SignScore 0.15 * CorrelationScore 0.10 * TopChangeSkill row_score = sqrt(MagnitudeGain) * UngatedScore The multiplicative gate prevents sign or ranking guesses from earning substantial credit without improving numerical graph estimation. Final Score overall_mean = mean(row_score over all evaluated rows) bottom_quartile_mean = mean(row_score over the lowest-scoring 25% of evaluated rows) RobustRowScore = 0.78 * overall_mean 0.22 * bottom_quartile_mean The grader also concatenates the prediction vectors for all evaluated rows in answer-file order and does the same for the targets. PopulationCorrelation is the Pearson correlation between those two concatenated vectors, clipped to [0, 1]. If either centered concatenated vector has zero norm, this component is 1 only when both complete concatenated vectors are exactly equal; otherwise it is 0. Invalid row predictions are inserted as 28 zeros and receive no row credit. The correlation is multiplied by the fraction of rows having valid predictions, so malformed rows cannot be used as abstentions. ValidFraction = valid_prediction_rows / evaluated_rows PopulationCorrelation = clip(PearsonCorrelation(concatenate(P), concatenate(T)), 0, 1) ValidFraction final_score = 0.72 * RobustRowScore 0.28 * PopulationCorrelation The row component measures whether individual graph fragments are numerically useful, correctly signed, and correctly ranked. The population component measures whether a model recovers calibrated edge-change variation across animals, transitions, and locations instead of collapsing every case toward one vector. The score is deterministic, finite, and clipped to [0, 1]. The sample submission scores exactly 0. A known-answer submission scores exactly 1. The same formulas apply independently when the platform evaluates any public or private answer partition. Submission Format Submit one CSV file with exactly two columns in this order: id: string copied from test.csv. coactivity_change: JSON list of exactly 28 finite numbers in [-1, 1]. Example: id,coactivity_change 0a12bc34de56f789abcd,"[0.12,-0.08,0.03,0.21,-0.14,0.05,0.01,-0.04,0.09,0.16,-0.11,0.02,0.07,-0.03,0.10,0.08,-0.05,0.04,0.06,-0.02,0.13,-0.08,0.05,-0.09,0.07,0.01,-0.04,0.02]" Structural submission errors are rejected with a clear error. These include wrong columns or column order, missing rows, extra rows, duplicate IDs, unknown IDs, or missing IDs. Rows are aligned by id, never by CSV order. Split, Independence, and Leakage Control The true leakage unit is the animal. All source recordings, stages, stimulus conditions, calibration frames, and graph targets from one animal stay entirely in train or entirely in test. The 24 eligible animals are assigned by a deterministic subject-level procedure before row construction. Preparation enumerates every six-animal subset that would contribute 26 through 38 pairs. It minimizes an objective equal to twice the absolute distance from 30 test pairs, plus 10 times the summed absolute deviation from overall stimulus-family proportions, plus 2 times the summed absolute deviation from overall transition proportions, plus 4 for each transition having at least six total pairs but none in the candidate test subset. SHA-256 order breaks an exact objective tie. The selected six animals produce 30 test pairs; the other 18 animals produce 118 training pairs. The prepared row split is therefore 944 train rows and 240 test rows. No animal, source asset, or longitudinal pair crosses that boundary. Exact source assets are deduplicated by immutable source asset ID and verified file hash. Longitudinal pairs are unique by animal, imaging round, stimulus signature, and ordered experience phases. Near-duplicate rows from one pair are prevented by partitioning the 64 spatial nodes: its eight rows use disjoint node sets and therefore disjoint target edges. Public test visibility is fixed per source recording. If one calibration movie is referenced by more than one row, every reference points to the same 256 frames. No alternate test row reveals a withheld frame, neighboring excluded frame, hidden graph value, or alternate crop from that recording. Movie indices are assigned by an independent SHA-256 ordering. Row IDs hash the complete private pair and node specification under a namespace. Public rows omit subjects, dates, filenames, session IDs, source paths, asset IDs, graph statistics, and hidden-frame counts. Candidate alias order is row-local. Row order is sorted by anonymous ID. Neither IDs, index size, row order, metadata, repeated aliases, nor transition frequency determines the target. What Not to Use Do not attempt to identify public source files, animals, filenames, recording dates, or repository asset IDs. Do not assume that an experience transition implies a fixed graph update. Changes are measured separately from each recording pair. Do not treat N01 through N08 as fixed spatial regions; their coordinates are row-local. Do not load the full movie bank into accelerator memory. Use memory mapping and minibatches. Do not submit source graph files, model weights, Python code, natural-language explanations, or extra columns. Do not exploit CSV row order or movie-index magnitude. Both are independently anonymized. Resource Limit and Practical Workload Solutions have one NVIDIA A10G GPU and a maximum runtime of 60 minutes. The public movie bank is approximately 1.61 GB before filesystem compression. A shared 2D frame encoder with temporal pooling and frame subsampling is expected to train comfortably in 20 to 35 minutes with mixed precision. A compact factorized 3D convolutional or video-transformer model with cached movie embeddings is expected to fit in roughly 35 to 55 minutes. Full-resolution source movies are not part of the prepared package and are neither required nor appropriate for the runtime. Benchmark Boundary Ordinary calcium-imaging benchmarks commonly segment cells, denoise movies, infer spikes, classify stimuli, or estimate connectivity from a complete recording. Longitudinal plasticity studies usually compare population summaries after extensive offline processing. This challenge asks for a different object: a row-local fragment of the change in a static coactivity graph, estimated from two budget-limited calibration movies, with the reference graph computed only from withheld frames and evaluation performed on entirely new animals. Solving it requires jointly modeling cortical space, calcium dynamics, longitudinal change, and node-conditioned graph readout. It is not cell segmentation, image classification, video generation, time-series forecasting, or generic scalar regression.
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## EchoKey: Noisy Cross-View Permutation Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77bwh3gtcasr30krab3j606x8e3k2p
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat dianpham's score of 0.471!

Full challenge description from page:

> EchoKey: Noisy Cross-View Permutation Recovery Overview EchoKey asks a model to recover one hidden four-way correspondence shared across a complete episode bundle. Each scored row contains 14 panels. A panel has four privacy-transformed acoustic items and four anonymous symbolic views of those same events. Their order is independently obscured, but one permutation key is reused across all panels in the row. The task is not transcription and it is not four independent retrieval decisions. A system must infer cross-view compatibility, combine repeated but noisy evidence, and return the single bijection that best explains the complete bundle. Research Positioning Standard audio-text retrieval ranks candidates independently and can assign several acoustic items to the same text. Speech recognition predicts literal words and assumes a published vocabulary. Conventional permutation prediction often scores only exact recovery and discards useful partial structure. EchoKey uses privacy-normalized acoustic sketches, a benchmark-specific opaque token alphabet, a shared episode key, deliberately unreliable cross-view cadence evidence, and a chance-corrected partial-permutation metric. The output remains one scalar class, but evaluation measures how many of the four links are recovered rather than treating every non-exact permutation as equally wrong. Objective For every row of test.csv, predict which of the 24 permutations maps acoustic slots to symbolic slots in all 14 panels. If the predicted permutation is p, acoustic slot a maps to symbolic slot p[a]. Class indices use lexicographic order: import itertools PERMUTATIONS = list(itertools.permutations(range(4))) Class 0 is (0, 1, 2, 3), while class 23 is (3, 2, 1, 0). Episode-Bundle Construction Each panel contains four non-overlapping source events from one independent recording session. The acoustic and symbolic objects are two transformed views of the same four events. Symbolic candidates are reordered so that every panel in an episode follows one common target permutation. Fourteen panels are bundled into one scored row. Train/test assignment occurs at the complete-session level before panel construction. No source event is reused in another released panel, exact normalized symbolic duplicates are removed before splitting, and IDs, array indices, and row order are generated independently of the target. Cross-View Cadence Channel Every symbolic sequence contains one anonymous cadence tag. It is a noisy observation of a coarse local-direction state present in its paired acoustic sketch. Approximately 38% of these tags are deliberately flipped. A tag is therefore useful across a bundle but unreliable in isolation; blindly trusting one panel is not a competitive strategy. The acoustic state is recoverable from local eight-frame block direction, while the identities of the two anonymous tag tokens must be inferred from training data. The remaining opaque sequence preserves additional event content, allowing learned acoustic-symbolic models to improve on the cadence-only rule. Privacy Transformation The acoustic objects are non-playable sketches rather than raw audio or conventional spectrograms. Energy and temporal-change measurements are projected into 32 anonymous bands, normalized within each item, transformed by a fixed private block coordinate system, and rank-quantized to eight bits. Absolute level, the original frequency basis, and literal source timing are not released. The symbolic view uses stable opaque tokens with no published reverse dictionary. Literal text, original recording identifiers, paths, and source metadata are absent from all participant files. A creator-side source-retrieval control compares every released acoustic item with 56 candidate source items from the same episode. Top-1 retrieval is 0.0159, below random chance 0.0179; mean reciprocal rank is 0.0799. This tested deterministic lookup route does not survive the released transformation. Why the Task Is Difficult There are 24 legal global keys but only two noisy cadence states. Many panels contain collisions in which several slots share the same state, and more than one permutation can explain the local tag pattern. The model must aggregate evidence across 14 panels while respecting a one-to-one assignment. Training is exactly balanced over the 24 classes, and the complete test set contains four or five episodes per class. Duration, constant-label prediction, array order, and isolated nearest-neighbor matching are weak baselines. The intended source-free cadence rule scores 0.3894 on the complete evaluation set; random and constant submissions remain near zero after chance correction. Neural content modeling has room to separate solutions beyond the rule baseline. Data Files The participant package contains: train.csv: 408 labeled episode rows; test.csv: 101 unlabeled episode rows; audio.npy: one shared uint8 tensor with shape [509, 14, 4, 32, 128]; train_texts.json: anonymous symbolic panels for training IDs; test_texts.json: anonymous symbolic panels for test IDs; and sample_submission.csv: the exact submission schema. No network access is required for training or inference. CSV Schema train.csv has id, array_index, and target. test.csv has id and array_index. id is an opaque unique episode identifier. array_index selects the first axis of audio.npy. target is an integer permutation class from 0 through 23. One CSV row is one complete independent session bundle. Validation splits must keep rows intact; there are no panel rows to regroup. Acoustic Array Layout For an episode, audio[k, a] is acoustic slot a in panel k and has shape [32, 128]. The final axis contains sixteen local blocks of eight values. Values range from 0 through 255 and are neither decibels nor waveform amplitudes. The anonymous band axis is not a Mel-frequency axis. Models may normalize the values, process blocks or panels as sets, learn local directional filters, and pool evidence across panels before applying a bijective assignment layer. Symbolic Payload Each JSON value is a list of 14 panels. Every panel is a list of four space-separated opaque-token sequences. Panel index k corresponds to audio[k], and list position is the symbolic slot. Token identities are stable across train and test. Exactly one of two anonymous cadence-tag tokens appears in every sequence, mixed into the ordinary token stream. Solvers must learn their interpretation from labeled training bundles; literal-language decoding is neither supplied nor required. Evaluation The evaluator decodes the predicted and true classes into four-element permutations. It first measures the fraction of individual acoustic-to-symbolic links that agree, then removes the 0.25 agreement expected from a random permutation: slot_accuracy = matching permutation positions / (4 x scored episodes) score = clip((slot_accuracy - 0.25) / 0.75, 0, 1) The score ranges from 0 to 1 and higher is better. A perfect submission scores 1.0. A uniform-random permutation has expected score 0.0. Because partial permutation structure is scored, one wrong link does not erase the three links a solver recovered correctly. Submission Format Submit exactly two columns in this order: id,prediction E0123456789abcdef,7 Eabcdef0123456789,19 prediction must be an integer from 0 through 23. Rows may be reordered because the evaluator aligns by id. Missing rows, duplicate IDs, extra or reordered columns, Boolean or fractional predictions, non-finite values, and out-of-range classes raise descriptive validation errors. Compute and Training Requirement EchoKey is a From Scratch challenge intended for one NVIDIA A10G. Trainable parameters must be randomly initialized and fitted only on the released training package. The 408 labeled episodes contain 5,712 panels, 22,848 acoustic objects, 22,848 symbolic sequences, and 91,392 possible within-panel cross-view links per full pass. A source-free feature rule can establish a meaningful baseline without a GPU. GPU training is useful for models that learn residual sequence content, block-level acoustic features, panel interaction, differentiable assignment, and multi-seed validation beyond that baseline. What Not to Use Do not use pretrained speech, transcription, language, translation, multimodal, or embedding models. Do not use external lookup, search, retrieval, pronunciation, or transcription services. Do not identify or link released items to recordings, transcripts, publications, people, or source archives. Do not reconstruct audio, recover a literal token dictionary, manually label test items, or probe labels through repeated submissions. Classical signal processing and text statistics are allowed when fitted or calibrated only with the released training data. Limitations The benchmark covers one controlled speech domain, one anonymous token system, privacy-transformed acoustics, a fixed four-way assignment size, and a deliberately noisy cadence channel. It measures cross-view set matching under this contract. It does not establish general transcription quality, open-domain semantic understanding, speaker robustness, formal privacy, or suitability for production speech systems. &nbsp;
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Interrupted Codon Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7648kkpgys7r92sjfyefexyx8e7ydh
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat dominico's score of 0.681!

Full challenge description from page:

> Overview Recover codons interrupted by introns from noisy nucleotide signals. Given a locus oriented along its transcribed strand and a known coding anchor, predict each interrupted codon's three genomic positions and translated amino-acid residue under the standard genetic code. The anchor identifies the target gene. Context can include neighboring sequence; only the gene containing the anchor is evaluated. Targets are derived from coding annotations checked against the corresponding protein translation. Signals are simulated nucleotide evidence rather than measured sequencing traces. Public files train.csv: 6,000 training loci. test.csv: 1,000 evaluation loci. signals/: one compressed NumPy signal array per locus. train_answers.csv: columns locus_id,split_codons, containing training targets. train_phase.csv: columns locus_id,phase_path, linking to training supervision in training_phase/. train_groups.csv: columns locus_id,group_id, with opaque contig groups for validation. sample_submission.csv: all test IDs with a syntactically valid example prediction. Example predictions are placeholders, not labels. Input table schema locus_id: opaque unique string. n_bases: valid locus length, no more than 8,192. anchor_base: zero-based position of a known coding base in the target gene. signal_path: relative path to the signal NPZ file. base_calls: exactly n_bases letters from A, C, G, T, obtained by taking the largest signal channel. Arrays Signal NPZ files contain key signal, a float16 array of shape (4,8192). Channel order is A,C,G,T. Valid positions contain values in [0,1], with gain variation, mild sinusoidal interference, localized channel perturbations and Gaussian noise. Positions from n_bases onward are zero padding. Training phase NPZ files contain key phase, a uint8 array of shape (8192,). Zero means outside the target coding sequence or padding. Values 1,2,3 mark the first, second and third bases of successive translated codons. The phase continues in spliced order across introns. Phase arrays are provided only for training loci. Splits and validation Complete contigs are assigned to one split using a fixed hash, so overlapping loci cannot cross the training/test boundary. Exact duplicate coding sequences are removed. Held-out proteins with eight-amino-acid k-mer containment of at least 0.30 against any training-pool protein are excluded. This reduces sequence memorization but does not establish independence of all gene families. Keep each contig group together in internal validation. Loci with ambiguous anchors, inconsistent coding phases, incomplete coding sequences or protein-translation mismatches are excluded. Prediction grammar base0.base1.base2:residue|base0.base1.base2:residue|... Each entry contains three increasing, zero-based integer positions, followed by one uppercase residue. At least one genomic position must be skipped: base2-base0 > 2. Fully contiguous codons are invalid. Allowed residues are ACDEFGHIKLMNPQRSTVWY*, where * denotes stop. Entries must be sorted numerically and lexicographically by their coordinate triples. No base may occur in two predicted codons. The parser accepts positions 0–8191. Restrict useful predictions to positions below n_bases; padding cannot match reference coding bases. At most 32 codons and 4,096 characters are permitted per row. No spaces or additional delimiters are allowed. An empty string is a valid empty prediction. For example, if positions 10,11,90 form an interrupted AAA codon, the token is 10.11.90:K. Evaluation A predicted codon and a reference codon receive pair weight zero when their residues differ. When residues match, the weight is their number of shared base coordinates divided by three. Thus one, two or three matching positions earn 1/3, 2/3 or 1. For each locus, choose the one-to-one assignment of predicted and reference codons with the largest total weight. Divide that weight by the larger of the predicted and reference codon counts. Every reference contains at least one interrupted codon; an empty prediction scores zero. The final score is the unweighted mean over test loci, ranges from 0 to 1, and is maximized. pair_weight = shared_positions / 3 if residues_match else 0 row_score = maximum_assignment_weight / max(predicted_count, reference_count) final_score = mean(row_score over all test loci) Submission Submit a UTF-8 CSV with exactly two columns in this order: locus_id,split_codons. Include every test ID exactly once. Do not include input metadata such as n_bases. locus_id,split_codons example_a,10.11.90:K|145.280.281:L example_b, These IDs are illustrative; use the IDs in the supplied sample. Missing, duplicate or unknown IDs, incorrect columns, invalid CSV or files exceeding 64 MiB score zero globally. A malformed codon payload scores zero for that row. Submission row order does not affect the score. Execution constraints Use one NVIDIA A10G within a 90-minute offline session. Train all learned parameters from random initialization on the supplied training data. Neural training and inference must use GPU computation; CPU preprocessing, loading and serialization are permitted. No pretrained models or embeddings, external genomic sequences or annotation tools, homology database lookups, hosted APIs, internet access, manual test labeling, hard-coded test predictions or test-driven tuning are allowed.
> 3 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Copied-to-Free Handwriting Transfer

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx729402j0gt2q3s9e79h0a5ps8e3r1y
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat jesuisnadi's score of 0.616!

Full challenge description from page:

> Overview Transcribe real Kurdish free-writing lines after learning from copied-passage handwriting. Recover complete words accurately enough for text search and downstream language processing, not merely a visually similar character sequence. Dataset There are 1,200 training images from 519 writers and 295 test images from 156 different writers. Training uses copied passages; testing uses free writing. No writer crosses the split, fixed shared-prompt pages are excluded, and exact transcriptions shared with testing are excluded from training. Similar vocabulary and handwriting patterns can still recur. A fixed hash ordering selects up to 1,200 training and 300 test images within those existing writer partitions. All 295 eligible test images are retained; no rows are duplicated to reach 300. Images are converted to grayscale and resized to at most 128 pixels high, preserving aspect ratio, without cropping or upscaling; JPEG quality is 90. Transcriptions remain unchanged, and no extra lines are created by augmentation. Pairs with exact repeated native annotation-file or image bytes are excluded. References are native human transcriptions, normalized to Unicode NFC and whitespace-separated tokens. They contain 8–320 characters. Lines with numerical/contact-like text and selected annotation markers were excluded. Word boundaries and character variants are significant. Some native ambiguity remains, and one reference cannot represent every defensible reading. Submission Submit UTF-8 CSV with exactly task_id,transcription, in that order. Include every test ID exactly once. transcription is a string of at most 2,000 Unicode characters; empty strings are allowed. Quote values containing commas, quotation marks or line breaks. task_id,transcription example,زمانی کوردی Evaluation The score is clipped corpus word accuracy, derived from standard word error rate (WER). Normalize both strings to NFC, split on whitespace, and compute minimum word-level Levenshtein distance. Each word insertion, deletion or substitution costs one. WER = sum(word_edit_distance) / sum(reference_word_count) score = max(0, 1 − WER) Whole-word scoring reflects whether recognized words are usable; almost-correct spellings do not count as correct words. Words retain case and punctuation. Scores range from 0 to 1, with gold equal to 1. Empty, non-string or overlength predictions receive the cost of deleting the reference for that row. Incorrect headers or ID sets are rejected. Row order has no effect. Expected Approach Train a compact line-image encoder with a character decoder on the supplied copied-writing examples, then apply it to free-writing lines. A small convolutional encoder with CTC is a practical starting point; preserve the target character order and word boundaries. For an efficient implementation: Decode and normalize each image once. Preserve aspect ratio, bucket batches by width and pad only to each batch's longest line. Build a character vocabulary from training transcriptions. Check that the encoder supplies enough time steps for the longest targets before launching training. Start with a few short epochs and greedy decoding. Consider a small beam only if measured inference time permits it. Validate on held-out writers, retaining the checkpoint with the best word accuracy. Do not use test transcriptions to build a lexicon or select decoding settings. What Not To Use GPU training and general-purpose pretrained models are allowed. Do not use external handwriting/transcription datasets, challenge-specific checkpoints, source copies, hard-coded answers, reverse image search, hosted APIs, manual transcription of test images. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The complete solution must finish within 60 minutes end to end, including data loading, preprocessing, feature extraction, training or adaptation, validation, inference, structured decoding and submission writing. This is a total execution limit, not a separate allowance for each stage. The platform may terminate execution at the limit; use elapsed-time checks and retain the best completed model so that a valid submission is written before the deadline. Start with a small end-to-end run and write a valid full-test submission early. Use a wall-clock timer from process start, avoid exhaustive searches and large ensembles, and reserve at least the final 10 minutes for inference and submission checks; increase this reserve if measured throughput requires it. Cache encoder outputs only while the encoder is frozen. &nbsp;
> 3 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Renovation Response Compass

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7d1qyp8fzf218ndqdkah5g618c8tyn
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview This is a From Scratch multimodal spatial-learning challenge. An acoustic renovation can improve an apartment overall while behaving very differently in individual directions because rooms, doorways, and propagation paths redistribute the effect. Dense before/after measurement is expensive. You receive a walkable-floor geometry and sixteen sparse, positioned acoustic probes collected before and after a material change. Your goal is to recover an ordered eight-direction response ledger for the unmeasured receiver cells. Any learned model must be initialized from random weights and trained only on the supplied public training data; pretrained weights and external embeddings are not allowed. Each packet describes one source in one de-identified apartment geometry and an ordered before/after material intervention. The labels are computed from acoustic clarity measurements at receiver locations that are not included among the sixteen public probes. For every valid direction row, predict how that direction's median C50 change differs from the apartment-wide median change: | response_state | Renovation-response residual | |---|---:| | far_lower | less than -3.224625 dB | | lower | -3.224625 dB to less than -0.837500 dB | | similar | -0.837500 dB to less than 0.837500 dB | | higher | 0.837500 dB to less than 3.215000 dB | | far_higher | at least 3.215000 dB | The eight direction indices are 0=east, 1=northeast, 2=north, 3=northwest, 4=west, 5=southwest, 6=south, and 7=southeast. A packet may have fewer than eight scored rows when a sector lacks enough unmeasured receiver cells. What Not To Use Use only the files in the provided public challenge dataset. Do not retrieve, download, fingerprint, or match against the underlying source corpus or any external copy of it. Do not reconstruct or exploit upstream geometry names, material indices, source identifiers, receiver identifiers, filenames, hashes, row ordering, private answer files, or hidden preparation artifacts. Hard-coded source lookup, geometric fingerprint tables, and external nearest-record retrieval are prohibited. Models and ordinary scientific libraries are allowed when they operate only on the provided public files. These restrictions are enforceable challenge rules. Submissions and solution code may be audited for external data access, forbidden lookup, identifier reversal, or hard-coded hidden answers; violations may be rejected regardless of numeric score. Evaluation Submissions are scored by unweighted macro-F1 across the five response_state classes. Each class contributes equally, including the two rarer extreme states. Higher is better. Scores range from 0 to 1, and a perfect submission scores exactly 1.0. The submission must contain exactly the columns row_id,response_state in that order and exactly one row for every test row_id. Missing, extra, duplicate, or blank ids are structural failures. An unknown, blank, non-string, or overlong state is scored as wrong for that row without invalidating other valid rows. Submission row order does not matter because rows are aligned by row_id. Dataset | File | Contents | |---|---| | train.csv | 49,751 labeled direction rows | | test.csv | 12,219 unlabeled direction rows | | train_packets.jsonl | 8,820 packet records with source coordinates and sixteen before/after probes | | test_packets.jsonl | 2,220 test packet records in the same schema | | geometries/.npy | 64×64 uint8 walkable-cell map; load with numpy.load(..., allow_pickle=False) | | feature_schema.json | Probe columns, directions, response labels, coordinate frame, and thresholds | | sample_submission.csv | Valid deterministic weak submission with all required test ids | | DATA_README.md | Compact join and file-format guide | Join each CSV row to its packet through packet_id and to its geometry through geometry_id. Packet source_xy and probe x,y coordinates are isotropically normalized and aligned to the geometry map. Every probe is [x, y, before_c50_db, after_c50_db, before_t30_s, after_t30_s]. The split is made at the complete geometry-family level before any packet or direction rows are generated. All five material variants, every source/receiver record, every intervention ordering, and the derived geometry asset for one family are assigned wholly to either public training or private evaluation—never both. Public training contains 50 families and private evaluation contains 10 different families, and preparation rejects any duplicate geometry hash that crosses the boundary. Consequently, memorizing a geometry, material-pair response, packet, or receiver layout from training cannot directly answer an evaluation row: the score measures transfer to entirely unseen apartment geometry families rather than interpolation among records or material variants from a seen family. Public identifiers are salted split-disjoint opaque tokens and do not expose upstream names or indices. Execution contract Agent runs and solution grading use the A10G compute tier with a 1.5-hour full-solve budget. This is a From Scratch task: train all learned parameters from random initialization using only the supplied public training split. General-purpose or task-specific pretrained weights, external embeddings, prior checkpoints, and cached learned artifacts are prohibited. CPU-compatible feature engineering and lightweight models are viable; GPU acceleration is available for compact spatial encoders or multimodal fusion trained within the run. Use only files shipped with the challenge and packages available in the execution environment. Network retrieval and external datasets are prohibited. Submission | Column | Type | Required value | |---|---|---| | row_id | string | An unchanged test id from test.csv | | response_state | string | One of far_lower, lower, similar, higher, far_higher | Example: row_id,response_state r_001122aabbccddeeff001122,similar r_0014f7a36e3057709430c516,higher
> 0 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## WildContext: Retrieval-Augmented Behavior Decoding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx769mrp8vbf5535dt06gm1w5d8e8ypk
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat aerofrazer's score of 0.616!

Full challenge description from page:

> WildContext: Retrieval-Augmented Behavior Decoding Overview The same visible behavior can look very different across acquisition sessions, while different behaviors can share similar backgrounds and motion. Conventional row-wise classification handles part of that variation by learning one global label vocabulary. WildContext removes that convenience and replaces it with case-local evidence: every query arrives with twelve anonymous evidence records drawn from the same held-out observation domain. Your model must determine which evidence records are behaviorally compatible with the query and return their attached response token. The six response tokens are remapped independently for every query, so token 2 in one case has no semantic relationship to token 2 in another. Evaluation acquisition groups never occur in training, so memorizing camera or session signatures is insufficient. The closest standard task families are behavior classification and cross-modal retrieval. Behavior classification normally predicts a fixed class, while ordinary retrieval usually compares items in one compatible representation space. Set-conditioned few-shot tasks consume demonstrations, but often sample synthetic functions or fixed semantic classes. WildContext combines real field observations, protected acquisition-group holdout, incompatible query/evidence views, query-local token permutations, hard alternatives, and scalar accuracy evaluation. The scored object is therefore a complete local evidence-decoding episode rather than an independent feature row. Objective Train a model from scratch using only the released challenge files. For every row in test.csv, predict one integer response token from 0 through 5. Each case contains one query vector and twelve evidence vectors. Every token occurs exactly twice in the case. The correct response is the token attached to the two evidence records that express the same latent behavior as the query. Evidence order is independently shuffled and has no temporal, quality, or ranking meaning. From-Scratch Formulation This is a from-scratch set-conditioned retrieval challenge. External media, labels, behavior models, pretrained weights, hosted embeddings, and outside retrieval systems are not required or permitted. The anonymous numeric vectors supplied with the challenge are the complete model input. A practical system first assembles the twelve evidence records for each query, learns separate query and evidence encoders, and scores the two records associated with every candidate token. A bilinear metric, pairwise ranker, dual-view neural network, or permutation-invariant set encoder can learn the cross-view relationship. Aggregate both records for each token before returning the highest-scoring candidate. The challenge uses the A10G compute tier. CPU linear and tree methods provide meaningful baselines, while the GPU supports multi-seed neural set encoders and hyperparameter exploration within the agent budget. When evidence rows are expanded into training pairs, split by complete query ID so all twelve records from one episode stay together. Case Construction Every case uses all six latent behavior classes, but a fresh behavior-to-token permutation is generated for that case. Query behavior and target token are jointly balanced, making global token frequency uninformative. Query and evidence vectors occupy separate 96-dimensional views whose coordinates are intentionally incompatible. Every released occurrence is unique; exact-vector joins cannot connect training and evaluation cases or assemble repeated-event components. Case IDs and document IDs are opaque keyed hashes and do not encode behavior, answer token, source group, row position, or partition. Evidence contains difficult alternatives selected from the same anonymous observation pools. Direct same-coordinate cosine is intentionally only a sanity baseline. Solving the task requires learning a cross-view comparison from labelled training episodes and applying it to the local evidence set of each unseen query. Dataset Split The protected acquisition session is assigned before cases are constructed. Complete sessions are held out for evaluation, and the public and private evaluation groups are also disjoint. The prepared release contains 3,600 training queries and 792 evaluation queries. It contains 52,704 evidence rows: 43,200 associated with training cases and 9,504 associated with evaluation cases. The test-to-train ratio is 22%. No source event, track, protected acquisition group, query occurrence, evidence occurrence, or exact feature fingerprint crosses the train/evaluation boundary. No protected group crosses public/private visibility. Target tokens are exactly balanced in train, public, and private partitions. Files The release contains: train.csv - 3,600 labelled query episodes with id, 96 query features, and integer target. test.csv - 792 evaluation queries with the same query features and no target. evidence.csv - all query-local evidence records with id, opaque doc_id, integer token, and 96 evidence features. sample_submission.csv - the exact required id,prediction schema with a varied, label-free example. data_manifest.json - dimensions, token vocabulary, row counts, evidence counts, and format metadata. Join queries to evidence using id. Each ID has exactly twelve evidence rows and exactly two rows for each token from 0 through 5. Feature Layout Query columns are named q_0 through q_95. Evidence columns are named e_0 through e_95. All feature values are finite floating-point numbers. The query and evidence coordinates are separate learned views. Do not compare q_j directly with e_j as though they measured the same axis. Build training pairs or case-level tensors by joining on id, preserve the integer token, and treat the twelve evidence records as an unordered set. target is a finite integer in 0..5 and appears only in train.csv. doc_id is an opaque record identifier, not a feature. Neither CSV row order nor numeric formatting carries target information. Expected Output For every test ID, return exactly one finite integer prediction from 0 through 5. The value must be the query-local response token, not a global behavior label, evidence row number, rank, probability vector, or document ID. Submission row order does not affect scoring because the grader aligns by ID. Every required test ID must occur exactly once. Evaluation The metric is ordinary six-way accuracy: score = correctly predicted evaluation queries / evaluated queries Scores are bounded in [0, 1] and higher is better. A perfect submission scores 1.0. Because every response token is exactly balanced, every constant token scores exactly 1/6 on full, public, and private answers. Measured release diagnostics establish the intended difficulty. The varied template scores 0.1465; raw coordinate cosine scores 0.1629; query-only ridge scores 0.1843; and evidence-only ridge scores 0.1616. Three independent blind trained approaches score 0.3144, 0.3826, and 0.5000, with the same ordering on public and private slices. The exact answer scores 1.0. Thirty equal-quality private perturbations have score range 0, and progressive degradation is strictly ordered from 1.0 to 0.0. Validation Contract File-level structural faults raise a validation error with a specific reason. These faults include wrong, extra, or reordered columns; missing required rows; duplicate IDs; non-numeric or non-finite predictions; non-integer predictions; and labels outside 0..5. The grader is deterministic and aligns predictions from the answer IDs, so reordering otherwise valid submission rows cannot change the score. It supports the platform evaluating public and private answer subsets against one complete submission. Organizer-side visibility metadata is validated and ignored for scoring. Submission Format Submit a CSV with exactly these two columns in this order: id,prediction 0123456789abcdefabcd,3 abcdef0123456789abcd,0 Every id from test.csv must appear exactly once. Predictions must be ordinary finite integer values in 0..5. What Not To Use Do not use external video, behavior labels, datasets, APIs, web retrieval, or a second copy of the parent observations. Do not use pretrained model weights, pretrained behavior representations, hosted embeddings, or challenge-specific checkpoints. Do not attempt to identify the original recordings or recover hidden source, video, track, event, or partition identifiers. Do not infer targets from row order, hashes, document IDs, CSV byte layout, numeric formatting, token frequency, or repeated-submission probing. Do not fit, calibrate, reweight, pseudo-label, or adapt a model using the full test distribution or leaderboard feedback. Do not manually label evaluation rows or hardcode predictions. The final submission must be generated automatically from the supplied training and evidence data. &nbsp;
> Closes in 4m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Argo Delayed-Mode Ocean Profile QC Decisions

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a0pa69y7e4aa9jytn5jarqs8e4103
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat mrfizhz's score of 0.647!

Full challenge description from page:

> ## Overview Argo Delayed-Mode Ocean Profile QC Decisions This is a From Scratch scientific array-segmentation challenge. Ocean profiling floats report independent depth-indexed pressure, temperature, and salinity arrays. Expert operators later review suspicious profiles and change quality-control decisions over specific depth intervals. Every example in this challenge is known to contain at least one such expert action. Your task is to find the affected temperature or salinity intervals and predict the kind of QC transition the operator recorded. This is conditional action localization, not general screening of arbitrary ocean profiles and not prediction of the QC fields stored in a current NetCDF file. Participant inputs contain only normalized raw pressure, temperature, and salinity measurements plus validity masks. QC flags, adjusted values, calibration records, history records, source names, geographic coordinates, timestamps, and original identifiers are absent. Each example is a vertical spatial profile rather than a chronological forecasting series. All profiles from one physical float stay in one split. Test floats never occur in training, so successful solutions must learn transferable profile-shape and anomaly patterns rather than memorize a platform. What Not To Do Do not use the internet, external source files, source lookup, or hosted inference services. Do not reconstruct original float identifiers or match public arrays to outside Argo records. Do not infer answers from opaque IDs, row order, paths, array sizes, or file metadata. Do not submit a hand-coded threshold or lookup-only pipeline with no trained model. Do not use private files, hidden answers, grader internals, or repeated submissions as an answer-extraction channel. Do not use current QC, adjusted, calibration, or history fields; they are intentionally unavailable. Task For each test profile, load its n_levels by 6 NumPy array and predict non-overlapping inclusive intervals for TEMP and PSAL. Each predicted interval is [start_level, stop_level, class]. Transition classes are: class 1: QC 1 to 3; class 2: QC 1 to 4; class 3: any other recorded old-to-new transition. Levels not covered by a submitted interval mean no expert action for that parameter. Indices are zero-based and inclusive. Intended Approach And Validation A strong solution should train a GPU model such as a dilated 1D CNN, U-Net-style 1D segmenter, compact Transformer encoder, or boosted level predictor with multi-scale profile features. Useful features include local vertical gradients, robust rolling residuals, pressure-aware receptive fields, cross-parameter consistency, missingness masks, and multi-scale context. Predict per-level action classes, then merge adjacent equal nonzero predictions into intervals. Use series_id to create grouped validation folds so one float never appears in both sides of a validation split. Class weighting, focal loss, hard-negative mining, boundary-aware losses, and probability calibration are reasonable. Validate both event localization and transition identity; a model that predicts broad intervals will lose no-change accuracy and precision. The supplied reference uses GPU gradient-boosted level taggers with multi-scale profile features. It selects thresholds on a float-grouped public validation fold, trains from scratch on the released labels, and does not use pretrained weights or external data. Evaluation Scores are maximized. Every structurally valid test row receives: row_score = 0.15 * detection_accuracy 0.55 * event_f1 0.30 * transition_macro_f1 final_score = mean(row_score) detection_accuracy measures event versus no-event correctness across all TEMP and PSAL levels. event_f1 is binary F1 for corrected levels. transition_macro_f1 is macro F1 over transition classes present in the union of true and predicted event levels. This combination rewards precise boundaries and transition identity while penalizing broad or empty predictions. A perfect submission scores exactly 1.0. The theoretical range is 0.0 to 1.0. Wrong or reordered columns, missing/extra/duplicate/foreign IDs, and row-count mismatch raise a generic InvalidSubmissionError. They invalidate safe alignment and are not row-local defects. A missing, NaN, or Inf payload, malformed or oversized JSON, wrong keys, non-integer triples, overlapping intervals, invalid classes, or out-of-range bounds inside one otherwise aligned row gives that row a score of zero; other rows remain scorable. Error messages do not include private labels, answer rows, split details, or hidden values. Dataset All paths are relative to public/. The final prepared counts are inserted after deterministic preparation. | Item | Description | |---|---| | train.csv | Labeled profile index | | test.csv | Unlabeled profile index | | profiles/*.npy | Raw feature sequences | | sample_submission.csv | Valid weak baseline | train.csv contains 1,105 rows from 438 floats. | Column | Type | Description | |---|---|---| | id | string | Opaque profile id | | series_id | string | Opaque float group | | path | path string | Feature array path | | n_levels | integer | Profile row count | | target_json | JSON string | Training intervals | test.csv contains 688 rows from 219 unseen floats. | Column | Type | Description | |---|---|---| | id | string | Opaque profile id | | series_id | string | Opaque float group | | path | path string | Feature array path | | n_levels | integer | Profile row count | Each profiles/*.npy file is a finite float32 array with shape n_levels by 6. | Index | Feature | Description | |---|---|---| | 0 | pressure_scaled | Raw pressure / 7000 | | 1 | temperature_scaled | Scaled raw temperature | | 2 | salinity_scaled | Scaled raw salinity | | 3 | pressure_valid | Pressure mask | | 4 | temperature_valid | Temperature mask | | 5 | salinity_valid | Salinity mask | sample_submission.csv has exactly the required submission columns. | Column | Type | Constraint | |---|---|---| | id | string | Exact test id set | | prediction_json | JSON string | TEMP and PSAL runs | Submission Write exactly ./working/submission.csv with columns id and prediction_json in that order. The ID set must match test.csv exactly and may be in any row order. prediction_json must be a JSON object with exactly TEMP and PSAL. Each value is a sorted list of non-overlapping [start, stop, class] integer triples. Lists may be empty. {"PSAL":[[18,27,2]],"TEMP":[[104,109,1]]} Example with public test IDs: id,prediction_json p_002e2d65c0b20519a792,"{""PSAL"":[[18,27,2]],""TEMP"":[]}" p_0084eafc2b9459603edf,"{""PSAL"":[],""TEMP"":[[104,109,1]]}" ~
> Closes in 1h 35m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Reef Benthic Layout Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73txy4z7y890nr5ga58ae4vd8eb8eh
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat hoang_phuc_6868's score of 0.237!

Full challenge description from page:

> Reef Benthic Layout Recovery Overview A single downward or oblique photograph of a coral reef captures a mosaic of benthic cover — patches of living coral, dead or bleached coral, algae, bare substrate, and open water — distributed across the frame. Reef monitoring turns these images into spatial cover estimates, but a photograph hands over only pixels: the cover composition of any given region is entangled with lighting, turbidity, viewing angle, and the fine visual differences between, say, living and recently-dead coral of the same growth form. In this challenge each input is one reef photograph, and the target is a spatial composition grid: the frame is divided into a fixed grid of cells, and for every cell you must return a calibrated probability distribution over six benthic cover classes describing the mixture of cover within that cell. The output is therefore a structured field of distributions — one distribution per cell — not a single label and not one number. The task rewards recovering where each cover type sits and in what proportion, and it is scored so that the rare, ecologically critical classes (dead or bleached coral) count as much as the abundant ones, and so that a content-free constant prediction — the same grid for every image — earns no credit. This is a from-scratch representation-learning task. Every model must be trained on the provided reef photographs alone, with randomly initialized weights — the underwater texture and colour cues that separate the cover classes have to be learned directly from the training pixels. Pretrained image weights are not permitted: no ImageNet-pretrained backbone, no self-supervised or foundation-model checkpoint, and no external feature extractor may initialize any part of the network. Because underwater scenes differ sharply from the natural-image corpora those weights are built on, and because whole survey sites are held out of training, the benthic-cover representation must be built up from the data rather than transferred in. The task is hard for three reasons. First, the six classes include visually confusable pairs — living versus dead-or-bleached coral, algae-covered substrate versus bare hard substrate — that can only be separated by texture and colour cues learned from scratch under variable underwater illumination. Second, cover is a mixture: most cells contain several classes, so a cell's target is a genuine distribution, and a confident single-class guess is penalized when the cell is mixed. Third, the composition of a region cannot be read off any single pixel; it must be integrated across the cell while respecting the boundaries between cover types. Dataset Each item is one reef photograph paired with its ground-truth composition grid. The photographs are drawn from many distinct reef survey sites, and whole sites are held disjoint across the train and test splits. Public files public/train.csv — one row per training image, with columns id, image, grid. public/test.csv — one row per test image, with columns id, image (the grid target is withheld). public/images/ — the reef photographs referenced by the image column, as anonymized PNG files (e.g. images/img_7f3c9e21.png), each resized so its longer edge is at most 384 pixels (aspect ratio preserved). public/sample_submission.csv — a valid submission in the exact required format. Columns: id, grid. Private file (organizer only) private/answers.csv — the held-out ground-truth composition grids, stored in the same columns as sample_submission.csv (id, grid). Used only for scoring. Split and anti-memorization The split is designed so the challenge cannot be won by memorizing a particular reef: Whole survey sites are held disjoint across splits. The reef sites contributing images to test.csv do not contribute any image to train.csv. A model must generalize benthic-cover reading to reefs it has never seen, not recall a memorized site. No image is shared across splits, and no image is reused within a split — each row is a distinct photograph. Only the cover-class vocabulary is shared between splits. Generalization is over unseen reefs, unseen lighting, and unseen spatial arrangements of cover. Column descriptions Each row describes one reef photograph and its composition grid. id (string) — unique image identifier, an opaque token (e.g. img_a1b2c3d4). Present in every file. image (string) — relative path to the reef photograph under public/images/ (e.g. images/img_7f3c9e21.png). Present in train.csv and test.csv. grid (JSON string) — the composition grid: a JSON array of 32 cells in row-major order over a fixed 4-row by 8-column grid laid over the image (cell 0 = top-left, cell 7 = top-right, cell 31 = bottom-right). Each cell is an array of 6 non-negative floats that sum to 1, giving the cover distribution sand, hard_substrate, algae, coral_alive, coral_dead_bleached, other] for that cell. Present in train.csv and private/answers.csv; withheld from test.csv. In a submission this column holds the predicted grid in the same format. The six cover classes (fixed order within each cell) are: sand — loose sediment / bare sand. hard_substrate — bare hard reef substrate and rubble not covered by living cover. algae — algae-covered substrate and seagrass. coral_alive — living coral of any growth form. coral_dead_bleached — dead or bleached coral. other — non-benthic content: open water, deep shadow, fauna (fish and mobile invertebrates), divers, and survey equipment. Data example A truncated train.csv row (grid shortened; live rows hold all 32 cells): id,image,grid img_a1b2c3d4,images/img_7f3c9e21.png,"[[0.02,0.10,0.15,0.60,0.03,0.10],[0.00,0.05,0.20,0.55,0.05,0.15], ... ,[0.30,0.40,0.10,0.05,0.00,0.15]]" Submission format Hand in a CSV with a header row and exactly the columns: id,grid Rules: One row per test image and no more (matching the row count of public/test.csv), preceded by a header row. grid is a JSON string encoding an array of exactly 32 cells (row-major over the 4×8 grid). Each cell is an array of exactly 6 finite, non-negative floats. Within each cell the six values are treated as a distribution and are normalized to sum to 1 before scoring; a cell of all zeros is treated as a uniform distribution. Identifiers must be unique, complete, and recognized — no duplicate, missing, or unknown ids. Sample submission Every row carries exactly 2 fields: id and grid. The sample uses a fixed dummy grid (the same 32×6 uniform value in every row): id,grid img_a1b2c3d4,"[[0.1667,0.1667,0.1667,0.1667,0.1667,0.1667], ... ,[0.1667,0.1667,0.1667,0.1667,0.1667,0.1667]]" img_9f8e7d6c,"[[0.1667,0.1667,0.1667,0.1667,0.1667,0.1667], ... ,[0.1667,0.1667,0.1667,0.1667,0.1667,0.1667]]" Evaluation Metric: Benthic Layout Skill, a class-macro Brier skill score measured against a blended reference. For every cell of every test image, the submission provides a predicted distribution p over the six classes and the ground truth provides the true distribution g. The reference distribution for cell c of image i is ref[i = BETA * global_mean_gridc] + (1 - BETA) * image_mean[i] where global_mean_grid[c] is the average ground-truth distribution of cell c over all test images (the population's average spatial layout) and image_mean[i] is the mean of image i's 32 ground-truth cells (its own overall composition). Because the reference already contains the average layout, a content-free constant grid scores at chance; credit is earned for recovering this image's own composition and its spatial detail beyond the population average. Squared error is pooled per class across all cells of all images, then compared to this reference: BETA = 0.6 EPS = 1e-9 CLASSES = ["sand", "hard_substrate", "algae", "coral_alive", "coral_dead_bleached", "other"] global_mean_grid[c = mean over all test images of gik] image_mean[i = mean over the 32 cells of image i refik] = BETA * global_mean_grid[c + (1 - BETA) * image_meani for k in range(6): SSE_k = sum((pc - gc)**2 for c in all_cells) REF_k = sum((refc - gc)**2 for c in all_cells) skill_k = 1.0 - SSE_k / max(REF_k, EPS) mean_skill = mean(skill_k for k in range(6)) # macro-average over the 6 classes a negligible monotone term (<= 1e-4) orders sub-reference submissions score = 0.02 + 0.98 * max(0.0, mean_skill) + 1e-4 / (1 + exp(-mean_skill)) score = min(1.0, max(0.02, score)) # in [0.02, 1.0] Range: [0.02, 1.0]; higher is better. Perfect grid: score = 1.0 (zero squared error on every class). Content-free predictors — the same constant grid in every image (including the population's average grid) and the uniform sample submission — score at the 0.02 floor: they carry no image-specific information. Squared error is pooled per class before normalizing (never per cell or per image), and the six classes are macro-averaged, so the rare coral_dead_bleached and sand classes count as much as the abundant coral_alive and other. Being a proper scoring rule, the metric rewards calibrated distributions and penalizes confident errors: a well-calibrated partial reconstruction scores well above an overconfident one. A row whose grid cannot be parsed as 32 cells of 6 finite non-negative values (malformed JSON, wrong length, NaN/inf, negative, or blank) earns zero skill for that row (it is scored as if it predicted the reference grid) while every other row grades normally; whole-file faults (wrong columns, missing/unknown/duplicate/blank id, empty file) are rejected. Squared error is pooled per class before normalizing (never per cell or per image), and the six classes are macro-averaged, so the rare coral_dead_bleached and sand classes count as much as the abundant coral_alive and other — a submission that only fits the common classes cannot score well. All scoring constants (the 4×8 grid, the six-class order, BETA = 0.6, EPS, the 0.02 floor and 0.98 span, and the blended reference) are fixed in eval.py. What Not To Use (Prohibited Methods) To keep the board fair and preserve the meaning of the composition-recovery task, the methods below are off-limits. Any entry shown to use one will be thrown out in post-submission review. General restrictions (apply to every submission) No external answer keys or cover annotations. Do not use any external reef-survey annotation set, dense cover mask, or point-count label file to recover the composition grids. Do not match test images, sites, or frames back to any external source. No id- or filename-based hardcoding. Do not bake in per-id grids or fixed distributions, and do not build a lookup from any memorized external mapping. No train/test leakage. Do not let preprocessing, normalization, or splitting carry test-set information into training, and do not train on the held-out test sites or any near-duplicate of their images. No private-label tuning. Do not tune hyperparameters, thresholds, or model selection against the hidden test grids, whether directly or by repeatedly probing the leaderboard. Challenge-specific restrictions No pretrained image weights — train from scratch. Every model must be trained on the provided training photographs from randomly initialized weights. Do not initialize any part of your network from pretrained weights of any kind: no ImageNet- (or other dataset-) pretrained backbones, no self-supervised or foundation-model checkpoints (e.g. CLIP, DINO, MAE, SAM, or any pretrained ResNet / ViT / ConvNeXt), and no external pretrained feature extractors or embeddings. Only weights learned from scratch on the provided train split may be used to produce the composition grids. No manual cover annotation. Test grids must be produced by your system from the provided photograph, not drawn, point-counted, or estimated by hand. No external mask recovery. Do not reconstruct a test image's cover map from any information outside its own provided pixels (external dense masks, the original survey the frame may come from, or site metadata). No image back-matching. Do not trace test ids, image filenames, or pixel content back to an outside source to recover the composition grids. &nbsp;
> 2 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Hubei Mine Review Clicks

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79f1ezttpwhndjk06dgkwnns8ebxfh
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 0.564!

Full challenge description from page:

> Hubei Mine Review Clicks Overview Train a computer-vision model from scratch to nominate one inspection click, or an abstention, for each satellite-image tile. If a tile contains a sufficiently visible annotated mine footprint, the click should land near a representative interior point of its largest footprint. If it does not, abstain. The output is a spatial action, not an image class, a bounding box, a segmentation map, or a tabular target. An analyst who can inspect only one candidate location per tile needs a location worth opening, not a list of every possible region. The benchmark therefore rewards accurate mine-site placement on occupied tiles while independently rewarding abstention on empty tiles. A system that always clicks or always abstains has no score. The image is the evidence; no source-image identifier, location, mine type, or numeric summary is exposed as a predictive feature. Image and target construction Each public image is a 160-by-160 RGB JPEG crop. All 25 crops from one 800-by-800 annotated source image are non-overlapping and assigned to the same side of the split. A fixed, private preparation key chooses a quarter-turn rotation and optional reflection for the entire original image; its polygon annotations receive exactly the same geometric transform before cropping. This preserves visual evidence and annotation geometry while keeping released tile files separate from the upstream full-image filenames. For each crop, intersect every annotated mine-instance polygon with the crop. A polygon occupying fewer than 20 crop pixels is not an inspection target in that crop. Among the remaining intersections, choose the largest by annotated pixel area. The reference click is the pixel center deepest inside that intersection, found by a Euclidean distance transform that treats the crop border as exterior; ties are resolved by interior depth and then image position. Coordinates are divided by 160 and rounded to six decimals, so (0,0) is the upper-left boundary and (1,1) is the lower-right boundary. If no intersection occupies at least 20 pixels, the reference is an abstention. The point is a deterministic action label derived from the existing reviewed polygon, not a newly invented mine annotation. The 20-pixel eligibility rule prevents tiny edge slivers from becoming ambiguous one-click targets. A solver may predict any valid point; it need not reconstruct the underlying polygon or the deterministic point-selection procedure exactly to receive partial credit. Split and generalization The complete source collection has 1,426 800-by-800 annotated images, numbered consecutively. Preparation assigns original image numbers 1 through 1100 to training, excludes 1101 through 1150 as a 50-image boundary gap, and assigns 1151 through 1426 to evaluation. All 25 tiles from an original stay together, so no original image or annotation is shared across train and test. JPEG bytes are hashed globally; duplicate prepared images would be removed before release. The realized data have 27,500 training tiles and 6,900 test tiles, with 7,140 and 2,303 occupied tiles respectively. The tr_ and te_ case identifiers are assigned only after separate keyed shuffles and encode neither the original image number nor its label. Opaque IDs alone are not a leakage guarantee; the parent-image split, boundary gap, and exact-tile deduplication are the relevant controls. Source-image numbers, rather than acquisition-session identifiers, define the available split groups. The claimed holdout is original-image-disjoint, not a claim that the upstream acquisition has session-disjoint metadata. The 34,400 tiles are non-overlapping crops of 1,376 retained original images, not 34,400 independent satellite scenes. Their combined visible area is large, but performance should be read as transfer to held-out source images in this collection. Files The public directory contains: public/ train.csv train_labels.csv test.csv sample_submission.csv tiles/ .jpg train.csv has 27,500 rows with exactly case_id,image_path. test.csv has 6,900 rows with the same two feature columns, in the same order and types. image_path is relative to public/ and points to the row's 160-by-160 JPEG. train_labels.csv has exactly case_id,inspection_click; it joins one-to-one with train.csv. The test feature file has no click labels. sample_submission.csv has exactly case_id,inspection_click, matching the private answer CSV columns and order. It includes every test identifier once. Its clicks are generated by a train-only logistic occupancy classifier and ridge point locator fitted to 10-by-10 image downsamples; the decision threshold is selected on a held-out part of the training rows. It is a learned starter rather than a fixed center or copied answer. Submission Submit a UTF-8 CSV with exactly these two columns, in this order: case_id,inspection_click te_0123456789abcdef,"{""click"":[0.503125,0.503125]}" The identifier above illustrates the syntax only. Copy actual IDs from test.csv. The inspection_click cell is a JSON object with exactly one key, click. Its value is either null for abstention or a two-number list [x,y] with both finite coordinates in [0,1]. Examples of valid cells are {"click":null} and {"click":[0.48,0.37]}. Booleans, extra keys, strings as coordinates, and cells longer than 96 characters are invalid. An invalid cell earns zero for that row, including when the true tile is empty. Every graded ID must occur once. A missing or duplicate graded ID returns 0. Extra or missing columns, reversed column order, and duplicate normalized column names raise ValueError. On the full test set, extra IDs return 0. For a public/private answer partition, the full test submission may contain other issued test IDs; any fabricated ID still returns 0. Submission row order is ignored. Scoring For a positive reference click t and a submitted point p, define its credit using normalized Euclidean distance: d = sqrt((p_x - t_x)^2 + (p_y - t_y)^2) positive_credit = max(0, 1 - d / 0.60) Abstaining or submitting an invalid cell on a positive tile gives zero. On a negative tile, a valid abstention gives one and any point or invalid cell gives zero. Let P be the mean credit over positive tiles and A the mean over negative tiles. The two facets are fused and adjusted as follows: M = sqrt(P * A) score = clip((M - 0.25) / 0.75, 0, 1) An exact match to every target returns 1.0 directly. If fewer than eight rows are graded, or a non-exact answer subset contains only one class, its score is zero. This keeps tiny or single-class public slices from receiving accidental skill credit. The distance term rewards useful click placement without requiring exact pixel-level reproduction of a derived interior point. Separate positive and negative means prevent the more numerous empty tiles from dominating the evaluation. Their geometric fusion makes either always-click or always-abstain policies score zero. The fixed 0.25 floor removes small accidental gains from guessing on the complete mixed test set, while preserving the exact upper endpoint. The score is deterministic, bounded, and unchanged by row permutation. Method restrictions Use only train.csv, train_labels.csv, and their public tile images to fit predictive parameters. Randomly initialized neural vision models, linear models, and other supervised learners are allowed. Pretrained vision models, external satellite imagery, upstream full images or annotation files, source-record matching, cached target lookup, manually drawn test clicks, and human annotation services are prohibited. A submitted point or abstention must be a model decision learned from the provided examples. Standard image decoding, resize, normalization, batching, optimization, probability calibration on a training split, likelihood decoding, and JSON/CSV serialization are allowed. Handwritten visual mine rules, per-image memorization, filename-derived guesses, and rule-based correction of model outputs are not allowed. &nbsp;
> 1 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Atom Resonance Hierarchies

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7838dydkrx59nbyyrdk0r1n98e69ne
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat digy's score of 0.741!

Full challenge description from page:

> Overview Predict a hierarchy of carbon resonance groups from a molecular graph and an unassigned, noisy list of carbon-13 chemical shifts. Matching observed resonances to graph atoms is ambiguous when nearby chemical environments produce similar shifts. This task evaluates whether a model can recover the nested grouping structure at three resolutions. For each molecule, predict three partitions of its carbon atoms at tolerances of 1.0, 4.0 and 12.0 ppm. True groups are connected components under single linkage: sort the assigned shifts and start a new group whenever the next gap exceeds the tolerance. Groups can merge as tolerance increases but cannot split. Public files train.csv: 4,000 training molecules. test.csv: 1,000 held-out molecules. queries.csv: the combined index with an additional split column. graphs/: 5,000 molecular graph JSON files. train_labels.csv: training IDs and target resonance_groups. train_groups.csv: training IDs and opaque scaffold group_id values for validation. sample_submission.csv: all test IDs with valid example partitions. task_format.json: feature ordering and tolerance metadata. Input tables train.csv and test.csv contain molecule_id (opaque ID with an m_ prefix followed by 20 hexadecimal characters), graph_file (relative JSON path), and atom_count (number of carbons, 8–48). This count is input metadata, not a prediction column. Molecular graph JSON atoms: one list per heavy atom, ordered as atomic number, formal charge, aromatic flag (0/1), hydrogen count, and integer chiral tag. neighbors: adjacency lists of zero-based graph indices. bonds: lists containing source index, target index, floating-point bond order, integer stereo code, and a list of stereo atom indices. carbon_indices: graph indices of carbon atoms, in the order required for predictions. unassigned_resonances_ppm: one observed shift per carbon, randomly shuffled. Observations add independent Gaussian noise with standard deviation 0.25 ppm and a shared molecular offset uniformly sampled from −0.8 to 0.8 ppm. Values are rounded to five decimal places. Graph atom order is randomized. The observed resonance-list order does not identify the carbon associated with a shift. Splits and validation Exact canonical molecular duplicates are removed. Complete Bemis–Murcko scaffolds are assigned to one split using a fixed hash; training and test scaffolds are disjoint. Acyclic structures share one scaffold group. This prevents the same molecular scaffold from appearing in both splits and reduces structural memorization. Related chemistry can still occur across different scaffolds, so the benchmark measures scaffold-held-out generalization rather than complete chemical-family independence. Keep every group from train_groups.csv together in internal validation. Eligible molecules have complete carbon assignments, 8–48 carbons, and three nontrivial nested reference partitions. At each tier there are at least two clusters and fewer clusters than carbons. Symmetry-equivalent atoms must have consistent reference group assignments. Target format For each tolerance, form a vector of N group labels in carbon_indices order. Canonicalize labels by first appearance: the first group is 0, the next previously unseen group is 1, and so on. For example, labels [5,5,9,2] canonicalize to [0,0,1,2]. Concatenate the three N-byte unsigned-integer vectors in increasing tolerance order, then encode the resulting 3N bytes using standard padded Base64. A coarser partition may merge finer clusters but must never split one. Identical adjacent predicted tiers are allowed. Illustrative four-carbon encoding example (real inputs have 8–48 carbons) Tier 1: [0,0,1,2] Tier 2: [0,0,1,1] Tier 3: [0,0,0,0] Packed bytes: [0,0,1,2,0,0,1,1,0,0,0,0] Base64: AAABAgAAAQEAAAAA Evaluation Compute the Adjusted Rand Index (ARI) between predicted and reference partitions at each tier, clipping each ARI to [0,1]. A molecule scores the minimum of its three clipped tier scores. The final score is the unweighted mean across all test molecules; higher is better and the range is [0,1]. choose2(x) = x * (x - 1) / 2 T = choose2(N) A = sum(choose2(size) for each reference cluster) B = sum(choose2(size) for each predicted cluster) J = sum(choose2(size) for each reference/predicted intersection) ARI = 2 * (T * J - A * B) / (T * (A + B) - 2 * A * B) If the denominator is zero, ARI is 1 when A = B = J and 0 otherwise. Clip negative values to zero. All-singleton and all-one-cluster baselines score zero against these nontrivial reference tiers. Submission Submit a UTF-8 CSV with exactly two columns in this order: molecule_id,resonance_groups. Include every test ID exactly once. Obtain each N from the public input table and emit exactly 3N decoded bytes. Follow sample_submission.csv for the complete test ID list. Missing, extra, duplicate or malformed IDs, wrong columns, an empty file or an incorrect row count score zero for the entire submission. Invalid or noncanonical Base64, more than 260 encoded characters, incorrect decoded length, noncanonical cluster labels or nonnested partitions score zero for that row. Row order does not affect the score. Execution constraints Use one NVIDIA A10G within a 90-minute offline solution session. Train all learned parameters from random initialization using the supplied training data. Neural training and inference must use GPU tensor computation. CPU data loading, graph parsing, control flow and CSV serialization are allowed. No pretrained weights, external embeddings, outside datasets, spectral database lookups, hosted APIs, internet access, manual test annotation or hard-coded test predictions are permitted. Software developed for this benchmark must use an OSI-approved open-source license.
> Closes in 21m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## First Marks

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73tg0eg3rf47mgw55xt1ze8d8e5wzb
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat killshark's score of 0.387!

Full challenge description from page:

> Task Rank 40 opaque intent tokens for each 64-by-64 image of an opening drawing trace. Blue-violet marks occur earlier and red-orange marks occur later. Color preserves segment order; time gaps, pressure, later points, and later traces are absent. Data public/train.csv contains id,image,ranking; public/test.csv contains id,image. Images are under public/images/. In training, ranking is a label container, not a fully supervised order. Element 0 is the only ground-truth label: the recorded intent for that image. Elements 1 through 39 are deterministic filler, formed by hashing the row ID with each remaining token. Their order contains no relevance, similarity, tie, or weak-supervision signal and must be ignored during training. The full permutation is stored so the training label and submitted prediction use the same ranking field and every row carries the complete allowed vocabulary. Training has 15,003 drawings and evaluation has 1,900. IDs match k_[0-9a-f]{24}x; intent tokens match c[0-9a-f]{8}. Both are opaque and non-ordinal. The dataset has exactly 40 unique intent tokens in one fixed global pool. Fit a 40-class visual model using only element 0 of each training ranking as the class label. At inference, sort the model's 40 class scores from highest to lowest and submit that permutation. The candidate pool never varies by image. Exact canonical opening-trace components stay in one partition. Conflicting components are removed and duplicates are collapsed before a target-blind hash assigns train, evaluation, or reserve. This prevents the same retained geometry from appearing on both sides. The reserve keeps training counts from revealing evaluation totals. Metric If the true intent appears at rank r, row credit is 1/r. Let H_40=sum(1/r for r=1,...,40) and let MRR be mean row credit. The score is: clip((MRR-H_40/40)/(1-H_40/40),0,1) The grader reads only element 0 of the hidden answer as the true intent. It ignores the hidden order of the other 39 tokens, then finds the true intent's position in the submitted ranking. Requiring all 40 submitted tokens measures whether the model places the true class first, near the front, or far down the list without inventing relevance labels for incorrect classes. Rows have equal weight. Subtracting H_40/40 maps random ordering to 0 without changing the order of above-chance systems; a perfect ranking scores 1. Submission Submit exactly id,ranking. ranking must be canonical JSON containing every released intent token exactly once, from most to least likely. id,ranking k_0123456789abcdef01234567_x,"[""c_00583fe4"",""c_02935974"",""c_06955a95"",""c_094a09e9"",""c_0abb62a8"",""c_0b3970e1"",""c_0d4a0f5a"",""c_12a38b05"",""c_12ec9d0b"",""c_12f769c1"",""c_145552d7"",""c_14e4e6ad"",""c_1564e3c6"",""c_1686fd90"",""c_19073c45"",""c_1a88ee12"",""c_23177939"",""c_23c0db02"",""c_28cad15e"",""c_35e72d5d"",""c_3670fe71"",""c_36eadf0f"",""c_37238b12"",""c_3b19e959"",""c_3b1b478b"",""c_3d0e01f4"",""c_436ecad5"",""c_443dd6fb"",""c_469b6c1d"",""c_491238e1"",""c_4a74ab85"",""c_516e27ad"",""c_51a11644"",""c_5a46ede6"",""c_5c3f70cc"",""c_5cec8e3d"",""c_5ec5a498"",""c_61dd6ab0"",""c_6201e988"",""c_639349a8""]" Malformed columns, IDs, JSON, duplicate or missing tokens, and incomplete row coverage raise ValueError. Rules Fit a visual model from scratch on the released training images. CNNs, sequence-aware image models, vision transformers, train-only augmentation, calibration, and ensembles are allowed. Do not use pretrained artifacts, outside or synthetic data, source recovery, image lookup, manual mappings, hardcoded rankings, pseudo-labeling, aggregate test fitting, test-time adaptation, private files, network access, package installation, subprocesses, or host inspection. The result measures ranked intent retrieval from a sealed temporal-color opening trace. &nbsp;
> Closes in 4h 33m
> 11 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Gel Crosslinking State Ranking from Bead Trajectories

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx715whk275vqzw8y63fhwjr8n8bwhjn
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Gel Crosslinking State Ranking from Bead Trajectories Overview Drop micron-scale beads into a polymer solution and film them. In a liquid the beads wander freely. As the polymer crosslinks into a gel, the network closes around each bead and traps it, and the wandering turns into rattling inside a cage. This is how microrheology measures a material without touching it. These are real microscope recordings of polyacrylamide crossing its sol-gel transition — six crosslinker concentrations, filmed under one set of optics, roughly 200 tracer beads per frame at 30 frames per second. Nothing here is simulated from a stochastic motion model, so there is no generating process to invert and no model-class prior to exploit. The obvious readout is how far the beads move. On this data each gel's median step size tracks crosslinker concentration at a correlation of -0.989, so a benchmark that kept amplitude would partly be a benchmark of wobble size. So the amplitude is taken away. Every trajectory released here has been rescaled to the same step size. Rescaling alone is not enough. What it leaves behind has one dominant number: how far a trajectory spreads from its own centre — its radius of gyration — which is a direct readout of the cage. On unmatched slates built from these recordings, ranking by that number alone scored 35.53, against 30.61 for a trained model. A benchmark that left it in would mostly be a benchmark of one statistic. So the spread is matched as well. The five trajectories of every slate are chosen to have nearly the same radius of gyration. What survives is how the motion is organised in time — whether successive steps are independent or anti-correlated, whether displacement keeps growing with lag or flattens into a cage, how the path bends and turns — and reading that is the task. On this build, ranking by radius of gyration scores 80.91. The best of about twenty single descriptors, asphericity, scores 69.16. Those are the untrained floors; everything past them has to be learned. Models must be trained from scratch. No pretrained weights, no fine-tuning, no distillation from a pretrained teacher. There is no foundation model for normalised bead trajectories, and the released tracks carry no absolute scale, position or orientation for one to key on. Every parameter must be learned from the training slates. The benchmark contains: 5,000 training slates, in two folds of 2,500 900 test slates 6 gels spanning the sol-gel transition, five of which appear in any one slate The Task Each slate holds five bead trajectories from five neighbouring gels, in shuffled order. The label belongs to the material, not the trajectory. Two beads with identical motion statistics can carry different answers because they sat in different gels, and no single bead carries an answer at all — only its position among the five offered. There is nothing per-trajectory to regress against. Neighbouring matters. Across the full crosslinker range the gels behave very differently: over all of a gel's trajectories, the median mean-squared-displacement exponent falls from 0.80 in the least crosslinked gel to 0.04 in the most. Within a window of adjacent gels the difference is subtle — through the middle of the range the medians sit at 0.39, 0.31, 0.30, and the two most crosslinked gels at 0.055 and 0.043. Matching makes it harder still. A slate's five trajectories come from the stretch where the gels' radii of gyration overlap — the more confined beads of a looser gel beside the freer beads of a tighter one — so the typical difference between two gels is not what separates their trajectories here. Some pairs stay close to a coin flip for every solver measured: 0.06 against 0.0625, 0.0625 against 0.065, and 0.0725 against 0.075. With six gels and five to a slate there are two windows, and which one a slate is drawn from varies: 0.02 to 0.0725 wt% bis — includes the liquid-like 0.02 gel; ranking by asphericity scores 56.6 on these slates 0.06 to 0.075 wt% bis — every gel is near or past the gel point; the same ranking scores 78.9 Fitting one anomalous-diffusion exponent per trajectory and sorting is the standard move in trajectory analysis. On matched slates it scores 84.27 — barely better than guessing. Return the ordering, from least set to most set: ranks — a list of exactly five integers, a permutation of 0..4. ranks[i] is the position of the i-th trajectory within this slate: 0 for the least crosslinked of the five, 4 for the most. Every rank must be used exactly once. Ranks are slate-relative, so they say nothing about which absolute window the slate came from. The output is a permutation. It is not a class label and not a number. Dataset Under ./dataset/public/: train.csv — slate_id, trajectories, ranks test.csv — slate_id, trajectories sample_submission.csv — a valid submission in the required format build_summary.json — slate size, trajectory length, counts, the concentrations used, the recording left out, how the slates were matched, and which training slates belong to each fold trajectories is a JSON list of five trajectories. Each trajectory is a list of 64 [x, y] coordinate pairs, sampled at 30 frames per second. ranks in train.csv is the true ordering for that slate, in the same format required of a submission. Training folds The training slates come in two folds of 2,500. train.csv lists fold 0 first — its first 2,500 rows — and fold 1 after, and build_summary.json names every slate of each fold under train_folds.slate_ids. Each recording's training frames are cut into two consecutive stretches, one per fold, and every slate draws all five of its trajectories from a single stretch, so the two folds share no frames and no bead tracks. The test slates come from a third, later stretch. Validate across folds, not within one. Slates inside a fold reuse the same few hundred tracks per gel, so a model checked against a random slice of its own training slates can keep improving on that check while it memorises individual tracks — and get worse on the test set, whose tracks all come from later frames. A model trained on one fold and checked on the other is asked the question the test set asks. What has been done to the trajectories Each recording is first corrected for drift. The whole field of view creeps slowly — up to about 1.5 pixels over the first 560 frames of a recording — carrying every bead with it, so the median frame-to-frame motion of all beads is subtracted. Each released trajectory is then translated so it begins at the origin, divided by its own root-mean-square step, and turned by a random rotation and a random reflection. Three consequences worth planning around: absolute position and absolute scale carry no information, by construction every trajectory in every slate has identical step magnitude, so any statistic of displacement size is constant across the slate and cannot separate anything direction carries no information either — bead motion in a gel has no preferred axis, so the rotation changes no label, and it removes the camera's axes, along which vibration and residual drift would otherwise identify a recording How slates are matched Each slate takes one target value of log(Rg / RMS step) — the logarithm of the radius of gyration over the root-mean-square step, which is the same before and after rescaling — and every trajectory in the slate lies within 0.05 of that target: the target is the value of a random candidate window from a random gel in the slate's window each gel then contributes a window with a value in [target - 0.05, target + 0.05] so any two trajectories of a slate differ by at most 0.10 in log, about 10% in radius of gyration candidate windows start every 4 frames along a track a window is skipped if any of its steps is longer than 3.5 times its own RMS step, which at that size is a linking error a window is also skipped if its RMS step is more than 2 times that of the median window from the same gel and stretch; matching draws on the tails of each gel's distribution, where jittery stretches with outsized steps collect Between 60% and 74% of draws find a matching window for every gel, depending on the split; the rest are redrawn. build_summary.json records the rule and the shares. The seventh recording in the source, 0.0525 wt% bis, is not used. Only 401 of its 800 frames are present and they are not consecutive, so its trajectories would mix steps of different durations. Measured on this build, a solver that ranks by residual step size scores 98.69, against an average of 99.32 for random orderings whose twenty draws reached as low as 97.53 — the shortcut is dead, not merely weakened. Evaluation Scores run from 0 to 100 and LOWER IS BETTER. The score is an error, not an accuracy. A perfect submission scores 0; guessing scores 100. Kendall's tau is used rather than exact-permutation match so that getting most of an ordering right still earns credit. With slates this hard an exact-match metric would sit near zero for everyone and stop separating a good solver from a mediocre one. tau_i = Kendall's tau between the submitted and true ranks of slate i score = 100 * clip(1 - mean(tau_i), 0, 1) With five trajectories there are 10 pairs, and each pair placed in the wrong order lowers that slate's tau by 0.2: 0 pairs wrong: tau 1.0, error 0.0 1 pair wrong, e.g. one adjacent swap: tau 0.8, error 0.2 2 pairs wrong: tau 0.6, error 0.4 5 pairs wrong: tau 0.0, the level of a random guess 10 pairs wrong, the exact reverse: tau -1.0 A submission that got exactly one pair wrong on every slate would score 100 * (1 - 0.8) = 20. The floor is 100 and cannot be undercut. Random orderings have an expected mean tau of 0 and score about 100. Any submission whose mean tau is at or below zero — including the exact reverse of the truth, mean tau -1 — is clipped to 100. Being systematically wrong earns nothing. There is no per-item accuracy to optimise here. The ordering is one joint decision over five trajectories, and only that decision is scored. Submission Format submission.csv with two columns: slate_id,prediction_json slatete_xxxxxxxxxxxx,"{""ranks"":[2,0,4,1,3]}" Requirements: Every slate_id in test.csv exactly once — no duplicates or omissions. ranks must be a genuine permutation of 0..4: five whole numbers, each rank used exactly once. Repeated ranks, fractional values, booleans and strings are rejected. Other keys inside prediction_json are ignored, as are extra CSV columns and row order. Malformed submissions raise an error during grading. What Not To Use Pretrained weights of any kind. Train from random initialisation on the provided training slates only. No checkpoints from any hub, no fine-tuning, no distillation from a pretrained teacher. Submissions using pretrained weights are disqualified regardless of score. GPU. Solutions run on CPU alone, with 10 cores and 64 GB of RAM. The private answers file, or anything derived from it. Hardcoded slate_id to ordering lookup tables. External LLM or hosted APIs at any point. Allowed and expected: any architecture trained from scratch, hand-engineered dynamical descriptors, ensembling, cross-validation, and reasoning across a whole slate at once — the ordering is a joint decision over five trajectories and treating it as such is part of the task. &nbsp;
> 0 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Anonymous Physiological Synchrony Cohort Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7an4fw1y6eea9g5tzzw0d8kx8e4q6y
- DOMAIN exactly as displayed: FROM SCRATCH
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: ?
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Medium
> Anonymous Physiological Synchrony Cohort Recovery
> Overview Predict which anonymous brain-and-body recordings were captured while different people watched the same exact two-second moment of an educational video. Each test case contains 12 short multimodal recordings from 12 different participants. The recordings come from three nearby moments of one lesson. Exactly four recordings belong to each moment, but their order is shuffled. Your model must recover the three hidden groups by assigning a probability to every pair of recordings. For example, if recordings 0, 3, 7, and 9 came from one moment, all six pairwise links among those four recordings are positive. The other two hidden groups are encoded in the same way. A complete answer therefore has 66 probabilities: one for each unordered pair among 12 recordings. The source study recorded adults seated in a sound-attenuated booth while they watched short explanatory videos. Signals were sampled in synchrony with the video. The released views combine scalp electrical activity, cardiac activity, eye position, pupil size, and head motion. Two viewing sessions were collected under different attention instructions. The challenge removes participant identity, lesson identity, timestamps, filenames, experiment labels, and condition labels. The practical capability being tested is anonymous synchronization recovery. Similar problems arise when separately stored wearable or laboratory streams lose shared clock labels, when privacy-preserving exports remove participant and stimulus identifiers, or when multiple sensor uploads must be reconciled without using content files. This is a From Scratch GPU challenge. It is a fixed-size graph prediction problem, not sequence generation, forecasting, image classification, ordinary tabular learning, or per-record multiclass classification. Objective For every row in test.csv: Load the associated 12 x 64 x 256 tensor from cohort_tensor_bank.npy. Compare the 12 anonymous multimodal traces jointly. Predict the probability that each pair of traces came from the same lesson moment. Submit the 66 probabilities in the exact edge order defined below. Every hidden target is a balanced partition of the 12 traces into three unlabeled groups of four. Group names do not exist. Only pairwise co-membership matters. Real-world collection and challenge construction The underlying recordings were collected from 31 adults. Each participant watched the same set of five educational videos in two sessions. The five videos range from roughly two to eight minutes. During viewing, the laboratory recorded 64-channel scalp electrical activity at 128 Hz together with eye, pupil, head-motion, and cardiac measurements aligned to the same playback clock. The challenge uses non-overlapping two-second source intervals. Each interval contributes 256 samples per channel. A challenge case is formed from three non-overlapping moments inside one 45-second block of one lesson and one session. The three moments are separated by 14 seconds: one comes from the early part of the block, one from the middle, and one from the later part. Four different participants contribute a recording for each moment. The 12 participant identities are distinct within the case. The target is source-derived: two items are linked if and only if their recordings cover the same source playback interval. No arbitrary class code, artificial pulse, or reusable class template is inserted. Before release, each case receives one row-local sparse projection of the 64 scalp channels. The same projection is used for all 12 items in that case, but a different projection is used in other cases. Robust scaling, quantization, small deterministic sensor noise, and one of five sensor-availability conditions are then applied. The construction also applies a deliberately weak consensus-preserving transform. For each real playback interval, it averages the four transformed source recordings, removes each channel's temporal mean, smooths that real cohort average with the fixed kernel [0.25, 0.50, 0.25], and blends a small amount back into those same four recordings. The blend weights are 0.085, 0.065, 0.075, 0.060, and 0.050 for the five conditions listed below. This transform is disclosed because it is part of the input definition. It does not use a synthetic class signature: every blended value is computed from the four real recordings at that interval. Its purpose is to retain a measurable but weak common-response signal after anonymization and row-local projection. The small weights, independent participants, competing nearby moments, temporal jitter, modality dropout, and hidden condition labels prevent the blend from becoming a direct answer code. Dataset files The prepared dataset contains five public files and one private answer file. train.csv Contains 800 training cases. id: string. A unique anonymized case ID. bank_row: integer. Row index on axis 0 of cohort_tensor_bank.npy. test.csv Contains 240 hidden cases. It has exactly the same feature columns as train.csv. id: string. A unique anonymized case ID. bank_row: integer. Row index on axis 0 of cohort_tensor_bank.npy. train_targets.csv Contains the labels for all 800 training IDs. id: string. Training case ID. cohort_edges: string. JSON list of 66 binary values in the required edge order. 1 means the two items came from the same moment; 0 means they came from different moments. cohort_tensor_bank.npy A NumPy array stored without pickled objects. dtype: uint8. shape: (1040, 12, 64, 256). axis 0: case bank row. axis 1: anonymous item index from 0 through 11. axis 2: transformed signal channel. axis 3: time sample at 128 Hz. The 64 transformed channels are: channels 0 through 46: row-local sparse projections of the 64 scalp electrical channels; channel 47: filtered cardiac waveform; channel 48: instantaneous heart-rate trace; channels 49 and 50: horizontal and vertical gaze-angle traces; channels 51 through 53: three head-position traces; channel 54: pupil-size trace; channels 55 through 63: availability masks for scalp activity and the eight body/eye channels, in that order. Signal channels use the decoding formula: decoded_value = stored_uint8 / 127.5 - 1 The first 55 channels are centered transformed measurements. An availability-mask value of approximately 0.8 means the corresponding source channel was available; a value of approximately -0.8 means it was unavailable or deliberately masked in that case. Sensor noise is applied to the measurement channels, not to the availability masks. sample_submission.csv Contains all 240 test IDs and the required submission columns. Every edge is assigned the uninformed prior probability 3/11. This submission scores exactly 0. Private answers.csv Contains exactly the same columns, in the same order, as sample_submission.csv: id; cohort_edges. It is used only by the grader. Split and leakage controls The true leakage units are participant identity and global lesson-time block. Participant assignment is deterministic. Participants with usable recordings for all ten lesson-session combinations are ordered by a fixed SHA-256 construction hash. The first 13 complete participants are used only for test cases. The other 18 participants are used only for training cases. No participant contributes to both splits. Time assignment is also deterministic. Each video is divided into 45-second blocks after excluding its opening and closing margins. Blocks are ordered by a fixed SHA-256 construction hash separately for each video. A complete block is assigned to exactly one split. Both viewing sessions inherit the same assignment for that lesson block. Therefore, the exact lesson moments used in test never appear in training, even for different people or the other viewing session. Additional protections are enforced during preparation: every participant/session/time fragment is used in exactly one challenge case; no exact fragment hash is repeated; no complete case tensor is repeated; train and test IDs are disjoint; train and test participant hashes are disjoint; train and test lesson-time-block hashes are disjoint; IDs and bank_row values are created after case construction and do not encode the target partition; item order is independently permuted in every case; all three candidate moments come from the same lesson, session, and 45-second block, so topic, recording condition, duration, and coarse temporal context cannot identify a group; participant IDs, source paths, filenames, video titles, timestamps, condition names, experiment numbers, and source row order are absent from public data. The prepared test fraction is 240 / 1040 = 23.08%. Input conditions The data include five equally represented transformation conditions. Their labels are private and are not submission targets. aligned_multimodal: all available modalities are retained with small sensor noise; consensus blend weight 0.085. temporal_jitter: each anonymous item receives a small independent temporal displacement of at most eight samples; consensus blend weight 0.065. ocular_sparse: three eye/body channels are unavailable for each item; consensus blend weight 0.075. neural_sparse: a deterministic subset of projected scalp channels is unavailable; consensus blend weight 0.060. mixed_dropout: smaller neural and eye/body dropouts are combined with temporal jitter and stronger noise; consensus blend weight 0.050. There are 160 training cases and 48 hidden cases from each condition. These conditions prevent one fixed correlation rule or one favored modality from dominating the entire test set. Output representation cohort_edges must be a JSON list containing exactly 66 finite numbers. Every number must lie in the closed interval [0, 1]. Edge order is lexicographic over unordered item pairs: (0,1), (0,2), ..., (0,11), (1,2), (1,3), ..., (1,11), ... (10,11) Equivalently: edge_pairs = [ (i, j) for i in range(12) for j in range(i + 1, 12) ] The first value predicts whether items 0 and 1 share a moment. The final value predicts whether items 10 and 11 share a moment. Probabilities are scored directly. They do not need to sum to one. A strong submission should nevertheless make its 66 values consistent with three groups of four. Valid and invalid predictions A syntactically valid prediction looks like: [0.12,0.91,0.08,... exactly 66 values total ...] Valid entries may be integers or decimal numbers from 0 through 1. The following row-level predictions are invalid and receive worst-case prediction values for that row: an empty string; malformed JSON; a JSON object instead of a list; a list with any length other than 66; NaN, infinity, booleans, strings, or nested lists; a number smaller than 0 or greater than 1. An invalid row is converted to 66 zeros. It cannot gain an abstention advantage. Evaluation Let N be the number of evaluated rows. Let y[r,e] be the binary truth for row r and edge e, and let p[r,e] be the submitted probability. Every target has 18 positive and 48 negative edges, so the analytic uninformed edge prior is: q = 18 / 66 = 3 / 11 All component scores and the final score are clipped to [0, 1]. LogSkill Mean binary log loss is: LogLoss = -(1 / (66 * N)) sum over r,e of y[r,e] * log(max(p[r,e], 1e-15)) (1 - y[r,e]) * log(max(1 - p[r,e], 1e-15)) The constant-prior reference loss is computed analytically: PriorLogLoss = -q * log(q) - (1 - q) * log(1 - q) LogSkill = clip((PriorLogLoss - LogLoss) / PriorLogLoss, 0, 1) Predicting q for every edge gives 0. Perfect probabilities give 1. BrierSkill Brier = (1 / (66 * N)) sum over r,e of (p[r,e] - y[r,e])^2 The constant-prior Brier error is: PriorBrier = q * (1 - q) BrierSkill = clip((PriorBrier - Brier) / PriorBrier, 0, 1) AUCSkill For one row, compare every positive edge with every negative edge. There are 18 * 48 = 864 comparisons. RowAUC = (wins + 0.5 * ties) / 864 A win occurs when a positive edge has a larger probability than a negative edge. A tie occurs when the probabilities are equal. MeanAUC = mean(RowAUC over all evaluated rows) AUCSkill = clip((MeanAUC - 0.5) / 0.5, 0, 1) PartitionSkill There are exactly 5,775 ways to divide 12 labeled items into three unlabeled groups of four. For each possible balanced partition, the grader sums the 18 submitted probabilities on its within-group edges. The unique maximum-sum partition is the decoded prediction. If all probabilities are constant, or if several partitions tie for the maximum within numerical tolerance 1e-12, the row is treated as undecodable. Its overlap is set to the chance value q, and it is not exact. For a uniquely decoded partition: RowPartitionOverlap = number of decoded within-group edges that are truly positive / 18 MeanPartitionOverlap = mean(RowPartitionOverlap over evaluated rows) PartitionSkill = clip((MeanPartitionOverlap - q) / (1 - q), 0, 1) The normalization uses q = 3/11 because each item has exactly 3 true partners among the other 11 items. TailAUCSkill Sort all row-level AUC values from smallest to largest. Let: K = ceil(0.20 * N) BottomAUC = mean(the K smallest RowAUC values) TailAUCSkill = clip((BottomAUC - 0.5) / 0.5, 0, 1) This component rewards models that remain useful on their hardest fifth of cases. ExactPartition ExactPartition = fraction of evaluated rows whose uniquely decoded 18-edge partition exactly equals the hidden 18-edge partition Final score final_score = 0.28 * LogSkill 0.20 * BrierSkill 0.18 * AUCSkill 0.20 * PartitionSkill 0.08 * TailAUCSkill 0.06 * ExactPartition The score is finite and bounded in [0, 1]. The provided constant-prior sample scores exactly 0. A perfect oracle scores exactly 1. No private empirical normalization constants are used. Every reference value in the formulas follows from the fixed 3 x 4 partition structure. Submission format Submit one UTF-8 CSV file with exactly two columns in this order: id cohort_edges The file must contain every test ID exactly once. Rows may appear in any order because the grader aligns by id. Schematic example: id,cohort_edges 8d91c0e7a42b39d45a10,"[0.12,0.91,0.08,... exactly 66 values total ...]" Use ordinary CSV quote escaping around the JSON field. Do not add index columns, confidence columns, group labels, comments, or explanatory text. Structural errors reject the entire submission. These include wrong column names or order, wrong row count, missing IDs, duplicate IDs, unknown IDs, or extra IDs. Recommended modeling directions A basic approach can compute lag-tolerant similarities between all item pairs and fit a calibrated pair classifier. Better systems can learn a shared temporal encoder, perform modality-aware masking, and reason over all 12 item embeddings jointly. Useful model families include: multichannel temporal CNNs with a learned pair head; Siamese encoders with lag-aware cross-correlation features; masked-modality encoders; graph neural networks over the 12-item complete graph; Set Transformers that enforce competition among the three latent groups; differentiable balanced-partition or optimal-transport heads. An A10G is appropriate because each batch jointly encodes 12 dense 64 x 256 streams, forms 66 pair interactions, and may run cross-stream attention or lag-aware matching. The benchmark is designed for 50 to 60 minutes of GPU training, including validation and submission generation. What not to use Do not search for source filenames, participant IDs, lesson titles, timestamps, experiment labels, or original row coordinates. They are not present in public cases. Do not infer groups from item position. Item order is independently permuted for every case. Do not assume the three groups come from different topics or recording conditions. They always come from nearby moments of the same lesson and session. Do not use bank_row, CSV row order, or ID prefixes as target features. They are assigned after case construction. Do not threshold every pair independently without checking global consistency. The hidden answer is always three groups of four. Do not submit group-name sequences, JSON objects, cluster labels, embeddings, model files, or natural-language explanations. Benchmark boundary Intersubject-correlation studies ordinarily begin with known participants watching a known common stimulus and measure average synchrony. Video-identification studies ordinarily compare one recording with a named catalog of candidate clips. Generic clustering benchmarks ordinarily group independent feature vectors without a shared multimodal playback clock. This benchmark withholds both identity and stimulus time, mixes three moments from one short lesson block into one anonymous 12-item set, and asks for a calibrated balanced co-membership graph. It combines source-participant transfer, unseen lesson-time transfer, multimodal missingness, row-local scalp projections, lag tolerance, and set-level consistency. The prediction object and leakage structure therefore differ from ordinary intersubject-correlation estimation, stimulus classification, and generic clustering.
> Closes in 3h 49m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Gas-Chamber Exposure Program Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx778rks9aec3a22shwkmsw5fs8e7re6
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Draft
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Overview A chemical-monitoring rig has lost its controller log, but the multichannel response traces from each exposure remain. Recover the ordered two-stage exposure program from every hidden sensor sequence: dose state first, then moisture state. This is a multiclass sequence-classification task with one joint program label per exposure. &nbsp; Each example is a 256-step, 6-channel float32 sequence from one continuous physical exposure. The first three channels are lower, median, and upper response trajectories across an anonymous sensor set. The final three channels are their first-difference trajectories. Evaluation examples come from unseen acquisition conditions with local calibration and timing variation. The legal program grammar is exactly Cnn>Hmm. The dose token is one of C00, C01, C02, C03, or C04; the moisture token is one of H00, H01, H02, or H03. C03>H02 is valid. Both stages must be recovered in the stated order. Task Load each sequence named in train.csv, train a sequence classifier on exposure_program, and predict one valid program for every ID in test.csv. Intended Approach Use the full temporal tensor. Compact 1D CNNs, temporal convolutional networks, recurrent models, and small Transformers trained from scratch are suitable. A multi-task model may use separate dose and moisture heads plus a joint-program head. Validation should hold out coherent acquisition groups or simulate calibration drift rather than use only a random row split. Dataset train.csv test.csv signal_spec.json sample_submission.csv train/signals/ID.npy test/signals/ID.npy train.csv has 900 rows and these columns: id: opaque episode identifier. signal_path: relative path to the episode tensor. exposure_program: training label in Cnn>Hmm form. test.csv has 400 rows and the same first two columns, without the label. Tensor shape and dtype are declared once in signal_spec.json rather than repeated as constant manifest columns. Every .npy file is finite float32 with shape (256, 6). Channel order is: 0: set_level_q25 1: set_level_q50 2: set_level_q75 3: set_delta_q25 4: set_delta_q50 5: set_delta_q75 Submission Submit exactly two columns in this order: id,exposure_program. For example, gx_0023b592c429063d,C04>H00 is one valid row. There must be exactly one row for every test ID. Missing, extra, duplicate, or unknown IDs and missing, extra, renamed, or reordered columns are invalid submissions. A malformed program in an otherwise structurally valid row earns zero credit for that row. Evaluation Score = 0.25 times dose macro-F1 + 0.25 times moisture macro-F1 + 0.50 times exact complete-program accuracy. Macro-F1 covers all five dose classes and all four moisture classes. Exact accuracy rewards only rows where both ordered tokens are correct. The metric is linear, bounded from 0.0 to 1.0, and a perfect submission returns exactly 1.0. Runtime and Dependencies Solutions run offline with a 90-minute limit on one NVIDIA A10G. Use libraries already available in the challenge environment, such as NumPy, pandas, scikit-learn, and PyTorch. Network calls, hosted APIs, and downloading external weights or data are not allowed. Train any learned model from scratch using only the provided public files. What Not To Use Upstream-corpus retrieval, source fingerprinting, checksum matching, or nearest-neighbor lookup. Source filenames, dates, timestamps, raw row order, acquisition identity, IDs, paths, file sizes, hashes, metadata, private answers, or grader side channels. External labels, network services, hosted APIs, pretrained weights, or external embeddings. Fixed lookup tables, source-specific parsers, one-head-only submissions, or rule-only program templates. &nbsp;
> 3h ago
> $400–$500
> Draft

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Streamflow Signature Matching

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74ajb2esqmdbqma25szq1hh98edtce
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 0.790!

Full challenge description from page:

> Overview: This is a retrieval problem. You are given one unidentified measurement profile and a gallery of candidate monitoring sites, and you rank the gallery so that the site the profile came from appears as high as possible. Nothing is forecast, nothing is extrapolated, and no quantity is estimated: the deliverable is an ordering of candidates. Each site is a river monitoring station, and a profile is 180 successive discharge measurements taken at one station. The query profile and the correct candidate were captured on two entirely separate occasions, far enough apart that the conditions have nothing in common - different storms, different droughts, no shared events at all. The question is whether a station is still recognisable from the character of its record when none of the circumstances are shared. The one property that would make this trivial has been removed. Every profile is log-transformed and then standardised to zero mean and unit variance, so the size of the river is gone. A small creek and a major river arrive looking equally large, and ordering candidates by magnitude achieves nothing. What survives is the character of the trace: how sharply the reading climbs when water arrives, how long it takes to fall back, whether it settles onto a steady floor or decays toward nothing, whether it is smooth or rough between events, whether something upstream is holding it up. Whether that character is a durable property of the site, or merely a property of the conditions on the occasion you happened to look, is the open question. The measured answer is that it is partly durable: matching by summary statistics of the standardised profile scores 0.272 against 0.092 for guessing. There is a real signature, and roughly three quarters of the available score is not reachable by any summary statistic tried here. Task definition: A case is a query profile q and a gallery G of n candidate profiles, 25 <= n <= 79. Exactly one element of G came from the same monitoring site as q; every other element came from a different site in the same region. You submit an ordering of G and are scored on where the correct one lands. The prediction unit is one ranking per case, produced independently for each of 811 evaluation cases. It is not a label, not a numeric estimate, and not one global model output. There are 1,924 training cases with their answers and 811 evaluation cases without. Every profile is 180 numbers. The gallery for a case is shared by every query in that region, so the same candidate appears in many cases; how often a candidate occurs across the dataset therefore carries no information about any individual case, and was measured at the guessing floor. What the inputs are, exactly: Each profile is 180 successive discharge measurements from one station, transformed once, before release, by exactly these steps: Measurements are taken in their original physical unit, non-negative. A transform of the form log(1 + x) is applied, compressing the range without discarding small readings or failing on zeros. The profile is standardised to zero mean and unit standard deviation. What follows from that. Absolute magnitude is unrecoverable, so the size of the catchment cannot be used. Within a profile the relative structure is preserved exactly: the sharpness, timing and asymmetry of every rise and decay survive, as does the roughness between them. Between profiles nothing is comparable in absolute terms, only in character. The 180 values are given in acquisition order, so neighbouring values are adjacent readings and local structure is meaningful. What is not provided, in any form: the identity or name of any site, its location, its region in any interpretable form, the calendar on which any profile was captured, the river, the drainage area, the climate, any catchment attribute, any upstream regulation, and any second measured quantity such as rainfall, temperature or stage. Region codes are opaque and exist only to say which candidates form a gallery. The query and the correct candidate come from occasions that do not overlap and are separated by several cycles, so they share no events. A surge visible in the query is not present in the reference, and matching by aligning events does not work: the measured correlation route reaches only 0.130. Supervision and split: The split unit is the monitoring site. A site contributes to training or to evaluation, never both, so every identity in the evaluation set is one the training data has never seen. A solution therefore cannot learn a fixed set of classes; it has to learn what makes any two profiles come from the same site. Galleries are built inside a split. No candidate appearing in an evaluation gallery appears anywhere in the training data, which was verified directly: zero evaluation candidates occur in any training gallery, and zero evaluation answers occur among the training answers. Discarding candidates that are known training answers therefore gains nothing and scores below the floor. Evaluation: The metric is the mean reciprocal rank, written MRR. Each case has exactly one correct candidate. Find its position in your submitted ranking, take one divided by that position, and average over every evaluation case. Putting the right site first scores 1 for that case, second 0.5, tenth 0.1, and omitting it entirely scores 0. The challenge score is that mean, so it runs from 0 to 1 and higher is better. Why this metric: there is exactly one correct answer per case, so reciprocal rank is the natural measure and no aggregation weight needs justifying. Mean average precision would be numerically identical, since average precision with a single relevant item reduces to the reciprocal rank. The metric depends only on the order of your scores, so it is invariant to any monotone rescaling of whatever similarity you rank by, which means there is no calibration to tune and no threshold anywhere in the evaluation. No second component is combined with it: a recall-at-k term would discard information MRR already uses, and a per-region macro average would be redundant because every case contributes exactly one reciprocal rank regardless of which gallery it came from. Galleries differ in size between 25 and 79 candidates, so the guessing floor is not one number per case; the figures below are averaged over the evaluation set exactly as a submission would be. Floor and ceiling, all measured on the evaluation cases. A perfect submission scores 1.0. Guessing scores 0.092. Four routes that use no signal land exactly there: the supplied sample_submission, which lists each gallery in its given order, scores 0.092; sorting candidate identifiers alphabetically scores 0.092; ranking by how often a candidate appears across the dataset scores 0.092; and a random shuffle scores 0.089. Discarding candidates that are known training answers scores 0.085, below guessing. Ranking by correlation between the raw query and candidate profiles scores 0.130. The strongest route that involves no learning is a nearest-neighbour match on summary statistics of the profile - quantiles, step-to-step change, lag-1 and lag-5 self-similarity, skew, kurtosis - at 0.272, and that is the number to beat. Dataset: The following files are provided in public/. train.csv - one row per training case, 1,924 rows. case_id - text - identifier for this case. region - text - an opaque code for the gallery this case belongs to. Candidates are only ever drawn from within one region. query_id - text - the profile id of the query, joining to profiles.csv. n_candidates - integer - the size of this case's gallery, between 25 and 79. candidate_ids - text - the gallery's profile ids, space-separated. Exactly one came from the same site as the query. All cases in a region share the same gallery. train_labels.csv - the training answers, one row per training case, 1,924 rows. Join on case_id. case_id - text - identifier matching train.csv. correct_candidate_id - text - the profile id of the candidate from the same site. test.csv - one row per evaluation case, 811 rows, with exactly the same columns as train.csv in the same order. Its sites appear in no training case and no answers are provided. profiles.csv - one row per profile, 5,470 rows, covering every query and every candidate. profile_id - text - the identifier referenced by query_id and candidate_ids. f000 to f179 - number - the 180 values of that profile, in acquisition order, transformed and standardised as described above. Rounded to four decimal places. sample_submission.csv - a correctly formatted submission listing each gallery in its given order, scoring 0.092. Submission: Submit a CSV with exactly these two columns, named exactly as shown. A submission whose columns are renamed is rejected rather than scored. case_id - text - one row for each case_id in test.csv, 811 rows plus a header row. ranked_candidate_ids - text - that case's candidate profile ids, space-separated, best first. Rank all of them; the correct candidate scores zero for that case if you leave it out. Example, with fabricated identifiers for illustration: case_id,ranked_candidate_ids case_0001example,ref_00000000aa ref_00000000bb ref_00000000cc case_0002example,ref_00000000cc ref_00000000aa ref_00000000bb Requirements: a header row, one row per evaluation case, in any order. Write the file without a pandas index column. An empty ranked_candidate_ids cell scores zero for that case rather than being rejected, and a duplicated case_id is rejected. Rules: The only valid input signal is the numbers in profiles.csv and what you learn from the training cases and their answers. The following approaches are not allowed: Hardcoding a ranking for specific evaluation cases. Using the case_id, region or profile_id strings as a prediction signal. They are opaque hashes provided so you can join rows, not so you can mine them. Using the order of candidates inside candidate_ids, or the row order of any supplied file, as a prediction signal. Gallery order is fixed per region by a seeded hash and carries none, which was measured: the supplied order scores exactly the guessing floor. Using how often a candidate appears across the dataset as a prediction signal. Every candidate in a region appears in every case of that region, so this carries nothing by construction, and it was measured at the floor. Using whether a candidate appears in train_labels.csv as a prediction signal. Galleries are closed inside each split, so no evaluation candidate appears in training at all. Identifying the real monitoring network these records come from and consulting it in any form: the publishing agency's data, a mirror, a hosted copy, or any other archive of river measurements. Recovering the real station behind a profile, and then matching by station identity or by looking up the same stretch of record, is retrieval of the answer key rather than modelling. Station identities, locations, regions and the calendar of every profile are withheld precisely to prevent this. Using any external hydrological, meteorological or geographic dataset to reconstruct which station or which stretch of record a profile came from. Using private, role-gated, or API-key-based models, or calling any external inference API at inference time. Using non-reproducible external weights or artifacts not publicly available. The intended task is to learn what makes two records come from the same place: the characteristic speed of the climb and the decay, the roughness of the trace between events, how completely the reading falls away when nothing is arriving, and how much of that survives when the circumstances are entirely different. The exploits above bypass exactly that, and every structural one of them was measured during construction and sits at the guessing floor. Pretrained model policy: There is no pretrained model for this signal. Nothing here can be solved by recalling text or images, no public checkpoint was trained on anything resembling it, and there is no backbone to fine-tune. Any approach has to be built and fitted from scratch on the supplied training cases, which is what makes this a from-scratch problem rather than an adaptation one. The natural routes are a learned embedding of the profile trained with a metric or contrastive objective over the 1,924 training cases, a learned pairwise comparator over profile pairs, or engineered descriptors fed to a learned ranker. Whichever you choose, reproduce the 0.272 summary-statistic baseline first and check that your model beats it, because a system that does not is contributing nothing over classical descriptors. &nbsp;
> 3 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Flood Connection Recovery Across Radar Gaps

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ck1g6py3n0janq7stwte0gd8eb88c
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 0.435!

Full challenge description from page:

> Flood Connection Recovery Across Radar Gaps Overview Recover which survey points inside a missing strip of post-event radar belong to newly flooded waterbodies, and which points share the same waterbody. Two pre-event observations, elevation and the remaining post-event radar provide context. The missing strip is a controlled acquisition-gap simulation, not a claim that the source instrument actually lost those measurements. The target is not just a water/nonwater class per point: two flooded points can be connected by a path elsewhere in the tile, including outside the gap. Infer their grouping using the entire visible spatial and temporal context. Dataset There are 1,266 training tiles from 26 events and 913 test tiles from 16 other events. All derivatives of a source event stay together in either training or the combined held-out test set. Each original source tile contributes at most one native-resolution crop; pixels and survey points are not independent source samples. An event contributes at most 250 retained tiles. One of nine nonoverlapping windows per source tile is selected, preferring a window with new flood on a regular survey grid when available. Event-level stratification balances row and flood support; this enriched benchmark does not reproduce real-world flood prevalence. Public files are train.csv, test.csv, sample_submission.csv, evidence/.npy, and training_masks/.npy. Asset paths are relative to the public directory. Train columns are id,evidence_path,connections; test columns are id,evidence_path. | Input | Definition | |---|---| | id | Unique opaque alignment string | | evidence_path | Relative path to float32 array of shape (9,64,64), in channel, row, column order | | Channels 0,1 | Older pre-event radar, VV and VH polarization, in dB | | Channels 2,3 | Newer pre-event radar, VV and VH polarization, in dB | | Channels 4,5 | Post-event radar, VV and VH polarization, in dB, unavailable in the simulated gap | | Channel 6 | Elevation in metres, not flood depth | | Channel 7 | Source-valid mask: 1 valid, 0 invalid | | Channel 8 | Post-event-observed mask: 1 visible, 0 unavailable | | training_masks/.npy | Training-only uint8 (64,64) supervision: 1 newly flooded, 0 otherwise, including the hidden strip. No test masks are supplied | Pixels are nominally 10 metres across; each tile is 640 by 640 metres. Zero-based columns 24 through 39 inclusive are the sixteen-column gap, spanning all rows. Channels 4 and 5 are zero there and channel 8 is zero. The two pre-event observations and elevation remain available at source-valid gap pixels. The gap occupies one quarter of the tile, leaving observed post-event context on both sides. Outside the gap, channel 8 equals channel 7. At source-invalid pixels, channels 0 through 6 are zero. Do not interpret missing zeros as measured 0 dB: use the masks. Before this challenge's gap masking, radar powers were converted to 10 log10(max(power,0.00000001)), computed in float64, clipped to [-80,40] dB and stored as float16; elevation was also stored as float16. Public arrays convert those values to float32 without restoring lost precision. At least 98% of each retained tile is source-valid. Source labels distinguish nonwater, permanent water, new flood and invalid; only valid new flood is positive for this task. Permanent water is not a positive target. Target There are sixteen survey points, indexed 0 through 15 in row-major order at (row,column) coordinates with row in {3,11,19,27,35,43,51,59} and column in {27,35}. Thus point 0 is (3,27), point 1 is (3,35), and point 15 is (59,35). Every point is inside the simulated gap. Form four-neighbour connected components of the valid newly flooded pixels over the whole 64-by-64 tile. A point is dry for this target if its pixel is not valid new flood. Otherwise its group consists of survey points in the same component. Connections outside the crop are not considered. Components with no survey point need not be predicted. Submission Submit exactly 913 rows with exactly id,connections in that order. Include every test ID exactly once; row order may change. connections is a string of exactly 32 characters, two characters per survey point in index order, without separators. Use -- for a dry point. For a flooded point, encode the smallest survey-point index in its component as two lower-case base-36 digits: 00,01,02,03,04,05,06,07,08,09,0a,0b,0c,0d,0e,0f. Every member of a component uses the same code, and that code must identify the component's smallest member. Single-point components are allowed. No other codes or alternative component names are valid. An illustrative valid row with all points dry, using an illustrative ID: id,connections example,-------------------------------- Evaluation Use component-balanced matched port-set IoU. For a predicted group P and a true group T in the same row, IoU = |P intersection T| / |P union T|. Find a one-to-one matching maximizing the sum of these overlaps within each row. Unmatched groups contribute zero; groups are never matched across rows. Across the evaluated rows, let S be the sum of matched IoUs, Np the total predicted group count and Nt the total true group count. The score is S / max(Np,Nt). If both counts are zero, return 1; if exactly one is zero, return 0. Correctly dry rows add no true-negative credit. The combined held-out test set contains flooded groups. Splitting one waterbody or merging different waterbodies reduces the matched overlap, without awarding credit for arbitrary component numbering. Maximize the score, with theoretical bounds 0 and 1 and gold optimum 1. Missing, extra, duplicate, blank or padded IDs; missing, extra, reordered or duplicate columns; ragged CSV rows; malformed lengths; invalid, noncanonical or out-of-range tokens; NaN or infinity reject the submission with an explicit error. Invalid row values identify the offending ID. The grader does not repair outputs or use hidden fallback predictions. Expected Approach Train a spatial neural model from randomly initialized weights, using the supplied training flood masks and connection targets. GPU training is supported. Temporal feature construction, segmentation, missing-observation modeling, training-only validation, augmentation, ensembling and deterministic component decoding are allowed. A trained model must participate in prediction. Fit learned preprocessing statistics on training data only. Public-only joint test inference is allowed. What Not To Use Do not use pretrained weights, externally trained embeddings, outside datasets, external source lookup, original-identifier recovery or external metadata joins. Do not access private answers or raw source labels during participant training or inference. Do not hardcode test predictions or hidden mappings.
> Closes in 5h 6m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.


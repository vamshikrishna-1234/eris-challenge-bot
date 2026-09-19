# CPU Computer Vision Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed CPU examples in this document: 57

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.

## Partial-Context Axial Nanoparticle Localization

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77j8ywksnbkejtvrq6y3cax18ap9r8
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Beat abhi404's score of 0.330!

Full challenge description from page:

> Partial-Context Axial Nanoparticle Localization
> Overview
> This challenge asks you to classify how the nucleus-relative location of gold nanoparticle aggregates changes through depth in real tumor-spheroid cells imaged with serial block-face scanning electron microscopy. Each sample has a grayscale montage of the same cell-centered region in three ordered depth planes and a separate structural reference for the central plane. The montage panels run from lower to central to upper section and are separated by narrow gray dividers.
> The structural reference is a 176x176 label image aligned with the central panel. Background is encoded as 0, a deliberately coarse cell region as 96, and a deliberately coarse nucleus region as 224. The cell and nucleus annotations are reduced to 16x16 and 8x8 grids respectively before being expanded to the public image size, so they provide approximate location rather than precise boundaries. The reference contains no nanoparticle mask, particle location, target label, lower-plane structure map, or upper-plane structure map. It supplies a partial anatomical frame of reference; solvers must still identify nanoparticle evidence in the electron-microscopy panels and compare it through depth.
> The task is axial spatial reasoning, not temporal forecasting. A sample may remain peripheral through all three sections, remain perinuclear, move from a peripheral section to a perinuclear section, move in the opposite direction, or reverse around the central section. Samples are provided at four physical plane spacings, so strong solutions must compare cellular ultrastructure and nanoparticle position across panels rather than rely on one static frame or total brightness.
> Evaluation
> Submissions are scored with macro F1 across five axial-localization classes. F1 is computed independently for each class, and the final score is the unweighted mean of the five class F1 values.
> The score ranges from 0 to 1. Higher is better.
> Target classes:
> 0 - persistently peripheral: all three sections are peripheral-dominant.
> 1 - persistently perinuclear: all three sections are perinuclear-dominant.
> 2 - peripheral to perinuclear: the lower section is peripheral-dominant and the upper section is perinuclear-dominant.
> 3 - perinuclear to peripheral: the lower section is perinuclear-dominant and the upper section is peripheral-dominant.
> 4 - axial reversal: the lower and upper sections agree, while the central section has the opposite localization state.
> These labels describe ordered spatial sections. They do not imply physical particle motion or a temporal direction.
> Dataset
> The prepared public dataset contains:
> train.csv - training image identifiers, image paths, dimensions, plane spacing, and target labels.
> test.csv - test image identifiers, image paths, dimensions, and plane spacing.
> sample_submission.csv - a valid submission template with deterministic non-constant example labels.
> images/ - transformed three-plane grayscale PNG montages.
> contexts/ - central-plane cell references with coarsened nucleus regions.
> manifest.json - prepared split and schema summary.
> train.csv columns:
> id - string sample identifier.
> image_path - relative path to the prepared PNG image.
> context_path - relative path to the aligned central-plane cell and coarse-nucleus PNG.
> width - image width in pixels.
> height - image height in pixels.
> plane_count - number of ordered depth panels. Always 3.
> plane_spacing_nm - distance from the central panel to either neighboring panel, in nanometers. Values are 200, 400, 600, or 1000.
> axial_localization_class - integer target label from 0 to 4.
> test.csv has the same feature columns, but does not include axial_localization_class.
> Each montage contains lower, central, and upper views of the same cell-centered region. Prepared microscopy images include deterministic orientation, crop, intensity, blur, and noise variation. The panel order is preserved. Only the transformed central cell/nucleus context is supplied. Lower and upper structure maps, nanoparticle masks, source coordinates, source cell identifiers, and the measurements used to derive the target are not public features.
> The train/test split holds out complete 3D cell identities. Every depth sample and every plane-spacing variant from a source cell occur in only one split. The prepared split contains 28 training cells and 15 private test cells, with no source cell shared across the splits.
> Submission
> Submit a CSV file with this exact header:
> id,axial_localization_class
> Example:
> id,axial_localization_class
> upt_03a94ea1288bbf76,2
> upt_18d2cb740cad1279,0
> upt_2b971df4bf286304,4
> The example shows the required format only. A real submission must contain exactly one row for every row in test.csv.
> Submission columns:
> id - string identifier from test.csv.
> axial_localization_class - integer predicted class from 0 to 4.
> Requirements:
> Include the header exactly as shown and keep the columns in this order.
> Do not include extra columns.
> Include exactly one row for every test ID and no duplicate IDs.
> Use only finite integer class labels from 0 to 4.
> Practical Notes
> This is a CPU-solvable small-data vision problem. Useful approaches may include structure-aware bright-particle features, explicit lower-versus-upper comparisons, multiscale texture descriptors, pretrained generic vision embeddings, compact convolutional models, and class-balanced validation. The central context should be aligned with each panel before nucleus-relative evidence is compared. plane_spacing_nm should be treated as acquisition context rather than as a substitute for image evidence.
> Validation should preserve source-cell groups when possible because neighboring sections and spacing variants from one cell are correlated. Macro F1 and per-class F1 are more informative than accuracy for this task.
> What Not To Use
> Do not locate, download, query, or reconstruct the original source volume, unprovided source masks, source annotations, source coordinates, or source metadata.
> Do not reverse or estimate the preparation transforms to match test images against external copies of the source data.
> Do not use challenge-specific external images, annotations, derived measurements, manually recovered labels, or files outside the prepared public dataset.
> Do not infer targets from ID strings, hashes, path text, row order, regular expressions, file ordering, or other identifier tricks.
> Do not exploit the private test set through hand-labeling, leaderboard probing, repeated submissions, pseudo-labels derived from private feedback, or any other test-set leakage.
> Generic pretrained vision backbones are allowed, provided their use does not introduce challenge-specific external images or labels.
> Solutions must run within the platform's CPU and time limits.

Inspiration note: Useful because it uses visual evidence for structured state or risk prediction, not just ordinary image classification.

## BPT Ionisation Class from Broadband Imaging

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx706j6es28wh0z9smver9ccjh8ahdxa
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> BPT Ionisation Class from Broadband Imaging
> Overview
> A galaxy's optical spectrum can distinguish gas ionised by ordinary star formation
> from gas dominated by an active galactic nucleus or by low-ionisation nuclear
> emission. These regimes are defined by diagnostic emission-line ratios on BPT
> diagrams. Spectra are expensive to obtain, while broadband galaxy images are cheap
> and abundant.
> In this challenge, each case contains only a 64x64 three-band broadband image of a
> galaxy. The spectrum, coordinates, redshift, catalog identifiers, emission-line
> fluxes, and line ratios are hidden. The task is to predict one clean spectroscopic
> diagnostic BPT class:
> star_forming: line ratios are consistent with ionisation from star formation;
> composite: line ratios lie in the transition region where star formation and nuclear activity both contribute;
> seyfert_agn: the galaxy lies in the active/Seyfert part of the BPT diagrams;
> liner: the galaxy lies in the low-ionisation nuclear emission-line region.
> The target deliberately uses ratios between emission lines rather than whether a
> line is merely detected. Broadband colour and morphology correlate with the target,
> but they do not directly reveal the diagnostic ratios measured by spectroscopy.
> Target construction
> Labels are derived privately from the hidden SDSS spectrum. A case is eligible only
> when H-alpha, H-beta, [O III]5007, [N II]6584, and the combined [S II]6717+6731
> doublet all have positive flux and signal-to-noise ratio of at least 3.
> The diagnostic coordinates are:
> x_NII  = log10([N II]6584 / H-alpha)
> y_OIII = log10([O III]5007 / H-beta)
> x_SII  = log10(([S II]6717 + [S II]6731) / H-alpha)
> The standard NII-BPT Kauffmann and Kewley boundaries identify star_forming,
> composite, and active systems. Active systems are split into seyfert_agn and
> liner using the SII-BPT divider
> y_OIII = 1.89*x_SII + 0.76. Objects within 0.05 dex of a decision boundary are
> also excluded to avoid unstable labels caused by measurement noise.
> Evaluation
> Submissions are scored with macro-averaged F1 over the four fixed classes. For each
> class independently:
> F1_class = 2*TP / (2*TP + FP + FN)
> The final score is:
> macro_f1 = (F1_star_forming + F1_composite + F1_seyfert_agn + F1_liner) / 4
> Macro-F1 gives equal importance to all four diagnostic regions even though
> star-forming galaxies are more common. A solver therefore cannot score well by
> always predicting the majority class. Scores range from 0 to 1, and a perfect
> submission scores 1.
> Dataset
> Public files:
> train.csv: labeled training cases;
> test.csv: unlabeled test cases;
> sample_submission.csv: a valid submission example;
> task_manifest.json: class vocabulary, schema, and metric summary;
> images/: one PNG broadband cutout per case.
> Columns:
> id string): opaque case identifier;
> image string): relative path such as images/sdss_0a1b2c3d4e5f.png;
> ionisation_class string, train and submission only): exactly one of star_forming, composite, seyfert_agn, or liner.
> Galaxies from the same two-degree sky cell are assigned to the same split. Training
> and test therefore do not share local sky regions. Public images are independently
> flipped/rotated with a salted deterministic transform, and no source identifier or
> coordinate is exposed.
> Submission
> Submit a CSV with exactly these columns in this order:
> id,ionisation_class
> sdss_0a1b2c3d4e5f,star_forming
> sdss_112233445566,composite
> sdss_778899aabbcc,seyfert_agn
> sdss_aabbccddeeff,liner
> Every test id must appear exactly once. Class names are case-sensitive and must use
> the fixed vocabulary above.
> Appropriate approaches
> Train a compact four-class image classifier suitable for the CPU time limit.
> Use broadband colour, concentration, asymmetry, central brightness, and morphology as features, while remembering that none directly measures the BPT line ratios.
> Use class-balanced training or validation objectives because the physical class frequencies are unequal.
> Select hyperparameters using a sky-region-disjoint validation split and evaluate macro-F1 rather than accuracy.
> What must not be used
> Do not use external spectra, spectroscopic catalogs, BPT labels, line fluxes, or line-ratio measurements to recover test answers.
> Do not identify a source galaxy from its image in order to look up its spectrum.
> Do not recover coordinates, redshift, catalog identifiers, or private source rows.
> Train only on the public training data.

Inspiration note: Useful because it uses visual evidence for structured state or risk prediction, not just ordinary image classification.

## Historical Hand-Shadow Pose Plan Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a6cemhescw2ym9911xkq10d8a1gsv
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Plain language objective: infer the hand-and-arm arrangement that would cast a provided hand-shadow silhouette.
> Hand-shadow performers can make a rabbit, bird, camel, or character appear on a wall by arranging their hands between a small light and a screen. This challenge turns that visual inverse problem into a structured computer-vision task: recover the expert hand-and-arm ink mask implied by the target shadow.
> Each row contains a 128 x 128 target-shadow image. The answer is not a caption or object category. You must submit a structured pose-plan surrogate: a binary 128 x 128 mask of the historical hand/arm drawing in run-length encoding, a normalized bounding box for that hand ink, and a confidence value.
> This is not hand-shadow classification, captioning, or visible-hand segmentation. The hand is not visible in the test input. A valid answer must reconstruct a spatial hand-pose proxy from the target silhouette: where the palm/arm mass should sit, which parts of the outline require extended fingers or compact hand mass, and how much uncertainty remains. The mask, bounding box, and confidence should describe one consistent visual construction rather than three independent guesses.
> This is a CPU-only challenge. Solutions must run within 1.5 hours on 10 CPU cores and 62 GB RAM. Reasonable approaches include classical contour features, shape retrieval trained only on public train rows, lightweight image encoders, small autoencoders, and structured mask decoders. No GPU is required or assumed.
> Task
> For each test row, read the target-shadow image and predict these three outputs:
> hand_ink_rle: row-major RLE for a 128 x 128 binary hand/arm ink mask, where 1 means predicted hand/arm ink.
> hand_bbox_json: a normalized box around the predicted hand/arm ink with exactly x, y, w, and h.
> confidence: your calibrated estimate of how accurate the row prediction is.
> The central object is the mask. A strong submission should learn the visual relationship between shadow contours and hand construction from the public training pairs, then derive a compatible box and confidence from the predicted mask.
> Intended Approach And Validation
> A practical CPU solution is to decode the training hand_ink_rle masks, featurize each target shadow, and learn a compact shadow-to-hand-mask predictor. Good starting points include contour descriptors plus train-only retrieval, k-nearest template alignment, random forests or gradient-boosted patch features, small image-to-mask encoder-decoders, PCA/autoencoder mask models, and lightweight refinement of training hand-pose templates.
> Another reasonable route is a two-stage pipeline: first predict a coarse hand mask or hand-mask embedding from shadow shape, area, contour curvature, holes, endpoints, and aspect-ratio features; then postprocess the predicted mask with connected-component cleanup, derive the bounding box from that mask, and calibrate confidence on held-out training folds. This is still a visual modeling task: the target image gives the evidence, but its file path, row id, size, and prompt do not contain the answer.
> Use only the released public training labels for model selection. Make your own validation folds from train.csv, for example by grouping visually similar shadow footprints, aspect-ratio bins, or contour-complexity bins that you compute from the training images. Check both mask quality and downstream bbox/confidence behavior. Open-source local CV libraries, classical features, and generic offline vision backbones are allowed if they run under the CPU limit and do not use external hand-shadow plate lookup or hidden test information.
> What Not To Use / Do:
> Do not submit object captions, animal names, or generic class labels instead of the required hand-pose mask.
> Do not use external source lookup, original book filenames, page order, captions, or historical plate matching to recover held-out answers.
> Do not use metadata-only rules, row order, file size, mtime, prepared id, or filesystem side channels.
> Do not use hosted or closed-source APIs for training, inference, distillation, pseudo-labeling, or mask generation.
> Do not submit a generic segmentation model that ignores the target-shadow evidence and emits one fixed hand template.
> Do not reduce the task to one bounding box, one average mask, or one object-family decision; the spatial hand mask is required.
> Do not inspect private answer files, hidden platform state, grader internals, or filesystem artifacts outside the released public files.
> Do not use runtime internet access, source-image search, reverse image search, perceptual hashing against outside collections, or downloaded task-specific weights.
> Do not use malformed RLE/JSON, duplicate ids, extra columns, missing rows, NaN/inf values, or grader-probing attempts.
> Enforcement on invalid approaches: source-lookup solutions, metadata-only predictors, fixed-template submissions, caption-only methods, hosted-API approaches, and submissions that do not attempt the required hand-mask reconstruction may be rejected before payout regardless of leaderboard score.
> Evaluation
> Each row receives a score in [0, 1]. Higher is better.
> The binary mask head combines exact and tolerant shape agreement:
> IoU      = intersection / union
> Dice     = 2 * intersection / (pred_pixels + true_pixels)
> TolF1    = F1 after radius-2 binary dilation
> S_mask   = 0.34*IoU + 0.38*Dice + 0.28*TolF1
> The bounding-box head compares normalized x, y, w, and h:
> S_bbox = exp(-L1_bbox_error / 0.55)
> core   = 0.72*S_mask + 0.18*S_bbox
> calib  = 1 - abs(confidence - core / 0.90)
> row    = core + 0.10*calib
> The final score blends mean row quality with worst hidden subgroup quality:
> raw_final = 0.78*mean(row)
> + 0.12*worst_object_family(row)
> + 0.10*worst_shadow_footprint(row)
> Final = raw_final ** 1.45
> The hidden subgroup labels are private metadata and are not columns in train.csv or test.csv. The theoretical minimum is 0.0 and the theoretical maximum is 1.0. Perfect labels with confidence 1.0 score exactly 1.0.
> Worst subgroup means the lowest subgroup mean across the private group buckets used by the grader.
> The grader returns 0.0 for missing, extra, or reordered submission columns; duplicate ids; missing or extra ids; row-set mismatch; invalid id values; NaN/inf confidence; confidence outside [0,1]; or invalid answer files. Malformed or overlong row-local RLE/JSON receives zero credit for the affected row without leaking private labels.
> Dataset
> The prepared dataset ships as a public/ directory with train/test CSV files, target-shadow PNG images, and a sample submission template. Images are 128 x 128 grayscale PNGs derived from historical hand-shadow instruction plates. Public ids and paths are opaque and do not expose original source filenames, captions, or page order.
> sample_submission.csv is a weak placeholder template with the required submission columns and test ids.
> Item	Description
> train/shadows/*.png	Train shadows
> test/shadows/*.png	Test shadows
> train.csv	Inputs plus labels
> test.csv	Inputs only
> sample_submission.csv	Weak template
> train.csv columns
> The train-only label columns are hand_ink_rle and hand_bbox_json. The train input columns are id, target_shadow_path, canvas_size, and prompt.
> Column	Type	Description
> id	int	Unique row id
> target_shadow_path	string	PNG path
> canvas_size	int	Always 128
> prompt	string	Task instruction
> hand_ink_rle	string	Target mask RLE
> hand_bbox_json	string	Target bbox JSON
> test.csv columns
> The test input columns are id, target_shadow_path, canvas_size, and prompt. Test rows do not include hand_ink_rle or hand_bbox_json.
> Column	Type	Description
> id	int	Unique row id
> target_shadow_path	string	PNG path
> canvas_size	int	Always 128
> prompt	string	Task instruction
> The RLE is row-major over the 128 x 128 mask. Runs are written as start:length pairs separated by spaces, using zero-based flattened pixel indices. An empty string represents an all-zero mask.
> Submission
> Write your prediction file to ./working/submission.csv. Submit a CSV with exactly these four columns in this order: id, hand_ink_rle, hand_bbox_json, confidence.
> Column	Type	Constraint
> id	int	Same ids as test
> hand_ink_rle	string	RLE, max length
> hand_bbox_json	string	x/y/w/h JSON
> confidence	float	In [0,1]
> Train-only label columns are hand_ink_rle and hand_bbox_json. Test input columns are id, target_shadow_path, canvas_size, and prompt. hand_bbox_json must be a JSON object with exactly the keys x, y, w, and h, such as {"x":0.12,"y":0.08,"w":0.64,"h":0.77}. Values must be finite and normalized. x and y must be at least 0, w and h must be positive, all four values must be at most 1, and the box may not extend outside the canvas.
> Example rows in the same placeholder style as sample_submission.csv:
> id,hand_ink_rle,hand_bbox_json,confidence
> 101,"24:5 151:7 278:9","{""x"":0.08,""y"":0.02,""w"":0.76,""h"":0.91}",0.28
> 102,"31:4 158:6 285:8","{""x"":0.10,""y"":0.04,""w"":0.72,""h"":0.88}",0.28
> 103,"","{""x"":0.20,""y"":0.20,""w"":0.60,""h"":0.60}",0.10

Inspiration note: Useful because it uses visual evidence for structured state or risk prediction, not just ordinary image classification.

## Vegetation Transition Assessment From Camera Panels

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx785q0f7tffwdydrgbxhk9bh98a0neh
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Plain language objective: from a short sequence of real vegetation camera views, decide what vegetation transition the ecosystem is about to enter next, and report how confident that decision is.
> This is a CPU-only Computer Vision challenge. Each row contains a 384 x 192 JPEG panel made from four chronological vegetation-camera crops, plus compact greenness context from the same observation period. The camera panel is the primary input: useful solutions should read canopy color, texture, snow/cloud, brightness, and seasonal appearance cues from the images, then use the greenness trace as supporting context.
> For every test row, submit three prediction fields:
> transition_band: one of green_up, peak_or_stable_green, senescence, or dormant_or_no_change.
> confidence: a finite float in [0,1] for the submitted transition band.
> evidence_json: a compact JSON object with expected_direction, trend_bin, and uncertainty.
> The evidence fields must use these values: expected_direction is one of rising, stable, or falling; trend_bin is one of strong_rise, weak_rise, stable, weak_fall, or strong_fall; uncertainty is one of low, medium, or high.
> This is not a phenology-date regression task and not a lookup exercise. The public rows remove source site names, exact dates, source filenames, camera IDs, URLs, and raw row positions. The maximum solution time is 1.5 hours on 10 CPU cores and 62 GB RAM. GPU training, hosted vision APIs, closed-source teacher APIs, external source lookup, network downloads, and runtime-downloaded pretrained weights are not allowed.
> What Not To Use / What Not To Do (violation may cause rejection regardless of score):
> Do not reverse-map public panels or traces to original source site names, camera IDs, timestamps, URLs, filenames, source CSV rows, or future observations.
> Do not use external PhenoCam archives, gallery pages, APIs, thumbnails, ROI CSV products, raw JPEGs, or image retrieval at inference time to recover hidden future data.
> Do not use row order, file size, JPEG metadata, modification time, image hashes, salted IDs, path strings, or fold-group values as answer channels.
> Do not reduce the task to a site-season calendar prior, a lookup table, a phenology-date regression benchmark, or a metadata-only predictor that ignores the released panel and trace evidence.
> Do not download model weights, feature extractors, embeddings, datasets, or helper code at runtime; any pretrained backbone must already be available in the base runtime and must be generic, local, and non-PhenoCam-specific.
> Do not inspect private answers, grader internals, hidden platform state, or side channels.
> Do not submit malformed JSON floods, duplicate IDs, extra columns, non-finite values, or other grader exploits.
> Enforcement on invalid approaches: solutions may be reviewed for actual use of the released images and traces, source-lookup code, external calls, and metadata-only behavior. Source retrieval, hosted APIs, hidden-answer access, or submissions that avoid the required camera-evidence contract may be rejected before payout.
> Task
> For each test row, read the panel image and recent greenness trace, then output the next-transition record. A strong submission should combine visual canopy color and texture cues with recent greenness direction and uncertainty. The trace alone is intentionally partial, and the panel alone does not show the hidden future window.
> Use training-only validation folds grouped by fold_group so nearby windows from the same anonymized camera season do not appear on both sides of validation. A fixed template, metadata-only model, or calendar-prior solution should remain weak; useful submissions need to learn from the released visual and greenness evidence.
> Intended Approach and Validation
> A practical CPU solution is image-first: extract color, texture, brightness, snow/cloud, and seasonal appearance features from the panel image, parse trace_json and trace_summary_json into recent level/range/slope context, and train a calibrated structured predictor or compact ensemble for the transition and evidence fields.
> Reasonable CPU methods include random forests, gradient-boosted trees, logistic models over engineered evidence, shallow CPU CNNs, frozen local vision features, and small image-plus-trace ensembles. Open-source local computer-vision libraries and generic pretrained vision features are allowed only when they are already present in the base runtime, run within the CPU limit, and do not use external PhenoCam source data, site pages, hosted APIs, runtime downloads, or hidden test information.
> Calibrate confidence on training-only validation folds. Check performance by transition band, vegetation type, and uncertainty so the model does not only work on the most common vegetation state.
> Dataset
> The public files contain prepared JPEG panel images and CSV metadata with opaque salted IDs. The private split holds out entire source ROI/site groups, and related camera-season groups stay together, so useful models need to generalize from labelled training evidence to unseen anonymized ecosystems rather than memorizing nearby frames, repeat site calendars, or camera-specific seasonal patterns.
> File overview
> Item	Description
> train.csv	Inputs and targets
> test.csv	Test inputs only
> sample_submission.csv	Weak valid template
> train/images/*.jpg	Train panels
> test/images/*.jpg	Test panels
> train.csv columns
> Column	Type	Description
> id	string	Opaque row id
> image_path	string	JPEG panel path
> trace_json	string	Recent GCC trace
> trace_summary_json	string	Trace summary
> fold_group	string	Fold group
> vegetation_type	string	ROI veg code
> transition_band	string	Train target
> expected_direction	string	Direction target
> trend_bin	string	Trend target
> uncertainty	string	Uncertainty target
> test.csv columns
> Column	Type	Description
> id	string	Opaque row id
> image_path	string	JPEG panel path
> trace_json	string	Recent GCC trace
> trace_summary_json	string	Trace summary
> fold_group	string	Fold group
> vegetation_type	string	ROI veg code
> image_path is a public-relative path to a 384 x 192 JPEG panel. The top row contains four 96 x 72 vegetation-camera crops in chronological order from left to right; the lower part is blank layout space and does not contain hidden text. Source filenames and timestamps are not exposed.
> trace_json is a JSON array of exactly eight objects. Each object has exactly d and gcc_delta. The d values are -21, -18, -15, -12, -9, -6, -3, and 0, in three-day steps relative to the latest public trace point. gcc_delta is a rounded relative GCC change from the first trace point, clipped to [-0.30,0.30] and rounded to 0.01.
> trace_summary_json is a JSON object with exactly recent_slope, recent_range, and level_bin. recent_slope is the recent four-point GCC change divided by a local scale and rounded to 0.01. recent_range is the eight-point GCC range divided by the same local scale and rounded to 0.01. level_bin is one of low, mid, or high.
> fold_group is an anonymized ROI-year group for validation. Rows with the same fold_group should stay together in local validation; it is not a stable site or camera identity. vegetation_type is one of AG, DB, EN, GR, or SH.
> The train-only target columns have these allowed values:
> transition_band: green_up, peak_or_stable_green, senescence, dormant_or_no_change.
> expected_direction: rising, stable, falling.
> trend_bin: strong_rise, weak_rise, stable, weak_fall, strong_fall.
> uncertainty: low, medium, high.
> The same four target columns are absent from test.csv.
> Evaluation
> Submissions are scored by Mean Future Transition Evidence Utility. Each row combines transition-band utility, evidence-head correctness, and confidence honesty.
> The row score is:
> band_score = 1.0 for an exact transition_band match
> band_score = asymmetric partial credit in [0,0.28] for near misses
> evidence_score = 0.16*direction_exact
> + 0.12*trend_bin_exact
> + 0.06*uncertainty_exact
> confidence_score = confidence if transition_band is correct
> confidence_score = 1 - confidence otherwise
> row_score = (0.62*band_score + evidence_score + 0.04*confidence_score) ** 3.00
> The transition-band partial-credit table is asymmetric:
> True band	Submitted band	Utility
> green_up	peak_or_stable_green	0.18
> green_up	dormant_or_no_change	0.04
> green_up	senescence	0.00
> peak_or_stable_green	green_up	0.28
> peak_or_stable_green	dormant_or_no_change	0.18
> peak_or_stable_green	senescence	0.06
> senescence	peak_or_stable_green	0.08
> senescence	dormant_or_no_change	0.18
> senescence	green_up	0.00
> dormant_or_no_change	peak_or_stable_green	0.25
> dormant_or_no_change	green_up	0.12
> dormant_or_no_change	senescence	0.12
> The final score is:
> Final = 0.50*macro_transition
> + 0.20*mean(row_score)
> + 0.15*worst_transition_band
> + 0.10*worst_vegetation_type
> + 0.05*worst_uncertainty
> macro_transition is the unweighted mean of row scores within the four true transition bands, so a constant-band submission cannot score well just by matching a frequent band. Higher is better. The theoretical minimum is 0.0 and the maximum is 1.0. A perfect submission scores exactly 1.0.
> The grader requires exactly the listed columns in the listed order, one row per test ID, unique IDs, the exact test ID set, finite confidence in [0,1], and valid transition-band strings. A structural failure returns 0.0. Malformed or over-long row-local evidence_json scores zero for that row and does not crash the grader.
> Submission
> Write the final submission CSV to exactly ./working/submission.csv. It must contain exactly these four columns in this order and exactly one row for every test ID.
> Column	Type	Constraint
> id	string	Same set as test
> transition_band	string	See allowed bands
> confidence	float	In [0,1]
> evidence_json	string	Strict JSON object
> The four allowed transition_band values are green_up, peak_or_stable_green, senescence, and dormant_or_no_change.
> evidence_json must be a JSON object with exactly expected_direction, trend_bin, and uncertainty. expected_direction must be one of rising, stable, or falling. trend_bin must be one of strong_rise, weak_rise, stable, weak_fall, or strong_fall. uncertainty must be one of low, medium, or high.
> Example formatting:
> id,transition_band,confidence,evidence_json
> pct_a1b2c3d4e5f60718,green_up,0.72,"{""expected_direction"":""rising"",""trend_bin"":""weak_rise"",""uncertainty"":""medium""}"
> pct_fedcba9876543210,senescence,0.66,"{""expected_direction"":""falling"",""trend_bin"":""strong_fall"",""uncertainty"":""low""}"
> pct_0011223344556677,peak_or_stable_green,0.58,"{""expected_direction"":""stable"",""trend_bin"":""stable"",""uncertainty"":""high""}"
> Requirements are strict: the submitted IDs must exactly match the test IDs, column order must match the table, duplicate or missing IDs are invalid, confidence must be finite and in [0,1], transition bands must use the allowed enum values, and evidence JSON strings must be compact and valid.

Inspiration note: Useful because it uses visual evidence for structured state or risk prediction, not just ordinary image classification.

## Sketch Stroke Draw Order Prediction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7d92v03jfpw5x1epa701skex8ah9wa
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Beat mailliwa's score of 0.705!

Full challenge description from page:

> Background
> You are given a large collection of simple freehand sketches. Each sketch was drawn by a person one pen stroke at a time, and the sequence in which the strokes were laid down was recorded. That draw order has been removed: for each sketch the individual strokes are shown to you in a scrambled order, each as its own small image. Your job is to recover the order in which the strokes were originally drawn — which stroke came first, second, and so on.
> People do not draw randomly: they tend to lay down large outlines and containing shapes before small interior details, and there are consistent habits in how a shape is built up. A model can learn these ordering regularities from the training sketches and apply them to unseen ones. The order is genuinely ambiguous for many sketches, so the goal is to rank the strokes as close to the true draw order as possible, not to be perfect.
> The sketches in the test set come from object types that do not appear in training, so a solution must learn a general ordering prior rather than memorizing the habits of any particular kind of drawing.
> Data
> All files are in the challenge directory. There is one row per stroke (a sketch with n_strokes strokes contributes n_strokes rows).
> train.csv
> One row per stroke of each training sketch, with the answer.
> id (string) — unique row id, formatted <drawing_id>_s<stroke_index>.
> drawing_id (string) — id of the sketch this stroke belongs to; strokes of the same sketch share it.
> stroke_index (integer) — the stroke's position in the scrambled presentation order, 0 … n_strokes-1. This is NOT the draw order.
> n_strokes (integer) — number of strokes in this sketch (4–10).
> image (string) — relative path to this stroke's image, e.g. train/<id>.png.
> draw_order (integer) — the label: the stroke's true position in the drawing sequence, 0 … n_strokes-1, where 0 was drawn first.
> test.csv
> Same columns as train.csv except draw_order (which is withheld): id, drawing_id, stroke_index, n_strokes, image (path test/<id>.png).
> sample_submission.csv
> A valid baseline submission you can overwrite.
> id (string) — every test row id, matching test.csv exactly.
> order_score (float) — a predicted ordering value (all 0.0 in the sample).
> train/ and test/ image folders
> One PNG per stroke, named <id>.png, size 40×40 RGB:
> Red channel — the single stroke for this row.
> Green channel — all the other strokes of the same sketch (context, so you can see where this stroke sits within the whole drawing).
> Blue channel — unused (zero).
> No stroke coordinates, timings, or object labels are provided; everything you need is in the images.
> Task and submission format
> For every row in test.csv, predict order_score — a real number giving the stroke's estimated place in the draw sequence, where a lower order_score means drawn earlier. Within each sketch, the strokes are ranked by their order_score (ascending) to form your predicted draw order; only the relative ordering within a sketch matters, not the absolute values.
> Submit a CSV with exactly these columns:
> id — every test row id, exactly the set in test.csv (no missing, extra, or duplicate ids).
> order_score — a finite number for each id.
> Evaluation metric
> Submissions are scored by mean pairwise stroke-order accuracy. For each sketch, consider every unordered pair of its strokes. A pair is scored:
> 1 if your order_score ranks the two strokes in the same order as the true draw order,
> 0 if it ranks them in the opposite order,
> 0.5 if you give the two strokes equal order_score.
> The sketch's score is the average over its pairs; the final score is the mean over all sketches. Random ordering scores about 0.5; a perfect ordering scores 1.0. Higher is better.
> Rules — how a solution must be produced
> This challenge tests whether a model can learn stroke-ordering regularities. Your predictions must be produced by a model or estimator fit on the provided training data and applied to the test images.
> The following are not allowed and will fail the challenge's method rubrics even if they raise the numeric score:
> Using any external dataset or any model pre-trained on outside sketch data.
> Identifying, retrieving, or matching the sketches (or their strokes) against any outside collection, and reading an order off a matched record.
> Recovering the answer by fingerprinting, hashing, or looking up the source of an image rather than predicting from a learned model.
> Hand-coded ordering rules that are not learned from the training data.

Inspiration note: Useful because it uses visual evidence for structured state or risk prediction, not just ordinary image classification.

## CT Tree-Core Crossdating And Ring Evidence Ledger

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7b4371b9knbzgvs01jvbgssh8arenq
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Plain language objective: for each anonymized tree-core segment, locate every annual ring visible in a real CT strip and assign the correct calendar year to each ring using the aligned wood-density trace and the provided dated reference chronology.
> Each public row contains two aligned inputs. The ct_image file is a cropped grayscale CT strip rendered at 2048 x 96 pixels. The density_npz file contains a length-2048 float32 density trace aligned to the same x-axis. The public reference_chronology.csv is a dated master chronology built from training-side trees only; it does not include hidden test-tree labels. Train rows include the ring ledger so participants can learn ring-boundary appearance, density cues, and chronology alignment behavior.
> For every test row, predict two fields:
> Output	What it represents
> rings_json	Ordered annual ring intervals with exact calendar years
> confidence	Row confidence in [0,1]
> rings_json is an ordered JSON list of annual ring objects. Each object must have row-local pixel coordinates left and right, plus the integer calendar year. confidence is a calibrated row-level probability in [0, 1] that the submitted joint ring/year ledger is correct.
> The output is intentionally a joint evidence ledger, not separate decorative heads. A correct answer must recover both the spatial ring interval and the exact calendar year sequence. Segment start and end years are dependent summaries and are not separate submission columns.
> Only CPU-based challenges are allowed. A complete solution must run in at most 1.5 hours. Runtime machine: 10 CPU cores and 62 GB RAM. Novelty score must be at least 6. Do not submit a tabular or regression challenge. The challenge must be creative, meaningful, and based on real-world data.
> Task
> Build a crossdating pipeline for unseen CT tree-core fragments. Your method should detect the annual ring intervals supported by the CT image and density trace, then align the recovered ring-width sequence to the dated reference chronology. The final ledger should contain one object per annual ring, in left-to-right order, with exact calendar years increasing by one year per ring.
> Intended Approach
> Strong CPU-only solutions will likely combine:
> CT texture or edge features for boundary proposals.
> Density-trace filtering for latewood/earlywood transitions and local ring evidence.
> A compact learned or classical boundary detector trained on public train rows.
> Dynamic programming, correlation, or probabilistic alignment against the train-only reference chronology.
> Calibration from train/validation folds grouped by source tree.
> Appropriate offline tools include NumPy, SciPy, scikit-image, OpenCV, scikit-learn, PyTorch CPU, compact 1D CNN/TCN models, and classical signal-processing libraries. Use only the released training labels for model selection; validation should be built from training rows in a way that tests generalization across tree groups and year ranges. GPU-only training or hosted inference is not appropriate for the official run.
> What Not To Do
> Using any of the approaches below is grounds for rejection on review, regardless of leaderboard score.
> Do not use original source filenames, source archive paths, source tree/core ids, crop offsets, original image sizes, collection years, file ordering, checksums, or online source lookup to reconstruct answers.
> Do not hardcode public row ids, private split behavior, or any answer ledger.
> Do not use the raw official files directly at solution time unless they are part of the public challenge data made available to all participants.
> Do not use external APIs, hosted LLMs, hosted vision models, hosted OCR, or remote inference services.
> Do not train or infer from non-public challenge labels or private files.
> Do not reduce the task to plain ring segmentation without years, plain chronology alignment without spatial evidence, classification, scalar regression, or start/end-year prediction alone.
> Do not invent missing-ring, false-ring, ambiguous, unknown, or quality labels. The official audited source has no zero-valued absent-ring measurements, and this challenge does not ask for those labels.
> Do not submit malformed JSON, unordered rings, nonconsecutive years, impossible intervals, out-of-range pixel positions, missing rows, duplicate ids, extra ids, or invalid confidences as a format hack.
> Enforcement on invalid approaches: submissions that score by lookup, metadata reconstruction, private-file access, external hosted models, or rule-only shortcuts that ignore the joint boundary-plus-year task may be rejected even if the CSV passes the grader.
> Evaluation
> The primary metric is Robust Joint Ring-Year Ledger Score. Higher is better. Theoretical minimum is 0.0; theoretical maximum is 1.0.
> For a row, let P be the predicted ring list and T the true ring list. A predicted ring can earn full central credit only when its year exactly equals a true ring's year and its left and right boundaries are close to that same true ring.
> Position tolerance is 10 pixels. For one matched predicted/true interval:
> left_score     = max(0, 1 - abs(pred_left - true_left) / 10)
> right_score    = max(0, 1 - abs(pred_right - true_right) / 10)
> interval_score = 0.5 * (left_score + right_score)
> The central joint score is:
> joint_event_score = sum(interval_score for exact-year matches) / max(len(P), len(T))
> Extra rings, missing rings, or wrong calendar years reduce the denominator-normalized score. Because test ledgers contain consecutive annual rings and no missing-ring labels, submitted years must be strictly consecutive in the submitted order.
> A light boundary-only auxiliary score gives partial credit for spatial ring recovery even when the years are wrong. It greedily matches predicted and true intervals by descending interval_score, ignoring year, with each predicted and true ring used at most once:
> boundary_only_score = sum(greedy_interval_scores) / max(len(P), len(T))
> Per-row correctness:
> correctness = 0.90 * joint_event_score
> + 0.10 * boundary_only_score
> Confidence is scored only as calibration on earned task credit:
> confidence_score = correctness * max(0, 1 - abs(confidence - joint_event_score))
> row_score        = 0.94 * correctness + 0.06 * confidence_score
> The final leaderboard score blends the mean row score with a private worst-subgroup term:
> Final = 0.85 * mean(row_score)
> + 0.15 * lowest subgroup mean
> The lowest subgroup mean is computed across private subgroup axes for cohort, ring-count regime, and mean-ring-width regime. Every scored subgroup has at least 30 test examples in the checked preparation run. The subgroup term is included so solutions must work across old/young cores, different fragment lengths, and different ring-width regimes rather than only on easy rows.
> The grader raises InvalidSubmissionError for global structural submission errors: wrong or reordered columns, missing ids, extra ids, duplicate ids, missing confidence, non-finite confidence, or confidence outside [0, 1]. Row-local malformed ring JSON, overlong ring JSON, non-list JSON, impossible intervals, unordered rings, nonconsecutive years, invalid years, NaN/Inf positions, or out-of-range positions set that row's score to 0.0 without leaking labels or crashing.
> Dataset
> The public data contains transformed row-local real CT segments only. It does not expose original filenames, source archive paths, physical tree/core ids, crop offsets, original strip sizes, source order, collection years, hidden split metadata, or private answer metadata. All test CT images are 2048 x 96; all density traces have length 2048.
> The checked prepared split contains:
> Train episodes: 435
> Test episodes: 126
> Public prepared size: about 52.0 MB
> Private answer size: about 0.3 MB
> Test physical tree groups: 24
> Train/test tree-group overlap: 0
> File overview
> Item	Description
> public/reference_chronology.csv	Train-tree-only dated reference chronology
> public/train/images/*.jpg	Train CT strip crops
> public/test/images/*.jpg	Test CT strip crops
> public/train/signals/*.npz	Train aligned density traces
> public/test/signals/*.npz	Test aligned density traces
> public/train.csv	Inputs plus train labels
> public/test.csv	Inputs only
> public/sample_submission.csv	Valid weak submission template
> reference_chronology.csv columns
> Column	Type	Description
> year	int	Calendar year
> ring_width_index	float	Mean width index
> sample_depth	int	Train sample count
> ring_width_index_std	float	Train std dev
> ring_width_index is the train-tree normalized ring-width chronology for that calendar year. sample_depth and ring_width_index_std describe how much training-side support went into that reference value.
> train.csv columns
> Column	Type	Description
> id	string	Opaque anonymized segment id
> ct_image	string	Relative path to the grayscale CT crop
> density_npz	string	Relative path to aligned density array
> prompt	string	Constant task prompt
> rings_json	string	Train-only label ledger
> start_year	int	Dependent summary of first ring year
> end_year	int	Dependent summary of last ring year
> ring_count	int	Dependent summary of ledger length
> test.csv columns
> Column	Type	Description
> id	string	Opaque anonymized segment id
> ct_image	string	Relative path to the grayscale CT crop
> density_npz	string	Relative path to aligned density array
> prompt	string	Constant task prompt
> density_npz contents
> Each .npz file contains:
> Array	Shape	Description
> density	(2048,)	Robust-normalized aligned density trace
> x	(2048,)	Row-local x coordinates
> Submission
> Write the final submission CSV to exactly ./working/submission.csv. It must contain exactly these columns in this order: id, rings_json, and confidence.
> Column	Type	Constraint
> id	string	Same set as test
> rings_json	JSON	Ordered ring list
> confidence	float	In [0,1]
> rings_json must be a JSON list of objects:
> [{"left": 103.25, "right": 139.74, "year": 1907},
> {"left": 139.74, "right": 178.02, "year": 1908}]
> Rules:
> Include exactly one row per test id.
> Do not include train ids.
> Keep rings sorted from left to right.
> Use finite left and right values in [0, 2047].
> Require right > left for every ring.
> Use integer years, strictly increasing by one year per ring.
> Use confidence in [0, 1].
> sample_submission.csv
> The supplied sample is valid but weak. It uses a crude fixed-count density heuristic and is intended only to show formatting.
> CPU And Runtime
> The challenge is designed for CPU-only methods. A complete solution must run in at most 1.5 hours on 10 CPU cores and 62 GB RAM. The prepared public data is small enough for in-memory feature extraction, and the baselines shipped with the challenge are deterministic CPU-only Python/Numpy/Pillow code.
> Source And Attribution
> The hidden raw dataset is built from official CC BY 4.0 CT-scanned increment-core files. Public challenge rows are anonymized, fixed-size, row-local transformations of real official source evidence. Cite the dataset creators in solutions or derived work according to the dataset license.

Inspiration note: Useful because it uses visual evidence for structured state or risk prediction, not just ordinary image classification.

## Matching a Surface's Relief to its Appearance

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f3hn8w70vbz9dh18c6jxe9h8aq85x
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Beat samay_raina's score of 0.464!

Full challenge description from page:

> Matching a Surface's Relief to its Appearance
> Overview
> Every real surface has two faces. There is how it looks — its colour, its markings, the
> stains and grain and mortar of it. And there is how it is shaped — the fine relief of
> bumps, grooves and ridges that you would feel by running a hand across it. The two are
> related, because the same physical process made both: bricks are laid, wood grows rings,
> rust eats pits. But they are not the same thing, and neither one dictates the other.
> Each row of this challenge gives you a small colour patch of one surface, and six
> relief patches. Exactly one of the six is the relief of that same surface. The other five
> belong to different surfaces that happen to look broadly similar. Identify which candidate
> belongs to the query.
> The catch is that the colour patch and the true relief patch are taken from different,
> non-overlapping regions of the surface. They are not the same square of material
> photographed twice — so nothing lines up, and no edge in the colour patch has a matching
> groove in the relief patch. What connects them is only the character of the surface: the
> scale of its structure, how regular it is, how it is roughened. That is a real signal, and
> it is a weak one.
> You are given 3,522 training rows (each labelled with the correct candidate) and must
> identify the matching candidate for each of the 2,886 test rows.
> Data provenance
> The surfaces come from a public-domain (CC0) library of photographed surface materials,
> each supplied with a map of its colour and a map of its relief. Patches are resampled and
> independently flipped and rotated, so a published patch is not a verbatim crop of any
> source file. The dataset is released for unrestricted use, including commercial.
> Encoding
> Input (one row)
> **query** — a 32 × 32 × 3 uint8 colour patch of a surface.
> **candidates** — a 6 × 32 × 32 × 3 uint8 stack of relief patches. Exactly one is the
> relief of the query's surface, taken from a different region of it. The correct index is
> uniformly distributed over 0 … 5.
> A relief patch encodes the surface's local shape as a colour image: the three channels
> carry the direction the surface faces at each pixel, so flat areas share one colour and
> bumps, ridges and grooves show as deviations from it.
> Target
> The index of the matching candidate — a single integer 0 … 5.
> Dataset
> Arrays are in NumPy .npz format.
> **train.npz** — 3,522 training rows. Keys:
> ids — (3522,) int64 row identifiers, 0 … 3521.
> query — (3522, 32, 32, 3) uint8.
> candidates — (3522, 6, 32, 32, 3) uint8.
> target_str — (3522,) string, the index of the matching candidate.
> **test.npz** — 2,886 rows to label. Keys: ids (int64, 3522 … 6407),
> query, candidates. The matching index is withheld.
> IDs are globally unique across the dataset: test ids continue exactly where the
> training ids end.
> **sample_submission.csv** — a correctly-formatted example submission.
> No surface is shared between train and test. Every surface in the dataset contributes
> its rows to one side of the split only, so the test surfaces are ones you have never seen
> labelled.
> Evaluation
> Accuracy — the fraction of test rows whose matching candidate is identified exactly
> (higher is better, range 0–1). The final score is the mean over all 2,886 test rows.
> Always guessing one index scores about 0.17.
> Worked example
> Matching candidate: 3. You predict 3 → correct (contributes 1). You predict 0 → wrong
> (contributes 0).
> Submission format
> Submit submission.csv with exactly two columns and one row per test id
> (2,886 rows plus a header):
> id (int) — the test id from test.npz.
> prediction (int) — the index of the matching candidate, a single integer 0 … 5.
> Example:
> id,prediction
> 3522,3
> 3523,0
> 3524,5
> Every id in test.npz must appear exactly once. The grader rejects predictions outside
> 0 … 5, empty predictions, duplicate ids, and missing/extra ids.
> What not to use
> No external data. Train only on train.npz — do not fetch external material or
> texture libraries to match patches against.
> No test labels. The matching indices are withheld — produce predictions purely from
> the test inputs and a model learned on the training data.
> Reproducible inference. Fixed seeds, deterministic decoding — re-running on
> test.npz must reproduce the same submission.csv.

Inspiration note: Useful because it uses visual evidence for structured state or risk prediction, not just ordinary image classification.

## Episodic Retinal Predicate Induction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71256k48mnaw718qyz3bcx0d8aghg7
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> 1. Overview
> The objective is to infer a hidden visual predicate from a small set of labeled retinal-image pairs and then estimate the probability that each unlabeled query pair satisfies that predicate.
> The dataset is divided into independent episodes.
> Each episode contains:
> A support set of ordered ocular-image pairs with binary labels.
> A query set of ordered ocular-image pairs whose labels must be predicted.
> One hidden predicate that is shared by all rows in that episode.
> The meaning of label 1 is created locally by the support set.
> It is not tied to one permanent disease, finding, similarity measure, or diagnostic category.
> Instead, each episode defines a temporary piece of visual logic. The support examples demonstrate how retinal evidence from the left and right images must interact for a pair to be considered positive.
> A hidden predicate may require the two images to:
> Share a particular evidence pattern.
> Differ with respect to a particular pattern.
> Place relevant evidence on a specified side.
> Contain evidence on exactly one side.
> Satisfy different requirements on the left and right.
> Share one property while differing on another.
> Satisfy an overlap, difference, or cardinality condition.
> Jointly satisfy several visual conditions.
> Participants are not given the predicate as text, code, a formula, a clinical label, or a reusable class identifier.
> The predicate must be reconstructed from the labeled demonstrations inside the episode.
> The same ordered image pair could therefore receive different labels in different episodes because its interpretation depends on the temporary predicate currently in force.
> For every query row in test.csv, participants submit:
> P(label = 1 | support set, left image, right image)
> This is not ordinary image classification.
> It is not ordinary image matching.
> It is not simply few-shot recognition of a hidden class.
> The central task is to induce an episode-local visual predicate and execute it on new ordered image pairs.
> 2. What Distinguishes the Benchmark
> Most medical-image benchmarks assume that the meaning of every output is fixed before inference begins.
> A model may be asked whether an image contains a known condition, whether two images are similar, or whether a predefined clinical change has occurred.
> This benchmark removes that fixed semantic layer.
> The model is not told what visual concept to predict.
> It must infer both:
> Which retinal evidence matters in the current episode.
> What logical relationship between the two images defines a positive pair.
> The support set therefore functions as a temporary visual specification.
> A successful system must convert that specification into an executable decision rule.
> The benchmark combines several forms of generalization in one task:
> New images.
> New ordered pairs.
> New combinations of retinal evidence.
> New bindings between visual factors and logical operators.
> New multi-part predicates.
> New episode-specific meanings of the positive label.
> The key generalization target is not merely a new class.
> It is a new visual decision procedure assembled from previously encountered evidence and relation patterns.
> 3. Prediction Objective
> For every query pair in test.csv, predict:
> probability = P(label = 1 | episode support rows, left image, right image)
> Predictions must be finite numeric values in:
> [0, 1]
> The hidden predicate remains constant within one episode and changes between episodes.
> Participants must not assign a universal interpretation to label 1.
> A high probability should indicate that the query pair satisfies the predicate demonstrated by the support rows of its own episode.
> 4. Research Objective
> The benchmark evaluates whether a model can perform support-conditioned visual program induction.
> A successful system must combine four capabilities:
> Preserve reusable retinal evidence in its image representation.
> Identify which evidence dimensions are relevant in the current episode.
> Recover the logical relationship demonstrated by the support pairs.
> Apply that relationship consistently to unseen query pairs.
> The benchmark studies:
> Episode-local semantics.
> Visual predicate induction.
> Ordered relation reasoning.
> Temporary label construction.
> Latent evidence decomposition.
> Support-conditioned decision making.
> Counterexample-guided rule elimination.
> Compositional generalization.
> Factor-operator rebinding.
> Probability calibration under rule uncertainty.
> Strong performance cannot be achieved by detecting only whether an image appears normal or abnormal.
> Positive and negative pairs may both contain visible retinal findings.
> The distinction may depend on:
> Which evidence appears in both images.
> Which evidence appears in only one image.
> Which evidence differs between the two sides.
> Whether a pattern is located on the left or right.
> Whether two side-specific conditions hold simultaneously.
> Whether one condition holds while another does not.
> Whether the evidence sets satisfy a particular structural relationship.
> The task therefore requires a model to reason over the internal composition of each image and the relation between the two images.
> 5. Internal Evidence Representation
> During benchmark construction, each image is associated with an internal set of latent visual atoms.
> Conceptually:
> Z(I) = the set of latent visual atoms present in image I
> A latent atom represents a recurring retinal evidence pattern.
> These atoms are construction variables rather than participant-facing targets.
> They are not exposed as:
> Disease labels.
> Diagnostic names.
> Submission columns.
> Episode identifiers.
> Public metadata.
> The internal atom vocabulary is created by:
> Retaining findings with sufficient statistical support.
> Excluding findings that cannot support reliable episode generation.
> Removing participant-facing clinical names.
> Removing original annotation identifiers.
> Eliminating duplicate annotation patterns.
> Verifying the availability of positive, negative, and co-occurring examples.
> Ensuring that retained atoms can participate in several predicate families.
> Participants are not asked to predict the atoms directly.
> The atoms are used internally to construct hidden episode predicates.
> A model may benefit from learning an image representation that preserves multiple independent evidence factors, but evaluation measures only query-pair probabilities.
> 6. Episode-Local Predicate Induction
> Each episode defines a temporary binary predicate over ordered image pairs.
> The support set contains labeled examples:
> (left image, right image, label)
> The query set contains unlabeled examples:
> (left image, right image)
> All rows in one episode use the same hidden predicate.
> The support set is therefore not merely a collection of examples from a class.
> It is the only public description of the predicate.
> To solve an episode, a model must determine:
> Which latent evidence patterns are relevant.
> Which patterns are distractors or confounders.
> Whether the relation is symmetric or directional.
> Whether the predicate uses one condition or several.
> Whether evidence must be shared, different, absent, exclusive, or side-specific.
> Which candidate interpretation remains consistent with every support label.
> Positive demonstrations reveal conditions that may be sufficient.
> Negative demonstrations eliminate competing explanations.
> The intended reasoning process is therefore closer to predicate reconstruction than prototype matching.
> 7. Episode Definition
> An episode contains two row groups.
> 7.1 Support rows
> Support rows contain:
> left_image
> right_image
> A visible binary label
> A support label of 1 means that the ordered pair satisfies the hidden predicate.
> A support label of 0 means that it does not.
> Every episode contains both positive and negative support rows.
> 7.2 Query rows
> Query rows contain:
> left_image
> right_image
> A missing label in test.csv
> Participants submit the probability that each query pair satisfies the same predicate demonstrated by the support rows.
> 7.3 Temporary semantics
> Support labels are meaningful only inside their own episode.
> A positive demonstration from one episode does not define the meaning of 1 in another episode.
> Two episodes may use:
> Different visual atoms with the same logical operator.
> The same visual atoms with different operators.
> Similar support images with different predicate semantics.
> Different combinations of atomic and multi-part conditions.
> 8. Predicate Families
> Episode predicates are sampled from a controlled grammar over latent visual atoms.
> Participants are told the broad predicate families so that the task has a defined inference space.
> The following remain hidden:
> The active visual atoms.
> The exact operator.
> The operator arguments.
> The complete predicate assigned to each episode.
> 8.1 Shared-evidence predicates
> A pair is positive when both images contain a particular evidence pattern.
> A predicate may also require several patterns to be shared.
> Conceptual form:
> positive when atom A is present on both sides
> 8.2 Ordered-side predicates
> A pair is positive when evidence appears on one specified side and is absent or different on the other.
> Conceptual form:
> positive when atom A is present on the left but absent on the right
> Reversing the pair may change the label.
> 8.3 Exclusive-presence predicates
> A pair is positive when exactly one image contains the relevant evidence.
> Conceptual form:
> positive when atom A occurs on one side, but not both
> 8.4 Cross-side conjunction predicates
> A pair is positive when different side-specific requirements are jointly satisfied.
> Conceptual form:
> positive when the left contains atom A and the right contains atom B
> 8.5 Shared-and-different predicates
> A pair is positive when the images agree with respect to one evidence pattern and disagree with respect to another.
> Conceptual form:
> positive when atom A is shared and atom B differs
> 8.6 Evidence-set predicates
> A pair is positive when the latent evidence sets satisfy a structural condition.
> Possible conditions include:
> Non-empty intersection.
> Required intersection size.
> Required difference size.
> Containment.
> Partial overlap.
> Equality on a selected subset.
> Cardinality constraints.
> 8.7 Multi-part predicates
> Some episodes combine several atomic requirements.
> A pair may need to:
> Share one visual atom.
> Differ on another.
> Place a third atom on a specified side.
> A query is positive only when the complete predicate is satisfied.
> Partial satisfaction is negative.
> 9. Why the Task Is Difficult
> 9.1 The target semantics are reconstructed at inference time
> There is no permanent positive class.
> The output meaning must be inferred again for every episode.
> A visual factor that determines the label in one episode may be irrelevant in another.
> 9.2 The model must infer a relation, not only a concept
> Even after identifying the relevant retinal evidence, the model must determine how that evidence is combined across the ordered pair.
> The same atom may participate in:
> A shared condition.
> An exclusive condition.
> A left-only condition.
> A right-only condition.
> A conjunction with another atom.
> A higher-order evidence-set condition.
> 9.3 Images contain several simultaneous factors
> The underlying data is multi-label.
> A support pair may share multiple visible properties, even though only one or two define the predicate.
> The model must separate predicate-relevant evidence from coincidental co-occurrence.
> 9.4 Support examples admit competing hypotheses
> A small number of demonstrations may initially support several candidate predicates.
> For example, positive rows may be consistent with both:
> Shared presence of atom A.
> General abnormality on both sides.
> Shared presence of atom B.
> High evidence cardinality.
> A conjunction involving A and B.
> Negative counterexamples are required to eliminate these alternatives.
> 9.5 Negative rows are designed as logical counterexamples
> Negative pairs are not merely random mismatches.
> They may:
> Share common abnormalities with positive pairs.
> Match positive pairs in overall severity.
> Contain the relevant atom on the wrong side.
> Satisfy only one clause of a multi-part predicate.
> Support a plausible but incorrect simpler rule.
> Differ from positive rows in a subtle or less frequent factor.
> 9.6 Pair order can change the result
> For directional predicates:
> predicate(I_a, I_b) != predicate(I_b, I_a)
> A purely symmetric similarity representation cannot fully solve these episodes.
> 9.7 Factor-operator bindings change during evaluation
> Evaluation may use a familiar visual atom with a familiar predicate family but combine them in a way not observed in training.
> The model must therefore learn:
> Reusable visual factors.
> Reusable relation operators.
> A mechanism for binding them from support evidence.
> Memorizing complete training predicates is insufficient.
> 9.8 Confidence is part of the task
> Some support sets identify one predicate clearly.
> Others leave several plausible explanations.
> Models must express uncertainty through probability estimates.
> Extreme probabilities based on an unstable predicate hypothesis are penalized by the calibration component.
> 10. Episode Construction
> Raw clinical annotations are used only during benchmark preparation.
> The public task exposes:
> Anonymized ocular images.
> Ordered pair structure.
> Support labels.
> Training query labels.
> Test query identifiers.
> It does not expose:
> Original annotation matrices.
> Original filenames.
> Clinical label names.
> Latent atom identities.
> Predicate definitions.
> Predicate-family labels.
> Episode-generation metadata.
> Source-record identifiers.
> 10.1 Support-set sufficiency
> Each support set contains both positive and negative examples.
> Episode generation checks that the intended predicate can be distinguished from simpler competing hypotheses.
> Counterexamples are inserted where needed to distinguish:
> Conjunction from single-factor presence.
> Exclusive presence from ordinary presence.
> Directional predicates from symmetric predicates.
> Shared evidence from generic abnormality.
> Complete multi-part predicates from partial satisfaction.
> Evidence identity from overall evidence burden.
> 10.2 Variable episode size
> Episodes contain different numbers of support and query rows.
> Typical episodes contain:
> 8 to 14 support pairs.
> 6 to 12 query pairs.
> Positive and negative support examples.
> Positive and negative query examples.
> The variable structure prevents dependence on a fixed row count or fixed episode layout.
> 10.3 Prevalence-aware sampling
> Frequently occurring latent atoms are prevented from dominating the benchmark.
> Episode construction balances:
> Atom frequency.
> Predicate-family coverage.
> Positive and negative availability.
> Co-occurrence structure.
> Hard-negative availability.
> Less frequent atoms remain important because evaluation is aggregated by episode rather than by raw query count.
> 10.4 Counterfactual and hard-negative sampling
> Some negative pairs are selected because they nearly satisfy the predicate.
> A hard negative may:
> Satisfy all but one predicate clause.
> Reverse a directional condition.
> Contain the correct atoms on the wrong sides.
> Support a competing shared-evidence interpretation.
> Match the positive rows in evidence count while differing in evidence identity.
> 10.5 Image-pool separation
> Images are divided into disjoint development and evaluation pools before episode generation.
> An evaluation image does not appear in a public training episode.
> Images may be reused across several episodes within the same split because each episode can assign a different temporary semantic role to the image.
> 10.6 Anonymization
> Original filenames, annotation identifiers, source ordering, and source-specific metadata are removed.
> Each published image, episode, and pair receives an opaque randomized identifier.
> Identifiers do not encode:
> Source identity.
> Split membership.
> Image labels.
> Predicate family.
> Active atoms.
> Row role.
> Generation order.
> File-byte hash.
> Identifiers are not valid predictive features.
> 11. Evaluation Generalization Conditions
> The evaluation set contains several controlled generalization conditions.
> 11.1 Held-out images
> Evaluation images come from an image pool disjoint from the training image pool.
> 11.2 New evidence co-occurrences
> Individual visual atoms may appear in training while particular combinations of those atoms are reserved for evaluation.
> 11.3 New factor-operator bindings
> A predicate operator observed with one group of atoms during training may be assigned to different atoms during evaluation.
> 11.4 New composed predicates
> Some evaluation episodes combine predicate clauses in arrangements not present in the public training episodes.
> 11.5 Less frequent evidence
> Some episodes depend on latent atoms that occur less frequently in the image collection.
> 11.6 Degraded observations
> A subset of images may exhibit:
> Low contrast.
> Weak illumination.
> Partial obstruction.
> Reduced visible retinal area.
> Imperfect field centering.
> 11.7 Alternative-hypothesis negatives
> Some negative queries are selected specifically because they satisfy a plausible but incorrect interpretation of the support rows.
> No condition or regime identifier is provided.
> 12. Public Dataset
> The public release contains:
> undefined
> public/
> ├── train.csv
> ├── test.csv
> ├── sample_submission.csv
> └── images/
> ### 12.1 `train.csv`
> `train.csv` contains complete labeled training episodes.
> It includes:
> * Support rows with labels.
> * Query rows with labels.
> * Ordered left and right image paths.
> * Episode identifiers.
> * Pair identifiers.
> Training query labels allow participants to train and validate complete predicate-induction systems.
> ### 12.2 `test.csv`
> `test.csv` contains evaluation episodes.
> It includes:
> * Support rows with visible labels.
> * Query rows with missing labels.
> * Ordered left and right image paths.
> * Episode identifiers.
> * Pair identifiers.
> Participants submit predictions for query rows only.
> ### 12.3 `sample_submission.csv`
> `sample_submission.csv` is the authoritative submission template.
> It contains:
> * One row for every query pair in `test.csv`.
> * The required `pair_id` column.
> * The required `probability` column.
> * The expected query identifier set.
> * The expected column order.
> ### 12.4 `images/`
> The `images/` directory contains every unique ocular image referenced by the CSV files.
> Each unique image is stored once, even when reused across multiple pairs or episodes.
> Images are:
> * Stored in JPEG format.
> * Loaded as RGB.
> * Standardized through retinal-field cropping.
> * Square-padded before resizing.
> * Re-encoded to remove source metadata and source-specific file structure.
> CSV rows reference images through relative paths such as:
> `images/57b6e3fa9c624742a68cc32231bf447d.jpg`
> The authoritative image count is the number of unique paths referenced across `train.csv` and `test.csv`.
> ## 13. Training Data
> `train.csv` contains the following columns:
> * `episode_id`
> * `pair_id`
> * `left_image`
> * `right_image`
> * `role`
> * `label`
> ### `episode_id`
> Type: string.
> An opaque identifier for one episode.
> All rows sharing an `episode_id` use the same hidden predicate.
> The identifier does not encode:
> * The predicate.
> * The active atoms.
> * Predicate difficulty.
> * Source identity.
> * Generation order.
> ### `pair_id`
> Type: string.
> A unique identifier for one ordered image pair.
> It does not encode:
> * The two image identities.
> * Pair label.
> * Episode predicate.
> * Row role.
> * Source records.
> * Generation order.
> ### `left_image`
> Type: string.
> Relative path to the left image.
> ### `right_image`
> Type: string.
> Relative path to the right image.
> Image order may affect the label.
> ### `role`
> Type: string.
> Allowed values:
> * `support`
> * `query`
> ### `label`
> Type: integer.
> Allowed values:
> * `0`: the ordered pair does not satisfy the hidden episode predicate.
> * `1`: the ordered pair satisfies the hidden episode predicate.
> Labels are provided for support and query rows in `train.csv`.
> ## 14. Test Data
> `test.csv` uses the same columns as `train.csv`.
> For support rows:
> * `role` is `support`.
> * `label` is provided.
> For query rows:
> * `role` is `query`.
> * `label` is missing.
> * Participants must submit a probability.
> Conceptual example:
> episode_id,pair_id,left_image,right_image,role,label
> ep_c72f91a4,pr_88d24c1e,images/57b6e3fa9c624742a68cc32231bf447d.jpg,images/140c82db8fe5435ca2dcdebf481bb1da.jpg,support,1
> ep_c72f91a4,pr_509de7b3,images/a29a8343cbb644368096e72e930eb618.jpg,images/c88d76b6833d40aca57228d7a9fe919e.jpg,support,0
> ep_c72f91a4,pr_b904f873,images/4f33470cebf241b785a2a80686a90f76.jpg,images/7fa0698179094c46be3ffca74bdce846.jpg,query,
> ep_c72f91a4,pr_21cb8fd0,images/e46d78940ea844a08bd295d1306868fd.jpg,images/1776a67b78b44acd91c1c63225ace2ec.jpg,query,
> Identifiers are illustrative only.
> Support semantics do not transfer between episodes.
> ## 15. Submission Format
> Submit one probability for every query row in `test.csv`.
> Required columns:
> * `pair_id`
> * `probability`
> Example:
> pair_id,probability
> pr_b904f873,0.731
> pr_21cb8fd0,0.184
> Requirements:
> * Include query pairs only.
> * Include every test query `pair_id` exactly once.
> * Do not include support rows.
> * Do not include unknown identifiers.
> * Do not omit query identifiers.
> * Do not include duplicate identifiers.
> * Use finite numeric probabilities.
> * Keep all probabilities in `[0, 1]`.
> * Do not add extra columns.
> * Submission row order does not matter.
> Use `sample_submission.csv` as the authoritative schema.
> ## 16. Evaluation
> Evaluation is performed independently within each episode before episode scores are aggregated.
> This prevents episodes with more query rows from dominating the leaderboard.
> Every evaluated episode contains at least one positive query and at least one negative query.
> Probabilities used in logarithmic calculations are clipped to:
> `[0.000001, 0.999999]`
> Each episode receives three component scores:
> * Within-Episode Ranking.
> * Class-Balanced Calibration.
> * Threshold Agreement.
> ### 16.1 Within-Episode Ranking
> The ranking component measures whether positive queries receive higher probabilities than negative queries from the same episode.
> For every positive-negative query comparison:
> * Award `1` when the positive query has the higher probability.
> * Award `0.5` when the probabilities are equal.
> * Award `0` when the negative query has the higher probability.
> The ranking score is:
> `R_e = total ranking credit / number of positive-negative comparisons`
> This is equivalent to episode-level ROC AUC with half credit for ties.
> The score lies in:
> `[0, 1]`
> ### 16.2 Class-Balanced Calibration
> Positive and negative log losses are calculated separately.
> For positive queries:
> `L_positive = mean of -log(p_i)`
> For negative queries:
> `L_negative = mean of -log(1 - p_i)`
> The balanced calibration loss is:
> `L_balanced = (L_positive + L_negative) / 2`
> The calibration utility is:
> `C_e = exp(-L_balanced)`
> The value lies in:
> `(0, 1]`
> Positive and negative queries receive equal total importance.
> ### 16.3 Threshold Agreement
> Predictions are converted into binary decisions using a threshold of `0.5`.
> A query is predicted positive when:
> `probability >= 0.5`
> Otherwise, it is predicted negative.
> For each episode:
> `TPR_e = correctly predicted positive queries / number of positive queries`
> `TNR_e = correctly predicted negative queries / number of negative queries`
> Threshold Agreement is:
> `B_e = (TPR_e + TNR_e) / 2`
> This is episode-level balanced accuracy.
> ### 16.4 Per-Episode Score
> The score for episode `e` is:
> `S_e = 0.50 × R_e + 0.35 × C_e + 0.15 × B_e`
> ### 16.5 Robustness Aggregation
> Let `E` be the number of evaluated episodes.
> The mean episode score is:
> `MeanScore = sum of S_e across all episodes / E`
> Let `LowerQuartile` be the 25th percentile of all episode scores.
> The final score is:
> `Final Score = 100 × (0.80 × MeanScore + 0.20 × LowerQuartile)`
> The score is clipped to:
> `[0, 100]`
> A higher score is better.
> The lower-quartile term rewards systems that remain reliable across difficult predicate families rather than succeeding only on simple episodes.
> ## 17. What the Metric Rewards
> A strong submission should:
> * Infer the local predicate from support rows.
> * Rank positive queries above negative queries within each episode.
> * Produce calibrated probabilities.
> * Preserve left-to-right order when required.
> * Handle shared, exclusive, directional, and composed predicates.
> * Remain reliable across uncommon and difficult episodes.
> * Avoid catastrophic failure under new factor-operator bindings.
> A constant prediction receives limited ranking and threshold credit.
> Overconfident predictions based on an unstable predicate hypothesis are penalized by calibration loss.
> A system that solves only common shared-evidence predicates loses score through episode-level averaging and lower-quartile aggregation.
> ## 18. Feasible Modeling Approaches
> Each unique image can be encoded once and its representation cached.
> Episode inference can then operate on compact image and pair representations.
> Possible approaches include:
> * Frozen visual encoders.
> * Self-supervised retinal representations.
> * Transfer learning.
> * Multi-factor image embeddings.
> * Ordered-pair encoders.
> * Support-conditioned relation models.
> * Local ridge or logistic regression.
> * Episode-specific linear probes.
> * Set encoders.
> * Predicate-candidate scoring.
> * Latent rule enumeration.
> * Probabilistic hypothesis selection.
> * Calibrated ensembles.
> * Hybrid neural and symbolic models.
> For image embeddings `u` and `v`, a useful ordered-pair representation is:
> `pair_features(u, v) = [u, v, abs(u - v), u - v, u * v]`
> This includes:
> * Separate side-specific features.
> * Symmetric comparison features.
> * Directional difference features.
> * Multiplicative interaction features.
> A local classifier may be fitted on the support-pair representations within each episode.
> This provides a meaningful baseline but may struggle when:
> * The relevant visual atom is weak.
> * Confounding findings dominate the representation.
> * The predicate contains several clauses.
> * Several predicate hypotheses fit the support set.
> * Evaluation introduces a new factor-operator binding.
> ## 19. Method Requirements
> Predictions must depend on the supplied images and the labeled support rows of each episode.
> ### Allowed methods
> Participants may use:
> * Classical machine-learning models.
> * CPU-compatible neural models.
> * Pretrained encoders available in the execution environment.
> * Transfer learning.
> * Learned image embeddings.
> * Learned ordered-pair embeddings.
> * Support-conditioned models.
> * Test-time fitting on support rows.
> * Unsupervised learning on supplied images.
> * Self-supervised learning on supplied images.
> * Probabilistic models.
> * Calibrated ensembles.
> * Hybrid neural and symbolic methods.
> * Handcrafted preprocessing used as part of a learned visual system.
> ### Prohibited methods
> Participants may not:
> * Match images against external copies of the source data.
> * Recover original annotations from public datasets.
> * Use external clinical or diagnostic repositories.
> * Use filename-, path-, hash-, or identifier-based lookup tables.
> * Infer labels from identifier formatting.
> * Infer labels from row or file ordering.
> * Manually encode answers for recognized images.
> * Use external diagnostic APIs.
> * Use online inference services.
> * Access the internet during execution.
> * Use hidden annotations.
> * Use private manifests.
> * Use hidden predicate-generation metadata.
> * Submit predictions that do not depend on supplied image content.
> Identifiers are opaque and randomized.
> They must not be treated as predictive features.
> ## 20. Intended Difficulty
> A frozen visual encoder combined with an episode-local linear classifier should provide a non-trivial baseline.
> Such a system is not expected to solve the benchmark completely because:
> * The meaning of the positive label changes between episodes.
> * The model must infer both evidence identity and relation structure.
> * Some predicates depend on pair order.
> * Support rows contain unrelated co-occurring findings.
> * Negative rows act as close logical counterexamples.
> * Evaluation changes factor-operator bindings.
> * Some predicates contain several clauses.
> * Less frequent evidence may be poorly preserved in generic embeddings.
> * Several predicate hypotheses may fit a small support set.
> * Uncertainty varies between episodes.
> Higher-performing systems will likely require:
> * Image representations that preserve multiple independent retinal factors.
> * Ordered-pair representations that retain direction.
> * Explicit comparison of competing predicate hypotheses.
> * Joint use of positive demonstrations and negative counterexamples.
> * Compositional reuse of visual factors and logical operators.
> * Calibrated uncertainty when the support specification is ambiguous.
> The central question is not whether a model can recognize retinal abnormalities.
> It is whether a model can reconstruct a temporary visual predicate from examples and execute that predicate reliably on new ordered image pairs.
> &nbsp;

Inspiration note: Useful because it uses visual evidence for structured state or risk prediction, not just ordinary image classification.

## Coil Quarantine

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a5x92gvm3cwyw4hda9a4a1n8asvne
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> For each two-panel steel inspection image, predict four outputs: a 2 by 6 quarantine grid, a two-panel cut program, a span-relation graph, and a release disposition. Together, these outputs state where defects occur, the smallest horizontal interval that must be removed or isolated in each panel, which occupied zones are related, and whether the material can proceed.
> The images are derived from real 400 by 400 photographs of cold-rolled steel surfaces collected during production inspection at a steel company in China. The source collection covers seven annotation families, including inclusions, dents, oil spots, pits, punching defects, linear scratches, and macular discoloration. The source does not publish detailed camera settings, so no particular lens, exposure, or illumination setup should be assumed. Each challenge image combines two source windows and applies controlled reflections, mild photometric changes, sensor noise, and JPEG re-encoding while preserving the defect geometry.
> In a steel inspection workflow, locating a mark is only the first step. Downstream equipment needs an auditable handling instruction that identifies the affected span and the required level of isolation. Over-quarantining wastes usable material, while under-quarantining can release damaged steel. The challenge therefore evaluates whether visual evidence can be converted into one internally consistent control record rather than only a defect class.
> Dataset
> The prepared data contains 3,146 labeled training cases and 935 test cases. Every case is an 808 by 400 JPEG made from two real 400 by 400 inspection windows separated by an eight-pixel divider. Deterministic horizontal and vertical reflections, mild photometric changes, low-level sensor noise, and JPEG re-encoding increase orientation coverage and prevent direct source matching while preserving every annotation.
> The source archive contains 59 pairs of byte-identical images with conflicting annotation files. Each duplicate group is represented once, and its boxes are merged by class with an IoU threshold of 0.85. Neighboring source-index blocks connected by a duplicate are treated as one split component. No source image, duplicate payload, or connected neighboring block crosses between train and test.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Labeled rows with `case_id`, `inspection_path`, `coil_contract`, `quarantine_grid`, `cut_interval_program`, `span_relation_graph`, and `release_disposition`. |
> | `test.csv` | Unlabeled rows with only `case_id`, `inspection_path`, and `coil_contract`. |
> | `sample_submission.csv` | Submission template containing `case_id` and the four target columns in the required order. |
> | `inspections/*.jpg` | 808 by 400 RGB JPEG images. The left 400-pixel panel is `p1`, an eight-pixel divider follows, and the right 400-pixel panel is `p2`. |
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque unique case identifier. |
> | `inspection_path` | string | POSIX-style path relative to the public dataset root, for example `inspections/8f31c2a47d.jpg`. Join this value directly to the dataset root to load the image. |
> | `coil_contract` | string | A plain-language interpretation contract. In this release it states that the left panel is `p1`, the right panel is `p2`, each panel is divided into `z1` through `z6`, and the cut must be the smallest interval covering every visible defect center. It is an instruction string, not a target label, and has the same format in train and test. |
> Zone Coordinate System
> Each 400-pixel panel is divided left to right into equal zones z1 through z6. The quarantine_grid has two rows in panel order and six columns in zone order.
> | Grid value | Meaning |
> |---:|---|
> | 0 | No annotated defect center in the zone. |
> | 1 | One compact defect center. |
> | 2 | Two defect centers, or at least one broad defect whose normalized area is at least 0.08 or width is at least 0.34. |
> | 3 | Three or more defect centers. |
> Target Columns
> | Column | Data type | Description |
> |---|---|---|
> | `quarantine_grid` | JSON integer matrix | Shape 2 by 6 with values 0 through 3 using the semantics above. |
> | `cut_interval_program` | ordered token string | Exactly two panel operations followed by `seal:coil`. A panel operation is `pN:release` or `pN:cut:zA-zB`, where `A` and `B` are the first and last occupied zones. |
> | `span_relation_graph` | canonical edge set string | Sorted edges joined by `|`, or `none`. Within-panel edges join adjacent zones crossed by one annotated box. Cross-panel edges join the nearest occupied zones when both panels contain the same defect family. |
> | `release_disposition` | categorical string | One of `local_trim`, `isolate_window`, `segmented_hold`, or `full_hold`. |
> Disposition follows the complete packet geometry. local_trim requires every panel span to be at most one zone and at most one severity-2-or-3 cell overall. full_hold applies when a panel spans at least five zones or the packet has at least five severity-2-or-3 cells. Otherwise, a packet with a span of at least three zones and another panel spanning at most two zones is isolate_window; remaining cases are segmented_hold.
> Training disposition counts are 436 local_trim, 511 isolate_window, 1,879 segmented_hold, and 320 full_hold. Test counts are 101, 176, 547, and 111.
> Submission Format
> Write predictions to:
> ./working/submission.csv
> The CSV must contain exactly these columns in this order:
> case_id,quarantine_grid,cut_interval_program,span_relation_graph,release_disposition
> Example:
> case_id,quarantine_grid,cut_interval_program,span_relation_graph,release_disposition
> 6d39f082ac786a1877e1c81f,"[[0,1,2,0,0,0],[0,0,0,1,1,0]]",p1:cut:z2-z3>p2:cut:z4-z5>seal:coil,p1z2~p1z3|p2z4~p2z5,segmented_hold
> Each prediction field uses the following canonical format:
> | Column | Required format |
> |---|---|
> | `quarantine_grid` | JSON-encoded 2 by 6 integer matrix with values from 0 through 3. Row 1 represents `p1`; row 2 represents `p2`. |
> | `cut_interval_program` | Exactly three tokens separated by `>`, in the order `p1 operation > p2 operation > seal:coil`. A panel operation is `pN:release` or `pN:cut:zA-zB`, with `A` not greater than `B`. Example: `p1:release>p2:cut:z3-z5>seal:coil`. |
> | `span_relation_graph` | `none` or a lexicographically sorted, duplicate-free list of edges separated by `|`. A node such as `p1z2` means panel 1, zone 2. An undirected edge such as `p1z2~p1z3` links two related occupied zones. |
> | `release_disposition` | Exactly one of `local_trim`, `isolate_window`, `segmented_hold`, or `full_hold`. |
> Extra columns, reordered columns, duplicate IDs, missing IDs, and extra rows are rejected. Only an optional backend-added visibility column is ignored.
> Evaluation
> The metric is Material Quarantine Program Score:
> Score = 0.42 * GridScore
> + 0.27 * CutProgramScore
> + 0.19 * RelationGraphScore
> + 0.12 * DispositionScore
> For the 12 grid entries:
> GridScore = 0.14 * entry_accuracy + 0.86 * exact_matrix_match
> Cut-program edit distance is computed over the three >-separated tokens:
> edit_similarity = 1 - edit_distance(true_tokens, predicted_tokens)
> / max(number_of_true_tokens, number_of_predicted_tokens, 1)
> CutProgramScore = 0.16 * edit_similarity + 0.84 * exact_program_match
> For graph edges, set F1 is combined with exact-set credit. If T is the true edge set and P is the predicted edge set, then:
> set_F1 = 2 * |T intersection P| / (|T| + |P|)
> RelationGraphScore = 0.20 * set_F1 + 0.80 * exact_graph_match
> DispositionScore = 1 when the categorical value is exact, otherwise 0
> When both graph sets are empty, set_F1 is 1. When only one is empty, it is 0.
> The weighted formula above is first evaluated separately for each test case. A submitted panel is coherent when its program says release exactly when all six submitted grid entries for that panel are zero, and says cut exactly when at least one submitted grid entry is nonzero. If either panel is incoherent, the complete weighted score for that case is multiplied once by 0.90:
> adjusted_case_score = base_case_score                  if both panels are coherent
> adjusted_case_score = 0.90 * base_case_score           otherwise
> final_score = mean(adjusted_case_score over test cases)
> Malformed or overlong values score zero for their affected component. The coherence multiplier is then applied to the remaining per-case weighted score when applicable.
> Minimum score: 0.0
> Maximum score: 1.0
> Direction: higher is better.
> What Makes This Interesting
> This task begins with sparse real industrial evidence but ends with an executable material-control record. The relation graph requires reasoning about box extent and repeated morphology, while the exact interval grammar punishes both missed defects and wasteful over-coverage. The held-out neighboring blocks reduce gains from memorizing visually adjacent source frames.
> Method Requirements
> CPU-compatible detectors, compact convolutional models, vision transformers sized for CPU inference, segmentation models, and learned structured decoders are allowed. Classical preprocessing may support a learned visual system but cannot replace it as the primary solver.
> What Not To Use
> Do not recover original defect labels, source basenames, image indices, or annotations from external mirrors or lookup tables.
> Do not infer targets from opaque IDs, row order, JPEG hashes, source-neighbor ordering, or storage paths.
> Do not use hidden test cases for model updates, pseudo-label calibration, or threshold tuning.
> Do not exploit malformed JSON, repeated IDs, missing rows, extra columns, or grader behavior.
> Do not call hosted closed-model APIs during inference.

Inspiration note: Useful because it uses visual evidence for structured state or risk prediction, not just ordinary image classification.
## Reference-Guided Ultrasound Frame Retrieval and Sweep Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77x4n66pnyevbqm60b4xa6w58axcv7
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Be the first to climb the leaderboard!

### Full Challenge Description

> 1. Overview
> Reference-Guided Ultrasound Frame Retrieval and Sweep Reconstruction is a structured computer-vision challenge.
> For each case, participants receive one reference frame and twelve shuffled candidate frames. They must predict:
> Which seven candidates belong to the same acquisition sweep as the reference.
> The relative temporal positions position_0 through position_6 of those seven candidates.
> The start and end of the contiguous usable interval within the reconstructed sequence.
> The probability that the complete reconstruction is exactly correct.
> Each case contains:
> One reference frame.
> Twelve numbered candidate frames.
> Exactly seven true sweep members.
> Exactly five authentic distractors from other sweeps.
> Seven unique temporal positions.
> One non-empty contiguous usable interval.
> One complete-sweep confidence target.
> The challenge is not ordinary image classification or simple frame sorting.
> The correct sequence members are unknown, and several distractors may look highly compatible with the reference or with one another. A successful model must jointly retrieve, order, and evaluate the sequence.
> 2. Dataset and Source
> The dataset is derived from high-frequency ultrasound sequences of facial skin.
> The source recordings contain gradual visual changes involving:
> Internal structures.
> Boundary positions.
> Texture.
> Contrast.
> Signal intensity.
> Acquisition contact.
> Field coverage.
> Local deformation.
> Artifact strength.
> The challenge does not ask participants to identify patients, anatomical locations, medical conditions, or source recording sessions.
> Original source information is not released, including:
> Patient identifiers.
> Acquisition dates.
> Facial locations.
> Original filenames.
> Original frame indices.
> Source sequence identifiers.
> Expert identities.
> The participant-facing files are:
> /
> ├── images/
> ├── train.csv
> ├── test.csv
> └── sample_submission.csv
> The contact-sheet PNG is the only model input for each case.
> 3. Prediction Task and Novelty
> Most temporal-ordering datasets provide frames that are already known to belong to one sequence.
> This challenge does not.
> Five of the twelve candidates are distractors and must be rejected before the target sequence can be reconstructed.
> Most reference-based retrieval tasks stop after identifying matching items.
> Here, the selected items must also be assigned one-to-one to seven temporal positions.
> Most image-quality tasks classify individual frames independently.
> Here, usability is represented as one contiguous interval over the reconstructed sequence.
> The challenge therefore combines:
> Reference-conditioned frame retrieval.
> Same-sweep verification.
> Authentic hard-negative rejection.
> Ordered-subset recovery.
> One-to-one temporal assignment.
> Pairwise temporal reasoning.
> Contiguous interval localization.
> Exact reconstruction scoring.
> Confidence calibration.
> The output is one structured interpretation of the entire case rather than a set of independent labels.
> 4. Contact-Sheet Images
> Each case is stored as one RGB PNG contact sheet.
> The image dimensions are:
> Width: 640 pixels.
> Height: 440 pixels.
> Color mode: RGB.
> Each contact sheet contains:
> One 112 × 112 reference panel.
> Twelve 112 × 112 candidate panels.
> A four-column by three-row candidate grid.
> Candidate numbering follows row-major order:
> 0   1   2   3
> 4   5   6   7
> 8   9  10  11
> Candidate order is randomized independently for every case.
> Candidate index does not reveal:
> Membership.
> Temporal position.
> Usability.
> Source sequence.
> Distance from the reference.
> Whether the frame occurs before or after the reference.
> Case difficulty.
> The underlying ultrasound panels are grayscale, but the full contact sheets are stored as RGB PNG files.
> 5. Reference Frames, True Members, and Distractors
> The reference frame comes from the same acquisition sweep as the seven true candidates.
> It may be mildly altered to discourage direct pixel matching. Possible alterations include:
> Downsampling and resizing.
> Gaussian blur.
> Contrast adjustment.
> Brightness adjustment.
> Low-level noise.
> Partial masking.
> Small border removal.
> The seven true candidates are authentic frames selected from the reference sweep.
> The five distractors are also authentic ultrasound frames. They are not random noise or synthetic corruptions.
> Distractors may resemble the target sweep in:
> Brightness.
> Contrast.
> Texture.
> Structural layout.
> Edge density.
> Signal quality.
> Artifact appearance.
> Local deformation.
> Apparent temporal progression.
> Several distractors may come from one alternative sweep and form a convincing short sequence.
> A candidate is correct because it contributes to the globally coherent target sequence, not merely because it looks individually similar to the reference.
> 6. Temporal Order and Usable Interval
> The seven true candidates correspond to seven relative temporal positions:
> position_0
> position_1
> position_2
> position_3
> position_4
> position_5
> position_6
> position_0 is the earliest selected frame.
> position_6 is the latest selected frame.
> These are relative positions within the challenge case. They are not original source frame numbers or timestamps.
> The selected frames may contain gaps in the original acquisition.
> After reconstructing the sequence, participants must predict:
> usable_start
> usable_end
> Both values range from 0 through 6, and the interval includes both endpoints.
> Examples:
> Start 0, end 6: all seven reconstructed positions are usable.
> Start 2, end 5: positions 2 through 5 are usable.
> Start 4, end 4: only position 4 is usable.
> A true sweep member may lie outside the usable interval. Membership and usability are separate targets.
> The hidden interval is derived from source expert-quality annotations. The target is the longest contiguous run of informative frames after the seven true members are placed in temporal order.
> For example:
> 0, 1, 1, 1, 0, 1, 0
> produces:
> usable_start = 1
> usable_end = 3
> If several informative runs have the same maximum length, the earliest run is selected.
> Every generated case contains a non-empty usable interval.
> 7. Training Data
> train.csv contains one row per labeled training case.
> Its columns are:
> sample_id
> image_file
> member_0 through member_11
> position_0 through position_11
> usable_start
> usable_end
> sample_id
> Type: String.
> A unique opaque case identifier.
> The identifier must not be used as a predictive feature.
> image_file
> Type: String.
> Relative path to the corresponding contact-sheet PNG.
> Example:
> undefined
> images/sweep_a1b2c3d4e5f6.png
> ### `member_0` through `member_11`
> Type: Integer.
> For candidate `i`:
> - `1`: Candidate `i` belongs to the reference sweep.
> - `0`: Candidate `i` is a distractor.
> Every row contains exactly seven values equal to `1` and five values equal to `0`.
> ### `position_0` through `position_11`
> Type: String.
> For candidate `i`, the allowed values are:
> - `position_0`
> - `position_1`
> - `position_2`
> - `position_3`
> - `position_4`
> - `position_5`
> - `position_6`
> - `distractor`
> Every row contains exactly one occurrence of each temporal position and exactly five `distractor` values.
> A candidate with `member_i = 1` always has one of the seven position labels.
> A candidate with `member_i = 0` always has the label `distractor`.
> ### `usable_start`
> Type: Integer.
> First position in the usable interval. Allowed values are `0` through `6`.
> ### `usable_end`
> Type: Integer.
> Last position in the usable interval. Allowed values are `0` through `6`.
> Every row satisfies:
> 0 <= usable_start <= usable_end <= 6
> 8. Test Data
> test.csv contains one row per evaluation case.
> Its columns are:
> sample_id
> image_file
> For every test case, participants must submit:
> Twelve membership probabilities.
> Eight temporal-state probabilities for each of the twelve candidates.
> Seven usable-start probabilities.
> Seven usable-end probabilities.
> One complete-sweep confidence probability.
> Test rows follow the same structural rules as training rows:
> Exactly seven true members.
> Exactly five distractors.
> Exactly one candidate at each temporal position.
> One non-empty usable interval.
> 9. Submission Schema
> The submission must contain exactly 124 columns:
> One sample_id column.
> Twelve membership-probability columns.
> Ninety-six temporal-state probability columns.
> Seven start-probability columns.
> Seven end-probability columns.
> One p_sweep column.
> Membership probabilities
> The columns are:
> p_member_0 through p_member_11
> p_member_i is the probability that candidate i belongs to the reference sweep.
> Each value must be between 0 and 1.
> Membership probabilities do not need to sum to seven.
> Temporal-state probabilities
> For each candidate i, submit:
> p_candidate_i_position_0
> p_candidate_i_position_1
> p_candidate_i_position_2
> p_candidate_i_position_3
> p_candidate_i_position_4
> p_candidate_i_position_5
> p_candidate_i_position_6
> p_candidate_i_distractor
> The eight probabilities for each candidate must sum to 1 within an absolute tolerance of 0.00001.
> Interval probabilities
> Submit:
> p_start_0 through p_start_6
> p_end_0 through p_end_6
> The seven start probabilities must sum to 1.
> The seven end probabilities must sum to 1.
> Complete-sweep confidence
> p_sweep is the estimated probability that the decoded membership set, complete temporal assignment, usable start, and usable end are all exactly correct.
> It must be between 0 and 1.
> Participants should use sample_submission.csv as the authoritative column-order template.
> 10. Correctly Formatted Submission Example
> The following is a complete valid one-row CSV example containing all 124 required columns.
> The membership probabilities are all 0.50, each temporal distribution is uniform, both interval distributions sum exactly to 1, and p_sweep is 0.05.
> sample_id,p_member_0,p_member_1,p_member_2,p_member_3,p_member_4,p_member_5,p_member_6,p_member_7,p_member_8,p_member_9,p_member_10,p_member_11,p_candidate_0_position_0,p_candidate_0_position_1,p_candidate_0_position_2,p_candidate_0_position_3,p_candidate_0_position_4,p_candidate_0_position_5,p_candidate_0_position_6,p_candidate_0_distractor,p_candidate_1_position_0,p_candidate_1_position_1,p_candidate_1_position_2,p_candidate_1_position_3,p_candidate_1_position_4,p_candidate_1_position_5,p_candidate_1_position_6,p_candidate_1_distractor,p_candidate_2_position_0,p_candidate_2_position_1,p_candidate_2_position_2,p_candidate_2_position_3,p_candidate_2_position_4,p_candidate_2_position_5,p_candidate_2_position_6,p_candidate_2_distractor,p_candidate_3_position_0,p_candidate_3_position_1,p_candidate_3_position_2,p_candidate_3_position_3,p_candidate_3_position_4,p_candidate_3_position_5,p_candidate_3_position_6,p_candidate_3_distractor,p_candidate_4_position_0,p_candidate_4_position_1,p_candidate_4_position_2,p_candidate_4_position_3,p_candidate_4_position_4,p_candidate_4_position_5,p_candidate_4_position_6,p_candidate_4_distractor,p_candidate_5_position_0,p_candidate_5_position_1,p_candidate_5_position_2,p_candidate_5_position_3,p_candidate_5_position_4,p_candidate_5_position_5,p_candidate_5_position_6,p_candidate_5_distractor,p_candidate_6_position_0,p_candidate_6_position_1,p_candidate_6_position_2,p_candidate_6_position_3,p_candidate_6_position_4,p_candidate_6_position_5,p_candidate_6_position_6,p_candidate_6_distractor,p_candidate_7_position_0,p_candidate_7_position_1,p_candidate_7_position_2,p_candidate_7_position_3,p_candidate_7_position_4,p_candidate_7_position_5,p_candidate_7_position_6,p_candidate_7_distractor,p_candidate_8_position_0,p_candidate_8_position_1,p_candidate_8_position_2,p_candidate_8_position_3,p_candidate_8_position_4,p_candidate_8_position_5,p_candidate_8_position_6,p_candidate_8_distractor,p_candidate_9_position_0,p_candidate_9_position_1,p_candidate_9_position_2,p_candidate_9_position_3,p_candidate_9_position_4,p_candidate_9_position_5,p_candidate_9_position_6,p_candidate_9_distractor,p_candidate_10_position_0,p_candidate_10_position_1,p_candidate_10_position_2,p_candidate_10_position_3,p_candidate_10_position_4,p_candidate_10_position_5,p_candidate_10_position_6,p_candidate_10_distractor,p_candidate_11_position_0,p_candidate_11_position_1,p_candidate_11_position_2,p_candidate_11_position_3,p_candidate_11_position_4,p_candidate_11_position_5,p_candidate_11_position_6,p_candidate_11_distractor,p_start_0,p_start_1,p_start_2,p_start_3,p_start_4,p_start_5,p_start_6,p_end_0,p_end_1,p_end_2,p_end_3,p_end_4,p_end_5,p_end_6,p_sweep
> sweep_example001,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.142857,0.142857,0.142857,0.142857,0.142857,0.142857,0.142858,0.142857,0.142857,0.142857,0.142857,0.142857,0.142857,0.142858,0.05
> This row is structurally valid but represents an uninformative prediction.
> 11. Structured Decoding
> Predictions are decoded in three stages.
> Stage 1: Membership retrieval
> For each case, the evaluator ranks candidates by p_member_i from highest to lowest.
> The seven highest-ranked candidates are selected.
> When probabilities are equal, the lower candidate index ranks first.
> Stage 2: One-to-one temporal assignment
> The seven selected candidates must be assigned to positions 0 through 6.
> For selected candidate (i) and position (j), the assignment score is:
> p_candidate_i_position_j
> The evaluator examines every valid one-to-one assignment of the seven selected candidates to the seven positions.
> For assignment (A), its score is:
> assignment_score(A)
> =
> sum over selected candidates i of
> p_candidate_i_position_A(i)
> The assignment with the largest total score is selected.
> If several assignments have the same score, the first lexicographic assignment is used.
> All five unselected candidates are decoded as distractor.
> Stage 3: Interval decoding
> The predicted start is:
> argmax over j of p_start_j
> The predicted end is:
> argmax over j of p_end_j
> When probabilities are tied, the lower position index is selected.
> If the decoded start is greater than the decoded end, the predicted interval is invalid.
> 12. Evaluation
> The final score contains five utilities:
> Membership Utility.
> Ordering Utility.
> Pairwise Temporal Utility.
> Interval Utility.
> Sweep Confidence Utility.
> The final score is:
> final_score = 100 × (
> 0.25 × membership_utility
> + 0.25 × ordering_utility
> + 0.15 × pairwise_temporal_utility
> + 0.20 × interval_utility
> + 0.15 × sweep_confidence_utility
> )
> The result is clipped to the range [0, 100].
> 12.1 Membership Utility
> For one case, let:
> (y_i = 1) when candidate (i) is a true member and 0 otherwise.
> (p_i) be the submitted p_member_i.
> There are exactly seven true members.
> The soft intersection is:
> soft_intersection = sum from i=0 to 11 of y_i × p_i
> The soft union is:
> soft_union
> =
> sum from i=0 to 11 of p_i
> + 7
> - soft_intersection
> The case-level soft membership IoU is:
> soft_iou
> =
> (soft_intersection + 0.000000000001)
> /
> (soft_union + 0.000000000001)
> Membership Probability Utility is the mean soft IoU over all test cases:
> membership_probability_utility
> =
> mean(case-level soft_iou)
> Exact Membership Accuracy is the fraction of cases where the seven candidates with the highest membership probabilities exactly match the seven true members:
> exact_membership_accuracy
> =
> number of cases with exact selected member set
> /
> number of test cases
> Membership Utility is:
> undefined
> membership_utility
> =
> 0.60 × membership_probability_utility
> 0.40 × exact_membership_accuracy
> ### 12.2 Ordering Utility
> For candidate (i), let (q_{i,c}) be the submitted probability for temporal state (c).
> The eight states are:
> - `position_0`
> - `position_1`
> - `position_2`
> - `position_3`
> - `position_4`
> - `position_5`
> - `position_6`
> - `distractor`
> For each state (c), calculate the mean negative log probability over all candidates whose true state is (c):
> L_c
> =
> mean over candidates with true state c of
> -log(max(q_i,c, smallest positive float))
> Balanced Ordering Log Loss is the unweighted mean of the eight state-level losses:
> balanced_ordering_log_loss
> =
> (
> L_position_0
> L_position_1
> L_position_2
> L_position_3
> L_position_4
> L_position_5
> L_position_6
> L_distractor
> )
> /
> 8
> Ordering Probability Utility is:
> ordering_probability_utility
> =
> exp(-balanced_ordering_log_loss)
> The evaluator then performs the membership selection and one-to-one assignment described in Section 11.
> A case is exactly ordered only when the decoded state of all twelve candidates matches the truth:
> - All seven correct candidates are selected.
> - Every true candidate is assigned to its correct position.
> - Every distractor is decoded as `distractor`.
> Exact Ordering Accuracy is:
> exact_ordering_accuracy
> =
> number of exactly ordered cases
> /
> number of test cases
> Ordering Utility is:
> ordering_utility
> =
> 0.50 × ordering_probability_utility
> +
> 0.50 × exact_ordering_accuracy
> 12.3 Pairwise Temporal Utility
> The seven true candidates form:
> 7 × 6 / 2 = 21
> unordered pairs.
> For each pair of true candidates (a) and (b), the pair is correct when:
> Both candidates were selected into the decoded sequence.
> Their decoded relative order matches their hidden relative order.
> Formally, a pair is correct when:
> (decoded_position_a < decoded_position_b)
> ==
> (true_position_a < true_position_b)
> If either true candidate was not selected, that pair receives no credit.
> The case-level pairwise score is:
> correctly ordered true-member pairs / 21
> Pairwise Temporal Utility is the mean case-level pairwise score:
> undefined
> pairwise_temporal_utility
> =
> mean(correct pairs / 21)
> ### 12.4 Interval Utility
> The decoded and hidden intervals are converted into binary vectors of length seven.
> For interval `[start, end]`, vector position (j) is:
> 1 when start <= j <= end
> 0 otherwise
> For example, interval `[2, 5]` becomes:
> 0, 0, 1, 1, 1, 1, 0
> For a valid predicted interval, Interval IoU is:
> interval_iou
> =
> number of positions inside both intervals
> /
> number of positions inside either interval
> If decoded `start > end`, then:
> interval_iou = 0
> exact_interval = 0
> Mean Interval IoU is the mean over all cases.
> Exact Interval Accuracy is the fraction of cases where both boundaries are correct:
> decoded_start == usable_start
> and
> decoded_end == usable_end
> Interval Utility is:
> interval_utility
> =
> 0.65 × mean_interval_iou
> +
> 0.35 × exact_interval_accuracy
> 12.5 Sweep Confidence Utility
> A case has an exact sweep reconstruction only when all conditions hold:
> The selected member set is exactly correct.
> Every selected candidate has the correct temporal position.
> Every distractor is excluded.
> The usable start is correct.
> The usable end is correct.
> Define:
> sweep_target = 1 when the reconstruction is exact
> sweep_target = 0 otherwise
> Let submitted confidence be (p). Before log loss, it is clipped to:
> p_clipped = min(max(p, 0.000001), 0.999999)
> The case-level binary log loss is:
> -[sweep_target × log(p_clipped)
> + (1 - sweep_target) × log(1 - p_clipped)]
> Binary Sweep Log Loss is the mean over all cases:
> binary_sweep_log_loss
> =
> mean(case-level binary log loss)
> Confidence Probability Utility is:
> confidence_probability_utility
> =
> exp(-binary_sweep_log_loss)
> Exact Sweep Accuracy is:
> exact_sweep_accuracy
> =
> number of exact sweep reconstructions
> /
> number of test cases
> Sweep Confidence Utility is:
> sweep_confidence_utility
> =
> 0.50 × confidence_probability_utility
> +
> 0.50 × exact_sweep_accuracy
> 13. Submission Validation
> A submission is invalid and receives a score of 0 when any of the following occurs:
> The submission is not a valid table.
> A required column is missing.
> An unknown extra column is present.
> A column name is duplicated.
> A required sample_id is missing.
> An unknown sample_id is included.
> A sample_id appears more than once.
> A sample_id is blank.
> The submission has the wrong number of rows.
> A prediction is non-numeric.
> A prediction is NaN or infinite.
> A probability is below 0 or above 1.
> A candidate’s eight temporal-state probabilities do not sum to 1 within 0.00001.
> The seven start probabilities do not sum to 1 within 0.00001.
> The seven end probabilities do not sum to 1 within 0.00001.
> The submission must contain every sample_id from test.csv exactly once.
> Submission row order does not affect scoring.
> 14. Modeling Guidance and Restrictions
> A baseline model may:
> Crop the reference and twelve candidate panels.
> Encode every panel using a shared convolutional network.
> Compare each candidate representation with the reference representation.
> Predict membership probabilities.
> Predict temporal-state distributions.
> Pool case-level features to predict usable boundaries.
> Estimate complete-sweep confidence.
> Stronger approaches may use:
> Vision transformers.
> Set transformers.
> Graph neural networks.
> Reference-to-candidate cross-attention.
> Candidate-to-candidate cross-attention.
> Pairwise precedence models.
> Neural ranking.
> Differentiable sorting.
> Differentiable assignment.
> Pointer networks.
> Contrastive same-sweep learning.
> Global sequence-energy models.
> Beam search over ordered subsets.
> Interval-aware sequence decoders.
> Structured confidence calibration.
> Predictions must be based primarily on the supplied contact-sheet images.
> Predictions may not use:
> sample_id.
> Image filenames.
> CSV row order.
> PNG file size.
> PNG metadata.
> Compression characteristics.
> Hidden source identifiers.
> Original source filenames.
> Original frame indices.
> Acquisition dates.
> Patient identifiers.
> External copies of the source imagery.
> Hardcoded test predictions.
> Although the source images come from facial-skin ultrasound recordings, the challenge is a visual-reasoning benchmark.
> It is not intended for diagnosis, treatment selection, patient assessment, or clinical decision-making.
> 15. Summary
> Reference-Guided Ultrasound Frame Retrieval and Sweep Reconstruction asks participants to reconstruct one hidden ultrasound acquisition sequence.
> For each case, the model must:
> Select seven true frames from twelve candidates.
> Reject five authentic distractors.
> Assign the seven selected frames to temporal positions 0 through 6.
> Predict the contiguous usable interval.
> Estimate whether the entire reconstruction is exact.
> The defining difficulty is that neither sequence membership nor sequence order is provided.
> The benchmark evaluates reference-guided retrieval, hard-negative rejection, temporal reconstruction, interval localization, and confidence calibration in one clearly defined structured prediction task.

Inspiration note: Useful as inspiration for route/path reconstruction outputs with explicit evidence structure.
## 3-D Prostate MRI Topology Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79ch0gb4bhntbrb3c0qd509s8av51p
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Be the first to climb the leaderboard!

### Full Challenge Description

> # 3-D Prostate MRI Topology Reconstruction
> ## Overview
> Build a CPU-only medical-imaging model that reconstructs the prostate region
> from a two-channel 3-D MRI volume. The release is derived from a licensed
> prostate MRI segmentation collection. In the clinical scenario, a segmentation
> system can support quantitative prostate measurements and downstream image
> analysis. The source annotations distinguish peripheral and transition zones;
> this challenge deliberately merges both foreground zones so the target is a
> single anatomical topology mask.
> This is not tabular classification and not a per-slice independent label
> problem. Each example is a variable-depth volumetric array with a 3-D binary
> output. A solver must model spatial continuity across slices, preserve the
> shape of the organ, and also report volume and centroid measurements.
> The public arrays are lossy derivatives of the raw NIfTI files: the 320x320
> in-plane axes are pooled to 64x64, while the original slice count is retained.
> Each public case receives a stable challenge-local HMAC-based identifier and a
> target-aligned orientation transform, contrast remapping, and deterministic
> low-amplitude intensity dither. Private masks are never included in public
> test files. These transforms
> preserve the segmentation task while preventing direct lookup by source ID or
> exact voxel values.
> ## Inputs
> Each row of the input CSV contains:
> | Field | Type | Meaning |
> | --- | --- | --- |
> | id | string | Opaque case ID. Copy it exactly into the submission. |
> | image_file | string | Relative path such as images/case_<opaque-id>.npz. |
> | shape_x, shape_y, shape_z | int | Spatial array dimensions, normally 64, 64, and variable Z. |
> | channels | int | Always 2 for this release. |
> The referenced NPZ has one array named image with shape [64,64,Z,2] and
> floating-point values scaled independently per channel. Training rows also
> contain mask_rle; test rows do not.
> ## Target
> The target is a binary mask where 1 means either source label 1 or source
> label 2, and 0 means background. The mask has shape [64,64,Z]. The
> submission also contains:
> voxel_volume: foreground voxel fraction, foreground_voxels / total_voxels.
> centroid_x, centroid_y, centroid_z: foreground centroid coordinates
> normalized independently to [0,1] by the corresponding axis extent.
> Mask RLE uses space-separated start:length runs in C-order. Starts are
> 1-based. For example, 5:3 20:2 marks flattened positions 5-7 and 20-21.
> ## Evaluation
> The score is out of 10:
> 10 * (
> 0.55 * Dice
> + 0.25 * boundary_F1
> + 0.10 * volume_agreement
> + 0.10 * centroid_agreement
> )
> Definitions:
> Dice = 2 * intersection / (predicted_foreground + true_foreground).
> boundary_F1 is F1 over mask voxels that have at least one empty
> 6-connected neighbor. This rewards the organ boundary rather than only its
> area.
> `volume_agreement = max(0, 1 - abs(predicted_volume - true_volume) /
> true_volume)`.
> `centroid_agreement = max(0, 1 - distance(predicted_centroid,
> true_centroid) / 0.5)` using normalized coordinates.
> All component scores are in [0,1], so the final score is in [0,10].
> Malformed RLE, out-of-range runs, missing IDs, or duplicate IDs fail grading.
> ## Dataset
> The prepared release contains 25 labeled training volumes and 7 unlabeled test
> volumes:
> public/
> ├── images/*.npz
> ├── train.csv
> ├── test.csv
> └── sample_submission.csv
> private/
> └── answers.csv
> The train.csv mask_rle is the merged binary mask. test.csv contains
> the same input fields but omits the mask. answers.csv additionally stores
> the private mask RLE, normalized volume, centroid, shape, and voxel count for
> grader use.
> ## Submission
> Submit submission.csv with exactly one row for every test ID:
> | Column | Type | Description |
> | --- | --- | --- |
> | id | string | Exact ID from test.csv. |
> | mask_rle | string | 1-based row-major start:length runs for the full 3-D mask. |
> | voxel_volume | float | Foreground fraction in [0,1]. |
> | centroid_x | float | Normalized centroid coordinate in [0,1]. |
> | centroid_y | float | Normalized centroid coordinate in [0,1]. |
> | centroid_z | float | Normalized centroid coordinate in [0,1]. |
> Example:
> id,mask_rle,voxel_volume,centroid_x,centroid_y,centroid_z
> mri_abc123,5:3 20:2,0.0831,0.48,0.51,0.44
> What Not To Do
> Do not use private masks, grader files, hidden answers, or manually created test annotations.
> Do not identify original source cases using IDs, voxel fingerprints, metadata, external datasets, or exact-image matching.
> Do not use pretrained medical models, hosted inference APIs, GPUs, TPUs, or any external training data.
> Do not use per-slice independent prediction, fixed templates, threshold rules, ellipses, or handcrafted masks as the complete solution.
> Do not train on, pseudo-label, cluster, calibrate against, or otherwise adapt using the test set or leaderboard feedback.
> The final solution must contain a genuine CPU-only learned model trained exclusively on the released training volumes.
> This challenge is unique and uses deterministically obfuscated 3-D MRI derivatives and requires reconstructing both the prostate topology and its geometric statistics which is not seen in benchmarks.

Inspiration note: Useful as inspiration for route/path reconstruction outputs with explicit evidence structure.
## Anonymous Visual Event Assembly

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c1h34w5pz94zvpmfa52xzqs8ar5pn
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Be the first to climb the leaderboard!

### Full Challenge Description

> Anonymous Visual Event Assembly
> 1. Overview
> Anonymous Visual Event Assembly is a structured computer-vision challenge about reconstructing one synchronized physical event from a shuffled set of wearable-sensor views.
> The source recordings were collected from three body-worn sensor units during ordinary human activity. Each unit recorded:
> Temperature.
> Three-axis acceleration.
> Three-axis angular velocity.
> Three-axis magnetic-field measurements.
> A heart-rate signal was recorded alongside the wearable sensors and is used as a physiological reference.
> Participants are not asked to recognize the underlying activity. The challenge is instead to determine which anonymous sensor fragments were produced during the same 10-second event.
> Each example is presented as one RGB contact-sheet image containing:
> Eight anonymous candidate sensor tiles.
> One heart-rate reference strip.
> Exactly three candidates from the target event.
> Five authentic distractors from other recording windows.
> The three correct candidates come from the three synchronized wearable units that observed the same physical event.
> The five distractors are not synthetic noise or corrupted copies. They are real sensor fragments selected from other events and may closely resemble the target candidates in motion intensity, visual texture, frequency structure, temperature behavior, or missing-data patterns.
> A candidate is correct because it belongs to the same underlying event as the other two correct candidates, not because it simply appears more realistic.
> The model must solve four linked prediction problems:
> Identify the three candidates belonging to the target event.
> Assign those candidates to the anonymous roles role_0, role_1, and role_2.
> Predict the temporal correction required to align each true candidate with the event.
> Estimate the probability that the complete decoded assembly is correct.
> This makes the benchmark different from ordinary image classification, object detection, or independent tile matching.
> 2. Dataset
> A successful system must reason jointly across several image regions, discover cross-sensor compatibility, distinguish convincing alternative events, infer anonymous roles, and recover small timing offsets.
> The dataset contains:
> 7,000 training images.
> 3,000 test images.
> The released participant-facing files are:
> images/
> train.csv
> test.csv
> sample_submission.csv
> The contact-sheet images are the only model inputs.
> Raw sensor arrays, participant identities, source recording identifiers, physical body locations, and activity labels are not released.
> Most wearable-learning benchmarks assume that sensor identity, body location, recording membership, and timing are already known.
> This challenge removes all four assumptions.
> The model receives anonymous sensor views that have been:
> Separated from their original recording.
> Stripped of body-location names.
> Shuffled with fragments from other events.
> Shifted slightly in time.
> Rendered into images rather than supplied as raw arrays.
> The problem is therefore one of latent event reconstruction.
> The model must infer which observations belong together before it can assign their roles or timing.
> Some distractors are deliberately selected to form a convincing competing event. Two distractors may agree strongly with one another while still being unrelated to the heart-rate reference.
> This prevents a solution based only on selecting the most similar pair or the three visually strongest tiles.
> The intended reasoning unit is the complete assembly.
> 3. Real-World Motivation
> Multi-device wearable systems often collect one activity through several synchronized sensors.
> During a movement, one body-worn unit may show strong acceleration while another records a smaller but temporally related response. Their values are not identical, but their transitions and progression are linked because they were generated by the same person during the same event.
> In practical pipelines, sensor fragments can become:
> Detached from their source sessions.
> Stored without location metadata.
> Combined with fragments from other recordings.
> Misaligned by small timing offsets.
> Difficult to distinguish from similar movements.
> Anonymous Visual Event Assembly models this recovery problem.
> For each example:
> The heart-rate strip comes from the target event.
> The three true candidates come from that same event.
> The five distractors come from other valid windows within the same prepared split.
> Participants must reconstruct the synchronized event using only visual evidence.
> 4. Image Layout
> Every contact-sheet image is:
> 1024 pixels wide.
> 384 pixels high.
> RGB.
> Stored in PNG format.
> The upper part contains eight candidate tiles arranged in two rows and four columns.
> Candidate numbering is row-major:
> 0 1 2 3
> 4 5 6 7
> Therefore:
> Candidate 0 is the upper-left tile.
> Candidate 3 is the upper-right tile.
> Candidate 4 is the lower-left tile.
> Candidate 7 is the lower-right tile.
> Candidate positions are randomized independently for every example.
> A position does not reveal:
> Membership.
> Role.
> Source recording.
> Temporal shift.
> Difficulty.
> A horizontal heart-rate reference strip appears beneath the candidate grid.
> 5. Candidate Tile Representation
> Each candidate tile represents one wearable unit during a 10-second recording window.
> A tile contains ten horizontal signal strips:
> One temperature channel.
> Three acceleration channels.
> Three angular-velocity channels.
> Three magnetic-field channels.
> Time runs from left to right.
> The original source window contains 500 temporal samples because the prepared signals use a sample rate of 50 Hz over 10 seconds.
> The channels are normalized using statistics computed from training recordings and rendered as RGB values:
> Positive normalized values move toward red.
> Negative normalized values move toward blue.
> Values near the normalization center appear light.
> Larger magnitudes produce stronger color.
> Missing observations appear black.
> Dark rows separate adjacent channels.
> Participants are not expected to reconstruct the original numerical signals.
> Potentially useful evidence includes:
> Related transitions occurring at similar times.
> Compatible changes in movement intensity.
> Matching starts and endings of repeated motion.
> Cross-candidate frequency structure.
> Similar missing-data timing.
> Patterns that agree only after a small shift.
> Heart-rate behavior supporting one candidate group.
> Distractors that match locally but disagree across the full window.
> 6. Target Event and Distractors
> Every image contains exactly three true event members.
> The three true candidates originate from:
> The same source recording.
> The same 10-second event window.
> Three different wearable units.
> Each member has exactly one anonymous role:
> role_0
> role_1
> role_2
> The physical body locations associated with these roles are intentionally withheld.
> The remaining five candidates have the role distractor.
> All distractors are authentic sensor observations.
> The generator uses matched distractors so that simple color, intensity, or missingness statistics are insufficient.
> Some examples contain a competing distractor pair. Such a pair comes from one alternative event and may be highly compatible internally, but it does not match the target event represented by the heart-rate strip.
> 7. Temporal Alignment
> Each true candidate may be displayed with a small temporal displacement.
> The target shift specifies the correction needed to align the displayed tile with the target event.
> The allowed shift classes are:
> -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5
> Each class represents five original samples.
> At 50 Hz:
> One shift unit equals 0.1 seconds.
> A shift of 2 equals 0.2 seconds.
> A shift of 5 equals 0.5 seconds.
> A shift of -5 equals negative 0.5 seconds.
> A shift of 0 means no correction is required.
> Shift targets apply only to true members.
> Distractors use -99 in train.csv because they do not have a valid alignment with the target event.
> 8. Training Data
> train.csv contains one row per training image.
> Identification columns
> sample_id
> Type: string.
> A unique anonymized example identifier.
> image_file
> Type: string.
> The relative path to the corresponding contact-sheet PNG.
> Membership columns
> member_0
> member_1
> member_2
> member_3
> member_4
> member_5
> member_6
> member_7
> Type: integer.
> A value of 1 means the candidate belongs to the target event. A value of 0 means it is a distractor.
> Exactly three membership values equal 1 in every row.
> Role columns
> role_0
> role_1
> role_2
> role_3
> role_4
> role_5
> role_6
> role_7
> Type: string.
> Each value is one of:
> role_0
> role_1
> role_2
> distractor
> Every row contains exactly one candidate for each true role and exactly five distractors.
> Shift columns
> shift_0
> shift_1
> shift_2
> shift_3
> shift_4
> shift_5
> shift_6
> shift_7
> Type: integer.
> True members use values from -5 through 5.
> Distractors use -99.
> 9. Test Data
> test.csv contains:
> sample_id
> image_file
> Participants must submit predictions for every test row.
> Each test image follows the same structural rules:
> Eight candidates.
> Exactly three true members.
> One member for each anonymous role.
> Five authentic distractors.
> One heart-rate reference.
> One shift target for each true member.
> 10. Evaluation
> The final score contains four components:
> Membership Utility.
> Assignment Utility.
> Alignment Utility.
> Assembly Utility.
> The final score is the weighted geometric mean:
> Final Score =
> 100 ×
> Membership Utility^0.25 ×
> Assignment Utility^0.25 ×
> Alignment Utility^0.20 ×
> Assembly Utility^0.30
> Every probability used in a logarithmic calculation is clipped to:
> [0.000001, 0.999999]
> There are no hidden metric components or difficulty multipliers.
> 10.1 Exact-Accuracy Continuity Correction
> Each component combines a probability-based utility with an exact-decoding accuracy.
> On a finite evaluation set, an otherwise informative submission may produce zero fully exact predictions for a particularly strict component. To prevent one zero exact count from forcing the complete geometric-mean score to zero, the evaluator applies a half-observation continuity correction.
> For an exact-decoding metric, let:
> C be the number of correct exact predictions.
> N be the total number of predictions evaluated by that exact metric.
> The raw exact accuracy is:
> Exact Accuracy = C / N
> The exact accuracy used when calculating the component utility is:
> Adjusted Exact Accuracy =
> max(
> Exact Accuracy,
> 0.5 / N
> )
> The correction changes the utility only when the raw exact accuracy is zero.
> When at least one exact prediction is correct, the adjusted exact accuracy is identical to the raw exact accuracy.
> The raw exact accuracy remains the official exact-decoding statistic. The adjusted value is used only inside the component-utility formula.
> For Membership Utility, Assignment Utility, and Assembly Utility, N is the number of evaluated images.
> For Alignment Utility, N is the number of evaluated true members. Because every image contains exactly three true members, this is three times the number of evaluated images.
> 10.2 Membership Utility
> For each image, let the eight submitted membership probabilities be:
> (p_0, p_1, ..., p_7)
> The soft intersection is the sum of the probabilities assigned to the three true members:
> Soft Intersection =
> sum of p_i over candidates whose true membership is 1
> The soft union is:
> Soft Union =
> sum of all eight membership probabilities
> 3
> Soft Intersection
> The per-image soft membership IoU is:
> Soft IoU =
> (Soft Intersection + 0.000001)
> /
> (Soft Union + 0.000001)
> Membership Probability Utility is the mean soft IoU across all evaluated images:
> Membership Probability Utility = mean Soft IoU
> The evaluator also selects the three candidates with the highest membership probabilities.
> Higher probabilities rank first.
> When two or more candidates have equal membership probabilities, the lower candidate index ranks first.
> Exact top-three membership accuracy is the proportion of images for which the selected set exactly equals the three true members.
> Let:
> C_membership be the number of images with an exactly correct top-three member set.
> N_images be the number of evaluated images.
> Then:
> Exact Membership Accuracy =
> C_membership / N_images
> Adjusted Exact Membership Accuracy =
> max(
> Exact Membership Accuracy,
> 0.5 / N_images
> )
> Membership Utility is:
> Membership Utility =
> sqrt(
> Membership Probability Utility
> × Adjusted Exact Membership Accuracy
> )
> 10.3 Assignment Utility
> For every candidate, participants submit probabilities for:
> role_0
> role_1
> role_2
> distractor
> The four probabilities for each candidate must sum to 1 within an absolute tolerance of 0.00001.
> Negative log loss is calculated against the candidate’s true role.
> For a candidate with true role r, the candidate loss is:
> Candidate Role Loss =
> -log(
> clipped probability assigned to r
> )
> Loss is averaged separately for candidates whose true roles are:
> role_0
> role_1
> role_2
> distractor
> Let these four state-level mean losses be:
> L_role_0
> L_role_1
> L_role_2
> L_distractor
> Balanced assignment loss is:
> Balanced Assignment Loss =
> (
> L_role_0
> L_role_1
> L_role_2
> L_distractor
> )
> /
> 4
> Assignment Probability Utility is:
> Assignment Probability Utility =
> exp(-Balanced Assignment Loss)
> The evaluator also decodes the highest-probability role independently for every candidate.
> When two or more role probabilities are equal, ties are resolved using the following order:
> role_0
> role_1
> role_2
> distractor
> An image has an exact assignment only when the decoded role of all eight candidates is correct.
> This requires:
> Exactly one candidate decoded as the correct role_0 member.
> Exactly one candidate decoded as the correct role_1 member.
> Exactly one candidate decoded as the correct role_2 member.
> All five remaining candidates decoded as distractor.
> Let:
> C_assignment be the number of images with all eight role labels correct.
> N_images be the number of evaluated images.
> Then:
> Exact Assignment Accuracy =
> C_assignment / N_images
> Adjusted Exact Assignment Accuracy =
> max(
> Exact Assignment Accuracy,
> 0.5 / N_images
> )
> Assignment Utility is:
> Assignment Utility =
> sqrt(
> Assignment Probability Utility
> × Adjusted Exact Assignment Accuracy
> )
> 10.4 Alignment Utility
> Alignment is scored only for true members.
> For every candidate, participants submit probabilities for the 11 shifts:
> -5
> -4
> -3
> -2
> -1
> 0
> +1
> +2
> +3
> +4
> +5
> The eleven shift probabilities for each candidate must sum to 1 within an absolute tolerance of 0.00001.
> For each true member, alignment loss is the negative logarithm of the submitted probability assigned to the correct shift:
> Member Alignment Loss =
> -log(
> clipped probability assigned to the true shift
> )
> Alignment log loss is the mean member alignment loss across all true members:
> Alignment Log Loss =
> mean Member Alignment Loss
> Alignment Probability Utility is:
> Alignment Probability Utility =
> exp(-Alignment Log Loss)
> The evaluator also decodes the highest-probability shift for every true member.
> When two or more shift probabilities are equal, ties are resolved using the shift order:
> -5, -4, -3, -2, -1, 0, +1, +2, +3, +4, +5
> Therefore, the numerically lowest tied shift is selected.
> Exact shift accuracy is the proportion of true members whose decoded shift exactly equals the target shift.
> Let:
> C_shift be the number of true members with the correct decoded shift.
> N_true_members be the total number of evaluated true members.
> Because every image contains exactly three true members:
> N_true_members = 3 × N_images
> Then:
> Exact Shift Accuracy =
> C_shift / N_true_members
> Adjusted Exact Shift Accuracy =
> max(
> Exact Shift Accuracy,
> 0.5 / N_true_members
> )
> Alignment Utility is:
> Alignment Utility =
> sqrt(
> Alignment Probability Utility
> × Adjusted Exact Shift Accuracy
> )
> Distractor shift predictions do not affect alignment loss or exact shift accuracy.
> However, every distractor must still contain a valid eleven-class probability distribution whose values sum to 1 within the required tolerance.
> 10.5 Assembly Utility
> For each image, the evaluator constructs one decoded assembly.
> The evaluator decodes:
> The three candidates with the highest membership probabilities.
> The highest-probability role for each selected candidate.
> The highest-probability shift for each selected candidate.
> Membership ties are resolved by selecting the lower candidate index first.
> Role ties are resolved in this order:
> role_0
> role_1
> role_2
> distractor
> Shift ties are resolved in this order:
> -5, -4, -3, -2, -1, 0, +1, +2, +3, +4, +5
> The decoded assembly is exactly correct only when all of the following conditions hold:
> The selected candidate set contains exactly the three true members.
> The selected candidate corresponding to role_0 is assigned role_0.
> The selected candidate corresponding to role_1 is assigned role_1.
> The selected candidate corresponding to role_2 is assigned role_2.
> The decoded shift of the role_0 member is correct.
> The decoded shift of the role_1 member is correct.
> The decoded shift of the role_2 member is correct.
> A single incorrect member, role, or shift makes the decoded assembly incorrect.
> For each image, define the assembly target:
> Assembly Target = 1 when the decoded assembly is exactly correct.
> Assembly Target = 0 otherwise.
> Participants submit one p_assembly value for each image.
> Binary log loss is calculated as:
> Assembly Row Loss =
> -[
> Assembly Target × log(clipped p_assembly)
> (1 - Assembly Target)
> × log(1 - clipped p_assembly)
> ]
> Assembly log loss is the mean assembly row loss across all evaluated images:
> Assembly Log Loss =
> mean Assembly Row Loss
> Assembly Probability Utility is:
> Assembly Probability Utility =
> exp(-Assembly Log Loss)
> Exact assembly accuracy is the proportion of images whose complete decoded assembly is exactly correct.
> Let:
> C_assembly be the number of images with an exactly correct decoded assembly.
> N_images be the number of evaluated images.
> Then:
> Exact Assembly Accuracy =
> C_assembly / N_images
> Adjusted Exact Assembly Accuracy =
> max(
> Exact Assembly Accuracy,
> 0.5 / N_images
> )
> Assembly Utility is:
> Assembly Utility =
> sqrt(
> Assembly Probability Utility
> × Adjusted Exact Assembly Accuracy
> )
> The continuity correction prevents zero exact assemblies from automatically forcing the complete competition score to zero. It does not otherwise relax the definition of an exact assembly.
> 10.6 Final Score
> After calculating the four component utilities, the evaluator computes:
> Final Score =
> 100 ×
> Membership Utility^0.25 ×
> Assignment Utility^0.25 ×
> Alignment Utility^0.20 ×
> Assembly Utility^0.30
> The final score is clipped to the range:
> [0, 100]
> A higher score is better.
> 10.7 Submission Validation
> A submission is invalid and receives a score of 0 when any of the following conditions holds:
> The submission is not a valid table.
> A required column is missing.
> An unknown extra column is present.
> A required sample_id is missing.
> An unknown sample_id is included.
> A sample_id appears more than once.
> A sample_id is blank or missing.
> A prediction value is non-numeric.
> A prediction value is NaN or infinite.
> A probability is below 0 or above 1.
> A candidate’s four role probabilities do not sum to 1 within an absolute tolerance of 0.00001.
> A candidate’s eleven shift probabilities do not sum to 1 within an absolute tolerance of 0.00001.
> The submission must contain every test sample_id exactly once.
> Submission row order does not affect scoring.
> 11. Submission Schema
> The submission must contain exactly 130 columns:
> One sample_id.
> Eight membership probabilities.
> Thirty-two role probabilities.
> Eight groups of eleven shift probabilities.
> One p_assembly.
> The membership columns are:
> p_member_0
> p_member_1
> p_member_2
> p_member_3
> p_member_4
> p_member_5
> p_member_6
> p_member_7
> For each candidate i, the role columns are:
> p_candidate_i_role_0
> p_candidate_i_role_1
> p_candidate_i_role_2
> p_candidate_i_distractor
> The fully expanded role-column names are:
> p_candidate_0_role_0
> p_candidate_0_role_1
> p_candidate_0_role_2
> p_candidate_0_distractor
> p_candidate_1_role_0
> p_candidate_1_role_1
> p_candidate_1_role_2
> p_candidate_1_distractor
> p_candidate_2_role_0
> p_candidate_2_role_1
> p_candidate_2_role_2
> p_candidate_2_distractor
> p_candidate_3_role_0
> p_candidate_3_role_1
> p_candidate_3_role_2
> p_candidate_3_distractor
> p_candidate_4_role_0
> p_candidate_4_role_1
> p_candidate_4_role_2
> p_candidate_4_distractor
> p_candidate_5_role_0
> p_candidate_5_role_1
> p_candidate_5_role_2
> p_candidate_5_distractor
> p_candidate_6_role_0
> p_candidate_6_role_1
> p_candidate_6_role_2
> p_candidate_6_distractor
> p_candidate_7_role_0
> p_candidate_7_role_1
> p_candidate_7_role_2
> p_candidate_7_distractor
> For each candidate i, the shift columns are:
> p_candidate_i_shift_-5
> p_candidate_i_shift_-4
> p_candidate_i_shift_-3
> p_candidate_i_shift_-2
> p_candidate_i_shift_-1
> p_candidate_i_shift_0
> p_candidate_i_shift_+1
> p_candidate_i_shift_+2
> p_candidate_i_shift_+3
> p_candidate_i_shift_+4
> p_candidate_i_shift_+5
> The plus sign is part of every positive-shift column name.
> The final column is:
> p_assembly
> Submission requirements:
> Include every sample_id from test.csv exactly once.
> Do not include unknown identifiers.
> Do not omit any test row.
> Use exactly the columns from sample_submission.csv.
> Do not add extra columns.
> Use finite numeric values.
> Keep all probabilities between 0 and 1.
> Make each candidate’s four role probabilities sum to 1.
> Make each candidate’s eleven shift probabilities sum to 1.
> Membership probabilities do not need to sum to 3.
> Row order does not matter.
> 12. Correctly Formatted CSV Example
> The following is a complete one-row CSV example. It contains all 130 required columns and does not use omitted fields or ellipses.
> sample_id,p_member_0,p_member_1,p_member_2,p_member_3,p_member_4,p_member_5,p_member_6,p_member_7,p_candidate_0_role_0,p_candidate_0_role_1,p_candidate_0_role_2,p_candidate_0_distractor,p_candidate_1_role_0,p_candidate_1_role_1,p_candidate_1_role_2,p_candidate_1_distractor,p_candidate_2_role_0,p_candidate_2_role_1,p_candidate_2_role_2,p_candidate_2_distractor,p_candidate_3_role_0,p_candidate_3_role_1,p_candidate_3_role_2,p_candidate_3_distractor,p_candidate_4_role_0,p_candidate_4_role_1,p_candidate_4_role_2,p_candidate_4_distractor,p_candidate_5_role_0,p_candidate_5_role_1,p_candidate_5_role_2,p_candidate_5_distractor,p_candidate_6_role_0,p_candidate_6_role_1,p_candidate_6_role_2,p_candidate_6_distractor,p_candidate_7_role_0,p_candidate_7_role_1,p_candidate_7_role_2,p_candidate_7_distractor,p_candidate_0_shift_-5,p_candidate_0_shift_-4,p_candidate_0_shift_-3,p_candidate_0_shift_-2,p_candidate_0_shift_-1,p_candidate_0_shift_0,p_candidate_0_shift_+1,p_candidate_0_shift_+2,p_candidate_0_shift_+3,p_candidate_0_shift_+4,p_candidate_0_shift_+5,p_candidate_1_shift_-5,p_candidate_1_shift_-4,p_candidate_1_shift_-3,p_candidate_1_shift_-2,p_candidate_1_shift_-1,p_candidate_1_shift_0,p_candidate_1_shift_+1,p_candidate_1_shift_+2,p_candidate_1_shift_+3,p_candidate_1_shift_+4,p_candidate_1_shift_+5,p_candidate_2_shift_-5,p_candidate_2_shift_-4,p_candidate_2_shift_-3,p_candidate_2_shift_-2,p_candidate_2_shift_-1,p_candidate_2_shift_0,p_candidate_2_shift_+1,p_candidate_2_shift_+2,p_candidate_2_shift_+3,p_candidate_2_shift_+4,p_candidate_2_shift_+5,p_candidate_3_shift_-5,p_candidate_3_shift_-4,p_candidate_3_shift_-3,p_candidate_3_shift_-2,p_candidate_3_shift_-1,p_candidate_3_shift_0,p_candidate_3_shift_+1,p_candidate_3_shift_+2,p_candidate_3_shift_+3,p_candidate_3_shift_+4,p_candidate_3_shift_+5,p_candidate_4_shift_-5,p_candidate_4_shift_-4,p_candidate_4_shift_-3,p_candidate_4_shift_-2,p_candidate_4_shift_-1,p_candidate_4_shift_0,p_candidate_4_shift_+1,p_candidate_4_shift_+2,p_candidate_4_shift_+3,p_candidate_4_shift_+4,p_candidate_4_shift_+5,p_candidate_5_shift_-5,p_candidate_5_shift_-4,p_candidate_5_shift_-3,p_candidate_5_shift_-2,p_candidate_5_shift_-1,p_candidate_5_shift_0,p_candidate_5_shift_+1,p_candidate_5_shift_+2,p_candidate_5_shift_+3,p_candidate_5_shift_+4,p_candidate_5_shift_+5,p_candidate_6_shift_-5,p_candidate_6_shift_-4,p_candidate_6_shift_-3,p_candidate_6_shift_-2,p_candidate_6_shift_-1,p_candidate_6_shift_0,p_candidate_6_shift_+1,p_candidate_6_shift_+2,p_candidate_6_shift_+3,p_candidate_6_shift_+4,p_candidate_6_shift_+5,p_candidate_7_shift_-5,p_candidate_7_shift_-4,p_candidate_7_shift_-3,p_candidate_7_shift_-2,p_candidate_7_shift_-1,p_candidate_7_shift_0,p_candidate_7_shift_+1,p_candidate_7_shift_+2,p_candidate_7_shift_+3,p_candidate_7_shift_+4,p_candidate_7_shift_+5,p_assembly
> asm_example001,0.93,0.06,0.91,0.05,0.08,0.94,0.03,0.07,0.97,0.01,0.01,0.01,0.01,0.01,0.01,0.97,0.01,0.97,0.01,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.97,0.01,0.01,0.01,0.01,0.01,0.90,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.90,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.90,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.90,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.90,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.90,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.90,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.90,0.01,0.01,0.01,0.01,0.01,0.84
> In this example:
> Candidates 0, 2, and 5 have the highest membership probabilities.
> Candidate 0 is assigned role_0.
> Candidate 2 is assigned role_1.
> Candidate 5 is assigned role_2.
> The other candidates are assigned distractor.
> Candidate 0 predicts shift 0.
> Candidate 2 predicts shift -2.
> Candidate 5 predicts shift +1.
> p_assembly is 0.84.
> Participants should still use the released sample_submission.csv as the authoritative schema and column-order template.
> 13. Modeling Guidance
> A baseline system may:
> Crop the eight candidate regions.
> Encode every tile with a shared convolutional network.
> Encode the heart-rate strip separately.
> Predict membership, role, and shift distributions.
> Combine candidate representations to predict assembly confidence.
> Stronger approaches may use:
> Vision transformers.
> Set transformers.
> Graph neural networks.
> A competitive system should not treat candidates independently.
> The key question is not merely whether one tile resembles the reference. It is whether three anonymous sensor views jointly describe one coherent 10-second physical event.
> 14. Method Restrictions
> Predictions must be based on the supplied images.
> Predictions may not use:
> sample_id.
> Image filenames.
> CSV row order.
> PNG file size.
> PNG metadata.
> Compression artifacts.
> Hidden answers.
> Hardcoded test predictions.
> External copies of the source recordings.
> The learned visual system must remain the primary prediction method.
> 15. Summary
> Anonymous Visual Event Assembly asks models to reconstruct one synchronized human-movement event from eight authentic but anonymous wearable-sensor fragments.
> The benchmark combines:
> Event membership recovery.
> Anonymous sensor-role assignment.
> Fine temporal alignment.
> Structured confidence estimation.
> Joint reasoning over competing candidate groups.
> The central challenge is not classifying what activity occurred.
> It is discovering which observations belong together, determining how they relate, and reconstructing the hidden synchronized event.

Inspiration note: Useful as inspiration for route/path reconstruction outputs with explicit evidence structure.
## Manuscript Reading-Flow Card Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cvsmd2cc5mx6xpf2x4kgve58ay7m9
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image, feature-engineering, Dataset source is visible after the challenge closes.
- Best/top context: Beat keshav2703's score of 0.665!

### Full Challenge Description

> Overview
> Historical manuscript crops often contain irregular reading flow: uneven baselines, faded strokes, marginal shifts, decorative spacing, and partial lines at crop boundaries. In this task, each row asks you to reconstruct a compact reading-flow record for one transformed manuscript crop.
> The target is a card sequence, not plain text transcription. For every visible writing line, submit its reading-order index, pixel rectangle, center grid cell, length band, height band, and left-margin band. The answer also includes the total line count and the set of occupied center cells, so the record must stay consistent across ordering, geometry, and page-position summaries.
> Dataset
> The released files are:
> train.csv: 564 labeled examples with images, public context, output schema, and answer_json.
> test.csv: 313 unlabeled examples with the same public fields except answer_json.
> sample_submission.csv: A valid low-signal example submission.
> images/: Transformed manuscript crop images referenced by train.csv and test.csv.
> Columns:
> id (string): Row identifier.
> image (string): Relative path to the manuscript crop image.
> prompt (string): Fixed task instruction for the row.
> context_json (JSON string): Public crop metadata with image_width, image_height, grid_rows, and grid_cols.
> answer_format_json (JSON string): Required output schema and allowed band values.
> answer_json (JSON string, train only): Ground-truth reading-flow card record with line_count, line_cards, and occupied_center_cells.
> Each line_cards item has:
> order (integer): Reading-order index, starting at 0 from the top visible line.
> bbox (list of four integers): [x, y, width, height] in image pixels.
> center_cell (string): Center location on the 18 by 24 grid, formatted like r07_c12.
> length_band (string): One of short, medium, long, or wide.
> height_band (string): One of thin, regular, tall, or very_tall.
> left_margin_band (string): One of outer, near, middle, or inner.
> Evaluation
> The score is the mean row score over the test rows used for scoring. All row scores are between 0 and 1.
> For a row:
> row_score =
> 0.18 * count_score
> + 0.52 * geometry_score
> + 0.18 * center_cell_f1
> + 0.12 * band_score
> Definitions:
> count_score = exp(-abs(predicted_line_count - true_line_count) / 3).
> Lines are compared by their order index after sorting predicted and true line_cards by order.
> For each comparable ordered line, line_geometry = 0.65 * bbox_iou + 0.35 * center_distance_score.
> bbox_iou = intersection_area / union_area for the predicted and true pixel rectangles.
> center_distance_score = exp(-pixel_center_distance / 26).
> geometry_score is the sum of comparable line_geometry values divided by the true line count. Missing predicted lines contribute 0.
> center_cell_f1 is standard set F1 between predicted and true occupied_center_cells: 2 * precision * recall / (precision + recall), with precision and recall computed over grid-cell strings.
> For each comparable ordered line, compute line_band_match = (length_band_exact + height_band_exact + left_margin_band_exact + center_cell_exact) / 4.
> band_score = sum(line_band_match over comparable ordered lines) / max(1, true_line_count). Missing predicted lines contribute 0.
> Malformed answer_json values score 0 for that row. Submissions with wrong columns, duplicate ids, missing ids, or extra ids are rejected.
> Submission
> Submit a CSV with exactly two columns:
> id (string)
> answer_json (JSON string)
> Example:
> id,answer_json
> page_example_001,"{""line_count"":2,""line_cards"":[{""order"":0,""bbox"":[42,35,510,28],""center_cell"":""r03_c09"",""length_band"":""wide"",""height_band"":""regular"",""left_margin_band"":""outer""},{""order"":1,""bbox"":[45,91,498,31],""center_cell"":""r06_c09"",""length_band"":""wide"",""height_band"":""regular"",""left_margin_band"":""outer""}],""occupied_center_cells"":[""r03_c09"",""r06_c09""]}"
> page_example_002,"{""line_count"":1,""line_cards"":[{""order"":0,""bbox"":[80,60,360,24],""center_cell"":""r05_c10"",""length_band"":""long"",""height_band"":""thin"",""left_margin_band"":""near""}],""occupied_center_cells"":[""r05_c10""]}"
> What Not To Use
> Do not use GPU acceleration.
> Do not use external datasets, pretrained checkpoints, OCR services, manuscript-layout APIs, or external page matching.
> Do not manually search for held-out manuscript pages or line annotations outside the released files.
> Do not hard-code test ids or memorize the sample submission.
> Do not install packages at runtime, include additional model checkpoints or weights, use non-public or gated assets, or load remote code such as torch.hub or trust_remote_code.
> Do not submit malformed JSON, extra rows, missing rows, duplicate ids, or additional columns.

Inspiration note: Useful for ordered trace reconstruction instead of isolated per-item prediction.
## Slot-Constrained Certificate Fragment Provenance

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx742pdmv49kmc7n472mp0k5ax8ayv7e
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, image, small-data, multimodal, Dataset source is visible after the challenge closes.
- Best/top context: Be the first to climb the leaderboard!

### Full Challenge Description

> Overview
> Aviation release certificates contain dense combinations of tables, field labels, signatures, stamps, serial references, dates, approval information, and maintenance statements.
> In this challenge, each episode contains one certificate image with two to four informative horizontal document strips removed. Every removed strip is labeled with a gap identifier such as:
> G0
> G1
> G2
> G3
> A separate candidate bank contains fixed-size candidate strip images labeled with episode-local aliases such as:
> C0
> C1
> C2
> C3
> Some candidate strips originated from the masked certificate. Others are visually or textually similar distractors drawn from different held-out documents.
> Your task is to assign the correct candidate strip to every masked gap.
> Some episodes intentionally omit one required strip. For that individual gap, the correct assignment is:
> NONE
> The task is a constrained document-fragment provenance problem. It is not ordinary OCR, document classification, free-form image inpainting, question answering, or top-k retrieval.
> Core Task
> For every test episode, predict one assignment for each labeled gap.
> Example candidate bank:
> C0, C1, C2, C3, C4
> For a row with gap_count=3, an example prediction is:
> PATCHMAP=G0:C4>G1:C1>G2:NONE
> This means:
> Candidate C4 belongs in gap G0.
> Candidate C1 belongs in gap G1.
> The correct strip for G2 is absent from the candidate bank.
> Candidate aliases are episode-specific.
> C0 in one row has no relationship to C0 in another row.
> The same candidate alias cannot be assigned to more than one gap.
> What Provenance Means
> Strip provenance identifies which candidate strip originated from each removed location in the query document.
> The correct assignment may depend on:
> Surrounding table borders
> Nearby field labels
> Typography
> Character spacing
> Line continuity
> Document layout
> Stamps and signatures
> Background texture
> OCR content when available
> Relative vertical position
> Global one-to-one consistency across gaps
> A candidate can look plausible in isolation but still be incorrect because it does not align with the surrounding structure of the target gap.
> Distractors may contain:
> Similar certificate layouts
> Similar field names
> Similar serial or part-number patterns
> Similar dates
> Similar table boundaries
> Similar stamps
> Similar organization names
> Similar scan artifacts
> The task therefore requires learned document-strip matching rather than simple filename lookup, exact text matching, or fixed templates.
> Image Construction
> Query images preserve the overall certificate page while replacing two to four informative horizontal strips with labeled masks.
> Candidate strips are placed on a common fixed-size canvas. Raw candidate dimensions therefore do not directly reveal the matching gap.
> Low-information regions containing almost only white space, scanner margins, or negligible document content are excluded before episode generation.
> Query images and candidate strips receive separate deterministic image degradation, which may include mild contrast, brightness, blur, and noise variation.
> OCR Evidence
> cards.csv includes an ocr_text field for each candidate strip.
> The OCR field contains text extracted or associated with the same vertical source region when usable text is available.
> When no usable text is available, the value is:
> [NO_EXTRACTED_TEXT]
> OCR is noisy auxiliary evidence and must not be treated as guaranteed transcription.
> Solvers may use:
> Candidate images only
> OCR text only
> Both image and OCR evidence
> A strong solution is expected to combine visual compatibility with textual evidence when the text is available.
> Missing-Strip Cases
> Some episodes contain exactly one gap whose correct source strip is not present in the candidate bank.
> For that individual gap, submit:
> NONE
> Example:
> PATCHMAP=G0:C3>G1:NONE>G2:C0
> Every gap must still appear in the prediction.
> A prediction may use NONE at most once.
> Prepared Dataset
> The public dataset contains only files required for solving:
> train.csv
> test.csv
> cards.csv
> sample_submission.csv
> train_queries/
> test_queries/
> train_cards/
> test_cards/
> No source-document copies, debug reports, benchmark outputs, intermediate manifests, or private labels are included.
> train.csv
> The training file contains:
> sample_id
> group_id
> query_card_path
> candidate_cards
> gap_count
> target
> sample_id
> A content-free training identifier.
> Do not use sample_id as a predictive feature.
> group_id
> A content-free grouping identifier for leakage-safe validation.
> Rows sharing a source-document component have the same group_id.
> For local validation, all rows with the same group_id must remain in one fold.
> Do not use group_id as a predictive feature.
> query_card_path
> The relative path to the masked certificate image.
> candidate_cards
> A JSON list of episode-local candidate aliases.
> Example:
> ["C0","C1","C2","C3","C4"]
> gap_count
> The number of masked strips in the query image.
> Valid gap identifiers are:
> G0 through G(gap_count - 1)
> target
> The canonical strip-to-gap assignment program.
> Example:
> PATCHMAP=G0:C4>G1:C1>G2:NONE
> test.csv
> The test file contains:
> sample_id
> query_card_path
> candidate_cards
> gap_count
> The target and grouping metadata are not provided for test rows.
> cards.csv
> The candidate-strip index contains:
> sample_id
> candidate_alias
> image_path
> ocr_text
> sample_id
> Identifies the episode to which the candidate belongs.
> candidate_alias
> The episode-local alias, such as C0 or C4.
> image_path
> The relative path to the fixed-size candidate strip image.
> ocr_text
> Noisy auxiliary text associated with the candidate strip, or [NO_EXTRACTED_TEXT] when unavailable.
> Candidate aliases are meaningful only within one episode.
> Cards from different episodes must not be joined using their aliases.
> Train and Test Separation
> Source-document splitting occurs before episode generation.
> The preparation pipeline enforces:
> Source-document-disjoint train and test groups
> No original source document appearing in both train and test
> Separate private query-document and distractor-document pools
> No exact source strip reused across private test candidate cards
> No query image reused across train and test
> No candidate image path reused across private test rows
> Fresh candidate alias permutation for every episode
> No original filename exposed
> No original repository index exposed
> No stable source ordering exposed
> No private target stored in public files
> Fixed candidate canvas dimensions
> Removal of low-information candidate strips
> Each test episode must be processed independently.
> Submission Format
> Submit exactly two columns in this order:
> sample_id,prediction
> For a row with gap_count=3:
> TE000000,PATCHMAP=G0:C4>G1:C1>G2:NONE
> For a row with gap_count=2:
> TE000001,PATCHMAP=G0:C2>G1:C0
> The complete CSV begins with:
> sample_id,prediction
> The submission must contain exactly one row for every test sample_id.
> The submitted ID set must exactly match the test ID set.
> Duplicate, missing, unknown, or extra IDs are invalid.
> Extra columns are invalid.
> Prediction Grammar
> Every prediction must begin with:
> PATCHMAP=
> Every gap must appear exactly once.
> Assignments must be sorted by increasing gap index.
> Each assignment must use:
> G<gap_index>:<candidate_alias_or_NONE>
> Assignments must be separated by:
> >
> Valid examples:
> PATCHMAP=G0:C2>G1:C4
> PATCHMAP=G0:C1>G1:NONE>G2:C3
> Invalid examples:
> PATCHMAP=G1:C2>G0:C4
> PATCHMAP=G0:C2>G1:C2
> PATCHMAP=G0:MISSING>G1:C4
> CHAIN=C2>C4
> PATCHMAP=G0:C99>G1:C1
> PATCHMAP=G0:C2>G2:C4
> Rules:
> Every required gap must be present.
> Gaps must be consecutive from G0.
> Every submitted alias must belong to that row's candidate list.
> A candidate alias may not be assigned more than once.
> NONE may be used at most once.
> Whitespace is not permitted inside the prediction program.
> Evaluation
> Each gap is scored independently.
> For one gap:
> GapScore = 1
> when the predicted candidate alias or NONE exactly matches the target.
> Otherwise:
> GapScore = 0
> For one row:
> RowScore = mean GapScore over all gaps in that row
> The final score is:
> Score = mean RowScore over all test rows
> The score is finite and bounded to:
> [0, 1]
> Higher is better.
> A perfect submission scores exactly:
> 1.0
> No baseline subtraction or post-processing normalization is applied.
> A row with three gaps and two correct assignments receives:
> 2 / 3
> Allowed Approaches
> The following are allowed:
> Training a gap-conditioned visual matcher
> Fine-tuning a compact pretrained visual encoder
> Fine-tuning a compact pretrained text encoder
> Fine-tuning a compact multimodal model
> Training a cross-encoder over query-gap context and candidate strips
> Learning pairwise or listwise ranking objectives
> Learning one-to-one assignment scores
> Using OCR text provided in cards.csv
> Reading candidate images directly
> Combining visual and textual representations
> Using general-purpose pretrained backbones as initialization
> Fine-tuning those backbones inside the submitted solution
> Using character-level models for noisy OCR
> Using learned bipartite matching or constrained decoding
> Using grouped validation based on group_id
> Ensembling models trained inside the same end-to-end script
> Applying test-time augmentation independently to one episode
> Using lexical matching or regex only as auxiliary features beside a genuinely trained model
> Using deterministic parsing for loading, validation, and submission formatting
> A compliant solution must include genuine model training or fine-tuning inside the submitted script.
> A fully frozen or entirely handwritten pipeline is not sufficient.
> Prohibited Approaches
> The following are prohibited:
> Looking up original certificates using visible text, serial numbers, organization names, dates, filenames, or other fingerprints
> Searching public websites, external aviation repositories, or cached source copies
> Matching prepared strips back to the original document collection
> Using any external dataset
> Loading challenge-specific weights trained outside the submitted script
> Using hosted inference APIs
> Installing packages or repositories at runtime
> Hardcoding assignments, coefficients, embeddings, or private-label information
> Using sample_id, group_id, filename order, row order, or alias numbering as predictive features
> Aggregating information across test episodes
> Building a retrieval index jointly over the complete test set
> Cross-test clustering
> Cross-row nearest-neighbour matching
> Test-set fitting
> Test-time pseudo-labeling
> Test-distribution calibration
> Generating additional synthetic training data
> Solving the task entirely with handwritten rules, templates, OCR regex, or fixed similarity thresholds
> Treating OCR strings as guaranteed ground truth
> Reusing one candidate alias for multiple gaps
> Submitting malformed, partial, duplicated, or out-of-vocabulary assignments
> Each test episode must be processed independently.
> Compute Constraints
> Solutions must follow these constraints:
> CPU computation only
> Maximum runtime of 90 minutes
> Ten CPU cores
> 62.5 GiB RAM
> No GPU or CUDA
> No hosted APIs
> No external datasets
> No runtime package installation
> No runtime repository installation
> Only libraries already available in the execution environment may be used
> Training and inference must occur in one end-to-end script
> The final submission must be written to:
> ./working/submission.csv
> Recommended Modeling Directions
> Promising approaches include:
> Query-gap-conditioned candidate encoders
> Siamese strip matching
> Compact CNN feature pyramids
> Character-aware OCR encoders
> Text-image late fusion
> Cross-attention between gap context and strip content
> Learned visual boundary compatibility
> One-to-one bipartite assignment
> Hungarian decoding over learned scores
> Constrained beam search
> Group-disjoint cross-validation
> Fold-bagged inference
> A strong model should combine local visual compatibility, OCR content, document layout, and global assignment consistency.
> Independent nearest-neighbour matching may recover plausible candidates but fail when several strips share similar layouts or when one-to-one assignment matters.
> Novelty and Originality
> This is a slot-constrained multimodal document-strip provenance benchmark.
> It does not ask a model to retrieve supporting passages, answer a question, verify a claim, transcribe a form, classify a document, or generate missing pixels.
> Each episode presents a certificate with multiple labeled horizontal strip gaps and an episode-local bank of fixed-canvas candidate strips.
> The model must reconstruct a one-to-one mapping from gaps to source strips while detecting when one required strip is absent.
> Unlike multi-hop RAG benchmarks, the target is not a set or sequence of supporting passages.
> It is a constrained bipartite provenance assignment grounded jointly in:
> Document layout
> Surrounding visual context
> Noisy optional OCR
> Boundary and line continuity
> Cross-gap consistency
> Missing-strip detection
> Unlike image inpainting, the model does not generate pixels.
> Unlike ordinary retrieval, every output must satisfy a structured one-to-one assignment across multiple gaps.
> Unlike conventional jigsaw tasks, the candidate bank contains semantically and visually similar distractors from related certificate layouts, and candidate dimensions are normalized so raw shape does not directly reveal the answer.
> The hidden target is generated from episode-specific source-strip provenance and does not exist as a public annotation in any source document.

Inspiration note: Useful for provenance-ledger tasks where every fragment must be linked and justified.
## Exposure-Controlled Fluorescence Conservation Routing

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71cnt7bg1fyzgkg0ys6368s18ajv4h
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, image, Dataset source is visible after the challenge closes.
- Best/top context: Be the first to climb the leaderboard!

### Full Challenge Description

> Overview
> Use three microscopy panels to identify one local fluorescence change while ignoring a global exposure change.
> Every image packet shows the same four tracked cells in three panels:
> BASELINE shows the starting image.
> OBSERVED contains a global exposure change and one local event.
> EXPOSURE CONTROL contains the same global exposure change but no local event.
> Comparing OBSERVED with BASELINE alone is misleading because both local biology and camera exposure can change brightness. The EXPOSURE CONTROL reveals the camera-wide change. After accounting for it, predict where local signal was gained or lost, whether one cell moved, and the route taken by the event.
> Submit four linked outputs:
> | Output | What to predict |
> |---|---|
> | `signal_route_graph` | One canonical token describing the local route. |
> | `compartment_budget_matrix` | Signal gain or loss for cells A-D and channels R-G-B. |
> | `support_shift_matrix` | Movement direction for cells A-D. |
> | `budget_state` | The event family. |
> The backgrounds are real multi-channel fluorescence microscopy fields with instance masks. Controlled exposure changes and local events are applied to four tracked cells. Complete source fields are separated between train and test. The challenge is designed for CPU execution within 1.5 hours on 10 CPU cores.
> Scientific Decision Setting
> In longitudinal microscopy, a brighter region does not automatically indicate local signal gain. A global exposure increase can brighten every compartment at once, while a local biological event changes only selected cell-channel compartments. The packet therefore includes a matched exposure control generated with the same channel-wide gain as OBSERVED. This panel acts as a visual control measurement, not as another independent view.
> The required answer is a compact conservation record. A cell-to-cell event must identify one loss and one gain in the same channel. A channel-spillover event must identify one loss and one gain inside the same cell. An environment exchange has only one visible endpoint because the other endpoint lies outside the four tracked cells. A support relocation changes position but leaves the signal budget at zero.
> These constraints make the outputs mutually meaningful. The route states what happened, the budget matrix states where signal changed, the shift matrix handles physical movement, and the state identifies which conservation rule applies. A model cannot solve the complete task by predicting a bright cell or a single event class.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `public/train.csv` | 1,440 labeled packets from 120 source fields. |
> | `public/test.csv` | 432 unlabeled packets from 36 held-out fields. |
> | `public/sample_submission.csv` | Placeholder predictions in the required schema. |
> | `public/images/` | 1,872 JPEG packets, each `1488 x 548` pixels. |
> Train and test share no source field, source image-mask pair, image hash, filename, or case ID.
> Image Layout
> Each packet contains three 480 x 480 panels arranged from left to right:
> BASELINE | OBSERVED | EXPOSURE CONTROL
> Letters A, B, C, and D mark the same tracked cells in every panel. Marker lines and letter colors identify correspondence only. They do not reveal the event type or direction.
> R, G, and B refer to the three displayed fluorescence channels. They are image-channel codes, not fixed biological stain names.
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque 24-character identifier with no target meaning. |
> | `image_path` | string | Relative path to the three-panel JPEG. |
> | `budget_request` | string | Fixed instruction to remove exposure drift and recover the local event. It contains no case-specific answer. |
> Example input:
> case_id,image_path,budget_request
> 7a732f3cf227ac90c06548b8,images/7a732f3cf227ac90c06548b8.jpg,"Use the exposure control to separate acquisition drift from compartment signal flow and support motion."
> Target Columns
> | Column | Data type | Valid structure |
> |---|---|---|
> | `signal_route_graph` | string | One route token, at most 80 characters. |
> | `compartment_budget_matrix` | JSON integer matrix | Shape `4 x 3`; values `-2`, `0`, or `2`. |
> | `support_shift_matrix` | JSON integer matrix | Shape `4 x 2`; values `-1`, `0`, or `1`. |
> | `budget_state` | categorical string | One of four documented states. |
> Output Meaning
> Signal Route
> signal_route_graph is one route string, not an arbitrary graph. The valid forms are:
> | Form | Meaning |
> |---|---|
> | `A:R>B:R:2` | Signal moved between two different cells in one channel. |
> | `ENV>A:R:2` | Signal entered a tracked cell from outside the four cells. |
> | `A:R>ENV:2` | Signal left a tracked cell. |
> | `A:R>A:G:2` | Signal moved between two different channels in one cell. |
> | `A:support>right_down:1` | Cell A moved right and down. |
> Cell letters may be A through D. Channel letters may be R, G, or B. Movement directions are left_up, left_down, right_up, and right_down.
> For cell-to-cell transfer, the cells must differ and the channel must match. For channel transfer, the cell must match and the channels must differ.
> Compartment Budget Matrix
> Rows are cells A, B, C, D. Columns are channels R, G, B.
> | Value | Meaning after exposure correction |
> |---:|---|
> | `-2` | Local signal loss. |
> | `0` | No local signal change. |
> | `2` | Local signal gain. |
> Example for signal moving from cell A to cell C in channel R:
> [[-2,0,0],[0,0,0],[2,0,0],[0,0,0]]
> conserved_transfer and channel_spillover contain one -2 and one 2. reservoir_exchange contains one nonzero entry. support_relocation has an all-zero budget matrix.
> Support Shift Matrix
> Rows are cells A, B, C, D. Columns are horizontal movement followed by vertical movement.
> | Value | Horizontal column | Vertical column |
> |---:|---|---|
> | `-1` | left | up |
> | `0` | no movement | no movement |
> | `1` | right | down |
> Example for cell C moving right and up:
> [[0,0],[0,0],[1,-1],[0,0]]
> Only support_relocation has movement. Exactly one cell has two nonzero direction entries.
> Budget State
> | Value | Meaning |
> |---|---|
> | `conserved_transfer` | Signal moves between two cells in one channel. |
> | `reservoir_exchange` | Signal enters from or leaves to the environment. |
> | `channel_spillover` | Signal moves between two channels in one cell. |
> | `support_relocation` | One tracked cell moves while its signal budget remains unchanged. |
> State Distribution
> | State | Train | Test |
> |---|---:|---:|
> | `conserved_transfer` | 360 | 108 |
> | `reservoir_exchange` | 360 | 108 |
> | `channel_spillover` | 360 | 108 |
> | `support_relocation` | 360 | 108 |
> Submission Format
> Write predictions to exactly:
> ./working/submission.csv
> Required columns, in this exact order:
> case_id,signal_route_graph,compartment_budget_matrix,support_shift_matrix,budget_state
> Example:
> case_id,signal_route_graph,compartment_budget_matrix,support_shift_matrix,budget_state
> 7a732f3cf227ac90c06548b8,A:R>C:R:2,"[[-2,0,0],[0,0,0],[2,0,0],[0,0,0]]","[[0,0],[0,0],[0,0],[0,0]]",conserved_transfer
> Every hidden ID must appear exactly once. Missing, extra, duplicated, or reordered columns are rejected. Duplicate, missing, or unknown IDs and incorrect row counts are rejected. Route and matrix strings are length-capped before parsing. A malformed field receives zero for its component.
> Evaluation
> The Fluorescence Budget Score is:
> Score = 0.45 * CompartmentBudgetScore
> + 0.25 * SignalRouteScore
> + 0.20 * SupportShiftScore
> + 0.10 * BudgetStateScore
> Minimum score: 0.0
> Maximum score: 1.0
> Higher is better.
> CompartmentBudgetScore
> This component is evaluated on the 324 hidden cases with a nonzero true budget. Let I(condition) equal 1 when the condition is true and 0 otherwise.
> entry_agreement = sum(I(Y[i,j] = P[i,j])) / 12
> case_score = 0.05 * entry_agreement + 0.95 * I(Y = P)
> CompartmentBudgetScore = mean(case_score over the 324 active cases)
> The all-zero budget matrices in support_relocation cases are validated for shape and range but excluded from this component.
> SignalRouteScore
> The submitted route must satisfy the documented grammar. A hidden case scores 1 when the complete route equals the true route and 0 otherwise.
> SignalRouteScore = mean(exact route match over all 432 hidden cases)
> SupportShiftScore
> This component is evaluated on the 108 hidden support_relocation cases.
> entry_agreement = sum(I(Y[i,j] = P[i,j])) / 8
> case_score = 0.05 * entry_agreement + 0.95 * I(Y = P)
> SupportShiftScore = mean(case_score over the 108 movement cases)
> All-zero support matrices in the other states are validated for shape and range but excluded from this component.
> BudgetStateScore
> Recall is computed separately for each of the four equally represented states. BudgetStateScore is the mean of those four recalls, which is balanced accuracy.
> What Makes This Interesting
> Ordinary microscopy benchmarks usually segment cells, classify phenotypes, track motion, or compare two frames. This challenge asks a different question: which apparent changes remain after a matched acquisition control is used to remove global channel drift?
> The third panel changes the reasoning unit from visual difference to controlled attribution. A solver must estimate the shared exposure effect, remove it conceptually, assign the remaining change to labeled compartments, and express that change under a conservation rule. Physical relocation is deliberately included as a competing explanation because movement can create a large pixel difference without any signal gain or loss.
> The final answer is therefore not a collection of unrelated labels. It is a structured account of a local event with an origin, destination, signed channel budget, movement exception, and conservation family. This control-mediated accounting formulation is the central challenge.
> Suitable CPU Methods
> Suitable approaches include panel comparison, exposure-ratio estimation, local image statistics, compact image encoders, difference features, and constrained decoding. Local validation should keep complete microscopy fields together.
> What Not To Use
> Do not infer outputs from IDs, filenames, CSV order, hashes, fixed file size, or filesystem order.
> Do not match packets against external copies of source images or masks.
> Do not use source filenames, stain strings, repository split membership, or memorized source-to-target mappings.
> Do not exploit duplicate rows, malformed structures, parser limits, extra columns, private answers, or leaderboard feedback.

Inspiration note: Useful for active/budgeted evidence-acquisition challenge designs with reconstruction outputs.
## Palm-Leaf Reading Paths

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx731zz3z0m8qsxrz8hnzf84yh8b0wg2
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Beat data47's score of 0.530!

### Full Challenge Description

> Palm-Leaf Reading Paths
> Overview
> Palm-leaf OCR needs more than a foreground mask: a recognizer must know where each line begins, how it bends across a damaged leaf, and which line comes next. Archive systems can estimate that layout cheaply from normalized preview images before running expensive high-resolution recognition. Predict the ordered reading paths of handwritten lines in real palm-leaf manuscript previews.
> Each target path records its horizontal extent and sixteen vertical centerline knots. This structured target differs from ordinary pixel segmentation: it rewards usable line geometry, continuity, and reading order while remaining compact enough for CPU inference. The private set contains two complete manuscripts absent from training. No image, page sibling, or manuscript group crosses that boundary.
> Dataset
> File descriptions
> train.csv — Labeled page records with anonymous manuscript groups and ordered reading paths.
> test.csv — Held-out page records without reading paths.
> train/ — Normalized low-resolution previews of real manuscript photographs referenced by train.csv.
> test/ — Normalized low-resolution previews of real manuscript photographs referenced by test.csv.
> sample_submission.csv — Submission template containing random valid paths rather than zero placeholders.
> Column descriptions
> id (string, train and test) — Opaque page identifier.
> image_path (string, train and test) — CWD-relative path inside the public dataset.
> width (integer, train and test) — Prepared image width in pixels.
> height (integer, train and test) — Prepared image height in pixels.
> document_group (string, train only) — Anonymous manuscript group for leakage-safe validation.
> paths_json (string, train only; predict for test) — Top-to-bottom JSON list of reading-path objects.
> Each reading-path object contains exactly:
> x0 (number) — Normalized left endpoint in [0, 1).
> x1 (number) — Normalized right endpoint in (x0, 1].
> y (list of 16 numbers) — Normalized vertical centerline coordinates at equally spaced positions from x0 to x1.
> Example label:
> [{"x0":0.06152,"x1":0.93431,"y":[0.2381,0.2402,0.243,0.2441,0.246,0.2482,0.2511,0.253,0.2542,0.256,0.2571,0.259,0.2612,0.263,0.2641,0.266]}]
> Evaluation
> The Reading Path Utility Score matches predicted and human paths with an optimal one-to-one assignment. It combines centerline geometry, local curvature, horizontal coverage, and line count:
> geometry = exp(-mean_absolute_y_error / 0.035)
> curvature = exp(-mean_absolute_first_difference_error / 0.018)
> extent = exp(-mean_endpoint_error / 0.06)
> # Each matched component is converted to a soft F1 over true and predicted paths.
> score = (
> 0.55 * geometry_soft_f1
> + 0.20 * curvature_soft_f1
> + 0.15 * extent_soft_f1
> + 0.10 * count_ratio
> )
> Higher is better. The score is bounded from 0 to 1. Geometry has the largest weight because centerline placement drives OCR crops; curvature prevents flat-line shortcuts, extent penalizes truncated reading lanes, and count rewards operationally complete page layouts.
> Submission
> Submit one ordered JSON path list for every test page.
> id (string) — Identifier copied exactly from test.csv.
> paths_json (string) — JSON list containing 1 to 24 valid reading paths.
> Example with real test IDs:
> id,paths_json
> pl_0045435be6a5,"[{""x0"":0.08,""x1"":0.92,""y"":[0.20,0.20,0.21,0.21,0.21,0.22,0.22,0.22,0.23,0.23,0.23,0.24,0.24,0.24,0.25,0.25]}]"
> pl_0055f9168ad7,"[{""x0"":0.07,""x1"":0.94,""y"":[0.34,0.34,0.34,0.35,0.35,0.35,0.36,0.36,0.36,0.37,0.37,0.37,0.38,0.38,0.38,0.39]}]"
> Requirements
> Include exactly the columns id,paths_json and one row per test ID.
> Use exactly the keys x0, x1, and y in every path object.
> Supply exactly 16 finite normalized y values per path.
> Require 0 <= x0 < x1 <= 1.
> Order paths strictly from top to bottom by mean y.
> Include between 1 and 24 paths per page.
> Do not identify test pages against the source archive or retrieve source masks.
> Prohibited Methods
> Do not retrieve, reconstruct, cache, or register source masks for test pages.
> Do not identify public pages against source mirrors, or any outside archive.
> Do not use external training datasets, generated synthetic training examples, private labels, hardcoded answers, or test-time adaptation over the test distribution.

Inspiration note: Useful for ordered route/workflow reconstruction outputs with explicit consistency constraints.
## Highway Platoon Signature Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7e3g1bg1j7krxfy0b0rb49gn8b1v0z
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Be the first to climb the leaderboard!

### Full Challenge Description

> Highway Platoon Signature Reconstruction
> Overview
> Low-bandwidth roadside sensors often transmit privacy-reduced signatures instead of identifiable vehicle photographs. Reconstruct the ordered vehicle-type sequence represented by each overhead traffic panel.
> Every panel contains four to seven cards arranged left to right in overhead scan order. A card summarizes one real vehicle using 16 dithered sensor channels. Predict one token per card, preserving that order. Training panels come from earlier capture sessions; test panels come from a later session with different traffic and imaging conditions.
> The allowed tokens are CAR, HATCHBACK, PICKUP, SEDAN, SUV, TRAILER, TRUCK, and VAN.
> Dataset
> File descriptions
> train.csv — labeled training rows.
> test.csv — unlabeled test rows.
> train/ — training PNG signature panels.
> test/ — test PNG signature panels.
> sample_submission.csv — a valid random submission template.
> Column descriptions
> train.csv contains:
> id — unique 16-character panel identifier.
> image_path — path to the panel relative to the dataset public directory.
> vehicle_sequence — ordered vehicle tokens separated by >.
> test.csv contains:
> id — unique 16-character panel identifier.
> image_path — path to the panel relative to the dataset public directory.
> Card encoding
> Each card is 72 pixels wide and 80 pixels high. The central 64-by-64 area is a 4-by-4 grid; lighter cells represent larger normalized measurements. In row-major order, its channels are:
> C01 — bounding-box width-to-height ratio.
> C02 — bounding-box area.
> C03–C05 — red, green, and blue means.
> C06–C08 — red, green, and blue standard deviations.
> C09–C11 — grayscale 25th percentile, median, and 75th percentile.
> C12 — edge-magnitude mean.
> C13 — edge-magnitude standard deviation.
> C14 — saturation mean.
> C15 — dark-pixel fraction.
> C16 — bright-pixel fraction.
> The two short bars above the grid duplicate the dithered C01 and C02 values. Bounded deterministic dithering is part of the sensor representation, so robust models should learn class distributions rather than attempt exact source lookup.
> Evaluation
> Submissions are scored with Platoon Sequence Utility (PSU):
> For test panel i, let p_i be the predicted token sequence and y_i the true token sequence. Valid submissions have len(p_i) = len(y_i) because they must provide exactly one token per card. Let N be the number of test panels.
> The normalized token edit similarity uses token-level Levenshtein distance d(p_i, y_i), where inserting, deleting, or substituting one whole vehicle token costs 1:
> edit_i = 1 - d(p_i, y_i) / max(len(p_i), len(y_i))
> mean_normalized_token_edit_similarity = (1 / N) * sum_i(edit_i)
> For transition F1, add beginning and end markers to a sequence and form the multiset of adjacent directed transitions:
> T([s1, ..., sn]) = {BOS>s1, s1>s2, ..., s(n-1)>sn, sn>EOS}
> count_i(e, prediction) = multiplicity of transition e in T(p_i)
> count_i(e, truth)      = multiplicity of transition e in T(y_i)
> matched_i = sum_e min(count_i(e, prediction), count_i(e, truth))
> transition_F1_i = 2 * matched_i / (len(T(p_i)) + len(T(y_i)))
> mean_per_panel_transition_F1 = (1 / N) * sum_i(transition_F1_i)
> Repeated transitions retain their multiplicity. For example, two occurrences can contribute two matches. The beginning and end transitions are scored like all other transitions.
> The two critical-vehicle F1 values are computed globally over all aligned card positions. For each k in {TRAILER, TRUCK}:
> TP_k        = sum over all aligned positions of 1[predicted token = k and true token = k]
> predicted_k = sum over all predicted positions of 1[predicted token = k]
> true_k      = sum over all true positions of 1[true token = k]
> F1_k        = 2 * TP_k / (predicted_k + true_k)
> If predicted_k + true_k is zero, F1_k is defined as 0. The final score is:
> PSU = 0.45 * mean_normalized_token_edit_similarity
> + 0.35 * mean_per_panel_transition_F1
> + 0.20 * min(F1_TRAILER, F1_TRUCK)
> Every component lies in [0, 1], so PSU also ranges from 0 to 1. Higher is better.
> Submission
> Submit a CSV containing:
> id — every test ID exactly once.
> vehicle_sequence — exactly one allowed uppercase token per panel card (four to seven tokens), separated by >.
> Example:
> id,vehicle_sequence
> 824575d2729c1114,CAR>SUV>PICKUP>TRUCK
> c0313fe81e0b0491,SEDAN>CAR>TRAILER>VAN>SUV
> a8c7eb3b7be2eb3e,SUV>PICKUP>CAR>CAR
> Requirements
> Preserve each panel's left-to-right card order.
> Use only the eight allowed tokens and the > separator.
> Include exactly the id and vehicle_sequence columns.
> Include every test ID once with no missing values.
> Write the final file to ./working/submission.csv.
> Prohibited methods
> Matching panels or signatures to TRANSSET or any other outside source frames or annotations.
> Using cached or source-derived label lookup tables.
> Inferring labels from IDs, CSV row order, or submission templates.
> Emitting fixed, templated, or rule-only sequences that do not learn vehicle classes from the supplied labeled panels.

Inspiration note: Useful for ordered route/workflow reconstruction outputs with explicit consistency constraints.
## Anonymous Visual Operator Relay

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cvb58nbayx3drad0w2n7fbd8axaap
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Be the first to climb the leaderboard!

### Full Challenge Description

> 1. Overview
> Anonymous Visual Operator Relay is a few-shot structured computer-vision challenge about learning a visual transformation from demonstrations provided inside each individual case.
> Every case contains:
> Four support source-result pairs.
> Exactly three support pairs generated by one shared hidden operator.
> Exactly one plausible decoy pair generated by a different valid operator.
> One untransformed query image.
> One low-detail context strip.
> No visible transformed query result.
> Participants must predict:
> Which three support demonstrations follow the shared operator.
> Which support demonstration is the decoy.
> Where the query image would meaningfully increase after applying the inferred operator.
> Where the query image would meaningfully decrease.
> The probability that the complete decoded response is correct.
> The hidden operator changes from case to case.
> A model cannot solve the challenge by memorizing one fixed transformation. It must infer the active rule from the current support demonstrations and transfer that rule to the current query.
> 2. Core Research Task
> The benchmark asks:
> Can a model infer an unfamiliar spatial visual operation from a small set of demonstrations, reject one contradictory example, and apply the inferred operation to a new visual structure?
> The task combines:
> Few-shot visual rule induction.
> Before-and-after image comparison.
> Contradictory-example detection.
> In-context visual learning.
> Spatial transformation transfer.
> Directional change localization.
> Joint reasoning across multiple demonstrations.
> Complete-case confidence calibration.
> Most visual benchmarks use one fixed label space, segmentation rule, or restoration process across the full dataset.
> Anonymous Visual Operator Relay instead defines a local prediction rule inside every case.
> The correct answer depends on relationships among the support pairs and the query rather than on the identity of any single image.
> 3. Case Structure
> Each case contains four support demonstrations.
> Support demonstration i consists of:
> A source image.
> A result image.
> Exactly three demonstrations express the same hidden operator.
> The remaining demonstration is a decoy created using another valid operator.
> The decoy is not random noise, an unchanged image, or an obviously corrupted example. It may resemble the true demonstrations in broad visual statistics while violating their shared spatial logic.
> The case also contains:
> One query image to which the shared operator must be transferred.
> One context strip derived from the support demonstrations.
> The transformed query image is never displayed.
> The participant must infer its directional changes.
> 4. Contact-Sheet Images
> Each case is stored as one RGB PNG contact sheet.
> The contact sheet contains:
> S0 SOURCE
> S0 RESULT
> S1 SOURCE
> S1 RESULT
> S2 SOURCE
> S2 RESULT
> S3 SOURCE
> S3 RESULT
> QUERY
> LOW-DETAIL CONTEXT
> Each support, result, and query panel has a resolution of:
> Height: 96 pixels.
> Width: 96 pixels.
> Support-pair order is randomized independently for every case.
> The decoy position is also randomized.
> A support index does not reveal:
> Whether the pair is consistent.
> Which operator generated it.
> The expected query change.
> Case difficulty.
> Source image identity.
> The contact-sheet PNG is the complete visual input for the corresponding case.
> 5. Hidden Operators and Decoys
> The hidden operators are spatially conditional transformations.
> They are not limited to simple global rotations, flips, or brightness changes.
> An operator may depend on:
> Local intensity.
> Relative contrast.
> Connected-component size.
> Shape thickness.
> Boundary distance.
> Interior or exterior position.
> Local texture.
> Neighborhood agreement.
> Radial position.
> Symmetry.
> Multi-scale context.
> Global image conditions.
> Possible effects include:
> Expanding selected structures.
> Contracting selected structures.
> Filling internal gaps.
> Opening selected regions.
> Connecting nearby components.
> Breaking weak connections.
> Strengthening boundaries.
> Suppressing isolated texture.
> Removing small components.
> Treating central and peripheral regions differently.
> Combining compatible positive and negative changes.
> The same operator family may behave differently on different images because its conditions may or may not be satisfied.
> The decoy operator may produce a similar changed-pixel count, affected area, direction balance, boundary pattern, or visual scale. A strong model must infer a common spatial explanation for the three consistent demonstrations.
> 6. Prediction Targets
> Participants submit four types of predictions.
> Support consistency
> For each support pair i, predict:
> p_support_i
> This is the probability that support pair i follows the shared operator.
> Exactly three supports are true and one is the decoy.
> Positive-change mask
> Predict the query pixels whose transformed values would be meaningfully higher than their original values.
> This mask is submitted as:
> increase_rle
> Negative-change mask
> Predict the query pixels whose transformed values would be meaningfully lower than their original values.
> This mask is submitted as:
> decrease_rle
> Relay confidence
> Submit:
> p_relay
> This is the estimated probability that the complete decoded response satisfies the exact relay criteria defined in Section 13.
> The increase and decrease masks must be disjoint.
> Pixels in neither mask are treated as unchanged.
> 7. Training and Test Data
> The released directory contains:
> undefined
> /
> ├── images/
> ├── train.csv
> ├── test.csv
> └── sample_submission.csv
> ### Training file
> `train.csv` contains:
> - `sample_id`
> - `image_file`
> - `height`
> - `width`
> - `support_0`
> - `support_1`
> - `support_2`
> - `support_3`
> - `increase_rle`
> - `decrease_rle`
> *`sample_id`**
> Type: String.
> Unique opaque case identifier.
> It must not be used as a predictive feature.
> *`image_file`**
> Type: String.
> Relative path to the contact-sheet PNG.
> *`height` and `width`**
> Type: Integer.
> Dimensions of the query change masks.
> Both values are `96` in the generated dataset.
> *`support_0` through `support_3`**
> Type: Integer.
> Values:
> - `1`: The support pair follows the shared operator.
> - `0`: The support pair is the decoy.
> Every training row contains exactly three values equal to `1` and one value equal to `0`.
> *`increase_rle` and `decrease_rle`**
> Type: String.
> One-indexed row-major run-length encodings of the hidden directional masks.
> An empty value represents an empty mask.
> The two hidden masks are always disjoint.
> ### Test file
> `test.csv` contains:
> - `sample_id`
> - `image_file`
> - `height`
> - `width`
> Participants must predict all hidden support and mask targets for each test row.
> ## 8. Run-Length Encoding
> The increase and decrease masks use one-indexed row-major run-length encoding.
> A mask of shape `height × width` is flattened one row at a time from left to right and top to bottom.
> Each positive run is represented by:
> start length
> Multiple runs are separated by spaces.
> Example:
> 5 4 20 3
> This represents:
> - Four positive pixels beginning at flattened position 5.
> - Three positive pixels beginning at flattened position 20.
> The first flattened position is `1`, not `0`.
> An empty mask is represented by an empty CSV field:
> ""
> Every RLE must satisfy all of the following:
> - It contains an even number of tokens.
> - Every token is an integer.
> - Every start is positive.
> - Every length is positive.
> - Every run stays within `height × width`.
> - Runs within the same mask do not overlap.
> - The submitted increase and decrease masks do not overlap.
> ## 9. Submission Format
> The submission must contain exactly these columns, in this order:
> sample_id
> p_support_0
> p_support_1
> p_support_2
> p_support_3
> increase_rle
> decrease_rle
> p_relay
> Support and relay probabilities must:
> - Be numeric.
> - Be finite.
> - Lie between `0` and `1`.
> The support probabilities do not need to sum to three.
> The evaluator selects the three support pairs with the highest support probabilities.
> When support probabilities are tied, the lower support index ranks first.
> A correctly formatted submission may look like:
> sample_id,p_support_0,p_support_1,p_support_2,p_support_3,increase_rle,decrease_rle,p_relay
> relay_001,0.97,0.94,0.06,0.92,"112 7 243 4","501 3",0.78
> relay_002,0.91,0.08,0.95,0.93,"","84 5 190 2",0.64
> relay_003,0.96,0.93,0.90,0.11,"","",0.71
> An empty RLE value represents an empty mask.
> Participants should use `sample_submission.csv` as the authoritative column-order template.
> ## 10. Submission Validation
> A submission-wide structural error causes the complete submission to receive a score of `0`.
> Submission-wide errors include:
> - Missing required columns.
> - Unknown extra columns.
> - Incorrect column order.
> - Duplicate column names.
> - Missing `sample_id` values.
> - Blank identifiers.
> - Duplicate identifiers.
> - Missing required test identifiers.
> - Unknown identifiers.
> - Non-numeric probability values.
> - NaN or infinite probabilities.
> - Probabilities below `0` or above `1`.
> Submission row order does not affect scoring.
> An RLE problem that can be associated with one specific `sample_id` is handled at the case level.
> Examples include:
> - An odd number of RLE tokens.
> - A non-integer RLE token.
> - A non-positive start or length.
> - A run outside the mask dimensions.
> - Overlapping runs inside one mask.
> - Overlap between the submitted increase and decrease masks.
> For such an identifiable RLE error, that case contributes zero to every case-level metric component. Other valid cases remain scorable.
> ## 11. Support Utility
> For one case, let:
> - `y_i = 1` when support `i` is a true demonstration.
> - `y_i = 0` when support `i` is the decoy.
> - `p_i` be the submitted `p_support_i`.
> There are exactly three true supports.
> The soft intersection is:
> soft_intersection =
> y_0 p_0 + y_1 p_1 + y_2 p_2 + y_3 p_3
> The soft union is:
> soft_union =
> p_0 + p_1 + p_2 + p_3
> 3
> soft_intersection
> The case-level soft support IoU is:
> soft_support_iou =
> (soft_intersection + 0.000000000001)
> /
> (soft_union + 0.000000000001)
> Mean Soft Support IoU is the average over all evaluation cases.
> The evaluator also selects the three support pairs with the highest probabilities.
> A case has exact support recovery when the selected set exactly equals the three true support pairs.
> exact_support_accuracy =
> number of cases with exact support recovery
> /
> number of evaluation cases
> Support Utility is:
> support_utility =
> 0.60 × mean_soft_support_iou
> 0.40 × exact_support_accuracy
> ## 12. Directional Mask Utilities
> Four components evaluate the predicted query changes.
> ### Increase Utility
> For one case, let:
> - `H_inc` be the hidden increase mask.
> - `P_inc` be the predicted increase mask.
> The F1 score is:
> increase_f1 =
> 2 × |H_inc ∩ P_inc|
> /
> (|H_inc| + |P_inc|)
> Special cases:
> - If both masks are empty, `increase_f1 = 1`.
> - If exactly one mask is empty, `increase_f1 = 0`.
> Increase Utility is:
> increase_utility =
> mean increase_f1 across all cases
> ### Decrease Utility
> For hidden decrease mask `H_dec` and predicted decrease mask `P_dec`:
> decrease_f1 =
> 2 × |H_dec ∩ P_dec|
> /
> (|H_dec| + |P_dec|)
> The same empty-mask rules apply.
> Decrease Utility is:
> decrease_utility =
> mean decrease_f1 across all cases
> ### Change Utility
> Define:
> hidden_change =
> H_inc OR H_dec
> undefined
> predicted_change =
> P_inc OR P_dec
> The case-level change IoU is:
> change_iou =
> |hidden_change ∩ predicted_change|
> /
> |hidden_change ∪ predicted_change|
> If both change masks are empty:
> change_iou = 1
> Change Utility is:
> change_utility =
> mean change_iou across all cases
> ### Direction Utility
> Direction is evaluated over:
> evaluated_union =
> H_inc OR H_dec OR P_inc OR P_dec
> Each pixel in this union receives one of three labels:
> - Increase.
> - Decrease.
> - Unchanged.
> A pixel is correct when its predicted directional label equals its hidden label.
> direction_accuracy =
> correct directional labels in evaluated_union
> /
> number of pixels in evaluated_union
> If the evaluated union is empty:
> direction_accuracy = 1
> Direction Utility is:
> direction_utility =
> mean direction_accuracy across all cases
> ## 13. Relay Confidence and Final Score
> A case has an exact relay when all of the following conditions hold:
> - The three true support pairs are selected exactly.
> - `increase_f1 >= 0.90`.
> - `decrease_f1 >= 0.90`.
> - `change_iou >= 0.90`.
> - The predicted increase and decrease masks do not overlap.
> Define:
> relay_target = 1
> when all conditions are satisfied, and:
> relay_target = 0
> otherwise.
> The submitted `p_relay` is clipped to:
> [0.000001, 0.999999]
> For one case, relay binary log loss is:
> relay_row_loss =
> -[
> relay_target × log(p_relay)
> (1 - relay_target) × log(1 - p_relay)
> ]
> Relay Log Loss is the mean over all cases.
> Relay Probability Utility is:
> relay_probability_utility =
> exp(-relay_log_loss)
> Exact Relay Accuracy is:
> exact_relay_accuracy =
> number of cases with relay_target = 1
> /
> number of evaluation cases
> Relay Utility is:
> relay_utility =
> 0.50 × relay_probability_utility
> 0.50 × exact_relay_accuracy
> The final score is:
> final_score = 100 × (
> 0.20 × support_utility
> 0.22 × increase_utility
> 0.22 × decrease_utility
> 0.16 × change_utility
> 0.10 × direction_utility
> 0.10 × relay_utility
> )
> The final score is clipped to:
> [0, 100]
> A higher score is better.
> The metric is additive. Weak performance in one component lowers the score according to its declared weight but does not automatically reduce the entire score to zero.
> ## 14. Modeling Guidance, Restrictions, and Limitations
> A basic system may:
> - Crop all support source and result panels.
> - Crop the query panel.
> - Encode every panel using a shared convolutional network.
> - Calculate feature differences between support sources and results.
> - Detect the least consistent support pair.
> - Transfer the inferred difference representation to the query.
> - Decode positive and negative changes using a segmentation head.
> - Estimate complete-case confidence.
> Stronger approaches may use:
> - Vision transformers.
> - Cross-attention between source and result panels.
> - Set transformers over support pairs.
> - Meta-learning.
> - In-context visual learning.
> - Neural process models.
> - Hypernetworks conditioned on support transformations.
> - Learned operator embeddings.
> - Graph reasoning over visual structures.
> - Multi-scale directional decoders.
> - Contrastive operator-consistency learning.
> - Iterative support-set refinement.
> - Decoy-aware attention.
> - Confidence-calibrated structured prediction.
> Predictions may not use:
> - `sample_id`.
> - Image filenames.
> - CSV row order.
> - PNG file size.
> - PNG metadata.
> - Compression properties.
> - Hidden source identifiers.
> - Original source labels.
> - External copies of source arrays.
> - Hardcoded evaluation outputs.
> The benchmark uses standardized, reduced-resolution visual panels.
> Some transformation effects may be ambiguous near weak boundaries or low-contrast regions.
> The operator library represents a controlled collection of spatial transformations and does not cover every possible visual operation.
> Directional masks identify meaningful increases and decreases but do not reproduce exact transformed intensities.
> Although the source arrays originate from biomedical image collections, this is a visual-reasoning benchmark. It is not intended for diagnosis, patient assessment, medical decision-making, biological interpretation, or clinical deployment.
> ## 15. Summary
> Anonymous Visual Operator Relay asks a model to infer a case-specific visual transformation from four demonstrations.
> The model must:
> - Identify the three demonstrations that share one hidden rule.
> - Reject one plausible contradictory demonstration.
> - Transfer the inferred rule to a new query image.
> - Predict where the query increases.
> - Predict where the query decreases.
> - Estimate whether the complete decoded response is correct.
> The defining difficulty is that the active operator changes from case to case and is never named.
> The three consistent demonstrations must be interpreted jointly, the decoy may be visually plausible, and the query may contain structures not seen in exactly the same form in the supports.
> The challenge evaluates few-shot visual rule induction, contradictory-example detection, directional change localization, and confidence calibration in one structured prediction task.
> &nbsp;

Inspiration note: Useful for ordered route/workflow reconstruction outputs with explicit consistency constraints.
## Basketball Court Landmark Trace Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7d1h53dcyhrb3z9bvyddhpv18ayxcj
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image, feature-engineering, Dataset source is visible after the challenge closes.
- Best/top context: Beat krishna_ram's score of 0.836!

### Full Challenge Description

> Overview
> Each example is a 512 by 288 RGB broadcast basketball frame. The task is to recover the visible court-line landmark trace: identify which of 48 fixed court landmark slots are visible, place each visible landmark at a normalized image coordinate, assign its coarse grid cell, and summarize the visible landmarks by left/middle/right image zone. The same submission also includes the broad visible court box.
> The images contain real play footage with players, camera motion, partial court visibility, scoreboard crops, and black broadcast bars. The landmarks come from court geometry annotations, so a good solution must use the visual court lines and camera perspective rather than treating every frame as having the same template.
> Dataset
> The provided files are:
> train.csv: 557 labeled examples.
> test.csv: 291 unlabeled examples.
> sample_submission.csv: valid low-information submission file with the required columns.
> images/: 848 JPEG images referenced by train.csv and test.csv.
> Columns in train.csv:
> id (string): unique example id.
> image_path (string): relative path to a JPEG image under images/.
> width (integer): image width in pixels. All rows use 512.
> height (integer): image height in pixels. All rows use 288.
> prompt (string): task instruction.
> answer_format_json (JSON string): required output schema, landmark id list, grid shape, and allowed zones.
> answer_json (JSON string): ground-truth visible court geometry for training rows.
> Columns in test.csv:
> id (string): unique example id.
> image_path (string): relative path to a JPEG image under images/.
> width (integer): image width in pixels.
> height (integer): image height in pixels.
> prompt (string): task instruction.
> answer_format_json (JSON string): required output schema.
> The answer JSON object has exactly these fields:
> {
> "court_box": [0.0000, 0.3714, 1.0000, 0.9951],
> "visible_landmarks": [
> {"point_id": "k08", "xy": [0.2745, 0.6771], "cell": "r12_c08", "zone": "left_third"},
> {"point_id": "k09", "xy": [0.3412, 0.7056], "cell": "r12_c10", "zone": "middle_third"}
> ],
> "visible_count": 2,
> "zone_counts": {"left_third": 1, "middle_third": 1, "right_third": 0}
> }
> court_box is [x_min, y_min, x_max, y_max], normalized to [0, 1], with (0, 0) at the top-left image corner. point_id must be one of k00 through k47. xy is the normalized landmark coordinate. cell is the landmark coordinate quantized to an 18 by 32 row-column grid, formatted like r12_c08. zone is one of left_third, middle_third, or right_third. visible_landmarks must be sorted by point_id; visible_count and zone_counts must match the list.
> Evaluation
> The score is the mean row score over all test rows. Each row score is clipped to [0, 1].
> The court box score is standard rectangle intersection-over-union:
> court_box_score = area(intersection(predicted_box, true_box))
> / area(union(predicted_box, true_box))
> Visible landmarks are matched only by identical point_id. For each submitted landmark whose id is visible in the true answer:
> distance = sqrt((pred_x - true_x)^2 + (pred_y - true_y)^2)
> xy_score = exp(-distance / 0.025)
> matched_landmark_score = 0.72 * xy_score
> + 0.18 * cell_exact
> + 0.10 * zone_exact
> cell_exact and zone_exact are 1 when the submitted value matches the true value and 0 otherwise.
> The landmark score is F1-style:
> precision = sum(matched_landmark_score) / number_of_predicted_landmarks
> recall    = sum(matched_landmark_score) / number_of_true_visible_landmarks
> landmark_score = 1 if both landmark lists are empty
> landmark_score = 0 if exactly one landmark list is empty
> landmark_score = 0 if precision + recall = 0
> landmark_score = 2 * precision * recall / (precision + recall) otherwise
> For visible count:
> count_score = 1 if predicted_count = true_count
> count_score = max(0, 1 - |predicted_count - true_count| / max(1, true_count)) otherwise
> For zone counts:
> zone_l1 = |pred_left - true_left| + |pred_middle - true_middle| + |pred_right - true_right|
> zone_total = sum(predicted_zone_counts) + sum(true_zone_counts)
> zone_count_score = 1 if zone_total = 0
> zone_count_score = max(0, 1 - zone_l1 / zone_total) otherwise
> The row score is:
> row_score = 0.67 * landmark_score
> + 0.18 * court_box_score
> + 0.10 * count_score
> + 0.05 * zone_count_score
> Malformed JSON, missing fields, extra fields, invalid value types, inconsistent counts, invalid landmark ids, unsorted landmark lists, invalid grid cells, or invalid normalized coordinates receive zero for that row. Submissions with the wrong columns, wrong column order, duplicate ids, missing ids, extra ids, or the wrong number of rows are rejected.
> Submission
> Submit a CSV file with exactly these two columns in this order:
> id (string): test row id.
> answer_json (JSON string): predicted court landmark trace.
> Example:
> id,answer_json
> court_11111111111111,"{""court_box"":[0.0,0.38,1.0,0.98],""visible_landmarks"":[{""point_id"":""k08"",""xy"":[0.27,0.68],""cell"":""r12_c08"",""zone"":""left_third""}],""visible_count"":1,""zone_counts"":{""left_third"":1,""middle_third"":0,""right_third"":0}}"
> court_22222222222222,"{""court_box"":[0.05,0.42,0.95,0.96],""visible_landmarks"":[{""point_id"":""k09"",""xy"":[0.34,0.71],""cell"":""r12_c10"",""zone"":""middle_third""}],""visible_count"":1,""zone_counts"":{""left_third"":0,""middle_third"":1,""right_third"":0}}"
> What Not To Use
> Do not use GPU acceleration.
> Do not use external basketball, sports-court, pose-estimation, landmark, or detector datasets.
> Do not use pretrained detector, landmark, homography, mask-recovery, or vision-language models.
> Do not use hosted vision APIs or manually maintained answer tables.
> Do not search for matching images, external metadata, or external annotation files outside the provided data.
> Do not install packages at runtime, include additional model checkpoints, use non-public or gated assets, or load remote code such as torch.hub or trust_remote_code.
> Do not hard-code predictions for specific test ids.

Inspiration note: Useful for graph/scaffold reconstruction tasks with decoys and consistency scoring.
## Flightline View-Graph Budgeting

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7626qeq2167zsdqmqpke1t158b0ssm
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Beat lelouch's score of 0.569!

### Full Challenge Description

> Flightline View-Graph Budgeting
> Overview
> Photogrammetry does not need every possible image pair to be matched. Exhaustive matching grows quadratically, while a sparse set of wrong edges can waste computation or leave the camera graph disconnected. For each case, choose exactly five candidate edges among six real UAV views: the smallest possible budget for a connected six-camera backbone. Each candidate edge is represented by a three-channel local-affinity map. Its 64 by 64 cells compare an 8 by 8 patch grid from one real frame with the grid from the other; channels encode color, texture, and combined affinity. The maps preserve correspondence structure without releasing an individually source-matchable frame.
> The target is a graph, not a class label or a ranked list. Many different submissions can receive full credit for one case. An edge is useful when the UAVPairs source workflow verified that its two frames are geometrically matchable. A good plan uses verified edges while connecting as many cameras as possible. This is a visual-learning challenge: a valid solution must train at least one predictive model from the supplied affinity maps and training labels before graph decoding.
> Every affinity value is deterministically measured from real UAV captures. Preparation applies crop, mirror, color normalization, resize, patch statistics, and cross-affinity computation; it generates no source imagery or labels. Evaluation holds out complete flight sequences, including every source frame from those sequences.
> Dataset
> File descriptions
> train.csv -- 600 graph cases from four training-only flight sequences, with the verified edges exposed.
> test.csv -- 240 graph cases from two unseen flight sequences, without verified edges.
> train/affinity/ -- Three-channel pair-affinity PNGs referenced only by train.csv.
> test/affinity/ -- Pair-affinity PNGs derived from evaluation-only flight sequences.
> sample_submission.csv -- A valid submission containing deterministic random five-edge plans.
> Column descriptions
> sample_id (string) -- Opaque identifier for one six-view planning case.
> flight_group (string, training only) -- Opaque source-flight group for leakage-resistant grouped validation.
> evidence_ab through evidence_ef (string) -- Paths relative to dataset/public/ for the 15 unordered candidate-edge affinity maps.
> verified_edges (string, training only) -- Pipe-separated verified pairs such as AB|AC|BD|CE|EF. This list can contain between five and nine edges.
> Every unordered pair among A through F is a candidate. Edge codes always place the earlier letter first: AB is valid and BA is not.
> Evaluation
> Submissions are scored with Robust View-Graph Utility, bounded from 0 to 1. For each case, only submitted edges present in the hidden verified set are retained. Edge precision measures matching-budget efficiency. Connected coverage is the number of cameras in the largest component of the retained graph divided by six.
> verified = set(submitted_edges) & set(hidden_verified_edges)
> edge_precision = len(verified) / 5
> connected_coverage = largest_component_size(verified) / 6
> case_utility = 0.40  *edge_precision + 0.60*  connected_coverage
> score = 0.80  *mean(case_utility) + 0.20*  mean(bottom_quartile(case_utility))
> Connected coverage receives the larger weight because a reconstruction pipeline cannot solve cameras outside its match graph. Precision still matters because each bad match consumes one fifth of the fixed budget. The bottom-quartile term penalizes methods that abandon difficult viewpoints or one held-out flight regime.
> Submission
> Submit exactly one row for every sample_id in test.csv.
> sample_id (string) -- Exact identifier copied from test.csv.
> edge_plan (string) -- Exactly five distinct valid edge codes separated by |.
> Example using real test identifiers and formatting-only plans:
> sample_id,edge_plan
> ba3322330ce7d435,AB|AC|BD|CE|EF
> 29cab6a79405ad37,AB|BC|CD|DE|EF
> Requirements
> The file must contain exactly 240 data rows.
> Every test sample_id must appear exactly once; missing, duplicate, or unknown identifiers are invalid.
> Each edge_plan must contain exactly five distinct entries from AB, AC, AD, AE, AF, BC, BD, BE, BF, CD, CE, CF, DE, DF, EF.
> Letters inside an edge must be in ascending order.
> File format: CSV with exact columns sample_id,edge_plan.
> What Not To Use
> Do not retrieve the upstream archive or its overlap metadata to identify evaluation frames or recover hidden edges.
> Do not reverse-map public affinity maps, hashes, or identifiers to upstream filenames or source-frame pairs.
> Do not use external image-search, source-dataset lookup tables, or leaderboard probing.
> Do not submit a fixed statistic-only, threshold-only, or other untrained rule-only decoder. Such methods are useful baselines but do not satisfy the required visual-learning step.
> Train and validate only from the supplied public data.

Inspiration note: Useful for graph/scaffold reconstruction tasks with decoys and consistency scoring.
## Chromosome Contact Fragment Scaffolding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dmpeb11xk6b8729e6t6vxxs88y39h
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, image, Dataset source is visible after the challenge closes.
- Best/top context: Beat oguricapu's score of 0.871!

### Full Challenge Description

> Overview
> Reconstruct an oriented eight-fragment chromosome scaffold from a contact-map quilt containing ten labeled candidates. Two candidates are overlapping breakpoint decoys. For every case, submit the scaffold sequence, the two excluded fragments, and a matrix describing the evidence supporting each recovered join.
> Chromosome-contact experiments measure how often genomic regions occupy nearby three-dimensional positions. Assemblies can use this contact decay to order and orient sequence fragments, but breakpoint uncertainty creates several highly plausible alternatives. Here, each image is built from real corrected contact measurements and matching annotation tracks. The eight true fragments tile one contiguous genomic interval. Each decoy is a real fragment shifted two or three bins from a genuine breakpoint, so it overlaps the correct chain and can have equally strong local contact.
> This differs from image classification and boundary-change detection. The primary prediction is a constrained scaffold program over ten image-local fragment identities. A complete global reversal of the chromosome is biologically equivalent, so the grader accepts both orientations.
> The challenge is CPU compatible. Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> Dataset
> The prepared dataset contains 1,645 labeled training quilts and 544 hidden test quilts. Seven complete species are held out for test. No species, source window, public row, or image payload crosses the split.
> Every public asset is a 780 by 790 RGB JPEG. Source species names, chromosome identifiers, genomic coordinates, accessions, matrix dimensions, and filenames are removed. Four heatmap palettes are used without changing the underlying evidence.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Quilt references, scaffold contracts, and three labeled structured targets. |
> | `test.csv` | Quilt references and scaffold contracts for hidden cases. |
> | `sample_submission.csv` | Valid placeholder output with the required schema. |
> | `images/*.jpg` | Opaque contact-fragment quilts referenced by the CSV files. |
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque unique case identifier. |
> | `contact_quilt_path` | relative path string | JPEG location under the public dataset root. |
> | `scaffold_contract` | string | Declares the number of candidates, scaffold length, decoy count, matrix shape, and reversal equivalence. It contains no case-specific answer. |
> Quilt Layout
> The central square is an 80 by 80 contact matrix divided into a 10 by 10 grid of fragment blocks. Each block contains 8 by 8 genomic bins. Display labels f1 through f10 identify the candidates on both axes.
> Diagonal blocks show within-fragment contact. Off-diagonal blocks show contact between two displayed fragments. The display order is random, and every displayed fragment can be independently reversed. Darker cells represent stronger contact after palette normalization.
> Three tracks below the matrix remain aligned with the displayed fragment order:
> | Track | Meaning |
> |---|---|
> | `gene +` | Count of genes annotated on the forward strand in each bin. |
> | `gene -` | Count of genes annotated on the reverse strand in each bin. |
> | `repeat` | Count of repeat or non-gene annotations in each bin. |
> The two decoys are not remote negative examples. Each is shifted by -3, -2, +2, or +3 genomic bins from one of the six internal genuine fragments. The correct eight-fragment scaffold is therefore the globally consistent non-overlapping tiling, not simply the eight candidates with highest contact.
> Target Columns
> | Column | Data type | Description |
> |---|---|---|
> | `scaffold_program` | ordered token string | Eight distinct oriented fragment tokens in genomic order, followed by `seal:scaffold`. |
> | `decoy_fragment_set` | canonical set string | Exactly two excluded fragment labels in increasing numeric order. |
> | `join_evidence_matrix` | JSON integer matrix | Shape 7 by 3. Rows follow adjacent scaffold joins; columns encode contact, gene, and repeat support. |
> Target Diversity
> | Property | Train | Test |
> |---|---:|---:|
> | Rows | 1,645 | 544 |
> | Unique scaffold programs | 1,645 | 544 |
> | Unique decoy sets | 45 | 45 |
> | Unique join matrices | 1,644 | 544 |
> Scaffold Grammar
> A fragment token is fN+ or fN-, where N is 1 through 10. + means retain the fragment's displayed direction when placing it in the scaffold. - means reverse it. Eight distinct fragment labels must appear, followed by seal:scaffold.
> f3+>f5->f4->f2+>f8->f6->f1->f7->seal:scaffold
> The globally reversed equivalent is obtained by reversing the eight fragment tokens and flipping every sign:
> f7+>f1+>f6+>f8+>f2->f4+>f5+>f3->seal:scaffold
> Both programs receive identical credit.
> Decoy Set Grammar
> Submit the two unused labels as fA|fB, with A < B numerically.
> f9|f10
> Join Evidence Matrix
> The seven rows correspond to joins 1 through 7 in the submitted scaffold direction. The three columns are ordered as follows:
> | Column index | Evidence channel |
> |---:|---|
> | 0 | Contact strength between the two endpoint regions. |
> | 1 | Forward-plus-reverse gene-track continuity across the join. |
> | 2 | Repeat-track continuity across the join. |
> For each channel, a join is ranked against all directed candidate-fragment joins and both possible orientations in that case. Values have these meanings:
> | Value | Meaning |
> |---:|---|
> | 0 | Lower 40 percent of candidate support. |
> | 1 | At least the 40th percentile but below the 80th percentile. |
> | 2 | Top 20 percent of candidate support. |
> For gene and repeat continuity, smaller endpoint discontinuity means stronger support. If the reversed scaffold program is submitted, reverse the seven matrix rows. The column order never changes.
> [[2,2,1],[2,0,1],[2,1,0],[2,2,1],[2,0,0],[2,0,1],[2,1,1]]
> Example Input
> case_id,contact_quilt_path,scaffold_contract
> fcfd5ace58e1df48f287a1a5,images/4dc2dbc2b5e5f251c35f2d64e65a63fe.jpg,"Recover one eight-fragment oriented scaffold from f1 through f10, exclude two decoys, and report a 7 by 3 join-evidence matrix. Global reversal is equivalent."
> Example Label
> case_id,scaffold_program,decoy_fragment_set,join_evidence_matrix
> fcfd5ace58e1df48f287a1a5,f3+>f5->f4->f2+>f8->f6->f1->f7->seal:scaffold,f9|f10,"[[2,2,1],[2,0,1],[2,1,0],[2,2,1],[2,0,0],[2,0,1],[2,1,1]]"
> Submission Format
> Write the final CSV to exactly ./working/submission.csv with these columns in this order:
> case_id,scaffold_program,decoy_fragment_set,join_evidence_matrix
> | Column | Required serialization |
> |---|---|
> | `case_id` | Exact opaque string from `test.csv`. |
> | `scaffold_program` | Nine `>`-delimited tokens, at most 100 characters. |
> | `decoy_fragment_set` | Two numerically sorted `|`-delimited labels, at most 16 characters. |
> | `join_evidence_matrix` | JSON 7 by 3 integer matrix with values from 0 through 2, at most 100 characters. |
> Valid nontrivial example:
> case_id,scaffold_program,decoy_fragment_set,join_evidence_matrix
> example_case,f3+>f5->f4->f2+>f8->f6->f1->f7->seal:scaffold,f9|f10,"[[2,2,1],[2,0,1],[2,1,0],[2,2,1],[2,0,0],[2,0,1],[2,1,1]]"
> Extra columns, reordered columns, duplicate IDs, missing IDs, unknown IDs, and additional rows are rejected. A single backend-managed visibility column is ignored. Malformed structured values receive zero for their affected component.
> Evaluation
> The metric is Chromosome Scaffold Reconstruction Score:
> RowScore = 0.58 * ScaffoldProgramScore
> + 0.20 * DecoySetScore
> + 0.22 * JoinEvidenceScore
> Score = mean(RowScore over all hidden cases)
> The minimum score is 0.0, the maximum score is 1.0, and higher is better.
> ScaffoldProgramScore
> Let Y be the hidden nine-token program, reverse(Y) its globally reversed sign-flipped equivalent, and P the submitted program. Token-level Levenshtein distance is the minimum number of insertions, deletions, and substitutions.
> similarity = max over C in {Y, reverse(Y)} of
> 1 - token_edit_distance(C, P) / 9
> exact_program = 1 if P equals Y or reverse(Y), otherwise 0
> ScaffoldProgramScore = 0.14 * similarity + 0.86 * exact_program
> The parser accepts exactly nine tokens, so edit-distance work is bounded. Repeated fragments, invalid signs, or malformed programs score 0.
> DecoySetScore
> Let Y and P be the hidden and submitted two-fragment sets.
> set_F1 = 2 * |Y intersect P| / (|Y| + |P|)
> exact_set = 1 if Y equals P, otherwise 0
> DecoySetScore = 0.25 * set_F1 + 0.75 * exact_set
> A malformed, repeated, or unsorted set scores 0.
> JoinEvidenceScore
> The prediction is compared with the hidden matrix and its row-reversed equivalent. For each candidate truth matrix C, entry weights are 3 when C[i,j] = 2, 2 when C[i,j] = 1, and 1 when C[i,j] = 0.
> weighted_agreement(C, P) =
> sum(w[i,j] * I(C[i,j] = P[i,j])) / sum(w[i,j])
> candidate_score(C, P) =
> 0.24 * weighted_agreement(C, P)
> + 0.76 * I(C exactly equals P)
> JoinEvidenceScore = max(candidate_score(C, P)
> for C in {hidden, row_reversed_hidden})
> An overlong, malformed, non-integer, out-of-range, or incorrectly shaped matrix scores 0.
> What Makes This Interesting
> The task adapts a real assembly ambiguity rather than inserting an obvious negative patch. Every decoy overlaps a valid genomic fragment and preserves real contact and annotation measurements. Recovering the scaffold requires reasoning about a complete tiling, independent fragment orientation, duplicated local evidence, three annotation channels, and the physical symmetry that makes global chromosome reversal equivalent.
> Method Requirements
> CPU-compatible image encoders, block-contact features, overlap inference, dynamic programming, graph search, sequence models, and constrained decoding are allowed. Training and calibration must use only public training cases.
> What Not To Use
> Do not derive outputs from case_id, image path, row order, JPEG size, palette, archive order, or storage metadata.
> Do not match public quilts to external contact-map repositories, assemblies, source figures, or annotation mirrors.
> Do not update parameters, thresholds, or retrieval labels from hidden test quilts.
> Do not exploit extra columns, duplicate IDs, missing rows, oversized fields, malformed JSON, or parser behavior.
> Do not use hosted closed-model APIs at inference time.

Inspiration note: Useful for graph/scaffold reconstruction tasks with decoys and consistency scoring.
## Evidence-Guided Flood Mask Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76kt7cydaxk341egy5fc2gfs8asma7
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Beat nsndtrai's score of 77.473!

### Full Challenge Description

> Evidence-Guided Flood Mask Repair
> 1. Challenge Overview
> Evidence-Guided Flood Mask Repair is a structured prediction challenge about auditing and correcting flood extent maps from multimodal satellite and environmental data.
> Flood mapping is used in disaster response, infrastructure planning, emergency coordination, agricultural assessment, and post-event damage analysis. Automated flood masks can be useful at large scale, but they often contain localized errors caused by cloud cover, radar noise, terrain effects, missing observations, confusing land surfaces, or imperfect model boundaries.
> In this challenge, each case begins with a draft binary flood mask that is already mostly correct.
> Participants do not generate an entirely new flood map from scratch.
> Instead, they inspect the supplied evidence and submit a sparse repair plan describing:
> Pixels that should be added to the flood class.
> Pixels that should be removed from the flood class.
> Each case provides:
> An eight-channel spatial raster.
> An eight-channel validity mask.
> A draft binary flood mask.
> An audit mask identifying the only region where edits are permitted.
> A unique opaque case identifier.
> The objective is to determine:
> Whether the draft flood mask contains an error.
> Where the error is located.
> Whether flood pixels should be added or removed.
> How far the correction should extend.
> Which nearby flood structures should remain unchanged.
> Whether the correct action is to make no edit.
> Some audit regions contain genuine flood-mask defects.
> Other audit regions are already correct.
> A successful system must therefore learn both intervention and restraint.
> 2. Real-World Prediction Scenario
> The positive class represents flooded land or water-covered terrain associated with a flood event.
> The negative class represents areas that should not be labeled as flooded.
> The input raster combines information from radar, optical imagery, terrain, and recent precipitation.
> These sources provide complementary evidence.
> Radar measurements can detect surface-water and moisture-related changes even when optical observations are degraded by clouds.
> Optical channels help distinguish water, vegetation, soil, and built surfaces when observations are valid.
> Elevation provides terrain context because flood extent is constrained by local topography.
> Recent precipitation provides event context because heavy rainfall can increase the likelihood of flooding.
> The draft mask represents an existing flood prediction produced before the repair stage.
> The participant’s task is to identify localized inconsistencies between that draft prediction and the available evidence.
> 3. Core Prediction Problem
> This benchmark does not ask only which pixels appear flooded.
> It asks which parts of an existing flood prediction are inconsistent with the available evidence and what the smallest justified correction is.
> The draft mask acts as a strong prior.
> Most draft pixels are already correct and should remain unchanged.
> The model must compare:
> The current draft flood state.
> Radar evidence.
> Optical evidence.
> Observation validity and missingness.
> Elevation and terrain structure.
> Recent precipitation context.
> Local flood boundaries.
> Connected flood structures.
> The cost of making an unnecessary edit.
> This makes the challenge a constrained flood-mask repair task rather than ordinary semantic segmentation.
> 4. Distinctive Task Structure
> Existing Prediction as an Input
> The draft flood mask is the initial state of the final output.
> The model must determine which portions of that draft should be trusted.
> Hard Intervention Boundary
> The audit mask defines where edits are permitted.
> Pixels outside the audit mask are immutable.
> Sparse Directional Output
> Participants submit separate addition and removal masks rather than a complete replacement flood mask.
> This preserves the direction of every correction.
> Explicit No-Change Cases
> Some cases require no additions and no removals.
> The model must recognize when the draft is already supported by the available evidence.
> Preservation Requirement
> Correct flood and non-flood pixels inside the audit region must be protected from unnecessary edits.
> Structural Evaluation
> The metric evaluates boundaries and connected flood components in addition to pixel overlap.
> Robustness Aggregation
> The final score rewards consistent performance across all cases, including sparse, mixed, structurally difficult, and no-change cases.
> 5. Inputs
> Every case contains aligned raster, draft-mask, and audit-mask inputs.
> Multimodal Raster
> The raster has shape 8 × H × W.
> The channels are:
> Channel 0: Sentinel-1 VV radar backscatter.
> Channel 1: Sentinel-1 VH radar backscatter.
> Channel 2: Sentinel-2 green reflectance.
> Channel 3: Sentinel-2 red reflectance.
> Channel 4: Sentinel-2 near-infrared reflectance.
> Channel 5: Sentinel-2 shortwave-infrared reflectance.
> Channel 6: elevation.
> Channel 7: seven-day cumulative precipitation.
> All channels are normalized to the interval from 0 to 1.
> The values are normalized features rather than original physical units.
> Channel 0 and Channel 1 describe radar return strength in VV and VH polarization.
> Radar backscatter may help separate open water, rough land surfaces, vegetation, and moisture-related changes.
> Channel 2 and Channel 3 describe visible green and red reflectance.
> These channels provide information about surface color, vegetation, sediment, soil, and water appearance.
> Channel 4 describes near-infrared reflectance.
> Water commonly has low near-infrared reflectance, while healthy vegetation often has stronger near-infrared response.
> Channel 5 describes shortwave-infrared reflectance.
> This channel can help distinguish water and wet surfaces from dry soil, vegetation, and built areas.
> Channel 6 describes relative terrain elevation after normalization.
> Flooding is influenced by terrain shape, low-lying regions, drainage paths, and local topographic barriers.
> Channel 7 describes normalized seven-day cumulative precipitation.
> Higher recent rainfall may support the presence of flooding, although precipitation alone does not determine the flood boundary.
> Validity Mask
> Each raster archive also contains a Boolean validity mask with shape 8 × H × W.
> A value of True means that the corresponding channel observation is valid.
> A value of False means that the observation is missing or invalid.
> Invalid raster positions are filled with zero after normalization.
> Models should use the validity mask to distinguish genuine normalized zero values from missing observations.
> Draft Flood Mask
> The draft mask is a binary image with shape H × W.
> Pixel meaning:
> 0 means non-flood.
> Any nonzero value means flood.
> The draft mask is already mostly correct.
> Audit Mask
> The audit mask is a binary image with shape H × W.
> Pixel meaning:
> 0 means editing is forbidden.
> Any nonzero value means editing is permitted.
> The audit mask identifies where the draft should be reviewed.
> It does not reveal which pixels are wrong.
> 6. Repair Operation
> Let draft be the supplied draft flood mask.
> Let audit be the supplied audit mask.
> Let add be the predicted flood-addition mask.
> Let remove be the predicted flood-removal mask.
> The repaired flood mask is:
> repaired = (draft OR add) AND NOT remove
> Pixels in add change from non-flood to flood.
> Pixels in remove change from flood to non-flood.
> All other pixels preserve their draft state.
> The addition and removal masks must be disjoint.
> 7. Validity Constraints
> Every predicted addition must satisfy:
> audit = 1
> draft = 0
> Every predicted removal must satisfy:
> audit = 1
> draft = 1
> For every pixel where audit = 0:
> add must equal 0.
> remove must equal 0.
> repaired must equal draft.
> Participants should constrain predictions before encoding them.
> Conceptually:
> Additions are restricted to editable pixels currently labeled non-flood.
> Removals are restricted to editable pixels currently labeled flood.
> Any overlap between additions and removals must be removed.
> 8. Possible Draft Defects
> A draft may contain one or more localized flood-mapping defects.
> Missing Flood Region
> A genuinely flooded region is absent from the draft.
> False Flood Region
> A non-flood region is incorrectly labeled as flooded.
> Boundary Expansion
> The flood mask extends beyond the boundary supported by the evidence.
> Boundary Contraction
> A supported portion of the flood extent is missing.
> Local Omission
> A flooded branch, corridor, shoreline section, low-lying region, or compact component is absent.
> False Island
> An unsupported isolated flood component is present.
> Broken Connectivity
> A valid connection between flooded regions is missing.
> False Bridge
> Two separate flood components are incorrectly connected.
> Incorrect Hole Fill
> A valid non-flood hole inside or near the flood region is incorrectly filled.
> Incorrect Hole Cut
> A false non-flood hole is introduced into a valid flood region.
> Terrain-Inconsistent Spill
> The draft extends uphill or across terrain in a way that is not supported by the available evidence.
> Sensor-Confusion Error
> The draft follows a pattern caused by radar noise, optical ambiguity, cloud-related missingness, shadows, wet soil, vegetation, or another surface that resembles flood evidence in only some channels.
> Mixed Defect
> Multiple compatible error types occur in one case.
> No-Change Case
> The draft flood mask is already correct inside the audit region.
> The correct output contains an empty addition mask and an empty removal mask.
> 9. Why the Task Is Difficult
> Most Pixels Are Already Correct
> The imbalance is not only flood versus non-flood.
> It is also change versus preservation.
> True Edits Are Sparse
> A large audit region may contain only a small correction.
> Addition and Removal Are Asymmetric
> Evidence supporting a missing flood region may differ from evidence supporting removal of a false flood region.
> Sensor Modalities May Disagree
> Radar, optical imagery, terrain, and rainfall may support different interpretations.
> Missingness Is Structured
> Clouds, invalid observations, or sensor limitations may be concentrated around difficult areas.
> Terrain Matters
> A visually plausible flood prediction may be inconsistent with elevation and local drainage structure.
> Geometry Matters
> A repair may have reasonable pixel overlap while producing an incorrect flood boundary.
> Connectivity Matters
> A repair may create a false bridge, remove a valid connection, split a flood component, or introduce an isolated region.
> Correct Regions May Appear Suspicious
> Some difficult-looking audit regions should remain unchanged.
> 10. Public Directory
> The released public directory contains:
> audit_masks/
> draft_masks/
> rasters/
> sample_submission.csv
> test.csv
> train.csv
> All paths stored in the CSV files are relative to the public directory.
> 11. Raster Files
> The rasters/ directory contains compressed NumPy archives.
> Each .npz file contains:
> x
> valid
> x
> Type: float32
> Shape: 8 × H × W
> Values are normalized to the interval from 0 to 1.
> Channel order:
> Channel 0: Sentinel-1 VV radar backscatter.
> Channel 1: Sentinel-1 VH radar backscatter.
> Channel 2: Sentinel-2 green reflectance.
> Channel 3: Sentinel-2 red reflectance.
> Channel 4: Sentinel-2 near-infrared reflectance.
> Channel 5: Sentinel-2 shortwave-infrared reflectance.
> Channel 6: normalized elevation.
> Channel 7: normalized seven-day cumulative precipitation.
> valid
> Type: Boolean
> Shape: 8 × H × W
> A value of True means that the corresponding observation is valid.
> A value of False means that the observation is unavailable or invalid.
> Invalid positions in x are filled with zero.
> Models should use valid to distinguish real zero values from missing observations.
> 12. Draft Masks
> The draft_masks/ directory contains binary PNG files.
> Each mask has the same height and width as its corresponding raster.
> Pixel meaning:
> 0 means non-flood.
> Any nonzero value means flood.
> The draft should be interpreted as image_array greater than zero.
> 13. Audit Masks
> The audit_masks/ directory contains binary PNG files.
> Pixel meaning:
> 0 means editing is forbidden.
> Any nonzero value means editing is permitted.
> The audit mask should be interpreted as image_array greater than zero.
> An audit region may contain:
> One genuine flood-mask defect.
> Multiple defects.
> Several plausible-looking repair locations.
> Correct flood structure surrounding a defect.
> Disconnected candidate regions.
> Missing observations.
> Contradictory evidence.
> No defect.
> 14. Training Data
> train.csv contains:
> case_id
> raster_path
> draft_mask
> audit_mask
> height
> width
> add_rle
> remove_rle
> case_id
> A unique opaque identifier for the repair case.
> raster_path
> The relative path to the compressed raster archive.
> Multiple cases may reference the same parent raster.
> draft_mask
> The relative path to the draft flood-mask PNG.
> audit_mask
> The relative path to the audit-mask PNG.
> height
> The image height in pixels.
> width
> The image width in pixels.
> add_rle
> Run-length encoding of pixels that must change from non-flood in the draft to flood in the corrected mask.
> An empty string means that no flood pixels need to be added.
> remove_rle
> Run-length encoding of pixels that must change from flood in the draft to non-flood in the corrected mask.
> An empty string means that no flood pixels need to be removed.
> When both fields are empty, the case is a valid no-change example.
> Empty edit fields may appear as blank CSV cells or may be parsed as missing values by some CSV libraries.
> Both are interpreted as empty masks.
> Participants are encouraged to load CSV files with automatic missing-value conversion disabled so blank RLE values remain empty strings.
> 15. Test Data
> test.csv contains:
> case_id
> raster_path
> draft_mask
> audit_mask
> height
> width
> Participants must predict add_rle and remove_rle for every test case.
> The hidden corrections are not included.
> 16. Sample Submission
> sample_submission.csv contains:
> case_id
> add_rle
> remove_rle
> The supplied sample submission leaves both edit columns empty.
> Submitting it unchanged produces the valid copy-draft baseline.
> A correctly formatted submission file may look like this:
> case_id,add_rle,remove_rle
> case_0a4f93,"112 8 368 4",""
> case_193d7c,"","501 6"
> case_282aac,"",""
> The first example predicts two addition runs and no removals.
> The second example predicts one removal run and no additions.
> The third example predicts no change.
> The case identifiers shown above are illustrative.
> A real submission must use the exact case_id values provided in test.csv.
> 17. Run-Length Encoding
> Edit masks use one-indexed row-major run-length encoding.
> The binary mask is flattened one row at a time from top to bottom and left to right.
> Each positive run is represented by:
> start length
> Starts are one-indexed.
> Multiple runs are separated by spaces.
> For example:
> 4 3 12 2
> This represents:
> Three positive pixels beginning at flattened position 4.
> Two positive pixels beginning at flattened position 12.
> An empty mask is represented by an empty string.
> A correct encoder should:
> Flatten the mask in row-major order.
> Detect every consecutive run of positive pixels.
> Record the one-indexed start of each run.
> Record the number of pixels in each run.
> Return an empty string when the mask contains no positive pixels.
> A correct decoder should:
> Treat blank values and missing values as empty masks.
> Require an even number of integer values.
> Interpret alternating values as start and length.
> Convert starts from one-indexed to zero-indexed positions.
> Require positive run lengths.
> Reject runs that exceed the declared mask dimensions.
> Reject overlapping or unsorted runs.
> 18. Submission Format
> The submission must contain exactly:
> case_id
> add_rle
> remove_rle
> Submission requirements:
> Include every evaluation case_id.
> Include each identifier exactly once.
> Do not include unknown identifiers.
> Use valid one-indexed row-major RLE.
> Keep every run inside the declared dimensions.
> Keep all edits inside the audit mask.
> Add only where the draft is non-flood.
> Remove only where the draft is flood.
> Keep addition and removal masks disjoint.
> A malformed edit invalidates only the affected case.
> Submission-wide structural failures invalidate the full submission.
> Examples include:
> Incorrect submission columns.
> Missing evaluation identifiers.
> Duplicate identifiers.
> Unknown identifiers.
> An empty submission table.
> 19. Evaluation
> Every case is scored independently.
> The evaluation measures:
> Addition accuracy.
> Removal accuracy.
> Final repaired-mask agreement.
> Boundary agreement.
> Preservation of correct draft pixels.
> Connected-component agreement.
> Robustness across cases.
> Addition F1
> addition_f1 is the binary F1 score between the hidden addition mask and the predicted addition mask.
> If both masks are empty, addition_f1 equals 1.
> If exactly one mask is empty, addition_f1 equals 0.
> Removal F1
> removal_f1 is the binary F1 score between the hidden removal mask and the predicted removal mask.
> The same empty-mask rules apply.
> Edit Score
> edit_score is the average of addition_f1 and removal_f1.
> Audit-Region IoU
> audit_iou is the intersection-over-union between the repaired prediction and corrected flood target inside the audit region.
> Only pixels inside the audit mask are included.
> If both evaluated masks contain no flood pixels, audit_iou equals 1.
> Boundary Agreement
> Flood-boundary pixels are compared inside the audit region with a tolerance of two pixels.
> The boundary score is a boundary F1 score.
> If both boundary sets are empty, boundary_score equals 1.
> If only one boundary set is empty, boundary_score equals 0.
> Preservation Score
> The preservation score measures the fraction of already-correct draft pixels inside the audit region that remain unchanged.
> If there are no already-correct audit pixels, preservation_score equals 1.
> Component Agreement
> Eligible connected flood components intersecting the audit region are matched one-to-one when their IoU is at least 0.25.
> Components smaller than eight pixels are ignored.
> The component score is a component-level F1 score.
> If neither result contains an eligible component, component_score equals 1.
> If only one result contains eligible components, component_score equals 0.
> Per-Case Score
> The case score is calculated as:
> 40 percent edit score.
> 25 percent audit-region IoU.
> 15 percent boundary agreement.
> 10 percent preservation score.
> 10 percent component agreement.
> Equivalently:
> case_score = 0.40 × edit_score + 0.25 × audit_iou + 0.15 × boundary_score + 0.10 × preservation_score + 0.10 × component_score
> Final Score
> Let mean_case_score be the mean of all case scores.
> Let lower_quartile_score be the 25th percentile of all case scores.
> The final score is:
> final_score = 100 × (0.85 × mean_case_score + 0.15 × lower_quartile_score)
> The result is clipped to the interval from 0 to 100.
> 20. High-Level Grader Logic
> The grader first validates the submission as a whole.
> It requires exactly three columns:
> case_id
> add_rle
> remove_rle
> It requires every evaluation identifier to appear exactly once.
> It rejects duplicate identifiers, unknown identifiers, missing identifiers, and empty submission tables.
> If a submission-wide structural requirement fails, the final score is zero.
> If submission-wide validation succeeds, the grader processes each evaluation case independently.
> For each case, the grader:
> Loads the draft flood mask.
> Loads the audit mask.
> Decodes the hidden addition mask.
> Decodes the hidden removal mask.
> Decodes the participant addition mask.
> Decodes the participant removal mask.
> Confirms that additions and removals do not overlap.
> Confirms that all edits lie inside the audit mask.
> Confirms that additions occur only where the draft is non-flood.
> Confirms that removals occur only where the draft is flood.
> Reconstructs the hidden corrected flood mask.
> Reconstructs the participant’s repaired flood mask.
> Computes the pixel, boundary, preservation, and component metrics.
> Combines the metrics into a weighted case score.
> If a participant prediction is malformed or violates a case-level constraint, that case receives a score of zero while other cases remain eligible for scoring.
> After all cases are scored, the grader calculates:
> The mean case score.
> The 25th percentile case score.
> The final score combines both values so that consistent performance is rewarded.
> 21. What the Metric Rewards
> A strong system should:
> Detect genuine flood-mask defects.
> Predict the correct edit direction.
> Recover accurate flood boundaries.
> Preserve valid flood and non-flood pixels.
> Restore meaningful connected flood structure.
> Avoid false islands and false bridges.
> Leave correct audit regions unchanged.
> Perform consistently across different case types.
> The metric does not reward aggressive editing by default.
> Unnecessary edits may reduce edit accuracy, preservation, IoU, boundary agreement, and component agreement simultaneously.
> 22. Modeling Guidance
> A practical model may combine:
> The eight raster channels.
> The eight-channel validity mask.
> The draft flood mask.
> The audit mask.
> Distance to the current flood boundary.
> Local elevation variation.
> Local rainfall context.
> Neighborhood statistics.
> Connected-component features.
> Missing-observation features.
> A natural output formulation is a three-state pixel classifier:
> Keep.
> Add flood.
> Remove flood.
> Predictions may then be filtered using:
> Audit membership.
> Draft-state validity.
> Component size.
> Boundary consistency.
> Morphological consistency.
> Terrain consistency.
> Topological checks.
> Confidence thresholds.
> A participant may also model addition and removal using two binary output heads.
> 23. Validation Guidance
> Multiple training cases may reference the same parent raster.
> A random row-level train and validation split may place cases derived from the same raster in both partitions.
> This can produce overly optimistic validation results.
> Participants are strongly encouraged to group validation by raster_path.
> A useful development process is:
> Establish the copy-draft baseline.
> Create a validation split grouped by raster_path.
> Train and evaluate a simple baseline.
> Confirm that the learned system improves over copy-draft.
> Tune addition and removal thresholds independently.
> Validate the final encoded submission.
> 24. Numerical Stability and NaN Prevention
> This task contains sparse targets and many valid no-change regions.
> Some training crops may contain:
> No addition pixels.
> No removal pixels.
> No changed pixels.
> Very few audit pixels.
> Only one active class.
> Loss implementations must handle these cases safely.
> Never Reduce Over an Empty Selection
> A masked loss may become NaN when no pixels are selected.
> Before averaging losses inside the audit region, verify that at least one pixel is selected.
> If no pixel is selected, skip that batch or sample.
> Avoid Division by Zero in Class Weights
> Per-batch class weights are dangerous when one class is absent.
> A calculation that divides the negative count by the positive count becomes infinite when the positive count is zero.
> Participants should:
> Clamp denominators to at least one.
> Limit class weights to a reasonable maximum.
> Consider fixed moderate class weights instead of per-batch weights.
> Fail Immediately on Non-Finite Values
> Before each optimizer update, verify that:
> Model inputs are finite.
> Model outputs are finite.
> The loss is finite.
> Gradients are finite.
> Model parameters remain finite.
> Training should stop immediately if any of these checks fail.
> Participants should not continue training after a NaN or infinite gradient.
> Participants should not use a checkpoint saved after numerical failure.
> Training should restart from clean model weights after the underlying issue is corrected.
> Gradient Clipping
> Gradient clipping may help prevent unstable updates.
> However, clipping does not repair NaN gradients.
> A non-finite gradient must be treated as a failure rather than merely clipped.
> Safe Loss Behavior
> For a three-class model with keep, add, and remove outputs:
> Compute per-pixel loss without reduction.
> Select only pixels allowed by the chosen training mask.
> Confirm that the selection is nonempty.
> Average the selected loss.
> Confirm that the result is finite before backpropagation.
> 25. Prediction Safety
> Before encoding a prediction, participants should enforce all hard constraints.
> The final addition mask should contain only pixels that:
> Were predicted as flood additions.
> Lie inside the audit mask.
> Are non-flood in the draft.
> The final removal mask should contain only pixels that:
> Were predicted as flood removals.
> Lie inside the audit mask.
> Are flood in the draft.
> Any overlap between additions and removals must be removed.
> This filtering should occur even if the model was trained to obey the constraints.
> 26. Submission Validation Guidance
> Before saving the final submission:
> Constrain additions and removals using the audit and draft masks.
> Remove any overlap.
> Encode both masks using one-indexed row-major RLE.
> Preserve empty masks as empty strings.
> Confirm that the CSV columns are exact.
> Confirm that every evaluation identifier appears exactly once.
> Decode every RLE and verify its constraints.
> A recommended validator should confirm:
> The submission has exactly the required columns.
> No case_id is missing.
> No case_id is duplicated.
> No unknown case_id is present.
> All required evaluation identifiers are present.
> Every RLE contains start-length pairs.
> Every start is one-indexed and positive.
> Every run length is positive.
> Every run remains inside the declared dimensions.
> Runs are sorted and do not overlap.
> Addition and removal masks are disjoint.
> All edits are inside the audit mask.
> Additions occur only where the draft is non-flood.
> Removals occur only where the draft is flood.
> 27. Minimal Valid Submission Behavior
> A valid copy-draft submission contains every test case_id and leaves both edit fields empty.
> This produces no additions and no removals.
> Participants should confirm that their complete pipeline can always fall back to this valid output if model training or inference fails.
> A failed model should not be allowed to produce malformed RLE, missing rows, invalid edits, or corrupted outputs.
> 28. Pre-Submission Checklist
> Before finalizing a submission:
> Confirm that the unchanged sample submission produces a valid CSV.
> Evaluate the model on a split grouped by raster_path.
> Stop training immediately if inputs, outputs, loss, gradients, or parameters become non-finite.
> Reload only a checkpoint saved before any numerical failure.
> Apply audit and draft-state constraints before RLE encoding.
> Confirm that addition and removal masks are disjoint.
> Decode and validate every final RLE.
> Confirm that all test identifiers appear exactly once.
> Confirm that the CSV columns are exactly case_id, add_rle, and remove_rle.
> Compare the final model against the copy-draft baseline.
> 29. Research Positioning
> This benchmark studies flood-map repair rather than independent flood segmentation.
> Its defining structure is the combination of:
> A mostly correct draft flood prediction.
> A broad review region rather than direct error prompts.
> Immutable pixels outside that region.
> Separate sparse addition and removal outputs.
> Explicit no-change examples.
> Preservation-aware evaluation.
> Boundary-aware evaluation.
> Component-aware evaluation.
> Robustness-aware aggregation.
> The participant is learning a flood-map intervention policy rather than only predicting a final flood class independently at every pixel.
> 30. Summary
> Evidence-Guided Flood Mask Repair asks a model to inspect an existing flood prediction and determine:
> Which flood and non-flood regions should be trusted.
> Which pixels should be changed.
> Whether a change requires adding or removing flood.
> How far the correction should extend.
> Which valid structures must be preserved.
> Whether the correct action is to make no change.
> The output is a constrained, sparse, directional flood-mask repair plan.
> Submissions are evaluated through:
> Edit accuracy.
> Final flood-mask agreement.
> Boundary fidelity.
> Preservation.
> Connected-component consistency.
> Robustness across cases.
> A successful solution must combine multimodal evidence interpretation, flood-boundary reasoning, terrain awareness, conservative intervention, numerical stability, and strict submission validation.

Inspiration note: Useful for graph/scaffold reconstruction tasks with decoys and consistency scoring.

## Neuromuscular Wiring Recovery from Sensor Sheets

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75v77mxbtgsv9hz2p02krkes8bjr81
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat aneeshm44's score of 0.499!

Full challenge description from page:

> Overview
> Each example is a static diagnostic image built from a synchronized hand recording. Four muscle-activity envelopes appear on the left as displayed electrode slots E0 through E3. Four finger-motion traces appear on the right as F0 through F3.
> The displayed sheet has two calibration faults:
> The four electrode traces have been placed into the wrong slot order.
> Between one and three finger traces have been shifted in time.
> Predict the correction needed to recover the canonical sensor arrangement and the one-to-one muscle-to-finger phase-lock graph:
> | Output | Meaning |
> |---|---|
> | `rewire_permutation` | Which displayed electrode slot belongs in each canonical electrode position |
> | `finger_phase_vector` | Signed phase correction for each displayed finger trace |
> | `phase_lock_graph` | Four canonical electrode-to-finger edges with their best phase-lag bucket |
> This is a computer-vision and structured-decoding challenge. Solvers receive rendered PNG sheets, not raw sensor tables. The target is not the gesture name, participant identity, or movement speed.
> Real-World Motivation
> Wearable sensing systems combine electrodes and motion gloves through independent hardware channels. A connector swap or timing offset can leave every individual trace looking valid while breaking the correspondence needed for hand-pose estimation or musical control. A useful diagnostic system must recover the wiring and timing relationship, not merely flag that a recording is unusual.
> The source recordings were captured with an eight-channel surface-electromyography armband and a twenty-channel instrumented glove. They cover multiple sessions, movement speeds, and general or musical gestures. The prepared split holds out complete participants, which prevents the benchmark from rewarding participant-specific trace memorization.
> Dataset
> The prepared challenge contains 1,100 training sheets and 420 test sheets. Each source recording is used once. Public identifiers and PNG filenames are opaque.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Public inputs and labels for 1,100 examples |
> | `test.csv` | Public inputs for 420 hidden-label examples |
> | `sample_submission.csv` | Schema-valid baseline submission |
> | `sensor_sheets/` | Rendered `1200 x 820` RGB PNG files |
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque identifier matching `^nw[0-9a-f]{22}$` |
> | `sensor_sheet_path` | string path | Relative path to one diagnostic PNG |
> | `calibration_contract` | string | States the displayed slot names and the required canonical-order and phase corrections |
> Sensor Sheet Layout
> All eight traces share a normalized left-to-right recording-time axis.
> | Display area | Contents |
> |---|---|
> | Left column | Four smoothed muscle-activity envelopes labeled `E0` to `E3` |
> | Right column | Motion derivatives for thumb, index, middle, and ring channels, displayed as `F0` to `F3` |
> The four left traces are selected from stable electrode channels and then permuted. The right traces remain attached to their finger labels, but one to three are shifted by a nonzero phase bucket.
> Signals are resampled to 240 visual points. One phase bucket equals four of those points. Positive correction moves a displayed finger trace later along the sheet; negative correction moves it earlier.
> Target Columns
> | Column | Data type | Description |
> |---|---|---|
> | `rewire_permutation` | JSON integer array of length 4 | Displayed slot index for canonical electrodes `e0`, `e1`, `e2`, and `e3` |
> | `finger_phase_vector` | JSON integer array of length 4 | Required correction for `F0` through `F3`, with each entry from `-3` to `3` |
> | `phase_lock_graph` | canonical four-edge string | One-to-one canonical electrode and finger assignment plus lag bucket |
> Rewire Permutation
> The array must be a permutation of [0,1,2,3]. At array position i, the value gives the displayed E slot that should be moved into canonical electrode position ei.
> Example:
> [2,0,3,1]
> This means displayed slot E2 belongs in canonical position e0, displayed E0 belongs in e1, displayed E3 belongs in e2, and displayed E1 belongs in e3.
> The prepared data uses all 23 non-identity permutations.
> Finger Phase Vector
> The four entries correspond to F0, F1, F2, and F3. Valid values are integers from -3 through 3. Between one and three entries must be nonzero.
> Example:
> [0,-2,1,0]
> This applies no correction to F0, shifts F1 earlier by two buckets, shifts F2 later by one bucket, and leaves F3 unchanged.
> | Split | One shifted finger | Two shifted fingers | Three shifted fingers |
> |---|---:|---:|---:|
> | Train | 251 | 513 | 336 |
> | Test | 97 | 201 | 122 |
> Phase-Lock Graph
> The graph is computed from the canonical, unshifted recording. Each finger has exactly one electrode, and every electrode is used once.
> An edge has the form:
> e<electrode>-f<finger>:l<signed_lag>
> Electrode and finger indices range from 0 through 3. Lag values range from -3 through +3 and must include an explicit sign.
> Edges must appear in f0, f1, f2, f3 order:
> e2-f0:l-1>e0-f1:l+0>e3-f2:l+2>e1-f3:l-2
> The maximum accepted graph length is 100 characters.
> Split Isolation
> The source release recommends a complete 15-participant cohort. Twelve complete participants supply training sheets and three different complete participants supply test sheets. Participant groups do not cross the split.
> Submission Format
> Write the final CSV to:
> ./working/submission.csv
> It must contain exactly these columns in exactly this order:
> case_id,rewire_permutation,finger_phase_vector,phase_lock_graph
> Every test case_id must appear once. Extra or reordered columns, duplicate IDs, unknown IDs, missing rows, and extra rows are rejected.
> Example:
> case_id,rewire_permutation,finger_phase_vector,phase_lock_graph
> nwf34a281d55b2d8c14e790a,"[2,0,3,1]","[0,-2,1,0]",e2-f0:l-1>e0-f1:l+0>e3-f2:l+2>e1-f3:l-2
> Evaluation
> Submissions are evaluated with the Sensor Wiring Recovery Score:
> Score =
> 0.32 * RewireScore
> + 0.28 * FingerPhaseScore
> + 0.40 * PhaseLockGraphScore
> Each component is averaged across test rows before the weighted combination. Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> RewireScore
> position_accuracy = matching permutation positions / 4
> exact_permutation = 1 if all four positions match, else 0
> RewireScore =
> 0.15 * position_accuracy
> + 0.85 * exact_permutation
> FingerPhaseScore
> For true vector Y and prediction P:
> entry_proximity_i = max(0, 1 - abs(Y_i - P_i) / 6)
> mean_proximity = mean(entry_proximity_i for i in 0..3)
> exact_phase = 1 if all four entries match, else 0
> FingerPhaseScore =
> 0.18 * mean_proximity
> + 0.82 * exact_phase
> PhaseLockGraphScore
> Let T and P be the four ordered edge sequences.
> edge_F1 = |set(T) intersection set(P)| / 4
> edit_similarity = 1 - token_Levenshtein_distance(T, P) / 4
> exact_graph = 1 if all four ordered edges match, else 0
> PhaseLockGraphScore =
> 0.15 * edge_F1
> + 0.15 * edit_similarity
> + 0.70 * exact_graph
> Because every valid graph has four unique edges, the displayed edge_F1 formula is equivalent to standard set F1. Token Levenshtein insertion, deletion, and substitution cost 1.
> Malformed JSON, non-permutations, out-of-range integers, invalid graph grammar, repeated electrode assignments, wrong edge order, and overlong values receive zero for the affected component. Grading remains finite for schema-valid malformed submissions.
> Reference Validation
> | Check | Result |
> |---|---:|
> | Exact hidden-answer submission | `1.0000` |
> | Packaged sample submission | `0.0768` |
> | Unique rendered sheets | `1,520 / 1,520` |
> | Train-test participant overlap | `0` |
> | Train-test sheet-hash overlap | `0` |
> | Non-identity rewire permutations represented in train | `23 / 23` |
> | Non-identity rewire permutations represented in test | `23 / 23` |
> Method Requirements
> Solutions must run within the CPU-only time limit. Image encoders, trace extraction, cross-correlation features, assignment algorithms, structured decoders, and CPU-compatible ensembles are allowed when trained or calibrated only with public training data.
> What Not To Use
> Do not use case_id, filenames, row order, media hashes, or file sizes as target predictors.
> Do not identify or match public sheets to original participant recordings outside the supplied challenge data.
> Do not use private answers, hidden split artifacts, grader internals, or submission feedback as labels.
> Do not perform participant lookup, test-label adaptation, or per-test memorization.
> Do not exploit duplicate rows, extra columns, malformed JSON, or excessive parser inputs.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Crystallization Field Object Cell Audit

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73kfgqtzf66cwv5schfs1kq58b2j7a
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: image, feature-engineering, Dataset source is visible after the challenge closes., Leaderboard
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview
> Each example is a microscope image from a crystallization screening field. The image may contain a liquid drop and small crystal objects. Your task is to recover the annotation-defined object audit for the image: how many annotated objects are present, whether they are drops or crystals, which coarse grid cells they touch, and a compact card for each annotated object.
> This is not a request to mark every bright speck in the image. The target follows the annotation layer, so some visual debris may be unlabelled while clear drop and crystal objects are counted. Correct outputs need the image appearance and geometry of annotated drops and crystals to match the required structured JSON.
> Dataset
> The provided files are:
> train.csv: 260 labelled examples.
> test.csv: 250 unlabelled examples.
> sample_submission.csv: A valid low-scoring submission that demonstrates the required file format.
> images/: Resized microscope JPEG images referenced by train.csv and test.csv.
> Columns in train.csv:
> id (string): Unique row id.
> image (string): Relative path to the image file.
> prompt (string): Natural-language task instruction.
> answer_format_json (JSON object as string): Defines the image size [512,512], grid [24,24], valid classes drop and crystal, valid area bins, and required answer fields.
> answer_json (JSON object as string): Ground-truth inventory for training rows.
> test.csv has the same columns except answer_json.
> The required answer_json object has these fields:
> object_count (integer): Total number of annotated objects.
> class_counts (object): Counts by class, using keys drop and/or crystal.
> area_counts (object): Counts by object area bin. Valid bins are tiny, small, medium, large, and field.
> occupied_cells (list of strings): 24 by 24 grid cells touched by any annotated object mask, encoded as r00c00 through r23c23.
> drop_cells (list of strings): Grid cells touched by annotated drop masks.
> crystal_cells (list of strings): Grid cells touched by annotated crystal masks.
> object_cards (list of objects): One card per annotated object. Each card contains label, bbox, center_cell, and area_bin.
> An object card looks like:
> {"label":"crystal","bbox":[120,88,166,140],"center_cell":"r05c06","area_bin":"small"}
> bbox is [x0,y0,x1,y1] in the 512 by 512 image, inclusive pixel coordinates.
> Evaluation
> The score is the mean row score over all test rows. Each row score is between 0 and 1.
> For a set field such as occupied_cells, precision is:
> |predicted_cells intersect true_cells| / |predicted_cells|
> Recall is:
> |predicted_cells intersect true_cells| / |true_cells|
> The set F1 is 2 * precision * recall / (precision + recall). If both sets are empty, the F1 is 1. If only one set is empty, the F1 is 0.
> Count dictionaries are expanded into multisets before computing the same F1 formula. For example, {"crystal": 2, "drop": 1} becomes the multiset [crystal, crystal, drop].
> The object-card score uses two duplicate-aware multiset F1 scores:
> coarse_object_f1 compares (label, center_cell, area_bin).
> fine_object_f1 compares (label, center_cell, area_bin, quantized_bbox), where each bbox coordinate is rounded to a 32-pixel bin.
> object_score = 0.65 * coarse_object_f1 + 0.35 * fine_object_f1
> The cell score is:
> cell_score =
> 0.45 * F1(occupied_cells)
> + 0.25 * F1(drop_cells)
> + 0.30 * F1(crystal_cells)
> The object-count score is:
> count_score = 1                         if predicted_count == true_count
> count_score = max(0, 1 - abs(predicted_count - true_count) / max(1, true_count)) otherwise
> The complete row score is:
> row_score =
> 0.12 * count_score
> + 0.16 * F1(class_counts)
> + 0.12 * F1(area_counts)
> + 0.25 * cell_score
> + 0.35 * object_score
> Malformed JSON or invalid field values receive 0 for that row. A submission with wrong columns, missing rows, extra rows, duplicate ids, or ids not matching the test set is rejected.
> Submission
> Submit a CSV file with exactly two columns:
> id (string)
> answer_json (JSON object serialized as a CSV string)
> Example:
> id,answer_json
> crdrop_example_01,"{""object_count"":1,""class_counts"":{""drop"":1},""area_counts"":{""medium"":1},""occupied_cells"":[""r10c10""],""drop_cells"":[""r10c10""],""crystal_cells"":[],""object_cards"":[{""label"":""drop"",""bbox"":[205,205,305,305],""center_cell"":""r12c12"",""area_bin"":""medium""}]}"
> crdrop_example_02,"{""object_count"":0,""class_counts"":{},""area_counts"":{},""occupied_cells"":[],""drop_cells"":[],""crystal_cells"":[],""object_cards"":[]}"
> What Not To Use
> Do not use GPU acceleration.
> Do not use external datasets, additional checkpoints, or pretrained vision models.
> Do not use hosted inference APIs, remote OCR/vision services, or remote-code loaders.
> Do not include additional model weights, training corpora, or external annotation files.
> Do not search for matching images, external metadata, or external annotation files outside the provided files.
> Do not hardcode row ids, image hashes, or answer strings.
> Do not use files outside the provided public files at prediction time.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Masked Row-Plot Window Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72mh6tzxh5wvg4sw7e5gbq2x8awtnk
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: feature-engineering, image, Dataset source is visible after the challenge closes., Leaderboard
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview
> Each row gives a prepared overhead image of a small crop-row plot and a partially filled worksheet for that image. One 4 by 6 rectangle of worksheet cells has been blanked out. Your job is to repair that hidden window: report which hidden cells contain visible plant centers, how crowded each occupied hidden cell is, and which plant category is dominant in that cell.
> The worksheet uses a 12 by 12 grid laid over the image. The released part of the worksheet gives the crowding and dominant-category values outside the hidden rectangle, so the prediction should be consistent with both the image and the visible worksheet context.
> The images contain crop plants and several weed types in overhead field views. Public row ids and filenames are remapped, and original collection identifiers are not included.
> Dataset
> File manifest:
> File	Contents
> train.csv	385 examples with image paths, damaged worksheet windows, output constraints, and ground-truth answer_json.
> test.csv	250 examples with image paths, damaged worksheet windows, and output constraints.
> sample_submission.csv	Low-information valid submission showing the required two-column CSV format.
> images/	Prepared 384 by 256 row-plot images referenced by the CSV files.
> CSV columns:
> Column	Type	Meaning
> id	string	Public row identifier.
> image	string	Relative path to the row-plot image.
> prompt	string	Short task instruction.
> damaged_window_json	JSON string	Visible worksheet values and the coordinates of the hidden 4 by 6 window.
> answer_format_json	JSON string	Required output fields and allowed values.
> answer_json	JSON string	Ground-truth repair object for training rows only.
> Fields inside damaged_window_json:
> Field	Type	Meaning
> image_size	list of integers	[width,height], always [384,256].
> worksheet_grid	list of integers	[rows,columns], always [12,12].
> hidden_window	object	Location and cell names for the blanked 4 by 6 worksheet region.
> hidden_window.top_row	integer	Top row index of the hidden rectangle.
> hidden_window.left_col	integer	Left column index of the hidden rectangle.
> hidden_window.height	integer	Hidden window height, always 4.
> hidden_window.width	integer	Hidden window width, always 6.
> hidden_window.cells	list of strings	The 24 hidden cell names, such as r04_c07, in row-major order.
> unknown_value	integer	Placeholder value -1 used inside the hidden rectangle.
> visible_crowding_grid	list of 144 integers	Row-major worksheet grid outside the hidden window. Values are 0, 1, 2, 3, or -1 for hidden cells.
> visible_dominant_code_grid	list of 144 integers	Row-major dominant-code grid outside the hidden window. Code 0 means empty, codes 1 to 5 are plant categories, and -1 marks hidden cells.
> visible_occupied_cell_count	integer	Number of occupied cells outside the hidden window.
> visible_dominant_code_totals	object	Counts of visible occupied cells by category outside the hidden window.
> Fields inside answer_format_json:
> Field	Type	Meaning
> required_fields	list of strings	Required keys in each submitted answer_json.
> hidden_window_cell_count	integer	Number of cells in the hidden window, always 24.
> cell_name_format	string	Cell-name format, for example r00_c00.
> crowding_bin_values	list of integers	Allowed crowding values for occupied hidden cells: 1, 2, or 3.
> dominant_codebook	object	Maps integer codes to category names. Code 0 means empty; submitted occupied cells must use codes 1 to 5.
> dominant_code_values_for_hidden_occupied_cells	list of integers	Valid dominant codes for submitted occupied hidden cells.
> The required answer_json object has:
> Field	Type	Meaning
> missing_occupied_cell_count	integer	Number of occupied cells inside the hidden window.
> missing_dominant_code_totals	object	Counts of occupied hidden cells by category name.
> hidden_occupied_cells	list of objects	One object for each occupied hidden cell. Empty hidden cells are omitted.
> Each hidden_occupied_cells item contains:
> Field	Type	Meaning
> cell	string	Hidden worksheet cell such as r04_c07.
> crowding_bin	integer	1, 2, or 3, where 3 means three or more centers in that cell.
> dominant_code	integer	Dominant category code from 1 to 5.
> Evaluation
> The score is the mean of the per-row repair scores. Higher is better:
> row_score =
> 0.10 * missing_count_score
> + 0.14 * dominant_total_score
> + 0.16 * occupied_cell_f1
> + 0.36 * occupied_cell_triple_f1
> + 0.12 * crowding_accuracy
> + 0.12 * dominant_code_accuracy
> missing_count_score compares the predicted and true number of occupied hidden cells:
> missing_count_score =
> 1 - abs(predicted_count - true_count)
> / (predicted_count + true_count)
> If both counts are zero, the score is 1.
> dominant_total_score applies the same count formula to the five-category totals:
> dominant_total_score =
> 1 - sum_k abs(predicted_total_k - true_total_k)
> / sum_k (predicted_total_k + true_total_k)
> If both total dictionaries are all zero, the score is 1.
> occupied_cell_f1 is set F1 over the submitted occupied hidden-cell names:
> occupied_cell_f1 =
> 2 * |predicted_cells intersect true_cells|
> / (|predicted_cells| + |true_cells|)
> occupied_cell_triple_f1 is set F1 over exact triples (cell, crowding_bin, dominant_code).
> crowding_accuracy is the fraction of true occupied hidden cells whose submitted crowding_bin is correct. Missing true cells count as incorrect. If there are no true occupied hidden cells, an empty prediction receives 1 and a non-empty prediction receives 0.
> dominant_code_accuracy is computed the same way using dominant_code.
> The grader checks internal consistency before scoring each row. missing_dominant_code_totals must sum to missing_occupied_cell_count; hidden_occupied_cells must have that same length; cells cannot be duplicated; crowding bins must be 1, 2, or 3; dominant codes must be 1 through 5; and the dominant-code counts implied by hidden_occupied_cells must match missing_dominant_code_totals. Malformed JSON or an invalid row scores 0 for that row. Wrong columns, extra columns, missing rows, duplicate ids, or ids that do not match the test set make the whole submission invalid.
> Submission
> Submit a CSV with exactly two columns:
> id (string): must match the ids in test.csv; row order is not used by the grader.
> answer_json (JSON string): predicted repair object using the schema above.
> Example:
> id,answer_json
> rowwin_example_001,"{""missing_occupied_cell_count"":2,""missing_dominant_code_totals"":{""maize"":1,""amaranth"":0,""barnyard_grass"":1,""quickweed"":0,""weed_other"":0},""hidden_occupied_cells"":[{""cell"":""r04_c07"",""crowding_bin"":1,""dominant_code"":1},{""cell"":""r05_c08"",""crowding_bin"":2,""dominant_code"":3}]}"
> rowwin_example_002,"{""missing_occupied_cell_count"":1,""missing_dominant_code_totals"":{""maize"":0,""amaranth"":0,""barnyard_grass"":0,""quickweed"":0,""weed_other"":1},""hidden_occupied_cells"":[{""cell"":""r08_c02"",""crowding_bin"":1,""dominant_code"":5}]}"
> What Not To Use
> Do not use external row-plot, agronomy-image, or overhead-field datasets.
> Do not search the web for matching images or source metadata.
> Do not submit memorized repair objects for individual test ids.
> Do not use GPU acceleration.
> Do not use pretrained agronomy-image, overhead-field, or vegetation-analysis models.
> Do not use hosted vision APIs.
> Do not install packages at runtime.
> Do not use additional model checkpoints, torch.hub, or trust_remote_code.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Vineyard Berry Load Grid And Cluster Census

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bnyn5nwtcbk0pne0p7v085h8arwtx
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> You are given a color vineyard image showing grape bunches at varying scales, occlusions, and distances. The task is to recover a compact crop-load census from the image: total annotated berry count, total annotated grape-bunch count, a 20 rows by 12 columns berry-density grid, and coarse bunch cards for the annotated grape regions.
> Good submissions need to combine small-point evidence from visible berries with higher-level bunch geometry. The output is not a free-form segmentation mask: it is a structured agronomy record containing row-major density bins, hotspot cells, area-bin counts, and normalized bunch boxes. The images are re-encoded during preparation, with anonymized row ids and filenames.
> Dataset
> train.csv: 992 labeled examples with id, image_path, prompt, context_json, answer_format_json, and answer_json.
> test.csv: 320 unlabeled examples with id, image_path, prompt, context_json, and answer_format_json.
> sample_submission.csv: a valid low-scoring example submission.
> images/: resized JPEG vineyard images referenced by image_path.
> Columns:
> id (string): anonymized row id.
> image_path (string): relative path to the stored image.
> prompt (string): task instruction.
> context_json (JSON string): stored image size and grid dimensions.
> answer_format_json (JSON string): required grid length, valid density values, valid area bins, and bounding-box format.
> answer_json (JSON string, train only): target berry-density and cluster-geometry record.
> Each answer_json contains:
> berry_count (integer): number of annotated berry center points.
> cluster_count (integer): number of annotated grape-cluster regions.
> density_grid (list of 240 integers): row-major 20 rows by 12 columns grid. Values are density bins: 0 for empty, 1 for 1-2 berries, 2 for 3-5 berries, 3 for 6-10 berries, and 4 for more than 10 berries.
> hotspot_cells (list of strings): grid cells with at least 6 annotated berries.
> cluster_area_counts (object): count of annotated grape clusters in small, medium, large, and very_large area bins.
> cluster_cells (list of strings): grid cells containing annotated cluster centers.
> cluster_cards (list of objects): one object per annotated grape cluster, with normalized bbox, center_cell, and area_bin.
> Bounding boxes use [x_min, y_min, x_max, y_max] normalized to the stored image.
> The target follows the provided annotation layer. Some cluster boxes may be coarse, overlapping, or cover partially occluded grape bunches when that is how the released annotation represents the cluster.
> Evaluation
> The final score is the mean row score over the test rows used for scoring. Scores range from 0 to 1, and higher is better.
> For each row:
> row_score =
> 0.10 * berry_count_score
> + 0.10 * cluster_count_score
> + 0.34 * density_grid_score
> + 0.08 * hotspot_cell_f1
> + 0.10 * cluster_area_count_f1
> + 0.08 * cluster_cell_f1
> + 0.20 * cluster_card_f1
> For either count field:
> count_score = max(0, 1 - abs(predicted_count - true_count) / max(1, predicted_count, true_count))
> density_grid_score = 0.35 * exact_cell_accuracy + 0.65 * active_bin_macro_iou. Exact cell accuracy is the fraction of the 240 grid cells where the predicted bin equals the hidden bin. Active-bin macro IoU is the mean IoU over nonzero density bins that appear in the hidden grid. For a density bin b, IoU is |predicted_cells_b intersect true_cells_b| / |predicted_cells_b union true_cells_b|.
> hotspot_cell_f1 and cluster_cell_f1 are standard set F1 over submitted and hidden grid-cell strings.
> cluster_area_count_f1 is multiset F1 over area-bin counts. The overlap is sum_b min(predicted_count_b, true_count_b), precision is overlap divided by total predicted count, recall is overlap divided by total hidden count, and F1 is the harmonic mean.
> cluster_card_f1 greedily matches predicted cluster cards to hidden cards. Pair score is:
> 0.30 * area_bin_exact + 0.25 * center_cell_exact + 0.45 * bbox_iou
> Matched pair scores are summed, then converted to F1 using predicted-card precision and hidden-card recall.
> Malformed JSON or a non-compliant answer_json receives 0 for that row. Wrong columns, duplicate ids, missing rows, extra rows, or ids that do not match the test set are rejected.
> Submission
> Submit a CSV with exactly two columns: id and answer_json. The submitted ids must match test.csv; row order is not used by the grader.
> Example:
> id,answer_json
> vine_11111111111111,"{""berry_count"":0,""cluster_count"":0,""density_grid"":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],""hotspot_cells"":[],""cluster_area_counts"":{},""cluster_cells"":[],""cluster_cards"":[]}"
> vine_22222222222222,"{""berry_count"":0,""cluster_count"":1,""density_grid"":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],""hotspot_cells"":[],""cluster_area_counts"":{""small"":1},""cluster_cells"":[],""cluster_cards"":[{""bbox"":[0.45,0.45,0.55,0.58],""center_cell"":""r10c06"",""area_bin"":""small""}]}"
> What Not To Use
> Do not use GPU acceleration.
> Do not use vineyard, grape, fruit-counting, or plant-detection datasets outside the released files.
> Do not use pretrained detector/segmenter checkpoints, added model weights, or extra training corpora.
> Do not use hosted vision APIs, remote counting services, runtime package installation, or remote-code loaders.
> Do not match test images against web images, source archives, or external annotation files.
> Do not hard-code berry counts, cluster cards, image hashes, or answers for particular test ids.
> At prediction time, use only the files released in the public package.
> Submissions
> 36

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Multi-View Archaeological Dossier Matching

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7aze3699n0xj0gaqaej8n6m18c1nhr
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Multi-View Archaeological Dossier Matching
> Overview
> Build a CPU-only computer-vision system that reattaches an orphaned archaeological field photograph to the correct multi-photograph site dossier.
> Field archives are often assembled across cameras, survey days, storage devices, and later digitization projects. A photograph can remain visually intact after its filename, folder association, or catalogue link is lost. An archivist then has to compare persistent evidence such as terrain, masonry, carving, soil, vegetation, surface remains, damage patterns, monument geometry, and surrounding landscape against existing site records, and must be able to conclude that none of the proposed records is a defensible match.
> Each row contains:
> one square query photograph whose catalogue association is unknown
> one dossier sheet containing six candidate site cards
> for training rows, the correct candidate slot or none
> Every candidate card contains two different photographs of the same candidate archaeological location. The two panels are independent photographic observations, not two crops or renditions of one photograph. When a candidate is the correct match, the query photograph is also a different photographic observation from both images in that card. A positive decision therefore requires reasoning across three distinct views of a location.
> The six candidate identities change on every row, and all final-test locations are absent from the training locations. A model must learn a transferable relation: whether a query view and a two-view candidate dossier plausibly document the same place. The none outcome makes the task open-set and requires calibrated evidence rather than forced nearest-neighbour selection.
> The two photographs inside a candidate card do not have fixed semantic roles such as overview/detail, and their order carries no target meaning. They can differ strongly in viewpoint, scale, visible archaeological feature, lighting, vegetation, occlusion, or surrounding context. Consequently, a strong model should combine evidence across the pair rather than expect pixel alignment or require both references to resemble the query equally well.
> Your complete solution must run on CPU and finish within 1.5 hours, including training, validation, inference, calibration, and writing the submission. The intended memory limit is 62 GB RAM.
> Dataset
> dataset/public/
> â”œâ”€â”€ train.csv
> â”œâ”€â”€ test.csv
> â”œâ”€â”€ sample_submission.csv
> â””â”€â”€ images/
> â”œâ”€â”€ query/
> â”‚   â””â”€â”€ <opaque_name>.jpg
> â””â”€â”€ dossier/
> â””â”€â”€ <opaque_name>.jpg
> All public filenames and row identifiers are opaque. Public JPEGs have standardized dimensions, contain no EXIF payload, and use independent mild crop, rotation, photometric, blur, and JPEG perturbations. Horizontal mirroring is not used because left-right site geometry can be meaningful.
> Dossier geometry
> A dossier sheet is exactly 672 Ã— 648 pixels. It contains a fixed 3-column Ã— 2-row grid of six 224 Ã— 324-pixel candidate cards in row-major order:
> â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
> â”‚  slot_0  â”‚  slot_1  â”‚  slot_2  â”‚
> â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
> â”‚  slot_3  â”‚  slot_4  â”‚  slot_5  â”‚
> â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
> Each card contains two 224 Ã— 160-pixel photographs separated by a 4-pixel horizontal divider:
> â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
> â”‚ reference photograph Aâ”‚  224 Ã— 160
> â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤  4-pixel divider
> â”‚ reference photograph Bâ”‚  224 Ã— 160
> â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
> Photographs A and B are different photographic observations of the same candidate location. They are not an overview/detail pair generated from a common image. There are no printed slot labels or location names in the dossier sheet; the names above describe the fixed pixel regions only.
> A query image is exactly 384 Ã— 384 pixels.
> train.csv
> id,query_image,dossier_sheet,target
> Columns:
> id
> Data type: string
> Opaque identifier, unique within train.csv.
> query_image
> Data type: relative path string
> Path to the orphaned query photograph under dataset/public/.
> dossier_sheet
> Data type: relative path string
> Path to the six-card candidate sheet under dataset/public/.
> target
> Data type: categorical string
> One of:
> slot_0, slot_1, slot_2, slot_3, slot_4, slot_5, none
> slot_k means that both photographs in card k document the same archaeological location as the query, although all three are different photographic views. none means that the query's location is absent from all six candidate cards.
> test.csv
> id,query_image,dossier_sheet
> The columns have the same meaning as in train.csv, but the target is hidden. The test rows come from archaeological locations that do not occur in the training rows. This tests transfer rather than unseen-label guessing: the output labels are always the same seven row-local decisions, and every row supplies the candidate visual evidence needed to make that decision.
> The public split contains exactly:
> training rows: 1,000
> test rows:       400
> Every test id must appear exactly once in the submission.
> sample_submission.csv
> id,p_slot_0,p_slot_1,p_slot_2,p_slot_3,p_slot_4,p_slot_5,p_none
> The sample assigns probability 1/7 to every outcome. It is format-valid and scores exactly 0.0; it is only a serialization and column-order example.
> Submission format
> Write predictions to:
> working/submission.csv
> The file must contain exactly these columns in this order:
> id,p_slot_0,p_slot_1,p_slot_2,p_slot_3,p_slot_4,p_slot_5,p_none
> For every row:
> all seven probabilities must be finite numeric values;
> every probability must be in [0, 1];
> the seven probabilities must sum to 1 within absolute tolerance 1e-6.
> Rows may appear in any order. Missing IDs, unknown IDs, duplicate IDs, missing values, non-finite values, out-of-range values, extra columns, and invalid probability sums are rejected rather than repaired or scored.
> Example:
> id,p_slot_0,p_slot_1,p_slot_2,p_slot_3,p_slot_4,p_slot_5,p_none
> arc_96b5b079d23935fde7628e,0.05,0.10,0.62,0.07,0.05,0.04,0.07
> arc_67b5b079d23935fde7629f,0.05,0.10,0.62,0.07,0.05,0.04,0.07
> Evaluation
> The score measures retrieval quality, open-set calibration, and ranking quality. It ranges from 0.0 to 100.0 and is maximized.
> Let K = 7, let y be the true outcome index, and let p_y be its submitted probability.
> For each row, compute:
> nll = -ln(max(p_y, 1e-15))
> brier = Î£[k=0..6] (p_k - 1[k = y])Â²
> Two tie-aware ranking credits are also computed:
> top1_credit: expected top-1 correctness if outcomes with equal maximum probability are ordered uniformly at random;
> top2_credit: expected inclusion of the true outcome in the first two positions if a probability tie crosses the top-2 boundary.
> Thus a seven-way uniform row receives exactly 1/7 top-1 credit and 2/7 top-2 credit, rather than receiving an arbitrary advantage from column order.
> Rows are first averaged within their archaeological location, and those location averages are then averaged without weighting. This location-macro aggregation prevents a heavily photographed location from dominating the score.
> Call the resulting four macro quantities:
> macro_nll
> macro_brier
> macro_top1
> macro_top2
> They are converted to chance-referenced skills:
> log_skill = clip(1 - macro_nll / ln(7), 0, 1)
> brier_skill = clip(1 - macro_brier / (6/7), 0, 1)
> top1_skill = clip((macro_top1 - 1/7) / (6/7), 0, 1)
> top2_skill = clip((macro_top2 - 2/7) / (5/7), 0, 1)
> where:
> clip(x, 0, 1) = min(1, max(0, x))
> The final score is:
> 100 Ã— (
> 0.40 Ã— log_skill
> + 0.30 Ã— brier_skill
> + 0.20 Ã— top1_skill
> + 0.10 Ã— top2_skill
> )
> Not allowed
> External APIs or remote inference services.
> External archaeological photograph collections, site catalogues, maps, coordinates, survey records, annotations, or location labels.
> Manual matching or manual annotation of test rows.
> Using visible textual identifiers in the public images as a substitute for visual archaeological matching.
> Hard-coding predictions by test ID.
> Exploiting row order, JPEG serialization, opaque filenames, preparation implementation details, or evaluator behavior instead of modeling the visual relation.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## BlindSpot Ledger: Object Visibility Forecasting

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f286qrrnxrpm2rpm3jrj4mx8c0ybz
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Moving a camera through a cluttered scene changes more than object appearance. Some objects become visible, others disappear behind neighboring objects, and the apparent location and scale of every surviving object shift with viewpoint. A system that only recognizes what is currently visible cannot anticipate what the next camera will actually observe.
> Each BlindSpot Ledger example contains three RGB context views, called A, B, and C, of one static physical scene. Object boxes and a verified identity ledger across those three views are provided. The camera then follows a two-step route from C to an unseen view D and from D to an unseen view E. The images for D and E are never provided to participants.
> The task is to forecast the future observation state of every tracked physical object. For each object and each unseen view, predict whether it will be visible. If visible, also predict the region of the image in which its bounding-box center will appear and its apparent scale.
> This is not image classification, target-image matching, object detection, multi-view association, or novel-view image generation. The output is a structured, variable-length ledger of future object observations rather than pixels, poses, or matches against a target view. The model must infer viewpoint-conditioned visibility and coarse projection from previously observed appearance, multi-view context, occlusion patterns, and the requested camera route.
> Source Representation
> Each example provides three context images:
> view A - the earliest observed camera position;
> view B - the second observed camera position;
> view C - the final observed camera position.
> Every detected object box has a row-local anonymous identifier such as A03, B11, or C07. The fields boxes_a, boxes_b, and boxes_c are independently JSON-encoded lists of box records. Every box record contains:
> box_id - row-local anonymous box identifier;
> x1 - normalized left coordinate;
> y1 - normalized top coordinate;
> x2 - normalized right coordinate;
> y2 - normalized bottom coordinate.
> Coordinates lie in [0, 1] relative to the corresponding image width and height.
> Example box list:
> [ {"box_id":"A00","x1":0.061,"y1":0.214,"x2":0.173,"y2":0.481}, {"box_id":"A01","x1":0.208,"y1":0.337,"x2":0.354,"y2":0.692} ]
> The context_groups field is a JSON-encoded identity ledger for the observed views. Each record contains one row-local track_id and the corresponding boxes from A, B, and C. JSON null means that the object is not visible in that context view.
> Example:
> [ {"track_id":"T00","a":"A03","b":"B11","c":"C07"}, {"track_id":"T01","a":"A05","b":"B02","c":null}, {"track_id":"T02","a":null,"b":"B06","c":"C04"} ]
> Every supplied context box appears exactly once in context_groups. Track identifiers are randomized independently within each example and contain no object, camera, category, or ordering information.
> The requested route is supplied through route_cd and route_de. Both fields use this fixed eight-label vocabulary:
> F - approximately forward;
> FR - forward-right;
> R - right;
> BR - back-right;
> B - approximately backward;
> BL - back-left;
> L - left;
> FL - forward-left.
> route_cd describes the horizontal transition from context view C to unseen view D. route_de describes the following transition from D to unseen view E.
> Challenge Construction
> Each challenge example is constructed from five ordered camera observations of one static physical scene. Views A, B, and C become participant inputs. Views D and E remain hidden and supply only the organizer targets. No pixels, crops, filenames, or box lists from D or E are released.
> A physical object is eligible for tracking only when it is visible in at least one of A, B, or C. An object that first appears in D or E but is absent from every context view is outside the prediction set. From the eligible objects, each route request contains a bounded ledger subset chosen to preserve varied future visibility patterns and control row length. Objects outside that ledger may remain visible as unboxed scene context, but they never require predictions. Every submitted track_id therefore has direct visual evidence in the participant input while still requiring extrapolation to unseen viewpoints.
> For each tracked object, the hidden annotations determine:
> whether it is visible in D;
> whether it is visible in E;
> the grid cell containing its bounding-box center when visible;
> its apparent scale bin when visible.
> Training and test data are separated at the physical-scene level. All camera observations, box annotations, and routes derived from one scene remain entirely in one partition. Image hashes and visual-near-duplicate checks prevent the same observation from appearing across partitions. Public identifiers, box identifiers, and track identifiers are assigned after splitting.
> Every physical scene contributes exactly four route requests. The four rows share the same A-B-C context and query four selected hidden D-E paths. All four requests always remain in the same partition. Their row and track identifiers are independently randomized, so repeated context pixels provide no cross-partition answer lookup.
> The proposed release contains 5,000 examples in total:
> 4,000 labeled training examples;
> 1,000 unlabeled test examples, divided into 500 public-leaderboard rows and 500 private-leaderboard rows.
> The test rows come from 250 held-out physical scenes, with exactly four route-request rows per scene.
> Exactly 125 complete scenes are assigned to the public partition and 125 complete scenes are assigned
> to the private partition. Therefore, each partition contains 125 scenes x 4 routes = 500 rows, and
> the complete test set contains 1,000 rows. No scene is split between the two. The assignment is deterministic and balanced against the pre-registered
> shortcut ladder plus three organizer CPU reference solvers described in Evaluation. It is never
> fitted to participant submissions.
> Every example contains exactly three public images but a variable number of tracked objects. Scene density, camera displacement, visibility overlap, stacking, and the number of similar-looking objects vary across examples.
> The task differs materially from multi-view association. Participants receive the complete association ledger for the available images, and there is no target image against which to match an object. The prediction unit is the future observation state under a requested camera route: a tracked object can remain visible, disappear, reappear, move to a new image region, or change apparent scale across D and E.
> Target Language
> The training target future_states is a JSON-encoded list containing exactly one record for every track_id in context_groups.
> Each record has this structure:
> { "track_id":"T00", "d":{"visible":1,"cell":17,"scale":"M"}, "e":{"visible":0,"cell":null,"scale":null} }
> visible is an integer:
> 1 - the tracked physical object is visible in the unseen view;
> 0 - the object is outside the image or fully occluded.
> When visible is 1, cell identifies the location of the hidden bounding-box center on a 6 x 6 grid. Cells are numbered in row-major order from 0 to 35:
> 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35
> For a normalized box center (cx, cy), compute the values as follows:
> row    = min(5, floor(6 multiplied by cy))
> column = min(5, floor(6 multiplied by cx))
> cell   = (6 multiplied by row) + column
> When visible is 1, scale describes normalized bounding-box area. Compute a as the box width multiplied by the box height: (x2 - x1) multiplied by (y2 - y1).
> S - a < 0.012;
> M - 0.012 <= a < 0.045;
> L - a >= 0.045.
> When visible is 0, both cell and scale must be JSON null.
> Record order does not affect the score. Every context track_id must appear exactly once, and no unknown track identifier may appear.
> What The Task Requires
> A competitive solver must build one representation for each physical object from all context views in which it appears. It must combine the central object crop with surrounding scene structure because identical-looking objects can have different visibility outcomes after the camera moves.
> The model must learn how route direction interacts with the current location, apparent scale, partial occlusion, and neighboring objects. An object near an image boundary may leave the field of view. An object hidden in C may reappear after a lateral move. Two objects at similar image coordinates may behave differently because one is elevated, stacked, or blocked from the requested viewpoint.
> The two prediction horizons are coupled. A track can follow one of four visibility patterns across D and E: hidden-hidden, hidden-visible, visible-hidden, or visible-visible. Predicting each horizon with unrelated fixed rules ignores this structure and is explicitly measured by the evaluation.
> The challenge is designed for CPU training and inference. Object detection and observed-view identity association are removed from the learning problem. A practical solution can fine-tune a lightweight visual encoder on object and context crops, aggregate features across A-B-C, combine them with route and box-geometry features, and train small classification heads for visibility, grid cell, and scale. Global scene features can help model competition and occlusion between tracked objects.
> What Not To Use
> Do not use private labels, organizer answer files, grader feedback, manually assigned test targets, or repeated leaderboard probing.
> Do not use id, CSV row order, local box numbering, track numbering, filenames, path strings, JSON order, track count, or parser failures as predictive shortcuts. These fields are randomized or structurally validated and carry no hidden-view information.
> Do not search external image collections, recover hidden camera images, link test examples to private annotations, or construct an answer lookup. Do not manually inspect and label the test set.
> Do not submit a constant future ledger, fixed route table, hand-written projection rule, fabricated pseudo-answer key, or manually selected coordinates. Predictions must be produced by a model trained on the provided labeled examples.
> Openly licensed pretrained feature extractors may be used, subject to platform resource rules and their own licenses. The final predictor must learn from the provided training data and generalize to unseen physical scenes.
> Dataset Files
> The public participant release contains:
> train.csv - 4,000 examples with participant features and future_states targets;
> test.csv - 1,000 examples with the same participant features and no target;
> sample_submission.csv - every test ID and the required prediction column;
> train_images/ - three JPEG context images for every training ID;
> test_images/ - three JPEG context images for every test ID.
> The public file structure is:
> public/ train.csv test.csv sample_submission.csv train_images/ <id>_A.jpg <id>_B.jpg <id>_C.jpg test_images/ <id>_A.jpg <id>_B.jpg <id>_C.jpg
> For a row with identifier <id>, the three context images are <id>_A.jpg, <id>_B.jpg, and <id>_C.jpg in the corresponding image directory.
> The grader additionally receives private/answers.csv. It contains only id and the hidden future_states targets required for scoring. Participants do not receive this file.
> CSV Columns
> train.csv contains:
> id (string) - opaque unique example identifier;
> boxes_a (string containing JSON) - box records for context view A;
> boxes_b (string containing JSON) - box records for context view B;
> boxes_c (string containing JSON) - box records for context view C;
> context_groups (string containing JSON) - verified observed-view identity ledger;
> route_cd (string) - requested transition from C to unseen D;
> route_de (string) - requested transition from D to unseen E;
> future_states (string containing JSON) - training-only target ledger.
> test.csv contains the same participant feature columns except future_states.
> sample_submission.csv contains:
> id (string) - test example identifier;
> future_states (string containing JSON) - predicted hidden-view ledger.
> Use a JSON parser for every JSON-valued CSV cell. Do not parse JSON with regular expressions or manual string splitting.
> Evaluation
> Higher is better. The final score lies in [0.001, 1.0] and rewards four aspects of the future ledger.
> Visibility Macro F1
> The grader collects all (track_id, horizon) visibility decisions, where horizon is D or E. It computes binary F1 separately for the visible and hidden classes, then averages the two class F1 values. This prevents a submission from scoring well by predicting the majority visibility state everywhere.
> Spatial Proximity
> Spatial proximity is evaluated only when the object is truly visible. A predicted hidden state receives zero spatial credit for that object-horizon pair. Otherwise, let m be the Manhattan distance between the predicted and true cells on the 6 x 6 grid. The pair receives:
> spatial_pair = exp(-m / 1.5)
> An exact cell receives 1.0, a nearby cell receives partial credit, and a distant cell approaches zero. Spatial proximity is the mean over all truly visible object-horizon pairs.
> Scale Accuracy
> Scale accuracy is evaluated over truly visible object-horizon pairs. A pair receives 1 only when the submission predicts visible and supplies the correct S, M, or L label. Predicting hidden or the wrong scale receives 0.
> Two-Step Pattern Accuracy
> For each track, the grader compares the complete two-bit visibility pattern [visible_d, visible_e]. A track receives 1 only when both horizon states are correct. Pattern accuracy is the mean over all tracks.
> The grader computes:
> core_score = 0.50 * visibility_macro_f1 + 0.35 * spatial_proximity + 0.15 * scale_accuracy consistency_factor = 0.60 + 0.40 * pattern_accuracy raw_score = core_score * consistency_factor skill_score = (raw_score - 0.25092408163309765) / 0.7490759183669023 final_score = clip(skill_score, 0.001, 1.0)
> The anchor is measured, not chosen as a difficulty knob. On the frozen release, the strongest
> pre-registered no-model shortcut is an all-visible ledger using the most frequent training-only
> cell and scale at each horizon. Its full-test raw score is exactly 0.25092408163309765, so that
> measured value becomes the anchor. The sample submission implements this same syntactically
> valid baseline and therefore scores 0.001 after calibration.
> Measured Baseline Ladder
> All values below were measured on the frozen 1,000-row test set. Public and private each contain
> 500 rows from 125 complete scenes. Each entry reports label-training use followed by full raw,
> public raw, private raw, and calibrated final score in that order.
> Constant hidden ledger: no label training; 0.101092, 0.101086, 0.101098, 0.001000.
> Constant visible at center: no label training; 0.225876, 0.225798, 0.225954, 0.001000.
> All visible with train-mode cell and scale: uses aggregate training-label frequencies but no fitted predictive model; 0.250924, 0.250894, 0.250954, 0.001000.
> Route-pair modal-state lookup, which collapses to all hidden: uses aggregate training-label frequencies but no fitted predictive model; 0.101092, 0.101086, 0.101098, 0.001000.
> Identifier hash: no label training; 0.210359, 0.210241, 0.210476, 0.001000.
> Last observed box: no label training; 0.184272, 0.184274, 0.184270, 0.001000.
> Hand-written linear box projection: no label training; 0.180565, 0.180457, 0.180673, 0.001000.
> CPU HistGradientBoosting on labeled geometry and route features: uses label training; 0.401794, 0.401797, 0.401789, 0.201408.
> The route-pair lookup and constant-hidden scores are intentionally identical, not duplicated by
> mistake. The lookup was fitted on training labels by selecting the most frequent complete state
> for each (route_cd, route_de, horizon) key. On this frozen release, the selected modal state is
> hidden for every key and both horizons. Its test ledger is therefore exactly equivalent to the
> constant-hidden ledger, which independently verifies that route labels alone provide no useful
> shortcut.
> The maximum public/private raw gap across these eight registered methods is 0.000235205.
> The anchor is recalculated only when the frozen dataset changes; the dataset hash, ladder report,
> grader constant, and prepared sample are release-gated together. A model must exceed the anchor by
> learning transferable relationships from labeled training examples. A perfect submission scores
> 1.0, while a structurally invalid submission receives 0.001.
> Measured Rank-Stability Audit
> Three unique organizer CPU submissions use the same metadata-learning pipeline but train on fixed
> nested subsets containing 100%, 20%, and 5% of the training scenes. Their full final scores are
> 0.203187, 0.168686, and 0.142299. The same order holds on both public and private partitions.
> Mean absolute public/private score drift is 0.000168393, while the smallest adjacent solver gap
> is 0.026281601, giving a drift-to-gap ratio of 0.006407. A leave-one-scene-out jackknife over
> 125 independent scenes per partition gives a minimum adjacent signal-to-noise ratio of 4.4628
> standard errors. The release gate requires at least three valid unique submissions, identical rank
> order across full/public/private, drift below half the smallest adjacent gap, and every adjacent
> gap above two jackknife standard errors.
> The grader aligns rows by id. A submission is structurally invalid if it has incorrect columns; duplicate, missing, blank, or unknown IDs; malformed JSON; missing or repeated track IDs; unknown track IDs; missing D or E states; invalid visibility values; cells outside [0, 35]; invalid scale labels; or non-null cell or scale values for a hidden prediction. Invalid structures are not repaired automatically.
> Submission Format
> Write the final submission to:
> ./working/submission.csv
> Submit exactly two columns in this order:
> id,future_states te_000001,"[{""track_id"":""T00"",""d"":{""visible"":1,""cell"":17,""scale"":""M""},""e"":{""visible"":0,""cell"":null,""scale"":null}}]"
> Because future_states contains JSON quotes and commas, use a CSV library rather than constructing rows manually. In Python, serialize the list with json.dumps, store the resulting string in the future_states column, and save the dataframe with to_csv(..., index=False).
> Rows may appear in any order because the grader aligns them by id. Within each JSON list, track records may also appear in any order. Every track_id in the corresponding context_groups value must appear exactly once.
> Expected Output
> The submission must contain 1,000 data rows and two columns. Every test ID must appear exactly once. Every future_states cell must be valid JSON containing one D state and one E state for every context track.
> The grader returns one floating-point score in the inclusive range [0.001, 1.0]. Higher is better.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Ledger Entry Consistency Verification

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78gw619nd1hf39hjmhae5fz98bzf1t
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Easy
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Ledger Entry Consistency Verification
> Domain: Computer Vision
> Compute tier: CPU only. The reference environment provides 10 CPU cores and
> 64 GB RAM, with no GPU. The full run -- loading data, any training, validation,
> inference, and writing submission.csv -- must complete within 1.5 hours end
> to end.
> Overview
> A large photographic archive is paired with an old ledger of recorded entries,
> and the two records do not always agree. Every photograph shows one physical
> object together with a printed length reference visible in the same frame.
> Next to each photograph, a ledger entry records what someone claimed about
> the object at the time, as a short text string such as "14.2 mm" or
> "3.7 cm".
> Your task: given (a) one photograph and (b) its associated claim text, decide
> whether the two records agree:
> CONSISTENT -- the claim agrees with what the photograph actually shows,
> within a stated tolerance;
> OVERSTATE -- the claim is larger than what the photograph shows, outside
> tolerance;
> UNDERSTATE -- the claim is smaller than what the photograph shows,
> outside tolerance.
> This is a three-class classification problem whose answer cannot come from
> either record alone: the photograph never states what was claimed, and the
> claim text never states what the photograph actually shows. Resolving the
> disagreement means jointly interpreting both records -- deriving a real-world
> size from what is visible in the frame (every photograph has its own framing
> and distance, so no single global scale applies across the archive) and
> relating that to the value written in the claim.
> Dataset
> The dataset consists of a set of photograph files plus a manifest describing
> each one. Every photograph is a single JPEG image showing one object placed on
> a plain background next to a printed reference scale with fine millimeter
> graduations and centimeter markings; some photographs also show small paper
> labels next to the object. The reference scale's position, orientation (it may
> run along any of the four edges of the frame), and effective pixel scale all
> vary from photograph to photograph -- there is no single global scale that
> applies to every image.
> Participants receive three files:
> **train.csv** -- one row per training photograph. Columns: id (a short
> opaque string identifier, e.g. spec_00123, unique per row), image_path
> (a single relative file path string such as images/spec_00123.jpg
> pointing into the accompanying images/ folder -- this is one path per
> row, not separate width/height/format columns), claimed_value_text (a
> single free-text string such as "14.2 mm" or "3.7 cm" -- one string
> column, not separate numeric-value and unit columns), and true_verdict
> (one of the three string labels CONSISTENT, OVERSTATE, or
> UNDERSTATE).
> **test.csv** -- the same id, image_path, and claimed_value_text
> columns as train.csv, for a disjoint set of photographs, with
> true_verdict withheld.
> **sample_submission.csv** -- an example valid submission for every row of
> test.csv (a constant majority-class prediction), showing the exact
> submission format.
> **images/** -- the JPEG photographs referenced by image_path in both
> train.csv and test.csv.
> Example train.csv row (a real row from this dataset):
> id,image_path,claimed_value_text,true_verdict
> spec_01041,images/spec_01041.jpg,62 mm,OVERSTATE
> The CONSISTENT tolerance rule
> Let
> ð‘š
> true
> m
> true
> â€‹
> be the object's true linear extent in millimeters, as
> calibrated from the photograph's own reference scale, and let
> ð‘š
> claim
> m
> claim
> â€‹
> be the
> claimed value from claimed_value_text, converted to millimeters (a value
> stated in cm is multiplied by 10). Define the relative error:
> ð‘Ÿ
> =
> ð‘š
> claim
> âˆ’
> ð‘š
> true
> ð‘š
> true
> r=
> m
> true
> â€‹
> m
> claim
> â€‹
> âˆ’m
> true
> â€‹
> â€‹
> The ground-truth verdict is:
> verdict
> =
> {
> CONSISTENT
> if
> âˆ£
> ð‘Ÿ
> âˆ£
> â‰¤
> 0.07
> OVERSTATE
> if
> ð‘Ÿ
> >
> 0.07
> UNDERSTATE
> if
> ð‘Ÿ
> <
> âˆ’
> 0.07
> verdict={
> CONSISTENT
> â€‹
> ifÂ âˆ£râˆ£â‰¤0.07OVERSTATE
> â€‹
> ifÂ r>0.07UNDERSTATE
> â€‹
> ifÂ r<âˆ’0.07
> â€‹
> That is, claims within 7% of the true calibrated measurement count as
> consistent (allowing for ordinary reading/rounding precision); claims that
> overstate or understate the true size by more than 7% are labeled
> accordingly. This rule is exact and is what generated every label in this
> dataset -- there is no hidden fudge factor beyond it.
> Evaluation
> Metric: macro-averaged F1 across the three verdict classes.
> For each class
> ð‘
> âˆˆ
> CONSISTENT
> ,
> OVERSTATE
> ,
> UNDERSTATE
> câˆˆCONSISTENT,OVERSTATE,UNDERSTATE,
> with true positives
> ð‘‡
> ð‘ƒ
> ð‘
> TP
> c
> â€‹
> , false positives
> ð¹
> ð‘ƒ
> ð‘
> FP
> c
> â€‹
> , and false negatives
> ð¹
> ð‘
> ð‘
> FN
> c
> â€‹
> counted over the whole test set:
> ð¹
> 1
> ð‘
> =
> 2
> ð‘‡
> ð‘ƒ
> ð‘
> 2
> ð‘‡
> ð‘ƒ
> ð‘
> +
> ð¹
> ð‘ƒ
> ð‘
> +
> ð¹
> ð‘
> ð‘
> F1
> c
> â€‹
> =
> 2TP
> c
> â€‹
> +FP
> c
> â€‹
> +FN
> c
> â€‹
> 2TP
> c
> â€‹
> â€‹
> Score
> =
> 1
> 3
> âˆ‘
> ð‘
> ð¹
> 1
> ð‘
> Score=
> 3
> 1
> â€‹
> âˆ‘
> c
> â€‹
> F1
> c
> â€‹
> If a class does not appear in either the predictions or the answers for a
> given class
> ð‘
> c (i.e.
> ð‘‡
> ð‘ƒ
> ð‘
> =
> ð¹
> ð‘ƒ
> ð‘
> =
> ð¹
> ð‘
> ð‘
> =
> 0
> TP
> c
> â€‹
> =FP
> c
> â€‹
> =FN
> c
> â€‹
> =0), that class's
> ð¹
> 1
> ð‘
> F1
> c
> â€‹
> is
> defined as 1.0 (nothing to get wrong). The final score is floored at
> 0.0001 so that it is never reported as exactly zero.
> Score bounds: minimum 0.0001, maximum 1.0. Higher is better. A perfect
> submission (every verdict exactly correct) scores 1.0. Predicting a single
> constant class for every row scores well below 1.0 whenever the true classes
> are not all identical (see baselines below).
> ### Reference implementation
> import numpy as np
> LABELS = ("CONSISTENT", "OVERSTATE", "UNDERSTATE")
> def macro_f1(y_true, y_pred, labels=LABELS):
> f1s = []
> for c in labels:
> tp = int(np.sum((y_true == c) & (y_pred == c)))
> fp = int(np.sum((y_true != c) & (y_pred == c)))
> fn = int(np.sum((y_true == c) & (y_pred != c)))
> denom = 2 * tp + fp + fn
> f1 = (2.0 * tp / denom) if denom > 0 else 1.0
> f1s.append(f1)
> return float(np.mean(f1s))
> def score(y_true, y_pred):
> return max(1e-4, macro_f1(np.asarray(y_true), np.asarray(y_pred)))
> ## Baselines
> All numbers below were measured on this dataset's actual train/test split
> (1,650 train / 550 test rows).
> Three things are worth noting in this table. First, the majority-class
> baseline looks unusually low because macro-F1 rewards spreading predictions
> across all three classes; an uninformed classifier that simply guesses in the
> training class proportions already scores 0.346, so that (not 0.191) is the
> more meaningful "no real information" reference point. Second, the
> image-only baseline lands right at that uninformed reference (0.343 vs.
> 0.346): generic image statistics genuinely carry no usable signal about the
> claim, exactly as expected, since the model never sees what was claimed. The
> text-only baseline scores modestly above the uninformed reference (0.440),
> because some claims are numerically implausible as a measurement of the
> pictured kind of object regardless of the specific photograph -- a limited,
> realistic amount of signal.
> Third, the full-pipeline number (1.000) is a ceiling, not a target you should
> expect your own solution to land on exactly: it is what you get only if your
> own way of relating the photograph to a real-world size reproduces the same
> result, to the same precision, that this dataset's labels were computed from
> -- and the exact thresholds behind that computation are not published. A
> well-engineered independent approach (learned or classical) will have some
> amount of ordinary measurement error and should expect a strong score clearly
> above the text-only and image-only baselines, but not necessarily at 1.000.
> The large gap between the uninformed/text/image baselines and this ceiling is
> what rewards actually resolving the photograph and the claim jointly, rather
> than relying on either one alone; closing as much of that gap as possible, not
> reaching 1.000 exactly, is what this challenge is scored on.
> ## Submission Format
> Submit a `submission.csv` with exactly two columns, `id` and `prediction`,
> and exactly one row per row of `test.csv`:
> - `id` -- must exactly match a `test.csv` id (every test id must appear
> exactly once; no missing, extra, or duplicate ids).
> - `prediction` -- exactly one of the three strings `CONSISTENT`,
> `OVERSTATE`, or `UNDERSTATE` (case-sensitive; no other values, and no
> probabilities or scores).
> Example `submission.csv`:
> id,prediction
> spec_00123,OVERSTATE
> spec_00456,CONSISTENT
> spec_00789,UNDERSTATE
> Use the provided `make_submission.py` helper to build this file from a list
> of predicted labels aligned to `test.csv`'s row order.
> ## Allowed and Prohibited Approaches
> **Allowed:**
> - Any model architecture, trained on the provided `train.csv` images and
> claim text, including convolutional networks, vision transformers, or
> classical hand-engineered computer-vision techniques, used in any
> combination to relate the photograph to a real-world size. Whether that
> relation is learned end to end or built from classical vision components is
> your choice -- either is a legitimate, fully valid solution path, not a
> shortcut around the task.
> - Pretrained model weights, but only from libraries preinstalled in the
> provided environment (e.g., Hugging Face `transformers`/`hub`, `timm`, as
> available in the standard Kaggle Docker image). Downloading model weights
> from an arbitrary external URL or a non-preinstalled source is not
> permitted.
> - Standard image augmentation and preprocessing applied to the provided
> training images.
> - Any way of interpreting `claimed_value_text`, including converting it to a
> numeric value and unit.
> **Prohibited:**
> - Using any data not provided with this challenge. No external images,
> external measurement datasets, external pretrained scale/measurement-
> detection models beyond what is preinstalled, or any other outside data
> source.
> - Looking up the photographed object in any external database, archive, or
> search engine using any label, code, or barcode visible in the photograph.
> The images in this dataset were sourced from a real photographic archive;
> attempting to identify or cross-reference the original source record for
> any specific photograph is not permitted, and in any case does not provide
> the measurement value being asked for here.
> - Any use of the test set beyond running your trained model or pipeline on it
> to produce predictions. In particular: no pseudo-labeling from test
> predictions fed back into training, no reweighting or re-sampling of
> training data based on the test distribution, no transductive or
> semi-supervised use of the test set, no test-time training or adaptation
> using test images, and no statistic of any kind computed over the test set
> other than the final forward pass that produces each prediction.
> - Hard-coding, memorizing, or otherwise special-casing individual test
> `id` values or file names.
> - Manual (human) labeling of any test image.
> &nbsp;

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Historical Quilt Block State Prediction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cteycpn360vqxgmwwy1mbpx8c2sb4
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Quilt Block Cohort State Resolution
> Domain: Computer Vision
> Compute tier: CPU only. The reference environment provides 10 CPU cores
> and 64 GB RAM, with no GPU. The complete run -- loading the data, any
> training, validation, inference, and writing submission.csv -- must finish
> within 1.5 hours end to end.
> Overview
> You are given six real photographs. Each one shows a single square crop of a
> pieced, patterned section from a different historical quilt; no two
> photographs in the same group of six come from the same quilt. Your task is
> to assign each of the six photographs one of four possible states, labeled
> 0, 1, 2, or 3.
> The state assigned to any one photograph is not a property of that
> photograph considered on its own. It depends on which five other
> photographs it happens to appear together with in that particular group of
> six. The very same photograph, placed into a different group of six, can be
> assigned a different state. There is no way to determine a photograph's
> correct state by inspecting it in isolation -- the six photographs that make
> up a group have to be considered jointly.
> This is what separates the task from ordinary per-image labeling. A model
> that only ever looks at one photograph at a time, however sophisticated,
> cannot do meaningfully better than guessing. Recovering the structure that
> actually determines the outcome requires reasoning about the full set of six
> photographs together, as a single unit.
> Dataset
> The dataset consists of a folder of JPEG photographs plus three CSV files.
> images/ contains individual JPEG photographs, each 320x320 pixels. Every
> photograph is a roughly square crop taken from one real historical quilt
> photograph, capturing one region of that quilt's pieced pattern.
> train.csv has one row per group of six photographs used for training. Its
> columns are: group_id (a short opaque string identifier, unique to the
> row), block_1 through block_6 (six separate string columns; each one
> holds a single relative file path into the accompanying images/ folder,
> for example images/blk_00231.jpg -- one path per column, six photographs
> per group, always drawn from six different quilts), and state_code (one
> string column holding a six-character code; its k-th character, always one
> of the digits 0, 1, 2, or 3, is the true state of the photograph
> named in column block_k for that row).
> test.csv has the same group_id, block_1, ..., block_6 columns as
> train.csv, for a disjoint set of groups whose quilts never appear in
> train.csv, with state_code withheld.
> sample_submission.csv shows the exact format of a valid submission: one
> row per row of test.csv, with a constant (weak) six-character prediction.
> Example row from train.csv (a real row from this dataset):
> group_id	block_1	block_2	block_3	block_4	block_5	block_6	state_code
> grp_000000	images/blk_00190.jpg	images/blk_00360.jpg	images/blk_00392.jpg	images/blk_01213.jpg	images/blk_00335.jpg	images/blk_00817.jpg	030123
> In this example row, the photograph at images/blk_00190.jpg (slot 1) has
> true state 0, the photograph at images/blk_00360.jpg (slot 2) has true
> state 3, and so on through slot 6.
> Evaluation
> Metric: mean per-slot accuracy.
> Every test group contributes six individual slot predictions. The score is
> the fraction of all of these individual slot predictions, pooled across
> every test group, that exactly match the true state for that slot.
> Score
> =
> 1
> 6
> ð‘
> âˆ‘
> ð‘–
> =
> 1
> ð‘
> âˆ‘
> ð‘˜
> =
> 1
> 6
> 1
> [
> ð‘ 
> ^
> ð‘–
> ,
> ð‘˜
> =
> ð‘ 
> ð‘–
> ,
> ð‘˜
> ]
> Score=
> 6N
> 1
> â€‹
> âˆ‘
> i=1
> N
> â€‹
> âˆ‘
> k=1
> 6
> â€‹
> 1[
> s
> ^
> i,k
> â€‹
> =s
> i,k
> â€‹
> ]
> where
> ð‘
> N is the number of test groups,
> ð‘ 
> ð‘–
> ,
> ð‘˜
> âˆˆ
> {
> 0
> ,
> 1
> ,
> 2
> ,
> 3
> }
> s
> i,k
> â€‹
> âˆˆ{0,1,2,3} is the true
> state of the photograph in slot
> ð‘˜
> k of group
> ð‘–
> i, and
> ð‘ 
> ^
> ð‘–
> ,
> ð‘˜
> s
> ^
> i,k
> â€‹
> is your
> predicted state for that slot.
> def score(y_true, y_pred):
> """y_true, y_pred: lists of N six-character strings, each character
> one of '0', '1', '2', '3'."""
> correct = sum(a == b for t, p in zip(y_true, y_pred) for a, b in zip(t, p))
> total = 6 * len(y_true)
> return max(1e-4, correct / total)
> Score bounds: minimum 0.0001, maximum 1.0. Higher is better. Predicting
> every slot uniformly at random among the four states scores approximately
> 0.25 in expectation. A submission that gets every slot exactly right scores
> 1.0.
> Baselines
> All numbers below are measured on this dataset's actual released train/test
> split.
> Baseline	Description	Mean per-slot accuracy
> Uniform random	Each slot predicted uniformly at random from {0,1,2,3}	~0.25
> Constant (sample submission)	Always predicts the single most common state, for every slot of every group	0.249
> Per-photograph-only	A model given only a photograph's own extracted features, never its groupmates	0.214
> Whole-group	A model given all six photographs' extracted features jointly	0.716
> Oracle	The organizers' own exact procedure, applied directly	1.0
> Note that the per-photograph-only baseline sits at, or even slightly below,
> the trivial constant baseline. This is expected, not a mistake: a
> photograph's state genuinely does not depend on that photograph alone, so a
> model with no access to its groupmates has no real signal to find and
> performs like an uninformed guess. The gap between the per-photograph-only
> baseline and the whole-group baseline is the entire signal this challenge is
> designed to reward: both are given access to the same underlying
> information, but only the whole-group baseline is allowed to consider more
> than one photograph at a time. Closing as much of that gap as you can, not
> reaching the oracle row (which requires knowledge no participant is given),
> is what this challenge scores.
> Submission Format
> Submit a submission.csv with exactly two columns, group_id and
> prediction, and exactly one row per row of test.csv:
> group_id -- must exactly match a test.csv group_id (every test
> group_id must appear exactly once; no missing, extra, or duplicate ids).
> prediction -- a six-character string, each character one of the digits
> 0, 1, 2, 3, in the same slot order as block_1...block_6 in
> test.csv. No other characters, and no separators between digits.
> Example submission.csv (illustrating the format; grp_004800 and
> grp_004801 are real test.csv group_id values):
> group_id,prediction
> grp_004800,203110
> grp_004801,331002
> Use the provided make_submission.py helper to build a correctly formatted
> file from either a list of six-character strings or a list of six per-slot
> integer predictions, aligned to test.csv's row order.
> Allowed and Prohibited Approaches
> Allowed:
> You must build your solution on top of a genuinely small pretrained image
> backbone, drawn only from a library preinstalled in the provided
> environment (for example, Hugging Face transformers/hub or timm, as
> available in the standard Kaggle Docker image). The backbone's own
> weights must be kept completely frozen and unmodified throughout: no
> gradient updates, fine-tuning, or other change to any of its parameters,
> at any point.
> On top of that frozen backbone, you may train a small number of
> additional parameters -- for example, a lightweight head on the
> backbone's output representation, or a small learned set of extra values
> combined with the backbone's inputs or intermediate activations. This
> additional, strictly limited amount of task-specific adaptation is where
> all of your learning must happen.
> Any way of combining information across the six photographs in a group so
> that each prediction can depend on all six, not just one -- this is the
> intended skill being measured, and any architecture or method that
> achieves it is acceptable, as long as the frozen-backbone rule above is
> respected.
> Standard image preprocessing and augmentation applied to the provided
> training images.
> Prohibited:
> Updating, fine-tuning, or otherwise modifying the frozen backbone's own
> weights in any way. Submissions that touch the backbone's parameters
> (beyond using them, unmodified, in a forward pass) do not satisfy the
> challenge's constraint, regardless of the resulting score.
> Using any pretrained model weights from a source other than a library
> preinstalled in the provided environment. Downloading weights from an
> arbitrary external URL, or from any source not already part of the
> standard preinstalled environment, is not permitted.
> Using any data not provided with this challenge. No external images,
> external quilt or textile datasets or archives, external pretrained
> models trained specifically for a related task, or any other outside
> data source.
> Looking up any photograph's source or original object in any external
> database, archive, or search engine. Even if a source were identified,
> doing so provides no information about this dataset's group-dependent
> states, which are assigned entirely by the organizers.
> Any use of the test set beyond running your trained model on it to
> produce predictions. In particular: no pseudo-labeling from test
> predictions fed back into training, no reweighting or re-sampling of
> training data based on the test distribution, no transductive or
> semi-supervised use of the test set, no test-time training or adaptation
> using test images, and no statistic of any kind computed over the test
> set other than the final forward pass that produces each prediction.
> Hard-coding, memorizing, or otherwise special-casing individual test
> group_id values, file names, or image contents.
> This constraint is designed to measure how much useful group-level
> structure can be recovered without touching a general-purpose pretrained
> vision model's own weights -- using only a small amount of task-specific
> adaptation added on top of it.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Thermal History From Track Morphology

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70f3p73w6kmfagypghqe1qhn8c2wkw
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> When a crystalline mineral grain is heated, the microscopic linear damage tracks running
> through it slowly anneal â€” they shorten, narrow, and fade. How far this has progressed
> encodes the grain's thermal history, but the mapping is not one-to-one: a long treatment
> at a low temperature and a short treatment at a high temperature can leave the tracks in a
> nearly identical state (a timeâ€“temperature trade-off). Reading a grain's treatment back
> from a single field of view therefore means separating two entangled latent factors â€”
> how hot and for how long â€” from the statistical texture of the surviving tracks.
> You are given optical-microscopy images of etched damage tracks in individual mineral
> grains, each grain having received a controlled laboratory heat treatment held at one
> temperature for one duration. For the training grains you are told the treatment's
> temperature band and duration class. Your job is to recover both from the image. Tracks
> are positioned at random within each grain, so no two grains look alike even under
> identical treatment; the signal lives in the population statistics of the tracks (their
> lengths, densities, and shapes), and the timeâ€“temperature trade-off leaves the two axes
> only partially separable from morphology.
> Dataset
> Each item is a single optical-microscopy field of view showing etched damage tracks
> inside one mineral grain. Every grain contributes several non-overlapping fields of
> view, cut at native resolution and sharing no pixels; all fields of one physical grain
> carry the same group identifier, and the split keeps whole grains on one side, so no grain
> appears in both training and evaluation. The scored prediction for each image is a pair of
> calibrated distributions â€” one over the three temperature bands and one over the three
> duration classes.
> The split is additionally stratified by treatment condition, so each class's share of the
> evaluation set matches its share of the training set to within about one percentage point
> on both axes. The class shares themselves are uneven: on the training set the temperature
> bands run roughly 42% Low / 32% Mid / 26% High, and the duration classes roughly 44%
> Short / 20% Medium / 36% Long.
> Public files
> train.csv â€” labelled training images. Columns:
> id, group_id, image, temp_band, duration.
> test.csv â€” unlabelled test images (no temp_band, no duration, no group_id).
> Columns: id, image.
> images/ â€” a folder of anonymised JPEG files (cropped fields of view at native
> resolution, metadata-stripped), one per image reference in the CSVs.
> sample_submission.csv â€” a valid, correctly-formatted submission that assigns every
> image a uniform distribution on each axis. Columns: id,
> p_temp_low, p_temp_mid, p_temp_high,
> p_dur_short, p_dur_medium, p_dur_long.
> Private file (organiser only)
> answers.csv â€” held-out labels. Columns: id, group_id, temp_band, duration.
> Column descriptions
> Each row of train.csv / test.csv describes one field of view:
> id (string) â€” opaque image identifier; one submission row per id.
> group_id (string, train only) â€” opaque identifier of the physical grain an image was
> taken from. All fields of view of one grain share it; use it to build grain-disjoint
> local validation folds. It is deliberately absent from test.csv.
> image (string) â€” filename of the field-of-view image inside images/.
> temp_band (string, train only) â€” the treatment temperature band, one of Low
> (lower-temperature treatments), Mid (intermediate), High (higher-temperature).
> duration (string, train only) â€” the treatment duration class, one of Short,
> Medium, Long.
> Data example
> A single training row:
> id,group_id,image,temp_band,duration
> img_97ffe55535954a8e,grp_80533bec48ce0e73,img_97ffe55535954a8e.jpg,Low,Long
> Submission format
> Submit a CSV with exactly seven columns â€” id plus the six probability columns below â€”
> and exactly one row per test id.
> id â€” an image identifier from test.csv.
> p_temp_low, p_temp_mid, p_temp_high â€” the predicted probability that the
> treatment temperature band is each of the three values. These three must sum to 1.
> p_dur_short, p_dur_medium, p_dur_long â€” the predicted probability of each
> duration class. These three must sum to 1.
> Every id in test.csv must appear exactly once. A submission with a missing id, an unknown
> id, a duplicate id, a triple that does not sum to 1 (within a tolerance of 0.02), or a non-finite
> value is rejected. Probabilities are checked against the same 0.02 tolerance on the lower
> bound: a value in [-0.02, 0) â€” which is what writing the third class as 1 - p1 - p2
> can produce â€” is accepted and clamped to 0, while anything below -0.02 is rejected. Each
> triple is renormalised to sum to exactly 1 before scoring.
> Sample submission (uniform on both axes â€” an uninformative baseline):
> id,p_temp_low,p_temp_mid,p_temp_high,p_dur_short,p_dur_medium,p_dur_long
> img_b41ce40471ff740c,0.3333,0.3333,0.3334,0.3333,0.3333,0.3334
> img_5592361d2b16d7cd,0.3333,0.3333,0.3334,0.3333,0.3333,0.3334
> Evaluation
> The headline number is the mean normalised Brier skill across the two axes
> (temperature band and duration class), each treated as a three-class calibrated
> prediction.
> For one axis, an image's Brier score is the squared error between its predicted
> distribution and the one-hot true label:
> def brier(p, y_index):          # p: length-3 probabilities, y_index: true class 0..2
> return sum((p[c] - (1.0 if c == y_index else 0.0)) ** 2 for c in range(3))
> Each axis is normalised against the uniform baseline (predicting 1/3 for every class),
> whose expected Brier score is 2/3, and the two axis skills are averaged with equal
> weight:
> skill_axis = 1 - mean(brier over items on that axis) / (2/3)
> score      = 0.5 * skill_temperature + 0.5 * skill_duration
> Range: 0.0â€“1.0. Higher is better.
> Baseline: a uniform (or otherwise uninformative) submission scores about 0.0; a
> perfect, fully-confident submission scores 1.0.
> Class frequencies carry no credit. Every image is scored against its own one-hot
> label, so a submission that repeats one fixed distribution on every row scores at most
> about 0.03 â€” regardless of which distribution it repeats, including the class
> frequencies of the training set, and including the exact class frequencies of the
> evaluation set. Because the two sets' class shares agree to within about one percentage
> point (see Dataset), those two constants score within 0.01 of each other: the class
> balance is not a quantity that separates submissions under this metric.
> Score floor: a valid submission is clamped to a minimum of 0.02, so a well-formed
> submission never returns exactly 0.0.
> Grade direction: Maximize. Reported bounds: min 0.0, max 1.0.
> What Not To Use (Prohibited Methods)
> This task must be solved by learning to read the treatment from the track morphology in the
> provided micrographs. The following are prohibited:
> No external label sources. Do not use any outside collection of annealing
> measurements, track-length tables, or pre-computed treatment labels to label the test
> images. Predictions must come from your own model reading the pixels.
> No matching images back to an external source. Do not attempt to identify the source
> micrographs, mineral sample, or experimental run and pull their treatment records; do not
> match image content, ids, or filenames against any external repository, image search, or
> reverse-image service to recover the labels.
> No id-, group-, or field-based hardcoding. id and group_id are opaque tokens; do
> not make the submission a function of ids, row order, or filename structure instead of the
> track morphology.
> No manual labelling of the test set. Do not hand-estimate which test grains received
> which treatment.
> No private-label tuning. Do not tune, select, or calibrate your model against the
> held-out test labels in any way; the test treatments are not available to solvers.
> No leakage through the group field. group_id appears only in train.csv, to build
> grain-disjoint validation folds; do not use it to infer or align test grains.
> No content-free shortcuts. Ordering or scoring images by how often a grain recurs, by
> image size, or by capture order is out of scope â€” the data is built so these carry no
> signal.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Atari Gameplay Attention Set Matching

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75jvpe0pkbyke9cykrrkpdv18c360q
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Atari Gameplay Attention Set Matching
> Overview
> Develop a CPU-only computer-vision system that restores the correct correspondence between shuffled gameplay footage and visual-attention telemetry from game playtests.
> The recording pipeline preserved short gameplay micro-episodes together with their corresponding attention routes, but a synchronization failure independently shuffled the two streams within small batches. Each example contains:
> four gameplay micro-episodes, each shown as four temporally ordered frames;
> four attention-route strips, each containing the route observed over the same four matching time steps;
> a one-to-one but unknown correspondence between the four scene strips and the four route strips.
> Your model must assign compatibility scores to all 16 possible sceneâ€“route pairs. The evaluator then converts those scores into a maximum-weight one-to-one assignment. The task is therefore structured cross-modal matching, rather than image classification, object detection, gaze-coordinate regression or future-frame forecasting.
> The task models a practical quality-control problem in instrumented game research and usability testing. Timestamp loss, buffered writes, dropped packets, and parallel-export failures can leave small batches internally complete but incorrectly paired. Recovering the correspondence allows analysts to retain otherwise usable sessions even when the original synchronization metadata is no longer available.
> The public examples originate from human-operated gameplay sessions in which gaze positions were recorded synchronously with gameplay frames under a semi-frame-by-frame acquisition protocol. That source collection protocol preserves genuine human visual-attention behavior, but this challenge defines a different learning problem from gaze prediction or action imitation: the original sceneâ€“attention alignment is used only to construct authentic paired micro-episodes, after which correspondence is deliberately removed within each four-item batch.
> The resulting task is a set-level synchronization-repair problem. Each row forms a complete 4Ã—4 bipartite matching instance, and a solver must estimate all 16 cross-modal compatibility scores before a one-to-one assignment is decoded. This formulation requires joint reasoning over scene content, short-term visual change, attention geometry, and the global permutation constraint rather than predicting a gaze map, gaze coordinate, action, or class label independently for each frame.
> Entire recording sessions are held out for testing. The release contains eight opaque visual families, all represented in both splits, with 48 training sessions and 32 held-out test sessions in total. This split evaluates transfer to unseen play sessions rather than requiring predictions for unseen labels. Within each row, candidates are constructed so that simple global route summaries are insufficient; effective solutions must relate route geometry to visual content and temporal change in the scene strips. Candidate sets are also filtered to exclude near-duplicate scene alternatives whose attention correspondence would be intrinsically ambiguous.
> The complete solution must run on CPU and finish within 1.5 hours, including training, validation, inference, and submission generation. The memory limit is 62 GB.
> Dataset
> dataset/public/
> â”œâ”€â”€ train.csv
> â”œâ”€â”€ test.csv
> â”œâ”€â”€ sample_submission.csv
> â””â”€â”€ images/
> â”œâ”€â”€ scenes/
> â””â”€â”€ traces/
> The prepared release contains exactly 1,296 training rows and 480 test rows spanning eight visual families. The training split contains 48 recording sessions (6 per family), while the test split contains 32 disjoint recording sessions (4 per family). This larger set of held-out sessions improves the stability of leaderboard comparisons while preserving the stated total row counts.
> Visual layout
> Each scene_file is a 678Ã—264 RGB JPEG with four fixed slots:
> S0  S1
> S2  S3
> Each scene slot contains four gameplay frames arranged chronologically from left to right. The frames are temporally adjacent and together form a single micro-episode; they are not provided as a video, and the task does not require future-frame prediction. Each gameplay frame is rendered at 80Ã—105 pixels.
> Each trace_file is a 678Ã—264 RGB PNG with four fixed slots:
> T0  T1
> T2  T3
> Each trace slot contains four coordinate panels arranged chronologically from left to right. Points and short segments represent the within-step attention route, while increasing marker size indicates temporal progression within a panel. The neutral trace background contains no gameplay pixels. Each gaze panel is rendered on the same 80Ã—105 canvas as its corresponding gameplay panel.
> The scene and trace boards are shuffled independently. Their slot labels define the indices used by the target mapping and submission columns.
> train.csv
> id,session_id,domain_id,scene_file,trace_file,target_mapping
> Columns:
> id: opaque row identifier, unique within train.csv;
> session_id: opaque recording-session group for grouped validation;
> domain_id: opaque visual-family identifier shared across sessions;
> scene_file: path relative to dataset/public/ for the four-scene board;
> trace_file: path relative to dataset/public/ for the four-route board;
> target_mapping: compact JSON array of four integers.
> For a target such as:
> [2,0,3,1]
> scene slot S0 matches trace slot T2, S1 matches T0, S2 matches T3, and S3 matches T1. Every target is a permutation of [0,1,2,3].
> test.csv
> id,session_id,domain_id,scene_file,trace_file
> The columns have the same meaning as in train.csv, except that target_mapping is withheld. Training and test session_id sets are disjoint, while the same domain_id values appear in both splits, ensuring that test rows remain learnable from the public training data.
> Every test id must appear exactly once in the submission. IDs, file names, CSV row order, and opaque group codes do not encode the sceneâ€“trace correspondence.
> sample_submission.csv
> id,s0_t0,s0_t1,s0_t2,s0_t3,s1_t0,...,s3_t3
> The sample assigns 0.0 to all 16 compatibility scores. It is a valid serialization example; however, because all pair scores are tied, the ranking component remains at chance and the resulting final score is exactly 0.0.
> Submission format
> Write predictions to:
> working/submission.csv
> CSV example:
> id,s0_t0,s0_t1,s0_t2,s0_t3,s1_t0,s1_t1,s1_t2,s1_t3,s2_t0,s2_t1,s2_t2,s2_t3,s3_t0,s3_t1,s3_t2,s3_t3
> focus_35fd85389232c10b63d530b4,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
> focus_88c33e0a91f6cf61fb5ba902,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
> In the actual CSV, these columns appear on a single header row. Column sI_tJ represents the compatibility score between scene slot SI and trace slot TJ.
> Requirements:
> all 16 scores must be finite real numbers in [-1,000,000, 1,000,000];
> scores may be negative and do not need to be probabilities;
> rows may appear in any order;
> no extra columns or duplicate IDs are permitted.
> For each row, the evaluator selects the permutation p maximizing:
> s0_t[p[0]] + s1_t[p[1]] + s2_t[p[2]] + s3_t[p[3]]
> Ties are resolved deterministically according to lexicographic permutation order. Submit informative relative compatibility scores rather than only an implicitly decoded mapping, because the evaluator also measures pairwise ranking quality.
> Evaluation
> The score is designed specifically for the rebinding formulation rather than inherited from a gaze-prediction or action-prediction benchmark. It evaluates three complementary aspects of performance: correctness of individual sceneâ€“trace matches, recovery of the complete four-way assignment, and quality of the submitted pairwise compatibility ranking before assignment.
> For one row, let p be the maximum-weight predicted assignment and let y be the true mapping.
> pair_accuracy = number of scene slots with p[i] = y[i], divided by 4
> quartet_exact = 1 when p = y, otherwise 0
> The third component evaluates the submitted compatibility matrix before assignment. For each true pair (i, y[i]), its score is compared against:
> the three false pairs in scene row i;
> the three false pairs in trace column y[i].
> Each comparison contributes 1 for a win, 0.5 for a tie, and 0 for a loss. The mean across the resulting 24 comparisons is:
> bidirectional_rank_auc
> Each component is first averaged within session_id. The evaluator then computes the unweighted mean across test sessions, making the held-out recording sessionâ€”rather than the individual rowâ€”the unit of generalization.
> The chance levels are:
> pair_accuracy chance          = 1/4
> quartet_exact chance          = 1/24
> bidirectional_rank_auc chance = 1/2
> These values refer to an uninformed prediction baseline. In particular, quartet_exact = 1/24 corresponds to choosing uniformly among the 24 possible one-to-one assignments of four scene slots to four trace slots. Candidate-set filtering determines which micro-episodes appear together but is independent of the sceneâ€“trace permutation, so it does not alter this assignment baseline.
> Chance-adjusted gains are:
> pair_gain = clip((pair_accuracy - 1/4) / (3/4), 0, 1)
> quartet_gain = clip((quartet_exact - 1/24) / (23/24), 0, 1)
> rank_gain = clip((bidirectional_rank_auc - 1/2) / (1/2), 0, 1)
> The final score is:
> 100 Ã— (pair_gain Ã— quartet_gain Ã— rank_gain)^(1/3)
> The geometric mean prevents a system from achieving a strong score through only one aspect of performance: local pair ranking, globally consistent assignment, and complete batch recovery must all be strong.
> Not allowed
> External APIs.
> External gameplay-attention pairs, gaze annotations, or task-specific labeled data.
> Manual matching or annotation of test examples.
> Hard-coding predictions by test ID, file name, row order, or group code.
> Recovering source-recording identities or using external copies of the underlying sessions.
> Exploiting serialization artifacts, image-encoding quirks, preparation implementation details, or evaluator behavior instead of modeling sceneâ€“route compatibility.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Chromatic Galaxy Structure Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dx5pytsjh9t4p70ds7n5pnd8c0bxj
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Easy
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Chromatic Galaxy Structure Recovery
> Overview
> A galaxy does not look the same at every wavelength. Blue light traces young stars, which often sit in an extended disc, while red light traces old stars, which pile up in a compact central bulge. So the SAME galaxy is usually a little larger, less concentrated, and even a different projected shape in a blue band than in a red band, and how strongly its appearance shifts between bands is a real, measurable property tied to the galaxy's internal make-up. Recovering that wavelength dependence is a different problem from reading a single catalogue number off one band.
> Every galaxy here is a real Hyper-Suprime-Cam cutout imaged in five bands. For each one you recover five numbers from the five-band 64 by 64 pixel image: its spectroscopic redshift, and four gradients that describe how its structure changes from blue light to red light. Redshift fixes the distance and colour axis, and the four gradients describe the internal structure, so the five targets probe genuinely different aspects of the galaxy and you have to recover all five.
> Because the gradients are small differences read across faint, real survey imagery with noise and neighbouring sources, a hand-crafted-feature measurement only goes so far. The shape gradients in particular are limited by how precisely a per-band shape can be measured, so they stay hard, and being good at redshift or size tells you little about them.
> Task
> For each test galaxy you output five numbers:
> redshift â€” your estimate of the galaxy's spectroscopic redshift, a distance and colour property read from how the light is distributed across the five bands.
> size_grad â€” the chromatic size gradient, defined as log base 10 of the half-light radius in the g band minus log base 10 of the half-light radius in the y band. A positive value means the galaxy is more extended in blue light than in red light.
> conc_grad â€” the chromatic concentration gradient, defined as the Sersic index in the g band minus the Sersic index in the y band. A negative value means the light profile is more sharply concentrated in red light than in blue light.
> ell_grad â€” the chromatic shape gradient over the broad band pair, defined as the ellipticity in the g band minus the ellipticity in the y band. It captures how much the galaxy's projected elongation changes across the full blue-to-red range.
> ell_grad_rz â€” the chromatic shape gradient over the inner band pair, defined as the ellipticity in the r band minus the ellipticity in the z band. It captures how the projected elongation changes over a narrower, redder pair of bands, which carries different information from the broad shape gradient.
> You are given a large set of training galaxies, each labelled with all five true values, so you can train on them.
> Required approach. Train a model on the provided images, for example a single multi-task convolutional network with a shared body and five output heads, or several specialised models. Only the ranking of your estimates is scored, so you are learning to order galaxies by each target. A learned representation of the multi-band image is what recovers the chromatic gradients; a single-band summary measurement falls short, and the shape gradients demand that the model read subtle per-band structure.
> Evaluation
> Submissions are scored with ChromaScore, higher is better, in the range 0 to 1. It is the average of five rank-agreement sub-scores, each in 0 to 1:
> Redshift agreement. The rank agreement between your redshift estimates and the true redshifts over the test galaxies, measured by Kendall's tau and clipped to the range 0 to 1, where 1 is perfect ordering and 0 is random.
> Size-gradient agreement. The same rank agreement for your size_grad estimates against the true chromatic size gradients.
> Concentration-gradient agreement. The same rank agreement for your conc_grad estimates against the true chromatic concentration gradients.
> Broad shape-gradient agreement. The same rank agreement for your ell_grad estimates against the true broad shape gradients.
> Inner shape-gradient agreement. The same rank agreement for your ell_grad_rz estimates against the true inner shape gradients.
> ChromaScore = the mean of the five agreements.
> Only the ordering of your estimates within each target matters, so any monotonic units are fine. This is a ranking score, not a regression error.
> Dataset
> The prepared public dataset:
> train_X.npy â€” training images, a float16 array of shape Ntrain by 5 by 64 by 64: five-band 64 by 64 pixel galaxy cutouts in band order g, r, i, z, y.
> train_redshift.npy â€” a float32 array of length Ntrain: the true spectroscopic redshift of each training galaxy.
> train_size_grad.npy â€” a float32 array of length Ntrain: the true chromatic size gradient.
> train_conc_grad.npy â€” a float32 array of length Ntrain: the true chromatic concentration gradient.
> train_ell_grad.npy â€” a float32 array of length Ntrain: the true broad shape gradient.
> train_ell_grad_rz.npy â€” a float32 array of length Ntrain: the true inner shape gradient.
> test_X.npy â€” test images, a float16 array of shape Ntest by 5 by 64 by 64. The id of the galaxy in row i, counting rows from 0, is the letter g followed by i written as a zero-padded 5-digit integer, so row 0 is g00000, row 1 is g00001, and so on.
> sample_submission.csv â€” a valid submission in the required format.
> Pixel values are calibrated fluxes and can be negative in the background, so a stretch such as arcsinh followed by per-image normalisation is a natural preprocessing step. The gradients are subtle, so preserving the multi-band information rather than collapsing the bands is what lets a model read them.
> Submission
> Submit a CSV with exactly these columns: id, redshift, size_grad, conc_grad, ell_grad, ell_grad_rz.
> Every test id must appear exactly once, and every value must be finite. Example:
> id,redshift,size_grad,conc_grad,ell_grad,ell_grad_rz
> g00000,0.42,0.05,-0.31,0.02,-0.01
> g00001,0.91,-0.02,0.14,-0.09,0.03
> g00002,0.18,0.11,-0.68,0.07,0.00
> Write the final submission to ./working/submission.csv, UTF-8.
> Allowed And Prohibited
> Allowed:
> Train any model on the provided images: convolutional networks, multi-task shared bodies with separate heads, separate specialised models per target, transformers, or metric-learning heads.
> Any preprocessing of the images such as arcsinh or log stretching, per-band normalisation, cropping, or augmentation such as flips and rotations, plus ensembling.
> Standard open-source deep-learning libraries such as PyTorch.
> Prohibited:
> Do not use external datasets or any information beyond the provided files.
> Do not train on, adapt to, or fit statistics from the test images, whose targets are withheld.
> Do not hardcode outputs or use per-id answer tables.
> Do not use external LLM APIs or any model-generated labels in your submission.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Real-Video Edit Region Localization

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71sbkmf2nffatetpa57sqnt98c1bqx
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Real-Video Edit Region Localization
> Overview
> Content moderators and video-forensics systems often need to identify where a frame was altered before deciding whether to escalate it for review. This challenge asks for a binary pixel mask of the regions changed by a professional editor in a real video frame. The task is intentionally different from ordinary real/fake classification: a useful system must localize small edits and transfer to editing styles it has not seen.
> The source is ANAKIN, a real-video corpus containing professionally edited clips, their original source material, and pre-existing per-frame edit masks. This challenge uses only the edited frames and the supplied masks. It does not generate frames, edits, masks, or labels. Public images preserve the supplied real JPEG frame pixels so small edit boundaries remain learnable. The released subset covers inpainting, splicing, and swap edits. All six source editor groups are separated: four groups are available for training and two disjoint groups form the hidden test.
> Dataset
> File descriptions
> train.csv: 288 labeled development examples. Each row points to one RGB JPEG frame and its matching binary PNG mask.
> test.csv: 144 unlabeled frames from editor groups absent from training. Each row points to one RGB JPEG frame.
> sample_submission.csv: valid non-empty example masks in the required format.
> images/: RGB JPEG frames referenced by both CSV files. Dimensions vary by source aspect ratio; the width is at most 512 pixels, and the height is the corresponding aspect-ratio-preserving size.
> masks/: grayscale L) binary PNG training masks referenced only by train.csv. Pixel value 0 is background and 255 is an edited-region pixel. Each mask has exactly the same width and height as its image.
> Column descriptions
> sample_id (string): stable opaque identifier for one frame, represented as 16 lowercase hexadecimal characters; it has no semantic meaning.
> image_path (string): POSIX path to the RGB JPEG relative to the public dataset directory, such as images/<sample_id>.jpg.
> mask_path (string, train.csv only): POSIX path to the matching binary PNG mask relative to the public dataset directory, such as masks/<sample_id>.png.
> Evaluation
> Each submitted mask_rle is decoded into the exact width and height of its corresponding hidden image. The supplied masks remain pixel-level real annotations, but this easier task evaluates the compact region proposal implied by each mask. Let T be the binary ground-truth mask and P be the binary predicted mask. A frame score is:
> frame_score = 0.75  *box_iou(T, P) + 0.25*  center_score(T, P)
> box_iou first takes the smallest axis-aligned box containing all foreground pixels. Boxes use (x_min, y_min, x_max, y_max) with exclusive maximum coordinates. Its value is intersection-over-union of the two boxes. center_score compares the box centers using normalized Euclidean distance:
> distance = euclidean_distance(truth_center, prediction_center) / image_diagonal
> center_score = max(0.0, 1.0 - 2.0 * distance)
> If both masks are empty, both component scores are 1.0. If exactly one mask is empty, both are 0.0. This rewards a useful compact region proposal without requiring a solver to reproduce every edited pixel boundary exactly.
> There are two hidden test editor groups and three manipulation families: inpainting, splicing, and swap. Every hidden frame belongs to exactly one cross-product bucket (held_out_editor_group, manipulation_type), giving 2 Ã— 3 = 6 buckets with 24 frames each. The editor-group labels are hidden metadata and are not columns in test.csv. The final score is the mean frame score within each bucket, followed by an equal-weight macro-average across all six buckets:
> score = mean(
> mean(frame_score for frame in bucket)
> for bucket in [
> (editor_group, manipulation_type)
> for editor_group in held_out_editor_groups  # exactly 2 hidden groups
> for manipulation_type in ("inpainting", "splicing", "swap")
> ]
> )
> The score is bounded in [0, 1]; higher is better. Macro-averaging keeps a long clip, a prolific editor, or an easy manipulation family from dominating the result.
> Submission
> Submit one CSV with exactly these columns:
> sample_id: every ID in test.csv, exactly once.
> mask_rle: a space-separated sequence of one-indexed start length pairs in row-major order. Use 0 0 for an empty mask.
> Example:
> sample_id,mask_rle
> 528ae4886c7f2b92,10234 18 11890 7
> 94034559e2e00bf6,0 0
> Requirements
> Match the column names and order exactly.
> Include every test ID once; row order may differ.
> Keep all runs inside the image dimensions and use non-negative lengths.
> Do not include an index column or additional columns.
> Prohibited methods
> Do not reverse-match test frames to an external source or manually label test masks.
> Do not create synthetic frames, synthetic edits, or synthetic masks.
> Do not use sample_id, file order, editor identifiers, or manipulation labels as a shortcut.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Steel Surface Focus Trace Synthesis

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74dd3sv0k20w5w29q10b9fzd8c36jk
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> An industrial vision controller receives a steel-surface frame and must emit a short trace of spatial focus operations. Each operation points to one of twelve public rectangles in the frame and has an execution weight of one, two, or three. The controller may be interrupted after weight 3 or continue until weight 6, so the trace must be useful at both horizons.
> Your goal is to reconstruct this anytime focus trace from the image. Executed operations should recover every visible flaw precisely, avoid repeatedly examining the same pixels, and retain useful evidence if any one operation is deleted by a downstream processing fault.
> The inputs are 200-by-200 RGB JPEGs with grayscale-like steel textures. Surface phenomena include crazing, inclusions, patches, pitted areas, rolled-in scale, and scratches. A frame may contain several spatially separated flaws. Predicting a defect category is insufficient because the required output describes where the controller should focus and in what execution order.
> Task
> For every test row, submit an ordered JSON trace containing zero to four candidate_id handles.
> A valid trace must:
> use only handles from that row;
> contain no repeated handle;
> contain at most four handles; and
> have total cost no greater than 6.
> The order is part of the prediction. At execution horizon 3 or 6, the evaluator scans from left to right. It stops immediately before the first operation that would make cumulative cost exceed the horizon. It does not skip that operation to execute a later one.
> Dataset
> The public package contains 1,440 training rows and 360 test rows.
> Public Files
> Path	Description
> train.csv	Training frames, operation handles, and exact target traces.
> test.csv	Test frames and operation handles without target traces.
> sample_submission.csv	Deterministic pseudo-random valid traces demonstrating the output format.
> images/*.jpg	The 200-by-200 RGB frames referenced by the CSV files.
> train.csv Columns
> Column	Type	Description
> id	string	Unique frame identifier.
> image_path	string	Image path relative to the public directory.
> candidates_json	JSON list	Twelve row-local focus operations.
> budgets_json	JSON list of integers	Execution horizons, always [3,6].
> max_selected	integer	Maximum trace length, always 4.
> reference_selection_json	JSON list of strings	Exact highest-utility training trace.
> test.csv Columns
> Column	Type	Description
> id	string	Unique frame identifier.
> image_path	string	Image path relative to the public directory.
> candidates_json	JSON list	Twelve row-local focus operations.
> budgets_json	JSON list of integers	Execution horizons, always [3,6].
> max_selected	integer	Maximum trace length, always 4.
> Focus Operation Schema
> Every object in candidates_json contains:
> Field	Type	Description
> candidate_id	string	Row-local operation handle used in the submitted trace.
> x1	integer	Inclusive left coordinate.
> y1	integer	Inclusive top coordinate.
> x2	integer	Exclusive right coordinate.
> y2	integer	Exclusive bottom coordinate.
> cost	integer	Execution weight: 1, 2, or 3.
> Rectangles use [x1,x2) x [y1,y2) and satisfy 0 <= x1 < x2 <= 200 and 0 <= y1 < y2 <= 200. Handles are local to one row.
> Example:
> {"candidate_id":"W1_603097","x1":22,"y1":57,"x2":116,"y2":183,"cost":3}
> Submission Format
> Submit exactly two columns:
> Column	Type	Description
> id	string	Test identifier. Every test ID must appear exactly once.
> selection_json	JSON list of strings	Ordered focus-operation handles.
> Example:
> id,selection_json
> inspect_ab38eefb00856fc27543,"[""W7_22cdf8"",""W1_603097"",""W10_067a23"",""W9_ce50f2""]"
> inspect_aa69a2a3f5b98a119fe6,"[""W11_2dfdd5"",""W7_4e00fe"",""W4_3cd858"",""W10_2f8b61""]"
> Use [] for an empty trace. Wrong or reordered columns, missing or additional IDs, duplicate IDs, malformed JSON, unknown handles, repeated handles, more than four operations, or total cost above 6 invalidate the complete submission and produce score 0.
> Evaluation
> Each frame has one or more private flaw rectangles. For private rectangle t and executed focus rectangle w, define:
> hit(t,w) = intersection_area(t,w) / area(t)
> precision(t,w) = min(1, area(t) / area(w))
> f(t,w) = hit(t,w) * precision(t,w)
> For a non-empty executed set S, the flaw-capture value is:
> H(S) = mean_t max_(w in S) f(t,w)
> Let J(S) be the mean pairwise intersection-over-union among rectangles in S, with J(S)=0 when fewer than two operations execute. Define trace evidence:
> E(S) = H(S) * (1 - 0.25 * J(S))
> Set E(empty)=0.
> To simulate deletion of one trace instruction, define Z(S)=0 when fewer than two operations execute. Otherwise:
> Z(S) = min_(w in S) E(S without w)
> The value of an executed trace prefix is:
> A(S) = 0.75 * E(S) + 0.25 * Z(S)
> For horizon h in {3,6}, let S_h be the prefix produced by the execution rule in the Task section. The raw value for row i is:
> raw_i = (A(S_3) + A(S_6)) / 2
> The evaluator exhaustively computes best_i, the largest raw value attainable by any valid trace for that row, and defines:
> ratio_i = min(1, raw_i / best_i)
> R_i = ratio_i^6
> The final score includes the overall mean and the weakest eligible private groups:
> Score = 0.85 * mean_i(R_i) + 0.075 * min_defect_group mean(R_i) + 0.075 * min_count_group mean(R_i)
> The defect groups are the six surface phenomena listed in the Overview. Count groups are single, two, and three_plus. A group participates in a minimum term only when it contains at least five test rows.
> Scores lie in [0,1]; higher is better. The exact private optimum scores 1.
> Expected Approach
> Useful CPU systems may combine texture analysis, anomaly localization, rectangle-level descriptors, trace-value prediction, horizon-aware decoding, and constrained search. Training traces supervise both spatial focus and instruction order.
> What Not To Use
> Do not use GPU acceleration.
> Do not use internet access, external datasets, or hosted inference services.
> Do not recover test answers through corpus lookup, metadata matching, manual test labeling, or hardcoded test mappings.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## NanoVeil: SEM Faint-Feature Detectability Segmentation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dbxw2ky25gbxtqh6z6q6z258a3m45
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> NanoVeil: Faint-Feature Detectability Segmentation Across Unseen SEM Textures
> Overview
> Automated feature detectors on scanning-electron-microscope (SEM) images do not find every faint feature: whether a small low-contrast feature is recovered depends on the texture around it â€” smooth background reveals it, busy nanostructure hides it or spoofs it with competing peaks. This challenge targets one question that a plain "segment the object" task sidesteps: can you read an SEM texture and predict where it lets a faint feature survive â€” on specimen types you have never seen?
> You output, for each 384Ã—384 SEM tile, a binary mask over a 16Ã—16 grid of cells: 1 where a faint feature injected at that location is recovered by a matched-filter detector, 0 where it is lost to the surrounding texture. You are judged on how well that mask tracks the true detectability field â€” not on finding any real object in the image.
> Two properties set this apart from ordinary microscopy segmentation:
> It is scored entirely on withheld specimen categories. Every scored test tile comes from a nanoscience category â€” a specimen type with its own characteristic texture â€” that appears nowhere in training. A model that memorises one category's look does not transfer; what is measured is detectability-reading that generalises across a texture domain shift, not accuracy on a familiar specimen.
> The target is only partly determined by the image. Recovery at each location is driven by the visible local structure â€” roughness, edge density, clutter â€” plus an irreducible random component (sub-pixel placement, detector noise) that no model can resolve. A strong model recovers the spatial pattern well above a constant guess, but a substantial ceiling remains, so the score is capped well below 1.
> So the task is neither "find the features" nor "denoise the image" â€” it is: predict the map of where a faint feature is recoverable in an SEM texture you were not trained on.
> Dataset
> Everything lives under ./dataset/public/. All tiles are 384Ã—384 grayscale. There are 600 training and 300 test tiles, drawn from six nanoscience categories (150 tiles each); the two test categories are held out from training.
> Column descriptions
> id (int) â€” opaque example id; the tile is images/<id>.png.
> category (string, train only) â€” nanoscience specimen type (e.g. Fibres, Powder, Biological). Several appear in training; the scored test tiles come from categories that do not.
> mask_rle (string, train only) â€” the recovery mask, run-length encoded over the 384Ã—384 tile (1 = a faint feature is recovered at that location, 0 = lost). The mask is piecewise-constant over the 16Ã—16 cell grid the detectability was probed on, so it varies at the 24-px cell scale.
> Task
> For every id in test.csv, predict a 384Ã—384 binary recovery mask and write it to ./working/submission.csv as a run-length encoding (see Submission format). The masks are freshly generated for this challenge and are published nowhere, and the SEM images carry no dense annotation â€” so do not attempt to recover the source images from any external microscopy corpus or to use the id order as a signal; predict each mask with your own model or algorithm.
> Evaluation
> The score (higher is better, in [0, 1]) is the mean over test tiles of each tile's macro-Dice â€” the average of the Dice overlap for the two classes:
> Dice_c = 2 Â· |predicted_c âˆ© true_c| / (|predicted_c| + |true_c|)      # = 1 if both are empty
> tile   = 0.5 Â· (Dice_recovered + Dice_missed)
> score  = mean(tile) over all test tiles
> Macro-averaging the two classes means a constant mask (all-recovered or all-missed) scores low (~0.33): only a mask that tracks where the texture genuinely recovers a faint feature does well. The maximum is capped well below 1 by the irreducible per-cell recovery randomness and by the fact that the test categories are unseen.
> Submission format
> Write ./working/submission.csv with exactly these two columns, in this order:
> id,mask_rle
> one row per test id (no missing, extra, or duplicate ids);
> mask_rle is the run-length encoding of the recovered (1) pixels of the 384Ã—384 mask, enumerated in row-major order, 1-indexed, as space-separated start length pairs. An empty mask is the empty string.
> Example:
> id,mask_rle
> 12,12289 24 12673 24 13057 24
> 37,
> (12289 24 = 24 recovered pixels starting at position 12289, row-major.) The grader is strict and rejects (raises) any submission whose columns are not exactly id,mask_rle in that order, whose id set is wrong/missing/duplicated, or whose mask_rle does not decode to a valid 384Ã—384 mask.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Live-Cell Division Geometry Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a2ftfen713aqgpvpxeefkad8c53e0
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Each row shows a two-panel microscopy crop around one annotated cell-division event. The left panel is the mother-cell frame before division. The right panel is the following daughter-cell frame. Predict the structured record that describes where the mother appears, where the two daughter cells appear, how the daughter pair is arranged, and how the local daughter-cell signal intensity is binned.
> The images come from fluorescent live-cell microscopy. Cells are crowded, daughter cells can be close together, and the same event may look different across channels and local crop positions. A useful solution must learn visual event geometry from the training rows and apply it to held-out videos.
> Do not use GPU acceleration.
> Dataset
> The public files are:
> train.csv: training rows with images and target records.
> test.csv: test rows with images and row-specific schema context.
> sample_submission.csv: valid submission skeleton with low-information placeholder records.
> images/: PNG two-panel microscopy crops referenced by image_path.
> Columns in train.csv:
> id (string): anonymized row id.
> image_path (string): relative path to the PNG crop.
> event_packet_json (JSON string): row-specific context and allowed values.
> answer_json (JSON string): target division-geometry record.
> Columns in test.csv:
> id (string): anonymized row id.
> image_path (string): relative path to the PNG crop.
> event_packet_json (JSON string): row-specific context and allowed values.
> event_packet_json contains:
> image_path (string): relative path to the row image.
> panel_order (array of strings): always ["mother_time","daughter_time"].
> panel_size_px (array of two integers): panel height and width in pixels.
> grid (object): grid dimensions and cell naming convention.
> time_gap_frames (integer): frame gap between the two panels.
> allowed_values (object): allowed values for area, axis, separation, and displacement bins.
> Target JSON
> Submit answer_json as a JSON object with exactly these fields:
> mother_cell (string): 8 by 8 grid cell containing the mother-cell center in the left panel.
> daughter_cells (array of two strings): grid cells containing the two daughter-cell centers in the right panel. Keep duplicates if both centers fall in the same cell.
> daughter_signal_bin_counts (object): integer counts for dim, low, bright, and hot; values must sum to 2.
> split_axis_bin (string): one of compact, horizontal, vertical, diag_down, or diag_up.
> daughter_separation_bin (string): one of contact, narrow, medium, or wide.
> lineage_motion_cards (array of two objects): one card per daughter cell. Each card has daughter_cell, dx_bin, dy_bin, and signal_bin.
> Allowed dx_bin and dy_bin values are neg2, neg1, zero, pos1, and pos2. The displacement bins describe the daughter center relative to the mother center after the crop transform.
> Submission
> Submit a CSV with exactly:
> id (string)
> answer_json (JSON string)
> Example:
> id,answer_json
> lineage_example_01,"{""mother_cell"":""r03_c03"",""daughter_cells"":[""r03_c04"",""r04_c04""],""daughter_signal_bin_counts"":{""dim"":0,""low"":1,""bright"":1,""hot"":0},""split_axis_bin"":""vertical"",""daughter_separation_bin"":""narrow"",""lineage_motion_cards"":[{""daughter_cell"":""r03_c04"",""dx_bin"":""pos1"",""dy_bin"":""zero"",""signal_bin"":""low""},{""daughter_cell"":""r04_c04"",""dx_bin"":""pos1"",""dy_bin"":""pos1"",""signal_bin"":""bright""}]}"
> Evaluation
> The final score is the mean row score. Higher is better; scores range from 0 to 1.
> For each row:
> row_score = 0.23 * mother_score + 0.25 * daughter_cell_score + 0.07 * signal_count_score + 0.06 * axis_score + 0.06 * separation_score + 0.33 * motion_card_score
> Definitions:
> mother_score: 1 if mother_cell matches exactly, otherwise 0.
> daughter_cell_score: duplicate-aware F1 over the two predicted daughter cells and two true daughter cells.
> signal_count_score: mean over the four signal bins of max(0, 1 - abs(pred_count - true_count) / 2).
> axis_score: 1 if split_axis_bin matches exactly, otherwise 0.
> separation_score: 1 if daughter_separation_bin matches exactly, otherwise 0.
> motion_card_score: duplicate-aware F1 over complete motion-card tuples (daughter_cell, dx_bin, dy_bin, signal_bin).
> Duplicate-aware F1 counts duplicate entries with multiset matching. Precision is matched predicted entries divided by total predicted entries. Recall is matched predicted entries divided by total true entries. The F1 is 2 * precision * recall / (precision + recall), with score 0 when there are no matches.
> Malformed JSON, wrong fields, invalid cells, invalid bin values, or wrong list lengths receive 0 for that row. Wrong columns, duplicate ids, missing ids, extra ids, or wrong row count are file-level errors.
> What Not To Use
> Use only the released training rows and the public test inputs. Do not use external datasets, source archives found online, reverse-image lookup, manual annotation of test rows, hosted inference APIs, challenge-specific pretrained checkpoints, or GPU acceleration.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Visual Road-Corridor Route Synthesis

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74wnhsnfymwsscby2re5ymnx8c2ra1
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Infer a safe, smooth route through a forward-facing country-road image. The
> scenes were captured in daylight and generally good weather on roads in Santa
> Catarina, southern Brazil. They include asphalt, paved and unpaved surfaces as
> well as markings, patches, drainage structures, puddles, potholes, cracks,
> speed bumps, roadside background, and other obstacles.
> Each image is divided into a hidden 9-by-11 traversability grid. A submitted
> route chooses one column in each grid row, starting at the bottom of the image
> and moving toward the distant part of the road. Adjacent choices may stay in
> the same column or move by one column.
> The evaluator scores the decision itself against withheld dense surface and
> hazard annotations. The task is therefore not to submit a segmentation mask:
> participants must convert visual understanding into a globally coherent path.
> Task
> For every test image, predict a JSON list of nine column indices. List position
> 0 is the bottom grid row and position 8 is the top grid row. Columns run
> from 0 at the left to 10 at the right.
> Dataset
> The package contains 561 labeled training scenes and 140 test scenes. Images
> are 352 pixels wide by 288 pixels high and stored as RGB JPEG files. Training
> and test use separate scene partitions.
> The dense road-surface and hazard annotations used to calculate traversal
> costs are withheld. Training supervision consists of the minimum-cost route
> derived from those annotations.
> Public Files
> train.csv contains the 561 training inputs and their optimal routes.
> test.csv contains the 140 test inputs without route labels.
> sample_submission.csv contains one deterministic pseudo-random valid route
> for every test ID. It demonstrates the submission grammar and is not a
> baseline solution.
> images/ contains the 701 JPEG road scenes referenced by the CSV files.
> train.csv Columns
> id â€” string. Opaque unique scene identifier.
> image_path â€” string. JPEG path relative to the public directory.
> grid_rows â€” integer. Always 9; the route contains one decision for each
> grid row.
> grid_columns â€” integer. Always 11; valid route columns are 0 through
> 10.
> path_json â€” JSON-encoded string. A list of exactly nine integer column
> indices describing the optimal training route from the bottom grid row to
> the top grid row.
> test.csv Columns
> id â€” string. Opaque unique scene identifier.
> image_path â€” string. JPEG path relative to the public directory.
> grid_rows â€” integer. Always 9.
> grid_columns â€” integer. Always 11.
> test.csv does not contain path_json.
> sample_submission.csv Columns
> id â€” string copied from test.csv.
> path_json â€” JSON-encoded list of nine valid column indices.
> Submission Format
> Submit exactly two columns. A valid two-row example is:
> id,path_json
> route_bd42cf5241f85cdbffda,"[6,6,7,7,6,7,6,6,6]"
> route_75b8ea2d5e90d6079a83,"[5,6,5,4,5,4,4,4,4]"
> Every value must be an integer from 0 through 10, and the absolute
> difference between adjacent values must not exceed 1. Include every test ID
> exactly once and no additional columns. An invalid submission scores 0.
> Evaluation
> Each private pixel label has the following traversal cost before cell
> averaging: background 9.0; asphalt 1.0; paved road 1.2; unpaved road
> 1.5; road marking 1.8; speed bump 4.5; reflective marker 2.2; drain
> 3.0; cover 3.0; patch 3.4; puddle 6.2; pothole 8.0; crack 4.2.
> The cost of path p is:
> cost(p) = sum(r=0..8) grid_cost[r,p[r]] + 0.25 sum(r=1..8) |p[r]-p[r-1]|
> Let p* be the minimum-cost valid path and d = max(0, cost(p)-cost(p*)).
> U = exp(-d / 2)
> C = mean(r=0..8) [p[r] = p*[r]]
> T = mean(r=1..8) [(p[r]-p[r-1]) = (p*[r]-p*[r-1])]
> E = 1 when p = p*, otherwise 0
> Square brackets denote an indicator that is 1 when its condition is true and
> 0 otherwise. C is exact grid-cell accuracy, while T measures whether the
> submitted path makes the same left, straight, or right transition as the
> optimal path.
> The scene score is:
> R = 0.45 U + 0.25 C + 0.15 T + 0.15 E
> First calculate the robustness aggregate:
> A = 0.85 mean(R) + 0.075 worst_surface_mean(R) + 0.075 worst_hazard_level_mean(R)
> The reported score is Score = A^3. This strict calibration rewards routes
> that are consistently close to the private optimum rather than routes that
> merely remain near the road center.
> Scores are in [0,1], and higher is better.
> Expected Approach
> Relevant methods include CPU semantic features, road-boundary estimation,
> hazard detectors, coarse cost-map prediction, dynamic programming, and models
> that learn the planner's trade-off from the provided optimal training paths.
> What Not To Use
> Do not use GPU acceleration.
> Do not use internet access, external datasets, or hosted inference services.
> Do not recover answers through corpus lookup, metadata matching, manual test labeling, or hardcoded test mappings.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Ephemeroptera vs Trichoptera Larva Order Classification

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75md4ah9estwcs9p00h2mm1s8c37ch
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview: Classify each freshwater aquatic insect larva as belonging to the order Ephemeroptera (mayflies, label 0) or Trichoptera (caddisflies, label 1) from degraded 64x64 flow microscopy images. Both orders are ecologically important bioindicators found in clean freshwater systems, and their larvae are captured automatically by flow imaging devices deployed at sampling sites.
> The defining challenge is genus-disjoint generalization. The training set contains larvae from a specific subset of genera within each order: Leptophlebia and Caenis for Ephemeroptera, and Tinodes, Mystacides, Psychomyia, Cyrnus, and Polycentropus for Trichoptera. The test set contains entirely different genera that do not appear in training: Kageronia, Ephemera, Heptagenia, Cloeon, Centroptilum, and Baetis (Ephemeroptera) alongside Lepidostoma, Ecnomus, Limnephilidae, Limnephilus, Hydroptila, and other caddisfly genera (Trichoptera). A model that memorizes genus-specific texture or coloration will fail; the task demands learning the shared morphological hallmarks of each order that hold across unseen genera.
> Images have been degraded: downsampled to 64x64 pixels, with per-image Gaussian noise, five random horizontal scratch lines, and three 10x10 black occlusion patches. Test images additionally receive a randomized contrast scaling (0.80 to 1.20 multiplier). These degradations simulate high-throughput field conditions and prevent trivial memorization.
> Evaluation: The metric is macro-averaged F1 score: the unweighted mean of the per-class F1 scores for Ephemeroptera and Trichoptera. Because the test set is balanced (equal counts of each order), predicting all-zero or all-one both yield a macro-F1 of approximately 0.333. A random predictor scores approximately 0.50. A frozen ResNet18 with no fine-tuning, evaluated by nearest-neighbor on extracted features, scores approximately 0.60, which represents the upper bound achievable without any training on the provided images.
> def evaluate(y_true, y_pred): from sklearn.metrics import f1_score return f1_score(y_true, y_pred, average='macro', zero_division=0)
> Dataset: The public directory contains the following files.
> train/ Directory of 3,749 JPEG images (64x64 pixels). Filenames match img_id values in train.csv. test/ Directory of 606 JPEG images (64x64 pixels). Filenames match img_id values in test.csv. train.csv Training labels, one row per specimen. img_id - string - Unique specimen identifier, matches the image filename stem. order - integer - Taxonomic order label: 0 for Ephemeroptera, 1 for Trichoptera. test.csv Test specimen identifiers. No label column. img_id - string - Unique specimen identifier. sample_submission.csv Correctly-formatted submission template with all predictions set to 0. img_id - string - Unique specimen identifier. order - integer - Your predicted order label.
> Submission: Submit a CSV file with exactly 606 rows (one per test image) plus a header row. The required columns are img_id (matching values in test.csv) and order (integer 0 or 1). Row order does not matter.
> Example submission (3 sample rows): img_id,order larva_00042,0 larva_00081,1 larva_00093,0
> Rules: The only valid input signal is the image pixels within each 64x64 JPEG file. The following approaches are not allowed:
> Hardcoding predictions for specific test images.
> Using specimen identifiers (img_id values) or image filenames as a prediction signal instead of the image content.
> Using JPEG metadata, file size, or compression artifacts as a classification signal.
> Looking up the test genera listed in this description via an external taxonomy database to assign labels without using the provided images.
> Using private, role-gated, or API-key-based models, or calling any external inference API at inference time.
> Using non-reproducible external weights or artifacts not publicly available.
> The intended task is to learn the visual morphological features that distinguish Ephemeroptera from Trichoptera across genuinely unseen genera. Within each order, morphology varies substantially: Ephemeroptera range from flat-headed sprawlers (Kageronia, Heptagenia) to burrowing forms with projecting tusks (Ephemera) to small streamlined swimmers (Baetis, Cloeon, Centroptilum), while Trichoptera range from slender net-spinning forms (Ecnomus, Neureclipsis) to bulky case-bearers (Limnephilus, Lepidostoma) to tiny micro-caddis (Hydroptila, Oxyethira). A model that generalizes correctly must capture order-level morphological structure rather than genus-specific appearance.
> Pretrained model policy: Fine-tuning a publicly available pretrained model (ResNet, EfficientNet, ViT, or similar) is allowed and encouraged. A frozen ResNet18 with no fine-tuning scores approximately 0.60 using nearest-neighbor on ImageNet features; fine-tuning the backbone on the provided training images is the intended path to improve beyond that level. The genus-disjoint split means the model must generalize order-level morphology to genuinely unseen genera, so the training images are the essential signal regardless of pretraining.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Hive Resource Balance Regime from Frame Images

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77y28thq3aegncd1qaf214bx8c42eg
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Not shown/captured

Full challenge description from page:

> Hive Resource Balance Regime from Frame Images
> Overview
> A colony-monitoring system receives one image of a single hive frame at a time. The image can contain cells associated with developing brood, stored food, open comb, and the surrounding frame. Your task is to infer the frame's resource balance regime from visual evidence alone. The regime is an image-level operational summary, not the name of one visible object.
> The four regimes describe the dominant composition of the frame: brood-dominant, forage-dominant, mixed-resource, or sparse/uncertain. A useful model must learn fine-grained visual differences between visually similar cells and remain useful when the acquisition style changes between training and test images. The public training split has 979 images; the private test split has 245 images from eight held-out acquisition/sequence groups.
> The operational label policy is composition-based: brood-dominant and forage-dominant require at least half of the non-frame cell evidence to belong to the corresponding resource family; sparse/uncertain is used for an empty-evidence share of at least 60% or no cell evidence; all remaining frames are mixed-resource.
> Dataset
> File descriptions
> train.csv -- Labeled image index with one row per training image.
> test.csv -- Unlabeled image index with one row per test image.
> train/ -- 320x224 JPEG images referenced by train.csv.
> test/ -- 320x224 JPEG images referenced by test.csv.
> sample_submission.csv -- Submission template with a valid random regime for each test image.
> Column descriptions
> id (string) -- Stable 12-character identifier for one image.
> image_path (string) -- Relative path to the image under the supplied public image folders.
> target (string, train only) -- One of brood_dominant, forage_dominant, mixed_resource, or sparse_uncertain.
> Evaluation
> Submissions are scored using Composition-Weighted Macro F1 (CWM-F1), which is maximized. It combines overall regime quality, performance on the two decision-critical regimes, and balanced per-regime recall:
> ALL_REGIMES = [
> "brood_dominant", "forage_dominant", "mixed_resource", "sparse_uncertain"
> ]
> overall_f1 = macro_f1(y_true, y_pred, labels=ALL_REGIMES)
> critical_f1 = macro_f1(y_true, y_pred,
> labels=["brood_dominant", "sparse_uncertain"])
> balanced_accuracy = mean(
> recall(y_true, y_pred, regime) for regime in ALL_REGIMES
> )
> score = (0.55  *overall_f1 + 0.25*  critical_f1
> + 0.20 * balanced_accuracy)
> All component scores are in [0, 1], so the final score is also in [0, 1].
> Submission
> Submit a CSV file with one prediction for every row in test.csv.
> id (string) -- The 12-character identifier from test.csv.
> target (string) -- One of brood_dominant, forage_dominant, mixed_resource, or sparse_uncertain.
> Example:
> id,target
> 04bd67054490,brood_dominant
> 024dea6e68a3,mixed_resource
> Requirements
> The file must contain exactly one row for every image in test.csv.
> Every id from test.csv must appear exactly once.
> Every prediction must be one of the four allowed regime strings.
> File format: .csv only, with exact column names id,target.
> What Not To Use
> Do not recover image labels or cell annotations from files outside the supplied public folders; that bypasses the image-learning task.
> Do not use filename metadata, row order, or reverse maps from the hashed image IDs to infer a regime.
> Do not use a checkpoint trained specifically on this challenge's images or annotations. A general-purpose image backbone is allowed only when it is trained or fine-tuned as part of the submitted solution.
> Do not submit a fixed color-threshold or annotation-count lookup in place of a trained image model; the challenge evaluates visual generalization under a held-out acquisition group.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## The Split Verdict: Forecasting Assessor Discord On Rodent-Face Imagery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx722w61tzh5gn9ed7jfhah3ph88mtxd
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat iqbalez's score of 0.788!

Full challenge description from page:

> Leaderboard
> (20)
> Your Submissions
> The Split Verdict — Contention-Capture Triage on Rodent-Face Imagery
> Task
> You are given cropped rodent (mouse) face images. Each face was independently rated by a
> panel of trained expert assessors, every assessor working alone, on a structured rubric of
> five facial regions (each region marked 0, 1, or 2). The panel does not speak with one voice:
> for many faces the assessors land on different marks.
> You are building the triage front door of a labelling pipeline. For each test face you output
> a single review priority — a free‑scale number saying how urgently that face should be pulled
> out and sent to a human to adjudicate. You are not asked to recover the panel's rating, and
> you are not asked to predict a calibrated number. You are asked to order the faces so that
> the ones the panel most splits on rise to the top of your queue.
> The reason this is not the obvious problem in disguise: a model that reproduces the panel's
> consensus mark learns almost nothing about where the panel splits. A face's contention —
> how far the panel's independent verdicts scatter — is governed by its visual indeterminacy: a
> frame caught in motion, a head turned away, a region behind an occluder, an expression captured
> mid‑transition, an exposure unlike the rest. Those cues are only loosely coupled to the mark
> itself. To win you must learn what makes a face hard for a panel to agree on — exactly the signal
> a real pipeline uses to decide which images are worth a human's time.
> Data
> The public/ folder contains the images and three CSV files:
> public/
> ├── images/                 # all face crops, one .jpg per image_id (train + test)
> ├── train.csv               # labelled training faces: image_id, contention
> ├── test.csv                # faces to triage: image_id (contention hidden)
> └── sample_submission.csv   # a valid example submission you can overwrite
> **images/** — about 1,155 de-identified rodent-face crops, one per row, named
> <image_id>.jpg. Each is an 8-bit RGB JPEG, 112×112 pixels, lightly transformed (small
> random crop, optional horizontal flip, mild brightness/contrast jitter, lossy re-encode) and
> given a fresh random id so it cannot be traced to a source. The folder holds every served
> face, both train and test.
> The faces come from about 314 animals (subjects); the split is by subject (see below).
> **train.csv** — one row per training face (about 982 rows). Two columns:
> **image_id** — data type string. Opaque face id (fc-<n>-<rand>); matches
> images/<image_id>.jpg.
> **contention** — data type float (≥ 0). The face's realized panel scatter — the target
> quantity your queue must concentrate (defined below). Larger = the panel's verdicts spread more.
> **test.csv** — one row per test face (about 173 rows, one face per animal). One column:
> **image_id** — data type string. Opaque face id; its contention is hidden — triaging these
> faces is the task.
> **sample_submission.csv** — a valid, ready-to-overwrite example (about 173 rows). Two columns:
> **image_id** — data type string. Copied from test.csv.
> **priority** — data type float. A weak image-legibility baseline priority; overwrite it with
> your own.
> The split is by subject (animal): every face of a given animal is entirely in train or entirely
> in test (about 141 train animals and 173 test animals, disjoint). The test set serves a
> single face per animal, so per-subject memorisation does not transfer and the test faces cannot
> be clustered back into per-animal groups — each test face must be judged on its own.
> How contention is defined
> For one face, take the assessors who marked each of the five regions, compute the variance of
> their 0/1/2 marks for that region, and average those variances across the five regions. Larger =
> the panel scattered more. Only faces marked by at least three assessors are included, so the
> quantity is stable.
> Submission format
> A CSV with a header and **exactly one row per test image_id**:
> image_id,priority
> The submission has exactly two columns:
> **image_id** — data type string. The identifier, copied from test.csv.
> **priority** — data type float. Your review-priority key — higher = send to a human sooner.
> Any real number; only the ordering of your values is used.
> **priority is a ranking key, not a value to match.** train.csv gives the target contention;
> your submission gives priority, which is whatever score you want to sort the faces by. The
> grader never compares priority to contention numerically — it only reads the order your
> priority imposes and asks how fast that order captures the true contention. So priority
> can be a predicted contention, a quality score, a probability, a raw confidence — anything
> monotonic with "how contentious this face is".
> Provide a value for every image_id in test.csv — duplicate, unknown, or missing ids
> are rejected. priority is coerced numeric; an invalid value (NaN, inf, or unparseable) is
> sent to the bottom of the queue (lowest priority), so it can never be ranked ahead of a real
> value, whatever numeric scale you use.
> Example
> image_id,priority
> fc-552-t14kc,0.04
> fc-633-6owo5,0.31
> fc-602-f4wsa,0.12
> Note: image_ids are random (fc-<n>-<rand>) and the faces are lightly transformed — they
> cannot be matched to their public collection of origin. Recovering the per-assessor verdicts by
> matching, or importing them from outside, is prohibited (WHAT_NOT_TO_USE.md); your
> priority must come from a model trained on the provided images.
> Scoring
> Your priority is read on two complementary facets, which are then passed through a
> form-agnostic nonlinear response so the score does not hinge on any single curve.
> Facet 1 — contention capture (magnitude-weighted). Sort the faces by your priority,
> most-urgent first, and walk the queue. The faster the panel's true contention accumulates, the
> better, measured against a random queue (0) and the oracle queue (1):
> w_i      = n - (queue position of face i by your priority) + 1     # first reviewed = n, last = 1
> A_you    = sum_i  contention_i * w_i
> A_random = sum_i  contention_i * (n + 1) / 2
> A_oracle = A_you computed with faces in true-contention order
> C        = (A_you - A_random) / (A_oracle - A_random)
> This is the normalised area between your contention-capture curve and the random-triage
> diagonal, divided by the oracle's. It is magnitude-weighted: placing the most contentious
> faces at the head of the queue is worth far more than ordering the placid tail.
> Facet 2 — rank agreement. R = Spearman rank correlation between your priority and the true
> contention (ties at the average rank).
> Combine. The two facets form a weighted-geometric base skill b, which is mapped to the final
> score by the average of six endpoint-matched response curves — exponential, logarithmic, sine,
> raised-cosine, tangent, and hyperbolic-tangent:
> b     = clip(C, 0, 1)^0.6  *  clip(R, 0, 1)^0.4
> score = clip( mean_k  g_k(b), 0, 1 ),   averaged over the six curves
> g1(b) = (exp(2.5 b) - 1) / (exp(2.5) - 1)        g2(b) = ln(1 + 4 b) / ln(5)
> g3(b) = sin(pi b / 2)                            g4(b) = (1 - cos(pi b)) / 2
> g5(b) = tan(1.3 b) / tan(1.3)                    g6(b) = tanh(2 b) / tanh(2)
> Every g_k satisfies g_k(0) = 0 and g_k(1) = 1, so a perfect ordering scores exactly 1 and
> a no-skill ordering scores exactly 0 — the response bank only reshapes the climb in between, and
> only the ordering of your priority ever matters. A constant or random priority scores ≈ 0;
> queueing the least-contentious faces first scores 0 (clipped); the oracle ordering scores 1.
> Why it is hard. Part of the contention is plain legibility (a blurred or badly-framed face is
> hard for anyone), and a simple image-quality priority already reaches the baseline. Beating it
> means reading the subtler drivers of disagreement — ambiguous pose and expression — and even the
> oracle does not reach the visual ceiling, because with a handful of assessors the realized scatter
> carries real noise. The headroom above the image-quality baseline is exactly the part that requires
> genuinely understanding what makes a face contentious.
> What earns a high score
> A priority that captures visual indeterminacy beyond sharpness — pose, occlusion, framing,
> and ambiguous or transitional expressions — not just a consensus-mark predictor.
> Getting the most contentious faces to the very top of the queue (the metric rewards the head
> of the queue far more than the tail).
> Sensible regularisation and subject-aware validation (each training animal contributes
> several faces; the test set has one face per animal), and a priority for every test face.
> What you may and may not use
> The task is to assign each test face a review priority that orders faces by their
> contention — how far an expert panel's independent verdicts spread for that image. The rules
> keep it about modelling the image, not recovering the panel's verdicts by matching the faces to
> their public origin.
> Prohibited — origin lookup and verdict recovery (automatic disqualification)
> These faces are drawn from a publicly available collection whose per-assessor verdicts are also
> published, so the true contention could be looked up if the images were re-identified. To prevent
> that, every served face carries a fresh random opaque id (fc-<n>-<rand>) and a light
> transform, and the following are forbidden:
> Matching / re-identifying the served faces against their public collection of origin, or any
> external source — by pixel/byte comparison, hashing, nearest-neighbour search, reverse-image
> search, metadata, or learned-feature similarity — to recover the per-assessor verdicts or the
> contention value.
> Importing the origin's per-assessor verdicts, or any externally computed scatter, for these
> images. Your priority must be **produced by a model trained only on the provided train.csv**.
> Cached / hard-coded / memorised contention values of any kind.
> **Parsing the image_id** or any id/order pattern to infer the target (ids are random).
> Grader gaming: exploiting the capture-curve computation, tie handling, validation, or numeric
> edge cases instead of modelling. (A constant or random priority scores ≈ 0 by design.)
> Re-scoring the test faces by human assessors or an external service.
> Submissions found to rely on any of the above are out of scope and may be rejected.
> Allowed
> Any ML approach trained on train.csv: convolutional nets, vision transformers, transfer
> learning / fine-tuning from generic pretrained weights, feature extractors + a regressor,
> ensembles, etc.
> Building your priority however you like: regress the contention directly and use it as the
> priority; or model image legibility (sharpness, head angle, occlusion, framing, capture
> conditions); or predict the rubric's five regions and derive a scatter proxy; or fit a
> heteroscedastic / variance head. All fair — only the ordering of your priority is scored.
> Standard augmentation, subject-aware cross-validation (each animal contributes several
> faces), test-time augmentation.
> numpy, pandas, scikit-learn, PyTorch/TensorFlow, Pillow, scikit-image, opencv
> and similar general libraries (generic pretrained backbones are fine; a model or service that
> returns these images' original per-assessor verdicts is not).
> The spirit of the task
> The goal is to read, from the face alone, how hard that face would be for a panel to agree on,
> and to put the hardest faces at the front of the review queue. The signal must come from a model
> trained on the provided images, never from recovering the verdicts by lookup or matching. A good
> consensus-predictor is not enough: a face's contention lives in its visual indeterminacy, a
> different and harder property to read off the pixels.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Budgeted Concrete Damage Inspection Planning

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75t3sakdamwpc587geakpx418ahr2d
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↓ Lower is better
- Tags: Not shown/captured
- Best/top context found: Beat aneeshm44's score of 0.345!

Full challenge description from page:

> Leaderboard
> (17)
> Your Submissions
> Budgeted Concrete Damage Inspection Planning
> Overview
> Infrastructure inspection systems cannot acquire every close-range view when flight time, access, or review capacity is limited. In this challenge, each concrete-surface overview has nine overlapping candidate inspection regions with different acquisition costs. Your task is to prioritize those regions under multiple budgets while estimating how much crack and spalling damage each region would reveal.
> This is a structured visual decision problem, not a segmentation submission. A useful solution must identify likely damage, account for candidate size and cost, and avoid spending the budget on redundant overlapping regions.
> For every candidate, submit:
> three budget-specific priority scores that define its position in the inspection order at budgets 3, 6, and 9;
> predicted_crack_yield, the predicted crack area inside the region as a fraction of the full 320 x 320 overview;
> predicted_spall_yield, defined in the same way for spalling.
> The hidden planning utility of a selected set is the unique, non-duplicated crack area plus twice the unique spalling area covered by its union. Spalling receives additional weight because it is much rarer in this dataset. Pixels covered by several selected regions contribute only once.
> Generalization Protocol
> Each overview is a deterministic, anonymized geometrically and photometrically transformed view derived from one source patch. Candidate geometry and all targets are measured in the released 320 x 320 coordinate system. Source masks, polygons, filenames, and difficulty labels are not released.
> The source has no capture-session, structure, site, device, or timestamp identifiers. The publisher's Easy and Medium visual partitions form the training set, while its entire Hard partition is held out for testing. Partition names are not released. The protocol measures transfer to visually difficult cases, but it does not establish cross-dam, geographic, temporal, or device-held-out generalization.
> Inspection Policy
> For each instance and budget, candidates are sorted by the corresponding priority_score_b3, priority_score_b6, or priority_score_b9, with lower candidate_id breaking an exact tie. The evaluator scans that budget-specific order and selects a candidate when its inspection_cost fits within the remaining budget. Candidates that do not fit are skipped. The budgets are 3, 6, and 9 cost units. Separate orders prevent an unavoidable compromise in which one ranking must represent three different oracle subsets.
> For each budget, the selected plan is compared with the best feasible subset among all 512 subsets of the nine candidates:
> weighted_utility(S) = unique_crack_fraction(S)
> + 2 * unique_spall_fraction(S)
> regret_b = 0                                      if oracle_utility_b = 0
> regret_b = 1 - selected_utility_b/oracle_utility_b otherwise
> PlanningRegret = mean(regret_3, regret_6, regret_9 over all instances)
> Candidate-yield calibration is evaluated independently:
> CrackRMSE = RMSE(predicted_crack_yield) / 0.03
> SpallRMSE = RMSE(predicted_spall_yield) / 0.06
> raw_loss = 0.85 * PlanningRegret
> + 0.075 * CrackRMSE
> + 0.075 * SpallRMSE
> score = min(1, raw_loss / 0.20)
> Lower is better, and the score is bounded from 0 to 1 inclusive. For every raw_loss < 0.20, which is the region intended to distinguish competent solutions, the normalization is linear: a reduction of 0.01 in raw loss always reduces the reported score by 0.05. Losses at or above 0.20 receive the maximum score of 1. This cap keeps the declared score range meaningful without compressing the competitive region. Priority-score magnitudes do not enter the loss and affect only ordering. A submission with exact yields and an oracle order for each budget scores 0; unlike a single shared order, the submission format can represent that solution. The dominant term rewards inspection decisions rather than independent candidate regression.
> Dataset
> public/
> |-- train.csv
> |-- test.csv
> |-- sample_submission.csv
> |-- train_images/
> `-- test_images/
> There are 1,000 training instances and 500 test instances, with nine candidate rows per instance. Thus, train.csv contains 9,000 rows and test.csv contains 4,500 rows. Every overview is a 320 x 320 RGB JPEG. Image paths are relative to ./dataset/public/.
> Shared columns
> Column	Type	Description
> instance_id	integer	Anonymized overview identifier.
> candidate_id	integer	Candidate identifier from 0 through 8 within an instance.
> image_path	string	Relative path to the shared overview image.
> x0, y0	integer	Inclusive upper-left candidate coordinates.
> x1, y1	integer	Exclusive lower-right candidate coordinates.
> inspection_cost	integer	Cost units consumed if the candidate is selected.
> Training-only labels
> Column	Type	Description
> crack_yield_fraction	float	Crack pixels inside this candidate divided by the full overview area.
> spall_yield_fraction	float	Spalling pixels inside this candidate divided by the full overview area.
> The two training labels are singleton yields. They do not reveal the utility of overlapping candidate combinations because duplicate damage must be counted only once.
> Submission
> Write ./working/submission.csv with exactly these columns:
> Column	Type	Description
> instance_id	integer	Test instance identifier.
> candidate_id	integer	Candidate identifier.
> priority_score_b3	float	Any finite score; larger values are inspected earlier at budget 3.
> priority_score_b6	float	Any finite score; larger values are inspected earlier at budget 6.
> priority_score_b9	float	Any finite score; larger values are inspected earlier at budget 9.
> predicted_crack_yield	float	Candidate crack yield prediction in [0, 1].
> predicted_spall_yield	float	Candidate spalling yield prediction in [0, 1].
> Example:
> instance_id,candidate_id,priority_score_b3,priority_score_b6,priority_score_b9,predicted_crack_yield,predicted_spall_yield
> 100000,0,7.2,8.1,6.4,0.0081,0.0000
> 100000,1,8.9,7.4,8.8,0.0144,0.0032
> 100000,2,6.1,8.7,7.3,0.0067,0.0000
> Requirements:
> Include exactly one row for every test instance/candidate pair; row order does not matter.
> Include exactly the seven required columns.
> IDs must be finite integers and candidate IDs must be in [0, 8].
> All three priority scores must be finite; exact ties within an order are resolved by candidate ID.
> Yield predictions must be finite and within [0, 1].
> CPU-Compatible Approaches
> The task is designed for CPU training and inference. Practical approaches include region-level color and texture features, edge statistics, compact regressors, low-resolution neural models trained from scratch, and overlap-aware greedy selection. A useful planning baseline should compare predicted damage gain per cost while discounting portions already covered by earlier candidates.
> The supplied sample submission uses candidate geometry and global training-label means without learning from image content. It repeats its geometry order at all three budgets and receives the maximum score of 1.000000 on the private answers (its uncapped normalized loss is 1.028793), with planning regret 0.205987.
> The included CPU reference uses candidate-crop features, an ExtraTrees yield regressor, and overlap-aware greedy prioritization. For simplicity it repeats one learned order at all three budgets; budget-specific subset optimization is an immediate route beyond this feasibility reference. It completes in about one minute on the creator CPU and scores 0.662390, with planning regret 0.120106. These are feasibility references, not target performance levels.
> Allowed and Prohibited
> Allowed:
> Use only files under ./dataset/public/.
> Train on the released overview images, candidate geometry, costs, and training labels.
> Use CPU-compatible preprocessing, classical models, compact CPU neural networks, ranking methods, optimization, calibration, and ensembling with available libraries.
> Prohibited:
> Do not access ./dataset/private/ or answer files.
> Do not use source images, masks, annotations, identifiers, or external image-matching materials.
> Do not recover targets from hidden preparation artifacts or source membership.
> Do not require GPU hardware, GPU-only libraries, or external model downloads.
> Expected Output
> ./working/submission.csv

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Paired Image Description Demixing

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71q0b2bvjpjrw97ewxha3knx8c89cq
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat moatasem's score of 0.702!

Full challenge description from page:

> Leaderboard
> (19)
> Your Submissions
> Overview
> Detailed image descriptions support accessibility, visual search, dataset auditing, and evaluation of vision-language systems. A difficult failure occurs when descriptions from two visually similar images are mixed: most objects remain plausible, but attributes, counts, positions, actions, or background details are assigned to the wrong image.
> Every challenge case contains a paired image sheet and one shuffled pool of textual fragments. Image A is shown on the left and Image B on the right. The images come from the same related-scene family and deliberately share subjects, environments, and vocabulary. Their decisive difference may be one number, color, orientation, object state, spatial relation, viewpoint, or background element.
> The fragment pool combines statements from both detailed descriptions. It also contains one fact that applies to both images and one plausible distractor that applies to neither. Your task is to decide the provenance of every fragment and recover the correct discourse order for both descriptions.
> This is not ordinary captioning because all output text is supplied. It is not independent image-text retrieval because every fragment participates in one coupled two-image reconstruction. It is also different from visual difference summarization: the output must retain complete image-specific and shared content while rejecting distractors and producing two ordered sequences simultaneously.
> The challenge is designed for CPU solutions. Compact 128-pixel paired images, visual concept tags, and fixed numeric image descriptors are released. A practical solution can combine TF-IDF or compact sentence representations with linear models, gradient boosting, ranking models, and the supplied descriptors without training a large vision-language model.
> Task
> For every test case, return:
> the ordered fragment sequence describing Image A; and
> the ordered fragment sequence describing Image B.
> Every fragment has a case-local identifier such as F01 or F12. A fragment belongs to exactly one of four provenance classes:
> A_ONLY — present only in the Image A sequence;
> B_ONLY — present only in the Image B sequence;
> BOTH — present in both sequences; or
> NEITHER — present in neither sequence.
> Each fragment may appear at most once in an individual sequence.
> Reconstruction Rules
> Predictions must follow these rules:
> Include every fragment supported by the corresponding image.
> Include a shared fragment in both sequences.
> Omit distractors from both sequences.
> Do not duplicate a fragment within one sequence.
> Recover the target discourse order within each sequence.
> Use only fragment identifiers supplied in the corresponding case.
> Use uppercase A: and B: section markers.
> Join fragments with >.
> Separate the two sequences with |.
> Do not include whitespace in the serialized prediction.
> A valid prediction has the form:
> A:F03>F07>F01|B:F06>F02>F05
> Data Files
> train.jsonl — 6,141 training cases with target reconstructions.
> test.jsonl — 1,243 test cases without targets.
> images/ — one 260×128 WebP paired-image sheet per case; A is left and B is right.
> train_visual_features.npy — float16 training descriptor array.
> test_visual_features.npy — float16 test descriptor array.
> sample_submission.csv — a complete formatting example.
> The test set is approximately 20% of the training-set size.
> JSONL Fields
> Both JSONL files contain:
> case_id — opaque unique case identifier.
> image_pair_path — relative path to the paired-image sheet.
> image_a_side — always left.
> image_b_side — always right.
> feature_index — row index in the corresponding visual-feature array.
> visual_tags_a — compact visual concept tags for Image A.
> visual_tags_b — compact visual concept tags for Image B.
> fragments — shuffled objects containing fragment_id and fragment text.
> train.jsonl additionally contains:
> target_a — ordered fragment identifiers for Image A.
> target_b — ordered fragment identifiers for Image B.
> target_prediction — canonical serialized target.
> Fragment identifiers are assigned independently in every case. F03 has no consistent meaning or position across cases. Fragment array order is randomized separately from fragment identifiers.
> Visual Feature Arrays
> The visual feature arrays have shape:
> [number_of_cases, 2, 544]
> Axis 1 uses Image A at index 0 and Image B at index 1. For each image, the 544 float16 features are:
> indices 0:432 — a 12×12 RGB thumbnail flattened in row-major channel-last order;
> indices 432:480 — three normalized 16-bin color histograms; and
> indices 480:544 — an 8×8 grayscale thumbnail.
> All values are finite. Thumbnail values are scaled to [0,1].
> Fragment Construction
> Human-authored descriptions are divided at sentence or independent-clause boundaries. Long descriptions are reduced to at most eight contiguous fragments without changing word order inside a fragment.
> Each case also contains four short atomic statements constructed in the same range of surface forms:
> one visual concept specific to Image A;
> one visual concept specific to Image B;
> one concept shared by both images; and
> one visually plausible distractor from another image in the same related-scene family.
> Because all four atomic roles use the same statement templates, template detection does not reveal provenance. Distractors are selected within the same related-scene family rather than from unrelated random images.
> Evaluation
> The metric evaluates fragment provenance, within-description order, and complete reconstruction.
> Provenance Macro F1
> For every valid fragment, the grader derives one of A_ONLY, B_ONLY, BOTH, or NEITHER from the two submitted sequences.
> For provenance class c:
> F1_c = 2 × TP_c / (2 × TP_c + FP_c + FN_c)
> The provenance score is the unweighted mean across all four classes:
> provenance_macro_f1 = (F1_A_ONLY + F1_B_ONLY + F1_BOTH + F1_NEITHER) / 4
> Counts are pooled across all evaluated cases before class F1 is calculated.
> Pairwise Order F1
> Each submitted sequence is converted into ordered fragment pairs. For example:
> F03>F07>F01
> produces:
> (F03,F07), (F03,F01), (F07,F01)
> For every case and image side, submitted pairs are compared with target pairs. Counts are pooled across cases and both image sides:
> order_precision = correct_submitted_pairs / submitted_pairs
> order_recall = correct_submitted_pairs / target_pairs
> order_f1 = 2 × order_precision × order_recall / (order_precision + order_recall)
> Exact Reconstruction
> For case i:
> exact_i = 1
> only when both submitted sequences exactly equal their target sequences. Otherwise:
> exact_i = 0
> The exact reconstruction rate is:
> exact_rate = mean(exact_i)
> Final Score
> score = 0.60 × provenance_macro_f1 + 0.30 × order_f1 + 0.10 × exact_rate
> The score ranges from 0.0 to 1.0, and higher is better. An exact submission scores 1.0.
> Split and Leaderboard Design
> The independent split unit is a related-image family. Every image, pair, fragment set, and derived atomic statement from one family remains entirely within train or test. No original image appears on both sides.
> The source contains 149 related-image families. The challenge assigns 125 families to train and 24 to test. Within test, 9 complete families contribute 313 cases to the public leaderboard, while 15 complete families contribute 930 cases to the private leaderboard.
> No family crosses public/private visibility. The largest family contributes approximately 15.4% of public cases and 10.3% of private cases.
> Submission
> Submit a CSV containing exactly these columns in this order:
> case_id,prediction
> Provide exactly one row for every test case_id.
> Complete example:
> case_id,prediction
> TE000001,"A:F03>F07>F01|B:F06>F02>F05"
> TE000002,"A:F04>F09>F02>F08|B:F05>F01>F08"
> In the second example, F08 is shared by both images.
> Column names, markers, and fragment identifiers are case-sensitive.
> The complete submission receives 0.0 if it contains:
> missing, extra, duplicate, or reordered columns;
> missing, extra, or duplicate case identifiers;
> blank or non-string predictions;
> leading, trailing, or internal whitespace;
> unknown fragment identifiers;
> a duplicate fragment within one image sequence;
> missing A: or B: sections; or
> malformed separators or extra sections.
> Expected Output
> A successful system should compare the images jointly, separate image-specific content from shared content, reject plausible within-family distractors, and reconstruct two coherent descriptions from one mixed fragment pool.
> What Not to Use
> Do not use fragment identifiers or JSON array positions as provenance or ordering features. Both are randomized per case.
> Do not treat Image A and Image B as unrelated retrieval examples. Hard pairs share objects and vocabulary and differ in fine details.
> Do not assign every fragment to exactly one image. Every case contains a shared fragment and a distractor.
> Do not rely only on exact tag matching. Long fragments contain attributes and relations not represented by the compact tag lists.
> Do not ignore discourse order. Correct provenance with arbitrary ordering cannot receive full credit.
> Do not generate new captions or paraphrases. Only released fragment identifiers are accepted.
> Do not use filenames, case identifiers, directory order, or descriptor indices as semantic features.
> Do not use reverse-image search or attempt to recover the original source descriptions externally.
> Do not manually label test pairs or create test-specific lookup tables.
> Do not infer targets from sample_submission.csv; it is only a formatting example.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Reciprocal Pattern Orbit Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7agpznv7w38p6k1046jzmwxn8c7861
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat douglas's score of 0.371!

Full challenge description from page:

> Leaderboard
> (13)
> Your Submissions
> Overview
> Predict which panels on a six-panel diffraction board came from the same acquisition run, then recover the discrete display rotation and reflection relating panels in each group. The final output is a compact run partition, three relative-action tokens, and a 6 x 6 closure matrix that certifies the same relationships.
> In single-crystal alignment work, a short run contains several measurements made while alignment is adjusted. Spot locations therefore move naturally from one step to the next. A useful model must recognize that different steps belong to one run while also accounting for display rotation, reflection, clipping, exposure drift, and obstruction. This benchmark turns that verification step into a constrained learned reconstruction task.
> Each board contains six labeled panels, A through F. Exactly three panels are distinct steps from one acquisition run, two are distinct steps from a second run, and one comes from a third run. All three runs use the same crystal family, so material appearance cannot solve the partition. The displayed panels include independent contrast changes, small angular jitter, translations, center-marker masking, edge loss, detector dust, and blur.
> Dataset
> The inputs are derived from real room-temperature x-ray backreflection measurements. Complete acquisition runs are assigned to one split before any board is constructed, so neither a hidden source image nor another step from its run appears in training.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Input columns and labeled orbit certificates. |
> | `test.csv` | Input columns only. |
> | `sample_submission.csv` | Schema-valid baseline. |
> | `orbit_boards/*.jpg` | `720 x 480` RGB JPEG boards with a `3 x 2` panel layout. |
> CSV Columns
> | Column | Data type | Availability | Description |
> |---|---|---|---|
> | `case_id` | string | train and test | Opaque unique case identifier. |
> | `orbit_board_path` | string | train and test | Relative path to the six-panel image. |
> | `board_contract` | string | train and test | Declares panel labels, layout, and the discrete action group. |
> | `orbit_partition` | canonical string | train only | Partition of `A` through `F` into acquisition-run groups of sizes 3, 2, and 1. |
> | `relative_action_word` | ordered token string | train only | Three root-to-member dihedral action tokens. |
> | `closure_matrix` | JSON integer matrix | train only | Symmetric `6 x 6` relationship certificate with values 0, 1, or 2. |
> Orbit Partition
> Letters inside a group are alphabetically sorted. Groups are ordered by their first letter and separated by |. For example:
> ACF|BE|D
> This means A, C, and F come from one run; B and E come from another; and D is the singleton run.
> Relative Actions
> The alphabetically first panel in each non-singleton group is its root. One token is emitted for every other group member:
> <root>><member>:r<rotation>f<reflection>
> rotation is a zero-padded integer from 00 through 11, representing multiples of 30 degrees. reflection is 0 for orientation-preserving and 1 for reflected. Exactly three tokens are required and are joined with ;. Tokens are ordered first by root and then by member. The > character appears only inside a token to indicate direction from the root to the member.
> Example:
> A>C:r03f0;A>F:r09f1;B>E:r01f0
> Closure Matrix
> Rows and columns follow A,B,C,D,E,F.
> | Value | Meaning |
> |---:|---|
> | 0 | The panels come from different acquisition runs. |
> | 1 | The panels share a run and their relative display action preserves orientation. The diagonal is also 1. |
> | 2 | The panels share a run and their relative display action contains a reflection. |
> The matrix must be symmetric, have shape 6 x 6, and contain only integers from 0 through 2.
> Evaluation
> The metric is the Reciprocal Orbit Certificate Score.
> BaseScore = 0.40 * PartitionScore
> + 0.35 * ActionScore
> + 0.25 * ClosureScore
> FinalScore = BaseScore * (0.92 + 0.08 * CoherenceRate)
> Minimum score: 0.0.
> Maximum score: 1.0.
> Higher scores are better.
> PartitionScore
> For a partition, form the set of all unordered panel pairs that belong to the same group. relation_F1 is standard set F1 between the predicted and true pair sets.
> row_partition_score = 0.38 * relation_F1
> + 0.62 * exact_partition_match
> PartitionScore is the mean row score.
> ActionScore
> The three action tokens are compared as sets and as a canonical ordered word.
> row_action_score = 0.32 * token_set_F1
> + 0.68 * exact_action_word_match
> ActionScore is the mean row score.
> ClosureScore
> For each matrix entry, correct agreement receives weight 2.4 when the true value is 1 or 2 and weight 1.0 when the true value is 0. Weighted agreement is the sum of weights on correct entries divided by the sum of all entry weights.
> row_closure_score = 0.25 * weighted_entry_agreement
> + 0.75 * exact_matrix_match
> ClosureScore is the mean row score.
> CoherenceRate
> A row is coherent when the nonzero off-diagonal matrix pairs exactly equal the within-group pairs in orbit_partition, and every action token joins two panels in the same submitted group. CoherenceRate is the fraction of coherent rows.
> Malformed values receive zero for their component. The grader bounds string and JSON lengths before parsing.
> Submission Format
> Write the final file to:
> ./working/submission.csv
> It must contain exactly these columns in this order:
> case_id,orbit_partition,relative_action_word,closure_matrix
> All CSV fields are strings. The matrix is a JSON-encoded string.
> case_id,orbit_partition,relative_action_word,closure_matrix
> lo_4417fc3e7054be207ff2,ACF|BE|D,A>C:r03f0;A>F:r09f1;B>E:r01f0,"[[1,0,1,0,0,2],[0,1,0,0,1,0],[1,0,1,0,0,2],[0,0,0,1,0,0],[0,1,0,0,1,0],[2,0,2,0,0,1]]"
> The grader rejects extra or reordered columns, duplicate IDs, missing IDs, unknown IDs, and wrong row counts. An optional backend-managed visibility column is ignored.
> Expected Methods
> Suitable approaches include compact learned diffraction descriptors, contrastive multi-view training, pairwise orbit affinity prediction, discrete action heads, and constrained graph decoding. CPU inference is practical because each board contains only six moderate-resolution panels.
> What Not To Use
> Do not use IDs, row order, JPEG byte size, path strings, source-file recovery, external archive lookup, or fixed panel-position rules as predictors. Do not use handcrafted image matching or lookup tables as the main decision mechanism. Predictions must come from a learned model applied to the supplied board.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Synoptic Report Repair from Temporal Sky Evidence

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7005f3q49j16wgqx9qevaz6x8c1471
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat masry1's score of 0.428!

Full challenge description from page:

> Leaderboard
> (7)
> Your Submissions
> Overview
> Operational sky reports are structured judgments, not single image labels. Several visual layers can coexist, neighboring categories can look similar, and qualified observers may disagree about coverage, height, or morphology. A useful system must know both when to correct a report and when the available panel does not support one unique correction.
> Each case supplies three chronological frames from a fixed outdoor camera and one anonymous observer's seven-field draft. Predict the minimal repair ledger that reconciles the draft with the withheld peer panel for the current frame.
> This is a temporal visual adjudication task. It is not ordinary cloud classification: correct draft fields must be left untouched, tied peer judgments require deferral, and all required changes must be emitted as one exact structured program.
> Adjudication Rule
> The seven anonymous report fields are:
> F0: dominant vertical family.
> F1: total sky-cover band.
> F2: lower-layer cover band.
> F3: lowest-base height band.
> F4: lower-layer morphology.
> F5: middle-layer morphology.
> F6: upper-layer morphology.
> For each case, the draft observer is removed from the panel and adjudication uses every remaining report. Peer reports are withheld from public inputs. Each field is adjudicated independently:
> If one peer value has a unique highest vote count and differs from the draft, replace the draft value with that peer value.
> If the unique highest peer value equals the draft, emit no repair for that field.
> If the highest peer vote count is tied, emit DEFER for that field.
> Every public case requiring prediction has at least two repair atoms.
> Input Format
> The three paths are chronological:
> frame_0_path: earliest context frame.
> frame_1_path: intermediate context frame.
> frame_2_path: current frame associated with the draft report.
> A draft report contains every field in fixed order. Example:
> F0=F0V03|F1=F1V07|F2=F2V02|F3=F3V05|F4=F4V08|F5=F5V03|F6=F6V00
> The value codes are intentionally anonymous operational categories. Their visual meaning and observer-specific use must be learned from the training examples. field_vocabulary.csv lists every valid field-value combination.
> Repair Ledger Grammar
> Each repair atom has the form FIELD:OLD_VALUE>NEW_VALUE. Multiple atoms are separated with | and must appear in increasing field order.
> Examples:
> Replace one value: F1:F1V07>F1V06
> Defer one field: F4:F4V08>DEFER
> Complete ledger: F1:F1V07>F1V06|F4:F4V08>DEFER
> Rules:
> A field may appear at most once.
> OLD_VALUE must equal the value shown for that field in the draft report.
> A replacement value must belong to the same field.
> NEW_VALUE cannot equal OLD_VALUE.
> Do not emit atoms for fields that already agree with a unique peer plurality.
> Do not add spaces, comments, confidence values, or extra delimiters.
> Dataset
> The public dataset contains:
> train.csv: 5,742 labeled observer-draft repair cases.
> test.csv: 1,261 unlabeled cases requiring repair ledgers.
> sample_submission.csv: 1,261 structurally valid example predictions, one per test case.
> field_vocabulary.csv: valid anonymous values for all seven report fields.
> images/: 2,152 anonymized 320 by 200 JPEG frames referenced by the CSV files.
> All cases using the same current image stay in one split. Entire capture days are disjoint between training and test, so random row validation is not reliable.
> train.csv Columns
> case_id (string): anonymous unique training-case identifier.
> observer_code (string): stable anonymous draft-observer identifier.
> frame_0_path (string): path to the earliest context image.
> frame_1_path (string): path to the intermediate context image.
> frame_2_path (string): path to the current image.
> draft_report (string): complete seven-field draft report.
> repair_ledger (string): target ordered repair program.
> test.csv Columns
> case_id (string): anonymous unique test-case identifier.
> observer_code (string): stable anonymous draft-observer identifier.
> frame_0_path (string): path to the earliest context image.
> frame_1_path (string): path to the intermediate context image.
> frame_2_path (string): path to the current image.
> draft_report (string): complete seven-field draft report.
> field_vocabulary.csv Columns
> field_code (string): one of F0 through F6.
> field_description (string): operational role of the field.
> value_code (string): valid anonymous value for the field.
> value_description (string): explanation of how value semantics are obtained.
> sample_submission.csv Columns
> case_id (string): test identifier copied from test.csv.
> repair_ledger (string): predicted ordered repair program.
> Evaluation
> The score is bounded in [0, 1], where higher is better:
> Score = 0.70 * FieldMacroRepairF1 + 0.30 * ExactRepairLedgerAccuracy
> The weights sum to 1.00, and each component appears exactly once.
> FieldMacroRepairF1
> For each of the seven fields, a predicted repair is a true positive only when its old value and new value, including DEFER, exactly match the target atom for the same case and field.
> A missing required atom is a false negative.
> An unnecessary atom is a false positive.
> A wrong replacement for a required field is both a false positive and a false negative.
> For one field, F1 = 2 * TP / (2 * TP + FP + FN).
> FieldMacroRepairF1 is the unweighted mean of the seven field F1 values.
> All seven fields are represented in the prepared test answers. If a mathematically empty field subset is encountered during platform partition scoring, its F1 is defined as 1.0 when both truth and prediction are empty.
> ExactRepairLedgerAccuracy
> This is the fraction of test cases for which the complete predicted atom set exactly equals the target atom set. Atom order is validated separately by the grammar.
> Malformed ledger rows receive zero credit and are not silently clipped, reordered, deduplicated, or repaired. Structural CSV violations such as missing required IDs, duplicate IDs, or extra columns raise an error.
> Submission
> Submit a CSV with exactly two columns. Example rows:
> Header: case_id,repair_ledger
> Row: CASETST_7a91c87d09e152,F1:F1V07>F1V06|F4:F4V08>DEFER
> Row: CASETST_e835ca01e32597,F0:F0V02>F0V03|F3:F3V05>F3V06
> Every required test case_id must appear exactly once. Additional rows outside the scored answer partition are ignored after required-ID and duplicate-ID validation.
> Allowed And Prohibited Methods
> Allowed
> Train CPU-compatible visual, temporal, multi-task, observer-calibration, or structured-decoding models using the supplied public files.
> Use ordinary image features, generally pretrained image representations, temporal differences, and observer-conditioned models.
> Construct image-grouped or capture-day-like local validation partitions using only public information.
> Use deterministic image augmentation derived only from the supplied public images.
> Prohibited
> Searching for or matching challenge images against the original source release or another external copy.
> Recovering embedded timestamps, source filenames, original observer identifiers, or external annotations.
> Hardcoding test ledgers, manually labeling test images, or constructing source-annotation lookup tables.
> Exploiting row order, case hashes, image paths, repeated current frames, or sample-submission values as prediction shortcuts.
> The intended solution must learn repair behavior from the supplied temporal images, the anonymous draft-observer profile, the draft report, and labeled training cases.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Consensus Gap: Predicting Where Land-Cover Maps Disagree

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c4jwe9mkz9p9q9nfgjvnpzs8bxqa4
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top score: 0.451

Full challenge description from page:

> Overview
> You are given a set of high-resolution four-band aerial image tiles. For each tile, three independent automated land-cover classification products have been computed and reduced to a common six-class legend (water, trees, grass/shrub, cropland, built, barren). Over a coarse 16x16 grid laid on the tile, a grid cell is labelled "in conflict" when the three products do NOT unanimously agree on the land-cover class of that cell, and "in consensus" when all three agree.
> Your task is to predict, from the aerial imagery ALONE, a 16x16 map of per-cell conflict scores: for each cell, how likely the three land-cover products are to disagree there. You never see the land-cover products or their classes — only the image. The land-cover class itself is never scored; only the binary agree/disagree map is.
> This is a dense, per-cell reliability-prediction task. Conflict concentrates where the scene is genuinely ambiguous (ecotones, mixed and transitional cover, fine-grained edges), so the signal is spatial and visual rather than a simple global property of the tile.
> Data
> All tiles are provided as NumPy arrays. Each tile is a 256x256x4 array of unsigned 8-bit integers with band order red, green, blue, near-infrared. A 16x16 label grid is laid over each tile; grid cells are indexed in row-major order (row 0 first, left to right), giving 256 cells numbered 0..255.
> The dataset contains 4,613 tiles in total: 3,296 training tiles (in train.csv, with labels) and 1,317 test tiles (in test.csv, labels withheld). Budget your from-scratch training accordingly.
> Files provided:
> train.csv — the training table. It has two columns:
> id: string, the tile identifier. The corresponding image is train/<id>.npy.
> labels: a string of 256 space-separated integers, row-major over the 16x16 grid. Each value is 1 (the three products disagree in that cell), 0 (they agree), or -1 (the cell is invalid / undefined and must be ignored during both training and evaluation).
> test.csv — the test table. It has one column:
> id: string, the tile identifier. The corresponding image is test/<id>.npy.
> sample_submission.csv — a valid submission in the exact required format (constant scores). It has two columns:
> id: string, matching every id in test.csv.
> scores: a string of 256 space-separated floating-point numbers in the range [0, 1], row-major over the 16x16 grid.
> train/ — a directory of training images, one file per training id, named <id>.npy. Each is a 256x256x4 uint8 array (R, G, B, NIR).
> test/ — a directory of test images, one file per test id, named <id>.npy. Each is a 256x256x4 uint8 array (R, G, B, NIR).
> Every training tile has at least one conflict cell and at least one consensus cell (the label grid is never all-0 or all-1 among valid cells). Invalid cells (label -1) occur only rarely and only in train.csv; they mark grid cells with undefined product coverage and should be excluded.
> Task and submission format
> For every id in test.csv, output a row with:
> id: the tile identifier (each test id exactly once).
> scores: 256 space-separated floats in [0, 1], row-major over the 16x16 grid, giving the predicted probability that each cell is in conflict.
> Write these rows to submission.csv with the header "id,scores". The submission must contain exactly the test id set (no missing ids, no duplicates), and every scores string must contain exactly 256 finite values in [0, 1]. Submissions violating these rules are rejected.
> Rules and constraints
> All model parameters must be initialized randomly and learned during your run from the provided train/ tiles and their train.csv labels. Do NOT use pretrained weights, pretrained backbones, foundation models, self-supervised or otherwise externally-trained checkpoints, or any form of transfer learning.
> No external data. Use only the provided tiles. Do not pull in outside imagery, land-cover maps, or other datasets, and do not attempt to geolocate or otherwise re-identify the tiles to look up their labels — the task is to predict from the imagery alone.
> Evaluation metric
> Predictions are scored by the normalized Average Precision (an AUPRC skill score), micro-averaged over all graded cells pooled across all test tiles. Let AUPRC be the area under the precision-recall curve computed over every graded (valid) cell of every test tile, treating "in conflict" as the positive class, and let p be the fraction of graded cells that are in conflict. The reported score is:
> normAP = (AUPRC - p) / (1 - p)
> An uninformative or constant submission achieves AUPRC = p and therefore normAP = 0. A perfect ranking achieves AUPRC = 1 and normAP = 1. Higher is better. The score is reported in [0, 1]. Because the metric is a ranking measure, only the relative ordering of your per-cell scores matters, not their absolute calibration.
> Notes
> The label is defined by disagreement among three independent products, so part of the signal is irreducible; a strong model captures where conflict is visually grounded without over-predicting on homogeneous scenes.
> Train and test tiles come from disjoint geographic regions, so memorizing location or local appearance will not transfer; the task rewards learning generalizable visual cues of land-cover ambiguity.
> Images have been radiometrically perturbed and reoriented; do not rely on absolute pixel values, orientation, or any metadata (none is provided).

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Satellite Proposal Headroom Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx764x4bkjrgtcccnzcfyt4qzx8c9x8e
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image, feature-engineering, multimodal, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.345

Full challenge description from page:

> Satellite Proposal Headroom Recovery
> Overview
> Satellite imagery is often processed by a fast detector that returns an approximate object box before a more precise downstream model is applied. In this challenge, each 384 by 384 image crop contains one target object together with a noisy proposal box. Your task is to refine that proposal into the human-verified target box.
> The challenge is linked to the Satellite Imagery Bounding Box Refinement Dataset. Its 9,636 crops come from 446 source images, with 4 to 160 crops per source. Crops from one source reuse scene content and object boundaries under different rotations, flips, crop contexts, brightness, contrast, and proposal severity, so a crop-level random split would place near-duplicates on both sides and inflate evaluation scores. The deterministic group split assigns every crop from a source image to one side only: 355 source groups and 7,708 rows for training, and 91 unseen source groups and 1,928 rows for evaluation. This makes the leaderboard measure transfer to new source scenes rather than memorization of related crops.
> Objective
> For every row in test.csv, predict the normalized target coordinates target_x1, target_y1, target_x2, and target_y2. Strong solutions can combine proposal geometry with visual evidence from the corresponding crop.
> The metric rewards only recovery of the proposal's remaining IoU headroom. Copying the supplied proposal is valid but scores zero, so useful predictions must read the image and improve the box.
> Dataset
> All solver-visible files are under ./dataset/public/. The preparation pipeline produces 7,708 training samples and 1,928 test samples using a deterministic source-image-group split.
> images/ contains the 384 by 384 WebP crops referenced by both CSV files.
> train.csv contains proposal coordinates and verified target coordinates.
> test.csv contains proposal coordinates but omits the four target columns.
> sample_submission.csv demonstrates the required output schema and copies each public proposal into the target columns as the frozen score-zero baseline.
> Fields
> sample_id is the opaque unique row identifier.
> image_file is the relative path to a crop under ./dataset/public/.
> proposal_x1, proposal_y1, proposal_x2, and proposal_y2 are the noisy normalized proposal coordinates.
> target_x1, target_y1, target_x2, and target_y2 are the verified normalized target coordinates and appear only in labeled data.
> Every coordinate is expressed relative to image width or height and must lie in the closed interval from 0 to 1. A valid XYXY box satisfies x1 < x2 and y1 < y2.
> Submission
> Write predictions to ./working/submission.csv as UTF-8 CSV with exactly 1,928 data rows and exactly these columns in this order: sample_id, target_x1, target_y1, target_x2, target_y2.
> Include every sample_id from test.csv exactly once, with no missing, duplicate, or extra identifiers.
> Use finite numeric coordinates in the interval from 0 to 1.
> Keep predicted target boxes well formed with strictly increasing horizontal and vertical bounds.
> Row order does not affect the score.
> Evaluation
> Let M be the unweighted mean IoU between submitted predictions and hidden targets. The frozen proposal-copy submission has mean IoU B = 0.45090616651819165. When M >= B, the score is (M - B) / (1 - B). When M < B, the score is (M - B) / B.
> Copying every proposal scores 0, a mean IoU halfway from B to 1 scores 0.5, perfect predictions score 1, a mean IoU of B / 2 scores -0.5, and zero mean IoU scores -1. Scores range from -1 to 1 and higher is better.
> Mean IoU directly measures box quality. Normalizing it around the proposal-copy baseline makes 0 mean no improvement, positive values measure the fraction of remaining aggregate IoU headroom recovered, and negative values measure the fraction of baseline IoU lost. The transform is strictly increasing, so it preserves the full mean-IoU ranking rather than collapsing degraded predictions into a tie.
> A prediction that can be aligned to its row but has non-finite, out-of-range, or reversed target coordinates contributes zero IoU. A malformed schema or invalid identifier set fails closed to a score of -1.
> Rules
> Train only on files under ./dataset/public/.
> Do not access ./dataset/private/, recover source identities, or build hardcoded identifier lookup tables.
> Do not use external datasets, external APIs, network calls, or remote inference. Pretrained weights already installed in the challenge environment are allowed, but a run may not download models or checkpoints.
> Use libraries already available in the configured Kaggle Python environment and complete the pipeline within the configured runtime.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Elapsed Time Between Two Storm Satellite Frames

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7drb60x8vc5s3j9vpd5j1zvx8bqrqp
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.643

Full challenge description from page:

> Elapsed Time Between Two Storm Satellite Frames
> Overview
> Each row holds two thermal infrared views of the same storm, taken some minutes apart. Predict how
> many minutes apart they are.
> Weather satellites deliver frames on a fixed schedule, and methods that follow storms lean on that:
> find the convective cells, then link them between frames known to be five minutes apart. Here the
> schedule is what is missing. You are not asked what is in the picture — you are asked how far the
> atmosphere has moved on between two pictures, which is a question about the rate at which
> convection reorganises itself.
> No timestamp, location or storm identifier is published. The two frames are all you get.
> The task
> For every row in test.npz, predict minutes: the elapsed time between frame_a and frame_b.
> The answer is always one of six values — 5, 10, 15, 20, 30 or 40 — and each is close to one
> sixth of the rows, so there is no majority interval worth defaulting to.
> Both frames come from a single storm and are contrast-normalised together over that storm's own
> brightness range. Absolute brightness therefore carries no information about the interval; only the
> relation between the two frames does.
> Why it is difficult
> The elapsed time is not the amount of change. The natural guess is that fields decorrelate as
> time passes, so a bigger difference means a longer gap. Pairs were deliberately selected to break
> that: binning mean absolute frame difference predicts the interval at 0.166 against a 0.167 floor.
> Any method resting on how much changed scores at chance by construction. See How the pairs were
> selected.
> Storms evolve at different rates. A vigorous cell reorganises in ten minutes; a decaying anvil
> drifts for forty with little structural change. The same interval looks different across storms,
> and the same appearance can mean different intervals in different storms.
> The intervals are unevenly spaced. They run 5, 10, 15, 20, 30, 40, so the step between
> neighbouring answers widens along the ladder — the top of the ladder is coarser than the bottom.
> Test pairs come from unseen storms. The split is by source storm, so nothing about a particular
> storm's appearance can be memorised and reused.
> Files
> train.npz — imagery for the 6,271 labelled pairs, holding three aligned arrays.
> ids — string array of shape (6271,), one opaque identifier per pair.
> frame_a — uint8 array of shape (6271, 96, 96), the earlier view. Brightness 0 to 255,
> row-major from the top-left.
> frame_b — uint8 array of shape (6271, 96, 96), the later view of the same storm, identically
> encoded.
> train.csv — the answers for those rows. 6,271 rows, in the same order as the arrays in
> train.npz.
> id — string, matches ids in train.npz.
> minutes — integer, one of 5, 10, 15, 20, 30, 40. The elapsed interval between the two frames.
> test.npz — the same three arrays for the 2,975 evaluated pairs, frames of shape
> (2975, 96, 96). It carries no target array.
> sample_submission.csv — 2,975 rows, columns id and minutes, answering the most common
> training interval for every row. It is structurally valid and scores below a uniform random guess,
> which is the point: with six near-equal intervals there is nothing to be gained by predicting one
> value everywhere.
> metadata.json — frame shape and dtype, the array names, the interval ladder and the split sizes.
> It contains no source name, storm identifier, place or timestamp.
> Loading:
> import numpy as np, pandas as pd
> tr = np.load("train.npz")
> a, b = tr["frame_a"], tr["frame_b"]      # (6271, 96, 96) uint8 each
> y = pd.read_csv("train.csv")["minutes"]  # aligned row-for-row with the arrays
> How the pairs were selected
> Pairs were not sampled uniformly. Candidates were first sorted into fourteen bands by how much the
> two frames differ, and within every band an equal number of each of the six intervals was kept. The
> size of the difference between frame_a and frame_b is therefore statistically independent of the
> interval.
> What remains is in the manner of the change rather than its size. A field can change by a given
> amount in ten minutes by drifting bodily across the frame, or by the same amount in forty minutes by
> growing new cells while old ones collapse. Those two look alike by total pixel difference and differ
> in structure: whether the field moved or turned over, whether cold tops spread or fragmented,
> whether change is coherent across the scene or scattered through it.
> Split
> Train and test are disjoint by source storm. Of 1,658 storms, 530 contribute only to the test side,
> so no storm appears on both. Each of the six intervals is close to one sixth of each side.
> Evaluation
> Score = 0.75 × ExactRate + 0.25 × NearRate
> ExactRate is the fraction of test pairs whose interval is named exactly.
> NearRate is the fraction landing exactly one step away on the ladder [5, 10, 15, 20, 30, 40].
> Adjacency is by position on that ladder, not by minutes: 30 is one step from both 20 and 40. Errors
> of two steps or more earn nothing.
> The partial credit is deliberate — calling twenty minutes fifteen is a near miss and calling it
> forty is not, and a metric scoring both as zero would be blind to the difference.
> Worked example: on 100 rows, 40 exact and 35 adjacent gives
> 0.75 × 0.40 + 0.25 × 0.35 = 0.3875.
> The score runs from 0 to 1 and higher is better. Guessing uniformly scores about 0.198; answering a
> single constant interval scores about 0.157. Roughly 0.20 is the price of saying nothing, so read a
> submission against that rather than against zero.
> Submission format
> A CSV with exactly two columns in this order: id, minutes. Include every test id exactly once.
> id,minutes
> cd_3f9a21c0b7e412,15
> cd_08bd5e1a44c9f3,5
> cd_c71e90aa2d6b85,40
> minutes must be a whole number drawn from 5, 10, 15, 20, 30, 40. Missing, extra or duplicate ids,
> unknown ids, reordered or additional columns, non-numeric or non-integer values, and values off the
> ladder are all rejected rather than scored low.
> Method rules
> This challenge is sized for CPU. The frames are small and the intended route — reading image
> structure out of the two views and mapping it onto the interval ladder — trains in minutes on an
> ordinary processor. No GPU is required at any point.
> Train only on the supplied files.
> Not allowed:
> External satellite archives or storm catalogues, or any attempt to identify the source events or
> their timestamps.
> Pretrained vision weights of any kind.
> Keying predictions to row identifiers, row order or file position rather than to the frames.
> Notes
> The split holds out entire storms: no storm in the test rows appears in the training rows. Build
> your validation split the same way — hold out whole storms, not random rows — or you will
> overestimate your score, because pairs drawn from one storm share its appearance and its rate of
> evolution.
> frame_b is always the later view; the ordering is never reversed. A pair is therefore directional,
> and features that are symmetric in the two frames discard whatever the direction of change carries.
> Published frames are dithered by one brightness level, so pixel values are not exact copies of any
> archived imagery. The dither is far below the scale of any real structure and can be ignored.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Dense Visual-Plantar Temporal Registration

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70cmxk11a2jemh7dy27t8vw98c44tt
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image, video, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 73.648

Full challenge description from page:

> Dense Visual-Plantar Temporal Registration
> Overview
> Develop a CPU-only computer-vision system that restores temporal correspondence between two synchronized physiological observation streams after their timestamps have been removed.
> Each example is a single grayscale registration board constructed from a 2.40-second walking interval. The upper half contains 12 chronologically ordered, appearance-suppressed video-motion tiles sampled uniformly through the reference interval. The lower half contains 12 chronologically ordered bilateral plantar-pressure tiles from the same physical event, but their original timestamps are absent, their temporal spacing is irregular, and intermediate pressure observations may be missing.
> Your task is to predict the temporal position of every plantar tile inside the video interval. The output is a strictly increasing sequence of 12 normalized values:
> alignment_path[i] = temporal position of plantar tile i in the video interval
> A value of 0.0 denotes the beginning of the video interval and 1.0 denotes its end. The task is therefore not action classification, gait-event classification, object detection, pressure reconstruction, or forecasting. It is a dense cross-modal registration problem in which correspondence must be inferred from motion phase, bilateral support, pressure redistribution, and the progression of the walking sequence.
> This models a practical multimodal-data repair workflow. Clinical and wearable recordings can lose reliable timing metadata because of clock resets, packet loss, export errors, or incomplete archive manifests. Manual realignment is costly and may be ambiguous when a recording contains repeated gait cycles. A reliable content-based registration system can support synchronization quality control, recovery of legacy recordings, and preparation of multimodal data for downstream biomechanical analysis.
> The two panels originate from independently measured modalities observing the same real walking event. The correspondence target is derived from the acquisition timeline; it is not generated from a pose estimator, a simulator, a rendered gait template, an encoded filename, or an image-processing artifact.
> Entire participant groups are held out for final evaluation. Performance therefore measures temporal registration for previously unseen people rather than memorization of participant appearance, footwear, neighboring windows, or recording-specific signatures.
> The complete solution must run on CPU and finish within 1.5 hours, including training, validation, inference, and submission generation. The runtime environment provides approximately 62 GB of RAM.
> Most visual gait tasks predict an activity label, event time, pose, or biomechanical quantity from video. PhaseBridge instead exposes both modalities and asks the model to recover their missing correspondence structure.
> A single global offset is insufficient. The plantar sequence has an unknown temporal extent within the video interval, and missing intermediate observations create non-uniform gaps between adjacent plantar tiles. The solver must consequently estimate a 12-knot monotone path rather than choose one class or regress one synchronization scalar.
> The challenge combines five design elements:
> Cross-modal timestamp recovery: supervision is the physical correspondence between camera motion and plantar sensing, not a creator-defined visual class.
> Dense monotone output: every plantar observation must be localized, including observations surrounding missing packets.
> Time-as-space representation: two temporal streams are encoded as aligned image panels while retaining independent temporal grids.
> Physiological-anchor evaluation: support transitions receive dedicated weight because they are operationally important synchronization landmarks.
> Participant-transfer testing: all rows from a person remain in one split, preventing identity-based shortcut learning.
> A method designed for kinematics-to-force regression cannot be transferred directly: no joint coordinates, body model, marker trajectories, calibrated camera geometry, or force target is supplied. Conversely, a conventional static-image regressor must discover the ordered tile structure before it can solve the registration problem.
> Dataset
> dataset/public/
> ├── images/
> │   ├── phase_<opaque_id>.jpg
> │   └── ...
> ├── train.csv
> ├── test.csv
> └── sample_submission.csv
> Registration boards
> Every board is a 512 × 576 grayscale JPEG divided into two 512 × 288 panels.
> ┌────────────────────────────────────────────┐
> │ 12 video-motion tiles: uniform video time │
> ├────────────────────────────────────────────┤
> │ 12 plantar tiles: unknown irregular time  │
> └────────────────────────────────────────────┘
> Both panels use a 4 × 3 row-major grid:
> t00  t01  t02  t03
> t04  t05  t06  t07
> t08  t09  t10  t11
> Each tile is 128 × 96 pixels.
> Upper panel: video-motion sequence
> The 12 upper tiles are sampled uniformly through the 2.40-second reference interval. Pixel intensity emphasizes observed motion while attenuating static background and exact RGB appearance. A shared activity crop preserves coarse body translation and limb-motion progression across tiles. Mild geometric, intensity, blur, noise, and JPEG nuisance variation reduces reliance on source-video signatures without changing temporal order.
> The upper panel does not provide RGB frames, explicit silhouettes, 2D or 3D pose coordinates, joint trajectories, body measurements, cadence labels, gait-event annotations, or timestamps.
> Lower panel: plantar sequence
> The 12 lower tiles are chronological, but adjacent tiles are not guaranteed to be equally spaced in time. Their sequence may cover only a subinterval of the upper panel, and missing intermediate observations create larger temporal gaps at unknown positions.
> Each plantar tile contains:
> an 8 × 4 left-insole sensor lattice;
> an 8 × 4 right-insole sensor lattice, mirrored horizontally for a consistent bilateral view;
> one compact load bar beneath each lattice.
> Sensor-channel positions are fixed across all rows. Brighter cells indicate greater relative pressure, while longer bars indicate greater total load for the corresponding foot. The representation preserves bilateral support and regional pressure progression but includes no timestamp, sample index, cadence name, participant name, or recording name.
> The lower sequence is an observed input modality. The model is not asked to predict pressure values; it must determine where those observed pressure states belong in the visual timeline.
> train.csv
> id,group_id,board_path,alignment_path
> Columns:
> id: opaque row identifier, unique within train.csv;
> group_id: opaque participant group for grouped validation;
> board_path: image path relative to dataset/public/;
> alignment_path: compact JSON array containing 12 strictly increasing target values.
> group_id is provided exclusively for participant-grouped validation and must not be used as a predictive feature.
> test.csv
> id,group_id,board_path
> The columns have the same definitions as in train.csv, except that alignment_path is omitted. Training and test group_id sets are disjoint. Every test id must appear exactly once in the submission.
> sample_submission.csv
> id,alignment_path
> The sample contains the same evenly spaced valid path for every row. It demonstrates serialization and monotonicity only; it does not use the image content and is not intended to be competitive.
> Target representation
> For a board with lower-panel tiles p00 through p11, the target is:
> alignment_path = [u00, u01, ..., u11]
> where:
> 0.0 <= u00 < u01 < ... < u11 <= 1.0
> ui is the normalized time of plantar tile pi within the upper-panel video interval. The upper video tile centers occur at:
> (j + 0.5) / 12,  for j = 0, ..., 11
> The target values are continuous. A plantar tile may lie between two video-tile centers, and several adjacent plantar tiles may map to the same coarse video cell while remaining strictly ordered in continuous time.
> Submission format
> Write predictions to:
> working/submission.csv
> The CSV must contain exactly these columns in this order:
> id,alignment_path
> alignment_path must be a JSON array containing exactly 12 finite numeric values. Every value must lie in [0, 1], and the values must be strictly increasing. The evaluator rejects malformed, non-finite, out-of-range, or non-monotone paths rather than repairing or clipping them.
> Example:
> id,alignment_path
> phase_71f0a41bdc9e6c4d107aa1,"[0.083,0.141,0.206,0.271,0.335,0.462,0.528,0.594,0.661,0.727,0.861,0.923]"
> phase_71f0a41bdc9e6c4d107bb2,"[0.083,0.141,0.206,0.271,0.335,0.462,0.528,0.594,0.661,0.727,0.861,0.923]"
> Rows may appear in any order. Do not include confidence intervals, explanations, alternate paths, timestamps in seconds, or additional columns.
> Evaluation
> The score measures absolute localization, synchronization of physiological transitions, recovery of missing-sample gaps, interval endpoints, and coarse visual-cell correspondence.
> For one row, let:
> t = true alignment path
> p = predicted alignment path
> Both contain 12 values.
> 1. All-knot localization
> point_mae = mean_i |p_i - t_i|
> L = max(0, 1 - point_mae / 0.090)
> This component measures the average continuous-time registration error.
> 2. Physiological-anchor localization
> Each plantar tile has an underlying bilateral support state: no contact, left-only contact, right-only contact, or double support. A foot is considered in contact when its normalized total load is at least 0.08. An anchor is a tile index i from 1 through 11 at which the support state differs from tile i - 1. Every evaluated row contains at least two such anchors.
> Let H be the anchor-index set:
> anchor_mae = mean_{i in H} |p_i - t_i|
> A = max(0, 1 - anchor_mae / 0.055)
> This stricter component emphasizes heel-contact, unloading, and bilateral-support transitions that are particularly useful for synchronization repair.
> 3. Inter-observation gap fidelity
> gap_mae = mean_i |(p_{i+1} - p_i) - (t_{i+1} - t_i)|
> G = max(0, 1 - gap_mae / 0.045)
> This component rewards correct localization of missing intermediate observations rather than only the overall offset.
> 4. Recovered temporal span
> start = max(0, 1 - |p_0 - t_0| / 0.080)
> end   = max(0, 1 - |p_11 - t_11| / 0.080)
> S = sqrt(start × end)
> Both ends of the pressure subinterval must be recovered.
> 5. Coarse video-cell agreement
> Define:
> cell(x) = min(11, floor(12 × x))
> V = mean_i [cell(p_i) == cell(t_i)]
> This measures whether each plantar observation is assigned to the correct coarse part of the visual sequence.
> Row and final score
> The five components are combined by a soft geometric conjunction:
> g(x) = 0.01 + 0.99 × x
> M = g(L)^0.30 × g(A)^0.25 × g(G)^0.20 × g(S)^0.15 × g(V)^0.10
> Q = (M - 0.01) / 0.99
> If L = 0, A = 0, or S = 0, then Q = 0. A path that misses the overall interval or its physiological anchors is not considered a usable synchronization repair.
> Row qualities are first averaged within each group_id. The final score is the unweighted mean of participant-group scores:
> score = 100 × mean_group(mean_row(Q))
> Temporal-order ablation
> For a sequence-aware model, apply one fixed permutation to all 12 lower-panel tile positions during training and validation while leaving the target unchanged. The fixed permutation preserves marginal image statistics but destroys chronological plantar progression. A substantial degradation relative to correctly ordered tiles indicates that the model uses temporal and physiological sequence structure rather than only path priors or total image intensity.
> Cross-modal ablations
> Two additional diagnostics are recommended:
> train with the upper panel masked to measure how much can be inferred from the plantar timing prior alone;
> train with the lower panel masked to measure how much can be inferred from video appearance and target priors alone.
> A strong solution should materially outperform both single-panel ablations.
> Not allowed
> External APIs or hosted inference services.
> External plantar-pressure, gait-synchronization, gait-kinetics, or synchronized gait-label datasets.
> Manual annotation or manual tuning of individual test rows.
> Identifying, matching, or retrieving source participants or source recordings outside the released public files.
> Using id, group_id, file names, row order, JPEG serialization details, or nuisance-transform artifacts as predictive features.
> Hard-coding predictions by test identifier or participant group.
> Reverse-engineering preprocessing randomness or hidden sampling rules instead of modeling visible cross-modal correspondence.
> Any test-time measurement unavailable in the released public files.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## PixelGrid: Compositional Visual Outlier Reasoning

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ay8fq8f0wt9e0rqewbgfrpd8bmfwa
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image, generative, multimodal, small-data, feature-engineering, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.575

Full challenge description from page:

> Overview
>
> Each 64×64 pixel-art scene contains four sprites arranged in a 2×2 grid. Three sprites form a coherent hidden semantic set; one sprite is the outlier. Your model must make two predictions:
>
> The grid location of the outlier.  
> Whether the three inlier sprites share the same fine-grained class or only a broader parent class.  
>
> This is a multi-output compositional visual-reasoning challenge. The source collection contains independent sprites; the prepared benchmark contains newly generated scenes and scene-level targets. It therefore requires set comparison, outlier localization, and relationship-depth inference rather than direct single-image classification.
>
> The hidden test is a zero-shot parent-class transfer split: none of the latent parent groups or fine classes used to assemble hidden test scenes occurs in public training scenes. Parent and fine-class names are never provided. A solution must therefore learn transferable visual relationship reasoning rather than memorizing observed semantic groups.
>
> Dataset
> File Structure
>
> Plaintext
>
> public/
> ├── train/                         # 16,000 labelled 64×64 RGB PNG scenes
> ├── test/                          # 3,200 unlabelled 64×64 RGB PNG scenes
> ├── train.csv
> ├── test.csv
> └── sample_submission.csv
>
>
> The four sprites in a scene are assembled from disjoint source-image partitions. The parent groups and fine classes used for hidden test scenes are also absent from public training scenes. Captions, source labels, hashes, original IDs, palettes, and other source metadata are not present in public data.
>
> train.csv Columns
>
> Plaintext
>
> +---------------------+--------+----------------------------------------------------------------------------------+
> | Column              | Type   | Description                                                                      |
> +---------------------+--------+----------------------------------------------------------------------------------+
> | scene_id            | string | Opaque per-scene identifier, for example scene_000001; it carries no source or    |
> |                     |        | target information.                                                              |
> | filename            | string | PNG filename under public/train/, for example scene_000001.png.                  |
> | outlier_cell        | string | One of top-left, top-right, bottom-left, or bottom-right.                        |
> | inlier_relationship | string | Either same-fine-class or same-parent-class.                                     |
> +---------------------+--------+----------------------------------------------------------------------------------+
>
> test.csv Columns
>
> Plaintext
>
> +----------+--------+-----------------------------------------------------------+
> | Column   | Type   | Description                                               |
> +----------+--------+-----------------------------------------------------------+
> | scene_id | string | Opaque test-scene identifier copied into the submission.  |
> | filename | string | PNG filename under public/test/.                          |
> +----------+--------+-----------------------------------------------------------+
>
>
> test.csv deliberately omits both targets.
>
> Submission
>
> Submit exactly one row per scene_id in test.csv. Rows may be reordered, but scene IDs must be unique and match the test set exactly.
>
> Submission Columns
>
> Plaintext
>
> +---------------------+--------+---------------------------------------------------+
> | Column              | Type   | Description                                       |
> +---------------------+--------+---------------------------------------------------+
> | scene_id            | string | Identifier copied from test.csv.                  |
> | outlier_cell        | string | Predicted outlier location.                       |
> | inlier_relationship | string | Predicted relationship shared by the three        |
> |                     |        | inliers.                                          |
> +---------------------+--------+---------------------------------------------------+
>
> Example of a valid file:
>
> Code snippet
>
> scene_id,outlier_cell,inlier_relationship
> scene_000001,bottom-right,same-fine-class
> scene_000002,top-left,same-parent-class
> scene_000003,top-right,same-fine-class
>
> Evaluation
>
> The score is maximized and ranges from 0 to 1:
>
> Plaintext
>
> 0.70 × macro-F1(outlier_cell) + 0.30 × macro-F1(inlier_relationship)
>
> Score range: 0.0 to 1.0  
> Direction: maximize  
> Macro-F1 gives equal importance to all target values.  
> The hidden test set is balanced across every outlier-cell and relationship combination.  
> Unknown target strings are counted as incorrect; missing, duplicate, or unexpected scene_id values make the submission invalid.
>
>  
>
> Submissions
> 5
> Top Score
> 0.575
> Created
> Aug 2, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> 3/12
> solvers beat AI
> How closing works
>
> 2 more distinct solvers needed to activate the $650 prize pool and start the closing countdown. At 12, up to 12 solvers will be selected to continue.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Non-Line-of-Sight Ultrasound Scan Planning and Echo Interpretation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78bbtvp7peapr75r2g67dst98bpgfk
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image, text, multimodal, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: —

Full challenge description from page:

> Overview
>
> Predict three outputs from one ultrasound-style evidence sheet: scan_plan, the three probe locations that should be measured; depth_partition, a coarse 4 x 4 hidden-depth ranking; and acquisition_order, the selected probes ordered from earliest useful echo return to latest.
>
> The setting is non-line-of-sight inspection. A flat relay surface, such as a wall, divider, or inspection plate, is visible to the sensor, while the object or cavity behind it is not directly visible. Each candidate probe location sends an ultrasound pulse into the relay surface. The returned time-of-flight profile gives partial evidence about hidden structure behind that region. Because each probe costs time and power, the task is to choose a small, nonredundant measurement plan and also interpret the depth pattern already visible in the echoes.
>
> The hidden objects are synthetic echo-scattering structures sampled from real non-line-of-sight scan cubes. They vary in shape, depth, return strength, and local redundancy. The image is not a medical diagnosis task. It is an acquisition-planning and echo-interpretation task: infer which visible probe locations best reveal hidden geometry, estimate the coarse hidden-depth layout, and order the selected measurements by return timing.
>
> The scan-plan component is evaluated by reconstruction utility, not only by equality to one reference set. A different three-probe set can receive partial credit when it captures strong, nonredundant echo evidence.
>
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `public/train.csv` | Labeled training evidence sheets. |
> | `public/test.csv` | Evaluation inputs without targets. |
> | `public/sample_submission.csv` | Schema-valid baseline predictions. |
> | `public/images/` | Prepared `1160 x 720` RGB JPEG echo-budget sheets referenced by the CSV files. |
>
>
> Full measurement files are assigned to only one split. Hidden cases include held-out object geometry and held-out acquisition settings. Prepared images and IDs do not expose source filenames, distances, dates, or split roles.
>
> The prepared release has 1,050 labeled training sheets and 420 hidden test sheets. Training contains all 56 possible three-label plan combinations, 805 distinct depth partitions, and 321 distinct acquisition sequences. The test source cubes are disjoint from the training source cubes.
>
> CSV Columns
>
> public/train.csv contains case_id, echo_budget_sheet_path, scan_plan, depth_partition, and acquisition_order.
>
> public/test.csv contains case_id and echo_budget_sheet_path.
>
> public/sample_submission.csv contains case_id, scan_plan, depth_partition, and acquisition_order.
>
> Evidence Sheet Layout
>
> Each image has two kinds of visual evidence:
>
> The large left panel is a relay-surface return-delay map. Brighter regions have stronger echo energy. Color progresses from early return to late return according to the legend at the bottom of the panel.
> The left panel is divided into a visible 4 x 4 grid. The submitted depth_partition predicts a delay-rank code for each of these 16 grid cells.
> Eight circular probe markers labeled A through H are drawn on the relay map. These are the only valid probe labels.
> The right side contains eight small time-of-flight trace panels, one for each candidate label. The horizontal axis runs from early return on the left to late return on the right.
> The bottom-right caption states that profile panels are read left to right from early to late return.
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | String | Opaque identifier matching `eb[0-9a-f]{20}`. |
> | `echo_budget_sheet_path` | String | Relative path such as `images/eb0123456789abcdefabcd.jpg`. The path points to the evidence sheet for that case. |
>
> Target Columns
> | Column | Data type | Description |
> |---|---|---|
> | `scan_plan` | String set | Three distinct probe labels from `A` through `H`, separated by `|`. Order is ignored, so `A|D|G` and `G|A|D` represent the same plan. |
> | `depth_partition` | JSON integer matrix | Exactly four rows by four columns. Entries are integers `0`, `1`, `2`, or `3`, where lower values mean earlier echo-delay regions within the case. |
> | `acquisition_order` | String sequence | Three distinct probe labels separated by `>`. The sequence gives the selected probes ordered from earliest informative return to latest informative return. |
>
> Depth Codes
>
> The spatial map is divided into four equal rows and four equal columns. For each region, the reference computes the energy-weighted time centroid of its mean echo profile. The 16 centroid delays are ranked within the case. The earliest four receive code 0, the next four code 1, the next four code 2, and the latest four code 3. This case-relative ranking prevents a shared relay-wall return from collapsing all regions into one absolute bin.
>
> | Code | Time-of-flight range |
> |---|---|
> | `0` | Four regions with the earliest energy-centroid delays. |
> | `1` | Four regions with the next-earliest delays. |
> | `2` | Four regions with the next-latest delays. |
> | `3` | Four regions with the latest delays. |
>
> Scan Utility
>
> Each candidate has a private gain value from 0 through 1. Candidate pairs also have a private redundancy value from 0 through 1 based on echo-profile similarity. These values are not given as columns, but they are derived from the same displayed spatial-return map and profile traces that participants see.
>
> For a three-candidate set P, raw_utility(P) = sum(candidate_gain for candidates in P) - 0.22 * sum(pair_redundancy for the three pairs in P).
>
> The gain and redundancy values are generated from the same displayed echo evidence. Training rows provide the optimal plan but not the private utility table.
>
> Submission Format
>
> Write the final file to ./working/submission.csv. Use exactly case_id, scan_plan, depth_partition, and acquisition_order, in that order.
>
> | case_id | scan_plan | depth_partition | acquisition_order |
> |---|---|---|---|
> | `eb0123456789abcdefabcd` | `A|D|G` | `[[0,0,1,1],[0,1,1,2],[1,2,2,3],[2,2,3,3]]` | `D>A>G` |
>
>
> Rules:
>
> Submit one row for every test ID.
> Extra, missing, or reordered columns are rejected.
> Duplicate, missing, malformed, or unknown IDs are rejected.
> A single backend-managed visibility column is tolerated and ignored.
> scan_plan is limited to 20 characters and must contain three distinct valid labels.
> depth_partition is limited to 160 characters and parsed only as bounded JSON.
> acquisition_order is limited to 20 characters and must contain three distinct valid labels.
> Malformed components receive zero component credit.
> Evaluation
>
> The metric is the Echo Budget Utility Score: Score = 0.46 * PlanUtilityScore + 0.32 * DepthPartitionScore + 0.22 * AcquisitionOrderScore.
>
> Minimum score: 0.0. Maximum score: 1.0. Higher is better.
>
> PlanUtilityScore
>
> The grader evaluates raw_utility for all 56 possible three-candidate plans. Let u_min and u_max be the minimum and maximum utility for the current case, and let u_pred be the submitted plan utility.
>
> normalized_utility = 1 when u_max = u_min; otherwise, normalized_utility = (u_pred - u_min) / (u_max - u_min).
>
> canonical_optimum is 1 when the submitted plan equals the hidden canonical optimum and 0 otherwise. The row score is row_plan_score = 0.30 * normalized_utility + 0.70 * canonical_optimum.
>
> The hidden optimum is selected by maximum utility with lexicographic label order breaking an exact tie. The utility term rewards a valid near-optimal plan, while the exact term requires that canonical optimum.
>
> DepthPartitionScore
>
> entry_accuracy = correctly predicted grid entries / 16. exact_matrix is 1 when all 16 entries match and 0 otherwise. The row score is row_depth_score = 0.25 * entry_accuracy + 0.75 * exact_matrix.
>
> AcquisitionOrderScore
>
> Let d be token-level Levenshtein distance between the three true and three submitted labels. Insertion, deletion, and substitution each cost one.
>
> edit_similarity = 1 - d / 3. exact_order is 1 when all three labels match in order and 0 otherwise. The row score is row_order_score = 0.22 * edit_similarity + 0.78 * exact_order.
>
> The three row scores are averaged over hidden cases and combined with the stated weights.
>
> Reference Validation
>
> The packaged reference answers score 1.0. The schema-valid sample submission scores 0.102180, and a frequent-target training baseline scores 0.114872. All 1,470 prepared sheet hashes are unique, with no train-to-test hash overlap. Two clean preparations produced byte-identical public and private trees. The grader rejects duplicate IDs, unknown IDs, missing rows, extra columns, reordered columns, oversized JSON, and malformed target values.
>
> Expected And Allowed Methods
>
> Suitable approaches can read the fixed sheet layout with ordinary image and signal-processing operations. The relay map can be summarized with grid-cell color statistics, energy centroids, gradients, connected regions, and delay-color histograms. The eight trace panels can be converted into one-dimensional profiles using fixed panel coordinates, followed by peak timing, width, area, decay, and pairwise similarity features.
>
> These descriptors can feed regularized linear models, compact multilayer perceptrons, random forests, histogram gradient boosting, or ranking models. Only 56 three-probe plans exist, so every valid plan can be scored directly using predicted gain and redundancy terms. The 4 x 4 depth matrix and three-token acquisition order can be decoded with small independent or jointly calibrated models.
>
> Pretrained feature extractors, signal processing, geometric features, and locally trained models are allowed. Hosted inference services are not allowed.
>
> What Not To Use
> Do not use case_id, filenames, row order, file size, hashes, or archive ordering as prediction features.
> Do not reverse-search displayed panels to recover original measurement filenames or published figure identities.
> Do not match evidence sheets against external copies of the source scans or maintain a source lookup table.
> Do not use private gain vectors, redundancy matrices, answer files, or hidden acquisition metadata.
> Do not submit extra columns, duplicate IDs, oversized JSON, non-finite numbers, or malformed values intended to exploit grader behavior.
> Do not fit or tune model parameters on hidden test rows.
> What Makes This Interesting
>
> The best individual echo is not necessarily part of the best three-probe plan. Two strong candidates may be nearly redundant, while a weaker candidate can add a distinct time-of-flight view and improve the set. The utility scorer therefore rewards information complementarity. At the same time, the depth map and acquisition order require spatial and temporal interpretation of the same packet.
>
>  
>
> Submissions
> 0
> Top Score
> —
> Created
> Aug 2, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> 0/12
> solvers beat AI
> How closing works
>
> Be the first to solve this challenge! 5 distinct solvers with graded solutions are needed to activate the $650 prize pool and start a closing countdown. At 12, up to 12 solvers will be selected to continue.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Visual Column Provenance Arbitration

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70ad1d264y80sse227jgz8gs8bmbcz
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: —

Full challenge description from page:

> Overview
>
> Each example contains one image and four mixed-up relationship cards. A relationship card should say which subject is connected to which object and by what relationship, such as “person holds paddle.” The subject and its box are already in the correct card, but the four relationship words and the four object label-box pairs have been shuffled separately.
>
> Your task is to put both shuffled parts back into the correct cards:
>
> For each card, choose which of the four displayed relationship words belongs to its subject.
> For each card, choose which of the four displayed object label-box pairs belongs to its subject.
> Use every relationship-word source and every object source exactly once.
>
> You submit two lists of source-card numbers, one for relationship words and one for objects. The grader follows those lists to rebuild all four cards. A correct answer therefore restores the complete set of relationships in the image; it does not invent new labels or boxes.
>
> This represents a column-mixing failure in a visual-record database. The source relationships come from Open Images. Preparation selects four difficult relationships with distinct subject and object instances, at least two predicate labels, and at least two object labels. It shuffles the predicate and object columns independently and keeps all examples from the same source image in one split. External image lookup is prohibited.
>
> Dataset
> train.csv: 280 labeled incidents.
> test.csv: 107 hidden-label incidents.
> sample_submission.csv: 107 schema-valid identity mappings.
> train_images/: 280 episode JPEGs referenced by training data.
> test_images/: 107 episode JPEGs referenced by test data.
>
> Every incident contains exactly four cards. In each card, the subject label and subject box are fixed in the correct position. Source images are disjoint between splits.
>
> Fields:
>
> scene_id: opaque string and submission identity.
> image_path: path relative to the public dataset directory.
> shuffled_ledger: JSON array of four cards numbered 0 through 3. Every card contains subject, subject_box, predicate, object, and object_box. Boxes are four normalized floats in [xmin,ymin,xmax,ymax] order. The subject fields are already correct. The predicate and object fields have been copied from other cards.
> reconciliation_plan: training-only answer object. It contains two lists: predicate_from and object_from. Each list contains the numbers 0, 1, 2, and 3 exactly once.
>
> For reconstructed card i:
>
> predicate_from[i] gives the card whose displayed predicate must be copied into card i.
> object_from[i] gives the card whose displayed object label and object box must be copied into card i.
>
> For example, predicate_from[0] = 2 means that reconstructed card 0 uses the predicate currently displayed in shuffled card 2. Requiring each list to use 0, 1, 2, and 3 exactly once makes it a one-to-one mapping (a permutation).
>
> Evaluation
>
> Submissions are evaluated with the Executed Provenance Reconciliation Score (EPRS). The grader validates both submitted source lists, uses them to rebuild the four cards, and compares those rebuilt cards with the hidden correct cards by scene_id. CSV row order has no effect.
>
> For card i, card_exact_i is 1 only if the executed subject label and box, predicate, object label, and object box all exactly match the clean card. Otherwise it is 0. Define incident_exact as 1 only if all four cards are exact.
>
> For one incident:
>
> incident_score = 0.10 × mean(card_exact_0, card_exact_1, card_exact_2, card_exact_3) + 0.90 × incident_exact
>
> EPRS is the arithmetic mean of incident_score across all 107 test incidents, clipped to [0,1]. Higher is better; a completely correct submission scores 1.0. The card term gives limited partial credit, while most credit requires restoring all four cards. A plausible-looking relationship receives no credit unless the submitted mappings actually rebuild the correct card.
>
> The grader rejects invalid JSON, duplicate JSON keys, missing or extra plan fields, non-integer entries, non-bijective arrays, missing/extra/duplicate/foreign scene IDs, extra submission columns, null predictions, and oversized cells.
>
> Submission Format
>
> Submit exactly two columns:
>
> scene_id: copied from test.csv, with every ID exactly once.
> predicted_reconciliation: JSON object containing exactly predicate_from and object_from; both must be permutations of [0,1,2,3].
>
> Example:
>
> scene_id,predicted_reconciliation
>
> case_example,"{""predicate_from"":[2,0,3,1],""object_from"":[1,3,0,2]}"
>
> Distinction From Neighbouring Benchmarks
>
> Open Images VRD and scene-graph generation predict relation triplets or scored edges from pixels. Here, the vocabulary, boxes, and complete multiset of fields are already supplied; generating another triplet is not a valid answer. The learned output is the provenance of two independently detached database columns, represented as coupled scene-wide bijections and evaluated only after transactional execution.
>
> Generic CSP and shuffled-role benchmarks begin from symbolic clues and score a satisfying assignment. Here, the constraints alone are insufficient because every permutation satisfies the public grammar. Solvers must estimate compatibility from the released labels, box geometry, image regions, and training relationships before applying the one-to-one decoder. The benchmark combines visual-record compatibility, provenance arbitration, and executable state restoration rather than attaching a CSP decoder to standard SGG outputs.
>
> Requirements
> Train only on released training scenes and labels.
> Use image pixels, localized boxes, and global one-to-one decoding.
> Train a CPU model that combines labels, box geometry, and one-to-one decoding.
> Finish within 90 minutes using the configured CPU environment and write working/submission.csv reproducibly.
> What Not To Use
>
> Do not access raw/private files, identify source images, retrieve external annotations, use hosted APIs, manually label test images, use GPU computation, or fit representations on the complete test set.
>
>  
>
> Submissions
> 0
> Top Score
> —
> Created
> Aug 1, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> 0/12
> solvers beat AI
> How closing works
>
> Be the first to solve this challenge! 5 distinct solvers with graded solutions are needed to activate the $650 prize pool and start a closing countdown. At 12, up to 12 solvers will be selected to continue.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Crowd Fracture — Predicting Where Human Perception Breaks Down

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bp47pzy5w1eq0tvd9hkv8pd8c3k8p
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top score: —

Full challenge description from page:

> Overview
>
> A large volunteer crowd was asked to annotate a corpus of wildlife camera-trap photographs. Each capture event is a burst of three photographs fired by a single passive-infrared motion trigger, so the three frames are seconds apart and show the same scene. Every event was shown independently to many volunteers, and each was asked three separate questions about it:
>
> which species is present,
> how many individuals there are,
> what the animals are doing — a set of behaviour checkboxes.
>
> Volunteers did not always agree. Crucially, they did not disagree about the same thing every time. On one event the crowd is unanimous that it is a zebra but splits badly on whether there are four of them or seven. On another everyone agrees there are exactly two animals but half the crowd calls them Thomson's gazelles and half calls them Grant's. On a third the species and the count are obvious and the argument is entirely about whether the animal is standing or moving.
>
> Your task is to predict which of the three questions the crowd will fracture on.
>
> Not how much they disagreed — which aspect of the scene defeated them. The output is a single label per event: identity, number, or activity.
>
> You are not asked what animal is in the photograph, how many there are, or what it is doing. None of those are graded, and none of them appear in any file you are given. The species is never revealed anywhere in this dataset.
>
> Why this is hard
>
> The three failure modes have genuinely different visual causes, and they are not ranked by how "bad" the image is:
>
> identity fractures on distance, silhouette, motion blur, an animal facing away, or a species that has a close look-alike in the same habitat;
> number fractures on occlusion, overlapping bodies, a herd receding into the distance, or animals partly out of frame — often on images where the species is perfectly obvious;
> activity fractures on ambiguous posture, an animal caught mid-stride, or a scene where the three burst frames disagree with each other about whether anything moved.
>
> A model that only learns "this is a hard image" will do poorly, because every event in this dataset fractured on something. The label is comparative: it identifies which aspect fractured most, relative to how often that aspect is contested at all. Each aspect's crowd-disagreement measure is converted to its rank within the training distribution of that same aspect, and the label is whichever ranks highest. So a small amount of behaviour disagreement can outrank a large amount of count disagreement, because behaviour disagreement is rarer.
>
> For every event exactly 15 volunteer annotations were used, taken in the order they arrived. This is deliberate: how many volunteers happened to see an event is an artefact of platform scheduling and has nothing to do with the image, so fixing the number at 15 makes the label invariant to it.
>
> Every event in this dataset contains at least one animal. Events the crowd retired as empty were removed, so "is the image empty?" is not the task and will not help you.
>
> Files
>
> The dataset consists of four files and two image folders.
>
> train.csv — one row per training capture event. Columns:
>
> event_id — string. Opaque unique identifier for the capture event. Also the filename stem of its three frames.
> station_id — string. Opaque identifier of the camera station that took the event. Many events share a station. Use this for grouped cross-validation — the test set comes from camera stations that appear nowhere in train.csv, so a random row split will read optimistically.
> fracture_axis — integer in {0, 1, 2}. The target. 0 = identity, 1 = number, 2 = activity. This column appears only in train.csv.
>
> test.csv — one row per test capture event. Columns:
>
> event_id — string. Opaque unique identifier for the capture event. Also the filename stem of its three frames.
> station_id — string. Opaque identifier of the camera station that took the event, in the same format as train.csv. Every station id appearing here appears in no training row — the two splits are station-disjoint — so these are new tokens that tell you only which test events came from the same camera. Row order is shuffled.
>
> sample_submission.csv — a valid, fully populated submission in the exact required format. Columns:
>
> event_id — string. Every event id in test.csv, exactly once.
> fracture_axis — integer in {0, 1, 2}.
>
> It predicts the training-set modal class for every row. It is well formed and it scores approximately zero, because a constant prediction has a kappa of zero by construction.
>
> label_scheme.json — describes the label. Keys:
>
> n_classes — integer, always 3.
> classes — list of three strings, ["identity", "number", "activity"], in the order matching integer codes 0, 1, 2.
> aspect_base_rates — object mapping each class name to its frequency in the training split.
> rule — string describing how the label is derived.
>
> train/ — image folder. For every event_id in train.csv it contains exactly three JPEG files: <event_id>_0.jpg, <event_id>_1.jpg, <event_id>_2.jpg. Each is a 192×128 RGB JPEG. Index 0, 1, 2 is chronological order within the burst.
>
> test/ — image folder, identical structure, for every event_id in test.csv.
>
> All images are 192 pixels wide and 128 pixels high, three-channel RGB, JPEG. All metadata has been stripped: there is no EXIF, no timestamp, no camera identifier, no location, and the burned-in information strip that the cameras print along the bottom edge of each photograph has been cropped away before downscaling.
>
> Submission format
>
> Write a CSV named submission.csv with a header row and exactly these two columns, in this order:
>
> event_id,fracture_axis
>
> It must contain exactly one row for every event_id in test.csv, with no duplicates and no missing ids. Every fracture_axis value must be an integer in {0, 1, 2}. Missing values, NaN, non-numeric values, and values outside that range are rejected rather than scored.
>
> Evaluation
>
> The score is Cohen's kappa between your predicted class and the true class, pooled over all test rows, with negative values clamped to zero:
>
> S = max(0, kappa(fracture_axis))
>
> Kappa compares your accuracy against the accuracy expected by chance given your own prediction marginals. Two consequences worth planning around:
>
> Any constant submission scores 0, so predicting the largest class everywhere earns nothing, no matter how large that class is.
> The classes are nominal, not ordered. There is no partial credit for being "close" — predicting number when the answer is activity is exactly as wrong as predicting identity. Decoding by an argmax over class probabilities is the natural choice; a posterior-mean or ordinal decode is meaningless here.
>
> S lies in [0, 1] and is maximised.
>
> Notes and constraints
> The test set comes from camera stations that never appear in training, so backgrounds, vegetation, camera placement and lighting all shift between train and test. Validate with a station-disjoint split, not a random one. The class balance also shifts between the two splits; a model that hard-codes the training prior will be miscalibrated.
> The three burst frames are the input, not one photograph. The activity class in particular depends on what changed between frames.
> The solution must be a learned model that reads the images. Producing the graded column by any hand-written rule, threshold, or lookup is not a valid solution.
>
>  
>
> Submissions
> 0
> Top Score
> —
> Created
> Aug 8, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> 0/12
> solvers beat AI
> How closing works
>
> Be the first to solve this challenge! 5 distinct solvers with graded solutions are needed to activate the $650 prize pool and start a closing countdown. At 12, up to 12 solvers will be selected to continue.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Ordering Storm Cells by When They First Produced Lightning

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74qxxyrnjw9p49wfeb4kbez98bms4c
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat reze's score of 0.277!

Full challenge description from page:

> Ordering Storm Cells by When They First Produced Lightning Overview Three regions of one thunderstorm all began producing lightning within about twenty minutes of each other. You are shown what their cloud tops looked like afterwards. Put them in the order they ignited. Satellite models of lightning run forwards: they read the imagery and estimate where flashes are happening or about to happen. This runs the other way. Nothing here asks whether a region is electrically active — all three are, and you are told so. The question is which one got there first, which is a question about how far each cell has progressed through its life cycle, read off a cloud top that has been developing since. The lightning record itself is never published, for any moment. The task Each row gives three regions of a single storm, labelled a, b and c, and a short sequence of imagery covering the thirty minutes ending at the snapshot time. Output, for each region, its position in the ignition order: 0 for the one that ignited first, 1 for the second, 2 for the last. Every row's three answers are a permutation of 0, 1, 2 — there are no ties. The three regions are published in a random order, so the label a, b or c carries no information about the answer. Why it is difficult The cells are at similar stages. Rows were built only from triples whose ignitions fall inside a twenty-minute window, with consecutive ignitions at least three minutes apart. Cells that ignited an hour apart look obviously different; cells that ignited eight minutes apart do not. The ordering is genuinely subtle rather than artificially hidden. The obvious maturity rule does not work here. Ranking the regions by how cold their cloud top has become is the natural approach, and on these rows it is right exactly as often as chance, in either direction. It is not a weak strategy; it is worth nothing at all. The evidence is comparative, not absolute. No single region's appearance means anything on its own, because storms differ enormously in how cold and how large they run. What matters is how each region compares with the other two in the same row. A method that scores each region in isolation and sorts the scores gives up most of the available signal — measured, that loses about 40% of the achievable score. Test storms are unseen. The split holds out whole storms, so nothing about a particular storm's appearance transfers. Files train.npz — imagery for the 2,753 labelled rows, holding two arrays. ids — string array of shape (2753,), one opaque identifier per row. cube — uint8 array of shape (2753, 3, 2, 3, 24, 24). The axes are row × region × channel × frame × height × width. axis 1, region: 0 is region a, 1 is b, 2 is c. axis 2, channel: 0 is thermal window brightness, 1 is water-vapour brightness. axis 3, frame: 30 minutes before the snapshot, 15 minutes before, and the snapshot. axes 4 and 5: a 24 × 24 crop, roughly 8 km per pixel, row-major from the top-left. Brightness is contrast-normalised per storm across both channels, so absolute values carry no information — only differences within a row do. train.csv — the answers, 2,753 rows, in the same order as train.npz. id — string, matches ids in train.npz. rank_a, rank_b, rank_c — integers. The position of each region in the ignition order, 0 first. Each row is a permutation of 0, 1, 2. storm_group — string. An opaque key shared by every row taken from the same storm. It is there so you can hold whole storms out of your own validation split. It names no storm and carries no time or place, and it is not released for the evaluated rows. test.npz — the same two arrays for the 1,279 evaluated rows, cube of shape (1279, 3, 2, 3, 24, 24). No answers. sample_submission.csv — 1,279 rows with the four required columns, ordering the regions by how rough their final thermal view looks. It is structurally valid and scores about 0.05, barely above a random ordering, which is the point. metadata.json — cube axes and dtype, channel meanings, frame offsets, and split sizes. It contains no storm identifier, place or timestamp. Loading: import numpy as np, pandas as pd tr = np.load("train.npz") cube = tr["cube"] # (2753, 3, 2, 3, 24, 24) uint8 y = pd.read_csv("train.csv") # aligned row-for-row with the cube region_b_watervapour_last = cube[:, 1, 1, -1] # (2753, 24, 24) What a row shows Each row is three regions of a single storm, equal tiles of that storm's field of view, together with a short sequence of imagery covering the thirty minutes ending at the snapshot. All three regions were already producing lightning before the snapshot was taken. Nothing is being forecast: the ordering you are asked for lies in the past relative to the imagery you see, and the question is what the cloud tops still show of it. Consecutive ignitions are separated by at least a few minutes, so no two regions ignited at the same moment and every row has one well-defined order. Split Train and test are disjoint by source storm. Of 632 storms, 202 contribute only to the test side. All six possible orderings occur with close to equal frequency, so there is no ordering worth guessing by default. Evaluation Score = max(0, 2 × (PairAccuracy − 0.5)) PairAccuracy is the fraction of region pairs placed in the correct relative order, averaged over rows. Three regions give three pairs per row: (a, b), (a, c) and (b, c). Pairs rather than exact permutations, because getting two of the three comparisons right is real skill and a metric that only rewarded a perfect ordering would discard it. Ordering at random gives a PairAccuracy of 0.5, so the rescaling puts a guess at 0 and a perfect answer at 1. The score is clipped at 0, so an ordering worse than chance scores 0 rather than going negative. Worked example: on 100 rows you get all three pairs right on 40 rows and two of three on the rest. PairAccuracy is 0.40 × 1 + 0.60 × (2/3) = 0.80, and the score is 2 × (0.80 − 0.5) = 0.60. Submission format A CSV with exactly four columns in this order: id, rank_a, rank_b, rank_c. Include every test id exactly once. id,rank_a,rank_b,rank_c ig_4c1f7a9e02b3d5,1,0,2 ig_9b20e5cc71a884,0,2,1 ig_37de6110af95c2,2,1,0 Each row's three ranks must be a permutation of 0, 1 and 2. Missing, extra, duplicate or unknown ids, reordered or additional columns, non-integer values, values outside 0 to 2, and rows with ties or repeats are all rejected rather than scored low. Method rules This challenge is sized for CPU. The crops are small — a row is 3 × 2 × 3 × 24 × 24 bytes — and the intended route, comparative features across the three regions followed by an ordinary learner, trains in minutes on an ordinary processor. No GPU is required at any point. Train only on the supplied files. Not allowed: External lightning archives, satellite archives or storm catalogues, or any attempt to identify the source storms or their timestamps. Pretrained vision weights of any kind. Keying predictions to row identifiers, row order or file position rather than to the imagery. Notes The split holds out entire storms. Build your validation split the same way — hold out whole storms, not random rows — or you will overestimate your score, since several rows can come from one storm. Group on storm_group in train.csv to do it: most storms there contribute more than one row, so a random row split would put rows from the same storm on both sides. Treat a row as a comparison, not as three independent predictions. Centring each region's features against the row's own mean, or feeding all three regions to the model together, is worth a large fraction of the achievable score. Frames are dithered by one brightness level, far below the scale of any real structure. Ignore it. &nbsp;
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Wound-Front Reconstruction And Optical Self-Calibration

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73ck791vsewe16thjxqt6a7n8dsjwm
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Wound-Front Reconstruction And Optical Self-Calibration Overview A scratch-wound assay is the standard bench method for measuring how fast cells migrate. A confluent monolayer is scratched, the same well is imaged over a day or two, and the cell-free gap is quantified as it closes. Almost every published number from such an assay depends on two things being right: where the migration front is, and how many microns a pixel is worth. This challenge asks you to recover both, from a single microscopy field, with no metadata at all. You are given 1936 × 365 phase-contrast fields cut from wound-healing acquisitions spanning 0 to 44 hours after the scratch, imaged at two objective powers. For each evaluation field you predict: rle — the open (cell-free) wound mask, run-length encoded; and gap_width — the mean gap width in scale-normalised units. No frame carries a scale bar. No timepoint, objective power, or treatment label is given for any evaluation field. Both answers have to come from the pixels. The scoring deliberately does not reward getting the wound roughly right. A scratch wound is one big region, so Dice saturates: a random forest that misses the front by ten pixels still scores Dice 0.939, and the published SAM segmentation of this archive scores 0.982. Those two are not remotely equally good at the thing the assay measures. The score is therefore built on Boundary IoU, which looks only at the rim of the mask — the migration front — and separates them cleanly: 0.052 against 0.202. Goal Reconstruct the expert-annotated migration front to within a few pixels, and report a physically comparable gap width, for 60 held-out fields. The two halves are one problem. gap_width is defined as gap_width = wound_area_fraction × 1936 / magnification so a correct width needs a correct mask and the objective power that produced the frame. Over the training fields, raw wound area correlates 0.400 with magnification and averages 2.21× larger at 10× than at 5×; the scale-normalised width correlates only 0.069 and averages 42.94 against 47.45. The normalisation is what makes wounds imaged at different objective powers comparable at all — and recovering it means reading optical scale out of cell morphology, because nothing else in the frame reveals it. Why This Challenge Is Interesting The residual against the expert is systematic, not noise. The archive ships three SAM prompt variants of the same automatic segmentation. Measured on the evaluation fields, those variants agree with each other at 0.728 mean Boundary IoU, but agree with the expert front at only 0.202. An automatic method can therefore be reproducible to within a pixel or two — what it is missing is not randomness but a consistent difference in where a human draws the front. Simply dilating SAM by one pixel already recovers part of it (0.202 → 0.222). The rest is learnable, and learning it is the challenge. Saturated metrics hide exactly this. Under Dice, the gap between a crude classifier and a state-of-the-art segmenter is 0.939 versus 0.982 — four points, easily mistaken for noise. Under the front metric used here it is 0.052 versus 0.202, nearly fourfold. The challenge is built on the measurement that actually distinguishes methods. Optical self-calibration is a real, unglamorous problem. Multi-site and archival microscopy routinely loses acquisition metadata, and a wound width in pixels is meaningless without it. The only cue left is the apparent size and texture of the cells themselves. A straightforward texture-and-spectrum classifier recovers the objective power on only 77% of held-out fields, so this half is genuinely uncertain rather than a free lookup. Nothing here is memorisable. Copying the nearest training field's mask and width scores 0.0000. So does every fixed band, every column-threshold heuristic, the mean training mask, and the single most typical training mask. Dataset Microscopic Wound Healing Image Dataset, Katja Löwenstein (Kaggle: katjalwenstein), accompanying Löwenstein, Rehrl, Schuster & Gadermayr, "Virtually Objective Quantification of in vitro Wound Healing Scratch Assays with the Segment Anything Model", arXiv:2407.02187 (2024). The three sam_* mask sets are that work's automated segmentations. Licence. The upstream licence terms were not machine-readable at the time of writing and must be confirmed and recorded from the Kaggle dataset page before this challenge is published. If the licence does not permit redistribution, link to the source rather than mirror the images. Any publication using this challenge should cite both the dataset and the paper. The usable archive holds 29 acquisitions of 1936 × 1460 pixels: 12 at 5× and 17 at 10×, at 0, 16, 23, 24, 38 and 44 hours after the scratch. The evaluation unit is a field, not a well Each acquisition is cut into four stacked 1936 × 365 fields. This mirrors ordinary microscopy practice — several fields are imaged per well and each is quantified separately — and it yields 60 independently segmented migration fronts in the evaluation set rather than 15. Every target is field-specific. Sibling fields cut from the same well have different wound shapes, so they have different masks and different gap widths; no evaluation row's answer appears anywhere else in the table, and this is asserted at build time. It matters because the platform partitions the evaluation rows into public and private scoring slices without regard to which well a field came from. Per-well quantities such as the assay timepoint and the objective power are deliberately not submission columns for exactly that reason — they are identical across a well's four fields and would transfer straight from a public row to a private one. Magnification stays recoverable on training fields as area(mask) × 1936 / gap_width, so it can still be learned without ever being a graded, shareable answer. Splitting into training and evaluation is by acquisition, never by field, so no well is ever both trained on and evaluated. Verified: zero shared wells, zero shared images, zero shared masks. How the data were prepared Acquisitions are allocated to the evaluation set within each timepoint, in proportion to that timepoint's size, and each objective power appears in proportion to its share of the archive rather than being forced to an even split — so the scarcer power stays learnable from training rather than being drained into the evaluation slice. fields acquisitions 5x fields 10x fields train 51 14 17 34 evaluation 60 15 28 32 timepoints (fields) 0h 16h 23h 24h 38h 44h train 16 12 3 8 11 1 evaluation 16 16 4 12 8 4 wound area fraction min max train 0.0059 0.4933 evaluation 0.0106 0.4109 gap_width min max median train 2.01 95.49 42.26 evaluation 2.30 81.38 Both wound-area extremes are pinned to training, so the evaluation set interpolates rather than extrapolates. Identifiers are opaque and assigned after a seeded shuffle, so nothing about time, scale or area can be read from an image_id. Every image is re-encoded to PNG, because in the raw archive the container format (JPG versus PNG) correlated with wound area. Filenames in the source encoded the timepoint and objective power directly; none of that survives into the published data. Data File Structure public/ train.csv 51 rows image_id, image_path, rle, gap_width test.csv 60 rows image_id, image_path sample_submission.csv 60 rows image_id, rle, gap_width extra.csv 4 rows image_id, image_path images/train/*.png 51 fields, RGB PNG, 1936 x 365 images/test/*.png 60 fields images/extra/*.png 4 fields with no mask (ungraded) masks/expert/*.png 51 expert masks, 0/255, 255 = open wound masks/sam_1_1/*.png 51 published SAM masks (prompt variant 1_1) masks/sam_1_2/*.png 51 published SAM masks (prompt variant 1_2) masks/sam_2_1/*.png 51 published SAM masks (prompt variant 2_1) masks_without_image/ 12 annotations whose image is absent upstream README.md private/ answers.csv 60 rows image_id, rle, gap_width Masks are found by naming convention: the expert mask for training field wh_train_007 is masks/expert/wh_train_007.png, and likewise for each SAM variant. No mask of any kind is published for an evaluation field. train.csv and test.csv expose exactly the same feature columns — image_id and image_path. Training adds the two target columns and nothing else. Field dimensions are not columns because every field is 1936 × 365; a one-valued column carries no information. Examples A row of train.csv (RLE truncated for display): image_id,image_path,rle,gap_width wh_train_001,images/train/wh_train_001.png,313901 3 314266 6 314631 10 ...,25.1304 A row of test.csv: image_id,image_path wh_test_001,images/test/wh_test_001.png A row of extra.csv — four fields whose upstream acquisition has an image but no annotation. They are never graded; they are unlabelled imagery you may use for unsupervised work such as fitting a scale head: image_id,image_path wh_extra_001,images/extra/wh_extra_001.png Input Description Each field is an RGB PNG, 1936 pixels wide and 365 tall — one of four horizontal cuts of a full acquisition. The wound runs roughly vertically through the frame: a cell-free channel of lower texture energy, bounded left and right by advancing cell fronts. Early fields show a wide, clean gap; late fields show a narrow, ragged one that may be nearly closed. The image is all you get. There is no timepoint, no objective power, no well identifier, no treatment label, and no scale bar. Target Description rle — the open wound mask at 1936 × 365, run-length encoded: column-major (Fortran) flattening of the mask, 1-indexed positions, space-separated start length pairs, pairs sorted by start position and non-overlapping, an empty mask is the empty string. For a mask m, the encoding is flat = np.concatenate([[0], m.flatten(order="F").astype(np.uint8), [0]]) change = np.flatnonzero(flat[1:] != flat[:-1]) + 1 rle = " ".join(f"{s} {e - s}" for s, e in zip(change[0::2], change[1::2])) gap_width — the mean gap width in scale-normalised units, gap_width = wound_area_fraction × 1936 / magnification where wound_area_fraction is the fraction of the field's pixels that are open wound and magnification is the objective power (5 or 10). Values are clipped to [0, 400] before scoring; negative, missing or non-finite values are rejected. Submission Format A CSV with exactly these columns, one row per evaluation field, in any row order: image_id,rle,gap_width wh_test_001,255501 91250,50.0 wh_test_002,182501 51830,28.4 (Those two rows are the first lines of the shipped sample_submission.csv; its heuristic emits one contiguous band per field, hence a single start length pair. A real mask will have many pairs.) All 60 image_id values from test.csv must be present, with no duplicates. Extra columns and extra unknown rows are ignored. sample_submission.csv is a valid, complete, gradeable submission produced by a crude training-free heuristic — it scores 0.0000, which is the floor. Evaluation For each evaluation field, with pred your mask and true the expert mask: Front_i = mean over d in {2, 3, 5} of BoundaryIoU_d(pred_i, true_i) Region_i = Dice(pred_i, true_i) Segmentation = mean_i [ 0.15 * Region_i + 0.85 * Front_i ] Metrology = max(0, 1 - mean RelErr(gap_width) / (0.70 * mean RelErr(REFERENCE))) raw = 0.85 * Segmentation + 0.15 * Metrology Score = (raw - raw_reference) / (1 - raw_reference), clipped to [0, 1] REFERENCE is REFERENCE_GAP_WIDTH = 42.26, the median gap width over the training fields. raw_reference is the raw score of a fixed reference submission — a central band covering 20% of the width, plus a constant gap_width of 42.26 — scored against the same answers inside the grader. It is recomputed on every call rather than hard-coded, so the floor always tracks the data. Metrics Boundary IoU (Cheng, Girshick, Dollár, Kirillov & He, Boundary IoU: Improving Object-Centric Image Segmentation Evaluation, CVPR 2021) is the intersection-over-union computed only over the pixels within d of a mask's own boundary, measured inward. On a wound this large that restricts scoring to the migration front and discards the saturated interior. Three rim widths are averaged — 2, 3 and 5 pixels — so the score reflects front accuracy across a range of tolerances rather than one arbitrary cutoff. The rim is measured inward from each mask and the image border carries no rim. Where the wound simply runs out of the field of view, that cut is framing rather than a cell front, and no credit is given for it — which is why a full-height band earns almost nothing. Dice is the usual region overlap, kept at 0.15 weight as a sanity term so a mask with a good front but a wildly wrong body cannot win. Symmetric relative error for widths is |pred - true| / max(|pred|, |true|), capped at 1, so no single field can dominate the mean. Metrology as a skill score. Predicting the published constant 42.26 scores exactly 0. The reference is tightened to 0.70 of the constant predictor's error, so you must beat the no-knowledge answer by 30% before the term pays anything — the point is recovering the optical scale, and reproducing the training median is not evidence of having done so. What the Score Means Measured on the 60 evaluation fields (segmentation / metrology / score): empty masks + reference width ........ 0.000 / 0.000 / 0.0000 all-foreground + reference width ..... 0.045 / 0.000 / 0.0000 column-threshold heuristic ........... 0.106 / 0.000 / 0.0000 central band + reference width ....... 0.113 / 0.000 / 0.0000 <- the floor texture + RF masks, constant width ... 0.185 / 0.000 / 0.0677 texture + RF masks, learned scale .... 0.185 / 0.409 / 0.1356 texture + RF masks, oracle scale ..... 0.185 / 0.701 / 0.1839 published SAM masks, constant width .. 0.319 / 0.000 / 0.1937 published SAM masks, learned scale ... 0.319 / 0.538 / 0.2829 published SAM masks, oracle scale .... 0.319 / 0.919 / 0.3460 SAM front dilated 1px, oracle scale .. 0.336 / 0.915 / 0.3614 front within 4 px, oracle scale ...... 0.359 / 0.964 / 0.3912 front within 3 px, oracle scale ...... 0.425 / 0.974 / 0.4553 front within 2 px, oracle scale ...... 0.544 / 0.983 / 0.5685 front within 1 px, oracle scale ...... 0.806 / 0.993 / 0.8160 exact masks + oracle width ........... 1.000 / 1.000 / 1.0000 A competent classical CPU pipeline — texture features into a random forest, Dice 0.939 — scores 0.136. The published SAM segmentation, a GPU-scale model quoted as a reference ceiling rather than something a CPU solver reaches inside the budget, scores 0.346. Matching the expert front to within three pixels scores 0.455, within two pixels 0.569. A method as self-consistent as the SAM prompt variants are with each other would score about 0.78. Most of the range is unclaimed and the ladder between the rungs is smooth, so incremental work on the front converts into score at every level rather than only at the top. Metrology cannot carry a submission. A non-segmenting entry handed the exact gap widths still scores only 0.166, because the width term is worth 0.15 of the raw score. Conversely, exact masks with the reference width score 0.834 — the segmentation is where the challenge lives. Allowed Resources The provided training images, expert masks, and all three SAM mask sets. The SAM masks are the reference you are trying to beat; the systematic offset between them and the expert front is the most useful signal in the archive. extra.csv imagery and masks_without_image/, both ungraded, for unsupervised or auxiliary work. Any classical computer-vision or machine-learning method that runs on CPU: thresholding, texture and frequency features, active contours, level sets, random forests, gradient boosting, small convolutional networks trained from scratch, classical registration, morphological post-processing. Deriving quantities from the training labels — wound area, magnification via area(mask) × 1936 / gap_width, front position profiles, closure statistics. Reasoning across the four sibling fields of an evaluation acquisition if you can identify them. They share an objective power, so pooling a scale estimate across them is legitimate. It will not carry you far: the width term is capped at 0.166 of the total. What Not to Use No pretrained weights of any kind, including SAM itself, ImageNet backbones, or any foundation model. The published SAM masks are provided as data; the model is not available to you and reproducing it is not the exercise. No internet access at train or inference time. No external datasets or external annotations. No GPU. No manual annotation of evaluation fields, and no hand-tuning against the leaderboard beyond ordinary model selection. Do not attempt to recover the source archive or match evaluation fields to their originals. Do not submit per-well constants. Sibling fields have genuinely different masks and widths; a well-level answer is wrong for at least three of every four fields. Compute Constraints CPU only: roughly 10 cores, roughly 62 GB RAM. About 1.5 hours of wall clock for the whole solve. No internet, no GPU. For reference, the classical baseline above — twelve texture and gradient features at stride 4, a 120-tree random forest, Gaussian smoothing and largest-component selection — trains and predicts all 111 fields in about 100 seconds on two cores. Grading 60 fields takes 4 seconds. Important Notes Submit masks at exactly 1936 × 365. Runs outside the image, unsorted runs, overlapping runs, zero or negative lengths, and non-integer tokens are all rejected with an error naming the offending image_id. An empty RLE is accepted and means "fully closed". No evaluation field is fully closed, so an empty mask always scores zero on that field. gap_width must be present, finite and non-negative for every row. The grader requires only NumPy and pandas. SciPy is used for the exact Euclidean distance transform when present, with an exact NumPy implementation of the Felzenszwalb–Huttenlocher transform as a fallback; both paths produce bit-identical scores. Data preparation is fully deterministic — a fixed seed and sorted enumeration, with two independent runs verified byte-identical across all 337 files (103.8 MB). &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Projected Boundary Trace Cut Responses

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx776t280ga83rxk3krpjd9w3s8e0v4w
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat pvduy's score of 0.811!

Full challenge description from page:

> Background Mapping and understanding topological connectivity in complex, noisy image structures (such as projected filaments, vessels, or material traces) is a fundamental computer vision challenge. Rather than merely segmenting pixels, analytical systems must often reason about graph properties—specifically, how different boundary regions connect and how local blockages or dropouts impact the overall network integrity. Overview Given a 512×512 grayscale image, predict twelve numerical graph responses that map the connectivity between four fixed boundary regions ("ports"). The task evaluates how a projected trace network connects these ports, both before and after a central square is erased. This is a mathematical operation on a binary annotation graph derived from the visual traces. It does not infer individual filament ownership, biological transport, physical severing, or experimental intervention outcomes. Multi-pixel ports use the minimum path distance over any source and destination foreground pixel. Training and inference must be strictly self-contained within a 90-minute allowance on a CPU environment (at most 10 CPU cores and 62 GB RAM). Dataset Information (Public Files) The dataset comprises highly augmented grayscale image crops and their corresponding graph responses. +------------------------+-------------------------------------------------------------+ | File / Directory | Purpose | +------------------------+-------------------------------------------------------------+ | images/ | Directory of 512x512 grayscale JPEG images. | | train.csv | Labeled training rows containing the 12-element targets. | | test.csv | Unlabeled evaluation queries. | | sample_submission.csv | Format-example rows for test IDs. | | response_schema.json | Reference details regarding port coordinates and ordering. | +------------------------+-------------------------------------------------------------+ Train/evaluation split and leakage control: Before any crops or perturbations are generated, complete images are grouped by visual similarity: normalize each image using its 1st/99th intensity percentiles, resize to 64×64, center and normalize the intensity vector, then form connected components of pairs with correlation greater than 0.98. Sort deterministic opaque component hashes and hold out the first round(0.25 × number of components) whole groups for evaluation; the remaining groups form training. Every crop and both perturbation variants of an image stay in its group’s split. Exact pixel-identical images cannot cross the boundary. Thus evaluation tests unseen image groups, rather than alternate augmentations of training images. This conservative image-based grouping reduces repeated-background memorization; it does not establish independent acquisition sessions or eliminate every possible near-duplicate. See split_protocol.json for the same protocol and group counts. Feature Schema train.csv and test.csv +-----------+---------+----------------------------------------------------------------+ | Column | Type | Description | +-----------+---------+----------------------------------------------------------------+ | id | String | Opaque unique example identifier. | | image | String | Relative path to the 512x512 JPEG image. | | responses | JSON | (train only) Array of 12 graph response floats in [0, 1]. | +-----------+---------+----------------------------------------------------------------+ Geometry and Coordinate Definitions Pixel $x$ increases rightward and $y$ increases downward. Foreground crossings connect in projection; nearby unconnected pixels are never bridged. The four boundary ports (half-open rectangles) are defined as: Port 0 (Left): $x \in [0, 12), y \in [64, 448)$ Port 1 (Top): $x \in [64, 448), y \in [0, 12)$ Port 2 (Right): $x \in [500, 512), y \in [64, 448)$ Port 3 (Bottom): $x \in [64, 448), y \in [500, 512)$ The erasure region is a central square defined as: Central Cut: $x \in [192, 320), y \in [192, 320)$ Response Function and Ordering Foreground pixels form an eight-neighbor graph where horizontal/vertical edges have a length of $1$ and diagonal edges have a length of $\sqrt{2}$. For any pair of ports, if no path exists, the response is $0$. Otherwise, the response is calculated using the shortest path distance $d$: $$R = \frac{1}{1 + \frac{d}{512}}$$ The 12-element target vector is ordered as follows: Intact Responses (6 values): Port pairs (0,1), (0,2), (0,3), (1,2), (1,3), (2,3) computed on the unmodified graph. Erased Responses (6 values): The exact same port pairs computed after completely erasing all vertices within the central cut square. Constraint: Every erased response must be less than or equal to its intact counterpart. Evaluation Metrics The evaluation metric is the Nonnegative Global Variance-Weighted Multioutput R-Squared. It evaluates the total squared prediction error across all test examples and all twelve coordinates simultaneously (it is not an average of per-image or per-coordinate $R^2$ scores). Let $y$ be the true responses, $\hat{y}$ be the predicted responses, and $\bar{y}$ be the mean of the true responses across the test set for a given coordinate. $$\text{Error} = \sum_{i=1}^{N} \sum_{j=1}^{12} (y_{i,j} - \hat{y}_{i,j})^2$$ $$\text{Denominator} = \sum_{i=1}^{N} \sum_{j=1}^{12} (y_{i,j} - \bar{y}_j)^2$$ $$\text{Score} = \begin{cases} \max\left(0, 1 - \frac{\text{Error}}{\text{Denominator}}\right) & \text{if } \text{Denominator} > 0 1.0 & \text{if } \text{Denominator} = 0 \text{ and } \text{Error} = 0 0.0 & \text{otherwise} \end{cases}$$ Scores range from $0.0$ to $1.0$ (higher is better). A perfect prediction scores $1.0$. Sample Submission Format Submit a UTF-8 encoded CSV file containing exactly two columns in this order: id,responses. Include one row per test ID. id,responses 811abcd1234567890abcdef1,"[0.85, 0.0, 0.45, 0.0, 0.92, 0.0, 0.35, 0.0, 0.21, 0.0, 0.70, 0.0]" Parsing Bounds & Rejection: - The responses JSON array must contain exactly twelve finite numbers in the range $[0, 1]$. Booleans are invalid. - Monotonicity Constraint: Erased values must not exceed their corresponding intact values (plus a 1e-8 floating-point tolerance). - Missing/extra IDs, duplicated IDs, or JSON strings exceeding 4,096 characters will cause the entire file to score 0.0. Row order does not affect grading. What Not To Use To ensure fair evaluation of training efficiency and algorithmic design: No Source Exploitation: Do not access private native masks, source filenames, source lookup services, or hidden responses. No External Datasets: Task-specific supervision must use only the supplied public training data. No External Services: The solution must run fully offline. No internet access, web lookup, or hosted inference APIs are permitted. Hardware Limits: The submitted solution must execute within a CPU-only environment bounded by a 90-minute limit. Pretrained weights may be acquired and cached beforehand, but training/inference must complete strictly within the budget. &nbsp;
> All-solver grace
> Grace ends in 57m
> $700 Pool
> Lockdown

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Scrambled Sea Turtle Specis and Identity Classification

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dhab8w6h6m4nb064j3338ph8bnncc
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 6.923!

Full challenge description from page:

> Overview In this challenge, your task is to accurately predict both the specis and individual turtle identity from the limited tile-scrambled underwater sea turtle images. Each 256x256 pixel image in the dataset has been divided into 64x64 pixel tiles and randomly scrambled within the image frame. Your model must learn robust visual representations that generalise across scrambled tiles to identify individual sea turtles as well as their specis. &nbsp; Note: It is 'specis' and not 'species'. Dataset Description Directory Layout train.csv: Training metadata mapping processed images to their ground truth specis and turtle identities. test.csv: Test set image paths for prediction evaluation. images/train/: Directory containing scrambled training images. images/test/: Directory containing scrambled testing images. sample_submission.csv: Template for submission format. CSV Columns image path (String): Relative path to the image file (e.g., images/train/08a67e08cfbc.png). specis (String): Animal specis (e.g., Green, Hawksbill). turtle_name (String): Unique identifier for individual sea turtles. &nbsp; To resolve this validation error, add a Dataset & Train/Test Split section to your problem description to explicitly state how data leakage is prevented across individual turtle identities. Dataset & Train/Test Split To ensure robust evaluation and prevent target leakage or identity memorization: Identity-Based Group Split: The dataset is partitioned using a strict group split on individual turtle identities (turtle_name). No individual turtle present in the test evaluation set appears in the training dataset. Stratification by Specis: Splits are stratified across specis (specis) to ensure balanced distribution of taxonomic categories across train, validation, and test sets. Image Patch Disjointness: Multiple scrambled patches or multi-view captures derived from the same individual turtle are strictly grouped into the same split, preventing cross-leakage between training and evaluation splits. Submission Format Your submission file must be a CSV named submission.csv containing predictions for all rows in test.csv: image path,specis,turtle_name images/test/08a67e08cfbc.png,Green,turtle_a1b2c_3d4e images/test/08a67e08cfyu.png,Hawksbill,turtle_f5g6h_7i8j Evaluation Metric Submissions are scored using a weighted combination of accuracy across identity, specis, and joint predictions: &nbsp; $$Score = 3.5 \cdot \text{Acc}{\text{identity}} + 2.5 \cdot \text{Acc}{\text{specis}} + 4.0 \cdot \text{Acc}_{\text{joint}}$$ &nbsp; $\text{Acc}_{\text{identity}}$: Accuracy of predicted turtle_name ($\in [0.0, 1.0]$). $\text{Acc}_{\text{specis}}$: Accuracy of predicted specis ($\in [0.0, 1.0]$). $\text{Acc}_{\text{joint}}$: Accuracy where both turtle_name and specis are simultaneously correct ($\in [0.0, 1.0]$). Score Range & Scaling: Since the component weights sum to 10.0 (3.5 + 2.5 + 4.0 = 10.0), the raw output formula naturally evaluates to a score between 0.0 (minimum) and 10.0 (maximum). No additional scaling or re-normalization is applied. Grade Direction: Maximize Min Score: 0 Max Score: 10 Metric Justification Joint Accuracy (4.0 weight): Highest priority. Real-world conservation tracking requires exact predictions for both identity and specis together. Getting one right while failing the other renders the record unusable for field research. Identity Accuracy (3.5 weight): High difficulty. Differentiating individual sea turtles from scrambled image patches is a fine-grained recognition task that demands robust feature extraction. Specis Accuracy (2.5 weight): Baseline task. Specis classification relies on broader visual patterns and fewer class boundaries, making it less complex than individual identification. &nbsp; Summary: This weighting scheme forces models to learn fine-grained individual features while maintaining high-level taxonomy on scrambled imagery. Technical Restrictions & Guidelines Hardware & Runtime Limits Max Wall-Clock Time: 1 Hour (60 minutes) total wall-clock time for the complete end-to-end training and inference pipeline with no GPU setting. Strict Timeout: Runs exceeding the 60-minute wall-clock limit will automatically time out and fail grading. Strict Restrictions (WHAT NOT TO USE) Pre-Trained Weights Limitation: ONLY standard, general open-source ImageNet-pretrained weights (e.g., ImageNet-1k / ImageNet-22k checkpoints from standard libraries like timm or torchvision) are allowed. Pre-training on domain-specific datasets (e.g., wildlife, sea turtles, bio-metric re-ID, or self-supervised domain sets) is strictly prohibited. Model Parameter Limit: Total model size must be less than 10 Million parameters ($\le 10\text{M}$ parameters). NO Lookups or Direct Mappings: You must NOT use exact image hash lookups, file-size matching, metadata indexing, or deterministic mappings between test images and training identities/specis. Predictions must strictly come from model inference. NO Global Appearance / Feature Matching Heuristics: You must NOT use color histogram nearest-neighbors, global color/texture distribution matching, mean/variance image feature heuristics, or direct feature-matching algorithms to shortcut individual re-identification via encounter-level visual similarities. NO Image Retrieval / Nearest-Neighbor Feature Matching: You must NOT use $k$-nearest neighbors ($k$-NN), cosine similarity matching, vector database lookups, or embedding-based distance matching between test and training representations. Predictions must be directly generated by a classification head in a single forward pass, rather than via feature similarity retrieval. NO Handcrafted / Classical Feature Matching: You must NOT use handcrafted local visual descriptors (e.g., SIFT, SURF, ORB), direct pixel-wise distance metrics (e.g., MSE, SSIM, L1/L2 pixel distances), or statistical keypoint matching to establish correspondences between test and training images. NO Tile-Based / Jigsaw Approaches: You must NOT use explicit tile-matching algorithms, edge-matching heuristics, jigsaw solvers, or tile-position prediction tasks to reconstruct or infer spatial tile arrangements. NO Image Unscrambling / Tile Reshuffling: Reconstructing, reordering, or unscrambling the $64 \times 64$ tiles back into original images is strictly forbidden. Models must learn directly from the raw scrambled inputs. NO Ensembling / Model Stacking: Submissions must use a single model architecture for inference. Combining, averaging, or ensembling predictions across multiple separate model checkpoints or distinct network architectures is prohibited. NO External Data / Images: Downloading or introducing external sea turtle datasets or external image files is strictly prohibited. NO Test-Set Leakage or Transductive Learning: Test set images must only be used during final inference. Test-time augmentation (TTA), pseudo-labeling, transductive feature alignment, or cross-validation on test features is strictly prohibited. Recommended Methods (WHAT TO USE) Lightweight Vision Models: Custom CNNs or lightweight Vision Transformers/ConvNeXt-style networks ($\le 10\text{M}$ parameters) using standard open-source ImageNet initialization. Data Augmentation for Scrambled Features: Apply strong visual augmentations (e.g., Mixup, CutMix, Random Erasing, and Color Jitter) to prevent overfitting on local tile textures. &nbsp;
> 1 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.


# Non-CPU Computer Vision Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed Non-CPU examples in this document: 90

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.

## Foam Coarsening Next Event And Pressure Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75wkns9d7xdms2w7rm0bhab189ep3d
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Foams appear in beer heads, bread, tissue-like cell layers, metal grain growth, and lung air-sac mechanics, and their cells coarsen as pressure differences drive gas from smaller or poorly connected bubbles into larger neighbours. In this challenge, each example is a short top-down video of a wet foam rearranging over time, and your job is to recover the hidden coarsening state and answer a local wall-removal query from the visual dynamics.
> You are given public training videos with labels and public test videos without labels. Each video shows wet foam cells with rounded translucent bubble caps, bright liquid Plateau borders, moving films, and style variation in tint, lighting, and wetness. A public per-row roster, bubble_roster_json, maps each bubble id to its position in the first frame; use those ids - and no others - in your JSON outputs by locating each listed bubble in the clip and tracking it as the foam coarsens.
> What Not To Use: do not use filename lookup, row order, archive order, raw-data private columns, scene hashes, generated metadata outside the public CSVs, reverse-engineered seeds, video encoding artifacts, or hard-coded answer lists. Do not submit a generic captioning, object-counting, single-frame bubble-size heuristic, roster-position-only guess, or detector-only solution as a substitute for the requested temporal and causal predictions. Enforcement on invalid approaches: rule-only shortcuts or submissions that do not solve the intended visual foam-dynamics task may be rejected before payout.
> For each test row, predict four heads: the bubble id or ids most likely to vanish next after the clip ends, the set of currently visible bubbles that are shrinking during the observed clip, the queried bubbles ranked from highest to lowest internal pressure, and whether the named wall-removal merge would grow, shrink, or remain uncertain. Submit a calibrated confidence value in [0,1] for each row.
> Dataset
> The public folder contains train/test CSV files, sample submission, and videos under split-specific video folders.
> train.csv contains one row per public training clip with the public video fields and the four label columns. test.csv contains one row per public test clip with only the fields available at prediction time. sample_submission.csv is a valid placeholder template that gives the exact required submission schema.
> train.csv columns
> id is the anonymized row identifier. video is a relative path under the public folder. bubble_roster_json is a JSON object mapping each bubble id to its normalized [x, y] position (each in 0-1) in the first frame, so you can identify and track each bubble through the clip. query_bubbles_json lists the bubble ids to rank by pressure. query_wall_json names the two bubbles separated by the wall in the counterfactual query. prompt repeats the row-level task in plain text. next_vanish_json is the training answer list of bubble ids likely to vanish next. shrinking_set_json is the training answer list of visible bubbles that are shrinking. pressure_rank_json is the training answer list of queried bubbles ordered from highest to lowest pressure. cf_merge_outcome is one of grows, shrinks, or uncertain.
> test.csv columns
> id is the test row identifier that must appear in your submission. video points to the test MP4 clip. bubble_roster_json maps each bubble id to its normalized [x, y] position in the first frame so you can identify and track every bubble you must answer about. query_bubbles_json lists exactly the bubble ids that must appear in pressure_rank_json. query_wall_json names the queried wall as two bubble ids. prompt is the row task prompt.
> Submission
> Submit a CSV with exactly these columns in exactly this order.
> id must match a test row exactly once. next_vanish_json must be a JSON list of bubble-id strings for the next likely vanish or merge event. shrinking_set_json must be a JSON list of visible bubble-id strings that are shrinking in the observed clip. pressure_rank_json must be a JSON list containing each queried bubble id exactly once, ordered from highest to lowest pressure. cf_merge_outcome must be exactly grows, shrinks, or uncertain. confidence must be finite and within [0,1].
> Example submission rows:
> id,next_vanish_json,shrinking_set_json,pressure_rank_json,cf_merge_outcome,confidence
> 101,"[""B04""]","[""B04"",""B12""]","[""B04"",""B08"",""B01""]",shrinks,0.72
> 205,"[""B03"",""B19""]","[""B03"",""B11"",""B19""]","[""B19"",""B03"",""B07""]",uncertain,0.58
> Evaluation
> For each row, S_next is F1 over the predicted next-vanishing set, S_sign is mean per-visible-bubble shrink/grow membership accuracy, S_rank is Kendall order agreement rescaled to [0,1] over the queried pressure ranking, and S_cf is exact counterfactual bucket accuracy. The row correctness is 0.46*S_next^2 + 0.08*S_sign^2 + 0.18*S_rank^2 + 0.28*S_cf^2.
> The final score is a robustness-aware blend: 0.82*mean(row_correctness) + 0.06*worst_split_group + 0.05*worst_ood_axis + 0.05*worst_render_style + 0.02*mean(calibration), where calibration is 1 - (confidence - row_correctness)^2 clipped to [0,1]. Higher is better. The theoretical minimum is 0.0 and the theoretical maximum is 1.0.
> Submissions with structural errors are invalid and the grader raises InvalidSubmissionError: missing, extra, or reordered columns; duplicate ids; missing or extra rows; non-integer ids; or invalid confidence values. Row-level content errors such as malformed or overlong JSON, unknown bubble ids, repeated ids inside a JSON list, wrong pressure-ranking item sets, or invalid counterfactual buckets score 0.0 for that row while the rest of the submission is still evaluated.

Inspiration note: Useful because it uses visual evidence for structured state or risk prediction, not just ordinary image classification.

## Dispatch State Vectors From Roadside Incident Clips

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ejgpry5tqqwkey8tkrxfeed896hap
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> You are given short source-neutral fixed-view roadside incident clips. Your task is to convert each test clip into a dispatch state vector: what active incident family is visible, which coarse road zone is affected, whether vulnerable road users are involved, how severe the public risk is, what response priority should be assigned, and how confident the model is.
> The benchmark-specific object is the structured state vector, not a caption, detector output, or source-native class lookup. The same clip must be interpreted as an operational decision: event family, fixed active-event phase, affected zone, vulnerable-user evidence, risk level, dispatch priority, and calibrated confidence. For example, a vehicle fire and a pothole may both affect a lane, but they imply different public risk and response priority; a physical altercation or armed snatching event may involve vulnerable users even when the road surface is intact.
> This is not a generic abnormal-versus-normal benchmark, not a traffic-anomaly captioning task, and not a one-column incident classifier. Use the public training clips and labels to learn visual evidence for the supported incident families and dispatch outputs. The public files use opaque clip IDs and prepared video paths only. They do not expose source filenames, source class folders, raw timestamps, original frame counts, source row order, or source metadata.
> What Not To Do (using these approaches can cause solution rejection regardless of score):
> Do not use external source-corpus lookup, source-page search, video fingerprinting, source filename matching, or frame-level reverse search to recover hidden labels.
> Do not infer labels from clip_id, video_path, row order, file size, file modification time, duration, frame rate, or any platform artifact outside the public files.
> Do not reduce the task to binary anomaly detection, generic incident/crime classification, detector-only pothole spotting, traffic-video captioning, or a single hazard-type classifier while ignoring risk, vulnerable-user, zone, priority, and calibration heads.
> Do not submit unsupported hazard labels such as wrong-way driving, missing traffic signals, illegal crossing, motorcycle wrong-lane behavior, or obstruction types that are not in the allowed schema.
> Do not submit missing rows, duplicate IDs, extra columns, reordered columns, invalid categorical values, non-finite confidence, or confidence outside [0, 1].
> Internet And External Resources
> Use the provided public challenge files as the only source of clip-specific evidence. Do not query search engines, source dataset pages, online video indexes, reverse-image or reverse-video services, map/street-view services, social-media video search, external road-hazard video corpora, or hosted APIs to identify test clips, recover source filenames, reconstruct source folders, or look up labels for these rows.
> Generic modeling resources are allowed when they are not used for answer lookup: open-source vision/video frameworks, public pretrained image or video backbones, local augmentation recipes, and offline training or fine-tuning on the released public training examples. Hosted commercial inference APIs, web-scraped clip matching, and external labeled datasets specific to these hazard videos are not allowed.
> Evaluation
> Each row is scored across six categorical heads and one confidence value. Allowed categorical values are listed in the Dataset and Submission sections. Invalid row-local categorical values receive zero for the entire row and receive no calibration credit for that row. Structural CSV errors such as wrong columns, duplicate IDs, missing IDs, ID-set mismatch, or invalid confidence are rejected by the grader.
> The row categorical score is:
> row = 0.10 * hazard_type
> + 0.03 * hazard_phase
> + 0.22 * affected_zone
> + 0.20 * vulnerable_user_present
> + 0.23 * public_risk_level
> + 0.22 * response_priority
> The final score is:
> row_power = row^1.60
> Final = 0.18 * mean(row_power)^2.20
> + 0.52 * mean(row_exact)^1.35
> + 0.04 * mean(hazard_type)^2.00
> + 0.08 * mean(risk_priority)^2.00
> + 0.04 * mean(calibration)^1.50
> + 0.14 * worst_group^1.80
> row_exact is 1 only when all six categorical heads are correct for the row. risk_priority is the average of public-risk and response-priority correctness. calibration is max(0, 1 - (confidence - exact_row_indicator)^2) and is only awarded when all categorical values in the row are valid. worst_group is the lowest mean row_power across hidden source-hazard, risk, and priority groups, so a solution that only works on one visible event family will not score as well as a robust dispatch-state model.
> Higher is better. Theoretical minimum: 0.0. Theoretical maximum: 1.0. A perfect label submission with confidence 1.0 scores exactly 1.0.
> Dataset
> Files shipped to participants are listed below. All paths in CSVs are relative to public/.
> Item	Description
> public/train.csv	Training clip inputs
> public/train_labels.csv	Training labels
> public/test.csv	Test clip inputs
> public/videos/*.mp4	Prepared video clips
> public/sample_submission.csv	Submission template
> public/train.csv contains one row per prepared training clip. It has no original source filenames or source labels embedded in the path.
> Column	Type	Description
> clip_id	string	Opaque clip id
> video_path	string	Relative MP4 path
> duration_sec	float	Clip duration
> frame_rate	float	Prepared FPS
> public/test.csv has the same public input columns as train.csv and omits labels.
> Column	Type	Description
> clip_id	string	Opaque clip id
> video_path	string	Relative MP4 path
> duration_sec	float	Clip duration
> frame_rate	float	Prepared FPS
> public/train_labels.csv contains the labels for training clips.
> Column	Type	Description
> clip_id	string	Matches train id
> hazard_type	category	Event family
> hazard_phase	category	Constant event phase (active_event)
> affected_zone	category	Road zone
> vulnerable_user_present	category	VRU evidence
> public_risk_level	category	Risk severity
> response_priority	category	Dispatch urgency
> Allowed hazard_type values are road_accident, vehicle_fire, fight_or_assault, gunpoint_or_snatching, and pothole. hazard_phase is intentionally constant in this version: every row must use active_event, because the inspected source provides active-hazard clips but no reliable normal, pre-event, or aftermath phase annotation. Allowed affected_zone values are lane, shoulder, intersection, and unknown. Allowed vulnerable_user_present values are yes, no, and unclear. Allowed public_risk_level values are none, low, medium, high, and critical. Allowed response_priority values are normal, monitor, inspect_soon, and dispatch_urgent. The non-phase triage heads are not fixed by incident family; they vary within several incident families using clip-level visual evidence such as salience location, visible motion, contrast, and severity cues.
> Submission
> Submit a CSV file with exactly these columns in this order:
> Column	Type	Constraint
> clip_id	string	Same ids as test
> hazard_type	category	Allowed value
> hazard_phase	category	Must be active_event
> affected_zone	category	Allowed value
> vulnerable_user_present	category	Allowed value
> public_risk_level	category	Allowed value
> response_priority	category	Allowed value
> confidence	float	In [0,1]
> Every clip_id from public/test.csv must appear exactly once. Extra IDs, missing IDs, duplicate IDs, missing columns, extra columns, reordered columns, non-finite confidence, and confidence values outside [0, 1] are invalid structural submissions.
> Example submission rows:
> clip_id,hazard_type,hazard_phase,affected_zone,vulnerable_user_present,public_risk_level,response_priority,confidence
> clip_a13f4c9b8e2010,road_accident,active_event,lane,yes,critical,dispatch_urgent,0.88
> clip_b57e2d9046ac31,pothole,active_event,lane,no,medium,inspect_soon,0.71
> Enforcement On Invalid Approaches
> Submissions based on source lookup, source filenames, source folder inference, video reverse search, row-order side channels, metadata-only shortcuts, or grader-format exploitation may be rejected before payout. The task is to learn the relationship between the provided prepared road clips and the structured dispatch-state labels from the public training data.

Inspiration note: Useful because it uses visual evidence for structured state or risk prediction, not just ordinary image classification.

## Grating Misalignment Recovery From A Moire Pattern

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx766n9z3aj6mf04dp9er0xb2h895mwc
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Semiconductor overlay metrology, precision displacement sensors, and security-print inspection often place one fine grating over another; a tiny rotation, scale error, or phase shift between the sheets produces large wavy moire bands that make sub-pixel misalignment visible. This challenge turns that metrology problem into a single-image benchmark: from one rendered grating overlay, infer the hidden top-layer misalignment up to its true periodic ambiguity and answer a counterfactual nudge query.
> You are given one RGB image containing a reference grating and a second fine grating overlaid on top of it. The top grating is slightly rotated, slightly rescaled, and shifted in-plane relative to the reference grating. The visible moire bands encode the hidden rotation/scale mismatch and the shift phase, but absolute shift repeats every grating period, so the correct answer is often a set of equivalent shifts rather than one overconfident value.
> Synthetic-to-real note: the images are synthetic layered-film renders, not photographs, but they preserve the metrology cues that matter here: carrier grating visibility, moire fringe geometry, contrast loss, dust, sheet edges, fiducial ticks, and lighting variation. The task is not to identify a render style; it is to recover physically meaningful alignment buckets from the visible moire pattern.
> For each test image, predict rotation_bucket, scale_bucket, shift_set_json, cf_moire_json, and confidence. Public metadata gives only the reference grating type, grid resolution, and a queried rotation nudge in degrees. It never gives the true misalignment, hidden period, subgroup tags, render style, or private answer. Public IDs are salted and opaque, public asset names are reassigned, and raw generation settings are redacted from the challenge artifacts.
> What Not To Use (any of these may cause rejection on review, regardless of score):
> Filename, row order, hashes, or file metadata as answer signals; predictions must come from the public image pixels and public CSV fields only.
> Private files or platform probes, including attempts to read private/answers.csv or recover generation settings.
> Source lookup or raw-corpus lookup, including attempts to use generator internals, raw upload rows, source file order, or hidden scene hashes instead of the public image pixels and public CSV fields.
> Single texture naming such as reporting "wavy stripes" without estimating the structured rotation, scale, modulo shift, and counterfactual fringe heads.
> Over-precise shift guesses that ignore grating-period wraparound; the intended output is an equivalence set when several shifts are physically identical.
> Brittle deterministic parser shortcuts that ignore the rendered capture variation, such as a fixed threshold/Fourier script tuned to one carrier style instead of visual metrology across line, dot, and hex gratings.
> Hosted or closed-source APIs for training, inference, distillation, or pseudo-labelling.
> Format hacks, extra columns, malformed JSON, invalid bucket names, non-finite confidence, or submissions designed to exploit the grader rather than solve the task.
> Enforcement on invalid approaches: rule-only solutions, metadata side-channel solutions, or submissions that do not perform the stated image-based moire metrology task may be rejected before payout. The goal is to reward genuine visual inverse reasoning under periodic ambiguity.
> Evaluation
> Each row receives a correctness score in [0, 1] from four heads. S_shift is the Jaccard score between the predicted modulo shift equivalence set and the private true set, with correct abstention credited only when the image is genuinely too weak to determine the shift phase. S_cf compares the counterfactual fringe orientation and spacing buckets after the public rotation nudge. S_rot gives ordinal credit for the unsigned rotation-magnitude bucket, because a single still image does not reliably identify clockwise versus counterclockwise sign. S_scale gives ordinal credit for nearby scale buckets.
> The raw row formula is correctness_raw = 0.38*S_shift^2 + 0.30*S_cf^2 + 0.18*S_rot^2 + 0.14*S_scale^2.
> The stricter row correctness is correctness = correctness_raw^1.80, which keeps perfect labels at full credit while reducing common-prior and partly correct guesses.
> Calibration is 1 - |confidence - correctness|.
> The row score is 0.90*correctness + 0.10*calibration.
> The final score is 0.68*mean(row_score) + 0.14*worst(split_group) + 0.10*worst(ood_axis) + 0.08*worst(render_style).
> The subgroup labels are private and are used only by the grader. Each worst-subgroup term is the lowest mean row score within that hidden axis. Higher is better. The theoretical minimum is 0.0; the theoretical maximum is 1.0. The grader returns 0.0 for missing, extra, or reordered columns; duplicate IDs; row-set mismatch; invalid confidence; invalid rotation/scale bucket; malformed or over-long JSON; or invalid counterfactual bucket values.
> Dataset
> The dataset ships under public/ with train images, test images, CSV files, and a sample submission. Image paths are relative to the public/ root.
> File overview
> The public/ directory contains five items: train/images/*.jpg are the training moire renders; test/images/*.jpg are the test moire renders; train.csv contains inputs and labels for training; test.csv contains inputs only; and sample_submission.csv is a weak placeholder submission with the required columns.
> Item	Description
> train/images/*.jpg	Train images
> test/images/*.jpg	Test images
> train.csv	Inputs + labels
> test.csv	Inputs only
> sample_submission.csv	Template
> train.csv columns
> id (int) is the unique public row identifier. image (string) is the relative JPEG path. ref_grating_type (string) is line, dot, or hex. grid_res (string) is the phase-grid convention used for shift JSON. cf_nudge_deg (float) is the queried top-layer rotation nudge. prompt (string) repeats the task instruction. rotation_bucket (string) is one of near_zero, small, medium, or large; it is an unsigned magnitude bucket, not a clockwise/counterclockwise sign. scale_bucket (string) is one of smaller, slightly_smaller, matched, slightly_larger, or larger. shift_set_json (string) is the modulo shift equivalence set or an abstention object. cf_moire_json (string) is the counterfactual fringe bucket object.
> Column	Type	Description
> id	int	Public row id
> image	string	JPEG path
> ref_grating_type	string	line/dot/hex
> grid_res	string	Shift grid
> cf_nudge_deg	float	Query nudge
> prompt	string	Task text
> rotation_bucket	string	Rotation label
> scale_bucket	string	Scale label
> shift_set_json	string	Shift set
> cf_moire_json	string	Future fringe
> test.csv columns
> test.csv has the six public input columns and no labels: id is the unique public row identifier; image is the relative JPEG path; ref_grating_type is the reference grating family; grid_res gives the shift-grid convention; cf_nudge_deg gives the queried rotation nudge; and prompt repeats the task instruction.
> Column	Type	Description
> id	int	Public row id
> image	string	JPEG path
> ref_grating_type	string	line/dot/hex
> grid_res	string	Shift grid
> cf_nudge_deg	float	Query nudge
> prompt	string	Task text
> Submission
> Submit a CSV with exactly these six columns in this order: id, rotation_bucket, scale_bucket, shift_set_json, cf_moire_json, confidence.
> Column	Type	Constraint
> id	int	Same test ids
> rotation_bucket	string	Allowed bucket
> scale_bucket	string	Allowed bucket
> shift_set_json	string	Valid JSON
> cf_moire_json	string	Valid JSON
> confidence	float	In [0,1]
> shift_set_json must either be {"abstain":true} or a JSON object with abstain:false, period_bins, canvas_bins, x_mod_bins, and y_mod_bins. The x_mod_bins and y_mod_bins fields are integer lists on a 0..47 canvas-grid convention, and the set they describe is the Cartesian product of those lists. A line-grating shift can legitimately have many equivalent bins along the stripe direction.
> cf_moire_json must be a JSON object with orientation_bucket and spacing_bucket. Orientation buckets are east_west, ne_sw, north_south, nw_se, east_west_steep, ne_sw_steep, north_south_steep, and nw_se_steep. Spacing buckets are very_wide, wide, medium, tight, and very_tight.
> Example of a correctly formatted submission file:
> Header: id,rotation_bucket,scale_bucket,shift_set_json,cf_moire_json,confidence
> Example row with a shift set: 102,small,slightly_larger,"{""abstain"":false,""period_bins"":12,""canvas_bins"":48,""x_mod_bins"":[3,15,27,39],""y_mod_bins"":[5,17,29,41]}","{""orientation_bucket"":""ne_sw"",""spacing_bucket"":""wide""}",0.62
> Example abstention row: 219,near_zero,matched,"{""abstain"":true}","{""orientation_bucket"":""east_west"",""spacing_bucket"":""very_wide""}",0.40
> Example medium-rotation row: 314,medium,smaller,"{""abstain"":false,""period_bins"":12,""canvas_bins"":48,""x_mod_bins"":[1,13,25,37],""y_mod_bins"":[0,12,24,36]}","{""orientation_bucket"":""north_south"",""spacing_bucket"":""medium""}",0.71

Inspiration note: Useful because it uses visual evidence for structured state or risk prediction, not just ordinary image classification.

## Wind Turbine Blade Thermography Maintenance Triage

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77297a1jy6kc09f4b1neagnn8933qq
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Problem Description
> Blade inspections often include thermal imagery that highlights apparent heating, local hot spots, elongated damage-like signatures, or broad diffuse patterns on composite structures. The task is to read source-neutral prepared blade inspection photos and produce a compact maintenance-triage report from the visual evidence.
> Overview
> Each case contains a thermal blade image and, when available, a paired visual/RGB image. Some thermal-only cases use a neutral placeholder in the RGB path; the thermal image is always the main evidence. For each hidden test case, predict the apparent damage stage, thermal severity, maintenance urgency, evidence pattern, and confidence.
> The target labels are apparent thermal-morphology triage labels derived from the prepared inspection media. They are not claims of certified engineering damage state, remaining blade lifetime, or actual work-order decisions. Strong solutions should learn visual cues such as localized hot spots, elongated heat traces, broad heating, weak/no clear signal, and how those cues combine into a structured triage report.
> What not to use:
> Do not identify or search for the upstream source dataset, original filenames, source videos, source frame positions, camera timestamps, original image IDs, or row order.
> Do not build a hardcoded source-file lookup table, manually label hidden test images, or submit id-to-answer maps.
> Do not use non-visual metadata-only shortcuts that ignore the prepared inspection images.
> The challenge rewards learned image modeling from the provided public training examples and prepared image files.
> Dataset
> The public dataset contains train.csv, train_labels.csv, test.csv, sample_submission.csv, and an images/ folder. Public IDs and image paths are opaque and do not reveal source filenames, frame numbers, or split order.
> Item	Description
> train.csv	public train inputs
> train_labels.csv	train targets
> test.csv	hidden-label inputs
> sample_submission.csv	valid weak dummy
> images/	prepared JPEG images
> train.csv gives the image paths for training cases. train_labels.csv gives the labels for those same case_id values. test.csv has the same input columns as train.csv but no labels. sample_submission.csv is a legal low-signal submission for schema checking.
> train.csv Columns
> Column	Type	Description
> case_id	string	opaque case id
> rgb_image_path	string	RGB or placeholder
> thermal_image_path	string	thermal JPEG path
> train_labels.csv Columns
> Column	Type	Description
> case_id	string	opaque case id
> damage_stage	string	apparent stage
> thermal_severity	string	heat severity
> maintenance_urgency	string	triage urgency
> evidence_pattern	string	visual pattern
> confidence	float	label certainty
> Allowed damage_stage values are none, early_localized, growing_localized, and advanced_diffuse.
> Allowed thermal_severity values are none, low, medium, and high.
> Allowed maintenance_urgency values are normal, monitor, inspect_soon, and repair_priority.
> Allowed evidence_pattern values are no_clear_signal, localized_hotspot, elongated_crack_like, and diffuse_heating.
> test.csv Columns
> Column	Type	Description
> case_id	string	opaque case id
> rgb_image_path	string	RGB or placeholder
> thermal_image_path	string	thermal JPEG path
> Submission Format
> Submit exactly one row for every test case_id, using the exact columns and order below.
> Column	Type	Constraint
> case_id	string	exact test id
> damage_stage	string	allowed value
> thermal_severity	string	allowed value
> maintenance_urgency	string	allowed value
> evidence_pattern	string	allowed value
> confidence	float	0 to 1
> Example row:
> case_id	damage_stage	thermal_severity	maintenance_urgency	evidence_pattern	confidence
> wt_012345abcdef	early_localized	low	monitor	localized_hotspot	0.78
> Sample submission rows:
> case_id,damage_stage,thermal_severity,maintenance_urgency,evidence_pattern,confidence
> wt_02e2d60a55be,advanced_diffuse,high,repair_priority,diffuse_heating,0.5
> wt_083ec13f9328,advanced_diffuse,high,repair_priority,diffuse_heating,0.5
> wt_0881bf3021e5,advanced_diffuse,high,repair_priority,diffuse_heating,0.5
> Evaluation
> Structural invalid submissions raise an invalid-submission error rather than receiving a valid score. Structural invalidity includes missing, extra, or reordered columns; duplicate case_id values; missing or extra test ids; non-numeric confidence; non-finite confidence; or confidence outside [0, 1].
> Row-local invalid label strings receive zero task credit for that affected row and zero calibration credit for that row. Other structurally valid rows are still scored normally.
> For valid submissions, each row receives a weighted triage score. damage_stage, thermal_severity, and maintenance_urgency are ordinal heads: exact matches receive 1.0, one-step misses receive limited partial credit, and farther misses receive little or no credit. evidence_pattern is exact-match. AllExact is 1.0 only when all four label heads are exactly correct. Confidence = max(0, 1 - abs(submitted_confidence - hidden_confidence) / 0.5) and is awarded only when all row labels are valid.
> RowScore = 0.075 * Damage + 0.075 * Severity + 0.075 * Urgency + 0.075 * Pattern + 0.60 * AllExact + 0.10 * Confidence.
> WorstGroup is the minimum mean RowScore over hidden damage_stage, thermal_severity, maintenance_urgency, and evidence_pattern groups.
> Final = 0.90 * mean(RowScore) + 0.10 * WorstGroup.
> The theoretical minimum is 0.0; the theoretical maximum is 1.0; higher is better. A structurally valid all-invalid-label submission can score 0.0, and a perfect submission with the hidden labels scores exactly 1.0.
> Intended Solution
> Strong solutions should use computer-vision models, image embeddings, multimodal RGB/thermal fusion when an RGB image exists, and calibrated classifiers or fine-tuned vision backbones. Thermal-only cases should still be handled from visual thermal evidence. Simple priors, path metadata, and RGB placeholders are intentionally weak compared with models that read the thermal image content.
> Enforcement On Invalid Approaches
> Submissions based on upstream source lookup, original file names, hidden frame positions, raw timestamp recovery, manual hidden-test labeling, hardcoded id maps, row-order shortcuts, or non-visual metadata-only heuristics may be rejected before payout even if the CSV is structurally valid.

Inspiration note: Useful because it uses visual evidence for structured state or risk prediction, not just ordinary image classification.

## Elevation and Repair Mask Reconstruction from Surface Tiles

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cgxzcvn6s565qdpf6dgyc9h8a0nz8
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: image, segmentation, Dataset source is visible after the challenge closes.
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> You are given grayscale overhead surface tiles derived from remote-sensing height products. Each tile is a compact visual card: brightness changes, ridge texture, crater-like depressions, shadows, and unusually smooth regions provide partial evidence about both local surface shape and the locations where the underlying measurement grid needed repair.
> For each held-out tile, reconstruct a three-layer ledger on a 64-by-64 grid:
> a 64-level local relief code with one integer value per cell,
> a binary anomaly-repair layer marking cells whose original measurement behaved like an outlier before repair,
> a binary void-repair layer marking cells whose original measurement was absent before filling.
> This is an image-to-ledger reconstruction task. The target is not a category label and not a continuous physical-height export. A strong solution must infer a compact surface code and two repair-provenance layers from the visual tile.
> Dataset
> train.csv: 500 labeled examples with id, image path, prompt, image dimensions, expected answer schema, and answer_json.
> test.csv: 300 held-out examples with the same public input columns except answer_json.
> sample_submission.csv: 300-row valid baseline submission.
> images/: PNG surface tile images referenced by the CSV files.
> Column definitions:
> id (string): Opaque row id.
> image_path (string): Relative path to the surface tile image.
> prompt (string): Natural-language instruction for the reconstruction task.
> frame_width (integer): Input image width in pixels.
> frame_height (integer): Input image height in pixels.
> answer_format_json (JSON object): Required output schema. It specifies height=64, width=64, and the required fields elevation_q, deviation_rle, and nan_rle.
> answer_json (JSON object, train only): Ground-truth ledger object.
> answer_json has this structure:
> height (integer): Always 64.
> width (integer): Always 64.
> elevation_q (list of integers): Exactly 4096 row-major cells, top-left to bottom-right. Each value must be an integer from 0 to 63. The field name is fixed by the grader; semantically, these are local relief codes, where nearby values represent similar surface height within the tile.
> deviation_rle (list of [value, count] pairs): Run-length encoded 64-by-64 binary anomaly-repair layer. 1 marks a cell repaired because the original measurement behaved like an outlier; 0 marks all other cells.
> nan_rle (list of [value, count] pairs): Run-length encoded 64-by-64 binary void-repair layer. 1 marks a cell repaired because the original measurement was absent before filling; 0 marks all other cells.
> RLE format is row-major over the 4096 grid cells. Each run is [value, count], where value is 0 or 1, count is a positive integer, and all counts in the list must sum to exactly 4096.
> Submission Format
> Submit a CSV with exactly these columns: id, answer_json.
> The included sample_submission.csv is a complete valid submission example with all 4096 relief-code cells. A shortened display example is:
> id,answer_json
> row_example,"{""height"":64,""width"":64,""elevation_q"":[31,31,32,32],""deviation_rle"":[[0,4096]],""nan_rle"":[[0,4096]]}"
> Do not use ellipses or shortened arrays in an actual submission. A submitted row must contain all 4096 relief-code integers, and each RLE list must decode to exactly 4096 binary cells.
> Evaluation
> Each submitted row is decoded into three 64-by-64 ledger layers and scored from 0 to 1.
> For the local relief-code layer:
> mae = mean(abs(pred_elevation_q[i] - true_elevation_q[i])) over all 4096 cells.
> normalized_mae_score = max(0, 1 - mae / 12).
> coarse_bin_accuracy = mean((pred_elevation_q[i] // 4) == (true_elevation_q[i] // 4)).
> exact_cell_accuracy = mean(pred_elevation_q[i] == true_elevation_q[i]).
> elevation_score = 0.70 * normalized_mae_score + 0.20 * coarse_bin_accuracy + 0.10 * exact_cell_accuracy.
> For each binary mask:
> Decode the submitted RLE and true RLE into 4096 binary cells.
> IoU = intersection / union, where intersection counts cells that are 1 in both masks and union counts cells that are 1 in either mask.
> If both masks contain no positive cells, IoU is defined as 1.0.
> The row score is:
> 0.74 * elevation_score + 0.13 * deviation_iou + 0.13 * nan_iou
> The final leaderboard score is:
> 0.82 * mean_row_score + 0.06 * worst_relief_range_group + 0.06 * worst_repair_density_group + 0.06 * worst_region_group
> mean_row_score is the average row score over the hidden answers. Each worst-group term is the lowest mean row score among held-out grouping labels with at least five rows. The grouping labels represent relief range, repair-mask density, and broad acquisition-region buckets. Higher is better.
> What Not To Use
> Hardcoded mappings from image filenames or row ids to answers.
> Any files, labels, masks, or metadata outside the released public files.
> Row-order shortcuts or package-internal generation artifacts.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Yeast Cell Count and Morphology Prediction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dq3vvhns8dw5fe6qrxtsbfs89m6qx
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↓ Lower is better
- Tags: image, feature-engineering, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> This challenge uses grayscale microscopy crops of yeast cells growing in small engineered microstructures. In this setting, researchers care about practical image-derived summaries such as how many cells are visible, how much of the local field is covered by cells, and whether the visible cells appear compact or elongated. These quantities are useful for checking growth, crowding, segmentation quality, and local morphology without requiring a participant to submit full instance masks.
> Each public PNG is a transformed crop from a larger microscopy field. The crop has been resized and lightly perturbed with rotation, contrast variation, blur, and noise. The original instance masks are not provided for the test images. During dataset preparation, those hidden annotations are used to compute four direct microscopy targets:
> cell_count_bin: a 5-way count target for the number of visible cells in the crop, with bin 4 meaning four or more cells.
> cell_confluence: the fraction of crop pixels covered by visible cell masks.
> mean_cell_area: the average visible cell-mask area as a fraction of the crop area.
> elongation_score: an aspect-ratio morphology score where compact cells are near 0 and more elongated visible cells are closer to 1.
> This is not a segmentation or object-detection submission task. The goal is to infer annotation-derived cell-count and morphology summaries from degraded grayscale crops. Test crops come from source records held out from training and over-sample peripheral regions, so random crop-level validation can overestimate performance.
> Evaluation
> Submissions are scored with a bounded lower-is-better objective:
> raw_score = 0.55 * CountLogLoss + 0.45 * MorphologyNRMSE
> score = min(raw_score / 2.25, 1.0)
> CountLogLoss is the average multiclass log loss for the five cell_count_bin probabilities. Before computing this term, each submitted probability is clipped to [1e-15, 1], then the five probabilities in each row are renormalized to sum to one.
> MorphologyNRMSE is the mean normalized root mean squared error across cell_confluence, mean_cell_area, and elongation_score. Submitted morphology values are clipped to [0, 1] before scoring, and each target's RMSE is normalized by that target's standard deviation in the hidden answers.
> The final score combines the count and morphology errors, divides by 2.25, and caps the result at 1.0. Lower scores are better.
> Dataset
> The prepared public dataset contains:
> public/
> |-- train.csv
> |-- test.csv
> |-- sample_submission.csv
> |-- train_images/
> |-- test_images/
> There are 540 training rows and 288 test rows.
> train.csv columns:
> Column	Type	Description
> id	integer	Training row identifier.
> image_path	string	Relative path to the transformed training crop.
> source_fold	integer	Coarse source-record grouping key for validation design.
> cell_count_bin	integer	Visible cell-count class from 0 to 4, where 4 means four or more cells.
> cell_confluence	float	Fraction of crop pixels covered by visible cell masks.
> mean_cell_area	float	Average visible cell area divided by crop area.
> elongation_score	float	Mean visible-cell elongation score in [0, 1].
> test.csv columns:
> Column	Type	Description
> id	integer	Test row identifier.
> image_path	string	Relative path to the transformed test crop.
> Submission
> Submit a CSV file with exactly these columns:
> Column	Type	Description
> id	integer	Test id from test.csv.
> p_count_0	float	Predicted probability for zero visible cells.
> p_count_1	float	Predicted probability for one visible cell.
> p_count_2	float	Predicted probability for two visible cells.
> p_count_3	float	Predicted probability for three visible cells.
> p_count_4	float	Predicted probability for four or more visible cells.
> cell_confluence	float	Predicted cell confluence.
> mean_cell_area	float	Predicted mean visible cell area.
> elongation_score	float	Predicted mean visible cell elongation.
> Example:
> id,p_count_0,p_count_1,p_count_2,p_count_3,p_count_4,cell_confluence,mean_cell_area,elongation_score
> 100000,0.15,0.30,0.25,0.20,0.10,0.18,0.07,0.31
> 100001,0.40,0.25,0.18,0.10,0.07,0.04,0.03,0.12
> 100002,0.08,0.20,0.32,0.25,0.15,0.34,0.11,0.42
> Requirements:
> The submission must contain exactly 288 rows.
> The id values must match test.csv exactly.
> Include a header row.
> Write the final submission to ./working/submission.csv.
> Baselines
> The provided sample_submission.csv predicts training count priors and training mean morphology values. Its score is approximately 0.602716.
> Allowed And Prohibited
> Allowed:
> Use the prepared public files under ./dataset/public/.
> Train models using the provided training labels.
> Use image preprocessing, self-supervised learning on the provided public images, ensembling, calibration, and source-aware validation.
> Use general-purpose libraries available in the execution environment.
> Prohibited:
> Do not use private answer files or any information from ./dataset/private/.
> Do not use raw source tensors, hidden support tensors, external datasets, unprovided source materials, or original annotation files.
> Do not attempt to identify, match, or recover the original records behind the prepared public crops.
> Do not manually inspect or infer labels from hidden preparation code or private files.
> Expected Output
> Your solution must write:
> ./working/submission.csv

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Microfield Counterfactual Repair Audit

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73faxff6wy4247czn3p18ah189g93t
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: image, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> High-throughput microscopy scanners often capture tissue or cellular regions as a grid of adjacent microfields. These microfields are later assembled through a stitching or registration stage. In real scanning pipelines, local coherence can fail before global stitching begins because of stage drift, focus slips, illumination changes, sample warping, camera jitter, compression traces, or micro-fractures.
> Microfield Counterfactual Repair Audit (MCRA) is a visual-spatial reasoning benchmark built around this failure mode. Each case contains four adjacent microfield views arranged as a 2x2 matrix. The model must jointly inspect the four views, evaluate whether the local field can close spatially, estimate rupture severity, classify the audit state, and choose the minimal counterfactual repair action needed to restore coherence.
> This is not a single-image anomaly task and not a plain tabular classification task. A strong solution must combine image evidence, cross-view boundary reasoning, calibrated probability prediction, ordinal severity estimation, and logically consistent repair planning.
> Dataset Size
> The released split is intentionally large enough to reduce leaderboard noise for an image + tabular multi-task challenge.
> Plaintext
> +----------------------+------------+------------------------------------------+
> | Component            | Count      | Notes                                    |
> +----------------------+------------+------------------------------------------+
> | public/train.csv     | 1,000 rows | 200 rows per audit_code class.           |
> | public/test.csv      | 250 rows   | 50 rows per audit_code class.            |
> | public/images/train/ | 4,000 JPGs | Four image views per training case.      |
> | public/images/test/  | 1,000 JPGs | Four image views per test case.          |
> | private/answers.csv  | 250 rows   | Hidden labels for the public test cases. |
> +----------------------+------------+------------------------------------------+
> Research Grounding and Frontier Novelty
> MCRA is designed to be different from standard microscopy, stitching, and VQA datasets. The novelty is the coupled counterfactual repair-audit formulation: the model is not rewarded for only identifying a defect, only predicting a probability, or only classifying a tile. It must produce a complete, internally consistent audit card across categorical, probabilistic, ordinal, and counterfactual repair targets.
> Plaintext
> +------------------------------------+---------------------------------------------------------+
> | Related Paradigm                   | How MCRA Differs                                        |
> +------------------------------------+---------------------------------------------------------+
> | Independent microscopy tile tasks  | Uses four connected views and requires local spatial    |
> |                                    | coherence reasoning across view boundaries.             |
> +------------------------------------+---------------------------------------------------------+
> | Classical stitching tools          | Does not ask solvers to run a registration optimizer;   |
> |                                    | asks them to diagnose failure and infer repair intent.  |
> +------------------------------------+---------------------------------------------------------+
> | Single-image anomaly detection     | Requires multi-output structural reasoning rather than  |
> |                                    | one isolated defect class or anomaly score.             |
> +------------------------------------+---------------------------------------------------------+
> | Microscopy VQA                     | Replaces free-text answers with strict machine targets: |
> |                                    | audit_code, closure_score, rupture_level, repair_action.|
> +------------------------------------+---------------------------------------------------------+
> | Generic counterfactual image tasks | Uses physically motivated local field repair decisions  |
> |                                    | rather than semantic object edits.                      |
> +------------------------------------+---------------------------------------------------------+
> Note: The benchmark is deliberately multi-task. The evaluation rewards models that preserve logical symmetry between audit state, closure probability, rupture severity, and repair action. For example, a predicted severe rupture with a no-repair action is internally inconsistent, even if one individual column looks plausible.
> Data Provenance and Security Note
> The underlying microscopy-style image source is transformed into salted, isolated four-view sub-grids. Original acquisition identifiers, source filenames, raw labels, and source order are not exposed in public files. Public image filenames are salted hashes. Full provenance and license information are maintained for platform review and dataset-source disclosure after competition closure according to host-platform rules.
> View Layout Matrix
> Each row represents one localized 2x2 microfield matrix:
> Plaintext
> +-----------------------------------------------------------------+
> |                  TOP-LEVEL 2x2 SPATIAL MATRIX                   |
> +--------------------------------+--------------------------------+
> |             view_a             |             view_b             |
> |  Top-left microfield image     |  Top-right microfield image    |
> +--------------------------------+--------------------------------+
> |             view_c             |             view_d             |
> |  Bottom-left microfield image  |  Bottom-right microfield image |
> +--------------------------------+--------------------------------+
> Task Objective
> Given the four image views and associated tabular image-quality metadata, predict the following audit card for each test case:
> Plaintext
> +---------------+--------+-------------------------------------------------------------+
> | Output Field  | Type   | Objective                                                   |
> +---------------+--------+-------------------------------------------------------------+
> | audit_code    | string | Categorical structural quality-control state.               |
> | closure_score | float  | Predicted probability in [0.0, 1.0] that closure truth = 1. |
> | rupture_level | int    | Ordinal severity score from 0 to 5.                         |
> | repair_action | string | Minimal intervention required to restore coherence.         |
> +---------------+--------+-------------------------------------------------------------+
> Prepared Target Domains
> audit_code labels
> Labels are strict and case-sensitive. Participants must submit the exact strings shown below.
> Plaintext
> +---------------+--------------------------------------------------------------+
> | Label         | Structural Meaning                                           |
> +---------------+--------------------------------------------------------------+
> | sealed-field  | All four views preserve local coherence; no repair needed.   |
> | soft-drift    | Mild stage drift exists, but the grid remains stitchable.    |
> | edge-rupture  | A boundary failure prevents ordinary local closure.          |
> | single-repair | One view is the dominant corrupt node and can be replaced.   |
> | multi-break   | Multiple views or regions fail; local repair is insufficient.|
> +---------------+--------------------------------------------------------------+
> repair_action labels
> Labels are strict and case-sensitive. For example, repair-A is valid, but repair-a, Repair-A, repair_A, and numeric aliases are invalid.
> Plaintext
> +-------------+--------------------------------------------------+
> | Repair Tag  | Action Meaning                                   |
> +-------------+--------------------------------------------------+
> | keep        | No repair is needed.                             |
> | repair-A    | Replace or re-acquire view_a, the top-left node. |
> | repair-B    | Replace or re-acquire view_b, the top-right node.|
> | repair-C    | Replace or re-acquire view_c, the bottom-left.   |
> | repair-D    | Replace or re-acquire view_d, the bottom-right.  |
> | multi       | Drop or re-acquire the full four-view grid.      |
> +-------------+--------------------------------------------------+
> Dataset Architecture
> Plaintext
> dataset/
> ├── public/
> │   ├── train.csv              # Input features + complete multi-task targets
> │   ├── test.csv               # Input features only; no target columns
> │   ├── sample_submission.csv  # Required submission schema and row order
> │   └── images/
> │       ├── train/             # 4,000 JPEG view nodes
> │       └── test/              # 1,000 JPEG view nodes
> └── private/
> └── answers.csv            # Hidden test oracle used by the grader
> Image Specifications
> Plaintext
> +-----------------+--------------------------------------------+
> | Parameter       | Configuration                              |
> +-----------------+--------------------------------------------+
> | Encoding format | JPEG (.jpg)                                |
> | Spatial size    | 224 x 224 pixels per independent view node |
> | Color space     | 3-channel RGB                              |
> | Case layout     | Four image paths per row: view_a to view_d |
> +-----------------+--------------------------------------------+
> Images may contain realistic scanning artifacts including focus degradation, oblique illumination gradients, local sensor glitches, translational stage drift, compression traces, and micro-fracture-like discontinuities.
> Column Naming and Target Schema
> Plaintext
> +-----------------------+---------------+------------------------------------------------------+
> | File / Context        | Column        | Required Meaning                                     |
> +-----------------------+---------------+------------------------------------------------------+
> | public/train.csv      | closure       | Binary training target: 1 = closed, 0 = ruptured.    |
> | public/test.csv       | none          | Features only; no closure or closure_score column.   |
> | sample_submission.csv | closure_score | Example predicted probability in [0.0, 1.0].         |
> | submission.csv        | closure_score | Participant probability that closure truth equals 1. |
> | private/answers.csv   | closure_score | Hidden binary oracle 0/1; not a probability.         |
> +-----------------------+---------------+------------------------------------------------------+
> Important: closure_score has two different roles depending on file context. In submission.csv it is a predicted probability. In private/answers.csv it is the hidden binary 0/1 oracle.
> Comprehensive Dataset Features
> Plaintext
> +-------------------------+--------+------------------------------------------+
> | Column Identifier       | Type   | Description                              |
> +-------------------------+--------+------------------------------------------+
> | case_id                 | string | Globally unique salted sub-grid ID.      |
> | view_a_path             | string | Relative path to top-left image node.    |
> | view_b_path             | string | Relative path to top-right image node.   |
> | view_c_path             | string | Relative path to bottom-left image node. |
> | view_d_path             | string | Relative path to bottom-right image node.|
> | capture_signature       | string | Masked acquisition-style signature.      |
> | signal_mean_a           | float  | Integrated luminosity proxy for view_a.  |
> | signal_mean_b           | float  | Integrated luminosity proxy for view_b.  |
> | signal_mean_c           | float  | Integrated luminosity proxy for view_c.  |
> | signal_mean_d           | float  | Integrated luminosity proxy for view_d.  |
> | signal_range            | float  | Max brightness spread across the grid.   |
> | contrast_range          | float  | Local contrast variability across views. |
> | edge_range              | float  | High-frequency edge spread across views. |
> | texture_range           | float  | Texture variability across views.        |
> | color_range             | float  | RGB chromaticity spread proxy.           |
> | focus_floor_index       | float  | Weakest local focus/sharpness proxy.     |
> | field_pressure_index    | float  | Geometric distortion pressure proxy.     |
> | compression_trace_index | float  | Quantization/compression trace proxy.    |
> | coherence_index         | float  | Baseline cross-view coherence proxy.     |
> | rupture_index           | float  | Boundary mismatch / phase rupture proxy. |
> | audit_load_index        | float  | Structural complexity and entropy proxy. |
> | audit_code              | string | Target in train.csv only.                |
> | closure                 | int    | Binary target in train.csv only.         |
> | rupture_level           | int    | Target in train.csv only.                |
> | repair_action           | string | Target in train.csv only.                |
> +-------------------------+--------+------------------------------------------+
> Evaluation Metric: Counterfactual Repair Audit Score
> Submissions are evaluated using the Counterfactual Repair Audit Score, a robust composite metric that tests classification performance, continuous calibration, ordinal progression, and joint logical consistency.
> Final Score​=0.25⋅F1Audit​+0.15⋅MCCnorm​+0.20⋅BSS+0.15⋅Rord​+0.15⋅F1Repair​+0.10⋅Cjoint​​
> Variable References
> Plaintext
> +--------+------------------------------------------------------+
> | Symbol | Meaning                                              |
> +--------+------------------------------------------------------+
> | y_i    | True audit_code label.                               |
> | p_i    | Predicted audit_code label.                          |
> | s_i    | Binary closure oracle: 0 or 1.                       |
> | q_i    | Predicted closure_score probability in [0.0, 1.0].   |
> | g_i    | True rupture_level value in [0, 5].                  |
> | h_i    | Predicted rupture_level value in [0, 5].             |
> | r_i    | True repair_action token.                            |
> | t_i    | Predicted repair_action token.                       |
> +--------+------------------------------------------------------+
> Closure oracle source:
> In train.csv, the binary closure target is named closure.
> In private/answers.csv, the hidden binary oracle is named closure_score.
> In submission.csv, closure_score is a predicted probability.
> Metric Components
> Audit Macro F1 Score
> Audit Macro F1 evaluates prediction quality across all 5 audit_code classes.
> For each audit class c:
> F1_c = (2 * TP_c) / (2 * TP_c + FP_c + FN_c)
> The final Audit Macro F1 is:
> F1_Audit = (1 / 5) * SUM(c = 1 to 5) F1_c
> Normalized Audit Matthews Correlation Coefficient
> The audit Matthews Correlation Coefficient is normalized into the [0, 1] range.
> MCC_norm = clip((MCC + 1) / 2, 0, 1)
> Closure Brier Skill Score
> The Closure Brier Skill Score evaluates probability calibration.
> The oracle value s_i is binary:
> s_i in {0, 1}
> The submitted closure_score value q_i is a probability:
> q_i in [0.0, 1.0]
> The Brier score is:
> Brier = (1 / N) * SUM(i = 1 to N) (q_i - s_i)^2
> The reference closure rate is:
> r = (1 / N) * SUM(i = 1 to N) s_i
> The reference Brier score is:
> Brier_ref = (1 / N) * SUM(i = 1 to N) (r - s_i)^2
> The final Brier Skill Score is:
> BSS = clip(1 - (Brier / Brier_ref), 0, 1)
> Ordinal Rupture Proximity Score
> The ordinal rupture proximity score rewards near-miss predictions linearly.
> For each row:
> credit_i = 1 - (abs(h_i - g_i) / 5)
> The final ordinal rupture proximity score is:
> R_ord = (1 / N) * SUM(i = 1 to N) credit_i
> Repair Action Macro F1
> Repair Action Macro F1 evaluates prediction quality across all 6 repair_action classes.
> For each repair_action class r:
> F1_r = (2 * TP_r) / (2 * TP_r + FP_r + FN_r)
> The final Repair Action Macro F1 is:
> F1_Repair = (1 / 6) * SUM(r = 1 to 6) F1_r
> Joint Repair Consistency Score
> The joint score checks whether audit prediction, rupture severity, and repair action are logically consistent. No joint credit is awarded when audit_code is wrong.
> For each row:
> audit_exact_i = I(p_i == y_i)
> repair_exact_i = I(t_i == r_i)
> The row-level joint score is:
> joint_i = audit_exact_i * (0.50 + 0.30 * credit_i + 0.20 * repair_exact_i)
> The final joint consistency score is:
> C_joint = (1 / N) * SUM(i = 1 to N) joint_i
> ​
> Strict Submission Requirements
> Submissions must be saved as:
> Plaintext
> ./working/submission.csv
> The file must use this exact column order:
> Plaintext
> case_id,audit_code,closure_score,rupture_level,repair_action
> Submission Failure Conditions
> Plaintext
> +----+---------------------------------------------------------------+
> | No | Rejection State                                               |
> +----+---------------------------------------------------------------+
> | 1  | Submission columns are changed, reordered, omitted, or added. |
> | 2  | Row count or case_id order differs from sample_submission.csv.|
> | 3  | Duplicate, missing, blank, or unknown case_id values appear.  |
> | 4  | closure_score is missing, non-numeric, NaN, Inf, or outside   |
> |    | the [0.0, 1.0] range.                                         |
> | 5  | rupture_level is not an integer from 0 to 5.                  |
> | 6  | audit_code is not an exact canonical string label.            |
> | 7  | repair_action is not an exact canonical string label.         |
> | 8  | Label aliases are used, such as audit_code=0 or repair-a.     |
> | 9  | The file contains helper, target, answer, fold, or leak cols. |
> +----+---------------------------------------------------------------+
> Strict Label Examples
> Plaintext
> +-----------------+--------+---------------------------------------------+
> | Submitted Value | Valid? | Reason                                      |
> +-----------------+--------+---------------------------------------------+
> | sealed-field    | yes    | Exact audit_code label.                     |
> | 0               | no     | Numeric audit_code aliases are rejected.    |
> | Sealed-Field    | no     | Case mismatch.                              |
> | repair-A        | yes    | Exact repair_action label.                  |
> | repair-a        | no     | Case mismatch; no normalization is allowed. |
> | repair_A        | no     | Underscore alias is not accepted.           |
> +-----------------+--------+---------------------------------------------+
> What Not To Use
> Plaintext
> +----+---------------------------------------------------------------+
> | No | Prohibited Method                                             |
> +----+---------------------------------------------------------------+
> | 1  | Accessing or using private/answers.csv during solving.        |
> | 2  | Manually labeling test rows by inspecting hidden labels.      |
> | 3  | Reversing salted case_id values or image names to infer order.|
> | 4  | Searching for external mirrors or source labels.              |
> | 5  | Hardcoding predictions by row index, filename pattern, or ID. |
> | 6  | Submitting blind constants without using image/tabular inputs.|
> | 7  | Adding hidden helper columns to bypass grader validation.     |
> | 8  | Using row-order, source-order, or duplicate-artifact leakage. |
> +----+---------------------------------------------------------------+
> Example Valid Submission
> Code snippet
> case_id,audit_code,closure_score,rupture_level,repair_action
> a91f0c3d7b20e441,sealed-field,0.94,0,keep
> bc42a10f8de93a1,single-repair,0.12,4,repair-C
> d13fa9901bb83a6,multi-break,0.04,5,multi

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Thermal Chart Calibration Cell Segmentation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx761t3zdxt5anhgee81k2gz4h88wc82
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: image, segmentation, feature-engineering, Dataset source is visible after the challenge closes.
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> This is a computer vision segmentation challenge built from rendered MOX gas-sensor thermal-cycle charts. Each image shows several resistance traces and visually similar amber calibration cells. Your task is to segment only the withheld calibration-cell subset for each test image.
> Every amber square or diamond is a candidate calibration cell attached to a trace band, with its center placed no more than 13 vertical pixels from that band's baseline. Only a small subset is labeled as withheld calibration cells. That subset represents cells selected for calibration review according to trace-relative geometry and panel context, especially surface_hint, load_band, vibration_band, and age_band. All other amber candidates are distractors.
> The target distinction is therefore a label-learning task, not a color rule: targets and distractors can have the same shape, color, outline, and size. Use the labeled masks in train.csv to learn how image geometry and the public context fields relate to target membership, then predict the selected subset in each test image.
> The source domain is synthetic MOX gas-sensor profiling. The released challenge transforms sensor-profile records into chart images and hidden spatial masks; raw source values and private masks are not released in the public test set.
> Task Framing
> This benchmark is context-conditioned selective segmentation. In conventional semantic or instance segmentation, an object's local appearance usually defines its class and all matching instances are targets. Here, local appearance identifies only the candidate set; predicting every valid amber cell is explicitly incorrect.
> The source sensor profiles contribute operating dynamics, not pre-existing segmentation labels. The rendered spatial targets and the context-conditioned candidate-selection objective are created specifically for this benchmark.
> Target membership is relational. A candidate must be interpreted jointly with its assigned trace band, its position within the full chart, and the row's panel-level operating context. The required output is one binary mask containing only the context-selected candidates. This combines dense pixel localization with candidate-level selection and image-plus-tabular reasoning in a single prediction task.
> Because targets and distractors come from the same visual candidate family, a crop-only detector cannot determine membership from color or shape alone. A two-stage method may detect candidates first, but its selection stage must still learn the relationship among candidate geometry, the surrounding traces, and the public metadata from the training masks.
> Dataset
> The public dataset contains three CSV files and two image folders.
> train.csv: 720 labeled rows. Each row includes an image path, metadata, and the target column mask_rle.
> test.csv: 716 unlabeled rows. This file has the same feature columns as train.csv, but does not include mask_rle.
> sample_submission.csv: Example submission file with the required columns.
> train_images/: PNG images referenced by train.csv.
> test_images/: PNG images referenced by test.csv.
> Feature columns:
> id: String. Opaque panel identifier.
> image_path: String. Relative path to the PNG image.
> width: Integer. Image width in pixels. All images are 256 pixels wide.
> height: Integer. Image height in pixels. All images are 160 pixels tall.
> device_hint: Categorical string. Coarse gas or sensor-family hint.
> surface_hint: Categorical string. Coarse material hint.
> load_band: Categorical string. One of low, nominal, or high.
> vibration_band: Categorical string. One of quiet, mixed, or rough.
> age_band: Categorical string. One of fresh, seasoned, or stale.
> mask_rle: String. One-indexed run-length encoded binary mask. Present only in train.csv.
> Evaluation
> Submissions are evaluated with a weighted segmentation score. Higher is better. For one image, let P be the set of predicted foreground pixels and T the set of hidden target pixels. Let |M| denote the number of foreground pixels in mask M.
> Dice overlap
> D = 2 * |P intersect T| / (|P| + |T|)
> If both masks are empty, D = 1.
> Centroid recall
> The grader separates each mask into 4-connected components: pixels belong to the same component when they are connected through shared horizontal or vertical edges. A component center is the arithmetic mean (x, y) coordinate of all foreground pixels in that component.
> A hidden component is recalled when at least one predicted component center is within Euclidean distance 8 pixels of the hidden component center. Matching is not required to be one-to-one.
> C = recalled hidden components / total hidden components
> If both masks have no components, C = 1. If only one mask has components, C = 0.
> Area discipline
> When the hidden mask is nonempty:
> A = max(0, 1 - abs(|P| - |T|) / |T|)
> If both masks are empty, A = 1. If the hidden mask is empty but the prediction is not, A = 0.
> Combined score
> The per-image score is the following weighted sum:
> S = 0.55 * D + 0.25 * C + 0.20 * A
> The final submission score is the arithmetic mean of S across all test rows, clipped to the range [0, 1].
> The three terms measure different parts of selective segmentation: Dice evaluates mask shape, centroid recall evaluates whether the selected hidden cells were localized, and area discipline penalizes flooding the output with every visually valid candidate. Thus, detecting all amber cells without learning target membership cannot optimize the metric.
> Submission Format
> Submit a CSV file with exactly two columns: id and mask_rle.
> Example submission:
> id,mask_rle
> stfm_001,1 1
> stfm_002,28 4 190 7
> stfm_003,1 1
> Requirements:
> The file must contain exactly 716 prediction rows plus a header row.
> Every id from test.csv must be present exactly once.
> The only columns must be id and mask_rle.
> mask_rle must contain one-indexed start and length pairs in column-major order.
> Blank or missing values are scored as empty masks, but a submission whose entire mask_rle column is missing is rejected.
> Malformed runs and runs outside the image bounds are rejected.
> An individual RLE cell longer than 65,536 characters is safely scored as an empty mask.
> To encode a mask, flatten it by reading each image column from top to bottom, moving from the leftmost column to the rightmost. Number flattened positions starting at 1. Record each consecutive foreground run as start length, then join all pairs with spaces. For example, 1 3 10 2 marks three pixels beginning at flattened position 1 and two pixels beginning at position 10. A blank value represents an empty mask.
> What Not To Use
> Do not use private answers, hidden masks, or any files outside the released public dataset.
> Do not reverse-map identifiers, use external lookup tables, or reconstruct the raw gas-sensor source records.
> Do not submit masks produced by a rule that ignores the released image content.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Chiromantic Profiling and Cross-Hand Identity

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7708d76y3rkgpxzxks704xxs8b42c3
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Reading the Other Hand: Chiromantic Profiling and Cross-Hand Identity
> What you are building
> A model that looks at one photograph of a palm and answers three quite different questions at once:
> Who is this? — match the palm to a person enrolled in the training set. The catch: you only
> ever enrolled their other hand. Matching a left palm against a gallery of right palms is a
> genuinely hard biometric problem, because a person's two hands are similar but not mirror copies.
> What kind of hand is it? — assign the palm its chiromantic elemental type, the four-way
> Earth / Air / Water / Fire classification that traditional hand-reading builds on, plus the
> hand's 2D:4D digit-ratio band.
> What does the hand you cannot see look like? — infer the elemental type of that person's
> opposite hand, from this hand alone.
> The three questions are deliberately in tension. Identity ties a palm to a person; the chiromantic
> reading describes the hand in front of you; the contralateral question asks you to generalise from
> one hand to its partner.
> Concretely, for every test image you output four fields: subject (question 1),
> element and digit_band (question 2), and contra_element (question 3). They are defined
> precisely in The task below.
> The chiromantic taxonomy, stated plainly
> Traditional palmistry sorts hands into four elemental types using two measurable proportions — how
> elongated the palm is (palm height ÷ palm breadth), and how long the fingers are relative to it
> (mean finger length ÷ palm breadth). Each axis is split at the population median, giving a 2×2 grid:
> palm shape ↓ \ finger length →	short fingers	long fingers
> square palm (elongation below median)	earth	air
> long palm (elongation above median)	fire	water
> Equivalently, in words — the exact rule used to label every hand in this dataset:
> square palm + short fingers → earth
> square palm + long fingers → air
> long palm + short fingers → fire
> long palm + long fingers → water
> Each hand was measured from its landmarks and assigned its type by exactly this rule, with the two
> axes split at the population median. No claim is made, or scored, about what
> any of this predicts about a person. The elemental type is a shape classification and nothing more;
> what you are being asked to do is recover a geometric property of a hand from a photograph of it.
> The 2D:4D digit ratio — index-finger length divided by ring-finger length — is a separate,
> well-studied morphometric. It is reported as a band 0..3 (population quartiles).
> The task
> For each test image, predict four things.
> target	type	meaning
> subject	categorical	which enrolled person this palm belongs to (an opaque id such as id_3f7a91c05b2e), or unenrolled
> element	categorical	the chiromantic elemental type of the hand in the image: earth, air, water or fire
> digit_band	ordinal 0,1,2,3	the 2D:4D band of the hand in the image; 0 = lowest quartile, 3 = highest
> contra_element	categorical	the elemental type of the same person's other hand — the one you were never shown
> Data
> The dataset is five items — two image folders and three CSV files. Each is described below,
> with the exact columns of every CSV.
> 1. train_images/ — 916 JPEG palm photographs, one per training row, each named <item_id>.jpg
> (colour JPEG, longest side 400 px, a single palm on a plain background). These are the gallery.
> 2. train.csv — 916 rows, the labels for the gallery images. It has exactly five columns:
> item_id — string, e.g. palm_9f3c1e7a55b0d284; matches the file train_images/<item_id>.jpg.
> subject — string, e.g. id_3f7a91c05b2e; the opaque person id of this gallery palm.
> element — string, one of earth, air, water, fire (the elemental type of this hand).
> digit_band — integer 0, 1, 2 or 3 (this hand's 2D:4D quartile).
> contra_element — string in {earth, air, water, fire} (the elemental type of this person's
> other hand).
> 3. test_images/ — 913 JPEG palm photographs (same format), each named <item_id>.jpg. These
> are the palms you must make predictions for.
> 4. test.csv — 913 rows, one column only: item_id — exactly the rows you must predict
> (one per file in test_images/). No labels are given here.
> 5. sample_submission.csv — 913 rows, a valid, correctly-formatted non-ML baseline submission.
> Its columns are the five submission columns: item_id, pred_subject, pred_element,
> pred_digit_band, pred_contra_element (format defined under Submission format).
> How the 184 subjects are split. The 184 people in the corpus are divided into two disjoint
> pools. 101 "enrolled" subjects have one hand (the gallery hand) in train_images / train.csv
> and their opposite hand in the test set; their test images are the 501 identity rows. The
> remaining 83 "novel" subjects appear only in the test set — one hand each — as the 412
> chiromancy rows. So train.csv contains 101 distinct subject ids (your enrolled gallery), and
> the 913 test images = 501 identity + 412 chiromancy. You are not told which test image is which.
> Gallery structure — multiple images per subject. A subject is not a single image. Each enrolled
> subject contributes several gallery photographs of the same (gallery) hand — up to 10 each (median
> 10), 916 in total across the 101 subjects — so the same subject id recurs on many train.csv
> rows. Their opposite hand then appears as several probe photographs — up to 5 each (median 5), 501
> in total (the identity rows). Each novel subject likewise contributes up to 5 test photographs
> (median 5) of one hand, 412 in total (the chiromancy rows). So subject is a group label over rows,
> not a per-row key: identification means matching a probe photograph to the enrolled id whose ~10
> gallery photographs (of the other hand) it belongs to.
> Submission format
> A CSV with exactly these five columns, one row per item_id in test.csv:
> item_id,pred_subject,pred_element,pred_digit_band,pred_contra_element
> palm_9f3c1e7a55b0d284,id_3f7a91c05b2e,earth,2,water
> palm_1b7d40ae9c236f15,id_a04c72e19d5b,water,0,water
> palm_4e82c5d1730ab9f6,unenrolled,fire,3,earth
> pred_element and pred_contra_element must each be one of earth, air, water, fire.
> pred_digit_band must be an integer in {0,1,2,3}, filled for every row. pred_subject may be any
> enrolled id or the literal unenrolled. Extra columns, missing rows, duplicate item_ids and
> out-of-range values are all rejected.
> How you are scored — Bimanual Chiromantic Fidelity (BCF)
> Test rows fall into two scored groups, recorded in the answer key (as introduced under Data):
> the 501 identity rows (the held-out opposite hands of the 101 enrolled subjects) are scored only
> on subject; the 412 chiromancy rows (the 83 novel subjects) are scored only on element,
> digit_band and contra_element. That split is fixed by construction; you are not told which group
> a given test row is in, so you must predict all four targets for every row. The identity metric uses
> K = 101 enrolled identities.
> Four skills, each chance-corrected so that guessing earns nothing, then fused.
> 1. subject — chance-corrected identification accuracy, over the identity rows:
> accuracy = fraction of enrolled probes whose predicted id is correct
> skill    = (accuracy - 1/K) / (1 - 1/K)          K = number of enrolled identities
> 2. element and contra_element — Cohen's kappa, over the chiromancy rows. With p_o the
> observed agreement and p_e the agreement expected by chance,
> p_e   = sum over the four types t of  P(pred = t) * P(true = t)
> kappa = (p_o - p_e) / (1 - p_e)
> where P(pred = t) and P(true = t) are the observed frequencies of type t in your submission
> and in the answer key.
> 3. digit_band — quadratic weighted kappa, over the chiromancy rows. With O[i][j] counting
> rows of true band i predicted as j, w[i][j] = (i-j)^2 / 9, and E the outer product of O's
> row and column totals rescaled to O's total:
> QWK = 1 - ( sum_ij w[i][j]*O[i][j] ) / ( sum_ij w[i][j]*E[i][j] )
> A two-band miss is charged four times a one-band miss, so being close counts.
> 4. Fusion. Each skill is clipped to [0, 1] and the four are combined by their geometric mean:
> CORE  = ( s_subject * s_element * s_digit_band * s_contra_element ) ** (1/4)
> score = 0.014 + 0.986 * CORE
> The geometric mean makes all four mandatory — solve identification brilliantly but ignore the
> chiromantic targets and your score still collapses. There is deliberately no margin subtraction
> and no rescaling of the skill range: the score is a direct function of the four measured skills.
> Score range: [0.014, 1.0]. The minimum attainable score is 0.014, not 0 — that floor is a
> fixed additive term so the non-ML baseline scores a non-zero value. A submission equal to the answer
> key scores exactly 1.0. Because every skill is chance-corrected, a constant submission scores
> exactly the floor, and a random one scores the floor in the large majority of draws.
> Provenance and grounding
> The imagery is real observational data. These are photographs of the hands of 184 adult
> volunteers, captured under a controlled protocol — palm to the camera, plain background, roughly
> constant camera distance — as part of a published, peer-reviewed research corpus of human hand
> images. Every person in the collection was photographed on both hands, which is what makes the
> identity and contralateral questions possible at all. Nothing here is synthetic, generated,
> simulated or scraped, and no image was altered beyond downscaling and re-encoding.
> The labels are measured, not asserted. For every photograph, 21 hand landmarks were detected and
> three scale-invariant proportions computed — palm elongation (palm height ÷ palm breadth), relative
> finger length (mean finger length ÷ palm breadth), and the 2D:4D ratio (index length ÷ ring length).
> Each hand's label uses the median across all of its photographs, so pose and finger-spread noise
> is averaged out.
> Three independent checks say the measurements are sound rather than merely plausible:
> check	result	expected
> 2D:4D distribution	mean 0.983, sd 0.037	published human norm ≈ 0.95 mean, ≈ 0.04 sd
> middle finger longest of the four	95–100% of hands	anatomically near-universal
> detected handedness vs. recorded hand	99.5% agreement	should be near-perfect
> Grounding of the two chiromantic constructs.
> The 2D:4D digit ratio is an established morphometric in the biological literature, introduced
> as a quantitative marker by Manning, Scutt, Wilson & Lewis-Jones (1998), "The ratio of 2nd to 4th
> digit length", Human Reproduction 13(11), and the subject of a large subsequent literature. It is
> used here purely as a measured proportion of the hand.
> The four-element hand taxonomy (square vs. elongated palm × short vs. long fingers) is the
> modern systematisation of the morphological hand-typing set out in Cheiro, "Cheiro's Language of
> the Hand" (1897) and W. G. Benham, "The Laws of Scientific Hand Reading" (1900), whose seven-type
> schemes classify hands by exactly these palm-and-finger proportions. This challenge adopts the
> geometry of that tradition and nothing else: the type is assigned by the stated rule from
> measured proportions, and no predictive claim about any person is made or scored.
> What is adapted, and what is new. Existing hand-image benchmarks pose same-hand biometric
> matching — enrol a hand, then match more photographs of that same hand — alongside demographic
> attribute prediction. This challenge deliberately departs from both: identification here is
> cross-hand (the gallery holds only a person's other hand), the demographic attributes are
> excluded from the data entirely, and two morphometric targets plus a contralateral target are
> introduced that prior benchmarks on this kind of imagery do not define.
> Notes on the data
> A person's two hands are correlated but not identical, which is what makes the contralateral
> target non-trivial: simply predicting the other hand's type to equal the shown hand's is a
> reasonable baseline, and it is beaten by genuinely modelling the relationship. Measured bilateral
> correlations are r ≈ 0.42 for palm elongation, r ≈ 0.49 for 2D:4D and r ≈ 0.81 for finger length.
> Labels are computed from landmark geometry aggregated over several photographs of each hand, so a
> single image is a slightly noisy view of its own label. This is a real property of the problem.
> Some subjects wear rings. The flag is not provided, and jewellery cannot help identification
> across hands, but it is present in the imagery.
> Rules
> 1. Rule-based, heuristic and hand-authored solutions — PROHIBITED
> Your solution must be a model LEARNED from the provided training data. Not permitted as the
> solution:
> hand-written pixel or geometry rules and thresholds (e.g. "if the palm is taller than N pixels,
> predict water");
> hand-authored decision lists, lookup tables or if/else cascades;
> manually tuned per-class priors or band cut-points chosen by inspecting the labels;
> always emitting a constant answer (this is the provided baseline, and the chance-corrected metric
> scores it at the floor);
> any pipeline whose predictions would be unchanged if the training labels were shuffled.
> Pretrained backbones, landmark detectors, hand-crafted geometric descriptors and classical CV
> features are all fine as features. The decision must be the model's.
> 2. External retrieval — PROHIBITED
> reverse-image-searching a palm, or querying any external database or search tool to identify a
> photograph or a person;
> obtaining any external copy of the underlying imagery and joining it to the provided items;
> attempting to de-anonymise item_id or subject back to a source record or a real person.
> 3. Reverse-engineering the preparation — PROHIBITED
> reconstructing or inverting the enrolled/novel pool assignment, the anonymisation, or the split;
> fitting to artefacts of item_id hashing, file ordering or JPEG encoding metadata rather than to
> the hand;
> attempting to recover which test rows belong to which scored block in order to game the metric.
> 4. Test-set abuse — PROHIBITED
> training on, or hand-labelling, any part of the test set;
> probing the leaderboard to fit the private key;
> per-row manual overrides of model output.
> 5. Not prohibited (use freely)
> any learned model — CNNs, vision transformers, metric-learning and re-identification losses,
> fine-tuned pretrained backbones, gradient boosting on image or landmark features, ensembles;
> pretrained weights and off-the-shelf hand-landmark detectors as feature extractors;
> transductive use of the unlabelled test images (self-training, pseudo-labelling, test-time
> augmentation, clustering test rows by identity);
> modelling the four targets jointly and exploiting their correlations — in particular, the
> relationship between a hand and its partner;
> cross-validation, calibration, class re-weighting and any data augmentation.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Diatomic Orbital Image Multi-Task Inversion

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72945qwhfjv1mqdqazxvfjd188pfzv
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: image, Dataset source is visible after the challenge closes.
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Every chemical bond between two atoms is governed by quantum mechanics: the way electrons distribute themselves in space determines whether a material conducts electricity, how strongly it interacts with light, and how it behaves under pressure. Computational chemists routinely predict these properties by solving the Schrödinger equation numerically — but the reverse question is rarely posed: can you reconstruct the quantum fingerprint of a bond just by looking at the electron density images it produces?
> The dataset, which contains diatomic element–element pairs simulated with the DFTB+ tight-binding DFT package. For each pair, a set of orbital population images was rendered from the simulation output. Each image is a 10-channel 32×32 float tensor where every channel captures a physically distinct aspect of the electronic structure (see Dataset section for the full channel legend). These images encode rich structural information — bonding geometry, charge transfer, orbital hybridisation — but in a format that is not directly human-readable.
> The challenge runs in the inverse direction of conventional quantum ML: instead of predicting scalar properties from images (the standard benchmark task), participants receive scalar quantum descriptors and must recover or reason about the images that generated them. This tests whether models have truly learned the physics encoded in the orbital images, or merely statistical correlations.
> The dataset covers four interaction regimes — covalent, polar-covalent, ionic, and metallic — derived from Mulliken charge asymmetry (Δq) and the electronic band gap (E_g) using DFTB-derived thresholds:
> | Regime | Condition |
> | ----- | ----- |
> | Metallic | E_g < 0.05 eV |
> | Ionic | Δq ≥ 0.80 e |
> | Polar-covalent | 0.30 e ≤ Δq < 0.80 e, E_g ≥ 0.05 eV |
> | Covalent | Δq < 0.30 e, E_g ≥ 0.05 eV |
> Tasks
> Task A — Cross-modal Retrieval (40%). Given a scalar descriptor query (band gap, dipole, charge asymmetry, regime), rank a shuffled gallery of orbital images to find the image corresponding to that descriptor. Every descriptor query has exactly one matching gallery image. The gallery pool additionally contains distractor images that do not correspond to any descriptor query, making naive nearest-neighbour baselines unreliable.
> Task B — Descriptor Inversion (35%). Given an orbital image for a held-out element pair, predict its four scalar quantum descriptors: band gap (eV), dipole moment (Debye), Mulliken charge asymmetry (e), and interaction regime. No element identity or geometry is provided — only the image.
> Task C — λ-Recovery (25%). Given a linearly blended orbital image — a convex combination of two anchor images at weight λ — together with both anchors' descriptor vectors, predict the scalar mixing coefficient λ. True λ values are sampled from the open interval (0.1, 0.9). This tests whether models learn a metrically consistent latent geometry rather than simply memorising channel statistics.
> Overall leaderboard score:
> 0.40 × Score(A) + 0.35 × Score(B) + 0.25 × Score(C)
> All component scores are in [0, 1]; higher is always better.
> Dataset
> File layout
> public/
> train.npz                  — pairs of images + descriptors
> gallery.npz                — descriptor queries, no images (pair_id prefix starts with 'gl_')
> gallery_images.npz         — shuffled image pool: true matches + distractors (slot_id prefix starts with 'sl_')
> inversion_queries.npz      — images only, descriptors withheld (pair_id prefix starts with 'iv_')
> interpolation_queries.npz  —  blended images + anchor descriptors, λ withheld (query_id prefix starts with 'iq_')
> sample_submission.csv      — correctly formatted stub for all three tasks
> Image channel legend
> Each pair's orbital image is a 10-channel 32×32 float32 tensor. The ten channels are:
> | Channel | Symbol | Description |
> |---|---|---|
> | 0 | s-pop | s-orbital electron population (ℓ = 0) |
> | 1 | p-pop | p-orbital electron population (ℓ = 1, summed over m) |
> | 2 | d-pop | d-orbital electron population (ℓ = 2, summed over m) |
> | 3 | ang-s | Angular field transform of the s-channel — encodes angular anisotropy |
> | 4 | ang-p | Angular field transform of the p-channel |
> | 5 | ang-d | Angular field transform of the d-channel |
> | 6 | cooc-sp | s–p co-occupancy map — joint electron presence in s and p orbitals |
> | 7 | cooc-pd | p–d co-occupancy map — joint electron presence in p and d orbitals |
> | 8 | chg-proj | Charge-density projection onto the internuclear axis |
> | 9 | chg-perp | Charge-density projection perpendicular to the internuclear axis |
> All images in public files are per-channel z-score normalised using statistics derived from the training split only. Raw pixel values from the original simulation are not recoverable without those statistics.
> Loading the data
> import numpy as np
> train = np.load("train.npz", allow_pickle=True)
> images       = train["images"]        # [N_train, 10, 32, 32] — normalised float32
> pair_id      = train["pair_id"]       # [N_train] — opaque hex strings, e.g. "tr_3f8a1c..."
> band_gap_ev  = train["band_gap_ev"]   # [N_train] — electronic band gap, eV
> dipole_debye = train["dipole_debye"]  # [N_train] — dipole moment magnitude, Debye
> charge_delta = train["charge_delta"]  # [N_train] — Mulliken charge asymmetry |Δq|, e
> regime       = train["regime"]        # [N_train] — one of the four regime strings above
> Task A query and gallery files:
> gallery      = np.load("gallery.npz",        allow_pickle=True)
> gallery_imgs = np.load("gallery_images.npz", allow_pickle=True)
> query_ids    = gallery["pair_id"]       # descriptor queries — no images provided
> band_gap_ev  = gallery["band_gap_ev"]
> dipole_debye = gallery["dipole_debye"]
> charge_delta = gallery["charge_delta"]
> regime       = gallery["regime"]
> pool_images  = gallery_imgs["images"]   # [N_pool, 10, 32, 32] — true + distractor images
> slot_ids     = gallery_imgs["slot_id"]  # [N_pool] — submit these ids in your ranked list
> Task B inversion queries:
> inv     = np.load("inversion_queries.npz", allow_pickle=True)
> images  = inv["images"]    # [N_inv, 10, 32, 32] — predict descriptors from these
> pair_id = inv["pair_id"]   # [N_inv]
> Task C interpolation queries:
> interp  = np.load("interpolation_queries.npz", allow_pickle=True)
> query_id      = interp["query_id"]          # [N_interp]
> blended_image = interp["blended_image"]     # [N_interp, 10, 32, 32] — the λ-blended image
> # Both anchor descriptor vectors are provided:
> anchor_a_band_gap_ev  = interp["anchor_a_band_gap_ev"]
> anchor_a_dipole_debye = interp["anchor_a_dipole_debye"]
> anchor_a_charge_delta = interp["anchor_a_charge_delta"]
> anchor_a_regime       = interp["anchor_a_regime"]
> anchor_b_band_gap_ev  = interp["anchor_b_band_gap_ev"]
> anchor_b_dipole_debye = interp["anchor_b_dipole_debye"]
> anchor_b_charge_delta = interp["anchor_b_charge_delta"]
> anchor_b_regime       = interp["anchor_b_regime"]
> # λ is withheld — predict it.
> Evaluation
> Task A — Cross-modal Retrieval
> For each descriptor query, the submission provides a ranked list of up to 10 slot_id values. The grader checks whether the correct slot appears in the top-1, top-5, and top-10 positions.
> Hit@k = (number of queries whose correct slot_id appears in the top-k predictions) / (total queries)
> Score(A) = (Hit@1 + Hit@5 + Hit@10) / 3
> Each Hit@k value is in [0, 1]; Score(A) is their simple average.
> Task B — Descriptor Inversion
> For the three continuous descriptors (band gap, dipole moment, charge asymmetry), a normalised MAE is computed per property and averaged.
> For each property p:
> range(p) = max(true value of p across the answer set) − min(true value of p across the answer set)
> norm_range(p) = the max of: range(p), or a fixed minimum floor for that property
> band_gap_ev floor = 0.10
> dipole_debye floor = 0.50
> charge_delta floor = 0.05
> normMAE(p) = MAE(p) / norm_range(p), then capped at a maximum of 1.0
> ContScore = 1 − (normMAE(band_gap_ev) + normMAE(dipole_debye) + normMAE(charge_delta)) / 3
> Regime prediction is scored by simple accuracy:
> RegimeAccuracy = (number of queries with correctly predicted regime) / (total queries)
> Score(B) = 0.5 × ContScore + 0.5 × RegimeAccuracy
> Note: the floor values above mean the normaliser is not always the raw answer-set range — if the true values for a property happen to span a narrow range in the held-out split, the floor is used instead, which can make normMAE noticeably smaller than the raw-range formula alone would suggest.
> Task C — λ-Recovery
> True λ values are sampled uniformly from the open interval (0.1, 0.9) by construction, giving a maximum possible range of 0.8.
> Score(C) = the max of: 0, or 1 − (MAE(λ) / 0.8)
> Note: while true λ values lie strictly between 0.1 and 0.9, submitted predictions are accepted anywhere in the closed range [0.1, 0.9] inclusive — a prediction of exactly 0.1 or 0.9 is valid and will not be rejected.
> Submission Format
> Submit a single submission.csv with three columns ( task, query_id, prediction) and one row per query across all tasks. The total row count equals N_gallery + N_inv + N_interp.
> task,query_id,prediction
> A_retrieval,gl_3f8a1c...,sl_9b2d44|sl_7c1e09|sl_4a8f23|sl_002b11|sl_ff8830|...
> A_retrieval,gl_02bc7f...,sl_7c1e09|sl_9b2d44|sl_3f8a1c|...
> B_inversion,iv_a1d034...,0.3400|1.1200|0.4500|polar-covalent
> B_inversion,iv_ff2201...,2.1000|0.0400|0.1200|covalent
> C_lambda,iq_5e7b12...,0.3300
> C_lambda,iq_9c3a07...,0.7100
> Task A rows: Each row corresponds to a query_id taken from gallery["pair_id"] (formatted as gl_...). The prediction field must contain a pipe-separated |) ranked list of slot_id values from gallery_images["slot_id"] (formatted as sl_...), ordered from best match to worst match, with a maximum of 10 entries.
> Task B rows: prediction is a pipe-separated string of exactly four values in the order band_gap_ev|dipole_debye|charge_delta|regime. Floats must be rounded to 4 decimal places and non-negative. regime must be one of covalent, polar-covalent, ionic, metallic.
> Task C rows: prediction is a single float in [0.1, 0.9] (inclusive), rounded to 4 decimal places.
> Submissions with missing query_id values, malformed prediction strings, invalid regime values, or negative floats will be rejected automatically.
> Submission Validation
> Before scoring, the grader runs the following checks. Any violation raises an error and rejects the submission outright — there is no partial credit for a row that fails validation.
> Global checks (all tasks)
> Submission must contain exactly the columns task, query_id, prediction.
> Every task value must be one of the known task labels (A_retrieval, B_inversion, C_lambda). Unknown labels are rejected.
> No duplicate (task, query_id) pairs anywhere in the file.
> Every query_id present in the answer key must appear in the submission (no missing rows). Extra rows beyond what's required are allowed and simply ignored.
> Task A — A_retrieval
> prediction cannot be missing/blank.
> Must be a |-separated list of slot_id values, trimmed of whitespace.
> The list cannot be empty (e.g. "" or whitespace-only).
> No blank entries between pipes (e.g. sl_001||sl_002 is invalid).
> Maximum of 10 entries per row.
> All entries within a single row's list must be unique — duplicate slot_ids in the same ranked list are rejected.
> Task B — B_inversion
> prediction cannot be missing/blank.
> Must contain exactly 4 |-separated fields (exactly 3 pipe characters) — no more, no fewer.
> The first three fields (band_gap_ev, dipole_debye, charge_delta) must each parse as a finite, non-negative number (not NaN, not ±inf, not negative).
> The fourth field (regime), after trimming whitespace, cannot be blank and must be exactly one of: covalent, polar-covalent, ionic, metallic.
> Task C — C_lambda
> prediction cannot be missing/blank.
> Must parse as a finite number (not NaN, not ±inf).
> Must fall within [0.1, 0.9] inclusive, and any value outside that band is rejected.
> If any of these checks fail, the grader raises a descriptive error identifying the offending query_id/row and the specific rule violated, and no score is computed for that submission.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Text-Conditioned CT Slice Region Localization

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74q80qybd0are8s2gdhvb6y98a4p5a
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: image, segmentation, medical, 3d-medical, multimodal, text, Dataset source is visible after the challenge closes.
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Given one 2D CT slice crop and a natural-language prompt, predict the location of the anatomical or abnormal region referred to by the prompt. Each prompt asks for one visible target region, such as a calcification focus, fluid collection, organ region, lung abnormality, vessel finding, implant-related region, or other CT-visible structure. The same slice can contain several plausible regions, so the answer must be conditioned on both the image and the text.
> The records are derived from 3D CT volumes with paired text references and segmentation masks. For this challenge, each volume-mask pair is converted into the 2D slice where the referred region is visible, then compressed to a 20 by 20 grid. The prediction is a compact localization ledger: which grid cells contain the referred region, which cells lie on its outline, and which target cells are closer to the boundary or deeper in the 2D region interior.
> This is a text-conditioned medical visual grounding task. A generic organ foreground mask is not enough; the model must use the prompt to decide which CT finding or anatomical region is being requested.
> Dataset
> Files:
> train.csv: 700 labeled prompted CT slices.
> test.csv: 400 unlabeled prompted CT slices.
> sample_submission.csv: 400-row valid baseline.
> images/: PNG CT slice crops referenced by the CSV files.
> Columns:
> id (string): Opaque row id.
> image_path (string): Relative path to the PNG slice.
> prompt (string): Natural-language phrase identifying the CT region to recover.
> answer_format_json (JSON object): Required output shape and allowed values.
> answer_json (JSON object, train only): Ground-truth prompt-conditioned region ledger.
> Required JSON fields:
> grid_shape (JSON list of integers): Always [20, 20].
> target_region_cells (JSON list of integers): Length-400 row-major binary grid. A value of 1 means the cell contains the prompted target region; 0 means it does not.
> edge_bins (JSON list of integers): Length-400 row-major boundary grid. 0 means no prompted-region boundary is assigned to the cell. Values 1, 2, and 3 are nonzero boundary bins for the target region outline, with larger values representing stronger or more complex local boundary contact after downsampling.
> depth_bins (JSON list of integers): Length-400 row-major 2D interior-distance grid. This is not physical scanner depth. 0 means outside the prompted region. Values 1 through 5 are coarse bins for target cells, from near the outline to deeper inside the region on the slice.
> Row-major order means the array starts at the top-left grid cell, moves left to right across the first row, then continues row by row to the bottom-right cell.
> Submission Format
> Submit exactly two columns, id and answer_json.
> id,answer_json
> example_row,"{""grid_shape"":[20,20],""target_region_cells"":[0,0,1],""edge_bins"":[0,1,1],""depth_bins"":[0,0,2]}"
> The example is abbreviated; all three arrays must be length 400 in real submissions.
> Evaluation
> The grader enforces strict JSON, exact id matching, valid integer bins, grid_shape = [20, 20], and complete array lengths. Invalid or incomplete rows are rejected.
> For target_region_cells, the grader computes binary foreground IoU:
> IoU(P, T) = intersection(P, T) / union(P, T)
> where P is the set of cells predicted as 1 and T is the set of true target cells. If both sets are empty, the IoU is defined as 1.0. The target-region component is:
> target_region_cells_score = IoU(P, T)^2
> For edge_bins and depth_bins, the grader computes active-bin macro IoU over nonzero labels. For each nonzero value v that appears in either the prediction or the truth, it forms two binary sets: cells predicted exactly as v and cells truly labeled exactly as v. It computes binary IoU for that value, then averages those IoUs across active nonzero values. If no nonzero value appears in either prediction or truth, the macro IoU is 1.0.
> field_score = active_bin_macro_IoU^2
> The square is intentional: near-miss masks receive partial credit, but the metric rewards precise localization more strongly than loose overlap.
> The row score is:
> row_score = 0.50 * target_region_cells_score + 0.28 * edge_bins_score + 0.22 * depth_bins_score
> The final score is the mean row score. Scores are bounded between 0 and 1.
> What Not To Use
> Do not use unreleased masks, reports, metadata, answer files, or generation artifacts.
> Do not use row-order shortcuts, hardcoded ids, or manual lookup of held-out CT slices.
> Do not submit mask images or any file outside the required JSON-in-CSV format.
> Do not use external datasets, hosted inference APIs, runtime package installs, vendored or downloaded code, private/gated assets, challenge-specific pretrained checkpoints.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Image And DNA-Guided Insect Taxonomic Hierarchy Prediction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a77969yzb888ayhdxgwcx2n8arzff
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: image, Based on dataset:, BIOSCAN-30k DNA-Barcoded Insect Image Source Subset, Download Data
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> For each test specimen, submit:
> taxon_path_json: a JSON object with keys phylum, class, order, family, subfamily, genus, and species. Fill ranks only down to the supported depth and leave lower ranks as empty strings.
> support_state: one of order_supported, family_supported, subfamily_supported, genus_supported, or species_supported.
> confidence: a finite value in [0,1] estimating whether both the submitted path and support state are exactly correct.
> The path and support state must be consistent and must correspond to one path/rank pair in that row's candidate_paths_json. Abstention at phylum or class is not part of this task: all scored specimens are insects in Arthropoda/Insecta, and the safest supported claim always starts at order. For example, a family_supported answer should contain phylum, class, order, and family, with subfamily, genus, and species left blank.
> Intended Approach
> Treat this as a GPU-enabled multimodal structured-prediction task with selective abstention and calibrated confidence. The required output is a jointly consistent taxonomic path, support depth, and confidence, so this is neither regression nor ordinary flat classification. Use only the released training data and labels.
> What Not To Use / What Not To Do
> Do not recover original upstream specimen files, raw specimen identifiers, raw filenames, raw DNA barcode strings, source-database records, collection metadata, or hidden labels by lookup. Do not match prepared images or barcode sketches back to public upstream records. Do not use row order, file size, image path strings, salted IDs, mtimes, geography, private files, grader internals, or malformed JSON behavior as answer channels. Do not submit a DNA-only lookup table, image-only single-head labeler, fixed template, hosted vision/genomics API, runtime internet search, runtime-downloaded pretrained weights, or closed-source teacher labels.
> Enforcement on invalid approaches: submissions may be reviewed for source lookup, external calls, metadata-only behavior, DNA-lookup behavior, fixed answer maps, private-answer access, and approaches that avoid the required hierarchy and abstention contract. The goal is learned multimodal taxonomic evidence reconciliation, not recovery of public source labels.
> Evaluation
> Each row receives four components.
> joint_exact:
> 1.0 only when both the submitted path and support_state are exactly correct,
> else 0.0.
> path_score:
> hierarchy-aware credit for the submitted taxon path.
> Correct ancestors receive partial credit.
> A correct supported-depth path receives 1.0.
> Constant phylum/class ranks receive no credit.
> Unsupported over-specific claims are multiplied by 0.25.
> state_score:
> 1.0 if support_state exactly matches the hidden supported depth,
> else 0.0. A state inconsistent with the submitted path depth receives 0.0.
> calibration:
> 1 - abs(confidence - exact),
> where exact is 1 only when both path and support_state are exactly correct.
> row_score = 0.60 * joint_exact
> + 0.25 * path_score
> + 0.10 * state_score
> + 0.05 * calibration
> Final = 0.82 * mean(row_score)
> + 0.08 * worst_depth_group(row_score)
> + 0.05 * worst_order_group(row_score)
> + 0.05 * worst_family_group(row_score)
> The hidden group terms use real private properties derived from taxonomic depth, order, and family, with sparse groups merged before scoring. Higher is better. Minimum is 0.0; maximum is 1.0. This bound is intentional: row_score and every worst-group term are each in [0,1], and the final weights 0.82 + 0.08 + 0.05 + 0.05 sum to exactly 1.00. A perfect submission has all four final terms equal to 1.0 and scores exactly 1.0.
> The grader requires exactly the listed submission columns in the listed order. Wrong columns, duplicate IDs, missing IDs, extra IDs, non-finite confidence, or confidence outside [0,1] raise InvalidSubmissionError. A path/state pair outside the row's supplied candidate roster receives zero. Row-local malformed or overlong path JSON, or an invalid support-state string, also scores zero for that affected row without leaking private labels.
> Dataset
> The prepared public corpus contains de-identified 160 x 160 JPEG specimen images, anonymized DNA barcode sketches, candidate taxonomy rosters, and training labels. Raw DNA strings, original filenames, specimen identifiers, collection geography, dates, and upstream metadata are not public inputs.
> File overview
> Item	Description
> train/images/*.jpg	Training images
> test/images/*.jpg	Test images
> train.csv	Inputs plus labels
> test.csv	Test inputs only
> sample_submission.csv	Weak template
> train.csv columns
> Column	Type	Description
> id	string	Opaque row id
> image	string	JPEG path
> barcode_sketch_json	string	DNA sketch vector
> candidate_paths_json	string	Candidate roster
> prompt	string	Task instruction
> taxon_path_json	string	Target path
> support_state	string	Target depth
> barcode_sketch_json is a JSON list of 32 integer bucket values derived from the real DNA barcode. candidate_paths_json is a JSON list of candidate objects with candidate_id, rank, and path fields. Training rows include the target path and support state.
> The train-only label columns are taxon_path_json, the hierarchy-safe target path, and support_state, the deepest supported rank for that path.
> test.csv columns
> Column	Type	Description
> id	string	Opaque row id
> image	string	JPEG path
> barcode_sketch_json	string	DNA sketch vector
> candidate_paths_json	string	Candidate roster
> prompt	string	Task instruction
> Test rows have the same public input columns as training rows and no target labels.
> In test.csv, id is the opaque row key; image is the public JPEG path; barcode_sketch_json is the anonymized DNA sketch; candidate_paths_json is the row-local candidate roster; and prompt is the shared task instruction.
> Submission
> Write the final submission CSV to exactly ./working/submission.csv. It must contain exactly these columns in this order and exactly one row for every test ID.
> Column	Type	Constraint
> id	string	Same set as test
> taxon_path_json	string	Seven-rank JSON
> support_state	string	Allowed state
> confidence	float	In [0,1]
> Example:
> id,taxon_path_json,support_state,confidence
> ibe_0123abcd9876ef,"{""phylum"":""Arthropoda"",""class"":""Insecta"",""order"":""Diptera"",""family"":""Sciaridae"",""subfamily"":"""",""genus"":"""",""species"":""""}",family_supported,0.62
> ibe_fedcba98765432,"{""phylum"":""Arthropoda"",""class"":""Insecta"",""order"":""Hymenoptera"",""family"":"""",""subfamily"":"""",""genus"":"""",""species"":""""}",order_supported,0.38
> Requirements are strict: every test ID must appear exactly once; duplicate, missing, or foreign IDs are invalid; columns must match exactly; confidence must be finite and in range; JSON strings must stay within the documented format and length limits.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Rotor-Safe Ultrasonic Notch Set Planning

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74m214b5a49nywhyap00f6cn8bnpag
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview
> Each image shows sound energy over time and frequency with eight labeled boxes. Choose up to four boxes that remove rotor noise without erasing short biological pulses. Then predict which six time intervals keep their pulses and which six rotor-frequency bands are removed.
> Ultrasonic microphones used in airborne wildlife surveys record more than biological pulses. Motors, propellers, and airflow create persistent frequency bands that can conceal short echolocation events. Removing every strong band is not a safe solution because a wide filter may erase the pulses being studied. A useful intervention must suppress platform noise, preserve transient evidence, and avoid selecting mutually overlapping filters.
> Every case includes a spectrogram board and its corresponding 250 kHz mono WAV excerpt. Eight outlined rectangles labeled A through H are possible filters: choosing a rectangle means suppressing the sound inside that frequency-time box. Two rectangles are compatible when they do not overlap too much. The three submitted outputs are therefore the chosen label set, six pulse-survival decisions, and six rotor-band coverage decisions.
> This is acoustic intervention planning. It is not species recognition, generic sound tagging, or pixel segmentation.
> Compute Budget
> Solutions run with one NVIDIA A10G GPU and a maximum wall-clock time of 30 minutes. Audio loading, preprocessing, model fitting, inference, plan search, and submission generation all count toward the limit. GPU use is allowed but not required.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `public/train.csv` | Labeled spectrogram and audio cases. |
> | `public/test.csv` | Evaluation cases with all targets withheld. |
> | `public/sample_submission.csv` | Schema-valid placeholder predictions. |
> | `public/images/` | JPEG spectrogram boards referenced by the CSV files. |
> | `public/audio/` | Corresponding 16-bit mono WAV excerpts sampled at 250 kHz. |
> The prepared release contains 1,050 training cases and 420 hidden test cases. Complete flight recordings are assigned to only one split. Public identifiers and media names do not reveal recording dates, flight identity, source offsets, or labels.
> Before the spectrogram and targets are created, each excerpt receives a deterministic sub-percent time-scale perturbation, fractional-sample displacement, mild spectral tilt, polarity and gain variation, and low-amplitude sensor noise. These changes preserve pulse and harmonic structure while preventing exact waveform matching against the published recordings.
> The training targets contain 59 distinct optimal notch sets, 61 distinct pulse-survival words, and 40 distinct rotor-coverage words.
> Spectrogram Board Layout
> Each board is a 1180 x 720 RGB JPEG. The central heatmap covers approximately 15 kHz through 115 kHz. Time increases from left to right and frequency increases from bottom to top.
> Visual elements have the following meaning:
> bright horizontal ridges indicate frequency content that persists across time;
> short localized ridges indicate transient ultrasonic events;
> rectangles A through H show the exact frequency-time support of the eight candidate notch proposals;
> labels P1 through P6 along the lower edge divide the recording into six equal chronological intervals;
> the six strongest persistent bands are ordered by increasing frequency when constructing rotor_cover_word.
> Some proposals span the complete time axis, while others cover only part of the recording. Rectangles may overlap partially or strongly. Their label color is only an identifier and does not encode quality, compatibility, or target value.
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | String | Opaque identifier matching `bn[0-9a-f]{20}`. |
> | `notch_board_path` | String path | Relative path to the labeled spectrogram JPEG generated from the transformed WAV excerpt. It contains boxes `A` through `H` and time labels `P1` through `P6`. |
> | `audio_clip_path` | String path | Relative path to the transformed WAV excerpt from which the spectrogram was produced. The WAV contains the sound signal but no proposal labels. |
> Target Columns
> | Column | Data type | Meaning and valid form |
> |---|---|---|
> | `notch_antichain` | Set string | One through four distinct proposal labels from `A` through `H`, joined by `|`. Order does not affect grading. |
> | `pulse_survival_word` | Seven-character binary string | Prefix `b`, followed by one survival bit for each interval `P1` through `P6` in chronological order. |
> | `rotor_cover_word` | Seven-character binary string | Prefix `b`, followed by one coverage bit for each of the six strongest persistent bands in ascending-frequency order. |
> For pulse_survival_word, bit 1 means the transient evidence in that interval survives the selected reference notches. For rotor_cover_word, bit 1 means at least one selected notch covers the center of that persistent band.
> Reference Filter Construction
> Proposal Compatibility
> For any two proposal rectangles, the reference computes intersection-over-union over their frequency-time area. The pair conflicts when:
> rectangle_iou > 0.28
> A valid notch_antichain contains no conflicting pair and contains between one and four proposals.
> Proposal Value And Plan Utility
> Each proposal receives a private value from three quantities visible in the supplied evidence:
> persistent-band energy removed by the rectangle;
> transient energy damaged inside the rectangle;
> normalized rectangle area.
> Transient damage is penalized more strongly than filter area. For valid proposal set P, pair overlap introduces an additional cost:
> raw_utility(P) =
> sum(proposal_value for proposals in P)
> - 0.18 * sum(pair_overlap for proposal pairs in P)
> The reference set is the highest-utility valid set among all one-through-four-proposal combinations. Exact utility ties are resolved by lexicographic proposal-label order.
> Consequence Words
> For each P1 through P6 interval, the reference compares damaged transient energy with all transient energy in that interval:
> survival_bit =
> 1 if damaged_transient_energy <= 0.14 * total_transient_energy
> 0 otherwise
> The six survival bits are concatenated after prefix b.
> The reference also identifies the six strongest persistent frequency-band centers. A rotor-coverage bit is 1 when any proposal in the reference notch set contains that center frequency, otherwise it is 0.
> Submission Format
> Write the final file to:
> ./working/submission.csv
> Use exactly these columns in this order:
> case_id,notch_antichain,pulse_survival_word,rotor_cover_word
> Example:
> case_id,notch_antichain,pulse_survival_word,rotor_cover_word
> bn0123456789abcdefabcd,A|D|H,b110101,b101110
> Submission requirements:
> Include exactly one row for every hidden case_id.
> Extra, missing, or reordered columns are rejected.
> Duplicate, missing, malformed, and unknown identifiers are rejected.
> A single backend-managed visibility column is accepted and removed.
> notch_antichain is limited to 24 characters and must contain one through four distinct valid labels.
> Each consequence word must be exactly the prefix b followed by six characters from {0,1}.
> Malformed values receive zero credit for their corresponding component.
> Evaluation
> The Ultrasonic Intervention Score combines one plan score and two consequence-word scores:
> Score =
> 0.48 * AntichainUtilityScore
> + 0.29 * PulseSurvivalScore
> + 0.23 * RotorCoverageScore
> Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> All component calculations are performed per hidden case and then averaged.
> AntichainUtilityScore
> Malformed or conflicting submitted plans receive zero for this component. For a valid plan, the grader evaluates all compatible one-through-four-proposal combinations. The private utility numbers are deterministic reference measurements of energy visible in the supplied packet; participants submit only proposal labels. Let u_min be the utility of the worst valid proposal set, u_max the utility of the best valid set, and u_pred the utility of the submitted set.
> normalized_utility =
> 1                                      if u_max equals u_min
> (u_pred - u_min) / (u_max - u_min)    otherwise
> canonical_optimum =
> 1 if the submitted set equals the hidden reference set
> 0 otherwise
> row_antichain_score =
> 0.25 * normalized_utility
> + 0.75 * canonical_optimum
> The normalization maps the valid utility range to 0 through 1: the worst valid set receives normalized utility 0, and the best receives 1. The normalized term gives limited credit to a near-optimal intervention. Most component credit requires the canonical optimal set.
> PulseSurvivalScore
> Let correct_bits be the number of matching positions among the six submitted survival bits.
> bit_accuracy = correct_bits / 6
> exact_word = 1 if all six bits match, else 0
> row_pulse_score =
> 0.28 * bit_accuracy
> + 0.72 * exact_word
> RotorCoverageScore
> The same calculation is applied to the six rotor-coverage bits:
> bit_accuracy = correctly matched coverage positions / 6
> exact_word = 1 if all six coverage bits match, else 0
> row_rotor_score =
> 0.28 * bit_accuracy
> + 0.72 * exact_word
> Expected And Allowed Methods
> Allowed approaches include audio CNNs, spectrogram transformers, compact image encoders, pulse and harmonic detectors, proposal-ranking models, interval classifiers, and exhaustive search over the bounded proposal-set space. Signal processing and pretrained audio or vision backbones may be combined within the 30-minute A10G budget.
> What Makes This Interesting
> The visually strongest rectangle is not automatically the safest filter. It may remove a useful pulse, and two individually valuable proposals may become invalid when selected together. The task therefore asks for an intervention under a geometric conflict constraint, followed by two explicit certificates of its biological and mechanical consequences. A successful model must connect localized spectrogram evidence with a globally compatible filter plan.
> What Not To Use
> Do not infer labels from IDs, filenames, CSV order, file sizes, hashes, or source offsets.
> Do not search for clips in external archives or match excerpts against complete source recordings.
> Do not use recording dates, flight identifiers, source filenames, telemetry, private proposal tables, or hidden answers during inference.
> Do not exploit duplicate rows, extra columns, overlapping-label parser behavior, oversized values, malformed sets, or grader exceptions.
> Do not train, calibrate, pseudo-label, or choose thresholds using hidden test packets.
> Reference Validation
> The packaged reference submission scores 1.0. The supplied sample submission scores 0.267606, and a constant submission built from frequent training targets scores 0.284291. Independent clean preparations produced byte-identical public and private output hashes. The grader rejects duplicate IDs, missing IDs, unknown IDs, extra or reordered columns, oversized strings, malformed sets, and malformed consequence words.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Bridge Corrosion Condition Window Profile Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73spnbxdcny4078tyn1j9qq98bjxj6
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat shikum's score of 0.316!

Full challenge description from page:

> Overview
> Bridge inspection photos often contain small, irregular corrosion regions spread across beams, fasteners, joints, and concrete-steel boundaries. In this task, each row gives a transformed inspection window and asks you to reconstruct a compact corrosion-condition profile over an 8 by 8 grid.
> For every image, predict which grid cells contain annotated corrosion, which cells correspond to fair, poor, or severe condition regions, coarse area bins for each condition state, and an eight-row vertical condition profile. The target is not a single label for the image; it is a structured record describing where corrosion appears and how the visible condition states are distributed.
> Dataset
> Files:
> train.csv: 1,108 labeled examples.
> test.csv: 467 held-out examples.
> sample_submission.csv: A weak schema example with the required columns.
> images/: 1,575 JPEG inspection windows referenced by image_path.
> Columns in train.csv:
> id (string): Row identifier.
> image_path (string): Relative path to the transformed inspection-window JPEG.
> packet_json (JSON string): Input constraints. It contains image_size as [288, 288], grid_shape as [8, 8], and condition_states as ["fair", "poor", "severe"].
> answer_json (JSON string): Ground-truth corrosion-condition profile.
> Columns in test.csv:
> id (string): Row identifier.
> image_path (string): Relative path to the transformed inspection-window JPEG.
> packet_json (JSON string): Same structure as in train.csv.
> The answer_json object has exactly these fields:
> affected_cells (array of strings): Grid cells containing any annotated corrosion. Cell tokens use rRR_cCC, for example r03_c05.
> fair_cells (array of strings): Affected cells containing fair-condition corrosion.
> poor_cells (array of strings): Affected cells containing poor-condition corrosion.
> severe_cells (array of strings): Affected cells containing severe-condition corrosion.
> area_bins (object): Integer bins from 0 to 9 for fair, poor, and severe, representing coarse annotated area for each state.
> row_condition_profile (array of 8 integers): One value per grid row. 0 means no corrosion in that row, 1 fair only, 2 poor only, 3 severe only, and 4 mixed states.
> All cell arrays must contain valid cells from the released 8 by 8 grid. The state-specific cell arrays must be subsets of affected_cells.
> Evaluation
> The score is the mean row score over the held-out test rows.
> For a set-valued field, F1 is:
> F1 = 2 * precision * recall / (precision + recall)
> with precision = |predicted intersection true| / |predicted| and recall = |predicted intersection true| / |true|. If both sets are empty, F1 is 1. If exactly one set is empty, F1 is 0.
> For each row:
> affected_score = F1(predicted affected_cells, true affected_cells).
> state_score is the mean F1 for fair_cells, poor_cells, and severe_cells.
> bin_score is the mean over fair, poor, and severe of max(0, 1 - abs(predicted_bin - true_bin) / 4).
> profile_score is the fraction of the 8 row_condition_profile positions that match exactly.
> The raw row score is:
> 0.34 * affected_score + 0.30 * state_score + 0.20 * bin_score + 0.16 * profile_score
> Malformed JSON or invalid values score 0 for that row. The submitted CSV must still have exactly the required columns, exactly one row per test id, and no missing, extra, or duplicate ids.
> After the component-weighted raw row score is computed, the grader applies a strictness transform to reduce credit for broad base-rate guesses: row_score = raw_row_score ^ 4.0. Perfect rows still score 1.0, malformed rows score 0.0, and partial rows must be close across several fields to retain substantial credit.
> Submission
> Submit a CSV with exactly two columns:
> id (string)
> answer_json (JSON string)
> Example:
> id,answer_json
> corr_example_01,"{""affected_cells"":[""r02_c03"",""r02_c04""],""fair_cells"":[""r02_c03""],""poor_cells"":[""r02_c04""],""severe_cells"":[],""area_bins"":{""fair"":2,""poor"":1,""severe"":0},""row_condition_profile"":[0,0,4,0,0,0,0,0]}"
> corr_example_02,"{""affected_cells"":[""r05_c01""],""fair_cells"":[],""poor_cells"":[],""severe_cells"":[""r05_c01""],""area_bins"":{""fair"":0,""poor"":0,""severe"":1},""row_condition_profile"":[0,0,0,0,0,3,0,0]}"
> What Not To Use
> Do not use any files outside the supplied dataset package.
> Do not use external image collections, annotation collections, search engines, or lookup services.
> Do not hard-code row ids, image names, or answers.
> Do not manually label the held-out images.
> Do not use hosted vision APIs or pretrained external checkpoints.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Biomedical Morphology Map Prediction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75cgazqa0yasmd1ngbfpsj818a6mpq
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat nsndtrai's score of 0.495!

Full challenge description from page:

> Overview
> Given one biomedical image crop, predict three dense morphology maps on a 40 by 40 grid. The maps describe where the target pattern is visible, where its transition cells occur, and the local scale bin of the pattern. This is an image-understanding task: the answer must be inferred from the PNG crop, then serialized as three aligned arrays for grading.
> The images span heterogeneous acquisition styles with different contrast profiles, anatomical scales, and bright-on-dark or dark-on-bright appearances. Across these views, target patterns can be low contrast, fragmented, or partially ambiguous. A good solution must learn visual evidence across imaging styles, then produce low-resolution maps that preserve support, transition activity, and local scale.
> This framing is deliberately different from returning a single filled region. A prediction that only marks occupied cells can lose transition and scale information; a prediction that only marks a sparse trace can miss the visible support. The scoring therefore rewards a balanced reconstruction of support, transition bins, and coarse local scale.
> Dataset
> Files:
> train.csv: 950 labeled medical image crops.
> test.csv: 449 unlabeled medical image crops.
> sample_submission.csv: 449-row valid baseline.
> images/: PNG image crops referenced by the CSV files.
> Columns:
> id (string): Opaque row id.
> image_path (string): Relative path to the PNG image.
> modality_context (string): Anonymous public imaging-style bucket such as style_group_07. These values indicate broad appearance groups only; they are not labels for the output arrays and do not identify source datasets.
> answer_format_json (JSON object): Required map schema. It contains grid_shape: [40, 40], array_order: "row_major", and a fields object listing the required length and allowed integer values for vessel_cells, edge_bins, and thickness_bins.
> answer_json (JSON object, train only): Ground-truth dense map target serialized as arrays.
> answer_json fields:
> grid_shape: [40, 40].
> vessel_cells: length-1600 row-major integers in [0, 1]. This schema field is the target-support channel: 1 means the grid cell contains visible target support; 0 means the cell is inactive.
> edge_bins: length-1600 row-major integers in [0, 1, 2, 3]. 0 means inactive. Nonzero values mark active transition cells and separate coarse transition-pattern bins, so the prediction must preserve local shape changes rather than only filled interiors.
> thickness_bins: length-1600 row-major integers in [0, 1, 2, 3, 4, 5]. 0 means inactive. Nonzero values are coarse local scale bins, with larger values corresponding to wider visible support in that grid cell.
> The arrays are aligned: index i = row * 40 + column refers to the same grid cell in all three fields.
> Submission Format
> Submit a two-column CSV: id, answer_json. The answer_json value stores the three predicted 40 by 40 maps in row-major order.
> id,answer_json
> example_row,"{""grid_shape"":[40,40],""vessel_cells"":[0,0,1],""edge_bins"":[0,1,1],""thickness_bins"":[0,0,2]}"
> The example omits most cells. Real submissions must provide complete length-1600 arrays.
> Evaluation
> The grader validates strict JSON, complete length-1600 arrays, allowed integer values, and exact id coverage. It scores each row from 0 to 1.
> For any two binary cell sets P and T over the 1600 grid cells:
> IoU(P, T) = |P intersect T| / |P union T|
> If both P and T are empty, the IoU for that binary comparison is 1.0.
> The three field scores are computed as follows:
> vessel_cells_score: Let P = {i: predicted_vessel_cells[i] = 1} and T = {i: true_vessel_cells[i] = 1}. Compute support IoU and square it: vessel_cells_score = IoU(P, T)^2.
> edge_bins_score: Let B be the set of nonzero edge-bin values that appear in either prediction or truth. For each b in B, compute IoU({i: predicted_edge_bins[i] = b}, {i: true_edge_bins[i] = b}). Average those IoUs over B, then square the average. If B is empty, the unsquared macro IoU is 1.0.
> thickness_bins_score: Use the same active-bin macro IoU procedure as edge_bins_score, but with nonzero thickness-bin values 1 through 5. The macro IoU is squared after averaging.
> The row score is:
> row_score = 0.46 * vessel_cells_score + 0.30 * edge_bins_score + 0.24 * thickness_bins_score
> The leaderboard value is the mean row_score across all evaluated rows, bounded from 0 to 1. Squaring is applied to each completed field score before the weighted row formula, so near misses receive partial credit but diffuse, overfilled, or sparse-only predictions are penalized.
> The metric is intentionally geometry-focused: inactive-cell predictions score poorly because support cells and active nonzero geometry bins drive the IoU terms.
> What Not To Use
> Do not use unreleased target arrays, labels, metadata, answer files, or generation artifacts.
> Do not use row order, hardcoded ids, or hidden labels outside the released files.
> Do not submit auxiliary images or files outside the required CSV.
> Do not use external datasets, hosted inference APIs, runtime package installs, vendored or downloaded code, private/gated assets, challenge-specific pretrained checkpoints.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Satellite Change Detection with Sensor Fault Diagnosis

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx755qsh2cx7vtq32gcv1vky9s8b2xh0
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat morax's score of 0.738!

Full challenge description from page:

> Overview
> Satellite change maps are used to monitor urban expansion, damaged infrastructure, flooding,
> deforestation, and other changes to the Earth's surface. In practice, images collected before and
> after an event often come from different sensors. Their appearance can differ because of
> illumination, radiometric calibration, spatial registration, atmospheric conditions, or an
> incorrect source tile.
> You are given four registered views of the same derived geographic scenario:
> a pre-event optical image;
> a post-event SAR image;
> a raw post-event optical image;
> a claimed corrected post-event optical image produced by an upstream processing pipeline.
> The claimed corrected image is not always trustworthy. It may be clean, radiometrically distorted,
> spatially misregistered, or associated with incompatible image content.
> For every example, your model must:
> Estimate the true amount of physical change in each cell of a 4 x 4 spatial grid.
> Diagnose the state of the claimed corrected image.
> Recover the translation needed to repair a registration failure.
> Recover the channel-wise affine correction needed to repair a radiometric failure.
> This is not ordinary pairwise change segmentation. A successful model must distinguish real
> surface change from sensor disagreement, diagnose why one piece of evidence is inconsistent, and
> continue estimating change when the claimed optical product cannot be trusted.
> What the Task Requires
> Solving an example well exercises four related capabilities:
> Cross-sensor representation: compare optical and SAR observations whose pixel values have different physical meanings.
> Evidence auditing: decide whether disagreement is caused by real land change, radiometric distortion, registration error, or incompatible content.
> Spatial change recovery: estimate where physical change occurred without treating every visual difference as a true event.
> Corrective inference: estimate repair parameters for the faulty observation rather than only assigning it a class label.
> The SAR and raw optical observations provide independent post-event evidence. Models must reason
> across all four inputs instead of relying exclusively on the claimed corrected image.
> Data Provenance
> The challenge is derived from openly licensed, registered multi-sensor remote-sensing imagery
> containing pre-event optical observations, post-event SAR observations, post-event optical
> products, and manually prepared change annotations.
> Every source crop is assigned to a buffered geographic block before derived scenarios and audit
> conditions are created. Overlapping source scenes use the same geographic block system. Both the
> base and donor content for an example remain inside one block, and no block appears in both train
> and test. Original filenames, geographic coordinates, scene names, acquisition identifiers, crop
> positions, and unchanged source images are not released.
> The released examples contain transformed, composited, and re-encoded observations with opaque
> identifiers. The physical-change targets describe controlled cross-sensor changes in these derived
> scenarios and are not unchanged copies of public source annotations. Attribution and licensing
> information for the upstream collection is provided separately in the dataset documentation.
> File Structure
> The public challenge data contains:
> train.csv - training identifiers, array indices, diagnostic labels, repair targets, and 4 x 4 change-grid targets.
> test.csv - test identifiers and array indices without targets.
> train_images.npz - the four input image tensors for training examples.
> test_images.npz - the four input image tensors for test examples.
> sample_submission.csv - a complete, varied submission-format example.
> metric_config.json - public class priors, normalization scales, target means, and metric constants used by the grader.
> Each NPZ file contains:
> pre_optical - pre-event optical patches.
> post_sar - post-event SAR patches.
> post_optical_raw - raw post-event optical patches.
> post_optical_claim - candidate corrected post-event optical patches to be audited.
> Each tensor has shape [number_of_examples, 64, 64, 3]. The row selected by input_index in the
> corresponding CSV identifies the matching row in all four tensors.
> Images are stored as unsigned 8-bit arrays. Convert them to floating point and apply training-only
> normalization when appropriate.
> Features
> train.csv and test.csv contain:
> id - opaque unique example identifier.
> input_index - row index into the corresponding NPZ arrays.
> All four images describe the same nominal derived scenario. However, the claimed corrected optical
> image may contain an audit fault. Natural differences between sensors, resampling artifacts, and
> observation noise remain part of the problem.
> Diagnostic Targets
> train.csv contains fault_type, with one of four values:
> clean - the claimed corrected optical image is usable.
> radiometric - its channel intensities require an affine correction.
> registration - its spatial position requires translation.
> content_swap - some or all of the claimed content is incompatible with the other observations and cannot be repaired by one global affine or translation transform.
> Participants submit probabilities for all four diagnostic states.
> Repair Targets
> Training rows also contain:
> shift_x - horizontal translation to apply to the claimed image, expressed as a fraction of patch width.
> shift_y - vertical translation to apply to the claimed image, expressed as a fraction of patch height.
> Positive shift_x moves image content to the right. Positive shift_y moves image content downward.
> The radiometric repair targets are:
> gain_r, gain_g, gain_b;
> bias_r, bias_g, bias_b.
> Image intensities are interpreted on the range [0, 1]. For channel c, the repair convention is:
> repaired_c = gain_c * claimed_c + bias_c
> Translation targets are evaluated only for registration examples. Gain and bias targets are
> evaluated only for radiometric examples. The conventional identity values for other rows are zero
> translation, unit gain, and zero bias.
> Change Targets
> Every image patch is divided into a 4 x 4 grid. Each cell covers a 16 x 16 pixel region.
> The sixteen targets are named:
> change_00 through change_03;
> change_10 through change_13;
> change_20 through change_23;
> change_30 through change_33.
> The first digit is the grid row and the second digit is the grid column. Each target is the fraction
> of pixels in that cell affected by the controlled physical-change scenario. Values lie in [0, 1].
> Participants must predict continuous change fractions, not thresholded binary labels.
> Evaluation
> The score combines change recovery, fault diagnosis, and repair accuracy.
> All priors, baseline predictions, and normalization scales described below are supplied in
> metric_config.json. They are computed from the training split, fixed before scoring, and are not
> recomputed from a submission.
> Change Skill
> Let y_ic be the true change fraction and p_ic the predicted fraction for example i and grid cell c.
> E_change = mean over i,c of (p_ic - y_ic)^2
> Let mean_change_c be the public training-mean prediction for cell c.
> B_change = mean over i,c of (mean_change_c - y_ic)^2
> The change skill is:
> S_change = clip(1 - E_change / B_change, 0, 1)
> Fault Diagnosis Skill
> Let q_ik be the submitted probability for fault class k, and let z_i be the correct class.
> Every submitted probability must be finite and non-negative, and every row must have a strictly
> positive probability sum. Valid rows are normalized to sum to one and then clipped to
> [1e-15, 1] for the logarithm.
> E_fault = -mean over i of log(q_i,z_i)
> Let prior_k be the public training fault-class prior.
> B_fault = -mean over i of log(prior_z_i)
> The diagnostic skill is:
> S_fault = clip(1 - E_fault / B_fault, 0, 1)
> Registration Repair Skill
> Let R be the test examples whose true fault type is registration. The two translation dimensions
> are normalized by the public scales scale_shift_x and scale_shift_y.
> E_shift = mean over i in R,j in {x,y} of
> ((pred_shift_ij - true_shift_ij) / scale_shift_j)^2
> B_shift is calculated with the same formula after replacing every prediction with the public
> training-mean translation.
> S_shift = clip(1 - E_shift / B_shift, 0, 1)
> Radiometric Repair Skill
> Let P be the examples whose true fault type is radiometric. Let the six repair dimensions be the
> three gains and three biases.
> E_radio = mean over i in P,j of
> ((pred_radio_ij - true_radio_ij) / scale_radio_j)^2
> B_radio is calculated with the same formula after replacing every prediction with the
> corresponding public training-mean repair value.
> S_radio = clip(1 - E_radio / B_radio, 0, 1)
> The combined repair skill is:
> S_repair = 0.5  *S_shift + 0.5*  S_radio
> Final Score
> raw_score = 0.55 * S_change
> + 0.25 * S_fault
> + 0.20 * S_repair
> final_score = max(0.001, min(1.0, raw_score))
> Higher is better. An exact submission scores 1.0. Predictions that do not improve on the published
> constant baselines are at the score floor.
> Submission
> Submit a CSV with exactly these columns:
> id,p_clean,p_radiometric,p_registration,p_content_swap,shift_x,shift_y,gain_r,gain_g,gain_b,bias_r,bias_g,bias_b,change_00,change_01,change_02,change_03,change_10,change_11,change_12,change_13,change_20,change_21,change_22,change_23,change_30,change_31,change_32,change_33
> Provide exactly one row for every id in test.csv.
> The CSV must contain exactly the documented columns, with no additional columns. Every prediction
> must parse as a finite numeric value. Blank values, nonnumeric text, NaN, infinity, negative fault
> probabilities, and probability rows whose sum is not positive invalidate the entire submission and
> return the score floor. Valid non-negative fault probabilities are normalized to sum to one.
> Finite change predictions are clipped to [0, 1], and finite repair predictions are clipped to their
> documented physical ranges before scoring.
> A complete example row is:
> id,p_clean,p_radiometric,p_registration,p_content_swap,shift_x,shift_y,gain_r,gain_g,gain_b,bias_r,bias_g,bias_b,change_00,change_01,change_02,change_03,change_10,change_11,change_12,change_13,change_20,change_21,change_22,change_23,change_30,change_31,change_32,change_33
> TE01A9F3,0.08,0.63,0.19,0.10,-0.014,0.006,0.93,1.04,0.98,0.018,-0.012,0.006,0.03,0.05,0.12,0.20,0.04,0.11,0.36,0.55,0.02,0.08,0.29,0.61,0.01,0.04,0.17,0.42
> What Not To Use
> Do not assume that every difference between the pre-event and post-event images represents physical change.
> Do not treat post_optical_claim as a guaranteed clean target. Determining whether it can be trusted is part of the task.
> Do not use identifiers, row order, or input_index as predictive features. They are lookup keys only.
> Do not attempt to identify source scenes through external imagery search, geographic fingerprinting, or filename recovery.
> Do not infer hidden answers from sample_submission.csv. It is a varied formatting example and contains no privileged predictions.
> Expected Output
> For every test patch, return:
> four fault-state probabilities;
> two registration repair values;
> six radiometric repair values;
> sixteen continuous physical-change estimates.
> Successful solutions must recover physical change while explicitly auditing and repairing
> unreliable cross-sensor evidence.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Lumbar MRI Structure Slice Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dhpaasfktynns3npt4kc8xd8a6bz8
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat komilpamar's score of 0.484!

Full challenge description from page:

> Overview
> Given a sagittal lumbar MRI slice, reconstruct a compact anatomy ledger. The ledger divides the image into a 36 by 36 grid and asks for the anatomy present in each cell, whether that cell lies near a visible structure boundary, and the coarse left-right slice-depth band. The visible structures are lumbar vertebral regions, intervertebral discs, and the spinal canal.
> The problem is not a whole-image classification task. It requires spatial recovery of anatomy under MRI contrast variation, partial slice coverage, and nearby structures with similar intensity.
> Dataset
> Files:
> train.csv: 800 labeled MRI slices.
> test.csv: 400 unlabeled MRI slices.
> sample_submission.csv: 400-row valid baseline.
> images/: PNG slice crops referenced by the CSV files.
> Columns:
> id (string): Opaque row id.
> image_path (string): Relative path to the PNG slice.
> scan_context (string): MRI acquisition context, either t1 or t2.
> answer_format_json (JSON object): Output grid shape, row-major array order, required field names, valid integer values, and required array length.
> answer_json (JSON object, train only): Ground-truth anatomy ledger.
> Required answer_json fields:
> grid_shape: [36, 36].
> structure_cells: length-1296 row-major integers. 0 means background, 1 means vertebral region, 2 means spinal canal, and 3 means intervertebral disc.
> edge_bins: length-1296 row-major integers. 0 means no labeled anatomy in the cell. 1, 2, and 3 indicate increasing local boundary concentration inside an anatomical cell.
> depth_bins: length-1296 row-major integers. 0 means no labeled anatomy in the cell. 1 through 5 indicate the coarse sagittal slice-depth band for anatomical cells.
> Submission Format
> The submission CSV must contain exactly id and answer_json; column order is not important.
> id,answer_json
> example_row,"{""grid_shape"":[36,36],""structure_cells"":[0,0,1],""edge_bins"":[0,1,1],""depth_bins"":[0,0,2]}"
> The arrays above are abbreviated. Full submissions must include 1296 entries for each array.
> Evaluation
> The grader rejects malformed rows before scoring. Valid rows are evaluated with squared active IoU for each output field.
> For each array, the grader ignores value 0 when deciding which classes to average over. For every nonzero value appearing in either the prediction or truth, it computes:
> IoU(value) = intersection(pred == value, truth == value) / union(pred == value, truth == value)
> The field score is the mean of those nonzero-value IoUs, squared. The resulting field scores are combined as:
> row_score = 0.52 * structure_cells_score + 0.28 * edge_bins_score + 0.20 * depth_bins_score
> The final score is the mean row score over the held-out rows. The range is 0 to 1.
> What Not To Use
> Do not use unreleased masks, annotations, metadata, answer files, or organizer-only artifacts.
> Do not infer targets from row order, hardcoded ids, or manual lookup of held-out slices.
> Do not use external datasets, hosted inference APIs, runtime package installs, vendored or downloaded code, private/gated assets, challenge-specific pretrained checkpoints.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Roadside Message Panel Text-Region Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx707p88fqdv6ssa6rp1jbq1p18bna9z
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat zip_zip_zap_zap's score of 0.550!

Full challenge description from page:

> Overview
> Roadside traffic-monitoring images often capture electronic message panels from an oblique viewpoint, with glare, motion blur, nearby signs, and partially visible displays. The panels are used to communicate lane closures, warnings, route guidance, or short traffic-control messages. Each row gives a transformed road-scene image with one annotated message panel. Recover the visible message-panel record in that image: where the panel sits, the displayed text, and the set of text tokens visible on the panel.
> This is a structured visual recovery task. A good solution needs both localization and reading of the panel text, not just an image-level decision.
> Files
> train.csv: Labeled examples.
> test.csv: Held-out examples to predict.
> sample_submission.csv: A weak example with the required columns.
> images/: JPEG files referenced by image_path.
> Columns in train.csv:
> id: Opaque row identifier.
> image_path: Relative path to the transformed image.
> packet_json (JSON string): input constraints. It contains image_size ([1280,720]) and max_panels (integer, always 3).
> answer_json (JSON string): target structured record. It contains panel_count (integer), message_tokens (list[string]), and panels (list[object]).
> Columns in test.csv:
> id: Opaque row identifier.
> image_path: Relative path to the transformed image.
> packet_json (JSON string): same structure as in train.csv.
> Answer Format
> Submit a CSV with exactly two columns:
> id
> answer_json
> Each answer_json value must be a JSON object with exactly these keys:
> panel_count: Integer number of annotated message panels. In this release it is always 1, and is kept as a schema consistency field.
> message_tokens: Sorted unique list of uppercase tokens visible in the panel text.
> panels: List of panel records.
> Each panel record must have exactly these keys:
> box: [x_min, y_min, x_max, y_max] integer pixel coordinates in the transformed image.
> text: Uppercase message text, with normal spacing.
> truncated: 1 if the panel is marked truncated, otherwise 0.
> Example:
> id,answer_json
> panel_example_01,"{""message_tokens"":[""CARRIL"",""CERRADO""],""panel_count"":1,""panels"":[{""box"":[250,94,425,147],""text"":""CARRIL CERRADO"",""truncated"":0}]}"
> panel_example_02,"{""message_tokens"":[""DESPACIO""],""panel_count"":1,""panels"":[{""box"":[612,210,786,270],""text"":""DESPACIO"",""truncated"":0}]}"
> Evaluation
> The score is the mean row score over all held-out rows. Each row score is in [0,1].
> Rows with malformed JSON or invalid field values receive zero for that row. The CSV must still contain exactly the required columns, exactly one row for every expected id, and no missing, duplicate, or extra ids.
> For each row:
> token_score is set F1 over message_tokens: precision is matching submitted tokens divided by submitted tokens, recall is matching submitted tokens divided by true tokens, and F1 is 2*precision*recall/(precision+recall). If both token sets are empty, the score is 1; if only one side is empty, the score is 0.
> Each predicted panel can match at most one true panel, and each true panel can match at most one predicted panel. Candidate panel-pair scores are sorted high to low and greedily assigned without reuse.
> A panel-pair score is 0.38*box_iou + 0.42*text_similarity + 0.14*panel_token_f1 + 0.06*truncated_exact. box_iou is standard intersection-over-union for the two pixel boxes. text_similarity is normalized sequence similarity after uppercasing and whitespace normalization. panel_token_f1 is set F1 over alphanumeric tokens extracted from each panel's text. truncated_exact is 1 when the submitted and true truncated flags match and 0 otherwise.
> panel_match_score converts the greedy matched sum into F1-style precision and recall: precision = matched_score_sum / submitted_panel_count, recall = matched_score_sum / true_panel_count, and panel_match_score = 2*precision*recall/(precision+recall). If both panel lists are empty, the score is 1; if only one list is empty, the score is 0.
> The row score is:
> 0.20 * token_score + 0.80 * panel_match_score
> What Not To Use
> Use the supplied images and tables only.
> Do not hard-code row ids or answers.
> Do not manually label held-out rows.
> Do not use lookup services, web search, image search, or external copies of road-scene datasets.
> Do not call hosted vision or OCR systems.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Shadow Motion Cause Separation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7182s1h177xekmf34tw7sde98bjq92
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview
> Predict three structured records from a six-frame visual sequence: a regional cause-code grid, a camera-compensated shadow-motion program, and the four material-boundary cells that remain most reliable after shadowed pixels are ignored.
> Outdoor inspection cameras often observe three effects at once. Cast shadows move across a surface, foreground objects enter or leave the view, and the camera itself translates over textured material. A simple difference image merges all three. This challenge instead asks a model to separate their evidence and describe how the shadow layer moves after camera motion is removed.
> Each input is a 956 x 512 RGB JPEG containing six chronological frames labeled A through F. The panels come from transformed real or controlled image sequences. Crop, horizontal reflection, brightness calibration, and contrast calibration vary between examples. The source scene and original frame numbers are never exposed.
> For every sequence sheet, predict:
> | Output | Meaning |
> |---|---|
> | `cause_code_grid` | A `4 x 4` integer grid describing which visual causes are supported in each spatial cell. |
> | `transport_program` | Five ordered tokens describing shadow displacement and area change from `A` to `B` through `E` to `F`, after compensating global camera translation. |
> | `boundary_survivor_set` | Four grid cells containing the strongest persistent material-boundary evidence outside annotated shadow and foreground-object regions. |
> This is a structured visual decomposition task. It is not ordinary shadow segmentation, optical-flow regression, or scene classification.
> Compute Budget
> Solutions run with one NVIDIA A10G GPU and a maximum wall-clock time of 30 minutes. Training, validation, inference, and writing submission.csv must all finish within that budget. GPU use is allowed but not required.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `public/train.csv` | Labeled training records. |
> | `public/test.csv` | Hidden-label evaluation records. |
> | `public/sample_submission.csv` | A schema-valid baseline submission. |
> | `public/images/` | Prepared six-panel JPEG sequence sheets referenced by both CSV files. |
> The hidden split contains complete physical sequences that do not contribute any source frame to training. Exact prepared-image hashes are unique across all rows.
> The prepared dataset contains 1,100 labeled training rows and 420 hidden test rows.
> Public Training Distribution
> The following counts cover all 17,600 cells in the public training grids. Codes 6 and 7 remain valid outputs even though they do not occur in the public training split.
> | Cause code | Training cell count |
> |---|---:|
> | `0` | 11,706 |
> | `1` | 4,634 |
> | `2` | 1,036 |
> | `3` | 205 |
> | `4` | 15 |
> | `5` | 4 |
> | `6` | 0 |
> | `7` | 0 |
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | String | Opaque identifier matching `sc[0-9a-f]{20}`. It contains no source, scene, frame, split, or label information. |
> | `sequence_sheet_path` | String | Relative path such as `images/sc0123456789abcdefabcd.jpg`. The file shows frames `A` through `F` in chronological order, with `A` to `C` on the upper row and `D` to `F` on the lower row. |
> Target Columns
> | Column | Data type | Description |
> |---|---|---|
> | `cause_code_grid` | JSON array of integer arrays | Exactly four rows by four columns. Every value is an integer from 0 through 7. |
> | `transport_program` | String token sequence | Exactly five `>`-separated transition tokens, one for each adjacent panel pair. |
> | `boundary_survivor_set` | String set | Exactly four distinct cell tokens separated by `|`. Order does not affect grading. |
> Cause Codes
> The image is divided into four equal rows and four equal columns. Cell r0c0 is the upper-left cell and r3c3 is the lower-right cell.
> Each cause code is a three-bit value:
> | Bit value | Evidence represented |
> |---|---|
> | `1` | Shadow occupancy changes materially during the six frames. |
> | `2` | A visible foreground-object annotation occupies part of the cell. |
> | `4` | Camera translation is present and the cell contains enough texture to carry that viewpoint motion. |
> Add the active bit values. For example, code 5 means changing shadow plus texture-supported camera motion, while code 6 means foreground-object evidence plus camera motion. Code 0 means none of the three conditions is supported.
> Transport Program
> The grammar is:
> f<step>:<direction>:<area_change>
> Five tokens are joined with >. Steps must be f1, f2, f3, f4, and f5 in that order.
> direction is one of N, NE, E, SE, S, SW, W, NW, H, or X. The eight compass tokens describe image-plane motion, so S means south. H means the compensated displacement is smaller than the movement threshold and the shadow holds position. X means too little shadow is visible to estimate a centroid reliably.
> area_change is inc, flat, or dec, describing the change in shadow-covered area between the two panels.
> Example:
> f1:E:inc>f2:SE:flat>f3:S:dec>f4:X:flat>f5:W:inc
> Boundary Survivor Set
> Valid tokens are r0c0 through r3c3. The target contains the four cells with the strongest temporally persistent image-gradient evidence after shadow and visible foreground-object pixels are excluded.
> Example:
> r0c2|r1c1|r2c3|r3c0
> Submission Format
> Write the final CSV to:
> ./working/submission.csv
> The file must contain exactly these columns in this order:
> case_id,cause_code_grid,transport_program,boundary_survivor_set
> One nontrivial row is:
> case_id,cause_code_grid,transport_program,boundary_survivor_set
> sc0123456789abcdefabcd,"[[0,1,5,4],[2,3,7,4],[0,1,1,4],[0,0,4,4]]",f1:E:inc>f2:SE:flat>f3:S:dec>f4:X:flat>f5:W:inc,r0c2|r1c1|r2c3|r3c0
> Requirements:
> Include exactly one row for every test case_id.
> Duplicate IDs, missing IDs, unknown IDs, reordered columns, and extra columns are rejected.
> A single backend-managed visibility column is tolerated and ignored.
> cause_code_grid is limited to 160 characters.
> transport_program is limited to 180 characters and exactly five tokens.
> boundary_survivor_set is limited to 120 characters and exactly four distinct valid cells.
> Malformed component values receive zero for that component.
> Evaluation
> The metric is the Shadow Cause Separation Score:
> Score =
> 0.42 * CauseGridScore
> + 0.36 * TransportScore
> + 0.22 * BoundarySurvivorScore
> Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> CauseGridScore
> For one sample, compare the three bits at all 16 positions.
> bit_agreement =
> correctly matched bit states
> / (16 * 3)
> exact_grid = 1 if all 16 integer codes match, else 0
> row_grid_score =
> 0.32 * bit_agreement
> + 0.68 * exact_grid
> CauseGridScore is the mean row_grid_score over test samples. The bit term gives limited partial credit when a solver identifies one cause correctly but misses a co-occurring cause. Exact recovery remains dominant.
> TransportScore
> Let d be token-level Levenshtein edit distance between the five true tokens and five submitted tokens. Substitution, insertion, and deletion each cost one.
> edit_similarity = 1 - d / max(true_token_count, submitted_token_count, 1)
> exact_program = 1 if all five tokens match in order, else 0
> row_transport_score =
> 0.22 * edit_similarity
> + 0.78 * exact_program
> TransportScore is the mean row score.
> BoundarySurvivorScore
> Treat the four submitted cell tokens as a set. If T is the true set and P is the submitted set:
> set_f1 = 2 * |T intersection P| / (|T| + |P|)
> exact_set = 1 if T equals P, else 0
> row_boundary_score =
> 0.50 * set_f1
> + 0.50 * exact_set
> BoundarySurvivorScore is the mean row score.
> Reference Validation
> The packaged reference answers score 1.0. The schema-valid sample submission scores 0.240473, and a frequent-target training baseline scores 0.298787. The training and hidden splits contain 555 and 249 distinct transport programs. Two clean preparations produced byte-identical output trees, and the grader rejects duplicate IDs, missing IDs, unknown IDs, extra columns, reordered columns, oversized structures, and malformed component values.
> Expected And Allowed Methods
> A10G-compatible approaches include fine-tuned compact vision transformers, temporal CNNs, optical-flow or registration features combined with learned heads, sequence models over panel embeddings, and small ensembles. Mixed precision, pretrained visual backbones, and classical alignment or edge extraction are allowed, provided the complete solution finishes within 30 minutes.
> What Not To Use
> Do not derive predictions from case_id, image filenames, CSV row order, file size, hashes, or split ordering.
> Do not search for or match prepared images against external copies of the source frames.
> Do not build source-frame lookup tables, perceptual-hash indexes, or nearest-neighbor databases from external mirrors.
> Do not use original source filenames, acquisition-folder names, unpublished annotations, or private answer files.
> Do not exploit malformed rows, duplicate identifiers, grader exceptions, or submission-schema behavior.
> Do not adapt model parameters using hidden test examples or any test-derived pseudo-labels.
> What Makes This Interesting
> The same dark region can move because illumination changed, because the camera moved, or because a foreground object entered the cell. The cause grid allows these explanations to coexist instead of forcing a single class. The transport program then asks for a motion description in a camera-compensated coordinate system, while the survivor set asks which material boundaries remain trustworthy after contaminated pixels are removed. A good solution must use temporal appearance, geometry, and texture persistence together.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Urban Surface Marking Extent Profile Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73vy9vj52rq71hxhg9cvvf618bjz94
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat sensi's score of 0.672!

Full challenge description from page:

> Overview
> City maintenance photos can contain many small markings on walls, pillars, railings, doors, or utility boxes. Some markings are tiny and isolated, while others span long strips or appear as clusters. Each row gives a transformed street-scene image and asks you to reconstruct a compact profile of the visible marked regions.
> Predict which cells in a 9 by 12 grid are touched by annotated markings, which occupied cells touch an image edge, how many marking regions are present, where the largest region cards fall, and how marking mass is distributed vertically. The target is a structured spatial summary of marked surface regions rather than a single image label.
> Dataset
> Files:
> train.csv: 700 labeled examples.
> test.csv: 322 held-out examples.
> sample_submission.csv: A weak schema example with the required columns.
> images/: JPEG street-scene images referenced by image_path.
> Columns in train.csv:
> id (string): Row identifier.
> image_path (string): Relative path to the transformed street-scene JPEG.
> packet_json (JSON string): Input constraints. It contains image_size as [360, 480], grid_shape as [9, 12], and max_region_cards as 12.
> answer_json (JSON string): Ground-truth marking extent profile.
> Columns in test.csv:
> id (string): Row identifier.
> image_path (string): Relative path to the transformed street-scene JPEG.
> packet_json (JSON string): Same structure as in train.csv.
> The answer_json object has exactly these fields:
> marking_count (integer): Number of annotated marking regions, capped at 30.
> occupied_cells (array of strings): Grid cells touched by any annotated marking region.
> edge_touch_cells (array of strings): Occupied cells touched by a region that reaches the image boundary.
> size_histogram (object): Counts for small, medium, and large marking regions, each capped at 9.
> vertical_band_counts (array of 9 integers): Count of marking-region centers in each grid row, capped at 9 per row.
> area_bin (integer): Coarse bin from 0 to 8 for total marked area fraction.
> region_cards (array of objects): Up to 12 largest/earliest region summaries. Each card has integer cx_bin, cy_bin, w_bin, and h_bin.
> Cell tokens use rRR_cCC, for example r04_c07. edge_touch_cells must be a subset of occupied_cells.
> Evaluation
> The score is the mean row score over the held-out test rows.
> For a set-valued field, F1 is:
> F1 = 2 * precision * recall / (precision + recall)
> where precision = |predicted intersection true| / |predicted| and recall = |predicted intersection true| / |true|. If both sets are empty, F1 is 1. If exactly one set is empty, F1 is 0.
> For each row:
> count_score = max(0, 1 - abs(predicted_marking_count - true_marking_count) / 8).
> occupied_score = F1(predicted occupied_cells, true occupied_cells).
> edge_score = F1(predicted edge_touch_cells, true edge_touch_cells).
> hist_score is the mean over small, medium, and large of max(0, 1 - abs(predicted_count - true_count) / 4).
> vertical_score is the mean over the 9 rows of max(0, 1 - abs(predicted_band_count - true_band_count) / 5).
> area_score = max(0, 1 - abs(predicted_area_bin - true_area_bin) / 4).
> card_score is duplicate-aware F1 over exact (cx_bin, cy_bin, w_bin, h_bin) region-card tuples.
> The row score is:
> 0.14 * count_score + 0.27 * occupied_score + 0.12 * edge_score + 0.12 * hist_score + 0.12 * vertical_score + 0.08 * area_score + 0.15 * card_score
> Malformed JSON or invalid values score 0 for that row. The submitted CSV must still have exactly the required columns, exactly one row per test id, and no missing, extra, or duplicate ids.
> Submission
> Submit a CSV with exactly two columns:
> id (string)
> answer_json (JSON string)
> Example:
> id,answer_json
> mark_example_01,"{""marking_count"":2,""occupied_cells"":[""r02_c04"",""r02_c05"",""r03_c05""],""edge_touch_cells"":[],""size_histogram"":{""small"":1,""medium"":1,""large"":0},""vertical_band_counts"":[0,0,1,1,0,0,0,0,0],""area_bin"":2,""region_cards"":[{""cx_bin"":3,""cy_bin"":2,""w_bin"":2,""h_bin"":1},{""cx_bin"":4,""cy_bin"":3,""w_bin"":1,""h_bin"":1}]}"
> mark_example_02,"{""marking_count"":1,""occupied_cells"":[""r07_c00"",""r07_c01""],""edge_touch_cells"":[""r07_c00""],""size_histogram"":{""small"":1,""medium"":0,""large"":0},""vertical_band_counts"":[0,0,0,0,0,0,0,1,0],""area_bin"":1,""region_cards"":[{""cx_bin"":0,""cy_bin"":7,""w_bin"":1,""h_bin"":1}]}"
> What Not To Use
> Do not use any files outside the supplied dataset package.
> Do not use external image collections, annotation collections, search engines, or lookup services.
> Do not hard-code row ids, image names, or answers.
> Do not manually label the held-out images.
> Do not use hosted vision APIs or pretrained external checkpoints.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Diffraction Detector Evidence Routing

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx784sdf4nts4xbqktgw8xad058a6k3z
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview
> For each six-panel diffraction contact sheet, predict a routing certificate that says which detector panels should be used, inspected, or dropped before crystallographic integration.
> The input is a grayscale image containing six detector crops labeled A through F. Some panels contain strong Bragg-spot evidence. Others are weakened by saturation, beam-shadow regions, dead strips, hot pixels, or low spot continuity. The challenge asks for one coherent evidence-routing record: a partition of panels, a quality matrix, an artifact-coupling graph, and a final integration gate.
> This is intended to model a practical crystallography archive step. Before integration, a pipeline or scientist needs to know whether the detector packet has enough usable evidence, whether some panels require manual indexing, or whether the scan should be recollected or discarded. The task is not frame ordering, material classification, phase identification, or image retrieval.
> Dataset
> The prepared data contains 600 training cases and 455 hidden test cases. The source detector frames come from multiple acquisition series. Five acquisition series contribute training cases, and three separate acquisition series contribute hidden test cases. Within the training series, cases are selected by opaque SHA-256 ranking rather than chronological order, so source ordering does not define the split.
> Ground-truth labels are generated from the rendered detector panel evidence and source acquisition geometry. Each panel is assigned four quality values: spot continuity, saturation risk, shadow risk, and integration utility. The panel partition, artifact graph, and integration gate are then derived from those quality values using the same deterministic contract for train and test.
> | Path | Description |
> |---|---|
> | `train.csv` | 600 rows. Contains `case_id`, `image_path`, and the four target columns. |
> | `test.csv` | 455 rows. Contains only `case_id` and `image_path`. |
> | `sample_submission.csv` | A complete schema-valid baseline submission with one row per hidden test case. |
> | `images/` | 1,055 grayscale JPEG contact sheets. Each image is `824 x 590` pixels and contains six labeled detector panels. |
> Columns
> | Column | Data type | Present in | Description |
> |---|---|---|---|
> | `case_id` | string | train, test, submission | Opaque 20-character hexadecimal identifier. |
> | `image_path` | string | train, test | Relative path to the `824 x 590` JPEG contact sheet. |
> | `routing_partition` | string | train, submission | Three panel groups in the order `use`, `inspect`, `drop`. |
> | `detector_quality_matrix` | JSON string | train, submission | `6 x 4` integer matrix in panel order `A, B, C, D, E, F`. |
> | `artifact_coupling_graph` | string | train, submission | Canonical edge set for panel pairs with shared artifact risk, or `none`. |
> | `integration_gate` | string | train, submission | Final packet decision: `integrate`, `manual_index`, `recollect`, or `discard`. |
> Image Features
> | Feature | Data type | Description |
> |---|---|---|
> | Panel label | categorical text in image | One of `A` through `F`, printed beside a detector panel. |
> | Bragg-spot pattern | grayscale pixels | Bright reflection spots used to judge spot continuity. |
> | Saturated region | grayscale pixels | Overloaded bright areas and hot pixels that increase saturation risk. |
> | Shadow artifact | grayscale pixels | Dark bands, dead strips, or blocked regions that increase shadow risk. |
> | Panel utility | visual quality evidence | Combined usefulness of the panel after continuity, saturation, and shadow risk are considered. |
> | Coupled artifact evidence | pairwise visual relation | Two panels may share high saturation risk, high shadow risk, or both. |
> Target Format
> routing_partition has this exact format:
> use:LABELS;inspect:LABELS;drop:LABELS
> Every panel label A through F must appear exactly once across the three groups. Labels inside each group must be alphabetic. Use none for an empty group.
> detector_quality_matrix is a JSON-encoded 6 x 4 integer matrix. Rows follow A, B, C, D, E, F.
> | Matrix column | Name | Range | Meaning |
> |---:|---|---:|---|
> | 0 | `spot_continuity` | 0 to 4 | Coherence of useful Bragg-spot evidence. |
> | 1 | `saturation_risk` | 0 to 4 | Risk from overloaded or saturated regions. |
> | 2 | `shadow_risk` | 0 to 4 | Risk from beam shadow, dead strips, or blocked detector evidence. |
> | 3 | `integration_utility` | 0 to 4 | Expected usefulness for downstream integration. |
> artifact_coupling_graph is either none or a |-separated list of sorted edge tokens:
> L~R:t
> L and R are panel labels with L alphabetically before R. The edge type t is shadow, saturation, or compound.
> integration_gate must be one of:
> | Value | Meaning |
> |---|---|
> | `integrate` | Enough panels are usable for automatic integration. |
> | `manual_index` | Enough evidence exists, but manual crystallography review is needed. |
> | `recollect` | Too few panels are usable, so new detector evidence is needed. |
> | `discard` | The packet has insufficient usable evidence. |
> Example labeled row:
> case_id,image_path,routing_partition,detector_quality_matrix,artifact_coupling_graph,integration_gate
> d01a0fa1b0664d01857f,images/d01a0fa1b0664d01857f.jpg,use:ACDEF;inspect:none;drop:B,"[[1,2,0,4],[3,4,0,4],[2,1,2,3],[2,0,2,4],[4,1,1,4],[4,0,3,4]]",none,integrate
> Training distribution:
> | Integration gate | Count |
> |---|---:|
> | `integrate` | 168 |
> | `manual_index` | 297 |
> | `recollect` | 101 |
> | `discard` | 34 |
> Training data contains 107 unique routing partitions, 600 unique detector-quality matrices, and 420 unique artifact-coupling graphs.
> Submission Format
> Write the final CSV to exactly:
> ./working/submission.csv
> The file must contain exactly these columns in this order:
> case_id,routing_partition,detector_quality_matrix,artifact_coupling_graph,integration_gate
> All target fields are strings. detector_quality_matrix must be valid JSON. The grader rejects extra columns, reordered columns, duplicate column names, missing or extra rows, duplicate IDs, unknown IDs, and malformed IDs. Malformed target values receive zero for the affected component.
> Field limits exist only to keep grading bounded: 46 characters for routing_partition, 210 for detector_quality_matrix, 230 and at most 18 edges for artifact_coupling_graph, and one valid integration_gate token.
> Example:
> case_id,routing_partition,detector_quality_matrix,artifact_coupling_graph,integration_gate
> d01a0fa1b0664d01857f,use:ACDEF;inspect:none;drop:B,"[[1,2,0,4],[3,4,0,4],[2,1,2,3],[2,0,2,4],[4,1,1,4],[4,0,3,4]]",none,integrate
> Evaluation
> Submissions are evaluated with the Detector Evidence Routing Score.
> Minimum score: 0.0
> Maximum score: 1.0
> Higher is better.
> The base score is the weighted sum below. These weights sum to 1.0 before the coherence multiplier is applied.
> base = 0.30 * PartitionScore
> + 0.34 * MatrixScore
> + 0.20 * GraphScore
> + 0.16 * GateScore
> PartitionScore
> The partition is converted into tokens such as use:A and drop:B.
> PartitionScore = 0.30 * SetF1(true_tokens, predicted_tokens)
> + 0.70 * I(predicted partition exactly equals true partition)
> MatrixScore
> Let Y[i,j] and P[i,j] be hidden and submitted matrix entries.
> w = [1.2, 1.2, 1.2, 1.4]
> weighted_agreement = sum_i sum_j w[j] * I(P[i,j] = Y[i,j]) / (6 * sum_j w[j])
> MatrixScore = 0.34 * weighted_agreement + 0.66 * I(P exactly equals Y)
> GraphScore
> The graph is scored as a set of complete edge tokens.
> GraphScore = 0.40 * SetF1(true_edges, predicted_edges)
> + 0.60 * I(predicted graph exactly equals true graph)
> GateScore
> GateScore = I(submitted integration_gate exactly equals hidden integration_gate)
> Coherence Multiplier
> The four targets are scored independently against hidden truth. Coherence is a small extra multiplier that checks whether a submitted partition and gate are consistent with the submitted matrix and graph.
> For a submitted row, compute expected groups from the submitted matrix:
> A panel is use if integration_utility >= 3, saturation_risk <= 3, and shadow_risk <= 3.
> A panel is drop if integration_utility <= 1, or saturation_risk = 4, or shadow_risk = 4.
> All other panels are inspect.
> Then compute:
> usable = number of panels in submitted use group
> risky = number of panels in submitted drop group + floor(number of submitted graph edges / 3)
> The submitted row is coherent, so C = 1, only if all three checks pass:
> The submitted routing_partition exactly matches the expected groups computed from the submitted matrix.
> The submitted graph is syntactically valid under the graph grammar.
> The submitted gate is compatible with usable and risky:
> integrate requires usable >= 4 and risky <= 2.
> manual_index is always compatible after checks 1 and 2 pass.
> recollect requires usable = 2.
> discard requires usable < 2.
> Otherwise C = 0.
> CaseScore = base * (0.84 + 0.16 * C)
> FinalScore = mean(CaseScore over all test cases)
> Malformed fields score 0 for their component and make the row incoherent. Hidden answers are parsed strictly and must satisfy the same detector-routing contract.
> What Makes This Interesting
> This is not photo sequencing, acquisition ordering, splice detection, phase identification, or image retrieval. The solver must route detector evidence for downstream crystallography: decide which panels are trustworthy, which panels need review, which panels should be dropped, and whether the packet can proceed.
> The key reasoning object is a quality-controlled integration route. It combines reciprocal-space spot evidence, artifact risk, panel-pair coupling, and gate-level decision logic. The held-out acquisition-series split tests whether a method learns transferable detector-evidence cues rather than memorizing one scan or using row order.
> What Not To Use
> Do not match public images against external copies of the source detector frames by exact hash, perceptual hash, local-feature retrieval, or manual source-file lookup.
> Do not use public IDs, image filenames, row order, file size, or submission order as substitutes for image evidence.
> Do not construct a lookup table from recovered source filenames, acquisition indices, or external metadata.
> Do not exploit duplicate rows, malformed submissions, parser limits, or grader behavior.
> Fit and tune predictive components only with the supplied public training data. No test-label adaptation is allowed.
> Classical computer vision and learned image models are both allowed when they operate on the supplied public images and respect the runtime limits.
> Reference Validation
> The exact hidden answers score 1.0. Sample, train-mode, duplicate, leakage, and strict-schema audit results are recorded in validation_report.json.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Storm Region Ignition Forecasting from Satellite Imagery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78csqy5n0gxy8j48j51h3mwd8bm4f8
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Storm Region Ignition Forecasting from Satellite Imagery
> Overview
> A thunderstorm is watched from orbit for an hour. The field of view is divided into a grid of
> sixteen regions. Some of those regions are completely silent during that hour — not a single
> lightning flash anywhere in them.
> In the hour that follows, exactly one of the silent regions ignites: lightning begins there.
> Your task is to say which one.
> You are given the satellite imagery and nothing else. The lightning record is never published —
> not for the hour you can see, and not for the hour you are predicting. All you are told is which
> regions were silent, and those are what you choose between.
> Three properties of how each row is put together decide what can and cannot work:
> The region that ignites is never the one that looks most convective. Every row is chosen so
> that the coldest, most storm-like silent region is not the answer. Picking whichever region
> looks most developed right now is therefore not merely a weak strategy — it is reliably wrong,
> and scores far below a random guess.
> Only silent regions can be the answer. Regions already producing lightning are excluded, so
> "wherever the storm already is" separates nothing.
> You never see lightning. The answer lives in a measurement channel that is not published,
> describing an hour that is not published either.
> What is left is how the cloud field is developing — where it is cooling, spreading and
> organising — rather than how it looks at the final moment.
> Task constraints
> The storms are unseen. No storm appearing in training appears in the test rows. Whole storm
> events are held out.
> No metadata is published. Location, date, time of day, storm severity and every other
> measurement channel are withheld. A row is the imagery and the silent-region mask, nothing else.
> The number of silent regions varies from row to row, between four and sixteen.
> Data
> Every row publishes twelve infrared satellite frames, five minutes apart, covering one hour.
> Each frame is a 64 x 64 grid of uint8 values encoding cloud-top temperature on a fixed scale,
> so brightness is comparable across rows: low values are cold, high cloud tops.
> The 4 x 4 region grid divides each frame into sixteen 16 x 16 blocks, numbered row-major:
> region 0 is the top-left, region 3 the top-right, region 15 the bottom-right.
> Files provided:
> train.npz — training inputs; holds the arrays ids, frames and silent described below,
> with N = 3,750 rows
> train.csv — training answers; two columns, id and prediction, described below
> test.npz — test inputs; the same three arrays as train.npz, with N = 2,999 rows
> sample_submission.csv — a correctly-formatted but deliberately weak example submission, with
> the same two columns as train.csv (id and prediction) and one row for each of the 2,999
> test ids. It names the lowest-numbered silent region of each row, scores about 0.14, and exists
> to show the exact expected format rather than as a useful starting point.
> Arrays in train.npz / test.npz:
> ids — type str, shape (N,) — the row id, e.g. cell_0a1b2c3d4e5f6071
> frames — type uint8, shape (N, 12, 64, 64) — the hour of imagery; frames[i, t] is frame
> t of row i, with t = 0 the earliest and t = 11 the most recent
> silent — type uint8, shape (N, 16) — the candidate mask; silent[i, c] is 1 when region
> c of row i was completely silent during the published hour, and 0 otherwise. The answer is
> always a region whose entry is 1
> Columns in train.csv:
> id — type string, e.g. cell_0a1b2c3d4e5f6071 — matches an entry of ids in train.npz
> prediction — type integer, e.g. 6 — the region index in 0…15 that ignites in the hour
> following the published imagery
> You are given 3,750 training rows (each with the answer) and must give an answer for each of
> the 2,999 test rows.
> Data provenance
> The imagery comes from SEVIR (Storm EVent ImagRy), a collection of real storm events over the
> United States assembled by MIT Lincoln Laboratory from geostationary weather satellite and
> ground-based lightning observations, published through the AWS Open Data programme. The
> collection is released with no restrictions on use.
> The published frames are cropped, downsampled, rescaled, quantised and perturbed before release.
> Evaluation
> The score is accuracy — the fraction of test rows whose named region is correct:
> score = (number of rows where prediction == truth) / 2,999
> Range 0–1, higher is better. Naming the lowest-numbered silent region of each row scores about
> 0.14, which is what the provided sample_submission.csv does; always naming the single most
> common region scores about 0.19.
> Submission format
> Submit submission.csv with exactly these two columns, in this order, one row per test id:
> id, prediction
> Example:
> id,prediction
> cell_0a1b2c3d4e5f6071,6
> cell_112233445566778a,11
> prediction must be a whole number in 0…15. A structural error (missing, extra or duplicate
> ids, wrong or extra columns, a non-numeric, non-integer or out-of-range prediction) makes the
> whole submission score 0.
> Rules — what you may and may not use
> The intended solution learns, from the released training rows alone, to read where a cloud field
> is about to become electrically active. Everything below either protects that intent or protects
> the integrity of the test answers. A submission that breaks any prohibited rule is invalid
> regardless of score.
> Data — prohibited
> No external data of any kind. Do not fetch, download or otherwise bring in any satellite
> imagery, lightning record, radar product, weather reanalysis or storm report. The released
> train.npz and train.csv are the only permitted training material.
> No pretrained or third-party weights. Do not use any model whose parameters were fitted on
> data other than the released training rows, and do not download weights from anywhere. Every
> learned parameter in your solution must be fitted by you, here, on the released training rows.
> Ordinary library code that contains no fitted parameters is unrestricted.
> No identifying the source. Do not attempt to locate, name or download the collection the
> imagery was taken from, and do not try to match a published frame back to any public satellite
> archive or to recover the date, time or place of a storm. The frames are cropped, downsampled,
> rescaled, quantised and perturbed specifically to prevent this.
> No recovering the withheld lightning record. The lightning observations behind the answers
> are deliberately withheld. Do not reconstruct them from an outside source, and do not obtain
> them from anywhere other than what the released arrays themselves contain.
> Labels — prohibited
> No test answers. The answers for the test rows are withheld and must stay that way. Do not
> source them, guess at them from outside the released data, or hand-write them.
> No labelling test rows by hand. Answers must come from a procedure that runs on the test
> inputs. Do not inspect and annotate test rows yourself, individually or in bulk, and do not have
> any person or outside service annotate them for you.
> Answer each row from its own imagery. A row is answered using the frames and the mask given
> in that row. Do not compare rows against each other, and do not carry an answer from one row to
> another. Anything derived from how the rows happen to sit together in the release exploits the
> packaging rather than solving the task.
> No probing the score. Do not use repeated scored submissions to infer individual test
> answers, and do not tune anything against a score obtained that way.
> No answers baked into the submission. Predictions must be produced by your model at
> inference time. A submission.csv containing hard-coded, per-id or manually adjusted entries is
> invalid.
> Process — required
> The solution must be a learned model. Predictions must come from a model whose parameters
> were fitted on the released training rows and their answers. A fixed rule or a hand-tuned
> formula is not an acceptable solution even if it scores above the floor.
> Train only on training rows. Model fitting uses train.npz and train.csv only. You may
> read the test inputs to predict on them, but the test rows must never contribute to fitting
> parameters, selecting a model, or tuning anything.
> Hold out honestly. Any validation split you make must be drawn from the training rows, and
> the test answers must play no part in choosing between approaches.
> Reproducible inference. Fixed seeds and deterministic decoding — re-running your solution on
> test.npz must reproduce the same submission.csv and the same score.
> Documented method. The approach should be described clearly enough that a reader can see how
> a row is turned into a prediction and can re-run it.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Two-Angle Polarization Completion And Coupled Stress-Optic Mapping

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx708gb18ns4864tnb2ykqmmfh8bh1q3
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview
> Complete a coupled four-angle optical field from only two polarization-response views. For each transparent specimen under load, reconstruct both absent response images and recover the corresponding dense wrapped-retardance and cyclic principal-direction maps. You receive an RGB context image, an unloaded reference image, a binary specimen mask, and two aligned response images whose analyzer angles are chosen from 0, 45, 90, and 135 degrees; all six unordered two-angle pairings can occur.
> For every test case, submit one fixed-shape tensor payload containing:
> Output	What it represents
> missing_a	Missing response image A
> missing_b	Missing response image B
> retardance_bin	Wrapped-retardance bin map
> direction_bin	Cyclic direction bin map
> All four submitted arrays are 128 x 128. missing_a and missing_b are uint8 response images in [0,255], corresponding to missing_angle_A and missing_angle_B in test.csv. retardance_bin is a uint8 discrete wrapped-retardance map in 0..15. direction_bin is a uint8 cyclic principal-direction map in 0..7; bins wrap modulo 8, so bin 0 is adjacent to bin 7.
> This is not style transfer, specimen classification, scalar load regression, or ordinary image restoration. The benchmark-specific object is the coupled stress-optical image field: missing polarized measurements must agree with the dense retardance and cyclic direction maps under the four-angle polarimetric equations. Train rows include target NPZ files so models can learn the response convention; test rows expose only inputs.
> Appropriate solutions include small U-Nets, UNet++ variants, compact image transformers, or physics-guided encoder-decoders trained on the public train set. Useful features include the mask, observed angle pair, missing angle pair, unloaded reference, local fringe gradients, and Stokes-style consistency losses. A complete solution must run within 1.5 hours on the selected GPU tier; an A10G has ample headroom for compact image-to-image models.
> What Not To Do
> Using any of the approaches below is grounds for rejection on review, regardless of leaderboard score.
> Do not use source lookup, reverse-image search, original experiment names, raw filenames, source paths, load-step ids, row order, file hashes, or public web copies to reconstruct hidden targets.
> Do not reduce the task to specimen identity, load value, ordinary classification, scalar regression, or a single dense map while ignoring the missing polarization images.
> Do not submit the observed images copied into every output without learning the missing angle response.
> Do not use hosted APIs, hosted vision models, private files, internet access at inference time, or closed remote inference services.
> Do not exploit private/answers.csv, grader internals, file-system metadata, mtimes, CSV row order, or malformed NPZ payloads.
> Do not submit arrays with wrong shapes, dtypes, ranges, NaN/Inf values, path-traversal archive members, duplicate IDs, missing IDs, or extra IDs.
> Enforcement on invalid approaches: submissions that score through lookup, metadata reconstruction, private-file access, external hosted models, or rule-only shortcuts that do not solve the sparse-polarization inverse-imaging task may be rejected even if the CSV passes the grader.
> Intended Approach
> A strong solution should learn a multi-channel image-to-image mapping from the public training cases. A practical route is to stack RGB, reference, mask, observed response images, and four angle planes, train a compact GPU U-Net or transformer decoder to predict the four target arrays, and validate on train-only geometry or angle-pair folds. Losses should combine masked image reconstruction for the two missing views, ordered-bin losses for retardance, cyclic losses for direction, and a differentiable or post-hoc four-angle consistency term. Good solutions may use classical photoelastic features as inputs or auxiliary losses, but the final prediction should use learned visual generalization rather than source lookup, hardcoded IDs, or metadata rules.
> Evaluation
> The metric is a normalized image-tensor score. Higher is better. The theoretical minimum is 0.0; the theoretical maximum is 1.0.
> For each row, the grader decodes prediction_npz_b64 and checks four arrays:
> missing_a       uint8, shape (128,128), values 0..255
> missing_b       uint8, shape (128,128), values 0..255
> retardance_bin  uint8, shape (128,128), values 0..15
> direction_bin   uint8, shape (128,128), values 0..7
> The row score is:
> missing_score    = image similarity for the two missing views
> retardance_score = exact/adjacent-bin plus boundary score
> direction_score  = exact/adjacent cyclic-bin plus boundary score
> forward_score    = predicted-view Stokes maps vs hidden maps
> row_score = 0.50*missing_score
> + 0.25*retardance_score
> + 0.15*direction_score
> + 0.10*forward_score
> missing_score uses masked absolute-error, RMS-error, local-gradient, local-structure, and edge agreement terms. retardance_score rewards exact wrapped bins, adjacent-bin tolerance, and boundary agreement. direction_score rewards exact cyclic bins, adjacent-bin tolerance modulo 8, and boundary agreement. forward_score reconstructs the four analyzer-angle field from the two observed inputs plus your two missing-view predictions, recomputes wrapped retardance and direction under the same four-angle Stokes convention, and compares those recomputed maps to the hidden target dense maps.
> The final score blends mean row performance with hidden robustness:
> Final = 0.85 * mean(row_score)
> + 0.15 * worst subgroup mean
> The worst subgroup is the lowest mean over hidden specimen-geometry, load-regime, and observed-angle-pair groups. All checked test subgroups have at least 12 rows.
> Global structural errors raise InvalidSubmissionError: wrong or reordered columns, missing IDs, extra IDs, duplicate IDs, or an ID set that does not exactly match test.csv. Row-local corrupt base64/NPZ payloads, wrong array keys, wrong shapes, wrong dtypes, out-of-range tensor values, path traversal, duplicate NPZ members, and decompression-bomb-like payloads score zero for that row without leaking labels.
> Dataset
> The public split contains prepared source-neutral tensors only. It does not expose original experiment names, raw source paths, source filenames, load-step IDs, raw metadata, checksums, split construction metadata, or private answer metadata.
> Checked prepared split:
> Train cases: 192
> Test cases: 288
> Image size: 128 x 128
> Public prepared size: about 29.5 MB
> Private answer size: about 17.2 MB
> Train/test specimen-geometry overlap: 0
> File overview
> Item	Description
> train/images/*.png	Train input images
> test/images/*.png	Test input images
> train/targets/*.npz	Train target tensors
> train.csv	Inputs plus targets
> test.csv	Inputs only
> sample_submission.csv	Valid weak template
> All image paths are relative to the public dataset root. Train and test image folders use the same schema; only train rows include target NPZ paths.
> train.csv columns
> Column	Type	Description
> case_id	string	Opaque case id
> rgb_image_path	string	RGB context path
> unloaded_reference_path	string	Reference path
> specimen_mask_path	string	Mask path
> observed_polarization_image_1	string	First observed view
> observed_angle_1	int	First angle
> observed_polarization_image_2	string	Second observed view
> observed_angle_2	int	Second angle
> missing_angle_A	int	Target angle A
> missing_angle_B	int	Target angle B
> target_npz_path	string	Train targets
> prompt	string	Task prompt
> In train.csv, the observed and missing angle fields are always drawn from 0, 45, 90, and 135. target_npz_path points to a train-only NPZ containing five stored arrays: the four prediction targets plus a convenience copy of the public specimen mask. The mask array is not a prediction target and must not be included in a submission NPZ. The prompt field is a repeated source-neutral task reminder and is not a label.
> test.csv columns
> Column	Type	Description
> case_id	string	Opaque case id
> rgb_image_path	string	RGB context path
> unloaded_reference_path	string	Reference path
> specimen_mask_path	string	Mask path
> observed_polarization_image_1	string	First observed view
> observed_angle_1	int	First angle
> observed_polarization_image_2	string	Second observed view
> observed_angle_2	int	Second angle
> missing_angle_A	int	Target angle A
> missing_angle_B	int	Target angle B
> prompt	string	Task prompt
> In test.csv, the path columns point only to public input images. The two missing-angle columns identify which polarizer-response images your missing_a and missing_b arrays must represent. There is no test target path in the public split.
> target NPZ contents
> Array	Shape	Description
> missing_a	(128,128)	Missing view A
> missing_b	(128,128)	Missing view B
> retardance_bin	(128,128)	Wrapped bins
> direction_bin	(128,128)	Cyclic bins
> mask	(128,128)	Convenience mask copy
> The first four arrays are prediction targets. mask duplicates the public image referenced by specimen_mask_path for convenient masked training and evaluation; participants do not predict it.
> Submission
> Submit a CSV with exactly these columns in this order:
> case_id,prediction_npz_b64
> Column	Type	Constraint
> case_id	string	Same set as test
> prediction_npz_b64	base64 NPZ	Four arrays
> Write one row for every test case_id; missing, extra, unknown, or duplicate IDs are invalid. The NPZ payload must contain exactly missing_a, missing_b, retardance_bin, and direction_bin with the shapes, dtypes, and ranges listed above. The supplied sample_submission.csv is valid but weak; it is a formatting template, not a competitive baseline. If the platform expects a file path, write the final CSV to ./working/submission.csv.
> Example submission rows:
> case_id,prediction_npz_b64
> spu_009fa288c320fb,<base64-encoded-npz>
> spu_02cc6e9f647e69,<base64-encoded-npz>
> spu_04e0e5a6d7a48f,<base64-encoded-npz>

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Wall Fixture Inspection Sheet Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78vwvjftgm7s1mcdfwn10vy98b4w1s
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview
> Each row contains a prepared 2 by 2 mosaic of wall-fixture photographs. Visible fixtures may include sockets, switches, and power strips. Predict the complete inspection sheet for the full mosaic: fixture count, counts by fixture type, 12 by 12 grid cells covered by fixtures, edge-near covered cells, one localized card for each visible fixture, and pairwise arrangement records for fixture pairs.
> This is a visual consistency task. The count fields, grid fields, fixture cards, and pair records must describe the same objects across all four mosaic panels. Fixtures vary in scale, background, orientation, grouping, and placement near borders.
> Dataset
> The released files are:
> train.csv: 2,648 completed examples.
> test.csv: 1,013 examples without answers.
> sample_submission.csv: 1,013 weak valid rows showing the required CSV and JSON format.
> images/: 3,661 transformed 512 by 512 JPEG mosaics referenced by image_path.
> Columns:
> id (string): unique row identifier.
> image_path (string): relative path to the image.
> prompt (string): fixed task instruction.
> image_context_json (JSON string): object with image_path (string), grid_rows (integer, 12), grid_cols (integer, 12), device_type_values (array[string]), and max_device_cards (integer, 12).
> answer_format_json (JSON string): output constraints, including grid dimensions, valid fixture types, valid bins, box format, and required answer fields.
> answer_json (JSON string, training only): target inspection sheet.
> Required answer_json fields:
> device_count (integer): number of fixture cards, from 0 to 12.
> device_counts (array[object]): one object per present type, with device_type (string) and count (integer). Valid types are power socket, power strip, and light switch.
> occupied_cells (array[string]): unique grid cells, named r00c00 through r11c11, touched by any fixture rectangle.
> edge_cells (array[string]): unique occupied cells belonging to fixtures whose centers are near the image border.
> device_cards (array[object]): one object per visible fixture, sorted top-to-bottom then left-to-right. Each card has device_id, device_type, center_cell, area_bin, aspect_bin, frame_zone, and box.
> arrangement_pairs (array[object]): one object per fixture pair, capped at 36. Each pair has a, b, type_pair, relation, distance_bin, and alignment. a and b are device ids with a < b; relation is one of above, below, left_of, right_of, or diagonal; distance_bin is near, mid, or far; alignment is same_row, same_col, or offset.
> box is normalized [x, y, width, height] with values from 0 to 1. area_bin is one of small, medium, large, or panel; aspect_bin is one of square, wide, or tall; frame_zone is one of center, edge, or corner.
> Example answer_json:
> {
> "device_count": 2,
> "device_counts": [{"device_type": "power socket", "count": 1}, {"device_type": "light switch", "count": 1}],
> "occupied_cells": ["r04c04", "r04c05", "r07c08"],
> "edge_cells": [],
> "device_cards": [
> {"device_id": "device_00", "device_type": "power socket", "center_cell": "r04c04", "area_bin": "medium", "aspect_bin": "square", "frame_zone": "center", "box": [0.33, 0.32, 0.18, 0.19]},
> {"device_id": "device_01", "device_type": "light switch", "center_cell": "r07c08", "area_bin": "small", "aspect_bin": "tall", "frame_zone": "center", "box": [0.66, 0.58, 0.07, 0.16]}
> ]
> }
> Evaluation
> Each row receives a score from 0 to 1. Malformed JSON or invalid values score 0 for that row, while other rows are still evaluated. The final score is the mean row score over all evaluated rows.
> raw_row_score =
> 0.01 * count_score
> + 0.03 * type_score
> + 0.10 * occupied_score
> + 0.04 * edge_score
> + 0.62 * device_card_score
> + 0.20 * arrangement_pair_score
> Definitions:
> arrangement_pair_score is duplicate-aware F1 over complete pair records (a, b, type_pair, relation, distance_bin, alignment).
> count_score is 1.0 only when device_count is exact, otherwise 0.0.
> type_score is duplicate-aware F1 over the expanded device-type multiset from device_counts.
> occupied_score starts from IoU(predicted_occupied_cells, true_occupied_cells), where IoU = intersection_size / union_size and empty-vs-empty IoU is 1. Values at or below 0.40 score 0; larger values score (IoU - 0.40) / 0.60.
> edge_score uses the same IoU definition on edge_cells. Values at or below 0.35 score 0; larger values score (IoU - 0.35) / 0.65.
> device_card_score greedily matches each true fixture card to the best unused predicted card. A matched-card score is 0.20 * device_type_exact + 0.44 * box_overlap_score + 0.20 * center_cell_exact + 0.06 * area_bin_exact + 0.05 * aspect_bin_exact + 0.05 * frame_zone_exact. box_overlap_score is 0 when box IoU is 0.25 or lower; otherwise it is (box_iou - 0.25) / 0.75. Cards with similarity below 0.72 are not matched. The row-level card score is the F1-style harmonic mean of matched-card precision and recall.
> box_iou is standard intersection-over-union between two normalized [x, y, width, height] rectangles.
> Submission
> Submit a CSV with exactly two columns:
> id (string): row id from test.csv.
> answer_json (JSON string): predicted inspection sheet using the schema above.
> id,answer_json
> electro_1111111111111111,"{""device_count"":1,""device_counts"":[{""device_type"":""power socket"",""count"":1}],""occupied_cells"":[""r05c05"",""r05c06"",""r06c05"",""r06c06""],""edge_cells"":[],""device_cards"":[{""device_id"":""device_00"",""device_type"":""power socket"",""center_cell"":""r05c06"",""area_bin"":""medium"",""aspect_bin"":""square"",""frame_zone"":""center"",""box"":[0.42,0.42,0.16,0.16]}]}"
> electro_2222222222222222,"{""device_count"":2,""device_counts"":[{""device_type"":""light switch"",""count"":1},{""device_type"":""power socket"",""count"":1}],""occupied_cells"":[""r03c04"",""r08c07""],""edge_cells"":[""r03c04""],""device_cards"":[{""device_id"":""device_00"",""device_type"":""light switch"",""center_cell"":""r03c04"",""area_bin"":""small"",""aspect_bin"":""tall"",""frame_zone"":""edge"",""box"":[0.32,0.20,0.08,0.18]},{""device_id"":""device_01"",""device_type"":""power socket"",""center_cell"":""r08c07"",""area_bin"":""large"",""aspect_bin"":""square"",""frame_zone"":""center"",""box"":[0.54,0.62,0.22,0.22]}]}"
> What Not To Use
> Do not use internet lookup.
> Do not use external electrical-fixture, product-image, or annotation datasets.
> Do not use any image, annotation table, metadata file, or answer source outside the released files.
> Do not infer labels from row order, original filenames, archive paths, or metadata.
> Do not use hosted inference APIs or remote services.
> Do not install packages at runtime or download code, weights, or checkpoints.
> Do not use pretrained models or checkpoints made from these rows.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Cavitation Collapse Forecasting From Pre-Collapse Shadowgraphy

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cp7wg1bha5yncwyk5698fp58a4jgb
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview
> A liquid cavity has been recorded shortly before it collapses. For each episode, use a silent high-speed shadowgraph sequence, its synchronized pressure-sensor prefix, and safe pre-event experimental metadata to reconstruct the next recorded stages of the collapse. Your submission must jointly produce four future silhouettes, the first collapse/rebound outcome, and the future pressure-shock envelope, with an honest confidence value.
> The core problem is temporal computer vision. A model must encode 48 ordered grayscale frames, follow the changing bubble boundary, preserve spatial geometry, and decode four pixel-level silhouette masks at later offsets. The event output also contains image-plane rebound displacement and area, so appearance, motion, segmentation, and geometric tracking all contribute directly to the score. The synchronized pressure sequence is a second modality that helps resolve visually similar prefixes with different collapse dynamics.
> This is a structured video-understanding and sensor-fusion task rather than ordinary classification, a single scalar regression, or current-frame segmentation. The hidden set holds out complete acquisition manoeuvres, so validate by grouping related training episodes rather than randomly splitting rows.
> The prepared corpus contains 96 training episodes from 24 physical bubbles and 40 hidden episodes from 10 different physical bubbles. All cutoffs from one bubble remain together, and the hidden bubbles belong to three acquisition manoeuvres that never appear in training. There are no missing public fields. This is therefore a compact, group-generalization challenge rather than an IID row-prediction task.
> Task
> Each row describes one prefix ending at cutoff_us. The privacy-processed video contains 48 chronological grayscale frames at 160 by 160 pixels and stops at the cutoff. The signal NPZ contains time_us with shape (64,) and pressure with shape (64,4). The four pressure channels are signed mean, RMS, peak magnitude, and high-frequency energy for synchronized prefix bins. They are normalized sensor-domain measurements; use their order and evolution rather than assuming physical volts. Every target occurs strictly after the available prefix.
> Predict one coupled future object:
> Four 48 by 48 silhouettes at 300, 700, 1200, and 1700 microseconds after the cutoff.
> First collapse time, first rebound time, rebound centroid displacement (dx and dy in pixels), and rebound area ratio.
> A 48-bin nonnegative pressure-shock envelope covering 2400 microseconds after the cutoff.
> Confidence in the correctness of the complete row.
> Intended Approach
> A practical A10G solution first decodes the MP4 into an ordered frame tensor. A 3-D CNN, video transformer, or 2-D backbone with temporal attention can learn boundary motion and produce multiscale visual tokens. A mask decoder then reconstructs the four 48 by 48 silhouettes, while pooled visual tokens support the image-plane event geometry. Encode the four-channel pressure sequence with a 1-D convolutional network or transformer, embed the numeric metadata, and fuse those features with the visual representation before the event, pressure, and confidence heads. Train all heads jointly, use legal image augmentations consistently across time, preserve sensor synchronization, and select models with manoeuvre-grouped validation. The silhouette contraction/rebound, event geometry, and pressure-shock evolution should describe one physically consistent outcome.
> The target environment is one NVIDIA A10G GPU with 24 GB VRAM, 64 GB system RAM, and a 30-minute end-to-end limit. A measured CUDA baseline completes in about two minutes. Offline pretrained vision weights are allowed when packaged with the submission; runtime downloads are not.
> What Not To Use
> Do not identify or retrieve the upstream raw experiments, match public files to outside media, or use external labels.
> Do not use filenames, row order, opaque-ID hashes, file bytes, or source reconstruction as prediction features.
> Do not access private answers, grader internals, hidden artifacts, or any non-public path.
> Do not reduce the task to one head, metadata lookup, fixed physics rules, or hand-authored templates.
> Do not download models, data, or code at runtime; package any allowed pretrained weights with the solution.
> Do not submit rule-only score chasing that bypasses learned video and pressure understanding.
> Approaches that violate these rules or do not align with temporal computer vision and pressure-sequence fusion may be rejected before payout.
> Evaluation
> The Mean Cavitation Vision-Dynamics Score is maximized and lies in [0,1].
> For a row, let M be the mean IoU of the four predicted and true masks. Empty-versus-empty IoU is 1; otherwise IoU is intersection divided by union.
> For event values, define:
> C = max(0, 1 - |collapse_us - truth| / 400)
> R = max(0, 1 - |rebound_us - truth| / 500)
> D = max(0, 1 - displacement_L2_error / 6)
> A = max(0, 1 - |area_ratio - truth| / 0.15)
> E = 0.35*C + 0.25*R + 0.25*D + 0.15*A
> Let P = max(0, 1 - RMSE / 0.40) for the 48 pressure values. The uncalibrated row score is:
> core = 0.45*M + 0.25*E + 0.30*P
> calibration = max(0, 1 - |confidence - core|)
> row = core * (0.90 + 0.10*calibration)
> The final score is the mean row score. A perfect submission scores 1.0. Wrong columns/order, wrong row count, duplicate or missing IDs, nonfinite/out-of-range confidence, or an ID-set mismatch raises InvalidSubmissionError and the submission is rejected. If any mask, event, or pressure cell is malformed, the complete affected row scores 0 while other structurally valid rows are still evaluated. This behavior is identical to grade.py.
> Dataset
> Public files
> Item	Description
> train.csv	Inputs and labels
> test.csv	Hidden-label inputs
> sample_submission.csv	Valid prior prediction
> train/videos/	Training MP4 files
> test/videos/	Test MP4 files
> train/signals/	Training NPZ files
> test/signals/	Test NPZ files
> train.csv
> Column	Type	Description
> id	string	Opaque episode ID
> video_path	string	Relative MP4 path
> pressure_path	string	Relative NPZ path
> cutoff_us	integer	Prefix end in us
> frame_rate_hz	float	Source sample rate
> microns_per_pixel_x	float	Horizontal scale
> microns_per_pixel_y	float	Vertical scale
> gravity_x_g	float	Gravity x in g
> gravity_y_g	float	Gravity y in g
> gravity_z_g	float	Gravity z in g
> cavity_pressure_kpa	float	Local static kPa
> vapor_pressure_kpa	float	Vapor kPa
> ambient_pressure_kpa	float	Ambient kPa
> pressure_calibration_uv_per_pa	float	Sensor calibration
> future_masks_json	JSON string	Four mask RLEs
> event_outcome_json	JSON string	Five event values
> pressure_future_json	JSON string	48 pressure values
> test.csv
> Column	Type	Description
> id	string	Opaque episode ID
> video_path	string	Relative MP4 path
> pressure_path	string	Relative NPZ path
> cutoff_us	integer	Prefix end in us
> frame_rate_hz	float	Source sample rate
> microns_per_pixel_x	float	Horizontal scale
> microns_per_pixel_y	float	Vertical scale
> gravity_x_g	float	Gravity x in g
> gravity_y_g	float	Gravity y in g
> gravity_z_g	float	Gravity z in g
> cavity_pressure_kpa	float	Local static kPa
> vapor_pressure_kpa	float	Vapor kPa
> ambient_pressure_kpa	float	Ambient kPa
> pressure_calibration_uv_per_pa	float	Sensor calibration
> Mask labels are a JSON list of four strings. Each string is a canonical row-major, zero-based RLE with space-separated start length pairs over 2304 pixels; "" is an empty mask. The event JSON has exactly collapse_us, rebound_us, rebound_dx_px, rebound_dy_px, and rebound_area_ratio. Times must satisfy 0 <= collapse_us < rebound_us <= 4500; displacements are in [-48,48]; area ratio is in [0,2]. Pressure JSON must have exactly 48 finite values in [0,8].
> Submission
> Write submission.csv with exactly the test IDs and this exact column order:
> Column	Type	Constraint
> id	string	Exact test ID
> future_masks_json	JSON string	Four valid RLEs
> event_outcome_json	JSON string	Exact five keys
> pressure_future_json	JSON string	48 values, 0 to 8
> confidence	float	From 0 to 1
> Save the final file at ./working/submission.csv. Use sample_submission.csv as a parser-safe template; it is a train-prior baseline, not hidden truth.
> A syntactically valid, deliberately weak one-row example is:
> id,future_masks_json,event_outcome_json,pressure_future_json,confidence
> cavf_0c6ca49d440e7c0d,"["""","""","""",""""]","{""collapse_us"":1500,""rebound_area_ratio"":0.35,""rebound_dx_px"":0,""rebound_dy_px"":0,""rebound_us"":2100}","[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]",0.2
> Your actual file must contain all 40 test IDs exactly once.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Machine-Sensed Cutting-Edge Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ct4gckvf7rnaz8sn7hws6rn8a8xmd
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, multimodal
- Best/top context found: Be the first to climb the leaderboard!; Top Score: not yet shown

Full challenge description from page:

> Overview
> Predict the current microscopic condition of a milling tool's cutting edge from indirect evidence collected while it is cutting.
> Task
> For each case, you receive:
> Input	Meaning
> previous_tool_image	Earlier microscope image of the same physical cutting edge
> chip_image	Photograph of chips produced during the current operation
> surface_image	Photograph of the machined surface produced during the current operation
> force_signal	Synchronized current Fx, Fy, Fz cutting-force sequence
> Your submission must reconstruct:
> Output	Meaning
> current_tool_image	Current microscope image of the cutting edge
> edge_loss_mask	Binary mask aligned to the reconstructed image; white marks newly lost/chipped edge material relative to the earlier image
> This is cross-modal image reconstruction and damage localization. It is not ordinary wear classification, scalar wear regression, metadata lookup, or tabular prediction. Good solutions should learn how chip morphology, surface texture, force dynamics, and the earlier edge appearance jointly constrain the current edge state.
> What Not To Do
> Using any of the approaches below is grounds for rejection on review, regardless of leaderboard score.
> Do not use source lookup, reverse-image search, original experiment names, raw filenames, source paths, physical tool IDs, blade IDs, run IDs, row order, file hashes, timestamps, wear labels, wear measurements, or public web copies to reconstruct hidden targets.
> Do not reduce the task to wear classification, scalar wear regression, current-wear-bin prediction, or tabular modeling.
> Do not submit the previous microscope image as the current image without solving the current reconstruction task.
> Do not ignore either output; the current image and edge-loss mask are both required.
> Do not use hosted APIs, hosted vision models, private files, internet access at inference time, or closed remote inference services.
> Do not exploit private/answers.csv, grader internals, file-system metadata, mtimes, CSV row order, malformed PNG payloads, or oversized image bombs.
> Do not submit wrong shapes, wrong modes, non-binary masks, missing IDs, extra IDs, duplicate IDs, reordered columns, or non-PNG payloads.
> Enforcement On Invalid Approaches
> Submissions that score through lookup, metadata reconstruction, private-file access, external hosted models, or rule-only shortcuts that do not solve the cross-modal current-edge reconstruction task may be rejected even if the CSV passes the grader.
> Intended Approach
> A strong solution should train a compact multimodal image-to-image model on the public training set. A practical route is:
> Encode the earlier tool image at target resolution.
> Resize and encode the chip and surface images.
> Convert the force signal into learned features or a rasterized time-series representation.
> Train a U-Net, UNet++, compact ViT decoder, or hybrid encoder-decoder to predict the RGB current edge and binary mask.
> Use image reconstruction losses, BCE/Dice mask losses, and extra weighting around the edge-loss region.
> Use the public split_role == validation rows for model selection. A complete strong solution should fit within 1.5 hours on A10G.
> Evaluation
> The metric is a normalized composite image score. Higher is better. The theoretical minimum is 0.0; the theoretical maximum is 1.0.
> For each test case, submit:
> Prediction field	Required payload
> current_tool_image_png_b64	Base64-encoded RGB PNG, exact size 600 x 194
> edge_loss_mask_png_b64	Base64-encoded grayscale PNG, exact size 600 x 194, values only 0 or 255
> The row score combines:
> Component	Weight
> Tool-image fidelity	0.42
> Edge-loss mask quality	0.38
> Image fidelity near true edge loss	0.15
> Cross-output consistency	0.05
> The four components are computed as follows, with every component clipped to [0,1]:
> Tool-image fidelity: 0.38 * MAE_score + 0.22 * RMSE_score + 0.22 * gradient_score + 0.13 * structure_score + 0.05 * edge_F1, where MAE_score = clip(1 - MAE/54), RMSE_score = exp(-RMSE/54), and gradient_score = clip(1 - gradient_MAE/38). structure_score is the grader's channel-wise global luminance/variance/covariance similarity, and edge_F1 compares gradient-threshold edge maps with a one-pixel tolerance on the predicted edge map.
> Edge-loss mask quality: 0.58 * tolerant_F1 + 0.20 * IoU + 0.15 * boundary_F1 + 0.07 * density_score. tolerant_F1 dilates the predicted mask by one pixel; boundary_F1 compares two-pixel mask boundaries with a two-pixel tolerance on the predicted boundary; and density_score = exp(-abs(predicted_density - true_density)/0.025).
> Image fidelity near true edge loss: inside the true mask dilated by five pixels, 0.58 * clip(1 - MAE/42) + 0.42 * clip(1 - gradient_MAE/32). If the true mask is empty, this component uses the full-image fidelity score.
> Cross-output consistency: the geometric mean of edge-loss mask quality and near-loss image fidelity.
> The final score blends mean performance and hidden robustness:
> Final = 0.85 * mean(row_score)
> + 0.15 * worst_subgroup_mean
> The robustness term evaluates confidential physically meaningful subgroups in the private test set. A perfect submission returns exactly 1.0.
> Global structural errors raise InvalidSubmissionError: wrong or reordered columns, missing IDs, extra IDs, duplicate IDs, blank IDs, an ID set mismatch, or overlarge payloads. Row-local corrupt base64, non-PNG payloads, wrong image mode, wrong image shape, or non-binary masks score zero for that row.
> Dataset
> The public split contains source-neutral prepared files only. It does not expose original experiment names, source filenames, source paths, physical tool IDs, blade IDs, run IDs, row order, timestamps, wear classes, wear measurements, source hashes, or private answer metadata.
> Checked prepared split:
> Train cases: 296
> Validation cases: 44
> Private test cases: 92
> Tool output size: 600 x 194
> Chip image size: 512 x 512
> Surface image size: 384 x 384
> Force signal shape: (3, 8192)
> Public prepared size: about 364.5 MB
> Private answer size: about 64.3 MB
> File overview
> Item	Description
> train.csv	Train/validation manifest with input and target paths
> test.csv	Test manifest with input paths only
> sample_submission.csv	Valid weak template
> train/images/*_previous_tool.png	Earlier microscope images
> train/images/*_chip.jpg	Current chip images
> train/images/*_surface.png	Current machined-surface images
> train/signals/*_force.npz	Current force signals
> train/targets/*_current_tool.png	Train current-edge targets
> train/targets/*_edge_loss_mask.png	Train binary mask targets
> test/images/*	Test input images
> test/signals/*	Test input force signals
> All paths are relative to the public dataset root.
> train.csv columns
> Column	Type	Description
> case_id	string	Opaque case ID
> split_role	string	train or validation
> previous_tool_image	path	Earlier microscope image
> chip_image	path	Current chip photograph
> surface_image	path	Current machined-surface photograph
> force_signal	path	Current force NPZ
> current_tool_image	path	Train target RGB PNG
> edge_loss_mask	path	Train target binary PNG
> test.csv columns
> Column	Type	Description
> case_id	string	Opaque case ID
> previous_tool_image	path	Earlier microscope image
> chip_image	path	Current chip photograph
> surface_image	path	Current machined-surface photograph
> force_signal	path	Current force NPZ
> force_signal NPZ contents
> Array	Shape	Type	Description
> force	(3,8192)	float32	Robust-normalized Fx/Fy/Fz signal
> sample_rate_hz	scalar	float32	1000.0
> axis_order	(3,)	uint8	[0,1,2]
> Submission
> Submit a CSV with exactly these columns in this order:
> case_id,current_tool_image_png_b64,edge_loss_mask_png_b64
> Column	Type	Constraint
> case_id	string	Same set as test.csv
> current_tool_image_png_b64	base64 PNG	RGB, 600 x 194
> edge_loss_mask_png_b64	base64 PNG	grayscale, 600 x 194, binary values
> Example:
> case_id,current_tool_image_png_b64,edge_loss_mask_png_b64
> te_004851dbf02e,<base64-rgb-png>,<base64-binary-mask-png>
> te_03e890a73395,<base64-rgb-png>,<base64-binary-mask-png>
> The supplied sample_submission.csv is valid but weak. If the platform expects a file path, write the final CSV to ./working/submission.csv.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Electrical-Tree Growth-Order Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bygnhwrx3gcc5afw7ngkdh58a24t3
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: video
- Best/top context found: Be the first to climb the leaderboard!; Top Score: not yet shown

Full challenge description from page:

> Overview
> A high-voltage polymer specimen can develop a branching electrical-breakdown tree. During a hidden interval, new conductive branches appear and split while partial-discharge activity evolves in phase with the applied voltage.
> For each case, you receive an optical microscopy anchor immediately before the interval, an optical anchor immediately after it, a synchronized phase-resolved partial-discharge (PRPD) video from the interval, and coarse strain context. Reconstruct which branch pixels first appeared in each of four temporal bins and the rooted parent/child growth graph that explains the branch-formation order.
> This is temporal physical reconstruction. It is not image classification, scalar regression, ordinary final-tree segmentation, missing-view completion, or a request to copy the after image. The after anchor exposes only the final union. A useful model must use synchronized temporal evidence to assign branch births and use physical connectivity to construct a rooted graph.
> GPU solutions are allowed and expected. Use the A10G - Standard ML workloads tier. The maximum solution runtime is 1.5 hours.
> Task
> For every test case_id, submit one strict JSON growth ledger containing:
> four disjoint 256×256 masks, where mask b contains only pixels born in temporal bin b;
> a rooted graph with branch segment identity, parent relation, birth bin, and a quantized endpoint on a finite 32×32 grid.
> The train labels were deterministically derived from real withheld optical frames through persistent change detection, rooted filtering, thin-structure processing, and temporal assignment. They are derived targets, not claimed human annotations.
> Intended Approach
> Use a GPU multimodal architecture. A strong starting point is a shared optical encoder for the before/after anchors, a temporal 3D-CNN or video-transformer encoder for the PRPD sequence, a small embedding for the strain context, and cross-attention or feature fusion between the final-tree geometry and discharge timeline. Decode four thin birth masks and a rooted segment graph jointly or in a geometry-aware second stage. Useful losses include class-balanced focal/Dice losses for sparse masks, topology-aware losses, discrete endpoint classification, parent-edge classification, and temporal-order supervision.
> The split is physical-specimen disjoint: every interval and derivative from one specimen stays on one side. Models must generalize to unseen specimens while the real coarse strain modes remain represented.
> What Not To Use / What Not To Do
> Do not recover or match prepared media to upstream public videos, source filenames, specimen/run identities, timestamps, frame indices, experiment order, or public-source records. Do not use runtime internet, hosted APIs, external answer services, runtime-downloaded weights, private files, grader internals, salted-ID inversion, row order, path strings, mtimes, file lengths, byte hashes, codec metadata, malformed JSON behavior, or fixed lookup maps as answer channels. Do not submit precomputed upstream labels, manually recovered test labels, a final-anchor copy presented as temporal reconstruction, or a hidden fallback such as disabling learned video models and silently switching to a metadata/interpolation hack when inference fails.
> Source lookup and external-answer recovery are prohibited even if an upstream source can be found. Submissions may be reviewed for retrieval, external calls, metadata-only behavior, fixed answer maps, private-answer access, and pipelines that bypass the required temporal multimodal reconstruction.
> Evaluation
> Each valid row receives four transparent components:
> temporal_mask = micro-aggregated thin-structure F1 over four bins
> with a 2-pixel spatial tolerance; matching stays within bin
> rooted_graph = 0.20 * matched_node_F1
> + 0.80 * matched_parent_edge_F1
> birth_order = geometry-match coverage
> * (0.40 * discrete_birth_bin_similarity
> + 0.60 * pairwise_birth_order_agreement)
> union = thin-structure F1 between the predicted and target growth unions
> with the same 2-pixel tolerance
> row_score = 0.50 * temporal_mask
> + 0.30 * rooted_graph
> + 0.15 * birth_order
> + 0.05 * union
> Graph segments are matched with deterministic minimum-cost bipartite matching using only their 32×32 endpoint geometry. A pair is eligible when endpoint distance is at most 4 grid cells. Birth bins are excluded from node matching and rooted-graph scoring, so the birth-order component does not receive duplicate credit through the graph match. Parent edges are evaluated only through the resulting geometry mapping and dominate the graph component.
> The leaderboard aggregate balances cases and real physical groups:
> final_score = 0.70 * mean_case_score
> + 0.20 * mean_of_physical_specimen_means
> + 0.10 * mean_of_real_strain_mode_means
> All terms lie in [0,1]; higher is better. The theoretical minimum is 0.0, maximum is 1.0, and a perfect ground-truth submission scores exactly 1.0. There is no score cap, nonlinear power, or hidden suppression curve.
> Submission-level structure is strict. Wrong or reordered columns, duplicate IDs, blank IDs, missing/extra/foreign IDs, an empty submission, or an oversized CSV raise InvalidSubmissionError. In an otherwise structurally valid submission, a row-local malformed, overlong, non-finite, out-of-range, cyclic, or schema-invalid JSON ledger scores zero only for that row. Grader errors do not reveal private labels, source groups, or answer content.
> Dataset
> The prepared public data contain de-identified optical anchors, synchronized cropped/re-encoded PRPD videos, coarse strain context, and train labels. Raw source titles, filenames, specimen/run identifiers, timestamps, frame counters, watermarks, audio, and identifying metadata are not participant inputs.
> File overview
> Item	Description
> train/images/*.jpg	before/after optical anchors for labeled cases
> train/prpd/*.mp4	synchronized 512×512, 48-frame PRPD evidence
> train/context/*.json	coarse strain mode and level
> test/images/*.jpg	before/after optical anchors for test cases
> test/prpd/*.mp4	synchronized test PRPD evidence
> test/context/*.json	coarse test strain context
> train.csv	public inputs plus target_json
> test.csv	public test inputs only
> sample_submission.csv	valid weak final-anchor/geodesic sample
> train.csv columns
> Column	Type	Description
> case_id	string	opaque row key
> before_image	string	path to the pre-interval optical anchor
> after_image	string	path to the post-interval optical anchor
> prpd_video	string	path to synchronized PRPD evidence
> strain_context	string	path to coarse context JSON
> time_bins	integer	always 4
> target_json	JSON string	temporal masks and rooted growth graph
> test.csv columns
> Column	Type	Description
> case_id	string	opaque row key
> before_image	string	pre-interval optical anchor path
> after_image	string	post-interval optical anchor path
> prpd_video	string	synchronized PRPD video path
> strain_context	string	coarse context JSON path
> time_bins	integer	always 4
> strain_context has exactly strain_mode (none, tensile, or compressive) and strain_level (none, low, mid, or high as applicable). It contains no specimen/run ID.
> Target and prediction JSON schema
> {
> "case_id": "et_0123456789abcdef",
> "growth_masks_rle": [
> {"bin": 0, "size": [256, 256], "rle": "..."},
> {"bin": 1, "size": [256, 256], "rle": "..."},
> {"bin": 2, "size": [256, 256], "rle": "..."},
> {"bin": 3, "size": [256, 256], "rle": "..."}
> ],
> "growth_graph": {
> "segments": [
> {"segment_id": "s0", "parent_id": "ROOT", "birth_bin": 0, "endpoint_bin": [15, 11]},
> {"segment_id": "s1", "parent_id": "s0", "birth_bin": 2, "endpoint_bin": [18, 9]}
> ]
> }
> }
> RLE is row-major, alternates background/foreground run counts starting with the background run, and must sum to 65536. The four masks must be pairwise disjoint. The graph must contain 1–64 segments. Segment IDs must be unique nonempty strings of at most 32 characters; every parent must be ROOT or another segment ID; the graph must be acyclic and have at least one root. birth_bin is an integer in [0,3]. endpoint_bin is [row_bin, column_bin] with two integers in [0,31]. Each complete JSON string is capped at 120,000 characters and must use exactly the documented keys.
> Submission
> Write ./working/submission.csv with exactly these columns in this order and exactly one row per test case:
> Column	Type	Constraint
> case_id	string	exact test ID set; each ID once
> prediction_json	JSON string	exact schema above; at most 120,000 characters
> Example CSV shape:
> case_id,prediction_json
> et_0123456789abcdef,"{...strict escaped JSON...}"

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Cavitation Ensemble Phase Topology

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73b3qtt9kq69p667256ghpqd8bqg3z
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, text, multimodal
- Best/top context found: Top Score | 0.390 | Created | Aug 2, 2026 | Start New Solution

Full challenge description from page:

> Overview
> Given one scientific evidence image, reconstruct three properties of an interacting bubble ensemble: the cyclic phase order of six labeled bubbles, three relative phase-coherence domains, and the drive-window interval where synchronization error is lowest.
> Ultrasonic bubble populations can behave like a coupled oscillator network. Individual bubbles may lead or lag one another around a cycle, several bubbles may lock into the same response group, and a low-error interval may appear as the acoustic drive changes. In sonochemical reactors and therapeutic-ultrasound systems, these relationships can be more informative than assigning one regime label to the entire recording.
> Each 1080 x 720 RGB JPEG contains:
> six labeled stroboscopic bubble traces, A through F;
> a synchronization-error trace over 31 consecutive drive settings;
> an acoustic-pressure trace over the same 31 settings.
> The task has three outputs with three different mathematical structures:
> | Output | Structure | Meaning |
> |---|---|---|
> | `cyclic_phase_order` | Directed cycle over six labels | The order in which bubbles occur around one oscillation cycle. Rotating the written cycle does not change its meaning. |
> | `lock_partition` | Three-part set partition of `A` through `F` | Which bubbles belong to the same relative phase-coherence domain. |
> | `clearing_interval` | Closed integer interval | The longest low-synchronization-error interval within the 31-position drive window. |
> The hidden data use a broadband scaling factor absent from training. This is not curve classification or scalar regression. A solver must recover a cycle, an equivalence relation, and an interval from the same evidence packet.
> Compute Budget
> Solutions run with one NVIDIA A10G GPU and a maximum wall-clock time of 30 minutes. The limit includes feature extraction, training, inference, and submission generation. GPU use is allowed but not required.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `public/train.csv` | Labeled training cases. |
> | `public/test.csv` | Evaluation cases with targets withheld. |
> | `public/sample_submission.csv` | Schema-valid baseline predictions. |
> | `public/images/` | Scientific phase-packet images referenced by the CSV files. |
> Prepared images are byte-unique. The numerical scaling factor used for hidden cases is held out as a group, and neither file paths nor opaque IDs expose it.
> The prepared dataset contains 1,100 training cases and 420 test cases. The three-domain target has 90 distinct partitions in training and 86 in the hidden split.
> The renderer preserves the source trajectories while varying trace color assignment and adding faint nuisance traces, measurement grids, short instrument-dropout bands, and low-amplitude sensor grain. These visual effects do not alter the reference targets.
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | String | Opaque identifier matching `cv[0-9a-f]{20}`. |
> | `phase_packet_path` | String | Relative JPEG path. The image contains six bubble traces on the left and two 31-position drive traces on the right. |
> Target Columns
> | Column | Data type | Description |
> |---|---|---|
> | `cyclic_phase_order` | String | Exactly six distinct labels joined by `>`. |
> | `lock_partition` | String | Exactly three nonempty groups joined by `|`; labels inside a group are joined by `+`. |
> | `clearing_interval` | JSON integer array | Exactly two integers `[start,end]` with `0 <= start <= end <= 30`. |
> Cyclic Order
> A>B>D>F>C>E describes directed edges A to B, B to D, D to F, F to C, C to E, and E to A. Any rotation, such as D>F>C>E>A>B, describes the same cycle. Reversing the sequence describes a different cycle.
> Lock Partition
> Every label must appear exactly once in exactly one of three groups. Group order and label order inside groups do not affect grading.
> A+C|B+D+F|E
> This example contains three relative coherence domains. To construct the reference, bubbles are placed in cyclic phase order. Each adjacent cyclic pair receives:
> boundary_score =
> 0.65 * cyclic_phase_gap / (2 * pi)
> + 0.35 * (1 - trace_correlation) / 2
> The three strongest boundaries cut the cycle into the three submitted domains. This relative construction remains informative even when all six traces are globally synchronized.
> Clearing Interval
> Positions are indexed from 0 at the left edge of the synchronization-error trace to 30 at its right edge. Both endpoints are included.
> [8,14]
> Submission Format
> Write:
> ./working/submission.csv
> The columns must appear exactly in this order:
> case_id,cyclic_phase_order,lock_partition,clearing_interval
> Example:
> case_id,cyclic_phase_order,lock_partition,clearing_interval
> cv0123456789abcdefabcd,A>B>D>F>C>E,A+C|B+D+F|E,"[8,14]"
> Submission rules:
> Supply exactly one row for every test ID.
> Extra columns, missing columns, reordered columns, duplicate IDs, missing IDs, and unknown IDs are rejected.
> A single backend-managed visibility column is tolerated and ignored.
> Cycles are limited to 40 characters.
> Partitions are limited to 60 characters.
> Intervals are limited to 30 characters and are parsed only as bounded JSON.
> A malformed component receives zero for that component.
> Evaluation
> The metric is the Bubble Phase Topology Score:
> Score =
> 0.34 * CycleScore
> + 0.38 * PartitionScore
> + 0.28 * ClearingIntervalScore
> Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> CycleScore
> Convert each six-label cycle into its six directed adjacent edges, including the final edge back to the first label.
> edge_agreement =
> number of true directed cycle edges submitted
> / 6
> exact_cycle = 1 if the submitted and true edge sets are identical, else 0
> row_cycle_score =
> 0.35 * edge_agreement
> + 0.65 * exact_cycle
> This makes the score invariant to cyclic rotation while preserving direction.
> PartitionScore
> There are 15 unordered label pairs among six bubbles. For each pair, compare whether the two labels are in the same submitted group and the same true group.
> pair_agreement =
> correctly matched same-group or different-group decisions
> / 15
> exact_partition = 1 if every submitted group equals a true group, else 0
> row_partition_score =
> 0.32 * pair_agreement
> + 0.68 * exact_partition
> ClearingIntervalScore
> For true interval T and prediction P, interval IoU uses inclusive integer positions:
> intersection =
> max(0, min(T.end, P.end) - max(T.start, P.start) + 1)
> union =
> max(T.end, P.end) - min(T.start, P.start) + 1
> interval_iou = intersection / union
> endpoint_score =
> max(0, 1 - (|T.start-P.start| + |T.end-P.end|) / 60)
> row_interval_score =
> 0.18 * endpoint_score
> + 0.32 * interval_iou
> + 0.50 * exact_interval
> Each component score is averaged over hidden cases before the weighted sum.
> Reference Validation
> An exact answer file scores 1.0. The provided sample submission scores 0.121574, and a train-mode constant submission scores 0.259772. Two clean preparations produced byte-identical outputs. No prepared image bytes or numerical scaling-factor groups cross the train-test boundary.
> Expected And Allowed Methods
> Allowed approaches include compact CNNs or vision transformers, mixed-precision image encoders, curve tracing, signal-shape descriptors, clustering over extracted traces, circular statistics, and constrained sequence decoders. A strong A10G solution may combine learned visual extraction with explicit cyclic and partition decoding, provided it completes within 30 minutes.
> What Not To Use
> Do not derive targets from opaque IDs, JPEG filenames, row ordering, file sizes, or hashes.
> Do not search for prepared packets in external repositories or match them to published source arrays.
> Do not use original simulation filenames, hidden scaling-factor metadata, private answer files, or unpublished intermediate records.
> Do not exploit cycle rotations to submit duplicate labels or malformed token strings.
> Do not submit duplicate IDs, extra columns, oversized JSON, or values intended to trigger parser or grader failures.
> Do not adapt model parameters on hidden test packets.
> What Makes This Interesting
> Most visual benchmarks represent order as a line and grouping as a class. Here, phase order is circular, so the first written label is arbitrary, while phase locking is an equivalence relation that may contain groups of different sizes. The third output is a contiguous interval on a separate trace. Solving all three requires a model to reconcile local oscillator shape with a population-level synchronization transition.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Same Instrument Matching Across the Register

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c8ymc9psyhddzpje7y13kyd8b2heg
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Top Score | 0.583 | Created | Jul 23, 2026 | Start New Solution

Full challenge description from page:

> Same-Instrument Matching Across the Register
> Overview
> You are given one query note and six candidate notes. Exactly one candidate was played
> on the same physical instrument as the query. Name that candidate's index.
> The difficulty is that you never hear the two notes in the same part of the instrument's range.
> Every candidate sits at least two octaves away from the query, and a note's sound changes
> wholesale across that distance: the low note and the high note of one instrument are not the
> same sound with the pitch moved, they are different sounds. So the query and its own match do
> not resemble each other in any direct way, while the five wrong candidates are chosen to
> resemble the right one closely.
> Three properties of how each row is put together decide what can and cannot work:
> Every candidate is the same kind of instrument. All six share the query's instrument
> family and the way it produces sound — six acoustic guitars, or six electronic organs. Naming
> the instrument therefore returns the same answer for all six and separates nothing.
> Every candidate is at nearly the same pitch. The six sit within a few semitones of one
> another, so the correct one is not the one at a distinctive pitch. How hard each note was
> struck is drawn independently of everything else.
> Every wrong candidate was chosen to sound like the right one. The five decoys are the
> notes whose overall character is closest to the true candidate's, so no coarse impression of
> the sound singles the right one out. They are drawn from a band rather than from the very
> closest matches available, so each row stays answerable rather than becoming a coin flip.
> What remains is the identity of the individual instrument — whatever about that instrument
> survives being played two octaves away.
> Task constraints
> The instruments are unseen. No instrument that appears in training appears in the test
> rows, so the match must be made for instruments encountered for the first time. What
> transfers is the general skill, not any particular instrument.
> No metadata is published. Pitch, loudness, instrument family, instrument type and
> instrument identity are all withheld. A row is seven sound patches and nothing else.
> Loudness carries nothing. Every patch is individually normalised, so overall level and
> gain are removed and only the shape of the sound remains.
> Position carries nothing. The correct index is spread evenly over 0…5, so always
> answering with the same index scores chance.
> Data
> Each note is published as a time–frequency patch: the first two seconds of the note —
> its onset and the sound as it settles — represented as a 64 × 42 grid of uint8 values.
> The 64 rows are frequency bands spaced by ear rather than linearly; the 42 columns are
> successive moments in time. Each patch is normalised on its own before being quantised.
> Files provided:
> train.npz — training inputs; holds the arrays ids, query and candidates described
> below, with N = 4,322 rows
> train.csv — training answers; two columns, id and prediction, described below
> test.npz — test inputs; the same three arrays as train.npz, with N = 3,579 rows
> sample_submission.csv — a correctly-formatted but deliberately weak example submission,
> with the same two columns as train.csv (id and prediction) and one row for each of the
> 3,579 test ids. It answers the same candidate index for every row, scores ≈ 0.16, and is
> provided to show the exact expected format rather than as a useful starting point.
> Arrays in train.npz / test.npz:
> ids — type str, shape (N,) — the row id, e.g. note_0a1b2c3d4e5f6071
> query — type uint8, shape (N, 64, 42) — the query note's patch; query[i] is the
> patch for row i
> candidates — type uint8, shape (N, 6, 64, 42) — the six candidate patches;
> candidates[i, k] is candidate k of row i, for k in 0…5
> Columns in train.csv:
> id — type string, e.g. note_0a1b2c3d4e5f6071 — matches an entry of ids in train.npz
> prediction — type integer, e.g. 3 — the index in 0…5 of the candidate played on the
> same instrument as the query
> You are given 4,322 training rows (each with the answer) and must give an answer for each
> of the 3,579 test rows.
> Evaluation
> The score is accuracy — the fraction of test rows whose predicted index is correct.
> score = (number of rows where prediction == truth) / 3,579
> Range 0–1, higher is better. Chance is 1/6 ≈ 0.167, and the provided
> sample_submission.csv scores ≈ 0.16.
> Submission format
> Submit submission.csv with exactly these two columns, in this order, one row per test id:
> id, prediction
> Example:
> id,prediction
> note_0a1b2c3d4e5f6071,3
> note_112233445566778a,0
> prediction must be a whole number in 0…5. A structural error (missing, extra or duplicate
> ids, wrong or extra columns, a non-numeric, non-integer or out-of-range prediction) makes the
> whole submission score 0.
> Rules — what you may and may not use
> The intended solution learns, from the released training rows alone, what makes two notes the
> same instrument. Everything below either protects that intent or protects the integrity of the
> test answers. A submission that breaks any prohibited rule is invalid regardless of score.
> Data — prohibited
> No external data of any kind. Do not fetch, download or otherwise bring in any audio
> corpus, instrument or note collection, impulse-response set, or sample library. The released
> train.npz and train.csv are the only permitted training material.
> No pretrained or third-party weights. Do not use any model whose parameters were fitted
> on data other than the released training rows, and do not download weights from anywhere.
> Every learned parameter in your solution must be fitted by you, here, on the released
> training rows. Ordinary library code that contains no fitted parameters is unrestricted.
> No identifying the source. Do not attempt to locate, name or download the collection the
> notes were taken from, and do not try to match a published patch back to any public
> recording. The patches are normalised, quantised and perturbed specifically to prevent this.
> No recovering the withheld metadata. The pitch, loudness, instrument family, instrument
> type and instrument identity of every note are deliberately withheld. Do not reconstruct them
> from an outside source, and do not obtain them from anywhere other than what the released
> arrays themselves contain.
> Labels — prohibited
> No test answers. The answers for the test rows are withheld and must stay that way. Do
> not source them, guess at them from outside the released data, or hand-write them.
> No labelling test rows by hand. Answers must come from a procedure that runs on the test
> inputs. Do not listen to, inspect and annotate test rows yourself, individually or in bulk,
> and do not have any person or outside service annotate them for you.
> Answer each row from its own seven patches. A row is answered using the query and the six
> candidates given in that row. Do not compare patches across different rows, and do not carry
> an answer from one row to another. Anything derived from how the rows happen to sit together
> in the release exploits the packaging rather than solving the task.
> No probing the score. Do not use repeated scored submissions to infer individual test
> answers, and do not tune anything against a score that was obtained that way.
> No answers baked into the submission. Predictions must be produced by your model at
> inference time. A submission.csv containing hard-coded, per-id or manually adjusted entries
> is invalid.
> Process — required
> The solution must be a learned model. Predictions must come from a model whose parameters
> were fitted on the released training rows and their answers. A fixed rule, a hand-tuned
> formula, or a similarity score with constants chosen by hand is not an acceptable solution
> even if it scores above chance — the training answers exist to be learned from, and a method
> that does not use them is out of scope.
> Train only on training rows. Model fitting uses train.npz and train.csv only. You may
> read the test inputs to predict on them, but the test rows must never contribute to fitting
> parameters, selecting a model, or tuning anything.
> Hold out honestly. Any validation split you make must be drawn from the training rows,
> and the test answers must play no part in choosing between approaches.
> Reproducible inference. Fixed seeds and deterministic decoding — re-running your solution
> on test.npz must reproduce the same submission.csv and the same score.
> Documented method. The approach should be described clearly enough that a reader can see
> how a patch is turned into a prediction and can re-run it.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Slide Microfragment Radial Ordering Certificate

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c0ct5wn385e245541010yrx8bmekx
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Top Score | — | Created | Aug 1, 2026 | Start New Solution

Full challenge description from page:

> Overview
> Given one transformed composite microscope field image, recover a radial ordering certificate for the annotated microfragments visible across the nine tiled subfields. The images show small mineralized or fossil-like particles on slide micrographs; each released image is a deterministic 3 by 3 tile made from same-split annotated fields. Each visible mark belongs to one of three released annotation families, type_a, type_b, and type_c.
> The submitted JSON is an ordered certificate, not a segmentation mask, box list, image tag, or generic object graph. It asks for the fragments in clockwise radial order around the image center, with each ordered node carrying its family, zone, sector, radius band, shape, size, and approximate box. The certificate also includes sector-level counts, rim/edge counts, and transition steps between consecutive ordered fragments.
> Dataset
> The released files are:
> train.csv: labeled examples with row_id, image_path, and microfragment_certificate_json.
> test.csv: unlabeled examples with row_id and image_path.
> sample_submission.csv: valid submission skeleton with one row per test image.
> images/: transformed microscope images referenced by train.csv and test.csv.
> Columns:
> row_id (string): opaque row identifier.
> image_path (string): relative path to the transformed microscope image.
> microfragment_certificate_json (JSON string, train and submission only): radial-order certificate for the image window.
> microfragment_certificate_json must be a JSON object with exactly six keys:
> mark_count: integer from 0 to 30.
> type_counts: object with integer counts for type_a, type_b, and type_c.
> sector_counts: list of family/sector density records.
> edge_summary: object with rim and edge-touch counts.
> radial_order: ordered fragment nodes, capped at 24.
> transition_steps: consecutive-step records between ranked fragments.
> Each type_counts object must contain exactly type_a, type_b, and type_c, and the values must sum to mark_count.
> Each sector_counts item has:
> type: one of type_a, type_b, type_c.
> sector: one of s0 through s11, where sectors divide the image plane around the center.
> density: one of one, two, three, four_plus.
> Each radial_order item has:
> rank: integer from 0 to 23. Rank 0 is the first retained fragment in clockwise radial order.
> type: one of type_a, type_b, type_c.
> zone: one of the 64 cells from r0c0 through r7c7.
> sector: one of s0 through s11.
> radius_band: one of center, inner, outer, rim.
> scale: one of pinpoint, small, medium, large.
> aspect: one of needle, oval, compact.
> bbox: [center_x, center_y, width, height] as normalized floats rounded to three decimals.
> For crowded windows, radial_order is capped at 24 fragments. The source ordering is clockwise sector first, then distance from image center, with stable tie-breaking.
> Each transition_steps item has:
> from_rank: integer rank.
> to_rank: integer rank equal to from_rank + 1.
> type_pair: sorted family pair joined by |, for example type_a|type_b.
> sector_step: one of same, short, medium, long, opposite.
> radius_delta: one of inward, flat, outward.
> distance: one of near, middle, far.
> edge_summary has:
> rim_count: integer from 0 to 30.
> edge_touch_count: integer from 0 to 30.
> Example target:
> {"edge_summary":{"edge_touch_count":0,"rim_count":1},"mark_count":2,"radial_order":[{"aspect":"oval","bbox":[0.24,0.39,0.05,0.03],"radius_band":"inner","rank":0,"scale":"small","sector":"s5","type":"type_a","zone":"r2c1"},{"aspect":"needle","bbox":[0.67,0.72,0.04,0.11],"radius_band":"outer","rank":1,"scale":"medium","sector":"s1","type":"type_b","zone":"r4c4"}],"sector_counts":[{"density":"one","sector":"s1","type":"type_b"},{"density":"one","sector":"s5","type":"type_a"}],"transition_steps":[{"distance":"far","from_rank":0,"radius_delta":"outward","sector_step":"opposite","to_rank":1,"type_pair":"type_a|type_b"}],"type_counts":{"type_a":1,"type_b":1,"type_c":0}}
> Evaluation
> Higher is better. Each row receives a score from 0 to 1:
> row_score = 0.05*mark_count_exact + 0.08*type_count_similarity + 0.12*sector_count_f1 + 0.07*edge_numeric_closeness + 0.60*radial_order_score + 0.08*transition_component
> type_count_similarity is the sum of per-type count intersections divided by the sum of per-type count unions:
> sum(min(pred_count_t, true_count_t) for t in type_a,type_b,type_c) / sum(max(pred_count_t, true_count_t) for t in type_a,type_b,type_c).
> sector_count_f1 and transition F1 use complete-record matching after duplicate-key validation. Convert each valid submitted record and true record into a tuple, count tuples, then compute matches = sum(min(pred_count(tuple), true_count(tuple))). Precision is matches / submitted_tuple_count, recall is matches / true_tuple_count, and F1 is 2*precision*recall/(precision+recall). If both tuple sets are empty, F1 is 1; if only one is empty, F1 is 0.
> edge_numeric_closeness averages two normalized closeness scores, one for rim_count and one for edge_touch_count. For each numeric field, closeness = 1 - min(1, abs(predicted - true) / max(1, true_mark_count)).
> radial_order_score compares submitted and true nodes by rank. A submitted node with the wrong rank or wrong type receives 0 for that true node. For the correct type at the correct rank, similarity is (0.18 + 0.20*zone_exact + 0.15*sector_exact + 0.12*radius_band_exact + 0.08*scale_exact + 0.07*aspect_exact + 0.20*bbox_closeness) * zone_gate, where zone_gate is 1.0 when the zone matches and 0.35 otherwise. bbox_closeness = max(0, 1 - mean_absolute_bbox_error / 0.025). The total is divided by the larger of submitted-node count, true-node count, and 1.
> transition_component is transition-step F1 when the true row has at least one transition step. If the true row has no transition steps, this component is 1 only when the submitted transition list is also empty; otherwise it is 0.
> Malformed JSON, invalid keys, invalid categories, duplicate sector entries, duplicate ranks, invalid transition steps, or type counts that do not sum to mark_count score 0 for that row. A submission with missing rows, extra rows, duplicate ids, wrong ids, or wrong columns is rejected.
> Submission
> Submit a CSV with exactly these columns in this order:
> row_id,microfragment_certificate_json
> micro_example_01,"{""edge_summary"":{""edge_touch_count"":0,""rim_count"":1},""mark_count"":1,""radial_order"":[{""aspect"":""oval"",""bbox"":[0.42,0.51,0.04,0.03],""radius_band"":""inner"",""rank"":0,""scale"":""small"",""sector"":""s0"",""type"":""type_a"",""zone"":""r2c3""}],""sector_counts"":[{""density"":""one"",""sector"":""s0"",""type"":""type_a""}],""transition_steps"":[],""type_counts"":{""type_a"":1,""type_b"":0,""type_c"":0}}"
> What Not To Use
> Do not use external datasets or source lookup.
> Do not use unreleased answer files or any file not included in the released data.
> Do not use hosted inference APIs.
> Do not install packages at runtime.
> Do not use downloaded code or challenge-specific checkpoints.
> Do not hard-code answers for the released test ids.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Bubble Plume Cell Contour Profile Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71tgn9g046k3e3w8dnns8vhs8bj729
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Top Score | 0.441 | Created | Jul 31, 2026 | Start New Solution

Full challenge description from page:

> Overview
> Each row contains a 128 by 128 grayscale image crop centered on one air bubble rising through liquid in a laboratory plume experiment. The task is to predict a structured shape record for that bubble on a fixed 16 row by 16 column grid laid over the crop.
> In plain terms, identify which coarse grid cells belong to the bubble, which of those cells lie on its boundary, where its centroid falls, whether it touches an image edge, and a few binned measurements describing size, span, and contour roughness. These records summarize real bubble silhouettes from experimental fluid-imaging data; original acquisition identifiers are not part of the released files.
> Dataset
> The released files are:
> train.csv: 2,500 labeled examples.
> test.csv: 1,000 held-out examples.
> sample_submission.csv: 1,000 weak valid rows showing the required CSV and JSON shape.
> images/: 3,500 normalized grayscale PNG crops referenced by image_path; each image is 128 by 128 pixels.
> CSV columns:
> id (string): Unique row identifier.
> image_path (string): Relative path to the PNG crop in images/.
> prompt (string): Row instruction.
> image_context_json (JSON object): Image and grid context with these fields:
> image_path (string): Same relative image path.
> image_size_px (array of two integers): Width and height in pixels, always [128, 128].
> grid_rows (integer): Number of grid rows, always 16.
> grid_cols (integer): Number of grid columns, always 16.
> profile_parts (array of strings): Names of the shape components to recover.
> answer_format_json (JSON object): Output constraints with these fields:
> type (string): Always object.
> required_fields (array of strings): Required keys in answer_json.
> grid_rows (integer) and grid_cols (integer): Required grid size.
> cell_pattern (string): Valid cell-token range, r00c00 through r15c15.
> boundary_touch_flags_allowed (array of strings): Allowed edge flags: top, bottom, left, right.
> run_formats (array of strings): Row and column silhouette run formats.
> bins (JSON object): Allowed values for the binned area, width, height, and roughness fields.
> answer_json (JSON object, train only): Ground-truth bubble shape record using the schema below.
> Target JSON
> answer_json must contain exactly these fields:
> mask_area_band (string): Coarse foreground-area bin, one of area00 through area06; larger suffixes indicate larger bubble support.
> width_span_bin (string): Coarse horizontal span bin, one of width00 through width05.
> height_span_bin (string): Coarse vertical span bin, one of height00 through height05.
> boundary_touch_flags (array of strings): Unique list of crop edges touched by the bubble support, using only top, bottom, left, and right.
> occupied_cells (array of strings): Unique 16 by 16 grid cells occupied by the bubble support. Cells use r00c00 through r15c15.
> contour_cells (array of strings): Unique occupied cells on the coarse bubble boundary. Every contour cell must also appear in occupied_cells.
> centroid_cell (string): Grid cell containing the bubble-support centroid.
> contour_roughness_bin (string): Coarse boundary irregularity bin, one of rough00 through rough06; larger suffixes indicate a less smooth coarse contour.
> row_silhouette_runs (array of strings): Unique row-run strings such as r05:c03-12. Each string gives one contiguous occupied interval in a row.
> column_silhouette_runs (array of strings): Unique column-run strings such as c07:r02-14. Each string gives one contiguous occupied interval in a column.
> Example:
> {"boundary_touch_flags":[],"centroid_cell":"r07c08","column_silhouette_runs":["c07:r07-08","c08:r07-08"],"contour_cells":["r07c07","r07c08","r08c07","r08c08"],"contour_roughness_bin":"rough02","height_span_bin":"height03","mask_area_band":"area03","occupied_cells":["r07c07","r07c08","r08c07","r08c08"],"row_silhouette_runs":["r07:c07-08","r08:c07-08"],"width_span_bin":"width02"}
> Evaluation
> Each row first receives a component-weighted raw score:
> raw_row_score =
> 0.27 * occupied_cell_score
> + 0.20 * contour_cell_score
> + 0.14 * row_silhouette_score
> + 0.14 * column_silhouette_score
> + 0.08 * centroid_score
> + 0.06 * area_band_score
> + 0.04 * span_bin_score
> + 0.04 * roughness_bin_score
> + 0.03 * boundary_touch_score
> The final per-row score applies a strictness transform:
> row_score = raw_row_score ^ 4.0
> This transform keeps perfect rows at 1.0, keeps malformed rows at 0.0, and reduces credit for broad base-rate guesses that are only partially correct across many fields.
> For any set-valued field, intersection over union is:
> set_iou(predicted, true) = |predicted intersection true| / |predicted union true|
> If both sets are empty, the IoU is 1.0. Otherwise an empty/nonempty mismatch has IoU 0.0.
> Component definitions:
> occupied_cell_score = set_iou(predicted_occupied_cells, true_occupied_cells) ^ 1.25. The exponent makes near-miss masks lose more credit than plain IoU while still preserving partial credit.
> contour_cell_score = set_iou(predicted_contour_cells, true_contour_cells) ^ 1.15.
> row_silhouette_score = set_iou(predicted_row_silhouette_runs, true_row_silhouette_runs).
> column_silhouette_score = set_iou(predicted_column_silhouette_runs, true_column_silhouette_runs).
> boundary_touch_score = set_iou(predicted_boundary_touch_flags, true_boundary_touch_flags).
> centroid_score = exp(-d / 2.0), where d is Manhattan distance between predicted and true centroid cells on the 16 by 16 grid.
> area_band_score = exp(-abs(predicted_area_index - true_area_index)), where area03 has index 3.
> width_bin_score = exp(-abs(predicted_width_index - true_width_index)).
> height_bin_score = exp(-abs(predicted_height_index - true_height_index)).
> span_bin_score = 0.5 * width_bin_score + 0.5 * height_bin_score.
> roughness_bin_score = exp(-abs(predicted_roughness_index - true_roughness_index)).
> The final leaderboard score is the arithmetic mean of row_score over all held-out rows.
> Malformed JSON, missing fields, extra fields, invalid cells, duplicate unique-list values, invalid bins, invalid run strings, or contour cells outside the occupied cells score zero for that row. A submission with missing rows, extra rows, duplicate ids, wrong ids, or wrong columns is rejected.
> Submission
> Submit a CSV with exactly these columns in this order:
> id,answer_json
> bpcp_test_example,"{""boundary_touch_flags"":[],""centroid_cell"":""r07c08"",""column_silhouette_runs"":[""c07:r07-08"",""c08:r07-08""],""contour_cells"":[""r07c07"",""r07c08"",""r08c07"",""r08c08""],""contour_roughness_bin"":""rough02"",""height_span_bin"":""height03"",""mask_area_band"":""area03"",""occupied_cells"":[""r07c07"",""r07c08"",""r08c07"",""r08c08""],""row_silhouette_runs"":[""r07:c07-08"",""r08:c07-08""],""width_span_bin"":""width02""}"
> What Not To Use
> Do not use internet lookup.
> Do not use external datasets or external annotations.
> Do not infer answers from row order, original filenames, archive paths, or hidden metadata.
> Do not use unreleased answer files or any file not included in the released data.
> Do not use hosted inference APIs or remote services.
> Do not install packages during solution execution or download code, weights, or checkpoints.
> Do not use challenge-specific pretrained models or checkpoints.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Hive Entrance Flow Record Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73q3azf1qd82rgm796gt79r18b5kxz
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, video, multimodal
- Best/top context found: Top Score | — | Created | Jul 24, 2026 | Start New Solution

Full challenge description from page:

> Overview
> Small entrance cameras can capture rapid insect traffic near a nest opening, but the same individual may be visible in only one or two neighboring frames. In this challenge, each row gives three consecutive transformed camera frames: the previous frame, the current frame, and the next frame. Your task is to recover a compact movement record for the current frame.
> For every current-frame row, predict how many insects are visible, which grid cells they occupy, which cells contain overlapping insects, how many are near the left and right image edges, and a short list of movement cards. A movement card describes one visible insect in the current frame using its current cell, optional previous/next cells, motion direction, size bin, and normalized rectangle.
> The records are designed to reward visual localization and short-range motion reasoning across the three images. Labels come from frame-level tracking annotations made on the original camera footage, then converted into the compact record format used here.
> Dataset
> Files:
> train.csv: 1,800 training rows with input image paths and answer_json.
> test.csv: 650 evaluation rows with the same input fields, without answers.
> sample_submission.csv: 650 weak valid example submission rows.
> images/: 4,945 transformed frame images referenced by the CSV files.
> Columns in train.csv:
> id (string): row identifier.
> prev_image_path (string): path to the previous transformed frame.
> cur_image_path (string): path to the current transformed frame.
> next_image_path (string): path to the next transformed frame.
> packet_json (JSON string): grid shape and allowed token values.
> answer_format_json (JSON string): required output fields.
> answer_json (JSON string): target record for the current frame.
> Columns in test.csv are the same except answer_json is omitted.
> answer_json must contain:
> bee_count (integer): number of visible insects in the current frame.
> occupied_cells (array[string]): sorted grid cells containing at least one current-frame insect.
> cluster_cells (array[string]): sorted grid cells containing two or more current-frame insects.
> left_edge_count (integer): number of current-frame insects touching the left edge region.
> right_edge_count (integer): number of current-frame insects touching the right edge region.
> motion_counts (object): counts for arriving, leaving, leftward, rightward, upward, downward, nearly_still, and single_frame.
> flow_cards (array[object]): up to 12 cards sorted by current cell. Each card has center_cell, prev_cell, next_cell, motion, size_bin, and box.
> Grid cells use the format r00c00 through r09c13. prev_cell and next_cell may be null when the same individual is not visible in that neighboring frame. box is [x1, y1, x2, y2] normalized to the current transformed image, with values from 0.0 to 1.0.
> Example answer:
> {
> "bee_count": 2,
> "occupied_cells": ["r06c08", "r07c08"],
> "cluster_cells": [],
> "left_edge_count": 0,
> "right_edge_count": 0,
> "motion_counts": {
> "arriving": 0,
> "leaving": 1,
> "leftward": 0,
> "rightward": 1,
> "upward": 0,
> "downward": 0,
> "nearly_still": 0,
> "single_frame": 0
> },
> "flow_cards": [
> {
> "center_cell": "r06c08",
> "prev_cell": "r06c07",
> "next_cell": "r06c09",
> "motion": "rightward",
> "size_bin": "small",
> "box": [0.58, 0.63, 0.62, 0.70]
> },
> {
> "center_cell": "r07c08",
> "prev_cell": "r07c08",
> "next_cell": null,
> "motion": "leaving",
> "size_bin": "tiny",
> "box": [0.59, 0.73, 0.62, 0.78]
> }
> ]
> }
> Evaluation
> The score is the mean row score over all evaluated rows. Higher is better. Each row first receives this raw score:
> 0.02 * count_score + 0.22 * occupied_score + 0.06 * cluster_score + 0.02 * left_edge_score + 0.02 * right_edge_score + 0.06 * motion_count_score + 0.75 * flow_card_score
> count_score = exact-or-zero count term; old exp(-abs(predicted_count - true_count) / 0.6).
> left_edge_score and right_edge_score use the same formula with denominator 0.5.
> occupied_score and cluster_score are thresholded F1 scores over predicted and true cell sets:
> precision = matched_cells / predicted_cells, recall = matched_cells / true_cells, and F1 = 2 * precision * recall / (precision + recall). If both sets are empty, the F1 score is 1.0; if only one is empty, it is 0.0. The thresholded score is 0 when F1 <= 0.35; otherwise it is (F1 - 0.35) / 0.65.
> motion_count_score is the average count score over motion values that are nonzero in either the predicted or true record, using denominator 0.5. If both records contain no motion counts, this component is 1.0.
> flow_card_score greedily matches each true card to the unused predicted card with the highest card similarity. Card similarity is:
> 0.26 * center_cell_match + 0.08 * prev_cell_match + 0.08 * next_cell_match + 0.24 * motion_match + 0.08 * size_bin_match + 0.26 * box_overlap_score
> box_overlap_score is 0 when box IoU is 0.30 or lower; otherwise it is (box_iou - 0.30) / 0.70. A predicted card is matched only if its best similarity is at least 0.65. The matched-card average is multiplied by matched_predicted_cards / submitted_cards to penalize extra cards.
> Malformed JSON, invalid cells, invalid motion values, invalid boxes, or more than 12 cards score zero for that row. File-level problems such as missing rows, duplicate ids, wrong ids, missing columns, or extra columns reject the submission.
> Submission
> Submit a CSV with exactly two columns:
> id (string)
> answer_json (JSON string)
> Example:
> id,answer_json
> bee_1111111111111111,"{""bee_count"":0,""occupied_cells"":[],""cluster_cells"":[],""left_edge_count"":0,""right_edge_count"":0,""motion_counts"":{""arriving"":0,""leaving"":0,""leftward"":0,""rightward"":0,""upward"":0,""downward"":0,""nearly_still"":0,""single_frame"":0},""flow_cards"":[]}"
> bee_2222222222222222,"{""bee_count"":1,""occupied_cells"":[""r04c06""],""cluster_cells"":[],""left_edge_count"":0,""right_edge_count"":0,""motion_counts"":{""arriving"":0,""leaving"":0,""leftward"":0,""rightward"":0,""upward"":0,""downward"":0,""nearly_still"":0,""single_frame"":1},""flow_cards"":[{""center_cell"":""r04c06"",""prev_cell"":null,""next_cell"":null,""motion"":""single_frame"",""size_bin"":""small"",""box"":[0.44,0.41,0.49,0.48]}]}"
> What Not To Use
> Do not use external datasets, downloaded model weights, or hosted vision APIs.
> Do not manually search for matching frames or original camera footage.
> Do not use labels or files outside the provided competition data.
> Do not hard-code row ids or memorize the sample submission.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Leaf Health Markup Report Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71nphzvaf8ftg36xhp9tkfcx8b5h64
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, feature-engineering
- Best/top context found: Top Score | — | Created | Jul 24, 2026 | Start New Solution

Full challenge description from page:

> Overview
> Each row contains a prepared 2 by 2 crop-leaf inspection mosaic with localized disease symptoms or pest marks. Predict the complete answer_json markup report for the full mosaic: number of non-healthy marked regions, counts by visible mark type, the 8 by 8 cells touched by damage, a total-area severity bin, the dominant damaged cell, edge-touch flags, and up to twelve localized damage cards.
> The images come from an annotated agricultural leaf-damage collection. The source annotations mark rectangular regions for disease or pest symptoms on leaf photos collected under varied lighting, background, scale, and leaf orientation. The released mosaics combine several annotated panels into one inspection image, so a correct answer must account for multiple leaves and keep the region cards, grid cells, counts, and edge flags consistent.
> Dataset
> Files:
> train.csv: 3,000 labeled examples.
> test.csv: 1,000 unlabeled examples.
> sample_submission.csv: 1000 valid weak baseline rows.
> images/: 4,000 RGB JPEG mosaic images referenced by the CSV files. Images are 640 by 640 pixels.
> Columns in train.csv:
> id (string): row identifier.
> image_path (string): relative path to the JPEG image in images/.
> prompt (string): short task instruction.
> profile_schema_json (JSON string): row schema and allowed values. It contains:
> grid (object): rows and cols, both integers and both equal to 8; cell_format is r{row}_c{col}.
> native_class_names (array[string]): allowed mark names: dark rot patch, brown blight patch, rust-colored patch, mite stippling patch, insect feeding patch, healthy leaf region, pale spot patch, and general disease patch.
> severity_area_bins (array[string]): allowed area bins: none, trace, low, moderate, and high.
> bbox_format (array[string]): [x_center, y_center, width, height].
> card_fields (array[string]): required fields for each damage card.
> max_damage_cards (integer): maximum number of damage cards, always 12.
> required_fields (array[string]): required top-level keys in answer_json.
> answer_json (JSON string, train only): target markup report.
> Columns in test.csv are the same except answer_json is omitted.
> Target JSON
> Each answer_json must contain exactly these fields:
> damage_box_count (integer): count of non-healthy annotated regions, from 0 to 12.
> class_counts (object): map from visible non-healthy mark name to integer count. Zero-count classes may be omitted.
> occupied_cells (array[string]): sorted array of 8 by 8 cell tokens such as r2_c3; each listed cell is touched by at least one damage region.
> severity_area_bin (string): one of none, trace, low, moderate, or high, based on total marked damage area.
> dominant_damage_zone (string): the occupied cell with the greatest damage-box overlap, or none when there is no damage.
> edge_touch_flags (object): booleans left, right, top, bottom, and any. The any value must equal the OR of the four side flags.
> damage_cards (array[object]): up to twelve objects, ordered by largest area first. Each card has:
> class_name (string): one non-healthy mark name.
> bbox (array[number]): normalized [x_center, y_center, width, height].
> center_cell (string): 8 by 8 grid cell containing the box center.
> area_bin (string): one of trace, low, moderate, or high.
> edge_touch (array[string]): any subset of left, right, top, and bottom.
> Bounding boxes use normalized [x_center, y_center, width, height] coordinates.
> Evaluation
> The score is the mean row score across test rows. First compute:
> raw_row_score =
> 0.02 * damage_box_count_score
> + 0.17 * class_count_F1
> + 0.21 * occupied_cell_F1
> + 0.03 * severity_bin_exact
> + 0.05 * dominant_zone_exact
> + 0.02 * edge_flag_accuracy
> + 0.59 * damage_card_score
> The count score is 1.0 for an exact count; otherwise it is 0.20 * max(0, 1 - abs(predicted - true) / max(1, predicted, true)).
> class_count_F1 and occupied_cell_F1 use multiset overlap. If both sides are empty, the F1 value is 1; if exactly one side is empty, it is 0. These F1 values are then thresholded: scores at or below 0.50 become 0, and larger scores become (F1 - 0.50) / 0.50.
> Damage cards are greedily matched. For each true card, the grader chooses the unused predicted card with highest similarity:
> bbox_score = exp(-mean_abs_bbox_error / 0.020)
> card_similarity =
> 0.22 * class_name_exact
> + 0.18 * center_cell_exact
> + 0.10 * area_bin_exact
> + 0.10 * edge_touch_F1
> + 0.40 * bbox_score
> Cards with similarity below 0.75 are not matched and contribute 0. The final damage_card_score is the sum of matched similarities divided by max(number_of_predicted_cards, number_of_true_cards, 1).
> Invalid JSON or malformed values score zero for that row. A submission with wrong columns, duplicate ids, missing ids, or extra ids is rejected.
> Submission Format
> Submit a CSV with exactly two columns:
> id,answer_json
> leaf_example,"{""damage_box_count"":1,""class_counts"":{""rust-colored patch"":1},""occupied_cells"":[""r2_c3""],""severity_area_bin"":""low"",""dominant_damage_zone"":""r2_c3"",""edge_touch_flags"":{""left"":false,""right"":false,""top"":false,""bottom"":false,""any"":false},""damage_cards"":[{""class_name"":""rust-colored patch"",""bbox"":[0.68,0.48,0.12,0.16],""center_cell"":""r2_c3"",""area_bin"":""low"",""edge_touch"":[]}]}"
> What Not To Use
> Do not use external image collections or searched copies of the test images.
> Do not use online services or hosted vision APIs.
> Do not hard-code answers, row ids, image filenames, or values not present in the released test inputs.
> Do not submit extra columns or omit required rows.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Source Recovery Prediction in Crowded Astronomical Images

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx790x3rb3zaze9k6cpxqgtpen8a236e
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Top Score | 0.573 | Created | Jul 8, 2026 | Start New Solution

Full challenge description from page:

> CrowdMiss: Will the Faint Source Be Recovered in the Crowd?
> Automated source-detection pipelines that measure stars in dense fields do not recover every
> source: whether a faint point source is successfully measured depends on how crowded its immediate
> surroundings are, together with irreducible measurement noise. Predicting which sources will be
> missed — the completeness of the catalog, source by source — is a core, unsolved problem in dense-field
> photometry. This challenge asks you to predict it directly from the image.
> Overview
> Each example is a small single-channel image cutout of a dense star field. Near the centre of each
> cutout, a detection-and-measurement pipeline attempted to recover a faint point source whose brightness
> was controlled to sit near the field's detection threshold — a narrow completeness-test band, not a
> single exact value. Your task is a binary prediction: was that source recovered (label = 1)
> or missed (label = 0)?
> The outcome is driven by the local structure visible in the cutout — the density and proximity of
> neighbouring stars, the sky level, the blending of nearby light — plus factors the image cannot reveal
> (photon noise, the source's undisclosed brightness within the threshold band, and its unknown sub-pixel
> placement). As a result the target is only partly predictable from the image: strong models rank
> recoverable sources above missed ones well above chance, but a substantial irreducible ceiling remains.
> The cutouts come from several distinct fields. The test set is drawn from fields that do not
> appear in the training set (identified by the field column, provided for training examples only).
> A solution must therefore learn to read crowding in a way that transfers to unseen fields, whose
> stellar density and depth differ from anything seen in training — not memorise field-specific cues.
> The exact sub-pixel location of the tested source within each cutout is not disclosed and varies from
> example to example; the source itself is not present in the image (it was measured and removed). Only
> the surrounding field is shown.
> Dataset
> images/<id>.png — the field cutouts, 45×45 grayscale PNG, one per example (train and test).
> train.csv — columns id, field, label:
> id — integer example id; the cutout is images/<id>.png.
> field — integer field group this cutout belongs to (for building cross-field validation splits).
> label — 1 if the source was recovered, 0 if missed.
> test.csv — column id only. Predict a recovery score for each test id. Test cutouts belong to
> fields disjoint from every training field, and their field values are withheld.
> Column descriptions
> Task
> For every id in test.csv, output a real-valued recovery score (higher = more likely recovered).
> Scores are evaluated by ranking, so any monotonic scale is fine (a probability in [0, 1] is natural).
> This is a self-contained prediction task. Do not attempt to identify the origin of the images or
> retrieve any external catalog, label, or metadata; ids and field identifiers are opaque and carry no
> external meaning. Solutions must depend only on the pixel content of the provided cutouts and the
> training labels.
> Evaluation
> The score is the area under the ROC curve (ROC-AUC) of your recovery scores against the withheld
> true recovery labels, pooled over the test set:
> 0.5 = random ranking (uninformative).
> 1.0 = every recovered source ranked above every missed source.
> AUC is threshold-free and insensitive to the score's scale or calibration; only the induced ordering
> matters. The classes are approximately balanced.
> Submission format
> Write working/submission.csv with exactly two columns:
> id,score
> 0,0.83
> 1,0.12
> ...
> One row for every test id, each id exactly once (no missing ids, no extras, no duplicates).
> score is a finite real number.
> The grader rejects any submission that violates this contract (missing/extra/duplicate ids, null or
> non-finite scores, wrong columns).

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Constrained Endoscopic Mask Triage

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7873tndrtkssf7bjp151p2as8974mn
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, segmentation, medical, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.731

Full challenge description from page:

> Constrained Endoscopic Mask Triage
> Overview
> An automated segmentation service has produced a provisional polyp mask for each endoscopic frame. Eight nonoverlapping, local boundary replacements have already been proposed, but the quality-control system must commit exactly three. Some replacements move the contour toward the lesion boundary; others move an already plausible contour away from it. Select the globally best three-region commit and return the exact mask produced by those replacements.
> This is not unconstrained segmentation or interactive prompting. The prediction artifact is an executable, fixed-budget state transition. Every proposal is known before inference, no annotation is revealed after a choice, and the submitted mask must exactly witness execution of the submitted plan.
> The challenge is derived from externally released, real clinical endoscopy images and clinician-verified masks. Dataset identity, original identifiers, and reference-mask provenance are intentionally withheld. Cases are assigned opaque IDs, and related source families plus perceptual near-duplicate groups are kept entirely on one side of the train/test split.
> What Must Be Learned
> Each case contains eight 24 x 24 windows centered on visually ambiguous, low-gradient portions of the real lesion boundary. Within every window, the deployed and candidate patches are neighboring smooth contour hypotheses generated by small erosions, dilations, or translations. All eight proposals change pixels. Four improve local agreement with the hidden reference and four worsen it, with their positions and directions shuffled deterministically per case.
> Proposal size or foreground direction is therefore not a reliable answer. A solver must compare RGB boundary evidence with both contour hypotheses, infer each counterfactual effect, and allocate three commits jointly. Training exposes only the optimal three-region plan, not the repaired target mask, hidden reference mask, or per-region Dice gains.
> Files
> train.csv: 515 labeled quality-control cases.
> test.csv: 199 held-out cases without optimal plans.
> sample_submission.csv: one valid executable submission.
> images/: 714 RGB endoscopy frames referenced by the 515 training and 199 test rows, each 384 x 384 pixels.
> Both CSVs contain:
> id: opaque unique case identifier.
> image_path: relative path under images/.
> width, height: full image dimensions.
> defective_mask_rle: deployed full-frame mask.
> regions_json: JSON array of exactly eight candidate replacements.
> Each region object contains an opaque region_id, inclusive top-left coordinates x0, y0, exclusive bottom-right coordinates x1, y1, and a local candidate_rle. The eight rectangles are in-bounds and nonoverlapping. Training rows additionally contain review_plan, the optimal JSON list of exactly three distinct region IDs. No repaired or reference mask is public training supervision.
> Plan Execution
> Decode defective_mask_rle as the initial full-frame mask.
> Select exactly three distinct IDs from that row's regions_json.
> Decode each selected candidate_rle at shape (y1-y0, x1-x0).
> Replace the corresponding rectangle in the current full-frame mask.
> Encode the complete result as repaired_mask_rle.
> Replacement order is irrelevant because regions do not overlap. There are C(8,3) = 56 valid plans. The grader independently executes the plan and rejects a submitted mask that differs from that execution.
> RLE Convention
> Masks use one-indexed, column-major run-length encoding. Values alternate between start and length integers. Lengths must be positive; runs must be sorted, nonoverlapping, and within the applicable full-image or local-region bounds. An empty mask is an empty string.
> Evaluation
> For each case:
> D_initial is Dice between the deployed mask and hidden clinician mask.
> D_selected is Dice after executing the submitted three-region plan.
> D_best is the maximum Dice among all 56 valid plans.
> U = clip((D_selected - D_initial) / (D_best - D_initial), 0, 1).
> O = 1 when D_selected >= D_best - 1e-12, and 0 otherwise.
> The per-case score is:
> 0.85 * O + 0.15 * U
> The final score is the arithmetic mean across test cases. Higher is better, with range 0 to 1. Exact optimality receives most of the weight because the operational output is the committed three-action bundle; normalized utility supplies bounded partial credit for a near-optimal repair. Tied plans receive full optimality credit whenever their executed Dice reaches D_best within the stated tolerance.
> Only cases with D_best - D_initial > 0.0002 are published. This fixed preparation threshold removes zero-headroom and numerically unstable cases; it is not applied dynamically to submissions.
> Submission Format
> Submit exactly these columns in this order:
> id,review_plan,repaired_mask_rle
> case_...,"[""r_a"",""r_b"",""r_c""]",1 5 390 7
> Every test ID must appear exactly once. Duplicate or foreign IDs, extra columns, malformed JSON or RLE, unknown or repeated region IDs, plans other than length three, and masks that do not equal plan execution are rejected.
> Compute And Restrictions
> This is an A10G GPU challenge with a 90-minute runtime. Generally available pretrained visual encoders are allowed. Internet access, external datasets, private answers, source-identity recovery, manual test labeling, source-dataset reverse mapping, and test-specific lookup tables are prohibited. Solvers may use only released public files and generally available pretrained weights.
> Related Work
> Rasanjalee et al., "Understanding Annotation Error Propagation and Learning an Adaptive Policy for Expert Intervention in Barrett's Video Segmentation," arXiv:2602.21855, 2026, studies expert re-prompting and temporal propagation. This benchmark instead evaluates single-frame selection among fixed, executable contour transitions under an exact cardinality constraint.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Change Mosaic Ledger: Counterfactual Semantic Transition Recognition

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c4t6q1hqwtdbwxp42h790zn8drrq7
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.556

Full challenge description from page:

> Overview
> Satellite monitoring systems must distinguish meaningful physical transitions from illumination,
> seasonal colour, compression, sensor variation, and small registration differences. A bright pixel
> residual is not enough: the system must recognize what changed and determine the direction of that
> change in the displayed image pair.
> Every challenge case contains two 192 x 192 RGB mosaics named before and after. Each mosaic is a
> 2 x 2 grid of 96 x 96 tiles. Corresponding positions in the two mosaics form four independent paired
> observations. The decisive evidence may be a small building, a narrow road, a group of trees, or the
> absence of any semantic transition despite substantial appearance differences.
> The task is deliberately image-only. Auxiliary text, filenames, region descriptions, coordinates,
> construction keys, and hidden split metadata are not released. Every complete mosaic is newly
> assembled for this challenge and does not exist elsewhere as a participant-facing record.
> What Makes This Challenge Different
> The closest public task family is bitemporal remote-sensing change captioning, including
> MOSAIC-SEN2-CC, where a paired observation is used to generate a textual description and is evaluated
> with captioning metrics. Conventional semantic change detection instead predicts a binary or
> multiclass map from one aligned pair. This challenge changes the prediction unit, target,
> construction, and evaluation simultaneously:
> Four independent transitions per case: one 2 x 2 mosaic joins four unrelated paired decisions. Its
> eight underlying scene pairs never form one natural observation elsewhere.
> Counterfactual temporal direction: a verified event can be displayed forward or reversed after
> construction. The target is therefore both the semantic object and the displayed ADDED or
> REMOVED direction, not a recoverable historical label.
> Context-demixed evidence: each semantic crop is recomposed with unrelated same-partition carrier
> context before spatial and radiometric transformations. Systems must separate the local event from
> plausible surrounding content.
> Matched no-change controls: NO_CHANGE tiles receive the same acquisition-like nuisance and
> label-independent residual-energy distribution as real transitions, preventing a difference
> threshold from solving the task.
> Dependency-aware evaluation: exact and perceptual dependencies are grouped before train, public,
> or private assignment. Donors and carriers obey the same boundary, while class- and
> dependency-balanced probability skill prevents frequent classes or reused construction groups
> from controlling the leaderboard.
> The visual evidence begins with decoded and validated real bitemporal remote-sensing observations,
> not procedurally rendered shapes. Semantic events are admitted only after multiple agreeing
> creator-side records. The released mosaics, temporal directions, carrier contexts, no-change
> controls, and leaderboard units are all newly constructed for this challenge. The novelty lies in
> this combined counterfactual recognition protocol, not in ordinary image-pair classification alone.
> Task
> For every test case, predict the semantic transition at each of the four aligned tile positions:
> tile 0: top-left;
> tile 1: top-right;
> tile 2: bottom-left; and
> tile 3: bottom-right.
> For each tile, return seven non-negative class scores or probabilities. The grader normalizes each
> seven-value block independently. A submission therefore contains four probability distributions per
> test id and 28 prediction values in total.
> The labels are defined relative to the displayed before and after arrays. Displayed order may
> differ from construction-time chronology. Participants must infer the transition shown in the
> released images rather than recover hidden construction metadata.
> Transition Classes
> The seven classes, in the required probability-column order, are:
> BUILDING_ADDED: a building or house appears in the after tile.
> BUILDING_REMOVED: a building or house present in before is absent in after.
> ROAD_ADDED: a road, driveway, parking surface, path, or sidewalk appears in after.
> ROAD_REMOVED: transport-surface infrastructure present in before is absent in after.
> VEGETATION_ADDED: trees or other substantial vegetation appear in after.
> VEGETATION_REMOVED: trees or other substantial vegetation present in before are absent in
> after.
> NO_CHANGE: the two tiles represent the same semantic state, although acquisition-like colour,
> texture, blur, compression, and alignment differences may remain.
> The target is the semantic event, not the object occupying the largest area and not the largest raw
> pixel difference.
> Prediction Rules
> Predictions must follow these rules:
> Produce one row for every id in test.csv.
> Predict all four tile positions independently.
> Provide all seven class values for every tile.
> Use only finite, numeric, non-negative values.
> Ensure that each seven-value tile block has a strictly positive sum.
> Use the published column names exactly; names are lowercase after the tile_t_p_ prefix.
> Do not include any columns other than id and the 28 published prediction columns.
> The seven values do not need to sum to exactly 1.0 because the grader normalizes each tile block.
> Higher probability on the correct semantic transition produces a better score.
> What Makes the Task Difficult
> Every released tile is constructed from a semantic donor and unrelated same-partition carrier
> context. Regional crops are spatially transformed, blended, radiometrically adjusted, independently
> degraded, and re-encoded before four tiles are assembled into a mosaic. Genuine changes may be shown
> in forward or reversed temporal order; reversal also changes ADDED into REMOVED and
> vice versa. NO_CHANGE receives the same family of acquisition nuisance as the semantic classes.
> These operations are designed so that:
> each released mosaic is a unique derived composite;
> hidden construction annotations do not reveal the displayed transition direction;
> raw difference magnitude is not a reliable NO_CHANGE detector;
> class frequency and tile position provide no useful label prior; and
> repeated transformations of a rare dependency group cannot dominate the score.
> The useful signal is a learned paired visual representation. GPU training has a practical advantage
> for fine-tuning Siamese convolutional or transformer encoders and processing all tile pairs in
> batches. CPU execution remains allowed.
> Data Files
> The participant download contains:
> train.csv: 5,600 training ids, array indices, and four one-hot seven-class target blocks.
> test.csv: 1,400 test ids and array indices without labels.
> train_images.npz: compressed uint8 training mosaics, approximately 895 MiB.
> test_images.npz: compressed uint8 test mosaics, approximately 222 MiB.
> sample_submission.csv: a complete submission containing every test id and prediction column.
> metric_config.json: class order, tile order, prediction columns, metric name, and public metric
> constants.
> The complete participant-facing download occupies approximately 1.1 GiB. Preparation and modeling
> do not require network access.
> CSV Fields
> train.csv contains:
> id: opaque unique mosaic identifier.
> input_index: row index into both arrays in train_images.npz.
> tile_0_p_building_added through tile_0_p_no_change: one-hot target block for the top-left
> tile pair.
> tile_1_p_building_added through tile_1_p_no_change: one-hot target block for the top-right
> tile pair.
> tile_2_p_building_added through tile_2_p_no_change: one-hot target block for the bottom-left
> tile pair.
> tile_3_p_building_added through tile_3_p_no_change: one-hot target block for the bottom-right
> tile pair.
> Each training block contains one value equal to 1.0 at the correct class and six values equal to
> 0.0. The lowercase suffixes follow the class order listed in Transition Classes.
> test.csv contains:
> id: opaque unique mosaic identifier.
> input_index: globally unique image index. Test values run from 5,600 through 6,999; subtract
> 5,600 to obtain the row index in both arrays in test_images.npz.
> Ids and array indices carry no semantic, class, dependency, or visibility information. CSV row order
> should not be treated as a feature.
> Image Arrays
> train_images.npz contains:
> before: uint8 RGB array with shape [5600, 192, 192, 3].
> after: uint8 RGB array with shape [5600, 192, 192, 3].
> test_images.npz contains:
> before: uint8 RGB array with shape [1400, 192, 192, 3].
> after: uint8 RGB array with shape [1400, 192, 192, 3].
> Pixel values lie in [0, 255]. For train rows, input_index directly selects the matching entry in
> both training arrays. For test rows, use input_index - 5600 to select the matching entry in both
> test arrays. Split each mosaic at pixel 96 along both spatial axes:
> tile 0 uses rows 0:96 and columns 0:96;
> tile 1 uses rows 0:96 and columns 96:192;
> tile 2 uses rows 96:192 and columns 0:96; and
> tile 3 uses rows 96:192 and columns 96:192.
> The two arrays have identical row and tile order. Do not swap before and after, because temporal
> direction is part of six of the seven labels.
> Dataset Construction
> Candidate semantic regions pass a creator-side consistency audit before derivation. Only
> unambiguous events identifying one supported object family, one coarse spatial region, and one
> addition or removal direction are retained. Mixed-direction events, ambiguous regions, and weakly
> supported labels are excluded. Every retained semantic event requires multiple agreeing records with
> perfect label purity.
> All construction images are decoded and validated before use. Exact and perceptual fingerprints join
> duplicate dependencies before any challenge split is assigned. This grouping occurs before derived
> mosaics are sampled.
> For each derived tile, an audited semantic region is cropped with randomized scale and position,
> combined with unrelated carrier context from the same partition, transformed, and re-encoded.
> Semantic temporal order is randomized. NO_CHANGE is generated from one observed stable state rather
> than inferred from the absence of a description. Four independently sampled tile pairs are then
> placed into each 2 x 2 mosaic. Each mosaic uses four donors and four carriers from eight distinct
> underlying scene pairs.
> Exact transformation parameters, lineage mappings, hidden group weights, and visibility assignments
> remain creator-only.
> Evaluation
> The metric is class- and dependency-group-balanced probability skill. Let K = 7. For every
> evaluated tile prediction, let p be the normalized probability assigned to its correct class.
> For class k, the grader computes a hidden dependency-group-weighted mean correct-class
> probability:
> P_k = sum_i(w_i * p_i) / sum_i(w_i)
> where the sum includes evaluated tile predictions whose true class is k. The seven class means are
> then averaged:
> balanced_probability = (P_0 + P_1 + ... + P_6) / 7
> The final score is:
> score = clip((balanced_probability - 1/7) / (1 - 1/7), 0.001, 1.0)
> The score ranges from 0.001 to 1.0, and higher is better. A perfect submission receives 1.0. A
> uniform distribution receives the 0.001 score floor. Because every class receives equal metric
> weight, no fixed class-prior prediction can outperform the uniform reference.
> Dependency-group weights prevent repeated derived views of the same dependency from receiving more
> influence merely because they occur more often. The weights are used only by the hidden grader and
> are not participant-facing.
> Split and Leaderboard Design
> The independent split unit is a duplicate-aware dependency cluster. Every underlying pair, exact
> duplicate, perceptually detected dependency, donor use, carrier use, and derived mosaic remains
> entirely within train, public test, or private test. Assignment occurs before mosaic generation.
> The split contains:
> train: 5,600 mosaics using 3,584 dependency clusters;
> public leaderboard: 350 mosaics using 219 dependency clusters; and
> private leaderboard: 1,050 mosaics using 652 dependency clusters.
> The public leaderboard contains 25 percent of test mosaics and the private leaderboard contains 75
> percent. No underlying scene pair or dependency cluster crosses train/test or public/private
> visibility.
> Class balance is exact in every tile position. Each of the seven classes appears 800 times per tile
> position in train, 50 times per tile position in public test, and 150 times per tile position in
> private test. Across all four positions, this gives 3,200 training, 200 public, and 600 private tile
> instances per class.
> Road infrastructure is the smallest semantic object family. It still contains 368 independent train
> groups, 24 public groups, and 67 private groups. The hidden weighting scheme equalizes repeated donor
> dependencies within each class and visibility subset.
> Submission
> Submit one CSV row for every id in test.csv. The submission must contain exactly 29 columns: id
> followed by the 28 tile probability columns. Use this published order:
> id, tile_0_p_building_added,tile_0_p_building_removed,tile_0_p_road_added,tile_0_p_road_removed,tile_0_p_vegetation_added,tile_0_p_vegetation_removed,tile_0_p_no_change, tile_1_p_building_added,tile_1_p_building_removed,tile_1_p_road_added,tile_1_p_road_removed,tile_1_p_vegetation_added,tile_1_p_vegetation_removed,tile_1_p_no_change, tile_2_p_building_added,tile_2_p_building_removed,tile_2_p_road_added,tile_2_p_road_removed,tile_2_p_vegetation_added,tile_2_p_vegetation_removed,tile_2_p_no_change, tile_3_p_building_added,tile_3_p_building_removed,tile_3_p_road_added,tile_3_p_road_removed,tile_3_p_vegetation_added,tile_3_p_vegetation_removed,tile_3_p_no_change
> The line breaks above are for readability only. A CSV header occupies one physical line. A complete,
> directly usable example for all 1,400 test ids is provided in sample_submission.csv.
> The complete submission receives the 0.001 score floor if it contains:
> missing, extra, or duplicate columns;
> missing, extra, blank, or duplicate test ids;
> missing, non-numeric, non-finite, or negative prediction values; or
> a seven-class tile block whose values sum to zero.
> Submission row order does not matter because rows are matched by id. Probability-column order
> should follow the published sample, while exact column names and membership are mandatory.
> Expected Output
> A successful system should compare each aligned tile pair jointly, recognize the changed semantic
> object, determine the displayed temporal direction, distinguish true stability from acquisition
> nuisance, and return calibrated probabilities for all seven classes. It should apply the same visual
> reasoning across all four positions rather than learning four unrelated label priors.
> What Not to Use
> Do not use id, input_index, CSV row order, or file order as semantic features.
> Do not infer labels from tile position. Every class is exactly balanced at every position.
> Do not treat raw pixel-difference magnitude, colour shift, blur, or compression as a semantic
> label. These nuisance signals are deliberately shared across classes.
> Do not assume construction-time temporal direction is preserved. Released semantic pairs may be
> reversed.
> Do not treat the four tiles as one multi-label target. Each aligned position is an independent
> seven-class prediction.
> Do not infer targets from sample_submission.csv; its normalized predictions are uniform and it
> is provided only as a formatting example.
> Do not rely on a fixed rule-based mapping from residual statistics to labels. The semantic object
> and direction require learned visual evidence.
> Do not use reverse-image search, recover hidden construction annotations, or construct lookup
> tables for the test set.
> Do not manually label test mosaics or build test-id-specific rules.
> Do not use public/private leaderboard feedback to encode predictions for individual test ids.
> Recommended Modeling Direction
> A practical solution treats each 96 x 96 tile as a paired-image classification problem. A shared
> encoder can process before and after, followed by directional difference, absolute difference,
> feature fusion, and a seven-class head. The four positions can be reshaped into one larger tile batch
> for efficient training and inference.
> Pretrained convolutional networks or compact vision transformers are suitable starting points.
> Useful augmentations should preserve temporal semantics or update labels when order is swapped.
> Validation should avoid treating multiple transformed views of one dependency as independent
> evidence. Probability outputs preserve confidence information and support smooth ranking across
> solution quality.
> GPU acceleration is useful for paired representation learning, batched augmentation, and joint
> feature extraction. CPU-only methods are permitted but simple handcrafted residual statistics are
> not expected to capture the required semantic distinctions.

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## MazeEcho Hidden-Source Tomography

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cnwc3fbvz6rf44q8hqd9e0s8dvwrb
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, large-scale, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: —

Full challenge description from page:

> Overview
>
> An echo is evidence of a cause that is no longer visible. After a wave has crossed corridors,
>
> reflected from interfaces, and mixed through multiple paths, the remaining pressure field contains a
>
> distorted record of where the excitation began. MazeEcho asks models to reconstruct that hidden cause.
>
> Each example provides a partial view of a maze-like propagation medium, a sparse sensor mask, and
>
> twelve consecutive late-time pressure observations. The target is not the next frame and not a single
>
> source coordinate. It is a normalized 16 x 16 probability map describing the complete initial
>
> source-energy distribution.
>
> The challenge is a dense inverse problem with two simultaneous uncertainties: the model sees only a
>
> small fraction of the pressure grid, and parts of the propagation geometry are also withheld. Useful
>
> solutions must reason across space, time, visibility masks, and previously unseen maze topologies.
>
> What Makes This Challenge Different
>
> MazeEcho treats the observation process itself as a changing part of the problem. A useful abstract
>
> view of one example is:
>
>
> late_observation[t] = sensor_mask * calibrate(propagate(source, geometry, t)) + noise
>
> given:   partial_geometry, sensor_mask, late_observation[60:72]
>
> recover: normalized_distributed_source
>
>
> The sensor mask, visible geometry, calibration, polarity, orientation, and noise realization vary
>
> between panels. Consequently, a model cannot learn one fixed inverse filter or interpret unobserved
>
> zeros as physical measurements.
>
> The task combines properties that are normally evaluated separately:
>
> Backward causal recovery: infer an earlier hidden field from late scattered evidence rather
>
> than extrapolating an observed state forward.
>
> A variable observation operator: only 512 of 4,096 pressure locations are retained, and the
>
> retained positions change between panels.
>
> Incomplete propagation context: rectangular geometry regions are hidden, so the model must
>
> recover a cause without a complete path map.
>
> Distributed and possibly multimodal answers: 256 output values describe probability mass over
>
> the full target grid; reducing the output to one coordinate loses valid source structure.
>
> Nuisance-resistant inference: independent gain, frame calibration, polarity, measurement noise,
>
> rotation, and reflection prevent raw amplitude or absolute orientation from becoming shortcuts.
>
> Topology transfer: evaluation groups are entire maze topologies, not randomly mixed panels.
>
> Coarse-to-fine skill measurement: three sum-pooled resolutions distinguish regional recovery
>
> from precise localization without turning the task into brittle exact-pixel matching.
>
> This contract is different from common neighboring task types:
>
> | Task type | Typical mapping | MazeEcho mapping |
>
> | --- | --- | --- |
>
> | Forward field forecasting | observed early field to later field | late partial fields to unobserved initial cause |
>
> | Point-source localization | measurements to one coordinate | measurements to a distributed probability field |
>
> | Image inpainting | masked target-like image to completed image | indirect wave evidence to a different latent field |
>
> | Fixed-array inversion | one known sensing operator | a panel-specific sensing and calibration operator |
>
> The central research question is whether a learned model can recover a distributed cause when both
>
> the propagation evidence and the observation operator are incomplete. Solving forward rollout,
>
> single-point localization, or ordinary image completion does not solve this combined objective.
>
> Construction Boundary
>
> The physical starting material consists of 400 simulated maze-acoustics trajectories selected from
>
> Polymathic AI's Acoustic Scattering Maze release in The Well. MazeEcho reuses the simulated maze
>
> material fields, initial pressure fields, twelve pressure states at indices 60 through 71, and the
>
> fact that some trajectories share a topology. It does not claim that these underlying wave
>
> trajectories were newly simulated. License, revision, file-level hashes, and full source attribution
>
> are recorded in the accompanying dataset card and platform Source field.
>
> Everything that defines the participant task is constructed after that selection:
>
> | Benchmark stage | Reused physical information | Newly designed for MazeEcho |
>
> | --- | --- | --- |
>
> | Spatial representation | Maze material and pressure values | Validated 64 x 64 compact representation with hidden creator metadata |
>
> | Observation generation | Twelve late pressure states | Four independent panels per trajectory, each with 512 sensors, geometry occlusions, gain, frame calibration, polarity, noise, rotation, and reflection |
>
> | Prediction target | Initial pressure as organizer-only physical evidence | Background-suppressed, locally smoothed, unit-mass 16 x 16 distributed source map |
>
> | Generalization protocol | Shared-topology relationships | Opaque ids and topology-grouped train, public, and private partitions assigned before panel expansion |
>
> | Evaluation contract | No pre-existing task labels or score | Three-resolution sum-pooled error normalized by the scored subset's constant-mean baseline |
>
> The separation is reproducible rather than conceptual only: source checks, group assignment, panel
>
> generation, target construction, public/private separation, and output serialization are deterministic
>
> steps in the preparation pipeline. Thus the benchmark contribution is the inverse reconstruction
>
> problem and its controlled evaluation protocol, while the inherited trajectories remain attributed
>
> simulation evidence.
>
> Task
>
> For every id in test.csv, predict 256 finite, nonnegative values. Column
>
> source_rRR_cCC represents target-grid row RR and column CC, with both indices running from 00
>
> through 15.
>
> The grader converts every valid prediction row to unit mass. For numerical stability, it first divides
>
> the row by its largest entry and then divides by the resulting row sum. This procedure prevents
>
> overflow and makes the score invariant to finite positive rescaling. Larger normalized values place
>
> more predicted source mass in the corresponding cells.
>
> Prediction Rules
>
> Submit exactly one row for every test id.
>
> Include id followed by all 256 target columns in published row-major order.
>
> Every target value must be finite and nonnegative.
>
> Every prediction row must contain strictly positive total mass.
>
> Do not add, remove, rename, or reorder columns.
>
> Predictions do not need to arrive normalized because normalization is part of grading.
>
> Why the Task Is Difficult
>
> The first released observation occurs sixty simulation steps after the hidden source. By then,
>
> direct evidence has mixed with reflections from material boundaries and with signals travelling along
>
> multiple corridors. Only one eighth of the spatial pressure grid is measured in each panel.
>
> The missing-data pattern is not constant. Four observation panels are created for each trajectory,
>
> each with its own sensor placement, geometry occlusion, calibration, polarity, noise, and spatial
>
> orientation. Opaque identifiers and array indices carry no source, topology, or visibility signal.
>
> A strong model must combine local pressure evolution with long-range maze-conditioned interactions.
>
> Masked spatiotemporal convolutions, U-Nets, neural operators, and vision transformers are natural
>
> model families. A pooled linear model cannot represent the same geometry-dependent propagation.
>
> Data Files
>
> The participant release contains:
>
> train.csv: 1,292 labeled rows;
>
> test.csv: 308 held-out rows;
>
> train_inputs.npy: float16 tensor with shape [1292, 15, 64, 64];
>
> test_inputs.npy: float16 tensor with shape [308, 15, 64, 64];
>
> grid_axis.npy: float32 coordinate axis for the 64 x 64 input grid;
>
> target_grid_axis.npy: float32 coordinate axis for the 16 x 16 output grid;
>
> observation_time_indices.npy: twelve retained indices, 60 through 71; and
>
> sample_submission.csv: a complete structurally valid submission template.
>
> Preparation and modeling require no network access.
>
> CSV Schema
> train.csv
>
> id: unique opaque panel identifier.
>
> array_index: zero-based row index in train_inputs.npy.
>
> source_rRR_cCC: 256 normalized target values flattened in row-major order.
>
> test.csv
>
> id: unique opaque panel identifier.
>
> array_index: global row reference from 1,292 through 1,599.
>
> For a test row, subtract 1,292 from array_index to address the first axis of test_inputs.npy.
>
> sample_submission.csv
>
> The submission template contains exactly 257 columns: id followed by the same 256
>
> source_rRR_cCC columns used by the training targets. answers.csv uses exactly this schema and
>
> column order.
>
> Input Channels
>
> One input row has shape [15, 64, 64]:
>
> channel 0: signed geometry evidence; known path approaches -1, known wall approaches +1, and
>
> unavailable geometry is 0;
>
> channel 1: geometry-known mask, where 1 marks available geometry;
>
> channel 2: pressure-sensor mask, where 1 marks a measured location; and
>
> channels 3 through 14: twelve consecutive normalized late-time pressure observations.
>
> Unmeasured pressure cells are stored as zero. Channel 2 must therefore be used to distinguish a
>
> missing measurement from a measured value near zero. Convert float16 tensors to float32 before model
>
> computation.
>
> Targets flatten a 16 x 16 map in row-major order. After source_r00_c15, the next target column is
>
> source_r01_c00.
>
> Evaluation
>
> The grader validates the complete submission contract before scoring. It then normalizes every
>
> prediction and truth row and applies non-overlapping sum pooling at three resolutions:
>
> factor 1 produces a 16 x 16 map;
>
> factor 2 produces an 8 x 8 map by summing each 2 x 2 block; and
>
> factor 4 produces a 4 x 4 map by summing each 4 x 4 block.
>
> Sum pooling preserves total probability mass. At each resolution R, the error is normalized by the
>
> constant-mean baseline calculated from the exact answer subset being scored:
>
>
> SSE_R = sum_i sum_u (P_R[i,u] - T_R[i,u])^2
>
> Mean_R[u] = mean_i T_R[i,u]
>
> BaselineSSE_R = sum_i sum_u (Mean_R[u] - T_R[i,u])^2
>
> NormalizedError_R = SSE_R / BaselineSSE_R
>
>
> Here i indexes scored examples and u indexes cells at resolution R. Mean_R is recomputed from
>
> the scored answer subset; it is not a training-set prior.
>
> The exact combined error and score are:
>
>
> Error = 0.50 * NormalizedError_16x16
>
>       + 0.30 * NormalizedError_8x8
>
>       + 0.20 * NormalizedError_4x4
>
> Score = clip(1 - Error^1.2, 0.001, 1.0)
>
>
> Higher is better. A perfect prediction scores 1.0. The scored subset's constant-mean map has error
>
> 1.0 at every resolution and therefore receives 0.001. Missing or duplicate ids, schema changes,
>
> negative values, NaN, infinity, or zero-mass rows also receive 0.001.
>
> Split and Leaderboard Design
>
> The independent unit is a complete maze-topology group. Every trajectory sharing that topology and
>
> all four panels derived from each trajectory remain together.
>
> The release contains 355 independent topology groups:
>
> training: 284 groups, 323 trajectories, and 1,292 rows;
>
> public test: 18 groups, 19 trajectories, and 76 rows; and
>
> private test: 53 groups, 58 trajectories, and 232 rows.
>
> Public evaluation contains 25.35% of held-out independent groups and 24.68% of held-out rows.
>
> Source-centroid quadrant and maze-density strata are balanced at group level. No topology,
>
> trajectory, opaque id, or exact feature tensor crosses a boundary.
>
> Computational Expectations
>
> GPU training has a material advantage. Every example contains fifteen 64 x 64 spatial channels,
>
> and suitable models repeatedly apply spatial convolutions or attention across twelve time steps.
>
> CPU preprocessing and classical baselines are permitted, but the intended high-capacity
>
> spatiotemporal models are substantially faster to train on an accelerator.
>
> Submission
>
> Use sample_submission.csv as the template. Submit one CSV row per test id with exactly 257
>
> columns: id followed by all 256 source-map columns in the published order.
>
> Row order may change because the grader joins by id. Column order may not change.
>
> What Not To Use
>
> Do not use hidden answers, visibility assignments, creator dependency maps, or unreleased metadata.
>
> Do not infer targets from id text, row order, or array_index; these fields are opaque and audited.
>
> Do not manually coordinate labels for held-out examples or access evaluator-only files.
>
> Classical acoustic inversion and CPU models remain valid approaches. These rules prohibit unreleased
>
> information, not legitimate physics-based modeling.
>
> Expected Output
>
> The expected artifact is one valid submission.csv containing a normalized source-field prediction
>
> for every test example. The leaderboard maximizes the multiscale skill score defined above.
>
>  
>
> Submissions
> 0
> Top Score
> —
> Created
> Sep 6, 2026
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

## Counterfactual Table Topology Blueprint Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx737h370zrapg69fjkd67pnz18dsyj9
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; challenge detail page timed out
- Difficulty: Medium
- Compute: Not displayed; challenge detail page timed out
- GPU: Not displayed; challenge detail page timed out
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage card score context: Beat alba's score of 63.320!

Full challenge description from page:

> Overview Counterfactual Table Topology Blueprint Reconstruction is a high-difficulty computer-vision challenge centered on the recovery of concealed table structure. Each sample contains a scientific table image in which one structurally meaningful rectangular chamber has been hidden. Four candidate blueprints propose different logical reconstructions of the missing region. Exactly one blueprint restores the original table topology. The other three blueprints are valid counterfactual structures. They occupy the same chamber, use the same number of atomic rows and columns, and remain compatible with the chamber’s outer dimensions. Their differences are concentrated inside the concealed region through plausible changes involving cell division, cell merging, spanning behavior, header organization, and functional roles. For every sample, predict: Which blueprint reconstructs the hidden chamber. The topology family represented by the original chamber. The functional-role composition of the original chamber. The chamber’s exact merge mass. The prediction is a compact structural record rather than a generated table. A submission contains: sample_id blueprint_id topology_code role_code merge_mass A conceptual prediction is: CTBR_7A91F4,B03,T06,R04,5 This means: B03 is the selected reconstruction blueprint. T06 is the predicted topology family. R04 is the predicted functional-role regime. The hidden chamber has merge mass 5. Participants do not submit: Bounding-box arrays. Cell polygons. HTML. XML. Graph serializations. OCR text. Variable-length detection records. Natural-language explanations. The compact output format keeps submission generation reliable while the underlying visual inference remains strongly structured. The decisive portion of the table is not directly visible. A model must infer it from boundary continuation, repeated geometry, header hierarchy, neighboring cell organization, global alignment, and the differences among several legal counterfactual blueprints. The challenge therefore transforms table understanding into visual hidden-subgraph reconstruction. Challenge Domain Primary domain: Computer Vision Secondary domains: Object Detection Visual Document Understanding Structured Prediction Graph Reconstruction The execution environment provides one NVIDIA A10G GPU. Pretrained visual and multimodal models are allowed. The task itself is evaluated as a computer-vision reconstruction problem rather than as a model-training regime. Reconstruction Objective A table can be represented at several interconnected levels. At the visual level, it contains: Text regions. Ruling lines. Whitespace. Alignment patterns. Typographic distinctions. Repeated horizontal and vertical structure. At the geometric level, it contains: Row bands. Column bands. Boundary intersections. Cell extents. Spanning regions. Header boundaries. At the logical level, it contains: Atomic grid positions. Logical cells. Row and column spans. Horizontal and vertical adjacency. Header-to-body organization. Functional cell roles. The challenge removes a localized logical region from the visual table while preserving its surrounding evidence. A successful model must reconstruct the missing relationship between these levels. The selected blueprint must agree with: The visible row system. The visible column system. Boundary terminations near the chamber. Repeated dimensions elsewhere in the table. The apparent header depth. The location of the body region. Spans entering or approaching the chamber. The table’s broader structural rhythm. Locally plausible line placement is insufficient when it creates a globally inconsistent table. Public Prediction Object Each test sample contains: One sample_id. One partition_key. One reconstruction-board image. One masked table. One highlighted hidden chamber. Four rendered blueprint candidates. Four local blueprint identifiers. The hidden target contains: One correct blueprint_id. One topology_code. One role_code. One integer merge_mass. Four private candidate-affinity values used for graded evaluation. Blueprint identifiers are: B01 B02 B03 B04 Topology codes are: T01 T02 T03 T04 T05 T06 T07 T08 Role codes are: R01 R02 R03 R04 R05 R06 R07 R08 Blueprint identifiers are local to each sample. B03 in one sample has no connection to B03 in another sample. Candidate order is independently permuted, and no blueprint position is associated with a particular structural edit or target class. Topology and role codes remain stable throughout the complete dataset. Their behavior can be learned from the released training examples. Reconstruction Board Every sample is presented as one visual reconstruction board. The board contains two principal regions. Masked Table Panel The upper panel contains: The complete processed table image. One concealed rectangular chamber. A clearly visible chamber boundary. Registration marks aligned with the hidden grid region. The original visual evidence surrounding the chamber. The source table preserves its aspect ratio. Tables are padded when necessary rather than stretched into distorted proportions. Row height, column width, text scale, and alignment therefore retain their original visual relationships. The chamber is covered using a standardized neutral mask. The mask does not contain the source pixels, blurred remnants, transparency artifacts, or compressed traces of the hidden content. Its appearance is independent of the chamber’s target class. Blueprint Candidate Panel The lower panel contains four candidate blueprints. Each candidate: Uses the Counterfactual Table Topology Blueprint Reconstruction Overview Counterfactual Table Topology Blueprint Reconstruction is a high-difficulty computer-vision and structured-prediction challenge over partially concealed scientific tables. Each sample contains a table image in which one structurally meaningful rectangular chamber has been hidden. Four candidate blueprints propose alternative reconstructions of the missing table region. Exactly one candidate preserves the original logical structure. The other three candidates are legal counterfactual table structures. They occupy the same chamber dimensions and remain compatible with the chamber’s coarse exterior interface, but alter internal relationships involving: Row separation. Column separation. Horizontal spanning. Vertical spanning. Hierarchical headers. Projected row headers. Header-to-body transitions. Logical cell grouping. Functional cell roles. The model must recover four targets: The correct topology blueprint. The chamber’s latent topology family. The chamber’s latent functional-role composition. The chamber’s merge mass. A submission contains only: sample_id blueprint_id topology_code role_code merge_mass Participants do not submit bounding boxes, segmentation masks, polygons, table markup, adjacency matrices, or variable-length graph programs. The compact output format keeps submission generation reliable while leaving the underlying visual task substantially more demanding than ordinary image classification. A successful model must inspect the visible table, infer its row and column rhythm, understand header organization, trace boundaries approaching the mask, reason about spanning cells, compare four plausible hidden subgraphs, and choose the reconstruction that restores the most coherent complete table. The central prediction objective is: Recover a concealed rectilinear table subgraph by selecting its correct structural blueprint and reconstructing its topology, functional regime, and logical merge complexity. Prediction Object Every sample contains: One reconstruction-board image. One masked table chamber. Four candidate blueprints. One hidden correct blueprint. One hidden topology code. One hidden role-composition code. One hidden merge-mass value. Candidate blueprint identifiers are: B01 B02 B03 B04 Topology codes are: T01 T02 T03 T04 T05 T06 T07 T08 Role-composition codes are: R01 R02 R03 R04 R05 R06 R07 R08 merge_mass is a non-negative integer. The categorical code inventories remain stable throughout the challenge. Their behavior is learnable from the released training examples. The evaluation data introduces no unseen code. Reconstruction Board Every public board image contains two visually separated regions. The upper region displays: The scientific table crop. The concealed structural chamber. The visible table content surrounding that chamber. A clearly marked chamber boundary. Registration marks identifying the chamber extent. The lower region displays four structural blueprints labeled: B01 B02 B03 B04 The entire board uses a fixed outer canvas layout. Candidate placement, padding, label position, and panel size remain consistent across all samples. The table preserves its aspect ratio. It is padded to fit the board rather than stretched into a different geometry. The chamber mask uses a neutral visual treatment that does not reveal: Original ruling lines. Original text. Original shading. Hidden cell boundaries. Hidden cell roles. Which candidate is correct. The four blueprint panels use a standardized symbolic rendering system. They depict topology, not restored source pixels. Candidate Blueprint Rendering Each candidate blueprint represents the hidden chamber as a normalized structural schematic. Blueprints display: The chamber’s outer rectangle. Atomic row and column tracks. Logical cell boundaries. Merged-cell regions. Header-role shading. Projected-row-header markings. Spanning-header markings. General spanning-cell markings. Boundary attachment points. Blueprints do not reproduce: Original words. Original typography. Source-image noise. Compression artifacts. Cell contents. Original pixel fragments. The correct option cannot be selected through direct patch matching because the original concealed pixels are never supplied as a candidate. All candidates are rendered using the same: Canvas dimensions. Stroke widths. Font. Label placement. Color palette. Role legend. Padding. Rasterization method. The rendering process prevents stylistic differences from revealing correctness. Hidden Chamber The hidden chamber is aligned with the table’s logical geometry. It covers: At least two logical rows. At least two logical columns. No more than six logical rows. No more than six logical columns. Its boundaries follow existing normalized row and column extents. The chamber does not arbitrarily cut through the image without regard to table structure. It represents a coherent rectilinear subregion of the logical grid. A chamber may contain: Ordinary body cells. Column-header cells. Projected row headers. Spanning headers. General spanning cells. Empty structural cells. Several functional roles at once. Cells extending beyond the chamber are clipped to the chamber-local grid for local topology calculations. Their visible continuation outside the mask remains available as evidence. Structural Evidence The chamber removes the decisive local pixels, but the surrounding image preserves a broad field of structural evidence. A model can reason from: Row boundaries approaching the chamber. Column boundaries approaching the chamber. Boundary lines terminating before the mask. Repeated column widths elsewhere in the table. Repeated row heights. Whitespace alignment. Typography changes between header and body regions. Bold or centered header text. Repeated numerical alignment. Visible spans neighboring the chamber. Symmetry across adjacent column groups. Header depth outside the chamber. Projected row-header patterns. Border continuity. Cell padding and text alignment. Long-range grid regularity. Some samples can be solved from strong local evidence. Others require reasoning across most of the visible table. A candidate may agree perfectly with the chamber’s left and right edges while contradicting the header hierarchy visible several rows above or below. The task therefore rewards both local boundary detection and global layout interpretation. Chamber Selection The dataset emphasizes structurally informative chambers. Selected chambers contain sufficient visual context and satisfy the published grid-size limits. Structurally richer regions receive priority. Common chamber characteristics include: At least one spanning cell. A transition between header and body. A projected row header. A hierarchical column header. Unequal row heights. Unequal column widths. Multiple internal junction types. A span terminating within the chamber. A span continuing across a chamber boundary. Mixed functional roles. A combination of ordinary and merged cells. Regular body-grid chambers remain present as essential negative and calibration examples, but they do not dominate the challenge. The evaluation set contains a deliberately broad range of: Chamber sizes. Table aspect ratios. Grid densities. Header depths. Span directions. Merge masses. Role compositions. Visual ruling styles. Legal Counterfactuals Every incorrect blueprint is a structurally legal table partition. A counterfactual satisfies all of the following: Every atomic grid position belongs to exactly one logical cell. Every logical cell occupies a contiguous rectangular region. No two logical cells overlap. No grid position is left uncovered. Every row span remains within the chamber. Every column span remains within the chamber. Every role belongs to the supported role inventory. The chamber dimensions match the gold chamber. The resulting topology differs from gold. The resulting topology differs from the other candidates. Candidates are rejected if they create: Nonrectangular cells. Disconnected cells. Overlapping spans. Missing grid positions. Out-of-range coordinates. Duplicate structures. A topology identical to gold. Changes outside the concealed chamber. Rendering-only differences without structural change. The model therefore chooses among four genuine structural hypotheses rather than distinguishing one valid diagram from three malformed distractions. Counterfactual Operations Incorrect blueprints are derived through controlled transformations of the hidden logical structure. Possible transformations include: Splitting a horizontal spanning cell. Splitting a vertical spanning cell. Splitting a bidirectional spanning cell. Merging horizontally adjacent cells. Merging vertically adjacent cells. Extending a span by one row. Extending a span by one column. Shortening a span. Moving a header termination. Converting a spanning header into separate header cells. Converting separate header cells into a spanning header. Replacing a projected row header with body cells. Introducing a projected row header at a plausible row. Changing the role of a geometrically valid cell. Moving an internal junction. Redistributing the same merge mass across different cells. Exchanging a header merge for a body merge. Preserving cell count while changing adjacency. A candidate can contain more than one operation when a single edit would be too obvious or when several edits are required to maintain a legal rectangular partition. Counterfactuals remain close enough to gold to create meaningful competition. They are not required to have identical topology statistics. However, candidate sets preferentially include alternatives sharing coarse properties such as: Similar logical cell count. Similar merge mass. Similar header occupancy. The same number of atomic rows. The same number of atomic columns. Similar exterior attachment patterns. This prevents basic candidate counting from solving most samples. Interface Compatibility All four candidates share the same outer chamber. They preserve: Chamber width. Chamber height. Atomic row count. Atomic column count. Outer boundary. Registration points. Blueprint scale. Counterfactual candidates also preserve the chamber’s major exterior attachments whenever a legal alternative permits it. This means that multiple candidates can agree on: Where visible row boundaries meet the chamber. Where visible column boundaries meet the chamber. Which exterior tracks continue into the hidden region. The chamber’s coarse header and body division. They differ mainly in how those exterior constraints are resolved internally. For example, two candidates may show the same three column tracks entering a concealed header region. One may continue all three divisions, another may merge the first two columns beneath a spanning header, and a third may merge all three columns. All remain compatible with the exterior rectangle. Only one agrees with the complete surrounding table. Atomic Grid Representation Every hidden chamber is represented internally as an atomic grid. An atomic position is identified by: Local row index. Local column index. A chamber containing three rows and four columns has twelve atomic positions. Logical cells partition these positions into rectangular groups. An ordinary cell occupies one atomic position. A horizontally spanning cell occupies several adjacent column positions in the same row range. A vertically spanning cell occupies several adjacent row positions in the same column range. A bidirectional spanning cell occupies a rectangle covering multiple rows and columns. This representation provides a common comparison space for blueprints with different logical-cell counts. Blueprint Topology Graph Every blueprint induces a chamber-local topology graph. Graph nodes represent logical cells. Each node contains: Local row start. Local row end. Local column start. Local column end. Row span. Column span. Functional role. Graph relationships represent: Horizontal adjacency. Vertical adjacency. Shared atomic ownership. Row-boundary continuation. Column-boundary continuation. Header grouping. Span containment over atomic positions. The correct blueprint graph is reconstructed directly from the hidden logical cells. Counterfactual graphs are generated through legal topology transformations. Participants are not required to submit a graph. They select one of four visibly rendered graph candidates. Topology Codes topology_code summarizes the structural regime of the hidden chamber. The eight supported codes are: T01 T02 T03 T04 T05 T06 T07 T08 Each chamber receives exactly one code. The underlying structural regimes distinguish: Regular unmerged grid structure. Horizontal-span-dominant structure. Vertical-span-dominant structure. Bidirectional spanning. Hierarchical header topology. Projected-row-header topology. Mixed header-and-body topology. Compound topology containing several interacting structures. A deterministic precedence policy resolves chambers satisfying more than one description. Compound and specialized structural patterns take precedence over simpler patterns. A chamber with hierarchical headers and bidirectional spanning does not collapse into the ordinary horizontal-span category. Topology codes remain stable between training and test data. The model predicts the code separately from the candidate identifier. This auxiliary target encourages the visual representation to capture the type of structure being reconstructed rather than only its position among four options. Role-Composition Codes role_code summarizes the functional composition of cells inside the hidden chamber. Supported values are: R01 R02 R03 R04 R05 R06 R07 R08 The underlying compositions distinguish chambers dominated by or combining: Body cells. Column-header cells. Projected row headers. Spanning headers. General spanning cells. Header-to-body transitions. Multiple header types. Mixed functional structure. Every chamber receives exactly one role code through a deterministic precedence policy. The role code is based on logical cell roles rather than text meaning inferred by a language model. Visual evidence for role composition can include: Position near the top of the table. Bold typography. Centered labels. Repeated subcolumns. Section-divider formatting. Indented first-column text. Spanning labels. Changes in numerical density. Strong boundary transitions. Whitespace surrounding projected headers. The concealed chamber removes the target cells themselves, so role prediction may require extrapolating patterns from neighboring rows and columns. Merge Mass merge_mass is a chamber-local measure of logical merging. For every unique logical cell intersecting the chamber: cell merge mass = local row span × local column span − 1 The chamber merge mass is: merge_mass = sum of cell merge masses An ordinary 1 × 1 cell contributes: 0 A 1 × 2 cell contributes: 1 A 1 × 4 cell contributes: 3 A 2 × 2 cell contributes: 3 A 3 × 2 cell contributes: 5 Only the portion of a cell inside the chamber is used. A cell spanning two rows globally but intersecting only one selected chamber row has a chamber-local row span of one. This keeps merge mass aligned with the exact structure displayed in the candidate blueprints. A regular chamber has: merge_mass = 0 Two candidates may have identical merge mass but distribute their merges differently. Merge mass therefore provides a useful structural quantity without replacing blueprint selection. Worked Reconstruction Example Consider a hidden chamber covering: Two atomic rows. Three atomic columns. Six atomic positions. The atomic positions are: Top row: (0,0), (0,1), (0,2) Bottom row: (1,0), (1,1), (1,2) The visible table shows: Three column tracks continuing below the chamber. A header band continuing from the left. A body row continuing on both sides. No vertical span crossing the chamber boundary. A missing divider between the first two top-row positions. The four blueprints propose different internal partitions. Blueprint B01 B01 contains: One header cell spanning (0,0) and (0,1). One ordinary header cell at (0,2). Three separate body cells in the bottom row. This is the correct hidden topology. Blueprint B02 B02 contains: Three separate header cells in the top row. Three separate body cells in the bottom row. This candidate incorrectly introduces a boundary between (0,0) and (0,1). Blueprint B03 B03 contains: One header cell spanning all three top-row positions. Three separate body cells in the bottom row. This candidate preserves the merge between (0,0) and (0,1) but incorrectly removes the boundary between (0,1) and (0,2). Blueprint B04 B04 contains: Three separate header cells in the top row. One body cell spanning (1,0) and (1,1). One ordinary body cell at (1,2). B04 has the same total merge mass as B01, but the merge occurs in the wrong row and carries the wrong functional role. The gold targets are: blueprint_id = B01 topology_code = T05 role_code = R06 merge_mass = 1 T05 identifies the applicable header-oriented horizontal-span regime. R06 identifies a chamber containing both header and body structure. Merge mass is calculated as follows: The 1 × 2 header cell contributes 1. The remaining four 1 × 1 cells contribute 0. Total merge mass is 1. This example illustrates why each target captures different information. B01 and B04 share the same merge mass. B01 and B03 share part of the correct header merge. B01 and B02 share the same number of atomic rows and columns. Only B01 recovers the complete hidden structure. Boundary Agreement Blueprint affinity uses the atomic grid. For every horizontally or vertically adjacent pair of atomic positions, the topology records whether those positions: Belong to the same logical cell. Are separated by a logical-cell boundary. Boundary agreement is the fraction of adjacent atomic pairs for which the candidate and gold structures make the same decision. Let this value be: Boundary A perfect blueprint has: Boundary = 1 A candidate differing by one internal split can retain high boundary agreement. Same-Cell Relation F1 For every unordered pair of atomic positions, a same-cell relation is created when both positions belong to the same logical cell. Let: P be the candidate same-cell relation set. G be the gold same-cell relation set. Then: SameCellF1 = 2 × |P intersection G| / (|P| + |G|) If both sets are empty: SameCellF1 = 1 If only one set is empty: SameCellF1 = 0 This comparison measures logical grouping directly. A candidate that places the correct number of boundaries in the wrong locations can have reasonable boundary agreement while receiving poor same-cell relation F1. Role Occupancy Agreement Every atomic position inherits the functional role of its logical cell. Role occupancy agreement is the fraction of atomic positions whose candidate role matches the gold role. Let this value be: RoleOccupancy A candidate can reproduce the correct geometry while assigning an incorrect header or body role. Such a candidate receives structural credit but loses functional credit. Blueprint Structural Affinity Every candidate has a deterministic affinity with the gold blueprint. Affinity is: Affinity = 0.50 × Boundary + 0.30 × SameCellF1 + 0.20 × RoleOccupancy Affinity lies in: [0,1] The gold blueprint always receives exactly: 1 No visual embeddings, learned models, OCR outputs, or semantic judges participate in affinity calculation. Worked Affinity Calculation The worked two-row, three-column chamber contains seven internal adjacency decisions: Four horizontal adjacencies. Three vertical adjacencies. For B01: Boundary agreement: 7/7 Same-cell F1: 1 Role occupancy: 1 Affinity: 1 For B02: Boundary agreement: 6/7 Same-cell F1: 0 Role occupancy: 1 Therefore: B02 affinity = 0.50 × 6/7 + 0.30 × 0 + 0.20 × 1 B02 affinity ≈ 0.6286 For B03: Boundary agreement: 6/7 Same-cell F1: 0.5 Role occupancy: 1 Therefore: B03 affinity = 0.50 × 6/7 + 0.30 × 0.5 + 0.20 × 1 B03 affinity ≈ 0.7786 For B04: Boundary agreement: 5/7 Same-cell F1: 0 Role occupancy: 1 Therefore: B04 affinity = 0.50 × 5/7 + 0.30 × 0 + 0.20 × 1 B04 affinity ≈ 0.5571 B03 receives more partial credit than B02 or B04 because it preserves the original first merge and introduces only one additional merge. The affinity score recognizes this structural proximity even though B03 fails exact blueprint recovery. Dataset Structure The public package contains: train.csv test.csv sample_submission.csv boards/ There is no public answer file. There is no public logical-cell annotation file. There is no public source-object annotation file. There is no public counterfactual edit log. There is no official validation file. Board Images Board images are stored under: boards/ Each file contains: One masked table panel. One chamber boundary. Four candidate blueprint panels. Candidate identifiers. A consistent visual legend. Board images use compact encoding while preserving sharp structural edges. Lossless encoding is used where role shading, fine grid boundaries, or small blueprint details would be damaged by lossy compression. Every board_file value resolves to exactly one released image. Training File Each row of train.csv contains: sample_id partition_key board_file blueprint_id topology_code role_code merge_mass B01_affinity B02_affinity B03_affinity B04_affinity sample_id Type: String. Purpose: Submission alignment only. The identifier has no semantic meaning and must not be used as a predictive feature. partition_key Type: String. An opaque grouping identifier for related source material. All boards derived from the same document family share a partition relationship. Participants should use this field for grouped local validation. The identifier value itself has no semantic meaning. board_file Type: String. A relative path to the corresponding reconstruction board image. blueprint_id Training only. Type: String. One of: B01 B02 B03 B04 topology_code Training only. Type: String. One of: T01 T02 T03 T04 T05 T06 T07 T08 role_code Training only. Type: String. One of: R01 R02 R03 R04 R05 R06 R07 R08 merge_mass Training only. Type: Non-negative integer. Candidate Affinities Training rows contain: B01_affinity B02_affinity B03_affinity B04_affinity Each value lies in: [0,1] The correct candidate receives exactly 1. Incorrect candidates receive deterministic partial affinity according to their structural similarity with gold. These values permit: Affinity regression. Soft candidate ranking. Pairwise ranking. Listwise ranking. Knowledge distillation. Calibration of near-correct alternatives. Test File Each row of test.csv contains: sample_id partition_key board_file The test data omits: Correct blueprint identifiers. Topology codes. Role codes. Merge mass. Candidate affinities. Original table identifiers. Original document identifiers. Original annotation paths. Chamber coordinates. Hidden logical cells. Counterfactual edit histories. Source row order. Split Strategy The official train/test split is performed by complete source article. Every table associated with one article remains entirely within one split. All chambers created from one table also remain in the same split. This prevents overlap through: Repeated document typography. Shared table templates. Related column organizations. Repeated captions. Similar header conventions. Multiple tables from the same experiment. Alternative chambers cut from the same image. Large shared pixel regions. No source image appears in both training and test data. No crop from a test table appears in training. No counterfactual derived from a test chamber appears in training. Local Validation Participants should split local validation by partition_key. A random row split can place visually related boards on both sides. Related boards may share: Most of the same source image. Identical typography. The same outer table geometry. The same header hierarchy. Different masked chambers from one table. Similar tables from one article. Repeated row and column patterns. Grouped validation better measures reconstruction performance on unseen document families. Submission Format The submission contains exactly five columns: sample_id blueprint_id topology_code role_code merge_mass A conceptual row is: CTBR_A92F18,B03,T06,R04,5 Every expected sample_id must appear exactly once. Valid blueprint values are: B01 B02 B03 B04 Valid topology values are: T01 T02 T03 T04 T05 T06 T07 T08 Valid role values are: R01 R02 R03 R04 R05 R06 R07 R08 merge_mass must be a finite integer between: 0 and 4096 inclusive. Invalid submissions include: Missing samples. Extra samples. Duplicate sample IDs. Missing columns. Extra columns. Incorrect column order. Unknown blueprint identifiers. Unknown topology codes. Unknown role codes. Blank predictions. Non-numeric merge mass. Fractional merge mass. Negative merge mass. Merge mass outside the supported range. Use sample_submission.csv exactly. Evaluation Submissions are evaluated using the Counterfactual Table Topology Blueprint Reconstruction Score. The score ranges from: 0.01 to 100 Higher is better. A perfect reconstruction receives exactly: 100 The metric contains six published components: Exact Blueprint Accuracy. Blueprint Structural Affinity. Topology Macro F1. Role Macro F1. Merge-Mass Similarity. Complete Reconstruction Accuracy. There are no hidden metric components. There are no hidden metric weights. There is no model-based evaluation. Exact Blueprint Accuracy For each sample: Correct blueprint_id receives 1. Incorrect blueprint_id receives 0. Exact Blueprint Accuracy is averaged across the evaluation set. Let this value be: Blueprint Blueprint Structural Affinity For each sample: Read the submitted blueprint_id. Retrieve that candidate’s private deterministic affinity. Award the corresponding affinity value. The dataset-level average is: Affinity This component distinguishes structurally close mistakes from fundamentally incorrect reconstructions. Topology Macro F1 F1 is calculated independently for each topology code represented in the evaluation set. The class-level scores are averaged equally. Let the result be: Topology Macro averaging prevents regular grids and other frequent structural families from dominating the evaluation. Role Macro F1 F1 is calculated independently for each role code represented in the evaluation set. The class-level values are averaged equally. Let the result be: Role Merge-Mass Similarity For one sample, let: p be predicted merge mass. g be gold merge mass. The sample similarity is: MergeSimilarity = exp(-|p − g| / (g + 1)) An exact prediction receives: 1 Numerical errors receive smoothly decreasing partial credit according to their distance from the gold merge mass. The dataset-level component is: Merge which is the average MergeSimilarity across all evaluation samples. Complete Reconstruction Accuracy A sample receives complete credit only when all four targets are exact: Correct blueprint. Correct topology code. Correct role code. Correct merge mass. Otherwise, it receives zero. The dataset-level fraction is: Complete Final Score Candidate reconstruction quality is: Reconstruction = sqrt(Blueprint × Affinity) Structural interpretation quality is: Structure = (Topology × Role × Merge)^(1/3) The final score is: Counterfactual Table Topology Blueprint Reconstruction Score = 100 × Reconstruction^0.55 × Structure^0.45 × (0.90 + 0.10 × Complete) The result is clipped to: [0.01,100] A perfect submission has: Blueprint = 1 Affinity = 1 Topology = 1 Role = 1 Merge = 1 Complete = 1 and receives exactly: 100 The multiplicative composition requires both candidate reconstruction and structural understanding. A model cannot produce a strong score solely by: Estimating merge mass. Predicting the most frequent topology. Detecting header regions. Selecting candidates through superficial rendering features. Exploiting one output column while ignoring the others. Metric Reproduction For every local validation sample: Compare the predicted blueprint with gold. Retrieve the selected candidate’s affinity. Accumulate topology predictions by class. Accumulate role predictions by class. Calculate merge-mass similarity. Check complete reconstruction. Calculate topology macro F1. Calculate role macro F1. Calculate Reconstruction. Calculate Structure. Apply the final formula. Clip the result to the published range. No external resource is needed to reproduce the score. Modeling Approaches A practical system can divide the board into five visual regions: One masked-table panel. Blueprint B01. Blueprint B02. Blueprint B03. Blueprint B04. A shared visual backbone can encode all five regions. Candidate representations can then be fused with: The complete masked-table representation. Features surrounding the chamber. Detected row and column tracks. Global header features. Candidate topology features. The system can produce: Four candidate compatibility scores. One topology distribution. One role distribution. One merge-mass estimate. Vision Transformer Approach A vision-transformer model can process the full board or separate panel crops. Useful inputs include: Full-resolution board. Masked-table crop. Chamber-neighborhood crop. Four blueprint crops. Multi-scale versions of the table. Cross-attention can compare candidate structures with visible evidence surrounding the chamber. The blueprint tokens can attend to: Boundary endpoints. Repeated column positions. Repeated row positions. Header bands. Similar structural regions elsewhere in the table. Detection-Assisted Approach A structured vision system can first detect visible table components: Rows. Columns. Header regions. Spanning cells. Projected row headers. Boundary segments. Junctions. The visible detections form a partial table graph. Each candidate blueprint supplies an alternative hidden subgraph. The model or a deterministic graph layer can insert each candidate and measure: Boundary consistency. Row continuity. Column continuity. Header-tree consistency. Span regularity. Alignment with visible objects. Role compatibility. This converts the task into constrained completion over detected objects. Graph Reconstruction Approach A graph-based model can represent: Visible row bands as nodes. Visible column bands as nodes. Boundary junctions as nodes. Candidate logical cells as nodes. Adjacency and span relationships as edges. Candidate blueprints become competing graph completions. Graph compatibility features may include: Degree consistency. Boundary continuation. Repeated cell dimensions. Span termination. Header-tree depth. Role-transition likelihood. Symmetry. Local cell-area distributions. Global alignment residuals. A graph neural network can score complete candidate reconstructions after candidate insertion. Multi-Scale Reasoning The challenge contains evidence at several spatial scales. Local evidence includes: Lines approaching the mask. Nearby whitespace. Text alignment at the chamber edge. Boundary endpoints. Junction shapes. Regional evidence includes: Repeated widths across neighboring columns. Repeated heights across neighboring rows. Local header groups. Adjacent spans. Section boundaries. Global evidence includes: Complete table symmetry. Full header hierarchy. Body-grid regularity. Table-wide role organization. Repeated substructures. Models using only a small crop around the chamber may perform well on locally determined samples but fail when the decisive evidence is elsewhere in the table. Affinity Learning The four published training affinities provide richer supervision than a single correct-choice label. A model can learn affinity through: Mean-squared regression. Smooth L1 regression. Pairwise ranking. Listwise ranking. Soft-label cross-entropy. KL-divergence against normalized affinities. Margin losses ordered by structural similarity. A combined loss may use: Exact blueprint classification. Affinity regression. Topology classification. Role classification. Merge-mass regression. This encourages the model to distinguish between: Nearly correct structural alternatives. Incorrect span placement. Incorrect role assignment. Fundamentally different topologies. OCR-Assisted Reasoning OCR is permitted but not required. Recognized text outside the chamber may help identify: Header labels. Body values. Units. Repeated subcolumns. Section headings. Projected row headers. Statistical value regions. However, OCR does not reveal the concealed cell structure directly. The original chamber text is removed, and several candidates can remain compatible with the surrounding content. OCR therefore provides auxiliary functional evidence rather than an answer key. Practical Baseline A practical A10G baseline may: Load each reconstruction board. Detect the masked-table and blueprint panels. Encode all five panels using a pretrained vision backbone. Extract a higher-resolution crop around the chamber. Fuse the table representation with each candidate. Predict one candidate affinity per blueprint. Select the candidate with the highest predicted affinity. Predict topology and role codes. Regress merge mass. Write the five required submission columns. A stronger baseline can add auxiliary row, column, boundary, and junction detection losses. Stronger Systems Potential improvements include: Explicit line-segment detection. Row and column band segmentation. Chamber-interface extraction. Candidate graph parsing. Header hierarchy modeling. Multi-resolution feature pyramids. Local-global attention. Graph neural candidate reranking. Candidate affinity distillation. Counterfactual consistency loss. Rotation and scale augmentation. OCR-enhanced role prediction. Separate topology and appearance encoders. Ensemble averaging across image scales. Joint classification and integer regression. Calibration using affinity targets. Allowed Resources Participants may use: Released challenge files. Public pretrained visual models. Public pretrained multimodal models. Public pretrained OCR models. Standard numerical libraries. Standard computer-vision libraries. Standard machine-learning libraries. Standard deep-learning frameworks. Image-processing libraries. Deterministic graph algorithms. Locally derived features. Training augmentations derived from released images. Ensembles that fit the execution limits. Disallowed Resources Participants may not use: Hidden evaluation annotations. Private evaluator files. Original source identifiers. External copies of evaluation tables for structure lookup. Manual reconstruction of test chambers. Online human annotation. Hard-coded test answers. Submission-feedback reconstruction. Remote vision APIs. Remote language-model APIs. sample_id as a predictive feature. partition_key as a semantic feature. Row order as a predictive feature. Filename order as a predictive feature. General pretrained visual knowledge is allowed. Direct recovery of hidden test structures is not. Compute The execution environment provides: One NVIDIA A10G GPU. The task supports: Mixed-precision training. High-resolution visual encoding. Vision transformers. Detection transformers. Convolutional backbones. Multi-scale feature extraction. Graph neural networks. OCR-assisted systems. Compact multimodal models. Small visual ensembles. Model size, input resolution, and inference batching remain part of the competition strategy. Difficult Cases Expected difficult cases include: Borderless tables. Weak ruling lines. Grayscale compression. Dense narrow columns. Very short rows. Deep hierarchical headers. Multiple spanning-header levels. Projected row headers. Mixed header-and-body chambers. Candidates with identical exterior interfaces. Candidates differing through one internal split. Candidates with equal merge mass. Correct cell geometry paired with incorrect roles. Repeated column widths. Irregular row heights. Text baselines resembling structural boundaries. Spans inferred from distant evidence. Chambers near the transition from header to body. Visually sparse cells. Blank spanning cells. Local evidence contradicting global regularity. Several high-affinity counterfactuals. Small structural differences occupying few pixels. Limitations The benchmark focuses on cropped scientific tables. It does not directly evaluate: Full-page table detection. OCR transcription accuracy. Table question answering. Factual verification. Spreadsheet formula reconstruction. Document retrieval. Natural-language generation. Semantic interpretation of cell values. The chamber mask is an artificial visual intervention. Its hidden geometry, logical structure, and functional roles nevertheless come directly from the table’s preserved structural annotations. The challenge isolates a specific capability: Recovering a structurally valid table region after its decisive local visual evidence has been removed. Expected Outcome A successful system should: Detect visible row and column organization. Understand spanning-cell geometry. Recognize functional table regions. Infer header depth. Identify projected-header patterns. Track boundaries approaching an occluded region. Use global table regularity. Parse candidate topology diagrams. Compare legal counterfactual subgraphs. Rank near-correct alternatives. Select the exact hidden blueprint. Classify topology and role composition. Estimate logical merge complexity. Generalize across article-disjoint test data. Produce a reliable five-column submission. &nbsp;
> All-solver grace
> Grace ends in 46m
> $700 Pool
> Lockdown

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Underground Object Depth Ordering

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79j0n1yyjyhrfhp4yk1ftd558dvxr4
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; challenge detail page timed out
- Difficulty: Medium
- Compute: Not displayed; challenge detail page timed out
- GPU: Not displayed; challenge detail page timed out
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage card score context: Beat komilpamar's score of 0.421!

Full challenge description from page:

> Underground Object Depth Ordering Overview Deep underground galleries are visually hostile: the only light is a moving head-lamp, dust and water haze scatter it, rock faces are near-textureless, and the objects that matter — cables and ducting strung along the ribs, roof-anchor hardware, indicator boards, standing machinery, electrical cabinets, rail sections, the occasional person — recur across frames at wildly varying range and pose. A camera-mounted range sensor recorded, for each frame, how far every labelled object actually sat from the lens; that range channel and the object outlines are withheld. Given only the colour frame, a solver must recover the front-to-back depth ordering of the objects present in the scene — which object is nearest the camera, which sits furthest down the gallery, and everything in between. The task is deliberately not "estimate a depth map". It is a relative ordering problem over a fixed vocabulary of scene objects, scored so that the scene-independent tendency — the average distance at which each kind of object tends to appear — earns nothing. Objects in these galleries are not fixed scenery: the same cable run is right at the lens in one frame and far down the drift in the next, machinery is parked at varying stand-off, an indicator board floats near or far. Empirically the average ordering explains barely more than half the pairwise relations in a scene, so credit accrues almost entirely to reading the per-scene geometry from a single low-light frame. Doing that requires learning both what each object is — the vocabulary is specific to this environment and does not match everyday imagery — and how its monocular appearance cues range under head-lamp lighting. Dataset The data are single colour frames captured in underground galleries, each paired (privately) with a per-object range reading derived from a co-mounted range sensor. Every frame is labelled with the depth rank of each object class that is visibly present in it. Public files train.csv — one row per training frame. Columns: id, image, and the fifteen target rank columns listed under Column descriptions. test.csv — one row per test frame. Columns: id, image only. The rank columns are withheld. train/… and test/… — the colour frames referenced by the image column, as JPG files. train/depth/.png and train/mask/.png — training frames only: the co-registered 16-bit range image (per-pixel range, 0 = no return) and the object-index outline map (0 = background, otherwise the class index) for each training frame, provided as auxiliary supervision at an id-derived path. No such files are provided for the test split. sample_submission.csv — a valid submission with the exact columns a submission must have. Private file (organizer only) answers.csv — columns id plus the fifteen rank columns: the ground-truth depth rank of every object class for each test frame. Column descriptions Each row corresponds to one colour frame. Columns are: id (string) — opaque frame identifier (e.g. img_9f2c1a4b7d0e8c15). Carries no ordering information. image (string) — relative path to the colour JPG for this frame (e.g. test/img_9f2c1a4b7d0e8c15.jpg). The fifteen rank_ columns (integer) — the per-class depth rank. In the *ground truth* (train.csv targets and answers.csv), each of the k object classes *present* in the frame gets an integer rank 1…k (1 = nearest, k = furthest among the present classes), and every class *not present* gets 0. Only present classes (rank ≥ 1) are scored. In a *submission* the encoding is different — you emit a *strict permutation of 1…15* over all fifteen columns (see *Submission format); the grader reads the front-to-back order your permutation induces and scores it only on the classes that are truly present in that frame. The fifteen object classes (column name → what it denotes): rank_cable — power/comms cabling runs rank_fixture — metal fixtures and brackets rank_indicator — indicator boards and gauges rank_tube — pipes, hoses and ducting rank_electronic — electronic equipment units rank_anchor — roof/rib anchoring hardware rank_machinery — heavy mining machinery rank_rail — rail track sections rank_electrical — electrical cabinets and gear rank_supplies — loose tools and materials rank_support — support / bracing equipment rank_door — doors and gates rank_container — containers and bins rank_rescue — rescue equipment rank_person — a person Split and anti-memorization Frames are grouped into near-duplicate visual clusters — the corpus contains several head-lamp exposures of the same gallery stretch, and these are pooled by a shared capture-station key and a perceptual hash. Each cluster is assigned wholly to train or to test, so no test frame has a near-duplicate twin in the training split and a solver cannot win by memorizing a training frame's ranks and copying them onto a look-alike test frame. Only the abstract object vocabulary and the range-cue statistics are shared across the split; every test frame is a genuinely unseen scene. The withheld range channel and object outlines mean the test ordering cannot be read off any provided artefact and must be inferred from the colour frame. Test frames are further restricted to scenes with at least two present object classes whose ordering is not already fixed by the average tendency (see Evaluation), so the held-out set measures per-scene reasoning rather than the global prior. Data example A truncated train.csv row. Here five classes are present (ranks 1…5, near→far) and the other ten are absent (0): id,image,rank_cable,rank_fixture,rank_indicator,rank_tube,rank_electronic,rank_anchor,rank_machinery,rank_rail,rank_electrical,rank_supplies,rank_support,rank_door,rank_container,rank_rescue,rank_person img_9f2c1a4b7d0e8c15,train/img_9f2c1a4b7d0e8c15.jpg,3,4,0,2,0,5,0,0,0,0,1,0,0,0,0 Submission format Submit a CSV with a header and exactly one row per test id. Required columns, in this order: id,rank_cable,rank_fixture,rank_indicator,rank_tube,rank_electronic,rank_anchor,rank_machinery,rank_rail,rank_electrical,rank_supplies,rank_support,rank_door,rank_container,rank_rescue,rank_person Each of the fifteen rank_ columns is an integer, and together they must form a *strict permutation of 1…15** for every row (each integer 1…15 appears exactly once per row). 1 = nearest object, 15 = furthest. Exactly one row per test id — no missing ids, no unknown/extra ids, no extra columns. Sample submission (constant ordering — the same permutation on every row): id,rank_cable,rank_fixture,rank_indicator,rank_tube,rank_electronic,rank_anchor,rank_machinery,rank_rail,rank_electrical,rank_supplies,rank_support,rank_door,rank_container,rank_rescue,rank_person img_9f2c1a4b7d0e8c15,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 img_2b7e0d1c6a3f9e84,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 Evaluation The metric is the Scene Ordering Skill (SOS), macro-averaged over test frames. It measures how well a submission orders the object classes present in a frame relative to a fixed scene-independent baseline order, so that reproducing only the average "how far each object kind usually sits" tendency scores zero and credit accrues solely to per-scene ordering. For one frame, let S be the set of object classes present in it (a class counts as present when its outline covers at least 0.5% of the frame; frames with fewer than two present classes are excluded from the test set). Let r* be the ground-truth depth order restricted to S, and r_sub the order that the submitted permutation induces on S. (1) pairwise concordance of an order against the ground-truth order on S. conc = fraction of present-class PAIRS placed in the correct near/far order. conc = (kendall_tau + 1) / 2, so a random order -> 0.5 and a perfect order -> 1. def conc(order_on_S, truth_on_S): pairs = [(a, b) for a, b in combinations(S, 2)] correct = sum(1 for a, b in pairs if sign(order_on_S[a] - order_on_S[b]) == sign(truth_on_S[a] - truth_on_S[b])) return correct / len(pairs) For each test frame f: C_sub[f] = conc(r_sub, r*) # submission's concordance on frame f C_prior[f] = conc(PRIOR_ORDER, r*) # fixed baseline order's concordance on frame f miss[f] = 1.0 if truth_rank_of(argmin_S(r_sub)) > median_rank(S) else 0.0 (2) skill score, referenced to the baseline order (a ratio of means over all frames, NOT a per-frame ratio): the baseline order -> 0, the exact order -> 1. base = sum(C_sub[f] - C_prior[f] for f) / sum(1.0 - C_prior[f] for f) (3) nearest-object penalty (mean over frames), subtracted after the skill score. penalty = LAMBDA * mean(miss[f] for f) # LAMBDA = 0.10 SOS = max(0.02, min(1.0, base - penalty)) PRIOR_ORDER is the single fixed near→far ordering of the fifteen classes that best matches the corpus's pairwise depth orderings — the concordance-optimal constant order (documented as a constant in the grader; it is exactly what a solver recovers by fitting the best constant order to the training ranks). Because no constant order beats PRIOR_ORDER on the corpus, referencing the score to it makes any image-blind constant submission score base ≤ 0 — the scene-independent tendency earns nothing, and credit is left only for reading each frame's own geometry. base (the positive signal) is a skill score: the total concordance the submission gains over the baseline order, divided by the total concordance the baseline itself leaves on the table. It is 0 for the baseline order, 1 for the exact order, and negative for orderings worse than the baseline. It is aggregated as a ratio of sums across frames (not an average of per-frame ratios), which keeps frames the baseline nearly solves from dominating the score. penalty (LAMBDA = 0.10) subtracts the fraction of frames where the submission places a genuinely far object (true rank in the farther half of the present set) at the nearest position — the most operationally harmful ordering error. It is applied after base (never as a multiplier), so it always makes a submission worse. Frames the baseline already solves (C_prior > 0.9) and frames with fewer than two present classes are excluded from the test set. The headline SOS is base - penalty, floored at 0.02 and capped at 1.0. Baseline (chance). A random strict permutation, and any fixed constant ordering (including PRIOR_ORDER itself), score base ≤ 0 and, after flooring, sit at 0.02. A submission that recovers the true per-scene order exactly scores 1.0. Higher is better. SOS is maximized by ordering each frame's present objects front-to-back correctly, beyond what the fixed global order already explains, while never placing a far object nearest. What Not To Use (Prohibited Methods) No external answer keys or source lookups. Do not use any external range/depth maps, object-outline masks, camera-range metadata, or full multimodal captures for these scenes to recover test ranks. Do not attempt to match test frames or their ids back to any external image collection, publication, or repository to obtain the withheld range channel. No id-based hardcoding. id values are opaque hashes and encode no ordering. Do not build id-to-rank lookup tables, and do not exploit row order, file order, or id order — they are shuffled and carry no signal. No train/test leakage. Clusters of near-duplicate captures are held disjoint across train and test precisely to forbid this. Do not search for a training near-duplicate of a test frame and do not train on, or copy ranks from, any frame you believe to be a near-duplicate of a test frame. No private-label tuning. The test range channel, test object outlines, and answers.csv are organizer-only. Do not manually estimate, annotate, or eyeball test-frame depth orders by hand; the submission must come from a method that generalizes from the training supervision. Allowed. Any model trained or fine-tuned on the provided training frames, their range images, and their object outlines; any publicly pretrained vision backbone used as a starting point; any use of the training ranks to estimate the global baseline order. &nbsp;
> $700 Pool
> Closes in 11h 2m
> 10 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Foot Pressure Image Reconstruction From Walking Motion Tensors

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78epbn1pd0rx2hyv6j573e998a3q4s
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Draft
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Overview This is a Computer Vision challenge. The object to predict is a one-channel foot pressure image: a 40 x 40 spatial grid of measured plantar pressure pixels. The public input is not a photograph, but it is an image-like motion tensor from a walking trial, and the intended task is dense image reconstruction. Clinical walking-analysis labs record detailed foot motion and joint moments together with plantar pressure platforms. In this challenge, each row gives a real stance-phase walking-motion tensor from a right-foot walking trial, and the goal is to reconstruct the measured right-foot peak contact-pressure image for the same trial. Unlike common walking-analysis benchmarks that classify gait, regress a scalar clinical score, estimate joint kinetics, or model pressure-platform data from pressure measurements alone, this benchmark asks for the spatial pressure image that is not present in the input. The useful signal must pass across modalities: 18 stance-phase motion/moment curves have to be converted into a two-dimensional plantar loading field with correct support, hotspot placement, peak pressure, and center of pressure. A model that treats the row as a generic tabular regression target or a gait-label prediction leaves the central image-reconstruction object unresolved. Each input .npz file contains a curves tensor of shape (18, 100). Treat this as an 18-channel by 100-pixel motion image: the channels encode multi-segment foot rotations and moments over 100 normalized stance-frame positions. The target is not a rendered heatmap or a class label; it is a measured one-channel pressure image from pressure-platform sensor cells. Public ids are opaque, raw subject and trial identifiers are stripped, and rows are split by held-out subject. Task Train on labeled walking trials and predict held-out-subject walking trials. For each test .npz, load the motion-image tensor, infer the plantar loading pattern from the stance-phase motion and moment signal image, and emit a full pressure image plus auxiliary summary values. Test rows are independent: the public id exists only for row alignment and carries no biomechanical or source-order meaning. The benchmark is framed around cross-modal pressure-image synthesis: the public tensor is a compact motion image and the hidden target is a measured sensor image. It is distinct from pressure-based gait recognition, pose estimation, foot-posture classification, and scalar biomechanics prediction because those tasks do not require reconstructing the unseen 40 x 40 loading map for a held-out subject. The train/test split is made at the participant level: all walking trials from a person are assigned entirely to train or entirely to test. This matters because repeated trials from the same participant share body geometry, foot posture, movement signatures, and pressure-footprint tendencies; putting trials from one participant on both sides would let a solver memorize person-specific loading templates. After the split, public ids are regenerated from salted hashes and sorted independently, so ids, filenames, and row order do not reveal the source participant, trial number, or private split rule. For each test row, predict: pressure_field: the 40 x 40 peak pressure image flattened row-major into 1600 pressure-pixel intensities separated by spaces. peak_pressure: the brightest pressure-pixel value in N/cm^2. center_of_pressure_x and center_of_pressure_y: image-center coordinates normalized to [0, 1]. confidence: your calibrated confidence in [0, 1]. Intended Approaches This is an image-to-image / tensor-to-image Computer Vision task, not a metadata or lookup task. Natural approaches include U-Net-style decoders, DeepLab/SegFormer-style dense heads, convolutional encoder-decoders, vision-transformer image decoders, temporal CNN or TCN encoders over the 18-channel motion image followed by a 2D pressure-image head, and learned pressure-image bases. Classical walking-motion features may be useful, but they should feed a learned dense-image model rather than replace it with fixed rules. Use the released public training labels to fit pressure-image bases, preprocessing layers, calibration models, and validation folds. The held-out-subject split means a model should generalize across people, not memorize trial templates. Good submissions should recover foreground pressure support, high-pressure hotspot regions, center-of-pressure, and peak pressure together; optimizing only a peak value or only a population-average pressure image is deliberately weak. Generic Python and computer-vision ML libraries such as NumPy, pandas, scikit-learn, PyTorch, TensorFlow, JAX, timm, segmentation-model libraries, and transformer libraries are allowed when they are used to train or adapt a model from the released public training data. What Not To Do Do not use external raw-source lookup, source-row reconstruction, filename lookup, row order, raw participant or trial identifiers, hidden private columns, hard-coded answer lists, or any attempt to infer labels from source archive order. Do not use external task-specific plantar-pressure labels, private answer files, source-row matching, test-set pseudo-labeling, transductive fitting on test rows, or precomputed answer tables. Do not submit a metadata-only prior, peak-only pressure guess, label-only walking-pattern model, pressure-image template matching method, or fixed rule pipeline as a substitute for reconstructing the measured loading image from the public motion tensor. Enforcement on invalid approaches: rule-only shortcuts, hard-coded lookup solutions, or submissions that do not solve the intended dense pressure-image reconstruction task may be rejected before payout. Dataset The public folder contains train/test manifests, a sample submission, a feature-name JSON file, and per-row .npz motion-image tensors. | Item | Description | |---|---| | train.csv | Train inputs plus labels | | test.csv | Test inputs only | | sample_submission.csv | Valid weak template | | input_feature_names.json | Curve channel order | | train/inputs/*.npz | Train motion tensors | | test/inputs/*.npz | Test motion tensors | train.csv gives one row per labeled walking trial. test.csv gives one row per held-out walking trial. sample_submission.csv is a weak valid template in the exact submission schema. input_feature_names.json lists the 18 channel names in the order used by every motion tensor. The .npz paths are relative to the public folder. train.csv columns | Column | Type | Description | |---|---|---| | id | int | Opaque row id | | image_path | string | Path to tensor image | | pressure_field | string | Flattened pressure image | | peak_pressure | number | Max pressure | | center_of_pressure_x | number | COP x in [0,1] | | center_of_pressure_y | number | COP y in [0,1] | id is an anonymized public row identifier. image_path points to a .npz tensor-image file with the curves tensor of shape (18, 100). The train-only label columns are pressure_field, peak_pressure, center_of_pressure_x, and center_of_pressure_y. test.csv columns | Column | Type | Description | |---|---|---| | id | int | Opaque row id | | image_path | string | Path to tensor image | id is the test row identifier that must appear exactly once in the submission. image_path points to a test .npz tensor-image file with the same motion-tensor layout as the train inputs. Test pressure images are not public. The motion-tensor channel order is: R_ANK_AB, R_ANK_INV, R_ANK_DF, R_MT_AB, R_MT_INV, R_MT_DF, R_MP_AB, R_MP_INV, R_MP_DF, M_ANK_AB, M_ANK_INV, M_ANK_DF, M_MT_AB, M_MT_INV, M_MT_DF, M_MP_AB, M_MP_INV, M_MP_DF. Submission Submit a CSV with exactly these columns in exactly this order. | Column | Type | Constraint | |---|---|---| | id | int | Match test ids | | pressure_field | string | 1600 pressure pixels | | peak_pressure | number | 0 to 90 | | center_of_pressure_x | number | 0 to 1 | | center_of_pressure_y | number | 0 to 1 | | confidence | number | 0 to 1 | pressure_field must contain exactly 1600 finite pressure-pixel intensities in row-major order for a 40 x 40 pressure image. Values must be non-negative and no greater than 90 N/cm^2. peak_pressure, center_of_pressure_x, center_of_pressure_y, and confidence must be finite numbers in their allowed ranges. Requirements The grader rejects a structurally invalid submission rather than repairing it. The CSV must contain exactly the six columns listed above, in that order, with no missing or extra columns. It must contain exactly one row for every id in test.csv; missing ids, extra ids, duplicate ids, non-integer ids, fractional ids, and invalid confidence values are invalid submission-file errors. Malformed row-local prediction content does not collapse the whole submission. If a row has an empty, overlong, non-numeric, wrong-length, negative, or physically impossible pressure_field, or non-finite/out-of-range auxiliary prediction values for peak_pressure, center_of_pressure_x, or center_of_pressure_y, that row receives zero task credit and zero calibration credit. Other valid rows in the same submission are still scored normally. Example submission rows: | id | pressure_field | peak_pressure | center_of_pressure_x | center_of_pressure_y | confidence | |---:|---|---:|---:|---:|---:| | 101 | 0.000 0.000 0.250 ... 0.000 | 24.375 | 0.482 | 0.613 | 0.64 | | 205 | 0.000 0.100 0.400 ... 0.000 | 31.820 | 0.516 | 0.587 | 0.71 | Evaluation Each row is scored in [0, 1]. Let Y be the true 40 x 40 pressure image and P be the submitted pressure image. The main pressure-field term is image-based: it rewards local structural similarity, coarse-scale image layout, pressure-edge alignment, foreground support overlap, and high-pressure hotspot overlap. S_image = 0.34local_SSIM + 0.18pooled_SSIM + 0.14edge_alignment + 0.16support_mask_F1 + 0.18*hotspot_mask_F1 local_SSIM is a structural-similarity score computed on the full 40 x 40 pressure image. pooled_SSIM applies the same structural comparison after 2 x 2 average pooling, so the metric also rewards correct overall plantar-loading layout. edge_alignment compares the pressure-image gradients, while the support and hotspot terms are Dice/F1-style image mask overlaps. The auxiliary heads are scored from the peak-pressure pixel and the center-of-pressure location. The center-of-pressure term uses both the submitted coordinate and the coordinate implied by the submitted pressure image. S_peak = exp(-abs(pred_peak - true_peak) / max(0.20*true_peak, 1.0)) S_cop = 0.70exp(-submitted_cop_distance / 0.075) + 0.30exp(-field_cop_distance / 0.090) core = 0.76S_image + 0.10S_peak + 0.14*S_cop The final score is: Final = 0.80mean(core) + 0.06lowest posture-family mean + 0.05lowest peak-pressure-bucket mean + 0.05lowest loading-pattern mean + 0.04*mean(calibration) Calibration is 1 - (confidence - core)^2, clipped to [0, 1]. Hidden robustness groups are private and are based on real biomechanical pressure and posture properties. The theoretical minimum is 0.0 and the theoretical maximum is 1.0; exact private labels score exactly 1.0. The hidden group terms cover three real axes from the held-out rows: foot-posture family neutral_posture, supinated_posture, pronated_posture, with sparse groups coarsened if needed), peak-pressure tertiles low_peak_pressure, mid_peak_pressure, high_peak_pressure), and center-of-pressure loading tertiles medial_loading, central_loading, lateral_loading). Each group term is a worst-group mean over private test rows, so the final score rewards pressure-image reconstruction that works across posture, loading intensity, and spatial loading pattern instead of only optimizing the average row. Submissions with structural file errors raise InvalidSubmissionError: missing, extra, or reordered columns; duplicate ids; id-set mismatch; non-integer ids; or invalid confidence. Row-local malformed prediction content, including malformed pressure_field strings, wrong pressure-image length, non-finite or impossible pressure values, and invalid auxiliary prediction heads, gives zero credit only for that row and cannot earn calibration credit.
> 4h ago
> $400–$500
> Draft

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Multi-Apartment Room and Door Graph Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7e7t645w4j1fg411tn8h50sh8dtf1b
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat crocx's score of 0.611!

Full challenge description from page:

> Overview Recover individual room shapes, their uses and the door connections between them from an unlabelled multi-apartment floor plan. Return a separate mask for every scored room, assign its type and connect room pairs joined by an internal door. Walls, openings and fixtures are visible; room names and semantic colors are absent. The output supports spatial indexing of digitized residential floors. Adjacent rooms of the same type must remain separate, including repeated rooms across different apartments. Shared walls alone do not imply a door connection, and recognizing a large living area does not compensate for missing smaller rooms. Dataset There are 1,178 training floors and 288 test floors, with housing sites held out. Each floor contains three to six source apartments. Inputs are 768 × 768 grayscale PNGs. Each room has a 256 × 256 binary mask aligned with the full image; row indices increase downward and columns rightward from the upper-left corner. The output schema supports up to 64 scored rooms per floor. | File | Columns / contents | |---|---| | train.csv, test.csv | task_id: unique string; image_path: relative PNG path | | train_labels.csv | task_id, target_json: JSON string in the submission format | | sample_submission.csv | task_id, target_json: random rectangle-and-link examples for all test IDs | | images/ | One input image per plan | Housing sites and their buildings stay in one split; only one floor per source plan is retained, and exact duplicate rendered plans are removed. Similar architectural layouts may still occur across sites. Room uses can be visually ambiguous. Only the listed room categories in residential units are targets; shared utility or circulation areas outside those units are unscored. Door links are derived from native opening-to-room geometry; floors with ambiguous multi-room door contacts are excluded. Windows, entrance doors, passages without a native door and links to unscored areas are not targets. Multiple doors between the same room pair count as one connection. The resulting graph may have separate components for different apartments; it is not a building-wide exit or safety map. The room types are: | Type | Meaning | |---|---| | 1 | Generic room | | 2 | Bedroom | | 3 | Living room | | 4 | Living/dining room | | 5 | Kitchen | | 6 | Bathroom | | 7 | Corridor | | 8 | Balcony | | 9 | Storeroom | Submission Submit a UTF-8 CSV with exactly task_id,target_json, in that order, and every test ID exactly once. Each JSON object has exactly two keys: rooms: a list of 0–64 objects, each containing exactly type and runs. type is an integer from 1 to 9. runs encodes one room's mask in row-major order as [binary_value, count] pairs. Values are integers 0 or 1, counts are integers 1–65,536, and counts sum to 65,536. Each mask must contain foreground; room masks must not overlap. There may be at most 65,536 runs per mask. doors: at most 2,016 distinct [a,b] pairs indexing the rooms list, with integer indices satisfying 0 <= a < b < number_of_rooms. Self-links and repeated pairs are invalid. List order does not matter. Room ordering is arbitrary if the door indices are updated consistently. All numbers must be JSON integers, not booleans or floating-point values. Extra or duplicate JSON keys are invalid. Maximum JSON length: 2,000,000 characters. These illustrative masks demonstrate the format, not actual test answers: task_id,target_json floor_example_a,"{""rooms"":[{""type"":1,""runs"":[[1,32768],[0,32768]]},{""type"":6,""runs"":[[0,32768],[1,32768]]}],""doors"":[[0,1]]}" floor_example_b,"{""rooms"":[],""doors"":[]}" Evaluation The metric is multi-threshold room-and-door graph F1, averaged across floors and ten mask-IoU thresholds. Higher is better, from 0 to 1. A predicted room matches a reference room when their types agree and mask intersection-over-union is strictly greater than the current threshold. Evaluate thresholds 0.50, 0.55, ..., 0.95. Disjoint masks make the matches one-to-one. At each threshold, a predicted door is correct only when both endpoint rooms match and the corresponding reference rooms have a door link. TP(t) = rooms matched at threshold t + correct door links at threshold t P = predicted rooms + predicted door links G = reference rooms + reference door links F1(t) = 2 * TP(t) / (P + G) floor_score = mean(F1(t) for t in 0.50, 0.55, ..., 0.95) score = mean(floor_score across evaluated floors) Lower thresholds measure room identification; higher thresholds require precise shapes. Averaging the fixed range distinguishes rough outlines from accurate geometry, instead of giving every room above IoU 0.50 the same credit. Each room or connection is one graph element; links involving unmatched rooms earn no credit. This is graph F1 across geometric tolerances, not confidence-ranked AP or a transformation of a single score. A perfect reconstruction scores 1. An empty prediction scores 0 on this release. If both graphs are empty, every threshold scores 1. A random submission can score zero. Invalid row JSON, overlapping masks or invalid door indices score zero for that row. Incorrect headers, duplicate/missing/extra IDs, empty files and inconsistent CSV row widths cause file-level errors. Rows are aligned by ID. What Not To Use Generic pretrained visual encoders and GPU training are allowed. Do not use floor-plan-specific pretrained checkpoints, external labeled floor plans, original source copies, image lookup, test-answer dictionaries, hosted APIs or manual test annotation. &nbsp;
> $700 Pool
> 2 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Cross-Projection Design Retrieval

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71sz0en9phh1xh9kajcq97dx8dvpd7
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat haidang's score of 0.434!

Full challenge description from page:

> Overview Given one technical drawing, retrieve views of the same product design shown in a different projection family. Distinguish the exact design from similar products and from same-family views of that design. This supports linking complementary drawings when organizing visual design documentation. Projection families are perspective, front/rear elevation, left/right side, and top/bottom plan. Front and rear belong to the same family; so do left and right, and top and bottom. A relevant result must depict the same design in a different family. A matching object category alone is insufficient. Dataset There are 231 training queries from 89 designs and 210 test queries from 77 held-out designs. The training gallery contains 1,136 images and the test gallery 821 images. Each query is also a gallery image. Images are 384 × 384 grayscale PNGs; each query has 1–5 relevant views. Entire design records remain in one split. The galleries also include distractor-only designs, so not every gallery image is a query. Every query has at least three other designs from its detailed product category in the corresponding gallery. Product categories and projection labels are not supplied as input fields. Source crop/metadata dimension mismatches, identified contaminated crops, ambiguous detail/embodiment annotations and high-similarity cross-design copies were excluded. Queries with rotation/reflection near-copies among their cross-family positives were excluded. Remaining extraction or view-description errors are possible; symmetric products and sparse drawings can also be visually ambiguous. This historical sample does not cover all modern product styles. | File | Columns / contents | |---|---| | train.csv, test.csv | task_id: unique string, also the query image ID; image_path: relative PNG path, string | | gallery.csv | image_id: unique string; image_path: relative PNG path, string; gallery_split: train or test | | train_labels.csv | task_id, target_json: JSON string containing all relevant retained training-gallery IDs | | sample_submission.csv | task_id, target_json: random test-gallery rankings | | images/ | One PNG per gallery image, shared with query references | For queries in train.csv, search gallery rows with gallery_split = train; for queries in test.csv, use gallery_split = test. Join a query's task_id to the gallery's image_id. Split membership is recorded only in the combined gallery table, where both values occur. Submission Submit a UTF-8 CSV with exactly task_id,target_json, in that order, and every test ID exactly once. Each JSON object contains only ranking, an ordered list of 0–10 distinct image-ID strings, most relevant first. IDs must come from the query's gallery split and differ from its query ID. IDs are nonempty and at most 100 characters; each JSON string is at most 20,000 characters. task_id,target_json view_example_a,"{""ranking"":[""view_example_b"",""view_example_c""]}" view_example_b,"{""ranking"":[""view_example_a""]}" Use actual query/gallery IDs. Missing, extra or duplicate task IDs, incorrect headers and inconsistent CSV row widths invalidate the file. Row order is irrelevant. Invalid JSON, duplicate/extra JSON keys, duplicate ranked IDs, self-retrieval and oversized lists score zero for that row. Unknown or wrong-split image IDs receive no relevance credit and consume their ranked positions. Evaluation The metric is standard mean average precision at 10 (MAP@10), from 0 to 1; higher is better. A result is relevant only when it shows the same design in a different projection family. Same-family views receive no relevance credit even when the design matches. For a query with R relevant gallery views, let rel[k] equal 1 for a relevant result at rank k, otherwise 0. Let precision[k] be the fraction of relevant results among the first k positions. AP@10 = sum_k (precision[k] × rel[k]) / min(10, R) MAP@10 = mean AP@10 across evaluated queries The sum uses submitted ranks up to 10; omitted positions contribute zero. All queries have at least one relevant view. Returning all relevant views first scores 1; an empty ranking scores 0. This metric rewards finding complementary views early without rescaling the score. What Not To Use Generic pretrained visual encoders and GPU training are allowed. Do not use design-patent-specific pretrained checkpoints, external labeled design figures or source copies, original-filename matching, reverse image search, test-answer dictionaries, hosted APIs or manual test annotation. &nbsp;
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Drawing Stroke Assembly and Precedence Prediction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75mg2vmqxvh9sxnryz6wyywd8ay9tt
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat masry1's score of 0.476!

Full challenge description from page:

> Drawing Stroke Assembly and Precedence Prediction Overview Each example shows you the same drawing twice: a finished 256-by-256 colour composite, and an unordered inventory holding the individual monochrome pen strokes that were used to make it. Your task is to put every inventory stroke back where it belongs in the composite, and to recover which stroke lies visually above the other at each place where two of them cross. This is not sketch classification and it is not free-form vectorization. Every piece that has to be localized is already handed to you. What you return is a compact assembly program: one affine placement per piece, followed by zero or more directed precedence edges. Training rows — 1,260, each with its gold assembly program. Test rows — 420, unlabelled. Pieces per row — 3 through 8. Composite — one 256-by-256 RGB PNG per row. Inventory — one RGB PNG per row, a contact sheet of 64-by-64 cells. Placement output — three transformed anchors per piece. Relationship output — directed above-below edges between overlapping pieces. Training and test use disjoint source families. Each source trajectory is given a piece-specific non-linear warp that is shared by both released views, followed by an episode-level affine placement. Because the warp is shared, the correspondence between an inventory piece and its appearance in the composite is genuine and visible; because it is non-linear, exact raw-stroke matching is not the intended route. What Makes This Hard The two subtasks are coupled. You cannot rank the crossings until you know where the pieces went, and a placement that is a few pixels out turns a crossing that should be read one way into one that reads the other. Neither half is worth much alone: a perfect set of placements with no edges at all scores 0.44, and a perfect edge graph over placements that are worthless scores 0.36. Nothing is free. A submission that never opens either image has been measured. Putting every anchor of every piece at the single point that best fits the training placements, and asserting every ordered pair, scores 0.063; the placement half of that alone scores 0.042, and the placeholder in sample_submission.csv scores 0.030. Those are the floors this task starts from, stated here so nobody mistakes them for progress. The inventory tells you nothing about order. Cell order is shuffled independently for every example, so a piece's index carries no information about its position, its size, or when it was drawn. Gold edges run from the lower index to the higher one in 52 percent of cases, which is a coin flip. The precedence is local. Two pieces are ordered only where they actually overlap, and the evidence is a small patch of visible colour at the crossing. A non-overlapping pair has no edge and no relative order to find. The families are cold. Every test row is drawn from source families that no training row ever showed you, so a model that has learned the habits of the training families rather than the geometry of the problem will not transfer. Where The Answers Come From Every answer is a recorded fact of how the row was built. The placement is the affine transformation that was actually applied to that piece when the composite was rendered, expressed through three canonical anchors. The precedence is the order in which the pieces were drawn onto the canvas: at a crossing, the later piece covers the earlier one, so the earlier one is below. Gold edges exist only where two pieces genuinely meet — their width-8 canonical raster supports must share at least ten pixels. Every official row has at least one such overlap. Nothing in the published views states any of these numbers; they have to be read out of the pixels. From-Scratch Requirement This is a from-scratch computer-vision challenge. Every learned parameter used by a submitted system must be trained only from the released challenge training data, inside solution.py, during the graded run. Loading weights fitted beforehand, or shipping a model with the submission, does not satisfy this. Classical image processing and optimization require no training and are fully allowed. Allowed approaches include: thresholding, morphology, skeletonization, connected components, contour and shape descriptors; affine registration, template matching between the two released views, RANSAC, graph matching, and constrained optimization; models initialized with random weights and trained only on released train.csv images and targets; self-supervised learning using only released challenge images; augmentations created only from released training images; and ensembles whose every component satisfies these rules. The intended solution space is released-image correspondence and geometry, not semantic recognition and not recovery of any public source. What Not To Use No pretrained or externally trained model weight, checkpoint, adapter, embedding, codebook or learned feature extractor of any kind, including general vision, vision-language, sketch, vectorization, segmentation, retrieval and foundation models, and no features, embeddings or labels produced by one. No external images, stroke vectors, sketch datasets, generated sketch corpora, annotations, embeddings, cached features, pseudo-labels or category labels. No copy or derivative of the upstream source records, including source keys, categories, filenames, line numbers, recognized flags, raw trajectories or rendered source bitmaps. No source-record identification or lookup by hashes, perceptual hashes, reverse-image search, nearest-neighbour retrieval, vector matching, category recovery or metadata inference, and no use of a recovered source identity or source order to infer placements, precedence edges or test outputs. This is grounds for automatic disqualification. No hosted inference, search, retrieval or labeling APIs, no remote services, and no network access at grading time. No use of the test set beyond ordinary per-row inference: no training on test rows, no pseudo-labelling, and no fitting, calibrating, thresholding or normalising with statistics pooled across the test set. No manual test labeling, no private-answer access, no hard-coded test predictions, and no pipeline that contains a prohibited component even when that component is frozen or used only offline. No hardcoded lookup tables and no fingerprinting of row identifiers, filenames or row order. Identifiers and filenames are opaque and carry nothing. Evidence Every row is two PNG images. The composite holds all pieces on a lightly textured background. Strokes are coloured so that pieces which overlap are visually distinguishable. At a crossing, the piece rendered later covers the one rendered earlier and therefore determines the visible top colour. That visible colour is the evidence for the precedence edge. The inventory is a contact sheet with four columns and one or two rows of 64-by-64 cells, each holding one monochrome piece. Read the non-blank cells in row-major order: the first non-blank cell is p00, the second is p01, and so on through p(piece_count - 1). Blank trailing cells are padding and must not receive predictions. Cell order is shuffled independently for every example. Validating Your Model The leakage unit is the source family. Every test row comes from families that appear in no training row, and no released column names the family, so you cannot group by it directly. Validate by holding out whole rows, and expect a held-out score to sit above what you will see at test time, because rows of the same training family share a source that test rows never do. A random split of rows flatters a model that has learned family habits rather than geometry. Evaluation Each valid row receives a placement score and an edge score. Placement. For each of the three anchors of every piece, let d be the Euclidean distance in pixels between the submitted and the gold coordinate. Anchor accuracy is $$ A(d)=\exp\left[-\frac{1}{2}\left(\frac{d}{16}\right)^2\right]. $$ The row's placement score is the mean anchor accuracy over all pieces and all anchors in that row. Precedence. Let P be the submitted directed edge set and G the gold directed edge set. The edge score is $$ \mathrm{edge}=\max\left(0,\ \frac{|P\cap G|-\tfrac{1}{2}|P\setminus G|}{|G|}\right). $$ A correct edge earns one unit, a wrong edge costs half a unit, and the total is divided by the gold edge count and floored at zero. Predicting many pairs in the hope of catching a few therefore does not pay, and guessing a direction at random on an overlapping pair is worth almost nothing in expectation. Every official row has at least one gold overlap, so an empty submitted edge set receives a zero edge score. Row score. First compute $$ \mathrm{base}=0.55\,\mathrm{placement}+0.45\,\mathrm{edge}, $$ then apply a soft balance term: $$ R=\mathrm{base}\left[0.8+0.2\min(\mathrm{placement},\mathrm{edge})\right]. $$ The balance term rewards solving both subtasks without creating a hard threshold. Holding the other component fixed, improving placement or the edge score cannot reduce the score. Perfect placement with no edges scores 0.44; perfect edges with zero placement scores 0.36. Final aggregation. The reported score combines four terms and is bounded to the interval from 0 to 1. Overall, weight 0.50 — the mean row score over all test rows. Piece macro, weight 0.15 — the unweighted mean of three piece-count buckets: small is 3 to 4 pieces, medium is 5 to 6, large is 7 to 8. Crossing macro, weight 0.15 — the unweighted mean of three crossing-density buckets. Crossing density is the gold edge count divided by C(piece_count, 2); it is sparse below 0.18, medium from 0.18 inclusive to 0.36 exclusive, and dense at or above 0.36. Hard mean, weight 0.20 — the mean over rows with at least seven pieces or at least six gold edges. These slices affect only how row scores are aggregated. They never change the row grammar, and the bucket a row falls into is not published. Split and Leakage Training and test source families are disjoint. Public identifiers and filenames are opaque, and no source category, record key, stroke order, line number or upstream metadata is released through train.csv, test.csv, images/ or task_manifest.json. Row order is randomised and carries nothing. The released images are sufficient to solve every row. External identity recovery and source lookup are prohibited under the from-scratch rule above, and they are checkable: any read outside the released dataset directory, any bundled or downloaded model, and any network call is a violation by definition. Dataset The prepared public data contains: train.csv — labelled training rows; test.csv — unlabelled test rows; sample_submission.csv — submission template; task_manifest.json — public dimensions and scoring constants; and images/ — one composite and one inventory PNG for every train and test row. No released image path is reused by another row. train.csv id — type: string; opaque unique row identifier. composite_file — type: string; relative path to the row's composite PNG. inventory_file — type: string; relative path to the row's inventory PNG. piece_count — type: integer; the number of non-blank inventory pieces, from 3 through 8. target_sequence — type: string; the gold placement and precedence program, in the grammar given under Submission Format. test.csv test.csv contains the same id, composite_file, inventory_file and piece_count columns. It does not contain target_sequence, and no answer or label file for the test rows exists anywhere the script can reach. sample_submission.csv id — type: string; one required test identifier per row. target_sequence — type: string; a syntax-valid, placement-only placeholder that puts every piece at the same fixed box. It demonstrates the required grammar and CSV quoting and is not intended as a useful prediction. task_manifest.json title — type: string; stable task identifier. task_domain and task_form — type: string; the domain and the shape of the required output. split — type: object; row counts and the zero-source-family-overlap guarantee. images — type: object; format, mode and dimensions of both views. piece_ids — type: string; the row-major inventory ordering rule. sequence_grammar — type: object; separator, group forms, coordinate limits and graph constraints. metric — type: object; the exact row and aggregation constants used by the grader. Its values match grade.py. Submission Format Submit one CSV with exactly these columns in this order: id — type: string; a test identifier copied without modification, each appearing exactly once. target_sequence — type: string; the complete placement groups followed by any predicted edge groups. A placement group maps a piece's three canonical anchors into composite-image coordinates and is written as Pii x_tl y_tl x_tr y_tr x_bl y_bl. The anchors are the top-left, top-right and bottom-left corners of the tight axis-aligned bounding box of that piece's stroke centreline, taken before line-width dilation and antialiasing. For example, P02 41 73 98 66 48 129 places piece p02 with transformed anchors (41,73), (98,66) and (48,129). Coordinates are integer pixels from -32 through 287; an anchor may fall slightly outside the visible stroke even though the composite canvas is 256 by 256. An edge group is written as Ebb aa and means that piece paa is visually above piece pbb at their overlap. For every row: include exactly one placement group for every piece from p00 through p(piece_count - 1); include zero or more edge groups; separate groups with a vertical bar, with optional surrounding spaces; use two decimal digits in every piece token; keep every coordinate within -32 through 287; and include at most piece_count + Cpiece_count, 2) groups in total. The predicted edge graph must be acyclic. Do not submit self-edges, duplicate edges, contradictory directions, or more than one direction for an unordered pair. Groups may appear in any order. A syntactically invalid row scores zero and leaves every other row unaffected. Missing, duplicate or null identifiers reject the submission, as do extra, missing or reordered columns. Rows whose identifier is not being graded are ignored rather than rejected. If an edge estimate is uncertain, omitting that edge is valid. Never omit a placement group: start from the placement-only structure in sample_submission.csv and replace coordinates as estimates become available, which keeps a partial solver syntactically valid throughout. A concrete one-row CSV example is shown below without a fenced code block. The identifier is illustrative and is not a release row. Header: id,target_sequence First row: i0123456789abc,"P00 25 42 77 38 29 91 | P01 103 66 154 72 96 118 | P02 62 121 111 109 74 173 | E00 02 | E01 02" A Practical Starting Point A stable solver can be built without any semantic recognition, in six stages: Split the inventory into its 64-by-64 cells and extract one soft stroke mask per piece. Estimate the composite background and construct colour-insensitive stroke and edge maps. Match each inventory mask to the composite with a coarse-to-fine affine search. Use the shared episode orientation and shear as a joint constraint, and enforce one-to-one piece assignments. Map the three inventory bounding-box anchors through the selected affine transform. For every pair whose transformed masks overlap, inspect the local visible colour and the continuity on both sides of the crossing to decide which piece is above. Remove the lowest-confidence edge from any predicted cycle before serialization. Shape correspondence and joint geometry are worth solving before any learned model is introduced. A category classifier is not useful for this target and sits outside the intended solution path. Research Context Prior work on drawing reconstruction usually estimates stroke order or animation from a single final raster; the closest methodological neighbour is Fu and colleagues, Animated Construction of Line Drawings, SIGGRAPH Asia 2011, which infers a plausible drawing sequence from static line art. This challenge instead supplies an unordered inventory of the actual candidate pieces and asks for a different structured object: per-piece affine anchor placement together with an explicit acyclic overlap graph. The family-disjoint split, the candidate-conditioned correspondence, the joint geometric and precedence output, and the balance-aware metric make this an inverse assembly problem rather than single-image stroke-order reconstruction. Compute Environment Submitted solutions run on GPU and no network access are available. Training, inference and serialization must all fit within those limits. Expected Output Your script receives the public dataset directory and the exact submission CSV path as two positional arguments. It may read only the files listed under Dataset above, all of which live inside that directory. It must write only the submission CSV at the given path, and must not depend on any file left behind by an earlier run. &nbsp;
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Jupiter Diagnostic-Band Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72rc2z52tdanby2a2cd4cfyx8dsgsf
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat konda's score of 0.715!

Full challenge description from page:

> Jupiter Diagnostic-Band Reconstruction Overview Jupiter looks different at different wavelengths because its clouds and hazes sit at different altitudes and absorb light differently. Hubble's Outer Planet Atmospheres Legacy (OPAL) program publishes aligned global maps through several filters each year. For every sample, you receive a 64 by 64 visible-band image. Predict two coarse diagnostic maps for the same location: ultraviolet F275W and methane-absorption FQ889N. A useful solution must infer atmospheric structure that ordinary visible color does not directly reveal and generalize to later Hubble observing cycles. Research gap and benchmark position Generic missing-band reconstruction is established in Earth remote sensing. For example, Neagoe et al. (2023) use a modified U-Net to reconstruct missing Sentinel-2 bands. This challenge changes the scientific target and the generalization regime: it reconstructs two physically selected Jovian diagnostic bands from annual Hubble maps and holds out entire future observing cycles. The OPAL archive describes yearly global maps in a wide range of filters. F275W is used as a proxy for high-altitude haze, while FQ889N probes high clouds through methane absorption. The exact challenge contract—a paired 8 by 8 ultraviolet/methane grid, visible-only 64 by 64 input, cycle-level temporal holdout, opaque crops and one bounded metric—is not an existing OPAL science product or a standard remote-sensing benchmark. Data All solver-visible files are under ./dataset/public/. images/ contains 3,840 lossless 64 by 64 RGB WebP inputs. train.csv contains 2,304 labeled patches from HST Cycles 23, 25 and 28. test.csv contains 1,536 unlabeled patches from Cycles 31 and 32. sample_submission.csv contains a valid zero baseline. The RGB channels are not ordinary display color. They encode F631N, F502N and F395N, in that order. Pixel values were scaled with fixed training-only robust limits. Images, source maps and observing cycles never cross the temporal split. Targets Each diagnostic target is reduced from 64 by 64 to an 8 by 8 block-mean grid, standardized using training-cycle statistics, and clipped to [-8, 8]. There are 128 prediction columns: f275w_r0_c0 through f275w_r7_c7; fq889n_r0_c0 through fq889n_r7_c7. Rows and columns are zero-based and follow the top-to-bottom, left-to-right orientation of the input image. The sample submission supplies every exact column name and should be used as the schema authority. Submission Write ./working/submission.csv. It must contain sample_id followed by all 128 target columns. Include every test identifier exactly once. Row order does not matter. Every prediction must be finite and lie in [-12, 12]. Missing, duplicate, extra or malformed identifiers and columns fail closed to a score of 0. Evaluation The grader aligns rows by sample_id, then computes one root mean squared error over all 128 standardized target values and every test sample. RMSE = sqrt(mean((prediction - target)^2)) score = exp(-RMSE) Scores lie in (0, 1], and higher is better. An exact reconstruction scores 1.0. A prediction with RMSE 1 scores approximately 0.367879. The supplied sample submission predicts the training mean, which is zero after standardization and scores 0.380768 on the frozen test set. A deterministic spatial ridge baseline using pooled 8 by 8 visible-band features scores 0.499775. This leaves substantial headroom for models that learn spatial and cross-spectral structure. Modeling guidance A per-pixel spectral regression is a reasonable baseline, but it cannot fully use bands, belts, vortices and haze structures around each location. Competitive approaches can fine-tune a compact convolutional network, vision transformer or encoder-decoder that consumes the full visible patch and predicts both 8 by 8 diagnostic grids jointly. Runtime Compute: one NVIDIA A10G GPU. Time limit: 90 minutes. Network access: disabled. External data lookup is prohibited. Pretrained components may be used only when already available in the execution environment; no weights or data may be downloaded during a run. The dataset is an offline research benchmark and is not a navigation, operational or scientific-calibration product. Source-quality revision Before any scaling, each FITS map is converted to I/F using its official cycle/filter README multiplier. Only first rotations from Cycles 23, 25, 28, 31 and 32 are retained. Other downloaded first rotations are excluded for documented satellite/shadow replacement, transits or incomplete coverage. Every 64x64 patch is entirely within map rows [320,1472) and contains only positive finite pixels in all five filters. This fixed central-band restriction excludes polar boundary regions independently of target magnitude. Visible-image quantiles use stride-16 positive finite pixels across the central band of training cycles; target means and standard deviations use only the selected training patches. Both are fitted after I/F conversion without test cycles. Residual fringes, interpolated mosaic seams and non-simultaneous filter observations remain source limitations; this is not an artifact-free scientific retrieval product.
> $700 Pool
> Closes in 1h 24m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Single-Image Spatial Reasoning

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx722hys7ehpnqf11jqhnpm8eh8dt14z
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat hoang_phuc_6868's score of 0.685!

Full challenge description from page:

> Single-Image Spatial Reasoning Overview Given a single photograph of an indoor scene and a natural-language question about the scene's physical geometry, predict a calibrated probability distribution over ordinal magnitude bins for the answer. The questions ask for physical quantities that are not written anywhere in the image and cannot be read off a label — how many instances of an object are present, how far apart two objects are, and how large an object is. Answering requires recovering approximate scene geometry (relative depth, scale, and layout) from a single 2-D view, then expressing the answer as a magnitude on an ordinal scale. The corpus is a collection of everyday indoor rooms — homes and workplaces — photographed from a single viewpoint each, with wide variation in furniture, clutter, lighting, and camera pose. Because a single view is inherently ambiguous about absolute scale, a well-performing model must express uncertainty: rather than committing to one bin, it distributes probability mass across neighbouring magnitude bins in proportion to its confidence. The scoring rewards mass placed on or near the correct bin and penalizes confident mass placed far from it, so both the point estimate and its calibration matter. The task is hard for three reasons: (1) monocular scale is under-determined, so metric quantities (distance and object size) must be inferred from learned priors over indoor scenes; (2) the three question types span very different magnitude ranges and difficulties, and the headline score weights each type equally, so a model cannot coast on the easiest type; and (3) confident errors are punished, so a model that is accurate but poorly calibrated loses to one that is slightly less accurate but honest about its uncertainty. Dataset Public files public/train.csv — one row per training query. Columns: id, image, question, question_type, prob_bin_1, prob_bin_2, prob_bin_3, prob_bin_4, prob_bin_5, prob_bin_6, prob_bin_7, prob_bin_8. public/test.csv — one row per test query. Columns: id, image, question, question_type (the eight prob_bin_* target columns are withheld). public/images/ — the scene photographs referenced by the image column, one JPEG per file, named with opaque tokens (e.g. images/img_9f3a2c1b7e0d4a56.jpg). Several queries may reference the same image. public/sample_submission.csv — a valid submission in the required format. Columns: id, prob_bin_1 … prob_bin_8. Private file (organizer only) private/answers.csv — the ground-truth answer for every test query, stored in the same columns as sample_submission.csv (id, prob_bin_1 … prob_bin_8) as a one-hot distribution on the correct bin. Column descriptions The public CSVs use the following columns: id (string) — unique query identifier. The id encodes the question type as its second token (q__, where ` is one of count, dist, size), e.g. q_dist_000123`. image (string) — relative path to the scene photograph for this query (e.g. images/img_9f3a2c1b7e0d4a56.jpg). question (string) — the natural-language question about the scene (e.g. "How far apart are the sofa and the television?"). question_type (string) — the spatial task family, one of: count (number of instances of a named object), dist (straight-line distance between two named objects), size (longest dimension of a named object). Each family's raw magnitude is discretized into ordinal octile bins, so the physical unit does not affect the task. prob_bin_1 … prob_bin_8 (float) — the predicted probability that the answer falls in ordinal bin 1 through 8. In train.csv and private/answers.csv these hold the ground-truth one-hot distribution (1.0 on the correct bin, 0.0 elsewhere); in a submission they hold the predicted distribution, which must be non-negative and sum to 1. Ordinal bins. For each question type the magnitude is discretized into 8 equal-frequency ordinal bins (octiles): bin 1 holds the smallest magnitudes for that type and bin 8 the largest, with each bin containing roughly one eighth of that type's answers. The bins are latent ordinal classes — you learn the mapping from image to bin directly from the training labels (each train.csv row's one-hot prob_bin_* marks its true bin), so no numeric bin boundaries are needed to make a prediction. Equal-frequency binning means the prior over bins is roughly flat within each type, so guessing the most common bin scores no better than chance. Data example A truncated train.csv row (target columns shown in full): id,image,question,question_type,prob_bin_1,prob_bin_2,prob_bin_3,prob_bin_4,prob_bin_5,prob_bin_6,prob_bin_7,prob_bin_8 q_size_000042,images/img_9f3a2c1b7e0d4a56.jpg,"What is the longest dimension of the dining table?",size,0,0,0,0,1,0,0,0 Split and anti-memorization The train and test splits are disjoint at the scene level: every photograph appears in exactly one split, so no test image (and none of its queries) is ever seen during training. The split is produced by a data-derived, reproducible partition of the scene collection, grouping all queries of a scene together before assignment. Because absolute scale cannot be memorized from the training answers and must be inferred from each unseen room's appearance, a model cannot win by lookup — it must generalize scene-geometry priors to new rooms. Image files carry no location metadata, and identifiers are opaque tokens unrelated to any source ordering. Submission format Submit a CSV with exactly these columns and exactly one row per test id: id,prob_bin_1,prob_bin_2,prob_bin_3,prob_bin_4,prob_bin_5,prob_bin_6,prob_bin_7,prob_bin_8 Every test id in test.csv must appear exactly once; unknown or missing ids are rejected. The eight prob_bin_ values in each row must be *non-negative* and *sum to 1.0** (a tolerance of 0.02 is allowed, after which values are renormalized). No extra columns are permitted. Sample submission (a uniform distribution on every row): id,prob_bin_1,prob_bin_2,prob_bin_3,prob_bin_4,prob_bin_5,prob_bin_6,prob_bin_7,prob_bin_8 q_count_000001,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125 q_dist_000001,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125 q_size_000001,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125 Evaluation The headline metric is the Ordinal Calibration Score (OCS) — a per-type mean of a distance-weighted credit minus a far-miss penalty, then macro-averaged with equal weight across the three question types. Higher is better. For each query, let b be the true bin (1–8) and p[1..8] the submitted distribution (renormalized to sum to 1). Define a fixed near-bin credit by ordinal distance d = |k − b|: CREDIT = {0: 1.0, 1: 0.4, 2: 0.1} # credit for mass at ordinal distance d; 0 for d >= 3 FAR = 3 # a "far miss" is mass placed 3+ bins from the truth BETA = 0.5 # weight of the far-miss penalty def query_score(p, b): credit = sum(p[k] * CREDIT.get(abs(k - b), 0.0) for k in range(1, 9)) penalty = sum(p[k] for k in range(1, 9) if abs(k - b) >= FAR) return credit - BETA * penalty # in [-BETA, 1.0]; negative for confident far misses def ocs(all_scores_by_type): mean within each of the 3 types, then equal-weight macro-average across types per_type = {t: mean(scores) for t, scores in all_scores_by_type.items()} score = mean(per_type[t] for t in ("count", "dist", "size")) return max(0.02, score) # small positive floor Scoring notes (all reflected in eval.py): Distance-weighted credit. Probability mass on the exact bin earns full credit (1.0), mass one bin away earns 0.4, two bins away earns 0.1, and three or more bins away earns nothing. This rewards a calibrated distribution centred on or near the truth. Far-miss penalty. Mass placed 3 or more bins from the truth is additionally penalized at weight BETA = 0.5, so a confidently wrong prediction scores below an uncertain one. A single query's score can therefore be negative (as low as −0.5); the metric is not bounded below by 0. Equal-weight macro-average over the three question types. Each of count, dist, size contributes exactly one third of the headline score, so a model cannot inflate its score by mastering only the easiest type. The type of each query is recovered from its id. Score floor. The final macro-average is clamped up to a small positive floor of 0.02 so a valid submission never returns exactly 0. Baseline. A uniform distribution (0.125 on every bin — the sample submission) is the chance baseline: after the far-miss penalty it earns essentially no net credit and grades at the small score floor (≈0.02). Any content-free strategy (guessing the most common bin, using row position, or a constant bin) scores at this same chance level. A perfect one-hot submission on every query scores 1.0. Higher is better. What Not To Use (Prohibited Methods) This challenge measures whether a model can infer physical scene geometry from a single image. The following are prohibited: No external answer keys or metadata. Do not use any external precomputed depth maps, 3-D reconstructions, camera-pose files, object dimensions, room-dimension tables, or spatial annotations to recover test answers. The answers must come from your model's inference on the provided images alone. No matching images back to a source. Do not attempt to identify the original scenes, rooms, buildings, or capture sessions behind the test photographs, and do not match test images (by pixel content, near-duplicate search, reverse image search, or embedded data) to any external dataset, video, floor-plan, or 3-D scan in order to look up true distances, sizes, counts, or areas. No id- or filename-based hardcoding. Do not build lookup tables from id, image filename, or row order to test answers. Identifiers are opaque and carry no answer information. No manual labelling of the test set. Do not hand-estimate distances, sizes, or counts for test images, whether by a person or by an external service. No train/test leakage. Do not use test images or their queries during training or model selection beyond producing the submitted predictions. No private-label tuning. Do not attempt to infer, reconstruct, or fit to the private ground-truth bins. &nbsp;
> $700 Pool
> Closes in 2h 15m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Anonymous Sensor Cohort Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ev4paycfsdq2tpxtdk3jp8h8drs4n
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat developerg's score of 0.464!

Full challenge description from page:

> Overview Recover three unknown camera cohorts from eight residual tiles. For each case, predict the cohort partition, the five strongest within-cohort links, and one representative tile for every cohort. The setting is source-forensics before device identities are known. An evidence packet may contain residual summaries from several acquisition pipelines after EXIF, filenames, and photographed content have been removed. The useful signal is not the visible scene. It is the aggregate pattern left by demosaicing, sensor noise, sharpening, channel coupling, and compression. There are always three local cohorts with sizes 3, 3, and 2. Their identities disappear after every row, so this is not six-class phone recognition. A model must learn whether two tiles share a sensor process, then express that relation as a partition, an affinity forest, and a medoid certificate. What A Board Contains Every 944 by 500 JPEG board has eight labeled tiles, A through H. One tile is a signed residual composite built from six real photographs taken by the same camera. Each constituent photograph is orientation-corrected, centrally resampled, and converted once into a channelwise high-pass log-amplitude spectrum. For every composite, the six cached spectra receive independent smooth frequency tilts and channel gains before averaging, then are reconstructed with case-random phase. This retains recurring acquisition-pipeline statistics while removing scene identity and direct pixel correspondence to any one source photograph. Spectral perturbations, reconstruction phase, tile location, and letter assignment are sampled independently of cohort membership. Source filenames, device names, EXIF fields, timestamps, and constituent lists are absent from the public release. Dataset | Path | Contents | |---|---| | train.csv | 1,600 labeled residual-cohort boards. | | test.csv | 400 hidden boards. | | sample_submission.csv | Schema-valid baseline predictions. | | images/ | The 2,000 distinct JPEG boards referenced by the CSV files. | Columns | Column | Data type | Train | Test | Description | |---|---|---:|---:|---| | case_id | string | yes | yes | Opaque identifier used only for alignment. | | cohort_board_path | relative path string | yes | yes | Path to the eight-tile residual board. | | sensor_partition | canonical partition string | yes | no | Three same-camera groups. | | residual_affinity_forest | canonical undirected edge set | yes | no | Five minimum-distance links inside the groups. | | representative_tile_set | canonical label set | yes | no | One residual medoid per group. | Exact duplicate source payloads are collapsed before construction. Remaining captures are grouped into device-independent one-hour acquisition blocks. Every source block belongs entirely to training or test across all cameras observed in that hour, preventing duplicate or nearby scene sessions from crossing the boundary. Each composite tile uses six photographs selected only from its split-local capture pool. Local group labels and board positions are randomized, so a global device label cannot be copied into the required partition. The same six device groups occur on both sides: the transfer claim concerns held-out capture blocks, not unseen camera hardware. Adjacent hours can still contain similar scenes, and reused within-split photographs make the 2,000 boards correlated. The split blocks direct source reuse; it does not guarantee that all scene resemblance disappears. The training set contains 278 distinct partitions and 1,165 distinct forests. Each board has exactly five forest edges and three representatives, and every panel letter becomes a representative in hundreds of cases. The Cohort Certificate Partition Sort letters within each group, then order groups by their first letter. Every letter A-H appears once and group sizes must be 2, 3, and 3. ACF|BDH|EG Affinity Forest A residual descriptor measures blockwise high-pass energy and cross-channel differences after reconstruction. Euclidean descriptor distance defines edge cost. The hidden certificate uses the minimum spanning tree inside each true group: one edge for the two-item group and two edges for each three-item group. Write each undirected edge with its smaller letter first and sort the five edges lexicographically. A-C|A-F|B-D|D-H|E-G Representatives Within each group, select the tile with the smallest summed descriptor distance to the other members. Panel letter resolves an exact tie. Sort the three selected labels. A|D|E The partition, forest, and representative fields are limited to 14, 40, and 8 characters respectively. Submission Format Write ./working/submission.csv with exactly these columns in order: case_id sensor_partition residual_affinity_forest representative_tile_set | case_id | sensor_partition | residual_affinity_forest | representative_tile_set | |---|---|---|---| | sc_370f68794d4920f44831 | ACF\|BDH\|EG | A-C\|A-F\|B-D\|D-H\|E-G | A\|D\|E | The row is a format example, not a disclosed answer. Every hidden ID must occur exactly once. Extra or reordered columns, missing or unknown IDs, duplicate rows, repeated letters, invalid group sizes, and malformed edges are rejected or score zero as specified. Evaluation The metric is the Anonymous Cohort Certificate Score: Score = 0.55 * PartitionScore + 0.25 * ForestScore + 0.20 * RepresentativeScore Minimum score: 0.0. Maximum score: 1.0. Higher is better. Exact answers score 1.0. PartitionScore A partition induces a set of same-group letter pairs. For true pair set T and predicted pair set P: pair_F1 = 2 * |T intersection P| / (|T| + |P|) The row score is 0.75 * pair_F1 + 0.25 * exact_partition_match, averaged over hidden cases. ForestScore Set F1 is computed over the five submitted edges. The base row score is: 0.70 * edge_F1 + 0.30 * exact_forest_match The edges must form one connected tree inside every submitted partition group, with no edge between groups, and the submitted representative set must contain exactly one member of every group. A row satisfying all three conditions keeps its base score; otherwise the row receives 0.20 times the base score. This check uses all three submitted fields and does not require that they match the hidden answer. RepresentativeScore The base row score is 0.60 * set_F1 + 0.40 * exact_set_match. Exactly one representative must belong to each submitted group, and the submitted forest must satisfy its coherence rule. A coherent row keeps the base score; otherwise it receives 0.20 times the base score. If one F1 set is empty and the other is not, F1 is zero. Invalid or overlong values score zero for the affected component. Hidden answers are never clipped or repaired. Why Local Cohorts Change The Problem A global classifier can memorize a stable device label. This task deliberately removes that label and asks for an equivalence relation inside each packet. It then tests whether the learned residual geometry is internally meaningful: the forest must connect nearest evidence, and the representatives must act as cohort medoids. A partition guessed from scene content cannot satisfy those additional certificates reliably. Modeling Approaches Participants may fine-tune high-resolution residual encoders, camera-fingerprint networks, metric-learning models, or pairwise affinity systems. A practical pipeline predicts an eight-by-eight relation matrix and then decodes the constrained partition, minimum spanning trees, and medoids. What Not To Use Do not use case_id, board filenames, panel position, row order, hidden EXIF, source directories, or online lookup tables as prediction signals. Each tile is a new six-capture spectral composite, not an encoded copy of one public photograph.
> $700 Pool
> Closes in 40m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Handwritten Molecule Fragment Reassembly

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cjf0etgbmej5c4y9gs2m8as8dty9v
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat arin's score of 0.850!

Full challenge description from page:

> Overview Resolve structural ambiguity from a handwritten molecular diagram. Given three or four graph fragments with fixed atoms and internal bonds, predict the missing connections as atom-index pairs and bond types. Preserve the supplied graph and add exactly the declared number of bonds. Attachment sites and image coordinates are unknown. Different assemblies can satisfy the packet, so use the drawing to resolve branches, repeated motifs and ring closures. The task models completing a partial digital structure from its original sketch; submit the missing bonds alongside the unchanged packet. Dataset Each example supplies two complementary inputs: a 384 × 384 grayscale PNG and a packet describing the disconnected graph pieces. The release has 3,001 training examples and 831 test examples, with a distinct drawing for each example. Complete structures contain 6–73 non-hydrogen atoms; each packet has three or four fragments with 2–8 bonds left to recover. A structurally different completion consistent with the packet has been verified for every example. The packet is therefore insufficient to uniquely specify the answer, although alternative completions need not be equally plausible. | File | Rows | Columns / contents | |---|---:|---| | train.csv | 3,001 | task_id, image_path, packet_json | | train_labels.csv | 3,001 | task_id, target_json | | test.csv | 831 | task_id, image_path, packet_json | | sample_submission.csv | 831 | task_id, target_json | | images/train/ | 3,001 images | Training drawings referenced by train.csv. | | images/test/ | 831 images | Test drawings referenced by test.csv. | task_id is an opaque string. image_path is relative to the supplied data directory. packet_json and target_json are JSON encoded inside quoted UTF-8 CSV fields. Join features and labels by task_id, never by row position. Structural groups are disjoint between train and test: ring-scaffold families stay together, while acyclic molecules sharing an unlabeled branching topology stay together. Constitutional duplicates are also grouped. There are 1,917 training groups and 528 test groups. Use structure-group-aware validation when selecting models; random row validation may overestimate transfer to unfamiliar structures. Handwriting quality varies and some drawings are faint or dense. Labels follow the supplied atom, aromaticity and bond conventions rather than every visual drawing convention. Stereochemistry and hydrogen counts are outside the output contract. The collection is finite and contains uncommon chemical structures, so performance need not generalize to all diagram sources. Packet schema The object has exactly four keys: { "atoms": [[7,0,0,1],[7,0,0,1],[6,0,0,1],[16,0,0,1],[7,0,0,0],[6,0,0,1]], "bonds": [[0,2,4],[1,3,4],[4,5,1]], "fragments": [[0,2],[1,3],[4,5]], "missing_bond_count": 3 } atoms: one [atomic_number, formal_charge, isotope, aromatic] list per atom. Atom indices are zero-based positions in this list and have no image-coordinate or source-order meaning. Allowed atomic numbers are 5,6,7,8,9,14,15,16,17,32,33,34,35,50,51,52,53. Charge is an integer from −3 to +3; isotope is an integer from 0 to 300, with 0 meaning unspecified; aromatic is 0 or 1. The schema permits 6–96 atoms; this release contains at most 73. bonds: retained edges [a,b,bond_type]. Indices satisfy 0 <= a < b < number_of_atoms. Types are 1 single, 2 double, 3 triple and 4 aromatic. All supplied edges lie inside one fragment. Type 4 does not mean bond order four. The schema permits 3–192 retained edges. fragments: three or four disjoint lists covering all atom indices exactly once. Each has at least two atoms and is connected by the retained bonds. Partly cut aromatic rings are allowed; fragments are graph components, not necessarily standalone valid molecules. missing_bond_count: exact number of edges to predict. The schema permits number_of_fragments - 1 through 12; this release contains 2–8. Explicit/implicit hydrogen counts and stereochemical descriptors are not supplied or scored. Atomic number, formal charge, isotope, aromatic flag and categorical bond type are preserved in evaluation. Submission Submit the proposed connections for every test drawing in one UTF-8 CSV. Match the column names and order in sample_submission.csv exactly: task_id,target_json Include every test ID exactly once. Each target_json value is an object with exactly two keys: packet: copy the corresponding public packet_json object unchanged. This is context, not an additional prediction. JSON whitespace and object-key order may differ; array contents and order must remain unchanged. missing_bonds: exactly missing_bond_count triples [a,b,bond_type]. Each must join different supplied fragments, have a < b, and use a permitted bond type. Edge-list order does not matter. Duplicate atom pairs, self-loops, retained-edge replacements and disconnected completed graphs are invalid. All numeric fields must be JSON integers, not booleans or floating-point values. No extra or duplicate JSON keys are permitted. The maximum target_json length is 50,000 characters. Two actual training-label examples illustrate the CSV format; use the test IDs and test packets for your submission: task_id,target_json frag_00126a0045e1be86d47cf8ec,"{""packet"":{""atoms"":[[7,0,0,1],[7,0,0,1],[6,0,0,1],[16,0,0,1],[7,0,0,0],[6,0,0,1]],""bonds"":[[0,2,4],[1,3,4],[4,5,1]],""fragments"":[[0,2],[1,3],[4,5]],""missing_bond_count"":3},""missing_bonds"":[[0,3,4],[1,5,4],[2,5,4]]}" frag_0f66bb7765c51f71b29d5666,"{""packet"":{""atoms"":[[33,0,0,0],[7,0,0,0],[16,0,0,0],[6,0,0,0],[7,0,0,0],[16,0,0,0]],""bonds"":[[0,5,1],[1,4,1],[2,3,1]],""fragments"":[[0,5],[1,4],[2,3]],""missing_bond_count"":4},""missing_bonds"":[[0,1,1],[0,2,1],[1,3,1],[3,5,1]]}" Evaluation Performance is measured by exact labeled-graph reconstruction accuracy on a 0-to-1 scale; higher is better. The evaluator joins your proposed bonds to the supplied bonds and compares the resulting structure with the reference. An example earns 1 only when the two completed graphs are isomorphic: a one-to-one atom mapping must preserve every supplied atom label and bond type. Otherwise it earns 0. Symmetry-equivalent attachments are accepted; a different connectivity is not. Arbitrary atom numbering and fragment identifiers do not determine structural identity, although your copied input packet must remain unchanged. row_score = 1 if the completed labeled graphs are equivalent, otherwise 0 score = sum(row_score for every evaluated example) / number_of_evaluated_examples The final score is the fraction of examples whose connectivity is fully recovered. This measures whether the completed record represents the right structure: even one misplaced bond can change it. Already supplied bonds earn no separate credit, and incomplete reconstructions earn no partial credit. A random submission can legitimately score zero. Malformed row JSON, an altered packet or an invalid assembly scores zero for that row without invalidating otherwise valid rows. Incorrect CSV headers, duplicate/missing/extra IDs, an empty file or a broken table structure cause a file-level error. Rows are aligned by ID, so reordering them does not affect the score. Chemical toolkit sanitization is not an extra scoring criterion; labeled connectivity under the supplied convention is the criterion. Allowed Methods and What Not To Use Generic pretrained vision models may be used and fine-tuned on the supplied training data. GPU use is allowed. Do not use challenge-specific molecular-recognition or OCSR pretrained checkpoints, external labeled molecular-image corpora, original-source copies, reverse image search, held-out-source matching, web lookup, manual test annotation, hard-coded test answers or hosted APIs. &nbsp;
> $700 Pool
> Closes in 2h 1m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Nuclear Partition Inference from Sparse Feedback

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72mkc0bn1cgb4p5cazvdst0x8dyt9y
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat 15_luz's score of 0.681!

Full challenge description from page:

> Background Infer a spatial grouping preference from sparse ownership feedback and use it to partition a nuclear image. This benchmark combines visual instance recovery with inverse calibration of a capacity-constrained graph objective. The grouping preferences, capacities and cost fields are synthetic mathematical interventions, not measured biological effects. Overview Each row supplies one perturbed 48×48 grayscale microscopy image, two ordered seed pixels, an exact 48×48 cost map, an integer quota and calibration demonstrations. Recover eligible nuclear instances and return two ordered territory masks. Territory 0 contains exactly quota whole instances including the first seed; territory 1 contains every other eligible instance including the second seed. Eligible instances contain 8–600 pixels. Each image contains 5–16 eligible instances; quotas range from 2 through n−2. Each image has exactly one released query. Calibration supplies at most three ownership bits, all referring to the same single non-seed probe location. It never enumerates the other nuclei. Recovering full instance boundaries and the unobserved instances from the image is essential: representative coordinates alone do not determine pixel-to-pixel graph gaps or territory masks. Dataset Information (Public Files) images/ Perturbed 48×48 grayscale PNGs costs/ Exact 48×48 cost PNGs, values 0–64 train.csv Training queries and masks train_instances.csv Training-only id,instances index train_instances/ Training-only canonical instance-label NPY arrays test.csv Evaluation inputs without masks sample_submission.csv id,masks formatting example territory_contract.py Exact geometry and optimization reference Audit files, preparation statistics, hidden preferences and hidden instance annotations are private. There is no public protocol.json. The exact reference routine contains the mathematical task definition; it does not contain evaluation geometry or answers. Feature Schema id Opaque query identifier image Relative path to one 48×48 grayscale image seeds JSON: two ordered integer [x,y] pixels cost_image Relative path to the query cost PNG quota Exact number of instances assigned to territory 0 calibration JSON list of demonstration objects masks Training only: two ordered RLE masks Each calibration object has cost_image, quota and probes. probes contains exactly one [x,y,owner] triple. All demonstrations in a row use the same probe pixel, chosen once from the non-seed instances. owner is 0 or 1 under that demonstration's optimum. This intentionally supplies one foreground location and sparse ownership feedback, not a list of object locations. Demonstrations share the row's image, seeds and hidden preference, but do not duplicate its query cost/quota. Read their cost PNGs into a cost key when using the reference helper. Target JSON Schema Submit masks as [first_runs,second_runs]. Each run is [start,length] on the row-major 48×48 grid, index=48*y+x. Starts are integers 0–2303; lengths are positive integers and start+length must not exceed 2304. Runs must be sorted, non-overlapping and non-adjacent. Each mask has at most 1,152 runs. Empty lists are permitted. Preserve seed order. Geometry: Each eligible instance is one node. Its representative is the instance pixel nearest its arithmetic centroid, with row-major tie breaking. Order nodes by representative y, then x, then first row-major instance pixel. Integer annotation IDs carry no geometric meaning. Let g(i,j) be the minimum squared Euclidean distance between pixels of two instances. Between representatives, sample n+1 equally spaced points where n is the maximum absolute x/y displacement. Round exact halves upward, include endpoints and count distinct pixels once. Let c(i,j) be the sum of costs along these points. Define w(i,j)=floor(4096/(1+g(i,j)+c(i,j))). Assignment: Territory 0 includes the first seed and exactly quota instances; territory 1 includes the second seed and all remaining instances. Minimize the sum of g(i,assigned_seed) over nodes plus lambda*w(i,j) over unordered pairs assigned to different territories. Break equal-energy ties by the lexicographically smallest sorted tuple of canonical node indices in territory 0. Return unions of complete instance masks; all other pixels are background. Inverse calibration: lambda belongs to {1,2,4,8}; training uses {1,4} and evaluation uses {2,8}. The row's value is hidden. For recovered geometry, enumerate all four candidates and retain those matching every calibration ownership bit. The resulting set S must be nonempty. Preparation only retains cases where candidates in S agree on the requested answer. This ensures a well-defined prediction conditional on the image and supplied feedback. It does not make the answer known without recovering the image's instance geometry. During preparation, two adjacent-capacity optima are examined privately. Candidate preferences must disagree on at least one of these optima, and increasing capacity must cause at least one instance to leave territory 0 while others enter. One query is selected randomly for release; its counterfactual counterpart is not released. This selection tests nontrivial grouping while preventing paired-row consistency from supplying an additional evaluation constraint. The public reference is permitted after learned instance recovery; a rules-only metadata solver is not a compliant visual solution. Input Perturbations All corruption acts directly on the 48×48 observation: seeded gain 0.7–1.3, offset −25 to 25, one or two directional smearing passes with mixing 0.15–0.35, three to seven bright/dark rectangular distractors, Gaussian noise with standard deviation 15–30, rounding and clipping to 0–255. Masks are unchanged. The PNG is stored at its native task resolution, without an 8× enlargement. There is no block-averaging route to an uncorrupted observation. Cost images are exact mathematical inputs and are not corrupted. Generalization & Leakage Controls Complete parent images remain in one split before crop generation. A fixed held-out group plus 60% (rounded upward, with a minimum of five) of the remaining parent images form evaluation; the others provide training. The additional images are selected by sorting deterministic opaque hashes before any label-based crop eligibility checks. Exact full-image duplicates cannot cross the split. Patient and slide identities are unavailable, so no patient-level independence is claimed. Accepted evaluation crops from the same parent image are spatially disjoint. A crop is released only once, with one query and one fixed non-seed probe coordinate across its demonstrations. Training may contain overlapping crops within training images. No training instance labels are supplied for evaluation images. Preparation audits unique image references, the probe limit and the exact public-file allowlist. Counts, crop mappings, grouping records and hidden preferences stay private. Evaluation Metrics For each ordered territory, Dice D_i=2|P_i intersect T_i|/max(1,|P_i|+|T_i|). Let O=|P_0 intersect P_1|/max(1,|P_0 union P_1|). The row score is sqrt(D_0D_1)(1−O). The final score is the arithmetic mean over evaluation rows, between 0 and 1; higher is better. Territory order matters. Sample Submission Format Submit a UTF-8 CSV with exactly id,masks in this order and every evaluation ID exactly once. Quote JSON cells. id,masks example_id,"[[[100,3],[148,3]],[[900,4],[948,4]]]" Wrong columns, broken CSV structure, missing/extra or duplicate IDs invalidate the file with score zero. A malformed mask cell scores zero for that row. JSON is limited to 30,000 characters. Booleans, noninteger runs, invalid bounds, overlapping or adjacent runs and wrong numbers of masks are rejected. Row order does not affect grading. What Not To Use Use only the provided training data. Fine-tune a general-purpose pretrained visual component on the training examples within the configured offline runtime. Cache permitted weights beforehand. No external datasets, internet access, hosted inference, manual evaluation labels, hard-coded ID answers or challenge-specific pretrained checkpoints. Do not fit on evaluation images or aggregate calibration across evaluation rows. Deterministic geometry and optimization postprocessing is permitted after learned instance recovery.
> $700 Pool
> 3 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## AgNP-Vision: Open-Set Synthesis Recipe Ranking from Electron Micrographs

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx739hpj00h2byxc2jkjsay1p18e1mjf
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat shikum's score of 0.458!

Full challenge description from page:

> AgNP-Vision: Synthesis Recipe Ranking from Electron Micrographs Overview Silver nanoparticles (AgNPs) are synthesized under many different recipes — different reducing agents, different capping/stabilizing agents, different reaction times — and the recipe strongly shapes particle morphology (size, shape, dispersion, aggregation). A materials scientist handed an unlabeled transmission electron microscope (TEM) micrograph of a nanoparticle batch often needs to determine which synthesis condition most plausibly produced it, such as when detecting a mislabeled batch or matching a mystery sample to a recorded protocol. This challenge poses that as a ranking problem: given a query micrograph and a small labeled reference gallery, produce a full preference ordering over all candidate synthesis conditions, most likely first. An earlier design considered predicting antibacterial potency directly from a micrograph. That formulation was rejected because the source data contains bioactivity assays for only one of the nine synthesis conditions. Every image from that condition would carry the same target value, allowing a constant prediction to solve the task. Task The input is a 512×512 grayscale PNG tile, identified by sample_id, cropped and contrast-normalized from a TEM micrograph. You are given: A gallery of 54 reference tiles, six per synthesis condition, each labeled with its condition. 210 unlabeled query tiles. For every query, output a full ranking of the nine condition labels from most to least likely. There is no separate labeled training set. Build an embedding or similarity method from the gallery, then rank the conditions by how well their examples match each query. Gallery and query tiles are split by source micrograph. Tiles cropped from the same source micrograph never appear on both sides, so a solution must generalize beyond one micrograph's background artifacts. The nine valid condition labels are: Borohidreto_de_sódio_Ácido_Citrico__1_hora Borohidreto_de_sódio_Ácido_Citrico__2_horas Borohidreto_de_sódio_Ácido_Citrico__30_min Borohidreto_de_sódio_Ácido_Citrico__4_horas Borohidreto_de_sódio_Ácido_tartárico__1_hora Borohidreto_de_sódio_Ácido_tartárico__2_horas Borohidreto_de_sódio_Ácido_tartárico__30_min Borohidreto_de_sódio_Ácido_tartárico__4_horas Etanolico Evaluation Submissions are scored with Mean Reciprocal Rank (MRR). For query $q$ with true condition $c(q)$ and submitted ranking $\hat r(q) = (\text{cond}_1, \text{cond}_2, \ldots, \text{cond}_9)$, let $\text{rank}(q)$ be the one-indexed position of $c(q)$: $$ \text{rank}(q) = \min\{\, i \in \{1,\dots,9\} : \hat r(q)_i = c(q) \,\} $$ $$ \text{MRR} = \frac{1}{|Q|}\sum_{q \in Q} \frac{1}{\text{rank}(q)} $$ MRR lies in $[1/9, 1]$ for a valid submission. A perfect submission scores 1.0, a submission that always ranks the true condition ninth scores $1/9$, and a uniformly random permutation has expected MRR $\frac{1}{9}\sum_{i=1}^{9}\frac{1}{i} \approx 0.3143$. MRR is chosen because the practical objective is to put the correct recipe as early as possible in the list a scientist would inspect. If the true recipe is at rank $r$, then $r$ candidates must be checked before it is found, and the per-query score $1/r$ assigns sharply decreasing credit as that inspection burden grows. For example, moving the answer from rank 2 to rank 1 gains $0.5$, while moving it from rank 9 to rank 8 gains only about $0.014$. This head-weighting matches the intended quality: getting the first recommendation right matters more than rearranging implausible recipes near the bottom. The principal alternatives were rejected for task-specific reasons: Top-1 accuracy discards every position after the first, so rankings with the true condition second and ninth receive the same score even though one is a much better shortlist. Recall@K has the same threshold problem at the chosen cutoff and introduces an arbitrary $K$ when the submission already supplies a complete ranking. Each query has exactly one relevant condition. Its average precision is therefore $\operatorname{AP}(q)=\operatorname{Precision@rank}(q)=1/\operatorname{rank}(q)$, so MAP is algebraically identical to MRR here and cannot produce a different ordering of submissions. With one binary-relevant condition, NDCG reduces to $1/\log_2(\operatorname{rank}(q)+1)$. That discount gives rank 2 about $0.631$ and rank 9 about $0.301$, compared with $0.5$ and $0.111$ under reciprocal rank. NDCG is useful when several items have graded relevance; this task has neither. Its flatter discount would give relatively more credit to burying the only correct condition near the bottom, contrary to the intended first-candidate emphasis. No composite term is added because the plausible components either measure the same rank again or require information the task does not contain. Accuracy and Recall@K are thresholded functions of the same true-condition rank, while MAP is exactly the same quantity; combining any of them with MRR would only change the rank-discount curve and double-count ranking quality. Calibration metrics such as log loss or Brier score require probabilities, but submissions contain only an ordering, so calibration is not observable. Coverage and duplicate penalties are enforced as validity constraints because every row must be a complete permutation of all nine labels. A per-condition macro average would only reweight the same reciprocal ranks: eight conditions have 24 queries and one has 18 after exact deduplication. Per-query MRR keeps the declared unit of evaluation—a query micrograph tile—equally weighted. There is therefore no second, independently supported outcome to combine with rank quality in this dataset. Submission Submit a CSV file with these columns: query_id (str): the tile identifier from query_ids.csv. ranked_conditions (str): all nine condition labels joined by |, ordered most likely first. Each condition must occur exactly once. Example: query_id,ranked_conditions sample_765fa6613757,Etanolico|Borohidreto_de_sódio_Ácido_tartárico__4_horas|Borohidreto_de_sódio_Ácido_Citrico__1_hora|Borohidreto_de_sódio_Ácido_Citrico__2_horas|Borohidreto_de_sódio_Ácido_Citrico__30_min|Borohidreto_de_sódio_Ácido_Citrico__4_horas|Borohidreto_de_sódio_Ácido_tartárico__1_hora|Borohidreto_de_sódio_Ácido_tartárico__2_horas|Borohidreto_de_sódio_Ácido_tartárico__30_min sample_63713cd2ade3,Borohidreto_de_sódio_Ácido_Citrico__1_hora|Borohidreto_de_sódio_Ácido_Citrico__30_min|Etanolico|Borohidreto_de_sódio_Ácido_Citrico__2_horas|Borohidreto_de_sódio_Ácido_Citrico__4_horas|Borohidreto_de_sódio_Ácido_tartárico__1_hora|Borohidreto_de_sódio_Ácido_tartárico__2_horas|Borohidreto_de_sódio_Ácido_tartárico__30_min|Borohidreto_de_sódio_Ácido_tartárico__4_horas Requirements Must contain exactly 210 rows, one per query in query_ids.csv. Include the header query_id,ranked_conditions. Each ranked_conditions value must be a |-separated permutation of all nine labels listed above. Each required query_id must appear exactly once. Dataset public/gallery/ (directory): 54 PNG tiles, 512×512, 8-bit grayscale. public/gallery.csv (file): labeled gallery metadata. sample_id (str): gallery tile identifier matching a PNG filename. condition (str): one of the nine condition labels listed above. public/queries/ (directory): 210 unlabeled PNG tiles, 512×512, 8-bit grayscale. public/query_ids.csv (file): query identifiers. sample_id (str): query tile identifier matching a PNG filename. public/sample_submission.csv (file): a valid-format placeholder submission in a fixed alphabetical ranking order. Constraints Do not use the original Zenodo record or another external copy of this dataset to look up labels for public query items. Do not use LLM-generated content in a solution's data-handling pipeline. &nbsp;
> $700 Pool
> Closes in 4h 40m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Cloud Gallery Registration and Boundary Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7b9nx78y8s3x9mvzazt1r0gx8dy5xz
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat killshark's score of 0.568!

Full challenge description from page:

> Background Cloud observations assembled from partial camera views can contain inconsistent orientation, photometric differences, and unrelated fragments. Recovering a semantic boundary profile requires first identifying which views belong together and locating them in a common coordinate frame. This benchmark combines visual provenance selection, overlap registration, and sparse cloud-genus boundary reconstruction using the supplied polygon annotations. Overview Each input image is a shuffled 3×3 gallery of nine 224×224 tiles. Six tiles cover one hidden canonical 512×384 sky photograph through overlapping windows. Three distractors come from other photographs in the same data split. The anchor_slot identifies the canonical photograph's unrotated upper-left tile. Recover the ordered class intervals along three directed chords in that canonical photograph. The six genuine crop origins are exactly (0,0), (144,0), (288,0), (0,160), (144,160), and (288,160), all with width and height 224. Genuine neighboring crops therefore overlap by 80 pixels horizontally or 64 vertically. Apart from the anchor, each tile is independently rotated by 0, 90, 180, or 270 degrees counterclockwise, shuffled, and photometrically perturbed. Gallery slot order carries no spatial meaning. Use overlap evidence to reject unrelated tiles, undo rotation, and recover canonical coordinates before predicting boundary profiles. No assembled canonical photograph or full-frame class mask is supplied. Training-only layouts provide registration supervision, and three annotated chords provide sparse semantic supervision. A class mask predicted directly on the gallery cannot be sampled using the query coordinates: those coordinates refer to the hidden canonical frame and exclude all distractors. Tile identity and arrangement are deterministic transformations of source photographs; cloud labels remain native polygon annotations. Dataset Information (Public Files) The public directory contains all assets required to train and evaluate models locally. Canonical source views are resized to 512×384, cropped by removing the bottom 24 rows, and resized back to 512×384. The identical transform applies to source masks before chord sampling. Public galleries are 672×672 and contain nine 224×224 tiles. +-----------------------+-------------------------------------------------------+ | File / Directory | Purpose | +-----------------------+-------------------------------------------------------+ | images/ | 672x672 shuffled nine-tile RGB galleries. | | train.csv | Labeled canonical-frame chord queries. | | test.csv | Unlabeled canonical-frame chord queries. | | train_layout.csv | Training-only index: id,layout for six genuine tiles. | | sample_submission.csv | Unchanged id,intervals format example. | | class_legend.json | Native cloud category IDs 0..5. | +-----------------------+-------------------------------------------------------+ Feature Schema train.csv and test.csv +-------------+---------+---------------------------------------------------------------------+ | Column | Type | Description | +-------------+---------+---------------------------------------------------------------------+ | id | String | Opaque query identifier. | | image | String | Relative path to the 672x672 tile gallery. | | anchor_slot | Integer | 0..8 row-major gallery slot of unrotated canonical upper-left tile. | | chords | JSON | Three [x0,y0,x1,y1] queries in canonical 0..1000 coordinates. | | intervals | JSON | Train only: ordered native class intervals for the three chords. | +-------------+---------+---------------------------------------------------------------------+ The auxiliary layout cell is a JSON list of six records [slot,canonical_x,canonical_y,rotation_k]. Here rotation_k is the number of 90-degree counterclockwise rotations applied to the crop before placing it in the gallery. Undo this rotation to reconstruct the view. The three slots absent from the layout are distractors. This supervision is supplied only for training IDs. Query Chords Schema The chords field contains exactly three coordinate quadruples: $$\text{chords} = [[x_{0,1}, y_{0,1}, x_{1,1}, y_{1,1}], [x_{0,2}, y_{0,2}, x_{1,2}, y_{1,2}], [x_{0,3}, y_{0,3}, x_{1,3}, y_{1,3}]]$$ Coordinates are integers normalized to a 0–1000 coordinate space. Sampling convention: Sample each directed segment at 128 uniformly spaced points from $(x_0, y_0)$ to $(x_1, y_1)$ inclusive, mapped to the image dimensions $(512 \times 384)$ via nearest-pixel rounding: $$x[i] = \text{round}\left( \frac{i}{127} \times 511 \right), \quad y[i] = \text{round}\left( \frac{y_0 + \frac{i}{127}(y_1 - y_0)}{1000} \times 383 \right) \quad \text{for } i \in [0, 127]$$ Target Intervals Schema The intervals field is a JSON array of three lists (one per chord). Each chord's sequence is represented as an array of contiguous, half-open intervals: $$[[\text{class}, \text{start}, \text{stop}], \dots]$$ class: Integer from 0 to 5: 0: Unannotated background / clear sky 1: Trees / buildings (foreground obstacles) 2: Stratocumuliform 3: Stratiform 4: Cirriform 5: Cumuliform start, stop: Integer sample indices spanning $[0, 128]$. Structural Constraints: Runs within a chord must start at 0 and terminate at 128. Intervals must be strictly contiguous without gaps or overlaps (i.e., run $k$'s stop must equal run $k+1$'s start). Adjacent intervals along the same chord must differ in class. Each chord can contain between 1 and 128 runs. Generalization & Leakage Controls All crops of a source photograph remain in its assigned split. Distractor photographs are selected only from the same split as the target, so a source cannot enter training through a gallery while belonging to evaluation. The canonical photo and its six tiles always stay together. Source grouping uses available capture dates or buffered capture-time blocks; it does not claim unavailable physical camera or observer identities. The original perturbations remain: gain 0.9–1.1, offset −8..8, independent RGB channel offsets −5..5, 2–5 bright/dark rectangular distractors with half-sizes 2–6 pixels and intensity changes 10–25, and Gaussian noise with standard deviation 4–8 on the 0–255 scale. Target and distractor source views receive the same degradation family. Each gallery tile additionally receives independent gain 0.95–1.05, offset −4..4, and Gaussian standard deviation 2–4. Values are rounded, clipped, and JPEG-encoded deterministically. Temporal Grouping: All images captured on the same calendar date are kept together within the same split. Buffer Zones for Undated Sequences: Undated files are clustered into 45-minute continuous blocks separated by 4-minute buffer exclusions to prevent near-duplicate temporal frames from leaking between training and evaluation splits. RGB Deduplication: Bitwise identical images are identified and removed prior to splitting. Split Stratification: 75% of independent temporal groups are assigned to train.csv and 25% to test.csv. Evaluation Metrics Evaluation combines region classification accuracy (macro Intersection over Union) with boundary localization precision along each query line. Each submission row expands the predicted and ground-truth intervals into three 128-element integer vectors (concatenated to a 384-sample sequence). 1. Non-Zero Class IoU ($M$) Let $C_{\text{active}}$ be the set of non-zero classes ($c \in 1, 2, 3, 4, 5$) present in either the ground truth or the prediction for that row: $$\text{IoU}_c = \frac{\vert{}P_c \cap T_c\vert{}}{\vert{}P_c \cup T_c\vert{}}$$ $$M = \frac{1}{\vert{}C_{\text{active}}\vert{}} \sum_{c \in C_{\text{active}}} \text{IoU}_c$$ (If neither prediction nor ground truth contains any non-zero classes, $M = 1.0$ if both vectors are identical, and $0.0$ otherwise). 2. Boundary Transition Score ($B$) Transitions represent internal boundary interfaces, formatted as tuples: $$(\text{sample index}, \text{previous class}, \text{next class})$$ For each chord independently: Predicted transitions are matched to ground-truth transitions on the same chord. A candidate match is valid if and only if both the predecessor and successor classes match exactly: $$(c_{0,\text{pred}}, c_{1,\text{pred}}) = (c_{0,\text{true}}, c_{1,\text{true}})$$ and their spatial locations are within a tolerance of 2 samples: $$\vert{}x_{\text{pred}} - x_{\text{true}}\vert{} \le 2$$ Matches are paired greedily in ground-truth order (ties broken by reference index). Let $N_{\text{pred}}$ and $N_{\text{true}}$ be the total count of boundary transitions across all three chords, and $K$ be the number of matched transitions: $$B = \begin{cases} \frac{2K}{N_{\text{pred}} + N_{\text{true}}} & \text{if } N_{\text{pred}} + N_{\text{true}} > 0 1.0 & \text{if } N_{\text{pred}} + N_{\text{true}} = 0 \end{cases}$$ 3. Row & Final Score The row score combines regional classification and boundary sharpness: $$\text{Row Score} = 0.75 \times M + 0.25 \times B$$ The competition metric is the arithmetic mean of row scores across all evaluation cases: $$\text{Final Score} = \frac{1}{N_{\text{test}}} \sum_{i=1}^{N_{\text{test}}} \text{Row Score}_i$$ Scores range from $0.0$ to $1.0$, where $1.0$ denotes an exact classification and boundary reconstruction. Sample Submission Format Submit a UTF-8 CSV containing exactly two columns: id and intervals. Include every test ID exactly once. id,intervals 2fab93a3dbbe6ba10d254705,"[[[3,0,128]],[[3,0,128]],[[3,0,128]]]" Parsing Bounds & Invalidation: - The serialized intervals cell must not exceed 12,000 characters. - Structural errors (non-integer indices, out-of-bounds classes, overlapping intervals, non-zero starting index, terminal index not equal to 128, or identical adjacent classes) will invalidate that specific row, assigning it a score of 0.0. - Missing rows, duplicate IDs, modified columns, or files exceeding 30,000,000 bytes will fail the entire submission with a score of 0.0. What Not To Use To ensure a fair and reproducible benchmarking environment: No External Visual Datasets: External meteorological datasets, supplementary sky photography, or web scraping are prohibited. No Pretrained Checkpoint Violations: Only general-purpose weights from the organizer's approved baseline allowlist may be loaded. Any fine-tuned cloud segmentation models or task-specific checkpoints trained outside the competition runtime are forbidden. No Test-Time Transduction: Pseudo-labeling test rows, calculating test-set aggregate statistics, or manual visual inspection of the evaluation images is strictly disallowed. No Online Inference: The execution container operates fully offline. Hosted APIs, reverse image search, or external lookup tables will cause immediate disqualification. Deterministic geometric postprocessors and standard label-preserving data augmentations (e.g., color jitter, horizontal flips) are permitted during training. &nbsp;
> $700 Pool
> 2 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Category-Held-Out Surface Primitive and Boundary Parsing

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a9f9frywd1gk23t7h65dca18dxssm
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat killerpsycho's score of 0.560!

Full challenge description from page:

> Overview Label an unorganized 3D point cloud with both its surface primitive and its proximity to a geometric boundary. Generalize to CAD categories absent from training, using coordinates rather than supplied normals, CAD topology or axis labels. Dataset train.csv / test.csv: task_id; 700 training objects and 200 test objects. train_points.npz / test_points.npz: arrays keyed by task_id, with N × 3 coordinates and at most 1,024 points per object. train_labels.csv / sample_submission.csv: task_id,target_json. All objects in a source category remain in one split, including template-generated variants. Exact normalized-coordinate duplicates are removed. Each cloud is centered, scaled to unit maximum radius, independently rotated and point-shuffled. Subsampling selects native points without interpolation. Only source coordinates are inputs; primitive and boundary annotations remain targets. Similar local geometry can recur across categories, and sparse sampling makes some boundaries ambiguous. Task Return one integer per point, in the supplied array order: label = 2 × primitive + near_edge. Primitive codes are 0 other, 1 cone, 2 cylinder and 3 plane. near_edge is 0 or 1, giving eight joint classes. Objects are selected by fixed hash order within the existing category-held-out partitions. Each selected cloud retains a deterministic 1,024-point subset (or all points if fewer), with the matching primitive and boundary labels at exactly those indices. No labels are interpolated. Submission task_id,target_json example_1,"[6,7,4,4]" example_2,"[2,3,0]" These abbreviated examples illustrate variable point counts. Actual list length must equal the object's point count. Columns must be exactly task_id,target_json, in that order, with each test ID once. Wrong-length lists, noninteger/out-of-range labels or malformed JSON give that object zero. Evaluation Mean per-object intersection-over-union. Within each object, compute TP / (TP + FP + FN) for every joint class present in either prediction or reference, then average those class IoUs. Average the resulting scores equally across objects. Score 1 is perfect. This balances joint geometric classes within each object without letting larger clouds dominate. Malformed rows receive zero, not an abstention that can improve another object's score. File-level schema and ID errors are rejected. Expected Methods Point-cloud networks and learned local geometric descriptors. Generic public pretrained models are allowed. What Not To Use No original CAD/mesh lookup, source point labels, source-specific checkpoints, external labeled CAD data, manual test annotation or hosted APIs. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The maximum end-to-end runtime is 1.5 hours, including data loading, training or adaptation, inference, structured decoding, validation, and submission writing. &nbsp;
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Two-Cut Connectivity from Molecular Sketches

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx714hz468mbqt9p13st4xqgjs8e4883
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat reze's score of 0.666!

Full challenge description from page:

> Overview Infer how a drawn molecular graph separates when two bonds are removed. Rings can preserve connectivity after one deletion, while a second deletion can split them; branch placement changes the resulting component sizes. The target is a structural connectivity fingerprint useful for comparing drawings by graph resilience. It is not a chemical reaction, bond-breaking energy, or mass-spectrum prediction. Task Interpret the drawing as an undirected graph of heavy atoms: omit every hydrogen atom, including explicitly drawn or isotope-labelled hydrogen, and its incident edges. Each bond between two retained atoms is one edge, regardless of bond order, aromaticity or stereochemistry. The graphs are connected and contain 3–73 heavy atoms and at least two edges. Consider every unordered pair of distinct edges, with equal weight. Delete both edges and count the heavy atoms in each connected component. Sort component sizes in descending order and append zeros until there are three values. Let b be the second-largest size and c the third-largest size. If the graph remains connected, both are zero; if it splits into two components, only c is zero. Predict the probability distribution of (b,c) over these deletions. Encode it as 925 values in row-major order: index 25*b+c, for b=0,...,36 and c=0,...,24. Values count atoms, not molecular mass. The largest component is deliberately not part of the fingerprint. For example, component sizes [7,3,1] contribute to index 76. A three-atom chain contributes all its probability to index 26: deleting its two edges leaves [1,1,1]. Dataset There are 1,800 training drawings and 400 test drawings, one distinct heavy-atom graph per row. Test drawings come from three writers absent from training; the training set contains other writers. Graphs equivalent after ignoring hydrogen and stereochemistry do not cross the split. No writer identity is an input. | File or field | Definition | |---|---| | train.csv | Columns id,image,profile; 1,800 rows. | | test.csv | Columns id,image; 400 rows. | | sample_submission.csv | Columns id,profile; a deterministic pseudo-random format example, not an inferred prediction. | | images/ | Referenced 256×256 grayscale PNG drawings, white background, pixel intensities 0–255. Aspect ratio is preserved by fitting and padding; no bond or atom location annotations are supplied. | | id | Opaque string used only for row alignment. | | image | Relative path to the drawing in the public package. | | profile | JSON array of 925 probabilities in the indexing order defined above. | Submission Format Submit exactly id,profile, in that column order, with one row for every test ID and no other IDs. Rows may be reordered. Each profile must be a JSON array of exactly 925 finite numeric values in [0,1], summing to one within an absolute tolerance of 1e-6. JSON booleans, strings instead of numbers, nulls and nested arrays are invalid. Probability on a mathematically impossible outcome is allowed but earns no overlap with the truth. The following is a literal format example placing all probability on (0,0); replace demo with a test ID and provide your prediction: id,profile demo,"[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]" Missing, additional, repeated, blank or padded IDs; missing, additional, repeated or reordered columns; malformed CSV or JSON; incorrect lengths; and invalid probability values reject the entire submission with an error. The grader does not silently repair predictions. Evaluation For true profile y and prediction p, the per-drawing score is: sum_j min(y_j,p_j) / sum_j max(y_j,p_j). The final score is the arithmetic mean across drawings; higher is better, with theoretical range [0,1]. An exact known-answer submission scores 1. Rows are aligned by ID and each drawing is a complete scoring unit. This probability-overlap metric rewards matching the frequencies of component-size outcomes, not merely selecting the most common outcome. For exactly normalized profiles it equals (1-TV)/(1+TV), where TV = 0.5*sum_j abs(y_j-p_j). Thus increasing total misplaced probability decreases the score. Unlike squared error, it does not disproportionately emphasize a few large probability errors; unlike KL divergence, it remains finite for sparse profiles and zero-probability predictions. Exact atom-count outcomes, rather than approximate mass or spatial distance, define overlap. Expected Approach Train a model from scratch using the provided drawings and training profiles. Image encoders, learned intermediate graph representations and graph-aware losses are possible approaches. Training, feature extraction and inference must run on CPU. What Not To Use Do not use GPU acceleration. Do not use pretrained models or external training data. Do not recover source identifiers or retrieve source annotations. Use IDs only for alignment. &nbsp;
> $700 Pool
> 2 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Cross-Room-Type Indoor Object Segmentation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx789zg9dtfshx03prfzya1g8d8e3b7p
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat moatasem's score of 0.268!

Full challenge description from page:

> Cross-Room-Type Indoor Object Segmentation Task type This is a segmentation-under-domain-shift task. You are given photographs of indoor scenes and must, for every photo, mark which pixels belong to each of three objects. What makes it different from ordinary indoor semantic segmentation is the split: the test photos come from room types that never appear in training. Your model is trained on one set of room categories (bedrooms, bathrooms, offices, closets, …) and scored on a disjoint set (dining rooms, kitchens, galleries, attics, chapels, …). You are therefore not rewarded for learning "what a dining room looks like" and guessing from context — you must learn what each object itself looks like, so it transfers to rooms you have never seen. The three objects The three target objects are deliberately room-agnostic — each occurs across dozens of room types — so none of them can be inferred from the room category, and the amount of one tells you almost nothing about the amount of the others: door -- a door or doorway. chair -- a chair or seat. curtain -- a curtain or drape. Their per-image areas are decorrelated, with every pairwise rank correlation at or below 0.05 in magnitude, so the three per-object scores are three near-independent measures: a solution good at one gets little on the others, and must find each object on its own — in rooms it was not trained on. Why this is hard (and what it rewards) A plain segmentation model learns strong room-context priors: seeing a bedroom, it expects the large rectangle to be a bed. Here that shortcut is removed — the scored rooms are new categories — so a model that leans on room context collapses, while one that has learned room-invariant object appearance (a door is a door in a kitchen or a chapel) generalises. The split, not just the pixels, is the challenge. What you are given train_images/.png -- 256 by 256 RGB indoor-scene photos. train_masks.csv -- the ground-truth masks for the training photos, in the same format as your submission: columns id, door, chair, curtain, one row per training image, each cell the RLE of that object's binary mask over the 256 by 256 frame (0 0 when the object is absent). Decode each class to a binary mask; the three never overlap, so together they give a per-pixel label map (0 other, 1 door, 2 chair, 3 curtain). train_groups.csv -- columns id, room_type: the room category of each training photo. Use it for room-aware cross-validation — hold out whole room types locally to mimic the real test shift. (Test room types are disjoint from every value here.) test_images/.png -- the photos to segment; each is from a room type absent from training. test_queries.csv -- column id, the photos to score. sample_submission.csv -- a correctly shaped example: one row per test image with 0 0 (an empty mask) for every object. What you submit working/submission.csv with exactly the columns id, door, chair, curtain and one row per test image (each id appears exactly once): id -- the test image id. door, chair, curtain -- for each object, a run-length encoding of that object's binary mask over the 256 by 256 frame: a space-separated string of start length start length ... pairs, where start is a 0-indexed row-major pixel position into the flattened 256 by 256 mask and length is the number of consecutive set pixels. When the object is absent, write 0 0 (a zero-length run, i.e. an all-zero mask) -- do not leave the cell blank. Positions must stay within 0 to 65535. There is exactly one row per test image, and every test id must appear exactly once. How you are scored The metric is SceneScore, higher is better, bounded in 0 to 1. For each object the score is the dataset-level intersection-over-union over the held-out-room-type test set: the intersection and the union of predicted and true pixels are summed over all test images, and the object score is intersection divided by union. SceneScore is the mean of the three object scores. Predicting everything empty, or the same fixed mask for every image, both score near 0; a solution that segments each object where it actually is — in unseen room types — scores high. The split Leave-whole-room-type-out. Room types are partitioned so that ~20 percent of the photos, forming a set of entire room categories, are held out for test; the remaining room categories are training. No room type is shared between train and test, so every test photo is a room context the model has never seen. All three objects are room-agnostic and remain present in both splits. The split is a deterministic function of the room-type names. Allowed and prohibited Allowed -- any model you train on the provided photos, such as a convolutional segmentation network trained from scratch; standard image preprocessing and augmentation such as horizontal flips, crops, and colour jitter; any domain-generalisation technique. Prohibited -- external data or pretrained image weights; per-id answer tables or any hardcoded output; training on, fitting to, or otherwise adapting to the test photos (test-time training, tuning on test statistics, or hand-labelling them); recovering anything from the id rather than the image. Ids are randomised and carry no signal. (Running your trained model's forward pass on the test photos to produce their masks is the task itself and is of course expected.) Compute GPU, one hour. The from-scratch reference network trains well inside that budget. &nbsp;
> $700 Pool
> 2 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Lost Wash — recover the surveyor's wall-construction code from a colour-stripped town plan

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cj8a77k3jcvnxw5y0ehmdt18dz81q
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat 15_luz's score of 0.351!

Full challenge description from page:

> The task You are given crops of historical large-scale urban survey plans (fire-insurance atlases of small North American towns, 1880s–1920s). On the originals, the field surveyor painted every building footprint in a colour that encodes the material of its walls. In this dataset that colour layer has been removed: what remains is a 1-bit line drawing (lot lines, streets, footprint outlines, porches, annotations) in which every building interior is blank. For each building listed in test.csv you must predict which construction class the surveyor recorded. There are four classes: frame — wood-frame construction brick — brick (or tile) walls stone — stone or concrete walls special — special construction (fire-resistive or metal-clad structures) Nothing in the rasters states the class. It has to be inferred from what the drawing still shows: the shape, size and orientation of the footprint, how it sits on its lot, how densely it is packed against its neighbours, whether it faces a commercial street or sits behind a dwelling, what kind of town the crop comes from, and whatever other regularities of the era's building practice you can learn from the training towns. Test towns are never seen in training. A model has to learn a population-level habit, not one town's quirk. Files train.csv test.csv sample_submission.csv classes.txt images/train/.png 1-bit PNG, 1024 x 1024 px, white paper / black ink (training crops) images/test/.png same, test crops masks/train/.png 16-bit PNG, 1024 x 1024 px, building-instance raster for the training crop masks/test/.png same, test crops Every crop covers the same ground scale: 150 pixels per map inch, i.e. 3 pixels per foot at the atlases' standard 1:600 scale (a 25 ft house is about 75 px wide). All crops are 1024 x 1024 px. A crop and its mask share one file stem (crop_id). In a mask raster, pixel value 0 means "no building" and every other value is the id of one building instance; that value is the inst column of the tables. The instance raster contains every building in the crop, including buildings that are not listed in the tables (buildings cut by the crop border or assigned to a neighbouring crop) — you may use them as context, but only listed buildings are graded. Each crop has been given a private rotation/flip, so north is not a fixed direction. Tables train.csv — one row per graded training building. Columns: building_id (string): unique id of the building, formed as _. crop_id (string): the crop (image and mask file stem) the building lives in. town_id (string): opaque id of the town the crop was cut from. Use it for grouped validation: test towns are disjoint from training towns, so a random split of train.csv will over-estimate your test score. inst (integer): the pixel value of this building in masks/train/.png. cx (float): x coordinate (column, pixels) of the building's centroid in the crop. cy (float): y coordinate (row, pixels) of the building's centroid in the crop. area_px (integer): number of pixels of the building instance. bbox_w (integer): width of the building's bounding box in pixels. bbox_h (integer): height of the building's bounding box in pixels. material (string): the target, one of frame, brick, stone, special. test.csv — one row per graded test building, with the same columns except material. sample_submission.csv — the required submission layout (building_id, material) filled with a cycling dummy label; it scores at the floor. classes.txt — the four class names, one per line. Submission format A CSV with exactly two columns, building_id and material, containing every building_id of test.csv exactly once, and a material value from the four class names. Extra columns, missing ids, duplicate ids, ids that are not in test.csv, or unknown labels are rejected, not scored. Evaluation The score is the macro-recall skill: recall_k = (number of gold class-k buildings predicted as k) / (number of gold class-k buildings) BA = mean over the K classes present in the graded rows of recall_k score = (BA - 1/K) / (1 - 1/K), floored at 0.01 and capped at 1.0 With K = 4, predicting the same class for everything gives BA = 0.25 and a score at the floor; uniform random guessing has expected score 0; a submission that is perfect on frame and brick but never predicts the two rare classes scores exactly 1/3. Every class therefore matters equally, although frame is by far the most frequent class and special the rarest. The public and private leaderboards are two disjoint subsets of the test buildings scored with the same formula. Rules The graded predictions must come from a model you train on the provided training data (pretrained, publicly available vision backbones are allowed and encouraged as initialisation). Hand-written rules may be used as features or baselines but not as the submitted predictor. Do not try to identify or retrieve the original atlas sheets, any other historical map archive, street gazetteer or geographic database for these towns. The challenge is about inference from the supplied rasters; solutions that look up source material will be rejected in review regardless of score. Use only the data in this challenge plus public pretrained weights. No additional labelled map data. Your solution must run end to end (training and full test inference) inside the platform's time limit on a single GPU. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Fossil Diatom Morphometric Bands

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78tva685t2zdk75vsys5ag0n8c8cc9
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat masry1's score of 0.819!

Full challenge description from page:

> Fossil Diatom Morphometric Bands Overview Paleoenvironmental microscopy workflows use valve morphology as evidence during specialist screening. The challenge supplies real transmitted-light microscopy tiles and training band labels for a marine microfossil taxon. Your task is to infer the dominant valve-size band of each held-out tile from its pixels. This is a tile-level morphometric screening task, not ordinary object detection. For each annotated valve, let w and h be its normalized bounding-box width and height, and define its normalized size as sqrt(w * h). For a tile, the target statistic is the median of these valve sizes; “dominant” means this median, not the most frequent class. The statistic is assigned to an ordered band: small when it is below 0.055905, medium when it is at least 0.055905 and below 0.074165, and large when it is at least 0.074165. These cutpoints are dimensionless because the box dimensions are normalized to the tile. The band labels are tied to visible morphology, not filenames or a generated classifier. The box measurements are used to construct the training labels and hidden answers; solvers receive tile pixels plus training labels and must infer the band from pixels. The public/private split holds out complete sampling locations. A method that memorizes scanner texture, slide preparation, or location-specific backgrounds should not generalize well. The public train labels and hidden test answers use the same fixed boundaries. The public test CSV contains no target labels. Dataset File descriptions train.csv: a CSV index with one row per labeled tile; it contains IDs, relative image paths, anonymized training-group IDs, and size_band labels. Image pixels are not embedded in the CSV. test.csv: a CSV index with one row per unlabeled tile; it contains IDs, relative image paths, and anonymized sampling-group IDs. Image pixels are not embedded in the CSV. sample_submission.csv: a CSV template with test IDs and randomized valid size_band values. images/*.jpg: separate fixed-resolution JPEG files referenced by image_path in the CSV indexes. Column descriptions id (string): opaque 16-character SHA-256-derived tile identifier. image_path (string): path relative to ./dataset/public/ for the supplied JPEG. group_id (string, train and test): anonymized sampling-group token. Use it to keep validation folds group-aware and to identify tiles from the same sampling group; it is structural metadata, not a target proxy. size_band (string, train only): one of small, medium, or large. Evaluation The score combines class-balanced classification quality with ordinal closeness: from statistics import mean from sklearn.metrics import f1_score band_order = {"small": 0, "medium": 1, "large": 2} macro = f1_score(y_true, y_pred, labels=list(band_order), average="macro") true_index = [band_order[label] for label in y_true] pred_index = [band_order[label] for label in y_pred] ordinal = 1.0 - mean(abs(t - p) for t, p in zip(true_index, pred_index)) / 2.0 score = 0.60 macro + 0.40 ordinal The score is bounded in [0, 1] and is maximized. Macro-F1 prevents the common size band from dominating. The ordinal term gives partial credit to a one-band miss while treating a small-to-large jump as the most serious disagreement. This reflects how a morphometric screening tool would be used before a specialist performs full measurements. Submission Submit exactly one CSV with columns id and size_band. Include exactly one row for every ID in test.csv. Preserve each test ID exactly; do not sort by a different key or add an index column. Use only small, medium, or large; nulls and extra columns are invalid. Example: id,size_band 005e8625b1b93116,medium Requirements Use the supplied real tile pixels. External labeled data, lookup tables, synthetic images, and generated labels are prohibited. Do not use outside checkpoints, annotation files, or precomputed morphometric measurements as target lookups. Keep the solution deterministic, offline, and feasible on the CPU tier. Use paths relative to ./dataset/public/ for inputs and write ./working/submission.csv. A model may use image pixels and deterministic features computed from those pixels. group_id is supplied in both indexes for group-aware validation; treat it as structural metadata rather than a target proxy. What Not To Use Do not use web search or reverse-image search to recover held-out labels; the task is intended to measure learning from the supplied pixels and training labels. Do not use published morphometric tables, segmentation measurements, or external annotation files as target lookups; they bypass the pixel-level inference task. Do not use cached answer files, filename/order lookups, or target-proxy columns; they do not generalize to the opaque test IDs. &nbsp;
> $700 Pool
> Closes in 3h 6m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Cephalometric Angle Ranking from Lateral Head X-rays

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7crkk0xrax8sf1k0f1ene5gn8e26ag
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat douglas's score of 0.638!

Full challenge description from page:

> Cephalometric Angle Ranking from Lateral Head X-rays Task type This is a ranking task. You receive lateral head radiographs and must place them in order along seven cephalometric angles that orthodontists read from such films. You are scored only on how well your ordering of the test radiographs matches, angle by angle, the ordering that comes from expert landmark measurement. Degree values are never compared against each other; relative order is everything. Why the task is graded by rank, not by degrees The same skull, filmed on two machines or traced in two clinics, yields angle numbers that drift by a calibration offset, yet the clinical reading is comparative in nature -- is this jaw set further back than that one, does this face grow more vertically than the rest of the cohort, are these incisors more upright than average. A rank metric rewards recovering the geometry that separates one head from the next and cancels any constant bias a model carries, so a high score reflects reading the anatomy correctly rather than reproducing one measurement convention. Ranking also keeps the seven angles on an equal footing despite their very different natural spreads. The seven angles -- easy planes to hard incisor geometry Each radiograph is summarised by seven angles chosen to span a wide range of difficulty. The easy ones are read from large, well-separated landmarks and most solutions order them well; the hard ones depend on pinpointing tiny incisor tips and apices, and that is where a stronger model pulls ahead of a weaker one. Because your score is the mean over all seven, it spreads according to how much of the hard incisor geometry you can read -- not just the easy planes. fma (easy) -- vertical growth pattern, between the skull-base horizontal and the lower border of the mandible. gonial (easy) -- the angle at the corner of the jaw (Articulare-Gonion-Menton), a shape read from large landmarks. sna (moderate) -- the forward position of the upper jaw, at the cranial base. anb (moderate) -- the sagittal relationship between the jaws, SNA minus SNB. impa (hard) -- inclination of the lower front tooth to the mandibular plane. u1sn (hard) -- inclination of the upper front tooth to the cranial-base line. iia (hardest) -- the angle between the upper and lower front-tooth axes. The angles measure different things: every pairwise rank correlation is at or below 0.63 and most are under 0.4, with the two plane angles coupled to each other and the incisor angles coupled among themselves, but otherwise close to independent. A solution cannot ride one angle to score the rest; it must read both the coarse jaw planes and the fine incisor axes from the image. What you are given train_images/.png -- lateral head radiographs, 192 by 192 grayscale, letterboxed so the geometry that defines the angles is undistorted. train_targets.csv -- columns id, fma, gonial, sna, anb, impa, u1sn, iia, the seven angles in degrees for every training film. train_groups.csv -- columns id, group, the imaging machine each training film came from, so you can build a machine-aware validation split. test_images/.png -- the radiographs to place in order. test_queries.csv -- column id, the films to score. sample_submission.csv -- a correctly shaped example. What you submit working/submission.csv with exactly the columns id, fma, gonial, sna, anb, impa, u1sn, iia, one row per test id, every test id present once, all values finite. Any monotonic numeric estimate per angle works, since only the induced order is scored. How you are scored The metric is CephScore, higher is better, bounded in 0 to 1. For each angle it computes Kendall's tau between your estimates and the true angles across the test films, then clips it below at 0. CephScore is the mean of the seven clipped taus. A constant or random submission scores about 0; a solution that perfectly recovers all seven orderings scores 1. Because the seven span easy to hard, the achievable score spreads with how well a solution reads the hard incisor angles. The split -- unseen imaging machines The films were captured on seven different imaging machines. Whole machines are held out: every test radiograph comes from a scanner that appears nowhere in training. A solution therefore has to read anatomy that transfers across devices, not the contrast, sharpening, or field-of-view signature of a particular machine. The held-out machines are selected deterministically, and the machine of each training film is disclosed so you can reproduce a matching validation split yourself. Allowed and prohibited Allowed -- any model you train on the provided films, from a convolutional network to a landmark or keypoint model to a hand-feature regressor; standard image preprocessing; group-aware cross-validation using the disclosed machines. Prohibited -- external data or pretrained image weights; per-id answer tables or any hardcoded output; reading, fitting, or adapting to the test films in any way; recovering order from the id rather than the image. Ids are randomised and carry no signal. Compute GPU, one hour. The from-scratch reference network trains well inside that budget. &nbsp;
> $700 Pool
> Closes in 5h 29m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Blackjack Scene Structured Recognition

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77qj7cnyxjpybw34hm97530s8dx49f
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat masry1's score of 0.541!

Full challenge description from page:

> Blackjack Scene Structured Recognition Research objective Given one cluttered Blackjack table image, identify the dealer's face-up card and every card in the player's two-to-five-card hand. Then compute the player's Blackjack total, decide whether the hand is soft, and select the correct action. Submit all five results in one structured prediction record. The benchmark tests scene-level card recognition and rule-based reasoning together. Training labels describe the complete scene, but do not provide card crops, bounding boxes, corner coordinates, masks, object-to-role assignments, or separate per-card training examples. A solver must infer all of the following from the complete scene: locate the gold D and blue P semantic regions; bind visible cards to the correct role while rejecting face-down cards and table clutter; recover a variable-size unordered player set containing two to five cards; execute Ace-dependent Blackjack arithmetic to obtain total and soft; map the recovered state to the legal action under the stated rules. Target cards may be independently rotated, perspective-warped, overlapped, shadowed, blurred, compressed, partially cropped, or obscured by punched holes. Consequently, a correct action without a correct structured visual record is not sufficient for a high score. Difference from the closest public benchmark The closest related public work is JackFurby/blackjack(https://huggingface.co/datasets/JackFurby/blackjack)), created for concept-bottleneck research. It supplies synthetic Blackjack scenes together with task labels, concept labels, card identities, and explicit card-corner coordinates. This challenge deliberately evaluates a different supervision and generalization regime: Weak spatial supervision: only scene-level card sets and derived targets are released; no localization annotations or isolated target crops are available. Role-conditioned set recovery: identical card classes can appear in target and non-target contexts, so the output depends on semantic region binding rather than image-level presence alone. Held-out visual assets: training and evaluation scenes are rendered from disjoint source-card image partitions. Perceptual duplicates crossing those partitions were removed. Asymmetric evaluation shift: evaluation uses unseen card artwork and stronger geometric, occlusion, clutter, blur, and compression transformations while preserving the same semantic rules. Joint structured scoring: the metric separately measures dealer identity, player multiset recovery, Ace-aware state, legal action, and full-record exact match. Neither card classification nor best-move classification alone solves the benchmark. Small-data transfer setting: only 1,600 labeled scenes are public, so robustness must come from transferable visual representations rather than exhaustive generator coverage. The claimed contribution is therefore the benchmark protocol—weak role binding under held-out visual styles followed by deterministic symbolic state execution—not the novelty of playing-card recognition or Blackjack rules themselves. Dataset The public training set contains 1,600 labeled scenes. The evaluation set contains 300 scenes with privately held labels. Images are RGB JPEG files at 768 x 512 pixels. All card assets are derived from the CC0 Cards Image Dataset-Classification(https://www.kaggle.com/datasets/gpiosenka/cards-image-datasetclassification)). Joker images and the source dataset's pretrained model files were excluded. Only the 52 standard rank-suit classes were retained. Training and evaluation use disjoint source-card image partitions. Evaluation also uses stronger rotation, perspective, occlusion, clutter, blur, and JPEG degradation. The card vocabulary and Blackjack rules do not change. Diagnostic baseline During construction, an ImageNet-initialized ResNet18 with scene-level multitask heads was trained for 10 CPU epochs on a fixed 900-train/240-validation pilot generated by the same pipeline. Under the predecessor's stricter multiplicative metric, its best composite score was 0.03195. That historical result is disclosed only as a shortcut check and is not numerically comparable with the additive metric below. Public files train.csv — labeled training scenes with columns: id, image, prediction test.csv — evaluation scenes with columns: id, image images/train/ — training JPEG files images/test/ — evaluation JPEG files sample_submission.csv — submission template with columns: id, prediction Column definitions id — opaque identifier; row order and ID structure contain no target information. image — relative path to the scene image. prediction — canonical combined target containing all five required fields. Card codes Ranks: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K Suits: C — clubs D — diamonds H — hearts S — spades Examples: AH, 10D, QS. Blackjack rules Six-deck basic strategy Dealer stands on soft 17 Double after split is allowed No surrender or insurance DOUBLE and SPLIT are available only for an initial two-card hand Hands containing more than two cards can only be labeled HIT or STAND Dealer, player, and distractors Include only the face-up target card inside the gold D region as the dealer card. Include all face-up target cards inside the blue P region as player cards. Purple face-down cards are distractors and are never targets. Table chips, lines, shadows, and paper-like objects are distractors. Target cards can overlap one another; recover the complete multiset from all remaining evidence. Submission format Submit a CSV containing exactly two columns and exactly one row for every test ID: id,prediction The prediction contains exactly five semicolon-separated fields: dealer=9D;player=7S,AH;total=18;soft=1;action=HIT Field names are case-insensitive. Card and action values are normalized to uppercase. Surrounding whitespace, field order, and player-card order are ignored. The following are invalid: a missing, unknown, or duplicate ID a missing or additional prediction field an invalid card code fewer than two or more than five player cards duplicate exact cards within one hand a total outside 4 to 21 a soft value outside 0 or 1 an action outside HIT, STAND, DOUBLE, and SPLIT Missing, unknown, or duplicate IDs and invalid CSV schemas reject the whole submission. A malformed prediction record affects only its own ID: that row receives zero for all row-level components and is counted as incorrect in the soft-label recalls, while all other rows remain scorable. The parser validates each record strictly and its validation messages identify the offending ID. Sample: id,prediction va_000000,"dealer=AC;player=2C,3D;total=5;soft=0;action=HIT" Evaluation Valid records receive additive partial credit. A malformed prediction record receives zero for that row without discarding the other submitted rows. Player-card multiset F1 Let count_pred(k) and count_true(k) be the numbers of occurrences of card code k in the predicted and true player hands. Define: matched = sum over k of min(count_pred(k), count_true(k)) precision = matched / number_of_predicted_player_cards recall = matched / number_of_true_player_cards player_multiset_f1 = (2 × precision × recall) / (precision + recall) If precision + recall is zero, player_multiset_f1 is 0.0. Player-card order does not affect this calculation. Per-row composite score For the remaining fields, define dealer_correct, total_correct, soft_correct, and action_correct as 1.0 when the corresponding prediction equals the truth and 0.0 otherwise. The visual component is: visual = (0.85 × player_multiset_f1) + (0.15 × dealer_correct) The direct total component is total_correct. Because soft=0 is the majority class, the soft flag is evaluated globally with chance-corrected balanced accuracy rather than raw accuracy. Let recall_soft_0 and recall_soft_1 be recall for the two soft classes across all evaluation rows. Malformed records count as incorrect for their true class. Define: soft_balanced_accuracy = (recall_soft_0 + recall_soft_1) / 2 soft_skill = max(0, (2 × soft_balanced_accuracy) - 1) Thus a constant soft=0 or constant soft=1 prediction receives soft_skill = 0, while perfect soft predictions receive soft_skill = 1. Define full_record_exact_match as 1.0 only when the dealer card, unordered player-card multiset, total, soft flag, and action are all correct; otherwise it is 0.0. The metric awards additive partial credit so that improvement in any required component remains measurable. Define the non-soft row score and final score as: base_row_score = (0.65 × visual) (0.105 × total_correct) (0.05 × action_correct) (0.15 × full_record_exact_match) score = mean(base_row_score over all evaluation rows) (0.045 × soft_skill) The range is 0.0–1.0 and higher is better. A perfect submission scores 1.0. Prohibited methods Do not use external playing-card datasets, labels, templates, or separately downloaded source-card images. Do not reverse-image-search or externally retrieve evaluation card assets. Do not reconstruct generation seeds or hidden scenes from IDs. Do not derive predictions from identifiers, filenames, row order, or submission position. Do not manually label evaluation images. Do not use leaderboard feedback to reconstruct private labels. Do not use a content-free fixed lookup or handcrafted-only pipeline without a trained or fine-tuned model. Do not generate additional solver-training card scenes unless explicitly permitted by the platform rules. Using published Blackjack rules to compute total, soft, and action from cards predicted by a trained visual model is allowed. &nbsp;
> $700 Pool
> Closes in 2h 14m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Molecular Sketch Counterfactual Jury

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74h22exatr71vffjyt1efsyd8dshan
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat aneeshm44's score of 0.943!

Full challenge description from page:

> Overview For each hand-drawn molecule, choose the candidate graph supported by the sketch, identify its closest one-edit alternative, and classify the chemical edit that makes the alternative wrong. A case contains four notebook-style diagrams labeled A through D and eight anonymous graph records labeled g1 through g8. The candidates form four hidden pairs. Within each pair, the two graphs differ by exactly one atom, bond-order, bond-presence, or bond-endpoint edit. Either endpoint may be the graph shown in the image. This models chemical-document arbitration rather than ordinary optical recognition. A digitization pipeline often produces several plausible molecular records, and a reviewer needs both the accepted structure and a concrete counterfactual reason for rejecting its nearest rival. The answer must therefore account for all eight candidates, not merely emit one molecular string per panel. The Jury Procedure Submit three linked decisions: | Decision | Purpose | |---|---| | sketch_graph_bijection | Assign each panel to the graph it depicts. | | closest_decoy_bijection | Assign each panel to its paired one-edit alternative. | | decoy_fault_word | Name the edit separating the accepted and rejected graphs. | The two bijections must be disjoint and must use every ID g1 through g8 exactly once. This turns the case into a constrained graph jury: accepting a graph automatically determines which candidates remain available as counterfactuals for the other panels. How Cases Are Constructed The starting molecular records come from a real multi-contributor drawing collection. Contributor groups are held out between training and test. When the same molecular graph was drawn by multiple people, all copies follow the held-out side, preventing chemical identity from crossing the boundary. For each panel, preparation starts from one source graph and creates a new one-edit pair. Neither endpoint is the deposited source graph. The displayed endpoint is balanced so exactly two panels show the first derived endpoint and two show the second. Atom IDs are then reassigned independently for every candidate. The diagram is redrawn from the accepted graph with case-local rotation, shear, scale, stroke width, paper tone, and acquisition noise. Every visible atom label and bond is generated from that accepted graph. No deposited PNG survives as a lookup image, and source-graph membership does not reveal which endpoint was accepted. Contributor holdout is only the first split barrier. Preparation fingerprints molecular topology independently of atom numbering, removes any training source graph whose identity occurs in the held-out contributor pool, rejects every derived endpoint that equals any deposited source graph, and rejects the complete build if a newly derived accepted or decoy topology appears in both splits. A training accepted-graph dictionary therefore cannot contain a hidden endpoint. In a hidden packet, both anonymous endpoints are public and differ by one edit; only grounding those candidates in the redrawn pixels determines which endpoint was accepted. Dataset | Path | Contents | |---|---| | train.csv | 1,600 labeled jury cases. | | test.csv | 400 contributor-held-out cases. | | sample_submission.csv | Schema-valid baseline predictions. | | images/ | Distinct 1000 by 760 RGB JPEG boards. | Public Inputs | Column | Data type | Description | |---|---|---| | case_id | string | Opaque identifier used for alignment. | | sketch_board_path | relative path string | Four-panel molecular evidence board. | | candidate_graph_packet | JSON array encoded as a string | Eight objects with local fields id and graph. | Training Labels | Column | Data type | Description | |---|---|---| | sketch_graph_bijection | canonical mapping string | Four accepted panel-to-graph assignments. | | closest_decoy_bijection | canonical mapping string | Four rejected paired alternatives. | | decoy_fault_word | canonical labeled sequence | Four edit classes in panel order. | The 6,400 training-panel decisions contain 1,635 atom, 1,563 order, 1,602 rewire, and 1,600 toggle labels. There are 1,005 distinct accepted-bijection words and 1,009 distinct decoy-bijection words. Reading Candidate Graphs A graph uses the form atoms=;bonds=. An atom token gives a local node ID and element symbol. A bond token gives its two local endpoints and V2000 bond-type integer. Node numbering is arbitrary and differs among candidates, so graph comparison must be invariant to node IDs. The four fault labels mean: | Label | Counterfactual difference | |---|---| | atom | One element symbol differs. | | order | One bond type differs. | | rewire | One bond endpoint moves to a previously unconnected atom. | | toggle | One bond exists in only one endpoint; the label is direction-neutral. | Verdict Grammar Both bijection strings contain four tokens in A, B, C, D order: Graph IDs cannot repeat within a bijection. Across both bijections, the sets must be disjoint and their union must equal all eight candidate IDs. The fault word follows the same panel order: Fault labels may repeat. Bijection strings are limited to 28 characters and the fault word to 48 characters. Submission Format Write ./working/submission.csv with exactly these columns in order: case_id sketch_graph_bijection closest_decoy_bijection decoy_fault_word | case_id | sketch_graph_bijection | closest_decoy_bijection | decoy_fault_word | |---|---|---|---| | gj_f6c321d46a7f02902a61 | A=g6\|B=g1\|C=g8\|D=g3 | A=g2\|B=g7\|C=g4\|D=g5 | A:rewire\|B:atom\|C:toggle\|D:order | The example illustrates syntax only. Every hidden ID must occur once. Extra or reordered columns, duplicate or unknown IDs, missing rows, invalid graph IDs, repeated mapping targets, and malformed tokens are rejected or scored zero as documented. Evaluation The Molecular Jury Resolution Score is: Score = 0.55 * CorrectMatchScore + 0.25 * DecoyMatchScore + 0.20 * FaultScore Minimum score: 0.0. Maximum score: 1.0. Higher is better. Exact answers score 1.0. The weights follow the chemical review decision. CorrectMatchScore receives 0.55 because selecting the molecular record supported by the sketch is the primary archival action and an incorrect accepted graph changes the represented compound. DecoyMatchScore receives 0.25 because identifying the nearest rejected graph establishes the exact counterfactual under review, but it is subordinate to selecting the accepted structure. FaultScore receives 0.20 because it records the rejection reason; once both graph endpoints are known, this edit class is easier to derive mechanically than either image-to-graph assignment. The components therefore prioritize accepted identity, then counterfactual identity, then explanation. For an accepted or decoy bijection, panel_accuracy is the fraction of four panels mapped correctly. Each mapping row receives: 0.35 * panel_accuracy + 0.65 * exact_bijection_match CorrectMatchScore and DecoyMatchScore are the corresponding means. Exact bijection receives the larger share because the eight candidates form one constrained case: reusing one graph or displacing one panel changes the remaining assignments. Panel accuracy remains as bounded diagnostic credit for a partly resolved jury. For the fault word, fault_accuracy is the fraction of four panel labels that are correct. Its row score is: 0.50 * fault_accuracy + 0.50 * exact_fault_word_match The two submitted bijections must each contain four distinct graph IDs, remain disjoint, and cover g1 through g8. If this coherence rule fails, all three row scores are multiplied by 0.20. Malformed or overlong fields score zero for their component. Hidden answers are validated and never repaired. Fault scoring divides its weight evenly between local labels and the complete word because each one-edit explanation is meaningful independently, while a complete review still requires all four explanations. The 0.20 coherence multiplier is not another metric component; it limits credit for an impossible verdict that accepts or rejects the same candidate more than once. Why The Counterfactual Matters The accepted candidate cannot be selected by asking which graph already exists in a public collection: both pair endpoints are newly derived, and either one may be drawn. A solver must ground graph topology in the pixels, establish the pairing relation among anonymous candidates, and describe the smallest disagreement. This is a different reasoning object from image-to-SMILES transcription. Modeling Approaches Suitable systems may fine-tune a diagram encoder and a graph neural network, learn cross-modal compatibility, identify one-edit candidate pairs, and solve the two disjoint bijections with constrained decoding. Stereochemistry-aware graph features may be used, although images are never mirrored during preparation. The competition environment provides access to a single NVIDIA A10G GPU. The complete pipeline must finish within 1.5 hours, including data loading, training, inference, validation, decoding, and submission generation. What Not To Use Do not predict from case_id, board filenames, row order, candidate ordering, graph IDs, contributor metadata, or external graph lookup tables. Node IDs have no stable meaning, and neither candidate endpoint is a deposited source graph.
> $700 Pool
> Closes in 7h 31m
> 11 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Selecting Complementary Spectral Responses From Microscopy

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73ap2hpg5rdhne20zkwayez18e2arv
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview Predict which small groups of nanoparticle images would produce the requested optical response when their separately measured signals are added. Among six candidates, return every successful group that has no successful smaller subset, or an empty list when no group works. The images are real dark-field microscope observations. Each shows a colored diffraction pattern on a dark background, not a resolved photograph of the particle's surface. Color and the spatial distribution of light provide clues about scattering across wavelengths, including wavelengths outside the camera's visible range. Training examples include measured spectra to teach this relationship. The practical question is whether complementary observations can meet a spectral requirement that no observation meets alone. A candidate with too much response in one unwanted band can complement another candidate with a different imbalance. This is a virtual sum of separately recorded detector responses, not a prediction of the chemistry or electromagnetic interactions of physically mixed particles. Dataset Files | File | Contents | |---|---| | train.csv | 10,000 labeled requests. Columns, in order: case_id, candidate_images, pass_band_nm, guard_bands_nm, contrast, minimal_recipes. | | test.csv | 2,000 unlabeled requests with exactly the first five training columns, in the same order. | | sample_submission.csv | One row per test ID with case_id and minimal_recipes. Its varied predictions are sampled from complete training answers, without using test labels. | | images/ | 11,797 lossless 100 x 100 RGB PNG observations, each 30,168 bytes. Paths in the CSVs are relative to this public directory. An observation can be referenced by several requests within one split. | | training_spectroscopy.npz | Calibrated spectra for images used by training requests only. It contains no test-particle spectrum. | private/answers.csv, used by the evaluator rather than distributed as an input, contains exactly case_id and minimal_recipes for every test row. Request Fields | Column | Type | Meaning | |---|---|---| | case_id | string | Opaque identifier such as pool_8df90516ac2e870e7c501ea9. | | candidate_images | JSON-encoded array of six strings | Image paths in local candidate order A, B, C, D, E, F. A letter has no permanent identity across requests. | | pass_band_nm | JSON-encoded array of two integers | Inclusive lower and upper wavelength endpoints of the desired band, for example [835,865]. | | guard_bands_nm | JSON-encoded 2 x 2 integer array | The two unwanted bands, for example [[635,665],[735,765]]. Their order has no effect on the decision. | | contrast | float | Required ratio of pass-band response to each guard-band response. Values are 1.1, 1.3, or 1.5. | | minimal_recipes | JSON-encoded array of strings | Complete family of inclusion-minimal successful candidate subsets. Examples: ["A+B","C+E+F"] or []. | All bands are 30 nm wide. Their centers are 550, 600, 650, 700, 750, 800, 850, 900, or 950 nm; the three centers in a request are distinct. Candidate images contain no overlaid label or spectral curve. One complete labeled training request is shown below. Its four recipes include two minimal triples and two minimal pairs. | Field | Value | |---|---| | case_id | pool_6b9df7a542eb2901a02352f2 | | candidate_images | ["images/particle_b985e193f0a718aadc0bd868.png","images/particle_72a37d4c2964b2fe84278708.png","images/particle_ca35dee28086fa600d715515.png","images/particle_5d4664aa9b41aa0a04094858.png","images/particle_194d401b5b753b2085979cde.png","images/particle_37b0319fe9e6a8ca7beb5b77.png"] | | pass_band_nm | [835,865] | | guard_bands_nm | [[785,815],[935,965]] | | contrast | 1.1 | | minimal_recipes | ["A+B+C","A+B+E","A+F","B+F"] | Auxiliary Training Measurements The NPZ can be read with numpy.load(..., allow_pickle=False). | Key | Array type and shape | Meaning | |---|---|---| | image_paths | Unicode strings, [N] | Public paths of the N training particles represented in this file. | | wavelengths_nm | float64, [2048] | Strictly increasing measured calibration wavelengths, approximately 468.767 to 1026.760 nm. Spacing is not assumed uniform. | | calibrated_spectra | float32, [N,2048] | Background-subtracted, reference-corrected scattering intensities. Negative corrected values are set to zero. These are relative responses, not concentration or absolute emitted power. | N is the number of distinct particles actually used by training requests, not the number of requests. Test images are not present in image_paths. The hidden labels use the original float64 calibration rather than the rounded auxiliary float32 values. The paired-data build uses N = 9,471 distinct training observations and 2,326 distinct test observations. One image occurs in at most 65 training requests or 45 test requests. Reuse is necessary for asking different pass/guard questions about a finite set of measured responses; these are not additional independent particle captures. The same six-image request with the same bands and contrast does not recur under another letter permutation. What Counts As A Successful Group? For each particle, background is subtracted from its measured spectrum and the result is divided by the reference intensity at the same wavelength. Negative values after background correction are set to zero. A band's response is the trapezoidal integral of this corrected spectrum divided by the band's width. Band endpoints are linearly interpolated on the measured wavelength axis. For a nonempty candidate subset S of size at most three, let P(S), G1(S), and G2(S) be the sums of the members' mean responses in the pass band and the two guard bands. Let c be contrast. S succeeds exactly when P(S) >= c * G1(S) and P(S) >= c * G2(S). There is no extra power normalization, learned threshold, or rounding before this comparison. A successful group is minimal if no nonempty proper subset also succeeds. Return all such groups, not just one best group. For example, two particles with pass/guard responses (10,8,0) and (10,0,8) fail individually at c = 1.5, while their pooled response (20,8,8) succeeds. Adding another particle to an already successful pair cannot create a new minimal recipe. Requests are selected so that all six particles fail individually. In both splits, 20% of requests have no successful recipe, 40% have one or more two-particle recipes but no minimal three-particle recipe, and 40% have at least one minimal three-particle recipe. The last group can also contain two-particle recipes. These proportions concern complete requests, not the frequency of any candidate letter or particular answer string. | Request category | Train | Test | |---|---:|---:| | No successful recipe | 2,000 | 400 | | Minimal pairs only | 4,000 | 800 | | At least one minimal triple | 4,000 | 800 | Separation And Scope Particles are partitioned before any six-image request is constructed. Identical images under rotation or reflection, and identical measured spectra, are grouped together. Groups with identical image evidence but conflicting calibrated spectra are excluded. Every candidate and every auxiliary training measurement comes from its own split-local pool. The source does not supply acquisition-session or substrate identifiers. Consequently, this is held-out image-group evaluation, not a claim of generalization to unseen laboratories, microscopes, substrates, or acquisition days. Reuse within a split is explicit; 12,000 requests are not 72,000 independently recorded particles. Submission Format Write the final CSV to ./working/submission.csv. Required columns, in order, are case_id, minimal_recipes. Both are string columns; minimal_recipes contains a JSON array, not Python list syntax. | case_id | minimal_recipes | |---|---| | pool_8df90516ac2e870e7c501ea9 | ["A+B","C+E+F"] | | pool_e356bcc7109fabc403dda821 | [] | This is a format illustration, not a hidden answer. Preserve actual IDs from test.csv. Use a CSV library to quote the JSON field correctly. Each recipe uses one to three distinct letters from A through F, joined by + in alphabetical order. Sort the recipe strings lexicographically and do not repeat a recipe. No submitted recipe may be a proper subset of another submitted recipe. The parser allows at most 20 recipes and at most 256 characters for the complete JSON string, including whitespace. The current constructed cases have no single-particle solution, but the parser accepts the general one-to-three-particle grammar. Missing or extra rows, duplicate IDs, unknown IDs, duplicate columns, extra columns, or reordered columns reject the entire submission. Row order can differ because IDs are used for alignment. The submission schema must exactly match the evaluator's answer schema. Malformed recipe values receive the penalties specified below rather than being silently repaired. Evaluation The Spectral Pooling Family Score measures recovery of the complete family of minimal recipes. Minimum score: 0.0. Maximum score: 1.0. Higher is better. Score = 0.60 * MicroRecipeF1 + 0.25 * MeanRequestF1 + 0.15 * CompleteRequestAccuracy. For request i, let Y_i be the true set of recipe strings and Q_i be the submitted set. Matching requires the exact same candidate subset, not overlapping candidate letters. Define TP_i = |Y_i intersect Q_i|, FP_i = |Q_i minus Y_i|, and FN_i = |Y_i minus Q_i|. | Component | Complete definition | Weight rationale | |---|---|---| | MicroRecipeF1 | Sum TP, FP, and FN across all requests, then compute 2TP / (2TP+FP+FN). If the denominator is zero, the component is 1. | 60% rewards the recovery of valid recipes and penalizes invented ones; no-solution cases cannot dominate this term merely by being empty. | | MeanRequestF1 | For each request compute 2TP_i / (2TP_i+FP_i+FN_i), taking 1 when both families are empty. Average over all evaluated requests. | 25% gives small and large recipe families equal per-request influence. | | CompleteRequestAccuracy | sum_i indicator(Q_i = Y_i) / number_of_requests. | 15% rewards supplying the entire usable family without making the score mostly all-or-nothing. | A malformed recipe value contributes zero to its request F1 and exact-match term, 20 false positives to the micro term, and one false negative for every true recipe in that request. Twenty is the maximum legal family size. Invalid hidden labels raise an evaluator error; they are never clipped or repaired. The empty prediction [] is valid. It receives perfect per-request credit only for a genuinely empty answer and misses every true recipe otherwise. Predictions that list all possible pairs are also syntactically valid, but their false positives reduce both F1 components. Why This Task Recognizing a particle's shape or selecting the individually brightest particle is insufficient. All candidates already fail the requested contrast individually. The useful signal is complementarity: the same response can be helpful under one pass/guard choice and harmful under another. A model must learn image-to-spectrum relationships and carry their uncertainty into a small set-selection problem. What Not To Use Image encoders, training-spectra supervision, calibrated surrogate models, ensembles, and deterministic subset enumeration are allowed. No natural-language explanation is graded. A recipe decoder alone cannot recover the unobserved spectral responses from the request text. Do not retrieve or match original source records, source-trained published weights, or their annotations to recover test spectra. Do not build answer lookups from IDs, row order, filenames, hashes, encoded file sizes, repeated assets, or leaderboard probing. Training on the supplied auxiliary measurements is allowed; importing an external checkpoint trained on these specific held-out observations is not. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The maximum end-to-end runtime is 1.5 hours, including data loading, training or adaptation, inference, structured decoding, validation, and submission writing.
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Reading Handwritten Entries With Ditto References

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76hg1fcd95kakk1v9n4zfqax8e15bj
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat jesuisnadi's score of 0.476!

Full challenge description from page:

> Overview Predict the ten written fields of a historical table row, expanding explicit ditto marks from earlier rows when the supplied evidence permits it. Also identify which earlier row supplies each expanded value. This combines handwriting recognition with reference resolution: recognizing a quotation mark is not the same as recovering the entry it stands for. The images are real grayscale scans of handwritten population-census tables. Record keepers often repeated a value using a shorthand mark instead of writing it again. An isolated row recognizer can read the visible ink yet produce an unusable record by leaving a resolvable reference unexplained, or by copying across a blank cell. Each case therefore supplies the current row and up to six preceding row images from the same table page. Human transcriptions provide the literal cell contents. A deliberately narrow, fully specified editorial rule expands six recognized forms of ditto notation. It does not infer historical identities, modernize names, complete uncertain words, or interpret every possible abbreviation. The goal is a faithful machine-readable entry with a traceable copy source, not a claim about the people recorded in the register. Dataset | File | Contents | |---|---| | train.csv | Exactly case_id,row_path,preceding_rows,resolved_cells,copy_links. | | test.csv | Exactly case_id,row_path,preceding_rows. | | sample_submission.csv | Exactly case_id,resolved_cells,copy_links, populated with complete target pairs sampled from training rows. | | images/ | Grayscale PNG row images, 1800 pixels wide by 160 pixels high. Different episodes may reference the same preceding row. | Paths such as images/line_837040613469490c0c83ef07.png are relative to the public directory. Each image contains one long handwritten table row, resized without changing its aspect ratio and placed on white padding. Table ruling, handwritten marks, variable spacing, faded ink, and blank cells remain visible. Canvas size is constant; text is not re-rendered from its transcription. One RGB-encoded source row is converted to grayscale using standard luminance weights; the remaining source rows are already grayscale. A valid private ancillary PNG chunk fixes each file at 300,000 bytes without altering its pixels or adding visible marks. The source table has ten cell positions, here referred to simply as C1 through C10 from left to right. These are positional slots, not ten language-independent semantic classes. The task preserves source field order and wording rather than guessing missing demographic information. The publisher's multi-writer partition is retained: original training writers supply training cases, and original validation/test writers supply hidden cases. All preceding rows come from the same page and split as their query. No preceding-row transcription is supplied at inference. Structural filtering excludes rows that do not have exactly ten bounded cells. Exact-pixel split checks run before outputs are written. | Quantity | Training | Test | |---|---|---| | Cases and distinct current-row images | 3,835 | 958 | | Writers | 64 | 16 | | Table pages | 128 | 32 | | Cases with at least one expanded cell | 854 | 161 | | Expanded cells | 1,052 | 191 | | Cases with all six preceding rows | 3,060 | 763 | | Cases with no preceding row | 130 | 33 | There are 4,793 distinct PNGs in images/; images used as preceding context are references to these files, not duplicated copies. Seven structurally invalid rows are excluded from the original 4,800-row collection. No writer, page, or exact decoded image is shared between training and test. The test contains about 25% as many cases as training; rows from the same page are related observations, not independent writers. Fields | Column | Data type | Meaning | |---|---|---| | case_id | string | Opaque entry_ identifier followed by 24 lowercase hexadecimal characters. | | row_path | string | Relative path to the current row image. | | preceding_rows | JSON-encoded string containing an array of zero to six strings | Image paths in nearest-first order. Element 0 is the immediately preceding supplied row, element 1 the next earlier row, and so on. | | resolved_cells | JSON-encoded string containing an array of ten strings | Literal or expanded cell values in C1-to-C10 order. Each string has 1 to 128 Unicode characters. | | copy_links | JSON-encoded string containing an array of ten integers | For each cell, 0 means no expansion; 1 to 6 is the one-based position in preceding_rows of the concrete value that was copied. | The source uses ¤ for a blank cell. ? and ! describe writing above or below the normal baseline and remain literal transcription characters. They are not generic uncertainty outputs. Transcription strings use Unicode NFC; runs of whitespace collapse to one space, and leading/trailing whitespace is removed. Case, accents, punctuation, spelling, and non-whitespace characters remain significant. Exact Expansion Rule A whole cell is a recognized ditto mark only if its normalized content equals one of ", "", d°, D°, idem, or Idem. For such a cell, inspect the same column in each supplied preceding row, nearest first. Skip further recognized ditto marks. Copy the first concrete, nonblank value encountered, and record that row's distance. A blank ¤ terminates the search. If no concrete value is reached, keep the literal ditto mark and use link 0. All non-ditto cells remain literal with link 0. There is no cross-column or cross-page copying. Marks containing extra characters are literal under this contract. A missing or structurally invalid preceding row ends the supplied context; the task never jumps over it using unseen evidence. If a chain of marks ends at the third preceding row, the link is 3, not the distance to the first intervening mark. For a C1 example, suppose the current cell is ", the nearest preceding cell is d°, and the second preceding cell is Martin. The resolved value is Martin with link 2. If the nearest preceding cell instead is ¤, the answer remains " with link 0, even if an older row contains Martin. Reference Distances Counts below are cells, not cases. All distance codes 0 through 6 are valid; code 6 occurs in training but not in this test split. A valid reference must point to an image actually supplied for that case. | Copy distance | Training cells | Test cells | |---|---|---| | 0: literal or unresolved | 37,298 | 9,389 | | 1 | 688 | 134 | | 2 | 231 | 42 | | 3 | 91 | 9 | | 4 | 29 | 5 | | 5 | 8 | 1 | | 6 | 5 | 0 | Labeled Example This record is present in train.csv. Its six preceding images are supplied nearest first; the C1 expansion uses the third image. All other fields are literal. The ! in C10 is retained as an annotation marker. | Field | Value | |---|---| | case_id | entry_173194c5d9df0596acc6722f | | row_path | images/line_40086c14d48df2d04d4b6f30.png | | preceding_rows | ["images/line_e65dc8fb676685062dd68c5e.png","images/line_14c5924c96b0c2439d04766d.png","images/line_08abd6fd5348431db060aab1.png","images/line_c63bd430376cc9f3dd373d66.png","images/line_870e586993616800ee44bace.png","images/line_82e3812f0e7e491332fc6b61.png"] | | resolved_cells | ["Delelaux","Henri","08","I & Loire","¤","¤","f","¤","E samaritaine","!18399"] | | copy_links | [3,0,0,0,0,0,0,0,0,0] | Submission Format Write ./working/submission.csv with exactly case_id,resolved_cells,copy_links, in that order. Both target columns must be strings containing valid JSON, not Python list syntax. Use exactly one row for each test ID. | case_id | resolved_cells | copy_links | |---|---|---| | entry_837040613469490c0c83ef07 | ["Martin","Jeanne","87","Paris","¤","C","ch","¤","s p","22408"] | [2,0,0,0,0,0,1,0,0,0] | This is an illustrative format example, not a hidden record. The links indicate that C1 was copied from the second preceding row and C7 from the first. Ordinary CSV quoting is required around JSON strings containing commas and double quotes. resolved_cells has a maximum serialized length of 9,000 characters; copy_links has a maximum of 100 characters. Every link is an integer from 0 to 6; booleans, decimal-valued JSON numbers, and numeric strings are invalid link values. Arrays must contain exactly ten elements. Content strings must meet the length and normalization requirements above. Extra/missing rows, duplicate/unknown/blank IDs, and extra/missing/reordered/duplicate columns reject the submission. Row order may change because matching uses IDs. An invalid content array earns zero content and field-exact credit for that case. Invalid link arrays lose every true link in that case and add ten false link predictions. Hidden annotations that violate the contract raise an evaluator error rather than being corrected during scoring. Evaluation The Reference-Preserving Transcription Score is 0.45 * ContentScore + 0.20 * FieldExactScore + 0.35 * CopyScore. Minimum score: 0.0. Maximum score: 1.0. Higher is better. Each term is calculated as follows before the weighted sum is taken. For an evaluated case, let y_j and p_j be the true and submitted string in cell j. Active cells are all positions except those where both strings are the blank marker ¤. This includes a false nonblank prediction in a truly blank cell, and a false blank prediction in a nonblank cell. Blank-on-blank positions do not inflate transcription accuracy. ContentScore: 45% For each active cell, calculate 1 - D(y_j,p_j)/max(len(y_j),len(p_j)), where D is character-level Levenshtein distance with insertion, deletion, and substitution cost 1. Characters are Unicode code points, not words or bytes. Average over active cells to obtain a case score, then average over all evaluated cases. If an entire valid case has no active cells, its content score is 1. A malformed array scores 0 for that case. This largest term gives graded credit for accurate reading without requiring a perfect row for any reward. It does not use an LLM judge or a semantic paraphrase score. FieldExactScore: 20% For each valid case, average 1[y_j = p_j] over the same active cells. A valid all-blank case scores 1; a malformed content array scores 0. Average these case scores over the evaluated set. The 20% weight rewards fields that can be used without correction, while keeping near-correct handwriting recognition useful. CopyScore: 35% A positive reference is the ordered pair (cell_index, preceding_row_distance) for a nonzero link. Within each case, an exact pair match is a true positive. A predicted pair absent from the true set is a false positive; a true pair absent from the prediction is a false negative. Aggregate TP, FP, and FN over all evaluated cases, without matching references between different cases. Then CopyScore = 2*TP/(2*TP+FP+FN). If all three totals are zero, CopyScore is 1. A wrong nonzero distance creates both one false positive and one false negative. Invalid arrays add ten false positives and all true references as false negatives. The 35% weight makes reference resolution a substantive part of the benchmark rather than incidental OCR postprocessing. Zero links are not scored as positive matches, so a mostly literal corpus does not make an all-zero link predictor look successful. What Not To Use Handwriting models, language models, visual attention across preceding rows, and deterministic implementation of the stated expansion rule are allowed. Use training supervision to learn visual transcription and notation; no model is required to invent a different editorial policy. Do not recover source annotations through image fingerprints, source filename databases, or external register indexes. Do not transfer hidden answers from repeated media, use identifiers or file size as label lookups, reconstruct answers by leaderboard probing, or exploit parser failures. A shared preceding-row image may legitimately be encoded once and reused within its supplied split. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The maximum end-to-end runtime is 1.5 hours, including data loading, training or adaptation, inference, structured decoding, validation, and submission writing. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Aerial Multimodal Scene Composition Grids

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cvmyd8kkt4yfwqcbakmx80d8dse5f
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat hoang_phuc_6868's score of 0.622!

Full challenge description from page:

> Aerial Multimodal Scene Composition Grids Overview Aerial views of urban road scenes are captured simultaneously by a colour (RGB) camera and a thermal-infrared (TIR) camera. Each scene carries a dense semantic labelling in which every pixel belongs to one of nine categories. Your task is to describe the *semantic layout* of each scene at the resolution of a fixed grid: the image is divided into a 16×16 array of 256 cells, and for every cell you must predict the class composition of that cell — the fraction of the cell's pixels belonging to each of the nine classes, expressed as a 9-way probability distribution. The collection includes daytime and nighttime scenes, including low-information colour images and degraded thermal images. Spatially constant colour images were excluded during preparation; the retained colour images are not all-black. Both channels are provided for every scene because their information quality varies. The scenes are also strongly imbalanced — road and tree pixels dominate, while pedestrians, motorcycles, and traffic facilities are rare — and they share a strong spatial layout prior (roads occupy the lower-central field of view). The metric measures each prediction against a per-cell positional-prior baseline and up-weights the rarer object classes — each of the eight object classes is weighted by the inverse square root of its frequency, with a floor so that a single near-absent class cannot dominate — so a prediction that matches the average spatial layout scores at the baseline, and the harder minority classes count for more than the abundant ones. Dataset Public files train.csv — one row per training scene: id, rgb_path, tir_path, lighting, and the 256 cell columns cell_000 … cell_255 holding the ground-truth composition of each cell. test.csv — one row per test scene: id, rgb_path, tir_path, lighting. No labels. train/rgb/, train/tir/, train/mask/ — training colour images, thermal images, and grayscale label masks (pixel values 0..8). Each training scene's mask is at train/mask/.png — the same ` as its rgb_path/tir_path` — so the pixel-level labels are available for training even though there is no mask_path column. test/rgb/, test/tir/ — test colour and thermal images (no masks). sample_submission.csv — a valid submission in the required format. Private files (organizer only) answers.csv — ground-truth cell compositions for the test scenes. Split and anti-memorization The collection contains 3,379 retained image pairs after image-quality filtering, exclusion of 26 frames at ambiguous telemetry date boundaries, and removal of cross-split near-duplicates (below). It has 2,831 training scenes and 548 test scenes; the test split contains 252 day and 296 night scenes. The split is grouped by capture session so that a model cannot win by memorising a near-identical training frame. The original thermal frames retain acquisition timestamps and, for later flights, GPS and camera telemetry. Preparation reconstructs each recording / flight from those fields — all frames of one acquisition day are kept together, and days are joined into one component when their GPS tracks overlap or a reviewed cross-date match establishes the same fixed viewpoint. Each connected component is one group_id and is assigned whole to either train or test (28 components: 17 train, 11 test), so every consecutive frame of a fixed viewpoint stays on the same side of the split. As a second safeguard, any test scene that is still a near-duplicate of a training scene on either modality (RGB or thermal) is removed, so no test scene has a near-twin in train. The partition is fixed and deterministic: the same train/test split is reproduced on every rebuild. The public and private leaderboard subsets are drawn by the platform from the test set. Column descriptions The public CSV columns are as follows: id (string) — unique scene identifier; also the basename of that scene's image files. rgb_path (string) — path to the scene's colour image (3-channel PNG) under public/. tir_path (string) — path to the scene's thermal-infrared image (3-channel false-colour PNG) under public/. lighting (string) — day or night, the capture condition of the scene. cell_000 … cell_255 (string) — one column per grid cell in row-major order (cell_{16*row + col}, row and col from 0 at the top-left). Each holds nine space-separated numbers, the class composition of that cell in class order unlabelled, road, building, motorcycle, car, truck, tree, human, traffic_facilities], summing to 1. In train.csv these are ground truth; in a submission they are your predicted distribution. The nine class ids are: 0 unlabelled, 1 road, 2 building, 3 motorcycle, 4 car, 5 truck, 6 tree, 7 human, 8 traffic_facilities. Data example A truncated test.csv row (cell columns are in train.csv / submissions): id,rgb_path,tir_path,lighting img_3f9a1c2b7d4e6a80,test/rgb/img_3f9a1c2b7d4e6a80.png,test/tir/img_3f9a1c2b7d4e6a80.png,night A single ground-truth cell value (nine space-separated fractions): 0.120000 0.540000 0.000000 0.000000 0.010000 0.000000 0.330000 0.000000 0.000000 Submission format A CSV with a header row and exactly one row per test scene. Columns, in order: id — the test scene id (every test id must appear exactly once; no extra ids). cell_000 … cell_255 — 256 columns, one per grid cell in row-major order. Each cell holds nine space-separated non-negative numbers giving your predicted class distribution for that cell, in the class order above. Each cell's nine numbers must sum to 1 (a tolerance of 0.02 is allowed; values are renormalised before scoring). Every cell must contain exactly nine values. The prediction width is fixed at 256 cells × 9 classes for every row. Sample submission id,cell_000,cell_001,...,cell_255 img_3f9a1c2b7d4e6a80,0.111111 0.111111 0.111111 0.111111 0.111111 0.111111 0.111111 0.111111 0.111111,0.111111 ... ,... The shipped sample_submission.csv predicts a uniform distribution in every cell of every scene — a valid but uninformative baseline. Evaluation Metric: difficulty-weighted per-class Brier skill over the positional prior. For each scene and each cell the true composition is a 9-way distribution t and the submission is a 9-way distribution p. Define the positional prior r as, for each cell position, the mean true composition of that cell across all test scenes (the best possible position-only, content-free prediction). For each scored class c we accumulate, over all test scenes and all 256 cells, the sum of squared errors of the submission and of the prior: SSE_pred[c] = sum over scenes, cells of (p[cell - tcell)^2 SSE_priorc] = sum over scenes, cells of (r[cell - tcell)^2 skill[c] = 1 - SSE_pred[c] / SSE_prior[c] # 0 if SSE_prior[c] == 0 The headline score is a frequency-weighted average of skill[c] over the **eight foreground classes** c ∈ {1..8} (road, building, motorcycle, car, truck, tree, human, traffic_facilities). Each class is weighted by the inverse square root of its frequency, so rarer (harder) classes count for more; classes rarer than a 1% floor are all treated as equally rare so that a single near-absent class cannot dominate or destabilize the score: freq[c] = mean composition mass of class c over all test cells # from the test set w[c] = max(freq[c], 0.01) ** (-0.5) # inverse-sqrt, rare floored score = sum( w[c] * skill[c] for c in 1..8 ) / sum( w[c] for c in 1..8 ) The unlabelled class (0) is part of every distribution but is not scored, mirroring the convention that unlabelled pixels are ignored in segmentation metrics. The score is clamped to the range [0.02, 1.0] (a small positive floor is applied so a valid submission never returns exactly 0). Interpretation of the scale: A submission that predicts the positional prior in every cell scores 0 (clamped to 0.02). Predicting a single constant distribution everywhere, or the uniform distribution, scores at or below 0 (clamped to the 0.02 floor). A perfect submission scores 1.0. Because the average up-weights the rarer object classes (motorcycle, car, truck, human, traffic_facilities), a submission that captures only the abundant road/tree/building classes is held well below 1; accuracy on the harder minority classes dominates the score. Higher is better. The random / content-free baseline (predicting the positional prior, or a uniform distribution) scores ≈0 (reported as the 0.02 floor). What Not To Use (Prohibited Methods) This challenge must be solved using only the provided images and their training labels. Do not use any external pre-computed segmentation masks, class maps, or pixel annotations for these scenes, or any external dataset of aerial urban traffic imagery, to recover or refine test-scene compositions. Do not attempt to match test images, thumbnails, or file hashes back to any external image collection, and do not use reverse-image search or any external index to identify a scene and look up its labels. Do not hardcode id-to-composition mappings, memorise per-id outputs, or otherwise encode test answers into the submission. Do not attempt to match a test scene to a visually near-duplicate training scene in order to copy that training scene's composition onto the test scene. Do not manually annotate, hand-label, or visually estimate the composition of test scenes. Do not train or tune against the private test labels in any way; all model selection must use the training split only. &nbsp;
> $700 Pool
> Closes in 4h 56m
> 8 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Segmenting the Bowel as One Tract

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74175zmhgdc9vz6yvshsbt618e2hh0
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat ammomahdavikia's score of 0.531!

Full challenge description from page:

> Segmenting the Bowel as One Tract Overview MR enterography photographs the small and large bowel of a patient with suspected inflammatory bowel disease. Reading one means saying not just where the bowel is, but which part of it: the stomach is not the duodenum, and the ascending colon is not the descending colon even though the two are indistinguishable in isolation. The digestive tract is a single continuous tube in a fixed order, and a reading is useful only if it respects that. A label that lands on the right voxels while leaving the tract in disconnected pieces has not traced anything. You are given abdominal MR volumes and must label every voxel as one of ten bowel segments or as background. Twelve patients arrive with a full segmentation. Sixty more arrive as images with nothing marked at all. Thirty are held out for scoring. Twelve is deliberate: segmenting a bowel study by hand takes a radiologist hours, so the method worth having is the one that works from a dozen of them while making something of the sixty that arrive unmarked. How you use that pool is yours to decide, whether by pseudo labelling, consistency training, self supervised pretraining on the images themselves, or not at all. The ten segments, label values 1 to 10 in order: stomach, duodenum, small intestine, appendix, cecum, ascending colon, transverse colon, descending colon, sigmoid colon, rectum. They are the same tissue at the same intensity. Nothing in the greyscale separates one from another; only position, continuity and the course of the tract do. Evaluation Submissions are scored using mean Dice over the ten segments, modulated by anatomical continuity, averaged over patients. Higher is better, and the score lies in 0 to 1. A class is present for a patient when at least one voxel carries it. Presence in the reference means presence in that patient's reference mask and nothing else. present in the reference and in your prediction: Dice is computed normally present in the reference, absent from your prediction: Dice 0 absent from the reference, present in your prediction: Dice 0, because inventing an organ is an error absent from both: skipped for that patient, so predicting no appendix for a patient who has none costs nothing Continuity asks whether consecutive segments that touch in the reference also touch in your prediction, and it asks this only of the voxels where your prediction and the reference agree. It cannot earn score on its own; it can only reduce, by at most half, a score that Dice already earned. Measuring it on the agreeing voxels is deliberate and it is what makes the factor mean something. Asked of the whole prediction, contact could be manufactured anywhere: a two voxel blob of every segment painted into an empty corner satisfies every pair in the chain at a Dice cost too small to notice. Asked of the agreeing voxels, a corner that overlaps nothing contributes nothing, and the only way to be credited with a join is to have found both segments where they actually are. CHAIN = ((1, 2), (2, 3), (3, 5), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10)) def evaluate(reference, prediction): """reference and prediction are label volumes, height by width by slices, with values 0 to 10. Returns the score for one patient.""" dice = [] for c in range(1, 11): a, b = (reference == c), (prediction == c) total = a.sum() + b.sum() if total == 0: continue # in neither: not this patient's question dice.append(2.0 * (a & b).sum() / total) if not dice: return 0.0 score = sum(dice) / len(dice) continuity is asked of the agreeing voxels, not of the whole prediction agree = {c: (reference == c) & (prediction == c) for c in range(1, 11)} pairs = hits = 0 for x, y in CHAIN: ra, rb = (reference == x), (reference == y) if not ra.any() or not rb.any() or not touches(ra, rb): continue # not an adjacency this reference has pairs += 1 if agree[x].any() and agree[y].any() and touches(agree[x], agree[y]): hits += 1 if pairs: score *= 0.5 + 0.5 * hits / pairs return score def touches(a, b): """Do two masks share a voxel or a voxel face?""" if (a & b).any(): return True for axis in range(3): lo = [slice(None)] * 3 hi = [slice(None)] * 3 lo[axis] = slice(1, None) hi[axis] = slice(0, -1) if (a[tuple(lo)] & b[tuple(hi)]).any(): return True if (a[tuple(hi)] & b[tuple(lo)]).any(): return True return False The chain runs stomach to duodenum to small intestine to cecum, with the appendix hanging off the cecum, then cecum to ascending to transverse to descending to sigmoid to rectum. Continuity is anchored on the reference rather than on textbook anatomy, so a reference that annotates two segments as separated does not penalise a submission that agrees with it. The final score is the mean of the per patient scores. Dataset Files in public/: train.csv, the twelve labelled patients train_masks.csv, their segmentation, one row per slice unlabeled.csv, sixty patients with no segmentation at all test.csv, the thirty patients you must submit for volumes/.npz, one file per patient, holding image, an int16 array shaped height by width by slices classes.json, the label value to segment name mapping sample_submission.csv, a valid submission that predicts background everywhere Columns in train.csv, unlabeled.csv and test.csv, which are identical: patient_id, string, an opaque identifier height, integer, rows in each slice, 264 to 360 width, integer, columns in each slice, 320 or 384 slices, integer, coronal slices in the volume, 27 to 31 spacing_x, float, millimetres per pixel down the rows spacing_y, float, millimetres per pixel across the columns spacing_z, float, millimetres between slices, much larger than in plane volume_file, string, the path to that patient's npz Columns in train_masks.csv: id, string, the slice identifier, formed as patient, slice number and geometry rle, string, that slice's label map, run length encoded Volumes differ in size and are not resampled, and the data is strongly anisotropic: slices are 4.8 mm apart while pixels are near 1.2 mm. What to do about that is part of the problem. Submission Submit a CSV file with the following format: ColumnTypeDescriptionidstringSlice identifier, copied from sample_submission.csvrlestringRun length encoding of that slice's label map, values 0 to 10 The encoding walks the slice in C order, row by row, left to right, alternating value and count. 0 1200 3 45 0 900 means 1200 background pixels, then 45 pixels of class 3, then 900 background. Requirements: One row per slice of every test patient, 836 in all. Copy the id values from sample_submission.csv rather than building them. Include header row. Counts must be positive whole numbers and must sum to the slice's height times width, which you can read from test.csv. A slice with nothing in it is 0 , never an empty string. What the grader does with anything else, stated exactly, because you should not have to guess: A duplicate id, an empty id, or a missing id or rle column rejects the whole submission. These are structural and the run stops there. A row whose encoding cannot be read is scored as if you predicted nothing on that slice. That covers counts that do not sum to the slice, an odd number of values, a label outside 0 to 10, a count that is not positive, and an empty string. You lose that slice, not the run. A slice you leave out is also scored as if you predicted nothing there. The row count above is what you should submit, not a trap: a short file still scores. An id the answers do not contain is ignored. Rows for slices outside the scored set cost nothing. What not to use Pretrained weights, stated exactly. Weights fitted to medical images of any kind are forbidden: TotalSegmentator, MRSegmentator, nnU-Net's released checkpoints, MedSAM, SAM and its variants, and any model zoo entry that has seen abdominal scans. Weights pretrained on ordinary photographs, ImageNet and COCO included, ARE allowed, and so is any architecture. The line is what the parameters have seen, not where they came from. No external data, and this rule is load bearing. These images are derived from a public deposit that also publishes the masks. Nothing in the construction stops someone matching a test image back to that deposit and reading off the answer, so the rule is what protects the benchmark. Retrieving the source dataset, searching for these images, and using any external medical imaging collection or published atlas all put a submission outside the task. The identifiers here are salted hashes and the acquisition metadata is stripped for the same reason. No general purpose segmentation services or APIs. Models above 8 billion parameters are out of scope. A nominal 7B measuring around 7.6B is fine. Forbidding medical pretrained weights is what keeps this a question about learning from twelve patients rather than about which checkpoint to download. Budget Your solution runs end to end on a single A10G with 24 GB, within a wall clock limit. It must run with no arguments, resolve its own input and output paths, and write a valid submission even if training fails or time runs out. Installing packages is not possible. &nbsp;
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Speckle Object Recovery Across Scattering Regimes

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7e1pkpxj8qg2wehkesm23ns58e27a1
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat infinitq's score of 0.731!

Full challenge description from page:

> Speckle Object Recovery Across Scattering Regimes Overview A camera looking at an object through a thin scattering layer - ground glass, a slice of tissue, a sheet of paper - records speckle: a field of bright and dark grains with no visible structure. The light field has not been destroyed, only scrambled. Over a limited range the scattering layer acts as a convolution, so the frame is the object convolved with a random point spread function that you do not know. You are given 6,396 training frames taken through 64 scattering layers, with the binary object that produced each frame. You must recover the object behind each of 1,200 test frames. Every test frame was taken through its own scattering layer, and not one of those 1,200 layers appears anywhere in the training set - there is no calibration frame, no reference beam and no repeated measurement to lean on, so nothing can be inferred about a kernel except from the single frame in front of you. The difficulty is not the unfamiliar layer, it is which of two regimes that layer is in. Half the corpus is isoplanatic: one point spread function covers the whole object, and the frame is exactly one convolution. The other half is not: the point spread function decorrelates across the field, so opposite corners of the object are imaged through effectively unrelated kernels and no single deconvolution or global correlation can undo it. The two halves are equal in size and which half a test frame belongs to is not disclosed, so a solution has to handle both without being told which it is looking at - and half of every score comes from the half that no single deconvolution can undo. Evaluation A prediction is a 32x32 binary object mask, submitted run-length encoded in a single column. It is compared to the true mask with an IoU maximised over every translation and over the 180-degree twin, and the score is the mean of that quantity over the 1,200 test rows. For one row, with prediction p and truth g decoded to 32x32 and zero-padded to 64x64: best = 0.0 for o in (g, g[::-1, ::-1]): # the object and its 180-degree twin for t in all_integer_shifts: # computed by FFT cross-correlation inter = (p * shift(o, t)).sum() union = p.sum() + o.sum() - inter best = max(best, inter / union if union > 0 else 0.0) row_score = best score = mean(row_score over all 1,200 test rows) Higher is better; 0 is the minimum and 1.0 is the maximum, reached only by an exact match on every row. The two regimes are present in exactly equal numbers, so half the score comes from each and no weighting is needed to make the harder half count. The two stratum names and the physical parameter that defines them are in public/strata.csv; which regime a given test frame belongs to is not published. Why this metric. A random phase screen has no defined origin and no defined handedness. An object at position u seen through kernel S and the same object at u + t seen through S shifted by -t produce the identical frame, so absolute position is not identifiable from a single measurement. The 180-degree twin is not identifiable either: replacing the object by its point reflection can be absorbed exactly into a phase modulation of the kernel, and a speckle kernel's statistics are unchanged by that. Both statements are properties of the measurement, not of any particular method. A pixelwise loss against a positioned mask would therefore score a quantity no valid method can recover, and would reward a model that has learned where objects tend to sit. Maximising over translation and over the twin removes exactly those two ambiguities and nothing else. Why a plain mean over rows. The isoplanatic half and the shift-variant half reward opposite treatment - anything that leans on a single global kernel helps on the first and hurts on the second - and 600 of the 1,200 test rows are the hard regime, so a solution that handles only the easy half is already capped near half the reference score. Keeping the score a per-row mean also keeps it free of any grouping, which means the public and private halves measure exactly the same quantity however the platform splits them, and every row is scored on its own terms. Dataset public/train.csv - 6,396 rows - and public/test.csv - 1,200 rows - carry the same two columns. | Column | Type | Description | | --- | --- | --- | | sample_id | string | Unique id, e.g. S000000. | | image | string | Path to the 96x96 8-bit camera frame, relative to public/. | public/train_labels.csv - 6,396 rows, one per training frame, joined on sample_id. | Column | Type | Description | | --- | --- | --- | | sample_id | string | Matches train.csv. | | mask | string | Path to the 32x32 binary object mask that produced the frame (0 or 255). | | diffuser_id | string | Which of the 64 training scattering layers formed the frame; about 100 rows share each. Group your validation split on this. | | stratum | string | wide (isoplanatic) or narrow (shift-variant). | | pupil_shift_per_object_px | float | The physical parameter behind the stratum: 0.0 for wide, 3.0 for narrow. | public/strata.csv - the two stratum definitions. public/sample_submission.csv - the required schema, filled with random values. Frames are in public/train/images/ and public/test/images/; training masks are in public/train/masks/. None of the train_labels.csv columns has a test counterpart - the stratum and the scattering layer of a test frame are deliberately withheld. Full physical description of how the frames were formed, the noise model, the object families and the stratum definitions: see the dataset description. Submission | Column | Type | Description | | --- | --- | --- | | sample_id | string | One row per test frame. | | mask_rle | string | The predicted 32x32 mask, run-length encoded (see below). Empty string for "no object anywhere". | The encoding. Flatten the 32x32 mask row-major - index row * 32 + col - and number the 1,024 pixels 1 .. 1024. Write space-separated start length pairs covering every run of set pixels, e.g. 114 5 145 7 176 9. An all-zero mask is the empty string. This is the usual segmentation convention, but note the row-major order: many Kaggle tasks use column-major, and the two are not interchangeable. def encode(mask): # mask: (32, 32) array of 0/1 flat = np.asarray(mask).reshape(-1) > 0.5 if not flat.any(): return "" padded = np.concatenate([[False], flat, [False]]) starts = np.flatnonzero(~padded[:-1] & padded[1:]) + 1 ends = np.flatnonzero(padded[:-1] & ~padded[1:]) + 1 return " ".join(f"{s} {e - s}" for s, e in zip(starts, ends)) Requirements Must contain exactly 1,200 rows, one per test sample, with sample_id matching test.csv exactly - no duplicates, none missing, none extra. Any of those three raises rather than scores. Must include a header row with sample_id and mask_rle. A missing column raises; column order does not matter and additional columns are ignored. Predictions are binary - a pixel is either in the mask or not. A malformed encoding raises: an odd number of values, a non-integer, a negative length, or a run falling outside 1 .. 1024. Row order does not matter; rows are matched by sample_id. Constraints A trained image model must do the work. This is a computer-vision task: the reconstruction must come from a convolutional or transformer model trained or fine-tuned inside your script. A tabular model applied to raw pixels is not an acceptable solution. Each test frame must be scored on its own. Your prediction for a test row must depend only on that row's frame and on what you learned from the training split. Estimating anything from the test set as a whole - pooled statistics, a shared kernel, clustering test frames, adapting to the test distribution - is not permitted, and would not survive contact with the setting anyway, since every test frame comes from a different scattering layer. Training and inference must both happen inside the submitted script, from the raw files, within the platform's runtime limit. The reference solution trains and predicts in well under it on the default GPU. &nbsp;
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Sentinel-1 Amazon Airstrip Footprint Tracing

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7938tqy1khtv2rtvxftrjff98e5mj8
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat ravi56's score of 0.305!

Full challenge description from page:

> Sentinel-1 Amazon Airstrip Footprint Tracing Overview Airstrip monitoring in the tropical Amazon is difficult because optical imagery is frequently obscured by cloud and narrow unpaved strips resemble other linear landscape features in SAR. This challenge asks you to trace the supplied candidate airstrip footprint in a single Sentinel-1 SAR tile. The output is a compact binary mask, not a confidence score or a point label. This challenge retains its float-valued SAR arrays, hides a geographic holdout, and uses an edge-aware footprint metric. The practical objective is to estimate the covered area and usable extent of a narrow strip well enough to prioritize remote-sensing review; it is not a certified geospatial measurement. The public training set contains 832 locations and the hidden test set contains 208 locations from a geographically disjoint source region. Each location appears once. No source coordinate, source identifier, geodata file, or hidden evaluator metadata is available as a model feature. Dataset File descriptions train.csv: 832 labeled development rows with the feature columns id and image_path. test.csv: 208 unlabeled holdout rows with exactly the same feature columns and order as train.csv. train_targets.csv: public training labels keyed by id; each finite integer target is the positive-pixel count of that row's supplied mask. masks/: 832 grayscale binary PNG masks keyed by the public training id; these are the full public segmentation targets and are not present for test IDs. images/: one .npz archive for every row in train.csv and test.csv. Load the array named image; it is float32 with shape (200, 200) and retains the source SAR intensity scale. sample_submission.csv: a valid non-constant example submission with one row per test id. Column descriptions id (string): opaque 16-character lowercase hexadecimal identifier; it has no geographic or semantic meaning. image_path (string): POSIX path relative to dataset/public, for example images/01927a9bb8941816.npz. target (integer): public training-only foreground-pixel count in train_targets.csv; the matching full mask is masks/.png. prediction (string): submission RLE mask in sample_submission.csv and the required output. Evaluation The grader decodes each prediction into a boolean 200×200 mask. RLE runs are one-indexed and row-major. The hidden truth is decoded with the same function. For one tile, let T be the truth mask and P be the prediction mask. The Footprint Fidelity Score is the weighted sum of pixel overlap, edge agreement, and footprint extent: import numpy as np HEIGHT = 200 WIDTH = 200 BOUNDARY_RADIUS = 2 def decode_rle(value): tokens = value.split() numbers = [int(token) for token in tokens] if numbers == [0, 0]: return np.zeros((HEIGHT, WIDTH), dtype=bool) flat = np.zeros(HEIGHT * WIDTH, dtype=bool) previous_end = 0 for start, length in zip(numbers[::2], numbers[1::2]): if start HEIGHT * WIDTH or start <= previous_end: raise ValueError("invalid RLE") flat[start - 1:start - 1 + length] = True previous_end = start + length - 1 return flat.reshape(HEIGHT, WIDTH) def dilate(mask, radius=BOUNDARY_RADIUS): result = np.zeros_like(mask, dtype=bool) for dy in range(-radius, radius + 1): for dx in range(-radius, radius + 1): y0, y1 = max(0, dy), min(HEIGHT, HEIGHT + dy) sy0, sy1 = max(0, -dy), min(HEIGHT, HEIGHT - dy) x0, x1 = max(0, dx), min(WIDTH, WIDTH + dx) sx0, sx1 = max(0, -dx), min(WIDTH, WIDTH - dx) result[y0:y1, x0:x1] |= mask[sy0:sy1, sx0:sx1] return result def erode(mask, radius=BOUNDARY_RADIUS): return dilate(mask, radius) def box(mask): ys, xs = np.nonzero(mask) if len(xs) == 0: return None return int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1) def box_iou(truth, prediction): truth_box, prediction_box = box(truth), box(prediction) if truth_box is None and prediction_box is None: return 1.0 if truth_box is None or prediction_box is None: return 0.0 left = max(truth_box[0], prediction_box[0]) top = max(truth_box[1], prediction_box[1]) right = min(truth_box[2], prediction_box[2]) bottom = min(truth_box[3], prediction_box[3]) intersection = max(0, right - left) * max(0, bottom - top) truth_area = (truth_box[2] - truth_box[0]) * (truth_box[3] - truth_box[1]) prediction_area = (prediction_box[2] - prediction_box[0]) * (prediction_box[3] - prediction_box[1]) union = truth_area + prediction_area - intersection return intersection / union if union else 0.0 def boundary_f1(truth, prediction): truth_boundary = truth & ~erode(truth) prediction_boundary = prediction & ~erode(prediction) if not truth_boundary.any() and not prediction_boundary.any(): return 1.0 if not truth_boundary.any() or not prediction_boundary.any(): return 0.0 truth_tolerance = dilate(truth_boundary) prediction_tolerance = dilate(prediction_boundary) precision = (prediction_boundary & truth_tolerance).sum() / prediction_boundary.sum() recall = (truth_boundary & prediction_tolerance).sum() / truth_boundary.sum() return 2.0 precision recall / (precision + recall) if precision + recall else 0.0 def frame_score(truth, prediction): denominator = truth.sum() + prediction.sum() dice = 2.0 * np.logical_and(truth, prediction).sum() / denominator if denominator else 1.0 return 0.55 dice + 0.30 boundary_f1(truth, prediction) + 0.15 * box_iou(truth, prediction) score = np.mean([frame_score(T, P) for T, P in zip(hidden_truth, hidden_predictions)]) The final score is the unweighted mean of frame_score over all 208 hidden locations. It is bounded in [0, 1], and higher is better. A two-pixel boundary tolerance reflects the narrow target and source mask/SAR registration uncertainty. A background-only prediction receives zero for every non-empty truth; a full-frame mask is penalized by Dice, boundary precision, and the enclosing-box term. Submission Submit one CSV with exactly these columns: id: every id from test.csv, exactly once. prediction: a row-major, one-indexed start length RLE string for a 200×200 binary mask; use 0 0 only for an empty mask. Example with real test IDs: id,prediction 01927a9bb8941816,18061 4 18262 8 02a976d80cc4c273,15312 2 15512 3 Requirements Match the column names and order exactly. Include every hidden test ID once, with no extra IDs or index column. Keep all RLE runs sorted, non-overlapping, positive-length, and within the 200×200 image bounds. Use deterministic preprocessing and a reproducible seed when fitting a model. What Not To Use Do not add fabricated images, masks, labels, negative scenes, or augmentation copies as a substitute for learning from the supplied real tiles. Do not use file order, public/test partition markers, or any metadata other than the public image arrays and public training targets as a prediction shortcut. Do not treat a prediction as operational evidence of illegal activity; the source labels and this benchmark are for research screening only. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Ghost Leaf Reunification

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73wz2tmzjgywwfa6f8xr8h7h89rb84
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat arin's score of 0.587!

Full challenge description from page:

> Ghost Leaf Reunification Overview Thin historical paper remembers both of its faces. Reverse-side ink, foxing, stains, fibers, and uneven illumination can leave related local frequency signatures after readable content and spatial layout have been removed. Each row contains eight shuffled false-color spectral panes made from the two sides of four different physical paper leaves. Recover the four hidden front/back pairings. There are no page numbers, side labels, document identifiers, filenames, or stable tile positions. Training and test rows come from disjoint physical-volume groups. A volume that contributes any training item contributes no test item. Evaluation Let A be the fraction of hidden undirected leaf pairs recovered across all test rows. A uniformly random perfect matching of eight tiles has expected pair accuracy 1/7. The score is max(0, (A - 1/7) / (6/7)). The score is bounded to [0,1]. A perfect submission scores exactly 1. A chance-level matching scores approximately 0. A malformed row recovers zero pairs but does not invalidate other structurally valid rows. Dataset train.csv contains id, asset_path, and pairing_json. test.csv contains id and asset_path. sample_submission.csv contains id and pairing_json. Each asset_path points to one RGB PNG in assets/. The image is a two-row by four-column contact sheet. Every 128 by 128 tile is one anonymous paper-side spectral pane; tile indices 0 through 7 follow row-major order. A pane is an independently shuffled 8 by 8 collection of local spectral microtiles. Local Fourier magnitude is retained, but text phase, microtile reading order, and continuous line edges are absent. Microtile orientations are also randomized independently for every pane. The channels have fixed meanings: Red represents local spectral energy from foreground ink and paper-side marks. Green emphasizes local spectral energy from moderate-strength and faint ink marks. Blue represents local spectral energy from the broad paper and illumination field after strong ink removal. Each training target is a JSON list of eight integers. At position i, the value is the tile index paired with tile i. A valid target is a self-free symmetric perfect matching. For example, if positions 2 and 6 are paired, entry 2 is 6 and entry 6 is 2. Submission Submit one CSV with exactly two columns in this order: id,pairing_json. Every test ID must appear exactly once. Row order may differ because grading aligns by ID. Requirements: pairing_json must be a JSON list of exactly eight integers. Every integer 0 through 7 must occur exactly once. No tile may pair with itself. Pairing must be symmetric: if entry i is j, entry j must be i. Booleans, strings, decimals, missing entries, duplicate indices, and values outside 0 through 7 are invalid. Wrong columns or column order, duplicate IDs, missing IDs, extra IDs, or unknown IDs invalidate the whole submission and raise a grading error. The values in sample_submission.csv are distinct invalid placeholders. Replace every placeholder before submission. Modeling Notes This is a set-matching problem, not an eight-way classification problem. Useful systems may encode spectral microtiles with a shared CNN or set encoder, aggregate each pane without assuming microtile position, score all 28 candidate pairs with cross-attention or distributional features, and decode the maximum-weight perfect matching. Joint row-level training is preferable to eight independent partner predictions because the output must satisfy a global one-to-one constraint. The available accelerator is an A10G GPU with a maximum runtime of 90 minutes. Difficulty is Medium. What Approaches Not to Use Do not use internet lookup, reverse-image search, external document collections, source-identification attempts, manual test labeling, OCR-based public-record reconstruction, or attempts to recover organizer-only page order or provenance. Build predictions only from the released train images, targets, and test images. Notes Ordinary bleed-through restoration begins with a known recto/verso pair and tries to clean or register it. Page-ordering tasks reconstruct a sequence. This challenge does neither: four unknown pairs are mixed into one row, readable-page appearance is replaced by shuffled phase-free spectral microtiles, and evaluation measures complete pairing generalization to unseen physical volumes. &nbsp;
> $700 Pool
> Closes in 4h 9m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Binding versus Diffusion from Nuclear Photobleaching Movies

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bdd5vy86jn6mp82fe5csqeh8e5cy7
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat osman0's score of 0.760!

Full challenge description from page:

> Binding versus Diffusion from Nuclear Photobleaching Movies Overview This is Computer Vision Challenge ! How long does a transcription factor stay on chromatin? What fraction of it is bound at any moment, and how fast does the rest diffuse? The standard way to ask a living cell is FRAP — fluorescence recovery after photobleaching. A laser destroys the fluorescence of a GFP-tagged protein inside a small spot of the nucleus, and a confocal microscope films the fluorescence coming back as unbleached molecules replace bleached ones. Turning that movie into kinetic parameters is a classic ill-posed inverse problem. A protein that binds briefly but diffuses slowly, and one that diffuses fast but binds for tens of seconds, can produce almost the same recovery curve in the bleach spot. What separates them is where fluorescence returns first (diffusion refills a spot from its edge inward; unbinding refills it everywhere at once) and how recovery changes with spot size (diffusion-limited recovery slows with the square of the spot radius; binding-limited recovery does not care). On top of that the nucleus is finite and irregular, nucleoli block diffusion, the bleach pulse takes time, and every image frame bleaches the sample a little more. You are given simulated confocal FRAP movies of 1,363 training cells from 70 protein constructs, with the true kinetics of every training cell, and must recover the kinetics of 615 test cells from 30 different constructs — together with how much you trust each estimate. Each construct contributes 16–24 cells, bleached with different spot radii, and you may analyse a construct's test cells together: how recovery scales with spot size across them is what separates binding from diffusion. The data is synthetic and generated by an exact, documented forward model (lattice reaction–diffusion inside an irregular nucleus → finite bleach pulse → imaging photobleaching → optics → camera). The ground truth is therefore exact. Task For each cell in test.csv, predict four kinetic parameters and a confidence: d_free_um2_s* — diffusion coefficient of the free (unbound) protein, in µm²/s. k_off_per_s* — dissociation rate from chromatin, in s⁻¹. The residence time is 1 / k_off. bound_fraction* — fraction of the mobile protein that is bound at equilibrium, k_on* / (k_on* + k_off). immobile_fraction* — fraction of all protein that never exchanges during the experiment. confidence* — how much you trust your estimates for that cell (only the ranking across cells is used). The model behind these definitions, per pixel of the nucleus: d(free)/dt = D ∇²(free) − k_on* · free + k_off · bound d(bound)/dt = k_on* · free − k_off · bound d(immobile)/dt = 0 with no-flux boundaries at the nuclear envelope and around nucleoli. Before the bleach every species is uniform and at equilibrium. Evaluation Submissions are scored with a composite in [0, 1]; higher is better. Per test cell i: TOL_D = 0.45 # decades: a 2.8x error in D scores zero for that term TOL_K = 0.60 # decades: a 4x error in k_off scores zero TOL_B = 0.30 # absolute error in bound_fraction TOL_M = 0.15 # absolute error in immobile_fraction sD = max(0, 1 - abs(log10(D_pred / D_true)) / TOL_D) sK = max(0, 1 - abs(log10(koff_pred / koff_true)) / TOL_K) sB = max(0, 1 - abs(b_pred - b_true) / TOL_B) sM = max(0, 1 - abs(m_pred - m_true) / TOL_M) s_i = 0.25 sD + 0.35 sK + 0.20 sB + 0.20 sM Rates are scored in log space because they span two orders of magnitude and a 2× error in a residence time means the same thing at 1 s as at 50 s. The four reported terms: S_cell* (weight 0.40) — mean(s_i) over all test cells. S_residence* (weight 0.20) — mean(sK) over test cells whose true bound_fraction ≥ 0.30, the cells where residence time is the biological read-out. S_worst* (weight 0.15) — mean of s_i over the lowest-scoring 25% of cells. A weakest-link term: cells you estimate badly cannot be averaged away by cells you estimate well. S_selective* (weight 0.25) — mean of s_i over the most-confident 25 / 50 / 75 / 100% of cells, averaged over the four cutoffs. score = 0.40 S_cell + 0.20 S_residence + 0.15 S_worst + 0.25 S_selective S_selective scores the ranking implied by your confidence column. Only the order matters — scale, sign and units are irrelevant. Cells sharing a confidence value are treated as exchangeable and given equal fractional weight, so a **constant or random confidence column makes S_selective exactly equal to S_cell**. It is never a free gain and never a penalty; only a ranking that genuinely tracks your own per-cell accuracy changes the score. Some parameters are physically unidentifiable in some cells (see Things you should know), so knowing which of your estimates are trustworthy is part of the task. import numpy as np def selective(s, confidence, cutoffs=(0.25, 0.5, 0.75, 1.0)): n = len(s) order = np.argsort(-confidence, kind="stable") s, c = s[order], confidence[order] groups = np.split(np.arange(n), np.flatnonzero(np.diff(c)) + 1) out = [] for cut in cutoffs: budget, acc = cut * n, 0.0 for g in groups: if budget <= 1e-12: break take = min(len(g), budget) acc += s[g].sum() * take / len(g) budget -= take out.append(acc / (cut * n)) return float(np.mean(out)) Dataset Everything lives under ./dataset/public/. public/ ├── train_movies.npy (1363, 48, 40, 40) uint16 209 MB ├── train_frame_times.npy (1363, 48) float32 ├── train.csv 1363 rows: protocol + the four targets ├── test_movies.npy (615, 48, 40, 40) uint16 94 MB ├── test_frame_times.npy (615, 48) float32 ├── test.csv 615 rows: protocol only ├── sample_submission.csv 615 rows in the required format ├── acquisition.json pixel size, PSF, frame structure, camera offset └── nucleus_shapes.npy (4000, 90) float32 real nuclear outlines used by the simulator Movies train_movies.npy, test_movies.npy) Axes: (cell, frame, row, col). Values: raw camera ADU as uint16, including a 100 ADU offset. Pixel size: 0.3 µm, so each 40 × 40 frame is a 12 × 12 µm field containing one nucleus. Frames: 3 pre-bleach, then 15 fast and 30 slow post-bleach frames. Row alignment: row k of _movies.npy and _frame_times.npy is the row with movie_index == k in the matching CSV. Frame times train_frame_times.npy, test_frame_times.npy) Acquisition time of every frame, in seconds. t = 0 is the end of the bleach pulse; pre-bleach frames have negative times. train.csv / test.csv movie_index* (int) — row in the matching array files. cell_id* (str) — unique cell identifier. construct_id* (str) — protein construct. Cells of one construct share kinetics up to cell-to-cell variation. Train and test share no constructs. bleach_x_px, bleach_y_px* (float) — nominal bleach-spot centre as column and row, with pixel centres at integer coordinates. bleach_radius_um* (float) — bleach spot radius, µm. bleach_duration_s* (float) — duration of the bleach pulse, s. dt_fast_s, dt_slow_s* (float) — fast and slow frame intervals, s. d_free_um2_s, k_off_per_s, bound_fraction, immobile_fraction* (float) — train only: the exact kinetic parameters of that cell. acquisition.json Pixel size, image size, frame structure, frame-time origin, PSF sigma, bleach-spot edge sigma, camera offset, array axis order and the bleach coordinate convention, in machine-readable form. nucleus_shapes.npy Shape: (4000, 90), float32. Content: each row is the outline of one real segmented nucleus (BBBC039, CC0) as a scale-free radial function: the distance from the centroid to the boundary at 90 equally spaced angles starting at −π, divided by sqrt(area / π). Use: the forward model draws every nucleus from this bank. It carries no information about any cell's kinetics, and it is provided so that simulated training data can use the same geometry distribution. How the movies were made The full forward model, with every range, is in the dataset description; in brief: Kinetics. Per construct: D log-uniform on 0.1–10 µm²/s, k_off log-uniform on 0.01–2 s⁻¹, bound_fraction uniform on 0.02–0.92, immobile_fraction exactly 0 with probability 0.35 and uniform on 0.03–0.40 otherwise. Each cell perturbs these lognormally D by σ = 0.15, k_off by 0.20, binding-site density by 0.30, immobile fraction by 0.25, in natural-log units). Nucleus. A real nuclear outline — one of 4,000 outlines of segmented U2OS nuclei from the BBBC039 image set (CC0), released as nucleus_shapes.npy — randomly rotated and mirrored and scaled to an area of 20–50 µm², with 0–3 simulated elliptical nucleoli that exclude the protein. All boundaries are no-flux. Bleach. A soft-edged laser spot (edge σ 0.35 µm) of the given radius, pointed at the nominal centre with a Gaussian pointing error of σ 0.15 µm per axis, bleaches every species for bleach_duration_s while diffusion and exchange keep running. Imaging. Every frame bleaches every species by the same factor exp(−α). α is unknown per cell: the total loss over the 48-frame recording is drawn uniformly from 13–54%, the range measured from real confocal FRAP recordings of a nuclear transcription factor (see the dataset description). Camera. Gaussian PSF (σ 0.25 µm), Poisson shot noise with brightness 12–250 photons per pixel, background 0.3–3 photons, gain 0.8–2.2 ADU per photon, Gaussian read noise 1–3.5 ADU, 100 ADU offset. Things you should know before modelling These are properties of the data, not hints about a particular solution. The nucleus mask is not given. It has to be found from the images; the pre-bleach frames show it clearly. Nucleoli appear as dark holes. The reservoir is finite. The bleach removes a sizeable part of all the fluorescent protein in the nucleus, so even a fully mobile protein does not recover to its pre-bleach intensity. Imaging photobleaching is always present and differs from cell to cell. It is uniform over the nucleus. The bleach is not instantaneous. For fast-diffusing proteins a large part of the bleached zone refills during the pulse, so the first post-bleach frame is already a partially recovered, broadened profile. The bleach spot is often near a boundary. In most cells the spot centre is within one spot radius of the nuclear envelope or a nucleolus. Spot size varies between cells of the same construct, as do bleach duration and frame timing. Some parameters are unidentifiable in some cells, and that is physical. If diffusion across the spot is faster than the first frame, only a lower bound on D is visible. If the residence time exceeds the length of the movie, only a lower bound on it is visible. When binding is strong and exchange fast, the recovery depends on D and bound_fraction mainly through D·(1 − bound_fraction). No amount of modelling recovers information that is not in the movie. Brightness varies 20-fold between cells, so noise does too. Prohibited methods Reading, reconstructing or inferring private/answers.csv by any means. Recovering test labels from the data generator. The dataset's generator is published with a fixed master seed. Re-running it with that seed, or obtaining the raw dataset, and matching test cells back to their generated parameters — by seed, by hash, by movie similarity or any other means — is cheating, not a solution. So is reading any raw-dataset file. Hard-coding or hand-labelling any test prediction, or keying predictions on cell_id, construct_id or movie_index values. Using construct_id as a categorical predictor. Test constructs never appear in training, so an identifier-keyed feature is noise at test time. Fitting to the test targets in any form, including iterative probing of the leaderboard score. Test-time and transductive learning on the test split, specifically: test-time augmentation (TTA); test-time normalisation, i.e. normalisation or calibration statistics computed from the test split rather than from the training data or from each movie on its own; pseudo-labelling of test cells; self-training on test cells; unsupervised or semi-supervised domain adaptation using the test split. Models must be fitted on train.csv / the training movies (plus any data you simulate yourself) and then applied to the test movies without further adaptation. External data or network access at run time. Libraries outside the Kaggle Python Docker image. Exceeding the 1hr 30-minute run-time budget. Submitting sample_submission.csv unchanged. Submission Write ./working/submission.csv with exactly 615 rows plus a header, and exactly these six columns: cell_id* (str) — from test.csv. d_free_um2_s* (float) — strictly positive. k_off_per_s* (float) — strictly positive. bound_fraction* (float) — must lie in [0, 1]. Values outside are rejected, not clipped. immobile_fraction* (float) — must lie in [0, 1]. Values outside are rejected, not clipped. confidence* (float) — any finite number; only the ranking is used. cell_id,d_free_um2_s,k_off_per_s,bound_fraction,immobile_fraction,confidence cell_00000,3.0,0.16,0.47,0.12,0.5 cell_00001,3.0,0.16,0.47,0.12,0.5 *(These are the first two rows of sample_submission.csv; the values are placeholder constants, not ground truth.)* The grader rejects a submission for: missing or unknown columns — extra columns are rejected rather than ignored, because the usual cause is a merge that carried a label-derived field along; duplicate or unrecognised cell_id values, or any cell_id of an unscored context cell; a row count other than 615; NaN, infinite or non-numeric values; a non-positive d_free_um2_s or k_off_per_s; a bound_fraction or immobile_fraction outside [0, 1]. These are physical fractions: an out-of-range value is a bug in the pipeline, so the grader rejects it rather than quietly clipping it into range. &nbsp;
> 3 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Video-Conditioned Bimanual Pose Completion under Latent World Gauge

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7154adcj4qf79t73tmpxb0598e9eva
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat nightmare's score of 92.712!

Full challenge description from page:

> This is a Computer Vision challenge for video-conditioned 3D hand-pose completion. The primary observation is a synchronized RGB video clip. Structured hand tracks and task text provide additional geometric and semantic context. The goal is to reconstruct the hidden motion of one hand during a bimanual manipulation. It is not a forecasting benchmark and it is not evaluated as generic time-series prediction. Overview Each example is a 64-frame RGB manipulation clip with synchronized left- and right-hand states. One hand is designated as the query hand. Its states are hidden over a central 24-frame interval, while the other hand remains observable throughout the clip. The query hand remains visible before and after the hidden interval. Participants predict the query-hand state at 12 requested locations inside the gap. Each predicted state contains a 3D position, a continuous rotation-6D orientation, and a gripper value. The benchmark rewards visual grounding, bimanual coordination, relative geometry, task understanding, and coherent completion of the missing action. Each clip is expressed under its own arbitrary world-coordinate gauge, so global coordinate memorization is unreliable. Inputs For each bridge, the model receives: a synchronized 64-frame RGB video clip; the complete counterpart-hand trajectory; the query-hand trajectory before and after the gap; validity and visibility masks; timestamps; the queried hand identity; a natural-language task description; the gap location and requested query offsets. The frame rate is 25 Hz. The hidden interval starts at zero-based frame 20 and has length 24, covering frames 20 through 43. Predictions are requested at offsets 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43. Several submission rows belong to the same bridge. They should be modeled together because the metric evaluates the shape of the completed motion as well as individual poses. State Representation A hand state contains ten continuous values: [x, y, z, rot6d_0, rot6d_1, rot6d_2, rot6d_3, rot6d_4, rot6d_5, gripper] The first three values are Cartesian position in meters. The next six values are the first two vectors of a continuous rotation-6D representation. The final value is the gripper state. The evaluator converts rotation-6D values to a proper rotation matrix with Gram-Schmidt orthogonalization. If the two supplied vectors are a and b, it computes u = a / ||a||, v = (b - (b dot u)u) / ||b - (b dot u)u||, w = u cross v, and forms the matrix with columns u, v, w. Predictions must be finite. A finite but degenerate predicted rotation receives the maximum angular error of pi radians for every affected comparison instead of invalidating the entire submission. Gold rotations are non-degenerate. Latent World Gauge Every bridge is transformed by its own fixed horizontal world rotation and 3D translation. Both hands and all frames within the bridge receive the same transformation, but unrelated bridges use different transformations. The vertical axis is retained. Conceptually, positions and orientations transform as p' = Gp + c and R' = GR, where G is a rotation about the vertical axis and G and c are constant within one bridge. As a result, absolute origins and horizontal headings are not consistent across examples. Relative hand geometry within a bridge remains meaningful. A natural representation is the query pose in the counterpart-hand frame. Why Video and Counterpart Motion Matter Endpoint interpolation is a useful baseline, but hidden actions can include curved paths, pauses, reversals, intermediate rotations, grasp changes, object contact, support, transfer, folding, opening, closing, and coordinated movement around a shared object. The RGB clip can reveal the manipulated object, contact state, hand roles, workspace geometry, and action phase. The complete counterpart trajectory supplies a moving geometric reference. The task description supplies a semantic prior but does not uniquely determine the missing pose. Public Files The public package contains train.csv, train_targets.csv, test.csv, sample_submission.csv, bridges/, and clips/. train.csv and test.csv Both feature files have exactly these columns: sample_id, bridge_id, episode_id, bridge_path, clip_path, query_hand, task_text, gap_start, gap_length, query_offset, query_offsets sample_id uniquely identifies one requested prediction. bridge_id groups the 12 requests from one clip. bridge_path and clip_path locate the synchronized structured and RGB inputs. query_offset identifies the requested frame. query_offsets lists all requested frames for the bridge. The evaluation feature file contains no prediction columns. train_targets.csv Training targets contain exactly: sample_id, x, y, z, rot6d_0, rot6d_1, rot6d_2, rot6d_3, rot6d_4, rot6d_5, gripper Join training targets to train.csv by sample_id. The requested frame remains available as the public query_offset feature in train.csv. Bridge files Each bridges/*.npz file contains: partner_state, shape [64,10]; partner_valid, shape [64,10]; query_state, shape [64,10]; query_valid, shape [64,10]; query_visible, shape [64]; timestamps_s, shape [64]. The public query state is zeroed and marked unavailable inside the hidden interval. The counterpart state remains visible throughout. Video clips Each clips/*.mp4 file contains the synchronized 64 RGB frames for its bridge. Video use is central to the Computer Vision framing, although participants may combine visual and structured encoders in any architecture. Submission Use sample_submission.csv as the exact schema. It contains: sample_id, x, y, z, rot6d_0, rot6d_1, rot6d_2, rot6d_3, rot6d_4, rot6d_5, gripper Keep every supplied sample_id unchanged and replace the ten prediction values. Every expected ID must appear exactly once. Row order may differ because the evaluator aligns by sample_id. Extra columns, missing IDs, duplicate IDs, unknown IDs, nonnumeric values, and non-finite values receive the evaluator floor. The private answers.csv begins with exactly the same columns, in exactly the same order, as sample_submission.csv. It may append private grouping and grading columns after that shared prefix. Those appended fields are not submission targets and must not be added by participants. Evaluation Evaluation combines absolute pose, counterpart-relative coordination, trajectory shape, and gripper reconstruction. All scales and aggregation rules are public below. For two rotations A and B, angular distance is d_R(A,B) = arccos(clip((trace(A^T B)-1)/2, -1, 1)). Absolute pose error For a bridge with K probes, E_abs = mean_t 0.5 * [(||p_hat_t-p_t|| / 0.04)^2 + (d_R(R_hat_t,R_t) / radians(15))^2]. The position scale is s_p_abs = 0.04 meters and the rotation scale is s_R_abs = radians(15). Counterpart-relative coordination error Let the counterpart pose at a probe be (p_t^C, R_t^C). Define query position and orientation relative to it as q_t = (R_t^C)^T(p_t-p_t^C) and Q_t = (R_t^C)^T R_t. Apply the same transformation to the prediction. E_coord = mean_t 0.5 * [(||q_hat_t-q_t|| / 0.03)^2 + (d_R(Q_hat_t,Q_t) / radians(12))^2]. The relative-position scale is s_p_coord = 0.03 meters and the relative-rotation scale is s_R_coord = radians(12). Trajectory-shape error For adjacent requested probes, compare position increments and relative rotation increments: E_shape = mean_t 0.5 * [(||(p_hat_{t+1}-p_hat_t)-(p_{t+1}-p_t)|| / 0.025)^2 + (d_R(R_hat_t^T R_hat_{t+1}, R_t^T R_{t+1}) / radians(10))^2]. The shape-position scale is s_p_shape = 0.025 meters and the shape-rotation scale is s_R_shape = radians(10). Gripper error E_grip = mean_t ((g_hat_t-g_t) / 0.10)^2. The gripper scale is s_g = 0.10. Combined bridge and leaderboard error For every bridge, E_bridge = 0.25 E_abs + 0.40 E_coord + 0.20 E_shape + 0.15 E_grip. Bridge errors are averaged within each private (task, query_hand) group. The resulting group errors are macro-averaged so common task families cannot dominate. Call this value E_macro. The leaderboard score is score = 100 / (1 + E_macro / 1.50). The score is clipped to [0.01,100]. A perfect prediction receives 100. Larger errors strictly reduce the score, while finite imperfect submissions retain visible partial credit instead of collapsing through exponential underflow. Grading is deterministic. Split Integrity Training and evaluation are separated by source episode. No episode contributes bridges to both partitions. The split is balanced where possible across task and queried-hand combinations. Participants constructing a local validation set should keep every bridge, and preferably every source episode, wholly within one partition. Dataset Limitations and Risks The benchmark is derived from a finite collection of recorded bimanual demonstrations. It does not represent every object, manipulation strategy, workspace, camera placement, operator, hand morphology, or failure mode found in real robotic or human manipulation. Performance should therefore be interpreted as completion accuracy on this benchmark distribution, not as evidence of unrestricted real-world manipulation competence. Task frequencies are not guaranteed to be uniform. Some task and queried-hand combinations may contain substantially more eligible bridges than others, and rare combinations may appear only in training. Macro-averaging by task and queried hand limits their influence on the leaderboard but does not create missing examples or eliminate representation imbalance. Aggregate scores may also conceal weaker performance on an individual task or hand side. Only source episodes with complete valid hand states and video frames can produce bridges. Within each eligible episode, preparation favors a window with comparatively non-linear or otherwise informative motion. This eligibility and difficulty selection can underrepresent tracking failures, static actions, short episodes, severe occlusion, unusual motion, and examples with incomplete annotations. Models trained on the released data may consequently be less reliable on those cases. Every bridge uses the same 64-frame duration, central 24-frame gap, 25 Hz sampling rate, and fixed set of 12 interior queries. The benchmark does not directly measure robustness to longer clips, gaps at sequence boundaries, variable-duration gaps, irregular sampling, missing counterpart motion, or arbitrary query density. The RGB clips come from the available synchronized observation camera and inherit its viewpoint, resolution, compression, lighting, and occlusion characteristics. Visual evidence may be ambiguous when a hand or manipulated object is hidden. The structured hand states originate from the source tracking system and may carry its calibration conventions and measurement noise even after validity filtering. The world-gauge augmentation changes horizontal heading and translation while preserving the vertical axis, temporal dynamics, relative hand geometry, task identity, and scene content. It prevents direct memorization of a universal horizontal origin or heading, but it does not synthesize new actions, viewpoints, objects, contact patterns, or full 3D camera orientations. Success under this augmentation therefore demonstrates robustness to the tested gauge family only, not invariance to every coordinate transformation or distribution shift. Because both hands in a bridge share one gauge, counterpart-relative representations are intentionally favored. Such representations can still fail when counterpart tracking is noisy or when the missing motion depends on object state that is only weakly visible. Participants should report validation results by task and queried hand where possible rather than relying only on one aggregate score. Compute and Method Constraints The intended execution environment provides one NVIDIA A10G GPU with approximately 24 GB of VRAM. A submission has a 90-minute end-to-end runtime limit. This limit includes loading the public data, preprocessing, model fitting or adaptation, video and trajectory inference, postprocessing, and writing the final submission file. Solutions must contain at least one learned machine-learning component that contributes materially to the predictions. The learned component may process video, structured hand states, task text, or a fusion of these inputs. Neural video encoders, pose encoders, multimodal models, and models trained or fine-tuned on the supplied training partition are permitted. Purely hand-written interpolation, fixed geometric heuristics, nearest-neighbor lookup, TF-IDF retrieval, or other fixed statistical rules may be used as auxiliary features or baselines, but they may not be the central prediction method. A submission whose predictions are produced primarily by those non-learned mechanisms is not admissible. Publicly available pretrained model weights are allowed when they were released before the competition, can be loaded and executed locally, and do not contain labels or hidden examples from this benchmark. Fine-tuning those models on the provided training data is allowed. Additional task-specific labeled data, private copies of the source episodes, hidden benchmark targets, and manually labeled evaluation clips are prohibited. General-purpose pretrained weights are not treated as additional task-specific labeled data. All computation must run inside the provided environment. Remote inference APIs, external model-serving endpoints, internet lookups during execution, and human-in-the-loop prediction are prohibited. Participants may cache computations within a run, but may not rely on results computed from private evaluation data outside the official run. CPU preprocessing and ordinary open-source libraries are allowed, subject to the same 90-minute total runtime and available system memory. No particular model architecture is required beyond the materially contributing learned component. Modeling Directions Useful approaches include video encoders, vision Transformers, 3D pose encoders, relative-hand representations, masked motion completion, endpoint-conditioned models, cross-attention between RGB and pose tracks, SE(3)-aware networks, and multimodal fusion with task text. A simple baseline interpolates between the visible query poses on either side of the gap. Stronger models should use the RGB evidence and counterpart motion to recover deviations that the endpoints cannot determine. Scope This benchmark evaluates Computer Vision models for completing occluded 3D hand motion in bimanual manipulation videos. It does not ask for action forecasting beyond the observed clip, force prediction, object reconstruction, or free-form text generation. The central question is: can a model use visual evidence and the complete bimanual context to reconstruct the pose of an occluded hand under an unfamiliar world gauge?
> 2 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Confirmed Methane Plume Footprints

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7453r9ta7nj7eykmffrs4nhh8e9s7y
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat poggerman's score of 0.645!

Full challenge description from page:

> Overview A methane retrieval maps the column concentration of methane over a patch of ground from the air. Every scene here already carries an apparent enhancement that a detection pass flagged. Some of those survived quality review and some did not. For each scene, return the pixels covered by a confirmed plume, and the empty set when the enhancement did not survive review. About 44% of scenes have the empty set as their answer, so deciding whether an enhancement is real carries as much of the score as outlining it does. The two scenes look alike: a plume that failed review is not a blank field, it is an enhancement that a reviewer judged to be something else. The retrieval is patchy. A pixel where the retrieval failed carries a reserved code rather than a concentration, the median scene is missing 3.3% of its pixels and the worst is missing 71.9%, and those gaps sit over cloud, water and dark ground where an enhancement would also be hardest to read. Evaluation The score pays two skills separately. For every test scene, the decision term is 1 when a submitted footprint is non-empty exactly where the true footprint is non-empty, and 0 otherwise. For the scenes that truly hold a plume, the delineation term is the Dice overlap of the submitted and true pixel sets: $$ \mathrm{Dice} = \frac{2\,|P \cap T|}{|P| + |T|} $$ The raw score is $$ 0.5 \cdot \overline{\text{decision}} + 0.5 \cdot \overline{\text{Dice}} $$ where the first mean runs over every test scene and the second only over the scenes with a plume. An all-empty submission already earns half the negative fraction, so the reported score removes that floor: $$ S = \mathrm{clip}\!\left(\frac{R - F}{1 - F},\ 0,\ 1\right) $$ Higher is better and the range is 0 to 1. The shipped sample_submission.csv answers no-plume everywhere and scores exactly 0; an exact submission scores 1. Reference points measured during authoring on held-out flight days, not on the scored partition: the all-no-plume submission 0.0000, and a from-scratch convolutional segmentation network 0.5761. That network finds 95% of the plumes and outlines them to a Dice of 0.56, and loses most of its score on unconfirmed scenes, where it still returns a footprint about half the time. Dataset 1,827 scenes from 70 flight days, split so that no flight day appears on both sides. Train: 1,447 scenes with their footprints. Test: 380 scenes from 16 other flight days. Confirmed and unconfirmed scenes are present in similar proportion on both sides, and every group holds both kinds. Files scenes/.png: one 16-bit grayscale PNG per scene, 672 × 672. train.csv: the training scenes with their footprints. test.csv: the test scenes. sample_submission.csv: the submission format, all empty. LICENSE.txt, ATTRIBUTION.txt, encoding.json. Columns sample_id (string): the scene. scene (string): the PNG path, relative to the dataset root. mask_rle (string, train.csv only): the footprint, run-length encoded. Reading a scene Stored pixels are unsigned 16-bit codes under one global affine map, identical for every scene: ppb = 1000.0 + 0.1556 * code The code 65535 means the retrieval is missing at that pixel and is not a concentration. Because the map is global, no per-scene statistic is disclosed by the encoding. The run-length encoding A footprint is a space-separated list of start length pairs over the row-major 672 × 672 grid, with start counted from 1. Runs must be disjoint and inside the grid; order does not matter. The single token no-plume means the scene holds no confirmed plume. sample_id,mask_rle scene_0123456789abcdef,12045 31 12717 44 scene_0123456789abcde0,no-plume Submission Submit a CSV file with exactly the two columns sample_id,mask_rle, one row for every test sample_id and no others. Requirements Exactly those two columns, in that order. Row order has no effect. Every test sample_id exactly once; no missing, duplicate or unknown identifier. Each value either no-plume or a valid run-length encoding as described above. A wrong or reordered column set, an empty table, or a missing, duplicate or unknown sample_id is reported as an error naming the fault. A row whose encoding cannot be decoded — an odd number of values, a non-integer, a non-positive length, a run outside the grid, or overlapping runs — scores as a wrong decision for that row alone, and the other rows are scored normally. Compute One A10G GPU, offline, about 90 minutes. What not to use These rules are specific to this challenge. External data of any kind. No other retrievals, emission inventories, facility registries, satellite imagery or plume catalogues, and no attempt to match a scene against an outside source. Pretrained weights of any kind. Train from scratch on the supplied scenes. Identification of the scenes. Do not try to work out the location, date, flight or facility a scene belongs to, or to look it up anywhere. Hand-entered answers. Every footprint must come from a model or algorithm that reads the supplied scenes. Notes Two properties shape the score. The decision half is all or nothing per scene, so a footprint placed on a scene that failed review costs the same as missing a real plume entirely, and a model tuned only for overlap will spend that half badly. The delineation half is measured only where a plume really is, so nothing is gained by outlining aggressively on scenes that have none. The footprints are review decisions about which enhancements to accept, not physical measurements of plume extent, and no emission rate, wind field or terrain accompanies a scene. Solving this does not establish performance on an operational emissions product.
> 1 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Trait-Matched Canopy Retrieval

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76k3p6cb4a16a01rh07qmqfn8ds5gb
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat samluu206's score of 0.367!

Full challenge description from page:

> Overview Select the candidate plants that match a reference plant on one architectural trait but differ on the other. Each query contains real color and reconstructed-height images for one reference and eight candidates. The request tells you which trait to preserve: growth habit or mainstem prominence. Return one set of candidate letters, or NO_MATCH if no candidate satisfies both conditions. Breeding researchers compare plants with similar overall architecture but a contrasting structural characteristic. This benchmark evaluates that visual screening step, not genetic matching or causal treatment selection. Matching both traits is not a contrast; differing in both does not preserve the requested characteristic. The images are 224 x 224 plot crops from aerial surveys of peanut breeding plants during a growing season. RGB shows canopy color, texture, soil and overall shape; the normalized surface-model image depicts reconstructed canopy-height structure. Height is derived by photogrammetry from RGB acquisition, not measured by an independent LiDAR sensor. The source acquisition used a UAV RGB camera at 30 m, with 80% forward/side overlap, in clear weather near solar noon. The released crops do not provide calibrated metric height arrays. Growth-habit and mainstem-prominence annotations come from the original released trait folders. They are not inferred from pixel thresholds for this challenge. All reference and candidate views are genuine: no counterfeit panels, synthetic defects, donor swaps or repair-response surfaces are used. Dataset | File | Contents | |---|---| | train.csv | 2,454 labeled queries. Columns: case_id,reference_path,gallery_paths,match_request,counterpart_set. | | test.csv | 350 queries. Columns: case_id,reference_path,gallery_paths,match_request. | | sample_submission.csv | Columns case_id,counterpart_set; one row per test ID. It predicts NO_MATCH everywhere and scores 0.075. | | validation_groups.csv | String case_id and integer validation_fold (0-4) for each training query. Split by these folds, not random query rows. | | plots/ | 1,168 compressed NPZ files. Each contains one real plant's RGB and height crops. Multiple queries intentionally reference the same file rather than store duplicate image copies. | Prepared public size is approximately 170.7 MB. There are 818 training plants and 350 held-out plants. Each training plant is the reference for three different galleries; each test plant is the reference once. Gallery plants recur across queries, so queries are not independent experiments. The 146 source plot IDs lacking one of the two annotations are excluded from this task; they are not assigned invented labels. A physical plot's two task-folder records are joined before splitting. Every reference and every gallery candidate belongs to its split-local pool. Training galleries additionally stay inside the reference's validation fold, so entire folds isolate every component plant. All eight gallery members are distinct and exclude the reference. Sampling is uniform without using the trait labels; gallery position and positive-set size are not fixed. The scientific class imbalance is retained rather than hidden through fabricated cases. Input Fields | Column | Type | Meaning | |---|---|---| | case_id | string | Opaque query identifier, used only to align submissions. | | reference_path | string | Relative NPZ path from the public root, such as plots/70e0088562eb27bfae0ccb10.npz. | | gallery_paths | JSON array encoded as a string | Exactly eight relative NPZ paths. Positions 0-7 correspond to local candidate letters A-H. Letters have no identity outside their query. | | match_request | categorical string | One of the two requests defined below. | Load NPZ files with numpy.load(path, allow_pickle=False). Keys rgb and height each contain a uint8 array of shape 224 x 224 x 3, with values 0-255. Even the height product is supplied as a three-channel image, not floating-point elevation. Both arrays receive the same deterministic rotation/reflection. No brightness modification, pixel replacement, cropping or resizing is added. Plot file names do not disclose source IDs or trait names. Selection Rule | Request | Candidate must satisfy | |---|---| | same_growth_different_stem | Same annotated growth-habit class as the reference, and a different mainstem-prominence class. | | same_stem_different_growth | Same annotated mainstem-prominence class as the reference, and a different growth-habit class. | The released growth concepts are bunch, spreading, spreading-and-bunch, mixed and prostrate. Mainstem prominence is apparent, somewhat apparent or not apparent. “Different” means unequal annotated class, not a minimum height difference or a better agricultural outcome. Some concepts are rare: there are only four jointly annotated prostrate plants. The two traits are correlated. A growth-only shortcut that assumes a fixed mainstem state is not a reliable substitute for comparing both traits. For example, under same_growth_different_stem, a bunch/not-apparent reference admits a bunch/apparent candidate, but rejects a bunch/not-apparent candidate and a spreading/apparent candidate. These labels explain the semantics; per-plant class labels are not supplied as public metadata. Training query answers provide relational supervision. Target And Distribution counterpart_set is a canonical string of all qualifying gallery letters, separated by | in alphabetical order. The empty set is exactly NO_MATCH. There is no ranking among equally qualifying candidates and no requirement that at least one qualifies. | Number selected | Train queries | Test queries | |---|---|---| | 0 | 984 | 155 | | 1 | 627 | 87 | | 2 | 355 | 61 | | 3 | 246 | 24 | | 4 | 134 | 17 | | 5 | 74 | 3 | | 6 | 27 | 2 | | 7 | 6 | 0 | | 8 | 1 | 1 | All set sizes 0-8 are valid, including seven even though no packaged test query currently has that size. The training request counts are 1,233 growth-preserving and 1,221 stem-preserving. Test counts are 181 and 169, respectively. Example labeled query: case_000dc56133528d27f2210eaa uses reference plots/70e0088562eb27bfae0ccb10.npz, request same_stem_different_growth, and target A|C|D|E|F|G. Read its eight candidate paths from the corresponding training row; these letters refer only to that row's gallery order. Submission Format Write ./working/submission.csv with exactly case_id,counterpart_set, in that column order. | Column | Type and constraints | |---|---| | case_id | String matching a test ID exactly; 1-64 characters, no surrounding whitespace. | | counterpart_set | String, at most 15 characters: NO_MATCH or distinct A-H letters in alphabetical order separated by |. | A valid example using the training record above is: | case_id | counterpart_set | |---|---| | case_000dc56133528d27f2210eaa | A\|C\|D\|E\|F\|G | The backslash escaping in the rendered Markdown table is not part of the submitted value. An equivalent CSV example is: Use actual test IDs in your submission. Exactly one row per test ID is required. Row order may vary. Extra, missing or reordered columns, duplicate column names, additional or missing rows, unknown IDs and duplicate IDs are rejected. The grader supports at most 100,000 rows. Malformed selection strings count as missing every valid candidate and selecting every invalid candidate, and receive an incorrect empty/nonempty decision. They do not become an empty set. Invalid hidden targets raise an error. There is no JSON parsing of submitted targets. Evaluation The Counterpart Retrieval Score is: Score = 0.85 * CandidateF05 + 0.15 * EmptyGalleryScore. Minimum score: 0.0. Maximum score: 1.0. Higher is better. Most credit measures which candidates qualify; the small second term measures recognizing when there are no valid candidates. An always-empty answer cannot earn candidate-retrieval credit when positive candidates exist. For query i, let T_i be the true set and P_i the predicted set. Define TP_i = |T_i intersect P_i|, FN_i = |T_i minus P_i| and FP_i = |P_i minus T_i|. Sum these counts over all evaluated queries to obtain TP, FN and FP. CandidateF05 = 1.25 * TP / (1.25 * TP + 0.25 * FN + FP). This is pooled set F-beta with beta 0.5, not an average of separate per-query scores. False selections cost four times as much as missed selections in the denominator: passing an unsuitable plant to a reviewer defeats the matched-contrast screen. Every query has eight candidates, and each candidate decision has equal weight. Correctly rejecting a negative does not increase TP. If the denominator is zero, all evaluated sets are correctly empty and CandidateF05 is 1. For EmptyGalleryScore, classify each query as empty (T_i has no members) or nonempty. The predicted class is empty exactly when P_i has no members. EmptyGalleryScore = mean of the recalls of the true empty and true nonempty query classes. Each class recall is the fraction of its queries whose predicted empty/nonempty class is correct. If one class is absent from the particular answer file evaluated, average only the present class. Both classes occur in the complete packaged test set. No hidden class-frequency weights are applied. A malformed submitted set is treated as missing every true candidate and selecting every false candidate for CandidateF05; its empty-gallery decision is always wrong. Thus malformed values cannot act as advantageous abstentions. Hidden malformed values raise an error instead. All arithmetic and class counts use only the evaluated answer file, so the same rules apply to validation folds and platform public/private slices. For example, truth A|B and prediction A contribute TP=1, FN=1, FP=0; their stand-alone candidate F0.5 is 1.25/1.50. Truth A|B and prediction A|C contribute TP=1, FN=1, FP=1, a lower 1.25/2.50. Both predictions correctly recognize that this gallery is nonempty. An all-NO_MATCH prediction scores 0.075 on the packaged test set: zero positive-retrieval credit and 0.5 balanced empty-gallery accuracy. Exact answers score 1.0. There is no constant-baseline subtraction, arbitrary exact-match multiplier, free-text comparison, or additional target serialization. Permitted Methods And Limits Train a pair-comparison or gallery-retrieval model using the public query labels. RGB encoders, height encoders, multimodal fine-tuning, metric learning, classical image features, and joint inference across unlabeled test queries are allowed. Precompute a plant embedding once and reuse it across galleries. Use the supplied validation folds to prevent a gallery plant from leaking into its reference fold's validation data. The independent plant count, not the number of pair comparisons or pixels, governs the amount of biological evidence available. What Not To Use Do not identify plots in an external source collection to retrieve their annotations. Do not use source filenames, source class folders, private provenance, hidden labels, identifier/hash lookup tables, row-order rules or packet-size rules as answer oracles. Do not exploit malformed submissions, share hidden answers, or use repeated leaderboard probing to recover labels. Opaque names and rotations do not technically prevent matching to a public upstream collection; the source-lookup prohibition remains necessary. These are image-derived screening recommendations, not causal controls or a validated breeding decision system. Phenotypic matching alone does not establish genetic equivalence, yield, disease resistance or treatment response. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The complete solution must finish within 90 minutes end to end, including data loading, preprocessing, feature extraction, training or adaptation, validation, inference, structured decoding and submission writing. This is a total execution limit, not a separate allowance for each stage. The platform may terminate execution at the limit; use elapsed-time checks and retain the best completed model so that a valid submission is written before the deadline. Start with a small end-to-end run and write a valid full-test submission early. Use a wall-clock timer from process start, avoid exhaustive searches and large ensembles, and reserve at least the final 10 minutes for inference and submission checks; increase this reserve if measured throughput requires it. Cache encoder outputs only while the encoder is frozen.
> 1 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Spatial Availability Envelope from Shelf Images

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx795sr2nxhmv3zk64n33wsnt98e1xz5
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat ravi56's score of 0.397!

Full challenge description from page:

> Spatial Availability Envelope from Shelf Images Overview You are given small RGB images of produce arranged in a retail shelf scene. Build an image-level spatial segmentation/counting model that predicts an availability envelope for each image: the total number of visible produce instances and how those instances are distributed over a 32 by 32 image grid. This output is intended for replenishment triage, where a reliable count and a compact micro-location summary are more useful than an expensive full-instance annotation for every camera frame. The target is deliberately lighter than a bounding-box or mask export, but the 32 by 32 grid retains fine shelf-slot locality instead of averaging neighboring items into one large cell. Each cell is four pixels wide and tall in the published view, so a model must learn both counting and precise centroid placement under changes in capture session, framing, lighting, and item appearance. The hidden test set contains 681 real images from complete capture components held separate from training; the evaluator also macro-averages seven hidden item groups so that a frequent appearance cannot dominate the result. Dataset File descriptions dataset/public/train_images/ — 1,306 real RGB shelf images for training. dataset/public/test_images/ — 681 real RGB shelf images for prediction. dataset/public/train.csv — Training rows with an image path and the target prediction. dataset/public/test.csv — Test rows with an image path but no target profile. dataset/public/sample_submission.csv — A schema-valid example submission with non-zero random profiles. Column descriptions dataset/public/train.csv contains: id — Unique string identifier for the image. IDs are opaque and must be copied exactly into the submission. image — Relative path to a 128 by 128 RGB image under dataset/public/. prediction — JSON string containing exactly count and zone_counts. count is a non-negative integer. zone_counts has 1,024 non-negative integers whose sum equals count. dataset/public/test.csv contains: id — Unique string identifier for the test image. image — Relative path to a 128 by 128 RGB image under dataset/public/. The 1,024 grid cells are row-major: cell index 32 * row + column, with both row and column ranging from 0 through 31. The cells partition the published 128 by 128 view, so each cell is 4 pixels wide and tall; use the row-major index rather than assuming a different coordinate convention. The hidden split keeps complete capture components and visually near-identical frames in the same side and does not place a component on both sides. Do not assume that neighboring rows in either CSV are independent observations. Evaluation groups and holdout components The seven macro groups are semantic item groups, one for each produce category represented in this benchmark: apple, carrot, cucumber, orange, pepper, potato, and tomato. The group label is an evaluator-only attribute: it is not a column in either public CSV and is not submitted. Both training and hidden test contain examples from all seven groups, so this is not an unseen-class recognition task; it tests profile prediction across item appearances. The preparation process builds visual/capture components from the original frames by connecting records from the same capture group, records with identical image bytes, or same-product records whose centered 32 by 32 RGB views have cosine similarity of at least 0.980. The RGB check closes near-duplicate scene leakage that a grayscale-only check can miss; the lower cutoff also absorbs the concrete same-product near-copy found at cosine 0.982160 during audit. It then selects whole components near 35% within each product-by-capture-regime stratum. This prevents a large processed stream from making one product's test set look artificially out of distribution. Where a regime has at least two independent components, both train and test retain that regime; a sole processed stream stays in training. This is a mixed generalization test: a replenishment model must transfer across complete capture streams and visual conditions, while also handling frames from regimes it has seen during training. Each complete visual component is assigned wholly to one side, and session identity is not a public feature. The final split has 141 visual components, with 65 components selected for test and 1,306 train / 681 test images; test rows by semantic item group are apple 129, carrot 90, cucumber 86, orange 92, pepper 90, potato 73, and tomato 121. Training covers every semantic group, and every product has substantial train and test coverage. The evaluator first averages row scores within each of the seven semantic groups, then averages those seven group means equally. This matches the intended replenishment use because performance must be reliable across all seven produce categories, while a row-weighted mean would allow frequent categories to dominate. The semantic groups are the seven produce categories and are present in both train and test; they define equal evaluation weighting rather than an unseen-class test. The visual/capture components define leakage-resistant generalization, and the solver does not need to predict the hidden group label. Evaluation This is a maximize task. Each prediction is parsed as (count, zone_counts). For one row, let t be the true count, p the predicted count, T be the binary 1,024-cell occupancy map, and P be the predicted binary occupancy map. The count component is count_score = max(0, 1 - abs(p - t) / max(1, t)). Because the target is quantized into 4-pixel cells, the spatial components use a narrow Gaussian smoothing before comparison. The kernel has standard deviation 0.5 grid cell (2 pixels) and radius 2 cells; it is zero-padded and renormalized so that the total mass is preserved at image edges. This gives a centroid in a neighboring cell partial credit without treating an 8-pixel displacement as correct. Let B(v) be this smoothed map and let O(v) be the same smoothing applied to the binary occupancy map of profile v. The soft occupancy component is soft_zone_f1 = 2 * sum_i(min(O(T)_i, O(P)_i)) / (sum_i(O(T)_i) + sum_i(O(P)_i)). When both occupancy maps are empty, soft_zone_f1 is 1. The smoothed intensity component is soft_zone_intensity = max(0, 1 - sum_i(abs(B(true_zone_counts)_i - B(predicted_zone_counts)_i)) / max(1, t + p)). The spatial component is spatial_score = 0.50 * soft_zone_f1 + 0.50 * soft_zone_intensity. This balance makes a prediction useful only when it identifies where stock is present and allocates the mass to the right micro-locations, while avoiding a cliff at cell boundaries; a broad or distant displacement still loses most of the spatial credit. The row score is row_score = 0.30 * count_score + 0.70 * spatial_score. Spatial accuracy receives the larger weight because a replenishment action sent to the wrong four-pixel shelf location is operationally worse than a small total-count error; the count component still rewards getting the total inventory right. The final score is the unweighted mean of the mean row scores for each of the seven hidden item groups. This macro-average prevents a model from scoring well by fitting only the most common visual group. The score is bounded in [0, 1], and higher is better. The evaluator rejects a submission if its columns, row count, or ID set is wrong; if a profile is not a JSON object with exactly the two required keys; if count is not an integer in [0, 64]; if zone_counts is not a list of 1,024 non-negative integers; or if the zone sum does not equal count. A true empty profile is valid, although the public test happens to contain at least one visible instance in every row. Complete metric code import json import numpy as np GRID_SIDE = 32 GRID_CELLS = GRID_SIDE * GRID_SIDE MAX_COUNT = 64 SMOOTH_SIGMA_CELLS = 0.5 SMOOTH_RADIUS = 2 SMOOTH_OFFSETS = np.arange(-SMOOTH_RADIUS, SMOOTH_RADIUS + 1, dtype=float) SMOOTH_KERNEL = np.exp(-0.5 * (SMOOTH_OFFSETS / SMOOTH_SIGMA_CELLS) ** 2) SMOOTH_KERNEL /= SMOOTH_KERNEL.sum() GROUPS = ("apple", "carrot", "cucumber", "orange", "pepper", "potato", "tomato") def parse_profile(value): parsed = json.loads(value) if not isinstance(parsed, dict) or set(parsed) != {"count", "zone_counts"}: raise ValueError("profile keys are invalid") count = parsed["count"] zones = parsed["zone_counts"] if not isinstance(count, int) or isinstance(count, bool) or not 0 0) for value in true_zones]) predicted_map = smooth_grid([int(value > 0) for value in predicted_zones]) denominator = float(true_map.sum() + predicted_map.sum()) if denominator == 0.0: return 1.0 overlap = float(np.minimum(true_map, predicted_map).sum()) return max(0.0, min(1.0, 2.0 * overlap / denominator)) def row_score(true_value, predicted_value): true_count, true_zones = true_value predicted_count, predicted_zones = predicted_value count_score = max(0.0, 1.0 - abs(predicted_count - true_count) / max(1, true_count)) soft_zone_f1 = soft_presence(true_zones, predicted_zones) true_map = smooth_grid(true_zones) predicted_map = smooth_grid(predicted_zones) soft_zone_intensity = max( 0.0, 1.0 - float(np.abs(true_map - predicted_map).sum()) / max(1, true_count + predicted_count), ) spatial_score = 0.50 * soft_zone_f1 + 0.50 * soft_zone_intensity return 0.30 * count_score + 0.70 * spatial_score def macro_score(true_values, predicted_values, groups): if not (len(true_values) == len(predicted_values) == len(groups)): raise ValueError("row counts do not match") by_group = {group: [] for group in GROUPS} for true_value, predicted_value, group in zip(true_values, predicted_values, groups): if group not in by_group: raise ValueError("unknown evaluator group") by_group[group].append(row_score(true_value, predicted_value)) if any(not values for values in by_group.values()): raise ValueError("every evaluator group needs at least one row") return sum(sum(values) / len(values) for values in by_group.values()) / len(GROUPS) The platform validates the submission header, exact row count, unique IDs, and exact test-ID set before calling this metric. It parses the solver's prediction values with parse_profile; true_values are decoded from the private answers, and groups are evaluator-only product labels. Neither the hidden group labels nor answer metadata are supplied to solvers. The final value returned by the grader is macro_score(true_values, predicted_values, groups). Submission Submission columns id — String copied from every row of dataset/public/test.csv; include each test ID exactly once. prediction — JSON string with exactly this shape: {"count": integer, "zone_counts": [1,024 integers]}. The 1,024 values must sum to count. The file must contain exactly 681 data rows plus the header, with no additional columns. A shortened valid example using the first test ID is: id,prediction AGI_0083937b7894ffd5,"{""count"":4,""zone_counts"":[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]}" Requirements Preserve the exact test ID set and row count. Emit valid JSON strings rather than Python dictionaries or lists. Keep the count and zone vector internally consistent on every row. Train from the labeled image/profile pairs in the public training files; the test profile is not supplied. What Not To Use Do not reverse-map an opaque id to a packaging filename, row number, or capture sequence. That would turn the holdout construction into a lookup problem instead of visual inference. Do not infer labels from image extensions, directory names, or filename ordering. Those fields are packaging details and are not intended to encode the profile. Do not add synthetic shelf frames or synthetic target profiles as benchmark examples. Standard label-preserving augmentation of real training images (such as flips, crops, or color jitter) is allowed when the image geometry and zone_counts are transformed consistently; the prohibition is on manufacturing extra labeled examples or targets. &nbsp;
> 0 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Auroral Episode Representation Transfer

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7be8j5qke0zg2s30sab9r1wx8drvcp
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview Train a model to recover a six-frame auroral episode hidden inside a ten-panel satellite montage. For every montage, predict the six panels in chronological order with their dominant bright sectors, a 5 x 4 matrix describing the five physical transitions, and the overall evolution regime. Ultraviolet space-weather instruments record long sequences of the northern auroral oval. During scientific review, timestamps or buffer indices can become detached while the image payloads remain available. A useful recovery model must recognize which views belong to one continuous episode, reject visually similar observations from elsewhere in the same day, and summarize how the arc changed. Each montage contains ten panels labeled A through J. Six panels are consecutive observations with no adjacent gap above 400 seconds. Four hard distractors come from other times on the same observation date and are selected for morphological similarity to the true episode. All ten panels share one random rotation or reflection, while independent translations, gain changes, noise, mild blur, and occasional scan-line loss imitate display and transmission variation. Ground truth chronology comes from acquisition timestamps before those timestamps are removed. Morphology labels are computed from the transformed measurement grids before display noise is added. The benchmark therefore evaluates transfer of learned auroral structure and temporal compatibility, not recovery of metadata. Dataset Files | Path | Contents | |---|---| | train.csv | 4,000 labeled montage cases. | | test.csv | 900 unlabeled cases from held-out observation dates. | | sample_submission.csv | Complete, schema-valid baseline predictions. | | aurora_montages/*.jpg | 4,900 distinct 1200 x 480 RGB JPEG montages. | train.csv contains case_id, aurora_montage_path, episode_path, morphology_delta_tensor, and evolution_regime, in that order. test.csv contains only case_id and aurora_montage_path. Columns | Column | Data type | Train | Test | Meaning | |---|---|---:|---:|---| | case_id | string | yes | yes | Opaque identifier used only for submission alignment. | | aurora_montage_path | relative path string | yes | yes | Location of the ten-panel evidence image. | | episode_path | canonical token sequence | yes | no | Six chronological panel labels, each paired with its dominant angular sector. | | morphology_delta_tensor | JSON integer matrix | yes | no | Five transition rows over four morphology measurements. | | evolution_regime | categorical string | yes | no | Overall structural behavior of the recovered episode. | Montage Layout Panels A through E occupy the top row from left to right. Panels F through J occupy the bottom row. Every panel is a 240 x 240 view of the same polar coordinate frame. The letter badge identifies only the local panel position and carries no time or class information. The ten panels use a shared viewing transform so spatial motion remains comparable across the montage. Their independent photometric changes prevent simple pixel subtraction from acting as a timestamp detector. Episode Path episode_path has exactly six unique tokens separated by >. One token follows @q. | Element | Valid values | Meaning | |---|---|---| | panel | A through J | Local montage panel label. | | sector | integers 0 through 7 | Angular sector with the greatest bright-arc energy. | Sector q0 begins at image-right. Sector numbers increase counterclockwise in 45-degree steps. A valid example is H@q2>C@q2>J@q3>A@q3>F@q4>D@q4. Morphology Delta Tensor The tensor has five rows, one for each adjacent transition in the six-panel path, and four columns: | Column index | Measurement | |---:|---| | 0 | Change in the number of active bright sectors. | | 1 | Change in the number of connected bright components. | | 2 | Quantized inward or outward movement of the intensity-weighted radial center. | | 3 | Quantized change in arc anisotropy, which distinguishes elongated arcs from more isotropic patches. | Every entry is an integer from -2 through 2. Positive values mean an increase, outward movement, or greater anisotropy. Negative values mean the opposite. Changes beyond the range are clipped during target construction. Evolution Regime | Value | Meaning | |---|---| | support_expansion | The five transition codes have a positive net change in active-sector support. | | support_contraction | The five transition codes have a negative net change in active-sector support. | | support_reversal | Net active-sector change is zero, but support both decreases and increases during the episode. | | coherent_drift | Net active-sector change is zero without both a decrease and an increase. | Generalization Split All target frames and distractors for one montage come from one observation date. The 46 dates are assigned to 37 training dates and nine test dates before montage construction. A source frame, decoded frame, or distractor pool cannot cross that boundary. The 4,900 montages are derived cases, not 4,900 independent satellite passes. Date-level separation prevents exact episode reuse, while same-day hard negatives keep each case locally realistic. Hash checks reject repeated source payloads, repeated complete montages, and decoded-frame overlap between the two date pools. Training regime frequencies are: | Regime | Training cases | |---|---:| | support_expansion | 1,067 | | support_contraction | 1,024 | | support_reversal | 864 | | coherent_drift | 1,045 | Learning Setup The intended solution adapts a pretrained high-resolution image representation to auroral morphology. A practical system can encode the ten panels, learn pairwise temporal compatibility, decode a constrained six-node path, and attach morphology heads to adjacent selected panels. At 1200 x 480 pixels, each case contains ten fine-grained measurement views and 90 directed panel-pair hypotheses. The complete pipeline must finish within 1.5 hours, including data loading, training, inference, validation, decoding, and submission generation. Submission Format Write the final file to ./working/submission.csv. It must contain exactly these columns in this order: case_id,episode_path,morphology_delta_tensor,evolution_regime | Column | Required serialization | |---|---| | case_id | Nonempty string copied from test.csv. | | episode_path | Six unique canonical tokens joined by >, at most 47 characters. | | morphology_delta_tensor | JSON 5 x 4 integer matrix, at most 160 characters. | | evolution_regime | One valid categorical value from the table above. | Example: | case_id | episode_path | morphology_delta_tensor | evolution_regime | |---|---|---|---| | aur_bdf1da45217330492d27 | H@q2>C@q2>J@q3>A@q3>F@q4>D@q4 | [[0,1,1,0],[-1,0,1,1],[1,-1,0,0],[0,1,-1,-1],[-1,0,0,1]] | support_reversal | The ID set, row count, column names, and column order must exactly match the hidden answer file. Duplicate IDs, missing rows, unknown IDs, reordered columns, or extra columns are rejected. If the backend adds a visibility column to the hidden answers, the submitted file must contain the same column in the same final position. Malformed target values receive zero for their component. Evaluation Submissions are scored with the Auroral Representation Transfer Score: Score = 0.55 * PathScore + 0.30 * TensorScore + 0.15 * RegimeScore Minimum score: 0.0. Maximum score: 1.0. Higher scores are better. Component scores are averaged over all hidden cases unless stated otherwise. PathScore For one case, panel_accuracy is the fraction of six positions containing the correct panel label. token_accuracy is the fraction containing both the correct panel and sector. row_path = 0.15 * panel_accuracy + 0.20 * token_accuracy + 0.65 * exact_path_match PathScore is the mean row_path. A malformed path receives zero. TensorScore Let Y[i,j] be the hidden tensor entry and P[i,j] the submitted entry. Set w[i,j] = 2.5 when Y[i,j] is nonzero and w[i,j] = 1.0 otherwise. weighted_agreement = sum(w[i,j] * I(Y[i,j] = P[i,j])) / sum(w[i,j]) row_tensor = 0.20 * weighted_agreement + 0.80 * I(P = Y) TensorScore is the mean row_tensor. A malformed, non-integer, out-of-range, or incorrectly shaped tensor receives zero. RegimeScore RegimeScore is balanced accuracy across the four regimes. For each regime, recall is the number of correctly predicted cases in that regime divided by its hidden frequency. The four recalls are averaged with equal weight. An invalid regime value is always incorrect. What Makes This Interesting This is not next-frame generation and not static aurora classification. The central object is a hidden episode assembled from an unordered local archive: the model must reject hard same-day decoys, recover chronology, preserve a board-relative coordinate system, and produce a compact physical transition certificate. A correct path is necessary but not sufficient because the tensor tests whether the learned representation preserves morphological change. What Not To Use Do not derive predictions from case IDs, CSV order, file names, JPEG byte size, hashes, or another packaging artifact. Do not reverse-match panels to external source files, timestamps, or lookup tables. Do not exploit repeated media, hidden-answer probes, malformed values, or leaderboard feedback as substitutes for learning from the supplied training montages.
> 0 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Cross-Tone Elicitation-Event Linking: Four-Way Corpus QC

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74wawmmdvtvyc8ked2trg6r18e7xzp
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat aneeshm44's score of 0.964!

Full challenge description from page:

> Cross-Tone Elicitation-Event Linking: Four-Way Corpus QC Overview Help a speech-corpus curator recover the correct companion recording after a tonal-contrast elicitation. Each episode has one real falling-tone anchor and four real level-tone candidates from the same speaker and lexical contrast family. Exactly one candidate was captured in the same elicitation repetition as the anchor; the other three belong to different repetitions of that same contrast family. The hidden acquisition-event relation is the target: it is not acoustic-nearest-neighbor search, speaker identification, tone classification, or lexical-family lookup. A useful system verifies continuity across the tone alternation before the pair is admitted to a balanced corpus or sent for manual audit. The hidden episodes use speakers absent from training, so the verifier must transfer elicitation-continuity evidence to new voices. Return a relevance score for every anchor/candidate row; within each four-row episode, the same-elicitation candidate should receive the highest score. This is a four-way corpus-provenance decision over paired tonal recordings, where the label represents membership in a shared acquisition event rather than a surface class. Dataset File descriptions train.csv -- 8,656 labeled-example inputs, representing 2,164 four-candidate training episodes, with columns id, audio_a_path, and audio_b_path. The target is supplied separately in train_targets.csv so train and test expose identical model-feature columns. train_targets.csv -- 8,656 public training labels with columns id and target. Its ids match train.csv exactly and do not occur in test.csv. test.csv -- 6,992 unlabeled-example inputs, representing 1,748 hidden four-candidate episodes, with the same three model-feature columns as train.csv. sample_submission.csv -- A valid 6,992-row submission with exact columns id,prediction and non-constant random probabilities. audio/ -- 7,852 real mono WAV files from the source release; the episode rows reference the recordings used by the alignment graph. Every filename is an opaque 12-character identifier followed by .wav. Column descriptions id (string) -- Opaque 12-character identifier for one anchor/candidate example. Copy it exactly into the submission; it has no semantic ordering. audio_a_path (string) -- Relative path from the public dataset directory to the falling-tone anchor WAV file. audio_b_path (string) -- Relative path from the public dataset directory to a level-tone candidate WAV file. target (integer, train_targets.csv only) -- Binary relevance label. 1 means the candidate is the level-tone recording from the same elicitation repetition index as the episode anchor; 0 means it is one of the three other repetitions from that same contrast family and speaker. prediction (float, submission only) -- A finite relevance score in 0, 1]; larger values should rank a candidate earlier in its four-candidate episode. Split and leakage control The hidden test is built from complete speaker groups, not from a random row split. Training uses speakers 1–7 and the hidden test uses speakers 8–10, giving three independent held-out voices. Only source speaker/contrast groups with at least four matched repetitions are included in the four-way episode graph. The hidden data contains 158 available speaker/contrast groups and 1,748 complete four-candidate episodes, totaling 6,992 rows; the training data contains 371 groups and 2,164 episodes. The raw source has some groups with fewer than four matched repetitions, and those groups are omitted from episodes rather than padded with duplicate candidates. Use both supplied waveforms as the primary inputs. The public CSVs do not provide speaker metadata, lexical text, source filenames, repetition numbers, tone tracks, source paths, episode ids, or handcrafted target proxies. Paths are relative to the directory containing the CSV files. The four rows of an episode share the same audio_a_path, so solvers can form episodes from the visible inputs without an extra grouping column; row order and id order carry no meaning. For each eligible falling-tone anchor, the preparation pairs the level-tone recording with the same source repetition index as the positive and the next three distinct available level-tone repetitions from that speaker and contrast family as negatives, wrapping within the group when necessary. The candidate rows are emitted through a deterministic per-episode permutation and then keyed by opaque ids. The hidden speaker split is disjoint at the waveform-file level, and no public WAV is shared between train and test. Evaluation Submissions are scored with Macro Elicitation-Continuity Mean Reciprocal Rank (EC-MRR@4), a maximize metric bounded in [0, 1]. The score averages one reciprocal rank per complete four-candidate episode, giving every held-out anchor equal weight. The private answers.csv uses the same external id,prediction schema as a submission; its normalized prediction payload privately encodes the evaluator-only episode index and binary relevance target. The following code is the complete scoring definition, including payload decoding, strict validation, tie handling, and the platform's optional visibility projection behavior. import numpy as np import pandas as pd REQUIRED_COLUMNS = ["id", "prediction"] OPTIONAL_ANSWER_COLUMN = "visibility" CANDIDATES_PER_QUERY = 4 EXPECTED_TEST_ROWS = 6992 EXPECTED_TEST_QUERIES = 1748 PAYLOAD_SCALE = 2 * EXPECTED_TEST_QUERIES def _valid_answer_columns(columns): if len(columns) == len(REQUIRED_COLUMNS): return set(columns) == set(REQUIRED_COLUMNS) return len(columns) == len(REQUIRED_COLUMNS) + 1 and set(columns) == set(REQUIRED_COLUMNS + [OPTIONAL_ANSWER_COLUMN]) def decode_answer_payload(value): numeric_value = float(value) if not np.isfinite(numeric_value): raise ValueError("answer payload must be finite") if numeric_value > 1.0: code = int(numeric_value) if code != numeric_value: raise ValueError("integer answer payload must be integral") else: if numeric_value 1e-6: raise ValueError("invalid normalized hidden answer payload") code = round(scaled) query_index, label = divmod(code, 2) if label not in {0, 1} or not 0 1)).any(): raise ValueError("predictions must be finite and in [0,1]") if OPTIONAL_ANSWER_COLUMN in answers.columns: visibility = answers[OPTIONAL_ANSWER_COLUMN].astype(str).str.lower() if not visibility.isin({"public", "private"}).all(): raise ValueError("answer visibility must be public or private") decoded = [decode_answer_payload(value) for value in answers["prediction"]] truth = pd.DataFrame(decoded, columns=["same_repetition", "query_index"]) truth.insert(0, "id", answer_ids.tolist()) predicted = pd.DataFrame({"id": submission_ids.tolist(), "prediction": probability}) scored = truth.merge(predicted, on="id", how="left", validate="one_to_one") allow_partial_queries = len(answers) != EXPECTED_TEST_ROWS query_scores = [] for query_index, query in scored.groupby("query_index", sort=True): labels = query["same_repetition"].to_numpy(dtype=int) if len(query) != CANDIDATES_PER_QUERY or int(labels.sum()) != 1: if allow_partial_queries: continue raise ValueError("each query must contain exactly four candidates and one positive") values = query["prediction"].to_numpy(dtype=float) positive_score = float(values[labels == 1) strictly_higher = int(np.sum(values > positive_score)) tied = int(np.sum(values == positive_score)) average_rank = strictly_higher + (tied + 1) / 2.0 query_scores.append(1.0 / average_rank) if not query_scores: raise ValueError("no complete queries are available to score") if not allow_partial_queries and len(query_scores) != EXPECTED_TEST_QUERIES: raise ValueError("unexpected complete query count") score = float(np.mean(query_scores)) if not np.isfinite(score) or not 0.0 <= score <= 1.0: raise ValueError("score is out of bounds") return score Rows are matched by id, so the metric is invariant to submission and answer row order. Within a complete episode, the positive candidate's rank is its average descending rank when ties occur; a constant score therefore receives 1 / 2.5 = 0.4, while a perfect ranker receives 1.0. Invalid ids, duplicate ids, non-finite values, values outside [0,1], missing rows, malformed hidden payloads, an unexpected complete query count, queries without exactly one positive, or an empty set of complete queries are rejected. The complete prepared answer set has 6,992 rows and 1,748 queries, and is checked strictly. If the platform validates a smaller public/private projection, with or without answer-only visibility metadata, incomplete four-row queries are omitted because their reciprocal rank is undefined; an empty projection is rejected. Submission Submit one UTF-8 CSV with exactly one relevance score for every row in test.csv. The four rows sharing an audio_a_path form one candidate list; no separate query column is required. id (string) -- Copy each of the 6,992 test identifiers exactly once. prediction (float) -- A finite relevance score in [0, 1]; higher values rank the candidate earlier within its four-candidate episode. Example using real identifiers from this task: id,prediction 000449d36607,0.537214 0006003b2162,0.461902 000de62bfb61,0.672881 001159989757,0.418205 Requirements The file must contain exactly 6,992 data rows. The column names must be exactly id,prediction, in that order. Every test id must appear exactly once; no extra ids are accepted. Every prediction must parse as a finite number in [0, 1]; missing values, infinities, and strings are invalid. Fit a learned candidate ranker from train.csv, train_targets.csv, and both public audio inputs. A fixed constant, manually keyed table, or hard-coded acoustic rule is not a valid solution. Evaluate complete four-candidate episodes during local model selection and keep the speaker-held-out validation design intact. Train and infer within the selected NVIDIA A10G environment and keep execution within 30 minutes. What Not To Use Do not use reverse-audio matching or an external copy of the recording collection to recover hidden repetition indices, targets, or episode membership. Do not use filename dictionaries, path-order assumptions, repetition-number lookups, row positions, or manually reconstructed lexical metadata as a target proxy; public identifiers and audio paths are intended to be opaque. Do not use a cached answer list, a hard-coded candidate table, or a hand-written spectral rule in place of a learned four-way repetition matcher. Do not collapse the task to independent tone classification or lexical-family recognition; both waveforms and the candidate relationship must inform the ranking. Do not add recordings or labels from outside the public audio and CSV files; the score is meant to measure repetition alignment from the supplied real audio. &nbsp;
> All-solver grace
> Grace ends in 37m
> Lockdown

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Metal-Oxide Optical Response from Combinatorial Imaging

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78235d5vt1dg633n2m29yta98e60re
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat hoang_phuc_6868's score of 0.564!

Full challenge description from page:

> Metal-Oxide Optical Response from Combinatorial Imaging Task Type This is a ranking challenge -- a learning-to-rank task, not regression and not classification. For each sample you output one score per target, used only to ORDER the samples along that target. The absolute value of a score is never compared to any ground truth, and any monotonic rescaling of your scores leaves the result unchanged. There are no classes to assign and no target values to match -- the objective is purely to sort the test samples into the correct order for each target. Overview A combinatorial materials library packs thousands of different metal-oxide compositions onto a handful of plates, each sample a small deposited spot that is photographed and then measured for how it absorbs light. The photograph and the absorption measurement are two windows onto the same material. This challenge gives you only the photograph -- a 64 by 64 colour image of one sample -- and asks you to recover five numbers that summarise how that sample absorbs light across the ultraviolet-visible range, from its overall absorption level to where its absorption edge sits in energy and how broad the absorption band is. What makes it more than a colour-matching exercise is that the average colour of the image is far from enough. Two samples can look almost the same on average yet absorb very differently, and the useful signal lives in the fine texture of the image -- the way brightness and hue vary across the spot, which reflects thickness, morphology, and composition. A model that only reads the mean colour reaches a low score; a model that reads the spatial texture does substantially better. You are predicting a physical measurement from an image, and the image rewards being looked at closely. Task Each sample is one 64 by 64 RGB image. You output a ranking score for each of five optical descriptors, chosen to span a wide difficulty range from an easy overall level to a hard edge position and band width: abs_mean (easy) -- the mean absorption over the spectrum, the sample's overall optical density. abs_nir (moderate) -- the absorption strength at a near-infrared probe energy (1.45 eV). abs_uv (moderate) -- the absorption strength at a near-ultraviolet probe energy (2.95 eV). edge_ev (hard) -- the photon energy of the absorption edge, where absorption rises through its midpoint; a band-gap proxy. spread_ev (hard) -- the spectral bandwidth: the standard deviation of photon energy weighted by absorption, that is how broad the absorption band is (narrow bands low, broad bands high). The easy level descriptors are read from overall colour, while the edge ENERGY and the band WIDTH are spectral-shape quantities a stronger model reads more precisely -- so a solution's score spreads with how well it recovers the spectral shape, not just the level. The descriptors are correlated (the spectra are effectively low-dimensional), so the challenge is not to find independent signals but to read the harder shape ones accurately. Required approach. Train a model on the provided images. You are learning to map the optical appearance of a sample to its measured absorption descriptors. Evaluation Submissions are scored with OpticalScore, higher is better, in the range 0 to 1. For each descriptor the sub-score is Kendall's tau rank correlation between the order your scores induce and the true order over the test samples, clipped to the range 0 to 1. Only the ordering of your estimates matters, so this is a ranking task, not regression: any monotonic rescaling of a descriptor leaves the score unchanged. OpticalScore = the mean of the five per-descriptor sub-scores. Why ranking is the appropriate metric here. This is a combinatorial materials-screening task. A library packs thousands of compositions, and the practical objective is to identify and prioritise which compositions absorb most or least at each probe energy -- so the decision-relevant quantity is the rank ORDER of the samples, not the exact absorption number. Absolute absorption also carries instrument-calibration and film-thickness normalisation that shift the overall scale without changing which composition out-absorbs which; the ordering is the stable, physically meaningful quantity that drives material selection. A scale-invariant rank correlation therefore measures exactly what matters -- recovering the correct ordering of compositions -- and does not reward trivial magnitude- or scale-matching, which is why ranking rather than absolute-error regression is used. A random or constant prediction scores about 0. Because the descriptors span easy to hard, the achievable score spreads with how much of the hard spectral-shape geometry a solution can read, not just the overall colour. Dataset The prepared public dataset: train_images/ -- 64 by 64 RGB optical images as PNG files, one per sample, named by id. train_targets.csv -- columns id, abs_mean, abs_nir, abs_uv, edge_ev, spread_ev: the true optical descriptors for the training samples. test_images/ -- optical images to characterise, named by id. test_queries.csv -- column id: the samples to score. sample_submission.csv -- a valid submission in the required format. The test samples come from synthesis plates held out entirely from training, so build a model whose mapping generalises to samples it has not seen rather than memorising a plate. Submission Submit a CSV with exactly these columns: id, abs_mean, abs_nir, abs_uv, edge_ev, spread_ev. Each row's id matches an id in test_queries.csv; every id must appear exactly once; all values must be finite numbers. Example: id,abs_mean,abs_nir,abs_uv,edge_ev,spread_ev q00000,0.42,-1.10,0.88,-0.31,1.55 q00001,-0.87,0.05,1.20,0.64,-0.42 Your scores can be on any scale -- only their ORDER within each column is used -- so you need not match the training targets' scale (which are themselves rank-normalised standard-normal values). Allowed And Prohibited Allowed: Train any model on the provided images: convolutional networks, vision transformers, and ensembles. Any preprocessing and augmentation consistent with the task, such as flips, crops, colour jitter, and normalisation. Standard open-source deep-learning libraries such as PyTorch, and standard image libraries. Prohibited: Do not use external datasets or any information beyond the provided files, and do not use models pretrained on external data. Do not train on, adapt to, or fit any statistics from the test images; use them only to produce predictions. The test descriptors are not provided. Do not hardcode outputs or use per-id answer tables. Do not use external LLM APIs or any model-generated labels in your submission. &nbsp;
> Closes in 3h 38m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Catalog Sabotage

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72bjx5net19b317rmpsqb96d8dtwy5
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat civil_dept's score of 0.580!

Full challenge description from page:

> Task Given one whole-object image and 80 row-local eight-token catalog codes, rank the full code assigned to the pictured object. The grader evaluates the order of complete codes. The eight fixed slots describe catalog section, class, class subtype, object family, object subtype, material or process family, material or process subtype, and depicted theme. Token names are opaque but stable. Every evaluation token occurs in training, while some correct eight-token combinations do not, so memorizing complete training codes cannot cover every query. A valid baseline fits one visual token classifier per slot. For candidate c = (t_1,...,t_8), sum_s log p_s(t_s | image) is the log of the product of its slot probabilities, so either value gives the same ranking. Joint image-code models are also allowed. Data train.csv has 1,009 rows and test.csv has 289. Both use the identical feature columns id, image, and candidate_0 through candidate_79. train_labels.csv maps every training id to one relevant_candidate; join it by id. Within each row, all candidates are distinct eight-token codes. images/ contains each complete catalog photograph on a neutral intake background. Preparation keeps the full object and aspect ratio, then applies at most a 4-pixel framing offset, at most 3 degrees of camera rotation, mild exposure and white-balance change, low sensor noise, and JPEG compression. These variations represent ordinary differences in centering, camera alignment, room light, sensor response, and file export. No lens warp, blur, mosaic, palette reduction, mirroring, crop, mask, or tile rearrangement is applied. An acquisition-series group shares a normalized source-title, creator, and portfolio signature. Whole groups are assigned before labels and candidates are built, and no group or image crosses the split. This blocks repeated-series memorization and tests unseen-series ranking within the same capture process. For local validation, use train_validation_groups.csv to keep each training group_id in one fold; data_manifest.json records the prepared counts and split construction. Candidate allocation is role-safe and frequency-balanced: across evaluation rows, every eligible complete code appears 157 or 158 times. Frequency therefore does not reveal which code is correct. Gold positions have no fixed quota, and no cross-row assignment is required. Metric Each query has one correct visual-taxonomy candidate. Reciprocal rank is 1/r_i when it appears at rank r_i; ties receive the mean for their positions, and MRR averages rows equally. The random 80-way expectation is H_80/80. Subtracting that floor makes random ranking score 0, perfect ranking score 1, and preserves the ordering of above-chance systems. With H_80 = sum(k=1..80, 1/k), the score is: max(0, (MRR - H_80/80) / (1 - H_80/80)) Higher is better; scores are clipped to [0,1]. Submission Submit id followed by score_0 through score_79 in that order, with every test ID exactly once. Scores must be finite real numbers in [-1000000, 1000000]; larger means more relevant. See sample_submission.csv. id,score_0,score_1,score_2,score_3,score_4,score_5,score_6,score_7,score_8,score_9,score_10,score_11,score_12,score_13,score_14,score_15,score_16,score_17,score_18,score_19,score_20,score_21,score_22,score_23,score_24,score_25,score_26,score_27,score_28,score_29,score_30,score_31,score_32,score_33,score_34,score_35,score_36,score_37,score_38,score_39,score_40,score_41,score_42,score_43,score_44,score_45,score_46,score_47,score_48,score_49,score_50,score_51,score_52,score_53,score_54,score_55,score_56,score_57,score_58,score_59,score_60,score_61,score_62,score_63,score_64,score_65,score_66,score_67,score_68,score_69,score_70,score_71,score_72,score_73,score_74,score_75,score_76,score_77,score_78,score_79 q000000000000000000000000x,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0 Rules Allowed: released files, train-only validation, and packaged general-purpose pretrained visual or multimodal weights. Required: each row's ranking must be learned from its image and candidate sequences. Prohibited: external images or row-level catalog records, source lookup, synthetic replacement data, hardcoded answers, candidate-only submissions, cross-row assignment, test-wide fitting or adaptation, network access, package installation, subprocesses, and host inspection. The grader rejects malformed schemas, wrong ID coverage, duplicate or altered IDs, booleans, non-numeric values, NaN, and infinity.
> Closes in 4h 8m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Metamaterial Ensemble Laminate Counterexample Search

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dcps3ysrqsezqnwbmnkr29h8dta6f
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat junhyeok's score of 0.240!

Full challenge description from page:

> Overview Compare six cellular laminates and find every case where the less material-intensive design is nevertheless stiffer. The submission must provide the complete counterexample graph, rank all six assemblies by axial screening stiffness, and classify how widespread the violations are. This is an early design-review problem for architected materials. Engineers often use solid fraction as a quick screening rule before simulation or fabrication. That shortcut becomes unreliable when each laminate side represents an ensemble of stochastic unit cells and the two sides interact in series or parallel. The challenge asks a model to expose every failure of the shortcut, not merely estimate one property for one image. The competition environment provides access to a single NVIDIA A10G GPU. The entire pipeline must finish within 1.5 hours, including data loading, training or adaptation, inference, decoding, validation, and submission generation. Engineering Setup One inspection board contains six labeled assemblies, A through F, arranged in two rows of three. Every panel combines two visible consensus topologies at a 35%, 45%, 55%, or 65% boundary. A vertical boundary places the two ensembles in series along horizontal loading. A horizontal boundary places them in parallel. Dark pixels are solid material and light pixels are void. Boundary orientation and fraction are visible; source properties and identities are hidden. Each visible side is a nonlinear consensus made from four split-local unit cells. Their hidden weights are 0.34, 0.28, 0.22, and 0.16. Periodic transformations, weighted fusion, a weak periodic field, and density-preserving thresholding create a new mask, so no deposited source topology appears intact. For source moduli combined into ensemble values E1 and E2, and visible first-side fraction w, panel stiffness is defined by: parallel: E = w * E1 + (1-w) * E2 series: E = 1 / (w/E1 + (1-w)/E2) The panel material fraction uses the same visible mixture rule. These equations establish the screening target; the underlying source measurements are not public inputs. Dataset | Path | Contents | |---|---| | train.csv | 4,000 labeled six-panel design reviews. | | test.csv | 800 hidden reviews. | | sample_submission.csv | Schema-valid baseline output. | | inspection_boards/ | Distinct 824 by 594 pixel JPEG boards. | Columns | Column | Data type | Train | Test | Description | |---|---|---:|---:|---| | case_id | string | yes | yes | Opaque identifier used only for submission alignment. | | inspection_board_path | relative path string | yes | yes | Path to the six-panel topology board. | | counterexample_graph | canonical directed-edge set | yes | no | All density-stiffness counterexamples. | | stiffness_order | canonical permutation string | yes | no | Labels A-F ordered from greatest to least stiffness. | | violation_state | categorical string | yes | no | Edge-count regime: sparse, contested, or dense. | Exact unit cells and every reflected or quarter-turned equivalent belong to one split only. All four members of an ensemble come from that split-local pool. Public IDs and board paths are unrelated to source order. test.csv contains exactly case_id and inspection_board_path. train.csv appends counterexample_graph, stiffness_order, and violation_state. The comparison request is the same for every board and appears in this specification, not as a constant input feature. Every ensemble constituent is selected after topology-group splitting, so a held-out board cannot borrow a training-side constituent. Many boards reuse constituents within their own split; the 6,000 boards are not 6,000 independent source collections. Training contains 1,333 sparse, 1,333 contested, and 1,334 dense boards. It includes 3,658 distinct counterexample graphs and 716 distinct stiffness orders. Counterexample Certificate Directed Graph An edge X>Y means X has lower composite material fraction than Y but greater axial stiffness. Submit every such edge, sort tokens canonically, and join them with |. Use the literal token no_edges when the set is empty. This explicit token is an ordinary string and is never interpreted as a missing value. At most 15 edges and 96 characters are allowed. Stiffness Order Submit one permutation of A through F, from greatest to least stiffness, joined by >. The string is limited to 16 characters. Violation State | State | Number of submitted counterexample edges | |---|---:| | sparse | 0 through 4 | | contested | 5 through 7 | | dense | 8 or more | The categorical value must agree with the submitted graph edge count. Evaluation The Mechanical Counterexample Certificate Score is: Score = 0.46 * GraphScore + 0.39 * RankScore + 0.15 * StateScore Minimum score: 0.0. Maximum score: 1.0. Higher is better. Exact answers score 1.0. For graph truth T and submitted edge set P: set_F1 = 2 * |T intersection P| / (|T| + |P|) If both sets are empty, F1 is 1; if only one is empty, F1 is 0. The graph row score is 0.55 * exact_set_match + 0.45 * set_F1, averaged as GraphScore. This gives useful credit for individual counterexamples while retaining a majority exact-set term for completeness. The six-label order contains 15 unordered pairs. pair_concordance is the fraction whose relative order matches truth. The rank row score is 0.60 * exact_permutation_match + 0.40 * pair_concordance, averaged as RankScore. A mostly correct order therefore receives informative partial credit without making exact ranking optional. For each state present in hidden truth, recall is the fraction of rows with that true state predicted correctly. StateScore is the unweighted mean of the three recalls. A graph-inconsistent state is counted as incorrect. Malformed graphs, repeated edges, invalid permutations, and overlong strings score zero for their affected component. Submission Format Write ./working/submission.csv with these required columns in order: case_id counterexample_graph stiffness_order violation_state | case_id | counterexample_graph | stiffness_order | violation_state | |---|---|---|---| | mc_10ab20cd30ef40aa | A>D\|C>B | C>A>F>B>D>E | sparse | All required fields are strings. Every hidden ID must appear exactly once. An optional backend-managed visibility column may appear anywhere in the submission, answers, or both; its values are ignored and its presence does not need to match between files. After removing this optional column, the four required columns must match the order above. All other extra columns, reordered required columns, duplicate column names, duplicate IDs, missing or unknown IDs, and extra prediction rows are rejected. Malformed target strings score zero as documented. This metadata exception does not change the scoring formulas. Why Counterexamples Are The Target Predicting a scalar modulus would reward accurate average behavior while concealing the precise designs that defeat a common engineering heuristic. The directed graph instead requires a complete relational witness over six assemblies. A model must learn ensemble behavior, read series-versus-parallel composition, compare all panels jointly, and preserve enough ordering information to identify every inversion. Modeling Approaches A practical starter system can use four steps: Crop the six fixed panel locations and estimate material fraction from dark-pixel occupancy. Fine-tune one shared image encoder to assign a stiffness score to each crop, using pairwise or listwise losses derived from the training orders. Sort the six scores to form stiffness_order, then classify each panel pair as a counterexample using predicted stiffness and measured material fraction. Canonicalize the edge set and derive violation_state from its edge count. This decomposition is small enough to implement quickly. A joint board model may improve cases where boundary orientation and neighboring panels provide useful context. What Not To Use Do not predict from row order, case_id, board filename, archive order, or a reconstructed source-property lookup table. No source topology appears intact in a board. Hidden labels and private files are not permitted. Reference Validation The preparation creates 4,000 training and 800 hidden boards with distinct JPEG payloads and no cross-split hash. Hidden states contain 266 sparse, 266 contested, and 268 dense cases, with 778 distinct graphs and 480 distinct stiffness orders. Two clean rebuilds are byte-identical across all 4,804 files. Exact answers score 1.0; the varied sample scores 0.167093; the training-column-mode baseline scores 0.080446. A prior pixel-density monotonic baseline scored 0.098327 on the larger predecessor release under its earlier metric. In that earlier retrieval audit, none of 120 ensemble sides selected a true source constituent at rank one, two did so within the top five, and the median best-constituent rank was 4,483.5. Those predecessor measurements are not presented as scores for the reduced release. &nbsp;
> 2 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## SpectralKnot: Cross-Band Acquisition Topology Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7d309dgf1mby776g0g6zmnx18e6d1g
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat junhyeok's score of 0.162!

Full challenge description from page:

> SpectralKnot: Cross-Band Acquisition Topology Repair Overview The Advanced Baseline Imager aboard GOES-16 records the same Earth disk through multiple infrared channels during one scanning campaign. Operational archives preserve channel names, scan navigation, and orientation. This benchmark models a damaged archive in which those labels were detached from small image cards. Given a C13 anchor plus eighteen anonymous candidate cards, recover the six cards from the same geographic crop and report the inverse transform that returns each card to the anchor orientation. The six required channels are C07, C08, C11, C14, C15, and C16. For every channel, the candidate set also contains two genuine nearby crops from the same scan. Recognizing spectral appearance alone is therefore insufficient: channel identity, location, and orientation must agree. This is multi-view association and transform recovery, not classification, forecasting, or missing-channel synthesis. Eight complete scan campaigns train and four disjoint campaigns evaluate. Dataset train.csv has 1,200 labeled cases and test.csv has 600 input cases. train_images.npz and test_images.npz contain uint8 arrays shaped [case,19,48,48]. Card zero is the C13 anchor and cards one through eighteen are candidates. Complete scan campaigns are assigned to one split only: eight campaigns contribute training cases and four contribute evaluation cases. | CSV column | Type | Meaning | |---|---|---| | example_id | string | Opaque case identifier. | | candidate_ids_json | JSON string list | Nineteen card IDs in tensor order; item zero names the anchor. | | topology_json | JSON object in train_labels.csv | Gold channel-to-candidate and inverse-transform mapping for training cases. | train.csv and test.csv have identical feature columns: example_id and candidate_ids_json. Training targets are stored separately in train_labels.csv, joined by example_id. sample_submission.csv supplies all evaluation identifiers and the exact output columns. Submission Submit exactly example_id,topology_json. The JSON object must contain exactly C07,C08,C11,C14,C15,C16; JSON key order is ignored. Each value contains one distinct candidate ID and one transform from r0, r90, r180, r270, flip_x, flip_y, transpose, or anti_transpose. For example, the start of one row is shown below; use the shipped sample_submission.csv for a complete six-channel record: example_id,topology_json SK_001,"{""C07"":{""candidate_id"":""V_0123456789ABCDEF"",""inverse_transform"":""r90""},""C08"":{""candidate_id"":""V_1123456789ABCDEF"",""inverse_transform"":""flip_x""},""C11"":{""candidate_id"":""V_2123456789ABCDEF"",""inverse_transform"":""r0""},""C14"":{""candidate_id"":""V_3123456789ABCDEF"",""inverse_transform"":""transpose""},""C15"":{""candidate_id"":""V_4123456789ABCDEF"",""inverse_transform"":""r270""},""C16"":{""candidate_id"":""V_5123456789ABCDEF"",""inverse_transform"":""flip_y""}}" Evaluation For each of the six channels, candidate accuracy is one when the selected card is the native same-location card. Joint accuracy is one only when both the card and its inverse transform are correct. An inverse transform attached to the wrong card receives no standalone credit because it cannot repair that acquisition. Each component is averaged over all channels and cases. Two record-level terms are also computed. Candidate-portfolio exactness is one only when all six candidate IDs are correct. Topology exactness is one only when all six candidate IDs and all six inverse transforms are correct. The final score is 0.15 * candidate accuracy + 0.20 * joint accuracy + 0.20 * candidate-portfolio exactness + 0.45 * topology exactness, bounded in [0,1] and maximized. The 35% channel-level credit provides stable progress for partially repaired records. The remaining 65% measures whether the acquisition is operationally usable as a complete six-channel bundle: one wrong member invalidates the portfolio, and one wrong orientation invalidates the full topology. Malformed prediction rows receive zero credit for that row. A malformed table, missing or duplicated identifiers, wrong columns, or missing values returns a total score of 0.0. This behavior is identical on public and private evaluation slices. Not Allowed Methods And Limitations Do not retrieve source scans, infer hidden campaigns from IDs, access private mappings, manually label test cases, or probe evaluation labels. Models may use the released training cases, image tensors, and generally available pretrained vision components. The bounded corpus uses normalized 48-pixel crops from twelve GOES campaigns. Prepared identifiers are re-keyed from organizer-held source bytes and do not preserve the construction salt or original raw identifiers. Histogram equalization removes marginal-intensity channel shortcuts. Nearby rivals are deliberately constructed, and the small campaign count limits claims about seasonal or geographic generalization. Prepared cards also contain deterministic cross-case spectral interference, independent nonlinear tone response, mild blur, scan-direction gain drift, noise, three occluded patches, and an additional card-specific orientation composed into the private inverse. These nuisance effects preserve the primary card's channel and nominal crop while preventing raw pixel correlation or the obsolete builder token recipe from serving as the complete solution. The outputs are not official NOAA navigation, calibration, or operational weather products. &nbsp;
> 0 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Conditional Mechanical Freedom under Paired Constraint Release

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75h2wqmwpc04zsfajmyc2exs8e8350
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat osman0's score of 76.980!

Full challenge description from page:

> Overview Conditional Mechanical Freedom under Paired Constraint Release is a multimodal Computer Vision challenge for structured mechanical-state classification. Each example will contain an RGB observation of a mechanism, a nominal mechanism description, camera calibration, and a mechanical probe. The probe identifies a reference link, a monitored link, two releasable relation groups, two link-local query points, and a requested direction of relative motion. The model predicts categorical motion signatures for four counterfactual conditions: the observed mechanism with no queried release; release A only; release B only; releases A and B together. It also predicts an explicit categorical paired-release interaction signature. The participant-facing target is entirely categorical. There are no continuous response values in train targets, test data, sample submissions, or submitted predictions. The hidden preparation pipeline first computes physically meaningful local six-dimensional motion responses, then discretizes each component into a fixed public motion-token vocabulary. Those continuous responses are generation internals only and are never participant targets. The benchmark centers on conditional release interaction. A relation may be decisive in one constraint context and redundant in another. Two restraints can individually appear irrelevant while their combined removal unlocks a new direction of motion. Conversely, two individually important restraints can overlap so strongly that adding their separate effects exaggerates the joint change. The task therefore evaluates whether a visual model can infer the functional consequences of an observed assembly rather than merely recognize the equipment category or reconstruct its nominal design. Hidden Physical Construction Let z0 denote the admissible response before either queried release, zA the response after releasing A, zB the response after releasing B, and zAB the response after releasing both. The hidden paired-release interaction residual is eta = zAB - zA - zB + z0. These vectors are used only by the dataset builder to generate categorical labels and private interaction strata. They are not serialized as public targets. If the two release effects compose independently, eta is near zero. If one release changes the significance of the other, eta becomes large. A cooperative release can satisfy zA approximately equal to z0 and zB approximately equal to z0 while zAB differs substantially from z0. Neither release alone opens the requested motion, yet the pair does. The reverse behavior is also possible. Both single releases may change the response while their effects overlap, making the joint release less dramatic than an additive model would predict. Motion Token Vocabulary Each hidden scalar motion component is converted into exactly one categorical token. The public token order is: N6, N5, N4, N3, N2, N1, Z, P1, P2, P3, P4, P5, P6 The bins are: N6: x 0.70 The same vocabulary is used for the six hidden interaction-residual components. Interaction residuals are not clipped before tokenization. Tokens are strings. Participants must submit the token names exactly as written above. What the Model Receives Every query is associated with one observed mechanism state. Participant-visible evidence contains: one RGB image; one nominal mechanism file; camera calibration; one release probe. The nominal mechanism describes links, rest transforms, and benchmark-supported mechanical relations. It does not expose the observed link transforms used to derive the hidden physical state. The probe contains: reference_link, the link against which relative motion is measured; monitored_link, the link whose motion is queried; reference_point, a point in the reference-link local frame; monitored_point, a point in the monitored-link local frame; release_a, the first relation group; release_b, the second relation group; requested_twist, the requested six-dimensional motion direction; length_scale, the public scale used to normalize translation relative to rotation. The two query points are generally nonzero. Their world-space lever arms therefore depend on the observed link orientations. Replacing them with the link origins changes the query and is not a valid simplification. Several probes may share one image. scene_id is public so participants can cache visual representations and keep complete scene groups together when constructing local validation. Meaning of a Release The benchmark models instantaneous local kinematics. A release removes the equality restrictions associated with the queried relation group while keeping the mechanism at the same observed configuration. The four conditions therefore differ only in which queried relations remain active. No finite repositioning occurs between conditions. The task does not model gravity, compliance, friction, collision, motor effort, damage, or accessibility of a physical fastener. It does not ask whether a released mechanism would move on its own. The hidden physical quantity is the requested motion that would be kinematically admissible at the observed state. The participant predicts only its categorical motion signature. If a queried relation is already ineffective in the current assembly, releasing it is a no-op. If another relation imposes the same local restriction, releasing one group may also have little effect. When both queried groups are released, their active restrictions are removed jointly. Hidden Motion Representation A requested relative motion is represented internally by d = (vx, vy, vz, wx, wy, wz). The first three components are the velocity of the monitored query point relative to the reference query point. The final three components are relative angular velocity. Translation is divided by the probe's public length_scale. Rotational components use radians. Both are expressed in the declared camera-coordinate frame. Every requested twist is normalized so that its L2 norm is one. For condition S, let VS be the normalized relative-motion space permitted by the active relation system. The hidden physical response is the orthogonal projection of d onto VS. A hidden zero vector means the requested motion is completely blocked. A hidden response equal to d means the requested motion is completely admissible. Intermediate responses contain the translational and rotational components that remain admissible. Participants are not asked to regress these values. Each component is converted to one of the public motion tokens. Why the RGB Observation Matters The mechanism file is nominal. The private target generator uses the observed world transform of every available link. Observed orientations affect relation axes. Observed positions affect joint lever arms. The nonzero link-local query points introduce additional point-velocity lever arms. Camera calibration then maps the resulting relative twist into the public camera frame. Consequently, a solver that uses only the mechanism file, relation identifiers, and equipment category does not possess enough information to reconstruct the categorical targets exactly. The RGB observation is the only public source of the current link state. The preparation pipeline does not select probes using singular directions, eigenvectors, hidden projection magnitude, categorical target rarity, or another function that ranks candidates by answer strength. Within each interaction stratum, retained probes are chosen by a deterministic hash of public query ingredients rather than by target magnitude. Why Pose Estimation Alone Is Not Enough Accurate pose is useful, and pose estimation followed by a correct release-aware kinematic solver is a valid approach. Independent pose prediction is not sufficient by itself. The categorical output also depends on the active relations, the counterfactual release set, the reference and monitored links, both link-local query points, the requested direction, and the paired interaction between A and B. A system that assigns independent scalar importance to A and B can fail even when its geometric reconstruction is plausible. Sources of Difficulty Configuration dependence. The same nominal mechanism can produce different motion-token signatures at different observed states. Point dependence. Nonzero query points couple angular freedom to translational point velocity. Assembly dependence. Missing or inactive components alter the effective relation system. Constraint redundancy. An active relation is not necessarily individually decisive. Paired interaction. The effect of A can depend strongly on whether B remains active. Directional evaluation. Correct mobility dimension does not imply the correct six-dimensional categorical signature. Visual ambiguity. Occlusion, viewpoint, texture, clutter, and domain changes make the observed state imperfectly recoverable. Repeated scene probes. A model should reuse one scene representation across distinct mechanical questions without treating them as separate captures. Public Data The public package contains: train.csv; test.csv; sample_submission.csv; images/; mechanisms/. There is no provided development split. Participants should construct validation splits from train.csv. All rows sharing one scene_id must remain in the same local partition. The public feature columns are: sample_id; scene_id; image_path; mechanism_path; camera; probe. camera is compact JSON containing the camera-to-world matrix, camera intrinsics, and coordinate convention. probe is compact JSON containing the reference and monitored links, their link-local points, the release identifiers, requested twist, and length scale. Training rows additionally contain 30 categorical targets: 24 motion-component tokens covering base, release A, release B, and release A+B; 6 explicit paired-release interaction tokens. Test rows contain no response tokens, observed link transforms, scene-specific relation-activation labels, correspondence solutions, or private evaluation strata. sample_id is an alignment key and must not be used as a predictive feature. Row order and filename order must not be used as predictive features. Train and Test The competition provides only train and test partitions. Training contains diverse rendered observations together with a subset of real-image scenes and full categorical query targets. Test contains held-out real-image scenes. All assets and probe variants belonging to one underlying scene remain in one partition. The task measures generalization to new observed states of mechanism families represented in training. It does not claim unrestricted transfer to arbitrary unseen machinery. The final row counts depend on mechanical eligibility and numerical-stability checks performed during preparation. Submission Format Use sample_submission.csv exactly. The submission contains 31 columns. The first is sample_id. The remaining 30 columns are categorical strings in this exact order: base_vx_token, base_vy_token, base_vz_token, base_wx_token, base_wy_token, base_wz_token; release_a_vx_token, release_a_vy_token, release_a_vz_token, release_a_wx_token, release_a_wy_token, release_a_wz_token; release_b_vx_token, release_b_vy_token, release_b_vz_token, release_b_wx_token, release_b_wy_token, release_b_wz_token; release_ab_vx_token, release_ab_vy_token, release_ab_vz_token, release_ab_wx_token, release_ab_wy_token, release_ab_wz_token; interaction_vx_token, interaction_vy_token, interaction_vz_token, interaction_wx_token, interaction_wy_token, interaction_wz_token. Every expected sample_id must appear exactly once. Row order may differ because the grader aligns by sample_id. Column names and order must match sample_submission.csv exactly. Every prediction value must be one of the 13 public motion tokens. Numeric values, missing values, unknown strings, malformed submissions, duplicate IDs, missing IDs, and extra submission columns receive the evaluator floor. Private Grading Metadata The private answers.csv begins with exactly the same 31-column prefix as sample_submission.csv, with the same names and in the same order. After that exact submission-compatible prefix, answers.csv may append grader-only fields such as: sceneid; equipmentid; _stratum; _configuration. These private fields are not prediction targets and must not appear in a submission. They are used for scene grouping, equipment grouping, interaction-stratum balancing, and build auditing. The grader explicitly verifies that the answers.csv prefix is identical to the sample-submission schema. Evaluation Metric The metric is categorical. Submitted tokens are never decoded into continuous motion values and no regression loss is used. For a predicted token p and gold token g, define categorical component credit: 1.00 if p equals g exactly; 0.25 if p is immediately adjacent to g in the public 13-token order; 0.00 otherwise. For query q, let Rq be the average categorical credit over the 24 four-condition response tokens. Let Iq be the average categorical credit over the 6 explicit interaction tokens. The per-query score is sq = 0.55 Rq + 0.45 Iq. Thus interaction remains a first-class part of evaluation while the prediction contract stays purely categorical. Balanced Interaction Strata Easy no-change probes do not dominate the leaderboard. Each evaluation query belongs privately to exactly one of four strata, assigned from the hidden physical responses during preparation. Unchanged The largest hidden change caused by A, B, or A+B is at most 0.03 in normalized six-dimensional response norm. Cooperative The query is not unchanged, both hidden individual changes are at most 0.03, and the hidden A+B change is at least 0.15. Other Non-Additive The query is neither unchanged nor cooperative and the hidden interaction-residual norm is at least 0.15. Remaining Every other valid query. The final evaluation set contains all four strata. Aggregation is hierarchical: query scores are averaged within each scene and stratum; scene scores are averaged within each equipment and stratum; represented equipment are averaged within each stratum; the four stratum scores receive equal final weight. Thus scenes with more probes do not automatically receive greater influence, and interaction-heavy strata remain consequential. The final leaderboard score is 100 * (S_unchanged + S_cooperative + S_other_non_additive + S_remaining) / 4. Scores are clipped to [0.01, 100]. Grading is deterministic. There is no LLM judge, embedding service, external scoring API, or manual interpretation. Modeling Directions The intended environment provides one NVIDIA A10G-class GPU with approximately 24 GB of memory and a 90-minute end-to-end runtime budget. The runtime includes loading images and mechanism files, preprocessing, training or adaptation, inference, optional mechanical computation, and writing the submission. Possible approaches include: image encoders combined with graph neural networks; part-aware visual attention; query-conditioned multimodal transformers; models that infer observed link state; differentiable constraint layers; pose or assembly prediction followed by analytical kinematics and tokenization; hybrid neural and numerical systems; direct structured token classification. No architecture is mandated. A strong solution should encode each scene once and answer several release probes from the shared visual representation. Allowed Resources Participants may use the released files, public pretrained vision or multimodal checkpoints, standard numerical and machine-learning libraries, and locally derived training features. Remote inference APIs are not allowed. Disallowed Shortcuts Participants may not use hidden test labels, private evaluator files, manual test annotation, external copies of hidden scene annotations, recovered observed pose files, hard-coded test responses, submission-feedback reconstruction, sample_id semantics, row order, or filename order. General pretrained visual knowledge is allowed. Direct recovery of private scene state or test answers is not. Release Quality Before a query is admitted, preparation verifies that: the nominal mechanism contains enough supported relation information; observed pose matrices are interpreted in their declared world frame; requested directions were generated without consulting hidden projectors; both link-local query points are finite and nonzero; release operations do not decrease the admissible motion space; hidden physical projections are stable under nearby rank tolerances; reference and monitored links are present in the observed system; requested twists have unit norm; hidden physical response components are finite; categorical targets belong to the fixed public vocabulary; candidate retention does not rank by hidden response magnitude or token rarity; the public package does not expose observed link transforms or private strata; sample_submission.csv and the leading answer columns have identical schemas; all four interaction strata are represented in evaluation. Queries that cannot be interpreted reliably are excluded rather than guessed. Scope The challenge evaluates visual inference of local rigid-link kinematic freedom under hypothetical changes to mechanical relations, expressed as structured categorical motion signatures. It does not predict forces, damage, finite disassembly trajectories, gravity-driven motion, collision, or safety. Its central question is: can a model infer not only what motion category a restraint prevents, but how that categorical motion signature changes after another restriction has been removed at the observed state?
> Ranks finalizing

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## From Ink to Isobars: Sea-Level Pressure Fields from Historical Weather Maps

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7akddrvpsjre9zys08phrx398e78ak
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview For decades, the day's weather reached the public as a printed map. An analyst plotted a few hundred telegraphed station reports, drew the isobars by hand, marked the highs and lows, and sent the chart to press. This challenge asks a model to read such a chart the way a meteorologist would and recover the sea-level pressure field it depicts. Each input is a scanned daily weather map of the contiguous United States and southern Canada, drawn from observations taken at 8 a.m. Eastern Standard Time (13:00 UTC) on a date between 1910 and 1937. The output is the sea-level pressure at that moment, in hectopascals, at 377 fixed grid points over the United States. The pages are cluttered and inconsistent. Besides isobars labelled in inches of mercury, they carry station symbols and printed station values, the words HIGH and LOW at pressure centres, isotherms, shaded precipitation, forecast text and station tables. Drafting style, lettering and page layout drift across the 28 years, and every scan has its own margins, stains and offset. The targets are not a tracing of the drawn isobars. They come from an independent gridded analysis of the same moment, made much later with a numerical weather model. The chart and the target therefore disagree where the analyst smoothed or extrapolated, over the western plateaus, where the reduction of pressure to sea level differs, and over the ocean and Mexico at the edges of the grid. A good model learns how the drawn chart relates to the pressure field; transcribing contours alone is not enough. Evaluation Submissions are scored with a mean-squared-error skill score measured against the long-term mean field: $$ S = \max\left(0,\ 1 - \frac{\sum\left(\hat{p} - p\right)^{2}}{\sum\left(\bar{p} - p\right)^{2}}\right) $$ Both sums run over all 642 test maps and all 377 grid points. At each grid point of each map, $\hat{p}$ is the predicted sea-level pressure and $p$ is the target, both in hPa, and $\bar{p}$ is the mean of the training targets at that grid point, a single fixed field. A score of 1 means exact predictions; predicting the long-term mean field, or anything worse, scores 0. Higher is better. The day-of-year climatology in sample_submission.csv scores 0.13: it captures the seasonal cycle but none of the day's weather. A monthly climatology, a per-cell median, a constant 1013.25 hPa and yesterday's field all score 0, so the score moves only by reading the map. Dataset There are 2,996 maps: 107 randomly chosen dates from each year 1910–1937. Train: 2,354 maps from the 22 years not listed for test. Test: 642 maps from six whole years: 1913, 1921, 1925, 1929, 1933 and 1937. The test years are spread across the period, so no test day has a neighbouring day in the training set and the test covers the full range of drafting styles. Maps from nearby dates share weather systems, so validate by holding out whole years. Files train.csv: date, image and the 377 target columns. test.csv: date and image. sample_submission.csv: the required submission format, filled with a day-of-year climatology fitted on the training targets. grid.csv: one row per target column, with the columns column, row, col, lat_deg_n and lon_deg_e; longitudes are negative to the west. maps/YYYYMMDD.jpg: RGB JPEG scans, 1,280 pixels wide and 935–1,083 pixels tall, uncropped. Columns date (string): observation date as YYYYMMDD, one map per date. image (string): path of the map, maps/YYYYMMDD.jpg. p_RR_CC (float, train.csv only): sea-level pressure in hPa at grid row RR and column CC. Grid The 377 target columns cover a regular 2-degree grid of 13 latitudes by 29 longitudes: RR runs from 00 at 50° N down to 12 at 26° N. CC runs from 00 at 124° W east to 28 at 68° W. Submission Submit a CSV file with a header row and one row per test map. The header is date followed by the 377 pressure columns, in the order of sample_submission.csv: date,p_00_00,p_00_01,...,p_12_28 19130102,1014.62,1014.91,...,1019.03 Requirements Exactly 642 rows, one for every test date, each date once. Exactly the 378 columns of sample_submission.csv, in the same order. Every pressure a finite number between 800 and 1,200 hPa. A wrong or reordered column set, a missing, duplicate or unknown date, or the wrong number of rows is reported as an error naming the fault rather than scored. A row whose values are not finite pressures between 800 and 1,200 hPa is scored as if it had submitted the reference field, so one unusable row costs that row and nothing more. Compute One A10G GPU and about 90 minutes end to end. The scans are large, so plan the input resolution and the training schedule for that budget. What not to use These rules are specific to this challenge and take precedence over the general solver guidebook where the two differ. Pretrained weights of any kind. Train every model from scratch on the supplied maps. This excludes backbones from timm or Hugging Face, OCR and document models, and any weather or map model. External data. No gridded pressure analyses, reanalyses or forecasts, station records, digitised or scanned weather maps, or other meteorological data. Maps and targets for other dates count as external data. Looking up the date. Each map prints its date and the CSV files give it. The date may be used as an input feature, never to retrieve a record of that day's weather. Other test maps. Predict each test map from that map and its own row alone. Do not smooth or average predictions across neighbouring test dates, pseudo-label test maps, adapt a model on the test set, or calibrate outputs to the distribution of the test set. Synthetic training data. Do not render or generate additional maps. Augmenting the supplied maps is fine. The guidebook's other rules still apply, including that a solution must train a genuine image model rather than fit a tabular model to raw pixels. Notes The targets estimate the state of the atmosphere; they do not measure it. Their errors are larger early in the period and near the edges of the grid, so a perfect score is not attainable, and a high score means close agreement with the targets rather than with the true pressure field. Performance on these maps does not establish performance on other chart series, periods or countries.
> 0 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Worst-Class Vessel Ranging from Submarine Fibre-Optic Sensing

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78tcbz31fy9smswcn1k4t6w98dw2sh
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview A submarine telecommunications cable has been converted into a distributed acoustic sensing (DAS) array. The system continuously records acoustic activity along the cable, producing compact spatial-spectral images of underwater events. Each observation is provided as a 24 × 100 single-channel image representing the acoustic energy observed across a subset of the cable over a 10-second window. The image contains structured spatial and frequency information, and the goal is to learn visual patterns in these measurements that are useful for estimating a vessel's range from the sensing system. The challenge is centered on learning from structured scientific images, where the final prediction is a continuous physical quantity — and the evaluation is deliberately focused on the vessel class for which ranging is hardest. Data Each observation is a PNG image containing a 24 × 100 spatial-spectral measurement. Image structure Axis Size Meaning Rows 24 Sensing positions, in three groups of 8 contiguous channels Columns 100 Logarithmically spaced frequency bands, ~4–98 Hz The 24 rows are divided into three groups of 8 contiguous sensing channels, drawn from three separated regions along the cable (an early, a middle, and a late segment). Channels within a group are evenly spaced; the three groups are separated from one another by a substantially larger gap than the spacing within a group. Frequency increases left to right; the 49–51 Hz region is excluded. The PNG therefore preserves both spatial and spectral structure — it is not an ordinary natural image. Pixel calibration Pixel intensity is calibrated to acoustic energy using a fixed global scale: log10_energy = pixel_value / 65535.0 * (-3.0 - -17.0) + -17.0 This global calibration should be preserved during modeling. Training Data 53,507 training PNGs, plus: train.csv id, distance_m id — identifies the observation distance_m — target vessel distance, in meters train_metadata.csv — additional fields per observation: id vessel_class vessel_length_m vessel_beam_m vessel_fingerprint transit_run Some metadata fields are intentionally incomplete: Field Condition Share vessel_class Unknown 3.39% vessel_class Other vessel type 0.42% vessel_length_m / vessel_beam_m Missing ~2.94% Test Data 21,264 test PNGs, plus test.csv and sample_submission.csv. The required output is one distance prediction per test observation. No vessel class, fingerprint, or other metadata is provided for the test set. Class membership for test observations is used only internally, for scoring, and is not revealed anywhere in the public data. Vessel and Group Structure The dataset contains repeated observations from vessel transits. A vessel fingerprint identifies observations belonging to the same underlying vessel identity. The train/test split is performed by vessel fingerprint, not by individual image, since visually similar observations from the same vessel can occur across many windows. A random row-level validation split is not representative of the leaderboard evaluation and can produce severely optimistic results. Validation should respect the vessel-level grouping instead. The Target Target: vessel distance from the sensing system, in meters. Range: approximately 10 m → 12,000 m. Evaluation operates in log-distance space. Predictions are clipped to [10, 12000] before scoring. Useful signal may come from combinations of: acoustic intensity frequency-dependent structure spatial activation patterns propagation signatures differences between the three sensing regions temporal/acoustic patterns within the image vessel-dependent acoustic fingerprints Image Learning The 24 × 100 representation should be treated as a structured sensor image — models may exploit both local and global patterns, including relationships between neighboring sensing positions and frequency bands. Potential approaches include: convolutional neural networks vision transformers hybrid CNN/Transformer architectures multi-scale feature extractors learned image embeddings attention-based spatial-spectral models image encoders followed by regression heads ensembles of different image architectures Because the input is single-channel with physical (not RGB-like) axes, models should preserve the underlying spatial/spectral structure rather than treating the image as an arbitrary natural photograph. Metadata Metadata can be used alongside the image, for the training set only: vessel class, length, beam vessel fingerprint, transit run missingness indicators interactions between metadata and learned image representations Metadata can be fused with image features via: concatenation attention auxiliary branches mixture-of-experts models stacking regression ensembles Metadata should not be assumed complete or perfectly reliable. Validation The most important requirement is avoiding leakage between observations of the same vessel. Recommended: split by vessel_fingerprint, not by individual rows. For stricter schemes, also group by transit_run. Leaderboard performance may differ substantially from ordinary random-split validation. Data Augmentation and Image Handling Augmentations must preserve the physical meaning of the sensor image. Invalid arbitrary brightness/contrast changes gamma transformations per-image normalization that destroys the global energy scale vertical or horizontal flipping random row shuffling arbitrary cropping that removes physical regions Potentially valid (applied consistently) shared/global rescaling resizing additive noise mixup other transforms that preserve the physical interpretation of the axes and global calibration Evaluation The evaluation emphasizes the vessel class that is hardest to range accurately. Distances are transformed to log10(distance_m) and clipped to [10, 12000]. A small numerical floor, FLOOR = 0.015, is applied. Test observations are partitioned into evaluation groups based on their privately held vessel class. This grouping is not derived from, or recoverable from, the observation id or any other public field. A worst-class group is a vessel class with at least 300 held-out observations. Final score: final = 0.5 × OverallScore + 0.5 × WorstClassScore where WorstClassScore is the score of the worst eligible vessel-class group. Optimizing only average performance is therefore insufficient — a model that excels on common/easy classes but fails on one difficult class still scores weakly. A constant median-distance predictor scores ≈ 0. Effective target quantization is ≈ 57.7 m between windows (≈ 0.0145 in log10 distance). What Makes the Challenge Difficult Source of difficulty Why it matters Structured image input A compact scientific image, not a tabular feature vector Spatial-spectral relationships Distance information spans both position and frequency Limited spatial coverage 24 rows cover three separated regions, not the full cable Vessel variability Different types/dimensions produce different acoustic signatures Repeated observations Multiple observations per vessel make naive validation leak-prone Incomplete metadata Vessel info is missing for some training rows, and absent entirely at test time Worst-class evaluation Robustness across hard classes matters, not just the average Allowed Any ML architecture and library CNNs, vision transformers, hybrid CNN/Transformer architectures Generic pretrained model weights, adapted to single-channel input Input normalization that preserves the intended global calibration Learned image embeddings; multi-scale spatial/spectral feature extraction Any reasonable regression head All fields in train_metadata.csv; metadata/image feature fusion Unsupervised or transductive use of test images for feature construction Clustering of train/test image representations Dataset-level statistics computed from train and test images Domain adaptation based only on the provided data Vessel/group identifiers supplied by the dataset Test-time augmentation (TTA) Model ensembling, stacking, and blending; multiple independently trained models Consistent image resizing; shared/global rescaling; additive noise; mixup Cross-validation using vessel-level grouping Any loss function appropriate for continuous distance prediction Not Allowed Attempting to identify the underlying source dataset or acquisition site — including via web search — in order to look up ground-truth values Retrieving the target distance from an external source Matching observations against any external release of the same or similar recordings Recovering timestamps or acquisition order not explicitly provided Using external datasets containing recordings from the same experiment Using pretrained models trained specifically on recordings from this dataset Manually labeling the provided observations Modifying the supplied dataset Probing the grader or evaluation system Exploiting implementation bugs in the evaluation system Writing files outside ./working External general-purpose pretrained models are permitted, provided they were not trained on recordings from this experiment or otherwise leak the target information. Submission Format The submission must contain exactly: id, distance_m for all 21,264 test observations, with: no missing or duplicate IDs no missing predictions no non-finite or invalid distance values no columns other than id and distance_m Predicted distance is expressed in meters. The final file should follow the structure of sample_submission.csv.
> 0 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Seed Cohort Emergence Bracket Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx793tmmebwdgyae8a917vht1s8dwj4a
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview For each case, predict the observation interval in which each of eight marked seeds first becomes visibly germinated. The answer is one 8 x 2 integer matrix in the same order as the eight supplied boxes. Commercial seed testing is inspected at discrete times, so a camera rarely captures the exact instant of emergence. The useful record is a censoring bracket: the last photograph where a seed is still negative and the first photograph where it is positive. A seed that remains negative at the final inspection is right-censored rather than assigned a guessed future time. Each input contains twelve original overhead photographs from one laboratory dish. Seeds can shift as roots expand, and glare, overlap, husks, and small early radicles make exact transition localization difficult. A solution must track all eight marked seeds and recover eight brackets jointly. It cannot obtain the target by classifying only the final image or by predicting a typical germination time. Dataset | File | Contents | |---|---| | train.csv | 1,858 cases with input columns and emergence_brackets | | test.csv | 400 cases with input columns only | | sample_submission.csv | Schema-valid varied baseline for all test IDs | | sequences/ | 239 ZIP files, each holding twelve original 624 x 624 RGB JPEG observations from one dish | The 193 training dishes and 46 test dishes contribute 2,868 distinct public photographs. One dish supports several cases because different reliable tracks can anchor different eight-seed cohorts. Case rows are therefore not independent experiments. CSV Columns train.csv contains id,sequence_path,query_boxes,observation_frames,emergence_brackets. test.csv contains the same four input columns in the same order and omits only the target. | Column | Type | Description | |---|---|---| | id | string | Opaque case identifier beginning with case_ | | sequence_path | string | Relative path to the dish ZIP inside sequences/ | | query_boxes | JSON array with shape 8 x 4 | Initial-image boxes [xmin,ymin,xmax,ymax] for seeds S0 through S7 | | observation_frames | JSON array of 12 increasing integers | Original frame indices represented by the twelve JPEGs | | emergence_brackets | JSON integer matrix with shape 8 x 2 | Hidden or training censoring bracket for each query seed | The file names inside a sequence ZIP use the original zero-based index, such as frame_000.jpg and frame_046.jpg. Gaps are deliberate. Adjacent retained images can be separated by different amounts of source time. The boxes locate each seed in the first image only. They are not later-frame detections or root masks. All selected seeds are visibly negative initially. Tracks with changing object counts, conflicting identity assignments, weak overlap, or negative-after-positive reversals were excluded before case construction. Target Matrix For seed Sj, let L be the index of its last retained negative photograph and H its first retained positive photograph. The event is constrained to (L,H]. An observed transition is serialized as [L,H], using the original indices listed in observation_frames. A seed that is still negative in the final photograph is serialized as [L,-1], where L is the final observed index and -1 means right-censored. Matrix row j always belongs to query box j. Rows must not be sorted by time. For example, with observation frames [0,3,15,26,31,37,46,59,67,73,85,96], a valid target is: [[37,46],[96,-1],[67,73],[46,59],[59,67],[96,-1],[59,67],[59,67]] This says that S0 changed after frame 37 and by frame 46, while S1 and S5 remained negative through frame 96. Split And Leakage Protection All dishes and frames from an acquisition group stay in one partition. Seventeen acquisition groups supply training cases and five different groups supply test cases. The 400 evaluation anchors are selected round-robin across held-out dishes from 450 eligible held-out tracks, increasing independent visual coverage without changing labels. Exact source-image hashes do not cross the boundary. Cohort companions, tracking decisions, and observation schedules are built entirely within one dish; no image or seed donor is taken from the opposite partition. Training contains 12,604 observed seed transitions and 2,260 right-censored seed instances across its repeated cohorts. Test contains 2,739 observed transitions and 461 right-censored instances. These are cohort appearances, not counts of independent physical seeds. Submission Format Write ./working/submission.csv with exactly these columns in this order: | Column | Required type | |---|---| | id | Test identifier string copied without modification | | emergence_brackets | JSON integer matrix with exactly eight rows and two entries per row | Example: | id | emergence_brackets | |---|---| | case_01185445d490d8c6135d98363c1fa01a | [[37,46],[96,-1],[67,73],[46,59],[59,67],[96,-1],[59,67],[59,67]] | Each lower endpoint must be an integer from 0 through 200. Each upper endpoint must be -1 or an integer greater than its lower endpoint and no greater than 200. Booleans, floats, quoted integers, ragged matrices, nested objects, strings longer than 256 characters, and invalid JSON are malformed. Submit every test ID exactly once. Row order may differ. Extra or reordered columns, duplicate columns, duplicate IDs, unknown IDs, missing rows, and extra rows reject the submission. If the evaluation backend adds visibility, it must appear as the final column in both tables so their schemas still match exactly; it is not scored. Evaluation The Emergence Bracket Certificate Score is: Score = 0.55 * CompleteCertificateAccuracy 0.30 * SeedBracketAccuracy 0.15 * ImpliedOrderMacroF1 Minimum score: 0.0. Maximum score: 1.0. Higher is better. CompleteCertificateAccuracy This is the fraction of test cases whose complete 8 x 2 matrix exactly equals the hidden matrix. Its 55% weight reflects the operational requirement to return one internally usable cohort record rather than a collection of mostly correct seed guesses. SeedBracketAccuracy For each case, compare its eight bracket rows. A seed is correct only when both endpoints match. SeedBracketAccuracy is the number of exactly correct seed rows divided by 8N, where N is the number of test cases. Its 30% weight preserves meaningful partial credit without reducing the task to independent endpoint accuracy. ImpliedOrderMacroF1 Every bracket matrix implies 28 pair relations. For a pair (X,Y): class B applies when H_X != -1 and H_X <= L_Y; class A applies when H_Y != -1 and H_Y <= L_X; class U applies otherwise because the two censoring intervals do not establish an order. Pool the 28 relations over all test cases. For each class k in {B,A,U}, compute ordinary one-versus-rest F1_k = 2TP_k / (2TP_k + FP_k + FN_k). A zero denominator contributes 1. ImpliedOrderMacroF1 is (F1_B + F1_A + F1_U) / 3. This 15% component rewards scientifically correct ordering consequences while leaving the primary emphasis on the harder interval certificate. A malformed prediction receives zero complete and seed credit for that case. Its 28 relations produce no predicted class and therefore contribute false negatives to the relation component. Hidden malformed values raise an error. Ground truth is never clipped or repaired. What Makes This Interesting The target combines tracking, subtle visual state recognition, and interval censoring. Eight exact brackets create a much larger joint output space than pairwise before-or-after labels, while every entry remains interpretable. The model must preserve uncertainty at the end of the experiment instead of converting missing evidence into a confident biological claim. What Not To Use Do not identify the source collection and retrieve its annotations, omitted photographs, original XML, sequence names, or pretrained source-specific checkpoints. Do not use opaque IDs, path hashes, archive sizes, row order, or repeated leaderboard queries as target proxies. General-purpose vision encoders, tracking models, and image augmentation are allowed. Keep entire dishes and acquisition groups together during local validation. A random case split would place the same photographs and physical seeds on both sides and produce a misleading score. Reference Validation Two clean preparations produced 243 files with byte-identical contents. Train and test feature columns match after removing the target; IDs are unique and exact source-image hashes are disjoint. Exact answers score 1.000000. The packaged sample scores 0.055480, and a position-wise training-mode certificate scores 0.058419. The grader rejects schema, ID, row-count, duplicate-column, and oversized-value attacks.
> 0 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Last Representatives: Taxonomic Branch Loss

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f928b47rpzt2ca2q7spdpas8dxbz6
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview A packet holds ten photographs of small insects and spiders — flies, aphids, ants, parasitoid wasps, leafhoppers, bark beetles, sheet-web spiders. A removal list names some of the ten. Which taxonomic branches lose their last representative when those photographs go? Recognising a removed specimen is not enough. A second specimen of the same genus keeps that genus represented, and another genus from the same family keeps the family represented. The answer depends on what stays behind as much as on what leaves. Each packet draws its ten photographs from four to seven genera, with one to four specimens per genus, in shuffled order; four, five or six slots are then marked for removal. How many genera a packet holds, how the ten photographs divide among them, and how many slots are removed all vary from packet to packet and are not published for any individual packet. The genus vocabulary is deliberately close: 82 genera from 14 families in 5 orders, dominated by small flies — non-biting midges, dark-winged fungus gnats, lesser dung flies, biting midges, scuttle flies, leaf-miner flies, vinegar flies and house flies — plus aphids, ants, braconid wasps, leafhoppers, ambrosia beetles and sheet-web spiders. Several genera inside a family separate only by subtle characters at this resolution. Supervision is weak on purpose. Only 20 photographs per genus carry an individual genus label, and none of them appear in a packet. Packet photographs carry no individual label at all: a training packet gives only its packet-level answer. Working out what a lost or retained branch implies about the removed and the retained photographs is part of the task. Evaluation For each test packet the score is the intersection over union of the predicted and the true set of lost branch IDs, and two empty sets score 1. The final score is the mean over all 400 test packets; higher is better, and it lies between 0 and 1. The published taxonomy has order, family and genus nodes, and each node stands for the branch ending at it; the root and the species rank are not scored. Take the union of the taxonomy paths of all ten specimens, then the union over the retained specimens only. The lost set is the first union minus the second, counting each branch once. Removing one of two specimens of a genus does not erase that genus; removing both does, and its family follows only when no other genus of that family remains. Reference points measured on the sealed test packets from the public files alone: the empty-set submission scores 0.115; a classical CPU pipeline on hand-built image features 0.096; a linear model on features from the supplied checkpoint 0.387; and the strongest solver measured during authoring 0.571. Dataset 1,000 training packets, 200 validation packets and 400 test packets, plus an auxiliary set of labelled photographs. Files train.csv and validation.csv: sample_id, images_json, removed_json, lost_branches. test.csv: sample_id, images_json, removed_json. train_images.csv: the auxiliary labelled photographs, 20 per genus, with image, label and group. These appear in no packet. schema.json: genus class indices, branch IDs, each genus's order/family/genus path, the packet size, the possible genus counts, the range of specimens per genus, the possible removed counts and the auxiliary count per genus. images/: RGB PNG photographs, 224 × 224 pixels, resized with the aspect ratio preserved and padded white. sample_submission.csv: the submission format, filled with empty sets. A generic image checkpoint and the baseline sources (solve.py, coverage.py, grade.py) ship in the public package for offline use. Columns sample_id (string): the packet. images_json (string): a JSON array of ten image paths, relative to the dataset root, in slot order. removed_json (string): a JSON array of four, five or six distinct zero-based slot indices; every other slot is retained. lost_branches (string, training and validation only): a JSON array of the branch IDs that lose their last representative. image, label, group (train_images.csv): photograph path, genus class index, and an anonymous collection-site token. Submission Submit a CSV file with exactly the two columns sample_id,lost_branches, one row per test packet. lost_branches is a JSON array of distinct integer branch IDs from schema.json, from 0 to 100. Use [] for an empty set; the order does not matter. sample_id,lost_branches packet_000123,"[7,42,88]" packet_000124,"[]" Requirements Exactly those two columns, in that order, and every test sample_id exactly once. Each value a JSON array of distinct integers in range. A wrong or reordered column set, an empty table, a missing, extra or duplicate sample_id, or a non-string ID is reported as a file error. A row whose value cannot be decoded — malformed JSON, not an array, booleans, floats, null, negative or out-of-range IDs, duplicates, or deep nesting — scores 0 for that row alone; the other rows are scored normally. Compute One A10G GPU, offline, about 90 minutes. A model may use the auxiliary labelled photographs, the packet photographs with their packet-level answers, and the supplied checkpoint. What not to use These rules are specific to this challenge. External data of any kind. No other photographs, labels, taxonomies, species lists or reference collections, and no attempt to identify a specimen against an outside catalogue. Pretrained weights other than the checkpoint supplied in the package. Test answers or test-time supervision from outside. Packet structure and the published ranges may be used on test packets; anything derived from external sources may not. Hand-entered answers. Every prediction must come from a model or algorithm that reads the supplied photographs. Notes Packets and removal lists are assembled for this benchmark; they do not describe natural co-occurrence, real collections or conservation decisions, and the target measures taxonomic representation rather than evolutionary distance, branch length, abundance or ecological damage. Two properties are worth keeping in mind. The answer is a set, so a packet where every genus has a spare specimen has an empty answer, and predicting the empty set everywhere already scores 0.115. And the target is nested: losing a genus can pull its family and order with it, so an error on one photograph can change several branch IDs at once.
> 0 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Pump Settings And Breakthrough Tips From Flow Videos

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dx7nnn6xd5mxfhry5pkyjwn89hr3w
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Overview In thin transparent lab flow cells, an injected liquid can advance unevenly instead of spreading as a smooth circle. Lab teams do not only need a future picture of the pattern; they need a compact control report: which pump setting and pressure-buffering condition produced the movie, which visible tip may reach the edge first, and whether a higher pump rate would make the pattern split into more branches. You are given short top-down videos of real measured radial front evolution rendered as de-identified lab-cell clips. The videos show a circular glass cell, screws, clamps, tubing, reflections, resident fluid tint, and the growing front. There are no labels, pump readouts, grids, source filenames, scenario tags, or setting text in the videos or public CSVs. For each test clip, predict four quantities: rate_regime, the injection-rate bucket; reservoir_regime, the pressure-buffering/reservoir bucket; breakthrough_tip_json, the visible leading tip or near-tied leading-tip set expected to reach the outer rim first; and cf_branching_dir, the branching-direction change if the pump were raised by one rate regime. Also report calibrated confidence in [0, 1]. rate_regime describes pump speed: low clips spread slowly, moderate and high clips advance faster, and very_high clips are the fastest regime. Faster forcing changes both the time scale and the amount of branching visible in the clip. reservoir_regime describes the connected reservoir or compressibility condition: small, medium, large, and very_large are increasing pressure-buffering buckets that affect how smoothly pressure relaxes and how the front branches. cf_branching_dir asks the counterfactual question "if this same experiment were pumped one rate regime faster, would the front become more branched, less branched, or remain effectively the same/uncertain?" Benchmark-specific task: this is not a living-colony expansion benchmark, a generic shape-growth forecast, a CFD surrogate, or a standard flow-visualization dataset where the target is only viscosity contrast, breakthrough time, raw contour segmentation, or next-frame prediction. No segmentation mask, future frame, or full contour is submitted. Each clip is scored as a structured lab-control decision: infer two hidden operating regimes, localize the leading visible tip set in normalized coordinates, answer an adjacent pump-rate counterfactual, and calibrate confidence. The public media are source-neutral rendered lab-cell clips derived from measured fronts, so the intended signal is video evidence inside the supplied clips rather than matching a known experiment table, published contour, source record, or external growth-pattern benchmark. What Not To Use: do not use filename lookup, row order, archive order, file size, mtime, raw private columns, source-record lookup, source-image/contour matching, external copies of the upstream experiment, hard-coded answer lists, or grader probing. Do not submit a generic captioner, a single-frame color-area heuristic, a plain circular-front detector, a segmentation-only front tracker, a future-frame predictor, or a metadata-only prior as a substitute for visual pump-control reasoning. Hosted or closed-source APIs may not be used for training, pseudo-labeling, or inference. Enforcement on invalid approaches: solutions built around lookup, source reconstruction, rule-only shortcuts, private-file access, platform exploitation, or methods that ignore the video pump-control evidence may be rejected before payout even if they produce a leaderboard score. Dataset The public data contains train videos with labels, test videos without labels, and a sample submission template. Video paths are relative to the public/ root, so a video value such as test/videos/000123.mp4 resolves to public/test/videos/000123.mp4. train.csv contains the public input fields plus the four train-only label columns. test.csv contains only the public input columns. sample_submission.csv is a valid weak baseline in the exact required submission format. train.csv columns rate_regime is one of low, moderate, high, or very_high. reservoir_regime is one of small, medium, large, or very_large. breakthrough_tip_json is a JSON list of [x,y] points in normalized image coordinates, with [0,0] at the top-left and [1,1] at the bottom-right. Use multiple points only when visible leading tips are genuinely near-tied. cf_branching_dir is one of more_branched, less_branched, or same_uncertain. prompt is the same generic instruction text for every row and contains no label values. cf_rate_step is the generic query value raise_one_regime and does not reveal the hidden rate. confidence is not a dataset column; it is a self-reported submission value only. test.csv columns In test.csv, id is the opaque public row id to return in the submission, video is the relative MP4 path to inspect, prompt is the same generic instruction text used in training rows, and cf_rate_step is always raise_one_regime for the pump-up counterfactual. There is no confidence column in test.csv; submit confidence only in your prediction file. Submission Submit a CSV with exactly these columns in exactly this order. Example submission rows: Evaluation Each row receives a correctness score in [0,1]. S_break scores the submitted leading-tip set against the true visible leading-tip set. Let P be the predicted set of normalized [x,y] points and G be the true set. For every predicted point, compute its Euclidean distance to the closest true point; average those distances to get d_pred_to_true. For every true point, compute its distance to the closest predicted point; average those distances to get d_true_to_pred. The symmetric distance is d_sym = 0.5(d_pred_to_true + d_true_to_pred). The size penalty is 1.0 when len(P) = len(G), otherwise max(0.55, 1 - 0.16abs(len(P)-len(G))). Then S_break = exp(-d_sym/0.105)*size_penalty, clipped to [0,1]. Malformed, empty, or oversized predicted tip JSON gives S_break = 0 for that row. S_rate is ordinal partial credit over rate buckets ordered as low, moderate, high, very_high. If i_pred and i_true are the bucket indexes from 0 to 3, then S_rate = max(0, 1 - abs(i_pred-i_true)/3). Exact is 1.0, one bucket off is 0.6667, two buckets off is 0.3333, and three buckets off is 0.0. Invalid rate strings score 0 on this head. S_reservoir is the same ordinal formula over reservoir buckets ordered as small, medium, large, very_large: S_reservoir = max(0, 1 - abs(i_pred-i_true)/3). Invalid reservoir strings score 0 on this head. S_cf is 1.0 only when cf_branching_dir exactly matches the true value and 0.0 otherwise. Allowed values are more_branched, less_branched, and same_uncertain. correctness = 0.38S_break^2 + 0.22S_rate^2 + 0.20S_reservoir^2 + 0.20S_cf^2 calibration = 1 - abs(confidence - correctness) If all row-local predictions are well-formed, row_score = 0.90correctness + 0.10calibration. If the row has malformed tip JSON or an invalid category string, the malformed head scores 0 and calibration credit for that row is 0; other valid rows still count normally. The final score blends mean row performance with robustness across three documented evaluation slices. For each slice, compute the mean row score inside every bucket and take the minimum bucket mean. worst_split_group is the worst bucket over pump-rate families, worst_ood_axis is the worst bucket over branch-density and front-stress regimes, and worst_render_style is the worst bucket over visual styles such as lighting, dye tint, glare, and glass appearance. These terms reward submissions that work across slow and fast experiments, sparse and highly branched fronts, and multiple render styles rather than only on the easiest subset. raw_final = 0.68mean(row_score) + 0.14worst_split_group + 0.10worst_ood_axis + 0.08worst_render_style final = raw_final^1.35 The robustness slices are the physical and visual slices described above; they are used only for final aggregation and are not submission columns. The scoring calculation is fully specified here, so participants should optimize for accurate predictions on every visible test clip rather than for any metadata shortcut. The theoretical minimum is 0.0; the theoretical maximum is 1.0. The grader raises an invalid-submission error for missing, extra, or reordered submission columns; duplicate ids; an id set that does not exactly match the answers; invalid id values; non-finite or out-of-range confidence; or other structural failures that prevent safe row alignment. Malformed or oversized breakthrough_tip_json safely scores zero for that row's tip head rather than crashing the grader, and invalid category strings score zero on their row-local heads while other rows continue to count. A perfect submission with confidence 1.0 scores exactly 1.0. &nbsp;
> 1d ago
> $400–$500
> Revision Requested

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Stir Schedule Retrodiction From Dye Mixing Pattern

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75vwgzj8gj7whcfckzxy5d8588zb2e
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Overview In stirred reactors, pharmaceutical blenders, and lab mixing vessels, an unlogged sequence of impeller actions can determine whether a tracer dye remains in sparse streaks, disperses into plumes, leaves boundary residue, splits into competing eddies, or becomes broadly mixed through the fluid. Process engineers sometimes need to reconstruct the recent control history from the final mixing pattern, identify where the tracer entered, and predict how a specified extra stir would move the dye. This challenge turns that inverse process-control problem into a synthetic 3D-rendered visual benchmark with exact hidden labels, multiple private transport regimes, and vessel imagery that ranges from sparse tracer traces to heavily dispersed dye. You are given one rendered top-down image of a circular vessel containing a tracer dye pattern after a hidden ordered sequence of stir operations. Each row also gives the vessel grid resolution, the number of operations in the hidden schedule, and a query stir type for a one-step forward question. From the image and public query fields, predict the recoverable recent stir schedule, the original dye release cell, the recoverable depth, and the occupied grid cells after applying the queried extra stir. What Not To Use: do not use filename order, row order, filesystem metadata, hashes, private files, answer dictionaries, seed/config reverse-engineering, external lookup tables, hosted closed-source APIs, generic captioning as a substitute for the required structured outputs, a single transport-template replay, or any single-frame color-summary shortcut that ignores vessel-local geometry, regime-dependent dye transport, and the ordered counterfactual query. Enforcement on invalid approaches: rule-only solutions or submissions that do not solve the intended visual fluid-reasoning task may be rejected before payout, regardless of leaderboard score. For each test image submit five fields: schedule_json, release_cell, recoverable_depth, cf_forward_json, and confidence. schedule_json is a JSON list of length schedule_len, ordered from oldest operation to newest operation. Each element is either the string "unknown" or an object with direction in {cw, ccw} and strength in {weak, medium, strong}. release_cell is a vessel-grid cell string such as 3,4. recoverable_depth is an integer count of how many most-recent operations you believe are recoverable. cf_forward_json is a JSON list of occupied grid-cell strings after the queried extra stir. confidence is your estimated probability in [0, 1] that the row is correct. Evaluation Each row receives a correctness score in [0, 1], then the final score blends mean performance with the lowest hidden subgroup mean on each private axis. Higher is better. S_sched = position-weighted ordered schedule score, with newer operations weighted more heavily. S_cf = IoU between predicted and true counterfactual occupied grid-cell sets. S_rel = 1.0 for exact release cell, 0.5 for four-neighbor release cell, 0.0 otherwise. S_depth = exp(-abs(predicted_depth - true_depth) / 1.5). correctness = 0.45 * S_sched^2 + 0.25 * S_cf^2 + 0.20 * S_rel^2 + 0.10 * S_depth^2 calibration = 1 - abs(confidence - correctness) row_score = 0.88 * correctness + 0.12 * calibration Final = 0.68 * mean(row_score) 0.14 * worst_group(row_score) over a hidden mixing-family axis 0.10 * worst_group(row_score) over a hidden transport-regime axis 0.08 * worst_group(row_score) over a hidden render-style axis The grader returns 0.0 if the submission columns are missing, extra, or reordered; if ids are duplicated or do not exactly match the test ids; if confidence is missing, non-finite, or outside [0, 1]; if recoverable_depth is not a valid integer in range; or if a submitted JSON string is over the length limit. Malformed JSON that is not overlong receives zero credit for that affected head instead of crashing. Dataset The public/ directory contains the train and test images, the public CSV files, and a sample submission. The image paths in the CSVs are relative to public/, so a training row with image=train/images/000123.jpg refers to public/train/images/000123.jpg, and a test row with image=test/images/000456.jpg refers to public/test/images/000456.jpg. File overview public/train/images/.jpg contains the rendered training vessel images. public/test/images/.jpg contains the rendered test vessel images. public/train.csv contains input columns and labels for training. public/test.csv contains input columns only. public/sample_submission.csv contains one placeholder row per test id. train.csv columns id is an anonymized integer row id. image is the relative path to the rendered vessel image. grid_res is the vessel-grid side length. schedule_len is the number of hidden stir operations. cf_stir_type is a JSON object describing the queried extra stir. prompt is a short natural-language task instruction. schedule_json is the ordered label list from oldest to newest operation. release_cell is the original dye release cell. recoverable_depth is the true recoverable recent-operation count. cf_forward_json is the true counterfactual occupied-cell list. test.csv columns id is the anonymized integer row id. image is the relative path to the rendered vessel image. grid_res is the vessel-grid side length. schedule_len is the number of hidden stir operations. cf_stir_type is a JSON object describing the queried extra stir. prompt is a short natural-language task instruction. Submission Submit a CSV with exactly these columns in exactly this order: id, schedule_json, release_cell, recoverable_depth, cf_forward_json, confidence. id must match one test row. schedule_json must be a JSON list of length schedule_len; each element is either "unknown" or an object with direction in {cw, ccw} and strength in {weak, medium, strong}. release_cell must be a grid cell string like 2,5. recoverable_depth must be an integer between 0 and schedule_len. cf_forward_json must be a JSON list of grid cell strings. confidence must be finite and in [0, 1]. Example submission format: id,schedule_json,release_cell,recoverable_depth,cf_forward_json,confidence 104,"[""unknown"",{""direction"":""cw"",""strength"":""medium""}]","3,4",1,"[""3,4"",""3,5""]",0.62 205,"[""unknown"",""unknown"",{""direction"":""ccw"",""strength"":""strong""}]","2,6",1,"[""1,6"",""2,6""]",0.57 319,"[""unknown"",""unknown"",""unknown""]","4,3",0,"[]",0.31 &nbsp;
> 1d ago
> $400–$500
> Revision Requested

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Layer-Causality Audit From Sparse Folded-Sheet Stills

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dsxjverz8rh2edr4ygafywx894crb
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Overview Inspectors for deployable structures often receive only the final folded article and must certify how material layers were packed. The same visible crease-line set can be reached by multiple histories, but only some histories are physically meaningful, and independent folds in separate parts of the sheet can leave no evidence of relative order. You are given 2-3 oblique Blender-rendered stills of one folded creased sheet and must infer the causal fold sequence, mountain/valley signs, which fold pairs commute, and a skip-one-fold counterfactual stack height. Each row contains images, a JSON list of 2-3 image paths showing the same folded sheet from different oblique views. The sheet is rendered as a single continuous folded mesh with paper thickness, bevels, faint local grid/fiducial marks, visible crease traces, soft shadows, occlusion, and layer stacking cues. The public crease_pattern_json gives only visible sheet-local crease-line ids, axes, and grid lines; it does not reveal the moved side or fold-action region, and ids are arbitrary. Public article ids and image filenames are anonymized salted identifiers; raw scene hashes, base scenario ids, fold-action regions, and private grouping tags are not participant-facing fields. This is not a visual-to-crease-pattern benchmark. The visible crease-line ids and grid lines are already public inputs. The hard target is a causal layer-stack audit: recover the non-commuting partial order, explicitly mark order pairs that are information-theoretically free, and answer a counterfactual stack-height query for a skipped fold. Similar origami datasets that ask for crease-pattern or mountain/valley recovery from many views do not require this abstention-aware chronology or skip-action counterfactual. For each test row you must output five fields: fold_order_json, a JSON list of crease ids in the recoverable fold sequence; mountain_valley_json, a JSON object mapping every crease id to M or V; free_pairs_json, a JSON list of unordered [crease_id, crease_id] pairs whose relative order is genuinely undetermined because the folds commute; cf_stack_height_bucket, the layer-height bucket at query_point_xy if cf_skip_crease_id were skipped; and confidence, your probability in [0,1] that the structured row is correct. What Not To Do (any of these is grounds for rejection on review, regardless of leaderboard score): Do not force a total order over commuting folds. If two disjoint folds leave no physical trace of which came first, report that pair in free_pairs_json. Do not solve from a single still. The paired oblique views are needed for occlusion and layer-stack evidence. Do not treat this as generic image captioning, folded-paper recognition, or crease counting; the scored outputs are structured fold chronology, mountain/valley signs, commuting-pair abstention, and counterfactual stack height. Do not infer commuting pairs only from public crease-line metadata. The public crease pattern intentionally omits the moving side/region; the free-pair head must be inferred from layer/occlusion evidence and learned training examples. Do not use filename order, row order, image metadata, filesystem timestamps, or public id values as side channels. Do not reverse-engineer seeds, generator internals, or private files; predictions must come only from public images and public CSVs. Do not submit malformed JSON, overlong fields, bad confidence values, or other format hacks intended to exploit the grader. Do not use hosted or closed-source APIs at training or inference time, including pseudo-labeling from such systems. Enforcement on invalid approaches: rule-only solutions or approaches that do not perform the visual/geometric retrodiction task, including caption-only systems or answer lookup schemes, may be rejected before payout even if they produce a nonzero score. Evaluation Each row receives four correctness heads. S_order is pairwise order accuracy over the recoverable partial order only: true commuting pairs are excluded from this order score. S_mv is the fraction of crease ids whose mountain/valley assignment is correct. S_free is Jaccard similarity between the predicted and true unordered commuting-pair sets. S_cf compares the submitted counterfactual stack-height bucket to the true bucket, with exact matches best and adjacent buckets receiving partial credit. correctness = 0.38S_order^2 + 0.22S_mv^2 + 0.22S_free^2 + 0.18S_cf^2 score_core = correctness^1.55 calibration = 1 - |confidence - score_core| row_score = 0.92score_core + 0.08calibration The final score blends mean performance with the lowest subgroup mean on private axes, so solutions must work across crease families, hard commuting/deep-stack cases, and render styles. Final = 0.70 * mean(row_score) 0.12 * worst_subgroup(row_score) # crease-pattern family 0.10 * worst_subgroup(row_score) # difficulty axis 0.08 * worst_subgroup(row_score) # render style The grader raises InvalidSubmissionError for structural CSV failures: incorrect submission header, missing or extra columns, duplicate ids, row-set mismatch, or missing/non-finite/out-of-range confidence. Malformed or overlong row-local JSON degrades only the affected row/head without crashing the whole submission, and malformed row-local content receives no calibration credit. Higher is better. Minimum: 0.0. Maximum: 1.0. Dataset The dataset ships as two splits under public/. Public CSVs use paths relative to the public/ root, such as train/images/_v0.jpg and test/images/_v0.jpg. File overview public/train/images/.jpg are the training folded-sheet stills. public/test/images/.jpg are the test folded-sheet stills. public/train.csv contains public inputs plus labels. public/test.csv contains public inputs only. public/sample_submission.csv is a weak valid submission template. train.csv columns id (int) is the public article id. images (string) is a JSON list of 2-3 still-image paths. grid_res (int) is the flat sheet grid resolution. num_creases (int) is the number of crease ids. crease_ids_json (string) is a JSON list of crease ids. crease_pattern_json (string) is a JSON list of visible crease-line entries with id, axis, and grid_line only. cf_skip_crease_id (string) is the crease skipped for the counterfactual. query_point_xy (string) is a JSON [x,y] point in sheet-local coordinates in [0,1]. prompt (string) states the task. fold_order_json, mountain_valley_json, free_pairs_json, and cf_stack_height_bucket are the labels to predict for test rows. test.csv columns test.csv has the same nine input columns as train.csv and no labels: id, images, grid_res, num_creases, crease_ids_json, crease_pattern_json, cf_skip_crease_id, query_point_xy, and prompt. Submission Submit a CSV with exactly these six columns in this order: id, fold_order_json, mountain_valley_json, free_pairs_json, cf_stack_height_bucket, confidence. fold_order_json must be a JSON list of crease ids. mountain_valley_json must map every crease id to M or V. free_pairs_json must be a JSON list of two-id lists; pair order inside a pair does not matter. cf_stack_height_bucket must be one of 1, 2, 3, 4, or 5plus. confidence must be finite and in [0,1]. Example submission: id,fold_order_json,mountain_valley_json,free_pairs_json,cf_stack_height_bucket,confidence 1024,"[""c17A"",""c92K"",""c33Q""]","{""c17A"":""M"",""c92K"":""V"",""c33Q"":""M""}","[[""c17A"",""c33Q""]]",2,0.42 2048,"[""c21H"",""c44P"",""c11Z"",""c80B""]","{""c21H"":""V"",""c44P"":""M"",""c11Z"":""V"",""c80B"":""M""}","[]",5plus,0.36 &nbsp;
> 1d ago
> $400–$500
> Revision Requested

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Collapse Attribution And Counterfactual Fragility

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77gxqtmz18h6pkn0eb3jrjr188e54c
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Overview You are given a single photoreal still of a freshly-built stack of coloured blocks standing on a flat surface, captured the instant before it is released under gravity. Each stack is built close to its stability boundary, so whether it stands or topples is genuinely uncertain from the image alone. For every scene you must produce three coupled predictions: will_collapse — a probability in [0, 1] that the stack collapses (i.e. at least one block moves appreciably) once released. initiator_block_id — the id of the block that first loses support and triggers the cascade, or "NONE" if the stack is stable. keystone_block_id — the id of the single counterfactual keystone: the one block whose removal would most change the outcome (turning a collapsing stack stable, or a stable stack into a collapsing one). "NONE" if no single-block removal would flip the outcome. Each scene ships with a small roster table listing the blocks by block_id, each with the block's pixel centroid in the image and its RGB colour, so you can refer to a specific block unambiguously in your answer. You see only the rendered pixels and this roster — the masses, friction, and the physics of the release are never given and must be reasoned about. The initiator and keystone questions are deliberately the hard part: they are not "is this stable?" but "who causes the failure?" and "which removal is the highest-leverage intervention?" — a causal, counterfactual judgement that a plain stability classifier cannot make. What Not To Do (any of these is grounds for rejection on review, regardless of leaderboard score): Treat it as a pure stability classifier. Predicting only will_collapse and leaving initiator_block_id / keystone_block_id at a constant is out of scope — the causal heads carry the majority of the score and must be reasoned, not stubbed. Hosted / closed-source APIs at any stage of training or inference (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.), including any distillation or pseudo-labelling from such teachers. Only open-weights models and self-trained pipelines are permitted. Pixel-hash or reverse-image-lookup any still against any external image collection to recover an identity or outcome. The images have been processed so byte-level matching is not reliable; predictions must come from the shipped pixels and the roster columns alone. Filename / order side-channels. Do not assume any structure in the lexicographic ordering of .jpg files, and do not exploit file-system metadata, mtimes, or any signal outside the image pixels and the CSV columns. Format / range hacks. Submitting out-of-range will_collapse values or non-canonical block-id strings to game the grader's clipping/coercion is not allowed. Grader / platform exploitation. Hard-coded answer dictionaries, filesystem probes for private/answers.csv, or any channel that is not public/train/, public/train.csv, public/blocks_train.csv, public/test/, public/test.csv, and public/blocks_test.csv. Evaluation The grader computes, over the full test set: S_collapse = Brier Skill Score of will_collapse vs a static climatology p = predicted P(collapse), y = true outcome in {0,1} MSE_model = mean (p - y)^2 ref = 0.5 (static climatology) MSE_ref = mean (ref - y)^2 = 0.25 S_collapse = clip(1 - MSE_model / MSE_ref, 0, 1) S_initiator = macro-F1 over the initiator classes (block ids + "NONE"), computed over the whole test set. "NONE" is always an equally-weighted scored class; numeric block-id classes are scored when they occur in the ground truth. S_keystone = mean keystone accuracy. Per scene: 1.0 if the predicted keystone equals the true top-1 keystone, 0.5 if it equals the second-most-impactful block, else 0.0. Final = 0.30 * S_collapse^2 0.35 * S_initiator^2 0.35 * S_keystone^2 clipped to [0, 1] S_collapse is a Brier Skill Score: a constant predictor (the base rate, or 0.5 everywhere) scores 0; a perfectly calibrated set of outcomes scores 1. S_initiator is macro-averaged F1 over the block-id classes plus "NONE". "NONE" is always scored with equal weight, so an "always NONE" submission cannot coast; a block-id class absent from the ground truth is excluded so it cannot inflate the average. S_keystone rewards the counterfactual judgement, with partial credit for the second-best block. Each sub-score is squared before weighting, so a strong-but-naive model cannot coast to a high composite; a perfect solution (all three sub-scores 1.0) still reaches the maximum 1.0. The two causal heads carry the dominant 0.70 weight. Higher is better. Minimum: 0.0, Maximum: 1.0. A row missing from the submission — or whose id is not in test.csv — causes the grader to return 0.0. The grader also returns 0.0 on duplicate ids, a missing required column, or any exception during parsing. Out-of-range will_collapse values are clipped to [0, 1] (non-numeric → 0.5); block-id values that are not a non-negative integer or "NONE" are coerced to "NONE". Dataset public/train/images/.jpg — one RGB still per training scene. public/test/images/.jpg — one RGB still per test scene. public/train.csv — per training scene: id, image_path, n_blocks, and the three targets will_collapse, initiator_block_id, keystone_block_id. public/test.csv — per test scene: id, image_path, n_blocks. No targets. public/blocks_train.csv, public/blocks_test.csv — one row per (scene, block) giving the block roster (id, pixel centroid, colour). public/sample_submission.csv — one row per test id in the submission format, filled with weak placeholders that must be overwritten. Row counts are seed-dependent and printed by prepare.py (typical: a few thousand train scenes and ~half as many test scenes). File overview | Item | Description | |-------------------------------|-----------------------------------| | public/train/images/*.jpg | Block-stack still (train) | | public/test/images/*.jpg | Block-stack still (test) | | public/train.csv | Scene targets (train) | | public/test.csv | Scene ids only (test) | | public/blocks_train.csv | Block roster (train) | | public/blocks_test.csv | Block roster (test) | | public/sample_submission.csv| Submission template | train.csv columns | Column | Type | Description | |----------------------|--------|----------------------------| | id | int | Unique scene id | | image_path | string | Relative path to the still | | n_blocks | int | Number of blocks in scene | | will_collapse | int | 1 if stack collapses | | initiator_block_id | string | Block id or "NONE" | | keystone_block_id | string | Block id or "NONE" | test.csv columns | Column | Type | Description | |--------------|--------|----------------------------| | id | int | Unique scene id | | image_path | string | Relative path to the still | | n_blocks | int | Number of blocks in scene | blocks_train.csv / blocks_test.csv columns | Column | Type | Description | |------------|------|--------------------------| | id | int | Scene id | | block_id | int | Block id within scene | | cx | int | Block centroid x (pixel) | | cy | int | Block centroid y (pixel) | | color_r | int | Block colour R (0-255) | | color_g | int | Block colour G (0-255) | | color_b | int | Block colour B (0-255) | Submission Submit a CSV with a header row and exactly one row per id in test.csv, with these 4 columns in this order: id, will_collapse, initiator_block_id, keystone_block_id. | Column | Type | Constraint | |----------------------|--------|--------------------------| | id | int | Same set as test.csv | | will_collapse | float | P(collapse) in [0, 1] | | initiator_block_id | string | Block id or "NONE" | | keystone_block_id | string | Block id or "NONE" | Requirements: Header row plus exactly one row per test id; the id set must match test.csv exactly. Duplicate ids cause the grader to return 0.0. will_collapse is a float in [0, 1]; out-of-range values are clipped and non-numeric cells default to 0.5. initiator_block_id and keystone_block_id are a non-negative integer block id (as a string) or "NONE". Anything else is coerced to "NONE". A row-set mismatch, a missing required column, or any parsing exception causes the grader to return 0.0. Example of a correctly formatted submission file (illustrative only): id,will_collapse,initiator_block_id,keystone_block_id 4000,0.92,5,4 4001,0.07,NONE,NONE 4002,0.61,2,2 &nbsp;
> 8d ago
> $400–$500
> Accepted

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Annotator Reliability And Adversarial Rater Detection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c2a9h3r8tw4rhjn9419vafs846jp2
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Overview This is a Computer Vision / Medical Imaging challenge that breaks the standard "image → label" supervised setup by adding a per-row annotator-roster table. For every test patch the solver receives a 96×96 RGB H&E (Hematoxylin & Eosin) histology tile plus five noisy binary votes — each cast by a synthetic annotator with a private, fixed reliability profile, and each accompanied by a self-stated confidence score in 0, 1]. The solver's job is to recover three structured outputs per row: pred_consensus — a binary class label in {0, 1} predicting whether the centre 32×32 region of the patch contains metastatic tumour tissue (the gold-standard binary label for the patch). pred_rel_1, …, pred_rel_5 — five floats in [0, 1] estimating each rater's intrinsic reliability: that rater's long-run probability of voting correctly, a fixed property of the (hidden) profile it was drawn from. This target is not a function of the gold consensus on this row — a reliable rater can be wrong on a given patch and an unreliable one can be right — so it cannot be recovered by simply comparing the observable rater labels to a consensus guess. It must be inferred from the image, the rater's stated confidence, and the cross-rater agreement pattern. pred_adversarial_idx — a categorical value in {"1", "2", "3", "4", "5", "NONE"} naming which rater (if any) is from a deliberately-confident-but-wrong "adversarial" pool. Some rows contain one adversarial rater; the rest contain none. The exact frequency at test time is not advertised but is observable in the training labels. The five raters per row are sampled from a private pool of fixed reliability profiles with different accuracy and confidence signatures. The pool includes one adversarial profile — a rater that casts its vote with high stated confidence but is mostly wrong — alongside several non-adversarial profiles of varying skill. Profile names and the rule that maps a profile to its behaviour are never in the public CSVs — the solver sees only the per-row labels, confidences, and (on training rows) the gold consensus, the float true_rel_i reliability targets, and the true_adversarial_idx. This problem is fundamentally a joint image + tabular task. Important property of the rater pool: the non-adversarial raters are noisy enough on their own that a closed-form majority vote over the five rater labels is barely better than chance at recovering the gold consensus. A solver that ignores the image and only aggregates the rater table will under-perform a solver that consumes both. Likewise, a solver that ignores the rater table (image-only binary classification) cannot recover the per-row reliability or the adversarial rater identity. A small fraction of training consensus labels carry irreducible noise — the rate is not advertised — and the test labels stay clean. The H&E patches have been processed so that pixel-level matching against external collections is not feasible, and the same processing is applied identically to train and test so the pixel-statistic distributions match. Evaluation The grader computes, over the full test set: S_consensus = mean over rows of [1 if pred_consensus == true_consensus else 0] S_reliability = Brier Skill Score of the reliability predictions against a climatological reference. Over all (row, rater) pairs: MSE_model = mean (pred_rel_i - true_rel_i)^2 ref = mean(true_rel_i) (climatology) MSE_ref = mean (ref - true_rel_i)^2 S_reliability = clip(1 - MSE_model / MSE_ref, 0, 1) true_rel_i is each rater's intrinsic reliability in [0, 1. S_adversarial = macro-F1 across the adversarial classes {"1", "2", "3", "4", "5", "NONE"}, computed over the entire test set. "NONE" is always an equally-weighted scored class; the numeric slot classes are included when they occur in the ground truth. Final = 0.25 * S_consensus^2 0.25 * S_reliability^2 0.50 * S_adversarial^2 clipped to [0, 1] S_consensus is straightforward classification accuracy: 1 for an exact match on the binary class, 0 otherwise. S_reliability is a Brier Skill Score: the mean squared error of your reliability estimates is normalised against the error of the climatological baseline (predicting the dataset-wide mean reliability for every rater). A constant predictor — 0.5 everywhere, or the mean itself — scores exactly 0, so there is no "guess a constant" floor; a perfect estimate scores 1. Because true_rel_i is the rater's intrinsic profile reliability rather than its per-row agreement with the gold label, this head is independent of the consensus head and cannot be reconstructed by comparing the observable rater labels to a consensus guess. S_adversarial is macro-averaged F1 across the adversarial identities (5 rater slots + "NONE"), aggregated once over the test set. "NONE" is always an equally-weighted scored class — it is never dropped and never up-weighted for being the majority. A numeric slot class absent from the ground truth is excluded from the average so it cannot inflate the score with a spurious perfect 1.0. A trivial "predict NONE everywhere" submission scores only about 0.14 (only the "NONE" class is recovered, the numeric-position classes are F1 = 0), well below what a learned model achieves. Identifying the adversarial rater is the genuinely hard, non-image-only part of the task, so it carries the dominant 0.50 weight. Each sub-score is squared before weighting. Squaring compresses the high end (e.g. an 0.85 sub-score contributes as 0.72), so a strong image-only classifier cannot coast to a high composite on the consensus and reliability heads. A perfect solution (all three sub-scores 1.0) is unaffected and still reaches the maximum 1.0. Higher is better. Minimum: 0.0, Maximum: 1.0. A row that is missing entirely from the submission — or whose id does not appear in test.csv — causes the grader to return 0.0. Likewise, the grader returns 0.0 if the submission contains duplicate ids, is missing any required column, or otherwise raises an exception during parsing. pred_rel_i values out of range are clipped to [0, 1]. Non-binary pred_consensus values are coerced to 0 (worst case) by the grader. pred_adversarial_idx values that don't match the canonical six-class set are coerced to "NONE". Submitting illegible / corrupt cells therefore degrades the score smoothly rather than zeroing the whole submission. Dataset public/train/images/.jpg — 96×96 RGB JPEG, one per training row. public/test/images/.jpg — 96×96 RGB JPEG, one per test row. public/train.csv — labels and rater table for training rows, including the gold true_consensus, the float true_rel_1..5 reliability targets in [0, 1], and the true_adversarial_idx. A small fraction of true_consensus values carries irreducible noise. public/test.csv — the same id, image_path, and rater table for test rows. No labels. public/sample_submission.csv — one row per test id in the exact submission format. The shipped values are deliberately weak placeholders (pred_consensus = 0, pred_rel_i = 0.5, pred_adversarial_idx = "NONE"); participants must overwrite all three heads to score meaningfully. Row counts are seed-dependent and printed at the end of prepare.py (typical: 8,000 train rows and 4,000 test rows; one row = 1 JPEG + 1 CSV row). File overview Files shipped to participants: public/train/images/.jpg (96×96 RGB H&E patches, one per training row), public/test/images/.jpg (96×96 RGB H&E patches, one per test row), public/train.csv (labels + rater table for training rows), public/test.csv (ids + rater table only, no labels), and public/sample_submission.csv (submission template with the full 8-column shape). Feature Details The columns differ between the training CSV, the test CSV, and the submission CSV. They are listed separately so there is no ambiguity about which columns belong to which file. Training data columns (public/train.csv) — 19 columns: Columns (in order): id (int), image_path (string), rater_1_label (int), rater_2_label (int), rater_3_label (int), rater_4_label (int), rater_5_label (int), rater_1_conf (float), rater_2_conf (float), rater_3_conf (float), rater_4_conf (float), rater_5_conf (float), true_consensus (int), true_rel_1 (float), true_rel_2 (float), true_rel_3 (float), true_rel_4 (float), true_rel_5 (float), true_adversarial_idx (string). Test metadata columns (public/test.csv) — 12 columns: Columns (in order): id (int), image_path (string), rater_1_label (int), rater_2_label (int), rater_3_label (int), rater_4_label (int), rater_5_label (int), rater_1_conf (float), rater_2_conf (float), rater_3_conf (float), rater_4_conf (float), rater_5_conf (float). No label columns are present. Submission columns (public/sample_submission.csv and your final submission) — 8 columns: Columns (in order): id (int), pred_consensus (int, 0 or 1), pred_rel_1 (float in [0,1]), pred_rel_2 (float in [0,1]), pred_rel_3 (float in [0,1]), pred_rel_4 (float in [0,1]), pred_rel_5 (float in [0,1]), pred_adversarial_idx (string, one of "1","2","3","4","5","NONE"). Submission Submit a CSV file with a header row and exactly one row per id in test.csv. The header must contain these 8 columns in this order: id, pred_consensus, pred_rel_1, pred_rel_2, pred_rel_3, pred_rel_4, pred_rel_5, pred_adversarial_idx. Requirements: Header row plus exactly one row per id in test.csv — id must equal exactly the set in test.csv. Duplicate ids cause the grader to return 0.0. pred_consensus must be an integer in {0, 1}. Non-binary values are coerced to 0 (worst case) by the grader. pred_rel_1 … pred_rel_5 must be floats in [0, 1]. Out-of-range values are clipped; non-numeric cells default to 0.5. pred_adversarial_idx must be one of the six strings "1", "2", "3", "4", "5", "NONE". Anything else (including 0, blank, or a numeric out of 1..5) is coerced to "NONE" by the grader. Missing rows are not silently filled in — a row-set mismatch causes the grader to return 0.0. The grader returns 0.0 if any of the eight required columns are missing from the submission, if the submission contains duplicate ids, or if it raises any exception during parsing. Example of a correctly formatted submission file (illustrative only): The three rows below come from three different test ids. The full submission has one row per test id. The placeholders show the column layout — real submissions will have informative per-row predictions. id,pred_consensus,pred_rel_1,pred_rel_2,pred_rel_3,pred_rel_4,pred_rel_5,pred_adversarial_idx 8000,1,0.91,0.62,0.74,0.08,0.55,4 8001,0,0.83,0.71,0.66,0.79,0.69,NONE 8002,1,0.40,0.86,0.92,0.29,0.51,1 What Not To Do Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score: Submit closed-form rule-only outputs that ignore the image. A formula like pred_rel_i = mean(|rater_i_label - majority_label|) or a pure rater-agreement statistic with no learned image component is out of scope — the challenge is meant to be solved by joint image + tabular reasoning. Isolate the adversarial rater from stated confidence alone. Any heuristic or rule-based system that picks pred_adversarial_idx purely from the self-stated confidence scores (e.g. "the rater with the highest confidence is the adversary") without processing the image patch is out of scope. The adversarial profile's confidence band deliberately overlaps an honest specialist's, so confidence alone cannot separate them — telling an adversary apart from an honest-but-wrong expert requires reasoning jointly over the image evidence and the full rater pattern. Hosted / closed-source APIs at any stage of training or inference (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.), including any distillation / pseudo-labelling from such teachers. Only open-weights models and self-trained pipelines are permitted. Externally pretrained classifiers used as a black-box consensus head — i.e., loading any third-party H&E-tile checkpoint that was already fine-tuned for binary metastasis classification on a public corpus, and submitting its argmax as pred_consensus while ignoring the rater table. Generic ImageNet / DINOv2 / CLIP backbones are fine; any solution that does not consume the rater-roster columns is rejected on review. Pixel-hash any visible JPEG against any public H&E archive in order to recover the underlying patch identity or gold consensus. The patches have been processed so byte-level lookup is not reliable; the consensus and rater-roster labels must be recovered from the provided JPEG pixels and the CSV columns alone. Filename / order side-channels. Do not assume anatomical adjacency, slide order, or any other structure in the lexicographic ordering of .jpg files; do not exploit file-system metadata, file mtimes, or any signal outside the JPEG pixels and the CSV columns. Format / range hacks that game the grader. Submitting non-binary pred_consensus values, padding pred_adversarial_idx with non-canonical strings, or supplying out-of-range pred_rel_i values to deliberately exploit the grader's clipping behaviour. Grader / platform exploitation. Hard-coded answer dictionaries, filesystem probes for private/answers.csv, attempts to read hidden splits, or any channel that is not public/train/, public/train.csv, public/test/, and public/test.csv. &nbsp;
> 8d ago
> $400–$500
> Accepted

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Joint Visual Analogue Matching for Laboratory Scenes

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79fswzdtrr5k9680xvggrb958e140a
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 0.488!

Full challenge description from page:

> Overview Match three laboratory photographs to three different visual analogues chosen from a five-image candidate bank. Predict one assignment: which candidate best represents each reference scene when a candidate cannot be reused. Laboratory image collections contain clear liquids, cloudy mixtures, settled solids, and deposits on glass. When assembling a comparison sheet, three independent searches can repeatedly choose the same example and leave another scene poorly represented. This task evaluates the joint choice instead: the best complete assignment can require accepting a second-best individual match. The photographs are real crops from videos of transparent reaction vessels during mixing, dissolution, settling, and evaporation. Reflections, wall deposits, illumination changes, and suspended material make appearance comparisons difficult. Human-drawn material-region rectangles provide the training supervision. The matching rule compares their category counts, vertical distributions, and overlaps. It measures visual similarity under that explicit rule, not chemical equivalence, purity, reaction success, or safe handling. Dataset Each request contains eight separate photographs, not a rendered board. reference_images gives three ordered references, R1 through R3. candidate_images gives five ordered candidates, A through E. The letters are local positions in these arrays and have no global material identity. The images show close views of vessels and their contents; no class boxes or target labels are drawn on the public JPEGs. | File or directory | Contents | |---|---| | train.csv | 4,735 requests, with columns case_id, reference_images, candidate_images, analogue_assignment, in that order. | | test.csv | 1,039 requests with only case_id, reference_images, candidate_images, in that order. | | training_regions.csv | Region annotations and validation groups for the 4,735 training catalog photographs. It contains image_path, phase_regions, validation_group. It contains no test photographs. | | sample_submission.csv | One schema-valid, deliberately untrained prediction per test ID. Complete assignments are resampled from training labels without consulting test targets. Its columns match the required submission. | | images/ | 5,774 unique JPEG photographs referenced by the CSV arrays: 4,735 in the training catalog and 1,039 in the test catalog. Widths range from 120 to 528 pixels and heights from 194 to 1,040 pixels. Original visible pixels are retained. Every file occupies 140,000 bytes; file length is not a scene feature. | Paths are relative to the directory containing train.csv and test.csv, for example images/material_7f4e8fc0ba94f8400482ee85.jpg. A photograph is stored once and can participate in several requests within its own split. Request Columns | Column | Data type | Meaning | |---|---|---| | case_id | string | Opaque request identifier, match_ followed by 24 lowercase hexadecimal characters. | | reference_images | JSON-encoded string array | Exactly three image paths in R1, R2, R3 order. | | candidate_images | JSON-encoded string array | Exactly five image paths in A, B, C, D, E order. | | analogue_assignment | string, training target | Three distinct candidate letters joined by >, in reference order. E>A>D assigns R1 to E, R2 to A, and R3 to D. | For the training request match_574cfbce669ee015da240e53, the actual image order and label are: | Role | Image path | |---|---| | R1 | images/material_7f4e8fc0ba94f8400482ee85.jpg | | R2 | images/material_9b0af55c0b2ddd8018009136.jpg | | R3 | images/material_6cfb4813c8f17790aa9a474a.jpg | | A | images/material_fb0ce429cb76b2baf3f7ab5b.jpg | | B | images/material_60c549c7aa960bd226014cc4.jpg | | C | images/material_54edc68d8cc5fbcd14db23d4.jpg | | D | images/material_10f8f50f7978e0635b426637.jpg | | E | images/material_ecc165bab8fb7cebce772ea2.jpg | The label is E>A>D. The order of each array matters; there is no chronological ordering across the photographs. Auxiliary Training Annotations | Column | Data type | Meaning | |---|---|---| | image_path | string | A training catalog JPEG path, appearing once in this annotation table. | | phase_regions | JSON-encoded nested array | Between one and eight distinct regions, each [category,x0,y0,x1,y1]. Coordinates are finite numbers from 0 to 1, normalized by the full image width and height. The origin is the upper-left corner, x increases rightward, and y increases downward. Each box has positive width and height. | | validation_group | string | Opaque identifier for a conservative training source family. Keep complete groups together when constructing internal image-level validation pools and all request components. This is validation metadata, not a prediction feature. | | Category | Visible appearance described by the annotations | |---|---| | homogeneous | Clear, visually uniform liquid. | | heterogeneous | Cloudy or nonuniform liquid. | | residue | Deposited solid on a vessel region above the liquid. | | empty | Clear air space inside the vessel. | | solid | Visible solid material, including suspended particles or a settled region. | Different categories may overlap. These are rectangles, not pixel segmentation masks. In particular, a rectangle enclosing suspended solid can overlap the rectangle for a cloudy liquid. Do not interpret every pixel in such a rectangle as a chemically pure material. Composition And Split The source has 6,031 images. Two images with zero-area annotations are excluded; 255 duplicate copies are removed from the remaining 6,029, leaving 5,774 unique photographs. Exactly repeated annotation lines are collapsed. Experiment sequences, known shared visual setups, and exact duplicates are grouped transitively before splitting. There are 38 training families and 22 test families, with no shared component family or identical image across the split. Every request uses eight different families from its own split. One request is anchored on each retained catalog photograph. Additional references and candidates are drawn from the same local catalog, so 4,735 and 1,039 are request counts, not independent experimental acquisitions. All 60 legal assignments occur in both splits. The test count is 21.94% of the training count. | Target coverage | Training | Test | |---|---|---| | Distinct legal assignments present | 60 of 60 | 60 of 60 | | Minimum requests for one complete assignment | 60 | 7 | | Maximum requests for one complete assignment | 97 | 28 | | Evaluation assignments absent from training | Not applicable | 0 | Catalog reuse is capped at 48 requests per photograph. The realized maxima are 39 in training and 33 in test; the medians are 6 and 7. The split blocks known source-family memorization, but the underlying collection does not supply a complete physical-apparatus identity registry. No claim of wholly independent laboratories is made. Matching Rule Training targets are derived from the provided region annotations. Test annotations are not supplied. A solver can learn region recognition or a comparison representation; the following definition states exactly which visual relationships determine the assignment. Image Descriptor Use category order homogeneous, heterogeneous, residue, empty, solid. Enclose all annotated boxes in their smallest common axis-aligned rectangle. This rectangle defines a comparison frame; it is not a prediction of the physical vessel boundary. Place a 32 by 32 lattice of cell centers in that frame. In normalized image coordinates, center (j,i) is x_min + (j+0.5)(x_max-x_min)/32, y_min + (i+0.5)(y_max-y_min)/32, with i and j from 0 through 31. For each category, mark a center if it lies in at least one of that category's rectangles. Lower edges are inclusive and upper edges exclusive: x0 A>C, with total cost 4. This toy table explains the constraint; it is not an additional public input. Submission Format Write the final CSV to exactly ./working/submission.csv. It must contain exactly these columns in this order: case_id,analogue_assignment. | Column | Required type and format | |---|---| | case_id | String copied exactly from test.csv. Include every test ID once. | | analogue_assignment | Exactly five ASCII characters: three distinct uppercase letters from A through E, separated by two > characters. There are no spaces, brackets, trailing newline characters inside the value, confidence scores, or extra tokens. | Valid example, shown as the two CSV fields: | case_id | analogue_assignment | |---|---| | match_1300c2a0a6edcc92ad6d265a | A>E>D | The example demonstrates formatting, not a correct test answer. Row order may differ from test.csv; column order may not. Extra or missing columns, duplicate columns, wrong row counts, duplicate IDs, and unknown IDs reject the submission. An invalid assignment value, including repeated candidate letters or an overlong string, receives zero for that request. The parser checks the five-character bound before interpreting the letters. Evaluation The Joint Analogue Assignment Score measures correct individual matches and complete comparisons. Minimum score: 0.0. Maximum score: 1.0. Higher is better. For test request i, let k_i be the number of reference positions assigned the correct candidate, from zero to three. A malformed assignment has k_i = 0. For N evaluated requests: | Component | Formula | Weight and rationale | |---|---|---| | LinkScore | sum_i(k_i/3) / N | 0.50: individual matches remain the main useful output and receive gradual credit. | | PairCompletionScore | sum_i(k_i*(k_i-1)/6) / N | 0.30: this is the fraction of the three reference pairs for which both assignments are correct. It rewards comparisons that can actually be used together. | | SheetCompletionScore | sum_i I(k_i=3) / N | 0.20: all three matches must be correct before the whole comparison sheet is complete. | Score = 0.50 * LinkScore + 0.30 * PairCompletionScore + 0.20 * SheetCompletionScore. I(condition) is 1 if the condition holds and 0 otherwise. Every request has equal weight. These components deliberately measure increasing completeness of the same assignment; they are not three independent prediction targets. With 0, 1, 2, or 3 correct links, a request receives respectively 0, 1/6, 13/30, or 1. There is no extra language, coherence, frequency, or hidden-context bonus. A uniformly random legal assignment has expected score 71/600, approximately 0.11833. This chance floor is reported rather than hidden by a nonlinear rescaling. Exact answers receive 1.0. Invalid hidden labels are treated as a dataset error and raise an exception instead of being clipped or repaired. Simple Modeling Approach Train a small image encoder or region detector using training_regions.csv, then predict the comparison descriptors defined above. Cache one descriptor per photograph, calculate the 3-by-5 distance table for each request, and select the lowest-cost assignment among the 60 ways to choose three distinct candidates. For validation, keep validation_group families together and ensure every image in a validation request belongs to its held-out pool. This is an optional starting point, not a required architecture. and its a fairly simple and easy challenge quick to solve. What Makes This Interesting Recognizing an inventory is insufficient: the distribution and overlap of those materials influence which scene is a useful analogue. Matching each reference separately is also insufficient by construction. The task combines learned visual comparison with a small, exact allocation constraint, so an otherwise good pairwise model must manage competing choices. The photograph bank is reusable within a split, allowing image representations to be cached rather than repeatedly decoding the same media. What Not To Use Do not derive predictions from IDs, path strings, file sizes, row order, request frequency, or other packaging artifacts. Do not match the photographs to external source collections to retrieve annotations or use pretrained checkpoints specifically trained on this collection. General-purpose pretrained models and learned or classical image methods are allowed. Use the supplied training annotations for learning and properly grouped internal validation. Do not obtain evaluation labels through external lookup, manual source matching, leaderboard probing, or malformed submissions. Do not treat repeated catalog appearances as independent evidence of a hidden label. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The complete solution must finish within 90 minutes end to end, including data loading, preprocessing, feature extraction, training or adaptation, validation, inference, structured decoding and submission writing. This is a total execution limit, not a separate allowance for each stage. The platform may terminate execution at the limit; use elapsed-time checks and retain the best completed model so that a valid submission is written before the deadline. Start with a small end-to-end run and write a valid full-test submission early. Use a wall-clock timer from process start, avoid exhaustive searches and large ensembles, and reserve at least the final 10 minutes for inference and submission checks; increase this reserve if measured throughput requires it. Cache encoder outputs only while the encoder is frozen
> 4 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Locate and Type the Stitch Defects in an Inspection Order

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bnv7s5afgwnqaag13ksn2dn8ean3t
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 0.412!

Full challenge description from page:

> Overview Mark the pixels of requested stitch defects and label each marked pixel with its defect type. Each input is a real fabric photograph plus an inspection order naming three defect types. Do not mark unrequested defects. A quality-control system needs to distinguish a broken stitch from a stain, not just draw a generic damaged region. The photographs and pixel labels are publisher-provided fabric inspections. The revision retains defect identity instead of collapsing all requested defects into one foreground mask. Dataset | Path | Format | Contents | |---|---|---| | train.csv | UTF-8 CSV | 8,660 labelled examples; input columns followed by target columns. | | test.csv | UTF-8 CSV | 1,995 examples containing input columns only. | | sample_submission.csv | UTF-8 CSV | One schema-valid baseline row per test case, in the required answer format. | | images/ | Image directory | 10,655 files used by the CSV paths. These paths are relative to the public directory. | train.csv columns, in order: case_id, image_path, reject_defect_types, rejected_region. test.csv columns, in order: case_id, image_path, reject_defect_types. The organizer-only answers.csv contains case_id, rejected_region in that order. Its rows correspond exactly to test IDs and its target formats are the same as submission formats. It is not an input to the solution. Input Columns | Column | Data type | Meaning | |---|---|---| | case_id | string | Opaque image-order ID. | | image_path | string | Relative path to a 224x224 RGB JPEG in images/. | | reject_defect_types | JSON-encoded string | Exactly three requested defect names from the codebook below. | Target Columns in Training | Column | Data type | Meaning | |---|---|---| | rejected_region | JSON-encoded string | Typed row-major runs [defect_code,start,length] for requested pixels. | Defect Codes and Run Encoding Codes: 1 skipped stitch, 2 broken stitch, 3 pinched fabric, 4 crooked seam, 5 thread sagging, 7 stain or damage, 10 overlapped stitch. Unmarked pixels have implicit code 0. Codes 6,8,9 are not defined. The images contain real thread, seam, fabric and surface texture. Masks use the publisher's pixel classes. Flatten the 224x224 image row by row starting at top-left index 0. [2,225,3] assigns broken-stitch code 2 to indices 225,226,227. Sort runs first by code then by start. Within a code, touching runs must be merged. Runs of any codes must not overlap. The canvas has 50,176 pixels. Predict [] when no requested defect is present. Preparation keeps the original images and labels. For an image containing defects, the request includes at least one present type, avoiding mostly empty orders; remaining types can be absent. Normal images remain negative cases. No target-dependent visual transformation is applied. A wrong defect code is both a missed true-class pixel and an extra predicted-class pixel. Example Input This is an actual labelled training example. JSON below shows the CSV cell values; arrays stored in a CSV cell remain JSON-encoded strings. { "case_id": "case_98f9de9189a47d7c2e838870", "image_path": "images/case_98f9de9189a47d7c2e838870.jpg", "reject_defect_types": "[\"pinched fabric\",\"thread sagging\",\"overlapped stitch\"]" } Split and Independence Complete fabric groups are held out: denim and nylon form evaluation while other fabric groups form training. Exact decoded copies crossing splits, or carrying contradictory masks, are excluded; remaining exact image copies are deduplicated. Image-order cases are not replicated with alternative orders. Similar seam geometries can remain across fabrics. This tests fabric transfer, not camera or manufacturer independence. Target Distribution The table counts submitted-list entries, not independent source observations. For masks, an entry is a run, not a pixel. Media and document reuse are described above. | Split | Target | Empty sets | Minimum entries | Median entries | Maximum entries | |---|---|---|---|---|---| | train | rejected_region | 1930 | 0 | 16.0 | 327 | | test | rejected_region | 420 | 0 | 17.0 | 324 | Evaluation The Typed Inspection Score has Minimum score 0.0 and Maximum score 1.0; higher is better. For each case with nonempty truth, TP counts correctly typed nonbackground pixels, FN true nonbackground pixels whose prediction differs, and FP predicted nonbackground pixels whose truth differs. CaseScore = TP/(TP + 2*FN + FP). Let A be the mean CaseScore over nonempty-truth cases. Let B be the fraction of empty-truth cases predicted exactly empty. FinalScore = 0.80*A + 0.20*B. If an evaluated subset lacks either group, renormalize the remaining weight to one. This weighting and missed-pixel penalty are unchanged; typing is the added requirement. The 80% term prioritizes finding requested defects, the 20% term retains false-alarm control, and weighting FN twice reflects missed inspection defects. Malformed typed runs score zero for that case. A wrong code on a true defect contributes to both FN and FP. Background accuracy is not otherwise rewarded. Invalid truth raises. Always predicting [] earns 0.2 only when both groups are represented, not evidence of an effective model. Submission Format Write the final UTF-8 CSV to /submission/submission.csv. Exact header: case_id,rejected_region. | Column | CSV data type | |---|---| | case_id | string | | rejected_region | string containing a JSON array | JSON array of at most 8,192 triples and 262,144 characters. All triple values are integers, not booleans. Code must be in the codebook; start >= 0, length > 0, start+length <= 50,176. No overlaps, and no touching same-code runs. Canonical ordering is mandatory. Example submission row, taken from the training example above: case_id,rejected_region case_98f9de9189a47d7c2e838870,"[[5,25984,56],[5,26208,2464]]" Use one row for every test ID. Rows may be reordered, but column order must match the header. Extra or missing columns, duplicate column names, duplicate IDs, extra rows, missing rows, and unknown IDs reject the submission. IDs must be strings matching case_ followed by 24 lowercase hexadecimal characters. Targets must be JSON strings, not Python expressions. NaN, infinity, booleans, objects in place of arrays and overlong fields are not valid target values. Computation and Allowed Methods A conditional semantic-segmentation model can use the requested type list to mask unrequested classes. Classical CPU and pretrained image methods are allowed. Train only on the supplied training labels. Public inputs can be used for prediction and preprocessing. A pre-trained model is allowed unless the hosting platform separately restricts it; source-specific checkpoints trained on this evaluation corpus are not allowed. Source work or author groups should also be respected during local model selection. What Not To Use Do not use original source annotations, dataset-specific model checkpoints, external answer tables, or online searches to recover evaluation labels. Do not map public files to source answers through hashes, filenames, text search, image matching, row order, source identifiers or archive metadata. Do not use evaluation labels for model selection. Use only the provided training labels and the evidence in the public inputs. These rules constrain solution behaviour; they do not claim that searchable source material has been cryptographically anonymized. Limitations Publisher pixel boundaries and defect classes may be noisy. Most photographs show few native defect types, so typed output does not guarantee difficulty. Source images and masks remain an external-lookup risk. &nbsp;
> 3 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Schematic To Board Layout Retrieval

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74h2sjhk669d3h34bk7m9fyh8e6nfh
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 0.430!

Full challenge description from page:

> Schematic To Board Layout Retrieval Overview Every electronic design exists in two very different pictures. The schematic is the logical view: components drawn as standardized symbols (a resistor's zig-zag, a capacitor's parallel plates, an integrated-circuit block with named pins) wired together by nets, arranged for human readability with no relation to physical placement. The board layout is the physical view of the same design: copper traces, drilled pads, and the footprints of the very same components, placed and routed to fit a real printed circuit board. The two views share no visual vocabulary — one is line-art symbols, the other is copper geometry — yet they describe the identical circuit. An experienced engineer can look at a schematic and recognize which of several candidate board layouts implements it, by reasoning about the composition and structure both views must share: the same mix of component types, the same connector count, the same rough complexity and functional blocks. This competition asks a model to make that cross-view correspondence. Each query is a schematic image. Each query comes with a fixed candidate pool of 20 board-layout images; exactly one of them is the layout of the query's own design, and the other 19 are layouts of other designs chosen to be hard to rule out. The model must score the 20 candidates by how well each matches the query, ranking the true layout as high as possible. The candidate pool is built so that shallow cues do not separate the answer: negatives are drawn to share the query's coarse statistics — similar component count and similar board complexity — so a match on "how busy the picture is" does not identify the true layout, and the pool order carries no signal. The two views also look nothing alike pixel-to-pixel, and the correspondence between a logical schematic and its physical realization is not visually apparent. Designs range from single-sensor breakouts to dense multi-block boards, spanning many rendering styles. Dataset The data is a collection of query schematic images, candidate board-layout images, and, for each query, a fixed pool of 20 candidate layouts with the true match hidden among them. Images are referenced from the CSVs by their id token (not a path). Query schematics are in one shared folder; candidate board layouts are split into a train/ and a test/ universe, and a row's candidate images live under the same split as the row. Public files public/train.csv — one row per training query, with columns: id, the 20 candidate columns cand01…cand20, and the 20 relevance-target columns rel01…rel20. public/test.csv — one row per test query, with columns id and the 20 candidate columns cand01…cand20. The relevance targets are withheld. public/schematics/.png — the query schematic image for the row whose id matches the filename, at original resolution. public/train/layouts/.png and public/test/layouts/.png — the candidate board-layout images; the image for candidate token candNN of a train.csv row is under public/train/layouts/, and for a test.csv row under public/test/layouts/. A layout token may appear in more than one query's pool within its split. public/sample_submission.csv — a valid, correctly-formatted submission with constant placeholder scores. Private file (organizer only) private/answers.csv — the ground-truth relevance for the test queries: columns id plus rel01…rel20, where the column matching the true layout holds 1.0 and the other 19 hold 0.0. Not distributed to participants. Column descriptions The public and private CSVs use the following columns. id (string) — opaque unique identifier for one query, e.g. qry_9f3c2a71b0e4d5a6. It also names the query's schematic image file: public/schematics/.png. Used to align submissions with the answer key. cand01 … cand20 (string) — the 20 candidate layout id tokens for this query, e.g. lay_1a2b3c4d5e6f7a8b; the corresponding image is public//layouts/.png, where ` is train for a train.csv row and test for a test.csv` row. The pool order is fixed and carries no information about which candidate is correct. rel01 … rel20 (float) — the relevance of the candidate in the matching position. In a submission and in private/answers.csv, each value is a score in [0, 1] expressing how well that candidate matches the query; in train.csv the true layout's column holds 1.0 and the rest hold 0.0. relNN aligns with candNN. Data example A truncated train.csv row (only 3 of the 20 candidate and relevance columns shown): id,cand01,cand02,cand03,...,rel01,rel02,rel03,... qry_9f3c2a71b0e4d5a6,lay_1a2b3c4d5e6f7a8b,lay_77c0d9e1f2a3b4c5,lay_0e5d6c7b8a9f0102,...,0.0,1.0,0.0,... Split and anti-memorization Every schematic and every layout belongs to a source design project. The train/test split is made disjoint at the level of the design: a project's schematic and its layout are always assigned to the same side, so no design seen in training reappears at test time. To close the near-duplicate loophole, exact-duplicate images are removed beforehand and near-duplicate designs (forks and re-uploads of the same project) are removed down to a single representative — every near-duplicate but one is deleted from the dataset, so no design has a near-identical twin anywhere in either split. A test query's candidate pool is drawn only from test-side layouts, and every test layout is itself the true match for exactly one query, so the pool of distractors is composed of other genuine designs — a model cannot win by memorizing which layout goes with which schematic from training, nor by recognizing a near-duplicate of a training design, and must instead generalize to unseen designs. Candidate pools are built with a usage-balanced, complexity-matched sampler so that no layout dominates the distractor pools and candidate frequency carries no signal about relevance. Submission format Submit a CSV with a header row and exactly one row per test id — the same set of ids as public/test.csv, no more and no fewer. The required columns are, in order: id,rel01,rel02,rel03,rel04,rel05,rel06,rel07,rel08,rel09,rel10,rel11,rel12,rel13,rel14,rel15,rel16,rel17,rel18,rel19,rel20 id — a test query id. rel01 … rel20 — a relevance score in [0, 1] for each of the 20 candidates, where relNN scores the candidate given in the candNN column of test.csv for that query. Higher means more likely to be the true layout. Scores need not sum to 1, and ties are allowed. The submission must contain exactly these 21 columns; extra or missing columns are rejected. A sample submission (constant 0.5 for every candidate, truncated to 4 score columns): id,rel01,rel02,rel03,...,rel20 qry_9f3c2a71b0e4d5a6,0.5,0.5,0.5,...,0.5 qry_5b1e08c4a2d7f930,0.5,0.5,0.5,...,0.5 Evaluation The metric is Mean Reciprocal Rank (MRR) over the fixed 20-candidate pool. For each query the true layout occupies one candidate position; the model's scores induce a ranking of the 20 candidates, and the query earns the reciprocal of the rank at which the true layout appears. For a query whose true layout receives submitted score s*, with the 20 candidate scores s[1..20]: n_greater = count of candidates with s > s* # strictly ranked above the true layout n_ties = count of candidates with s == s* # tied with the true layout (includes it) Reciprocal rank credited as the EXPECTED reciprocal rank over the tied block, so an honest uniform score is not punished and information-free tie-breaking gives no gain: rr = mean( 1/r for r in (n_greater+1) .. (n_greater+n_ties) ) MRR = mean_over_queries( rr ) chance = (1/20) * (1/1 + 1/2 + ... + 1/20) corrected_MRR = max(0, (MRR - chance) / (1 - chance)) Higher is better. The leaderboard reports chance-corrected MRR. If the true layout is scored strictly highest it earns rank 1 (rr = 1.0), and a perfect submission scores 1.0. Chance baseline. A submission that carries no information about relevance — every candidate scored equally, or scored at random — earns, in expectation, raw MRR = (1/20) · (1/1 + 1/2 + … + 1/20) = 0.1798869828571841. The correction maps that chance baseline to 0; the shipped sample submission therefore receives the positive reporting floor described below. Tie handling. When several candidates share the true layout's score, the reciprocal rank is the mean of the reciprocals across the tied positions (the expected value under a random ordering of the tie). A constant submission and the same submission plus infinitesimal noise therefore score the same — adding meaningless noise to break ties confers no advantage. Floor. A small positive floor (0.02) is applied after chance correction, so that a valid submission is never reported as exactly 0.0. Fault scope. Each score must be a finite number in [0, 1]. A row-local fault — a missing, non-numeric, out-of-range, NaN or inf value in a score column — affects only that query: that query is scored as a maximally-incorrect ranking (rr = 0), while all other queries grade normally. Whole-file faults — a missing or extra column, a missing/unknown/duplicate/blank id, or an empty file — are rejected with an error. What Not To Use (Prohibited Methods) The pairing must be determined from the circuit's own visual structure. The following are prohibited: No external answer keys or design databases. Do not use any external parts list, netlist, project manifest, or design-repository index to determine which layout belongs to which schematic. No matching images back to any external repository. Do not match query or candidate images, ids, filenames, or perceptual hashes against any public design repository, code host, or CAD dataset to recover the correct pairing. No text-scraping shortcuts. Do not solve the pairing by reading and matching title-block text, project names, author names, dates, or silkscreen strings across the schematic and layout images; the task must be solved from the circuit's visual structure, not from incidental text. No id-based or positional hardcoding. Do not map ids to answers, exploit id ordering, or assume the true candidate sits in any particular pool position; ids are opaque and pool order is randomized and carries no label information. No train/test leakage or private-label tuning. Do not use the private answer key, and do not tune against the test relevances in any way. Model selection must use only the public training data. No manual pairing of the test set. Do not hand-match the test schematics to layouts (or crowdsource the matching) to construct the submission. &nbsp;
> 1 / 12 beat AI

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.

## Cross-Genotype Wheat-Plot Trait Ranking from Drone Imagery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx780s9xx3nkh97scbgbjqhkm18ec4fr
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 0.501!

Full challenge description from page:

> Cross-Genotype Wheat-Plot Trait Ranking from Drone Imagery Task type This is a multi-target ranking task. From a single overhead drone photograph of one wheat field plot, you order the plots along **three different agronomic traits at once**: how tall the canopy is, how much grain the plot yields, and how much protein that grain carries. For each trait you output a score per plot; only the relative order your scores impose is graded, so calibrating to real units is unnecessary -- ranking the plots correctly on all three axes is the whole task. The three traits are close to statistically independent on this data (each pair of traits has a rank correlation near zero). A model cannot do well on all three by reading one thing off the image: tall plots are not especially high-yielding, high-yielding plots are not especially high-protein. Three distinct visual signals have to be read from the same canopy. What makes it hard Three uncorrelated axes from one picture. Because the traits barely correlate, a feature that orders height well carries almost no information about protein. A strong solution needs three separate read-outs of the canopy, not one general "vigour" score. Unseen genotypes at test time. Every plot belongs to a wheat genotype (a breeding line). The scored plots come from genotypes that never appear in training. You cannot learn "line X yields well" and look it up; you must learn what tall, high-yielding, or high-protein canopies look like well enough to carry over to lines you have never seen. Subtle, entangled canopy cues. Height, grain yield, and grain protein leave overlapping traces in colour, texture, canopy density, and how the ground shows through. Senescence colour that hints at protein also shifts with yield; canopy closure that hints at yield also shifts with height. Disentangling the three is the core difficulty. Field nuisances. Plots are imaged over several site-years, so illumination, soil background, and growth stage vary between groups of plots. The ordering has to hold across those conditions. What you are given train_images/.png -- 256 by 256 RGB drone images, one per training plot. train_targets.csv -- columns id, height, yield, protein, one row per training plot: the three trait values you learn to order by. They have been rank-transformed to a common, smooth scale; their ordering is what matters. train_groups.csv -- columns id, genotype: which genotype each training plot belongs to. Use it to build a genotype-disjoint validation split that mirrors how you will be scored (hold out whole genotypes, never single plots). test_images/.png -- the plots to rank. test_queries.csv -- column id, the plots to score. sample_submission.csv -- a correctly shaped example (a constant prediction; it scores about zero). What you submit working/submission.csv with exactly the columns id, height, yield, protein and one row per test plot (each id appears exactly once): id -- the test plot id. height, yield, protein -- three real numbers whose job is only to order the plots on that trait. Larger means "ranked higher" on that trait. Any monotonic rescaling of a column gives an identical score; the units and offsets are irrelevant. How you are scored The metric is TraitScore, higher is better, bounded in 0 to 1: For each of the three traits, the sub-score is Kendall's tau between your predicted order and the true order of the scored plots, clipped to lie in 0 to 1 (a perfectly correct order scores 1; a random or reversed order scores about 0). TraitScore = the mean of the three sub-scores. All three traits count equally, so you cannot win by nailing one ranking and ignoring the others. A constant or random submission scores near 0; only orderings that genuinely track all three traits score high. One non-finite cell is simply ranked last for that trait and costs about one plot's worth of that trait's score, so a single bad value never voids the run. The split The split is cross-genotype: whole genotypes are assigned entirely to training or entirely to test, so every scored plot comes from a breeding line absent from the training set. A validation split you build for yourself should do the same -- hold out whole genotypes using train_groups.csv -- or your local score will look far better than the real one, because ranking plots of a genotype you have already seen is much easier than generalising to a new one. Allowed and prohibited Allowed -- any model you train on the provided plots, such as a convolutional network trained from scratch with one shared trunk and a head per trait; standard preprocessing and augmentation. Overhead plots have no canonical orientation, so 90-degree rotations and flips (the eight dihedral transforms) are label-safe. Prohibited -- external data or pretrained image weights; per-id answer tables or any hardcoded output; training on, fitting to, or otherwise adapting to the test plots (test-time training, tuning on test statistics, or hand-labelling them); recovering anything from the id or from the genotype rather than from the image. Ids are randomised and carry no signal, and genotypes are not provided for the test plots. (Running your trained model's forward pass on the test images to produce their scores is the task itself and is expected.) Compute GPU, one hour. The from-scratch reference network trains comfortably inside that budget. &nbsp;
> Closes in 4h 54m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses visual evidence for structured state, localization, or repair-style outputs beyond ordinary classification.


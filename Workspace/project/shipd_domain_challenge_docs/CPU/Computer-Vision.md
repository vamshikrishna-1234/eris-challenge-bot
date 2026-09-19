# CPU Computer Vision Challenge Examples

Scrape timestamp: 2026-07-19T00:00:00+05:30

Confirmed CPU examples in this document: 8

These entries are included because the challenge detail page displayed this domain and the challenge is part of the CPU-only challenge collection.

## Contrail Persistence Forecasting

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx772j591ttaee56rc993111gx8ap6wz
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Contrail Persistence Forecasting
> Overview
> Persistent contrails can contribute substantially more climate forcing than contrails that dissipate quickly. An operational camera system must decide early which newly detected tracks deserve continued monitoring, but the costly error is asymmetric: undercalling a long-lived contrail can remove it from lifecycle analysis, while a cautious overcall mainly spends additional tracking capacity.
> Predict the future persistence band of a newly observed contrail from its first three annotated appearances. Each example is a compact two-row sequence image made entirely from real GVCCS camera frames and human masks:
> Top row: the first three real contrail crops in chronological order.
> Bottom row: the corresponding human segmentation masks.
> Each source frame is 30 seconds after the preceding frame.
> The target measures the elapsed source-frame positions from the third observed appearance to the final annotated appearance:
> short: 0–4 future frame positions, at most 2 minutes after observation.
> sustained: 5–20 future frame positions, 2.5–10 minutes after observation.
> persistent: 21 or more future frame positions, more than 10 minutes after observation.
> The dataset contains 750 balanced training tracks and 360 balanced test tracks. Entire source videos are held out: 69 videos contribute training tracks, 17 different videos contribute test tracks, and no video occurs in both. This tests transfer across unseen sky conditions and recording periods rather than memorization of nearby frames.
> Dataset
> File descriptions
> train.csv: Training identifiers, sequence-image paths, anonymized video groups, and persistence labels.
> test.csv: Test identifiers, sequence-image paths, and unseen anonymized video groups.
> sample_submission.csv: Random valid predictions in the required format.
> train/: 384×256 JPEG sequence images for the training rows.
> test/: 384×256 JPEG sequence images for the test rows.
> Column descriptions
> id: Salted track identifier.
> sequence_image: Relative path to the six-panel sequence image.
> sequence_group: Salted source-video group. Use it to keep validation folds video-disjoint; it is not a stable predictive category because test groups are unseen.
> persistence_band: One of short, sustained, or persistent; present only in train.csv.
> Evaluation
> Submissions are scored with Macro Asymmetric Persistence Utility. Exact predictions receive 1.0. Operationally conservative overcalls receive limited partial credit; undercalls receive less because they can prematurely stop monitoring:
> True short, predicted sustained: 0.20.
> True short, predicted persistent: 0.05.
> True sustained, predicted persistent: 0.20.
> True sustained, predicted short: 0.05.
> True persistent, predicted sustained: 0.05.
> True persistent, predicted short: 0.00.
> Utility is averaged separately within each true persistence band, then the three band means are averaged. Every band therefore has equal weight despite deployment prevalence.
> UTILITY = {
> ("short", "sustained"): 0.20,
> ("short", "persistent"): 0.05,
> ("sustained", "persistent"): 0.20,
> ("sustained", "short"): 0.05,
> ("persistent", "sustained"): 0.05,
> ("persistent", "short"): 0.00,
> }
> def utility(target, prediction):
> return 1.0 if target == prediction else UTILITY[(target, prediction)]
> score = scored.groupby("target")["utility"].mean().mean()
> Higher is better. The score is bounded from 0 to 1.
> Submission
> Submit a CSV with exactly these columns:
> id: Every test identifier exactly once.
> persistence_band: One of short, sustained, or persistent.
> Example:
> id,persistence_band
> c_0018dff444a61,short
> c_01092c80f9cfe,persistent
> Requirements
> Include exactly 360 rows, one for each test track.
> Do not include missing values or duplicate identifiers.
> Preserve test identifiers exactly; row order is not important.
> Use only the three allowed persistence labels.
> Train and validate with CPU-compatible methods.
> Keep validation folds disjoint by sequence_group.
> What Not To Use
> Do not reverse-map the six-panel images to original source timestamps, frame filenames, video IDs, or contrail track IDs.
> Do not use external copies of the original contrail sequence archive to recover future frames, final track length, or hidden persistence labels.
> Do not use lookup tables built from the source annotation files. Predictions must be based on the released early observation sequence images.

Inspiration note: Useful because it makes a CPU-only vision benchmark from compact image-derived features/frames, with a physically meaningful persistence target and a bounded scoring setup.

## Mars Rover Route Safety Ledger from Real Terrain Images

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79h64tgzftxn7n68g5cb0mxx8amq85
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Plain language objective: infer which ground patches are safe, where the hazards are, and whether the proposed corridor should be driven.
> You receive a real Mars rover Navcam image, coarse real mission/camera context, and a normalized image-plane route corridor. Predict an operational traversability evidence ledger that shows terrain regions, locates major rock or unknown hazards, decides whether the queried corridor is safe, slow, avoid, or uncertain, and quantifies clearance, blockage, connected safe width, and annotation uncertainty.
> This is not plain terrain classification or a segmentation-only task. A valid answer contains a compact region map plus route-conditioned structured and numeric evidence. The mask uses the real source taxonomy 0=soil, 1=bedrock, 2=sand, 3=big_rock, and 255=unknown. There is no wheel-track, slope, GPS, depth, rover-pose, or synthetic route-outcome label.
> The route query is normalized to the image: (0,0) is the top-left and (1,1) is the bottom-right. route_query_json contains route_name, start_x, start_y, end_x, end_y, and half_width. The corridor is the set of pixels no farther than half_width from the supplied line segment.
> For every row, submit these seven outputs:
> terrain_mask_rle: a row-major 32 × 32 region map over the five allowed class values.
> hazard_boxes_json: up to eight normalized boxes around connected big_rock or substantial unknown regions.
> route_safety_class: one of safe_to_drive, drive_slowly, avoid_area, or uncertain.
> clearance_score: mean route passability in [0,1].
> obstacle_coverage: fraction of route pixels that are big_rock.
> safe_corridor_width: robust connected nonblocked width in [0,1].
> uncertainty_score: reliability penalty from real unknown-mask coverage in [0,1].
> The compact mask JSON has exactly this schema:
> {"shape":[32,32],"counts":[[255,120],[0,450],[1,300],[2,150],[3,4]]}
> counts is a list of [class_value,run_length] pairs whose positive lengths sum to 1024. Runs are row-major and class values must be in {0,1,2,3,255}.
> Each hazard box is an object with exactly kind,x,y,w,h. kind is big_rock or unknown; coordinates and sizes are normalized finite values in [0,1]; width and height are positive; and each box must remain inside the image. Example:
> [{"kind":"big_rock","x":0.44,"y":0.57,"w":0.12,"h":0.09}]
> The reference ledger is deterministic from the real mask. clearance_score is the corridor mean with weights soil 1.00, bedrock 0.95, sand 0.55, big rock 0.00, and unknown 0.25. obstacle_coverage is the big-rock fraction in the corridor. uncertainty_score = 0.75 * route_unknown_fraction + 0.25 * full_mask_unknown_fraction. safe_corridor_width samples 15 points along the route, measures the horizontal connected run of pixels that are neither big rock nor unknown around each point, normalizes by image width, and takes the 20th percentile.
> The route class is uncertain when uncertainty is at least 0.32; otherwise it is avoid_area when obstacle coverage is at least 0.14, clearance is below 0.44, or safe width is below 0.08; otherwise it is drive_slowly when obstacle coverage is at least 0.035, sand coverage is at least 0.32, clearance is below 0.76, or safe width is below 0.18; remaining rows are safe_to_drive.
> hazard_boxes_json contains 4-connected component boxes from the 32 × 32 map: big-rock components require at least two cells and unknown components require at least 20 cells. The eight largest qualifying components are retained.
> Only CPU solutions are allowed. The maximum solution time is 1.5 hours on 10 CPU cores and 62 GB RAM. Credible approaches include 384-pixel image features, classical texture/superpixel models, random forests, compact CPU segmentation networks, shallow encoder-decoders, and train-time feature extraction. GPU foundation-model fine-tuning is neither required nor allowed.
> What Not To Use / What Not To Do (violation may cause rejection regardless of score):
> Do not use an original AI4MARS filename, image-id, product-id, or source-annotation lookup for hidden rows.
> Do not download or index the upstream masks to recover private answers, including perceptual image retrieval against the named source.
> Do not submit a metadata-only solution that ignores image pixels.
> Do not decode salted IDs, row order, file order, mtimes, JPEG sizes, or path strings as answer channels.
> Do not use a rule-only template that predicts one fixed mask/ledger without learning from images.
> Do not reduce the task to one scene-level terrain class or only route_safety_class; all spatial and numeric heads are required.
> Do not use external hosted image, segmentation, vision-language, or inference APIs.
> Do not use closed-source teacher APIs for labels, distillation, or pseudo-labelling.
> Do not inspect private/answers.csv, grader internals, filesystem side channels, or hidden platform state.
> Do not use malformed JSON floods, non-finite numbers, extra columns, duplicate IDs, or other format/grader exploits.
> Enforcement on invalid approaches: solutions may be reviewed for actual image use, source-lookup code, external calls, and rule-only behaviour. Metadata-only models, source retrieval, hosted APIs, hidden-answer access, or submissions that avoid the required spatial evidence contract may be rejected before payout.
> Task
> For each test row, read the rover image and the route corridor, then output a route-conditioned terrain evidence ledger. The central object is the 32 × 32 terrain map: the hazard boxes, route class, and numeric route measures should be consistent with the terrain you predict, not independent guesses. A strong submission should identify sand/soil/bedrock texture, isolate rock or unknown components, and reason about whether the specific corridor has enough clear connected ground for a rover to traverse.
> The test rows are not a lookup exercise. Related rover/source image families are kept together, and the public IDs and file paths are opaque, so useful models need to generalize from the labelled training images to unseen rover terrain appearances and route placements.
> Intended Approach and Validation
> A practical CPU solution is to train a compact image-to-mask model on train.csv: decode the training terrain_mask_rle labels, resize or featurize each image, and learn a 32 × 32 terrain predictor using a lightweight U-Net, shallow encoder-decoder, random forest over patch features, superpixel classifier, or k-nearest/gradient-boosted texture model. After predicting the terrain map, derive hazard boxes and route metrics from that predicted map using the public geometry definitions, optionally with small calibration models for the route class and numeric heads.
> Another reasonable route is a two-stage CPU pipeline: first produce per-cell terrain probabilities from local intensity, texture, gradient, and neighborhood features; then apply connected-component cleanup and route-corridor postprocessing to produce hazard_boxes_json, clearance_score, obstacle_coverage, safe_corridor_width, uncertainty_score, and route_safety_class. This is still a visual modeling task: the route text tells you where to evaluate the image, but it does not contain the answer.
> Use only the released training labels for model selection. Make your own validation folds from train.csv—for example stratified by mission, route family, and visual texture clusters—and check both mask quality and the downstream ledger heads. Calibrate numeric outputs on training-only validation folds so they stay in [0,1] and remain consistent with the predicted mask. Open-source local CV libraries, classical features, and generic offline pretrained vision features are allowed if they run under the CPU limit and do not use AI4MARS source annotations or hidden test information.
> Evaluation
> Each row receives seven head scores. Higher is better.
> S_mask   = mean IoU over present classes 0,1,2,3,255
> S_boxes  = class-aware greedy IoU-F1 for boxes with IoU >= 0.30
> S_route  = 1 for exact route class, else 0
> S_clear  = exp(-abs(error) / 0.14)
> S_block  = exp(-abs(error) / 0.07)
> S_width  = exp(-abs(error) / 0.14)
> S_uncert = exp(-abs(error) / 0.14)
> independent = 0.34*S_mask + 0.14*S_boxes + 0.15*S_route
> + 0.10*S_clear + 0.10*S_block + 0.09*S_width
> + 0.08*S_uncert
> joint = sqrt(S_mask * (0.45*S_route
> + 0.55*min(S_clear,S_block,S_width,S_uncert)))
> row_score = independent * (0.70 + 0.30*joint)
> The final score combines mean performance with the weakest real private subgroup along mission, terrain condition, and route family:
> Final = 0.76 * mean(row_score)
> + 0.10 * worst_mission(row_score)
> + 0.08 * worst_terrain(row_score)
> + 0.06 * worst_route(row_score)
> The worst-group terms are the lowest minimum mean row score over the private mission, terrain-family, and route-family buckets.
> The minimum is 0.0 and the maximum is 1.0. A perfect submission scores exactly 1.0.
> The grader requires exactly the listed columns in the listed order, one row per test ID, unique IDs, and the exact test ID set. A structural failure, any non-finite numeric field, or any numeric value outside [0,1] raises InvalidSubmissionError. Malformed or over-long row-local mask/box JSON, or an invalid route class string, scores zero for that row and does not crash the grader.
> Dataset
> The public corpus contains prepared 384 × 384 grayscale JPEGs with opaque salted IDs. mission is Curiosity, Spirit, or Opportunity; camera is Navcam. Related rover/time/product sequence families stay in one split. Original source filenames and product IDs are absent.
> File overview
> Item	Description
> train/images/*.jpg	Training images
> test/images/*.jpg	Test images
> train.csv	Inputs and labels
> test.csv	Test inputs
> sample_submission.csv	Weak constant template
> train.csv columns
> train.csv contains the eight public input columns and all seven target columns.
> Column	Type	Description
> id	string	Opaque row id
> image	string	JPEG path
> mission	string	Rover mission
> camera	string	Camera family
> image_width	int	Prepared width
> image_height	int	Prepared height
> route_query_json	string	Corridor query
> prompt	string	Task contract
> terrain_mask_rle	string	32x32 mask RLE
> hazard_boxes_json	string	Hazard boxes
> route_safety_class	string	Route decision
> clearance_score	float	Route passability
> obstacle_coverage	float	Rock fraction
> safe_corridor_width	float	Safe width
> uncertainty_score	float	Unknown fraction
> The input fields are id (opaque row key), image (public-relative JPEG path), mission (Curiosity, Spirit, or Opportunity), camera (Navcam), image_width and image_height (prepared pixel dimensions), route_query_json (normalized corridor object), and prompt (the shared task instruction). The train-only labels are terrain_mask_rle (32 × 32 terrain RLE), hazard_boxes_json (component boxes), route_safety_class (four-way route decision), clearance_score (weighted route passability), obstacle_coverage (route big-rock fraction), safe_corridor_width (robust connected safe width), and uncertainty_score (unknown-area measure).
> test.csv columns
> test.csv contains exactly the same eight input columns as training data and none of the target columns.
> Column	Type	Description
> id	string	Opaque row id
> image	string	JPEG path
> mission	string	Rover mission
> camera	string	Camera family
> image_width	int	Prepared width
> image_height	int	Prepared height
> route_query_json	string	Corridor query
> prompt	string	Task contract
> In test.csv, id is the opaque row key; image is the public-relative JPEG path; mission is Curiosity, Spirit, or Opportunity; camera is Navcam; image_width and image_height are the prepared pixel dimensions; route_query_json is the normalized corridor object; and prompt is the shared task instruction. No target column is present in test data. sample_submission.csv is the submission template and contains one weak constant placeholder row for every test ID.
> Submission
> Write the final submission CSV to exactly ./working/submission.csv. It must contain exactly these eight columns in this order and exactly one row for every test ID.
> Column	Type	Constraint
> id	string	Same set as test
> terrain_mask_rle	string	Valid 32x32 RLE
> hazard_boxes_json	string	Up to 8 boxes
> route_safety_class	string	Four allowed values
> clearance_score	float	In [0,1]
> obstacle_coverage	float	In [0,1]
> safe_corridor_width	float	In [0,1]
> uncertainty_score	float	In [0,1]
> Example formatting:
> id,terrain_mask_rle,hazard_boxes_json,route_safety_class,clearance_score,obstacle_coverage,safe_corridor_width,uncertainty_score
> rvr_0123456789abcd,"{""shape"":[32,32],""counts"":[[0,1024]]}",[],safe_to_drive,0.91,0.00,0.44,0.05
> rvr_fedcba98765432,"{""shape"":[32,32],""counts"":[[255,80],[2,900],[3,44]]}","[{""kind"":""big_rock"",""x"":0.4,""y"":0.6,""w"":0.1,""h"":0.1}]",drive_slowly,0.61,0.04,0.22,0.09
> Requirements are strict: the submitted IDs must exactly match the test IDs, the column order must match the table above, duplicate or missing IDs are invalid, numeric values must be finite and in [0,1], and malformed row-local mask, box, or route content receives zero for that row.

Inspiration note: Useful because it turns CPU computer vision into route-safety reasoning from real terrain images, producing a structured safety ledger rather than a plain class label.

## Identity Matching Under Appearance Drift

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cxzegz7zt6579catqg9gpbd8a6cdf
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> A corkwing wrasse is trapped on a Norwegian reef, photographed, tagged and released. Years later it swims into a trap again. It has grown, lost scales, picked up parasites and changed colour with the spawning season. Is it the same fish?
> Most benchmarks that pose that question are quietly solvable without answering it, because the true match differs from its distractors in ways that have nothing to do with identity: it is a little larger, or its photograph is a little older, or it simply recurs across the dataset in a way the distractors do not. A model that learns those regularities scores well and has recognised nothing.
> This challenge is built the other way round. Each query is offered forty candidates that have been matched to the true match on every measurable confounder except identity: same flank, same capture year, body length within 5 millimetres, and each candidate photograph used in exactly one candidate list across the whole test set, so no image can be identified by how often it recurs. Beyond that, the forty candidates are the ones that most look like the true match, chosen by an appearance descriptor, so the true match does not stand out on coarse shape, shading or colour. The distractors are drawn from a different population than the true matches, and a detector trained to tell those populations apart from the image alone scores at chance (AUC 0.497). Every photograph is centre-cropped to a square, so scale and aspect ratio say nothing. What is left is the animal's head pattern.
> On top of that, the answer must survive appearance drift. Query and true match are separated by at least a year (median 671 days, up to six), so the model cannot lean on a near-duplicate frame; it has to learn which parts of a pattern persist through a year of growth and injury and which do not.
> Identities are scarce, too. Of the 1,509 individuals in the training photographs, only 250 come with an identity label. The remaining 5,564 photographs are released with no identity at all. Enough labelled identities to fine-tune your way to the answer is exactly what you do not get, and the unlabelled pool is where the remaining signal has to come from.
> Two further properties close the last escapes. No fish in the test set ever appears in training, so identities cannot be memorised: a solver learns what makes two photographs the same animal, not who the animals are. And unlike faces, cattle muzzles or whale flukes, no pretrained model and no public tool exists for this species, so identity cannot be looked up or transferred. Ground truth is not a human judgement either: every fish carries a PIT tag that was read at each capture, so the correct answer is a physical fact.
> You are given a query photograph and its forty candidates, exactly one of which is the same individual at an earlier capture. You rank the candidates, best first, and you are scored by how high you place the true match.
> Task
> For each query_id in queries.csv, rank that query's forty candidate_ids from candidates.csv, most likely match first.
> Why the easy answers do not work
> The candidate lists are built so that nothing except the animal's head pattern separates the true match from the thirty-nine distractors. Each of the following was measured on this exact split, where ranking at random scores 0.107:
> Body size. All forty candidates lie within 5 mm of the true match in body length, and the query itself has grown since. A ranking rule based purely on size scores 0.124, against 0.109 for a random ranking.
> Photograph age. All forty candidates were photographed in the same year as the true match. Since the true match is always the older photograph, a solver that learned to spot "an older looking picture" from camera, lighting or background would win. It cannot, because every candidate is equally old.
> Coarse appearance. The distractors are the closest look-alikes of the true match among all fish that satisfy the constraints above, measured by oriented edge energy. Shape, shading and colour therefore cannot separate them.
> How often an image appears. Every candidate photograph is used in exactly one candidate list across the entire test set. If distractors were recycled, simply counting occurrences would reveal the true match without looking at a single pixel.
> Distractor provenance. Distractors are fish that were only ever caught once, true matches are fish that were recaptured. A detector trained to tell those two groups apart from the image alone reaches AUC 0.497 on held-out true matches, which is chance: the true match does not look like a true match.
> Absolute scale and aspect ratio. Every photograph is centre-cropped to a square and resized to 224x224, so a fish cannot be recognised by the shape or size of its crop.
> Off-the-shelf models. No pretrained corkwing wrasse recogniser exists, and identity cannot be recovered from a photograph by any tool or lookup. Frozen self-supervised features straight off the shelf reach 0.267, so generic features help but do not solve it.
> What is left is the head pattern: the arrangement of spots, stripes, scars and the shape of the operculum. Reading it, and learning which parts of it survive a year of growth, is the challenge.
> Data
> All inputs are under dataset/public/:
> train/<image_id>.jpg: 6,676 training photographs of fish caught at least twice.
> train_identities.csv: identity labels for 250 of those individuals only (1,112 photographs). Columns image_id, individual_id, side. Two rows share individual_id if and only if they show the same fish. side is the flank photographed, left or right. The other 5,564 photographs in train/ appear in no row of this file: they are an unlabelled pool, and you may use them however you like.
> test/<image_id>.jpg: the query and candidate photographs.
> queries.csv: column query_id, one row per query. The image is test/<query_id>.jpg.
> candidates.csv: columns query_id, candidate_id, forty rows per query. Exactly one candidate per query is the same fish as the query, photographed at least a year earlier. A candidate always shows the same flank as its query.
> sample_submission.csv: a correctly formatted example for every query, ranking the candidates in the order they were given.
> The true matches are held out privately and used only for scoring.
> Evaluation
> Submissions are scored by Mean Reciprocal Rank: for each query, the reciprocal of the position at which the true match appears in your ranking.
> for each query q:  RR_q = 1 / rank of the true match in your ranking   (0 if you omit it)
> score = mean(RR_q)                                    (higher is better, range 0 to 1)
> Ranking the candidates at random scores about 0.107. Putting the true match first every time scores 1. Frozen off-the-shelf features score 0.267, and a metric-learning head trained on the 250 labelled identities reaches 0.291 in local checks. Neither touches the unlabelled pool, and that is where the headroom is.
> Submission format
> Write ./working/submission.csv with exactly these columns:
> query_id,ranking
> m_1a2b3c4d5e6f7a,m_9f8e7d6c5b4a39 m_2b3c4d5e6f7a8b m_44c1a0e9b7d213 ...
> One row per query_id in queries.csv (the id set must match exactly).
> ranking is a single space-separated string of candidate_ids for that query, best first.
> Every id must be one of that query's forty candidates, with no repeats. You may submit fewer than forty (a query whose ranking omits the true match scores 0 for that query). Start from sample_submission.csv to guarantee the correct format, and write with index=False.
> Constraints
> Read the challenge inputs only from ./dataset/public/. Write your output only to ./working/submission.csv.
> No package installs (no pip or conda install). You may use the preinstalled libraries (numpy, pandas, scikit-learn, pillow, pytorch, torchvision, transformers, and so on) and pretrained backbones from the standard model hubs.
> Must finish within the grading time budget on the provided hardware.
> What Not To Use
> Do not retrieve this challenge's source photographs or their tag numbers from the public internet to recover the true matches. Decide only from the provided images.
> Do not hardcode outputs or otherwise bypass learning from the data.
> A learning-based approach is expected: turn a pretrained vision backbone into an identity embedding with a metric-learning objective (ArcFace, triplet or contrastive) on the 250 labelled identities, and lean on the unlabelled photographs through self-supervision, pseudo-labelling or augmentation-based consistency to make up for how few identities are named. Then rank each query's candidates by embedding similarity. Local ablations show the gains come from what the embedding learns about head patterns, not from any property of how the candidate lists were assembled.

Inspiration note: Useful because it frames CPU computer vision as robust identity matching under appearance drift, a realistic retrieval/re-identification pattern with ranking-style outputs.

## Cross-Inspector Assembly Signatures

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ffd0k07dbmvt0xpsemkjhdd8atxy5
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ? Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> Cross-Inspector Assembly Signatures
> Overview
> Industrial optical inspection rarely depends on one observer. A trained operator, a conventional rule system, and a learned inspection tool can react differently to the same assembly image. Predicting only a visible component class hides those operational disagreements.
> Your task is to predict the inspection signature produced by the three channels from a privacy-preserving image view. Each target describes which channels raised an alert. The holdout uses disjoint acquisition blocks, so nearby production images do not appear on both sides of the split.
> The four signatures are:
> CLEAR_CONSENSUS ? all three channels were clear.
> TOOL_ONLY_ALERT ? only the learned toolchain raised an alert.
> EOLT_ONLY_ALERT ? only the conventional end-of-line system raised an alert.
> HUMAN_CONFIRMED_ALERT ? the human and learned toolchain raised an alert; the conventional system may be clear or alert.
> Dataset
> File descriptions
> train.csv ? Labeled observations with image paths, acquisition-group identifiers, and inspection_signature.
> test.csv ? Held-out observations with image paths but no target or acquisition-group identifier.
> train/ ? Privacy-preserving PNG views for labeled observations.
> test/ ? Privacy-preserving PNG views for held-out observations.
> sample_submission.csv ? A valid template containing random signature labels.
> data_summary.json ? Split sizes, training class counts, and image dimensions.
> Column descriptions
> id (string) ? Unique 16-character hexadecimal observation identifier.
> image_path (string) ? Relative path to the corresponding PNG image.
> group_id (string) ? Hashed contiguous acquisition block used for grouped validation; present in train.csv only.
> inspection_signature (string) ? One of the four signatures above; present in train.csv only.
> Evaluation
> Submissions are scored with the Inspection Coverage Score. Macro-F1 rewards balanced signature prediction, balanced accuracy measures average per-signature sensitivity, and minimum class recall penalizes a model that completely ignores one operational disagreement mode.
> from sklearn.metrics import balanced_accuracy_score, f1_score, recall_score
> LABELS = [
> "CLEAR_CONSENSUS",
> "TOOL_ONLY_ALERT",
> "EOLT_ONLY_ALERT",
> "HUMAN_CONFIRMED_ALERT",
> ]
> def inspection_coverage_score(y_true, y_pred):
> macro_f1 = f1_score(y_true, y_pred, labels=LABELS, average="macro", zero_division=0)
> balanced = balanced_accuracy_score(y_true, y_pred)
> recalls = recall_score(y_true, y_pred, labels=LABELS, average=None, zero_division=0)
> return 0.50  *macro_f1 + 0.30*  balanced + 0.20 * min(recalls)
> Higher is better. The score is bounded from 0 to 1.
> Submission
> Submit a CSV containing one prediction for every row in test.csv.
> id (string) ? Exact identifier from test.csv.
> inspection_signature (string) ? One allowed signature label.
> Example:
> id,inspection_signature
> 008e089a4b8324a9,TOOL_ONLY_ALERT
> 01f44e8027134ff5,CLEAR_CONSENSUS
> Requirements
> The file must contain exactly the same number of rows and IDs as test.csv.
> Each ID must occur exactly once.
> Columns must be exactly id,inspection_signature in that order.
> Every prediction must be one of the four documented labels.
> Missing values, duplicate IDs, unknown IDs, extra columns, and unknown labels are invalid.
> What Not To Use
> Do not reverse-search released images or use external copies of matching inspection imagery to recover label assignments; that bypasses the intended visual generalization task.
> Do not reconstruct a mapping from public observation IDs or image bytes to outside filenames or row order; identifiers and views are deliberately transformed to prevent lookup solutions.
> Do not use cached label tables, copied answer maps, or hand-authored per-image rules. Predictions must come from a trained model using the supplied public data.

Inspiration note: Useful because it turns a CPU-only vision task into multi-observer disagreement prediction, with a compact four-label operational signature and group-aware generalization.

## Horizon Line Detection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f5589tbgxmmwh6h4jd4307h8ahbez
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: image, feature-engineering
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> Dataset source is visible after the challenge closes.
> Description
> Leaderboard
> (1)
> Your Submissions
> Background
> When a photo is taken, the camera has some orientation with respect to gravity: it may be rolled (tilted left/right, so the true horizon is not level in the frame) and pitched (aimed up or down, so the horizon sits high, low, or entirely outside the frame). The horizon is the image of the true, gravity-level horizon — the line at infinity of the ground plane. Recovering where it lies is a core step in single-image camera calibration, image rectification, and augmented reality.
> You are given a large collection of small 128×128 real-world photographs, each a perspective view of a diverse outdoor or indoor scene, captured with an unknown camera roll and pitch. Your job is to locate the horizon across the width of each image — a structured, per-region classification.
> Two properties make this hard on purpose:
> Low resolution (128 px). The long, crisp straight lines that make horizon geometry easy are largely gone, and the resolution caps how large a model can usefully be.
> The horizon is frequently off-frame or invisible. Roll and pitch both vary widely, so for many images the horizon lies partly or fully outside the crop, or is occluded (e.g. indoors), and must be inferred from perspective.
> What you predict
> The image width is divided into 16 equal vertical column strips (strip 0 is the leftmost 8 pixels, strip 15 the rightmost). The vertical extent — extended above and below the frame to cover off-frame horizons — spans normalized heights from −0.5 to +1.5 image-heights (0.0 = top edge of the image, 1.0 = bottom edge) and is split into 40 equal horizontal bands, indexed 0 (top) to 39 (bottom). Each band is 1/20 of an image height (≈6 px) tall.
> For each of the 16 strips, you predict the single band through which the horizon passes at that strip. So each image has 16 integer labels b0, b1, …, b15, each in {0, …, 39}:
> A level, centered horizon → all strips near the middle band (≈ band 19–20).
> A rolled camera → the band index changes smoothly from left strips to right strips (a tilted horizon).
> A camera pitched up → the horizon is low in the frame → higher band indices; pitched down → lower band indices.
> If the horizon is above the frame at a strip, that strip's label is band 0; if below the frame, band 39.
> Files
> All files are in the challenge working directory.
> train.csv — the training table, one row per training image. Columns:
> id (string): image identifier; the image is train/<id>.png.
> b0 (integer): band index (0–39) of the horizon in strip 0.
> b1 (integer): band index in strip 1.
> … (one column per strip) …
> b15 (integer): band index in strip 15.
> scene_group (integer): an anonymized scene identifier. All training images sharing a scene_group come from the same underlying scene. Use it to build a scene-grouped validation split (keep whole groups together); the test set is entirely different, unseen scenes, so a random per-image split overstates accuracy. This column is for training only and is not part of the submission.
> test.csv — the test table, one row per test image. Columns:
> id (string): image identifier; the image is test/<id>.png. No labels.
> sample_submission.csv — a correctly formatted example submission. Columns:
> id (string): a test image id.
> b0 … b15 (integer): predicted band index (0–39) for each of the 16 strips.
> train/ — folder of training images, one <id>.png per training id; each a 128×128 RGB PNG.
> test/ — folder of test images, one <id>.png per test id; each a 128×128 RGB PNG.
> Every image is 128×128, 3-channel (RGB), 8-bit PNG.
> Evaluation metric
> Per-strip triangular partial credit: each (image, strip) earns full credit for the exact band and linearly decaying partial credit for near bands, reaching 0 at TOL = 2 bands away. So a band that is exactly right scores 1.0, one band off scores 0.5, and two or more bands off scores 0. The final score is the mean of this over all (image, strip) pairs:
> score = mean over test images, over strips c in 0..15 of  max(0, 1 - |b{c}_pred - b{c}_true| / 2)
> The final score lies in [0, 1] and is maximized (higher is better). The metric rewards geometric proximity — getting each strip's band close matters, so a model that localizes the horizon precisely beats one that is merely in the right neighborhood; a one-band miss is not penalized as harshly as a wild one.
> Submission format
> Produce a CSV named submission.csv with exactly these 17 columns and one row per test image:
> id,b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15
> id: every id in test.csv, each exactly once (no missing, extra, or duplicate ids).
> b0…b15: integer band indices in {0, …, 39}.
> Any non-integer or out-of-range band value, a wrong id set, or duplicate ids makes the submission invalid.
> Constraints
> CPU-ONLY. Solutions must train and run inference using the CPU only. No GPU may be used for any part of training or inference. Design a model and a training budget that fit on CPU within the session time limit, and measure your inference throughput so you produce predictions for every test image, not just train a good model.
> Any modeling approach that learns the mapping from image pixels to band labels is acceptable.
> Notes
> The train/test split holds out entire scenes (no scene appears in both); validate with the scene_group column so your local scores are honest.
> Camera roll and pitch are sampled over a wide range, so both the tilt (how the band index changes across strips) and the overall vertical position vary substantially and independently.
> If you augment with a horizontal flip, remember it mirrors the strips: the band label sequence must be reversed (b0…b15 → b15…b0). Avoid rotations or arbitrary crops that change the horizon without relabeling.
> A large fraction of images have the horizon off-frame or occluded (labels pinned to band 0 or 39 across strips); these are the hardest and are retained deliberately — inferring an invisible horizon is a core part of the task.

Inspiration note: Useful because it turns camera-geometry reasoning into a compact per-strip structured output, which is a nice CPU-friendly design trick for vision tasks that need more shape than a single class label.

## Traffic Sign Pair Proposal Route Screening

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c2b47e53h2pmstcn2zas1r58aqje4
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ? Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> Dataset source is visible after the challenge closes.
> Description
> Leaderboard
> (4)
> Your Submissions
> Traffic Sign Proposal Coupling
> Overview
> Compact edge-perception systems often transmit contour telemetry instead of full photographs. A downstream detector must decide whether the closest visible sign pair should share one proposal, receive separation review, or be processed independently. For coupled pairs, vertical alignment also matters: aligned signs can share a proposal column, while laterally offset signs need a different proposal path.
> Predict the proposal route from each 192 by 192 three-channel derivative preview. Every preview comes from one real traffic-sign photograph. Its channels encode gradient magnitude, horizontal derivative magnitude, and vertical derivative magnitude. Cropping, projective transformation, rotation, quantization, and removal of photographic texture preserve sign contours and spatial layout while limiting source reconstruction. No synthetic scenes, generated objects, or composited examples are used.
> Every released example contains at least two sufficiently visible reviewed signs. For each sign pair, compute center distance divided by the mean box diagonal. The pair with the smallest ratio is the critical pair. Its route is:
> JOINT_ALIGNED: ratio at most 0.49, with horizontal displacement at most 11% of total horizontal-plus-vertical displacement.
> JOINT_OFFSET: ratio at most 0.49, with greater horizontal displacement.
> SEPARATION_ALIGNED: ratio above 0.49 and at most 0.62, with horizontal displacement at most 11% of total displacement.
> SEPARATION_OFFSET: ratio above 0.49 and at most 0.62, with greater horizontal displacement.
> INDEPENDENT_PROPOSALS: ratio above 0.62.
> The holdout is grouped by underlying capture frame, so related crops never cross the training/test boundary.
> Dataset
> File descriptions
> train.csv: 1,052 labeled derivative previews from training capture groups.
> test.csv: 342 unlabeled derivative previews from held-out capture groups.
> train/: Prepared JPEG previews referenced by train.csv.
> test/: Prepared JPEG previews referenced by test.csv.
> sample_submission.csv: Valid randomly populated submission template.
> Column descriptions
> id (string): Hashed example identifier.
> image_path (string path): Relative path from dataset/public to the preview JPEG.
> screening_route (string categorical): One of the five proposal routes; present only in train.csv.
> Evaluation
> The Proposal Coupling Score rewards balanced classification and prevents a model from abandoning its hardest route:
> score = (
> 0.60 * macro_f1
> + 0.25 * balanced_accuracy
> + 0.15 * min(recall_for_each_route)
> )
> Macro-F1 and balanced accuracy give every route equal influence despite unequal support. Worst-route recall penalizes systems that ignore difficult coupling or alignment cases. Scores range from 0 to 1, and higher is better.
> Submission
> Submit a CSV with:
> id (string): Every test identifier exactly once.
> screening_route (string categorical): One legal route label.
> Example:
> id,screening_route
> sign_4e8656fcb63df39f,JOINT_ALIGNED
> sign_1b8468ea9451ecc9,SEPARATION_OFFSET
> sign_2187d6bdaca9a68f,INDEPENDENT_PROPOSALS
> Requirements
> Include exactly id and screening_route in that order.
> Include every test ID exactly once with no missing values.
> Use only JOINT_ALIGNED, JOINT_OFFSET, SEPARATION_ALIGNED, SEPARATION_OFFSET, and INDEPENDENT_PROPOSALS.
> Run offline on CPU and write ./working/submission.csv.
> Allowed Methods
> Train normal image classifiers, compact convolutional models, localization-aware models, or ensembles using supplied public files.
> Engineer contour, region, projection, gradient, and pair-relation features from the supplied previews.
> What Not To Use
> Do not reverse-match previews to outside photographs, filenames, annotations, manifests, or lookup tables to recover held-out routes.
> Do not build predictions from hashed-ID order or cached route mappings.
> Do not use only global or coarse cell aggregates while presenting the method as spatial proposal reasoning.

Inspiration note: Useful because it turns compact contour-derived vision inputs into structured pair-routing classification, with a nice geometric coupling threshold design instead of plain object recognition.

## Honeycomb Coverage Revisit Planner

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74nxde5gwyatr1bqgz1wtjqs8akckt
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: text, image
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Given four overlapping robotic inspection photographs, estimate how much physical comb area the views share, determine which degraded views leave unsupported coverage, and compile the shortest route for reacquiring every uncovered region.
> An inspection mosaic can fail even when its individual images remain recognizable. A blurred or obscured view may be harmless if neighboring photographs cover the same cells, while a smaller defect can be critical when it affects a unique boundary region. A useful recovery system must therefore combine visual overlap, evidence quality, and route planning. This benchmark evaluates that closed-loop decision rather than asking for another image-registration correction.
> Each packet contains four photographs labeled A, B, C, and D. The views were captured at neighboring robot positions over a real honeycomb surface. One or two panels have controlled acquisition degradation. Predict a fine overlap-fraction matrix, a four-panel coverage-debt vector, and the canonical shortest revisit program beginning at panel A.
> Complete acquisition sessions and scan configurations are isolated between train and test. Source scan names, timestamps, image indices, camera coordinates, motor positions, and registration tables are not public. Prepared images use fixed-dimension uncompressed indexed-color BMP encoding, so compressed file length cannot reveal degradation strength. The task is designed for CPU execution within 1.5 hours on 10 CPU cores.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `public/train.csv` | 900 labeled four-view planning packets. |
> | `public/test.csv` | 540 packets from a held acquisition session. Targets are withheld. |
> | `public/sample_submission.csv` | Valid placeholder output in the required schema. |
> | `public/images/` | 1,440 indexed-color BMP packets, each 790 by 830 pixels. |
> Train and test share no acquisition session, scan configuration, four-view source loop, case ID, filename, or prepared image hash.
> Image Layout
> The packet uses a two-by-two grid:
> | Position | Panel |
> |---|---|
> | upper left | A |
> | upper right | B |
> | lower left | C |
> | lower right | D |
> Panels show honeycomb cells, bees, cell contents, boundaries, glare, and local surface texture. Crop gauge, brightness, contrast, and color response vary independently. Letter markers identify panel roles only.
> Three reliability profiles are used:
> | Profile | Reliability values assigned to visibly degraded panels |
> |---|---|
> | localized loss | one panel at `0.62` |
> | distributed loss | two panels at `0.48` and `0.58` |
> | severe plus moderate loss | two panels at `0.18` and `0.52` |
> All other panels have reliability 1.0. Panel assignments are independently shuffled. Degradation is rendered as a combination of local blur and a nonrectangular veil or obstruction.
> Every training source loop appears with all three profiles. Each hidden source loop appears exactly once, so hidden packets cannot be grouped into alternate degradations of the same four source views. The hidden profile counts are 170 localized-loss, 190 distributed-loss, and 180 severe-plus-moderate packets.
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque 24-character identifier unrelated to source loop, geometry, or target. |
> | `image_path` | string | Relative path to the four-panel BMP. |
> | `planning_request` | string | Fixed instruction to recover overlap, coverage debt, and a revisit route. It contains no case-specific answer. |
> Target Columns
> | Column | Data type | Description |
> |---|---|---|
> | `overlap_bucket_matrix` | JSON 4 by 4 integer matrix | Fine pairwise overlap fraction for panels A-D. |
> | `coverage_debt_vector` | JSON length-4 integer vector | Unsupported evidence debt for panels A-D. |
> | `revisit_program` | ordered token sequence | Canonical shortest route from A that reacquires every panel with nonzero debt. |
> Overlap Bucket Matrix
> Rows and columns are A, B, C, D. For two different panels, let f be their geometric intersection area divided by one panel's viewport area.
> overlap_value = round(20 * f)
> Values range from 0 through 20. The matrix is symmetric and its diagonal is always 20. A value of 0 means less than half of one twentieth of a viewport overlaps after rounding. A value of 20 would mean complete footprint overlap.
> [[20,7,1,6],[7,20,6,1],[1,6,20,7],[6,1,7,20]]
> Coverage Debt Vector
> Coverage debt combines view reliability with whether another reliable panel covers the same region. A 36 by 36 lattice is evaluated inside each panel footprint. A lattice point is supported when it lies inside another panel whose reliability is at least 0.75.
> unsupported_fraction = unsupported_lattice_points / 1296
> debt_measure = unsupported_fraction * (1 - panel_reliability)
> debt_measure is converted to an integer:
> | Vector value | Debt measure |
> |---:|---|
> | `0` | less than 0.03 |
> | `1` | 0.03 to less than 0.18 |
> | `2` | 0.18 to less than 0.35 |
> | `3` | 0.35 to less than 0.55 |
> | `4` | 0.55 or greater |
> Vector positions are A, B, C, D. Every packet has at least one nonzero entry.
> [0,2,0,3]
> Revisit Program
> The robot begins at A. It moves along visually overlapping acquisition-neighbor edges and must capture every panel whose debt value is nonzero. The selected route uses the fewest moves. When multiple routes have equal length, alphabetically earlier next panels are preferred.
> | Token | Meaning |
> |---|---|
> | `start:A` | Begin at panel A. |
> | `move:<A-D>` | Move to the stated neighboring view position. |
> | `capture:<A-D>` | Reacquire a panel with nonzero debt. |
> | `seal:coverage` | Finish after every debt panel has been captured. |
> If A has debt, capture:A immediately follows start:A. A panel is captured at most once, although a route may pass through a position more than once.
> start:A>move:B>capture:B>move:D>capture:D>seal:coverage
> Programs are limited to 16 tokens and 240 characters. The capture set must equal the nonzero positions in the submitted debt vector.
> Submission Format
> Write predictions to:
> ./working/submission.csv
> Required columns, in exact order:
> case_id,overlap_bucket_matrix,coverage_debt_vector,revisit_program
> Example:
> case_id,overlap_bucket_matrix,coverage_debt_vector,revisit_program
> 8e43f65e5504d462f065101a,"[[20,7,1,6],[7,20,6,1],[1,6,20,7],[6,1,7,20]]","[0,2,0,3]",start:A>move:B>capture:B>move:D>capture:D>seal:coverage
> Every hidden ID must appear exactly once. Extra, missing, duplicated, or reordered columns are rejected. Duplicate, missing, or unknown IDs and incorrect row counts are rejected. JSON and program values are length-capped before parsing. A malformed field scores zero for its component.
> Evaluation
> Score = 0.50 * OverlapFractionScore
> + 0.25 * CoverageDebtScore
> + 0.25 * RevisitProgramScore
> Minimum score: 0.0
> Maximum score: 1.0
> Higher is better.
> OverlapFractionScore
> Only the six upper-triangle off-diagonal entries are used for partial agreement because symmetry and the diagonal are structural constraints.
> entry_agreement = mean(I(truth = prediction)) over the 6 entries
> row_score = 0.25 * entry_agreement + 0.75 * exact_matrix_match
> OverlapFractionScore = mean(row_score)
> CoverageDebtScore
> entry_agreement = mean(I(truth = prediction)) over A-D
> row_score = 0.25 * entry_agreement + 0.75 * exact_vector_match
> CoverageDebtScore = mean(row_score)
> RevisitProgramScore
> Levenshtein distance is computed over complete >-delimited tokens.
> edit_similarity = 1 - token_edit_distance
> / max(true_token_count, predicted_token_count, 1)
> row_score = 0.25 * edit_similarity + 0.75 * exact_program_match
> RevisitProgramScore = mean(row_score)
> A program is scored only when its capture set exactly matches the submitted debt vector.
> Suitable CPU Methods
> Suitable methods include local feature matching, phase correlation, overlap estimation, compact image-quality models, graph search, and constrained decoding. Validation should hold out complete acquisition configurations.
> What Not To Use
> Do not infer outputs from IDs, filenames, CSV order, fixed byte size, hashes, or filesystem order.
> Do not match panels against external source scans, camera-position tables, motor logs, or registration annotations.
> Do not recover source timestamps, scan identifiers, or acquisition coordinates as lookup keys.
> Do not exploit duplicate rows, extra columns, malformed structures, parser limits, private answers, or leaderboard feedback.

Inspiration note: Useful because it combines overlap estimation, degradation-aware coverage reasoning, and shortest-route decoding into one CPU-friendly structured vision task rather than just image classification.

## Print Ornament Coexistence

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bma24crfdm0yjpjjtk26qz98av5j8
- DOMAIN exactly as displayed: Computer Vision
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> Print Ornament Coexistence
> Overview
> Historical cataloging systems often find two decorative impressions that look related but must answer a more useful question than simple similarity: do they represent unrelated designs, variants active in successive periods, or variants documented during overlapping periods?
> Each row provides a compact symmetric frequency-discrepancy map computed from two authentic ornament crops plus coarse activity bins. Its three channels summarize the spatial-frequency magnitude of fine-scale ink disagreement, coarse-scale ink disagreement, and edge disagreement. This deterministic measurement contains no generated source imagery and does not expose either crop by itself. This computer vision challenge asks solvers to predict the relationships. Evaluation motifs are absent from training, same-family evaluation pairs emphasize visually divergent variants, and independent pairs emphasize visually similar designs. A useful model must generalize visual kinship rather than memorize familiar motifs, then combine that evidence with chronology.
> The labels are:
> INDEPENDENT -- The two ornaments belong to different human-curated motif families.
> SUCCESSIVE_VARIANT -- They belong to the same motif family, but their original observed activity intervals do not share a year.
> COEXISTING_VARIANT -- They belong to the same motif family and their original observed activity intervals share at least one year.
> Dataset
> File descriptions
> train.csv -- 378 labeled ornament pairs from training-only motif families.
> test.csv -- 180 difficult pairs from motif families absent from training, without relationship.
> train/ -- RGB frequency-discrepancy PNGs referenced by train.csv; channels encode fine, coarse, and edge disagreement spectra.
> test/ -- Evaluation pair-discrepancy PNGs referenced by test.csv.
> sample_submission.csv -- A valid two-column submission template with deterministic random labels.
> Column descriptions
> pair_id (string) -- Unique opaque identifier for one ornament pair.
> pair_image (string) -- Path relative to dataset/public/ for the symmetric three-channel frequency-discrepancy map.
> left_start_bin (integer) -- Coarse fifteen-year bin containing the left variant's earliest observed activity.
> left_end_bin (integer) -- Coarse fifteen-year bin containing the left variant's latest observed activity.
> right_start_bin (integer) -- Coarse fifteen-year bin containing the right variant's earliest observed activity.
> right_end_bin (integer) -- Coarse fifteen-year bin containing the right variant's latest observed activity.
> relationship (string) -- Training target: INDEPENDENT, SUCCESSIVE_VARIANT, or COEXISTING_VARIANT.
> The bin origin is intentionally hidden. Bins preserve ordering and approximate overlap but are not calendar years. Labels use the original unrounded activity intervals, so bin overlap alone is not sufficient.
> Evaluation
> Submissions are scored using Weak-Link Catalog Utility, a bounded score from 0 to 1. Higher is better. A cataloging workflow is only useful when it recognizes every relationship type, so the metric rewards overall class balance while explicitly limiting systems that neglect their weakest class or only learn one endpoint.
> macro_f1 = f1_score(truth, prediction, average="macro")
> recalls = recall_score(
> truth,
> prediction,
> labels=["INDEPENDENT", "SUCCESSIVE_VARIANT", "COEXISTING_VARIANT"],
> average=None,
> )
> weakest_recall = min(recalls)
> endpoint_balance = 2 * recalls[0] * recalls[2] / (recalls[0] + recalls[2] + 1e-12)
> score = 0.45 * macro_f1 + 0.35 * weakest_recall + 0.20 * endpoint_balance
> Macro F1 measures balanced classification quality. Weakest-class recall prevents a solver from ignoring independent designs or either chronology class. Endpoint balance is the harmonic mean of INDEPENDENT and COEXISTING_VARIANT recall: both false continuity and missed continuity matter in catalog work, and strong performance on one cannot compensate for failure on the other.
> Submission
> Submit one CSV row for every pair in test.csv.
> pair_id (string) -- Exact identifier from test.csv.
> relationship (string) -- One of the three allowed relationship labels.
> Example using real test identifiers and formatting-only labels:
> pair_id,relationship
> oca_00aa97b6ea3da790,INDEPENDENT
> oca_0108f5f7317ec144,SUCCESSIVE_VARIANT
> Requirements
> The file must contain exactly 180 data rows, one for each test pair.
> Every pair_id from test.csv must appear exactly once; duplicates and unknown identifiers are invalid.
> relationship must be exactly INDEPENDENT, SUCCESSIVE_VARIANT, or COEXISTING_VARIANT.
> File format: CSV with exact columns pair_id,relationship.
> What Not To Use
> Do not use web search, outside visual catalogs, or outside activity tables to recover motif-family or chronology labels for the supplied pair maps.
> Do not reconstruct hidden page identifiers, source-crop filenames, catalog order, or outside variant identifiers from the pair-discrepancy maps.
> Do not build a lookup table that maps public pair or image identifiers to externally recovered relationships.
> Do not use leaderboard probing to hardcode or tune individual evaluation-pair labels.

Inspiration note: Useful because it turns pairwise visual kinship plus coarse chronology into a three-way catalog reasoning task, which is a neat CPU-friendly alternative to plain similarity scoring.


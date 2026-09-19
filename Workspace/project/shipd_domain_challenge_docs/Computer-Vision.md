# Computer Vision Challenge Examples

Scrape timestamp: 2026-07-08T00:00:00+05:30

Confirmed examples in this document: 8

These entries are included because the challenge detail page displayed this domain. Titles were not used for classification.

## Aerial Tree Canopy State Segmentation
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79c1y5vqpe5hjpmxbcpbddkd8a0erp
- DOMAIN exactly as displayed: Computer Vision
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, segmentation
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-08; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Each row contains a high-resolution aerial RGB tile. Your task is to recover a compact run-length ledger over a fixed 128 by 128 spatial lattice. Every cell in that lattice must be assigned one of three canopy states.
> The target cell states are:
> 0: open/background area outside the annotated tree layer.
> 1: merged canopy mass where neighboring tree cover forms a connected group.
> 2: individual crown structure where a single tree crown is annotated separately.
> The output is not an image-level canopy estimate. It is an ordered spatial ledger: the grader expands your JSON runs into 16384 cells and checks whether canopy masses and individual crowns land in the correct places. A solution must read the aerial texture, color, shadow, and crown-shape evidence from the tile.
> Dataset
> train.csv: 600 labeled examples with id, image_path, prompt, image dimensions, answer_format_json, and answer_json.
> test.csv: 400 held-out examples with the same input columns except answer_json.
> sample_submission.csv: 400-row valid baseline submission.
> images/: Aerial RGB tile images referenced by the CSV files.
> Column definitions:
> id (string): Opaque row id.
> image_path (string): Relative image path under images/.
> prompt (string): Natural-language instruction for the row. It states the lattice size and the meaning of the three canopy-state codes.
> frame_width (integer): Width of the input image in pixels.
> frame_height (integer): Height of the input image in pixels.
> answer_format_json (JSON object): Required output schema. It contains type="mask_rle", height=128, width=128, and classes=[0,1,2].
> answer_json (JSON object, train only): Ground-truth run ledger with height, width, classes, and rle.
> RLE format:
> The 128 by 128 lattice is decoded in row-major order from top-left to bottom-right.
> rle is a list of [state_code, count] pairs.
> state_code must be one of 0, 1, or 2.
> count is the number of consecutive cells with that state.
> The run counts must sum to height * width, which is 128 * 128 = 16384 cells.
> Submission Format
> Submit a CSV with exactly these columns: id, answer_json.
> Example:
> id,answer_json
> row_example,"{""height"":128,""width"":128,""classes"":[0,1,2],""rle"":[[0,16384]]}"
> The example assigns every cell to open/background. Real predictions should encode the full 128 by 128 canopy-state lattice.
> Evaluation
> Each submitted run ledger is expanded and compared with the hidden target lattice for the same id.
> For one state code, overlap IoU is:
> intersection(predicted_cells_for_state, true_cells_for_state) / union(predicted_cells_for_state, true_cells_for_state)
> If a state is absent from both prediction and truth, it is ignored for the IoU average.
> The row score is:
> 0.50 * mean_present_state_iou + 0.35 * mean_canopy_state_iou + 0.15 * exact_cell_accuracy
> Definitions:
> mean_present_state_iou: Mean IoU over all state codes whose prediction or target has at least one cell.
> mean_canopy_state_iou: Mean IoU over canopy state codes 1 and 2 that appear in the prediction or target.
> exact_cell_accuracy: Fraction of the 16384 cells where the predicted state equals the hidden target state.
> The final leaderboard score is:
> 0.82 * mean_row_score + 0.06 * worst_area_bin + 0.06 * worst_collection_group + 0.06 * worst_difficulty_bin
> Definitions:
> mean_row_score: Mean row score over all evaluated rows.
> worst_area_bin: Lowest mean row score among private canopy-area groups with at least five rows.
> worst_collection_group: Lowest mean row score among private collection groups with at least five rows.
> worst_difficulty_bin: Lowest mean row score among private difficulty groups with at least five rows.
> Scores range from 0 to 1; higher is better.
> The grader rejects malformed JSON, wrong dimensions, wrong class lists, invalid RLE runs, missing or extra submission columns, wrong row counts, duplicate ids, and submitted ids that do not match the answer ids.
> What Not To Use
> Hardcoded mappings from filenames or row ids to answers.
> Any files, annotations, or metadata outside the released public files.
> Row-order shortcuts or package-internal generation artifacts.

Inspiration note: Useful because it turns image understanding into a pixel/region-level output with clear held-out visual scoring.

## Cataract Surgery Tool Recognition & Anticipation
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70987ba6d2bq7hj6cy8bgjys8a11d2
- DOMAIN exactly as displayed: Computer Vision
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, large-scale, medical
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-08; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Given a single frame from a cataract-surgery microscope video, infer three things:
> primary_tool — the instrument family dominant in THIS frame (or none);
> next_tool — the instrument family dominant in the NEXT frame of the same procedure;
> pupil_frac — the fraction of the frame covered by the visible pupil (0-1).
> primary_tool is a recognition task: read what is in the frame. next_tool is an anticipation task: from one still image you must guess what the surgeon does next, which is only partly determined by the current frame — surgical transitions carry genuine uncertainty. This makes next_tool intrinsically hard and it is where most of the score sits. You receive labelled training frames and unlabelled test frames from surgical cases that never appear in training (no shared patient, eye, or microscope setup), so a solution must generalise to unseen procedures. Test frames are provided in a randomised order with no case or time index — every prediction is from a single image.
> The frames are real cataract surgeries recorded through an operating microscope.
> Evaluation
> A single number in [0, 1] (higher is better):
> score = 0.25 * S_current + 0.60 * S_next + 0.15 * S_pupil
> S_current = difficulty-weighted, class-balanced recall of primary_tool.
> S_next = difficulty-weighted, class-balanced recall of next_tool.
> S_pupil = mean over frames of clip(1 - |pupil_hat - pupil| / 0.02, 0, 1).
> For each categorical target, per-class recall is recall_k = ( sum of frame weights for class-k frames you predicted k ) / ( sum of frame weights for all class-k frames ), and the sub-score is the mean of recall_k over the classes present. Each frame's weight is 1 (large/clear dominant tool), 2 (medium), or 3 (small or occluded — the hard frames), so difficult frames drive the score and a constant guess floors near 1 / (number of classes).
> Because the score is class-balanced, predicting the most common tool everywhere does not help. Because next_tool is only partly predictable from a single frame (and its labels carry a few percent of real annotation noise), even a strong model plateaus on S_next — the attainable total score is bounded well below 1.0. This is intentional: the challenge measures how far you can push a genuinely hard anticipation task, not whether you can memorise frame appearance.
> Any prediction that is missing, non-numeric where a number is required, NaN, infinite, or out of range receives the worst outcome for that component (it never crashes the grader). The score is computed after merging your rows to the answer key on id; row order is irrelevant.
> Dataset (the files you are given)
> train.csv — 1,369 labelled frames from 20 surgical cases, columns:
> id (string), image (string, e.g. images/cf01234.jpg);
> primary_tool, next_tool (strings), pupil_frac (float) — the labels; next_tool and pupil_frac carry small annotation/measurement noise, and the images are lightly augmented, so exact recall of any source value is neither possible nor rewarded.
> test.csv — 839 frames from 10 different surgical cases, columns id and image.
> images/ — all frames referenced above, as 512-px JPEGs.
> sample_submission.csv — a correctly formatted constant baseline.
> primary_tool and next_tool each take exactly one of: none, incision, capsulorhexis, phaco, irrigation_aspiration, lens_implantation, visco_manipulation.
> Submission
> Produce a CSV with exactly one row per id in test.csv and these four columns in this order: id,primary_tool,next_tool,pupil_frac. For example:
> id,primary_tool,next_tool,pupil_frac
> cf00001,irrigation_aspiration,irrigation_aspiration,0.081
> cf00009,phaco,irrigation_aspiration,0.079
> cf00011,phaco,phaco,0.072
> cf00013,capsulorhexis,phaco,0.077
> cf00020,visco_manipulation,none,0.088
> Requirements
> Exactly 839 rows (one per test id) plus the header; ids must match test.csv exactly (no missing, extra, duplicate, or unknown ids).
> Columns present and named exactly id, primary_tool, next_tool, pupil_frac (extra columns are ignored; a missing or renamed required column is rejected).
> primary_tool and next_tool each one of the seven allowed strings; pupil_frac in [0, 1]. Unknown/out-of-range values score worst for that field but do not error.
> What not to use
> Do not use the answer key, attempt to recover it, or reverse-engineer the frame→id assignment; the test frames carry no case or temporal index and must be treated as independent single images.
> Using ImageNet-pretrained backbones, augmentation, and ensembling is allowed and expected. What is prohibited is external labels/data specific to these surgeries.

Inspiration note: Useful because it turns visual recognition, segmentation, temporal anticipation, or localization into a precisely scored image/video benchmark.

## Nucleus Boundary Grid Recovery
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76k6j9t2esm4jvasyj8q9c1n8a28xd
- DOMAIN exactly as displayed: Computer Vision
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, segmentation, medical
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-08; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> This challenge asks you to recover a compact nucleus instance and class boundary map from H&E tissue image fields. Each row provides one RGB histology image field and a required JSON output schema. The hidden target is a 24 by 24 row-major grid derived from expert nucleus annotations.
> For every grid cell, predict:
> class_codes: the dominant nucleus class code in the cell, or 0 for background/no nucleus.
> boundary_bins: a coarse bin for how much annotated nucleus boundary crosses the cell.
> instance_count_bins: the number of nucleus instances touching the cell, capped into bins 0 through 7.
> The task is local visual recovery of nuclei, boundaries, and cell-type structure from the provided image crop.
> Dataset
> The public files are:
> train.csv: 1481 completed training rows.
> test.csv: 263 held-out rows with the same input fields but without answer_json.
> sample_submission.csv: 263-row valid baseline submission.
> images/: RGB JPEG image fields referenced by train.csv and test.csv. The source image dimensions vary by row and are provided in the CSV.
> train.csv columns:
> id: opaque row id.
> image_path: relative path to the input RGB JPEG.
> image_height: source image height in pixels.
> image_width: source image width in pixels.
> answer_format_json: JSON object defining the required output shape and allowed values.
> answer_json: completed training target.
> test.csv columns:
> id: opaque row id.
> image_path: relative path to the input RGB JPEG.
> image_height: source image height in pixels.
> image_width: source image width in pixels.
> answer_format_json: JSON object defining the required output shape and allowed values.
> The answer_format_json object specifies:
> grid_shape: [24, 24].
> array_order: row_major.
> class_codes: allowed class values.
> boundary_bins: allowed boundary-density bins.
> instance_count_bins: allowed instance-count bins.
> Each answer_json object must contain exactly:
> grid_shape: [24, 24].
> class_codes: a length-576 row-major integer list.
> boundary_bins: a length-576 row-major integer list.
> instance_count_bins: a length-576 row-major integer list.
> Submission Format
> Submit a CSV with exactly two columns, in any order:
> id
> answer_json
> Example:
> id,answer_json
> nib_example,"{""grid_shape"":[24,24],""class_codes"":[0,0,1],""boundary_bins"":[0,0,1],""instance_count_bins"":[0,0,2]}"
> The example is shortened for readability. Real submissions must provide all 576 values in each array.
> Evaluation
> The grader aligns rows by id. For each row, it computes three macro-F1 scores over the submitted grid arrays:
> class_macro_f1: macro-F1 over the class_codes labels that are present in the hidden row.
> boundary_macro_f1: macro-F1 over the boundary_bins labels that are present in the hidden row.
> instance_macro_f1: macro-F1 over the instance_count_bins labels that are present in the hidden row.
> For a label v, the per-label F1 is:
> F1(v) = 2 * true_positive(v) / (predicted_count(v) + true_count(v))
> The macro-F1 for an array is the mean of F1(v) over hidden labels present in that row. The row score is:
> row_score = 0.50 * class_macro_f1 + 0.30 * boundary_macro_f1 + 0.20 * instance_macro_f1
> The final score is the mean over all private test rows. A perfect answer file scores exactly 1.0.
> The grader rejects malformed JSON, wrong top-level JSON keys, invalid values, missing or extra submission columns, wrong row counts, missing ids, duplicate ids, and submitted ids that do not exactly match the private answer ids. Submission column order does not matter.
> What Not To Use
> Do not use files, masks, annotations, metadata, or answer files outside the released public files.
> Do not use row order or any organizer-only metadata to infer targets.
> Do not submit masks or files outside the documented answer_json format.

Inspiration note: Useful because it turns visual recognition, segmentation, temporal anticipation, or localization into a precisely scored image/video benchmark.

## Tracing the Coastline Across Unseen Survey Flights
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dqa1e1w4tsst6tmjv21w5rx89jvkx
- DOMAIN exactly as displayed: Computer Vision
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-08; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Where exactly is the land–water line in a drone photograph of a beach? On a real coast it is not a crisp edge — it is a band of wet sand, breaking foam, swash and shadow that shifts with the tide, the light, and the season. Tracing that coastline precisely from aerial imagery underpins coastal-erosion monitoring, yet it is genuinely hard: the target is a thin, wandering curve, its appearance changes completely between survey flights, and being a few pixels off is the difference between a useful map and a useless one.
> This challenge gives you drone images of a Baltic coast and asks your model to delineate the coastline — output the thin curve where land meets water. The test images come from flight sessions that are entirely held out of training, so the lighting, tide and seasonal appearance are ones your model has never seen. Precision is everything: the score is dominated by how tightly your predicted curve hugs the true one and by how well it generalises to the worst unseen session.
> Task
> For each test image, output the coastline as a thin binary mask (the curve pixels), encoded as RLE. Train on the labelled images; predict the images from the held-out sessions.
> Evaluation
> The coastline is a 1–2 px-wide curve, so it is scored with a boundary-F1 blended over 1, 2 and 3 px tolerances — the 1 px term is the strict driver (pixel-accurate localisation), while the 2 and 3 px terms give partial credit for a curve that is close but not pixel-perfect. For one image and a tolerance t:
> precision@t = fraction of your predicted coastline pixels that lie within t px of a gold coastline pixel,
> recall@t = fraction of gold coastline pixels that lie within t px of one of your predicted pixels,
> BoundaryF1@t = 2·precision@t·recall@t / (precision@t + recall@t),
> the per-image BoundaryF1 is the mean of BoundaryF1@1, BoundaryF1@2, BoundaryF1@3,
> computed per image (distances are exact Euclidean nearest-neighbour between the two curves). The composite in [0, 1], higher better:
> Score = 0.50 * MeanBoundaryF1 + 0.50 * WorstSessionsF1
> MeanBoundaryF1 (0.50) — the mean over all test images. Your curve must hug the truth as tightly as possible; on a fuzzy, tide-blurred coast (foam, wet sand, shadow) the 1 px term is where the score is won or lost, while the 2–3 px terms reward getting close.
> WorstSessionsF1 (0.50) — the test images are grouped by their (hidden) flight session; this is the mean of the two lowest per-session mean BoundaryF1 scores. A model that works on most unseen sessions but collapses on the hardest ones is heavily penalised — it rewards robust cross-session generalisation.
> An empty prediction scores 0 for that image. A prediction may cover at most 60,000 pixels per image (a real coastline curve is a few thousand); a denser blanket/area mask causes the submission to be rejected, so predict a thin curve.
> Dataset
> All images are resized drone photographs (width 1024 px). All CSV fields are as described; there are no missing values.
> public/images/<image_id>.jpg — resized drone images (1024 px wide).
> public/train.csv — one row per training image. Columns:
> image_id (string) — unique salted image identifier, e.g. CST_a1b2c3d4e5f6.
> image (string) — relative path (images/<image_id>.jpg).
> width (integer), height (integer) — image dimensions in pixels.
> public/train_coastlines.csv — one row per training image. Columns:
> image_id (string) — foreign key to train.csv.
> rle (string) — the gold coastline mask, RLE-encoded (see below).
> public/test.csv — one row per test image; same schema as train.csv. Coastlines withheld.
> public/sample_submission.csv — a median-row-prior baseline (a single thin line at the typical coastline row; a valid thin-curve example that scores near zero).
> public/metadata.json — composite weights, RLE definition, submission schema.
> RLE encoding. The coastline mask is flattened row-major (C order) and encoded as a space-separated string of start length pairs, one pair per run of foreground pixels: start is the 0-based flat pixel index (row * width + col) of the run's first pixel, length is the run length. An empty string means "no coastline predicted".
> Submission Format
> Submit a CSV at ./working/submission.csv with exactly these columns:
> image_id,rle
> CST_a1b2c3d4e5f6,12044 3 13068 2 14092 2 ...
> CST_b2c3d4e5f6a1,8190 2 9214 2 ...
> Requirements (strict — the grader rejects a violating submission rather than repairing it):
> Exactly the two columns image_id, rle; no extra columns; no null/duplicate image_ids.
> Exactly one row per test image_id, and only test image_ids — the submission's id set must match the test set exactly. Missing required ids or extra/unknown ids cause the submission to be rejected.
> RLE indices must be within width * height; malformed runs are ignored. Predict a thin curve (1–2 px): a prediction covering more than 60,000 pixels on any image is rejected, and a thick band scores poorly on precision regardless.
> Approach Guidelines
> A segmentation model (U-Net / DeepLab / a boundary-aware head) or an edge/curve regressor that outputs a thin coastline is the natural approach; keep the curve thin — over-thick predictions wreck precision at the strict 1 px tolerance.
> Generalise across sessions. WorstSessionF1 means one unseen session you handle badly caps half the score; augment heavily over lighting/colour/tide appearance.
> The land–water boundary is fuzzy (foam, wet sand, shadow) — sub-pixel-accurate localisation under that ambiguity is the central difficulty.
> What Not To Use
> Matching the released images against the source survey dataset (reverse image search, perceptual hashing, geolocation/EXIF) to recover the gold coastline. Image ids are salted and EXIF is stripped.
> Any external annotated coastline dataset tied to this coast used to look up answers for these specific images.
> Hardcoded {image_id → coastline} tables, or training on the test images.

Inspiration note: Useful because it turns visual recognition, segmentation, temporal anticipation, or localization into a precisely scored image/video benchmark.

## Neuron 3D Branching-Topology Prediction from 2D Projection Images
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73c4vfj2rz1wm4j668bw0nzd8a5p0g
- DOMAIN exactly as displayed: Computer Vision
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, medical, 3d-medical, feature-engineering, small-data
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-08; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> A neuron's dendritic arbor is a three-dimensional branching tree that grows out from the cell body
> (soma). How that tree is organised — how many branches it has and how they nest at increasing
> distances from the soma — shapes how the neuron collects and integrates its inputs, and is one of the
> primary features used to tell neuron types apart. Neuroanatomists capture this branching organisation
> compactly with a persistence barcode: a small, unordered set of (birth, death) intervals, from
> topological data analysis, that records the tree's branching structure under a distance-from-the-soma
> sweep (the Topological Morphology Descriptor).
> Reading that 3D structure normally requires a full, painstaking 3D reconstruction of the cell. A single
> 2D image of a filled neuron — the kind produced by ordinary widefield microscopy or by flattening
> (projecting) a 3D image stack onto one plane — is far cheaper to obtain, but it loses the depth
> axis: neurites that are separated in 3D overlap in the picture, and distances along the line of sight
> are foreshortened. This challenge asks: from a single 2D projection image of a neuron's dendritic
> arbor, can you recover the persistence barcode of its underlying 3D branching tree?
> You are given a large set of grayscale projection images, each showing one neuron's dendritic arbor at
> an arbitrary in-plane orientation, with the soma at the centre of the frame. Each training image is
> paired with the ground-truth barcode of that neuron's 3D tree. For the test images the barcode is
> withheld and you must predict it. The images come from many different laboratories and species; the
> test images are from sources not represented in the training set, so your model must generalise to
> neurons it has never seen, imaged under conditions it has never seen.
> Because a single flat projection cannot fully determine the 3D tree (branches hidden behind others, or
> pointing along the viewing direction, are ambiguous), even a perfect model cannot be exactly right on
> every neuron — the task has an irreducible error floor and leaves genuine head-room. A model that has
> learned what real dendritic trees look like can nonetheless recover the barcode far better than any
> depth-blind rule.
> What you predict
> For each image (one row) you predict that neuron's radial-distance persistence barcode: an
> unordered set of (birth, death) pairs describing its 3D dendritic branching. The barcode is defined
> as follows:
> The dendritic tree is rooted at the soma. Every point on the tree has a radial distance = its
> straight-line (Euclidean) distance to the soma, in 3D.
> Sweep a threshold inward, from the farthest points toward the soma. Each dendritic tip starts a
> branch "component" that is born at that tip's radial distance. When two branches meet at a
> branch point, the branch whose tip reaches less far dies at that branch point's radial
> distance, while the farther-reaching branch continues. The single primary branch finally dies at the
> soma (radial distance 0).
> This produces one (birth, death) pair per branch: birth = the radial distance of the branch's
> farthest tip; death = the radial distance at which it merges into a longer branch (0 for the
> primary branch). Every pair satisfies birth >= death >= 0.
> All values are normalised by the neuron's maximum radial reach, so birth lies in (0, 1] and
> death lies in [0, 1]. The barcode is therefore a scale-free descriptor of branching
> topology: it encodes the arrangement of branches, not the absolute size of the cell.
> The number of pairs (bars) equals the number of dendritic branches and varies from neuron to neuron
> (between 15 and 90 in this data). Predicting how many bars there are, and where each lies in
> the (birth, death) plane, are both part of the task.
> Data
> You are given:
> train/images/<row_id>.png    one grayscale projection image per training neuron
> train.csv                    row_id + barcode (the ground-truth 3D barcode)
> test/images/<row_id>.png     one grayscale projection image per test neuron
> test.csv                     row_id only
> sample_submission.csv        a correctly-formatted, low-scoring baseline
> Images. Each image is a single-channel 8-bit PNG, 160 x 160 pixels. Bright pixels are neurite
> / soma; dark pixels are background. The soma is at the centre of the frame; the arbor is shown at an
> arbitrary in-plane orientation and is scaled to fit the frame (absolute size is not recoverable from
> the image, which is why the target is scale-free).
> train.csv (3989 rows) — columns:
> row_id — string — unique opaque identifier; matches train/images/<row_id>.png.
> barcode — string — the ground-truth barcode: a space-separated list of birth:death tokens, each
> a pair of decimal numbers with birth >= death >= 0 and birth <= 1. Example (truncated):
> 1.0000:0.0000 0.83:0.27 0.61:0.13 .... The order of the tokens is not meaningful (it is an
> unordered set).
> test.csv (1792 rows) — one column:
> row_id — string — unique opaque identifier; matches test/images/<row_id>.png.
> sample_submission.csv (1792 rows) — row_id plus a barcode column filled with a fixed
> baseline barcode. It is valid and correctly formatted but deliberately weak (it scores the floor);
> replace the barcode values with your predictions.
> Submission format
> Submit a CSV with a header and exactly these 2 columns, in this order:
> row_id, barcode
> Exactly 1792 rows (one per test.csv row_id), each row_id present exactly once.
> No missing, duplicate, extra, unknown, or reordered ids; no extra or missing columns.
> barcode is a space-separated list of birth:death tokens (each token has exactly one :).
> Each token is a predicted (birth, death) bar. Values should lie in the normalised range [0, 1]
> (birth >= death >= 0, birth <= 1) — the same range as the target barcode. The grader tolerates a
> small overshoot but rejects any value below 0 or above 1.5 (or any non-finite value) as malformed.
> An empty string is accepted (it means "predict no bars") but scores poorly. At most 2000 bars per row.
> Concrete example of a correctly-formatted submission (row_id, then a barcode string):
> row_id,barcode
> prx-018-4af2,1.0000:0.0000 0.8123:0.2740 0.6050:0.1310 0.4400:0.0900
> prx-002-9c1a,1.0000:0.0000 0.7700:0.0000 0.5200:0.3100 0.3300:0.1200 0.2100:0.0400
> prx-114-0b7d,1.0000:0.0000 0.9100:0.4500 0.6600:0.2600 0.5100:0.1900 0.2900:0.0700 0.1500:0.0300
> (The three rows above show different bar counts; the first bar 1.0000:0.0000 — the primary branch —
> is present for essentially every neuron.)
> better; Maximize). It compares each predicted barcode to the true barcode with the standard
> 1-Wasserstein (optimal-transport) distance between persistence diagrams, then maps that distance to
> a skill score that is chance-corrected against the best constant prediction.
> Per-row distance. Treat each barcode as a set of points (birth, death) in the plane. The
> 1-Wasserstein distance W(P, T) between a predicted diagram P and the true diagram T is the
> minimum-cost matching in which every point may be matched either to a point of the other diagram or to
> its own orthogonal projection onto the diagonal {birth = death}, with cost equal to the Euclidean
> distance moved (a point matched to the diagonal costs its distance to it, |birth - death| / sqrt(2)).
> This is computed exactly by solving the corresponding assignment problem; it naturally handles diagrams
> with different numbers of bars (extra / missing bars are matched to the diagonal).
> Distance-to-score. With a fixed scale TAU = 10:
> raw_i   = exp( - W(P_i, T_i) / TAU )                     # per test row i
> raw_bar = mean_i raw_i                                    # mean over all test rows
> # no-skill reference = the best a single constant barcode can do:
> ref = max over C in {empty barcode, R} of  mean_i exp( - W(C, T_i) / TAU )
> skill = clip( (raw_bar - ref) / (1 - ref), 0, 1 )
> Score = clip( 0.05 + 0.95 * skill, 0.05, 1.0 )
> Here R is a fixed population-median reference barcode defined inside the grader, and C ranges over
> the two constant strategies (predicting nothing, or predicting R for every neuron). Subtracting ref
> removes the credit obtainable with no skill: any constant submission — including the provided
> sample_submission.csv — scores the floor 0.05, a submission identical to the ground truth scores
> 1.0, and better predictions score smoothly in between. Because a single 2D projection cannot fully
> determine the 3D tree, the maximum reachable by a real model is well below 1.0.
> def evaluate(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> """Persistence-Barcode Wasserstein Concordance (chance-corrected vs the best constant barcode).
> Returns a float in [0.05, 1.0]; higher is better (Maximize). Raises ValueError on a malformed
> submission (wrong/missing/extra/reordered columns or ids, duplicate ids, unparseable barcode
> token, or non-finite / out-of-range birth/death values)."""
> ...
> What makes this different (relation to prior work)
> Not neuron reconstruction / tracing. Standard morphology pipelines consume a full 3D image
> stack and output a traced skeleton. Here the input is a single flattened 2D projection and the
> output is a compact topological summary of the 3D tree — a genuinely under-determined inverse
> problem, not a tracing task.
> Not a barcode computed from a known morphology. Topological Morphology Descriptors are usually
> computed from an already-reconstructed 3D tree and then used as features. Here the 3D tree is
> hidden; you must infer its barcode from appearance alone.
> A topological-data-analysis target, scored by an optimal-transport distance between persistence
> diagrams — distinct from per-pixel, per-class, or per-scalar objectives.
> Notes
> Pre-trained vision backbones are allowed and expected to help; you must still train on the
> provided training data.
> The target barcode is invariant to how the neuron is oriented in the image plane, so in-plane
> rotations and flips are label-preserving augmentations.
> See the challenge's "What not to use" guidance for prohibited shortcuts — in particular,
> skeletonising the 2D image and computing a barcode from that skeleton by a fixed rule is a non-ML
> shortcut and scores at the floor.
> What Not To Use
> This is a machine-learning challenge: the intended solution learns to infer a neuron's hidden
> 3D branching topology from the appearance of a single 2D projection image. Solutions that
> recover the answer by any non-ML / "raw logic" route are out of scope and will be rejected on
> review even if they score well.
> Prohibited
> Hand-coded skeletonization / tracing + a rule-based barcode computation. Thresholding the
> image, skeletonizing it, building a graph, and computing a persistence barcode from that 2D
> skeleton by a fixed algorithm is a non-solution: a single 2D projection collapses depth and
> overlaps neurites, so the 2D skeleton is systematically wrong and this pipeline scores at the
> floor. Such classical descriptors may be inputs/features to a learned model, but a rule-based
> pipeline with no learning is rejected.
> Any other classical-CV heuristic as the whole solution: edge/line/Hough fitting, connected
> components, morphological skeletons, distance transforms, FFT/autocorrelation, moments, or
> PCA-on-pixels used to directly produce the barcode.
> Regex / lookup / rule-based parsing of ids or filenames to derive predictions.
> Exploiting non-semantic artifacts: frame/border effects, file ordering, row_id structure,
> image metadata, or any side channel. The ids are opaque and carry no label information; the row
> order is randomised.
> Hard-coded constants or answer lookups: constant / population-average barcodes, per-id answer
> tables, or any row_id -> barcode mapping.
> Reconstructing the labels from an external neuron-morphology collection. Do not attempt to
> match a test image to any external database of 3D neuron reconstructions (by rendering candidate
> morphologies and matching, by hashing, by reverse image search, or by near-duplicate retrieval)
> to look up the true barcode. The images are re-rendered projections at an arbitrary orientation;
> such matching is both unreliable and disallowed.
> External data or pre-trained task weights beyond generic vision backbones. Do not train on, or
> fine-tune from, any external corpus of neuron morphologies / persistence barcodes. Generic
> ImageNet-pretrained backbones are allowed; task-specific pre-baked weights are not.
> Test-set leakage / coupling. In particular, all of the following are prohibited:
> (a) Test-time augmentation (TTA) — including averaging predictions over multiple rotations /
> flips of a test image. (The target is orientation-invariant, so TTA is an obvious temptation; it
> is disallowed.)
> (b) Pseudo-labelling / self-training / any transductive use of the test set (no training or
> fine-tuning on test predictions; no feeding test inferences back into training).
> (c) Lookup tables tied to the test set (per-id answer maps).
> (d) Fitting, adapting, or normalising on test-set statistics, or any interaction with the
> test set beyond the single final forward pass that produces the submission.
> (e) Inference-only solutions that ship pre-baked trained weights instead of training in the
> solution. You must train your model on the provided training images and their barcodes; the
> test set may be used only to produce the final predictions.
> Allowed (and encouraged)
> Any learned model: CNNs, vision transformers, encoder-decoder / heatmap / set-prediction heads,
> hybrid architectures, etc.
> Pre-trained vision backbones (ImageNet ResNet/ViT/etc.) as feature extractors or for
> fine-tuning — encouraged; they typically help.
> Standard, label-preserving training-time augmentation: horizontal/vertical flips and in-plane
> rotations are label-preserving here (the target is invariant to how the neuron is oriented in the
> image plane), as are mild noise/blur.
> Classical image descriptors used as auxiliary inputs to a learned model (not as the whole
> solution).
> Standard Kaggle-environment libraries (numpy, pandas, scikit-learn, PyTorch, TensorFlow, etc.).
> Non-ML solutions, or solutions that violate any item above, are rejected on review regardless of
> leaderboard score.

Inspiration note: Useful because it turns visual recognition, reconstruction, segmentation, temporal anticipation, or localization into a precisely scored image/video benchmark.

## RGB-D Object Projection Trace Recovery
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx732pfbje94na65bkeaqeqna18a22bm
- DOMAIN exactly as displayed: Computer Vision
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, multimodal
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-08; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Your objective is to recover a sparse image-space metrology ledger for a target object from a registered color frame, paired range image, calibration matrix, and loose target window.
> The data represents cluttered indoor workbench scenes captured with a calibrated color-plus-depth sensor. The scenes contain manufactured parts and simple solids under ordinary indoor lighting, with partial occlusion and nearby distractor objects. This kind of geometry ledger is useful when a system needs image-space measurement traces for manipulation, inspection, or spatial alignment rather than only a rectangular object crop.
> The ledger contains one anchor point, three calibrated endpoint markers, twelve perimeter trace segments, and a visibility bin. This is not a 2D detection task: the loose target window is already provided, and the score depends on placing the object's measurement traces accurately in pixel coordinates.
> Image coordinates use pixel units with origin at the top-left of the frame, u increasing to the right, and v increasing downward.
> Dataset
> train.csv: 350 labeled target rows with answer_json.
> test.csv: 250 held-out target rows without answer_json.
> sample_submission.csv: 250-row valid baseline submission.
> rgb/: Color PNG frames.
> depth/: Range PNG maps aligned with the color frames.
> Column definitions:
> id (string): Opaque row id.
> rgb_path (string): Relative path to the color image.
> depth_path (string): Relative path to the paired range image.
> prompt (string): Task instruction.
> frame_width (integer): Frame width in pixels.
> frame_height (integer): Frame height in pixels.
> camera_intrinsics_json (JSON list): 3-by-3 calibration matrix for the paired color/range frame.
> target_window_json (JSON object): Loose normalized target window with x, y, w, and h values. These are fractions of the full frame and are intended only to identify the target region.
> answer_format_json (JSON object): Required fields and value conventions.
> answer_json (JSON object, train only): Ground-truth metric trace ledger.
> answer_json has this structure:
> origin_uv (list of numbers): [u, v] pixel coordinate of the target object's anchor point.
> axis_uv (JSON object): The field name is fixed by the grader. It contains keys x, y, and z; each value is a [u, v] pixel coordinate for one calibrated endpoint marker.
> box_edges (JSON list): The field name is fixed by the grader. It contains exactly 12 perimeter trace segments. Each segment is [[u1, v1], [u2, v2]] in pixel coordinates. Segment index order should follow the training examples; the two endpoints inside a segment may be swapped without penalty.
> visibility_bin (string): One of v0, v1, v2, or v3, representing the target's visible geometry level.
> Some trace points can lie slightly outside the visible frame when the object is partially clipped.
> Submission Format
> Submit a CSV with exactly these columns: id, answer_json.
> Example:
> id,answer_json
> row_example,"{""origin_uv"":[312.4,214.7],""axis_uv"":{""x"":[335.1,205.2],""y"":[299.0,190.8],""z"":[280.3,215.1]},""box_edges"":[[[210.0,180.0],[260.0,184.0]],[[260.0,184.0],[270.0,230.0]],[[270.0,230.0],[218.0,226.0]],[[218.0,226.0],[210.0,180.0]],[[215.0,170.0],[268.0,174.0]],[[268.0,174.0],[280.0,220.0]],[[280.0,220.0],[224.0,216.0]],[[224.0,216.0],[215.0,170.0]],[[210.0,180.0],[215.0,170.0]],[[260.0,184.0],[268.0,174.0]],[[270.0,230.0],[280.0,220.0]],[[218.0,226.0],[224.0,216.0]]],""visibility_bin"":""v2""}"
> Evaluation
> Each row score is:
> 0.20 * origin_score + 0.38 * axis_endpoint_score + 0.36 * box_edge_score + 0.06 * visibility_score
> All point distances are Euclidean distances in image pixels:
> dist(a, b) = sqrt((a_u - b_u)^2 + (a_v - b_v)^2)
> The point score is an exponential pixel-distance penalty:
> point_score(a, b, sigma) = exp(-dist(a, b) / sigma)
> Metric components:
> origin_score = point_score(pred_origin_uv, true_origin_uv, 38).
> axis_endpoint_score is the mean of the three endpoint-marker scores in axis_uv, using sigma=42 for x, y, and z.
> For each of the 12 submitted box_edges, the grader compares it to the true trace segment at the same segment index. Because a segment has no direction, the grader scores both endpoint orders and keeps the better one:
> direct = point_score(pred_p1, true_p1, 42) + point_score(pred_p2, true_p2, 42)
> swapped = point_score(pred_p1, true_p2, 42) + point_score(pred_p2, true_p1, 42)
> edge_score = max(direct, swapped) / 2
> box_edge_score is the mean of the 12 segment edge_score values.
> visibility_score = 1 if the submitted visibility_bin exactly matches the hidden value, otherwise 0.
> The final leaderboard score is:
> 0.82 * mean_row_score + 0.06 * worst_visibility_group + 0.06 * worst_object_count_group + 0.06 * worst_object_token_group
> mean_row_score is the average row score over the hidden answers. Each worst-group term is also a 0-to-1 mean row score: it is the lowest mean row score among held-out grouping labels with at least five rows for that grouping axis. Therefore the final score is also between 0 and 1. Higher is better.
> worst_visibility_group is not the standalone visibility_score; it is the lowest mean full row score after grouping rows by the held-out visibility bucket.
> worst_object_count_group is the lowest mean full row score after grouping rows by scene clutter level: single, pair, few, or crowded. worst_object_token_group is the lowest mean full row score after grouping rows by the opaque target-object bucket such as obj_01, obj_02, and so on.
> What Not To Use
> Hardcoded mappings from filenames or row ids to geometry labels.
> Any files, geometry fields, masks, or annotations outside the released public files.
> Row-order shortcuts or package-internal generation artifacts.

Inspiration note: Useful because it turns visual recognition, reconstruction, segmentation, temporal anticipation, or localization into a precisely scored image/video benchmark.

## Capsule Mucosa Visibility
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78amrc9zr7spwc722tm3qyw18a2bsg
- DOMAIN exactly as displayed: Computer Vision
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, image, multimodal
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-08; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Each example contains one RGB capsule endoscopy frame and a short review-context card. The task is to decide which part of the frame is still clinically salvageable for mucosa review, then express that decision as a structured obstruction map.
> This is not a clean-versus-dirty classifier. The frame can contain fluid, bubbles, debris, low contrast, edge contamination, or partial visibility. A useful solution must identify the main clear-view region, quantify the obstruction pattern, map local mucosa visibility, reconstruct the ordered contamination ledger, and assign a triage status.
> You must predict five fields:
> | Output | What it represents |
> |---|---|
> | `clear_focus_box` | Normalized box around the main salvageable clear-view region. |
> | `cleanliness_vector` | Length-7 obstruction vector covering clear area, turbidity, bubbles, dominant zone, edge obstruction, texture visibility, and confidence. |
> | `mucosa_visibility_grid` | `4x4` spatial grid of mucosal visibility levels. |
> | `contamination_sequence` | Ordered token sequence that summarizes the contamination evidence chain. |
> | `triage_status` | Final review disposition: `clear`, `usable`, `limited`, `obscured`, or `manual_review`. |
> Dataset
> The prepared dataset contains:
> | Item | Value |
> |---|---:|
> | Training rows | 1000 |
> | Test rows | 393 |
> The prepared files are:
> | Path | Type | Description |
> |---|---|---|
> | `dataset/public/train.csv` | CSV file | Training rows with public inputs and all target columns. |
> | `dataset/public/test.csv` | CSV file | Test rows with public inputs only. |
> | `dataset/public/images/` | directory | Public JPEG capsule frames referenced by `image_path`. |
> | `dataset/public/sample_submission.csv` | CSV file | Submission template with the exact required schema. |
> | `dataset/private/answers.csv` | CSV file | Private answer file with `sample_id` and all five target columns. |
> Input Columns
> | Column | Type | Description |
> |---|---|---|
> | `sample_id` | string | Opaque public identifier. |
> | `image_path` | string | Relative path to the public capsule frame. |
> | `review_context` | string | Short context stating that the frame needs visibility triage. |
> | `visibility_request` | string | Natural-language instruction for the salvageability map. |
> | `capture_note` | string | Coarse frame-quality note with tone, color bias, and source resolution. |
> Example input row:
> | Column | Example value |
> |---|---|
> | `sample_id` | `cva_example` |
> | `image_path` | `images/cva_example.jpg` |
> | `review_context` | `Single capsule endoscopy frame. Audit whether mucosa is visibly assessable despite fluid, bubbles, or debris.` |
> | `visibility_request` | `Return the clear-view focus box and the structured contamination ledger from the image.` |
> | `capture_note` | `frame_tone=balanced; color_bias=warm; source_resolution=336x336` |
> Target Columns
> | Column | Type | Description |
> |---|---|---|
> | `clear_focus_box` | JSON numeric array | Normalized `[x, y, width, height]` box around the main clear-view region. Values must be in `[0, 1]`, with positive width and height. |
> | `cleanliness_vector` | JSON integer array | Length-7 vector `[clear_area_bucket, turbid_bucket, bubble_bucket, dominant_obstruction_zone, edge_obscuration_count, texture_visibility_bucket, confidence_bucket]`. |
> | `mucosa_visibility_grid` | JSON integer matrix | Shape `4x4`. Values from `0` through `3`, where larger values mean clearer visible mucosa. |
> | `contamination_sequence` | ordered token sequence | Tokens separated by `>`, such as `inspect_capsule>clear_4>turbid_1>bubble_0>dominant_lower_left>edge_2>status_usable`. |
> | `triage_status` | categorical string | One of `clear`, `usable`, `limited`, `obscured`, or `manual_review`. |
> Target Value Details
> | Field | Valid values |
> |---|---|
> | `clear_area_bucket` | Integer from `0` through `5`. |
> | `turbid_bucket` | Integer from `0` through `5`. |
> | `bubble_bucket` | Integer from `0` through `5`. |
> | `dominant_obstruction_zone` | `0=upper_left`, `1=upper_mid`, `2=upper_right`, `3=mid_left`, `4=mid_center`, `5=mid_right`, `6=lower_left`, `7=lower_mid`, `8=lower_right`. |
> | `edge_obscuration_count` | Integer from `0` through `4`. |
> | `texture_visibility_bucket` | Integer from `0` through `4`. |
> | `confidence_bucket` | Integer from `0` through `3`. |
> Example target row:
> | Column | Example value |
> |---|---|
> | `clear_focus_box` | `[0.1429,0.0833,0.7619,0.8095]` |
> | `cleanliness_vector` | `[4,1,0,7,2,2,2]` |
> | `mucosa_visibility_grid` | `[[2,3,3,2],[2,3,3,2],[1,2,3,2],[0,1,2,1]]` |
> | `contamination_sequence` | `inspect_capsule>clear_4>turbid_1>bubble_0>dominant_lower_mid>edge_2>status_usable` |
> | `triage_status` | `usable` |
> Class Distribution
> | `triage_status` | Train rows | Test rows |
> |---|---:|---:|
> | `clear` | 440 | 186 |
> | `limited` | 117 | 46 |
> | `manual_review` | 124 | 46 |
> | `obscured` | 20 | 18 |
> | `usable` | 299 | 97 |
> Submission Format
> Write the final submission CSV to exactly ./working/submission.csv.
> If the runtime root is /workspace, the equivalent absolute path is /workspace/working/submission.csv.
> The submission must contain exactly these columns in this order:
> | Order | Column |
> |---:|---|
> | 1 | `sample_id` |
> | 2 | `clear_focus_box` |
> | 3 | `cleanliness_vector` |
> | 4 | `mucosa_visibility_grid` |
> | 5 | `contamination_sequence` |
> | 6 | `triage_status` |
> Example submission row:
> | Column | Example value |
> |---|---|
> | `sample_id` | `cva_example` |
> | `clear_focus_box` | `[0.1429,0.0833,0.7619,0.8095]` |
> | `cleanliness_vector` | `[4,1,0,7,2,2,2]` |
> | `mucosa_visibility_grid` | `[[2,3,3,2],[2,3,3,2],[1,2,3,2],[0,1,2,1]]` |
> | `contamination_sequence` | `inspect_capsule>clear_4>turbid_1>bubble_0>dominant_lower_mid>edge_2>status_usable` |
> | `triage_status` | `usable` |
> Every sample_id from dataset/public/test.csv must be present exactly once. Extra columns, missing columns, reordered columns, duplicate IDs, wrong row count, missing test IDs, extra IDs, or oversized sample IDs cause grading to fail.
> Evaluation
> Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> The final score is:
> Score =
> 0.24 * SalvageWindowScore
> + 0.42 * ObstructionMapScore
> + 0.16 * ContaminationLedgerScore
> + 0.18 * ReviewDispositionScore
> Component Summary
> | Component | Inputs | Weight | Formula |
> |---|---|---:|---|
> | `SalvageWindowScore` | `clear_focus_box` | 0.24 | `0.75 * IoU + 0.25 * CenterScore` |
> | `ObstructionMapScore` | `cleanliness_vector`, `mucosa_visibility_grid` | 0.42 | `0.45 * CleanlinessVectorScore + 0.55 * VisibilityGridScore` |
> | `ContaminationLedgerScore` | `contamination_sequence` | 0.16 | `0.25 * normalized_similarity + 0.75 * exact_sequence_match` |
> | `ReviewDispositionScore` | `triage_status` | 0.18 | Fixed weighted accuracy over triage labels. |
> Metric Details
> SalvageWindowScore: The submitted box must be a valid normalized [x, y, width, height] box. IoU is standard intersection over union. CenterScore = max(0, 1 - L1_center_distance).
> CleanlinessVectorScore: Parses a length-7 JSON integer vector. Entry weights are w_i = 1 + true_i. Weighted entry agreement is sum_i(w_i * 1[pred_i == true_i]) / sum_i(w_i). Row score is 0.42 * weighted_entry_agreement + 0.58 * exact_vector_match.
> VisibilityGridScore: Parses a 4x4 JSON integer matrix with values from 0 through 3. It uses the same weighted entry agreement formula as CleanlinessVectorScore, with exact-match weight 0.50.
> ContaminationLedgerScore: Tokens are split on >. Let edit_distance be standard Levenshtein distance between true and predicted token sequences. normalized_similarity = max(0, 1 - edit_distance / max(len(true_tokens), len(pred_tokens))). Row score is 0.25 * normalized_similarity + 0.75 * exact_sequence_match. The exact-match term is intentionally high because the sequence is an ordered evidence ledger.
> ReviewDispositionScore: Uses fixed public row weights by true class: clear=1.0, usable=1.3, limited=2.0, obscured=3.5, and manual_review=2.0. For each row, row_score = 1 if the submitted status exactly matches the true status and is valid, otherwise 0. The component is sum(weight_true * row_score) / sum(weight_true).
> Invalid JSON, wrong shapes, non-finite numbers, out-of-range values, overlong strings, overlong token lists, and invalid category labels receive zero for the affected component. Ground-truth values are validated strictly and are not clipped.
> The final weighted score is clipped to [0.0, 1.0]. An exact submission scores 1.0.
> What Not To Use
> Do not use lookup tables or deterministic mappings from sample_id, public image paths, public image file names, raw frame identifiers, file order, public row order, archive order, image byte hashes, compression artifacts, split artifacts, hidden source metadata, or private answer files to target values.
> Do not hardcode labels for individual public rows, scrape private answer files, modify the grader, exploit duplicated files, or infer answers from train/test membership. A valid solution should infer the structured salvageability map from the supplied public image and public context only.

Inspiration note: Useful because it turns visual recognition, reconstruction, segmentation, temporal anticipation, or localization into a precisely scored image/video benchmark.

## Shadow-Based GPS and Time Prediction
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70wnk1p7139nvg52sj0ght6188w7c0
- DOMAIN exactly as displayed: Computer Vision
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-11; includes user-provided reviewer/creator discussion about UTC-hour/longitude coupling and benchmark validity.

Full challenge description from page:

> Overview
> Given a single outdoor photograph containing visible shadows, predict the GPS coordinates (latitude, longitude) and UTC hour the image was captured. The only reliable geolocation cues are shadow geometry — length, direction, sharpness — combined with sky appearance and terrain texture.
> This is an inverse sun-position problem: from a 2D projection of 3D shadow-casting geometry, recover where on Earth and when the image was taken. The task requires implicit understanding of solar geometry, atmospheric optics, and terrain cues — all learned from visual features through computer vision.
> Evaluation
> Submissions are scored using a composite of Haversine distance for geolocation and circular mean absolute error for time. The composite score ranges from ~0 to 1 (higher is better).
> Haversine Distance (Geolocation Error)
> Given predicted coordinates (lat₁, lon₁) and ground truth (lat₂, lon₂):
> Δ
> lat
> =
> lat
> 2
> −
> lat
> 1
> Δ
> lon
> =
> lon
> 2
> −
> lon
> 1
> Δlat=lat
> 2
> ​
> −lat
> 1
> ​
> Δlon=lon
> 2
> ​
> −lon
> 1
> ​
> 𝑎
> =
> sin
> ⁡
> 2
> (
> Δ
> lat
> 2
> )
> +
> cos
> ⁡
> (
> lat
> 1
> )
> ⋅
> cos
> ⁡
> (
> lat
> 2
> )
> ⋅
> sin
> ⁡
> 2
> (
> Δ
> lon
> 2
> )
> a=sin
> 2
> (
> 2
> Δlat
> ​
> )+cos(lat
> 1
> ​
> )⋅cos(lat
> 2
> ​
> )⋅sin
> 2
> (
> 2
> Δlon
> ​
> )
> 𝑑
> =
> 6371
> ×
> 2
> ×
> arcsin
> ⁡
> (
> min
> ⁡
> (
> 𝑎
> ,
> 1.0
> )
> (km)
> d=6371×2×arcsin(
> min(a,1.0)
> ​
> )(km)
> Circular Hour Error (Time Error)
> 𝑒
> hour
> =
> min
> ⁡
> (
> ∣
> hour
> 1
> −
> hour
> 2
> ∣
> ,
> 24
> −
> ∣
> hour
> 1
> −
> hour
> 2
> ∣
> )
> e
> hour
> ​
> =min(∣hour
> 1
> ​
> −hour
> 2
> ​
> ∣,24−∣hour
> 1
> ​
> −hour
> 2
> ​
> ∣)
> Composite Score
> geoscore
> =
> 1
> +
> 𝑑
> ‾
> /
> 500
> timescore
> =
> 1
> +
> 𝑒
> hour
> ‾
> /
> 3
> geoscore=
> 1+
> d
> /500
> 1
> ​
> timescore=
> 1+
> e
> hour
> ​
> /3
> 1
> ​
> score
> =
> 0.5
> ×
> geoscore
> +
> 0.5
> ×
> timescore
> score=0.5×geoscore+0.5×timescore
> ​
> Where
> 𝑑
> ‾
> d
> is the mean Haversine distance across all test samples, and
> 𝑒
> hour
> ‾
> e
> hour
> ​
> is the mean circular hour error. The reference values (500 km, 3 h) normalize each component to a ~[0, 1] range before averaging.
> Anti-cheat: Individual samples with raw geo error exceeding 10,000 km (more than a quarter of Earth's circumference) have their error multiplied by 1.5 before computing the mean. This penalizes degenerate strategies such as predicting a fixed midpoint for all samples.
> Expected baselines:
> Random guessing (uniform lat/lon/hour): ~0.18 (mean geo error ~10,000 km, mean time error ~6 h)
> Sample submission (all zeros): ~0.23 (lat=0, lon=0, hour=12.0 — better than random)
> Physics-aware model (implicit sun geometry): ~0.70+
> Perfect prediction: 1.0
> Dataset
> The dataset consists of 8,000 fully synthetic outdoor images (5,600 train, 2,400 test) at 512×512 resolution generated through a physically-based Blender rendering pipeline with Nishita atmospheric sky models. Images are procedurally generated — each scene is uniquely rendered with randomized terrain, shadow-casting objects (buildings, trees, rocks), and atmospheric conditions. Sun elevation is constrained to 8–55° to ensure visible shadows across all samples. The only variables preserved across images are the physically accurate sun position and the ground-truth GPS coordinate assigned to that sun position.
> Data Generation
> Images are produced by a procedural rendering pipeline. For each scene, a GPS coordinate and UTC hour are sampled, and the corresponding sun position (elevation and azimuth) is computed from first-principles solar geometry using the day of year. The scene is then drawn with the sun placed at the correct angular position and shadows cast in the correct direction. Deliberate noise is injected into sun placement, shadow angle, and atmospheric appearance — this prevents extracting sun position analytically from image pixels and forces models to learn solar geometry implicitly.
> Key Design Decisions
> Day of year (doy) is provided in both train.csv and test.csv. Without it, the inverse-sun-position problem is underdetermined. In any real-world scenario, the date a photo was taken is known.
> Scene-level metadata is stripped: internal parameters such as sun elevation, sun azimuth, and scene type are not included in any public file. The model must infer them from the image alone.
> Train and test sets are disjoint — no location or image appears in both splits.
> Public Files
> **train.csv** — Training labels (5,600 rows)
> image_id (str) — Filename without extension, e.g. scene_000001, maps to train/scene_000001.png
> latitude (float) — GPS latitude in decimal degrees, range [-90, 90]
> longitude (float) — GPS longitude in decimal degrees, range [-180, 180]
> hour (float) — UTC hour of capture, range [0, 24)
> doy (int) — Day of year the photo was taken, range [1, 365]
> **test.csv** — Test file list (2,400 rows)
> image_id (str) — Filename without extension, maps to test/{image_id}.png
> doy (int) — Day of year the photo was taken, range [1, 365]
> **sample_submission.csv** — Submission template (2,400 rows)
> image_id (str) — Filename from test/
> latitude (float) — Placeholder value 0.0, range [-90, 90]
> longitude (float) — Placeholder value 0.0, range [-180, 180]
> hour (float) — Placeholder value 12.0, range [0, 24)
> All placeholder values are neutral — they carry no information about the test set answers.
> Image Properties
> Resolution: 512×512 pixels, RGB
> Format: PNG
> Scene types: urban, rural, desert, forest, coastal (randomly assigned, not correlated with image_id or any public feature)
> Sun elevation range: 8–55° (constrained to ensure visible shadows; sun never directly overhead)
> Content: outdoor scenes with physically accurate Nishita sky, procedural terrain, 3D objects (buildings, trees, rocks, poles, cacti), and ray-traced cast shadows. Shadow geometry is the primary predictive signal.
> Submission
> Submit a CSV file with the following columns:
> image_id (str) — Filename from test/
> latitude (float) — Predicted latitude in [-90, 90]
> longitude (float) — Predicted longitude in [-180, 180]
> hour (float) — Predicted UTC hour in [0, 24)
> Example (first 3 rows):
> image_id,latitude,longitude,hour
> scene_000255,48.8566,2.3522,14.5
> scene_000413,-33.8688,151.2093,8.2
> scene_000005,35.6762,139.6503,19.0
> ...
> (2,400 rows total)
> Requirements:
> Must contain exactly 2,400 rows (one per test sample)
> Include header row with exact column names: image_id, latitude, longitude, hour
> Latitude: float in [-90, 90]
> Longitude: float in [-180, 180]
> Hour: float in [0, 24)
> A sample_submission.csv with neutral placeholders (0.0, 0.0, 12.0) is provided in the public dataset
> Rules & Constraints
> Allowed
> Base models: Any architecture up to 13B parameters. Pre-trained weights allowed (ImageNet, etc.) but no models pre-trained specifically on geolocation tasks.
> Fine-tuning: LoRA, QLoRA, full fine-tuning, or training from scratch.
> Training data: ONLY the provided training set. No external images, GPS databases, elevation maps, or astronomical data.
> Ensembles: Model ensembles are allowed. No restriction on combining predictions from multiple independently trained models.
> Libraries: Any open-source ML/vision library (PyTorch, TensorFlow, OpenCV for basic image I/O only).
> NOT Allowed
> Physics-based solvers: ABSOLUTELY NO direct computation of sun position equations, shadow geometry formulas, or any analytical trigonometry to solve for coordinates. The model must learn solar geometry IMPLICITLY from training data. This includes:
> No sun elevation/azimuth extraction from image pixels
> No shadow angle measurement with image processing
> No analytical solution of the sun-position equations
> No hard-coded astronomical formulas or ephemeris data
> External knowledge bases: No Wikipedia, astronomical tables, sun position calculators, GIS databases, or elevation maps.
> Closed-source / commercial APIs: No GPT-4, Claude, Gemini, or any LLM API (local or cloud).
> Human-written rules: No regex, hard-coded rules, or manual feature engineering for sun/shadow detection.
> Data leak exploitation: Must not exploit any known data generation patterns. If you discover a leak, report it — don't exploit it.

Inspiration note: Useful because it turns visual shadow geometry, hidden geolocation, and cyclic time estimation into a single metric-driven benchmark with a built-in identifiability trap.

Important challenge takeaway:

> The important part is the identifiability tension: UTC hour is entangled with longitude and local solar time, so the task is not just shadow-time prediction. A strong model must infer latent geography from image cues, then combine that with solar geometry and day/time constraints; otherwise it collapses to the constant-hour leaderboard ceiling.

Research-paper angle:

> This can support a research paper only if expanded beyond the discussion into experiments: establish constant, metadata-only, image-only, geolocation-first, and physics-aware baselines; measure the UTC-vs-local-solar-time label issue; analyze error decomposition for latitude, longitude, and hour; and show whether images actually add information beyond shortcut priors.

User-provided Discord review / creator discussion:

> oguricapu ? 7/4/26, 9:10 PM
> Yo @Principal Reviewers  I think something might be wrong with this challenge: https://shipd.ai/quests/eris/challenges/jx70wnk1p7139nvg52sj0ght6188w7c0?tab=all
>
> From what I can tell, the labels are UTC hour plus GPS coordinates spread all over the world. That makes the hour target basically tied to longitude (UTC ? local solar time - lon/15). From the image alone, I don't see how you could recover UTC hour, especially since camera orientation is random.
>
> I checked the data on my end, and the image doesn't seem to add any useful information for predicting the hour. Predicting a constant value around 13.0 gets almost everything you're going to get for that target. The hour score tops out around 0.43, which puts the overall challenge ceiling at roughly 0.237.
>
> The weird part is that the AI baseline is 0.2399, while the challenge description says 0.70+ should be achievable. After 17 submissions, the best human score is 0.2393, which is basically the same. It feels like everyone's just bumping into the same limit.
>
> Was the label supposed to be local solar time instead of UTC? That would actually be something a vision model could learn. Right now it seems like the task itself may have an issue.
> haidang ? 7/4/26, 9:45 PM
> heloo, i created that challenge, i'll answer questions you have about this challenge.
> about : hour-longitude coupling & synthetic data concerns
> On the hour-longitude degeneracy
> you're mathematically correct that hour_angle = (hour-12)?15 + lon couples hour and longitude. But this isn't a bug - it's the core reason this challenge requires ML rather than a physics formula.
> regarding the question: 'why is this bright, sunny picture timestamped at 19:51?
> because 19:51 UTC is 3:00 PM local time at this location (~68?E). The sun IS up. The UTC label forces you to figure out WHERE on Earth this is - because without the location, you can't make sense of the hour. That's the whole point of the challenge.
> the degeneracy means you can't "solve" for UTC hour deterministically. But ML models don't solve equations - they learn conditional distributions P(hour | image_features, doy). Here's why the image DOES contain hour-relevant signal:
> shadow length/sharpness correlates with sun elevation, which constrains the (hour, lat, doy) combination
> terrain type + vegetation constrain latitude -> narrowing the possible (lat, hour) pairs
> architectural style, road markings, driving side - all provide geographic priors
> 20% of images share locations at different hours -> models can learn temporal shadow patterns at fixed positions
> a quick experiment: using only lat+lon+doy (no image at all), a Random Forest predicts hour with 2.07h mean error -> time_score = 0.59. That beats the constant - hour baseline (0.43) by a wide margin. a CV model that can extract lat/lon from visual features can do even better.
> On the 0.70+ baseline
> this was stated as achievable by a "physics-aware model (implicit sun geometry)." Let me clarify what that means:
> Perfect geo + constant hour=13.03 -> score = 0.716 - the 0.70 ceiling IS mathematically reachable
> But it requires near-perfect geo prediction (~10-50 km error), which is genuinely hard
> the fact that 17 submissions all cluster around 0.24 doesn't mean the challenge is broken - it means nobody has solved it yet. That's the point of a challenge.
> On synthetic data
> This is the most important design decision
> Real outdoor photos cannot provide ground-truth solar geometry. In a real photo:
> You don't know the true height of shadow-casting objects -> can't compute true sun elevation from shadow length
> Camera intrinsics (focal length, sensor size, lens distortion) are unknown -> can't measure shadow angles precisely
> GPS EXIF is often inaccurate by 10-50m, sometimes wrong by kilometers
> Timestamps may be in local time, camera time, or UTC - inconsistent across datasets
> Weather, season, atmospheric conditions are uncontrolled confounders
> Blender gives me something no real dataset can: a controlled physics laboratory where we KNOW the sun was exactly at elevation 34.7? and azimuth 218.3? for every pixel. i can inject controlled noise (?8px jitter, ?5? shadow perturbation, 30% cloud occlusion) to prevent analytical solving while preserving the learnable signal.
> bottom line: The degeneracy you identified is real, but it's a feature - it's what makes this a machine learning challenge rather than a trigonometry problem. The 0.24 leaderboard proves the challenge is genuinely unsolved.
> I want someone to break through that ceiling - that's where the interesting research happens
> if you have any questions about the challenge, feel free to ask me.

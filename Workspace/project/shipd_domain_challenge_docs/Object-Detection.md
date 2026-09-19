# Object Detection Challenge Examples

Scrape timestamp: 2026-07-02T00:00:00+05:30

Confirmed examples in this document: 4

These entries are included because the challenge detail page displayed this domain. Titles were not used for classification.

## SkyPatch-1080: UAV Small-Object Person Detection
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74fx5f1dzg7c89ctezvtsmph89qn10
- DOMAIN exactly as displayed: Object Detection
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, large-scale
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-03; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> SkyPatch-1080 is a single-class, multi-instance object-detection benchmark for UAV nadir imagery. Frames were captured by unmanned aerial vehicles during campus-scale patrol flights and civil-defense exercise monitoring. Footage uses a fixed 1920×1080 RGB raster at nadir-like viewing angles, so pedestrians appear as tiny footprints on pavement and open ground — often under 32×32 pixels per box.
> Unlike ground-level roadside localization tasks (handheld mobile cameras, one primary vehicle per frame, normalized box coordinates), SkyPatch-1080 evaluates dense multi-person recall from a fixed aerial raster: up to 66 labeled people per frame, 43,175 training boxes across 2,379 images, and 757 held-out test images from separate flight families. Predict every person in each test frame as axis-aligned boxes with confidence scores.
> Scientific Gaps & Technical Delta
> Canonical aerial detection literature — including TinyPerson (Scale Match for Tiny Person Detection, WACV 2020) and the Tiny Object Detection (TOD) Challenge (AP50_tiny metrics) — established top-view tiny-person detection with mixed-scale or video-centric evaluation. Broader multi-class drone surveillance corpora and aerial pedestrian video surveys extended detection to heterogeneous UAV platforms. SkyPatch-1080 recomposes these ideas into a competition bundle with three structural deltas prior benchmarks do not jointly enforce:
> Fixed-raster small-footprint gating: All frames share a 1920×1080 canvas (not variable-resolution tiling). About 90% of training person boxes have area below 32×32 pixels. Models cannot rely on resolution jitter or crop-scale heuristics alone; they must localize sub-thirty-two-pixel footprints on a uniform HD grid.
> Flight-family generalization split: Public UAV corpora often random-split frames within the same flight sequence, leaking temporal background and altitude cues. SkyPatch-1080 holds out three entire capture families (of twelve) for test. Generalization is measured across unseen flight sessions, not unseen frames from familiar trajectories.
> Per-image macro mAP@0.5 under zero-context telemetry: Evaluation macro-averages average precision at IoU 0.5 per test image, then across images — so a single crowded frame with missed tiny instances is penalized equally to a sparse frame. Combined with MD5-salted image_id filenames, this blocks filename-based label recovery and prevents aggregate mAP from hiding catastrophic per-scene recall collapse.
> What this is not
> Not a multi-class drone surveillance benchmark: single class (people) only, not ten-class aerial DET corpora.
> Not a ground-level traffic localization + classification task: no vehicle taxonomy, no normalized [0,1] single-target boxes, no roadside mobile-camera viewpoint.
> Not a video tracking or re-identification challenge: each JPEG is scored independently; no track IDs or temporal continuity are provided.
> The Dataset
> Collection and recording conditions
> Platform: consumer/prosumer UAV platforms at low-to-medium altitude over open campus and drill-scene areas.
> View: predominantly top-down / oblique nadir views over crowds and sparse groups.
> Raster: 1920×1080 RGB JPEG, consistent across all frames.
> Labels: axis-aligned person boxes in absolute pixel coordinates on that canvas.
> Scale: about 90% of training person boxes have area below 32×32 pixels; training frames contain a median of 10 people and a maximum of 66 people per image.
> Competition split: 12 aerial capture families in the source pool; 3 entire families are held out for test (flight-family split, not random frames).
> File listing
> public/train/ — 2,379 training JPEG images ({image_id}.jpg).
> public/train_boxes.csv — labeled person boxes for training images (43,175 rows).
> public/test/ — 757 test JPEG images (labels hidden).
> public/test_images.csv — authoritative list of test image_id values (757 rows).
> public/sample_submission.csv — one-row-per-image degenerate submission template.
> train_boxes.csv columns (training labels only)
> **image_id** (string) — 14-character hashed id matching train/{image_id}.jpg.
> **xmin** (float) — Left edge in pixels (0–1920).
> **ymin** (float) — Top edge in pixels (0–1080).
> **xmax** (float) — Right edge in pixels (0–1920).
> **ymax** (float) — Bottom edge in pixels (0–1080).
> **class_name** (string) — Always people. Training file only — do not include this column in submissions.
> test_images.csv columns (test index only)
> **image_id** (string) — One row per test image; every id in this file must receive predictions. No box columns are provided.
> sample_submission.csv columns (submission template)
> **image_id** (string) — Matches test_images.csv.
> **xmin, ymin, xmax, ymax** (float) — Pixel box coordinates (degenerate 1×1 px placeholder boxes in the template).
> **score** (float) — Detection confidence placeholder (template uses 0.01).
> This file demonstrates the submission schema. Your real submission should include all predicted boxes, with multiple rows per image_id when needed.
> Evaluation Metric
> Submissions are scored with mean Average Precision at IoU 0.5 (mAP@0.5), macro-averaged across test images. Higher is better.
> For each test image:
> Sort predicted boxes by descending score.
> Greedily match predictions to unmatched ground-truth boxes at IoU ≥ 0.5.
> Compute average precision from the precision–recall curve for that image.
> Average per-image AP equally over all 757 test images.
> Images with no predictions receive AP = 0 when ground-truth boxes exist. Predictions for unknown image_id values are ignored.
> This per-image macro formulation differs from corpus-level COCO mAP or TinyPerson AP50_tiny pooling, which can overweight frequent large instances or dominant scene types.
> Submission Format
> Submit a CSV with one row per predicted box (multiple rows per image_id are expected).
> image_id,xmin,ymin,xmax,ymax,score
> a91f02bc13d8e7,412.5,318.0,425.0,332.0,0.93
> a91f02bc13d8e7,1020.0,540.0,1035.0,558.0,0.87
> c44b19aa02f1de,12.0,48.0,28.0,65.0,0.71
> Submission columns (no class_name)
> **image_id** (string) — Must match an id from test_images.csv.
> **xmin, ymin, xmax, ymax** (float) — Pixel coordinates on the 1920×1080 canvas.
> **score** (float) — Confidence in [0, 1].
> Requirements
> Cover every image_id listed in test_images.csv (predict zero boxes by omitting rows for that image, or emit low-confidence boxes).
> Multiple boxes per image are allowed and expected in crowded frames.
> Include a header row.
> What Not To Use
> Reverse image lookup. Do not match test frames against public video portals, image search engines, or third-party aerial archives using pixels or metadata.
> Filename or registry recovery. Hashed image_id values are opaque; do not map them back to external catalog filenames or mirror repositories.
> Mirror split label recovery. Do not scrape public leaderboard archives or upstream annotation mirrors to reconstruct private test boxes.
> Grader or filesystem exploitation. Predictions must come from a detector trained on the released training images and boxes.

Inspiration note: Useful because it stresses small-object localization, dense multi-instance outputs, and a metric that rewards per-image recall rather than easy aggregate wins.

## Multimodal Wildlife Localization
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77sqgckp2yqn3sqkj91g33bx89wh9g
- DOMAIN exactly as displayed: Object Detection
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↓ Lower is better
- Tags: Not shown/captured
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Locate the animal in each paired RGB and thermal aerial wildlife crop. Each test row corresponds to one real AWIR crop containing a single cow, deer, or horse after deterministic crop/resize/flip preprocessing. Predict a normalized bounding box around the visible animal using the provided public training boxes and the paired image arrays.
> The challenge is designed for CPU-feasible computer vision and multimodal feature extraction. The RGB crop contains texture and shape cues, while the thermal crop often helps separate the animal from grass, soil, and shadows.
> Dataset
> File descriptions:
> dataset/public/train.csv: Training IDs, array indices, species labels, and normalized bounding boxes.
> dataset/public/test.csv: Test IDs and array indices. Bounding boxes are hidden.
> dataset/public/train/images.npz: Training image arrays with keys rgb and thermal; arrays are aligned to array_index in train.csv.
> dataset/public/test/images.npz: Test image arrays with keys rgb and thermal; arrays are aligned to array_index in test.csv.
> dataset/public/sample_submission.csv: A valid random submission in the required format.
> Column descriptions:
> id: Hashed example identifier.
> array_index: Row position in the matching NPZ arrays.
> class_label: Animal class for public training examples only.
> x_min: Left edge of the bounding box, normalized from 0 to 1.
> y_min: Top edge of the bounding box, normalized from 0 to 1.
> x_max: Right edge of the bounding box, normalized from 0 to 1.
> y_max: Bottom edge of the bounding box, normalized from 0 to 1.
> Evaluation
> Submissions are scored with composite bounding-box localization loss. Lower is better.
> intersection = area(predicted_box & true_box)
> union = area(predicted_box | true_box)
> iou = intersection / union
> coord_mae = mean(abs(predicted_coords - true_coords))
> row_loss = 100  *(0.65*  (1 - iou) + 0.35 * coord_mae)
> score = mean(row_loss)
> Invalid submissions are rejected. Coordinates must be finite normalized values between 0 and 1, and every row must satisfy x_min < x_max and y_min < y_max.
> Submission
> Submission columns:
> id: Test example identifier.
> x_min: Predicted normalized left edge.
> y_min: Predicted normalized top edge.
> x_max: Predicted normalized right edge.
> y_max: Predicted normalized bottom edge.
> Example:
> id,x_min,y_min,x_max,y_max
> AWIR_f4295657b38f,0.1200,0.1800,0.7300,0.6900
> Requirements:
> Submit exactly one row for every test ID.
> Use the same IDs as dataset/public/test.csv.
> Do not use external AWIR source metadata, original image filenames, or private labels.
> Write predictions to ./working/submission.csv.

Inspiration note: Useful because it pairs visual inputs with bounded localization outputs and an IoU/coordinate-sensitive metric.

## Tax Form Field Localization
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70p79jax7k88df1wt8vzvmd18a111c
- DOMAIN exactly as displayed: Object Detection
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↓ Lower is better
- Tags: image
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-08; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Document automation systems often need to locate the writable field that corresponds to a form line before OCR, validation, or downstream extraction can work reliably. In this challenge, each example is a real crop from an official fillable tax form. Your task is to predict the normalized bounding box of the primary right-column text-entry field in the crop.
> The public data contains anonymous crop IDs and RGB image arrays. The crops preserve local form rules, gray fills, and writable-field boundaries near the target while suppressing most isolated printed text strokes and most page-layout geometry outside the target neighborhood. Each crop also receives a per-sample geometric deidentification transform, and target boxes are measured after that transform. Source PDF filenames, page numbers, widget names, crop offsets, transform parameters, and private coordinates are not included in the test set.
> Dataset
> File descriptions
> train.csv -- Training crop IDs, image array indices, and target bounding boxes.
> test.csv -- Test crop IDs and image array indices without target boxes.
> train/images.npz -- RGB training images with key images; rows align to array_index in train.csv.
> test/images.npz -- RGB test images with key images; rows align to array_index in test.csv.
> sample_submission.csv -- A valid random submission with one normalized box per test ID.
> Column descriptions
> id (string) -- Anonymous crop identifier.
> array_index (integer) -- Row index in the matching images.npz array.
> x_min (float) -- Left edge of the target field box, normalized from 0 to 1.
> y_min (float) -- Top edge of the target field box, normalized from 0 to 1.
> x_max (float) -- Right edge of the target field box, normalized from 0 to 1.
> y_max (float) -- Bottom edge of the target field box, normalized from 0 to 1.
> Evaluation
> Submissions are scored with mean Complete-IoU localization loss. Lower is better. The score is non-negative and has no finite configured upper bound.
> For each row, let the predicted box be (px_min, py_min, px_max, py_max) and the true box be (tx_min, ty_min, tx_max, ty_max).
> intersection_width = max(0, min(px_max, tx_max) - max(px_min, tx_min))
> intersection_height = max(0, min(py_max, ty_max) - max(py_min, ty_min))
> intersection_area = intersection_width * intersection_height
> pred_area = (px_max - px_min) * (py_max - py_min)
> true_area = (tx_max - tx_min) * (ty_max - ty_min)
> union_area = pred_area + true_area - intersection_area
> iou = intersection_area / max(union_area, 1e-12)
> pred_center = ((px_min + px_max) / 2, (py_min + py_max) / 2)
> true_center = ((tx_min + tx_max) / 2, (ty_min + ty_max) / 2)
> center_distance = (pred_center_x - true_center_x)  **2 + (pred_center_y - true_center_y)**  2
> cover_width = max(px_max, tx_max) - min(px_min, tx_min)
> cover_height = max(py_max, ty_max) - min(py_min, ty_min)
> cover_diagonal_squared = cover_width  **2 + cover_height**  2
> center_penalty = center_distance / max(cover_diagonal_squared, 1e-12)
> pred_width = max(px_max - px_min, 1e-12)
> pred_height = max(py_max - py_min, 1e-12)
> true_width = max(tx_max - tx_min, 1e-12)
> true_height = max(ty_max - ty_min, 1e-12)
> v = (4 / pi ** 2)  *(atan(true_width / true_height) - atan(pred_width / pred_height))* * 2
> alpha = v / max(1 - iou + v, 1e-12)
> shape_penalty = alpha * v
> row_loss = 100 * (1 - iou + center_penalty + shape_penalty)
> score = mean(row_loss)
> Here atan is arctangent in radians and pi is the mathematical constant. This is the same formula implemented in grade.py.
> Invalid submissions are rejected. Coordinates must be finite normalized values between 0 and 1, and every row must satisfy x_min < x_max and y_min < y_max.
> Submission
> Submit a CSV file with one predicted box for every row in test.csv.
> id (string) -- The anonymous crop identifier from test.csv.
> x_min (float) -- Predicted normalized left edge.
> y_min (float) -- Predicted normalized top edge.
> x_max (float) -- Predicted normalized right edge.
> y_max (float) -- Predicted normalized bottom edge.
> Example:
> id,x_min,y_min,x_max,y_max
> TFL_00216595d4d7,0.31,0.42,0.70,0.49
> TFL_0037dd0cb6dc,0.55,0.18,0.83,0.25
> Requirements
> The file must contain exactly one row for every test ID.
> Every id from test.csv must be present exactly once.
> Coordinates must be normalized to the 256 by 256 crop dimensions.
> File format: .csv only, with exact column names id,x_min,y_min,x_max,y_max.
> What Not To Use
> Do not use external copies of the source PDFs, widget metadata, source filenames, page numbers, or form-field manifests to recover hidden test boxes.
> Do not infer boxes from row order or hashed IDs; those fields are deterministic handles for grouping and grading only.

Inspiration note: Useful because it pairs real document/image inputs with bounded localization outputs and a coordinate-sensitive metric.

## Occlusion-Aware Cattle Detection in Aerial Drone Imagery
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx785jk5t50qcdmgqrtevdqcbh89zc5a
- DOMAIN exactly as displayed: Object Detection
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-08; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> When animals graze in groups, an overhead drone sees them overlapping and partially hiding one another — one cow's body is clipped by another, by a fence, or by vegetation. Knowing which detections are occluded is operationally important (occluded animals are miscounted, mis-measured, and mis-tracked), and it is exactly what a plain bounding-box detector throws away.
> This challenge asks for more than boxes. For every cow in an aerial image you must predict its bounding box and whether it is occluded (partially hidden) or fully visible — and a detection only counts if it gets both right. The occlusion label is part of every match, so getting it right adds to the score on top of good localisation; the task rewards reasoning about inter-animal occlusion in cluttered herds, not just finding cows.
> The images are large (thousands of pixels), cows are tiny (~30–50 px), many images contain no animals at all, and the test images come from a shifted setting — so strong localisation is necessary but not sufficient.
> Data
> train_images/ — training images (JPEG), including cow-free negatives.
> train.csv — tid,width,height for every training image (tid = training image id; the file is train_images/<tid>.jpg).
> train_labels.csv — the gold cows, one row per cow: tid,xmin,ymin,xmax,ymax,occluded, where occluded ∈ {0,1} (1 = the cow is partially hidden by another animal / object). Images with no rows contain no cows.
> test_images/ — the images to run on, named <item_id>.jpg.
> test.csv — item_id,width,height for every test image.
> sample_submission.csv — a valid submission with a dummy baseline.
> There is a single object class (cow) with a per-instance occlusion attribute.
> Task
> For every test image, predict a set of cows: each a bounding box, an occluded flag (0/1), and a confidence score. Some test images contain no cows.
> Evaluation
> Occlusion-conditioned Average Precision at IoU ≥ 0.5. A predicted cow is a true positive only if it overlaps an unmatched gold cow with IoU ≥ 0.5 AND its predicted occluded flag equals that gold cow's occlusion state. Each gold cow can be matched at most once; unmatched predictions (wrong location or wrong occlusion label) are false positives. Detections are ranked globally by score to trace the precision–recall curve. Higher is better, in [0, 1]. Only the top 100 highest-scoring boxes per image are scored.
> Because the occlusion label is part of every true-positive match, a detector that labels every cow "visible" forfeits the credit for the cows that are actually occluded. Reading occlusion correctly therefore contributes directly to the score, on top of localisation.
> Submission format
> A CSV with exactly these columns, one row per predicted cow:
> item_id,xmin,ymin,xmax,ymax,occluded,score
> cow_ade4e7d4c26e,1204.5,880.1,1243.0,930.7,0,0.91
> cow_ade4e7d4c26e,512.0,300.4,548.9,349.2,1,0.77
> item_id — a test image id from test.csv (only known ids allowed).
> xmin,ymin,xmax,ymax — box in pixels, in-frame (0 ≤ xmin < xmax ≤ width, likewise y).
> occluded — 0 (visible) or 1 (occluded).
> score — confidence in [0, 1].
> Images with no predicted cows have no rows. Do not invent boxes for empty images.
> Requirements (violations rejected as invalid): exactly the columns above; no nulls; numeric coords/score; occluded in {0,1}; boxes in-frame and non-degenerate; no unknown item_id; at most 1000 boxes per image.
> What Not To Use
> No runtime installs or downloads — no pip/conda/apt installs and no fetching or vendoring extra packages, code, or model files; use only what is in the runtime.
> No external data or network access — no extra detection datasets, cattle/aerial-animal detection heads, or external occlusion labels, and no downloads over the network. ImageNet/COCO backbones are fine.
> No remote or dynamic models — no hosted inference APIs, gated checkpoints, trust_remote_code=True, torch.hub.load(), or passing a challenge-specific fine-tuned checkpoint off as "pretrained".
> No identifying or retrieving the source imagery / its annotations, and no use of any answer/label file.

Inspiration note: Useful because it pairs real image inputs with bounded localization outputs and a coordinate-sensitive metric.

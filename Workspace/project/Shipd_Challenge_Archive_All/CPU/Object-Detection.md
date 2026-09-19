# CPU Object Detection Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed CPU examples in this document: 11

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.

## Robot Workcell Inventory Evidence

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76m6p9zb0x4fhge3n2tdd7r58atkqs
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Beat jojo_rabbit's score of 0.666!

Full challenge description from page:

> Robot Workcell Inventory Evidence
> Overview
> An automated laboratory workcell must verify inventory before a robot continues a manipulation step. Each inspection names one queried object. From the image, classify the visible inventory state as absent, single, pair, or group, then return one compact crop covering the visual evidence for that count.
> This is more than generic scene classification. The same workcell image can be queried for different objects, small instances can be partly occluded, and camera geometry changes across the held-out set. A useful model must condition visual detection/counting on the object query and show where it found the evidence. For an absent query, the crop should identify the relevant empty search area rather than the full frame.
> The task models a practical inventory gate: an incorrect count can make a robot grasp an empty location, miss a required pair, or continue while extra items obstruct the work area. The evidence crop lets an operator verify the decision quickly.
> Dataset
> File descriptions
> train.csv — 2,388 labeled inventory inspections with image paths, opaque scene groups, object queries, inventory states, and normalized evidence crops.
> test.csv — 400 inventory inspections with the same inputs but without the five target fields.
> sample_submission.csv — A valid randomly populated submission with the required six columns.
> train/ — Lossy, record-specific JPEG views referenced by train.csv.
> test/ — Lossy, record-specific JPEG views referenced by test.csv.
> Column descriptions
> id (string) — Unique 12-character hexadecimal inspection identifier.
> image_path (string) — Path relative to ./dataset/public/ for the inspection image.
> scene_group (string) — Opaque key grouping rows created from the same physical camera capture. Keep this key intact when constructing validation folds; it is not a predictive feature.
> query_object (string) — Object whose visible inventory must be counted and grounded.
> inventory_state (string) — Target state (train only): absent for zero visible matching instances, single for one, pair for two, or group for three or more.
> x_min (float) — Normalized left edge of the evidence crop in [0, 1] (train only).
> y_min (float) — Normalized top edge of the evidence crop in [0, 1] (train only).
> x_max (float) — Normalized right edge of the evidence crop in [0, 1] (train only).
> y_max (float) — Normalized bottom edge of the evidence crop in [0, 1] (train only).
> For present states, the evidence crop encloses all visible instances matching query_object. For absent, it encloses the relevant empty search area. Open an image with ./dataset/public/ joined to image_path; image coordinates use the upper-left origin.
> Evaluation
> Submissions are scored with the Inventory-Grounded Score. Higher is better.
> For each row, crop overlap is measured by box Dice:
> [
> D_i = \frac{2,|B_i \cap \hat{B}_i|}{|B_i| + |\hat{B}_i|}.
> ]
> The final score is:
> [
> 0.55,F1_{macro}(inventory_state) + 0.45,mean(D_i).
> ]
> Macro-F1 weights all four inventory states equally. Box Dice rewards crops that cover the complete queried evidence while penalizing unnecessarily broad regions. The score is bounded in [0, 1].
> def inventory_grounded_score(state_true, state_pred, boxes_true, boxes_pred):
> state_f1 = f1_score(state_true, state_pred, average="macro")
> intersection = box_intersection_area(boxes_true, boxes_pred)
> dice = 2 * intersection / (box_area(boxes_true) + box_area(boxes_pred))
> return 0.55  *state_f1 + 0.45*  dice.mean()
> Submission
> Submit one CSV row for every inspection in test.csv.
> id (string) — Exact identifier from test.csv.
> inventory_state (string) — One of absent, single, pair, or group.
> x_min (float) — Left crop coordinate in [0, 1].
> y_min (float) — Top crop coordinate in [0, 1].
> x_max (float) — Right crop coordinate in [0, 1] and strictly greater than x_min.
> y_max (float) — Bottom crop coordinate in [0, 1] and strictly greater than y_min.
> Example using real test IDs:
> id,inventory_state,x_min,y_min,x_max,y_max
> 01382db66e16,pair,0.180000,0.244000,0.710000,0.812000
> 01ed0d6825b6,absent,0.225000,0.196000,0.786000,0.844000
> 01eec4a692d7,group,0.108000,0.308000,0.902000,0.930000
> Requirements
> The file must contain exactly 400 data rows.
> Every id from test.csv must appear exactly once; no other IDs are allowed.
> Columns must appear exactly as id,inventory_state,x_min,y_min,x_max,y_max.
> Coordinates must be finite numbers in [0, 1] and define a positive-area crop.
> File format: CSV with a header row.
> What Not To Use
> Do not use reverse-image search or outside copies of these workcell images to recover counts or region boxes.
> Do not build filename, row-order, identifier, or scene-group lookup tables. The opaque keys are not inventory evidence.
> Do not submit a query-only system that never reads image_path; inventory state and location must be inferred from the supplied image.
> Do not split rows from one scene_group across training and validation folds.
> Do not use hardcoded query-to-count templates or exact-match caches in place of a trained visual model.

Inspiration note: Useful because it keeps the visual task concrete and measurable while tying detections to real operational evidence.

## RobotLink Watch: Multi-Panel Latency Incident Detection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7aqq3bjr0v4z6c70d0beqn898akad7
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat syncora's score of 0.336!

Full challenge description from page:

> RobotLink Watch: Multi-Panel Latency Incident Detection
> Overview
> Reliable remote-robot operation depends on recognizing communication failures before they degrade control, perception, or operator feedback.
> In this challenge, each sample is a 320 × 320 monitoring image containing three stacked telemetry panels. The panels are built from privacy-preserving composites of real networked-robot delay measurements. Controlled communication incidents are then introduced at unknown positions.
> Your task is to detect every controlled incident, identify its type, and localize it with a bounding box.
> The task is genuine multi-class object detection. An image may contain no labeled incidents or several incidents distributed across different panels.
> The benchmark labels only the controlled incidents added during dataset preparation. Naturally irregular background behavior is not automatically a labeled incident.
> Incident classes
> The class mapping is:
> 0 — level_shift: a temporary sustained upward or downward displacement of the local latency level.
> 1 — ramp_drift: a gradual directional change that develops over a continuous interval.
> 2 — jitter_burst: a sustained local increase in short-term variability.
> 3 — spike_cluster: a concentrated group of narrow latency impulses.
> The same image can contain multiple instances of the same class.
> Public data
> All public files are located under ./dataset/public/.
> train.csv
> Each row describes one labeled training image.
> Columns:
> sample_id — anonymized unique sample identifier.
> image_path — image path relative to ./dataset/public/.
> annotations — JSON list containing the ground-truth objects.
> Each training annotation contains exactly:
> {
> "class_id": 2,
> "xmin": 0.157791,
> "ymin": 0.674725,
> "xmax": 0.331764,
> "ymax": 0.962500
> }
> All coordinates are normalized to the full image:
> xmin and xmax are divided by image width.
> ymin and ymax are divided by image height.
> The valid coordinate range is [0, 1].
> Every box satisfies xmin < xmax and ymin < ymax.
> test.csv
> Columns:
> sample_id
> image_path
> The test file does not contain annotations.
> classes.json
> Maps each integer class_id to its class name.
> sample_submission.csv
> Provides every required test sample_id and an empty prediction list.
> Submission format
> Your script must write:
> ./working/submission.csv
> The submission must contain exactly these two columns:
> sample_id
> predictions
> Each predictions value must be a valid JSON list. Use [] when no incident is predicted.
> Each predicted object must contain exactly:
> {
> "class_id": 3,
> "confidence": 0.913,
> "xmin": 0.120,
> "ymin": 0.355,
> "xmax": 0.311,
> "ymax": 0.621
> }
> Submission requirements:
> class_id must be one of 0, 1, 2, or 3.
> confidence must be finite and within [0, 1].
> Every coordinate must be finite and within [0, 1].
> Every box must satisfy xmin < xmax and ymin < ymax.
> At most 100 detections may be submitted for one image.
> Every expected sample_id must appear exactly once.
> Missing, duplicate, and extra IDs are rejected.
> Unknown columns are rejected.
> Malformed JSON is rejected.
> Example CSV row:
> sample_id,predictions
> 4a32f9d0137b42a8ef,"[{""class_id"":3,""confidence"":0.913,""xmin"":0.120,""ymin"":0.355,""xmax"":0.311,""ymax"":0.621}]"
> Evaluation metric
> Submissions are scored using mean Average Precision over IoU thresholds from 0.50 through 0.95 in increments of 0.05.
> For each class and IoU threshold:
> Predictions are sorted by descending confidence.
> A prediction can match only a ground-truth box from the same image and class.
> Each ground-truth box can be matched at most once.
> A match is accepted when its Intersection over Union meets the active threshold.
> Average Precision is computed with 101 recall levels.
> The final score is the mean AP across all four classes and all ten IoU thresholds.
> Theoretical minimum: 0.0
> Theoretical maximum: 1.0
> Direction: higher is better
> Compute environment
> Hardware: CPU only
> Available CPU cores: 10
> Available memory: 62.5 GiB
> Maximum end-to-end runtime: 1.5 hours
> GPU and CUDA execution are prohibited
> The submitted solution must be one independent end-to-end Python script. It must perform preprocessing, model training or fine-tuning, test inference, and submission generation during the same run.
> What is allowed
> Training a genuine object-detection or visual-localization model during the submitted run.
> Fine-tuning general-purpose pretrained computer-vision backbones or detection weights available through preinstalled libraries such as torchvision, timm, or Hugging Face.
> Training a compact CNN, transformer, or detector from random initialization.
> Standard label-preserving image augmentations such as resizing, cropping that correctly updates boxes, brightness changes, blur, noise, and horizontal transformations that correctly update annotations.
> Per-image test-time augmentation when every test image is processed independently.
> Ensembling multiple genuinely trained models inside the same end-to-end script.
> Using hand-engineered visual features only as auxiliary inputs to a genuine trained vision model.
> Hyperparameter selection and calibration using only the released training data and training-only validation splits.
> What is not allowed
> GPU or CUDA use.
> External datasets or external labeled examples.
> Runtime installation through pip, conda, apt, GitHub, or downloaded custom code.
> Loading self-hosted, challenge-specific, or previously fine-tuned weights.
> An inference-only pipeline with no real training or fine-tuning during submission execution.
> Pure rule-based image processing, thresholding, template matching, or classical computer-vision logic as the complete solver.
> A tabular model trained directly on raw pixels or solely on hand-crafted image statistics without a genuine image model.
> Generating additional labeled incident images for training. Ordinary label-preserving augmentation is allowed.
> Looking up, identifying, downloading, or reconstructing the original telemetry recordings behind the prepared images.
> Using sample_id, file order, row order, filenames, or hidden source identity as predictive features.
> Pseudo-labeling, test-time adaptation, clustering, reweighting, calibration, or feature normalization that uses the overall test-set distribution.
> Cross-sample inference in which one test image affects the prediction for another test image.
> Private sharing of solution code or approaches between competing solvers.
> Validation guidance
> Training images are generated from source experiments that are disjoint from the experiments used for test images. Random image-level validation alone can therefore overestimate generalization.
> Use robust validation, conservative augmentation, and models that learn incident morphology rather than memorizing a particular panel background or rendering style.

Inspiration note: Useful because it keeps the visual task concrete and measurable while tying detections to real operational evidence.

## Work-Zone Safety Evidence Inventory Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7btshk3p31902nqca341zxm98ayvep
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: ?

Full challenge description from page:

> Each example is a 512 by 384 RGB image from a work-zone or safety-inspection scene. The task is to reconstruct an inspection-style evidence record from the image: every visible safety item or scene marker must be represented by its class, normalized box, coarse grid cell, size bin, and higher-level family. The same record also carries per-class and per-family count summaries, so the answer must be internally consistent rather than a loose list of boxes.
> The images include people, cones, helmets, gloves, masks, face shields, goggles, coveralls, and missing-safety-item markers in cluttered scenes with varied scale and lighting. A good solution must combine visual localization, object-type recognition, and record normalization: predicting a plausible object label is not enough unless the spatial cell, size bucket, family bucket, and count ledgers agree with the visible evidence.
> Dataset
> The provided files are:
> train.csv: 554 labeled examples.
> test.csv: 280 unlabeled examples.
> sample_submission.csv: valid low-information submission file with the required columns.
> images/: 834 JPEG images referenced by train.csv and test.csv.
> Columns in train.csv:
> id (string): unique example id.
> image_path (string): relative path to a JPEG image under images/.
> width (integer): image width in pixels. All rows use 512.
> height (integer): image height in pixels. All rows use 384.
> prompt (string): task instruction.
> answer_format_json (JSON string): output schema, class names, family names, grid shape, and size bins.
> answer_json (JSON string): ground-truth object inventory for training rows.
> Columns in test.csv:
> id (string): unique example id.
> image_path (string): relative path to a JPEG image under images/.
> width (integer): image width in pixels.
> height (integer): image height in pixels.
> prompt (string): task instruction.
> answer_format_json (JSON string): required output schema.
> The answer JSON object has exactly these fields:
> {
> "objects": [
> {"class": "Helmet", "family": "head_ppe", "bbox": [0.4210, 0.0833, 0.5330, 0.2115], "center_cell": "r01_c07", "size_bin": "small"}
> ],
> "object_count": 1,
> "class_counts": {"Cone": 0, "Coverall": 0, "Face_Shield": 0, "Gloves": 0, "Goggles": 0, "Head": 0, "Helmet": 1, "Mask": 0, "No_glasses": 0, "No_gloves": 0, "Person": 0},
> "family_counts": {"body_part": 0, "body_ppe": 0, "face_ppe": 0, "hand_ppe": 0, "head_ppe": 1, "missing_ppe": 0, "person": 0, "site_object": 0}
> }
> bbox is [x_min, y_min, x_max, y_max], normalized to [0, 1], with (0, 0) at the top-left image corner. center_cell is the object center on a 12 by 16 row-column grid, formatted like r01_c07. size_bin is one of small, medium, or large. objects must be sorted by class and then numeric bbox coordinates. Count fields must match the object list.
> Evaluation
> The score is the mean row score over all test rows. Each row score is clipped to [0, 1].
> Predicted objects are matched to unused true objects with the same class, using the highest object-pair score:
> object_pair_score = 0.74 * bbox_iou
> + 0.14 * center_cell_exact
> + 0.08 * size_bin_exact
> + 0.04 * family_exact
> bbox_iou is standard rectangle intersection-over-union. The exact-match terms are 1 when the submitted value matches the true value and 0 otherwise.
> The object-list score is F1-style:
> precision = sum(matched_object_pair_score) / number_of_predicted_objects
> recall    = sum(matched_object_pair_score) / number_of_true_objects
> object_score = 1 if both lists are empty
> object_score = 0 if exactly one list is empty
> object_score = 0 if precision + recall = 0
> object_score = 2 * precision * recall / (precision + recall) otherwise
> For a count dictionary:
> count_dict_score = 1 if predicted and true totals are both 0
> count_dict_score = max(0, 1 - sum_abs_count_error / (predicted_total + true_total)) otherwise
> For total object count:
> object_count_score = 1 if predicted_count = true_count
> object_count_score = max(0, 1 - |predicted_count - true_count| / max(1, true_count)) otherwise
> The row score is:
> row_score = 0.70 * object_score
> + 0.14 * class_count_score
> + 0.10 * family_count_score
> + 0.06 * object_count_score
> Malformed JSON, missing fields, extra fields, invalid value types, inconsistent counts, invalid boxes, invalid center cells, or more than 24 objects receive zero for that row. Submissions with the wrong columns, wrong column order, duplicate ids, missing ids, extra ids, or the wrong number of rows are rejected.
> Submission
> Submit a CSV file with exactly these two columns in this order:
> id (string): test row id.
> answer_json (JSON string): predicted object inventory record.
> Example:
> id,answer_json
> work_11111111111111,"{""objects"":[{""class"":""Helmet"",""family"":""head_ppe"",""bbox"":[0.42,0.08,0.53,0.21],""center_cell"":""r01_c07"",""size_bin"":""small""}],""object_count"":1,""class_counts"":{""Cone"":0,""Coverall"":0,""Face_Shield"":0,""Gloves"":0,""Goggles"":0,""Head"":0,""Helmet"":1,""Mask"":0,""No_glasses"":0,""No_gloves"":0,""Person"":0},""family_counts"":{""body_part"":0,""body_ppe"":0,""face_ppe"":0,""hand_ppe"":0,""head_ppe"":1,""missing_ppe"":0,""person"":0,""site_object"":0}}"
> work_22222222222222,"{""objects"":[{""class"":""Cone"",""family"":""site_object"",""bbox"":[0.20,0.44,0.31,0.91],""center_cell"":""r08_c04"",""size_bin"":""medium""}],""object_count"":1,""class_counts"":{""Cone"":1,""Coverall"":0,""Face_Shield"":0,""Gloves"":0,""Goggles"":0,""Head"":0,""Helmet"":0,""Mask"":0,""No_glasses"":0,""No_gloves"":0,""Person"":0},""family_counts"":{""body_part"":0,""body_ppe"":0,""face_ppe"":0,""hand_ppe"":0,""head_ppe"":0,""missing_ppe"":0,""person"":0,""site_object"":1}}"
> What Not To Use
> Do not use GPU acceleration.
> Do not bring in outside safety-gear, roadwork, compliance-inspection, object-detection, or segmentation datasets.
> Do not use pretrained detectors, pose models, mask models, vision-language models, or added checkpoint files.
> Do not call hosted vision services, remote APIs, runtime installers, torch.hub, or trust_remote_code loaders.
> Do not match test images to external pages, metadata, source archives, or annotation files.
> Do not maintain manual answer tables or hard-code object inventories for individual test ids.
> Use only the released public files when generating predictions.

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Historic Newspaper Visual Region Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7baeg5jdp3vesgnsv5xyrnx58ayygf
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Each example shows a scanned historical newspaper page. The task is to recover the visible non-text visual regions and page furniture that were marked by annotators: photographs, illustrations, maps, comics/cartoons, editorial cartoons, headlines, and advertisements. For every held-out page, submit a structured JSON object listing the annotated regions, their category, a normalized bounding box, a coarse page-grid cell, and a coarse area bin.
> This is a visual layout recovery problem. The images are page scans with dense typography, uneven print quality, and overlapping layout elements. The labels come from region-level page annotations; no labels are generated from model predictions.
> Dataset
> The public files are:
> train.csv: 1,300 labeled training rows.
> test.csv: 600 unlabeled test rows.
> sample_submission.csv: a valid low-information submission showing the required CSV and JSON shape.
> images/: transformed page images referenced by the CSV files.
> Columns in train.csv:
> id (string): row identifier.
> image (string): relative path to the page image.
> page_width (integer): image width in pixels. All rows use 512.
> page_height (integer): image height in pixels. All rows use 768.
> prompt (string): task instruction.
> answer_format_json (JSON string): output constraints, including image size, box scale, page grid size, category names, area bins, and maximum number of regions.
> answer_json (JSON string): target object for training rows.
> test.csv keeps the page image, dimensions, prompt, and schema fields for each page, but does not include answer_json.
> The expected answer_json object has:
> region_count (integer): number of submitted region records, from 0 to 20.
> category_counts (object): counts for all seven categories: photograph, illustration, map, comics_cartoon, editorial_cartoon, headline, and advertisement.
> dominant_category (string): the category with the largest count, tie-broken alphabetically; use none only when there are no regions.
> regions (list): region records in any order. Each record has:
> category (string): one of the seven allowed categories.
> box (list of four integers): [x0, y0, x1, y1], normalized to a 0-1000 coordinate scale, with x0 < x1 and y0 < y1.
> cell (string): center cell on the 12 by 8 page grid, formatted like r04_c03.
> area_bin (string): one of a0, a1, a2, a3, or a4, from smallest to largest.
> Example training target:
> {
> "region_count": 2,
> "category_counts": {
> "photograph": 1,
> "illustration": 0,
> "map": 0,
> "comics_cartoon": 0,
> "editorial_cartoon": 0,
> "headline": 1,
> "advertisement": 0
> },
> "dominant_category": "photograph",
> "regions": [
> {"category": "headline", "box": [62, 42, 948, 91], "cell": "r00_c04", "area_bin": "a1"},
> {"category": "photograph", "box": [290, 130, 690, 430], "cell": "r04_c03", "area_bin": "a3"}
> ]
> }
> Evaluation
> Each page receives a row score, and the final score is the average across test pages. Higher is better:
> row_score =
> 0.68 * region_f1
> + 0.14 * count_score
> + 0.12 * category_count_f1
> + 0.06 * dominant_category_score
> count_score = exp(-abs(predicted_region_count - true_region_count) / 4).
> category_count_f1 is standard F1 over category-count multisets. Let overlap = sum_c min(pred_count_c, true_count_c). Precision is overlap / sum_c pred_count_c, recall is overlap / sum_c true_count_c, and F1 is 2PR/(P+R). If both totals are zero, the score is 1. If exactly one total is zero, the score is 0.
> dominant_category_score is 1 if the submitted dominant_category exactly matches the hidden value, otherwise 0.
> region_f1 uses greedy one-to-one matching between submitted and hidden regions. A submitted region can match a hidden region only when the category is the same. For a possible pair:
> pair_score = 0.78 * IoU(box)^2 + 0.14 * cell_exact + 0.08 * area_bin_exact
> Pairs are sorted by pair_score from highest to lowest. The grader takes the highest remaining pair until no positive pair remains. Precision is sum(pair_score) / submitted_region_count, recall is sum(pair_score) / hidden_region_count, and region_f1 = 2PR/(P+R). If both lists are empty, region_f1 is 1. If exactly one list is empty, region_f1 is 0.
> Malformed JSON or a structurally invalid row scores 0 for that row. Wrong columns, extra columns, missing rows, duplicate ids, or ids that do not match the test set make the whole submission invalid.
> Submission
> Submit a CSV with exactly two columns:
> id (string): must match the ids in test.csv; row order is not used by the grader.
> answer_json (JSON string): predicted page-region inventory using the schema above.
> Example:
> id,answer_json
> newsreg_example_001,"{""region_count"":1,""category_counts"":{""photograph"":0,""illustration"":0,""map"":0,""comics_cartoon"":0,""editorial_cartoon"":0,""headline"":1,""advertisement"":0},""dominant_category"":""headline"",""regions"":[{""category"":""headline"",""box"":[80,70,920,120],""cell"":""r01_c04"",""area_bin"":""a1""}]}"
> newsreg_example_002,"{""region_count"":0,""category_counts"":{""photograph"":0,""illustration"":0,""map"":0,""comics_cartoon"":0,""editorial_cartoon"":0,""headline"":0,""advertisement"":0},""dominant_category"":""none"",""regions"":[]}"
> What Not To Use
> Do not use external image or annotation copies.
> Do not use web matching, reverse-image matching, OCR/text archive matching, page-title matching, or external metadata matching for test rows.
> Do not submit row-id lookup tables or memorized answers.
> Do not use GPU acceleration.
> Do not use pretrained object detectors or document-layout models trained on external layout datasets.
> Do not install packages at runtime, include additional model checkpoints, use non-public or gated assets, or load remote code such as torch.hub or trust_remote_code.

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Printing Element Provenance Detection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75nw7642c7b64qx2twjqyf298at54s
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Printing Element Provenance Detection
> Overview
> Historical ornaments were assembled from reusable printing elements. Repeated impressions of the same element can look different because of:
> Uneven inking pressure
> Paper texture
> Printing-block wear
> Scanning artifacts
> Blur
> Partial damage
> Missing ink
> Each challenge image is a newly rendered 320 × 320 contact sheet.
> The upper strip contains four reference elements in fixed left-to-right support slots:
> S0 | S1 | S2 | S3
> The lower region contains a composite ornament assembled from multiple independently rendered elements.
> Some elements in the lower composite descend from one of the four displayed supports. Other elements are unrelated distractors.
> A descendant can be:
> Directly reprinted
> Horizontally mirrored
> Rotated by 180°
> Partially fragmented
> Your task is to:
> Localize every support-descended element in the lower composite.
> Identify the support slot from which each detected element descends.
> Identify the transformation applied to the element.
> Assign a confidence score to every prediction.
> The support and query impressions are rendered independently. Exact pixel matching is therefore insufficient.
> The same underlying ornament element may differ between the support strip and lower composite because of:
> Contrast variation
> Blur
> Shape erosion
> Ink dropout
> Scale variation
> Paper appearance
> Local noise
> Printing degradation
> Provenance Classes
> Each detection uses a joint class identifier:
> class_id = support_slot × 4 + operation_id
> Operation identifiers
> 0 — DIRECT An independently rendered instance with unchanged orientation.
> 1 — MIRROR A horizontally mirrored instance.
> 2 — ROTATE An instance rotated by 180°.
> 3 — FRAGMENT A partial instance with a substantial region removed.
> Complete class mapping
> Class 0  = S0 + DIRECT
> Class 1  = S0 + MIRROR
> Class 2  = S0 + ROTATE
> Class 3  = S0 + FRAGMENT
> Class 4  = S1 + DIRECT
> Class 5  = S1 + MIRROR
> Class 6  = S1 + ROTATE
> Class 7  = S1 + FRAGMENT
> Class 8  = S2 + DIRECT
> Class 9  = S2 + MIRROR
> Class 10 = S2 + ROTATE
> Class 11 = S2 + FRAGMENT
> Class 12 = S3 + DIRECT
> Class 13 = S3 + MIRROR
> Class 14 = S3 + ROTATE
> Class 15 = S3 + FRAGMENT
> Support-slot semantics are episodic.
> S0 always means the leftmost support in the current image. It does not represent a permanent ornament category shared across different rows.
> Likewise, the visual meaning of every class from 0 through 15 changes from one sample to another according to the four support cards displayed in that image.
> Prepared Dataset
> The public dataset contains:
> train_images/
> test_images/
> train.csv
> test.csv
> schema.json
> sample_submission.csv
> train_images/
> Contains the generated training contact-sheet images.
> Every image has dimensions:
> 320 × 320 pixels
> test_images/
> Contains the generated test contact-sheet images.
> Test images do not include public annotations.
> train.csv
> The training metadata contains the following fields.
> sample_id
> Type: string
> Description: content-free identifier for the training sample
> Example:
> train_000127
> image_path
> Type: string
> Description: relative path to the corresponding contact-sheet image
> Example:
> train_images/train_000127.png
> annotations
> Type: JSON string
> Description: list of labeled target boxes in the image
> Example:
> [
> {
> "class_id": 6,
> "bbox": [121, 147, 38, 42]
> }
> ]
> The bbox field uses absolute COCO coordinates:
> [x, y, width, height]
> Where:
> x is the horizontal coordinate of the upper-left corner.
> y is the vertical coordinate of the upper-left corner.
> width is the box width in pixels.
> height is the box height in pixels.
> To convert a training box to corner coordinates:
> x1 = x
> y1 = y
> x2 = x + width
> y2 = y + height
> test.csv
> The test metadata contains the following fields.
> sample_id
> Type: string
> Description: content-free identifier for the test sample
> image_path
> Type: string
> Description: relative path to the corresponding test contact-sheet image
> The test file does not contain an annotations column.
> schema.json
> The schema file documents the exact challenge contract, including:
> Image width and height
> Support-slot count
> Operation mapping
> Joint class formula
> Valid class identifiers
> Submission column names
> Required prediction fields
> Maximum predictions per image
> Bounding-box coordinate rules
> Evaluation IoU thresholds
> Models should not infer the challenge contract from filenames or row positions. Use schema.json for authoritative structural information.
> sample_submission.csv
> The sample submission demonstrates the required CSV structure:
> sample_id,predictions
> Rows with no detections use:
> []
> The following are prohibited:
> Test-set adaptation
> Cross-row clustering
> Test-time pseudo-labeling
> Retrieval-index fitting on the test set
> Cross-test aggregation
> Public-source lookup
> Reconstruction through external ornament databases
> Using test filenames or row order as predictive signals
> Submission Format
> Submit a CSV file containing exactly these two columns:
> sample_id,predictions
> The column order must also match this format.
> sample_id
> Must exactly match one identifier from test.csv.
> predictions
> Must be a JSON list.
> Each prediction object must contain exactly the following fields:
> {
> "class_id": 6,
> "x1": 121.0,
> "y1": 147.0,
> "x2": 159.0,
> "y2": 189.0,
> "confidence": 0.87
> }
> Coordinates refer to the complete 320 × 320 contact-sheet image, including both the support strip and lower composite.
> However, valid target objects occur only in the lower composite region.
> Prediction requirements
> class_id:
> integer from 0 through 15
> confidence:
> finite numeric value from 0 through 1
> Bounding-box coordinates must satisfy:
> 0 ≤ x1 < x2 ≤ 320
> 0 ≤ y1 < y2 ≤ 320
> Each image may contain at most:
> 40 predictions
> Images with no predicted descendants must use:
> []
> Required ID coverage
> The submission must contain exactly one row for every sample_id in test.csv.
> The grader rejects submissions containing:
> Missing test IDs
> Duplicate IDs
> Unknown IDs
> Extra IDs
> Extra columns
> Missing columns
> Malformed JSON
> Non-list prediction values
> Missing prediction fields
> Extra prediction fields
> Invalid class identifiers
> Non-finite confidence values
> Confidence values outside [0,1]
> Invalid bounding boxes
> Boxes outside the image
> More than 40 predictions for one image
> Evaluation
> Submissions are evaluated using class-aware mean Average Precision.
> Average Precision is calculated independently for each of the 16 joint provenance classes at the following IoU thresholds:
> 0.25
> 0.50
> 0.75
> A prediction is counted as a true positive only when all of the following conditions are satisfied:
> Its class_id matches the target class.
> It belongs to the same image as the target.
> Its Intersection over Union meets or exceeds the current threshold.
> The target box has not already been matched to a higher-confidence prediction.
> Predictions are ranked globally by confidence within each class and IoU threshold.
> Matching is performed greedily.
> A target may be matched at most once.
> Additional predictions overlapping an already matched target are counted as false positives.
> Intersection over Union
> For a predicted box P and target box G:
> IoU(P, G) =
> area(P ∩ G) / area(P ∪ G)
> Final score
> Score =
> mean over 16 classes and 3 IoU thresholds
> of AP(class, threshold)
> Equivalently:
> Score =
> mean(
> AP(class_id, IoU threshold)
> for class_id in 0...15
> for IoU threshold in {0.25, 0.50, 0.75}
> )
> The final score is finite and bounded to:
> [0, 1]
> Higher scores are better.
> Classes without any private ground-truth objects are excluded from the mean for that evaluation split.
> False detections on images without descendants reduce precision naturally. There is no separate clean-image metric.
> Compute and Runtime Constraints
> Solutions must follow all of these requirements:
> CPU computation only
> Maximum runtime of 90 minutes
> Hardware limit of 10 CPU cores
> Memory limit of 62.5 GiB RAM
> No GPU or CUDA usage
> No internet access
> No hosted inference services
> No package installation at runtime
> No external datasets
> No external ornament databases
> No runtime model downloads
> Use only the prepared public dataset
> Use only libraries and model assets already available offline
> Process every test image independently
> Do not fit models, retrieval systems, thresholds, or calibration parameters on the test set
> Do not use sample_id, filenames, or row order as predictive features
> The final submission must be written to:
> ./working/submission.csv
> Recommended Modeling Directions
> This challenge rewards support-conditioned visual matching rather than persistent global-category memorization.
> Potential CPU-compatible approaches include:
> Shared support and query CNN encoders
> Dynamic similarity maps between support features and composite features
> Siamese region matching
> Prototypical region matching
> Support-conditioned CenterNet-style detection
> Compact feature-pyramid detectors
> Operation-specific transformation heads
> Connected-component proposals followed by learned pair verification
> Lightweight correlation volumes
> Offline pretrained compact visual backbones with lightweight fine-tuning
> A strong solution should jointly handle:
> Object localization
> Episodic source attribution
> Transformation recognition
> Distractor rejection
> Scale variation
> Printing degradation
> Ink dropout
> Partial fragmentation
> Support-query appearance differences
> Global classification alone is insufficient because the class meaning changes for every image.
> Template matching alone is also insufficient because support and query impressions are independently rendered and may differ substantially in appearance.

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Ceramic Layer Recovery Routing

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cr1f1f41epgg440h7mevphd8ardz9
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Inspect one ceramic print-layer image and produce a nozzle recovery route. The prediction must locate over-deposited, under-deposited, and mixed grid cells; visit every affected cell in the contract-defined order; identify adjacent cells that require conflicting flow changes; and select the overall recovery mode.
> This is not a defect-presence classifier. The image is converted into an executable maintenance plan. Sparse flaws, overlapping defect types, reflective wet clay, rotated parts, dark backgrounds, and different toolpath geometries must all be reconciled in one spatial ledger.
> The task reflects closed-loop additive manufacturing. A printer that only declares a bad layer still leaves an operator to decide where to intervene and whether material flow should increase, decrease, or alternate locally. The structured output makes that decision auditable.
> Dataset
> The prepared dataset contains 1,296 labeled training cases and 415 test cases. Images are resized with aspect ratio preserved to fit within 768 by 512 pixels. At most three source variants are retained from each original acquisition. Deterministic horizontal or vertical reflections, small contrast and brightness changes, low-level sensor noise, and JPEG re-encoding prevent byte-level or simple perceptual lookup while preserving the labeled geometry.
> Original acquisition groups are assigned wholly to train or test before opaque IDs and media names are created. Exact image hashes are checked, and no acquisition or identical image crosses the split.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Inputs and four structured targets for labeled cases. |
> | `test.csv` | Inputs only for hidden cases. |
> | `sample_submission.csv` | Required schema and valid formatting examples. |
> | `layers/*.jpg` | Opaque ceramic layer images. |
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque unique case identifier. |
> | `layer_image_path` | path string | Relative path to the ceramic layer JPEG. |
> | `recovery_contract` | string | Names the starting corner and defines nearest-Manhattan routing with row then column tie-breaking. |
> Flow Debt Matrix
> The image is divided into a 4 by 4 grid. Rows run top to bottom and columns left to right. Each annotated defect contributes to the cell containing its box center.
> | Cell value | Meaning |
> |---:|---|
> | `0` | No annotated defect center. |
> | `1`, `2`, `3` | One, two, or at least three over-extrusion centers. |
> | `-1`, `-2`, `-3` | One, two, or at least three under-extrusion centers. |
> | `4` | Both over-extrusion and under-extrusion occur in the cell. |
> Target Columns
> | Column | Data type | Description |
> |---|---|---|
> | `flow_debt_matrix` | JSON integer matrix | Shape 4 by 4 using values `-3` through `4` with the semantics above. |
> | `nozzle_recovery_program` | ordered token string | One visit per nonzero cell, then `seal:layer`. Visit tokens are `visit:rNcM:boost`, `visit:rNcM:reduce`, or `visit:rNcM:rebalance`. |
> | `adjacent_conflict_graph` | canonical edge set string | Orthogonally adjacent occupied cells with different actions, written `rNcM~rXcY`, sorted and joined by `|`; `none` if absent. |
> | `recovery_mode` | categorical string | `clear_layer`, `boost_flow`, `reduce_flow`, or `alternating_repair`. |
> The recovery program starts at the corner stated in recovery_contract. At each step it visits the remaining affected cell with the smallest Manhattan distance. Ties use the smaller row and then smaller column. Negative cells use boost, positive cells use reduce, and value 4 uses rebalance.
> Training recovery-mode counts are 110 clear_layer, 199 boost_flow, 202 reduce_flow, and 785 alternating_repair. Test counts are 56, 65, 75, and 219.
> Submission Format
> Write predictions to:
> ./working/submission.csv
> The file must contain exactly these columns in this order:
> case_id,flow_debt_matrix,nozzle_recovery_program,adjacent_conflict_graph,recovery_mode
> Example:
> case_id,flow_debt_matrix,nozzle_recovery_program,adjacent_conflict_graph,recovery_mode
> b847228bb85dff111a7544da,"[[0,0,0,0],[0,-1,1,0],[0,0,4,0],[0,0,0,0]]",visit:r2c2:boost>visit:r2c3:reduce>visit:r3c3:rebalance>seal:layer,r2c2~r2c3|r2c3~r3c3,alternating_repair
> Extra columns, reordered columns, duplicate IDs, missing IDs, and extra rows are rejected. Only a backend-added visibility column is ignored. Matrix text is limited to 100 characters, route text to 520 characters and 17 tokens, and graph text to 420 characters and 24 edges.
> Evaluation
> The metric is Layer Recovery Integrity Score:
> Score = 0.46 * FlowMatrixScore
> + 0.30 * RecoveryProgramScore
> + 0.16 * ConflictGraphScore
> + 0.08 * RecoveryModeScore
> For the 16 matrix entries:
> FlowMatrixScore = 0.10 * entry_accuracy + 0.90 * exact_matrix_match
> Program distance is Levenshtein distance over >-separated tokens:
> edit_similarity = 1 - edit_distance(true_tokens, predicted_tokens)
> / max(number_of_true_tokens, number_of_predicted_tokens, 1)
> RecoveryProgramScore = 0.12 * edit_similarity + 0.88 * exact_program_match
> Graph edges use standard set F1:
> ConflictGraphScore = 0.18 * set_F1 + 0.82 * exact_graph_match
> RecoveryModeScore = 1 for an exact category and 0 otherwise
> The submitted route must visit exactly the nonzero cells of the submitted matrix with the actions implied by their values. The submitted mode must also agree with that matrix. Incoherent rows receive a 10 percent penalty. Malformed or overlong values score zero for their component.
> Minimum score: 0.0
> Maximum score: 1.0
> Direction: higher is better.
> What Makes This Interesting
> The challenge converts real visual process defects into a constrained control program. Fine localization affects the matrix, the matrix determines a route under a case-specific start state, and neighboring cells can demand opposing flow changes. It therefore joins visual inspection, spatial planning, and consistency checking without relying on free-text grading.
> Method Requirements
> CPU-compatible detectors, compact segmentation models, small convolutional or transformer backbones, and learned structured decoders are allowed. Classical image processing may support a learned model but cannot be the primary prediction system.
> What Not To Use
> Do not recover source labels through original filenames, augmentation hashes, source archives, external mirrors, or image lookup tables.
> Do not map opaque paths, case_id, row position, file size, or compression artifacts directly to targets.
> Do not place variants of hidden test images into an external retrieval index.
> Do not update models or thresholds using hidden test labels or grader feedback.
> Do not exploit duplicate IDs, omitted rows, extra columns, malformed JSON, or parser limits.

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Visual Notation Audit Witness Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70bc2snmbnjkhs8pdw1r4cf18ar5sg
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: feature-engineering, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Music notation review tools often need to explain why a local mark should be inspected. For example, a dot-like mark, accidental, beam fragment, tie-like curve, rest, or notehead can require nearby context before a human or downstream system can decide what it means.
> Each example is a 512x512 crop from an engraved music page. One extra real notation glyph or glyph fragment has been inserted near compatible notation context to create a local audit target. The source images and inserted marks come from real engraved music pages; the insertion locations are generated so the visual witness boxes have known answers. These targets are generated visual audit cases rather than formal music-theory judgments.
> Your job is to recover the visual witness for the inserted audit target. Each row includes a coarse region_* search box that marks the part of the crop where the relevant evidence appears. Inside that region, predict three tighter boxes:
> culprit: the inserted mark or fragment that triggered the audit target
> anchor: the nearby note, rest, stem, or symbol that the culprit must be compared with
> reference: the staff line, ledger line, beam, stem, or other context needed to verify the relationship
> Also predict witness_type, the kind of visual audit pattern explained by those three boxes. This is not full optical music recognition: you do not need to transcribe the whole score. It is a localized visual evidence task over real music notation crops.
> Witness Types
> Allowed witness_type values:
> | Value | Meaning |
> |---|---|
> | duration_budget_witness | A visible duration symbol is the focus of a local duration audit |
> | dot_duration_witness | A dot-like mark must be interpreted relative to a nearby notehead or rest |
> | beam_grouping_witness | A beam fragment must be interpreted relative to local stems or note grouping |
> | pitch_spelling_witness | An accidental-like mark must be checked against a nearby notehead position |
> | tie_continuation_witness | A tie-like continuation mark must be checked against the local note context |
> | notehead_family_witness | A notehead-family audit target is visible only with nearby staff or stem context |
> Evaluation
> The score is maximized and ranges from 0 to 100.
> score = 100 * (
> 0.30 * mean_slot_iou
> + 0.20 * culprit_hit50
> + 0.12 * anchor_hit50
> + 0.10 * reference_hit35
> + 0.18 * witness_type_accuracy
> + 0.10 * exact_witness_accuracy
> )
> IoU is computed separately for the culprit, anchor, and reference boxes on each row. Missing predictions, invalid boxes, duplicate ids, or invalid witness types are rejected before scoring. mean_slot_iou is the average of the three per-slot IoUs for each row, then averaged over all rows. culprit_hit50 and anchor_hit50 are the fraction of rows where that slot has IoU at least 0.50. reference_hit35 is the fraction of rows where the reference slot has IoU at least 0.35. witness_type_accuracy is exact class accuracy. exact_witness_accuracy is the fraction of rows where all three localization thresholds are met and witness_type is correct.
> Dataset
> Public files:
> | File | Rows / Count | Description |
> |---|---:|---|
> | train.csv | 900 rows | Labeled visual evidence examples |
> | test.csv | 300 rows | Unlabeled visual evidence examples |
> | sample_submission.csv | 300 rows | Valid submission with deterministic placeholder boxes |
> | images/ | 1,200 PNG files | 512x512 music notation crops referenced by train and test rows |
> Hidden file:
> | File | Rows | Description |
> |---|---:|---|
> | answers.csv | 300 rows | Test witness boxes and witness types |
> CSV Columns
> train.csv columns:
> | Column | Type | Description |
> |---|---|---|
> | id | string | Unique example id |
> | image_path | string | Relative path to the 512x512 PNG crop |
> | width | integer | Image width, always 512 |
> | height | integer | Image height, always 512 |
> | region_xmin | number | Left edge of the coarse search region |
> | region_ymin | number | Top edge of the coarse search region |
> | region_xmax | number | Right edge of the coarse search region |
> | region_ymax | number | Bottom edge of the coarse search region |
> | witness_contract | string | JSON object naming the three required output slots and explaining their meanings |
> | culprit_xmin | number | Left edge of the culprit box |
> | culprit_ymin | number | Top edge of the culprit box |
> | culprit_xmax | number | Right edge of the culprit box |
> | culprit_ymax | number | Bottom edge of the culprit box |
> | anchor_xmin | number | Left edge of the anchor box |
> | anchor_ymin | number | Top edge of the anchor box |
> | anchor_xmax | number | Right edge of the anchor box |
> | anchor_ymax | number | Bottom edge of the anchor box |
> | reference_xmin | number | Left edge of the reference box |
> | reference_ymin | number | Top edge of the reference box |
> | reference_xmax | number | Right edge of the reference box |
> | reference_ymax | number | Bottom edge of the reference box |
> | witness_type | string | One of the six allowed witness types |
> Example witness_contract value:
> {"task":"recover_visual_witness_set_for_inserted_notation_audit_target","witness_slots":["culprit","anchor","reference"],"slot_meanings":{"culprit":"inserted glyph or fragment that triggered the audit target","anchor":"nearby glyph whose relation to the culprit makes the target interpretable","reference":"staff, beam, stem, or ledger context needed to verify the relation"}}
> test.csv contains id, image_path, width, height, region_xmin, region_ymin, region_xmax, region_ymax, and witness_contract.
> sample_submission.csv and answers.csv use the submission columns below.
> Submission
> Submit a CSV with exactly this header and one row per test id:
> id,culprit_xmin,culprit_ymin,culprit_xmax,culprit_ymax,anchor_xmin,anchor_ymin,anchor_xmax,anchor_ymax,reference_xmin,reference_ymin,reference_xmax,reference_ymax,witness_type
> test_0123456789abcdef,88,144,119,179,128,132,164,176,68,184,212,199,pitch_spelling_witness
> test_fedcba9876543210,221,82,281,105,230,118,269,163,202,69,321,91,beam_grouping_witness
> Requirements:
> Include exactly one row for every test id.
> Use the exact column order shown above.
> All box coordinates must be numeric and inside the 512x512 image frame.
> For every box, xmax must be greater than xmin, and ymax must be greater than ymin.
> witness_type must be one of the six allowed values.
> Missing values, duplicate ids, extra ids, extra columns, and invalid witness types cause rejection.
> Save the file as ./working/submission.csv.
> Restrictions
> Use only the provided challenge files and generally available methods.
> Do not use hidden files, row order, file order, hashes, grader internals, or source-row reconstruction.
> Standard computer vision, visual reasoning, annotation learning, and lightweight CPU models are allowed.

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Canal Surface Position-Shape Card Inventory

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73n1797n4gnwhw9r3an91nhs8avb7y
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering, image
- Best/top context found: Top Score | — | Created | Jul 19, 2026 | Start New Solution

Full challenge description from page:

> Overview
> Waterway monitoring images often contain scattered floating debris that is easy to notice coarsely but hard to inventory precisely. Each row gives one RGB canal scene. Your task is to build a compact position-shape inventory for the visible debris: one card per debris item, with a fine-grid center cell and three binned footprint measurements.
> The center grid has 36 rows and 64 columns over the full image. A card such as {"center_cell":"r18_c32","width_bin":2,"height_bin":2,"area_bin":2} means the debris center falls in row 18, column 32 of that grid, with released width, height, and area bins for the same visible item.
> The prediction is an unordered, duplicate-aware card inventory. It is not enough to give a total count or a rough region tally; high scores require matching the individual debris positions and their footprint bins.
> Dataset
> The files are:
> train.csv: 1,240 labeled examples.
> test.csv: 261 unlabeled examples to predict.
> sample_submission.csv: valid low-information submission example.
> images/: JPG images referenced by image_path.
> train.csv columns:
> id (string): public row identifier.
> image_path (string): relative image path under images/.
> width (integer): image width in pixels.
> height (integer): image height in pixels.
> prompt (string): task instruction for the row.
> answer_format_json (stringified JSON): required output schema and valid bins.
> answer_json (stringified JSON): target position-shape card inventory.
> test.csv contains the same fields except answer_json.
> Fields in answer_format_json:
> required_fields (list of strings): required top-level keys in answer_json.
> max_cards (integer): maximum number of debris cards, always 20.
> center_grid (list of integers): [36,64], the row and column count for center cells.
> center_cell_format (string): cell-name format such as r00_c00.
> width_bin_values (list of integers): allowed width bins, 0 through 7.
> height_bin_values (list of integers): allowed height bins, 0 through 7.
> area_bin_values (list of integers): allowed area bins, 0 through 7.
> card_fields (list of strings): required fields in each debris card.
> Each answer_json has exactly this shape:
> {
> "count": 2,
> "debris_cards": [
> {"center_cell": "r11_c28", "width_bin": 2, "height_bin": 2, "area_bin": 2},
> {"center_cell": "r25_c48", "width_bin": 3, "height_bin": 3, "area_bin": 4}
> ]
> }
> count is the number of submitted debris cards and must equal the length of debris_cards. debris_cards is unordered. If two visible items fall into the same binned card, both copies should be submitted.
> Submission
> Submit a CSV with exactly these columns:
> id
> answer_json
> Example:
> id,answer_json
> canal_example_001,"{""count"":2,""debris_cards"":[{""center_cell"":""r11_c28"",""width_bin"":2,""height_bin"":2,""area_bin"":2},{""center_cell"":""r25_c48"",""width_bin"":3,""height_bin"":3,""area_bin"":4}]}"
> canal_example_002,"{""count"":1,""debris_cards"":[{""center_cell"":""r18_c32"",""width_bin"":2,""height_bin"":2,""area_bin"":2}]}"
> The JSON object must contain exactly count and debris_cards. Each card must contain exactly center_cell, width_bin, height_bin, and area_bin. Extra keys, missing keys, invalid cells, invalid bins, duplicate IDs, missing rows, or extra rows are invalid. A malformed row-level JSON value scores 0 for that row and the rest of the file is still graded.
> Evaluation
> The scorer first validates the global CSV:
> columns must be exactly id,answer_json;
> row count must match test.csv;
> IDs must be present, unique, and exactly match the ids in test.csv.
> Global shape errors raise validation errors. Row-level JSON/schema errors score 0 for that row.
> For valid rows:
> count_score =
> 1 - abs(predicted_count - true_count)
> / (predicted_count + true_count)
> If both counts are zero, count_score = 1.
> The other terms use duplicate-aware multiset F1:
> multiset_f1 =
> 2 * matched_items / (predicted_item_count + true_item_count)
> center_f1 compares only center_cell values.
> shape_f1 compares triples (center_cell, width_bin, height_bin).
> exact_card_f1 compares full cards (center_cell, width_bin, height_bin, area_bin).
> Final row score:
> row_score = 0.08 * count_score
> + 0.24 * center_f1
> + 0.18 * shape_f1
> + 0.50 * exact_card_f1
> The final score is the mean row score across all test rows.
> What Not To Use
> Do not use GPU acceleration.
> Do not use outside copies of the annotations or image collections.
> Do not use external file metadata, experiment names, camera/time metadata, or outside matching to reconstruct answers.
> Do not use hosted inference APIs, non-public or gated assets, challenge-specific pretrained checkpoints, additional model weights, runtime package installation, or remote-code loaders.
> Do not submit malformed JSON, invalid card fields, duplicate IDs, or rows with extra/missing columns.

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Pitch Person Formation Geometry Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78nd9w1s6khhw3x6p48g04t18b2arf
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Each example is a broadcast-style pitch image containing multiple visible people on or near the field of play. The task is to recover a compact formation geometry record: how many people are visible, where each person is located, the approximate body box, the bottom-center footpoint, the coarse grid cell, and simple position bins for lane, depth, and apparent size.
> Most rows contain many small visible people at different scales, with partial occlusion and crowded areas. Solvers must localize multiple visible people and keep the structured counts consistent with the submitted cards.
> Dataset
> The public files are:
> train.csv: 256 labeled training rows.
> test.csv: 255 unlabeled test rows.
> sample_submission.csv: a valid low-information submission showing the required CSV and JSON shape.
> images/: transformed 640 by 360 pitch images referenced by the CSV files.
> Columns in train.csv:
> id (string): row identifier.
> image (string): relative path to the image.
> prompt (string): task instruction.
> packet_json (JSON string): public image-level context with image_size, coordinate_scale, and grid_shape.
> answer_format_json (JSON string): output constraints, valid bins, coordinate scale, and maximum card count.
> answer_json (JSON string): target object for training rows.
> test.csv includes the pitch image, prompt, context packet, and schema fields; the formation target is withheld.
> The expected answer_json object has:
> player_count (integer): number of submitted person cards, from 0 to 35.
> lane_counts (object): counts for left, center, and right.
> depth_counts (object): counts for near, midfield, and far.
> size_counts (object): counts for small, medium, and large.
> occupied_cells (list of strings): unique 12 by 20 grid cells used by the person cards, formatted like r07_c12.
> player_cards (list): one record per visible person.
> Each person card contains:
> box (list of four numbers): [x0,y0,x1,y1] body box on a 0-1000 coordinate scale.
> footpoint (list of two numbers): [x,y] bottom-center point of the box on the same scale.
> center_cell (string): 12 by 20 grid cell containing the box center.
> lane (string): left, center, or right, determined from the footpoint x-position.
> depth_bin (string): near, midfield, or far, determined from the box center y-position.
> size_bin (string): small, medium, or large, determined from the box height.
> Evaluation
> Per-image formation scores are averaged across the test rows. Higher is better:
> row_score =
> 0.12 * support_score
> + 0.88 * player_card_f1^4
> player_count_score is intentionally part of support_score; it is not repeated as a separate top-level row-score term.
> player_count_score = max(0, 1 - abs(predicted_player_count - true_player_count) / max(1, true_player_count)).
> For each count dictionary:
> count_score = 1 - sum_k abs(predicted_count_k - true_count_k)
> / sum_k (predicted_count_k + true_count_k)
> If both count dictionaries sum to zero, the count score is 1.
> occupied_cell_f1 is standard set F1:
> occupied_cell_f1 = 2 * |predicted_cells intersect true_cells|
> / (|predicted_cells| + |true_cells|)
> If both sets are empty, the score is 1.
> player_card_f1 is duplicate-aware greedy F1 over person cards. For each submitted/hidden card pair:
> pair_score =
> 0 if IoU(box) < 0.10 and Euclidean_distance(footpoint) > 35
> otherwise:
> pair_score =
> 0.60 * IoU(box)^3
> + 0.28 * exp(-(Euclidean_distance(footpoint) / 32)^2)
> + 0.12 * bin_score
> bin_score =
> 0.40 * center_cell_exact
> + 0.20 * lane_exact
> + 0.25 * depth_bin_exact
> + 0.15 * size_bin_exact
> Distances use the 0-1000 coordinate scale. IoU(box) is the standard intersection-over-union of two axis-aligned boxes. Exact-match terms are 1 when equal and 0 otherwise. Matching only coarse bins is not enough: a submitted card must overlap the correct person box or place the footpoint very close to it before any bin agreement earns credit.
> All submitted/hidden card pairs are sorted from highest pair_score to lowest. The grader takes the highest-scoring remaining one-to-one matches. If matched_sum is the sum of selected pair scores, then:
> player_card_f1 = 2 * matched_sum / (submitted_card_count + hidden_card_count)
> If both card lists are empty, the person-card score is 1.
> The support term is:
> support_score =
> 0.32 * player_count_score^2
> + 0.18 * lane_count_score
> + 0.18 * depth_count_score
> + 0.12 * size_count_score
> + 0.20 * occupied_cell_f1^2
> The grader checks internal consistency: player_count must equal the number of person cards, occupied_cells must match the cards, count dictionaries must match the cards, and each card's lane/depth/size/cell must match its submitted geometry. Malformed JSON or an invalid row scores 0 for that row. Wrong columns, extra columns, missing rows, duplicate ids, or ids that do not match the test set make the whole submission invalid.
> Submission
> Submit a CSV with exactly two columns:
> id (string): must match the ids in test.csv; row order is not used by the grader.
> answer_json (JSON string): predicted formation geometry using the schema above.
> Example:
> id,answer_json
> pitchgeom_example_001,"{""player_count"":2,""lane_counts"":{""left"":1,""center"":1,""right"":0},""depth_counts"":{""near"":1,""midfield"":1,""far"":0},""size_counts"":{""small"":0,""medium"":2,""large"":0},""occupied_cells"":[""r06_c09"",""r09_c04""],""player_cards"":[{""box"":[430,500,470,620],""footpoint"":[450,620],""center_cell"":""r06_c09"",""lane"":""center"",""depth_bin"":""midfield"",""size_bin"":""medium""},{""box"":[205,730,255,860],""footpoint"":[230,860],""center_cell"":""r09_c04"",""lane"":""left"",""depth_bin"":""near"",""size_bin"":""medium""}]}"
> pitchgeom_example_002,"{""player_count"":0,""lane_counts"":{""left"":0,""center"":0,""right"":0},""depth_counts"":{""near"":0,""midfield"":0,""far"":0},""size_counts"":{""small"":0,""medium"":0,""large"":0},""occupied_cells"":[],""player_cards"":[]}"
> What Not To Use
> Do not use GPU acceleration.
> Do not use outside sports-video, person-detection, broadcast-analysis, tracking, or segmentation datasets.
> Do not use pretrained player/person detectors, sports-analysis models, mask-recovery models, or additional checkpoint files.
> Do not call hosted vision APIs, remote analysis services, runtime package installers, torch.hub, or trust_remote_code.
> Do not search for matching match frames, source metadata, external labels, or image hashes.
> Do not hard-code player layouts or formation cards for specific test ids.
> Use only the released public files while producing predictions.

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Urban Overhead Vehicle Arrangement Sheet

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7307hpybjcy55pf7hm6ce4bn8b3jmb
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image, feature-engineering, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.687

Full challenge description from page:

> Overview
> Each row contains a 128 by 128 overhead image tile from an urban scene. Your task is to predict a compact vehicle arrangement sheet for the tile: the total number of visible vehicles, which grid cells contain vehicle centers, which grid cells are crowded, how many vehicles touch the image boundary, and a short list of representative vehicle cards.
> The imagery comes from overhead object annotations that have been prepared as small competition tiles: public ids and filenames are remapped, original source identifiers are absent, and all outputs use the tile-local grid described below. The visible vehicles are tiny, often close together, and can be partly cut off by the tile edge. A correct answer must make the count, occupied cells, crowded cells, edge count, and card list agree with one another.
> Dataset
> Files:
> train.csv: training rows with id, image_path, context_json, answer_format_json, and answer_json.
> test.csv: rows with id, image_path, context_json, and answer_format_json.
> sample_submission.csv: valid weak placeholder predictions.
> images/: transformed 128 by 128 aerial image tiles.
> Columns:
> id (string): row identifier.
> image_path (string): relative path to the transformed tile image.
> context_json (JSON string): public tile context.
> image_size (list[integer]): image width and height in pixels, always [128,128].
> grid_shape (list[integer]): grid rows and columns, always [8,8].
> max_vehicle_cards (integer): maximum number of representative vehicle cards allowed in the answer.
> source_split_hint (string): coarse split marker retained for auditing only; it is not a label.
> answer_format_json (JSON string): required output schema with the grid shape, valid cell ids, valid size/aspect bins, and card limit.
> answer_json (JSON string, train only): object with:
> vehicle_count (integer): number of vehicle boxes in the tile.
> occupied_cells (list[string]): 8 by 8 grid cells such as r03c05 containing at least one vehicle center.
> crowded_cells (list[string]): occupied cells containing two or more vehicle centers.
> edge_touch_count (integer): number of vehicle boxes touching the image boundary.
> vehicle_cards (list[object]): up to six objects with cell, size_bin, and aspect_bin. These cards summarize representative vehicle centers and are used to check whether the submitted arrangement sheet is spatially consistent.
> Allowed size_bin values are tiny, small, medium, and large. Allowed aspect_bin values are wide and tall.
> Evaluation
> Submissions are scored by mean row score from 0 to 1.
> For each row:
> count_score = max(0, 1 - abs(predicted_count - true_count) / max(predicted_count, true_count, 1))
> occupied_score is F1 between predicted and true occupied-cell sets.
> crowded_score is F1 between predicted and true crowded-cell sets.
> edge_score uses the same count formula as count_score, applied to edge_touch_count.
> card_score is F1 between sets of (cell, size_bin, aspect_bin) vehicle cards.
> Set F1 is 1 when both sets are empty, and 0 when exactly one set is empty.
> The row score is:
> 0.22 * count_score
> + 0.30 * occupied_score^2
> + 0.14 * crowded_score
> + 0.14 * edge_score
> + 0.20 * card_score
> The square on occupied_score is intentional: it reduces credit for broad guesses that mark many nearby cells while missing the exact occupied-cell pattern.
> Malformed JSON or invalid field values score 0 for that row. Missing rows, extra rows, duplicate ids, missing columns, or extra columns are rejected.
> Submission
> Submit a CSV with exactly two columns:
> id (string)
> answer_json (JSON string)
> Example:
> id,answer_json
> tile_example_001,"{""vehicle_count"":2,""occupied_cells"":[""r03c04"",""r04c04""],""crowded_cells"":[],""edge_touch_count"":0,""vehicle_cards"":[{""cell"":""r03c04"",""size_bin"":""small"",""aspect_bin"":""wide""}]}"
> tile_example_002,"{""vehicle_count"":0,""occupied_cells"":[],""crowded_cells"":[],""edge_touch_count"":0,""vehicle_cards"":[]}"
> What Not To Use
> Do not use external datasets, source archives, source identifiers, or lookup tables outside the released files.
> Do not reverse-search images or match released tiles to public map sources.
> Do not use hidden answers, row-order tricks, or hard-coded test-row predictions.
> Do not install packages at runtime or call hosted inference/vision APIs.
> Do not use GPU execution.

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Facade Workfront Proposal from Inspection Frames

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx717k3fv2yx7cq6ae8914t7t98bwr58
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat pvduy's score of 44.736!

Full challenge description from page:

> Vertical Envelope Workfronts Overview Build an CPU-only object detector that converts building-envelope inspection images into review-ready intervention zones. A workfront is an image-plane rectangle that groups one or more nearby visual findings requiring the same maintenance action. It is a triage unit for inspection review and repair planning; it is not a claim about exact platform reach, physical access geometry, or final engineering scope. The task represents the second stage of an inspection workflow: an upstream screening pass has already selected candidate maintenance frames, and this system must turn each frame into a compact set of action-labeled zones. For every workfront in an image, predict: its anonymous action code; a confidence score used for ranking; its normalized bounding box. The five action codes are operational intervention categories: | Code | Required building-envelope action | |---|---| | a0 | Seal a narrow linear discontinuity. | | a1 | Investigate and isolate a moisture-ingress region. | | a2 | Reinstate a detached or missing surface finish. | | a3 | Treat an exposed or oxidized material region. | | a4 | Escalate an outward-deformation region for engineering review. | The images contain real exterior-surface texture, joints, parapets, walkways, roof and eave edges, windows, shadows, staining, vegetation, fixtures, and other confounders. They are standardized to a common size and may include realistic capture degradation such as haze, blur, compression, illumination shifts, and mirror orientation. Thin discontinuities and small intervention zones are especially important. Rows from one local capture neighborhood share an opaque batch_id. Source sequences are assigned wholly to one split before local batches are exposed, and perceptual near-duplicates are thinned. Training and test batches are disjoint, so the task measures transfer to new building regions rather than memorization of adjacent frames. The complete solution must run on CPU and finish within 1.5 hours, including training, local validation, inference, and submission generation. Up to 62.5 GB RAM is available. Dataset dataset/public/ ├── train.csv ├── test.csv ├── sample_submission.csv └── images/ └── facade_.jpg All public images are RGB JPEG files with size 512 × 320 pixels. Identifiers and filenames are opaque. Bounding-box coordinates are normalized to [0, 1] relative to the public image width and height. train.csv train.csv contains 800 rows and these columns: id,batch_id,image_path,detections id Data type: string Opaque row identifier, unique within train.csv. batch_id Data type: string Opaque local capture-neighborhood group. Use it for grouped validation. image_path Data type: string Relative path beneath dataset/public/. detections Data type: JSON array encoded as a string Ground-truth workfronts for the image. Each element of the training detections column has exactly this form: {"action":"a0","bbox":[0.132,0.118,0.287,0.361]} bbox is: [x_min, y_min, x_max, y_max] and must satisfy: 0 = 0.25 are active. An image is frame-complete only when: the number of active detections equals the number of target workfronts; and a complete one-to-one matching exists in which every pair has the same action and IoU at least 0.50. One missed workfront, one extra active detection, one wrong action, or one poorly localized box makes that image score zero for this component. F_complete = frame-complete test images / all test images Final score score = 100 × (0.70 × AP_multi + 0.20 × R_small + 0.10 × F_complete) Not allowed External APIs or remote inference services. External façade-defect, building-damage, or workfront annotations, including task-specific pretrained detectors. Manual annotation or case-by-case visual labeling of test images. Hard-coding predictions by id, batch_id, filename, or row order. Exploiting serialization artifacts, identifiers, grouping metadata, or file ordering instead of modeling image content. &nbsp;
> $700 Pool
> Closes in 8h 37m
> 11 / 12 beat AI

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.


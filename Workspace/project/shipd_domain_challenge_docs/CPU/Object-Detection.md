# CPU Object Detection Challenge Examples

Scrape timestamp: 2026-07-14T00:00:00+05:30

Confirmed CPU examples in this document: 0

These entries are included because the challenge detail page displayed this domain and the challenge is part of the CPU-only challenge collection.

## Sparse-Frame Object Forecasting

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76m043degefe4wqhjv7dre4989zgk3
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: image, segmentation, large-scale
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Sparse-Frame Object Forecasting
> Overview
> Each input frame is a sparse motion field: only pixels whose brightness changed between successive instants are lit, so a moving object appears as a drifting cluster of bright dots against an otherwise empty background — there is no static texture, filled silhouette, or steady color to read an object off directly. This challenge supplies short bursts of such frames — four in a row following a single moving object — and asks for the object's bounding box and category one time step beyond what is shown. That final frame is withheld; the only evidence available is the object's trajectory across the visible history.
> Every clip contains exactly one object drawn from four categories: people, car, cat, uav. Object category is labeled on every frame of the training clips, but test clips supply only raw history imagery, so the category itself must also be inferred from appearance rather than read off a label. Motion is not uniform: objects speed up, slow down, reverse, or drift toward the frame edge, so the object's last visible position is frequently a poor estimate of where it lands one step later. Category frequency is skewed — cat and uav clips are common while people and car clips are scarcer — and the scoring function averages across categories rather than clips, so the scarcer categories are not washed out by the frequent ones. A submission must also state its class belief as a calibrated probability vector, which the Brier-based scoring rewards for honesty rather than confidence alone.
> Solver environment: CPU-only — 10 cores, 62 GB RAM, no GPU — and every submission must run end-to-end (data loading + training + inference) in ≤ 1.5 hours. Frames are provided at a reduced 640x360 resolution to fit this budget; the sparse moving-object trace remains clearly resolvable at this size.
> Dataset
> Each record is a short clip: five sequential rendered frames (PNG, 640x360) from a single recording, labeled t0 through t4 in chronological order. Exactly one object is tracked per clip — one box per frame, one category for the whole clip. History frames t0–t3 are always provided; the objective is to forecast the object in frame t4. Training clips retain t4 and its label; test clips do not.
> Public files
> **public/images/train/<clip_id>/** — history frames t0.png–t3.png and the forecast frame t4.png for every training clip, each at 640x360.
> **public/images/test/<clip_id>/** — history frames t0.png–t3.png for every test clip, each at 640x360. Frame t4.png is withheld.
> **public/train.csv** — five rows per clip (one per frame). Columns: clip_id, frame_index, x, y, w, h, category.
> **public/test.csv** — one row per test clip. Column: clip_id.
> **public/sample_submission.csv** — a correctly-formatted placeholder submission.
> Private file (organizer only)
> **private/answers.csv** — the true t4 object for each test clip. Columns: clip_id, x, y, w, h, category. Not distributed to participants.
> Column descriptions
> train.csv records the tracked object's box in every frame of every clip:
> clip_id (string) — clip identifier; matches the directory public/images/train/<clip_id>/.
> frame_index (int) — frame position within the clip, 0–4; 4 is the frame being forecast. Only present in train.csv.
> x (float) — box left edge, in pixels from the frame's left edge.
> y (float) — box top edge, in pixels from the frame's top edge.
> w (float) — box width in pixels.
> h (float) — box height in pixels.
> category (string) — object category, one of people, car, cat, uav.
> test.csv holds a single column:
> clip_id (string) — identifier of the test clip to forecast; matches the directory public/images/test/<clip_id>/, which contains history frames t0.png–t3.png. Each frame measures 640x360 pixels.
> Data example
> One clip's five training rows (a single tracked object across all frames):
> clip_id,frame_index,x,y,w,h,category
> clip_75cda5e34a6b,0,259.49,278.07,30.4,17.33,car
> clip_75cda5e34a6b,1,279.5,280.21,30.4,17.32,car
> clip_75cda5e34a6b,2,299.51,282.36,30.4,17.32,car
> clip_75cda5e34a6b,3,319.52,284.5,30.39,17.32,car
> clip_75cda5e34a6b,4,339.54,286.64,30.4,17.32,car
> Submission format
> Submit a file named submission.csv containing exactly these 9 columns, in order:
> clip_id,x,y,w,h,p_people,p_car,p_cat,p_uav
> Each row forecasts one test clip: a bounding box (x, y, w, h, top-left origin, pixel units) for the object expected in frame t4, plus a probability vector across the four categories. Requirements:
> Exactly **one row per clip_id**, and every clip listed in test.csv must be covered.
> The four p_* values must be non-negative and sum to 1 (tolerance of 0.02; values are renormalized after the check passes).
> Exactly the columns listed above — no more, no fewer — with a header row.
> Box width and height must both be strictly positive.
> Sample submission (two clips):
> clip_id,x,y,w,h,p_people,p_car,p_cat,p_uav
> clip_3d2af526c0a0,318,174,54,31,0.10,0.80,0.05,0.05
> clip_55d4fcfd6ced,120,80,35,45,0.05,0.05,0.85,0.05
> Evaluation
> Scoring uses the Macro Calibrated Forecast Score (MCFS), higher is better. It combines localization accuracy and calibrated class belief, then averages across the four categories so that scarcer categories weigh as much as common ones.
> Per-clip score. For a test clip with true category c*, true box g, predicted box p, and predicted probability vector prob over the four categories:
> iou  = IoU(p, g)
> loc  = iou  if iou >= 0.5  else  0       # localization gate
> cls  = 1 - 0.5 * sum_k (prob[k] - 1[k == c*])^2   # Brier reward in [0, 1]
> q    = loc * cls                          # clip quality in [0, 1]
> A predicted box overlapping the true box below the 0.5 IoU threshold scores zero for that clip regardless of the category prediction. The Brier term reaches its maximum (cls = 1) only when all probability mass sits on the true category; both a confident wrong guess and a hedged, uncertain guess are penalized relative to it.
> Per-category aggregation.
> class_score_c = mean(q) over all test clips whose true category is c
> Final score.
> MCFS = mean over the 4 categories of class_score_c
> Averaging over categories rather than clips means the less-common car category (15.4% of clips) is weighted equally with the more common cat category (34.9%).
> Reference scores. A perfect forecast scores 1.0. A random or empty forecast scores near 0.0; because every valid submission must report a strictly positive score, any raw score at or below 0.02 is raised to that fixed floor value. The IoU threshold is 0.5 and the probability-sum tolerance is 0.02.
> What Not To Use (Prohibited Methods)
> This task must be solved using only the provided sparse-motion frames and training labels.
> No external answer keys or label sources. Do not use any external dataset, its annotations, or precomputed boxes to recover or supplement t4 forecasts.
> No source matching. Do not attempt to match provided frames, clip IDs, or pixel content back to any public dataset, recording, or repository in order to look up the withheld frame. Clip IDs are anonymized; re-identifying their origin or retrieving the true t4 frame by any external means is not allowed.
> No id-based hardcoding. Do not hardcode forecasts or category distributions keyed to specific clip IDs, and do not build a lookup table of test answers.
> No train/test leakage. Do not train or tune on test clips. The withheld t4 frame of a test clip must never be obtained by any means.
> No private-label tuning. Do not attempt to access, reconstruct, or fit to private/answers.csv.
> No manual annotation. Do not hand-label, crowdsource, or visually inspect-and-record forecasts for the test clips.
> Submissions may be audited for these behaviors; violations are grounds for rejection.

Inspiration note: Useful because it makes object detection temporal by asking solvers to forecast sparse-frame object presence/locations, with CPU-compatible inputs and a detection-style output shape.

## Habitat Instance Contact Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a0wazct5myxbhp21wfcs8j58aqq0v
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Field survey systems must count individual target organisms without merging nearby bodies into one detection. This is especially difficult when organisms overlap, touch, or rest within the same plant cluster. To reduce uplink bandwidth and avoid retaining identifiable raw habitat photographs, the supplied images are three-channel edge-and-texture telemetry views rather than RGB photographs. Your task is to locate every visible target instance and recover a contact graph that indicates which detected instances touch or nearly touch.
> The hidden set is separated from training by capture session, not by random image row. It also includes confirmed empty scenes and look-alike organisms. Every telemetry view is deterministically derived from one real photograph; there are no generated or composited records. Good solutions must therefore generalize across recording conditions, reject hard negatives, separate crowded instances, and produce a consistent graph.
> Dataset
> File descriptions
> train.csv: labeled training rows.
> test.csv: unlabeled test rows.
> train/images/: training JPEG edge-and-texture telemetry views.
> test/images/: test JPEG edge-and-texture telemetry views.
> sample_submission.csv: valid submission structure with random example predictions.
> Column descriptions
> train.csv:
> id: opaque image identifier.
> image_path: path relative to dataset/public.
> instances: JSON list of ground-truth instances.
> test.csv:
> id: opaque image identifier.
> image_path: path relative to dataset/public.
> Each object in instances contains:
> instance_id: unique string within that image.
> bbox: [x_min, y_min, x_max, y_max], normalized to [0, 1].
> contacts: list of instance_id values for other instances in the same image.
> Two ground-truth boxes are contacts when the Euclidean gap between their rectangular boundaries is at most 0.02 of image width/height. Touching and overlapping boxes have zero gap. Each relation is undirected; listing it from either or both endpoints has the same meaning.
> The public data contain 1,919 labeled training images. The hidden set contains 691 images from held-out capture sessions.
> Evaluation
> Predicted boxes are matched one-to-one to ground truth with Hungarian assignment at IoU >= 0.50.
> Detection F1 is computed per image and averaged equally across three hidden object-count strata: empty, one instance, and two-or-more instances. Contact edges are mapped through the matched boxes. Topology quality combines edge F1 with matched-node coverage and is averaged equally across multi-instance images with and without contacts.
> The final score is the geometric mean of the two components:
> detection_score = mean([empty_f1, single_f1, multi_f1])
> topology_score = mean([no_contact_topology, contact_topology])
> score = sqrt(detection_score * topology_score)
> Either component reaching zero forces the final score to zero. The geometric mean prevents strong localization from masking a weak contact graph, while the stratified component averages prevent abundant easy scenes from hiding failures on empty or crowded cases. Higher is better; the range is 0 to 1.
> Submission
> Submit submission.csv with:
> id: every test identifier exactly once.
> instances: JSON list using the schema above.
> Example:
> id,instances
> 00111dc6a64d8234,"[{""instance_id"":""p1"",""bbox"":[0.112,0.244,0.251,0.396],""contacts"":[]}]"
> 0050f30778a61e22,[]
> Requirements
> Include exactly the columns id,instances and every test ID once.
> Use finite normalized box coordinates with x_max > x_min and y_max > y_min.
> Use unique instance IDs within each image.
> Contact references must point to predicted instances in the same row and cannot contain self-links.
> Use only the supplied public data. Do not recover the source corpus, filenames, or hidden annotations through external lookup.

Inspiration note: Useful because it turns CPU object detection into structured instance recovery: boxes plus a contact graph, with stratified/geometric scoring that rewards both localization and topology.

## Lab Bench Inventory Reconciliation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7976a3kye5bd32aeabc513en8apfn3
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Laboratory inventory systems need more than a list of visible tools. A technician looking for missing apparatus or clearing a work area also needs to know where each item is located. Camera changes, reflective glass, overlapping vessels, and nearly identical flask variants make this difficult to automate reliably.
> Predict a zone-aware apparatus ledger for each bench photograph. Each ledger records the count of every apparatus category whose object center lies in the left, center, or right third of the image. The test set is captured by a camera model absent from training, so successful systems must generalize beyond device-specific appearance.
> Dataset
> File descriptions
> train.csv -- Labeled training rows with image paths and zone-aware inventory ledgers.
> test.csv -- Test rows with image paths but no inventory ledger.
> train/ -- Training photographs referenced by train.csv.
> test/ -- Test photographs referenced by test.csv.
> labels.json -- Allowed apparatus labels, zone names, zone rule, and ledger format.
> sample_submission.csv -- Submission template populated with deterministic nonzero example predictions.
> Column descriptions
> id (string) -- Unique 12-character hexadecimal image identifier.
> image_path (string) -- Path to the photograph relative to the public dataset directory.
> inventory (string) -- Target in train.csv only. Pipe-separated apparatus@zone:count entries, or none when no apparatus is present.
> Zones use the horizontal center of each visible apparatus instance:
> left -- Center x-coordinate is below one third of image width.
> center -- Center x-coordinate is at least one third and below two thirds of image width.
> right -- Center x-coordinate is at least two thirds of image width.
> The released 512 × 512 images are deterministic crops with mild perspective and
> rotation changes plus optional horizontal flips. They remain transformed real
> photographs rather than generated or composite images. Apparatus is included only
> when its center remains in-frame and at least half of its transformed bounding box
> is visible. Zone labels refer to object centers in the displayed image after this
> transformation.
> Evaluation
> Submissions are scored with zone-aware count intersection over union (count IoU). Each apparatus-zone pair is treated as a multiset token: matched units form the intersection, while matched, excess, and missing units form the union. The final score is 70% macro count IoU across apparatus-zone tokens that have private support and 30% micro count IoU across all tokens. Unsupported-token false positives still enlarge the micro union.
> def evaluate(predicted_ledgers, true_ledgers, apparatus, zones):
> per_token_iou = []
> micro_tp = micro_fp = micro_fn = 0
> for name in apparatus:
> for zone in zones:
> token = f"{name}@{zone}"
> tp = fp = fn = support = 0
> for predicted, actual in zip(predicted_ledgers, true_ledgers):
> p = predicted.get(token, 0)
> a = actual.get(token, 0)
> support += a
> tp += min(p, a)
> fp += max(p - a, 0)
> fn += max(a - p, 0)
> if support > 0:
> per_token_iou.append(tp / (tp + fp + fn))
> micro_tp += tp
> micro_fp += fp
> micro_fn += fn
> macro_iou = sum(per_token_iou) / len(per_token_iou)
> micro_iou = micro_tp / (micro_tp + micro_fp + micro_fn)
> return 0.70  *macro_iou + 0.30*  micro_iou
> Higher is better, with a score range from 0 to 1. Count IoU represents the fraction of the combined reported and actual inventory that is correctly reconciled, so every missing or excess unit has a direct cost. Macro weighting prevents common beakers and bottles from hiding failures on uncommon supported apparatus-zone combinations; the micro component reflects total inventory accuracy.
> Submission
> Submit one zone-aware inventory string for every test image.
> id (string) -- Identifier copied exactly from test.csv.
> inventory (string) -- Pipe-separated apparatus@zone:count entries. Use none only when predicting no apparatus.
> Example:
> id,inventory
> 003895b2d5df,beaker@left:1|conical_flask@center:1
> 00d49ec486c7,reagent_bottle@right:2
> Requirements
> The file must contain exactly 969 rows plus the header.
> Columns must be exactly id,inventory.
> Every test id must appear exactly once, with no missing or duplicate IDs.
> Apparatus names and zones must match labels.json exactly.
> Counts must be integers from 1 through 10; do not include zero-count entries or duplicate tokens.
> File format: CSV only.
> What Not To Use
> Do not reverse-search test images or use exact-image/source matching to obtain apparatus identities or locations.
> Do not retrieve external copies of these photographs, their object-label files, or their annotation metadata to reconstruct test ledgers.
> Do not use checkpoints, lookup tables, or caches trained specifically on annotations for these test photographs.

Inspiration note: Useful because it casts object detection as inventory reconciliation: detect/count visible lab items and reward scene-level consistency, a practical CPU-friendly structured vision pattern.

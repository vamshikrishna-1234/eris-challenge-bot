# Non-CPU Object Detection Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed Non-CPU examples in this document: 16

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.

## Garment Instance Token Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx724bzfky50rnhn17przyzc898a71p4
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: image, multimodal, Dataset source is visible after the challenge closes.
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Objective
> Recover a structured visual ledger for each fashion image. For every test image, submit the visible garment instances as JSON: each instance needs an anonymized garment category token, a normalized bounding box, and anonymized localized attribute tokens supported by the image evidence.
> This is a visual parsing task. Strong submissions should inspect the image, localize garment instances or garment parts, infer the category token from visual evidence and training examples, and attach the fine-grained attribute tokens that apply to that localized instance.
> Files
> train.csv - training images with answer ledgers.
> test.csv - held-out images requiring predicted ledgers.
> sample_submission.csv - valid submission format with a weak visual prior.
> categories.csv - allowed anonymized garment category tokens.
> attributes.csv - allowed anonymized localized attribute tokens.
> images/ - anonymized JPEG files referenced by image_path.
> train.csv contains 834 rows. test.csv and sample_submission.csv contain 324 rows.
> train.csv columns:
> id - anonymized row id.
> image_path - path to the anonymized JPEG image.
> width - image width in pixels.
> height - image height in pixels.
> target_json - answer JSON for the training row.
> test.csv columns:
> id - anonymized row id.
> image_path - path to the anonymized JPEG image.
> width - image width in pixels.
> height - image height in pixels.
> Submission Format
> Submit a CSV with exactly these columns:
> id
> prediction_json
> Column order does not matter. Row order does not matter. The ids must exactly match test.csv.
> Example:
> id,prediction_json
> glvp_0123456789abcdef,"{""instances"":[{""category"":""garment_0123abcd45"",""bbox"":[0.247,0.112,0.315,0.506],""attributes"":[""attr_1111aaaa22"",""attr_3333bbbb44""]}]}"
> JSON Schema
> prediction_json must be a JSON object with exactly one key, instances.
> {
> "instances": [
> {
> "category": "garment_0123abcd45",
> "bbox": [0.247, 0.112, 0.315, 0.506],
> "attributes": ["attr_1111aaaa22", "attr_3333bbbb44"]
> }
> ]
> }
> Rules:
> instances is a list with at most 80 entries.
> Each instance object has exactly category, bbox, and attributes.
> category must exactly match one anonymized token in categories.csv.
> bbox is normalized [x, y, width, height], where all values are finite numbers in [0, 1], width and height are positive, and the box stays inside the image frame.
> attributes is a list of unique strings, each exactly matching one anonymized token in attributes.csv.
> Use an empty list for attributes only when no localized attribute token is supported for that predicted instance.
> Evaluation
> The grader parses each row, validates ids, columns, JSON schema, normalized geometry, and allowed garment tokens, then scores each image with order-insensitive instance matching.
> For a predicted instance p and ground-truth instance g:
> IoU(p,g) is the intersection-over-union of the normalized boxes.
> Category(p,g) = 1 if the category strings are identical, otherwise 0.
> AttrF1(p,g) = 1 when both attribute sets are empty; 0 when only one set is empty; otherwise 2 * |attributes_p intersect attributes_g| / (|attributes_p| + |attributes_g|).
> PairScore(p,g) = 0.50 * IoU(p,g) + 0.25 * Category(p,g) + 0.25 * AttrF1(p,g).
> For each image, all predicted/ground-truth pairs are sorted by PairScore; pairs are greedily accepted while neither instance has already been matched. The image score is:
> sum(accepted PairScore values) / max(number of predicted instances, number of ground-truth instances)
> The final score is the mean image score over all test rows. The score is maximized, with theoretical minimum 0 and theoretical maximum 1.
> Malformed submissions, duplicate ids, missing ids, extra columns, missing columns, invalid JSON, out-of-range boxes, invalid categories, or invalid attribute tokens raise an error instead of receiving a numeric score.
> What Not To Use
> Do not use private files, answer files, hidden metadata, hardcoded id-to-answer maps, filename-based lookup tables, or any file outside the released public challenge files.
> Do not use external datasets, challenge-specific fine-tuned checkpoints, private/gated assets, hosted inference APIs, remote-code loaders, or internet lookups during scoring.

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Cross-Variety Grape-Bunch Detection in Vineyard Imagery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77zbc7569hc0b4kmqfmr0mt58bkrnw
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Given a field photograph of a grapevine canopy, detect every grape bunch and return an axis-aligned bounding box with a confidence score. There is a single object class (grape bunch, 0). The catch is generalisation: the test images are a grape variety that never appears in training.
> Two things make this hard:
> Occlusion and soft extent. Bunches hang amid leaves, canes and wires, are often partly hidden, and hang in adjacent clusters. Recall depends on finding partly-occluded bunches and separating neighbours, and because the boundary between fruit and foliage is visually soft, tight localisation is genuinely difficult — the score averages Average Precision over IoU thresholds 0.50–0.95, so loose boxes fall out at the higher thresholds.
> A held-out grape variety. The training and test images are different cultivars. Bunch colour, size, compactness and the surrounding canopy differ from one variety to another, so a detector tuned to the training varieties' look transfers imperfectly. Robust bunch features, not memorised appearance, are what carry over.
> Some training images are bunchless canopy (no boxes); use them as hard negatives to avoid hallucinating fruit.
> Data
> train.csv, test.csv, train_labels.csv, and sample_submission.csv are UTF-8 CSV with a header. Images are JPEG files named <item_id>.jpg.
> train_images/ + train.csv + train_labels.csv
> train_images/<item_id>.jpg — the training images.
> train.csv — item_id, width, height for every train image.
> train_labels.csv — the gold boxes, one row per bunch: item_id, class, x1, y1, x2, y2. Corners are pixel coordinates; class is always 0. Images with no rows are bunchless (negative) canopy.
> test_images/ + test.csv
> test_images/<item_id>.jpg — the images to detect on (the held-out variety).
> test.csv — item_id, width, height for every test image. Gold boxes are withheld.
> sample_submission.csv
> item_id,class,x1,y1,x2,y2,score
> gb_1a2b3c4d5e6f,0,712.0,455.0,880.0,631.0,0.3
> A weak baseline that places one mean-size box at the image centre — it scores near zero.
> metadata.json
> Keys task, columns, submission_columns, submission_note, metric, files. Informational.
> Task
> For each test image, output every grape bunch you detect as an axis-aligned box with a confidence score.
> Evaluation
> Mean Average Precision (mAP) over IoU thresholds 0.50–0.95 (step 0.05), in [0, 1], higher is better. For each threshold, predictions are matched greedily to gold boxes by descending score (one prediction per gold box); AP is the area under the precision–recall curve, and the ten thresholds are averaged. There is a single class.
> Submission format
> A UTF-8 CSV with a header and exactly these columns, in order:
> item_id,class,x1,y1,x2,y2,score
> item_id — string; a test image id.
> class — integer 0 (the only class).
> x1,y1,x2,y2 — numbers; the box corners in pixels.
> score — number in [0, 1]; detection confidence.
> Requirements (violations rejected as invalid): exactly the columns above; only known test item_ids; numeric coordinates; class equal to 0; at most 2000 boxes per image. An image with no predicted rows earns no detections there.
> Allowed
> Any approach: any detector (one- or two-stage), dense/crowd heads, tiling, or test-time strategies, trained on the provided images. ImageNet/COCO-pretrained backbones are fine. Everything must run on the provided GPU.
> What Not To Use
> No external detection data or pretrained fruit/bunch detectors — ImageNet/COCO backbones are allowed, but no external grape or fruit datasets, no off-the-shelf fruit detectors, and no external annotations.
> No network access — no downloading data, weights (beyond allowed pretrained backbones already present), or code at run time.
> No attempting to identify or retrieve the source imagery, and no use of any answer/label file.

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Source-Attributed Dual-Channel Detection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7em7rvmg190ts4jp173v6pbs8ayxfy
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: image, segmentation, feature-engineering, Dataset source is visible after the challenge closes.
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> A fixed sensing station overlooks a shared outdoor field of view through two co-registered imaging channels: a primary channel (a conventional color photographic sensor) and a secondary channel (a co-registered sensor that responds to energy emitted by objects rather than light reflected from them). The two channels degrade under opposite conditions — under strong ambient light the primary channel is crisp while the secondary channel loses contrast against a warm background, and under weak ambient light the primary channel collapses to noise while the secondary channel still separates warm foreground objects from a cool scene. Because either channel can be the blind one, a detection is only trustworthy if the system also knows which channel actually carried the evidence for it.
> The task therefore has two coupled parts. For every capture a submission must detect and localize each moving agent with a bounding box and one of six category labels, and for each detection it must also declare an evidence-source belief — a probability distribution over which channel(s) carry legible evidence for that object: channel A only, channel B only, both, or neither. A detection earns credit only when it is both well-localized and correctly attributed to its evidence source; a belief concentrated on the wrong channel (for example, crediting the color channel for an object only the emitted-energy channel could see in the dark) earns no calibration credit for that detection, so its contribution collapses toward zero.
> Each item is one capture delivered as a co-registered pair of frames — one primary-channel frame and one secondary-channel frame of the same field of view, pixel-aligned and identically sized. The task carries two deliberate distribution shifts. First, an ambient-condition shift: training captures are dominated by the strong-light regime while test captures are weighted toward the weak-light regime, and the ambient condition is withheld from the test set. Second, a station shift: the test captures come from sensing stations (and capture sessions) that never appear in training, so a model cannot memorize a fixed background. Agents span a wide size range and the rarer categories are heavily under-represented, so the score is macro-averaged over categories.
> Dataset
> The challenge data is delivered as co-registered primary + secondary channel frame pairs with box-level annotations for training. Images are anonymized, delivered at their native capture resolution (long side ≤ 1280 px), re-encoded to strip all capture metadata, and referenced by relative path. Each training capture is one row; all of its ground-truth boxes — each carrying its category and its evidence-source regime — are packed into a single JSON boxes column.
> Public files
> public/train.csv — training captures, one row per capture, with all ground-truth boxes for that capture in a JSON column. Columns: capture_id, channel_a_path, channel_b_path, station_id, ambient, session_id, boxes.
> public/test.csv — test captures, one row per capture (no boxes, no station/ambient metadata). Columns: capture_id, channel_a_path, channel_b_path, width, height.
> public/sample_submission.csv — a valid, correctly-formatted submission with one constant placeholder detection per test capture. Columns: capture_id, class, score, xmin, ymin, xmax, ymax, e_a, e_b, e_both, e_none.
> public/images/ — the primary and secondary channel frames referenced by channel_a_path and channel_b_path (PNG).
> Private file (organizer only)
> private/answers.csv — ground-truth boxes for the test captures, one row per box. Columns: capture_id, class, xmin, ymin, xmax, ymax, source. Never distributed to solvers.
> Column descriptions
> The public CSVs use the following columns.
> capture_id (string) — unique capture identifier, e.g. img_1f3a9c20b4e5d6a7. Appears exactly once per row in both train.csv and test.csv.
> channel_a_path (string) — relative path to the primary-channel (color) frame, e.g. images/img_1f3a9c20b4e5d6a7_a.png.
> channel_b_path (string) — relative path to the co-registered secondary-channel frame of the same capture, e.g. images/img_1f3a9c20b4e5d6a7_b.png. Same pixel dimensions as the primary frame.
> station_id (string) — anonymized identifier of the sensing station, e.g. stn_3af1c2. Present in train.csv only. Stations are disjoint across splits — every test capture comes from a station not present in training — so it is withheld from test.csv. It identifies the station grouping within the training data (the grouping that the train/test split holds out).
> ambient (string) — ambient-light condition, either strong or weak. Present in train.csv only; withheld from test.csv.
> session_id (string) — anonymized identifier of the capture session a frame came from, e.g. ses_041. Present in train.csv only. All frames sharing a session_id come from one continuous session. Train and test use disjoint sessions (a session_id never spans both splits).
> boxes (string) — present in train.csv only. A JSON-encoded list of the ground-truth boxes in this capture, each box a 6-element list [class, xmin, ymin, xmax, ymax, source] in frame pixel coordinates. A capture always has at least one box.
> width (int) — pixel width of the frames for this item (present in test.csv).
> height (int) — pixel height of the frames for this item (present in test.csv).
> class (int) — the agent category, an integer index 0–5 (used inside train.csv's boxes and in answers.csv). The index-to-category mapping is: 0 = a person travelling on foot, 1 = a rider of a pedal-driven two-wheeler, 2 = a rider of a motor-driven two-wheeler, 3 = a rider of a small personal-mobility device, 4 = a small passenger vehicle, 5 = a large multi-occupant or freight vehicle.
> source (int) — the evidence-source regime of a box, an integer index 0–3 (in train.csv's boxes and in answers.csv): 0 = channel A only, 1 = channel B only, 2 = both channels, 3 = neither channel. Defined by which held-out single-channel reference recognizer recovers the object's category (see Evaluation).
> xmin, ymin, xmax, ymax (number) — pixel coordinates of a box in the delivered frame, with 0 ≤ xmin < xmax ≤ width and 0 ≤ ymin < ymax ≤ height. In train.csv's boxes and in answers.csv these are integers; in a submission they may be integer or fractional (a detector's raw float coordinates are accepted and scored directly — IoU is computed in floating point).
> score (float) — present in a submission (and the sample submission): the confidence of a predicted detection, in [0, 1]. Used to rank detections when computing average precision.
> e_a, e_b, e_both, e_none (float) — a submission's evidence-source belief for a detection: a probability distribution over the four regimes (channel A only, channel B only, both, neither). Non-negative and sum to 1 (a tolerance of ±0.02 is allowed; values are renormalized after the check).
> Data example
> A truncated train.csv row (one capture; each box carries its category and evidence-source regime):
> capture_id,channel_a_path,channel_b_path,station_id,ambient,session_id,boxes
> img_1f3a9c20b4e5d6a7,images/img_1f3a9c20b4e5d6a7_a.png,images/img_1f3a9c20b4e5d6a7_b.png,stn_3af1c2,weak,ses_041,"[[0,182,96,214,171,1],[4,10,120,64,180,2]]"
> Submission Format
> Submit a single CSV named submission.csv with a header row and the following exactly eleven columns, in this set — no more, no fewer:
> capture_id — the test capture the detection belongs to. Must be a capture_id present in test.csv.
> class — the predicted agent category, an integer 0–5.
> score — the detection confidence, a real number in [0, 1]. Used to rank detections when computing average precision.
> xmin, ymin, xmax, ymax — the predicted box in delivered-frame pixel coordinates (integer or fractional), with xmin < xmax and ymin < ymax.
> e_a, e_b, e_both, e_none — the evidence-source belief for this detection: a distribution over the four regimes (channel A only, channel B only, both, neither). Non-negative, sum to 1 (±0.02, renormalized).
> A submission contains zero or more rows per test capture — one row per predicted detection. A capture for which no detection is submitted is simply omitted (this is interpreted as "no detections" for that capture and costs recall). There is no fixed row count. The following are rejected with an error: any row whose capture_id is not a known test capture; any class outside 0–5; any non-numeric, NaN, infinite, negative, or out-of-[0,1] score; any box with xmin ≥ xmax or ymin ≥ ymax, or a non-numeric / NaN / infinite coordinate; any evidence-source values that are negative or do not sum to 1 within tolerance; and any missing required column or unexpected extra column.
> At most 100 detections per capture are scored; if a capture has more, only the 100 highest-score detections for that capture are kept and the rest are dropped before scoring.
> Sample submission (one constant placeholder detection per test capture with a uniform evidence-source belief — every row byte-identical except capture_id):
> capture_id,class,score,xmin,ymin,xmax,ymax,e_a,e_b,e_both,e_none
> img_1f3a9c20b4e5d6a7,0,0.5,10,10,80,80,0.25,0.25,0.25,0.25
> img_77b0e4d1c2a39f88,0,0.5,10,10,80,80,0.25,0.25,0.25,0.25
> Evaluation
> The metric is the Source-Attributed Detection Score (SADS), higher is better. It combines standard detection average precision with an evidence-source calibration term, so a detection earns credit only when it is both well-localized and correctly attributed to its evidence source.
> Evidence-source ground truth. The source regime of a box is defined by running two frozen single-channel reference recognizers — one that sees only the channel-A crop of the box, one that sees only the channel-B crop — and recording which of them recovers the object's true category. A channel is "legible" for that object if its recognizer is correct. The regime is 0 = channel A only, 1 = channel B only, 2 = both, 3 = neither. The reference recognizers are held out and never released; a solver must predict the regime from appearance, not reproduce the recognizer.
> For each object category c with ground-truth boxes (each carrying a true regime z ∈ {0,1,2,3}):
> 1. Localization (average precision). For two boxes, overlap is intersection-over-union IoU(A,B) = area(A∩B) / area(A∪B). Every predicted box of category c across all test captures is sorted by descending score and matched greedily to the highest-IoU not-yet-matched ground-truth box of category c in its capture:
> for each predicted box p of category c (in descending score order):
> find the ground-truth box g of category c in p's capture with the highest IoU
> among not-yet-matched ground-truth boxes
> if such g exists and IoU(p, g) >= IOU_THR:      # IOU_THR = 0.5
> p is a true positive; mark g matched
> else:
> p is a false positive
> AP_c is the area under the precision–recall curve (all-point / VOC-2010 interpolation), recall normalized by the number of ground-truth boxes of category c.
> 2. Evidence-source calibration on true positives. For each true-positive detection i matched to a ground-truth box of regime z_i, with evidence-source belief q_i = [e_a, e_b, e_both, e_none]:
> G_i = 1 - 0.5 * sum_r (q_i[r] - onehot(z_i)[r])^2   # in [0, 1], quadratic (Brier) proper score
> R_c = mean_i G_i over the true positives of category c   # 0 if the category has no true positive
> G_i is a symmetric calibration score over the four evidence-source regimes: a belief concentrated on the correct regime z_i earns G = 1, a uniform belief [0.25, 0.25, 0.25, 0.25] earns G = 0.625, and a belief concentrated on a single wrong regime earns G = 0. A category all of whose true positives place their mass on the wrong regime therefore has R_c = 0.
> 3. Per-category score and aggregation. The average precision is scaled by the mean evidence-source calibration of its true positives (both AP_c and R_c are non-negative):
> s_c = AP_c * R_c
> SADS = mean_over_categories( s_c )                # c = 0..5, every category present in the test set
> SADS = max(0.02, min(1.0, SADS))
> Constants: IOU_THR = 0.5, maximum scored detections per capture MAX_DET_PER_CAPTURE = 100, evidence-source sum tolerance 0.02, score floor 0.02, ceiling 1.0.
> Baseline. A single fixed detection per capture with a uniform evidence-source belief (as in the shipped sample submission) matches almost nothing and scores at the floor (≈ 0.02). A model that localizes the common categories but leaves its evidence-source belief uniform has each category's AP scaled by 0.625; recovering the correct evidence-source regime for each detection lifts that factor toward 1.0, so correct localization and correct evidence-source attribution together are required to approach 1.0. Higher is better.
> What Not To Use (Prohibited Methods)
> This challenge must be solved from the released capture pairs and training annotations alone. The following are prohibited and are grounds for disqualification:
> No external answer keys or source recovery. Do not attempt to identify, download, or match against the original source dataset this challenge was derived from, or any public dual-channel / multi-sensor object-detection dataset, to recover boxes, categories, evidence-source regimes, or capture conditions. Do not match captures, capture_id, station_id, or session_id values, or pixel content back to any external source.
> No id-based or metadata hardcoding. Do not hardcode predictions keyed on capture_id, station_id, or session_id, and do not infer boxes, categories, or evidence-source regimes from filename patterns, file ordering, image dimensions, or any residual capture metadata.
> No train/test leakage. Do not use test captures (or nearby frames of the same session) to fit or tune any model. Capture sessions are disjoint across train and test; do not attempt to bridge them.
> No private-label tuning. Do not tune against private/answers.csv; it is organizer-only and unavailable at solve time.
> No externally-computed annotations, and no model with knowledge of the source data. Do not import pre-computed boxes, category labels, or evidence-source annotations for these specific captures from any external source, and do not use any model that was trained, fine-tuned, or distilled on the original dataset this challenge was derived from (or on any published dual-channel / multi-sensor detection benchmark covering the same captures). Boxes, categories, and evidence-source beliefs must be predicted from the released data, never looked up.
> Permitted (to be explicit): publicly available general-purpose pretrained vision weights — ImageNet- or COCO-pretrained classification backbones, standard detection architectures and their public checkpoints, and general open-vocabulary / zero-shot vision models — used either frozen or fine-tuned on the released public/train.csv split. Fitting a model on the released training annotations is permitted and unrestricted. The prohibition above concerns the provenance of labels, not the use of pretrained weights.
> No manual labeling of the test set. Do not hand-annotate boxes, categories, or evidence-source regimes for test captures.

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Compositional Thermal Detection Across Unseen Time-of-Day and Altitude

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cyadcxcngewrznzjq7fy9fd8a4d2z
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: image, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> This challenge is a test of intensity-invariant compositional generalization on thermal imagery, scored by the worst case. Every frame belongs to one cell of a two-by-two grid -- thermal condition (day or night) crossed with flight altitude (low or high) -- and the grid is split along its diagonal: training holds two opposite cells, and the two remaining cells are held out for evaluation. Each factor value (day, night, low, high) therefore appears in training, but only in the pairings training uses; each test cell is a pairing the model never saw and must compose. On top of that, every frame's intensity (gain and polarity) is randomized, so brightness carries no information. The reported score is the worst of the two held-out cells, so a solution must generalize to BOTH unseen combinations, not just the easier one. No ordinary detection task, and no ordinary single-axis domain-shift task (day-to-night alone, or near-to-far alone), does this; a solution that has merely memorized how each individual factor looks, or that leans on brightness, is built to fail here. The split, the worst-cell scoring, and the rendering ARE the challenge, not incidental preprocessing around a standard benchmark.
> The substrate is heat. Every image is a single-channel long-wave infrared frame captured from a drone: no color, no texture, no visible appearance -- an object exists only as a warm or cold patch against a cluttered thermal background, and must be assigned one of three classes (Person, Car, or Bicycle) from the shape and contrast of that heat signature alone.
> Two factors govern every frame, and thermal appearance depends on both. The first is the thermal condition (day or night): the scene's heat structure changes between them -- at night warm bodies stand out sharply against cool ground, while by day the sun loads heat into pavement and metal so the contrast between an object and its background compresses, inverts, or washes out. The second is flight altitude (low or high), which sets object scale -- at high altitude objects shrink to only a handful of pixels. These two factors form a two-by-two grid, split along its diagonal. Training contains day frames at HIGH altitude and night frames at LOW altitude. The two opposite cells are held out for testing: day frames at LOW altitude, and night frames at HIGH altitude. Every factor value is thus present in training -- day (seen high up), night (seen low down), low altitude (seen at night), high altitude (seen by day) -- but each test cell is a pairing the model never trained on, so it must compose day appearance with a scale it saw only at night, and night appearance with a scale it saw only by day. Performance is measured on the weaker of these two held-out cells.
> On top of this, the intensity mapping of every frame is randomized, in two ways, independently per frame and in both training and test. First, gain: as a thermal camera's automatic gain control would, each frame is given its own contrast and brightness setting, so the same physical temperature maps to different pixel values from frame to frame. Second, polarity: thermal imagery can be shown white-hot (warm is bright) or black-hot (warm is dark), and each frame is independently assigned one or the other. Together these make absolute pixel value meaningless -- a warm body is bright here, dark there, high-contrast in one frame and faint in the next -- so a detector cannot lean on brightness at all and must key on shape and local contrast structure. Because the same randomization is present throughout training, this is an invariance a model can and must learn, not a surprise sprung only at test time.
> This is why standard recipes do not transfer. A detector tuned for invariance to a single day-night shift, or a single altitude shift, has never been asked to combine a specific pair of factor values it never encountered jointly; and one that has quietly learned a brightness or contrast shortcut is defeated by the per-frame gain and polarity randomization. Two further properties sharpen the difficulty: the objects are small -- at high altitude often only a handful of pixels -- frequently clustered and partially occluded, so localization is delicate; and telling a person from a bicycle from a car by bare thermal shape is itself error-prone.
> You are given training images with ground-truth boxes, each labeled with one of three classes (Person, Car, Bicycle), and test images with no labels. Predict, per test image, a set of boxes with a class and a confidence score. Every image is an independent still frame -- no video, tracking, or temporal information is provided or may be used.
> Dataset
> The data is a collection of real thermal (long-wave infrared) aerial images captured from a drone over outdoor scenes. Every object of interest is annotated by an axis-aligned bounding box and a class label. The split is factorial over two factors, time of day and flight altitude: training is the {day-high, night-low} diagonal of the two-by-two grid, and the test images are the opposite diagonal -- day-time low-altitude frames and night-time high-altitude frames -- held out of training entirely, while each factor value still appears in training on its own. The test set mixes the two held-out cells; you are not told which test image belongs to which cell. No frame is shared between train and test.
> There are three object classes, encoded as integers:
> 0 = Person
> 1 = Car
> 2 = Bicycle
> Files:
> train_images/ : a folder of JPEG thermal images, one per training frame, named  .jpg where   is an opaque image identifier. Images are single-channel (grayscale) thermal frames.
> train_annotations.csv : one row per training image. Columns:
> id (string): opaque image id, matching the file train_images/ .jpg.
> width (integer), height (integer): pixel dimensions of that image.
> boxes (string): every ground-truth box in that image, as a ";"-separated list, each box written as five space-separated values "cls x1 y1 x2 y2" -- the integer class followed by the top-left and bottom-right pixel corners (x to the right, y downward). An image with no objects has an empty boxes value.
> test_images/ : a folder of JPEG thermal test images, named  .jpg.
> test.csv : one row per test image, with columns id, width, height (no boxes).
> sample_submission.csv : a valid, low-information entry that scores near the floor and only shows the required format.
> Submission Format
> Submit a CSV with exactly two columns, in any order:
> id : one row per test image, matching the ids in test.csv (every test id present, none added, no duplicates).
> predictions : that image's predicted boxes as a ";"-separated list, each box written as six space-separated numbers "cls x1 y1 x2 y2 score" -- the integer class (0, 1, or 2), the pixel corners, and a real-valued confidence (higher = more confident; the scale is arbitrary, only the ordering matters). Predict no boxes for an image by leaving its predictions value empty.
> Example entry (coordinates illustrative only):
> id,predictions
> 000701c34b2c0def,0 312 240 326 268 0.95;1 90 380 168 430 0.80
> 00589a5f9cd22f6b,
> An entry is rejected before scoring if it has a missing column, duplicate ids, an id set that does not match test.csv, or any predictions cell that is present but not parseable as groups of six finite numbers.
> Evaluation
> Submissions are scored by the WORST held-out cell. The test images come from two held-out cells of the factorial grid (day-time low-altitude, and night-time high-altitude). For each cell separately we compute a COCO-style mean Average Precision: for each of the three classes, Average Precision averaged over ten IoU thresholds from 0.50 to 0.95 in steps of 0.05 (at most 100 detections per image per class), then averaged across the classes present in that cell. The reported score is the MINIMUM of the two cell values -- so a submission is only as good as its weaker held-out combination, and doing well on one cell while failing the other scores near the floor.
> Within a cell, for a given class and IoU threshold, detections of that class across the cell's images are ranked by confidence. Walking down that ranking, each detection is matched to an as-yet-unmatched ground-truth box of the same class in the same image if their intersection-over-union meets the threshold (a true positive); otherwise it is a false positive. From the running true/false-positive counts a precision-recall curve is formed and its 101-point interpolated area is the Average Precision at that threshold. Averaging over thresholds gives the class AP; averaging the class APs gives the cell mAP; the minimum over the two cells, floored at 0.001, is the reported score (higher is better).
> Formally, let K be the two held-out cells, C = {Person, Car, Bicycle}, T = {0.50, 0.55, ..., 0.95} the ten IoU thresholds, and R = {0.00, 0.01, ..., 1.00} the 101 recall points. For cell k, class c and threshold t, let p_{k,c,t}(r) be the precision at recall r on that cell-and-class precision-recall curve. Then:
> p_hat_{k,c,t}(r) = max over r' >= r of p_{k,c,t}(r)
> (interpolated precision; 0 if recall r is unattained)
> AP_{k,c,t}       = (1 / 101) * sum over r in R of p_hat_{k,c,t}(r)
> (Average Precision at one threshold)
> AP_{k,c}         = (1 / 10)  * sum over t in T of AP_{k,c,t}
> (class AP over the ten IoU thresholds)
> mAP_k            = (1 / 3)   * sum over c in C of AP_{k,c}
> (cell mAP over the three classes)
> score            = max(0.001, min over k in K of mAP_k)
> (worst-cell value, floored at 0.001)
> At most 100 detections per image per class are counted; any beyond that are discarded before ranking.
> This metric rewards finding objects (recall), not inventing them (precision), assigning the right class, and drawing tight boxes -- in BOTH held-out cells. There is no fixed output that scores above the floor: emitting nothing gives zero recall, and flooding images with guesses collapses precision, so both score near zero in every cell and the minimum stays at the floor. Only genuine, well-ranked, well-localized, correctly-classified detections in the weaker cell raise the score.
> What Not To Do
> Do not use any external image dataset, nor any labels, annotations, or metadata beyond what is provided here. In particular, do not attempt to identify the source of these images or reverse-image-search a test image to recover its annotations from any external collection. Grading is offline; this is on the honor system.
> Model eligibility. You may use only general-purpose pretrained backbones or detectors -- specifically, weights pretrained on generic image-classification or generic object-detection corpora such as ImageNet or COCO, downloaded through an installed package. Weights that were pretrained OR fine-tuned on any thermal, infrared, aerial, or UAV object-detection dataset are NOT allowed, because they would encode this task's distribution and give an uneven advantage. Whatever backbone you start from, you must train or fine-tune your own model on the provided training data; a pretrained model applied with no fitting to this data is not an acceptable solution.
> Do not use the image id, file name, file order, or any per-file artifact as a feature; ids are opaque and carry no information about content or labels.
> Do not treat the frames as video: there is no temporal ordering, tracking, or cross-image association to exploit, and the test images come from two factor combinations (day-time low-altitude, and night-time high-altitude) held out of training. Do not try to infer which held-out cell a test image belongs to and special-case it; detect each image independently from its own pixels.

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Dual-Channel Withheld-Condition Object Localization

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fqsch5njpnvrhdvavcd4wys8bj6md
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat hoang_phuc_6868's score of 0.395!

Full challenge description from page:

> Overview
> An overhead sensing platform surveys a ground scene from a fixed sequence of observation conditions. At each condition it captures a co-registered pair of frames: a primary channel (a conventional colour photographic sensor) and a secondary channel (a sensor responding to energy emitted by objects rather than light reflected from them). A downstream system does not consume the frames directly — it consumes a scene ledger, the structured inventory of what is present: for every object, its broad type, where its footprint sits in the frame, how large that footprint is, and which way the object is oriented. A ledger is judged as a set, so an object left out costs as much as one invented.
> Each record releases the frames captured at three observation conditions — 0, 20 and 40 — and asks for the ledger at one further condition that is never shown. The withheld condition is not the same for every record: it is one of 10, 30 or 50, it varies from record to record, and the value that applies to a given record is stated in that record's missing_condition column in both train.csv and test.csv. A record therefore releases six frames (three conditions x two channels) and asks for the ledger belonging to a seventh, unreleased configuration — the particular one named by its own missing_condition.
> Because the sensing geometry changes between conditions, an object's footprint at the withheld condition sits somewhere other than where it appeared in any released frame, and its apparent size and orientation change with it. The displacement is a property of the sensing geometry rather than of any individual object, and applies coherently to a whole scene at once.
> Scenes are cluttered and unevenly populated. A scene holds between one and fourteen objects, the type mix is heavily imbalanced — the most common type outnumbers the rarest by more than fifty to one — and objects are small relative to the frame, with a median footprint about a twentieth of the frame's shorter side. Orientation is reported per object, not per scene. Scenes are disjoint between the training and test splits, so no test scene appears in training under any condition.
> Dataset
> Each record is one scene. The released frames are anonymized, re-encoded to strip capture metadata, and referenced by relative path. Ledgers are given for training records only.
> Public files
> public/train.csv — 1490 training records, one row per scene, with the target ledger in a JSON column. Columns: id, observations, missing_condition, entity_ledger.
> public/test.csv — 395 test records, one row per scene, with no ledger. Columns: id, observations, missing_condition.
> public/frames/ — the JPEG frames referenced by observations. Six per record: three observation conditions x two channels.
> public/sample_submission.csv — a valid, correctly-formatted submission carrying one constant placeholder entry per test record. Columns: id, entity_ledger.
> Private file (organizer only)
> private/answers.csv — the target ledgers for the 395 test records, together with the aggregation bands used for scoring. Columns: id, missing_condition, density_band, entity_ledger. Never distributed to solvers.
> Column descriptions
> The public CSVs use the following columns.
> id (string) — unique record identifier, e.g. item_4f2a91c07b3e8d65. Appears exactly once per row in both train.csv and test.csv.
> observations (JSON string) — a mapping from released observation condition ("0", "20", "40") to that condition's two frame paths, under the keys channel_a (primary channel) and channel_b (secondary channel). Both frames of a condition are the same size and cover the same field of view.
> missing_condition (integer) — the single observation condition withheld for THIS record, and whose ledger is the prediction target. One of 10, 30 or 50; it varies from record to record, so it must be read per row rather than assumed constant. No frame is released at this condition. Present in both train.csv and test.csv.
> entity_ledger (JSON string) — present in train.csv only. The target ledger at the withheld condition: an unordered JSON list of 1 to 14 entries, each with the six fields below. Every record has at least one entry.
> entity_type (integer) — the broad object category of an entry, an index 0–11. Categories are anonymized; no external meaning is attached to the index.
> cx (float) — footprint centre on the horizontal axis, normalized to [0, 1] of frame width.
> cy (float) — footprint centre on the vertical axis, normalized to [0, 1] of frame height.
> span_x (float) — footprint width, normalized to (0, 1] of frame width.
> span_y (float) — footprint height, normalized to (0, 1] of frame height.
> bearing_deg (float) — footprint orientation in degrees, in [-180, 180].
> density_band (string) — present in private/answers.csv only. The target-ledger size band used for macro-averaging: low (1–3 entries), medium (4–6), or high (7 or more). Withheld from solvers.
> Data example
> A truncated train.csv row (one scene; frame paths shortened for display):
> id,observations,missing_condition,entity_ledger
> item_4f2a91c07b3e8d65,"{""0"":{""channel_a"":""frames/img_a1b2.jpg"",""channel_b"":""frames/img_c3d4.jpg""},""20"":{...},""40"":{...}}",30,"[{""entity_type"":2,""cx"":0.311,""cy"":0.482,""span_x"":0.041,""span_y"":0.037,""bearing_deg"":-12.5}]"
> Submission format
> Submit a single UTF-8 CSV named submission.csv with a header row and exactly two columns — no more, no fewer:
> id — the test record the ledger belongs to. Must be an id present in test.csv.
> entity_ledger — a JSON list of at most 14 entries predicted for that record's withheld condition. Although every ground-truth ledger holds at least one entry, a prediction is not required to: an empty list [] is an accepted prediction (scored as predicting no objects, see below).
> Exactly one row per test record. Every entry must have exactly the six keys entity_type, cx, cy, span_x, span_y, bearing_deg. entity_type must be an integer 0–11; cx, cy, span_x and span_y must be finite values in [0, 1] with the two spans strictly positive; bearing_deg must be finite and in [-180, 180]. An empty list [] is valid and is scored as predicting no objects.
> The following are rejected with an error: a missing, duplicate, empty or unknown id; a missing or extra column; an entity_ledger that is blank, is not valid JSON, is not a list, or holds more than 14 entries; an entry with missing, extra or misspelled keys; a non-integer or out-of-range entity_type; and any non-numeric, NaN, infinite or out-of-range coordinate, span or bearing.
> Sample submission (one constant placeholder entry per test record — every row byte-identical except id):
> id,entity_ledger
> item_4f2a91c07b3e8d65,"[{""entity_type"":0,""cx"":0.5,""cy"":0.5,""span_x"":0.05,""span_y"":0.05,""bearing_deg"":0.0}]"
> item_88b0e4d1c2a39f77,"[{""entity_type"":0,""cx"":0.5,""cy"":0.5,""span_x"":0.05,""span_y"":0.05,""bearing_deg"":0.0}]"
> Evaluation
> The metric is the Latent Ledger Recovery Score (LLRS), higher is better, bounded to [0.02, 1.00].
> Footprints are compared as axis-aligned boxes derived from their centre and spans, clipped to the frame: [cx - span_x/2, cx + span_x/2] x [cy - span_y/2, cy + span_y/2]. Overlap is intersection-over-union.
> Within a record, predicted and reference entries of the same entity_type are matched one-to-one, greedily in descending IoU order; a pair may only match if its IoU is at least IOU_THRESHOLD = 0.30. Each matched pair earns its IoU discounted by the circular difference between the predicted and reference bearing:
> bearing_credit = 1.0 - 0.25 * min(abs(pred_bearing - ref_bearing),
> 360 - abs(pred_bearing - ref_bearing)) / 180
> # bearing_credit lies in [0.75, 1.0]: an exact bearing costs nothing,
> # a fully reversed bearing costs a quarter of the pair's credit.
> spatial_fidelity = sum(iou(pred, ref) * bearing_credit for pred, ref in matches)
> spatial_fidelity /= max(1, len(reference))
> omission_rate    = (len(reference) - len(matches)) / max(1, len(reference))
> unsupported_rate = (len(prediction) - len(matches)) / max(1, len(prediction))
> record_score = max(0.0, spatial_fidelity
> - 0.45 * omission_rate
> - 0.30 * unsupported_rate)
> Record scores are macro-averaged twice: once over the three values of missing_condition (records are grouped by the condition withheld from them), and once over the three private target-density bands (low, medium, high). The final score is the harmonic mean of the two macro-averages, so a solver that is strong at one withheld condition or one density band but weak at another cannot average its way to a high score:
> score = 2 * condition_macro * density_macro / max(1e-12, condition_macro + density_macro)
> score = max(0.02, min(1.00, score))
> Constants: IoU match threshold 0.30, omission penalty weight 0.45, unsupported penalty weight 0.30, bearing penalty weight 0.25, maximum entries per record 14, score floor 0.02, score ceiling 1.00. The floor is a reporting clamp applied after the metric is computed; the metric's own minimum is 0.
> Baseline. A constant single placeholder entry repeated on every record, as in the shipped sample submission, almost never reaches the IoU match threshold against a real entry and scores at the floor (0.02). Predicting an empty ledger for every record likewise scores at the floor. Higher is better.
> What Not To Use (Prohibited Methods)
> This challenge must be solved from the released frames and training ledgers alone. The following are prohibited and are grounds for disqualification:
> No external answer keys or source recovery. Do not attempt to identify, download, or match against the original source release this challenge was derived from, or against any public multi-view or multi-sensor aerial object-detection archive, in order to recover ledgers, footprints, types, bearings, or the frames at withheld conditions. Do not match record ids, frame filenames, or pixel content back to any external archive.
> No frames from the withheld condition. The task is to produce a ledger for an observation condition whose frames are not released. Do not obtain, reconstruct from an external archive, or otherwise import imagery captured at a record's missing_condition.
> No id-based or metadata hardcoding. Do not hardcode predictions keyed on id, and do not infer footprints, types, or bearings from filename patterns, file ordering, row ordering, or any residual capture metadata.
> No train/test leakage. Scenes are disjoint across the splits; do not attempt to bridge them, and do not use test records to fit or tune any model.
> No private-label tuning. Do not tune against private/answers.csv or against leaderboard feedback; the answers file is organizer-only and unavailable at solve time.
> No manual labelling of the test set. Do not hand-annotate footprints, types, or bearings for test records, and do not use external scene-description files, replay records, or scene-generation tooling to reconstruct a target ledger.
> Permitted (to be explicit): publicly available general-purpose pretrained vision weights — ImageNet- or COCO-pretrained classification backbones, standard detection architectures and their public checkpoints, and general open-vocabulary or zero-shot vision models — used either frozen or fine-tuned on the released public/train.csv split. Fitting a model on the released training ledgers is permitted and unrestricted. The prohibitions above concern the provenance of the target ledgers, not the use of pretrained weights.

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Localizing Overlapping Sounds from Sparse Labels

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx728gpe4p20b1rrwjhvfcdajh8ah2wm
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat komilpamar's score of 0.209!

Full challenge description from page:

> Localizing Overlapping Sounds from Sparse Labels
> Overview
> At dawn in a temperate forest, dozens of birds sing at once. An ecologist who wants to know which animals were present, how often they called, and how they partitioned the acoustic space has to draw a box around every vocalization on the spectrogram: when it began, when it ended, and the band of frequencies it occupied. Doing that by hand, for the hundreds of hours a modern acoustic survey produces, is impossible. Doing it by machine requires boxes to learn from, and nobody has them, because drawing them is the very thing that does not scale.
> This challenge poses the problem as it actually presents itself in the field.
> Almost none of your training data has boxes. Of the 1,530 training windows, only 120 come with their boxes drawn in, 828 boxes across those 120 windows. The other 1,410 windows arrive with a single number attached: how many vocalizations that window contains. Not where they are, not how long they last, not what band they cover. Just the count.
> Those two kinds of label do different work, and you need both. The handful of drawn boxes is the only place you can see what a vocalization actually is: how long a call lasts, how wide a band it spans, where in the spectrum it sits. The 1,410 counts are the only thing that can tell you how many sounds are really there in a spectrogram that a naive threshold would happily carve into forty pieces. Neither alone is enough.
> And the sounds overlap. In a chorus this dense, 78% of the annotated vocalizations overlap another one in time. Two birds singing at the same instant are not separable on a timeline at all: they are separable only because they occupy different frequency bands. That is why the answer is a rectangle in the time-frequency plane and not an interval. Anything that reduces the problem to "when did something sing" collapses two birds into one and cannot recover.
> And the test is a different season. Every training window comes from recordings made in late April and May. The test windows come from a morning in July, when the chorus has changed: of the 26 species heard in the test recording, 7 are never heard in training at all. A detector that memorised the songs it was shown will miss them.
> Task
> For each ten-second audio window in the test set, output one box per bird vocalization you find: its start and end in seconds, the lowest and highest frequency it reaches in Hz, and a confidence score.
> Data
> All inputs are under dataset/public/:
> train/<window_id>.wav: 1,530 ten-second windows of dawn-chorus audio (22,050 Hz, mono, 16-bit). Readable with scipy.io.wavfile or the standard library wave module.
> train_boxes.csv: the drawn boxes, for 120 training windows only. Columns window_id, begin_s, end_s, low_hz, high_hz. 828 vocalizations in total. This is everything you get to see of what a bird sound looks like.
> train_counts.csv: a count for every training window, the 120 labelled ones included. Columns:
> window_id (string): the window. The audio is train/<window_id>.wav.
> n_vocalizations (int): how many bird vocalizations that window contains, from 0 to 18. Where they are is not stated. Behind these counts stand 10,289 vocalizations, and you see the boxes of 828 of them.
> test/<window_id>.wav: 779 ten-second windows to localize, from a July recording.
> test_windows.csv: columns window_id, duration_s (10.0), sample_rate (22050).
> sample_submission.csv: a correctly formatted example for every test window. Its baseline puts one box over the whole window and the whole band, which is valid and scores about 0.
> The reference boxes for the test windows are held out privately and used only for scoring. There are 5,707 of them, a mean of 7.3 per window.
> Evaluation
> Predictions are scored by average precision at an IoU of 0.2, computed in the time-frequency plane.
> A predicted box is a rectangle: (begin_s, end_s) by (low_hz, high_hz). It matches a reference vocalization when their intersection-over-union is at least 0.2. Both axes are normalized by the window, 10 seconds and 11,025 Hz, so a second and 1,102 Hz count for the same amount and neither unit dominates the overlap. Predictions are ranked by score across the whole test set, matched greedily to the still-unmatched reference boxes of the same window, and integrated into all-point-interpolated average precision.
> score = AP@0.2 over the time-frequency plane        (higher is better, range 0 to 1)
> The threshold is low on purpose. A detector that finds a sound but draws it thirty percent too wide has found the sound, and in a chorus this dense the reference edges are a judgement call even for the expert who made them. Measured on this split: a method that knew the exact centre of every vocalization and drew one learned box size around it would score only 0.14 at an IoU of 0.5, and 0.71 at 0.2. At the stricter threshold the metric stops measuring whether the sound was found and starts measuring agreement with one annotator's edges.
> For orientation, on this test set:
> the placeholder scores 0.00
> a classical energy-blob detector that ignores every label scores 0.25
> the same detector, with its blobs reshaped toward the median box in train_boxes.csv, scores 0.35
> a method with perfect centres and one learned box size would score 0.71
> The reference solution is the third of these. Everything above it has to come from the counts.
> Submission format
> Write ./working/submission.csv with exactly these columns:
> window_id,begin_s,end_s,low_hz,high_hz,score
> w_1a2b3c4d5e6f7a_03,1.42,2.06,3120.0,5480.0,0.91
> w_1a2b3c4d5e6f7a_03,4.88,5.31,880.0,1720.0,0.67
> ...
> As many rows per window_id as you like, including none.
> begin_s and end_s in seconds from the start of the window, inside [0, 10], with end_s > begin_s.
> low_hz and high_hz in Hz, inside [0, 11025], with high_hz > low_hz.
> score is your confidence, in [0, 1]. It only affects the ranking, so any monotone scale works.
> A malformed submission is rejected: a box outside its window, a box with no extent, a NaN, an unknown window_id, or a score outside [0, 1].
> Constraints
> Read the challenge inputs only from ./dataset/public/. Write your output only to ./working/submission.csv.
> One A10G GPU (24 GB), plus 10 CPU cores and 62 GB of memory, and a hard limit of 1.5 hours for the whole run. The windows are short, so a detector trained on the raw audio fits comfortably in that budget; the reference itself finishes in about 30 seconds, leaving plenty of room to train.
> Train from scratch. No pretrained weights of any kind. Do not download a checkpoint from a model hub and do not initialise from anything trained elsewhere. Every parameter you use must be fitted on the provided training windows. A bird-sound recogniser pretrained on a large public collection would turn this localization into a lookup, so pretrained audio models are not allowed; building the detector from the boxes and counts you are given is the point.
> No package installs (no pip or conda install). You may use the preinstalled libraries (numpy, scipy, pandas, scikit-learn, pytorch, and so on). Note that no audio-decoding library is guaranteed to be present, which is why the audio is plain 16-bit WAV that scipy.io.wavfile and the standard library wave module read with no dependency at all.
> What Not To Use
> Do not retrieve this challenge's source recordings or their annotations from the public internet in order to recover the reference boxes. Localize only from the audio you are given.
> Do not hardcode outputs or otherwise bypass learning from the data.
> A learning approach is expected, and the two label types pull in different directions. The 828 drawn boxes are enough to learn what a vocalization looks like, and far too few to learn a detector: train on them alone and you will overfit to 120 windows of April. The 1,410 counts cover the whole training set but say nothing about location, so they cannot be trained on directly. Pseudo-labelling the counted windows with a detector bootstrapped from the boxes, calibrating a peak-finder so that the number of boxes it emits matches the counts it was given, or a model that predicts a count and is made to point at what it is counting, are all in the spirit of the task.

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Fastener Take-Off from Degraded Shop Drawings

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71em2sje8qef5eb49yqx5j5n8a4hp4
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat singhking's score of 0.685!

Full challenge description from page:

> Overview
> You are given scanned mechanical shop drawings and must read off, sheet by sheet, the small hardware marks they carry -- the bolts, nuts, screws, washers and weld flags -- reporting for each mark where it sits and which of the five it is. This supports a "take-off": before parts are ordered or an assembly is audited, an estimator tallies every piece of hardware a drawing calls out. The catch is that the sheets are old -- photocopied and rescanned, so faint, speckled and skewed -- and each mark is only a few pixels across, sitting among dimension lines, leader lines, hatching and notes. The core difficulty is robustness: pulling the small, low-contrast marks out of a noisy, cluttered sheet.
> Concretely this is a visual localization task -- an image goes in, and a set of positioned, labeled boxes comes out. The signal a model must learn is the shape and typical placement of each tiny mark and how that shape survives scan degradation; the output is one box per mark together with its hardware category, one of bolt, nut, screw, washer, weld. It is not whole-image classification and not tabular feature analysis: the answer lives in where the marks are and what they are, at small scale, under noise.
> What makes this its own regime is that the sheets are fully synthetic and procedurally generated for the challenge. That turns difficulty into a controllable variable -- the degree of scan degradation and clutter is set by the generator, not inherited from one fixed scrape of real drawings -- so the benchmark measures degradation-robust take-off rather than performance on a single particular collection. Ground truth is machine-exact, and the generator (Pillow + numpy) ships with the data, so the regime is fully documented and reproducible.
> Relation to prior work
> Reading small graphical marks off scanned technical drawings is an established line of research -- for example SiED (Symbols in Engineering Drawings, Elyan et al. 2020) and related drawing-digitization work. This challenge deliberately adapts that line into a new regime along three axes. First, the data is a controllable synthetic generator with dialable scan degradation and clutter, so it is a robustness benchmark rather than a fixed symbol library. Second, the target is mechanical fastener and joint hardware for a quantity take-off (procurement and estimating), not general piping, electrical or architectural symbol vocabularies. Third, because the marks are only pixels across, scoring is by point localisation and counting rather than pixel-tight boxes. The prior line supplies the recognition methods; the synthetic-degradation take-off regime is what is new here.
> The sheets and marks
> Each synthetic sheet is composed like a real mechanical drawing: orthographic views, a section cut with hatching, dimension and leader lines, a parts table and a title block. Into this the generator places the five kinds of hardware mark at known positions, then applies scan-like degradation (blur, speckle noise, contrast shift) and dense occluding lines. Because generation is procedural, every mark has a pixel-accurate box and a category with no annotation noise, licensing risk or leakage.
> The five hardware marks are:
> bolt -- a hex bolt drawn from the side (head plus threaded shaft)
> nut -- a hex nut seen from the top
> screw -- a socket-head cap screw seen from the top
> washer -- a flat washer (an annulus)
> weld -- a fillet weld flag
> The difficulty
> The task is deliberately hard, and the ceiling is well below a perfect score. The marks are tiny -- only a few pixels across -- and they sit amid a dense field of drawing lines, dimension text and hatching, all under photocopy-style blur and noise that lowers their contrast. Several kinds are easy to confuse at that scale: a top-view nut, a washer and a socket screw are all small and roughly circular once blurred. A model picks up real signal -- the distinctive shapes of the marks and their typical placement on a sheet -- and so scores clearly above a blind baseline, but small size, degradation and inter-class similarity keep the achievable score well short of 1.
> Example
> Three real marks from a training sheet, one box each (corners in pixels):
> image_id: im_00042, category: bolt, box: [612, 331, 640, 352] -- a side-view bolt on the fastener schedule
> image_id: im_00042, category: nut, box: [210, 455, 231, 476] -- a hex nut on the flange bolt circle
> image_id: im_00087, category: weld, box: [502, 620, 548, 642] -- a fillet weld flag on a welded joint
> The marks are only a few pixels across and share the sheet with dense clutter and scan noise, which is what makes them hard to find.
> Evaluation
> Because the marks are only a few pixels across, boxes are matched to ground-truth marks not by pixel-tight overlap but by CENTRE DISTANCE: a predicted box matches a mark of the same kind on the same sheet when their centres are within 15 pixels. The score blends three factors, each macro-averaged over the five hardware kinds:
> find -- Average Precision under centre-distance matching: did you locate the marks?
> place -- centring quality of the true positives: how close to the mark centre your boxes land (1 at the exact centre, down to 0 at the tolerance).
> tally -- count agreement: per kind, how close the number of confident detections that actually land on a real mark (true positives) per sheet is to the true count (the take-off tally). A confident box that does not land on a real mark earns nothing, so the count cannot be guessed.
> The final score is 0.45 times find plus 0.25 times place plus 0.30 times tally, between 0 and 1, higher is better. Because localisation is by centre, the difficulty comes from confusing the small round kinds (nut, washer, screw) and from marks missed entirely, so the maximum achievable value stays well below 1, while blind or constant-count submissions score near 0.
> Precisely, the grader works one hardware kind and one sheet at a time. Predictions of that kind are ranked by confidence from high to low. Each prediction is matched to the nearest not-yet-used ground-truth mark of the same kind on the same sheet, using the distance between box centres; it is a true positive if that centre distance is at most 15 pixels, otherwise a false positive. From this ranking, find is the 101-point interpolated Average Precision (a precision-recall summary). place is the average, over the true positives, of one minus the centre distance divided by 15 (so a box exactly on a mark scores 1, one at the tolerance scores 0). For tally, only confident predictions (confidence at least 0.50) that are true positives by the same centre rule are counted per sheet; the kind's tally is one minus the total absolute difference between predicted and true counts, divided by the total true count. find, place and tally are each averaged over the five kinds, then combined with weights 0.45, 0.25 and 0.30. The reference grader grade.py, plain numpy and pandas) is shipped with the challenge.
> Dataset
> Inside public/:
> images/: the scanned sheets, one JPEG per drawing (1300 x 900 pixels). Every image referenced by train.csv or test.csv is here.
> train.csv: the ground-truth marks for the training sheets, one row per mark, with columns
> image_id (string): the sheet identifier; the file is images/<image_id>.jpg
> category (string): the hardware kind, one of bolt, nut, screw, washer, weld
> xmin, ymin, xmax, ymax (numbers): the box corners in pixels, with xmax > xmin and ymax > ymin
> test.csv: one row per test sheet with a single column image_id -- the sheets you must tally (their marks are withheld and must be inferred)
> sample_submission.csv: a valid, correctly formatted example submission (one dummy, low-confidence box per test sheet); it shows the required columns and carries no ground-truth information.
> Approximate split sizes: about 500 training sheets (roughly 18,000 marks) and about 100 test sheets. All five hardware kinds appear in both splits.
> Submission
> One CSV, a header plus one row per predicted mark (a sheet may carry many marks, or none).
> image_id,category,score,xmin,ymin,xmax,ymax
> im_00042,bolt,0.94,612,331,640,352
> im_00042,nut,0.88,210,455,231,476
> im_00087,weld,0.71,502,620,548,642
> image_id (string): a test sheet id from test.csv
> category (string): one of bolt, nut, screw, washer, weld
> score (number): confidence for the mark; it ranks predictions and, at or above 0.50, marks a detection as counted in the tally (higher = more confident)
> xmin, ymin, xmax, ymax (numbers): box corners in pixels, with xmax > xmin and ymax > ymin. Only the box centre is used for matching, so a small box centred on the mark is enough.
> Rows with an unknown kind or sheet id, or a degenerate box, are ignored; scores are clipped to [0, 1].
> What Not To Use
> This challenge is about learning to find the hardware marks from the training sheets, so a few classes of solution defeat the point and will not be accepted.
> Your solution must be a learned model trained on the provided sheets and boxes. A standard ImageNet/COCO-pretrained localization backbone fine-tuned on this data is expected; hand-built rules without a learned model do not satisfy the challenge.
> Do not hardcode, memorize, or game the output. Boxes copied from the answers, tables keyed to image ids, or anything that bypasses learning from the pixels will be rejected. The sample submission is a format reference only and is not a valid entry.
> Do not fingerprint the images by filename, ordering, or file metadata -- the score must come from the image pixels.
> Do not use external drawing datasets, or any model pre-trained on this challenge's data; and do not train on the test sheets (they carry no labels), which are for inference only.
> Everything must run within the compute and time budget of the challenge's GPU tier; a compact model is sufficient.
> Expected Output
> Write your predictions to ./working/submission.csv in the format described above.

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Meal Region Inventory Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx724tq4g83yg130gpzt7zq5cn8bmrte
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, segmentation
- Best/top context found: Top Score | — | Created | Aug 1, 2026 | Start New Solution

Full challenge description from page:

> Overview
> Each row contains a transformed food photograph with several annotated meal items. Predict a structured inventory of the visible food regions: category counts, occupied grid cells, item-size summaries, near-contact pairs where annotated food regions touch or nearly touch, and representative region cards with approximate geometry.
> The target is a JSON record derived from source COCO object annotations. It is not a single food category label; the region-card portion requires localizing visible food regions in the image.
> Dataset
> Released files:
> train.csv: labeled rows with row_id (string), image_path (string), and meal_inventory_json (JSON string).
> test.csv: rows to predict with row_id (string) and image_path (string).
> sample_submission.csv: schema-valid randomized example.
> category_schema.json: allowed food category names, grid shape, density values, and size values.
> images/: transformed meal images referenced by the CSV files.
> meal_inventory_json has exactly six fields:
> item_count (integer): total annotated food-region instances.
> category_counts (array): objects with category (string) and count (integer).
> cell_occupancy (array): objects with category, cell, and density; valid cells are r0c0 through r7c7.
> size_profile (array): objects with category, size, and density; size is one of bite, small, medium, large.
> near_contact_pairs (array): objects with sorted category names a and b, plus density.
> region_cards (array): up to 12 representative food regions. Each card has category, cell, size, and bbox, where bbox is [center_x, center_y, width, height] as normalized floats rounded to three decimals.
> Allowed density values are one, two, and three_plus.
> Evaluation
> Higher is better. Each row receives:
> row_score = 0.17*category_count_similarity + 0.24*cell_occupancy_f1 + 0.13*size_profile_f1 + 0.10*near_contact_pair_f1 + 0.04*item_count_exact + 0.32*region_card_score
> category_count_similarity is the sum of per-category count intersections divided by the sum of per-category count unions:
> sum(min(pred_count_c, true_count_c) for each category c) / sum(max(pred_count_c, true_count_c) for each category c).
> Each F1 term is duplicate-aware F1 over complete records:
> For cell_occupancy_f1, each record is the complete tuple (category, cell, density).
> For size_profile_f1, each record is the complete tuple (category, size, density).
> For near_contact_pair_f1, each record is the complete tuple (a, b, density).
> For a given F1 term, count duplicate submitted and true tuples with multisets. matches = sum(min(pred_count(tuple), true_count(tuple))); precision = matches / submitted_tuple_count; recall = matches / true_tuple_count; and F1 = 2*precision*recall/(precision+recall). If both multisets are empty, F1 is 1. If only one side is empty, F1 is 0. The leaderboard score is the mean row score.
> region_card_score greedily matches submitted region cards to true cards without reusing a submitted card. A matched card receives 0.25*category_exact + 0.15*cell_exact + 0.10*size_exact + 0.50*bbox_closeness, where bbox_closeness = max(0, 1 - mean_absolute_bbox_error / 0.08). The matched-card total is divided by the larger of submitted-card count, true-card count, and 1.
> Malformed JSON, invalid category names, duplicate category/cell records, category counts that do not sum to item_count, or invalid enum values score zero for that row. Wrong columns, missing ids, duplicate ids, wrong ids, or extra ids reject the submission.
> Submission
> Submit a CSV with exactly these columns:
> row_id,meal_inventory_json
> meal_example,"{""item_count"":1,""category_counts"":[{""category"":""Rice"",""count"":1}],""cell_occupancy"":[{""category"":""Rice"",""cell"":""r4c4"",""density"":""one""}],""size_profile"":[{""category"":""Rice"",""size"":""medium"",""density"":""one""}],""near_contact_pairs"":[],""region_cards"":[{""category"":""Rice"",""cell"":""r4c4"",""size"":""medium"",""bbox"":[0.55,0.58,0.32,0.28]}]}"
> What Not To Use
> Do not use external copies of the source data or source lookup.
> Do not use hidden answers or files outside the released data.
> Do not hard-code answers for released test ids.
> Do not use hosted inference APIs.
> Do not install packages at runtime.
> Do not use downloaded code, vendored solvers, or challenge-specific checkpoints

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Fungal Spore Taxon-Cell Census Report

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx767hcbq93d0qszf0djtkfed18bmwre
- DOMAIN exactly as displayed: Object Detection
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
> Each row contains a 5 by 5 mosaic microscope panel showing fungal spores from leaf-disease samples. Predict a structured taxon-cell census for the annotated spores visible across the full panel: the total spore count, counts for each taxon, occupied grid cells, coarse shape and size summaries, border-touch count, and a capped set of localized spore instance cards.
> The answer is a JSON record for the whole composite image. The input image is assembled as 5 by 5 source tiles, while the output uses a separate 12 by 12 scoring grid over the complete composite image. The mosaic tiles can contain different densities, taxa, and morphology patterns, so aggregate count prediction alone is not enough. A strong submission must find many small spores, assign their taxon and coarse morphology, and place representative instances accurately on the normalized image coordinate system.
> Dataset
> The released files are:
> train.csv: 3,927 labeled examples with row_id (string), image_path (string path under images/), and spore_profile_json (JSON string target).
> test.csv: 1,309 unlabeled examples with row_id (string) and image_path (string path under images/).
> sample_submission.csv: 1,309 valid submission rows with the required columns.
> images/: composite microscope JPEG images referenced by train.csv and test.csv.
> spore_profile_json must be a JSON object with exactly six keys:
> spore_count: integer from 0 to 700.
> taxon_counts: object with integer counts for all three taxa.
> cell_profile: list of taxon/cell density records.
> shape_profile: list of taxon/shape/size density records.
> edge_touch_count: integer from 0 to 700.
> spore_cards: list of up to 96 representative annotated spores.
> The taxon keys are:
> colletotrichum_siamense, olivea_tectonae, neopestalotiopsis_sp.
> Each taxon_counts object must contain exactly those three keys and must sum to spore_count.
> Each cell_profile item has:
> taxon: one of the three taxon keys.
> cell: one of the 144 output grid cells from r0c0 through r11c11; these 12 by 12 cells are overlaid on the full 5 by 5 mosaic image.
> density: one of one, two, three, four_plus.
> Each shape_profile item has:
> taxon: one of the three taxon keys.
> shape: one of slender, oval, round.
> size: one of tiny, small, medium, large.
> density: one of one, two, three, four_plus.
> Each spore_cards item has:
> taxon: one of the three taxon keys.
> cell: one of the 144 output grid cells from r0c0 through r11c11; these 12 by 12 cells are overlaid on the full 5 by 5 mosaic image.
> shape: one of slender, oval, round.
> size: one of tiny, small, medium, large.
> bbox: [center_x, center_y, width, height] as normalized floats rounded to three decimals in the full composite image.
> For crowded images, the card list is capped at 96 spores selected from the source annotations by larger area first, with stable ordering for ties.
> Example target:
> {"spore_count":1,"taxon_counts":{"colletotrichum_siamense":1,"olivea_tectonae":0,"neopestalotiopsis_sp":0},"cell_profile":[{"taxon":"colletotrichum_siamense","cell":"r5c4","density":"one"}],"shape_profile":[{"taxon":"colletotrichum_siamense","shape":"slender","size":"small","density":"one"}],"edge_touch_count":0,"spore_cards":[{"taxon":"colletotrichum_siamense","cell":"r5c4","shape":"slender","size":"small","bbox":[0.57,0.69,0.04,0.10]}]}
> Evaluation
> Higher is better. Each row receives a score from 0 to 1:
> row_score = 0.16*cell_profile_f1 + 0.08*taxon_count_similarity + 0.10*shape_profile_f1 + 0.06*spore_count_exact + 0.05*edge_touch_closeness + 0.55*spore_card_score
> The final score is the mean row score.
> For profile lists, F1 uses duplicate-aware multiset matching over complete profile records. Let overlap be the summed multiset intersection count, P = overlap / number_of_predicted_records, and R = overlap / number_of_true_records; the F1 value is 2*P*R/(P+R), with score 1 when both lists are empty and 0 when only one list is empty. taxon_count_similarity is the sum of per-taxon count intersections divided by the sum of per-taxon count unions. edge_touch_closeness = 1 - min(1, abs(predicted_edge_touch_count - true_edge_touch_count) / max(1, true_spore_count)).
> spore_card_score greedily matches submitted cards to true cards without reusing a submitted card. A submitted card with the wrong taxon for a true card receives similarity 0 for that match. For the same taxon, card similarity is (0.22 + 0.16*cell_exact + 0.08*shape_exact + 0.06*size_exact + 0.48*bbox_closeness) * cell_gate, where cell_gate is 1.0 when the cell matches and 0.45 otherwise. bbox_closeness = max(0, 1 - mean_absolute_bbox_error / 0.007), where the box values are normalized to [0,1]; the 0.007 denominator is intentionally strict because instance cards are representative localized annotations, not loose object-presence flags. The matched-card total is divided by the larger of submitted-card count, true-card count, and 1.
> Malformed JSON, invalid keys, missing taxon keys, invalid categories, duplicate cell/profile entries, or taxon counts that do not sum to spore_count score 0 for that row. A submission with missing rows, extra rows, duplicate ids, wrong ids, or wrong columns is rejected.
> Submission
> Submit a CSV with exactly these columns in this order:
> row_id,spore_profile_json
> spore_example_01,"{""spore_count"":0,""taxon_counts"":{""colletotrichum_siamense"":0,""olivea_tectonae"":0,""neopestalotiopsis_sp"":0},""cell_profile"":[],""shape_profile"":[],""edge_touch_count"":0,""spore_cards"":[]}"
> What Not To Use
> Do not use external datasets or source lookup.
> Do not use unreleased answer files or any file not included in the released data.
> Do not use hosted inference APIs.
> Do not install packages at runtime.
> Do not use downloaded code or challenge-specific checkpoints.
> Do not hard-code answers for the released test ids.

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Flattened Glyph Component Localization

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79nayapzhgbpmjp2pq9mzfc98c21cy
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat sasekiart's score of 0.975!

Full challenge description from page:

> Flattened Glyph Component Localization Overview Identify which of six shapes appears inside a composite glyph, then locate its full extent—even where another stroke covers it. Test images use font families that do not appear in training. Task Each 640 × 384 grayscale image contains a composite glyph on the left and six candidate shapes on the right. Exactly one candidate is part of the composite. Candidate slots are numbered 1 through 6 from left to right, then top to bottom. For each test image, predict component_slot and the candidate's complete bounding box using x_min, y_min, x_max, and y_max. Box coordinates are normalized to the 384 × 384 left panel, with (0,0) at the top left and (1,1) at the bottom right. Include covered portions of the component in the box. Data All available files are under dataset/public/. train.csv contains image paths, slots, and boxes; test.csv contains image paths without labels; and sample_submission.csv shows the required output columns. Image paths are relative to dataset/public/. The training split contains 1,800 labeled panels from 225 font families. The test split contains 600 panels from 100 different families and repositories. Targets are partially covered by other strokes, and the candidate shapes are intentionally similar. The zero-filled rows in sample_submission.csv are placeholders, not labels. Evaluation A prediction with the wrong slot scores 0. For a correct slot, the grader calculates box IoU and awards one ninth of the row score for each threshold met: 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, and 0.90. The final score is the mean over all 600 test rows, and higher is better. Submission Write ./working/submission.csv with one row for every test ID and these columns in order: unit_id,component_slot,x_min,y_min,x_max,y_max. Slots 1 through 6 require finite coordinates satisfying 0 <= x_min < x_max <= 1 and 0 <= y_min < y_max <= 1. Slot 0 is allowed only with an all-zero box and always scores 0. Missing, extra, or duplicate IDs and malformed rows make the submission invalid. Rules Use only the files in dataset/public/. Solutions must run offline on CPU and write the required CSV. Internet access, external fonts, private files, hidden answers, downloads, package installation, and GPU use are prohibited.
> $700 Pool
> Closes in 15m
> 12 / 12 continuing slots

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Reference-Conditioned Road Sign Damage Grounding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74nrfwct357st52kvr4ravpd8ds7sg
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Reference-Conditioned Road Sign Damage Grounding
> Overview Road-inspection systems encounter signs at widely different scales, under clutter, partial occlusion, and changing acquisition conditions. A fixed class name is not always available when a new inspection criterion is introduced. This challenge tests whether a model can use visual references supplied with each case to define the required conditions and then ground those conditions in a full road scene. Each case contains one road scene and two reference crops. reference_0_path defines condition R0; reference_1_path defines condition R1. The reference order changes independently for every case. A model must detect every sign in the scene and assign each box to the visually matching reference condition. This is conditional object detection, not ordinary two-class image classification. A solver that ignores the reference crops cannot know whether a physical condition should be emitted as R0 or R1 in a particular case. Split And Leakage Control A source similarity group is the complete set of raw images carrying the same precomputed group_code in source_annotations.csv. The code was assigned before challenge splitting and anonymization to link correlated source frames; it is independent of prepared case IDs and target geometry. The 4,185 source images form 2,283 such groups. A group may contain one frame or multiple related frames, and every object from an image inherits that image's group. The splitter stratifies whole groups according to whether they contain the less frequent condition and assigns each complete group to exactly one partition. It never divides a group between training and test. Reference crops for a case are also selected only from the same partition as the scene and from a different group than that scene. These rules prevent an exact or correlated source-frame series from serving as training data for a test scene or its references. The grouping does not claim that broad sign shapes, road backgrounds, or acquisition styles are unique to one partition. Learning patterns that transfer between genuinely different groups is intended generalization. The protection is specifically against memorizing another frame from the same linked source group. Dataset The public data contains three CSV files and an images/ folder. train.csv: training cases, image paths, dimensions, and target box ledgers. test.csv: test cases with the same input fields but no target ledger. sample_submission.csv: one non-null, valid-format zero-skill corner-box prediction for each test case. images/scenes/: re-encoded 640 by 480 RGB scene images. images/supports/: 128 by 128 RGB reference crops. train.csv Columns case_id (string): anonymous unique case identifier. scene_path (string): relative path to the road-scene JPEG. reference_0_path (string): relative path to the crop defining R0. reference_1_path (string): relative path to the crop defining R1. scene_width (integer): published scene width in pixels; always 640. scene_height (integer): published scene height in pixels; always 480. detections (string): semicolon-separated ground-truth atoms in the same six-field format required for submissions. Gold confidence is always 1.0. test.csv Columns case_id (string): anonymous unique case identifier. scene_path (string): relative path to the road-scene JPEG. reference_0_path (string): relative path to the crop defining R0. reference_1_path (string): relative path to the crop defining R1. scene_width (integer): published scene width in pixels; always 640. scene_height (integer): published scene height in pixels; always 480. sample_submission.csv Columns case_id (string): test case identifier. detections (string): prediction ledger described below. The sample uses one extremely small, low-confidence corner box so the column contains no missing values while carrying no useful target information. All box coordinates are normalized to [0, 1] relative to scene width and height. Submission Submit a CSV with exactly two columns: case_id and detections. Each non-empty detection atom must have six whitespace-separated fields: reference_tag confidence x1 y1 x2 y2 Separate multiple atoms with semicolons. For example, one valid CSV row is: SGNTST_01a2b3c4d5e6f7,"R1 0.94 0.120 0.210 0.245 0.430;R0 0.73 0.610 0.185 0.690 0.340" Rules: reference_tag must be R0 or R1. confidence must be finite and within [0, 1]. Coordinates must be finite and within [0, 1]. Every box must satisfy x1 < x2 and y1 < y2. Every required test case_id must occur exactly once. A malformed detection ledger receives zero detections for that case. Missing IDs, duplicate IDs, missing columns, extra columns, and null IDs are rejected. Rows belonging to another platform scoring partition are ignored after all required IDs are confirmed. Evaluation The score is bounded in [0, 1] and higher is better: Score = 0.35 * ConditionedAP50 + 0.20 * ConditionedAP75 + 0.25 * WorstReferenceAP50 + 0.15 * SmallSignAP50 + 0.05 * ExactSceneAccuracy The displayed terms are the complete formula and the weights sum to 1.00. Detection Matching Predictions are sorted globally by decreasing confidence. A prediction can match at most one previously unmatched ground-truth box from the same case and with the same R0 or R1 tag. The unmatched target with the highest intersection-over-union is used when it reaches the metric threshold. For each AP component, cumulative precision and recall are computed over the selected predictions. AP is the mean of interpolated precision at 101 evenly spaced recall levels from 0.00 through 1.00. At each recall level, interpolated precision is the maximum precision observed at that recall or any greater recall. Metric Components ConditionedAP50: AP over all tagged boxes at an IoU threshold of 0.50. ConditionedAP75: AP over all tagged boxes at an IoU threshold of 0.75. WorstReferenceAP50: the smaller of two independently computed scores, AP50_R0 and AP50_R1. AP50_R0 retains only R0 target and predicted boxes in every case, and AP50_R1 does the same for R1. Taking their minimum requires reliable grounding for both case-local references and is fully reproducible from the published tags. SmallSignAP50: AP50 for target and predicted boxes with normalized area at most 0.008. Filtering is performed at box level for both truth and predictions. ExactSceneAccuracy: fraction of test scenes for which the predicted box count is exact and every predicted box has a one-to-one, same-tag match at IoU at least 0.50. The same box may contribute to more than one named component. These are weighted views of one prediction set, and no metric block is added outside the displayed formula. Allowed And Prohibited Methods Allowed methods include supervised detection, reference-conditioned feature fusion, metric learning, transfer learning from general-purpose pretrained vision models, ensembling, and deterministic assignment or post-processing based on model outputs. Prohibited methods include external source matching, reverse-image search, manually hardcoded test labels or boxes, source-identifier recovery, and non-ML lookup systems that identify individual test scenes. Use only the files supplied with this challenge and generally available pretrained models that were not trained to reveal this challenge's test answers. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Underwater Marine-Animal Spotting

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx797277cfhnwx0ek70psxcpfn8e63g3
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat hoang_phuc_6868's score of 0.629!

Full challenge description from page:

> Underwater Marine-Animal Spotting Task type This is a tiny-object spotting task -- object detection scored by LOCATION, not box overlap. You are given underwater video frames and must, for every frame, place a box on each of three marine animals with a confidence score. The animals are small and murky (a typical animal is ~14 pixels across in the 512-pixel frame), so their exact extent is ambiguous and what matters is putting a marker ON each animal. You are therefore scored by whether your box is CENTRED on a real animal -- not by how tightly it hugs the animal's outline. This is not classification and not ranking; you localise a variable number of animals per frame. The three animals Each frame is searched for three animals that occur largely independently, so finding one tells you little about the others: crab -- a crab on or near the bottom. fish -- a fish. starfish -- a starfish. Their per-frame counts are decorrelated, with every pairwise rank correlation at or below about 0.10 in magnitude, so the three per-animal scores are three near-independent measures: a solution good at one gets little on the others, and must learn to find each animal on its own -- against a murky, low-contrast underwater background where animals are small and sometimes partly hidden. What you are given train_images/.jpg -- 512 by 512 RGB underwater frames. train_boxes.csv -- the ground-truth boxes for the training frames, with columns id, boxes, one row per frame. boxes packs all of that frame's boxes as a ;-separated list; each box is category xmin ymin xmax ymax (space-separated), category one of crab, fish, starfish, coordinates corner pixels in the 512 by 512 frame. Every training frame contains at least one box. test_images/.jpg -- the frames to detect in; each contains at least one box. test_queries.csv -- column id, the frames to score. sample_submission.csv -- a correctly shaped example: one row per test frame with a fixed generic box per class (a weak baseline that shows the encoding). What you submit working/submission.csv with exactly the columns id, boxes -- one row per test frame (each id appears exactly once). Pack all of a frame's predicted boxes into the single boxes cell: id -- the test frame id. boxes -- a ;-separated list of predicted boxes; each box is category xmin ymin xmax ymax score (space-separated). category is one of crab, fish, starfish; xmin ymin xmax ymax are the corners in the 512 by 512 frame with xmax > xmin and ymax > ymin; score is your confidence (higher = more confident, used only to order predictions). Every test frame contains at least one animal, so predict at least one box; write boxes = nobox only in the rare case you predict none -- never leave the cell blank. For example, a row q00042 with boxes = crab 200 240 300 320 0.9;starfish 220 300 320 400 0.6 predicts a crab and a starfish. How you are scored The metric is ReefScore, higher is better, bounded in 0 to 1. Matching is centre-based, not IoU-based: for each animal your boxes are ranked by score, and a box counts as a true positive if its centre falls inside an as-yet-unmatched true box of the same animal in the same frame (among the true boxes whose interior contains your centre, the best-overlapping one is consumed), and a false positive otherwise. The per-animal score is the Average Precision (area under the precision-recall curve, Pascal-VOC all-points) and ReefScore is the mean of the three. Because matching is by centre, an approximately-sized box placed on an animal scores just as well as a pixel-perfect one -- but a box centred on empty water, or a second box on an animal already found, is a false positive that costs precision, and every missed animal costs recall. Predicting nothing scores 0. The split Training and test frames are disjoint by source video. Because consecutive frames of a video are near-identical, a random frame split would leak; instead whole source videos are held out, so every test frame comes from a recording never seen in training. About 20 percent of the frames are held out for test by a deterministic hash of the source-video id. Allowed and prohibited Allowed -- any model you train on the provided frames, such as a convolutional detector trained from scratch; standard image preprocessing and augmentation such as flips, scaling, and colour jitter. Prohibited -- external data or pretrained image weights; per-id answer tables or any hardcoded output; reading, fitting, or adapting to the test frames in any way; recovering anything from the id rather than the image. Ids are randomised and carry no signal. Compute GPU, one hour. The from-scratch reference detector trains well inside that budget. &nbsp;
> $700 Pool
> 3 / 12 beat AI

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## In-Situ Recyclable Material Recovery Detection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fpn6dbvn7nx5442dzwbyvts8e093g
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> In-Situ Recyclable Material Recovery Detection Overview Detect every visible recyclable-material item in a cluttered outdoor photograph. The operational question is how many recoverable items are present, which material stream each item belongs to, and where each item is located well enough for a human or robotic sorting workflow to inspect it. The task uses real photographs and released annotations. The public package contains labeled training images and unlabeled test images; filenames are replaced with opaque identifiers so solutions must learn from visual evidence rather than metadata. The hidden evaluation images are held out by capture identity and near-duplicate visual components. This makes the benchmark test transfer to a new capture component, not memorization of adjacent frames, while the score rewards both a useful material inventory and boxes that are useful for inspection. Dataset File descriptions train.csv: one labeled training row per image. test.csv: one unlabeled test row per image. train_images/: RGB JPEG files referenced by the training rows. test_images/: RGB JPEG files referenced by the test rows. sample_submission.csv: a schema-valid, non-constant example submission. Column descriptions train.csv columns: id: opaque image identifier. image: relative path to the corresponding public JPEG. prediction: JSON list of labeled material instances. test.csv columns: id: opaque image identifier. image: relative path to the corresponding public JPEG. Each annotation object contains: class_id: integer material class, where 0 is paper, 1 is plastic bottle, 2 is plastic bag, and 3 is plastic waste. bbox: four normalized coordinates x1, y1, x2, y2], with the origin at the top-left and x2 > x1, y2 > y1. The prepared split contains 2,209 labeled training images and 633 hidden test images. Images sharing a capture-name stem or a connected near-duplicate component stay on the same side of the split; the capture-group metadata is not included in the public files. Evaluation The grader parses the two-column submission, aligns rows by id, and rejects missing, duplicate, extra, or malformed IDs and prediction payloads. A prediction can match only a ground-truth item of the same material class. Matching is one-to-one and processes candidate pairs from highest quality to lowest quality, with deterministic tuple ordering for ties. The complete score calculation is shown below. submission is a pandas DataFrame with columns id and prediction; answers has those same prediction columns and may also carry the optional platform metadata column visibility, which is ignored by the score. Each prediction value is a JSON string containing the material-instance list. The returned score is maximized and is always in [0, 1]. import json import math CLASSIDS = (0, 1, 2, 3) def parseValue(value): if not isinstance(value, str): raise ValueError("prediction must be a JSON string") decoded = json.loads(value) if not isinstance(decoded, list) or len(decoded) > 128: raise ValueError("prediction must be a list with at most 128 items") parsed = [] for item in decoded: if not isinstance(item, dict) or set(item) != {"class_id", "bbox"}: raise ValueError("each annotation must contain class_id and bbox only") classId = item["class_id"] if isinstance(classId, bool) or not isinstance(classId, int) or classId not in CLASSIDS: raise ValueError("invalid class_id") bbox = item["bbox"] if not isinstance(bbox, list) or len(bbox) != 4: raise ValueError("bbox must contain four coordinates") box = tuple(float(coordinate) for coordinate in bbox) if not all(math.isfinite(coordinate) and 0.0 x1 and y2 > y1): raise ValueError("bbox must have positive area") parsed.append((classId, box)) return parsed def iou(first, second): x1 = max(first[0], second[0]) y1 = max(first[1], second[1]) x2 = min(first[2], second[2]) y2 = min(first[3], second[3]) intersection = max(0.0, x2 - x1) * max(0.0, y2 - y1) firstArea = (first[2] - first[0]) * (first[3] - first[1]) secondArea = (second[2] - second[0]) * (second[3] - second[1]) return intersection / max(firstArea + secondArea - intersection, 1e-12) def pairQuality(predicted, target): iouScore = iou(predicted, target) predictedCenter = ((predicted[0] + predicted[2]) / 2.0, (predicted[1] + predicted[3]) / 2.0) targetCenter = ((target[0] + target[2]) / 2.0, (target[1] + target[3]) / 2.0) centerDistance = math.hypot(predictedCenter[0] - targetCenter[0], predictedCenter[1] - targetCenter[1]) centerSimilarity = max(0.0, 1.0 - centerDistance / 0.15) predictedArea = max((predicted[2] - predicted[0]) * (predicted[3] - predicted[1]), 1e-9) targetArea = max((target[2] - target[0]) * (target[3] - target[1]), 1e-9) sizeSimilarity = math.exp(-abs(math.log(predictedArea / targetArea)) / 1.5) quality = 0.65 iouScore + 0.25 centerSimilarity + 0.10 * sizeSimilarity eligible = iouScore >= 0.05 or centerSimilarity >= 0.45 return quality, eligible def matchPairs(predicted, target): pairs = [] for predictedIndex, (predictedClass, predictedBox) in enumerate(predicted): for targetIndex, (targetClass, targetBox) in enumerate(target): if predictedClass != targetClass: continue quality, eligible = pairQuality(predictedBox, targetBox) pairs.append((quality, eligible, predictedIndex, targetIndex)) pairs.sort(reverse=True) usedPredicted = set() usedTarget = set() qualitySum = 0.0 matches = 0 for quality, eligible, predictedIndex, targetIndex in pairs: if not eligible or predictedIndex in usedPredicted or targetIndex in usedTarget: continue usedPredicted.add(predictedIndex) usedTarget.add(targetIndex) qualitySum += quality matches += 1 return qualitySum, matches def materialRecoverySurfaceScore(submission, answers): expectedColumns = ["id", "prediction"] answerColumns = list(answers.columns) answerPredictionColumns = [column for column in answerColumns if column != "visibility"] if list(submission.columns) != expectedColumns or not ( answerColumns == expectedColumns or ( len(answerColumns) == len(expectedColumns) + 1 and set(answerColumns) == set(expectedColumns) | {"visibility"} and answerPredictionColumns == expectedColumns ) ): raise ValueError("submission must be id,prediction; answers may add only visibility") if len(submission) != len(answers) or submission.isna().any().any() or answers.isna().any().any(): raise ValueError("row counts and missing values are invalid") predictedIds = submission["id"].astype(str) targetIds = answers["id"].astype(str) if predictedIds.duplicated().any() or targetIds.duplicated().any() or set(predictedIds) != set(targetIds): raise ValueError("IDs must be unique and match exactly") predictions = dict(zip(predictedIds, submission["prediction"].map(parseValue))) targets = dict(zip(targetIds, answers["prediction"].map(parseValue))) totals = {classId: [0, 0, 0, 0.0] for classId in CLASSIDS} countScores = [] for imageId in targetIds: predictedImage = predictions[imageId] targetImage = targets[imageId] for classId in CLASSIDS: predictedClass = [item for item in predictedImage if item[0] == classId] targetClass = [item for item in targetImage if item[0] == classId] qualitySum, matches = matchPairs(predictedClass, targetClass) totals[classId += len(targetClass) totalsclassId += len(predictedClass) totalsclassId += matches totalsclassId += qualitySum denominator = len(predictedClass) + len(targetClass) if denominator: countScores.append(2.0 * min(len(predictedClass), len(targetClass)) / denominator) classScores = [] for targetCount, predictedCount, matches, qualitySum in totals.values(): denominator = targetCount + predictedCount - matches classScores.append(qualitySum / denominator if denominator else 1.0) softLocalization = sum(classScores) / len(classScores) countF1 = sum(countScores) / len(countScores) if countScores else 0.0 score = 0.75 softLocalization + 0.25 countF1 if not math.isfinite(score) or not 0.0 <= score <= 1.0: raise ValueError("score is outside [0,1]") return score For each material class, the soft localization score is the sum of matched qualities divided by ground-truth count plus prediction count minus matched count. The four class scores are averaged equally. The count term is the mean per-image, per-class F1 over material classes that are present in either the prediction or the ground truth; an image with no predictions receives no background credit. The final Material Recovery Surface Score is 0.75 mean(class soft-localization scores) + 0.25 mean(count F1 scores). This weighting reflects the practical need for both a reliable material inventory and inspection-useful placement. Submission Submit a CSV with exactly id,prediction columns. Include exactly one row for every test id, exactly once. Encode prediction as a JSON list with at most 128 items per image. Each annotation item must contain only class_id and bbox. Coordinates must be finite normalized values in [0, 1] and form a positive-area box. Example: id,prediction WST_4f9e8a0d9a13b3c2,"[{""class_id"":1,""bbox"" :[0.20,0.40,0.34,0.61]}]" Requirements Train and validate using only the public prepared images and training annotations. Keep capture stems, preparation metadata, private answers, and any reverse ID mapping out of the solution. Use the YAML class mapping above; do not infer class IDs from filenames. Keep local validation group-aware so capture and near-duplicate variants do not cross a fold. Prohibited: recovering hidden IDs or capture metadata, using cached/external annotations for these images,,replacing detection with a fixed template, or creating synthetic images or labels. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Blind-Interval Object Detection from Communication-Waveform I/Q

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74cp6134cxc99rj20h5pdbn58e8bea
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat guyc890's score of 22.871!

Full challenge description from page:

> Overview Each example contains an unknown set of moving objects. The detector must identify the objects present at a target time without receiving RF observations from the interval containing that time. The participant-visible input contains: ten RF observations immediately before the blind interval; and ten RF observations immediately after the blind interval. The twenty central SRS record times are withheld. They cover approximately 50 ms and contain the labeled target time. The supplied relative_times_ms values give the measured offset of every visible RF observation from that target time. During training, a visual frame synchronized to the labeled target time is available as optional privileged supervision. During evaluation, the teacher_image_path column remains present for feature-schema consistency, but its value is blank and no image is supplied. This is object detection, not tracking For each sample, the required output is an unordered detection set: D = {(s_i, r_i, v_i)} for i = 1,...,K, where s_i is confidence, r_i is bistatic range in meters, and v_i is signed radial velocity in meters per second. Participants do not submit persistent identities, and the evaluator does not reward identity consistency between samples. A model may internally associate RF structures, filter trajectories, or interpolate motion across the blind interval, but the scored output remains an instantaneous object set. Blind interval The complete conceptual interval has 40 nominal SRS record times: positions 0 through 9 are visible before the gap; positions 10 through 29 are withheld; and positions 30 through 39 are visible after the gap. The target time lies at the center of the withheld region. With the approximately 2.5 ms SRS cadence, the visible observations normally lie about 26 to 49 ms before and after the target. Exact offsets are supplied per sample instead of assuming perfectly uniform timing. No zero-filled placeholder is inserted for a missing observation. The target-time RF evidence is absent by construction. RF input Each RF tensor is stored as float16 real and imaginary components with shape: [20, 4, 1632, 2] The dimensions are: 20 participant-visible times; 4 receive channels; 1,632 active pilot tones; and real and imaginary components. The source record buffer contains six OFDM symbols, but the configured SRS occupies buffer symbol index 0. Preparation retains and despreads that SRS symbol only. The other buffer symbols are not presented as additional sounding observations. The tensor contains despread complex channel observations, not organizer-generated detections. It embeds no target range, target velocity, target count, camera coordinate, tracker output, persistent identity, or target-dependent mask. Participants may construct power-delay profiles, Range-Doppler maps, cross-antenna phase features, covariance matrices, temporal Fourier features, clutter-subtracted tensors, learned complex embeddings, or other representations. Physical target space Every scored object has one bistatic range and one radial velocity. Range is scored in [0, 60] meters and velocity in [-5, 5] m/s. Positive and negative velocity indicate opposite radial directions under the published convention. This is point-set detection in physical kinematic space. Object class, world position, physical dimensions, and persistent source identity are not leaderboard targets. Privileged vision Training examples include a visual frame synchronized to the same target frame used to construct their physical labels. It may be used for a multimodal teacher, object-count supervision, RF-vision alignment, auxiliary contrastive objectives, or distillation into an RF-only student. Its use is optional. Evaluation provides no image and no hidden-image API. A valid inference pipeline must operate from RF and public non-target metadata alone. Files The public package contains: train.csv train_objects.csv test.csv sample_submission.csv rf/ train_teacher_images/ metadata/ There is no supplied development partition. Nearby sensing windows can be highly correlated, so random row-level validation is strongly discouraged. Local validation should use contiguous temporal blocks. Train and test schema train.csv and test.csv contain exactly the same feature columns, in exactly this order: sample_id rf_path teacher_image_path relative_times_ms blind_gap_ms visible_record_count max_detections For training rows, teacher_image_path points to the privileged target-time image. For test rows, it is the empty string. This keeps feature schemas identical without exposing evaluation imagery. relative_times_ms is JSON containing the measured offset of each visible RF observation from the hidden target time. Negative values are pre-gap observations and positive values are post-gap observations. blind_gap_ms is the nominal duration represented by the twenty withheld record times. max_detections is submission capacity and does not reveal the true object count. Training labels train_objects.csv contains one row per training target: sample_id object_index range_m velocity_mps object_index is an arbitrary within-sample row identifier and has no persistent meaning between samples. Training targets with incomplete or out-of-domain physical localization are excluded. Temporal split and leakage controls Complete temporal blocks are held out. Guard intervals separate training and evaluation regions, and the preparation process verifies that no participant-visible RF record is reused across the two partitions. The split also prevents target-time training images from exposing adjacent evaluation frames. Participants may use test.csv for unsupervised or transductive preprocessing unless the execution environment states otherwise, but may not use withheld labels or unavailable synchronized imagery. Evaluation never exposes target range, target velocity, target count, target identity, target-time RF observations, synchronized test imagery, image coordinates, organizer tracker peaks, or tracker residuals. Submission Each sample has at most three scored objects. sample_submission.csv contains exactly three unordered slots: sample_id score_0, range_0, velocity_0 score_1, range_1, velocity_1 score_2, range_2, velocity_2 Confidence values must lie in [0, 1]. Range must lie in [0, 60], and velocity must lie in [-5, 5]. Every value must be finite. An unused slot uses confidence 0.0. Its coordinates must still be finite and in range, but they do not participate in matching. Submission columns must match sample_submission.csv exactly. Duplicate IDs, unknown IDs, non-finite values, invalid columns, and out-of-domain values receive the evaluator floor. The private answers.csv contains every sample_submission.csv column plus private metadata. It may contain additional rows used by evaluator-contract tests. A scoring call aligns submitted IDs to their answer rows and ignores unrelated extra answer rows. Physical matching distance For prediction p and target g, normalized distance is: d(p,g) = sqrt(((r_p-r_g)/1.5)^2 + ((v_p-v_g)/0.50)^2). A prediction may match a target only when its distance is no greater than the current threshold. Each target and prediction can be used at most once. Matching occurs independently within each sample before global precision-recall statistics are accumulated. Detection metric Average precision is evaluated at normalized thresholds 0.75, 1.00, and 1.50. At each threshold: positive-confidence predictions are ranked globally by confidence; one-to-one within-sample matching determines true and false positives; unmatched ground-truth objects are false negatives; and standard interpolated average precision is calculated. The three AP values are averaged to obtain physical mAP. Physical mAP is computed separately for samples containing exactly one target and samples containing multiple targets. When both regimes are present, the final score is: Score = 100 * (mAP_single + mAP_multi) / 2. An evaluator-contract slice containing only one regime uses that regime's mAP. The score is clipped to [0.01, 100]. Grading is deterministic and uses no LLM judge, manual assessment, embedding service, or external API. Why the task is difficult Targets can overlap in range, velocity, multipath structure, clutter, sidelobes, and antenna-dependent fading. The strongest pre-gap and post-gap structures may belong to different objects. A weak target can disappear beneath another reflection, velocity may change across the gap, and objects may enter or leave the scored set near the hidden time. A conventional detector can build a Range-Doppler map at the instant being scored. That direct route is unavailable here because all RF observations near the target instant are withheld. The model must infer the target-time set from how complex channel structure evolves before and after the blind interval. Compute budget The intended environment provides one NVIDIA A10G GPU with 24 GB VRAM, host CPU and memory, and a 90-minute end-to-end budget. RF tensors can be memory-mapped or streamed; they need not all be loaded into host memory simultaneously. A useful baseline may coherently combine receive channels, suppress stationary components, form delay or Range-Doppler representations on each side of the gap, associate peaks, and interpolate physical coordinates. Learned approaches may use complex CNNs, antenna-aware transformers, temporal Fourier networks, pre-gap and post-gap cross-attention, set decoders, neural filters, or RF-vision distillation. Scope The benchmark evaluates measured moving-object detection from temporally censored communication-waveform sensing. It does not evaluate personal identification, persistent tracking IDs, camera inference at evaluation, or every physical RF scatterer. Given complex RF measurements immediately before and after a missing sensing interval, detect the moving objects that occupied the hidden target time.
> 2 / 12 beat AI

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Marine Debris Detection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c5w3rrjtk9h2pax20bxyh5d8e97dm
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat masry1's score of 0.417!

Full challenge description from page:

> Marine Debris Detection Overview A coastal survey image has been partly reviewed: some annotated debris boxes are already in a ledger, while other annotated objects still need entries. Detect the remaining objects in the same image and localize their annotated extents precisely so each new entry provides a close object crop. Use both the pixels and the supplied ledger, and do not return boxes that are already logged. All debris is one detection class. Examples include floats, rope, netting, manufactured fragments, tires, processed wood, and stranded vessels. Natural rocks, vegetation, water, and unmodified driftwood are not automatically debris. Training boxes illustrate the annotation scope. Fine-grained material identification, removal priority, object mass, and physical access are not requested. Every supplied ledger box is an exact human annotation from that row's image. The target is the complement of those ledger annotations for the review state; it does not require deciding whether two views show the same physical object. Every released row has at least one target box. The ledger can be empty, and its length does not determine how many targets remain. The images contain small objects, dense accumulations, edge-truncated objects, and black regions without image coverage. Targets follow the provided human box annotations, including annotated truncated objects. No additional minimum object size applies. There are no instance masks or fine-grained category targets. An unannotated region is not independently certified debris-free; scores measure agreement with the annotated catalogue, not exhaustive environmental ground truth. Visually plausible but unmatched proposals receive no match credit and count toward the prediction total. Use CPU only, at most 62GB of RAM, and at most 90 minutes for the complete solution, including preprocessing, training, validation, inference, and submission writing. Dataset There are 1,010 training rows and 411 test rows, with one distinct 640 × 640 RGB JPEG per row under images/. Each row is one image plus one partial-review state. The same ground can appear in several source images. survey_id identifies a geographic dependency group suitable for grouped validation: training and test group IDs are disjoint, and known overlapping views and shared orthophoto sources stay together. These groups are not certified independent flights or physical specimens. Keep all rows sharing a survey_id together during validation. The ledger is image-local. It is not a tracking history, change-over-time signal, or cross-view physical-object match. Public inputs contain everything required to interpret it. Do not search for source annotations or infer test labels from unavailable external records. train.csv | Column | Type | Meaning | |---|---|---| | id | String | Unique review-state ID. | | image | Relative path | JPEG input under images/. | | survey_id | String | Geographic group for validation and score aggregation. | | logged_boxes | JSON array | Debris boxes already annotated in this image. | | new_boxes | JSON array | Remaining annotated debris boxes to predict. | Both box columns use arrays of [left,top,right,bottom] values. Coordinates are measured in pixels from the image's upper-left corner, with x increasing rightward and y downward. Boxes use continuous half-open extents [left,right) × [top,bottom) inside the image. Coordinates lie in [0,640]; width and height must be positive. Ledger boxes can touch an image edge. You may combine logged_boxes and new_boxes to train a detector for all annotated debris, then remove detector proposals matching the row's ledger. For example, suppressing proposals at IoU at least 0.5 to a logged box is a permitted heuristic; the 0.81 threshold in evaluation applies to matching remaining targets, not to a mandatory ledger-suppression algorithm. test.csv The columns are id,image,survey_id,logged_boxes, with the same meanings as in training. Generate one prediction row for every test ID, including rows for which your model predicts no remaining objects. sample_submission.csv The columns are id,new_boxes. Every new_boxes value is []; this is a valid abstention example, not a competitive detector. It uses no hidden object counts. Image files, CSV inputs, and this sample are the complete model-input package. Submission format Write working/submission.csv as a UTF-8 CSV with the required columns id and new_boxes. Rows and columns may be reordered. Additional uniquely named columns are ignored consistently. Column names must be nonempty strings without surrounding spaces. Duplicate headers, blank or ragged rows, malformed CSV quoting, missing IDs, repeated IDs, or extra IDs invalidate the entire submission. The CSV may start with a UTF-8 byte-order mark. For these invented examples, image demo_a contains three annotated objects at [100,100,140,140], [300,200,350,250], and [500,400,540,460]; its ledger contains the first and third. Image demo_b contains objects at [0,20,25,65] and [200,300,230,335]; its ledger contains the second. The two submission rows below return only the remaining boxes, including an edge-touching target. id,new_boxes demo_a,"[[300,200,350,250]]" demo_b,"[[0,20,25,65]]" Evaluation For boxes A and B, IoU(A,B) = area(A ∩ B) / area(A ∪ B), using their continuous pixel areas. A prediction can match a target in the same row if IoU is at least 0.81. This requires close agreement with the annotation: a box that merely surrounds the correct object can miss the localization requirement. Matching maximizes the number of qualifying one-to-one matches. A prediction and a target can each participate in at most one match. Equality at IoU 0.81 counts as a match. For example, [0,0,81,100] against [0,0,100,100] qualifies exactly, whereas [0,0,80,100] does not. Multiple maximum matchings have the same match count and therefore the same score; enumeration and tie order do not affect scoring. Within each geographic group in the scoring cohort, sum the matched pairs TP, the number of submitted boxes P, and the number of target boxes T over its rows. The group score is 2 × TP / (P + T) when P + T > 0. If both totals are zero, the group score is 1. Returning no boxes for a group with targets scores 0. Unmatched boxes, including duplicate proposals and already logged objects, increase P without increasing TP; missing objects increase T without increasing TP. The final score is the arithmetic mean of the group scores, a float from 0 to 1 to maximize. Each group present in the supplied scoring cohort has equal weight. If a cohort contains only part of a group, its totals use those supplied rows only. There is no confidence ranking, score power, or hidden cutoff. Correct complete predictions attain 1. A full-size image rectangle is not a substitute for localized objects. Not allowed -Remote inference services External task images, task labels, models trained on this debris collection, source-to-answer lookup, and manual annotation of test images are not allowed. Training, selecting thresholds, or changing hyperparameters using test predictions, test distribution statistics, or test labels is not allowed. Use only training-side validation groups for those decisions. Do not transfer labels between test images or update model weights at test time. Each output must depend only on its row's image and ledger plus a model fitted on training data. &nbsp;
> Closes in 25m
> 12 / 12 continuing slots

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.

## Weld-Radiograph Detection Under Exposure Shift

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ew0w1tm9ksw6x2fveefzrzh8e77n3
- DOMAIN exactly as displayed: Object Detection
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 0.231!

Full challenge description from page:

> Weld-Radiograph Detection Under Exposure Shift What this benchmark is This is a distribution-shift generalization benchmark posed as object detection. The subject matter is industrial weld radiography, but the point of the task is not weld inspection in the usual sense — it is whether a detector can keep working when the imaging conditions change between training and deployment. Radiographs are acquired at different exposures (film/sensor brightness set by the equipment and operator), and a model tuned to one exposure band tends to fail on another. Here, training and evaluation are drawn from strongly different exposure distributions: you fit on a mostly-bright set and are scored on a much darker one. This is a distributional shift, not a hard threshold on brightness — the two ranges overlap — but they are far apart (see below). The challenge is a controlled test of cross-condition robustness, using weld radiographs as the medium. Concretely: for every image you place axis-aligned boxes around each of three annotated weld regions and give each box a confidence. This is not classification and not ranking — you localise a variable number of regions per image, drawn from a much darker exposure distribution than the one you trained on. The evaluation protocol (what makes it distinct) The defining feature is the split, not the label format: Every source radiograph is characterised by its overall brightness (an exposure proxy). Source radiographs are grouped (augmented copies and near-duplicate re-encodes are kept together), each group is ranked by its mean brightness, and the darkest groups — about 20 percent of the images — become the test set; the rest are training. Because groups move on their mean brightness, this is a strong distributional shift, not a clean partition: the image-level brightness ranges overlap (on the built split, training runs 23–246 grey, test 23–224), yet the two distributions are far apart — a Kolmogorov–Smirnov statistic of about 0.80, a training median near 127 versus a test median near 87, about 94 percent of test images below the training 25th percentile, and only about 7 percent of training images darker than the test median. There is no brightness threshold that separates the sets — a solver keying off a single cutoff will not find one; it has to generalise across the shifted exposure distribution. A detector that memorises the training exposure, or quietly relies on exposure-correlated cues, degrades on the darker test distribution; only one that has learned exposure-invariant region appearance transfers. This turns a standard-looking detection dataset into a cross-imaging-condition generalization problem. Ordinary detectors do not transfer to it without explicitly addressing the shift (exposure augmentation, normalization, or other domain-generalization techniques). The three annotated regions Each radiograph carries boxes for three region types (kept under their source names for the submission encoding): badweld — a weld run annotated as poor. goodweld — a weld run annotated as sound. defect — a localised flaw such as porosity or a crack. They are only partially independent (poor runs and localised flaws tend to co-occur), so the three per-region scores are related rather than orthogonal; a solution still has to recover each on its own, under the unseen exposure. What you are given train_images/.jpg — 512 by 512 RGB weld radiographs (the brighter-exposure portion of the data). train_boxes.csv — ground truth for the training images, columns id, boxes, one row per image. boxes is a ;-separated list; each box is category xmin ymin xmax ymax (space-separated), category one of badweld, goodweld, defect, corner pixels in the 512 by 512 frame. Every training image has at least one box. train_conditions.csv — columns id, brightness: the mean grey level (0–255) of each training image, i.e. the exposure axis the split is built on. Use it to reproduce the shift locally (hold out your own darkest images for validation) and to drive exposure augmentation. The test set is much darker on average, though the ranges overlap. test_images/.jpg — the radiographs to detect in; each comes from the darker exposure distribution and has at least one box. test_queries.csv — column id, the images to score. sample_submission.csv — a correctly shaped example: one row per test image with a fixed generic box per category. What you submit working/submission.csv with exactly the columns id, boxes — one row per test image (each id once). Pack all of an image's predicted boxes into the single boxes cell: id — the test image id. boxes — a ;-separated list; each box is category xmin ymin xmax ymax score. category is one of badweld, goodweld, defect; xmin ymin xmax ymax are corners in the 512 by 512 frame with xmax > xmin and ymax > ymin; score is your confidence (higher = more confident, used to order predictions). Predict at least one box per image; write boxes = nobox only if you predict none — never leave the cell blank. For example, q00042 with boxes = goodweld 150 200 360 300 0.9;defect 240 240 290 300 0.7. How you are scored WeldScore, higher is better, in 0 to 1: for each region type the Average Precision at IoU 0.5 (Pascal-VOC all-points) — your boxes ranked by score, a true positive if it overlaps an as-yet-unmatched true box of the same type with IoU ≥ 0.5, else a false positive, AP the area under the precision-recall curve — and WeldScore is the mean of the three, computed on the held-out dark-exposure test set. Because the test set is a shifted exposure regime, the score reflects generalization, not just fit: predicting nothing scores 0; boxes in the wrong place, at the wrong size, or duplicated cost precision. Allowed and prohibited Allowed — any model you train on the provided images, e.g. a convolutional detector from scratch; standard preprocessing and augmentation, and in particular exposure / brightness / contrast augmentation and normalization to bridge the imaging-condition gap; any domain-generalization method. Prohibited — external data or pretrained image weights; per-id answer tables or hardcoded output; reading, fitting, or adapting to the test images in any way (test-time training or tuning on test statistics); recovering anything from the id rather than the image. Ids are randomised and carry no signal. Compute GPU, one hour. The from-scratch reference detector trains well inside that budget. &nbsp;
> 3 / 12 beat AI

Inspiration note: Useful because it asks for localized evidence or object-level recovery in a constrained real-world visual setting.


# Non-CPU Prompt Engineering Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed Non-CPU examples in this document: 2

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.

## Livestock Posture Keypoint Geometry Profile Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73gapftbwzzg251a0ftp1zmn8b5aqz
- DOMAIN exactly as displayed: Prompt Engineering
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat wukong's score of 0.663!

Full challenge description from page:

> Overview
> Farm-animal posture images can show an animal standing, walking, turning, or partly occluded by its environment. Each row contains a transformed RGB image and a JSON packet listing 18 anatomical keypoints such as nose, neck, withers, tail head, knees, and hooves. Your task is to recover a structured posture profile: which joints are visible or occluded, which grid cell each labeled joint occupies, the animal body box, limb-span bins, and a compact list of joint cards with approximate image coordinates.
> The labels are anatomical keypoint annotations. This is not a captioning task and not a single animal-class lookup; partial credit depends on recovering both the joint identities and their geometry.
> Dataset
> Files provided:
> train.csv: 1,500 labeled examples.
> test.csv: 729 unlabeled examples.
> sample_submission.csv: a valid weak-format submission for all test rows.
> images/: 2,229 transformed JPEG images referenced by image_path.
> Columns in train.csv:
> id (string): row identifier.
> image_path (string): relative path to the transformed image.
> prompt (string): task instruction.
> pose_packet_json (JSON string): grid size, joint names, species tokens, visibility meanings, and maximum joint-card count.
> answer_format_json (JSON string): required output fields and value constraints.
> answer_json (JSON string): ground-truth posture profile for the training row.
> Columns in test.csv are the same except answer_json is omitted.
> The answer_json object must contain exactly these fields:
> species_token (string): cattle, horse, or sheep.
> visible_joint_count (integer): number of labeled joints with visibility 1 or 2.
> visible_joints (array of strings): union of occluded_joints and clear_joints. This includes every joint with visibility 1 or 2.
> occluded_joints (array of strings): joints labeled with visibility 1; these joints are present but visually occluded.
> clear_joints (array of strings): joints labeled with visibility 2; these joints are clearly visible.
> joint_cells (object): visible joint name to 12 by 12 grid cell, using cells r00_c00 through r11_c11.
> core_cells, front_leg_cells, rear_leg_cells (objects): subset maps for body-core, front-leg, and rear-leg joints.
> crowded_joint_cells (array of strings): cells containing at least two visible joints.
> body_bbox (array of four floats): normalized [x, y, width, height] box around the animal.
> posture_bin (string): sparse_visible_pose, sideways_long_body, upright_compact_body, or balanced_body_view.
> limb_span_bins (object): released limb-pair name to short, medium, long, or extended.
> joint_cards (array): up to 18 cards. Each card has joint, cell, uv normalized coordinate pair, and visibility value 1 or 2.
> Example answer_json shape:
> {"species_token":"cattle","visible_joint_count":4,"visible_joints":["neck","withers","tail_head","left_front_hoof"],"occluded_joints":["left_front_hoof"],"clear_joints":["neck","withers","tail_head"],"joint_cells":{"neck":"r04_c05","withers":"r04_c07","tail_head":"r05_c09","left_front_hoof":"r09_c04"},"core_cells":{"neck":"r04_c05","withers":"r04_c07","tail_head":"r05_c09"},"front_leg_cells":{"left_front_hoof":"r09_c04"},"rear_leg_cells":{},"crowded_joint_cells":[],"body_bbox":[0.18,0.21,0.64,0.68],"posture_bin":"sideways_long_body","limb_span_bins":{"neck__withers":"medium","withers__tail_head":"long"},"joint_cards":[{"joint":"neck","cell":"r04_c05","uv":[0.45,0.36],"visibility":2}]}
> Evaluation
> Each row receives a score between 0 and 1. Invalid JSON, invalid fields, or invalid values score 0 for that row while grading continues for other rows.
> For one row:
> raw_row_score = 0.05 * species_match
> + 0.04 * visible_count_score
> + 0.14 * visible_joint_f1
> + 0.06 * occluded_joint_f1
> + 0.06 * clear_joint_f1
> + 0.09 * joint_cell_map_f1
> + 0.05 * core_cell_map_f1
> + 0.05 * front_leg_cell_map_f1
> + 0.05 * rear_leg_cell_map_f1
> + 0.05 * crowded_cell_f1
> + 0.08 * bbox_score
> + 0.05 * posture_bin_match
> + 0.08 * limb_span_map_f1
> + 0.15 * joint_card_score
> visible_count_score = max(0, 1 - abs(predicted_count - true_count) / max(1, predicted_count, true_count)).
> List fields are scored with set F1. Map fields are converted to key:value items and scored with multiset F1. bbox_score = exp(-mean_absolute_bbox_error / 0.04).
> joint_card_score greedily matches predicted joint cards to true cards. A matched card receives 0.32 for exact joint, 0.22 for exact cell, 0.14 for exact visibility, and 0.32 * exp(-euclidean_uv_error / 0.045). The final card score divides the matched similarity sum by the larger of the predicted and true card counts.
> The leaderboard score is the mean row score over all test rows.
> After the component-weighted raw row score is computed, the grader applies a strictness transform to reduce credit for broad base-rate guesses: row_score = raw_row_score ^ 2.5. Perfect rows still score 1.0, malformed rows score 0.0, and partial rows must be close across several fields to retain substantial credit.
> Submission
> Submit a CSV with exactly these two columns:
> id (string): must match every test id exactly once.
> answer_json (JSON string): predicted posture profile using the schema above.
> Example:
> id,answer_json
> pose_1111111111111111,"{""species_token"":""cattle"",""visible_joint_count"":1,""visible_joints"":[""neck""],""occluded_joints"":[],""clear_joints"":[""neck""],""joint_cells"":{""neck"":""r06_c06""},""core_cells"":{""neck"":""r06_c06""},""front_leg_cells"":{},""rear_leg_cells"":{},""crowded_joint_cells"":[],""body_bbox"":[0.25,0.25,0.5,0.5],""posture_bin"":""balanced_body_view"",""limb_span_bins"":{},""joint_cards"":[{""joint"":""neck"",""cell"":""r06_c06"",""uv"":[0.5,0.5],""visibility"":2}]}"
> What Not To Use
> Do not use external image collections, annotation files, repositories, or dataset mirrors.
> Do not search for or match original images outside the provided files.
> Do not use hosted vision APIs, labeling services, or human-in-the-loop labeling for test rows.
> Do not use pretrained or fine-tuned checkpoints built specifically from the same image collection.
> Do not exploit row order, files outside the released package, package-generation code, or submission-format quirks.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Culture-Well Organoid Neighborhood Graph

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70kc9eq9bv96efv06nkq6he58bmr1g
- DOMAIN exactly as displayed: Prompt Engineering
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
> Given one microscopy image from a culture well, recover a local graph of the annotated organoid-like structures in that field of view. Organoids are small three-dimensional cell-culture structures used to study growth, development, and treatment response in laboratory wells. In these images, visible structures are annotated with morphology-stage tokens such as spheroid, cystic, and early budding.
> For each image, submit a JSON record whose main evidence is a set of representative structure nodes and stage-pair neighborhood edges. Each node describes a visible structure by stage, grid cell, size, aspect, and approximate bounding box. Each edge summarizes structures that share a cell or sit close together. Count totals, grid-cell sets, quadrant totals, and size histograms are included as consistency checks for the same graph.
> Dataset
> The files are:
> train.csv: 550 labeled examples.
> test.csv: 290 unlabeled examples.
> sample_submission.csv: a weak valid submission showing the required columns and JSON shape.
> images/: microscopy images referenced by image_path.
> Columns in train.csv:
> id (string): row identifier.
> image_path (string): relative path to the image.
> prompt (string): task instruction.
> packet_json (JSON string): image context. It contains grid ({"rows":10,"cols":10}), view (string), stage_tokens (list[string]), and max_morphology_cards (integer). stage_tokens always lists the four allowed stage tokens for the row.
> answer_format_json (JSON string): output schema summary.
> answer_json (JSON string): target organoid neighborhood graph record.
> Columns in test.csv are the same except answer_json is omitted.
> The submitted answer_json must contain:
> organoid_count (integer): total number of annotated visible structures.
> stage_counts (object): count for each stage token that appears.
> occupied_cells (list[string]): unique grid cells containing at least one structure.
> mixed_stage_cells (list[string]): cells containing more than one stage token.
> crowded_cells (list[string]): cells containing three or more annotated structures.
> quadrant_counts (object): counts for upper_left, upper_right, lower_left, and lower_right.
> size_histogram (object): counts for tiny, small, medium, and large.
> stage_cell_sets (object): mapping from each stage token to the grid cells where that stage appears.
> morphology_cards (list[object]): representative structure nodes, limited by the row's max_morphology_cards value in packet_json. In this release, every row has max_morphology_cards = 18. Each card contains stage (string), anchor_cell (string), bbox ([x,y,w,h] normalized floats), size_bin (string), and aspect_bin (round, oval, or elongated).
> stage_proximity_pairs (list[object]): stage-pair neighborhood edges. Each object contains a (string stage token), b (string stage token, with a <= b alphabetically), relation (same_cell or near_neighbor), and density (one, two, three, or four_plus).
> Grid cells use rXX_cYY, with rows r00 through r09 and columns c00 through c09.
> Quadrant boundaries are fixed: upper_left is rows r00-r04 and columns c00-c04; upper_right is rows r00-r04 and columns c05-c09; lower_left is rows r05-r09 and columns c00-c04; lower_right is rows r05-r09 and columns c05-c09.
> Evaluation
> Submissions are scored from 0 to 1. The final score is the mean row score over all hidden test rows.
> For each row:
> row_score =
> 0.04 * organoid_count_score
> + 0.08 * stage_count_f1
> + 0.09 * occupied_cell_f1
> + 0.06 * mixed_stage_cell_f1
> + 0.04 * crowded_cell_f1
> + 0.05 * quadrant_count_f1
> + 0.05 * size_histogram_f1
> + 0.07 * stage_cell_set_score
> + 0.28 * morphology_card_score
> + 0.24 * stage_proximity_pair_f1
> organoid_count_score = max(0, 1 - abs(predicted_count - true_count) / max(1, predicted_count, true_count)).
> For cell lists and count dictionaries, F1 is duplicate-aware: precision is matched submitted items divided by submitted items, recall is matched submitted items divided by true items, and F1 is 2 * precision * recall / (precision + recall). If both sides are empty, the F1 term is 1.
> stage_cell_set_score is the average F1 over all four allowed stage tokens listed in packet_json, not only over stages that appear in the row. For each token, the submitted cell set for that token is compared with the true cell set for that token. If a token is absent from both, that token's cell-set F1 is 1.
> morphology_card_score greedily matches submitted cards to true cards. For a matched card, similarity is 0.30*stage_exact + 0.25*anchor_cell_exact + 0.12*size_bin_exact + 0.08*aspect_bin_exact + 0.25*bbox_score, where bbox_score = max(0, 1 - mean_absolute_bbox_error / 0.075) over normalized [x,y,w,h]. The total matched-card score is divided by the larger of submitted-card count, true-card count, and 1.
> stage_proximity_pair_f1 is duplicate-aware F1 over complete (a, b, relation, density) edge records. A same_cell record means the paired structures fall in the same 10 by 10 grid cell. A near_neighbor record means their centers are close but not in the same cell.
> Malformed JSON or an invalid row schema scores zero for that row. The CSV must still have exactly the required columns and exactly the required ids.
> Submission
> Submit a CSV with exactly two columns:
> id (string)
> answer_json (JSON string)
> Example:
> id,answer_json
> org_11111111111111,"{""organoid_count"":2,""stage_counts"":{""spheroid"":2},""occupied_cells"":[""r04_c05""],""mixed_stage_cells"":[],""crowded_cells"":[],""quadrant_counts"":{""upper_right"":2},""size_histogram"":{""small"":2},""stage_cell_sets"":{""spheroid"":[""r04_c05""]},""morphology_cards"":[{""stage"":""spheroid"",""anchor_cell"":""r04_c05"",""bbox"":[0.45,0.35,0.05,0.05],""size_bin"":""small"",""aspect_bin"":""round""}],""stage_proximity_pairs"":[{""a"":""spheroid"",""b"":""spheroid"",""relation"":""same_cell"",""density"":""one""}]}"
> org_22222222222222,"{""organoid_count"":3,""stage_counts"":{""cystic_organoid"":2,""early_budding_organoid"":1},""occupied_cells"":[""r05_c03""],""mixed_stage_cells"":[""r05_c03""],""crowded_cells"":[""r05_c03""],""quadrant_counts"":{""lower_left"":3},""size_histogram"":{""small"":1,""medium"":2},""stage_cell_sets"":{""cystic_organoid"":[""r05_c03""],""early_budding_organoid"":[""r05_c03""]},""morphology_cards"":[{""stage"":""cystic_organoid"",""anchor_cell"":""r05_c03"",""bbox"":[0.30,0.52,0.08,0.07],""size_bin"":""medium"",""aspect_bin"":""round""}],""stage_proximity_pairs"":[{""a"":""cystic_organoid"",""b"":""early_budding_organoid"",""relation"":""same_cell"",""density"":""two""}]}"
> What Not To Use
> Do not use external image collections or annotation files.
> Do not search for matching original images or annotation records.
> Do not use hosted vision APIs.
> Do not use pretrained or fine-tuned checkpoints trained on this exact dataset.
> Do not manually label the test images.
> Do not exploit row order, hidden files, or package-generation details.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.


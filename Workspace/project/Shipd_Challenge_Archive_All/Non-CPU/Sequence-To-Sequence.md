# Non-CPU Sequence To Sequence Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed Non-CPU examples in this document: 78

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.

## Multibeam Sonar Strip Depth And Seafloor Hazard Triage

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx778qk10jhzj8f1m4nrk5ge6h89km00
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Problem Description
> Multibeam sonar surveys map the seafloor by sending a fan of acoustic beams from a moving vessel and converting the returning echoes into depth soundings across a narrow strip. Those depth strips help survey teams, cable planners, autonomous robots, and navigation-risk tools decide whether the next stretch of bottom is flat and predictable, steeply changing, rough, or uncertain enough to deserve caution.
> In this challenge, you only see a compact public prefix of each real sonar strip. Given numeric features from that partial strip, predict the withheld depth continuation and classify the local seafloor hazard profile.
> Overview
> You are given source-neutral rows derived from real multibeam sonar survey lines. Each row contains a partial along-track strip profile and compact summary features from the observed prefix only. For each test row, predict a fixed-length normalized withheld depth profile, the slope bucket, the roughness bucket, a practical hazard-zone label, and a confidence value.
> The public inputs are deliberately minimal: an opaque id, numeric prefix_profile, numeric strip_features, strip_length_bucket, and sensor_context. Raw file names, survey identifiers, day or line ids, coordinates, timestamps, source paths, and raw row order are not public. The intended approach is learned sequence/sensor modeling from the provided training rows, not public-source lookup or map download.
> What not to use: do not solve this as generic bathymetry-map lookup, global-grid interpolation, coordinate lookup, filename/order/id decoding, source-row recovery, or rule-only last-value extrapolation. Submissions should model the sonar strip continuation and terrain-risk heads from the public training data.
> Task Specification
> For every test id, submit exactly these predictions:
> depth_profile: exactly 24 semicolon-separated finite floats, each in [-8, 8], representing the normalized withheld strip continuation.
> slope_bucket: one of flat, gentle, steep, dropoff.
> roughness_bucket: one of smooth, moderate, rough, very_rough.
> hazard_zone: one of none, slope_hazard, rough_bottom, abrupt_change, uncertain.
> confidence: a finite float in [0, 1].
> The depth target is normalized enough that direct source matching is not a valid strategy, while preserving real seafloor shape. The class heads summarize the withheld segment, not the visible prefix alone.
> Dataset
> The public dataset contains train.csv, test.csv, and sample_submission.csv.
> Public Files
> Item	Description
> train.csv	labeled strip prefixes
> test.csv	hidden-label strip prefixes
> sample_submission.csv	valid dummy submission
> train.csv includes public inputs and all labels. test.csv includes only public inputs. The sample submission is a weak schema-valid baseline, not a competitive solution.
> train.csv Columns
> Column	Type	Description
> id	string	opaque row id
> prefix_profile	string	48 numeric values
> strip_features	string	56 coarse numeric values
> strip_length_bucket	string	swath-density bucket
> sensor_context	string	coarse context bucket
> depth_profile	string	24 target values
> slope_bucket	string	target slope class
> roughness_bucket	string	target roughness class
> hazard_zone	string	target hazard class
> confidence	float	target reliability
> prefix_profile is a semicolon-separated vector with exactly 48 numeric values. It is a coarse masked sketch of the visible strip context rather than a raw ping-by-ping trace. Values equal to the numeric marker 8.0, displayed in the CSV with normal decimal formatting such as 8.00, mark intentionally unreported sketch positions and should not be treated as true depth readings. strip_features is a semicolon-separated vector with exactly 56 coarse numeric values derived only from the public context. Public buckets are source-neutral and do not identify the original survey, line, day, coordinates, or timestamp.
> id is the opaque row identifier. prefix_profile is the observed normalized strip prefix. strip_features is a compact numeric summary vector from the observed prefix. strip_length_bucket is one of sparse_swath, standard_swath, or dense_swath. sensor_context is one of shallow_regular, shallow_patchy, mid_depth_regular, mid_depth_patchy, mid_depth_wide, deep_edge_regular, deep_edge_patchy, or deep_edge_wide. depth_profile is the withheld normalized continuation. slope_bucket, roughness_bucket, and hazard_zone are target classes for the withheld segment. confidence is the target reliability value.
> test.csv Columns
> Column	Type	Description
> id	string	opaque row id
> prefix_profile	string	48 numeric values
> strip_features	string	56 coarse numeric values
> strip_length_bucket	string	swath-density bucket
> sensor_context	string	coarse context bucket
> The test file has the same public input fields as the training file and withholds every target.
> For test.csv, id is the opaque row identifier to use in the submission. prefix_profile has exactly 48 semicolon-separated numeric values with the same 8.0 / 8.00 unreported-sketch marker used in training, strip_features has exactly 56 semicolon-separated coarse numeric values, strip_length_bucket uses the same three values as in training, and sensor_context uses the same source-neutral context vocabulary as in training. No hidden target columns are included.
> Submission Format
> Column	Type	Constraint
> id	string	exact test id
> depth_profile	string	24 floats
> slope_bucket	string	allowed class
> roughness_bucket	string	allowed class
> hazard_zone	string	allowed class
> confidence	float	0 to 1
> Submit exactly one row for every test id, with the columns in the exact order shown above.
> Example submission row descriptions:
> Row 1: id = ms_00154168fa0601; depth_profile = 0.120;0.110;0.090;0.070;0.050;0.030;0.020;0.010;0.000;-0.010;-0.020;-0.030;-0.040;-0.050;-0.060;-0.070;-0.080;-0.090;-0.100;-0.110;-0.120;-0.130;-0.140;-0.150; slope_bucket = gentle; roughness_bucket = moderate; hazard_zone = none; confidence = 0.62.
> Row 2: id = ms_001e0ef616c497; depth_profile = 0.000;0.030;0.050;0.090;0.130;0.170;0.220;0.270;0.330;0.390;0.450;0.510;0.580;0.660;0.740;0.830;0.930;1.040;1.160;1.290;1.430;1.580;1.740;1.910; slope_bucket = steep; roughness_bucket = rough; hazard_zone = slope_hazard; confidence = 0.57.
> Evaluation
> Invalid submissions raise an error rather than receiving a valid numeric score. Structural invalidity includes missing, extra, or reordered columns; duplicate ids; an id set different from test.csv; invalid categorical values; malformed depth vectors; non-finite values; and confidence outside [0, 1].
> For valid submissions, the score is a weighted blend of depth-continuation accuracy, the three class-label heads, confidence calibration, and worst hidden-subgroup robustness. The component weights are transparent: depth profile quality is 40%, slope macro-F1 is 18%, roughness macro-F1 is 16%, hazard macro-F1 is 18%, confidence calibration is 3%, and worst hidden-subgroup robustness is 5%.
> For one row, let PredDepth[j] and TrueDepth[j] be the 24 submitted and hidden normalized depth values. The row depth similarity is defined as follows:
> DepthMAE(row) = mean_j(abs(PredDepth[j] - TrueDepth[j]))
> DepthRMSE(row) = sqrt(mean_j((PredDepth[j] - TrueDepth[j])^2))
> RowDepth(row) = 0.72 * exp(-DepthMAE(row) / 1.05) + 0.28 * exp(-DepthRMSE(row) / 1.35)
> The full-score formula is:
> DepthScore = mean(RowDepth over all rows)^1.15
> SlopeScore = macro_f1(pred_slope_bucket, true_slope_bucket)^2
> RoughnessScore = macro_f1(pred_roughness_bucket, true_roughness_bucket)^2
> HazardScore = macro_f1(pred_hazard_zone, true_hazard_zone)^2
> ConfCal = mean(max(0, 1 - abs(pred_confidence - true_confidence) / 0.5))^2
> Base = 0.40 * DepthScore + 0.18 * SlopeScore + 0.16 * RoughnessScore + 0.18 * HazardScore + 0.03 * ConfCal
> WorstHidden = min over hidden subgroup buckets of Base(bucket) / 0.95
> Final = clip(Base + 0.05 * WorstHidden, 0.0, 1.0)
> macro_f1 is the standard unweighted mean F1 over the hidden classes present for that head. Base(bucket) recomputes the same depth, class, and confidence components on only the rows in that hidden bucket. Hidden subgroup axes are real sonar/seafloor groups such as slope regime, roughness regime, hazard type, depth range, target-gap bucket, and source-line robustness group. The private subgroup membership is not public, so participants should optimize by making models that work across all visible strip shapes and contexts rather than only the most common rows.
> The theoretical minimum is 0.0; the theoretical maximum is 1.0; higher is better. A perfect submission with the hidden labels scores exactly 1.0.
> Intended Solution
> Strong solutions should treat each row as a masked sequence-continuation problem. Train compact sequence models from scratch or fine-tune sequence encoders over the coarse strip sketch, unreported-position pattern, and source-neutral sensor context, then jointly predict the withheld depth profile, hazard heads, and confidence. Generic per-row methods should only be sanity checks, calibration helpers, or post-processing, not the whole solution.
> Simple last-value continuation, global train medians, metadata-only grouping, and nearest-neighbor prefix matching are intentionally weak. The training data teaches the normalization and terrain-risk conventions.
> Enforcement On Invalid Approaches
> Submissions based on public-source lookup, raw survey row recovery, external bathymetry-grid downloads, coordinate or timestamp reconstruction, source filename/path matching, hardcoded id-to-answer maps, manual labeling of hidden rows, or rule-only interpolation may be rejected before payout even if the CSV is structurally valid. The competition rewards learned sonar strip continuation and seafloor hazard triage from the provided public split.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Kinyarwanda Spoken Word Mixture Untangling

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ejasqsejbvvjj6pevpxkyhn8bkcya
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> This is a GPU-friendly audio sequence challenge. Each row contains a short WAV file made by mixing three real Kinyarwanda spoken-word clips. You are also given eight candidate keyword cards with row-local aliases such as K1, K2, and K8.
> Your task is to identify which three aliases were spoken and output them in their temporal onset order.
> In plain terms: listen to a short overlapping keyword mixture, choose the three words that are actually present, and put them in the order they start. Some rows are clean and staggered; others contain dense overlap, a quiet middle word, confusable prefix decoys, or low-level babble.
> The source audio comes from MLCommons Multilingual Spoken Words, using Kinyarwanda one-second keyword examples. Training mixtures are synthesized only from source train_pool speakers. Hidden test mixtures are synthesized only from disjoint test_pool speakers.
> This is not single-label keyword spotting, generic ASR, classification, or regression. A submission is a constrained three-token sequence over row-local aliases.
> Dataset files
> train.csv contains 2,400 rows. Each row has:
> id: string. Unique training row ID.
> audio_path: string. Relative path to the mixture WAV under the public directory.
> candidate_cards: JSON list. Eight candidate keyword cards for the row.
> mixture_condition: string. One of six public acoustic condition labels.
> expected_keywords: integer. Always 3.
> sample_rate: integer. Always 16000.
> duration_seconds: number. Mixture duration in seconds.
> target_sequence: string. Training-only answer, exactly three aliases separated by spaces.
> test.csv contains 1,200 rows. It has the same public columns as train.csv except target_sequence.
> sample_submission.csv contains every test ID with an empty prediction. It is structurally valid and scores 0.
> Mixture audio files are stored under:
> audio/train/: training mixture WAV files.
> audio/test/: hidden-test mixture WAV files.
> Candidate card schema
> Each candidate_cards item is a JSON object with:
> alias: string. Row-local keyword alias, one of K1 through K8.
> word: string. Kinyarwanda keyword text.
> char_count: integer. Number of characters in the keyword.
> vowel_count: integer. Number of Latin vowels in the keyword.
> prefix: string. First three characters.
> suffix: string. Last three characters.
> Aliases are row-local. K3 in one row has no relationship to K3 in another row.
> Task
> For each test row, submit exactly three aliases separated by single spaces. The aliases must be distinct and must come from K1 through K8.
> Valid prediction example:
> K4 K2 K8
> This means the solver predicts that alias K4 starts first, alias K2 starts second, and alias K8 starts third.
> Invalid row-level predictions score 0 for that row. Examples include empty strings, unknown aliases, duplicate aliases, more or fewer than three aliases, JSON, natural language, or comma-separated lists.
> Evaluation
> Structurally invalid submission files are rejected. Examples are missing columns, extra columns, duplicate IDs, unknown IDs, missing rows, or wrong column order.
> The grader aligns rows by id, not row order.
> For each row:
> ExactSequence is 1 if all three aliases are correct and in the correct order, else 0.
> PositionAccuracy is the fraction of the three positions with the exact correct alias.
> SetF1 is the fraction of the three target aliases recovered, ignoring order. Because every valid prediction and target has length three, this is intersection_size / 3.
> PairwiseOrder is the fraction of the three ordered alias pairs that appear in the correct temporal order.
> AdjacentOrder is the fraction of the two adjacent target links recovered exactly.
> The row score is:
> row_score =
> 0.45 * ExactSequence
> + 0.20 * PositionAccuracy
> + 0.17 * SetF1
> + 0.10 * PairwiseOrder
> + 0.08 * AdjacentOrder
> The 1,200 hidden rows are balanced across six acoustic families, with 200 rows per family:
> clean_stagger
> light_overlap
> buried_middle
> dense_overlap
> prefix_decoys
> babble_tail
> Family labels are present as mixture_condition, but source speakers and exact source clips are hidden. The worst-family term prevents solvers from ignoring overlap-heavy or quiet-word cases.
> The final score is:
> final_score =
> 0.70 * mean(row_score over all rows)
> + 0.20 * worst_family_mean
> + 0.10 * bottom_20_percent_mean
> Scores are finite and bounded in [0, 1]. The sample submission scores 0. A perfect oracle scores 1.
> Submission format
> Submit a CSV with exactly two columns in this order:
> id: string. Test row ID.
> predicted_sequence: string. Three distinct aliases separated by spaces.
> Example:
> id,predicted_sequence
> 0a12bc34de56f789,K4 K2 K8
> Recommended solution approach
> A basic solution can train a small spectrogram CNN or conformer-style audio encoder to predict the three active aliases and their order from the mixture. Stronger solutions should exploit the candidate word text, learn keyword embeddings, separate overlapping speech, and handle speaker-disjoint test clips.
> The challenge is designed for GPU use. The intended hardware is one NVIDIA A10G with a 90-minute runtime budget.
> What not to use
> Do not use row IDs, audio filenames, CSV row order, or fixed alias identities.
> Do not assume K1 K2 K3 or any fixed alias order is meaningful.
> Do not ignore onset order; recovering the correct set without order receives only partial credit.
> Do not optimize only clean mixtures. Dense-overlap, quiet-middle, prefix-decoy, and babble-tail rows affect worst-family and bottom-tail score.
> Do not submit word strings, JSON lists, comma-separated aliases, natural-language explanations, or extra columns.
> Benchmark boundary
> Standard keyword-spotting benchmarks ask whether a single word is present in one clip. Standard ASR benchmarks transcribe continuous speech. This benchmark sits between them: the vocabulary is row-local and visible, but the audio is an overlapped three-word mixture with distractor words and a required temporal alias sequence.
> The task is therefore not ordinary single-label keyword classification, full-sentence ASR, speaker identification, or audio tagging.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Federal Register Document Title Generation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx737p732hbwacv5et6g2hm5j189vsrr
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: text, generative, large-scale, Dataset source is visible after the challenge closes.
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Federal Register documents use compact official titles to summarize regulatory actions, notices, and agency procedures. In this challenge, each example contains a cleaned document context with the official title removed. Your task is to generate that title.
> This is a text-generation task. Good solutions should learn how agency names, document type, topics, CFR references, and abstract language map to concise Federal Register title phrasing.
> Files
> The solver-visible files are under ./dataset/public/.
> train.csv
> test.csv
> sample_submission.csv
> train.csv
> Training rows contain these columns:
> example_id: anonymized training example ID.
> document_type: Federal Register document type.
> agency_text: semicolon-separated agency names.
> topic_terms: semicolon-separated topic terms.
> cfr_titles: semicolon-separated Code of Federal Regulations title numbers when present. For example, title 21 refers to the Food and Drugs portion of the CFR.
> context: cleaned document abstract or summary text. HTML tags are removed, whitespace is normalized, URLs and Federal Register citation patterns are stripped, and exact title text plus distinctive long title words are removed. Contexts are clipped to at most 1600 characters.
> target_title: complete official action title to learn from. Source records whose complete official title is longer than 220 characters are excluded during preparation rather than truncated.
> test.csv
> Same as train.csv, but without target_title.
> sample_submission.csv
> A valid format template. It contains dummy placeholder title text and is not intended to score well.
> Submission Format
> Write your submission to:
> ./working/submission.csv
> The file must contain exactly these columns:
> example_id,predicted_title
> Example:
> example_id,predicted_title
> fr_0123456789abcdef,Airworthiness Directives; Example Aircraft Model
> fr_abcdef0123456789,Notice of Availability of Draft Guidance
> Validation rules match the grader exactly:
> The columns must be exactly example_id and predicted_title, in that order.
> Every test example_id must appear exactly once.
> Extra IDs, missing IDs, duplicate IDs, extra columns, and null values are invalid.
> predicted_title is converted to text before scoring, but it must not be blank after stripping whitespace.
> predicted_title must be at most 220 characters.
> ASCII control characters are invalid in predicted_title.
> Evaluation
> Submissions are scored with a normalized title-generation score. Before scoring, both predicted and true titles are lowercased and tokenized with the regular expression [a-z0-9]+.
> For each example, the grader computes:
> token F1 between normalized predicted-title tokens and true-title tokens,
> ordered-token LCS F1, which rewards preserving the target phrase order.
> Token F1 is computed from multiset token overlap:
> precision is overlapping token count divided by predicted token count,
> recall is overlapping token count divided by true token count,
> token F1 is two times precision times recall, divided by precision plus recall.
> LCS F1 uses the longest common subsequence length between the predicted-token sequence and true-token sequence:
> LCS precision is LCS length divided by predicted token count,
> LCS recall is LCS length divided by true token count,
> LCS F1 is two times LCS precision times LCS recall, divided by LCS precision plus LCS recall.
> The final per-example score is the weighted average:
> 0.70 times token F1 plus 0.30 times LCS F1.
> The leaderboard score is the mean over all test examples. Higher is better. The score range is 0.0 to 1.0.
> Rules
> Use only files in ./dataset/public/.
> Do not use internet access, external downloads, Federal Register source lookup, document-number reconstruction, private files, or hidden metadata.
> Do not install packages.
> Use libraries available in the Kaggle Python Docker image.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Ornament Rehearsal Corridor Compiler

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7aeyf4vcr23f5c2d2528eh798b0m9t
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat mrfizhz's score of 0.306!

Full challenge description from page:

> Overview
> For each ten-second vocal passage, identify the requested melodic ornaments and compile the smallest permitted set of rehearsal cuts that covers them.
> Every example provides:
> A mono WAV excerpt.
> A 12-cell spectrogram of the same excerpt.
> A text lesson contract naming the ornament codes to preserve and the maximum number of rehearsal cuts.
> Predict three structured outputs:
> | Output | Prediction |
> |---|---|
> | `ornament_spine` | Requested ornament events in chronological order |
> | `practice_cut_program` | Up to three non-overlapping cell intervals covering every requested event |
> | `coverage_matrix` | A six-by-twelve event-to-time occupancy certificate |
> This is an audio-visual, policy-conditioned sequence-to-sequence task. It is not a raga classifier, singer classifier, or ordinary multi-label ornament detector. A correct solution must recognize event timing, obey a per-example text contract, and compile a canonical interval plan.
> Musical And Educational Context
> Hindustani vocal music uses short pitch gestures and sustained-note behaviors that can be difficult to isolate during practice. A teacher may ask a student to focus on selected ornament families while avoiding a long replay of the entire lesson. The useful output is therefore not only “which ornaments occur.” It is an ordered event account and a compact set of practice windows that covers the requested evidence.
> The source material contains 4.08 hours of strongly annotated performances by two expert musicians, plus broadcast-derived material and accompaniment recordings. Event annotations provide onset, offset, and ornament codes. The prepared cases use the expert vocal recordings and convert the time annotations into a common 12-cell planning coordinate system.
> Dataset
> The prepared dataset contains 1,700 training cases and 800 test cases. Each source recording belongs to only one split. Public case IDs, audio filenames, and image filenames are opaque.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Public inputs and labels for 1,700 cases |
> | `test.csv` | Public inputs for 800 hidden-label cases |
> | `sample_submission.csv` | Schema-valid baseline submission |
> | `audio/` | Ten-second, mono, `16,000 Hz`, 16-bit WAV excerpts |
> | `spectrograms/` | `1040 x 540` RGB JPEG time-frequency panels |
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque identifier matching `^rp[0-9a-f]{22}$` |
> | `audio_path` | string path | Relative path to one ten-second WAV excerpt |
> | `spectrogram_path` | string path | Relative path to the paired spectrogram |
> | `lesson_contract` | string | Requested ornament codes, maximum cut count, cell count, and overlap rule |
> Example lesson contract:
> Preserve only H,K,Me;compile at most 2 cuts;12 equal cells;an event activates every cell it overlaps
> The contract is case-sensitive and uses the exact codes documented below. A requested code can be absent from the passage; in that case its coverage row remains zero and it contributes no spine token.
> Spectrogram Coordinate System
> The horizontal axis is divided into twelve equal cells labeled 00 through 11. Each cell spans one twelfth of the ten-second excerpt, approximately 0.8333 seconds. Frequency increases upward. Color indicates log spectral magnitude.
> A small gray footer mark is a layout checksum and has no target meaning.
> Ornament Codes
> | Code | Ornament |
> |---|---|
> | `H` | Holding note or nyas-like sustain |
> | `K` | Kanswar |
> | `Me` | Meend |
> | `G` | Gamak |
> | `Mu` | Murki |
> | `An` | Andolan |
> Case and suffix variants in the source annotations are canonicalized to these six codes.
> Target Columns
> | Column | Data type | Description |
> |---|---|---|
> | `ornament_spine` | ordered token string | Requested events in onset order, including repeated codes |
> | `practice_cut_program` | ordered interval string | One to three canonical cell intervals |
> | `coverage_matrix` | JSON binary matrix, shape `6 x 12` | Requested ornament occupancy by code and time cell |
> Ornament Spine
> The spine contains between two and ten tokens joined by >. Repeated adjacent ornaments remain repeated because they represent distinct annotated events.
> Example:
> K>Me>K>H>Me
> Only codes named by the lesson contract appear. The maximum accepted spine length is 60 characters.
> | Spine event count | Train | Test |
> |---:|---:|---:|
> | 3 | 128 | 53 |
> | 4 | 201 | 61 |
> | 5 | 240 | 105 |
> | 6 | 276 | 127 |
> | 7 | 267 | 109 |
> | 8 | 246 | 123 |
> | 9 | 194 | 122 |
> | 10 | 148 | 100 |
> Coverage Matrix
> Matrix rows always follow:
> H,K,Me,G,Mu,An
> Columns are cells 00 through 11. An entry is 1 when at least one requested event of that row’s ornament overlaps any portion of the cell. Otherwise it is 0.
> Example with abbreviated spacing:
> [
> [0,0,1,1,0,0,0,0,0,0,0,0],
> [0,0,0,1,1,0,0,0,0,0,0,0],
> [0,0,0,0,0,0,1,1,1,0,0,0],
> [0,0,0,0,0,0,0,0,0,0,0,0],
> [0,0,0,0,0,0,0,0,0,0,0,0],
> [0,0,0,0,0,0,0,0,0,0,0,0]
> ]
> The maximum accepted JSON string length is 250 characters.
> Practice Cut Program
> A cut token has the form:
> c<start_cell>-<end_cell>
> Both cell indices use two digits from 00 through 11. Start must not exceed end. Multiple cuts are joined by > and must be ordered and non-overlapping.
> Example:
> c02-04>c06-08
> The canonical program is derived from the submitted case’s true coverage:
> Find maximal contiguous runs of active matrix columns.
> If the number of runs does not exceed the contract budget, retain those runs.
> If there are too many runs, repeatedly merge the adjacent pair separated by the smallest number of inactive cells.
> Ties are resolved by merging the earlier pair.
> Continue until the number of intervals equals the budget.
> The program may contain fewer intervals than the budget when fewer active runs exist. The maximum accepted program length is 60 characters.
> | Cut count | Train | Test |
> |---:|---:|---:|
> | 1 | 1,024 | 490 |
> | 2 | 555 | 254 |
> | 3 | 121 | 56 |
> Split Isolation
> Recordings are grouped before window selection. A complete vocal recording cannot contribute excerpts to both training and test. The hidden split includes both experts and multiple lesson families, but holds out complete source recordings. Exact audio and spectrogram hashes are checked across the split.
> Submission Format
> Write the final CSV to:
> ./working/submission.csv
> It must contain exactly these columns in exactly this order:
> case_id,ornament_spine,practice_cut_program,coverage_matrix
> Every test case_id must appear once. Extra or reordered columns, duplicate IDs, unknown IDs, missing rows, and extra rows are rejected.
> Example:
> case_id,ornament_spine,practice_cut_program,coverage_matrix
> rp4f781ac95b03e296f103bd,K>Me>K>H>Me,c02-04>c06-08,"[[0,0,1,1,0,0,0,0,0,0,0,0],[0,0,0,1,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]]"
> Evaluation
> Submissions are evaluated with the Rehearsal Corridor Compilation Score:
> Score =
> 0.40 * OrnamentSpineScore
> + 0.25 * PracticeCutScore
> + 0.35 * CoverageMatrixScore
> Each component is averaged over all test cases before combination. Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> OrnamentSpineScore
> edit_similarity =
> 1 - token_Levenshtein_distance(true_spine, predicted_spine)
> / max(true_token_count, predicted_token_count, 1)
> row_spine_score =
> 0.14 * edit_similarity
> + 0.86 * exact_spine_match
> Token insertion, deletion, and substitution each cost 1.
> PracticeCutScore
> Let interval_F1 be standard set F1 over complete interval tokens. Let covered_cell_F1 be standard set F1 over the union of cell indices covered by the intervals.
> row_cut_score =
> 0.15 * interval_F1
> + 0.15 * covered_cell_F1
> + 0.70 * exact_program_match
> For sets A and B, precision is |A intersection B| / |B|, recall is |A intersection B| / |A|, and F1 is their harmonic mean. Two empty sets score 1; exactly one empty set scores 0.
> CoverageMatrixScore
> True active entries receive weight 3; true inactive entries receive weight 1.
> weighted_agreement =
> sum(weight[i,j] * 1[Y[i,j] = P[i,j]])
> / sum(weight[i,j])
> row_matrix_score =
> 0.18 * weighted_agreement
> + 0.82 * exact_matrix_match
> Malformed or overlong strings, unknown ornament codes, too many spine tokens, invalid or overlapping cuts, malformed JSON, wrong matrix shape, non-binary entries, and out-of-range cells receive zero for the affected component. Schema-valid malformed submissions receive a finite score.
> Reference Validation
> | Check | Result |
> |---|---:|
> | Exact hidden-answer submission | `1.0000` |
> | Packaged sample submission | `0.1306` |
> | Unique WAV payloads | `2,500 / 2,500` |
> | Unique spectrogram payloads | `2,500 / 2,500` |
> | Train-test source-recording overlap | `0` |
> | Train-test WAV-hash overlap | `0` |
> | Train-test image-hash overlap | `0` |
> | Unique training coverage matrices | `1,606` |
> | Unique test coverage matrices | `760` |
> Method Requirements
> Solutions may use the provided A10G GPU within the competition time limit. Audio encoders, spectrogram encoders, event detectors, sequence models, structured decoders, and open-weight pretrained models are allowed when trained or calibrated only with public training data.
> What Not To Use
> Do not use IDs, filenames, row order, media hashes, file sizes, or source naming patterns as label predictors.
> Do not match public excerpts to external copies of the original recordings or annotations.
> Do not use hidden answers, grader internals, split artifacts, or submission feedback as labels.
> Do not adapt parameters on hidden test cases or construct per-test lookup tables.
> Do not exploit duplicate rows, extra columns, malformed parser inputs, or oversized values.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Wrist Gesture Command Ledger Decoding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7aenqybwzs3sgxx9xd5nacnd8bm7kk
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat backprop's score of 0.608!

Full challenge description from page:

> Wrist Gesture Command Ledger Decoding
> Overview
> This is a wearable-signal sequence decoding challenge. For each row, you receive a short six-channel wrist sensor trace. The trace contains two to four hand gestures performed as a compact command phrase. Your task is to output the command ledger: the onset frame, row-local gesture alias, and intensity tier for every foreground gesture.
> In plain terms: read the wrist accelerometer/gyroscope signal and write down which hand gestures happened, when they started, and how strongly they appeared.
> The real-world motivation is assistive human-computer interaction. A wrist-worn controller for prosthetics, accessibility interfaces, or small devices must decode short gesture phrases from noisy muscle-motion signals, not just classify one isolated gesture. The examples are generated from real mechanomyographic recordings collected with a wrist-worn accelerometer and gyroscope. Train and hidden test rows use disjoint participants, and every row uses fresh gesture aliases such as C03 and C10.
> This is not image hand-gesture recognition, lip reading, video action recognition, or ordinary single-label classification. The prediction is a variable-length structured sequence.
> Dataset files
> The prepared public data has 6,000 training rows and 1,500 hidden test rows.
> train.csv contains:
> id: string. Unique training row ID.
> sensor_frame: string. A 6 by 160 quantized wrist-sensor frame encoded with 64 printable symbols.
> frame_shape: string. Always 6x160.
> frame_hop_ms: integer. Milliseconds represented by one frame. Always 25.
> gesture_cards: JSON list. The eleven row-local gesture aliases available in this row.
> channel_cards: JSON list. The six row-local sensor-channel descriptors.
> max_events: integer. Maximum allowed event tokens. Always 4.
> target_command_ledger: string. Training-only answer ledger.
> test.csv contains the same public columns but omits target_command_ledger.
> sample_submission.csv contains:
> id: string. Test row ID.
> predicted_command_ledger: string. Empty dummy ledger. The sample is valid and scores 0.
> Input field schemas
> sensor_frame:
> Type: string.
> Length: 960 characters.
> Shape: 6 channels by 160 frames, stored channel-major. The first 160 characters are channel 1, the next 160 are channel 2, and so on.
> Decoding alphabet: 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_.
> Decoding value: map each character to an integer from 0 to 63. Larger values indicate stronger positive calibrated sensor response; smaller values indicate stronger negative response.
> Meaning: the six channels are row-local calibrated mixtures of linear acceleration and angular-rate signals from a wrist-worn sensor.
> gesture_cards is a JSON list with exactly eleven objects. Each object has:
> gesture: string. Row-local alias from C01 through C11.
> label: string. Human-readable gesture label, such as finger snapping or wrist flexion.
> motion_group: string. Coarse gesture family, such as wrist, impact, finger-release, or thumb-pose.
> description: string. Short description of the physical motion.
> channel_cards is a JSON list with exactly six objects. Each object has:
> channel: string. Row-local channel name from X1 through X6.
> sensor_family: string. Either linear-acceleration or angular-rate.
> calibration: string. Short note that signs and gains are row-local normalized.
> Output grammar
> Submit one string per row in predicted_command_ledger.
> A non-empty ledger is a space-separated sequence of event tokens:
> T037:C04:I1 T091:C10:I2
> Token meaning:
> T037: gesture onset at frame 37.
> C04: row-local gesture alias from that row's gesture_cards.
> I1: intensity tier.
> Rules:
> Onset frames must be T000 through T159.
> Gesture aliases must be C01 through C11.
> Intensity tiers must be I0, I1, or I2.
> Submit at most 4 event tokens.
> Duplicate identical event tokens are invalid.
> An empty string is structurally valid but scores 0 because every hidden target has at least two events.
> Evaluation
> Structurally invalid submission files are rejected. Structural errors include missing columns, extra columns, duplicate IDs, unknown IDs, missing IDs, wrong row count, or wrong column order.
> Malformed row-level ledgers score 0 for that row instead of crashing the grader. Rows are aligned by id, not by row order.
> For each row, the grader parses predicted and hidden event sets. One-to-one matching is greedy by smallest onset distance.
> Definitions:
> StrictEventF1: F1 after matching events with the same gesture alias, same intensity tier, and onset distance at most 2 frames.
> GestureTimingF1: F1 after matching events with the same gesture alias and onset distance at most 5 frames, ignoring intensity.
> OnsetF1: F1 after matching events with onset distance at most 3 frames, ignoring gesture and intensity.
> GestureMultisetF1: multiset F1 over gesture aliases, ignoring onset and intensity.
> IntensityScore: after GestureTimingF1 matching, each matched event receives 1.0 for exact intensity, 0.5 for adjacent intensity tier, and 0 for a two-tier miss. The sum is divided by the number of hidden events; unmatched hidden events receive 0.
> CountScore: event-count agreement.
> ExactLedger: 1 only when the normalized predicted ledger exactly equals the hidden ledger.
> F1 is:
> F1 = 0 when there are no matches.
> F1 = 2 * matched_event_count / (predicted_event_count + hidden_event_count) otherwise.
> CountScore is:
> if predicted_event_count == 0:
> CountScore = 0
> else:
> CountScore =
> max(0, 1 - abs(predicted_event_count - hidden_event_count) / max(hidden_event_count, 3))
> Row score is:
> row_score =
> 0.42 * StrictEventF1
> + 0.20 * GestureTimingF1
> + 0.12 * OnsetF1
> + 0.10 * GestureMultisetF1
> + 0.08 * IntensityScore
> + 0.03 * CountScore
> + 0.05 * ExactLedger
> The hidden test set is balanced across five private generation families with 300 rows in each family:
> separated_pairs
> tempo_shifted_triplets
> overlap_bursts
> weak_middle_signal
> axis_dropout_phrase
> Family labels are not included in public files. They are used only for robust scoring.
> Final score:
> overall_mean = mean(row_score over all hidden rows)
> worst_family_mean = minimum family mean over the five private families
> bottom_20_mean = mean(row_score over the lowest-scoring 20% of hidden rows)
> final_score =
> 0.75 * overall_mean
> + 0.15 * worst_family_mean
> + 0.10 * bottom_20_mean
> Scores are finite and bounded in [0, 1]. The sample submission scores 0. A perfect oracle scores 1.
> Submission format
> Submit a CSV file with exactly two columns in this order:
> id: string. Test row ID from test.csv.
> predicted_command_ledger: string. Space-separated command ledger.
> Example:
> id,predicted_command_ledger
> 0a12bc34de56f789,T037:C04:I1 T091:C10:I2
> Do not submit JSON, arrays, Python code, natural-language explanations, extra columns, or multiple candidate ledgers.
> Recommended solution approach
> A basic solution can train a subject-disjoint time-series model from sensor_frame to ledger tokens. Stronger solutions should combine onset detection, gesture recognition, calibration-invariant channel modeling, intensity estimation, and sequence decoding. Small convolutional, recurrent, transformer, or neural-symbolic decoding approaches are all feasible under the runtime limit.
> What not to use
> Do not use source participant numbers, repetition numbers, source filenames, row order, or fixed meanings of aliases. These are absent from solver-facing rows or regenerated per row.
> Do not assume that one row contains only one gesture. Every hidden row contains a short command phrase with two to four events.
> Do not rely only on the largest peaks. Some rows contain a weak middle gesture, channel dropout, or overlapping gestures.
> Do not optimize only timing. Most score weight requires binding the correct gesture alias and intensity to the correct onset.
> Benchmark boundary
> Most related wearable-gesture datasets evaluate isolated gesture classification or continuous gesture detection with global gesture labels. This benchmark changes the task contract: each example is a generated command phrase made from real wrist mechanomyography, with subject-disjoint hidden participants, row-local gesture aliases, row-local channel calibration, variable event count, onset timing, intensity tiers, and robust subgroup scoring.
> It is therefore a wearable-signal sequence-to-sequence decoding benchmark, not a renamed accelerometer classification task and not a lip-reading/video benchmark.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Football Physical Performance Interpolation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70gw3xetkh0nmg9zs88mab158bjr03
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat mrnguyen's score of 0.433!

Full challenge description from page:

> Football Physical Performance Interpolation: TIP to OTIP Metric Generation
> OVERVIEW
> This challenge tasks you with building a sequence generation model that predicts a football player's 13 physical performance metrics during the defensive phase (Opponent-in-Possession) given ONLY their offensive-phase (Team-in-Possession) metrics, peak speed data, and positional context. The dataset comes from the Australian A-League 2024/2025 season and contains detailed physical tracking metrics derived from optical tracking systems. Each row represents a player's aggregated physical output for a specific positional role across the entire season.
> Critically, overall match metrics (the "All Minutes" statistics) are NOT provided in the input. This means the trivial shortcut of computing OTIP as ALL minus TIP is completely unavailable. The model must learn the genuine positional relationship between offensive-phase and defensive-phase physical output, which varies dramatically across positions and is non-linear.
> The output is a structured text sequence containing the 13 OTIP numeric values. There are no ratings, no phase deltas, no assessments, and no format compliance bonus. The scoring uses a steep penalised sMAPE curve so that a simple per-position median-ratio baseline scores low and only genuine predictive skill is rewarded. Every point in the score must be earned by accurate numeric prediction.
> DATA FILE STRUCTURE
> You are provided with the following files in the public directory:
> train.csv contains the training data with columns "id", "input", and "target". The "input" column holds a structured text sequence encoding the player's context and TIP physical metrics. The "target" column holds the ground truth sequence of 13 OTIP numeric values.
> test.csv contains the test inputs with columns "id" and "input". You must generate the "target" for each test row.
> sample_submission.csv shows the expected submission format with columns "id" and "target".
> metadata.json contains challenge metadata including the list of target metric names, scoring formula, and dataset sizes.
> INPUT FORMAT EXAMPLE
> A typical input sequence looks like this:
> [POS] Full Back [TEAM] Melbourne City FC [MIN] tip:30.07 otip:24.77 [MATCHES] 25 [TIP] distance:3774.68 mpm:125.53 running:599.44 hsr_dist:238.40 hsr_cnt:23.84 sprint_dist:91.76 sprint_cnt:4.64 hi_dist:330.16 hi_cnt:28.48 med_accel:41.92 high_accel:3.16 med_decel:33.20 high_decel:6.68 [PEAK] psv99:29.52 psv99_top5:31.24 [PREDICT_OTIP]
> Breaking down the input structure:
> The [POS] token indicates the player's position group. The [TEAM] token indicates the club. The [MIN] token provides minutes during team-in-possession and opponent-in-possession. The [MATCHES] token gives the number of matches played. The [TIP] block contains 13 physical metrics from team-in-possession phases only. The [PEAK] block contains 2 peak speed metrics (inherent physical capability). The [PREDICT_OTIP] token signals that the model should generate the opponent-in-possession metrics.
> Important: The overall "All Minutes" metrics are deliberately excluded from the input. This prevents the trivial shortcut of computing OTIP as ALL minus TIP.
> TARGET FORMAT EXAMPLE
> The corresponding target sequence looks like this:
> distance:3686.08 mpm:148.84 running:683.48 hsr_dist:263.04 hsr_cnt:24.44 sprint_dist:85.08 sprint_cnt:4.36 hi_dist:348.12 hi_cnt:28.80 med_accel:43.16 high_accel:1.88 med_decel:30.04 high_decel:4.76
> Each token follows the format metric_name:value where the value is a float formatted to two decimal places. The 13 target metrics in order are: distance, mpm, running, hsr_dist, hsr_cnt, sprint_dist, sprint_cnt, hi_dist, hi_cnt, med_accel, high_accel, med_decel, high_decel.
> These correspond to the Opponent-in-Possession physical performance: total distance covered, metres per minute, running distance, high-speed running distance and count, sprint distance and count, high-intensity distance and count, medium acceleration count, high acceleration count, medium deceleration count, and high deceleration count.
> SUBMISSION FORMAT
> Your submission must be a CSV file named "submission.csv" with exactly two columns: "id" and "target".
> The "id" column must contain integer IDs matching the rows in test.csv (0, 1, 2, and so on).
> The "target" column must contain your model's generated sequence for each test example. Each sequence must contain the 13 metric tokens in the correct order.
> Example submission row:
> id: 0
> target: distance:3450.22 mpm:142.10 running:620.55 hsr_dist:245.30 hsr_cnt:22.10 sprint_dist:78.40 sprint_cnt:3.80 hi_dist:323.70 hi_cnt:25.90 med_accel:40.50 high_accel:1.60 med_decel:28.30 high_decel:4.20
> Important format notes:
> All 13 metric tokens must be present in the correct order: distance, mpm, running, hsr_dist, hsr_cnt, sprint_dist, sprint_cnt, hi_dist, hi_cnt, med_accel, high_accel, med_decel, high_decel.
> Each numeric value must be a valid non-negative float.
> The separator between metric name and value is a colon. Tokens are separated by spaces.
> Missing tokens or unparseable values are treated as a prediction of 0.0 for that metric, which will receive a very low score under the penalised sMAPE metric.
> EVALUATION
> Your submission is evaluated using a single metric: penalised sMAPE. The final score ranges from 0.0 to 1.0, and the grading direction is Maximize.
> Scoring Formula
> For each of the 13 target metrics in each test row:
> Step 1: Compute the standard Symmetric Mean Absolute Percentage Error (sMAPE):
> sMAPE = 2 * |predicted - ground_truth| / (|predicted| + |ground_truth|)
> This is the standard formulation where the denominator is the average of the absolute values, equivalently written as (|predicted| + |ground_truth|) / 2, so the factor of 2 in the numerator cancels the /2 in the denominator.
> Step 2: Compute the per-metric score:
> per_metric_score = max(0, 1 - 6 * sMAPE)
> Step 3: The per-row score is the mean of the 13 per-metric scores.
> Step 4: The overall score is the mean of all per-row scores, multiplied by the coverage factor (fraction of test rows present in your submission).
> What the penalty factor of 6 means
> The factor of 6 makes the scoring curve steep. Here is what different levels of prediction error translate to in terms of per-metric score. These values are computed using the standard sMAPE formula above, assuming predicted and ground truth are both positive:
> A 0% relative error (perfect prediction) gives sMAPE of 0.000, yielding a score of 1.00.
> A 5% relative error gives sMAPE of approximately 0.049, yielding a score of 0.71.
> A 10% relative error gives sMAPE of approximately 0.095, yielding a score of 0.43.
> A 15% relative error gives sMAPE of approximately 0.140, yielding a score of 0.16.
> A 17% relative error gives sMAPE of approximately 0.157, yielding a score of 0.06.
> A 20% relative error gives sMAPE of approximately 0.182, yielding a score of 0.00.
> This means that even moderately inaccurate predictions receive very little credit. A simple per-position median-ratio baseline, which typically has 10-15% average relative error across metrics, will score in the range of 0.10-0.30. Only models that achieve consistently precise predictions across all 13 metrics will score above 0.50.
> Why this scoring was chosen
> The previous version of this challenge used a composite score that included position-relative ratings, phase intensity deltas, a natural-language assessment, and a format compliance bonus. These components were problematic because they are all deterministic functions of the 13 numeric values and publicly published formulas. Once the numbers are predicted, the ratings follow from the public position_percentiles.json, the deltas follow from the public threshold comparison, and the assessment follows from the public if-else template. Together with the 20% format compliance weight, these derivable components contributed roughly 70% of the total score for free, inflating scores and leaving no headroom for solvers to differentiate.
> The current scoring eliminates all derivable components and all format compliance weight. The score reflects only what actually has to be learned: the 13 OTIP numeric values. The steep penalty curve ensures that simple statistical baselines like the per-position median ratio score low, and only genuine predictive skill earns a high score.
> Coverage Penalty
> If your submission has fewer rows than the test set, the final score is multiplied by the fraction of test rows present. For example, submitting predictions for only 90 out of 100 test rows multiplies your score by 0.90.
> GOAL
> Build a sequence generation model that takes a structured text input describing a player's positional context, TIP physical metrics, and peak speed, and generates a structured text output predicting the player's 13 OTIP physical metrics as accurately as possible.
> The key challenge is that overall match metrics are NOT provided in the input. The model cannot simply compute OTIP as ALL minus TIP. Instead, it must learn the genuine positional relationship between offensive and defensive phase physical output, which varies dramatically across positions and is non-linear. A Centre Forward's defensive intensity profile is fundamentally different from a Full Back's, even when their TIP metrics look similar. The model must capture these positional nuances to achieve precise predictions.
> The steep scoring curve means that even moderate errors are heavily penalised. A model that predicts the right ballpark but is 15% off on average will score only around 0.16. Only models that achieve consistently precise predictions across all 13 metrics will score well.
> WHAT TO USE
> You may use any pre-trained sequence-to-sequence language model (such as T5, BART, BLOOM, GPT-2, or similar architectures) as a starting point. Fine-tuning a pre-trained model on the training data is the recommended approach.
> You may also use traditional ML approaches (gradient boosted trees, neural networks, etc.) by parsing the structured input into features and predicting each metric separately, then formatting the output as a sequence.
> You may use any deep learning framework (PyTorch, TensorFlow, JAX, Hugging Face Transformers, and so on).
> You may use data augmentation techniques, feature engineering, ensemble methods, or custom decoding strategies.
> You may parse the structured input into any intermediate representation that helps your model.
> You may compute position-specific statistics from the training data and incorporate them as features or constraints.
> WHAT NOT TO DO
> Do not attempt to look up or infer the test set ground truth from external sources. The test answers are hidden and any attempt to circumvent this violates the challenge rules.
> Do not copy the TIP metric values directly as OTIP predictions. The OTIP metrics are systematically different from TIP metrics and the relationship varies by position. Direct copying will result in poor numeric accuracy and a very low score under the steep penalty curve.
> Do not assume that a simple per-position median ratio of OTIP to TIP will score well. While this baseline captures the average relationship, individual players deviate significantly from the position average, and the steep penalty curve means that even 15% average error yields a score of only about 0.16.
> Do not submit fewer rows than the test set. Missing rows will reduce your score proportionally through the coverage penalty.
> Do not use the same prediction for all test rows. Each player has a unique physical profile that depends on their position, team, and individual capabilities.
> Do not submit predictions in any format other than the specified metric_name:value token sequence. The grader extracts numeric values using regex matching on the expected metric names. Other formats will not be parsed correctly and will receive a score of 0.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Simultaneous Classical Japanese Speech Translation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70p4810zagxw4dz4vb8mp3c98bkk3e
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat mango's score of 0.433!

Full challenge description from page:

> Simultaneous Classical Japanese Speech Translation
> Overview
> This challenge uses short audio clips of narrated classical, literary Japanese prose —
> archaic grammar, dropped subjects, and dense literary vocabulary that differ sharply from modern
> spoken Japanese. The goal is incremental / simultaneous translation: producing correct
> English from the portion of a passage you have heard so far, rather than waiting for everything.
> Each test item ships the first K sentences of a passage, where K is 1, 2, 3, or 4 (a
> passage is at most four sentences). You receive the audio of exactly those K sentences — when K
> is below the passage's full length the remaining sentences are withheld — and you output one
> English translation of what was said. Items with fewer sentences are weighted more, rewarding
> systems that produce correct English from less context (the real-time, low-latency case).
> This is not transcription (the input is Japanese audio, the output is English text), and it
> is not a single batch translation — each item is a passage prefix scored on its own. Test
> passages come from a work held out of training entirely, so validating on training passages can
> overestimate performance.
> Evaluation
> Submissions are scored with a bounded higher-is-better objective, StreamScore ∈ [0, 1]:
> per item i:  m_i = cosine( embed(translation_i), embed(reference_i) )
> q_i = clip((m_i - chance_floor) / (1 - chance_floor), 0, 1) * length_penalty_i
> StreamScore  = ( Σ_i w(f_i) * q_i ) / ( Σ_i w(f_i) )
> w = { 0.25: 0.35, 0.50: 0.30, 0.75: 0.20, 1.00: 0.15 }     # f = sentences shipped / 4
> reference_i is the human English translation of exactly the sentences you were given —
> aligned at sentence boundaries, not by word fraction.
> m_i is semantic similarity from a fixed sentence-embedding model: meaning is scored, not
> wording, because a correct literary translation uses different words than the reference (a
> character metric would score a correct answer almost like random text).
> chance_floor is the submission's own mean similarity on mismatched (item, reference) pairs,
> so generic or on-topic English maps to ≈ 0.
> length_penalty_i scales down output much longer than the reference, so translating sentences
> you were not given does not help.
> Every test item ships exactly 1, 2, 3, or 4 sentences (a passage's opening, maximum 4),
> so the fraction is f = (sentences shipped) / 4, giving exactly f ∈ {0.25, 0.50, 0.75, 1.00}.
> The four weights sum to 1.00 (0.35 + 0.30 + 0.20 + 0.15). Shorter prefixes weigh more (the
> real-time reward). Higher is better. See grade.py.
> Dataset
> The prepared public dataset (GPU / A10G runtime, ~1 hour):
> public/
> |-- train.csv
> |-- test.csv
> |-- sample_submission.csv
> |-- train/audio/
> +-- test/audio/
> There are 612 training rows and 272 test rows. Each test clip contains 1–4 whole sentences and
> ranges from about 3 to 40 seconds of audio (train clips are single sentences).
> train.csv columns:
> Column	Type	Description
> id	integer	Training row identifier
> audio_path	string	Relative path to the training clip (one sentence, full audio)
> ja_transcript	string	Japanese transcript of the clip
> en_reference	string	Human English translation of the clip
> test.csv columns:
> Column	Type	Description
> id	integer	Test row identifier
> audio_path	string	Relative path to the test clip — the audio of a passage's opening sentences
> Submission
> Submit a CSV file with exactly these columns:
> Column	Type	Description
> id	integer	Test id from test.csv
> translation	string	Your English translation of the audio you were given
> Example:
> id,translation
> 100000,"She had been waiting by the window since morning."
> 100001,"The road climbed higher and the air grew colder."
> 100002,"He said little, but his meaning was plain enough."
> (Illustrative placeholders, not real answers.)
> Requirements
> Exactly 272 rows — one per id in test.csv — plus a header row.
> Columns must be exactly id,translation; ids unique and matching test.csv exactly.
> (The grader rejects submissions with wrong columns, duplicate ids, or missing/extra rows.)
> Write the final submission to ./working/submission.csv. UTF-8, RFC-4180 quoting.
> Baselines
> sample_submission.csv contains empty translations and scores ≈ 0.00.
> Higher is better; an oracle (the exact reference translations) scores 1.00, so there is
> large headroom. When the challenge is created, an AI agent attempts it to set the baseline
> that solvers must beat.
> Allowed And Prohibited
> Allowed:
> Train models using the provided training labels (audio, Japanese transcript, English reference).
> Fine-tune public pretrained ASR / translation models; build an incremental / simultaneous
> policy; audio preprocessing; self-supervised learning on the provided public audio; ensembling
> and calibration.
> General-purpose libraries available in the execution environment (GPU / A10G).
> Prohibited:
> Do not use external datasets or any unprovided source materials, transcripts, or published
> translations.
> Do not attempt to identify, match, or recover the passages behind the clips — whether from
> outside sources or by stitching audio together across test items.
> Do not hardcode outputs or use per-id answer tables.
> Do not use external LLM APIs or any LLM-generated outputs in your submission.
> A genuinely trained / fine-tuned model is expected — not a frozen off-the-shelf pipeline
> copied across items.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Catalan Administrative Discourse Operator Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ekeg0e2ab5cdxayjr5f4p1h8bk4ez
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat alba's score of 0.551!

Full challenge description from page:

> Catalan Administrative Discourse Operator Reconstruction
> Overview
> Administrative documents depend on short connective phrases to express addition, contrast, consequence, sequencing, explanation, and related discourse transitions. When those phrases are missing, restoring them requires understanding both sides of each boundary and the larger sequence.
> This sequence-to-sequence challenge is configured for one NVIDIA GPU with 10 GB of VRAM. Every example contains six ordered sentence boundaries taken from one real public-administration document. The opening discourse operator at each boundary has been removed. All remaining words have been replaced with stable, collision-prone codes, so the task cannot be solved by external text lookup.
> Predict the six removed operators in order. Targets are opaque tokens from O00 through O25; the mapping from original phrases is intentionally not public. Repeated operator tokens are allowed.
> Every row also supplies a finite-field constraint. For that row, each operator token deterministically generates an invertible 2-by-2 matrix over the field modulo 17. Multiplying the six matrices in predicted order should reproduce the supplied boundary_matrix. Matrix multiplication is order-sensitive, and many different paths share the same boundary, so the constraint assists structured decoding without replacing contextual learning.
> Task
> For every row in test.csv, predict an operator_path containing exactly six operator tokens.
> context_sequence contains six gap sections:
> G1 through G6 identify the ordered gap positions.
> LEFT introduces the coded words before a gap.
> MASK marks the removed discourse operator.
> RIGHT introduces the coded words after the removed operator.
> NEXT_GAP separates consecutive gap sections.
> Codes matching w[0-9a-f]{4} are stable collision-prone lexical buckets.
> The same word normally receives the same code across rows, but unrelated words may collide. Structural markers, IDs, row order, seeds by themselves, and filenames do not encode target labels.
> Strong solutions should use a compact neural sequence encoder, learn contextual patterns for each gap, model dependencies across the six outputs, and use the matrix boundary during constrained decoding. Models, batches, and cached tensors must fit within 10 GB of GPU memory.
> Finite-Field Constraint
> The complete public construction is stored in operator_algebra.json.
> For an operator token and the row’s constraint_seed:
> Starting with counter 0, calculate SHA-256 of the ASCII string FFDOR1|constraint_seed|operator_token|counter.
> Reduce the first four digest bytes modulo 17 and interpret them as [a,b,c,d], representing [[a,b],[c,d]].
> If the determinant is zero modulo 17 or the matrix is the identity, increment the counter and repeat.
> Start from the identity matrix and right-multiply the six accepted matrices in submitted order, reducing every entry modulo 17.
> The hidden path’s product is the public boundary_matrix. Because the construction is instance-conditioned and highly many-to-one, boundary lookup across rows does not reveal the answer.
> A context-free meet-in-the-middle search can nevertheless enumerate all 26-cubed three-token prefixes and suffixes and always find at least one six-token path whose product equals the supplied matrix. The matrix-agreement component, worth 15% of the total score, can therefore be earned in full without learning discourse context. This is an intentional decoding aid, not evidence that the recovered path is the labelled path: many paths satisfy the same matrix, and the position, edge, edit, and exact-path components comprising the other 85% distinguish them using the hidden contextual target.
> Dataset
> train.csv contains 2,108 labelled rows.
> test.csv contains 702 unlabelled rows.
> sample_submission.csv is a valid training-only scaffold. It uses the per-position majority token from train.csv, never test labels.
> operator_algebra.json defines the allowed tokens, modulus, matrix layout, matrix-generation procedure, and ordered-composition rule.
> train.csv columns
> sample_id
> Type: string.
> Format: FFDOR_TR_ followed by six decimal digits.
> Meaning: synthetic row identifier assigned after train shuffling; it has no predictive meaning.
> context_sequence
> Type: string.
> Format: six space-separated masked-gap sections using the markers and word-code grammar described above.
> Meaning: anonymized left and right context for six ordered missing discourse operators.
> constraint_seed
> Type: string.
> Format: exactly 16 lowercase hexadecimal characters.
> Meaning: row-specific input to the public operator-matrix construction.
> boundary_matrix
> Type: string containing a JSON array.
> Format: [a,b,c,d], with four integers from 0 through 16.
> Meaning: ordered finite-field matrix product of the hidden six-token path.
> operator_path
> Type: string.
> Format: exactly six space-separated tokens from O00 through O25.
> Meaning: training-only target sequence in gap order.
> test.csv columns
> sample_id
> Type: string.
> Format: FFDOR_TE_ followed by six decimal digits.
> Meaning: synthetic row identifier assigned after an independent test shuffle; it has no predictive meaning.
> context_sequence
> Type: string.
> Format: the same six-section coded sequence used in train.csv.
> Meaning: anonymized input contexts requiring operator reconstruction.
> constraint_seed
> Type: string.
> Format: exactly 16 lowercase hexadecimal characters.
> Meaning: row-specific matrix-generation input.
> boundary_matrix
> Type: string containing a JSON array.
> Format: [a,b,c,d], with four integers from 0 through 16.
> Meaning: target path’s ordered matrix product modulo 17.
> sample_submission.csv columns
> sample_id
> Type: string.
> Format: one exact identifier from test.csv.
> Meaning: test row being predicted.
> operator_path
> Type: string.
> Format: exactly six space-separated allowed operator tokens.
> Meaning: predicted discourse-operator sequence.
> operator_algebra.json fields
> name — string; algebraic constraint name.
> modulus — integer; prime modulus 17.
> path_length — integer; required output length, 6.
> identity_matrix — array of four integers; flattened identity matrix.
> operator_tokens — array of strings; allowed output vocabulary.
> matrix_layout — string; flattened matrix interpretation.
> generation — string; deterministic instance-conditioned matrix procedure.
> composition — string; ordered right-multiplication procedure.
> The train/test split is performed by whole source-document families before independent shuffling. Documents sharing an exact participant-visible gap or six-gap window are grouped together. Preparation requires exactly 2,108 training rows and 702 test rows, exactly six visible gap sections per row, and zero train/test overlap for both complete contexts and individual masked-gap sections. It also verifies that all 26 operators occur in both partitions, with at least 30 training occurrences and 5 test occurrences per operator.
> Evaluation
> Each structurally valid submission receives the mean row score:
> score = 0.45 * A_position
> + 0.20 * F_edge
> + 0.15 * S_edit
> + 0.15 * A_matrix
> + 0.05 * I_exact
> A_position is the fraction of the six positions whose predicted token equals the hidden token.
> F_edge is multiset F1 over the five adjacent directed token pairs. For a path p1 p2 p3 p4 p5 p6, its edge multiset is (p1,p2), (p2,p3), (p3,p4), (p4,p5), (p5,p6). Direction is significant, so (O01,O02) differs from (O02,O01). Absolute edge position is not included: the same directed pair may match at a different edge position. Repeated pairs retain multiplicity, and overlap uses the minimum predicted and hidden count for each directed pair.
> S_edit is 1 - token_Levenshtein_distance / 6.
> A_matrix is the fraction of the four flattened product-matrix cells that equal the hidden product.
> I_exact is 1 when the complete six-token path is exactly correct and 0 otherwise.
> A perfect submission scores 1.0. Higher is better.
> An individual row receives zero if its operator_path is missing, contains anything other than O00 through O25, or does not contain exactly six space-separated tokens. Duplicate tokens are valid and are not an error.
> The entire submission is rejected when:
> the columns are not exactly sample_id,operator_path in that order;
> an ID is empty or duplicated; or
> the submitted ID set differs from the test.csv ID set.
> Submission
> Submit a UTF-8 CSV file with exactly these columns, in this order:
> sample_id,operator_path
> FFDOR_TE_000001,O08 O08 O08 O08 O08 O08
> FFDOR_TE_000002,O08 O08 O08 O08 O08 O08
> Each test ID must appear exactly once. Spaces separate tokens inside operator_path; do not use commas or JSON syntax inside that field. sample_submission.csv is the exact file-format template.
> Rules
> Use only the supplied challenge files and preinstalled runtime, including the preinstalled GPU libraries.
> Solutions must run on one NVIDIA GPU with at most 10 GB of VRAM and finish within 1.5 hours.
> GPU memory use must remain within the platform limit; compact encoders, mixed precision when supported, and bounded batches are recommended.
> Do not access the internet or install packages during execution.
> Do not use external corpora, source-text copies, reverse lookup, source-specific dictionaries, hidden files, IDs, or row order to recover targets.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Animal Habitat Profile Extraction & Inference

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx769c9edbrzv9r3vws1efyw3n89rxhv
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat imeintanis's score of 0.731!

Full challenge description from page:

> Habitat Dossier Normalization: turn a messy field record into a clean ecology profile
> Overview
> Field biologists rarely get clean data. A real occurrence record is a jumble of tag lists, half-filled free-text, dict-style notes, and geography — some of it inconsistent or mislabelled. Turning that mess into a tidy, analysis-ready profile is a daily task, and it rewards care.
> In this challenge each item is one animal's messy field record (higher taxonomy, behavioural tags, diet, mating notes, and biogeography). Your job is to normalize it into a strict 7-field ecology profile. Two kinds of field:
> Extraction fields — the evidence is present in the record, but messy. You must parse it and map it onto a controlled vocabulary, resolving synonyms and conflicts (e.g. a record tagged both Nocturnal and Diurnal normalizes to cathemeral).
> Inference fields — the source has been held out of the record. You must reason about them from the remaining ecology and geography. Specifically, an animal's habitats and climate are never stated in the record; you infer them.
> This is not a fit-one-classifier task. It is graded per field, and items span a difficulty gradient: harder records (more conflicts, broader ranges, more inference) count for more, so a thorough, well-reasoned solution scores materially higher than a quick one.
> The 7 fields and their controlled vocabularies
> Extraction (single value each):
> activity — one of: nocturnal, diurnal, crepuscular, cathemeral, unknown
> locomotion — one of: terrestrial, arboreal, aquatic, semiaquatic, fossorial, volant, unknown
> social — one of: solitary, social, unknown
> reproduction — one of: viviparous, oviparous, ovoviviparous, unknown
> trophic_guild — one of: carnivore, herbivore, omnivore, insectivore, piscivore, unknown
> Inference (a set; zero or more, semicolon-separated):
> habitats — any of: Agricultural, Caves, Coastal, Forest, Freshwater, Grassland, Marine, Mountains, Rainforest, Rocky areas, Savanna, Shrubland, Wetlands
> climate — any of: tropical, temperate, cold, arid, polar
> Use unknown for a single field when the record does not support a confident value. Matching is case-insensitive and tolerant of common synonyms and plurals (e.g. ocean→Marine, egg-laying→oviparous).
> Evaluation
> Each field contributes a field score, fields are combined by weight into an item score, and items are combined by difficulty weight into the final score.
> For animal i with difficulty tier t_i (an integer 1–4):
> single-value field: s_f = 1 if the normalized prediction equals the gold value, else 0
> multi-value field: s_f = 2 · |A ∩ B| / (|A| + |B|) (set Dice/F1 between predicted set A and gold set B; 1.0 if both empty)
> item score: item_i = ( Σ_f W_f · s_f ) / ( Σ_f W_f )
> final score: overall = ( Σ_i t_i · item_i ) / ( Σ_i t_i ), in [0, 1], higher is better.
> Field weights W_f — the genuinely hard, held-out habitats field dominates, so the score tracks habitat-inference quality rather than the easily-parsed fields:
> habitats = 20
> climate = 2
> activity = 1, locomotion = 1, social = 1, reproduction = 1, trophic_guild = 1
> Note on the split: train and test hold out entire taxonomic orders — every Order in the test set is absent from train. You therefore cannot memorise a taxonomy→habitat lookup; the habitats and climate fields must be generalised to unseen taxa. This is deliberate and is why strong solutions land well below a perfect score.
> The exact metric (this is what the grader computes):
> def evaluate(gold_rows, pred_rows, tiers, W):
> SINGLE = ["activity","locomotion","social","reproduction","trophic_guild"]
> MULTI  = ["habitats","climate"]
> num = den = 0.0
> for g, p, t in zip(gold_rows, pred_rows, tiers):
> item = 0.0
> for f in SINGLE:
> item += W[f] * (1.0 if canon(f, p[f]) == canon(f, g[f]) else 0.0)
> for f in MULTI:
> A, B = canon_set(p[f]), canon_set(g[f])
> dice = 1.0 if not A and not B else (0.0 if not A or not B
> else 2*len(A & B)/(len(A)+len(B)))
> item += W[f] * dice
> item /= sum(W.values())
> num += t * item; den += t
> return num / den
> Dataset
> The public/ folder contains:
> train.csv — 4962 rows: id, record (the messy input), tier (difficulty 1–4), and the seven gold fields, so you can learn/validate your normalization.
> test.csv — 1413 rows: id, record only (from taxonomic orders not present in train).
> sample_submission.csv — 1413 rows in the exact submission format (a constant baseline).
> Across the data an animal occupies about 2.58 habitats on average; many single fields are legitimately unknown for a given animal. Difficulty tiers in train are roughly 781/3156/741/284 for tiers 1/2/3/4.
> Submission
> A CSV with exactly these columns, one row per test id (1413 rows plus header):
> id, activity, locomotion, social, reproduction, trophic_guild, habitats, climate
> Single fields hold one token; habitats and climate hold a semicolon-separated set (possibly empty). A valid submission looks exactly like this (these are real test.csv ids):
> id,activity,locomotion,social,reproduction,trophic_guild,habitats,climate
> AD-003664,nocturnal,fossorial,solitary,viviparous,carnivore,Forest;Grassland;Rainforest;Savanna;Shrubland,temperate;tropical
> AD-000671,nocturnal,arboreal,social,viviparous,herbivore,Forest;Freshwater,tropical
> AD-003279,diurnal,terrestrial,solitary,viviparous,insectivore,Agricultural;Forest;Grassland;Rainforest;Savanna;Shrubland,tropical
> Requirements
> Provide exactly the 1413 test ids, each exactly once. A missing, duplicate, or unrecognised id makes the submission invalid.
> Column names must be exactly the seven field names plus id. Extra columns are ignored; a renamed or missing required column is invalid.
> Single fields must be one token from that field's vocabulary (use unknown if unsure). Values outside the vocabulary score as wrong for that field.
> habitats and climate are semicolon-separated sets; order does not matter and duplicates are collapsed. An empty set is allowed.
> Matching is case-insensitive and tolerant of common synonyms/plurals; unresolvable tokens are dropped, never fatal.
> Allowed methods and what not to use
> This is a closed-book task. You must produce every prediction using only the provided files and your own on-the-fly reasoning over them. There is no internet at solve time.
> Allowed — the only inputs you may use:
> public/train.csv (records + gold fields + tier) and public/test.csv (records) — including any statistics, patterns, or models you learn from these files only.
> Your own general reasoning about the text in each record. Standard, offline libraries in the runtime image (pandas, scikit-learn, etc.) for modelling.
> This is what you must not use and will lead to immediate disqualification of your solution — you cannot use external source verification or external-style locomotion/volancy reasoning while developing the solution.'
> Prohibited — using any of these disqualifies the submission, regardless of score:
> The internet / any network access at solve time — no web search, no browsing, no API calls, no runtime downloads, no fetching model or data files.
> External datasets, trait databases, gazetteers, or knowledge bases about these organisms — explicitly including (but not limited to) TetrapodTraits, EltonTraits, AmphiBIO, PanTHERIA, GBIF, iNaturalist, the IUCN Red List, Wikipedia/Wikispecies, or any field guide or encyclopedia. Do not import, hard-code, paste, or otherwise inject facts from such sources (e.g. a taxon's volancy, diet, or habitat).
> Re-identifying the masked species (its name and name-bearing text are removed) and then using pretrained or memorised knowledge of that species or its taxon to look up any answer field. Reasoning must generalise from the record, not recall an external fact about the specific animal or family.
> Pretrained model weights that encode external biological knowledge used to supply answers (as opposed to a model you fit on train.csv).
> Reading, reconstructing, or reverse-engineering the private answer key; and relying on the id or row order (ids are randomised and carry no signal).
> Enforcement is harness-side: solutions run in a no-network, no-external-data environment, and any run whose visible trajectory shows web search or use of an external biological reference is disqualified even if its score is high. If you are unsure whether a source is allowed, it is not — use only train.csv and the record in front of you.
> Prior work / why this is novel
> This is a real, openly-licensed corpus (see the dataset documentation for the exact CC0 source), not a synthetic set and not a known benchmark. Its mechanism is deliberately different from the usual single-label trait classification: it is a graded, difficulty-weighted normalization task that combines extraction of messy in-record evidence with inference of deliberately held-out fields, scored per field so that thoroughness and reasoning both move the score. The nearest neighbours — trait databases and species-description NLP — expose the target in the input, predict a single class, or are graded by one flat metric; none pose held-out-field inference over a masked, messy record under a difficulty-weighted, per-field score.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Thermochemical Voxel-to-Token Sequence Translation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dcgb40ptbr7mrk50amtxam58bkk9v
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat khoango6804's score of 0.514!

Full challenge description from page:

> Overview
> High-accuracy reference atomization energies are expensive, while approximate electronic-structure methods exhibit structured errors that depend on both the method and molecular environment. This is a multimodal sequence-to-sequence translation challenge. Each source message is an episode of eight molecule-method queries represented by anonymous method symbols, perturbed energy values, elemental inventories, and four-channel 3D density fields. The required translation is one ordered target sentence containing exactly eight vocabulary tokens.
> Each target token communicates the method-conditioned error band of one query after a training-only elemental-composition calibration has been removed. The target sentence is not an absolute energy, a scalar regression value, or a single class label. Solvers must translate eight aligned multimodal source segments into the position-anchored token language Q1L* ... Q8L*. The eight molecules in an episode are unrelated and each source molecule appears only once, so the sentence cannot be recovered through a fixed phrase table, repeated-molecule lookup, or dependencies between output positions.
> Source Representation
> The benchmark is derived from a curated computational thermochemistry archive. A high-accuracy reference energy is used only during hidden target construction and is never released in the prepared public files. Eight lower-cost electronic-structure methods are represented by stable anonymous integer codes from 0 through 7. Source names, record identifiers, method names, exact geometries, and reference values do not appear in the prepared release.
> The complete elemental inventory is stored as counts over 15 supported atomic numbers. Separately, at most three randomly selected atoms contribute to a coarse 3D field. Before voxelization, their coordinates are centered and subjected to a random orthogonal transform, mild affine distortion, random scaling, additive noise, and quantization. Gaussian densities are deposited on a 12\times12\times12 grid and separated into four broad element channels. The field is finally quantized to uint8. The released field is therefore a lossy spatial observation rather than a searchable copy of the source coordinates.
> The approximate atomization energy is divided by atom count, independently recalibrated, perturbed with small noise, and quantized. It is useful evidence, but it is not an exact searchable copy of the source value.
> Challenge Construction
> Only records with finite high-accuracy reference values and finite results for all eight selected approximate methods are eligible. A composition must occur at least eight times in the source derivative. Molecules are split by an element-labeled molecular-graph hash, so the same graph cannot occur in both train and test.
> Each eligible molecule is assigned exactly one method code, with global method balance. Molecules are then randomly arranged into eight-query episodes and independently permuted across the eight output positions. The training release contains 5,016 episodes, or 40,128 molecule-method queries. The test release contains 1,664 episodes, or 13,312 queries.
> For molecule i, method m, and atom count N_i, the raw per-atom method error is
> r_{i,m}=\frac{E^{\mathrm{approx}}_{i,m}-E^{\mathrm{ref}}_i}{N_i}.
> A shrunk composition-and-method mean b_{c,m} is fitted using training molecules only. The adjusted error is
> e_{i,m}=r_{i,m}-b_{c(i),m}.
> For each anonymous method separately, the training adjusted errors are divided at their 20th, 40th, 60th, and 80th percentiles. These boundaries assign the vocabulary suffixes L1 through L5. Test target sentences use the unchanged training boundaries.
> Input Encoding
> All model inputs for one eight-query episode are stored in the input_blob column of train.csv or test.csv. The value is ASCII Base85 encoding of a zlib-compressed binary payload. After decompression, the payload begins with the five-byte format marker TMDG1, followed by three fixed-layout tensors in this order:
> fields — shape [8, 4, 12, 12, 12], dtype uint8, 55,296 bytes.
> compositions — shape [8, 15], dtype uint8, 120 bytes.
> queries — shape [8, 2], little-endian float32, 64 bytes.
> The payload contains no pickle, executable object, path, source identifier, or hidden label. Decode Base85, decompress with zlib, verify the TMDG1 marker, then read the tensors from the fixed byte offsets above.
> The fields tensor should be divided by 255 before being passed to a neural network. Its four density channels are:
> hydrogen, atomic number 1;
> atomic numbers 3 through 5;
> atomic numbers 6 through 9;
> atomic numbers 11 through 17.
> Each field is sampled on the same cubic grid. Its quantized values encode the sum of Gaussian densities contributed by the observed atoms in that channel.
> The final axis of compositions contains atom counts in this fixed atomic-number order:
> [1, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17]
> The final dimension of queries contains:
> method_code — anonymous integer-valued code from 0 through 7.
> approximate_tae_per_atom — perturbed and quantized approximate total atomization energy divided by atom count.
> Position 0 in each decoded tensor maps to token Q1, position 1 maps to Q2, and so on through Q8.
> Target Language
> The target sentence contains exactly eight space-separated tokens in this fixed order:
> Q1L* Q2L* Q3L* Q4L* Q5L* Q6L* Q7L* Q8L*
> The output vocabulary contains five band symbols at each position:
> L1 — adjusted method error in the lowest method-specific band.
> L2 — adjusted method error in the second band.
> L3 — adjusted method error in the middle band.
> L4 — adjusted method error in the fourth band.
> L5 — adjusted method error in the highest method-specific band.
> For example:
> Q1L2 Q2L5 Q3L1 Q4L3 Q5L4 Q6L2 Q7L5 Q8L1
> Tokens must use the position prefix shown above. Reordering otherwise correct symbols changes the sentence and is an error.
> What The Task Requires
> Useful sequence models must combine three kinds of evidence: the anonymous method identity, the approximate energy observation, and molecular features learned from elemental composition plus the 3D density field. Constant sentences, method-frequency phrase tables, energy-only decoding, ID memorization, and train-sentence retrieval do not capture the graph-disjoint test behavior. The hidden construction reference is not present in the prepared inputs, while partial observation, spatial perturbations, voxelization, and quantization make record recovery unreliable.
> This benchmark is designed for GPU encoder-decoder training. A compact 3D CNN or vision transformer can encode each source segment, while a position-aware Transformer decoder emits the eight-token target sentence. Hybrid voxel encoders with autoregressive or teacher-forced token decoders are appropriate. The reference GPU voxel-to-token model trains for 20 epochs in approximately 6–8 minutes on a modern GPU. CPU summary-feature models are valid but intentionally much less competitive.
> What Not To Use
> Do not use private test labels, manually hard-coded test sequences, or information obtained from the grader. Do not treat opaque IDs, CSV row order, array order, archive metadata, or file fingerprints as predictive features. These values identify rows only and are independently constructed across the split.
> Only the released prepared training data may be used. External datasets, independently acquired reference energies, record linkage, reverse lookup, source reconstruction, and attempts to recover hidden identifiers are outside the task. The challenge must be solved from the prepared public training labels and decoded public input_blob values.
> Do not snap predictions to complete target sequences observed in training, model the eight outputs as a closed codebook, or infer one position from another. The eight positions contain unrelated molecule-method queries, and nearly all test sequences are new combinations.
> Classical tabular models are allowed, but collapsing the 3D field to hand-crafted summaries is intended only as a weak baseline. Competitive solutions should learn spatial representations and decode the complete output sentence with a GPU sequence model rather than rely solely on composition, energy, frequency tables, or aggregate voxel statistics.
> Dataset Files
> train.csv — training episode IDs, compressed input blobs, and target sequences.
> test.csv — test episode IDs and compressed input blobs.
> sample_submission.csv — valid submission schema and token syntax.
> The grader additionally receives a private answers.csv file containing test IDs and hidden target sequences.
> CSV Columns
> train.csv contains:
> id (string) — opaque episode identifier.
> input_blob (string) — Base85-encoded, zlib-compressed fixed-layout GPU input payload.
> target_sequence (string) — eight ordered training tokens.
> test.csv contains:
> id (string) — opaque episode identifier.
> input_blob (string) — Base85-encoded, zlib-compressed fixed-layout GPU input payload.
> sample_submission.csv contains:
> id (string) — test episode identifier.
> target_sequence (string) — placeholder sequence showing the required eight-token format.
> Evaluation
> For distance-aware sequence evaluation, the five vocabulary suffixes are mapped to ordered indices 0 through 4. This mapping is used only to give near-miss tokens partial credit; the submitted object remains one serialized token sentence. For output position p, let y_{i,p} be the hidden token index and \hat y_{i,p} be the submitted token index. The position-specific normalized error is
> \rho_p =
> \frac{\sum_i(\hat y_{i,p}-y_{i,p})^2}
> {\min_{k\in0,1,2,3,4}\sum_i(k-y_{i,p})^2}.
> Each position has its own denominator. The raw skill is computed over all eight positions with equal weight:
> s_{\mathrm{raw}}=1-\frac{1}{8}\sum_{p=1}^{8}\rho_p.
> The raw skill can be negative when a submitted sentence is worse than the best constant vocabulary symbol. The calibration below is defined for every real value of s_{\mathrm{raw}}; its first branch assigns 0.001 whenever s_{\mathrm{raw}}\le 0.128, including all negative values.
> The reported leaderboard score expands the useful operating range of this deliberately difficult benchmark without changing model ranking. Define the monotonic calibration function
> g(s)=
> \begin{cases}
> 0.001, & s\le 0.128,
> 0.001+\dfrac{s-0.128}{0.230-0.128}(0.500-0.001), & 0.128<s\le 0.230,
> 0.500+\dfrac{s-0.230}{1-0.230}(1-0.500), & s>0.230.
> \end{cases}
> The final score is \operatorname{clip}(g(s_{\mathrm{raw}}),0.001,1.0).
> Higher is better. A perfect submission scores 1.0, and non-perfect scores remain strictly ordered above the lower threshold rather than saturating at the ceiling. Constant or malformed submissions receive the clipped minimum of 0.001.
> Submission Format
> Submit one CSV with exactly two columns:
> id,target_sequence
> tmd_0123456789abcdef0123,Q1L2 Q2L5 Q3L1 Q4L3 Q5L4 Q6L2 Q7L5 Q8L1
> Every test ID must appear exactly once. Extra columns, missing IDs, duplicate IDs, unknown IDs, missing values, wrong token counts, invalid position prefixes, and vocabulary symbols outside L1 through L5 are invalid and receive 0.001.
> Expected Output
> Your submission must contain 1,664 rows and exactly eight ordered tokens per row. Scores are returned as a single float in the inclusive range [0.001, 1.0].

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Reconstructing Full Prose from Telegraphic Compressions

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73ky1jhtvz6qjjepc6pywzcn8bgbs5
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat faahmily's score of 0.476!

Full challenge description from page:

> Reconstructing Full Prose from Telegraphic Compressions
> Overview
> Telegrams were priced per word, so senders stripped messages to their skeleton: "ARVD BALTIMORE TUESDAY STOP SEND FUNDS OFFICE STOP". Each item in this challenge is one telegraphic-style compressed message; your model must reconstruct the exact original sentence — restoring the dropped articles, auxiliaries, prepositions, possessives and pronouns, expanding telegraph abbreviations, and recovering the original casing and punctuation. Compression is lossy and ambiguous ("a" vs "the", "is" vs "was", which preposition was dropped), so reconstruction must be learned from the training pairs, not looked up in a rulebook.
> Real-World Motivation
> Archives hold enormous collections of historical telegrams and telegraphic dispatches — diplomatic cables, business wires, news flashes — that are hard for modern readers to parse and nearly useless for full-text search or NLP pipelines because the function-word skeleton of natural language is missing. A model that expands telegraphese into faithful full prose makes these collections readable, searchable, and machine-processable. The same capability transfers to modern highly elliptical text (headlines, logs, clinical shorthand).
> What Makes This Different
> This is not sentence compression (which maps long → short; this task is the harder inverse with an exact-wording target), not paraphrase generation (the gold output is the unique original sentence), and not punctuation/casing restoration (those restore surface features of otherwise complete text; here whole word classes are missing and must be regenerated correctly in context). The evaluation is echo-normalized: any submission equivalent to trivially recasing the input scores 0, so the entire score range measures genuine reconstruction skill.
> Data
> train.csv — 20,202 rows, columns: id (string, format TG followed by six digits, e.g. TG004217), telegram (string, uppercase telegraphic message with STOP separators, typically 4-20 words), original (string, the exact original sentence, 8-26 words, natural casing and punctuation).
> test.csv — 2,360 rows, columns: id, telegram (same formats as train; no original column).
> sample_submission.csv — the required submission format, filled with a weak naive baseline. Train and test are disjoint by source book: no test sentence comes from a book seen in training, so memorizing book-specific phrasing does not transfer; the compression style is identical across splits.
> Target and Submission
> Submit a CSV with exactly two columns: id, prediction.
> Exactly one row per test id; no missing, extra, or duplicate ids.
> prediction is your reconstructed sentence (non-empty string).
> Predictions absurdly longer than the input (over 6x telegram length) are rejected.
> Example of a correctly formatted submission.csv:
> id,prediction
> TG000007,"He had received the letter on Tuesday morning, and answered it at once."
> TG000012,"The account was settled before they arrived at the office."
> Evaluation
> Echo-Normalized Reconstruction Score (ENRS), averaged over items, range 0–1, higher is better. For each item, similarity is character n-gram F1 (n = 1–4, averaged) between your prediction and the original; the score is that similarity normalized so that a no-skill baseline — the telegram trivially lowercased with STOP converted to periods — scores exactly 0 and a perfect reconstruction scores exactly 1: score = clip((sim(pred, original) − sim(trivial, original)) / (1 − sim(trivial, original)), 0, 1). Interpretation: ~0.00 echo or trivial recasing; ~0.05 random function-word insertion; higher values require correctly deciding which words were dropped, what they were, and where they belong, plus true casing and punctuation. Some items are inherently ambiguous, so a perfect corpus-level score is not reachable — strong models land well below 1.
> Compute
> This challenge is designed for GPU solving. The intended solution class is fine-tuning a pretrained open-weights sequence-to-sequence or language model (e.g., T5/ByT5/FLAN-T5 family or similar) on the 20k training pairs — comfortable within the time limit on the provided GPU, impractical with rule-only CPU approaches, which score near 0 by construction of the metric.
> Restrictions / Prohibited Methods
> No source retrieval: do not query, scrape, or match sentences against Project Gutenberg, any book corpus, search engine, or web source to recover the original text. Reconstruction must come from a model trained on the provided training data. Violations are grounds for rejection regardless of score.
> No hard-coded per-id answers or lookup tables against reconstructed sources.
> No hosted or closed-source API models at any stage (training, distillation, pseudo-labelling, or inference). Open-weights pretrained models are permitted as generic backbones; fine-tuning them on the provided train.csv is allowed and expected, but they must not have been previously tuned on this challenge's data.
> No probing for private answers, no training or calibrating on the test inputs' hidden targets, no grader or platform side channels.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Vessel Maneuver Program Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7115y6sc75dzmnvfxf1ec3698args4
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat darkone's score of 74.828!

Full challenge description from page:

> Vessel Maneuver Program Reconstruction
> Overview
> Recover a hidden maneuver program from a partially observed stream of symbolic motion measurements. Each row contains 20 ordered motion tokens. The first ten tokens expose a lossy context sequence, while the final ten expose displacement and turn-rate evidence from a query sequence whose heading and speed channels are withheld. Your submission must reconstruct those two hidden channels as a variable-length run-length program.
> This is a sequence-to-sequence reconstruction task, not coordinate regression or one-label classification. The hidden structure is the joint evolution of heading and speed across the query sequence. Every target is derived deterministically from real motion measurements; missing values occur only in the public observation, never in the answer.
> Observation encoding
> observation_program contains ten p tokens followed by ten q tokens, from p00 through p09 and from q00 through q09. Every token has this form:
> pSS:fBB:lBB:hBB:vBB:rBB
> SS is the zero-based position within its ten-step section.
> f is forward displacement relative to the course at p00.
> l is lateral displacement relative to the course at p00; positive values point to starboard.
> h is wrapped heading offset relative to the course at p00.
> v is speed offset relative to the speed at p00.
> r is rate of turn.
> xx means that component is unavailable.
> All q-section h and v components are xx because they are the channels to reconstruct. Some other components are independently unavailable. The missingness pattern does not depend on the answer.
> Let Δx and Δy be consecutive projected-coordinate changes and let θ be the course at p00, expressed clockwise from north. The unquantized rotated displacements are:
> f = Δx sin θ + Δy cos θ
> l = Δx cos θ − Δy sin θ
> Heading differences are wrapped to the half-open interval [−180°, 180°). A feature with ordered edges e₀ through eₘ₋₁ receives code 00 below e₀, code kk in [eₖ₋₁, eₖ), and code mm at or above eₘ₋₁.
> The public feature edges are:
> f: −50, 0, 50, 100, 150, 200, 250, 350
> l: −100, −40, −15, −5, 5, 15, 40, 100
> h: −30, −12, −5, −2, 2, 5, 12, 30
> v: −2, −0.8, −0.25, 0.25, 0.8, 2
> r: −20, −7, −2, 2, 7, 20
> Thus f, l, and h use codes 00 through 08; v and r use codes 00 through 06. zone_code is an opaque categorical operating-zone identifier from z00 through z06.
> Target encoding
> For each q position, the hidden heading state is the quantized wrapped course offset from p09, using the published h edges. The hidden speed state is the quantized speed offset from p09, using the published v edges.
> This change of reference is intentional. Observation-channel h and v codes describe motion relative to the beginning of the context at p00, whereas target h and v states describe how the query continues relative to the final context state at p09. Equivalently, the target heading offset is the wrapped query-course offset from p00 minus the wrapped p09 course offset from p00, with the result wrapped again to [−180°, 180°) before quantization. The target speed offset is the query speed offset from p00 minus the p09 speed offset from p00 before quantization.
> Adjacent positions with the same joint heading-speed state are run-length encoded. A segment token has the form:
> nDD:hHH:vVV
> DD is a duration from 01 through 10.
> HH is a heading state from 00 through 08.
> VV is a speed state from 00 through 06.
> Segment durations must sum to exactly ten. Adjacent tokens cannot repeat the same hHH:vVV pair. Program length therefore varies from one through ten tokens.
> The intended first-order approach is to combine the visible query displacement geometry with the context heading and speed history, then use sequential consistency and turn-rate evidence to reconstruct the hidden joint program.
> Evaluation Metric
> The score combines two ordinal agreement terms and one structural boundary term. All terms are computed globally over the 1,800 test rows.
> Expand every submitted and target program into ten heading states, ten speed states, and nine possible between-step boundary indicators.
> For an axis with K ordered classes, let Oᵢⱼ be the number of positions with true class i and predicted class j. Let Aᵢ = Σⱼ Oᵢⱼ, Pⱼ = Σᵢ Oᵢⱼ, N = Σᵢⱼ Oᵢⱼ, and Eᵢⱼ = AᵢPⱼ ÷ N.
> Define quadratic weights Wᵢⱼ = (i − j)² ÷ (K − 1)².
> The clipped quadratic weighted kappa is Q = clip[0,1](1 − Σᵢⱼ WᵢⱼOᵢⱼ ÷ Σᵢⱼ WᵢⱼEᵢⱼ). If the denominator is zero, Q is 1 only when the two expanded arrays are identical and 0 otherwise.
> Compute Qₕ with K = 9 for heading and Qᵥ with K = 7 for speed.
> Across the nine boundary positions per row, let TP, FP, and FN have their standard binary meanings. Boundary F1 is B = 2TP ÷ (2TP + FP + FN). If this denominator is zero, B = 1.
> The final score is S = 100 × clip[0,1](0.40Qₕ + 0.35Qᵥ + 0.25B).
> An empty, malformed, noncanonical, or otherwise invalid program is replaced for that row by maximally distant heading and speed endpoints and the inverse of the true boundary mask. It cannot act as an abstention. A valid file with poor programs may score 0. A perfect reconstruction scores exactly 100. Higher is better.
> Measured reference scores using only train.csv for fitting and test.csv for inputs were:
> Constant central-state program: 0.000000
> Context-only recent-trend heuristic: 18.559451
> ExtraTrees sequence regressor: 45.322579
> Fixed geometry and Random Forest hybrid: 58.141604
> Perfect reconstruction: 100.000000
> Dataset
> The public challenge package contains three files:
> train.csv — 9,000 rows with sample_id, zone_code, observation_program, and maneuver_program.
> test.csv — 1,800 rows with only sample_id, zone_code, and observation_program.
> sample_submission.csv — 1,800 rows with sample_id and a valid placeholder maneuver_program.
> sample_id is a content-free integer identifier. Train and test vessels are disjoint, no exact zone_code plus observation_program input occurs in both partitions, and timestamps, vessel identifiers, source filenames, coordinates, and raw track identifiers are absent from all public files.
> Submission
> Submit a CSV with exactly 1,800 rows and exactly these columns in this order:
> sample_id - string or integer - test identifier copied without modification.
> maneuver_program - string - one canonical variable-length program whose durations sum to ten.
> The header is required. IDs may appear in any row order, but duplicate, missing, or unknown IDs, a wrong row count, extra columns, or reordered columns cause the submission to be rejected. Invalid program strings are accepted as rows but receive the explicit worst-case treatment described above.
> Example using real test IDs:
> sample_id,maneuver_program
> 7130,n10:h04:v03
> 6805,n03:h03:v03 n07:h04:v03
> 4519,n02:h04:v02 n05:h05:v03 n03:h05:v04
> What Not to Use
> A constant n10:h04:v03 program fails because chance-corrected ordinal agreement and boundary F1 remove its majority-state advantage.
> Context-only linear continuation ignores the query displacement view and performs poorly when the maneuver changes after p09.
> Treating the row as a single classification example discards the ten-position structure and cannot place segment boundaries.
> Lookup by vessel, timestamp, filename, coordinates, ID ranges, or public row order cannot work because those keys are removed and the identifier ordering is content-free.
> Ignoring xx masks or assuming each code is nominal throws away ordinal and geometric information.
> Successful approaches should fuse the two sequence sections, exploit the published geometry and ordinal bins, model dependencies between adjacent query positions, and decode a canonical run-length program.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Diel Oxygen Regime Transcription

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7er6jn81abacfan00zp5871589tpps
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat draken_dev's score of 0.668!

Full challenge description from page:

> Diel Oxygen Regime Transcription
> Overview
> At a water-quality monitoring station, a multi-parameter sonde continuously records the physical state of the water — temperature, specific conductance (salinity/ion load), and turbidity (suspended sediment). What managers actually care about, though, is the dissolved-oxygen (DO) regime: whether the water is hypoxic (oxygen-starved, a pollution and fish-kill hazard), low, healthy, or supersaturated by an afternoon algal bloom. DO is measured by a separate, failure-prone, and often-absent optical probe.
> Your task is to transcribe the unobserved dissolved-oxygen regime sequence of one day from the co-observed physical channels. Each example is a single 24-hour (diel) window from one station. You are given the hourly sequence of water temperature, specific conductance, and turbidity for that window. You must output the sequence of 24 DO regime tokens — one per hour — even though dissolved oxygen itself is never provided.
> This is hard because dissolved oxygen is governed by the daily photosynthesis–respiration cycle and by pollution loading, which the physical channels only partially reveal; because the test stations are different stations from the training ones (you must generalise to a site you have never seen); and because the ecologically critical hypoxic hours are rare and must be recovered, not averaged away.
> The readings are real USGS field data from Sacramento–San Joaquin Delta monitoring stations. Station identifiers have been anonymised and absolute dates removed; only the hour of day is retained.
> What you predict
> For each window id, a target_sequence: a string of exactly 24 characters, one per hourly step, drawn from this regime alphabet (dissolved oxygen in mg/L):
> H — hypoxic, DO < 5 mg/L (oxygen stress / impairment).
> L — low, 5 ≤ DO < 7.5 mg/L.
> N — normal, 7.5 ≤ DO < 9.5 mg/L.
> S — supersaturated, DO ≥ 9.5 mg/L.
> Character t (0-indexed) is your predicted regime for hourly step t of that row's input_sequence.
> Evaluation
> Submissions are scored by a rarity- and transition-weighted macro-F1 over the four regime tokens, in [0, 1], higher is better. The 'twenty-four hourly positions' of every window are pooled (after aligning your rows to the answer key by id), then:
> Each position carries a weight w = class_weight[true_token] * transition_factor.
> class_weight = {H: 3.863, L: 2.454, N: 1.334, S: 2.203}. These are sqrt(1 / frequency) of each regime in the corpus (H 6.7%, L 16.6%, N 56.2%, S 20.6%), so the rare hypoxic regime is worth the most and a constant guess cannot farm the score.
> transition_factor = 1.5 if the true token differs from the previous hour's true token (a regime change), else 1.0. Correctly placing the onset and recovery of an episode matters more than restating a steady state.
> For each regime c, weighted true-positive, false-positive and false-negative masses are accumulated and F1_c = 2*TP / (2*TP + FP + FN).
> The final score is the unweighted mean of the four F1_c.
> Equivalent reference implementation of the core computation:
> def evaluate(y_true, y_pred):
> # y_true, y_pred: lists of equal-length 24-char strings over {H,L,N,S}, row-aligned by id
> CW = {"H": 3.863, "L": 2.454, "N": 1.334, "S": 2.203}
> toks = ["H", "L", "N", "S"]
> TP = {c: 0.0 for c in toks}; FP = dict(TP); FN = dict(TP)
> for t_seq, p_seq in zip(y_true, y_pred):
> for i, (t, p) in enumerate(zip(t_seq, p_seq)):
> w = CW[t] * (1.5 if i > 0 and t_seq[i] != t_seq[i-1] else 1.0)
> if p == t: TP[t] += w
> else:      FP[p] = FP.get(p, 0.0) + w; FN[t] += w
> f1 = []
> for c in toks:
> d = 2*TP[c] + FP[c] + FN[c]
> f1.append(2*TP[c]/d if d > 0 else 0.0)
> return sum(f1) / len(f1)
> A prediction that is the wrong length, contains an unknown character, or is missing is scored as fully incorrect for that window (worst outcome), never as a crash.
> Dataset you are given
> The prepared data live under public/:
> train.csv — labelled windows. Columns:
> id (string) — unique window identifier.
> site_id (string) — anonymised monitoring-station code. Windows from the same station share a code. The stations in test.csv do not appear in train.csv.
> input_sequence (string) — the 24-hour co-observed channel sequence (format below).
> target_sequence (string) — the 24-character DO regime sequence to be predicted.
> test.csv — the same columns except target_sequence, which you must produce.
> sample_submission.csv — a correctly formatted, label-free example submission with randomly chosen regime tokens.
> input_sequence format
> A string of 24 hourly steps separated by ;. Each step is HH,temp,spc,turb:
> HH — hour of day, 00–23 (the steps are 24 consecutive hours of one day/night cycle).
> temp — water temperature (°C).
> spc — specific conductance (µS/cm).
> turb — turbidity (FNU).
> Any of the three channel values may be empty (a real probe gap) — e.g. 03,,208,16.6 has a missing temperature. Dissolved oxygen is deliberately absent. The published channel values also carry a small anonymising perturbation (they are not exact instrument readings), so they cannot be matched verbatim against external records. Example of the first two steps: 02,15.1,208,16.6;03,14.9,208,16.8;....
> Submission format
> A CSV with a header and exactly one row per id in test.csv, with two columns id and target_sequence. Any additional columns are ignored. Example (ids are real test ids; regime strings shown are illustrative of the format only):
> id,target_sequence
> OBS10019098,NNNNNNNNNNNSSSSSSSSNNNNN
> OBS10368832,NNNNNLLLLLLHHHLLLNNNNNNN
> OBS10506332,NNNNNNNNNNNNNNNNNNNNNNNN
> Requirements
> Exactly 878 rows, one for every id in test.csv; the id set must match exactly — no missing, extra, or duplicated ids (any mismatch is rejected).
> target_sequence must be exactly 24 characters, each one of H, L, N, S, with no spaces or separators. Position t is the regime for step t of that row's input_sequence.
> The train-label format and the submission format are identical (a 24-character regime string).
> Produce predictions by modelling the inputs; hard-coding or copying the answer key is disallowed and detectable.
> What not to use
> No pretrained model weights, no external datasets, and no network access or downloads at train or inference time.
> Do not attempt to re-identify the source station or timestamps and look dissolved-oxygen values up in any external database (for example, USGS). Station ids are anonymised and absolute dates were removed specifically to prevent this; using such a lookup is cheating.
> (The automated grader cannot see your code and cannot enforce these rules; they are enforced by the evaluation harness and by review.)
> Prior work
> The nearest public tasks are single-label water-potability / water-quality classification (one categorical verdict per sample, not a sequence) and dissolved-oxygen forecasting (predict future DO from past DO and other channels). This task is neither. It is a cross-channel sequence transduction: reconstruct the entire unobserved DO regime trajectory of a diel cycle from only the co-observed physical channels, at a monitoring station held out of training. Because dissolved oxygen never appears in the input, the persistence/autoregressive shortcut that dominates DO-forecasting benchmarks is unavailable; the score is driven by inferring the biogeochemical oxygen state — especially the rare hypoxic hours — and by generalising the physical-to-oxygen relationship to an unseen site. The combination of held-out-channel diel transcription, a station-disjoint spatial split, and a hypoxia-weighted sequence metric does not correspond to any existing public benchmark.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Layered Icon Stack Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7anqz195e4hxxadey93mmvr18bkjw9
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat sensi's score of 0.143!

Full challenge description from page:

> Layered Icon Stack Reconstruction
> Overview
> This is a GPU-oriented computer-vision challenge about recognizing overlapping pictograms and reasoning about which ones are in front. Each row contains one 256 by 256 image made by stacking six anonymous icon instances. The icons partially cover one another, may be rotated or recolored, and are mixed with visual noise.
> Your task is to output the six candidate aliases that actually appear in the image, ordered from back layer to front layer.
> In plain terms: look at a messy pile of icons, decide which six icons from the candidate list are present, and recover the hidden stacking order. This is not image classification, scalar regression, or ordinary object detection. A valid answer is a short ordered sequence of row-local aliases.
> The source artwork comes from OpenMoji. Training and test scenes use disjoint source icons, and public rows do not include source hexcodes, filenames, or stable icon IDs.
> Dataset files
> train.csv contains 2,160 rows. Each row has:
> id: string. Unique training scene ID.
> image_path: string. Relative path to the 256 by 256 PNG scene.
> scene_card: JSON object. Canvas size, candidate count, present count, and target-order convention.
> candidate_cards: JSON list. Twenty-four row-local candidate icon cards.
> target_stack: string. Training-only answer: six aliases ordered back to front.
> test.csv contains 900 rows. It has the same public columns as train.csv but omits target_stack.
> sample_submission.csv contains every test ID with an empty dummy prediction. It is structurally valid and scores 0.
> Generated image files are stored under:
> images/train/: training PNG scenes.
> images/test/: test PNG scenes.
> Field schemas
> scene_card is a JSON object with:
> canvas_size: list of two integers. Always [256, 256].
> candidate_count: integer. Always 24.
> present_count: integer. Always 6.
> target_order: string. Always back_to_front.
> output_separator: string. States that aliases should be separated by single spaces.
> Each candidate_cards item is a JSON object with:
> alias: string. Row-local candidate alias such as I03.
> group_hint: string. Broad visual group hint, such as animals-nature, objects, or symbols.
> subgroup_hint: string. More specific source subgroup hint.
> label_hint: string. Short source-derived natural-language label.
> tag_hint: string. A short comma-separated tag hint.
> Aliases are row-local. I03 in one row has no relationship to I03 in another row.
> target_stack, present only in train.csv, is a space-separated sequence of exactly six aliases. The first alias is the back-most rendered icon. The last alias is the front-most rendered icon.
> Example target:
> I14 I03 I21 I08 I17 I02
> ## **Task**
> For each test image, submit `predicted_stack`: six candidate aliases ordered from back layer to front layer.
> Valid prediction example:
> I14 I03 I21 I08 I17 I02
> The grader also accepts a JSON list of aliases such as:
> ["I14","I03","I21","I08","I17","I02"]
> Predictions with duplicate aliases, unknown aliases, invented aliases, more than 12 aliases, empty strings, or malformed JSON score 0 for that row.
> ## **Evaluation**
> Structurally invalid submission files are rejected. Examples are missing columns, extra columns, duplicate IDs, unknown IDs in full-answer grading, missing IDs, or wrong column order. The grader aligns rows by ID, not row order.
> For each valid row:
> - `PresentF1` is F1 between the predicted alias set and the six true present aliases.
> - `OrderedPairF1` is F1 over all ordered alias pairs. For a sequence `A B C`, the ordered pairs are `(A,B)`, `(A,C)`, and `(B,C)`.
> - `AdjacentLinkF1` is F1 over adjacent ordered pairs. For `A B C`, the adjacent pairs are `(A,B)` and `(B,C)`.
> - `ExtremeAccuracy` gives half credit for identifying the two back-most aliases and half credit for identifying the two front-most aliases.
> - `ExactStack` is 1 if the full sequence exactly matches the target stack, else 0.
> The row score is:
> row_score = 0.34 * PresentF1
> 0.26 * OrderedPairF1
> 0.20 * AdjacentLinkF1
> 0.10 * ExtremeAccuracy
> 0.10 * ExactStack
> The 900 hidden rows are balanced across six private rendering families:
> - `clear_offset`
> - `radial_overlap`
> - `tight_occlusion`
> - `low_contrast`
> - `small_dense`
> - `edge_clipped`
> Each family has 150 hidden rows. Family labels are private and are used only for subgroup-robust scoring.
> The final score is:
> final_score = 0.72 * mean(row_score over all rows)
> 0.18 * worst_family_mean
> 0.10 * bottom_20_percent_mean
> Scores are finite and bounded in `[0, 1]`. The sample submission scores 0. A perfect oracle scores 1.
> Participants can compute training metrics locally, but cannot exactly compute hidden `worst_family_mean` or bottom-tail behavior without the private answers.
> ## **Submission format**
> Submit a CSV with exactly two columns in this order:
> 1. `id`: string. Test row ID.
> 2. `predicted_stack`: string. Space-separated aliases, back to front.
> CSV example:
> id,predicted_stack 0a12bc34de56f789,I14 I03 I21 I08 I17 I02
> ## **Recommended solution approach**
> A simple approach can train a CNN or vision transformer to score image/candidate pairs, then use a second model or heuristic to infer layer order from occlusion patterns. Stronger approaches should combine visual-text matching, candidate-set calibration, and pairwise front/back reasoning. The intended hardware is one NVIDIA A10G-class GPU within a 90-minute solution budget.
> ## **What not to use**
> - Do not use row IDs, row order, alias numbers, or candidate-card order as semantic signals.
> - Do not assume all candidate aliases are present. Exactly 6 of 24 candidates are present.
> - Do not treat this as single-label classification; every row requires a six-item ordered sequence.
> - Do not search for source hexcodes, filenames, or exact source IDs. These are intentionally absent from solver-facing files.
> - Do not submit bounding boxes, probabilities, natural language, image files, or extra columns.
> - Do not optimize only easy separated scenes. Worst-family and bottom-tail scoring penalize failure on tight, low-contrast, small, and clipped scenes.
> ## **Benchmark boundary**
> This differs from ordinary emoji classification and standard object detection. The solver is not asked to name one icon or draw boxes for a fixed class vocabulary. This is a completely original and highly novel task. The row contains a new candidate set, source-disjoint icons, heavy overlap, and a hidden z-order. The benchmark measures candidate grounding plus occlusion-aware sequence recovery.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Visuo-Tactile Four-Phase Motion Program Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73g4ty8by5kbxj0s7rwvxhrd8b4kps
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat khoango6804's score of 0.496!

Full challenge description from page:

> Overview
> Contact-rich manipulation produces three synchronized visual streams: one wrist-mounted scene view and two optical tactile views that record deformation at the gripper surfaces. Behind these observations is a continuous motion trajectory describing translation, rotation, and gripper opening.
> This challenge withholds the trajectory. Participants receive only compact, appearance-suppressed residual sequences derived from the three synchronized views. The task is to recover a four-phase motion program and emit an ordered sequence of exactly eight tokens. Each phase contributes one motion-axis token followed by one signed-intensity token.
> The required grammar is:
> phase_1_axis phase_1_intensity phase_2_axis phase_2_intensity phase_3_axis phase_3_intensity phase_4_axis phase_4_intensity
> Unlike ordinary action recognition, the target is not a task name. Unlike behavioral cloning, the benchmark does not ask for a continuous next action. Unlike video forecasting, the complete sensory consequence of the manipulation is observed. The model must invert those consequences into a compact, mixed categorical-ordinal control program.
> Object appearance, task identity, timestamps, source filenames, and raw trajectory values are removed. The wrist stream primarily exposes scene-relative motion, while the tactile streams expose local deformation and gripper interaction. Recovering the program therefore requires temporal reasoning and multimodal fusion rather than recognizing a visible object or memorizing a task label.
> Source Representation
> Each source demonstration contains synchronized observations from:
> one wrist-mounted fisheye camera;
> two optical tactile cameras mounted on the gripper surfaces;
> a six-degree-of-freedom tool-center-point trajectory;
> a gripper-opening trajectory.
> Only demonstrations containing all three video streams and a complete synchronized trajectory are retained.
> The trajectory is used privately to construct the target sequence. It is never included in the released challenge inputs.
> Challenge-Side Construction
> Every retained demonstration is normalized to a common temporal coordinate from 0 to 1. Twenty-four synchronized observation times are sampled uniformly across the demonstration.
> For each view:
> The selected frames are converted to grayscale.
> Each frame is center-cropped and resized to 32 by 32.
> The first sampled frame is treated as the local appearance reference.
> Every frame is replaced by its signed residual relative to that reference.
> Residuals are clipped using limits estimated from training data only.
> The clipped values are quantized to signed 8-bit integers.
> A small target-independent spatial offset, view-specific gain, and low-amplitude residual noise are applied consistently within the episode.
> For time position t, the released value is therefore derived from:
> residual[t] = grayscale_frame[t] - grayscale_frame[0]
> The raw reference frame is not released. This suppresses static object identity, background appearance, sensor texture, and direct frame matching while retaining motion and deformation evidence.
> The two tactile views are randomly swapped for every example. The swap and all residual nuisances are independent of the target and do not change the target program. The wrist view remains in the first view slot.
> Four-Phase Program Construction
> The hidden synchronized trajectory is divided into four equal normalized-duration intervals:
> phase 1: [0.00, 0.25);
> phase 2: [0.25, 0.50);
> phase 3: [0.50, 0.75);
> phase 4: [0.75, 1.00].
> For each phase, seven signed motion quantities are computed between the phase endpoints:
> local translation along X;
> local translation along Y;
> local translation along Z;
> local rotation around X;
> local rotation around Y;
> local rotation around Z;
> change in gripper opening.
> Translations and rotations are expressed relative to the gripper coordinate frame at the beginning of the demonstration. Positive gripper change means opening and negative change means closing.
> Each channel is divided by a robust scale estimated from training trajectories only. The channel with the largest absolute normalized displacement becomes the phase's motion-axis token. A fixed channel order resolves the rare case of an exact numerical tie.
> The selected channel's signed normalized displacement is then converted into one of six ordered intensity levels. Negative and positive events are divided separately into three magnitude tiers using training-only quantiles.
> Every phase is computed exclusively from its corresponding trajectory interval. Later-phase tokens are not generated by looking up earlier-phase tokens. Dependencies between phases arise from real manipulation trajectories rather than a synthetic token grammar.
> Input Arrays
> Each example is a signed integer tensor with shape:
> [3, 24, 32, 32]
> The axes represent:
> view, normalized_time, height, width
> The view order is:
> view 0: wrist-camera residuals;
> view 1: first anonymous tactile stream;
> view 2: second anonymous tactile stream.
> The identities of views 1 and 2 are independently randomized for every example.
> The first temporal slice is zero because it is the residual reference. Values are stored as int8. Models may convert them to float32 during feature extraction or training.
> Target Sequence
> The target contains exactly eight whitespace-separated tokens:
> A1 I1 A2 I2 A3 I3 A4 I4
> For phase k, Ak is the dominant motion axis and Ik is its signed intensity.
> Motion-Axis Tokens
> Each phase position has seven valid axis tokens:
> AkTX - translation along local X;
> AkTY - translation along local Y;
> AkTZ - translation along local Z;
> AkRX - rotation around local X;
> AkRY - rotation around local Y;
> AkRZ - rotation around local Z;
> AkGR - change in gripper opening.
> The phase number is mandatory. For example, A1TZ is valid only in position 1, while A3TZ is valid only in position 5.
> Signed-Intensity Tokens
> Each phase has six ordered intensity tokens:
> IkN3 - large negative impulse;
> IkN2 - medium negative impulse;
> IkN1 - small negative impulse;
> IkP1 - small positive impulse;
> IkP2 - medium positive impulse;
> IkP3 - large positive impulse.
> Their ordinal indices are:
> N3 = 0, N2 = 1, N1 = 2, P1 = 3, P2 = 4, P3 = 5
> The phase prefix is mandatory.
> An example target sequence is:
> A1TZ I1P2 A2GR I2N3 A3RY I3P1 A4TX I4N2
> This describes positive local-Z translation in phase 1, strong gripper closing in phase 2, mild positive local-Y rotation in phase 3, and medium negative local-X translation in phase 4.
> What the Task Requires
> A successful solver must combine:
> Temporal residual analysis to distinguish persistent motion from transient sensor changes.
> Multimodal fusion across the wrist and two tactile streams.
> Camera-relative reasoning about translation, rotation, and gripper motion.
> Phase-specific decoding rather than whole-video task classification.
> Ordered serialization into a valid eight-token program.
> A model that recognizes only the manipulated object, memorizes source task names, predicts one global motion label, or emits the most common sequence cannot solve the benchmark reliably.
> Dataset Files
> The prepared dataset contains:
> train.csv - training identifiers, array indices, and target sequences.
> test.csv - test identifiers and array indices without targets.
> train_residuals.npy - training residual tensors.
> test_residuals.npy - test residual tensors.
> sample_submission.csv - a valid nonconstant submission example.
> The first dimension of each NumPy array indexes examples. A row with array_index equal to 17 uses array row 17.
> CSV Columns
> train.csv contains:
> id - opaque training identifier;
> array_index - row index in train_residuals.npy;
> target_sequence - ordered eight-token target.
> test.csv contains:
> id - opaque test identifier;
> array_index - row index in test_residuals.npy.
> sample_submission.csv contains:
> id - test identifier;
> target_sequence - predicted eight-token motion program.
> Evaluation
> The eight output positions are evaluated separately across the complete test corpus.
> Motion-axis positions use categorical mismatch count. Signed-intensity positions use squared error between ordinal token indices.
> For each position j:
> position_ratio_j = model_error_j / optimal_constant_error_j
> The denominator is computed independently for every position.
> For a motion-axis position, the optimal constant is the most common valid axis token for that position. For an intensity position, it is the valid ordinal token nearest the mean private target index for that position.
> The position weights are:
> phase 1 axis: 5/32;
> phase 1 intensity: 3/32;
> phase 2 axis: 5/32;
> phase 2 intensity: 3/32;
> phase 3 axis: 5/32;
> phase 3 intensity: 3/32;
> phase 4 axis: 5/32;
> phase 4 intensity: 3/32.
> The weights sum to 32/32 = 1.
> The final score is:
> score = 1 - sum_j(position_weight_j * position_ratio_j)
> The score is clipped to [0.001, 1.0]. Higher is better.
> A perfect submission scores 1.0.
> The optimal constant sequence has zero unclipped skill and receives the clipped minimum score of 0.001.
> Axis recovery receives five-eighths of the total metric weight.
> Ordered intensity recovery receives three-eighths of the total metric weight.
> Malformed sequences, invalid prefixes, invalid tokens, missing identifiers, duplicate identifiers, extra identifiers, or an incorrect number of tokens receive the minimum score.
> Submission Format
> Submit a CSV containing exactly two columns:
> id,target_sequence
> Every test identifier must appear exactly once. Each prediction must contain exactly eight space-separated tokens in the documented order.
> Example:
> id,target_sequence
> vtm_0123abcdef456789abcd,"A1TZ I1P2 A2GR I2N3 A3RY I3P1 A4TX I4N2"
> vtm_7654fedcba3210fedcba,"A1GR I1N1 A2TX I2P3 A3RZ I3N2 A4TY I4P1"
> Computational Expectations
> The released inputs are compact int8 tensors designed for CPU-based experimentation. Practical approaches include temporal statistics, image moments, compact optical-flow descriptors, PCA, histogram-based tree models, linear classifiers, and lightweight temporal convolutional networks.
> No GPU is required. The intended solutions operate on low-resolution residual sequences and should fit within a short CPU training budget.
> What Not To Use
> Do not use id, array_index, CSV row order, or file position as predictive features. The identifier is opaque and array_index is only an array lookup key.
> Do not treat the problem as task-name or object classification. The required output describes four phase-local motion components, not the semantic manipulation category.
> Do not use only the first temporal slice. It is the zero residual reference and contains no motion evidence.
> Do not assign a permanent left/right meaning to view 1 or view 2. The two tactile streams are independently swapped for every example.
> Do not emit continuous positions, Euler angles, quaternions, gripper distances, or decimal-valued actions. The required output is the documented eight-token sequence.
> Do not attempt to match released residuals to external videos, filenames, task directories, or public trajectory records. Source identifiers and static reference appearances are intentionally absent.
> Do not fit normalization, clipping, dimensionality-reduction, or vocabulary statistics using test inputs.
> Do not infer answers from sample_submission.csv. It is a varied formatting example rather than a source of privileged predictions.
> Expected Output
> For every test residual tensor, return one valid ordered eight-token motion program:
> A1 I1 A2 I2 A3 I3 A4 I4
> A strong solution should combine the wrist and anonymous tactile streams, preserve the four-phase order, identify each dominant motion axis, and recover the corresponding signed intensity level.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Document Block Reading-Order Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7045mm1g1e8gnm5ra8dg8et18bktcw
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat douglas's score of 66.908!

Full challenge description from page:

> Document Block Reading-Order Reconstruction
> Overview
> Digitization pipelines can recover the words on a damaged page while losing where several regions belonged and what structural roles they served. This challenge presents real OCR-derived archival pages in which four to seven content blocks retain their text, horizontal geometry, and only a coarse vertical zone, but lose their exact vertical coordinates, document roles, and reading-order positions. The remaining blocks keep a quantized layout and their roles. Reinsert every withheld block into the correct gap, recover its role, and return the candidates in their original reading order.
> The hidden structure is the page's two-dimensional document grammar: margins frame the page, headings introduce bodies, fields pair keys with values, lists continue locally, visual regions interrupt text flow, and multi-column regions interact with lexical continuity. Exact names and coordinates are removed or symbolized. Every target is determined by the source annotation; there is no random target corruption, prompt judging, leakage-based cap, or agent-specific behavior. The intended first-order approach is to use coarse geometry and retained role transitions to estimate gaps, infer candidate roles from shape and language, then decode candidates sharing a gap jointly.
> The six role labels, in their published cyclic order, are MARGIN, HEADING, TEXT, LIST, FIELD, and VISUAL.
> Evaluation Metric
> There are
> 𝑁
> =
> 550
> N=550 test pages and
> 𝑀
> =
> 2,656
> M=2,656 withheld blocks. Page
> 𝑖
> i has
> 𝑘
> 𝑖
> k
> i
> ​
> candidates. Candidate
> 𝑗
> j has true gap
> 𝑔
> 𝑖
> 𝑗
> g
> ij
> ​
> , predicted gap
> 𝑔
> ^
> 𝑖
> 𝑗
> g
> ^
> ​
> ij
> ​
> , true role
> 𝑟
> 𝑖
> 𝑗
> r
> ij
> ​
> , and predicted role
> 𝑟
> ^
> 𝑖
> 𝑗
> r
> ^
> ij
> ​
> .
> Gap proximity is
> 𝐻
> 𝑖
> =
> (
> 1
> /
> 𝑘
> 𝑖
> )
> ∑
> 𝑗
> =
> 1
> 𝑘
> 𝑖
> exp
> ⁡
> (
> −
> ∣
> 𝑔
> ^
> 𝑖
> 𝑗
> −
> 𝑔
> 𝑖
> 𝑗
> ∣
> /
> 1.5
> )
> H
> i
> ​
> =(1/k
> i
> ​
> )∑
> j=1
> k
> i
> ​
> ​
> exp(−∣
> g
> ^
> ​
> ij
> ​
> −g
> ij
> ​
> ∣/1.5).
> Exact-gap accuracy is
> 𝐴
> 𝑖
> =
> (
> 1
> /
> 𝑘
> 𝑖
> )
> ∑
> 𝑗
> =
> 1
> 𝑘
> 𝑖
> 1
> [
> 𝑔
> ^
> 𝑖
> 𝑗
> =
> 𝑔
> 𝑖
> 𝑗
> ]
> A
> i
> ​
> =(1/k
> i
> ​
> )∑
> j=1
> k
> i
> ​
> ​
> 1[
> g
> ^
> ​
> ij
> ​
> =g
> ij
> ​
> ].
> For role
> 𝑐
> c,
> 𝑃
> 𝑐
> =
> 𝑇
> 𝑃
> 𝑐
> /
> (
> 𝑇
> 𝑃
> 𝑐
> +
> 𝐹
> 𝑃
> 𝑐
> )
> P
> c
> ​
> =TP
> c
> ​
> /(TP
> c
> ​
> +FP
> c
> ​
> ),
> 𝑅
> 𝑐
> =
> 𝑇
> 𝑃
> 𝑐
> /
> (
> 𝑇
> 𝑃
> 𝑐
> +
> 𝐹
> 𝑁
> 𝑐
> )
> R
> c
> ​
> =TP
> c
> ​
> /(TP
> c
> ​
> +FN
> c
> ​
> ), and
> 𝐹
> 1
> 𝑐
> =
> 2
> 𝑃
> 𝑐
> 𝑅
> 𝑐
> /
> (
> 𝑃
> 𝑐
> +
> 𝑅
> 𝑐
> )
> F1
> c
> ​
> =2P
> c
> ​
> R
> c
> ​
> /(P
> c
> ​
> +R
> c
> ​
> ). A zero denominator contributes zero. Role macro-F1 is
> 𝐹
> =
> (
> 1
> /
> 6
> )
> ∑
> 𝑐
> 𝐹
> 1
> 𝑐
> F=(1/6)∑
> c
> ​
> F1
> c
> ​
> .
> Let
> 𝐸
> (
> 𝑧
> )
> E(z) be the set of directed adjacent candidate-token pairs in sequence
> 𝑧
> z. Because every valid sequence contains the same
> 𝑘
> 𝑖
> k
> i
> ​
> unique candidates, adjacency F1 reduces to
> 𝐷
> 𝑖
> =
> ∣
> 𝐸
> (
> 𝑦
> ^
> 𝑖
> )
> ∩
> 𝐸
> (
> 𝑦
> 𝑖
> )
> ∣
> /
> (
> 𝑘
> 𝑖
> −
> 1
> )
> D
> i
> ​
> =∣E(
> y
> ^
> ​
> i
> ​
> )∩E(y
> i
> ​
> )∣/(k
> i
> ​
> −1).
> Coupled block accuracy is
> 𝐶
> 𝑖
> =
> (
> 1
> /
> 𝑘
> 𝑖
> )
> ∑
> 𝑗
> =
> 1
> 𝑘
> 𝑖
> 1
> [
> 𝑔
> ^
> 𝑖
> 𝑗
> =
> 𝑔
> 𝑖
> 𝑗
> ∧
> 𝑟
> ^
> 𝑖
> 𝑗
> =
> 𝑟
> 𝑖
> 𝑗
> ]
> C
> i
> ​
> =(1/k
> i
> ​
> )∑
> j=1
> k
> i
> ​
> ​
> 1[
> g
> ^
> ​
> ij
> ​
> =g
> ij
> ​
> ∧
> r
> ^
> ij
> ​
> =r
> ij
> ​
> ].
> Whole-page exactness is
> 𝑄
> 𝑖
> =
> 1
> [
> 𝑦
> ^
> 𝑖
> =
> 𝑦
> 𝑖
> ]
> Q
> i
> ​
> =1[
> y
> ^
> ​
> i
> ​
> =y
> i
> ​
> ], including candidate order, every gap, and every role.
> A valid prediction contains every row-specific qNN token exactly once, uses only gaps from g00 through the gap after that row's final retained block, uses one published role per token, and contains no other tokens. For an invalid row,
> 𝐻
> 𝑖
> =
> 𝐴
> 𝑖
> =
> 𝐷
> 𝑖
> =
> 𝐶
> 𝑖
> =
> 𝑄
> 𝑖
> =
> 0
> H
> i
> ​
> =A
> i
> ​
> =D
> i
> ​
> =C
> i
> ​
> =Q
> i
> ​
> =0. For role macro-F1, every invalid candidate is assigned the next role after its true role in the published cyclic order, so invalid output receives a full wrong-label penalty and cannot be a cheaper abstention.
> The final score is
> 𝑆
> =
> 100
> ×
> clip
> ⁡
> (
> 0.25
> 𝐻
> ˉ
> +
> 0.15
> 𝐴
> ˉ
> +
> 0.20
> 𝐹
> +
> 0.20
> 𝐷
> ˉ
> +
> 0.10
> 𝐶
> ˉ
> +
> 0.10
> 𝑄
> ˉ
> ,
> 0
> ,
> 1
> )
> S=100×clip(0.25
> H
> ˉ
> +0.15
> A
> ˉ
> +0.20F+0.20
> D
> ˉ
> +0.10
> C
> ˉ
> +0.10
> Q
> ˉ
> ​
> ,0,1), where bars denote the mean over test pages. Higher is better. The minimum is 0; exact reconstruction of every page is 100.
> Measured on the shipped public files: invalid output 0.00, format-only g00:TEXT placement 11.47, geometry-only placement with a constant role 37.17, trained numeric multitask decoding 52.02, text-plus-geometry joint decoding 53.97, and perfect reconstruction 100.00.
> Dataset
> The public/ directory contains:
> train.csv - 1,088 labeled pages.
> sample_id - string - opaque page identifier with no source, order, role, channel, or target information.
> scan_channel - string - balanced nuisance marker, either c0 or c1; it is not predictive of the target.
> layout_view - string - retained blocks in reading order, separated by || .
> candidate_slate - string - four to seven withheld blocks in independently shuffled token order, separated by || .
> placement_sequence - string - ordered candidate-to-gap-and-role tokens forming the target.
> test.csv - 550 query pages with exactly sample_id, scan_channel, layout_view, and candidate_slate.
> sample_submission.csv - 550 format-valid example rows with the required submission columns.
> A retained block has the form [rNN] xXX yYY wWW hHH ROLE :: text. Horizontal positions range from x00 through x07; vertical positions range from y00 through y15; widths range from w00 through w07; and heights range from h00 through h07. A candidate has the form [qNN] zoneZ xXX wWW hHH :: text, where values from zone0 through zone2 preserve only a coarse vertical zone and the role is withheld. Frequent non-identifying words and function words remain readable; rare content words are deterministically symbolized as vNNNN; numbers and source keys are replaced; and a deterministic fraction of input tokens is shown as <mask>.
> Gap g00 is before r00, g01 is after r00 and before r01, and the final gap is after the last retained block. Multiple candidates may share one gap. Their order in placement_sequence gives their order inside that missing run.
> Submission
> Submit a CSV with a header and exactly 550 data rows. Columns must appear in this exact order:
> sample_id - string - every test identifier exactly once; row order may differ from test.csv.
> placement_sequence - string - every row-specific candidate exactly once as qNN>gNN:ROLE, in reconstructed reading order.
> Missing, duplicated, or unknown identifiers; a wrong row count; duplicate headers; or missing, extra, or reordered columns raise a clear validation error. Invalid prediction strings receive worst-case row credit and a full wrong-role penalty without crashing the grader.
> Examples using real test identifiers and valid row-specific candidate counts:
> sample_id,placement_sequence
> f1d544645e8eed38,q02>g01:HEADING q00>g04:TEXT q03>g04:LIST q01>g06:FIELD
> f03451d43ea8f79b,q04>g02:MARGIN q01>g05:HEADING q05>g05:TEXT q00>g09:LIST q03>g12:FIELD q02>g14:VISUAL
> The examples demonstrate syntax only and are not disclosed answers.
> What Not to Use
> Candidate token order is independently shuffled, so emitting q00 q01 ... with g00:TEXT scores only 11.47.
> A geometry-only solver cannot see candidate roles and scores 37.17 even with constrained gap decoding.
> A constant TEXT role performs poorly under six-class macro-F1, especially on margins, headings, lists, fields, and visual regions.
> Coarse-zone sorting cannot distinguish multiple blocks in one zone or reconstruct a consecutive missing run.
> Independent placement misses the 20% adjacency term and often reverses candidates assigned to the same gap.
> scan_channel is exactly balanced inside every candidate-count group and carries no target information.
> Exact-source lookup is not an intended route: document identifiers, page numbers, exact coordinates, numbers, source keys, and rare lexical identifiers are absent or symbolized.
> Prompt injection and output prose are irrelevant because scoring is deterministic parsing and comparison.
> Expected solutions combine layout-aware gap scoring, role-transition modeling, lexical and shape-based role inference, and constrained sequence decoding.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Ciphered Wordform Analogy Completion

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cj6psvkthn1ny7gbjdq1ey18bjk02
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat mrnguyen's score of 0.529!

Full challenge description from page:

> Ciphered Wordform Analogy Completion
> Overview
> This is a GPU-oriented sequence generation challenge about learning hidden word-building analogies from examples. Each row is a small encrypted mini-language. You see ten examples showing how anonymous input words change under grammatical tags, then you must generate four missing output words for new inputs.
> In plain terms: learn the pattern from the row’s examples and complete the four missing wordforms. The characters are row-local ciphers, so a, b, or r in one row do not have the same meaning in another row. The task rewards models that can infer edits such as suffix changes, prefix additions, stem substitutions, and combined boundary changes from limited context.
> The benchmark is grounded in real multilingual wordform resources, but the solver-facing words are regenerated nonce strings. Source-derived transformations are mapped through row-local ciphers and applied to synthetic stems. This preserves realistic word-change behavior while preventing direct source lookup of hidden answers.
> This is not classification, regression, language identification, or metadata prediction. The prediction is four generated strings for each row.
> Dataset files
> train.csv contains 3,120 rows. Each row has:
> id: string. Unique training row ID.
> language_card: JSON object. Broad source hint and row-local alphabet information.
> support_examples: JSON list. Ten visible input/tag/output examples.
> query_slots: JSON list. Four input/tag slots whose outputs must be generated.
> max_form_length: integer. Maximum allowed generated output length.
> target_forms: JSON object. Training-only answers for the four query slots.
> test.csv contains 1,200 rows. It has the same public columns as train.csv but omits target_forms.
> sample_submission.csv contains every test ID with empty strings for all four query slots. It is structurally valid and scores 0.
> JSON field schemas
> language_card contains:
> language: string. Broad source language code used as a hint.
> lexical_category: string. One of V, N, or ADJ.
> cipher_alphabet: list of strings. Row-local characters that may appear in input and output words.
> Each support_examples item contains:
> lemma: string. Nonce input word in the row-local cipher.
> feature_bundle: string. Semicolon-delimited grammatical tag bundle.
> form: string. Output word for the support input and tag bundle.
> Each query_slots item contains:
> qid: string. One of Q0, Q1, Q2, or Q3.
> lemma: string. Nonce input word to transform.
> feature_bundle: string. Target grammatical tag bundle.
> target_forms, present only in train.csv, is a JSON object with exactly these keys:
> Q0: string. Correct output for query slot Q0.
> Q1: string. Correct output for query slot Q1.
> Q2: string. Correct output for query slot Q2.
> Q3: string. Correct output for query slot Q3.
> Task
> For each test row, submit a JSON object mapping all four query IDs to generated output words.
> Valid prediction example:
> {"Q0":"martev","Q1":"klino","Q2":"safris","Q3":"devra"}
> Rules:
> Include exactly the keys Q0, Q1, Q2, and Q3.
> Each value must be a string.
> Values may not contain whitespace.
> Each generated form must be at most max_form_length characters.
> Do not include extra keys.
> Evaluation
> Structurally invalid submission files are rejected. Examples are missing columns, extra columns, duplicate IDs, unknown IDs, missing rows, or wrong column order.
> Malformed row-level JSON or invalid form strings score 0 for that row. The grader aligns by id, not row order.
> For each query slot:
> ExactForm is 1 if the predicted output exactly equals the hidden target output, else 0.
> CharF1 is character multiset F1 between prediction and target.
> BigramF1 is character-bigram multiset F1 between prediction and target.
> BoundaryScore gives 0.25 credit each for matching the first character, last character, first two characters, and last two characters.
> Partial credit is:
> Partial =
> 0.45 * CharF1^2
> + 0.35 * BigramF1^2
> + 0.20 * BoundaryScore
> The slot score is:
> slot_score =
> 0.72 * ExactForm
> + 0.28 * Partial
> For a row:
> ExactAll = 1 if all four query outputs are exactly correct, else 0
> row_score =
> 0.88 * mean(slot_score over Q0 to Q3)
> + 0.12 * ExactAll
> The 1,200 hidden rows are balanced across six private transformation families, 200 rows per family:
> suffix_dense
> prefix_tail
> midstem_mutation
> circumfix_mix
> sparse_nominal
> adjective_agreement
> The final score is:
> final_score =
> 0.70 * mean(row_score over all rows)
> + 0.12 * worst_family_mean
> + 0.10 * worst_language_mean
> + 0.08 * bottom_20_percent_mean
> Scores are finite and bounded in [0, 1]. The sample submission scores 0. A perfect oracle scores 1.
> Submission format
> Submit a CSV with exactly two columns in this order:
> id: string. Test row ID.
> predicted_forms: string. JSON object mapping Q0 through Q3 to generated forms.
> Example:
> id,predicted_forms
> 0a12bc34de56f789,"{""Q0"":""martev"",""Q1"":""klino"",""Q2"":""safris"",""Q3"":""devra""}"
> Recommended solution approach
> A basic approach can infer simple string edits from support examples. Stronger GPU-based sequence-to-sequence or fine-tuned models should learn how grammatical tags, lexical categories, source hints, row-local ciphers, and sparse examples interact.
> The hard part is not applying one visible edit. Only part of the test behavior repeats an exact support tag. Many rows require transferring a pattern across related tags or combining multiple edit cues.
> What not to use
> Do not use row IDs, row order, or fixed character meanings.
> Do not assume characters have stable identities across rows.
> Do not search for real source words to recover answers. Test inputs and targets are synthetic nonce strings.
> Do not assume every query tag appears among support examples.
> Do not copy the input word unchanged; target outputs are generated from nontrivial source-derived edits.
> Do not submit plain text lists, XML, Python code, or extra JSON keys.
> Benchmark boundary
> Conventional wordform-generation datasets usually ask for one real output word from a real input word and a known tag. This benchmark instead asks for four outputs in a row-local cipher, using only a small in-context analogy set and generated source-derived transformations and is a highly novel task.
> The material task delta is the combination of nonce strings, per-row cipher invariance, multi-slot JSON output, sparse in-context examples, hidden transformation families, and subgroup scoring by both transformation family and source language. It is not a direct public-dataset split, lookup task, fixed-label prediction task, or language-identification benchmark.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Groundline: Polyphonic Voice-Path Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7awrqghsn2nnyn257wwnk6hd8bmchf
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Groundline: Polyphonic Voice-Path Recovery
> Overview
> Each example is a short passage of music represented as an ordered sequence of note symbols rather than an audio recording. Several notes may sound at the same time. The passage is divided into half-beat time steps, and the lowest-sounding note has been removed from every step. Your task is to reconstruct this missing lowest-note line in order: predict which of 12 pitch classes is sounding, whether that note begins or continues, or whether the step is a rest. Submit the complete prediction for one passage as one space-separated token string.
> Recovering a missing lowest-note line is useful when restoring incomplete digital scores, checking damaged symbolic-music exports, or completing an accompaniment from the surviving upper notes. The visible inputs show partially observed note beginnings, sustained upper notes, the ordered outer upper notes, musical meter, and two known lowest-note states on each side of the missing passage. The examples come from real public-domain and CC0 symbolic scores. Titles, composers, filenames, original keys, and source links are removed; entire musical works and exact duplicate fingerprints are kept on only one side of the train/test split. A useful starting approach is to combine the visible upper-note relationships and then decode a consistent sequence between the known left and right boundary states.
> Token Grammar
> Every output token describes one hidden half-beat frame:
> N00 through N11 - a hidden pitch-class state with a real note onset in this frame.
> C00 through C11 - the hidden pitch-class state continues without an onset in this frame.
> R - no hidden ground note sounds in this frame.
> Pitch classes are cyclic symbolic codes. Their names are consistent across every view in a row and within a source work, but they do not expose the original key. A target contains exactly 24, 28, 32, 36, or 40 space-separated tokens. Its length is the number of frame tokens in each public stream.
> Visible stream tokens use these conventions:
> attack_stream - A03.07 lists visible upper pitch classes that begin in a frame; A_ is empty or fully redacted.
> sustain_stream - S03.07.10 lists visible upper pitch classes sounding in a frame; S_ is empty or fully redacted.
> outer_stream - U03K10 gives the lowest and highest visible upper pitch classes in registral order; U_ is unavailable.
> phase_stream - M04P03 means phase 3 in a four-beat meter represented on the half-beat grid.
> boundary_context - L=N01.C01 R=N08.C08 gives two ground states immediately before and two immediately after the hidden passage.
> display_code - D0 or D1 is a deliberately balanced nuisance code. It carries no target information.
> Only observations are removed. Every scored target token is derived deterministically from the unmodified source note events.
> Evaluation Metric
> The Groundline Recovery Score is in the interval from 0 to 100 and is maximized.
> Let p_t and p̂_t be the true and predicted pitch/rest states at frame t, ignoring the N versus C prefix. Across all N_f scored frames,
> P = (1 / N_f) × Σ_t 1[p̂_t = p_t].
> Let y_t = 1 exactly when the true token begins with N, and let ŷ_t be defined the same way for the prediction. Across all frames,
> TPR = Σ_t 1[y_t = 1 and ŷ_t = 1] / Σ_t 1[y_t = 1],
> TNR = Σ_t 1[y_t = 0 and ŷ_t = 0] / Σ_t 1[y_t = 0],
> J = max(0, TPR + TNR − 1).
> J is chance-corrected onset discrimination. Predicting only N or only nonN receives zero on this term.
> Let B contain every adjacent true frame pair whose pitch/rest state changes. For a non-rest pair, define the directed cyclic interval δ_t = (p_t − p_{t−1}) mod 12, and define δ̂_t analogously. Then
> d_t = min(|δ̂_t − δ_t|, 12 − |δ̂_t − δ_t|),
> s_t = exp(−d_t / 0.75).
> For a transition involving R, s_t = 1 only when both predicted endpoint states exactly match the two true endpoint states; otherwise s_t = 0. The transition term is
> T = (1 / |B|) × Σ_{t in B} s_t.
> The final score is
> Score = 100 × clip(0.70 × P + 0.15 × J + 0.15 × T, 0, 1).
> A malformed path, an illegal token, or a path with the wrong number of tokens receives zero pitch matches, zero transition similarity, and worst-case onset predictions for that row. It cannot create an abstention advantage.
> The theoretical minimum is 0. A score of 100 requires an exact valid recovery of every path. Reproduced public-data references on the shipped files are: valid constant 7.183904, local harmony heuristic 22.106116, continuity-aware heuristic 26.360081, contextual gradient-boosted model 37.234474, and multi-view BiGRU 40.833945. These are baselines, not an estimate of the achievable ceiling.
> Dataset
> train.csv
> Contains 10,000 labeled passages.
> id - integer - fresh row identifier from 0 through 9,999.
> attack_stream - string - lossy upper-note attack frames.
> sustain_stream - string - lossy upper-note sustain frames.
> outer_stream - string - ordered outer-upper-voice frames.
> phase_stream - string - meter and half-beat phase frames.
> boundary_context - string - two left and two right ground-state tokens.
> display_code - string - balanced nuisance code D0 or D1.
> ground_path - string - target sequence of 24, 28, 32, 36, or 40 tokens.
> test.csv
> Contains 3,000 query passages with IDs 10,000 through 12,999. Its columns are id, attack_stream, sustain_stream, outer_stream, phase_stream, boundary_context, and display_code. It never contains ground_path.
> sample_submission.csv
> Contains all 3,000 test IDs and a valid constant path of the required length for each row.
> Submission
> Submit a CSV with a header and exactly 3,000 rows. Columns and order must be exactly:
> id - integer - one unique test identifier.
> ground_path - string - exactly 24, 28, 32, 36, or 40 legal tokens, matching that row's public stream length.
> Duplicate, missing, unknown, or extra IDs are rejected. Extra or reordered columns are rejected. Row order is irrelevant.
> Example using real test IDs:
> id,ground_path
> 10000,C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00
> 10001,C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00 C00
> What Not to Use
> TF-IDF and other lexical bag-of-words routes are prohibited and do not represent the symbolic frame structure.
> A single-frame substitution table misses boundary context, registral ordering, and temporal voice leading.
> Predicting N everywhere earns zero chance-corrected onset credit.
> Copying the left boundary state cannot follow real harmonic transitions.
> display_code is balanced by length and split; using it as a target proxy adds no information.
> Source lookup cannot recover answers because titles, composers, URLs, file names, original keys, and original pitch codes are absent.
> Expected approaches model the cyclic pitch relations in all three visible note views and perform contextual sequence decoding.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Anonymous Spectrogram Event Binding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73whsgg3af11jk309fbjh5ms8bjx19
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Anonymous Spectrogram Event Binding
> Overview
> This is an audio reasoning challenge over compact spectrogram evidence. Each row contains a small 48 by 64 spectral image encoded as text. The image was generated from two overlapping streams of short musical-note sounds. Your task is not to describe the whole audio scene. Instead, you must recover only the event sequence belonging to the requested anonymous stream.
> In plain terms: each row is a tiny acoustic puzzle. Several note events are visible in the spectrogram, but only some belong to the target stream. Use the stream’s timbre fingerprint, the row-local pitch cards, and the raster evidence to output the target events as a compact symbolic ledger.
> The source audio comes from commercially redistributable one-shot instrument-note recordings. Public rows are generated spectrogram rasters, not raw source clips. They contain row-local pitch aliases and anonymous timbre fingerprints. Train and test use disjoint source instruments, so source-note lookup, filename matching, and fixed instrument identity are not useful shortcuts.
> This is not instrument classification, genre tagging, speech recognition, source separation, or ordinary full-scene music transcription. The prediction is a constrained evidence-binding output: select the target stream’s events from an overlapping anonymous acoustic scene.
> Dataset files
> train.csv contains:
> id: string. Unique training row ID.
> spectral_raster: string. A 48 by 64 quantized log-spectral raster encoded with 64 printable symbols.
> grid_shape: string. Always 48x64.
> frame_hop_ms: integer. Milliseconds represented by one time frame. Always 25.
> pitch_cards: JSON list. Row-local pitch aliases and their approximate fundamental bins.
> strand_cards: JSON list. Two anonymous acoustic stream cards, S1 and S2.
> focus_strand: string. The stream to recover, S1 or S2.
> max_events: integer. Maximum allowed event tokens. Always 5.
> density_profile: string. Coarse public condition label: standard, dense, or noisy.
> target_event_ledger: string. Training-only answer ledger.
> test.csv has the same public columns but omits target_event_ledger.
> sample_submission.csv contains:
> id: string. Test row ID.
> predicted_event_ledger: string. Empty dummy ledger. The sample scores 0.
> There are 2,100 training rows and 1,200 hidden test rows. Hidden test rows are balanced across five private generation families with 240 rows per family.
> Input field schemas
> spectral_raster:
> Type: string.
> Length: 3,072 characters.
> Decoding: map each character through 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_ to an integer from 0 to 63, then reshape row-major to 48 frequency bins by 64 time frames.
> Meaning: larger values indicate stronger log spectral energy.
> pitch_cards is a JSON list. Each item has:
> pitch: string. Row-local pitch alias such as P03.
> fundamental_bin: integer. Approximate frequency-bin location of that pitch in the raster.
> register: string. low, mid, or high.
> neighbor_span: list of two integers. Inclusive nearby frequency-bin range useful for tolerant local evidence.
> strand_cards is a JSON list with exactly two items. Each item has:
> strand: string. S1 or S2.
> attack_code: string. Coarse attack descriptor, fast or slow.
> brightness_code: string. Coarse timbre descriptor, bright or dark.
> timbre_template: list of eight integers. Quantized low-to-high spectral profile for that anonymous stream.
> Output grammar
> Submit one string per row in predicted_event_ledger.
> A non-empty ledger is a space-separated sequence of event tokens:
> T07:P03:V1 T20:P11:V2 T38:P04:V0
> Token meaning:
> T07: onset frame 7.
> P03: row-local pitch alias from pitch_cards.
> V1: velocity tier. Valid tiers are V0, V1, and V2.
> Rules:
> Onset frames must be T00 through T63.
> Pitch aliases must be P01 through P14.
> Velocity tiers must be V0, V1, or V2.
> Submit at most 5 events.
> Duplicate identical event tokens are invalid.
> An empty string is valid but scores 0 because every hidden target has target-stream events.
> Evaluation
> Structurally invalid submission files are rejected. Structural errors include missing columns, extra columns, duplicate IDs, unknown IDs, missing IDs, wrong row count, or wrong column order.
> Malformed row-level ledgers score 0 for that row instead of crashing the grader. Rows are aligned by id, not row order.
> For each row:
> StrictEventF1 is F1 after one-to-one matching events with exact pitch alias, exact velocity tier, and onset within 1 frame.
> LoosePitchEventF1 is F1 after one-to-one matching events with exact pitch alias and onset within 2 frames, ignoring velocity.
> OnsetF1 is F1 after one-to-one matching events by onset within 1 frame, ignoring pitch and velocity.
> PitchMultisetF1 is F1 over the multiset of predicted pitch aliases.
> CountScore rewards predicting the right number of target-stream events.
> ExactLedger is 1 only when the normalized event sequence exactly matches the hidden ledger.
> CountScore:
> if PredEvents is empty:
> CountScore = 0
> else:
> CountScore = max(0, 1 - abs(|PredEvents| - |TrueEvents|) / max(|TrueEvents|, 3))
> Row score:
> row_score =
> 0.48 * StrictEventF1
> + 0.22 * LoosePitchEventF1
> + 0.10 * OnsetF1
> + 0.08 * PitchMultisetF1
> + 0.05 * CountScore
> + 0.07 * ExactLedger
> The hidden set is balanced across five private families:
> clear_duet
> dense_overlap
> soft_foreground
> low_register
> noisy_echo
> Family labels are not present in solver-facing files. They are used only for robust hidden scoring.
> Final score:
> overall_mean = mean(row_score over all hidden rows)
> worst_family_mean = minimum family mean over the five private families
> bottom_20_mean = mean(row_score over the lowest-scoring 20% of hidden rows)
> final_score =
> 0.72 * overall_mean
> + 0.18 * worst_family_mean
> + 0.10 * bottom_20_mean
> Scores are finite and bounded in [0, 1]. The sample submission scores 0. A perfect oracle scores 1.
> Submission format
> Submit a CSV with exactly two columns in this order:
> id: test row ID.
> predicted_event_ledger: space-separated event ledger.
> Example:
> id,predicted_event_ledger
> 0a12bc34de56f789,T07:P03:V1 T20:P11:V2 T38:P04:V0
> What not to use
> Do not use source note IDs, source file names, source instrument IDs, row order, or fixed pitch-alias meanings. These are absent from public rows or row-local.
> Do not output every visible event. Distractor-stream events are intentionally present and should not be submitted.
> Do not submit JSON, MIDI files, WAV files, natural-language descriptions, comma-separated lists, or extra columns.
> Do not rely only on the largest spectral peaks. Some target-stream events are softer than distractor events.
> Benchmark boundary
> This task is not isolated-note tagging, instrument recognition, source separation, or full-scene note transcription. Those settings usually ask for a global class label, a separated waveform, or every musical event in the scene.
> This benchmark asks for something narrower and more structural: recover a requested anonymous stream’s symbolic event ledger from a tiny encoded spectrogram, using row-local pitch aliases and abstract timbre evidence. The hard part is acoustic evidence binding under aliasing, overlap, soft target events, and source-instrument-disjoint generalization.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Responsive Image Crop Caption Repair Sequencing

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ffxdj2z1qrcqd2m9m3qf1258bmejm
- DOMAIN exactly as displayed: Sequence To Sequence
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
> Responsive publishing systems routinely reuse one photograph at several aspect ratios and zoom levels. A caption that is accurate for the source image may become over-specific, misleading, or unusable after a crop removes its visual evidence. Repairing that caption is not ordinary image classification: the system must compare the source with each derived view, locate the evidence for multiple claims, and decide how every claim should change.
> Each example in this challenge contains one 512 by 512 contact sheet. Its four labeled panels show the source photograph followed by three progressively tighter nested crops: VIEW 1, VIEW 2, and VIEW 3. The example also contains eight independently ordered natural-language claims that are true of the source panel. The task is conditional sequence generation: produce one ordered sentence of exactly 24 position-anchored action tokens describing whether every claim should be kept, qualified, or dropped in every cropped view.
> The benchmark differs from crop-quality scoring, image-difference captioning, and binary entailment. It requires a three-step repair trajectory for eight claims at once, distinguishes weakened evidence from complete disappearance, and rewards both token-level decisions and globally consistent trajectories. The intended use case is automatic maintenance of captions, alt text, and product or editorial image metadata when one source asset is rendered across responsive layouts.
> Source Representation
> The contact sheet is a 2 by 2 grid with fixed panel order:
> SOURCE — the uncropped reference photograph.
> VIEW 1 — the widest derived crop.
> VIEW 2 — a tighter crop fully contained in VIEW 1.
> VIEW 3 — the tightest crop, fully contained in VIEW 2.
> Each panel preserves the photograph's aspect ratio and is letterboxed when necessary. The labels are part of the rendered sheet so a vision model can identify the panels without relying on the CSV row order.
> The eight claims cover complementary forms of visual evidence:
> presence of each of two localized objects;
> dominant visible color of each object;
> horizontal or vertical source-frame region of an object;
> horizontal ordering of the two objects;
> relative apparent size of the two objects.
> Claim order is independently shuffled for every episode. Object roles, wording, crop center, and crop scale are also varied. Therefore claim_1 does not have a permanent semantic type, and a fixed action template cannot recover the target sentence.
> Challenge Construction
> Only source photographs containing at least two distinct, high-confidence localized object regions are eligible. Near-duplicate detections of the same object are suppressed. One source image may produce two or three episodes with different object roles, claim order, and crop paths.
> The source collection provides semantic clusters for visually related photographs. Complete clusters are assigned to only one side of the benchmark before episodes are generated. The prepared release contains 6,000 training episodes from 2,300 source photographs and 1,200 test episodes from 550 different source photographs. No source photograph or source cluster crosses the split.
> For an object region (B) and crop rectangle (C), visible coverage is the intersection area divided by the source object area:
> coverage(B, C) = area(B intersect C) / area(B)
> Actions are constructed as follows:
> A presence claim is KEEP at coverage of at least 0.72, QUALIFY from 0.16 up to 0.72, and DROP below 0.16.
> A color claim requires more evidence: KEEP at coverage of at least 0.86, QUALIFY from 0.28 up to 0.86, and DROP below 0.28.
> A frame-region claim is KEEP when coverage is at least 0.72 and the object's visible center remains in the same left/center/right or upper/middle/lower region. It is QUALIFY when the object remains at least 0.16 visible but the wording is no longer exact, and DROP otherwise.
> A pairwise relation is KEEP when both objects retain at least 0.72 coverage and the relation remains true. It is QUALIFY when the primary object remains at least 0.16 visible but the secondary evidence is partial, absent, or no longer supports the exact relation. It is DROP when the primary object falls below 0.16 coverage.
> Candidate crop paths are chosen to balance the three actions and produce varied claim trajectories. These choices depend on image evidence and deterministic target construction, not on public IDs or row positions.
> Target Language
> The output contains exactly 24 whitespace-separated tokens in view-major, then claim-major order:
> V1Q1_* ... V1Q8_* V2Q1_* ... V2Q8_* V3Q1_* ... V3Q8_*
> Every asterisk must be replaced by exactly one action:
> KEEP — the claim remains fully supported without rewriting.
> QUALIFY — the primary referent remains visible, but the wording must be weakened or contextualized.
> DROP — the claim's primary visual referent is effectively absent and the claim should be removed.
> For example, a syntactically valid sentence begins:
> V1Q1_KEEP V1Q2_QUALIFY ... V3Q8_DROP
> Position prefixes are mandatory. V2Q4_KEEP is valid only at the fourth claim position for VIEW 2; moving the same token elsewhere is an error.
> What The Task Requires
> A competitive solver must jointly perform object grounding, crop-to-source comparison, claim-conditioned evidence measurement, relation verification, and ordered decoding. The source panel is necessary for interpreting source-relative location and size wording, while the three crop panels determine how support changes over time.
> This is designed as a GPU-relevant multimodal sequence task. A practical solution can encode the four panels with a pretrained vision backbone, encode each claim with a text encoder, fuse crop/source and claim representations, then decode the 24 actions with a small Transformer or structured prediction head. The 6,000 training episodes support short fine-tuning runs; a compact pretrained vision-language model can be trained and evaluated in roughly 5–10 minutes on a modern GPU.
> CPU-only metadata, filename, text-frequency, and global image-statistic models are useful sanity baselines but do not observe which claimed object evidence survives each crop. They are expected to remain substantially below a model that learns localized visual-language alignment. Classical models are not prohibited, but a strong nonvisual baseline would indicate a leakage or construction defect rather than the intended solution.
> What Not To Use
> Do not use private test labels, grader feedback, manually hard-coded test sentences, or information obtained from repeated submission probing.
> Do not use id, CSV row order, image filename, filesystem order, encoded file bytes, or compression artifacts as predictive features. IDs and filenames are opaque lookup keys only.
> Do not perform reverse-image search, source-catalog matching, external caption retrieval, or record linkage. The task must be solved from the released contact sheets, claims, and training targets.
> Do not infer actions only from claim position, wording template, crop index, or a closed list of training target sentences. Claim order and construction choices are independently varied, and test source clusters are disjoint.
> Do not fit preprocessing, vocabulary frequencies, or thresholds using hidden answers or test-derived pseudo-labels.
> Do not submit free-form rewritten captions, probabilities, bounding boxes, or one label per episode. The required object is the documented 24-token sequence.
> Dataset Files
> The public release contains:
> train.csv — 6,000 training episodes, input paths, eight claims, and target sequences.
> test.csv — 1,200 test episodes with the same inputs but no target.
> sample_submission.csv — valid submission columns and token syntax.
> images/ — 7,200 WebP contact sheets referenced by the CSV files.
> The grader additionally receives private answers.csv, containing test IDs and hidden target sequences.
> CSV Columns
> train.csv contains:
> id (string) — opaque episode identifier.
> image_path (string) — relative path to the 512 by 512 contact sheet.
> claim_1 through claim_8 (string) — ordered source-image claims.
> target_sequence (string) — 24 ordered action tokens.
> test.csv contains the same columns except target_sequence.
> sample_submission.csv and private answers.csv contain:
> id (string) — test episode identifier.
> target_sequence (string) — one 24-token repair sequence.
> Evaluation
> Let the three action classes be KEEP, QUALIFY, and DROP. After validating each position prefix, the grader computes three corpus-level quantities.
> action_macro_f1 is macro F1 across the three actions over all 24 token positions. Every action class has equal importance regardless of frequency.
> trajectory_accuracy is the fraction of example-claim pairs for which all three ordered view actions are correct. For claim (q), the compared trajectory is (V1Qq, V2Qq, V3Qq).
> exact_episode_rate is the fraction of examples for which all 24 actions are correct.
> These three quantities form the raw composite:
> raw_composite = 0.60 × action_macro_f1 + 0.30 × trajectory_accuracy + 0.10 × exact_episode_rate
> Nested crops have an unavoidable position prior: wide views retain more evidence than tight views. The grader therefore constructs a null sentence by selecting the most frequent hidden action independently at each of the 24 positions and evaluates it with the same raw composite. Let this value be constant_composite. First compute normalized skill over that position-wise majority baseline:
> normalized_skill = clip((raw_composite - constant_composite) / (1 - constant_composite), 0, 1)
> The final reported score is sqrt(normalized_skill). Higher is better. The score lies in [0, 1]. A perfect submission scores 1.0, while the position-wise majority sentence and weaker solutions score 0.0. Baseline removal prevents crop index alone from earning credit. The square root expands the deliberately narrow useful operating range and is strictly monotonic, so it does not change the ranking of submissions with positive skill. An invalid sequence on one otherwise valid test row receives no correct actions, trajectories, or episode credit for that row; other valid rows still count. Missing, duplicate, or unknown test IDs invalidate the submission and receive 0.0.
> Submission Format
> Submit one CSV containing exactly one row per test episode and the two required columns:
> id,target_sequence
> ep_0123456789abcdef0123,"V1Q1_KEEP V1Q2_QUALIFY V1Q3_DROP V1Q4_KEEP V1Q5_KEEP V1Q6_QUALIFY V1Q7_DROP V1Q8_KEEP V2Q1_QUALIFY V2Q2_QUALIFY V2Q3_DROP V2Q4_KEEP V2Q5_QUALIFY V2Q6_DROP V2Q7_DROP V2Q8_KEEP V3Q1_DROP V3Q2_QUALIFY V3Q3_DROP V3Q4_QUALIFY V3Q5_DROP V3Q6_DROP V3Q7_DROP V3Q8_QUALIFY"
> Every test ID must appear exactly once. Each prediction must contain exactly 24 tokens with the required view and claim prefix at every position.
> Expected Output
> The submission must contain 1,200 rows. The grader returns one floating-point score in the inclusive range [0, 1].

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Math Reasoning Bridge Correction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70bw7sa7p5x6b2htcpvehq4n89fyny
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, small-data, feature-engineering, generative
- Best/top context found: Top Score | 0.681 | Created | Jun 27, 2026 | Start New Solution

Full challenge description from page:

> Math Reasoning Bridge Correction
> Overview
> This is a real-data sequence-to-sequence NLP challenge built from human-written grade-school math reasoning problems. Each row contains a reasoning bridge with a deliberate flaw. Your task is to write a short natural-language revision that fixes the bridge and explains the intermediate quantity needed by the later reasoning.
> This is not a formula-completion task. The target is a two-sentence revision that identifies the broken bridge, names the relevant arithmetic relationship, and explains why the corrected intermediate value should be carried forward.
> The public task is transformed from the source data: original source IDs and raw split names are not released, and rows are presented as bridge-revision prompts rather than direct question-answer examples.
> Dataset
> The public dataset contains:
> train.csv: 6,155 labeled bridge-correction rows with revision_text.
> test.csv: 1,445 unlabeled bridge-correction rows without revision_text.
> sample_submission.csv: Example submission with required columns.
> Columns:
> id: string. Opaque bridge identifier.
> bridge_prompt: string. Prompt containing problem context, previous reasoning, a flawed bridge, redacted later reasoning, answer checksum band, and decoy quantities.
> card_count: integer. Always 3.
> difficulty_band: categorical string. Possible values are short, medium, and long.
> bridge_type: categorical string. Coarse bridge family. Possible values are single_op, multi_op, rate_or_percent, unit_conversion, and comparison.
> number_count: integer. Count of numeric quantities in the source problem text.
> checksum_band: categorical string. Coarse final-answer type, such as small_integer, multi_digit, large_integer, or decimal.
> revision_text: string. Target bridge revision. Present only in train.csv.
> Example bridge_prompt:
> Revise one flawed reasoning bridge. Return two concise sentences.
> Problem context: A company is lining a 900-foot path with a fence. Every 6 feet, a fence pole is placed. The entire path is lined with a fence except for a 42-foot bridge.
> Number bank: 900;6;42
> Previous reasoning: There are 900 - 42 = 858 feet of path to line.
> Flawed bridge: 858 * 6 = 141
> Later reasoning with bridge value redacted: The poles have to go on both sides, so there will be [BRIDGE_VALUE] * 2.
> Answer checksum band: multi_digit
> Decoy quantities: 900;42
> An appropriate revision_text would be:
> The broken bridge should be replaced with a short explanation of the single-operation step. It needs to state that 858 / 6 gives 143 before the later reasoning continues.
> Evaluation
> Submissions are evaluated using a bounded custom semantic repair score. Higher is better. The final score is the mean row score across all test rows, clipped to the range from 0 to 1.
> For each row, the prediction is lowercased and whitespace is collapsed. Tokens are lowercase alphanumeric spans or arithmetic operator tokens: +, -, *, /, and =. Repeated tokens count separately. For the token-F1 component only, generic task words are ignored, including words such as bridge, correct, correction, quantity, relevant, revision, revise, short, and common English stopwords. Operator tokens are not ignored, so 858 / 6 = 143 is evaluated differently from 858 * 6 = 143.
> The row score is:
> 0.30 times token F1 plus 0.35 times corrected-result F1 plus 0.20 times flaw correction plus 0.10 times evidence F1 plus 0.05 times concision.
> Token F1:
> True content tokens come from the hidden revision_text after removing the ignored generic words.
> Predicted content tokens come from submitted revision_text after the same filtering.
> Overlap is the repeated-token intersection count.
> Precision is overlap divided by predicted token count.
> Recall is overlap divided by true token count.
> Token F1 is 2 * precision * recall / (precision + recall).
> Corrected-result F1:
> Each hidden row has one corrected bridge result.
> Predicted result values are extracted only from claimed corrected results, such as the right-hand side of a + b = c or numbers following cue words like gives, equals, becomes, supplies, result, or value.
> Loose numbers copied from the prompt do not receive result credit unless the submission claims them as the corrected bridge result.
> Numbers are compared by numeric value, so 143 and 143.0 match.
> Corrected-result F1 is precision/recall F1 between the hidden result and the submitted claimed result values.
> Predictions that claim many different result values receive no corrected-result credit and are capped at a low score.
> Flaw correction:
> Each row has a hidden flaw type such as wrong result, wrong operation, stale carry-forward value, missing premise, percent/rate misuse, or unit mismatch.
> The prediction receives flaw-correction credit only when it names or clearly implies the row's specific flaw family, such as incorrect/wrong/miscalculated, operation/operator/add/subtract/multiply/divide, carry-forward/stale/previous, premise/given/derived, percent/rate/fraction/hundred, or unit/convert/conversion.
> Mentioning words from a different flaw family reduces flaw-correction credit.
> Evidence F1:
> Each row has hidden evidence terms consisting of key numbers and selected problem terms.
> Numeric evidence terms match by numeric value.
> String evidence terms must appear as discrete lowercase words using regex word-boundary matching.
> Evidence F1 is precision/recall F1 over submitted evidence-like terms and hidden evidence terms, so unrelated extra numbers or words can reduce precision.
> Concision:
> A prediction with 12 to 55 tokens receives full concision credit.
> A prediction with 6 to 11 tokens or 56 to 80 tokens receives half credit.
> A prediction with fewer than 6 or more than 80 tokens receives no concision credit.
> Guardrail:
> Predictions that are only numbers, only an equation, or only a tiny formula-like phrase are capped at a low score even if some numbers match. The task requires a natural-language bridge revision.
> Submissions that repeat the same nontrivial revision_text for more than 20 percent of test rows are capped at 0.10 final score.
> Exact match rule:
> If the normalized submitted revision_text exactly matches the hidden normalized revision_text, the row score is 1.0.
> Submission Format
> Submit a CSV file with exactly two columns:
> id,revision_text
> bridge_abc123,The bridge should explain the missing rate step. It needs to state that 60 / 3 gives 20 before the later reasoning continues.
> bridge_def456,Correct the bridge by naming the relevant unit conversion. The intermediate value is 45 * 2 = 90, which is the quantity used next.
> Requirements:
> Include exactly one row for every id in test.csv.
> Do not include extra IDs, missing IDs, duplicate IDs, or extra columns.
> revision_text must be non-empty.
> Return a concise revision, not a full solution to the original problem.
> What Not To Use
> Do not reverse-map prompts to original source rows or external answer keys. Do not use hidden targets, private answers, source IDs, raw split information, or the original GSM8K files. The intended task is bridge revision from the released prompt and coarse metadata.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## MatureMap: Protein Processing Program Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7etz6dpyd6xa2c38m0zxbegn8b429k
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, generative, small-data
- Best/top context found: Top Score | 65.679 | Created | Jul 24, 2026 | Start New Solution

Full challenge description from page:

> MatureMap: Protein Processing Program Recovery
> Overview
> Proteins are synthesized as residue chains, but many become functional only after signal sequences, transit peptides, propeptides, or mature peptides are separated and membrane-spanning regions establish topology. Each row provides a lossy residue-property tape from one manually reviewed protein. Exact amino-acid identities have been replaced by biochemical property symbols, and a deterministic fraction of symbols has been withheld.
> Recover the curated processing and topology program as a variable-length, space-separated string such as SIGNAL@1-24 PROPEPTIDE@25-61 PEPTIDE@62-78. Coordinates are one-indexed and inclusive. Targets are unchanged expert annotations; difficulty comes from information removal, family-held-out evaluation, weak boundary evidence, and global biological consistency—not randomized labels.
> The intended first-order approach is to learn local hydrophobicity, charge, rigidity, terminal-position, and taxonomic cues for segment proposals, then use a sequence model or constrained decoder to make the complete program biologically consistent. assay_lane is a balanced nuisance field with no intended target meaning.
> Evaluation Metric
> Let the processing labels be
> 𝑃
> =
> S
> I
> G
> N
> A
> L
> ,
> T
> R
> A
> N
> S
> I
> T
> ,
> P
> R
> O
> P
> E
> P
> T
> I
> D
> E
> ,
> P
> E
> P
> T
> I
> D
> E
> P=SIGNAL,TRANSIT,PROPEPTIDE,PEPTIDE and the topology labels be
> 𝑇
> =
> T
> M
> ,
> I
> N
> T
> R
> A
> M
> E
> M
> B
> R
> A
> N
> E
> ,
> C
> Y
> T
> O
> P
> L
> A
> S
> M
> I
> C
> ,
> E
> X
> T
> R
> A
> C
> E
> L
> L
> U
> L
> A
> R
> ,
> L
> U
> M
> E
> N
> A
> L
> ,
> P
> E
> R
> I
> P
> L
> A
> S
> M
> I
> C
> T=TM,INTRAMEMBRANE,CYTOPLASMIC,EXTRACELLULAR,LUMENAL,PERIPLASMIC.
> For predicted segment
> 𝑝
> p and true segment
> 𝑡
> t with the same label, let
> 𝑜
> o be their inclusive overlap,
> ℓ
> 𝑝
> ℓ
> p
> ​
> and
> ℓ
> 𝑡
> ℓ
> t
> ​
> their lengths, and
> Δ
> 𝑠
> ,
> Δ
> 𝑒
> Δ
> s
> ​
> ,Δ
> e
> ​
> their absolute start- and end-coordinate errors.
> Their overlap Dice is
> 𝐷
> (
> 𝑝
> ,
> 𝑡
> )
> =
> 2
> 𝑜
> ℓ
> 𝑝
> +
> ℓ
> 𝑡
> D(p,t)=
> ℓ
> p
> ​
> +ℓ
> t
> ​
> 2o
> ​
> .
> Their boundary similarity is
> 𝐵
> (
> 𝑝
> ,
> 𝑡
> )
> =
> exp
> ⁡
> (
> −
> Δ
> 𝑠
> +
> Δ
> 𝑒
> 2
> max
> ⁡
> (
> 4
> ,
> 0.1
> ℓ
> 𝑡
> )
> )
> B(p,t)=exp(−
> 2max(4,0.1ℓ
> t
> ​
> )
> Δ
> s
> ​
> +Δ
> e
> ​
> ​
> ).
> Their soft match is
> 𝑠
> (
> 𝑝
> ,
> 𝑡
> )
> =
> 0.65
> 𝐷
> (
> 𝑝
> ,
> 𝑡
> )
> +
> 0.35
> 𝐵
> (
> 𝑝
> ,
> 𝑡
> )
> s(p,t)=0.65D(p,t)+0.35B(p,t).
> For each label, all candidate predicted/true pairs are sorted by decreasing
> 𝑠
> s and accepted greedily when neither segment has already been paired.
> For axis
> 𝐴
> \inP
> ,
> 𝑇
> A\inP,T, let
> 𝑀
> 𝐴
> M
> A
> ​
> be the sum of accepted soft matches across the test set, and let
> 𝑛
> 𝐴
> 𝑝
> 𝑟
> 𝑒
> 𝑑
> n
> A
> pred
> ​
> and
> 𝑛
> 𝐴
> 𝑡
> 𝑟
> 𝑢
> 𝑒
> n
> A
> true
> ​
> be its predicted and true segment counts. The axis score is
> 𝐹
> 𝐴
> =
> 2
> 𝑀
> 𝐴
> 𝑛
> 𝐴
> 𝑝
> 𝑟
> 𝑒
> 𝑑
> +
> 𝑛
> 𝐴
> 𝑡
> 𝑟
> 𝑢
> 𝑒
> F
> A
> ​
> =
> n
> A
> pred
> ​
> +n
> A
> true
> ​
> 2M
> A
> ​
> ​
> .
> For every allowed label
> 𝑐
> c, let
> 𝑛
> 𝑐
> 𝑝
> 𝑟
> 𝑒
> 𝑑
> n
> c
> pred
> ​
> and
> 𝑛
> 𝑐
> 𝑡
> 𝑟
> 𝑢
> 𝑒
> n
> c
> true
> ​
> be its predicted and true counts across the test set. The program-inventory score is
> 𝑈
> =
> 2
> ∑
> 𝑐
> min
> ⁡
> (
> 𝑛
> 𝑐
> 𝑝
> 𝑟
> 𝑒
> 𝑑
> ,
> 𝑛
> 𝑐
> 𝑡
> 𝑟
> 𝑢
> 𝑒
> )
> ∑
> 𝑐
> 𝑛
> 𝑐
> 𝑝
> 𝑟
> 𝑒
> 𝑑
> +
> ∑
> 𝑐
> 𝑛
> 𝑐
> 𝑡
> 𝑟
> 𝑢
> 𝑒
> U=
> ∑
> c
> ​
> n
> c
> pred
> ​
> +∑
> c
> ​
> n
> c
> true
> ​
> 2∑
> c
> ​
> min(n
> c
> pred
> ​
> ,n
> c
> true
> ​
> )
> ​
> .
> For row
> 𝑖
> i, remove coordinates and retain the ordered label sequences. Let
> 𝑑
> 𝑖
> d
> i
> ​
> be their unit-cost Levenshtein distance and
> 𝑚
> 𝑖
> m
> i
> ​
> the longer sequence length. Transition similarity is
> 𝐸
> 𝑖
> =
> max
> ⁡
> (
> 0
> ,
> 1
> −
> 𝑑
> 𝑖
> /
> 𝑚
> 𝑖
> )
> E
> i
> ​
> =max(0,1−d
> i
> ​
> /m
> i
> ​
> ), with
> 𝐸
> 𝑖
> =
> 1
> E
> i
> ​
> =1 only when both sequences are empty.
> Let
> 𝐸
> =
> 1
> 𝑁
> ∑
> 𝑖
> 𝐸
> 𝑖
> E=
> N
> 1
> ​
> ∑
> i
> ​
> E
> i
> ​
> .
> Final score is
> 100
> ×
> clip
> ⁡
> [
> 0
> ,
> 1
> ]
> (
> 0.30
> 𝐹
> 𝑃
> +
> 0.30
> 𝐹
> 𝑇
> +
> 0.25
> 𝑈
> +
> 0.15
> 𝐸
> )
> 100×clip
> [0,1]
> ​
> (0.30F
> P
> ​
> +0.30F
> T
> ​
> +0.25U+0.15E).
> Malformed predictions receive zero match and transition credit. For counting denominators, each true segment in that row is paired with one unmatched wrong prediction, producing both a false negative and a false positive; malformed output therefore has no abstention advantage.
> The theoretical minimum is 0. The maximum is 100 and requires exact segment labels, coordinates, multiplicities, and order.
> Measured public-data-only references on the shipped family-held-out split are:
> Invalid sample submission: 0.000000.
> Hydrophobic-window heuristic: 13.617702.
> Competent CPU residue-tree model: 48.260716.
> Strong CPU BiGRU sequence model: 50.237964.
> Perfect answers: 100.000000.
> The learned models use only train.csv. Their predictions are scored once against the held-out answers; no source accessions, external protein database, or private features are used.
> Dataset
> train.csv
> Contains 1,637 labeled proteins from 1,151 normalized protein families.
> sample_id - string - Content-free integer identifier assigned after deterministic shuffling.
> sequence_length - integer - Number of residue positions, from 40 through 1,200.
> residue_tape - string - One biochemical property symbol per residue position.
> taxonomy_band - string - Coarse source taxonomy: BACTERIA, ARCHAEA, EUKARYOTA, VIRUS, or OTHER.
> assay_lane - string - Balanced nuisance code L0 or L1; it has no intended target meaning.
> processing_program - string - Complete ordered target program.
> Residue-property encoding
> h - hydrophobic aliphatic residue.
> a - aromatic residue.
> p - polar uncharged residue.
> b - basic or positively charged residue.
> d - acidic or negatively charged residue.
> g - glycine.
> c - cysteine.
> r - proline or conformationally rigid residue.
> x - withheld or uncommon residue.
> The character at string index zero represents biological coordinate 1. The tape always has exactly sequence_length characters. About six percent of source symbols are deterministically withheld as x; positions are preserved.
> Target-program encoding
> Every token has the literal form LABEL@START-END, using one-indexed inclusive coordinates. Tokens must be sorted by start coordinate, then end coordinate, then label. Alternative mature peptides can overlap and therefore multiple same-label segments may share residues.
> SIGNAL - cleavable secretion signal peptide.
> TRANSIT - organelle-targeting transit peptide.
> PROPEPTIDE - precursor segment removed during maturation.
> PEPTIDE - curated mature peptide product.
> TM - transmembrane segment.
> INTRAMEMBRANE - segment embedded within one side of a membrane.
> CYTOPLASMIC - cytoplasmic topological domain.
> EXTRACELLULAR - extracellular topological domain.
> LUMENAL - organelle-lumen topological domain.
> PERIPLASMIC - periplasmic topological domain.
> test.csv
> Contains 512 unlabeled proteins from 424 normalized protein families disjoint from training.
> sample_id - string - Content-free integer identifier.
> sequence_length - integer - Number of residue positions.
> residue_tape - string - Lossy biochemical property tape.
> taxonomy_band - string - Coarse source taxonomy.
> assay_lane - string - Balanced nuisance code L0 or L1.
> It contains no target column, source accession, protein name, exact amino-acid sequence, checksum, annotation comment, or external alignment key.
> vocabulary.csv
> token_kind - string - Either residue or target.
> token - string - Published residue symbol or target label.
> meaning - string - Human-readable token definition.
> sample_submission.csv
> Contains all 512 test identifiers.
> sample_id - string - Every test identifier exactly once.
> processing_program - string - Placeholder INVALID, intentionally scoring zero.
> Submission
> Upload exactly 512 data rows plus a header with exactly these columns in this order:
> sample_id - string - Every test identifier exactly once.
> processing_program - string - One complete space-separated program.
> Extra or reordered columns, duplicate IDs, missing IDs, unknown IDs, and incorrect row counts are rejected cleanly. Row order does not matter. Missing values, non-finite numeric values, unknown labels, invalid coordinates, duplicate tokens, unsorted tokens, and overlong programs receive the published malformed-row treatment without crashing.
> Format-only examples using real test identifiers are:
> sample_id,processing_program
> 0,SIGNAL@1-22
> 2,TRANSIT@1-31 PROPEPTIDE@32-54
> 5,CYTOPLASMIC@1-18 TM@19-40 EXTRACELLULAR@41-692
> These demonstrate syntax only and are not disclosed answers.
> What Not to Use
> A whole-protein classifier cannot emit a variable number of typed segments and coordinates.
> A single hydrophobicity threshold confuses N-terminal signal peptides with membrane helices and misses transit peptides, propeptides, mature peptides, and membrane sidedness.
> Independent residue decisions fragment long domains and ignore alternating membrane topology and processing order.
> Majority-program prediction fails because segment counts, types, coordinates, lengths, and taxonomic contexts vary substantially.
> Exact-source lookup is not an intended route: accessions, names, comments, exact amino-acid identities, checksums, and cross-references are absent.
> assay_lane is balanced within target archetypes and is intentionally non-informative.
> Strong solutions should combine local biochemical windows, terminal position, taxonomy, long-range sequence context, segment-duration constraints, and globally consistent decoding.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Faithful, Style-Controlled News Lead Generation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ec0a9n099w50v8acgzdmpqd8a0z8e
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, generative, small-data, finance
- Best/top context found: Top Score | 0.502 | Created | Jul 7, 2026 | Start New Solution

Full challenge description from page:

> Overview
> Given only a news headline and a requested target_outlet, generate the article's opening lead — the one-to-three-sentence description that would introduce that story — written in the requested outlet's house style. This is the reverse of headline writing: you must expand a short headline into a faithful, outlet-appropriate opening paragraph.
> Your generated lead must (1) read in the requested outlet's lead style, (2) faithfully cover the facts named in the headline (the people, organizations, places, and numbers in the headline should appear in your lead), and (3) be a fluent, non-trivial expansion rather than a restatement of the headline.
> This is a controllable, conditional text-generation (sequence-to-sequence) task. It is not classification, regression, tabular, retrieval, or ranking. For each test row you output exactly one generated lead string. There are no labels, categories, or numeric targets to predict; the requested outlet is an input control, not a prediction target. All text is authentic published news; no synthetic or machine-generated text is included, and none may be added.
> Target Output
> For each row in public/test.csv, produce one value:
> predicted_lead: a single non-empty string — the generated opening lead for that row's headline, in the row's requested target_outlet style.
> Files available at runtime
> When your solution runs, these files already exist in the working directory:
> public/train.csv — labeled training rows. Columns: sample_id, target_outlet, headline, lead, validation_fold. Use target_outlet + headline as input and lead as the target.
> public/test.csv — rows to predict. Columns: sample_id, target_outlet, headline. No lead is given.
> public/sample_submission.csv — a valid, correctly formatted submission you can copy and overwrite. Columns: sample_id, predicted_lead.
> public/prepared_schema.txt — a plain-text description of the columns.
> You must create the directory working/ if it does not exist and write your predictions to ./working/submission.csv.
> Required workflow
> Read public/train.csv and train (or fine-tune) a text-to-text model that maps target_outlet, headline) to a lead in that outlet's style. A common approach is to prepend a style control token (for example the outlet name) to the headline.
> Read public/test.csv.
> For every sample_id, generate one predicted_lead in the row's requested target_outlet style, covering the headline's facts.
> Write a CSV to exactly ./working/submission.csv with the columns sample_id,predicted_lead, one row per test sample_id.
> The number of rows in ./working/submission.csv (excluding the header) must equal the number of rows in public/test.csv, and every sample_id must match.
> Minimal baseline (guaranteed valid submission)
> A trivial baseline that always produces a correctly formatted, scorable submission: read public/test.csv; for every row, use the headline text itself (or the word "news" if empty) as the predicted_lead; then write the columns sample_id,predicted_lead to ./working/submission.csv, one row per test sample_id. Start from this, then replace the lead logic with your trained, style-conditioned model.
> Evaluation
> Submissions are scored with a composite higher-is-better metric. Each predicted_lead is compared to its withheld reference lead. All ROUGE components are F1, computed on word tokens obtained by lowercasing each string and extracting maximal [a-z0-9]+ runs (no stemming). This is exactly what the grader uses.
> FinalScore = 0.55 RougeL + 0.25 FaithfulExpansionSkill + 0.15 StyleSkill + 0.05 DiversitySkill
> The final score is clipped to [0.0, 1.0]. Higher is better.
> RougeL: mean ROUGE-L (F1) between the predicted lead and the reference lead over all test rows (shared content in the correct order).
> FaithfulExpansionSkill: rewards a lead that both grounds in the headline and adds genuine new content. For each row the grader computes two quantities and multiplies them: coverage = the fraction of the headline's claim tokens (word tokens belonging to capitalized words or to words containing a digit) that appear in your predicted lead (1 if the headline has no claim tokens); and expansion = the fraction of your lead's content tokens (word tokens of length 3 or more) that do NOT appear in the headline (0 if the lead has no content tokens). The row score is coverage * expansion, and FaithfulExpansionSkill is the mean over all rows. Because it multiplies the two, simply echoing the headline (no expansion) scores 0, and inventing unrelated text (no coverage) also scores low — you must cover the headline's facts and expand beyond them.
> StyleSkill: measures whether your leads match the requested outlet's lead style. For each outlet, the grader computes a five-number style signature per lead — normalized word count, mean word length, digit-word ratio, capitalized-word ratio, and punctuation amount — averages it over your predictions and over the true references for that outlet, takes the mean absolute difference d, and scores clip(1 - d, 0, 1). StyleSkill is the mean across outlets.
> DiversitySkill: discourages constant submissions. With U = number of distinct predicted leads (compared case-insensitively after trimming whitespace) and N = number of test rows: clip((U / N) / 0.90, 0, 1). Full credit when at least 90% of predictions are distinct.
> The target is the real published lead, not a derived proxy. Because a headline maps to many plausible leads, even the true reference leads do not reach a perfect 1.0; the ceiling reflects that one-to-many nature. Trivial strategies score low — echoing the headline, emitting a constant lead, or outputting an unrelated real lead all fall far below a model that learns to expand each headline into a faithful, fluent, outlet-appropriate lead.
> Dataset
> The prepared challenge dataset contains:
> public/train.csv
> public/test.csv
> public/sample_submission.csv
> public/prepared_schema.txt
> private/answers.csv (used only by the grader; not visible to your solution)
> Training rows come from two outlets, each labeled with its target_outlet, so the model can learn each outlet's lead style. The public test set contains held-out headlines from both outlets, each tagged with the requested target_outlet; the reference leads are withheld in private/answers.csv. Rows with an empty headline or empty lead are dropped during preparation, and test leads do not appear in training.
> Files And Columns
> public/train.csv
> sample_id: anonymized unique id (carries no target or source information).
> target_outlet: outlet whose lead style to write in reuters or cnbc).
> headline: article headline (model input).
> lead: reference opening lead in that outlet's style (training target).
> validation_fold: deterministic integer fold for public validation.
> public/test.csv
> sample_id: anonymized unique test id.
> target_outlet: requested outlet lead style reuters or cnbc).
> headline: article headline (model input).
> public/sample_submission.csv
> sample_id: matching test id.
> predicted_lead: predicted opening lead string.
> private/answers.csv
> sample_id: matching test id.
> target_outlet: requested outlet lead style.
> headline: article headline.
> lead: withheld reference lead.
> Text Properties
> Headlines are short English news headlines (about 60–75 characters, a single clause) covering finance, markets, and business, largely from 2018–2020. Reference leads are short opening paragraphs (about 150–250 characters, one to three sentences) whose length and register vary by outlet. Headlines and leads may contain commas, so any comma inside a field must be handled by standard CSV quoting.
> What Not To Use
> Private labels or answer leakage: Do not access, reconstruct, cache, or hard-code the withheld reference leads in private/answers.csv.
> Filename, id, or row-order rules: Do not use sample_id values, row order, or hidden metadata as a lookup for the target.
> External text retrieval or matching: Do not search the web, news archives, APIs, or any external corpus to find or match the real article lead for a test headline. Test leads must be generated by your model from the provided headline and requested outlet only.
> External or synthetic training pairs: Do not use additional external datasets, and do not synthesize or augment extra headline -> lead pairs. Use only public/train.csv. Publicly pretrained seq2seq models are allowed and encouraged.
> Cross-split contamination: Do not train on any public/test.csv headlines.
> Grader exploits: Do not exploit bugs in parsing, clipping, or scoring.
> Expected approach: fine-tune a pretrained sequence-to-sequence model (for example BART or T5) with an outlet style-control token prepended to the headline, then generate one lead per test row in the requested outlet style.
> Submission Format
> Write your final submission to exactly this path:
> ./working/submission.csv
> It must contain exactly two columns, sample_id and predicted_lead (no other columns). This exact order is recommended:
> sample_id,predicted_lead
> Example rows (leads with commas are quoted, as standard CSV):
> led_0123abcd45ef67890123,Oil prices rose on Monday as investors weighed supply risks.
> led_abcdef0123456789abcd,"Technology shares led a Wall Street rebound, while the dollar slipped."
> Submission Requirements
> The file must exist at ./working/submission.csv and be a readable CSV.
> It must contain exactly the two columns sample_id and predicted_lead and no others.
> It must contain exactly one row per test sample_id; every sample_id in public/test.csv must be present, with no duplicates and no extras.
> Every predicted_lead must be a non-empty string after trimming whitespace.
> If the file is missing, unreadable, has wrong or extra columns, has duplicate/missing/extra sample_ids, or has any empty prediction, the submission scores 0.0.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Sonar Echo Gap Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f9r2vfb3f2xzmg9wshqpsg58bn1dv
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top Score | — | Created | Aug 2, 2026 | Start New Solution

Full challenge description from page:

> Sonar Echo Gap Reconstruction
> Overview
> This is a video sequence-to-sequence reconstruction challenge built from underwater Adaptive Resolution Imaging Sonar footage. Each row contains a short sonar echo strip with a deliberately corrupted middle gap. Your task is to reconstruct the true missing sonar echo frames as a compact quantized raster string.
> In plain terms: you see sonar frames before the gap, a damaged version of the gap, and sonar frames after the gap. You must fill in the missing fish-school echo structure.
> The source videos are ARIS sonar surveys of mullet schools. Sonar frames are not ordinary photographs: fish schools appear as acoustic echo patterns over range and bearing. The challenge generator resizes each source frame to a 16 by 32 echo grid, quantizes intensity to 64 levels, applies deterministic flips/contrast changes/noise, corrupts the middle gap, and hides the original clean gap as the target.
> Train and hidden test examples use disjoint source videos. Solver-facing files do not expose source filenames, recording dates, source frame indices, or source-video IDs.
> This is not object detection, fish counting, segmentation, or behavior classification. The submission is a generated eight-frame sonar echo patch.
> Dataset files
> train.csv contains:
> id: string. Unique training row ID.
> observed_echo_strip: string. A 28 by 16 by 32 quantized sonar strip. Frames 10 through 17 contain the corrupted gap.
> observed_shape: string. Always 28x16x32.
> gap_start_frame: integer. Always 10.
> gap_frames: integer. Always 8.
> grid_shape: string. Always 16x32.
> corruption_profile: string. Public corruption family: clean_gap, range_dropout, bearing_smear, speckle_confuser, or low_echo.
> target_gap_strip: string. Training-only clean gap strip in the required submission format.
> test.csv has the same public columns but omits target_gap_strip.
> sample_submission.csv contains:
> id: string. Test row ID.
> predicted_gap_strip: string. Empty dummy prediction. The sample scores 0.
> There are 2,000 training rows and 1,000 hidden test rows. Hidden test rows are balanced across five corruption families with 200 rows per family.
> Input and output encoding
> All strip strings use this 64-symbol alphabet:
> 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_
> Each character maps to an integer from 0 to 63.
> observed_echo_strip has length 14,336:
> 28 frames * 16 range bins * 32 bearing bins = 14,336
> Decode it row-major as:
> frame, range_bin, bearing_bin
> predicted_gap_strip must have length 4,096:
> 8 gap frames * 16 range bins * 32 bearing bins = 4,096
> It uses the same row-major order and alphabet. Larger values represent stronger sonar echo intensity. The grader rejects wrong submission columns, but malformed row-level strips simply score 0 for that row.
> Evaluation
> Structurally invalid submission files are rejected. Structural errors include missing columns, extra columns, duplicate IDs, unknown IDs, missing IDs, wrong row count, or wrong column order.
> Malformed row-level predictions score 0 for that row instead of crashing the grader.
> For each row, let Pred be the decoded 8 by 16 by 32 predicted strip and True be the hidden strip.
> Foreground pixels are cells with intensity greater than 14.
> ForegroundF1 is F1 over foreground cells:
> Precision = true_positive_foreground_cells / predicted_foreground_cells
> Recall = true_positive_foreground_cells / true_foreground_cells
> ForegroundF1 = 2 * Precision * Recall / (Precision + Recall)
> If the prediction has no foreground cells, the row score is 0.
> IntensityAgreement is foreground-weighted intensity similarity:
> Union = cells where Pred > 14 or True > 14
> MAE = mean absolute intensity error on Union
> IntensityAgreement = ForegroundF1 * max(0, 1 - MAE / 63)
> PeakF1 compares the strongest echo locations. For each gap frame, the grader takes the 16 highest-intensity cells in Pred and True; PeakF1 is the mean overlap fraction across the eight frames.
> PeakF1 = mean(number of shared top-16 cells / 16 over the 8 frames)
> TemporalMass compares total echo energy per frame:
> TemporalMass = max(0, 1 - mean(abs(predicted_frame_mass - true_frame_mass) / max(true_frame_mass, 1)))
> ExactStrip is 1 only when all 4,096 predicted symbols exactly match the hidden strip.
> The row score is:
> row_score =
> 0.40 * ForegroundF1
> + 0.25 * IntensityAgreement
> + 0.20 * PeakF1
> + 0.10 * TemporalMass
> + 0.05 * ExactStrip
> If ExactStrip is 1, row_score is exactly 1.
> The hidden set is balanced across five families:
> clean_gap
> range_dropout
> bearing_smear
> speckle_confuser
> low_echo
> Final score:
> overall_mean = mean(row_score over all hidden rows)
> worst_family_mean = minimum family mean over the five families
> bottom_20_mean = mean(row_score over the lowest-scoring 20% of hidden rows)
> final_score =
> 0.76 * overall_mean
> + 0.14 * worst_family_mean
> + 0.10 * bottom_20_mean
> Scores are finite and bounded in [0, 1]. The sample submission scores 0. A perfect oracle scores 1.
> Submission format
> Submit a CSV with exactly two columns in this order:
> id: test row ID.
> predicted_gap_strip: 4,096-character quantized sonar gap strip.
> Example:
> id,predicted_gap_strip
> 0a12bc34de56f789,0000000000000000000000000000000000000000...
> The example is abbreviated. Real predictions must contain exactly 4,096 valid alphabet characters.
> What not to use
> Do not use source filenames, recording dates, source frame indices, row order, or source-video IDs. These are absent from solver-facing rows.
> Do not submit JSON, bounding boxes, masks in another format, natural-language descriptions, or extra columns.
> Do not optimize only pixel background. Background-only predictions score 0.
> Do not copy the corrupted gap blindly. The middle frames are deliberately degraded with dropout, smearing, speckle, and low-echo transformations.
> Recommended solution approach
> A simple baseline can copy the corrupted gap from frames 10 through 17 of observed_echo_strip. Stronger approaches should train video inpainting or sequence-to-sequence models that use both temporal context and corruption-family information.
> Benchmark boundary
> Nearest prior work includes fish counting, sonar image segmentation, video inpainting, and underwater object detection. This benchmark differs by using source-video-disjoint ARIS sonar clips, a corrupted temporal gap, a fixed 64-symbol echo-strip output language, foreground-only scoring, and robust family/tail aggregation. It is a sonar video gap-reconstruction task, not a fish detector, count regressor, or ordinary segmentation benchmark.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Duration-Constrained Command Program Decoding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78r3ptwhear6er55f0jbymxx8bkgcn
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: feature-engineering, small-data, generative
- Best/top context found: Top Score | 67.287 | Created | Jul 31, 2026 | Start New Solution

Full challenge description from page:

> Duration-Constrained Command Program Decoding
> Overview
> Embedded devices often retain compact response sketches after their detailed control logs are unavailable. In this challenge, every row covers a 64-step interval from one real measurement channel. The simultaneous command indicators active during that interval have been removed. Your task is to decode the complete duration-constrained command program that is consistent with the released response sketch.
> The 64 scalar measurements are pairwise pooled before release: p00 summarizes program steps 0 and 1, p01 summarizes steps 2 and 3, and p07, for example, summarizes steps 14 and 15. Thus, each row has 32 visible observations covering the same 64 steps over which the command program is defined. The pooled response is locally normalized, quantized, and sparsely omitted. The ten opaque command IDs from B00 through B09 are deterministic clusters of real simultaneous command indicators, while each dNN=BKK instruction specifies how long bundle BKK is asserted. The supplied first and last bundles are endpoint constraints, not labels for the interior. A channel identifier exposes channel-specific response behavior. route_flag is an exactly balanced acquisition-route nuisance variable with no stable target relationship.
> This is temporal program decoding under observation aliasing. The hidden object is a command schedule, the evidence is a half-resolution response sketch, and the submitted object is a variable-length instruction program whose dwell times must total 64. The intended first-order approach is to estimate bundle evidence from local response neighborhoods and then decode a globally coherent program using the endpoint constraints and learned transition grammar.
> Evaluation Metric
> Each valid command program expands to 64 command-bundle symbols. For row
> 𝑖
> i, let the true and predicted expanded programs be
> 𝑦
> 𝑖
> y
> i
> ​
> and
> 𝑦
> ^
> 𝑖
> y
> ^
> ​
> i
> ​
> .
> Position accuracy is
> 𝐴
> 𝑖
> =
> 1
> 64
> ∑
> 𝑡
> =
> 0
> 63
> 1
> [
> 𝑦
> 𝑖
> ,
> 𝑡
> =
> 𝑦
> ^
> 𝑖
> ,
> 𝑡
> ]
> A
> i
> ​
> =
> 64
> 1
> ​
> ∑
> t=0
> 63
> ​
> 1[y
> i,t
> ​
> =
> y
> ^
> ​
> i,t
> ​
> ].
> A boundary occurs at position
> 𝑡
> t, for
> 1
> ≤
> 𝑡
> ≤
> 63
> 1≤t≤63, when the command bundle differs from position
> 𝑡
> −
> 1
> t−1. Let
> 𝐵
> 𝑖
> B
> i
> ​
> and
> 𝐵
> ^
> 𝑖
> B
> ^
> i
> ​
> be the true and predicted boundary sets. Match boundaries one-to-one with maximum cardinality subject to
> ∣
> 𝑡
> −
> 𝑡
> ^
> ∣
> ≤
> 2
> ∣t−
> t
> ^
> ∣≤2. If
> 𝑚
> 𝑖
> m
> i
> ​
> boundaries match, boundary F1 is
> 𝐹
> 𝑖
> =
> 2
> 𝑚
> 𝑖
> ∣
> 𝐵
> 𝑖
> ∣
> +
> ∣
> 𝐵
> ^
> 𝑖
> ∣
> F
> i
> ​
> =
> ∣B
> i
> ​
> ∣+∣
> B
> ^
> i
> ​
> ∣
> 2m
> i
> ​
> ​
> . If both sets are empty,
> 𝐹
> 𝑖
> =
> 1
> F
> i
> ​
> =1; if only one is empty,
> 𝐹
> 𝑖
> =
> 0
> F
> i
> ​
> =0.
> Collapse consecutive duplicate bundle IDs to obtain ordered instruction-symbol sequences
> 𝐶
> 𝑖
> C
> i
> ​
> and
> 𝐶
> ^
> 𝑖
> C
> ^
> i
> ​
> . If
> LCS
> ⁡
> LCS is longest-common-subsequence length, order similarity is
> 𝑂
> 𝑖
> =
> 2
> LCS
> ⁡
> (
> 𝐶
> 𝑖
> ,
> 𝐶
> ^
> 𝑖
> )
> ∣
> 𝐶
> 𝑖
> ∣
> +
> ∣
> 𝐶
> ^
> 𝑖
> ∣
> O
> i
> ​
> =
> ∣C
> i
> ​
> ∣+∣
> C
> ^
> i
> ​
> ∣
> 2LCS(C
> i
> ​
> ,
> C
> ^
> i
> ​
> )
> ​
> .
> The row score is
> 𝑠
> 𝑖
> =
> 0.45
> 𝐴
> 𝑖
> +
> 0.35
> 𝐹
> 𝑖
> +
> 0.20
> 𝑂
> 𝑖
> s
> i
> ​
> =0.45A
> i
> ​
> +0.35F
> i
> ​
> +0.20O
> i
> ​
> .
> The final score is
> 100
> ×
> clip
> ⁡
> (
> 1
> 𝑁
> ∑
> 𝑖
> 𝑠
> 𝑖
> ,
> 0
> ,
> 1
> )
> 100×clip(
> N
> 1
> ​
> ∑
> i
> ​
> s
> i
> ​
> ,0,1). Higher is better.
> An invalid row receives
> 𝑠
> 𝑖
> =
> 0
> s
> i
> ​
> =0, exactly the worst possible row score. A score of 0 means no credited reconstruction; 100 means every command bundle, dwell boundary, and program transition is perfect. Measured public-only references on the frozen 650-row test set are: invalid template 0.00, edge persistence 32.53, one-change heuristic 34.78, pointwise gradient boosting 51.50, bidirectional recurrent decoding 56.89, and perfect 100.00.
> Dataset
> The participant files are:
> train.csv - 1,164 labeled response windows.
> test.csv - 650 unlabeled response windows.
> sample_submission.csv - the exact two-column submission schema with deliberately invalid placeholder predictions.
> Columns in train.csv:
> sample_id - string - content-free row identifier.
> channel_code - string - anonymous measurement-channel identifier from s00 through s81.
> route_flag - string - balanced nuisance value, r0 or r1.
> endpoint_bundles - string - known first and last command-bundle IDs separated by |, such as B00|B03.
> response_sketch - string - 32 ordered pooled observations spanning the 64-step window. The integer token index JJ runs from 00 through 31; observation pJJ summarizes command-program steps
> 2
> 𝐽
> 2J and
> 2
> 𝐽
> +
> 1
> 2J+1, where
> 𝐽
> J is the integer value of JJ. A token such as p07:v-02/d+03 gives its quantized level and observed delta, while p07:x marks that pooled observation as omitted.
> command_program - string - target command program. Each instruction has the form dNN=BKK, where NN is dwell duration and BKK is a command-bundle symbol.
> test.csv contains the same query columns and never contains command_program.
> Submission
> Submit exactly 650 data rows plus a header. Columns and order must be exactly:
> sample_id - string - one identifier copied from test.csv.
> command_program - string - a space-separated sequence of dwell-and-bundle instructions.
> Every token must match dNN=BKK, durations must be positive two-digit integers, bundle IDs must range from B00 through B09, and durations must sum to 64. For example, a valid sequence for q200000 is d12=B00 d08=B03 d44=B00. Submission rows may appear in any order as long as every required sample_id appears exactly once. Column order is fixed: the header must be exactly sample_id,command_program. Duplicate, missing, or unknown IDs; extra or reversed columns; and incorrect row counts are rejected. Malformed or missing prediction strings receive zero credit for that row.
> An example of a correctly formatted submission file is:
> sample_id,command_program
> q200000,"d12=B00 d08=B03 d44=B00"
> q200001,"d01=B02 d31=B00 d16=B01 d16=B00"
> The example illustrates formatting only. A complete submission must contain all 650 IDs from test.csv exactly once.
> Task Construction
> Each example supplies observations from the same interval as the hidden program, and the task operates directly on those observations rather than inspecting a supplied predictive model. Solvers decode command-bundle identity and dwell structure from a lossy single-channel response. The half-resolution evidence, endpoint constraints, executable-length grammar, and joint position-boundary-order metric are specific to this task.
> Unlike event-labeling tasks, there are no trajectories or behavior-event labels here. Boundary timing is only one component of reconstruction credit; command identity, dwell length, and program order must also be recovered.
> What Not to Use
> Predicting only the first edge bundle ignores the interior control program and loses all boundary credit.
> A single global boundary cannot model recurring command cycles or delayed responses.
> Thresholding raw levels fails because each channel has a different local response scale.
> Treating the 64 positions independently creates invalid command flicker and weak program order.
> Using route_flag as a shortcut cannot generalize because it is deliberately balanced and non-informative.
> Expected solutions learn channel-aware response evidence and combine it with constrained program decoding, temporal smoothing, or a bidirectional temporal model.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Stroboscopic Gearbox Repair Synthesis

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7d85hxz5p0e333zptwgc4b5h8bgm14
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, multimodal, large-scale
- Best/top context found: Top Score | — | Created | Jul 31, 2026 | Start New Solution

Full challenge description from page:

> Stroboscopic Gearbox Repair Synthesis
> Overview
> Diagnose a faulty mechanical transmission from visual motion and
> counterfactual tests, then generate an executable Repair DSL program.
> Each case is a unique synthetic gearbox-like assembly containing gears, belts,
> clutches, motors, and monitored output shafts. The diagnostic JPEG combines a
> large labeled drawing of the faulty assembly with six stroboscopic frames. The
> CSV row supplies several motor interventions and reports both the intended and
> observed output-speed signatures.
> The target is not a class label or a caption. It is a minimal program that
> changes physical parameters or connectivity so that the repaired assembly
> satisfies held-back interventions in a private exact-rational simulator.
> A successful solution must combine:
> fine-grained visual grounding of gear and edge identifiers;
> tooth-count, belt-crossing, clutch, and connectivity perception;
> temporal reasoning from angular-marker motion;
> counterfactual comparison of expected and observed shaft behavior;
> multi-fault localization;
> constrained sequence generation under the Repair DSL grammar.
> Category and Runtime Rules
> The primary category is Computer Vision. The output is a
> sequence-to-sequence Repair DSL program.
> A genuine learned vision model must perform the core task. A rules-only image parser, hardcoded generator inversion, lookup table, or manually templated solver is not compliant.
> General-purpose pretrained vision backbones are allowed only when permitted by the platform's solver rules. All task-specific training or fine-tuning must occur inside the submitted run.
> External datasets, external mechanical drawings, self-hosted fine-tuned weights, internet retrieval, and test-label reconstruction are prohibited.
> TF-IDF, n-gram retrieval, Markov chains, hardcoded repair templates, and frequency-only substitutes are not valid core solvers.
> Regex may be used only for deterministic parsing, validation, and final DSL cleanup around a trained model.
> Test cases may be processed only as independent inference inputs. Do not pseudo-label, adapt to, calibrate on, cluster, or retrieve across the test set.
> The proposed Diamond runtime is one H100 GPU, 10 CPU cores, and 62 GB RAM. The complete submitted run must finish within 90 minutes.
> The platform invokes python3 solution.py <public_dir> <submission_out>. Read all challenge files from Path(sys.argv[1]) and write the final CSV exactly to Path(sys.argv[2]).
> Objective
> For every example_id in test.csv, generate one repair_program.
> The program is applied to the private faulty assembly. The repaired assembly is
> then simulated on eight held-back motor interventions. Functional improvement
> is measured relative to the same case's no-op behavior, so a mostly working
> faulty device does not give free semantic credit.
> Different executable repairs may receive high functional credit. Reaching the
> top of the leaderboard additionally requires the minimal canonical edits,
> correct arguments, and exact normalized program.
> Mechanical Semantics
> Every active transmission edge connects source gear u to target gear v.
> omega_v = sign(mode) omega_u teeth_u / teeth_v
> Mode signs:
> MESH, BELT_CROSSED, and CLUTCH_REV use sign -1.
> BELT_OPEN and CLUTCH_FWD use sign +1.
> OPEN transmits zero speed.
> All private simulation uses exact rational arithmetic. A source edit must point
> to an earlier gear identifier than the edge's target, preserving the acyclic
> mechanical graph.
> Repair DSL
> A program begins with REPAIR and ends with END. Multiple edits are separated
> by a space, semicolon, and space.
> Allowed operations:
> SET_TEETH gear=Gnn teeth=k
> Set a gear's tooth count.
> Gnn is a visible gear identifier.
> The generator uses tooth counts 12, 16, 20, 24, 28, 32, 36, and 40.
> SET_MODE edge=Enn mode=value
> Set an edge mode.
> Allowed values are MESH, BELT_OPEN, BELT_CROSSED, CLUTCH_FWD, CLUTCH_REV, and OPEN.
> SET_SOURCE edge=Enn source=Gnn
> Change the source gear of an existing edge.
> SET_OUTPUT output=On gear=Gnn
> Attach a monitored output shaft to a gear.
> No-op example:
> REPAIR END
> One-edit example:
> REPAIR SET_TEETH gear=G07 teeth=24 END
> Multi-edit example:
> REPAIR SET_MODE edge=E03 mode=BELT_CROSSED ; SET_OUTPUT output=O1 gear=G14 END
> Canonical edit order is SET_TEETH, SET_MODE, SET_SOURCE, then
> SET_OUTPUT, with targets sorted lexicographically inside each operation.
> Submissions do not need canonical order to execute, but exact-program credit
> uses normalized canonical order.
> Public Dataset
> train.csv
> Contains 4,000 labeled cases.
> example_id - unique GBX- case identifier.
> image_path - relative path below the public directory.
> evidence_text - readable motor interventions with intended and observed output speeds.
> evidence_vector - JSON numeric form of the public intervention evidence.
> difficulty_level - integer from 1 through 4 in training.
> fault_count - number of target edits, from 1 through 3 in training.
> motor_count - number of independently driven root gears.
> gear_count - number of gears visible in the assembly.
> edge_count - number of transmission edges.
> output_count - number of monitored output shafts.
> component_roster - JSON lists of gear, edge, and output identifiers with their large-panel bounding boxes. It contains no tooth count, mode, connectivity, fault flag, or repair target.
> visual_annotations - train-only JSON boxes and observed attributes for gears, edges, and outputs in the large image panel.
> target_patch - canonical target Repair DSL program.
> test.csv
> Contains 1,000 unlabeled cases. It has the shared public columns above, while
> visual_annotations and target_patch are absent. Test cases have difficulty
> levels 4 or 5 and contain three or four faults.
> images/*.jpg
> One 1280 by 960 diagnostic image per train or test case. The left panel is the
> labeled faulty assembly. The six right panels show the same assembly at
> successive times under the first public motor pulse.
> component_catalog.json
> Documents identifiers, edge modes, visual encodings, allowed tooth counts, and
> the mechanical speed law.
> repair_grammar.json
> Machine-readable Repair DSL grammar, operation arguments, limits, modes, and
> examples.
> task_schema.json
> Prepared train, test, private-answer, and submission schemas.
> sample_submission.csv
> Contains every test ID with the valid no-op program REPAIR END.
> Distribution Shift
> The dataset is split by latent construction grammar, not by random rows.
> Training uses topology families F0-F5 and visual domains D0-D4.
> Test uses held-out topology families F6-F7 and visual domains D5-D6.
> Training contains one to three faults.
> Test contains three to four faults.
> Every topology signature is globally unique.
> Exact target duplicates are checked and reported.
> This split prevents a visually similar training assembly from serving as a
> complete repair lookup. Primitive components and DSL operations remain shared,
> so compositional transfer is possible.
> Evaluation
> The metric is counterfactual_repair_gain, maximized from 0 to 1.
> For each case:
> CaseScore = 0.65 RepairGain + 0.20 EditF1 + 0.10 TokenF1 + 0.04 ExactPatch + 0.01 * ExecutableSyntax
> Signal quality
> For predicted speed p and intended speed e:
> If e = 0, quality is exp(-2 * abs(p)).
> If e is nonzero and p is zero or has the wrong sign, quality is 0.
> Otherwise quality is exp(-abs(ln(abs(p / e)))).
> Q(state) is the mean signal quality over every monitored output in every
> private intervention.
> Repair gain
> Let Q_noop be the quality of the original faulty assembly and Q_patch the
> quality after applying the submitted program.
> RepairGain = clip((Q_patch - Q_noop) / (1 - Q_noop), 0, 1)
> If Q_noop is already numerically 1, RepairGain is defined as 0. The generator
> rejects unobservable fault sets, so this is only a defensive rule.
> Edit F1
> Each parsed edit is canonicalized into one complete edit atom. Multiset F1 is
> computed between submitted and target edit atoms. An operation receives edit
> credit only when its target and every argument are correct.
> Token F1
> Multiset token F1 is computed after removing the wrapper tokens REPAIR, END,
> and ;. It gives limited credit to incomplete programs that contain correct
> operations, identifiers, or values.
> Exact patch
> ExactPatch is 1 when the normalized submitted program exactly equals the
> canonical minimal target; otherwise it is 0.
> Invalid programs
> An invalid or non-executable program cannot receive semantic, edit, exact, or
> syntax credit. It may still receive the 0.10 token component so partial
> generation remains measurable.
> Case weights
> Each private case weight is:
> 1 + 0.12 fault_count + 0.04 (difficulty_level - 1) + 0.05 * I(gear_count >= 22)
> The final leaderboard score is the case-weighted mean of CaseScore.
> Submission Format
> Submit a CSV with exactly these columns in this order:
> example_id,repair_program
> Example:
> GBX-0123456789ABCDEF0123,REPAIR SET_MODE edge=E03 mode=MESH END
> Requirements:
> Include every test example_id exactly once.
> Do not include missing, duplicate, or extra IDs.
> Do not add any columns.
> Keep each program in one CSV field; normal CSV quoting handles spaces.
> Write the file exactly to the submission_out path supplied by the platform.
> Difficulty Ladder
> The metric and data expose distinct capability levels:
> format-only or no-op output remains near the floor;
> correct fault vocabulary without component grounding receives limited token credit;
> a model that repairs one of three or four faults enters the intended low-to-mid band;
> multimodal localization and multi-edit generation move into the competent band;
> topology reconstruction plus simulator-guided search unlocks the high band;
> exact minimal multi-fault repair is required for 1.0.
> Promising improvement paths include multi-scale OCR, gear and edge detection,
> temporal marker tracking, scene-graph induction, rational constraint solving,
> learned error localization, constrained decoding, reranking with a locally
> implemented simulator, and ensembles trained entirely inside the submitted run.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Middle Polish Archive Variant Lattice

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75dcdk2g02dg37wgy102g3t18b23hx
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, generative
- Best/top context found: Top Score | — | Created | Jul 23, 2026 | Start New Solution

Full challenge description from page:

> Middle Polish Archive Variant Lattice
> Overview
> Build a system that expands an editor-style historical-Polish search query into the spellings that may appear in a source document.
> For each test row, you receive a short sequence of query tokens written in editorial spelling. Your submission must return an aligned variant lattice: for every query-token position, give one to three possible source spellings and a probability for each one. A variant lattice is simply a token-by-token list of ranked spelling candidates. It is not a translation, summary or unaligned generated sentence.
> In plain terms:
> input:  editorial query tokens + linguistic codes + three examples from the same source profile
> output: source-spelling candidates with probabilities at each token position
> The prepared rows come from human-annotated 17th- and 18th-century Polish source documents in a public digital-humanities corpus. In that corpus, each accepted token is aligned with two spellings:
> an editor-facing transcription, used here as query_tokens;
> a source-preserving spelling, used here as observed_tokens in training and as the hidden target in testing.
> Rows are created by extracting aligned sentence-level token sequences from those annotations. For each source document, the preparation script selects three separate aligned sentences as public calibration examples, then uses other aligned sentences from the same document as prediction rows. Broken XML files, rejected segmentation alternatives, malformed tokens, and invalid alignments are skipped during preparation.
> A profile_id represents one anonymized source document or work. Rows with the same profile come from the same source and therefore tend to share spelling habits, printer conventions, abbreviation behavior, and editorial/transcription patterns. Training and test profiles are disjoint, but every test profile includes three public calibration examples from that profile. The split therefore tests few-shot transfer to a new source profile rather than memorization of a source seen in training.
> A small row-level expansion_budget limits how many extra candidates you may add beyond the mandatory one candidate per token. The model must decide where uncertainty is useful. Spending alternatives on every token is invalid, while predicting only one spelling everywhere may miss important historical variants.
> This models a practical archive-search workflow. Researchers often search with modernized or editorial spelling, while source records may preserve older spelling conventions. A useful expansion system improves recall without flooding the search engine with too many noisy alternatives. Ordinary historical normalization is only a partial building block: this task runs in the reverse direction, adapts to a source profile from examples, and evaluates calibrated aligned candidate sets rather than one deterministic normalized string.
> Your complete solution must run on one NVIDIA A10G GPU with 24 GB of VRAM and finish within 1 hour, including training, validation, inference, and writing the submission.
> Dataset
> dataset/public/
> ├── train.csv
> ├── test.csv
> └── sample_submission.csv
> JSON-valued columns use compact JSON. All token positions are aligned. The validated release contains 3,500 training rows and 900 test rows; the test rows span 200 anonymous profiles.
> train.csv
> case_id,profile_id,query_tokens,analysis_codes,expansion_budget,calibration_examples,observed_tokens
> Columns:
> case_id
> Data type: string
> Opaque row identifier, unique within train.csv.
> profile_id
> Data type: string
> An anonymized source-profile identifier. One profile corresponds to one source document or work, not to a person. Rows with the same value share source-specific spelling behavior and the same three calibration examples.
> query_tokens
> Data type: JSON array of Unicode strings
> Editorially spelled input sequence. These are the spellings a researcher might naturally type into an archive search system.
> analysis_codes
> Data type: JSON array of arrays of strings
> Linguistic feature codes aligned to query_tokens. Each inner array contains one or more categorical codes for the corresponding token.
> The codes are derived from the token's morphosyntactic analysis in the source annotations. They represent broad word-class information and, when available, inflectional features such as case, number, gender, person, tense, mood, degree, or related grammatical categories.
> The exact tag labels are anonymized into stable g_... codes. Identical codes have identical meaning everywhere in the public files, but the code strings have no numeric order or direct human-readable label. Treat them as categorical features.
> expansion_budget
> Data type: integer
> Maximum number of extra candidates allowed across the row, beyond one mandatory candidate at every token position. Values are between 2 and 8 and depend only on public sequence length.
> calibration_examples
> Data type: JSON array of three objects
> Each object has an aligned query_tokens array and observed_tokens array from the same profile_id. Calibration sequences are distinct from the row's requested sequence. They show how this profile tends to spell some editorial tokens in source form.
> observed_tokens
> Data type: JSON array of Unicode strings
> The aligned source-profile spelling sequence to learn for this row.
> For every training row:
> len(query_tokens) == len(analysis_codes) == len(observed_tokens)
> Within every calibration object:
> len(query_tokens) == len(observed_tokens)
> test.csv
> case_id,profile_id,query_tokens,analysis_codes,expansion_budget,calibration_examples
> The columns have the same meanings as in train.csv, but the requested observed sequence is not included. The public expansion_budget is part of the submission contract and does not depend on the hidden spelling sequence. Training and test profile_id sets are disjoint. The calibration examples make each held-out profile locally observable, so the split tests few-shot transfer rather than unsupported convention guessing.
> Every test case_id must appear exactly once in the submission.
> sample_submission.csv
> case_id,variant_lattice
> The sample contains a valid one-candidate lattice filled with a deliberately incorrect placeholder. It demonstrates serialization and scores exactly 0.0.
> Shortened data examples
> The examples below are shortened for readability. Actual public rows are CSV rows, and the JSON fields use the same shapes. Code values shown here are illustrative examples of the public g_... format.
> A training row fragment:
> case_id: avl_1f4d8c2a9306b7e4d512
> profile_id: p_9c083fd44b2a6f071a
> query_tokens: ["który", "jest", "panem", "?"]
> analysis_codes: [
> ["g_8f2b4c91aa", "g_3a16db9240"],
> ["g_17e0d6a531"],
> ["g_4ad19b0c77", "g_a24861fb02"],
> ["g_2ab08ef591"]
> ]
> expansion_budget: 2
> calibration_examples: [
> {"query_tokens": ["który", "był"], "observed_tokens": ["ktory", "był"]},
> {"query_tokens": ["jest", "to"], "observed_tokens": ["iest", "to"]},
> {"query_tokens": ["pan", "mój"], "observed_tokens": ["pan", "moy"]}
> ]
> observed_tokens: ["ktory", "iest", "panem", "?"]
> A matching test row has the same public fields but omits observed_tokens:
> case_id: avl_45bc2e8a0f19d320ab6d
> profile_id: p_3e64a8d0b296c107
> query_tokens: ["który", "jest", "dobry", "."]
> analysis_codes: [
> ["g_8f2b4c91aa", "g_3a16db9240"],
> ["g_17e0d6a531"],
> ["g_91dcef3740"],
> ["g_7f26311db5"]
> ]
> expansion_budget: 2
> calibration_examples: [
> {"query_tokens": ["który", "człowiek"], "observed_tokens": ["ktory", "człowiek"]},
> {"query_tokens": ["jest", "taki"], "observed_tokens": ["iest", "taki"]},
> {"query_tokens": ["mój", "dom"], "observed_tokens": ["moy", "dom"]}
> ]
> For this test row, a valid lattice would contain four position lists, one for each token in query_tokens.
> Submission format
> Write predictions to:
> working/submission.csv
> The CSV must contain exactly these columns in this order:
> case_id,variant_lattice
> variant_lattice is a JSON array with one entry per query_tokens position. Each position is a list of one to three candidate objects:
> [
> [
> {"text": "ktory", "prob": 0.65},
> {"text": "który", "prob": 0.35}
> ],
> [
> {"text": "iest", "prob": 0.70},
> {"text": "jest", "prob": 0.30}
> ],
> [
> {"text": "dobry", "prob": 1.0}
> ],
> [
> {"text": ".", "prob": 1.0}
> ]
> ]
> For every token position:
> the candidate list must contain between 1 and 3 objects;
> every object must contain exactly text and prob;
> text must be a unique, non-empty, trimmed Unicode string of at most 160 characters and must not contain control or surrogate characters;
> prob must be a finite number in [0.01, 1.0];
> probabilities must be in non-increasing order and sum to 1.0 within 1e-6;
> when probabilities tie, list order determines the top-1 candidate.
> Across the row, define:
> extra_candidates = Σ_positions (number_of_candidates_at_position - 1)
> extra_candidates must not exceed that row's public expansion_budget. A one-candidate prediction at every position always uses budget 0. The budget is global: using a second candidate at one position consumes one unit, and using three candidates consumes two units.
> The outer list length must equal the corresponding query_tokens length. Rows may appear in any order. Extra columns, missing rows, duplicate identifiers, malformed JSON, invalid probabilities, or incorrect sequence lengths invalidate the submission.
> CSV example:
> case_id,variant_lattice
> avl_45bc2e8a0f19d320ab6d,"[[{""text"":""ktory"",""prob"":0.65},{""text"":""który"",""prob"":0.35}],[{""text"":""iest"",""prob"":0.70},{""text"":""jest"",""prob"":0.30}],[{""text"":""dobry"",""prob"":1.0}],[{""text"":""."",""prob"":1.0}]]"
> avl_45bc2e8a0f19d320ab12,"[[{""text"":""ktory"",""prob"":0.55},{""text"":""który"",""prob"":0.45}],[{""text"":""iest"",""prob"":0.70},{""text"":""jest"",""prob"":0.30}],[{""text"":""dobry"",""prob"":1.0}],[{""text"":""."",""prob"":1.0}]]"
> Evaluation
> The score rewards accurate spellings, calibrated uncertainty, transfer to unseen query-to-source spelling pairs, complete phrase coverage, and preservation of tokens that should not change. The expansion budget is a hard validity constraint rather than a separately weighted score component, so a solver cannot gain coverage by flooding every position with alternatives.
> Per-position credit
> For one position, let the submitted candidates be (v_j, p_j) and let t be the true observed token. Define:
> p_true = sum of p_j for candidates where v_j == t
> probability_credit = max(0, 2 × p_true - Σ_j p_j²)
> probability_credit is 1 for a probability-1 correct candidate and 0 when the true token is absent. Splitting probability across unnecessary candidates lowers the credit.
> Character similarity is:
> char_similarity(v, t) = max(0, 1 - levenshtein(v, t) / max(len(v), len(t), 1))
> The probability-weighted character score for one position is:
> expected_char = Σ_j p_j × char_similarity(v_j, t)
> Position groups
> For a row:
> changed positions are positions where the public query token differs from the true observed token;
> unchanged positions are positions where they are equal;
> novel-variant positions are changed positions whose exact query_token → observed_token pair is not shown in any public training target or public calibration example.
> Novel-variant positions affect scoring only through the novel_probability and novel_top1 components, which together make up 35% of the row score. They are included to measure whether a model can compose known spelling behavior rather than merely copy a seen token-pair table.
> To keep this learnable, a novel-variant position is eligible only when its character-level edit pattern has support in the public training data. This pattern is called an edit signature. It is computed by case-folding the query token and observed token, aligning their characters, and recording only the non-matching edit operations, such as substitutions, insertions, deletions, or case-only differences. For example, accent loss, ji style substitutions, or a recurring inserted character can form reusable edit patterns. The exact signature is not something you submit; it is only a construction check ensuring that novel positions require transfer from recurring public transformations, not guessing a completely unseen spelling rule.
> The prepared test set contains at least two novel-variant positions per row. These positions use the same character inventory and recurring transformation structure as the public training data.
> Row score
> Define:
> changed_probability = mean probability_credit on changed positions
> changed_top1 = exact top-1 accuracy on changed positions
> changed_char = mean expected_char on changed positions
> novel_probability = mean probability_credit on novel-variant positions
> novel_top1 = exact top-1 accuracy on novel-variant positions
> full_changed_coverage = 1 if every changed target occurs anywhere in its candidate list, else 0
> unchanged_probability = mean probability_credit on unchanged positions
> The row score is:
> 0.20 × changed_probability
> + 0.10 × changed_top1
> + 0.10 × changed_char
> + 0.25 × novel_probability
> + 0.10 × novel_top1
> + 0.15 × full_changed_coverage
> + 0.10 × unchanged_probability
> The component weights are:
> | Component | Weight | What it measures |
> |---|---:|---|
> | changed_probability | 0.20 | Probability assigned to correct changed-token spellings |
> | changed_top1 | 0.10 | Whether the best candidate is exactly correct on changed tokens |
> | changed_char | 0.10 | Character-level closeness on changed tokens |
> | novel_probability | 0.25 | Probability quality on held-out query-to-observed pairs |
> | novel_top1 | 0.10 | Top-1 exact accuracy on held-out query-to-observed pairs |
> | full_changed_coverage | 0.15 | Whether every changed token is covered somewhere in the lattice |
> | unchanged_probability | 0.10 | Preservation of tokens that should stay unchanged |
> Row scores are averaged within each profile_id. The final score is the unweighted mean of those profile scores multiplied by 100. Profile-macro averaging prevents large profiles from dominating evaluation.
> Not allowed
> External APIs.
> External historical spelling pairs, historical corpora, specialist dictionaries, or manually created test transcriptions.
> Searching for or re-identifying public source passages to recover test spellings.
> Hard-coding predictions by case_id, profile_id, row order, or filename.
> Exploiting serialization details, preparation behavior, grader behavior, or identifiers instead of modeling the public text and calibration evidence.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Masked Evidence Pair Relation Prediction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76mdfta4qvjx17cg5qf2nxp189w7c9
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, generative, large-scale
- Best/top context found: Top Score | 0.278 | Created | Jul 4, 2026 | Start New Solution

Full challenge description from page:

> Overview
> Predict a structured comparison JSON for two masked reading-comprehension examples. Each row contains two short evidence snippets from encyclopedic passage-question-answer annotations. In each snippet, the original answer text has been replaced with [ANSWER], and many names and numbers have been replaced with generic placeholders.
> Your task is not to recover the hidden answer text. Instead, compare the two hidden answers and predict how they relate to each other: whether they have the same broad answer type, which one is longer by token bucket, which one is longer by character bucket, how their vowel-count buckets compare, whether their initial and final character classes match, whether their hidden spans contain stopwords in the same way, which one appears earlier in its evidence sentence, whether their text shapes match, and whether their question families match.
> The source records are English Wikipedia passage-question-answer annotations collected for reading-comprehension research. The preparation script transforms those records into a new paired relation task by masking answers, normalizing names and numbers, pairing two masked examples together, and hiding the relation object for test rows.
> This is a structured NLP and fine-tuning challenge. Correct solutions must reason over two masked examples at once and output a valid JSON relation object. A model that only classifies one example at a time will miss the cross-example comparison fields.
> Dataset
> The public data contains 39,820 labeled training rows and 8,741 unlabeled test rows. The preparation pipeline creates paired examples from raw passage-question-answer records, anonymizes row ids, masks answer spans, replaces surface identifiers, shuffles rows, and hides the relation labels for the test split.
> Files:
> train.csv: Labeled paired rows with public text fields and answer_json.
> test.csv: Unlabeled paired rows with the same public text fields, without answer_json.
> sample_submission.csv: Example submission file with the required columns.
> Private file:
> answers.csv: Hidden relation objects used by the grader.
> Columns:
> id (string): Anonymized pair id.
> question_a (string): Normalized question for the first masked example.
> masked_evidence_a (string): Normalized evidence sentence for the first example, containing [ANSWER].
> question_b (string): Normalized question for the second masked example.
> masked_evidence_b (string): Normalized evidence sentence for the second example, containing [ANSWER].
> answer_json (JSON object, train only): Ground-truth relation object for the pair.
> answer_json contains:
> type_relation (string): same if both hidden answers have the same broad answer type, otherwise different. Broad answer types are number, date, proper, and common.
> length_relation (string): a_shorter, same, or a_longer, based on answer token-count buckets. The length buckets are one, two, three, and four_plus.
> char_length_relation (string): a_shorter, same, or a_longer, based on hidden answer character-length buckets. The buckets are short, medium, long, and very_long.
> vowel_count_relation (string): a_fewer, same, or a_more, based on hidden answer vowel-count buckets. The buckets are none, few, some, and many.
> initial_class_relation (string): same if both hidden answers begin with the same character class, otherwise different. Character classes are vowel, consonant, digit, and other.
> final_class_relation (string): same if both hidden answers end with the same character class, otherwise different.
> stopword_relation (string): same if both hidden answers either contain at least one common English stopword or both contain none, otherwise different.
> position_relation (string): a_earlier, same, or a_later, based on whether answer A appears before, in the same coarse region as, or after answer B within its evidence sentence. Sentence regions are early, middle, and late.
> shape_relation (string): same if both hidden answers have the same character-shape category, otherwise different. Shape categories are numeric, title, upper, lower, and mixed.
> family_relation (string): same if both questions have the same question family, otherwise different. Question families are the normalized first question word: what, who, when, where, which, how, or other.
> Submission Format
> Submit a CSV with columns id and answer_json in any order.
> Your submission must contain exactly one row for every id in test.csv. Do not add extra ids, omit ids, or duplicate ids. The grader rejects submissions whose id set does not exactly match the test id set.
> answer_json must be a valid JSON object with exactly these fields:
> type_relation
> length_relation
> char_length_relation
> vowel_count_relation
> initial_class_relation
> final_class_relation
> stopword_relation
> position_relation
> shape_relation
> family_relation
> Example submission CSV:
> id,answer_json
> pair_5af2097cd28e,"{""type_relation"":""same"",""length_relation"":""same"",""char_length_relation"":""a_shorter"",""vowel_count_relation"":""a_fewer"",""initial_class_relation"":""different"",""final_class_relation"":""same"",""stopword_relation"":""different"",""position_relation"":""a_earlier"",""shape_relation"":""different"",""family_relation"":""same""}"
> pair_833e0d01b919,"{""type_relation"":""different"",""length_relation"":""a_longer"",""char_length_relation"":""a_longer"",""vowel_count_relation"":""a_more"",""initial_class_relation"":""same"",""final_class_relation"":""different"",""stopword_relation"":""same"",""position_relation"":""same"",""shape_relation"":""different"",""family_relation"":""different""}"
> Use sample_submission.csv as the safest template: keep all ids exactly as provided and replace only the answer_json values.
> Evaluation
> Submissions are scored from 0 to 1 using a majority-baseline-corrected weighted field accuracy. For each field, raw accuracy is compared against the majority-class accuracy for that field in the hidden answers. A constant majority-class submission receives 0 credit for that field, while perfect accuracy receives 1 credit for that field.
> field_score = max(0, (field_accuracy - field_majority_rate) / (1 - field_majority_rate))
> final_score =
> 0.18 * char_length_relation_score +
> 0.16 * vowel_count_relation_score +
> 0.15 * initial_class_relation_score +
> 0.15 * final_class_relation_score +
> 0.14 * length_relation_score +
> 0.10 * stopword_relation_score +
> 0.07 * shape_relation_score +
> 0.03 * type_relation_score +
> 0.01 * position_relation_score +
> 0.01 * family_relation_score
> Metric definitions:
> field_accuracy: Fraction of test rows where the submitted value exactly matches the true value for a field.
> field_majority_rate: Accuracy obtained by always predicting the most common hidden value for that field.
> field_score: Chance-corrected field score after subtracting the majority-class floor.
> The final score is the weighted sum of the ten corrected field scores. Most weight is assigned to hidden-answer-internal relations, so visible question-family and answer-position shortcuts have little impact.
> What Not To Use
> Hardcoded mappings from row ids to relation objects.
> Manual lookup of ids or masked rows outside the released public data.
> External copies of the original unmasked records with labels.
> Files or answer keys outside the released public data.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## The Logical Jigsaw: Trajectory Reconstruction & Step Generation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78t1wh02s3asvw6mckqrn49s847h3m
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, generative, segmentation
- Best/top context found: Top Score | 0.387 | Created | Apr 4, 2026 | Start New Solution

Full challenge description from page:

> The Logical Jigsaw: Trajectory Reconstruction & Step Generation
> Overview
> Standard language models rely heavily on positional context to predict the next token. But what happens when that positional context is shattered?
> In this challenge, you are provided with mathematical reasoning chains from a high-quality process-supervision dataset. Dataset Context & Scope: The data originates from a large-scale mathematics evaluation project focusing on high-school level competition math (algebra, geometry, combinatorics, number theory). The original raw data was collected by having language models generate step-by-step solutions to complex problems, which human annotators then rigorously evaluated step-by-step for mathematical soundness.
> For this competition, the data has been sabotaged:
> One intermediate reasoning step has been deleted.
> The remaining steps have been completely shuffled.
> Your agent must act as a mathematical dependency parser. It must reconstruct the chronological order of the provided steps AND generate the missing logical bridge required to complete the proof.
> Evaluation
> Submissions are evaluated using an Additive Multi-Metric Score:
> Final Score = (0.5 Sequence Score) + (0.5 Generation Score)
> 1. Sequence Score (LCS Partial Credit): The model's proposed chronological order is compared to the ground truth using a Normalized Longest Common Subsequence (LCS). This ensures models receive partial credit for nearly correct logical chains.
> To maximize this score, the model must output a JSON array where the integers represent the original index of the steps in shuffled_steps, and the string "NEW" represents the chronological placement of the missing step.
> A perfect permutation scores 1.0*. If 8 out of 10 steps are in the correct relative sequential order, it scores 0.8.
> Invalid JSON formats score 0.01*.
> 2. Generation Score (Normalized Token F1): Because string-matching metrics like BLEU fail on mathematical notation, the generated_step is evaluated using a custom, pure-Python Normalized Token F1 score.
> The grading script strips away common English filler words (e.g., "we", "divide", "both", "sides").
> It extracts all mathematical variables, digits, and operators, converting them into an unordered token set.
> It calculates the F1 overlap between the generated tokens and the ground truth tokens.
> This allows models to receive high scores for generating the correct mathematical equations regardless of their surrounding natural language phrasing or spacing.
> Dataset
> The dataset consists of mathematical reasoning chains partitioned into training and testing sets.
> 1. train.csv
> This file contains the training data with the ground truth targets included.
> id (string): Unique cryptographic row identifier.
> problem (string): The full text of the initial math problem.
> ground_truth_answer (string): The final numerical or algebraic answer.
> shuffled_steps (string): A JSON-encoded list of the remaining valid reasoning steps in randomized order.
> target_sequence (string): The target variable. A JSON list showing the correct chronological order, using indices and the string "NEW".
> missing_step (string): The target variable. The text required to fill the "NEW" gap.
> 2. test.csv
> This file contains the evaluation data. The targets are withheld.
> id (string): Unique cryptographic row identifier.
> problem (string): The full text of the initial math problem.
> ** ground_truth_answer (string): The final numerical or algebraic answer. (Note: This is intentionally provided in the test set so the model knows the final mathematical destination it is reconstructing the trajectory toward).*
> shuffled_steps (string): A JSON-encoded list of the remaining valid reasoning steps in randomized order.
> 3. sample_submission.csv
> This file demonstrates the exact formatting required for your submission.
> id (string): Row identifier corresponding to test.csv.
> sequence (string): The predicted JSON list sequence.
> generated_step (string): The text generated to fill the missing gap.
> Submission
> Submit a CSV file with exactly the same number of rows as test.csv.
> Required Columns and Data Types
> id (string): Must exactly match the row identifiers from test.csv.
> sequence (string): A valid JSON list representing the chronological order.
> generated_step (string): The text generated to fill the missing gap.
> Sequence Formatting Constraints
> To receive a sequence score of 1.0, the sequence column MUST adhere to the following strict constraints:
> It must be a valid JSON array.
> The array length must be exactly len(shuffled_steps) + 1.
> It must contain the exact string "NEW" exactly one time (representing the location of your generated_step).
> The remaining elements must be a perfect mathematical permutation of the integers from 0 to len(shuffled_steps) - 1.
> Example submission.csv Format
> id,sequence,generated_step
> 8f4c2b9a1d3e,"[2, 0, ""NEW"", 1]","x = 3"
> a1b2c3d4e5,"[""NEW"", 0, 1]","We divide both sides by 2."

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Chinese Abstract Generation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71ennmg80086g538agfbfkk98bp9qr
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: text, Dataset source is visible after the challenge closes., Leaderboard, (3)
- Best/top context found: Beat laddulal's score of 0.474!

Full challenge description from page:

> Overview: Given a Chinese academic paper's title (potentially truncated), its academic discipline, and a short list of author-assigned keywords, generate the paper's abstract in Chinese. The abstract is a 3-6 sentence summary that conveys the paper's research question, methodology, and findings in the conventions of Chinese academic prose. Training papers provide the full title and up to 5 keywords. Test papers provide only the first 12 characters of the title and 2 keywords, requiring the model to infer the full research context and generate a complete, coherent abstract from limited metadata.
> Evaluation: Metric: character-level F1 (char_F1). The score measures the overlap between predicted and reference abstracts at the individual Chinese character level, computing precision and recall over the character multisets and returning their harmonic mean. Higher is better; perfect match scores 1.0; a submission of entirely wrong characters scores 0.0.
> The metric rewards generating Chinese academic text that shares vocabulary with the reference abstract. A model that generates grammatically correct but topically irrelevant text scores near 0. A model that generates abstract text covering the right subject and methods scores 0.3-0.5. A model that closely captures the research contribution scores 0.6+.
> Dataset: train.csv contains 10,000 papers with full metadata and reference abstracts for supervised training. test.csv contains 2,000 papers with limited metadata; abstracts are hidden and must be predicted. sample_submission.csv shows the correct submission format.
> train.csv columns: paper_id - string - unique paper identifier (e.g. train_00000) title - string - full paper title in Chinese discipline - string - academic sub-discipline in English (e.g. Architecture, Chinese Literature) keywords - string - pipe-separated author keywords in Chinese (e.g. 深度学习|图像分类|卷积神经网络) abstract - string - full reference abstract text in Chinese (used as training target)
> test.csv columns: paper_id - string - unique paper identifier (e.g. test_00000) title - string - first 12 characters of the paper title in Chinese discipline - string - academic sub-discipline in English keywords - string - 2 pipe-separated author keywords in Chinese
> sample_submission.csv columns: paper_id - string - identifier matching test.csv abstract - string - placeholder abstract
> Submission: Submit a CSV file with exactly two columns: paper_id and abstract.
> paper_id - string - must match test.csv exactly (e.g. test_00000) abstract - string - generated Chinese abstract text
> Example (3 rows from a valid submission): paper_id,abstract test_00001,本文提出了一种新的特征提取框架，利用多层次语义表示对输入序列进行编码，实验表明该方法在标准评测基准上显著优于基线模型。 test_00002,本文从理论与实证两个层面对研究对象进行了系统分析，归纳了主要规律，并探讨了其在实践中的应用路径与政策含义。 test_00003,本文通过田间试验考察了不同处理方式对产量和品质的影响，结合统计分析得出了若干具有实践指导意义的结论。
> Requirements: exactly 2000 rows, one per test paper; header row required; paper_id must exactly match test.csv; abstract column must not be empty.
> Rules: The only valid input signal is the provided title, discipline, and keyword metadata in test.csv. The following approaches are not allowed:
> Hardcoding or memorizing specific abstracts for particular paper IDs. Using the paper title or keywords to perform an external literature search and retrieve the actual published abstract from academic databases, journal websites, or preprint servers. The challenge tests abstract generation from structured metadata, not retrieval from external sources. Using the paper_id or row ordering as a prediction signal. Using private, role-gated, or API-key-based models, or calling any external inference API at inference time. Using non-reproducible external weights or artifacts not publicly available.
> The challenge tests a model's ability to generate fluent, topically coherent Chinese academic prose given limited metadata. A model that retrieves published abstracts from external sources bypasses the intended generation task and violates the good-faith constraint.
> Pretrained model policy: Fine-tuning a publicly available Chinese language model (BERT, GPT-2, Qwen, Baichuan, ChatGLM, or similar) on the provided training pairs is allowed and encouraged, provided the fine-tuning genuinely uses train.csv. If a pretrained model generates near-perfect abstracts without any fine-tuning on train.csv (char_F1 greater than 0.85 with no training), train the model from scratch on train.csv instead. The intended learning task is modeling the specific vocabulary, sentence structure, and content conventions present in the provided training abstracts, not retrieving memorized training examples.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Multilingual Document Reading-Order Graph Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx797zjgz5kde6jxyr82pdgb718bj9me
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: image, multimodal, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Beat propane's score of 0.241!

Full challenge description from page:

> Overview
> Document-understanding systems must recover more than individual words. They
> must determine which lines belong to the same paragraph, how lines are ordered
> within each paragraph, and how paragraphs should be traversed across a page.
> This becomes difficult for multi-column pages, side regions, irregular spacing,
> and multilingual scripts. A simple top-to-bottom or left-to-right sort can
> produce a graph that is locally plausible but globally incorrect. Such errors
> propagate into screen readers, document search, information extraction, and
> retrieval-augmented generation systems.
> Every page in this challenge is supplied with an image, OCR line proposals,
> paragraph-region proposals, and an imperfect reading-order graph. Your task is
> to generate a canonical sequence of graph-edit operations that transforms the
> observed graph into the intended document hierarchy and reading order.
> This is a sequence-to-sequence structured-prediction problem. You are not asked
> to transcribe the image or merely decide whether the graph is correct. You must
> identify the incorrect relations and emit the minimal repair sequence.
> Task
> Each page contains two kinds of nodes:
> LINE nodes representing recognized text lines.
> BLOCK nodes representing paragraph or document-region candidates.
> The graph uses three relation types:
> CONTAINS: a block contains a line.
> NEXT_LINE: one line follows another within the same block.
> NEXT_BLOCK: one block follows another in page-level reading order.
> The observed graph is a structurally valid alternative produced from the
> intended graph by one controlled local corruption. The corruption may:
> swap adjacent lines within a paragraph;
> swap adjacent paragraph regions in page order;
> exchange visually close lines between two paragraph regions; or
> combine a cross-region line exchange with a paragraph-order swap.
> All nodes remain available. Only graph edges are changed. For each test page,
> predict the edge deletions and additions required to reconstruct the intended
> graph.
> Data
> The public package contains page images, JSONL case files, CSV indices, and an
> operation catalog. It contains English, Japanese, and Simplified Chinese pages.
> File Structure
> train.csv — training identifiers, case indices, and target repair sequences.
> test.csv — test identifiers and case indices without targets.
> train_cases.jsonl — graph-repair cases for the training split.
> test_cases.jsonl — graph-repair cases for the test split.
> images/ — WebP page images referenced by the case files.
> operation_catalog.json — valid operations, relations, and ordering rules.
> sample_submission.csv — a correctly formatted example submission.
> The case_index column gives the zero-based line number of the corresponding
> object in the relevant JSONL file.
> CSV Columns
> train.csv contains:
> id — opaque identifier for one page.
> case_index — line index in train_cases.jsonl.
> repair_sequence — canonical target graph-edit sequence.
> test.csv contains:
> id — opaque identifier for one page.
> case_index — line index in test_cases.jsonl.
> Case Structure
> Each JSONL case has this structure:
> {
> "image_path": "images/doc_182b74fd891acfe13230.webp",
> "language": "ja",
> "width": 637,
> "height": 900,
> "nodes": [],
> "observed_edges": []
> }
> Nodes
> A line node has this form:
> {
> "node": "L017",
> "kind": "LINE",
> "bbox": [0.078125, 0.171875, 0.453125, 0.203125],
> "angle": 0,
> "text": "recognized line text"
> }
> A block node has this form:
> {
> "node": "P004",
> "kind": "BLOCK",
> "bbox": [0.0625, 0.140625, 0.46875, 0.625],
> "angle": 0
> }
> Bounding boxes use normalized coordinates:
> [x_min, y_min, x_max, y_max]
> Coordinates lie between 0.0 and 1.0. They are deliberately coarse, noisy,
> quantized detector proposals rather than exact rendering boxes. Every proposal
> has positive width and height. OCR text may contain the placeholder character
> □. The page image therefore remains useful evidence.
> Node identifiers are randomly assigned within each page. Their numeric suffixes
> do not encode position, order, paragraph membership, or corruption type.
> Identical node identifiers on different pages do not imply shared meaning.
> Observed Edges
> Each edge is represented as one JSON array:
> ["CONTAINS", "P004", "L017"]
> ["NEXT_LINE", "L017", "L018"]
> ["NEXT_BLOCK", "P004", "P009"]
> A valid final graph satisfies all of these rules:
> Every LINE has exactly one incoming CONTAINS edge.
> Every CONTAINS edge has a BLOCK source and a LINE target.
> Within each block, NEXT_LINE edges form one directed path through all of that block's lines.
> Every NEXT_LINE edge connects lines assigned to the same block.
> NEXT_BLOCK edges form one directed path through all non-empty blocks.
> No relation contains a self-loop.
> The complete graph is acyclic.
> The observed graph already satisfies these structural rules, so validity alone
> does not reveal the answer. Layout, OCR text, language, and image evidence must
> be used to select the intended graph.
> Target
> The target is a non-empty, semicolon-separated sequence of primitive graph
> edits. Every operation uses exactly five pipe-separated fields:
> OPERATION|RELATION|SOURCE|TARGET|END
> The final field is always the literal token END.
> Delete an Edge
> DEL_EDGE|NEXT_LINE|L017|L021|END
> This removes NEXT_LINE(L017, L021). The edge must exist when the operation is
> applied.
> Add an Edge
> ADD_EDGE|NEXT_LINE|L017|L018|END
> This adds NEXT_LINE(L017, L018). The edge must not already exist when the
> operation is applied.
> Supported Relations
> The relation field must be one of CONTAINS, NEXT_LINE, or NEXT_BLOCK.
> Source and target node types must match this table:
> | Relation | Source | Target |
> |---|---|---|
> | CONTAINS | BLOCK | LINE |
> | NEXT_LINE | LINE | LINE |
> | NEXT_BLOCK | BLOCK | BLOCK |
> Canonical Order
> Operations must appear in this order:
> all DEL_EDGE operations;
> all ADD_EDGE operations.
> Within each category, sort lexicographically by
> (relation, source, target). Duplicate operations are not allowed.
> A complete repair sequence can look like this:
> DEL_EDGE|CONTAINS|P003|L011|END;DEL_EDGE|NEXT_LINE|L010|L014|END;ADD_EDGE|CONTAINS|P006|L011|END;ADD_EDGE|NEXT_LINE|L010|L011|END
> Each target is the minimal symmetric-difference repair: every incorrect
> observed edge is deleted once, and every missing intended edge is added once.
> Dataset Construction
> The train/test assignment is grouped by language and coarse layout family.
> Pages in the same layout group cannot cross the split. No group contributes
> more than 15 percent of the test rows. Each held-out page is scored separately,
> and the final score is the mean of those page scores rather than an average over
> layout groups.
> Each source page is transformed deterministically. Line and block identifiers
> are shuffled independently, proposal boxes are quantized and perturbed, OCR
> text receives limited character masking, and a geometrically plausible local
> alternative graph is constructed. File names, row position, identifier suffix,
> operation count, and node numbering do not determine the target.
> What Not to Use
> Solutions must be developed from the files released in the public challenge
> package. To preserve the blind evaluation, do not use:
> private answers, hidden test annotations, or information obtained from the grading environment;
> external copies of the source pages or their original layout annotations;
> reverse-image search, OCR-text lookup, perceptual matching, or record linkage against public document archives to recover a test page's original graph;
> manual annotation of individual test pages or hand-written test-specific repair sequences;
> internet services or external APIs that retrieve page-level answers; or
> assumptions that row order, file names, opaque page identifiers, node-number suffixes, or operation counts encode the target.
> Models, algorithms, and feature engineering trained on the released training
> split are allowed. General-purpose software may be used as long as it does not
> retrieve external page-level labels or matching source records.
> Evaluation
> Submissions are evaluated using three fully specified components.
> Edit-Operation F1
> For each page, every predicted operation is represented by the complete tuple:
> (operation, relation, source, target)
> The tuple is a true positive only when all fields match a required operation
> for that page:
> operation_precision =
> correct predicted operations / predicted operations
> operation_recall =
> correct predicted operations / required operations
> operation_f1 =
> 2 × operation_precision × operation_recall
> / (operation_precision + operation_recall)
> Every test page requires at least one repair.
> Final-Edge F1
> The grader applies submitted operations to each observed graph. Every resulting
> edge is represented by (relation, source, target) and compared with the
> intended final graph for that page:
> edge_precision = correct final edges / predicted final edges
> edge_recall = correct final edges / required final edges
> edge_f1 = 2 × edge_precision × edge_recall
> / (edge_precision + edge_recall)
> Exact Graph Indicator
> A page receives an exact-graph value of 1 only when its reconstructed edge set
> is identical to the intended edge set; otherwise it receives 0:
> exact_graph = 1 if final edges equal intended edges, else 0
> The score for each structurally valid page is:
> page_score =
> 0.73 × page_operation_f1
> + 0.02 × page_edge_f1
> + 0.25 × page_exact_graph
> An inapplicable edit or a resulting graph that violates a structural condition
> gives that page a score of 0.0; it does not discard scores from other pages.
> The final score is the arithmetic mean of all page scores. It ranges from 0.0
> to 1.0, and higher is better. An exact submission scores 1.0.
> The complete submission receives 0.0 if it contains any of the following:
> missing, extra, or duplicate identifiers;
> missing, extra, or reordered columns;
> blank, non-string, non-finite, or otherwise unparsable predictions;
> surrounding whitespace or empty operations;
> unknown operations, relations, or node identifiers;
> incorrect field counts or terminal fields;
> invalid source/target node types;
> duplicate operations; or
> noncanonical operation ordering.
> An edge deletion or addition that is inapplicable when reached, or a resulting
> graph that violates a structural condition, receives 0.0 for that page only.
> Submission
> Submit a CSV containing exactly these columns in this order:
> id,repair_sequence
> Provide exactly one row for every identifier in test.csv. Complete example:
> id,repair_sequence
> doc_0012a4f9,"DEL_EDGE|NEXT_LINE|L003|L009|END;ADD_EDGE|NEXT_LINE|L003|L004|END"
> doc_0078c1e5,"DEL_EDGE|CONTAINS|P002|L014|END;DEL_EDGE|NEXT_BLOCK|P002|P005|END;ADD_EDGE|CONTAINS|P006|L014|END;ADD_EDGE|NEXT_BLOCK|P002|P006|END"
> Column names, operation names, relation names, and node identifiers are
> case-sensitive.
> Expected Output
> For every test page, return the minimal canonical sequence of graph edits that
> reconstructs the intended paragraph hierarchy, within-paragraph line order,
> and page-level block order.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Marginalia: Ordered Citation Path Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7caxp0cng5s5yena7nqfmd1x8bgq09
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: text, generative, feature-engineering, Dataset source is visible after the challenge closes.
- Best/top context found: Beat killerpsycho's score of 40.410!

Full challenge description from page:

> Marginalia: Ordered Citation-Path Recovery
> Overview
> Historical commentary often explains a passage by weaving together several citations. Those citation strings are easy to lose during OCR, redaction, or archival conversion even when the surrounding reasoning survives. In this challenge, each row contains three to seven citation contexts whose explicit references have been replaced, together with nine shuffled candidate passages. Recover which candidate belongs to every context and return the mappings in citation order.
> Every context and candidate comes from real public-domain material. Direct reference strings, source names, authors, books, chapters, and verse identifiers are absent from the public rows. Regular lexical masking removes exact-lookup shortcuts, while nearby passages from the same books and chapters act as hard negatives. The intended first-order approach is to encode each citation context and candidate passage, score all context-candidate pairs, and solve a one-to-one constrained assignment before decoding the ordered mapping string.
> Evaluation Metric
> For row i, the true mapping sequence is y_i and the predicted sequence is ŷ_i. Each token has the form rXX>sYY, where rXX identifies a citation context and sYY identifies one of that row's candidate passages.
> A valid prediction must contain exactly the row's reference_count tokens. It must use each required context handle from r00 through r(k-1) exactly once, use only passage handles s00 through s08, and may not repeat a passage handle. A missing, non-string, empty, overlong, malformed, wrong-length, or structurally invalid prediction receives a row score of zero.
> Let C_i be the multiset overlap between the predicted and true mapping tokens. Mapping F1 is
> M_i = 2 C_i / (|ŷ_i| + |y_i|).
> Let E(z) be the multiset of directed adjacent token pairs in sequence z, and let C_i^E be the multiset overlap between E(ŷ_i) and E(y_i). Transition F1 is
> T_i = 2 C_i^E / (|E(ŷ_i)| + |E(y_i)|).
> A zero denominator contributes zero. Let X_i = 1 when the entire predicted path exactly equals the true path and X_i = 0 otherwise. The row score is
> s_i = 0.60 M_i + 0.20 T_i + 0.20 X_i.
> For each k from three through seven, let I_k be the test rows whose true path contains k mappings. The final score macro-averages the five path-length groups:
> S = 100 × clip((1/5) Σ(k=3..7) ((1/|I_k|) Σ(i∈I_k) s_i), 0, 1).
> Each path length therefore contributes equally even though shorter paths are more common. Higher is better. Zero means no credited mappings, transitions, or complete paths; exact recovery of every citation path is 100. Measured on the shipped files: empty sample submission 0.00, format-only mapping 6.92, lexical-overlap assignment 20.66, hybrid word/character assignment 20.95, a public-only cross-encoder with constrained decoding 28.70, and perfect 100.00.
> Dataset
> The public/ directory contains:
> train.csv — 4,000 labeled rows.
> sample_id — integer — Consecutive public row identifier.
> reference_count — integer — Number of citation contexts and required output mappings, from three through seven.
> citation_contexts — string — Ordered contexts serialized as rXX [text] segments separated by || . <TARGET_REF> marks the citation being recovered, <OTHER_REF> marks another citation inside the same local window, <MASK> marks removed lexical material, and <NUM> marks a removed number.
> candidate_slate — string — Nine shuffled candidate passages serialized as sYY [text] segments separated by || .
> evidence_path — string — Ordered context-to-passage mapping tokens separated by single spaces.
> test.csv — 1,000 query rows containing only sample_id, reference_count, citation_contexts, and candidate_slate.
> sample_submission.csv — 1,000 rows with the required submission columns and blank predictions.
> Anchor chapters are disjoint between train and test. Public identifiers are fresh consecutive integers, candidate slots are assigned independently inside every row, presentation order is shuffled, and no public field exposes source identity or canonical reference coordinates.
> Submission
> Submit a CSV with a header and exactly 1,000 data rows. Columns must appear in this exact order:
> sample_id — integer or equivalent string — Every test identifier exactly once; row order may differ from test.csv.
> evidence_path — string — Exactly one unique rXX>sYY token per citation context, written in ascending context order and separated by spaces.
> Missing, duplicate, or unknown identifiers, the wrong row count, or missing, extra, duplicated, or reordered columns raise a clear validation error. Invalid prediction strings receive zero for their rows and cannot be used as abstentions.
> Example using test identifiers:
> sample_id,evidence_path
> 0,r00>s00 r01>s01 r02>s02
> 1,r00>s00 r01>s01 r02>s02 r03>s03 r04>s04
> The example demonstrates the required syntax only. Predictions must be inferred from the corresponding rows in test.csv.
> What Not to Use
> Candidate presentation order is independently shuffled and has no relationship to citation order.
> Sorting opaque rXX and sYY tokens cannot reveal the mapping because slot assignment is local to each row.
> Candidate-only ranking cannot determine which passage belongs to which context.
> Raw token overlap stalls on quotation masking and same-chapter hard negatives; it scores 20.66.
> Independent top-one retrieval can assign the same candidate repeatedly, producing structurally invalid paths.
> Source lookup is not required, and source identifiers, authors, canonical coordinates, and unredacted citation strings are not available in public rows.
> Expected solutions combine contextual retrieval, pairwise semantic reasoning, one-to-one assignment, and constrained sequence decoding.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Phylogenetic Corridor Assembly from Shuffled Evidence Cards

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76n9c1kwtq8n8z04jxsxj2jd8bm21n
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: clustering, generative, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Beat parthbiyani's score of 72.397!

Full challenge description from page:

> Phylogenetic Corridor Assembly from Shuffled Evidence Cards
> Overview
> Predict the ordered sequence of card-role tokens that forms the true phylogenetic path between two given anchor nodes. For each row, you must identify the cards belonging to that path, place them in order from the first anchor to the second, and label every selected card as occurring before, at, or after the least common ancestor.
> The underlying records are real paths extracted from a frozen biological synthesis of curated phylogenetic trees contributed by published studies. These trees organize sampled taxa through shared ancestral nodes. Each source record is the exact minimal route connecting two terminal taxa through their least common ancestor; the target therefore represents a genuine relationship in the synthesized hierarchy rather than an invented or randomized sequence.
> The participant-facing representation hides the scientific names and source identifiers. The two endpoint cards remain identified, while the intervening path cards are shuffled together with five cards taken from another coherent biological branch. The output is one variable-length token string per row. Solving a row requires three coupled decisions: exclude the intruder cards, assemble compatible neighboring ports, and locate the single ancestral turn.
> Every row uses one of ten stable anonymous rulebook_code mappings. Rulebooks replace structural categories with tokens such as b3, h1, and s2; their meanings can be learned from train.csv. Card fields are deterministically omitted with ?, but targets are never altered. Port marks are deliberately collision-prone, port order is arbitrary, and the five intruder cards form a locally coherent fragment. No single field determines the answer.
> collection_lane is an exactly balanced nuisance value, t0 or t1, with no stable relationship to card selection, ordering, or turn location. It is included to test shortcut resistance and should not be used as a predictive signal.
> The intended first-order approach is to learn rulebook-specific node and port compatibility from labeled rows, then decode a fixed-length path between the released anchors while jointly rejecting the intruder fragment.
> Evaluation Metric
> For row
> 𝑖
> i, let the true sequence contain
> 𝐾
> 𝑖
> K
> i
> ​
> card-role tokens and let the submitted sequence contain exactly
> 𝐾
> 𝑖
> K
> i
> ​
> distinct cards. The available slate contains
> 𝐾
> 𝑖
> +
> 5
> K
> i
> ​
> +5 cards:
> 𝐾
> 𝑖
> K
> i
> ​
> true cards and five intruders. Therefore, token count alone does not make card selection correct; a structurally valid submission may include intruders while omitting the same number of true cards. Write the true card order as
> 𝑦
> 1
> ,
> …
> ,
> 𝑦
> 𝐾
> 𝑖
> y
> 1
> ​
> ,…,y
> K
> i
> ​
> ​
> and the predicted order as
> 𝑦
> ^
> 1
> ,
> …
> ,
> 𝑦
> ^
> 𝐾
> 𝑖
> y
> ^
> ​
> 1
> ​
> ,…,
> y
> ^
> ​
> K
> i
> ​
> ​
> .
> Card selection is
> 𝐶
> 𝑖
> =
> ∣
> {
> 𝑦
> ^
> 1
> ,
> …
> ,
> 𝑦
> ^
> 𝐾
> 𝑖
> }
> ∩
> {
> 𝑦
> 1
> ,
> …
> ,
> 𝑦
> 𝐾
> 𝑖
> }
> ∣
> 𝐾
> 𝑖
> .
> C
> i
> ​
> =
> K
> i
> ​
> ∣{
> y
> ^
> ​
> 1
> ​
> ,…,
> y
> ^
> ​
> K
> i
> ​
> ​
> }∩{y
> 1
> ​
> ,…,y
> K
> i
> ​
> ​
> }∣
> ​
> .
> Coverage-normalized order agreement is
> 𝑂
> 𝑖
> =
> 1
> (
> 𝐾
> 𝑖
> 2
> )
> ∑
> 𝑎
> <
> 𝑏
> 1
> [
> 𝑦
> 𝑎
> and
> 𝑦
> 𝑏
> are selected and
> 𝑦
> 𝑎
> precedes
> 𝑦
> 𝑏
> in the prediction
> ]
> .
> O
> i
> ​
> =
> (
> 2
> K
> i
> ​
> ​
> )
> 1
> ​
> ∑
> a<b
> ​
> 1[y
> a
> ​
> and y
> b
> ​
> are selected and y
> a
> ​
> precedes y
> b
> ​
> in the prediction].
> Missing true cards receive no pairwise credit.
> Directed adjacency recall is
> 𝐴
> 𝑖
> =
> ∣
> {
> (
> 𝑦
> ^
> 𝑗
> ,
> 𝑦
> ^
> 𝑗
> +
> 1
> )
> }
> 𝑗
> =
> 1
> 𝐾
> 𝑖
> −
> 1
> ∩
> {
> (
> 𝑦
> 𝑗
> ,
> 𝑦
> 𝑗
> +
> 1
> )
> }
> 𝑗
> =
> 1
> 𝐾
> 𝑖
> −
> 1
> ∣
> 𝐾
> 𝑖
> −
> 1
> .
> A
> i
> ​
> =
> K
> i
> ​
> −1
> ∣{(
> y
> ^
> ​
> j
> ​
> ,
> y
> ^
> ​
> j+1
> ​
> )}
> j=1
> K
> i
> ​
> −1
> ​
> ∩{(y
> j
> ​
> ,y
> j+1
> ​
> )}
> j=1
> K
> i
> ​
> −1
> ​
> ∣
> ​
> .
> Role accuracy is
> 𝑅
> 𝑖
> =
> 1
> 𝐾
> 𝑖
> ∑
> 𝑐
> ∈
> {
> 𝑦
> 1
> ,
> …
> ,
> 𝑦
> 𝐾
> 𝑖
> }
> 1
> [
> 𝑐
> is selected with its correct role
> ]
> .
> R
> i
> ​
> =
> K
> i
> ​
> 1
> ​
> ∑
> c∈{y
> 1
> ​
> ,…,y
> K
> i
> ​
> ​
> }
> ​
> 1[c is selected with its correct role].
> Exact token-position accuracy is
> 𝑃
> 𝑖
> =
> 1
> 𝐾
> 𝑖
> ∑
> 𝑗
> =
> 1
> 𝐾
> 𝑖
> 1
> [
> 𝑡
> ^
> 𝑗
> =
> 𝑡
> 𝑗
> ]
> ,
> P
> i
> ​
> =
> K
> i
> ​
> 1
> ​
> ∑
> j=1
> K
> i
> ​
> ​
> 1[
> t
> ^
> j
> ​
> =t
> j
> ​
> ],
> where a token includes both its card ID and role.
> The row score is
> 𝑠
> 𝑖
> =
> 0.10
> 𝐶
> 𝑖
> +
> 0.20
> 𝑂
> 𝑖
> +
> 0.30
> 𝐴
> 𝑖
> +
> 0.15
> 𝑅
> 𝑖
> +
> 0.25
> 𝑃
> 𝑖
> .
> s
> i
> ​
> =0.10C
> i
> ​
> +0.20O
> i
> ​
> +0.30A
> i
> ​
> +0.15R
> i
> ​
> +0.25P
> i
> ​
> .
> The final score is
> 100
> ×
> clip
> ⁡
> (
> 1
> 𝑁
> ∑
> 𝑖
> =
> 1
> 𝑁
> 𝑠
> 𝑖
> ,
> 0
> ,
> 1
> )
> .
> 100×clip(
> N
> 1
> ​
> ∑
> i=1
> N
> ​
> s
> i
> ​
> ,0,1).
> Higher is better. A score of 0 means no credited selection, ordered pair, adjacency, role, or position. A score of 100 means every card, role, and position is exact.
> Measured public-only references on the frozen 650-row test set are: format-only card order 18.344636, trained card selection without structural assembly 29.224776, learned greedy assembly 39.768576, learned width-64 assembly 45.088704, and port-aware width-256 assembly 54.103989.
> Dataset
> The participant files are:
> train.csv — 750 labeled packets containing 8,497 true path nodes.
> test.csv — 650 unlabeled packets containing 7,511 true path nodes.
> sample_submission.csv — the exact submission schema with structurally valid format-only sequences.
> Columns in train.csv:
> sample_id — string — content-free identifier.
> rulebook_code — string — anonymous encoding system from r00 through r09.
> collection_lane — string — balanced nuisance value t0 or t1.
> path_length — integer — number of true path cards and required output tokens, from 8 through 20.
> anchor_pair — string — oriented endpoint card IDs in the form vNN>vNN.
> node_cards — JSON string — shuffled array containing path_length + 5 node-card objects.
> path_sequence — string — ordered target sequence with role labels.
> test.csv contains the same six query columns and never contains path_sequence.
> Each object in node_cards contains:
> id — row-local card ID from v00 through v24.
> mass — anonymous descendant-mass band.
> branch — anonymous immediate-child-count band.
> offshoot — anonymous number of child branches outside the corridor.
> support — anonymous source-support-count band.
> conflict — anonymous absence-or-presence conflict code.
> named — anonymous named-or-unnamed node code.
> ports — array containing one or two unordered port objects.
> Each port object contains:
> mark — coarse collision-prone edge signature.
> slope — anonymous direction of neighbor mass relative to the current node.
> span — anonymous magnitude band for the mass change.
> echo — anonymous combined evidence-and-branching sketch.
> Any card or port field except id, ports, and mark may be ?. A shared visible value is weak evidence, not proof of adjacency, because categories collide across unrelated edges.
> Card IDs are scoped only to the current row's node_cards array. For example, v03 in one row has no identity, biological relationship, or correspondence with v03 in any other row. IDs are independently reassigned after each row's cards are shuffled.
> Target tokens have the form vNN:U, vNN:T, or vNN:D:
> U — the card occurs before the least common ancestor while moving upward from the first anchor.
> T — the single least common ancestor where the path turns.
> D — the card occurs after the turn while moving downward to the second anchor.
> Submission
> Submit exactly 650 data rows plus a header. Columns must be exactly:
> sample_id — string — one identifier copied from test.csv.
> path_sequence — string — a space-separated sequence of card-role tokens.
> A submitted row must contain exactly path_length distinct card IDs selected from that row's path_length + 5 available node_cards. Exactly five available cards are intruders. Selecting an intruder is a validly formatted but incorrect prediction: it receives no card-selection credit and necessarily displaces a true card. Every token must match vNN:ROLE, where ROLE is U, T, or D. The role pattern must contain one or more U tokens, exactly one T, and one or more D tokens, in that order. Tokens must use exactly one ASCII space as the separator, without leading or trailing whitespace.
> The first and last cards should match the oriented IDs in anchor_pair to earn credit, but an incorrect endpoint choice is treated as a prediction error rather than a formatting error. Submission rows may appear in any order, while the two columns must remain in the stated order.
> An example of a correctly formatted submission file is:
> sample_id,path_sequence
> q200000,"v00:U v01:U v02:U v03:U v04:U v05:U v06:T v07:D v08:D v09:D v10:D v11:D"
> q200001,"v00:U v01:U v02:U v03:U v04:T v05:D v06:D v07:D"
> The example illustrates formatting only. A complete submission must contain every test ID exactly once. Incorrect row counts; duplicate, missing, or unknown IDs; extra or reordered columns; non-string predictions; invalid roles; repeated or unknown cards; incorrect token counts; malformed separators; and invalid role patterns are rejected before scoring.
> What Not to Use
> Card-ID order is an independent shuffle and provides only format-level performance.
> collection_lane is balanced and non-informative by construction.
> Selecting cards from node fields alone cannot distinguish the coherent intruder fragment reliably.
> Treating equal port marks as exact links fails because marks are intentionally collision-prone.
> Sorting only by mass cannot determine which side of the turning ancestor a card belongs to.
> Source lookup is not a viable strategy because public rows contain no taxon names, source node IDs, release identifiers, or stable record keys.
> Expected solutions combine learned node selection, rulebook decoding, port-pair compatibility, constrained path search, and turn-role prediction.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Tactile Surface Route Decoding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73c2m8ty3k51x0pth0ejvq9d8bnpjk
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat rekht's score of 0.926!

Full challenge description from page:

> Tactile Surface Route Decoding
> Overview
> This is a multimodal sequence-decoding challenge about touch. Each row contains a compressed trace from a soft tactile sensor as it scans several unknown surfaces in sequence. Your task is to output the ordered route of contacts: which row-local surface was touched, and the force tier of that contact.
> In plain terms: read the vibration, resistance, motion, and pressure patterns, compare them with the row-local surface cards, and write the sequence of touched surface aliases plus force tiers, such as:
> S03:F1 S01:F2 S05:F0 S02:F1
> The source data comes from real laboratory tactile-sensor recordings. The challenge rows are generated as new composite routes: a row combines transformed contact segments from source trials, removes texture names, and assigns fresh row-local aliases. Train and hidden test rows use disjoint source trial groups, so memorizing a source filename or public row ID cannot reveal the hidden route.
> This is not texture classification. A prediction is a variable-length sequence over row-local contact tokens, and the same physical texture can have a different alias in every row.
> Dataset files
> train.csv contains:
> id: string. Unique training row ID.
> touch_raster: string. A compressed 15 by 96 multimodal tactile raster encoded with 64 printable symbols.
> raster_shape: string. Always 15x96.
> frame_unit: string. Always normalized_touch_time.
> surface_cards: JSON list. Five row-local surface cards, one for each candidate surface alias.
> route_length_hint: string. Always 4_or_5; the true route has four or five contacts.
> max_segments: integer. Maximum number of route tokens allowed. Always 5.
> target_surface_route: string. Training-only contact route ledger.
> test.csv has the same public columns but omits target_surface_route.
> sample_submission.csv contains:
> id: string. Test row ID.
> predicted_surface_route: string. Empty dummy route. The sample scores 0.
> There are 3,600 training rows and 1,500 hidden test rows. Hidden test rows are balanced across five private generation families with 300 rows per family.
> Input field schemas
> touch_raster:
> Type: string.
> Length: 1,440 characters.
> Decoding alphabet: 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_.
> Decoding method: map each character to an integer from 0 to 63 and reshape row-major to 15 sensor channels by 96 time frames.
> Meaning: larger values indicate stronger quantized sensor response after deterministic source-wide clipping and resampling.
> The 15 channels are ordered as:
> channels 0–1: piezovibration readings.
> channels 2–7: piezoresistive velostat readings.
> channels 8–13: IMU motion readings.
> channel 14: pressure-like contact reading.
> surface_cards is a JSON list of exactly five objects. Each object has:
> surface: string. Row-local alias from S01 through S05.
> vibration_profile: list of eight integers from 0 to 63.
> resistance_profile: list of eight integers from 0 to 63.
> motion_profile: list of eight integers from 0 to 63.
> pressure_profile: list of four integers from 0 to 63.
> contact_band: string. Coarse anonymized contact descriptor: low, medium, or high.
> profile_energy_bucket: integer. Coarse total-energy bucket for the card.
> Example surface_cards item:
> {"surface":"S03","vibration_profile":[31,34,35,29,27,30,32,33],"resistance_profile":[20,22,26,24,21,23,25,22],"motion_profile":[39,37,35,36,40,41,38,36],"pressure_profile":[48,51,49,50],"contact_band":"medium","profile_energy_bucket":6}
> Task
> Submit one ordered route string per row. A route is a space-separated sequence of contact tokens.
> Valid examples:
> S03:F1 S01:F2 S05:F0 S02:F1
> S04:F0 S04:F2 S02:F1 S05:F1 S01:F2
> Rules:
> Every token must have the form Sxx:Fy.
> Sxx must be one of S01, S02, S03, S04, or S05.
> Fy is a force tier and must be one of F0, F1, or F2.
> F0, F1, and F2 represent low, medium, and high relative contact strength within the generated scan.
> The route may contain repeated surface aliases.
> The route may contain at most five tokens.
> An empty route is structurally valid but scores 0 because every hidden route has contacts.
> Do not submit JSON, comma-separated values, source texture names, explanations, or extra columns.
> Evaluation
> Structurally invalid submission files are rejected. Structural errors include missing columns, extra columns, duplicate IDs, unknown IDs, missing IDs, wrong row count, or wrong column order.
> Malformed row-level routes score 0 for that row instead of crashing the grader. Rows are aligned by id, not row order.
> For each row, let Pred be the submitted alias sequence and True be the hidden alias sequence.
> SurfaceEditSimilarity is normalized Levenshtein similarity after stripping force tiers and keeping only the surface aliases:
> SurfaceEditSimilarity =
> max(0, 1 - edit_distance(PredSurfaces, TrueSurfaces) / max(len(Pred), len(True), 1))
> SurfacePositionAccuracy rewards exact surface aliases at exact positions, ignoring force tier:
> SurfacePositionAccuracy =
> number of positions i where PredSurface[i] == TrueSurface[i]
> / max(len(Pred), len(True), 1)
> TokenPositionAccuracy rewards exact full contact tokens at exact positions:
> TokenPositionAccuracy =
> number of positions i where Pred[i] == True[i]
> / max(len(Pred), len(True), 1)
> TokenBigramF1 is F1 over adjacent ordered full-token pairs. For example, S03:F1 S01:F2 S05:F0 has bigrams (S03:F1,S01:F2) and (S01:F2,S05:F0).
> TokenBigramPrecision = matched predicted token bigrams / number of predicted token bigrams
> TokenBigramRecall = matched predicted token bigrams / number of true token bigrams
> TokenBigramF1 = 0 if both denominators are not positive; otherwise
> TokenBigramF1 = 2 * TokenBigramPrecision * TokenBigramRecall / (TokenBigramPrecision + TokenBigramRecall)
> SurfaceMultisetF1 is F1 over the multiset of surface aliases, ignoring order and force tier but respecting repeated aliases.
> SurfaceMultisetPrecision = matched predicted surface aliases / number of predicted surface aliases
> SurfaceMultisetRecall = matched predicted surface aliases / number of true surface aliases
> SurfaceMultisetF1 = 2 * SurfaceMultisetPrecision * SurfaceMultisetRecall / (SurfaceMultisetPrecision + SurfaceMultisetRecall)
> ExactRoute is 1 only when the entire normalized contact route exactly equals the hidden route, including force tiers; otherwise it is 0.
> The row score is:
> row_score =
> 0.15 * SurfaceEditSimilarity
> + 0.20 * SurfacePositionAccuracy
> + 0.25 * TokenPositionAccuracy
> + 0.25 * TokenBigramF1
> + 0.05 * SurfaceMultisetF1
> + 0.10 * ExactRoute
> The hidden set is balanced across five private generation families:
> steady_scan
> repeat_contact
> weak_middle
> dropout_band
> speed_warp
> Family labels are not present in solver-facing files. They are used only for robust hidden scoring.
> Final score:
> overall_mean = mean(row_score over all hidden rows)
> worst_family_mean = minimum family mean over the five private families
> bottom_20_mean = mean(row_score over the lowest-scoring 20% of hidden rows)
> final_score =
> 0.75 * overall_mean
> + 0.15 * worst_family_mean
> + 0.10 * bottom_20_mean
> Scores are finite and bounded in [0, 1]. The sample submission scores 0. A perfect oracle scores 1.
> Submission format
> Submit a CSV with exactly two columns in this order:
> id: test row ID.
> predicted_surface_route: space-separated contact route tokens.
> Example:
> id,predicted_surface_route
> 0a12bc34de56f789,S03:F1 S01:F2 S05:F0 S02:F1
> What not to use
> Do not use raw source texture names, source filenames, experiment indices, row order, or fixed alias meanings. These are absent from solver-facing rows or regenerated per row.
> Do not assume a single global class label. Each row is a sequence route, aliases are local to that row, and the force tier must be inferred from the trace.
> Do not submit every surface card in a fixed order. The metric heavily rewards exact position and adjacent transition recovery.
> Do not optimize only clean scans. Hidden scoring includes repeated contacts, weak middle contacts, sensor-dropout bands, and speed-warped routes.
> Benchmark boundary
> The nearest common task family is tactile texture classification from sensor recordings. That task predicts one texture label for one trial. This benchmark instead asks for source-disjoint contact-route reconstruction from composite multimodal traces, using row-local candidate cards, force-tier inference, and a sequence output grammar. It measures tactile sequence binding and in-context surface/force matching rather than ordinary sensor classification, regression, or metadata prediction. This is a completely original and highly novel problem.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Silent Indonesian Sentence Lipreading From Mouth Videos

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70w9bh41z02yganpcfyht6v988ydkr
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: A10G
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: video, Based on dataset:, LUMINA Indonesian Mouth Video Official Subset, Download Data
- Best/top context found: Top score: —

Full challenge description from page:

> Silent Indonesian Sentence Lipreading From Mouth Videos
> Overview
> Silent visual transcription can support deaf and hard-of-hearing users by converting visible speech into readable text when audio is unavailable, unreliable, or intentionally removed for privacy. In this challenge, each example is a short mouth-centered MP4 clip of one Indonesian sentence, and the task is to transcribe the sentence as normal text from the visual mouth motion alone.
> You receive labeled training clips and unlabeled test clips. The public files contain silent re-encoded videos with opaque row ids; they do not include audio, source filenames, speaker ids, sentence numbers, source order, or transcript metadata for test rows. For each test clip, submit one free-form transcript string and a confidence score.
> The output is a transcript, not a structured slot table. Do not submit columns such as color, digit, verb, place, speaker, or sentence id; the grader only accepts pred_transcript as a normal sentence string.
> What Not To Use (any of these can cause solution rejection regardless of leaderboard score):
> Audio extraction, WAV files, hidden raw files, private answers, or any non-public data.
> Source lookup, source reconstruction, media fingerprint matching against external corpora, or answer recovery from public dataset mirrors.
> Filename, public id, row order, video metadata, source speaker, source sentence number, or file-size side channels.
> Structured slot parsers or schema-specific submissions that replace the required transcript string with separate fields.
> Hand-built answer dictionaries, exact train-to-test lookup tables, or nearest-neighbor copying that ignores the test video.
> Hosted commercial APIs or closed-source models for prediction, distillation, pseudo-labeling, or manual transcription.
> Extra columns, reordered columns, duplicate ids, missing ids, malformed confidence values, or over-long transcript strings.
> Enforcement on invalid approaches: solutions that use source lookup, media fingerprinting, audio, private data, row-order tricks, or structured-slot shortcuts may be rejected before payout. The intended solution is learned visual speech recognition from silent MP4s, optionally with an open-weight video, speech, or language model adapted on the public training data.
> Intended Approaches: Train or fine-tune a model that reads the public silent MP4 frames and emits a transcript sequence. Reasonable approaches include a 3D CNN, video transformer, frame encoder with temporal pooling, visual-speech encoder with CTC or sequence-to-sequence decoding, or a hybrid that extracts mouth-region visual features and decodes them with a language model trained or adapted only on the public training transcripts. Use validation splits from train.csv to tune transcript normalization, decoding, and confidence calibration. Generic open-weight vision, video, speech, or text backbones are allowed when they are trained or adapted using only the provided public challenge files; the test videos should be used only for the final forward pass that produces predictions.
> Evaluation
> The grader normalizes transcripts by lowercasing, removing punctuation/diacritics, and collapsing whitespace. Each row receives word-level, character-level, exact-match, length, and calibration credit:
> word_score   = max(0, 1 - word_edit_distance(pred, truth) / true_word_count)
> char_score   = max(0, 1 - char_edit_distance(pred, truth) / true_char_count)
> exact_score  = 1 if normalized transcript is exact, else 0
> length_score = max(0, 1 - abs(pred_word_count - true_word_count) / true_word_count)
> content      = 0.50*word_score + 0.30*char_score + 0.15*exact_score + 0.05*length_score
> calibration  = 1 - abs(confidence - content)
> row_score    = 0.95*content + 0.05*calibration
> The final score blends mean row quality with worst hidden-subgroup performance:
> Final = 0.70 * mean(row_score)
> + 0.08 * worst opening-word family
> + 0.07 * worst color-word family
> + 0.06 * worst preposition family
> + 0.05 * worst character-length bucket
> + 0.04 * worst word-count bucket
> Here worst means the lowest subgroup mean row score within that hidden axis.
> These weights are chosen to match free-text visual speech recognition rather than a slot-filling task. Word accuracy gets the largest weight because word error rate is the most direct measure of whether a transcript is usable. Character accuracy gets the next largest weight so near-correct Indonesian spelling and visually similar mouth shapes still receive partial credit. The exact-match bonus rewards fully usable transcripts without making the metric all-or-nothing, and the small length term discourages blank, one-word, or padded guesses. Confidence affects only a small calibration component so solvers cannot win through confidence tricks; they still need accurate text. The final score keeps most weight on mean row quality while reserving 30% for worst-subgroup performance, so a model must work across different sentence starts, mid-sentence content words, relation words, and sentence lengths instead of doing well only on the easiest rows.
> The split is created before public ids are assigned. Complete source speaker groups are held out for the hidden test set, while the public train set uses different speaker groups from the same recording protocol and sentence style. This tests realistic speaker generalization but remains learnable because train and test share the same language, camera framing style, mouth-centered video format, and transcript distribution. The public files then remove source filenames, speaker ids, sentence ids, source order, audio, and metadata.
> Hidden subgroup axes are derived only inside preparation/grading from hidden truth transcripts and hidden media properties. The opening-word, color-word, and preposition axes are semantic word-family coverage checks from normalized hidden transcript tokens; the character-length and word-count axes are sentence-length buckets. These values are not public columns and are not encoded in public ids or paths. Preparation checks that hidden buckets have enough rows before writing the challenge, so the worst-subgroup terms measure broad lipreading quality rather than memorization of a tiny group.
> Higher is better. The theoretical minimum is 0.0; the theoretical maximum is 1.0. Perfect normalized transcripts with confidence 1.0 score exactly 1.0.
> Structural malformed submissions raise an internal InvalidSubmissionError: wrong, extra, or reordered columns; duplicate ids; missing or extra ids; row-count mismatch; missing, non-finite, or out-of-range confidence; and non-numeric confidence are all structural failures. The hidden answers file uses the same columns as a valid submission: id, pred_transcript, confidence. The public score for a structurally malformed submission is 0.0 after the grader catches that error. Row-local malformed transcript content, including blank or over-long transcript strings, receives zero for that row without leaking labels.
> Dataset
> The prepared data is under public/. Video paths are relative to the public/ directory and point to silent MP4 files. Public ids and paths are opaque and do not encode source filenames, source speaker ids, sentence numbers, or train/test order.
> File overview
> public/train/videos/*.mp4 contains labeled training clips; public/test/videos/*.mp4 contains unlabeled test clips; public/train.csv contains training inputs plus transcript labels; public/test.csv contains test inputs only; and public/sample_submission.csv is a weak schema-valid submission template.
> | Item | Description |
> |---|---|
> | train/videos/*.mp4 | Train videos |
> | test/videos/*.mp4 | Test videos |
> | train.csv | Inputs + labels |
> | test.csv | Inputs only |
> | sample_submission.csv | Template |
> train.csv columns
> id is an opaque public row id. video_path is the relative path from public/ to the silent MP4 clip. pred_transcript is the train-only Indonesian sentence label. The feature columns shared by train.csv and test.csv are exactly id and video_path.
> | Column | Type | Description |
> |---|---|---|
> | id | string | Opaque row id |
> | video_path | string | Path to MP4 |
> | pred_transcript | string | Train transcript |
> test.csv columns
> id is an opaque public row id. video_path is the relative path from public/ to the silent MP4 clip.
> | Column | Type | Description |
> |---|---|---|
> | id | string | Opaque row id |
> | video_path | string | Path to MP4 |
> Submission
> Submit a CSV with exactly one row per id in test.csv and exactly these columns in this order: id, pred_transcript, confidence.
> id must match the test id set exactly. pred_transcript must be a normal transcript string with at most 160 characters and at most 24 normalized words. confidence must be a finite float in [0,1].
> | Column | Type | Constraint |
> |---|---|---|
> | id | string | Same ids as test |
> | pred_transcript | string | Transcript text |
> | confidence | float | In [0,1] |
> Example submission format:
> id,pred_transcript,confidence
> li_0a12bc34de56ff,cari enam fonemik hijau dari solo,0.72
> li_1b23cd45ef67aa,baca delapan gondola ungu ke loket,0.64
> li_2c34de56fa78bb,lihat satu piano merah di sekolah,0.51

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Stroboscopic Field Sequence Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7eg7bvb4a3n2zd176m1090218dty44
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; challenge detail page timed out
- Difficulty: Medium
- Compute: Not displayed; challenge detail page timed out
- GPU: Not displayed; challenge detail page timed out
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage card score context: Beat pvduy's score of 0.424!

Full challenge description from page:

> Overview A scanning field sensor records only one of four interleaved spatial lattices per acquisition. A complete spatial layout is therefore distributed across an ordered set of measurements rather than appearing in any single input frame. Each sample contains eight noisy sparse observations of a normalized 64 x 64 vorticity field. Exactly 1,024 of 4,096 grid sites are measured at each step. The phase rotates through the four coordinate parities, so every site is visited once during each four-step cycle but never as part of a simultaneous full-field observation. This is a GPU sequence-to-sequence reconstruction task. The model translates an eight-frame sparse spatial sequence into a four-channel dense target sequence in a fixed order. Evaluation rewards both pointwise field accuracy and radial energy-spectrum fidelity. What Makes This Challenge Different Prediction unit: one example is an asynchronous eight-step sensor history, not a fully observed frame or a static image. Target: one submission row contains four ordered dense output fields rather than an image label or a single reconstructed frame. Observation process: a moving parity lattice reveals only 25 percent of the grid at each time, with small sensor noise and no simultaneous dense input. Data construction: every window receives a consistent periodic translation, dihedral transform, and nonlinear periodic row-column shear. The result is a new sequence-reconstruction example rather than a repackaged pre-existing sample. Dependency control: complete trajectories are split before window creation. Byte-identical trajectories discovered during auditing are excluded rather than allowed to cross partitions. Metric: normalized field error is combined with radial log-power error, then evaluated with channel weights that emphasize the two most distant output frames. Shortcut resistance: participant IDs are cryptographic opaque labels; simulation identities, frame offsets, transformations, dependency groups, construction keys, and visibility are withheld. Output protocol: each dense target sequence is an exact-size little-endian float16 tensor encoded as base64, allowing strict validation without a 16,384-column CSV. Task For every row in test.csv, translate the corresponding sparse tensor row in test_inputs.npz into four complete normalized scalar fields. Preserve the target-channel order learned from train_targets.npz. Write one encoded output sequence for every test sample_id. Targets The target tensor has shape 4 x 64 x 64. Its first axis contains target channels 0, 1, 2, and 3 in the fixed order used by train_targets.npz. Spatial axes use row-major order on a periodic grid. All fields use one global normalization fitted only on training trajectories. Training targets are stored as int8 values with scale 0.0625. Convert them to floating-point values with: target = target_sequence_q.astype(float32) * 0.0625 The targets are sensor-noise free. The sparse input measurements include zero-mean observation noise with standard deviation 0.125 in normalized field units. Prediction Rules Valid decoded predictions must: have shape 4 x 64 x 64; use little-endian float16 values; be flattened in C order, with output channel first, then row, then column; contain exactly 16,384 finite values, or 32,768 decoded bytes; remain inside the inclusive range [-12, 12]; and appear exactly once for every test sample_id. The float16 bytes must be base64 encoded in the target_sequence_b64 column. Row order is ignored because the grader joins by sample_id. What Makes the Task Difficult At one input step, three quarters of the field are missing. Combining four successive phases produces a spatially complete mosaic, but its four parities come from different positions in the ordered acquisition sequence. Simple inpainting ignores cross-step structure, while ordinary image-to-image reconstruction does not model an ordered multi-input, multi-output sequence. The periodic shears and spatial transforms prevent a fixed pixel location or image border from identifying an originating simulation group. Observation noise prevents exact value hashing. The four output channels require learning nonlinear cross-channel structure rather than copying an input mosaic. Finally, overly smooth outputs can have acceptable pointwise error while losing important high-frequency structure, which is why the metric includes spectral fidelity. Data Files The prepared public directory contains: train.csv: 1,024 training IDs and phase sequences. test.csv: 256 test IDs and phase sequences. train_inputs.npz: training sampled_values_q and phase arrays. test_inputs.npz: test sampled_values_q and phase arrays. train_targets.npz: four dense targets for each training row. tensor_schema.json: shapes, dtypes, scales, phase definitions, and submission byte order. metric_config.json: score constants and valid prediction bounds. sample_submission.csv: a structurally valid zero output sequence for every test ID. The prepared public files occupy about 33 MiB. No network access is required after preparation. CSV Fields train.csv and test.csv both contain: sample_id: opaque unique sample identifier. phase_sequence: eight space-separated phase integers matching the corresponding NPZ phase row. sample_submission.csv contains: sample_id: one of the IDs from test.csv. target_sequence_b64: base64 representation of one float16 tensor with shape 4 x 64 x 64. There is no participant-facing array index. NPZ row i corresponds directly to CSV row i in the matching split. Input Format sampled_values_q has shape N x 8 x 1,024 and dtype int8. Dequantize it by multiplying by 0.0625. phase has shape N x 8 and dtype uint8. A phase identifies the measured parity inside each 2 x 2 block: phase 0: even row, even column phase 1: even row, odd column phase 2: odd row, even column phase 3: odd row, odd column For sample i and observation j, reshape sampled_values_q[i, j] to 32 x 32 and place it at: dense[row_parity::2, column_parity::2] All other locations at that observation time are unavailable, not measured zeros. A binary mask can be reconstructed from the same phase. target_sequence_q has shape N x 4 x 64 x 64 and dtype int8. It appears only in train_targets.npz. Dataset Construction The challenge uses a self-contained collection of numerically generated single-channel periodic fields. Creator-side full-group hashing removes exact duplicates before any split or fitted statistic is created, leaving 80 independent simulation groups. Complete groups are then assigned to train, public test, or private test before any windows or transforms are generated. Dense simulation fields are reduced to 64 x 64 with non-overlapping mean pooling. A global mean and standard deviation are fitted using training groups only. Every retained 16-state sample receives a shared periodic translation, dihedral transform, and nonlinear periodic row-column shear. Eight selected states generate the rotating sparse input sequence, while four fixed target positions generate the ordered dense target sequence. Sparse observations receive small independent sensor noise before quantization, while targets remain clean. Evaluation For sample s and output channel c, let y be the true field and y_hat the submitted field. The normalized pointwise error is: field_error = L2(y_hat - y) / (L2(y) + 1e-6) The grader then computes orthonormal two-dimensional Fourier power. Radial bins 1 through 12 contain frequencies with integer radius b <= r < b + 1. Let P and P_hat be the 12 mean-power values: spectrum_error = L2(log1p(P_hat) - log1p(P)) / (L2(log1p(P)) + 1e-6) The channel skill is: combined_error = 0.75 field_error + 0.25 spectrum_error channel_skill = exp(-6.0 * combined_error) Channel weights are 1/6, 1/6, 2/6, and 2/6 in target order. The final score is the mean weighted channel skill over scored samples, clipped to [0.001, 1.0]. Higher is better. An exact submission scores 1.0 on both public and private data. A valid all-zero output scores about 0.00248. Platform settings: Grade Direction: Maximize Min Score: 0.001 Max Score: 1.0 Malformed payloads, non-finite values, out-of-range values, wrong columns, duplicate IDs, missing IDs, or extra IDs receive 0.001. Split and Leaderboard Design The effective split contains 80 unique trajectory groups and 16 windows per group: train: 64 trajectories and 1,024 windows public test: 4 trajectories and 64 windows private test: 12 trajectories and 192 windows Test size is 25 percent of train size. Public test is 25 percent of all test rows and independent trajectory groups. Trajectory-level vorticity RMS and high-frequency spectral share are stratified across partitions. No trajectory, duplicate dependency, temporal sibling, or derived window crosses a partition. Creator-side validation used ten equal-quality, trajectory-correlated perturbations. Public score standard deviation was about 0.00125 and private score standard deviation was about 0.00086. Ten ordered quality levels produced public/private Spearman rank correlation 1.0 and top-3 overlap 3 of 3. Tested baseline families also had public/private rank correlation 1.0. Submission Write submission.csv with exactly these columns and this order: sample_id,target_sequence_b64 skr_0123456789abcdef,AAAAAA... Python encoding example: import base64 payload = base64.b64encode( prediction.astype("<f2").reshape(4, 64, 64).tobytes(order="C") ).decode("ascii") The example uses a placeholder ID. Use the exact IDs from test.csv in a real submission. Expected Output A valid submission has 256 rows and two columns. Each payload decodes to exactly 32,768 bytes. The provided sample submission demonstrates the required schema but contains only zero output sequences and does not reveal hidden targets. What Not to Use Use only the released participant-facing challenge data and compute available in the challenge environment. Do not recover, download, search for, or match hidden simulation identities, sequence positions, construction parameters, dependency groups, visibility labels, or withheld target fields. Do not derive outputs from hashes, row order, filenames, external data collections, or any recovered simulation identity. These are challenge-integrity constraints. CPU approaches remain allowed; they are simply less competitive for the intended dense spatiotemporal workload. Recommended Modeling Direction Reconstruct value and mask channels for all eight observation steps. It is useful to build separate mosaics from steps 0 through 3 and steps 4 through 7, because their difference contains ordered sequence information even though neither mosaic is a complete simultaneous observation. Periodic convolutions, multi-frame U-Nets, Fourier neural operators, recurrent sequence-to-sequence field models, and compact video transformers are natural starting points. Producing a residual relative to a reconstructed stroboscopic mosaic can stabilize training. A loss that combines field error with gradient or spectral structure better matches the evaluator than plain per-pixel MSE. The supplied reference model is a 605,764-parameter periodic residual CNN. Three independent 10-epoch GPU runs scored 0.2805, 0.2835, and 0.2908 on public data, with corresponding private scores 0.2837, 0.2870, and 0.2942. On the creator machine, the same one-epoch workload processed about 88.1 examples per second on MPS and 15.7 on CPU, a 5.62x throughput advantage with matching loss. The challenge is targeted at an A10G-class GPU and is designed to leave room for stronger spectral and attention-based models. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Cross-Speaker Lexical Change Detection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7669xq80t6mheyr8zj8njt7n8dtsqg
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat aneeshm44's score of 0.890!

Full challenge description from page:

> Overview Compare two independently recorded Russian word streams and report the words added to or removed from the second stream. Each input is one stereo recording: the left channel is before, and the right channel is after. Return the lexical changes only, not either full transcription. Word order, speaker identity, timing, and volume may change without a lexical change. Shared words are spoken by different speakers in the two channels. Counting matters: if a word occurs twice before and once after, report one removal of that word. This is a controlled benchmark for comparing spoken inventories across recordings. Each channel combines three to six isolated word clips, with partial overlap, independent timing, gain, echo, and low-level noise. It does not represent naturally recorded conversations. For example, before [дом, мост, дом, вода] and after [мост, вода, дом, лес] require {"added":["лес"],"removed":["дом"]}. Reordering the shared words does not change that answer. Files and Columns train.csv — 20,000 paired-recording inputs. train_labels.csv — their lexical changes. test.csv — 4,000 held-out paired-recording inputs. sample_submission.csv — a randomly filled format example. audio/train/ and audio/test/ — referenced stereo WAV recordings. train.csv and test.csv have identical columns: task_id (string): unique pair identifier. audio_path (string): relative path to a 3.5-second, stereo, 16 kHz, 16-bit PCM WAV. Keep the channels separate; averaging them discards the before/after distinction. train_labels.csv contains task_id (string) and target_json (JSON object with exactly two fields): added (array of strings): words whose occurrence count increased, repeated once for each added occurrence. removed (array of strings): words whose occurrence count decreased, repeated once for each removed occurrence. Use exact Russian spellings from the training labels. The 256-word vocabulary is shared across training and test. Target lists are sorted for readability, but their order is not scored. Each example contains one or two additions and one or two removals. An unchanged word should appear in neither list. A word occurs at most twice within one channel. Split and Scope The recordings come from 365 training speakers and 100 separate test speakers. The pools contain 6,144 training clips and 2,048 test clips: respectively 24 and 8 recordings per vocabulary word. No speaker or clip crosses the split. Within a pair, a shared word uses different speakers and different recordings between channels; no source clip is reused within that pair. Pairs reuse recordings within their split, so 24,000 pairs are not 24,000 independently collected recording sessions. The vocabulary is finite, source segmentation can be imperfect, and clip composition is more controlled than real conversational change detection. Public filenames omit original clip and speaker identifiers. Submission Submit UTF-8 CSV with exactly task_id,target_json, in that order. Include every test identifier exactly once. Each JSON object must have exactly added and removed; each value must be a list of at most six nonempty strings, each at most 80 characters. Empty lists are valid predictions. task_id,target_json change_example_1,"{""added"":[""лес""],""removed"":[""дом""]}" change_example_2,"{""added"":[""слово"",""слово""],""removed"":[""голос""]}" The identifiers and words above illustrate the format. Use the supplied test identifiers and vocabulary. CSV row order and JSON field/list order do not affect scoring. Duplicate JSON keys are invalid. Evaluation The score is mean per-pair multiset F1 of directional word changes. Treat each occurrence as an event (direction, word), where direction is added or removed. TP = sum over events e of min(predicted_count(e), true_count(e)) P = total number of predicted events, including repeated occurrences G = total number of true events pair_F1 = 2 * TP / (P + G) score = mean(pair_F1 over test pairs) F1 balances missed changes against invented changes. Unchanged content earns no credit, and the wrong direction is an error. Repetition is counted rather than collapsed to a set. Exact spelling and Unicode content must match; no normalization or transliteration is applied. Unknown words are valid guesses but cannot match a target. Scores range from 0 to 1, higher is better. Empty predictions score zero for this dataset because every pair has changes. If both prediction and reference were empty, their pair score would be one. Invalid per-row JSON, keys, list lengths, or string values score that row zero. Incorrect CSV columns and missing, duplicate, empty, or extra identifiers are file-level errors. What Not To Use Do not use external datasets, source copies, source-audio matching indexes, or web lookup of held-out clips. Do not hard-code test identifiers or answer dictionaries. Do not use hosted inference APIs or manually annotate test examples. Generic pretrained audio models are allowed; challenge-specific pretrained checkpoints are not. &nbsp;
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Reconstructing Typed Succession Lineage of Serial Publications

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx746h7e18zn0he9vc6y3d3f3h8drd9e
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat mrfizhz's score of 0.649!

Full challenge description from page:

> Overview Serial publications (journals, yearbooks, bulletins, newspapers) constantly **change identity over time*: one title *continues under a new name, several titles merge into one, or a title splits and one strand continues in part. Your task is to generate the succession lineage of a serial from descriptive attributes alone. Each item is one source serial together with a list of candidate successor serials — the source's real successors mixed with same-era serials that are not its successors (hard negatives). Given the source's and the candidates' attributes, you generate the source's outgoing succession edges as a short string: for each candidate that is a real successor, candidate_id:transition_type, joined by ; — or no_edge if the source has no successor among the candidates. The transition types are: continues — the candidate is the direct continuation of the source (a title change), continues_in_part — the candidate continues only part of the source (a split / partial carry-over), merged — the source is one of several serials merged / absorbed into the candidate. Why it is hard A succession edge links two different serials (the title changes), so exact-title matching and copying fail; you must reconcile evolving attributes — partial title overlap, publisher/place continuity, subject, temporal adjacency — jointly. The candidates include same-era hard negatives, so "pick any temporally adjacent serial" fails. The split is family-disjoint — test succession families are never seen in training — so a memorised lookup fails; you must learn the reconciliation function and generalise. The transition type depends on structure not visible in a single pair (a merge has several sources feeding one successor), so even a strong model cannot reach a perfect score. All free text is ciphered, so no external catalogue or pretrained prior applies. The cipher All free-text fields are passed through one fixed character substitution. This preserves the signals a model learns from — shared tokens between a serial and its successor, repeated publishers, matching places — while making the text unrecognisable and un-lookupable as any real publication. Years and a relabelled language code are kept as real signals. Data train.csv, test.csv, sample_submission.csv are UTF-8 CSV with a header. Fields item_id — string id of the item (one source serial). source — the source serial, as src|title|publisher|place|subject|lang|start|end (fields |-separated; text ciphered). candidates — the candidate successors, ' ## '-separated; each candidate is cK|title|publisher|place|subject|lang|start|end where cK (c0, c1, …) is its id **within this item**. target (train only) — the gold generation string (see Submission format). Test items are disjoint succession families from training. sample_submission.csv Predicts no_edge for every item. It scores 0. metadata.json Keys task, input_columns, submission_columns, types, metric, files. Informational. Evaluation Score = 0.70 · typed-edge-F1 + 0.30 · untyped-edge-F1, in [0, 1], higher is better. An edge is (item_id, candidate_id[, type]): untyped-edge-F1 — precision/recall F1 over the candidates you mark as real successors (candidate_id), regardless of type: partial credit for finding the succession link. typed-edge-F1 — the same, but an edge counts correct only if the transition type also matches. Because both are F1 over the real edges, predicting no_edge everywhere — or any constant — scores 0. Submission format A UTF-8 CSV with a header and exactly these columns, in order: item_id,target item_id — a test item id. target — a ;-separated string of cK:type entries (each cK a candidate id from that item, each type one of continues, continues_in_part, merged), or no_edge. Example item_id,target sl_1a2b3c4d5e6f7a,no_edge sl_9f8e7d6c5b4a3f,c3:continues sl_0011223344556a,c1:merged;c7:merged Requirements (violations rejected as invalid): exactly the columns above; one row per test item_id; the set of item_ids must exactly match the test set; no duplicates. A blank prediction is read as no_edge. Malformed entries are ignored. Allowed Any approach trained on the provided data, including from-scratch sequence models. Everything runs on the provided GPU. No network access at run time. What Not To Use No external data, catalogues, or pretrained models; no attempt to de-anonymize the cipher or identify the real serials. &nbsp;
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Shuffled Document Reconstruction and Selective QA

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7665ahf15gzxjtkaz29vhbpn8drhkk
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat aneeshm44's score of 0.707!

Full challenge description from page:

> Overview Reconstruct each shuffled document and answer all of its questions using only the supplied text. Every row contains the segments of one fictional document in scrambled order and five questions; some questions are deliberately unanswerable. The two outputs test complementary capabilities: discourse-level sequence reconstruction and evidence-grounded question answering. Names and events are fictional, so memorized world knowledge is not a substitute for reading the row. Files train.csv — training inputs. train_labels.csv — sequence and answer targets for training rows. test.csv — held-out inputs with the same feature columns as train.csv. sample_submission.csv — valid submission-format example. Input Columns train.csv and test.csv contain identical columns: task_id (string): unique row identifier. document_topic (string): broad document category. shuffled_segments_json (JSON array): shuffled document segments. Each object contains: segment_id (string): identifier used in the reconstruction output. text (string): segment text. questions_json (JSON array of length 5): question objects. Each object contains: question_id (string): identifier used in the answer output. question (string): question about the document. train_labels.csv contains: task_id (string): matching training-row identifier. target_json (JSON object): paragraph_order (array of strings): every segment_id in original document order. answers (object): maps each question_id to its short answer. The exact value UNANSWERABLE marks questions that cannot be answered from the document. Dataset Split and Leakage Controls The 3,590 source documents are divided into 2,872 training documents and 718 test documents using a deterministic seeded assignment at the document level. All five questions belonging to a document remain on the same side of the split. No source document contributes segments, questions, or answers to both training and test. Source document_id, question_id, and PDF path values are not released in the prepared files. Public identifiers are remapped, and row order is independently shuffled. These controls block direct joins through source IDs and prevent repeated questions from the same document crossing the split. A remaining leakage risk is external source lookup: the underlying benchmark is publicly downloadable and its text is distinctive. Using web search, a source copy, or an externally prepared answer table for held-out rows is prohibited. Because the source was publicly released before this challenge, pretrained models may also contain some source exposure; using the most recent source release and requiring joint reconstruction reduce but cannot eliminate that risk. Submission Submit a CSV with exactly two columns: task_id target_json target_json must contain exactly paragraph_order and answers. Include every segment once and one string answer for each question. task_id,target_json task_ab12,"{""paragraph_order"":[""seg_c"",""seg_a"",""seg_b""],""answers"":{""q_1"":""UNANSWERABLE"",""q_2"":""October 10""}}" Evaluation Each row receives the mean of a sequence-reconstruction score and an answer score. Let L be the Levenshtein edit distance between the submitted segment-ID sequence and the ground-truth sequence. Insertions, deletions, and substitutions each cost 1. Let n be the larger of the two sequence lengths. sequence_score = max(0, 1 - L / n) Invalid, unknown, or repeated segment IDs occupy a position but cannot match a target ID. Answers are normalized by lowercasing, removing punctuation and English articles, and collapsing whitespace. For answerable questions, the score is token F1: precision = shared_token_count / submitted_token_count recall = shared_token_count / target_token_count answer_F1 = 2 * precision * recall / (precision + recall) For an UNANSWERABLE target, credit is 1 only when the normalized submitted answer is also unanswerable; otherwise it is 0. answer_score is the mean over the five questions. row_score = 0.50 * sequence_score + 0.50 * answer_score final_score = mean(row_score over all test rows) Sequence reconstruction and question answering receive equal weight because both are required outputs; a solution that handles only one can score at most 0.5. Scores range from 0 to 1 and higher is better. Malformed row-level JSON scores 0 for that row. Missing, duplicate, or extra task_id rows are file-level errors. What Not To Use Do not use external datasets, copies of the source corpus, or web lookup of held-out text. Do not hard-code test IDs, document text, or answer dictionaries. Do not use hosted inference APIs or manually annotate test rows. Generic pretrained language models are allowed; challenge-specific pretrained checkpoints are not. &nbsp;
> $700 Pool
> Closes in 56m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Lost in Transmission: One-Sided Arabic-Latin Landmark Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx782nhzt7vavw23hncf42962d8dsswx
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat komilpamar's score of 0.962!

Full challenge description from page:

> Overview Medieval Arabic works and their Latin translations were often divided, cited, and edited under different traditions. A landmark that identifies the start of a proposition, line group, or scholarly reference unit in one edition may be absent from the corresponding translation. Recovering that location makes parallel reading, citation transfer, and digital critical-edition work possible. Each challenge case contains: an Arabic or Latin source passage divided into eight to twelve consecutive scholarly units; the corresponding passage in the other language as one continuous token sequence; a shared shuffled lattice of plausible target-language gaps. The internal landmarks have been removed from the target. Project every ordered boundary in the segmented source onto one candidate target gap. Cases run in both directions: Arabic to Latin and Latin to Arabic. This is not sentence alignment. The source units are inherited from critical-edition landmarks, may cross modern sentence boundaries, and can differ greatly in length. The translations are historical rather than literal, spelling is nonstandard, and technical names vary. The target has no supplied sentence segmentation. To prevent edition typography from revealing boundaries, challenge text is case-folded and Unicode punctuation is removed on both sides. A solver must combine cross-lingual meaning with a global monotone sequence decision. GPU use and locally available pretrained backbones are allowed and encouraged. The complete solution must run within the platform's 1.5-hour limit. Hosted inference services are not allowed. Task mechanics Suppose source_segments_json contains K ordered segments named u0 through u(K-1). There are K-1 source boundaries: b0 is after u0 and before u1; b1 is after u1 and before u2; in general, bi is after ui and before u(i+1). target_text uses single-space tokenization. In this challenge, a token is exactly one item returned by: target_tokens = target_text.split() A candidate with "token_index": j is the gap before target_tokens[j], equivalently after the first j target tokens. Token indices are zero-based. All released candidates are internal gaps. For every source boundary, choose exactly one candidate gap_id. Chosen target positions must be strictly increasing in source-boundary order. Candidate JSON order and gap-id suffixes carry no answer information. Also provide a confidence between 0 and 1 for each selected boundary. It should estimate the probability that the selected gap_id is exactly correct. Example For eight source segments, the required boundary ids are b0 through b6. A valid prediction could be: [ {"boundary_id":"b0","gap_id":"g5","confidence":0.82}, {"boundary_id":"b1","gap_id":"g1","confidence":0.61}, {"boundary_id":"b2","gap_id":"g8","confidence":0.74}, {"boundary_id":"b3","gap_id":"g22","confidence":0.68}, {"boundary_id":"b4","gap_id":"g41","confidence":0.77}, {"boundary_id":"b5","gap_id":"g13","confidence":0.59}, {"boundary_id":"b6","gap_id":"g50","confidence":0.71} ] The JSON objects may appear in any list order. The grader restores boundary order using boundary_id before checking monotonicity. Evaluation Higher is better. The final score is bounded by 0 and 1, and a perfect calibrated submission scores exactly 1. For one case, let: B = K - 1, the number of internal boundaries; N, the number of whitespace-delimited target tokens; y_i, the gold token index for boundary bi; p_i, the submitted token index for boundary bi. Exact boundary accuracy ExactBoundaryAccuracy = mean(1[p_i = y_i] for i in 0..B-1) Induced segment overlap Add passage edges at 0 and N to the predicted and gold boundary sequences. These edges induce K corresponding target-token spans. For half-open token spans [a,b) and [c,d): intersection = max(0, min(b,d) - max(a,c)) union = max(b,d) - min(a,c) TokenIoU = intersection / union MeanSegmentIoU = mean(TokenIoU over the K corresponding spans) Sustained local path exactness For every consecutive run of three source boundaries, require all three projected gaps to be exact: TripletExact = mean( 1[p_i = y_i and p_(i+1) = y_(i+1) and p_(i+2) = y_(i+2)] for i in 0..B-3 ) This distinguishes a usable stretch of recovered edition structure from isolated lucky gaps while retaining boundary-level partial credit. Boundary proximity Set y_-1 = 0 and y_B = N. For boundary i: left_i = y_i - y_(i-1) right_i = y_(i+1) - y_i tolerance_i = max(4, 0.5 * min(left_i, right_i)) proximity_i = max(0, 1 - abs(p_i - y_i) / tolerance_i) MeanProximity = mean(proximity_i over all B boundaries) Whole-sequence exactness SequenceExact = 1 if every submitted gap id is correct, otherwise 0 Correctness and calibration Correctness = 0.30*ExactBoundaryAccuracy 0.30*TripletExact 0.20*SequenceExact 0.10*MeanSegmentIoU 0.10*MeanProximity CalibrationQuality = 1 - mean((confidence_i - 1[p_i = y_i])^2) RowScore = 0.96Correctness + 0.04CalibrationQuality Robustness aggregation The private cases are grouped in three ways: direction: Arabic to Latin or Latin to Arabic; lattice ambiguity: three equally sized groups ranked by the mean distance from each gold gap to its nearest decoy; held-out work: one group for each of the three unseen works, whose identities are not released. For each family, the grader calculates the mean row score in every group and retains the lowest group mean. FinalScore = 0.55*mean(RowScore) 0.15*worst direction mean 0.15*worst ambiguity mean 0.15*worst held-out-work mean Malformed or oversized row-local JSON, missing or repeated boundaries, unknown or repeated gap ids, non-finite confidence, confidence outside [0,1], or a non-monotone projection scores zero for that row. Wrong columns, row count, missing or extra case ids, or duplicate case ids invalidate the submission. Row order does not affect scoring. Dataset All paths below are relative to public/. train.csv contains 108 labeled cases from six works. test.csv contains 109 unlabeled cases from three different works. sample_submission.csv contains a structurally valid projection for every test case. metadata.json records source provenance, preparation rules, schemas, and aggregate audit counts. ATTRIBUTION.md records source credit, license terms, and the changes made to the derivative. The train/test split is by complete work. No work contributes text to both partitions. Filename stems, titles, bibliographic metadata, TEI tags, milestone labels, and source positions are absent from the case files. Public case fields case_id: opaque case identifier. source_lang: ar or la. target_lang: the other language. source_segments_json: ordered source-segment objects. target_text: the corresponding target passage with its internal landmarks removed. candidate_gaps_json: shuffled candidate target gaps. projection_json: present only in train.csv; contains the gold boundary-to-gap pairs for training cases. Source-segment object {"segment_id":"u0","text":"..."} Candidate-gap object {"gap_id":"g4","token_index":137} Each case contains exactly eight candidates per source boundary. The lattice includes the true positions and a superposition of coherent counterfactual segmentation paths produced from the target-unit length multiset. Every candidate in this release belongs to at least one such path; the constructor's collision fallback was not needed. The candidates are possibilities, not independent labels, and their originating paths are hidden. Gold-projection object {"boundary_id":"b0","gap_id":"g4"} Submission Submit exactly 109 rows with exactly these columns in this order: case_id projection_json Include every case_id from test.csv exactly once. Rows may appear in any order. projection_json must be a JSON list containing exactly one object for every required boundary. Each object must have exactly these fields: boundary_id: the required local boundary id; gap_id: one candidate id from that row; confidence: a finite number in [0,1]. Intended approach A competitive system will likely combine a multilingual or byte-level backbone with structured decoding. Useful directions include: fine-tuning a multilingual encoder or encoder-decoder on the labeled Arabic-Latin cases; scoring how well each source unit matches every target span induced by candidate pairs; using terminology, numerals, proper names, cognates, transliteration patterns, and neighboring-unit context; decoding the full boundary sequence with dynamic programming rather than choosing each boundary independently; ensembling models with different tokenization behavior on historical spelling; calibrating exact-boundary confidence on grouped training folds. A source-length heuristic is deliberately unreliable because the historical translations expand and contract unevenly and many competing paths are coherent under the same target-unit length evidence. Punctuation and case cannot be used because both are removed during preparation. Data and resource rules Use only the released challenge files and permitted pretrained model weights. External parallel corpora, reverse-text search, web retrieval, external answer data, and hosted inference APIs are not allowed. Predictions must be derived from the Arabic and Latin text released in each case. Do not exploit grader feedback, row order, identifiers, hashes, serialization details, or file metadata as prediction shortcuts. A complete solution must satisfy the platform's runtime and hardware rules.
> $700 Pool
> Closes in 1h 10m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Counterfactual Vampire Proof-search

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76kzpkdy7ngd84kkf5k61y0s8ds2d3
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat alba's score of 0.632!

Full challenge description from page:

> Counterfactual Vampire Overview Predict how hidden Vampire theorem-prover strategies behave on a problem. Each input is an ordered 120-token transcript from 120 probe strategies. The output is a 12-token survival signature. The hidden target panel contains exactly 240 different strategies, partitioned into 12 non-overlapping cohorts of 20. Each output token summarizes the number of successful strategies in one cohort. You predict 12 aggregates, not 240 individual outcomes. This is masked matrix completion over a real problem-by-strategy performance matrix. Probe outcomes reveal a problem's latent difficulty profile, which is statistically related to performance under other strategies. Aggregating 20 outcomes makes each target less dependent on one strategy. The task does not assume a deterministic mapping; it measures learned generalization to unseen TPTP families. Leakage controls are structural: Complete TPTP families are held out: 31 train groups, 10 test groups, and 0 overlap. Using training-family outcomes only, strategy ranks 1–240 form the target panel and ranks 241–360 form the probe panel. Probe/target overlap is 0. Target strategies are assigned round-robin to 12 cohorts of 20. Quantile thresholds use training-family target counts only and are then frozen. All 7,149 retained probe sequences are distinct, with feature-identical train/test overlap 0. Public rows expose only random IDs and token sequences. Source names, groups, strategy IDs, target counts, and test targets are hidden. Evaluation For target position k, let c_k be the number of UNS successes among its 20 hidden strategies, so c_k is between 0 and 20. For thresholds [b20,b40,b60,b80]: Q0: c_k <= b20 Q1: b20 < c_k <= b40 Q2: b40 < c_k <= b60 Q3: b60 < c_k <= b80 Q4: b80 < c_k The thresholds are nearest-rank training percentiles at 20%, 40%, 60%, and 80%. The frozen thresholds are: Positions 1 and 12: [0,3,11,19] Positions 2, 7, and 10: [0,2,12,19] Positions 3, 4, 5, 6, 8, and 9: [0,3,12,19] Position 11: [0,2,11,19] For example, [0,3,11,19] maps counts 0, 1–3, 4–11, 12–19, and 20 to Q0, Q1, Q2, Q3, and Q4. For row r, position j, predicted code p_rj, and true code t_rj, define: R_jq = mean(1[p_rj = t_rj] over rows where t_rj = q) B = mean(R_jq over all 12 positions and all 5 true classes) k_r = number of exactly correct positions in row r J = mean(k_r(k_r-1)/(1211) over rows) C = max(0, mean(sign(t_ri-t_rj)*sign(p_ri-p_rj))) raw = 0.60B + 0.20J + 0.20*C score = clip((raw - 0.06)/0.94, 0, 1) For C, the mean covers every row and unordered pair i<j for which t_ri != t_rj. A correct relative cohort order contributes 1, a predicted tie contributes 0, and a reversal contributes -1. B prevents frequent target states from dominating, while J and C require coupled cohort-level predictions. The 0.06 term is a deterministic contamination allowance for noisy single-run prover measurements. It does not randomly alter labels or scores: identical submissions always receive identical scores, zero raw credit remains 0, and perfect prediction remains 1. Equivalent code for already parsed integer codes is: import numpy as np def evaluate(y_true, y_pred): y_true = np.asarray(y_true, dtype=int) y_pred = np.asarray(y_pred, dtype=int) if y_true.shape != y_pred.shape or y_true.ndim != 2 or y_true.shape[1] != 12: raise ValueError("Expected matching arrays with shape (n_rows, 12)") hits = y_true == y_pred recalls = [ hits[y_true[:, j] == q, j].mean() for j in range(12) for q in range(5) ] balanced = np.mean(recalls) k = hits.sum(axis=1) joint = np.mean(k * (k - 1) / (12 * 11)) i, j = np.triu_indices(12, k=1) true_order = np.sign(y_true[:, i] - y_true[:, j]) pred_order = np.sign(y_pred[:, i] - y_pred[:, j]) informative = true_order != 0 cohort_order = max(0.0, np.mean(true_order[informative] * pred_order[informative])) raw = 0.60 * balanced + 0.20 * joint + 0.20 * cohort_order return float(np.clip((raw - 0.06) / 0.94, 0, 1)) Higher is better. Scores are clipped to [0,1]; a perfect submission scores 1.0. Malformed prediction content scores 0 for that row. Structural submission errors raise ValueError. Dataset train.csv: 5,037 rows with id, probe_sequence, and survival_signature. test.csv: 2,112 rows with id and probe_sequence. sample_submission.csv: 2,112 rows with id and a label-free survival_signature baseline. Private answers contain exactly id,survival_signature. The grader merges by id and uses only those trusted fields if the platform supplies auxiliary answer columns. Every probe_sequence contains exactly 120 ordered tokens. Position is fixed across rows. U0: proof success using at most 5% of the strategy's search limit. U1: success using more than 5% and at most 20%. U2: success using more than 20% and at most 50%. U3: success using more than 50%. TMO: timeout. GUP: unsuccessful early stop. ERR: failed run. Submission Submit exactly 2,112 rows with exactly the columns id,survival_signature. Each signature must contain 12 space-separated tokens from Q0 through Q4. id,survival_signature 128612157795,Q0 Q0 Q0 Q0 Q0 Q0 Q0 Q0 Q0 Q0 Q0 Q0 405873521411,Q3 Q3 Q3 Q3 Q3 Q3 Q3 Q3 Q3 Q3 Q3 Q3 Use every test ID exactly once. Row order does not matter. Requirements Missing, duplicate, or foreign IDs are rejected. Missing, renamed, or extra columns are rejected. Missing, malformed, NaN, infinite, out-of-range, or wrong-length signatures receive score 0 for that row. Use GPU computation for the substantive model or retrieval step. Maximum runtime is 90 minutes. What not to use Do not use external datasets, pretrained weights, runtime downloads, network access, or source problem-name lookups. Do not infer targets from id, CSV order, or hard-coded test predictions. Extra Modelling Information Counterfactual Vampire  performs per-problem cross-panel transduction. It observes a sequence from 120 probe strategies, predicts an ordered 12-position signature for 240 disjoint target strategies, and evaluates on entirely unseen TPTP families after removing exact transcript duplicates. It neither predicts a single tactic nor constructs one global schedule. The  mechanism is counterfactual survival-signature generation across disjoint prover panels under group-level domain shift; the real run matrix supplies observations rather than a pre-existing benchmark label. &nbsp;
> $700 Pool
> Closes in 2h 10m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Discourse Patch Generation: Order and Graph Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76v9by2nhhfs5h1b1p38957h8ashd2
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat sayantikalaskar's score of 0.842!

Full challenge description from page:

> Discourse Patch Generation: Order and Graph Repair Overview and Objective Each example represents a short passage as five to seven privacy-transformed discourse units and a nearly correct candidate discourse structure. The candidate contains exactly three faults: one pair of units is swapped in the reading order, one non-root unit has the wrong parent, and a different non-root unit has the wrong discourse relation. Generate the minimal repair patch. The patch must identify the swapped pair and replace the two corrupted links. Applying it to the candidate must restore the passage's original order and labeled rooted dependency tree. Unlike constructing a discourse graph from scratch, this task requires localizing coupled faults while preserving every already-correct decision. Dataset Files and Features train.csv contains 282 labeled examples: unit_id — string; opaque example identifier with a u_ prefix, always treated as text. segments_json — JSON-encoded array; five to seven segment objects. candidate_json — JSON-encoded object; corrupted candidate order and links. patch_json — JSON-encoded object; gold repair patch. test.csv contains 65 examples with unit_id, segments_json, and candidate_json. The hidden patch_json values are scored by the grader. sample_submission.csv contains exactly two string columns, unit_id and patch_json, with one valid dummy patch for every test ID. It demonstrates the required CSV and JSON syntax but does not contain hidden repairs. dataset_summary.json records train_examples, test_examples, segment_count_range, relation_labels, candidate_schema, patch_schema, and corruptions_per_example. Each object in segments_json has: id — string; local segment ID such as S1. tokens — string; punctuation, placeholders such as `, and per-example pseudolexical codes such as w3af`. Codes preserve repetition only within the same example and have no cross-example meaning. features — array of two strings. One value is a discourse-marker class: marker_additive, marker_anaphora, marker_attribution, marker_cause, marker_contrast, marker_temporal, or marker_none. The other is one deterministic coarse cue with prefix first_, head_, shape_, tense_, subord_, or len_, describing broad POS, head type, clause shape, tense marking, subordination, or length. candidate_json has exactly two keys: order — array of every segment ID exactly once, with one unknown pair swapped. links — one [child,parent,relation] array per segment. One child attaches to ROOT with relation root; all other parents are segment IDs. Exactly one non-root parent and one relation on a different non-root child are corrupted. Allowed non-root relations are attribution, cause, context, contrast, elaboration, evaluation, joint, and organization. Construction, Split Isolation, And Generalization Preparation selects closed discourse subtrees containing five to seven units from the 75-document source snapshot. Selected examples do not reuse discourse units, including within a split. Complete source documents are assigned to a single split before examples are emitted. The resulting training set has 282 examples from 57 documents; the test set has 65 examples from 16 different documents. Two source documents contribute no eligible selected examples. There are zero shared source documents, source discourse units, example IDs, or exact public examples between training and testing. Each example receives its own pseudolexical encoding and shuffled segment identifiers. Repeated token codes preserve repetition within that example; their spelling does not identify the same word across examples. Both splits intentionally use the same relation vocabulary and corruption family: one order swap, one parent fault, and one relation fault on a different child. Generalization means locating and repairing those faults in held-out passages, using the supplied structural and coarse linguistic cues. It does not mean extrapolating to unseen corruption types. Shared abstract structures can occur; document separation and the absence of duplicated examples prevent direct training-row lookup, but do not prove that every possible shortcut or source-reconstruction attack is impossible. Given the same raw snapshot and preparation seed, document selection, subtree selection, token transformation, segment shuffling, and corruptions are deterministic and reproducible. Reproducibility does not reuse training examples as test examples. Source lookup and source-corpus matching remain prohibited as stated below. Patch and Submission Format Write ./working/submission.csv with exactly two columns in this order: unit_id,patch_json. Include every test ID exactly once. The prediction columns are identical to the authored private answers.csv columns; any platform-added visibility field is leaderboard metadata, not a prediction. Each patch_json value must have exactly these keys: {"swap":["S2","S5"],"set_links":[["S1","S3","cause"],["S4","S2","context"]]} swap contains the two distinct segment IDs whose positions must be exchanged. Their order inside the array does not matter. set_links contains exactly two [child,parent,relation] repairs with distinct non-root children. Each repair replaces that child's candidate parent and relation together. The candidate root cannot be repaired. This is a complete illustrative CSV with a header and one row. Actual submissions must use the IDs from test.csv: unit_id,patch_json example_001,"{""swap"":[""S2"",""S5""],""set_links"":[[""S1"",""S3"",""cause""],[""S4"",""S2"",""context""]]}" Evaluation Higher scores are better. The final score is a weighted sum of four chance-adjusted corpus-level accuracies: S: exact accuracy of the unordered two-ID swap set. C: mean fraction of the two corrupted link children correctly localized. P: mean fraction of the two target children for which both localization and restored parent are correct. R: mean fraction of the two target children for which both localization and restored relation are correct. For an accuracy x and chance rate c, define: A(x,c) = max(0, (x - c) / (1 - c)) For an example with n segments, the chance rates are 1 / choose(n,2) for the swap, 2 / (n-1) for child localization, 2 / (n-1)^2 for parent restoration, and 2 / (8(n-1)) for relation restoration. Each chance rate is averaged over the test set to obtain cS, cC, cP, and cR. The complete scoring formula is: score = 0.30A(S,cS) + 0.20A(C,cC) + 0.25A(P,cP) + 0.25A(R,cR) The score is bounded to [0,1]. Aggregation And Design Rationale For each component and each row in the partition being scored, compute its correctness contribution and the nominal chance rate above. Average the correctness contributions to obtain S, C, P, and R; separately average the chance rates to obtain cS, cC, cP, and cR. Apply A once to each pair of corpus averages, then take the weighted sum. Do not average individually clipped per-row adjustments. Public and private partitions use this same procedure independently on their own rows. The weights reserve 30% for restoring reading order and 70% for graph repair: 20% for locating the corrupted children, 25% for their restored parents, and 25% for their restored relations. This rewards partial progress on fault localization while placing more total weight on repairing the graph. Parent and relation credit also requires correct child localization, so the components intentionally overlap. These weights are task-design choices, not estimates of statistical optimality. The nominal chance rates come from independent random proposals. An unordered swap is selected uniformly from choose(n,2) pairs. Two distinct repair children are selected uniformly from the n-1 non-root children, giving expected localization fraction 2/(n-1). A proposed parent is then selected uniformly from the n-1 segment IDs other than the child, giving joint localization-and-parent probability 2/(n-1)^2. A proposed relation is selected uniformly from eight labels, giving joint localization-and-relation probability 2/(8(n-1)). These reference rates are defined before conditioning proposals on final tree validity. They are not exact expected scores for a random generator restricted to valid repaired trees. Clipping the adjusted components at zero also means a finite random submission need not score exactly zero. Validation Rules The grader rejects wrong columns, missing or extra example IDs, duplicate example IDs, empty values, NaN, malformed JSON, extra JSON keys, wrong array lengths or types, unknown segment tokens outside S1 through S7, and unknown relation labels. A syntactically correct patch using the allowed vocabulary that violates the current example's constraints receives zero correctness for all four components on that row: this includes a segment absent from that example, repeated swap IDs, duplicate repair children, a repaired root, self-links, cycles, or a disconnected graph. These rows remain in the corpus averages and chance-rate averages. Valid repairs retain the partial-credit formula above. Invalid private gold patches remain evaluation errors. Use only the prepared public files. External source lookup, source-corpus matching, hardcoded test repairs, private-file access, and grader exploitation are prohibited. &nbsp;
> $700 Pool
> Closes in 3h 37m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Pilot-Conditioned Dual-Vocal Pitch Tracking in Hindustani Mixtures

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bf7xhrbd9sjs7bdagjvx0zd8dy26a
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat duongnguyen's score of 0.815!

Full challenge description from page:

> Pilot-Conditioned Dual-Vocal Pitch Tracking in Hindustani Mixtures Overview This is an audio sequence-to-sequence challenge. For each case, recover two ordered vocal pitch trajectories from one monaural mixture of overlapping Hindustani vocal passages. Two short enrollment pilots identify the streams: pilot index 0 defines output A and pilot index 1 defines output B. The assignment must remain stable through similar pitches, rapid ornaments, same-vocalist pairs, and contour crossings. The goal models an analysis tool for music teaching and archival work: an engineer may have short clean references for two voices but only a mixed recording of their simultaneous phrases. A useful system must follow each referenced voice's pitch movement rather than return an unordered set of active notes. Objective Predict pitch_a and pitch_b for every case_id. Each prediction is a JSON list of exactly 128 integer tokens. Token k represents MIDI pitch 36 + 0.5 × (k - 1) and therefore adjacent tokens are 50 cents, or half a semitone, apart. Valid tokens are 1 through 145. Position t describes the pitch at frame t; frames are spaced 512 samples (32 ms) apart at 16 kHz. There is no unvoiced token. The two outputs are ordered. pitch_a must follow the source represented by pilots[0], and pitch_b must follow pilots[1]. Swapping the sequences is not accepted as equivalent. Public Dataset | Path | Rows/files | Description | |---|---:|---| | train.csv | 1,800 rows | Packet paths and both labeled pitch-token sequences. | | test.csv | 450 rows | Packet paths for held-out source recordings; no target columns. | | sample_submission.csv | 450 rows | Syntactically valid seeded-random submission with every test ID. | | audio_packets/*.npz | 2,250 files | One input packet per case. | CSV columns The three CSV files have the following exact schemas. All files include one header row and no index column. train.csv columns Exact column order: case_id,packet_path,pitch_a,pitch_b case_id — string; required and unique. An opaque training-case identifier used for row identity. It contains no source, pitch, or split information. packet_path — string; required. A relative path such as audio_packets/pkt_.npz. Resolve it relative to ./dataset/public/ to load this row's input packet. pitch_a — string containing a JSON array of integers; required target. The array has exactly 128 integers in the inclusive range 1–145. It is the ordered pitch trajectory for the voice represented by pilots[0] in this row's packet. pitch_b — string containing a JSON array of integers; required target. The array has exactly 128 integers in the inclusive range 1–145. It is the ordered pitch trajectory for the voice represented by pilots[1] in this row's packet. train.csv contains 1,800 rows. Parse pitch_a and pitch_b with a JSON parser; they are serialized arrays inside CSV string fields. test.csv columns Exact column order: case_id,packet_path case_id — string; required and unique. An opaque test-case identifier. Copy every value exactly once into the submission. packet_path — string; required. The relative path from ./dataset/public/ to the test case's compressed NumPy input packet. test.csv contains 450 rows. It intentionally has no pitch_a or pitch_b columns; those are the two values to predict. sample_submission.csv columns Exact column order: case_id,pitch_a,pitch_b case_id — string; required and unique. The corresponding identifier from test.csv. pitch_a — string containing a JSON array of integers; required prediction. Exactly 128 integers, each from 1 through 145, for the voice identified by pilots[0]. pitch_b — string containing a JSON array of integers; required prediction. Exactly 128 integers, each from 1 through 145, for the voice identified by pilots[1]. sample_submission.csv contains all 450 test IDs and seeded-random, syntactically valid placeholder sequences. The placeholders are not hidden answers. Packet arrays Load packets with numpy.load(path, allow_pickle=False). | Array | dtype and shape | Meaning | |---|---|---| | mixture | int16, (65536,) | 4.096-second monaural mixture. | | pilots | int16, (2, 16384) | Ordered 1.024-second enrollment pilots; row 0 is A and row 1 is B. | | sample_rate | int32 scalar | Always 16,000 Hz. | Convert int16 audio to approximately [-1, 1] by dividing by 32,767. The split is disjoint at the original-recording level. All derived examples from one source recording stay on one side. Training uses 90 source groups and test uses 22 unseen source groups, with zero group overlap. Source names, performer identifiers, original titles, and pairing parameters are not present in public files. Submission Write the final CSV to ./working/submission.csv with exactly these columns in this order: case_id,pitch_a,pitch_b Requirements: Exactly 450 rows, one for every test case_id. IDs may be in any row order but must be unique, non-blank, and match the test set exactly. pitch_a and pitch_b must each be compact valid JSON lists containing exactly 128 integers from 1 through 145. Do not add columns. A backend-managed visibility column is ignored if present. Missing, extra, duplicate, null, non-integer, out-of-range, overlong, or malformed values reject the submission. Example value for one sequence (abbreviated here only for explanation): [63,63,64,...]. The submitted value must contain all 128 tokens; ellipses are invalid. Evaluation Submissions use the Pilot-Conditioned Dual-Contour Score. Higher is better. The theoretical range is 0.0 to 1.0, and exact hidden answers score 1.0. For one true stream y[0..127] and prediction p[0..127], let token error e[t] = |y[t] - p[t]|. proximity = mean(max(0, 1 - e[t] / 12)) fine_accuracy = mean(I(e[t] = 2: motion = mean(max(0, 1 - |dy[t] - dp[t]| / 12)) If a stream has no such transition, motion is the fraction of predicted transitions with |dp[t]| <= 1. stream_score = 0.55 × proximity + 0.30 × fine_accuracy + 0.15 × motion The row score is the equal mean of the A and B stream scores. The final score is the mean row score over all test cases. The grader aligns by case_id, not row order, and is valid on any non-empty answer shard. Constraints Use only the supplied public data and standard libraries already present in the selected runtime. Internet access, hosted APIs, external audio, source mirrors, original-recording lookup, audio fingerprinting, test-answer reconstruction, and manual labeling of the test set are prohibited. Public general-purpose models are allowed only when already available offline in the runtime; challenge-specific checkpoints and runtime package installation are not allowed. The intended approach uses CUDA-accelerated time-frequency features and a pilot-conditioned convolutional or attention model trained on the provided cases. Signal-processing and CPU models are valid baselines, but the dense two-stream time-frequency learning workload is why the A10G tier is selected. &nbsp;
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Powerlifting Attempt Policy: Predicting Sequential Risk Decisions Under Escalating Failure

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dpwxcq06rfe0msn29t09npx8dvfxk
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat spiderman's score of 0.548!

Full challenge description from page:

> Background A powerlifting meet is a sequential decision problem played out in the open. Each athlete performs three lifts in a fixed order (squat, then bench press, then deadlift) with exactly three attempts at each. Before every single attempt the athlete must declare the weight to the scorer's table in advance, and cannot change it once declared. They decide knowing only what has already happened in the meet. The consequences escalate down the sequence. Openers are conservative and almost always succeed. Third attempts are gambles: 37.9% of third squats, 54.5% of third benches and 44.1% of third deadlifts fail in this data. A failed attempt is spent, and three failures at any one lift ends the meet with no recorded total at all. What makes this a sequence problem rather than a set of independent guesses is that every declaration is conditioned on the outcomes before it. A lifter who has just missed a second attempt does not behave like one who made it. A lifter whose squats went badly enters the bench round with a different appetite for risk than one whose squats went well. The decision at position k is a function of the realised history at positions 1 through k-1. Task You are given an input sequence and must produce an output sequence. Input sequence: the athlete's complete squat round, being three ordered attempts each carrying both the declared weight and its realised outcome, together with athlete and meet context (sex, age, bodyweight, weight class, division, equipment, country, federation, date, meet name). Output sequence: the athlete's remaining six declarations, in the order they occur in the competition: Bench1Kg > Bench2Kg > Bench3Kg > Deadlift1Kg > Deadlift2Kg > Deadlift3Kg Each element of the output sequence is a signed value using the dataset's own convention. The magnitude is the weight declared in kilograms, and the sign encodes the realised outcome: positive for a successful lift, negative for a failed one. Predicting -172.5 means "they will call for 172.5 kg and miss it." You are therefore generating a policy trajectory: at each position, both the action taken and the consequence that follows, with every later position conditioned on the earlier ones. The elements are not exchangeable and cannot be permuted. Position 3 is a third bench attempt with all the risk-taking that implies, and position 4 is a first deadlift attempt with all the caution that implies. Swapping them is not a valid prediction. Decoding the output autoregressively, conditioning each declaration on those already emitted, is the natural approach, though any method is permitted. Files | File | Contents | |---|---| | public/train.csv | Training rows with the full sequence, input and output, for each athlete-meet entry. | | public/test_features.csv | Held-out rows with the output sequence removed. Carries a row_id column. | | public/sample_submission.csv | A valid submission of the correct shape with placeholder values, showing the required format. It scores 0.2952 and is not a competitive answer. | | private/ | Not accessible to your solution. | Columns that would trivially reveal any element of the output sequence have been removed from all provided files: Best3SquatKg, Best3BenchKg, Best3DeadliftKg, TotalKg, Place, Dots, Goodlift. Best3BenchKg, for instance, is simply the maximum of the three bench elements you are asked to generate. Split The test set consists of entire held-out national federations that appear nowhere in training: CPU, NSF, AEP, JPA, PA, PZKFiTS and UkrainePF. No athlete appears on both sides of the boundary. Athletes who competed under both a training and a test federation were removed entirely, so that individual habits cannot leak across the split. This split carries the scientific question. Attempt selection is taught. It reflects coaching convention, and convention differs between national federations, so a Norwegian lifter and a Japanese lifter are coached into different progressions. A model that has memorised how USAPL athletes bid has not obviously learned anything transferable. The challenge is whether a learned model of sequential risk-taking generalises to coaching cultures it has never observed. Training set: 462,392 sequences. Test set: 85,456 sequences. Submission Write submission.csv with exactly these seven columns, in this order: row_id,Bench1Kg,Bench2Kg,Bench3Kg,Deadlift1Kg,Deadlift2Kg,Deadlift3Kg Requirements, all enforced by the grader: Exactly seven columns, named and ordered as shown. Extra columns are rejected. Exactly 85,456 rows, one per row in test_features.csv, plus a header. Every row_id appears exactly once. Duplicate, missing, or unknown row_id values are rejected. Every prediction is a finite, non-zero number. Zero is not a valid prediction, because the sign carries the attempt outcome. Row order does not matter and does not affect the score. Any violation of requirements 1 through 4 rejects the whole submission. Offending rows are not scored as zero and skipped. Evaluation Each element of the generated sequence is scored, then averaged across the sequence and across all test rows. For an element with true signed value y and predicted signed value p: a = exp( -abs( abs(p) - abs(y) ) / (0.10 abs(y)) ) declared-weight accuracy b = 1.0 if sign(p) == sign(y) else 0.0 outcome accuracy score = 0.85 a + 0.15 * b The final score is the unweighted mean of score over all six positions of all test rows, bounded in [0, 1]. Higher is better. Three properties are deliberate: The weight term decays smoothly rather than cutting off at a threshold, so a near miss earns proportionate credit. The decay scale is relative to the true weight, so a 60 kg bench and a 300 kg deadlift are held to the same standard rather than the heavier lift dominating. The outcome term carries only 0.15. Outcomes are largely majority-predictable, and weighting them heavily would pay for guessing rather than for modelling the policy. Reference points measured on the held-out set: | Submission | Score | |---|---| | Perfect prediction | 1.0000 | | Gradient-boosted baseline | 0.5375 | | Strength-ratio heuristic | 0.4836 | | Shipped sample_submission.csv | 0.2952 | Notes No element of the output sequence is derivable by arithmetic from any provided column, and no fixed rule reproduces it. Constant-increment baselines ignore the conditioning structure entirely, which is where the headroom lies. Bomb-outs are in scope. Sequences in which all three attempts at a lift failed are real competitive outcomes, not corrupt records. A small number of entries carry implausible ages, below 10 in 0.08% of rows. These are upstream data-entry errors. The age value is blanked, and no attempt data is dropped. Athletes entered in multiple divisions at the same meet produce identical attempt records in the source. These are deduplicated on athlete, meet and full lift sequence, so no performance is scored twice. &nbsp;
> $700 Pool
> Closes in 4h 26m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Protocol-Aware MQTT Trace Restoration

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7d0g4256tyjpefgy64d5jx498dw0qk
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat aegistran's score of 0.662!

Full challenge description from page:

> Protocol-Aware MQTT Trace Restoration Overview MQTT is a lightweight publish/subscribe messaging protocol used by many Internet of Things systems. A packet capture or telemetry pipeline can contain gaps, duplicate records, corrupted packet labels, or small ordering errors. These artifacts make a logically valid session appear incomplete or protocol-invalid and complicate incident review, replay, and state reconstruction. Your task is to reconstruct the canonical MQTT control-packet sequence that existed before capture corruption. Each row contains a variable-length observed sequence, broad deployment context, and noisy capture-quality estimates. The target clean_trace is another variable-length sequence. This is sequence-to-sequence transduction, not attack classification or next-event prediction. All traces are synthetic, use abstract packet tokens rather than payloads, and are based on a generalized subset of MQTT 5.0 behavior. They contain no device identifiers, credentials, topics, payload data, or production traffic. Compute Constraint This is a CPU-only challenge. Solutions must not require a GPU or accelerator and should finish within approximately one hour in a standard Kaggle-compatible CPU environment. Sequence Representation Tokens are separated by one ASCII space. Each token encodes direction, packet type, and, when needed, Quality of Service (QoS), message identifier, subscription identifier, or retained state. Examples: C2B_CONNECT_NEW C2B_SUBSCRIBE_Q1_S0 B2C_SUBACK_Q1_S0 C2B_PUBLISH_Q2_M0 B2C_PUBREC_M0 C2B_PUBREL_M0 B2C_PUBCOMP_M0 C2B_DISCONNECT_NORMAL C2B means client-to-broker and B2C means broker-to-client. Message identifiers such as M0 are local to one trace. Subscription identifiers use S0, S1, and so on. The clean sequences encode protocol relationships including: CONNECT followed by optional enhanced authentication and CONNACK; SUBSCRIBE paired with SUBACK and UNSUBSCRIBE paired with UNSUBACK; QoS 0 publication without acknowledgement; QoS 1 publication followed by PUBACK; QoS 2 publication followed by PUBREC, PUBREL, and PUBCOMP; optional PINGREQPINGRESP keep-alive exchanges; a final client or broker disconnect event. Observed traces may omit, duplicate, substitute, or locally reorder tokens. The model must emit the complete clean sequence rather than an edit script. Evaluation Submissions are scored by the MQTT trace fidelity score, a quality-sensitive token-sequence restoration metric. Higher is better. For reference sequence y and prediction p, let d(y, p) be token-level Levenshtein edit distance and let |.| denote token count: row_similarity = 1 - d(y, p) / max(|y|, |p|) row_fidelity = row_similarity ** 4 score = mean(row_fidelity) The score lies in [0, 1]. An exact sequence scores 1; entirely wrong or excessively long output approaches 0. Insertions, deletions, and substitutions each cost one edit. Raising the row similarity to the fourth power gives substantially more credit to near-complete protocol restoration than to a superficially plausible trace that still contains several defects. The transformation is continuous and is applied independently to every row before averaging. The copy-observed-trace baseline scores approximately 0.103. Dataset Prepared data contains 16,000 traces from 800 synthetic device profiles: dataset/public/train.csv — 12,800 damaged traces with clean_trace labels from 640 devices; dataset/public/test.csv — 3,200 damaged traces from 160 unseen devices; dataset/public/sample_submission.csv — exact submission schema using the copy baseline. The split is group-disjoint by device_profile_id. All 20 traces for a device remain in one split. Row-random validation leaks persistent device, firmware, broker, and transport behavior. Identifiers and Persistent Context | Column | Type | Description | |---|---|---| | trace_id | string | Unique trace identifier used for submission matching | | device_profile_id | string | Device group; 20 sessions per profile | | client_role | category | sensor, actuator, gateway, or monitor | | firmware_family | category | Generalized MQTT client implementation family | | broker_profile | category | Edge, regional, or cloud broker context | | transport_profile | category | Stable LAN, cellular, congested Wi-Fi, or intermittent WAN | | scenario_family | category | Telemetry, command, bidirectional, churn, resume, retained, or request-response workflow | | keep_alive_seconds | int | Negotiated keep-alive interval | Capture Context and Sequences | Column | Type | Description | |---|---|---| | estimated_capture_loss_rate | float | Noisy estimate of missing-token rate | | estimated_duplication_rate | float | Noisy estimate of duplicate-token rate | | estimated_reorder_rate | float | Noisy estimate of adjacent-reordering rate | | estimated_token_error_rate | float | Noisy estimate of packet-label substitution rate | | observed_token_count | int | Number of tokens in observed_trace | | observed_trace | string | Damaged, space-delimited input sequence | | clean_trace | string | Training-only canonical target sequence | The rate columns are estimates, not exact edit counts. They cannot directly reveal which tokens changed or the target length. Clean-start state, session-present state, authentication use, QoS ceiling, message counts, subscription counts, and receive-maximum are intentionally hidden; solvers must infer their effects from the damaged trace and broad context. Submission Write ./working/submission.csv with exactly these columns: | Column | Type | Description | |---|---|---| | trace_id | string | Identifier copied from test.csv | | clean_trace | string | Predicted canonical packet-token sequence | Requirements: Include exactly 3,200 rows and every test trace_id exactly once. Use non-empty, space-delimited tokens containing only uppercase letters, digits, and _. Emit no more than 160 tokens per prediction. Include the header and no additional columns. Row order does not matter because the grader aligns by trace_id. &nbsp;
> $700 Pool
> Closes in 11h 24m
> 10 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Forecast Ink Recontact Order from Partial Assamese Pen Traces

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx731j1hka56bp94s5jh51bxv58dxqcy
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat minipeepee's score of 0.530!

Full challenge description from page:

> Forecast Ink Recontact Order from Partial Assamese Pen Traces Overview Predict a variable-length event sequence from an unfinished handwriting trajectory. You observe the pen's past motion and must output the order in which its future motion will first revisit eight older portions of the observed ink. Each region may occur at most once in the output; omit regions that are never revisited. This sequence-to-sequence problem models anticipation in incremental digital ink handling: a system needs to know where a writer is likely to return before committing earlier ink to further processing. Samples originate from real Assamese tablet handwriting. The complete glyph, its character label, and the future trajectory are unavailable. These are geometrical recontact events, not measurements of physical drying, pressure, or smearing. Objective and region vocabulary A case shows one partial trace as 128 ordered samples. The first coordinate is horizontal and the second is vertical in the recording's orientation. Coordinates are centered and scaled using the observed prefix only, then undergo a small shared affine calibration change. One unit is approximately the largest observed prefix extent. Coordinates are rounded to 0.001 units. A sample's ink flag indicates whether the interpolated point lies on a recorded pen-down segment. A straight interpolation between separate pen strokes has ink=0: it represents a gap, not an ink stroke. Sampling is uniform along accumulated path length, including straight inter-stroke travel for indexing. There are no timestamps. Divide the observed path-length parameter into ten equal consecutive intervals. Regions 1 through 8 correspond to the pen-down ink in the first eight intervals, in chronological order. The final two intervals remain visible as recent-motion context and are not target regions. In the public 128-sample sequence, region r is approximately the portion with normalized index (r-1)/10 <= index/128 < r/10; evaluation labels use a denser interpolation of the same observed measurements. Region identity is therefore case-relative, not a fixed location on the page. All eight regions contain observed ink. A future recontact occurs when the pen returns within 0.055 normalized units of a region's existing ink after being more than 0.09 units away from that region. Only future pen-down portions count. A short continuation guard excludes the first 12 points of a 768-point future interpolation, preventing the immediate continuation at the observation cut from becoming a return event. A region's event time is its first qualifying return. Equal discretized event times are ordered by increasing region number. This definition describes the label meaning; the future measurements needed to evaluate it are withheld. This release uses revision 2 cohort construction. For each original writing trace, the organizer examines eight deterministic candidate observation cuts between 48% and 68% of recorded points. It retains the first candidate with at least three future recontacts, or, if none qualifies, the first with at least two. Traces with no qualifying candidate are excluded. Eligibility also requires enough observed ink in every queried region. This selection uses future events to define the cohort; candidate selection is not independent of the target. It is identical across all writers and does not use model predictions. Only one candidate per source trace is released. This is an active-return cohort: every case is known to eventually revisit at least two different old regions. The exact regions, their order, and how many further regions are revisited remain unknown. Forecast until the end of the recorded symbol, without assuming a fixed elapsed time. You may submit zero through eight distinct region IDs, although true event sequences have at least two entries. Dataset The prepared data is in ./dataset/public/. | File | Contents | |---|---| | train.csv | 2,607 labeled cases from 37 writers, with 256 coordinate columns and the complete observed ink_mask sequence in each row. | | train_metadata.json | Validation-only writer groups and fold assignments, keyed by labeled case ID. | | train_prefix.npy | Optional float32 mirror (2607,128,3) of the decoded training CSV sequences, in CSV row order. | | test.csv | 627 unlabeled cases from 8 additional writers, with the same coordinate columns and ink_mask sequence. | | test_prefix.npy | Optional float32 mirror (627,128,3) of the decoded test CSV sequences, in CSV row order. | | sample_submission.csv | Valid seeded random three-region forecasts for all 627 test IDs. These values are examples, not answers. | train.csv columns: | Column | Type / allowed values | Meaning | |---|---|---| | case_id | nonempty string | Opaque identifier for submission alignment. | | x_000 through x_127 | finite number, read as float32 | Horizontal observed coordinate at each ordered sample. | | y_000 through y_127 | finite number, read as float32 | Vertical observed coordinate at each ordered sample. | | ink_mask | JSON array string of exactly 128 integer flags, each 0 or 1 | Flag at index i describes whether sample i lies on a pen-down segment. | | recontact_order | JSON array string, distinct integers 1–8 | Ground-truth first-return sequence. | test.csv contains case_id, 256 numeric coordinate columns, and the structured ink_mask field, with no target. Training has the identical features followed by recontact_order. Neither CSV has an array_index column. All features describe the observed prefix. The exact order is case_id,x_000,y_000,x_001,y_001,...,x_127,y_127,ink_mask; training additionally ends with recontact_order. There are 257 feature columns, 259 total training columns, and 258 total test columns. The complete pen-down channel is stored as one ordered sequence rather than 128 separate binary columns. Decode it with json.loads; retain all 128 positions, including rare pen-up gaps. There is no loss of observations. Recover the original (n,128,3) float32 sequence with: import json import numpy as np columns = [f"{axis}_{step:03d}" for step in range(128) for axis in ("x", "y")] xy = frame[columns].to_numpy(dtype="float32").reshape(len(frame), 128, 2) ink = np.asarray(frame["ink_mask"].map(json.loads).tolist(), dtype="float32") x = np.concatenate([xy, ink[..., None]], axis=2) The optional .npy files contain exactly these decoded float32 sequences, with one entry per CSV row in the same order. If you reorder CSV rows, reorder their corresponding arrays or reconstruct directly from those CSV rows. A gap must never be inferred from coordinates alone or replaced with a constant pen-down flag. train_metadata.json is a JSON object whose keys are exactly the labeled case_id values. Each value has two non-null fields: | Field | Type / allowed values | Meaning | |---|---|---| | writer_group | opaque string | Anonymous writer group for leakage-safe validation; not a predictive feature. | | fold | string: train or validation | Suggested held-out-writer development split. | Join this metadata to training rows by case_id, preserving the CSV row order. It contains no test IDs or targets. Use it only to select validation rows and keep writers disjoint; do not include these fields in model features. Each prefix array's final axis is [x, y, ink]. x and y are finite normalized float32 coordinates. ink is float32 with values 0 or 1. Samples are ordered and fixed-length, with no null values or padding. Do not treat gap interpolation as measured ink, or distort point order with time reversal or random permutation. The suggested training fold contains 2,029 cases from 30 writers; the validation fold has 578 cases from seven different writers. All cases for a writer stay together. There is one released case per original writing trace, so a later prefix from the same trace cannot reveal an earlier case's future. Test writers occur in neither development fold. You may refit on all 2,607 labeled cases after model selection. Evaluation The score is mean normalized Levenshtein similarity, maximized, with theoretical bounds 0 to 1. For true sequence T and predicted sequence P, let d(T,P) be the minimum number of single-token insertions, deletions, and substitutions needed to transform one sequence into the other. Each edit costs 1. row_score = 1 - d(T,P) / max(1, len(T), len(P)) score = mean(row_score over the evaluated cases) Perfect predictions score 1. Empty predictions score 0 on this cohort. Incorrect extra regions, omitted regions, and wrong order all reduce the score. The score is computed independently per case and remains valid on any nonempty evaluation shard. For example, [1,3] against [1,3] scores 1; [1] against [1,3] scores 0.5; and [3,1] against [1,3] scores 0. Submission Write ./working/submission.csv with exactly these columns, in this order: case_id,recontact_order ir_example,"[2,5,1]" Use the actual IDs from test.csv. There must be exactly 627 rows, with a header and one row per test ID. recontact_order must be a JSON list string of at most eight distinct integer tokens from 1 through 8. [] is valid. Do not use strings, decimals, repeated tokens, booleans, nulls, NaN, or infinity within the list. The field must be at most 80 characters. Rows may be reordered: the grader aligns IDs. Missing, extra, duplicate, blank or non-string IDs, and missing, extra or reordered columns reject the whole submission with a validation error. A malformed prediction affects only its own row: malformed JSON, nulls, repeated or out-of-range tokens, noninteger tokens, lists longer than eight, and fields longer than 80 characters receive a row score of zero. Other rows are still scored normally. Invalid organizer answers remain errors. For a platform-provided evaluation shard, submit exactly the IDs in that shard. Resources and constraints Train and infer offline using only the prepared public data and standard installed numerical/ML packages. The intended compute is A10G for neural sequence modeling; the supplied reference uses CUDA. No internet calls, runtime package installations, hosted APIs, external datasets, or challenge-specific pretrained checkpoints are allowed. A solution may use the public training/validation folds and then retrain on all labeled writers. Write solution outputs only beneath ./working/. Do not acquire the source corpus to identify hidden continuations, use private answers or organizer files, fingerprint traces against external collections, or exploit case IDs, row order, or writer identifiers as predictive shortcuts. These are evaluation rules, not restrictions on the underlying dataset's CC BY license. No source writer or symbol identification is part of the task. Baseline anchors and score interpretation These scores are measured on the revision 2 test cohort. The sample submission illustrates the file format; it is not a competitive baseline. | Policy | Revision 2 test similarity | |---|---:| | Empty prediction | 0.000000 | | Fixed [5,6,7,8] for every case | 0.253608 | | Training-selected constant [6,7,8] | 0.244968 | | Shipped seeded random three-token sample | 0.152035 | | Random tokens, lengths sampled from training; median of 20 seeds | 0.154506 | | Chronological [1,2,3,4,5,6,7,8] | 0.238636 | The fixed four-token order was identified in the review as chosen using training data. It was frozen before revision 2 test evaluation; this is a useful no-input baseline, not the theoretical minimum or a claim that it is the best possible constant. Its revision 2 labeled-training score is 0.254209. A separate constant selected among the 80 most common training-fold orders is also shown; it was chosen before test scoring and reached 0.262737 on writer validation. The documented random policy scores 0.140131–0.169746 across 20 seeds. Report raw similarity first. For context, a supplementary baseline-adjusted score is (score - b) / (1 - b), with b equal to the fixed-order score on the same evaluated split. This is not the official metric; it may be negative and is not clipped. The local GPU reference scores 0.431036 raw and 0.237715 after adjustment. A fitted constant baseline is not pure random chance. For the original 324-case release only, the fixed order scored 0.219084, the shipped sample 0.168827, and the reviewer reported a random baseline of 0.123. The random policy behind 0.123 was not supplied, so that exact number is reviewer-reported, not independently reproduced. The review's best agent score of 0.46 becomes 0.308504 after adjustment against the original fixed-order baseline; 0.41 becomes 0.244477. These historical numbers do not describe revision 2. Uncertainty Revision 2 expands the held-out cohort from 324 to 627 distinct source traces. Length-two truths fall from 61.73% to 57.42%; the primary change is sample count. There are still only eight held-out writers. More cases reduce individual-row influence, but do not add independent writers or guarantee a reliable ordering of similar models. The original three agent runs have not been rerun on this revised release and must not be compared directly with its scores. Use paired predictions and uncertainty grouped by writer when comparing solutions. &nbsp;
> $700 Pool
> Closes in 11h 42m
> 6 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Recover Ordered Aviation Finding Paths

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77gfbjm8ahvj32ed6rtpgyrx8c7ae5
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat reze's score of 0.412!

Full challenge description from page:

> Latent-Alphabet Hierarchy-Trace Transduction Decode an order-preserving, lossy evidence channel into a report's first-occurrence trace through a two-level aviation finding ontology. Each public input is a sequence of opaque symbols such as h0042; its target is a variable-length sequence of distinct paths such as Personnel issues / Task performance, arranged by their first appearance in the source annotations. Each case couples three latent structures: symbol-to-path evidence correspondence, adaptive sequence termination, and path precedence. Hash collisions make individual symbols ambiguous, deterministic deletion removes part of the evidence stream, and repeated target paths are suppressed after their first occurrence. A solver must therefore aggregate recurring symbol patterns, infer how many hierarchy paths the report requires, and jointly decode their identities and relative order. Use only the bundled public files. Solve-time internet access, external corpora, source lookup, APIs, downloads, package installation, private-file access, and external pretrained models are prohibited. The complete solution must run offline on CPU. Representation Construction The public representation is constructed from each report's cause narrative, while event time is used only to create chronological stages. Raw report identifiers, dates, plaintext words, source links, and hidden sequences are excluded from the prepared public files. For the public evidence channel, the cause narrative is lowercased, digit-bearing tokens are replaced by `, and alphabetic tokens are retained in source order. A deterministic case-specific generator retains each normalized token with probability 0.5; each retained token is then mapped with fixed-key BLAKE2b into one of 4,096 bins rendered as h0000 through h4095. The mapping is deliberately many-to-one, so the model must learn distributional and positional evidence rather than recover plaintext vocabulary. Constructed case_id` values replace raw report identifiers. For the target trace, the report's finding sequence is parsed from left to right. Every finding is reduced to its first two hierarchy levels, and each resulting path is emitted only at its first occurrence. The prepared public files contain labeled traces for training and validation, while test traces remain private. Task Distinction This is not source retrieval, plaintext extraction, or unordered multilabel classification. Solvers receive only a lossy ordered symbol channel and must infer a distinct variable-length hierarchy trace. Path membership, adaptive stopping, and first-occurrence precedence are coupled, and chronological transfer is evaluated at whole-report level. Dataset The public dataset contains: train.csv: 2,923 labeled cases from earlier reports; validation.csv: 513 labeled cases from a later period; test.csv: 324 unlabeled cases from the final period; dataset_summary.json: representation metadata and the 21 allowed path tokens; sample_submission.csv: a valid all-abstention submission. train.csv and validation.csv have these columns: case_id: a constructed identifier that is opaque within the prepared public files; features_json: an ordered JSON list of protected symbols from h0000 through h4095; finding_sequence_json: the ordered JSON list of distinct target paths. test.csv contains only case_id,features_json. Source report IDs, dates, plaintext words, and hidden target sequences are absent from the prepared public files. Target construction reads the source annotation sequence from left to right, reduces every finding to its first two hierarchy levels, and retains only the first occurrence of each path. Predictions must likewise contain distinct allowed paths. Repeating a path is invalid rather than an alternate way to express an insertion. The split is chronological rather than random: training uses earlier reports, validation uses a later period, and test uses the final period. It therefore measures whether learned symbol-to-path, length, and ordering relationships transfer over time. All reports involved in an exact normalized input-narrative duplicate spanning stages are removed, and one row represents one complete report. Related aircraft, operators, investigators, accident families, and recurring narrative templates may still appear in different stages because the source has no authoritative component grouping for those relations. Evaluation For a predicted path sequence P and gold sequence G, let D(P, G) be Levenshtein distance over complete path tokens. Insertion, deletion, and substitution each cost one: case_similarity = clip(1 - D(P, G) / max(len(P), len(G)), 0, 1) score = mean(case_similarity over all test reports) Higher is better. The theoretical range is [0, 1]. An exact sequence scores 1. The exact empty JSON list [] is a valid abstention defined to score 0 for that report, so an all-abstention submission scores 0 overall. Scoring is edit-sensitive over complete path tokens. One wrong path in a three-path sequence creates one substitution and scores 1 - 1/3; omitting one path creates one deletion and receives the same score. A prediction containing the correct paths in a different order incurs the edits needed to recover the published first-occurrence order. A uniformly random ordered length-three prediction sampled without replacement from the 21-token vocabulary has exact expected score 0.060186042524 on this hidden split. For diagnosis only, chance-normalized performance may be reported as (score - 0.060186042524) / (1 - 0.060186042524); the official leaderboard uses raw similarity. The hidden split has 324 report-level evaluation units, so one report contributes at most 0.308642 percentage point to the final score. Related-report structure means small score differences should not be overinterpreted. Inference Strategy A CPU-feasible system can estimate path-emission evidence from ordered symbol n-grams and positional features, calibrate a report-specific stopping rule, learn pairwise or higher-order precedence potentials, and decode a distinct variable-length hierarchy sequence with constrained search. Transition features, length calibration, and beam search provide complementary signals for the coupled emission, termination, and ordering decisions. The chronological split tests whether those mechanisms transfer to later reporting periods. The most common complete training sequence scores 0.255555555556 on test. A separately validated author-side CPU reference decoder scores 0.346788653733; it is not distributed with the challenge. These are local calibration values, not live Agent scores. Submission Write ./working/submission.csv with exactly these columns in this order: case_id,finding_sequence_json Include every test case_id exactly once. finding_sequence_json must be a JSON list containing zero or more distinct strings from the published 21-token vocabulary, in predicted order. Use the exact JSON list [] to abstain. Example format using a format-only placeholder ID: case_id,finding_sequence_json C0000000000000000,"[""Personnel issues / Task performance"",""Aircraft / Aircraft oper/perf/capability""]" Missing or extra rows, duplicate IDs, unexpected columns, malformed or oversized JSON, non-list values, unknown tokens, non-string elements, repeated paths, and sequences longer than 21 tokens invalidate the submission. The grader does not reorder or repair output.
> $700 Pool
> 4 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Learning Organisation Name Translation Without a Dictionary

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72e20t1zsep3j61zqvtnnyw58bma38
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat arvyn's score of 0.585!

Full challenge description from page:

> Cross-Lingual Organization Name Normalization Overview A curated index of research institutions holds, for each one, a single canonical English name, and also records what that institution calls itself in its own language. "Universiteit Antwerpen" and "University of Antwerp" are the same place. So are "Potsdam-Institut für Klimafolgenforschung" and "Potsdam Institute for Climate Impact Research". Given an organization's name in some other language, plus its language code, predict that organization's canonical English name. You have 24,216 paired examples to learn from and 6,116 organizations you have never seen to apply it to. This is a string-to-string transduction problem drawn from real registry data — every pair is a name a person actually curated, not a generated or machine-translated example. It matters in practice: reconciling institution names across languages is what lets publishers, funders and repositories tell whether two records refer to the same place. The split is by organization, not by row. Every name belonging to one institution sits entirely in train or entirely in test, so nothing can be looked up: an organization whose English name you need at test time never had that name shown to you in training. What transfers is the pattern, not the entry. Row order and pair_id carry no information either — both come from a fixed-seed shuffle applied before the split, so an id tells you nothing about which rows share an organization. What makes this hard. Three behaviours share one dataset and telling them apart is most of the work: Translation. Universidad de Chile becomes University of Chile; Laboratorium für Festkörperphysik becomes Laboratory for Solid State Physics. The vocabulary is systematic — universiteit, universite, universidad and universitaet all mean university — but has to be induced from the training pairs alone. Transliteration. 東京大学 becomes The University of Tokyo; 名古屋経済大学 becomes Nagoya Keizai University. A substitution table over Latin word tokens cannot help here, and 104 languages appear in the test split. Preservation. Proper nouns must survive both operations. Potsdam stays Potsdam; Краснодарский becomes Krasnodar, not a translated word. An unseen token is far more likely to be a place or a founder's name than a translatable term, so pushing every token through a substitution table damages the names that were already correct. Because the target is always English and the source never is, copying the source through is close to worthless — it scores 0.054. There is no free credit here: every point has to come from actually mapping one language onto another. Measured on this data with the official grader: ApproachScoreReturn an empty string0.000Copy the source name through unchanged0.054Aligned word substitution table0.222Bag co-occurrence table0.262Keyword cues with per-language priors (reference)0.510 The reference solution reaches 0.510 by combining two signals: a per-language prior for the scaffolding most targets in a language share, and character n-gram cues so the same mechanism works on scripts where whole-word alignment is meaningless. Evaluation Submissions are scored using mean token-level F1 between the submitted name and the canonical English name, averaged over all 6,116 test rows. Both strings are lowercased and split into alphanumeric tokens. Precision is the share of submitted tokens that appear in the target, recall is the share of target tokens that appear in the submission, and the row scores their harmonic mean. Token multiplicity is respected, so repeating a word earns nothing extra. from collections import Counter import re def evaluate(pred, target): p = Counter(re.findall(r"\w+", pred.lower())) t = Counter(re.findall(r"\w+", target.lower())) overlap = sum((p & t).values()) if not overlap: return 0.0 precision = overlap / sum(p.values()) recall = overlap / sum(t.values()) return 2 * precision * recall / (precision + recall) Range: 0.0 to 1.0, higher is better. Partial credit is deliberate — a solver that recovers "University of Antwerp" but misses a qualifier should not score the same as one that returns nothing. Dataset Read from ./dataset/public/. train.csv — 24,216 rows. ColumnTypeDescriptionpair_idstrUnique row identifier, e.g. P004821.source_namestrThe organization's name in another language.langstrISO 639 language code of source_name, e.g. fr, ja, zh.target_namestrTarget. The canonical English name for that organization. test.csv — 6,116 rows. Same columns without target_name. sample_submission.csv — 6,116 rows in the required format, filled by copying source_name through. It scores 0.054. Sources span Latin, Cyrillic, CJK, Devanagari, Arabic, Thai, Greek and Hebrew scripts, so character-level processing must be Unicode-aware. All files are UTF-8. Submission Write a CSV named submission.csv to ./working/ with the following format: ColumnTypeDescriptionpair_idstrRow identifier from test.csvtarget_namestrYour predicted English name, as plain text pair_id,target_name P000004,University of Antwerp P000011,Potsdam Institute for Climate Impact Research ... Requirements: Must contain exactly 6,116 rows (one per test sample), plus a header. Any order is accepted. A pair_id you omit scores 0 for that row rather than voiding the submission; duplicated ids keep their first row and unknown ids are ignored. Only an unreadable file, or one missing the pair_id or target_name column, is unscorable. Rules Learn from the provided data only. No pretrained models, no LLMs, no translation APIs, and no external data of any kind. Use only libraries available in the Kaggle Python Docker image (pandas, numpy, scikit-learn, xgboost, lightgbm, tensorflow, pytorch and similar). No LLM-generated outputs may be used anywhere in your solution. Your notebook must run end to end, top to bottom: read from ./dataset/public/, learn the mapping, then write ./working/submission.csv. Seed everything; your run should be reproducible. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Ephemeral Dialogue Register Machine Induction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7aqkcb1dmqb1k83xan4ewswn8dttvd
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat rajat20056's score of 66.598!

Full challenge description from page:

> Overview Ephemeral Dialogue Register Machine Induction is an episodic structured-language challenge in which every record defines a new temporary reasoning machine. Each episode introduces six opaque operators, O01 through O06. An operator is a hidden three-register program over a dialogue’s latent commonsense state. Its meaning is local to that episode: the program assigned to O04 in one row is unrelated to the program assigned to O04 in another. The episode provides three demonstrations for each operator. From those demonstrations, a model must recover: which three latent semantic registers the operator uses; the order in which those registers are executed; which probe position is an intrusion rather than a program input; how the operator’s trace order changes under a binary control value. The model must then execute the recovered machine on six new dialogues. For every query, it predicts the applicable temporary operator, three ordered register-bank slots, and the rejected probe position. The six queries form a coupled assignment: every temporary operator is used exactly once. This is not ordinary answer selection. Every register-bank statement belongs to the query dialogue, and the bank contains one statement from every latent semantic dimension. Dialogue relevance therefore does not isolate the answer. A successful system must distinguish the hidden semantic roles of statements, reconstruct an episode-specific program, apply its control-dependent orientation, and decode the complete operator assignment. The Latent Dialogue State Each dialogue is associated with ten recurring but unnamed semantic dimensions. Together they form a latent dialogue state with ten registers. The challenge never publishes the original dimension names. Registers are represented only through natural-language statements observed for a dialogue. A statement might describe an internal state, an unstated condition, an expected consequence, a participant’s intention, or another aspect of conversational commonsense, but those roles are not supplied as labels. A hidden operator selects three distinct registers in an ordered program: r_a → r_b → r_c Order matters. The programs r_a → r_b → r_c, r_c → r_b → r_a, and r_a → r_c → r_b are different. The space contains 720 possible ordered three-register programs before episode-level selection. Temporary Operators Every episode selects six distinct programs and assigns them to O01 through O06 using a fresh hidden codebook. There is no global operator dictionary. Across different episodes: the same program can receive different operator codes; the same operator code can denote different programs; the program’s control permutation can change; the set of competing programs can have a different overlap structure. Each operator is demonstrated three times on separate dialogues. A demonstration contains: a binary control value, C0 or C1; a complete multi-turn dialogue; four shuffled probe statements, P01 through P04; a three-step executed trace; the probe position rejected by the operator. Exactly three probe statements instantiate the program’s three semantic registers. The fourth statement is an intrusion from another register. Probe order is independently shuffled and does not reveal execution order. The demonstrations include both control values. C0 executes the operator’s base order. C1 applies an episode-local non-identity permutation of its three registers. The alternative trace can therefore be a swap, a cyclic rotation, or a full reversal. The control permutation is itself episode-local. It must be inferred from the demonstrations rather than assumed from the operator code. Query Execution Each episode contains six query fields, query_Q01 through query_Q06. A query contains: a control value; a new multi-turn dialogue; four shuffled probe statements; a ten-slot register bank, S01 through S10. The observed probe identifies the unordered semantic footprint of the applicable program, together with one intrusion. The register bank supplies a different observed statement for each of the dialogue’s ten latent registers. The model must return five values: the temporary operator that matches the three valid probe registers; the register-bank slot executed at step 1; the register-bank slot executed at step 2; the register-bank slot executed at step 3; the probe slot that must be rejected. The three predicted register slots must be distinct. The probe statements and register-bank statements use different observed answer variants. Exact phrase matching between the probe and bank is therefore unavailable. All ten register-bank entries remain grounded in the same query dialogue, so generic dialogue–candidate relevance is also insufficient. Why the Outputs Are Coupled The five outputs for a query describe one executable object. An operator prediction can be correct while its trace is wrong because the control-dependent permutation was applied incorrectly. A trace can contain the correct three semantic registers but still place them in the wrong order. A model can identify the intrusion but still select the wrong operator when several local programs share two registers. Episode-level competition adds another dependency. O01 through O06 must each be used once. In dense episodes, multiple operators may: share the same three registers in different orders; share a two-register prefix; be forward/reverse counterparts; use another operator’s register as the intrusion; agree under one control value but diverge under the other. A locally plausible choice may therefore make the remaining operator assignment inconsistent. Illustrative Miniature Consider a reduced episode with two operators. The demonstrations for O01 show a program involving three latent roles: an unstated condition, a participant’s internal state, and a likely consequence. Under C0, traces appear in that order. Under C1, the local controller rotates the consequence to the first step. The demonstrations for O02 use the same three roles but execute the internal state first and follow a different control orientation. A query supplies four shuffled probe statements: three instantiate the shared roles and one expresses a participant’s later intention. Its register bank contains ten dialogue-grounded statements, one for every latent role. The model must determine whether the probe corresponds to O01 or O02, reject the intention statement, locate the three alternate statements in the register bank, and order their slot codes according to the query’s control value. The full challenge expands this interface to six operators, eighteen demonstrations, six queries, ten registers per query, and thirty scored decisions per episode. Public Dataset Files The release contains: train.csv test.csv sample_submission.csv Training and test data use the same public feature layout. Training rows additionally contain the thirty target columns. Episode Columns Every row begins with: sample_id: a unique episode identifier; machine_density: a difficulty band from D1 through D4. The identifier contains no source coordinate, semantic label, split marker, or reusable operator information. The six support columns are: support_O01 support_O02 support_O03 support_O04 support_O05 support_O06 Each support field contains three demonstrations defining that episode’s temporary operator. The six query columns are: query_Q01 query_Q02 query_Q03 query_Q04 query_Q05 query_Q06 Each query field contains its control, dialogue, four-position probe, and ten-slot register bank. Training Targets For every query Qxx, training data provides: query_Qxx_operator query_Qxx_step1 query_Qxx_step2 query_Qxx_step3 query_Qxx_reject Operator targets use O01 through O06. Trace targets use S01 through S10. Intrusion targets use P01 through P04. Within each training row: operator labels form a complete permutation of O01 through O06; the three trace slots for a query are distinct; all target codes refer only to content inside that row; no original semantic-dimension name appears as a target. Test Generalization Test dialogues are disjoint from training dialogues. Test episodes also use ordered three-register programs withheld from scored training episodes. The individual semantic registers remain observable through other training programs, but the held-out ordered compositions are new. Because every test episode supplies its own operator demonstrations, the withheld programs remain solvable. A system must infer the temporary machine from the current support set and compose familiar semantic roles in a new order. This split tests two forms of generalization simultaneously: semantic transfer to unseen dialogues; compositional transfer to unseen ordered programs. Submission Format A submission contains exactly 31 columns: sample_id followed by five prediction columns for each of the six queries. The required order is: sample_id, query_Q01_operator,query_Q01_step1,query_Q01_step2,query_Q01_step3,query_Q01_reject, query_Q02_operator,query_Q02_step1,query_Q02_step2,query_Q02_step3,query_Q02_reject, query_Q03_operator,query_Q03_step1,query_Q03_step2,query_Q03_step3,query_Q03_reject, query_Q04_operator,query_Q04_step1,query_Q04_step2,query_Q04_step3,query_Q04_reject, query_Q05_operator,query_Q05_step1,query_Q05_step2,query_Q05_step3,query_Q05_reject, query_Q06_operator,query_Q06_step1,query_Q06_step2,query_Q06_step3,query_Q06_reject For every episode: O01 through O06 must each be predicted exactly once; each query must use three distinct register slots; all required identifiers must occur exactly once; additional columns are not permitted. Blank values, malformed codes, duplicate identifiers, missing rows, unexpected rows, repeated operator codes, repeated trace slots within a query, or incorrect column order produce an explicit grading error. Small Submission Example The following is a complete, structurally valid one-row submission example: sample_id,query_Q01_operator,query_Q01_step1,query_Q01_step2,query_Q01_step3,query_Q01_reject,query_Q02_operator,query_Q02_step1,query_Q02_step2,query_Q02_step3,query_Q02_reject,query_Q03_operator,query_Q03_step1,query_Q03_step2,query_Q03_step3,query_Q03_reject,query_Q04_operator,query_Q04_step1,query_Q04_step2,query_Q04_step3,query_Q04_reject,query_Q05_operator,query_Q05_step1,query_Q05_step2,query_Q05_step3,query_Q05_reject,query_Q06_operator,query_Q06_step1,query_Q06_step2,query_Q06_step3,query_Q06_reject EDRMI-EXAMPLE000000001,O03,S07,S02,S09,P04,O06,S01,S10,S04,P02,O01,S05,S03,S08,P01,O05,S09,S06,S02,P03,O02,S04,S08,S01,P02,O04,S10,S07,S05,P04 This row illustrates formatting only and is not a disclosed test answer. In an actual submission, EDRMI-EXAMPLE000000001 must be replaced by a sample_id from test.csv, and every test identifier must appear exactly once. The example uses all six operator codes exactly once, uses three distinct register slots within every query, and uses one valid probe code for every rejection. Evaluation The evaluator measures five levels of recovery. Let: A be operator accuracy; I be intrusion-rejection accuracy; T be individual trace-step accuracy; R be complete three-step trace accuracy; Q be exact query accuracy, requiring the operator, all three ordered steps, and the rejection to be correct; E be exact episode accuracy, requiring all six queries to be exactly correct. The balanced component is: $$ B = (A I T)^{1/3} $$ The executable-recovery component is: $$ X = 0.70Q + 0.20R + 0.10E $$ The leaderboard score is: $$ 100 \times B^{0.35} \times X^{0.65} $$ The exponents reflect the challenge’s intended hierarchy of competence. The balanced component B receives weight 0.35 because operator identification, intrusion detection, and individual register recovery are necessary diagnostic foundations, but they do not establish that the inferred machine was executed correctly. The executable-recovery component X receives the larger weight 0.65 because the primary objective is complete program application: selecting the correct temporary operator, applying its control-dependent permutation, producing the ordered three-step trace, and rejecting the intrusion jointly. The multiplicative form prevents strong execution credit from compensating for broadly unreliable register recovery, while the heavier exponent on X ensures that systems assembling complete executable traces outrank systems that accumulate isolated component matches. The returned value is clipped to the closed interval [0.01, 100]. A perfect submission receives exactly 100.0. Partial step credit helps distinguish systems that recover some semantic registers from systems that fail completely. Exact-query credit dominates the score because an unordered register set is not a successfully executed program. Exact-episode credit rewards complete temporary-machine reconstruction and globally consistent operator assignment. Evaluation is deterministic and uses exact categorical matches. It does not use a language model, embedding service, external API, manual review, or semantic judge. Difficulty Bands machine_density describes structural competition among the six local programs. D1: programs have relatively low register overlap. D2: several programs share one register and create moderate signature competition. D3: programs frequently share two registers or a partial ordered prefix. D4: multiple programs operate on the same register sets in different orders, with dense forward/reverse and intrusion collisions. Difficulty is determined from hidden program topology rather than surface-word overlap. Expected Modeling Approaches A competitive system will likely need separate but jointly trained capabilities: infer latent semantic-register representations from the support demonstrations; induce a three-register program and control permutation for every temporary operator; identify the three valid probe roles and the intrusion in each query; align query register-bank statements to latent roles; execute the selected program under the query control; solve the six-query operator permutation jointly. Relevant model families include: episode-conditioned cross-encoders; hierarchical transformers over dialogue, probe, and register-bank structure; set-to-sequence architectures; meta-learning systems with temporary program representations; latent-variable models for semantic register discovery; The permutation decoder alone cannot solve the task. It can enforce validity only after a learned model supplies meaningful semantic and program-compatibility scores. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The maximum end-to-end runtime is 1.5 hours, including data loading, training or adaptation, inference, structured decoding, validation, and submission writing.
> $700 Pool
> Closes in 5h 45m
> 11 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## POLICY BLACKOUT: Climate Accountability Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77e32h3ntv75yy8s3wxkmj6x8dx4ry
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat preetam335's score of 0.675!

Full challenge description from page:

> POLICY BLACKOUT: Climate Accountability Reconstruction Overview Reconstruct the semantic roles of erased passages in real EU climate and energy legislation. Each packet contains a legislative excerpt with one or more numbered gaps. Predict an ordered sequence of role codes: who implements or monitors a rule, what a deadline governs, or how another legal instrument is referenced. This is structured NLP prediction, with variable-length responses, rather than tabular prediction or regression. Target names, dates, citations, and source identifiers are unavailable. Optional evidence contains other uses of the same normalized source surface within the same article. The surface is replaced by TRACE]. Identical wording does not guarantee coreference or the same semantic role: each answer concerns its numbered gap's local context. Evaluation The score is weighted family accuracy plus exact packet accuracy: score = 0.75 × (0.65 × Actor_accuracy + 0.20 × Time_accuracy + 0.15 × Reference_accuracy) + 0.25 × packet_exact_accuracy. Family accuracy pools all gaps of that family. Packet accuracy requires every code in the packet to be correct. All terms lie in [0,1]; the weights sum to one. A malformed prediction packet receives zero credit for every gap in that packet and for its exact-packet term. The following helper reproduces scoring after structural validation and alignment by id. y_true contains trusted dictionaries with decoded kinds and prediction lists; y_pred contains predicted lists or JSON strings. Before calling it, enforce the submission schema and exact unique ID set described below. It is intended for held-out public-training validation, whose answer rows must cover all three families. import json, math, numbers, re from decimal import Decimal, InvalidOperation SIZES = {"Actor": 8, "Time": 5, "Reference": 3} OFFSETS = {"Actor": 0, "Time": 8, "Reference": 13} WEIGHTS = {"Actor": .65, "Time": .20, "Reference": .15} NUMERIC = re.compile( r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE?[0-9]+)?\Z" ) def packet(value, kinds): if isinstance(value, str): if (len(value) > 2048 or value.count("[") != 1 or value.count("]") != 1 or "{" in value or "}" in value): return None try: value = json.loads(value) except (ValueError, RecursionError): return None if not isinstance(value, list) or not 1 32 or not NUMERIC.fullmatch(text): return None try: d = Decimal(text) except InvalidOperation: return None if not d.is_finite() or d != d.to_integral_value(): return None if not OFFSETS[kind] <= d < OFFSETS[kind] + SIZES[kind]: return None n = int(d) if not OFFSETS[kind] <= n < OFFSETS[kind] + SIZES[kind]: return None result.append(n) return result def evaluate(y_true, y_pred): if not y_true or len(y_true) != len(y_pred): raise ValueError("Aligned, nonempty packet collections are required.") totals = dict.fromkeys(SIZES, 0) correct = dict.fromkeys(SIZES, 0) exact = 0 for truth, submitted in zip(y_true, y_pred): kinds, labels = truth["kinds"], truth["prediction"] predicted = packet(submitted, kinds) exact += int(predicted is not None and predicted == labels) for i, kind in enumerate(kinds): totals[kind] += 1 correct[kind] += int(predicted is not None and predicted[i] == labels[i]) if any(totals[k] == 0 for k in SIZES): raise ValueError("Validation must cover every annotation family.") score = .75 * sum(WEIGHTS[k] * correct[k] / totals[k] for k in SIZES) score += .25 * exact / len(y_true) if not math.isfinite(score): raise ValueError("Invalid evaluation inputs.") return float(min(1., max(0., score))) Dataset Read the four supplied files in ./dataset/public/: train.csv: 2,495 packets; columns id,group,text,kinds,evidence,prediction. test.csv: 755 packets; columns id,group,text,kinds,evidence. sample_submission.csv: columns id,prediction, with correctly sized placeholder lists. label_schema.json: explicit global-code-to-label mappings for each annotation family; JSON object keys are numeric strings. id is an opaque randomized string; preserve it exactly. group is an opaque article/revision-component identifier, provided for validation grouping only; do not use it as a predictive feature. text contains [GAP_0] through [GAP_n], [CONTEXT_GAP] for other erased passages, and [NUMBER] for redacted numbers. Gap numbers are randomized independently of source order. kinds is present on every training and test row. It is a JSON list of unscored annotation-family names. Its entry i identifies the label space for [GAP_i]. evidence is a parallel JSON list: entry i contains zero to three redacted witness strings for that gap. Witnesses stay within the same source article and outside the target core. prediction is a JSON list in that same gap-number order, in training and submissions alike. Codes are globally unique integers, explicitly mapped in label_schema.json. Actor uses 0–7, Time uses 8–12, and Reference uses 13–15: Actor: 0 Addressee_default, 1 Addressee_sector, 2 Authority_default, 3 Authority_monitoring, 4 Addressee_monitored, 5 Authority_legislative, 6 Addressee_resource, 7 Authority_established. Time: 8 Time_Compliance, 9 Time_Monitoring, 10 Time_InEffect, 11 Time_PolDuration, 12 Time_Resources. Reference: 13 Ref_OtherPolicy, 14 Ref_PolicyAmended, 15 Ref_Strategy_Agreement. The 3,250 distinct packets contain 6,554 scored gaps: 5,092 training and 1,462 test gaps. Construction uses non-overlapping target cores of up to 32 words, retaining final short cores only when they contain at least 16 words, with up to 48 source words of surrounding context on each side. Adjacent packets may share context, so packets are not independent documents. Training represents 293 articles in 258 components; test represents 84 articles in 81 components. Both articles and represented components are disjoint across the split. Related article revisions and near-duplicate articles are grouped together. Laws intentionally overlap: evaluation concerns unseen article components within known legal domains, not unseen legislation or time-series forecasting. Preserve component disjointness when making validation splits. Submission Write ./working/submission.csv with exactly id,prediction and one row for every test ID. The private answer CSV has the same two columns and the same list encoding. It contains no kinds column: the grader derives each family from its globally unique trusted answer code. CSV row order is irrelevant because grading joins by ID. The following real-ID examples illustrate formatting only; codes are family-valid placeholders, not answers: id,prediction fb04fd2a7efdbedab79a400e45d1eef8,[0] 80dd242bd72f36da8efd8545e5bb1769,"[0,0,0]" Requirements Submit exactly 755 unique IDs, with no missing, duplicate, or foreign IDs. Missing, extra, renamed, or duplicate columns and ID-set errors cause a clean ValueError; error messages do not reveal hidden answers. Each list must have the required length, between one and eight, and each element must be an integer within its family's range. Finite, integer-valued numeric strings or floats are accepted, but integer JSON codes are recommended. NaN, infinity, null, booleans, fractional/out-of-range values, malformed JSON, nested lists, or incorrect lengths invalidate the entire packet. Predictions longer than 2,048 characters are invalid. The total solution limit is 90 minutes, including training, inference, and submission writing. Train from scratch using supplied training data only. The notebook reads ./dataset/public/ and writes ./working/submission.csv. What not to use Do not use external data, pretrained weights, runtime downloads, source-document retrieval, test-set fitting. Do not infer labels from IDs or group identifiers. The participant harness must expose only the prepared public data and enforce access/resource rules; the score function alone cannot enforce them. Extra Modeling Information In this challenge the annotated source spans are erased, responses are variable-length role sequences, and optional anonymized same-surface witnesses must be interpreted without assuming shared roles. Joint packet credit tests consistency across several gaps. Goal being reconstruction of setup while acknowledging that the source corpus and role taxonomy are established research artifacts.
> $700 Pool
> 4 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Acoustic Palimpsest: Spoken Question Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx798q1v25633xdfzgmpgdff0s8b3ym2
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview Acoustic Palimpsest is a structured audio-language reasoning challenge about reconstructing spoken Mandarin questions from shuffled audio fragments. Every case contains fifteen audio candidates, six written answer candidates, and three hidden target questions. Each target question has been divided into four contiguous fragments. Twelve audio candidates therefore belong to the three target questions. The remaining three candidates are authentic orphan fragments taken from other utterances. The model must emit: Three ordered chains containing four audio candidate IDs each. One written-answer candidate ID for each chain. A confidence probability for the complete structure. A confidence probability for the complete answer graph. A confidence probability for the entire case. The three predicted chains must use twelve distinct audio candidates. The three unused candidates are interpreted as the predicted orphan set. The three hidden questions do not have permanent public identities. The evaluator treats the submitted chains as an unordered set. A correct chain may be placed in chain_0, chain_1, or chain_2, provided that its attached answer moves with it. This is not a transcription task. Participants do not submit question transcripts. It is also not ordinary question answering. No complete question is provided. A successful system must jointly recover fragment membership, temporal order, orphan status, and question-to-answer relationships. Core Prediction Problem Every case contains: Fifteen shuffled audio candidates. Three hidden target questions. Four fragments per target question. Twelve target fragments in total. Three orphan fragments. Six written answer candidates. Three correct answers. Three answer distractors. A hidden case can be understood conceptually as: Question A: a0 -> a1 -> a2 -> a3 -> answer_x Question B: b0 -> b1 -> b2 -> b3 -> answer_y Question C: c0 -> c1 -> c2 -> c3 -> answer_z Orphans: o0, o1, and o2 The labels A, B, and C are explanatory only. They do not correspond to the public chain suffixes. A valid prediction for one case must contain: Exactly three chains. Exactly four candidate IDs in every chain. Twelve distinct audio candidate IDs across the three chains. Exactly three distinct answer candidate IDs. One answer attached to each chain. Three finite confidence values between zero and one. What the Model Must Learn The model must determine: Which fragments belong to the same spoken question. Which three fragments are orphans. The correct order of the four fragments in each question. Which written answer belongs to each reconstructed question. How likely the complete structural prediction is to be exact. How likely the complete answer graph is to be exact. How likely the entire case is to be exact. The central difficulty is global consistency. A locally plausible fragment transition may be wrong if using it prevents the remaining candidates from forming two coherent questions. Two orphan fragments may form a convincing short sequence. A correct answer may also be assigned to the wrong reconstructed question. Chains should therefore be decoded jointly rather than independently. Audio Preparation All released fragments use a consistent participant-facing format: Mono audio. 16,000 Hz sample rate. FLAC encoding. Signed 16-bit PCM after decoding. Standardized amplitude limits. Reduced excessive leading and trailing silence. Invalid, damaged, extremely short, or otherwise unsuitable recordings are excluded during preparation. Every target question is split into four contiguous regions: position_0 position_1 position_2 position_3 position_0 contains the beginning of the question. position_3 contains its ending. Fragment boundaries are placed near lower-energy locations when possible, but they are not guaranteed to align with word or phrase boundaries. A boundary can occur between syllables, during coarticulation, near a grammatical particle, between a number and its unit, or immediately before or after a short pause. Small boundary fades and fragment-level amplitude normalization may be applied. Original timestamps, waveform offsets, and complete source recordings are not released. Useful reconstruction evidence may include: Prosodic continuation. Partial-syllable compatibility. Spectral continuity. Speaking rhythm. Breathing patterns. Phrase structure. Mandarin grammar. Interrogative structure. Semantic continuation. Sentence-final intonation. Orphan Fragments Every case contains exactly three orphan fragments. Orphans are authentic speech fragments that do not belong to any of the three target questions in the current case. They are not synthetic noise, reversed speech, silence-only files, or environmental sounds. Orphans are selected to create plausible alternatives. They may resemble target fragments in speaker characteristics, channel conditions, duration, loudness, speaking rate, topic, answer type, or local acoustic continuity. An orphan may look compatible with the beginning or ending of a true chain. This is intentional. Participants do not submit an orphan column. The evaluator calculates the predicted orphan set as all candidate IDs from 0 through 14 minus the twelve IDs used by the submitted chains. Answer Candidates Every case contains exactly six written answer candidates. Exactly three are correct, with one correct answer for each target question. The remaining three are distractors. The answer relationship is one-to-one. A submitted answer candidate may not be reused across chains. Distractors are selected to remain plausible. Answer candidates may share a broad type such as person, place, historical period, year, number, institution, scientific term, cultural concept, title, or short factual phrase. The evaluator scores both answer selection and answer attachment. Selecting the correct unordered answer set is not sufficient if those answers are connected to the wrong reconstructed questions. Released Files The public package contains: audio/ train.csv test.csv sample_submission.csv There are no separate case-packet files. Candidate descriptions are stored directly in JSON-formatted CSV columns. Audio waveforms are stored under audio/. Participants should resolve each audio_file path relative to the public challenge directory. Audio Candidate JSON The audio_candidates_json column contains a JSON array of exactly fifteen objects. Each object contains: candidate_id: an integer from 0 through 14. audio_file: the relative path to the corresponding FLAC fragment. A typical object is: {"candidate_id":0,"audio_file":"audio/palimpsest_example_00.flac"} Every candidate ID appears exactly once within a case. Array position does not reveal question membership, temporal position, or orphan status. Answer Candidate JSON The answer_candidates_json column contains a JSON array of exactly six objects. Each object contains: answer_id: an integer from 0 through 5. text: the written answer candidate. A typical object is: {"answer_id":0,"text":"少林寺"} Every answer ID appears exactly once within a case. Candidate order does not reveal correctness or question-to-answer matching. Training Data train.csv contains one labeled case per row. Its columns are: sample_id audio_candidates_json answer_candidates_json chain_0 chain_1 chain_2 answer_0 answer_1 answer_2 sample_id is an opaque string used only to align rows. It must not be used as a predictive feature. Each chain column is a JSON array of four candidate IDs ordered from earliest to latest. A value such as 7,2,10,0] means that candidate 7 begins the question and candidate 0 ends it. Across the three gold chains, all twelve candidate IDs are distinct. Exactly three candidate IDs remain unused. For consistent storage in train.csv, the three gold chains are sorted by the candidate ID in their first position. This is only a storage convention. Evaluation is permutation-invariant. Each answer_i value is the answer attached to chain_i. Answer IDs are integers from 0 through 5. The three gold answer IDs are distinct. Test Data test.csv contains: sample_id audio_candidates_json answer_candidates_json All target chains, answer links, orphan labels, and exactness targets are hidden. Dataset Scale The release contains: 4,000 training cases. 1,200 test cases. 60,000 training audio fragments. 18,000 test audio fragments. 78,000 released audio fragments in total. Every case remains compact, but the full test partition contains 18,000 audio fragments. Submission Format Use sample_submission.csv as the submission template. The submission must contain these ten columns: sample_id chain_0 chain_1 chain_2 answer_0 answer_1 answer_2 p_structure p_answers p_case The grader accepts these columns in any input order, but using the exact template order is strongly recommended. Reproducing the Grader Locally A typical workflow is: import pandas as pd from grader import grade train = [pd.read_csv("train.csv") Example only: use your preferred case-level validation split. validation = train.sample(frac=0.2, random_state=42).copy() answers = validation [ "sample_id", "chain_0", "chain_1", "chain_2", "answer_0", "answer_1", "answer_2", ] ].copy() submission = [pd.read_csv("validation_submission.csv") score = grade(submission, answers) print(score) validation_submission.csv must use the same ten-column schema as the competition submission: sample_id chain_0 chain_1 chain_2 answer_0 answer_1 answer_2 p_structure p_answers p_case The answers DataFrame needs the labeled columns: sample_id chain_0 chain_1 chain_2 answer_0 answer_1 answer_2 The easiest way to obtain these labels is directly from the held-out rows of train.csv. Submission chain cells must be valid JSON strings such as: 7,2,10,0] The labeled chain values read from train.csv can be passed directly to the grader. For example, a complete local evaluation can be constructed entirely in memory: import json import pandas as pd from grader import grade train = [pd.read_csv("train.csv") validation = train.iloc:100].copy() answers = validation[ [ "sample_id", "chain_0", "chain_1", "chain_2", "answer_0", "answer_1", "answer_2", ] ].copy() submission = pd.DataFrame( { "sample_id": validation["sample_id"], "chain_0": [ json.dumps([0, 1, 2, 3], separators=(",", ":")) for _ in range(len(validation)) ], "chain_1": [ json.dumps([4, 5, 6, 7], separators=(",", ":")) for _ in range(len(validation)) ], "chain_2": [ json.dumps([8, 9, 10, 11], separators=(",", ":")) for _ in range(len(validation)) ], "answer_0": 0, "answer_1": 1, "answer_2": 2, "p_structure": 0.1, "p_answers": 0.1, "p_case": 0.05, } ) score = grade(submission, answers) print(score) The example predictions above are arbitrary and are intended only to demonstrate the grader interface. For realistic validation, replace them with predictions from your model. Local Grader Behavior The local grader uses the same published metric described in the Evaluation section. It performs permutation-invariant matching between the three submitted chains and the three labeled chains before evaluating temporal order and attached answers. The grader also checks submission validity. Malformed prediction data generally gives zero credit to the affected expected case rather than discarding otherwise valid cases. Examples of row-level errors include: Missing expected sample_id. Duplicate expected sample_id. Invalid JSON in a chain column. A chain containing something other than four integers. Candidate IDs outside 0 through 14. Repeated candidate IDs. Failure to use exactly twelve distinct candidates across the three chains. Answer IDs outside 0 through 5. Repeated answer IDs. Missing confidence values. NaN or infinite confidence values. Confidence values outside zero through one. When malformed cases are encountered, the grader may print a small number of example errors before returning the score. Unknown sample_id values that do not occur in the supplied labeled answers table are ignored and may be reported. Some problems cannot be interpreted at the row level and instead cause the grader to raise an error. These include invalid submission schemas such as missing columns, additional columns, or duplicated column names. Participants should therefore run the grader on the exact file they intend to evaluate: submission = [pd.read_csv("validation_submission.csv") score = grade(submission, answers) This is preferable to grading only an in-memory object before serialization because CSV serialization can change chain representations or data types. Checking a Perfect Local Submission A useful sanity test is to convert labeled validation rows into submission format and assign confidence 1.0 to all three exactness predictions. import pandas as pd from grader import grade train = pd.read_csv("train.csv") validation = train.iloc:100].copy() answers = validation[ [ "sample_id", "chain_0", "chain_1", "chain_2", "answer_0", "answer_1", "answer_2", ] ].copy() gold_submission = validation[ [ "sample_id", "chain_0", "chain_1", "chain_2", "answer_0", "answer_1", "answer_2", ] ].copy() gold_submission["p_structure"] = 1.0 gold_submission["p_answers"] = 1.0 gold_submission["p_case"] = 1.0 score = grade(gold_submission, answers) print(score) This should return: 100.0 If it does not, check that the submission columns and chain serialization have not been modified. Recommended Validation Workflow For model development: Split train.csv into training and validation cases. Keep every complete case on only one side of the split. Train the model without using the validation labels. Generate predictions for the validation cases. Write those predictions using the competition submission schema. Reload the prediction CSV with pandas. Select the seven label columns from the corresponding validation rows. Call grade(submission, answers). Use the returned score to compare modeling approaches. For example: LABEL_COLUMNS = [ "sample_id", "chain_0", "chain_1", "chain_2", "answer_0", "answer_1", "answer_2", ] validation_answers = validation[LABEL_COLUMNS].copy() validation_submission = [pd.read_csv("validation_submission.csv") score = grade(validation_submission, validation_answers) print(f"Validation score: {score:.6f}") The same grader can therefore be used both for submission-format testing and for genuine local model evaluation on held-out training cases. Chain Predictions Every chain cell must be a valid JSON string representing an array of exactly four distinct integers. The accepted form is: [7,2,10,0] Forms such as (7,2,10,0), [7 2 10 0], and array([7,2,10,0]) are invalid because they are not JSON arrays. Across chain_0, chain_1, and chain_2: Exactly twelve distinct candidate IDs must be used. Every candidate ID must lie from 0 through 14. A candidate may not appear in more than one chain. Exactly three candidates must remain unused. Whitespace inside a valid JSON array does not matter. [7,2,10,0] and [7, 2, 10, 0] are equivalent. Answer Predictions answer_0 is attached to chain_0, answer_1 is attached to chain_1, and answer_2 is attached to chain_2. Every answer must be an integer from 0 through 5. The three submitted answer IDs must be distinct. Confidence Predictions p_structure estimates the probability that the complete audio structure is exact, including all three groups, all twelve temporal positions, and the complete orphan set. p_answers estimates the probability that all three question-to-answer edges are exact after permutation-invariant structural matching. p_case estimates the probability that both the complete structure and complete answer graph are exact. All three probabilities must be numeric, finite, and between zero and one. Complete Row Example A valid row can use: sample_id = palimpsest_example001 chain_0 = [7,2,10,0] chain_1 = [4,11,6,1] chain_2 = [12,9,3,14] answer_0 = 2 answer_1 = 5 answer_2 = 0 p_structure = 0.18 p_answers = 0.31 p_case = 0.08 Because chain cells contain commas, normal CSV writers will quote those cells automatically. Participants should use a CSV library instead of assembling rows by string concatenation. Safe Submission Construction A recommended workflow is: Load test.csv and sample_submission.csv with pandas. Preserve every test sample_id exactly. Serialize each chain with json.dumps([int(x) for x in chain], separators=(",", ":")). Convert NumPy integers to ordinary Python integers before serialization. Confirm that the three chains use twelve distinct candidate IDs. Confirm that the three answer IDs are distinct. Clip each confidence to the interval from zero to one. Save with submission.to_csv("submission.csv", index=False, encoding="utf-8"). Reload the written file with pd.read_csv("submission.csv"). Run the provided local submission checker on the reloaded file. The final reload is important. An in-memory list can look correct but be written in a representation that is not valid JSON. If a prediction pipeline fails for one case, keep that sample_id in the submission and write a syntactically valid fallback row based on the sample submission. This preserves credit for every case the model solved successfully. Row-Level Validation Policy Malformed prediction data invalidates only the affected expected case whenever the grader can still identify and interpret the rest of the submission. An expected case receives zero credit for all metric components when: Its sample_id is missing from the submission. Its sample_id appears more than once. Any chain is missing or is not valid JSON. Any chain does not contain exactly four integers. A chain contains an out-of-range or repeated candidate. The three chains do not use exactly twelve distinct candidates. Any answer is missing, non-integral, or outside 0 through 5. The three answer IDs are not distinct. Any confidence is missing, non-numeric, NaN, infinite, or outside zero through one. Valid cases continue to receive their normal scores. One malformed row does not erase credit earned by other rows. Unknown sample IDs are ignored. Blank submission rows do not replace any required expected case. Some failures remain submission-wide because row-level interpretation is impossible. The entire submission receives zero when: A required column is missing. An unknown extra column is present. A column name is duplicated. The submitted table cannot be interpreted as the expected submission format. The evaluator encounters an unrecoverable internal error. Participants should still use sample_submission.csv exactly. Row tolerance is a safeguard against isolated prediction failures, not an alternative submission format. Permutation-Invariant Structural Matching Let the submitted chains be P0, P1, and P2, and let the gold chains be G0, G1, and G2. For every predicted-gold pair, the evaluator calculates fragment-set overlap and pairwise temporal agreement. chain_overlap(P,G) equals the number of shared fragment IDs divided by four. Each gold chain contains six ordered fragment pairs. A pair receives temporal credit when both fragments appear in the predicted chain and their relative order matches the gold order. chain_pairwise_order(P,G) equals correctly ordered gold pairs divided by six. Pair compatibility is: 0.55 × chain_overlap + 0.45 × chain_pairwise_order The evaluator checks all six one-to-one assignments between predicted and gold chains and selects the assignment with the largest total compatibility. Before resolving an exact tie, both predicted and gold chain objects are sorted canonically by their chain tuples. The first lexicographic assignment in that canonical order is selected. This makes tie resolution independent of the public chain suffixes. Answers do not influence this matching decision. After structural matching, the answer attached to each submitted chain is compared with the answer belonging to its matched gold chain. Evaluation The competition metric is the Palimpsest Graph Reconstruction Score. The final score is: 100 × (0.30 × partition_utility + 0.30 × temporal_utility + 0.25 × answer_graph_utility + 0.15 × confidence_utility) The result is clipped to the interval from 0 through 100. Higher is better. A perfect submission receives exactly 100. There are no hidden metric components. Latent Partition Utility This component evaluates whether the fifteen candidates were divided into three correct four-fragment groups and one correct three-fragment orphan set. Mean chain overlap averages chain_overlap across the three structurally matched chain pairs and then across cases. Co-membership F1 compares same-question relations among the twelve gold target fragments. A fragment pair is predicted as same-question only when both fragments occur in the same submitted chain. Orphan overlap is the number of correctly unused candidates divided by three. Exact orphan accuracy is one only when the complete predicted orphan set equals the gold orphan set. Exact partition accuracy is one only when all three matched fragment sets and the orphan set are exact. Internal order is ignored for this target. The partition formula is: 0.30 × mean_chain_overlap + 0.30 × co_membership_f1 + 0.20 × orphan_overlap + 0.10 × exact_orphan_accuracy + 0.10 × exact_partition_accuracy Temporal Path Utility This component evaluates temporal order after structural matching. Mean position accuracy is the fraction of the twelve target positions containing the exact correct candidate. Mean pairwise temporal accuracy is the fraction of the eighteen gold temporal relations recovered correctly. Exact chain accuracy is the fraction of matched chains whose four candidate IDs are all in the correct positions. Exact structure accuracy is one only when all three matched chains and the complete orphan set are exact. The temporal formula is: 0.25 × mean_position_accuracy + 0.35 × mean_pairwise_temporal_accuracy + 0.20 × exact_chain_accuracy + 0.20 × exact_structure_accuracy Grounded Answer-Graph Utility Answers are evaluated after structural matching. An answer edge is correct when the answer attached to a predicted chain equals the answer belonging to its matched gold chain. Chain quality is: 0.50 × chain_overlap + 0.50 × chain_pairwise_order Grounded answer credit is: answer_correct × (0.20 + 0.80 × chain_quality) A correct answer attached to an exact chain receives full grounded credit. A correct answer attached to a structurally weak chain receives limited grounded credit. Mean answer accuracy measures correct matched answer edges without structural weighting. Correct answer-set accuracy is one when the three submitted answer IDs equal the three gold answer IDs as an unordered set. Exact answer-graph accuracy is one when all three matched question-to-answer edges are correct. The answer-graph formula is: 0.55 × mean_grounded_answer + 0.20 × mean_answer_accuracy + 0.10 × correct_answer_set_accuracy + 0.15 × exact_answer_graph_accuracy Confidence Utility Three binary exactness targets are evaluated. The structure target is one only when all three chain memberships, all twelve temporal positions, and all three orphans are exact. The answer target is one only when all three question-to-answer edges are exact after structural matching. The complete-case target is one only when both the structure and answer targets are one. For probability p and binary target y, Brier Utility is: 1 - (p - y)^2 The grader averages Brier Utility independently for p_structure, p_answers, and p_case. Confidence Utility is the mean of those three values. Confidence values do not influence structural matching. How Invalid Rows Enter the Metric The grader first scores every valid case normally. Each invalid expected case contributes zero to every published component. Operationally, component values calculated over valid cases are adjusted by the fraction of expected rows that are valid. This ensures that a malformed prediction affects its own case without erasing credit earned on correctly formatted cases. For example, if 1,199 of 1,200 expected cases are valid, the malformed case contributes zero while the other 1,199 cases retain their normal contributions. Submission-wide format failures remain zero-score conditions because the evaluator cannot reliably interpret individual rows. Local Submission Validation A local submission checker is provided to help catch formatting and schema problems before upload. Participants should use it after saving and reloading their final CSV. The local check is intended to detect problems such as: Missing required columns. Unexpected columns. Missing or duplicated sample_id values. Invalid JSON chain cells. Chains with the wrong number of candidate IDs. Out-of-range candidate IDs. Repeated candidate IDs within or across chains. Invalid or duplicated answer IDs. Missing, non-finite, or out-of-range confidence values. The checker is for submission validation. Hidden test labels are not released, so participants should not expect local validation on test.csv to reproduce the private leaderboard score. For model development, participants can create their own validation split from the labeled training cases and evaluate predictions against those held-out labels. Always validate the CSV after writing it to disk rather than validating only the in-memory prediction objects. Recommended Local Checks Before uploading a submission, verify that: The CSV contains all ten required columns. Every test sample_id appears exactly once. No unknown extra columns are present. Every chain is valid JSON. Every chain contains four distinct integers. The three chains use exactly twelve distinct candidate IDs. All candidate IDs are between 0 and 14. The three answer IDs are distinct integers between 0 and 5. p_structure, p_answers, and p_case are finite numbers between zero and one. Saving and reloading the CSV does not change any prediction values. Reordering submission rows does not affect your local processing because rows are identified by sample_id. Using the provided sample_submission.csv as the starting template is strongly recommended. Intended Modeling Approaches A strong solution can combine three complementary representations: Multilingual ASR hypotheses for Mandarin lexical and grammatical evidence. Pretrained speech-encoder representations for acoustic continuity, prosody, phonetic content, and boundary compatibility. Text or instruction-model representations for reconstructed-question coherence and answer compatibility. The strongest practical systems should not treat transcription as the final prediction. ASR is an intermediate representation that may be incomplete at fragment boundaries. Raw acoustic evidence remains important when a fragment begins or ends inside a syllable, when the transcription omits a grammatical particle, or when two locally plausible text continuations differ in spectral or prosodic continuity. Restrictions Predictions must be based primarily on the supplied audio fragments, written answer candidates, and released training labels. Predictions may not use: sample_id as a predictive feature. CSV row order as a predictive feature. Audio filenames as predictive features. File sizes or timestamps as predictive features. Compression artifacts intentionally unrelated to speech content. Hidden directory paths. Original source identifiers. Original repository ordering. External copies of the underlying recordings. Internet searches for exact private-test questions. Hard-coded private-test predictions. Manual reconstruction of private test cases. The task evaluates machine-learning systems rather than source-example lookup. The challenge is not designed for speaker identification, accent evaluation, demographic inference, medical diagnosis, psychological assessment, authentication, profiling, or surveillance. Medicine- or health-related material is treated only as factual language content. Competition predictions must not be interpreted as medical advice. Train and Validation Separation The challenge split does not reuse the upstream collection's original split. Normalized source groups are deterministically assigned to challenge train or test, and each group remains entirely on one side. Exact source groups do not cross the official split. For local validation, keep every complete case together. Do not split fragments from one case across training and validation. Why the Task Is Difficult Several ambiguities occur simultaneously. A model may understand an individual fragment but still fail because: It attaches the fragment to the wrong question. It identifies the correct group but predicts the wrong order. It mistakes an orphan for a target fragment. It chooses all three correct answers but attaches them incorrectly. It makes locally strong decisions that prevent a globally consistent solution. It produces overconfident probabilities for exact-case targets. The complete solution is a latent graph containing three temporal paths, three answer edges, and three orphan nodes. Expected Outcome A successful system should learn to: Group related Mandarin speech fragments. Recover within-question temporal order. Reject plausible orphan fragments. Match reconstructed questions with written answers. Decode all three chains jointly under uniqueness constraints. Calibrate probabilities for exact structure, exact answer graph, and exact case recovery. The defining task is to determine how fifteen audio fragments, six answer candidates, three temporal paths, three answer edges, and three orphan nodes fit into one coherent latent structure.
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Thermal Sensor Stack Ordering

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79fhx3bs6caapkk2rvh485gx8c50kj
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat aryanm's score of 0.555!

Full challenge description from page:

> Thermal Sensor Stack Ordering Problem domain: Seq2Seq Compute tier: GPU Direction: Maximize Score range: 0.0 to 1.0 Overview A vertical stack of room-temperature sensors observes the same indoor environment from different physical heights. Their absolute readings can be similar, but their response patterns differ as heating, cooling, ventilation and air movement propagate through the room. Each case contains four anonymized 60-step thermal-response sequences — candidate_0, candidate_1, candidate_2, candidate_3. They correspond to the same four physical room sensors, but their public positions are shuffled independently for every case. Your task is to output the four local candidate IDs in lowest-to-highest physical sensor order. For example, N2 N0 N3 N1 predicts that candidate_2 is lowest, followed by candidate_0, candidate_3 and candidate_1. Related work and design grounding This benchmark is a permutation-recovery task, but it differs from chronological permutation-reconstruction benchmarks, in which shuffled segments of one signal are reassembled into their original time order. Here the four sequences are simultaneous, not sequential: they are recorded at the same time from different heights, so temporal adjacency carries no information and the target is a physical spatial ordering rather than a chronological one. Reassembling by continuity at segment boundaries, the dominant strategy in chronological reordering tasks, is therefore inapplicable. The recoverable signal is vertical thermal stratification. Air temperature in a conditioned room varies systematically with height, and the effect is standardised for measurement: ISO 7730 and ASHRAE Standard 55 both define vertical air temperature difference between ankle and head level as a local thermal discomfort criterion, and ISO 7726 specifies the corresponding measurement heights. The source sensors sit at 10, 50, 100 and 150 cm, spanning that range. Ordering is recoverable because heating, cooling and ventilation reach these heights with different lag, amplitude and smoothness, not because absolute temperature increases monotonically with height. The public transform is drawn from the established time-series augmentation family for wearable and sensor signals: random monotone time-warping, magnitude scaling, jitter and smoothing, as introduced for sensor data by Um et al. (ICMI 2017) and catalogued in the empirical augmentation survey of Iwana and Uchida (PLOS ONE, 2021). Those transforms are normally used to enlarge a training set while preserving labels; they are used here for the inverse purpose, as an obfuscation layer that removes absolute level, amplitude and rate cues while preserving the relative response morphology the task depends on. Each candidate additionally receives an independent random gain and offset, which defeats ordering by amplitude. The evaluation harness combines three standard quantities rather than a single one: exact-position accuracy, permutation exact-match, and a pairwise concordance term that is the rank-correlation quantity of Kendall (Biometrika, 1938), normalised over the six candidate pairs. The composite weighting is specific to this benchmark and is chosen so that partially correct stratification receives graded credit instead of the all-or-nothing scoring typical of permutation tasks. The source measurements come from the RICO dataset, collected in the SINTEF ZEB Test Cell laboratory; full provenance is in the next section. Source, provenance and licence Dataset: RICO — multivariate HVAC indoor/outdoor measurements, SINTEF ZEB Test Cell laboratory Citation: Data in Brief, Volume 61, 2025, Article 111678 DOI: 10.60609/TW79-4K72 Files used: the five RICO_Acquisition_*.hdf releases, pinned by MD5 in prepare.py and re-verified on every build Licence: CC BY 4.0 — permits commercial use and derivative works, with attribution. The citation and DOI above are the required attribution and are carried in the private build manifest as well as here. RICO is published as a multivariate time-series resource with no defined benchmark target. The ordering task, the obfuscation layer, the splits and the metric introduced here are not part of that release. Source and split Each source experiment contains synchronized indoor environmental and HVAC measurements. The challenge uses four vertically separated room-temperature sensors from each eligible source experiment. Absolute source sensor names, timestamps, temperatures, source-file identities and acquisition metadata are not released as participant-facing case features. Source experiments are assigned to splits before derived challenge cases are created, and all variants generated from one source experiment remain within the same split. | Split | Source experiments | Cases | |---|---:|---:| | Train | 186 | 1,116 | | Validation | 59 | 354 | | Test | 60 | 360 | Each source experiment produces six independently transformed and shuffled challenge cases. Public inputs Each row contains case_id, candidate_0, candidate_1, candidate_2 and candidate_3. case_id is an opaque identifier used only for row and submission alignment. Each candidate_* field contains one chronological sequence of exactly 60 whitespace-separated integer tokens, every value in -12 through 12: -2 -2 -1 0 1 2 2 3 3 2 1 0 ... The candidate sequences are transformed versions of the underlying thermal responses. The public transformation suppresses absolute temperature level and scale and applies deterministic case-local transformations before quantization. Participants must therefore infer physical ordering from relative response structure rather than directly sorting raw temperature values. The mapping between public candidate columns and local node IDs is candidate_0 -> N0, candidate_1 -> N1, candidate_2 -> N2, candidate_3 -> N3. These node IDs are local to each row: N0 does not represent one fixed physical sensor across the dataset. Prediction target The target column is predicted_path. It contains exactly four whitespace-separated node IDs giving the physical sensor order from lowest to highest, and each of N0, N1, N2, N3 must appear exactly once. For example, N2 N0 N3 N1 means the hidden physical ordering is candidate_2, candidate_0, candidate_3, candidate_1, from lowest to highest. Dataset files train.csv — case_id, candidate_0..3, predicted_path validation.csv — same schema as train.csv test.csv — case_id, candidate_0..3 (target withheld) sample_submission.csv — case_id, predicted_path metadata.json — public benchmark configuration: candidate count, sequence length, split sizes, score range and metric version. It contains no hidden sensor identities and no test targets. Submission format Submit exactly two columns, in this order: case_id,predicted_path Your submission must match the test set exactly: the same number of rows as test.csv, and the same set of case_id values, each appearing exactly once. A missing ID, an extra ID, an unknown ID or a duplicated ID all score 0.0. Each predicted_path must contain exactly four whitespace-separated node IDs and must be a permutation of N0 N1 N2 N3, with no node repeated or omitted.csv case_id,predicted_path tes_example_001,"N2 N0 N3 N1" tes_example_002,"N1 N3 N0 N2" The example IDs and predictions above are illustrative only. Any malformed submission receives a score of 0.0. Evaluation The metric evaluates both exact rank placement and relative physical ordering. Each case receives three components. Position accuracy is the fraction of the four rank positions holding the correct candidate. If two of four candidates sit in exactly the right position, PositionAccuracy = 2 / 4 = 0.5. PositionAccuracy = (number of exactly correct rank positions) / 4 Pairwise order accuracy. Four candidates define six pairwise lower-before-higher relationships. A pair is correct when the submitted relative order of those two sensors matches the hidden physical order. This gives partial credit when a sequence is not exactly right but preserves much of the physical ordering. PairwiseOrderAccuracy = (number of correct pairwise order relationships) / 6 Exact path is 1 when the whole submitted four-node sequence matches the hidden target, and 0 otherwise. ExactPath = 1 if the full predicted path equals the target, else 0 Case score All three terms are added, each with a positive weight: case_score = 0.45 * PositionAccuracy + 0.35 * PairwiseOrderAccuracy + 0.20 * ExactPath Final score final_score = mean(case_score over all graded cases) The range is 0.0 to 1.0 and higher is better. A perfect submission scores exactly 1.0. A uniformly random permutation scores 0.295833 in expectation. Benchmark integrity Source experiments are isolated across train, validation and test before any derived challenge cases are generated, and all variants from one source experiment stay in the same split. Candidate identities are shuffled independently for every case, and participant-facing case IDs are opaque. Original source sensor names, source-file identities, timestamps and acquisition identifiers are not released as prediction features. RICO is a public dataset, so the preparation is audited against an attacker holding the raw archive: a joint retrieval attack that aligns under monotone time warping and searches every candidate-to-sensor assignment must gain no meaningful advantage over the same attack denied the true source experiment. &nbsp;
> $700 Pool
> Closes in 7h 43m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Galaxy Workflow Checkpoint Retention Priority

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cfkfhr0chbssc8ncaacx7518e7rpp
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat balaji's score of 0.326!

Full challenge description from page:

> Workflow Checkpoint Retention Priority Overview Scientific workflow engines produce intermediate results that may be expensive to recompute. At a checkpoint decision, retaining a result can save future work, while retaining every result wastes storage and discarding a useful result can force a long recomputation. The release turns this operational trade-off into a sequence-to-sequence prediction problem over real scientific workflow exports. Each row contains a deterministic canonical topological prefix ending at a current workflow step. Every non-empty workflow contributes exactly one deterministic checkpoint selected from its canonical positions, so no public group exposes another row that could reveal its continuation. The continuation after the released checkpoint is hidden. Given the visible prefix and current-step summary, generate a three-token retention trace for the current position and the next two positions in canonical order. When the workflow ends before all three positions exist, use a trailing terminal token for each missing position. The hidden evaluation keeps complete workflow graphs on one side of the split and keeps identical visible checkpoint-signature families together. This tests transfer to unseen workflow structures rather than row memorization or copying a matching public sequence. The output is an ordered local trace because an operator needs a coherent short planning window, not an isolated decision. Dataset File descriptions train.csv — Sparse feature rows for the training workflows; it contains no target column. train_targets.csv — Public id-keyed numeric targets for exactly the training ids; decode the base-four value into the three target tokens. test.csv — One-checkpoint feature rows for workflows held out as whole groups and visible-signature families from training; it contains no target or label column. sample_submission.csv — A deterministic non-constant example submission with the required id,prediction columns. The 703 non-empty real workflows each contribute exactly one checkpoint row: 562 training rows and 141 hidden-test rows. A checkpoint may be the final workflow step; in that case its missing future is represented by the trailing terminal suffix. Column descriptions The train.csv and test.csv files contain the same columns in the same order: id (string) — Stable opaque row identifier; submit it unchanged. workflow_group (string) — Opaque workflow-group key for group-aware local validation; it is not a semantic lookup key and does not encode graph topology. prefix_modules (string) — Space-separated normalized module-family tokens in canonical topological order through the current step. candidate_module (string) — Normalized module-family token for the current step. candidate_type (string) — Recorded type of the current step. prefix_length (integer) — Number of visible steps through the current step. parameter_count (integer) — Number of non-runtime parameter fields recorded for the current step. The train_targets.csv sidecar contains: id (string) — Training row identifier matching train.csv exactly and matching no test id. target (integer) — Base-four encoding of the three target tokens using discard=0, long_replay=1, branch_retain=2, and terminal=3, with the first token as the most significant digit. The sample_submission.csv file contains: id (string) — Test row identifier matching test.csv exactly. prediction (string) — A JSON array containing exactly three ordered tokens. Evaluation For each workflow step, let c be the number of distinct immediate children and let d be the number of distinct downstream descendants. Both values are nonnegative integers, and every immediate child is a downstream descendant, so valid records satisfy d >= c. Exactly one of these four disjoint cases applies: If c >= 2, emit branch_retain for every valid value of d. If c = 8, emit branch_retain. If c = 2 emits branch_retain even when d is between 3 and 7. There is no fifth valid case, so the four rows are exhaustive and have no overlap. A row target is the three-token sequence beginning at the current step's canonical position; later positions use the next two positions from the same canonical topological order. Missing later positions are encoded by a trailing terminal suffix. These thresholds are a topology-only prioritization proxy: fan-out and broad downstream reach indicate more branches or more future work that could be forced to recompute, while a short continuation offers less reuse value. The source has no execution-time, result-size, cache-hit, or storage-cost telemetry, so the benchmark measures structural prioritization and transfer rather than claiming to estimate a literal runtime saving. The four-case partition above is the evaluator's definition of the hidden oracle. It is disclosed so that the token meanings and boundary behavior are auditable; it is not an executable feature recipe in the solver package. The solver-visible files contain no graph edges, step ids, child lists, continuation records, or values of c and d. prefix_modules is only an ordered module-family string, and workflow_group is an opaque grouping key; neither field encodes the hidden topology. Applying the oracle therefore requires private workflow information that is outside the public input contract. This benchmark measures prediction from lossy public evidence about a hidden continuation, rather than recovery of the oracle counts. Module order, current-step type, parameter footprint, and prefix position provide real but incomplete signal about the local three-token trace. Because only one checkpoint row is released per workflow, a solver cannot reconstruct a workflow's continuation from another public row in the same group. In author-side workflow-disjoint validation, a positional trace prior scored 0.159831 while a learned prefix decoder scored 0.283321 on the current hidden groups. The public prior is a baseline; the score is method-agnostic, and the supplied reference solution demonstrates fitting a multi-position decoder to the public evidence. Submissions are scored using weighted_cache_trajectory_score, a maximize metric in [0, 1]. Position 0 receives weight 0.5, position 1 receives weight 0.3, and position 2 receives weight 0.2 because the current checkpoint is the immediate operating decision. Position 0 can only contain a retention token because every row starts at an existing workflow step, so its token-F1 vocabulary excludes the impossible terminal token. Positions 1 and 2 use token F1 weights of 1.0 for discard, 1.5 for long_replay, 2.0 for branch_retain, and 0.5 for terminal. At each position, normalization uses only tokens present in the truth or prediction; this keeps an exact answer at 1.0 even when a token is absent from a particular holdout, while a predicted absent token is still penalized. The weighted token score receives weight 0.8 and the exact three-token sequence rate receives weight 0.2. The terminal token has lower weight because it marks padding rather than a retention action. The metric is defined by this complete code: import numpy as np TOKENS = ["discard", "long_replay", "branch_retain", "terminal"] TOKEN_WEIGHTS = {"discard": 1.0, "long_replay": 1.5, "branch_retain": 2.0, "terminal": 0.5} POSITION_WEIGHTS = np.asarray([0.5, 0.3, 0.2], dtype=float) POSITION_TOKEN_WEIGHTS = [ {"discard": 1.0, "long_replay": 1.5, "branch_retain": 2.0}, TOKEN_WEIGHTS, TOKEN_WEIGHTS, ] def token_f1(y_true, y_pred, token): true = np.asarray(y_true) == token pred = np.asarray(y_pred) == token tp = np.sum(true & pred) fp = np.sum(~true & pred) fn = np.sum(true & ~pred) denominator = 2 * tp + fp + fn return 0.0 if denominator == 0 else (2.0 * tp) / denominator def weighted_cache_trajectory_score(y_true, y_pred): truth = np.asarray(y_true, dtype=object) prediction = np.asarray(y_pred, dtype=object) if truth.shape != prediction.shape or truth.ndim != 2 or truth.shape[1] != 3: raise ValueError("truth and prediction must have the same shape (n, 3)") position_scores = [] for position in range(3): position_weights = POSITION_TOKEN_WEIGHTS[position] active_tokens = [ token for token in position_weights if np.any(truth[:, position] == token) or np.any(prediction[:, position] == token) ] if not active_tokens: position_scores.append(0.0) continue position_score = sum( token_f1(truth[:, position], prediction[:, position], token) * weight for token, weight in position_weights.items() if token in active_tokens ) / sum(position_weights[token] for token in active_tokens) position_scores.append(float(position_score)) token_score = float(sum(score * weight for score, weight in zip(position_scores, POSITION_WEIGHTS)) / sum(POSITION_WEIGHTS)) exact_sequence_rate = float(np.all(truth == prediction, axis=1).mean()) return float(0.8 token_score + 0.2 exact_sequence_rate) Malformed JSON, unknown tokens, sequences other than three tokens, a terminal first token, and non-trailing terminal tokens are rejected. A token absent from both truth and prediction is omitted from that position's normalization; a token present only in the prediction is included and penalized by its F1 of zero. Higher scores are better and the score is always bounded by 0 and 1; an exact answer scores 1.0. Submission Submit one UTF-8 CSV with exactly these columns, in this order: id (string) — Test identifier copied unchanged from test.csv. prediction (string) — JSON array of exactly three tokens from discard, long_replay, branch_retain, and terminal; any terminal tokens must be a trailing suffix. The submission must contain exactly 141 data rows, one for every test id, with no duplicate or unknown ids. Example: id,prediction 013a578555856a2c,"[\"discard\",\"long_replay\",\"branch_retain\"]" 02981e76cfaf221a,"[\"branch_retain\",\"terminal\",\"terminal\"]" 037fcb757dfc9cc1,"[\"discard\",\"discard\",\"terminal\"]" Requirements Keep train.csv and test.csv feature columns identical and in the documented order. Join train_targets.csv by id; its ids cover every training id and no test id. Keep local validation folds workflow-disjoint using workflow_group; do not place one workflow in both a training fold and its validation fold. Treat workflow_group as a fold key, not as a source of a complete workflow; exactly one checkpoint row is released for each non-empty workflow. Use the canonical topological-prefix semantics and smallest-step-id tie break when reproducing local features. The supplied reference solution fits a multi-position decoder using only the public feature files; submissions may use any model that respects the public input contract. Run offline with the supplied public files and finish within the selected CPU runtime budget. What Not To Use Do not reverse-map opaque ids, workflow groups, or module tokens to recover the complete graph for a held-out workflow. Do not use external copies, mirrors, notebooks, or lookup tables that reveal downstream edges or target sequences for these workflows. Do not infer target sequences from row order, workflow-group numbering, candidate ids, or the presence of a particular test row. Do not combine sparse rows from a public group with external records to reconstruct omitted positions or the final step. Do not use private graph topology, hidden continuation records, or external lookup data to reconstruct c, d, or the target sequence. Do not generate synthetic workflows, synthetic prefixes, or synthetic target sequences. &nbsp;
> $700 Pool
> 3 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Rebind Two Missing Moon-Orbiter Frames

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ecy24smjphhf5ft2mczc0en8dwx6d
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat ak_2434's score of 0.683!

Full challenge description from page:

> Lunar Interregnum: Rebind Two Missing Moon-Orbiter Frames Overview An interval in an authentic DSLWP lunar-orbiter downlink has lost two consecutive radio frames. For each episode you receive the intact frame immediately before the gap, the intact frame immediately after it, and eight shuffled candidate frames from the same UTC-day spacecraft/channel stream. Exactly two candidates belong in the gap. Recover their slots in chronological order. This is a structured sequence-retrieval task over binary telemetry, not row-wise tabular classification or regression. Each decision jointly ranks 56 ordered candidate pairs. The two direct source counter bytes at zero-based positions 2 and 3 and the four source CRC bytes at positions 219 through 222 are withheld. Each other byte independently has a 27% chance of one uniformly selected bit being flipped. The effective expected bit-error rate is therefore about 3.375%. The corruption is deterministic for the released dataset, identically distributed across anchors and candidates, and carries no label information. Most metric weight is carried by the complete ordered splice. &nbsp; Evaluation The score is the difficulty-weighted Lunar Ordered Splice Utility in [0, 1]; higher is better. For a row with structurally valid, distinct integer predictions p1 and p2 in 0..7, true slots t1 and t2, and private weight w, define: def row_utility(t1, t2, p1, p2): if p1 not in range(8) or p2 not in range(8) or p1 == p2: return 0.0 return ( 0.105 0.045 * (p1 == t1) 0.030 * (p2 == t2) 0.820 * (p1 == t1 and p2 == t2) 0.105 * (p1 == t2 and p2 == t1) ) def evaluate(true_first, true_second, pred_first, pred_second, weights): values = [ row_utility(t1, t2, p1, p2) for t1, t2, p1, p2 in zip( true_first, true_second, pred_first, pred_second ) ] return sum(w * value for w, value in zip(weights, values)) / sum(weights) The 0.105 term is a provisional base for an in-range pair of distinct slots, not a guaranteed minimum row score. For a fully reversed true pair, the reversal term cancels that base exactly, so its utility is 0.105 - 0.105 = 0.0. A valid non-reversed pair with neither position correct scores 0.105; a first-position-only hit scores 0.150; a second-position-only hit scores 0.135; and a completely correct ordered pair scores 1.0. Thus 82% of total row utility is reserved for recovering the complete ordered splice. The supplied fixed-pair sample scores 0.137228114478 over the complete test set because its weighted average includes the provisional base and occasional position matches; no per-row floor is claimed. The private weights are 0.75, 1.00, and 1.35 for easy, medium, and hard candidate banks as measured by the rank of the true path under a fixed label-blind transition ambiguity calculation. The 563 test rows contain 121, 267, and 175 rows at those weights, respectively, so the fixed denominator is 594.0. The grader merges by id before applying the weighted mean. The canonical private-answer schema is id,first_slot,second_slot,difficulty_weight. If the platform appends its standard trailing visibility metadata column, the grader validates that its values are public or private and then ignores that column for scoring. This exception applies only to the platform answer frame; participant submissions must still contain exactly the three documented submission columns. Missing, renamed, extra, duplicate, or foreign-ID structure raises a clean ValueError. For an otherwise structurally valid submission, nonnumeric or non-finite values, non-integral values, repeated slots, and slots outside 0..7 give that row utility 0.0. The final score is always finite. Dataset All files are under ./dataset/public/. train_frames.npy (uint8, shape (1261, 10, 223)) — training episodes. train_ids.npy (Unicode string, shape (1261,)) — randomized opaque training IDs. train_targets.npy (uint8, shape (1261, 2)) — ordered true candidate slots for training. test_frames.npy (uint8, shape (563, 10, 223)) — test episodes. test_ids.npy (Unicode string, shape (563,)) — randomized opaque test IDs. sample_submission.csv (CSV, 563 rows) — label-free constant example. Every numeric value in the prepared files is finite. Frame and target tensors use uint8; submission slots use integers; and private difficulty weights are restricted to 0.75, 1.00, and 1.35. For every episode tensor: Axis position 0 is the left anchor frame. Axis position 1 is the right anchor frame. Axis positions 2..9 are candidate slots 0..7. Every frame has 223 byte values in 0..255. Zero-based byte positions 2, 3, 219, 220, 221, and 222 are always zero because their source counters and CRC are withheld. Every other byte is exposed after deterministic, role-symmetric single-bit corruption at the documented rate. train_targets[row, 0] is the slot of the first missing frame. train_targets[row, 1] is the slot of the second missing frame. The source contains 21,032 received records. Preparation retains 20,301 valid distinct non-replay frames and creates 1,824 distinct episode tensors from 18,240 non-reused source frames. Every prepared frame occurrence comes from a different retained source frame, eliminating the cross-episode sliding-window reconstruction shortcut. Whole UTC observing days are held out: 62 days contribute training episodes and 29 different days contribute test episodes, with zero day overlap, zero source-frame reuse, zero prepared-frame duplication, and zero identical episode tensors across the split. Submission Write ./working/submission.csv with exactly three columns in exactly this order: id — every test ID exactly once. first_slot — integer candidate slot 0..7 for the first missing frame. second_slot — a different integer candidate slot 0..7 for the second missing frame. The file must contain exactly 563 rows. Row order does not matter because grading merges on id. Example using real test IDs: id,first_slot,second_slot rid_9541a23904f9a63ebfea9d21,0,1 rid_6378e7614e0968d219b8a469,0,1 rid_f24bb3441df592a5c477548f,0,1 Requirements Train model parameters from scratch using only the supplied public files. Preserve every test ID exactly once; do not add columns. Emit two distinct integer slots in 0..7 for every row. Treat each episode as an ordered binary sequence problem; candidate file order and IDs are randomized and inert. Write only ./working/submission.csv. What not to use Do not use pretrained weights, pretrained packet decoders, foundation models, or embeddings trained outside this challenge. Do not use external datasets, internet access, runtime downloads, or package installation. Do not recover source timestamps or withheld counters from another copy of the DSLWP corpus. Do not hardcode test IDs, candidate slots, or a fixed output file. Extra Modeling Information Lunar Interregnum asks a question: select and order a missing two-frame path from a hard same-burst candidate bank after the direct counter source is withheld, under observing-day cold start. This challenge is discrete listwise path recovery over authentic 223-byte radio frames, with pair exactness and order reversal explicitly scored. It is neither scalar imputation nor anomaly classification. &nbsp; &nbsp;
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Counterfactual Evidence Prioritization

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72sv9nfn4ac664pt8w2ajc3h8e4hg9
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat shishu's score of 0.794!

Full challenge description from page:

> Counterfactual Evidence Prioritization Overview Build a ranked evidence queue for analysts reviewing English passages. For each passage, either abstain or extract a condition describing an unreal or contrary-to-fact situation together with its linked outcome. Assign every extracted record a confidence so that accurate, complete evidence is prioritized ahead of false alarms and weak extractions. Each input is an intact excerpt. A modal word such as “would” or a connective such as “if” does not by itself establish a counterfactual relationship. Predict both roles together, without resolving pronouns, inventing missing context, or estimating whether an imagined intervention would actually work. A false record wastes review effort, a missed record hides potentially useful evidence, and inaccurate boundaries make the evidence harder to reuse. Your complete solution must run on CPU, use no more than 62 GB RAM, and finish within 1.5 hours, including preprocessing, training, validation, inference, and writing the submission. Dataset dataset/public/ ├── train.csv ├── test.csv └── sample_submission.csv There are 4,000 training excerpts and 800 test excerpts. Each row is one excerpt. Training and test come from separate source partitions, and components of exact or strongly overlapping text do not cross between them. This does not establish that different rows came from different articles because article identities are unavailable. Use training-only partitions for development and confidence calibration. train.csv id,text,spans,confidence id is a nonempty opaque string. text is the complete Unicode input, with a length from 1 through 4,000 Unicode code points. Count characters as Python's len(text) does, including spaces, punctuation, and newline characters; do not count UTF-8 bytes or UTF-16 code units. No field is missing. spans is a JSON string containing either [] for an excerpt annotated as non-counterfactual or [[condition_start,condition_end],[outcome_start,outcome_end]] for an annotated evidence pair. Offsets are zero-based and half-open, so text[start:end] recovers the phrase. The condition is listed first even when the outcome appears earlier. Both spans are nonempty, non-overlapping, and uniquely grounded in the visible excerpt. In training, confidence is the binary relevance target: it is 1 when spans contains an annotated pair and 0 when spans is empty. In a submission, the same column contains your continuous confidence in the complete extracted pair. Use training-only validation to estimate extraction reliability as well as passage relevance: a counterfactual passage with inaccurate spans is a poor queue entry. The annotations identify a selected counterfactual condition and its expressed outcome. Follow the demonstrated phrase boundaries, including negation and words belonging to each phrase. Context outside the marked phrases remains available as input. The annotations do not claim causal truth and are not exhaustive inventories of every hypothetical remark in a passage. Minor boundary differences receive partial credit; a different unannotated relationship is not the selected record. test.csv id,text The two fields have the same meanings as in training. Predict one complete evidence pair or abstain for every row, then assign a confidence to each submitted pair. sample_submission.csv id,spans,confidence The sample copies the test IDs, predicts [], and uses confidence 0 for every excerpt. It is valid and scores 0 because the evaluation contains annotated evidence records. Submission format Write predictions to: working/submission.csv Required column names: id,spans,confidence For the illustrative input If the bridge had held, the road would have stayed open., predict If the bridge had held as the condition and the road would have stayed open as the outcome, with a high confidence if the complete record is reliable. For The road is open today., abstain. The following two rows illustrate those predictions; use the actual test IDs in your submission. id,spans,confidence q_aaaaaaaaaaaaaaaaaaaaaaaa,"[[0,22],[24,55]]",0.91 q_bbbbbbbbbbbbbbbbbbbbbbbb,[],0 Use UTF-8 CSV; an initial UTF-8 byte-order mark is accepted. Quote JSON cells correctly for CSV. The file must be at most 16,000,000 bytes and contain between 1 and 2,000 data rows, covering the complete supplied test set. Each spans cell must be a JSON string of at most 1,024 UTF-8 bytes. Its only permitted shapes are [] and an array of exactly two [start,end] arrays. Every offset must be a JSON integer satisfying 0 <= start < end <= 4000; booleans, floating-point numbers, nulls, NaN, and infinities are invalid. Adjacent spans are allowed; overlapping spans are invalid. Use a finite confidence from 0 through 1, inclusive. Decimal and scientific notation are accepted, with at most 32 UTF-8 bytes per CSV confidence cell; percentages, booleans, nulls, NaN, and infinities are invalid. Confidence 0 is allowed with a nonempty pair and places it last among extracted pairs. An empty spans value always abstains, regardless of confidence. Confidence is used for ranking; monotonic transformations that preserve pair order do not change the score. Include each test ID exactly once, with no missing or additional IDs. IDs have the form q_ followed by 24 lowercase hexadecimal characters. Rows and columns may be reordered. Required column names must match exactly, including case; additional columns are ignored. Duplicate headers, blank records, malformed quoting, and missing required values are invalid. An invalid submission is rejected in full. Values are not repaired, clipped, or partially scored. Evaluation The score is quality-aware evidence average precision in [0.0, 1.0]. Higher is better. It rewards ranking accurate, complete counterfactual evidence early. Every queued record consumes review effort; inaccurate extractions reduce queue precision even on counterfactual passages. For two half-open spans p and g, define character overlap as I(p,g) = max(0, min(p.end,g.end) - max(p.start,g.start)) and character Dice as D(p,g) = 2*I(p,g) / ((p.end-p.start) + (g.end-g.start)). For a submitted pair on an annotated positive passage, its extraction quality is q = min(D(predicted_condition, annotated_condition), D(predicted_outcome, annotated_outcome)). Its quality is zero on an annotated negative passage or when either span extends beyond the input text. Such out-of-text predictions within the 4,000-character format limit remain in the queue and receive a score; their offsets are not clipped. Both roles must overlap their corresponding annotations to earn quality; swapping roles changes the result, and the weaker span determines the complete record's quality. Discard abstained rows from the ranked queue. Sort the remaining rows by decreasing confidence, breaking equal-confidence ties by ascending id. At rank k, let Q_k = q_1 + ... + q_k be the cumulative extraction quality. Let G be the total number of annotated evidence pairs in the test set, including those on abstained passages. Evidence precision at rank k is Q_k / k; evidence recall increases by q_k / G at that rank. The score is: (1 / G) sum over all queued rows at rank k of q_k (Q_k / k) If G is zero, the score is 1 only for an empty queue and 0 otherwise. In this evaluation G is positive. All rows contribute before the final division, with no intermediate rounding. For example, suppose there are two annotated pairs and the queue contains qualities 0.5 followed by 1.0. Evidence precision is 0.5 at rank 1 and 0.75 at rank 2, so the score is (0.50.5 + 1.00.75)/2 = 0.5. Ranking the complete pair first gives (1.01.0 + 0.50.75)/2 = 0.6875. Confidence therefore needs to reflect extraction quality, not just whether a passage is counterfactual. Exact extraction of every annotated pair, ranked before all false records, reaches 1. Abstaining everywhere reaches 0. Missing pairs reduce recall; false records and inaccurate extractions ranked before useful records reduce precision. Records with zero quality ranked after every record with nonzero quality do not change the score. Not allowed Do not use external datasets, pretrained model weights, pretrained embeddings or tokenizers, language-model APIs, internet source lookup, or manually assigned test labels. Do not hardcode predictions by test ID or source identity. Do not fit preprocessing, vocabularies, thresholds, or model parameters on test data, and do not use one test row's contents to change another row's prediction. &nbsp;
> $700 Pool
> Closes in 2h 38m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Sim-to-Field Anonymous-Witness Reservoir Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79pkb4tfxen3mw327mj00swn8drb7a
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat jlm99's score of 0.244!

Full challenge description from page:

> Sim-to-Field Anonymous-Witness Reservoir Reconstruction Overview This is a Sequence to Sequence domain-transfer task. A target reservoir has a 35-day telemetry blackout. You receive its 28 normalized storage and water-level readings immediately before the outage, its 28 readings immediately after, and an anonymous variable-size set of 2–5 other reservoirs that remained online in the same basin for all 91 aligned days. Reconstruct the target's two hidden nonlinear excursion sequences and attribute the reconstruction across the anonymous witnesses. The central difficulty is simulator-to-field transfer. Every labeled training row is a coupled network simulation, exposed at one of three fidelity bands. Every test row and hidden test target is an observed field case from a reservoir absent from training. Models must learn from synthetic variation without assuming that simulator artifacts persist in the observed domain. The field cases derive from historical daily reservoir telemetry released under a redistributable open-data license. Source attribution and licensing are provided with the dataset documentation rather than in this solver-facing task. Reservoir names, basin names, dates, coordinates, absolute capacities, and physical measurement scales are removed. Field-case inclusion never uses hidden excursion magnitude, so ordinary, low-excursion, and pronounced outages are represented. Synthetic-to-Observed Transfer Regime Training begins from eligible historical contexts but publishes only simulated inputs and simulated targets. A deterministic process surrogate adds a broad basin forcing and a sharper operational pulse, applies different capacity-dependent responses to the target and anonymous witnesses, couples level to storage with a hysteresis term, adds low-amplitude colored sensor variation, and renormalizes the resulting trajectories. Each base context produces one row at each fidelity: simulated_near: mild intervention closest to the field distribution; simulated_mid: moderate intervention; simulated_stress: stronger intervention and domain shift. The test domain is observed: neither its inputs nor targets receive those simulator interventions. There are no observed target rows in public training. The three fidelities form a transfer curriculum, not three copies—the complete public input tuple is unique for every row. A useful method may learn broadly across all fidelities, calibrate on the near band, use domain-invariant representations, or explicitly model the simulator-to-observed shift. Because a literal observed value would make the test domain column constant, observed cases instead receive one of three public-context activity sub-regimes. These bands use only motion in the visible target flanks and witness trajectories; they never inspect the hidden interval. Objective and Target Semantics Each case covers 91 consecutive days: days 1–28: visible target-reservoir left flank; days 29–63: hidden 35-day target outage; days 64–91: visible target-reservoir right flank; days 1–91: fully visible trajectories for every anonymous witness. Target storage and level are normalized separately per case from the two visible flanks and clipped to [-4, 4]. For each hidden day, endpoint interpolation is the straight line from the last left value to the first right value. The target excursion is the true hidden normalized value minus that interpolation. Predict three objects: storage_excursion: 35 chronological storage departures; level_excursion: 35 chronological water-level departures. witness_attribution: a fixed length-8 probability array. Its first K positions attribute the event across the row's witnesses, while the remaining 8-K inactive positions are zero. Positive values mean the hidden pulse lay above endpoint interpolation; negative values mean it lay below. These sequences preserve pulse direction, accumulated departure, crest/trough magnitude, event timing, and coupled storage-level motion. Attribution is an analogue score, not a causal claim. Preparation computes each witness's own 35-day endpoint-relative storage excursion. Its distance to the hidden target is 0.70 * mean_abs_error(target storage, witness) + 0.30 * mean_abs_error(target level, 0.55 * witness). A temperature-0.35 softmax over negative distances produces the target probability vector. Competitors see these labels for train but must infer them for test without the hidden target pulse. Why the Anonymous Witness Set Matters Each witness trajectory is normalized by its own 91-day median and interquartile range, then clipped to [-4, 4]. witness_capacity_ratio[j] is the clipped log capacity ratio of witness j to the target. Index j joins the trajectory to its attribute within that row only. The released outer set has between 2 and 5 members. Members have a case-specific anonymous ordering, so the same slot has no identity across rows. Permuting trajectories and capacities together must leave the two reconstructed sequences unchanged and permute the attribution probabilities in the same way. Padding plus masking and a shared set encoder are suitable approaches. The attribution output remains padded to length 8 for a fixed evaluator schema. Unlike ordinary fixed-channel gap filling or reservoir forecasting, this task combines a synthetic-to-observed evaluation boundary with an unordered, variable-cardinality context set while producing both invariant sequences and member-aligned probabilities. Public Dataset | File | Rows | Description | |---|---:|---| | train.csv | 1,269 | Simulated inputs and all three simulated targets: 423 rows at each fidelity, derived from 48 training target reservoirs. | | test.csv | 184 | Inputs only from 17 different target reservoirs. | | sample_submission.csv | 184 | Valid deterministic chance-style output with the required schema. | All test rows are observed field cases. The 48 train and 17 test target reservoirs are disjoint, and witnesses come from a separate reservoir pool. Target windows are spaced so a hidden interval cannot appear in another case's public flank. Rows are stably shuffled and use opaque IDs. Columns | Column | Type | Availability | Meaning | |---|---|---|---| | case_id | string | train, test | Opaque submission key; never use it as a feature. | | domain | string | train, test | Transfer regime: simulated_near, simulated_mid, or simulated_stress in train; observed_quiet, observed_typical, or observed_dynamic in test. The observed suffix is a stable rank band calculated only from public context motion. | | storage_left | JSON float array, length 28 | train, test | Target storage before the outage, oldest to newest. | | storage_right | JSON float array, length 28 | train, test | Target storage after the outage, oldest to newest. | | level_left | JSON float array, length 28 | train, test | Target water level before the outage. | | level_right | JSON float array, length 28 | train, test | Target water level after the outage. | | witness_storage | nested JSON float array, shape K × 91 | train, test | Full aligned storage trajectories for an anonymous set of K witness-only same-basin reservoirs; 2 ≤ K ≤ 5 in this release. | | witness_capacity_ratio | JSON float array, length K | train, test | Capacity attributes paired by index with witness_storage; values are clipped log ratios in [-3, 3]. | | storage_excursion | JSON float array, length 35 | train only | Hidden target storage departure from endpoint interpolation. | | level_excursion | JSON float array, length 35 | train only | Hidden target level departure from endpoint interpolation. | | witness_attribution | JSON probability array, length 8 | train only | Soft analogue attribution in the first K positions, paired by witness index; remaining positions are zero and all eight values sum to 1. | All sequences are chronological and rounded to four decimal places. Witnesses are public contextual measurements, never target labels. Submission Format Write ./working/submission.csv with exactly: case_id,storage_excursion,level_excursion,witness_attribution Each excursion cell must be a valid JSON array of exactly 35 finite numbers in chronological order, each within [-8, 8]. witness_attribution must contain exactly eight finite probabilities in [0,1] that sum to 1. Positions 0 through K-1 pair with the K input witnesses; positions K through 7 are inactive and should be zero. Probability mass assigned to inactive positions is treated as incorrect attribution. Include exactly one row for every one of the 184 test IDs, with no duplicate, missing, blank, extra, or unknown IDs and no additional columns. The grader aligns by case_id, not row order. Evaluation: Anonymous-Witness Pulse Skill Score The score is bounded to [0, 1]; higher is better. It evaluates event geometry, not only pointwise filling. For arrays y, p and tolerance t: C(y,p;t) = mean(clip(1 - abs(y-p)/t, 0, 1)) The raw pulse score RawPulse combines: target values: storage 0.24, level 0.10, using t=1.0; first differences: storage 0.08, level 0.04, using t=0.45; all 35 prefix means: storage 0.12, level 0.05, using t=0.8; signed mean pulse area: storage 0.08, level 0.03, using t=0.55; trough and crest amplitudes: storage 0.08, level 0.04, using t=1.0; trough and crest timing: storage 0.06, level 0.03, linearly tolerant over 12 days; joint two-signal first-difference vectors: 0.05, using Euclidean tolerance 0.65. The prefix, area, extrema, timing, and joint-motion terms make up 54% of the raw score. They distinguish two paths that have similar pointwise error but imply different operational pulse geometry. Let ZeroScore be the raw pulse score of zero excursion everywhere—the endpoint-interpolation prediction. The pulse skill P is: P = clip((RawPulse - ZeroScore) / (1 - ZeroScore), 0, 1) For the fixed-width attribution truth q and prediction a, 1 - 0.5*sum(abs(q-a)) measures probability overlap across all eight positions. It is normalized against the row's valid uniform distribution—equal mass on the first K positions and zero on inactive positions—to obtain attribution skill A, then clipped to [0,1]. The final score is: Score = 0.85 * P + 0.15 * mean(A) Zero excursion plus uniform attribution scores exactly 0.0; exact sequences plus exact attribution score 1.0. Worse-than-baseline components are clipped to zero. The metric is valid on any non-empty answer shard. Constraints Use only supplied public files and libraries already available in the competition image. Compute tier: A10G · Standard ML workloads. The reference uses shared witness encoders, invariant pooling, temporal convolutions, attention, and mixed-precision CUDA. H100 hardware is unnecessary. Do not use internet calls, hosted APIs, external datasets/code, or challenge-specific pretrained checkpoints at solution time. Do not attempt to deanonymize reservoirs or dates, fingerprint external copies, infer identity from witness position, or use case_id/row order as predictors. Do not tune against hidden answers, submission feedback, malformed JSON, parser behavior, or grader limits. What Success Requires A strong system must bridge the simulator-to-field shift, infer which anonymous regional pulses remain informative, preserve temporal alignment, combine a changing number of witnesses without slot identity, use both target flanks, and recover pulse functionals that ordinary MAE/RMSE imputation metrics ignore. The test split evaluates transfer to both an observed domain and unseen infrastructure. &nbsp;
> $700 Pool
> Closes in 3h 56m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Hungarian Construction Indexing

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73hndfy8k936nap3shyf7jnd8e4pzt
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat abu2win's score of 0.720!

Full challenge description from page:

> Hungarian Construction Indexing Overview Historical-text editors need searchable concordances that preserve how a verb construction was written while linking inflected and separated forms to the same lexical entry. Your task is to turn a marked construction from historical Hungarian court testimony into an index record: its normalized surface text, canonical preverb lemma, and verb lemma. All three components must be correct for an editor to accept the record automatically. You receive the original text before the marked construction, the construction itself, and any available text after it. The marked span can contain an attached preverb, a detached preverb, intervening words, or a historical auxiliary. Normalize the entire marked span, retaining intervening words and historical morphology. Identify the preverb and main verb represented by that span; their lemmas form the lexical index key even when they appear in a different order in the text. You do not need to locate additional constructions elsewhere in the context. The annotations standardize spelling rather than translate everything into contemporary Hungarian. Preserve archaic word forms when the training examples do. The text contains historical spellings, transcription signs, and occasional inherited annotation inconsistencies. Context is incomplete, and the right context is usually empty. The task measures agreement with the supplied annotation convention, not an independently verified edition of each document. Your complete solution must run on CPU, use no more than 62 GB RAM, and finish within 1.5 hours including preprocessing, training, validation, inference, and writing the submission. Dataset dataset/public/ ├── train.csv ├── test.csv └── sample_submission.csv There are 3,000 training rows and 800 test rows, each representing one marked construction occurrence. Training contains 22 dependency groups and test contains six. Groups keep documents from the same historical county together; detected duplicate contextual passages are also kept together. The partitions use different groups and documents. These groups do not establish independent witnesses or scribes. Use the supplied training group field for validation by holding out entire groups; individual rows from one document can share context. All files are UTF-8 CSV with a header and standard CSV quoting. Read empty input-context cells as empty strings, not missing values. For example, pandas users can pass dtype=str, keep_default_na=False. Existing transcription signs such as _, @, or ! inside text are input characters, not instructions or special missing-value codes. train.csv id,group,before,focus,after,analysis | Column | Type and meaning | |---|---| | id | Unique opaque occurrence ID, r_ followed by 16 lowercase hexadecimal digits. | | group | Opaque dependency-group ID, g_ followed by 16 lowercase hexadecimal digits. Use for validation, not as linguistic evidence. | | before | Original left context; at least three whitespace-delimited tokens. | | focus | Original marked construction; 1–120 Unicode characters. | | after | Available original right context, possibly empty. | | analysis | JSON array of exactly three strings: [normalized construction, preverb lemma, verb lemma]. | The three input-text fields total at most 1,600 Unicode characters per row. Their Unicode is NFC-normalized and runs of whitespace are replaced by single spaces; spelling and transcription signs remain. Training outputs are lowercase NFC text with single spaces. A normalized construction retains its surface word order and inflection; its two lemma components represent lexical identity. For example, a negative separated construction keeps its negation in the first component but not in the lemma pair. Derivatives and historical auxiliaries follow the examples' annotation convention. No exhaustive lemma vocabulary is imposed, and previously unseen lexical forms may occur. test.csv id,group,before,focus,after These fields have the same meanings and bounds as in training. Predict one analysis for every row. sample_submission.csv id,analysis The sample copies each public focus into the first component and leaves both lemma components empty. It demonstrates a valid incomplete prediction and scores 0 because a correct record requires all three components. Empty strings are allowed abstentions; they do not receive credit for nonempty reference components. Submission format Write predictions to: working/submission.csv Required columns, shown in canonical order: id,analysis The following two examples are invented and are not challenge rows. For before = "A jegyző szavai szerint", focus = "el nem ment", and after = "azon az éjjelen", the analysis retains the separated negative construction and identifies the lexical pair as el plus megy. For before = "A levélben ezt írták", focus = "fel emeltem", and empty after, the normalized construction joins the preverb to the inflected verb while the lexical pair uses the lemmas fel and emel. A CSV row uses doubled quotation marks inside a quoted JSON field: id,analysis r_0123456789abcdef,"[""el nem ment"",""el"",""megy""]" r_fedcba9876543210,"[""felemeltem"",""fel"",""emel""]" Submit every test ID exactly once, with no additional IDs. Row and column order are immaterial; required names are case-sensitive. Extra CSV columns are ignored consistently. Missing required names and duplicate headers are invalid. Group context is taken from the supplied input groups automatically, so it is not part of your predictions. Each analysis cell must contain one valid JSON array of exactly three strings. Each decoded string may contain 0–160 Unicode characters; control characters and Unicode surrogates are prohibited. Objects, nested arrays, numbers, booleans, null, NaN, infinity, and trailing JSON content are invalid. Strings need not occur in training. Incorrect but well-formed analyses receive a score rather than a format error. The submission must have 1–2,000 rows, subject to the stricter requirement to match all test IDs exactly. Every required cell must be a string of at most 4,000 characters with no missing values. Use UTF-8, optionally with a BOM, and valid CSV quoting; LF or CRLF line endings are accepted. Blank/ragged records, stray or unterminated quotes, duplicate/missing IDs, invalid encoding, and violations of these limits cause the entire submission to be rejected. No invalid values are repaired and no valid subset is scored. Evaluation The score is in [0.0, 1.0]. Higher is better. A record is correct only if all three decoded prediction strings exactly match their reference strings, including spelling, accents, case, spacing, and word order. JSON whitespace and character-escape style do not matter after parsing. No text normalization is applied during scoring. Let c_i be 1 for a completely correct record and 0 otherwise. For every group g, compute a_g = sum(c_i for i in g) / number_of_rows_in_g. The final score is sum(a_g for g in G) / number_of_groups. Every group has equal weight, regardless of its row count. The score is returned as a floating-point number without explicit rounding. An exact submission reaches 1.0. An all-empty analysis reaches 0.0. Partial credit comes from correctly completed records within each group; a record with only a correct spelling or only a correct lemma pair is incomplete and earns 0. The metric estimates the fraction of concordance entries that can be accepted without correcting either their surface text or lexical index key. Not allowed External corpora, pretrained weights, pretrained language tools, external dictionaries, remote APIs, source-to-answer lookup, manual test annotation, and hard-coded answers for individual test IDs are prohibited. Train models, tokenizers, dictionaries, normalization rules, and other fitted components using only the provided training rows. Inspecting and correcting your training-derived software or rules is allowed; manually entering test labels is not. Do not fit or adapt anything to the unlabeled test corpus, pool evidence across test examples, or infer labels from ID values, file ordering, or group identifiers. A frozen model must predict each test row from that row's text independently. Use groups to construct training-side validation. &nbsp;
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Contextual Khmer-to-Myanmar News Translation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74gdasesyzkm1544vjr658ax8dwsbb
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat dongfuhan's score of 0.446!

Full challenge description from page:

> Overview Translate a Khmer news sentence into Myanmar, using neighboring Khmer sentences to resolve references and terminology. Generate the translation freely; there is no candidate list or answer retrieval corpus. Dataset train.csv / test.csv: task_id (string), source_text (string), source_context_json (JSON string array). train_labels.csv: task_id, translation (Myanmar string). sample_submission.csv: the same output schema. There are 1,200 training pairs and 300 test pairs. Context contains up to two preceding and two following sentences, plus the focal sentence, in native article order. Only the focal sentence should be translated. Evaluation articles are disjoint from training. An evaluation article containing a verbatim training sentence was excluded; blank translations and duplicate pairs were removed. A fixed hash ordering selects the compact subset within those existing partitions; the retained sentences keep their original source-side context. The texts are translated news, not naturally authored Khmer–Myanmar parallel documents. Some translations are awkward or inaccurate, and one reference cannot capture every valid wording. Public pretrained models may have encountered this established corpus. Difficulty certification must account for that risk. Submission Submit a UTF-8 CSV with exactly task_id,translation in that order and one row for each test ID: task_id,translation example_1,မြန်မာဘာသာပြန်ဆိုချက်။ example_2,အခြားဘာသာပြန်ဆိုချက်။ Translations may contain quoted commas/newlines according to CSV rules. Empty predictions are allowed and earn no matching n-grams. The maximum prediction length is 100,000 characters per row. Evaluation Use corpus chrF2 on a 0–1 scale: character n-gram orders 1–6, whitespace removed, case and punctuation preserved. For each order, pool clipped n-gram matches and predicted/reference counts across sentences. Average precision P and recall R over orders with nonzero counts on both sides, then compute 5 × P × R / (4 × P + R). If there are no matches, the score is 0. A perfect reference copy scores 1. chrF2 supports scripts where whitespace is not a reliable word boundary and gives recall twice the F-score importance of precision. IDs are aligned independently of row order. Invalid file schemas or ID sets are rejected; non-string/overlength prediction cells are treated as empty. Expected Approach Adapt a compact multilingual sequence-to-sequence model that supports both scripts, using only the supplied parallel examples. Translate the focal sentence, with neighboring source sentences used as context rather than additional output targets. For an efficient implementation: Tokenize once and mark the focal sentence explicitly. If an input must be shortened, retain the full focal sentence before trimming distant context. Batch by token length and use a short fine-tuning run or parameter-efficient adaptation. Benchmark a training step and a generation batch before setting the epoch count. Begin with greedy decoding or a small beam. Choose output-length limits from training translations and check for truncated outputs. Use held-out training pairs for chrF2-based early stopping, keep overlapping source contexts together where identifiable, and write only the focal translation. What Not To Use No external parallel data, source-translation lookup, held-out answer tables, hosted translation services, manual translation of test examples or challenge-specific pretrained checkpoints. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The complete solution must finish within 60 minutes end to end, including data loading, preprocessing, feature extraction, training or adaptation, validation, inference, structured decoding and submission writing. This is a total execution limit, not a separate allowance for each stage. The platform may terminate execution at the limit; use elapsed-time checks and retain the best completed model so that a valid submission is written before the deadline. Start with a small end-to-end run and write a valid full-test submission early. Use a wall-clock timer from process start, avoid exhaustive searches and large ensembles, and reserve at least the final 10 minutes for inference and submission checks; increase this reserve if measured throughput requires it. Cache encoder outputs only while the encoder is frozen. &nbsp;
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Document-Scoped Translation Evidence Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74svk9w2e7h2c1nbda0491458eacny
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview Find where an English statement is translated within a bank of Czech sentences from the same document, then recover its token-level translation evidence. The corresponding Czech sentence is not identified. Alternatives share the document's topic and have similar lengths, requiring translation retrieval before precise word correspondence. This supports bilingual document inspection when sentence correspondence has been lost. Returning a sentence ID alone is insufficient: identify supporting words and distinguish definite from possible evidence. Neighboring English sentences provide context for terminology and references. Task Predict [candidate_index,english_index,czech_index,strength] records for the query sentence in english_tokens. All indices are zero-based: candidate refers to this row's Czech bank, and token positions refer to the query sentence and selected Czech candidate. Strength is sure or possible, following the human annotations. Many-to-many links are allowed; unaligned words need no output. Each bank contains one retained native translation and real same-document alternatives, not generated text. Return the query's links, not alignments for neighboring English sentences. Candidate IDs have meaning only within one row. Data There are 1,200 training queries from 56 documents and 300 test queries from six different documents. Every query represents a distinct native sentence pair. Context and bank sentences recur among queries in a document; they are not additional independent examples. train.csv and test.csv have exactly task_id,group_id,english_context,english_tokens,czech_bank. task_id: unique string beginning task_. group_id: document-group string beginning doc_; use for validation splitting. english_context: JSON array of 1–3 sentence token arrays, each containing 2–100 nonempty strings. english_tokens: JSON array of 2–100 nonempty query tokens; this sentence also occurs in english_context. czech_bank: JSON array of 4–8 distinct sentence token arrays, each containing 2–100 tokens. train_labels.csv and sample_submission.csv: task_id,links; identifier and JSON array of four-field evidence records. Entire source documents are assigned to one partition before constructing banks or selecting queries. No bank uses sentences from the other partition. Exact bilingual pairs are deduplicated and an audited cross-document near-repeat is excluded. Candidate order is independently shuffled for each query and does not preserve source order. The native annotations describe sentence-level word correspondence, not newly annotated cross-sentence discourse relations. This task combines document-scoped retrieval with those original links; no semantic links are invented. Context need not be necessary for every query. Limited document diversity, subjective possible links and a single reference constrain generalization; defensible alternative analyses may receive no credit. Evaluation Micro F1 over complete (task_id,candidate_index,english_index,czech_index,strength) matches: score = 2 × TP / (2 × TP + FP + FN) Counts are pooled across queries. A match requires the right translation location, both token positions and annotated strength. This measures correctly localized translation evidence: a sentence ID without word evidence earns no credit, while links to a wrong candidate create false positives. Partial recovery earns partial credit. This is ordinary F1, without score transformations or a separate retrieval bonus. Scores range from 0 to 1, higher is better; perfect predictions score 1. Empty predictions score 0 on nonempty references. If both sets are empty, the defined score is 1. Indices outside a row's actual sentence/token bounds cannot match. CSV row and evidence-list order do not affect scoring. Submission Format Submit UTF-8 CSV with exactly task_id,links, in that order, once per test ID: task_id,links task_example,"[[2,0,1,""sure""],[2,3,4,""possible""]]" Use [] or at most 10,000 distinct four-entry records. Candidate indices must be integers 0–7, token indices integers 0–99, and strength a permitted string. Use indices valid for the row. JSON is limited to 200,000 characters. Invalid payloads or duplicate records contribute no true positives, all reference links as false negatives, and one false positive. Wrong, reordered or duplicate headers and missing, extra or duplicate task IDs reject the file. Expected Approach Use a multilingual encoder to retrieve candidate translations, then train a contextual token-pair classifier for sure, possible and no-link. Preserve word-to-subword mappings. Train with same-document candidate negatives and validate by group_id; measure retrieval recall separately from alignment F1. For an efficient implementation, cache tokenization and frozen sentence embeddings, batch the small banks and align only the best few candidates. Use short adaptation runs, mixed precision and vectorized token-pair scoring. Keep a valid full-test submission early and reserve the final ten minutes for inference and checks. What Not To Use General-purpose pretrained language models are allowed. Learn task-specific parameters only from supplied training data. Do not use external alignment annotations, source copies, challenge-specific trained checkpoints, hosted APIs, manual test annotations or answer lookup tables. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The maximum end-to-end runtime is 90 minutes, including data loading, training or adaptation, inference, structured decoding, validation, and submission writing. This is a total execution limit, not a separate allowance for each stage. The platform may terminate execution at the limit; use elapsed-time checks and retain the best completed model so that a valid submission is written before the deadline.
> 0 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Matching Translations of Shuffled Document Regions

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74er0zmyja4ce7kxknzfx0ys8e8zhw
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview A translated document is more than a collection of sentence pairs. Headings establish context, table cells depend on neighboring rows and columns, captions refer to nearby content, and short regions such as dates, amounts, article numbers, and list markers are often ambiguous in isolation. Each case presents two unordered collections: source-language regions from one structured document; and a larger pool of target-language candidates. Exactly one target candidate is the translated counterpart of each source region. The remaining candidates are plausible distractors. For every source region, participants must predict: its target candidate_id; and an order_key that reconstructs the document's reading sequence. The challenge combines learned cross-lingual matching, relational layout reasoning, global one-to-one assignment, and set-to-sequence reconstruction. Some longer source regions contain a [GAP] marker where a short span is unavailable, requiring document context and assignment constraints to supplement the surviving words. Strong performance requires solving these parts together. A candidate match receives the most joint credit when it is also placed correctly among its neighbors. Why the Challenge Is Difficult Candidate pools contain approximately four candidates per source region. Distractors are confusable with real counterparts rather than merely random text in the same language. They can resemble the likely translation in: topic; form; length; numbers; punctuation; and document function. Candidate-side layout labels are not provided. Candidate identifiers and list positions are opaque and independently shuffled. Source regions are also shuffled. Their geometry uses a case-local frame whose orientation and axes are not consistent between cases. Relative spatial relationships remain informative, but a fixed global rule such as sorting by increasing box_y0 is unreliable. Multi-column pages, tables, side notes, headers, footnotes, and vertical regions create additional ambiguity. Evaluation cases are separated from training at a document-family level. Related versions of a document do not appear on both sides of the split. Learning Requirement An admissible solution must use at least one learned machine-learning component that contributes materially to the submitted predictions. Suitable components include: multilingual encoders; fine-tuned rerankers; neural pair classifiers; learned assignment models; graph neural networks; pointer networks; and set-to-sequence Transformers. TF-IDF, BM25, edit distance, character counts, fixed dictionaries, hand-written sorting rules, and nearest-neighbor lookup may be used as auxiliary signals or diagnostics, but they may not be the central prediction method. Compute and Runtime Limits Hardware: one NVIDIA A10G GPU. End-to-end runtime limit: 90 minutes. Internet access and remote inference services are unavailable. All preprocessing, fitting, inference, assignment, ordering, and submission writing must finish within the runtime limit. Publicly released pretrained open-weight models are allowed when their licenses permit competition use and all required files are locally available. Training or fine-tuning on the supplied training partition is allowed. External task-specific labels, private translations, reconstructed evaluation answers, and manual evaluation-set labeling are prohibited. Public Files The public package contains: train.csv; train_targets.csv; test.csv; sample_submission.csv; and cases/. Source-Region Tables train.csv and test.csv contain one row per source-language region. Rows sharing a case_id must be solved together. The columns are: sample_id: globally unique source-region identifier; case_id: identifier shared by all source regions in a case; case_path: relative path to the case's candidate-pool JSON; source_language: language code for source_text; target_language: language code for candidate texts; source_text: source-language region text, potentially containing one [GAP] span; layout_code: anonymous, case-local source-region role code; box_x0, box_y0, box_x1, box_y1: rectangle in the case-local coordinate frame; vertical: vertical-text indicator; source_position: position in the shuffled public row order; block_count: number of source regions in the case; and candidate_count: number of target candidates in the case. The feature tables contain no candidate answer, order answer, gold rank, or private aggregation field. Candidate-Pool Files Each case_path points to a JSON object: { "case_id": "case_...", "target_language": "de", "candidates": [ { "candidate_id": "candidate_...", "target_text": "..." } ] } Candidate IDs are case-local choice labels. Their characters and array positions do not encode: correctness; source position; or reading rank. Every gold candidate is used exactly once, while distractors are unused. Training Targets train_targets.csv has exactly the submission schema: sample_id,candidate_id,order_key For training rows: candidate_id identifies the translated counterpart; ascending order_key gives the reference reading sequence. Only relative order matters. Absolute magnitude and spacing do not. Submission Use sample_submission.csv as the exact schema: sample_id,candidate_id,order_key Requirements: include every supplied sample_id exactly once; keep the three columns in exactly the shown order; provide a nonblank candidate_id from the row's case pool; provide a finite order_key in [-1000000, 1000000]; and interpret ascending order_key as earlier reading order. Equal keys are allowed, but tied pairs receive only half pairwise-order credit. sample_id is used solely as a deterministic tie-breaker when a discrete sequence is required. Reusing a candidate is syntactically valid, but it cannot form the correct one-to-one assembly. The private answers.csv begins with the same three columns in the same order and may append private grading columns. Those appended columns are not submission targets. Evaluation Scoring is case-based and ranges from 0.01 to 100. A perfect submission receives 100. Malformed submissions receive the floor. Candidate Alignment For a case with n source regions, let m_i = 1 when row i predicts its exact gold candidate and 0 otherwise: A = mean_i(m_i) Reading Order For every unordered source-region pair, compare the sign of the predicted order-key difference with the sign of the gold-rank difference: correct direction: 1; tied prediction: 0.5; reversed direction: 0. Their mean is P. Sort rows by (order_key, sample_id). Let D be the fraction of directed gold-adjacent pairs that are also adjacent in this predicted sequence. O = 0.70 P + 0.30 D For a one-region case, O = 1. Joint Assembly Convert predicted order keys to stable ranks. For row i, let r_i be its gold rank and r_hat_i its predicted rank: J_row = mean_i(m_i / (1 + |r_hat_i - r_i|)) For each directed pair of consecutive gold regions, edge credit is: 1.0 when both candidate matches are correct and the pair is consecutive in the predicted sequence; 0.35 when both matches are correct and remain in the right relative direction but are not consecutive; and 0 otherwise. The mean edge credit is J_edge, and: J = 0.55 J_row + 0.45 J_edge This rewards locally coherent translated-document assembly, not just isolated correct rows. Case Score S = 0.45 A + 0.20 O + 0.35 J All components lie in [0,1]. Balanced Aggregation Cases are assigned to private aggregation strata defined by: language direction; and difficulty level. Let: S_g be the mean case score in stratum g; n_g be the number of evaluation cases in stratum g; K = 10 be the support cap. The aggregation weight for stratum g is: w_g = min(n_g, K) The final aggregate is: aggregate = sum_g(w_g * S_g) / sum_g(w_g) and the leaderboard score is: score = clip(100 * aggregate, 0.01, 100) This support-capped aggregation is designed to prevent both extremes: a very common language/difficulty group cannot dominate simply because it contains many cases; and a tiny one- or two-case group does not receive the same total influence as a large, well-supported group. For example, a stratum with one case receives weight 1, a stratum with five cases receives weight 5, and any stratum with ten or more cases receives weight 10. Private grouping fields affect aggregation only. They never change a row's answer. The preparation pipeline also performs a leakage-safe, best-effort support repair by moving only whole document families when a scored test stratum is extremely small. Family-disjointness is never broken to improve balance. Modeling Directions A strong solution can encode source and candidate text with a multilingual learned model, then rerank difficult pairs with a cross-encoder or sequence-to-sequence likelihood model. Global assignment should be solved jointly so one attractive candidate is not selected repeatedly. Ordering benefits from a learned pairwise precedence model or document graph over: region geometry; source semantics; role codes; and neighboring blocks. Because coordinates are case-local, geometry should be normalized and interpreted relationally rather than through a universal axis rule. The stages can exchange information. Confident translation matches can act as semantic anchors for neighboring regions, while a coherent sequence can disambiguate: repeated numbers; formulaic headings; and short table entries. Leakage Control and Local Validation The official split is document-family disjoint. Related versions of a source document remain entirely on one side of the split. This prevents a solver from receiving one translated/layout variant of a document during training and a closely related version during evaluation. When creating a local validation set, participants should group by case_id or by document-level case membership rather than randomly splitting individual source-region rows. A row-level split leaks neighboring regions from the same document case across local train and validation partitions and can substantially overestimate generalization. The preparation pipeline preserves family-level separation even when it adjusts test-stratum support. Rebalancing is performed only by moving complete document families. Why the Aggregation Uses a Support Cap Pure micro-averaging would allow frequent language directions and easy, common strata to dominate the score. Pure macro-averaging of every nonempty direction/difficulty cell creates the opposite problem: a stratum containing one case would receive the same total influence as a stratum containing dozens of cases. The support-capped rule lies between those extremes. It increases a stratum's influence with actual evaluation support until K = 10, then stops increasing it. This makes rare groups matter without allowing a handful of cases to control a large fraction of the leaderboard. Limitations This finite benchmark does not represent every: language; script; document genre; page convention; or translation style. Some short regions can remain genuinely ambiguous without full page imagery. The task evaluates recovery of the supplied correspondence and annotated order, not every linguistically acceptable translation or defensible reading sequence. Target texts are fixed candidates. A newly generated translation cannot be submitted directly; this is retrieval and structured assembly rather than open-ended generation. Aggregate performance may hide weakness on: a particular language direction; a rare role; or a complex layout. Analysis by case type is therefore encouraged. Summary Matching Translations of Shuffled Document Regions asks a model to rebuild a translated document from two shuffled sets. Success requires: learned cross-lingual discrimination among hard candidates; reconstruction of reading order in an unfamiliar coordinate frame; and globally consistent one-to-one assembly. High scores require both correct matches and coherent local sequence structure. The final metric preserves language/difficulty balancing while using support-capped stratum weights so that neither very large groups nor a handful of rare cases can dominate the result.
> 0 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Borrowed-Word Source-Form Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70bqta0fpt41s4p640g1ptah8e6y3h
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview Reconstruct the source-language word from which a borrowed word was recorded as originating. The input gives the borrowed spelling, its language, the source language, and a meaning when available. Generate the normalized source spelling: there is no candidate list or fixed set of answer classes. For example, the Irish word cúisín is paired with the English source form cushion. This is cross-language word reconstruction, not a choice between letter-coded candidates. Copying the input is insufficient because retained pairs differ in spelling. Records come from published, dictionary-derived etymological links. Labels describe the recorded direct borrowing relationship, not a claim that all historical origins are certain or exhaustively documented. Missing meanings and irregular spelling changes make some examples genuinely ambiguous. Dataset All files are UTF-8 CSVs; the source-form target is an ordinary string. | File | Contents | |---|---| | train.csv | 2,723 labeled records: case_id,recipient_language,recipient_word,meaning,donor_language,donor_form, in that order. | | test.csv | 470 records with the same five input columns and no target. | | sample_submission.csv | Every test ID with a normalized copy of the recipient word; columns case_id,donor_form. | Private answers.csv contains exactly case_id,donor_form. No external files or candidate catalog are needed. | Column | Type | Meaning | |---|---|---| | case_id | string | Opaque example identifier. | | recipient_language | string | Language using the borrowed word. | | recipient_word | string | Recorded borrowed spelling, with original capitalization and diacritics. | | meaning | string | Source gloss of at most 240 characters, or not_recorded. This is an input sentinel, not an answer. | | donor_language | string | Language in which the source word must be reconstructed. | | donor_form | string, target | Literal prefix form: followed by the normalized source spelling, containing 2-35 letters. | Spelling Convention Normalize a source spelling by applying Unicode casefolding, then NFKD decomposition, then retaining only characters for which Python str.isalpha() is true. This removes combining accents, punctuation, and spaces. For example, CUSHION becomes cushion. It is an orthographic normalization, not phonetic transcription or translation. Prepend form: to the result. The prefix is required for CSV-safe serialization and is excluded from spelling comparisons. Every example has a recorded source form; there is no absent-donor class, blank target, or NONE answer. Construction and Separation Cases have one normalized direct donor within the specified source language. The input and source language differ. The retained words use Latin-script spellings; normalized input/source similarity lies between 0.25 and 0.85 under the source-selection rule. Cases also have nearby dictionary spellings, retaining the previous difficult lexical cohort without displaying those alternatives. Explicit source-word mentions in supplied glosses are filtered. Missing or overlong glosses become not_recorded. Canonical source spellings are selected consistently before normalization. Connected borrowing families remain in one split. The previous version's family assignment is preserved; removing the public candidate catalog does not move training families into test. Dictionary omissions, extraction errors, broader cognate relationships, and pretrained exposure remain limitations. Hashing does not prevent external source lookup. | Coverage measure | Training | Test | |---|---|---| | Cases | 2,723 | 470 | | Distinct normalized target strings | 2,043 | 355 | | Cases without a recorded gloss | 2,575 | 441 | | Observed target length, excluding prefix | 3-16 | 4-14 | Repeated source spellings within a split can be associated with different borrowing recipients. The allowed output length is broader than the observed range; it is not a fixed answer vocabulary. Submission Format Write ./working/submission.csv with the exact ordered columns case_id,donor_form. Both are strings. Include every test ID once. Rows may be reordered; extra, missing, duplicated, null, malformed, or unknown IDs and extra, missing, duplicated, or reordered columns reject the file. Real labeled training examples: | case_id | recipient_word | donor_language | donor_form | |---|---|---|---| | case_667690e4cc37ff81d409a13c | cúisín | English | form:cushion | | case_73c2eb60a74d8b450dde2c9f | lider | English | form:leader | Submit only the ID and target, using test IDs. The target must begin with form: and contain 2-35 lowercase letters afterward, for 7-40 total characters. Lists of guesses, blank values, extra prefixes, explanations, and punctuation in the spelling are invalid. Use the normalization convention above. Evaluation Metric: Source-Form Reconstruction Score. Minimum score: 0.0. Maximum score: 1.0. Higher is better. Score = 0.70 * WordExactScore + 0.30 * CharacterScore. For N evaluated cases, let y_i be the reference spelling and p_i the predicted spelling, after removing the required prefix. WordExactScore = sum(I(p_i = y_i)) / N. Every case has equal weight. Let d(y_i,p_i) be character-level Levenshtein distance with unit-cost insertion, deletion, and substitution. A valid prediction receives s_i = 1 - d(y_i,p_i) / max(len(y_i),len(p_i)). CharacterScore = sum(s_i) / N. Characters are Unicode code points; there is no word-level semantic matching. The 70% exact term rewards complete source-word recovery. The 30% character term gives bounded credit for partially correct spelling changes without allowing close copying to dominate. A malformed cell receives zero in both components and remains in N. Invalid reference targets raise an error. Length checks run before dynamic programming; references are never clipped. Validation Exact answers score 1.0. The copy-input sample scores approximately 0.159. These are local checks, not a promised agent-score range. Old candidate-selection scores are not comparable to this generation metric. Modeling A compact character-level encoder-decoder conditioned on the two language names is a suitable starting point. Train on the supplied word pairs, and add gloss features when present. A simple baseline learns reusable prefix/suffix edits within language pairs. Validate by lexical family and compare against copying the normalized input. Use 10 CPU cores, 62.5 GiB RAM for 90 mins, for the complete pipeline. Locally runnable pretrained resources are allowed subject to platform rules. Validate using training packets; external inference services are not required. What Not To Use Use public training data and local pretrained resources permitted by the platform. Do not retrieve evaluation source words through external dictionaries, source-text search, answer tables, or hidden-annotation-trained models. Do not use IDs, hashes, filenames, row order, or file sizes as predictive shortcuts. External inference services, other participants' outputs, and evaluator manipulation are prohibited. Legitimate content-based learning is allowed. &nbsp;
> 0 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Semantic Arguments with Syntactic Evidence

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75a7ywewp45sk18hn5bengrn8e3h41
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview Recover role-labelled predicate–argument links and their connecting dependency paths in Slovenian sentences. The objective is joint semantic–syntactic reconstruction under the annotation conventions demonstrated in training. Each output record must support a structural query specifying both a semantic relation and its syntactic route—for example, finding an actor attached through a particular sequence of dependency relations. Recovering the role alone does not answer that full query. Dataset There are 1,200 training sentences and 300 test sentences. All sentences of a document stay in one split; exact repeated sentence inputs are excluded. A fixed hash ordering selects the compact subset within those partitions without moving any document across the split. Topics and grammatical constructions can recur across documents. The independent sample count is the document count, not the number of argument links. The target contains native semantic links whose endpoints are tokens and have a connecting path in the annotated syntactic tree. Non-token endpoints and disconnected cases are excluded. At least two retained semantic links occur per sentence. Training and test targets follow the same role and dependency conventions. Each sentence has one reference analysis; a linguistically defensible alternative can therefore lose credit. The score measures reconstruction within this annotation framework, not unrestricted semantic understanding. Submission Submit UTF-8 CSV with exactly task_id,arguments, in that order. arguments is a JSON array of at most 500 objects: predicate, argument: zero-based token indices. role: one semantic role from schema.json. path: distinct token indices along the shortest undirected dependency-tree path, ordered from predicate to argument. It starts and ends at those endpoints. syntax: one label for each path step. down:REL follows a dependency head to its dependent; up:REL follows a dependent to its head. REL is the native Universal Dependencies relation, including any subtype. The native role meanings are: ACT actor; PAT patient; REC receiver; ORIG origin; RESLT result; TIME time; DUR duration; FREQ frequency; LOC location; SOURCE starting location; GOAL destination; EVENT event; AIM purpose; CAUSE cause; CONTR contradiction; COND condition; REG regard; ACMP accompaniment; RESTR restriction; MANN manner; MEANS means; QUANT quantity; MWPRED multiword predicate; MODAL modal construction; PHRAS phraseme. Empty arrays are permitted. Include every test ID once. task_id,arguments example,"[{""predicate"":2,""argument"":0,""role"":""ACT"",""path"":[2,0],""syntax"":[""down:nsubj""]}]" Evaluation Micro F1 scores exact (predicate, argument, role, path, syntax) matches. This measures recovery of complete, queryable relations: wrong endpoints select different participants, a wrong role changes their semantic relation, and a wrong path or dependency label changes the structural query the record satisfies. A correct ACT link with an incorrect dependency route is a role-labelling success but not a complete reconstruction, so it receives no tuple credit. For fixed endpoints in the reference dependency tree, the connecting path is unique. Exact matching therefore tests a defined structured target, rather than requiring one arbitrary wording of an explanation. The single reference is appropriate for learning and reproducing this shared annotation framework on held-out documents. It does not establish that rejected alternative analyses are linguistically wrong, or that the score measures role-only accuracy or downstream utility in every application. Partial role/path scores would answer different diagnostic questions; the ranking uses joint correctness because both parts are required by the stated structural-query objective. Micro aggregation gives each attachment equal weight across sentences; F1 balances missing attachments against spurious ones. TP counts complete matching records, FP unmatched predictions and FN unmatched reference records. score = 2 × TP / (2 × TP + FP + FN) Counts are pooled across sentences. Identical duplicate predictions count once. Scores range from 0 to 1, with gold at 1; a zero denominator returns 1. Malformed row content contributes all reference records as FN and max(1, reference_record_count) FP. Well-formed incorrect records contribute FP. Wrong headers or ID sets are rejected; row order has no effect. Expected Approach Use a shared compact token encoder with separate heads for dependency attachments and semantic roles. Predict a dependency tree, then recover each selected predicate–argument path deterministically from that tree. For an efficient implementation: Derive supervised dependency edges from the supplied training paths. Unobserved edges are unlabeled, not confirmed negatives; the paths do not expose complete reference trees. Cache tokenization and source-token alignment. Batch sentences by length and score likely predicate–argument pairs before more expensive path construction. Enforce an acyclic dependency tree during decoding. Traverse each selected path from predicate to argument and generate the corresponding directional syntax labels. Tune attachment thresholds on held-out training sentences. Validate endpoint indices, distinct path tokens and one syntax label per path step. What Not To Use GPU training and general-purpose pretrained models are allowed. No external annotated treebanks or role corpora, source copies, challenge-specific checkpoints, hard-coded answers, hosted APIs, manual test annotation. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The complete solution must finish within 60 minutes end to end, including data loading, preprocessing, feature extraction, training or adaptation, validation, inference, structured decoding and submission writing. This is a total execution limit, not a separate allowance for each stage. The platform may terminate execution at the limit; use elapsed-time checks and retain the best completed model so that a valid submission is written before the deadline. Start with a small end-to-end run and write a valid full-test submission early. Use a wall-clock timer from process start, avoid exhaustive searches and large ensembles, and reserve at least the final 10 minutes for inference and submission checks; increase this reserve if measured throughput requires it. Cache encoder outputs only while the encoder is frozen. &nbsp;
> 0 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Behavior Annotation Gap Repair from Pose Trajectories

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74y8p3ny2h8cq812b3pfx3hh8c1mg2
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview Behavior researchers annotate long recordings with intervals such as locomotion, investigation, digging, and grooming. Annotation tools can leave short gaps after an interrupted pass, a disputed interval, or a partial export even when the tracked body landmarks remain available. Repairing such a gap requires more than assigning one action to an isolated clip: the missing interval may contain background motion, several events, or a behavior that starts or ends at the gap boundary. Each case contains 180 pose steps spanning twelve seconds. Expert annotation survives for the first and final four seconds. The middle four seconds, represented by bins 0 through 59 in the required output, are hidden. Reconstruct every behavior segment inside that gap as an ordered event program. This is sequence reconstruction rather than clip classification. A valid answer may contain zero, one, or several non-overlapping event atoms, and both the behavior identity and temporal boundaries matter. Pose Evidence pose_sequence is a JSON list containing exactly 180 rows. Each row has 21 positions in this fixed order: left_ear_x, left_ear_y, left_ear_confidence right_ear_x, right_ear_y, right_ear_confidence nose_x, nose_y, nose_confidence body_center_x, body_center_y, body_center_confidence left_hip_x, left_hip_y, left_hip_confidence right_hip_x, right_hip_y, right_hip_confidence tail_base_x, tail_base_y, tail_base_confidence Coordinates are floating-point values in a case-local spatial frame. Spatial orientation, offset, scale, tracking-confidence calibration, and sampling phase can differ between cases, so an absolute coordinate or confidence threshold is not a stable shortcut. A missing coordinate is represented by JSON null; its confidence value remains available. Pose rows 0 through 59 align with left_context. Rows 60 through 119 form the hidden gap. Rows 120 through 179 align with right_context. Event Programs An event atom has the form behavior:start-end. Allowed behavior labels are: dig grooming investigate locomote start and end are inclusive integer bins from 0 through 59. Multiple atoms are separated by semicolons and must be sorted by start bin. Segments cannot overlap. Background bins are omitted. Example: locomote:3-11;investigate:26-34;dig:48-52 The example describes three behavior intervals and background everywhere else. An empty string represents an all-background interval. left_context and right_context use the same 60-bin event-program grammar, but their bin numbers are local to their own four-second context intervals. Dataset The public dataset contains three CSV files: train.csv: 2,046 labeled gap-repair cases from 30 recording sessions. test.csv: 418 unlabeled cases from eight held-out recording sessions. sample_submission.csv: one structurally valid example prediction for every test case. No recording session appears in both training and test. Public case identifiers do not expose recording names, source frame numbers, or source partition names. train.csv Columns case_id (string): anonymous unique training-case identifier. pose_sequence (JSON string): 180 by 21 pose and confidence sequence described above. left_context (string): surviving event program immediately before the hidden gap. right_context (string): surviving event program immediately after the hidden gap. target_program (string): expert behavior intervals inside the hidden 60-bin gap. test.csv Columns case_id (string): anonymous unique test-case identifier. pose_sequence (JSON string): 180 by 21 pose and confidence sequence. left_context (string): surviving event program before the gap. right_context (string): surviving event program after the gap. sample_submission.csv Columns case_id (string): test identifier copied from test.csv. predicted_program (string): predicted event program for the hidden interval. Evaluation The score is bounded in [0, 1], where higher is better: Score = 0.70 * FrameBehaviorMacroF1 + 0.30 * TypedBoundaryF1 The weights sum to 1.00. The two components measure behavior occupancy and boundary placement respectively; neither component is repeated in another hidden track. FrameBehaviorMacroF1 The grader expands every target and prediction into 60 frame labels. For each of the four behavior labels it computes standard F1: F1 = 2 * TP / (2 * TP + FP + FN) Background is excluded from the macro average, so predicting no events cannot obtain a large score from empty bins. If a behavior has neither true nor predicted frames, it is omitted. If it has false positives or false negatives, its F1 is included. The component is the mean F1 over represented behavior labels. TypedBoundaryF1 Every event contributes one typed start boundary and one typed end boundary. A predicted boundary matches an unmatched target boundary only when: the behavior label is identical; both are start boundaries or both are end boundaries; and their bin positions differ by at most two. Matching is one-to-one. After pooling boundary counts across all cases: Precision = TP / (TP + FP) Recall = TP / (TP + FN) TypedBoundaryF1 = 2 * Precision * Recall / (Precision + Recall) Malformed generative rows are treated as all-background predictions for those cases. They receive no positive behavior or boundary credit. Structural CSV violations such as missing required IDs, duplicate IDs, or extra columns raise an error. Submission Submit a CSV with exactly two columns. Header: case_id,predicted_program Example row: POSETST_1a2b3c4d5e6f70,locomote:3-11;investigate:26-34 Every required test case_id must appear exactly once. Additional rows outside the scored answer partition are ignored after required-ID and duplicate-ID validation. Allowed And Prohibited Methods Allowed Train CPU-compatible temporal, sequence, sparse-feature, tree-on-learned-feature, or constrained-decoding models using the supplied public files. Derive translation- and rotation-aware kinematic features from the supplied pose sequence. Use the visible left and right event contexts as conditioning evidence. Build session-like grouped validation partitions from public examples without attempting to recover source identities. Prohibited Downloading or matching against the original recordings, pose tracks, or annotation files. Recovering source session names, frame numbers, or source partition membership. Hardcoding test programs, manually annotating test cases, or using an external annotation lookup system. Exploiting case IDs, row order, sample-submission values, or private-answer assumptions. &nbsp;
> 0 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Bacterial Future Lineage Trees

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dafkzg2srf4e178xvze2nbh8e6msy
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat douglas's score of 0.576!

Full challenge description from page:

> Background Understanding cellular dynamics requires observing how individual cells grow, transition between biological states, and divide over time. While static image segmentation identifies cells in a single moment, forecasting a cell's biological future—mapping its precise state changes and division events across subsequent frames—remains a complex challenge. This requires models capable of extracting spatio-temporal dynamics from short microscopy histories to predict future cellular life-cycle trees. Overview Use a brief microscopy history (four frames) to predict the future life-cycle tree of a specifically marked root cell. You must forecast its state in each of the next twelve future frames, including the states and division times of any descendant cells born during that interval. The final observed frame provides a binary anchor mask identifying the root cell you must track. Nearby cells provide visual context but are not additional forecast roots. Because a short image history may not uniquely determine an actual biological future, this task measures your ability to predict the most likely deterministic future tree based on the provided temporal context. This is a GPU-only sequence-to-sequence challenge. All learned model training, structured decoding, and neural inference must execute within a single offline session. The planning envelope provides one NVIDIA A10G and a strict 90-minute solution-run budget. Dataset Information (Public Files) All assets necessary for training and evaluation are provided in the public directory. The input arrays are fixed-crop normalized histories with moderate Gaussian noise and intensity variation applied. +-----------------------+--------------------------------------------------------------+ | File / Directory | Purpose | +-----------------------+--------------------------------------------------------------+ | clips/ | Directory of .npy arrays containing 4-frame input histories. | | anchors/ | Directory of .png binary masks selecting the root cell. | | train.csv | 3,063 input rows for training. | | test.csv | 708 evaluation inputs (balanced changing/static futures). | | train_answers.csv | Ground-truth future lineage trees for the training set. | | train_groups.csv | Recording-group assignments for creating validation splits. | | sample_submission.csv | Format-example rows demonstrating the required output. | +-----------------------+--------------------------------------------------------------+ Feature Schema train.csv and test.csv +--------------+--------+--------------------------------------------------------------+ | Column | Type | Description | +--------------+--------+--------------------------------------------------------------+ | forecast_id | String | Opaque unique identifier for the example sequence. | | clip_path | String | Relative path (clips/.npy) to a Float16 NumPy array of | | | | shape (4, 128, 128) representing time, row, and column. | | anchor_path | String | Relative path (anchors/.png) to a Grayscale 128x128 mask.| | | | Values 0/255 mark background/target-cell in the 4th frame. | +--------------+--------+--------------------------------------------------------------+ train_answers.csv and train_groups.csv +----------------+--------+------------------------------------------------------------+ | Column | Type | Description | +----------------+--------+------------------------------------------------------------+ | future_lineage | String | (train_answers) The encoded biological future lineage tree.| | group_id | String | (train_groups) Opaque recording-sequence group. Examples | | | | sharing a group share a biological recording sequence. | +----------------+--------+------------------------------------------------------------+ Split design and validation A group is one complete microscopy recording sequence: all cells, descendants and temporal windows from that sequence belong to the same split. The held-out recording sequences are disjoint from the training sequences. Training group IDs in train_groups.csv are opaque identifiers for these complete recordings, not individual cells or clips. Keep each complete group in a single fold when validating. This separation prevents the same tracked cell, its relatives, overlapping image context, or later observations from the same recording appearing on both sides of the training/evaluation boundary. Observation windows use four frames and targets use only the following twelve frames; windows advance by sixteen frames. Crop positions and normalization use observed frames only. Shared biological state patterns across different recordings can still occur, so this design measures generalization to held-out recordings rather than independence of all biological mechanisms. The 708 evaluation examples contain 354 changing and 354 static futures. This balance is an evaluation design choice and does not estimate natural event prevalence. Target Tree Grammar Your prediction (future_lineage) must be a string that rigidly follows this biological grammar: 1. State Characters (1 character = 1 future frame): D — Dormant spore. R — Ripening spore. O — Outgrowth (including vegetative bacteria). 2. Division Syntax: A node starts with its consecutive state characters. If the cell divides within the forecast horizon, append (left|right), where left and right are the two daughter subtrees. The parent cell ceases to exist immediately before its daughters start. Both daughters begin in the same next frame, though their subsequent states may diverge. Daughter ordering (left vs. right) is immaterial and will be canonicalized during grading. 3. Biological & Structural Constraints: Every root-to-leaf path must contain exactly 12 state characters. States cannot regress (they must follow the strict D $\rightarrow$ R $\rightarrow$ O order). Only outgrowth cells (O) divide, and daughter nodes always start in O. A root that divides immediately after the observed clip may have zero state characters before its first opening parenthesis. Trees contain at most 63 nodes and at most 1024 characters. No whitespace, numeric states, or additional delimiters are allowed. Valid Examples: RRRRRRRRRRRR: One ripening cell persists through all twelve future frames. DDDRRROOOOOO: Three dormant frames, three ripening frames, six outgrowth frames. OOOOOO(OOOOOO|OOOOOO): The root has six outgrowth frames, then divides into two outgrowing daughters that each persist for the remaining six frames. OOOOOO(OOOOOO|OOO(OOO|OOO)): Root outgrowth for 6 frames, dividing into two daughters. Daughter A persists for 6 frames; Daughter B persists for 3 frames, then divides into two descendants for the final 3 frames. Evaluation Metrics Submissions are evaluated using Mean Exact Future-Tree Accuracy. Because biological daughter cell ordering (left vs. right branch) is arbitrary in the string representation, both the prediction and the reference are parsed and canonicalized before comparison. Canonicalization recursively sorts the two daughter subtrees at each division lexicographically. After canonicalization, the prediction must be an exact string match to the reference. There is no partial credit for predicting only a correct state, a correct endpoint, or a partial topological branch. $$\text{Score} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}[\text{canonical}(\text{prediction}_i) == \text{canonical}(\text{reference}_i)]$$ Scores range from $0.0$ (no exact matches) to $1.0$ (perfect accuracy). Sample Submission Format Submit a UTF-8 encoded CSV file containing exactly two columns in this order: forecast_id,future_lineage. Include exactly one row per test ID. forecast_id,future_lineage example_1,OOOOOO(OOOOOO|OOOOOO) Parsing Bounds & Rejection: Missing, extra, duplicate, or unknown IDs, wrong columns, or a top-level malformed CSV will result in a global file score of 0.0. A malformed tree (e.g., invalid characters, incorrect horizon length, trailing content) receives a score of 0.0 for that specific row. What Not To Use To ensure rigorous evaluation of model learning efficiency and sequential biological modeling: Execution Constraints: The solution must run entirely offline. You cannot use external datasets, web lookups, hosted APIs, manual annotation of test rows, hard-coded test IDs, or reverse image searches. No Pretrained Assets: You must train learned parameters from random initialization. No pretrained models, foundational vision checkpoints, or pre-calculated embeddings are permitted. Task-Specific Fitting: You must fit or adapt your task-specific parameters dynamically on the supplied training split during the isolated offline solution run. Utilize the provided train_groups.csv to ensure proper internal cross-validation without temporal leakage. &nbsp;
> Closes in 1h 57m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Dramaturg: Historical Markup Dependency Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7265s5x736heh5bx4nqshy7s8dsjt6
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat sasekiart's score of 64.366!

Full challenge description from page:

> Dramaturg: Historical Markup Dependency Reconstruction Overview Editorial markup in historical performance chronicles is not merely a list of names and dates. One passage can reuse the same canonical entry several times, nest an expansion beneath another annotation, and place genuine entries beside plausible but unused register candidates. This challenge asks you to reconstruct that hidden editorial analysis from three incomplete views: a coded surface trace, coded context from neighboring rows, and a shuffled bank of possible annotations. The prediction is a candidate-ordered audit rather than a transcription or a flat list. Every displayed candidate must be marked either DROP or assigned one or more annotation occurrences. A retained occurrence specifies its semantic kind, its rank in the hidden preorder, and the rank of its dependency parent. Solving a row therefore couples four decisions: reject distractors, recover repeated uses, order the retained occurrences, and assemble their dependency forest. All targets come directly from real editorial annotations. Input evidence is deterministically withheld at several visibility levels, but target nodes and relations are never randomized, corrupted, or synthetically relabeled. Output Language An annotation_audit contains one space-separated token for every entry in annotation_bank, in ascending handle order. C04=DROP means candidate C04 is not used by the hidden markup. C04=E@02^ROOT means C04 is an expansion occurrence with preorder rank 02 and no annotation parent. C04=E@02^ROOT+E@06^04 means the same candidate occurs twice. Its second occurrence has rank 06 and its parent is the occurrence at rank 04. Each occurrence atom has the form K@rr^pp: K is W for work, D for date, E for expansion, or P for person. rr is a two-digit preorder rank. pp is ROOT or the two-digit rank of an earlier occurrence. Across a row, ranks must be exactly 00 through occurrence_count-1, each used once. Every numeric parent must refer to an earlier rank. The audit must contain exactly bank_size candidate tokens, beginning with C00 and ending with C(bank_size-1). Evaluation Metric The Dramaturg Annotation Audit Score combines candidate triage, typed multiplicity, relative order, and dependency attachment. Every component lies in [0,1]. Candidate-selection F1 S. Treat every candidate-bank entry as retained or dropped. Aggregate true positives, false positives, and false negatives over all evaluation rows: &nbsp; S=\frac{2TP}{2TP+FP+FN}. &nbsp; Typed-occurrence F1 N. Give each occurrence the four-part stable key row|handle|kind|occurrence-index, where occurrence-index counts equal handle-kind occurrences in ascending predicted or true rank. Let T and P be the resulting true and predicted multisets: &nbsp; N=\frac{2\sum_x\min(T(x),P(x))}{\sum_xT(x)+\sum_xP(x)}. &nbsp; Pairwise-order concordance O. For row i, consider every pair of true occurrence keys in true preorder. A pair earns credit only when both typed occurrences are recovered and their predicted ranks preserve the true order: &nbsp; O_i=\frac{1}{\binom{n_i}{2}}\sum_{a<b}\mathbf{1}[a,b\text{ recovered and }\hat r_a<\hat r_b], \qquad O=\frac{1}{R}\sum_iO_i. &nbsp; Dependency-attachment F1 A. Convert each row into a multiset of directed parent→child edges using the stable occurrence keys and a distinguished ROOT. For row i: &nbsp; A_i=\frac{2\sum_e\min(T_i(e),P_i(e))}{\sum_eT_i(e)+\sum_eP_i(e)}, \qquad A=\frac{1}{R}\sum_iA_i. &nbsp; Final score. &nbsp; \text{Score}=100\times\operatorname{clip}_{[0,1]}(0.15S+0.25N+0.35O+0.25A). &nbsp; A malformed audit receives worst-case treatment for that row: every candidate decision is counted as wrong, its predicted occurrences match none of the truth, and both order and attachment receive zero. There is no abstention benefit. A score of 0 means no credited audit structure was recovered; 100 requires an exact candidate census, occurrence inventory, preorder, and dependency forest. Measured with the shipped public files and grader: Valid fixed audit: 2.586293 Lexical-overlap triage: 17.385622 Linear candidate model: 36.409442 Boosted candidate model: 43.170304 Position-aware candidate model: 43.695002 Contextual BiGRU audit model: 50.467711 Perfect audit: 100.000000 Public Data The prepared dataset contains: train.csv — 1,632 annotated rows. test.csv — 777 evaluation rows without annotation_audit. sample_submission.csv — a valid two-column submission with all 777 evaluation IDs. Columns in train.csv: id - integer - fresh row identifier assigned after partitioning and deterministic shuffling. surface_trace - string - lossy coded tokens from the focal passage; VM marks withheld evidence, LB a line break, and CELL a cell boundary. page_context - string - more heavily withheld coded evidence from adjacent rows on the same manuscript page. annotation_bank - string - shuffled candidate blocks separated by || ; each block contains a local Cxx handle, coded anchor evidence A=, coded register evidence R=, and an opaque profile hint H=. occurrence_count - integer - number of hidden annotation occurrences, from 3 through 10 in the released files. bank_size - integer - number of candidate tokens required in the audit, from 11 through 19. visibility_band - string - E0, E1, or E2, denoting increasing evidence withholding. layout_channel - string - balanced nuisance value D0 or D1; it does not generate or modify the target. annotation_audit - string - candidate census, typed occurrence ranks, and dependency parents. test.csv has the same eight input columns and never contains annotation_audit. The private answer file and sample_submission.csv both have exactly id,annotation_audit. Generalization Boundary Partitioning occurs at the complete manuscript-page level. All eligible cases from a page remain on one side: 114 pages supply the 1,632 training rows and 52 different pages supply the 777 evaluation rows. Adjacent passages and overlapping windows from an evaluation page therefore cannot appear in training. Exact structural template signatures are globally unique across the retained cases. Vxxxx values form a shared observation alphabet, not an answer code. A value represents a recurring lexical form but never a stable candidate handle, rank, parent, or keep/drop decision. Candidate banks are rebuilt per case, ordered with a case-dependent hash, and only then assigned local Cxx handles. Thus the same lexical evidence can appear under different handles in different rows, while the evaluation row's complete bank configuration and handle permutation are unseen during training. Shared observation codes make it possible to learn reusable lexical relationships. Evaluation tests whether those relationships transfer to held-out pages and new combinations of passages, candidates, distractors, multiplicities, ranks, and parent edges. Original words, manuscript years, page identifiers, row positions, case keys, template signatures, and partition values are absent from participant files. Submission Submit a CSV with a header and exactly 777 rows. Its columns must appear in this order: id - integer - each evaluation identifier exactly once. annotation_audit - string - one valid candidate token per displayed bank entry, in Cxx order. This syntax example uses the real evaluation identifier 1632, whose public row has five required occurrences and fourteen candidates: id,annotation_audit 1632,C00=W@00^ROOT+W@01^ROOT+W@02^ROOT+W@03^ROOT+W@04^ROOT C01=DROP C02=DROP C03=DROP C04=DROP C05=DROP C06=DROP C07=DROP C08=DROP C09=DROP C10=DROP C11=DROP C12=DROP C13=DROP The example is the public placeholder, not the hidden answer. Submission rows may be reordered. Reordered or extra columns, an incorrect row count, and duplicate, missing, or unknown IDs are rejected cleanly. What Not to Use A global Vxxxx-toCxx dictionary cannot work because handles are reassigned independently in every row. Independent keep/drop classification cannot recover repeated occurrences, ranks, or dependency parents and leaves 85% of the score unresolved. Ranking candidates without reconstructing parent edges loses the attachment term and misrepresents nested expansions. Predicting every bank entry as DROP is invalid because the public occurrence count must be satisfied and receives no abstention credit. layout_channel is balanced within structural strata and is intentionally non-predictive. Source lookup cannot reproduce the private audit because public rows contain no source strings, page keys, original order, or candidate permutation keys. A suitable first approach is to learn candidate-to-surface compatibility, estimate repeated use, and then apply a globally constrained decoder that assigns every occurrence rank and parent while emitting the complete candidate audit. &nbsp;
> Closes in 4h 17m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## English-to-German Sentence Translation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70ac5ydmzdfrsjxzdv4b5pss8e9kz1
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat nahi's score of 0.494!

Full challenge description from page:

> English-to-German Sentence Translation Task Translate an English sentence into a complete German sentence that preserves its meaning. Generate the target wording and word order from paired training examples. The prediction is an open-ended target-language sequence with variable length, lexical choices, inflection and ordering. It is not a fixed class, similarity rating or scalar translation-quality prediction. Dataset The public files are train.csv (1,800 labeled original cases), test.csv (400 unlabeled cases), and sample_submission.csv. Each training row contains exactly id,group_id,input,output; test rows omit output. The sample deterministically selects format examples from training outputs without consulting test answers; it is not a fitted baseline. id is an opaque case-alignment key. group_id identifies related source cases for grouped local validation. Neither identifier is a predictive input. input is one English sentence containing 4–18 word runs. German references contain 4–22 word runs. Original punctuation and capitalization are retained. Eligible pairs are linked into groups when they share normalized English or German text. Connected groups are split before case selection. Each normalized English sentence contributes at most one recorded translation, selected deterministically; multiple translations do not inflate the training count. These are isolated contributed sentences without surrounding discourse. Linked exact strings are grouped, but unseen paraphrase relationships may remain. A single reference cannot capture all correct translations. Submission Format Submit exactly id,output, in that order, with one row for every test ID and no extra IDs. Row order is irrelevant. Return the translated German sentence as a nonempty UTF-8 string. CSV quoting must preserve punctuation and embedded quotes. The following row demonstrates the grammar; replace its illustrative ID with a test ID. id,output example_case,Tom weiß nicht viel über Kunst. Missing, extra, reordered or duplicate columns; malformed CSV; missing, extra, duplicate, blank or padded IDs; non-string outputs, empty outputs or outputs exceeding 4096 characters reject the entire submission. Null bytes are forbidden. Evaluation The grader splits each output into Unicode word runs and individual non-whitespace punctuation characters, retaining capitalization. Let P and T be the resulting predicted and recorded sequences. Compute Levenshtein distance D with unit insertion, deletion and substitution costs. Sequence similarity is 1 - D / max(len(P), len(T), 1). The case score is 0.5 * similarity + 0.5 * exact, where exact is 1 only if the complete sequences match. The final score is the arithmetic mean over cases; higher is better, with theoretical minimum 0 and maximum 1. Token multiplicity and order matter. A scalar score or a class label cannot replace the required sequence. This single-reference edit metric measures surface agreement, not independent semantic adequacy or translation fluency. Valid translations can differ substantially from the recorded reference. Expected Approach Train a statistical or neural sequence translator on public pairs. A lexical alignment model is a small reference baseline; phrase modeling, inflection and target-language reordering can improve on word-by-word decoding. Use only a group-held-out portion of public training data to choose hyperparameters. Training, feature extraction and inference must run on CPU. Do not use GPU acceleration. Train learned components from scratch using the supplied public files. What Not To Use Pretrained models, embeddings, weights or external labeled corpora. Original-source lookup, recovered source identifiers, hidden outputs or hardcoded test answers. Case or group IDs as predictive features. &nbsp;
> Closes in 4h 52m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Python Snippet Generation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73b22j0atajcyegsdr888xb98e9189
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat reze's score of 0.436!

Full challenge description from page:

> Python Snippet Generation Task Translate a short programming description into a complete Python snippet. Recover operations, variable bindings, literal values and their composition from the request. The target is source code with open identifiers, literals and nested expressions. A utility name, intent class or numeric answer does not specify the program. The grader requires syntactically valid Python and evaluates the ordered program tokens. Dataset The public files are train.csv (1,800 labeled original cases), test.csv (400 unlabeled cases), and sample_submission.csv. Each training row contains exactly id,group_id,input,output; test rows omit output. The sample deterministically selects format examples from training outputs without consulting test answers; it is not a fitted baseline. id is an opaque case-alignment key. group_id identifies related source cases for grouped local validation. Neither identifier is a predictive input. input is a natural-language programming request. Quoted or backticked names can identify variables, columns, strings or filenames needed by the snippet. Missing library context is not supplied implicitly by execution. The original curated train and test partitions are retained. Original question identifiers form groups; any training group overlapping evaluation is removed before selection. Identical requests with conflicting snippets are excluded. Related programming patterns can recur across groups. Examples are short curated snippets, not complete tested applications. Requests can be underspecified, dependencies can be implicit, and multiple correct implementations may exist. Only the recorded implementation is a reference. No proposed snippet is executed during preparation or grading. Submission Format Submit exactly id,output, in that order, with one row for every test ID and no extra IDs. Row order is irrelevant. Return one nonempty Python source string of at most 4,096 characters. It must parse as a Python module. Multiple lines must be preserved inside one correctly quoted CSV cell. CSV quoting must preserve punctuation and embedded quotes. The following row demonstrates the grammar; replace its illustrative ID with a test ID. id,output example_case,"tuple(map(int, input().split(',')))" Missing, extra, reordered or duplicate columns; malformed CSV; missing, extra, duplicate, blank or padded IDs; non-string outputs, empty outputs or outputs exceeding 4096 characters reject the entire submission. Null bytes are forbidden. Syntax errors reject the whole submission. Parsing does not authorize or execute the code. Evaluation After syntax validation, the grader tokenizes Unicode word runs and individual non-whitespace punctuation characters; whitespace is ignored. Let P and T be the resulting predicted and recorded sequences. Compute Levenshtein distance D with unit insertion, deletion and substitution costs. Sequence similarity is 1 - D / max(len(P), len(T), 1). The case score is 0.5 * similarity + 0.5 * exact, where exact is 1 only if the complete sequences match. The final score is the arithmetic mean over cases; higher is better, with theoretical minimum 0 and maximum 1. Token multiplicity and order matter. A scalar score or a class label cannot replace the required sequence. The metric compares with the recorded reference, not an exhaustive set of semantically equivalent outputs. It does not establish execution correctness or operational validity. Expected Approach Train a code sequence generator or retrieve a related training example and adapt its identifiers and expression structure. Check Python syntax locally without executing generated snippets. Use only a group-held-out portion of public training data to choose hyperparameters. Training, feature extraction and inference must run on CPU. Do not use GPU acceleration. Train learned components from scratch using the supplied public files. What Not To Use Pretrained models, embeddings, weights or external labeled corpora. Original-source lookup, recovered source identifiers, hidden outputs or hardcoded test answers. Case or group IDs as predictive features. &nbsp;
> Closes in 4h 57m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Karakalpak Context-Guided Mixture Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74ax1atkzyph4cag18sz8na18dxj22
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Background Recovering omitted transcript text becomes a source-selection problem when recordings overlap. The same acoustic mixture can support different valid phrases depending on the supplied textual context. This benchmark studies context-guided recovery from paired Karakalpak recordings and evaluates whether predictions change correctly when the requested source changes. Overview Each mono 16-kHz input contains two overlapping native recordings. A prefix and suffix describe one contributor's transcript with a contiguous phrase omitted. Return that contributor's missing 3–8 words, in native transcript order, using both the acoustic mixture and the textual context. Every mixture has two queries. Their IDs share a pair prefix and end in 0 and 1. Both use exactly the same audio, but each supplies the context of a different contributor and requires a different phrase. The correct phrases are absent from all visible flanks in the pair. Speaker identities are unavailable: the task makes no claim that the recordings contain different speakers and supplies no speaker-ID shortcut. Pairs are formed from recordings in the same recording-order block, with duration ratio at most 1.5. Each component receives an independent onset offset of 0–0.5 seconds. Components are normalized to RMS 0.08, independently gain-adjusted by −1.5..1.5 dB, summed, and scaled down together only if the mixture peak exceeds 0.95. Mixtures last at most 29.5 seconds. Target text remains an exact span of one native transcript; it is not a transcription of the combined mixture. Monitoring perturbations: Each component retains deterministic seeded Gaussian noise at 34–42 dB SNR relative to clean waveform RMS, zero or one sinusoidal tone at 60–3,500 Hz with amplitudes 0.2–0.8% of clean RMS, one mild low-pass blend, a single 5–10 ms dropout, and amplitude quantization at step 1/8192. Peaks above 0.98 are scaled down; quiet recordings are not amplified to full scale. The component degradation preserves its duration and native transcript before the explicitly described mixing offsets and level balancing. Numerical stability: Load audio as floating-point values and compute spectral power and log features in FP32 outside mixed-precision autocast. Clamp power to a positive floor before logarithms and verify finite features and losses. Use batches appropriate for the variable recording lengths. Dataset Information (Public Files) The dataset comprises Karakalpak speech recordings and corresponding text alignments. All necessary files are located in the public data directory. +-------------------------+---------------------------------------------------------------+ | File / Directory | Purpose | +-------------------------+---------------------------------------------------------------+ | audio/ | Mono 16-kHz overlapping-recording mixtures, at most 29.5s. | | train.csv | Labeled context-guided phrase queries. | | test.csv | Unlabeled paired queries. | | train_sources/ | Training-only isolated delayed components for supervision. | | train_sources.csv | Training-only id,source_audio path index. | | protocol.json | Public counts and pair-generation settings. | | evaluation_reference.py | Exact public scorer, including paired counterfactual credit. | | benchmark_checks.py | Reproducible public oracle, swap, and context-blind controls. | | sample_submission.csv | Unchanged id,phrase format baseline. | +-------------------------+---------------------------------------------------------------+ The sample submission repeats the most frequent training target phrase (lexicographic tie-break) as a reproducible nonempty format baseline. It contains no evaluation labels; replace its phrases with model predictions. evaluation_reference.py is identical to the competition grader. From inside the public directory, run python benchmark_checks.py . to verify the paired contract on labeled training queries: native answers score 1; exchanging sources or copying one source answer to both contexts scores 0. These are reproducible evaluator controls, not claims about trained architecture performance. The supplied isolated training components also support separate training ablations of source recovery and span decoding. Feature Schema train.csv and test.csv +--------------------+---------+-------------------------------------------------------------+ | Column | Type | Description | +--------------------+---------+-------------------------------------------------------------+ | id | String | Pair identifier with suffix _0 or _1. | | audio | String | Path to the two-recording mono 16-kHz mixture WAV. | | prefix | String | Transcript text preceding the missing phrase. | | suffix | String | Transcript text following the missing phrase. | | missing_word_count | Integer | Number of missing words in the target phrase (3–8). | | phrase | String | (train.csv only) The missing target phrase. | +--------------------+---------+-------------------------------------------------------------+ Generalization & Leakage Controls Both components of each mixture come from the same recording-order block and remain in one split. Each source recording is used in at most one mixture. Candidate recordings are sorted by duration within a block and paired consecutively; odd leftovers and pairs exceeding the duration ratio are excluded. Query pairs remain intact in training or evaluation. The word-level edit distance between the two target phrases must be at least half the larger target word count, and neither target may appear in either query's visible context. These filters preserve an informative counterfactual comparison without revealing a missing phrase through the other row. train_sources.csv joins each training query ID to its isolated, perturbed, delayed target component. These training-only signals support learning source selection before phrase recovery. Isolated evaluation components, full evaluation transcripts, and source identities remain private. To ensure rigorous evaluation on independent data splits: Recording-Order Blocks: Clips are grouped into 100-clip blocks based on recording sequence. Buffer Isolation: 10-clip buffer zones separate blocks to reduce temporal overlap. Sequence Overlap Filtering: Test clips sharing identical 7-word token sequences with the training partition are automatically excluded to prevent memorization-based leakage. Evaluation Metrics Submissions are evaluated using a combination of word-level and character-level normalized Levenshtein similarities. 1. Word and Character Similarities Let $p$ be the normalized predicted phrase and $t$ be the normalized target phrase after applying NFC normalization, lowercasing, and whitespace collapse. Word-Level Similarity ($W$): $$W = \max\left(0, 1 - \frac{d(\text{words}(p), \text{words}(t))}{\max(1, \vert{}\text{words}(t)\vert{})}\right)$$ Where $d(\cdot, \cdot)$ is the Levenshtein edit distance on word tokens. Extra words in predictions count as insertions. Character-Level Similarity ($C$): $$C = \max\left(0, 1 - \frac{d(p, t)}{\max(1, \vert{}t\vert{})}\right)$$ Where $d(\cdot, \cdot)$ is the character-level Levenshtein edit distance. 2. Row Score The final score for an individual row is a weighted combination of word and character similarities: $$\text{Row Score} = 0.7 \times W + 0.3 \times C$$ 3. Final Score Score each pair jointly. Let R0 and R1 be the row similarities against the respective correct phrases. Let X be the sum of each prediction's row similarity against the other query's correct phrase. Let G be the sum of the two correct phrases' row similarities against each other. Compute F = clip((R0 + R1 - X) / (2 - G), 0, 1), then PairScore = sqrt(R0 * R1) * F. The competition score is the mean PairScore over all pairs. For evaluation on a supplied subset containing only one member of a pair, that singleton uses its ordinary row similarity. Full prepared training and test sets contain complete pairs and always use the joint score. Exact answers score 1. Copying any single prediction to both queries makes F zero, even if it contains both phrases. Partial answers receive continuous credit when they favor the requested context. The reference evaluator uses F=1 if 2-G is at most 1e-12; prepared pairs have distinct targets and do not use that fallback. Scores are finite floats in [0,1]. A malformed prediction or empty prediction makes its pair score zero. Sample Submission Format Submit a UTF-8 encoded CSV file containing exactly two columns in this order: id,phrase. Include one row per test ID with no extra or duplicate IDs. Quote JSON and text cells where necessary and double internal quotation marks. id,phrase k_0354a1aee873ae97e984d73b_0,"áli de az emes" Parsing Bounds & Rejection: Broken CSV structure, mismatched ID sets, or missing/extra evaluation IDs result in a file-level score of 0.0. A malformed prediction makes its pair score 0.0. Row order does not affect grading. What Not To Use To ensure fair evaluation of training efficiency and algorithmic design: No External Datasets: Use only the supplied training data and approved general-purpose pretrained weights cached before execution. No External Services: No internet access, web lookup, reverse audio search, hosted inference APIs, or external databases. No Source Exploitation: No manual annotation of test rows, hard-coded test-ID answers, source archive copies, or challenge-specific pretrained checkpoints. Fine-tune at least one pretrained architecture component on the training examples. Deterministic postprocessors are permitted. &nbsp;
> 0 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Recovering a Latent Source Form from Divergent Variants

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a43es3y7xy44rfv6675gbph8av8dt
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat devaton's score of 0.519!

Full challenge description from page:

> Overview Each item is a group of variant forms of one underlying entry — the same thing written differently by several sources, each tagged with an opaque code — together with a target level. The variants descend through a multi-level hierarchy, and the level names how far back the target sits: deeper levels are more divergent from the variants. A given variant group may be reconstructed at more than one level, and when it is, the group is identical across those levels but the target form is different. Your job is to recover the source form at the requested level. Two things make this more than a normalisation task. First, the source form is **never equal to any variant in the group** — each source transforms it in its own regular way (dropping, adding, or substituting characters), so the variants disagree and the target differs from every one of them. Second, because the target **depends on the level**, you cannot learn one fixed mapping from a variant group to an answer; you must learn how each level behaves and apply the one that is asked for. No variant is the answer. Copying any single variant — most frequent, shortest, longest — scores poorly (and no variant ever equals the target exactly); each carries its source's own transformations. The signal is in how the sources differ, aligned across the group. The level matters. The level fixes the target depth, and a variant group that recurs across levels maps to a different source form at each, so a solution that ignores the level column cannot separate those cases. Learn each level's regularities from training. Anonymised. Item ids, source codes and level codes are opaque, and the character inventory has been consistently substituted, so the strings cannot be matched to any outside resource — every regularity you need is present in the released data, but only there. Solve it from the training groups alone. Data All files are UTF-8 CSV with a header row. The variant list is stored as a JSON string inside a cell. Note: an item is a (variant group, level) pair, each row with its own item_id. A variant group may appear at more than one level; where it does, its variants are identical and only the source_form differs. train.csv — one row per revealed item test.csv — one row per item to solve sample_submission.csv item_id,source_form it_1a2b3c4d5e6f, A weak baseline that just echoes each item's most frequent variant — it scores near the naive floor. metadata.json A JSON object with keys task, columns, submission_columns, submission_note, metric, and files. Informational; the grader does not read it. Train / test split The split is by variant group (group-disjoint). Each variant group — one underlying entry with all of its divergent variants — is assigned entirely to the training set or to the test set, together with every level at which it is reconstructed. A variant group that appears anywhere in train.csv is therefore never present in test.csv, and vice versa: no group is shared between the two sets. The assignment is a fixed, salted hash of the group's identity (~80% train / 20% test), so it is fully deterministic and reproducible. Because whole groups are held out, a model cannot memorise a specific group's source form in training and copy it at test time — every test group is unseen. It must instead learn the level-wise regularities (how each level transforms its variants into the source form) from the training groups and apply them to new groups. This also closes the within-group leak: since a group is wholly train or wholly test, seeing one level of a group during training never exposes another level of the same group in the test set. Task For each test item, output the underlying source form its variant group has at that item's level. Evaluation Mean chrF over all test items, in [0, 1], higher is better. chrF is the standard character n-gram F-score (n-grams up to length 6, recall-weighted with beta = 2, spaces ignored) between your predicted source form and the gold source form. Predicting the exact form scores 1; a form sharing no character n-grams with the gold scores 0; partial character overlap earns partial credit. The final score is the mean over all test items. Why chrF. The target is a short character string — the reconstructed source form — and a good reconstruction is usually close rather than exactly right: most characters correct, with a few dropped, added, or substituted. The metric must therefore give **graded partial credit for character-level closeness**, not an all-or-nothing verdict. chrF does exactly this — it scores the overlap of character n-grams (both precision and recall) between the prediction and the gold form, so recovering most of the correct characters in roughly the right local order earns most of the credit, while a wrong guess earns little. Although chrF was introduced for machine translation, it is a **general character-level string-similarity measure** and is the standard choice for character-level reconstruction/generation tasks (morphological reinflection, transliteration, and historical- and proto-form reconstruction). Exact match would be too brittle here — a single-character error would score 0 despite a near-perfect reconstruction — and edit distance is unbounded and asymmetric; chrF's bounded [0, 1], recall-weighted n-gram F-score is a better-calibrated, standard measure of how much of the source form was recovered. Submission format A UTF-8 CSV with a header and exactly these columns: item_id,source_form it_1a2b3c4d5e6f, item_id — string; every test item id, each exactly once. source_form — string; your predicted underlying form for that item. Requirements (violations rejected as invalid): exactly the columns above; every test item_id present exactly once, with no unknown or duplicate ids. A blank prediction is allowed — it simply scores 0 for that item. Allowed Any approach: a character-level sequence-to-sequence model (conditioned on the level) trained from scratch on the training groups, a per-level multi-source alignment that reads the character correspondences off the training data, an edit-rule learner, or a retrieval-plus-repair scheme. Use only libraries already in the runtime; everything must run offline and on CPU (the data is small). What Not To Use No runtime installs or downloads — no pip/conda/apt installs and no fetching or vendoring extra packages, code, or model files; use only what is in the runtime. No external data or network access — no external lexicons, corpora, or resources, and no downloading data over the network. No remote or dynamic models — no hosted inference APIs, gated checkpoints, trust_remote_code=True, or torch.hub.load(). No attempting to identify or retrieve the source corpus, and no use of any answer/label file. &nbsp;
> Closes in 3m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Typed Learner-Error Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dfw3sx2hac570w68551w9j58c5fym
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat faaahmily's score of 0.551!

Full challenge description from page:

> Overview Recover annotated grammatical and orthographic repairs in Czech, German and Italian learner writing. For each repair, return its source span, linguistic type and replacement tokens, following the correction conventions demonstrated in training. The application is structured learner feedback: identifying the affected text, categorizing the issue and supplying its annotated local correction. This is not unrestricted essay rewriting. Dataset There are 700 training documents and 200 test documents. A deterministic assignment places each complete writer/document unit in exactly one split; essays are never divided into training and test sentences or repair events. The source metadata associates each retained document with a distinct author ID. Identical same-language token sequences are collapsed to one document when their annotations agree and excluded when they conflict. This prevents duplicate whole-essay answer reuse across splits. A fixed hash ordering selects the compact subset only after these split and duplicate checks; complete essays and their annotations are preserved. The split tests new writers' responses, and examination tasks can recur across writers. The compact subset is not designed as an unseen-topic split. Topic vocabulary and recurring phrases are therefore legitimate shared context, not evidence of unseen-topic generalization. Knowing the prompt alone does not specify a new writer's errors, token offsets or corrections. Whole-document separation does not eliminate every phrase-level memorization shortcut; no claim of prompt-disjointness or complete immunity to memorization is made. Documents have 20–650 tokens. The reference contains local grammar/orthography annotations whose aligned correction actually changes the annotated span. Nonlocal, unalignable and unchanged annotations are outside the task. Spans can overlap and several types may refer to one span. Training and test labels use the same annotation framework. One native reference is available; alternative valid edits and type assignments may not receive credit. The types cover spelling (O_Graph), punctuation (O_Punct), capitalization (O_Capit), word boundaries (O_Wordbd), apostrophes (O_Apostr), abbreviations (O_Abbrev), morphology (G_Morphol_Wrong), nonexistent inflections (G_Inflect_Inexist), agreement (G_Agr), prepositions (G_Prep), articles (G_Art), word order (G_Wo), conjunctions (G_Conj), negation (G_Neg), reflexives (G_Refl), clitics (G_Clit), part of speech (G_Pos), valency (G_Valency) and verb categories (G_Verb, G_Verb_main, G_Verb_compl). The training annotations establish their distinctions. Submission Submit UTF-8 CSV with exactly task_id,repairs, in that order, once per test ID. repairs is a JSON array of objects: start, end: integer, zero-based half-open source-token offsets. Equal offsets represent insertion. type: a type string from the supplied inventory. replacement: array of 0–40 nonempty tokens, each at most 500 characters and without whitespace. An empty array deletes the span. At most 1,000 events may be submitted per document. For example: task_id,repairs example,"[{""start"":2,""end"":3,""type"":""G_Art"",""replacement"":[""einen""]}]" Evaluation Corpus-level exact-event F0.5 measures recovery of the reference's complete typed edits. Matching the span locates the feedback, matching the type recovers its linguistic category, and matching the replacement reproduces the specified correction. Partial credit for any one field would reward an incomplete feedback record. Duplicate identical events count once. Token case and punctuation are preserved. The human annotations provide a supervised target for applying a shared correction policy to held-out writers. Exact matching is appropriate for that reproducible, policy-specific objective, not as a complete measure of grammatical acceptability. An equally valid unannotated correction can be counted as an unmatched prediction and leave the reference edit unmatched. Consequently, this score must not be interpreted as human-rated writing quality; assessing unrestricted repair quality would require additional references or human judgments. score = 1.25 × TP / (1.25 × TP + 0.25 × FN + FP) TP counts exact matching edits, FP unmatched predicted edits and FN missed reference edits, pooled across documents. F0.5 emphasizes precision because unnecessary interventions are undesirable in learner feedback: its denominator assigns an unmatched prediction four times the penalty of a missed reference edit. This is a stated benchmark preference, not an empirically established cost ratio. Scores range from 0 to 1; a perfect submission scores 1. If the denominator is zero, return 1. Invalid per-row JSON or values contribute all reference events as FN and max(1, reference_event_count) FP. Invalid headers or ID sets are rejected; row order has no effect. What Not To Use GPU training and general-purpose pretrained models are allowed. Use only supplied data for task-specific training. No external correction corpora, challenge-specific checkpoints, source copies, answer lookups, hosted APIs, manual correction of test rows. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The maximum end-to-end runtime is 1.5 hours, including data loading, training or adaptation, inference, structured decoding, validation, and submission writing. &nbsp;
> Closes in 46m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Along-Track Surface Opening Sequence Labeling

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7acj8ag04x95kd475m560jx98e8d2v
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat minipeepee's score of 0.498!

Full challenge description from page:

> Along-Track Surface Opening Sequence Labeling Overview Operational polar mapping systems need to flag narrow surface openings from along-track sensor measurements. A point classifier can find strong local responses while missing the start and end of an opening; a sequence model can use the ordered shape of the surrounding signal to produce a coherent alert profile. Each example is a fixed-length local profile covering 11 ordered positions at a uniform 10 m spacing. The five supplied sensor measurements are repeated in position order, and the goal is to return an opening probability for every position. The inputs are real observations; there are no simulated rows or augmentation requirements. The hidden evaluation set contains complete tracks that are not represented in training. This makes the task a small domain-shift test: models must learn signal structure that transfers across acquisition tracks instead of memorizing an identifier or a random-window neighbor. Train-side labels are provided in a separate sidecar so train and test expose the same feature columns. Dataset File descriptions dataset/public/train.csv: one training example per row, with an opaque id and a serialized 11-position input profile. dataset/public/train_targets.csv: the training target sidecar, keyed by the exact ids in train.csv. dataset/public/test.csv: evaluation examples with the same feature columns and order as train.csv. dataset/public/sample_submission.csv: schema-valid nonzero probability example for every test id. Column descriptions id: opaque stable identifier for one local profile. Treat it as a key only; it contains no usable ordering or track metadata. sequence in train.csv and test.csv: 55 semicolon-separated finite numbers in row-major order. Every five numbers describe one ordered position: relative height above a local low baseline, returned photon rate, contributing pulse count, height-distribution width, and mean-minus-median height offset. Positions 0 through 10 are ordered along track. target in train_targets.csv: an integer bitmask from 0 through 2047. Read its 11 bits from most significant to least significant to recover the binary target at positions 0 through 10; 1 means an annotated surface opening and 0 means background. Evaluation The grader parses the 11 probabilities for each test id, aligns rows by id, and computes two average-precision terms. point_ap rewards ranking opening positions above background positions. boundary_ap rewards large adjacent probability changes at true opening/background transitions, which measures whether the model localizes opening edges rather than only producing a broad alert. The final score is a bounded maximize metric: import numpy as np from sklearn.metrics import average_precision_score def safe_average_precision(labels, scores): labels = np.asarray(labels, dtype=np.int8).reshape(-1) scores = np.asarray(scores, dtype=np.float64).reshape(-1) positives = int(labels.sum()) if positives == 0: return 0.0 if positives == len(labels): return 1.0 return float(average_precision_score(labels, scores)) def opening_sequence_score(y_true, prediction): y_true = np.asarray(y_true, dtype=np.int8) prediction = np.asarray(prediction, dtype=np.float64) if y_true.ndim != 2 or prediction.shape != y_true.shape or y_true.shape[1] != 11: raise ValueError("truth and prediction must both have shape (n_examples, 11)") if not np.isfinite(prediction).all() or (prediction 1).any(): raise ValueError("predictions must be finite probabilities in [0, 1]") point_ap = safe_average_precision(y_true, prediction) boundary_true = y_true[:, 1:] != y_true[:, :-1] boundary_confidence = np.abs(prediction[:, 1:] - prediction[:, :-1]) boundary_ap = safe_average_precision(boundary_true, boundary_confidence) return float(0.70 * point_ap + 0.30 * boundary_ap) The boundary term uses the absolute change between adjacent predicted probabilities, so it is direction-free and evaluates both opening-to-background and background-to-opening edges. An evaluation partition with no positive point or no positive boundary receives 0 for that term. The official grader rejects missing or duplicate ids, malformed vectors, non-finite values, and probabilities outside [0, 1]; submission row order does not matter. Submission Submit one UTF-8 CSV file with exactly these columns: id: every id from test.csv, exactly once. prediction: 11 semicolon-separated decimal probabilities in [0, 1], in the same position order as the input sequence. Example: id,prediction window_00005f8e04e5b235,0.04;0.03;0.02;0.01;0.02;0.72;0.91;0.84;0.10;0.03;0.02 Requirements Keep the 11 output values aligned to the 11 input positions; do not emit one scalar per row. Use only the public files for model inputs and train-side targets. Preserve every test id exactly and write the final file as ./working/submission.csv. Predictions must be finite probabilities, not hard labels, because both official terms use ranking. Any offline model family is allowed if it fits the A10G runtime and memory budget. What Not To Use Do not infer or reconstruct labels from the opaque ids, row order, duplicate neighboring windows, or any hidden evaluation file. Do not retrieve the upstream archive, source-track identifiers, coordinates, timestamps, or withheld source channels to identify the evaluation track or its labels. Do not use raw annotation/proxy channels or source metadata that are absent from the public sequence column. Do not add synthetic profiles, generated labels, external pseudo-labels, or test-time augmentation intended to change the evaluation population. Do not tune against the private answers or repeatedly inspect hidden-test scores. &nbsp;
> Closes in 1h 28m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Cross-Mission Event-Shape Deep-Space Sensor Translation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73csrb4xqzb7tppsqnw0jwa18e6wcv
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat rajat20056's score of 0.476!

Full challenge description from page:

> Cross-Mission Event-Shape Deep-Space Sensor Translation Overview This is a cross-mission Sequence-to-Sequence machine learning challenge built from real hourly deep-space spacecraft telemetry. The task is to translate spacecraft context, target-stream history, and peer-sensor evidence into a missing target-sensor event sequence. Each example represents a fixed twenty-four-hour missing window for one target sensor stream. The model receives target-sensor context before and after the missing window, coded spacecraft identity, coded sensor identity, coarse mission-position buckets, and auxiliary peer-sensor readings from the same twenty-four-hour window. The model must output the twenty-four ordered value-bin symbols for the target stream. This challenge tests from-scratch sequence modeling, temporal feature learning, sparse context handling, cross-mission transfer, sensor-to-sensor translation, and event-shape reconstruction. Novel challenge design This benchmark uses a combinatorial zero-shot sensor-translation setup with event-shape scoring. The preparation pipeline deliberately withholds selected craft_code + sensor_code pairings from the training rows while keeping the individual spacecraft codes and individual sensor codes visible elsewhere in training. This means the model sees the spacecraft in other sensor contexts and sees the sensor stream on other spacecraft, but does not see that exact craft-sensor combination before scoring. This is different from ordinary telemetry forecasting or mission holdout forecasting. The task is not simply to forecast a future numeric trace from the same mission. It is a compositional translation problem: the solver must combine knowledge of spacecraft behavior, sensor-stream behavior, mission phase, orbital context, target-stream left/right context, and auxiliary peer-sensor readings to reconstruct a target stream for both familiar and unseen craft-sensor pairings. The evaluation also scores the event shape of the sequence, not only exact token matches. The twenty-four-step sequence is treated as six consecutive four-hour telemetry-shape cells. Each cell can behave like a plateau, ramp up, ramp down, spike, dip, oscillation, or mixed movement. A strong solution must therefore learn both the symbolic value bins and the local event dynamics. One-line objective Predict a hidden twenty-four-step target-sensor token sequence by learning transferable relationships across spacecraft, sensor channels, mission phase, orbital buckets, target-stream context, and auxiliary peer-sensor context, including craft-sensor pairings not present as training rows. Task For each row in test.csv, predict the missing twenty-four-step telemetry sequence. Each prediction must contain exactly twenty-four ordered value-bin symbols. Valid symbols are the forty-one two-letter tokens from aa through bo: aa ab ac ad ae af ag ah ai aj ak al am an ao ap aq ar as at au av aw ax ay az ba bb bc bd be bf bg bh bi bj bk bl bm bn bo The training target column is named target_sequence. It appears in train.csv and is not present in test.csv. Every row represents a fixed twenty-four-hour missing window. Because the window length is part of the challenge contract and is the same for all rows, it is not included as a feature column. Files visible to solvers The solver-facing dataset contains exactly these files: train.csv test.csv sample_submission.csv No extra helper files are provided. Training data train.csv contains input features and the target sequence to learn from. Columns in train.csv ID column id Unique training row ID. Spacecraft and target-sensor identifiers craft_code Coded spacecraft identifier. sensor_code Coded target telemetry sensor-stream identifier. Coarse time buckets hour_bucket Hour-of-day bucket for the middle of the missing window. month_bucket Month bucket for the middle of the missing window. doy_bucket Coarse day-of-year bucket for the middle of the missing window. Coarse mission and position buckets mission_bucket Coarse training-derived bucket representing mission elapsed time. distance_bucket Coarse training-derived bucket representing heliocentric distance from the Sun. latitude_bucket Coarse training-derived bucket representing heliographic latitude. longitude_bucket Coarse heliographic longitude sector. These mission and position fields are categorical buckets rather than raw numeric features. This keeps the prepared tabular profile stable while still giving solvers useful temporal and orbital context. Target-stream context before the missing window left_aa through left_bv Forty-eight context symbols before the missing target window. left_aa is the oldest context step and left_bv is the nearest step before the missing window. Each value is either a value-bin symbol from aa through bo, or miss when the source value was unavailable. Target-stream context after the missing window right_aa through right_bv Forty-eight context symbols after the missing target window. right_aa is the nearest step after the missing window and right_bv is the farthest right-context step. Each value is either a value-bin symbol from aa through bo, or miss when the source value was unavailable. Auxiliary peer-sensor context during the same window aux_a_code, aux_b_code, and aux_c_code Coded identifiers for up to three peer sensor streams available as auxiliary evidence for the target stream. aux_a_gap_aa through aux_a_gap_ax Twenty-four peer-sensor symbols from the first auxiliary stream during the same missing target window. aux_b_gap_aa through aux_b_gap_ax Twenty-four peer-sensor symbols from the second auxiliary stream during the same missing target window. aux_c_gap_aa through aux_c_gap_ax Twenty-four peer-sensor symbols from the third auxiliary stream during the same missing target window. These auxiliary columns turn the task into sensor translation. The target sensor stream is missing, but other sensor streams may still provide partial evidence about the same time period. Target sequence target_sequence Space-separated sequence of twenty-four value-bin symbols. This is the target sequence that must be learned from training rows. This column appears only in train.csv. Test data test.csv contains the same input columns as train.csv, except target_sequence is removed. Some craft_code + sensor_code pairings in test.csv are not present as training rows. Solvers should design models that can generalize compositionally across spacecraft codes, target-sensor codes, and auxiliary peer-sensor context. Combinatorial zero-shot pairing logic The split is not a simple random split and not a full mission holdout. The preparation pipeline first builds valid examples for each spacecraft-sensor pair. It then reserves selected pairings so that: the exact craft_code + sensor_code pairing is absent from training rows; the same craft_code appears in training rows with other sensor streams; the same sensor_code appears in training rows with other spacecraft; the scored set includes both familiar pairings and zero-shot pairings; macro averaging prevents frequent familiar pairings from overwhelming difficult compositional pairings. This is the central transfer-learning requirement of the challenge. A solver that only memorizes per-pair historical patterns should be weaker than a solver that learns reusable spacecraft embeddings, sensor embeddings, mission-position effects, and peer-sensor relationships. Submission format Submit a CSV file named submission.csv with exactly these columns: id Row ID from test.csv. prediction_sequence Space-separated sequence of exactly twenty-four value-bin symbols. Example: id,prediction_sequence te_aaaaaa,"as as at au au av av au at as ar ar as at au au av aw aw av au at as as" The submission must contain exactly one row for every ID in sample_submission.csv. Missing IDs, duplicate IDs, extra IDs, malformed sequences, unsupported symbols, or sequences with a length other than twenty-four receive the invalid-submission score. Evaluation Submissions are scored using a custom symbolic event-sequence reconstruction error. Lower is better. The final score is: score = 0.55 * macro_token_error + 0.25 * macro_transition_error + 0.20 * macro_event_shape_error The theoretical best score is 0. The theoretical worst score is 1. Grouping keys for macro averaging The macro group is defined by the visible pair: craft_code + sensor_code For example: craft_alpha + sensor_aa or craft_gamma + sensor_ae Step one: row-level token error For each row, the scorer parses the submitted prediction_sequence and the expected twenty-four-step sequence into two arrays of twenty-four symbols. For each row: row_token_error = fraction of the twenty-four positions where the submitted symbol is different from the expected symbol A perfect row has row_token_error = 0.0. A row with all positions wrong has row_token_error = 1.0. Step two: macro token error For each craft_code + sensor_code group: group_token_error = mean(row_token_error for rows in that group) Then: macro_token_error = mean(group_token_error across all craft-sensor groups) Macro averaging is used because spacecraft and sensor streams have different coverage levels. Without macro averaging, dense groups could dominate the score and hide weak transfer performance on sparse or zero-shot craft-sensor groups. Step three: transition error Each symbol is converted to its ordered bin index: aa -> first bin, ab -> second bin, ac -> third bin, and so on through bo -> final bin. For each twenty-four-step sequence, the scorer computes the sign of each adjacent step change: falling stable rising For each row: row_transition_error = fraction of the twenty-three adjacent transitions where the submitted transition direction differs from the expected transition direction For each craft_code + sensor_code group: group_transition_error = mean(row_transition_error for rows in that group) Then: macro_transition_error = mean(group_transition_error across all craft-sensor groups) Step four: event-shape error The twenty-four-step sequence is divided into six consecutive four-step cells: steps 1-4 steps 5-8 steps 9-12 steps 13-16 steps 17-20 steps 21-24 Each four-step cell is assigned one event-shape class using the ordered token indices: plateau The cell has very small spread. ramp_up The cell has a clear positive net movement. ramp_down The cell has a clear negative net movement. spike The cell rises to an internal high point and returns downward. dip The cell falls to an internal low point and returns upward. oscillating The cell changes movement direction multiple times. mixed The cell does not match one of the stronger shape patterns above. For each row: row_event_shape_error = fraction of the six four-step cells where the submitted event-shape class differs from the expected event-shape class For each craft_code + sensor_code group: group_event_shape_error = mean(row_event_shape_error for rows in that group) Then: macro_event_shape_error = mean(group_event_shape_error across all craft-sensor groups) Solvers can reproduce the token, transition, and event-shape calculations on validation splits created from train.csv, where target_sequence is provided. Why this metric is appropriate The main objective is accurate reconstruction of the full missing twenty-four-step target sequence. For that reason, most of the score, fifty-five percent, comes from macro token error. The macro term makes the score fair across spacecraft and sensor streams. A model must perform well across multiple mission-sensor groups, including unseen craft-sensor pairings, not only on the densest or easiest rows. Twenty-five percent of the score comes from transition error. This rewards models that capture local rising, falling, and stable movement between adjacent hourly steps. The remaining twenty percent comes from event-shape error. This explicitly rewards domain-relevant telemetry behavior across four-hour cells, such as plateaus, ramps, spikes, dips, and oscillations. A sequence can have reasonable token accuracy while missing the physical event shape, so this term separates simple frequency prediction from true sequence-event modeling. Data cleaning and split design The preparation pipeline removes exact duplicate raw rows, standardizes spacecraft names, parses timestamps, removes duplicate spacecraft-time keys, converts invalid numerics to unavailable values, removes infinite values, and applies broad physical sanity checks before creating examples. Prepared public columns are categorical text fields. Long raw numeric strings and exact timestamps are not exposed in the solver-facing files. The split is designed to reduce leakage: overlapping examples are thinned by a deterministic stride; ordinary familiar-pair examples use chronological train/test separation; selected craft-sensor pairings appear as scored rows without matching training rows; every reserved spacecraft code and every reserved sensor code still appears elsewhere in training rows. Allowed Solutions are allowed to: train neural sequence models, temporal convolution models, recurrent models, Transformer-style models, autoencoders, or other ML models from scratch using only the provided solver-facing files; use standard libraries available in the execution environment; engineer features from the provided training and test columns; create validation splits using only train.csv; use inference that processes one test row or one test batch at a time; use deterministic cleaning, parsing, tokenization, masking, batching, and training logic; share approaches publicly where Eris rules allow public discussion. Not allowed Solutions are not allowed to: use any files not listed in the solver-facing dataset; use external datasets; generate synthetic training rows; load self-hosted fine-tuned weights or cached artifacts from previous runs; use pretrained model weights, because this challenge is intended as a from-scratch sequence modeling challenge; use pure rule-based interpolation as the full solution without real ML training; hardcode predictions, coefficients, weights, leaderboard behavior, or dataset-specific shortcuts instead of training a model; use full test-set distribution adaptation, pseudo-target generation, prediction calibration from the full test set, or reweighting based on the full test set; install packages outside the allowed execution environment. Recommended solution direction Strong solutions should parse the context tokens carefully, embed categorical features, handle miss values explicitly, model differences between spacecraft and sensor streams, use auxiliary peer-sensor context, score validation folds with held-out craft-sensor pairings, and optimize not only exact token accuracy but also adjacent-step transitions and four-step event shapes. &nbsp;
> Closes in 2h 43m
> 10 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Punjabi News Dictation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72ev0t53dr4jhzqvbec1hf818e5ga3
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat aneeshm44's score of 0.926!

Full challenge description from page:

> Background Automatic Speech Recognition (ASR) for regional and morphologically rich languages presents unique challenges, particularly in domain-specific broadcast environments like news dictation. Spoken news speech contains diverse named entities, inflections, complex sentence structures, and variable pacing. Delineating phonetic acoustic nuances and transcribing them directly into native orthography without intermediate phonetic representations requires robust sequence-to-sequence acoustic and linguistic processing. Overview Given variable-length audio recordings of spoken Punjabi news dictations, transcribe each utterance into ordered, native Gurmukhi text. The solution must recover the full spoken lexical sequence, including named entities, numbers, and inflected word forms, directly from the audio signal. This is a GPU-only sequence-to-sequence challenge. Learned training, adaptation, and inference must execute on CUDA within a single self-contained offline session. The operational hardware envelope provides one NVIDIA A10G and a strict 90-minute total solution runtime. Dataset Information (Public Files) All assets necessary for training and evaluation are supplied in the public directory. Audio files are provided as mono 16 kHz PCM-16 FLAC files. +-----------------------+--------------------------------------------------------------+ | File / Directory | Purpose | +-----------------------+--------------------------------------------------------------+ | audio/ | Directory of mono 16 kHz PCM-16 FLAC audio recordings. | | train.csv | 715 labeled training examples with reference transcriptions. | | test.csv | 185 evaluation queries requiring transcriptions. | | sample_submission.csv | Format-example rows demonstrating the required output schema.| +-----------------------+--------------------------------------------------------------+ Split Protocol and Limits Preparation deduplicates normalized full transcripts, links records sharing the first four transcript words or an exact transcript, and assigns each entire connected group by a deterministic hash with nominal 20% evaluation probability. The retained split has 715 training rows and 185 evaluation rows. Exact transcripts and shared four-word prefixes cannot cross this boundary. This controls direct phrase copying; it does not establish speaker, recording-session, topic, or paraphrase disjointness. Broadcast vocabulary can recur across splits. Validation must be constructed from training rows and keep equal four-word transcript prefixes together. Evaluation measures transcription within this broadcast domain, not transfer to unseen speakers or domains. Audio Rendering The waveform is converted to mono 16 kHz. Deterministic rendering applies gain 0.90–1.10, Gaussian noise with sampled standard deviation 0.002–0.010, zero to two 10–29-sample transients with offsets in [−0.15,0.15], a 50 or 60 Hz hum of amplitude 0.005, and a 1000–3000 Hz tone of amplitude 0.002. Finally it is multiplied by 0.92, clipped to [−1,1], and encoded as PCM-16 FLAC. These amplitude values are in normalized waveform units. Rendering changes the input audio, not the reference text. Feature Schema train.csv and test.csv +------------------+---------+---------------------------------------------------------+ | Column | Type | Description | +------------------+---------+---------------------------------------------------------+ | id | String | Opaque 24-character hexadecimal row identifier. | | audio | String | Relative path to the FLAC audio file (audio/.flac). | | duration_seconds | Float | Decoded audio duration in seconds (at most 20.0s). | | prediction | String | (Train only) Reference Gurmukhi text transcription. | +------------------+---------+---------------------------------------------------------+ Target Text Schema Predictions must be submitted as plain text in the Gurmukhi script. Script & Formatting: Transcriptions must use standard Gurmukhi orthography conforming to the conventions shown in the training split. Do not output phonetic Latin transliterations, romanized script, or translations into English. Normalization: Text will undergo standard Unicode NFC normalization and consecutive whitespace collapsing prior to evaluation. Target Length Limits: Ground-truth training targets contain between 5 and 45 words and at most 600 characters. Any test prediction exceeding 100 words or 1,200 characters will automatically receive a score of 0.0 for that row. An illustrative target from the training set: ਕੁਲ ਦੁਨੀਆਂ ਚ ਤਾਂ ਕਰੋੜ ਤੋਂ ਵੱਧ ਹੋ ਗਏ ਹੋਣਗੇ Evaluation Metrics Word edit similarity penalizes missing, extra and substituted lexical units. Character edit similarity gives graded credit for partially correct Gurmukhi spellings and inflections within an otherwise incorrect word. Equal weighting balances whole-word recovery and orthographic fidelity. This is a text-transcription metric, not a direct acoustic or phonetic-distance measurement: Unicode codepoints are compared without phoneme alignment, and whitespace and NFC normalization are the only invariances. Submissions are evaluated row-by-row by comparing the normalized predicted text against the reference transcription. The evaluation balances word-level structural consistency and character-level phonetic alignment. Both candidate and reference strings are preprocessed by collapsing whitespace and applying Unicode NFC normalization. 1. Edit Similarity ($E$) For two token sequences $a$ and $b$ (whether lists of words or sequences of characters), edit similarity is computed using unit-cost Levenshtein distance: $$E(a, b) = \max\left(0, 1 - \frac{\text{Levenshtein}(a, b)}{\max(\text{len}(a), \text{len}(b))}\right)$$ If both $a$ and $b$ are empty, $E(a, b) = 1.0$. If exactly one sequence is empty, $E(a, b) = 0.0$. 2. Word and Character Metrics Word Edit Similarity ($S_{\text{word}}$): Evaluated by whitespace-tokenizing strings into word arrays: $$S_{\text{word}} = E(P_{\text{words}}, T_{\text{words}})$$ Character Edit Similarity ($S_{\text{char}}$): Evaluated directly on Unicode codepoints: $$S_{\text{char}} = E(P, T)$$ 3. Row Score and Final Score The overall row score is the unweighted average of word and character similarities: $$\text{Row Score} = 0.5 \times S_{\text{word}} + 0.5 \times S_{\text{char}}$$ The final competition score is the arithmetic mean of all row scores across the test set: $$\text{Final Score} = \frac{1}{N_{\text{test}}} \sum_{i=1}^{N_{\text{test}}} \text{Row Score}_i$$ Scores range from $0.0$ to $1.0$ (higher is better). Sample Submission Format Submit a UTF-8 encoded CSV file containing exactly two columns in this order: id,prediction. Include one row per test ID with no missing, extra, or duplicate IDs. Quote strings using standard CSV conventions to ensure punctuation and commas do not corrupt row formatting. id,prediction 4cbde45743f8bd7e1b57f67e,"ਕੁਲ ਦੁਨੀਆਂ ਚ ਤਾਂ ਕਰੋੜ ਤੋਂ ਵੱਧ ਹੋ ਗਏ ਹੋਣਗੇ" Parsing Bounds & Rejection: - Missing, extra, duplicate, or unaligned IDs, incorrect column headers, or files exceeding 256 MB raise an informative ValueError and reject the submission. - Predictions longer than 100 words or 1,200 characters score 0.0 for that row. - Individual prediction cells exceeding 65,536 characters trigger an invalid cell error and score 0.0 for the row. - Row ordering does not affect grading. What Not To Use To ensure rigorous evaluation of learning efficiency and offline speech recognition: Offline Execution Only: No internet access, hosted inference APIs, external cloud lookups, or reverse-engineering from external archives. No External Datasets: Solutions must rely strictly on the supplied training data for task supervision. External speech datasets or outside text corpora cannot be downloaded during the run. Pretrained Checkpoints: Generic pretrained weights (such as foundational ASR checkpoints) may only be used if explicitly pre-provisioned in the isolated environment's allowlist. Domain-specific, fine-tuned, or private checkpoints are strictly prohibited. No Exploitation: Manual labeling of test samples, hard-coded lookup dictionaries, or test ID conditioning is forbidden. Hardware Envelope: All training/adaptation and neural inference must finish within 90 minutes on the designated GPU environment (1 NVIDIA A10G) &nbsp;
> 3 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Editorial Plan Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7br769a2b5se5f4wwzgengzs8e98w8
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Editorial Plan Reconstruction Overview Given a real post exactly as its author first submitted it, reconstruct the plan a human editor carried out on it: an ordered sequence with one segment per sentence, recording whether the editor kept the sentence, rewrote it in place, or cut it from the post. Return the plan, not a revised post. Nothing tells you which sentences the editor touched. A solution has to locate the sentences that needed an editor's attention and decide what kind of intervention each one received, and those decisions hang together across a post. A sentence can be flawed but essential — it is repaired — or sound but out of place — it is removed. The posts are first submissions to a public question-and-answer community about writing, and each plan is the first revision the post actually received from a human editor. Cut sentences are often talk aimed at the community rather than the reader — greetings, apologies for asking, sign-offs, notes about editing — and they tend to come in runs, such as a closing thank-you followed by a signature. Rewritten sentences carry the argument and are fixed for grammar, clarity or formatting. Neither pattern is a word list: "thanks" appears both in sentences editors keep ("thanks to Word's grammar checker, …") and in closing lines they cut ("Thanks for any advice …"). Dataset UTF-8 CSVs contain JSON arrays in individual string cells. Parse CSV and JSON separately. | File | Contents | |---|---| | train.csv | 5,986 labeled posts. Columns, in order: case_id, post_kind, topic_tag, sentences, plan. | | test.csv | 1,405 unlabeled posts. Columns, in order: case_id, post_kind, topic_tag, sentences. | | sample_submission.csv | Input-only baseline for every test ID; columns case_id,plan. | Private answers.csv uses the ordered columns case_id,plan. No auxiliary files are needed. Input Columns | Column | Type | Contents | |---|---|---| | case_id | string | Opaque example identifier. | | post_kind | string | question or answer: the kind of post. | | topic_tag | string | The first community tag of the post's question, for example fiction, dialogue, technical-writing. | | sentences | JSON-encoded string | The post as first submitted: an ordered array of objects with string fields id s00, s01, …) and text. 5 to 20 sentences per post; code blocks, quotes, list items and headings are kept whole. | Web addresses appear as the literal token ` and user mentions as . Every post in this challenge received at least one rewrite or cut`. The Plan | Column | Type | Meaning | |---|---|---| | plan | string | Pipe-separated segments id:action, one for each sentence of the post, in order. | | Action | Meaning | |---|---| | keep | The sentence survives the revision unchanged, apart from whitespace. | | rewrite | The sentence survives the revision in modified form. | | cut | The sentence does not survive the revision, or is replaced by text unrelated to it. | For a four-sentence post whose editor rewrote the second sentence and cut the fourth, the plan is s00:keep|s01:rewrite|s02:keep|s03:cut. Ground Truth and Scope Each post's first submission and first revision were split into sentences with the same deterministic splitter and aligned by a monotone Needleman–Wunsch pass over token-level Dice similarity. An aligned pair that is identical after whitespace normalization is keep. An aligned pair with similarity of at least 0.55 is rewrite. A sentence with no counterpart, or whose counterpart falls below 0.55, is cut. This reproducible alignment defines the target; the procedure is documented in the source dataset. Only the first revision of each post is used, so every plan is one editor's single pass over untouched text. Revisions that changed no sentence (they only added material), whitespace-only revisions and wholesale rewrites (more than 60% of sentences changed) are excluded. Revision texts and the editors' change summaries are withheld. Plans reflect an editor's choice, including optional stylistic changes, and the same post could reasonably have been handled differently by another editor. Prepared Distribution | Measure | Training | Test | |---|---|---| | posts | 5,986 | 1,405 | | sentences (plan segments) | 61,017 | 14,188 | | keep | 49,346 (80.9%) | 11,442 (80.6%) | | rewrite | 9,526 (15.6%) | 2,231 (15.7%) | | cut | 2,145 (3.5%) | 515 (3.6%) | | edit runs | 9,244 | 2,145 | | posts containing a cut | 1,236 | 290 | A post holds 1 to 12 edited sentences. The split is stratified by whether a post contains a cut, how many sentences were edited, and post kind. Submission Format Write the final CSV to ./working/submission.csv. The header is case_id,plan. Both columns are strings. Include every test ID exactly once; rows may be reordered. A missing case_id or plan column, a duplicate ID, or a test ID absent from the file rejects the submission. Do not add an index. Labeled training example; use the corresponding test IDs in your submission: | case_id | plan | |---|---| | case_85cb35ae704c6c762f0264d2 | s00:rewrite\|s01:cut\|s02:keep\|s03:keep\|s04:keep\|s05:keep | Segments are matched by sentence id, so their order within a plan does not affect the score; ids and actions are case-insensitive. A plan that names an unknown id, repeats or omits a sentence, uses an action other than keep, rewrite or cut, or is empty is not repaired: it is scored as planning every sentence keep, so it earns nothing and its true edits count as misses. Evaluation Minimum score: 0.0. Maximum score: 1.0. Higher is better. Metric: Plan Reconstruction Score. Three components, computed over the evaluated posts: Agreement — Cohen's κ between predicted and true actions over the three actions, pooled over every sentence: (p_o − p_e) / (1 − p_e), where p_o is the fraction of sentences whose action matches and p_e is Σ over actions of (true share × predicted share). Clipped below at 0. EditRun — micro F1, 2·TP / (2·TP + FP + FN), over edit runs: maximal runs of consecutive sentences that share one action other than keep, identified by post, start, end (exclusive) and action. A run counts only if all four match exactly. Cut — micro F1 over cut sentences, identified by post and sentence id. Final score = 0.55 · Agreement + 0.25 · EditRun + 0.20 · Cut. Every constant plan scores 0 or close to it: Agreement is 0 for a constant plan by construction, and no post's true plan is a single run covering all of its sentences. If both prediction and truth contain no events of a type over the evaluated set, that F1 is 1; if both plans are the same single action throughout, Agreement is 1. An exact submission scores 1 on any set. Local Reference Checks | Check | Score | |---|---| | Exact answers | 1.000000 | | Supplied sample submission (every sentence keep) | 0.000000 | | Every sentence rewrite | 0.000000 | | Every sentence cut | 0.014011 | | Rule: cut the last sentence, keep the rest | 0.057052 | Learned GPU and hosted agent baselines are unmeasured. How This Differs from Related Work Sentence-level edit prediction has precedents. NewsEdits (Spangher et al., NAACL 2022) predicts which sentences of a news article a later version will change; there, most revisions are driven by new facts arriving, while here the subject of a post is fixed and edits are about the writing itself and about community norms. EditNet (Moroshko et al., 2019) makes keep, rewrite or delete decisions over sentences as a step inside summarization, where the edit serves compression; here each plan is a real human editor's decision about a real post, recorded in a site's revision history. Edit-intention corpora such as IteraTeR (Du et al., ACL 2022) and arXivEdits (Jiang et al., EMNLP 2022) label the intent of edits that are shown to the model; here the revision is never shown, and the task is to reconstruct it from the original alone. Two choices are specific to this challenge: every plan is a post's first revision, so labels are one editor's single pass rather than a mix of successive updates; and the metric is chance-corrected and credits contiguous edit runs, so neither the dominant keep action nor scattered guesses earn credit. Practical Starting Point Fine-tune a compact encoder as a cross-encoder over each sentence and its context: the sentence with its position, post kind and topic, paired with the neighbouring sentences and the post's opening. Decode each post's plan from the per-sentence scores with a keep bias tuned for the metric on held-out training posts, keeping all sentences of a post on the same side of the split. The competition environment provides access to a single NVIDIA A10G GPU. The entire pipeline must finish within 1.5 hours, including data loading, training or adaptation, inference, decoding, validation, and submission generation. Allowed Methods and Data Boundaries Models trained on the public training data, content-based nearest neighbours, and internal validation are allowed. General-purpose pretrained models are allowed where their licences and the platform rules permit. Select models using training data, not hidden outcomes. What Not To Use Do not retrieve evaluation labels through source-text searches, source IDs, external copies of the revision histories, or checkpoints trained on hidden annotations. Do not predict from case IDs, filenames, sizes, row order, or hashes. Other participants' outputs, external inference services, and evaluator manipulation are prohibited. Opaque IDs do not make source text unsearchable; source lookup remains prohibited. &nbsp;
> 0 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Inflection Completion Across Unseen Paradigm Patterns

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70s20rc75zwj090wf2h58e2d8e8gs8
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview Predict ten missing written forms of a word from three observed forms and their grammatical labels. Return the ten spellings in the requested order. The dictionary headword is not supplied. When expanding a dictionary, observing a few forms does not settle every case, tense, or possessive ending. A useful model must infer the word's pattern and apply it to other grammatical requests, including changes inside the stem. The examples use real dictionary-derived Finnish, Hungarian, and Russian inflection records covering nouns, verbs, and adjectives. No spellings are invented or deliberately corrupted. Evaluation combines unfamiliar lexical families, unseen complete inflection patterns, and transfers between grammatical-feature groups that are not directly paired in training. Individual test feature bundles are represented in training. The task is to compose learned transformations, not guess undocumented grammatical labels or retrieve another word with the same complete ending table. Dataset All files are UTF-8 CSV. Parse CSV first, then the JSON strings inside its cells. No media files or model assets are needed. | File | Contents and exact column order | |---|---| | train.csv | 3,449 labeled cases: case_id,language,observed_forms,requested_features,completed_forms. | | test.csv | 834 cases: case_id,language,observed_forms,requested_features. | | sample_submission.csv | One schema-valid prediction per test ID, with case_id,completed_forms. It repeats the first observed spelling ten times and is only a format example. | Private answers.csv contains case_id,completed_forms, one reference array per test case. Training and test inputs have exactly the same columns after removing the training target. Fields | Column | Data type | Meaning | |---|---|---| | case_id | string | Opaque identifier: case_ followed by 24 hexadecimal characters. It contains no grammatical information. | | language | categorical string | fin: Finnish; hun: Hungarian; rus: Russian. | | observed_forms | JSON-encoded string | Exactly three pairs [feature_bundle,spelling], all from the same underlying word. The three spellings differ. | | requested_features | JSON-encoded string | Ordered array of ten distinct grammatical-feature strings. None is an observed bundle. Different requests may share a correct spelling. | | completed_forms | JSON-encoded string; target | Exactly ten complete spelling strings, aligned to the requests. These are words, not suffixes or edit commands. | Feature bundles are semicolon-separated labels in stable sorted order. For example, DAT;N;SG requests a singular noun's dative form. Feature order within a bundle has no grammatical significance; the order of the ten requests does. | Labels | Interpretation | |---|---| | N, V, ADJ | Noun, verb, adjective. | | SG, PL; 1, 2, 3 | Number and grammatical person. | | NOM, ACC, GEN, DAT, INST | Nominative, accusative, genitive, dative, instrumental case. | | MASC, FEM, NEUT; ANIM, INAN | Gender and animacy distinctions. | | PRS, PST, FUT; PFV, IPFV | Tense and aspect distinctions. | | IND, IMP, COND, POT, SBJV | Mood distinctions. | | ACT, PASS, MID; FIN, NFIN | Voice and finiteness. | | V.PTCP, V.CVB, V.MSDR | Participle, converb, verbal-noun feature labels. | | PSS1S, PSS1P, PSS2S, PSS2P, PSS3S, PSS3P | Possessive-agreement labels distinguishing person and number. | | AT+ABL, AT+ALL, AT+ESS, IN+ABL, IN+ALL, IN+ESS, ON+ABL, ON+ALL, ON+ESS | Spatial-case labels combining a spatial relation and case. The plus sign belongs to the label. | | ESS, TRANS, TERM, PRP, FRML, BYWAY | Additional case or adverbial-form distinctions. | | CMPR, POS; DEF, INDF | Comparison/polarity and definiteness distinctions, interpreted with the other bundle features. | | LGSPEC1, PSS4P, PSS4S | Source-specific conditioning labels. Learn their usage from labeled examples; do not interpret 4 as an ordinary fourth person. | Every full bundle used in test appears in training observations or targets. Not every theoretically possible combination is used. Labeled Example This is an actual training record. Accents are part of the spelling. | Field | Value | |---|---| | case_id | case_90be19810e3d25cff56069d1 | | language | hun | | observed_forms | [["N;NOM;PSS2P;SG","szirmotok"],["IN+ESS;N;SG","sziromban"],["AT+ESS;N;SG","sziromnál"]] | | requested_features | ["N;NOM;PL;PSS1S","N;SG;TRANS","INST;N;PL","DAT;N;SG","N;ON+ESS;SG","AT+ALL;N;SG","N;NOM;PSS2S;SG","N;PL;PSS4S","N;NOM;PL;PSS2P","N;PL;PRP"] | | completed_forms | ["szirmaim","szirommá","szirmokkal","sziromnak","szirmon","sziromhoz","szirmod","szirmoké","szirmaitok","szirmokért"] | Construction and Generalization Preparation normalizes Unicode to NFC and feature separators to semicolons. It excludes multiword records, slots with multiple recorded spellings, and paradigms without sufficient coverage. All three observations and ten targets come from actual entries for the same word and part of speech. Requested spellings are absent from the observations, and at least six requested spellings are distinct. Within each language, derivational relatives and words sharing any recorded inflected spelling are joined transitively before splitting. No such family can supply both training and test. Candidate selection is capped at 8,000 word/part-of-speech pairs per language before the final packet filters. An inflection pattern is the complete sorted list of retained feature bundles and spellings after removing the longest prefix shared by every spelling in that paradigm. It records the changing endings and stem material without the invariant word prefix. This is an exact orthographic grouping, not a claim that all linguistic conjugation classes have been discovered. Patterns are defined using the full retained source paradigm, not just the ten requests. The split selects 18% of candidate pattern groups by a fixed hash ordering for evaluation. If a training-pattern word is related to any selected test-pattern word, that training candidate is excluded. This quarantine prevents a related spelling from crossing the split without merging almost every pattern into one giant component. It removes 4,930 candidates before the final packet filters. Seven additional evaluation families are excluded because their packets contain a feature bundle unsupported in training. Neither filter uses model predictions or errors. No complete retained pattern or lexical family crosses the final split. The three observed spellings must share a common prefix no longer than 60% of the shortest observation. This input-based criterion emphasizes changes across the observed word forms; it does not select cases based on model mistakes. It also favors shorter stems and longer endings, so it is a cohort restriction rather than a proof of linguistic irregularity. A conservative source-quality filter excludes a paradigm if a recorded form repeats the headword's leading three letters more often than the headword itself. This catches some concatenated-alternative artifacts but can exclude valid forms and does not replace a complete linguistic review. The same criteria apply to training and test. Feature bundles are assigned to three stable partitions: 0, 1, and 2. These are experimental partitions, not linguistic categories. Training packets connect 0 with 1 or 1 with 2, in either direction. Test packets connect 0 with 2. Thus even the unordered observed-to-requested bundle pairs are held out. A directly memorized bundle-pair lookup is insufficient. All test requests connect to an observed bundle through the training feature-pair graph: 8,317 requests have a two-edge route and 23 need four edges. This verifies feature connectivity, not that every word-specific spelling change has already been shown. | Language | Train | Test | |---|---|---| | Finnish | 1,458 | 446 | | Hungarian | 446 | 55 | | Russian | 1,545 | 333 | | Total | 3,449 | 834 | | Part of speech | Train | Test | |---|---|---| | Noun | 327 | 30 | | Verb | 3,083 | 789 | | Adjective | 39 | 15 | The final sets contain 2,531 training and 737 test lexical families, and 608 training and 146 test inflection patterns. Test size is 24.2% of training size. Pattern and family isolation deliberately change the language proportions, so this is not an in-distribution random-row evaluation. This lexicographic resource is not a balanced speech corpus. Dialectal alternatives, rare forms, and annotation errors can exist. Evaluation uses the retained recorded spellings, not every linguistically acceptable alternative. Opaque identifiers do not make external dictionary lookup impossible. Submission Format Write ./working/submission.csv with exactly case_id,completed_forms, in that order. Both columns contain strings. Do not add an index or input columns. Each target cell is a JSON array of ten nonempty strings. Each spelling has at most 80 Unicode characters before normalization and may contain letters, combining marks, hyphens, or apostrophes, but no spaces. The complete JSON cell is capped at 4,096 characters before parsing, including JSON syntax and whitespace. Repeated spellings are allowed. Extra elements, numbers, booleans, nested arrays, objects, and explanatory prose are invalid. The example above serializes as: case_id,completed_forms case_90be19810e3d25cff56069d1,"[""szirmaim"",""szirommá"",""szirmokkal"",""sziromnak"",""szirmon"",""sziromhoz"",""szirmod"",""szirmoké"",""szirmaitok"",""szirmokért""]" The example uses a training ID for illustration; submit the actual test IDs. Each expected ID must appear exactly once. Row order may change. Extra, missing, duplicate, malformed, or unknown IDs and extra, missing, duplicated, or reordered columns reject the file. Schema failures are not silently repaired. Evaluation Metric: Compositional Inflection Completion Score. Minimum score: 0.0. Maximum score: 1.0. Higher is better. Score = 0.20 * FormAccuracy + 0.80 * CompleteParadigmAccuracy. Let N be the number of evaluated cases. Let y_ij and p_ij be the reference and predicted spellings for case i and request j, after NFC normalization. I(condition) is 1 when the condition holds and 0 otherwise. | Component | Exact formula | Weight rationale | |---|---|---| | FormAccuracy | sum_i sum_(j=1..10) I(y_ij = p_ij) / (10N) | *20%** preserves incremental credit for correct inflections. A copied stem with the wrong ending earns no credit. | | CompleteParadigmAccuracy | sum_i I(all ten predicted spellings match) / N | 80% makes a complete, correction-free lexical entry the primary unit of success. An entry with even one wrong form cannot receive this term. | For example, nine correct spellings earn 0.20 * 9/10 = 0.18 for that case; ten correct spellings earn 0.20 + 0.80 = 1.0. The large exact-entry term is deliberate and can create sharp score differences between models with similar per-form accuracy. It does not cap a strong solver's score. Matching is case-sensitive and diacritic-sensitive. NFC-equivalent spellings match. There is no edit-distance reward, synonym matching, prose evaluation, private class-frequency weighting, or hidden difficulty multiplier. All cases have equal weight. A malformed target cell contributes zero for all ten forms and for the complete case, while remaining in both denominators. Invalid reference targets raise an error. Schema and IDs are validated before parsing targets; references are never clipped or coerced. Reference Checks Exact reference predictions score 1.0. The observation-copy sample and training-mode baselines score 0.0. A public-training-only two-step suffix-transformation baseline scores 0.310671: form accuracy 0.627698 and complete-entry accuracy 0.231415. It cannot compose routes longer than two steps. These are local diagnostics, not a bound on better models; hosted agents must be evaluated on this revision. Modeling A compact character model can condition on the language, three labeled observations, and requested bundle. Treat bundles as conditioning features rather than fixed answer classes. For a quick non-neural starting point, learn spelling transformations between observed bundles and compose them through an intermediate bundle. Keep related words together in internal validation; randomly separating forms of the same word overestimates generalization. The budget remains 90 minutes on 10 CPU cores with 62.5 GiB RAM. Large-model training is not required; these small text files leave the budget for modeling rather than media decoding. What Not To Use Public-training-data models and permitted local pretrained models are allowed. Do not retrieve test answers from external dictionaries, underlying source tables, source-trained lookup databases, or other participants. Do not use external inference services or checkpoints specifically trained on held-out records. Source lookup is not an allowed substitute for inflection prediction. IDs, hashes, row order, CSV offsets, file sizes, hidden answers, evaluator internals, and repeated scoring queries must not be used as answer channels. Learning from spelling, grammatical features, and public training relationships is allowed. Inferring the feature-transfer structure from training is also allowed; it describes the learning problem rather than hidden spellings. &nbsp;
> 0 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Long-Form Technical Translation Across Unseen Topic Groups

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78m4q5dfad6pbpj1qr2sfe0h8e6mez
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview Translate complete multi-sentence English technical abstracts into Ukrainian when their technical topic groups are absent from training. Preserve quantities, cross-sentence relationships and terminology without adding explanations. Test passages are not shortened or split into independently scored sentences. Dataset There are 1,200 training pairs from 1,200 family-connected groups and 300 test abstracts from 300 different groups. Input-only TF-IDF representations, reduced to 48 dimensions, define 32 topic clusters; eight deterministic clusters are reserved for testing. Families and exact repeated bilingual abstracts are grouped before selection. Any group touching a held-out cluster is excluded from training. Test families with training-input cosine similarity above 0.8 under the fixed text representation, or with members outside the reserved topic set, are quarantined. Training and test examples are capped by deterministic source-text ordering only after the established family/topic split and overlap checks. No example moves between partitions, and full abstracts and reference translations are retained. This is topic-group transfer, not a guarantee that every semantic paraphrase is separated. No model score or held-out translation quality was used to choose the topic groups. Test selection additionally requires at least 700 English characters and three sentence-like segments, detected by terminal punctuation followed by an uppercase word. This deterministic source-text rule targets sustained translation rather than short formulaic entries; it is not a manually verified sentence segmentation. Training inputs contain 100–3,600 characters; test inputs contain 700–3,600. References contain 100–5,000 characters. Training retains both short and long passages, including long-form examples from non-held-out topics. Original translations may phrase or condense details differently, and residual alignment errors are possible. There is one reference per abstract. Submission Submit UTF-8 CSV with exactly task_id,ukrainian, in that order. Include every test ID once. Predictions must be strings of at most 10,000 characters; empty strings are allowed. task_id,ukrainian example,Пристрій містить датчик температури. Evaluation The metric is corpus BLEU-4, in [0, 1], using one reference per abstract. Normalize Unicode to NFC, retain case, and tokenize into Unicode word runs or individual non-whitespace punctuation characters (\w+|). Count 1-, 2-, 3- and 4-token n-grams separately within each abstract; n-grams never cross abstract boundaries. Clip matches to reference counts, then sum matched and submitted counts across the evaluation slice to obtain each precision p_n. BLEU = BP × exp((log(p_1) + log(p_2) + log(p_3) + log(p_4)) / 4) BP = exp(min(0, 1 − reference_token_count / submitted_token_count)) No smoothing is applied. Return zero if the submission has no tokens or any n-gram order has no submitted or matched n-grams. Gold scores 1. Non-string or overlength rows are treated as empty predictions; their full reference length remains in the brevity penalty. Invalid headers or ID sets are rejected. Row order has no effect. BLEU measures correctly translated word sequences rather than partial character overlap; its brevity penalty discourages returning only a few easy phrases. This is a standard translation metric, not a transformed chrF score. Single-reference BLEU can penalize valid alternative wording and is not a complete measure of factual or semantic correctness. Expected Approach Adapt a compact English-to-Ukrainian sequence model using the supplied abstracts. Translate each complete abstract, retaining quantities and cross-sentence terminology; a large generative model with lengthy explanations is unnecessary. For an efficient implementation: Cache tokenization and bucket batches by sequence length. Use short fine-tuning runs or parameter-efficient adaptation. Measure training-step and generation throughput before setting an epoch budget. Start with greedy decoding or a small beam. If an abstract exceeds the model's context limit, translate ordered sentence groups and reassemble every group; do not silently drop the ending. Validate on held-out training groups using corpus BLEU. Set generation lengths from observed training translations and check for truncated outputs. What Not To Use GPU training and general-purpose pretrained bilingual models are allowed. No external parallel training data, source copies, challenge-specific checkpoints, hard-coded translations, hosted APIs, manual test translation. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The complete solution must finish within 60 minutes end to end, including data loading, preprocessing, feature extraction, training or adaptation, validation, inference, structured decoding and submission writing. This is a total execution limit, not a separate allowance for each stage. The platform may terminate execution at the limit; use elapsed-time checks and retain the best completed model so that a valid submission is written before the deadline. Start with a small end-to-end run and write a valid full-test submission early. Use a wall-clock timer from process start, avoid exhaustive searches and large ensembles, and reserve at least the final 10 minutes for inference and submission checks; increase this reserve if measured throughput requires it. Cache encoder outputs only while the encoder is frozen. &nbsp;
> 0 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Predicting Grammar Marker Scopes In Constructed Sign-Gloss Text

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx753b9yhwkmjqe1mreasy7q7589qfwy
- DOMAIN exactly as displayed: Sequence To_Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Overview Gloss means a written label for a sign, This is a controlled sign-gloss-domain scope parsing benchmark built around a constructed notation. The corpus provides exact gold scope labels for a compact grammar-marker inventory, making it possible to test nested and overlapping span recovery without relying on restricted sign-language datasets or community-owned annotations. The benchmark value is controlled structured prediction: a model must learn how an unfamiliar gloss-like notation expresses layered scope structure from examples alone. It is designed for evaluating sequence parsers that recover exact marker boundaries, nested scopes, and overlapping spans under limited prior knowledge. A sign gloss is a written token notation for manual hand signs. For example, a constructed gloss sequence such as IX-1 WANT BUY BOOK TOMORROW should be read as a sequence of manual-sign gloss tokens, not as ordinary English prose. This challenge uses a purpose-built gloss notation and lexicon. You are given gloss_sequence, a whitespace-separated sequence of constructed manual-sign gloss tokens. Your task is to predict marker_spans, a JSON list of [marker_type, start_index, end_index] triples describing every non-manual marker scope in the sequence. Token indices are zero-based and inclusive. Spans can overlap or nest, so a flat BIO tagger that forces one label per token is not sufficient. Allowed marker_type values are benchmark labels named QUESTION_BROWS, WH_BROWS, COND_HEAD_TILT, TOPIC_BROWS, NEG_HEADSHAKE, ROLE_SHIFT, MOUTH_ADVERB, and EMPH_HEAD_NOD. The names are mnemonic scope categories in the constructed annotation scheme. The intended solution is to train a sequence model on public/train.csv, such as a small Transformer encoder with span heads, an encoder-decoder model that emits normalized JSON spans, or another supervised sequence parser initialized from scratch or lightly adapted from open weights. Prompt-only methods are not expected to work well because the notation, token distribution, and scope conventions are constructed for this dataset and must be learned from the labeled examples. What to use: train on the public labeled examples, validate on held-out training folds, and predict all spans jointly so overlapping scopes can be represented. Post-processing that checks JSON syntax and removes duplicate spans is acceptable. What not to do: do not use a handwritten parser that maps a few visible tokens to fixed spans, do not assume every marker covers the whole sentence, do not force a single non-overlapping label per token, do not use row order or sequence_id patterns, do not inspect or reconstruct the generator, do not use external sign-language corpora or private annotations, and do not use hosted closed-source APIs or leaked answer files. Submissions or writeups built around these invalid approaches may be rejected before payout even if they obtain a leaderboard score. Enforcement on Invalid Approaches: rule-only systems, prompt-only solutions, hosted-API solutions, generator reconstruction, leaked-answer use, and leaderboard submissions that do not train on the public examples can be rejected prior to payout. Evaluation For each row, the grader parses the submitted marker_spans JSON. A valid span is a three-item list [marker_type, start_index, end_index] where the marker type is from the allowed vocabulary, both indices are integers, 0 end_index, or duplicate spans, receives 0.0 credit for that row while the rest of the submission is still scored. Dataset The public data contains labeled training sequences, unlabeled test sequences, and a valid sample submission. The training labels and private answer file contain procedural gold marker spans from the constructed grammar, plus private robustness groups. File overview public/train.csv contains the input gloss sequence and the gold marker_spans label. public/test.csv contains the same input fields without labels. public/sample_submission.csv has the exact submission columns and a weak non-degenerate baseline. Training columns sequence_id is a salted opaque identifier and does not encode raw order or split membership. gloss_sequence is a whitespace-separated sequence of constructed gloss tokens. marker_spans is a JSON list of [marker_type, start_index, end_index] triples using zero-based inclusive token indices. Test columns The test file has no marker labels and no public construction-family, template, base-scenario, marker-count, or hidden subgroup columns. The solver should infer all marker spans from the gloss token sequence itself. Submission Submit a CSV with exactly two columns in this order: sequence_id, marker_spans. The submitted sequence_id set must match public/test.csv exactly, with one row per test sequence and no duplicates. marker_spans must be a JSON list; use [] only when predicting no marker spans for a row. Example submission: sequence_id,marker_spans seq_0b81f09a7c44,"[[""COND_HEAD_TILT"",1,3],[""QUESTION_BROWS"",0,6]]" seq_2417db78bd90,"[[""NEG_HEADSHAKE"",2,5]]" seq_d93a4a7e19cc,"[[""TOPIC_BROWS"",0,1],[""MOUTH_ADVERB"",4,6]]" &nbsp;
> 1d ago
> $400–$500
> Revision Requested

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Audience Response Density Bands

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71pg5s0xche6jcz89m0wpgtd8e6tys
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 0.168!

Full challenge description from page:

> Audience Response Density Trajectories Overview Given a cleaned spoken-comedy transcript, generate a fixed-length response profile describing how observed audience-response events are distributed through the performance. The input is one text sequence and the output is one ordered six-token sequence, so the benchmark measures sequence-to-sequence generation over an ordered trajectory. The transcript is divided into six contiguous windows with equal numbers of cleaned-word positions. Each output token is an event-count state for its corresponding window: 0 means no observed events, 1 means one event, 2 means two events, and 3 means three or more events. Timestamp text, bracketed event annotations, and literal laughter-response cue words are removed from the solver-visible transcript; the event stream remains available only for author-side target construction. The six-window resolution gives editorial review a finer but still compact map of where response concentrates. The hidden evaluation uses complete held-out recording collections that do not occur in training. This collection shift tests whether a system learns textual cues for where audience response concentrates instead of memorizing one recording context. A coherent six-token profile is useful for prioritizing transcript sections for editorial review, timing analysis, and downstream spoken-media quality checks. Dataset File descriptions train.csv — 2,019 labeled-input records containing the same transcript feature as test.csv; training targets are provided in the id-keyed train_targets.csv sidecar so train and test expose identical model-feature columns. train_targets.csv — 2,019 public training targets keyed by id. The integer target is a base-4 encoding of the six response-profile tokens and is never present for test ids. test.csv — 437 unlabeled-input records from three complete held-out recording collections, containing the same transcript feature as train.csv. sample_submission.csv — 437-row template with the exact submission schema and valid randomized six-token JSON sequences. Column descriptions id (string) — Opaque stable identifier for one deduplicated transcript record; copy it unchanged. transcript (string) — Solver-visible cleaned transcript text. Timestamp text, known bracketed event annotations, and literal laughter-response cue words are removed while the available spoken word order and wording are retained. target (integer) — In train_targets.csv only, the base-4 encoding sum(b_i * 4^(5-i)) for the six ordered response-profile tokens b_0 through b_5, each in {0, 1, 2, 3}. prediction (string) — Submission output in the exact form [b0,b1,b2,b3,b4,b5], encoded as a valid JSON array with each token an integer from {0, 1, 2, 3}. Split and leakage control The raw release has 28 source collection files. A collection boundary is the source authors' workbook membership field, so it is a complete program or recording-context grouping rather than a random row slice. Preparation fixes 25 source collections for training and three different complete source collections for the hidden evaluation before opaque ids, deduplication winners, or model outputs are created; no source collection is represented on both sides. The same URL can occur in more than one raw collection because the release contains aggregate and collection-specific rows. There are 209 such URL groups touching a held-out collection; preparation assigns every one of them to the held-out side before deduplication, so none can leak a test performance into training. After the 100-source-word eligibility filter and one-record-per-URL deduplication, preparation removes any candidate training record sharing a contiguous 20-word solver-visible token shingle with a hidden candidate record. This deterministic, label-free decontamination removes aggregate-compilation fragments that otherwise cross the collection boundary; it does not create or alter a test record. The final public split contains 2,019 training records and 437 hidden-test records. The hidden side is 21.6% of the training count, or 17.8% of the combined prepared records; this is the closest balanced three-collection holdout to the intended 15–25% range because the smallest valid holdout unit is a complete collection, not an arbitrary row sample. The three hidden collection cells contain 155, 121, and 161 records, with median source-cleaned transcript lengths of approximately 603, 1,015, and 618 words before response-cue scrubbing; training comes from the other 25 collections and has a different source-program mixture. The collection boundaries come from the source authors’ workbook-membership field: each boundary groups a complete program or recording-context mixture, not a random row slice. The three held-out groups are fixed before label construction, URL de-duplication, opaque-id generation, or model fitting; their source membership is absent from public files. The prepared train and test transcripts have zero exact overlap after lowercasing and removing non-word separators, and the shingle guard leaves zero shared contiguous 20-word solver-visible spans. Stable ids are generated from URL only after holdout membership is fixed, and the solver never receives URL, source collection, title, timestamp, or event-bearing fields. These controls make the evaluation a test of transfer to unseen collection structure and wording mixtures rather than row-order, URL, duplicate-text, aggregate-fragment, or source-membership memorization. Semantic near-duplicates shorter than the shingle guard are not claimed to be absent, so the intended claim is collection-level robustness under the documented source release. Evaluation Submissions are scored using Collection-Balanced Response Profile Score, a maximize metric in [0, 1]. The three hidden collections receive equal weight because they are independent recording contexts and the intended claim is robust generalization across contexts, not performance dominated by the largest collection. Within each collection, all six profile positions contribute equally. For each collection, the token-level macro-F1 term receives weight 0.75 because every response state at every profile position must remain identifiable; this is the primary signal and prevents an all-quiet shortcut from dominating. The ordinal utility term receives weight 0.15 because state codes have ordered meaning: confusing 1 with 2 is less severe than confusing 0 with 3, but this term alone is too forgiving of a majority-class prediction. The exact-profile term receives weight 0.10 because downstream review prioritization needs a coherent six-window trajectory, while avoiding a large bonus for an entirely quiet profile. The composite is then chance-corrected within each collection against that collection’s all-zero “no observed events” submission. Thus the no-event profile scores 0, a perfect profile scores 1, and only improvement over the documented majority-class floor contributes to the usable score band. The complete score definition is: import json import numpy as np from sklearn.metrics import f1_score STATE_CODES = [0, 1, 2, 3] PROFILE_LENGTH = 6 def parse_profile(value): if not isinstance(value, str): raise ValueError("prediction must be a JSON array string") parsed = json.loads(value) if ( not isinstance(parsed, list) or len(parsed) != PROFILE_LENGTH or any(isinstance(token, bool) or not isinstance(token, int) or token not in STATE_CODES for token in parsed) ): raise ValueError("prediction must be [b0,b1,b2,b3,b4,b5] with tokens in 0..3") return np.asarray(parsed, dtype=int) def collection_score(truth_profiles, predicted_profiles): truth = np.asarray([parse_profile(value) for value in truth_profiles], dtype=int) predicted = np.asarray([parse_profile(value) for value in predicted_profiles], dtype=int) truth_tokens = truth.reshape(-1) predicted_tokens = predicted.reshape(-1) token_macro_f1 = f1_score( truth_tokens, predicted_tokens, labels=STATE_CODES, average="macro", zero_division=0, ) ordinal_utility = np.mean(1.0 - np.abs(truth_tokens - predicted_tokens) / 3.0) exact_profile_rate = np.mean(np.all(truth == predicted, axis=1)) raw_score = ( 0.75 * token_macro_f1 0.15 * ordinal_utility 0.10 * exact_profile_rate ) no_event = np.zeros_like(truth) no_event_tokens = no_event.reshape(-1) no_event_macro_f1 = f1_score( truth_tokens, no_event_tokens, labels=STATE_CODES, average="macro", zero_division=0, ) no_event_ordinal_utility = np.mean(1.0 - np.abs(truth_tokens - no_event_tokens) / 3.0) no_event_exact_profile_rate = np.mean(np.all(truth == no_event, axis=1)) no_event_baseline = ( 0.75 * no_event_macro_f1 0.15 * no_event_ordinal_utility 0.10 * no_event_exact_profile_rate ) usable_band = 1.0 - no_event_baseline if usable_band <= 0: raise ValueError("the collection has no usable band above the no-event baseline") return float(np.clip((raw_score - no_event_baseline) / usable_band, 0.0, 1.0)) def evaluate(answer_frame, submission_frame): merged = answer_frame.merge(submission_frame, on="id", validate="one_to_one") scores = [] for collection in ["collection_0", "collection_1", "collection_2"]: part = merged[merged["evaluation_cell"] == collection] if len(part) == 0: raise ValueError("every hidden collection must be non-empty") scores.append(collection_score(part["truth_profile"], part["prediction"])) return float(np.mean(scores)) answer_frame is the evaluator's decoded hidden target view; truth_profile and evaluation_cell are not solver-visible columns. The private answer store keeps its prediction values submission-valid and may carry only the platform visibility metadata column; that metadata is not part of a solver submission. The grader rejects missing values, duplicate or unknown ids, wrong row counts, sequences other than six integer states, and non-finite scores. A valid prediction below the no-event baseline receives 0 after chance correction; malformed content in any row invalidates the submission rather than receiving partial row credit. The exact profile oracle scores 1.0. Submission Submit one UTF-8 CSV with exactly two columns: id,prediction. id (string) — Every id from test.csv, exactly once and unchanged. prediction (string) — A valid JSON array of six ordered response states in the form [b0,b1,b2,b3,b4,b5], with each token in {0, 1, 2, 3}. Example using real ids from this release: id,prediction comedy_003234c86c4cdee93d60,"[3,0,0,0,0,0]" comedy_004e71301860c2199904,"[0,0,0,1,0,0]" Requirements Write the submission to ./working/submission.csv. Include exactly 437 data rows, one for every id in test.csv; derive the row count from the file rather than hard-coding it. Keep the columns exactly id,prediction in that order. Do not add profile-position columns or hidden grouping fields. Each prediction must be valid JSON and decode to exactly six integer states from {0, 1, 2, 3}. Train from the supplied public transcript and train_targets.csv; use a learned sequence decoder or an equivalent learned multi-position model rather than a fixed profile prior. Validate with complete collection-aware folds or a held-out-collection split; a random row split alone overstates transfer to the hidden recording collections. A malformed prediction in any row rejects the whole submission; validate every row before writing the CSV. Run offline with the supplied files and finish within the selected NVIDIA A10G runtime budget. What Not To Use Do not reverse-map opaque ids, row order, or transcript ordering to recover a held-out profile. Do not obtain an outside copy of an event-bearing transcript, timestamp stream, recording, caption file, or metadata table to recover the hidden profile. Do not copy event tokens or timing annotations into the model input; those signals are intentionally absent from the cleaned transcript. Do not submit a manually keyed profile table, a constant six-token prior as the main method, or a hard-coded lookup keyed by text fragments; the profile must come from a learned model of the supplied public examples. Do not collapse the output to one token: the task requires the ordered six-window response sequence. &nbsp;
> 1 / 12 beat AI

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.


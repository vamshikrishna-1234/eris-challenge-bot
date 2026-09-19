# Prompt Engineering Challenge Examples

Scrape timestamp: 2026-07-02T00:00:00+05:30

Confirmed examples in this document: 3

These entries are included because the challenge detail page displayed this domain. Titles were not used for classification.

## Iron Phase Route Closure
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74zwwz8dnsrpsx5p1c4kg3z989pkxt
- DOMAIN exactly as displayed: Prompt Engineering
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↓ Lower is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> You are given short public profiles for iron-containing precursor phases, procedure cues, route cues, and four possible product phases. The task is to choose which product phase best closes the observed transformation route.
> This is a practical materials-chemistry task. Lab notes and mined papers often say that a precursor was aged, heated, oxidized, or reduced, but the useful downstream question is narrower: which product phase should be expected under those cues? The options in this benchmark are intentionally close. Many choices share the same oxide, sulfide, or oxyhydroxide family, and common products were filtered so a simple popularity rule is weak.
> Dataset
> File descriptions
> train.jsonl -- 2,622 labeled route-closure examples. Each line has id, context, options, prompt, correct_option, and completion.
> test.jsonl -- 837 route-closure examples with the same public fields except correct_option and completion.
> train.csv -- CSV mirror of the training examples with flattened option columns.
> test.csv -- CSV mirror of the test examples with flattened option columns.
> sample_submission.csv -- A template with random option letters in the required submission format.
> preparation_audit.json -- Split and metric summary for the prepared public files.
> Column descriptions
> id (string) -- Unique hashed row identifier.
> context (string) -- Precursor phase profile, procedure cues, route cues, and extraction confidence bucket.
> options (object, JSONL only) -- Four candidate product profiles keyed by A, B, C, and D.
> prompt (string, JSONL only) -- Instruction-style prompt containing the context and four options.
> completion (string, train only) -- Correct option letter for fine-tuning style training.
> correct_option (string, train only) -- Correct option letter, one of A, B, C, or D.
> option_A (string, CSV only) -- Product profile for option A.
> option_B (string, CSV only) -- Product profile for option B.
> option_C (string, CSV only) -- Product profile for option C.
> option_D (string, CSV only) -- Product profile for option D.
> predicted_option (string, submission only) -- Your selected product option for each test row.
> Evaluation
> Submissions are scored with phase-route regret, a bounded 0 to 100 loss. Lower is better.
> Each test row has a hidden loss for each option:
> correct product option: 0
> wrong but chemically close option: partial loss based on formula composition, phase family, and phase-state flags
> wrong and chemically distant option: higher loss, capped at 1
> Your final score is:
> def phase_route_regret(chosen_option_losses):
> return 100 * mean(chosen_option_losses)
> A random option submission scores around 59 on the prepared split. A product-frequency shortcut scores around 34, and a simple public-only text ranker scores around 27. There is still headroom for models that use the procedure cues and chemistry profiles more carefully.
> Submission
> Submit a CSV file with one prediction for every row in test.jsonl or test.csv.
> id (string) -- The hashed row identifier from the test file.
> predicted_option (string) -- One of A, B, C, or D.
> Example:
> id,predicted_option
> ipr_001f3d6f847a,B
> ipr_0033317c3225,B
> ipr_0039e4822868,D
> Requirements
> The file must contain exactly 837 rows plus the header.
> Every id from the test file must appear exactly once.
> predicted_option must contain only A, B, C, or D.
> File format: .csv only, with exact column names id,predicted_option.
> What Not To Use
> Do not try to recover the original source dataset, DOI values, source URLs, phase identifiers, or hidden reaction equations.
> Do not reverse search formulas or option sets against public source mirrors to look up the product option.
> Do not query chemistry or materials databases to map the candidate option set back to source pathway rows.

Inspiration note: Useful as a prompt-engineering pattern where solvers must design robust instructions or reasoning procedures for a constrained prediction target without changing the underlying model.

## Checkpoint Signal Recovery from Worked Solutions
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76nk8256c4nwbnhnerekw2g989mff5
- DOMAIN exactly as displayed: Prompt Engineering
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: feature-engineering, text, generative
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Worked solutions often contain a hidden checkpoint where an editor or data-cleaning system has marked the current line with a compact three-channel signal. The signal is not a written explanation; it is a small telemetry record describing whether the current line is locally sound, whether it fits the preceding work, and whether it preserves the intended destination of the solution.
> In this challenge, each row contains a math problem and a worked solution excerpt ending at one marked checkpoint. The visible checkpoint signal has been removed. Your task is to recover the missing JSON signal from the problem text and the surrounding solution excerpt.
> This is a structured record-imputation task. You are not asked to write the next solution step, generate a critique, or answer the math problem directly.
> Dataset
> The prepared public data contains 950 labeled training rows and 350 test rows. Each row was created by taking a worked-solution checkpoint, removing the visible signal text, and keeping the problem plus the solution excerpt as evidence.
> Files:
> train.csv: Labeled examples with public fields and answer_json.
> test.csv: Unlabeled examples with the same public task fields.
> sample_submission.csv: Valid baseline submission with the required columns.
> Columns:
> id (string): Unique task id.
> prompt (string): Task instruction.
> problem_text (string): Math problem associated with the excerpt.
> reasoning_trace (string): Worked solution excerpt ending at the checkpoint.
> tag_schema_json (JSON object): Allowed output keys and values.
> answer_json (JSON object, train only): Correct checkpoint signal.
> Submission Format
> Submit a CSV with exactly these columns, in any order:
> id
> answer_json
> answer_json must be a JSON object with exactly these keys:
> math_reasoning: local line signal.
> logic_consistency: continuity-with-excerpt signal.
> final_correctness: destination-preservation signal.
> Each value must be "+" or "-".
> Example answer_json value:
> {"math_reasoning":"+","logic_consistency":"-","final_correctness":"-"}
> Example submission CSV:
> id,answer_json
> pstr_33aab39672cb080fd0,"{""math_reasoning"":""+"",""logic_consistency"":""+"",""final_correctness"":""+""}"
> pstr_ce5490e3f2c5b72e0b,"{""math_reasoning"":""-"",""logic_consistency"":""-"",""final_correctness"":""-""}"
> Evaluation
> Each row receives a score from 0 to 1:
> row_score = 0.38 exact_object + 0.36 component_accuracy + 0.16 relation_score + 0.10 destination_signal_score
> Metric definitions:
> exact_object: 1 when all three submitted keys match the true record, otherwise 0.
> component_accuracy: Fraction of the three keys that match. Possible values are 0, 1/3, 2/3, or 1.
> relation_score: 1 when the submitted equality relationship between math_reasoning and logic_consistency matches the true equality relationship. For example, if the true record has those two keys equal and the submission also has them equal, this term is 1.
> destination_signal_score: 1 when final_correctness matches, otherwise 0.
> The final leaderboard score is the arithmetic mean of row_score across all test rows.
> What Not To Use
> Hardcoded mappings from task ids to answers.
> Manual lookup of original upstream examples.
> External copies of the exact generated public/test rows.
> Hidden files or answer files not included in the public data.
> Reconstructing answers from package-generation internals.

Inspiration note: Useful as a prompt-engineering pattern where solvers must design robust instructions or reasoning procedures for a constrained prediction target without changing the underlying model.

## Disaster Scene Multimodal Incident Ledger Prediction
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx721x4yp3cqa608e7spw2d30989w8yn
- DOMAIN exactly as displayed: Prompt Engineering
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, multimodal
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Each example asks participants to reconcile a disaster image, expert visual questions, and a conflicting incident briefing. The task is to predict a structured incident ledger: visible hazard indicators, a response priority matrix, which question IDs support the decision, which briefing claim IDs contradict the image, an ordered dispatch sequence, and an incident status class.
> This challenge uses image evidence together with language evidence, but the required outputs are structured artifacts rather than free-form prose. Score range: minimum possible score is 0.0, maximum possible score is 1.0. Higher is better.
> The challenge combines image-grounded disaster understanding with structured language evidence. A solver has to read the scene, use the QA bundle as evidence, detect contradictions in a briefing, and output multiple structured artifacts that must agree with one another.
> Dataset
> The prepared dataset contains:
> Item	Value
> Training rows	1500
> Test rows	420
> Exact submission score	1.0
> Sample submission score	0.177105
> The prepared files are:
> Path	Type	Description
> public/train.csv	CSV file	1,500 training rows with public inputs and target columns.
> public/test.csv	CSV file	420 test rows with public inputs only.
> public/images/	directory	Images referenced by image_path in train and test rows.
> public/sample_submission.csv	CSV file	Valid submission template with all required output columns.
> Input Columns
> Column	Type	Description
> sample_id	string	Opaque public identifier.
> image_path	string	Relative path to the public disaster image.
> question_bundle	string	Question IDs and disaster-scene questions without answers. Public question text does not include source crisis-code labels.
> incident_briefing	string	Briefing claim IDs that may agree or disagree with the image.
> crisis_taxonomy_card	string	Short crisis-information taxonomy used to interpret question evidence, visual hazard categories, and dispatch constraints.
> Target Columns
> Column	Type	Description
> hazard_state_vector	JSON integer array	Length-8 vector with binary visible hazard and response indicators. Valid values are 0 or 1.
> response_priority_matrix	JSON integer matrix	Four by four matrix of response priority values. Valid values are integers from 0 through 3.
> evidence_question_set	pipe-separated token set	Question IDs whose question-answer evidence supports the response decision, or none. These IDs are not recoverable from visible crisis-code tags.
> contradiction_flag_set	pipe-separated token set	Briefing claim IDs contradicted by visual evidence, or none.
> dispatch_sequence	ordered token sequence	Dispatch actions separated by >, such as assess>cordon>utility_check.
> incident_status	categorical string	One of monitor, respond, urgent, or critical.
> Submission Format
> Submit a CSV with exactly these columns:
> sample_id,hazard_state_vector,response_priority_matrix,evidence_question_set,contradiction_flag_set,dispatch_sequence,incident_status
> Example submission row:
> incident_eb9f06cbccba9525,"[0,0,0,0,0,0,0,0]","[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]",none,none,assess,monitor
> Every sample_id from public/test.csv must be present exactly once. Duplicate rows are deduplicated by keeping the first occurrence. Extra columns are ignored. Missing required columns or an incorrect ID set cause grading to fail.
> Evaluation
> The final score is a weighted average:
> Score =
> 0.24 * HazardVectorScore
> + 0.22 * PriorityMatrixScore
> + 0.15 * EvidenceSetScore
> + 0.14 * ContradictionSetScore
> + 0.14 * DispatchSequenceScore
> + 0.11 * IncidentStatusScore
> Component Summary
> Component	Column	Weight	Details
> HazardVectorScore	hazard_state_vector	0.24	shape 8; range 0 to 1
> PriorityMatrixScore	response_priority_matrix	0.22	shape 4x4; range 0 to 3
> EvidenceSetScore	evidence_question_set	0.15	Splits on `
> ContradictionSetScore	contradiction_flag_set	0.14	Splits on `
> DispatchSequenceScore	dispatch_sequence	0.14	Splits tokens on >, then scores 0.30 * normalized_Levenshtein_similarity + 0.70 * exact_sequence_match.
> IncidentStatusScore	incident_status	0.11	valid values: monitor, respond, urgent, critical
> Metric Details
> matrix: The grader parses the submitted JSON with the required shape, rejects strings over 5000 characters, and gives zero for invalid JSON, wrong shape, or non-finite values. Predictions are clipped to the configured range and rounded to integers. Active entries are positions where the truth or prediction is nonzero. Entry credit is exact equality on active entries, with truth nonzero entries weighted 3.0 and other active entries weighted 1.0. Row score is 0.45 * active_entry_score + 0.55 * exact_array_match.
> set: Text is lowercased, spaces are removed, and |, ;, and , are accepted as delimiters. Empty or none means an empty set. Sets over 120 tokens, tokens over 120 characters, or strings over 12000 characters are treated as empty. Row score is 0.38 * token_F1 + 0.62 * exact_set_match.
> seq: Text is lowercased, spaces are removed, and tokens are split on >. Sequences over 80 tokens, tokens over 120 characters, or strings over 12000 characters score zero. Row score is 0.30 * normalized_Levenshtein_similarity + 0.70 * exact_sequence_match, where similarity is 1 - edit_distance / max(true_length, pred_length).
> category: Categorical component. Submitted labels are stripped and lowercased. Values outside the listed valid classes are treated as invalid predictions. The component is inverse-frequency weighted macro F1 over ground-truth classes present in the test set, with class weights 1 / sqrt(class_count + 1) capped at five times the median class weight and then normalized.
> After component scores are computed, the weighted sum is clipped to [0.0, 1.0]. An exact submission scores 1.0. The provided sample submission scores approximately 0.177105.
> What Not To Use
> Do not use lookup tables or deterministic mappings from sample_id, file names, raw source order, public row order, image hashes, compression artifacts, or split artifacts to target values.
> Do not infer target values from source dataset crisis codes, hidden source annotations, omitted answer labels, or any external mirror of the source dataset. The public question bundle intentionally omits source crisis-code labels, and a valid solution should use the supplied public image and language inputs.
> Do not hardcode labels for individual public rows, scrape private answer files, modify the grader, or exploit duplicate records. A valid solution should infer the structured outputs from the supplied public image and language inputs.

Inspiration note: Useful because it shows how prompt-controlled reasoning or multimodal interpretation can be scored through a compact target artifact.

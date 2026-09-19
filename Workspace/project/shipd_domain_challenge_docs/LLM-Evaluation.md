# LLM Evaluation Challenge Examples

Scrape timestamp: 2026-07-02T00:00:00+05:30

Confirmed examples in this document: 4

These entries are included because the challenge detail page displayed this domain. Titles were not used for classification.

## Execution-Free CUDA Kernel Performance Ranking
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79k8et32kbn6c4py1bevp4w189exzg
- DOMAIN exactly as displayed: LLM Evaluation
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> This challenge is an execution-free CUDA performance ranking benchmark.
> Each sample contains one PyTorch reference operation and eight generated CUDA/C++ kernel candidates that attempt to implement the same operation. All eight candidates are presented as source code. Participants do not write a new kernel, compile code, run CUDA, or benchmark anything. Instead, they must inspect the PyTorch reference and the candidate implementations, then assign scores so that the best hidden performer is ranked highest.
> The benchmark is designed around a realistic bottleneck in automated GPU optimization. Modern coding agents can generate many plausible CUDA kernels for the same operation, but generation alone is not enough. The system still needs to decide which candidate is worth trusting, benchmarking, or deploying. This challenge isolates that selection problem.
> The public candidate kernels are not arbitrary broken programs. During preparation, candidates are filtered from raw AI-generated CUDA attempts so that public portfolios contain plausible working implementations with non-empty source code, non-empty PyTorch references, correctness validation, and positive measured speed utility. The task is therefore not simple error detection. It is performance reasoning over competing correct-looking implementations.
> A strong solution must compare multiple kernels for the same operation and reason about tensor shapes, indexing logic, memory access patterns, coalescing, launch geometry, block and grid choices, occupancy, synchronization, shared memory, branching, redundant computation, arithmetic intensity, and likely runtime behavior.
> Motivation
> Most CUDA benchmarks focus on generation: can a model write a correct kernel, can it repair a broken kernel, or can it improve a single implementation. This challenge focuses on a different and under-tested step: selection.
> In practice, an AI system may produce several kernels that all appear valid. Some will be simple but fast. Some will look sophisticated but waste work. Some will use shared memory where global memory access would have been cheaper. Some will tile or vectorize in a way that helps only for certain tensor shapes. Some will be correct but lose performance through poor launch geometry, uncoalesced memory access, excessive synchronization, unnecessary branching, or low occupancy.
> Benchmarking every candidate can be expensive, especially inside larger optimization loops. A useful CUDA judge should be able to look at a portfolio of generated kernels and identify which implementation is most likely to win before execution.
> This benchmark asks whether a model can act like that judge.
> Task
> Given a PyTorch reference implementation and eight CUDA/C++ candidate implementations for the same hidden operation task, submit one numeric score for each candidate.
> Higher scores should mean that the candidate is more likely to be the hidden best performer in that portfolio. The candidate with the highest submitted score is treated as the predicted top pick.
> Scores do not need to be probabilities. They do not need to be bounded between 0 and 1. They do not need to sum to 1. Only the within-portfolio ranking induced by the submitted scores matters.
> Prepared Dataset
> The released challenge data contains train.csv, test.csv, and sample_submission.csv.
> train.csv contains labeled training portfolios. Each row is one CUDA ranking portfolio with one PyTorch reference operation, eight CUDA/C++ candidate implementations, and one best_candidate label.
> test.csv contains unlabeled evaluation portfolios. It has the same public input columns as train.csv, but best_candidate is hidden.
> sample_submission.csv contains the required submission format. It has one row per test portfolio and eight score columns, one score for each candidate.
> Each portfolio always contains exactly eight CUDA candidates for the same hidden operation task. The public files do not expose raw operation names, source levels, task IDs, kernel names, correctness labels, dense utility values, runtime fields, speedup fields, numerical-difference fields, error logs, profiler output, static-analysis output, upstream row indices, or hidden grouping metadata.
> The split is performed using hidden operation grouping. When possible, related operation families are separated between train and test. This makes the task closer to real generalization: participants should learn CUDA performance reasoning, not memorize operation-specific winners.
> train.csv Columns
> sample_id is a string. It is a unique public identifier for the training portfolio. It is used for row matching only and should not be used as a predictive shortcut.
> pytorch_code_module is a string. It contains the PyTorch reference implementation written in module form.
> pytorch_code_functional is a string. It contains the PyTorch reference implementation written in functional form.
> candidate_1_cuda_code through candidate_8_cuda_code are strings. Each column contains the CUDA/C++ source code for one generated candidate implementation.
> best_candidate is an integer from 1 to 8. It is the training label. A value of 1 means candidate_1_cuda_code was the hidden best performer in that portfolio. A value of 8 means candidate_8_cuda_code was the hidden best performer.
> test.csv Columns
> sample_id is a string. It is a unique public identifier for the test portfolio.
> pytorch_code_module is a string. It contains the PyTorch reference implementation written in module form.
> pytorch_code_functional is a string. It contains the PyTorch reference implementation written in functional form.
> candidate_1_cuda_code through candidate_8_cuda_code are strings. Each column contains one CUDA/C++ candidate implementation for the same reference operation.
> test.csv does not include best_candidate, runtime fields, utility values, correctness labels, source task metadata, profiler output, static-analysis output, or hidden ranks.
> sample_submission.csv Columns
> sample_id is a string. It must match a sample_id from test.csv.
> candidate_1_score through candidate_8_score are numeric values. Higher scores indicate that the corresponding candidate is more likely to be the hidden best performer.
> Scores are used only to rank candidates within each portfolio.
> Submission Format
> Submit a CSV with exactly these columns in exactly this order:
> sample_id, candidate_1_score, candidate_2_score, candidate_3_score, candidate_4_score, candidate_5_score, candidate_6_score, candidate_7_score, candidate_8_score
> Each sample_id must appear exactly once. All candidate_i_score values must be finite numeric values.
> Example submission:
> sample_id,candidate_1_score,candidate_2_score,candidate_3_score,candidate_4_score,candidate_5_score,candidate_6_score,candidate_7_score,candidate_8_score
> TS000001,0.12,0.91,0.33,0.04,0.78,0.20,0.16,0.55
> TS000002,0.81,0.11,0.06,0.38,0.72,0.44,0.09,0.15
> TS000003,0.03,0.21,0.67,0.64,0.08,0.32,0.17,0.95
> Invalid submissions include missing rows, extra rows, duplicate sample_id values, missing columns, extra columns, columns in the wrong order, non-numeric scores, NaN values, or infinite values.
> Evaluation
> Submissions are scored using the CUDA Top-Pick Score on a 0 to 100 scale. Higher is better.
> For each test sample, the submitted candidate scores are sorted from highest to lowest. The hidden best candidate is the candidate with the highest private measured utility.
> The final score is:
> 100 * (
> 0.60 * Top1ExactAccuracy
> + 0.20 * MeanReciprocalRank
> + 0.10 * PairwiseRankAccuracy
> + 0.10 * HardCaseScore
> )
> Top1ExactAccuracy is the fraction of test portfolios where the highest-scored submitted candidate is exactly the hidden best candidate.
> MeanReciprocalRank gives partial credit for ranking the hidden best candidate near the top. If the hidden best candidate is ranked first, the reciprocal rank is 1.0. If it is ranked second, the reciprocal rank is 0.5. If it is ranked eighth, the reciprocal rank is 0.125. This component is the mean reciprocal rank across all test portfolios.
> PairwiseRankAccuracy measures whether the submitted ordering agrees with the hidden utility-derived ordering. For each portfolio, all 28 candidate pairs are compared. A pair receives full credit if the candidate with better hidden utility receives the higher submitted score. Tied submitted scores receive half credit. This component is averaged across all candidate pairs and all test portfolios.
> HardCaseScore is computed on a deterministic hidden hard-case subset. During preparation, a test portfolio is marked as a hard case if at least one private difficulty condition is met, such as high source difficulty, a small utility gap between the best and second-best candidates, a small utility spread across all candidates, or several candidates clustered close to the best candidate. The hard-case flag is fixed in the private answers file before evaluation and does not depend on participant submissions.
> On the hard-case subset, the grader computes HardTop1ExactAccuracy, HardMeanReciprocalRank, and HardPairwiseRankAccuracy using the same definitions as above. The hard-case component is:
> HardCaseScore =
> 0.60 * HardTop1ExactAccuracy
> + 0.25 * HardMeanReciprocalRank
> + 0.15 * HardPairwiseRankAccuracy
> If the hidden test split contains no hard-case rows, HardCaseScore is computed over the full test set.
> Intended Methods
> Participants may use code language models, static feature extraction, CUDA-specific heuristics, ranking models, supervised classification, transformer encoders, LLM-based candidate judging, or lightweight CPU-based code analysis.
> Useful approaches may include parsing CUDA indexing patterns, comparing CUDA logic against the PyTorch reference, detecting memory coalescing, estimating arithmetic intensity, estimating thread-block utilization, detecting redundant computation, detecting expensive synchronization, identifying likely occupancy problems, and learning top-pick classifiers from best_candidate.
> The challenge can be solved with normal CPU-based text and code modeling. Participants are not required to compile or execute CUDA kernels.
> Rules
> Participants should predict from the provided PyTorch reference code and candidate CUDA code.
> Participants must not use hidden test labels, private answer files, hidden runtimes, hidden speedups, hidden correctness labels, raw source rows for test examples, operation IDs, candidate names, compiler logs, profiler outputs, static-analysis outputs, row order, or sample IDs as shortcuts.
> The intended behavior is execution-free CUDA performance reasoning from public source code.

Inspiration note: Useful as an LLM-evaluation pattern where models judge or rank code artifacts from static context, with a strict comparison target and no execution during inference.

## Protein Function Repair Evaluation
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx716fta50ekd450f0mx1k01ns89t1dn
- DOMAIN exactly as displayed: LLM Evaluation
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↓ Lower is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Protein function annotation systems often produce long ontology-style predictions across three aspects: molecular function (MF), biological process (BP), and cellular component (CC). In practice, a reviewer does not only need another predicted term list. They need to decide which aspect of the model output is least aligned with curator evidence and should be repaired first.
> In this challenge, each row contains an anonymized protein context packet and a model-generated ontology prediction. Your task is to rank the three aspects from most in need of repair to least in need of repair. The hidden target is derived from the model prediction's agreement with held-out curator annotations for each aspect.
> This is a compact LLM-evaluation and fine-tuning style problem: a good solution should learn when a model's molecular-function, biological-process, or cellular-component text is likely to be the weakest part of the annotation. The temporal holdout makes simple priors brittle because the test proteins come from a shifted evaluation split.
> Dataset
> File descriptions
> train.csv -- 3,200 labeled protein-context packets with anonymized features and the target column ranked_aspects.
> test.csv -- 1,200 unlabeled protein-context packets with the same public feature columns but without ranked_aspects.
> train.jsonl -- Fine-tuning-style mirror of the labeled training rows with prompt and completion fields.
> test.jsonl -- Fine-tuning-style mirror of the unlabeled test rows with prompt fields.
> sample_submission.csv -- A template showing the required submission format with random valid aspect permutations.
> Column descriptions
> id (string) -- A 12-character hashed row identifier.
> sequence_profile (string) -- Lossy amino-acid composition features and sequence length. Exact amino acid sequences are not included.
> location_hints (string) -- Normalized localization keywords.
> function_terms (string) -- Lossy function-description keywords with source identifiers removed.
> domain_hints (string) -- Normalized protein-domain keywords with source accessions and exact span coordinates removed.
> model_prediction_text (string) -- The model-generated ontology-style prediction text, grouped by MF, BP, and CC, with ontology identifiers removed.
> context_packet (string) -- A newline-delimited text packet combining the public evidence fields for fine-tuning or text classification.
> ranked_aspects (string) -- Target column in train.csv only. A pipe-separated permutation of MF, BP, and CC, ordered from most in need of repair to least in need of repair.
> Evaluation
> Submissions are scored using Aspect Repair Ranking Loss. Lower is better.
> For each row, the hidden evaluator computes the true MF, BP, and CC agreement scores between the model prediction and curator annotations. Your submitted ranking is penalized for pairwise inversions: if an aspect with lower hidden agreement is placed after an aspect with higher hidden agreement, the penalty is the absolute agreement-score gap for that pair. The row loss is normalized by the maximum possible inversion penalty for that row and scaled to 0-100.
> def row_loss(predicted_rank, hidden_scores):
> # hidden_scores maps MF/BP/CC to hidden agreement scores.
> # Lower hidden agreement means the aspect needs repair sooner.
> raw_loss = 0.0
> max_loss = 0.0
> for aspect_a, aspect_b in [("MF", "BP"), ("MF", "CC"), ("BP", "CC")]:
> gap = abs(hidden_scores[aspect_a] - hidden_scores[aspect_b])
> max_loss += gap
> if hidden_scores[aspect_a] < hidden_scores[aspect_b]:
> raw_loss += gap if predicted_rank.index(aspect_a) > predicted_rank.index(aspect_b) else 0
> elif hidden_scores[aspect_b] < hidden_scores[aspect_a]:
> raw_loss += gap if predicted_rank.index(aspect_b) > predicted_rank.index(aspect_a) else 0
> return 0.0 if max_loss == 0 else 100.0 * raw_loss / max_loss
> score = mean(row_loss(row_prediction, row_hidden_scores) for each test row)
> Submission
> Submit a CSV file with one prediction for every row in test.csv.
> id (string) -- The 12-character identifier from test.csv.
> ranked_aspects (string) -- A pipe-separated permutation of MF, BP, and CC, ordered from most repair-needed to least repair-needed.
> Example:
> id,ranked_aspects
> 0051aad50d65,CC|MF|BP
> 0061786a6f36,BP|CC|MF
> Requirements
> The file must contain exactly 1,200 rows plus a header.
> Every id from test.csv must be present exactly once.
> ranked_aspects must be one of: MF|BP|CC, MF|CC|BP, BP|MF|CC, BP|CC|MF, CC|MF|BP, or CC|BP|MF.
> File format: .csv only, with exact column names id,ranked_aspects.
> What Not To Use
> Do not reverse-search public protein text, domain hints, interaction-like wording, or prediction snippets to recover the original protein accession or held-out curator annotations. That bypasses the intended repair-ranking task.
> Do not use external protein annotation databases, ontology annotation mirrors, or accession-recovery workflows to look up MF/BP/CC annotations for the test rows. The challenge is to learn from the supplied public training packets.
> Do not reconstruct exact amino acid sequences or source identifiers from public lossy features for lookup-based labeling. Exact sequences and accessions are intentionally withheld.
> Do not submit a pure hand-written keyword map that assigns rankings without training or fitting a model on the public labeled rows. The task is meant to evaluate learned repair-prior modeling under temporal shift.

Inspiration note: Useful because it converts qualitative model-output assessment into a structured, reproducible scoring target.

## Educational Grade Review Queue
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fq27sdz90nc8w52g95z8ehd89akqc
- DOMAIN exactly as displayed: LLM Evaluation
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Educational assessment systems often collect more written responses than instructors can inspect one by one. The practical problem is deciding which answers should be reviewed first: a short answer is not automatically bad, and a long answer is not automatically sound. In this challenge, each record contains a real anonymized student answer, the question prompt, and the human-written rubric used to judge that answer. Your task is to assign a severity score that pushes responses with unusually large rubric gaps to the top of each review queue.
> The hidden test set uses substantive question groups that are absent from the labeled training data. That means a model cannot win by memorizing a prompt, a rubric, repeated option letters, or a row pattern. It has to read the task, parse the scoring criteria, inspect the answer, and decide which responses most clearly fail the expected standard.
> This is a practical assessment-review ranking benchmark with an LLM-evaluation use case, not a generic text regression task. A useful model needs the same core skill expected from rubric-based evaluators: turn natural-language grading criteria into a reliable review priority order for new questions. The hidden target removes a nonlinear answer-length baseline within each question group, so short-answer triage and answer-key parsing are not reliable strategies. Strong submissions should combine semantic answer understanding with group-wise ranking calibration.
> Dataset
> File descriptions
> train.jsonl -- 502 labeled assessment review records. Each JSON object contains the public text fields and the target column rubric_loss_score.
> test.jsonl -- 268 unlabeled assessment review records from held-out question groups, with the same public fields but without rubric_loss_score.
> train.csv -- CSV mirror of train.jsonl for solvers who prefer tabular tooling.
> test.csv -- CSV mirror of test.jsonl.
> sample_submission.csv -- A template showing the required submission format with random numeric severity scores.
> Column descriptions
> id (string) -- A 12-character hashed row identifier.
> question_group (string) -- A hashed group identifier. Scores are computed separately within each group.
> question_type (string) -- Response format category.
> max_points (float) -- Maximum available credit for the question.
> human_criteria_count (integer) -- Number of rubric criteria in the public human-created rubric text.
> response_word_count (integer) -- Word count for the cleaned answer.
> question_text (string) -- Cleaned question prompt.
> human_rubric_text (string) -- Cleaned human-created rubric criteria, descriptions, and scoring guidance.
> student_response_text (string) -- Cleaned anonymized answer.
> rubric_loss_score (float) -- Target column in train.jsonl and train.csv only. Higher values mean the answer has a larger rubric gap than expected after nonlinear answer-length adjustment within its question group.
> Evaluation
> Submissions are scored using mean capped weighted pairwise concordance by question group. Higher is better.
> For each question group, every pair of rows with different hidden rubric_loss_score values is compared. A pair is concordant when the row with the larger hidden score also has the larger submitted score. Pairs with larger hidden-score gaps receive more weight. Tied predictions receive half credit for that pair. The final score is the average across question groups.
> def weighted_pairwise_concordance(group):
> numerator = 0.0
> denominator = 0.0
> for left, right in all_pairs(group):
> delta = true_score[left] - true_score[right]
> if delta == 0:
> continue
> weight = min(abs(delta), 20.0)
> denominator += weight
> pred_delta = predicted_score[left] - predicted_score[right]
> if pred_delta * delta > 0:
> numerator += weight
> elif pred_delta == 0:
> numerator += 0.5 * weight
> return numerator / denominator
> score = mean(weighted_pairwise_concordance(group) for each question_group)
> The weight cap keeps the metric from being dominated by a few obvious extreme pairs. A useful submission should order the whole review queue, not only identify blanks or very short answers.
> Submission
> Submit a CSV file with one prediction for every row in test.jsonl or test.csv.
> id (string) -- The 12-character identifier from the test split.
> rubric_loss_score (float) -- Your numeric severity score. Larger values should indicate greater expected rubric loss within that row's question_group.
> Example:
> id,rubric_loss_score
> 0031378eb7ef,73.2
> 00d3d8a44cc1,14.8
> Requirements
> The file must contain exactly 268 rows plus a header.
> Every id from the test split must be present exactly once.
> rubric_loss_score values must be finite numeric values.
> File format: .csv only, with exact column names id,rubric_loss_score.
> What Not To Use
> Do not search for or use external copies of the original assessment data to recover hidden labels for the held-out responses.
> Do not reverse-map hashed row or question identifiers back to source response IDs, participant IDs, assignment IDs, or question IDs.
> Do not use outside score tables, published score extracts, or label mirrors to look up held-out rubric-loss values.
> Do not derive scores by parsing answer-key phrases such as correct option letters from rubric text. The hidden target is not a multiple-choice answer-key recovery task.
> Do not submit a fixed hand-written shortcut based only on answer length or row order. The target is intentionally adjusted so length-only triage should not dominate.

Inspiration note: Useful because it converts judgment quality, calibration, or arbitration into a measurable evaluator benchmark.

## LLM Judge Pairwise Calibration Arbitration
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cm2kdtzc0x3m4yq1hz857ms89v9kf
- DOMAIN exactly as displayed: LLM Evaluation
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Data
> The public files are:
> train.csv: pairwise calibration rows with two public rationale packets and the target arbitration_card.
> test.csv: hidden test rows with the same public fields but without arbitration_card.
> sample_submission.csv: schema-valid dummy predictions.
> The private evaluation file is a hidden id,arbitration_card answer table used only by the grader.
> The train/test split is source-record disjoint. Hidden test pairs are built only from judge cases that do not appear in train pairs.
> Public Columns
> id: anonymized pair id.
> packet_context: constant sentence describing the two-case arbitration packet.
> case_a_rationale: score-redacted rationale text for the first judge case.
> case_a_length_bin: short, medium, or long.
> case_a_quality_hint: mostly_positive, mostly_negative, or mixed_or_sparse.
> case_a_refusal_cue: yes or no.
> case_a_grounding_cue: yes or no.
> case_a_coverage_cue: yes or no.
> case_a_resolution_cue: yes or no.
> case_a_safety_cue: yes or no.
> case_b_rationale: score-redacted rationale text for the second judge case.
> case_b_length_bin: short, medium, or long.
> case_b_quality_hint: mostly_positive, mostly_negative, or mixed_or_sparse.
> case_b_refusal_cue: yes or no.
> case_b_grounding_cue: yes or no.
> case_b_coverage_cue: yes or no.
> case_b_resolution_cue: yes or no.
> case_b_safety_cue: yes or no.
> pair_quality_pattern: compact summary such as case_a=mostly_negative|case_b=mostly_positive.
> pair_length_pattern: compact summary such as case_a=short|case_b=medium.
> arbitration_card: target column, present only in train.csv and private answers.
> Example Training Row
> A public training row may contain:
> id: LJA_TR_0007
> case_a_rationale: The answer is grounded in the retrieved passage but omits one required eligibility condition.
> case_a_quality_hint: mixed_or_sparse
> case_b_rationale: The response refuses the request and redirects the user to an appropriate professional channel.
> case_b_quality_hint: mostly_positive
> pair_quality_pattern: case_a=mixed_or_sparse|case_b=mostly_positive
> arbitration_card: priority=case_a;axis_relation=safety_vs_coverage;score_gap=medium;review_route=manual_compare
> The exact values above are illustrative of the schema. Participants should learn the mapping from the actual training rows.
> Target Format
> Submit a CSV with exactly these columns:
> id
> arbitration_card
> Each arbitration_card must contain exactly four ordered slots:
> priority=<value>;axis_relation=<value>;score_gap=<value>;review_route=<value>
> Valid priority values are:
> case_a: case A should be prioritized as the weaker or riskier judge case.
> case_b: case B should be prioritized as the weaker or riskier judge case.
> tie: the two cases are effectively tied.
> Valid axis_relation values are:
> same_axis
> safety_vs_grounding
> safety_vs_coverage
> safety_vs_resolution
> grounding_vs_coverage
> grounding_vs_resolution
> coverage_vs_resolution
> Valid score_gap values are:
> none
> small
> medium
> large
> critical
> Valid review_route values are:
> approve_pair: both rationales appear strong enough that the pair can be accepted without immediate intervention.
> manual_compare: the pair needs normal human comparison.
> reject_lower: one case is clearly much weaker and should be rejected or escalated first.
> audit_rubric: the pair crosses rubric axes in a way that needs rubric-level audit rather than only case-level comparison.
> Submission Example
> A valid submission file starts like this:
> id,arbitration_card
> LJA_TE_0000,priority=case_b;axis_relation=grounding_vs_coverage;score_gap=small;review_route=manual_compare
> LJA_TE_0001,priority=tie;axis_relation=same_axis;score_gap=none;review_route=approve_pair
> Evaluation
> The metric is weighted slot accuracy over hidden test pairs.
> For each test row, the grader parses the four slots in order. It awards partial credit for each exactly correct slot:
> priority: 0.30 points
> axis_relation: 0.25 points
> score_gap: 0.25 points
> review_route: 0.20 points
> The row score is the sum of the weights for slots that exactly match the hidden answer. The final score is the arithmetic mean of row scores across all hidden test rows.
> Formula:
> score = mean(0.30 * I(priority correct) + 0.25 * I(axis_relation correct) + 0.25 * I(score_gap correct) + 0.20 * I(review_route correct))
> A perfect submission scores 1.0. Invalid submissions fail with an error. Missing ids, duplicate ids, unknown ids, extra columns, malformed cards, invalid slot values, or wrong slot order are rejected.
> What Not To Use
> Do not use raw source paths, source hashes, hidden scores, hidden criteria, private answers, row order, external downloads, internet lookup, or source repository search. The public data intentionally contains only score-redacted rationale packets and coarse public cues. Models should learn comparative calibration behavior from the training packets, not recover raw source records.

Inspiration note: Useful because it converts judgment quality, calibration, or arbitration into a measurable evaluator benchmark.

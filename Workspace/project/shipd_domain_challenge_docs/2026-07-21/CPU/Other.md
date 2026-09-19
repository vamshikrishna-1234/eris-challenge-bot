# CPU Other Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed CPU examples in this document: 63

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.

## Neuro-Symbolic Arabic Discourse Topology Deduction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73y1a3hgq3rye02cjzm43ae589v982
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat alba's score of 0.675!

Full challenge description from page:

> Standard Arabic discourse parsing frames relation identification as supervised text classification. This challenge abandons the text-classification paradigm and instead frames discourse structure recovery as Noisy Factor Graph Inference on a Linguistic Chain.
> In simple terms, you are predicting a sequence of Arabic discourse relation labels (chosen from 5 possible classes: CAUSE, CONTRAST, TEMPORAL, JOINT, ELABORATION) for each text instance. However, you are not given the raw Arabic text. Instead, you are given a set of partial, noisy unary and pairwise observations (logical clues), along with strict global histogram constraints (the exact count of each relation type in the sequence). Your task is to decode the most likely sequence of discourse relations that satisfies the global histogram while maximizing the likelihood of the local observations.
> This is not a standard logic-grid puzzle; it is a Statistical Relational Learning and Markov Random Field (MRF) decoding task. Existing pairwise discourse classifiers cannot solve this because they rely on lexical features, whereas this task requires probabilistic inference, belief propagation, and constrained decoding over a factor graph. It is natively CPU-friendly, solvable via lightweight Graph Neural Networks (GNNs), Loopy Belief Propagation, or neuro-symbolic MRF decoders in milliseconds.
> Critically, the local clues are not a reliable oracle: a subset of them are deliberately false, while the global histogram is always exact. This asymmetry — noisy local evidence decoded against a hard global constraint — is closer to robust/noisy-channel decoding (e.g. parity-constrained decoding, robust constraint satisfaction under corrupted observations) than to a plain logic-grid puzzle. A solver that trusts every clue equally will systematically pick infeasible or wrong completions on a meaningful fraction of rows; recovering the sequence requires learning which observations to trust, not just which ones are logically consistent.
> Data Provenance and Generation
> The underlying discourse topologies are derived from 611 rows of curated Arabic prose. The ground-truth relation sequences were deterministically extracted. The unary/pairwise observations and global histogram constraints were then synthetically generated via a deterministic perturbation pipeline to create the factor graph instances.
> Approximately 10% of the generated unary/pairwise clues (exact, not, same_as, diff_from) are deliberately corrupted to assert something false about the true sequence — an exact clue naming the wrong class, a not clue excluding the actually-correct class, or a same_as/diff_from clue asserting the wrong relationship. Which clues are corrupted is not marked anywhere in the data; it must be inferred statistically. The constraints histogram is never corrupted — it always exactly matches ground_truth_sequence. Because of this, a decoder that treats every clue as a hard equality/inequality constraint will find some rows infeasible (the propagated domains can conflict with the exact histogram) or will lock in a wrong answer with full confidence. A well-calibrated solver should treat clue satisfaction as soft evidence, weighted by a learned notion of per-clue reliability, while treating the histogram as the one constraint that is always safe to enforce exactly.
> Dataset
> The prepared data contains a random 70/30 split (approximately 427 training instances and 183 test instances). Sequence lengths (
> 𝑁
> N) vary per row and are capped at 20; in practice most rows fall between 4 and 20 positions. The relation classes are imbalanced (JOINT is the most common class by a wide margin, ELABORATION the rarest) — this reflects the deterministic extraction rule applied to the source prose, not an artifact of the clue/constraint generation.
> Files Provided
> train.csv: Contains the clues, the constraints, and the ground_truth_sequence.
> test.csv: Contains only the clues and constraints.
> sample_submission.csv: A valid example submission file.
> Columns and Features
> Column	Type	Description
> text_id	integer	Unique text identifier.
> clues	string	A JSON list of dictionaries representing unary and pairwise observations. Each dictionary contains a type field (one of exact, not, same_as, or diff_from), positional fields (pos, pos1, or pos2, depending on the observation type), and a value field when applicable. For example: [{"type":"exact","pos":0,"value":"CAUSE"},{"type":"same_as","pos1":1,"pos2":4}]. Roughly 10% of clues are individually false relative to ground_truth_sequence — this is not flagged in the data.
> constraints	string	A JSON object specifying the exact global histogram count of each of the 5 relation classes in the sequence (e.g., {"CAUSE": 2, "CONTRAST": 1, "TEMPORAL": 0, "JOINT": 3, "ELABORATION": 2}). The sum of these counts equals the total sequence length
> 𝑁
> N for that row. Unlike clues, this histogram is always exactly correct.
> ground_truth_sequence	string	(Train only) The complete, correct space-separated sequence of relations.
> Submission Format
> Your submission must be a CSV with exactly these columns in this order: text_id, reconstructed_sequence.
> Strict Constraints
> reconstructed_sequence (string) must be a space-separated string of valid relation labels (CAUSE, CONTRAST, TEMPORAL, JOINT, ELABORATION).
> The length of the predicted sequence must exactly equal
> 𝑁
> N, where
> 𝑁
> N is the sum of all integer values in the constraints dictionary for that row.
> If the sequence length is incorrect, contains out-of-vocabulary labels, or is malformed, the row will score 0.0 for both metric components.
> Example Submission
> text_id,reconstructed_sequence
> 0,CAUSE CONTRAST JOINT ELABORATION CAUSE
> 1,TEMPORAL TEMPORAL CONTRAST
> Evaluation Metric
> The score is a composite metric in [0, 1]; higher is better. It evaluates both the exact logical reconstruction and the model's ability to obey global constraints.
> Exact Topology Match (50% weight): 1.0 if the reconstructed sequence exactly matches the ground-truth sequence, else 0.0.
> Constraint Adherence (50% weight): 1.0 if the predicted sequence's category counts perfectly match the global constraints dictionary provided in the input, else 0.0. Edge case: If the predicted sequence length does not match
> 𝑁
> N (the sum of the constraints), or if the category counts deviate even slightly from the constraints dictionary, this component scores strictly 0.0 for that row.
> Worked Example
> Suppose a row has constraints: {"CAUSE": 2, "CONTRAST": 1, "TEMPORAL": 0, "JOINT": 1, "ELABORATION": 1}. The sum is
> 𝑁
> =
> 5
> N=5.
> If you predict CAUSE CONTRAST JOINT ELABORATION CAUSE, the counts match perfectly. Constraint Adherence = 1.0.
> If you predict CAUSE CAUSE CONTRAST JOINT ELABORATION ELABORATION (length 6), the length is wrong. Constraint Adherence = 0.0.
> If you predict CAUSE CAUSE CONTRAST JOINT TEMPORAL (length 5), the counts are wrong (TEMPORAL is 1 instead of 0, ELABORATION is 0 instead of 1). Constraint Adherence = 0.0.
> The final score is the equally weighted average of these two components:
> score = (0.50 * Exact_Match) + (0.50 * Constraint_Adherence)
> Intended Approach
> The intended skill is probabilistic graphical model inference and MRF decoding from partial, noisy unary/pairwise observations and an exact global histogram constraint. Parse each row's clues into a factor graph, where nodes represent sequence positions and factors represent the unary (exact, not) and pairwise (same_as, diff_from) observations. Train a compact model to predict the local clique potentials or unary/binary emission probabilities for the 5 discourse relations. Suitable CPU models include a Graph Neural Network (GNN) operating over the factor graph to learn message-passing heuristics, a small Transformer pointer network, or a neural initializer for a Loopy Belief Propagation (LBP) or constrained decoder.
> Because roughly 10% of clues are individually false, hard-constraining on every clue (i.e. deleting a class from a position's domain the instant any clue rules it out) is not sufficient — it will make some rows infeasible against the exact histogram and will confidently commit to wrong values on others. train.csv includes ground_truth_sequence specifically so this can be measured directly: fit the empirical reliability of each clue type (and ideally each clue in context, e.g. via agreement/disagreement with other clues on the same row) from the training data, and feed that into the decoder as a soft cost or prior rather than a hard filter. The global histogram, by contrast, is never corrupted and should be enforced exactly.
> Constrained decoding, differentiable SAT solving, or deterministic backtracking search may be used to enforce the strict global histogram constraints, but the underlying probability distributions, clue-reliability estimates, and structural predictions must originate from a model fitted on train.csv. Purely hard-coded, rule-based logic solvers without a learned component are not permitted — and will also score measurably worse than a calibrated approach, since they cannot recover from conflicting or corrupted clues the way a soft-evidence decoder can.
> Validate complete-sequence consistency against the global constraints and clue satisfaction during local validation, preserving edge cases where observations are sparse or conflicting (including cases where hard propagation over the clues alone yields zero feasible completions against the histogram — this is expected on some rows and must be handled by discounting low-confidence clues, not by giving up). Calibrate confidence against the exact topology match rather than only individual clue accuracy. The complete training and inference pipeline must use at most 10 CPU cores and 62 GB RAM, finish within 1.5 hours, and require no GPU. Internet access may be used for package installation and documentation, but not to retrieve external discourse treebanks, source archives, labels, answer maps, or hosted inference.
> What Not To Use
> Any of the following can cause solution rejection even if a leaderboard score is high. Enforcement on invalid approaches: use of any prohibited approach below is grounds for rejection regardless of the reported score.
> Do not download or query external discourse treebanks, Arabic corpora, or linguistic dictionaries to reconstruct the source text or infer hidden labels.
> Do not use exact-name search, source-file matching, public-ID dictionaries, or answer-key reconstruction.
> Do not submit a graph-traversal-only, regex-only, TF-IDF-only, n-gram-only, metadata-only, or fixed-rule system as the primary solution.
> Do not treat every clue as an unconditionally true hard constraint. Roughly 10% of clues are deliberately false, while the histogram in constraints is always exact. A pure constraint-propagation/backtracking solver that hard-enforces all clues is a fixed-rule system under the rule above, will find a meaningful fraction of rows infeasible, and is not a substitute for the required learned clue-reliability component.
> Do not reduce the task to generic knowledge-graph link prediction, standard sequence labeling, tabular classification, or a single next-event label.
> Do not use GPU, CUDA, GPU-only libraries, large pretrained models, hosted model APIs, or closed external inference services.
> Do not exploit row order, filenames, local aliases, hashes, file sizes, malformed JSON, grader exceptions, private files, or filesystem side channels.

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## Field Call Propagation Correspondence

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dcaj23aabryg39gfbgav0kh8armvc
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Beat shivam_s's score of 0.743!

Full challenge description from page:

> Each case contains one reference bird call and five candidate recordings. Identify which candidates are re-recordings of the same original call, rank only those matches from the cleanest to the most propagation-degraded observation, describe whether each match stayed in the same habitat, and identify every type of decoy present.
> This is a correspondence problem rather than species classification. Several candidates may contain the same species, and a candidate from another call can sound more similar in quality than a distant re-recording of the correct call. The solver must preserve vocal identity across distance, reverberation, resampling, and background interference.
> The scenario reflects low-power ecological monitoring. A field station may receive multiple detections that originated from one vocal event but traveled through different habitats. Correctly consolidating those detections prevents duplicate biological counts and separates true propagation evidence from unrelated birds and environmental noise.
> Dataset
> The prepared dataset contains 1,320 labeled training cases and 407 test cases. The public training and hidden test partitions originate from different recorded individuals. Before packet construction, byte-identical source recordings are globally deduplicated, including repeated negatives that occur under different filenames. Each public media filename and case ID is opaque. Public audio is standardized to mono 16 kHz PCM and receives a deterministic sub-1.5-percent time-scale shift, mild gain change, and low-level dither to prevent exact source-file matching.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Public inputs and four target fields for training cases. |
> | `test.csv` | Public inputs only for test cases. |
> | `sample_submission.csv` | Required submission schema and valid example values. |
> | `audio/*.wav` | Opaque reference and candidate recordings used by the CSV files. |
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque unique case identifier. |
> | `reference_audio_path` | path string | WAV recording used as the correspondence anchor. |
> | `candidate_audio_paths` | JSON array string | Five WAV paths in candidate order `c1` through `c5`. |
> | `correspondence_contract` | string | Packet-level instruction defining matching, range ordering, habitat relation, and decoy reporting. |
> Target Columns
> | Column | Data type | Description |
> |---|---|---|
> | `same_call_mask` | JSON integer vector | Five binary entries. Entry `i` is 1 when candidate `c{i+1}` is a re-recording of the reference call. |
> | `range_rank_program` | ordered token string | Matching candidate IDs ordered from least to most propagation loss, followed by `seal:range`. |
> | `habitat_relation_graph` | canonical edge set string | One edge per matched candidate: `r-cN:same_habitat` or `r-cN:cross_habitat`, joined by `|`. |
> | `decoy_type_set` | canonical set string | Present decoy categories joined by `|`: `background`, `other_call`, and `other_species`. |
> Every case has one, two, or three correct candidates. Training counts are 440, 446, and 434. Test counts are 126, 141, and 140.
> Submission Format
> Write the final CSV to:
> ./working/submission.csv
> Columns must appear exactly in this order:
> case_id,same_call_mask,range_rank_program,habitat_relation_graph,decoy_type_set
> Example:
> case_id,same_call_mask,range_rank_program,habitat_relation_graph,decoy_type_set
> 59c2f096acd54b2e1f85553d,"[0,1,0,1,0]",c2>c4>seal:range,r-c2:same_habitat|r-c4:cross_habitat,background|other_call|other_species
> Extra columns, reordered columns, duplicate IDs, missing IDs, and additional rows are rejected. Only a backend-added visibility column is ignored.
> Evaluation
> The metric is Propagation Correspondence Integrity Score:
> Score = 0.40 * MaskScore
> + 0.28 * RangeProgramScore
> + 0.17 * HabitatGraphScore
> + 0.15 * DecoySetScore
> For the five-entry mask:
> MaskScore = 0.12 * entry_accuracy + 0.88 * exact_mask_match
> For the range program, Levenshtein distance is computed over >-separated tokens:
> edit_similarity = 1 - edit_distance(true_tokens, predicted_tokens)
> / max(number_of_true_tokens, number_of_predicted_tokens, 1)
> RangeProgramScore = 0.18 * edit_similarity + 0.82 * exact_program_match
> Graph and decoy fields use standard set F1, followed by strict exact-set credit:
> HabitatGraphScore = 0.25 * set_F1 + 0.75 * exact_set_match
> DecoySetScore     = 0.30 * set_F1 + 0.70 * exact_set_match
> The mask, range program, and habitat graph must name exactly the same matched candidates. An inconsistent case receives a 10 percent coherence penalty. Malformed or overlong fields score zero for their component.
> Minimum score: 0.0
> Maximum score: 1.0
> Direction: higher is better.
> What Makes This Interesting
> The positive examples are linked by acoustic identity, not merely by species or recording quality. A solver must distinguish propagation damage from a genuinely different vocal event, then infer an ordered physical degradation path and habitat transfer. The output is a compact correspondence structure that can be checked exactly without free-text semantic grading.
> Method Requirements
> CPU-compatible audio encoders, spectrogram models, metric-learning systems, compact sequence models, and classical signal preprocessing used with a learned model are allowed. Training and calibration must use only the supplied public data.
> What Not To Use
> Do not recover source song IDs, habitats, distances, or labels through original filenames, external mirrors, audio hashes, or source-catalog lookup.
> Do not map opaque file paths, case_id, row order, or repeated storage artifacts directly to targets.
> Do not use hidden test data for parameter updates, threshold selection, or pseudo-label calibration.
> Do not exploit duplicate submissions, missing rows, extra columns, malformed JSON, or non-finite values.
> Do not call hosted closed-model APIs during inference.

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## Vulnerability Applicability Logic Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fpz9vhgvrwz3bq6djjdxfns8aqq4d
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Beat abhi404's score of 0.535!

Full challenge description from page:

> Vulnerability scanners must evaluate more than a flat list of affected products. A vulnerability can apply to several alternative configurations, and one configuration may require an application together with a particular operating system or hardware platform. Losing those Boolean boundaries during feed conversion can produce false positives or missed exposure.
> Each row contains one leakage-controlled vulnerability description, 4 to 16 shuffled CPE applicability atoms, and an intact configuration-count manifest field. Reconstruct the native NVD applicability tree: allocate every atom to its original node, allocate nodes to the declared number of configurations, and recover each configuration's AND or OR operator.
> The hidden target is the official NVD configuration structure. It is not a generated vulnerability label or a synthetic graph.
> Task
> For every case_id, submit an applicability_json object of this form:
> {
> "configurations": [
> {"operator": "AND", "nodes": [["ATOM_0"], ["ATOM_3"]]},
> {"operator": "OR", "nodes": [["ATOM_1", "ATOM_2"]]}
> ]
> }
> Configuration order, node order, and atom order inside a node are not scored. The grouping and operators are scored. Every displayed atom must appear exactly once.
> Dataset
> public/train.csv contains vulnerabilities published through 2024 and their native applicability trees.
> public/test.csv contains vulnerabilities published from 2025 onward without targets.
> public/sample_submission.csv demonstrates a valid, row-specific reconstruction.
> private/answers.csv contains hidden native trees for grading only and is not available to solvers.
> Columns
> case_id string): opaque row identifier unrelated to the CVE identifier.
> description_packet string): transformed English vulnerability description.
> atom_packet string): shuffled ATOM_# records with product-part class, row-local vendor/product aliases, vulnerable flag, coarse version-boundary profile, and target-platform aliases.
> atom_count integer): number of atoms in the row, from 4 through 16.
> configuration_count_hint integer): native number of top-level applicability configurations. The count survives the simulated feed-conversion failure, but membership, node boundaries, and operators are hidden.
> applicability_json JSON string, train only): native configuration, node, and operator structure over the row's atom IDs.
> Vendor, product, and target-platform terms use row-local aliases. Rare description terms are also row-local, while common security language remains readable. Exact CVE identifiers, URLs, source identifiers, and version values are not released. Repeated aliases preserve useful within-row relationships without enabling source-record lookup.
> Every retained source row contains all three pair relationships used by the metric: same node, different nodes in the same configuration, and different configurations.
> Evaluation
> Scores range from 0 through 1, and higher is better.
> For every unordered atom pair, the grader derives one of three relations:
> SAME_NODE
> SAME_CONFIGURATION_DIFFERENT_NODE
> DIFFERENT_CONFIGURATION
> PairRelationMacroF1 is macro F1 across those three relations.
> MatchedConfigurationOperatorAccuracy is the fraction of true configurations whose exact atom set appears in the prediction with the correct AND or OR operator.
> ExactTreeAccuracy is 1 only when all configuration memberships, node memberships, and operators match after ignoring list order.
> Score = 0.65 * mean(PairRelationMacroF1)
> + 0.20 * mean(MatchedConfigurationOperatorAccuracy)
> + 0.15 * mean(ExactTreeAccuracy)
> The native tree scores 1. Scores are clipped to the range 0 through 1.
> Submission Format
> Submit a UTF-8 CSV with exactly these columns:
> case_id,applicability_json
> NAT_0123456789abcdef,"{""configurations"":[{""operator"":""AND"",""nodes"":[[""ATOM_0""],[""ATOM_1""]]},{""operator"":""OR"",""nodes"":[[""ATOM_2"",""ATOM_3""]]}]}"
> Requirements:
> Include every test case_id exactly once, with no missing, duplicate, or unknown IDs.
> Use exactly the top-level key configurations.
> Every configuration must contain exactly operator and nodes.
> Operators must be AND or OR.
> Every node must be a non-empty list of valid atom IDs.
> Use every atom from that row exactly once, without adding atoms.
> Write the CSV to the exact output path supplied by the platform.
> Allowed
> CPU-only graph clustering, pair-relation models, structured prediction, compact neural models trained from scratch, and ensembles using only the public files.
> Joint use of the transformed description and every atom view.
> At most 10 CPU cores, 62 GB RAM, and 1.5 hours end-to-end.
> Prohibited
> No GPU or accelerator computation.
> No external NVD/CVE/CPE feed, vulnerability database, source-record lookup, web search, cached configuration tree, hosted inference API, or closed external model service.
> Do not reconstruct CVE IDs, source vendors, product names, exact versions, CPE strings, or original records.
> Do not use private answers, grader internals, test IDs, row order, filenames, hashes, or manually coded test trees.
> This benchmark evaluates structural recovery only and must not be used as a substitute for current official vulnerability-management data.

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## Recovering Interleaved Source Streams from a Merged Token Sequence

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73pcgrdc72ezyrwt05xq57498akgw7
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Beat akashmaggon's score of 0.238!

Full challenge description from page:

> Each instance is built from num_streams (K, between 2 and 4) real source
> streams. A source stream is a short passage of real text drawn from a
> distinct topical domain, reduced to a sequence of word tokens and then mapped
> through a single hidden vocabulary permutation to opaque integer ids. The
> same word always maps to the same id, so streams about the same subject share
> "vocabulary", but no id can be decoded back to a word.
> The K streams are merged into one observed sequence by a hidden schedule that
> walks along the streams, mostly taking a few tokens from one before switching
> to another, until all are exhausted. **The merge preserves each stream's
> internal order**, so once you know which positions belong to a stream, you
> have recovered that stream in order. Recovering the partition of positions is
> therefore the whole task.
> Concretely, for an observed sequence tokens of length seq_len, you output
> an assignment: one integer stream label per position, using labels
> 0..K-1. The specific integers you choose do not matter -- only the grouping
> does (see Evaluation). For example, an observed sequence
> tokens:      41  902  17  41  655  902  17  655
> true streams: 0    1   0   0    1    1   0    1
> interleaves stream A = positions [0,2,3,6] (tokens 41 17 41 17) with
> stream B = positions [1,4,5,7] (tokens 902 655 902 655).
> What makes this hard:
> No surface features. Token ids are meaningless; two ids are only
> related through the co-occurrence structure you learn from train.csv.
> No position shortcut. All K streams within an instance have the same
> length, and the schedule keeps them well interleaved, so guessing by
> location (for example, splitting the sequence into K contiguous blocks)
> scores near zero.
> Streams must be told apart by content alone. Because the K streams come
> from different topical domains, their token vocabularies differ -- but that
> difference is only visible after you have learned, from training data,
> which opaque ids belong together.
> Evaluation
> Submissions are scored with the Adjusted Rand Index (ARI) between your
> predicted partition and the true partition of positions, averaged over all
> test instances and clamped to [0, 1]. ARI compares two partitions by how
> often they agree on whether each pair of positions belongs to the same
> stream, corrected for chance agreement. It is:
> permutation-invariant -- relabeling your streams (calling stream 0
> "stream 1" and vice versa) does not change the score;
> chance-corrected -- a random assignment, an all-one-stream assignment,
> an all-singletons assignment, and a positional block guess all score ~0;
> bounded -- ARI is at most 1, and negative values are clamped to 0, so
> every instance scores in [0, 1].
> For one instance with n positions, let the contingency table cont[i][j]
> count positions whose true stream is i and predicted stream is j, with
> row sums a[i] and column sums b[j]:
> def comb2(x):
> return x * (x - 1) / 2.0
> def ari(true_labels, pred_labels):
> n = len(true_labels)
> if n == 0:
> return 0.0
> # cont[i][j] = number of positions with true stream i and predicted stream j
> cont = contingency_table(true_labels, pred_labels)   # shape (T, P)
> a = cont.sum(axis=1)      # true-stream sizes
> b = cont.sum(axis=0)      # predicted-stream sizes
> sum_comb_c = sum(comb2(v) for v in cont.flatten())
> sum_comb_a = sum(comb2(v) for v in a)
> sum_comb_b = sum(comb2(v) for v in b)
> total_comb = comb2(n)
> expected = sum_comb_a * sum_comb_b / total_comb
> max_index = 0.5 * (sum_comb_a + sum_comb_b)
> denom = max_index - expected
> if denom <= 0:                       # degenerate (both a single cluster)
> return 1.0 if true_labels == pred_labels else 0.0
> score = (sum_comb_c - expected) / denom
> return min(1.0, max(0.0, score))     # clamp to [0, 1]
> The final score is the mean of ari over all test instances. Because this is
> a genuinely hard separation of opaque tokens, even a strong learned solution
> scores well below 1 while trivial baselines sit near 0 -- higher is better.
> Submission validity. Your submission must contain exactly the test ids,
> each exactly once: any missing id, extra id, or duplicate id fails the whole
> submission (it scores 0). An assignment that is unparsable or whose length
> does not match the instance's seq_len scores 0 on that instance only.
> Dataset
> The public data contains 6,000 labeled training instances and **1,800
> test instances**. The source streams behind the training instances and those
> behind the test instances are disjoint, so no training passage appears in a
> test instance.
> Files:
> train.csv: labeled instances, with the true assignment.
> test.csv: instances without assignment.
> sample_submission.csv: a valid baseline submission (a round-robin guess).
> Columns:
> | Column | Type | Description |
> |---|---|---|
> | id | string | Unique instance id. Train ids are tr_NNNNNN, test ids are te_NNNNNN. |
> | num_streams | int, 2 to 4 | K, the number of source streams interleaved in this instance. |
> | seq_len | int | Length of the observed token sequence (the number of positions to label). |
> | tokens | string | The observed merged sequence: seq_len opaque integer token ids, space-separated, in observed order. |
> | assignment | string, train only | Label. seq_len integers in 0..K-1, space-separated, one per position, giving the true source stream of each token. |
> Token format. Every token is a positive integer id in the range
> 1..3000. Ids are opaque: they are a fixed hidden permutation of a real word
> vocabulary, so an id's numeric value carries no meaning and no ordering. The
> same underlying word always has the same id across every instance.
> Submission Format
> Submit a CSV with exactly id and assignment:
> id,assignment
> te_000001,0 1 0 0 1 1 0 1
> te_000002,2 0 1 2 0 1 1 2 0 0
> te_000003,0 1 1 0 1 0 0 1
> Requirements:
> Exactly 1,800 rows (one per test id), plus a header row. This is enforced:
> a submission missing any test id, carrying an extra id, or duplicating an
> id scores 0 outright.
> Every id from test.csv must appear exactly once.
> assignment is a space-separated list of integers, one per position, with
> length equal to that instance's seq_len. Use labels 0..K-1; the exact
> integers are arbitrary (only the grouping is scored).
> An unparsable or wrong-length assignment scores 0 on that instance rather
> than causing an error.
> What Not To Use
> Any attempt to reverse the token anonymization or map ids back to words
> (for example, matching id-frequency profiles against an external text
> corpus). The vocabulary permutation is hidden and the mapping is not part
> of the task; a valid solution learns token co-occurrence structure from the
> released training instances only.
> Hardcoded mappings from ids to answers, or any external answer key. The
> true interleaving of each instance is generated fresh and exists in no
> outside source, so there is nothing to look up.
> GPU usage is not required and not necessary; this is a CPU-only task.
> Expected Output
> Output to ./working/submission.csv.

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## Macromolecular Assembly Graph Gap Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx753t0vdcke3xms6cfwkbkwr18apepn
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Beat benben181's score of 0.600!

Full challenge description from page:

> Predict the three missing molecules and their stoichiometries in a partial biological assembly graph.
> A macromolecular assembly is a group of molecules, such as proteins, RNAs, small molecules, ions, or cofactors, that work together as one biological unit. Stoichiometry is the number of copies of a molecule in that unit.
> Each row gives a partial assembly card. The visible participants are listed with coarse molecule types, readable biological term hints, and known stoichiometry. Three participants have been removed. A row-local candidate list gives possible missing molecules using local molecule IDs and term hints. Your task is to output the three missing molecule_id values from that row's candidate list and the integer stoichiometry for each molecule.
> The released fields use local molecule IDs and term cards rather than external database identifiers or long exact record text. The task is therefore to model consistency between the assembly context, visible participants, candidate molecule terms, and copy counts, not to look up records externally.
> This is a structured graph-gap recovery task. It is not classification, regression, recommendation, or tabular prediction.
> Dataset
> Files:
> public/train.csv: 500 solved examples. It contains all input fields plus answer_json.
> public/test.csv: 300 unsolved examples. It contains the same input fields except answer_json.
> public/sample_submission.csv: required submission shape with placeholder values.
> Columns:
> id (string): unique released row id.
> prompt (string): task instruction for the row.
> organism_group (string): opaque organism grouping token.
> context_terms_json (JSON list of strings): biological terms extracted from the assembly context after removing direct identifiers and long exact text.
> function_terms_json (JSON list of strings): functional and location terms associated with the assembly.
> evidence_terms_json (JSON list of strings): evidence and property terms that describe how the assembly is supported or characterized.
> assembly_terms_json (JSON list of strings): coarse terms describing the assembly form, such as dimer-like or multimer-like wording when present.
> observed_participants_json (JSON list of objects): visible molecules in the partial graph. Each object has molecule_type (string, one of protein, small_molecule, rna, or other_molecule), participant_terms (JSON list of strings), and stoichiometry (integer).
> candidate_participants_json (JSON list of objects): possible missing molecules for this row. Each object has molecule_id, molecule_type, and name_terms. Every submitted molecule_id must come from this list.
> candidate_count (integer): number of candidate molecules in the row-local list.
> answer_json (JSON object, training rows only): ground-truth object with missing_participants, a JSON list containing exactly three objects. Each object has molecule_id (string) and stoichiometry (integer).
> Submission Format
> Submit a CSV with exactly these columns:
> id,prediction_json
> assembly_1234abcd5678ef,"{""missing_participants"":[{""molecule_id"":""mol_03"",""stoichiometry"":1},{""molecule_id"":""mol_08"",""stoichiometry"":1},{""molecule_id"":""mol_11"",""stoichiometry"":2}]}"
> assembly_98ab76cd54ef32,"{""missing_participants"":[{""molecule_id"":""mol_02"",""stoichiometry"":1},{""molecule_id"":""mol_07"",""stoichiometry"":2},{""molecule_id"":""mol_10"",""stoichiometry"":1}]}"
> prediction_json must be a JSON object with:
> missing_participants: a list of exactly three objects.
> Each object must contain molecule_id, the row-local candidate molecule ID for an absent molecule.
> Each object must contain stoichiometry, the integer stoichiometry for that molecule.
> Malformed JSON in a row receives zero for that row. Submissions with the wrong row count, duplicate ids, missing ids, extra ids, or extra/missing columns are rejected.
> Evaluation
> The score is mean exact recovery over test rows.
> For row i:
> row_score_i = 1 if the submitted three-object set exactly matches the hidden answer:
> all three hidden molecule_id values are present
> all three integer stoichiometries match the corresponding molecules
> Otherwise, row_score_i = 0.
> The final score is:
> score = (row_score_1 + row_score_2 + ... + row_score_N) / N
> where N is the number of test rows. Malformed JSON in one row receives row_score_i = 0 for that row. A perfect submission scores 1.0.
> CPU/GPU Policy
> GPU usage is not allowed. Solutions should run on CPU using local public files only.
> What Not To Use
> Do not use GPUs, external datasets, internet lookup, external downloads, hidden or non-released organizer files, hosted inference APIs, runtime package installation, remote-code loaders, or challenge-specific precomputed lookup tables. The intended work is CPU-only reasoning, parsing, and graph-consistency modeling from public/train.csv and public/test.csv.

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## Acoustic-Optical Telemetry Collision Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7085nma9k70wqmb3nwn321dh8aq0hg
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Acoustic-Optical Telemetry Collision Recovery
> Overview
> This competition asks you to recover the hidden provenance of a synthetic telemetry collision from paired acoustic and optical sensor features. Each episode defines four anonymous, episode-local source tokens. You receive three paired support packets for every token and one observed collision packet. Two or three tokens contributed to that collision with weights that change over ten temporal blocks.
> Both modalities share the same active tokens and weight trajectory, but they are observed through different continuous sensor operators. Some episodes additionally contain a localized nonlinear distortion, missing blocks, or a source that interferes with only one modality. Your model must jointly recover the active token set, the complete weight trajectory, its change points, and the locally corrupted blocks.
> The collision is a feature-level electronic telemetry simulation constructed from real synchronized laser powder bed fusion (LPBF) measurements. Its weights are not physical intermediate-alloy compositions and must not be interpreted as such. Original composition classification is not the task.
> Conventional tasks on these measurements predict a global source or composition label from one recording. Here, source labels are permuted within every episode, and the required output jointly covers the active set, a blockwise simplex trajectory, change points, and modality-specific corruption under chronological holdout. The learning problem is therefore episode-local multimodal inference rather than ordinary composition classification.
> Task
> For every row of test.csv, submit one strict JSON object with four fields:
> active_sources: the anonymous tokens that contributed to the shared collision;
> weights: one four-source simplex vector for each of ten blocks;
> change_points: block boundaries at which the underlying trajectory changes segment;
> corruption_mask: the acoustic and optical blocks affected by a localized severe disturbance.
> The four tokens are always named source_0, source_1, source_2, and source_3, but their underlying source regime is permuted independently in each episode. Token meaning must therefore be inferred from that episode's support packets.
> Prepared Files
> train.csv
> There are 800 training episodes. Columns are:
> Column	Type	Meaning
> id	string	Opaque unique episode identifier of the form ctc_ followed by 24 lowercase hexadecimal characters. It contains no target, source-row, or nuisance-family information.
> episode	JSON string	Public input object described below.
> target	JSON string	Gold structured target described below.
> test.csv
> There are 500 test episodes. Columns are:
> Column	Type	Meaning
> id	string	Opaque unique episode identifier.
> episode	JSON string	Public input object with the same schema as the training input.
> sample_submission.csv
> There are 500 rows and exactly two columns:
> Column	Type	Meaning
> id	string	Test identifier copied without modification.
> prediction	JSON string	One prediction object using the required output grammar.
> The sample is a valid no-skill prediction and receives score 0 by construction.
> Episode JSON Schema
> Each episode cell decodes to an object with exactly three fields:
> {
> "tokens": ["source_0", "source_1", "source_2", "source_3"],
> "support": [[[[[0.0]]]]],
> "observed": [[[0.0]]]
> }
> The shortened numeric arrays above show nesting only. Their exact shapes are:
> Field	Type and shape	Meaning
> tokens	list of 4 strings	Token order used by the last axis of every weight vector.
> support	float array [4, 3, 2, 10, 12]	Three examples for each token. Axes are token, support example, modality, temporal block, feature.
> observed	float array [2, 10, 12]	Collision to decode. Axes are modality, temporal block, feature.
> Modality index 0 is acoustic and modality index 1 is optical. Block indices are 0 through 9 in temporal order.
> The 12 features in the last axis, in order, are:
> root mean square amplitude;
> standard deviation;
> mean absolute amplitude;
> median absolute amplitude;
> 90th percentile of absolute amplitude;
> peak absolute amplitude;
> zero-crossing rate;
> normalized spectral centroid;
> first quarter-band power ratio;
> second quarter-band power ratio;
> third quarter-band power ratio;
> fourth quarter-band power ratio.
> Features are extracted from ten non-overlapping 500-sample waveform blocks. A robust scale is fitted only on training source bands, followed by log1p compression and L2 normalization of each 12-feature block. Published values are rounded to six decimal places.
> Target and Prediction JSON Schema
> Every target and prediction object has exactly these keys:
> {
> "active_sources": ["source_0", "source_2"],
> "weights": [
> [0.62, 0.0, 0.38, 0.0],
> [0.60, 0.0, 0.40, 0.0],
> [0.59, 0.0, 0.41, 0.0],
> [0.20, 0.0, 0.80, 0.0],
> [0.19, 0.0, 0.81, 0.0],
> [0.18, 0.0, 0.82, 0.0],
> [0.17, 0.0, 0.83, 0.0],
> [0.16, 0.0, 0.84, 0.0],
> [0.15, 0.0, 0.85, 0.0],
> [0.14, 0.0, 0.86, 0.0]
> ],
> "change_points": [3],
> "corruption_mask": [
> [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
> [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
> ]
> }
> Field rules are:
> Field	Required type and constraints	Meaning
> active_sources	JSON list containing 1 to 4 distinct valid token strings	Predicted unordered active-source set. Gold rows contain 2 or 3 tokens.
> weights	float array [10, 4]; every value finite and in [0, 1]; every row sums to 1 within 1e-6	Predicted source proportions for blocks 0 through 9. Columns follow tokens order.
> change_points	JSON list of at most 9 distinct integers in strictly increasing order; every value is from 1 through 9	Boundary b lies between blocks b-1 and b. Gold rows contain one or two boundaries drawn from 2 through 8; when there are two, their indices differ by at least 2.
> corruption_mask	integer array [2, 10] containing only 0 or 1	A 1 marks a locally severe corruption in that modality and block. Row 0 is acoustic and row 1 is optical.
> The globally applied mild continuous sensor operator is not marked in corruption_mask. The mask covers only additional localized operator shifts, dropped blocks, and modality-private interference. The four target fields are scored independently; a predicted active set does not impose zeros on the submitted trajectory.
> Episode Construction and Split Boundary
> Each source token has three public support packets. Hidden source packets are derived from held-out raw windows and are not exact copies of public support rows. Two or three hidden packets are combined along a shared, piecewise-smooth simplex trajectory with one or two separated change points.
> Acoustic and optical streams are transformed independently. Hidden nuisance strata vary the presence, location, modality, and severity of additional corruption, including missing blocks and modality-private interference.
> Train and test episodes use disjoint chronological source bands. Within each split, public support rows and rows used for hidden roles are disjoint. No raw row, derived episode, or opaque ID is shared between train and test. The source does not provide independent build IDs, so this is explicitly a source-order holdout rather than a claimed build-disjoint evaluation.
> Evaluation
> The metric contains four components and is macro-averaged across five equally sized hidden nuisance strata. Let F be the set of strata and let I_f be the test rows in stratum f.
> 1. Active-source F1
> For one row, let TP be the number of correctly predicted active tokens, FP the number of predicted tokens not active in gold, and FN the number of missed gold tokens.
> ActiveF1_i = 2 TP / (2 TP + FP + FN)
> If both sets are empty, F1 is defined as 1. Gold sets are never empty.
> 2. Trajectory similarity
> For block b, gold simplex w_b, and predicted simplex p_b:
> TV_b = 0.5 * sum over k of abs(p_bk - w_bk)
> Trajectory_i = mean over b=0..9 of clip(1 - TV_b, 0, 1)
> Because both rows are valid simplex vectors, TV_b lies in [0, 1].
> 3. Change-point F1
> Predicted and gold boundaries are sorted and matched one-to-one. A pair is eligible when their integer boundary indices differ by at most 1. Matching uses maximum cardinality; no boundary can be used twice.
> ChangeF1_i = 2 matched / (number_predicted + number_gold)
> If both lists are empty, the value is 1. Gold lists are never empty.
> 4. Corruption-mask F1
> For each modality, block indices with value 1 form a set. Ordinary set F1 is computed separately for acoustic and optical and the two values are averaged:
> ModalityMaskF1_i = 2 TP / (2 TP + FP + FN)
> MaskF1_i = 0.5 * (AcousticMaskF1_i + OpticalMaskF1_i)
> For each modality, TP, FP, and FN are computed from that modality's predicted and gold block sets. When both gold and predicted sets for one modality are empty, that modality's F1 is 1.
> Hidden-stratum macro average
> For each component c:
> R_f,c = mean of component c over rows in I_f
> R_c   = (1 / 5) * sum over f in F of R_f,c
> This prevents performance on the mildest episodes from dominating the score.
> No-skill normalization
> The exact constant prediction in sample_submission.csv defines a fixed no-skill reference. The grader evaluates that same constant against the hidden answers to obtain B_c for every component. Each submitted component is converted to skill above that reference:
> S_c = clip((R_c - B_c) / (1 - B_c), 0, 1)
> For every component, the fixed reference satisfies 0 <= B_c < 1.
> Therefore the supplied sample scores exactly 0 and a perfect prediction scores exactly 1. Performance at or below the reference for one component contributes zero for that component.
> Final score
> score =
> 0.25 * S_active
> + 0.45 * S_trajectory
> + 0.15 * S_change
> + 0.15 * S_mask
> Higher is better. The theoretical score range is [0, 1].
> Submission Validation
> The CSV columns must be exactly id,prediction in that order. IDs must be non-null strings, unique, syntactically valid, and exactly equal to the hidden test ID set. Extra, missing, duplicate, or unknown IDs and extra columns invalidate the whole submission.
> Each prediction must be strict JSON with exactly the four documented keys. Duplicate JSON keys, non-finite constants, unknown tokens, duplicate active tokens, unsorted or repeated change points, invalid mask values, invalid shapes, values outside their ranges, or a weight row that does not sum to one make that row malformed. A malformed row receives zero for all four raw components; it does not invalidate otherwise well-formed rows. Prediction cells larger than 16,384 UTF-8 bytes are malformed.
> Runtime
> Solutions run without network access on 10 CPU cores and 62 GB RAM, with a maximum runtime of 90 minutes. Use only the supplied challenge data and libraries already installed in the Kaggle-compatible environment. External data, pretrained weights, downloaded artifacts, package installation, hosted APIs, and attempts to recover hidden answers from IDs or row order are prohibited. The task is designed for from-scratch signal processing and multimodal sequence modeling.

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## Anonymous Bat Conversation Graph Recovery From Reference Calls

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76y3yrpvwhhja9tjct3kak3h8appab
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Plain language objective: match anonymous bat callers from reference calls, recover source-documented addressees and interaction contexts, and submit the directed social graph implied by each episode.
> You are given short real Egyptian fruit bat vocalization clips arranged into anonymous social episodes. Each episode contains two to four anonymous bats such as Bat_A, Bat_B, and Bat_C. For every anonymous bat, the episode provides reference WAV clips where that bat is known to be the caller. The gallery then contains additional shuffled WAV clips from the same anonymous episode.
> Your task is to recover the social call ledger: who called, who the call was directed to when the source supports it, what native interaction context was documented, and what directed caller-to-addressee graph is implied by the gallery. This is not bat-language translation and not ordinary global speaker classification. The anonymous node mapping resets in every episode, so the reference clips are part of the input evidence.
> CPU only: solutions must finish within 1.5 hours on 10 CPU cores and 62 GB RAM. Suitable approaches include high-sample-rate log-spectral features, compact Siamese or metric-learning models, 1D CNN/TCN encoders trained from scratch on CPU, nearest-reference scoring, calibrated unknown handling, and a lightweight graph head. Do not require GPUs, hosted APIs, external datasets, runtime downloads, or internet access.
> For every test episode, submit:
> call_predictions_json: one prediction object per gallery call.
> graph_json: directed edge counts and context summaries implied by the episode.
> confidence: row-level confidence in [0,1].
> What Not To Use / What Not To Do:
> Do not use source filenames, source file IDs, original bat IDs, treatment IDs, recording dates, recording channels, archive member order, file sizes, exact timestamps, or source-row lookup.
> Do not download, index, or search the upstream bat corpus or annotations to identify hidden test rows.
> Do not reduce the task to fixed global bat identity classification, context-only classification, metadata-only classification, or a decorative graph copied from per-call predictions without checking consistency.
> Do not invent hunting, translation, semantic-intent, or conversation labels outside the supplied native context taxonomy.
> Do not use hosted models, remote audio APIs, proprietary systems, GPU-only dependencies, external labels, runtime downloads, private files, grader internals, hardcoded IDs, or malformed-submission exploits.
> Enforcement on invalid approaches: submissions may be rejected before payout if they rely on source lookup, metadata reconstruction, private files, fixed templates, or methods that ignore the episode references and social graph-recovery task.
> Task
> For each test episode, group the provided gallery calls by episode_id, read the episode's reference_json, and predict a complete row-local social record. The caller field should be one of the anonymous episode nodes, inferred from the reference calls rather than from any global bat name. The addressee field should be one of the same nodes when source evidence supports a directed addressee, or UNKNOWN when the documented source target is unknown or not resolvable. The context field must use the supplied native context vocabulary.
> The graph is operational, not decorative: graph_json should summarize the directed caller-to-addressee counts and context counts implied by your per-call predictions. A strong answer keeps the per-call ledger and the graph internally consistent.
> Intended Approach
> A practical CPU solution can extract high-frequency log-mel or constant-Q style acoustic features from each WAV, learn a compact caller embedding from training episodes, and compare gallery calls to the row-local reference clips with a metric-learning or Siamese-style scorer. Addressee and context heads can use the same acoustic representation plus episode-level priors learned only from the training labels. The graph head can then be constructed from calibrated per-call predictions and checked for consistency.
> Reasonable CPU methods include nearest-reference matching with spectral features, gradient-boosted models over bat-call descriptors, compact 1D CNN/TCN encoders trained from scratch on CPU, and lightweight postprocessing for confidence calibration and graph consistency. Use train-only validation folds by episode and real audio/context families to tune thresholds for UNKNOWN, confidence, and graph counts. Do not validate on hidden test answers or external copies of the source corpus.
> Dataset
> Prepared files:
> Item	Description
> train.csv	Labeled gallery calls
> test.csv	Test gallery calls
> train_graphs.csv	Train graph labels
> taxonomy.json	Public vocabulary
> train/audio/	Train WAV clips
> test/audio/	Test WAV clips
> sample_submission.csv	Weak valid template
> The prepared split contains 36 training episodes and 18 test episodes. The test set is arranged to test generalization across bats, recording conditions, and interaction contexts, while each test episode supplies its own reference calls. Public IDs, audio paths, and row order are opaque. Original filenames, source bat IDs, treatment IDs, recording dates, recording channels, and source sample ranges are not public.
> All public audio is mono 16-bit WAV at 100,000 Hz. Clips are source-redacted, label-preserving excerpts derived from 250,000 Hz official WAVs and lightly processed to preserve bat-call structure while reducing direct source fingerprinting.
> train.csv columns:
> Column	Type	Description
> episode_id	string	Opaque episode ID
> call_id	string	Opaque gallery call ID
> audio_path	path	Gallery WAV path
> gallery_position	int	Shuffled position
> node_set_json	JSON	Episode node labels
> reference_json	JSON	Reference clips
> clip_duration_sec	float	Public clip duration
> sample_rate_hz	int	Always 100000
> caller	string	Train caller label
> addressee	string	Train addressee label
> context	string	Train native context
> test.csv columns:
> Column	Type	Description
> episode_id	string	Opaque episode ID
> call_id	string	Opaque gallery call ID
> audio_path	path	Gallery WAV path
> gallery_position	int	Shuffled position
> node_set_json	JSON	Episode node labels
> reference_json	JSON	Reference clips
> clip_duration_sec	float	Public clip duration
> sample_rate_hz	int	Always 100000
> reference_json is a JSON list. Each item has reference_id, bat, audio_path, and duration_sec. The bat field is an anonymous node label valid only inside that episode.
> Allowed context labels are listed in taxonomy.json: UNKNOWN_CONTEXT, SEPARATION, BITING, FEEDING, FIGHTING, GROOMING, ISOLATION, KISSING, LANDING, MATING_PROTEST, THREAT_LIKE, GENERAL, and SLEEPING.
> Submission
> Write ./working/submission.csv with exactly these columns in this order:
> The submission CSV must contain exactly one row per test episode (18 rows total).
> Column	Type	Constraint
> episode_id	string	Exact test episode
> call_predictions_json	JSON	One object per call
> graph_json	JSON	Directed graph object
> confidence	float	In [0,1]
> call_predictions_json must be a JSON list with exactly one object for every gallery call_id in that episode. Each object must have exactly:
> call_id: a test gallery call ID.
> caller: one of the episode nodes.
> addressee: one of the episode nodes, or UNKNOWN.
> context: one allowed context label.
> confidence: a number in [0,1].
> graph_json must be a JSON object with exactly edges. Each edge has source, target, count, and contexts. source and target are distinct episode nodes. count is the number of predicted directed calls. contexts maps context labels to counts for that directed edge.
> Example:
> episode_id,call_predictions_json,graph_json,confidence
> bat_ep_example,"[{""call_id"":""call_a"",""caller"":""Bat_A"",""addressee"":""Bat_B"",""context"":""SLEEPING"",""confidence"":0.62}]","{""edges"":[{""source"":""Bat_A"",""target"":""Bat_B"",""count"":1,""contexts"":{""SLEEPING"":1}}]}",0.62
> Every test episode must appear exactly once. Extra, missing, reordered, or duplicate columns; duplicate, missing, or unknown episode IDs; NaN or infinite row confidence; out-of-range row confidence; unreadable CSVs; or inconsistent row counts raise an invalid-submission error. Row-local malformed JSON, oversized JSON cells, invalid call labels, duplicate call IDs, duplicate graph edges, self-edges, invalid graph counts, or graph/call schema mistakes score zero for the affected episode row rather than crashing the whole submission.
> Evaluation
> Higher is better. Theoretical minimum: 0.0. Theoretical maximum: 1.0. A perfect private submission with all confidences equal to 1.0 scores exactly 1.0.
> For each episode, the grader computes:
> caller_accuracy   = mean exact caller match
> addressee_accuracy = mean exact addressee match, including UNKNOWN
> context_accuracy  = mean exact native-context match
> call_core         = 0.45*caller_accuracy + 0.25*addressee_accuracy + 0.30*context_accuracy
> For the submitted graph_json, directed edge counts and edge-context counts are compared with the hidden graph using count F1:
> count_f1 = 2 * overlap / (predicted_total + true_total)
> overlap  = sum over keys min(predicted_count, true_count)
> graph_score = 0.65*directed_edge_count_f1 + 0.35*edge_context_count_f1
> The submitted graph must also agree with the submitted per-call predictions:
> consistency = 0.65*edge_count_f1(graph, calls) + 0.35*edge_context_f1(graph, calls)
> core = 0.80*call_core + 0.15*graph_score + 0.05*consistency
> Confidence only calibrates earned credit:
> call_calibration = mean max(0, 1 - abs(call_confidence - per_call_correctness))
> row_calibration  = max(0, 1 - abs(row_confidence - core))
> episode_score    = core * (0.94 + 0.04*row_calibration + 0.02*call_calibration)
> The final score blends average performance with hidden worst-group robustness over real episode families:
> final = 0.78 * mean(episode_score) + 0.22 * mean(worst_group_mean per hidden axis)
> Hidden axes cover episode node-count family, native unknown-addressee presence, and dominant source context family. These groups are not public.
> Structural file failures raise an invalid-submission error. Row-local malformed JSON, invalid labels, bad call lists, or invalid graph records score 0.0 for the affected episode row. The grader uses generic messages and does not reveal labels, hidden groups, source IDs, split logic, metric internals, or traceback details.

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## Metal Complex Trans-Donor Pair Matching

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78d4j2xeccngqmjkc8aqfv5s8ancvj
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: generative
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Metal Complex Trans-Donor Pair Matching
> Overview
> Each item is one octahedral metal complex, given to you as 2D chemistry only: an opaque metal
> token plus the ligand connectivity graph, with the six coordinating donor atoms tagged D1…D6 in a
> randomised order. All 3D information — coordinates, angles, geometry — has been removed.
> Your job: recover the perfect matching on {D1…D6} — the three donor pairs that sit mutually
> trans (opposite each other, ~180°) across the metal. That is, identify which coordination isomer
> was actually crystallised. There are exactly 15 possible matchings. The output is a graph
> structure, not a class label or a number.
> Task
> train.csv gives complexes with their true trans-pairs revealed, to learn from.
> For every row of test.csv, read the metal, atoms, bonds and donors and output
> trans_pairs: the three trans donor pairs.
> Why it is hard
> The geometry that defines the answer is deleted, so the isomer must be inferred from ligand
> chemistry alone: trans influence, chelate bite angle, pincer/macrocycle topology, fac/mer
> preference, donor-atom electronics.
> The answer is not a computable minimum: the crystallised isomer is fixed by synthesis route and
> kinetics, so enumerating isomers by energy is not a reliable oracle. The label is a recorded
> experimental outcome.
> The output is a structured perfect matching with a hard constraint (each donor has exactly one
> partner), so per-pair scoring must be decoded into a legal matching.
> Chelating ligands force some donors cis, which constrains but never determines the answer.
> Data
> Three files are provided.
> train.csv — labelled complexes, with columns:
> item_id (string) — a 16-character hexadecimal identifier.
> metal (string) — an opaque metal token, e.g. MET_07 (the element identity is concealed).
> atoms (string) — comma-separated element symbols, one per atom index (0-based), metal excluded.
> bonds (string) — ;-separated ligand bonds as i-j atom-index pairs (the ligand connectivity).
> donors (string) — ;-separated Dk:atom_index tags giving the six donor atoms, e.g.
> D1:12;D2:3;D3:47;D4:8;D5:31;D6:20. The D1..D6 labels are randomised per item.
> trans_pairs (string) — the gold matching: three ;-separated Da-Db pairs (train only).
> test.csv — complexes to solve, with columns item_id, metal, atoms, bonds, donors.
> sample_submission.csv — a correctly-formatted example (a fixed matching; scores ≈ chance).
> Complexes are split group-disjoint by (metal + ligand composition), so near-identical complexes
> never span train and test.
> Submission Format
> Produce a CSV with exactly two columns, one row per item_id in test.csv (no duplicates):
> item_id (string) — the identifier, copied from test.csv.
> trans_pairs (string) — three ;-separated pairs Da-Db forming a perfect matching on
> D1…D6 (each label used exactly once). Pair order and within-pair order do not matter.
> Example (submission.csv):
> item_id,trans_pairs
> 3f1c9a0b7e2d4a56,D1-D4;D2-D6;D3-D5
> 908642c5be3e5ae8,D1-D2;D3-D6;D4-D5
> Evaluation
> Metric — mean per-row score, floored at 0. Each row scores:
> row = 0.5 * exact_matching + 0.5 * trans_edge_F1
> where, letting P be your set of 3 predicted pairs and G the gold set of 3 pairs:
> exact_matching = 1 if P == G else 0
> trans_edge_F1  = |P intersect G| / 3
> (Both sets always contain exactly 3 pairs, so precision = recall = F1 = overlap/3. Note |P ∩ G|
> can never be exactly 2 — fixing two pairs forces the third.)
> Aggregation and edge cases:
> Malformed row → 0. A trans_pairs value that is not a valid perfect matching on exactly
> D1…D6 (a label missing, repeated, unknown, or not 3 pairs) scores 0. It is not dropped —
> it still counts in the mean.
> Final score. Average row over all rows, then apply the floor once:
> score = max(0, mean_rows row). The floor applies only to the final mean. A perfect submission
> scores 1.0.
> For reference (all measured on this build): uniform-random guessing over the 15 matchings scores
> ≈ 0.133; a constant matching ≈ 0.139; the best possible constant (oracle-chosen on the test set)
> ≈ 0.146; a metal-token lookup ≈ 0.137; a molecule-size lookup ≈ 0.133. A trained donor-pair
> model reaches ≈ 0.43 (exact ≈ 0.36) in ~30 seconds on CPU. Every non-learning shortcut sits at
> chance — the margin belongs to the model.
> Approaches
> Encode each donor from its local ligand environment (a learned graph/WL encoder, or fine-tune a
> compact chemistry backbone over per-ligand strings with the donor marked), score the 15 candidate
> pairs from the donor embeddings + metal + donor-donor graph distance, and decode the best legal
> perfect matching. Trains in well under a minute on CPU.
> Chelate topology (graph distance between donors) is a strong constraint but not an answer.
> Validate locally by holding out training groups and computing the same metric.
> What Not To Use
> Do not attempt to identify the source structures and look up their geometry from any
> crystallographic database or search engine. The metal is an opaque token and identifiers are
> removed; the isomer must be predicted from the provided graph.
> Classical bag-of-words scoring (TF-IDF and similar) is not a permitted solution — it cannot
> express a matching over labelled donors, and the model must learn.
> Do not hard-code answers. The intended solution generalises to unseen complexes.

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## StrataSplice: Continuous Core Assembly From Overlapping Sensor Logs

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70rx0xnpa7g3kjdpqnkwmrc98a43h6
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Objective: each row provides an anonymized measurement bundle of overlapping multichannel logs from neighboring ocean-drilling core segments. Your job is to select and align the intervals that form one continuous sediment record.
> Each measurement bundle contains six local candidate segments. A segment has a relative depth axis, seven normalized sensor channels, and masks showing which channel samples are present. The public view preserves the local physical signal needed for hole-to-hole alignment while removing site, hole, core, sample labels, source filenames, coordinates, absolute depth, composite depth, source row order, and direct source keys.
> For every test record, submit a splice_json object with two fields. path is the ordered list of selected segment intervals. ties is the ordered list of tie points between adjacent selected intervals. The scored object is the physical splice path itself: which local core intervals are used, where each interval starts and ends, and where adjacent intervals tie together.
> This is a CPU-only challenge. Solutions must run within 1.5 hours on 10 CPU cores and 62 GB RAM. A reasonable strong approach is a compact CPU pipeline using robust channel scaling, masked cross-correlation or constrained dynamic time warping, candidate transition scoring, and dynamic programming over possible segment orders and interval bounds. GPU-only dependencies and hosted inference services are not required or permitted.
> Use the public training records and their splice_json labels to learn reusable sediment-core alignment cues. Do not rely on external source lookup, public PANGAEA table matching, hidden source metadata, row order, file size, or hard-coded record ids.
> Task
> For each test record, infer the continuous splice across the local candidate segments. The output path must be ordered from the top of the local record to the bottom of the local record. Each selected interval is inclusive over integer measurement indices. Each tie must agree exactly with the adjacent path entries: the left tie index is the previous interval end and the right tie index is the next interval start.
> The segment names are local aliases such as S1, S2, and S3. They have no source meaning outside the measurement bundle and may not be compared across rows.
> Intended Approach
> Strong CPU solutions can train or tune directly on the released public files. Useful approaches include masked per-channel similarity, robust smoothing, change-point proposals, constrained single-channel or multichannel DTW, tie scoring between candidate segment ends, and dynamic programming over valid monotone path assemblies.
> Simple fixed templates, segment-id sorting, first-segment rules, or metadata-only baselines are useful diagnostics but are not enough to solve the task. The useful signal is the local multichannel overlap pattern across neighboring candidate segments.
> Allowed tooling is ordinary offline CPU data science on the public files: NumPy, pandas, SciPy, scikit-learn, small CPU PyTorch/JAX/TensorFlow models, custom dynamic programming, and similar local open-source libraries.
> What Not To Use
> Do not use source-object lookup, public PANGAEA table matching, reconstructed site/hole/core/sample identifiers, absolute depth, composite depth, raw filenames, raw row order, or source checksums.
> Do not use record-id hashes, row order, NPZ byte length, filesystem metadata, or hidden split-specific constants as a substitute for signal alignment.
> Do not use private files, answer dictionaries, hard-coded test ids, grader exploitation, hosted APIs, closed remote inference, or GPU-only methods.
> Do not reduce the task to picking the longest segment, sorting local segment names, copying a fixed path template, or submitting malformed JSON to probe the grader.
> Enforcement on invalid approaches: a submission may be rejected before payout if it is built around prohibited source lookup, private-data access, platform exploitation, hard-coded ids, or metadata shortcuts that bypass the intended public sensor-alignment task, even if it obtains a leaderboard score.
> Evaluation
> The metric is the mean row score. Higher is better. The theoretical minimum is 0.0 and the theoretical maximum is 1.0. A perfect valid submission scores exactly 1.0.
> For one row, the grader parses the submitted splice_json and compares it with the private splice. The row score is:
> row_score = 0.5 * path_overlap + 0.5 * tie_score
> path_overlap is the intersection-over-union of selected segment-index cells. If a true path covers cells {(segment, index)} and a predicted path covers another set of cells, path_overlap is the size of their intersection divided by the size of their union.
> tie_score gives credit for ordered adjacent transitions. A submitted tie can match a private tie only when the left and right segment aliases agree and both tie indices are within tolerance. The tolerance is max(2, round(0.03 * segment_length)) on each side. Matched ties receive linearly decreasing credit as their left/right index errors grow within tolerance. Missing or extra ties are penalized by dividing total tie credit by the larger of the predicted and true tie counts.
> Submission-level structural failures raise InvalidSubmissionError: missing, extra, or reordered columns; duplicate ids; missing or extra ids; unreadable id set; or malformed private answer alignment. Row-local malformed splice_json values score 0.0 for that row without crashing or leaking labels.
> The grader zeroes row-local malformed splice objects: unknown keys, unknown segments, non-integer indices, negative indices, out-of-range indices, overlapping intervals on the same segment, inconsistent ties, impossible references, oversized JSON, and overly deep JSON. Submission-level duplicate ids, wrong columns, and missing/extra rows raise generic invalid-submission errors. Grader errors do not reveal private labels or source metadata.
> Dataset
> The public dataset contains 75 labeled training records and 63 unlabeled test records. Train and test records come from separated source-depth families, with gap intervals left unused between held-out and training families. Related or near-duplicate source windows are not split across train and test. Rows are sorted by opaque ids.
> Each measurement file is a compressed NumPy .npz archive. It contains segment_ids, channels, depth_axis, values, and mask. All measurement files have six candidate segments, 160 index positions per segment, and seven channels.
> File overview
> Item	Description
> public/train.csv	Training records
> public/test.csv	Test records
> public/sample_submission.csv	Valid baseline template
> public/packets/*.npz	Sensor arrays
> In prose: train.csv contains opaque row ids, measurement file paths, and training-only splice labels. test.csv contains opaque row ids and measurement file paths with no labels. sample_submission.csv shows the exact required submission columns. The packets/ directory contains the source-neutral local sensor arrays referenced by both train and test rows.
> train.csv columns
> Column	Type	Description
> id	string	Opaque record id
> packet_path	string	Relative NPZ path
> splice_json	string	Train-only splice
> The train.csv columns are: id, an opaque record identifier; packet_path, a relative path under public/; and splice_json, the training label in the same format required for submission.
> test.csv columns
> Column	Type	Description
> id	string	Opaque record id
> packet_path	string	Relative NPZ path
> The test.csv columns are: id, an opaque record identifier, and packet_path, a relative path under public/. There is no splice_json column in test.csv.
> Sensor Measurement File Schema
> Field	Type	Description
> segment_ids	string array	Local segment names
> channels	string array	Channel names
> depth_axis	float array	Relative depth axis
> values	float array	Sensor values
> mask	int array	Present-sample mask
> The values array has shape (6, 160, 7): six local candidate segments, 160 integer positions, and seven channels. The channel order is ms, gra_density, ngr, L_star, a_star, b_star, ln_ca_k. The mask array has the same shape and is 1 where a channel value is present and 0 where it is missing. The depth_axis array has shape (6, 160) and is relative within each segment.
> splice_json has this exact structure:
> {"path":[{"segment":"S1","start_idx":0,"end_idx":96},{"segment":"S2","start_idx":41,"end_idx":143}],"ties":[{"left_segment":"S1","left_idx":96,"right_segment":"S2","right_idx":41}]}
> path is an ordered nonempty list of objects {segment,start_idx,end_idx}. Each segment must be a valid local segment id from the measurement file. start_idx and end_idx must be integers with 0 <= start_idx <= end_idx < segment_length.
> ties is the ordered transition list between adjacent path intervals. It must contain exactly len(path) - 1 objects. Each tie must use the adjacent path segment names, the previous path interval's end_idx, and the next path interval's start_idx.
> Submission
> Submit ./working/submission.csv with exactly these columns in exactly this order: id, splice_json.
> Column	Type	Constraint
> id	string	Same set as test
> splice_json	string	Valid splice object
> Sample Submission
> The following CSV illustrates the required column order and JSON escaping for splice_json.
> id,splice_json
> pkt_0123abcd9999aa,"{""path"":[{""segment"":""S1"",""start_idx"":18,""end_idx"":141},{""segment"":""S4"",""start_idx"":19,""end_idx"":140}],""ties"":[{""left_segment"":""S1"",""left_idx"":141,""right_segment"":""S4"",""right_idx"":19}]}"
> pkt_4567abcd8888bb,"{""path"":[{""segment"":""S2"",""start_idx"":24,""end_idx"":133}],""ties"":[]}"

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## Distributed LoRa Packet Event And Consensus Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dpsf6kb19t93y5psn1aemj58a5nhs
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Plain language objective: several rooftop antennas are listening to the same low-power IoT radio messages. For each short synchronized listening window, reconstruct the message ledger: which packets were present, what bytes they carried, where each receiver heard them, and which receiver observations belong together.
> Each test row provides 2 to 4 synchronized complex I/Q receiver streams plus safe physical-layer settings. Submit one structured row per test case with events_json, detections_json, and confidence.
> This is a CPU-only challenge. Official solutions must run within 1.5 hours on 10 CPU cores and 62 GB RAM. No GPU is required for the official run.
> The expected route is CPU signal processing: LoRa dechirping, CFO search, FFT symbol evidence, packet-start correlation, receiver-wise likelihoods, cross-receiver association, and lightweight sequence models such as a small 1D CNN or TCN. GPU use is not required.
> Train and validate only from the provided public challenge files. The private test rows are grouped by full measurement outings and transmission families, so nearby source windows, repeated payload-linked variants, and receiver captures from the same physical transmission do not cross from training to test. The task remains learnable because the same LoRa physical-layer structure, receiver synchronization, and packet evidence appear in both splits; what changes is the route, propagation condition, receiver availability, and weak-signal impairment mix.
> Task
> For each test case, read all receiver I/Q streams together and submit a packet recovery ledger. The ledger must identify the ordered transmissions present in the shared time window, decode the payload bytes where supportable, use ?? erasures where bytes are not supportable, locate each receiver's packet start bin, and associate receiver detections that correspond to the same transmitted packet. The output is intentionally structured because the useful operational question is not only "did a packet exist?", but which receiver evidence supports each recovered payload and which parts remain uncertain.
> This is not plain modulation classification, receiver/device fingerprinting, SNR regression, geolocation, or a single-receiver demodulation benchmark. A valid solution should use the waveform evidence and the agreement/disagreement across receivers.
> Intended Approach
> Strong CPU-only solutions will likely combine classical LoRa signal processing with lightweight learned components. Useful ingredients include receiver-wise preamble correlation, CFO and drift search, dechirp/FFT symbol likelihoods, timing refinement, whitening or narrowband interference handling, byte-level likelihood aggregation, erasure calibration, cross-receiver dynamic matching, and train-only validation folds grouped by row families. Small CPU-trained 1D CNN/TCN models, calibrated tree models over signal features, or constrained decoders over classical symbol evidence are appropriate if they run offline within the time limit.
> Validate on train-only folds that keep related windows and receiver groups together. Check payload recovery, start-bin tolerance, association F1, erasure calibration, and subgroup performance separately; a method that only predicts nominal start positions or common payload priors should remain weak.
> Dataset
> The public split contains 80 training cases and 80 test cases. The underlying measurements are real low-power LoRa transmissions collected by four synchronized rooftop receiver heads across a campus-scale outdoor environment. The recordings include moving and stationary transmitters, line-of-sight, non-line-of-sight, partial-line-of-sight, and weak indoor or obstructed reception conditions.
> Every prepared case has a compressed .npz file containing complex64 I/Q arrays named by anonymized receiver IDs such as R0, R1, R2, and R3.
> The public I/Q windows are source-neutral weak-reception receiver windows derived from real LoRa captures. Public files remove source filenames, exact timestamps, original row IDs, SNR, offsets, GPS, and payload metadata.
> Item	Description
> train.csv	Labeled train rows
> test.csv	Test rows only
> train/iq/	Train I/Q NPZ
> test/iq/	Test I/Q NPZ
> metadata.json	Format constants
> sample_submission.csv	Valid template
> train.csv columns:
> Column	Type	Description
> id	string	Opaque row ID
> iq_path	path	NPZ I/Q path
> sample_rate_hz	int	Row sample rate
> bandwidth_hz	int	LoRa bandwidth
> spreading_factor	int	LoRa SF
> coding_rate	int	LoRa CR
> bin_samples	int	Samples per bin
> n_receivers	int	2 to 4
> receiver_ids_json	JSON	Receiver ID list
> max_events	int	Event cap
> max_payload_bytes	int	Payload byte cap
> stream_bins	int	I/Q length bins
> task_prompt	string	Task reminder
> events_json	JSON	Train events
> detections_json	JSON	Train detections
> test.csv columns:
> Column	Type	Description
> id	string	Opaque row ID
> iq_path	path	NPZ I/Q path
> sample_rate_hz	int	Row sample rate
> bandwidth_hz	int	LoRa bandwidth
> spreading_factor	int	LoRa SF
> coding_rate	int	LoRa CR
> bin_samples	int	Samples per bin
> n_receivers	int	2 to 4
> receiver_ids_json	JSON	Receiver ID list
> max_events	int	Event cap
> max_payload_bytes	int	Payload byte cap
> stream_bins	int	I/Q length bins
> task_prompt	string	Task reminder
> Each NPZ should be opened with numpy.load. The member names match receiver_ids_json; each member is a one-dimensional complex64 array of I/Q samples, where the real part is I and the imaginary part is Q. All receiver arrays inside one NPZ are synchronized to the same local case timeline and have length stream_bins * bin_samples samples. start_bin values are integer bins on that timeline, and one bin equals bin_samples samples.
> metadata.json contains public format constants and examples: bin_samples, iq_npz_format, the per-row sample_rate_hz note, example events_json and detections_json schemas, and the required submission columns.
> events_json is an ordered list. Each event object has exactly:
> Key	Type	Meaning
> event_id	string	E0, E1, ...
> payload_hex	string	Byte hex or ??
> Payload strings are byte pairs. Unknown bytes may be submitted as ??, one token per byte.
> detections_json is a list of receiver-local detections. Each object has exactly:
> Key	Type	Meaning
> event_id	string	Event reference
> rx	string	Receiver ID
> start_bin	int	Packet start bin
> Submission
> Write the final CSV to ./working/submission.csv.
> The submission must contain exactly these columns in this order:
> Column	Type	Constraint
> id	string	From test.csv
> events_json	JSON	Max 4 events
> detections_json	JSON	Max 20 detections
> confidence	float	0 to 1
> Every test id must appear exactly once. Extra columns, missing columns, reordered columns, duplicate IDs, missing IDs, extra IDs, NaN/Inf confidence, nonnumeric confidence, or confidence outside [0, 1] are structural errors and are rejected by InvalidSubmissionError.
> Row-local malformed JSON, overlong JSON, illegal byte strings, duplicate detection pairs, impossible receiver IDs, bad event references, or invalid start bins receive zero for the affected row/head and no calibration credit, while other valid rows still score normally.
> Example:
> id,events_json,detections_json,confidence
> lora_aaaaaaaaaaaaaaaa,"[{""event_id"":""E0"",""payload_hex"":""??""}]","[]",0.18
> lora_bbbbbbbbbbbbbbbb,"[{""event_id"":""E0"",""payload_hex"":""30303030303132""},{""event_id"":""E1"",""payload_hex"":""??0001""}]","[{""event_id"":""E0"",""rx"":""R0"",""start_bin"":17}]",0.42
> Evaluation
> Higher is better. Theoretical minimum: 0.0. Theoretical maximum: 1.0. A perfect private submission with confidence 1.0 scores exactly 1.0.
> Row score components:
> Head	Weight	Main credit
> Payload bytes	0.45	Exact bytes
> Detections	0.35	Association/start
> Event order	0.08	Ordered IDs
> Consistency	0.06	Valid references
> Confidence	0.06	Calibration
> Payload credit is byte-level. Exact byte pairs receive 1.0, ?? receives 0.24, and wrong bytes receive 0.0. Wrong payload length gives zero for that event payload. payload_score is the mean byte credit over all reference payload bytes in the row.
> Detection credit combines cross-receiver association and timing. Association is F1 over (event_id, rx) pairs. Timing credit for each reference pair is max(0, 1 - abs(start_bin_error) / 10), or 0.0 if that pair is missing. detection_score = 0.45 * association_f1 + 0.55 * mean_timing_credit.
> order_score is 1.0 when the submitted event ID order exactly matches the reference event order and 0.0 otherwise. consistency_score is 1.0 only when row-local JSON parses, event IDs are unique and valid, detections use valid receiver IDs and start bins, and every detection references a submitted event; otherwise it is 0.0.
> First compute task_score = 0.45 * payload_score + 0.35 * detection_score + 0.08 * order_score + 0.06 * consistency_score. Then compute task_target = task_score / 0.94. If consistency_score = 1.0, confidence_score = max(0, 1 - abs(confidence - task_target)); otherwise confidence_score = 0.0. The row score is clip(task_score + 0.06 * confidence_score, 0, 1).
> The final score is:
> 0.74 * mean_row_score + 0.10 * worst_area_group + 0.08 * worst_spreading_factor_group + 0.08 * worst_receiver_count_group.
> Here mean_row_score is the mean row score over all private test rows. worst_area_group is the lowest mean row score across private propagation/mobility groups. worst_spreading_factor_group is the lower mean row score across private spreading-factor groups. worst_receiver_count_group is the lowest mean row score across private receiver-count groups. These group labels are private robustness slices, so they cannot be used as answer shortcuts, but the aggregation formula is exactly as shown.
> What Not To Use / What Not To Do
> Using these approaches can cause rejection regardless of score:
> Do not identify, search, scrape, or use original source archive names, source row IDs, source metadata, payload annotations, filenames, timestamps, offsets, GPS records, SNR fields, or public-corpus lookup tables for hidden test rows.
> Do not use row order, opaque ID hashes, path strings, file sizes, ZIP metadata, NPZ member order, JSON length, or filesystem timestamps as answer channels.
> Do not solve the task as scalar regression, modulation classification, device fingerprinting, receiver localization, or a single-row tabular prediction problem.
> Do not submit a metadata-only, rule-only, or template-only solution that ignores the I/Q evidence.
> Do not use external hosted demodulation services, closed-source teacher APIs, or hidden/private answers.
> Do not exploit malformed JSON floods, duplicate IDs, extra columns, non-finite numbers, or grader/platform side channels.
> Enforcement on invalid approaches: prohibited or non-domain approaches may be rejected before payout even if they produce a numeric score. The task is meant to reward real signal recovery and multi-receiver packet consensus from the provided I/Q streams.

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## Serial Crystallography Lattice Indexing

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7b5n2dh8q032zxx9bg6n05a58a3p65
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: small-data
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> BraggBasis: Ambiguity-Aware Lattice Recovery From Serial Crystallography Peaks
> You are given an anonymized sparse packet of Bragg peaks from one single-shot XFEL serial-crystallography event. Each packet contains local spot IDs, reciprocal-space coordinates, transformed intensity, opaque panel codes, and a list of probe spots. Your task is to recover a physically equivalent reciprocal-lattice basis, estimate the detector-position correction for the event, report a defensible indexability confidence, and assign Miller indices to every requested probe spot.
> In serial crystallography, an X-ray free-electron laser fires very short X-ray pulses at many tiny crystals. Each shot records a sparse diffraction pattern rather than a direct picture of the molecule. The bright Bragg peaks are points in reciprocal space caused by the repeating crystal lattice. Indexing a shot means finding the lattice coordinate system that explains those peaks, then labeling selected peaks with integer Miller indices (h, k, l) so many snapshots can later be merged into structure-factor data.
> The central object is the coupled lattice solution. A prediction must explain the observed reciprocal-space peak set with one coherent basis and must use that basis consistently when assigning probe HKLs. The stored representative is not unique: arbitrary sign flips, axis ordering, and the finite orthorhombic crystallographic basis symmetries are accepted when they describe the same physical solution.
> The released packets are in a packet-local reciprocal coordinate frame and contain only local anonymous identifiers. Source filenames, event tags, run/delay/light-dark labels, original panel names, source row order, file offsets, and direct CrystFEL answer fields are absent from the public split. The visible coordinates have been processed so direct source-row lookup against public crystallography streams is not a reliable route to the hidden answers.
> Current platform budget: design solutions for 10 CPU cores, 62 GB RAM, and 1.5 hours.
> Intended Approaches
> Strong CPU solutions should treat each packet as a sparse reciprocal-lattice recovery problem rather than as tabular regression. Reasonable approaches include:
> Estimate the reciprocal-cell scale and HKL range from public/train.csv.
> Use pairwise-vector voting, RANSAC, FFT-style reciprocal-space voting, or another robust geometric search to propose candidate bases for each packet.
> Assign integer HKLs by constrained rounding or local combinatorial search, then keep basis/HKL pairs that explain many observed peaks consistently.
> Resolve crystallographic sign, permutation, and orthorhombic symmetry ambiguity by scoring physically equivalent bases rather than matching one stored convention.
> Calibrate indexability from train-only validation so confidence tracks lattice/HKL correctness instead of acting as a standalone label.
> What Not To Do
> Using these approaches is grounds for solution rejection on review:
> Do not download, search, or fingerprint public crystallography source streams to recover original event identity or hidden answers.
> Do not use source filenames, event tags, raw stream row order, archive offsets, or any metadata not present in public/.
> Do not read private/answers.csv, grader internals, or platform files outside the public dataset.
> Do not use hosted or closed-source APIs for training, inference, pseudo-labeling, or answer generation.
> Do not submit malformed JSON, duplicate IDs, foreign spot IDs, or values designed to exploit parser behavior.
> Do not run external CrystFEL/DIALS pipelines against recovered raw source events. Implementing indexing ideas on the released packets is allowed.
> Evaluation
> Submit one CSV row per test id with id,prediction_json in that order. For each row, prediction_json must contain:
> reciprocal_basis: a finite 3 by 3 numeric array.
> det_shift_mm: a finite length-2 numeric array.
> indexability: a finite confidence in [0, 1].
> probe_hkl: one object for every requested probe spot, each with exact local spot_id plus integer h, k, and l.
> The grader evaluates every signed/permuted orthorhombic equivalent basis representation and uses the best physically equivalent alignment. There are 48 candidate equivalence operators: all 3-axis permutations and all independent sign flips. Scores are computed per row as follows.
> For one equivalence operator op, the basis score is a smooth tolerance score:
> basis_rms = RMS(predicted_basis - op @ true_basis)
> basis_score(op) = exp(-((basis_rms / 0.012)^2))
> For the same op, the HKL score is exact probe coverage. The submitted probe_hkl list must contain exactly the requested local probe spot IDs. Missing, extra, foreign, or duplicate spot IDs give hkl_score(op) = 0. Otherwise:
> hkl_score(op) = fraction of probe spots whose integer (h,k,l) matches
> the equivalent true Miller index under op
> The basis and HKL terms are coupled through a lattice score:
> lattice_score(op) = sqrt(basis_score(op) * hkl_score(op))
> best_lattice = max lattice_score(op) over the 48 equivalent operators
> Detector shift is scored separately with a 2D Euclidean tolerance in millimeters:
> shift_error = norm(predicted_det_shift_mm - true_det_shift_mm)
> shift_score = exp(-((shift_error / 0.040)^2))
> The row score combines the best lattice/HKL alignment, detector shift, and confidence calibration:
> structural_score = best_lattice * (0.85 + 0.15 * shift_score)
> calibration_score = clip(1 - abs(indexability - best_lattice), 0, 1)
> row_score = clip(structural_score * (0.80 + 0.20 * calibration_score), 0, 1)
> The lattice and HKL terms dominate the metric. If either the basis or probe HKLs are wrong, best_lattice is near zero, so detector shift and confidence cannot earn useful score on their own.
> The final score is:
> valid_score = mean row score over test packets
> final_score = 0.125 + 0.875 * valid_score
> Higher is better. Theoretical minimum for a valid row-aligned submission: 0.125. Theoretical maximum: 1.0. A perfect physically equivalent prediction scores exactly 1.0. A structurally invalid file, such as missing columns, reordered columns, duplicate IDs, or an ID-set mismatch, is rejected. Row-local malformed JSON or invalid row content contributes zero before the valid-submission floor.
> Dataset
> Public files contain train/test CSVs, compact packet JSON files, and a sample submission. Training rows include target JSON records in the same schema as the submission so solvers can learn the reciprocal-basis scale, detector-shift distribution, and valid HKL conventions. Test rows contain only packet paths.
> File overview
> train.csv columns
> test.csv columns
> Packet JSON fields
> Each packet has unit, coordinate_frame, spots, and probe_spot_ids. Each spot has spot_id, qx, qy, qz, log_intensity, and panel. Probe IDs always refer to local spot IDs in the same packet.
> Submission
> Submit a CSV file with a header row and exactly one row per id in public/test.csv. The columns must appear in this exact order:
> Sample Submission Row
> id,prediction_json
> 17,"{""reciprocal_basis"":[[0.10,0.02,0.04],[0.01,0.07,-0.02],[0.04,0.01,0.09]],""det_shift_mm"":[0.002,0.035],""indexability"":0.71,""probe_hkl"":[{""spot_id"":""sp_00"",""h"":4,""k"":-12,""l"":18}]}"

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## Sparse Raman Microplastic Mapping And Next-Scan Planning

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71vwn2xmbkv559n9yfqv9vhn895k0q
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Sparse Raman Microplastic Mapping And Next-Scan Planning
> In plain language, a Raman microscope can see a sample in white light, but measuring every grid location is slow. For each episode, you receive a real source-derived, privacy-processed white-light acquisition thumbnail and Raman spectra measured at only a sparse subset of positions on a 32x32 analysis grid. Your task is to reconstruct an evidence-grounded material map, leave unsupported areas as unknown, cite observed spectra that support connected material regions, and choose five useful next measurements.
> This is a multimodal scientific mapping task. Strong solutions should combine broad image context, sparse Raman spectra, spatial propagation, abstention, and scan planning. A solution that only classifies individual observed spectra or only segments the image will miss important scoring heads. Public artifacts use opaque IDs and redacted paths; they do not contain source filenames, source map names, raw coordinates, repository IDs, or original map dimensions.
> What Not To Do (using these approaches can cause solution rejection regardless of score):
> Do not use source lookup, raw filename lookup, source map-name lookup, repository-index lookup, image fingerprint lookup against external source files, or hidden-answer reconstruction.
> Do not use private files, hidden answers, platform internals, or external hosted inference APIs.
> Do not infer labels from id, image, observed_spectra, row order, file sizes, file modification times, or any artifact outside the provided public files.
> Do not hand-code episode-specific rules, hard-code public IDs, or copy train labels into test rows.
> Do not reduce the task to ordinary per-spectrum classification or image segmentation only; those approaches are allowed as components but are not sufficient.
> Do not rely on GPU training or large downloaded pretrained models. This is CPU-only and should run within 1.5 hours on 10 CPU cores and 62 GB RAM.
> Task
> For each test episode, read the white-light thumbnail, the sparse observed spectra, and the public grid coordinates of those spectra. Submit a 32x32 material map, a connected-region evidence ledger, five next scan coordinates, and a 32x32 uncertainty map.
> The central object is the material map, but the required outputs should agree with each other. A predicted polymer region should be backed by observed Raman evidence from the same episode. The next scan coordinates should target useful unobserved positions rather than repeating nearby measurements. The uncertainty map should mark places where the sparse evidence does not justify a confident material label.
> This is not plain image segmentation, not a per-spectrum classifier, and not a metadata puzzle. The image gives broad particle and foreground context; the observed spectra give material evidence at sparse anchors; the spatial structure determines how far that evidence can be propagated. Strong submissions should combine those signals and abstain with unknown where the public evidence is genuinely insufficient.
> The test rows are not a lookup exercise. Public IDs, file paths, file sizes, row order, source names, raw coordinates, and original map dimensions are not answer channels. Useful models need to learn from the labelled training episodes and generalize to held-out physical maps.
> Intended Approach And Validation
> A practical CPU solution is to decode the training RLE material maps, read each 256-bin observed spectra CSV, resize or featurize each thumbnail, and train a compact per-cell material predictor. Reasonable approaches include spectral PCA or ExtraTrees, k-nearest or gradient-boosted spectral classifiers, patch-level image texture features, shallow CPU segmentation models, graph propagation from observed spectra, and connected-component cleanup.
> Another reasonable route is a two-stage pipeline. First classify or embed the observed spectra using only training labels, then propagate those spectral anchors over the 32x32 grid using image foreground cues, local spatial smoothness, and component morphology. After predicting the map, derive the ledger from connected predicted regions, cite observed spectrum IDs that support each polymer region, select nonredundant next scans in uncertain or under-observed areas, and calibrate the uncertainty bins.
> Use only the released training labels for model selection. Make validation folds from public/train.csv, keeping related-looking episodes or similar material mixtures together where possible, and check all heads: map quality, evidence-ledger validity, scan usefulness, and uncertainty calibration. Calibrate confidence and uncertainty on training-only validation folds so outputs remain finite, schema-valid, and consistent with the predicted map. Open-source local ML/CV libraries and generic offline feature extractors are allowed if they run within the CPU-only limit and do not use external source lookup or hosted inference.
> Evaluation
> Scores are maximized. A perfect submission scores exactly 1.0. Malformed submissions raise InvalidSubmissionError instead of receiving a hidden numeric score. This includes wrong or reordered columns, missing or duplicate IDs, malformed JSON, invalid labels, invalid confidence values, bad support IDs, missing required ledger entries, duplicate support citations, and invalid or already-observed scan coordinates. The error message is generic and does not leak private labels, split logic, scoring weights beyond the public formula, source paths, or stack traces.
> Each test row is scored with five heads:
> independent = 0.46*material + 0.18*ledger + 0.18*scan + 0.12*uncertainty + 0.06*consistency
> joint = sqrt(material * min(ledger, uncertainty, consistency))
> row_score = independent * (0.82 + 0.18*joint)
> The final score is:
> final = 0.78*mean(row_score)
> + 0.08*lowest mean row score over density groups
> + 0.08*lowest mean row score over material-mix groups
> + 0.06*lowest mean row score over source-context groups
> Material-map score is 0.68*mean_cell_credit + 0.32*macro_iou. Correct cells receive 1.0. Incorrect named labels receive 0.0. unknown receives partial credit up to 0.48*(1-support), where support is higher near observed spectra, especially spectra with the hidden true label.
> Ledger score is component_f1 * evidence_quality, so matched regions only receive ledger credit when they are backed by valid observed spectral evidence. Predicted and true nonblank components are greedily matched by same label when component IoU is at least 0.20. Evidence quality rewards cited observed spectra from the same episode whose hidden material agrees with the predicted polymer, plus confidence calibration to that support.
> Next-scan score compares your five proposed coordinates to a hidden static utility map derived from held-out labels and observed positions. Utility rewards discovering unobserved material, resolving under-observed components and boundaries, and covering distant areas. It penalizes coordinates that are duplicates, already observed, out of bounds, or redundant within about 2.5 grid cells.
> Uncertainty score is 1 - mean(abs(predicted_uncertainty - ideal_uncertainty)), after submitted uncertainty bins are divided by 4. Ideal uncertainty is 0 for correct named predictions, 1 for incorrect named predictions, and an intermediate support-aware value for unknown.
> Consistency rewards agreement between the predicted material map, row-major connected-region IDs, ledger polymer labels, and valid scan cardinality. Higher is better. Theoretical minimum: 0.0. Theoretical maximum: 1.0.
> Dataset
> Files shipped to participants are listed below. All paths in CSVs are relative to public/. The prepared split contains 40 training episodes, 14 test episodes, 54 privacy-processed white-light thumbnails, and 54 sparse observed-spectra CSV files.
> Item	Description
> public/train.csv	Labeled train rows
> public/test.csv	Test rows, no labels
> public/train/images/*.bmp	Train WL thumbnails
> public/test/images/*.bmp	Test WL thumbnails
> public/train/observed_spectra/*.csv	Train sparse spectra
> public/test/observed_spectra/*.csv	Test sparse spectra
> public/sample_submission.csv	Submission template
> public/train.csv has 40 rows. It contains the public input columns id, image, observed_spectra, map_shape, scan_budget, observed_count, and prompt, plus the train-only label columns material_map_rle, region_ledger_json, next_scans_json, and uncertainty_map_rle.
> Column	Type	Description
> id	string	Opaque episode id
> image	path string	Relative BMP path
> observed_spectra	path string	Relative spectra CSV
> map_shape	string	Always 32x32
> scan_budget	integer	Always 5
> observed_count	integer	Observed spectra count
> prompt	string	Episode instruction
> material_map_rle	JSON string	Train material map
> region_ledger_json	JSON string	Train region ledger
> next_scans_json	JSON string	Train scan targets
> uncertainty_map_rle	JSON string	Train uncertainty bins
> public/test.csv has 14 rows. It has the test input columns id, image, observed_spectra, map_shape, scan_budget, observed_count, and prompt, with all label columns removed.
> Column	Type	Description
> id	string	Opaque episode id
> image	path string	Relative BMP path
> observed_spectra	path string	Relative spectra CSV
> map_shape	string	Always 32x32
> scan_budget	integer	Always 5
> observed_count	integer	Observed spectra count
> prompt	string	Episode instruction
> Each image file is a privacy-processed white-light thumbnail derived from a source WDF microscope image. It preserves broad source-grounded visual context but is not a raw microscope photograph.
> Each observed spectra CSV contains spectrum_id, x, y, and 256 float spectrum-bin columns from b000 through b255. The spectrum_id values are opaque and can be cited in the ledger. The x and y values are public grid coordinates from 0 to 31.
> Column	Type	Description
> spectrum_id	string	Opaque spectrum id
> x	integer	Grid x coordinate
> y	integer	Grid y coordinate
> b000 to b255	float	Raman spectrum bins
> public/sample_submission.csv is a submission template with exactly the columns id, material_map_rle, region_ledger_json, next_scans_json, and uncertainty_map_rle, filled with a valid weak placeholder baseline.
> Column	Type	Constraint
> id	string	Same ids as test
> material_map_rle	JSON string	32x32 label RLE
> region_ledger_json	JSON string	At most 24 regions
> next_scans_json	JSON string	Five unobserved coords
> uncertainty_map_rle	JSON string	32x32 bins 0 to 4
> Submission
> Write the final submission CSV to exactly ./working/submission.csv. It must contain exactly these columns in this order: id, material_map_rle, region_ledger_json, next_scans_json, uncertainty_map_rle. The id set must match public/test.csv exactly, with no missing IDs and no duplicates.
> material_map_rle must be JSON with shape equal to [32,32] and counts as run-length encoded [label, length] pairs. Allowed labels are blank, ABS, Nylon, PC, PE, PEs, PET, PMMA, POM, PP, PS, PTFE, PU, PVC, Silicone, and unknown.
> {"shape":[32,32],"counts":[["unknown",1024]]}
> region_ledger_json must be a JSON list with at most 24 entries. It must contain exactly one entry for each connected nonblank, nonunknown component in your predicted map, in row-major component order, with no extra or missing regions. Each entry must have exactly region_id, polymer, confidence, and support_ids. Region IDs must be r000, r001, and so on. The polymer cannot be blank or unknown. Confidence must be finite and in [0,1]. support_ids must be nonempty, unique within the row, and each support ID must be an observed spectrum ID from the same episode.
> [{"region_id":"r000","polymer":"PP","confidence":0.7,"support_ids":["spc_abc123"]}]
> next_scans_json must be a JSON list of exactly five unique unobserved integer coordinates in [0,31].
> [[4,7],[12,5],[20,18],[2,25],[29,29]]
> uncertainty_map_rle uses the same RLE structure as material_map_rle, but run values are integer bins 0 through 4. Bin 0 means low uncertainty; bin 4 means high uncertainty.
> Enforcement On Invalid Approaches
> Submissions based on external source lookup, raw filename lookup, visual or spectral fingerprinting, hidden-answer reconstruction, row-order side channels, private files, or grader-format exploitation may be rejected before payout. The task is to learn from the provided public white-light thumbnails, sparse Raman spectra, and train labels.

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## Consensus Arc Span Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx785ghk45y43vvjay04kc94as8anr7k
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat romeo's score of 0.703!

Full challenge description from page:

> RNA families are represented by multiple aligned nucleotide sequences and a consensus base-pair graph. In each row, one contiguous interval of the consensus annotation has been hidden. Reconstruct every missing base-pair arc that touches that interval, including its annotation layer. This is a structured graph-infill task: the answer is a row-local set of paired-column edges, not a category or scalar.
> The alignment has already been projected to consensus columns and cropped to a local window. Sequence names, family names, source coordinates, and global column numbers are not provided. Each row may also be reversed. Its four nucleotide symbols are encoded by a row-local pairing-preserving permutation as 0, 1, 2, and 3; complementary pairs are always 0-3 and 1-2. These transformations preserve alignment covariation and complementary-pair evidence while preventing direct sequence-string joins.
> Dataset Files
> train.csv: 1,476 labeled rows.
> test.csv: 795 unlabeled rows from entirely held-out RNA families.
> sample_submission.csv: 795 valid low-information predictions in submission format.
> train.csv has seven columns:
> id (string): Globally shuffled opaque row identifier.
> column_count (integer): Number of row-local alignment columns.
> alignment_json (JSON list of strings): Between 3 and 24 encoded aligned sequences. Every string has exactly column_count characters drawn from 0, 1, 2, 3, N, and -. N is an unknown or ambiguous base and - is an alignment gap.
> visible_edges_json (JSON list): Visible consensus arcs. Each arc is [left, right, layer], where left and right are zero-based integer columns with 0 <= left < right < column_count, and layer is a string such as L0 or L1.
> masked_span_json (JSON list): Inclusive zero-based interval [start, end] whose consensus annotation is hidden.
> layer_vocab_json (JSON list of strings): The only layer labels valid for that row. L0 is the primary annotation layer; higher labels preserve distinct additional annotation layers, including pseudoknot layers where present.
> answer_json (JSON list): The missing consensus arcs in the same [left, right, layer] format.
> test.csv has the same six feature columns and omits answer_json. Every target arc has at least one endpoint in the inclusive masked span. Every visible arc has both endpoints outside it. A column can participate in at most one arc across the visible and missing edge sets.
> Submission Format
> Submit a CSV with exactly two columns, id and answer_json. Column order and row order do not affect scoring, but no additional or missing columns are accepted. Include every test id exactly once.
> answer_json must be a JSON list of unique [left, right, layer] triples. Both endpoints must be integers in row-local range, left < right, the layer must occur in that row's layer_vocab_json, and at least one endpoint must lie in the row's masked span. Do not pair any column more than once. An empty list is valid JSON, although each packaged target contains at least one edge.
> A complete valid two-row CSV example is:
> id,answer_json
> arc_aa31d8182b09bf886c2c,"[[12,39,""L0""]]"
> arc_cc8c724bba20c3a27c53,"[[16,75,""L0""],[18,73,""L0""],[20,71,""L0""]]"
> Evaluation
> For row r, let P_r be the submitted set of exact (left, right, layer) triples and T_r the hidden true set. The row score is edge-set F1:
> F1_r = 2 * |P_r intersection T_r| / (|P_r| + |T_r|).
> If exactly one set is empty, the row score is 0. If both are empty, it is 1. The leaderboard score is the unweighted arithmetic mean over all test rows:
> Score = (1 / N) * sum_r F1_r.
> The score is bounded by 0 and 1; higher is better. Exact reconstruction of every row scores 1.0.
> Expected Methods
> Useful CPU-compatible approaches include alignment column profiles, complementary-pair statistics, covariation features, dynamic programming, graph completion, compact sequence encoders trained only on train.csv, and constrained decoding that enforces one partner per column. The visible edge graph can provide stem and layer context around the hidden span.
> What Not To Use
> GPU hardware for training, inference, embedding, feature extraction, or search
> Hosted APIs or remote inference services
> Runtime package installation or downloaded/vendored executable code
> External datasets, extra alignments, answer tables, or private/gated assets
> Challenge-specific pretrained or fine-tuned checkpoints presented as general pretrained models
> Manual or automated reverse lookup against the source collection
> Hardcoded row-id, sequence, family, or test-answer maps
> Remote-code loaders such as trust_remote_code=True, torch.hub.load(), or equivalent mechanisms
> Only software and public general-purpose pretrained weights already available in the runtime may be used, and all challenge-specific fitting must use the provided training data on CPU.

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## Spoken Image Tour Route Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7b57cajav8q4tbtdnyycz1598asnk3
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Plain language objective: each test packet contains three mixed image-tour sessions. Reconstruct the three spoken tours by matching each audio recording to its photograph, assigning the phrase cards and pointer traces to the correct tour, ordering the phrases as spoken, and selecting the fixed audio windows in which each phrase occurs.
> The underlying records are real human image-narration sessions. In each original session, an annotator looked at one licensed photograph, spoke a natural description, and moved a pointer over image regions while speaking. The prepared challenge keeps the useful multimodal evidence: transformed photographic scene content, transformed human speech, redacted phrase rhythm, coarsened pointer movement, and fixed public time-window grids. It removes direct source identifiers, filenames, URLs, annotator identifiers, author information, exact upstream timestamps, and original row order.
> Each public packet mixes exactly three such sessions. The packet contains three transformed photographs, three transformed narration recordings, twelve shuffled phrase cards, twelve shuffled pointer-trace shards, and legal audio-window IDs for each public audio file. The original relationships are hidden. All identifiers are packet-local opaque strings such as A1, I2, C07, T04, and W03.
> This is a structured reconstruction task. It is not a single-label classification problem, a captioning problem, or continuous timestamp regression. A useful solution has to combine image evidence, speech evidence, redacted phrase/card evidence, trace geometry, and route ordering.
> For every test packet, submit one JSON object containing three routes. Each route must choose one public audio ID, one public image ID, and an ordered list of steps. Each step pairs one card ID with one trace ID and one or more legal audio-window IDs.
> Dataset
> The public dataset contains packet-level manifests plus the transformed packet media. Paths in train.csv and test.csv are relative to the prepared public directory. The test split has the same public structure as the train split but no target labels.
> File Overview
> Item	Description
> train.csv	Training packet rows
> test.csv	Test packet rows
> sample_submission.csv	Valid weak template
> packets/*/manifest.json	Packet manifest
> packets/*/images/*.jpg	Packet photographs
> packets/*/audio/*.ogg	Packet narrations
> manifest.json Fields
> Each packet_path points to a JSON object with the following fields.
> Field	Type	Description
> packet_id	string	Opaque packet ID matching the CSV row
> prompt	string	Row-local task prompt
> images	array	Three image objects
> images[].image_id	string	Public image ID, one of I1, I2, I3
> images[].path	string	Relative JPEG path such as images/I1.jpg
> audio	array	Three audio objects
> audio[].audio_id	string	Public audio ID, one of A1, A2, A3
> audio[].path	string	Relative OGG path such as audio/A1.ogg
> audio[].windows	array	Legal fixed windows for that audio
> audio[].windows[].window_id	string	Window ID such as W01
> audio[].windows[].start	number	Window start in seconds in the public audio
> audio[].windows[].end	number	Window end in seconds in the public audio
> cards	array	Twelve phrase-card objects
> cards[].card_id	string	Public card ID such as C07
> cards[].text	string	Redacted phrase summary with length and token-type counts
> cards[].token_count	integer	Number of source tokens in the phrase block
> traces	array	Twelve trace-shard objects
> traces[].trace_id	string	Public trace ID such as T04
> traces[].points	array	Ordered [x, y] points normalized to [0, 1]
> train.csv Columns
> Column	Type	Description
> packet_id	string	Opaque packet ID
> packet_path	string	Path to manifest.json
> prompt	string	Task instruction
> target_json	JSON string	Correct route object for training
> The target_json value has the same schema expected in submissions: one object with a routes array. Use these train-only targets to learn the structure and to build a local validation split.
> test.csv Columns
> Column	Type	Description
> packet_id	string	Opaque packet ID
> packet_path	string	Path to manifest.json
> prompt	string	Task instruction
> test.csv contains only public inputs. It does not include target routes, source identifiers, original filenames, URLs, annotator identifiers, author information, exact source timestamps, hidden group labels, private answer metadata, or source annotation columns.
> Submission
> Submit ./working/submission.csv with a header row and exactly one row per packet_id in test.csv. The header must contain these two columns in this exact order:
> Column	Type	Constraint
> packet_id	string	Same ID set as test.csv
> prediction_json	string	Route JSON object
> For each packet, prediction_json must be one JSON object. The top-level object has a routes array. Each route object has audio_id, image_id, and steps. Each step object has card_id, trace_id, and audio_windows.
> Example route object shape: {"routes":[{"audio_id":"A1","image_id":"I2","steps":[{"card_id":"C07","trace_id":"T04","audio_windows":["W03","W04"]}]}]}.
> Required semantics:
> exactly one route per public audio ID;
> every public audio ID and image ID is used exactly once;
> steps are listed in spoken order;
> every card ID and trace ID is assigned exactly once;
> each step has one card_id, one trace_id, and a nonempty ordered list of legal window IDs from that route's audio.
> Example of a correctly formatted two-line CSV submission:
> packet_id,prediction_json
> Pabc123,"{""routes"":[{""audio_id"":""A1"",""image_id"":""I2"",""steps"":[{""card_id"":""C07"",""trace_id"":""T04"",""audio_windows"":[""W03"",""W04""]}]},{""audio_id"":""A2"",""image_id"":""I1"",""steps"":[{""card_id"":""C03"",""trace_id"":""T09"",""audio_windows"":[""W01""]}]},{""audio_id"":""A3"",""image_id"":""I3"",""steps"":[{""card_id"":""C11"",""trace_id"":""T02"",""audio_windows"":[""W02""]}]}]}"
> Evaluation
> Each packet receives a score in [0, 1], and the final leaderboard score is the mean over test packets. Higher is better. The theoretical minimum is 0.0; the theoretical maximum is 1.0. A perfect valid submission scores exactly 1.0.
> For each packet, the grader parses prediction_json and compares it with the hidden target using three heads:
> Head	Weight	Definition
> Audio-image assignment	0.20	Fraction of the three audio IDs assigned to the correct image ID
> Step alignment	0.55	Soft maximum-matching F1 over card, trace, window, and audio fields
> Route order	0.25	F1 over adjacent card pairs within each audio route
> The row score is 0.20 x assignment_score + 0.55 x step_score + 0.25 x order_score.
> assignment_score is the fraction of the three gold audio-to-image pairs recovered exactly. If the route structure is invalid, this head is 0.
> step_score first requires a structurally valid step set that uses every required card ID exactly once and every required trace ID exactly once. The grader then computes a soft bipartite matching between submitted steps and gold steps. A submitted/gold step pair receives 0.35 x exact card_id match, plus 0.30 x exact trace_id match, plus 0.25 x Jaccard(submitted audio_windows, gold audio_windows), plus 0.10 x exact audio_id match.
> The best non-overlapping submitted/gold step matches are accumulated, then converted to precision, recall, and F1. This gives partial credit for recovering part of a step while still rewarding complete one-to-one reconstruction.
> order_score is F1 over ordered adjacent card edges. For each route, every neighboring pair of submitted cards creates an edge (audio_id, previous_card_id, next_card_id). The grader compares the submitted edge set with the gold edge set.
> Structural CSV errors are invalid-submission errors. These include missing, extra, or reordered columns; duplicate packet IDs; a packet ID set different from test.csv; unsupported control characters; and an oversized top-level CSV. Row-local malformed JSON, impossible IDs, duplicate card or trace assignments, illegal windows, overlong JSON, or overly deep JSON receive zero for the affected row components without crashing the grader.
> Generalization Contract
> Train and test packets use disjoint source records and disjoint source families where available. A complete original narration session never crosses split boundaries. Public packet IDs, media filenames, card IDs, trace IDs, and window IDs are opaque row-local handles.
> Solutions should learn from the public packet evidence: transformed photograph content, speech/audio evidence, redacted phrase rhythm, pointer geometry, and the fixed window grids. Do not rely on row order, file sizes, packet IDs, source lookup, recovered metadata, or external annotation search.
> Practical CPU Modeling Guidance
> The official setting is CPU-only: 10 CPU cores, 62 GB RAM, and a 1.5 hour wall-clock limit. Practical approaches should stay lightweight.
> Training-Only Validation Guidance
> Use train.csv, training packet manifests, and training targets to create your own validation split. Keep complete packets together. Do not tune on hidden test labels, infer labels through private files, or reconstruct answers through source metadata, filesystem details, source corpus lookup, or challenge-generation artifacts.
> What Not To Use
> Using any of the approaches below is grounds for rejection on review, regardless of leaderboard score:
> source-corpus lookup, public annotation search, reverse-image search, audio fingerprinting, text-card lookup, or trace-shape lookup against external collections;
> source identifiers, URLs, original filenames, author names, annotator identifiers, exact upstream timestamps, raw row order, file sizes, file mtimes, or packet-ID side channels;
> hosted or closed-source APIs for training, inference, pseudo-labeling, transcription, image understanding, or route recovery;
> hardcoded answer dictionaries, manual labeling of hidden test rows, private-file access, grader exploitation, or platform-internal state;
> malformed CSV/JSON, duplicate rows, extra columns, illegal IDs, impossible windows, oversized JSON, or other format hacks;
> treating the challenge as only classification, captioning, source retrieval, or continuous timestamp regression instead of producing the required route JSON.
> Enforcement on invalid approaches: submissions or writeups that rely on lookup, recovered metadata, private files, hosted-model shortcuts, hard-coded answers, or task-reducing shortcuts may be rejected even if the CSV is structurally valid. The intended route is to infer the structured route JSON from the provided public training data and packet evidence.

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## Blind Surface Contact Portfolio Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx730asx75p84481jpshaxh0758avqxp
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Plain language objective: for each portfolio, reconstruct which anonymous haptic probes belong to which anonymous surface photographs, what contact command produced each matched probe, and which shared sensor-to-image frame calibration explains the whole portfolio.
> Each row contains 3 or 4 anonymous surface photographs plus a shuffled set of friction probes. A probe contains a fixed-duration cleaned friction-audio file and a matching acceleration/force signal file. Most probes belong to one displayed surface, and some portfolios include one unmatched probe from a different calibration session. The required answer is one bounded JSON object that jointly gives the frame map, the probe-to-surface matches, every matched probe's contact program, and the unmatched probe set.
> This is not material classification, continuous regression, or independent per-file labeling. A useful answer must solve the portfolio-wide assignment graph and the shared finite calibration, then keep all contact-program fields consistent with those decisions.
> Only CPU solutions are allowed. The solution runtime limit is 1.5 hours on 10 CPU cores and 62 GB RAM. Runtime internet use, source-data lookup, hidden-answer access, and GPU-only pipelines are not allowed.
> What Not To Use / What Not To Do:
> Do not look up the original source archive, source filenames, texture IDs, material names, directory names, timestamps, position traces, or raw sensor files for hidden rows.
> Do not use runtime internet access, external copies of the raw source, source-media fingerprinting, file-size side channels, row order, opaque-ID hashes, or private files.
> Do not submit a material classifier, a per-probe contact classifier with no assignment graph, a metadata-only solver, or a fixed JSON template that ignores the media.
> Do not reduce the task to image-only retrieval, audio-only lookup, continuous velocity regression, or independent labels for each file.
> Do not exploit malformed JSON floods, duplicate IDs, extra columns, non-finite confidence values, or grader/platform side channels.
> Enforcement on invalid approaches: submissions may be reviewed for source lookup, runtime network use, private-file access, metadata-only behavior, and solutions that avoid the structured portfolio-reconstruction contract. Prohibited approaches can be rejected before payout even if the CSV is structurally valid.
> Task
> For each test row, read portfolio_json, load the referenced surface images and probe files, and submit one prediction_json object.
> The object has exactly these top-level keys:
> {"frame_map":"ROT90_FLIP_X","matches":[],"unmatched_probes":[]}
> frame_map is one of:
> ID, ROT90, ROT180, ROT270, FLIP_X, FLIP_Y, ROT90_FLIP_X, ROT90_FLIP_Y
> Each item in matches has exactly:
> {"probe_id":"P_1","surface_id":"S_C","direction":"NE","speed":"V40","force":"F500"}
> Allowed direction values are:
> N, NE, E, SE, S, SW, W, NW
> Allowed speed values are:
> V20, V30, V40, V50, V60
> Allowed force values are:
> F500, F1000
> unmatched_probes is a sorted list of probe IDs such as ["P_3"]. Matches must be sorted by probe_id; unmatched probes must be sorted; every row-local probe must appear exactly once either in matches or in unmatched_probes. A surface can be matched at most once.
> Intended Approach and Validation
> A practical CPU solution is to build train-only multimodal features for every surface and probe, then solve each portfolio as a constrained matching problem. Surface photographs can be represented with local texture descriptors, color and gradient statistics, compact CNN embeddings computed offline on CPU, or patch-level features. Probe recordings can be represented with audio spectra, MFCC-like band energies, zero-crossing and envelope statistics, acceleration FFT features, axis-energy ratios, and force summaries.
> One reasonable pipeline is to train compatibility models from train.csv: score each possible probe-surface pair, predict each matched probe's direction, speed, and force from the audio and sensor evidence, then run Hungarian or other assignment decoding under the one-probe-per-surface constraint. The shared frame_map should be searched over the eight allowed calibration tokens and chosen jointly with the assignment, rather than predicted independently from one file.
> Another reasonable route is a two-stage portfolio decoder. First, learn probe embeddings and surface embeddings from train-only labels, including modality-specific models for contact program tokens. Second, combine pair scores, program probabilities, unmatched-probe likelihood, and calibration consistency into a row-level structured decoder. The submitted heads should agree: a probe listed as unmatched should not also appear in matches, a surface should not receive two probes, and the contact program should be plausible for the same probe used in the assignment.
> Use only released training rows for model selection. Make validation folds from train.csv that avoid row-order and path shortcuts, for example by holding out complete surface families within the training surfaces or by stratifying on calibration token, unmatched-probe state, speed token, and force token. Check assignment F1, contact-program accuracy, frame-map accuracy, unmatched-set behavior, and the final portfolio score. Open-source local CV, audio, signal-processing, and classical ML libraries are allowed if they run within the CPU limit and do not use upstream source lookup, hidden test information, hosted APIs, runtime internet, or GPU-only computation.
> Dataset
> The public prepared data contains 360 labeled training portfolios and 150 hidden-label test portfolios. Each portfolio has local surface IDs and probe IDs that are meaningful only inside that row. Public IDs are opaque and sorted; no source filename, texture ID, material family, original path, position trace, or timestamp is provided.
> Prepared files:
> Item	Description
> train.csv	Labeled portfolios
> test.csv	Test portfolios
> sample_submission.csv	Valid weak template
> train/portfolios/<id>/surfaces/*.jpg	Train surface photos
> train/portfolios/<id>/probes/*.wav	Train probe audio
> train/portfolios/<id>/probes/*_signals.npz	Train accel/force probes
> test/portfolios/<id>/surfaces/*.jpg	Test surface photos
> test/portfolios/<id>/probes/*.wav	Test probe audio
> test/portfolios/<id>/probes/*_signals.npz	Test accel/force probes
> sample_submission.csv is a valid weak template and placeholder for the required submission schema.
> portfolio_json is a JSON object with surfaces, probes, audio_hz, sensor_hz, and duration_sec.
> Each surfaces item has surface_id and image, pointing to an anonymous JPEG under that row's surfaces/ folder. Each probes item has probe_id, audio, and signals, pointing to one cleaned fixed-duration WAV and one fixed-shape NumPy .npz under that row's probes/ folder. The signals file contains accel_uvn, force_n, sensor_hz, and duration_sec. accel_uvn has fixed shape (1024, 3) and force_n has fixed length 1024.
> train.csv columns:
> Column	Type	Description
> id	string	Opaque row id
> portfolio_json	JSON	Public inputs
> target_json	JSON	Train target
> Plain train column definitions: id is the opaque portfolio key; portfolio_json lists the surface/probe files and fixed sampling metadata; target_json is the train-only answer object with frame_map, matches, and unmatched_probes.
> test.csv columns:
> Column	Type	Description
> id	string	Opaque row id
> portfolio_json	JSON	Public inputs
> Plain test column definitions: id is the opaque portfolio key; portfolio_json lists the surface/probe files and fixed sampling metadata. Test rows do not contain target fields.
> Submission
> Write the final CSV to ./working/submission.csv. It must contain exactly these columns in this order and exactly one row for every test ID.
> Column	Type	Constraint
> id	string	Same set as test
> prediction_json	JSON	Valid target object
> confidence	float	In [0,1]
> Example:
> id,prediction_json,confidence
> bsc_0123456789abcdef,"{""frame_map"":""ROT90_FLIP_X"",""matches"":[{""direction"":""NE"",""force"":""F500"",""probe_id"":""P_1"",""speed"":""V40"",""surface_id"":""S_C""}],""unmatched_probes"":[""P_3""]}",0.42
> Wrong columns, reordered columns, missing IDs, extra IDs, duplicate IDs, nonnumeric confidence, non-finite confidence, confidence outside [0,1], oversized CSVs, or unreadable CSVs raise InvalidSubmissionError. Malformed row-local JSON, overlong JSON cells, invalid local IDs, duplicate JSON keys, extra JSON keys, invalid tokens, unsorted match lists, or impossible match/unmatched references give zero for the affected row rather than crashing the whole submission.
> Evaluation
> Minimum score: 0.0. Maximum score: 1.0. Higher is better. A perfect submission with confidence = 1.0 scores exactly 1.0.
> Each row receives four semantic component scores:
> Component	Definition	Weight
> Assignment	Edge F1	0.45
> Program	Tuple components	0.30
> Frame map	Exact token	0.15
> Unmatched	Set F1	0.10
> Assignment is F1 over (probe_id, surface_id) edges. Program credit is computed only on correctly assigned probe-surface pairs and combines direction, speed, force, and exact tuple credit. Frame-map credit is exact over the 8 calibration tokens. Unmatched credit is F1 over the row-local unmatched probe set, with double-empty sets scoring 1.0.
> The row semantic score is:
> 0.45 * assignment
> + 0.30 * program
> + 0.15 * frame_map
> + 0.10 * unmatched
> The confidence column adds a small calibration factor but cannot rescue a wrong structure:
> row_score = semantic * (0.92 + 0.08 * max(0, 1 - abs(confidence - semantic)))
> The final score is the mean row score blended with hidden worst-group robustness when groups are large enough:
> final = 0.88 * mean(row_score)
> + 0.12 * mean(worst_group_scores)
> Hidden groups cover calibration token, frame-map family, and unmatched-probe state. Each hidden frame-map token has at least 18 test rows, and unmatched/no-unmatched groups have 50 and 100 rows.

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## Legal-Move Preservation Ranking in Six-Piece Chess

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70whewrsq3pwc6zz3dccf0r58akr05
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Legal-Move Preservation Ranking in Six-Piece Chess
> Problem Description
> Overview
> Rank legal moves by how well they preserve the strongest theoretical result available in a six-piece chess endgame.
> The main target is counterfactual result degradation: for each supplied legal move, determine whether the resulting child position preserves the best available result or drops to a worse result class.
> Each test position provides a normalized FEN string, an 8 × 8 signed-integer board representation, the side to move, and a deterministically shuffled list of all legal candidate moves in lowercase UCI notation.
> For every test position, submit three outcome probabilities and five legal moves ordered from most to least result-preserving. Move ranking is the primary task; root-position outcome probabilities are auxiliary.
> Dataset
> public/
> ├── train/
> │   └── <position_id>.json
> ├── test/
> │   └── <position_id>.json
> ├── train.csv
> └── sample_submission.csv
> public/train/: labeled-position JSON files.
> public/test/: unlabeled-position JSON files with the same public schema.
> public/train.csv: training labels and move-level relevance.
> public/sample_submission.csv: one valid example row per test position.
> The public position fields are:
> position_id (string): Opaque position identifier.
> fen (string): Normalized Forsyth–Edwards Notation.
> board (JSON list of lists of integers): Signed 8 × 8 board matrix.
> side_to_move (string): white or black.
> candidate_moves (JSON list of strings): All legal UCI moves in deterministic row-local shuffled order.
> legal_move_count (integer): Number of legal moves.
> in_check (boolean): Whether the side to move is in check.
> piece_count (integer): Always 6.
> material_signature (string): Material configuration from the mover's perspective.
> The creator-side master JSONL also contains an opaque game_id. Exactly one selected position is permitted per game_id. The game_id is used only for split construction and is not exposed in public position files.
> The training columns are:
> position_id
> filename
> outcome
> root_wdl
> criticality
> optimal_move_count
> best_moves
> move_relevance
> Move relevance is:
> Relevance	Meaning
> 3	Preserves the best available result
> 2	Drops one result level below the best
> 1	Drops two result levels below the best
> 0	Drops three or more result levels below the best
> Criticality is:
> Label	Meaning
> only_move	Exactly one legal move preserves the best result
> narrow	Two or three legal moves preserve the best result
> flexible	Four or more legal moves preserve the best result
> Split and Leakage Controls
> The private set is constructed deterministically at the game_id group level.
> The preparation pipeline enforces all of the following:
> exactly one selected record per game_id;
> no game_id appears in both training and evaluation;
> exact and symmetry-equivalent root positions are deduplicated upstream;
> private selection prioritizes only_move and narrow positions;
> private selection prefers positions with many legal alternatives and few optimal moves;
> candidate-move order is deterministically shuffled for every public row;
> no normalized child FEN reached by one legal move from any test position is present as a training root FEN.
> For the last rule, the preparation script applies every supplied candidate_moves entry to every proposed test position. If a generated child FEN exists among training roots, the split is invalid. Test selection is therefore constructed as an outgoing-closed set over the observed one-ply position graph, followed by a hard zero-collision assertion.
> This prevents direct one-ply neighborhood transfer from a labeled training root to an evaluation position.
> Submission Format
> position_id,p_win,p_draw,p_loss,move_1,move_2,move_3,move_4,move_5
> Example:
> position_id,p_win,p_draw,p_loss,move_1,move_2,move_3,move_4,move_5
> eg_198bd6f2134f8e01cd42,0.70,0.25,0.05,e4e5,g2f2,f3f4,g2h2,g2f1
> Every test ID must appear exactly once. Probabilities must be finite, non-negative, and have positive total mass. Moves must use lowercase UCI notation. Missing, repeated, malformed, or unknown moves receive zero credit at the affected rank.
> Evaluation
> score =
> 0.20 × outcome_score
> + 0.60 × top1_preservation
> + 0.20 × move_ndcg_at_5
> outcome_score is exp(-macro_log_loss), where log loss is calculated separately for true wins, draws, and losses and then averaged.
> top1_preservation is the weighted accuracy with which move_1 has relevance 3.
> move_ndcg_at_5 is NDCG@5 using gain 2^relevance - 1.
> For both move components, criticality weights are:
> only_move: 0.60
> narrow:    0.30
> flexible:  0.10
> Scores range from 0 to 1, and higher is better.
> Expected Methods
> Suitable CPU methods include board-geometry features, king-distance and opposition features, pawn-race features, attack and defense maps, child-position features, pairwise move-preference models, learning-to-rank objectives, compact tree ensembles, small CPU-trained board encoders, and symmetry-aware augmentation.
> Strong solutions should model the change caused by each move rather than only the root position.
> Compute Limits
> CPU only.
> Up to 10 CPU cores.
> Up to 62 GB RAM.
> Maximum runtime of 1.5 hours.
> What Not To Use
> GPUs, TPUs, accelerators, or GPU-backed services.
> Internet access during execution.
> Online tablebase APIs.
> External Syzygy files.
> Stockfish tablebase probing.
> External labeled chess-endgame datasets.
> Hosted APIs or remote inference.
> Runtime downloads or package installation.
> Challenge-specific pretrained checkpoints.
> Hardcoded private answers, row mappings, or manually annotated test positions.
> General-purpose offline chess libraries may be used only when they do not provide exact tablebase answers.

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## Northeast India Shared Tokenizer Design

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f2qxyhnk4cn79emghtc27v58awtjz
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Northeast India Shared Tokenizer Design
> Overview
> This is an LLM-pretraining and tokenizer-design challenge. You are given text from nine languages spoken in Northeast India. Your job is to design one compact tokenizer codebook that represents all nine languages efficiently, including languages with very little training data.
> In plain terms, you must submit 1,024 byte-token merge definitions. The grader turns those definitions into an executable tokenizer and applies it to private multilingual text. A good submission shortens text in every language instead of spending nearly all its vocabulary on the largest corpora.
> The nine languages are Assamese, Garo, Khasi, Kokborok, Meitei, Mizo, Nagamese, Nyishi, and Pnar. They span three language families and multiple writing systems. This matters in real LLM systems: inefficient tokenization increases training cost, inference cost, context usage, and fragmentation for underrepresented languages.
> This is not classification or regression. The complete submission is one global model artifact: a hierarchical byte-token codebook.
> Dataset files
> train.csv contains the public tokenizer-training corpus.
> id — string. An anonymized public sentence ID.
> language — string. One of asm, grt, kha, trp, mni, lus, nag, njz, or pbv.
> language_name — string. Human-readable language name.
> language_family — string. Indo-Aryan, Austroasiatic, or Sino-Tibetan.
> source_group — string. An anonymized source-group alias. It is useful for group-disjoint local validation.
> text — string. UTF-8 training text.
> There is no row-level target in train.csv. Solvers learn the tokenizer directly from the corpus.
> test.csv contains 16 identical artifact-replica requests. Replication lets the platform evaluate complete tokenizer artifacts after it partitions leaderboard rows; it does not create 16 different language tasks.
> id — string. Artifact-row ID from A000 through A015.
> artifact_type — string. Always shared_byte_tokenizer.
> required_merges — integer. Always 1024.
> max_token_bytes — integer. Always 24.
> sample_submission.csv repeats one valid but useless JSON codebook in every artifact row. Every learned token contains the NUL byte, which does not appear in evaluated text, so the sample scores exactly 0.
> Output language
> The tokenizer begins with 256 base tokens:
> B00 represents byte hexadecimal 00.
> B01 represents byte hexadecimal 01.
> …
> BFF represents byte hexadecimal FF.
> Each predicted_codebook value is a JSON list that creates 1,024 additional tokens. Merge M0000 concatenates two base tokens. A later merge may reference any base token or an earlier learned token.
> Example:
> M0000 = B61 + B62
> M0001 = M0000 + B63
> M0000 represents UTF-8 bytes 61 62, which are text ab. M0001 represents bytes 61 62 63, which are text abc.
> Every object inside the JSON list has exactly these keys:
> id — the required merge ID.
> left_token_id — a base token or earlier merge ID.
> right_token_id — a base token or earlier merge ID.
> Rules:
> A merge may reference B00–BFF.
> A merge may reference only earlier M rows, never itself or a future row.
> Concatenation order is left token followed by right token.
> Every resulting byte sequence must be unique.
> Every resulting token must contain at most 24 bytes.
> Partial UTF-8 byte sequences are allowed because this is a byte-level tokenizer.
> All 1,024 merge objects are required inside every artifact row.
> Merge objects may appear in any JSON-list order because the grader aligns them by merge ID before construction.
> Tokenization procedure
> For every private text:
> Normalize the text to Unicode NFC.
> Encode it as UTF-8 bytes.
> At the current byte position, find every submitted learned token whose bytes match.
> Emit the longest matching learned token.
> If no learned token matches, emit the single base-byte token.
> Advance by the emitted token length and continue until all bytes are consumed.
> Because learned byte sequences must be unique, longest-match ties cannot occur. The tokenizer is lossless: concatenating emitted token bytes always reconstructs the normalized input exactly.
> Evaluation
> Content errors such as an unknown token reference, a forward reference, a duplicated derived byte sequence, or an over-length token make the global codebook invalid and return score 0. Structural CSV errors such as missing IDs, duplicate IDs, unknown IDs, missing rows, extra columns, or wrong column order are rejected.
> Private evaluation contains at least 300 monolingual cases for every language, plus large code-switch, orthographic-variation, and long-tail sets. Private source groups are disjoint from public training groups. Private cases are not direct copies of a named public test file.
> For any evaluation group, first define raw efficiency:
> ByteCount = number of UTF-8 bytes in the NFC-normalized group text
> TokenCount = number of tokens emitted by the submitted tokenizer
> ReferenceTokenCount = number of tokens emitted by the private reference codebook
> RawEfficiency =
> clip((ByteCount - TokenCount) / (ByteCount - ReferenceTokenCount), 0, 1)
> The byte-only tokenizer therefore has raw efficiency 0. A codebook matching or beating the reference has raw efficiency 1 for that group.
> MacroLanguageEfficiency is the arithmetic mean of the nine monolingual raw-efficiency values.
> WorstThreeLanguageEfficiency is the arithmetic mean of the three lowest monolingual values. It prevents a solution from sacrificing small languages.
> CodeSwitchEfficiency is raw efficiency over private source-new passages that combine material from two different languages.
> LongTailRobustness combines two private components:
> LongTailRobustness =
> 0.65 * LongTailEfficiency
> + 0.35 * OrthographicVariationEfficiency
> LongTailEfficiency emphasizes rare words from Garo, Kokborok, Nagamese, Nyishi, and Pnar. OrthographicVariationEfficiency uses punctuation, case, date, digit, and canonically equivalent Unicode variants.
> The private scorer also measures a fixed pooled-BPE anchor trained only on the public corpus. This anchor represents the straightforward solution that ignores language balancing. For each of the four components above, define:
> ClosedGap(component) =
> clip(
> (component - anchor_component)
> / (1 - anchor_component),
> 0,
> 1
> )
> StrictComponent(component) = ClosedGap(component) * ClosedGap(component)
> This measures the fraction of the remaining gap between ordinary pooled BPE and the private reference that the submission closes. Squaring prevents a nearly pooled solution from receiving most of the scale and makes consistent improvement across difficult languages matter. A submission at or below the pooled anchor receives 0 for that component; the reference receives 1.
> The score for one codebook artifact is:
> artifact_score =
> 0.40 * StrictComponent(MacroLanguageEfficiency)
> + 0.30 * StrictComponent(WorstThreeLanguageEfficiency)
> + 0.20 * StrictComponent(CodeSwitchEfficiency)
> + 0.10 * StrictComponent(LongTailRobustness)
> The grader evaluates every artifact row present in the platform-provided answer partition and returns their arithmetic mean:
> partition_score = mean(artifact_score for artifact rows in that partition)
> Submit the same best codebook in all 16 rows. If different codebooks are supplied, they are scored independently and averaged, so submitting weaker alternatives cannot improve on repeating the strongest artifact. An empty platform-generated partition returns 0 without crashing; it carries no evaluated artifact rows.
> Scores are finite and bounded in [0, 1]. The sample submission scores 0. The private reference codebook scores 1.
> Participants can calculate tokenizer behavior on public text, but cannot exactly reproduce private component scores without the private evaluation corpus.
> Submission format
> Submit a CSV with exactly two columns in this order:
> id — string. Artifact-row ID from test.csv.
> predicted_codebook — string. A JSON list containing exactly 1,024 merge objects.
> One merge object looks like:
> {"id":"M0001","left_token_id":"M0000","right_token_id":"B63"}
> The following CSV is schematic; the actual JSON field must contain every merge from M0000 through M1023, and the same complete value must be repeated for every test ID:
> id,predicted_codebook
> A000,"[{""id"":""M0000"",""left_token_id"":""B61"",""right_token_id"":""B62""},{""id"":""M0001"",""left_token_id"":""M0000"",""right_token_id"":""B63""}, ... complete through M1023 ...]"
> CSV artifact rows may appear in any order because the grader aligns them by id. Use ordinary CSV quote escaping exactly as demonstrated by sample_submission.csv.
> Recommended solution approach
> A basic solution can train byte-pair merges on pooled public text. Stronger solutions should consider language-balanced sampling, the worst-language objective, script diversity, long-tail words, and whether a merge is useful across related languages. CPU implementations using pair counts, tries, or standard tokenizer libraries fit within the runtime limit.
> What not to use
> Do not infer meaning from artifact IDs, merge IDs, JSON order, or CSV row order; they are only structural identifiers.
> Do not reference future merge IDs, invent token IDs, duplicate derived byte strings, or exceed the byte limit.
> Do not submit Unicode token strings, raw hexadecimal sequences, tokenizer model files, or natural-language explanations. Submit the exact JSON-list grammar inside predicted_codebook.
> Do not optimize only Assamese, Meitei, Khasi, or Mizo. The worst-three-language component heavily penalizes language starvation.
> Do not assume public sentence lookup reveals the private score. Private source groups, code-switched passages, long-tail cases, and orthographic variants are separately constructed.
> Do not key behavior to source IDs, source-group aliases, merge IDs, or row order.
> Resource limit
> Solutions have 90 minutes, 10 CPU cores, and 62 GB RAM. No GPU is required or expected.
> Benchmark boundary
> Prior work studies tokenizer fertility, multilingual vocabulary imbalance, SentencePiece or BPE training, and parity-aware token allocation. NE-BERT itself reports a weighted tokenizer for these languages. Those works compare fixed tokenizers or training algorithms.
> This benchmark instead asks each solver to submit a complete executable codebook under a fixed global merge budget. It evaluates that artifact on hidden source-disjoint monolingual, worst-language, code-switch, rare-word, and orthographic-robustness groups. It is therefore a constrained multilingual tokenizer-design problem rather than a tokenizer comparison table, language-model perplexity benchmark, text classification task, or ordinary next-token prediction task.

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.

## Contrastive Trajectory Evidence Set Completion

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ceva4xr7zszhwn6221y9rw98asv2g
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Evidence synthesis often begins with a small set of trusted observations and a larger pool of plausible continuations. The difficult part is deciding which new evidence belongs to the same underlying trajectory when a closely related process produces similar findings, interventions, and time expressions.
> Each case provides four trusted trajectory anchors and twelve candidate relation-evidence bundles. Exactly four candidates continue the focus trajectory. The remaining eight come from its paired contrast trajectory and are deliberately matched on relation type, object type, temporal regime, and vocabulary.
> Natural-language words use a stable private token vocabulary. The same private token has the same meaning throughout train and test, but source wording and condition names cannot be recovered by ordinary web search. The anchor set supplies case-level evidence for the focus trajectory, while labeled training cases teach which private patterns and structured fields transfer across entity groups.
> The task is set completion. Evidence is already bundled with its structured relation, and no chronological sorting is required or scored.
> Task
> Select exactly four bundle IDs and return them in ascending identifier order, joined by >.
> Example target style: B01>B04>B07>B10
> Valid IDs range from B00 through B11. Every selected ID must be unique.
> Dataset
> The public dataset contains 368 training cases and 136 test cases.
> train.csv: labeled anchor-and-candidate cases.
> test.csv: unlabeled cases from disjoint destination-entity groups.
> sample_submission.csv: one valid, varied prediction for every test case.
> train.csv Columns
> case_id (string): anonymous case identifier.
> focus_code (string): one of six stable anonymous trajectory codes.
> trajectory_seed (JSON string): four trusted anchor bundles from the focus trajectory.
> candidate_bundles (JSON string): twelve shuffled candidate bundles.
> target_bundle_set (string): the four correct candidate IDs in ascending order.
> test.csv Columns
> case_id (string): anonymous case identifier.
> focus_code (string): stable anonymous trajectory code.
> trajectory_seed (JSON string): four trusted focus anchors.
> candidate_bundles (JSON string): twelve shuffled candidates.
> sample_submission.csv Columns
> case_id (string): must match every test ID exactly once.
> pred_bundle_set (string): four ascending candidate IDs.
> Bundle Fields
> Every anchor and candidate bundle contains:
> subject_tokens (string): private-token relation subject.
> subject_type (string): semantic subject category.
> relation_tokens (string): private-token relation predicate.
> object_tokens (string): private-token relation object.
> object_type (string): semantic object category.
> time_tokens (string): private-token temporal expression.
> time_band (string): coarse temporal regime from TB_0 through TB_5.
> evidence_tokens (string): private-token supporting evidence.
> Candidate bundles additionally contain bundle_id. Anchor bundles contain anchor_id.
> Train and test are disjoint by connected destination-entity components and share no exact evidence excerpts.
> Evaluation
> The score is bounded between 0 and 1 and is maximized.
> Score = 0.70 * ChanceCorrectedSelectionSkill + 0.30 * ExactSetAccuracy
> RawBundleSelectionF1 is standard micro F1 over (case_id, bundle_id) pairs. Every selected distractor is a false positive, and every omitted continuation is a false negative.
> Every valid row selects four of twelve candidates while the truth also contains four. Uniform random selection therefore has expected raw F1 1/3. The chance-corrected component is ChanceCorrectedSelectionSkill = max(0, (RawBundleSelectionF1 - 1/3) / (2/3)). Random performance maps to approximately zero and perfect selection maps to one.
> ExactSetAccuracy is the fraction of cases whose complete four-bundle set exactly matches the target.
> These are the only metric components. There is no ordering score, attachment score, hidden track, or additional weight.
> Malformed row-level sets receive zero credit for that row. File-level contract violations, including missing IDs, duplicate IDs, unknown IDs, and extra columns, raise an error.
> Submission
> Submit a CSV with exactly case_id and pred_bundle_set.
> Example:
> case_id,pred_bundle_set TSC_12ab34cd56ef78,B01>B04>B07>B10 TSC_98fe76dc54ba32,B00>B03>B08>B11
> Allowed And Prohibited Methods
> Allowed methods include CPU-compatible sparse retrieval, contrastive feature models, compact encoders, set scorers, and constrained decoders trained only on the supplied public data.
> Prohibited methods include decoding private tokens with external corpora, matching cases to the source release, hardcoded test labels, source-identifier maps, and row-order or ID-based shortcuts. All training and inference must run within 1.5 hours using 10 CPU cores and 62 GB of RAM.

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.
## Historical Listing Continuation From Noisy Field Sketches

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74z8bv5evq26k33cf4qrrkbn8avx4d
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Beat dominico's score of 0.622!

### Full Challenge Description

> Overview
> Historical directories preserve snapshots of businesses and services across many editions. Linking recurring listings is difficult because addresses, proprietor fields, telephone numbers, category text, typography, and transcription quality can vary between appearances.
> Each challenge case begins with one anchor listing and twelve candidate cards drawn from three later editions. Four candidates are shown for each time step. Exactly one card at each step continues the same conservatively normalized recurring listing. The other cards are real listings from the same location and edition and were selected to be plausible confusers.
> Sensitive listing strings are represented as case-local noisy n-gram sketches. Matching source fragments receive the same sketch token only when that fragment survives independent observation dropout; every field also contains deterministic collision tokens. The representation preserves partial continuation evidence while preventing exact-name, exact-address, and archival lookup shortcuts. Train and test use disjoint recurring-listing keys and do not share source rows.
> The benchmark uses a conservative continuation definition based on normalized recurring listings. Resolving two differently named establishments as the same real-world business is outside the target contract.
> Task
> For every case, submit three atoms joined by semicolons.
> Each atom uses the format step|card_id.
> Valid example:
> 1|C07;2|C01;3|C10
> The steps must appear as 1, 2, and 3. Card IDs range from C00 through C11, and all three selected cards must be distinct.
> Dataset
> The public files are:
> train.csv: input cases and target identity chains.
> test.csv: input cases without target chains.
> sample_submission.csv: one valid, varied prediction for every test case.
> train.csv Columns
> case_id (string): anonymous case identifier.
> location_code (string): anonymous geographic grouping code.
> anchor_listing (JSON string): the starting listing.
> candidate_cards (JSON string): twelve candidate listing cards.
> target_chain (string): the three-atom gold trajectory.
> The anchor object contains year and five sketch strings: name_sketch, address_sketch, category_sketch, proprietor_sketch, and phone_sketch.
> Each candidate object contains:
> card_id (string): case-local ID from C00 through C11.
> step (integer): target time step, from 1 through 3.
> year_offset (integer): years after the anchor edition.
> year (integer): edition year.
> name_sketch (string): noisy case-local character-shingle tokens for the establishment name.
> address_sketch (string): noisy case-local character-shingle tokens for the address.
> category_sketch (string): noisy case-local character-shingle tokens for the category.
> proprietor_sketch (string): noisy case-local character-shingle tokens for the proprietor field.
> phone_sketch (string): noisy case-local character-bigram tokens for the telephone field.
> test.csv Columns
> case_id (string)
> location_code (string)
> anchor_listing (JSON string)
> candidate_cards (JSON string)
> sample_submission.csv Columns
> case_id (string)
> pred_chain (string)
> Evaluation
> The score is bounded in [0, 1], and higher is better.
> Score = 0.45 * ListingSelectionF1 + 0.30 * StepAccuracy + 0.25 * ExactTrajectoryAccuracy
> ListingSelectionF1
> Standard set F1 over all (case_id, card_id) pairs. Incorrect selected cards are false positives, and omitted target cards are false negatives.
> ListingSelectionF1 = 2TP / (2TP + FP + FN)
> StepAccuracy
> The fraction of the three target steps for which the predicted card exactly matches the card assigned to that step. A missing or malformed row receives zero credit for all three steps.
> ExactTrajectoryAccuracy
> The fraction of cases whose complete three-atom prediction exactly matches the target trajectory.
> These three displayed terms are the complete metric. There are no hidden tracks or additional score components.
> Submission
> Submit a CSV containing exactly case_id and pred_chain.
> Example:
> case_id,pred_chain
> DIR_12ab34cd56ef78,"1|C07;2|C01;3|C10"
> DIR_98fe76dc54ba32,"1|C03;2|C11;3|C05"
> Every test ID must appear exactly once. Unknown IDs, missing IDs, duplicate IDs, and extra columns raise an error. Blank or malformed row-level chains receive zero credit for that case.
> Allowed And Prohibited Methods
> Allowed methods:
> CPU-compatible sparse retrieval, sketch-overlap models, record-linkage models, compact encoders, sequence models, and constrained decoders.
> Training only from the supplied public challenge files.
> Deterministic output parsing and validity checks.
> Prohibited methods:
> Attempting to reverse case-local sketch tokens or searching external directory scans, archival catalogs, or source copies to identify test listings.
> Hardcoded test identities, manually constructed answer maps, or source-row lookup systems.
> Deriving predictions from case IDs, row order, card order, or file order.
> A non-ML shortcut system whose answers depend on manually encoded establishments.
> Solutions must train and run within 1.5 hours using 10 CPU cores and 62 GB of RAM.

Inspiration note: Useful as inspiration for corrupted-clue recovery where the model must identify and repair unreliable evidence.
## Binocular Gaze Log Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx717ac7rymwxv1crsr383b78n8aq72s
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering, small-data, multimodal, Dataset source is visible after the challenge closes.
- Best/top context: Beat mrnguyen's score of 68.385!

### Full Challenge Description

> Binocular Gaze Log Repair
> The Incident
> A binocular eye tracker normally writes two synchronized event logs: one for the left eye and one for the right. In this challenge, a logging failure has erased the event indices from the right-eye stream. The right-eye measurements survived, but they were detached from their timestamps and stored in an arbitrary order.
> Your job is to produce a repair manifest that puts those detached records back into their original chronology.
> The challenge is built from genuine binocular eye-tracking trials. The failure scenario is applied deterministically: right-eye records are shuffled, some synchronization evidence is withheld, and the original recorded chronology is retained as the answer. No target sequence is invented, randomized, or relabeled.
> Several fragments survived the logging failure:
> fixation_cards is the unordered registry of right-eye events.
> temporal_bands contains coarse early, middle, or late checkpoints for some cards.
> left_witness is the still-ordered left-eye log, with some entries unreadable.
> saccade_sketch contains surviving direction and distance diagnostics between consecutive right-eye events.
> cue_cell, scene_family, aperture_code, and aperture_profile describe the acquisition conditions.
> The two eyes do not always produce the same number of fixation events, revisits can occur in the same screen region, and many checkpoint or motion records are missing. About 70% of card checkpoints survive, and about half of the ordered left-eye records remain readable. Repairing the log therefore requires global alignment and path consistency rather than a simple sort.
> Record Format
> Right-eye cards use the form Cdd:Xdd:Ydd:Dd:
> Cdd is the row-local card identifier that must appear in the repair manifest.
> X00 through X11 identify horizontal screen cells.
> Y00 through Y07 identify vertical screen cells.
> D0 through D5 are increasing dwell-time bins.
> A temporal checkpoint is written as Cdd:Bd, where B0, B1, and B2 mean early, middle, and late. An unreadable checkpoint is Cdd:B?.
> The ordered left-eye log uses Xdd:Ydd:Dd entries. An unreadable left-eye event is X?:Y?:D?.
> Right-eye motion diagnostics use Qd:Rd. Q0 through Q7 encode eight direction sectors, while R0 through R3 encode increasing movement ranges. A missing diagnostic is Q?:R?.
> The required output is a space-separated permutation of card identifiers, for example:
> C04 C01 C07 C02 C00 C03 C06 C05
> Every target contains 8–18 cards.
> Recovery Score
> The grader rewards correct global order, intact consecutive transitions, and the two endpoints.
> Let the recorded order be
> 𝑦
> =
> (
> 𝑦
> 1
> ,
> …
> ,
> 𝑦
> 𝑚
> )
> y=(y
> 1
> ​
> ,…,y
> m
> ​
> ) and the submitted repair be
> 𝑝
> p. The target contains
> 𝑇
> =
> 𝑚
> (
> 𝑚
> −
> 1
> )
> /
> 2
> T=m(m−1)/2 ordered card pairs. Let
> 𝑐
> c be the number of target pairs whose cards both occur in
> 𝑝
> p in the correct relative order. Only the first occurrence of a valid target card can establish its position. Define
> [
> O=\max\left(0,\frac{2c-T}{T}\right).
> ]
> Next, form the multisets of directed adjacent edges
> 𝐸
> 𝑝
> =
> {
> (
> 𝑝
> 𝑖
> ,
> 𝑝
> 𝑖
> +
> 1
> )
> }
> E
> p
> ​
> ={(p
> i
> ​
> ,p
> i+1
> ​
> )} and
> 𝐸
> 𝑦
> =
> {
> (
> 𝑦
> 𝑖
> ,
> 𝑦
> 𝑖
> +
> 1
> )
> }
> E
> y
> ​
> ={(y
> i
> ​
> ,y
> i+1
> ​
> )}. If their overlap count is
> 𝑒
> e, define
> [
> P_E=\frac{e}{|E_p|},\qquad R_E=\frac{e}{|E_y|},\qquad
> F_E=\frac{2P_ER_E}{P_E+R_E}.
> ]
> Set
> 𝐹
> 𝐸
> =
> 0
> F
> E
> ​
> =0 when either edge set is empty or the denominator is zero. The endpoint term is
> [
> H=\frac{1}{2}\mathbf{1}[p_1=y_1]+\frac{1}{2}\mathbf{1}[p_{|p|}=y_m],
> ]
> with
> 𝐻
> =
> 0
> H=0 for an empty repair.
> The final score is
> [
> 100\times\operatorname{clip}(0.40O+0.50F_E+0.10H,0,1).
> ]
> The theoretical minimum is 0 and the maximum is 100. Missing cards, unknown cards, duplicates, malformed values, and extra tokens provide no abstention advantage.
> Measured public-data-only references are: empty sample submission 0.000000; arbitrary stored-card order 9.061814; checkpoint-only repair 33.340124; binocular alignment 41.587201; CPU beam repair 47.543374; wide CPU beam reference 50.510999; perfect repair 100.000000.
> Files
> train.csv
> Contains 3,600 repaired historical incidents.
> sample_id - int64 - Content-free incident identifier.
> fixation_cards - string - Detached right-eye records in arbitrary storage order.
> temporal_bands - string - Surviving card checkpoints and explicit missing checkpoints.
> left_witness - string - Ordered, partially unreadable left-eye reference log.
> saccade_sketch - string - Ordered, partially missing right-eye motion diagnostics.
> cue_cell - string - Coarse initial cue location.
> scene_family - string - Deidentified scene family S0 through S5.
> aperture_code - string - Deidentified viewing-aperture code A00 through A26.
> aperture_profile - string - Coarse aperture geometry in Vd_Id form.
> calibration_lane - string - Balanced nuisance value A or B; it is not a target signal.
> visit_order - string - Correct repair manifest.
> test.csv
> Contains 1,600 damaged logs with the same evidence columns and no visit_order.
> sample_submission.csv
> Contains the required header and every test identifier.
> Train and test use disjoint source images. Participant identifiers, source image names, raw timestamps, original trial identifiers, and fixation indices have been removed from participant-facing files.
> Submission
> Submit exactly two columns in this order:
> sample_id,visit_order
> 4126,C00 C01 C02 C03 C04 C05 C06 C07 C08
> 2358,C00 C01 C02 C03 C04 C05 C06 C07 C08 C09 C10 C11
> 4175,C00 C01 C02 C03 C04 C05 C06 C07 C08 C09
> The example uses real test IDs but merely repeats the arbitrary storage order, so it is a valid low-skill submission rather than a solution.
> Submit exactly 1,600 data rows plus the header. Every sample_id must match one test incident exactly. Column reordering, extra columns, duplicate IDs, missing IDs, unknown IDs, and extra rows are rejected. Submission row order may differ because grading aligns rows by ID.
> Repair Strategy Hints
> Use visible checkpoints to establish a partial early-to-late ordering.
> Align the left-eye reference log with right-eye cards using position and dwell information, while allowing unmatched events on either side.
> Treat each visible motion diagnostic as a constraint on a consecutive card pair.
> Decode one complete permutation globally; independent card ranks can violate otherwise strong transition evidence.
> Ignore calibration_lane: it is balanced within scene-family and sequence-length strata.
> The strongest systems will combine partial-order constraints, imperfect binocular alignment, and transition-aware path search.

Inspiration note: Useful as inspiration for route/path reconstruction outputs with explicit evidence structure.
## Recovering a Hidden Sequence from Coarse Coders with a Planted Impostor

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx735r0d45szwmyhswpx9sjb3d8axn28
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Beat mrnguyen's score of 57.673!

### Full Challenge Description

> Recovering a Hidden Sequence from Coarse Coders with a Planted Impostor
> Overview
> Real-world setting. Imagine a faded document whose true character sequence is
> unknown. It is transcribed independently by five low-fidelity readers ("coders").
> Each reader has poor discrimination: it cannot tell exact characters apart, only which
> broad group a character belongs to, and it leaves gaps where it cannot read a
> position at all. Different readers group the characters differently, so no single
> transcript identifies a character, but agreeing evidence from several readers narrows
> it down. The twist: one of the five readers was mistakenly given a **different but
> similar document**, so its transcript is internally sensible yet describes the wrong
> text. Your job is to reconcile the honest readers to recover the true sequence and to
> flag which reader was the mismatched one. This is a stylized, fully controlled version
> of multi-source record reconciliation and unreliable-annotator aggregation.
> Concretely. The hidden target is a sequence of tokens. Each token is one of 19
> distinct symbols, written M01, M02, M03, …, up to M19 (nineteen literal token
> strings, not a range of numbers). A token carries no numeric meaning; it is just a
> label. Each of the five coders reports, for every position of the sequence, one of
> four category codes, written c0, c1, c2, and c3 (four literal strings), or the
> special code NA meaning that coder skipped that position. Each coder uses its own
> fixed but hidden rule that maps every one of the 19 tokens to one of the 4 categories.
> Because 19 tokens are squeezed into 4 categories, many tokens share a category within a
> single coder, so one coder alone is highly ambiguous. The coders' rules are the same
> for every item, so they can be learned from the training split, where the true
> token sequence is given alongside the five reports. In addition, each coder randomly
> skips about a third of its positions (reported as NA) and reports a wrong category on a
> small fraction of the rest.
> Exactly one of the five coders per item is a planted impostor: instead of the true
> sequence, it reports categories for a different, confusable token sequence, and you are
> not told its index. Combining all five coders naively lets the impostor corrupt the
> answer, so you must find and exclude it.
> What "ordering" means here and why it helps. The token sequences are not random:
> in the training data, some tokens tend to follow others (there is learnable local
> structure, like letter patterns in words). A model can learn, from the training
> sequences, how likely each token is to follow the previous token — a *token-transition
> prior*. When the honest coders narrow a position down to several possible tokens but
> cannot pick one, this learned prior helps choose the most plausible token given its
> neighbours.
> Two things are predicted per item: the full token sequence, and the index (0 to 4)
> of the impostor coder.
> Intended approach. From train.csv, learn (a) for each coder, which tokens each
> category can correspond to, and (b) the token-transition prior. For each test item,
> intersect the candidate tokens the coders allow at each position; identify the impostor
> as the coder whose removal most improves agreement among the rest; then read off the
> sequence from the remaining coders, using the transition prior to break ties where the
> honest coders still allow several tokens.
> Evaluation
> Each item is scored, then the item scores are averaged. For one item, let the true
> token sequence be T = (t_1, …, t_L) with L positions, let the true impostor index be
> q = impostor_coder, and let the submitted sequence be P = (p_1, …, p_M) with the
> submitted impostor index q̂ = pred_impostor. Position i in every coder report and in
> T refers to the same underlying position, and L equals the number of space-separated
> codes in each coder report for that item.
> Token accuracy. Compare token by token up to the shorter length:
> matched = number of positions i with 1 ≤ i ≤ min(L, M) and p_i = t_i.
> acc = matched / L. So if your sequence is shorter than L, the missing positions
> count as wrong (the denominator is always L); if it is longer than L, the extra
> tokens are ignored.
> Exact match. exact = 1 if M = L and p_i = t_i for every position, otherwise 0.
> Impostor match. impostor_hit = 1 if q̂ = q, otherwise 0.
> Per-item score. s = 0.65 · acc + 0.20 · exact + 0.15 · impostor_hit.
> The final score is the mean of s over the N test items, clipped to [0, 1] and scaled
> to 100:
> Score = 100 · clip( (1/N) · Σ s , 0, 1 ), where clip(x, 0, 1) = min(max(x, 0), 1).
> Because each s is already in [0, 1], the clip only guards against malformed input.
> Score = 0 means no token was ever placed correctly and the impostor was never
> found; Score = 100 means every sequence was decoded exactly and every impostor
> identified. Higher is better.
> Measured reference scores on the test split with this exact grader:
> Constant guess (predict token M01 at every position, impostor 0) — 3.5
> Combining all five coders while ignoring the impostor — 41.0
> Learned coder rules + impostor detection + token-transition prior — 54.9
> Perfect answer — 100.0
> Finding the impostor is worth roughly fourteen points over ignoring it, and resolving
> the remaining ambiguous positions gives further, real headroom above that. The
> four-category coarseness, the skipped positions, and the impostor together keep
> achievable scores well below saturation.
> Dataset
> Files in public/:
> train.csv — labelled items, one row per item, with these columns:
> chain_id — int — unique item identifier.
> coder0, coder1, coder2, coder3, coder4 — string — the five coder reports.
> Each is a space-separated list of per-position codes; each code is one of the four
> category strings c0, c1, c2, c3, or NA for a skipped position. All five
> reports for an item have the same number of codes, L.
> sequence — string — the target: a space-separated list of L tokens, each one of
> the nineteen strings M01, M02, …, M19.
> impostor_coder — int — the index (0, 1, 2, 3, or 4) of the impostor coder.
> test.csv — one row per test item, with only chain_id and the five report columns
> coder0, coder1, coder2, coder3, coder4 (no sequence, no impostor_coder).
> category_legend.csv — a small fixed reference (not per-item) listing the codes that
> appear in the coder columns, with columns:
> code — string — one of c0, c1, c2, c3, or NA.
> meaning — string — plain-text meaning, where c0 through c3 are the four
> categories and NA means the coder skipped that position. It is only a parsing aid;
> it contains no information about any specific item.
> sample_submission.csv — a correctly formatted, low-scoring example.
> Submission
> Submit a CSV with exactly these three columns, in this order:
> chain_id — int — a test item identifier from test.csv.
> sequence — string — your predicted tokens as a space-separated list, for example
> M04 M11 M02 M09 M17 M03. Its length should equal L, the number of codes in that
> item's coder reports. Every token must be one of M01, M02, …, M19.
> pred_impostor — int — your predicted impostor coder index (0, 1, 2, 3, or 4).
> Requirements:
> The test set has 2794 items; submit exactly 2794 rows (one per test item) plus a
> header row.
> Each chain_id in test.csv appears exactly once — no missing, duplicate, unknown, or
> extra ids.
> Example submission line for a test item with chain_id = 1 whose coder reports each
> have 10 positions: 1,M04 M11 M02 M09 M17 M03 M08 M14 M05 M12,3 — a 10-token sequence
> followed by the predicted impostor index 3.
> What Not to Use
> A single coder. Each coder maps 19 tokens onto only 4 categories, so no coder
> identifies a token by itself; decoding one coder scores near chance.
> Combining all five coders without finding the impostor. The impostor disagrees on
> the positions where its source sequence differs, poisoning naive aggregation — this
> is the difference between about 41 and the mid-50s.
> Ignoring pred_impostor or guessing it at random: it is a scored term, and you
> cannot aggregate cleanly without finding the impostor.
> Per-position independent classification. Positions interact through the shared,
> learned coder rules and the single impostor; scoring each position alone discards the
> cross-position and cross-coder structure and the token-transition prior.
> Constant or majority-token sequences: near 0.
> What is expected instead: learn the coder rules and the token-transition prior from the
> training split, intersect the per-position candidate tokens across coders, detect and
> drop the one impostor coder, and decode the sequence, using the learned prior where the
> honest coders remain ambiguous.

Inspiration note: Useful as inspiration for corrupted-clue recovery where the model must identify and repair unreliable evidence.
## Affective Knock Audio Retrieval

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bmfvdaperdq1151rkr0j7918aw92e
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Beat rekht's score of 0.083!

### Full Challenge Description

> Affective Knock Audio Retrieval
> Overview
> A knock on a door is a physical signature. The way a person strikes wood, how hard, how fast, how many times, with what rhythm and what force behind each blow, is as particular to a single act of knocking as a spoken phrase is to a voice. This challenge asks a model to recognise that signature. You are given the first part of a knocking action and a large gallery of knock fragments, and you must find the one fragment that came from the same knock.
> The recordings were made by a professional foley artist knocking on a real door with a specific emotional intention behind each action: pounding in anger, a frightened rap, a cheerful tap, a flat neutral delivery, a heavy knock of grief. From each action two fixed-length fragments are cut, an opening query fragment drawn from earlier in the action and a gallery fragment drawn from later in it. Both fragments are the same length, so no fragment's duration reveals which action it came from. Your model sees the query and must rank the gallery so that the fragment cut from the same original action sits at the top.
> This is a retrieval problem, not a classification problem. There is no fixed label set to predict over. There is a gallery of candidate fragments and a query, and the task is to rank the gallery so the one correct fragment sits as close to the top as possible. The output for each query is a ranked list of gallery ids, best guess first.
> What makes this hard is that the gallery is full of near misses. Many fragments were knocked with the same emotional intention as the query, at a similar force and a similar tempo, on the same door. Coarse acoustic cues, how loud, how fast, roughly what timbre, get a model into the right neighbourhood of the gallery but not to the single correct fragment. Separating the true match from a crowd of same-emotion, same-instrument distractors demands a fine-grained learned representation of the knock itself, not a category guess.
> This is not speech recognition and it is not sound-event classification. It is fine-grained audio instance retrieval: learning an embedding of a percussive action precise enough to re-identify it from a held-out fragment.
> What makes this challenge distinct
> One correct answer in a large gallery. Every query has exactly one right fragment in the gallery. Getting the emotional neighbourhood right is not enough; the metric rewards putting the exact matching fragment first, and near misses inside a crowded region of the gallery cost real score. Random ranking scores essentially zero.
> Same-emotion distractors are the difficulty. When a coarse model gets a query wrong, its top pick is a fragment of the same emotional intention roughly two thirds of the time. The gallery is dense with acoustically similar knocks, so the signal that resolves the true match is fine timing and timbre structure, not gross loudness or tempo. A model that only learns to tell an angry knock from a sad one plateaus quickly.
> The loudness shortcut has been removed. In the raw recordings the angry and fearful knocks are far louder than the sad ones, and many clip the microphone while the quiet ones never do. Absolute energy would let a model group knocks by emotion without understanding any individual one. Every fragment has been peak-normalised to the same level before release, so loudness is gone and the model must rank on structure that survives normalisation.
> Query and gallery are drawn from different parts of the action. The query fragment comes from earlier in the action and the gallery fragment from later, so a model cannot win by matching a continuous acoustic tail. The representation has to capture what is stable about the whole action, its rhythmic and timbral identity, across two different slices of it.
> A learned embedding is the only way in. There is no gloss to match, no string to compare, no table to look up. The query fragment and the gallery fragment share no metadata, and their ids are opaque. The only route to ranking the correct fragment to the top is to encode both the query and every gallery item into a shared space where fragments of the same action land near each other. That is a trained neural audio encoder; corpus statistics and surface features do not get there.
> Dataset
> The recordings are door knocks performed with five emotional intentions: anger, fear, happiness, neutral, and sadness. Each action is a short sequence of individual knocks. From each action, a query fragment is cropped from an earlier window and a gallery fragment from a later window. Every fragment is cropped to exactly the same fixed length (0.3 seconds, 14400 samples) so that no fragment's duration carries any information about which action it came from. Both fragments are peak-normalised.
> Audio format: 48 kHz, mono, 16-bit PCM WAV, every clip exactly 14400 samples long. There are 490 query fragments and 490 gallery fragments, one matching pair per original action, balanced across the five emotional intentions at 98 pairs each.
> queries/audio/ contains 490 WAV files, one per query. queries.csv lists them:
> Column      Type    Description
> --------------------------------------------------------------------------
> query_id    str     Query identifier, matching a file query_id.wav in queries/audio/
> gallery/audio/ contains 490 WAV files, one per gallery fragment. gallery.csv lists them:
> Column       Type    Description
> --------------------------------------------------------------------------
> gallery_id   str     Gallery identifier, matching a file gallery_id.wav in gallery/audio/
> The gallery is the full ranking candidate pool. For every query, exactly one gallery fragment is the correct match, and it is always present in the gallery. Your job is to rank it to the top.
> Query and gallery ids are opaque and carry no information about the pairing or the emotional intention. A query id and its correct gallery id share no decodable structure; do not attempt to match them by parsing ids.
> Evaluation
> Each query is scored by where the correct gallery fragment lands in your ranked list. The primary metric is Mean Reciprocal Rank at 10.
> For a single query, let rank be the 1-based position of the correct gallery fragment within the first 10 entries of your ranked prediction. The reciprocal rank is 1 divided by that position, and 0 if the correct fragment does not appear in the top 10.
> reciprocal_rank = 1 / rank   if the correct fragment is in the top 10
> reciprocal_rank = 0          otherwise
> MRR@10 = mean(reciprocal_rank over all queries)
> The score is the mean of the reciprocal rank over all 490 queries. Putting the right fragment first scores 1.0 on that query, second 0.5, third 0.333, and so on down to tenth at 0.1. Anything past tenth scores nothing.
> For calibration under this exact metric:
> Strategy                                              MRR@10
> --------------------------------------------------------------
> Random ranking of the gallery                         ~0.006
> Raw MFCC features, cosine similarity, no training      ~0.23
> Learned contrastive audio embedding                    the target
> Rank the correct fragment first for every query        1.00
> The MFCC number is the reference point to internalise. Off-the-shelf acoustic features already place the correct fragment in the top ten for some queries, because emotion and gross tempo survive into both halves of an action. Moving well beyond ~0.23 requires a model that learns an embedding precise enough to tell one angry knock from another. That is where the headroom is. Higher is better, range 0.0 to 1.0.
> Submission Format
> Submit a CSV with one row per query.
> Column               Type    Description
> --------------------------------------------------------------------------
> query_id             str     Query id from queries.csv
> ranked_gallery_ids   str     Space-separated ranked list of gallery ids,
> best guess first, up to 10 entries
> Example rows:
> query_id,ranked_gallery_ids
> q_1a2b3c4d5e6f,g_9f8e7d6c5b4a g_0011223344ff g_aabbccddeeff ...
> q_2b3c4d5e6f70,g_112233445566 g_778899aabbcc g_ddeeff001122 ...
> Requirements:
> Exactly one row per query_id in queries.csv Include the header row ranked_gallery_ids must be a non-empty, space-separated list of gallery ids Only the first 10 entries are read; extra entries past rank 10 are ignored Gallery ids are matched as exact strings
> A query present in the test set but missing from your submission, or a row whose correct fragment is absent from the top 10, scores 0 on that query.
> The provided sample_submission.csv gives every query the same fixed ranked list of gallery ids. It is a valid submission out of the box and scores approximately 0; it shows the exact format the grader expects.
> What To Use
> Any pretrained audio model available on HuggingFace that fits the compute budget below is permitted. A wav2vec2 base encoder, an audio spectrogram transformer, or a small spectrogram convolutional network used as an embedding backbone are all suitable. A dual-encoder trained with a contrastive objective over the training pairs is the natural approach: encode the query and each gallery fragment into a shared space, then rank by similarity. You may mine hard negatives from same-emotion fragments, augment the audio, engineer log-mel or MFCC front ends, and ensemble your own trained models. Training a compact embedding network from scratch on the provided fragments is a legitimate solution and fits the budget with room to spare.
> What Not To Use
> External audio corpora, or any outside knocking or impact-sound dataset used to recover the correct fragment for a query. The embedding must be learned from the provided fragments.
> Any retrieval of the source recordings at inference to recover the correct gallery fragment for a query, including web search, live lookups, or reversing an id back to its origin.
> Closed or hosted model APIs for producing predictions. Predictions must come from a model you run yourself so results stay reproducible and tied to what your model learned.
> Any attempt to reverse or de-anonymise a query or gallery id back to its original recording, or to match a query id to its gallery id by any means other than the audio.
> Hand-matched answers for individual queries produced by listening to the fragments yourself. Sourcing the target by any of these routes is data leakage and invalidates the submission.
> Compute Budget
> Your solution must train and produce its submission within the following limits.
> Resource   Limit
> --------------------------------------------------------------
> CPU        10 cores
> RAM        62.5 GB
> Runtime    90 minutes, end to end, training plus inference
> GPU        none
> The dataset is small: 490 query and 490 gallery fragments, together under twelve minutes of audio. A contrastive embedding network trains in minutes on CPU and ranks the full gallery for all 490 queries well inside the budget. The runtime limit is not the binding constraint; learning an embedding that separates same-emotion knocks is.

Inspiration note: Useful as inspiration for route/path reconstruction outputs with explicit evidence structure.
## Repeated Air-Stroke Sequence Surgery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70h7yg5kfqsvw0xj6fj8p7ax8aqzqq
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, Dataset source is visible after the challenge closes.
- Best/top context: Be the first to climb the leaderboard!

### Full Challenge Description

> Overview
> Each case contains two real recordings of the same air-written character class. The first is an intact reference performance. The second has either been left intact or altered by a temporal or sensor-channel edit. Predict the inverse repair program, align eight coarse stroke regions between the performances, and classify the edit family.
> The input is an NPZ packet with two arrays named reference and corrupted. Both arrays have 192 time rows and six motion channels. The signals come from real finger-mounted inertial recordings made under distinct source recording IDs, so the two sequences share a character shape but are not duplicate waveforms. Temporal edits act on four consecutive 48-row quarters. Channel edits exchange or invert sensor columns.
> This models recovery of a damaged gesture packet when a second physical performance is available as a witness. Exact sample matching is impossible because people do not reproduce a motion identically. A successful system must separate ordinary cross-trial variation from an introduced sequence operation, then align the underlying stroke progression. The primary output is a repair program, not a gesture class.
> The challenge runs on CPU. Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> Dataset
> The prepared dataset contains 2,189 training cases and 561 test cases. Numeric source recording IDs are partitioned before pairing, so no source recording contributes to both splits. Within each character class, two IDs from the same partition form one case. Public packet paths and case IDs are opaque.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Input columns and labels for the source-disjoint training set. |
> | `test.csv` | Input columns for the source-disjoint test set. |
> | `sample_submission.csv` | Required submission columns in their exact order. |
> | `packets/*.npz` | Compressed two-array motion packets. |
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque unique case identifier. |
> | `motion_packet_path` | relative path string | Location of the NPZ packet under the prepared dataset root. |
> | `repair_contract` | string | Defines the array names, the 192-row timeline, the four quarter boundaries, and the requirement to repair before sealing. |
> NPZ Arrays
> | Array | Data type | Shape | Description |
> |---|---|---:|---|
> | `reference` | float16 matrix | 192 by 6 | Intact first performance after robust scaling and resampling. |
> | `corrupted` | float16 matrix | 192 by 6 | Second real performance after any controlled packet edit. |
> Channels c1 through c3 are angular-velocity channels. Channels c4 through c6 are acceleration channels. Timeline quarters are q1 rows 0 to 47, q2 rows 48 to 95, q3 rows 96 to 143, and q4 rows 144 to 191.
> Target Columns
> | Column | Data type | Description |
> |---|---|---|
> | `stroke_repair_program` | ordered token string | Zero, one, or two inverse edit operations in execution order. |
> | `cross_trial_alignment_graph` | canonical edge-set string | Eight reference-to-witness region links using tokens `aN:bM`. |
> | `trace_disposition` | categorical string | `unaltered`, `temporal_edit`, `channel_edit`, or `compound_edit`. |
> Disposition Distribution
> | Disposition | Train | Test |
> |---|---:|---:|
> | `channel_edit` | 694 | 180 |
> | `compound_edit` | 628 | 165 |
> | `temporal_edit` | 653 | 152 |
> | `unaltered` | 214 | 64 |
> Repair Program Vocabulary
> An unchanged packet uses accept:unaltered. Edited packets end with seal:stroke and use one or two of these operations:
> | Token | Action |
> |---|---|
> | `reverse:qN` | Reverse timeline quarter `qN`. |
> | `swap:qN:qM` | Exchange two distinct quarters. IDs appear in ascending order. |
> | `swap:cN:cM` | Exchange two distinct channels. IDs appear in ascending order. |
> | `invert:cN` | Multiply channel `cN` by `-1`. |
> Operations are listed in the order in which the corrupted packet must be repaired. Examples:
> reverse:q3>seal:stroke
> swap:c2:c5>swap:q1:q4>seal:stroke
> Alignment Graph
> Both repetitions are divided into eight coarse regions, a1 through a8 for the reference and b1 through b8 for the repaired witness. The target contains one edge for every reference region. Edges are unique, sorted, and separated by |.
> a1:b1|a2:b2|a3:b3|a4:b4|a5:b5|a6:b6|a7:b7|a8:b8
> The mapping need not be diagonal because the two physical performances can speed up or slow down at different points.
> Example Input
> case_id,motion_packet_path,repair_contract
> 46a6c692c349cb8223111bd9,packets/9effcb8b591ab1b47a1ccd20230dd158.npz,"The NPZ arrays reference and corrupted each have 192 time rows and six channels. Quarters q1 to q4 are consecutive 48-row spans. Recover the corrupted witness before sealing the stroke."
> Example Label
> case_id,stroke_repair_program,cross_trial_alignment_graph,trace_disposition
> 46a6c692c349cb8223111bd9,reverse:q2>seal:stroke,a1:b1|a2:b2|a3:b2|a4:b2|a5:b2|a6:b2|a7:b6|a8:b8,temporal_edit
> Submission Format
> Write predictions to ./working/submission.csv with exactly these columns in this order:
> case_id,stroke_repair_program,cross_trial_alignment_graph,trace_disposition
> Extra or reordered columns, duplicate IDs, missing IDs, unknown IDs, and row-count mismatches are rejected. One backend-added visibility column is ignored. Repair programs are limited to 130 characters and at most three tokens including the seal token. Graphs are limited to 100 characters and at most eight edges.
> Nontrivial valid row:
> case_id,stroke_repair_program,cross_trial_alignment_graph,trace_disposition
> 46a6c692c349cb8223111bd9,reverse:q2>seal:stroke,a1:b1|a2:b2|a3:b2|a4:b2|a5:b2|a6:b2|a7:b6|a8:b8,temporal_edit
> Evaluation
> The metric is Stroke Surgery Integrity Score:
> base_row_score =
> 0.50 * RepairProgramScore
> + 0.32 * AlignmentGraphScore
> + 0.18 * DispositionScore
> row_score = base_row_score              if program family and disposition agree
> row_score = 0.90 * base_row_score       otherwise
> Score = mean(row_score over test cases)
> RepairProgramScore
> Programs are parsed as token sequences. Token-level Levenshtein distance is the minimum number of token insertions, deletions, and substitutions required to transform one sequence into the other.
> similarity = 1 - edit_distance(true_tokens, predicted_tokens)
> / max(len(true_tokens), len(predicted_tokens), 1)
> exact = 1 if both token sequences are identical, else 0
> RepairProgramScore = 0.18 * similarity + 0.82 * exact
> Malformed programs score 0.
> AlignmentGraphScore
> Let Y and P be the true and predicted edge sets:
> set_F1 = 2 * |Y intersect P| / (|Y| + |P|)
> exact = 1 if Y equals P, else 0
> AlignmentGraphScore = 0.30 * set_F1 + 0.70 * exact
> Malformed graphs score 0.
> DispositionScore
> This component is exact categorical accuracy. It is 1 for the correct valid disposition and 0 otherwise.
> What Makes This Interesting
> The reference is not a clean copy of the damaged sequence. It is another real performance of the same character class with its own speed, amplitude, and writer variation. A solver must infer a reversible packet edit while also recovering a coarse nonlinear alignment between naturally different motions.
> Method Requirements
> CPU-compatible temporal convolutions, compact recurrent models, dynamic-time-warping features, contrastive encoders, and constrained sequence decoders are allowed. All fitting and threshold selection must use public training data only.
> What Not To Use
> Do not recover gesture classes or source recording numbers through external mirrors or source filenames.
> Do not use case_id, packet path, row order, compressed size, timestamps, or storage metadata as target features.
> Do not adapt parameters, select thresholds, or construct labeled retrieval entries from test packets.
> Do not exploit parser limits, malformed fields, duplicate IDs, missing rows, extra columns, or grader behavior.
> Do not call hosted closed-model APIs at inference time.

Inspiration note: Useful as inspiration for route/path reconstruction outputs with explicit evidence structure.
## Local-Fight Move-Order Recovery In Go

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cv178rxz4fyht6gbyw1cehd8atcqt
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image, Dataset source is visible after the challenge closes.
- Best/top context: Beat usamaasif's score of 0.656!

### Full Challenge Description

> Task
> You are given the state of a single localized fight on a Go board at the moment the fight begins, together with the unordered set of stones that were played inside that region during the fight. For each of the two sides, recover the chronological order in which that side's stones were played.
> Move order inside a Go fight is driven by the shape of the position — which group is under attack, which move is forcing, the vital point of a shape, whether a stone is a contact play or the reply to one. Recovering the order requires reading the board, not reading off a simple statistic. Each side played at least 4 stones in the region.
> These fights are selected so that the play order is tactically forced: they are dominated by driving sequences, ataris and their replies, capturing races (semeai) and ladders, where each side's stones were played in a determined order that follows from how the fight develops. This means the order is genuinely recoverable by reading the fight — but a blind proximity, recency, or liberty-count heuristic will not recover it, because the order comes from the tactical relationships between the moves, not from any one per-move statistic.
> Each board has been randomly reflected/rotated (one of 8 symmetries) and the two sides' labels randomly swapped, independently per fight, so there is no absolute orientation or color to rely on, and no move numbers or timestamps are given.
> Files
> All files are CSV. Boards are shared by two small tables keyed by fight_id; moves are listed one per row.
> train_boards.csv
> The board at the start of each training fight. Columns:
> fight_id — string. Identifier of the fight.
> board — string of exactly 225 characters, the 15x15 board in row-major order (row 0 first, 15 characters per row). Each character is one of: . an empty point, A a stone of side A, B a stone of side B, # a point off the edge of the board (the region overhangs the board edge).
> train.csv
> One row per stone played during each training fight, WITH its true order. Columns:
> id — string. Unique identifier of this move row.
> fight_id — string. The fight this move belongs to (join to train_boards.csv).
> side — string, either A or B. Which side played the stone.
> r — integer in 0..14. Row of the stone in the 15x15 board.
> c — integer in 0..14. Column of the stone in the 15x15 board.
> order — integer, 0-based. The stone's chronological rank WITHIN its own side (0 = that side's first stone in the region, 1 = its second, and so on).
> test_boards.csv
> The board at the start of each test fight. Same two columns as train_boards.csv:
> fight_id — string.
> board — string of 225 characters (same encoding as above).
> test.csv
> One row per stone played during each test fight, WITHOUT the order (that is what you predict). Columns:
> id — string. Unique identifier of this move row (use it in your submission).
> fight_id — string. The fight this move belongs to (join to test_boards.csv).
> side — string, A or B.
> r — integer in 0..14.
> c — integer in 0..14.
> sample_submission.csv
> A valid submission with a constant score, to fix the format. Columns:
> id — string. Matches every id in test.csv exactly once.
> play_order_score — float. The predicted play-order score for that move.
> Submission format
> Produce submission.csv with exactly the columns id and play_order_score, one row for every id in test.csv (each exactly once). play_order_score is a real number; for each fight and side, moves are ranked by DESCENDING play_order_score to form your predicted play order, so a HIGHER score means the stone was played EARLIER. Ties are allowed but earn no credit for the tied pair.
> Evaluation
> Metric: mean within-side Kendall tau-b. For each test fight and each side, your predicted order (from play_order_score) is compared to the true order using Kendall's tau-b; the two sides are averaged, then averaged over all fights. The reported score is this value clipped to the range 0.01 to 1.0 — higher is better. A random or constant submission scores approximately 0; a perfect ordering scores 1.0.

Inspiration note: Useful for ordered trace reconstruction instead of isolated per-item prediction.
## Seismic Evidence Forensics

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7e1rwqzm46q7bzt9xfwhpawd8b020z
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: multimodal, Dataset source is visible after the challenge closes.
- Best/top context: Be the first to climb the leaderboard!

### Full Challenge Description

> Overview
> You are given three forms of evidence for an anonymized seismic path:
> an ambient-noise cross-correlation waveform;
> a two-dimensional dispersion-energy image;
> a proposed period-by-period phase-velocity curve with a validity claim.
> Seismic stations continuously record vibrations from oceans, weather, and human activity. By
> cross-correlating this ambient noise between two stations, seismologists recover a virtual wave
> response that contains coherent surface-wave arrivals. Because Rayleigh waves of different periods
> sample different depths, their phase velocity as a function of period helps reveal subsurface
> structure.
> A dispersion-energy image shows candidate surface-wave energy across velocity and period. A valid
> dispersion curve should follow a physically supported ridge in that image and agree with the travel
> information in the cross-correlation waveform. The three released modalities are therefore
> different measurements of the same underlying propagation behavior.
> The evidence should describe the same wave propagation path. However, a case may contain a corrupted
> waveform, a corrupted dispersion image, a corrupted curve claim, or no corruption at all. When
> corruption is present, it affects a physically meaningful part of the evidence and may be subtle
> enough to remain visually plausible.
> For every case, audit the three evidence sources, identify which source is inconsistent, localize
> the affected period range, and reconstruct the supported phase-velocity curve.
> This is a scientific evidence-forensics problem, not ordinary dispersion picking. A model cannot
> solve the complete task by reading only one modality. It must compare a time-domain signal, a
> time-frequency representation, and a structured physical claim; determine whether they agree; and
> repair the claim when they do not.
> Station names, station coordinates, geographic metadata, source identifiers, and original path keys
> are not released.
> What the task requires
> Solving an item well exercises five related capabilities:
> Cross-modal seismic representation: learn comparable physical structure from a waveform, a
> dispersion image, and a proposed velocity curve.
> Evidence consistency reasoning: determine whether all modalities describe the same propagation
> path rather than treating each input independently.
> Forensic classification: distinguish a clean case from waveform, image, or curve-claim
> corruption.
> Period localization: identify the part of the 2-to-50-second period range affected by the
> inconsistency.
> Structured repair and calibration: reconstruct a coherent 49-point velocity curve and estimate
> where that reconstruction is supported by valid evidence.
> Source and provenance
> The underlying observations come from the SeisDispFusion-NCF collection. It organizes real seismic
> noise cross-correlation functions, two-dimensional dispersion representations, phase-velocity
> curves, and validity masks by station pair. The platform source is a compact Apache-2.0-derived
> archive containing only the selected waveforms, common-grid images, curves, masks, and shared axes
> required to reproduce this challenge.
> Challenge cases are derived after source stations have been assigned to one side of the train/test
> split. Each released case combines several compatible observations from that side into one derived
> path before any local inconsistency is introduced. The supported curve is derived from the same
> private combination rather than copied from one catalog row. Train and test have disjoint station
> sets, so no station or station pair can contribute to both sides.
> The released inputs are transformed challenge representations rather than unchanged source files.
> Original station identifiers, coordinates, filenames, pair ordering, combination members, and
> acquisition metadata are kept private.
> The source dataset is distributed under the Apache License 2.0. Users must follow its attribution
> and usage requirements. The challenge files are intended for machine-learning and geophysical
> research.
> File Structure
> train.csv - training identifiers, array indices, proposed curve evidence, and all targets.
> test.csv - test identifiers, array indices, and proposed curve evidence, without targets.
> train_waveforms.npy - training waveform matrix.
> test_waveforms.npy - test waveform matrix.
> train_dispersion_images.npy - training dispersion-image tensor.
> test_dispersion_images.npy - test dispersion-image tensor.
> periods.npy - the shared 49-value period axis in seconds.
> velocity_axis.npy - the shared 128-value image velocity axis in km/s.
> sample_submission.csv - a correctly formatted submission with varied baseline predictions.
> The waveform matrices have shape (number_of_examples, 1536). The dispersion-image tensors have
> shape (number_of_examples, 128, 49), with velocity on axis 1 and period on axis 2. Arrays are stored
> compactly as float16; convert them to float32 during training when appropriate.
> The row selected by waveform_index and image_index is the corresponding input for that CSV row.
> For example, a training item with both indices equal to 17 uses train_waveforms.npy[17] and
> train_dispersion_images.npy[17].
> Features
> train.csv and test.csv contain:
> id (string) - an opaque unique example identifier.
> waveform_index (integer) - row index into the waveform matrix for the corresponding split.
> image_index (integer) - row index into the dispersion-image tensor for the corresponding split.
> claim_vel_02 through claim_vel_50 - the proposed phase-velocity curve in km/s.
> claim_valid_02 through claim_valid_50 - the proposed validity values associated with the
> curve claim.
> The waveform is a robust-normalized ambient-noise correlation signal. The image is a normalized
> dispersion-energy representation with period along one axis and velocity along the other. The exact
> axes are provided in periods.npy and velocity_axis.npy.
> The proposed curve is evidence, not an answer. It can be fully consistent, partially inconsistent,
> or associated with another corrupted modality. A solution must evaluate it against the waveform and
> image.
> Targets
> train.csv additionally contains four groups of targets.
> Fault-type targets:
> fault_clean - 1 when all evidence is consistent.
> fault_waveform - 1 when the waveform is the inconsistent evidence source.
> fault_image - 1 when the dispersion image is the inconsistent evidence source.
> fault_claim - 1 when the proposed curve claim is inconsistent.
> Exactly one fault-type target is active for each training case. At submission time, these four
> columns contain predicted probabilities.
> Affected-period targets:
> affected_02 through affected_50 - binary indicators for periods affected by the inconsistency.
> All affected-period targets are 0 for a clean case. Submission values are probabilities in [0, 1].
> Repair targets:
> repair_vel_02 through repair_vel_50 - the supported phase-velocity curve in km/s.
> Trust targets:
> trust_02 through trust_50 - binary indicators showing where the repaired velocity is supported
> by a valid source observation.
> Submission values for the trust targets are probabilities. Velocity predictions are clipped to
> [1.0, 5.0] km/s, while all probability outputs are clipped to [0.0, 1.0].
> Evaluation
> The score combines curve-repair skill, diagnostic Brier skill, and a cross-sample variance check.
> All errors are aggregated over the complete test corpus. The exact calculation is defined below.
> In every formula, clip(x, a, b) means min(max(x, a), b).
> Prediction preprocessing
> Fault values are replaced by 0.25 when non-finite, clipped to [0, 1], and normalized across the
> four fault columns for each row. A row whose clipped values sum to zero becomes [0.25, 0.25, 0.25,
> 0.25].
> Affected-period and trust values are replaced by 0.5 when non-finite and clipped to [0, 1].
> Repaired velocities are replaced by 3.4 when non-finite and clipped to [1.0, 5.0] km/s.
> Period weights and private climatology
> For every integer period p from 2 through 50, define the public period weight:
> w_p = sqrt(p / 2)
> Let y_ip be the private repaired velocity for case i and period p, and let m_ip be its private binary
> trust target. The optimal trusted period-wise constant is:
> c_p = sum_i(m_ip * y_ip) / sum_i(m_ip)
> If a period has no trusted private observation, c_p is defined as 3.4. All protected divisions in
> the grader use a minimum denominator of 1e-12.
> Global repair skill
> For submitted repaired velocity r_ip, compute:
> E_global = sum_i sum_p(w_p *m_ip* (r_ip - y_ip)^2) B_global = sum_i sum_p(w_p *m_ip* (c_p - y_ip)^2) S_global = clip(1 - E_global / B_global, 0, 1)
> Hard claim-repair skill
> Let q_i equal 1 when the private fault target is fault_claim and 0 otherwise. Let a_ip be the private
> binary affected-period target. Define the hard-region mask:
> h_ip = m_ip *a_ip* q_i
> The same period climatology c_p is used for this region:
> E_hard = sum_i sum_p(w_p *h_ip* (r_ip - y_ip)^2) B_hard = sum_i sum_p(w_p *h_ip* (c_p - y_ip)^2) S_hard = clip(1 - E_hard / B_hard, 0, 1)
> The repair component is:
> repair_skill = 0.55 *S_global + 0.45* S_hard
> This hard-region term prevents a copied claim from receiving useful repair skill when the claim is
> the corrupted modality.
> Diagnostic Brier skills
> The same Brier-skill calculation is applied separately to fault type, affected periods, and trust.
> For any target matrix z_ij, prediction matrix x_ij, and public column weights u_j, first compute each
> private test-column prevalence:
> prevalence_j = (1 / N) * sum_i(z_ij)
> Then compute:
> E_brier = sum_i sum_j(u_j * (x_ij - z_ij)^2) B_brier = sum_i sum_j(u_j * (prevalence_j - z_ij)^2) S_brier = clip(1 - E_brier / B_brier, 0, 1)
> For fault type, the four column weights are all 1. For affected periods and trust, the column weight
> for period p is w_p = sqrt(p / 2). This produces S_fault, S_affected, and S_trust. If a Brier
> baseline denominator is zero, its skill is 1 only when prediction error is also zero; otherwise it
> is 0.
> The diagnostic multiplier is:
> diagnostic_factor = 0.70 + 0.10 *S_fault + 0.10* S_affected + 0.10 * S_trust
> Cross-sample variance factor
> Normalize submitted and private repaired velocities to the [0, 1] scale:
> R_ip = (r_ip - 1.0) / 4.0 Y_ip = (y_ip - 1.0) / 4.0
> For each period, take the population standard deviation across test cases, then average across all
> 49 periods:
> spread_prediction = mean_p(std_i(R_ip)) spread_truth = mean_p(std_i(Y_ip)) spread_fraction = spread_prediction / max(spread_truth, 1e-12) variance_factor = clip(0.70 + 0.30 * spread_fraction / 0.50, 0.70, 1.0)
> This term penalizes assigning one average repaired curve to every case. A single internally varied
> curve copied to every row has zero cross-sample spread and does not bypass the term.
> Final score
> raw_score = repair_skill *diagnostic_factor* variance_factor score = clip(raw_score, 0.001, 1.0)
> Higher is better. A constant-climatology repair is at the floor by construction, while an exact
> copy of every private target scores 1.0. Missing ids, duplicate ids, missing required columns, or an
> empty submission receive the 0.001 floor.
> Submission
> Submit a CSV containing id followed by the 151 prediction columns shown in the complete header
> below. The file therefore has 152 columns in total.
> Provide exactly one row for every id in test.csv. All target columns must contain numeric
> predictions. Column names are case-sensitive.
> Complete illustrative header and row:
> id,fault_clean,fault_waveform,fault_image,fault_claim,affected_02,affected_03,affected_04,affected_05,affected_06,affected_07,affected_08,affected_09,affected_10,affected_11,affected_12,affected_13,affected_14,affected_15,affected_16,affected_17,affected_18,affected_19,affected_20,affected_21,affected_22,affected_23,affected_24,affected_25,affected_26,affected_27,affected_28,affected_29,affected_30,affected_31,affected_32,affected_33,affected_34,affected_35,affected_36,affected_37,affected_38,affected_39,affected_40,affected_41,affected_42,affected_43,affected_44,affected_45,affected_46,affected_47,affected_48,affected_49,affected_50,repair_vel_02,repair_vel_03,repair_vel_04,repair_vel_05,repair_vel_06,repair_vel_07,repair_vel_08,repair_vel_09,repair_vel_10,repair_vel_11,repair_vel_12,repair_vel_13,repair_vel_14,repair_vel_15,repair_vel_16,repair_vel_17,repair_vel_18,repair_vel_19,repair_vel_20,repair_vel_21,repair_vel_22,repair_vel_23,repair_vel_24,repair_vel_25,repair_vel_26,repair_vel_27,repair_vel_28,repair_vel_29,repair_vel_30,repair_vel_31,repair_vel_32,repair_vel_33,repair_vel_34,repair_vel_35,repair_vel_36,repair_vel_37,repair_vel_38,repair_vel_39,repair_vel_40,repair_vel_41,repair_vel_42,repair_vel_43,repair_vel_44,repair_vel_45,repair_vel_46,repair_vel_47,repair_vel_48,repair_vel_49,repair_vel_50,trust_02,trust_03,trust_04,trust_05,trust_06,trust_07,trust_08,trust_09,trust_10,trust_11,trust_12,trust_13,trust_14,trust_15,trust_16,trust_17,trust_18,trust_19,trust_20,trust_21,trust_22,trust_23,trust_24,trust_25,trust_26,trust_27,trust_28,trust_29,trust_30,trust_31,trust_32,trust_33,trust_34,trust_35,trust_36,trust_37,trust_38,trust_39,trust_40,trust_41,trust_42,trust_43,trust_44,trust_45,trust_46,trust_47,trust_48,trust_49,trust_50 ef_0123abcdef456789abcd,0.25,0.25,0.25,0.25,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,3.40,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50,0.50
> The row above is a formatting example. Replace the illustrative id with an id from test.csv and
> provide one complete row for every test id.
> Write the final submission to ./working/submission.csv.
> What Not To Use
> Do not solve only standard waveform-to-dispersion regression. The task requires auditing agreement
> among all three released evidence sources.
> Do not assume every case is corrupted. Clean cases are part of the task.
> Do not use filenames, identifiers, row order, waveform indices, or image indices as predictive
> features. They are array lookup fields and carry no intended target information.
> Do not attempt to recover source station pairs, coordinates, source path keys, original files, or
> private targets through public-dataset fingerprinting or external catalog lookup.
> Do not search for superficial editing boundaries, compression differences, or array-storage
> artifacts. The intended evidence is physical disagreement across waveform, image, and curve.
> Do not use manually entered answers, hidden test labels, source lookup tables, or statistics
> computed jointly from public and private data.
> Do not infer privileged predictions from sample_submission.csv. It is a varied formatting example
> based only on training-set statistics.
> Expected Output
> For every test case, return calibrated probabilities for the evidence state, a probabilistic map of
> the affected period range, a repaired 49-point phase-velocity curve, and a 49-point trust map.
> Successful solutions should explain cross-modal physical consistency and repair sample-specific
> seismic evidence rather than merely reproduce the proposed curve or regress to an average path.

Inspiration note: Useful for ordered route/workflow reconstruction outputs with explicit consistency constraints.
## Central European Pretraining Curriculum

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74c9sj6fkvmehkgmk4qhkmn98ax7cq
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Beat backprop's score of 0.401!

### Full Challenge Description

> Central European Pretraining Curriculum
> Overview
> This is a CPU-only language-model curriculum-design challenge. You are given 4,500 parliamentary speech segments in Czech, Hungarian, Polish, and Slovak. Your job is to choose exactly 1,024 segments and arrange them into four ordered training stages.
> In plain terms, you are designing what a small language model reads first, second, third, and last. A good curriculum must establish all four languages early, cover uncommon policy language, transfer across related and unrelated languages, and avoid forgetting a smaller language by the final stage.
> Your submission is one global curriculum artifact, not one prediction per speech. The private grader trains the same fixed byte-level language model for every submission. Only the selected segment IDs and their stage order change.
> The public corpus is derived from parliamentary proceedings from Czechia, Hungary, Poland, and Slovakia. Records are grouped by country and sitting date before the public/private source split. Private evaluation passages are new mosaics made only from held-out source groups, so no public training segment is reused as a private test passage.
> Files
> train.csv is the public candidate pool. It contains:
> id: string. Anonymous candidate-segment ID.
> language: string. One of cz, hu, pl, or sk.
> language_name: string. Czech, Hungarian, Polish, or Slovak.
> language_family: string. Slavic or Uralic.
> country: string. Country represented by the parliamentary speech.
> topic_tag: string. Row-local public policy-topic tag.
> topic_label: string. Human-readable policy-topic description.
> source_group: string. Anonymous country-and-sitting-date group. Use this for group-aware local validation.
> text: string. UTF-8 parliamentary speech segment available for curriculum training.
> utf8_bytes: integer. Byte length of text before the grader's 640-byte truncation.
> test.csv contains 16 replicas of the same artifact request. It contains:
> id: string. Artifact-row ID from A000 through A015.
> artifact_type: string. Always four_stage_pretraining_curriculum.
> stages: integer. Always 4.
> items_per_stage: integer. Always 256.
> Artifact replication allows the platform to evaluate complete global artifacts after leaderboard partitioning. Submit the same best curriculum in all 16 rows. Different valid curricula are scored independently and averaged.
> sample_submission.csv contains:
> id: string. Artifact-row ID.
> predicted_curriculum: string. A complete JSON curriculum artifact. The provided artifact is valid but deliberately uninformative and scores 0.
> Curriculum format
> predicted_curriculum must be a JSON object with exactly one key, stages. Its value must be a list of exactly four stage objects in this exact order:
> foundation
> policy_breadth
> cross_language
> robust_finish
> Every stage object must contain exactly two keys:
> name: string. The required stage name.
> ids: list of exactly 256 unique candidate IDs from train.csv.
> IDs may not be reused within a stage or across stages. The complete curriculum therefore contains exactly 1,024 distinct public candidate IDs.
> Assignment to a stage matters. Order among IDs inside the same stage does not affect the score because all count updates within a stage are additive and decay occurs only between stages.
> Abbreviated schema illustration only:
> {"stages":[
> {"name":"foundation","ids":["candidate_id_1","... 255 more ..."]},
> {"name":"policy_breadth","ids":["candidate_id_257","... 255 more ..."]},
> {"name":"cross_language","ids":["candidate_id_513","... 255 more ..."]},
> {"name":"robust_finish","ids":["candidate_id_769","... 255 more ..."]}
> ]}
> The ellipses above are explanatory placeholders and are not valid submission values. See sample_submission.csv for a complete machine-valid artifact.
> Fixed training procedure
> The grader uses a fixed online byte n-gram language model. This makes the submitted curriculum executable and keeps evaluation feasible on CPU.
> For every selected segment:
> Encode text as UTF-8.
> Keep at most the first 640 bytes.
> Update byte counts for context orders 0, 1, 2, and 3.
> Use three beginning-of-sequence symbols before the first byte.
> Before stages 2, 3, and 4, every existing count is multiplied by 0.82. Thus, later stages have greater influence and a poor final stage can cause forgetting.
> For a next byte b and an order-n context, where n is 0, 1, 2, or 3:
> p_n(b) = (count(context_n, b) + 0.20)
> / (count(context_n) + 256 * 0.20)
> The final byte probability is:
> p(b) = 0.08 * p_0(b)
> + 0.12 * p_1(b)
> + 0.25 * p_2(b)
> + 0.55 * p_3(b)
> Evaluation loss is mean negative log base 2 probability per UTF-8 byte:
> loss = mean(-log2(p(true_next_byte)))
> Private evaluation sets
> The model is evaluated at four checkpoints:
> After foundation: 80 held-out source-new mosaics for each of the four languages.
> After policy_breadth: 160 held-out mosaics emphasizing policy topics that are uncommon in the public pool.
> After cross_language: 160 held-out passages joining material from two different languages.
> After robust_finish: the four monolingual sets are measured again to test final quality and language retention.
> Evaluation source groups are disjoint from public source groups. Exact public training texts are rejected during private evaluation construction.
> Evaluation metric
> The grader compares every measured loss with two fixed private curricula:
> anchor_loss: loss from a straightforward pooled, language-imbalanced curriculum.
> reference_loss: loss from a private balanced, diversity-aware reference curriculum.
> Lower language-model loss is better. For any measured loss:
> ClosedGap = clip(
> (anchor_loss - measured_loss)
> / (anchor_loss - reference_loss),
> 0,
> 1
> )
> StrictScore = pow(ClosedGap, 6)
> A result at or worse than the anchor receives 0. Matching or beating the reference receives 1. The sixth power deliberately keeps the weak pooled and merely stratified baselines near the bottom of the scale while preserving smooth credit for curricula that approach the reference.
> The five scored components are:
> FoundationMacro: mean StrictScore across Czech, Hungarian, Polish, and Slovak after stage 1.
> PolicyBreadth: StrictScore on the policy-tail set after stage 2.
> CrossLanguage: StrictScore on the bilingual set after stage 3.
> FinalWorstLanguage: minimum of the four monolingual StrictScores after stage 4.
> FinalMacro: mean of the four monolingual StrictScores after stage 4.
> The artifact score is:
> artifact_score =
> 0.25 * FoundationMacro
> + 0.20 * PolicyBreadth
> + 0.20 * CrossLanguage
> + 0.25 * FinalWorstLanguage
> + 0.10 * FinalMacro
> The grader returns the arithmetic mean of the artifact scores present in the platform-provided answer partition. An empty platform-generated partition returns 0 without crashing.
> Scores are finite and bounded in [0, 1]. The sample scores 0. The private reference curriculum scores 1. Participants can reproduce the training algorithm on public text, but cannot reproduce private losses without the held-out evaluation corpus.
> Invalid artifacts
> A row receives 0 if its JSON is malformed, has auxiliary keys, has the wrong stage names or order, uses an unknown candidate ID, contains anything other than 256 IDs per stage, or reuses an ID.
> The submission file is rejected if it has missing or extra columns, missing IDs, duplicate IDs, unknown IDs, missing rows, or the wrong column order.
> Submission format
> Submit a CSV with exactly these two columns in this order:
> id: string. Artifact-row ID from test.csv.
> predicted_curriculum: string. Complete JSON curriculum artifact.
> A schematic CSV row is shown below. The actual JSON must contain all four complete 256-ID stages.
> id,predicted_curriculum
> A000,"{""stages"":[{""name"":""foundation"",""ids"":[""id1"",""...""]}, ...]}"
> Use normal CSV quote escaping, exactly as demonstrated by sample_submission.csv.
> What not to use
> Do not treat the 16 test rows as different language tasks. They are replicas of one artifact request.
> Do not submit row classifications, natural-language explanations, model weights, Python code, or a list of texts.
> Do not reuse a candidate ID, invent IDs, add JSON keys, rename stages, or change stage order.
> Do not optimize only Polish or Czech. FinalWorstLanguage makes language starvation costly.
> Do not ignore stage order. Count decay makes the same selected set behave differently under a different schedule.
> Do not key decisions to candidate IDs, CSV order, or source-group hashes; those values carry no curriculum target.
> Do not expect public-source lookup to reveal private evaluation passages or reference losses.
> Resource limit
> Solutions have 90 minutes, 10 CPU cores, and 62 GB RAM. No GPU is required or expected.
> Benchmark boundary
> Existing data-selection benchmarks usually ask for a static subset, compare full neural pretraining runs, or study curriculum policies inside a specific translation or language-model system. This task instead asks for a complete ordered four-stage corpus artifact under a fixed global budget. The scorer executes that artifact in an online model, measures intermediate learning, cross-language transfer, rare-policy coverage, final retention, and worst-language robustness. It is neither text classification, regression, next-token prediction, ordinary active learning, nor a renamed tokenizer-design task.

Inspiration note: Useful for ordered route/workflow reconstruction outputs with explicit consistency constraints.
## Musical Instrument Replacement Compatibility Scoring

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx711qyfnasrp580tywjysecy18arz16
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: audio, text, Dataset source is visible after the challenge closes.
- Best/top context: Be the first to climb the leaderboard!

### Full Challenge Description

> Overview
> For each case, predict a four-candidate substitution decision for one missing orchestral note. The required outputs are a 4 by 4 compatibility matrix, a ranked order of the four candidates, a set of violated musical constraints, and a compact substitution program for the selected candidate.
> Each input contains one reference WAV file, four candidate WAV files, and a short contract that states which musical property matters most. The recordings are isolated monophonic orchestral notes. The hidden metadata used to build the labels contains instrument family, instrument identity, pitch ID, and dynamic ID. Participants do not receive those metadata fields directly, so the task must be solved from the audio plus the contract.
> This models an arrangement and sample-library workflow. If a requested note is unavailable, a system must choose a substitute, explain which properties changed, and produce a small action record that a downstream arranger could review. The same candidate can be acceptable under one contract and poor under another because the contract changes the relative importance of register, timbre, identity, and loudness.
> The challenge is CPU compatible. Submissions are scored from 0.0 to 1.0, where higher is better.
> Dataset
> The prepared dataset contains 2,330 labeled training cases and 583 held-out test cases. The split is grouped by source recording fold so that test reference recordings do not appear as training references. Public audio files are converted to mono 22,050 Hz PCM WAV and receive a small deterministic time-scale, gain, and dither transformation so file bytes do not match the original recordings.
> The source audio consists of studio-recorded single notes from orchestral instruments. Every public case presents a reference note and four candidate notes. Candidate IDs are local to the row and are always c1, c2, c3, and c4 in the order listed in candidate_audio_paths.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Public input columns plus all target columns for labeled training cases. |
> | `test.csv` | Public input columns only for held-out cases. |
> | `sample_submission.csv` | Example submission file with the exact required schema. |
> | `audio/*.wav` | Opaque WAV recordings used by the reference and candidate path columns. |
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque unique case identifier. It is not meaningful and should not be decoded. |
> | `reference_audio_path` | path string | Relative path to the WAV file containing the unavailable or target reference note. |
> | `candidate_audio_paths` | JSON array string | Four relative WAV paths in candidate order. The first path is candidate `c1`, the second is `c2`, and so on. |
> | `substitution_contract` | string | Natural-language contract that prioritizes one property: register, timbral family, exact instrumental voice, or dynamic behavior. Some contracts use arranger-facing wording such as articulation for the exact-voice requirement. |
> Metadata Semantics Used For Labels
> These metadata concepts are not public columns, but they define the targets:
> | Concept | Meaning |
> |---|---|
> | `instrument family` | Broad orchestral group such as strings, brass, winds, or keyboard. |
> | `instrument identity` | The specific instrument within its family, such as flute, oboe, violin, trumpet, or accordion. This is the scored exact-voice column, even when the contract text describes the requirement as articulation. |
> | `pitch ID` | Integer pitch index used to measure register distance between notes. Smaller gaps mean closer register. |
> | `dynamic ID` | Ordinal loudness marking used to measure dynamic mismatch. Larger gaps mean the candidate differs more in recorded loudness. |
> Target Columns
> | Column | Data type | Description |
> |---|---|---|
> | `compatibility_matrix` | JSON integer matrix | Shape 4 by 4. Rows correspond to `c1` through `c4`. Columns are `pitch`, `family`, `instrument`, and `dynamic`, in that order. |
> | `replacement_order` | ordered token string | Candidate ranking from best to worst, using `>` as the separator, followed by `seal:ranking`. Example: `c2>c1>c4>c3>seal:ranking`. |
> | `violation_set` | canonical set string | Sorted `|`-separated set of every nonzero matrix cell, or `none` if all cells are zero. Valid atoms are `cN:pitch`, `cN:family`, `cN:instrument`, and `cN:dynamic`. |
> | `substitution_program` | ordered token string | Action string for the best candidate: `choose:cN`, then zero or more adjustment tokens, then `commit:voice`. Tokens are separated by `>`. |
> Compatibility Matrix Values
> The four matrix columns use these integer penalties:
> | Matrix column | Valid values | Meaning |
> |---|---|---|
> | `pitch` | `0`, `1`, `2`, `3` | Register mismatch bucket. `0` means pitch-ID gap 0 or 1, `1` means gap 2 or 3, `2` means gap 4 or 5, and `3` means gap 6 or more. |
> | `family` | `0`, `2` | `0` means same instrument family, `2` means different family. |
> | `instrument` | `0`, `1`, `2` | `0` means same instrument, `1` means different instrument inside the same family, `2` means different family. |
> | `dynamic` | `0`, `1`, `2` | Absolute dynamic-ID gap, capped at `2`. |
> The contract converts each row of the matrix into a weighted total. Candidates are ranked by weighted total, then unweighted total, then candidate position.
> Substitution Program Vocabulary
> The program must use this grammar:
> choose:cN>[adjustments]>commit:voice
> Valid start tokens are choose:c1, choose:c2, choose:c3, and choose:c4.
> Valid adjustment tokens are:
> | Token | Meaning |
> |---|---|
> | `adjust:pitch` | The chosen candidate has a nonzero pitch penalty. |
> | `adjust:family` | The chosen candidate has a nonzero family penalty. |
> | `adjust:instrument` | The chosen candidate has a nonzero instrument penalty. |
> | `adjust:dynamic` | The chosen candidate has a nonzero dynamic penalty. |
> Adjustment tokens, when present, must appear in this order: adjust:pitch, adjust:family, adjust:instrument, adjust:dynamic. Tokens are not repeated. A perfect candidate can use choose:cN>commit:voice.
> Example Input Row
> case_id,reference_audio_path,candidate_audio_paths,substitution_contract
> 9b8fa32567655f96beeb1e79,audio/0a1337f508b3ff104e2a1f2a7b08b6.wav,"[""audio/1c46c0b243a5c7f9e09a884d662777.wav"",""audio/71be26f112a19c2e86817f3a271d98.wav"",""audio/57ff0e48f84ed187cb3f5f67b74a47.wav"",""audio/d545de0d82f9ea2afbe2293033bdc2.wav""]","Preserve register first, then timbral family, articulation, and dynamics. Rank all four candidates and compile the required adjustments for the best replacement."
> Example Labeled Row
> case_id,compatibility_matrix,replacement_order,violation_set,substitution_program
> 9b8fa32567655f96beeb1e79,"[[0,0,1,0],[1,0,0,1],[0,2,2,0],[3,2,2,2]]",c1>c2>c3>c4>seal:ranking,c1:instrument|c2:dynamic|c2:pitch|c3:family|c3:instrument|c4:dynamic|c4:family|c4:instrument|c4:pitch,choose:c1>adjust:instrument>commit:voice
> Submission Format
> Write the final submission CSV to exactly this path:
> ./working/submission.csv
> The CSV must contain exactly these columns in this order:
> case_id,compatibility_matrix,replacement_order,violation_set,substitution_program
> | Column | Required format |
> |---|---|
> | `case_id` | Existing test `case_id`, unique and nonempty. |
> | `compatibility_matrix` | JSON-encoded 4 by 4 integer matrix. Pitch column values must be 0 through 3. The other columns must be 0 through 2. |
> | `replacement_order` | Exactly four unique candidate IDs followed by `seal:ranking`, separated by `>`. |
> | `violation_set` | `none`, or sorted unique `|`-separated atoms matching `cN:pitch`, `cN:family`, `cN:instrument`, or `cN:dynamic`. |
> | `substitution_program` | `choose:cN`, zero or more valid adjustment tokens in the required order, and `commit:voice`, separated by `>`. |
> Nontrivial valid example:
> case_id,compatibility_matrix,replacement_order,violation_set,substitution_program
> 9b8fa32567655f96beeb1e79,"[[0,0,1,0],[1,0,0,1],[0,2,2,0],[3,2,2,2]]",c1>c2>c3>c4>seal:ranking,c1:instrument|c2:dynamic|c2:pitch|c3:family|c3:instrument|c4:dynamic|c4:family|c4:instrument|c4:pitch,choose:c1>adjust:instrument>commit:voice
> Extra columns, reordered columns, duplicate IDs, missing IDs, unknown IDs, and extra rows are rejected. A single backend-added visibility column is ignored. Malformed fields and overlong fields receive zero for the affected component.
> Evaluation
> The metric is Substitution Contract Integrity Score, a per-case structured score averaged over all hidden test cases.
> Score = mean(row_score over test cases)
> base_row_score =
> 0.40 * CompatibilityScore
> + 0.24 * RankingScore
> + 0.20 * ViolationScore
> + 0.16 * ProgramScore
> row_score = base_row_score if coherent else 0.92 * base_row_score
> coherent means the candidate selected by substitution_program is the same as the first candidate in replacement_order. This is an 8 percent row-level penalty applied once to the weighted row score.
> Minimum score: 0.0
> Maximum score: 1.0
> Direction: higher is better.
> CompatibilityScore
> For a true matrix Y and prediction P, both with shape 4 by 4:
> entry_accuracy = sum(I(Y[i,j] = P[i,j]) for all 16 entries) / 16
> exact_matrix_match = 1 if every entry matches, otherwise 0
> CompatibilityScore = 0.16 * entry_accuracy + 0.84 * exact_matrix_match
> Invalid matrices score 0 for this component.
> RankingScore
> Ranking strings are split on > into exactly five tokens. The edit distance is token-level Levenshtein distance.
> ranking_similarity = 1 - edit_distance(true_tokens, predicted_tokens) / 5
> exact_ranking_match = 1 if the full token sequence matches, otherwise 0
> RankingScore = 0.18 * ranking_similarity + 0.82 * exact_ranking_match
> Invalid rankings score 0 for this component.
> ViolationScore
> violation_set is parsed as a set of canonical atoms. none means an empty set.
> set_F1 = 2 * |Y intersect P| / (|Y| + |P|)
> If both sets are empty, set_F1 is 1.0. If only one set is empty, set_F1 is 0.0.
> exact_set_match = 1 if the parsed sets are identical, otherwise 0
> ViolationScore = 0.22 * set_F1 + 0.78 * exact_set_match
> Invalid sets score 0 for this component.
> ProgramScore
> Program strings are split on > into two to six tokens. The edit distance is token-level Levenshtein distance.
> program_similarity =
> 1 - edit_distance(true_tokens, predicted_tokens)
> / max(number_of_true_tokens, number_of_predicted_tokens, 1)
> exact_program_match = 1 if the full token sequence matches, otherwise 0
> ProgramScore = 0.15 * program_similarity + 0.85 * exact_program_match
> Invalid programs score 0 for this component.
> What Makes This Interesting
> The task joins acoustic perception with contract-conditioned structured reasoning. The matrix requires local judgments about pitch, timbre, instrument identity, and loudness. The ranking then applies a changing priority rule, and the program must summarize the chosen candidate without contradicting the ranking. Simple instrument recognition or pitch estimation is not enough to solve all outputs.
> Method Requirements
> CPU-compatible spectrogram encoders, compact audio transformers, metric-learning models, and learned structured decoders are allowed. Classical signal features may support the learned model. Training and calibration must use only the supplied public data.
> What Not To Use
> Do not recover original instrument, pitch, dynamics, fold, or filename metadata through external mirrors, hashes, or catalogue lookup.
> Do not map opaque file paths, case_id, row order, storage properties, or public split artifacts directly to targets.
> Do not use hidden test recordings for parameter updates, retrieval-label construction, threshold tuning, or calibration.
> Do not exploit duplicate IDs, omitted rows, extra columns, malformed fields, parser limits, or grader behavior.
> Do not call hosted closed-model APIs during inference.
> Reference Validation
> The exact hidden-answer submission scores 1.0. The sample submission uses valid formatting and is intended only as a schema reference.

Inspiration note: Useful for ordered route/workflow reconstruction outputs with explicit consistency constraints.

## Financial-Statement Concept Completion

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79yd3mjv67gn2bkgrz4mgepn8agwbx
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> When a company reports its financial statements, it populates a particular set of accounting
> concepts -- the individual line items such as revenue, inventory, loans receivable, deferred
> revenue, and hundreds of others. Which concepts appear together is highly structured: some
> combinations are dictated by accounting logic, others are typical of a kind of business, and
> many concepts strongly imply the presence of others.
> In this challenge each case is one filing, given as a set of the concepts it reports, but
> with a variable portion of them MASKED OUT. The mask fraction is sampled independently for
> each filing rather than fixed across the dataset. Each concept is shown as an opaque id such
> as c0042; the ids are consistent across cases but carry no external meaning. You see the
> CONTEXT -- the concepts that remain -- and must predict the SET of masked concepts that were
> removed. It is a cloze-style completion over a financial-statement vocabulary: fill in the
> missing items from the ones you can see.
> This is a multi-label set-prediction task: each case has a set of masked concepts to recover,
> and you output a set. The recovery has to be learned from the co-occurrence structure of the
> training filings -- and because the concepts are opaque, the answer cannot be looked up
> anywhere; it can only come from which concepts tend to appear together. Because mask density
> varies by filing, context size does not reveal the exact number of concepts to predict.
> Evaluation
> Submissions are scored by micro set-F1 between the predicted and the true masked concept
> sets, pooled across the whole test set:
> TP = predicted concept ids that were truly masked
> FP = predicted concept ids that were not masked
> FN = truly masked concept ids that were not predicted
> score = 2*TP / (2*TP + FP + FN)
> Recovering every masked set perfectly scores 1.0; predicting nothing scores 0. Range is 0
> to 1.
> Dataset
> The public data consists of the files below. The CSV files have one row per filing, aligned
> by the id column.
> train.csv — labeled training filings, with columns:
> id — type string: opaque filing identifier.
> context — type string: the revealed concepts, a space-separated set of opaque concept
> ids, for example c0004 c0015 c0037 c0091.
> target — type string: the masked concepts to recover, a space-separated set of opaque
> concept ids, disjoint from context. This column appears only in train.csv.
> test.csv — the filings to predict on, with the same id and context columns as
> train.csv, but with NO target column.
> sample_submission.csv — a valid example submission in exactly the format the grader
> expects, with columns id and concepts.
> task_manifest.json — documentation only: the task name, input and target description, the
> submission columns, and the metric.
> Filings are split so that no company appears in both train and test.
> Example train.csv rows:
> id,context,target
> rec_000621743ddc,c0004 c0015 c0037 c0091,c0002 c0059 c0128
> rec_00a1b2c3d4e5,c0010 c0044 c0080 c0102,c0007 c0150
> The matching test.csv rows drop the final target column.
> Submission
> Submit a CSV with exactly these columns:
> id — type string: test filing id.
> concepts — type string: the set of masked concept ids you predict for that filing, as a
> space-separated list with no repeats. Use an empty string to predict nothing.
> Example:
> id,concepts
> rec_000621743ddc,c0002 c0059 c0128
> rec_00a1b2c3d4e5,c0007 c0150
> Appropriate Approaches
> Compute is CPU only, with a fixed time limit. A co-occurrence or set-prediction model --
> for example a multi-label linear or neural predictor that maps the context concept set to
> scores over the vocabulary -- trains quickly on CPU and is a sensible starting point.
> Concept frequency alone is a weak baseline; the gain comes from which concepts co-occur
> with the specific context you are given.
> Pick how many concepts to output per case, since precision and recall trade off; tune this
> on a company-disjoint split of the training filings.
> What Must Not Be Used
> Predict the masked concepts using only the provided context and the training filings. Do
> not use any external data source to look up or reconstruct the answers.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Acoustic Operation Commutativity Test

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7b2acdtkrvzv04h5mwtjr2b58btckp
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Determine whether two changes to a moving-source recording commute. Each example contains four shuffled sounds intended to form a square: real low-speed, simulated low-speed, real high-speed, and simulated high-speed. Predict where each sound belongs, the four-axis commutator left by traversing the square in opposite orders, and the square edges affected by a corrupted corner.
> The sounds are controlled vehicle pass-by recordings with matched real and simulated versions. In a faithful acoustic simulator, changing speed and then moving from measurement to simulation should produce a result compatible with moving to simulation first and changing speed afterward. The two paths rarely agree perfectly because background noise, spectral detail, modulation, and simulation assumptions interact.
> Some squares are intact. Others replace one corner with a different simulation pipeline, an incorrect speed, or another source identity. This models validation of digital acoustic experiments where paired conditions must preserve the effect of an intervention. The task is not vehicle classification, speed regression, reference recommendation, or sequence generation.
> Objective
> For every case_id, predict:
> | Output | Prediction |
> |---|---|
> | `corner_role_matrix` | Assignment of the four shuffled sounds to the four square roles. |
> | `commutator_vector` | Signed disagreement between the two operation orders on four acoustic axes. |
> | `violating_edge_set` | The two square edges incident to a replaced corner, or `none` for an intact square. |
> Together these outputs reconstruct and test one acoustic commutative square.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Square packet paths and all three targets for training cases. |
> | `test.csv` | Packet paths for a held-out source family. |
> | `sample_submission.csv` | A bounded baseline with one row per test case. |
> | `acoustic_squares/*.npz` | Four-corner waveform and spectrogram packets. |
> Prepared Size
> | Split | Rows | Source families |
> |---|---:|---:|
> | training | 3,000 | 5 |
> | test | 600 | 1 held-out family |
> Every source family contributes 600 squares. Families are separated before packet construction, so no underlying recording or alternate square from the held-out family appears in training.
> CSV Columns
> | Column | Data type | Availability | Description |
> |---|---|---|---|
> | `case_id` | string | train, test | Opaque identifier used only for submission alignment. |
> | `acoustic_square_path` | path string | train, test | Relative path to one compressed NumPy packet. |
> | `corner_role_matrix` | JSON binary matrix | train only | Four public slots by four semantic square roles. |
> | `commutator_vector` | JSON integer vector | train only | Four signed commutator buckets. |
> | `violating_edge_set` | canonical set string | train only | Edges incident to the replaced corner, or `none`. |
> train.csv contains all five columns. test.csv contains only case_id and acoustic_square_path.
> Acoustic Square Packet
> | Array | Data type and shape | Description |
> |---|---|---|
> | `corner_waveforms` | float16, `(4,16000)` | Four normalized pass-by excerpts, each resampled to 4 kHz over four seconds. |
> | `corner_spectrograms` | float16, `(4,48,48)` | Coarse log-magnitude views of the four complete source recordings. |
> Rows in both arrays follow public slots q1 through q4. The slot permutation changes in every case. Small deterministic perturbations are added after packet construction. Original collection names, source identities, speeds, closest-approach times, and filenames are not exposed.
> Square Construction
> The four intended roles are:
> | Role column | Meaning |
> |---:|---|
> | 0 | `real_low`: measured recording at the lower speed |
> | 1 | `sim_low`: matched simulation at the lower speed |
> | 2 | `real_high`: measured recording at the higher speed |
> | 3 | `sim_high`: matched simulation at the higher speed |
> The two speeds differ by 8 through 34 km/h. A case uses one of four equally represented constructions:
> | Construction | Corner content |
> |---|---|
> | intact | All four matched corners are retained. |
> | simulation-pipeline warp | One simulated corner is replaced by an independently generated simulation at the same speed. |
> | speed warp | One corner is replaced by the same source and domain at a nearby incorrect speed. |
> | identity warp | One corner is replaced by another source identity at the intended speed and domain. |
> The replacement is present in the public audio. Scenario selection does not create a cosmetic label or global artifact.
> Target Formats
> Corner Role Matrix
> corner_role_matrix is a 4 by 4 permutation matrix. Rows are public slots q1 through q4; columns are the four roles listed above. Each row and each column contains exactly one 1.
> [[0,1,0,0],[0,0,0,1],[1,0,0,0],[0,0,1,0]]
> This example places q1 at sim_low, q2 at sim_high, q3 at real_low, and q4 at real_high. A corrupted sound retains the role of the corner it replaced.
> Commutator Vector
> Four scalar acoustic summaries are computed from the native-resolution recordings:
> pitch-motion trajectory
> short-time energy envelope
> long-run spectral distribution
> amplitude modulation
> Let R_low, S_low, R_high, and S_high be the four summary vectors after restoring the square roles.
> low_domain_shift = S_low - R_low
> high_domain_shift = S_high - R_high
> normalized_commutator = (high_domain_shift - low_domain_shift)
> / (abs(high_domain_shift) + abs(low_domain_shift) + epsilon)
> Each axis is encoded using thresholds -0.45, -0.12, 0.12, and 0.45:
> | Code | Normalized range |
> |---:|---|
> | `-2` | below `-0.45` |
> | `-1` | `-0.45` through below `-0.12` |
> | `0` | `-0.12` through `0.12` |
> | `1` | above `0.12` through `0.45` |
> | `2` | above `0.45` |
> commutator_vector is a JSON vector of length 4 in the axis order above.
> [0,1,-1,2]
> Violating Edge Set
> The square has four named edges:
> | Edge | Connected roles |
> |---|---|
> | `domain_low` | `real_low` and `sim_low` |
> | `domain_high` | `real_high` and `sim_high` |
> | `speed_real` | `real_low` and `real_high` |
> | `speed_sim` | `sim_low` and `sim_high` |
> An intact square uses none. A replaced corner reports its two incident edges, sorted lexicographically and joined by |.
> domain_high|speed_sim
> Edge-Set Distribution
> | Edge set | Training rows | Test rows |
> |---|---:|---:|
> | `none` | 750 | 150 |
> | `domain_high|speed_real` | 392 | 79 |
> | `domain_high|speed_sim` | 752 | 124 |
> | `domain_low|speed_real` | 372 | 87 |
> | `domain_low|speed_sim` | 734 | 160 |
> Submission Format
> Write the final CSV to:
> ./working/submission.csv
> It must contain exactly these columns in this order:
> case_id,corner_role_matrix,commutator_vector,violating_edge_set
> Example:
> case_id,corner_role_matrix,commutator_vector,violating_edge_set
> ac_39c0bf84f360c8cb7cc4,"[[0,1,0,0],[0,0,0,1],[1,0,0,0],[0,0,1,0]]","[0,1,-1,2]",domain_high|speed_sim
> Requirements:
> Include exactly one row for every test case_id.
> Preserve the required column order and add no columns. One backend-managed visibility column is accepted and ignored.
> Duplicate, missing, blank, extra, or unknown IDs reject the submission.
> Role matrices must be 4 by 4 binary permutation matrices no longer than 70 characters.
> Commutator vectors must contain four integers from -2 through 2 and be no longer than 24 characters.
> Edge sets must be canonical, contain zero or two valid edges, and be no longer than 48 characters.
> Malformed structured values receive zero for their component.
> Evaluation
> Submissions use the Acoustic Commutative Square Score:
> Score = 0.36 * CornerRoleScore
> + 0.39 * CommutatorScore
> + 0.25 * ViolatingEdgeScore
> CornerRoleScore
> assignment_accuracy is the fraction of the four public slots assigned to the correct role.
> row_score = 0.72 * exact_matrix_match + 0.28 * assignment_accuracy
> CornerRoleScore = mean(row_score over test cases)
> An invalid permutation matrix receives row score 0.
> CommutatorScore
> Hidden entries with absolute value 2 have weight 1.6, entries with absolute value 1 have weight 1.25, and zeros have weight 1.0.
> weighted_agreement = sum(weight[k] * I(Y[k] = P[k])) / sum(weight[k])
> row_score = 0.60 * exact_vector_match + 0.40 * weighted_agreement
> CommutatorScore = mean(row_score over test cases)
> ViolatingEdgeScore
> For valid edge sets:
> set_F1 = 2 * number_of_common_edges
> / (number_of_hidden_edges + number_of_submitted_edges)
> row_score = 0.65 * exact_set_match + 0.35 * set_F1
> ViolatingEdgeScore = mean(row_score over test cases)
> When both sets are empty, set F1 is 1. When only one is empty, it is 0. A malformed set receives row score 0.
> Score Range
> Minimum score: 0.0.
> Maximum score: 1.0.
> Higher is better. Exact hidden answers score 1.0.
> Compute Profile
> The challenge provides 3,000 training squares and 600 hidden squares. Compact spectral encoders, pairwise matching models, and permutation-aware classifiers can be trained and evaluated within CPUDefault using 10 CPU cores and 62.5 GiB RAM. The four-second excerpts and 48 by 48 views do not require a GPU.
> What Makes This Interesting
> Most sim-to-real audio benchmarks ask whether two domains match or whether a model transfers between them. This benchmark asks a different algebraic question: do two physical operations commute, and if they do not, where does the square fail?
> The solver must restore a shuffled diagram, compare two paths through it, and localize a replacement through its incident edges. The commutator is a path-dependent certificate rather than another source or domain label.
> What Not To Use
> Do not identify recordings through internet search, acoustic fingerprints, published filenames, or external mirrors.
> Do not use case_id, packet filenames, hashes, row order, source ordering, or split artifacts as predictors.
> Do not recover hidden collection branch, source identity, speed, or closest-approach labels from outside the public challenge files.
> Do not tune models, matching rules, or bucket thresholds using hidden test answers or submission feedback.
> Do not call hosted or closed-model APIs at inference time.
> Do not exploit duplicate IDs, extra columns, malformed JSON, parser limits, or grader behavior.
> Submissions
> 15

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Speech Watermark Filter Circuit Audit

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bm62rndwxtzvnnckjz1ghw98bv2zs
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> For each case, you are given a compact image-like matrix that summarizes four seconds of marked speech, a shuffled list of six possible audio filters, and a deployment policy. Predict three things: how each filter would change the speech evidence, which filters are not clearly worse than another option, and which one filter should be selected under the policy.
> The real-world setting is speech watermark mitigation. A platform may want to reduce a watermark-like signal without damaging intelligibility, timing, or stable speech structure. This is not a simple "strongest filter wins" problem. A filter that removes more watermark evidence can also remove useful speech detail, and a low-cost filter can be preferred when its quality loss is small. The model must judge the tradeoff from the response surface and the row-specific filter catalog.
> Each public packet contains one 64 x 96 response surface. Rows represent coarse frequency regions, columns represent time, and values represent marked-speech evidence after a standardized measurement step. The raw waveform, clean reference, speaker identity, source filename, and actual filtered outputs are not provided.
> The six filter names are shuffled into q1 through q6 independently for every row. The hidden labels were created by running all six filters and comparing internal responses with a private clean reference. Training and test speakers are disjoint, so useful solutions need to learn audio-response patterns rather than memorize speaker content, file order, or candidate positions.
> The prepared representation is intentionally CPU-friendly. All public matrices fit comfortably on a 10-core machine, and practical solutions can use frequency pooling, temporal pooling, discrete cosine features, texture summaries, tree ensembles, linear models, or small neural networks without raw-audio inference.
> Prediction Objective
> Predict exactly these connected artifacts for every case_id:
> | Output | Meaning |
> |---|---|
> | `circuit_response_word` | Six symbols, one per candidate, identifying the dominant evidence block after intervention. |
> | `pareto_intervention_set` | The complete non-dominated set under suppression, speech preservation, and intervention cost. |
> | `countermeasure_certificate` | The selected Pareto candidate, its response block, and its evidence tier under the row's deployment policy. |
> The outputs are coupled. The certificate candidate must belong to the submitted Pareto set, and its cut symbol must match the corresponding character in the submitted response word.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Four public input columns followed by all three training targets. |
> | `test.csv` | The same four public inputs without targets. |
> | `sample_submission.csv` | A schema-valid weak baseline submission. |
> | `watermark_traces/*.npz` | Compact response-surface packets referenced by the CSV files. |
> Prepared Size
> | Split | Rows | Source speakers |
> |---|---:|---:|
> | training | 6,045 | 1,570 |
> | test | 1,202 | 315 |
> Every row originates from a distinct seven-second source excerpt. Preparation uses a deterministic four-second crop before watermarking and surface construction. No source speaker occurs in both splits, and no packet payload is shared across them.
> CSV Columns
> train.csv contains four public input columns followed by three target columns. test.csv contains only the four public input columns.
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque identifier used only to align predictions with hidden rows. |
> | `watermark_trace_path` | relative path string | Location of one compressed NumPy response-surface packet. |
> | `intervention_catalog` | ordered token mapping | Case-specific mapping from `q1` through `q6` to physical filter operations. |
> | `deployment_policy` | categorical string | `suppression_first`, `speech_first`, `balanced`, or `low_compute`. |
> Target Columns In train.csv
> | Column | Data type | Description |
> |---|---|---|
> | `circuit_response_word` | six-character categorical string | One character per candidate ID, from `q1` through `q6`, naming the dominant evidence block for that candidate. |
> | `pareto_intervention_set` | sorted token-set string | Non-empty `|`-separated set of non-dominated candidate IDs. |
> | `countermeasure_certificate` | three-token string | Selected candidate, selected candidate's response block, and evidence tier under the row's deployment policy. |
> Example input row:
> case_id,watermark_trace_path,intervention_catalog,deployment_policy
> wc_45f375902b98d77a83be,watermark_traces/45f375902b98d77a83be.npz,q1:notch_lattice|q2:rolloff|q3:soft_gate|q4:time_smooth|q5:envelope_equalize|q6:frequency_smooth,balanced
> Response-Surface Packet
> | Array | Data type and shape | Description |
> |---|---|---|
> | `response_surface` | float16, `(64,96)` | Coarse log-magnitude frequency-by-time evidence from marked speech with a small deterministic measurement perturbation. Rows run from lower to higher frequency regions and columns follow time. |
> The packet contains no raw waveform, clean reference, source filename, speaker label, watermark-family label, or intervention output. Values are finite and non-negative. A participant may normalize the matrix or derive compact frequency, temporal, modulation, and texture summaries.
> Intervention Catalog
> Every row maps all six candidate IDs to these operations. The mapping order changes independently by case.
> | Operation | Intended behavior |
> |---|---|
> | `rolloff` | Gradually attenuates the upper spectral region. |
> | `frequency_smooth` | Smooths local variation across adjacent frequency bands. |
> | `time_smooth` | Smooths short fluctuations across neighboring time windows. |
> | `soft_gate` | Attenuates weak evidence while retaining stronger speech structure. |
> | `notch_lattice` | Applies a repeated narrow-band attenuation pattern. |
> | `envelope_equalize` | Reduces short-time level variation. |
> Example:
> q1:notch_lattice|q2:rolloff|q3:soft_gate|q4:time_smooth|q5:envelope_equalize|q6:frequency_smooth
> Target Formats
> Circuit Response Word
> circuit_response_word contains exactly six characters. Positions correspond to q1, q2, ..., q6.
> | Symbol | Dominant internal evidence block |
> |---|---|
> | `A` | spectral-envelope response |
> | `B` | temporal-envelope response |
> | `C` | local spectral-difference response |
> | `D` | modulation response |
> | `E` | nonlinear projection response |
> | `X` | no reliable response while preserving minimum speech utility |
> Example:
> ACBXDE
> This means q1 maps to A, q2 to C, q3 to B, q4 to X, q5 to D, and q6 to E.
> Pareto Intervention Set
> pareto_intervention_set is a numerically sorted, |-separated set of candidate IDs. A candidate belongs to the set when no other candidate provides at least as much suppression and speech preservation at no greater cost, with at least one strict improvement.
> q1|q3|q6
> The set is never empty and can contain one through six candidates.
> Countermeasure Certificate
> The certificate contains exactly three >-separated tokens:
> select:<candidate>>cut:<block>>guard:<evidence_tier>
> Valid values:
> | Field | Allowed values | Meaning |
> |---|---|---|
> | `<candidate>` | `q1` through `q6` | Best member of the hidden Pareto set under the row's policy. |
> | `<block>` | `A`, `B`, `C`, `D`, `E`, `X` | Dominant response symbol for the selected candidate. |
> | `<evidence_tier>` | `e0`, `e1`, `e2` | Weak, moderate, or strong mechanism-specific suppression evidence. |
> Example:
> select:q3>cut:B>guard:e2
> Distribution Summary
> | Deployment policy | Training rows | Test rows |
> |---|---:|---:|
> | `balanced` | 1,573 | 298 |
> | `low_compute` | 1,522 | 312 |
> | `speech_first` | 1,465 | 315 |
> | `suppression_first` | 1,485 | 277 |
> | Pareto-set size | Training rows | Test rows |
> |---:|---:|---:|
> | 1 | 1,174 | 251 |
> | 2 | 1,482 | 280 |
> | 3 | 2,179 | 433 |
> | 4 | 541 | 97 |
> | 5 | 195 | 31 |
> | 6 | 474 | 110 |
> All candidate IDs are selected at similar rates in training certificates, from 978 to 1,031 rows per ID. Test counts range from 190 to 224. This balance concerns shuffled candidate IDs, not physical operation identity.
> Submission Format
> Write the final CSV to exactly:
> ./working/submission.csv
> It must contain exactly these columns in this order:
> case_id,circuit_response_word,pareto_intervention_set,countermeasure_certificate
> | Column | Data type | Constraint |
> |---|---|---|
> | `case_id` | string | Must match one test ID exactly. |
> | `circuit_response_word` | six-character string | Every character must be in `A`, `B`, `C`, `D`, `E`, `X`. |
> | `pareto_intervention_set` | sorted token-set string | One through six unique `q` tokens separated by `|`; at most 17 characters. |
> | `countermeasure_certificate` | three-token string | Must follow the certificate grammar; at most 32 characters. |
> Example:
> case_id,circuit_response_word,pareto_intervention_set,countermeasure_certificate
> wc_45f375902b98d77a83be,ACBXDE,q1|q3|q6,select:q3>cut:B>guard:e2
> Submission rules:
> Include exactly one row for every test ID.
> Preserve the required column order and include no extra columns. One backend-managed visibility column is tolerated and removed.
> Duplicate, missing, blank, extra, or unknown IDs reject the submission.
> Frontier sets must be non-empty, numerically sorted, and duplicate-free.
> Overlong or malformed target values receive zero for their affected row component.
> Evaluation
> The evaluation metric is the Filter Circuit Audit Score:
> Score = 0.40 * CircuitWordScore
> + 0.27 * ParetoFrontierScore
> + 0.33 * CountermeasureCertificateScore
> CircuitWordScore
> character_accuracy is the number of correct character positions divided by six.
> row_word_score = 0.75 * exact_word_match + 0.25 * character_accuracy
> CircuitWordScore = mean(row_word_score)
> An invalid word receives row score 0.
> ParetoFrontierScore
> For valid non-empty sets:
> set_F1 = 2 * |truth intersection prediction| / (|truth| + |prediction|)
> row_frontier_score = 0.80 * exact_set_match + 0.20 * set_F1
> ParetoFrontierScore = mean(row_frontier_score)
> An invalid set receives row score 0.
> CountermeasureCertificateScore
> token_accuracy is the fraction of candidate, block, and evidence-tier tokens that exactly match the hidden certificate.
> base_row_score = 0.75 * exact_certificate_match + 0.25 * token_accuracy
> The submitted certificate is coherent only when its selected candidate belongs to the submitted frontier and its cut symbol equals the selected candidate's character in the submitted response word. A coherent certificate keeps base_row_score. An incoherent certificate receives 0.25 * base_row_score. A malformed certificate receives 0.
> CountermeasureCertificateScore is the mean row score.
> Minimum score: 0.0.
> Maximum score: 1.0.
> Higher is better. Exact hidden answers score 1.0. The final score is clipped to [0.0, 1.0] after component aggregation.
> Expected And Allowed Methods
> The compact matrix input is suitable for CPU-only pipelines. Practical approaches include pooled frequency and temporal summaries, low-order DCT or wavelet features, non-negative factorization, random projections, linear or tree ensembles, a small multilayer perceptron, or a shallow compact convolutional network. Candidate-specific heads can condition on the shuffled intervention catalog, while a policy head can select among the predicted Pareto candidates.
> Solutions have up to 1.5 hours on 10 CPU cores and 62 GB of RAM. The full training set and all test packets fit comfortably in memory when loaded as float16 or float32 arrays. No GPU is required or assumed.
> All fitting, calibration, model selection, and inference must use the public training files and execute locally.
> What Not To Use
> Do not match response surfaces to external audiobook, speech-corpus, or source-recording copies through speaker identity, content retrieval, or fingerprint reconstruction.
> Do not derive predictions from case_id, packet filename, row order, archive order, byte hashes, file sizes, or split artifacts.
> Do not obtain the clean reference, hidden watermark family, intervention outputs, or source filename from an external mirror.
> Do not tune features, thresholds, model parameters, or output rules using hidden test answers or submission feedback.
> Do not use hosted or closed-model inference APIs.
> Do not exploit duplicate IDs, missing rows, extra columns, reordered columns, malformed values, parser limits, or grader behavior.
> Submissions
> 37

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Recover the Missing Turn Rule

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78yzbtppc5es08qv1kkawvyx8b4x4e
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Recover the Missing Turn Rule
> Road maps encode legal manoeuvres as relations: an incoming road, an outgoing road, and a rule such as no_left_turn or only_straight_on. In this challenge, each observed OpenStreetMap relation has been reduced to an anonymous junction. The relation itself is hidden.
> Your task is to rank the five most likely candidate completions for every test junction. A completion jointly chooses:
> the outgoing arm (to_arm), and
> the restriction type (restriction).
> This is a structured relation-completion task, not a seven-class restriction classifier. Every candidate slate contains all supported restriction types for every arm, and candidate identifiers are shuffled independently per example.
> Files
> train.jsonl: labelled training examples.
> dev.jsonl: labelled development examples from a different region.
> test.jsonl: unlabelled examples from held-out regions.
> sample_submission.csv: required output shape.
> ATTRIBUTION.md and LICENSE-DATA.txt: provenance and ODbL-1.0 terms.
> Each JSONL row contains:
> example_id: stable row identifier.
> arms: two to eight anonymous junction arms.
> arm_id: local identifier such as a0.
> turn: one of u, hard_right, right, straight, left, or hard_left, measured relative to the incoming arm.
> is_from: true only for the incoming relation member.
> candidates: the allowed joint completions.
> candidate_id: local identifier such as c12.
> to_arm: one of the row's arm identifiers.
> restriction: one of no_left_turn, no_right_turn, no_straight_on, no_u_turn, only_left_turn, only_right_turn, or only_straight_on.
> target_candidate_id: present only in train.jsonl and dev.jsonl.
> Do not assume candidate IDs or arm order carry meaning; both are deterministically shuffled local identifiers.
> Submission
> Submit one CSV row per test.jsonl example, with columns exactly:
> example_id,ranking
> ranking must contain exactly five distinct, valid candidate IDs separated by single spaces, best first. Example:
> test-000000,c12 c3 c19 c0 c8
> Missing or extra example IDs fail validation. A malformed ranking scores zero for that row.
> Metric
> The score is mean reciprocal rank at 5 (MRR@5). If the observed completion is at rank r from 1 through 5, that row scores 1/r; otherwise it scores zero. The final score is the mean over all test rows and is bounded in [0, 1].
> Data design
> Targets are real, human-contributed OpenStreetMap restriction relations from a pinned 2026-07-22 snapshot. Train, development, and test use disjoint geographic regions. Coordinates, names, source IDs, and contributor metadata are absent. To prevent exact source lookup from identifying a hidden row, every retained visible junction signature occurs at least four times, has at least two different observed completions, and no completion occupies more than 60% of its group.
> Data © OpenStreetMap contributors, processed by Geofabrik, and redistributed under ODbL-1.0. See ATTRIBUTION.md.
> Submissions
> 28

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Anonymous Affect Codebook Transfer

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77vxpgnqdzdqbm3t0rvbf94n8bxv2j
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> For each case, match four query recordings to four anonymous reference codes. The reference clips are labeled A, B, C, and D. The query clips express the same four affective conditions in a different voice and a different order. Predict the code corresponding to each query clip.
> This models a practical cold-start problem. An acoustic system may receive a small, locally labeled reference set while the global meaning of those labels is private or changes between deployments. It must transfer the temporary codebook to an unseen speaker instead of memorizing a fixed emotion-to-class map.
> Every case contains eight real speech recordings:
> | Audio role | Meaning |
> |---|---|
> | `reference_A_path` through `reference_D_path` | Four recordings from one speaker. Their affective conditions define the anonymous codes for this case. |
> | `query_1_path` through `query_4_path` | Four recordings from a different speaker. Each uses one of the four reference conditions exactly once. |
> Return one permutation such as C>A>D>B. In this example, query 1 matches reference code C, query 2 matches A, query 3 matches D, and query 4 matches B.
> The hidden split contains speakers that never occur in the training split. Solving the task therefore requires speaker-independent acoustic comparison within each case.
> Dataset
> The public package contains 2,400 labeled training cases and 400 unlabeled test cases. Audio is provided as 16 kHz, mono, signed 16-bit PCM WAV. Each prepared clip is at most 2.6 seconds long. Source filenames and speaker names are replaced by opaque paths, and exact duplicate audio is removed before the speaker split.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Input paths and the correct query code word for 2,400 cases. |
> | `test.csv` | Input paths for 400 held-out cases. |
> | `sample_submission.csv` | A valid submission schema with a fixed baseline prediction. |
> | `audio/*.wav` | Normalized reference and query recordings used by both CSV files. |
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque unique case identifier. |
> | `reference_A_path` | string path | WAV file defining anonymous code A. |
> | `reference_B_path` | string path | WAV file defining anonymous code B. |
> | `reference_C_path` | string path | WAV file defining anonymous code C. |
> | `reference_D_path` | string path | WAV file defining anonymous code D. |
> | `query_1_path` | string path | First query recording. |
> | `query_2_path` | string path | Second query recording. |
> | `query_3_path` | string path | Third query recording. |
> | `query_4_path` | string path | Fourth query recording. |
> train.csv contains all input columns plus query_code_word. test.csv contains only the input columns.
> Target Column
> | Column | Data type | Description |
> |---|---|---|
> | `query_code_word` | string | Four distinct tokens from `A`, `B`, `C`, and `D`, joined by `>`, in query 1 through query 4 order. |
> Valid target strings are permutations of all four codes. They contain exactly four tokens and three > separators. Repeated, missing, lowercase, or unknown codes are malformed.
> Example labeled row, shortened to show the path pattern:
> case_id,reference_A_path,reference_B_path,reference_C_path,reference_D_path,query_1_path,query_2_path,query_3_path,query_4_path,query_code_word
> ac_0123456789abcdef012,audio/a.wav,audio/b.wav,audio/c.wav,audio/d.wav,audio/q1.wav,audio/q2.wav,audio/q3.wav,audio/q4.wav,C>A>D>B
> Evaluation
> The metric is the Anonymous Codebook Transfer Score. It combines position accuracy, relative-order agreement, and complete-case accuracy:
> Score = 0.45 * TokenScore
> + 0.30 * PairOrderScore
> + 0.25 * ExactCaseScore
> TokenScore
> For one case, compare the predicted and true code at each of the four query positions:
> token_score_i = correct query positions / 4
> TokenScore = mean_i(token_score_i)
> PairOrderScore
> Each code word defines an ordering of A, B, C, and D. There are six unordered code pairs. Let c_i be the fraction of these pairs whose relative order is the same in the prediction and truth.
> pair_order_i = max(0, 2 * c_i - 1)
> PairOrderScore = mean_i(pair_order_i)
> The transformation sets chance-level pair agreement to zero while preserving perfect agreement as one.
> ExactCaseScore
> exact_i = 1 if all four submitted codes exactly match the truth, otherwise 0
> ExactCaseScore = mean_i(exact_i)
> A malformed code word receives zero for all three components on that case. The final score is clipped to [0.0, 1.0].
> Minimum score: 0.0.
> Maximum score: 1.0.
> Higher is better.
> The supplied fixed sample submission scores approximately 0.1949 on the hidden answers used during challenge validation. An exact submission scores 1.0.
> Submission Format
> Write the final file to:
> ./working/submission.csv
> It must contain exactly these columns in this order:
> case_id,query_code_word
> Example:
> case_id,query_code_word
> ac_0123456789abcdef012,C>A>D>B
> ac_abcdef0123456789012,B>D>A>C
> The grader rejects duplicate IDs, missing or unknown IDs, extra columns, reordered columns, and row-count mismatches. A single backend-managed visibility column is accepted and removed before schema validation.
> Expected Approach
> The challenge is designed for CPU execution. Useful approaches include log-mel or cepstral features, compact pretrained speech embeddings evaluated on CPU, speaker normalization, metric learning, and permutation decoding. The central requirement is to compare the reference and query recordings within each case while generalizing to held-out voices.
> What Not To Use
> Do not derive predictions from case_id, path hashes, CSV row order, file ordering, or repeated-path frequency.
> Do not search for or match public clips against external copies of the source corpus.
> Do not use speaker names, source filenames, hidden metadata, or source annotation tables as inference inputs.
> Do not construct a lookup from audio hashes or near-duplicate fingerprints to known source labels.
> Do not use private answers, test labels, grader internals, or submission-format behavior to infer targets.
> Do not adapt model parameters, thresholds, or codebooks using withheld test labels.
> Submissions
> 26

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Surface Scan and Acoustic Folio Provenance Matching

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79bhx5qetrsfevj3372k20598br0y5
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Each case contains four fabricated surface scans and four shuffled acoustic measurement folios. Predict three outputs:
> Match each scan to its folio. Every scan and every folio is used exactly once. A correct pair comes from the same physical panel.
> Rank the scans by acoustic confusion. Put first the scan whose matching folio sounds most similar to a competing folio. Put last the scan whose folio is easiest to distinguish from all competitors.
> Report same-design scan pairs. Two scans are siblings when they come from different physical panels manufactured from the same underlying surface design. List every sibling pair, or report none.
> The first output recovers lost record correspondence. The second describes confidence in that recovery. The third separates legitimate repeat fabrications from accidental mismatches.
> The measurements come from additively manufactured architectural panels designed to shape reflected sound. The collection includes flat controls and patterned or deeply textured sand-and-binder surfaces. Dense panel geometry is stored as a three-dimensional mesh, while each acoustic record describes the short reflected response measured at one source-receiver position.
> Geometry and sound were acquired in a controlled two-robot setup. A linear sine sweep from 2 kHz to 40 kHz was played toward each panel and recorded at 96 kHz. The recordings were deconvolved into impulse responses, compensated for temperature, and restricted to the first 4 milliseconds so that the initial panel reflection is emphasized. Thousands of positions were measured per surface under slowly varying temperature, humidity, and pressure.
> The challenge represents a manufacturing archive whose identifiers were lost during independent geometry and acoustics exports. Geometry records and acoustic folios are shuffled separately, so visual position and array order do not reveal correspondence.
> Physical Measurement Context
> These are real experimental measurements, not simulated waveforms or procedurally generated surfaces.
> | Property | Context |
> |---|---|
> | Application domain | Architectural acoustics and the fabrication of wall-panel prototypes that alter reflected sound. |
> | Physical surfaces | Flat controls and patterned or deeply textured panels manufactured from fine sand and phenolic binder. |
> | Geometry record | A three-dimensional mesh of the fabricated panel surface, converted into a normalized point cloud for the challenge. |
> | Acoustic quantity | The microphone pressure response caused by a known sweep reaching the panel and reflecting toward the receiver. Peaks and decay structure encode the timing and strength of panel reflections. |
> | Excitation signal | Linear sine sweep spanning 2 kHz to 40 kHz. |
> | Recording setup | Automated two-robot source-receiver positioning with microphone recordings sampled at 96,000 samples per second. |
> | Response processing | Sweep deconvolution, temperature compensation, and a 4-millisecond window emphasizing the first surface reflection. |
> | Measurement coverage | Approximately 2,951 successfully packaged source-receiver positions per panel, with distance recorded for each position. |
> | Environmental conditions | Temperature, humidity, atmospheric pressure, and ambient sound level were recorded during acquisition and can drift across a long robotic run. |
> The correspondence problem therefore asks whether a model can connect physical surface form with measured reflected-sound behavior. It is relevant when geometry scans and measurement exports from fabrication experiments are stored by separate instruments or laboratory systems and their shared identifiers are damaged or lost.
> Each public packet contains four point clouds and four acoustic folios. An acoustic folio contains twelve coarse response previews, three full-resolution calibration traces, and normalized source-receiver distances. The test labels were constructed using complete measured responses that are not exposed in the public packet.
> The submission columns encode those three predictions:
> | Output | Meaning |
> |---|---|
> | `geometry_folio_permutation` | For each geometry slot, the index of its matching acoustic folio. |
> | `ambiguity_order` | All four scan slots ordered from most easily confused to most acoustically distinctive. |
> | `sibling_geometry_graph` | Every pair of different physical scans manufactured from one shared surface design. |
> This is not acoustic regression, sensor placement, failure analysis, or ordinary nearest-neighbour retrieval. It is a multimodal chain-of-custody reconstruction problem. A system must learn which geometric surface characteristics produce compatible acoustic response families while recognizing that repeat fabrications can be legitimate siblings rather than export errors.
> What Makes This Interesting
> The correct bijection cannot be recovered from filenames, IDs, or shared ordering. Geometry and acoustics are represented in different mathematical spaces, and their relationship is affected by measurement position, repeat fabrication, and coarse public previews. A successful model must construct a shared representation of surface shape and reflected sound.
> The ambiguity target adds a second reasoning layer. Even after predicting a bijection, the model must determine which matched surface has the weakest acoustic separation from the other folios. The sibling graph adds provenance structure: two visibly related surfaces may be separate physical fabrications of one design, and their acoustic signatures can be intentionally difficult to distinguish.
> The grouped split prevents a design family, repeat print, or rotated counterpart from appearing on both sides of the evaluation boundary. This tests transfer to unseen fabricated geometries rather than memorization of known panels.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | 1,680 labeled provenance cases. |
> | `test.csv` | 420 cases containing only public inputs. |
> | `sample_submission.csv` | A schema-valid constant prediction for every test ID. |
> | `provenance_packets/` | Compressed NumPy packets containing four geometry scans and four shuffled acoustic folios. |
> train.csv contains the three input columns and all three target columns. test.csv contains only case_id, provenance_packet_path, and matching_contract. The sample submission contains case_id followed by the three targets.
> CSV Columns
> | Column | Data type | Availability | Description |
> |---|---|---|---|
> | `case_id` | string | train and test | Opaque identifier used only to align submission rows. |
> | `provenance_packet_path` | string | train and test | Relative path to one `.npz` packet. |
> | `matching_contract` | string | train and test | Declares the four-way matching, ambiguity ranking, and sibling-report requirements. It contains no answer. |
> | `geometry_folio_permutation` | JSON integer vector | train only | Four unique integers from `1` through `4`. Position `i` gives the acoustic folio matched to geometry `g(i+1)`. |
> | `ambiguity_order` | ordered token string | train only | All four geometry tokens joined by `>`, least acoustically distinctive first. |
> | `sibling_geometry_graph` | edge-set string | train only | Same-design geometry pairs joined by `|`, or `none` when no pair exists. |
> Packet Arrays
> Geometry slots are g01 through g04. Acoustic folios are indexed 1 through 4 in their public array order.
> | Array | Data type | Shape | Description |
> |---|---|---:|---|
> | `geometry_points` | `float16` | `(4, 768, 3)` | Four independently normalized and rigidly rotated surface point clouds. |
> | `acoustic_folio_previews` | `float16` | `(4, 12, 100)` | Twelve blurred and downsampled impulse-response previews per folio. |
> | `acoustic_folio_calibrations` | `float16` | `(4, 3, 400)` | Three full-resolution calibration traces per folio. |
> | `acoustic_folio_distance_codes` | `float16` | `(4, 12)` | Candidate source-receiver distances normalized separately within each folio. |
> The geometry and folio axes are independently shuffled for every case. No source panel identifier, design name, fabrication metadata, acquisition timestamp, or original filename is included.
> Target Semantics
> For geometry_folio_permutation, the vector [3,1,4,2] means geometry g01 matches public acoustic folio 3, g02 matches folio 1, g03 matches folio 4, and g04 matches folio 2. Every valid vector is a permutation of [1,2,3,4].
> To construct ambiguity_order, eight hidden acoustic summary values are computed for each matched folio. They are the mean and standard deviation of first-difference energy, prominent-reflection count, late-response energy share, and spectral centroid across twelve complete responses. The summaries are standardized within the case. A folio's distinctiveness margin is its Euclidean distance to the nearest other folio. Geometry slots are ordered by this margin from smallest to largest. Deterministic tie breaking is used only for equal margins.
> For sibling_geometry_graph, an edge such as g01~g03 means that the two scans are separate panels associated with the same underlying fabrication design. Edge endpoints use ascending token order, and multiple edges are joined by |. none denotes an empty graph.
> Evaluation
> The metric is the Multimodal Provenance Reconstruction Score.
> Minimum score: 0.0
> Maximum score: 1.0
> Higher is better.
> Score = 0.60 * BijectionScore + 0.22 * AmbiguityOrderScore + 0.18 * SiblingGraphScore
> Malformed values receive zero for their affected component and case. A globally invalid CSV schema is rejected before scoring.
> BijectionScore
> Let entry_agreement be the fraction of the four geometry positions assigned to the correct folio.
> Case score: 0.72 * exact_permutation_match + 0.28 * entry_agreement.
> BijectionScore is the arithmetic mean of case scores.
> An exact match requires the complete four-way bijection. A malformed vector or a vector containing repeated folio indices receives zero.
> AmbiguityOrderScore
> Every four-item order contains six pairwise precedence relations. precedence_agreement is the fraction of the six true relations preserved by the submitted order.
> Case score: 0.56 * exact_order_match + 0.44 * precedence_agreement.
> AmbiguityOrderScore is the arithmetic mean of case scores.
> A valid order contains each of g01, g02, g03, and g04 exactly once.
> SiblingGraphScore
> Let T be the hidden edge set and P be the submitted edge set. Set F1 is 2 * |T intersection P| / (|T| + |P|). When both sets are empty, set F1 equals 1. When only one is empty, it equals 0.
> Case score: 0.64 * exact_edge_set_match + 0.36 * set_F1.
> SiblingGraphScore is the arithmetic mean of case scores.
> Submission Format
> Write the final CSV to exactly ./working/submission.csv.
> It must contain exactly these columns in this order: case_id, geometry_folio_permutation, ambiguity_order, sibling_geometry_graph.
> Example rows:
> | case_id | geometry_folio_permutation | ambiguity_order | sibling_geometry_graph |
> |---|---|---|---|
> | `ap_7c13b8e92a50fd491a2c` | `[3,1,4,2]` | `g03>g01>g04>g02` | `g01~g03` |
> | `ap_41ae6c09574d23b18f60` | `[2,4,1,3]` | `g02>g04>g01>g03` | `none` |
> The CSV must preserve the exact column order. Missing rows, extra rows, duplicate IDs, unknown IDs, duplicate columns, reordered columns, and extra columns are rejected. The optional backend-managed visibility column is removed before exact schema validation. Permutation strings are limited to 16 characters, ambiguity orders to 19 characters, and sibling graphs to 63 characters.
> Expected Methods
> The challenge is designed for CPU execution. Each packet is small, contains only four geometry-folio candidates, and can be processed independently.
> A practical solution can summarize each point cloud with coordinate moments, covariance eigenvalues, radial or height histograms, local roughness statistics, and occupancy projections. Acoustic folios can be represented with arrival-energy profiles, temporal moments, peak statistics, spectral bands, decay summaries, and calibration-to-preview differences. These descriptors produce only sixteen geometry-folio candidate pairs per case.
> Suitable learned models include regularized linear classifiers, compact multilayer perceptrons, random forests, histogram gradient boosting, or pairwise ranking models trained on the supplied cases. The final bijection can be recovered by evaluating all 24 four-item permutations or by using a small assignment solver. Ambiguity ordering and sibling edges can be predicted from the same compact descriptors with separate lightweight heads.
> Feature extraction should be batched with NumPy or an equivalent array library. Parallelizing packets across the available CPU cores is allowed. The complete public packet collection is approximately 73 MB, and the intended workflow fits comfortably within 62.5 GiB of memory without an accelerator.
> What Not To Use
> Do not infer targets from case IDs, packet filenames, row order, hashes, or archive ordering.
> Do not match transformed point clouds or traces against an external copy of the source collection.
> Do not use original panel identifiers, design names, fabrication metadata, timestamps, or source annotations.
> Do not build hardcoded source-panel or family lookup tables.
> Do not exploit malformed JSON, duplicate rows, column reordering, extra columns, or grader behavior.
> Do not tune models or thresholds using hidden labels or grader feedback.
> Models and feature extractors must run locally. Hosted inference APIs are not allowed.
> Submissions
> 64

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Pilot-Limited Binaural Coalition Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78bsthhccv30qny5189vw2h58btb5k
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Predict how six listening interventions work alone and in combination. Each case provides one complete static stereo recording and six brief pilot snippets. From that evidence, recover the utility level of all 63 non-empty intervention subsets, the interaction sign of every intervention pair, and the smallest subsets that attain the highest utility level.
> The recordings come from a rotating two-ear acoustic rig in a controlled loudspeaker environment. Each source trial contains a static capture and full measurements near two rotation angles. The public pilot snippets reveal about 23 milliseconds from each intervention, while the targets are calculated from the complete half-second intervention recordings. Solvers must learn how short pilot evidence predicts the full measurement outcome.
> This models measurement planning for compact robots and acoustic sensing devices. A controller can afford brief probes before committing to a full sensing plan. It must determine which probes add complementary information and which merely repeat evidence already supplied by another motion or frequency band.
> Objective
> For every case_id, predict:
> | Output | Prediction |
> |---|---|
> | `coalition_utility_lattice` | Utility level for all 63 non-empty subsets of six interventions. |
> | `interaction_sign_matrix` | Whether every intervention pair is synergistic, neutral, or redundant. |
> | `minimal_sufficient_antichain` | Minimal intervention coalitions that attain the highest utility level. |
> The three outputs describe one cooperative game. The submitted antichain must be derivable from the submitted lattice.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Acoustic packet paths, intervention catalogs, and all three game targets. |
> | `test.csv` | Inputs for held-out physical source-channel groups. |
> | `sample_submission.csv` | A bounded baseline submission with one row per test case. |
> | `static_packets/*.npz` | Compressed static recordings and pilot snippets referenced by the CSV files. |
> Prepared Size
> | Split | Rows | Independent source-channel groups |
> |---|---:|---:|
> | training | 6,204 | 56 |
> | test | 1,556 | 14 |
> The source hierarchy provides 7,770 complete static recordings with matching intervention captures. Ten duplicate static recordings are discarded, leaving 7,760 public cases. Every condition and trial associated with one physical channel or channel pair remains in one split.
> CSV Columns
> | Column | Data type | Availability | Description |
> |---|---|---|---|
> | `case_id` | string | train, test | Opaque identifier used only for submission alignment. |
> | `static_packet_path` | path string | train, test | Relative path to one compressed NumPy packet containing the static recording and pilot snippets. |
> | `intervention_catalog` | mapping string | train, test | Case-specific mapping from `i1` through `i6` to physical interventions. |
> | `coalition_utility_lattice` | JSON integer vector | train only | Utility levels for coalition masks 1 through 63. |
> | `interaction_sign_matrix` | JSON integer matrix | train only | Symmetric 6 by 6 pair-interaction matrix. |
> | `minimal_sufficient_antichain` | canonical set string | train only | Minimal top-utility coalitions. |
> train.csv contains all six columns. test.csv contains only case_id, static_packet_path, and intervention_catalog.
> Acoustic Packet
> | Array | Data type and shape | Description |
> |---|---|---|
> | `static_binaural` | float16, `(2,22050)` | Left and right captures sampled at 44.1 kHz for 0.5 seconds. |
> | `pilot_binaural` | float16, `(6,2,1024)` | Six noisy 23-millisecond binaural snippets in intervention-ID order. Each snippet comes from the corresponding rotated recording, but not from the complete interval used to construct the targets. |
> The channels are zero-centered, jointly peak-normalized, and perturbed by small deterministic measurement noise. Packets do not contain complete rotated captures, source directions, physical channel identifiers, result text, or original paths.
> Intervention Catalog
> The six intervention IDs are shuffled independently in each case. They cover two rotations and three frequency bands:
> | Physical action | Rotation | Frequency range |
> |---|---:|---:|
> | `rot44_low` | about 44 degrees | 300 to 1,800 Hz |
> | `rot44_mid` | about 44 degrees | 1,800 to 5,000 Hz |
> | `rot44_high` | about 44 degrees | 5,000 to 9,000 Hz |
> | `rot86_low` | about 86 degrees | 300 to 1,800 Hz |
> | `rot86_mid` | about 86 degrees | 1,800 to 5,000 Hz |
> | `rot86_high` | about 86 degrees | 5,000 to 9,000 Hz |
> Example:
> i1:rot86_mid|i2:rot44_low|i3:rot86_high|i4:rot44_high|i5:rot86_low|i6:rot44_mid
> Game Construction
> Each complete follow-up recording produces a four-value change vector relative to the complete static capture in the same frequency band. The public pilot snippets are not used to calculate the labels. The four target cues are interaural lag, correlation-peak sharpness, left-right energy asymmetry, and inter-channel coherence. Changes are standardized across the six interventions within a case and clipped to [-4,4].
> For a non-empty coalition S:
> coverage(S) = mean over four cues of max(abs(change_i), i in S)
> diversity(S) = mean pairwise Euclidean distance / 4
> redundancy(S) = mean absolute pairwise cosine similarity
> utility(S) = coverage(S)
> + 0.22 * diversity(S)
> - 0.18 * redundancy(S)
> - 0.12 * (number_of_interventions(S) - 1)
> For singleton coalitions, diversity and redundancy are both zero. The 63 utilities are discretized by their within-case 25th, 50th, and 75th percentiles into levels 0, 1, 2, and 3.
> Target Formats
> Coalition Utility Lattice
> coalition_utility_lattice is a JSON vector of length 63. Position m - 1 represents coalition mask m, for masks 1 through 63. Bit 0 denotes i1, bit 1 denotes i2, and so on.
> Examples of the ordering:
> | Vector position | Mask | Coalition |
> |---:|---:|---|
> | 0 | 1 | `i1` |
> | 1 | 2 | `i2` |
> | 2 | 3 | `i1+i2` |
> | 3 | 4 | `i3` |
> | 62 | 63 | `i1+i2+i3+i4+i5+i6` |
> Every entry is an integer from 0 through 3.
> Interaction Sign Matrix
> interaction_sign_matrix is a symmetric 6 by 6 JSON matrix. The diagonal is zero. For interventions i and j, compare the pair utility with the larger singleton utility:
> excess(i,j) = utility({i,j}) - max(utility({i}), utility({j}))
> margin = max(0.08 * standard_deviation(all 63 utilities), 0.02)
> The entry is 1 when excess is above the margin, -1 when it is below the negative margin, and 0 otherwise.
> Minimal Sufficient Antichain
> minimal_sufficient_antichain lists every coalition at utility level 3 that has no proper subset at level 3. Intervention IDs inside a coalition are joined by +. Coalitions are ordered by increasing binary mask and joined by |.
> i1+i3|i2+i4|i1+i5+i6
> No listed coalition may contain another listed coalition. The training antichains contain between 1 and 8 coalitions; test antichains contain between 1 and 6.
> Antichain Size Distribution
> | Coalitions | Training rows | Test rows |
> |---:|---:|---:|
> | 1 | 1,432 | 397 |
> | 2 | 1,906 | 467 |
> | 3 | 1,761 | 389 |
> | 4 | 843 | 225 |
> | 5 | 204 | 69 |
> | 6 | 42 | 9 |
> | 7 | 15 | 0 |
> | 8 | 1 | 0 |
> Submission Format
> Write the final CSV to:
> ./working/submission.csv
> It must contain exactly these columns in this order:
> case_id,coalition_utility_lattice,interaction_sign_matrix,minimal_sufficient_antichain
> Example:
> case_id,coalition_utility_lattice,interaction_sign_matrix,minimal_sufficient_antichain
> bp_2f7707b509861fc33c56,"[3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,3]","[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]",i1
> Requirements:
> Include exactly one row for every test case_id.
> Preserve the required column order and add no columns. One backend-managed visibility column is accepted and ignored.
> Duplicate, missing, blank, extra, or unknown IDs reject the submission.
> Lattices must contain 63 integers from 0 through 3 and be no longer than 160 characters.
> Interaction matrices must be symmetric 6 by 6 integer matrices with zero diagonal and values in {-1,0,1}.
> Antichains may contain at most 20 canonical coalitions and no more than 400 characters.
> Malformed structured values receive zero for their component.
> Evaluation
> Submissions use the Intervention Coalition Game Score:
> Score = 0.46 * LatticeScore
> + 0.29 * InteractionScore
> + 0.25 * AntichainScore
> LatticeScore
> For each of the 63 positions, entry_accuracy is 1 for an exact level match and 0 otherwise. ordinal_proximity gives partial credit when the predicted level is close to the hidden level. top_level_F1 treats positions at level 3 as a set and computes standard set F1.
> entry_accuracy = mean(I(Y[k] = P[k]))
> ordinal_proximity = mean(1 - abs(Y[k] - P[k]) / 3)
> top_level_F1 = 2 * number_of_shared_level_3_positions
> / (number_of_hidden_level_3_positions + number_of_predicted_level_3_positions)
> row_score = 0.10 * exact_vector_match
> + 0.38 * entry_accuracy
> + 0.25 * ordinal_proximity
> + 0.27 * top_level_F1
> LatticeScore = mean(row_score over test cases)
> InteractionScore
> Only the 15 unique entries above the diagonal are evaluated. macro_F1 is the unweighted mean of the standard per-class F1 values for -1, 0, and 1, calculated over all evaluated test entries. sign_proximity is 1 for the correct sign, 0.5 when the submitted and hidden signs differ by one step, and 0 when they differ by two steps. exact_matrix_rate is the fraction of test cases whose complete matrix is correct.
> InteractionScore = 0.65 * macro_F1
> + 0.25 * mean(sign_proximity)
> + 0.10 * exact_matrix_rate
> AntichainScore
> Treat the submitted and hidden antichains as sets of coalition masks.
> set_F1 = 2 * number_of_common_coalitions
> / (number_of_hidden_coalitions + number_of_submitted_coalitions)
> Jaccard(A,B) = size(A intersection B) / size(A union B)
> coalition_overlap = 0.5 * (
> mean over hidden coalitions of best submitted Jaccard match
> + mean over submitted coalitions of best hidden Jaccard match
> )
> base_score = 0.15 * exact_antichain_match
> + 0.55 * set_F1
> + 0.30 * coalition_overlap
> If the submitted antichain is exactly the minimal level-3 family implied by the submitted lattice, the row keeps base_score. Otherwise its row score is 0.25 * base_score. AntichainScore is the mean row score.
> Score Range
> Minimum score: 0.0.
> Maximum score: 1.0.
> Higher is better. Exact hidden answers score 1.0.
> What Makes This Interesting
> The benchmark reconstructs a hidden set function, not a best action. It asks how information changes when interventions cooperate, overlap, or become redundant, then checks whether the reported minimal sufficient family agrees with the entire submitted lattice.
> This creates a new reasoning object for binaural audio: cooperative-game recovery from short pilot observations. The 63 outputs are not independent labels. They form a constrained Boolean-lattice certificate with pair interactions and minimality structure.
> What Not To Use
> Do not recover source channels, directions, hidden rotated recordings, result text, or original paths from external copies of the source release.
> Do not fingerprint public audio against online mirrors or acoustic databases.
> Do not use case_id, packet filenames, hashes, row order, archive order, or split artifacts as predictors.
> Do not tune models, utility thresholds, or calibration rules using hidden test answers or submission feedback.
> Do not call hosted or closed-model APIs at inference time.
> Do not exploit duplicate IDs, extra columns, malformed JSON, parser limits, or grader behavior.
> Submissions
> 44

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Machining Audio And Force Record Association

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79gtz26dqtsn3gnwqgakyma98bzgv3
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: ↑ Higher is better

Full challenge description from page:

> Overview
> Match one machining-sound window to five candidate cutting-force traces, then rank all five candidates from most compatible to least compatible. Exactly one candidate was recorded during the same turning trial as the sound. The remaining candidates come from nearby operating settings and must also be placed in the correct relative order.
> The task represents a practical data-association failure in instrumented manufacturing. Microphone files and dynamometer exports may lose their shared trial identifiers after a controller reset, a partial export, or a laboratory data migration. Before the records can support process monitoring or force estimation, an engineer must determine which acoustic and mechanical measurements describe the same cutting regime.
> Every prediction is a five-letter route. Recovering only the best packet is useful, but the full route also measures whether the model has learned the local structure of the operating space.
> Association Rule
> Each original experiment is defined by cutting speed, cutting depth, and feed rate. For target construction, each physical parameter is replaced by its ordered level index and scaled independently to [0,1]. Candidate compatibility is Euclidean distance from the sound trial in this three-dimensional normalized operating space.
> The packet from the same experiment has distance zero. Other packets are ordered by increasing distance. Candidate letter is used only to break an exact distance tie.
> The five force candidates are stored in array order A, B, C, D, E. Their order in the packet is randomized independently for every case, so array position does not indicate compatibility.
> Dataset
> The public training set contains 1,680 cases derived from 70 experiments. The test set contains 420 cases derived from 30 other experiments. All transformed views of one experiment stay in one partition. Each documented speed, depth, and feed level is represented in both partitions.
> Signal Files
> Sound windows are 1.5-second mono WAV files at 16 kHz using signed 16-bit PCM. Stable random cropping, mild spectral equalization, level normalization, and low measurement noise reduce direct source-file fingerprinting.
> Each force packet is a NumPy .npy file containing a float32 array with shape (5,3,96):
> | Axis | Interpretation |
> |---|---|
> | 0 | Five candidates in fixed letter order `A` through `E`. |
> | 1 | Tangential `Ft`, radial `Fr`, and axial `Fa` force components. |
> | 2 | 96 uniformly resampled points from each force trace. |
> Independent small gain and sensor-noise transformations are applied to each candidate trace. Values remain expressed in the source force scale.
> Public Layout
> | Path | Contents |
> |---|---|
> | `train.csv` | Input paths plus the correct candidate route. |
> | `test.csv` | Input paths for held-out experiments. |
> | `sample_submission.csv` | Valid fixed-order submission. |
> | `audio/*.wav` | Opaque sound queries. |
> | `force_packets/*.npy` | Opaque five-candidate mechanical evidence packets. |
> CSV Schema
> | Column | Data type | Present in | Meaning |
> |---|---|---|---|
> | `case_id` | string | train and test | Opaque case identifier. |
> | `sound_window_path` | string path | train and test | Query acoustic window. |
> | `force_packet_path` | string path | train and test | Candidate force array with shape `(5,3,96)`. |
> | `force_route` | canonical string | train only | Candidate letters ordered from smallest to largest hidden compatibility distance. |
> A route contains each uppercase letter from A through E exactly once and uses > as the separator.
> C>A>E>B>D
> Training contains all 120 possible five-letter permutations. The test answers contain 117 of them.
> Submission Format
> Save the prediction file at:
> ./working/submission.csv
> The schema is exact and ordered:
> case_id,force_route
> Both fields are strings. Example:
> case_id,force_route
> lr_0123456789abcdef012345,C>A>E>B>D
> lr_abcdef0123456789abcdef,B>D>A>C>E
> Extra or reordered columns, duplicate column names, duplicate IDs, unknown IDs, omitted rows, additional rows, whitespace-padded IDs, and row-count mismatches are rejected. A single platform-managed visibility column may be present and is removed before validation. Routes longer than 24 characters and values that are not exact A to E permutations are malformed.
> Evaluation
> The Cross-Instrument Association Score evaluates the first choice, the complete relative order, and exact route recovery:
> Score = 0.50 * SameTrialScore
> + 0.35 * RelativeOrderScore
> + 0.15 * ExactRouteScore
> SameTrialScore
> For sample i, let same_i be one if the first submitted letter identifies the zero-distance force packet, otherwise zero.
> SameTrialScore = mean over samples of same_i
> RelativeOrderScore
> Five candidates create 10 unordered pairs. Let a_i be the fraction of those pairs whose relative order matches the hidden route.
> order_i = max(0, 2 * a_i - 1)
> RelativeOrderScore = mean over samples of order_i
> Agreement of one half or less contributes zero, while all 10 correct pair relations contribute one.
> ExactRouteScore
> exact_i = 1 when all five positions match, otherwise 0
> ExactRouteScore = mean over samples of exact_i
> Malformed routes receive zero for every component on the corresponding sample. The final weighted value is clipped to [0.0,1.0].
> Minimum score: 0.0.
> Maximum score: 1.0.
> Higher scores are better.
> Operational Significance
> This is not ordinary machine-state classification. The model must compare two sensor modalities, identify the one truly paired experiment, and preserve local ordering among four deliberately similar alternatives. The experiment-level holdout tests whether that relationship transfers to unseen combinations instead of memorizing transformed windows.
> What Not To Use
> Do not derive candidate routes from case IDs, opaque filenames, path order, CSV order, file size, or array storage beyond the documented candidate axis.
> Do not match challenge media to external source files, public trial numbers, source hashes, or published feature tables.
> Do not rebuild hidden targets from original filenames, source catalog order, or download metadata.
> Do not use private answers, grader internals, malformed-input behavior, duplicate exploitation, or leaderboard probing.
> Do not train, calibrate, or select routes using withheld test outcomes.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Multi-Task Rook Vocalization Recognition

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74vx07ftvp38nk8cz98fkhm58bz34c
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Easy
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Multi-Task Rook Vocalization Recognition
> Overview
> A captive colony of 15 rooks was recorded over many sessions, and every vocalisation was annotated with which individual produced it and which call type it was. This challenge asks you to do three different things at once on each one-second window of audio: decide whether a possibly faint rook call is present, recognise which of the 15 known rooks produced it, and recognise which of the 8 common call types it is.
> These are three genuinely different skills. Detecting that a call is present tells you nothing about who made it or what type it is, and the individual and the call type are themselves only weakly related, because each rook uses many call types and the same types recur across individuals. The final score is the average of the three, so being excellent at one skill alone leaves most of the score unclaimed, and you have to detect and identify and categorise.
> The test windows come from recording sessions held out of training, so a model cannot lean on a session-specific background or one stereotyped call. It must learn a genuine voice signature and call-type representation that survive a change of session, and it must find faint calls without raising false alarms. This is deliberately hard.
> Task
> For each test window you output, in one row:
> det_score â€” how likely the window contains a rook call, higher meaning more likely a call.
> ind_0 through ind_14 â€” a score for each of the 15 rooks, higher meaning more likely that individual made the call.
> ct_0 through ct_7 â€” a score for each of the 8 call types, higher meaning more likely that call type.
> You are given training windows, each marked as a call or background, and for calls labelled with the individual and, where applicable, the call type, together with the recording session so you can hold out whole sessions when validating. The individual and call-type outputs are only scored on the call windows, but you output all of them for every window.
> Required approach. Train a model on the provided windows, for example a single multi-task network with a shared spectrogram body and three heads for detection, individual and call type, or separate specialised models. A learned representation is what carries all three skills, and a solution that only detects, or only identifies, leaves most of the score unclaimed.
> Evaluation
> Submissions are scored with RookScore, higher is better, in the range 0 to 1. It is the average of three sub-scores, each in 0 to 1:
> Detection efficiency. For a fixed false-alarm rate a, set the threshold at the det_score above which a fraction a of the background windows fall. The detection efficiency at that false-alarm rate is the fraction of weak calls, the faint near-threshold ones, scored above the threshold. This sub-score averages the efficiency at a = 0.05 and a = 0.10.
> Individual agreement. For each call window, rank the 15 rooks by your ind_ scores. The reciprocal rank of the true individual is 1 divided by its rank, and tied scores share their average rank. This sub-score is the mean reciprocal rank over the call windows.
> Call-type agreement. The same mean reciprocal rank for your ct_ scores against the true call type, over the call windows that carry one of the eight scored call types.
> RookScore = the mean of detection efficiency, individual agreement and call-type agreement.
> Only the ordering of your scores within each group matters, so any monotonic scale is fine.
> Dataset
> The prepared public dataset:
> train_X.npy â€” training windows, a float16 array of shape Ntrain by 16000: one-second windows at 16 kHz, a mix of calls and background.
> train_iscall.npy â€” an int8 array of length Ntrain: 1 if the window is a call, 0 if background.
> train_ind.npy â€” an int8 array of length Ntrain: the individual id 0 to 14 for calls, and -1 for background.
> train_ct.npy â€” an int8 array of length Ntrain: the call-type id 0 to 7 for calls that carry one of the eight scored types, and -1 otherwise.
> train_rec.npy â€” an int16 array of length Ntrain: a recording-session id. Calls that share a value came from the same session, so use it to hold out whole sessions when validating.
> test_X.npy â€” test windows, a float16 array of shape Ntest by 16000. The id of the window in row i, counting rows from 0, is the letter t followed by i written as a zero-padded 5-digit integer, so row 0 is t00000, row 1 is t00001, and so on.
> individuals.txt, call_types.txt â€” the 15 rook names and the 8 call-type codes, one per line, where the line number is the id.
> sample_submission.csv â€” a valid submission in the required format.
> The same 15 individuals appear in training and test, but training and test windows always come from different recording sessions.
> Because the test windows are whole recording sessions held out of training, hold out whole sessions when you validate: group by train_rec.npy so no session appears on both sides of your split. A validation that does not hold out whole sessions will overestimate the held-out test score by roughly a tenth, because windows from the same session share a background and a few stereotyped calls and are much easier to match than windows from an unseen session.
> Submission
> Submit a CSV with exactly these 25 columns: id, det_score, ind_0 through ind_14, ct_0 through ct_7.
> Every test id must appear exactly once, and every value must be finite. Output all scores for every window, call or background. Example, abbreviated:
> id,det_score,ind_0,...,ind_14,ct_0,...,ct_7
> t00000,0.98,0.03,...,0.01,0.10,...,0.05
> t00001,0.02,0.07,...,0.06,0.14,...,0.09
> Write the final submission to ./working/submission.csv, UTF-8.
> Allowed And Prohibited
> Allowed:
> Train any model on the provided windows: 2-D CNNs on spectrograms, 1-D CNNs on the waveform, temporal-convolutional, recurrent or transformer networks, multi-task shared bodies or separate specialised models, embedding or metric-learning heads.
> Any preprocessing of the audio such as spectrograms, band-pass filtering, whitening, normalisation or resampling, plus data augmentation and ensembling.
> Standard open-source deep-learning libraries such as PyTorch.
> Prohibited:
> Do not use external datasets or any information beyond the provided files.
> Do not train on, adapt to, or fit statistics from the test windows, whose labels are withheld.
> Do not hardcode outputs or use per-id answer tables.
> Do not use external LLM APIs or any model-generated labels in your submission.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Calibrated Directed Forest Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fgcacs4cn483dj7wjwr7nfs8bxd26
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Calibrated Directed Forest Recovery
> Overview
> Domain: graph recovery â€” a structured, one-shot decision problem over daily observations. Measurement stations are organized into fully independent branching flow networks, each recording a physical quantity (e.g., water volume passing through) at regular intervals. The underlying structure is a directed forest: every station except a terminal sink drains into exactly one downstream station, so the networks contain no loops.
> Your task: for each station in the evaluation networks, decide its downstream partner â€” commit to a single ordered pair (u â†’ v), or leave the station unpaired (treating it as a sink). Each source station gets exactly one bid; a station submitted with no proposal is treated as having no outgoing connection. You also assign a confidence score to each proposal, used only to resolve directed cycles if they arise. A fixed greedy procedure then constructs a valid directed forest from your proposals and scores it against hidden reference pairs via Directed Edge F1.
> The defining difficulty is heterogeneous missingness: the observations are heavily gapped, and different station pairs share wildly different amounts of overlapping records â€” from near-complete to almost none. A decision must be made from whatever overlap exists. This is a commitment problem, not an estimation problem: there is no retry, no soft output to post-process, and no second guess once a station's bid is fixed.
> Distinct from dependence-estimation approaches that reconstruct a network from complete joint observations â€” for example extremal/tail-dependence methods that fit a single root-directed tree from extreme concurrent readings (QTree; Tran, Buck & KlÃ¼ppelberg, JRSS-B 2024) â€” this task is a per-station commitment over ordinary full-record series with heterogeneous gaps, across many disjoint networks, and is scored by the forest that the commitments induce.
> The central difficulty is cross-network generalization: the evaluation networks contribute zero training labels, so anything tuned to the development networks must transfer on the strength of its method, not its vocabulary of station behavior. Validation should therefore be grouped by network, mirroring the development/evaluation relationship.
> All data is real (USGS daily mean streamflow, 2018-2022). All labels are real directed connectivity links (first-downstream-neighbor edges from the USGS NLDI / NHDPlus flow network). Nothing is synthetic or model-generated.
> Dataset Info
> File structure:
> | File | Rows | Description |
> |------|------|-------------|
> | train_series.csv | 1,826 | Discharge matrix for the 10 development basins (213 gauges) |
> | train_edges.csv | 168 | Reference directed edges for the development basins (labels) |
> | dev_series.csv | 1,826 | Discharge matrix for the 7 validation basins (150 gauges) |
> | dev_basin_ids.csv | 150 | Station â†’ basin mapping for the validation basins |
> | test_series.csv | 1,826 | Discharge matrix for the 23 evaluation basins (510 gauges) |
> | test_basin_ids.csv | 510 | Station â†’ basin mapping for the evaluation basins |
> | sample_submission.csv | 0 | Format example (header only) |
> Columns of train_series.csv, dev_series.csv, test_series.csv:
> | Column | Type | Description |
> |--------|------|-------------|
> | date | string | Observation date YYYY-MM-DD) |
> | g0, g1, ... | float | Station reading; blank = no value recorded |
> Data characteristics:
> 1,826 daily observations per station (2018-01-01 to 2022-12-31).
> Fully disjoint networks: no station or edge crosses a basin boundary, and the evaluation basins share no stations with the development or validation basins. A station belongs to exactly one basin.
> 84 of the 510 evaluation stations are sinks (no outgoing connection); each of the other 426 evaluation stations has exactly one outgoing edge. Proposing an edge from a true sink is a guaranteed false positive.
> Heterogeneous gaps: many station-observation pairs have no recorded value. The gap pattern differs across stations â€” some have near-complete records while others are sparse â€” so different station pairs have wildly different amounts of overlapping observations.
> Anonymized identifiers: station IDs are integers, globally permuted by a deterministic hash. No station locations, names, coordinates, or metadata are provided; identity-based shortcuts are impossible.
> Evaluation
> Submissions are scored with Directed Edge F1 over the forest selected from your proposals. The scorer is deterministic and applied in this order:
> Merge duplicates â€” multiple rows with the same (basin_id, u, v) are merged by keeping the highest confidence.
> One bid per source â€” for each source station, keep the highest-confidence proposal and discard the rest.
> Greedy forest construction â€” sort the surviving proposals by confidence descending; accept each (u â†’ v) if station u has no accepted outgoing partner yet and adding it does not create a directed cycle with already-accepted pairs.
> Score the accepted forest against the reference pairs:
> Precision = |accepted âˆ© reference| / |accepted|
> Recall    = |accepted âˆ© reference| / |reference|
> Score     = 2 Ã— P Ã— R / (P + R)
> Higher is better; the score ranges from 0 to 1.
> Confidence is for cycle breaking, not source competition. Because each source station already commits to at most one proposal, there is no per-source competition to resolve. Confidence only matters when the submitted proposals collectively contain a directed cycle: the scorer drops the lowest-confidence edge in each cycle. If your proposals are acyclic (as a correct forest should be), confidence does not affect the outcome.
> Scoring details:
> Direction is strict. A reversed pair (v â†’ u) where the reference has (u â†’ v) counts as both a false positive and a false negative.
> Range. Score âˆˆ [0, 1]. Empty proposal against non-empty reference â†’ 0. Empty against empty â†’ 1.
> Scope. Only pairs within the evaluation networks contribute; the reference contains no cross-network pairs.
> Pooling. All evaluation networks are scored together in one pass, not averaged per network.
> Validity gate. Submissions are validated before selection and rejected on per-entry violations: wrong fields, non-integer or negative IDs, confidence outside [0, 1], unknown network or station IDs, or self-loops. Directed cycles are not rejected â€” they are resolved at selection time.
> Sample Submission
> Submit a CSV with exactly the four columns basin_id, upstream_gauge_id, downstream_gauge_id, confidence, in that order. Each row is one candidate directed edge upstream_gauge_id â†’ downstream_gauge_id:
> basin_id,upstream_gauge_id,downstream_gauge_id,confidence
> basin_merrimack,5,3,0.92
> basin_merrimack,3,8,0.87
> basin_trinity,2,7,0.74
> Rules:
> One proposal per source station. A station may appear as upstream_gauge_id at most once. Multiple rows with the same source â†’ highest confidence kept.
> Stations with no proposal are sinks (no outgoing connection). A basin with no predicted edges is represented by omitting it entirely; an empty (header-only) CSV is valid.
> All station IDs must be integers from the evaluation network's station mapping test_basin_ids.csv). Unknown IDs â†’ rejected.
> Confidence must be a real number in [0, 1].
> No self-loops u == v). Duplicate entries for the same directed pair are merged by taking the highest confidence.
> No extra fields beyond the four required ones. Row order is ignored.
> Submissions with wrong columns, malformed or unknown IDs, confidence out of range, or self-loops are rejected.
> What to Use
> The files listed under Dataset Info.
> train_edges.csv for fitting and cross-validation. All modeling choices must use only the development networks; the validation basins provide a held-out check on generalization before submission.
> numpy, scipy, scikit-learn (and other libraries pre-installed in the grading environment).
> Runtime budget: 90 minutes CPU on 10 cores / 62.5 GiB RAM. No internet.
> What Not to Use
> The evaluation networks' reference pairs (withheld), or any file outside the public directory.
> Any external data or lookups that could recover station identity or structure. No internet access.
> Station metadata beyond what is in the public files.
> Large pretrained models, cloud services, or packages not in the installed set.
> Tuning against the evaluation metric (inaccessible by design).

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Wearable Muscle And Motion Stream Reassociation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx707g149jdfjdnv6a9b7njw7x8bz4s4
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Predict one thing for every case: the complete one-to-one pairing between six forearm-sensor fragments and six anonymous glove-motion fragments.
> The case represents a synchronization failure in a wearable laboratory. A forearm armband and an instrumented glove recorded repeated executions of one movement, but their shared timestamps were lost during export. The six armband fragments remain in order E1 through E6; the six glove fragments have been shuffled and relabeled A through F. The required answer identifies which glove fragment belongs to each armband fragment.
> This is not gesture classification. All twelve fragments in a case come from the same participant, recording session, and hidden gesture. They differ only by repetition speed and temporal window. A successful model must distinguish subtle within-gesture dynamics, learn how forearm muscle activity relates to finger-joint motion, and solve a six-way assignment for participants absent from training.
> Reading One Case
> Each row points to one compressed NumPy packet. Loading that packet returns two arrays:
> | Array | Shape | Data type | Interpretation |
> |---|---:|---|---|
> | `muscle` | `(6,128,8)` | `float16` | Six forearm-electromyography fragments in fixed order `E1` to `E6`. Wrist inertial channels are deliberately excluded. |
> | `motion` | `(6,128,20)` | `float16` | Six shuffled glove fragments in candidate order `A` to `F`. The channels are four joint measurements for each of thumb, index, middle, ring, and pinky. |
> Every fragment is independently median-centered, scaled by its 90th-percentile absolute deviation, and clipped to [-6,6]. Both arrays contain 128 time samples. The glove window receives a deterministic start-and-end clock offset of up to 1.8 percent of the source recording, reproducing mild synchronization drift without changing fragment identity. Array position, file size, and identifier do not preserve the original recording order.
> The target is a six-character permutation. Character position corresponds to an armband fragment; character value names its synchronized glove candidate:
> E1 E2 E3 E4 E5 E6
> C  F  A  B  E  D
> The corresponding submission value is CFABED. Every letter A through F must occur exactly once.
> Dataset
> The prepared benchmark contains 1,580 labeled training cases and 394 hidden cases. Complete participants are assigned to only one partition before any temporal windows or packets are made. Thus, all windows from one participant remain together, including windows cut from the same source recording.
> Within each participant, session, and gesture, every source recording is divided into four temporal windows. The resulting same-gesture fragments are shuffled and consumed in groups of six. Armband and glove order are then permuted independently. A source fragment is used in only one case. Public case IDs and packet names are salted hashes that do not encode participant, session, gesture, speed, source path, or generation order.
> Public Files
> | Path | Purpose |
> |---|---|
> | `train.csv` | Packet paths and correct reassociation permutations. |
> | `test.csv` | Packet paths with the permutation withheld. |
> | `sample_submission.csv` | A format-valid fixed permutation. |
> | `packets/*.npz` | Paired armband and shuffled glove arrays. |
> CSV Contract
> | Column | Data type | `train.csv` | `test.csv` | Meaning |
> |---|---|---:|---:|---|
> | `case_id` | string | yes | yes | Opaque case identifier. |
> | `packet_path` | string | yes | yes | Relative path such as `packets/pkt_0123456789abcdef0123.npz`. |
> | `handoff_permutation` | six-character string | yes | no | Bijection from `E1...E6` to candidates `A...F`. |
> A labeled record has this form:
> case_id,packet_path,handoff_permutation
> wr_0123456789abcdef0123,packets/pkt_abcdef0123456789abcd.npz,CFABED
> Evaluation
> The Wearable Stream Reassociation Score rewards complete recovery while still giving measured partial credit. It has three terms computed from the same submitted permutation:
> Score = 0.55 * ExactReassociation
> + 0.30 * CorrectedPositionAgreement
> + 0.15 * CorrectedSwapSimilarity
> Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> ExactReassociation
> For row i, exact_i is 1 only when all six assignments are correct, and 0 otherwise.
> ExactReassociation = mean(exact_i)
> CorrectedPositionAgreement
> Let a_i be the fraction of the six positions whose submitted letter equals the hidden letter. Across uniformly random valid permutations, the expected position agreement is 1/6. The correction removes that legal-guess floor:
> raw_position = mean(a_i)
> CorrectedPositionAgreement = max(0, (raw_position - 1/6) / (1 - 1/6))
> CorrectedSwapSimilarity
> Compose the submitted permutation with the inverse hidden permutation. The resulting permutation describes how the submitted assignment must be rearranged to become correct. If it contains c_i disjoint cycles, the minimum number of pair swaps is d_i = 6 - c_i.
> swap_similarity_i = 1 - d_i / 5
> raw_swap = mean(swap_similarity_i)
> CorrectedSwapSimilarity = max(0, (raw_swap - 0.29) / (1 - 0.29))
> The constant 0.29 is the exact expected swap similarity over all 6! = 720 valid permutations. Chance correction is applied after averaging across the hidden set, so a random legal strategy has an expected corrected score near zero rather than receiving structural credit.
> Malformed permutations receive zero for all three terms on that row. Hidden answers are validated independently.
> Submission Format
> Write the final file to:
> ./working/submission.csv
> It must contain exactly these columns in exactly this order:
> case_id,handoff_permutation
> | Column | Required representation |
> |---|---|
> | `case_id` | One unchanged identifier from `test.csv`. |
> | `handoff_permutation` | Exactly six uppercase characters, using each of `A`, `B`, `C`, `D`, `E`, and `F` once. |
> Example:
> case_id,handoff_permutation
> wr_0123456789abcdef0123,CFABED
> wr_11111111111111111111,BEDACF
> The grader rejects reordered or extra columns, duplicate IDs, missing or extra rows, unknown IDs, and IDs with surrounding whitespace. The platform-managed visibility field is ignored when present. A malformed permutation is retained as an incorrect prediction rather than repaired or clipped.
> Practical Modeling Scope
> The benchmark is sized for CPU execution within 1.5 hours. Useful systems can learn compact temporal embeddings for EMG and glove motion, compare activation envelopes and motion derivatives under small clock offsets, score all 36 cross-modal pairs, and decode the maximum-weight bijection with a standard assignment algorithm. Broad gesture classification cannot distinguish candidates inside one packet. Participant-grouped validation is important because the hidden set contains entirely unseen people.
> What Not To Use
> The reassociation must be inferred from the released sensor evidence:
> Do not identify participants, sessions, gestures, or speeds through external source matching.
> Do not use case IDs, packet names, row order, compressed byte size, or archive ordering as predictors.
> Do not match public fragments against an external copy of the original recordings or their checksums.
> Do not reconstruct hidden assignments from private glove timestamps, source paths, or metadata not supplied in the public files.
> Do not exploit malformed rows, duplicate IDs, extra columns, missing rows, or grader behavior.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Bridge Sensor Window Selection and Observability Matrix Prediction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7aj56qep8w6w1xe6z48zw6y98c0t88
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Choose three of twelve bridge-sensor windows, then describe how well those three windows distinguish six recorded bridge conditions.
> Each case contains vibration evidence from six physical episodes, labeled e0 through e5, at twelve candidate measurement windows, labeled w00 through w11. The first submitted field names the three windows to retain. The second is a 6 by 6 matrix: entry [i][j] states how clearly the selected windows separate episode ei from episode ej, using categories 1 through 4.
> This models a field-monitoring budget decision. A bridge team may have twelve usable measurements but enough telemetry, power, or processing capacity to preserve only three. A useful selection must distinguish all episode pairs, including the hardest pair, while avoiding three windows that carry nearly identical information.
> The time-frequency tiles come from repeated bridge-vibration measurements. Training uses two field runs and the hidden set uses a third run. Episode and window order are shuffled independently in every case. The task is measurement planning from vibration evidence, not damage-label classification.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | 4,800 cases with inputs, scored targets, and a train-only response supervision matrix. |
> | `test.csv` | 1,000 cases built from a held-out repeated field run. |
> | `sample_submission.csv` | A schema-valid fixed plan and fixed matrix for every test case. |
> | `response_packets/*.npy` | Float16 time-frequency packets referenced by the CSV files. |
> CSV Columns
> | Column | Data type | Availability | Description |
> |---|---|---|---|
> | `case_id` | string | train, test | Opaque identifier used only to align submissions. |
> | `response_packet_path` | relative path string | train, test | Path relative to the public dataset root, such as `response_packets/bw_45a1....npy`. |
> | `packet_contract` | fixed-format string | train, test | Declares packet shape, episode labels, window labels, and the three-window budget. |
> | `window_schedule` | canonical token set | train only | Three selected window IDs. |
> | `observability_matrix` | JSON integer matrix | train only | Symmetric 6 by 6 separation certificate for the selected windows. |
> | `packet_response_matrix` | JSON float matrix | train only | Shape `(6, 12)`. Each row is an episode and each column is a public window. Values summarize visible spectral structure and provide auxiliary supervision. |
> train.csv contains all six columns. test.csv contains only case_id, response_packet_path, and packet_contract.
> Packet Contract Format
> packet_contract is the same fixed semicolon-separated string in every row:
> shape=6x12x24x24;episodes=e0_e5;windows=w00_w11;window_budget=3
> It is descriptive metadata rather than a hidden instruction. Split the string at semicolons, then split each segment at the first = character:
> | Key | Value | Meaning |
> |---|---|---|
> | `shape` | `6x12x24x24` | Packet axes are six episodes, twelve windows, 24 time bins, and 24 frequency bins. |
> | `episodes` | `e0_e5` | Episode labels run from `e0` through `e5`. |
> | `windows` | `w00_w11` | Candidate window labels run from `w00` through `w11`. |
> | `window_budget` | `3` | Every submitted schedule must contain exactly three distinct windows. |
> Response Packet
> Every .npy file has shape (6, 12, 24, 24) and dtype float16:
> axis 0 contains episodes e0 through e5;
> axis 1 contains candidate windows w00 through w11;
> axes 2 and 3 form a 24 by 24 time-frequency tile.
> One episode comes from a baseline condition and five come from physically changed conditions. Their order is randomized, and the omitted physical state varies by case. A candidate window represents one longitudinal station and one acceleration axis, aggregated across five stringers. Window identities are randomized independently in every case. Tiles summarize approximately 32 seconds of response between 0.5 and 40 Hz. Contrast changes, time rolls, additive noise, and occasional local dropouts prevent exact source matching.
> Packet Response Supervision
> packet_response_matrix contains 72 finite floating-point values in episode-major order. Entry [e][w] summarizes the visible frequency centroid, low-to-middle and high-band balance, temporal centroid, spectral roughness, and pulse contrast of the tile at episode e and window w. It is an auxiliary training label and is not a submission column.
> A solver can regress these values from training tiles, predict them for test tiles, and robustly standardize the six episode values within each window. The hidden response catalog used for target construction combines 0.80 times this standardized packet response with 0.20 times a standardized clean high-resolution response. The six combined episode values within every window are standardized once more before plans and matrix margins are computed. This keeps a real clean-response contribution while making most of the target evidence observable in the released packet.
> Window Schedule
> window_schedule contains exactly three distinct IDs from w00 through w11, joined by |:
> w01|w06|w10
> Token order does not change the score. Training targets use ascending order for a canonical representation. All 220 possible three-window schedules occur in training. The largest training schedule share is 0.812 percent; the largest test share is 1.30 percent.
> Observability Matrix
> observability_matrix is a symmetric 6 by 6 JSON matrix. Rows and columns follow episode order e0 through e5. Diagonal entries are 0. Every off-diagonal entry is a categorical separation margin from 1 through 4:
> | Value | Meaning |
> |---:|---|
> | 1 | Weak separation, normalized margin below 0.75. |
> | 2 | Limited separation, margin from 0.75 up to but not including 1.25. |
> | 3 | Strong separation, margin from 1.25 up to but not including 1.85. |
> | 4 | Very strong separation, margin at least 1.85. |
> Example:
> [[0,3,4,2,3,4],[3,0,2,1,4,3],[4,2,0,3,2,4],[2,1,3,0,3,2],[3,4,2,3,0,4],[4,3,4,2,4,0]]
> The matrix always refers to the submitted three-window plan. Submitting the hidden target matrix with a different plan is not coherent and is scored against the different plan actually submitted.
> Matrix Distribution
> Counts below use the 15 unique off-diagonal entries per matrix.
> | Margin value | Train entries | Test entries |
> |---:|---:|---:|
> | 1 | 1,499 | 1,011 |
> | 2 | 16,636 | 3,401 |
> | 3 | 18,038 | 3,007 |
> | 4 | 35,827 | 7,581 |
> Submission Format
> Write the final CSV to ./working/submission.csv.
> The file must contain exactly these columns in this order:
> | Column | Data type | Required content |
> |---|---|---|
> | `case_id` | string | One exact test identifier. |
> | `window_schedule` | canonical token string | Exactly three distinct valid window IDs separated by `|`. |
> | `observability_matrix` | JSON integer matrix | Symmetric shape `(6, 6)`, zero diagonal, and off-diagonal values from 1 through 4. |
> Example:
> | case_id | window_schedule | observability_matrix |
> |---|---|---|
> | `bw_47f74cfc329d84facfb0` | `w01|w06|w10` | `[[0,3,4,2,3,4],[3,0,2,1,4,3],[4,2,0,3,2,4],[2,1,3,0,3,2],[3,4,2,3,0,4],[4,3,4,2,4,0]]` |
> Include exactly one row for every test ID. Extra columns, reordered columns, duplicate IDs, missing IDs, unknown IDs, blank IDs, and row-count mismatches reject the submission. A single backend-managed visibility column is accepted and removed before schema validation. A schedule longer than 15 characters or a matrix longer than 220 characters is malformed. Malformed row values receive zero for every row-level component.
> Evaluation
> Submissions are evaluated with the Observability Code Score:
> Score = 0.55 * MeasurementPlanScore + 0.40 * MatrixCertificateScore + 0.05 * JointOptimalScore
> Scoring follows three steps:
> The grader measures the usefulness of the three submitted windows.
> It constructs the correct separation matrix for those same three windows and compares it with the submitted matrix.
> It awards a small joint bonus when both the plan and matrix are exactly optimal.
> The grader retains a response catalog R with shape (12,6). Row w represents candidate window w; column e represents episode e. As documented under Packet Response Supervision, each value is built from 0.80 times standardized visible-packet evidence and 0.20 times standardized clean high-resolution response evidence. This catalog is the common reference used for both plan scoring and matrix construction.
> The important dependency is:
> submitted window_schedule
> -> select three rows of R
> -> compute plan utility
> -> construct the expected observability_matrix
> -> compare that expected matrix with the submitted matrix
> Therefore, the matrix is not compared only with the matrix printed in the hidden answer row. It is compared with the matrix implied by the participant's submitted schedule. A useful alternate schedule can score well when its accompanying matrix correctly certifies that alternate schedule.
> MeasurementPlanScore
> For a submitted three-window plan P and episode pair (i,j), define:
> d(i,j,P) = sqrt((1/3) * sum((R[w,i] - R[w,j])^2 for w in P))
> Let D(P) be the 15 distances for all episode pairs. Let redundancy(P) be the mean absolute Pearson correlation among the three selected six-entry response rows. A nonfinite correlation is assigned redundancy 1.
> utility(P) = min(D(P)) + 0.18 * mean(D(P)) - 0.035 * redundancy(P)
> All 12 choose 3 = 220 valid plans are evaluated. Let q(P) be the fraction of those plans whose utility is less than or equal to the submitted plan's utility.
> plan_raw_row = q(P)^2
> For each hidden case i, define its random-plan baseline as:
> c_i = (1/220) * sum(q_i(Q)^2 for every legal plan Q)
> Here, q_i(Q) is the percentile rank of plan Q among the 220 plans for case i. Therefore, c_i is a per-case normalization constant: it is the expected squared-rank score when one of that case's 220 legal plans is chosen uniformly at random.
> Let P_raw be the mean plan_raw_row over all hidden cases, and let P_chance be the mean of c_i over those same cases.
> MeasurementPlanScore = clip((P_raw - P_chance) / (1 - P_chance), 0, 1)
> The correction is applied only after both quantities have been averaged over the hidden set. An optimal plan scores 1, while a uniformly random legal plan has expected score 0 after correction.
> MatrixCertificateScore
> The grader constructs the correct matrix for each submitted plan using the margin thresholds in the Dataset section. For hidden case i, let a_i be the fraction of the 15 unique upper-triangle entries that exactly match the correct matrix for that submitted plan:
> a_i = matching_upper_triangle_entries_i / 15
> Let A be the mean of a_i over all hidden cases. There are four valid off-diagonal categories, so the metric removes the 0.25 agreement expected from uniform category guessing:
> A_corrected = clip((A - 0.25) / 0.75, 0, 1)
> Let M_exact be the mean rate of complete 6 by 6 matrix exact matches for the submitted plans.
> MatrixCertificateScore = 0.90 * A_corrected + 0.10 * M_exact
> Entry chance correction is applied after averaging all test cases.
> JointOptimalScore
> joint_row is 1 only when the submitted plan has maximum utility among all 220 plans and the submitted matrix is exactly correct for that plan. JointOptimalScore is its mean over test cases.
> Minimum score: 0.0.
> Maximum score: 1.0.
> Higher is better. An exact optimal plan with its exact matrix scores 1.0.
> What Makes This Interesting
> This is not damage-state classification and it is not ordinary sensor ranking. A selected window is valuable only through the three-window code it forms with the other selections. The weakest episode pair controls much of the utility, redundant sensors are penalized, and the matrix must explain the submitted plan rather than repeat one fixed label.
> The setup mirrors a real deployment decision: choose a small measurement budget that preserves discrimination before high-bandwidth acquisition is available everywhere. The hidden-catalog grader also recognizes valid alternate plans, which avoids treating one arbitrary canonical schedule as the only acceptable engineering answer.
> What Not To Use
> Do not use case_id, row order, packet order, hashes, path lengths, or split artifacts as predictors.
> Do not match public packets against external copies of the field experiment or build source-state, sensor-name, filename, or waveform lookup tables.
> Do not infer answers from unpublished source metadata, raw state names, sensor coordinates, damage descriptions, or hidden response catalogs.
> Do not exploit duplicate rows, malformed CSV structure, parser behavior, grader feedback, or submission ordering.
> Do not tune or calibrate on withheld test responses through repeated leaderboard probing.
> Hosted or closed-model API calls are not allowed at inference time. Local open-weight models are allowed.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Interleaved API Sequence Disentanglement

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7e8aw97mrc1sxjnhqn54t1a58avmk8
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Interleaved API Sequence Disentanglement
> Overview
> In modern distributed systems, application logs often record events from multiple concurrent user sessions interleaved into a single stream. When a security breach occurs or when debugging complex application states, investigators must reconstruct the exact sequence of actions taken by individual users. However, in many legacy or privacy-restricted systems, user session identifiers are either missing, corrupted, or deliberately redacted.
> In this challenge, you are given a noisy, interleaved event log representing several concurrent user sessions on an e-commerce backend. The data is entirely synthetically generated using a custom Python-based procedural state-machine simulator. The simulator models realistic user navigation flows (searching, viewing items, adding to cart, and checking out) across 5 distinct item categories. To create the dataset, 2 to 4 independent user sessions are randomly generated, assigned overlapping global timestamps, and then interleaved into a single temporal sequence to simulate concurrent server traffic. Finally, the session IDs have been deliberately removed. Your task is to perform causal disentanglement: you must assign every event in the log to a distinct cluster, where each cluster represents a single, valid sequence of user actions (a session).
> To succeed, you must reverse-engineer the latent causal graph of the application's state machine. For example, a user must login before they can view_item, and they can only add_to_cart an item they have recently viewed.
> Target Semantics
> Each row in the dataset represents an "interleaved block" of events.
> Your goal is to predict a cluster ID (an integer 0, 1, 2...) for each event in the block, such that all events belonging to the same original user session share the same cluster ID. The exact number of sessions per block is not known in advance (typically 2 to 4). Because the labels are permutation-invariant, predicting 0,0,1,1 is scored identically to predicting 1,1,0,0.
> Evaluation
> The evaluation metric is the Adjusted Rand Index (ARI), a standard measure for clustering similarity that is invariant to permutations of cluster labels.
> Maximize
> Bounds: [0, 1] (Theoretical negative ARI scores for worse-than-random predictions are explicitly clamped to 0.0 by the grading script).
> The grader computes the ARI for each interleaved block and returns the average ARI across the entire test set. A score of 0.0 represents random assignment, while 1.0 represents perfect recovery of the original sessions.
> File Structure
> **train.csv**: Public training set containing 5,000 rows. Columns: id, events, num_events, cluster_labels.
> **test.csv**: Public test set containing 1,000 rows. Columns: id, events, num_events.
> **sample_submission.csv**: Correct submission format with 1,000 rows. Columns: id, cluster_labels.
> **answers.csv**: Private file containing 1,000 rows for the automated grader. Columns: id, cluster_labels.
> Features
> **id** (Type: string): Unique identifier for the interleaved block. Present in train.csv, test.csv, sample_submission.csv, and answers.csv.
> **events** (Type: string containing JSON array): A JSON-encoded list of event dictionaries. Present in train.csv and test.csv. Each dictionary represents an API action and contains the following JSON data types:
> "timestamp" (integer): A sequential integer representing the time of the event.
> "action" (string): The action type ("login", "search", "view_item", "add_to_cart", "checkout", "logout").
> "category" (string, optional): Present if the action is "search".
> "item_id" (integer, optional): Present if the action is "view_item" or "add_to_cart".
> "cart_size" (integer, optional): Present if the action is "checkout".
> **num_events** (Type: integer): The total number of events in the block. Present in train.csv and test.csv.
> **cluster_labels** (Type: string): A comma-separated list of integers representing the cluster assignment for each event. Present in train.csv (as ground-truth), answers.csv (as ground-truth), and sample_submission.csv (as placeholder predictions initialized to all zeros). Example: "0,1,0,2,1,2". The number of integers must exactly match num_events.
> Submission Format
> Your submission must be a CSV file with exactly two columns: id and cluster_labels. The id must perfectly align with the test.csv rows.
> id,cluster_labels
> test_00000,"0,1,0,1,2,0,2"
> test_00001,"0,0,1,1,1"
> No missing values or NaN are permitted.
> The cluster_labels string must contain exactly num_events comma-separated integers (one cluster ID for each event in the block).
> Restrictions
> External datasets or reverse-lookup of the synthetic generation rules are not permitted.
> The problem must be solved by learning or algorithmically reconstructing the valid state transitions from the training set or logic, not by extracting hidden metadata.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Peptide Assignment for an Uncharacterised Presenting Molecule

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ct81dkeg11x6qrh255d03sd8by02g
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Peptide Assignment for an Uncharacterised Presenting Molecule
> Overview
> A cell advertises what is going on inside it by holding short protein fragments - peptides - in the groove of a presenting molecule on its surface, where passing immune cells can inspect them. Which peptides a given molecule will hold is the question behind transplant matching and behind personalised cancer vaccines, and for the common presenting molecules it is close to settled: decades of experiments have established what each one accepts.
> The case that still stops a lab is a donor carrying a molecule rare enough that nothing has been worked out about it in advance. There is no established model for it and no catalogue of what it accepts. All that exists is the molecule's own groove lining - the 34 residues forming the cleft the peptide sits in - and a short list of peptides that this particular molecule has already been confirmed to hold.
> Work still has to go on from there, because the next batch of candidate peptides is already waiting and each one that goes forward costs a synthesis and an assay. This task is that decision, taken one at a time. You are given the groove lining, the peptides already confirmed for it, and four candidates that were each confirmed on some other donor's molecule. Exactly one of the four is also confirmed for the molecule in front of you. Name it.
> What makes it hard
> All four candidates are genuine confirmed peptides, so asking whether something looks like the sort of fragment that gets held does not separate them, and neither does size, since the four are always the same length. What separates them is whose groove they fit. A groove expresses what it accepts at a small number of positions along the peptide, and which chemistry it wants at those positions is set by the lining rather than by anything about the peptide alone - two linings differing at a handful of residues can want opposite chemistry at the same position. The three candidates that do not belong are drawn from molecules whose linings resemble the one under study, so the near misses are near.
> The evidence is deliberately thin. Four confirmed peptides are enough to see a leaning but not enough to pin it down, so a real share of these decisions stay uncertain even for a specialist. That is the honest state of the problem and the reason the reachable score sits well short of perfect.
> Every molecule in the evaluation records is absent from the training records. That is the transfer being tested: groove linings share residues and share chemistry, so what a system works out about the way a lining shapes what it accepts carries over to a lining it has never seen, while anything memorised about particular molecules does not.
> Data
> The measurements are real. Every confirmed-or-not call behind these records comes from a public compilation of measured peptide-MHC binding experiments released under Apache-2.0, covering more than a hundred presenting molecules. The records here reorganise those measurements into the decision described above, adapting the leave-one-molecule-out transfer setting used in immunopeptidomics - where a method is judged on molecules withheld from its training - into a few-shot form in which the only molecule-specific evidence is the handful of confirmed peptides supplied with each record. Because the underlying calls are experimental rather than generated, the limit on this task is set by the biology and the assays, not by anything added on top.
> Files:
> train.csv - 3,060 records with the answer included, for fitting
> test.csv - 590 records without the answer, the ones you are scored on
> sample_submission.csv - a correctly shaped but deliberately wrong submission, one row per test record, showing the exact two columns and row order expected; it scores 0
> Columns:
> record_id - string, the record identifier, e.g. rec_00007. Present in every file
> groove - string of exactly 34 residue letters, the lining of this molecule's peptide cleft
> observed - string, four peptides already confirmed for this molecule, separated by semicolons
> cand_1, cand_2, cand_3, cand_4 - strings, four candidate peptides between 8 and 14 residues long, all four the same length within a record, in no meaningful order
> presented - string, the one candidate among the four that is also confirmed for this molecule. Present in train.csv only; it is what you predict
> Submission
> Two columns, one row per record in test.csv. The presented column holds the peptide sequence itself, copied from whichever candidate you are naming - not a column name and not a number.
> record_id,presented rec_00007,YLDHEQRDPF rec_00012,GAGGAGGGV rec_00031,IRLPETIDL
> Scoring
> The share of records where the named peptide is the right one, rescaled so that guessing is worth nothing:
> score = max(0, (share_correct - 0.25) / 0.75)
> Scores run from 0 to 1. Because one of four candidates is always correct, a constant answer, a random answer, and any rule that ignores the evidence all sit at 0.
> What not to use
> No external APIs and no network calls at grading time.
> No external datasets. The provided training records are the only permitted source of supervision.
> No training on the evaluation records, including pseudo-labelling them.
> No hardcoded lookups keyed on record_id, and no attempt to fingerprint records by their id.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Larval Electric Field Response Inference

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76dhnnndsrgfc680ybjdrffs8c0e6j
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Larval Electric Field Response Inference
> Overview
> This is a from-scratch scientific signal-modeling challenge about fruit-fly larvae and electric fields.
> Each row represents one short larval behavior episode. A larva was tracked in a behavioral arena while an electric-field stimulus was applied or changed. The original stimulus label is hidden. You are given:
> one compact motion trace of the larva;
> five possible electric-field candidates;
> descriptions of the motion channels and row-local electrode axes.
> Your task is to predict which electric-field candidate caused the motion trace and what kind of biological response the larva showed.
> The answer is one six-part string. It predicts:
> which of five candidate electric fields caused the larval motion response;
> which row-local electrode axis was involved;
> whether the larvaâ€™s response was cathode-directed, anode-directed, or reversing;
> how quickly the larva responded after the field changed;
> how strong the movement response was;
> whether the response stayed stable or reversed/adapted during the episode.
> In plain terms: choose the correct electric-field card and fill in five response labels.
> The source data comes from Drosophila melanogaster electrosensation experiments released through Dryad. In the behavioral part of the study, larvae were recorded in controlled arenas while electric-field conditions were applied. Tracking data from those recordings can be summarized by movement features: forward speed, lateral speed, heading direction, body bending, turning, pausing, path curvature, centroid displacement, and arena-boundary contact. These are the kinds of features stored in motion_strip.
> This prediction is biologically meaningful because electrosensation is about how an animal detects electric-field direction and strength. A model must connect stimulus-like field candidates to movement evidence: for example, a delayed turn, a weak speed change, a strong bend, or a response that switches direction after a field reversal.
> The competition does not expose raw videos, filenames, voltage traces, genotype names, timestamps, source IDs, or original stimulus labels. Instead, each row contains an anonymized 12-channel motion strip and five row-local candidate field cards. Train and hidden test examples come from disjoint source subject groups, so a solution must generalize from motion-response patterns rather than memorizing source records.
> Task
> For every test row, submit exactly one certificate string:
> F03:A2:CATH:L2:G1:R0
> The six fields are:
> field: the active candidate field, one of F01 through F05.
> axis: the row-local electrode axis associated with that field, one of A1, A2, or A3.
> polarity: response direction. CATH means cathode-directed, ANOD means anode-directed, and REV means the response contains a reversal.
> latency: response timing. L0 is the earliest response tier and L4 is the latest response tier.
> drive: response strength. G0 is the weakest movement-drive tier and G3 is the strongest.
> reversal: adaptation/reversal behavior. R0 means little reversal, R1 means moderate reversal/adaptation, and R2 means strong reversal/adaptation.
> Field and axis aliases are row-local. For example, F03 in one row has no relationship to F03 in another row.
> The certificate therefore answers this concrete question:
> Which candidate field caused this larval motion trace, along which anonymized axis, with what direction, timing, strength, and reversal behavior?
> ## **Dataset files**
> `train.csv` contains 4,200 rows.
> - `id`: string. Unique training row ID.
> - `motion_strip`: string. A compact 12 by 96 larval motion-feature strip encoded with 64 printable symbols. It stores the observed motion response for one anonymized larval episode.
> - `strip_shape`: string. Always `12x96`.
> - `field_cards`: JSON list. Five possible electric-field candidates for this row. Exactly one candidate is the hidden active field.
> - `channel_cards`: JSON list. Twelve motion-channel descriptions. These explain what each channel of `motion_strip` represents.
> - `arena_card`: JSON object. Row-level context: frame timing, strip shape, number of field candidates, and row-local axis aliases.
> - `candidate_count`: integer. Always `5`; the number of candidate field cards in the row.
> - `certificate_schema`: string. Always describes the required answer format: `field:axis:polarity:latency:drive:reversal`.
> - `target_certificate`: string. Training-only canonical answer in the same format required for submissions.
> `test.csv` contains 1,200 rows with the same public columns but without `target_certificate`.
> `sample_submission.csv` contains:
> - `id`: string. Test row ID.
> - `predicted_certificate`: string. Empty dummy certificate. The sample scores 0.
> Hidden test rows are balanced across six private scenario families with 200 rows per family.
> Train/test split rule: source subject groups are split before row generation. A subject group used to create a test row is never used to create a training row. Public row IDs are newly hashed after anonymization and do not contain source IDs.
> The possible motion-channel sensor names are:
> - `forward_speed`: forward movement along the larvaâ€™s body axis.
> - `lateral_speed`: sideways movement.
> - `heading_cos`: cosine component of body heading.
> - `heading_sin`: sine component of body heading.
> - `bend_left`: left-bending activity.
> - `bend_right`: right-bending activity.
> - `turn_energy`: turning intensity.
> - `pause_energy`: pausing or reduced-motion activity.
> - `path_curvature`: local curvature of the movement path.
> - `centroid_shift`: displacement of the larval centroid.
> - `boundary_touch`: contact or near-contact with the arena boundary.
> - `group_motion`: pooled motion activity across the episode.
> ## **Input field schemas**
> ### `motion_strip`
> - Type: string.
> - Length: 1,152 characters.
> - Shape: 12 channels by 96 frames.
> - Alphabet: `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_`.
> - Decoding: map each character to an integer from 0 to 63 and reshape row-major into a 12 by 96 matrix.
> - Meaning: larger values represent stronger normalized larval motion-feature activity in that channel and time frame.
> The strip is not a camera image. It is a compact sensor-like representation of motion features such as speed, heading, bending, turning, pausing, and arena-boundary contact.
> ### `field_cards`
> `field_cards` is a JSON list of exactly five objects. Each object has:
> - `field`: string. Row-local field alias, `F01` through `F05`.
> - `axis`: string. Row-local axis alias, `A1`, `A2`, or `A3`.
> - `polarity`: string. Candidate field polarity, `CATH`, `ANOD`, or `REV`.
> - `stimulus_code`: string. A 64-character encoded field-waveform sketch using the same 64-symbol alphabet.
> - `stimulus_shape`: string. Coarse shape descriptor: `ramp`, `pulse`, or `biphasic`.
> - `confidence_tier`: string. Noisy source-calibration tier, `Q0` through `Q3`. This is not a label and high confidence candidates may be decoys.
> - `calibration_score`: number. Noisy normalized support score from source-derived calibration features.
> ### `channel_cards`
> `channel_cards` is a JSON list of exactly twelve objects. Each object has:
> - `channel`: string. Public channel alias, `C01` through `C12`.
> - `sensor`: string. Motion-feature name, such as `forward_speed`, `bend_left`, `turn_energy`, or `path_curvature`.
> - `quality`: string. `clean`, `mixed`, or `noisy`.
> - `lag_sensitive`: boolean. Whether the channel is expected to be useful for latency inference.
> ### `arena_card`
> `arena_card` is a JSON object with:
> - `axis_aliases`: list of objects. The row-local electrode axes available in this row. The aliases are `A1`, `A2`, and `A3`; their physical meaning is intentionally anonymized.
> - `frame_hop_ms`: integer. Milliseconds represented by one strip frame. Always `250`.
> - `strip_shape`: string. Always `12x96`.
> - `candidate_fields`: integer. Always `5`; the number of field cards that can be selected.
> - `source_modality`: string. Short description of the source representation, always a larval motion-feature strip.
> ## **Output grammar**
> Submit one certificate string per row in `predicted_certificate`.
> The full grammar is:
> field:axis:polarity:latency:drive:reversal
> Allowed values:
> - `field`: `F01`, `F02`, `F03`, `F04`, or `F05`.
> - `axis`: `A1`, `A2`, or `A3`.
> - `polarity`: `CATH`, `ANOD`, or `REV`.
> - `latency`: `L0`, `L1`, `L2`, `L3`, or `L4`.
> - `drive`: `G0`, `G1`, `G2`, or `G3`.
> - `reversal`: `R0`, `R1`, or `R2`.
> Valid examples:
> F01:A3:REV:L4:G2:R2 F05:A1:ANOD:L0:G0:R0
> Invalid examples:
> F06:A1:CATH:L2:G1:R0 F01,A1,CATH,L2,G1,R0 {"field":"F01","axis":"A1"}
> Malformed row-level certificates score 0 for that row. Structural CSV errors are rejected.
> ## **Evaluation**
> The grader aligns rows by `id`, never by row order.
> Structural submission errors are rejected. These include missing columns, extra columns, duplicate IDs, unknown IDs, missing IDs, wrong row count, or wrong column order.
> For each valid row, the predicted and hidden certificates are parsed into:
> field, axis, polarity, latency, drive, reversal
> Component scores:
> FieldScore = 1 if predicted field equals hidden field, else 0 AxisScore = 1 if predicted axis equals hidden axis, else 0 PolarityScore = 1 if exact polarity match, 0.25 if the pair is CATH versus ANOD, 0 otherwise LatencyScore = 1 if exact latency tier match, 0.35 if the latency tiers are adjacent, 0 otherwise DriveScore = 1 if exact drive tier match, 0.30 if the drive tiers are adjacent, 0 otherwise ReversalScore = 1 if exact reversal tier match, 0.30 if the reversal tiers are adjacent, 0 otherwise ExactCertificate = 1 if the entire certificate matches exactly, else 0
> The row score is:
> row_score = 0.35 * FieldScore
> 0.12 * AxisScore
> 0.13 * PolarityScore
> 0.13 * LatencyScore
> 0.12 * DriveScore
> 0.08 * ReversalScore
> 0.07 * ExactCertificate
> If `FieldScore` is 0, row_score is capped at 0.30. This prevents a submission from getting most of the score by guessing generic state tiers while missing the binding between the motion strip and the correct field candidate.
> The hidden test set is balanced across six private scenario families:
> - `axis_swap`
> - `weak_drive`
> - `latency_jitter`
> - `polarity_reversal`
> - `crowded_turn`
> - `calibration_conflict`
> Family labels are not included in public files. They are used only for robust scoring.
> The final score is:
> overall_mean = mean(row_score over all hidden rows) worst_family_mean = minimum family mean over the six private families bottom_20_mean = mean(row_score over the lowest-scoring 20% of hidden rows)
> final_score = 0.68 * overall_mean
> 0.22 * worst_family_mean
> 0.10 * bottom_20_mean
> Scores are finite and bounded in `[0, 1]`. The sample submission scores 0. A perfect oracle scores 1.
> Participants can validate syntax locally and train on the public training labels, but cannot exactly compute the hidden score without the private answer file.
> ## **Submission format**
> Submit a CSV with exactly two columns in this order:
> 1. `id`: string. Test row ID from `test.csv`.
> 2. `predicted_certificate`: string. One certificate following the grammar above.
> CSV example:
> id,predicted_certificate 0a12bc34de56f789,F03:A2:CATH:L2:G1:R0
> Do not submit JSON, Python code, multiple certificates, natural-language explanations, or extra columns.
> ## **What not to use**
> Do not use original Dryad filenames, voltages, genotype names, source IDs, timestamps, or row order. These are absent from solver-facing files.
> Do not assume the highest-confidence candidate is true. Calibration tiers and scores are noisy and deliberately include decoys.
> Do not assume a fixed meaning for `F01`, `F02`, `A1`, or `A2`. These aliases are row-local.
> Do not optimize only the easy candidate-choice component. The final score includes worst-family and bottom-20% terms, so weak-drive, latency-jitter, and calibration-conflict cases matter.
> ## **Benchmark boundary**
> Prior work on Drosophila electrosensation studies behavioral attraction, sensory neurons, and calcium responses to electric fields. Standard machine-learning tasks on behavioral data often classify conditions or regress stimulus strength from known experimental metadata.
> This challenge instead removes source stimulus identifiers and asks solvers to bind an anonymized motion response to one of several row-local electric-field candidates, then emit a compact biological response-state certificate. The output is a constrained scientific certificate, not a class label table, free-form text answer, raw trajectory forecast, or sequence transcription.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Material Spectrum Processing Lineage and Invariant-Band Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ems74eb1fwjaa4fy2p18aws8c4bak
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> For each packet of six spectral curves, predict which three curves belong to the same material, place those three in processing order, mark the three spectral regions that remain most stable across the chain, and classify the chain's dominant information-loss pattern.
> A material spectrum records a response value at successive wavelengths. Most source records here are absolute or relative reflectance, with a small number of other spectral measurement forms. Minerals, soils, vegetation, coatings, and other materials produce characteristic curve shapes. Spectral archives often store an original measured curve together with derived products made for later analysis or for comparison with a particular field sensor.
> This challenge uses three processing stages:
> Measured is the original sampled material spectrum.
> Oversampled is the same measurement interpolated onto a finer spectral grid.
> Sensor-convolved is the oversampled curve passed through a standard-resolution sensor response, which smooths nearby wavelengths according to the sensor bandpass.
> Metadata can become detached when such products are exchanged between laboratories or calibration systems. A visually similar spectrum from another material may then be mistaken for a processed descendant. Recovering the correct chain matters because calibration and remote-sensing comparisons are only meaningful when curves describe the same physical sample and their missing support or smoothing history is understood.
> Every case contains the three related stages for one material and three shuffled decoys from other materials in the same broad chapter. Predict these three connected outputs:
> | Output | Prediction |
> |---|---|
> | `lineage_tree` | The measured, oversampled, and sensor-convolved row IDs in that order. |
> | `invariant_band_mask` | A 12-position binary vector marking exactly three stable low-response regions. |
> | `lineage_disposition` | `stable_lineage`, `source_gap`, `sensor_loss`, or `shape_shift`. |
> Dataset
> The prepared cases come from a commercially reusable public archive of laboratory, field, and airborne spectral measurements. It covers several material classes and multiple instruments. Matched source products provide the measured, interpolated, and sensor-response versions of each material record. Full source and licensing details are provided in the raw dataset description.
> There are 1,800 training cases and 450 test cases. Related material-name families stay on one side of the split, and all three decoys are selected from the same split and broad source chapter as the target whenever that chapter has enough candidates.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Three input columns followed by all three target columns for 1,800 cases. |
> | `test.csv` | The three input columns for 450 hidden-label cases. |
> | `sample_submission.csv` | A schema-valid baseline with one row for every test case. |
> | `spectra/*.npz` | Six-row spectral packets referenced by `spectral_path`. |
> CSV Columns
> train.csv contains:
> case_id,spectral_path,measurement_contract,lineage_tree,invariant_band_mask,lineage_disposition
> test.csv contains:
> case_id,spectral_path,measurement_contract
> | Column | Data type | Train | Test | Description |
> |---|---|---:|---:|---|
> | `case_id` | string | yes | yes | Opaque identifier with no material, instrument, chapter, or source-order meaning. |
> | `spectral_path` | path string | yes | yes | Path relative to the prepared dataset root, such as `spectra/s_abc123.npz`. |
> | `measurement_contract` | string | yes | yes | The same packet instruction in every row. It states that rows are S1 through S6, requests measured-to-oversampled-to-sensor order, and requires exactly three stable regions. It contains no case-specific answer. |
> | `lineage_tree` | ordered token string | yes | no | Three unique packet row IDs in processing order. |
> | `invariant_band_mask` | JSON binary vector | yes | no | Length-12 vector containing exactly three values equal to 1. |
> | `lineage_disposition` | categorical string | yes | no | Dominant support or shape condition of the recovered chain. |
> The literal measurement_contract value is:
> The packet contains six rows S1 through S6 on a shared normalized coordinate. Recover the measured to oversampled to sensor-convolved lineage, then mark exactly three stable low-reflectance regions.
> The contract preserves the source builder's historical wording. Within this challenge, low-reflectance means low normalized packet response and is interpreted the same way for every source measurement form.
> Spectral Packet
> Each .npz packet contains:
> | Array | Data type | Shape | Description |
> |---|---|---|---|
> | `curves` | Float16 | `6 x 192` | Normalized spectral curves. Array row 0 is S1 and row 5 is S6. |
> | `valid` | UInt8 | `6 x 192` | Support indicator: 1 where the source product supplies a valid measurement and 0 where it contains missing or sentinel data. |
> Source records come from different instruments and do not share one universal wavelength interval. Each source curve is therefore interpolated onto a normalized 192-position coordinate covering that record's own stored span. Position j represents normalized coordinate j / 191, not a fixed wavelength in nanometers or microns. Physical wavelength files remain part of the raw dataset, but are intentionally not exposed as a common packet axis because their valid ranges differ by record and instrument.
> Before packing, valid source values are scaled using their 5th and 95th percentiles. A small gain, offset, and linear tilt are applied deterministically. The corresponding valid row is interpolated onto the same coordinate and equals 1 only when local source support exceeds 0.75.
> The six rows are shuffled independently in every case. Three rows form the true lineage. The other rows are one measured-stage, one oversampled-stage, and one sensor-convolved curve taken from different materials.
> Lineage Tree
> lineage_tree contains three unique S1 through S6 tokens joined by >:
> <measured row>><oversampled row>><sensor-convolved row>
> For example, S4>S1>S6 means S4 is the measured source, S1 is its oversampled descendant, and S6 is its sensor-convolved descendant.
> Invariant Band Mask
> The 192 positions are divided into 12 consecutive regions of 16 positions. For each region, preparation computes:
> stability = mean_normalized_response_across_three_stages
> + 0.75 * stage_to_stage_standard_deviation
> + 0.50 * mean_missing_support_fraction
> The three regions with the smallest stability values receive 1; the remaining nine receive 0. Low values favor localized low-response regions that remain consistent and well supported across all three processing stages.
> Mask position 0 covers packet coordinates 0 through 15, position 1 covers 16 through 31, and position 11 covers 176 through 191.
> Lineage Disposition
> Let measured_gap and sensor_gap be the missing fractions in the measured and sensor-convolved support rows. Shape correlation is calculated between those two curves only where both are valid. Conditions are applied in this order:
> | Condition | Disposition |
> |---|---|
> | `measured_gap > 0.14` | `source_gap` |
> | otherwise, `sensor_gap - measured_gap > 0.10` | `sensor_loss` |
> | otherwise, overlap is insufficient or correlation `< 0.82` | `shape_shift` |
> | otherwise | `stable_lineage` |
> Training distribution:
> | Disposition | Rows |
> |---|---:|
> | `stable_lineage` | 794 |
> | `source_gap` | 516 |
> | `shape_shift` | 383 |
> | `sensor_loss` | 107 |
> Evaluation
> The metric is the Spectral Lineage Certificate Score:
> Score = 0.45 * TreeScore
> + 0.35 * BandMaskScore
> + 0.20 * DispositionScore
> Minimum possible score: 0.0
> Maximum possible score: 1.0
> Higher scores are better.
> TreeScore
> Let position_similarity be the fraction of the three processing positions containing the correct row ID.
> row_tree_score = 0.30 * position_similarity
> + 0.70 * exact_tree_match
> TreeScore = mean(row_tree_score over test cases)
> Repeated, unknown, or malformed row IDs receive 0 for that case.
> BandMaskScore
> Treat the three positive answer positions as set T and the three submitted positions as set P.
> set_f1 = 2 * |T intersect P| / (|T| + |P|)
> row_mask_score = 0.40 * set_f1 + 0.60 * exact_mask_match
> BandMaskScore = mean(row_mask_score over test cases)
> The mask describes the selected material, so its row score is set to 0 unless the submitted tree contains exactly the correct three row IDs. Their submitted stage order may still be wrong. A malformed mask receives 0.
> DispositionScore
> This component is balanced accuracy over the dispositions present in the hidden answers. For disposition c:
> recall[c] = number of cases with true disposition c predicted as c
> / number of cases with true disposition c
> DispositionScore = mean(recall[c] over hidden-answer dispositions)
> A disposition is counted as correct only when the submitted lineage tree has all three rows in the correct processing order. Otherwise that case is treated as an incorrect disposition prediction.
> Submission Format
> Write the final CSV to:
> ./working/submission.csv
> It must contain exactly these columns in this order:
> case_id,lineage_tree,invariant_band_mask,lineage_disposition
> | Column | Required format |
> |---|---|
> | `case_id` | Every test ID exactly once, with no missing, extra, duplicate, or padded values. |
> | `lineage_tree` | Three unique S1 through S6 tokens joined by `>`; at most 20 characters. |
> | `invariant_band_mask` | JSON length-12 binary vector containing exactly three ones; at most 60 characters. |
> | `lineage_disposition` | Exactly one of `stable_lineage`, `source_gap`, `sensor_loss`, or `shape_shift`. |
> Example:
> case_id,lineage_tree,invariant_band_mask,lineage_disposition
> s_55a0fb90e82587b1eb82,S4>S1>S6,"[0,1,0,0,1,0,0,0,0,1,0,0]",sensor_loss
> The grader rejects extra or reordered columns, duplicate column names, duplicate IDs, missing or unknown IDs, and missing or extra rows. Malformed target values receive zero for the affected component.
> What Makes This Interesting
> Two curves can look similar because they describe the same material, because one is a processed descendant, or because unrelated materials share a broad continuum. Solving the task requires linking three processing stages while rejecting realistic same-domain decoys, then verifying that the selected chain preserves localized spectral evidence.
> Expected And Allowed Methods
> Suitable approaches include compact one-dimensional convolutional encoders, learned metric models, contrastive triplet scoring, permutation heads, and constrained search over six candidates. The short packets are suitable for local CPU training and inference.
> What Not To Use
> Do not derive predictions from case_id, packet names, row order, file sizes, byte hashes, or archive order.
> Do not recover material identities through external source lookup or source filenames.
> Do not exploit hidden split construction, private answers, malformed JSON, duplicate rows, or grader behavior.
> Signal-processing diagnostics may support preprocessing, but final lineage and band decisions must come from a learned model.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Cross-Graph Role Binding Under Ontology Reuse

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx775pdhdwnyymavqst0y8hgad8c43pn
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Ontology engineers frequently reuse a small design pattern inside a much larger domain ontology. Auditing that reuse requires identifying which host entities play the abstract roles defined by the pattern. Names and namespace prefixes are unreliable evidence because projects rename concepts, publish hashed identifiers, or combine several vocabularies.
> Each case provides two incomplete directed graph neighborhoods:
> a pattern-side graph whose custom entities use P tokens;
> a host-ontology graph whose custom entities use H tokens.
> The two node vocabularies are independently generated for every case. Several queried pattern roles are known to cross the reuse boundary, but their host correspondences are hidden. Reconstruct the complete one-to-one binding program.
> This is structured graph correspondence, not pattern classification. The pattern family is supplied, every case contains several simultaneous bindings, and exact node identity is unavailable.
> Graph Representation
> pattern_graph and host_graph are JSON lists of directed triples. Each triple has exactly three string elements:
> source node token;
> relation token;
> destination node token.
> Example triple:
> ["P03","SUBCLASS","P08"]
> Custom pattern nodes begin with P; custom host nodes begin with H. Tokens beginning with TERM_ represent shared RDF, RDFS, OWL, or datatype vocabulary and retain the same meaning on both graph sides. Common relation tokens such as TYPE, SUBCLASS, DOMAIN, and RANGE are also shared. Other predicates use stable REL_ tokens.
> The visible graphs are local neighborhoods. Some edges are independently absent and the host graph contains structurally confusable candidate nodes, so direct triple equality is insufficient.
> Binding Programs
> One binding atom has the form pattern_role=host_node.
> Example:
> P03=H11;P07=H04;P12=H19
> Atoms must be sorted by the numeric P token. Pattern roles and host nodes must each be unique. Every token on the left must come from query_roles; every selected host token should come from candidate_nodes.
> Dataset
> The public dataset contains three CSV files.
> train.csv: 2,019 labeled graph-binding cases from 303 host ontologies.
> test.csv: 367 unlabeled cases from 65 held-out host ontologies.
> sample_submission.csv: one structurally valid example program for every test case.
> All generated views from one host ontology remain in the same partition. Public identifiers and node tokens do not expose source repository paths or original IRIs.
> train.csv Columns
> case_id (string): anonymous unique case identifier.
> pattern_family (string): stable anonymous code for the reused design-pattern family.
> pattern_graph (JSON string): incomplete pattern-side directed triples.
> host_graph (JSON string): incomplete host-ontology directed triples.
> query_roles (string): space-separated pattern nodes requiring bindings.
> candidate_nodes (string): space-separated host nodes available for assignment.
> target_bindings (string): gold one-to-one binding program.
> test.csv Columns
> case_id (string): anonymous unique case identifier.
> pattern_family (string): anonymous design-pattern family code.
> pattern_graph (JSON string): pattern-side directed triples.
> host_graph (JSON string): host-side directed triples.
> query_roles (string): pattern roles requiring bindings.
> candidate_nodes (string): possible host assignments.
> sample_submission.csv Columns
> case_id (string): identifier copied from test.csv.
> predicted_bindings (string): predicted binding program.
> Evaluation
> The score is bounded in [0, 1], where higher is better.
> Score = 0.72 * BindingPairF1 + 0.28 * ExactBindingSetAccuracy
> The weights sum to 1.00, and each component appears once.
> BindingPairF1
> Every P=H atom is treated as a directed correspondence pair. Counts are pooled across all scored cases.
> BindingPairF1 = 2 * TP / (2 * TP + FP + FN)
> A pair is a true positive only when both its pattern role and host node are correct.
> ExactBindingSetAccuracy
> This is the fraction of cases whose predicted correspondence set exactly equals the target set. Pair order does not affect metric identity, although the submission grammar requires sorted atoms.
> Malformed generated programs are treated as empty binding sets for those rows. Structural CSV violations such as missing IDs, duplicate IDs, or extra columns raise an error.
> Submission
> Submit a CSV with exactly two columns.
> Header: case_id,predicted_bindings
> Example row: ONT_1a2b3c4d5e6f70,P03=H11;P07=H04;P12=H19
> Every required test ID must appear exactly once. Additional rows outside the scored answer partition are ignored after required-ID and duplicate-ID validation.
> Allowed And Prohibited Methods
> Allowed
> CPU-compatible graph matching, sparse learning, sequence models, assignment algorithms, and constrained decoding.
> Features derived from directed relations, node neighborhoods, degree profiles, and supplied family codes.
> Host-ontology-disjoint validation built from public examples.
> Prohibited
> Downloading or matching against the source ontology corpus.
> Recovering repository names, original IRIs, or source-path identities.
> Hardcoding test bindings or using an external ontology lookup service.
> Exploiting case IDs, row order, or sample-submission values.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Neuromorphic Readout Recovery Certificate

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7b2xq9kem7vkyskdebq3x4q18c02qt
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Predict how a six-region event sensor should spend six recovery opportunities after readout dead time has suppressed part of its event stream. For every packet, submit the best one-to-one assignment of time slots to regions, a matrix showing the cost of forcing every possible assignment, and an ordering of the time slots from most to least critical.
> Event cameras emit timestamped brightness changes instead of conventional frames. A busy pixel block cannot always report another event immediately. During this dead interval, genuine changes can disappear from the stream. A controller with limited recovery bandwidth cannot revisit every region at every moment, so it needs more than an event-count estimate. It must choose a globally compatible schedule and know how costly each alternative would be.
> The cases originate from measured high-speed calibration recordings. A documented, case-specific dead-time policy is applied to 4 by 4 readout blocks, and suppressed events are removed from the public packet. Training and evaluation use disjoint complete recordings. Region identities and polarity order are permuted independently in each case, preventing fixed sensor coordinates from defining the answer.
> This is a counterfactual readout-planning task rather than event reconstruction. The required outputs form a primal certificate, a forced-choice regret certificate, and a criticality order for the same hidden recovery problem.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | 2,996 labeled recovery cases from 25 source recordings. |
> | `test.csv` | 768 unlabeled cases from 12 held-out source recordings. |
> | `sample_submission.csv` | A schema-valid baseline with one row for every test case. |
> | `event_packets/` | 3,764 unique compressed NumPy evidence packets referenced by the CSV files. |
> CSV Columns
> | Column | Data type | Train | Test | Description |
> |---|---|---:|---:|---|
> | `case_id` | string | yes | yes | Opaque case identifier with no recording, time, or sensor-coordinate meaning. |
> | `event_packet_path` | path string | yes | yes | Path relative to the prepared dataset root, such as `event_packets/abc123.npz`. |
> | `recovery_matching` | ordered token string | yes | no | The optimal one-to-one assignment of T1 through T6 to R1 through R6. |
> | `forced_loss_matrix` | JSON integer matrix | yes | no | A 6 by 6 counterfactual regret code with values from 0 through 3. |
> | `critical_slot_order` | ordered token string | yes | no | A permutation of T1 through T6 from highest to lowest assignment criticality. |
> train.csv contains the two input columns followed by the three targets. test.csv contains only case_id and event_packet_path.
> Event Packet
> Each packet describes the retained portion of one non-overlapping 1,000-event source slice.
> | Array key | Data type and shape | Meaning |
> |---|---|---|
> | `observed_counts` | Float16, `2 x 6 x 6` | Retained-event counts by polarity, time cell, and packet-local region, log-scaled into 0 through 1. |
> | `fine_activity` | Float16, `2 x 12 x 6` | A twelve-bin retained-event histogram for resolving short bursts. |
> | `observed_intervals` | Float16, `2 x 6 x 6` | Mean intervals between retained events in each polarity, time, and region cell. |
> | `inter_event_quantiles` | Float16, length 16 | Quantiles of consecutive retained-event gaps. |
> | `dead_time_profile` | Float16, length 6 | The six packet-local dead-time settings divided by 20,000 microseconds. |
> Rows of every 6 by 6 grid are T1 through T6. Columns are R1 through R6. Regions are obtained from a 2 by 3 spatial partition and then assigned a fresh local permutation for each case.
> Hidden Recovery Burden
> The preparation process retains an event only when its 4 by 4 block and polarity key has been live for at least the configured regional dead time. Suppressed events define four hidden properties in each time-region cell: rejected-event count, polarity imbalance, microburst concentration, and repeated use of the same readout blocks. Each property is tied-rank normalized across the 36 cells.
> burden[t,r] = 0.34 * count_rank
> + 0.28 * polarity_imbalance_rank
> + 0.22 * microburst_concentration_rank
> + 0.16 * repeated_block_rank
> + 0.0001 * log(1 + rejected_count)
> The small final term gives a deterministic preference when the four rank components tie.
> Recovery Matching
> A valid matching assigns every time slot to exactly one region and uses every region exactly once. For a permutation p of the six regions:
> utility(p) = sum from t=1 to 6 of burden[t, p(t)]
> recovery_matching is the permutation with maximum utility. Exact ties use lexicographic region order. Tokens are written in time order, for example:
> T1~R6>T2~R3>T3~R5>T4~R2>T5~R4>T6~R1
> Forced Loss Matrix
> Let U* be the utility of the optimal matching. For every pair (Ti,Rj), optimize the other five assignments while forcing Ti to use Rj. The continuous forced loss is:
> loss[i,j] = U* - best utility subject to Ti~Rj
> The six selected edges always have loss 0. An additional edge can also have loss 0 when it belongs to a tied optimal matching. Positive losses are divided at their within-case one-third and two-third quantiles:
> | Code | Meaning |
> |---:|---|
> | `0` | Forcing the edge does not reduce optimal utility. |
> | `1` | Low positive loss. |
> | `2` | Medium positive loss. |
> | `3` | High positive loss. |
> Rows follow T1 through T6 and columns follow R1 through R6.
> Critical Slot Order
> For each time slot, find the smallest forced loss among its five non-selected regions. A large minimum means that every alternative assignment is costly. critical_slot_order ranks T1 through T6 by this value from largest to smallest, with time number breaking exact ties.
> Example labeled syntax:
> case_id,event_packet_path,recovery_matching,forced_loss_matrix,critical_slot_order
> er_example,event_packets/example.npz,T1~R6>T2~R3>T3~R5>T4~R2>T5~R4>T6~R1,"[[1,1,1,3,2,0],[3,1,0,2,3,2],[1,2,2,2,0,1],[1,0,2,3,1,3],[3,3,2,0,2,3],[0,2,3,3,1,1]]",T5>T2>T4>T1>T3>T6
> The row illustrates the grammar and is not a public case.
> Evaluation
> The metric is the Readout Recovery Certificate Score:
> Score = 0.38 * MatchingScore
> + 0.42 * ForcedLossScore
> + 0.20 * CriticalOrderScore
> MatchingScore
> Let a be the fraction of the six time positions assigned to the correct region.
> case_score = 0.72 * a + 0.28 * exact_matching
> MatchingScore = mean(case_score over test cases)
> ForcedLossScore
> For answer entry Y[i,j], set w[i,j] = 2 when the answer is 2 or 3 and w[i,j] = 1 otherwise. With prediction P:
> weighted_agreement = sum(w[i,j] * I(Y[i,j] = P[i,j])) / sum(w[i,j])
> case_score = 0.78 * weighted_agreement + 0.22 * exact_matrix
> ForcedLossScore = mean(case_score over test cases)
> CriticalOrderScore
> Six time slots define 15 unordered pairs. Pairwise concordance is the fraction of pairs whose relative order matches the answer.
> case_score = 0.76 * pairwise_concordance + 0.24 * exact_order
> CriticalOrderScore = mean(case_score over test cases)
> A malformed value receives 0 for its component on that case. A structurally invalid CSV is rejected before scoring.
> Minimum possible score: 0.0
> Maximum possible score: 1.0
> Higher scores are better.
> Submission Format
> Write the final CSV to:
> ./working/submission.csv
> It must contain exactly these columns in this order:
> case_id,recovery_matching,forced_loss_matrix,critical_slot_order
> | Column | Required format |
> |---|---|
> | `case_id` | Every test ID exactly once, with no missing, extra, duplicate, or padded values. |
> | `recovery_matching` | Six `Ti~Rj` tokens in T1 to T6 order, joined by `>`; every region used once; at most 48 characters. |
> | `forced_loss_matrix` | JSON 6 by 6 integer matrix with entries from 0 through 3; at most 180 characters. |
> | `critical_slot_order` | Every token T1 through T6 exactly once, joined by `>`; at most 24 characters. |
> Example:
> case_id,recovery_matching,forced_loss_matrix,critical_slot_order
> er_example,T1~R6>T2~R3>T3~R5>T4~R2>T5~R4>T6~R1,"[[1,1,1,3,2,0],[3,1,0,2,3,2],[1,2,2,2,0,1],[1,0,2,3,1,3],[3,3,2,0,2,3],[0,2,3,3,1,1]]",T5>T2>T4>T1>T3>T6
> A wrong or reordered schema, an extra column, duplicate column names, missing or extra rows, and duplicate or unknown IDs reject the submission.
> What Not To Use
> Do not derive predictions from case IDs, packet filenames, file sizes, hashes, row order, or archive order.
> Do not match packets against external raw recordings, source filenames, camera settings, timestamps, or event-stream fingerprints.
> Do not use exact-event, histogram-hash, or nearest-source lookup against an external copy of the measurements.
> Do not exploit private answers, hidden files, malformed CSV handling, duplicate rows, or grader implementation details.
> Do not call hosted or closed-model APIs during inference. Local CPU models and event-processing algorithms are allowed.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Gamma Field Fingerprint Inference

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70kspyn155b5eh23m992mjmd8c5f31
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Gamma Field Fingerprint Inference
> Overview
> This is a from-scratch scientific signal-modeling challenge. Each row shows a compact gamma-ray spectrum sketch from a simulated field measurement. Your task is to infer a five-part fingerprint describing what the spectrum most likely came from and how the measurement was degraded.
> In plain terms: read the 128-bin spectrum, compare it with six anonymous candidate material cards, and submit one compact answer string with:
> the candidate card that best explains the spectrum;
> the coarse assay tier of that candidate;
> the shielding tier that suppressed the low-energy region;
> the detector gain-drift tier that shifted spectral peaks;
> the background-continuum tier.
> A valid answer looks like this:
> C04:F3:S2:D-1:B2
> The source data are reference gamma spectra for nuclear-safeguards applications. Gamma spectroscopy is a non-destructive assay method: instruments record photon energy counts, and analysts use peak patterns, continuum background, detector response, shielding, and measurement time to reason about material composition and field conditions.
> The public rows are not exact source spectra. The preparation script creates source-disjoint, degraded field sketches by applying low-energy attenuation, detector-gain drift, background ridges, count noise, detector-transfer blur, and controlled mixture with non-target spectra. The row-local candidate aliases (C01 through C06) are regenerated independently for every row. Direct source lookup by filename, row order, or source identifier is not useful because those identifiers are absent and the scored fingerprint is tied to the generated field sketch.
> This is not classification, regression, sequence-to-sequence translation, or source-spectrum retrieval. The output is a constrained scientific fingerprint over row-local candidates and ordinal field-state tiers.
> Dataset files
> train.csv contains 3,120 rows. There are 520 rows from each of six generation families.
> id: string. Unique training row ID.
> spectrum_code: string. Encoded 128-bin degraded gamma-spectrum sketch.
> spectrum_shape: string. Always 128.
> candidate_cards: JSON list. Six anonymous candidate material cards for this row.
> detector_card: JSON object. Coarse detector and acquisition metadata for this row.
> field_card: JSON object. Noisy public hints about attenuation, gain stability, and continuum conditions.
> max_candidates: integer. Always 6.
> fingerprint_schema: string. Always candidate:assay:shield:drift:background.
> target_fingerprint: string. Training-only answer in the required output grammar.
> test.csv contains 960 hidden rows. There are 160 rows from each of six private generation families. It has the same public columns as train.csv but omits target_fingerprint.
> sample_submission.csv contains:
> id: string. Test row ID.
> predicted_fingerprint: string. Empty dummy prediction. The sample is structurally valid and scores 0.
> Input field schemas
> spectrum_code is a string of exactly 128 characters. Decode each character using this alphabet:
> 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_
> Each character maps to an integer from 0 to 63. The decoded vector is a low-resolution log-count spectrum. Larger values indicate stronger normalized spectral energy in that energy/channel bin. The bins are ordered from low channel/energy to high channel/energy.
> Each candidate_cards value is a JSON list of exactly six objects. Each object has:
> candidate: string. Row-local candidate alias, one of C01 through C06.
> material_code: string. Coarse anonymous material family code: alpha, beta, mixed, or unknown.
> compound_code: string. Coarse compound descriptor normalized from source metadata.
> composition_sketch: list of six integers. Rounded abundance indicators on a 0-to-99 scale. The entries are intentionally not named as real isotopes.
> assay_hint: string. Noisy coarse assay hint, one of F0 through F4; it may be adjacent to the true assay tier and should not be treated as an answer key.
> count_scale_hint: string. Coarse source count-scale bucket: tiny, small, medium, large, or huge.
> Example candidate card:
> {"candidate":"C04","material_code":"mixed","compound_code":"puo2_uo2","composition_sketch":[1,5,62,18,3,0],"assay_hint":"F3","count_scale_hint":"large"}
> detector_card is a JSON object with:
> resolution_code: string. Coarse detector-response class: sharp, medium, broad, coarse, or unknown.
> channel_bucket: string. Coarse source channel-count bucket: low, mid, or high.
> live_time_tier: string. Coarse acquisition live-time bucket: short, medium, long, or very_long.
> count_budget: string. Coarse total-count bucket: tiny, small, medium, large, or huge.
> field_card is a JSON object with noisy generated condition hints:
> acquisition_mode: string. Coarse measurement mode label: bench, portable, field, or screening.
> low_energy_shadow_hint: string. Noisy hint for low-energy attenuation: low, mixed, or high.
> gain_stability_hint: string. Noisy hint for peak drift: stable, minor, or wandering.
> continuum_hint: string. Noisy hint for background continuum: quiet, textured, or busy.
> These hints are deliberately noisy. They help but do not determine the target tiers.
> Output grammar
> Submit one fingerprint string per row in the predicted_fingerprint column.
> The grammar is:
> candidate:assay:shield:drift:background
> Allowed values:
> candidate: one of C01, C02, C03, C04, C05, or C06 from that row.
> assay: one of F0, F1, F2, F3, or F4.
> shield: one of S0, S1, S2, or S3.
> drift: one of D-2, D-1, D0, D+1, or D+2.
> background: one of B0, B1, B2, or B3.
> Valid examples:
> C01:F0:S0:D0:B0
> C06:F4:S3:D+2:B3
> C03:F2:S1:D-1:B2
> Invalid examples:
> C07:F2:S1:D0:B1 C03:F5:S1:D0:B1 C03:F2:S1:D3:B1 {"candidate":"C03"}
> ## **Evaluation**
> Structural submission errors are rejected. Structural errors include missing columns, extra columns, wrong column order, duplicate IDs, missing IDs, unknown IDs, and wrong row count.
> Malformed row-level fingerprints score 0 for that row instead of crashing the grader. Rows are aligned by `id`, never by row order.
> For each valid row, the grader compares the predicted fingerprint to the hidden target fingerprint.
> Definitions:
> CandidateExact = 1 if predicted candidate equals true candidate, else 0 ExactFingerprint = 1 if the full normalized fingerprint equals the hidden target, else 0
> Ordinal tier scores use adjacent-tier partial credit:
> AssayScore = 1.00 if assay tier is exact = 0.35 if assay tier is one step away = 0.00 otherwise
> ShieldScore = 1.00 if shield tier is exact = 0.30 if shield tier is one step away = 0.00 otherwise
> DriftScore = 1.00 if drift tier is exact = 0.35 if drift tier is one step away in [D-2, D-1, D0, D+1, D+2] = 0.00 otherwise
> BackgroundScore = 1.00 if background tier is exact = 0.25 if background tier is one step away = 0.00 otherwise
> The row score is:
> raw_row_score = 0.40 * CandidateExact
> 0.20 * AssayScore
> 0.14 * ShieldScore
> 0.12 * DriftScore
> 0.09 * BackgroundScore
> 0.05 * ExactFingerprint
> if CandidateExact == 0: row_score = min(raw_row_score, 0.28) else: row_score = raw_row_score
> The candidate cap prevents a submission from earning a high score by predicting field-state tiers while binding the spectrum to the wrong candidate card.
> The hidden rows are balanced across six private generation families:
> - `low_energy_absorber`
> - `gain_drift`
> - `low_count_field`
> - `mixed_material`
> - `detector_transfer`
> - `background_ridge`
> Family labels are not included in solver-facing files. They are used only by the grader for robust aggregation.
> For each family:
> family_mean = mean(row_score for hidden rows in that family)
> Then:
> worst_family_mean = minimum family_mean over the six families bottom_20_mean = mean(row_score over the lowest-scoring 20% of hidden rows)
> The final score is:
> final_score = 0.65 * mean(row_score over all hidden rows)
> 0.25 * worst_family_mean
> 0.10 * bottom_20_mean
> Scores are finite and bounded in `[0, 1]`. The sample submission scores 0. A perfect oracle scores 1.
> ## **Submission format**
> Submit a CSV file with exactly two columns in this order:
> 1. `id`: string. Test row ID from `test.csv`.
> 2. `predicted_fingerprint`: string. One fingerprint following the grammar above.
> Example:
> id,predicted_fingerprint 0a12bc34de56f789,C04:F3:S2:D-1:B2
> Do not submit JSON, Python code, multiple candidates, probability vectors, extra columns, or natural-language explanations.
> ## **What not to use**
> Do not use source filenames, source spectrum IDs, source archive order, acquisition dates, certificate paths, provider names, or exact isotope labels. These are absent from solver-facing rows and are not stable row semantics.
> Do not assume `assay_hint`, `field_card`, material-code frequency, candidate order, or row ID directly gives the answer. These are noisy or row-local.
> Do not train on private source groups or try to reconstruct hidden answers from the raw source archive. Train and hidden test rows are source-group-disjoint, and public rows are degraded counterfactual field sketches rather than exact source spectra.
> Do not optimize only for candidate matching. The final score also rewards the field-state tiers, worst-family robustness, and bottom-tail performance.
> ## **Resource limit**
> Solutions should run on 10 CPU cores with 62.5 GiB RAM in at most 90 minutes. No GPU is required or expected.
> ## **Benchmark boundary**
> Standard gamma-spectroscopy benchmarks often classify radionuclides, estimate isotope abundance from known spectra, or compare analysis software against reference measurements. This challenge is different: it gives a generated field sketch, six anonymous row-local candidate cards, and noisy acquisition hints, then asks for a compact fingerprint that binds material identity to shielding, gain drift, and background conditions. The benchmark therefore tests source-disjoint scientific signal modeling and constrained fingerprint inference, not ordinary isotope classification, regression, or spectrum lookup.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Acoustic Event Lifecycles in Unseen Rooms

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx757zqka41c5ggd4gj3bt1x7h8bzyn5
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Predict which sound events occur in each three-second, four-channel indoor
> recording, when every event begins and ends, and where each event is located as
> it moves. The scenes contain recognizable sounds such as speech, laughter,
> clapping, telephones, footsteps, doors, music, running water, bells, and knocks.
> The four synchronized channels preserve directional information from the
> recording space. For every detected event, predict its category, its active
> 200 ms time interval, and its azimuth, elevation, and distance near the event's
> beginning, midpoint, and end. These three positions form the event's short
> motion summary.
> Several events may overlap, two events of the same category may occur at once,
> and an event may move while active. Test recordings come from indoor rooms not
> represented in training. This room-held-out setting reflects applications such
> as robot auditory awareness, assistive monitoring, and smart-room systems that
> must understand unfamiliar acoustic environments.
> Task
> For every three-second test recording, return zero through eight passage
> entries. Each entry must recover all of the following:
> one category code;
> the first occupied 200 ms bin;
> the exclusive ending bin;
> three circular horizontal-direction codes;
> three vertical-direction codes; and
> three range codes.
> An occurrence remains one entry while it is contiguous. A silence gap longer
> than 200 ms separates two occurrences, even when both have the same category.
> Dataset
> The public package contains 800 labeled training recordings and 400 test
> recordings. Every WAV file has these properties:
> four channels;
> signed 16-bit PCM;
> 12,000 samples per second;
> 36,000 frames; and
> exactly three seconds of audio.
> The four channels preserve directional acoustic evidence. Training and test
> use different recording spaces.
> Public Files
> train.csv contains 800 labeled rows. It includes the input fields and the
> correct answer_json event ledger.
> test.csv contains 400 unlabeled rows with the same input fields but no
> answer_json column.
> sample_submission.csv contains one deterministic pseudo-random valid
> prediction for every test ID. It demonstrates syntax only and is not a
> baseline solution.
> audio/ contains the four-channel WAV recordings referenced by train.csv
> and test.csv.
> Input Columns
> id is an opaque string identifying one row.
> audio_path is the path to that row's WAV file, relative to the public
> directory.
> prompt is a short text reminder of the prediction objective.
> sample_rate is an integer and is always 12000.
> duration_seconds is a number and is always 3.0.
> answer_format_json is a JSON string describing the required target fields
> and value ranges.
> answer_json is the labeled training target. It appears only in
> train.csv.
> Ledger Format
> answer_json is an object containing exactly one key named tracks. The value
> is an unordered list of zero through eight objects. The key name tracks is
> part of the required file grammar; each object represents one passage entry.
> {
> "tracks": [
> {
> "class_id": 4,
> "onset_bin": 2,
> "offset_bin": 11,
> "azimuth": [7, 8, 10],
> "elevation": [3, 3, 4],
> "distance": [2, 2, 3]
> }
> ]
> }
> Every passage object must contain exactly these fields:
> class_id: one integer from 0 through 12.
> onset_bin: one integer from 0 through 14.
> offset_bin: one integer from 1 through 15, strictly greater than
> onset_bin.
> azimuth: exactly three integers, each from 0 through 23.
> elevation: exactly three integers, each from 0 through 7.
> distance: exactly three integers, each from 0 through 7.
> Category Codebook
> The 13 valid category codes are:
> 0: female speech;
> 1: male speech;
> 2: clapping;
> 3: telephone;
> 4: laughter;
> 5: domestic sounds;
> 6: walking or footsteps;
> 7: door opening or closing;
> 8: music;
> 9: musical instrument;
> 10: water tap or faucet;
> 11: bell; and
> 12: knock.
> Time Quantization
> The recording is divided into fifteen 200 ms bins. A passage occupies every
> bin t satisfying:
> onset_bin <= t < offset_bin
> Isolated single-frame annotations are not represented in the ledger.
> Spatial Quantization
> The three values in every spatial list correspond to the beginning, midpoint,
> and end of that passage's observed lifetime.
> Azimuth uses 24 circular bins of 15 degrees. Bin 0 begins at -180 degrees,
> and the codebook wraps between bins 23 and 0.
> Elevation uses the seven boundaries:
> [-65, -50, -35, -20, -5, 10, 25] degrees
> Bin 0 lies below -65 degrees. Bins 1 through 6 are the half-open
> intervals between adjacent boundaries, and bin 7 begins at 25 degrees. There
> are exactly eight elevation bins, numbered 0 through 7; therefore the
> largest possible elevation-bin error is seven.
> Distance uses these centimeter boundaries:
> [100, 130, 160, 190, 220, 260, 330]
> Bin 0 lies below 100 cm, and bin 7 begins at 330 cm.
> There are exactly eight distance bins, numbered 0 through 7; therefore the
> largest possible distance-bin error is seven.
> Submission Format
> Submit exactly these columns, in this order:
> id,answer_json
> row_0123456789abcdefabcd,"{""tracks"":[{""class_id"":4,""onset_bin"":2,""offset_bin"":11,""azimuth"":[7,8,10],""elevation"":[3,3,4],""distance"":[2,2,3]}]}"
> Every test ID must occur exactly once. Row order and passage order do not
> affect scoring. A valid empty ledger is {"tracks":[]}.
> The complete submission is rejected with score 0 for wrong, missing,
> additional, duplicated, or reordered columns; blank, duplicated, missing, or
> unknown IDs; malformed JSON; missing or extra object keys; non-integer values;
> out-of-range values; spatial lists of the wrong length; repeated identical
> passage objects; or more than eight entries in one ledger.
> Evaluation
> Predicted and true passages are compared as structured objects and then paired
> using a maximum-total-score one-to-one assignment.
> Passage-Pair Similarity
> For predicted passage p and true passage t:
> C is 1 when their category codes agree and 0 otherwise.
> T is intersection-over-union of their half-open time intervals.
> A is mean horizontal similarity across the three waypoints. At one waypoint it is 1 - circular_distance / 12, using the shorter distance on
> the 24-bin circle.
> E is mean vertical similarity, with waypoint similarity 1 - absolute_error / 7.
> D is mean range similarity, also using 1 - absolute_error / 7.
> S = 0.55 A + 0.225 E + 0.225 D.
> G = (0.25 + 0.75 C) (0.50 + 0.50 T).
> The pair score is:
> P = 0.35 C + 0.25 T + 0.40 S G
> Recording Score
> Let M be the optimal assignment total divided by the larger of the predicted
> and true passage counts. Every unmatched passage contributes zero.
> The count agreement term is:
> N = max(0, 1 - |number_predicted - number_true| / max(number_predicted, number_true, 1))
> Let X equal 1 only when the complete normalized ledgers are identical and
> 0 otherwise.
> R = 0.10 N + 0.78 M + 0.12 X
> Final Score
> The private test set defines three robustness axes:
> number of passages: 1, 2, 3-4, or 5-8;
> displacement behavior: static, mobile, or sweeping; and
> median range: near, mid, or far.
> For each axis, the evaluator keeps the lowest group mean among groups with at
> least five rows. Call these values W_count, W_motion, and W_range.
> Score = 0.82 mean(R) + 0.06 W_count + 0.06 W_motion + 0.06 W_range
> Scores are bounded in [0,1], and higher is better. A perfect submission
> scores exactly 1.
> Expected Approach
> Useful systems may combine CPU multichannel spectral descriptors,
> cross-channel phase and level relationships, temporal occurrence proposals,
> category recognition, waypoint regression, count estimation, and constrained
> ledger assignment. Predicting each time bin independently does not by itself
> produce the required occurrence lifecycles.
> Training, fine-tuning, feature extraction, and inference must run on CPU.
> What Not To Use
> Do not use GPU acceleration.
> Do not use external recordings, external annotations, answer lookups, or hosted identification services.
> Do not use private answers, grader internals, manual test labeling, leaderboard probing, hosted inference, or hardcoded test outputs.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Censored Acoustic Buffer Frontier Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72nzx7cpe3f4yrveysxp4fcn8c0tjx
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat pvduy's score of 0.319!

Full challenge description from page:

> Leaderboard
> (21)
> Your Submissions
> Overview
> Recover the complete decision frontier of six recording-buffer policies when the decisive part of a measured transient is missing. For each waveform packet, predict the ordered policies that are optimal for a nonzero range of operating preferences, the preference bins where the optimum changes, and the non-optimal policies that remain close enough to serve as reserves.
> Triggered structural monitors have finite memory. An early buffer preserves sharp onset evidence, while a late buffer preserves decay and reverberation. Operators may change the balance between those two objectives after deployment, so selecting one fixed window is insufficient. They need the upper envelope of all candidate policies: which policy wins first, which takes over next, exactly where each takeover occurs, and which alternatives remain nearly competitive.
> The critical 768-sample interval is withheld to model buffer rollover, detector dead time, or an unreadable acquisition block. Public evidence contains the measured context on both sides, its first difference, a visibility mask, and the six packet-local candidate placements. The waveforms come from controlled contact-transducer and non-contact optical-vibration experiments. Source acquisition groups are held out between training and evaluation.
> This task does not ask for an event timestamp or sound-event class. It asks a model to reconstruct a continuous piecewise-linear acquisition-policy frontier from censored physical evidence.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | 3,224 labeled waveform-policy cases. |
> | `test.csv` | 483 hidden-label cases from held-out acquisition groups. |
> | `sample_submission.csv` | A schema-valid baseline containing every test ID. |
> | `trace_packets/` | 3,707 unique compressed NumPy packets. |
> train.csv contains case_id, trace_packet_path, frontier_chain, switch_bin_word, and reserve_policy_set.
> test.csv contains only case_id and trace_packet_path.
> CSV Columns
> | Column | Data type | Train | Test | Meaning |
> |---|---|---:|---:|---|
> | `case_id` | string | yes | yes | Opaque identifier with no sensor, source, time, or policy meaning. |
> | `trace_packet_path` | relative path string | yes | yes | Location of one `.npz` packet under `trace_packets/`. |
> | `frontier_chain` | ordered token string | yes | no | Distinct policies on the continuous upper envelope from onset priority to decay priority. |
> | `switch_bin_word` | ordered token string | yes | no | Quantized preference location of every adjacent frontier takeover. |
> | `reserve_policy_set` | canonical token set | yes | no | Never-optimal policies whose minimum regret is at most 0.04. |
> Trace Packet
> Each packet contains trace, a Float16 array with shape 3 x 3072, and policy_starts, an Int16 array of length 6.
> | `trace` row | Meaning |
> |---:|---|
> | `0` | Robustly normalized measured waveform, with the withheld interval replaced by zero. |
> | `1` | First difference of row 0, also zero through the withheld interval. |
> | `2` | Visibility mask: 1 for observed samples and 0 for the withheld samples. |
> policy_starts[k] gives the start of policy P{k+1} inside the 768-sample hidden interval. Every policy retains a 384-sample window. Policy identities are independently permuted in each case, so P1 does not consistently mean early or late.
> Hidden Policy Utilities
> For each candidate window, onset capture is the retained fraction of first-difference energy concentrated at or before the strongest hidden transient. Decay capture is the retained fraction of waveform energy concentrated at or after that transient. Evidence on the opposite side receives weight 0.05.
> For operating preference q between 0 and 1, utility(policy,q) = (1-q) * onset_capture(policy) + q * decay_capture(policy).
> Every policy therefore defines a line over q. The target frontier is the upper envelope of those six lines.
> Frontier Chain
> frontier_chain lists every policy that is uniquely optimal over a positive-width interval, in increasing q order. Repeated policies are not allowed. A one-policy frontier is valid.
> Example: P1>P3>P6 means P1 is initially optimal, P3 takes over at the first switch, and P6 is optimal for the final preference interval.
> Switch Bin Word
> A chain of length m has exactly m-1 switch tokens. Divide the preference interval into 16 equal bins. B00 represents [0/16,1/16), B01 represents [1/16,2/16), and so on; B15 includes the right endpoint 1. Tokens must be in nondecreasing order and joined by >. A one-policy chain uses none.
> Example: chain P1>P3>P6 with B04>B11 changes near preferences 0.25 and 0.69.
> Reserve Policy Set
> Evaluate all six policy utilities at 33 evenly spaced preferences from 0 through 1. A policy is a reserve when it never appears on the frontier but comes within 0.04 utility of the best policy at least once. List reserve policies in sorted order with |, or use none. Frontier and reserve policies must be disjoint.
> Submission Format
> Write the final CSV to ./working/submission.csv. It must contain exactly case_id, frontier_chain, switch_bin_word, and reserve_policy_set, in that order.
> | Column | Required format |
> |---|---|
> | `case_id` | Every test ID exactly once, with no missing, extra, duplicate, or padded values. |
> | `frontier_chain` | One through six unique P1 through P6 tokens joined by `>`; at most 17 characters. |
> | `switch_bin_word` | `none` or zero through five B00 through B15 tokens joined by `>`; at most 19 characters. |
> | `reserve_policy_set` | `none` or sorted unique P1 through P6 tokens joined by `|`; at most 17 characters. |
> | case_id | frontier_chain | switch_bin_word | reserve_policy_set |
> |---|---|---|---|
> | `bf_example` | `P1>P3` | `B12` | `P4|P6` |
> The switch count must equal the submitted chain length minus one. Frontier and reserve policies must be disjoint. Extra or reordered columns, duplicate column names, missing or extra rows, and duplicate or unknown IDs reject the submission. Malformed bounded target values receive zero for their component.
> Evaluation
> The Acoustic Buffer Frontier Score is 0.45 * FrontierChainScore + 0.35 * SwitchLocationScore + 0.20 * ReserveSetScore.
> Every component is averaged separately over hidden Laser and PZT cases, then those two sensor-family means are averaged. This prevents the more numerous contact-transducer cases from dominating evaluation.
> Minimum score: 0.0
> Maximum score: 1.0
> Higher scores are better.
> FrontierChainScore
> Token edit similarity is 1 - Levenshtein_distance(Y,P) / max(|Y|,|P|,1), where tokens are policy IDs. The case score is 0.20 * token_edit_similarity + 0.80 * exact_chain_match.
> SwitchLocationScore
> The submitted switch count must be coherent with the submitted chain. If hidden and submitted switch counts match, local similarity is the mean of max(0, 1 - |hidden_bin - submitted_bin| / 4) over corresponding switches. If the counts differ, local similarity is 0. Two empty switch words have local similarity 1.
> The case score is 0.25 * local_similarity + 0.75 * exact_switch_word_match.
> ReserveSetScore
> For hidden set Y and submitted set P, set F1 is 2 * |Y intersect P| / (|Y| + |P|). Two empty sets receive 1 and exactly one empty set receives 0. The case score is 0.30 * set_F1 + 0.70 * exact_set_match.
> What Makes This Interesting
> The prediction object is a latent upper envelope, not a timestamp, waveform reconstruction, or event label. One wrong estimate of hidden onset or decay energy can change the number of frontier policies, their order, and several switch locations. The reserve set adds a separate near-optimality question: a policy can be absent from the envelope yet remain operationally valuable under small model error.
> The benchmark connects censored-signal inference with robust acquisition planning. A useful model must recover enough hidden physics to support decisions across an entire continuum of operator preferences rather than optimize one fixed objective.
> Expected And Allowed Methods
> Suitable CPU methods include compact one-dimensional convolutional networks, spectral and wavelet features, masked-signal encoders, sensor-specific calibration, utility regression followed by upper-envelope decoding, and direct structured prediction. The candidate frontier search itself is small; the learning problem is inferring hidden policy utilities from visible physical context.
> What Not To Use
> Do not derive predictions from case IDs, packet names, file sizes, hashes, row order, or source acquisition order.
> Do not match packets against external waveform archives, source filenames, trigger clocks, or sensor-family paths.
> Do not use exact-waveform, perceptual, or spectral-fingerprint lookup against an external copy of the measurements.
> Do not exploit malformed submissions, private files, hidden answers, or leaderboard probing.
> Do not call hosted or closed-model APIs during inference. Local CPU signal processing and locally executed models are allowed.
> Reference Validation
> Exact answers score 1.0. The schema-valid sample scores 0.112308, and a whole-column mode baseline scores 0.118629. Preparation is deterministic, every public packet is unique, and no source waveform or packet hash crosses train and test.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Acoustic Password Candidate Ranking Under a Verification Budget

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74kczvjkczyevy0apff7mg4x8c63ng
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat douglas's score of 0.958!

Full challenge description from page:

> Leaderboard
> (15)
> Your Submissions
> Overview
> For each case, rank eight candidate passwords from most to least compatible with ten recorded keystrokes. Then choose the two keystroke positions that should be recorded again to resolve the remaining uncertainty.
> Each audio packet contains ten aligned waveform clips, one for each password position. The candidate packet assigns labels A through H to eight ten-character strings. Several candidates differ only at nearby keyboard keys, and every clip includes channel distortion, room reflections, background interference, or another weak key sound. A strong solution must compare all ten recordings with all eight candidates and recognize which ambiguous positions would benefit most from a clean repeat.
> This models a defensive verification step after a suspected acoustic side-channel exposure. A security analyst may have several plausible reconstructions but only enough user attention to request two additional presses. The useful output is therefore not only a guessed password. It is a complete evidence ranking plus a limited follow-up measurement plan.
> The public training set is large enough to learn key acoustics from waveform or spectral features. Training clips come from repeated isolated-key recordings. Hidden clips come from separately recorded continuous password sessions and stronger held-out channel conditions. Source filenames, source order, and the original password strings are not exposed in the prepared data.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | 5,000 labeled cases with inputs, two scored targets, and two train-only supervision fields. |
> | `test.csv` | 1,000 unlabeled cases built from held-out press repetitions and channel conditions. |
> | `sample_submission.csv` | Schema-valid fixed predictions for every test case. |
> | `audio_packets/*.npy` | Ten-clip waveform packets referenced by the CSV files. |
> CSV Columns
> | Column | Data type | Availability | Description |
> |---|---|---|---|
> | `case_id` | string | train, test | Opaque row identifier used only for submission alignment. |
> | `audio_packet_path` | relative path string | train, test | Path from the public dataset root to one NumPy waveform packet. |
> | `candidate_packet` | JSON object string | train, test | Mapping from labels `A` through `H` to eight distinct ten-character lowercase-letter-or-digit candidates. |
> | `probe_contract` | fixed-format string | train, test | Declares ten aligned clips, an `A` through `H` ranking, and a two-position verification budget. |
> | `candidate_ranking` | ordered token string | train only | All eight candidate labels ordered from greatest to least compatibility. |
> | `verification_pair` | canonical token pair | train only | Two distinct positions selected for a clean repeat recording. |
> | `candidate_relevance` | JSON integer object | train only | Relevance from 2 through 6 for every candidate label in this release. This is auxiliary ranking supervision. |
> | `probe_utilities` | JSON float vector | train only | Utility of all 45 position pairs in the canonical order documented below. This is auxiliary verification supervision. |
> train.csv contains all eight columns. test.csv contains only case_id, audio_packet_path, candidate_packet, and probe_contract.
> Audio Packet
> Each .npy file is a signed 16-bit integer array with shape (10, 2048). Axis 0 follows password positions p1 through p10. Axis 1 contains 2,048 mono samples at 16 kHz, or 128 milliseconds of audio per position. Divide by 32767.0 to obtain an approximate floating-point waveform in [-1,1].
> Each clip starts near a detected key-press energy peak. Amplitude variation, timing warp, short room reflections, hum, additive noise, and a weaker overlapping key sound alter the source recording. Distortions are sampled independently across cases and positions. Test packets use presses segmented from separate continuous typing sessions, so no physical press event appears in both splits.
> Candidate Packet
> candidate_packet is a JSON object with exactly eight keys:
> {"A":"k4w9m2x8qp","B":"k4w9m2x8op","C":"k4w9m2c8qp","D":"k4w9n2x8qp","E":"k4w9m2x7qp","F":"k4e9m2x8qp","G":"k4w9m3x8qp","H":"j4w9m2x8qp"}
> Candidate labels are randomized independently in every case. A password character is one lowercase letter or digit. Most false candidates differ from the true string in one to four positions, with replacement keys sampled preferentially from nearby keyboard locations.
> Ranking Target
> For candidate c, let h(c) be its Hamming distance from the recorded ten-character string. Its integer relevance is:
> relevance(c) = max(0, 6 - h(c))
> The target candidate_ranking orders all eight labels by decreasing relevance. Ties use alphabetical label order. It is written as eight labels separated by >:
> F>A>C>H>B>D>E>G
> Verification Target
> verification_pair contains two distinct position tokens from p1 through p10, sorted numerically and joined by |:
> p3|p8
> The objective is to choose positions where a clean repeat would separate the true candidate from strong alternatives and replace weak current evidence. Pair utility combines three factors: whether each alternative disagrees at a selected position, how far the alternative key lies from the true key on a standard keyboard, and the measured clarity of the current waveform at that position. The 45 training utilities are ordered lexicographically:
> (p1,p2), (p1,p3), ..., (p1,p10), (p2,p3), ..., (p9,p10)
> The target pair is the first maximum-utility pair in that order.
> Training Target Distribution
> | Candidate relevance | Training candidate count |
> |---:|---:|
> | 2 | 5,823 |
> | 3 | 5,826 |
> | 4 | 11,665 |
> | 5 | 11,686 |
> | 6 | 5,000 |
> All 45 legal verification pairs occur in training. Their counts range from 85 to 130, with a median of 111. Candidate-label identities are independently shuffled, so no one label is tied to the correct password.
> Submission Format
> Write the final CSV to ./working/submission.csv.
> The file must contain exactly these columns in this order:
> | Column | Data type | Required content |
> |---|---|---|
> | `case_id` | string | One exact test identifier. |
> | `candidate_ranking` | ordered token string | A permutation of `A` through `H`, joined by seven `>` separators. |
> | `verification_pair` | token-pair string | Two distinct positions from `p1` through `p10`, in ascending order and joined by `|`. |
> Example:
> | case_id | candidate_ranking | verification_pair |
> |---|---|---|
> | `kp_2f728be53a4e49c1dc21` | `F>A>C>H>B>D>E>G` | `p3|p8` |
> Every test ID must occur exactly once. Extra columns, reordered columns, duplicate IDs, missing IDs, unknown IDs, blank IDs, and row-count mismatches reject the submission. A single backend-managed visibility column is accepted and removed before schema validation. Ranking strings longer than 15 characters and pair strings longer than 7 characters are malformed. Malformed row values receive zero for the affected row components.
> Evaluation
> Submissions are evaluated with the Active Acoustic Verification Score:
> Score = 0.55 * RankingScore + 0.40 * ProbeScore + 0.05 * JointScore
> Minimum score: 0.0.
> Maximum score: 1.0.
> Higher is better.
> RankingScore
> For a valid submitted permutation, let rel_k be the true relevance of the label placed at rank k, where k runs from 1 through 8:
> DCG = sum((2^rel_k - 1) / log2(k + 1) for k = 1..8)
> IdealDCG is the DCG of the canonical target ranking. ChanceDCG places the mean gain at every rank. The grader aggregates DCG, IdealDCG, and ChanceDCG over the complete hidden set before correcting chance:
> NDCG_raw = sum(DCG) / sum(IdealDCG)
> NDCG_chance = sum(ChanceDCG) / sum(IdealDCG)
> NDCG_corrected = clip((NDCG_raw - NDCG_chance) / (1 - NDCG_chance), 0, 1)
> Let ExactRankingRate be the fraction of test rows whose full eight-label permutation exactly matches the target:
> RankingScore = 0.55 * NDCG_corrected + 0.45 * ExactRankingRate
> An invalid ranking receives raw DCG 0 and cannot receive exact credit.
> ProbeScore
> For each hidden case, the grader ranks all 45 legal position pairs by true verification utility. Stable ties follow the canonical pair order. If the submitted pair has zero-based rank r in ascending utility order, its raw value is:
> probe_raw = ((r + 1) / 45)^2
> Let ProbeRawMean be the mean raw value over hidden rows. Let ProbeChanceMean be the mean value obtained by averaging the same 45 squared ranks within each row. Then:
> ProbeRankScore = clip((ProbeRawMean - ProbeChanceMean) / (1 - ProbeChanceMean), 0, 1)
> Let ExactProbeRate be the fraction of rows whose submitted pair exactly matches the canonical first maximum-utility pair:
> ProbeScore = 0.35 * ProbeRankScore + 0.65 * ExactProbeRate
> An invalid pair receives raw value 0.
> JointScore
> A row receives joint credit when the submitted first-ranked candidate is the true candidate and the submitted verification pair has maximum utility for that case. JointScore is the mean joint credit over all hidden rows.
> An exact target submission scores 1.0.
> What Makes This Interesting
> Ordinary acoustic key recognition asks for one class per clip. Here, each case is a constrained decision under uncertainty. Evidence must be combined across ten positions, the entire candidate list must be ranked, and the model must decide where a second measurement is worth spending. The best verification pair changes with both the candidate structure and the reliability of the current recordings.
> The task rewards calibrated relative evidence rather than isolated character accuracy. A model can recover useful partial score without solving every character, but a generic alphabetical ranking or fixed verification pair is chance-corrected toward zero.
> What Not To Use
> Do not use case_id, row order, path strings, file sizes, hashes, serialization details, or split position as predictors.
> Do not reverse-map packet bytes to the source repository, source filenames, original long password recordings, or an external waveform lookup table.
> Do not derive hidden labels from unpublished preparation constants, local copies of private answers, grader feedback, or repeated leaderboard probing.
> Do not exploit malformed CSV structure, parser behavior, duplicate rows, missing rows, column order, or backend-added fields.
> Hosted or closed-model API calls are not allowed at inference time. Local CPU models and signal-processing libraries are allowed.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Calibration Coalition Design for Spectral Method Transfer

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7eycskgh9hjkxez00y8b6edd8c2yhq
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat tom_777's score of 0.310!

Full challenge description from page:

> Leaderboard
> (13)
> Your Submissions
> Overview
> Choose a compact panel of calibration compounds for transferring an MS/MS method between two spectral libraries. For every case, select one to three of six calibration candidates, rank all six by their marginal contribution across possible panels, and decide whether the selected panel is sufficient for deployment.
> Tandem mass spectrometry records fragment-ion intensity after a precursor molecule is broken apart. Measurements of the same compound can differ across instruments, collision settings, and library pipelines. Laboratories therefore use standards measured in both environments to estimate how spectral evidence will transfer. The difficult question is not merely whether two spectra differ, but which small combination of standards provides complementary calibration evidence for a new compound.
> Each packet provides one source-library spectrum and one target-library pilot for the target compound. It also supplies six paired calibration compounds measured in both libraries. Two additional target-library repeats of the target compound are withheld during prediction. Those real repeats define how well every possible calibration coalition would have transferred the source spectrum.
> The challenge evaluates cooperative experimental design rather than compound identification, spectral search, or generic reproducibility classification. A candidate can be weak alone but valuable when combined with another standard, so solvers must learn complementarity rather than rank calibrators independently.
> | Output | Prediction |
> |---|---|
> | `calibration_coalition` | The best one-, two-, or three-candidate panel chosen from Q1 through Q6. |
> | `marginal_rank_vector` | Shapley-style contribution ranks for all six candidates. |
> | `deployment_state` | Whether one calibrator suffices, a coalition is ready, or a new standard is required. |
> Dataset
> The prepared data comes from a CC BY 4.0 public fragmentation library containing experimental MS/MS spectra and repeated measurements. Exact source, DOI, checksum, schema, and licensing appear in the raw dataset description.
> There are 1,000 training cases and 150 test cases. Target compounds, calibration compounds, and all their repeat spectra remain split-local. A compound used anywhere in a training packet cannot occur as a target or calibrator in test.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Three inputs followed by three targets for 1,000 cases. |
> | `test.csv` | The same three inputs for 150 hidden-label cases. |
> | `sample_submission.csv` | A schema-valid baseline. |
> | `handoff_packets/*.npz` | Target and calibration spectra referenced by `handoff_path`. |
> train.csv contains case_id, handoff_path, measurement_contract, calibration_coalition, marginal_rank_vector, and deployment_state.
> test.csv contains only case_id, handoff_path, and measurement_contract.
> Columns
> | Column | Data type | Train | Test | Meaning |
> |---|---|---:|---:|---|
> | `case_id` | string | yes | yes | Opaque identifier with no compound, polarity, source, or row-order meaning. |
> | `handoff_path` | path string | yes | yes | Relative path to one compressed spectral packet. |
> | `measurement_contract` | string | yes | yes | Fixed reminder of coalition size, ranking, and deployment outputs. |
> | `calibration_coalition` | sorted token set | yes | no | One to three unique tokens Q1 through Q6, joined by `|`. |
> | `marginal_rank_vector` | JSON integer vector | yes | no | Six ranks in Q1 through Q6 order; each rank 1 through 6 occurs once. |
> | `deployment_state` | categorical string | yes | no | `single_calibrator`, `coalition_ready`, or `collect_new_standard`. |
> The literal measurement_contract is: "Choose one to three of Q1 through Q6 as the calibration coalition, rank all six by marginal transfer contribution, and issue one deployment state."
> Spectral Packet
> | Array | Data type | Shape | Meaning |
> |---|---|---|---|
> | `source_anchor` | Float16 | `128` | Source-library spectrum for the target compound. |
> | `target_pilot` | Float16 | `128` | One visible target-library measurement of the same compound. |
> | `calibration_source` | Float16 | `6 x 128` | Source-library spectra for candidates Q1 through Q6. |
> | `calibration_target` | Float16 | `6 x 128` | Aligned target-library spectra for those six candidates. |
> The 128 positions cover fragment-to-precursor ratios from 0 through 1.06. Intensities are maximum-normalized, square-root transformed, and subjected to a small deterministic perturbation. Sixteen adjacent positions form each of eight ordered regions. A region level is the mean of its three largest intensities.
> The six calibration compounds have the same ion polarity as the target and are ordered by increasing precursor-mass distance. Their Q labels are local roles, not global compound identities.
> Coalition Utility
> For a coalition S, the regional transfer ratio is the median of (target_level + 0.04) / (source_level + 0.04) over members of S, clipped to 0.35 through 2.5. Multiplying the target compound's source level by that ratio gives its expected target level.
> Let hidden_level be the mean of two withheld target repeats. transfer_error is the hidden-intensity-weighted mean absolute difference between expected and hidden levels. pilot_error is the mean absolute difference between the visible pilot and hidden_level. repeat_error is the mean absolute difference between the two hidden repeats.
> utility(S) = exp(-4.2 * transfer_error) * exp(-0.7 * pilot_error) * exp(-0.5 * repeat_error).
> The empty coalition uses transfer ratio 1. Utility is computed for all 64 subsets of Q1 through Q6. The published coalition is selected among subsets of size one through three by maximizing:
> objective(S) = utility(S) - 0.018 * (|S| - 1).
> Ties prefer the smaller coalition and then numeric Q order.
> Marginal Rank Vector
> Each candidate receives its exact six-player Shapley contribution over utility. For candidate q, contributions from adding q to every coalition not containing it are averaged using the standard factorial Shapley weights. Candidates are ranked by decreasing contribution, with numeric Q order breaking exact ties.
> For example, [3,1,5,2,6,4] means Q2 has rank 1, Q4 rank 2, Q1 rank 3, and Q5 rank 6.
> Deployment State
> | Selected coalition and utility | State |
> |---|---|
> | One member and utility at least 0.68 | `single_calibrator` |
> | Otherwise, utility at least 0.54 | `coalition_ready` |
> | Utility below 0.54 | `collect_new_standard` |
> Training contains 113 single_calibrator, 551 coalition_ready, and 336 collect_new_standard cases. Coalition sizes are one for 519 cases, two for 379 cases, and three for 102 cases.
> Submission Format
> Write the final CSV to ./working/submission.csv with exactly these columns in order: case_id, calibration_coalition, marginal_rank_vector, deployment_state.
> | Column | Required format |
> |---|---|
> | `case_id` | Every test ID exactly once; no missing, unknown, duplicate, or padded IDs. |
> | `calibration_coalition` | One to three unique Q tokens in numeric order, joined by `|`; at most 20 characters. |
> | `marginal_rank_vector` | JSON vector of length 6 containing the permutation 1 through 6; at most 30 characters. |
> | `deployment_state` | Exactly one documented state. |
> | case_id | calibration_coalition | marginal_rank_vector | deployment_state |
> |---|---|---|---|
> | `fh_3e005da3839e8ca917b3` | `Q2|Q5` | `[3,1,5,2,6,4]` | `coalition_ready` |
> The grader rejects extra or reordered columns, duplicate column names, incorrect row counts, and invalid IDs. Malformed target values receive zero for their components.
> Evaluation
> The Calibration Coalition Game Score is:
> Score = 0.45 * CoalitionScore + 0.40 * MarginalRankScore + 0.15 * DeploymentScore.
> Minimum score: 0.0
> Maximum score: 1.0
> Higher scores are better.
> CoalitionScore
> The submitted coalition's objective is divided by the canonical coalition's objective and capped at 1. case_coalition_score = 0.20 * objective_ratio + 0.80 * exact_coalition_match. CoalitionScore is the mean case score. Invalid coalitions score 0.
> MarginalRankScore
> For hidden ranks Y and submitted ranks P, proximity = max(0, 1 - sum_i |Y[i] - P[i]| / 18). The case score is 0.20 * proximity + 0.80 * exact_vector_match. MarginalRankScore is the mean over hidden cases.
> DeploymentScore
> This is balanced accuracy over the three hidden deployment states. The submitted state must equal the state produced by the submitted coalition's hidden utility under the published thresholds. An inconsistent coalition-state pair is counted as incorrect.
> What Makes This Interesting
> The nearest experimental literature studies whether spectra reproduce across instruments after all measurements have been collected. This benchmark instead asks a prospective design question: which standards should be measured together before hidden validation repeats are available? Exact Shapley ranking exposes calibrators whose value is complementary rather than individually strong.
> The raw measurements come from the msPurity fragmentation library release. Hopley et al., 2008 is the closest reproducibility study, but it does not define calibration coalitions, cooperative contribution ranks, hidden-repeat utility, or compact-panel deployment decisions.
> Expected And Allowed Methods
> Suitable methods include compact spectral encoders, paired-domain models, set encoders, learned utility surrogates, and differentiable or enumerated subset selection. The arrays and 64-member coalition space are CPU-manageable.
> What Not To Use
> Do not derive outputs from IDs, filenames, row order, packet size, byte hashes, or Q position alone.
> Do not recover compound identities or query external spectral libraries.
> Do not exploit malformed submissions, hidden utility metadata, private answers, or leaderboard probing.
> Reference Validation
> Exact answers score 1.0, the sample scores 0.132780, and the whole-row mode scores 0.141754. Preparation keeps targets and all six calibration donors split-local and rejects duplicate packets.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Habitat-Invariant Audio Encoder Route Audit

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a2tcds5fkxptnjn53373ej98bxk23
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat laddulal's score of 0.475!

Full challenge description from page:

> Leaderboard
> (15)
> Your Submissions
> Overview
> This challenge models a wildlife-monitoring team adapting a songbird-call encoder before deploying it in two habitats. For each case, choose the two encoder blocks that should carry the adaptation, predict how that choice performs in forest and grassland, and rank all five blocks by their individual robustness.
> The audio consists of real territorial songbird vocalizations used in controlled playback experiments. A direct loudspeaker recording provides the reference call. The same reference is broadcast and rerecorded in forest and grassland, where vegetation, distance, reverberation, and background sound alter the signal. A call lineage is one reference vocalization together with its matched forest and grassland rerecordings. Each challenge case contains four such lineages, for twelve clips in total.
> The supplied encoder is a compact five-block analysis model created for this benchmark. It is not a named external pretrained model. Its blocks use different spectral-band and temporal-envelope receptive-field scales, producing one 32-dimensional representation per clip and block. Participants receive the waveforms and the five representation sets in each NPZ packet. Block names b1 through b5 are case-local aliases, so a globally frequent block number cannot identify the answer.
> In practice, adapting every block can be expensive and can erase useful call-identity features. This benchmark imposes a two-block adaptation budget. Updating an unsuitable block can preserve habitat acoustics instead of call identity, while a useful route keeps each field recording closer to its own direct-playback reference than to the three competing references.
> Targets are evaluated on a withheld perturbation of the same matched recordings. The public packet exposes a separate perturbation. Training cases teach how visible representation geometry predicts robustness under a second crop, gain change, time displacement, and noise realization. Test cases use entirely different call lineages.
> This is not species classification, habitat recognition, audio restoration, source separation, or provenance recovery. It evaluates whether a model can forecast the consequences of a layerwise adaptation decision before that decision is deployed.
> | Output | Required prediction |
> |---|---|
> | `adapter_route` | The best unordered pair of local blocks, written in ascending block order. |
> | `route_outcome_matrix` | A `4 x 2` ordinal matrix describing withheld forest and grassland identity margins. |
> | `single_block_order` | A permutation ranking all five blocks from strongest to weakest when used alone. |
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Inputs and three supervised targets for 3,000 cases. |
> | `test.csv` | Inputs for 700 hidden cases. |
> | `sample_submission.csv` | Schema-valid weak submission. |
> | `representation_packets/*.npz` | Waveforms and visible five-block encoder representations. |
> The hidden set is 23.3 percent of the training size. Prepared public files occupy approximately 1.36 GB. Training uses 128 call lineages, test uses 32 different lineages, and no source recording occurs on both sides.
> CSV Columns
> train.csv contains the three input columns followed by all three targets. test.csv contains only the inputs.
> | Column | Data type | Availability | Description |
> |---|---|---|---|
> | `case_id` | string | train and test | Opaque unique identifier. |
> | `representation_packet_path` | string | train and test | Path to the case-level NPZ packet. |
> | `encoder_contract` | categorical string | train and test | States that block aliases are case-local and that clips follow the four-lineage, three-condition layout. |
> | `adapter_route` | canonical string | train only | Two distinct block tokens joined by `+`, such as `b2+b5`. |
> | `route_outcome_matrix` | JSON-encoded integer matrix | train only | Four lineage rows by two habitat columns, with values from `0` through `3`. |
> | `single_block_order` | ordered token string | train only | All five local blocks ranked strongest to weakest. |
> Example labeled record:
> | Field | Example value |
> |---|---|
> | `case_id` | `hr_f1b359f6d5ae2971a9f30e` |
> | `representation_packet_path` | `representation_packets/022713ec01aa32ab7bab73ed.npz` |
> | `encoder_contract` | `case_local_blocks|four_lineages|speaker_forest_grassland` |
> | `adapter_route` | `b2+b5` |
> | `route_outcome_matrix` | `[[2,3],[3,3],[2,0],[3,3]]` |
> | `single_block_order` | `b2>b5>b3>b1>b4` |
> Representation Packet
> | Key | Data type and shape | Description |
> |---|---|---|
> | `waveforms` | float16, `(12,16000)` | Twelve one-second mono clips. |
> | `block_embeddings` | float16, `(5,12,32)` | Visible 32-dimensional representations for five local block aliases and twelve clips. |
> | `sample_rate` | int32 scalar | Constant value `16000`. |
> Waveform rows are grouped by lineage. Rows 0:3 belong to lineage l1, rows 3:6 to l2, rows 6:9 to l3, and rows 9:12 to l4. Within each group, the order is direct playback, forest, grassland.
> The five encoder blocks use different spectral and temporal receptive-field scales. Their aliases are independently permuted for every case, and the packet stores the representations after that permutation. The same alias order is used for the hidden audit perturbation.
> Retrieval Margin
> For a block set, concatenate the selected block representations and normalize each clip vector. For each field clip, calculate cosine similarity to the four direct-playback clips. Its identity margin is:
> margin = similarity_to_correct_lineage - maximum_similarity_to_other_lineages.
> There are eight margins per route: four lineages times two habitats. A positive margin means the correct lineage is the nearest playback reference.
> Adapter Route
> Every pair among the five local blocks is evaluated on the withheld audit perturbation. The canonical route is selected by the following priorities:
> maximize the minimum of the eight identity margins;
> maximize the number of positive margins;
> maximize the mean margin; and
> choose the lexicographically smallest block pair if all three quantities tie.
> The route uses ascending token order. b2+b5 is valid; b5+b2 is not.
> Route Outcome Matrix
> Rows correspond to l1, l2, l3, and l4. Columns correspond to forest and grassland. Each withheld margin is converted to an ordinal level:
> | Level | Withheld identity margin |
> |---:|---|
> | `0` | below `-0.02` |
> | `1` | at least `-0.02` and below `0.02` |
> | `2` | at least `0.02` and below `0.08` |
> | `3` | at least `0.08` |
> Single-Block Order
> Each block is also evaluated alone on the withheld perturbation using the same minimum-margin, positive-count, and mean-margin priorities. single_block_order lists all five block aliases from strongest to weakest, separated by >.
> Target Diversity
> All ten possible adapter routes occur in both splits. The largest training route class contains 333 of 3,000 rows, and the largest test route class contains 85 of 700 rows. Training contains 2,086 distinct outcome matrices and all 120 possible block permutations. Test contains 536 distinct outcome matrices and all 120 permutations.
> Submission Format
> Write the final CSV to exactly ./working/submission.csv.
> It must contain exactly these columns in this order: case_id, adapter_route, route_outcome_matrix, single_block_order.
> | Column | Required format | Limit |
> |---|---|---:|
> | `case_id` | Exact hidden test ID | 64 characters |
> | `adapter_route` | Two different tokens from `b1` through `b5`, ascending and joined by `+` | 8 characters |
> | `route_outcome_matrix` | JSON `4 x 2` matrix with entries in `{0,1,2,3}` | 48 characters |
> | `single_block_order` | Every token `b1` through `b5` exactly once, joined by `>` | 20 characters |
> Valid example:
> | `case_id` | `adapter_route` | `route_outcome_matrix` | `single_block_order` |
> |---|---|---|---|
> | `hr_f1b359f6d5ae2971a9f30e` | `b2+b5` | `[[2,3],[3,3],[2,0],[3,3]]` | `b2>b5>b3>b1>b4` |
> Include exactly one row for every test ID. Extra or reordered columns, duplicate IDs, missing IDs, unknown IDs, and extra rows cause rejection. One backend-managed visibility column is tolerated and removed. Malformed structured values score zero for their affected component.
> Evaluation
> The metric is the Withheld Representation Route Score.
> Final formula: Score = 0.36 * RouteScore + 0.34 * OutcomeScore + 0.20 * BlockOrderScore + 0.10 * JointCertificateScore.
> RouteScore
> For each case, block_overlap is the number of correctly selected blocks divided by two.
> case_route_score = 0.95 * exact_route_match + 0.05 * block_overlap.
> RouteScore is the mean case score. Malformed, repeated, or descending block pairs score zero.
> OutcomeScore
> entry_accuracy is the fraction of eight entries exactly matching the hidden matrix. ordinal_proximity is the mean of 1 - abs(hidden - submitted) / 3 over those entries.
> case_outcome_score = 0.80 * exact_matrix_match + 0.15 * entry_accuracy + 0.05 * ordinal_proximity.
> OutcomeScore is the mean case score. A malformed matrix scores zero.
> BlockOrderScore
> Five blocks define ten unordered pairs. pairwise_concordance is the fraction of those pairs whose submitted relative order matches the hidden order.
> case_order_score = 0.85 * exact_order_match + 0.15 * pairwise_concordance.
> BlockOrderScore is the mean case score. A malformed or incomplete permutation scores zero.
> JointCertificateScore
> For each case, the joint certificate is correct only when the submitted route, complete outcome matrix, and complete block order all exactly match their hidden values. JointCertificateScore is the fraction of hidden cases with all three outputs exactly correct. Partial agreement does not earn joint credit.
> Minimum score: 0.0.
> Maximum score: 1.0.
> Higher is better. Exact hidden answers score 1.0.
> What Not To Use
> Do not identify source recordings through release filenames, external mirrors, acoustic fingerprint services, or nearest-neighbor lookup against the original archive.
> Do not derive targets from public IDs, packet names, row order, file order, hashes, or memorized mappings.
> Do not use hidden audit perturbations, source-side lineage identifiers, environment filenames, or preparation records as inference inputs.
> Do not adapt models or thresholds using hidden answers, submission feedback, or test-specific pseudo-labeling.
> Do not exploit duplicate IDs, missing rows, extra rows, reordered columns, malformed JSON, parser limits, or grader behavior.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Recover Crystallographic Assembly Operators

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7e3dskps24c6g2297yfqfn058at93x
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Leaderboard

Full challenge description from page:

> Overview
> Proteins are three-dimensional molecular machines. In crystallography, scientists often solve and deposit an asymmetric unit, which is the part of a crystal structure stored in a PDBx/mmCIF file. The biologically relevant assembly may require copying one or more protein chains and moving those copies with symmetry transformations recorded in the same source file. Those transformations are represented as affine operators: a 3 by 3 rotation matrix plus a 3-value translation vector.
> This challenge is built from official RCSB PDB crystallographic protein structure records. The raw source records contain atomic coordinates, chain identifiers, biological assembly rows, and crystallographic operator matrices. The public data does not expose those native entry ids or filenames. Instead, each row gives an anonymized, row-local view of one assembly-recovery case.
> Each row contains a compact local chain bank, a row-local bank of candidate affine symmetry operators, candidate chain-copy contact edges, and a corrupted proposed assembly program. Your job is to repair that program: decide which local source chains and local operators are truly used, describe the minimal edits needed to fix the corrupted proposal, and reconstruct the final chain-copy interface graph produced by the repaired program.
> Task
> For every test row, submit five connected prediction heads plus confidence:
> selected local source chains;
> selected local operator ids;
> a minimal edit script that repairs the corrupted program;
> the final chain-copy interface graph after applying the repaired program;
> an ambiguity bucket describing whether near-equivalent alternatives are present.
> These heads are coupled. A program with the wrong operator can still produce plausible local contacts, and a graph-only answer does not explain how the assembly is constructed. Strong solutions need to reason jointly about protein-chain geometry, matrix/vector transformations, contact evidence, and program-repair consistency.
> The public rows are source-neutral. They contain no native entry ids, filenames, absolute archive paths, publication metadata, or raw source identifiers. Public ids and local chain/operator aliases are opaque and row-local. The challenge is to learn reusable structural cues from the released training rows, not to recover the source entry behind a test row.
> Generalization Contract
> Train and test rows are split by source-family signatures before public ids are assigned, so related assembly families are not deliberately shared across train and hidden test. Rows are sorted only by opaque id. The hidden test set contains hundreds of cases and many independent families, with varied operator counts, selected-chain counts, and interface-graph sizes.
> Solvers should learn how chain geometry, affine transformations, contact support, and corrupted-program edits fit together. The natural difficulty comes from near-symmetries, extra candidate operators, similar chain shapes, and plausible decoy contacts, not from arbitrary grading tricks.
> Intended Approach And Allowed Methods
> Strong From Scratch solutions can train compact models directly on the provided train.csv rows. Reasonable approaches include:
> graph or set models over local chains, operators, and candidate edges;
> pairwise chain-copy contact models followed by constrained decoding of valid assembly programs;
> learned ranking of candidate operators and repair edits using chain geometry, affine matrices, and contact support;
> small neural message-passing, transformer-style set encoders, ExtraTrees/gradient boosting, or hybrid geometric search with learned scoring;
> train-only validation splits by source-neutral family or complexity bucket for thresholding and calibration.
> Allowed tooling is ordinary offline machine learning on the released public files, including NumPy, pandas, scikit-learn, PyTorch/JAX/TensorFlow in CPU mode, LightGBM/XGBoost, and custom graph decoders. This is a CPU-based challenge. Solvers should design for the platform limit of 10 CPU cores, 62.5 GB RAM, and 1.5 hours of runtime.
> Simple metadata priors, one-head graph overlap, or copying the corrupted program are useful diagnostic baselines, but they are not sufficient as the primary intended solution. The challenge rewards learned program recovery under row-local geometry.
> What Not To Use
> Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score:
> source-entry lookup, geometry fingerprinting against public structure archives, native id recovery, raw filename matching, source manifest lookup, or direct reconstruction of hidden native assembly records;
> row order, opaque-id hashes, CSV byte length, JSON length, filesystem metadata, archive metadata, or any non-physical side channel;
> hard-coded id-to-answer maps, private-file access, answer-key probing, grader/platform exploitation, or manual hidden-test labeling;
> generic classification/regression framing that ignores the coupled program and graph structure;
> one-head-only outputs that skip the repair program, selected operators, or final interface graph;
> hosted closed-source APIs or external services at train or inference time.
> Enforcement on Invalid Approaches: submissions can be rejected before payout if they are built around lookup, private-data access, platform exploitation, hard-coded ids, or rule-only shortcuts that bypass the intended row-local structural inference.
> Evaluation
> Each row is scored in [0, 1]. Let:
> source_score    = set F1 on selected_asym_ids_json
> oper_score      = set F1 on oper_expression_json
> repair_score    = set F1 on repair_ops_json after canonicalization
> graph_score     = set F1 on interface_graph_json edges
> ambiguity_score = 1 - abs(bucket_distance(pred, true)) / 3
> compound        = 1 if all heads match exactly, else 0
> The row correctness score is:
> correctness = 0.08*source_score
> + 0.22*oper_score
> + 0.36*repair_score
> + 0.29*graph_score
> + 0.01*ambiguity_score
> + 0.04*compound
> These six weights sum to exactly 1.0. The compound term is part of that fixed correctness budget, not an extra bonus outside the formula, so correctness remains in [0, 1].
> Calibration is 1 - abs(confidence - correctness), and:
> row_score = 0.99*correctness + 0.01*calibration
> The final score blends global performance with hidden subgroup robustness:
> Final = 0.72 * mean(row_score)
> + 0.18 * worst_family_mean(row_score)
> + 0.10 * worst_complexity_mean(row_score)
> Higher is better. The theoretical minimum is 0.0, and a perfect submission with confidence 1.0 scores exactly 1.0.
> Submission-level structural failures raise InvalidSubmissionError: missing, extra, or reordered columns; missing, extra, or duplicate ids; id-set mismatch; and non-finite or out-of-range confidence. Row-local JSON fields are limited to 200,000 characters. Malformed row-local JSON scores zero for that affected row rather than crashing the grader or exposing private information.
> Dataset
> The public dataset contains 1,595 labeled training rows and 405 hidden-test rows. Each row is one anonymized assembly-recovery case. The public data contains no native entry ids, filenames, raw source paths, absolute source metadata, or native chain/operator labels.
> File overview
> Item	Description
> public/train.csv	Labeled training rows
> public/test.csv	Test rows, no labels
> public/sample_submission.csv	Valid weak template
> train.csv columns
> Column	Type	Description
> id	int	Opaque row id
> chain_bank_json	JSON	Local chain summaries
> candidate_ops_json	JSON	Candidate operators
> candidate_edges_json	JSON	Candidate contacts
> corrupted_program_json	JSON	Proposed bad program
> prompt	string	Row instruction
> selected_asym_ids_json	JSON	True local chains
> oper_expression_json	JSON	True operator ids
> repair_ops_json	JSON	Minimal edits
> interface_graph_json	JSON	True copy graph
> ambiguity_json	JSON	Ambiguity bucket
> test.csv columns
> Column	Type	Description
> id	int	Opaque row id
> chain_bank_json	JSON	Local chain summaries
> candidate_ops_json	JSON	Candidate operators
> candidate_edges_json	JSON	Candidate contacts
> corrupted_program_json	JSON	Proposed bad program
> prompt	string	Row instruction
> JSON field schemas
> All chain ids, operator ids, and graph-node ids are row-local aliases. They are meaningful only within the current row.
> chain_bank_json is a JSON list of chain-summary objects:
> cid (string): row-local chain id such as C00.
> n_ca (integer): number of protein alpha-carbon coordinates used for the chain summary.
> centroid (list of 3 floats): anonymized 3D centroid of the chain.
> radius (float): root-mean-square radial spread of the chain around its centroid.
> span (float): approximate geometric diameter of the chain in the anonymized coordinate frame.
> shape (list of 3 floats): sorted principal-axis variance values describing the chain's elongated or compact shape.
> sample_coords (list of coordinate lists): up to eight sampled anonymized alpha-carbon coordinates, each [x, y, z].
> candidate_ops_json is a JSON list of operator objects:
> oid (string): row-local operator id such as O03.
> matrix (list of 9 floats): flattened 3 by 3 affine rotation matrix in row-major order.
> vector (list of 3 floats): affine translation vector. Applying an operator maps a point p to matrix @ p + vector.
> candidate_edges_json is a JSON list of possible chain-copy contact objects:
> u (string): first possible chain-copy node id in chain@operator form, such as C00@O03.
> v (string): second possible chain-copy node id in the same form.
> dist (float): noisy, quantized candidate-contact distance feature between the two transformed chain copies.
> support (float): noisy candidate contact-support feature in [0, 1]; higher values usually mean stronger geometric evidence for an interface, but it is not the hidden threshold used for scoring.
> corrupted_program_json is a JSON object:
> selected_asym_ids (list of strings): corrupted proposed local source-chain ids.
> oper_expression (list of strings): corrupted proposed local operator ids.
> The training label columns use the same row-local ids:
> selected_asym_ids_json (JSON list of strings): true local source-chain ids.
> oper_expression_json (JSON list of strings): true local operator ids.
> repair_ops_json (JSON list of objects): minimal edits needed to repair the corrupted program. Each edit has op (insert or delete), field (selected_asym_ids or oper_expression), and value (the row-local id being inserted or deleted).
> interface_graph_json (JSON list of edge objects): true final interface graph. Training-label edges include u, v, and support, where nodes use chain@operator ids.
> ambiguity_json (JSON object): ambiguity metadata in the training labels. Training labels include bucket (low, medium, high, or critical), margin (float separation between true and near-decoy contacts), and alt_count (integer count of near-equivalent alternatives).
> The prompt column is a fixed natural-language instruction reminding solvers to recover the assembly program from the row-local inputs only.
> Submission
> Submit one CSV row per test id with exactly these columns in exactly this order:
> id,selected_asym_ids_json,oper_expression_json,repair_ops_json,interface_graph_json,ambiguity_json,confidence
> Column	Type	Constraint
> id	int	Must match test ids
> selected_asym_ids_json	JSON	Local chain list
> oper_expression_json	JSON	Local operator list
> repair_ops_json	JSON	Edit-operation list
> interface_graph_json	JSON	Edge list
> ambiguity_json	JSON	Bucket object
> confidence	float	In [0,1]
> selected_asym_ids_json and oper_expression_json should be JSON lists of local ids. repair_ops_json must be a JSON list of edit objects, and each edit object must have exactly the op, field, and value fields. In submissions, interface_graph_json should be a JSON list of edge objects with u and v fields, or two-element edge lists [u, v]. A submitted edge may include support, but support is optional metadata and is not required or scored. In submissions, ambiguity_json must include a bucket value from low, medium, high, or critical. The margin field is label-side metadata and is not required in submitted rows.
> Requirements:
> Header row plus exactly one row per test id; the submitted id set must match test.csv exactly.
> The submission must contain exactly the seven listed columns in the listed order; extra, missing, or reordered columns raise InvalidSubmissionError.
> Duplicate ids, missing ids, extra ids, non-finite confidence, or confidence outside [0, 1] raise InvalidSubmissionError.
> Row-local JSON fields must be valid JSON and no longer than 200,000 characters. Malformed row-local JSON scores zero for that affected row without crashing the grader.
> Submitted chain ids, operator ids, and graph-node ids are row-local aliases. Native PDB ids, filenames, source-entry ids, and archive metadata are not valid answers.
> Example:
> id,selected_asym_ids_json,oper_expression_json,repair_ops_json,interface_graph_json,ambiguity_json,confidence
> 17,"[""C00""]","[""O00"",""O01""]","[{""op"":""insert"",""field"":""oper_expression"",""value"":""O01""}]","[{""u"":""C00@O00"",""v"":""C00@O01""}]","{""bucket"":""medium"",""alt_count"":1}",0.62

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Matching Each Recorded Treatment Reason to Its Medicine

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f85z1mnvxhzd8f628php0c58byt20
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top score: —

Full challenge description from page:

> Overview
>
> This is a from-scratch modelling task. A pharmacovigilance safety report lists the medicines a patient was taking and, separately, the clinical reasons those medicines were being taken. The person who filed the report knew which reason belonged to which medicine, but that correspondence has been withheld from you. Both inventories are published in a scrambled order, every identity is replaced by an opaque code, and your job is to put them back together.
>
> Each report gives you a list of medicine slots and a shorter list of reason slots. Every reason slot belongs to exactly one medicine slot, and no two reason slots share a medicine slot. Some medicine slots are decoys that carry no reason at all — 54.0% of reports contain at least one, and there are 2.06 of them on average. You return, for every reason slot, the position of the medicine slot it belongs to.
>
> Nothing here can be solved by looking a code up in a table. The same medicine appears in reports for many different reasons, and the same reason draws on many different medicines, so a per-code rule cannot satisfy the one-to-one requirement across a whole report. The signal lives in the joint fit of the whole assignment, and the only place to learn it is train.csv. Everything needed is in the training split — no external model weights and no outside data are required, and the reference approaches below all finish in a couple of seconds on a modest CPU.
>
> Evaluation
>
> Write 𝑁 for the number of reports scored. For one report let 𝑘 be its number of reason slots, 𝐾 its number of medicine slots, and 𝑎 the number of reason slots you placed on the correct medicine slot.
>
> Pairwise term, corrected for chance:
>
> 𝐴 = ⟮1 ⁄ 𝑁⟯ × Σ ⟮𝑎 ⁄ 𝑘 − 1 ⁄ 𝐾⟯ ⁄ ⟮1 − 1 ⁄ 𝐾⟯
>
> Whole-report hit rate and its chance level:
>
> 𝐸 = ⟮1 ⁄ 𝑁⟯ × Σ ⟦𝑎 = 𝑘⟧ and 𝐸̄ = ⟮1 ⁄ 𝑁⟯ × Σ ⟮𝐾 − 𝑘⟯! ⁄ 𝐾!
>
> Whole-report term, corrected for chance:
>
> 𝐵 = ⟮𝐸 − 𝐸̄⟯ ⁄ ⟮1 − 𝐸̄⟯
>
> Final score:
>
> score = 100 × clip⟮0.65 × 𝐴 + 0.35 × 𝐵, 0, 1⟯
>
> A submission that places every reason slot correctly scores 100. An answer drawn uniformly at random from the valid ones has an expected value of 0 on both 𝐴 and 𝐵, because a random one-to-one placement lands on the truth 1 ⁄ 𝐾 of the time: the correction subtracts exactly that. The minimum is 0, since the score is clipped below.
>
> A row is credited only when it is a genuine placement: exactly 𝑘 whole numbers, all between 1 and 𝐾, and all different. A row that is blank, unparseable, the wrong length, out of range, or repeats a slot is scored as 𝑎 = 0, which is never better than an honest wrong guess and is worse than a random valid one.
>
> Measured reference points, all reproduced with the shipped scorer on the shipped public files:
>
> every row answered 1 2 3 …, which is sample_submission.csv — 0.00
>
> a random valid placement — 0.00
>
> ordering slots by the report_band distractor — 0.00
>
> placing reasons on the globally most common medicines — 0.87
>
> copying the answer from the training report with the same medicine and reason inventories — 0.00
>
> a learned reason-to-medicine association solved as a one-to-one placement — 35.22
>
> the same association plus route, dose form, role and reaction signals — 42.78
>
> placing every reason slot correctly — 100.00
>
> Dataset
>
> train.csv — 22,562 reports with the answer included.
>
> sample_id — integer identifier, unique across the whole release.
>
> medicine_codes — the medicine slots, space separated, in published order. 3 to 10 slots, 5.57 on average. Codes run m00000 to m08307; m99999 marks a medicine whose identity was withheld, which is 12.5% of slots.
>
> medicine_routes — one route code per medicine slot, in the same order. u00 to u62, with u99 where the route was withheld, which is 21.4% of slots.
>
> medicine_forms — one dose-form code per medicine slot, in the same order. f000 to f612, with f999 where the form was withheld, which is 21.3% of slots.
>
> medicine_roles — one role code per medicine slot, in the same order, drawn from p0, p1, p2 and p3.
>
> reason_codes — the reason slots, space separated, in published order. 3 to 8 slots, 3.51 on average, never more than the number of medicine slots. Codes run c00000 to c05176, and no code repeats inside a report.
>
> reaction_codes — the adverse reactions recorded on the report, space separated, 1 to 8 of them, codes x00000 to x06225. Context for the whole report, not tied to any one slot.
>
> patient_sex — M, F or U.
>
> patient_age_band — A under 18, B 18 to 44, C 45 to 64, D 65 and over, U unrecorded.
>
> report_band — b0 to b3. This is a declared distractor. It is drawn from a hash of the report and carries no information about the answer; a rule built on it scores 0.00.
>
> assignment — the answer. For each reason slot in published order, the 1-based position of its medicine slot.
>
> test.csv — 4,909 reports with the same columns except assignment.
>
> sample_submission.csv — a correctly formatted submission that places reason slots on the first medicine slots in order.
>
> Reports are grouped by their originating case, and no case contributes to both splits. Reports whose published content is identical have been reduced to one.
>
> Submission
>
> A CSV with a header row and exactly 4,909 data rows, one per sample_id in test.csv.
>
> sample_id — integer — the identifier copied from test.csv.
>
> assignment — text — space-separated 1-based medicine slot positions, one for every reason slot of that report, in published order.
>
> Validity rules, applied per row: the count must equal that report's number of reason slots; every value must be a whole number between 1 and that report's number of medicine slots; and no value may repeat. Rows breaking any of these are scored as zero correct placements.
>
> Every sample_id from test.csv must appear exactly once. Missing, duplicated and unknown identifiers are rejected, as is a wrong row count. Surplus columns are ignored and column order does not matter.
>
> Worked example, using real identifiers from test.csv. Report 26503 has 8 medicine slots and 4 reason slots, while reports 16550 and 26926 each have 4 medicine slots and 3 reason slots:
>
>
> sample_id,assignment
>
> 26503,2 7 1 5
>
> 16550,3 1 4
>
> 26926,2 4 1
>
> What Not to Use
>
> A per-code lookup table — mapping each reason code to the medicine it most often accompanies. It scores 0.87, because it cannot honour the one-to-one requirement: the same medicine gets claimed by several reasons at once, and the reasons that matter are the ones whose obvious medicine is absent from the report.
>
> Anything built on report_band — 0.00. It is a declared distractor, balanced across reports and independent of the answer.
>
> Position rules — answering 1 2 3 …, or any fixed ordering. Both score 0.00. The slots are published in a scrambled order that carries no trace of how the report was filed.
>
> Copying a similar training report — 0.00, no better than answering at random. Reports are deduplicated on published content and split so that no case appears on both sides, so there is nothing to copy.
>
> Scoring each reason slot independently and taking the best medicine for each — this throws away the constraint that carries most of the signal, and collides on the same slot whenever two reasons look alike.
>
> The intended route is to learn, from train.csv alone, how strongly each reason code associates with each medicine code, then treat one report as a single one-to-one placement problem and choose the arrangement that maximises the total association. Building the association counts from scratch gets you to 35.22. Folding in route, dose form, role and the report's reactions — which carry real signal when a medicine's identity is withheld — reaches 42.78, and there is room above that.
>
>  
>
> Submissions
> 0
> Top Score
> —
> Created
> Aug 6, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> 0/12
> solvers beat AI
> How closing works
>
> Be the first to solve this challenge! 5 distinct solvers with graded solutions are needed to activate the $650 prize pool and start a closing countdown. At 12, up to 12 solvers will be selected to continue.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Dating Undated Growth Sequences

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dc46qkvcvnwry8n3y08hvwn8c38ws
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: small-data, feature-engineering, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.673

Full challenge description from page:

> Placing Undated Ring Sequences on a Reference Timeline
> Overview
>
> A woody plant lays down one growth increment per year. Plants growing under a shared
>
> climate respond to the same good and bad years, so their increment sequences carry a
>
> faint common signal — and that signal is what lets an undated piece of wood be
>
> assigned to the exact years it grew in. Get it right and the sequence is pinned to a
>
> specific span of the timeline; get it wrong by even one position and every year of it
>
> is wrong.
>
> You are given a reference collection: 150 growth-increment series whose position on
>
> a common timeline is known. The timeline is an integer index running from 0 to 480; the
>
> calendar year that index 0 corresponds to is not disclosed and is not recoverable from
>
> anything in the data.
>
> You are also given undated segments: short runs of consecutive growth increments cut
>
> from other source series entirely. For each segment you must say **where on the reference
>
> timeline it sits** — the index of its first increment.
>
> Every segment comes from its own distinct source series. **No two segments — in
>
> training or in test — were cut from the same source series**, and no segment's source
>
> series appears in the reference collection. There is no series to look the answer up in,
>
> and no second piece of the same source to lean on. The position has to be inferred from
>
> the shape of the growth signal alone.
>
> The raw increments are not directly comparable between series. Every series carries a
>
> large, slow trend of its own — driven by stand age and by the individual site — and
>
> that trend is of comparable magnitude to the shared year-to-year signal it is
>
> superimposed on. The strength of the shared signal also varies widely across the
>
> collection: some pairs of series track each other closely, others barely at all.
>
> This is not a forecasting problem. Nothing is predicted forward in time, no future value
>
> is extrapolated, and no model of how the timeline evolves is involved. Every candidate
>
> answer already exists: a segment's position is one of a few hundred fixed indices, and
>
> the task is to decide which one its growth pattern matches. It is a pattern-matching and
>
> retrieval problem over anonymised numeric sequences, built from scratch with no
>
> pretrained components.
>
> Solve it using only the provided data.
>
> Evaluation
>
> A segment is either dated correctly or it is not. Being one position out is not a near
>
> miss — it assigns every increment in the segment to the wrong year — so the score is a
>
> plain exact-match rate:
>
> **Score = (number of test segments placed at exactly the correct offset) / (number of
>
> test segments scored).** The score lies in [0, 1] and higher is better.
>
> Exactly what the grader computes: it joins your submission to the answer key on
>
> segment_id, and counts a segment as correct only when your predicted offset is a whole
>
> number equal to the true offset. There is no partial credit and no tolerance. The final
>
> score is the number of correct segments divided by the number of segments scored.
>
> A prediction that is missing, non-numeric or not a whole number simply scores zero for
>
> that segment rather than invalidating the submission. Segments that are not part of the
>
> scored set are ignored.
>
> For calibration: a submission that answers 0 everywhere scores 0.000, and a submission
>
> that answers the single most frequent training offset everywhere scores 0.007.
>
> Dataset
>
> The public/ folder contains:
>
> | File | Rows | Description |
>
> |------|------|-------------|
>
> | reference.csv | 45,510 | The dated reference collection: 150 series placed on the timeline. |
>
> | train_segments.csv | 7,025 | 90 undated segments, provided for development. |
>
> | train_offsets.csv | 90 | The correct offset for each training segment. |
>
> | test_segments.csv | 10,395 | 136 segments to place. This is what you are scored on. |
>
> | sample_submission.csv | 136 | The exact required output format, filled with a placeholder value. |
>
> reference.csv
>
> | Column | Type | Description |
>
> |--------|------|-------------|
>
> | ref_id | string | Opaque reference-series token. Carries no signal. |
>
> | group_id | string | Opaque taxon token. Series sharing a token are the same botanical taxon. |
>
> | t | integer | Position on the reference timeline, 0 to 480. The same t is the same year for every series. |
>
> | width | integer | Growth increment for that position, in 1/100 mm. |
>
> A reference series covers one stretch of the timeline, not all of it, and different
>
> series cover different stretches. Occasional single t values may be absent within a
>
> series' span.
>
> train_segments.csv and test_segments.csv
>
> | Column | Type | Description |
>
> |--------|------|-------------|
>
> | segment_id | string | Opaque segment token. Carries no signal and no ordering information. |
>
> | group_id | string | Opaque taxon token, drawn from the same vocabulary as reference.csv. |
>
> | k | integer | Position within the segment, 0 to L-1, with no gaps. |
>
> | width | integer | Growth increment, in 1/100 mm. |
>
> Segment lengths are 40, 50, 60, 75, 90, 110 or 130 increments; the median is 75 and the
>
> mean is about 76.
>
> train_offsets.csv
>
> | Column | Type | Description |
>
> |--------|------|-------------|
>
> | segment_id | string | Matches a segment in train_segments.csv. |
>
> | offset | integer | Timeline index of that segment's k = 0 increment. |
>
> Definition of offset. A segment of length L placed at offset o occupies timeline
>
> positions o, o+1, ..., o+L-1. Its increment at k belongs to timeline position
>
> o + k. Every segment lies entirely inside the timeline, so o >= 0 and
>
> o + L - 1 <= 480. Observed training offsets run from 32 to 427.
>
> The reference series, the training segments and the test segments come from three
>
> disjoint sets of source series, and within the segments each source series
>
> contributes exactly one segment. Every one of the 226 segments therefore has its own
>
> source series: none is shared between two segments, or between a segment and a
>
> reference series. Near-duplicate source records were removed when the corpus was built,
>
> so no two source series are two codes for what is evidently the same record.
>
> Submission
>
> Submit a CSV with exactly the columns segment_id and offset, one row per segment in
>
> test_segments.csv:
>
>
> segment_id,offset
>
> seq_00000,<integer>
>
> seq_00001,<integer>
>
>
> Requirements
>
> One row per segment_id in test_segments.csv, plus the header. Every test
>
> segment_id must be present; a missing id makes the submission invalid.
>
> No duplicate segment_id values; a duplicate makes the submission invalid.
>
> The columns segment_id and offset must both be present. Any further columns are
>
> ignored rather than treated as an error.
>
> offset must be a whole number. Any other value scores zero for that segment rather
>
> than invalidating the submission.
>
> Rows whose segment_id is not being scored are ignored, never an error.
>
> What not to use
>
> No internet access at solve time, and no external data, corpora or pretrained
>
> checkpoints beyond the provided files.
>
> Do not attempt to identify the origin of the data, or to recover calendar years, from
>
> outside knowledge or any external source. The timeline origin is withheld and the task
>
> is to infer position from the provided signal.
>
> Do not attempt to reconstruct the private answer key.
>
> Do not use upstream source repositories, provenance lookup, source identifiers, or any
>
> artefact of how this dataset was constructed to recover test offsets. Recovering an
>
> offset from anything other than the released growth signal is out of scope, however it
>
> is obtained.
>
> Do not hard-code offsets or any per-segment answer; the method must be derived from
>
> the provided data.
>
> segment_id and ref_id values are randomly assigned. Do not rely on their order or
>
> on any pattern in them, and do not use row order as a feature.
>
> Why this is hard
>
> The answer for a segment exists in no record anywhere in the provided data. It is not a
>
> field that has been hidden and it is not held by some other series: the source series
>
> for the test segments are absent from the reference collection entirely, so the position
>
> can only be reconstructed from a shared signal that is faint, partly obscured by each
>
> series' own trend, and of unequal strength across the collection. The search space is
>
> large — a segment of length L may start at any offset from 0 to 481 - L inclusive, which
>
> is 482 - L admissible positions: 442 for the shortest 40-increment segments and 352 for
>
> the longest 130-increment ones — and the metric awards
>
> nothing for being close, so a method has to be right, not approximately right.
>
> Difficulty is set by segment length, and the collection deliberately mixes lengths.
>
> Short segments carry fewer matchable years and are substantially harder than long ones;
>
> roughly a third of the test set is 50 increments or shorter.
>
> Classical crossdating addresses this same underlying problem directly: matching a
>
> floating run of growth increments against a dated reference chronology is exactly what
>
> the discipline has done for a century, and those procedures are the natural starting
>
> point here. What differs is the evaluation, not the science. Those procedures are fixed
>
> statistics applied one series at a time, with a human accepting or rejecting each
>
> result; they learn nothing from labelled examples, and they are never asked to hold
>
> their accuracy on a held-out set of source series chosen to be absent from everything
>
> else supplied. Here the formulation is automated end to end and scored without a human
>
> in the loop.
>
> Two neighbouring lines of work genuinely do not apply. Work on automatic ring detection
>
> operates on photographs of wood cross-sections and solves an image-segmentation problem
>
> that ends where this one begins — here the increments are already measured, and no image
>
> exists. Work that uses growth increments as a climate proxy takes the dates as given
>
> and reconstructs climate from them, inverting the direction of inference used here.
>
> Submissions
> 6
> Top Score
> 0.673
> Created
> Aug 8, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> 6/12
> solvers beat AI
> Closing soon
>
> Prize pool active — closing countdown started. At 12, up to 12 solvers will be selected to continue.
>
> Closing in 11h 47m
>
> Submit your solution before the deadline. Payouts are processed after the challenge closes.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Habitat-Range Acoustic Interaction Square Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75mvkh91mj52syreeqxd4ccs8c6maj
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: —

Full challenge description from page:

> Overview
>
> For each five-channel bird-song packet, reconstruct which channel is the original recording and which four channels occupy the forest-near, grassland-near, forest-far, and grassland-far cells of a playback experiment. Then predict how four fixed time segments change along the four edges of that experimental square and recover the habitat-by-range interaction for each segment.
>
> The recordings come from real Yellowhammer songs and controlled outdoor playbacks. Source songs were captured within approximately 5 meters of singing posts. The same songs were later replayed in forest and grassland settings at multiple distances from 6.5 to 200 meters. Each challenge packet contains one source recording plus a matched 2 x 2 habitat-range square from one song. Channel rows are shuffled and renamed A through E.
>
> This models a blinded field experiment rather than microphone ranking. Ecological monitoring teams often need to determine whether signal loss is explained by distance alone or whether habitat changes the distance effect. The mixed interaction is important because a detector calibrated in open grassland may not degrade in the same way under forest reverberation and masking.
>
> The three required predictions are:
>
> | Output | Plain meaning |
> |---|---|
> | `factor_square` | Assign channels `A` through `E` to the five experimental roles. |
> | `edge_effect_matrix` | Measure motif-evidence change along the two range edges and two habitat edges. |
> | `mixed_interaction_vector` | Measure how much the range effect differs between forest and grassland for each motif. |
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | 3,200 packet references with all three targets. |
> | `test.csv` | 800 packet references without targets. |
> | `sample_submission.csv` | One schema-valid fixed prediction for every test row. |
> | `interaction_packets/*.npy` | Five-channel, one-second waveform packets. |
>
> CSV Columns
> | Column | Data type | Availability | Description |
> |---|---|---|---|
> | `case_id` | string | train and test | Opaque unique identifier used only for submission alignment. |
> | `interaction_packet_path` | relative path string | train and test | Path to one waveform packet. |
> | `packet_contract` | fixed string | train and test | Declares the five roles, four motifs, and sample rate. It contains no assignment. |
> | `factor_square` | canonical token string | train only | Channel assignment for the origin and four factorial cells. |
> | `edge_effect_matrix` | JSON integer matrix | train only | A `4 x 4` matrix of motif-evidence changes. |
> | `mixed_interaction_vector` | JSON integer vector | train only | Four habitat-by-range interaction values. |
>
>
> train.csv contains the three input columns followed by the three target columns. test.csv contains only case_id, interaction_packet_path, and packet_contract.
>
> Every packet_contract value is roles=O,FN,GN,FF,GF;motifs=4;sample_rate=16000.
>
> Audio Packet
>
> Each packet is a signed 16-bit NumPy array with shape 5 x 16000. Rows correspond to anonymous channels A, B, C, D, and E. Each row contains one second of mono audio at 16 kHz.
>
> All five rows use the same underlying source song. The two selected playback distances are separated by at least two published distance categories. Real split-local background recordings, smooth microphone coloration, weak echoes, short attenuation intervals, and RMS equalization are applied independently. These changes prevent absolute loudness, packet size, or one fixed frequency curve from revealing a role.
>
> Factor Square
>
> The five roles are:
>
> | Role | Meaning |
> |---|---|
> | `O` | Original near-source song recording. |
> | `FN` | Forest recording at the selected nearer playback distance. |
> | `GN` | Grassland recording at the same nearer distance. |
> | `FF` | Forest recording at the selected farther distance. |
> | `GF` | Grassland recording at the same farther distance. |
>
>
> factor_square uses the fixed role order O,FN,GN,FF,GF. Tokens are separated by |, and every channel letter must occur exactly once.
>
> O=C|FN=A|GN=E|FF=B|GF=D
> Motif Evidence Levels
>
> A motif is one of the four consecutive 0.25-second quarters of the packet: 0.00-0.25, 0.25-0.50, 0.50-0.75, and 0.75-1.00 seconds. Evidence is measured relative to the same quarter in role O.
>
> For one corner role and one motif, let c be cosine similarity between normalized log spectra from 1.8 to 8.2 kHz, and let r be the corner-to-origin RMS-energy ratio. The prepared label uses shape_score = clip((c - 0.10) / 0.80, 0, 1), energy_score = clip(r / 1.20, 0, 1), and level = round(4 * (0.75 * shape_score + 0.25 * energy_score)). Every evidence level is an integer from 0 through 4.
>
> Edge Effect Matrix
>
> Rows follow the four motifs in chronological order. Columns follow this fixed edge order:
>
> | Column | Directed edge | Entry calculation |
> |---:|---|---|
> | 0 | `FN -> FF` | `level(FF) - level(FN)` |
> | 1 | `GN -> GF` | `level(GF) - level(GN)` |
> | 2 | `FN -> GN` | `level(GN) - level(FN)` |
> | 3 | `FF -> GF` | `level(GF) - level(FF)` |
>
> Every matrix entry is an integer from -4 through 4. Positive values mean evidence is stronger at the edge destination; negative values mean it is weaker.
>
> [[0,-1,1,0],[-2,-1,0,1],[1,-2,-1,-4],[0,0,1,1]]
> Mixed Interaction Vector
>
> For each motif row, the interaction is the difference between the two range effects. The same value must also be recovered from the two habitat effects:
>
> interaction = edge[0] - edge[1] = edge[2] - edge[3].
>
> The vector has four integers from -8 through 8. A positive value means the forest range transition retained more evidence than the grassland range transition for that motif. A negative value means the grassland transition retained more.
>
> For the example matrix above, the vector is [1,-1,3,0].
>
> Submission Format
>
> Write the final CSV to exactly ./working/submission.csv.
>
> It must contain exactly these columns in this order:
>
> | Column | Data type | Required serialization |
> |---|---|---|
> | `case_id` | string | One exact test identifier. |
> | `factor_square` | string | Five canonical role assignments separated by `|`. |
> | `edge_effect_matrix` | JSON string | A `4 x 4` integer matrix with values from `-4` through `4`. |
> | `mixed_interaction_vector` | JSON string | Four integers from `-8` through `8`. |
>
>
> Example:
>
> | case_id | factor_square | edge_effect_matrix | mixed_interaction_vector |
> |---|---|---|---|
> | `hs_31d4e6a09a0c21d614a9` | `O=C|FN=A|GN=E|FF=B|GF=D` | `[[0,-1,1,0],[-2,-1,0,1],[1,-2,-1,-4],[0,0,1,1]]` | `[1,-1,3,0]` |
>
>
> The grader rejects extra or reordered columns, duplicate columns, duplicate IDs, missing or unknown IDs, and wrong row counts. One optional backend-managed visibility column is ignored. Factor strings longer than 32 characters, matrices longer than 128 characters, and vectors longer than 40 characters are malformed. Malformed target values receive zero for their affected component.
>
> Evaluation
>
> The metric is the Acoustic Interaction Square Score.
>
> BaseScore = 0.45 * FactorSquareScore + 0.35 * EdgeEffectScore + 0.20 * MixedInteractionScore.
>
> FinalScore = BaseScore * (0.92 + 0.08 * ClosureRate).
>
> Minimum score: 0.0.
>
> Maximum score: 1.0.
>
> Higher scores are better.
>
> FactorSquareScore
>
> For each row, role_accuracy is the fraction of the five roles assigned the correct channel. MeanRoleAccuracy is its mean over the hidden set. Because a random channel permutation has expected role accuracy 0.20, the aggregate correction is AdjustedRoleAccuracy = clip((MeanRoleAccuracy - 0.20) / 0.80, 0, 1).
>
> FactorSquareScore = 0.30 * AdjustedRoleAccuracy + 0.70 * ExactSquareRate, where ExactSquareRate is the fraction of complete five-role assignments that exactly match.
>
> EdgeEffectScore
>
> For one valid prediction matrix P and true matrix Y, proximity = mean(max(0, 1 - abs(P[i,j] - Y[i,j]) / 8)) and entry_accuracy = mean(P[i,j] = Y[i,j]) over all 16 entries.
>
> row_edge_score = 0.15 * proximity + 0.25 * entry_accuracy + 0.60 * exact_matrix_match.
>
> EdgeEffectScore is the mean row score. A malformed matrix receives zero.
>
> MixedInteractionScore
>
> For a valid submitted vector p and true vector y, proximity = mean(max(0, 1 - abs(p[i] - y[i]) / 16)).
>
> row_interaction_score = 0.25 * proximity + 0.75 * exact_vector_match.
>
> MixedInteractionScore is the mean row score. A malformed vector receives zero.
>
> ClosureRate
>
> A row is closed when the submitted matrix and vector satisfy both square paths for every motif: vector = matrix[:,0] - matrix[:,1] and vector = matrix[:,2] - matrix[:,3]. ClosureRate is the fraction of closed rows and scales the base score from 0.92 to 1.00. A zero matrix with a zero vector is internally closed but receives no special correctness credit unless it also matches the hidden values.
>
> What Makes This Interesting
>
> This is not ordinary channel selection or distance ranking. The model must reconstruct a blinded factorial design and estimate a discrete mixed derivative from audio. Correct edge effects must agree around two paths through the same habitat-range square, which turns independent predictions into one checkable experimental reconstruction.
>
> The task rewards models that separate source-song identity, habitat response, and distance attenuation while remaining robust to unrelated microphone and background changes. It can be approached with compact audio encoders, role-conditioned matching, and constrained decoding on CPU.
>
> What Not To Use
>
> Do not infer roles from case_id, row order, path strings, packet size, hashes, serialization details, or split position. Do not recover source filenames, search external copies of the recordings, or build lookup tables keyed by source songs. Do not exploit malformed CSV structure, missing rows, duplicate IDs, parser behavior, or repeated leaderboard probing. Predictions should come from a learned model applied to the supplied waveform packets.
>
>  
>
> Submissions
> 0
> Top Score
> —
> Created
> Aug 10, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> 0/12
> solvers beat AI
> How closing works
>
> Be the first to solve this challenge! 5 distinct solvers with graded solutions are needed to activate the $650 prize pool and start a closing countdown. At 12, up to 12 solvers will be selected to continue.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Zeolite Intervention Squares: Connectivity Change Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx728e1h79rn06p3j9hzdh0rqx8bzqv8
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 55.461

Full challenge description from page:

> Overview
>
> For each test row, compare four versions of the same material and identify where its pore connectivity changes. Output one token for each changing comparison. Output FLAT when none of the four comparisons changes.
>
> Zeolites are crystalline materials containing microscopic pores and channels. They are used in molecular separation, adsorption, and catalysis because some molecules can travel through those channels while larger molecules cannot. A channel may cross the repeating crystal along the x, y, or z direction. Predicting which directions remain connected helps distinguish an open three-dimensional pore network from a narrow or disconnected one.
>
> The data are author-owned processed results from a licensed, published computational study of 265 zeolite frameworks; formal provenance and licensing are provided on the dataset page. These are not laboratory sensor recordings. Starting from crystallographic framework geometry, the study represented empty pore space as small cubic cells called voxels. It repeated the calculation at grid widths 16, 24, and 32 and at five virtual-probe thresholds. A larger virtual probe cannot fit through a narrow opening, so increasing the threshold can remove a passage.
>
> The processing produced several physical summaries:
>
> pore diameters describe the width of openings through the framework;
> bottleneck value describes the most restrictive part of a retained route;
> route length measures the extent of the connected paths that remain;
> active voxels count accessible pore-space cells before route pruning;
> retained voxels count the cells still supporting routes after pruning;
> connected components count separate pore regions that cannot reach one another;
> periodic axes state whether a route crosses the repeating crystal along x, y, or z.
>
> Two voxel-neighbour rules provide complementary calculations. The 18-neighbour rule connects cells sharing a face or edge. The 26-neighbour rule also allows corner contacts. Differences between them indicate borderline connections. Probe thresholds are experimental settings in a computer calculation, not timestamps.
>
> Each competition row combines two grid resolutions and two probe thresholds. Their four combinations form this intervention square:
>
> Each row defines four conditions from one unseen zeolite framework:
>
> C01 ←W— C11
>
> | ↑
>
> S N
>
> ↓ |
>
> C00 —E→ C10
>
>
> - `C00`: lower grid resolution and lower probe threshold;
> - `C10`: higher grid resolution and lower probe threshold;
> - `C11`: higher grid resolution and higher probe threshold;
> - `C01`: lower grid resolution and higher probe threshold.
>
> You receive coarse framework geometry and lossy measurement cards for all four corners. None of the four topology states is disclosed. Infer their relationships while moving through the edges in the fixed order `E`, `N`, `W`, `S`, and emit one event token whenever the state at the destination differs from the state at the source. The letters only specify traversal order; they are not physical compass directions.
>
> Every emitted token answers three additional questions: which periodic axes survive at the destination, how two connectivity procedures differ there, and whether bottleneck, route-length, or voxel-support change dominates the edge.
>
> ### One-Row Example
>
> Suppose only the move from `C10` to `C11` changes connectivity. At `C11`, the `x` and `y` directions survive, the two procedures have zero rank gap, and route length is the dominant physical change. The correct output is:
>
>
> N-AXY-GZ0-ML
>
>
> Here `N` identifies the changed edge, `AXY` gives the destination axes, `GZ0` gives the destination rank gap, and `ML` identifies route length as the dominant mechanism.
>
> This is a relational counterfactual-program task. It is not a per-condition framework label, ordinary classification, regression, reconstruction, chronological time series, or one-dimensional trajectory forecast. The target is a coupled four-corner object created from the interaction of two interventions.
>
> All 30 squares from one framework stay on the same side of the split. The 60 test frameworks never appear in training. Input masking and quantization affect only supplied measurements; every target is deterministically computed from the clean licensed measurements.
>
> ## What You Must Predict
>
> Submit one `boundary_program` string for every test `id`.
>
> An event token has the form:
>
>
> Edge-Axis-Gap-Mechanism
>
>
> For example:
>
>
> N-AXY-GZ0-ML
>
> Edge
>
> The first field is one of:
>
> E: C00 → C10, increasing grid resolution at the lower probe;
> N: C10 → C11, increasing probe threshold at the higher grid;
> W: C11 → C01, decreasing grid resolution at the higher probe;
> S: C01 → C00, decreasing probe threshold at the lower grid.
>
> Tokens must appear in E N W S order, and each edge may appear at most once.
>
> Destination Axis State
>
> The second field is the hidden state at the destination corner:
>
> A0: no periodic axis survives;
> AX, AY, AZ: one named axis survives;
> AXY, AXZ, AYZ: two named axes survive;
> AXYZ: all three axes survive.
> Destination Rank Gap
>
> The third field is one of GN1, GZ0, GP1, GP2, or GP3, representing signed route-witness-minus-region rank gaps of -1, 0, +1, +2, and +3.
>
> Dominant Response Mechanism
>
> The fourth field describes which clean physical measurement changes most strongly across the edge after scaling each measurement by its dataset-wide standard deviation:
>
> MB: bottleneck change dominates;
> ML: log retained-route-length change dominates;
> MV: log retained-voxel-support change dominates.
>
> Absolute standardized changes are compared. Ties use the fixed priority MB, then ML, then MV. Mechanism labels are emitted only on edges where the topology state changes.
>
> Valid programs include:
>
>
> FLAT
>
> N-AXY-GZ0-ML
>
> E-AXYZ-GP1-MB N-A0-GZ0-MV S-AXZ-GZ0-ML
>
>
> Do not combine FLAT with event tokens.
>
> From-Scratch Rules
>
> Every learned encoder, embedding, representation, and prediction head must be initialized from random weights and trained only with the supplied competition files. Pretrained models, pretrained embeddings, external datasets, source-record retrieval, hidden-source matching, TF-IDF, and handcrafted lookup tables recovered from outside the competition are not permitted.
>
> CPU-trained trees, linear models, scratch-initialized neural networks, and deterministic constrained decoders are allowed.
>
> Evaluation
>
> The grader evaluates event locations and their attributes. The metric names below are written in full so they are not confused with the edge codes E, N, W, S or axis codes such as AX.
>
> 1. EdgeF1
>
> EdgeF1 is the micro F1 between predicted and true (row, edge) event sets. A correctly located edge event counts even if its attributes are wrong.
>
> 2. AxisF1
>
> At each true event edge, compare the predicted destination-axis code with the truth. Missing events are incorrect. Compute F1 separately for every axis code present in the hidden answers and average the values.
>
> 3. GapF1
>
> At each true event edge, compare the predicted destination-gap code with the truth. Missing events are incorrect. Compute F1 separately for every gap code present in the hidden answers and average.
>
> 4. MechanismF1
>
> At each true event edge, compare the predicted mechanism with the truth. Missing events are incorrect. Compute F1 separately for MB, ML, and MV, then average.
>
> 5. TokenF1
>
> TokenF1 is the micro F1 between predicted and true (row, complete event token) sets. Edge, destination state, and mechanism must all match.
>
> 6. ExactRate
>
> ExactRate is the fraction of rows whose complete normalized program exactly matches the answer, including FLAT rows.
>
> The final score is:
>
>
> Score = 100 × (
>
>     0.20 × EdgeF1
>
>   + 0.20 × AxisF1
>
>   + 0.15 × GapF1
>
>   + 0.20 × MechanismF1
>
>   + 0.15 × TokenF1
>
>   + 0.10 × ExactRate
>
> )
>
>
> Scores range from 0 to 100, and higher is better. Structurally invalid submissions are rejected with a clear error. A malformed program in an otherwise valid file receives no credit for that row and cannot create an abstention advantage.
>
> Dataset
> Files
> train.csv — 6,150 labeled intervention squares from 205 frameworks.
> test.csv — 1,800 unlabeled intervention squares from 60 disjoint frameworks.
> sample_submission.csv — required two-column submission template.
> metadata.json — code vocabularies, corner/edge order, widths, and split counts.
> Columns
>
> | Column | Type | Files | Description |
>
> |---|---|---|---|
>
> | id | string | train, test | Fresh sequential competition identifier with no framework or target information. |
>
> | grid_span | string | train, test | Lower and higher cubic-grid widths, such as G16>G32, meaning 16×16×16 and 32×32×32 voxel grids. |
>
> | probe_span | string | train, test | Lower and higher virtual-probe thresholds, such as P04>P10. These are intervention settings, not times. |
>
> | geometry_stream | string | train, test | Eight space-separated framework-geometry codes. |
>
> | corner_stream | string | train, test | Four lossy measurement cards in C00 C10 C11 C01 order. |
>
> | boundary_program | string | train only | Clockwise boundary program to predict. |
>
> geometry_stream Grammar
>
> The eight positions represent included-sphere diameter, three directional free-sphere diameters, effective limiting diameter, directional anisotropy, framework density, and maximum ring size. Sphere diameters summarize pore width; anisotropy measures how unequal the directional openings are; framework density measures solid framework atoms per volume; ring size describes the largest reported pore-forming atomic ring. Values are ordinal quantile codes 0 through 7; X means unavailable.
>
> corner_stream Grammar
>
> Each card has the form Cij_abcdefgh, where Cij identifies its square corner. The eight single-character fields are:
>
> Bottleneck: the narrowest support value along a retained 18-neighbour route; smaller buckets indicate a tighter limiting passage.
> Retained route length: the total length of routes remaining after bottleneck pruning under the 18-neighbour rule.
> Retained voxels: how many accessible voxels still support retained routes after pruning under the 18-neighbour rule.
> Active voxels: how many accessible voxels were available before pruning under the 18-neighbour rule.
> Connected components: how many disconnected accessible regions remain under the 18-neighbour rule.
> Neighbour-rule disagreement: the absolute difference in retained route length between the 18-neighbour and 26-neighbour calculations.
> Support survival ratio: retained voxels divided by active voxels under the 18-neighbour rule.
> 26-neighbour active voxels: the accessible-voxel count when face, edge, and corner contacts are all allowed.
>
> Each field is 0 through 7 or X. The unavailable pattern is deterministic for a framework-condition measurement and contains no target information. Every row contains exactly four cards in C00 C10 C11 C01 order.
>
> Rows from one hidden framework share underlying condition measurements, but no framework identifier or exact corner topology state is supplied and no framework crosses train/test. Participants may use only relationships available in the supplied files.
>
> Submission
>
> Your CSV must contain exactly these columns in this order:
>
>
> id,boundary_program
>
> id must match every test identifier exactly once.
> boundary_program must follow the grammar above.
> Do not add an index column, duplicate an ID, omit a row, or add extra columns.
>
> Example using real test IDs and syntactically valid placeholder predictions:
>
>
> id,boundary_program
>
> SQT00000000,FLAT
>
> SQT00000001,N-AX-GZ0-ML
>
> SQT00000002,E-AXYZ-GP1-MB W-AX-GZ0-MV
>
>
>  
>
> Submissions
> 36
> Top Score
> 55.461
> Created
> Aug 7, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> Grace-period rankings
> Lockdown
>
> The continuing roster is selected after the one-hour grace period; pre-cutoff submissions get up to one additional hour to finish.
>
> Closing in 10h 28m
>
> Submit your solution before the deadline. Payouts are processed after the challenge closes.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Satellite Embedding Index Reconciliation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx772c2h46zdsstmptwxdvxn0h89s9n7
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.649

Full challenge description from page:

> Overview
>
> Earth-observation systems often maintain several vector indexes for the same satellite catalog. One index may support semantic search, another may emphasize visual structure, and another may encode geographic or land-cover information. These indexes are normally joined through source identifiers rather than through their vector contents.
>
> During an index migration, identifiers can be lost while the vectors remain intact. Rows may also be shuffled, omitted, or replaced by a valid vector from a different tile. When this happens, rebuilding the index requires more than nearest-neighbor search because different encoders do not share a coordinate system and an injected record can still describe visually similar terrain.
>
> Each case in this challenge contains six anonymous satellite sites represented in one complete anchor panel and two independently shuffled target panels. The three panels were produced by different representation systems. Exactly one target panel is corrupted: one of its six site vectors is missing and has been replaced by a hard-matched foreign vector from another location.
>
> Your task is to align both target panels to the six anchor sites, identify the corrupted panel, identify which anchor site is missing from that panel, and reject its unused foreign card.
>
> This is not standard remote-sensing classification, geolocation, or cross-modal retrieval. Retrieval benchmarks assume that gallery identities are trustworthy and usually evaluate independent query-result pairs. Classical embedding alignment assumes clean paired samples and a complete correspondence. Here, every test item is a small unordered set, the encoder spaces are heterogeneous and anonymized, and one set violates the one-to-one correspondence through a simultaneous deletion and insertion. The correct solution must learn cross-space compatibility from training cases and perform joint constrained reconciliation rather than score each pair independently.
>
> The practical application is integrity auditing for replicated vector databases. A successful model can recover identity relationships between independently generated indexes without exposing raw imagery, source coordinates, or original catalog identifiers.
>
> This is a CPU-oriented From Scratch challenge. Participants train only on compact released vectors. Image decoding, vision-model inference, and GPU training are not required.
>
> Task
>
> Every case contains six anchor tokens, A0 through A5.
>
> Panel P contains card tokens P0 through P5. Panel Q contains card tokens Q0 through Q5. Card numbers are assigned independently and do not indicate the corresponding anchor.
>
> For every anchor, predict its card in Panel P and its card in Panel Q.
>
> Exactly one of the two panels is complete. Its six predictions must form a permutation of all six card tokens from that panel.
>
> The other panel is corrupted. Its six predictions must contain:
>
> exactly one MISSING token;
>
> five distinct card tokens from that panel; and
>
> one unused card, which is interpreted as the foreign record.
>
> You must also submit corrupt_panel as either P or Q. It must agree with the panel containing MISSING.
>
> Dataset
>
> The source archive provides three heterogeneous embedding views for exactly 22,000 globally distributed satellite sites selected from a larger aligned source intersection. Challenge preparation applies a separate fixed sparse projection to each view, fits scaling parameters on training sites only, removes geographic and catalog identifiers, and generates reconciliation cases.
>
> The prepared challenge contains:
>
> 12,000 labeled training cases;
>
> 2,400 unlabeled test cases;
>
> six anchor sites per case;
>
> three projected embedding panels per site; and
>
> 17,600 distinct training sites, 2,200 distinct public-test sites, and 2,200 distinct private-test sites.
>
> The test size is 20 percent of the training-case count. The test set contains 600 public cases and 1,800 private cases.
>
> Derived cases are not counted as independent sites. A source site is assigned to exactly one of train, public test, or private test before any case is generated. Every case draws all of its genuine and foreign records from one assigned site pool. Thus no site, encoder view, projected vector, or derived occurrence crosses a dataset or visibility boundary.
>
> Balanced spatial cells are the independent split groups. The 22,000 sites are partitioned into 110 geographically local groups of exactly 200 sites before challenge cases exist. The split assigns 88 complete groups to training, 11 to public test, and 11 to private test. Public and private visibility is assigned by complete spatial group and complete case, never by target column or individual panel row.
>
> Public and private therefore contain the same number of independent groups and the same number of distinct sites, but they intentionally contain different numbers of derived cases. Case generation reuses sites only within their assigned partition: the 600 public cases are distributed across the 11 public groups at approximately 54 or 55 cases per group, while the 1,800 private cases are distributed across the 11 private groups at approximately 163 or 164 cases per group. This preserves equal geographic group coverage while keeping public feedback at 25 percent of the 2,400 test cases and reserving 75 percent for final ranking.
>
> Cases reuse sites only inside their assigned partition. Corrupt-panel identity, missing-anchor position, and foreign-card position are generated independently with nearly uniform frequencies. Each held-out spatial group contributes approximately the same number of cases, so no tiny group dominates either visibility score.
>
> Case Construction
>
> For each case, six anchor sites are selected from a hard local neighborhood inside one protected spatial group. Their three projected encoder views form the initial complete panels. Using related sites rather than six globally unrelated tiles prevents coarse terrain semantics from solving the permutation.
>
> Rows within Panel P and Panel Q are independently shuffled. One target panel is then selected for corruption. One genuine target vector is removed and replaced with a foreign vector.
>
> The foreign site:
>
> is not one of the six anchor sites;
>
> belongs to the same dataset and visibility partition;
>
> comes from a different protected spatial cell;
>
> falls within the same seasonal quarter as the missing site whenever that pool is large enough; and
>
> is selected from the top four matches of an independently sampled 384-site hard-negative pool under the corrupted panel's own embedding space.
>
> These constraints prevent simple outlier detection based on vector norm, seasonal mismatch, or an obviously isolated within-panel vector.
>
> The source views have widths 512, 256, and 1,152 before preparation. Each receives an independent fixed sparse projection and signed square-root transform to the common released width of 192. Centering and scale parameters are fitted only on the 17,600 training sites, then frozen for held-out sites. Transformation seeds and parameters differ between the three panels and are not encoded in identifiers.
>
> Input Representation
>
> Each row in train.csv or test.csv contains:
>
> case_id - opaque unique identifier; and
>
> case_index - zero-based row index into the corresponding tensor pack.
>
> train_cases.npz and test_cases.npz each contain:
>
> anchor_f16 - float16 array with shape [number_of_cases, 6, 192];
>
> panel_p_f16 - float16 array with shape [number_of_cases, 6, 192]; and
>
> panel_q_f16 - float16 array with shape [number_of_cases, 6, 192].
>
> Each array has shape [number_of_cases, 6, 192]. For a CSV row, first select array row case_index. Within that case, row 0 of anchor_f16 corresponds to A0, row 1 to A1, and so on. Row 0 of panel_p_f16 is card P0; row 0 of panel_q_f16 is card Q0.
>
> All released vector values are finite. Each panel is scaled using training-partition statistics fitted before case construction. No participant should fit preprocessing statistics using test cases.
>
> The arrays contain no latitude, longitude, tile name, source identifier, raw image bytes, split label, visibility value, missing-site marker, or foreign-card marker.
>
> Files
> train.csv
>
> Contains:
>
> case_id;
>
> case_index;
>
> p_for_a0 through p_for_a5;
>
> q_for_a0 through q_for_a5; and
>
> corrupt_panel.
>
> test.csv
>
> Contains case_id and case_index. Target columns are withheld.
>
> train_cases.npz
>
> Contains the three packed training arrays anchor_f16, panel_p_f16, and panel_q_f16.
>
> test_cases.npz
>
> Contains the same three packed arrays for test cases. Its row order is deliberately mixed across public and private visibility.
>
> sample_submission.csv
>
> Contains the exact required columns and one formatting row for every test case.
>
> Targets
>
> For each anchor Aj, predict one Panel P token and one Panel Q token.
>
> Valid Panel P tokens are:
>
> P0
>
> P1
>
> P2
>
> P3
>
> P4
>
> P5
>
> MISSING
>
> Valid Panel Q tokens are:
>
> Q0
>
> Q1
>
> Q2
>
> Q3
>
> Q4
>
> Q5
>
> MISSING
>
> corrupt_panel must be P or Q.
>
> The unused card in the corrupted panel is automatically interpreted as the predicted foreign card. No separate foreign-card column is required.
>
> Evaluation
>
> The final submission score ranges from 0.001 to 1.0, and higher is better. Individual case scores range from 0.0 to 1.0. The 0.001 floor is applied only after averaging all evaluated case scores.
>
> For case i, define alignment accuracy over the twelve anchor-panel mappings:
>
> alignment_accuracy_i = (1 / 12) * ( sum over j=0..5 of I(predicted_p_i(Aj) = true_p_i(Aj)) + sum over j=0..5 of I(predicted_q_i(Aj) = true_q_i(Aj)) )
>
> Define corrupted-panel accuracy as:
>
> corrupt_hit_i = I(predicted_corrupt_panel_i = true_corrupt_panel_i)
>
> The anchor assigned MISSING is the predicted missing anchor. Define:
>
> missing_hit_i = I(predicted_missing_anchor_i = true_missing_anchor_i)
>
> The unused card in the corrupted panel is the predicted foreign card. Define:
>
> foreign_hit_i = I(predicted_foreign_card_i = true_foreign_card_i)
>
> Define exact case recovery as:
>
> exact_i = I(all twelve mappings are correct AND corrupt_hit_i = 1 AND missing_hit_i = 1 AND foreign_hit_i = 1)
>
> The per-case score is:
>
> case_score_i = (0.20 * alignment_accuracy_i) + (0.15 * corrupt_hit_i) + (0.10 * missing_hit_i) + (0.10 * foreign_hit_i) + (0.45 * exact_i)
>
> The coefficients sum to 0.20 + 0.15 + 0.10 + 0.10 + 0.45 = 1.00. Exact recovery receives the largest weight because an index repair is operationally complete only when both permutations, the missing anchor, the unused foreign card, and the corrupted panel are jointly correct. Partial components still receive credit, so one imperfect case does not invalidate other cases or the entire submission.
>
> The final score is:
>
> mean_score = (1 / N) * sum over i=1..N of case_score_i score = max(0.001, mean_score)
>
> File-level structural errors receive 0.001 for the complete submission. These errors include missing, extra, duplicated, or reordered columns; missing or extra rows; and missing, unknown, or duplicated case_id values.
>
> Prediction errors are local to one case. A row receives case_score_i = 0 if:
>
> any prediction is blank, non-string, malformed, or surrounded by whitespace;
>
> corrupt_panel is not P or Q;
>
> the complete panel is not an exact six-card permutation;
>
> the corrupted panel does not contain exactly one MISSING and five distinct in-panel cards;
>
> a Panel P column contains a Q token or a Panel Q column contains a P token; or
>
> the panel containing MISSING disagrees with corrupt_panel.
>
> Other valid rows retain their normal scores.
>
> Submission Format
>
> Submit one CSV file with exactly these columns in exactly this order:
>
> case_id
>
> p_for_a0
>
> p_for_a1
>
> p_for_a2
>
> p_for_a3
>
> p_for_a4
>
> p_for_a5
>
> q_for_a0
>
> q_for_a1
>
> q_for_a2
>
> q_for_a3
>
> q_for_a4
>
> q_for_a5
>
> corrupt_panel
>
> A correctly formatted submission begins as follows:
>
>
> case_id,p_for_a0,p_for_a1,p_for_a2,p_for_a3,p_for_a4,p_for_a5,q_for_a0,q_for_a1,q_for_a2,q_for_a3,q_for_a4,q_for_a5,corrupt_panel
>
> SIX7DHHKW5SP5LML,P3,P2,P4,P1,MISSING,P0,Q0,Q2,Q3,Q5,Q4,Q1,P
>
>
> Column names, case identifiers, and prediction tokens are case-sensitive. Blank rows are not allowed.
>
> Training Guidance
>
> This challenge is designed for CPU training from scratch. Useful approaches include:
>
> ridge or partial-least-squares mappings between encoder spaces;
>
> canonical-correlation models learned from training correspondences;
>
> compact multilayer perceptrons over vector pairs;
>
> pairwise compatibility models followed by Hungarian assignment;
>
> cycle-consistency scores across all three panels; and
>
> robust partial matching that evaluates alternative missing and foreign hypotheses.
>
> Direct cosine similarity between panels is not generally meaningful because each view was produced in a different representation space and independently projected. Models should learn compatibility using labeled training cases.
>
> A strong local validation procedure should group cases connected by an identical released vector fingerprint. Sites repeat only within the training partition, so a random case split can otherwise place the same site in both training and validation. Protected geographic group identifiers are intentionally not released.
>
> Expected Output
>
> For every test case, return two anchor-to-panel mappings and the identity of the corrupted target panel. One mapping must be complete; the other must identify one missing anchor and leave one foreign card unused.
>
> What Not to Use
>
> Do not download or search for external copies of the source satellite imagery, embeddings, coordinates, tile metadata, or catalog records.
>
> Do not use vector search against public Earth-observation indexes or attempt to identify released vectors through nearest-neighbor lookup outside the challenge data.
>
> Do not reconstruct latitude, longitude, source filenames, tile identifiers, acquisition timestamps, dataset row numbers, or original encoder outputs.
>
> Do not use pretrained cross-encoder alignment models or checkpoints trained on the source embedding collection. Predictive parameters must be learned from the released training partition.
>
> Do not use case_id, case_index, NPZ compression size, archive order, row order, card-token number, vector byte layout, or floating-point serialization artifacts as predictive features.
>
> Do not treat the vector with the smallest norm, lowest average similarity, or most unusual marginal distribution as automatically foreign. Foreign records are hard matched within the corrupted panel.
>
> Do not manually label test cases, construct test-specific lookup tables, or infer answers through repeated public-leaderboard probing.
>
> Do not access private answers, hidden preparation artifacts, grader internals, or grading-environment data.
>
> General-purpose numerical libraries are allowed. Solutions must learn from the released training cases and generalize to unseen spatial cells, sites, set permutations, missing records, and hard foreign insertions.
>
>  
>
> Submissions
> 6
> Top Score
> 0.649
> Created
> Jul 2, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> 1/12
> solvers beat AI
> How closing works
>
> 4 more distinct solvers needed to activate the $650 prize pool and start the closing countdown. At 12, up to 12 solvers will be selected to continue.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Multi-Mutant Causal-Symptom Relation Graph Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72m6shbqzapnpxghs7krn2158bk6a4
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top score: —

Full challenge description from page:

> Overview
>
> Large migration and compatibility investigations often produce several divergent versions of the same routine. Reviewing every version independently wastes effort: two incidents may touch the same underlying source operation, arise from the same kind of logical mechanism, or produce the same observable failure even when their edited code is different. A useful triage artifact is therefore a relation graph across the whole incident board, not another isolated bug label.
>
> Each case contains two or three Python mutant cards derived from one canonical source program and evaluated under one hidden witness regime. A common natural-language contract and passing Java and C++ implementations provide semantic references. Every Python card contains eight marked intervention proposals. Exactly two hidden interventions are certified as behavior-causing for that card; the other six are witness-neutral distractors.
>
> Reconstruct three graphs over the mutant cards:
>
> the shared-site graph connects mutants whose hidden causal intervention pairs touch at least one common canonical source-token position;
> the same-mechanism graph connects mutants whose hidden causal pairs have the same structural mechanism family; and
> the same-symptom graph connects mutants whose first observed behavioral difference belongs to the same failure-signature family.
>
> The task does not ask for the hidden intervention IDs or any global mechanism or symptom label. It asks only for the complete inter-mutant relations. Candidate IDs, span IDs, and program identifiers are independently relabeled inside every card, so equality of local IDs across two cards is meaningless. A solver must reason about each mutant in context and then construct a globally consistent three-layer graph.
>
> Complete programming contracts are held out from test. All boards derived from one contract remain in the same partition.
>
> Dataset
>
> The public dataset contains exactly three CSV files.
>
> train.csv contains 1,077 labeled relation-graph cases.
> test.csv contains 196 unlabeled cases from held-out programming contracts.
> sample_submission.csv contains one structurally valid prediction for every test case.
>
> The test/train row ratio is approximately 0.182. A case contains either two or three mutant cards.
>
> train.csv Columns
> case_id (string): anonymous unique case identifier.
> mutant_count (integer): number of mutant cards, either 2 or 3.
> task_contract (string): natural-language input/output contract with source examples removed.
> witness_profile (string): anonymized structure of the shared hidden input.
> java_witness (string): normalized passing Java implementation of the contract.
> cpp_witness (string): normalized passing C++ implementation of the contract.
> mutant_bank (JSON string): array containing exactly mutant_count Python mutant objects.
> shared_site_edges (string): target edge ledger for common hidden causal source positions.
> same_mechanism_edges (string): target edge ledger for equal hidden mechanism families.
> same_symptom_edges (string): target edge ledger for equal observed failure-signature families.
> test.csv Columns
>
> test.csv contains the seven feature columns case_id, mutant_count, task_contract, witness_profile, java_witness, cpp_witness, and mutant_bank. It omits all three edge-ledger targets.
>
> sample_submission.csv Columns
> case_id (string): identifier copied from test.csv.
> shared_site_edges (string): predicted shared-site edge ledger.
> same_mechanism_edges (string): predicted same-mechanism edge ledger.
> same_symptom_edges (string): predicted same-symptom edge ledger.
> Mutant Object Schema
>
> Each object in mutant_bank has exactly three fields.
>
> mutant_id (string): case-local node ID, M0, M1, or M2.
> target_program (string): normalized Python token stream containing eight intervention markers.
> intervention_candidates (string): eight semicolon-separated intervention atoms.
>
> target_program uses <NL>, <INDENT>, and <DEDENT> for program structure. Names such as v_007 are mutant-local identifiers. An intervention marker such as <E3:L4> identifies local intervention E3 at local span L4.
>
> Every intervention atom has the form intervention_id@span_id:observed_operator>proposed_operator. For example:
>
> E3@L4:GE>GT
>
> Operator codes are EQ, NE, LT, LE, GT, GE, ADD, SUB, MUL, FDIV, MOD, AND, and OR.
>
> Candidate IDs E0 through E7, span IDs L0 through L7, and v_### identifiers are independently assigned in each mutant. They do not form cross-mutant keys.
>
> Hidden Relation Definitions
>
> The hidden mechanism family is determined by the two certified interventions:
>
> Boolean-flow: at least one certified intervention changes AND or OR.
> Dual-guard: both certified interventions change comparison operators.
> Dual-value: both certified interventions change arithmetic operators.
> Guard-value: one certified intervention changes a comparison and the other changes arithmetic.
>
> The hidden symptom family is the first observed difference from canonical behavior:
>
> non-termination;
> runtime failure;
> changed output-line count;
> unchanged line count but changed output-token count; or
> unchanged output shape with changed values.
>
> The output graphs encode equality of these hidden families, not the family names themselves.
>
> Submission
>
> Submit a CSV with exactly four columns in this order:
>
> case_id,shared_site_edges,same_mechanism_edges,same_symptom_edges
>
> An edge atom has the form Mi~Mj, with the lower mutant ID first. Use semicolons between multiple atoms, list atoms in lexical order, and add no whitespace. Use the literal NONE when a graph has no edges.
>
> Example rows:
>
> case_id,shared_site_edges,same_mechanism_edges,same_symptom_edges
> MMG_0123456789abcde,M0~M2,M0~M1;M1~M2,NONE
> MMG_abcdef012345678,NONE,M0~M1,M0~M1
>
> For a two-mutant case, the only available edge is M0~M1. For a three-mutant case, the available edges are M0~M1, M0~M2, and M1~M2.
>
> Every required test ID must appear exactly once. Additional platform rows outside the scored answer set are ignored after required-ID and duplicate-ID validation. Null ledgers, missing IDs, duplicate IDs, or unexpected columns invalidate the submission. A non-null malformed ledger is treated as incorrect for every possible pair in that relation layer and cannot receive exact-case credit.
>
> Evaluation
>
> The score is bounded in [0, 1], where higher is better.
>
> For each relation layer, every case-qualified unordered mutant pair is one binary decision. Positive and negative decisions are pooled over all scored cases. Let F1_positive be standard F1 for relation edges and F1_negative be standard F1 after treating non-edges as the positive class.
>
> BinaryMacroF1 = (F1_positive + F1_negative) / 2
> RelationSkill = max(0, (BinaryMacroF1 - 0.5) / 0.5)
>
> The 0.5 reference removes the balanced random-classification floor while rewarding both recovered edges and recovered non-edges.
>
> The three layer components are:
>
> SharedSiteSkill: RelationSkill for shared_site_edges.
> SameMechanismSkill: RelationSkill for same_mechanism_edges.
> SameSymptomSkill: RelationSkill for same_symptom_edges.
>
> ExactMultiplexGraphAccuracy is the fraction of cases for which all three complete edge sets match exactly.
>
> The final score is:
>
> Score = 0.35 * SharedSiteSkill + 0.25 * SameMechanismSkill + 0.25 * SameSymptomSkill + 0.15 * ExactMultiplexGraphAccuracy
>
> Each component appears once, the weights sum to 1.0, and a perfect submission scores 1.0.
>
> Allowed And Prohibited Methods
> Allowed
> CPU-compatible code representations, sparse text models, graph models, compact encoders, pairwise classifiers, and constrained graph decoding.
> Models trained exclusively from the supplied public files.
> Validation grouped by complete programming contract.
> Program normalization and candidate-context features derived only from public fields.
> Prohibited
> Searching online judges, repositories, benchmark releases, or external corpora for supplied contracts or programs.
> Reconnecting cases to original problem, submission, source-file, or witness identities.
> Executing hidden source tests, recovering private witness literals, or retrieving external clean implementations.
> Hardcoded test graphs, row-order rules, or source-identity lookup systems.
>
>  
>
> Submissions
> 0
> Top Score
> —
> Created
> Jul 31, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> 0/12
> solvers beat AI
> How closing works
>
> Be the first to solve this challenge! 5 distinct solvers with graded solutions are needed to activate the $650 prize pool and start a closing countdown. At 12, up to 12 solvers will be selected to continue.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Lightning Skeletons: 4D Discharge Gap Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7crszwprwgnjn39yxqdt74f98amekx
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top score: —

Full challenge description from page:

> Objective
>
> A rapid atmospheric discharge leaves a branching cloud of radio sources in three dimensions. A telemetry failure erased the middle 30 percent of each discharge. The system retained a thinned point cloud before the gap, another after the gap, and a spatially blind radio envelope recorded during the missing interval.
>
> The original measurements come from synchronized ground receivers that triangulate brief radio impulses. Each detected impulse carries a three-dimensional position, relative time, signal power, receiver-support count, and fit-quality value. Challenge preparation converts every discharge into a private local coordinate frame, so the released values describe its internal branching geometry rather than a place, date, or observing campaign.
>
> Recover the hidden four-dimensional source skeleton and its power field. This is interpolation through a missing causal interval, not future forecasting: both severed ends are visible, but the branches that connected them are not.
>
> Files
>
> train.csv columns are row_id,context_points,gap_radio,gap_skeleton,gap_power.
>
> test.csv columns are row_id,context_points,gap_radio.
>
> sample_submission.csv and every valid submission use exactly row_id,gap_skeleton,gap_power, in that order.
>
> Rows are aligned by row_id; row order does not matter.
>
> Input Representation
>
> All array cells are flat JSON lists. Every numeric value lies in [0,1].
>
> row_id is an opaque scalar string join key with no physical or chronological meaning.
> context_points reshapes to 192 x 8: up to 96 sources before the gap followed by up to 96 sources after the gap.
> gap_radio reshapes to 12 x 3: spatially blind activity recorded across the erased interval.
>
> The eight context_points features are, in order: normalized x, normalized y, normalized altitude, normalized flash time, normalized source power, station-support fraction, location quality, and valid.
>
> The first 96 slots have time below 0.35; the final 96 slots have time above 0.65. Unused slots are all zero with valid = 0. Ignore padded slots. Coordinates are row-local: orientation, origin, and scale do not identify a real location.
>
> The three gap_radio features are, in order: fraction of hidden sources in the time bin, fraction of hidden power in the time bin, and mean location quality. The first two channels each sum to approximately one across 12 bins. They reveal when hidden activity occurred, not where it occurred.
>
> Targets and Submission
>
> Both outputs reshape to 6 x 5 x 8 x 8, ordered as time, altitude, y, x and flattened in C order. Each output therefore contains exactly 1,920 numbers.
>
> gap_skeleton is binary in training data. A submission may use soft values in [0,1] to express occupancy confidence.
>
> gap_power is normalized log-accumulated source power on the same grid. Submit values in [0,1].
>
> The flat index of cell (t,z,y,x) is:
>
> index = (((t * 5) + z) * 8 + y) * 8 + x
>
> Each prediction cell must be a valid JSON list of exactly 1,920 finite JSON numbers. Boolean values are not numbers for this task.
>
> Sample Submission Preview
>
> The downloadable sample_submission.csv contains all 947 required test IDs and complete 1,920-value arrays. This three-row preview abbreviates each all-zero array only for readability:
>
> row_tzzmjdjbbvzmhgusvhqe — gap_skeleton = [0.0, ..., 0.0] (1,920 values); gap_power = [0.0, ..., 0.0] (1,920 values).
> row_ezeqpynjjjjbjqamxcmu — gap_skeleton = [0.0, ..., 0.0] (1,920 values); gap_power = [0.0, ..., 0.0] (1,920 values).
> row_bxuubepswqnxmatdtauu — gap_skeleton = [0.0, ..., 0.0] (1,920 values); gap_power = [0.0, ..., 0.0] (1,920 values).
>
> The ellipses are not literal file contents. Every actual sample cell is valid JSON with exactly 1,920 zeros.
>
> Data-Backed Illustration
>
> For one released training row, the first three valid context points are:
>
> [0.55713,0.42676,0.62109,0.00000,0.46167,0.66650,0.83008,1.00000]
> [0.61328,0.41089,0.61963,0.01662,0.65674,0.77783,0.83008,1.00000]
> [0.54639,0.41821,0.63867,0.02068,0.64990,1.00000,0.66992,1.00000]
>
> Its first three spatially blind gap bins are:
>
> [0.11957,0.11731,0.48682]
> [0.06525,0.06042,0.43823]
> [0.15222,0.14478,0.57227]
>
> That row has 49 occupied hidden voxels. For example, flat target indices 164, 180, and 224 are occupied, with power values 0.25073, 0.18262, and 0.16895. These excerpts explain the layout; a valid submitted array still requires all 1,920 positions.
>
> Evaluation
>
> Let p_s and y_s be predicted and true skeleton tensors. Fine soft intersection-over-union is:
>
> fine_iou = sum(p_s * y_s) / sum(p_s + y_s - p_s * y_s)
>
> Max-pool each nonoverlapping 2 x 2 horizontal neighborhood while preserving time and altitude. Apply the same soft-IoU formula to the resulting 6 x 5 x 4 x 4 tensors to obtain coarse_iou.
>
> skeleton_quality = 0.75 * fine_iou + 0.25 * coarse_iou
>
> Let p_p and y_p be predicted and true power tensors, and let P = sum(p_p) and Y = sum(y_p). If either mass is zero, power_quality = 0. Otherwise:
>
> affinity = sum(sqrt(p_p * y_p)) / sqrt(P * Y)
> mass_ratio = min(P,Y) / max(P,Y)
> power_quality = affinity * sqrt(mass_ratio)
>
> The row and final scores are:
>
> row_score = sqrt(skeleton_quality * power_quality)
> score = mean(row_score)
>
> The geometric mean makes both outputs necessary. The score is clipped to [0,1]; higher is better. Exact answers score 1, and the all-zero sample scores 0.
>
> Invalid Predictions
>
> A malformed JSON cell, wrong vector length, nonnumeric or Boolean item, nonfinite value, or value outside [0,1] gives that row a score of zero. Missing, duplicate, unknown, or extra IDs; an empty submission; or any change to the exact column names or order rejects the entire submission with ValueError.
>
> Split and Generalization
>
> Each row is one discharge object. Complete source groups are assigned wholly to train or test before row construction. Absolute location, acquisition time, source filenames, original identifiers, and source order are removed. Test groups never appear in training.
>
> Boundary Against Nearby Tasks
>
> Operational lightning learning tasks usually predict regional occurrence, classify waveforms, or cluster already observed sources into flashes. Generic point-cloud completion usually reconstructs static object surfaces or driving scenes. This benchmark instead reconstructs the missing middle of one fast branching atmospheric process from two irregular 3-D temporal fragments plus a location-free gap sensor, and scores both hidden 4-D topology and calibrated power under group-disjoint transfer.
>
> Prohibited Shortcuts
>
> Do not identify, redownload, reverse-search, or match external source records to recover hidden targets. Do not use leaked acquisition metadata, filenames, original flash identifiers, organizer audit fields, private preparation artifacts, row order, or platform internals. Train from the released public challenge files and generally available modeling software.
>
> Resource Limit
>
> Solutions must run on CPU only, using at most 10 CPU cores, 62.5 GiB RAM, and 90 minutes.
>
> Submissions
> 0
> Top Score
> —
> Created
> Jul 16, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> 0/12
> solvers beat AI
> How closing works
>
> Be the first to solve this challenge! 5 distinct solvers with graded solutions are needed to activate the $650 prize pool and start a closing countdown. At 12, up to 12 solvers will be selected to continue.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Grid Puzzle Response Ranking

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75genss6we5f7eq7vq8vqmw18dskv4
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.609

Full challenge description from page:

> Overview
>
> Solvers are given short symbolic grid-transformation puzzles: a handful of demonstration pairs that each show an input grid and its transformed output grid, followed by a single query input grid. Each puzzle has one hidden correct transformation, but this competition is not about producing that correct output. Instead, for every query puzzle you are given a fixed set of ten candidate output grids — a mix of grids that members of a large respondent population actually produced when attempting the puzzle, together with filler grids nobody produced — and you must rank and weight the ten candidates by each grid's conditional selection share: among the respondents whose response is one of these ten candidate grids, the fraction who produced each grid. The correct answer is deliberately withheld from every candidate set, so this is a response-frequency task, not a correctness task.
>
> The target is a conditional distribution, not a raw population share. It is restricted to the candidate grids shown — degenerate grids that recur across many unrelated puzzles and the long low-frequency tail of rare responses are excluded, and the remaining shares are renormalized to sum to 1 over the ten candidates. Selection within this conditional distribution is far from uniform. On abstract grid-transformation problems a respondent population converges on a small number of characteristic answers: they get the grid dimensions right but the coloring wrong, apply a rule to the wrong region, stop one transformation step early, or over-generalize a partial pattern visible in the demonstrations. As a result the mass concentrates on a few candidates while the filler grids carry none. The filler grids are artifact-matched — each is a genuine human-error grid taken from a different puzzle, matched to this puzzle's grid dimensions and recolored into this puzzle's own color palette — so they cannot be told apart from real responses by surface features alone; distinguishing them requires reasoning about the puzzle. The data spans hundreds of distinct puzzles that vary widely in difficulty, in how many respondents attempted them, and in how concentrated versus spread-out the conditional shares are — capturing that concentration correctly is a core part of the task.
>
> Dataset
>
> The dataset contains 680 puzzles: 400 in train.csv and 280 in test.csv. Every candidate set holds exactly ten grids, of which 3–7 are population-produced response grids and the rest are artifact-matched filler grids.
>
> Public files
> public/train.csv — 400 rows, one per training puzzle. Columns: puzzle_id, support, query_input, candidates, and the target columns score_a … score_j.
> public/test.csv — 280 rows, one per test puzzle. Columns: puzzle_id, support, query_input, candidates. (The score_* target columns are withheld — that is what you predict.)
> public/sample_submission.csv — a valid baseline submission. Columns: puzzle_id, score_a, score_b, score_c, score_d, score_e, score_f, score_g, score_h, score_i, score_j.
> Private file (organizer only)
> private/answers.csv — the held-out conditional selection shares for each test puzzle. Columns: puzzle_id, score_a … score_j (identical column names to the sample submission), where each score_x holds the normalized conditional selection share of candidate x for that puzzle — among the respondents whose response is one of the ten candidate grids, the fraction who produced candidate grid x — summing to 1 across the ten candidates. Filler candidates that no respondent produced carry a share of 0.
> Column descriptions
>
> The public files use the following columns.
>
> puzzle_id (string) — Generic unique identifier for a puzzle (e.g. puz_0001). Carries no information about the source or difficulty.
> support (JSON string) — The demonstration set for the puzzle: a JSON list of [input_grid, output_grid] pairs. Each grid is a JSON 2-D array of integers in 0–9 (each integer denotes a cell color). A puzzle has 1–10 demonstration pairs; grid heights and widths range from 1 to 30 and may differ between input and output.
> query_input (JSON string) — The single query input grid for the puzzle, in the same nested-integer-array format. The (unseen) correct output of this grid is what respondents were trying to produce; it is not provided and is not among the candidates.
> candidates (JSON string) — A JSON object mapping the ten candidate labels a–j to candidate output grids (nested integer arrays). Each candidate is either a grid that at least one respondent produced, or an artifact-matched filler grid (a real human-error grid from a different puzzle, dimension-matched and recolored into this puzzle's palette); exactly ten per puzzle, in a fixed label order. The correct solution grid is never included.
> score_a … score_j (float, train only) — The target for each candidate a–j: the normalized conditional selection share — among respondents whose response is one of the ten candidate grids, the fraction who produced that candidate grid — summing to 1 across the ten candidates (filler grids carry 0). Provided for training puzzles only; withheld for test puzzles. These are the same columns you submit for the test set.
> Data example
>
> A single (truncated) train.csv row:
>
> puzzle_id,support,query_input,candidates,score_a,score_b,score_c,score_d,score_e,score_f,score_g,score_h,score_i,score_j  
> puz_0001,"[[[[0,0],[0,5]],[[5,5],[5,0]]],[[[0,5],[0,0]],[[5,0],[5,5]]]]","[[0,0,0],[0,5,0],[0,0,0]]","{""a"": [[5,5,5],[5,0,5],[5,5,5]], ""b"": [[0,0,0],[0,0,0],[0,0,0]], ""c"": [[5,5,5],[5,5,5],[5,5,5]], ""d"": [[0,5,0],[5,0,5],[0,5,0]], ""e"": [[0,0,0],[0,5,0],[0,0,0]], ""f"": [[5,0,5],[0,5,0],[5,0,5]], ""g"": [[0,0,5],[0,5,0],[5,0,0]], ""h"": [[5,5,0],[5,0,0],[0,0,0]], ""i"": [[0,0,0],[5,5,5],[0,0,0]], ""j"": [[9,9,9],[9,9,9],[9,9,9]]}",0.4,0.257,0.086,0.171,0.057,0.029,0.0,0.0,0.0,0.0  
>
> The score_* columns above (a training row) hold the normalized conditional selection shares; test rows omit them.
>
> Split and anti-memorization
>
> Puzzles are partitioned so that the underlying transformation puzzles are disjoint across train and test — no puzzle (and none of its demonstration grids, query grid, or candidate grids) appears in both splits. The selection shares being ranked are therefore held out at the puzzle level: a solver cannot memorize training targets and must generalize to puzzles it has never seen. Only the abstract vocabulary (the ten integer colors, the grid format, the candidate-labeling scheme) is shared between splits. Each candidate set is fixed at exactly ten grids so that every submission row has the same width.
>
> Submission format
>
> Submit a CSV with a header and exactly one row per test puzzle. Required columns, in order:
>
> puzzle_id, score_a, score_b, score_c, score_d, score_e, score_f, score_g, score_h, score_i, score_j
>
> For each puzzle the ten score_x values are nonnegative weights over the candidate set — your estimate of each candidate's selection share — normalized to a probability vector: every score_x must be ≥ 0 and the ten values must sum to 1 (a tolerance of 0.02 is allowed and the row is renormalized before scoring). The weights are used two ways (see Evaluation): the order they induce over the candidates, and the magnitude of each weight. Values that are equal at a resolution of 1e-6 are treated as tied and credited at the expected value over the tied block. Every candidate label a–j must receive a value. Extra columns, missing columns, missing puzzles, unknown puzzles, negative values, rows that do not sum to 1, and non-numeric values are rejected.
>
> Sample submission (uninformative uniform baseline — every candidate assigned equal weight 0.1):
>
> puzzle_id,score_a,score_b,score_c,score_d,score_e,score_f,score_g,score_h,score_i,score_j  
> puz_1001,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1  
> puz_1002,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1  
> Evaluation
>
> The metric is Response Ranking Calibration (RRC), macro-averaged over test puzzles. It blends how well a submission orders the candidates the population actually produced with how well it calibrates the weight magnitudes against the true conditional selection shares, minus a filler penalty.
>
> For one puzzle, let p be the true normalized conditional selection shares over the ten candidates (from private/answers.csv, Σ_c p_c = 1) and q the submitted weight vector (renormalized to sum to 1). Ranks are induced by q (rank 1 = highest weight); ties are credited at the expected value over the tied block, so an honest uniform prediction is neither rewarded nor punished relative to information-free jitter.
>
> # (1) normalized ranking term — expected reciprocal rank of a randomly drawn  
> #     response, affinely rescaled so a chance (uniform) order -> 0 and the  
> #     ideal descending-p order -> 1. No per-puzzle clip (jitter-safe).  
> base   = sum(p_c * E[1.0 / rank_c(q)] for c in candidates)     # expected-tie recip rank  
> chance = (1/10) * sum(1.0 / r for r in 1..10)                  # ~0.293 (fully-tied base)  
> ideal  = sum(sorted(p, desc)[r-1] * (1.0 / r) for r in 1..10)  # base of the ideal order  
> nrank  = 0.0 if (ideal - chance) <= 0 else (base - chance) / (ideal - chance)  
>   
> # (2) calibration term — L1 closeness of q to p, recentered so the uniform  
> #     vector -> 0 and an exact match -> 1, clipped to [0, 1].  
> l1sim(x) = 1 - 0.5 * sum(abs(p_c - x_c) for c in candidates)  
> cal      = clip((l1sim(q) - l1sim(uniform)) / (1 - l1sim(uniform)), 0, 1)  
>   
> # (3) filler penalty — candidates with p_c == 0 that q ranks in the top 3  
> n_filler_top3 = E[count(c for c in candidates if p_c == 0 and rank_c(q) <= 3)]  
> penalty = LAMBDA * (n_filler_top3 / 3.0)                       # LAMBDA = 0.15  
>   
> puzzle_score = W_RANK * nrank + W_CAL * cal - penalty          # W_RANK=0.4, W_CAL=0.6; may go negative  
> RRC          = max(0.02, mean(puzzle_score over test puzzles)) # floored, capped at 1.0  
> nrank (W_RANK = 0.4) rewards placing the grids the population actually produced near the top of the ranking. It is affinely normalized per puzzle so a chance ordering scores 0 and the ideal descending-p ordering scores 1, regardless of how concentrated or spread-out that puzzle's conditional shares are.
> cal (W_CAL = 0.6) measures how closely the magnitudes of q match p, not only their order: it is the L1 closeness of q to p, recentered so the uniform vector scores 0 and an exact match scores 1.
> penalty (LAMBDA = 0.15) subtracts for ranking implausible filler grids (candidates no respondent produced) into the top three. It is applied after the positive terms (never as a multiplier on them), so it always makes a submission worse.
> The headline RRC is the equal-weight mean of puzzle_score across all test puzzles, then floored at 0.02 and capped at 1.0.
>
> Baseline (uniform / chance). The uniform sample submission scores nrank = 0 and cal = 0 on every puzzle and, after the filler penalty, sits at the floored chance level (≈ 0.02). A submission whose weights match the true selection shares exactly scores 1.0.
>
> Grade bounds. Grade direction is Maximize, with Min Score = 0.02 and Max Score = 1.0. The reported RRC is floored at 0.02 (so no valid submission returns 0.0) and capped at 1.0 (attained only by an exact match to the true conditional shares), so the score always lies in [0.02, 1.0].
>
> Higher is better. RRC is maximized when q matches the true selection shares p — correct ordering, correct magnitudes, and zero-share filler grids kept out of the top three.
>
> What Not To Use (Prohibited Methods)
> No external answer keys, no hardcoded puzzle_id-to-score mappings, and no memorized lookups of any kind.
> No train/test leakage: do not use any test-puzzle target information; the selection shares for test puzzles are private.
> No private-label tuning: do not attempt to infer or fit against private/answers.csv.
> Do not match the puzzles, demonstration grids, query grids, or candidate grids back to any external public puzzle collection, competition, or solution repository to recover a puzzle's identity or its correct solution. The correct solution is deliberately excluded from every candidate set, so this cannot directly reveal the target — but reconstructing puzzle provenance to import outside metadata is prohibited.
> Do not use any external dataset of response frequencies, selection logs, or aggregate answer counts for these or similar grid puzzles to recover the test targets. The selection shares must be predicted, not looked up.
> Do not manually annotate or estimate the selection shares for individual test puzzles by hand.
> Do not exploit candidate label order, set position, or any structural artifact of test.csv as a proxy for the target; the candidate order within each set carries no target signal.
>
>  
>
> Submissions
> 11
> Top Score
> 0.609
> Created
> Sep 4, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> 5/12
> solvers beat AI
> Closing soon
>
> Prize pool active — closing countdown started. At 12, up to 12 solvers will be selected to continue.
>
> Closing in 11h 51m
>
> Submit your solution before the deadline. Payouts are processed after the challenge closes.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Clinical Trial Outcome-Timeframe Allocation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a3vj4q2bkz3jvg7zky16p4s8astgb
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.292

Full challenge description from page:

> Overview
>
> Each test case contains three outcome descriptions and three shuffled schedule profiles from one completed interventional clinical trial. Predict which schedule belongs to each outcome. The answer is a one-to-one assignment of the three outcomes to the three candidates.
>
> The linked source corpus was curated from the official ClinicalTrials.gov API v2 and processed on July 18, 2026. It contains study-level registry metadata for completed interventional studies, not patient records or individual clinical measurements. Sponsors or investigators submit each registered primary outcome as a measure name, a descriptive protocol field, and an assessment timeframe. The source corpus retained studies with at least three distinct, sufficiently complete primary-outcome relationships.
>
> Nested registry fields can become detached during schema migration, record normalization, or quality-control reconciliation. In that setting, the outcome definitions and the pool of schedules may remain available even though their links have been lost. This challenge reconstructs those authentic registry links from the clinical meaning of each outcome, the brief study context, and a compact profile of each candidate schedule.
>
> Each target is an original relationship from a completed interventional study. Targets are not generated from keywords or synthetic rules. The public candidate cards do not contain the original timeframe prose. Instead, each card contains stable schedule-profile tokens describing horizon, schedule shape, event anchor, repetition, duration count, and temporal spread. Models must learn how those profiles relate to clinical outcomes from the labeled training cases.
>
> This is not temporal named-entity extraction, outcome classification, or natural-language sentence matching. The model must infer three authentic cross-representation links jointly: free-text clinical outcome evidence is aligned to structured schedule profiles under a one-use-per-candidate constraint, and performance is tested under three complementary evidence views and unseen sponsor groups.
>
> Dataset
>
> All released files are under the public directory supplied to the solution.
>
> train.csv: 1,284 labeled allocation cases.
>
> test.csv: 429 held-out allocation cases without assignment_sequence.
>
> sample_submission.csv: a structurally valid submission generated independently of the hidden targets.
>
> The 1,713 cases come from 571 eligible source studies. Every source study contributes three evidence views. Training contains 428 source studies, and test contains 143 different source studies. Multiple studies can share the same normalized lead sponsor, so the 428 training studies belong to 254 sponsor groups and the 143 test studies belong to 117 sponsor groups. The test partition contains 25.04% of eligible studies, and its row count is 33.41% of the training row count. The split is disjoint by sponsor group: none of the 117 test groups occurs among the 254 training groups.
>
> A source study is retained only when all three public schedule profiles are distinct and all three outcome cards retain sufficient distinguishable evidence after masking. Consequently, no train or test row contains duplicate normalized schedule candidates.
>
> Raw trial identifiers, sponsor names, dates, original timeframe prose, and exact duration values are absent from the public files. Public case IDs are derived from a fingerprint of the complete private source record rather than directly from a trial identifier.
>
> Columns
>
> | Column | Type | Availability | Description |
>
> |---|---|---|---|
>
> | case_id | string | Train and test | Opaque unique case identifier. |
>
> | evidence_view | string | Train and test | One of BALANCED, MEASURE_FOCUS, or DESCRIPTION_FOCUS. |
>
> | study_context | string | Train and test | Leakage-controlled study-title context. |
>
> | outcome_cards_json | JSON string | Train and test | Three outcome cards with outcome_id, measure, and description. |
>
> | timeframe_candidates_json | JSON string | Train and test | Three shuffled candidates with timeframe_id and schedule_tokens. |
>
> | assignment_sequence | string | Train only | Correct one-to-one assignment. |
>
> Evidence Views
>
> The three views test whether a model can recover the same type of relationship when different amounts of outcome evidence are available:
>
> BALANCED: up to 48 measure tokens and 150 description tokens.
>
> MEASURE_FOCUS: up to 64 measure tokens and 32 description tokens.
>
> DESCRIPTION_FOCUS: up to 14 measure tokens and 190 description tokens.
>
> Outcome order, candidate order, public case ID, and row-local lexical aliases are independently reconstructed for every view. A view does not reveal the identity of its source study.
>
> Outcome Text
>
> Common clinical and methodological language remains readable. Direct duration expressions and temporal anchor words become temporal_reference; other numbers become number_reference. Less-common words become row-local lex_* aliases. The aliases preserve repeated concepts within one case but cannot be used as a global vocabulary or source-record key.
>
> Schedule Profiles
>
> Every candidate has the following form:
>
>
> {
>
>   "timeframe_id": "T2",
>
>   "schedule_tokens": ["H_16", "S_05", "A_02", "R_00", "N_1", "W_00"]
>
> }
>
>
> The token families and their meanings are fixed across train and test. A profile may contain more than one H_* or A_* token when the source schedule contains multiple horizons or event anchors.
>
> Horizon Tokens
>
> Explicit times are converted to days and placed into the following ordered bands. The lower endpoint of every interval is exclusive and the upper endpoint is inclusive.
>
> | Token | Concrete horizon |
>
> |---|---|
>
> | H_00 | Exactly 0 days, including an explicit baseline reference. |
>
> | H_01 | More than 0 and up to 1 hour. |
>
> | H_02 | More than 1 and up to 6 hours. |
>
> | H_03 | More than 6 and up to 12 hours. |
>
> | H_04 | More than 12 hours and up to 1 day. |
>
> | H_05 | More than 1 and up to 2 days. |
>
> | H_06 | More than 2 and up to 3 days. |
>
> | H_07 | More than 3 and up to 5 days. |
>
> | H_08 | More than 5 and up to 7 days. |
>
> | H_09 | More than 7 and up to 10 days. |
>
> | H_10 | More than 10 and up to 14 days. |
>
> | H_11 | More than 14 and up to 21 days. |
>
> | H_12 | More than 21 and up to 28 days. |
>
> | H_13 | More than 28 and up to 42 days. |
>
> | H_14 | More than 42 and up to 56 days. |
>
> | H_15 | More than 56 and up to 84 days. |
>
> | H_16 | More than 84 and up to 112 days. |
>
> | H_17 | More than 112 and up to 168 days. |
>
> | H_18 | More than 168 and up to 252 days. |
>
> | H_19 | More than 252 and up to 365 days. |
>
> | H_20 | More than 365 and up to 548 days. |
>
> | H_21 | More than 548 and up to 730 days. |
>
> | H_22 | More than 730 and up to 1,095 days. |
>
> | H_23 | More than 1,095 and up to 1,825 days. |
>
> | H_24 | More than 1,825 and up to 3,650 days. |
>
> | H_25 | More than 3,650 days. |
>
> | H_99 | No explicit numeric horizon or baseline reference was parsed. |
>
> Minutes, hours, weeks, months, and years are normalized using 1 day = 24 hours, 1 week = 7 days, 1 month = 30.4375 days, and 1 year = 365.25 days.
>
> Schedule-Shape Tokens
>
> | Token | Concrete meaning |
>
> |---|---|
>
> | S_00 | No listed shape pattern was detected. |
>
> | S_01 | Change-from-baseline or change-in wording. |
>
> | S_02 | Cumulative window, such as up to, throughout, until, or over the course. |
>
> | S_03 | Explicit from-to interval. |
>
> | S_04 | During or through an interval. |
>
> | S_05 | Post-event timing, such as after, post, or following. |
>
> | S_06 | Pre-event timing, such as before, pre, or prior to. |
>
> | S_07 | Point timing expressed with at or on. |
>
> | S_08 | Completion-relative timing, including end of, last visit, or study duration. |
>
> Exactly one S_* token appears in each profile. When multiple patterns occur, priority is S_01, S_02, S_03, S_04, S_05, S_06, S_07, then S_08; S_00 is the fallback.
>
> Event-Anchor Tokens
>
> | Token | Concrete anchor family |
>
> |---|---|
>
> | A_00 | No listed anchor family was detected. |
>
> | A_01 | Dose, administration, infusion, or injection. |
>
> | A_02 | Treatment, intervention, or therapy. |
>
> | A_03 | Surgery, procedure, operation, or extraction. |
>
> | A_04 | Discharge. |
>
> | A_05 | Randomization, enrollment, inclusion, or recruitment. |
>
> | A_06 | Visit. |
>
> | A_07 | Cycle. |
>
> | A_08 | Diagnosis. |
>
> | A_09 | Vaccination or immunization. |
>
> | A_10 | Follow-up. |
>
> | A_11 | Study-relative anchor. |
>
> | A_12 | Screening. |
>
> All detected anchor families are included, so a profile can contain several A_* tokens. A_00 appears only when none of A_01 through A_12 applies.
>
> Repetition, Count, And Spread Tokens
>
> | Token | Concrete meaning |
>
> |---|---|
>
> | R_00 | No repetition cue and no multi-horizon punctuation pattern. |
>
> | R_01 | Multiple parsed horizons or list/range wording. |
>
> | R_02 | Explicit periodic wording such as every, daily, weekly, monthly, each, or repeated; this takes priority over R_01. |
>
> | N_0 | No explicit duration value was parsed. |
>
> | N_1 | One distinct duration value was parsed. |
>
> | N_2 | Two distinct duration values were parsed. |
>
> | N_3 | Three distinct duration values were parsed. |
>
> | N_4 | Four or more distinct duration values were parsed. |
>
> | W_00 | Fewer than two horizons, or adjusted latest-to-earliest ratio below 1.5. |
>
> | W_01 | Adjusted latest-to-earliest ratio from 1.5 up to, but not including, 3. |
>
> | W_02 | Adjusted latest-to-earliest ratio from 3 up to, but not including, 10. |
>
> | W_03 | Adjusted latest-to-earliest ratio of 10 or greater. |
>
> For W_*, the adjusted ratio is (latest_days + 1) / (earliest_days + 1). Every profile contains exactly one R_*, one N_*, and one W_* token. The profile is fully documented, but its compatibility with each clinical outcome must still be learned from the authentic assignments in train.csv; candidate strings cannot be matched lexically to outcome prose.
>
> Task And Submission
>
> For each case_id, submit an assignment_sequence containing exactly three space-separated pairs:
>
>
> O1=T# O2=T# O3=T#
>
>
> O1, O2, and O3 identify the outcome cards. T1, T2, and T3 identify the shuffled schedule candidates. Every outcome and every candidate must be used exactly once.
>
> Example:
>
>
> case_id,assignment_sequence
>
> CTF_0123456789abcdef,O1=T2 O2=T3 O3=T1
>
> CTF_fedcba9876543210,O1=T1 O2=T3 O3=T2
>
>
> The submission must be a UTF-8 CSV with exactly the columns case_id,assignment_sequence in that order. It must contain every test ID exactly once, with no missing, duplicate, or additional IDs. Malformed assignments are rejected.
>
> Evaluation
>
> The metric is chance-corrected structured allocation accuracy. Higher is better, and scores range from 0 to 1.
>
> For each row:
>
> FieldAccuracy is the fraction of the three outcomes assigned to the correct schedule.
>
> ExactAllocation is 1 only when the entire three-pair permutation is correct, and 0 otherwise.
>
> First compute:
>
>
> raw_score = 0.75  *mean(FieldAccuracy) + 0.25*  mean(ExactAllocation)
>
>
> A uniformly random valid permutation has expected FieldAccuracy = 1/3 and expected ExactAllocation = 1/6, so its expected raw score is:
>
>
> chance_raw = 0.75  *(1/3) + 0.25*  (1/6) = 7/24
>
>
> The reported score is:
>
>
> score = clip((raw_score - 7/24) / (1 - 7/24), 0, 1)
>
>
> This assigns approximately 0 to random valid allocation while preserving a perfect score of 1.
>
> Runtime And Method Rules
>
> The platform runs:
>
>
> python3 [solution.py](http://solution.py) <public_dir> <submission_out>
>
>
> Training and inference must run on CPU. Read only from <public_dir> and write the final CSV to the exact <submission_out> path. The full run may use at most 10 CPU cores, 62 GB RAM, and 1.5 hours.
>
> Allowed approaches include structured matching, learned compatibility models, compact sequence encoders trained on the released rows, permutation scoring, bipartite assignment, and compliant ensembles.
>
> Do not use external clinical-registry data, source archives, web search, network retrieval, hosted inference APIs, private files, challenge-generation artifacts, or challenge-specific pretrained checkpoints. Do not attempt to reconstruct trial identifiers, sponsors, source pages, preparation fingerprints, or hidden original timeframe text. Do not use hardcoded test IDs, candidate positions, row order, or fixed answer maps.
>
> A valid solution must learn from the public labeled cases, use both the outcome evidence and candidate schedule profiles, and generalize to unseen sponsor groups.
>
>  
>
> Submissions
> 30
> Top Score
> 0.292
> Created
> Jul 18, 2026
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> 12/12
> continuing solver slots
> Lockdown
>
> The 12-solver continuing roster was selected from the standings after the one-hour grace period.
>
> Closing in 7h 47m
>
> Submit your solution before the deadline. Payouts are processed after the challenge closes.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Executable Rule-Patch Synthesis from Anonymous Historical Game Traces

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx744f5x15jwxeajp740se1g1n8akpqx
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Draft
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Overview In plain language: Work out the missing rules of an anonymous board game from examples of which moves work, how pieces change, and how play ends. For each test episode, submit those rules as a small executable JSON program, not a game name, class label, or prose explanation. Solver output should be a UTF-8 CSV at ./working/submission.csv with the preferred exact header id,patch_json, exactly one row for every test.csv id, no pandas/DataFrame index column, and no extra columns. If your synthesis method is uncertain for an id, still emit a grammar-valid fallback patch for that id rather than omitting the row. The grader is coverage-aware: it can ignore extra/index columns, recover reordered id and patch_json columns, drop foreign or bad ids, and score missing/unmatched test ids as row-level zero instead of failing the entire run. More precisely, each answer fills four holes in a supplied rule skeleton: the move generator M), move guard G), post-move effect E), and terminal rule T). The grader runs the submitted patch in the documented bounded interpreter and compares its behavior with the unknown reference rules. Many traditional strategy games survive through incomplete descriptions, variant rules, and partial records of play. This challenge models the work of reconstructing an executable ruleset from observations rather than from a title or prose description. Each episode supplies an anonymous board/equipment graph, a typed rule-program skeleton with four holes, one legal/illegal move-probe bundle, one partial play trace, and two naturally encountered terminal/winner observations. Site names, piece identities, directions, public ids, and harmless ordering choices are anonymized. The hidden target is a new compatible composition, not a renamed public game record. Public observations are exact interpreter outputs rather than corrupted labels. A partial trace may omit some final-state pieces, but every visible piece, accepted-action count, and terminal observation is consistent with the target program. Infer a JSON rule patch containing a move generator M), move guard G), post-move effect E), and terminal rule T). The patch is compiled and executed by a deterministic bounded interpreter. Submit the patch only; prose is invalid. Behaviorally equivalent patches receive full credit even when their JSON text or direction order differs. This is a CPU-only challenge. A complete solution has at most 90 minutes on 10 CPU cores and 62 GB RAM. GPU computation is neither required nor part of the intended solution. Task For every test episode, read the referenced JSON evidence, infer the semantics of its opaque board and direction symbols, synthesize all four interacting rule components, and write the patch in the exact grammar defined by DSL_SPEC.md. A submission is a program, not a game label, move label, table row, explanation, or scalar prediction. Generalization Contract Test episodes use held-out source-rule lineages and new compatible rule compositions. Exact train-patch retrieval is insufficient: the intended solution must transfer component behavior and validate interactions against each episode's observations. The hidden evaluator also executes counterfactual states and traces that are not present in the public evidence. Intended Approach A credible CPU solution should learn from the labeled public episodes and/or perform genuine episode-specific program induction from the supplied behavioral evidence. The final prediction must be a grammar-valid executable patch, not a metadata match, copied source record, fixed template, class label, scalar, or prose answer. All fitting, validation, calibration, and search must use only the released public data. Modeling Guidance Use the public DSL specification to understand the allowed JSON grammar and the meaning of public episode fields. The submitted object must use only the episode's opaque sites and directions, must contain exactly one patch for every test id, and must be serialized as ordinary JSON. Public traces may expose only part of a final state, so unsupported assumptions about omitted pieces are not labels. The supplied weak template is only a format example. Exact train-row retrieval, source lookup, independent per-hole majority voting, free-form code generation, and fitting one visible probe while ignoring traces or outcomes are not expected to transfer to the hidden counterfactual executions. Every submitted solution must run end to end without manual test labeling, read only the released public challenge data, write ./working/submission.csv, avoid network and private-path access, and complete within 90 minutes using at most 10 CPU cores and 62 GB RAM. Use fixed seeds where the selected learning or search procedure is stochastic. What Not To Use (any of these can cause solution rejection regardless of leaderboard score): Game-name, filename, culture, date, metadata-id, description, or rule-prose lookup. Web retrieval or nearest-neighbor recovery of public rule files. Source-dataset signatures, generator introspection, private-file access, or hidden-answer recovery. Public id, row order, file length, JSON length, episode filename, or site-name shortcuts. A finite hard-coded table of candidate answers copied from train rows. Regex-only parsing, metadata-only ranking, or fixed template inversion that neither learns from public training data nor performs episode-specific program induction. A classifier that predicts only a game, mechanic label, move class, scalar, or table row instead of emitting an executable patch. Submission-parser exploits, overlong payloads, nontermination attempts, dynamic code, filesystem access, or network access. The separately licensed full game player/application. Only the supplied bounded JSON grammar may be targeted. Enforcement on invalid approaches: solutions may be reviewed and rejected when they solve source retrieval or metadata exploitation rather than anonymous behavioral program synthesis. Evaluation The primary leaderboard metric is Coverage-Aware Semantic Rule Recovery Score (CA-SRRS), the mean executable-behavior recovery score blended with robustness across the disclosed move-rule, terminal-rule, and composition-depth group types. It is coverage-aware because the grader aligns submitted rows by valid test.csv ids: common CSV mistakes such as reordered columns, extra columns, a pandas index column, duplicate rows, foreign ids, or missing ids do not crash the run, but any unmatched test id receives row score 0.0. Every aligned row is parsed, type-checked, and compiled. An invalid, overlong, nonterminating, or ill-typed patch receives 0.0 for that row. The scorer accepts patch_json and common prediction-column aliases, ignores unrelated extra columns, drops foreign or non-integer ids, keeps the first duplicate id, and fills missing test ids with zero-credit empty patches. Unsafe unreadable local CSV files, invalid UTF-8, forbidden control bytes, or payloads above the documented limits remain rejected or zeroed before expensive parsing. For a valid patch, the grader uses the episode's public equipment map and a private collection of 18 legal-move probes, 10 terminal probes, and 10 action rollouts. It compiles the submitted patch once, executes it deterministically on each private state, and compares those outputs with outputs recorded from the reference patch. The private states are not released, but the execution algorithm, stopping rules, and comparison formulas are fully specified here and implemented in the supplied grade.py; there is no grading-time randomness and no source-text comparison. For a hidden legal-move probe, the interpreter enumerates the submitted program's complete legal action set for the supplied state. legal_set is the Jaccard similarity between that set and the complete reference set, with empty-versus-empty defined as 1.0; illegal_rej is the fraction of explicitly supplied illegal actions absent from the submitted set, or 1.0 when that list is empty. For a terminal probe, the interpreter evaluates T on the supplied state and compares both the Boolean terminal flag and, when the reference state is terminal, the winner; for a reference nonterminal state, the winner term equals the terminal-flag term. For a hidden rollout, actions are attempted in order from start. Execution stops before an action if the current state is terminal, or at the first action that the submitted program declares illegal; otherwise the move, guard, capture, effect, and turn change are applied. accepted compares how many actions were applied, exact_state requires exact equality of the complete final pieces map and turn, and the last two terms compare the post-rollout terminal flag and, only for a reference terminal result, its winner; for a reference nonterminal result, winner_after equals term_after. Operationally, two patches are behaviorally equivalent when these interpreter outputs agree on every scored probe and rollout, regardless of JSON key order or rule text; this is equivalence on the finite disclosed scoring procedure, not a claim of formal equality on every imaginable board state. legal_set = Jaccard(predicted complete legal set, hidden complete legal set) illegal_rej = fraction of explicit hidden illegal actions rejected legal_score = 0.85legal_set + 0.15illegal_rej terminal_flag = exact terminal/nonterminal agreement winner_score = exact winner agreement on terminal states terminal_score= 0.65terminal_flag + 0.35winner_score accepted = 1-min(1,abs(pred_count-ref_count)/max(1,num_actions)) exact_state = exact final pieces and side-to-move agreement term_after = exact post-rollout terminal agreement winner_after = exact post-rollout winner agreement rollout_score = 0.20accepted + 0.60exact_state 0.12term_after + 0.08winner_after behavior = (0.40legal_score + 0.20terminal_score 0.30*rollout_score) / 0.90 row_score = behavior^1.20 Syntax, type, bounds, and compilation are a gate rather than a source of points: an invalid row receives 0.0, while a valid row earns only behavioral credit. The three behavioral heads are normalized by their 0.90 weight sum and then raised to 1.20; this transparent strictness curve preserves 0.0 and 1.0 while still penalizing broadly partial or chance-level programs. Exact counterfactual state recovery receives the largest rollout share so that post-move effects cannot be ignored. The final score rewards both average behavior and robustness: Final = 0.75 * mean(row_score) 0.10 * lowest mean over hidden move-rule groups 0.08 * lowest mean over hidden terminal-rule groups 0.07 * lowest mean over hidden composition-depth groups Move-rule groups are the four reference M.kind values; terminal-rule groups are the four reference T.kind values; and composition depth is 2 + int(G.kind!="none") + int(E.kind!="none"), producing depths 2, 3, and 4. "Lowest mean" means the minimum arithmetic mean among all categories on that axis. Group labels remain private per row so they cannot become test features, but their definitions and weights are fixed. Higher is better. The theoretical minimum is 0.0; the theoretical maximum is 1.0. A semantically perfect patch set scores exactly 1.0. There is no artificial score cap. Dataset Prepared participant data is under public/. Episode paths are relative to that directory. DSL_SPEC.md defines the complete bounded grammar. File overview | Item | Description | |---|---| | train.csv | 1,800 labeled synthesis episodes | | test.csv | 600 unlabeled synthesis episodes | | train/episodes/*.json | Anonymous train evidence | | test/episodes/*.json | Anonymous test evidence | | DSL_SPEC.md | Exact executable JSON grammar | | sample_submission.csv | Valid low-information template | Table view: Public file table Item Description train.csv 1,800 labeled rows test.csv 600 unlabeled rows train/episodes/*.json Train evidence JSON test/episodes/*.json Test evidence JSON DSL_SPEC.md JSON grammar spec sample_submission.csv Format example train.csv is the labeled episode index. test.csv is the unlabeled episode index. sample_submission.csv demonstrates the exact output schema. DSL_SPEC.md defines the executable grammar. train/episodes/.json and test/episodes/.json contain the structured evidence referenced by their respective CSV rows. train.csv columns | Column | Type | Description | |---|---|---| | id | int | Opaque public integer id | | episode_id | string | Redundant opaque id alias | | episode_file | string | Relative JSON evidence path | | hole_count | int | Number of typed holes; always four | | evidence_counts_json | string | Counts of public probe types | | prompt | string | Synthesis instruction | | patch_json | string | Train-only executable target patch | Table view: train.csv table Column Type Description id int Opaque row id episode_id string ep_-prefixed id episode_file string Evidence JSON path hole_count int Always four evidence_counts_json string Public probe counts prompt string Shared instruction patch_json string Train target patch id is an opaque integer key. episode_id is the same key with an ep_ prefix and provides no independent signal. episode_file is a public-root-relative evidence path whose stem repeats id and adds no separate metadata. hole_count declares the four typed program holes. evidence_counts_json gives public probe counts. prompt is the shared source-neutral synthesis instruction. patch_json is the train-only executable label. Episode JSON schema Every episode file is one JSON object with exactly the following participant-relevant structures: episode_id is the redundant opaque ep_-prefixed row id. equipment defines the anonymous board. grammar_version is agrp-1; sites and directions are unique opaque strings; stepsite is the immediately adjacent site or null; raysite is the ordered list of farther sites along that direction; and zones contains home_1, home_2, goal_1, and goal_2 site arrays. skeleton declares the four typed holes. program maps move, guard, effect, and terminal to $M, $G, $E, and $T; holes lists each hole id and type; surface_order is presentation order only; and grammar_version is agrp-1. A state is {"turn":1|2,"pieces":{site:owner,...}}. turn is the player about to act. Each listed site contains one piece owned by player 1 or 2; an unlisted site is empty except in the explicitly partial observation described below. An action is {"to":site} for placement, or {"from":site,"to":site} for step, slide, and hop moves. Sites must come from that episode's equipment.sites. legal_move_probes is an array of {"state":...,"legal":[action,...],"illegal":[action,...]} objects. The public legal and illegal arrays are observed examples for that state, not promises that every possible action is listed. partial_play_traces is an array of {"start":...,"actions":[...],"accepted":n,"partial_final":...,"terminal_observed":bool} objects. Starting at start, the reference program attempts actions in order and stops at the first illegal action or when the current state is terminal. accepted is the number applied. partial_final.turn is the true final side to move, but partial_final.pieces reveals only a subset of occupied sites: an omitted site is unknown here, not evidence that it is empty. terminal_observed is the reference terminal flag after the accepted prefix. terminal_winner_probes is an array of {"state":...,"terminal":bool,"winner":0|1|2} objects. winner is 0 exactly when the state is nonterminal; otherwise it is the winning player. Patch grammar and execution semantics patch_json must be a strict JSON object with exactly the keys M, G, E, and T. Every direction list contains unique values from the current episode's equipment.directions. Unknown keys, duplicate JSON keys, nonstandard numbers, unknown sites or directions, and values outside these alternatives are invalid. M is {"kind":...,"dirs":[...],"max_steps":n,"capture":...}. kind is place, step, slide, or hop; capture is forbid, replace, or only; and max_steps is 1..5. place requires dirs=[] and creates {"to":...} actions on empty sites. step moves one adjacency. slide follows each ray through at most max_steps sites and stops after the first occupied site. hop jumps over one adjacent enemy to the empty site immediately beyond it. place, step, and hop require max_steps=1. For non-hop movement, capture="forbid" permits only empty destinations, capture="only" permits only enemy-occupied destinations, and capture="replace" permits empty or enemy-occupied destinations; a friendly destination is always illegal. A hop always requires an adjacent enemy and an empty landing site. G is {"kind":"none"}, {"kind":"origin_zone","zone":"home"|"goal"}, {"kind":"dest_zone","zone":"home"|"goal"}, or {"kind":"adjacent","who":"self"|"enemy","dirs":[...],"min":1..4}. Zones are selected relative to the acting player. The adjacency guard counts matching pieces one step from the destination in the listed directions. E is {"kind":"none"} or {"kind":"remove_adjacent"|"convert_adjacent","dirs":[...],"limit":1..4,"select":"first"|"all"}. After the mover reaches the destination, opposing adjacent pieces are visited in dirs order, limited to limit, and either removed or changed to the mover's owner. first affects only the first eligible site; all affects every eligible site up to the limit. T is {"kind":"connect","k":2..5,"dirs":[...]}, {"kind":"reach","count":1..5}, {"kind":"material","threshold":0..4}, or {"kind":"no_moves","winner":"self"|"opponent"}. connect wins when a player owns a same-direction run of at least k; reach wins when a player occupies at least count sites in that player's goal zone; material awards the opponent a win when a player's piece count is at most threshold; and no_moves triggers when the side to act has no legal action, with winner interpreted relative to that side. A turn enumerates moves from M, filters them through G, applies the move and capture, applies E, switches turn, and then evaluates T. If both players satisfy a terminal condition, the previous mover wins when eligible; otherwise the lower eligible player id is used. All loops are bounded by the finite equipment maps, max_steps<=5, direction limits, and the 24-action trace limit. These rules are also packaged in DSL_SPEC.md for convenient machine access; the definitions above are the participant-facing summary of the same interpreter contract. test.csv columns | Column | Type | Description | |---|---|---| | id | int | Opaque public integer id | | episode_id | string | Redundant opaque id alias | | episode_file | string | Relative JSON evidence path | | hole_count | int | Number of typed holes; always four | | evidence_counts_json | string | Counts of public probe types | | prompt | string | Synthesis instruction | Table view: test.csv table Column Type Description id int Opaque row id episode_id string ep_-prefixed id episode_file string Evidence JSON path hole_count int Always four evidence_counts_json string Public probe counts prompt string Shared instruction id is the opaque public integer id. episode_id is its redundant ep_-prefixed alias. episode_file is the path to the evidence JSON relative to public/ and repeats the same id in its stem. hole_count is four. evidence_counts_json records public evidence counts. prompt contains the synthesis instruction. Submission Write ./working/submission.csv with one row per test id and the preferred two columns in this order. | Column | Type | Constraint | |---|---|---| | id | int | Test id | | patch_json | string | Bounded four-key JSON patch | Table view: submission.csv table Column Type Constraint id int Test id patch_json string Four-key JSON patch Requirements Save a UTF-8 CSV at exactly ./working/submission.csv. Prefer exactly the columns id,patch_json in that order, with no leading/trailing header whitespace and no extra columns. Do not write a pandas/DataFrame index column. A safe final write pattern is df = df[["id", "patch_json"]] followed by df.to_csv("./working/submission.csv", index=False). Include every test.csv id exactly once for best score. If a submission has missing rows, duplicate rows, foreign ids, fractional ids, non-finite ids, or extra ids, the grader aligns by valid test ids, keeps the first duplicate, drops nonmatching rows, and assigns 0.0 to unmatched test ids. Encode patch_json as one strict JSON object with exactly the four keys M, G, E, T; duplicate keys, non-standard numeric constants, unknown fields, invalid opaque symbols, and values outside DSL_SPEC.md are invalid for that row. Keep each patch within the documented bounded grammar and 12,000-character row limit, and keep the aggregate UTF-8 patch payload at or below 16,000,000 bytes. An ordinary invalid patch row scores zero; recoverable participant-level submission structure mistakes are aligned and scored with missing rows as zero; an oversized aggregate patch payload scores 0.0; unsafe unreadable/control-byte local CSV files are rejected before grading. Use a standard JSON serializer and let the CSV library escape embedded quotes. Do not hand-build CSV quoting. Example format: id,patch_json 10000000,"{""M"":{""capture"":""forbid"",""dirs"":[""q2fbd8"",""q1573c""],""kind"":""step"",""max_steps"":1},""G"":{""kind"":""none""},""E"":{""kind"":""none""},""T"":{""kind"":""material"",""threshold"":0}}" 10000008,"{""M"":{""capture"":""forbid"",""dirs"":[""qa4039"",""q4f6e1""],""kind"":""step"",""max_steps"":1},""G"":{""kind"":""none""},""E"":{""kind"":""none""},""T"":{""kind"":""material"",""threshold"":0}}" &nbsp;
> Just now
> $400–$500
> Draft

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Coupled Pendulum Hidden Coupling-Graph Inference

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76v0mqtjrmhzyg1ct7wtreds88x2b9
- DOMAIN exactly as displayed: Other
- Challenge collection: CPU
- Status: Draft
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Coupled Pendulum Hidden Coupling-Graph Inference Overview Infer which pendulums influence one another from their motion in a short video, identify the strongest coupling, and predict each pendulum's phase well after the recording. The data are fully synthetic: a linear small-angle coupled-oscillator model is rendered as a head-on view of eight to ten pendulums on a shared rail. This is an idealized system-identification task, not footage of physical experiments. Every bob has the same size and colour and displays an integer ID from 0 to n_pendulums-1. Hidden links are never drawn. IDs and horizontal positions do not indicate the coupling graph. Use the motion over time to distinguish direct coupling from coincidental or indirect correlation. The coupling graph is undirected; its coefficients describe symmetric interactions. Return the coupled pairs, the pair with the largest coupling coefficient, a phase for every printed ID at query_time_s, and a confidence estimate of your weighted prediction accuracy. Strongest coupling means largest model coefficient; it is not necessarily the pair with the largest observed amplitude change. Some links are harder to estimate from short observations, but no unmeasured irreducible performance ceiling is claimed. Phase is atan2(angular_velocity / natural_angular_frequency, angle), converted to degrees modulo 360. Angle is zero when vertical and positive toward the right side of the displayed image; angular velocity uses the same sign. Natural angular frequency is the pendulum's uncoupled frequency, which must be inferred. Forecast the displayed motion, including the sign shown in mirrored views, and always answer using printed IDs. You may train visual and relational models or fit motion and coupled dynamics statistically. Estimate model choices from the labelled training data. Stream videos and retain compact trajectories rather than loading the corpus into memory. Compute and runtime Target CPU runtime: up to 10 cores and 62.5 GiB RAM, approximately one hour for the complete solution. No GPU or runtime internet is required or permitted by this challenge. Use standard Kaggle Python Docker libraries. Read only ./dataset/public/ and write generated files under ./working/, ending with ./working/submission.csv. A practical CPU route is video tracking followed by a fitted dynamics model or a lightweight learned graph model. What Not To Use Do not use hosted model APIs, runtime downloads, external copies of these clips, or external answer lookups. Do not access private files, raw simulator metadata, generation seeds, or organizer scripts. Do not exploit filenames, row order, filesystem metadata, grading internals, or hard-coded answer dictionaries. Do not replace the required outputs with captions or a different prediction task. A single frame, fixed graph, or ID-adjacency rule is only a weak diagnostic, not evidence of recovered dynamics. Relation to prior work Neural Relational Inference (Kipf et al., 2018) studies latent interaction graphs from trajectories; Visual Causal Discovery Network (Li et al., 2020) also studies visual interaction discovery and dynamics prediction. This challenge uses printed-ID pendulum videos, short observation windows, and long-horizon phase forecasts. It shares the broader inference objective with that literature. Evaluation Higher is better. Scores range from 0.0 to 1.0. Each clip has three accuracy components: E = 2 * |predicted_edges intersect true_edges| / (|predicted_edges| + |true_edges|) S = 1 for the exact strongest pair, otherwise 0 P = mean_i exp(-circular_distance(predicted_phase_i, true_phase_i) / 30) C = 0.50E + 0.22S + 0.28*P A = 1 - abs(confidence - C) row_score = C * (0.90 + 0.10*A) final_score = mean(row_score over all test clips) The weighting expresses the task priorities: half the credit rewards recovery of the full interaction graph, 22% rewards identifying its single strongest link, and 28% tests whether the inferred dynamics support future phase prediction. This gives graph structure the majority (72%) while retaining a substantial forecasting test; the weights are task-design choices, not physical constants or estimates fitted to baseline scores. Strongest-pair accuracy measures a specific interaction that aggregate edge F1 can miss. The 30-degree phase scale gives credit of exp(-1) at a one-twelfth-cycle error and smooth partial credit as errors decrease. Confidence is a self-estimate of C: absolute error gives a bounded, interpretable penalty, and its 10% modulation keeps prediction quality dominant. This is an accuracy-estimation term, not a claim of probabilistic calibration or a proper scoring rule. For a fixed C, matching confidence to C maximizes row credit. Two valid empty edge sets have E=1. If only one is empty, E=0. A true empty strongest-pair label matches only a well-formed []. A malformed strongest pair has S=0, including for no-edge rows. Phase distance is the shorter distance around the circle, from 0 to 180 degrees. Finite phase numbers are wrapped modulo 360. A missing or invalid phase value contributes zero for that pendulum; an unparseable phase object, duplicate JSON key, or impossible ID makes the phase head zero. Confidence estimates C, not the probability that every target is exactly correct. It adjusts earned accuracy and never supplies credit for wholly wrong predictions. No hidden subgroup weight, score cap, or score power is applied. The exact five submission columns and their order are required. Missing, extra, reordered or duplicate columns; duplicate, missing, extra or fractional row IDs; and nonnumeric, nonfinite, boolean or out-of-range confidence make the submission score 0.0. Legitimate numeric-string row IDs are accepted. Malformed row-local predictions affect their corresponding accuracy head without discarding valid predictions in other rows or heads. JSON cells are limited to 20,000 characters and four nesting levels before decoding. Pair endpoints must be JSON integers in 0..n_pendulums-1, distinct and valid. Reversed pair order is accepted; duplicate edges, self-loops, fractional/boolean/quoted endpoints, impossible IDs and invalid pair shapes make that graph head zero. Phases must be JSON numbers, not booleans or quoted strings. Nonstandard NaN/Infinity JSON tokens and duplicate object keys are invalid. Dataset There are 1311 labelled training clips and 639 test clips. Every video is a 1280 x 360 H.264 MP4 containing 24 RGB frames at 12 fps. The playback duration is 2 seconds; frame timestamps run from 0 through 23/12 seconds. query_time_s is approximately 12.2 to 14.2 seconds from the first frame, approximately 10.2 to 12.2 seconds after the clip. Video paths resolve relative to the public/ root, where the CSVs are stored. File overview | Item | Description | |---|---| | train.csv | Inputs and three labels | | test.csv | Inputs only | | sample_submission.csv | Weak dense template | | train/videos/ | Training MP4s | | test/videos/ | Test MP4s | train.csv columns | Column | Type | Description | |---|---|---| | id | integer | Opaque clip identifier | | video | string | Public-relative path | | n_pendulums | integer | Eight to ten bobs | | fps | integer | Frames per second | | query_time_s | float | Requested future instant | | prompt | string | Task reminder | | coupling_edges_json | JSON string | Coupled ID pairs | | strongest_pair | JSON string | Largest coupling pair | | phases_query_json | JSON string | ID-to-phase mapping | The last three columns are training labels. coupling_edges_json is a list such as [[0,2],[1,3]]. strongest_pair is one pair such as [0,2], or [] if there is no coupling. phases_query_json contains exactly one string key per pendulum ID, such as "0", with a numeric phase in [0,360). test.csv columns | Column | Type | Description | |---|---|---| | id | integer | Opaque clip identifier | | video | string | Public-relative path | | n_pendulums | integer | Eight to ten bobs | | fps | integer | Frames per second | | query_time_s | float | Requested future instant | | prompt | string | Task reminder | n_pendulums is an observed input count, not an evaluation target; only the graph, strongest pair and future phases are hidden. Test rows contain the same six input columns as training rows, without the three labels. The printed bob IDs are separate from the CSV clip id. The sample is a format-valid weak template whose guesses must be replaced. Submission Submit a header and exactly 639 rows, one for every test id, with these five columns in this order: | Column | Type | Constraint | |---|---|---| | id | integer | Exact test ID set | | coupling_edges_json | JSON list | Unique valid pairs | | strongest_pair | JSON list | One pair or [] | | phases_query_json | JSON object | One phase per bob ID | | confidence | number | Finite value in [0,1] | Example rows from the weak sample (these are guesses, not answers): id,coupling_edges_json,strongest_pair,phases_query_json,confidence 0,"[[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8], [3, 9], [4, 5], [4, 6], [4, 7], [4, 8], [4, 9], [5, 6], [5, 7], [5, 8], [5, 9], [6, 7], [6, 8], [6, 9], [7, 8], [7, 9], [8, 9]]","[0, 1]","{""0"": 180.0, ""1"": 180.0, ""2"": 180.0, ""3"": 180.0, ""4"": 180.0, ""5"": 180.0, ""6"": 180.0, ""7"": 180.0, ""8"": 180.0, ""9"": 180.0}",0.3 3,"[[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8], [4, 5], [4, 6], [4, 7], [4, 8], [5, 6], [5, 7], [5, 8], [6, 7], [6, 8], [7, 8]]","[0, 1]","{""0"": 180.0, ""1"": 180.0, ""2"": 180.0, ""3"": 180.0, ""4"": 180.0, ""5"": 180.0, ""6"": 180.0, ""7"": 180.0, ""8"": 180.0}",0.3 4,"[[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [3, 4], [3, 5], [3, 6], [3, 7], [4, 5], [4, 6], [4, 7], [5, 6], [5, 7], [6, 7]]","[0, 1]","{""0"": 180.0, ""1"": 180.0, ""2"": 180.0, ""3"": 180.0, ""4"": 180.0, ""5"": 180.0, ""6"": 180.0, ""7"": 180.0}",0.3 &nbsp;
> 3h ago
> $400–$500
> Draft

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.


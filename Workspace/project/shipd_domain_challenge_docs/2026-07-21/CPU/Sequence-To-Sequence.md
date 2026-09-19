# CPU Sequence To Sequence Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed CPU examples in this document: 91

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.

## Broken Cuneiform Witness Alignment

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f3gv2r6c14e85654fyqvy398ar3x6
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat adarsh2626's score of 0.546!

Full challenge description from page:

> Five cuneiform source lines and six English witness lines are presented in each case. Predict which source and witness lines express the same content. Some source lines have no surviving witness, and the remaining English lines are unrelated intruders.
> The result is a structured alignment audit with four connected outputs: a binary link matrix, a canonical link program, the unmatched source IDs, and the unused witness IDs. Solving the task requires cross-script semantic alignment and global one-to-one assignment. A locally plausible translation is not enough when it conflicts with a stronger packet-wide matching.
> This models a real archival problem. Fragment catalogues and translated witness tables are often assembled separately, and missing or misplaced rows must be identified before a bilingual edition can be trusted.
> Dataset
> The public data contains 4,200 labeled training cases and 386 unlabeled test cases. Source partitions remain separated during preparation. IDs are opaque and row order carries no source chronology. Deterministic lacuna masks hide 35 percent of cuneiform signs and 42 percent of normalized English tokens, while retaining at least one English token and two cuneiform signs. This removes exact source phrases and models damaged archival witnesses.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Public inputs and all four target columns for training cases. |
> | `test.csv` | Public inputs only for test cases. |
> | `sample_submission.csv` | Submission template with the required columns and example formatting. |
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque unique case identifier. |
> | `cuneiform_packet` | JSON array string | Five objects with IDs `w1` through `w5` and a partially lacunose Unicode cuneiform `line`. |
> | `english_witness_packet` | JSON array string | Six objects with IDs `e1` through `e6` and a normalized, partially lacunose English `line`. |
> | `alignment_contract` | string | The one-to-one alignment rule applied to the packet. |
> Target Columns
> | Column | Data type | Description |
> |---|---|---|
> | `alignment_matrix` | JSON integer matrix | A 5 by 6 binary matrix. Entry `[i][j]` is 1 only when source `w{i+1}` aligns to witness `e{j+1}`. Every row and column contains at most one 1. |
> | `alignment_program` | ordered token string | Link tokens in ascending source-ID order, followed by `seal:witness`. Example: `link:w1:e4>link:w3:e2>seal:witness`. |
> | `unmatched_source_set` | canonical set string | Unmatched source IDs joined by `|`, or `none`. |
> | `orphan_witness_set` | canonical set string | Unused witness IDs joined by `|`. At least one witness is unused in every case. |
> The number of unmatched source lines is balanced across zero, one, and two cases. Training counts are 1,411, 1,419, and 1,370. Test counts are 124, 135, and 127.
> Submission Format
> Write the final file to:
> ./working/submission.csv
> The CSV must contain exactly these columns in this order:
> case_id,alignment_matrix,alignment_program,unmatched_source_set,orphan_witness_set
> Example row:
> case_id,alignment_matrix,alignment_program,unmatched_source_set,orphan_witness_set
> 4a9b2607c32a4e61f0a09ca2,"[[0,0,0,1,0,0],[0,0,0,0,0,0],[0,1,0,0,0,0],[0,0,0,0,1,0],[1,0,0,0,0,0]]",link:w1:e4>link:w3:e2>link:w4:e5>link:w5:e1>seal:witness,w2,e3|e6
> Extra columns, reordered columns, duplicate IDs, missing IDs, and extra rows are rejected. The backend may append one visibility column; the grader ignores only that named column.
> Evaluation
> The metric is Packet Alignment Integrity Score:
> Score = 0.45 * MatrixScore
> + 0.30 * ProgramScore
> + 0.13 * UnmatchedScore
> + 0.12 * OrphanScore
> For one case, let entry_accuracy be the fraction of the 30 matrix entries that match and let matrix_exact be 1 only when the complete matrices are identical.
> MatrixScore = 0.18 * entry_accuracy + 0.82 * matrix_exact
> For the ordered program, Levenshtein distance is computed over >-separated tokens. If T is the true token list and P is the predicted list:
> edit_similarity = 1 - edit_distance(T, P) / max(len(T), len(P), 1)
> ProgramScore = 0.15 * edit_similarity + 0.85 * exact_program_match
> For each set field, standard set F1 is 2 * intersection_size / (true_size + predicted_size). It is 1 when both sets are empty.
> UnmatchedScore = 0.25 * set_F1 + 0.75 * exact_set_match
> OrphanScore    = 0.25 * set_F1 + 0.75 * exact_set_match
> The four predictions must describe the same alignment. If matrix links, program links, unmatched rows, and orphan columns disagree, that case receives a 10 percent coherence penalty. Malformed matrices, programs, or sets receive zero for the affected component. Parsing is length-bounded.
> Minimum score: 0.0
> Maximum score: 1.0
> Direction: higher is better.
> What Makes This Interesting
> The input is neither ordinary translation nor independent sentence retrieval. A solver must resolve a constrained partial permutation across two scripts while recognizing that several lines intentionally have no counterpart. The matrix and executable link grammar expose different failure modes, and the coherence rule rewards a genuinely unified alignment.
> Method Requirements
> CPU-compatible multilingual encoders, character models, compact sequence-to-sequence models, and matching algorithms learned or calibrated from the supplied training data are allowed.
> What Not To Use
> Do not identify source records through external phrase search, public corpus mirrors, original row numbers, or source-specific lookup tables.
> Do not map case_id, row position, hashes, or formatting artifacts directly to targets.
> Do not retrieve hidden translations or alignments from outside the supplied public files.
> Do not exploit submission parsing, duplicate rows, omitted rows, extra columns, or non-finite values.
> Do not adapt model parameters using hidden test labels or grader feedback.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## ReplyAudit: Contaminated Answer Assembly

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ak06bpx8dbfgkyncs2hwh6x8awwjp
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat monu's score of 64.152!

Full challenge description from page:

> ReplyAudit: Contaminated Answer Assembly
> Overview
> This challenge models a corrupted export from a specialist question-and-answer archive. During export, each answer was divided into labeled segments, the segment order was lost, and one topically plausible segment from a different answer was inserted. For every test row, identify the inserted segment and reassemble all genuine segments in the order recorded in the original answer.
> The text is anonymized to prevent source lookup. Tokens such as g13032 are fixed codes for normalized words or punctuation: the same code represents the same token everywhere in train.csv and test.csv. The special token r00 means that an input token was withheld. query_stream is the anonymized question that the answer addressed. candidate_stream contains the shuffled answer segments plus one contaminating segment from another reply record. The segment labels b0, b1, and so on are local to one row and only identify the presented candidates.
> Question tokens are independently withheld at a rate of 12%, and candidate-segment tokens at a rate of 18%. Redaction changes only the visible input; it never changes the correct contaminant or the recorded answer order. Candidate presentation order is randomized, and contaminant position is balanced for each candidate count. layout_code is an additional balanced nuisance field and contains no answer information.
> Submit one variable-length string per row. For example, DROP b3 | ORDER b2 b0 b1 means that b3 came from another reply and that the genuine answer reads as segment b2, followed by b0, followed by b1. This is a sequence-to-sequence archive-repair task, not single-label classification.
> A practical first approach is to compare each segment with the question and with the other candidates to locate the contaminant, then learn which token patterns tend to occur near the beginning, middle, end, or transition points of genuine answers.
> Evaluation Metric
> The score combines contaminant identification, global ordering, and exact neighboring-segment recovery.
> For row i:
> B_i is the set of candidate labels in candidate_stream.
> d_i is the true contaminating label.
> T_i = (t_i1, ..., t_im) is the genuine segments in their recorded answer order.
> A prediction must use the form DROP bX | ORDER bA bB ....
> A prediction row is valid only if DROP names exactly one label from B_i, ORDER contains every other candidate exactly once, no label is repeated, and no unknown label appears. An invalid row receives a_i = 0, tau_i = −1, and f_i = 0.
> Contaminant term
> a_i = 1 when the submitted DROP equals d_i; otherwise a_i = 0.
> D = (1 / N) × sum_i a_i.
> Global-order term
> Ordering is scored independently enough to give useful partial credit when DROP is wrong. For a valid prediction:
> Start with the submitted ORDER list.
> Append the submitted DROP label to its end.
> Remove the true contaminating label d_i.
> This produces P_i, a complete predicted order of the genuine segments.
> For example, suppose the truth is:
> DROP b3 | ORDER b2 b0 b1
> and the prediction is:
> DROP b1 | ORDER b2 b0 b3
> The submitted full list becomes b2 b0 b3 b1. Removing the true contaminant b3 gives P_i = b2 b0 b1. The contaminant term is wrong, but the genuine segments are in the correct relative order, so the ordering terms can still receive credit.
> Let C_i be the number of genuine segment pairs with the same relative order in P_i and T_i.
> Let R_i be the number of genuine segment pairs with opposite relative order.
> tau_i = (C_i − R_i) / (C_i + R_i).
> K = max(0, (1 / N) × sum_i tau_i).
> The maximum with zero is applied after averaging all rows, not separately to each row. Therefore, a random ordering has approximately zero aggregate concordance skill rather than receiving automatic half credit.
> Neighbor-link term
> Let E_i be the directed adjacent segment pairs in T_i.
> Let P_i^E be the directed adjacent segment pairs in P_i.
> precision_i = |E_i ∩ P_i^E| / |P_i^E|.
> recall_i = |E_i ∩ P_i^E| / |E_i|.
> f_i = 2 × precision_i × recall_i / (precision_i + recall_i).
> If the final denominator is zero, f_i = 0.
> A = (1 / N) × sum_i f_i.
> Final score
> Score = 100 × clip(0.40 × D + 0.35 × K + 0.25 × A, 0, 1).
> The theoretical minimum is 0 and the maximum is 100. A score of 100 requires the correct contaminant and the exact complete answer order for every row. Empty, malformed, duplicated-label, incomplete, and unknown-label strings receive the defined worst-case terms and provide no abstention advantage. The grader rounds the final score to six decimal places.
> Measured public-only references on the shipped data and grader are:
> Perfect answers: 100.000000.
> Valid presentation-order sample: 11.876831.
> Fixed-drop token-position profile: 15.044376.
> Competent candidate GBM plus token-position profile: 38.880492.
> Candidate GBM plus hashed pairwise decoder: 48.789690.
> Candidate GBM plus hashed position-aware decoder: 52.139426.
> Every learned reference fits only train.csv. Private targets are used solely to calculate the reported scores.
> Dataset
> train.csv
> Contains 1,764 labeled archive-repair examples.
> sample_id - integer - Fresh public identifier containing no source information.
> query_stream - string - An anonymized question represented by 20 to 120 space-separated g##### or r00 tokens.
> candidate_stream - string - Four to eight locally labeled answer segments. Each segment is written as bK [ token token ... ], contains 9 to 78 tokens, and is separated from the next segment by ||. Exactly one segment comes from a different reply record.
> layout_code - string - Balanced nuisance value, either z0 or z1; it is unrelated to the target.
> target_string - string - The correct contaminant and genuine answer order, formatted as DROP bX | ORDER bA bB ....
> An illustrative candidate_stream with shortened contents is:
> b0 [ g10201 g04410 r00 ] || b1 [ g09122 g18301 ] || b2 [ g04410 g27548 ]
> If b1 is the contaminant and the recorded answer order is b2 then b0, the target is:
> DROP b1 | ORDER b2 b0
> Actual rows contain at least four candidate segments.
> test.csv
> Contains 569 unlabeled examples with exactly these columns:
> sample_id - integer - Fresh public identifier.
> query_stream - string - Anonymized question in the training representation.
> candidate_stream - string - Shuffled genuine answer segments plus one contaminating segment.
> layout_code - string - Balanced nuisance value.
> sample_submission.csv
> Contains 569 valid-format presentation-order predictions with these columns:
> sample_id - integer - Test identifier.
> target_string - string - Example DROP ... | ORDER ... prediction.
> The split is performed by original question before answer examples or contaminating segments are constructed. It contains 1,438 train question groups and 450 test question groups, with zero group overlap and zero cross-split input-signature overlap. Public inputs contain no URLs, authors, votes, dates, original question or answer IDs, literal words, or recorded segment positions.
> Submission
> Upload a CSV with a header, exactly 569 rows, and exactly these columns in this order:
> sample_id - integer - Must match every test identifier exactly once.
> target_string - string - DROP bX | ORDER bA bB ..., naming one contaminating segment and every remaining candidate exactly once.
> Extra or reordered columns, duplicate IDs, missing IDs, unknown IDs, and an incorrect row count are rejected. CSV row order does not matter. Invalid target strings receive the worst-case row terms instead of crashing the grader.
> Concrete valid-format examples using real test IDs are:
> sample_id,target_string
> 4,DROP b0 | ORDER b1 b2 b3 b4 b5 b6 b7
> 7,DROP b0 | ORDER b1 b2 b3 b4
> 8,DROP b0 | ORDER b1 b2 b3 b4 b5 b6
> These rows demonstrate syntax only and are not disclosed answers.
> What Not to Use
> Presented candidate order fails because segments are shuffled and contaminant position is balanced separately for every candidate count.
> layout_code is balanced within each split and deliberately unrelated to the target.
> A per-token lookup table fails because common anonymized words occur in different answer positions and contexts.
> Question overlap alone is insufficient because the contaminating segment is selected to be topically plausible.
> Independent segment scoring cannot enforce one consistent answer order or recover directed neighboring pairs.
> External source lookup is blocked because public files omit literal words, URLs, source IDs, vote scores, timestamps, authors, and original positions.
> Strong solutions should combine question-conditioned contaminant detection with a global segment-order decoder. Sparse token features, gradient boosting, compact embeddings, pairwise relation models, and small CPU sequence encoders are all practical within the execution environment.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Multilingual Two-Stage Morphological Route Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77e6maygyn93h873596h2djn8aswk9
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat mastermind's score of 0.485!

Full challenge description from page:

> Multilingual Two-Stage Morphological Route Reconstruction
> Overview
> This is a sequence-to-sequence route-reconstruction challenge. Each row contains one serialized context with three complete demonstration routes and one incomplete query route. A route has three ordered word forms: an initial state, a first transformed state, and a second transformed state.
> Exactly two demonstrations follow the same hidden ordered pair of transformations as the query. The third is a contrastive decoy constructed from a different hidden route and, when the data permits, shares one latent state with the true route. Demonstrations are shuffled independently in every row, so their positions do not reveal which pair is relevant.
> Your model must jointly identify the coherent demonstrations, infer both transformations in their correct order, and generate the query's two missing stages. This is not ordinary single-step inflection or A:B::C:D completion: the required output is an ordered two-form trajectory under a row-specific latent route, in the presence of a plausible distractor.
> Task
> Every context follows this grammar:
> D1⟦start ⟶ stage_1 ⟶ stage_2⟧ ⟐ D2⟦start ⟶ stage_1 ⟶ stage_2⟧ ⟐ D3⟦start ⟶ stage_1 ⟶ stage_2⟧ ⟐ Q⟦query_start ⟶ ? ⟶ ?⟧
> The labels D1, D2, and D3 only identify display positions. Two routes demonstrate the query's hidden ordered transformation pair; one route is a decoy. Generate the two query forms as one output sequence:
> query_stage_1 ⟶ query_stage_2
> The order matters. Predicting only the final form, reversing the stages, selecting a demonstration route verbatim, or omitting the separator is incorrect.
> All forms are NFC-normalized Unicode strings. They may contain diacritics, non-Latin scripts, hyphens, apostrophes, or single internal ASCII spaces.
> Dataset
> train.csv contains 8,000 labelled route-reconstruction rows with these columns:
> id: string in train_###### format. It is assigned after deterministic shuffling and carries no predictive information.
> system: categorical string in anonymous system_?? format. It identifies one of five transformation systems.
> context: Unicode string of at most 900 code points following the four-route grammar above.
> target: Unicode string containing exactly two correct forms separated by ⟶ .
> test.csv contains 1,600 unlabelled rows with these columns:
> id: string in test_###### format. It is used only to align submissions and carries no predictive information.
> system: categorical string in anonymous system_?? format. It has the same meaning as in training.
> context: Unicode string following the same four-route grammar as training. Its query contains two ? slots.
> sample_submission.csv contains 1,600 rows and demonstrates the required id,prediction schema. For each anonymous system, its two scaffold stages are the most frequent stage strings fitted from training targets only; hidden test targets are never used.
> metadata.json records participant-safe row counts, column order, opaque system values, separators, sequence limits, metric, deterministic seed, and split notes. It contains no targets or source identifiers.
> Complete related-lexeme clusters are assigned to train or test before route construction. Exact normalized surface collisions and conservative one-character variants remain in one partition. Query lexemes and demonstration lexemes also have disjoint roles inside each partition. No test target surface occurs in any test input context. Train and test are shuffled independently before sequential IDs are assigned.
> Evaluation
> A prediction must parse into exactly two valid forms, p1 and p2, separated by the exact string ⟶ . Let the hidden stages be t1 and t2. Character similarity is normalized Levenshtein similarity:
> similarity(p, t) = 1 - levenshtein(p, t) / max(len(p), len(t))
> row_score = 0.40 * exact_match(p1 ⟶ p2, t1 ⟶ t2)
> + 0.30 * similarity(p1, t1)
> + 0.30 * similarity(p2, t2)
> The final score is the arithmetic mean of all row scores. Higher is better. A perfect submission scores 1.0.
> Submission
> Submit a UTF-8 CSV file with exactly these columns, in this order:
> id,prediction
> Here is a correctly formatted submission example. The prediction values are illustrative:
> id,prediction
> test_000001,form_one ⟶ form_two
> test_000002,first_stage ⟶ second_stage
> test_000003,alpha ⟶ beta
> Every test id must appear exactly once. Row order does not matter.
> prediction must contain exactly two NFC-normalized forms separated by one ⟶ string. Each form must contain 1–64 Unicode code points. The complete prediction may contain at most 131 code points. Leading or trailing whitespace, tabs, line breaks, control characters, non-ASCII whitespace, consecutive spaces inside a form, additional route separators, missing stages, or the reserved context characters ⟐, ⟦, and ⟧ inside a form are invalid.
> An invalid prediction receives zero for that row. A structurally invalid CSV, wrong column order, extra column, malformed data row, missing ID, duplicate ID, or extra ID receives an overall score of zero.
> Requirements
> Use only the supplied challenge files and preinstalled runtime libraries.
> CPU-only solutions must complete within the platform's 1.5-hour limit.
> Do not download packages or data during solution execution.
> Do not use external datasets, linguistic databases, source-corpus copies, reverse lookup, private answers, hidden files, filenames, IDs, or row order to recover targets.
> Do not treat D1, D2, or D3 as a fixed answer indicator; their order is independently shuffled.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Masked Glycan Branch Unit Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7exy8fc9p610w1bvgmfp82qh8ar9kc
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Beat mastermind's score of 0.517!

Full challenge description from page:

> Recover a missing branch unit from a glycan structure.
> Glycans are branched carbohydrate molecules found on proteins, lipids, and cell
> surfaces. Their behavior depends on both the residue building blocks and the
> chemical positions used to connect those residues. In this challenge, each row
> shows the visible part of one glycan as residue descriptors plus donor/acceptor
> linkage records. One connected branch has been removed.
> Your task is to reconstruct the missing branch as structured JSON. A correct
> answer must recover the branch attachment position, the hidden residue
> descriptors, and the internal linkage pattern of the missing branch. The hidden
> branch contains 3 to 6 residues. The branch labels in the answer are local labels
> r1, r2, ... in traversal order from the attachment point.
> This is a CPU-only structured sequence/graph reconstruction task. GPU usage is
> not allowed.
> Dataset
> Files:
> public/train.csv: 2,260 solved examples. It contains all public input
> columns plus recovered_branch_json.
> public/test.csv: 996 held-out examples. It contains the same public input
> columns without recovered_branch_json.
> public/sample_submission.csv: 996 schema-only placeholder rows.
> Columns:
> id (string): released row id.
> prompt (string): task instruction.
> masked_sequence (string): compact text summary of the visible glycan graph.
> It reports the total residue count, visible residue letters, visible linkage
> tokens, attachment parent residue, and hidden branch size.
> visible_residue_context_json (JSON list of objects): visible residue table.
> Each object has residue_label (string), residue_index (integer),
> unique_residue_index (integer), and residue_descriptor (string).
> visible_linkages_json (JSON list of objects): visible donor/acceptor linkage
> records. Each object has lin_index (integer), linkage_token (string),
> donor_residue (string), donor_position (string), acceptor_residue
> (string), and acceptor_position (string).
> branch_gap_json (JSON object): public information about the removed branch.
> It contains attachment_parent_residue (string),
> attachment_parent_descriptor (string), hidden_residue_count (integer),
> hidden_linkage_count (integer), branch_ids (list of strings), and
> visible_sibling_context (list of sibling linkage/residue records at the same
> attachment parent).
> answer_format_json (JSON object): row-specific output schema showing the
> required branch ids for that row.
> recovered_branch_json (JSON object, train only): ground-truth missing branch.
> recovered_branch_json must contain:
> attachment (object): parent_residue, donor_position, and
> acceptor_position.
> branch_residues (list of objects): one object per hidden residue, each with
> branch_id and residue_descriptor.
> branch_linkages (list of objects): each hidden linkage with donor,
> donor_position, acceptor, and acceptor_position. donor is either
> parent or a branch id such as r2; acceptor is a branch id.
> Submission Format
> Submit a UTF-8 CSV with exactly these columns:
> id,recovered_branch_json
> glybranch_test_0000,"{""attachment"":{""parent_residue"":""c"",""donor_position"":""3"",""acceptor_position"":""1""},""branch_residues"":[{""branch_id"":""r1"",""residue_descriptor"":""a1122h-1a_1-5""},{""branch_id"":""r2"",""residue_descriptor"":""a2122h-1b_1-5_2*NCC/3=O""},{""branch_id"":""r3"",""residue_descriptor"":""a2112h-1b_1-5""}],""branch_linkages"":[{""donor"":""parent"",""donor_position"":""3"",""acceptor"":""r1"",""acceptor_position"":""1""},{""donor"":""r1"",""donor_position"":""2"",""acceptor"":""r2"",""acceptor_position"":""1""},{""donor"":""r2"",""donor_position"":""4"",""acceptor"":""r3"",""acceptor_position"":""1""}]}"
> glybranch_test_0001,"{""attachment"":{""parent_residue"":""b"",""donor_position"":""6"",""acceptor_position"":""1""},""branch_residues"":[{""branch_id"":""r1"",""residue_descriptor"":""a1122h-1b_1-5""},{""branch_id"":""r2"",""residue_descriptor"":""a1122h-1a_1-5""},{""branch_id"":""r3"",""residue_descriptor"":""a2122h-1b_1-5_2*NCC/3=O""}],""branch_linkages"":[{""donor"":""parent"",""donor_position"":""6"",""acceptor"":""r1"",""acceptor_position"":""1""},{""donor"":""r1"",""donor_position"":""3"",""acceptor"":""r2"",""acceptor_position"":""1""},{""donor"":""r1"",""donor_position"":""6"",""acceptor"":""r3"",""acceptor_position"":""1""}]}"
> Every row must contain valid JSON. A malformed JSON value in one row receives
> score 0 for that row. Wrong row count, duplicate ids, missing ids, extra ids,
> extra columns, or missing columns are rejected.
> Evaluation
> The final score is the mean row score over all test rows.
> For each row, the grader normalizes the submitted JSON into:
> attachment = (parent_residue, donor_position, acceptor_position)
> ordered residue list [(branch_id, residue_descriptor), ...], sorted by
> numeric branch id
> linkage set {(donor, donor_position, acceptor, acceptor_position), ...}
> Sub-scores:
> exact_object = 1 if the normalized submitted attachment, residue list, and
> linkage set exactly match the answer; otherwise 0.
> attachment_score = 0.50 * parent_match + 0.25 * donor_position_match + 0.25 * acceptor_position_match.
> ordered_residue_score = number_of_exact_positionwise_residue_matches / max(predicted_residue_count, true_residue_count). A residue match requires
> both the same branch_id and the same residue_descriptor.
> linkage_f1 = 0 if the predicted linkage set or true linkage set is empty.
> Otherwise, linkage_f1 = 2 * |predicted_linkages ∩ true_linkages| / (|predicted_linkages| + |true_linkages|).
> The row score is:
> row_score = 0.30 * exact_object + 0.25 * attachment_score + 0.25 * ordered_residue_score + 0.20 * linkage_f1
> The final score is:
> score = mean(row_score over all test rows)
> The score range is 0 to 1. A perfect submission scores 1.0.
> Expected Methods
> Use CPU-only glycan graph parsing, branch-consistency constraints, motif
> retrieval, structured prediction, sequence/graph edit modeling, or lightweight
> local machine-learning methods trained only on the provided training rows.
> What Not To Use
> GPU usage is not allowed. Do not use external datasets, external identifier
> lookup, online record queries at prediction time, hosted inference APIs, runtime
> package installation, downloaded or vendored challenge-specific code, restricted
> or gated assets, challenge-specific pretrained checkpoints, trust_remote_code=True,
> or remote-code loaders such as torch.hub.load().

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Variety Seam Detection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7eb5d49eqw997mdwbmzga6yd8ap8se
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat rajat56's score of 0.427!

Full challenge description from page:

> Each example is a single line of text that has been stitched together from several contiguous fragments, where each fragment was copied verbatim from a different one of four closely-related written varieties of a common language. The four varieties (V0, V1, V2, V3) share the same script and the large majority of their vocabulary; they differ mainly in sub-word spelling conventions, a minority of distinctive word forms, and function-word usage. Adjacent fragments always come from different varieties, so the point where one fragment ends and the next begins is a seam.
> Your task, for every token in a line, is to predict which variety it belongs to. From that per-token labelling the seams (the positions where the variety changes) are determined automatically. Because the varieties overlap so heavily, most individual tokens are ambiguous in isolation — a large fraction of word forms are shared by two or more varieties. Reliable labelling therefore requires reading each token in context and exploiting sub-word cues, not a token-by-token dictionary.
> This is a token sequence-labelling / segmentation problem, not a document classification or regression problem. A single variety label per line is not a valid answer.
> Note on generalization: the test lines are built from a different, held-out time period than the training lines, and no source text is shared between the two. Solutions that memorize training vocabulary rather than learning the varieties' distinguishing regularities will generalize poorly.
> Data files
> You are given four files.
> train.csv
> One row per training example. Columns:
> id — string. Unique identifier for the example.
> tokens — string. The example's tokens, separated by single spaces. Tokenization is already done; split on spaces to recover the token list.
> n_tokens — integer. The number of tokens in tokens.
> labels — string. The ground-truth variety label for each token, separated by single spaces, in the same order as tokens. Contains exactly n_tokens labels, each one of V0, V1, V2, V3.
> test.csv
> One row per test example. Columns:
> id — string. Unique identifier for the example.
> tokens — string. The example's tokens, separated by single spaces.
> n_tokens — integer. The number of tokens in tokens.
> There is no labels column in test.csv; predicting it is the task.
> sample_submission.csv
> A valid but naive submission (every token labelled with the single most frequent training variety). Columns:
> id — string. Matches the id values in test.csv.
> labels — string. Space-separated per-token variety labels.
> labels.json
> A JSON array listing the four valid variety codes: ["V0", "V1", "V2", "V3"].
> Submission format
> Produce a CSV named submission.csv with exactly two columns:
> id — string. Exactly the set of id values in test.csv (no missing, no extra, no duplicates).
> labels — string. For each id, a single space-separated string of per-token variety labels. It must contain exactly n_tokens labels for that example, in token order, and every label must be one of V0, V1, V2, V3.
> Any row whose labels has the wrong token count, an unknown label, or an empty/missing value is invalid and will cause the submission to be rejected.
> Evaluation metric
> Submissions are scored with a blended F1 in [0, 1]:
> score = 0.5 * seam_boundary_F1 + 0.5 * token_macro_F1
> seam_boundary_F1. For one example, its seam set is the set of token indices i >= 1 at which the variety label differs from the token at i - 1. Predicted and gold seam sets are compared by exact index. True positives, false positives and false negatives are accumulated across all test examples, and a single micro F1 is computed. A constant, single-variety prediction produces no seams and therefore scores about 0 on this component.
> token_macro_F1. Per-variety token-level F1 (precision and recall over individual token labels), macro-averaged over the four varieties.
> The two components are averaged with equal weight. The final score is floored at a small positive value (a perfectly wrong submission never scores exactly 0) and capped at 1.0.
> Notes for solvers
> The label alphabet is closed and fixed at four codes; there is no "unknown" or "abstain" label.
> Token-by-token lookup tables are weak here on purpose: the varieties share most of their vocabulary, so context and sub-word structure carry the signal.
> The held-out time period means new, unseen word forms will appear at test time; design your validation to reflect generalization rather than memorization.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## PointerTape: Hierarchical Symbol-Binding Program Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cfgq5fj85jxr18c4g7vxt518apjvd
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> PointerTape: Hierarchical Symbol-Binding Program Recovery
> Overview
> Long rulebooks behave like programs: provisions act as modules, cross-references act as pointers, and the document hierarchy supplies a latent namespace. Each row presents a partially erased document program containing two to five ordered binding sites such as [REF_0] and [REF_1]. The task is to recover its binding tape: the row-local symbol assigned to every site, in execution order.
> The row's candidate_bank is a shuffled local symbol table containing 14 provisions. Symbols such as C03 are freshly assigned per row and have no stable meaning across examples. The table combines the true bindings with nearby semantic hard negatives and same-title distractors. Some unscored pointers appear as [OTHER_REF]; [GAP] marks a deterministically withheld word, [URL] replaces a web address, and [SEGMENT] or [CUT] marks document truncation. These operations remove information only from the observable program. They never alter the true binding tape.
> Unlike open-corpus retrieval or single-link resolution, every example requires joint recovery of several bindings inside a randomized namespace. The same candidate may bind multiple sites, and locally plausible bindings can form an implausible tape when considered together. The intended first-order approach is to infer each site's local semantic contract from its surrounding clause, compare that contract with symbol-table entries, use hierarchy as namespace evidence, and decode the complete binding tape jointly in marker order.
> Evaluation Metric
> For row
> 𝑖
> i, let the prediction be
> 𝑦
> ^
> 𝑖
> =
> (
> 𝑦
> ^
> 𝑖
> 1
> ,
> …
> ,
> 𝑦
> ^
> 𝑖
> 𝑛
> )
> y
> ^
> ​
> i
> ​
> =(
> y
> ^
> ​
> i1
> ​
> ,…,
> y
> ^
> ​
> in
> ​
> ) and the target be
> 𝑦
> 𝑖
> =
> (
> 𝑦
> 𝑖
> 1
> ,
> …
> ,
> 𝑦
> 𝑖
> 𝑚
> )
> y
> i
> ​
> =(y
> i1
> ​
> ,…,y
> im
> ​
> ).
> Let
> 𝑑
> l
> e
> v
> (
> 𝑦
> ^
> 𝑖
> ,
> 𝑦
> 𝑖
> )
> d
> lev
> ​
> (
> y
> ^
> ​
> i
> ​
> ,y
> i
> ​
> ) be token-level Levenshtein distance. The edit similarity is
> [
> E_i=\max\left(0,1-\frac{d_{\mathrm{lev}}(\hat y_i,y_i)}{\max(n,m,1)}\right).
> ]
> Every candidate belongs to a title, chapter, part, and section. For a predicted candidate
> 𝑎
> a and target candidate
> 𝑏
> b, define
> [
> h(a,b)=0.15\mathbf{1}[T_a=T_b]+0.20\mathbf{1}[C_a=C_b]+0.25\mathbf{1}[P_a=P_b]+0.40\mathbf{1}[S_a=S_b].
> ]
> Compare candidates at the same sequence position. A missing, extra, or invalid token has hierarchy similarity zero. The row hierarchy term is
> [
> H_i=\frac{1}{\max(n,m,1)}\sum_{j=1}^{\max(n,m)}h(\hat y_{ij},y_{ij}),
> ]
> where an out-of-range position contributes zero.
> Form the multisets of adjacent candidate-token bigrams in the prediction and target. Let their multiset overlap count be
> 𝑐
> 𝑖
> c
> i
> ​
> , predicted bigram count be
> 𝑝
> 𝑖
> p
> i
> ​
> , and target bigram count be
> 𝑡
> 𝑖
> t
> i
> ​
> . Define
> [
> P_i=\frac{c_i}{p_i},\qquad R_i=\frac{c_i}{t_i},\qquad B_i=\frac{2P_iR_i}{P_i+R_i}.
> ]
> Set
> 𝐵
> 𝑖
> =
> 0
> B
> i
> ​
> =0 if either sequence has no bigram or if the denominator is zero.
> Average each row term over the
> 𝑁
> N test rows:
> [
> E=\frac{1}{N}\sum_iE_i,\qquad H=\frac{1}{N}\sum_iH_i,\qquad B=\frac{1}{N}\sum_iB_i.
> ]
> The final score is
> [
> \mathrm{Score}=100\times\operatorname{clip}(0.45E+0.35H+0.20B,0,1).
> ]
> A score of 0 means no usable binding-tape agreement. A score of 100 means every binding and every adjacent transition is recovered exactly.
> Measured public-data-only references: sample submission 0.000000; single-token constant 8.492991; length-aware constant 18.979362; hand-built token/bigram overlap heuristic 33.705496; CPU gradient-boosted pair ranker using overlap features 42.243571; perfect 100.000000.
> Dataset
> train.csv - 7,299 labeled examples.
> sample_id - int64 - Content-free row identifier.
> redacted_section - string - Regulatory text with ordered target markers and lossy input markers.
> hierarchy_view - string - JSON object containing the query title, chapter, part, and section-heading names.
> candidate_bank - string - JSON list of 14 local candidate objects.
> render_profile - string - Balanced nuisance value A or B; it is not a target.
> target_sequence - string - Ground-truth binding tape as ordered, space-separated row-local symbols.
> test.csv - 1,768 query examples with the same query columns and no target column.
> sample_submission.csv - Required header and every test identifier.
> Every candidate_bank item contains:
> candidate_id - string - Row-local identifier from C00 through C13.
> title_name - string - Candidate regulatory title name.
> chapter_name - string - Candidate chapter name.
> part_name - string - Candidate part name.
> heading - string - Candidate section heading with its numeric citation removed.
> excerpt - string - Candidate provision excerpt with direct citations and URLs masked.
> Candidate order is shuffled independently for each row. Candidate identifiers cannot be transferred between rows.
> Submission
> sample_id - int64 - Must match every identifier in test.csv exactly once.
> target_sequence - string - The binding tape: one candidate identifier (for example, C07) for each [REF_i] marker, space-separated in ascending marker order. Every identifier must be one of C00 through C13 from that row's candidate_bank.
> Submit exactly 1,768 data rows plus the header. The exact column order is sample_id,target_sequence. Extra or reordered columns, duplicate IDs, missing IDs, unknown IDs, and wrong row counts are rejected. Row order may differ because scoring aligns by ID. Empty, missing, non-string, or malformed prediction values receive worst-case credit for the affected positions and never provide an abstention advantage.
> Example using real test IDs:
> sample_id,target_sequence
> 6,C13 C09
> 8,C01 C01
> 15,C11 C05 C00
> What Not to Use
> A single constant candidate fails because candidate identifiers are randomized independently for every row.
> Counting the markers without reading their clauses predicts only output length and does not identify the referenced provisions.
> Candidate title alone is insufficient because distractors are deliberately sampled from the same regulatory title.
> Whole-document lexical similarity misses cases where different markers in the same section refer to different provisions.
> Nearest-neighbor copying from training rows fails because the split is disjoint by regulatory part and exact query duplicates are removed.
> render_profile is balanced within target-length groups and is not informative about the answer.
> Successful systems should treat the row as a small symbol-binding program and combine site-local semantics, candidate contracts, hierarchy information, repeated-symbol behavior, and ordered tape consistency.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Typographic Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73713f7t95jrqk8edmscccv58aqh4j
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Typographic Reconstruction
> Domain: Natural Language Processing — text restoration over token sequences. You are given English prose with its entire typographic layer destroyed, and must rebuild that layer: where the writer paused, where each sentence ended, and which stretches of the text were spoken aloud by a character. Your output is a restored sequence, one symbol per word, aligned to the words you were given.
> Overview
> A page of prose carries two channels. One is the words. The other is everything wrapped around them — the commas, the full stops, the quotation marks that tell you a person has started speaking. Strip the second channel away and the words survive intact while the prose stops working:
> she said i cannot go he turned away then you have decided
> Restore it and the passage snaps back into shape:
> "She said I cannot go." He turned away. "Then you have decided?"
> Every item here is a passage of roughly 240 words from a nineteenth- or early-twentieth-century novel, flattened to a bare lowercase word stream: all punctuation removed, all capitalisation removed, all quotation marks removed, all paragraph and line structure removed. Nothing but words and single spaces remains.
> Your task is to rebuild the typography from the words alone. For each token you recover three things at once:
> PAUSE — the token is followed by a within-sentence break: a comma, semicolon, colon or dash
> STOP — the token ends a sentence: a full stop, question mark or exclamation mark
> QUOTE — the token lies inside spoken dialogue rather than narration
> This is the problem that sits at the end of every speech recogniser and every historical digitisation pipeline. An ASR system emits an unpunctuated word stream; OCR of a damaged page loses the light marks first — commas and quotes are the smallest ink on the page. The words come back cheaply. The typography has to be inferred, and inferring it is what makes the text readable again.
> The tag alphabet
> You describe the restored typography with one character per token, from a six-letter alphabet that crosses the speech channel with the mark channel:
> a = narration, no mark follows      d = spoken, no mark follows
> b = narration, PAUSE follows        e = spoken, PAUSE follows
> c = narration, STOP follows         f = spoken, STOP follows
> So a means an ordinary narrative word in mid-clause; f means the last word of a spoken sentence. The tag string for a passage has exactly one character per word, in order.
> For the fragment she said i cannot go he turned away restored as "She said I cannot go." He turned away. the tags run d d d d f a a c, written ddddfaac.
> Evaluation
> Your submission is scored on the three typographic surfaces, each measured independently over every token pooled across all passages, then averaged:
> PAUSE  = F1 over tokens whose tag is in {b, e}
> STOP   = F1 over tokens whose tag is in {c, f}
> QUOTE  = F1 over tokens whose tag is in {d, e, f}
> score  = (PAUSE + STOP + QUOTE) / 3
> The score lies in [0.0, 1.0] and higher is better. The three surfaces are averaged rather than pooled because they are wildly unequal in frequency: about 9.2% of tokens take a PAUSE, 6.0% take a STOP, and 45.7% sit inside dialogue. A single pooled figure would let the dialogue surface bury the other two. Averaging means restoring commas well matters as much as restoring dialogue well, and that emitting one surface everywhere earns almost nothing: marking every token as spoken scores 0.215, marking every token as a PAUSE scores 0.055, and a submission with no typography at all scores 0.000.
> An exact reference implementation:
> def evaluate(y_true: dict, y_pred: dict) -> float:
> # both map passage id -> tag string; y_pred must cover every id in y_true
> surfaces = (set("be"), set("cf"), set("def"))
> scores = []
> for members in surfaces:
> tp = fp = fn = 0
> for pid, gold in y_true.items():
> pred = y_pred[pid]
> if len(pred) != len(gold) or not set(pred) <= set("abcdef"):
> pred = "a" * len(gold)          # malformed scores as "no typography"
> for g, p in zip(gold, pred):
> gi, pi = g in members, p in members
> tp += gi and pi
> fp += pi and not gi
> fn += gi and not pi
> prec = tp / (tp + fp) if tp + fp else 0.0
> rec = tp / (tp + fn) if tp + fn else 0.0
> scores.append(2 * prec * rec / (prec + rec) if prec + rec else 0.0)
> return sum(scores) / len(scores)
> Dataset
> You are given a public/ folder with three files:
> train.csv — columns id, text, tags. id is a random passage identifier, text is the bare word stream, and tags is the restored tag string, exactly one character per word. There are 2700 training rows.
> test.csv — columns id, text. The 1260 passages you must restore. No tags column.
> sample_submission.csv — columns id, tags. A correctly formatted example submission. Its entries come from a weak baseline, not from the answer key.
> Passages run 233 to 250 words. The training and evaluation passages come from completely different books — no book appears on both sides — so a solution must recover general typographic structure rather than memorise one novel's habits.
> Submission
> Submit a single CSV with exactly the columns id and tags, one row for every id in test.csv (1260 rows). Row order does not matter; the grader joins on id. Any additional columns are ignored. Example, using real test ids from this task with the opening of their true tag strings:
> id,tags
> p2dcc2da2a857cb20,aabaabaaaaaaabaacaaaacaaaaaa...
> p22f8a53c52a69507,faaabaaaaaaaaaaabaaaabaaabaa...
> p02f01db6cbca9f3b,aaaaaaddfaabaaaabaaaaaaaaaaa...
> Requirements
> Give exactly one tag string for each of the 1260 test ids; the set of ids in your submission must equal the set of ids in test.csv (no missing, extra, duplicate, or unrecognised ids, or the submission is rejected).
> Each tag string must have exactly as many characters as its passage has words, drawn from abcdef. A string of the wrong length, or containing any other character, is scored as the worst legal answer — all a, meaning no typography anywhere — not as an error.
> Blank / NaN entries are scored the same way. A submission with no usable entries at all is rejected.
> The id values are opaque strings; do not assume any ordering or structure.
> What not to use
> No pretrained models, embeddings, or weights of any kind — no pretrained or masked language models, no downloaded word vectors, no off-the-shelf punctuation restorers, taggers, or sentence splitters carrying learned parameters. Build everything from the provided train.csv.
> No external data or resources — no other text corpora, no internet access at training or inference time.
> Do not attempt to re-identify the source texts. Do not match passages back to any external copy of these public-domain books to read the punctuation off the original.
> Only the words in the provided passages are meant to solve this task. (These restrictions are enforced by the evaluation harness, not by the grader.)
> Some extra modelling information
> The evidence is syntactic, not lexical. The cue is the shape of the clause around it, and in nineteenth-century prose those clauses are long, nested, and chained — exactly where a short context window runs out of information.
> Two of the three surfaces are rare. PAUSE covers 9.2% of tokens and STOP 6.0%, and they weigh as much in the score as dialogue at 45.7%. Anything that optimises plain accuracy will quietly learn to emit nothing and score near zero on two thirds of the metric. Optimising the score you are actually given, rather than the loss that comes for free, is most of the work here.
> Dialogue has no marker left in it. The quotation marks are gone. Whether a stretch of words is spoken has to be read off register, pronouns, speech verbs, and the way spans begin and end — and spans are long, so a single flipped token in the middle of a speech costs a run of errors.
> The books do not overlap. Training and evaluation passages come from different novels, so a house style learned from one author's punctuation does not simply transfer.
> The shortcuts are closed. No pretrained weights, no external corpora, CPU only. Every modern result on this problem leans on a pretrained language model; here you build the model from 2700 passages and nothing else.
> A perfect score is out of reach by construction — some marks were deleted with their words, and a comma before a coordinating conjunction is a genuine authorial choice rather than a fact waiting to be recovered. The work is in getting the recoverable structure back.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Lyric Underlay Alignment Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7db7t7stpehdcrn24dfmkc8s8ann0z
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Lyric Underlay Alignment Recovery
> Overview
> Recover the lyric underlay alignment for short protected vocal excerpts from authentic symbolic music scores.
> Each row contains note-event cards from one vocal excerpt and a shuffled set of lyric-syllable cards. The original MuseScore placement of lyrics has been hidden. Your task is to map every syllable card to the note event that carries that syllable in the source notation.
> The excerpts are selected to avoid easy one-note-per-syllable cases. Rows contain extra note events without new syllables, melismatic passages, repeated rhythmic patterns, and ambiguous nearby note positions. A strong solution must learn how lyric syllables align with musical rhythm, note duration, phrase structure, and syllabic markers rather than simply assigning syllables to the next chronological note.
> This is a symbolic-music alignment task, not audio transcription, voice separation, note-to-note continuation, classification, retrieval, or music generation.
> Dataset
> The prepared challenge contains 936 unique examples derived from 936 distinct complete source scores. Every source score contributes exactly one row.
> train.csv: 699 examples with the correct answer_json.
> test.csv: 237 examples without answers.
> sample_submission.csv: 237 structurally valid dummy predictions.
> Complete source scores remain within one split:
> distinct training source scores: 699;
> distinct evaluation source scores: 237;
> train/evaluation source-score overlap: 0;
> maximum rows contributed by one score: 1.
> The feature columns are:
> id: string. Opaque row identifier.
> prompt: string. Task instruction.
> underlay_packet_json: JSON object. Contains time signatures, shuffled note-event cards, and shuffled lyric-syllable cards.
> event_count: integer. Number of note events in the excerpt.
> syllable_count: integer. Number of lyric syllables requiring alignment.
> answer_json: JSON object, train only. Contains syllable_note_map, a mapping from every row-local syllable ID to the row-local note-event ID that carries it.
> The underlay_packet_json object contains:
> time_signatures: JSON list of time-signature objects.
> event_cards: JSON list of shuffled note-event cards from the vocal excerpt.
> syllable_cards: JSON list of shuffled lyric-syllable cards from the same excerpt.
> Each time-signature object contains:
> measure_offset: integer. Measure offset inside the protected excerpt.
> numerator: integer. Time-signature numerator.
> denominator: integer. Time-signature denominator.
> Each event card contains:
> event_id: string. Row-local opaque note-event ID.
> measure_offset: integer. Protected measure offset.
> onset_tick: integer. Onset position inside the measure.
> measure_ticks: integer. Number of ticks in the measure.
> duration_tick: integer. Note duration in ticks.
> pitch: integer. Transposed MIDI pitch.
> tie_in: boolean. Whether the note continues from a previous tied note.
> tie_out: boolean. Whether the note continues into a later tied note.
> Each syllable card contains:
> syllable_id: string. Row-local opaque syllable ID.
> lyric_position: integer. Order of the syllable inside the protected lyric sequence.
> token_aliases: JSON list of protected lyric-token aliases.
> syllabic: string. Source syllabic marker such as single, begin, middle, or end.
> The row ranges are:
> event count: 18–48, median 33;
> syllable count: 12–40, median 26.
> Submission Format
> Submit a CSV with exactly the two columns id and answer_json, in that order.
> Each answer_json value must contain exactly one field: syllable_note_map.
> The syllable_note_map value must be an object whose keys are all and only the syllable IDs displayed in that row. Each value must be one of the note-event IDs displayed in the same row. Every note-event ID may be used at most once.
> Example:
> id,answer_json
> lua_example_01,"{""syllable_note_map"":{""sy_a1"":""ev_b2"",""sy_c3"":""ev_d4""}}"
> Malformed JSON, missing or extra fields, missing syllable IDs, extra syllable IDs, unknown note-event IDs, duplicate note-event assignments, and invalid mappings receive zero credit for that row.
> Duplicate row IDs, null row IDs, unknown row IDs, missing rows, extra rows, extra columns, or an incorrect column order are rejected.
> Evaluation
> For a row with m syllables, underlay accuracy is the fraction of syllables whose submitted note-event assignment exactly matches the source alignment.
> row_score = correctly_aligned_syllables / m
> leaderboard_score = mean(row_score over all test rows)
> Scores for valid submissions range from 0 to 1, and higher is better.
> The metric contains no separate ordering, set-overlap, voice-continuation, or partial-component weights. Every syllable contributes one alignment decision.
> Expected Methods
> Suitable CPU methods include rhythmic alignment models, syllable-to-note compatibility features, monotonic sequence alignment, pairwise scoring models, lightweight classifiers, dynamic-programming decoders, and small CPU-trained sequence models.
> Validation must use training data only and respect complete-score grouping.
> What Not To Use
> GPUs, TPUs, accelerators, or GPU-backed services for any stage;
> external score lookup, source-record lookup, lyric lookup, dictionary lookup, or external datasets;
> hosted APIs, remote inference services, runtime downloads, or runtime package installation;
> pretrained challenge-specific checkpoints or checkpoints fine-tuned on this task outside the supplied training data;
> hardcoded row-ID mappings, hardcoded test answers, manual test annotation, selected-row patches, or answer tables;
> original score titles, composer names, file paths, MuseScore IDs, or source metadata not present in the public files;
> row-order, opaque-ID, or dataset-construction artifact exploitation;
> test-set fitting, pseudo-labeling, clustering, distribution calibration, or cross-row test adaptation;
> TF-IDF;
> BM25;
> a rule-only chronological, proportional, or next-note assignment as the complete solution.
> General-purpose software already installed in the CPU runtime may be used when it contains no challenge-specific answers and requires no network access. All task-specific fitting must occur inside the submitted solution using only train.csv.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Folk Harmonic Analysis: Chord-Function Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bqd2cx71ayjhj2svx0f15p18ahq1h
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat dongfuhan's score of 0.483!

Full challenge description from page:

> Folk Harmonic Analysis: Chord-Function Recovery from a Bare Melody
> Type: Sequence labeling (structured prediction) · Difficulty: medium · Higher score is better · Score range: 0 to 1
> Overview
> A traditional dance tune is just a single line of melody, yet a musician can hear the harmony implied by that line: where the tonic chord sits, where the music pulls toward the dominant, where a cadence resolves. Your task is to teach a model to do the same — given nothing but a bare, key-normalised melody, predict the harmonic function (the chord) sounding under every melody note.
> The melodies are real traditional folk dance tunes (jigs, reels, hornpipes, waltzes, morris tunes, country dances and more). Every tune has been transposed so that its tonic is C: whether the original was written in D, A, G or E-flat, you always receive it centred on C. The written key signature, the tune title, the mode, and the original chord symbols have all been removed. Because every tune shares the same tonic, the pitch of a note tells you its scale degree directly — but the pitch of a single note does not tell you the harmony: the same melody note can be harmonised by the tonic, the subdominant, a submediant, or a secondary dominant depending on where it falls in the phrase and what surrounds it. Recovering the harmony therefore requires reading the melody in context.
> This is the classical problem of automatic harmonic analysis / melody harmonisation, posed here on folk melodies at note resolution. It is a structured-prediction task: the label of each note depends on its neighbours (local melodic motion, metric position, the approach to a cadence, the phrase the note lives in), not on that note in isolation. A model that looks at each note independently will do poorly; a model that reads the melodic line as a sequence will do much better.
> For every note in every test tune, predict one harmonic-function label from a fixed 16-token vocabulary — 15 named chord classes plus OTHER — listed below.
> The Chord Vocabulary
> The vocabulary has 16 tokens: 15 named chord classes plus OTHER. Because all tunes are transposed to tonic C, each named chord is given as an absolute chord name in C, which is exactly its Roman-numeral function. The 15 named classes cover ~98% of notes; anything else is OTHER. Only the 15 named classes are averaged into the score (see Evaluation).
> Token	Function	Description
> C	I	tonic major
> Cm	i	tonic minor
> Dm	ii	supertonic minor
> D	II	supertonic major
> D7	V7/V	secondary dominant of the dominant
> Eb	bIII	flat-mediant major (modal/borrowed)
> F	IV	subdominant
> Fm	iv	subdominant minor
> G	V	dominant
> G7	V7	dominant seventh
> Gm	v	minor dominant
> Am	vi	submediant minor
> Bb	bVII	subtonic major (modal)
> E7	V7/vi	secondary dominant of the submediant
> C7	V7/IV	tonic seventh (dominant of the subdominant)
> OTHER	—	any chord outside the 15 named functions
> Dataset
> The public data is three CSV files. Each melody note is one row. Notes belong to tunes; you reconstruct each tune's melodic sequence by grouping rows with the same tune_id and ordering them by note_index. The split is held out by tune: no tune in test.csv appears in train.csv, so you must learn harmony that generalises to unseen melodies, not memorise tunes. There are 816 training tunes (~82k notes) and 205 test tunes (~20k notes).
> The mode of each tune (major, minor, dorian, mixolydian, …) is not given; infer it from the melody. The meter is given.
> train.csv — labelled notes, one row per note:
> Column	Type	Description
> tune_id	int	Identifies the tune a note belongs to. Group by this.
> note_index	int	0-based position of the note within its tune. Order by this.
> meter	string	The tune's time signature, e.g. 4/4, 6/8, 3/4, 9/8.
> pitch	int	MIDI pitch. The tonic is pitch class 0 (pitch % 12: 0 = tonic C, 7 = dominant G, …). Absolute octave is randomised per tune and is not meaningful; range ~36–96.
> dur	float	Note duration in quarter-note beats (0.5 = eighth note).
> pos	float	Metric position: offset within the bar in quarter-note beats (0.0 = downbeat).
> bar	int	0-based bar index of the note within the tune.
> chord	string	Target: the harmonic-function label (one of the 16 tokens).
> test.csv — unlabelled notes. Same columns as train.csv except there is no chord column, plus one extra leading column:
> Column	Type	Description
> id	int	Unique note identifier used for submission and scoring.
> (followed by tune_id, note_index, meter, pitch, dur, pos, bar as above.)
> sample_submission.csv — a correctly formatted dummy submission (predicts C for every note), with columns id, chord.
> Evaluation
> Submissions are scored by the macro-averaged F1 over the 15 named chord classes (the OTHER class is not averaged into the score). For each named class c, with precision P_c and recall R_c computed over all test notes:
> F1_c  = 2 * P_c * R_c / (P_c + R_c)          (0 if undefined)
> score = (1/15) * sum over the 15 named classes of F1_c
> Higher is better; the score lies in [0, 1]. Macro-averaging weights every harmonic function equally, so you cannot score well by predicting only the common chords: a model that predicts the tonic chord (C) for every note scores about 0.04, and a context-free per-note classifier scores about 0.14. Getting the rarer but musically crucial functions right (dominant sevenths, secondary dominants, modal Bb, minor-mode chords) is where the score is won.
> Reference points on this split (macro-F1): all-tonic baseline ~0.04; context-free per-note logistic regression ~0.14; a small from-scratch bidirectional-RNN sequence tagger trained for ~2 minutes on CPU ~0.43. These are guides, not targets — stronger sequence models, CRF decoding, and ensembling can go higher. The task is genuinely hard: folk harmonisation is ambiguous (many notes admit more than one defensible chord) and the ground-truth transcriptions carry human labelling noise, so a perfect score is not attainable.
> Submission
> Submit a CSV with exactly two columns and one row for every note in test.csv:
> Column	Type	Description
> id	int	The note id from test.csv. Each test id must appear exactly once.
> chord	string	Predicted harmonic-function label, one of the 16 vocabulary tokens. A token outside the vocabulary is treated as OTHER.
> Include the header row. The submission must contain exactly the same set of ids as test.csv (no missing ids, no extra ids, no duplicates), or it is invalid and is not scored. Example:
> id,chord
> 0,C
> 1,G7
> 2,F
> Method Requirements
> A real machine-learning model must do the learning. The intended solution trains a model (from scratch on the provided melodies, or by fine-tuning an open symbolic-music sequence encoder) that reads each melody as a sequence and predicts the harmonic function at each note. Modelling melodic context is expected; a purely per-note, context-free classifier is a permitted but weak baseline.
> Prohibited (may be rejected before payout even if the CSV is structurally valid):
> Hard-coded or purely rule-based harmonisation (fixed "scale-degree → chord" lookup tables, hand-written harmony rules) that is not learned from the data.
> Using any external data or resource — in particular, attempting to identify the source collection, or to look these melodies up (by their notes or by any other means) in an external music database, tune archive, or notation website in order to recover their original chord annotations. All harmony must be predicted from the provided melody alone.
> Using the test set as anything other than one-tune-at-a-time inference: no training or fitting on test notes, no pseudo-labelling, no test-time adaptation, no calibrating to the test distribution.
> Manually labelling test notes or shipping a hard-coded id-to-chord map.
> Allowed: training any model on the provided train.csv (RNNs, temporal CNNs, transformers, CRFs, HMMs, gradient-boosted or linear models with engineered context features); standard sequence-tagging techniques; ensembling models trained inside your script; per-tune inference such as Viterbi/CRF decoding over a single tune's note sequence.
> Runtime: the solution must run end-to-end (read raw data, train, write the submission) on CPU within the time limit. The task is small; a strong model trains comfortably on CPU in the available budget.
> Expected Output
> Output to ./working/submission.csv.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Conditional Peptide Enrichment-Path Capsule

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dacjwr0724pcn30hdvw4bed8aa87x
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Beat hair0nfire's score of 0.521!

Full challenge description from page:

> # Conditional Peptide Enrichment-Path Capsule
> Overview
> This is a sequence-to-sequence / NLP challenge: read one joint query string and write back a short enrich_path capsule.
> query  →  enrich_path
> Each query already pairs a peptide with an opaque selection-channel code. Your job is to predict how enrichment intensity moves across four successive selection rounds for that pair — not which channel binds the peptide.
> query:        NRMMMLAPK|||CHa1b2c3
> enrich_path:  R1:L R2:M R3:H R4:P
> Band codes: Z (zero), L (low), M (medium), H (high), P (peak). Peptide letters in query are contest encodings; band letters stay canonical.
> Dataset
> Contestant files under public/:
> public/
> train.csv
> test.csv
> sample_submission.csv
> public/train.csv — 4902 rows: id, query, enrich_path
> public/test.csv — 817 rows: id, query
> public/sample_submission.csv — 817 rows: id, enrich_path (placeholders)
> Train and test query values are disjoint. The package uses 16 opaque channel tokens.
> Column types
> id (string): opaque row id, format row_ + 12 lowercase hex chars (example: row_91f21f293774). Present in all three files.
> query (string): model input PEPTIDE|||CHxxxxxx. Peptide is a length-9 amino-acid string; channel is CH + 6 hex chars (example: MVRRHLSKV|||CHc976e4). Present in train.csv and test.csv.
> enrich_path (string): target capsule R1:B R2:B R3:B R4:B with each B in {Z,L,M,H,P} (example: R1:L R2:M R3:M R4:M). Present in train.csv and sample_submission.csv. This is the column to predict.
> Evaluation
> Metric: EPTF1 (Enrichment Path Token F1)
> Maximize. Range [0, 1]. Perfect → 1.
> Split each enrich_path on spaces, |, ,, or ; into tokens. Malformed tokens (for example R4:INVALID) are kept and lower precision. A prediction must include exactly four distinct rounds R1–R4; otherwise that row scores 0.
> precision = |P ∩ T| / |P|
> recall    = |P ∩ T| / |T|
> EPTF1_1   = 2 * precision * recall / (precision + recall)
> EPTF1     = mean(EPTF1_1 over all test ids)
> Submission must match answers in row count and id set.
> Outcome	EPTF1
> Exact four-token path	1
> Partial overlap (all four rounds present)	between 0 and 1
> Dropped round / wrong / empty	0 or near 0
> Submission
> Upload one CSV with header:
> id,enrich_path
> Every test id from public/test.csv exactly once
> Prefer R1:X R2:Y R3:Z R4:W with bands in {Z,L,M,H,P}
> No extra columns
> Template: public/sample_submission.csv
> id,enrich_path
> row_111111111111,R1:L R2:M R3:H R4:P
> row_222222222222,R1:Z R2:Z R3:Z R4:Z
> Only id and enrich_path are graded.
> What Not To Use
> Do not use grader artifacts, hidden labels, or files outside public/
> Do not recover test labels via external databases or web APIs
> Do not reverse-engineer opaque CH… tokens
> Do not submit columns other than id, enrich_path
> Only public/ may be used for training and inference

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Joint Discourse Intruder Filtering and Sequence Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7edwq644x18qmsc1qhtd7and8a9cq4
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Real text processing systems can accidentally combine fragments from different customer messages during batching, deduplication, or asynchronous ingestion. Before downstream analysis, a system must remove unrelated fragments and restore the genuine message fragments to their original discourse order.
> Each example contains eight shuffled privacy preserving discourse pieces. Exactly six pieces come from consecutive clauses of one real customer review. The remaining two pieces are intruders selected from different reviews with similar context, length, punctuation, and discourse cues.
> The task is to identify the six genuine pieces and return their identifiers in the original order. A valid prediction must remove both intruders and reconstruct the six piece sequence.
> WHY THE TASK IS HARD
> Each example has 20,160 legal six piece outputs. The intruders are deliberately chosen to look plausible rather than unrelated. Original review text, product identifiers, ratings, categories, and source row identifiers are not available. Topic labels are local to each example and have no meaning across different rows. The train and hidden test partitions are product disjoint. Strong solutions must combine intruder detection, pairwise order prediction, and globally valid sequence decoding.
> DATASET
> The public directory contains train.csv, test.csv, and sample_submission.csv.
> The train.csv file contains one row per training example. Its first column is review_id. The next eight columns are piece_1 through piece_8. Each piece column contains one anonymized discourse sketch. The final column is target_sequence, which lists the six genuine piece identifiers in their original order separated by single spaces.
> The test.csv file has the same review_id and piece_1 through piece_8 columns. It does not contain target_sequence.
> The sample_submission.csv file contains the required submission columns and one example prediction for every hidden test row.
> TARGET
> For every review_id in test.csv, predict exactly six distinct identifiers selected from piece_1 through piece_8. The identifiers must be arranged in the predicted original discourse order. The two omitted identifiers are treated as intruders.
> SUBMISSION
> Submit a CSV file named submission.csv.
> The first column must be named review_id.
> The second column must be named repaired_sequence.
> The file must contain exactly one row for every review_id in test.csv and no additional rows. review_id values must be unique. repaired_sequence must contain exactly six distinct valid piece identifiers. Separate the six identifiers with single spaces and do not include extra columns.
> A valid repaired_sequence value looks like this:
> piece_7 piece_2 piece_5 piece_1 piece_8 piece_3
> EVALUATION
> Submissions are scored with mean ordered pair recovery.
> For one hidden example, the true six piece sequence defines 15 ordered pairs. A pair receives credit only when both pieces appear in the submitted sequence and the first piece appears before the second piece. The score for one example is the number of recovered true ordered pairs divided by 15. The final score is the arithmetic mean across all hidden examples.
> A completely correct selection and order scores 1.0. Reversing all six true pieces scores 0.0. Including an intruder reduces the score because every true pair involving the omitted genuine piece is lost. Higher scores are better.
> COMPUTE REQUIREMENTS
> This is a CPU only challenge. A solution must complete within 1.5 hours on 10 CPU cores and 62 GB of memory. The reference solution uses sparse CPU models and constrained decoding. No GPU, hosted model, or external inference service is required.
> SOURCE SAFETY AND RULES
> The public files do not expose original review text, titles, source row numbers, product identifiers, ratings, recommendation labels, ages, category names, feedback counts, or URLs. The transformation is intentionally lossy and local to each example so public snippets cannot be searched back to source rows.
> Predictions must come from a generalizable algorithm trained only from the public challenge files. External source lookup, hidden labels, hardcoded test answers, row order assumptions, and row specific manual rules are not permitted.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Recovering the Causal Graph of an Accident from its Narrative

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78tvwr4whqesp9axxb4bxkcd8a48wj
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> When an aircraft accident is investigated, the finding is written up as a free-text narrative: who did what, to which part of the aircraft, under what conditions, what went wrong, and why. Buried in that prose is a small causal graph — the people and objects involved, the actions taken, the undesired events that occurred, and the causal and observational links between them.
> This challenge asks your model to read one narrative and recover that graph. For each narrative you must predict two things at once:
> the typed entities — every span of text that is an actor, an object, an action, an event, a condition, a finding, or a causal factor (9 types); and
> the typed relations between them — which action was performed by which agent, which event was caused by which factor, which object has which finding, and so on (6 types).
> Finding the entities is the routine half; reconstructing the relations — especially the causal ones — is the hard half, because it requires reading the narrative's logic, not just spotting noun phrases.
> Data
> train.csv — one row per training narrative: item_id, text, entities, relations.
> text — the raw narrative string. Character offsets below index into this exact string.
> entities — JSON list of gold entities, each [start, end, label] (0-based, end-exclusive character span; text[start:end] is the mention).
> relations — JSON list of gold relations, each [src_start, src_end, relation, tgt_start, tgt_end] — a directed, typed link from the source entity span to the target entity span.
> test.csv — item_id, text for the narratives to annotate (entities and relations withheld).
> sample_submission.csv — a valid submission with a simple gazetteer baseline.
> metadata.json — the label sets, submission schema, and metric.
> Entity labels (9): Agent, Aircraft, PhysicalObject, HumanAction, UndesiredEvent, ObservationFinding, EnvironmentalCondition, CausalFactor, RegulatoryItem.
> Relation labels (6): performedBy (action→agent), appliedTo (action→object), hasState (entity→event/condition), hasFinding (entity→observation), causedBy (event→cause), occursIn (event→condition/location).
> Task
> For every test narrative, output its typed entity spans and the typed relations between those spans. Narratives vary in length; some have many entities and relations, some few.
> Evaluation
> Score = 0.50 · EntityMicroF1 + 0.50 · RelationMicroF1, in [0, 1], higher is better.
> EntityMicroF1 — a predicted entity is a true positive only if its (start, end, label) exactly matches a gold entity (exact span and correct type). Micro-averaged over all narratives.
> RelationMicroF1 — a predicted relation is a true positive only if its (src_start, src_end, relation, tgt_start, tgt_end) exactly matches a gold relation (both endpoint spans and the relation type). Micro-averaged over all narratives.
> Getting the entities right but the relations wrong caps the score at 0.5; the relations — which encode the accident's causal structure — are where the task is won or lost.
> Submission format
> A CSV with exactly these columns, one row per predicted item:
> item_id,kind,start,end,label,tgt_start,tgt_end
> acc_ade4e7d4c26e,entity,17,22,Agent,-1,-1
> acc_ade4e7d4c26e,entity,31,44,HumanAction,-1,-1
> acc_ade4e7d4c26e,relation,31,44,performedBy,17,22
> kind — entity or relation.
> entity row: (start, end) is the entity span and label its entity type; set tgt_start/tgt_end to -1.
> relation row: (start, end) is the source entity span, (tgt_start, tgt_end) the target entity span, and label the relation type.
> A narrative with no predictions simply has no rows.
> Requirements (violations rejected as invalid): exactly the columns above; item_id non-null and only known test ids; kind in {entity, relation}; numeric start/end/tgt_start/tgt_end; at most 3000 predicted items per narrative. A row with bad geometry or an unrecognised label is not rejected — it simply fails to match (scores nothing).
> Allowed
> Fine-tune a pretrained language model (encoder for token tagging + a relation classifier, or a seq2seq/generative IE model) or train from scratch on the provided narratives and labels — with any tokenisation, span-enumeration, or joint-decoding strategy. Use only libraries already in the runtime and public general-purpose pretrained weights (e.g. a general text encoder); everything must run offline.
> What Not To Use
> No runtime installs or downloads — no pip/conda/apt installs and no fetching or vendoring extra packages, code, or model files; use only what is in the runtime.
> No external data or network access — no external entity/relation annotations for these narratives and no downloading data over the network. A general-purpose pretrained text encoder is fine.
> No remote or dynamic models — no hosted inference APIs, gated checkpoints, trust_remote_code=True, torch.hub.load(), or passing a challenge-specific fine-tuned checkpoint off as "pretrained".
> No attempting to identify or retrieve the source corpus or any external annotation of it, and no use of any answer/label file.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Chemical Plant Failure-Cause Graph Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx753rjrw48dxr649697kwxp7x8a03zn
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: small-data
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> In plain language, the objective is to recover a structured failure record from real chemical-plant operation streams.
> Each row is a time window from a laboratory batch chemical plant. The public input is a compact sequence file containing synchronized normalized feature channels derived from real sensor values, actuator values, sensor measurement uncertainty, and interpolation indicators. The hidden target says when failure phases become observable and recover, what failure mode is present, which component is affected, which observed effects and sensors support the event, whether the event is transient/recurrent/permanent, and whether the cause is known or genuinely unknown.
> This is not a binary anomaly-detection task, not one label per experiment, and not continuous-value regression. A valid answer is a variable-length event timeline plus a directed evidence graph for each row.
> Submit these fields for every test row:
> timeline_json: ordered phase intervals.
> event_graph_json: directed failure/evidence graph.
> confidence: numeric row confidence in [0,1].
> CPU only: solutions must finish within 1.5 hours on 10 CPU cores and 62 GB RAM. Practical methods include engineered temporal features, change-point detection, 1D CNN/TCN models, compact sequence encoders, nearest-neighbor features used inside learned models, and constrained graph decoders. GPU-only systems, hosted models, and runtime internet access are not allowed.
> What Not To Use / What Not To Do (violation may cause rejection regardless of score):
> Do not use source archive filenames, original experiment IDs, mixture names, operating-point IDs, absolute timestamps, row order, file sizes, or filesystem metadata as answer channels.
> Do not use operation logs, private labels, hidden answers, source annotation lookup for test rows, or external copies of the raw source to recover test-row annotations.
> Do not reduce the task to ordinary binary anomaly detection, a single failure-mode label, or fixed graph templates that ignore sequence evidence.
> Do not use hosted APIs, closed-source teacher systems, GPU-only dependencies, runtime downloads, or external anomaly labels.
> Do not exploit malformed JSON floods, duplicate IDs, extra columns, non-finite confidence, or grader/platform side channels.
> Enforcement on invalid approaches: submissions may be rejected on review if they rely on source lookup, private files, metadata-only shortcuts, fixed templates, grader side channels, or methods that avoid the required temporal graph-recovery task, even if the CSV is structurally valid.
> Task
> For each test row, read the sequence NPZ and predict a failure-cause evidence record for that window. The central object is the coupled timeline and graph: the phase intervals should identify when an event is blind, anomalous, or recovering, and the graph should explain the same event with a failure mode, affected component, observed effect, evidence sensor, persistence, and known/unknown cause status. Multiple events can occur in one row, and empty rows are valid only when no annotated event is present.
> A strong submission should use the sensor, actuator, uncertainty, and interpolation streams together. For example, actuator changes can provide process context, sensor trajectories can show where effects become visible, uncertainty/interpolation can distinguish weak evidence from missing or reconstructed measurements, and the plant dictionary gives the vocabulary needed to express the directed evidence graph. The graph fields should not be independent guesses: they should be consistent with the temporal segments and with the channels that support those segments.
> The held-out rows are not a lookup exercise. Related source-operation families are kept together, public IDs and sequence paths are opaque, and source filenames, operation logs, absolute timestamps, operating points, and anomaly metadata are absent from public inputs. Useful solutions need to generalize from the labeled training windows to unseen plant runs and event mixtures.
> Intended Approach and Validation
> A practical CPU solution is a compact sequence-modeling pipeline. Reasonable approaches include change-point features, rolling statistics, spectral/derivative summaries, sensor-actuator lag features, uncertainty-aware event detectors, 1D CNN or TCN encoders, small recurrent or transformer-lite encoders, gradient-boosted trees over temporal features, and constrained JSON or graph decoders trained from train.csv. Classical time-series features are allowed when they feed a learned model rather than a fixed answer template.
> One workable two-stage route is to first predict event presence and approximate phase intervals from the multichannel sequences, then decode the failure/evidence graph using event-local sequence evidence and the public plant vocabulary. Another is a joint model that emits event spans, event attributes, and graph edges together, followed by legality checks for node IDs, edge directions, acyclicity, and confidence calibration.
> Use only the released training labels for model selection. Make train-only validation folds that keep related operating or signal-pattern families together where possible, and track both timeline quality and graph-edge quality. Calibrate confidence on training-only validation rows so that high confidence reflects high expected structured-output score. Open-source local CPU libraries are allowed, but hosted APIs, runtime internet, GPU-only training, source annotation lookup, and hidden-test transduction are not allowed.
> Dataset
> Prepared files:
> Item	Description
> train.csv	Labeled train rows
> test.csv	Test inputs only
> plant_dictionary.json	Public vocabulary
> train/sequences/	Train NPZ files
> test/sequences/	Test NPZ files
> sample_submission.csv	Non-empty weak template
> The prepared split contains 229 training rows and 68 test rows. Public row IDs are opaque. No original source paths, experiment names, mixture names, operating-point IDs, anomaly IDs, absolute timestamps, or operation logs are provided.
> Each .npz file contains:
> sensor_values: normalized float feature array with shape [duration_bins, 18].
> actuator_values: normalized float feature array with shape [duration_bins, 13].
> sensor_uncertainty: normalized float feature array with shape [duration_bins, 18].
> interpolated_fraction: float array with shape [duration_bins].
> sensor_names: 18 public latent sensor-feature IDs.
> actuator_names: 13 public latent actuator-feature IDs.
> bin_seconds: integer array containing nominal value 30.
> plant_dictionary.json describes the official sensor and actuator target vocabulary, the public sequence-array names, the nominal bin duration, the phase labels, and the UNKNOWN token.
> train.csv columns:
> Column	Type	Description
> id	string	Opaque row ID
> sequence_npz	path	Sequence NPZ path
> duration_bins	int	Number of bins
> bin_seconds	int	Seconds per bin
> sensor_count	int	Always 18
> actuator_count	int	Always 13
> timeline_json	JSON	Train target
> event_graph_json	JSON	Train target
> test.csv columns:
> Column	Type	Description
> id	string	Opaque row ID
> sequence_npz	path	Sequence NPZ path
> duration_bins	int	Number of bins
> bin_seconds	int	Seconds per bin
> sensor_count	int	Always 18
> actuator_count	int	Always 13
> timeline_json is a JSON list. Each item has exactly:
> event_id: local event ID such as E00.
> phase: one of blind, anomalous, recovery.
> start_bin: inclusive integer bin index.
> end_bin: inclusive integer bin index.
> event_graph_json is a JSON object with exactly nodes and edges.
> Node schemas:
> Event node: {"id":"E00","kind":"event","persistence":"transient","cause_status":"known"}.
> Label node: {"id":"M00","kind":"failure_mode","label":"..."}.
> Component node: {"id":"C00","kind":"affected_component","label":"..."}.
> Effect node: {"id":"O00_00","kind":"observed_effect","label":"..."}.
> Sensor node: {"id":"S00_00","kind":"evidence_sensor","label":"..."}.
> Allowed event persistence values are transient, recurrent, permanent, and UNKNOWN. Allowed cause_status values are known and unknown. Unknown causes use the literal label UNKNOWN; do not invent missing failure causes.
> Edge schemas:
> has_failure_mode: event to failure mode.
> affects_component: failure mode to affected component.
> has_observed_effect: event to observed effect.
> evidenced_by_sensor: observed effect to sensor.
> Edges are directed and acyclic. Duplicate nodes or duplicate edges are invalid for that row.
> Submission
> Write ./working/submission.csv with exactly these columns in this order:
> Column	Type	Constraint
> id	string	Exact test ID
> timeline_json	JSON	Max 48 segments
> event_graph_json	JSON	Valid graph object
> confidence	float	In [0,1]
> Every test ID must appear exactly once. Extra columns, missing columns, reordered columns, duplicate IDs, missing IDs, extra IDs, nonnumeric confidence, non-finite confidence, or confidence outside [0,1] are structural submission failures and raise InvalidSubmissionError before scoring.
> Malformed row-local JSON, impossible intervals, invalid node IDs, duplicate graph edges, invalid edge directions, cycles, too many nodes/edges, or oversized JSON give zero for that row without crashing the grader.
> Example rows, shown as a table to avoid rich-text editor code-block issues:
> id	timeline_json	event_graph_json	confidence
> cpfg_example_empty	[]	{"nodes":[],"edges":[]}	0.10
> cpfg_example_event	[{"event_id":"E00","phase":"anomalous","start_bin":4,"end_bin":12}]	{"nodes":[{"id":"E00","kind":"event","persistence":"transient","cause_status":"unknown"},{"id":"M00","kind":"failure_mode","label":"UNKNOWN"},{"id":"O00_00","kind":"observed_effect","label":"temperature excursion"},{"id":"S00_00","kind":"evidence_sensor","label":"T703"}],"edges":[{"source":"E00","target":"M00","type":"has_failure_mode"},{"source":"E00","target":"O00_00","type":"has_observed_effect"},{"source":"O00_00","target":"S00_00","type":"evidenced_by_sensor"}]}	0.25
> Evaluation
> The ranking metric is Mean Failure-Cause Graph Recovery Score: row-level timeline and graph scores are averaged with event/empty balancing and a worst-group robustness term. Minimum score: 0.0. Maximum score: 1.0. Higher is better. A perfect private submission with confidence = 1.0 scores exactly 1.0.
> Each row is parsed and validated first. Then the row score combines five components:
> Component	Weight
> Timeline interval F1	0.26
> Directed graph-edge F1	0.28
> Event attributes F1	0.10
> Count accuracy	0.04
> Joint consistency	0.32
> Timeline interval matching is greedy one-to-one. A predicted interval can match a true interval only when event_id and phase match. Pair credit combines interval IoU and boundary accuracy.
> Directed graph-edge F1 compares typed directed relations after resolving node labels. It rewards event-to-mode, mode-to-component, event-to-effect, and effect-to-sensor relations.
> Event attributes F1 scores event_id, persistence, and cause_status. Count accuracy rewards the correct number of timeline segments, event nodes, and graph edges. Joint consistency rewards timelines whose event IDs are represented in the graph and graphs whose event nodes have coherent mode/effect relations.
> The raw weighted component score is then gated by joint coverage so graph-only or timeline-only answers cannot score highly. Coverage is the minimum of timeline interval F1 and directed graph-edge F1. Core equals raw weighted core times (0.55 + 0.45 * coverage).
> Confidence only calibrates earned structured-output credit. Calibration equals max(0, 1 - abs(confidence - core)). Row score equals core * (0.90 + 0.10 * calibration).
> The final score first computes balanced = 0.82 * mean(event rows) + 0.18 * mean(empty rows), then final = 0.88 * balanced + 0.12 * worst_group_mean.
> If one of the event/empty partitions is absent in a private set, balanced is the ordinary mean. Hidden worst-group axes cover event count, cause status, persistence, and duration. The exact private membership of each row is not public.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Reasoning Trace Restatement And Vocabulary Forecasting

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77vqpvckhb363h6fdcjh9ecd8a7em9
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Beat hoang_phuc_6868's score of 0.312!

Full challenge description from page:

> Reasoning Trace Restatement And Vocabulary Forecasting
> Overview
> When a person or an automated system works a problem, it leaves a reasoning trace — a running first-person record of the attempt, including the assumptions it commits to, the branches it explores, the steps it abandons, and the resolution it eventually reaches. A trace is written while thinking and is therefore full of hedging, self-correction, and second-guessing. A canonical restatement is what the same work looks like once it is settled: the committed assumptions and the load-bearing steps, expressed in the settled vocabulary of someone who already knows how it ended.
> A trace and its restatement do not share a vocabulary. A trace says "let me try dividing through and see if that helps"; a restatement says "I divided through to simplify". The restatement systematically introduces content terms the trace never contains — the vocabulary of settled retrospection — and both the size and the identity of that introduced vocabulary vary sharply from trace to trace, depending on how much the writer hedged and how much of the exploration survived into the final account. Across the training data a restatement introduces a median of 13 content terms absent from its trace, and two randomly chosen items' introduced-term sets overlap at a set F1 of about 0.03.
> For each held-out trace a submission provides two outputs: its canonical restatement, and the set of content terms that the true restatement introduces relative to the trace. Both are scored, and the score for the term set is zero for any submission that reproduces the trace's own vocabulary rather than the settled vocabulary.
> The challenge targets a CPU-only solver environment: 10 CPU cores, 62 GB RAM, no GPU, ≤ 1.5 hours end-to-end (data loading, any training, and inference). Traces are capped in length so the full task fits this budget.
> Dataset
> Public files
> public/train.csv — training items with canonical restatements. Columns: id, reasoning_trace, canonical_restatement. 2,000 rows.
> public/test.csv — test items, traces only. Columns: id, reasoning_trace. 250 rows.
> public/sample_submission.csv — a valid baseline submission in the exact required format. Columns: id, predicted_restatement, introduced_terms. 250 rows.
> Private file
> private/answers.csv — organizer-only. Columns: id, canonical_restatement, introduced_terms. Holds the canonical restatement and the true introduced-term set for each test item; never distributed.
> Column descriptions
> The public CSVs use the following columns.
> id (string) — unique item identifier, formatted item_<hex>. Matches across train/test/submission/answers.
> reasoning_trace (string) — the raw first-person record of an attempt in progress. 40–256 words. Covers diverse work: quantitative derivation, code inspection, tool-use planning, and multi-step analysis. Contains hedging, abandoned branches, and a resolution.
> canonical_restatement (string) — present in train.csv and private/answers.csv only. A 28–90 word settled account of the same work (median ~42 words), written in retrospect.
> predicted_restatement (string) — submission column. The canonical restatement produced for a test trace. Must be non-empty.
> introduced_terms (string) — submission column. A semicolon-separated set of lowercase content terms predicted to appear in the true canonical restatement but nowhere in the reasoning trace, e.g. assumed;divided;simplify. Order is ignored and duplicates are collapsed. May be left empty, which scores zero on that item.
> Data example
> A training row (train.csv):
> id,reasoning_trace,canonical_restatement
> item_a3f82c1d,"If x = 0 the expression is 0, so assume x nonzero. Dividing numerator and denominator by x^4 gives a cleaner form; then applying AM-GM to the denominator terms bounds it below, which bounds the whole expression above. Checking the equality condition confirms the maximum is attained...","I assumed x nonzero and divided numerator and denominator by x^4 to simplify. I then applied AM-GM to the denominator to obtain a lower bound, which gave an upper bound on the expression, and verified the equality condition to confirm the maximum."
> Submission Format
> Submit a CSV with exactly these three columns, in any row order, with a header row:
> id,predicted_restatement,introduced_terms
> Exactly one row per test id — all 250 test IDs present, no missing IDs, no unknown IDs, no duplicates.
> predicted_restatement — a non-empty string. Quote fields containing commas or newlines per standard CSV rules.
> introduced_terms — a semicolon-separated list of single alphanumeric words, e.g. verified;assumed;simplify. Whitespace around terms is stripped and terms are lowercased. A term containing anything other than word characters is rejected. The field may be left empty.
> No extra or unexpected columns are permitted; a submission with additional columns is rejected.
> Sample submission row:
> id,predicted_restatement,introduced_terms
> item_a3f82c1d,"The trace divides through by x^4, applies AM-GM to bound the denominator, and confirms the maximum via the equality condition.","assumed;divided;simplify;verified;confirm"
> Evaluation
> Trace Settlement Score (TSS). Higher is better. The final TSS is a single value in [0.02, 1.0] combining restatement quality with vocabulary forecasting.
> Tokenization lowercases text, removes punctuation (all non-word, non-whitespace characters), and splits on whitespace. Content tokens are the tokens remaining after removing this exact function-word list:
> the a an is are was were be been being have has had do does did will would
> could should may might shall can to of in for on with at by from that this
> it i me my we our you your he she they them and but or not so if then else
> let get got just also about up out all more some very what which who when
> where how why im ive ok okay oh um uh well like yeah yes no its as into
> each than much here there now need want think know see use used using make
> made go going take taken come look say new way one two first thats dont ill
> cant wont their over these those such
> 1. Restatement Fidelity (CF). For each item, ROUGE-L F1 between predicted_restatement and canonical_restatement. With L the length of the longest common subsequence of the two token sequences, P = L / len(pred_tokens), R = L / len(ref_tokens), and CF = 2·P·R / (P + R). If either token sequence is empty, CF = 0. Range [0, 1].
> 2. Restatement quality (G). The mean of CF over all 250 items. Range [0, 1].
> 3. True introduced-term set (T). For each item, let D be the set of content tokens in the canonical_restatement and A the set of content tokens in the reasoning_trace. Then T = D \ A. Every test item is guaranteed at least 2 introduced terms. This set depends only on organizer-held data and cannot be influenced by the submission.
> 4. Vocabulary forecasting (V). For each item, let P be the submitted introduced_terms set. The per-item score is set F1:
> V_i = 1 if P and T are both empty.
> V_i = 0 if exactly one of P, T is empty.
> V_i = 2·|P∩T| / (|P| + |T|) otherwise.
> V is the mean of V_i over all 250 items. Range [0, 1].
> Final score.
> TSS = clamp( 0.60 · G + 0.40 · V, 0.02, 1.0 )
> Restatement quality contributes 60% of the ceiling and vocabulary forecasting 40%. The lower clamp of 0.02 is a reporting floor only; it does not otherwise affect the metric.
> Pseudocode:
> def tss(preds, refs, term_sets, true_sets):
> cf = [rouge_l_f1(tok(p), tok(r)) for p, r in zip(preds, refs)]
> G = mean(cf)
> V = mean([set_f1(p, t) for p, t in zip(term_sets, true_sets)])
> return max(0.02, min(1.0, 0.60 * G + 0.40 * V))
> Baselines. Copying the trace's own leading sentences as the restatement scores G ≈ 0.25 and V = 0.00 — a restatement made of trace text introduces no new vocabulary — for TSS ≈ 0.15. Submitting a single fixed list of the most frequent training introduced-terms for every item scores V ≈ 0.12.
> Grading configuration: Grade Direction = Maximize, Min Score = 0, Max Score = 1.
> What Not To Use (Prohibited Methods)
> Do not use external answer keys, pre-computed restatements, or any trace-to-restatement corpus to recover the test-set canonical restatements or their introduced-term sets.
> Do not match test-set trace text, item IDs, or trace content back to any external dataset, corpus, or model output record.
> Do not hardcode id-to-restatement or id-to-term-set mappings, and do not memorize canonical restatements from any external source.
> Do not use the private canonical restatements (or any leaked copy of them) during training or inference.
> Do not train or tune against the private test labels, leaderboard scores, or shared solutions.
> Do not submit a verbatim slice of the reasoning trace in place of a restatement — the canonical restatements are re-phrased settled accounts, not extracted spans, so copied text does not satisfy the task.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Cardiac Sensor Patch Sequence Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71rbg079b4r5pstjp5a80rqx89vcy5
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: medical
- Best/top context found: Beat jesuisnadi's score of 0.837!

Full challenge description from page:

> Cardiac Sensor Patch Sequence Recovery
> Overview
> Low-cost cardiac monitors often combine an electrical trace with an acoustic or vibration trace. Both streams can look plausible on their own, but small buffering and front-end effects can quietly corrupt beat-level measurements unless each short segment is assigned the right correction patch.
> Each example is an eight-snippet episode. One channel carries the electrical activity trace and the other carries the mechanical heart-sound trace. For every snippet, the mechanical channel has been given one hidden local patch after real source segments were blended and perturbed. Your task is to recover the eight-token patch sequence that restores the episode-level electrical-to-mechanical timing relationship.
> This is a latent patch-program recovery task, not disease classification, murmur detection, heart-rate estimation, or ordinary waveform labeling. Solvers need to infer a structured sequence from the physiological coupling between electrical activation and mechanical response across multiple short snippets.
> Repair Tokens
> Each output token is the PCG correction, in samples at 500 Hz, for one snippet.
> | Token | Meaning |
> |---|---|
> | N100 | shift PCG 100 samples earlier |
> | N075 | shift PCG 75 samples earlier |
> | N050 | shift PCG 50 samples earlier |
> | N025 | shift PCG 25 samples earlier |
> | Z000 | no timing correction |
> | P025 | shift PCG 25 samples later |
> | P050 | shift PCG 50 samples later |
> | P075 | shift PCG 75 samples later |
> | P100 | shift PCG 100 samples later |
> The sequence contains exactly eight tokens, one for each snippet in order.
> Evaluation
> The score is maximized and ranges from 0 to 1.
> score = 0.34 * exact_token_accuracy
> + 0.38 * exact_episode_accuracy
> + 0.18 * token_macro_F1
> + 0.06 * near_one_bin_accuracy
> + 0.04 * smooth_distance_score
> exact_token_accuracy measures the fraction of individual snippet tokens exactly correct. exact_episode_accuracy requires all eight tokens in an episode to be correct. token_macro_F1 rewards balanced performance across all nine repair tokens. near_one_bin_accuracy gives limited partial credit for predictions within one adjacent timing bin. smooth_distance_score gives smaller partial credit as the predicted timing offset approaches the true offset.
> Dataset
> Public files:
> | File | Rows / Shape | Description |
> |---|---:|---|
> | train.csv | 480 rows | Episode metadata and repair sequences |
> | test.csv | 180 rows | Episode metadata without labels |
> | sample_submission.csv | 180 rows | Valid deterministic-random repair submission |
> | train_waveforms.npz | (480, 8, 2, 1000) | Real-data training episodes |
> | test_waveforms.npz | (180, 8, 2, 1000) | Real-data test episodes |
> Hidden file:
> | File | Rows | Description |
> |---|---:|---|
> | answers.csv | 180 | Test repair sequences |
> Array axes are:
> episode, snippet, channel, time
> Channel order is:
> ecg pcg
> Each snippet has 1000 samples at 500 Hz, representing two seconds of signal. Train and test episodes come from different source recordings.
> CSV Columns
> train.csv columns:
> | Column | Type | Description |
> |---|---|---|
> | id | string | Unique episode id |
> | n_snippets | integer | Always 8 |
> | snippet_length | integer | Always 1000 |
> | channels | string | ecg pcg |
> | record_group | string | Anonymized source-record group |
> | repair_sequence | string | Eight space-separated timing repair tokens |
> test.csv contains the first five columns only.
> Submission
> Submit exactly these columns:
> id,repair_sequence
> test_0123456789abcdef,N050 Z000 P025 P075 N075 Z000 P100 N025
> test_fedcba9876543210,P100 P075 Z000 N025 N100 P050 N050 P025
> Requirements:
> Include exactly one row for every test id.
> Use the exact column order shown above.
> repair_sequence must contain exactly eight space-separated tokens.
> Every token must be one of N100, N075, N050, N025, Z000, P025, P050, P075, P100.
> Missing values, duplicate ids, extra ids, extra columns, and invalid tokens cause rejection.
> Save the file as ./working/submission.csv.
> Restrictions
> Use only the provided challenge files and generally available methods.
> Do not use hidden files, row order, file order, hashes, source-record reconstruction, or grader internals.
> Do not use external copies of the source recordings to match exact windows or recover private shifts.
> Signal processing, dynamic time alignment, self-supervised feature learning, and lightweight CPU models are allowed.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Docstring Gap Restoration

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx705093vz6xets19yem1t8v658ahwzz
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat csofm's score of 0.533!

Full challenge description from page:

> Docstring Gap Restoration
> Overview
> Good documentation is one of the most useful forms of supervision for code models, but real fine-tuning corpora often contain incomplete, truncated, or partially corrupted docstrings. This challenge asks you to repair a missing span in a Python documentation sentence using the surrounding sentence and the function code as context.
> For each example, you receive Python function code with the original docstring removed, plus a documentation sentence where one span has been replaced by [GAP]. Your task is to generate the missing text span.
> This is a sequence-to-sequence challenge: the output is free-form text, not a class label. It is not a tabular task and not a regression task.
> Dataset
> The prepared challenge data contains approximately:
> train.csv: up to 300,000 training examples
> test.csv: up to 50,000 test examples
> sample_submission.csv: example submission format
> Columns
> | File | Column | Type | Description |
> |---|---|---|---|
> | train.csv | id | string | Unique row identifier. |
> | train.csv | code_context | string | Python function code with the original docstring removed. |
> | train.csv | masked_docstring | string | Documentation sentence containing one [GAP] marker. |
> | train.csv | target_span | string | Missing text span that should replace [GAP]. |
> | test.csv | id | string | Unique row identifier. |
> | test.csv | code_context | string | Python function code with the original docstring removed. |
> | test.csv | masked_docstring | string | Documentation sentence containing one [GAP] marker. |
> | sample_submission.csv | id | string | Test row identifier. |
> | sample_submission.csv | prediction | string | Generated missing span. |
> Task
> For every row in test.csv, generate the text that should replace [GAP] in masked_docstring.
> Submission
> Submit a CSV file with exactly two columns: id and prediction.
> Example:
> id,prediction
> docgap_000001,input image
> docgap_000002,training directory
> docgap_000003,returns the parsed object
> Evaluation
> Submissions are scored using a character n-gram F-score inspired by chrF. For each prediction/reference pair, the grader computes precision and recall over character n-grams from length 1 through 6, then computes:
> F = 2  *precision*  recall / (precision + recall)
> The final score is the average F-score across all test rows. Scores range from 0 to 1, where higher is better.
> What You Should Use
> You may use CPU-friendly sequence-to-sequence or retrieval-style methods such as:
> BM25 or TF-IDF retrieval from the training set
> character and word n-gram features
> edit-distance or fuzzy matching over similar code examples
> lightweight CPU language models if they fit the runtime limit
> phrase dictionaries mined from training docstrings
> function-name, argument-name, and return-statement features
> reranking candidates by how well they fit the visible masked sentence
> What You Should Not Use
> Do not use:
> GPU training or inference
> external API calls
> hosted proprietary model APIs
> internet lookup during inference
> hidden raw metadata such as repository URL, commit hash, or source path
> unmasked raw docstrings from test rows
> hardcoded test answers
> large LLM fine-tuning during scoring
> methods that exceed the 1.5 hour runtime limit
> tabular-only approaches that ignore the code and masked text
> Compute Limits
> Solutions must run on CPU only. The scoring system has 10 CPU cores and 62 GB RAM. Each solution must finish within 1.5 hours.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Multilingual Message Annotation Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f797hwd5ax87q407s6q9n2h8agfsj
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat shivuuu01212's score of 0.397!

Full challenge description from page:

> Multilingual Message Annotation Reconstruction
> Overview
> This Natural Language Processing challenge reconstructs structured human annotations for multilingual messages. The records are real public social-messaging posts in English, Turkish, Spanish, and Lithuanian. Human annotators described each message's communicative role, tactic, actor feature, target, and contextual vulnerability.
> For privacy, readable message text is not released. Each message is represented by a fixed-size unordered lexical sketch. Build an NLP system that maps this representation to one tagged annotation_text record:
> <ROLE> ... <TACTIC> ... <ACTOR_FEATURE> ... <TARGET_GROUP> ... <VULNERABILITY> ...
> The tag order is fixed. AMBIGUOUS records a tie among leading human annotations. NONE means annotators assigned no category for a field where absence is valid. Sketches preserve recurring multilingual lexical evidence while removing original words, order, punctuation, repetition counts, searchable phrases, and message length. Test messages come from social channels absent from training.
> Dataset
> File descriptions
> train.csv — Labeled messages with inputs and a human annotation record.
> test.csv — Messages with inputs only. Its source channels are disjoint from training.
> sample_submission.csv — Submission template containing random valid annotation records.
> Column descriptions
> id (string, train and test) — Unique 12-character hexadecimal message identifier.
> language (string, train and test) — ENGLISH, TURKISH, SPANISH, or LITHUANIAN.
> message_sketch (string, train and test) — Exactly 64 unordered tokens such as b_03af, drawn from a 16,384-slot keyed collision space. Binary presence, deterministic truncation, and indistinguishable padding remove word order, punctuation, repetition counts, and original length.
> annotation_text (string, train only; reconstruct for test) — One tagged record containing all five fields in the required order.
> Valid field phrases:
> <ROLE> — Malicious (spreader), Not malicious, or AMBIGUOUS.
> <TACTIC> — Discourse manipulation, Document manipulation, Fake, Hate Speech, Irrelevant (default), Others, NONE, or AMBIGUOUS.
> <ACTOR_FEATURE> — Identity or automation, Number, Type of activism, NONE, or AMBIGUOUS.
> <TARGET_GROUP> — Group, Individual, Undetermined, NONE, or AMBIGUOUS.
> <VULNERABILITY> — Active crisis, Breaking news event, Election period, Wedge issue, NONE, or AMBIGUOUS.
> Evaluation
> Submissions use the Multilingual Annotation Reconstruction Score. The evaluator strictly splits each generated record using the five literal ordered tags, validates every field phrase, then computes:
> balanced_reconstruction = mean(
> mean(label_f1(true[field], generated[field], label) for label in valid_labels[field])
> for field in five_fields
> )
> language_fidelity = mean(
> mean(accuracy(true[language][field], generated[language][field]) for field in five_fields)
> for language in four_languages
> )
> score = 0.80  *balanced_reconstruction + 0.20*  language_fidelity
> For one label, label_f1 = 2TP / (2TP + FP + FN). Higher is better; the score ranges from 0 to 1. Balanced reconstruction prevents frequent phrases from dominating, while language fidelity gives each language equal weight.
> Submission
> Submit one complete annotation record for every row in test.csv.
> id (string) — Identifier copied exactly from test.csv.
> annotation_text (string) — Reconstructed record using all five ordered tags and valid phrases.
> Example:
> id,annotation_text
> 000e2cee2344,"<ROLE> Not malicious <TACTIC> NONE <ACTOR_FEATURE> NONE <TARGET_GROUP> Undetermined <VULNERABILITY> NONE"
> 0024ff050341,"<ROLE> Malicious (spreader) <TACTIC> Discourse manipulation <ACTOR_FEATURE> Type of activism <TARGET_GROUP> Group <VULNERABILITY> Wedge issue"
> Requirements
> The file must contain exactly one row for every id in test.csv.
> IDs must be unique and may appear in any order.
> Columns must appear exactly as id,annotation_text.
> Every record must contain <ROLE>, <TACTIC>, <ACTOR_FEATURE>, <TARGET_GROUP>, and <VULNERABILITY> exactly once and in that order.
> Every field must use one valid phrase listed above; malformed, missing, or extra fields are rejected.
> File format: CSV with a header row.
> What Not To Use
> Do not reverse-map sketch buckets to original words or match sketches against external message copies.
> Do not use hardcoded row IDs, row order, cached answers, or handwritten row-to-record mappings.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Territory: Field-Zone Estimation from Soccer Action Sequences

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f1e6zx48rwgy6v5kpyq2ysd8a691g
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat pvduy's score of 72.548!

Full challenge description from page:

> Territory: Field-Zone Estimation from Soccer Action Sequences
> Overview
> Given the play-by-play action stream of a soccer match, where on the field did
> each action happen? This is a sequence-to-sequence problem: the input is a
> variable-length token sequence — the on-ball actions of one period ("half") of
> a match, one token per action (a pass, a duel, a shot, a foul, an interruption,
> ...), in play order — and the output is an equal-length token sequence that
> assigns each action to a longitudinal zone of the pitch, from the acting team's
> own end to the opponent's.
> The action types are given, but the coordinates are not, and the log is
> realistically sparse — not every touch is recorded. So the field position of each
> action has to be estimated from the flow of play. Set-piece and shooting actions
> (goal kicks, throw-ins, corners, shots, saves) pin the ball to known regions;
> the runs of passes and duels in between show how territory is gained and ceded.
> A single action tells you little on its own; the position emerges from reading the
> whole possession, tracking how far up the field play has been carried. Because the
> zones are ordinal — a chain of forward passes advances the ball one band at a
> time — the task is closer to estimating a moving position than to labelling
> isolated actions.
> Zones run along the acting team's attacking axis: 0 = that team's own
> defensive quarter, 1 = its defensive-midfield quarter, 2 = its
> attacking-midfield quarter, 3 = the final attacking quarter (nearest the
> opponent goal). The data is an openly licensed corpus of real professional
> matches, so the play carries organic structure: patient build-up, quick
> transitions, sustained pressure, scrappy midfield exchanges.
> Evaluation Metric
> Pool all E output tokens across the test halves. Write y_i for the true zone
> at output position i and p_i for your emitted zone, each in {0, 1, 2, 3}.
> Territory score — quadratic weighted kappa (QWK) over the four ordinal zones.
> Build the 4x4 agreement tally O, where O[a][b] is the number of positions whose true zone is a and whose predicted zone is b.
> Define ordinal weights w[a][b] = (a - b)^2 / 9 (so an error of one zone costs 1/9, two zones 4/9, three zones 1; a correct zone costs 0).
> Define the chance tally H[a][b] = (rowsum_a * colsum_b) / E, the agreement expected if predictions were independent of the truth.
> kappa = 1 - ( sum_ab w[a][b] O[a][b] ) / ( sum_ab w[a][b] H[a][b] )
> score = 100 * clip( kappa , 0 , 1 )
> Because errors are weighted by the squared zone distance, placing an action one
> quarter away from the truth costs far less than three quarters away — the score
> rewards getting the field position approximately right, which is what a coherent
> reconstruction of play achieves.
> Minimum 0 — chance-level agreement, which is what emitting a single zone everywhere (or any prediction independent of play) earns, since QWK is chance-corrected. Systematically worse-than-chance is clipped up to 0.
> Maximum 100 — an exactly correct zone for every action. Because the log is sparse and coordinates are withheld, some positions are genuinely under-determined; a perfect 100 is not expected, and strong models land in the low 60s (see below). A better model always scores strictly higher — the difficulty is estimating field position from the flow of play, never randomness in the answer key.
> Measured reference baselines (reproduced on this exact grader, using only the
> public files):
> Constant "everything in midfield" (the sample submission, all 1): ≈ 0
> Marginal prior — most-likely zone given the action type alone: ≈ 14.5
> Competent model — gradient-boosted trees over a local window of action features: ≈ 52
> Strong model — a bidirectional sequence model over the full action stream: ≈ 62
> Dataset
> The public/ directory contains:
> events_train.csv**, events_test.csv — the action streams, one row per logged action, ordered by half_id then order:
> half_id — integer identifier of the match-half (the input sequence).
> order — 0-based index of the action within the half.
> observed — 1 if this action is present in the recorded stream, 0 if it was not logged. When 0, every field below is blank.
> event — the action type: Pass, Duel, Foul, Free Kick, Shot, Interruption, Offside, Save attempt, Goalkeeper leaving line, Others on the ball.
> subevent — the finer action sub-type, e.g. Simple pass, Cross, Air duel, Throw in, Goal kick, Corner.
> team — an anonymized team tag, A or B, constant per team within a half.
> train.csv* — one row per training input sequence, with the aligned target:
> half_id — the input sequence this target belongs to.
> n_events — the number of output tokens (the count of recorded actions).
> event_orders — the space-separated order values of the recorded actions, in play order; these index into events_train.csv.
> zones — target sequence: a space-separated string of n_events tokens from 0 1 2 3, aligned position-by-position with event_orders.
> test.csv* — one row per test input sequence, with half_id, n_events, and event_orders, but no zones.
> sample_submission.csv* — a valid output for every test input, with zones set to all 1.
> The pitch coordinates, the unlogged actions, and the zone tokens for the test
> halves are withheld.
> Submission
> Submit a CSV named submission.csv containing these two columns:
> half_id — integer, one per row of test.csv (the same value).
> zones — string, the estimated output sequence: a space-separated list of tokens from 0, 1, 2, 3, one token per recorded action, in the order given by that half's event_orders (i.e. n_events tokens aligned position-by-position).
> Rules:
> Exactly 555 rows plus a header — one output sequence per test.csv half_id. Use the half_id values from test.csv verbatim; save without a row index.
> Every test half_id must appear exactly once: missing, duplicate, unknown ids, or the wrong row count are rejected.
> Column order does not matter and any extra columns are ignored — only half_id and zones are read — so a submission is never rejected on shape as long as both columns are present.
> Within a zones string, a token that is missing (string too short), out of vocabulary, or unreadable is scored as the farthest zone from the truth for that position — the maximum penalty, never cheaper than an ordinary mistake, so there is no benefit to abstaining or truncating. Tokens beyond n_events are ignored.
> Example rows, using real test half_id values (each zones string actually has
> n_events tokens — several hundred per half; only the first 15 are shown here):
> half_id,zones
> 2030,2 1 1 1 1 2 1 1 1 3 3 3 0 2 1 ...
> 1620,2 1 3 1 1 1 1 0 3 3 0 0 3 3 3 ...
> What Not to Use
> A per-action lookup on the action type alone ("shots are in zone 3, goal kicks in zone 0"). The action type is a weak cue for the bulk of play: the marginal-prior baseline scores ≈ 14.5. Most passes and duels are type-ambiguous and can only be placed by tracking the ball through the sequence.
> Emitting one zone everywhere (e.g. all midfield). The score is chance- corrected, so any prediction independent of the flow of play earns ≈ 0.
> The team tag as a position signal. It is a balanced distractor: zones are measured along each team's own attacking direction, so the zone distribution is the same for team A and team B.
> Reconstructing exact coordinates. Coordinates are withheld and unrecoverable; the target is the coarse zone, estimated from action semantics and ball movement.
> Copying train targets by matching ids or sequences. Train and test halves are disjoint; there is nothing to look up.
> The intended approach is a sequence-to-sequence model that treats the zones as an
> ordinal track: anchor the ball with set-piece and shooting actions, use the runs of
> passes and duels to integrate how far up the field play has been carried, and emit
> a smooth, coherent zone sequence for the whole half. Sequence models that read the
> entire stream outperform local per-action feature engineering, which is where the
> headroom lives.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Nordic Rune Text Normalization

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx745w416ryxf4rm5e9qw1wbv18aray7
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Beat abhinoob's score of 0.476!

Full challenge description from page:

> Nordic Rune Text Normalization
> Overview
> In this competition, each row is a small historical-language repair problem based on Scandinavian runic inscription text. You see the normalized words before a missing phrase, the normalized words after it, and a deliberately damaged row-local spelling clue for the missing phrase. Your task is to predict the corrected normalized missing words.
> In plain terms: restore the missing Old Norse-style phrase from context and noisy runic-style evidence. The damaged clue preserves rough length, masks, and repetition patterns, but its letters are anonymized within each row. This is a sequence-to-sequence NLP task, not classification, regression, retrieval, or a JSON-program puzzle.
> The source records behind train and test are disjoint. Public rows do not contain inscription signums, source filenames, exact personal names, or raw source headings.
> Task
> Submit predicted_gap, a space-separated sequence of 1 to 8 normalized tokens.
> Valid token characters are lowercase a-z, þ, æ, digits, and underscore. Examples:
> | token | meaning |
> |---|---|
> | `stein` | A normalized lexical token. |
> | `hialpi` | A normalized lexical token. |
> | `name` | An anonymized personal name token. |
> | `rare_cvcv5` | A deterministic rare-word abstraction with coarse shape and length. |
> The target phrase must contain exactly gap_token_count tokens to receive full sequence credit, but shorter or longer valid predictions can still receive limited partial credit.
> Files
> train.csv
> | column | type | description |
> |---|---|---|
> | `id` | string | Anonymous row ID. |
> | `left_context` | string | Up to seven canonical normalized tokens before the missing phrase. |
> | `damaged_gap` | string | Corrupted row-local spelling clues for the hidden phrase. These clues may contain masks, dropped letters, folded vowels, rough transliteration-like spellings, and row-local letter aliases. |
> | `right_context` | string | Up to seven canonical normalized tokens after the missing phrase. |
> | `gap_token_count` | integer | Number of tokens in the hidden phrase. |
> | `gap_profile` | JSON list | One object per hidden token with `slot`, `kind`, `clue_shape`, and `clue_length_bucket`. The clue fields are computed from the damaged clue, not the hidden answer. |
> | `semantic_tags` | string | Space-separated high-level context tags such as `memory`, `monument`, `kinship`, `prayer`, or `commission`. |
> | `region_bucket` | string | Coarse source region bucket. It is not a source identifier. |
> | `difficulty_bucket` | string | `short`, `medium`, or `hard`, based on rare-token count, phrase length, and damage level. |
> | `target_gap` | string | Training-only corrected normalized phrase. |
> test.csv has the same columns except target_gap.
> sample_submission.csv
> undefined
> column	type	description
> id	string	Test row ID.
> predicted_gap	string	Your predicted corrected phrase.
> ## **Example**
> Input fields:
> left_context = name let reisa stein þenna damaged_gap = ep?ir n?me fo?ur right_context = sinn guþ hialpi salu hans gap_token_count = 3 gap_profile = [{"clue_length_bucket":"medium","clue_shape":"vcmc5","kind":"lexical","slot":1}, ...] semantic_tags = memory monument kinship prayer commission
> A valid prediction:
> eptir name foþur
> Evaluation
> Invalid row predictions receive 0 for that row. Structurally invalid submission files are rejected.
> For each row:
> ExactSequence = 1 if the predicted token sequence exactly equals the hidden phrase, otherwise 0.
> TokenLCS = length of the longest common subsequence between predicted and true tokens divided by max(predicted_token_count, true_token_count).
> PositionF1 = F1 over (position, token) pairs. Precision is correct predicted pairs divided by predicted pairs; recall is correct predicted pairs divided by true pairs.
> CharacterSimilarity = mean aligned-token similarity, where each aligned token similarity is 1 - levenshtein_distance(predicted_token, true_token) / max(token_lengths). Missing aligned tokens receive 0.
> ProfileF1 = F1 over (position, coarse_shape) pairs, where coarse shape is computed from vowels, consonants, þ, and token length.
> The row score is:
> row_score =
> 0.30 * ExactSequence
> + 0.25 * TokenLCS
> + 0.15 * PositionF1
> + 0.20 * CharacterSimilarity
> + 0.10 * ProfileF1
> The final score is:
> final_score = mean(row_score over all test rows)
> The score is bounded in [0, 1]. The sample submission scores 0. A perfect oracle scores 1.
> Submission format
> The submission must have exactly two columns in this order:
> | column | type | description |
> |---|---|---|
> | `id` | string | Test row ID from `test.csv`. |
> | `predicted_gap` | string | Space-separated predicted phrase. |
> CSV example:
> id,predicted_gap
> 0a12bc34de56f789,eptir name foþur
> What not to use
> Do not use or assume source inscription signums, source file order, raw personal names, repository paths, or external lookup. These are absent from solver-facing files and the examples are source-disjoint anonymized repair windows.
> Do not simply copy damaged_gap. It is intentionally corrupted, row-locally letter-anonymized, and may contain invalid characters such as ?.
> Do not submit JSON, comma-separated lists, natural-language explanations, transliteration commentary, or source citations. Submit only the token sequence.
> Do not key predictions to row order, row ID hashes, fixed region buckets, or fixed rare-token positions. IDs and rare abstractions are generated deterministically but carry no answer key.
> Benchmark boundary
> This is not ancient-text retrieval, OCR, machine translation from a full sentence, or generic masked-language modeling. The task asks for constrained normalization of a short missing phrase from row-local damaged runic-style clues, neighboring normalized context, and source-disjoint cultural-heritage text. Unlike standard lacuna restoration benchmarks, the public input removes source signums and personal names, abstracts rare words, anonymizes damaged clue letters per row, and scores exact phrase recovery plus token, character, and profile-level partial correctness.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## KhuwaRoute: Orthographic Repair Trace from Translation Variants

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76g21abn04msf7apfk2z6kjd8a1af0
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat rzotime's score of 57.522!

Full challenge description from page:

> KhuwaRoute: Orthographic Repair Trace from Translation Variants
> Overview
> KhuwaRoute is a sequence-to-sequence challenge about low-resource translation review. The data is derived from a professionally translated Portuguese-Emakhuwa sentence collection with multiple human Emakhuwa renderings for many Portuguese source sentences. Bilingual translators produced the translations, independent reviewers checked them, and alternate Emakhuwa references were retained during the review process. This matters because Emakhuwa is low-resource and spelling or morphology variation is a real quality-control problem in translation workflows.
> In this challenge, each row shows lossy, de-identified public views of one translation-review record. Portuguese content words are represented as stable ptk##### aliases, Emakhuwa content words are represented as stable kwt##### aliases, and some Portuguese positions are replaced by length markers such as <p8>. The alias ids preserve repeated wordform identity inside the challenge, but they do not expose the original public-source text. Your model must output a compact repair trace that says, in plain terms: how different the observed anchor variant is from the checked wording, what coarse token edits would repair it, and which canonical de-identified Emakhuwa tokens should appear in the repaired wording. The task is not to write a new translation; it is to infer the hidden reviewer/post-editor trace from the public cues and patterns learned from training rows.
> Evaluation Metric
> Each prediction is parsed as:
> SHIFT=<class> | OPS=<ops> | CANON=<tokens>
> Valid SHIFT classes are STABLE_VARIANT, ORTHOGRAPHIC_SHIFT, and LEXICAL_RECAST.
> OPS is a whitespace-separated sequence of coarse edit tokens.
> CANON is a whitespace-separated sequence of canonical Emakhuwa content tokens.
> Target component meanings:
> SHIFT=STABLE_VARIANT - the anchor is close to the checked primary reference, usually needing only minor spelling or small token repairs.
> SHIFT=ORTHOGRAPHIC_SHIFT - the anchor has a moderate amount of spelling, morphology, or token-form variation relative to the checked reference.
> SHIFT=LEXICAL_RECAST - the anchor is a broader lexical or phrasal recast of the checked reference.
> K<n> in OPS - keep n consecutive anchor tokens.
> D<n> in OPS - delete n anchor tokens.
> A<n> in OPS - add n checked-reference tokens.
> R<a>:<b> in OPS - replace a anchor tokens with b checked-reference tokens.
> CANON - the first canonical de-identified kwt##### content tokens from the checked Emakhuwa reference after simple stopword removal.
> The final score is in [0, 100], higher is better:
> For each SHIFT class c, let TP_c, FP_c, and FN_c be true positives, false positives, and false negatives.
> F1_c = 2 TP_c / (2 TP_c + FP_c + FN_c), with F1_c = 0 if the denominator is zero.
> MacroF1_SHIFT = (F1_STABLE_VARIANT + F1_ORTHOGRAPHIC_SHIFT + F1_LEXICAL_RECAST) / 3.
> For OPS, tokenize on alphanumeric/edit-id tokens and use multiset token F1. For row i, let overlap m_i = sum_t min(count_hat_i(t), count_i(t)):
> F1_OPS_i = 2 m_i / (len_hat_i + len_i), with zero if exactly one side is empty.
> MeanF1_OPS = (1/N) sum_i F1_OPS_i.
> For CANON, use the same multiset token F1:
> MeanF1_CANON = (1/N) sum_i F1_CANON_i.
> RawScore = 0.30 MacroF1_SHIFT + 0.30 MeanF1_OPS + 0.40 * MeanF1_CANON.
> Score = 100 * clip(RawScore, 0, 1).
> A score of 0 means none of the parsed repair structure matches. A score of 100 means every shift class, edit profile, and canonical token sequence matches exactly. Measured references on the shipped split: perfect submission 100.000000, sample/constant submission 5.000000, anchor-copy baseline 35.625827, weak length/anchor proxy 40.224034, TF-IDF 7-neighbor public-data proxy 49.660142.
> Dataset
> The challenge uses 1,500 selected rows with alternate Emakhuwa references. Each selected row is unique. The rows are drawn from a held-out raw translation-review archive, then split deterministically into 996 public training rows and 504 public test rows. The three SHIFT classes are balanced, with 332 training rows and 168 test rows per class.
> The visible query columns are lossy de-identified views, not the original raw source row:
> pt_view - masked Portuguese content-word aliases. Exposed content words use ptk#####; some positions are replaced by length markers such as <p8>.
> anchor_hint - the first de-identified Emakhuwa content-token aliases from the observed anchor variant, with function words and punctuation removed.
> anchor_inventory - a sorted de-identified content-token alias inventory from the same anchor variant. This preserves vocabulary evidence while removing sentence order.
> route_hint - a balanced nuisance label with values atlas, beacon, cedar, and delta. It exists only as a shortcut-resistance check: it is balanced within each SHIFT class and should not help prediction.
> repair_sequence - the target sequence for training rows only.
> The hidden fields used to build the target are the original Portuguese sentence, the original full Emakhuwa anchor variant, the checked primary Emakhuwa reference, the raw-to-alias lexicons, the anchor-vs-primary token edit trace, and the canonical content tokens from that checked reference. These hidden fields are stripped from test.csv. The public test rows intentionally expose no raw lexical tokens from the source text.
> public/ contains:
> train.csv
> sample_id - string - unique row id.
> pt_view - string - masked Portuguese content-token aliases.
> anchor_hint - string - ordered prefix of de-identified Emakhuwa anchor content-token aliases.
> anchor_inventory - string - sorted inventory of de-identified Emakhuwa anchor content-token aliases.
> route_hint - string - balanced nuisance route label.
> repair_sequence - string - target sequence for training rows.
> test.csv
> sample_id - string - unique row id.
> pt_view - string - masked Portuguese content-token aliases.
> anchor_hint - string - ordered prefix of de-identified Emakhuwa anchor content-token aliases.
> anchor_inventory - string - sorted inventory of de-identified Emakhuwa anchor content-token aliases.
> route_hint - string - balanced nuisance route label.
> sample_submission.csv
> sample_id - string - test row id.
> repair_sequence - string - placeholder prediction in the required format.
> Concrete examples:
> Training row:
> sample_id: KR001025
> pt_view: ptk02373 ptk05280 <p8> ptk00330 ptk07759 <p8> ptk07533 ptk03385 <p8> ptk04606 ptk07941 <p8> ptk03228 ptk01007 <p8>
> anchor_hint: kwt03368 kwt01917 kwt02327 kwt04857 kwt03459 kwt02809 kwt13013 kwt12510 kwt01652 kwt11383
> anchor_inventory: kwt01130 kwt01652 kwt01917 kwt02327 kwt02724 kwt02809 kwt03368 kwt03380 kwt03459 kwt04600 kwt04857 kwt06136 kwt11383 kwt12510 kwt13013
> route_hint: delta
> repair_sequence: SHIFT=LEXICAL_RECAST | OPS=K3 R3:3 K1 R1:1 K8 | CANON=kwt03368 kwt01917 kwt02327 kwt06847 kwt11320 kwt12832 kwt13013 kwt03757 kwt01652 kwt11383
> Test row:
> sample_id: KR000348
> pt_view: ptk05271 ptk00070 <p8> ptk03246 ptk03524 <p8> ptk05494 ptk02564 <p8> ptk03664 ptk05101 <p8> ptk05388 ptk03213 <p8> ptk02014
> anchor_hint: kwt05202 kwt06954 kwt10884 kwt05049 kwt11210 kwt04432 kwt09976 kwt13146 kwt03563 kwt02248
> anchor_inventory: kwt00941 kwt01391 kwt01509 kwt01873 kwt02248 kwt02385 kwt03563 kwt04213 kwt04213 kwt04432 kwt04517 kwt05049 kwt05202 kwt05297 kwt05769 kwt06363 kwt06538 kwt06698 kwt06954 kwt07223 kwt07724 kwt08737 kwt08784 kwt09540 kwt09976 kwt10874 kwt10884 kwt11210 kwt13146
> route_hint: cedar
> Sample submission row:
> sample_id: KR000348
> repair_sequence: SHIFT=ORTHOGRAPHIC_SHIFT | OPS=K0 | CANON=EMPTY
> Submission
> Submit a CSV with exactly 504 rows and exactly these columns in this order:
> sample_id - string - must match the ids in test.csv, with no missing, duplicate, or unknown ids.
> repair_sequence - string - predicted structured sequence in the format SHIFT=<class> | OPS=<ops> | CANON=<tokens>.
> For automated runs, write the final answer file as submission.csv in the current working directory. The safest route is to start from sample_submission.csv, keep the sample_id column unchanged, and replace only the repair_sequence values.
> The first line of the file must be exactly:
> sample_id,repair_sequence
> Use every sample_id from test.csv exactly once. Row order does not matter, because the grader aligns rows by sample_id. Do not include an index column such as Unnamed: 0, training ids, notes, confidence scores, JSON, Markdown, or any extra columns. Extra columns, missing columns, missing rows, duplicate ids, unknown ids, or the wrong row count raise a clean validation error. Malformed sequence strings, unknown SHIFT classes, NaN, and infinity values do not crash the grader; they receive worst-case credit for the affected parts.
> Example submission:
> sample_id,repair_sequence
> KR000245,SHIFT=ORTHOGRAPHIC_SHIFT | OPS=K0 | CANON=EMPTY
> KR001262,SHIFT=ORTHOGRAPHIC_SHIFT | OPS=K0 | CANON=EMPTY
> What Not to Use
> Majority-class prediction fails because SHIFT classes are balanced and macro-F1 is used.
> The route_hint nuisance label fails because it is balanced within every SHIFT class and was included to detect shortcut reliance.
> Looking up the original public text fails because public query fields and CANON targets use de-identified aliases, not raw lexical tokens.
> Copying anchor aliases into CANON gets partial credit but misses the hidden edit profile and repair class.
> Treating this as ordinary Portuguese-to-Emakhuwa translation fails because the scored output is a repair trace, not fluent prose.
> Single-field length heuristics fail because the class and canonical token sequence depend on both the Portuguese source and the Emakhuwa variant.
> Expected strong solutions learn low-resource spelling and lexical repair patterns from the paired training examples, then decode a three-part sequence for the held-out public views.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Phase-Conditioned Procedure Span Infilling

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dqhn8t1r10rg9jsgt7f2z058ak648
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat cohort3krishna's score of 0.824!

Full challenge description from page:

> Generate the exact ordered normalized-word span omitted from one phase of a curated multi-step procedure. Each row supplies readable procedure context, prerequisite and consequence terms, the phase sequence, and masked_segments for the target step. A visible segment contains normalized words; a gap contains only its index and length. target_gap_index identifies which hidden span to generate. When one source step supplies two rows, both gaps remain hidden in both rows, preventing sibling-row answer leakage.
> Common function words are absent and inflected forms are conservatively normalized, so the output is a compact content-word sequence rather than verbatim prose. Related procedures and exact duplicate source steps remain together across allocation.
> Dataset
> train.csv: 766 labeled rows.
> test.csv: 413 unlabeled rows.
> sample_submission.csv: 413 deterministic schema-valid random predictions illustrating the required CSV serialization.
> All catalog records connected by any parent-child relation, plus records sharing an exact procedure-step text, are kept on the same side of the allocation boundary.
> Column Definitions
> id (string; opaque row id)
> prompt (string; task instruction)
> flow_context_json (JSON object; pattern_context_tokens, prerequisite_tokens, consequence_tokens, phase_sequence, and target_step with flow_position, phase, masked_segments, target_gap_index, and missing_token_count)
> missing_token_count (integer; exact number of normalized words to generate)
> answer_format_json (JSON object; root name, token pattern, and required count)
> answer_json (JSON object in train.csv only; ordered missing normalized words)
> Prediction Object
> answer_json is {"missing_tokens":[...]}. The list length must equal missing_token_count, order matters, and every item must match [a-z][a-z0-9_]{0,31}.
> Submission Format
> Submit a UTF-8 CSV with exactly id and answer_json, in either column order, and exactly one row for every test id. IDs must be unique and match the test ids exactly. The examples below demonstrate serialization; their identifiers and values are illustrative.
> id,answer_json
> flow_example_01,"{""missing_tokens"":[""credential"",""access""]}"
> flow_example_02,"{""missing_tokens"":[""send"",""request"",""server""]}"
> Malformed JSON or a row that violates its schema receives zero for that row. Grading continues for the remaining rows. Missing or extra columns, a wrong row count, duplicate ids, or a mismatched id set reject the complete submission.
> Evaluation
> position_accuracy is the fraction of list positions containing the exact true token. token_F1 is duplicate-aware multiset F1: common token multiplicity is summed from the intersection of token counters, precision is common multiplicity divided by submitted length, and recall is common multiplicity divided by true length. token_LCS is longest-common-subsequence length divided by the true length. exact_span is 1 only when the entire ordered list matches.
> row_score = 0.55*exact_span + 0.25*position_accuracy + 0.10*token_F1 + 0.10*token_LCS
> The final score is the arithmetic mean over all evaluation rows.
> Scores range from 0 to 1, and higher is better. A completely correct submission scores 1.
> Expected Methods
> CPU sparse retrieval, sequence alignment, phase-aware reranking, compact token models, and schema-constrained decoding.
> What Not To Use
> GPU, TPU, Metal, CUDA, ROCm, or any other accelerator for training, inference, feature extraction, or search
> Hosted APIs, remote inference services, or network access during solution execution
> Runtime package installation, downloaded code, vendored external code, or remote-code loaders
> External datasets, external answer tables, or challenge-specific pretrained checkpoints
> Hardcoded mappings from row ids, asset names, aliases, or exact evidence records to answers
> Manual labeling of evaluation rows
> Solutions must operate on the supplied files with CPU resources only. General-purpose libraries and public general-purpose pretrained weights already present in the execution environment are allowed when they run entirely on CPU and were not trained specifically for this dataset.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Cyber Match Clause Assembly

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76kqxwynk19jq977132ymeyh8arbyx
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Beat phoneixrider2_0's score of 0.543!

Full challenge description from page:

> Anonymous Constraint Formula Assembly
> Overview
> Each row is an anonymous constraint-assembly puzzle. You are given shuffled match cards describing software, platform, or environment conditions, plus noisy clue cards about which conditions may belong together. Your task is to reconstruct the hidden Boolean formula that combines the row-local aliases.
> In plain terms: divide the M# cards into the correct local clauses and write the AND/OR expression over those aliases. This is a structured-generation task over anonymized technical evidence cards. It is not classification, regression, severity prediction, entity lookup, or table prediction.
> Public rows do not include source record IDs, organization names, product names, raw prose, source URLs, or exact version strings. Train and test examples are source-record disjoint.
> Task
> Submit predicted_formula, a Boolean expression using:
> aliases from match_cards, such as M1;
> operators AND and OR;
> commas and parentheses.
> Examples:
> AND(OR(M1,M4),OR(M2,M3,M5))
> AND(M2,OR(M1,M3,M4))
> Every match alias from match_cards must appear exactly once. Extra aliases, missing aliases, duplicate aliases, unsupported operators, malformed parentheses, or blank formulas score 0 for that row.
> Files
> train.csv
> | column | type | description |
> |---|---|---|
> | `id` | string | Anonymous row ID. |
> | `match_cards` | JSON list | Shuffled match cards. Each card has `m`, `asset_hint`, `vendor_hint`, `product_hint`, `version_hint`, `endpoint_shapes`, `target_sw_shape`, and `update_shape`. These fields are hints, not exact source identities. |
> | `clue_cards` | JSON list | Noisy logical hints. Clues can be incomplete or distracting, and neither clue type is guaranteed correct. |
> | `operator_inventory` | string | Allowed operators, always `AND OR`. |
> | `leaf_count` | integer | Number of match aliases that must appear exactly once. |
> | `scenario_profile` | JSON object | Coarse noisy aggregate profile. It gives broad mix/balance hints but never the exact hidden clause sizes. |
> | `year_bucket` | string | Coarse source-feed time bucket. |
> | `target_formula` | string | Training-only canonical formula. |
> test.csv has the same columns except target_formula.
> sample_submission.csv
> | column | type | description |
> |---|---|---|
> | `id` | string | Test row ID. |
> | `predicted_formula` | string | Boolean formula over row-local aliases. |
> local aliases.
> ## **Match card schema**
> field	type	description
> m	string	Row-local match alias such as M4.
> asset_hint	string	Noisy coarse hint such as component, package, service, runtime, platform, system, or device. This is not a gold clause label.
> vendor_hint	string	Noisy row-local vendor-family hint such as VH3. Equal values can be useful but are not exact vendor identity or a gold clause label.
> product_hint	string	Noisy row-local product-family hint such as PH2. Equal values can be useful but are not exact product identity or a gold clause label.
> version_hint	string	Noisy version-range hint such as open, baseline, single, before, after, window, range, or bounded. This is not a gold clause label.
> endpoint_shapes	list[string]	Noisy coarse shape hints for version endpoints; exact versions are hidden and equal lists are not clause labels.
> target_sw_shape	string	Noisy coarse hint for a target-platform field.
> update_shape	string	Noisy coarse hint for an update/release field.
> Clue card schema
> | field | type | description |
> |---|---|---|
> | `kind` | string | `same_clause` or `requires_with`. Both are weak evidence cards, not hard constraints. |
> | `a`, `b` | string | Match aliases referenced by the clue. |
> | `confidence` | string | `low` or `medium`. Low-confidence clues include distractors. |
> Evaluation
> Invalid row predictions receive 0 for that row. Structurally invalid submission files are rejected.
> Formula arguments to AND and OR are treated as unordered for exact canonical comparison.
> For each valid row:
> ClauseF1 is F1 over non-root internal clauses represented as (operator, sorted_aliases_under_clause).
> PairRelationF1 is F1 over (operator, alias_a, alias_b) triples for alias pairs under the same non-root clause.
> RootOp is 1 when the predicted root operator equals the gold root operator, otherwise 0.
> ExactFormula is 1 when the canonical predicted formula exactly equals the canonical gold formula, otherwise 0.
> LeafCoverage is F1 over match aliases used by the formula. Because all aliases are required exactly once, missing or duplicated aliases make the row invalid.
> The row score is:
> row_score =
> 0.40 * ClauseF1
> + 0.30 * PairRelationF1
> + 0.05 * RootOp
> + 0.20 * ExactFormula
> + 0.05 * LeafCoverage
> The final score is:
> final_score = mean(row_score over all test rows)
> The score is bounded in [0, 1]. The sample submission scores 0. A perfect oracle scores 1.
> Submission format
> The submission must have exactly two columns in this order:
> | column | type | description |
> |---|---|---|
> | `id` | string | Test row ID from `test.csv`. |
> | `predicted_formula` | string | Boolean formula over match aliases. |
> CSV example:
> id,predicted_formula
> 0a12bc34de56f789,"AND(OR(M1,M4),OR(M2,M3,M5))"
> What not to use
> Do not use source record IDs, source URLs, organization names, product names, exact versions, row order, or external lookup. These are absent from solver-facing rows.
> Do not assume clue_cards are complete or always correct. They include distractors, and requires_with does not mean “must be in the other clause.”
> Do not submit JSON, natural-language explanations, source identifiers, product/version strings, or prose summaries.
> Do not omit aliases, duplicate aliases, invent aliases, or use unsupported operators.
> Benchmark boundary
> This benchmark is not a severity-scoring, weakness-tagging, product-normalization, retrieval, or text-classification task. The source records are transformed into row-local constraint cards, noisy relation clues, and anonymous aliases. The required output is an executable Boolean formula, so solvers must perform clause factorization and constrained decoding rather than retrieve a label from a known public record. This is a highly novel task and no near task exists on this platform.
> The closest adjacent task families usually ask for one label, one normalized product string, or one retrieved source record. This task changes the output object, supervision, and metric: it asks for a complete unordered AND/OR structure over all local aliases, with partial credit for internal clause recovery and exact credit for the final formula.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Masked Rare Physics Concept Route Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78hrmx82vpt6aq2d3shebjnn8a6zbm
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat rajat56's score of 0.644!

Full challenge description from page:

> Masked Rare Physics Concept Route Reconstruction
> Overview
> Specialized physics papers often combine signals from several levels of scientific taxonomy: a broad physical-sciences domain, a field, a subfield, a specific topic, and fine-grained concepts such as materials, devices, lattice models, spectroscopy methods, quantum phases, or plasma regimes. In this challenge, each example is a masked metadata prompt derived from a rare physics work. Your task is to reconstruct the ordered concept route that best describes the work.
> This is a sequence-to-sequence challenge. The input is not a table of independent numeric features. Each row contains a lossy metadata_prompt plus a noisy candidate_tokens bank. The prompt contains anonymized and transformed metadata signals such as year band, work type, citation band, venue type, limited institution-country/type signals, shuffled title terms, shuffled abstract terms, and keyword terms. The candidate bank contains 48 possible route tokens for the row, including the hidden route tokens mixed with distractors. Distractor topics are co-sampled with their parent DOMAIN, FIELD, and SUBFIELD tokens, so each bank contains multiple structurally valid route lineages. The public files do not contain source work identifiers, DOI values, source names, original row order, raw concept scores, or the ordered target concept route for test rows.
> The output is an ordered sequence of route tokens. A correct sequence should move from broad taxonomy to specific topic and concepts, for example from DOMAIN to FIELD, SUBFIELD, TOPIC, and then relevant CONCEPT_L* tokens. The exact token vocabulary is provided in token_schema.csv.
> This task is intentionally difficult because the metadata prompt is partial, unordered, and noisy, and the candidate bank is not ordered by relevance. Strong solutions should learn from train.csv how broad-to-specific routes are structured, score candidate tokens against the masked prompt, and rerank complete route sequences. Simple popularity baselines, exact keyword matching, or copying a nearby training route should leave significant headroom.
> Files
> | File | Columns | Description |
> |---|---|---|
> | public/train.csv | work_id, metadata_prompt, candidate_tokens, target_sequence | Labeled training examples. target_sequence is the ordered concept route to learn. |
> | public/test.csv | work_id, metadata_prompt, candidate_tokens | Unlabeled examples for which you must predict an ordered concept route. |
> | public/token_schema.csv | token, label | Valid route tokens and human-readable labels. The output family is encoded in each token prefix before the colon. |
> | public/sample_submission.csv | work_id, concept_sequence | Required submission shape. The included values are dummy placeholders and are not a useful baseline. |
> Columns
> | Column | Type | Description |
> |---|---|---|
> | work_id | string | An anonymized identifier for the prepared challenge row. |
> | metadata_prompt | string | A transformed solver-facing prompt containing lossy metadata signals. |
> | candidate_tokens | string | A noisy row-specific bank of 48 possible route tokens separated by | . The hidden route tokens are included with distractors, but the bank is unordered. |
> | target_sequence | string | Training-only ordered target route, with tokens separated by | . |
> | token | string | A valid output token such as FIELD:physics_and_astronomy or CONCEPT_L2:superconductivity. |
> | label | string | Human-readable token label derived from the token string. |
> | concept_sequence | string | Your predicted ordered route for a test row, with tokens separated by | . |
> Objective
> For every row in test.csv, predict a concept_sequence that reconstructs the hidden ordered route. The intended route tokens are present somewhere in that row's candidate_tokens, but distractors are also present and the order is shuffled. Use metadata_prompt, candidate_tokens, train.csv, and token_schema.csv to select and order the correct route. The best submissions should recover both the correct tokens and their broad-to-specific ordering.
> Evaluation
> Submissions are evaluated with a custom sequence score between 0 and 1, where higher is better.
> For each row:
> row_score =
> 0.50 x token_f1
> + 0.20 x ordered_lcs
> + 0.05 x family_order_lcs
> + 0.15 x weighted_critical_route
> + 0.10 x exact_sequence
> In this formula, x means multiplication. The coefficients sum to 1.00.
> The final score is the mean row_score across all test rows.
> For model-generated outputs, the grader uses only the first 20 parsed route tokens in each concept_sequence. Extra tokens are ignored rather than causing a submission-level failure. Empty or unparseable concept_sequence values receive 0 credit for that row.
> Metric components:
> | Component | Meaning |
> |---|---|
> | token_f1 | Multiset F1 between predicted route tokens and true route tokens. |
> | ordered_lcs | Longest common subsequence length between predicted tokens and true tokens, divided by true sequence length. |
> | family_order_lcs | Longest common subsequence length between predicted token families and true token families, divided by true sequence length. |
> | weighted_critical_route | Weighted exact-match credit for the first true DOMAIN, FIELD, SUBFIELD, and TOPIC tokens. Weights are 0.05, 0.10, 0.30, and 0.55 respectively. |
> | exact_sequence | 1 only when the full predicted token sequence exactly equals the true sequence; otherwise 0. |
> This metric rewards correct fine-grained tokens and ordering. Predicting only common broad prefixes such as the physical-sciences domain is not enough to score well.
> Submission Format
> Submit a CSV with exactly these columns in this order:
> | Column | Type | Description |
> |---|---|---|
> | work_id | string | Must match one row from test.csv. |
> | concept_sequence | string | Ordered route tokens separated by | . |
> Example:
> | work_id | concept_sequence |
> |---|---|
> | work_0123456789abcdef00 | DOMAIN:physical_sciences | FIELD:physics_and_astronomy | SUBFIELD:condensed_matter_physics | TOPIC:physics_of_superconductivity_and_magnetism | CONCEPT_L0:physics | CONCEPT_L1:condensed_matter_physics | CONCEPT_L2:superconductivity |
> | work_abcdef012345678900 | DOMAIN:physical_sciences | FIELD:physics_and_astronomy | SUBFIELD:atomic_and_molecular_physics_and_optics | TOPIC:semiconductor_materials_and_interfaces | CONCEPT_L0:materials_science | CONCEPT_L1:electronic_engineering | CONCEPT_L2:semiconductor | CONCEPT_L3:semiconductor_materials |
> Requirements:
> Include exactly one row for every test work_id.
> Do not duplicate work_id values.
> Keep the columns in the order work_id, concept_sequence.
> Use route tokens from token_schema.csv.
> Prefer tokens from the row's candidate_tokens bank unless your model has strong validation evidence for using another valid token.
> Separate tokens with | .
> Keep each route concise. Only the first 20 parsed tokens are scored.
> Do not add extra columns.
> Do not use external source-row lookup, original scholarly record IDs, DOI lookup, source names, source-row order, original concept scores, or non-public labels.
> Recommended approaches:
> Build a local validation split from train.csv.
> Train candidate-token scoring models using prompt terms, token labels, and the row-specific candidate bank.
> Combine supervised token selection, route-pattern features, candidate-lineage consistency, and route-level reranking.
> Use CPU-friendly models such as linear classifiers, gradient-boosted rerankers, compact sequence models, or constrained decoding over candidate_tokens.
> Tune for the provided sequence metric rather than plain exact match.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## KnotScript: Anonymous Hypergraph Program Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7erb0yhsrh7ww3k5s3jtrtax8aqfhv
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat usamaasif's score of 34.813!

Full challenge description from page:

> KnotScript: Anonymous Hypergraph Program Recovery
> Overview
> Recover an anonymous typed program that describes the hidden document grammar behind two aligned but incomplete symbol streams. Each row provides opaque lexical symbols, opaque structural symbols, and a document-family code. The output contains variable declarations, n-ary frame incidence, and two precedence chains. It contains no text spans, offsets, source identifiers, or canonical variable names.
> The same program may be written with any valid x… names for node variables and y… names for frame variables. The grader obtains a canonical index for every variable by traversing the submitted precedence chains, then compares the complete typed incidence graph. A solver must therefore recover which typed variables exist, exactly which role connects each frame and node, and both orders—not reproduce an index-based extraction format.
> Training rows include anchor_guide, a position scaffold for learning the latent node alignment. It is absent from test rows and is not part of the output. Difficulty includes 5% independent symbol redaction and 3% independent structural-symbol redaction. The real graph annotations are never perturbed. Near-template document groups are kept wholly on one side of the split, and every target code used in test occurs in at least one training group. scan_code is balanced within frame-bearing and frame-free groups and is deliberately uninformative.
> This is variable-length program transduction. The intended approach is to learn node alignment from the training scaffold, infer frame incidence jointly, and finally emit an anonymous constrained program.
> Evaluation Metric
> The grader parses each program into typed declarations, bindings, and precedence edges. The C edges must form one complete node chain and the Q edges must form one complete frame chain. Traversing those chains gives canonical node indices i and frame indices j, independent of handle names and statement order.
> Each valid program is represented by three complete fact multisets:
> Dᴺ = {(i, node_type)} for every canonical node position.
> Dᶠ = {(j, frame_type)} for every canonical frame position.
> B = {(j, role, i)} for every frame-role-node binding.
> For predicted facts P and target facts T, let cₚ(z) and cₜ(z) be the count of fact z:
> overlap(P,T) = Σ_z min(cₚ(z), cₜ(z))
> F(P,T) = 2 × overlap(P,T) ÷ (|P| + |T|)
> If both multisets are empty, F(P,T) = 1.
> Mᴺ is the mean F(Dᴺ_pred,Dᴺ_true) over all 510 rows. Mᶠ and Mᴮ are the means of F(Dᶠ_pred,Dᶠ_true) and F(B_pred,B_true) over rows where either the target or prediction declares a frame. Inventing a frame in a frame-free row therefore adds a zero-scoring frame and binding row.
> Final score
> Score = round(100 × clip(0.35 × Mᴺ + 0.20 × Mᶠ + 0.45 × Mᴮ, 0, 1), 6).
> The theoretical minimum is 0 and the theoretical maximum is 100. A malformed program is treated as an empty graph for that row. Every target declares at least one node, so an empty, missing, or garbage program receives no abstention credit. A perfect submission scores exactly 100.000000.
> Perfect-score equivalence is exact: score 100 requires equality of all three canonical fact multisets on every row. Equality fixes the ordered typed node list, ordered typed frame list, and every role-labelled incidence. Thus two valid programs receive the same perfect score exactly when they differ only in handle names or statement order.
> Measured on the shipped public files with the shipped grader:
> Empty program — 0.000000
> Surface-symbol lookup — 12.836931
> Nearest-template retrieval — 27.091257
> Contextual linear node decoder — 12.342689
> CPU BiGRU node decoder — 15.229116
> CPU joint BiGRU topology decoder — 33.402210
> Perfect submission — 100.000000
> The joint model gains 6.310953 points over nearest-template retrieval and 20.565279 over surface lookup. The CPU proxy is intentionally conservative; capable agent runs are expected around 35–65, with substantial headroom for better constrained program decoders.
> Dataset
> train.csv
> Contains 1,616 labeled documents.
> sample_id — string — opaque row identifier.
> symbol_sequence — string — space-separated g##### symbols with [GAP] markers.
> pos_sequence — string — aligned s## symbols with [SGAP] markers.
> genre_code — string — opaque document-family code.
> scan_code — string — balanced nuisance code p00 or p01.
> anchor_guide — string — training-only typed node spans in r##@start:length form.
> graph_program — string — target anonymous program.
> test.csv
> Contains 510 rows with only the five input columns. Neither training scaffold nor target is present.
> sample_submission.csv
> Contains every required test identifier and the empty program placeholder |.
> schema_vocabulary.csv
> token_kind — string — node_type, event_type, or argument_role.
> code — string — valid opaque code for that kind.
> Program Grammar
> Tokens are separated by spaces. Exactly one | separates the node layer from the frame layer.
> N:x0:r03 — declare node variable x0 with type r03.
> C:x0:x1 — node x0 immediately precedes node x1.
> F:y0:v04 — declare frame variable y0 with type v04.
> B:y0:a07:x1 — bind role a07 of frame y0 to node x1.
> Q:y0:y1 — frame y0 immediately precedes frame y1.
> Node handles must match x[a-z0-9]{1,8} and frame handles must match y[a-z0-9]{1,8}. Handles must be declared exactly once. Every edge must reference declared handles. Self-edges and duplicate statements are malformed. Every declared frame must have at least one B binding.
> For k declared nodes, the C statements must form one directed chain containing every node exactly once: zero edges when k ≤ 1, otherwise exactly k − 1 edges, one start, one end, and no branch, cycle, or disconnected component. The same rule applies to Q and the declared frames. The chain order—not the spelling of handles—defines canonical positions.
> Handle names and statement order do not affect the score. For example, consistently replacing every x0 with xblue and every y0 with y7 preserves the represented program.
> A real training program is:
> undefined
> N:x000:r13 N:x001:r03 N:x002:r03 N:x003:r00 N:x004:r00 N:x005:r06 N:x006:r15 C:x000:x001 C:x001:x002 C:x002:x003 C:x003:x004 C:x004:x005 C:x005:x006 | F:y000:v11 B:y000:a29:x002 B:y000:a06:x004 B:y000:a05:x005 B:y000:a12:x000 B:y000:a13:x003 B:y000:a11:x006
> ## Submission
> Submit a CSV with exactly `510` rows and a header. Required columns may be reordered; unrelated extra columns are ignored.
> - `sample_id` — string — every test identifier exactly once.
> - `graph_program` — string — one variable-length program.
> Example with a real test identifier:
> sample_id,graph_program
> 00121c7e48c685ee,|
> Duplicate, missing, or unknown identifiers and an incorrect row count reject the submission. Invalid programs receive the empty-graph result for that row and never crash the grader.
> ## What Not to Use
> - A position-indexed span extractor does not directly produce anonymous variables, exact incidence facts, or precedence programs.
> - A one-symbol substitution table can approximate node counts but cannot decide which roles share a variable.
> - Independent row-level labels cannot represent a variable-length graph program.
> - Copying canonical handle names is useless because handle renaming is score-invariant.
> - `scan_code` is balanced inside frame-bearing and frame-free groups.
> - External source alignment is blocked by opaque identifiers, fixed symbol permutations, and independent redaction.
> Successful solutions should combine sequence alignment, latent-variable induction, n-ary incidence recovery, and constrained program generation. All shipped baselines and the intended solution path run on CPU.
> &nbsp;

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Sanskrit Manuscript OCR Correction-Alignment Trace Decoding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79vcqywg7vwzcpwj27c289qd8an6ym
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: generative
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Sanskrit Manuscript OCR Correction-Alignment Trace Decoding
> Overview
> Historical manuscript digitization needs more than a corrected transcription. Editors must also be able to audit which noisy OCR character supported each correction and whether the correction was a direct copy, a replacement, or an insertion. This challenge asks for that complete correction-audit trace.
> Each row provides a transformed 80-token noisy OCR fragment. Your task is to generate the ordered correction-alignment trace for its 64 corrected characters. Every trace step jointly records the corrected character, its aligned OCR position, and the edit operation that produced it. This is an alignment-aware sequence-decoding task, not ordinary post-OCR text correction and not source lookup.
> Task or Target Semantics
> ocr_sequence contains exactly 80 space-separated tokens. Encoded character tokens range from c001 through c152. The token pad may occur only at the right end after a shorter OCR fragment and has no character meaning.
> target_sequence contains exactly 192 space-separated tokens. It represents 64 consecutive correction-alignment steps, with exactly three tokens per corrected character in this order:
> corrected_character alignment_pointer edit_operation
> corrected_character is c001 through c152, the corrected character at this reading-order position.
> alignment_pointer is a00 through a79 when the corrected character aligns to that zero-based position in the 80-token OCR input. a80 is the insertion sentinel: the corrected character has no corresponding OCR character.
> edit_operation is e_copy for an unchanged aligned character, e_substitute for a corrected aligned character, or e_insert for an inserted corrected character. e_insert must use a80; the other operations must use a00 through a79.
> The three tokens form one inseparable audit step. Repeated character codes, repeated alignment pointers, and repeated operations are valid when the underlying OCR alignment requires them. pad never appears in a target trace.
> Evaluation
> Submissions are scored with mean exact correction-alignment step accuracy. Higher is better.
> For N test rows, each with 64 trace steps:
> score = exactly_correct_trace_steps / (N * 64)
> A trace step is correct only when all three tokens—the corrected character, alignment pointer, and edit operation—match the hidden trace at the same corrected-character position. The theoretical range is 0.0 to 1.0.
> Dataset
> Public files:
> train.csv contains 9,600 labelled correction-alignment rows.
> test.csv contains 2,400 unlabelled correction-alignment rows.
> sample_submission.csv demonstrates the required submission schema with a weak trace-step majority scaffold derived only from public training targets. It scores above zero but uses no hidden test answers.
> Private file:
> answers.csv contains the 2,400 hidden correction-alignment traces used by the grader.
> The preparation pipeline clusters highly similar corrected fragments before splitting. Any fragments with corrected-text five-character-shingle Jaccard similarity of at least 0.80 are assigned together to train or test.
> Feature Details
> sample_id is a string identifier in the form s followed by 16 hexadecimal characters. It is an opaque key only and carries no source, document, or ordering information.
> ocr_sequence is a string containing exactly 80 whitespace-separated categorical tokens. Each token is c001 through c152, or right-padding pad.
> target_sequence is a string containing exactly 192 whitespace-separated categorical tokens. It appears only in train.csv and private answers.csv. Every consecutive group of three tokens is one corrected-character alignment trace step.
> The original records are real expert-corrected historical Sanskrit manuscript OCR pairs from a licensed academic manuscript-OCR collection. Formal license and source attribution are provided through the platform License and Source fields and reviewer-only raw manifest. Public files contain transformed token sequences only; they do not contain readable passages, source document identifiers, or source-row identifiers.
> Submission
> Submit a CSV with exactly 2,400 data rows plus the header. The two required columns are sample_id and target_sequence, in that order.
> sample_id must appear exactly once and must match every ID in test.csv.
> target_sequence must contain exactly 192 whitespace-separated tokens: 64 valid three-token correction-alignment steps.
> Every character token must be c001 through c152.
> Every alignment token must be a00 through a80; only e_insert may use a80.
> Every operation token must be e_copy, e_substitute, or e_insert.
> Example header: sample_id,target_sequence
> Example row. The trace below contains exactly 64 valid three-token steps:
> s1a2b3c4d5e6f7089,c014 a00 e_copy c021 a01 e_copy c005 a02 e_copy c117 a03 e_copy c009 a04 e_copy c041 a05 e_copy c052 a06 e_copy c003 a07 e_copy c014 a08 e_copy c021 a09 e_copy c005 a10 e_copy c117 a11 e_copy c009 a12 e_copy c041 a13 e_copy c052 a14 e_copy c003 a15 e_copy c014 a16 e_copy c021 a17 e_copy c005 a18 e_copy c117 a19 e_copy c009 a20 e_copy c041 a21 e_copy c052 a22 e_copy c003 a23 e_copy c014 a24 e_copy c021 a25 e_copy c005 a26 e_copy c117 a27 e_copy c009 a28 e_copy c041 a29 e_copy c052 a30 e_copy c003 a31 e_copy c014 a32 e_copy c021 a33 e_copy c005 a34 e_copy c117 a35 e_copy c009 a36 e_copy c041 a37 e_copy c052 a38 e_copy c003 a39 e_copy c014 a40 e_copy c021 a41 e_copy c005 a42 e_copy c117 a43 e_copy c009 a44 e_copy c041 a45 e_copy c052 a46 e_copy c003 a47 e_copy c014 a48 e_copy c021 a49 e_copy c005 a50 e_copy c117 a51 e_copy c009 a52 e_copy c041 a53 e_copy c052 a54 e_copy c003 a55 e_copy c014 a56 e_copy c021 a57 e_copy c005 a58 e_copy c117 a59 e_copy c009 a60 e_copy c041 a61 e_copy c052 a62 e_copy c003 a63 e_copy
> Restrictions
> Do not use external copies of the source corpus, web search, source-document lookup, or reverse-engineered source identifiers.
> Do not use private files, row order, filenames, hashes, or hidden metadata as prediction features.
> CPU-only methods using the provided public files and preinstalled runtime libraries are allowed.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Sound-Law Forensics

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7d5jv7vsnmsw6qma1kjxw4t58ajt0a
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Comparative Witness Repair Under Sound Change
> Overview
> Each row contains five daughter-language witnesses, lang_A through lang_E, that
> ultimately descend from the same hidden ancestral word. The witnesses were generated
> by deterministic sound-change cascades over real lexical seeds, then some witnesses
> were corrupted: a form may be borrowed from another etymon, replaced by the wrong
> branch's reflex, or perturbed by local noise. On a hard slice, daughters A and C are
> masked entirely.
> The released challenge files use abstract segment symbols such as no0, ko0, and
> lu0 rather than direct IPA-like symbols.
> Your job is to repair the witness panel itself:
> predict the clean inherited reflex each daughter should have shown
> label the status of each daughter witness
> This is not protoform reconstruction. The target is the repaired daughter panel, not
> the hidden ancestor.
> The Task
> For each test row, submit:
> repair_A ... repair_E: the clean inherited daughter reflexes
> status_A ... status_E: one of REGULAR, BORROWED, WRONG_BRANCH,
> LOCAL_NOISE, or MASKED
> The task is hard for several reasons:
> The daughters are not aligned. Apocope, paragoge, syncope, insertions, and deletions
> shift segments, so witness repair is not a position-wise copy problem.
> Different daughters lose different contrasts, so repairing one branch can require
> evidence from the others.
> About 33% of test rows contain at least one corrupted visible witness.
> A hard slice masks daughters A and C entirely, forcing imputation from B, D, and E.
> 2,404 test rows come from ancestral segment-bigram shapes excluded from training,
> so memorizing surface patterns is not enough.
> Dataset
> The prepared data is under ./dataset/public/:
> train.csv: observed witnesses plus gold repair and status targets
> test.csv: observed witnesses only
> sample_submission.csv: format example only
> Sizes:
> 36,000 training rows
> 6,000 test rows
> 1,819 hard test rows with lang_A and lang_C blank
> 12,538 contaminated training rows
> 2,003 contaminated test rows
> 2,404 test rows with held-out ancestral segment bigrams
> The hard, contaminated, and held-out-bigram slices overlap. In the test set:
> 604 rows are both hard and contaminated
> 716 rows are both hard and held-out-bigram
> 772 rows are both contaminated and held-out-bigram
> 221 rows belong to all three slices
> Observed input columns in train.csv and test.csv:
> id (string)
> Stable row identifier.
> lang_A (string)
> Daughter A witness; blank only on hard-slice rows.
> lang_B (string)
> Daughter B witness; always populated.
> lang_C (string)
> Daughter C witness; blank only on hard-slice rows.
> lang_D (string)
> Daughter D witness; always populated.
> lang_E (string)
> Daughter E witness; always populated.
> train.csv additionally includes these target columns:
> repair_A (string)
> Clean inherited daughter A reflex.
> repair_B (string)
> Clean inherited daughter B reflex.
> repair_C (string)
> Clean inherited daughter C reflex.
> repair_D (string)
> Clean inherited daughter D reflex.
> repair_E (string)
> Clean inherited daughter E reflex.
> status_A (string)
> One of REGULAR, BORROWED, WRONG_BRANCH, LOCAL_NOISE, MASKED.
> status_B (string)
> One of REGULAR, BORROWED, WRONG_BRANCH, LOCAL_NOISE, MASKED.
> status_C (string)
> One of REGULAR, BORROWED, WRONG_BRANCH, LOCAL_NOISE, MASKED.
> status_D (string)
> One of REGULAR, BORROWED, WRONG_BRANCH, LOCAL_NOISE, MASKED.
> status_E (string)
> One of REGULAR, BORROWED, WRONG_BRANCH, LOCAL_NOISE, MASKED.
> Example training rows:
> Example train.csv rows as CSV:
> tr_000000
> lang_A: no0 ko0 lu0 no0 re0 mu0 po0
> lang_B: lo0 pe0 mu0 ke0 pe0 re0 ku0 me0 ku0
> lang_C: ne0 no0 ko0 lu0 no0 re0 mu0 nu0 ko0
> lang_D: no0 ko0 lu0 no0 re0 ku0 pi0 ku0
> lang_E: lo0 no0 pu0 lu0 pe0 re0 pi0
> repair_A: no0 ko0 lu0 no0 re0 mu0 po0
> repair_B: lo0 pe0 mu0 ke0 pe0 re0 ku0 me0 ku0
> repair_C: ne0 no0 ko0 lu0 no0 re0 mu0 nu0 ko0
> repair_D: no0 ko0 lu0 no0 re0 ku0 pi0 ku0
> repair_E: lo0 no0 pu0 lu0 pe0 re0 pi0
> status_A ... status_E: REGULAR, REGULAR, REGULAR, REGULAR, REGULAR
> tr_000002
> lang_A: ni0 ma0 ko0 ma0
> lang_B: ko0 nu0
> lang_C: nu0
> lang_D: ko0 ma0 ma0
> lang_E: ko0 ma0 ma0
> repair_A: ni0 ma0 ko0 ma0
> repair_B: ko0 nu0 nu0
> repair_C: ko0 nu0 nu0
> repair_D: ko0 ma0 ma0
> repair_E: ko0 ma0 ma0
> status_A ... status_E: REGULAR, BORROWED, LOCAL_NOISE, REGULAR, REGULAR
> Evaluation
> Submissions are scored with a forensic witness-repair score in [0, 1].
> For each row, the repair component is evaluated only on forensic positions: daughters
> whose gold status is not REGULAR. These are the masked or corrupted witnesses, which
> are the positions that actually require repair. If a row has no forensic positions,
> all five daughters are used.
> For one repaired witness:
> sim(p, g) = 1 - edit_distance(p, g) / max(len(p), len(g))
> repair_skill(p, g) =
> 1.0                           if p == g
> max(0, (sim(p, g) - 0.60) / 0.40)   otherwise
> The status component is a row-level macro-F1 over the active status labels present in
> the row's gold or predicted witness labels.
> The per-row score is:
> item_score = 0.70 * mean(repair_skill over forensic positions)
> + 0.30 * status_macro_f1
> The full row-level calculation is:
> forensic_positions(row) = {d in {A,B,C,D,E} : gold_status_d != REGULAR}
> if forensic_positions(row) is empty:
> forensic_positions(row) = {A, B, C, D, E}
> repair_component(row) =
> mean( repair_skill(pred_repair_d, gold_repair_d)
> for d in forensic_positions(row) )
> status_component(row) = macro_f1_over_status_labels_in_that_row
> item_score(row) = 0.70 * repair_component(row) + 0.30 * status_component(row)
> final_score = mean( item_score(row) for row in FORENSIC rows )
> The final score is the mean item_score over FORENSIC rows only. FORENSIC rows are
> the union of the hard slice and the contaminated slice.
> This rewards models that repair missing or corrupted witnesses and correctly identify
> why a witness is problematic.
> Submission Format
> Write ./working/submission.csv with exactly these columns:
> Required columns:
> id
> repair_A
> repair_B
> repair_C
> repair_D
> repair_E
> status_A
> status_B
> status_C
> status_D
> status_E
> Column meanings:
> id
> Row id from test.csv.
> repair_A
> Predicted clean daughter A reflex.
> repair_B
> Predicted clean daughter B reflex.
> repair_C
> Predicted clean daughter C reflex.
> repair_D
> Predicted clean daughter D reflex.
> repair_E
> Predicted clean daughter E reflex.
> status_A
> Predicted status for daughter A.
> status_B
> Predicted status for daughter B.
> status_C
> Predicted status for daughter C.
> status_D
> Predicted status for daughter D.
> status_E
> Predicted status for daughter E.
> Allowed status values:
> REGULAR
> BORROWED
> WRONG_BRANCH
> LOCAL_NOISE
> MASKED
> Requirements:
> exactly one row per id in test.csv
> no duplicate ids
> all repair columns must be non-empty space-separated segment strings
> all status columns must be one of the five allowed labels
> Example:
> Example submission.csv:
> te_000000
> repair_A: ma0
> repair_B: nu0 ko0 na0 ko0
> repair_C: ni0 nu0 ni0 na0 mu0
> repair_D: ko0 ma0 mu0 ni0 na0 ni0
> repair_E: re0
> status_A ... status_E: MASKED, REGULAR, MASKED, REGULAR, REGULAR
> te_000001
> repair_A: pi0
> repair_B: ku0 me0 ni0
> repair_C: ko0 re0 pi0 ko0
> repair_D: ko0 re0 pi0 ku0
> repair_E: pi0
> status_A ... status_E: REGULAR, REGULAR, REGULAR, WRONG_BRANCH, REGULAR
> What Not To Use
> No external lookup or retrieval of answers.
> No hand-coded rule engine keyed to row ids.
> No manual answer keys or private-label leakage.
> No submission that hard-codes status labels from row ids.
> The intended path is a learned model that uses train.csv to infer regular
> cross-daughter correspondence patterns, repair corrupted or masked witnesses, and
> predict witness statuses.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Dialogue Turn Argument Extraction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx792w2csra4bays8fr0xwtzg18avva4
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Each row shows a short window from a task-oriented assistant conversation. One target turn in that window contains one or more argument annotations that would be needed to execute a transaction, such as booking, ordering, appointment scheduling, or ride coordination.
> Your task is to reconstruct the hidden argument bundle for the target turn. A valid answer is a JSON object listing the argument field, status, value text, and character span for every annotated value in that turn. This is a structured text reconstruction problem: strong solutions need to read the surrounding dialogue, interpret the domain schema, normalize values, and align them back to the exact target-turn spans.
> Dataset
> The released files are:
> train.csv: 12,000 labeled dialogue-turn examples.
> test.csv: 4,000 unlabeled dialogue-turn examples.
> sample_submission.csv: valid low-signal example submission.
> Columns:
> id (string): Row identifier.
> prompt (string): Row instruction.
> dialogue_window_json (JSON string): Ordered nearby turns. Each object has turn_index, speaker, and text.
> target_turn_index (integer): Turn index whose hidden argument annotations must be reconstructed.
> target_speaker (string): Speaker for the target turn.
> target_turn_text (string): Text where spans are measured.
> schema_card_json (JSON string): Domain schema with required and optional field names.
> argument_count_hint (integer): Number of argument objects expected.
> answer_format_json (JSON string): Valid output fields, valid statuses, and span convention.
> answer_json (JSON string, train only): Ground-truth argument bundle.
> Submission Format
> Submit a CSV with exactly two columns: id and answer_json.
> answer_json must be a JSON object with one key, arguments. Each argument object must contain:
> domain (string): Domain token from answer_format_json.
> field (string): Slot/argument field name.
> status (string): One of accept, reject, or mentioned.
> value_text (string): The annotated value text.
> start (integer): Start character offset in target_turn_text, or -1 if no exact span is available.
> end (integer): End character offset in target_turn_text, or -1 if no exact span is available.
> Example:
> id,answer_json
> tmarg_abc123,"{""arguments"":[{""domain"":""restaurant_reservation"",""field"":""time.reservation"",""status"":""accept"",""value_text"":""7 pm"",""start"":47,""end"":51}]}"
> tmarg_def456,"{""arguments"":[{""domain"":""movie_ticket"",""field"":""name.movie"",""status"":""mentioned"",""value_text"":""Aquaman"",""start"":30,""end"":37},{""domain"":""movie_ticket"",""field"":""location.theater"",""status"":""accept"",""value_text"":""Reno, Nevada"",""start"":41,""end"":53}]}"
> Malformed JSON or invalid argument objects score zero for that row. Wrong columns, missing rows, duplicate ids, or mismatched ids are rejected.
> Evaluation
> Each row receives a score in [0, 1].
> For each submitted argument and true argument, the grader compares:
> Schema match: 1 when domain, field, and status all match, otherwise 0.
> Value similarity: duplicate-aware token F1 between submitted value_text and true value_text.
> Span similarity: 1 for exact offsets, otherwise intersection-over-union of the character spans; invalid spans score 0.
> The grader greedily matches each true argument to the best remaining submitted argument. Let best_match be the average matched argument score, where each pair score is 0.55 * schema_match + 0.30 * value_similarity + 0.15 * span_similarity.
> Additional row terms:
> schema_f1: duplicate-aware F1 over (domain, field, status) triples.
> value_f1: duplicate-aware F1 over (domain, field, normalized value_text) triples.
> exact: 1 if the complete argument object set matches exactly, otherwise 0.
> length: max(0, 1 - abs(predicted_count - true_count) / max(1, true_count)).
> Row score:
> 0.42 * best_match + 0.25 * schema_f1 + 0.18 * value_f1 + 0.10 * exact + 0.05 * length
> Final score:
> 0.84 * mean_row_score + 0.06 * weakest_domain_group + 0.05 * weakest_argument_count_group + 0.05 * weakest_source_group
> The weakest-group terms are minimum mean row scores over hidden evaluation groups. Higher is better.
> What Not To Use
> Do not use external source lookup or search for the original conversations.
> Do not use hosted APIs, online services, browser automation, or network access during solving.
> Do not use runtime downloads, external corpora, pretrained checkpoints, or non-released answer material.
> Do not hardcode answer maps, row ids, source conversation ids, or memorized test outputs.
> Do not infer answers from file ordering, package-generation internals, or hidden evaluation metadata.
> Do not use GPU, TPU, accelerator execution, or GPU-backed inference services.
> Use only the files released with this challenge package.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## WebAssembly Conformance Trace Fragment Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76jrc5e62k9vqzcawn30hh698as67y
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> WebAssembly conformance tests check whether a small WebAssembly text module behaves as expected. A test usually defines a .wast module and then lists assertions such as assert_return for expected return constants or assert_trap for expected runtime trap messages.
> Each row contains a readable WebAssembly module snippet, visible neighboring assertions, and a few masked assertion queries. Your task is to recover the missing assertion outcomes for those queries: either the exact expected constants or the exact trap message.
> The records are built from conformance-test assertion fixtures. Source filenames, original line numbers, and source trace metadata are not included in the modeling files.
> Dataset
> train.csv: 1,000 labeled rows.
> test.csv: 500 unlabeled rows.
> sample_submission.csv: 500 schema-valid randomized submission rows.
> train.csv columns:
> id (string): anonymized row id.
> assertion_packet_json (JSON object serialized as a string): released module and masked-query evidence.
> assertion_trace_json (JSON object serialized as a string): target assertion outcomes for training rows.
> test.csv columns:
> id (string): anonymized row id.
> assertion_packet_json (JSON object serialized as a string): same schema as in training.
> sample_submission.csv columns:
> id (string): test row id.
> assertion_trace_json (JSON object serialized as a string): example output shape.
> Decoded assertion_packet_json fields:
> task (string): fixed task marker.
> module_snippet (string): readable WebAssembly text module syntax.
> module_summary (object): counts and short previews of exports and operator families.
> visible_assertions (list of objects): neighboring assertions with context_id (string) and assertion (string).
> masked_assertions (list of objects): query objects to recover. Every query has query_id (string) and kind (string, either assert_return or assert_trap).
> output_contract (object): required output field and query ids.
> For an assert_return query, the query object also contains:
> action (string): native invocation action such as (invoke "f" (i32.const 2)).
> expected_arity (integer): number of expected return values.
> value_type_hints (list of strings): expected WebAssembly constant type hints such as i32.const.
> For an assert_trap query, the query object also contains:
> action (string): native invocation action.
> trap_message_hidden (boolean): always true.
> trap_message_word_count (integer): word count hint for the hidden trap message.
> Decoded assertion_trace_json fields:
> assertions (list of objects): one object for each query id.
> For assert_return: query_id (string), kind (string), and expected (list of strings), where each expected value is a WebAssembly constant such as (i32.const 0).
> For assert_trap: query_id (string), kind (string), and trap_message (string).
> Submission Format
> Submit UTF-8 CSV with exactly id and assertion_trace_json, in either column order, and one row for every test id. Row order does not matter.
> assertion_trace_json must be a JSON object serialized inside the CSV cell. In CSV examples, the JSON cell is wrapped in double quotes and every internal JSON quote is doubled.
> id,assertion_trace_json
> case_example_01,"{""assertions"":[{""query_id"":""q00"",""kind"":""assert_return"",""expected"":[""(i32.const 0)""]}]}"
> case_example_02,"{""assertions"":[{""query_id"":""q00"",""kind"":""assert_trap"",""trap_message"":""integer divide by zero""}]}"
> Use the actual query ids and query count for each row. Duplicate ids, missing ids, extra ids, missing columns, or extra columns reject the whole submission. Malformed row-level JSON scores zero for that row.
> Evaluation
> For each valid row, hidden and submitted assertion outcomes are converted into canonical atoms:
> assert_return with values: one atom for each (query_id, return_slot_index, expected_value).
> assert_return with no values: one atom for (query_id, void_return).
> assert_trap: one atom for (query_id, trap_message).
> The canonical atom strings are strict JSON serializations with sorted object keys and no insignificant whitespace. Query order and JSON object-key order do not matter after canonicalization; expected values and trap messages must match exactly.
> Let P be the submitted atom set and T be the hidden atom set:
> precision = |P intersection T| / |P|
> recall    = |P intersection T| / |T|
> row_score = 2 * precision * recall / (precision + recall)
> If both sets are empty, the row score is 1.0. If exactly one set is empty, the row score is 0.0.
> The final score is the arithmetic mean over 500 test rows. A perfect submission scores 1.0.
> Expected Methods
> Suitable CPU methods include WebAssembly text parsing, assertion-pattern modeling, lightweight interpreters for supported fragments, symbolic execution for numeric operators, nearest-context retrieval, and constrained JSON decoding trained only from the supplied rows.
> What Not To Use
> GPU, TPU, accelerator, or GPU-backed execution
> network access, external lookup, external corpora, external archives, or repository copies outside the release
> pretrained external checkpoints, hosted inference APIs, gated assets, downloaded models, or remote-code loaders
> runtime package installation, code downloads, data downloads, or weight downloads
> hardcoded evaluation ids, manually annotated held-out rows, or non-released answer material

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Compositional Facility Evidence Normalization

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78b1z7wkwat0zd9yj00h37qn8ah910
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Compositional Facility Evidence Normalization
> 1. Overview and real-world setting
> This is a structured natural-language understanding and generation challenge based on environmental review records for Iowa swine feeding facilities.
> Environmental reviewers often need to compare several kinds of evidence about the same facility: the capacity recorded in permit documents, the capacity suggested by satellite-detected barn footprints, the number of detected barns, and the number of linked permit and parcel records. These sources can agree, conflict, cross an important regulatory threshold, or create a complicated record trail.
> The goal of this benchmark is to normalize that evidence into a consistent seven-field audit_note. The note represents:
> how urgent the review should be;
> which review workflow should be used;
> how consistent the evidence appears;
> how the reported and estimated capacity bands compare;
> whether the evidence crosses a major capacity threshold;
> how permit and parcel records are linked; and
> whether the detected infrastructure is plausible for the estimated scale.
> Each public input is text only. Participants must identify the final confirmed evidence in the report, compare multiple facts, and generate all seven normalized fields consistently.
> 2. Source data and benchmark packets
> The benchmark is derived from the Iowa CAFO Satellite-Permit Facility Records dataset. The source contains facility-level swine-operation records assembled from permit data, parcel links, and satellite-derived barn measurements.
> The preparation pipeline first converts raw numeric and identifier fields into visible qualitative bands. Targets are then derived only from those visible bands.
> Some rows are controlled counterfactual benchmark packets. These are creator-generated variations of a real source facility's qualitative evidence state, used to provide enough training and evaluation examples for rare but important combinations. For example, a packet may place the satellite-estimated capacity one band above the source facility's factual band or may vary the visible permit/parcel-link pattern. Every altered value is stated in the public report, and every target is recalculated from that final visible state.
> Counterfactual packets are benchmark examples only. They are not factual regulatory findings, compliance determinations, or allegations concerning any real facility.
> A source facility and every packet derived from it are assigned entirely to either training or testing, never both.
> 3. Files and dataset structure
> The prepared benchmark contains approximately 9,000 training rows and 1,600 test rows.
> train.csv — training rows with three columns:
> id (string): unique row identifier, e.g. train_00000. Each id appears exactly once.
> facility_report (string): an English evidence memo describing one facility packet. This is the sole model input. Its structure is described in Section 4.
> audit_note (string): the target seven-field normalized note for that report. Its format and allowed values are defined in Section 6.
> test.csv — evaluation rows with two columns:
> id (string): unique row identifier, e.g. test_00000. Each id appears exactly once.
> facility_report (string): the evidence memo. The corresponding audit_note must be predicted.
> sample_submission.csv — a valid submission skeleton with two columns:
> id (string): every test id, each exactly once.
> audit_note (string): a syntactically valid placeholder note in the required format. Replace the placeholder values with your predictions.
> The generated benchmark contains no raw coordinates, street addresses, facility identifiers, permit identifiers, parcel identifiers, exact animal-unit values, or satellite images.
> 4. Structure of facility_report
> facility_report is an English evidence memo. It may be written as a narrative paragraph, review note, evidence summary, or compact memorandum. Clause order and wording vary.
> A report may describe:
> facility production category;
> broad regional context;
> permit-record capacity band;
> satellite-footprint estimated capacity band;
> detected-barn-count band;
> permit-link-count band; and
> parcel-link-count band.
> Some reports contain both an earlier value and a later corrected value. Terms such as final, confirmed, retained, amended, replaced, withdrawn, reconciled, or superseded identify which evidence controls the target. Participants should use the final confirmed value and ignore explicitly superseded evidence.
> The reports never state target labels such as two_bands_above, dual_fanout, or urgent_review directly.
> 5. Visible evidence bands
> Capacity bands
> Capacity descriptions correspond to these ordered bands:
> at most 500 animal units;
> 501–749 animal units;
> 750–999 animal units;
> 1,000–1,499 animal units;
> 1,500–2,499 animal units; and
> 2,500 or more animal units.
> The 500- and 1,000-animal-unit boundaries define the three broader regulatory zones used by threshold_transition:
> small: at most 500;
> intermediate: 501–999; and
> permit scale: 1,000 or more.
> Detected-barn bands
> none or no confirmed count;
> one;
> two;
> three to four;
> five to seven; and
> eight or more.
> Permit-link and parcel-link bands
> none;
> one;
> two;
> three to four; and
> five or more.
> 6. Target audit_note
> Generate exactly one semicolon-delimited note using all seven keys:
> priority: <value>; route: <value>; confidence: <value>; capacity_relation: <value>; threshold_transition: <value>; record_topology: <value>; infrastructure_fit: <value>
> Field order may vary, but every key must appear exactly once and every value must be one of the allowed values below.
> priority — overall review urgency.
> routine_review
> targeted_review
> elevated_review
> urgent_review
> route — recommended review workflow.
> routine_file_check
> capacity_reconciliation
> threshold_review
> record_reconciliation
> infrastructure_review
> combined_evidence_review
> deferred_evidence_request
> urgent_multi_factor_review
> confidence — consistency and completeness of the visible evidence.
> high
> medium
> low
> conflicting
> capacity_relation — ordered difference between the final estimated-capacity band and the final reported-capacity band.
> estimate_below_report
> same_band
> one_band_above
> two_bands_above
> three_bands_above
> four_plus_bands_above
> threshold_transition — movement between the small, intermediate, and permit-scale regulatory zones.
> stays_small
> crosses_500
> stays_intermediate
> crosses_1000
> stays_permit_scale
> downward_transition
> record_topology — relationship between the final permit-link and parcel-link bands.
> no_linked_records
> one_to_one
> parcel_fanout
> permit_fanout
> dual_fanout
> asymmetric_complex
> infrastructure_fit — compatibility between the final detected-barn band, facility category, and final estimated-capacity band.
> sparse_for_scale
> light_for_scale
> proportionate
> dense_for_scale
> indeterminate
> 7. Worked example
> Example report:
> Evidence memorandum: The site is a wean-to-finish swine operation in central Iowa. Final permit documentation places the operation in the 1,000–1,499 animal-unit range. The retained footprint-based estimate is at least 2,500 animal units; an earlier estimate below 1,500 animal units was withdrawn during footprint review. Two barn structures are confirmed. The confirmed trail contains one permit reference and one parcel reference.
> Correct output:
> priority: elevated_review; route: combined_evidence_review; confidence: medium; capacity_relation: two_bands_above; threshold_transition: stays_permit_scale; record_topology: one_to_one; infrastructure_fit: sparse_for_scale
> The withdrawn estimate is ignored; the final 2,500-plus band controls the target. The estimate sits two bands above the reported band, both bands lie in the permit-scale zone, the one-permit/one-parcel trail is a simple one-to-one linkage, and a two-barn footprint is sparse for a wean-to-finish operation of that estimated scale.
> 8. Submission format
> Submit a CSV file named submission.csv containing exactly these two columns, in this order:
> id
> audit_note
> Example:
> id,audit_note
> test_00000,"priority: routine_review; route: routine_file_check; confidence: high; capacity_relation: same_band; threshold_transition: stays_intermediate; record_topology: one_to_one; infrastructure_fit: proportionate"
> test_00001,"priority: elevated_review; route: combined_evidence_review; confidence: medium; capacity_relation: two_bands_above; threshold_transition: stays_permit_scale; record_topology: one_to_one; infrastructure_fit: sparse_for_scale"
> test_00002,"priority: routine_review; route: record_reconciliation; confidence: medium; capacity_relation: same_band; threshold_transition: stays_permit_scale; record_topology: parcel_fanout; infrastructure_fit: proportionate"
> Every test ID must appear exactly once. A submission receives score 0 when it has missing IDs, additional IDs, duplicate IDs, missing required columns, incorrectly named columns, or an unreadable CSV structure.
> Invalid, missing, duplicate, or unrecognized component declarations inside an audit_note are retained as invalid predictions and scored as incorrect.
> 9. Evaluation
> The metric is the Compositional Evidence Normalization Score.
> For each of the seven components, the grader computes multiclass macro-F1. The following component weights are used identically for both the overall test-set term and the hard-subset term:
> Component Weight capacity_relation 0.18 route 0.16 threshold_transition 0.16 record_topology 0.14 infrastructure_fit 0.14 priority 0.12 confidence 0.10
> The weights sum to 1.00. The weighted component score is the sum of each component's macro-F1 multiplied by its weight.
> The final score is:
> 0.65 × overall weighted component macro-F1
> + 0.20 × hard-subset weighted component macro-F1
> + 0.15 × exact normalized seven-field tuple accuracy
> Hard-subset construction
> A test row belongs to the hard subset when at least one of the following is true:
> its internal review-risk score is at least 4, where that score is deterministically calculated from the seven visible-evidence-derived targets;
> threshold_transition is crosses_500 or crosses_1000;
> record_topology is dual_fanout or asymmetric_complex; or
> infrastructure_fit is sparse_for_scale or dense_for_scale.
> These conditions are fixed before any submission is evaluated. They identify rows involving threshold changes, multi-record structures, infrastructure mismatch, or several simultaneous concerns. The same component weights shown above are used on this subset.
> For the hard-subset term, macro-F1 is averaged over allowed classes that occur in the subset. This ensures that a perfect prediction receives a hard-subset score of 1.0.
> Exact tuple accuracy
> A row counts as an exact match only when all seven parsed component values are correct. Raw text equality is not required; the grader compares normalized parsed fields.
> Scores range from 0 to 1. Higher is better.
> 10. Fairness and preparation guarantees
> Targets are generated exclusively from evidence represented in the public report.
> Raw continuous values are not used after the visible bands are created.
> Identical canonical evidence states always have identical targets.
> A source facility and all its factual or counterfactual packets remain in one split.
> Train and test contain no shared source facilities, canonical evidence states, or exact reports.
> Every atomic target class appearing in test is represented in training.
> The test set evaluates new combinations and discourse structures rather than hidden labels.
> 11. Rules
> A model must be trained inside the submitted solution.
> Pure hardcoded policy tables or manual template parsing are not acceptable.
> External datasets are not permitted.
> Participant-generated synthetic training examples are not permitted.
> Test-set pseudo-labeling, test-distribution calibration, test-based reweighting, and test-time adaptation are not permitted.
> The complete solution must run within the platform time and resource limits.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Informal-to-Formal Theorem Retrieval with Adversarial Local Negatives

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dfda1se8t3gg27xr699q3c18aptn6
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Informal-to-Formal Theorem Retrieval with Adversarial Local Negatives
> Overview
> A mathematician writes "a two-step logical deduction." The formal object they mean is an abstract formula sitting under multiple hypotheses, written entirely in ASCII symbols. The two representations share absolutely zero vocabulary.
> This challenge introduces a novel cross-modal retrieval benchmark testing an AI model's ability to map informal English mathematical prose to rigorous formal symbolic logic. In the ordinary condition of formal mathematics, a library holds tens of thousands of machine-checkable statements written in a custom symbol language, and beside each one a human has written a sentence of English saying what it means. One says "reflexivity"; the other uses a string of symbols denoting an identity axiom. One says "the null set is a subset of any class"; the other uses a symbolic string expressing universal inclusion.
> Given one such English description, your task is to identify which of eight formal statements it describes.
> To elevate this beyond a standard retrieval task, we introduce Adversarial Topological Distractors. The seven wrong candidates are not randomly sampled. They are explicitly drawn from the theorem's immediate topological neighborhood in the underlying foundational logic library. This means all eight candidates are statements about the exact same mathematical sub-topic, written in the identical notation, at the exact same level of abstraction. Telling them apart is not a matter of noticing that one candidate mentions sets and the others do not.
> Lexical retrieval is structurally blind here. Cosine similarity between an English query and a string of formal logic symbols is close to a coin weighted by accident: the query and the answer share, on average, almost no tokens. Whatever connects the symbolic operators to the words "implication" and "antecedent" has to be learned entirely from the training pairs, which is precisely what the 17,400 labelled cases are for.
> No pretrained model is required and none is assumed. The benchmark is designed for CPU: co-occurrence statistics, alignment models, learned embeddings, lexical translation tables, and small classifiers. Solutions have at most 1.5 hours on 10 CPU cores and 62 GB RAM.
> Dataset
> Files
> train.csv - 17,400 labelled cases from 58 library blocks.
> test.csv - 3,982 unlabelled cases from 14 held-out library blocks.
> sample_submission.csv - Placeholder predictions in the exact required schema.
> Input Columns
> ColumnTypeDescriptionidstringOpaque identifier. Unrelated to the answer, the theorem, or split order.querystringOne theorem's English description, written by the library's own authors. Masked before publication (see below). Median length 17 words.c1 through c8stringEight candidate formal statements in symbolic notation, one per column. Exactly one is the statement the query describes.
> A query looks like:
> A specific two-step logical inference rule.
> A candidate looks like:
> OP_ASSERT ( VAR_1 OP_IMPLY ( VAR_2 OP_IMPLY VAR_3 ) ) (Note: Actual strings use a dense, prefix-free ASCII grammar, not these exact placeholder labels).
> The formal notation relies on a custom ASCII grammar: specific prefix tokens denote assertions, binary connectives handle implication and equivalence, and dedicated characters represent quantifiers, set membership, and empty structures. The vocabulary is divided into distinct variable classes: one set of ASCII tokens represents well-formed formulas, while another represents structural classes/sets.
> Target
> answer
> Data type: categorical string
> Description: Which candidate column holds the statement the query describes. One of c1, c2, c3, c4, c5, c6, c7, c8.
> The gold slot is uniformly random by construction: each of the eight slots holds the answer in between 12.1% and 13.3% of test cases, so slot position carries no signal.
> Query Masking
> Each query is the theorem's library comment with three things removed, ensuring that the task cannot be solved by following external bookkeeping:
> Attribution parentheticals (e.g., author names, revision dates, and procedural notes) are deleted, so metadata cannot be exploited.
> Cross-references to other theorems are replaced by the token CITE, so a solver cannot chase the library's pointers to the answer.
> Any occurrence of the theorem's own label becomes the token SELF.
> Leakage Controls
> Only theorems whose formal statement and English description are unique across the whole library are used. The underlying library contains families of variant theorems that share both a conclusion and a gloss; including them would make cases ill-posed rather than hard.
> The split is grouped by position in the library, which tracks its section structure. Whole blocks of neighbouring theorems move together, so a test query's topic neighbours are not sitting in the training set.
> Theorem labels are never published, and id values are salted digests.
> No formal statement is the gold answer of more than one case.
> Evaluation
> Submissions are scored by accuracy: the fraction of test cases whose predicted slot equals the gold slot.
> Python
> score = (predicted_answer == true_answer).mean()
> Minimum score: 0.0
> Maximum score: 1.0 (Higher is better)
> Chance baseline: 0.125. Always answering c1 scores 0.1236.
> Submission Format
> Write the final CSV to ./working/submission.csv. It must contain exactly these columns in exactly this order:
> Code snippet
> id,answer
> 0a1f4c9e2b7d31,c4
> 1b8e07d3aa5c62,c1
> Every test id must appear exactly once. Row order does not matter.
> answer must be one of c1 through c8. Matching is case-insensitive and surrounding whitespace is ignored.
> Missing ids, duplicate ids, or a missing answer column make the submission invalid. An answer outside c1 to c8 is simply counted wrong.
> Extra columns and extra rows are ignored.
> What Not To Use
> Do not infer the target from id, row order, CSV order, or any split artefact.
> Do not match the published queries or candidates against external copies of any foundational formal libraries, their label indices, or search-engine results to recover the original theorem.
> Do not use external formal-library annotations as inference-time inputs.
> Do not adapt models or thresholds using the hidden test labels.
> Learning the correspondence between English and the formal symbolic notation from the supplied training split is the entire point of the task, and every method that does so locally is allowed.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Medieval Charter HTR Error Localisation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70ngyzkbcyf6gkgnjaywzcph8atg7v
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Medieval Charter HTR Error Localisation: Tagging Each Character's Fault
> The problem
> When a handwritten text recognition (HTR) engine reads a medieval charter, it gets some characters right, swaps others for look-alikes, drops some, and runs others together so that a character is missing. Before anyone corrects the line, the useful first question is not what the line should say but where, character by character, the machine went wrong: which characters are sound, which were misread, which have something missing around them, which do not belong. A scholar skims the raw output and, without yet writing the correction, can point at the faults. Producing that per-character fault map is the task.
> This challenge asks a model to write that map out. Given only the noisy transcription of one charter line, expressed as text, generate its error profile: a sequence of tag tokens, one per character in order, each naming what is wrong with that character. The correct reading is never shown. The model reads the noisy characters and produces, in order, a tag for each: K for a correct character, S for a substituted one, I for a character with an insertion needed beside it, and D for a character that should be deleted.
> This is a natural language generation task. The input is text and the output is a token sequence conditioned on that text, one tag aligned to each input character. The model must recognise, from the shapes of the character sequences and the two languages in play, which characters are faithful medieval text and which are recognition errors, and emit the profile in order. Natural approaches are sequence-to-sequence and sequence-labelling methods: a character-level encoder with a per-position tag decoder, or a text-to-text model that reads the line and generates the tag stream. It is generation grounded in reading the language, not a lookup and not a correction.
> What makes this challenge distinct
> The fault of a character is set by its context, not its identity. Whether a given letter is correct or a misreading is not a property of the letter alone. The same character is faithful in one line and a substitution in another, depending on the word it sits in and the characters around it. A model that memorises a typical tag for each character is held to a low ceiling; the rest of the signal only comes from reading the whole line and tagging each position in context.
> Localising faults is not correcting them. The model never produces the clean reading and is never asked to. It does not say what the character should be, only that it is wrong and in what way. This isolates the act of finding and typing errors from the act of fixing them. It is also not a single verdict on the line: rather than labelling a whole line as good or bad, the model must place a tag on every character, so the output is a fault map, not a judgement.
> Text in, tags out. The input is the noisy line and the output is a tag per character. There are no quantities, no clean text, no line-level label. Everything is inferred from reading the noisy characters.
> Line-disjoint split across two languages. The corpus mixes Latin and Middle High German, and no line appears in both the training and test splits. The model must generalise the fault patterns to unseen lines in whichever language they fall, not recognise lines it has seen.
> Imbalanced tags that must all be recovered. Most characters are correct, so K dominates. The S, I, and D tags are the minority, and they carry the signal that matters. The metric weights every tag equally, so a model that only emits K scores poorly. The rare tags are where a good model earns its score.
> Data
> Two comma-separated files, train.csv and test.csv. Because the text contains commas and occasional quotation marks, text fields are quoted in the standard CSV way. The tags field is a space-separated sequence of single-letter tags, one per character of the line, in the same order.
> train.csv gives you the noisy line and its per-character tags so you can learn what each fault looks like:
> Column   Type     Meaning
> ----------------------------------------------------------------------
> id       string   Row identifier
> text     string   Noisy HTR transcription of one charter line (input)
> tags     string   Space-separated tag per character: K, S, I, or D (label)
> A sample train.csv row, with the tag stream aligned under the first characters of the line:
> id,text,tags
> 59,"qua piorum studiorum promiuio et renunrator est dex genae nons spe-","S K I K K K K K K K K ... "
> Here the opening q is a substitution (S), the following u is correct (K), the a has an insertion needed beside it (I), and so on for every character of the line.
> test.csv has the same columns except tags, which is withheld:
> Column   Type     Meaning
> ----------------------------------------------------------------------
> id       string   Row identifier
> text     string   Noisy HTR transcription of one charter line (input)
> A sample test.csv row:
> id,text
> 3,"den nutzen und rechten, die dar zu gehornt, versucht und unversucht"
> Dataset facts:
> Quantity                        Value
> ------------------------------------------------------------------
> Source                          medieval charter HTR output
> Languages                       Latin and Middle High German, mixed
> Training rows                   8,316
> Test rows                       924
> Median line length              about 110 characters
> Tags                            4 (K correct, S substituted, I insertion, D deletion)
> Tag balance                     K about 79%, S about 13%, I about 4%, D about 4%
> Split                           line-disjoint, stratified; no line in both splits
> The tag for each character is read off the canonical minimal edit path between the noisy line and its clean reading, so every target is exact with no alignment heuristics. The clean reading is used only to build the tags and is never released. The content mixes Latin and Middle High German; do not assume a single language. Lines are independent, so each is tagged on its own.
> How a profile is scored
> Each predicted tag stream is aligned to the reference by position: the first tag describes the first character, and so on. Grading compares the tags at every character position and computes a macro-averaged F1 across the four tags. For each tag, precision, recall, and F1 are computed treating that tag as the positive class, and the four F1 scores are averaged with equal weight:
> for each tag in {K, S, I, D}:
> precision = correct predictions of this tag / all predictions of this tag
> recall    = correct predictions of this tag / all reference positions of this tag
> f1        = 2 * precision * recall / (precision + recall)
> score = mean(f1 over the four tags)
> Macro averaging means every tag matters equally regardless of how many characters carry it, so recovering the rare S, I, and D tags is as important as the common K. A predicted tag that is missing, past the end of the sequence, or not one of the four valid tags counts as incorrect at that position. If a prediction is shorter than the reference, the missing positions count as wrong; extra positions past the reference length are ignored.
> Higher is better, in the range 0 to 1. Overall position accuracy is reported alongside for insight but is not the ranking metric.
> Calibration
> Reference points measured on this exact metric frame the leaderboard:
> Strategy                                          Macro-F1
> ------------------------------------------------------------
> Tag every character K (all correct)               about 0.22
> Per-character most-common tag (a lookup)          about 0.30
> The all-K baseline near 0.22 is what you get by declaring every character correct: it captures the common tag and scores zero on the three that matter. The per-character lookup near 0.30 maps each character to its most frequent tag in training and does little better, because whether a character is faithful depends on the line around it, not the character itself. Scores well above 0.30 require a model that reads the whole line and tags each position in context.
> Compute budget
> Your solution must train and produce its submission within the following limits:
> Resource   Limit
> ------------------------------------------------------------
> CPU        10 cores
> RAM        62.5 GB
> Runtime    90 minutes, end to end (training plus inference)
> GPU        none
> The task is designed to fit comfortably on CPU. The corpus is small and the lines are short, so a compact character-level tagger trains in minutes, not the full budget.
> Submission
> Submit a single UTF-8 CSV file with exactly two columns and a header row:
> Column   Type     Meaning
> ------------------------------------------------------------
> id       string   An id from test.csv
> tags     string   Space-separated tag per character of that line, in order
> For each test line, emit one tag per character of its text, in the same order, separated by single spaces. For example, for a line of eight characters:
> id,tags
> 3,K K S K K D K K
> Your file must include the header row and hold one prediction per test id. Rows may appear in any order, since they are joined to the answers on the id column. The provided sample_submission.csv lists every test id with an all-K sequence of the correct length, so it is a valid submission out of the box and shows the exact format the grader expects.
> Rules and allowed methods
> These constraints exist so that scores reflect what a model learned to read, and so that results are reproducible rather than retrieved. They are part of the task definition.
> Tags must be produced by a model that you train and run yourself. Any HuggingFace model or from-scratch architecture trained on the provided training data is permitted: character or byte level models, subword models, sequence taggers, and encoder-decoder or text-to-text architectures. You may engineer features from the line, address tag imbalance with weighting or resampling, cross-validate on the training data, and ensemble your own trained models.
> No TF-IDF or count-based statistical models. TF-IDF, including any sklearn TfidfVectorizer or TfidfTransformer or a hand-rolled equivalent, along with n-gram frequency models, Markov chains, and similar term-frequency or count-based schemes, are not permitted as the means of producing the tags. The profile must be generated by a learned model that reads the line, not assembled from character frequency statistics. The intent is to reward models that read the transcription as structured language rather than leaning on surface counts.
> No recovering the hidden reading. The tags derive from a clean reading that is never released. You may not reconstruct that reading, or the underlying edit path, from any outside source in order to recover the tags. You may not look the lines up against an external manuscript collection or transcription corpus.
> Hosted or closed model APIs are not allowed, because a submission has to be reproducible from your own trained model. Do not call external services, network APIs, or remote models at inference time.
> No external data of any kind. No manuscript corpora, no charter editions, no Latin or Middle High German lexicons, and no external transcription resources. The tags must come from your own model reading the provided line text.
> No hand-tagged entries. Predictions must be generated by the model, not produced by reading the test rows and tagging characters yourself.
> Compute. The solution must respect the compute budget above: 10 CPU cores, 62.5 GB RAM, no GPU, and a 90 minute end-to-end runtime covering both training and inference.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.

## Interleaved Loanword Stream Deconvolution

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79z7g4c0jts3yyps66beq3g58arhds
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Interleaved Loanword Stream Deconvolution
> Domain: Seq2Seq
> Overview
> Each example contains three protected loanword forms from one recipient-language vocabulary. Their glyph streams have been interleaved into one mixed stream while preserving the internal left-to-right order of every hidden form.
> The input supplies:
> one mixed protected-glyph sequence;
> three ordered lexeme slots;
> the target length and number of distinct glyphs for each slot;
> protected concept information and semantic fields;
> an opaque recipient-language code.
> The output is the three original variable-length glyph sequences in lexeme-slot order. This is a constrained sequence deconvolution problem: the output glyphs must collectively use every input glyph occurrence exactly once, and the three outputs must be capable of reproducing the displayed mixed stream through order-preserving interleaving.
> The target is not a row class, candidate ID, donor label, or per-token category. Solvers must generate three complete sequences.
> Number of Rows
> The prepared dataset contains exactly 366 unique sequence examples:
> | Split | File | Rows | Hidden lexeme streams |
> |---|---|---:|---:|
> | Training | train.csv | 271 | 813 |
> | Evaluation | test.csv | 95 | 285 |
> | Total | | 366 | 1,098 |
> Every row contains three output streams. Individual stream lengths range from 2 to 14 protected glyphs.
> sample_submission.csv and the hidden answers mirror the same 95 evaluation IDs and are not additional examples.
> Files
> train.csv — mixed streams and labeled deinterleavings.
> test.csv — mixed streams without target sequences.
> sample_submission.csv — structurally valid example output.
> Input Columns
> id: opaque row identifier.
> prompt: transduction instruction.
> deinterleaving_packet_json: mixed stream, recipient code, and three lexeme-slot descriptors.
> mixed_length: total number of glyph tokens in the mixed stream.
> slot_count: always 3.
> answer_json: training-only output.
> Input JSON Schema
> {
> "recipient_code": "recipient_xxx",
> "mixed_glyph_stream": ["g02", "g07", "g05", "g01", "g03", "g05", "g04"],
> "lexeme_slots": [
> {
> "slot_index": 0,
> "concept_code": "concept_a12",
> "semantic_field": "Food and drink",
> "target_length": 2,
> "unique_glyph_count": 2
> },
> {
> "slot_index": 1,
> "concept_code": "concept_b34",
> "semantic_field": "Animals",
> "target_length": 3,
> "unique_glyph_count": 3
> },
> {
> "slot_index": 2,
> "concept_code": "concept_c56",
> "semantic_field": "The body",
> "target_length": 2,
> "unique_glyph_count": 1
> }
> ]
> }
> Original spellings, language names, source identifiers, and output forms are not exposed directly.
> Output Schema
> answer_json must contain exactly:
> {
> "lexeme_streams": [
> ["g02", "g01"],
> ["g07", "g03", "g04"],
> ["g05", "g05"]
> ]
> }
> The three lists must follow the displayed lexeme_slots order.
> A valid prediction must:
> contain exactly three glyph-token lists;
> match every displayed target_length;
> use the same glyph multiset as mixed_glyph_stream;
> form a valid order-preserving deinterleaving of that mixed stream.
> Submit exactly two CSV columns:
> id,answer_json
> ild_example,"{""lexeme_streams"":[[""g01""],[""g02""],[""g03""]]}"
> Missing, duplicate, unknown, extra, or null row IDs are rejected. Malformed JSON and structurally impossible deinterleavings are rejected.
> Evaluation
> The three streams are flattened with boundary tokens and evaluated using one normalized token-level edit similarity:
> row_score = 1 - edit_distance(predicted_tokens, gold_tokens)
> / max(len(predicted_tokens), len(gold_tokens), 1)
> final_score = mean(row_score)
> For structurally valid submissions, scores range from 0 to 1, and higher is better. Exact deinterleaving receives 1. Invalid or malformed submissions are rejected by the strict grader rather than assigned a normal metric value. The platform grading configuration must therefore use negative infinity as the minimum bound and 1 as the maximum bound. There is no classification accuracy term, set-F1 term, LCS term, candidate-selection term, or weighted metric composition.
> Expected Approaches
> A compliant solution should train a sequence model on train.csv and jointly decode each mixed stream under the three displayed length constraints. Suitable CPU approaches include compact recurrent language models, character-level transformers trained from scratch, neural sequence scorers with beam search, or other learned constrained decoders.
> Prohibited Approaches
> external WOLD lookup, dictionaries, web search, or source reconstruction;
> external datasets, hosted APIs, remote inference, or runtime downloads;
> hardcoded evaluation outputs, manual answer injection, ID maps, or row patches;
> exploiting row order, opaque IDs, or deterministic construction artifacts;
> fitting on test rows, pseudo-labeling, test-time adaptation, or test-distribution calibration;
> TF-IDF at any stage;
> BM25, fixed n-gram overlap, fuzzy matching, or a rule-only main solution;
> a submission script with no genuine task-specific model training on train.csv.
> All task-specific fitting must happen inside the submitted CPU solution using only the public challenge files.

Inspiration note: Useful because it asks for structured sequence reconstruction rather than a single label, giving clear output-shape and metric inspiration.
## Icelandic Treelet Assembly

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73p8reann8yee4c5p00jsc098asqje
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Beat 0n1x's score of 0.750!

### Full Challenge Description

> Icelandic Treelet Assembly
> Overview
> Each row is a compact syntax reconstruction problem from historical Icelandic text. You are given shuffled token cards from one real parsed phrase fragment, a root phrase label, a small inventory of possible phrase labels, and noisy local syntactic clues. Your task is to output the full bracketed phrase-structure tree over the row-local token aliases.
> In plain terms: rebuild the hidden grammar tree for a short Icelandic phrase. This is a structured NLP / sequence-to-tree challenge, not classification, regression, retrieval, or ordinary next-token prediction.
> Train and test examples come from disjoint source documents. Public rows do not include source filenames, sentence IDs, raw text, or lemmas; only POS/morphology, shape clues, and closed-class forms are exposed.
> Task
> Submit predicted_tree, a bracketed tree string.
> A valid tree:
> starts with the given root_label;
> uses every token alias from token_cards exactly once;
> wraps each token alias with its exact POS tag from token_cards;
> uses only labels from label_inventory or POS tags from token_cards;
> has at most 80 nodes and depth at most 12.
> Example tree:
> (PP (P T3) (NP (D-D T1) (N-D T4)) (CP-REL (C T2) (IP-SUB (VBDI T5) (NP-SBJ (PRO-N T6)))))
> Files
> train.csv
> | column | type | description |
> |---|---|---|
> | `id` | string | Anonymous row ID. |
> | `root_label` | string | Root nonterminal label required for the output tree. |
> | `token_cards` | JSON list | Shuffled token cards. Each card has `tok`, `tag`, `coarse_pos`, `morph`, `surface_shape`, `lemma_shape`, and `closed_form`. |
> | `clue_cards` | JSON list | Noisy precedence and same-local-phrase hints. Hints can be incomplete or distracting. |
> | `label_inventory` | string | Space-separated nonterminal labels that may be useful, plus distractors. |
> | `period_bucket` | string | `early`, `middle`, `late`, or `modern`. |
> | `genre_bucket` | string | Coarse source genre bucket. |
> | `leaf_count` | integer | Number of token aliases that must appear exactly once. |
> | `span_count_bucket` | string | `few`, `medium`, or `many`, describing the rough number of internal constituents. |
> | `target_tree` | string | Training-only gold bracketed tree. |
> test.csv has the same columns except target_tree.
> sample_submission.csv
> undefined
> column	type	description
> id	string	Test row ID.
> predicted_tree	string	Your bracketed phrase-structure tree.
> Token card schema
> | field | type | description |
> |---|---|---|
> | `tok` | string | Row-local alias such as `T4`. |
> | `tag` | string | Exact POS/morphology preterminal label that must wrap this alias. |
> | `coarse_pos` | string | Coarse POS prefix from `tag`. |
> | `morph` | string | Morphological suffix from `tag`, if present. |
> | `surface_shape` | string | Coarse vowel/consonant/length shape of the hidden surface word. |
> | `lemma_shape` | string | Coarse vowel/consonant/length shape of the hidden lemma. |
> | `closed_form` | string | Retained function word for common closed-class items; otherwise empty. |
> ## **Clue card schema**
> field	type	description
> kind	string	precedes_near or same_local_phrase.
> left, right	string	For precedes_near, aliases where left is suggested to occur before/near right.
> a, b	string	For same_local_phrase, aliases suggested to belong to a nearby phrase.
> label_hint	string	Coarse phrase-family hint for a same-phrase clue.
> confidence	string	low or medium; present on precedence clues.
> ## **Evaluation**
> Invalid row predictions receive 0 for that row. Structurally invalid submission files are rejected.
> For each valid row:
> - `LabeledSpanF1` is F1 over internal constituents represented as `(label, ordered_aliases_under_that_constituent)`, excluding the root and excluding POS preterminals.
> - `AncestorPairF1` is F1 over `(coarse_label, earlier_alias, later_alias)` triples for alias pairs dominated by the same constituent.
> - `LeafOrderLCS` is the longest common subsequence length between predicted and true alias yields divided by the larger yield length.
> - `AdjacentLinkF1` is F1 over adjacent ordered alias pairs in the predicted and true yields.
> - `ExactTree` is 1 when the complete bracketed tree exactly matches the gold tree after canonical spacing, otherwise 0.
> - `RootLabel` is 1 when the predicted root label equals the required root label, otherwise 0.
> The row score is:
> row_score = 0.30 * LabeledSpanF1
> 0.20 * AncestorPairF1
> 0.20 * LeafOrderLCS
> 0.15 * AdjacentLinkF1
> 0.10 * ExactTree
> 0.05 * RootLabel
> The final score is:
> final_score = mean(row_score over all test rows)
> The score is bounded in `[0, 1]`. The sample submission scores 0. A perfect oracle scores 1.
> ## **Submission format**
> The submission must have exactly two columns in this order:
> column	type	description
> id	string	Test row ID from test.csv.
> predicted_tree	string	Bracketed tree string.
> CSV example:
> id,predicted_tree 0a12bc34de56f789,"(PP (P T3) (NP (D-D T1) (N-D T4)))"
> ## **What not to use**
> Do not use source filenames, sentence IDs, raw source text, row order, or external corpus lookup. These are absent from solver-facing files.
> Do not assume `clue_cards` are a complete parse. They are noisy and contain distractors.
> Do not output JSON, dependency arcs, natural-language explanations, or a flat alias list. The grader expects one bracketed tree string.
> Do not invent token aliases, omit aliases, duplicate aliases, or wrap aliases with the wrong POS tag.
> ## **Benchmark boundary**
> This is not standard constituency parsing from a sentence. The solver does not receive a sentence in word order. It receives shuffled row-local token cards, anonymized lexical shapes, retained closed-class forms, noisy local clues, and a label inventory, then must synthesize a complete phrase-structure tree. The task therefore tests tree assembly under partial syntactic evidence rather than ordinary supervised parsing, sentence ordering, or text retrieval.

Inspiration note: Useful as inspiration for corrupted-clue recovery where the model must identify and repair unreliable evidence.
## Dramatic Referent Route Generation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx713gf9s6r2q4qwe7emk4z4rd8as7rm
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, small-data, Dataset source is visible after the challenge closes.
- Best/top context: Beat caspian's score of 0.634!

### Full Challenge Description

> Dramatic Referent Route Generation
> Overview
> Actors, dramaturgs, and literary NLP systems often need to follow whether a person, object, place, or abstract idea remains active in a dramatic scene after it is mentioned. In this challenge, each example contains a transformed snippet from a public-domain German dramatic text. One annotated referent mention has been replaced by [REF], proper names have been replaced by <NAME>, and the surrounding tokens have been normalized for modeling.
> Your task is to generate a short three-token continuity route for the masked referent. The route describes whether the same referent continues immediately, returns nearby, reappears later, or closes out of the annotated passage; it also records the type of passage where the next mention appears and a coarse sentence-gap bucket.
> This is a CPU-friendly NLP generation task over historical theater text. A strong solution should read the local context, the position of [REF], the dialogue or stage-cue style, and the mention metadata prompt. The task is not solved by looking up source rows, titles, filenames, character names, or external copies of the plays.
> Files
> train.csv contains supervised prompt-answer examples.
> | Column | Type | Description |
> |---|---|---|
> | case_id | string | Anonymized public row identifier. |
> | metadata_prompt | string | Prompt containing the masked dramatic context and compact mention profile. |
> | answer_sequence | string | Three-token target route in the required schema. |
> test.csv contains prompts to solve.
> | Column | Type | Description |
> |---|---|---|
> | case_id | string | Anonymized public row identifier. |
> | metadata_prompt | string | Prompt containing the masked dramatic context and compact mention profile. |
> token_schema.csv lists every valid route token.
> | Column | Type | Description |
> |---|---|---|
> | token | string | Valid schema token that may appear in an answer sequence. |
> | component | string | One of horizon, next_zone, or gap. |
> | description | string | Meaning of the token. |
> sample_submission.csv shows the required submission format.
> | Column | Type | Description |
> |---|---|---|
> | case_id | string | Must match one row from test.csv. |
> | answer_sequence | string | Generated route sequence. |
> Target Route
> For each prompt, output exactly three tokens in this order:
> | Position | Component | Valid Tokens |
> |---|---|---|
> | 1 | horizon | HORIZON_SAME_BEAT, HORIZON_NEAR_HANDOFF, HORIZON_DISTANT_RECALL, HORIZON_CLOSED |
> | 2 | next_zone | NEXT_ZONE_DIALOGUE, NEXT_ZONE_STAGE, NEXT_ZONE_NONE |
> | 3 | gap | GAP_0, GAP_1, GAP_2_3, GAP_4_9, GAP_10_PLUS, GAP_NONE |
> The horizon token captures the broad continuity state of the masked referent. The next_zone token captures whether the next mention is in spoken dialogue, in a stage direction, or absent. The gap token captures the coarse distance to the next mention in sentence or cue units.
> Examples of valid answer sequences:
> | case_id | answer_sequence |
> |---|---|
> | drama_ref_02a7bd9a1874d591c3 | HORIZON_NEAR_HANDOFF NEXT_ZONE_DIALOGUE GAP_2_3 |
> | drama_ref_10ca8ff820b54a0f65 | HORIZON_CLOSED NEXT_ZONE_NONE GAP_NONE |
> | drama_ref_192f747fb0f14d9d9a | HORIZON_DISTANT_RECALL NEXT_ZONE_STAGE GAP_10_PLUS |
> Intended Solution Direction
> Build a local validation split from train.csv and model the prompt as text. Useful CPU approaches include character and word n-gram models, lightweight language-model embeddings computed offline on CPU, compact sequence-generation models, calibrated sparse linear models that generate schema tokens, or ensembles that combine text evidence with parsed mention-profile features.
> Recommended signals:
> | Signal | Why It Helps |
> |---|---|
> | Tokens around [REF] | The wording before and after the masked referent often indicates whether the referent is being introduced, echoed, handed off, or dismissed. |
> | Dialogue versus stage-cue phrasing | Stage directions and spoken dialogue carry referents differently. |
> | Mention profile fields | Span length, POS, number, gender, zone, and sentence position provide compact linguistic evidence. |
> | Character n-grams | Historical spelling, punctuation, and German morphology are informative even after name masking. |
> | Multi-output modeling | The three route components are related but not identical, so predicting them jointly or with reranking can improve score. |
> Disallowed Methods
> Do not use external source-row lookup, original play titles, original character names, source filenames, source document ids, original coreference ids, source row order, or non-public labels.
> Do not retrieve exact source passages from the internet or reconstruct the original annotated corpus rows. Submissions should be generated from the public files provided in the challenge.
> Evaluation
> Submissions are scored from 0 to 1, and higher is better. Each row receives a weighted route score:
> | Component | Weight | What It Rewards |
> |---|---:|---|
> | Exact three-token route | 0.40 | The first three generated schema tokens exactly match the target route. |
> | Ordered component matches | 0.30 | Credit for correct token at position 1, position 2, and position 3. |
> | Schema-token set F1 | 0.20 | Credit for including the correct route tokens even if order is partly wrong. |
> | Valid route format | 0.10 | The first three generated schema tokens follow horizon, next_zone, gap order. |
> The final score is the mean row score across all test prompts. Overlong generated text is truncated during scoring, and malformed route text receives little or no row credit rather than stopping evaluation.
> Submission Format
> Submit a CSV with exactly these columns in this order:
> | Column | Type | Description |
> |---|---|---|
> | case_id | string | Must match one row from test.csv. |
> | answer_sequence | string | Generated route sequence. |
> Example:
> | case_id | answer_sequence |
> |---|---|
> | drama_ref_02a7bd9a1874d591c3 | HORIZON_NEAR_HANDOFF NEXT_ZONE_DIALOGUE GAP_2_3 |
> | drama_ref_10ca8ff820b54a0f65 | HORIZON_CLOSED NEXT_ZONE_NONE GAP_NONE |
> | drama_ref_192f747fb0f14d9d9a | HORIZON_DISTANT_RECALL NEXT_ZONE_STAGE GAP_10_PLUS |
> Requirements:
> Include exactly one row for each test case.
> Do not include duplicate case_id values.
> Do not add extra columns.
> Put the columns in exactly this order: case_id, then answer_sequence.
> Use route tokens from token_schema.csv.

Inspiration note: Useful as inspiration for route/path reconstruction outputs with explicit evidence structure.
## DossierLink: Cross-Page Entity Ledger Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f81hxd7v8zpsyx4jmqsz3hd8azm46
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, small-data, feature-engineering, Dataset source is visible after the challenge closes.
- Best/top context: Be the first to climb the leaderboard!

### Full Challenge Description

> DossierLink: Cross-Page Entity Ledger Recovery
> Overview
> Declassified dossiers often contain repeated people, organizations, places, dates, and facilities across many imperfectly scanned pages. In this challenge, several entity mentions on one page have been redacted. A shuffled roster provides independently damaged alias shapes and OCR context from other pages of the same dossier. Recover which roster entity belongs in every redacted gap.
> This is a sequence-to-sequence cross-page linking task. Submit one variable-length space-separated link program per row, such as g0>e4 g1>e1 g2>e5. Query and roster order are independently shuffled. Every scored entity has a genuine occurrence on the query page and genuine supporting evidence on another page. Single-occurrence entities are excluded. Difficulty comes from organic OCR corruption and deterministic information removal, never random target noise.
> Each card contains type, a coarse len band, a heavily withheld alias fragment sketch, and a protected ctx token stream. len=S, M, or L represents increasing normalized alias length. Alias fragments use a##### codes, + joins multiple visible fragments, and x0 means that every fragment was withheld in that view. w##### values are stable protected OCR tokens. scan_lane is a balanced distractor and has no target meaning.
> The intended first-order approach is to score every gap-roster pair using type, alias compatibility, and cross-page context, then decode one globally consistent assignment rather than choosing each gap independently.
> Evaluation Metric
> For row
> 𝑖
> i, let
> 𝑇
> 𝑖
> T
> i
> ​
> be the true link set and
> 𝑃
> 𝑖
> P
> i
> ​
> the valid parsed prediction.
> 𝑐
> 𝑖
> =
> ∣
> 𝑇
> 𝑖
> ∩
> 𝑃
> 𝑖
> ∣
> c
> i
> ​
> =∣T
> i
> ​
> ∩P
> i
> ​
> ∣.
> Link precision is
> 𝑝
> 𝑖
> =
> 𝑐
> 𝑖
> /
> ∣
> 𝑃
> 𝑖
> ∣
> p
> i
> ​
> =c
> i
> ​
> /∣P
> i
> ​
> ∣ and recall is
> 𝑟
> 𝑖
> =
> 𝑐
> 𝑖
> /
> ∣
> 𝑇
> 𝑖
> ∣
> r
> i
> ​
> =c
> i
> ​
> /∣T
> i
> ​
> ∣.
> Link F1 is
> 𝐹
> 𝑖
> =
> 2
> 𝑝
> 𝑖
> 𝑟
> 𝑖
> /
> (
> 𝑝
> 𝑖
> +
> 𝑟
> 𝑖
> )
> F
> i
> ​
> =2p
> i
> ​
> r
> i
> ​
> /(p
> i
> ​
> +r
> i
> ​
> ). If
> 𝑃
> 𝑖
> P
> i
> ​
> is empty or a denominator is zero,
> 𝐹
> 𝑖
> =
> 0
> F
> i
> ​
> =0.
> Let
> 𝑉
> 𝑖
> V
> i
> ​
> be the set of distinct correct entity cards appearing in correctly predicted links. Entity recovery is
> 𝐸
> 𝑖
> =
> ∣
> 𝑉
> 𝑖
> ∣
> /
> ∣
> {
> 𝑒
> :
> (
> 𝑔
> ,
> 𝑒
> )
> ∈
> 𝑇
> 𝑖
> }
> ∣
> E
> i
> ​
> =∣V
> i
> ​
> ∣/∣{e:(g,e)∈T
> i
> ​
> }∣.
> Exact recovery is
> 𝑋
> 𝑖
> =
> 1
> X
> i
> ​
> =1 if
> 𝑃
> 𝑖
> =
> 𝑇
> 𝑖
> P
> i
> ​
> =T
> i
> ​
> , otherwise
> 𝑋
> 𝑖
> =
> 0
> X
> i
> ​
> =0.
> Row score is
> 𝑅
> 𝑖
> =
> 0.65
> 𝐹
> 𝑖
> +
> 0.20
> 𝐸
> 𝑖
> +
> 0.15
> 𝑋
> 𝑖
> R
> i
> ​
> =0.65F
> i
> ​
> +0.20E
> i
> ​
> +0.15X
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
> 1
> 𝑁
> ∑
> 𝑖
> 𝑅
> 𝑖
> )
> 100×clip
> [0,1]
> ​
> (
> N
> 1
> ​
> ∑
> i
> ​
> R
> i
> ​
> ).
> Malformed rows, repeated gap keys, unknown gaps, and unknown roster entities receive
> 𝑅
> 𝑖
> =
> 0
> R
> i
> ​
> =0. The theoretical minimum is 0. The maximum is 100 and requires the exact complete ledger for every row.
> Measured public-data-only references on the shipped split are:
> Invalid sample submission: 0.000000.
> Context-only constrained decoder: 23.393330.
> Type-plus-context constrained decoder: 38.126696.
> Type, length-band, and context decoder: 51.431231.
> Combined fragment-and-context decoder: 56.789225.
> Learned histogram-gradient assignment model: 58.011668.
> Perfect answers: 100.000000.
> Dataset
> train.csv
> Contains 3,418 labeled rows from 845 source dossiers.
> sample_id - string - content-free identifier in DL############ form.
> query_cards - string - three to five redacted mention cards encoded with the query-card grammar below.
> entity_roster - string - between three and ten shuffled candidate cards encoded with the roster-card grammar below. The roster contains at least one candidate for every gap and may contain same-type, same-length-band distractors.
> scan_lane - string - balanced nuisance code, exactly S0 or S1. It contains no entity-link information.
> target_links - string - complete space-separated one-to-one gap assignment in gK>eJ form.
> query_cards encoding
> query_cards stores cards separated by the exact delimiter || . A query card has this literal structure:
> gK{type=TYPE,len=BAND,alias=MASK,ctx=TOKEN TOKEN ...}
> For example:
> g0{type=PERSON,len=L,alias=a91c2f+a06bd1,ctx=w91a2f w36c10 w04bd9} || g1{type=ORG,len=M,alias=x0,ctx=w42b10 w91a2f}
> gK - local string identifier - gap label, contiguous from g0 through g2, g3, or g4 according to the row's gap count.
> type - categorical string - source entity category. Values are PERSON, ORG, GPE, DATE, NORP, LOC, FAC, or EVENT.
> len - categorical string - normalized alias-length band: S for at most 5 alphanumeric characters, M for 6–10, and L for 11 or more.
> alias - string - unordered fragment sketch derived from the normalized alias. Each visible fragment is encoded as a followed by five lowercase hexadecimal characters. Multiple fragments are joined by +; x0 means no fragment survived in that view. Query and roster fragments are withheld independently. Sketch order and sketch length do not encode original character positions or exact alias length. Shared fragment codes are positive evidence, while different codes are not aligned negative evidence.
> ctx - space-separated string - protected OCR context tokens surrounding the redacted mention on the query page. Every token has the exact form w followed by five lowercase hexadecimal characters, such as w91a2f. The same normalized OCR token always has the same protected value throughout the dataset. Card punctuation is not part of ctx.
> entity_roster encoding
> entity_roster uses the same exact || delimiter. A roster card has this literal structure:
> eJ{type=TYPE,len=BAND,alias=MASK,ctx=TOKEN TOKEN ...}
> For example:
> e0{type=ORG,len=M,alias=a772bc,ctx=w6fa20 w42b10} || e1{type=PERSON,len=L,alias=x0,ctx=w04bd9 w771ce}
> eJ - local string identifier - candidate label, contiguous from e0 through the final roster card. Labels are meaningful only within one row.
> type - categorical string - entity category with the same allowed values as query cards.
> len - categorical string - alias-length band with the same S, M, and L definitions as query cards.
> alias - string - independently withheld unordered fragment sketch for this roster identity. A matching pair can share visible fragment codes, but either view may expose x0 and nonmatching visible fragments do not establish a positional conflict.
> ctx - space-separated string - protected OCR tokens taken from a genuine occurrence on a different page of the same dossier. Tokens use the same stable w##### hexadecimal encoding as query context.
> The two columns are shuffled independently. Card position does not imply a match. Each target uses every query gap exactly once and uses no roster card more than once.
> test.csv
> Contains 1,007 unlabeled rows from 265 source dossiers disjoint from training.
> sample_id - string - content-free identifier in the same format as training.
> query_cards - string - query-card stream with exactly the grammar and sub-fields defined above.
> entity_roster - string - roster-card stream with exactly the grammar and sub-fields defined above.
> scan_lane - string - balanced S0 or S1 nuisance code.
> test.csv contains no target_links column.
> sample_submission.csv
> Contains 1,007 rows.
> sample_id - string - every test identifier exactly once.
> target_links - string - placeholder prediction. The shipped value is INVALID, which intentionally scores zero and does not reveal a target.
> Submission
> Upload exactly 1,007 data rows plus a header with exactly these columns in this order:
> sample_id - string - every test identifier exactly once.
> target_links - string - space-separated links in gK>eJ form.
> Link order does not matter. A roster entity may be used at most once because each card denotes one distinct ledger identity. Extra or reordered columns, duplicate IDs, missing IDs, unknown IDs, and wrong row counts are rejected cleanly. Invalid prediction strings receive the defined worst-case row score without crashing.
> Concrete valid-format examples using real test IDs are:
> sample_id,target_links
> DL0036c145cdfa,g0>e0 g1>e1 g2>e2 g3>e3 g4>e4
> DL00480ce77fcd,g0>e0 g1>e1 g2>e2 g3>e3 g4>e4
> DL00d44f3f463d,g0>e0 g1>e1 g2>e2
> These demonstrate syntax only and are not disclosed answers.
> What Not to Use
> Matching by card position fails because both sides are independently shuffled.
> Entity type alone fails because distractors are selected to match target types whenever available.
> Exact length matching fails because only coarse length bands are exposed and distractors preferentially share the same band.
> Literal-name lookup fails because names and source identifiers are removed and alias characters are independently withheld.
> Independent nearest-neighbor decisions can reuse one roster card and violate the global ledger structure.
> scan_lane is balanced and deliberately unrelated to the target.
> Strong solutions should combine alias-shape compatibility, learned protected-token associations, entity-type evidence, OCR-context similarity, and constrained assignment.

Inspiration note: Useful as inspiration for ledger-style structured outputs that force provenance and consistency.
## Medical Device Recall Event Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73sgv7kn8yxfwjj333b88chx8arex8
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, medical, Dataset source is visible after the challenge closes.
- Best/top context: Beat 0n1x's score of 0.517!

### Full Challenge Description

> Medical Device Recall Event Reconstruction
> 1. Overview and real-world setting
> Regulatory review queues do not arrive one clean record at a time. Product-level recall records reach reviewers in mixed batches: several records from one recall event, several from an unrelated event affecting similar devices, and occasionally a stray record from a third matter. Before any severity or cause assessment can happen, a reviewer must first reconstruct the batch — decide which records describe the same underlying event — and only then grade each reconstructed event.
> This challenge reproduces that workflow as a single structured task. Each row is a redacted docket: four to seven product-level recall records from the same medical specialty panel, drawn from exactly two real recall events (each contributing two or three records), sometimes plus one stray record from a third event. Firm names, brand names, identifiers, dates, and numerals have been removed or pseudonymized, so the records cannot be grouped by superficial metadata. For every docket, the solver must:
> partition the records into their true events;
> assign each reconstructed event its recall hazard class (the regulator's health-hazard determination); and
> assign each reconstructed event its coded root-cause family.
> This is a structured reconstruction task — not classification and not regression. The required output is a variable-size partition of records with per-group evidence grades, so no fixed label space over rows exists. A model that judges records in isolation cannot recover the partition, and a model that clusters by text similarity alone cannot grade the events. The partition ground truth is a physical fact — the hidden recall-event membership of each real record — and the hazard and cause targets are the historical human determinations recorded by regulatory reviewers, so no closed-form rule maps input text to targets.
> 2. Source data and preparation
> The benchmark is prepared from a national medical-device recall register and its associated enforcement determination records, spanning roughly two decades of real recall activity. Every record, event membership, hazard classification, and coded root cause is real; nothing is synthetically generated. The identity of the register is intentionally not disclosed, and the preparation pipeline removes and transforms everything that could match a prepared row back to a source record.
> The preparation pipeline joins each recall record to its enforcement determination, maps the register's coded root causes into eight consolidated families, and redacts the narrative fields. Redaction removes firm and manufacturer names, addresses, contacts, dates, regulatory submission numbers, and recall numbers, and replaces standalone numerals with coarse magnitude bands (NUM_SMALL, NUM_MED, NUM_LARGE). Mixed letter-digit identifiers such as model and catalog codes are replaced by salted, dataset-local pseudonyms of the form MODEL_abcd: the same physical identifier always maps to the same pseudonym inside the benchmark, so identifier co-occurrence across records is usable linkage evidence, but the pseudonyms cannot be reversed or searched against any external source. Sentences stating an assigned recall classification are removed.
> Events are usable when they contribute at least two distinct redacted records and carry uniform hazard and root-cause labels. Records with unknown or undetermined root causes are excluded. Dockets pair each event with a lexically adjacent event from the same specialty panel but a different recalling firm, so the distractor event describes similar devices and failure language — grouping by topic alone is insufficient. Record order within a docket is deterministically shuffled.
> A recall event, and every record of a recalling firm, is assigned entirely to either training or testing, never both. Each event appears in exactly one docket.
> 3. Files and dataset structure
> train.csv — training dockets with three columns:
> id (string): unique docket identifier, e.g. train_00000. Each id appears exactly once.
> docket_json (string): the input docket. Its schema is defined in Section 4.
> docket_gold (string): the target reconstruction. Its schema is defined in Section 5.
> test.csv — evaluation dockets with two columns:
> id (string): unique docket identifier, e.g. test_00000. Each id appears exactly once.
> docket_json (string): the input docket. The corresponding reconstruction must be predicted.
> sample_submission.csv — a valid submission skeleton with two columns:
> id (string): every test id, each exactly once.
> docket_note (string): a syntactically valid placeholder that places all records in one group. Replace it with your predictions.
> The prepared benchmark contains no firm names, recall event numbers, product codes, regulatory submission numbers, dates, or any other field that identifies the source records or the source register. Approximate sizes are 800–1,100 training dockets and 300–450 test dockets; exact counts depend on how many real recall events satisfy the usability constraints, and every usable event in the register is included.
> 4. Structure of docket_json
> docket_json is a JSON object with exactly two keys:
> panel (string): the shared medical specialty panel group of every record in the docket, one of: cardiovascular, orthopedic_physical_medicine, radiology, general_hospital_personal_use, in_vitro_diagnostics, surgery, anesthesiology_respiratory, sensory_dental, neurology, gastro_urology_obgyn. Because all records share the panel, specialty cannot be used to separate the events.
> records (array): four to seven objects, each with:
> rid (string): docket-local record identifier r1, r2, ... in display order (shuffled; order carries no signal);
> packet (string): the redacted narrative with three labeled segments concatenated in fixed order — REASON: (stated reason for recall), PRODUCT: (device description), ACTION: (corrective action). Redaction placeholders such as [FIRM], [LOT], [DATE], NUM_MED, and pseudonyms such as MODEL_kfpb may appear anywhere. A segment may be empty; its label is always present.
> Every docket contains exactly two events of two or three records each, plus at most one stray single-record event. Docket composition (2+2, 2+3, 3+3, with or without a stray) is not disclosed per row; recovering it is part of the task.
> 5. Target docket_note
> For each docket, produce one JSON object with exactly one key, groups: an array of group objects, each with exactly three keys:
> records: an array of rid strings — the records you assign to one event. Every rid in the docket must appear in exactly one group; no rid may be omitted, repeated, or invented.
> hazard: the hazard grade determined for that event after the regulator's health-hazard evaluation, one of:
> hazard_i — reasonable probability of serious adverse health consequences or death;
> hazard_ii — may cause temporary or medically reversible adverse health consequences;
> hazard_iii — not likely to cause adverse health consequences.
> root_cause: the consolidated coded cause family for that event, one of: device_design, software_design, manufacturing_process, material_component, packaging_process, labeling_error, human_error, regulatory_other.
> Group order is irrelevant; the grader aligns predicted groups to true events by record overlap.
> 6. Worked example
> The following illustrates the format and the reasoning, not a rule: the targets are real event memberships and historical determinations, so no deterministic mapping from text to output exists.
> A five-record cardiovascular docket contains: r1 and r4 describing an infusion set whose pseudonymized identifier MODEL_kfpb recurs in both packets, with a REASON describing an under-infusion condition without an alarm; r2 and r5 describing a catheter line with separation of the distal tip during use; and r3 describing a guidewire coating flaking, sharing no pseudonym or failure mechanism with the others. A reasonable reconstruction:
> {"groups": [
> {"records": ["r1", "r4"], "hazard": "hazard_i", "root_cause": "software_design"},
> {"records": ["r2", "r5"], "hazard": "hazard_ii", "root_cause": "device_design"},
> {"records": ["r3"], "hazard": "hazard_ii", "root_cause": "manufacturing_process"}
> ]}
> The shared pseudonym and shared failure mechanism link r1 with r4; the tip-separation narrative links r2 with r5; r3 matches neither and is a stray. Each reconstructed event is then graded from its own records.
> 7. Submission format
> Submit a CSV file named submission.csv containing exactly these two columns, in this order:
> id
> docket_note
> The JSON must be CSV-escaped normally (internal quotes doubled). Example:
> id,docket_note
> test_00000,"{""groups"": [{""records"": [""r1"", ""r3""], ""hazard"": ""hazard_ii"", ""root_cause"": ""device_design""}, {""records"": [""r2"", ""r4"", ""r5""], ""hazard"": ""hazard_i"", ""root_cause"": ""software_design""}]}"
> test_00001,"{""groups"": [{""records"": [""r1"", ""r2""], ""hazard"": ""hazard_iii"", ""root_cause"": ""labeling_error""}, {""records"": [""r3"", ""r4""], ""hazard"": ""hazard_ii"", ""root_cause"": ""material_component""}, {""records"": [""r5""], ""hazard"": ""hazard_ii"", ""root_cause"": ""packaging_process""}]}"
> Every test ID must appear exactly once. A submission receives score 0 when it has missing IDs, additional IDs, duplicate IDs, missing required columns, incorrectly named columns, or an unreadable CSV structure.
> A row-local malformed prediction — invalid JSON, wrong keys, an rid set that does not exactly cover the docket, duplicated rids, or an unrecognized hazard or root-cause value making the group object invalid — scores zero for that row's partition and exact terms and counts every true event in that row as unmatched for the grading terms. It does not crash the grader, and abstaining is never cheaper than answering.
> 8. Evaluation
> The metric is the Docket Reconstruction Score. Four components are computed:
> Partition pair-F1 (weight 0.35). For each docket, consider all unordered record pairs. A pair is positive when both records belong to the same event. Pair-F1 is computed between predicted and true co-membership pairs and averaged over dockets. Putting all records in one group or every record alone both score poorly.
> Root-cause macro-F1 (weight 0.28). Predicted groups are aligned one-to-one to true events greedily by descending record-overlap Jaccard; an alignment requires Jaccard >= 0.5. Over all aligned (true event, predicted group) pairs pooled across the test set — with unaligned true events counted as invalid predictions — multiclass macro-F1 is computed over the eight root-cause families.
> Hazard macro-F1 (weight 0.22). Identically constructed over the three hazard classes.
> Exact docket accuracy (weight 0.15). A docket counts only when the predicted partition exactly equals the true partition and every group's hazard and root cause are correct.
> Score = 0.35 × mean pair-F1
> + 0.28 × pooled root-cause macro-F1
> + 0.22 × pooled hazard macro-F1
> + 0.15 × exact docket accuracy
> Scores range from 0 to 1; higher is better. Measured reference points from the preparation pipeline: the sample submission (all records in one group with constant labels) scores about 0.19; a perfect partition with constant labels scores about 0.40; a perfect submission scores exactly 1.0. Macro averaging over the rare hazard and cause classes means constant-label strategies earn little on the grading terms.
> 9. Fairness and preparation guarantees
> Every partition target is the real hidden event membership of the source records, and every hazard and cause target is a historical reviewer-assigned label; the preparation pipeline generates no labels.
> Events with non-uniform labels or undetermined root causes are excluded.
> A recall event and all records of a recalling firm remain entirely in one split; the two (or three) events inside a docket always come from different firms.
> Each event appears in exactly one docket; no record text appears in more than one docket.
> Identifier pseudonyms are salted per benchmark build and are consistent within the build only.
> Every hazard class and root-cause family appearing in test events is represented among training events, with at least 10 test event-groups per class. Rare classes (notably the lowest-severity hazard grade) have limited natural support in the register; their macro-F1 terms are computed over event-groups pooled across the entire test set.
> 10. Rules
> A model must be trained inside the submitted solution; a substantial part of the final predictor must be genuinely trained or fit on train.csv.
> Solutions must run CPU-only within the platform limits (10 CPU cores, 62 GB RAM, 90 minutes end to end).
> Generic pretrained text encoders available through standard installed libraries are permitted.
> External datasets are not permitted, and models or lookup tables built specifically from any recall, enforcement, or device-safety data source are not permitted.
> Test-set pseudo-labeling, test-distribution calibration, and test-time adaptation are not permitted.
> 11. What not to use
> Do not attempt to identify the source register, and do not query, download, scrape, or reverse-match against any regulatory recall database, enforcement report collection, safety-communication archive, press release, or mirror of them to recover event memberships or classification labels. Source identifiers were removed and narrative identifiers pseudonymized specifically to prevent this; attempting re-identification is a rules violation regardless of whether it succeeds.
> Do not use internet access of any kind during the solution run.
> Do not hardcode per-row answers or build id-keyed lookup tables; ids are opaque and assigned after assembly and shuffling.
> Do not infer targets from record order, docket size alone, id structure, or any other side channel; record order is deterministically shuffled and carries no signal.
> Submissions may be audited for source-lookup code, network access, and rule-only or hardcoded behavior, and may be rejected before payout even when the CSV is structurally valid.
> 12. Benchmark boundary and originality
> This benchmark is not a recall-classification study. The nearest related work, RecallRisk-BERT (Atalay & Yigit-Sert, 2026), performs multi-task severity and root-cause classification over individual regulatory device-recall records, treating each record as an independent classification instance with structured and textual features. Here, single-record classification is neither the task nor sufficient for it: the central object is the docket, the central output is a partition of records into hidden real events, and event grading is scored per reconstructed event through an overlap-based alignment, so a per-record classifier earns partition credit of zero. To the authors' knowledge no existing benchmark poses record-to-event linkage on regulatory recall narratives, under redaction with linkage-preserving pseudonyms, with jointly scored per-event grading. General record-linkage and entity-resolution literature addresses database deduplication with structured keys, and conversation-disentanglement work addresses reply-structure recovery in chat logs; neither provides a reusable solution against this contract of redacted narrative evidence with regulator-adjudicated event labels.

Inspiration note: Useful as inspiration for ledger-style structured outputs that force provenance and consistency.
## CSS Selector DOM Witness Synthesis

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bm6x642493ezaa46edqvh9s8ap6kc
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Be the first to climb the leaderboard!

### Full Challenge Description

> CSS Selector DOM Witness Synthesis
> Overview
> Each row is a small inverse selector problem. You are given anonymous element aliases, allowed tag/class/attribute vocabularies, and several visible CSS selector cards. Each visible card says exactly which aliases it should match. Your task is to submit a JSON DOM tree that explains the visible cards and generalizes to private audit selector cards drawn from the same hidden witness.
> In plain terms: build a tiny HTML-like tree so that the provided selectors select the requested elements and reject the others. This is a sequence-to-structure program-synthesis challenge over web-language semantics, not classification or regression.
> The selector structures are derived from real browser conformance tests, but the challenge rows are anonymous synthetic witness cases. Test witness DOMs and private audit selector cards are not exposed in test.csv. Satisfying the visible cards is necessary, but it is not sufficient for a high private score.
> Task
> Submit predicted_dom, a stringified JSON object with exactly one key, nodes. nodes must contain every row-local element alias exactly once.
> Each node object must have exactly these keys:
> | key | type | description |
> |---|---|---|
> | `id` | string | Element alias from `node_ids`. |
> | `tag` | string | Tag chosen from `allowed_tags`. |
> | `parent` | string | Parent alias, or empty string for the single root. |
> | `classes` | list[string] | Unique class tokens from `allowed_classes`. |
> | `attrs` | object | Attribute-value pairs allowed by `allowed_attributes`. |
> The order of objects in nodes defines sibling order among nodes with the same parent. The submitted graph must be one rooted tree, must be acyclic, and must not exceed max_depth.
> Supported Selector Grammar
> Selectors use a deterministic subset of CSS:
> undefined
> form	meaning
> tag	Match a tag.
> .class	Match an element with a class.
> [attr=value]	Match an exact attribute value.
> A B	Descendant combinator.
> A > B	Child combinator.
> A + B	Adjacent following sibling.
> A ~ B	Later following sibling.
> :not(simple)	Negation of a simple selector.
> :first-child	First child under its parent.
> :last-child	Last child under its parent.
> :nth-child(n)	One-based child position for n from 1 to 5.
> ## **Files**
> `train.csv`
> column	type	description
> id	string	Unique row ID.
> node_ids	JSON list[string]	Element aliases to use exactly once.
> allowed_tags	JSON list[string]	Tags allowed in the submitted DOM.
> allowed_classes	JSON list[string]	Class tokens allowed in the submitted DOM.
> allowed_attributes	JSON object	Attribute names mapped to allowed values.
> selector_cards	JSON list[object]	Five visible selector constraints with card, selector, and must_match.
> constraint_family	string	Main selector family for balancing and subgroup scoring.
> max_depth	integer	Maximum DOM tree depth.
> max_classes_per_node	integer	Maximum classes per node.
> max_attrs_per_node	integer	Maximum attributes per node.
> complexity_budget	integer	Public budget used for compactness after all selector cards are correct.
> target_dom	JSON object	One valid training witness DOM.
> `test.csv` has the same columns except `target_dom`.
> Private scoring also uses eighteen held-out audit selector cards per test row. These audit cards have the same structure as `selector_cards`, but they are not present in solver-facing files. They are selected to cover multiple selector families and to emphasize relation, sibling, position, and negation probes. This is deliberate: a DOM that merely overfits the visible five cards should receive only limited credit.
> ## **Example**
> Selector card:
> {"card":"S1","selector":"section.c2 > .c5","must_match":["E4"]}
> A valid submitted DOM starts like this:
> {"nodes":[ {"id":"E1","tag":"section","parent":"","classes":["c2"],"attrs":{"data-kind":"alpha"}}, {"id":"E4","tag":"span","parent":"E1","classes":["c5"],"attrs":{}} ]}
> The full submission must include every alias in `node_ids`, not only the aliases shown in the example.
> ## **Evaluation**
> Structurally invalid submission files are rejected. A malformed JSON value or invalid DOM receives zero for that row.
> For each row, the grader runs both visible selector cards and private audit selector cards against the submitted DOM.
> `VisibleF1` is the mean F1 score over the visible selector cards, where each card compares the predicted matched alias set with the required `must_match` set.
> `VisibleExact` is the mean exact-match rate over visible selector cards.
> `AuditF1` and `AuditExact` are the same measurements over the private audit selector cards.
> `WholeAuditExact` is 1 if every visible and private audit selector card has the exact required match set, otherwise 0.
> `Compactness` is scored only when `WholeAuditExact = 1`:
> `Compactness = min(1, complexity_budget / submitted_complexity)`
> where submitted complexity is the sum over nodes of:
> `1 + number_of_classes + number_of_attributes`
> The row score is:
> `row_score = 0.05 * VisibleF1 + 0.05 * VisibleExact + 0.35 * AuditF1 + 0.40 * AuditExact + 0.10 * WholeAuditExact + 0.05 * Compactness`
> The final score is:
> `final_score = 0.85 * mean(row_score over all rows) + 0.15 * worst_family_mean`
> `worst_family_mean` is the lowest mean row score among the public `constraint_family` groups. Scores are bounded in `[0, 1]`. The sample submission scores 0. A perfect semantic witness scores 1. Because audit cards are private, participants cannot exactly recompute the hidden test score from `test.csv`; they should use the training `target_dom` rows to estimate how well their synthesis strategy generalizes beyond the visible cards.
> ## **Submission Format**
> The submission must have exactly two columns in this order:
> column	type	description
> id	string	Test row ID from test.csv.
> predicted_dom	stringified JSON	DOM witness object with exactly one key, nodes.
> CSV example:
> id,predicted_dom 0a12bc34de56f789,"{""nodes"":[{""id"":""E1"",""tag"":""div"",""parent"":"""",""classes"":[],""attrs"":{}}]}"
> ## **What Not To Use**
> Do not use row order, hashed IDs, source file names, or external source lookup as shortcuts. They do not encode a witness DOM.
> Do not optimize only for the visible selector cards. They are public evidence, not the whole scoring contract.
> Do not submit browser scripts, HTML files, natural language explanations, XPath, or CSS selectors. Submit only the JSON DOM object.
> Do not include keys other than `nodes` at the top level, and do not invent aliases, tags, classes, attributes, or attribute values outside the row vocabularies.
> ## **Benchmark Boundary**
> This is not ordinary CSS selector matching, web automation selector generation, DOM classification, or HTML repair. The solver is given desired selector outcomes and must synthesize a DOM witness that realizes all of them simultaneously. The hard part is satisfying interacting descendant, child, sibling, negation, positional, class, and attribute constraints under a compact output contract.

Inspiration note: Useful as inspiration for route/path reconstruction outputs with explicit evidence structure.
## Budgeted Wavelength Acquisition For Microscopy Spectrum Completion

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fv0kvkp2y4z0225skq9qdb58aw2h3
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image, multimodal, small-data, feature-engineering, Dataset source is visible after the challenge closes.
- Best/top context: Beat rajpal9955's score of 0.670!

### Full Challenge Description

> Budgeted Wavelength Acquisition for Microscopy Spectrum Completion
> Objective
> Predict the optimal ordered sequence of exactly eight wavelength candidates that minimizes full-spectrum reconstruction error as early as possible.
> A hyperspectral microscope records intensity over many wavelengths. Measuring every wavelength can be slow and storage-intensive, so an acquisition system should decide which wavelength to measure next using the measurements and microscopy context already available.
> Each example represents a synthetic microscopy-spectrum acquisition episode derived from the Detection of Unlabeled Nanoplastics Using Enhanced Dark-Field Hyperspectral Microscopy dataset. The source repository contains extracted pixel spectra and associated microscopy imagery from experimental nanoplastic samples. Preparation uses source-file-disjoint spectra to construct new completion tasks; the generated complete spectra do not occur as complete examples in the source repository.
> For each row, you receive:
> A 96 × 96 × 3 contextual image assembled from three source groups
> Seventeen measured values from an unknown 128-position spectrum
> Sixty-four candidate wavelengths that may be acquired
> You must output eight distinct candidate tokens in acquisition order. After each selected wavelength, the grader reveals its hidden intensity, reconstructs the complete spectrum by piecewise-linear interpolation, and measures reconstruction quality. Earlier selections receive more weight than later selections.
> An example ordered selection is: C07 C42 C18 C55 C03 C31 C60 C24
> Dataset Construction
> The prepared dataset contains:
> 300 training examples
> 180 test examples
> 128 canonical spectral positions per complete spectrum
> 17 initially observed anchor positions
> 64 selectable candidate positions
> 8 required acquisitions per prediction
> 3 vertically stacked context tiles per example
> 5 source-disjoint training validation groups
> Each complete synthetic spectrum is formed from six unique extracted pixel spectra drawn from three experimental source spectrum files. Preparation shifts and nonlinearly transforms the six source spectra, applies deterministic random weights, mixes their contributions, and applies smooth recalibration. Every extracted source pixel spectrum is used at most once. Source-file hashes are disjoint between training and testing.
> Context Image and Incremental Information
> The context image is generated from the same latent source components that produce the hidden spectrum.
> Each of the three 32 × 96 context tiles combines:
> A transformed microscopy crop associated with one source group
> A coarse signed residual signature from that group’s latent spectral contribution
> Coarse derivative and curvature cues
> Real microscopy texture and edge structure
> Mild blur, brightness modulation, and noise
> The residual signature describes spectral structure that is not already represented by linear interpolation through the seventeen anchors. It is coarse and image-like rather than a copy of the 128-point target spectrum.
> Preparation performs source-group-disjoint audits and refuses to produce the dataset unless:
> Context-only features achieve positive grouped residual-spectrum R²
> Anchor-plus-context features improve grouped residual-spectrum R² over anchors alone by at least 0.03
> Direct context-to-spectrum correlation remains bounded, preventing a pixel-level copy of the completed target
> This makes the context useful beyond the anchor values while keeping the task a genuine spectrum-completion and acquisition problem.
> Public Files
> train.csv
> id
> Type: string
> Meaning: Anonymous training-row identifier. It must not be used as a predictive feature.
> input_path
> Type: string
> Meaning: Relative path to the row’s NPZ archive. The path must not be used as a predictive feature.
> group_id
> Type: string
> Meaning: One of five anonymous source-disjoint validation groups. Use it only as a validation splitting key.
> target_selection
> Type: string
> Meaning: Eight-token deterministic greedy-oracle sequence. It is a useful training target, but the grader evaluates reconstruction utility rather than exact sequence agreement.
> test.csv
> id
> Type: string
> Meaning: Anonymous test-row identifier.
> input_path
> Type: string
> Meaning: Relative path to the row’s NPZ archive.
> sample_submission.csv
> id
> Type: string
> Meaning: Test-row identifier.
> selection
> Type: string
> Meaning: A space-separated sequence of exactly eight distinct tokens from C00 through C63, listed in acquisition order.
> inputs/*.npz
> Each training and test row has one compressed NumPy archive.
> context
> Data type: uint8
> Shape: 96 × 96 × 3
> Availability: Training and test
> Meaning: Three vertically stacked microscopy-context tiles containing texture and coarse latent residual cues. Values range from 0 to 255.
> anchor_indices
> Data type: integer
> Shape: 17
> Availability: Training and test
> Meaning: Canonical spectral positions already measured before acquisition begins.
> anchor_values
> Data type: float
> Shape: 17
> Availability: Training and test
> Meaning: Measured intensities at anchor_indices. Values are approximately between 0 and 1.
> candidate_indices
> Data type: integer
> Shape: 64
> Availability: Training and test
> Meaning: Canonical spectral positions corresponding to candidate tokens C00 through C63.
> full_spectrum
> Data type: float
> Shape: 128
> Availability: Training only
> Meaning: Complete synthetic target spectrum. Use it for training, local reconstruction simulation, and policy learning. It is withheld from test archives.
> The fixed anchor positions are:
> 0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 127
> Token C00 refers to candidate_indices[0]. Token C63 refers to candidate_indices[63].
> Group-Aware Validation
> Training source files are partitioned into five persistent groups before examples are created. Every training example draws all three source spectrum files from exactly one group.
> Therefore:
> A source spectrum file cannot appear under more than one group_id
> Holding out one group_id removes every example derived from its source files
> Each group contains many examples
> Group-aware validation more closely represents the source-file-disjoint hidden test split
> Use GroupKFold or leave-one-group-out validation with group_id as the splitting key. Do not use group_id as a predictive input.
> Submission Format
> Create submission.csv with exactly two columns in this order: id,selection
> The selection column must contain a single space-separated string of exactly eight distinct tokens from C00 through C63. The leftmost token is acquired first and the rightmost token is acquired eighth.
> Example rows:
> Q000000,C07 C42 C18 C55 C03 C31 C60 C24
> Q000001,C11 C04 C37 C52 C19 C61 C28 C45
> Q000002,C02 C16 C33 C47 C08 C59 C24 C41
> Submission requirements:
> Every expected test ID must appear exactly once
> No additional IDs are allowed
> No duplicate IDs are allowed
> No additional columns are allowed
> Each selection must contain exactly eight tokens
> All eight tokens must be distinct
> Every token must be between C00 and C63
> Additional text is invalid
> A malformed selection receives row utility 0.
> Evaluation
> The primary metric is Baseline-Calibrated Multi-Budget Reconstruction Utility. Higher scores are better.
> It measures how quickly the selected wavelength sequence reduces curvature-weighted full-spectrum reconstruction error at acquisition budgets of 1, 2, 4, and 8 wavelengths.
> Reconstruction
> For one row and one budget:
> Start with the seventeen anchor indices and values.
> Add the submitted candidate prefix for that budget.
> Reveal the true hidden intensity at each selected candidate.
> Sort all observed positions.
> Reconstruct every unobserved position by one-dimensional piecewise-linear interpolation.
> The anchors include both endpoints of the 128-position grid, so extrapolation is not required.
> Curvature-Weighted Reconstruction Error
> Let s[i] be the hidden complete spectrum.
> curvature[i] = abs(gradient(gradient(s))[i])
> Let q90 be the 90th percentile of the curvature values.
> When q90 is greater than zero:
> weight[i] = 1 + 2 × clip(curvature[i] / q90, 0, 3)
> When q90 is zero, every weight equals 1.
> For reconstructed spectrum r[i]:
> error = sqrt(sum(weight[i] × (r[i] - s[i])²) / sum(weight[i]))
> Oracle-Normalized Utility
> Preparation stores the anchor-only base error and the greedy-oracle reconstruction error at each evaluated budget.
> For budget b:
> utility_b = clip((base_error - submitted_error_b) / (base_error - oracle_error_b), 0, 1)
> When the denominator is numerically zero, utility is 1 only when the submitted error is no greater than the oracle error; otherwise it is 0.
> A sequence can receive full utility without exactly matching the oracle sequence when it achieves equivalent or lower reconstruction error.
> Row Utility
> The evaluated budgets and weights are:
> 1 selected wavelength: weight 0.35
> 2 selected wavelengths: weight 0.30
> 4 selected wavelengths: weight 0.20
> 8 selected wavelengths: weight 0.15
> row_utility = 0.35 × utility_1 + 0.30 × utility_2 + 0.20 × utility_4 + 0.15 × utility_8
> Raw Dataset Score
> raw_score = 0.90 × mean(row_utility) + 0.10 × mean(lowest 25% of row utilities)
> At least one row is included in the lower-tail calculation.
> Transparent Max-Gap Baseline
> The baseline is a fixed max-gap acquisition policy. Starting from the anchors, it repeatedly selects the candidate farthest from the nearest already observed wavelength. Ties prefer the larger containing interval and then the lower wavelength.
> The baseline does not use training targets, the mean training spectrum, hidden test spectra, context images, or fitted parameters.
> Continuous Final Score
> Let baseline_score be the held-out raw score of the max-gap policy. The displayed score assigned to that policy is 0.25.
> When raw_score is less than or equal to baseline_score:
> final_score = 0.25 × raw_score / baseline_score
> When raw_score is greater than baseline_score:
> final_score = 0.25 + 0.75 × (raw_score - baseline_score) / (1 - baseline_score)
> This calibration gives:
> Zero utility: 0
> Fixed max-gap baseline: 0.25
> Perfect per-row oracle utility: 1
> Continuous score separation both below and above the baseline
> Modelling Expectations
> Competitive systems may combine:
> Compact CNN context encoders
> Sparse-anchor multilayer perceptrons
> Residual-spectrum completion models
> Candidate-ranking networks
> Autoregressive acquisition policies
> Pairwise or listwise ranking losses
> Uncertainty and curvature prediction
> Diversity-aware decoding
> Group-aware cross-validation
> CPU ensembles trained within one execution
> At least one genuine learned model must be trained or fine-tuned using the released training examples.
> Runtime Requirements
> Solutions must:
> Run entirely on CPU
> Use at most 10 CPU cores
> Complete within 90 minutes
> Read from ./dataset/public/
> Write ./working/submission.csv
> Perform preprocessing, training, inference, and output generation in one execution
> Process each test row independently
> Prohibited Approaches
> GPU or accelerator use
> External datasets
> Hosted inference APIs
> Public-source matching or hidden-spectrum reconstruction through source lookup
> Using IDs, paths, group IDs, or row order as predictive features
> Challenge-specific weights trained outside the submitted script
> External precomputed embeddings or predictions
> Test-set pseudo-labeling
> Aggregate test-set adaptation
> Cross-test nearest-neighbour matching or clustering
> Allowing one test prediction to depend on another test row
> Accessing withheld preparation artifacts
> Pure rule-only solutions without genuine model training

Inspiration note: Useful for active/budgeted evidence-acquisition challenge designs with reconstruction outputs.
## Spoken Emphasis Consensus Sequencing

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7886fm61r2p1nccgrmd5sxqs8b0r1r
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Beat ismaildos4's score of 0.425!

### Full Challenge Description

> Spoken Emphasis Consensus Sequencing
> Overview
> Spoken emphasis is subjective. Several listeners can hear the same word and disagree about whether it stands out. Your job is to predict one consensus state at every word position: not emphasized N), uncertain because listeners disagree U), or emphasized E). The ordered states form the utterance's contour.
> Each row comes from real English audiobook speech and paid human judgments. The public sequence removes the transcript, word timing, audio stem, speaker identity, and participant identities. Each word position is represented by exactly one opaque token. The preprocessing first selects one of 16 hidden view variants for that word occurrence, then maps the word-view pair into one of 96 shared buckets. Only the resulting bucket token appears in sequence; the other 15 possible views do not appear. Different word-view pairs can map to the same bucket, so repeated words need not have the same token.
> All evaluation speakers are absent from training. A useful solution must transfer prominence patterns to unfamiliar voices and texts while handling the rare E state and the ambiguous U state.
> Reliable consensus contours can support emphasis-controlled speech generation and help prioritize utterances where listener disagreement warrants additional annotation. This benchmark isolates that contour-transfer problem without exposing the original transcript or audio identity.
> Dataset
> File descriptions
> train.csv -- 1,572 utterances from 13 speakers with human-consensus contours.
> test.csv -- 400 utterances from four held-out speakers without contours.
> sample_submission.csv -- The required submission schema populated with deterministic random valid contours.
> Column descriptions
> id (string) -- Unique 16-character hexadecimal utterance identifier.
> speaker_group (string) -- Anonymous speaker identifier for grouped validation. Present only in train.csv.
> sequence (string) -- Space-separated opaque tokens in spoken order, with exactly one token per word position.
> contour (string) -- Space-separated N, U, and E labels, with exactly one label per sequence token. Present in train.csv and required in submissions.
> There are 96 possible token values. Each token has the form xNN, from x00 through x95:
> xNN -- The single bucket assigned to one word occurrence. The hidden preprocessing has 16 possible views per word, but selects only one view for each occurrence before assigning it to a bucket. Many different word-view pairs share a bucket.
> The contour states mean:
> N -- At most one third of listeners marked the word as emphasized.
> U -- Listener support fell between one third and two thirds.
> E -- At least two thirds of listeners marked the word as emphasized.
> Evaluation
> Submissions are scored with Speaker-Balanced Contour Fidelity (SBCF). Higher is better; scores range from 0 to 1.
> For each held-out speaker, the grader computes three components: macro F1 over N, U, and E; mean transition-boundary F1 across that speaker's utterances; and mean squared per-row token accuracy. Macro F1 prevents the frequent N state from dominating. Boundary F1 rewards correct changes between contour states. Squaring each row's token accuracy gives more credit to a mostly correct contour than to the same number of correct labels scattered across weaker rows.
> The four speaker scores receive equal weight:
> row_token_accuracies = []
> for truth, prediction in speaker_utterances:
> correct = sum(t == p for t, p in zip(truth, prediction))
> row_token_accuracies.append(correct / len(truth))
> row_fidelity = mean(
> accuracy * accuracy
> for accuracy in row_token_accuracies
> )
> speaker_score = (
> 0.60 * macro_f1_N_U_E
> + 0.25 * mean_transition_boundary_f1
> + 0.15 * row_fidelity
> )
> SBCF = mean(speaker_score for speaker in held_out_speakers)
> A transition boundary is an index i > 0 where the state at position i differs from the state at position i - 1. Let T be the set of true boundary indices and P the set of predicted boundary indices for one utterance.
> if not T and not P:
> boundary_f1 = 1.0
> elif not T or not P:
> boundary_f1 = 0.0
> else:
> overlap = len(T & P)
> if overlap == 0:
> boundary_f1 = 0.0
> else:
> precision = overlap / len(P)
> recall = overlap / len(T)
> boundary_f1 = 2  *precision*  recall / (precision + recall)
> The first case defines a perfect match when neither contour changes state. The second case assigns zero when only one contour contains transitions. Otherwise, standard set-based F1 compares the predicted and true boundary positions.
> Submission
> Submit one contour for every row in test.csv.
> id (string) -- Exact identifier from test.csv.
> contour (string) -- Space-separated sequence using only N, U, and E.
> Example:
> id,contour
> 008d23ebd993a1f7,E N U N N N N N E U N U N N N N N N U N U U E N N
> 01200eceffc76d04,U N N U N N N U N U U N N N N N N N N N N
> Requirements
> The file must contain exactly 400 data rows, one for every test ID.
> Columns must be exactly id,contour in that order.
> IDs must be unique and match test.csv exactly.
> Every contour token must be N, U, or E.
> Each contour must contain exactly one label per token in that row's sequence.
> Contours may contain at most 48 labels.
> Missing values and empty contours are invalid.
> File format: UTF-8 CSV.
> What not to use
> Do not use external resources to reverse-map the opaque tokens to words, utterance identities, speakers, or target rows.
> Do not recover test contours from external annotations or alignments.
> Do not hardcode predictions by test ID, sequence fingerprint, row order, or a recovered external key.
> A fixed hand-written state rule without a model trained on train.csv is not a valid solution to this benchmark.

Inspiration note: Useful for ordered trace reconstruction instead of isolated per-item prediction.
## Hidden Binary Stars

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx774jkxk6k3g3hs2fv3brqses8b0tsa
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering, large-scale, Dataset source is visible after the challenge closes.
- Best/top context: Beat monu's score of 0.646!

### Full Challenge Description

> Overview
> This is a sequence-to-sequence spectral decoding task. Each input is a continuum-normalized
> near-infrared flux sequence with 7,514 ordered wavelength positions. The sequence contains the
> blended light of two unresolved stars whose absorption patterns overlap and are shifted relative
> to one another.
> For every input sequence, produce an ordered output sequence of exactly eight tokens encoding four
> conceptual quantities: the brighter component's three-token atmospheric state, the fainter
> component's three-token atmospheric state, the fainter component's one-token light contribution,
> and the one-token signed velocity separation.
> The output order is fixed:
> primary effective-temperature token;
> primary surface-gravity token;
> primary metallicity token;
> secondary effective-temperature token;
> secondary surface-gravity token;
> secondary metallicity token;
> secondary light-fraction token;
> signed relative-velocity token.
> The primary is always the component contributing more light to the released composite. This
> removes the usual component-swap ambiguity.
> This is not single-star parameter fitting. A successful sequence model must identify two
> overlapping line systems, preserve wavelength order, infer which features move together, and emit
> the eight output symbols in the correct semantic order.
> What The Task Requires
> Solving an item well exercises four related capabilities:
> Long-sequence representation: capture temperature-, gravity-, and metallicity-sensitive
> structure across thousands of ordered flux values.
> Component separation: distinguish the brighter line system from the weaker secondary pattern.
> Sequence alignment: infer the signed displacement between the two systems while respecting
> detector gaps and missing intervals.
> Ordered decoding: emit eight valid vocabulary tokens in exactly the documented order.
> Data Provenance
> The challenge examples are derived composite observations prepared from a licensed astronomical
> source collection. Full attribution and license information are maintained on the associated
> source-dataset record.
> Source identifiers, sky coordinates, timestamps, field names, telescope metadata, and original
> component spectra are absent from participant files. Parent observations are assigned to only one
> side of the split before composites are constructed.
> File Structure
> train.csv - training identifiers, spectrum indices, and target token sequences.
> test.csv - test identifiers and spectrum indices, without target sequences.
> train_spectra.npy - the training input-sequence matrix.
> test_spectra.npy - the test input-sequence matrix.
> wavelength.npy - the shared ordered wavelength positions in Angstrom.
> sample_submission.csv - a correctly formatted token-sequence submission.
> The spectrum matrices have shape (number_of_examples, 7514) and use float16 storage. Convert
> them to float32 during model computation when appropriate.
> The row selected by spectrum_index is the corresponding input sequence. For example, a training
> row whose spectrum_index is 17 uses train_spectra.npy[17].
> Input Sequence
> Each flux row is ordered by wavelength.npy. The sequence spans three detector segments. Gaps
> between segments remain as jumps in the wavelength values rather than artificial samples.
> Composite sequences contain continuum variation, noise, broadened features, and neutral-valued
> missing intervals. Wavelength position is meaningful; randomly permuting the input destroys the
> line geometry needed for decoding.
> Output Vocabulary
> target_sequence contains exactly eight whitespace-separated tokens. Each position has its own
> prefix and an ordinal, zero-padded bin index.
> PTE000 to PTE127 - primary effective temperature, 128 uniform bins from 2,500 to 9,000 K.
> PLG000 to PLG127 - primary log surface gravity, 128 uniform bins from -1.5 to 6.0 dex.
> PMH000 to PMH127 - primary metallicity, 128 uniform bins from -3.0 to 1.0 dex.
> STE000 to STE127 - secondary effective temperature, using the same 128-bin scale.
> SLG000 to SLG127 - secondary log surface gravity, using the same 128-bin scale.
> SMH000 to SMH127 - secondary metallicity, using the same 128-bin scale.
> SFR000 to SFR063 - secondary light fraction, 64 uniform bins from 0.08 to 0.34.
> DRV000 to DRV127 - secondary-minus-primary velocity, 128 uniform bins from -260 to 260 km/s.
> Bin endpoints are inclusive. For a vocabulary with B bins spanning lower value L to upper
> value U, token index k represents L + k * (U - L) / (B - 1).
> Example target sequence:
> PTE043 PLG092 PMH074 STE061 SLG105 SMH069 SFR031 DRV088
> Token prefixes, positions, and capitalization are mandatory.
> Evaluation
> The grader parses each output sequence into eight ordinal token indices. For each position, the
> corpus-level squared token-index error is divided by the error of the optimal constant token for
> that position. The normalized position errors receive these weights:
> primary atmosphere positions: 2/30 each;
> secondary atmosphere positions: 5/30 each;
> secondary light fraction: 3/30;
> signed relative velocity: 6/30.
> For each sequence position j, its ratio is computed separately across all test rows:
> position_ratio_j = sum_rows((predicted_index_row_j - true_index_row_j)^2) / sum_rows((true_index_row_j - mean_true_index_j)^2)
> The final sequence skill is the weighted sum over all eight positions:
> score = 1 - sum_j(position_weight_j * position_ratio_j), for j = 1,...,8
> Higher is better. The score is bounded to [0.001, 1.0]. An exact token sequence scores 1.0,
> while constant sequences sit at the floor. Giving more metric weight to the secondary atmosphere
> ensures that decoding only the brighter line system is insufficient.
> Malformed sequences, missing tokens, wrong prefixes, out-of-range indices, duplicate ids, or an
> incorrect id set receive the minimum score.
> Submission
> Submit a CSV with exactly two columns:
> id, target_sequence
> Provide exactly one row for every id in test.csv. The target_sequence value must contain all
> eight tokens in the documented order.
> Example rows:
> id,target_sequence TE0123ABCDEF,"PTE043 PLG092 PMH074 STE061 SLG105 SMH069 SFR031 DRV088" TE4567ABCDEF,"PTE071 PLG110 PMH096 STE052 SLG084 SMH058 SFR019 DRV034"
> What Not To Use
> Do not treat spectrum_index as a feature; it is only an array lookup key.
> Do not use the opaque id or row order to predict tokens.
> Do not emit physical decimal values directly. The required output is the fixed eight-token
> sequence.
> Do not collapse the input to a single average star. The fainter component's three atmosphere
> tokens carry 15/30 of the total metric weight (and 15/21 of the atmosphere-only weight).
> Do not copy the sample sequence as a prediction strategy; it is only a formatting example.
> Expected Output
> For every test flux sequence, return one valid eight-token output sequence. Strong solutions should
> preserve wavelength order, separate the two shifted line systems, and decode all eight positions
> rather than only the brighter component.

Inspiration note: Useful for provenance-ledger tasks where every fragment must be linked and justified.
## Masked Helioseismic Band Energy-Profile Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7b7vmkbfptpr71w7yzrs6f618ax24y
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image, small-data, Dataset source is visible after the challenge closes.
- Best/top context: Beat komilpamar's score of 0.671!

### Full Challenge Description

> Overview
> Solar observatories can lose one helioseismic frequency band while an active region is being reviewed. The remaining diagnostics still report continuum intensity, unsigned magnetic field, and three acoustic bands. Your job is to reconstruct the missing band's six-step fallback-tier profile from those co-timed measurements.
> Each sample contains the most recent 48 hourly observations from one solar active-region window. A blackout removes exactly one acoustic channel. The masked_channel field identifies the lost band, while telemetry contains the other five aligned signals. Predict a six-position fallback-tier sequence for the blackout: one token for each consecutive eight-hour part of the same 48-hour window. Each position is independently chosen from a seven-value vocabulary, Q1 through Q7.
> This is a compact CPU sequence-to-sequence reconstruction task, not an image task, raw-waveform imputation task, or future-event forecast. The useful evidence is the relationship between co-timed sensor paths: relative level, recent motion, and how the visible channels evolve together. The fallback-tier target is never present in public input. The held-out band can differ between regions, but remains unavailable across every released window from the same region.
> At a glance
> Input: 48 hourly values for five visible, aligned telemetry signals.
> Mask: one of B23, B34, B45, or B56.
> Output: a six-position fallback_tier_sequence, with each token drawn from Q1, Q2, Q3, Q4, Q5, Q6, and Q7.
> Runtime: CPU only. Raw telescope maps are not required.
> Fallback-Tier Target
> The output positions are chronological. Token 1 triages hours 0 through 8 of the unavailable band, token 2 triages hours 8 through 16, and token 6 triages hours 40 through 48.
> For each eight-hour slot, the preparation pipeline summarizes the unavailable acoustic power as one of seven ordered fallback tiers. Q1 means the lowest expected energy tier and Q7 the highest. Six cut points, the six boundaries between these seven tiers, are fitted separately for every acoustic channel and slot using training regions only, so the tiers remain comparable despite the bands having different physical scales.
> The mask codes identify acoustic-power frequency bands:
> B23 means 2-3 mHz.
> B34 means 3-4 mHz.
> B45 means 4-5 mHz.
> B56 means 5-6 mHz.
> Train and test regions are disjoint. A test region contributes no training window, and sample_id is an opaque identifier rather than a recoverable source key.
> Evaluation
> Submissions are scored with token-level macro F1 across the seven fallback tiers represented in the hidden answers. Every sample contributes six token positions. Macro averaging gives the rare low and high tiers the same importance as middle tiers.
> For each state, the grader calculates precision and recall over all sample-position pairs. F1 is 2 x precision x recall / (precision + recall). The final score is the unweighted mean of those per-state F1 values. Scores lie between 0 and 1; higher is better.
> Every test sample_id must occur exactly once. Each submitted sequence has six positions, and each position must contain one valid token from the seven-value vocabulary Q1, Q2, Q3, Q4, Q5, Q6, and Q7. Missing IDs, duplicate IDs, unknown tokens, malformed sequences, or missing required columns receive 0.0.
> Dataset
> The released data are compact tabular sequences derived from co-registered solar observations. Before release, each sensor is spatially aggregated into an hourly timeline, centered using a training-set median, scaled using a training-set standard deviation, clipped to [-12, 12], and rounded to four decimals. Raw image arrays, source-region numbers, timestamps, filenames, and paths are not included in the public challenge files.
> train.jsonl and test.jsonl are JSON Lines files. Each record contains sample_id, masked_channel, and telemetry. The telemetry object contains exactly five keys, each mapped to a chronological list of exactly 48 finite floats: continuum, magnetic, and the three acoustic keys other than the masked channel. A training record also contains fallback_tier_sequence, a JSON list of six target tokens. Test records omit that target field.
> The public folder contains:
> train.jsonl - labelled fallback-tier examples from training regions.
> test.jsonl - unlabelled fallback-tier examples from held-out regions.
> sequence_schema.json - signal names, mask codes, token vocabulary, sequence length, and public encoding details.
> sample_submission.csv - one valid placeholder row for each test sample.
> Submission Format
> Write ./working/submission.csv with exactly two columns: sample_id and fallback_tier_sequence.
> sample_id,fallback_tier_sequence
> sw_1ce4ca8e1dfe,Q4 Q5 Q4 Q3 Q4 Q5
> Tokens may be separated by spaces, commas, semicolons, or vertical bars. Row order does not matter. The submission must include every sample_id in test.jsonl exactly once.
> Rules
> Use only the released public data and CPU computation. Do not recover or look up original region numbers, timestamps, file paths, source metadata, external observatory records, or withheld acoustic measurements. Do not hardcode answers from identifiers, file order, hashes, or any recovered source identity.

Inspiration note: Useful for masked evidence completion with physical or semantic consistency constraints.
## Abstract Gap Restoration via Passage Selection and Sentence Ordering

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bk2yyh1easy024x7gnmngzn8az3y0
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, small-data, Dataset source is visible after the challenge closes.
- Best/top context: Beat sayantikalaskar's score of 0.621!

### Full Challenge Description

> A Discourse Restoration Chronicle: Abstract Gap Restoration via Passage Selection and Sentence Ordering
> Overview
> The Last Archive survived a catalog fire, but every damaged abstract lost three adjacent sentences. Recovery teams found four authentic three-sentence strips near each damaged record: one came from the abstract, and three came from other papers in nearby areas of research. The sentences on every strip were detached and shuffled.
> Your job is to identify the correct strip and restore its three sentences in their original order. Each row supplies a title, an abstract containing one three-sentence gap, and twelve candidate sentences. A randomized row-local folio value tells you which three sentences were recovered together, but it does not identify the correct folio or reveal the order inside it.
> This is a structured NLP discourse-restoration challenge. The three decoy folios are authentic adjacent passages selected from topic-, subfield-, or field-neighboring papers. Their source sentences are single-use across the constructed rows. A strong solution must combine passage-level topical fit, both gap boundaries, discourse stage, within-folio coherence, and directional ordering.
> Public text is scrubbed symmetrically to suppress document-identity matching. Tokens appearing in at most 15 eligible source documents become [TERM], and numeric tokens become [NUMBER], in titles, visible abstracts, and candidate sentences alike. Redaction does not depend on which folio is correct and creates no target-specific marker.
> The 5,200 training rows and 2,000 test rows are split by publication-source group. The 2,416 train sources and 837 test sources have zero overlap. Source identifiers are not exposed. Row ids, candidate codes, and folio values are randomized. Candidate codes carry no semantic, temporal, source, display-position, or target information. Folio values encode only the explicit row-local three-sentence grouping.
> Evaluation
> The metric is Ordered Triple Recovery Score. Let the submitted sequence be p = [p1, p2, p3] and the gold sequence be g = [g1, g2, g3]. Four components are computed per row:
> membership = |set(p) intersect set(g)| / 3
> transition = |{(p1,p2), (p2,p3)} intersect {(g1,g2), (g2,g3)}| / 2
> position = (I[p1=g1] + I[p2=g2] + I[p3=g3]) / 3
> exact = I[p=g]
> row_score = 0.45 * membership
> + 0.35 * transition
> + 0.10 * position
> + 0.10 * exact
> final_score = mean(row_score)
> The score is maximized. A perfect score is 1.0 and the worst score is 0.0. Membership supplies partial credit for finding the correct passage, while ordered transitions, exact positions, and exact recovery jointly carry 55% of the score. No sentence slot has a larger gain than another, so multiplying confidence for the first slot cannot dominate the metric.
> This reference implementation states the metric for structurally valid rows:
> import numpy as np
> def evaluate(gold_sequences, predicted_sequences):
> row_scores = []
> for gold, prediction in zip(gold_sequences, predicted_sequences):
> membership = len(set(prediction) & set(gold)) / 3.0
> gold_transitions = {(gold[0], gold[1]), (gold[1], gold[2])}
> predicted_transitions = {
> (prediction[0], prediction[1]),
> (prediction[1], prediction[2]),
> }
> transition = len(gold_transitions & predicted_transitions) / 2.0
> position = sum(a == b for a, b in zip(prediction, gold)) / 3.0
> exact = float(prediction == gold)
> row_scores.append(
> 0.45 * membership
> + 0.35 * transition
> + 0.10 * position
> + 0.10 * exact
> )
> return float(np.mean(row_scores))
> A sequence cell that is missing, non-finite, over 512 characters, not a JSON array, not exactly three distinct strings, or contains a code outside that row's twelve candidates receives a row score of 0. Structural submission errors raise ValueError before scoring.
> Dataset
> The mounted participant data is under ./dataset/public/.
> train.csv contains 5,200 labeled restoration cases.
> id (string): randomized row identifier.
> title (string): globally scrubbed scholarly title.
> fragmented_abstract (string): visible context with exactly one [GAP: THREE ADJACENT SENTENCES] marker.
> candidates (JSON string): twelve objects with randomized code, randomized row-local folio, and authentic scrubbed sentence text. Exactly four folios occur per row and each occurs three times.
> gold_sequence (JSON string): three candidate codes in original sentence order.
> test.csv contains 2,000 unlabeled restoration cases.
> id, title, fragmented_abstract, and candidates have the same meanings as in training.
> sample_submission.csv is a label-free baseline using the first three displayed candidate codes.
> id (string): test row identifier.
> sequence (JSON string): three distinct row-local candidate codes in predicted order.
> Every one of the 7,200 cases has a distinct fragmented abstract and a distinct candidate set. All 86,400 candidate codes are globally unique. Folio values are globally unique per recovered strip and appear exactly three times within one row. The public candidate texts originate from source sentences containing 8 to 80 words before symmetric scrubbing.
> Submission
> Write ./working/submission.csv with exactly two columns named id and sequence, in that order. There must be exactly one row for each of the 2,000 test ids. Each sequence cell must be a JSON array of exactly three distinct candidate codes from that row, ordered as your proposed restoration. The three codes may come from any candidates; the grader does not require them to share a folio.
> This example uses real test ids and candidate codes and demonstrates syntax only. It is the label-free displayed-order baseline, not a hidden answer:
> id,sequence
> VA52E72AC1DAC699F84FB4,"[""C1BE09CCAF6"",""CA407B76F14"",""C062FD25C0B""]"
> VA00AD335BC5247BCCA47F,"[""C65F892EA27"",""C42E184BAC8"",""C332527CA83""]"
> Requirements
> Use exactly the test id set. Missing, duplicate, foreign, or extra ids raise ValueError.
> Use exactly the columns id,sequence in that order. Renamed, reordered, missing, or extra columns raise ValueError.
> Encode each sequence as a standards-compliant JSON array. Separator-delimited alternatives are not accepted.
> Supply exactly three distinct string codes, using only codes shown in that row's candidates list.
> Missing, non-finite, overlong, malformed, repeated, incomplete, non-string, or foreign-code sequence content receives the worst row score of 0.
> The grader merges by id; CSV row order does not affect the score.
> The complete solution must run with 10 CPU cores and at most 62 GB RAM in 1.5 hours. GPU use is neither required nor permitted.
> What Not to Use
> Do not use pretrained language models, pretrained embeddings, external corpora, external metadata, or data other than ./dataset/public/.
> Do not access the network or download artifacts at runtime.
> Do not infer meaning from row ids, candidate codes, folio bytes, CSV row order, or code formatting. Those values are randomized.
> Do not install packages at runtime.
> These restrictions require harness-side network and filesystem isolation in addition to grader validation.
> Some extra modelling information
> This challenge defines grouped passage-source restoration as a different prediction mechanism.
> Four authentic adjacent passages compete for one interior gap; passage membership is explicit but correctness is hidden; every passage is internally shuffled; and evaluation separately rewards source recovery, directed transitions, exact positions, and exact reconstruction.
> Decoy passages use single-use source sentences, corpus-global symmetric scrubbing removes document-identity tokens without creating a target-dependent marker, and a publication-source holdout measures transfer to unseen venues.
> The research problem is therefore joint passage selection and local discourse reconstruction rather than unconstrained whole-document ordering or ending choice.

Inspiration note: Useful for ordered route/workflow reconstruction outputs with explicit consistency constraints.
## Legal Paragraph Ordering and Discourse State Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73c3jhnd26hm4snc3tbbk9298aze9t
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, small-data, generative, Dataset source is visible after the challenge closes.
- Best/top context: Beat 0n1x's score of 64.005!

### Full Challenge Description

> Legal Paragraph Ordering and Discourse State Recovery
> Overview
> Reconstruct the latent discourse path of shuffled paragraph bundles from real European Portuguese appellate decisions. Each row contains one contiguous passage whose paragraphs have been assigned anonymous q… handles and placed in a deterministic random order. The target restores the original paragraph order and assigns every paragraph its functional discourse state.
> Some long paragraphs retain their beginning and ending around a [MIDDLE_REDACTED] marker. This is lossy observation, not target noise: the scored order and states are the original human-annotated structure. The two rendering styles are equivalent, and render_code is a balanced nuisance feature. All bundles from one source document remain on the same side of the split.
> This is variable-length sequence transduction. The intended first-order approach is to infer a discourse state from each paragraph, use the learned state progression to establish coarse order, and then use cross-paragraph continuity to resolve order inside a state.
> Evaluation Metric
> For row r, let the true handle sequence be Tᵣ = (t₁,…,tₙ) and the submitted sequence be Pᵣ. Every target contains each input handle exactly once.
> Pairwise order accuracy. Let Cᵣ be the number of pairs i < j for which both tᵢ and tⱼ occur in Pᵣ and tᵢ precedes tⱼ. Then Oᵣ = Cᵣ / binom(n,2). A missing handle makes every pair involving it incorrect.
> Adjacency F1. Let A(Tᵣ) = {(tᵢ,tᵢ₊₁) : 1 ≤ i < n} and define A(Pᵣ) analogously. For multisets X and Y, overlap(X,Y) = Σ_z min(c_X(z),c_Y(z)) and F(X,Y) = 2 × overlap(X,Y) / (|X|+|Y|). Then Dᵣ = F(A(Pᵣ),A(Tᵣ)).
> Discourse macro-F1. Align submitted states by handle. For both state-bearing components, a missing or unknown state is replaced by a deterministic wrong valid state, so abstention is never cheaper than an ordinary error. For each active state k, F1ᵣ,k = 2TPᵣ,k / (2TPᵣ,k+FPᵣ,k+FNᵣ,k). Let Sᵣ be the mean of F1ᵣ,k over states having nonzero TP+FP+FN in that row.
> Transition F1. Replace every true adjacent handle pair by its ordered state pair to form G(Tᵣ). Valid submitted adjacent handles with valid states form G(Pᵣ). Then Rᵣ = F(G(Pᵣ),G(Tᵣ)).
> Let Ō, D̄, S̄, and R̄ be the respective means over all 2,148 test rows.
> Score = round(100 × clip(0.35 × Ō + 0.25 × D̄ + 0.20 × S̄ + 0.20 × R̄, 0, 1), 6).
> The theoretical minimum is 0, meaning no credited order, adjacency, state, or transition recovery. The theoretical maximum is 100, requiring every paragraph order and discourse state to be correct. Measured with the shipped public files and grader:
> Empty sample submission — 0.000000
> Display order with the majority REPORT state — 32.481674
> Public-train raw-count linear state decoder in display order — 35.263893
> Public-train raw-count linear states with coarse discourse ordering — 40.400988
> Perfect submission — 100.000000
> The measured ladder uses no TF-IDF. Better systems can improve state induction, paragraph continuity, and joint constrained decoding independently; capable agent runs are expected to spread across approximately 35–65 without any artificial score cap.
> Dataset
> train.csv
> Contains 7,700 labeled bundles.
> sample_id - string - opaque row identifier.
> bundle_text - string - shuffled paragraphs separated by blank lines; each begins with [qNN] or <qNN>.
> bundle_size - integer - number of paragraphs and required output tokens.
> render_code - string - balanced nuisance code r00 or r01 identifying equivalent delimiter styles.
> path_sequence - string - original order as handle:STATE tokens.
> test.csv
> Contains 2,148 rows and only the four query columns listed above. It contains no target column.
> sample_submission.csv
> Contains every required test identifier and an empty path_sequence placeholder.
> state_vocabulary.csv
> state_code - string - one valid uppercase output state.
> meaning - string - original European Portuguese annotation name.
> Valid states are HEAD, REPORT, ISSUE, FACTS, LAW, DECISION, PANEL, DECLARATION, FOOTNOTE, and TITLE.
> Submission
> Submit a CSV containing exactly 2,148 rows and a header. Required columns may be reordered, and unrelated extra columns are ignored.
> sample_id - string - every test identifier exactly once.
> path_sequence - string - exactly bundle_size space-separated qNN:STATE tokens.
> Every input handle must occur exactly once. Handles are case-sensitive. States must use the uppercase vocabulary. Duplicate, missing, or unknown identifiers and an incorrect row count reject the submission. A malformed row receives the worst-case empty prediction for all four components and never crashes the grader.
> Example using a real test identifier:
> sample_id,path_sequence
> 0006d41d0f7dbffb,q03:REPORT q01:REPORT q08:REPORT q04:FACTS q00:FACTS q07:LAW q02:LAW q06:DECISION q05:PANEL
> The example illustrates syntax only and is not the answer for that row.
> What Not to Use
> Treating the row as one class cannot express a variable-length permutation and state path.
> Keeping display order recovers no real chronology because handles and blocks are deterministically shuffled.
> A majority state misses factual, legal, decision, signature, declaration, title, and footnote structure.
> Sorting only by predicted state cannot resolve paragraphs within long report, fact, or law regions.
> render_code identifies equivalent syntax and is deliberately unrelated to the hidden path.
> External document lookup is blocked by opaque identifiers, stripped filenames, removed source offsets, and middle redaction.
> TF-IDF is neither required nor used by the shipped calibration.
> Successful solutions should combine discourse-state inference, cross-paragraph continuity, and constrained sequence decoding. The task and all shipped processing run on CPU.

Inspiration note: Useful for ordered route/workflow reconstruction outputs with explicit consistency constraints.
## Menu Course Order Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77ac3nhrc3z7qxesv278f3fx8az457
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, Dataset source is visible after the challenge closes.
- Best/top context: Be the first to climb the leaderboard!

### Full Challenge Description

> Menu Course Order Reconstruction
> Overview:
> Each example is a single historical dining menu described by the set of dishes it contained, the year it is
> dated, and the venue it came from. The dishes are given to you in a neutral alphabetical order that carries no
> information about how they were actually laid out. Your task is to reconstruct the true top-to-bottom reading
> order in which the dishes were printed on the physical menu. Historical menus follow an implicit culinary
> course grammar: light openers and soups are printed first, then fish, then roasts and main entrees, then
> desserts and pastries, and finally coffee and after-dinner items. Recovering the printed order therefore means
> inferring, from each dish's name alone, where it belongs in the arc of the meal, and doing so even for rare,
> archaic, or foreign-language dishes that may never appear in your training data.
> What you predict: for each menu, a permutation of its dishes giving their reading order from first-printed to
> last-printed.
> Evaluation:
> The metric is menu_order_kendall. For each menu, we compute Kendall's tau rank correlation between the true
> printed order and your predicted order, then clip it below at zero (so an uninformative or reversed guess
> scores 0, not a negative number). The final score is the mean of these per-menu values over all evaluation
> menus. It ranges from 0.0 (no better than an unordered guess) to 1.0 (every menu perfectly ordered). Higher is
> better.
> Dataset:
> train.csv - one row per training menu, with columns:
> id - string - a menu identifier.
> year - string - the four-digit year the menu is dated, or empty if unknown.
> place - string - the venue or place of the menu, or empty if unknown.
> items - string - the menu's dishes in alphabetical order, joined by the separator " || ".
> order - string - the answer for this training menu: a space-separated list of the 1-based positions of the
> items in reading order. The k-th number is the alphabetical index (1 = first item in items, 2 = second,
> and so on) of the dish printed k-th on the menu.
> test.csv - one row per evaluation menu, with columns id, year, place, items (same meaning as above). The order
> column is not provided.
> sample_submission.csv - a valid submission in the required format, with columns id and prediction. It uses the
> identity ordering (1 2 3 ...), i.e. the alphabetical order unchanged, as a placeholder.
> Worked example of the encoding: suppose a menu's items field is
> Assorted Cakes || Broiled Bluefish || Coffee || Green Turtle Soup || Roast Beef
> so the alphabetical indices are Assorted Cakes=1, Broiled Bluefish=2, Coffee=3, Green Turtle Soup=4,
> Roast Beef=5. The true printed order of this meal is Soup, then Fish, then Roast, then Cakes, then Coffee,
> which corresponds to indices 4, 2, 5, 1, 3. So the correct order string is "4 2 5 1 3".
> Submission:
> Submit a CSV with exactly two columns:
> id - string - the menu id, matching test.csv (every test id present exactly once).
> prediction - string - a space-separated permutation of the integers 1..N, where N is the number of items on
> that menu, giving your predicted reading order in the same 1-based alphabetical-index encoding as the order
> column above.
> Example submission rows:
> id,prediction
> menu_000012,4 2 5 1 3
> menu_000037,1 3 2 6 4 5 7 8
> Requirements: include a header row; submit exactly one row per test menu (the row count must equal the number
> of rows in test.csv); each prediction must be a permutation of 1..N for that menu (each position used once).
> Rules:
> The only valid input signal is the content of the dishes themselves (their names) together with the provided
> year and place. You are reconstructing where each dish sits in the meal's course structure from what the dish
> is. The following approaches are not allowed:
> Retrieving, downloading, or consulting the original menu, menu archive, or any external corpus of historical
> menus to look up or recover the true printed order of an evaluation menu, whether by matching the set of
> dish names, the year, the venue, or any other key. Recovering the answer from an outside source instead of
> predicting it defeats the task.
> Hardcoding predictions for specific test menus.
> Using the alphabetical presentation order of items, the id string, or the row order of test.csv as a
> prediction signal; the items are deliberately alphabetized so that presentation carries no order information.
> Using any external service or API to fetch per-menu answers at inference time.
> The intended solution learns the culinary course grammar of historical menus from the training data: it maps a
> dish name to its typical place in the meal (an oyster or consomme early, a sorbet mid-meal, a pastry or coffee
> late) and generalizes that mapping to dishes it has never seen by reading the words in the name. A strong
> baseline is to memorize, for each dish seen in training, its average printed position and order test dishes by
> that average; a good model must beat this by inferring positions for the large tail of rare, once-seen, and
> foreign-language dishes that the memorization baseline has no entry for.
> Pretrained model policy:
> Fine-tuning a publicly available pretrained language model (for example a small BERT- or T5-family text
> encoder) on the provided training menus is allowed, provided the fine-tuning genuinely uses the training data
> and the model is used only to score or order dish names by their inferred course position. Using a model to
> issue external lookups, or to reproduce a memorized menu archive, is not allowed. If a pretrained model can
> reconstruct these orders with near-perfect accuracy without training on the provided menus, train a dish-order
> model from scratch on the training set instead. Real learning here means predicting, from a dish's words
> alone, how early or late in a historical meal that dish would have been served.

Inspiration note: Useful for ordered route/workflow reconstruction outputs with explicit consistency constraints.
## Cymbal Excitation-and-Damping Program Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76j5nk68rxqr0d09947p2rcx8a2rej
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: audio, video, Based on dataset:, University of Oslo FourMs Cymbal Motion Audio And Video Source Files, Download Data
- Best/top context: Be the first to climb the leaderboard!

### Full Challenge Description

> Overview
> Plain language objective: for each short cymbal recording, identify the hits that happened and submit a JSON recipe of the performance.
> A cymbal is a metal percussion instrument that rings when it is struck and can be muted by damping. In these real laboratory recordings, a performer played a suspended cymbal while synchronized camera video, microphone audio, and body-worn inertial motion capture were recorded. Each prepared row is a 2.80 second clip from one take. The public files remove source names, source times, session numbers, and naming-key metadata, but keep the synchronized audio, video, and motion evidence needed for modeling.
> Each test row provides three aligned inputs: an MP4 video clip, a WAV audio clip, and a motion JSON file with two anonymous wrist-motion tracks. Your prediction is one program_json object for the row. A program is a compact performance ledger, not a single label.
> The program has three parts:
> events: an ordered list of cymbal strikes. Each event gives the 0.05 second time bin, the hand when recoverable, the loudness, and whether the strike is open/ringing or damped/muted.
> groups: musical relations over event indices. A group describes the local strike pattern, such as separated short strikes (STACCATO), a close two-strike ornament (FLAM_UP or FLAM_DOWN), repeated rolling strikes (ROLL), a suspended-cymbal attack (SUSPENDED_ATTACK), or rapid repeated tremolo (TREMOLO).
> motion_roles: the identity of the two anonymous motion tracks, namely which track is LEFT_WRIST and which track is RIGHT_WRIST.
> The only scored event action is STRIKE, meaning a hit that starts or reinforces cymbal sound. Damping is represented as OPEN or DAMPED on the strike event. The source data does not contain reliable separate frame-level mute or release contact times, so separate DAMP and RELEASE actions are not part of this challenge.
> This is not whole-clip category prediction. A useful solution must recover the ordered event sequence, timing bins, hand/intensity/damping tokens, group relations, and motion-track role map together. A prediction that only says "tremolo", only counts onsets, or only guesses the motion roles leaves most of the score unused.
> Only CPU solutions are allowed. Submissions must run within 1.5 hours on 10 CPU cores and 62 GB RAM. Practical CPU routes include audio onset features, video frame-difference or optical-flow summaries, wrist-velocity features from the motion JSON, compact tree or sequence models, and constrained JSON decoding trained only from public/train.csv.
> What Not To Do
> Using the approaches below can cause rejection regardless of leaderboard score:
> Do not use external source lookup, media fingerprinting against public archives, source naming-key lookup, filename recovery, or original timestamp matching.
> Do not infer labels from id, row order, file size, path strings, archive paths, file metadata, modification times, or any private files.
> Do not use hidden answers, manual test labeling, hosted APIs, runtime internet retrieval, or pre-baked per-ID submissions.
> Do not reduce the task to whole-clip label prediction, continuous-value prediction, onset-count prediction, or a group-only taxonomy predictor.
> Do not submit malformed JSON, oversized JSON, duplicate IDs, missing rows, extra columns, impossible track-role maps, or event/group references outside the schema.
> Enforcement on invalid approaches: solutions that rely on lookup, private files, remote services, hard-coded IDs, or other banned channels may be rejected before payout even if the CSV parses.
> Evaluation
> Higher is better. Theoretical minimum: 0.0. Theoretical maximum: 1.0. A perfect private-label submission with confidence 1.0 scores exactly 1.0.
> The grader first validates the CSV structure. The submission must have exactly the columns id, program_json, and confidence in that order. The ID set must exactly match the test IDs with no duplicates. confidence must be finite and in [0, 1]. Structural CSV failures raise InvalidSubmissionError. Row-local malformed or oversized program_json receives zero for that row and does not crash the grader.
> Each program_json must be a JSON object with the keys events, groups, and motion_roles. The events list must contain 1 to 28 events sorted by nondecreasing bin. The groups list must contain 1 to 16 group objects. motion_roles must map exactly track_0 and track_1.
> Each event object must contain:
> {"bin":18,"hand":"R","action":"STRIKE","intensity":"MF","damping":"OPEN"}
> Allowed event values:
> bin: integer from 0 to 55; bins are 0.05 seconds over a 2.80 second clip.
> hand: one of L, R, or U; U means the source-derived hand evidence is intentionally ambiguous.
> action: exactly STRIKE.
> intensity: one of P, MF, F, or VAR.
> damping: one of OPEN or DAMPED.
> Intensity tokens mean P for soft, MF for medium, F for loud, and VAR for variable intensity. Hand tokens mean L for left hand, R for right hand, and U for intentionally ambiguous hand evidence.
> Allowed group types are STACCATO, FLAM_UP, FLAM_DOWN, ROLL, SUSPENDED_ATTACK, and TREMOLO. Group members are zero-based indices into the submitted events list. The motion_roles object must map exactly track_0 and track_1 to the two values LEFT_WRIST and RIGHT_WRIST.
> Event matching uses a one-to-one greedy match between predicted and true events. For each candidate pair, dt = abs(pred_bin - true_bin). If dt > 2, the pair score is 0. Otherwise:
> timing = 1.0 when dt <= 1
> timing = 0.5 when dt == 2
> Candidate event pairs then receive:
> event_pair = 0.36 * timing
> + 0.20 * hand_match
> + 0.12 * action_match
> + 0.18 * intensity_match
> + 0.14 * damping_match
> The grader sorts candidate event pairs from high score to low score and matches each predicted event and each true event at most once. Pairs with combined score below 0.36 are not used. Event precision is sum(matched event_pair scores) / number_of_predicted_events. Event recall is sum(matched event_pair scores) / number_of_true_events. event_f1 is the usual F1 from those precision and recall values. Over-predicting or under-predicting events is therefore penalized.
> For each row, the grader also computes:
> group_f1: predicted group members are first mapped through the event matches. A predicted group can match a true group only if the group type is the same. The group-pair score is the Jaccard overlap between mapped predicted members and true members. Greedy precision, recall, and F1 are then computed over group pairs.
> token_score: exact hand, intensity, and damping matches on matched events, divided by 3 * max(number_of_predicted_events, number_of_true_events).
> adjacency_score: for every neighboring pair of true events, credit is 1 if both events are matched, the predicted order is the same, and the predicted bin gap is within two bins of the true gap. The score is the average over true neighboring pairs. If a true row has only one event, this term is 1.
> motion_role_score: the mean exact-match rate for track_0 and track_1, so the value can be 0.0, 0.5, or 1.0.
> calibration: for a schema-valid row, max(0, 1 - abs(confidence - row_score)); for a row with invalid program_json, calibration is 0.
> The row core is:
> row_core = 0.48 * event_f1
> + 0.18 * group_f1
> + 0.12 * token_score
> + 0.08 * adjacency_score
> + 0.14 * motion_role_score
> row_score = row_core ** 1.35
> The final score also includes a private worst-group robustness term. worst_hidden_group_core is the lowest mean row_core over private subgroups from four real axes: technique family, relation type, intensity token, and damping token. These subgroup labels are used only by the grader and are not public columns.
> The final score is:
> final = 0.62 * mean(row_score)
> + 0.16 * worst_hidden_group_core ** 1.20
> + 0.08 * mean(event_f1)
> + 0.06 * mean(group_f1)
> + 0.04 * mean(motion_role_score)
> + 0.04 * mean(calibration)
> The worst-group term rewards solutions that work across different technique, relation, intensity, and damping cases rather than only on the easiest open or single-pattern clips. Confidence cannot add credit to a wrong row; it only rewards calibration after structured program quality is earned.
> Dataset
> All public paths are relative to public/. The prepared dataset contains 56 training rows, 30 test rows, and 86 synchronized clip triples.
> File overview:
> Item	Description
> public/train.csv	labeled rows
> public/test.csv	input rows
> public/audio/*.wav	WAV clips
> public/video/*.mp4	MP4 clips
> public/motion/*.json	motion tracks
> public/sample_submission.csv	template
> public/train.csv: labeled training rows.
> public/test.csv: unlabeled test rows.
> public/audio/*.wav: source-neutral WAV clips.
> public/video/*.mp4: source-neutral MP4 clips.
> public/motion/*.json: anonymous motion tracks.
> public/sample_submission.csv: weak valid template.
> Each WAV is mono 16-bit PCM at 16,000 Hz and 2.80 seconds long. Each MP4 is a source-neutral view of the same 2.80 second performance window. Each motion JSON contains two anonymous wrist tracks sampled at 40 Hz over the same clip clock. Public input rows and paths contain no raw source filenames, original session numbers, original timestamps, naming-key IDs, or archive paths.
> Motion JSON structure:
> {
> "duration_s": 2.8,
> "sample_rate_hz": 40,
> "tracks": {
> "track_0": [[x, y, z], ...],
> "track_1": [[x, y, z], ...]
> }
> }
> duration_s is the row duration in seconds. sample_rate_hz is the motion sampling rate. tracks has exactly track_0 and track_1. Each track is a list of 112 [x, y, z] triples, one sample per 1/40 second. The coordinates are finite row-local motion coordinates in a body-centered frame. The axes are consistent inside a row, but the original left/right wrist names are hidden; predicting that hidden left/right role is part of the task.
> public/train.csv columns:
> Column	Type	Description
> id	string	opaque id
> video_path	string	relative MP4
> audio_path	string	relative WAV
> motion_path	string	motion JSON
> clip_duration_s	float	2.80
> bin_seconds	float	0.05
> n_bins	integer	56
> program_json	JSON string	train target
> label_origin	string	derivation note
> id (string): opaque row id.
> video_path (string): relative MP4 path.
> audio_path (string): relative WAV path.
> motion_path (string): relative motion JSON path.
> clip_duration_s (float): always 2.80.
> bin_seconds (float): always 0.05.
> n_bins (integer): always 56.
> program_json (JSON string): train label.
> label_origin (string): derivation note.
> program_json is the train-only target. The label_origin field is a constant note that labels are derived from synchronized official audio, motion, and take taxonomy; it is not a source ID and does not appear in test.csv.
> public/test.csv columns:
> Column	Type	Description
> id	string	opaque id
> video_path	string	relative MP4
> audio_path	string	relative WAV
> motion_path	string	motion JSON
> clip_duration_s	float	2.80
> bin_seconds	float	0.05
> n_bins	integer	56
> id (string): opaque row id.
> video_path (string): relative MP4 path.
> audio_path (string): relative WAV path.
> motion_path (string): relative motion JSON path.
> clip_duration_s (float): always 2.80.
> bin_seconds (float): always 0.05.
> n_bins (integer): always 56.
> The test input columns are id, video_path, audio_path, motion_path, clip_duration_s, bin_seconds, and n_bins. They have the same meanings as in train, except the train-only program_json and label_origin columns are absent.
> public/sample_submission.csv is a valid weak baseline with the exact submission columns.
> Submission template columns:
> Column	Type	Constraint
> id	string	exact test IDs
> program_json	JSON string	valid program
> confidence	float	finite [0,1]
> id (string): exact test IDs.
> program_json (JSON string): valid program object.
> confidence (float): finite in [0, 1].
> Submission
> Submit ./working/submission.csv with exactly one row per id in public/test.csv. The CSV must have exactly these columns in this order:
> id,program_json,confidence
> Example rows:
> id,program_json,confidence
> cy_0011223344556677,"{""events"":[{""bin"":14,""hand"":""R"",""action"":""STRIKE"",""intensity"":""MF"",""damping"":""OPEN""}],""groups"":[{""type"":""STACCATO"",""members"":[0]}],""motion_roles"":{""track_0"":""LEFT_WRIST"",""track_1"":""RIGHT_WRIST""}}",0.42
> cy_8899aabbccddeeff,"{""events"":[{""bin"":12,""hand"":""L"",""action"":""STRIKE"",""intensity"":""P"",""damping"":""DAMPED""},{""bin"":15,""hand"":""R"",""action"":""STRIKE"",""intensity"":""P"",""damping"":""DAMPED""}],""groups"":[{""type"":""FLAM_DOWN"",""members"":[0,1]}],""motion_roles"":{""track_0"":""RIGHT_WRIST"",""track_1"":""LEFT_WRIST""}}",0.55

Inspiration note: Useful for ordered route/workflow reconstruction outputs with explicit consistency constraints.

## Urdu Unseen-Trigger Rationale Highlighting

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7btkhbyxmfdd1r82gk3qaxex8b48ce
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Content moderators need more than an offensive-language category: they need the exact words that justify intervention while avoiding unnecessary highlighting of surrounding speech. Given a privacy-protected post and its moderation category, predict the contiguous token spans that human annotators selected as evidence for the moderation judgment.
> The dataset was collected with an Urdu language filter and random sampling rather than an offensive-keyword lexicon. Its moderation labels were assigned under the three-level Offensive Language Identification Dataset taxonomy by three Urdu-language experts who were regular Twitter users. They completed a guideline-calibration exercise before annotation; the reported Fleiss agreement coefficient was 0.615.
> The severity field is a categorical moderation stratum, not a numeric measure of increasing intensity. Category 1 is targeted offense toward an individual TIN-IND), 2 is targeted offense toward a group TIN-GRP), 3 is targeted offense toward another target such as an organization, event, or issue TIN-OTH), and 4 is untargeted offensive or profane language UNT). Non-offensive posts are not part of this rationale-highlighting task.
> Account names are replaced by USER, and pictographs are replaced by Emoji, to reduce disclosure of user identity and original content. These placeholders contain no recoverable lexical evidence and are never target tokens. The holdout tests whether a model can recognize previously unseen offensive expressions: every normalized human-marked lexical token belongs to only one split, and rows containing marked tokens assigned to both sides are excluded. Normalized duplicate posts are also kept out of cross-split comparisons.
> Dataset
> File descriptions
> train.csv: 1,420 labeled real Urdu posts with human rationale spans.
> test.csv: 876 real Urdu posts without rationale spans.
> sample_submission.csv: one valid example prediction for every test ID.
> Column descriptions
> id (string): challenge-generated stable row identifier used only to align posts and predictions; it carries no target meaning.
> text (string): privacy-protected Urdu post tokenized by existing whitespace.
> severity (integer): categorical OLID moderation stratum from 1 through 4; the numbers are category codes, not an ordinal intensity scale.
> token_count (integer): number of whitespace tokens in text.
> target_spans (string, train only): human-selected rationale tokens encoded as sorted, non-overlapping, one-based inclusive intervals separated by |; NONE means the human rationale contains no usable lexical token after privacy placeholders are removed.
> Span example
> For the seven-token training text USER گھٹیا انسان دنیا ہی چھوڑ دو, the numbered tokens are USER(1) گھٹیا(2) انسان(3) دنیا(4) ہی(5) چھوڑ(6) دو(7). Its target is 2-3, meaning tokens 2 and 3 form one contiguous rationale span. A target such as 2-3|6-6 would represent two separate spans. NONE represents an empty token set.
> Evaluation
> Submissions are scored with Unseen-Trigger Rationale Utility, a row-macro composite that rewards accurate rationale coverage, precise boundaries, limited collateral highlighting, and usable performance in every moderation category.
> For row i, let T_i be the set of true inclusive token intervals and P_i the set of predicted intervals. For inclusive intervals t=[a,b] and p=[c,d], define IoU(t,p) = max(0, min(b,d)-max(a,c)+1) / (max(b,d)-min(a,c)+1).
> Row boundary utility: For each true span, take the highest IoU with any predicted span, then average over the true spans: B_i = mean_{t in T_i}(max_{p in P_i} IoU(t,p)). If both sets are empty, B_i=1; if exactly one set is empty, B_i=0. The overall boundary utility is B = mean_i(B_i).
> Row token F1: Expand all intervals into binary token masks. For each row, compute F1_i = 2*TP_i / (2*TP_i + FP_i + FN_i). If both masks are empty, F1_i=1; if there is no true-positive token otherwise, F1_i=0. The macro token F1 is F = mean_i(F1_i).
> Row token precision: For each row, compute Prc_i = TP_i / (TP_i + FP_i). An empty prediction receives Prc_i=1 only when the true mask is also empty; otherwise it receives 0. The macro token precision is Prc = mean_i(Prc_i).
> Weakest-category boundary utility: For each moderation category s in {1,2,3,4}, average B_i over rows with severity=s; then take the minimum: W = min_s(mean_{i: severity_i=s}(B_i)). This differs from B, which averages all rows together: W prevents good performance on common categories from hiding failure on a less frequent category.
> The final score is:
> score = 0.35  *B + 0.25*  F + 0.20  *Prc + 0.20*  W
> The score is clipped to [0, 1]; higher is better.
> Submission
> Submit a CSV with:
> id (string): copied exactly from test.csv.
> spans (string): sorted, non-overlapping, one-based inclusive intervals separated by |, or NONE when predicting no rationale token.
> Example:
> id,spans
> u_9553627933b214d,9-9|12-12
> Requirements
> Include exactly 876 data rows, one for every test ID.
> Use the exact column names id,spans.
> Keep every interval within 1..token_count.
> Sort intervals by starting token and do not overlap or repeat them.
> Tokenize only by the whitespace already present in text.
> Use NONE as the entire spans value when predicting an empty rationale; do not combine NONE with intervals.
> Prohibited methods
> Looking up external copies, rationale vectors, or annotator explanations to recover test targets.
> Reconstructing or hardcoding the withheld marked-trigger partition.
> Reverse-mapping challenge IDs to original tweet identifiers.
> Submitting fixed category templates or ID/row-order lookup rules without modeling the text.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Kubernetes Runbook Policy Patch Synthesis

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70vamz009ykacpsvewnm6pp58b4h0f
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> This is a structured-generation and LLM-evaluation challenge about policy-as-code repair.
> For each row, you receive a Kubernetes-like workload object and five natural-language runbook policy cards. Some cards describe real violations in the starting object, while other cards are already satisfied distractors. Your task is to submit a compact JSON patch program that repairs the violated policies without damaging unrelated fields.
> In plain terms: read the workload, read the policy notes, decide which notes are actually failing, and output the JSON operations needed to make the workload pass admission.
> This mirrors a real workflow in Kubernetes admission control. Security and platform teams maintain policy templates that reject unsafe workloads, such as unapproved image registries, missing resource limits, privileged containers, writable secret mounts, or absent health probes. A useful model should not merely label the resource as bad; it should propose an executable remediation.
> The source material is the Open Policy Agent Gatekeeper policy-template library. The benchmark rows are regenerated and anonymized from policy-template themes. Source files do not contain the hidden row IDs, generated resources, prose cards, target patches, or reference repaired resources.
> Important v2 design note: public policy_cards do not contain machine-readable constraint types such as label_equals or image_registry_allowed. They contain prose policy cards. The executable constraints used by the grader are private.
> Dataset files
> train.csv contains:
> id: string. Unique row ID with no semantic meaning.
> resource_card: JSON object string. The starting Kubernetes-like workload object.
> policy_cards: JSON list string. Five public prose policy cards. Some are violated and some are already satisfied.
> allowed_values: JSON object string. Values that submitted patch operations may use.
> repair_memo: string. A row-specific remediation preference note. It gives partial guidance for choosing among multiple valid repairs.
> source_policy_hint: string. Coarse source-derived theme. It is not a source ID and does not identify which cards are violated.
> max_ops: integer. Maximum number of patch operations.
> target_patch: JSON object string. Training-only canonical patch program.
> test.csv has the same columns except target_patch.
> sample_submission.csv contains:
> id: string. Test row ID.
> predicted_patch: string. A dummy JSON patch. The provided sample intentionally scores 0.
> Sample counts:
> Training rows: 4,320.
> Hidden scored test rows: 1,560.
> Private families: six families with 260 hidden rows each.
> Public policy cards per row: five.
> Canonical repair operations per row: usually three, never more than max_ops.
> Public JSON structures
> resource_card is a JSON object with:
> kind: string. Pod or Deployment.
> metadata: object.
> name: string. Row-local resource name.
> namespace: string. Current namespace alias.
> labels: object from string keys to string values.
> spec: object.
> containers: list of container objects.
> volumes: list of volume objects.
> replicas: integer, present only for deployments.
> Each container object has:
> container: string. Row-local alias such as C1 or C2.
> role: string. primary or sidecar.
> image: object with registry, repository, and tag string fields.
> security: object with Boolean fields privileged, run_as_non_root, and allow_privilege_escalation, plus drop_capabilities, a list of strings.
> resources: object with nested requests and limits objects. Resource leaves may include cpu and memory strings.
> ports: list of integers.
> probes: object with readiness and liveness. Each value is either null or an object with path and port.
> mounts: list of objects with volume and read_only.
> Each volume object has:
> volume: string. Row-local alias such as V1.
> type: string. Volume type alias.
> Each public policy card has:
> policy: string. Row-local policy alias such as P1.
> severity: string. One of advisory, standard, important, or blocking.
> policy_text: string. Natural-language policy note. It may mention row-local aliases and allowed values, but it is not a machine-readable constraint object.
> note: string. General instruction reminding solvers to avoid unnecessary edits.
> Public policy cards may describe:
> required metadata labels or namespace scopes;
> image registry or image-tag restrictions;
> container security settings;
> dropped Linux capabilities;
> resource requests and limits;
> volume-type restrictions or read-only mount requirements;
> health-probe requirements;
> deployment replica bands;
> already-satisfied repository or label checks that should be left alone.
> allowed_values is a JSON object with:
> namespaces: list of strings. Namespace aliases allowed in SET_NAMESPACE.
> label_keys: list of strings. Label keys allowed in SET_LABEL.
> label_values: list of strings. Label values allowed in SET_LABEL.
> registries: list of strings. Registry values allowed in SET_IMAGE_REGISTRY.
> safe_tags: list of strings. Image tags allowed in SET_IMAGE_TAG.
> cpu_values: list of strings. CPU values allowed in SET_RESOURCE.
> memory_values: list of strings. Memory values allowed in SET_RESOURCE.
> probe_paths: list of strings. Probe paths allowed in ADD_PROBE.
> volume_types: list of strings. Volume types allowed in SET_VOLUME_TYPE.
> capabilities: list of strings. Capability names allowed in ADD_DROP_CAPABILITY.
> replicas: list of integers. Replica counts allowed in SET_REPLICAS.
> Patch grammar
> Submit one JSON object per row with exactly one key, ops.
> ops is a list of 1 to max_ops operations. Empty operation lists are invalid row predictions and score 0.
> Allowed operations:
> {"op":"SET_LABEL","key":"team","value":"platform-a1b2"}
> {"op":"SET_NAMESPACE","value":"ns-prod"}
> {"op":"SET_IMAGE_REGISTRY","container":"C1","value":"registry.corp.local"}
> {"op":"SET_IMAGE_TAG","container":"C2","value":"stable"}
> {"op":"SET_SECURITY","container":"C1","field":"privileged","value":false}
> {"op":"ADD_DROP_CAPABILITY","container":"C2","capability":"ALL"}
> {"op":"SET_RESOURCE","container":"C1","resource":"limits.cpu","value":"500m"}
> {"op":"SET_VOLUME_TYPE","volume":"V1","value":"emptyDir"}
> {"op":"SET_MOUNT_READONLY","container":"C1","volume":"V2","value":true}
> {"op":"ADD_PROBE","container":"C1","probe":"readiness","path":"/ready","port":8080}
> {"op":"SET_REPLICAS","value":3}
> Rules:
> Do not include keys other than ops at the top level.
> Each operation must have exactly the keys shown for its operation type.
> Operation aliases such as C1 and V2 must appear in the row.
> Operation values must come from allowed_values.
> Duplicate operations are invalid.
> A row prediction with malformed JSON, an unknown alias, an unknown value, an extra operation key, or more than max_ops operations scores 0 for that row.
> Evaluation
> The grader parses your patch, applies it to the starting resource_card, and evaluates the repaired resource against the private copy of the row's policy cards.
> For each valid row:
> PolicyPass is the fraction of policy cards satisfied after applying the patch.
> PolicyPass = passed_policy_cards / total_policy_cards
> TargetChangeF1 compares the scalar leaves changed by your repaired resource against the scalar leaves changed by the private reference repair. It is F1 over exact (json_pointer, value) pairs.
> precision = matching_changed_pairs / predicted_changed_pairs
> recall = matching_changed_pairs / reference_changed_pairs
> TargetChangeF1 = 2 * precision * recall / (precision + recall)
> If either side has no changed pairs, the F1 is 0 unless both are empty.
> ExactPatch is 1 if the normalized submitted operation set exactly equals the canonical target operation set, else 0.
> CollateralPreservation is the fraction of starting scalar leaves that are unchanged and were not changed by the reference repair.
> CollateralPreservation = preserved_unrelated_leaves / unrelated_starting_leaves
> The row score is:
> row_score =
> 0.20 * PolicyPass
> + 0.35 * TargetChangeF1
> + 0.40 * ExactPatch
> + 0.05 * CollateralPreservation
> The hidden rows are balanced across six private policy families:
> metadata scope
> image provenance
> container security
> resource budget
> volume exposure
> runtime health
> Family labels are not present in public files. They are used only for subgroup robustness.
> final_score = 0.88 * mean(row_score over all test rows) + 0.12 * worst_family_mean
> worst_family_mean is the lowest mean row score among the six private policy families.
> The score is finite and bounded in [0, 1]. The sample submission scores 0. A perfect oracle scores 1.
> Participants can validate JSON syntax and operation grammar locally from public files. They cannot exactly reproduce hidden PolicyPass or worst_family_mean because the executable normalized policy constraints are private; public cards are prose renderings of those constraints.
> Submission format
> Submit a CSV with exactly two columns in this order:
> id: string. Test row ID from test.csv.
> predicted_patch: string. JSON object following the patch grammar.
> Example:
> id,predicted_patch
> 0a12bc34de56f789,"{""ops"":[{""op"":""SET_SECURITY"",""container"":""C1"",""field"":""privileged"",""value"":false}]}"
> Rows may appear in any order because the grader aligns by ID.
> What not to use
> Do not use row order, row IDs, fixed container aliases, fixed volume aliases, or fixed policy aliases as signals.
> Do not assume every public policy card is violated. Some cards are intentionally satisfied distractors.
> Do not look for constraint.kind or other machine-readable policy fields in public files; they are intentionally absent.
> Do not submit a generic hardening patch that changes every field. Collateral damage and extra operations reduce the score.
> Do not assume policy satisfaction alone is enough for full credit. Several repairs can satisfy a policy; the benchmark also scores the reference branch shown by training examples.
> Do not invent values outside allowed_values.
> Do not submit Kubernetes YAML, natural-language explanations, shell commands, Python code, or JSON Patch RFC 6902 paths. Use only the operation grammar above.
> Do not use source repository paths or live policy-template lookup. Solver-facing rows are regenerated and anonymized; source files do not contain row targets.
> Benchmark boundary
> This is not Kubernetes object classification, vulnerability detection, static linting, or ordinary JSON repair. A submission must generate executable remediation programs and is scored by running those programs through policy checks, measuring exact repaired-state changes, and penalizing collateral edits.
> Compared with policy-as-code conformance suites, this benchmark asks for learned repair synthesis under row-local aliases and private branch preferences. Compared with program-repair tasks, the execution domain is admission-control policy semantics over structured workload objects rather than source-code compilation.
> Resource limit
> Solutions must run on CPU only, using at most 10 CPU cores, 62 GB RAM, and 1.5 hours.
> Submissions
> 48

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## TraceFuse: Shuffled Factory Trace Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7brb081ajakmgy2gkr5hpk698c3d95
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> TraceFuse: Shuffled Factory Trace Reconstruction
> Problem Domain: Seq2Seq
> Compute Tier: CPU
> Direction: Maximize
> Score Range: 0.0 to 1.0
> Overview
> Smart factories generate dense streams of low-level sensor and actuator measurements while physical processes are executed across multiple cyber-physical stations.
> In TraceFuse, each case contains exactly seven sensor fragments:
> exactly six fragments come from one completed factory-process execution;
> exactly one fragment is a decoy taken from a different execution of the same process family;
> the six genuine fragments have a hidden chronological order; and
> fragment identifiers, station identifiers, and sensor-channel identifiers are local to the current case.
> Your task is to:
> identify the six genuine fragments;
> reconstruct those six genuine fragments from earliest to latest; and
> identify the remaining fragment as the decoy.
> The required output is a structured sequence, making this a Sequence-to-Sequence task.
> Source Data
> The challenge is derived from sensor and process-execution data collected from a Fischertechnik smart-factory research model at the University of St. Gallen.
> The source data contains:
> low-level sensor and actuator measurements sampled at approximately 10 Hz;
> storage-process executions;
> production-process executions;
> Camunda process-instance records; and
> BPMN process models.
> Only completed process executions that fall within the available sensor-log intervals are used.
> Case Construction
> For each challenge case, sensor streams from one completed process execution are aligned onto a common timeline.
> Six chronological fragments are sampled from that execution with unobserved temporal gaps between neighboring fragments.
> A seventh fragment is selected from another execution of the same process family and used as the decoy.
> Before a case is released:
> absolute timestamps are removed;
> original station identities are replaced by case-local identifiers;
> sensor-channel identities are replaced by case-local identifiers;
> numeric measurements are standardized and quantized;
> limited signal corruption and missing observations may be introduced; and
> all seven fragments are shuffled and assigned the local identifiers F0 through F6.
> Identifiers such as F2, S00, and C03 therefore have meaning only inside the current case.
> In particular, fragment identifiers do not encode chronological position. F0 is not necessarily the earliest fragment, and F6 is not necessarily the latest.
> Dataset Files
> The public dataset contains:
> train.csv
> validation.csv
> test.csv
> sample_submission.csv
> metadata.json
> README.md
> train.csv
> Columns:
> case_id
> input_sequence
> target_sequence
> validation.csv
> Columns:
> case_id
> input_sequence
> target_sequence
> test.csv
> Columns:
> case_id
> input_sequence
> The target sequence is hidden for test cases.
> sample_submission.csv
> Columns:
> case_id
> predicted_sequence
> Input Sequence Format
> Each case contains exactly seven locally identified fragments:
> F0 F1 F2 F3 F4 F5 F6
> Each fragment begins and ends with explicit fragment markers.
> For example:
> <F0> ... </F0>
> Inside each fragment, sensor observations use entries of the form:
> S00.C03=0/0/1/X/2/...
> where:
> S00, S01, ... are case-local station identifiers;
> C00, C01, ... are case-local sensor-channel identifiers;
> each integer value is a quantized standardized measurement; and
> X represents a missing or dropped observation.
> For an integer measurement token q, the corresponding standardized value is:
> q Ã— 0.5
> An illustrative fragment may look like this:
> <F2>
> S00.C00=0/0/1/1/X/2
> S00.C01=-1/0/0/1/1/1
> S01.C00=3/3/2/2/2/1
> S01.C04=0/X/0/1/1/1
> </F2>
> Different fragments may contain different subsets of station/channel observations because observations can be missing or dropped.
> The same case-local station and channel identifiers are used consistently within a case.
> Prediction Task
> For each case_id, predict exactly one sequence with the following grammar:
> F? F? F? F? F? F? DECOY F?
> The sequence has exactly eight whitespace-separated tokens.
> Tokens 1 through 6 are the six genuine fragments only, listed in predicted chronological order from earliest to latest.
> Token 7 is the literal token DECOY.
> Token 8 is the predicted decoy fragment.
> The decoy fragment identifier must not appear among the first six tokens.
> Every fragment identifier from F0 through F6 must appear exactly once across the complete prediction: six before DECOY and the remaining one after DECOY.
> Example
> F4 F1 F6 F2 F0 F5 DECOY F3
> This prediction means that the six genuine fragments are predicted to occur chronologically as:
> F4 -> F1 -> F6 -> F2 -> F0 -> F5
> and F3 is predicted to be the decoy.
> Submission Format
> Submit a CSV containing exactly these two columns, in this order:
> case_id
> predicted_sequence
> Example:
> case_id,predicted_sequence
> tes_020cbab980328e,"F4 F1 F6 F2 F0 F5 DECOY F3"
> tes_02bb712df2504d,"F2 F0 F5 F3 F1 F6 DECOY F4"
> For every prediction:
> predicted_sequence must contain exactly 8 whitespace-separated tokens;
> tokens 1 through 6 must contain the six predicted genuine fragments in chronological order;
> token 7 must be exactly DECOY;
> token 8 must contain the predicted decoy fragment;
> the decoy fragment must not appear among tokens 1 through 6;
> F0 through F6 must each appear exactly once across the complete sequence;
> no fragment identifier may be duplicated;
> no fragment identifier may be omitted;
> every required test case_id must appear exactly once;
> duplicate case_id values are invalid; and
> unknown case_id values are invalid.
> Malformed submissions produce a grading error instead of a numeric score.
> Evaluation
> Each valid prediction is scored using three components:
> Exact Position Accuracy â€” 40%
> Directed Adjacency Accuracy â€” 40%
> Decoy Accuracy â€” 20%
> 1. Exact Position Accuracy
> Exact position accuracy measures how many of the six predicted genuine fragments are placed in their correct chronological positions.
> position_accuracy = correct_positions / 6
> For example, suppose the true chronological order of the genuine fragments is:
> F4 F1 F6 F2 F0 F5
> and the predicted genuine order is:
> F4 F1 F2 F6 F0 F5
> Four of the six positions are correct, so:
> position_accuracy = 4 / 6
> 2. Directed Adjacency Accuracy
> A sequence of six genuine fragments contains five directed neighboring links.
> For example:
> F4 -> F1 -> F6 -> F2 -> F0 -> F5
> contains these five true directed links:
> F4 -> F1
> F1 -> F6
> F6 -> F2
> F2 -> F0
> F0 -> F5
> Directed adjacency accuracy is:
> adjacency_accuracy = recovered_true_directed_links / 5
> A directed link is counted as correct only when both fragment identifiers and their direction are correct.
> For example, if F1 -> F6 is a true link, predicting F6 -> F1 does not receive credit for that link.
> Only adjacency relationships among the six fragments placed before DECOY are evaluated.
> 3. Decoy Accuracy
> Decoy accuracy is:
> decoy_accuracy = 1
> when the fragment following DECOY is the true decoy.
> Otherwise:
> decoy_accuracy = 0
> Case Score
> The score for one case is:
> case_score =
> 0.40 * position_accuracy
> + 0.40 * adjacency_accuracy
> + 0.20 * decoy_accuracy
> Each valid case therefore receives a score between 0.0 and 1.0.
> Final Score
> The final challenge score is the mean case score across all graded cases:
> final_score = mean(case_score over all graded cases)
> The theoretical score range is:
> 0.0 to 1.0
> Higher is better.
> A perfect submission scores exactly:
> 1.0
> Notes
> The challenge uses sensor data from a physical smart-factory research model.
> The released cases apply anonymization, fragmentation, signal corruption, missing observations, shuffling, and decoy insertion to create the sequence-reconstruction task.
> The benchmark is designed for the CPU compute tier.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Algorithmic Dual-View Evidence Reconciliation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dt7qz0dkr3cdqssqzr2xe598byqaw
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Algorithmic Dual-View Evidence Reconciliation
> Overview
> Predict the one evidence-supported arithmetic program and answer that reconcile two independently corrupted versions of the same financial calculation. For each case, you must also locate the distinct fault in each version and cite the smallest report-local evidence set that certifies the repair.
> LedgerMend models a forensic calculation audit. An analyst receives two executable calculation traces copied from the same report, but a different operator, numeric operand, or step reference has been altered in each trace. Both traces still run. Comparing them reveals two plausible shared repairs, and both candidate repairs also run successfully, yet they produce different answers. The calculation cannot be recovered from syntax or execution alone; the surrounding narrative statements and table rows must decide which executable interpretation the report actually supports.
> This dataset is an collection of questions, report text, executable arithmetic programs, and answers derived from public company reports. LedgerMend converts those annotations into reconciliation cases. Financial quantities are deterministically rescaled within each report so that the arithmetic relationships remain valid while direct source-record matching is discouraged. Calendar expressions are preserved verbatim: month names, day values, and years are not treated as financial quantities.
> Task
> Each row contains:
> A fintech question.
> Two damaged versions of one arithmetic program, called the left and right views.
> A report identifier used to retrieve relevant rows from evidence_corpus.csv.
> Exactly one semantic token was changed in each view, and the two changes occur at different token positions. Submit:
> the fault type and token index for the left view;
> the fault type and token index for the right view;
> the smallest annotated set of evidence IDs supporting the calculation;
> one repaired program that is exactly one declared edit from each view; and
> the numeric result of executing that program.
> In plain terms, both damaged calculations must be repaired to the same program, and the cited report evidence must justify that repair.
> What Makes The Task Different
> This is not a standard retrieval task followed by answer generation, nor is it conventional program repair with one broken input. Each example couples three decisions that must agree: diagnose two different faults, retrieve a minimal evidence certificate, and reconstruct one executable program. A correct-looking answer without the right program, a valid repair without supporting evidence, or independently plausible repairs that do not reconcile receive only partial credit.
> The ambiguity is deliberate and testable. Comparing the damaged views exposes exactly two one-token shared-repair candidates: the intended program and a counterfactual program carrying both corruptions. Construction retains a row only when both candidates execute successfully and yield different five-decimal answers. As a result, brute-force syntax repair and execution filtering cannot identify the target. The deciding signal lies in how report language grounds quantities, operators, and intermediate references.
> The retrieved evidence acts as a compact audit certificate rather than an unconstrained context dump. Program and answer credit is awarded only when the submitted repair is exactly one declared edit from each damaged view at distinct positions. Extra evidence can improve recall, but any evidence outside the annotated set triggers a nonminimality penalty. The best submission must therefore make one coherent joint prediction, not assemble separately optimized outputs for retrieval, classification, and arithmetic.
> Dataset
> Public Split
> File	Rows	Description
> public/train.csv	1,004	Inputs and complete reconciliation targets.
> public/test.csv	207	Five input columns requiring predictions.
> public/evidence_corpus.csv	27,655	Report-local narrative sentences, rendered table rows, and distractors.
> public/sample_submission.csv	207	Test identifiers and schema-valid placeholder predictions.
> Test contains 17.1% of the 1,211 prepared examples. All examples from the same company-year report, together with connected duplicate annotations, remain in one partition.
> train.csv
> Column	Type	Description
> example_id	string	Opaque reconciliation identifier.
> report_id	string	Opaque key linking the question to its evidence candidates.
> question	string	Financial question whose numeric references were rescaled with its report.
> corrupted_program	string	Executable left view containing one wrong semantic token.
> corrupted_program_b	string	Executable right view containing a different wrong token.
> fault_type	categorical string	Left-view fault: operator_swap, numeric_operand_swap, or reference_swap.
> fault_token_index	integer	Zero-based position of the incorrect left-view semantic token.
> fault_type_b	categorical string	Right-view fault using the same three-value vocabulary.
> fault_token_index_b	integer	Zero-based position of the incorrect right-view semantic token.
> retrieved_evidence_ids	JSON-array string	Exact smallest annotated evidence-ID set.
> repaired_program	string	Canonical program that reconciles the two views.
> answer	decimal string	Executed program result rounded to five decimal places.
> test.csv
> test.csv contains the five string inputs example_id, report_id, question, corrupted_program, and corrupted_program_b. It does not contain the eight prediction columns.
> evidence_corpus.csv
> Column	Type	Description
> report_id	string	Report owning the evidence segment.
> evidence_id	string	Opaque identifier used in submissions.
> evidence_text	string	Narrative sentence or rendered table row. Numeric values use the same report-level rescaling as the question and programs.
> sample_submission.csv
> The file contains exactly the eight submission columns shown below. Fault indices are integers, retrieved_evidence_ids is a JSON-array string, and the remaining fields are strings. Its placeholder programs demonstrate syntax only.
> Program Language
> A program is a comma-separated sequence of binary operations, for example:
> subtract(148.2, 121.6), divide(#0, 121.6)
> Allowed operators are add, subtract, multiply, and divide. Arguments may be decimal or percentage literals, allowed const_* constants, or backward #N references to earlier steps. Every step contributes three semantic tokens in this order: operator, first argument, second argument. Punctuation is not a token.
> For the example above, the token indices are 0 subtract, 1 148.2, 2 121.6, 3 divide, 4 #0, and 5 121.6.
> Evaluation
> The grader computes each component across all test rows:
> Left fault accuracy: fraction of rows where both the left fault type and index are exact.
> Right fault accuracy: fraction where both the right fault type and index are exact.
> Evidence-set F1: ordinary set F1. For each row, precision is the fraction of submitted evidence IDs in the annotated set, recall is the fraction of annotated IDs retrieved, and their harmonic mean is computed. Row F1 values are then averaged.
> Consistent program accuracy: fraction with the exact canonical target program, provided it differs from each damaged view at only its declared index and those two indices are distinct.
> Consistent answer accuracy: fraction where the submitted answer equals both the repaired program's executed result and the target answer, subject to the same consistency requirement.
> Joint reconciliation accuracy: fraction where both faults, the exact evidence set, canonical program, answer, and consistency checks are all correct together.
> Inconsistent reconciliation rate: fraction whose repair is not exactly one declared edit from both views at distinct positions.
> Nonminimal evidence rate: fraction containing at least one submitted evidence ID outside the annotated set.
> The final score in points is:
> 5 * left fault accuracy
> + 5 * right fault accuracy
> + 5 * evidence-set F1
> + 5 * consistent program accuracy
> + 5 * consistent answer accuracy
> + 75 * joint reconciliation accuracy
> - 10 * inconsistent reconciliation rate
> - 5 * nonminimal evidence rate
> No normalization is applied after this formula. A perfect submission scores 100. Structurally invalid submissions receive negative infinity. Valid but completely wrong submissions can score as low as -15. Higher is better.
> The competition score is computed from one submitted file. The five-run recommendation applies only when reporting experiments for a stochastic model: evaluate at least five independently seeded runs and report their mean rather than selecting the best result. A deterministic method needs only one competition submission.
> Submission Format
> example_id,fault_type,fault_token_index,fault_type_b,fault_token_index_b,retrieved_evidence_ids,repaired_program,answer
> LM_000668756AED93EF,numeric_operand_swap,1,operator_swap,0,"[""E_00DD5F8A4ACEE202""]","subtract(145.776, const_100), divide(#0, const_100)",0.45776
> The example is a labeled public training row. Submit exactly one row for every test example_id and no additional columns.
> Not Allowed Methods
> Looking up or reconstructing source answers, programs, annotations, or identifiers.
> Matching supplied text against online copies, published answer tables, or external corpora.
> Internet access, remote APIs, hosted retrieval, or evidence outside the supplied public files.
> Reading answer files, grader internals, platform secrets, or packaging artifacts.
> Manual test labeling, hard-coded example outputs, or repeated grading probes.
> Pretrained models and local symbolic execution are allowed when they use only the supplied public files.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Schema Conditioned SQL Surgery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79xet7txr9xp7crw9c3tw0558c2vf3
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Background
> In real-world database interactions, automated natural-language-to-SQL systems or human developers frequently write SQL queries that are syntactically sound in most parts but miss key filtering conditions, aggregation clauses, or temporal constraints. Traditional text-to-SQL benchmarks evaluate generation from scratch, but query editing and targeted repair ("surgery") are critical capabilities for real-world code assistants and interactive database tools.
> The Schema-Conditioned SQL Surgery task addresses this problem by requiring models to act as SQL surgeons: given a natural language question, a relational database schema, and a "damaged" SQL query containing missing clause placeholders (<HOLE_1> and optionally <HOLE_2>), the model must precisely predict the missing SQL fragments and reconstruct the complete, executable query.
> Overview
> The primary objective is from-scratch schema-conditioned SQL sequence repair.
> Objective: Predict the contents of 1 or 2 typed clause holes (<HOLE_1>, <HOLE_2>) embedded inside a damaged SQL query, and reconstruct the full, correct SQL query string.
> Track: From-scratch sequence repair. Models must be trained and fitted strictly on the supplied public training split (train.csv). External pretrained language model weights, hosted API services, or third-party datasets are prohibited.
> Grounding: All dataset labels are native and source-grounded (derived directly from human-annotated Spider 1.0 benchmarks via deterministic, keyword-aware clause deletion).
> Dataset Info
> The public challenge payload consists of curated tabular files containing JSON-encoded structural inputs and outputs.
> Public Files
> train.csv: Primary training split containing full inputs and gold labels.
> test.csv: Public evaluation set containing inputs only (labels withheld).
> sample_submission.csv: Submission template pre-filled with valid default fallback payloads.
> DATA_MANIFEST.json: Metadata file specifying row counts and primary payload column names.
> Tabular Schemas
> train.csv
> +-------------+--------------+-------------------------------------------------------------------------+
> | Column Name | Data Type    | Description                                                             |
> +-------------+--------------+-------------------------------------------------------------------------+
> | id          | UTF-8 String | Opaque unique identifier for each evaluation record (e.g., sql_a1b2c3). |
> | input_json  | UTF-8 JSON   | Serialized JSON object containing question, schema, and damaged_sql.    |
> | repair_json | UTF-8 JSON   | Target ground truth containing gold hole completions and full SQL text. |
> +-------------+--------------+-------------------------------------------------------------------------+
> test.csv
> +-------------+--------------+-------------------------------------------------------------------------+
> | Column Name | Data Type    | Description                                                             |
> +-------------+--------------+-------------------------------------------------------------------------+
> | id          | UTF-8 String | Opaque unique identifier matching the evaluation test set.             |
> | input_json  | UTF-8 JSON   | Serialized JSON object containing question, schema, and damaged_sql.    |
> +-------------+--------------+-------------------------------------------------------------------------+
> sample_submission.csv
> +-------------+--------------+-------------------------------------------------------------------------+
> | Column Name | Data Type    | Description                                                             |
> +-------------+--------------+-------------------------------------------------------------------------+
> | id          | UTF-8 String | Exact set of test IDs corresponding to test.csv.                      |
> | repair_json | UTF-8 JSON   | Baseline valid prediction JSON payload: {"holes":{},"reconstructed_sql":""} |
> +-------------+--------------+-------------------------------------------------------------------------+
> Internal JSON Payload Specifications
> input_json Payload Structure
> Plaintext
> +-------------+--------------+-------------------------------------------------------------------------+
> | Key         | Data Type    | Description                                                             |
> +-------------+--------------+-------------------------------------------------------------------------+
> | question    | UTF-8 String | The natural language query or task prompt.                             |
> | schema      | JSON Object  | Database schema object containing 4 keys:                               |
> |             |              |  - tables: List[String] (table names)                                   |
> |             |              |  - columns: List[Object] ({table_index, name, type})                    |
> |             |              |  - primary_keys: List[Int/Object]                                      |
> |             |              |  - foreign_keys: List[List]                                             |
> | damaged_sql | UTF-8 String | SQL query string with 1 or 2 clauses replaced by <HOLE_1>, <HOLE_2>.    |
> +-------------+--------------+-------------------------------------------------------------------------+
> repair_json Payload Structure (Target & Submission Output)
> Plaintext
> +-------------------+--------------+-------------------------------------------------------------------+
> | Key               | Data Type    | Description                                                       |
> +-------------------+--------------+-------------------------------------------------------------------+
> | holes             | JSON Object  | Dictionary mapping hole IDs to missing clause strings.            |
> |                   |              | Example: {"HOLE_1": "age > 30", "HOLE_2": "count(*) > 1"}         |
> |                   |              | Note: Content only; retained keywords (e.g. WHERE) are omitted.   |
> | reconstructed_sql | UTF-8 String | Complete predicted SQL statement after reconstructing all holes.  |
> +-------------------+--------------+-------------------------------------------------------------------+
> Evaluation Metrics
> Performance is scored at the individual row level using a composite metric blending token-level multiset
> ð¹
> 1
> F
> 1
> â€‹
> across hole predictions and exact normalized string matching for the reconstructed SQL query.
> 1. Hole Token Multiset
> ð¹
> 1
> F
> 1
> â€‹
> (
> ð»
> H)
> For each hole
> ð‘˜
> âˆˆ
> gold.holes
> kâˆˆgold.holes, lowercase word/punctuation tokens are extracted via regex \w+|[^\w\s]. The token multiset overlap between predicted tokens
> ð‘ƒ
> P and gold tokens
> ðº
> G is scored as:
> ð¹
> 1
> (
> ð‘ƒ
> ,
> ðº
> )
> =
> {
> 1.0
> if
> ð‘ƒ
> =
> âˆ…
> and
> ðº
> =
> âˆ…
> 0.0
> if
> ð‘ƒ
> =
> âˆ…
> or
> ðº
> =
> âˆ…
> 2
> â‹…
> âˆ‘
> min
> â¡
> (
> ð‘ƒ
> ð‘–
> ,
> ðº
> ð‘–
> )
> âˆ‘
> ð‘ƒ
> ð‘–
> +
> âˆ‘
> ðº
> ð‘–
> otherwise
> F
> 1
> â€‹
> (P,G)=
> âŽ©
> âŽ¨
> âŽ§
> â€‹
> 1.0
> 0.0
> âˆ‘P
> i
> â€‹
> +âˆ‘G
> i
> â€‹
> 2â‹…âˆ‘min(P
> i
> â€‹
> ,G
> i
> â€‹
> )
> â€‹
> â€‹
> ifÂ P=âˆ…Â andÂ G=âˆ…
> ifÂ P=âˆ…Â orÂ G=âˆ…
> otherwise
> â€‹
> ð»
> H is defined as the macro-average of
> ð¹
> 1
> (
> ð‘ƒ
> ,
> ðº
> )
> F
> 1
> â€‹
> (P,G) across all ground-truth holes in that row. If no holes exist in gold,
> ð»
> =
> 1.0
> H=1.0.
> 2. Query Reconstruction Match (
> ð‘„
> Q)
> The reconstructed query is tokenized, lowercased, and normalized into single-space string representations.
> ð‘„
> Q is a binary score:
> ð‘„
> =
> {
> 1.0
> ifÂ norm
> (
> pred.reconstructed_sql
> )
> =
> norm
> (
> gold.reconstructed_sql
> )
> 0.0
> otherwise
> Q={
> 1.0
> 0.0
> â€‹
> ifÂ norm(pred.reconstructed_sql)=norm(gold.reconstructed_sql)
> otherwise
> â€‹
> 3. Row Score & Final Submission Score
> For each valid evaluation row:
> RowScore
> =
> 0.55
> â‹…
> ð»
> +
> 0.45
> â‹…
> ð‘„
> RowScore=0.55â‹…H+0.45â‹…Q
> The final score is the arithmetic mean of all
> RowScore
> RowScore values across all rows in test.csv, clamped to
> [
> 0.0
> ,
> 1.0
> ]
> [0.0,1.0].
> Validation Strictness: If a row contains invalid JSON, missing payload fields, or unexpected types, its
> RowScore
> RowScore evaluates to 0.0. If submission row count, headers, or id alignment do not match test.csv exactly, the overall submission score will be 0.0.
> Submission Format
> Participants must submit a single UTF-8 encoded CSV file containing exactly two columns: id and repair_json.
> Header must strictly be: id,repair_json
> Must contain every id present in test.csv exactly once.
> JSON quotes inside CSV cells must be properly escaped ("").
> Example Submission File
> Code snippet
> id,repair_json
> sql_0123456789abcdef,"{""holes"":{""HOLE_1"":""T1.age > 25""},""reconstructed_sql"":""SELECT T1.name FROM users AS T1 WHERE T1.age > 25""}"
> sql_fedcba9876543210,"{""holes"":{""HOLE_1"":""AVG(price)"",""HOLE_2"":""category""},""reconstructed_sql"":""SELECT AVG(price) FROM products GROUP BY category""}"
> Resource Envelope
> Submissions are evaluated in a constrained CPU execution environment:
> Compute: 10 CPU cores (x86_64)
> Memory: 62 GB RAM
> Time Limit: 90 minutes total execution time
> GPU: Unavailable
> Network: Completely disabled
> Rules and Guidelines (What Not to Use)
> To maintain benchmark integrity and enforce the strictly "from-scratch" condition, participants must adhere to the following restrictions:
> No Pretrained Weights or Hosted APIs: You must not use pretrained language models, external neural weights, hosted LLM APIs, or online service queries.
> No External Datasets: Do not import external SQL corpora, supplementary Spider variants, or third-party schema datasets.
> No Reverse-Engineering or Source Matching: Do not attempt to look up upstream Spider 1.0 record keys, database source identifiers, or original timestamps. Row IDs are opaque hashes (sql_...) and must be treated as uninformative identifiers.
> Public File Isolation: Models must be trained and executed strictly using the released public training data (train.csv). Cross-participant submission sharing, answer trading, or manual target labeling is strictly prohibited.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Hen-House Motion Event Prediction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70t0c05ka36pn9w7a4jehgtx8bnwp8
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Hen-House Motion Event Prediction
> Overview
> This is a video sequence-to-sequence challenge built from fixed-camera poultry footage. Each row shows a compressed history of flock motion from an overhead hen-house camera. Your task is to predict three future motion events: the grid zone where the strongest motion will appear, the direction the motion will drift, and the motion-strength tier.
> In plain terms: the public input is a short motion history from a poultry house. You must predict what happens next in three consecutive future horizons.
> A valid prediction looks like:
> H0:Z04:DSE:M2 H1:Z08:DE:M1 H2:Z12:DC:M0
> The source videos are real fixed-camera RGB recordings from a poultry hen house. They show birds eating, drinking, and moving around under overhead cameras. The raw source archive contains 21 MP4 files, about 82 MB compressed. Source resolutions include 640x360, 640x480, 1280x720, and 1920x1080, with frame rates of 10, 20, 25, and 30 fps. The challenge generator uses 19 duration-sane videos after filtering two files whose container frame counts imply implausibly long durations.
> The public rows are not raw video frames. The generator samples each usable video at 10 Hz, converts frames to grayscale, computes frame-to-frame absolute-difference motion energy, pools motion into a 4 by 4 spatial grid, quantizes each zone to values from 0 to 63, applies deterministic spatial transforms, motion-ridge perturbations, and noise, and assigns fresh row-local zone aliases. The public past_motion_strip contains only the first 30 motion frames. The hidden target is derived from the following 18 motion frames, grouped into three future horizons.
> Train and hidden test examples use disjoint source videos, and every row uses fresh zone aliases. Solver-facing files do not expose source filenames, camera IP addresses, timestamps, or source-video identifiers.
> This is not animal classification, object detection, tracking, or action recognition. The output is a three-event structured forecast ledger.
> Dataset files
> train.csv contains:
> id: string. Unique training row ID.
> past_motion_strip: string. A 16 by 30 quantized motion strip encoded with 64 printable symbols.
> strip_shape: string. Always 16x30.
> frame_rate_hz: integer. Motion frames per second after sampling. Always 10.
> zone_cards: JSON list. Row-local grid-zone aliases and neighborhood metadata.
> forecast_horizons: string. Always H0,H1,H2.
> max_events: integer. Always 3.
> target_future_ledger: string. Training-only answer in the same three-token format required for submissions, for example H0:Z04:DSE:M2 H1:Z08:DE:M1 H2:Z12:DC:M0.
> test.csv has the same public columns but omits target_future_ledger.
> sample_submission.csv contains:
> id: string. Test row ID.
> predicted_future_ledger: string. Empty dummy ledger. The sample scores 0.
> There are 4,200 training rows and 1,500 hidden test rows. Hidden rows are balanced across five private scenario families with 300 rows per family.
> Input field schemas
> past_motion_strip:
> Type: string.
> Length: 480 characters.
> Decoding alphabet: 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_.
> Decoding method: map each character to an integer from 0 to 63, then reshape row-major to 16 zone rows by 30 time frames.
> Meaning: larger values indicate stronger frame-to-frame motion energy in that row-local zone.
> zone_cards is a JSON list of exactly sixteen objects. Each object has:
> zone: string. Row-local alias from Z01 through Z16.
> grid_row: integer. Row index from 0 to 3 in the transformed 4 by 4 grid.
> grid_col: integer. Column index from 0 to 3 in the transformed 4 by 4 grid.
> row_band: string. One of front, front_mid, back_mid, or back.
> col_band: string. One of left, left_mid, right_mid, or right.
> edge_zone: boolean. Whether the zone touches the grid boundary.
> neighbors: list of strings. Adjacent row-local zone aliases.
> Example zone_cards item:
> {"zone":"Z04","grid_row":0,"grid_col":3,"row_band":"front","col_band":"right","edge_zone":true,"neighbors":["Z03","Z08"]}
> Output grammar
> Submit exactly three space-separated event tokens, one for each horizon H0, H1, and H2.
> Each token has this form:
> Hk:Zxx:Dd:Mm
> Fields:
> Hk: horizon. Must be H0, H1, or H2.
> Zxx: row-local grid zone. Must be Z01 through Z16.
> Dd: drift direction. Must be one of DN, DNE, DE, DSE, DS, DSW, DW, DNW, or DC.
> Mm: motion-strength tier. Must be M0, M1, M2, or M3.
> The three tokens must appear in order: H0, then H1, then H2.
> Evaluation
> Structurally invalid submission files are rejected. Structural errors include missing columns, extra columns, duplicate IDs, unknown IDs, missing IDs, wrong row count, or wrong column order.
> Malformed row-level ledgers score 0 for that row instead of crashing the grader. Rows are aligned by id, not row order.
> For each horizon, the grader computes:
> ZoneScore =
> 1.00 if predicted zone equals true zone
> 0.10 if Manhattan distance between grid zones is 1
> 0.00 otherwise
> DirectionScore =
> 1.00 for exact direction
> 0.10 for adjacent compass direction
> 0.00 otherwise
> Compass distance is computed on this circular order:
> DN -> DNE -> DE -> DSE -> DS -> DSW -> DW -> DNW -> DN
> For example, the adjacent directions to DN are DNE and DNW. Directions at compass distance 2 or greater receive 0. If either direction is DC, direction credit is awarded only for exact DC.
> TierScore =
> 1.00 for exact motion tier
> 0.10 for adjacent tier
> 0.00 otherwise
> ExactEvent = 1 if the full event token is exactly correct, else 0
> For each horizon:
> EventScore =
> 0.52 * ZoneScore
> + 0.24 * DirectionScore
> + 0.14 * TierScore
> + 0.10 * ExactEvent
> TransitionScore is the fraction of the two adjacent zone transitions that are exactly correct:
> TransitionScore =
> correct predicted zone bigrams / 2
> ExactLedger is 1 only when the full three-token ledger exactly matches the hidden ledger.
> The row score is:
> row_score =
> 0.64 * mean(EventScore over H0,H1,H2)
> + 0.18 * TransitionScore
> + 0.18 * ExactLedger
> If ExactLedger is 1, row_score is exactly 1.
> The hidden set is balanced across five private families:
> steady_flow
> edge_surge
> quiet_break
> crowd_shift
> multi_peak
> Family labels are not present in solver-facing files. They are used only for robust hidden scoring.
> Final score:
> overall_mean = mean(row_score over all hidden rows)
> worst_family_mean = minimum family mean over the five private families
> bottom_20_mean = mean(row_score over the lowest-scoring 20% of hidden rows)
> final_score =
> 0.70 * overall_mean
> + 0.18 * worst_family_mean
> + 0.12 * bottom_20_mean
> Scores are finite and bounded in [0, 1]. The sample submission scores 0. A perfect oracle scores 1.
> Submission format
> Submit a CSV with exactly two columns in this order:
> id: test row ID.
> predicted_future_ledger: three-token future ledger.
> Example:
> id,predicted_future_ledger
> 0a12bc34de56f789,H0:Z04:DSE:M2 H1:Z08:DE:M1 H2:Z12:DC:M0
> What not to use
> Do not use source video filenames, camera IP addresses, timestamps, row order, or fixed zone meanings. These are absent from solver-facing rows or regenerated per row.
> Do not submit raw video, bounding boxes, JSON, natural-language explanations, or extra columns.
> Do not treat the task as classifying a poultry behavior. The target is a structured future-motion ledger over row-local zones.
> Do not simply repeat the strongest past zone. Hidden scoring includes quiet breaks, edge surges, crowd shifts, and multi-peak future motion.
> Recommended solution approach
> Stronger solutions should train sequence models or temporal nearest-neighbor systems using source-video-disjoint validation, zone-card geometry, and horizon-specific losses.
> Benchmark boundary
> Nearest prior work includes poultry behavior recognition, optical-flow analysis, object tracking, and video anomaly detection. Those tasks usually classify clips, track objects, or detect animals. This benchmark instead asks for a compact future ledger from transformed motion sketches with row-local grid aliases, disjoint source videos, horizon-specific structured outputs, and robust tail-family scoring. It is therefore a video-derived sequence forecasting task rather than ordinary animal classification or object detection.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Interrupted Query Recovery Ledger

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx710mjk3k1f8ad81ky7pq65058c1wgf
- DOMAIN exactly as displayed: Sequence To Sequence
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
> Interrupted Query Recovery Ledger is a hard, CPU sequence-to-sequence challenge about recovering final information intent from a query that changes direction while it is being expressed. Pretrained language models and pretrained sequence-to-sequence checkpoints are allowed.
> For each test example, the model receives:
> One reference passage.
> One interrupted query trace.
> The query trace may contain corrections, false starts, abandoned entities, repeated fragments, reformulated syntax, or an earlier request that is later replaced.
> The model must generate one recovery sequence containing two parts:
> The final intended query.
> The supporting evidence phrase from the reference passage, or <NONE> when the final intended query is not answerable from that passage.
> A valid target looks like:
> <QUERY> Which engineer designed the eastern bridge? <EVIDENCE> Mara Voss
> An unanswerable target looks like:
> <QUERY> Which treaty created the office? <EVIDENCE> <NONE>
> The task therefore couples query repair with contextual evidence recovery.
> A model cannot obtain a strong score by only deleting obvious hesitation words. It must determine which parts of the trace survive the speaker's revisions, preserve the intended word order, reconstruct missing or replaced material, and then answer the repaired query against the associated passage.
> There are no candidate outputs to rank.
> The submission contains one generated sequence per test example.
> What Is Being Predicted
> For one example, let:
> R be the released reference passage.
> T be the released interrupted query trace.
> Q* be the hidden final intended query.
> E* be a valid evidence phrase from R, or <NONE> when the query is not answerable from R.
> The required output is:
> <QUERY> Q* <EVIDENCE> E*
> The query and evidence are evaluated separately and jointly.
> The query is also aligned back to the interrupted trace. This alignment defines an implied repair path over the source trace:
> Which source tokens were retained.
> Which source tokens were discarded.
> Which new tokens were inserted.
> At which source boundaries inserted material appears.
> The model does not submit this repair path directly.
> It is reconstructed by the evaluator from the generated query and used as part of the metric.
> This makes two generations with similar bag-of-words content score differently when one preserves the actual repair structure and the other does not.
> Query Traces
> The released query traces are English information requests containing natural revision phenomena.
> A trace may contain:
> A false start followed by a restart.
> An entity that is later replaced.
> A date that is corrected.
> A location that is corrected.
> A number that is corrected.
> A predicate that is replaced.
> A partial syntactic restart.
> A complete question restart.
> Repetition.
> Filled pauses.
> Discourse repair markers.
> Multiple pieces of plausible but abandoned content.
> For example, a trace may conceptually resemble:
> Which city hosted the assembly in 1912, no sorry, make that the 1914 assembly?
> The intended query is not the literal entire trace.
> The model must infer which proposition survives the correction.
> Another trace may contain a much smaller edit:
> Which routing method uses datagrams or uh, I mean virtual circuits?
> The difficulty varies substantially across examples.
> Some traces can be repaired by deleting one short fragment.
> Others require identifying a replacement span or a full restart while ignoring earlier words that are still highly related to the reference passage.
> Reference Passages
> Each example includes an encyclopedia-style reference passage.
> The passage provides the evidence needed for answerable examples.
> Passages cover many domains, including:
> History.
> Geography.
> Biology.
> Geology.
> Mathematics.
> Economics.
> Politics.
> Networking.
> Universities.
> Social science.
> Engineering.
> The passage is not merely auxiliary context.
> It can help disambiguate which correction is semantically coherent.
> Abandoned fragments may also mention terms that occur in the passage, so lexical overlap alone is intentionally unreliable.
> Evidence Recovery
> The second part of the output is an evidence phrase.
> For answerable examples, the evidence should be a concise text span supported by the reference passage.
> For unanswerable examples, the evidence must be:
> <NONE>
> Some answerable examples admit several equivalent evidence strings.
> The evaluator accepts all private reference variants associated with the example.
> The public training target contains one canonical evidence string so the task remains a standard one-sequence supervised generation problem.
> The grader still gives full credit to another accepted evidence variant.
> Recovery Sequence Format
> Every generated sequence must contain the two markers:
> <QUERY>
> and
> <EVIDENCE>
> The expected structure is:
> <QUERY> repaired query text <EVIDENCE> evidence text
> Requirements:
> <QUERY> must appear first.
> <EVIDENCE> must appear after it.
> The query portion must be non-empty.
> Answerable predictions should place a text phrase after <EVIDENCE>.
> Unanswerable predictions should place exactly <NONE> after <EVIDENCE>.
> Marker matching is case-insensitive and surrounding whitespace is ignored.
> Extra text before <QUERY> is not valid.
> If a generated row cannot be parsed, that row receives zero for all metric components. Other rows in the submission are still evaluated normally.
> Challenge Type
> This is a Fine-Tuning sequence-to-sequence challenge.
> Pretrained models are allowed.
> Participants may start from public pretrained language or sequence-to-sequence checkpoints and fine-tune them on the released training data.
> Eligible systems include:
> Pretrained encoder-decoder Transformers.
> Pretrained text encoders with custom repair and evidence heads.
> T5-style sequence-to-sequence models.
> BART-style sequence-to-sequence models.
> Compact pretrained Transformers.
> Word-level or subword encoder-decoder models trained from scratch.
> Character-aware recurrent models.
> Small GRU or LSTM sequence-to-sequence models.
> Pointer-generator models.
> Copy-and-edit transducers.
> Repair tagging followed by deterministic reconstruction.
> Joint repair-and-evidence models.
> Extractive evidence rankers.
> Eligible ensembles.
> Rule-based components may be combined with learned systems.
> The challenge does not require a particular pretrained model family.
> Compute
> The execution environment provides:
> 10 CPU cores.
> 62.5 GiB RAM.
> No GPU.
> The challenge is designed for compact CPU-friendly NLP systems.
> Pretrained models are allowed, but the execution budget still favors compact architectures.
> A useful submission can combine efficient tokenization, alignment, edit modeling, span ranking, and a compact pretrained or custom sequence model.
> Released Dataset
> The public package contains:
> train.jsonl
> test.jsonl
> sample_submission.csv
> No auxiliary schema, relay, mapping, or hidden feature file is required to train or submit a solution.
> There is no official validation file.
> The official train/test split is grouped by complete reference passage so the same passage does not appear in both partitions.
> train.jsonl
> Each line contains one JSON object.
> Fields:
> sample_id
> Type: string.
> Unique row identifier used for submission alignment.
> Do not use it as a predictive feature.
> reference_text
> Type: string.
> The passage used to resolve the final query and recover evidence.
> query_trace
> Type: string.
> The interrupted information request.
> recovery_target
> Training only.
> Type: string.
> The complete target sequence in the form:
> <QUERY> ... <EVIDENCE> ...
> For unanswerable examples, the evidence segment is:
> <NONE>
> test.jsonl
> Contains the same public input fields as train.jsonl, except:
> recovery_target is omitted.
> The test data does not expose:
> Final intended queries.
> Evidence answers.
> Alternative accepted evidence strings.
> Source identifiers.
> Original partition membership.
> Answer offsets.
> Passage grouping hashes.
> Preparation hashes.
> Train/Test Split
> All available examples are regrouped by exact reference passage before the official split.
> A reference passage belongs entirely to train or entirely to test.
> Approximately 75% of released rows are used for training and 25% for test, subject to passage-group boundaries.
> This prevents direct passage memorization across official partitions.
> Multiple training rows may still share one reference passage.
> This is intentional because one passage can support several distinct interrupted queries.
> For local validation, split by complete reference_text rather than by individual rows.
> All derivatives of one passage should remain in the same local partition.
> Submission Format
> The submission contains one row per test example.
> Columns:
> sample_id
> recovery_text
> Example:
> IQR_... , "<QUERY> Which engineer designed the eastern bridge? <EVIDENCE> Mara Voss"
> The exact header is provided by sample_submission.csv.
> The evaluator accepts rows in any order and aligns them by sample_id.
> Invalid submissions include:
> Missing samples.
> Extra samples.
> Duplicate sample IDs.
> Missing columns.
> Extra columns.
> Incorrect column order.
> Blank recovery strings.
> Recovery strings longer than 8,192 characters.
> Embedded NUL characters.
> A syntactically valid CSV row can still contain a malformed recovery sequence. In that case only that row receives zero metric credit.
> Evaluation
> Submissions are evaluated using the Interrupted Query Recovery Score from 0.01 to 100.
> Higher is better.
> The metric has three sample-level components:
> Intent Text Recovery.
> Repair Topology Recovery.
> Evidence Recovery.
> The dataset-level means of these components are combined only after all test rows have been evaluated.
> There are no hidden metric weights.
> Text Normalization
> For query scoring, text is normalized as follows:
> Apply Unicode NFKC normalization.
> Lowercase the text.
> Replace the curly apostrophe â€™ with the ASCII apostrophe '.
> Tokenize with the regular expression:
> [a-z0-9]+(?:'[a-z0-9]+)?
> Punctuation outside these tokens is ignored by the query similarity components.
> The exact normalized token sequence is also used for normalized exact match.
> Intent Text Recovery
> Let:
> P be the normalized token sequence of the predicted repaired query.
> G be the normalized token sequence of the hidden repaired query.
> Three values are calculated.
> Token Multiset F1
> Tokens are compared as multisets.
> Precision is the number of shared token occurrences divided by the number of predicted tokens.
> Recall is the number of shared token occurrences divided by the number of gold tokens.
> Their harmonic mean is TokenF1.
> Ordered LCS F1
> Let LCS(P,G) be the length of the longest common subsequence of the two token sequences.
> Define:
> LCSF1 = 2 Ã— LCS(P,G) / (len(P) + len(G))
> This rewards correct order and penalizes duplicated or misplaced material.
> Normalized Exact Match
> ExactQuery = 1
> when P and G are identical token sequences, otherwise:
> ExactQuery = 0
> Intent Component
> The sample-level Intent Text Recovery value is:
> Intent = sqrt(TokenF1 Ã— LCSF1) Ã— (0.90 + 0.10 Ã— ExactQuery)
> Therefore an exact reconstruction receives 1.0.
> A bag-of-words reconstruction with incorrect order loses LCS credit.
> A nearly exact reconstruction still receives graded credit.
> Repair Topology Recovery
> The evaluator aligns the interrupted query trace to both:
> The hidden repaired query.
> The predicted repaired query.
> Alignment is performed with Python difflib.SequenceMatcher(a=trace_tokens, b=query_tokens, autojunk=False) on the normalized query tokens. The evaluator uses the returned opcodes in order. equal marks source tokens as KEEP, delete leaves source tokens as DROP, and the target-side tokens from replace or insert are recorded as insertions at source boundary i1.
> Each alignment induces two structures.
> Source Keep/Drop Labels
> Every token in the interrupted trace receives one label:
> KEEP if it belongs to an exact aligned block retained by the repaired query.
> DROP otherwise.
> The predicted KEEP/DROP labels are compared with the hidden labels.
> F1 is calculated independently for KEEP and DROP.
> If a class is absent from both prediction and truth, that class receives F1 = 1.
> Define:
> TagMacroF1 = (KeepF1 + DropF1) / 2
> Insertion Anchors
> Every insertion or replacement contributes generated tokens at a boundary between source-trace tokens.
> For each boundary used by either the prediction or truth, the inserted token multisets are compared using token F1.
> Boundary scores are weighted by the larger inserted-token count at that boundary.
> If neither alignment contains any insertion, the insertion score is 1.
> Call the weighted result:
> InsertionF1
> Repair Component
> The sample-level Repair Topology Recovery value is:
> Repair = sqrt(TagMacroF1 Ã— InsertionF1)
> This component is intentionally derived from the generated query rather than submitted separately.
> It rewards recovering the actual revision path, not only producing semantically related text.
> Evidence Recovery
> Evidence normalization follows this extractive-answer procedure:
> Apply Unicode NFKC normalization.
> Lowercase the text.
> Replace every Unicode character whose category begins with P with a space.
> Remove the English articles a, an, and the as whole words.
> Collapse consecutive whitespace.
> Answerable Examples
> For an answerable example, the prediction must not be <NONE>.
> The evaluator compares the predicted evidence against every accepted private evidence string.
> For each accepted answer it computes token F1 after evidence normalization.
> AnswerF1
> is the maximum of these values.
> AnswerExact
> is 1 when the normalized prediction exactly matches at least one accepted evidence string and 0 otherwise.
> SpanValid
> is 1 when the normalized predicted evidence tokens occur as a contiguous token span in the normalized reference passage and 0 otherwise.
> The answerable Evidence Recovery value is:
> Evidence = AnswerF1 Ã— (0.90 + 0.10 Ã— SpanValid) Ã— (0.90 + 0.10 Ã— AnswerExact)
> A fully exact supported evidence span receives 1.0.
> Unanswerable Examples
> For an unanswerable example:
> Evidence = 1
> only when the predicted evidence is exactly <NONE> after trimming and case normalization.
> Otherwise:
> Evidence = 0
> Answerability Gate
> For answerable examples, predicting <NONE> gives Evidence = 0.
> For unanswerable examples, predicting any text phrase gives Evidence = 0.
> The evidence component therefore includes the answerability decision directly.
> Final Score
> After evaluating all test examples, compute:
> IntentMean = mean(Intent)
> RepairMean = mean(Repair)
> EvidenceMean = mean(Evidence)
> Define the weighted geometric core:
> Core = (IntentMean^2 Ã— RepairMean Ã— EvidenceMean)^(1/4)
> Intent recovery receives double weight because reconstructing the final query is the primary objective.
> Then define a coupling factor:
> Coupling = 0.80 + 0.20 Ã— min(IntentMean, EvidenceMean)
> The final score is:
> Interrupted Query Recovery Score = 100 Ã— Core Ã— Coupling
> The result is clipped to:
> [0.01, 100]
> A perfect reconstruction receives exactly:
> 100
> The coupling factor discourages systems that are strong at only one side of the task.
> For example, a model that repairs queries well but cannot recover contextual evidence will lose geometric-core credit and additional coupling credit.
> Reproducing the Metric Locally
> For each validation example:
> Parse <QUERY> and <EVIDENCE> from the generated sequence.
> Normalize predicted and true queries into query tokens.
> Compute token multiset F1.
> Compute longest-common-subsequence F1.
> Compute normalized exact query match.
> Calculate the Intent component.
> Align the interrupted trace to the predicted and true query.
> Derive source KEEP/DROP labels.
> Derive inserted-token boundary maps.
> Compute KEEP/DROP macro F1.
> Compute weighted insertion-boundary F1.
> Calculate the Repair component.
> Normalize the predicted evidence.
> Score it against all accepted evidence strings, or verify <NONE> for an unanswerable example.
> Calculate the Evidence component.
> Average Intent, Repair, and Evidence separately across validation examples.
> Apply the published final formula.
> The reference implementation in grader.py is authoritative.
> Intended Modeling Approaches
> A strong CPU solution can decompose the problem into repair inference and evidence recovery while sharing useful representations.
> Repair Tagging
> One practical approach is to assign source-trace tokens latent actions such as:
> Retain.
> Delete.
> Begin replacement.
> Continue replacement.
> The repaired query can then be reconstructed with a small insertion model.
> Useful architectures include:
> BiLSTM taggers.
> GRU taggers.
> Lightweight temporal CNNs.
> Small pretrained or randomly initialized Transformers.
> Copy-and-Edit Transduction
> Most repaired queries preserve substantial material from the interrupted trace.
> Pointer or copy mechanisms can exploit this structure.
> A compact model may learn when to:
> Copy source tokens.
> Skip abandoned spans.
> Insert replacement material.
> Restart from a later source fragment.
> Context-Aware Repair
> The reference passage can help resolve ambiguous corrections.
> Useful features may include:
> Token overlap between candidate query fragments and the passage.
> BM25-style passage relevance.
> Local sentence retrieval.
> Learned token-to-context similarity.
> Character n-gram similarity.
> Lightweight cross-attention.
> Evidence Recovery
> After repairing the query, evidence can be predicted with an extractive span model or a ranking model.
> CPU-friendly options include:
> Sentence ranking followed by span scoring.
> TF-IDF or BM25 candidate generation with a learned reranker.
> BiLSTM span prediction.
> Compact pretrained or custom Transformer span prediction.
> Character-aware answer boundary models.
> Joint answerability and span scoring.
> Joint Modeling
> The repair and evidence tasks are coupled.
> A candidate repair that produces a question unsupported by the passage may be less plausible than a competing repair that produces a coherent answerable query.
> Stronger systems may jointly score:
> Repair path likelihood.
> Reconstructed-query likelihood.
> Evidence-span compatibility.
> Answerability.
> Beam search can retain several repair hypotheses and rerank them using contextual evidence compatibility.
> Additional Training on Released Text
> Participants may continue pretraining or train auxiliary representations on the released challenge corpus.
> Examples include:
> Masked-token prediction.
> Denoising autoencoding.
> Character corruption recovery.
> Next-token prediction.
> Contrastive passage/query objectives constructed from released rows.
> Generic knowledge already contained in a public pretrained checkpoint is allowed.
> Additional task-specific supervised data from outside the released challenge package is not allowed.
> Practical CPU Baseline
> A practical baseline may:
> Tokenize the interrupted query and passage.
> Learn common repair-marker patterns from training traces.
> Fine-tune a compact encoder or train a token keep/drop classifier.
> Reconstruct a candidate final query with deterministic alignment features.
> Train a small insertion model for replacement spans.
> Retrieve the most relevant passage sentence using the reconstructed query.
> Train a compact answerability classifier.
> Rank candidate evidence spans inside the retrieved sentence.
> Emit <NONE> when the answerability score is low.
> Serialize the final output with the required markers.
> Evaluate with the official metric.
> This baseline can be improved with:
> Character features.
> Subword tokenization learned from training text.
> Multiple repair hypotheses.
> Context-aware reranking.
> Joint span and answerability training.
> Query-repair auxiliary losses.
> Small eligible ensembles.
> Pretrained Model Policy
> Pretrained models are allowed.
> Participants may use:
> Public pretrained language models.
> Public pretrained sequence-to-sequence checkpoints.
> Public pretrained text encoders.
> Public pretrained word or subword embeddings.
> Public pretrained sentence representations.
> Tokenizers and vocabularies distributed with eligible checkpoints.
> Randomly initialized models trained only on released data.
> Continued pretraining on released challenge text.
> Fine-tuning on released training targets.
> The pretrained checkpoint may have been trained on external generic text before the challenge.
> The challenge does not require participants to reproduce that pretraining.
> All task-specific supervised fine-tuning performed for the submission must use only released challenge labels.
> Allowed Resources
> Participants may use:
> Released challenge files.
> Public pretrained model checkpoints.
> Public pretrained tokenizer files.
> Public model architecture source code.
> Standard numerical libraries.
> Standard NLP libraries.
> Standard machine-learning libraries.
> Standard deep-learning frameworks.
> Deterministic text normalization.
> Deterministic alignment algorithms.
> Classical information-retrieval methods.
> Dynamic programming.
> Auxiliary targets derived from released training labels.
> Additional unsupervised or self-supervised objectives on released challenge text.
> Eligible ensembles.
> Disallowed Resources
> Participants may not use:
> External task-specific labeled training data.
> External labels or hidden target rows from the underlying source benchmark.
> External answer or fluent-query lookups for evaluated examples.
> External copies of the underlying source corpus used to recover test targets.
> Internet retrieval or external knowledge-base lookup during prediction.
> Hosted language-model or question-answering APIs.
> Manual test annotation.
> Hidden test answers.
> Private evaluator files.
> Hard-coded test predictions.
> Recovery of hidden source identifiers for target lookup.
> Joining test rows to external copies of the original source data.
> sample_id as a predictive feature.
> Row order as a predictive feature.
> Submission-feedback reconstruction of hidden answers.
> A pretrained checkpoint is allowed because it supplies general language knowledge.
> Using an external copy of the benchmark to directly recover the hidden repaired question or answer is not allowed.
> Validation and Leakage
> The official split is passage-grouped.
> For local validation, all rows sharing the same reference_text must remain together.
> Do not place one query from a passage in training and another query from the same passage in validation.
> Any derivatives of one row must remain in the same local partition, including:
> Tokenized copies.
> Character encodings.
> Cached embeddings.
> Retrieved sentence candidates.
> Repair tags.
> Synthetic corruptions derived from that row.
> Evidence span candidates.
> If continued pretraining or representation learning uses held-out validation text, report that choice clearly when comparing local experiments because it changes the meaning of the validation score.
> Data License
> The underlying text material is distributed under CC BY 4.0.
> Challenge redistribution should preserve the attribution and license information supplied with the dataset package.
> Limitations
> The benchmark uses written English query traces rather than raw audio.
> It does not model:
> Acoustic hesitation timing.
> Prosody.
> Speech-recognition errors.
> Speaker identity.
> Real-time turn taking.
> The reference passages are encyclopedia-style text and do not represent every information environment.
> The majority of revision phenomena involve corrections or restarts.
> Some repaired questions differ from the trace by only a small local edit, while others require a broader restart.
> The evidence target is extractive or explicitly unanswerable.
> The challenge does not evaluate free-form explanatory answers.
> Several examples can share one passage within the same partition.
> Performance on this benchmark does not guarantee robustness to spontaneous spoken dialogue or automatic speech-recognition output.
> Expected Outcome
> A successful system should:
> Learn or fine-tune robust query-repair behavior.
> Separate abandoned content from final intent.
> Preserve the correct token order.
> Recover replacement material when required.
> Use the reference passage to resolve contextual ambiguity.
> Decide whether the repaired query is answerable.
> Recover concise supporting evidence when it is answerable.
> Emit a valid structured sequence.
> Train efficiently in the CPU-only environment.
> The prediction objective is:
> recover the final query and its contextual evidence from each interrupted information trace.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Edit-Budgeted Historical German Text Normalization

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ea8tp0j1esg8jt6gksnk7p18c0cra
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Edit-Budgeted Historical German Text Normalization
> Overview
> Historical spelling varies across time, authors, and printing conventions. A useful normalizer must handle character substitutions, combining marks, word-form changes, punctuation spacing, insertions, and deletions while preserving the meaning and order of the text.
> In this sequence-to-sequence challenge, every example contains three consecutive historical German sentences. Generate their three modernized spelling sequences in the same order. The sentences form one block, so surrounding context can help with ambiguous words and transformations.
> Each row also provides two target-derived decoder aids:
> edit_budget gives the exact Unicode code-point Levenshtein distance from each historical sentence to its hidden normalization.
> target_lengths gives the exact Unicode code-point length of each hidden normalized sentence.
> These profiles sharply describe how much revision is required without revealing where the edits occur or what the replacement text is. Many incorrect outputs share the same profiles. A context-free constructor can therefore satisfy both profiles without learning language; sample_submission.csv deliberately demonstrates such a weak scaffold. The profiles are decoding guidance, not submission-validity conditions: a correctly formatted prediction remains scorable even when its length or edit distance differs.
> The primary metric compares source-anchored revision events, so copying the historical input, making arbitrary edits that satisfy the budgets, retrieving a training sentence, or predicting only common spellings is substantially weaker than learning contextual revision patterns.
> Task
> historical_sequence contains exactly three sentences. The literal separator is âŸªSâŸ« : one ASCII space, followed by the three characters âŸªSâŸ«, followed by one ASCII space. The separator contains no newline or other control character. Line breaks around examples in this description are Markdown formatting only and are not part of the separator.
> For example, the abstract structure is:
> historical_sentence_1 âŸªSâŸ« historical_sentence_2 âŸªSâŸ« historical_sentence_3
> Predict one normalized_sequence with the same three-segment structure:
> normalized_sentence_1 âŸªSâŸ« normalized_sentence_2 âŸªSâŸ« normalized_sentence_3
> All text is compared after NFC Unicode normalization. Sentence order and exactly two occurrences of the literal âŸªSâŸ« separator matter.
> Dataset
> The platform generates four participant-facing files. Source names, publication identifiers, author identifiers, filenames, URLs, and original row positions are not included.
> train.csv
> Purpose: labelled examples for learning historical-to-modern revision patterns.
> Columns:
> sample_id
> Type: string.
> Format: EBH_TR_ followed by six decimal digits.
> Meaning: synthetic training identifier assigned after deterministic train shuffling; it carries no predictive meaning.
> historical_sequence
> Type: Unicode string.
> Format: exactly three non-empty NFC sentences joined by âŸªSâŸ« .
> Meaning: ordered historical-spelling input block.
> edit_budget
> Type: string containing a JSON array.
> Format: [d1,d2,d3], where each value is a non-negative integer.
> Meaning: exact source-to-hidden-target code-point Levenshtein distance for each sentence.
> target_lengths
> Type: string containing a JSON array.
> Format: [n1,n2,n3], where each value is a positive integer.
> Meaning: hidden normalized sentence lengths measured in Unicode code points.
> normalized_sequence
> Type: Unicode string.
> Format: exactly three non-empty NFC sentences joined by âŸªSâŸ« .
> Meaning: training target containing the three aligned modernized sentences.
> test.csv
> Purpose: unlabelled blocks requiring normalization.
> Columns:
> sample_id
> Type: string.
> Format: EBH_TE_ followed by six decimal digits.
> Meaning: synthetic test identifier assigned after an independent deterministic test shuffle; it is used only for submission alignment.
> historical_sequence
> Type: Unicode string.
> Format: exactly three non-empty NFC sentences joined by âŸªSâŸ« .
> Meaning: ordered historical-spelling input block.
> edit_budget
> Type: string containing a JSON array.
> Format: [d1,d2,d3], where each value is a non-negative integer.
> Meaning: exact source-to-hidden-target edit-distance profile for the three sentences.
> target_lengths
> Type: string containing a JSON array.
> Format: [n1,n2,n3], where each value is a positive integer.
> Meaning: exact hidden target-length profile for the three sentences.
> sample_submission.csv
> Purpose: exact submission schema plus a weak constraint-only scaffold.
> Columns:
> sample_id
> Type: string.
> Format: one exact identifier from test.csv.
> Meaning: test block being predicted.
> normalized_sequence
> Type: Unicode string.
> Format: exactly three non-empty segments joined by âŸªSâŸ« .
> Meaning: illustrative prediction. Its construction uses public test inputs and profiles plus a filler alphabet selected from training character counts only; it never uses hidden test text.
> metadata.json
> Purpose: participant-safe structural configuration.
> Fields:
> challenge_version â€” string in dotted-version format; prepared challenge version.
> task â€” string; canonical challenge title.
> train_rows â€” integer; number of labelled rows, equal to 6,000.
> test_rows â€” integer; number of unlabelled rows, equal to 1,500.
> segments_per_sequence â€” integer; required segment count, equal to 3.
> segment_separator â€” string; exact separator âŸªSâŸ« .
> submission_columns â€” array of strings; required ordered submission columns.
> constraints â€” string; summary of output structure and decoder-profile semantics.
> metric â€” string; summary of the four score components and weights.
> sample_submission â€” string; training-only and public-input scaffold description.
> split â€” string; whole-author grouping, duplicate audit, and shuffle summary.
> The split is performed by complete anonymized author groups. Every retained author and publication occurs in exactly one partition. Each century band contributes whole groups to both partitions. Exact and near-duplicate historical or normalized sentences are prevented across train and test. Blocks within one publication do not reuse source sentences. Train and test are independently shuffled before sequential synthetic IDs are assigned.
> Evaluation
> Let the three predicted sentences be p1, p2, and p3, and the hidden sentences be t1, t2, and t3.
> Character similarity for one sentence is:
> similarity(p, t) = 1 - levenshtein(p, t) / max(len(p), len(t), 1)
> S_char is the mean similarity across the three sentences.
> F_revision compares source-anchored revision events. For each sentence independently, the grader runs Python's deterministic difflib.SequenceMatcher with autojunk=False between the historical sentence and the candidate output. Every non-equal opcode becomes this position-sensitive event:
> (segment_index, input_start, input_end, opcode_tag, removed_input_text, inserted_output_text)
> The same events are derived from the hidden normalization. F_revision is multiset F1 over predicted and hidden events. Source positions, direction, removed text, inserted text, and repeated-event multiplicity all matter. An edit at the wrong position does not match the correct event.
> A_segment is the fraction of the three sentences that match exactly. I_block is 1 only when the complete three-sentence output matches exactly.
> row_score = 0.20 * S_char
> + 0.60 * F_revision
> + 0.15 * A_segment
> + 0.05 * I_block
> Let q be the arithmetic mean of all row scores. The reported leaderboard score is:
> final_score = q^2  *exp(-2.25*  q * (1 - q))
> The boundary values follow directly by substitution:
> q = 0: final_score = 0^2  *exp(-2.25*  0 * (1 - 0)) = 0.0
> q = 1: final_score = 1^2  *exp(-2.25*  1 * (1 - 1)) = 1.0
> This strictly increasing calibration preserves the ordering produced by the row metric while giving greater separation among strong, partially correct systems. Higher is better.
> Submission
> Submit a UTF-8 CSV file with exactly these columns in this order:
> sample_id,normalized_sequence
> Correctly formatted illustrative rows:
> sample_id,normalized_sequence
> EBH_TE_000001,Der erste Satz âŸªSâŸ« Der zweite Satz âŸªSâŸ« Der dritte Satz
> EBH_TE_000002,Eine moderne Form âŸªSâŸ« Noch eine Form âŸªSâŸ« Der letzte Abschnitt
> EBH_TE_000003,Alpha âŸªSâŸ« Beta âŸªSâŸ« Gamma
> Every test ID must appear exactly once. Row order does not matter. Use a compliant CSV writer so commas and quotation marks inside predicted text are escaped correctly.
> The grader NFC-normalizes each prediction before parsing. A valid normalized_sequence must contain exactly three non-empty segments separated by exactly two literal âŸªSâŸ« strings, each consisting of one ASCII space before and after âŸªSâŸ« and containing no newline. Each segment must contain at most 320 Unicode code points, have no leading or trailing whitespace, contain no control characters, and not contain the reserved separator marker. Internal printable punctuation and whitespace are allowed. Repeated words or repeated complete segments are allowed.
> An invalid individual sequence receives zero for that row. A profile mismatch does not make a row invalid; it only indicates that the prediction did not use the public decoder guidance exactly.
> The entire submission receives zero when its columns are not exactly sample_id,normalized_sequence in that order, a CSV row is malformed, an ID is empty or duplicated, the row count is wrong, or the submitted ID set differs from the test ID set.
> What Not to Use
> Do not use external corpora, dictionaries, language models, source-archive copies, internet lookup, or challenge-specific pretrained checkpoints.
> Do not attempt to recover publications through filenames, phrases, source identifiers, or external text search.
> Do not use IDs, row order, file order, metadata ordering, or sample-submission values as target signals.
> Do not access hidden files, private answers, platform internals, or private APIs.
> Do not install packages or download data during execution.
> Requirements
> Use only the supplied participant files and the preinstalled platform runtime.
> Solutions must run on CPU only, using at most 10 CPU cores and 62 GB RAM.
> The complete solution must finish within 1.5 hours.
> No GPU is required or permitted for this challenge configuration.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Dakshina Dual-View Transliteration and Alignment Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx705z9xv1h36m6gmjk0p4hyfx8bzrb0
- DOMAIN exactly as displayed: Sequence To Sequence
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
> In modern natural language processing, parallel text across different writing systemsâ€”specifically native regional scripts (e.g., Devanagari, Bengali) and Latin-script romanizations (transliterations used in digital communication)â€”frequently suffers from corruption. Real-world optical character recognition (OCR), keyboard auto-correction, and noisy transmission pipelines often produce incomplete transcriptions across both scripts simultaneously.
> This challenge presents a multilingual sequence repair and alignment fine-tuning task across 12 South Asian languages. Given two synchronized but partially corrupted views of a sentenceâ€”a native-script view with missing spans (native_skeleton) and a romanized view with disjoint missing spans (roman_skeleton)â€”models must leverage cross-script context to restore all missing text gaps, reconstruct both complete sentences, and output the exact token-level alignments.
> Operational Context & Data Origin
> The dataset is constructed from a standardized multilingual parallel text corpus collected across South Asian language domains. Sentences were filtered for length (4â€“32 token cells) and processed to produce high-quality cased, non-punctuated Latin romanizations.
> To simulate real-world transmission loss and cross-script recovery, deterministic disjoint holes are introduced into each sentence pair:
> Native-script gaps (e.g., <n0>, <n1>) and Roman-script gaps (e.g., <r0>, <r1>) never mask the same alignment cell.
> The intact tokens on one side serve as direct cross-script grounding to predict the missing text on the counterpart side.
> Task Mechanics
> For every test sample, your model is provided with:
> language: Two-letter language identifier.
> native_skeleton: The native-script sentence containing masked gap markers (<n0>, <n1>, ...).
> roman_skeleton: The synchronized romanized sentence containing masked gap markers (<r0>, <r1>, ...).
> hole_ids_json: A JSON list of expected gap markers present in the skeletons.
> Your model must output a single valid JSON object per row that restores every missing span, reconstructs both full normalized sentences, and provides the ordered token alignment array.
> +-----------------------------------------------------------------------------------+
> |                            DUAL-VIEW MASKED SENTENCE INPUT                        |
> +-----------------------------------------------------------------------------------+
> |                                                                                   |
> | Native Skeleton:  "à¤œà¤¬à¤•à¤¿ <n0> à¤•à¤® à¤¹à¥ˆà¥¤"                                               |
> | Roman Skeleton:   "Jabki yah <r0> hai."                                           |
> |                                                                                   |
> | Disjoint Cross-Script Evidence:                                                    |
> |  â€¢ Native gap <n0> aligns with Roman intact token "yah"  ==> Target Native: "à¤¯à¤¹"   |
> |  â€¢ Roman gap <r0>  aligns with Native intact token "à¤•à¤®"   ==> Target Roman:  "km"   |
> |                                                                                   |
> +-----------------------------------------------------------------------------------+
> |                             EXPECTED PREDICTION (JSON)                            |
> +-----------------------------------------------------------------------------------+
> |                                                                                   |
> | {                                                                                 |
> |   "native_gaps":    [{"hole_id": "n0", "text": "à¤¯à¤¹"}],                            |
> |   "roman_gaps":     [{"hole_id": "r0", "text": "km"}],                            |
> |   "native_text":    "à¤œà¤¬à¤•à¤¿ à¤¯à¤¹ à¤•à¤® à¤¹à¥ˆà¥¤",                                              |
> |   "romanized_text": "Jabki yah km hai.",                                          |
> |   "alignments":     [                                                             |
> |                       {"native": "à¤œà¤¬à¤•à¤¿", "roman": "Jabki"},                        |
> |                       {"native": "à¤¯à¤¹",   "roman": "yah"},                          |
> |                       {"native": "à¤•à¤®",   "roman": "km"},                           |
> |                       {"native": "à¤¹à¥ˆà¥¤",  "roman": "hai."}                          |
> |                     ]                                                             |
> | }                                                                                 |
> |                                                                                   |
> +-----------------------------------------------------------------------------------+
> Dataset Schema & File Structure
> File Layout
> .
> â”œâ”€â”€ train.csv                 # Public training split with input skeletons and gold target JSONs
> â”œâ”€â”€ test.csv                  # Public test split containing input skeletons
> â””â”€â”€ sample_submission.csv     # Example submission file showing required column format
> Data Schema
> Input Training Data (train.csv)
> Column Name | Data Type | Description
> id | String | Unique hash identifier for the record (e.g., ds_0000001_a1b2c3d4).
> language | String | Two-letter ISO language code (e.g., hi, bn, ta, ur).
> native_skeleton | String | Native-script sentence with masked gap placeholders (<n0>, <n1>).
> roman_skeleton | String | Synchronized romanized sentence with masked gap placeholders (<r0>, <r1>).
> hole_ids_json| JSON String | Array of required hole ID strings (e.g., ["n0", "r0"]).
> target_json | JSON String | Ground-truth solution JSON object.
> Input Test Data (test.csv)
> Column Name | Data Type | Description
> idStringUnique hash identifier matching sample_submission.csv.
> languageStringTwo-letter ISO language code.
> native_skeletonStringNative-script sentence with masked gap placeholders. roman_skeletonStringSynchronized romanized sentence with masked gap placeholders. hole_ids_jsonJSON StringArray of required hole ID strings to be restored.
> Sample Submission Data (sample_submission.csv)
> Column Name | Data Type | Description
> idStringUnique hash identifier matching test.csv.
> predictionStringStringified JSON object adhering to the target submission schema.
> Submission Format & Validation Rules
> Submissions must be a single CSV file named submission.csv containing exactly two columns: id and prediction.
> Column Definitions
> id (String): Exactly matches the id from test.csv.
> prediction (Stringified JSON): A JSON string matching the following exact key structure:
> {
> "alignments": [
> {"native": "à¤œà¤¬à¤•à¤¿", "roman": "Jabki"},
> {"native": "à¤¯à¤¹", "roman": "yah"}
> ],
> "native_gaps": [
> {"hole_id": "n0", "text": "à¤¯à¤¹"}
> ],
> "native_text": "à¤œà¤¬à¤•à¤¿ à¤¯à¤¹ à¤•à¤® à¤¹à¥ˆà¥¤",
> "roman_gaps": [
> {"hole_id": "r0", "text": "km"}
> ],
> "romanized_text": "Jabki yah km hai."
> }
> JSON Schema Verification
> {
> "$schema": "http://json-schema.org/draft-07/schema#",
> "type": "object",
> "required": ["alignments", "native_gaps", "native_text", "roman_gaps", "romanized_text"],
> "properties": {
> "native_gaps": {
> "type": "array",
> "items": {
> "type": "object",
> "required": ["hole_id", "text"],
> "properties": {
> "hole_id": { "type": "string" },
> "text": { "type": "string" }
> }
> }
> },
> "roman_gaps": {
> "type": "array",
> "items": {
> "type": "object",
> "required": ["hole_id", "text"],
> "properties": {
> "hole_id": { "type": "string" },
> "text": { "type": "string" }
> }
> }
> },
> "native_text": { "type": "string" },
> "romanized_text": { "type": "string" },
> "alignments": {
> "type": "array",
> "items": {
> "type": "object",
> "required": ["native", "roman"],
> "properties": {
> "native": { "type": "string" },
> "roman": { "type": "string" }
> }
> }
> }
> }
> }
> Evaluation Metric
> Primary Leaderboard Metric
> Submissions are evaluated on the Mean Weighted Hard-Gated Recovery Score in the range
> [
> 0.0
> ,
> 1.0
> ]
> [0.0,1.0]. The metric enforces severe performance drop-offs for structural structural anomalies or non-exact generation matches to prioritize perfect sequence reconstructions.
> Mathematical Formulation
> The final evaluation metric for a submission is the mean score across all
> ð‘
> N test rows:
> FinalÂ Score
> =
> 1
> ð‘
> âˆ‘
> ð‘–
> =
> 1
> ð‘
> Score
> row
> (
> ð‘–
> )
> FinalÂ Score=
> N
> 1
> â€‹
> âˆ‘
> i=1
> N
> â€‹
> Score
> row
> (i)
> â€‹
> Where the individual row score is evaluated via a structural gating condition
> Î¦
> valid
> Î¦
> valid
> â€‹
> :
> Score
> row
> =
> {
> 0.0
> if
> Î¦
> valid
> =
> 0
> 0.25
> â‹…
> ð‘†
> native_gap
> +
> 0.25
> â‹…
> ð‘†
> roman_gap
> +
> 0.20
> â‹…
> ð‘†
> native_full
> +
> 0.20
> â‹…
> ð‘†
> roman_full
> +
> 0.10
> â‹…
> F1
> alignment
> if
> Î¦
> valid
> =
> 1
> Score
> row
> â€‹
> ={
> 0.0
> 0.25â‹…S
> native_gap
> â€‹
> +0.25â‹…S
> roman_gap
> â€‹
> +0.20â‹…S
> native_full
> â€‹
> +0.20â‹…S
> roman_full
> â€‹
> +0.10â‹…F1
> alignment
> â€‹
> â€‹
> ifÂ Î¦
> valid
> â€‹
> =0
> ifÂ Î¦
> valid
> â€‹
> =1
> â€‹
> The Hard-Gating Validation Rule (
> Î¦
> valid
> Î¦
> valid
> â€‹
> )
> A row receives an automatic score of
> 0.0
> 0.0 if it fails either the structural hole validation or the exact alignment element count constraint:
> Î¦
> valid
> =
> ð¼
> (
> keys
> (
> ð‘ƒ
> native_gaps
> )
> =
> =
> keys
> (
> ðº
> native_gaps
> )
> âˆ§
> keys
> (
> ð‘ƒ
> roman_gaps
> )
> =
> =
> keys
> (
> ðº
> roman_gaps
> )
> âˆ§
> âˆ£
> ð´
> pred
> âˆ£
> =
> =
> âˆ£
> ð´
> gold
> âˆ£
> )
> Î¦
> valid
> â€‹
> =I(keys(P
> native_gaps
> â€‹
> )==keys(G
> native_gaps
> â€‹
> )Â âˆ§Â keys(P
> roman_gaps
> â€‹
> )==keys(G
> roman_gaps
> â€‹
> )Â âˆ§Â âˆ£A
> pred
> â€‹
> âˆ£==âˆ£A
> gold
> â€‹
> âˆ£)
> Detailed Component Definitions
> Baseline Character-Level Overlap (
> F1
> char
> F1
> char
> â€‹
> )
> Calculated using a frequency-aware multiset intersection between predicted character sequence
> ð‘ƒ
> P and ground-truth character sequence
> ðº
> G:
> Precision
> char
> =
> âˆ£
> ð‘ƒ
> âˆ©
> ðº
> âˆ£
> âˆ£
> ð‘ƒ
> âˆ£
> ,
> Recall
> char
> =
> âˆ£
> ð‘ƒ
> âˆ©
> ðº
> âˆ£
> âˆ£
> ðº
> âˆ£
> ,
> F1
> char
> =
> 2
> â‹…
> Precision
> char
> â‹…
> Recall
> char
> Precision
> char
> +
> Recall
> char
> Precision
> char
> â€‹
> =
> âˆ£Pâˆ£
> âˆ£Pâˆ©Gâˆ£
> â€‹
> ,Recall
> char
> â€‹
> =
> âˆ£Gâˆ£
> âˆ£Pâˆ©Gâˆ£
> â€‹
> ,F1
> char
> â€‹
> =
> Precision
> char
> â€‹
> +Recall
> char
> â€‹
> 2â‹…Precision
> char
> â€‹
> â‹…Recall
> char
> â€‹
> â€‹
> Gap Recovery Scores (
> ð‘†
> native_gap
> S
> native_gap
> â€‹
> ,
> ð‘†
> roman_gap
> S
> roman_gap
> â€‹
> )
> For all required holes
> ð»
> H in a view, gap scoring heavily favors exact matches (
> 1.0
> 1.0). If a gap's predicted text string does not match exactly, its partial character overlap score is hit with a severe exponential penalty:
> ð‘†
> gap
> =
> 1
> âˆ£
> ð»
> âˆ£
> âˆ‘
> â„Ž
> âˆˆ
> ð»
> Î¨
> (
> â„Ž
> )
> S
> gap
> â€‹
> =
> âˆ£Hâˆ£
> 1
> â€‹
> âˆ‘
> hâˆˆH
> â€‹
> Î¨(h)
> Where:
> Î¨
> (
> â„Ž
> )
> =
> {
> 0.80
> +
> 0.20
> â‹…
> F1
> char
> (
> pred
> â„Ž
> ,
> gold
> â„Ž
> )
> if
> pred
> â„Ž
> =
> =
> gold
> â„Ž
> 0.20
> â‹…
> (
> F1
> char
> (
> pred
> â„Ž
> ,
> gold
> â„Ž
> )
> )
> 2
> if
> pred
> â„Ž
> â‰ 
> gold
> â„Ž
> Where:Â Î¨(h)=
> âŽ©
> âŽ¨
> âŽ§
> â€‹
> 0.80+0.20â‹…F1
> char
> â€‹
> (pred
> h
> â€‹
> ,gold
> h
> â€‹
> )
> 0.20â‹…(F1
> char
> â€‹
> (pred
> h
> â€‹
> ,gold
> h
> â€‹
> ))
> 2
> â€‹
> ifÂ pred
> h
> â€‹
> ==gold
> h
> â€‹
> ifÂ pred
> h
> â€‹
> î€ 
> =gold
> h
> â€‹
> â€‹
> Full Sentence Recovery Scores (
> ð‘†
> native_full
> S
> native_full
> â€‹
> ,
> ð‘†
> roman_full
> S
> roman_full
> â€‹
> )
> Evaluates full sentence reconstructions. Missing an exact character match completely destroys token-overlap cushioning, applying a
> 90
> %
> 90% reduction to the underlying character metric:
> ð‘†
> full
> =
> {
> 1.0
> if
> pred
> text
> =
> =
> gold
> text
> 0.10
> â‹…
> F1
> char
> (
> pred
> text
> ,
> gold
> text
> )
> if
> pred
> text
> â‰ 
> gold
> text
> S
> full
> â€‹
> ={
> 1.0
> 0.10â‹…F1
> char
> â€‹
> (pred
> text
> â€‹
> ,gold
> text
> â€‹
> )
> â€‹
> ifÂ pred
> text
> â€‹
> ==gold
> text
> â€‹
> ifÂ pred
> text
> â€‹
> î€ 
> =gold
> text
> â€‹
> â€‹
> Alignment Multiset F1 (
> F1
> alignment
> F1
> alignment
> â€‹
> )
> Evaluates the predicted array of tuple cells against the gold list using multiset Precision and Recall. Element frequencies are accounted for via
> ð¶
> (
> ð‘Ž
> )
> =
> min
> â¡
> (
> count
> (
> ð‘Ž
> ,
> ð´
> pred
> )
> ,
> count
> (
> ð‘Ž
> ,
> ð´
> gold
> )
> )
> C(a)=min(count(a,A
> pred
> â€‹
> ),count(a,A
> gold
> â€‹
> )):
> Precision
> align
> =
> âˆ‘
> ð‘Ž
> ð¶
> (
> ð‘Ž
> )
> âˆ£
> ð´
> pred
> âˆ£
> ,
> Recall
> align
> =
> âˆ‘
> ð‘Ž
> ð¶
> (
> ð‘Ž
> )
> âˆ£
> ð´
> gold
> âˆ£
> ,
> F1
> alignment
> =
> 2
> â‹…
> Precision
> align
> â‹…
> Recall
> align
> Precision
> align
> +
> Recall
> align
> Precision
> align
> â€‹
> =
> âˆ£A
> pred
> â€‹
> âˆ£
> âˆ‘
> a
> â€‹
> C(a)
> â€‹
> ,Recall
> align
> â€‹
> =
> âˆ£A
> gold
> â€‹
> âˆ£
> âˆ‘
> a
> â€‹
> C(a)
> â€‹
> ,F1
> alignment
> â€‹
> =
> Precision
> align
> â€‹
> +Recall
> align
> â€‹
> 2â‹…Precision
> align
> â€‹
> â‹…Recall
> align
> â€‹
> â€‹
> (Note: As per the gating criteria
> Î¦
> valid
> Î¦
> valid
> â€‹
> , if
> âˆ£
> ð´
> pred
> âˆ£
> â‰ 
> âˆ£
> ð´
> gold
> âˆ£
> âˆ£A
> pred
> â€‹
> âˆ£
> î€ 
> =âˆ£A
> gold
> â€‹
> âˆ£, the entire row drops to
> 0.0
> 0.0.)

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Systematic Review Evidence Delta Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx762gwbpg3jkbcfhz38z9r44x8c5z6d
- DOMAIN exactly as displayed: Sequence To Sequence
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
> The objective is to execute an evidence-driven state transition on one existing systematic-review claim. After receiving a new evidence packet, predict whether the previous claim should be retained, revised, or withdrawn; assign its resulting stance; write the repaired claim; and cite the exact character span that makes that transition valid.
> Each example represents a realistic evidence-maintenance workflow. A previous synthesis has already recorded a claim about an intervention and an outcome. Six newly supplied passages may confirm it, oppose it, show no significant difference, or fail to address the same interventionâ€“outcome relation. Every packet contains strong lexical distractors, including two passages from each observed result direction. Finding a directional phrase or taking a majority vote is therefore insufficient: the cited passage must first be connected to the row's question.
> What makes this task different from static scientific fact verification is that the label is not a property of an isolated claimâ€“passage pair. It is a delta between a stored synthesis state and a newly arrived packet. The same new stance can therefore require different operations depending on the prior state, while an irrelevant packet must trigger withdrawal rather than a generic â€œnot enough informationâ€ class. A valid solution must perform four coupled actions: preserve claim identity, infer the state transition, generate the updated statement, and emit typed, replayable character offsets. A system that only predicts SUPPORTS, REFUTES, or NOINFO, as in conventional verification benchmarks, leaves most of this output undefined.
> The benchmark further introduces controlled evidence collisions: every row contains six passages balanced across observed result directions, but at most one passage resolves the exact interventionâ€“outcome question. This separates semantic applicability from directional wording and makes majority voting or phrase spotting unreliable. The score then evaluates the repair as one structured object through joint operationâ€“stance accuracy, typed evidence-link F1, span IoU, and stance-gated statement fidelity rather than sentence-label accuracy alone.
> The source material consists of licensed expert annotations of intervention, comparator, outcome, and evidence relationships from Evidence Inference 2.0 (DeYoung et al., BioNLP 2020), distributed by its authors under the MIT License. The dataset metadata and release notice preserve the verifiable repository attribution and license, while the participant CSV removes original article IDs, prompt IDs, source splits, and searchable medical strings. Those annotations are used as semantic seeds for newly constructed claim-update episodes; the benchmark does not reproduce the upstream prediction task or its original examples verbatim. Family-local lexical aliases block external answer lookup, while recurring render channels remain learnable from labeled training data.
> All examples originating from the same source article are assigned to one split before any sampling, rendering, aliasing, or hard-negative selection occurs. Row IDs, claim IDs, evidence IDs, row order, passage order, JSON key order, text length, and render channel frequency do not encode the target. Training rows have two renderings per family; every held-out family appears once.
> Output Objective
> Return one JSON object with a single top-level field named claims. It must contain the repair record for the claim in prior_synthesis.
> The repair record contains:
> claim_id: the unchanged opaque identifier from prior_synthesis;
> operation: retain, revise, or withdraw;
> stance: supported, contradicted, mixed, or insufficient;
> statement: the resulting non-empty claim statement;
> evidence: a list of zero or more evidence links.
> Use retain when the new stance agrees with the prior stance, revise when relevant evidence changes the stance, and withdraw when none of the supplied passages directly resolves the question. A withdrawn claim uses the insufficient stance and an explanatory statement, with an empty evidence list.
> Each evidence link contains:
> evidence_id: an identifier present in evidence_update;
> relation: supports, contradicts, or qualifies;
> start: zero-based inclusive character offset in that evidence item's text;
> end: zero-based exclusive character offset in that evidence item's text.
> Evaluation
> Submissions are evaluated with Evidence Delta Repair Fidelity. Higher is better, and the score lies in the interval from 0 to 1.
> For row (i), let:
> (V_i) be the JSON and reference-validity gate;
> (A_i) be operation-and-stance accuracy;
> (E_i) be typed evidence-link F1;
> (B_i) be evidence-span intersection over union;
> (T_i) be statement token F1.
> The row score is
> [
> S_i = V_i \left(0.30A_i + 0.30E_i + 0.20B_i + 0.20T_i\right).
> ]
> The leaderboard score is
> [
> \text{Final Score} = \frac{1}{N}\sum_{i=1}^{N}S_i.
> ]
> Validity gate
> V_i equals 1 when the prediction is valid JSON, follows the exact field schema, uses allowed enum values, references only evidence IDs supplied in that row, and uses integer spans satisfying
> [
> 0 \leq start < end \leq \text{length of the selected evidence text}.
> ]
> An invalid row receives zero. A missing or incorrect claim_id receives no credit for the reference claim.
> Operation-and-stance accuracy
> A_i equals 1 only when both operation and stance exactly match the reference; otherwise it equals 0:
> [
> A_i = \mathbf{1}[operation_p = operation_r ;\land; stance_p = stance_r].
> ]
> Typed evidence-link F1
> An evidence-link key is the pair (evidence_id, relation). Precision and recall are computed over the submitted and reference multisets of keys. Their harmonic mean is E_i. When both multisets are empty, E_i = 1; when only one is empty, E_i = 0.
> Evidence-span overlap
> For a correctly matched evidence-link key, span overlap is character intersection over union:
> [
> IoU = \frac{\max(0,\min(end_p,end_r)-\max(start_p,start_r))}
> {\max(end_p,end_r)-\min(start_p,start_r)}.
> ]
> For every reference evidence link, the grader keeps the highest IoU among submitted links with the same key. B_i is the mean of these values. If both reference and submitted evidence lists are empty, B_i = 1; if only one is empty, B_i = 0.
> Statement token F1
> Statements are lowercased and tokenized into alphanumeric or underscore-delimited tokens. Multiset token precision and recall are combined with their harmonic mean. Because a lexically similar sentence with the opposite conclusion is not a faithful repair, T_i equals this token F1 only when the submitted stance is correct; otherwise T_i = 0.
> Submission
> Submit a UTF-8 CSV file with exactly these columns:
> id (string): test-row identifier;
> repaired_plan (string): JSON prediction.
> Every test ID must occur exactly once. Extra columns, duplicate IDs, missing IDs, NaN, Infinity, comments, and trailing JSON commas are not accepted.
> Example:
> id,repaired_plan
> ED6F17C20B9A02C61D,"{""claims"":[{""claim_id"":""CL131B6F0586E8F41A"",""operation"":""revise"",""stance"":""mixed"",""statement"":""The evidence does not establish a significant difference in ENDPOINT_X between THERAPY_A and THERAPY_B."",""evidence"":[{""evidence_id"":""EV41C352B9857E8D0B"",""relation"":""qualifies"",""start"":96,""end"":218}]}]}"
> Dataset
> The release contains 16,000 rows derived from 9,600 disjoint evidence families:
> train.csv: 12,800 rows from 6,400 families, with two independently ordered renderings per family;
> test.csv: 3,200 rows from 3,200 held-out families, with one rendering per family;
> sample_submission.csv: one schema-valid placeholder row for every test ID.
> The test set consists of 480 public-leaderboard rows and 2,720 private-leaderboard rows. These are a partition of the same 3,200 test rows, not additional examples. Each of the four target stances contributes exactly 25% of train, public test, and private test.
> Columns in train.csv
> id (string): opaque unique row identifier;
> review_question (string): interventionâ€“outcome question to resolve;
> prior_synthesis (JSON string): existing claim before the update;
> evidence_update (JSON string): six candidate evidence passages;
> repair_policy (JSON string): allowed operations, stances, and evidence requirement;
> repaired_plan (JSON string): training-only target.
> Columns in test.csv
> test.csv contains the same five participant input columns but omits repaired_plan.
> Columns in sample_submission.csv
> id (string): test-row identifier copied unchanged from test.csv;
> repaired_plan (JSON string): schema-valid placeholder prediction that participants must replace.
> prior_synthesis JSON
> The object contains claims, a one-item list. Its claim has:
> claim_id (string);
> stance (string);
> statement (string).
> evidence_update JSON
> The object contains documents, a six-item list. Every document has:
> evidence_id (string): row-local opaque identifier;
> text (string): candidate passage to which output offsets refer.
> Passage order is independently shuffled. Exactly two candidate passages are drawn from each observed result direction, but zero or one passage directly resolves the row's question.
> repair_policy JSON
> The object lists allowed_operations, allowed_stances, require_evidence_for, and the natural-language withdraw_when rule. These fields define output semantics but do not identify the correct passage or stance.
> Target repaired_plan JSON
> In train.csv, repaired_plan is the supervised target. The same schema must be predicted for every row of test.csv. It contains claims, a one-item list whose object has:
> claim_id (string): unchanged identifier from prior_synthesis;
> operation (string): one of retain, revise, or withdraw;
> stance (string): one of supported, contradicted, mixed, or insufficient;
> statement (string): non-empty repaired claim text;
> evidence (list): zero or more typed evidence links.
> Every evidence link has evidence_id (string), relation (string: supports, contradicts, or qualifies), start (integer, inclusive), and end (integer, exclusive). The offsets index the text of the referenced item in evidence_update. A withdrawn, insufficient claim uses an empty evidence list.
> What Not To Use
> Do not use row order, identifier format, evidence position, JSON key order, whitespace, passage length, render-channel frequency, or the prior stance alone as target proxies.
> Do not attempt to reverse source aliases, retrieve hidden labels from external corpora, access organizer files, probe the leaderboard, or use any information unavailable to ordinary participants. Solutions should learn evidence-conditioned repairs from train.csv and the participant-facing test fields.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Locale Migration Patch Synthesis Challenge

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7an7wbrqk0sj2pj505jappth88ytxd
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Background
> Internationalization (i18n) infrastructure relies on standardized locale databases to format dates, numbers, currencies, units, and relative time expressions across thousands of software environments.
> Synthesizing precise, deterministic migration patches allows localization pipelines to safely preview, review, and apply automated schema and value updates across major version transitions without requiring manual re-annotation of entire locale trees.
> Overview
> This is a from-scratch CPU sequence-to-sequence challenge. The objective is to construct a sequence model that accepts an old XML locale fragment alongside its descriptive context (input_json) and synthesizes an ordered sequence of patch operations (locale_patch_json) to migrate the data to its newer representation.
> Execution Envelope & Limits
> Compute: 10 CPU cores
> Memory: 62 GB RAM
> Time Limit: 90 minutes (1.5 hours) for complete execution (training and test inference)
> Build Constraints: From scratch (no pre-trained weights, external lookup tables, or internet calls)
> Dataset Description
> The dataset consists of public UTF-8 CSV files generated by the preparation process. Data splitting is controlled by base language groups to guarantee that all regional variants of a given language remain strictly within either the training or test split. Unique identifiers are anonymized with an s2s08_ prefix.
> Public Files
> train.csv: The training dataset containing input contexts and ground-truth locale patch targets.
> test.csv: The evaluation dataset containing input contexts for which predictions must be generated.
> sample_submission.csv: A valid template submission file containing all test IDs paired with default empty patch payloads.
> Dataset Schema
> Plaintext
> +-------------------+------------------------+-------------------------------------------------------------+
> | Column            | Data Type              | Description                                                 |
> +-------------------+------------------------+-------------------------------------------------------------+
> | id                | Opaque UTF-8 string    | Unique identifier assigned to each example (e.g., s2s08_..) |
> | input_json        | Serialized JSON object | Input context containing old XML fragment & release metadata|
> | locale_patch_json | Serialized JSON object | Target payload containing ordered patch operations array    |
> +-------------------+------------------------+-------------------------------------------------------------+
> JSON Structure Definitions
> input_json Payload:
> locale: Opaque locale token or code.
> releases: Release version transition identifier pair (e.g., CLDR 44.1 to CLDR 48.2).
> old_fragment: Raw XML leaf fragment from the earlier version.
> context: Unchanged contextual metadata to aid path synthesis.
> locale_patch_json Payload:
> ordered_patch: An ordered list of patch operation objects, where each object contains:
> op: The operation type (add, replace, or delete).
> path: Canonical LDML path string targeted by the operation.
> value: The string value to insert or update (empty string for deletions).
> Evaluation Metrics
> Each prediction is evaluated independently against the ground-truth payload. The final score is the arithmetic mean of all row scores, bounded to
> [
> 0
> ,
> 1
> ]
> [0,1].
> The metric evaluates the predicted ordered_patch array against ground truth across four weighted components:
> 1. Exact Operation-Path-Value Multiset F1 (55%)
> Full patch elements are represented as complete 3-tuples:
> (
> ð‘œ
> ð‘
> ,
> ð‘
> ð‘Ž
> ð‘¡
> â„Ž
> ,
> ð‘£
> ð‘Ž
> ð‘™
> ð‘¢
> ð‘’
> )
> (op,path,value). Accuracy is scored using multiset F1:
> ð¹
> 1
> full
> =
> 2
> âˆ£
> ð‘ƒ
> full
> âˆ©
> ðº
> full
> âˆ£
> âˆ£
> ð‘ƒ
> full
> âˆ£
> +
> âˆ£
> ðº
> full
> âˆ£
> F1
> full
> â€‹
> =
> âˆ£P
> full
> â€‹
> âˆ£+âˆ£G
> full
> â€‹
> âˆ£
> 2âˆ£P
> full
> â€‹
> âˆ©G
> full
> â€‹
> âˆ£
> â€‹
> 2. Operation-Path Multiset F1 (25%)
> Partial patch elements evaluate structural targeting without penalizing value errors, represented as 2-tuples:
> (
> ð‘œ
> ð‘
> ,
> ð‘
> ð‘Ž
> ð‘¡
> â„Ž
> )
> (op,path). Accuracy is scored using multiset F1:
> ð¹
> 1
> partial
> =
> 2
> âˆ£
> ð‘ƒ
> partial
> âˆ©
> ðº
> partial
> âˆ£
> âˆ£
> ð‘ƒ
> partial
> âˆ£
> +
> âˆ£
> ðº
> partial
> âˆ£
> F1
> partial
> â€‹
> =
> âˆ£P
> partial
> â€‹
> âˆ£+âˆ£G
> partial
> â€‹
> âˆ£
> 2âˆ£P
> partial
> â€‹
> âˆ©G
> partial
> â€‹
> âˆ£
> â€‹
> 3. Ordered Operation-Path LCS-F1 (15%)
> Evaluates whether structural operations follow the correct relative sequential order using Longest Common Subsequence (LCS) F1 over partial 2-tuples
> (
> ð‘œ
> ð‘
> ,
> ð‘
> ð‘Ž
> ð‘¡
> â„Ž
> )
> (op,path):
> ð¹
> 1
> LCS
> =
> 2
> Ã—
> ð¿
> ð¶
> ð‘†
> (
> ð‘ƒ
> order
> ,
> ðº
> order
> )
> âˆ£
> ð‘ƒ
> order
> âˆ£
> +
> âˆ£
> ðº
> order
> âˆ£
> F1
> LCS
> â€‹
> =
> âˆ£P
> order
> â€‹
> âˆ£+âˆ£G
> order
> â€‹
> âˆ£
> 2Ã—LCS(P
> order
> â€‹
> ,G
> order
> â€‹
> )
> â€‹
> 4. Patch-Length Agreement (5%)
> Measures total array length agreement between predicted length
> âˆ£
> ð‘ƒ
> âˆ£
> âˆ£Pâˆ£ and ground-truth length
> âˆ£
> ðº
> âˆ£
> âˆ£Gâˆ£:
> ð‘†
> length
> =
> {
> 1.0
> if
> âˆ£
> ð‘ƒ
> âˆ£
> =
> âˆ£
> ðº
> âˆ£
> max
> â¡
> (
> 0.0
> ,
> 1.0
> âˆ’
> âˆ£
> âˆ£
> ð‘ƒ
> âˆ£
> âˆ’
> âˆ£
> ðº
> âˆ£
> âˆ£
> max
> â¡
> (
> 1
> ,
> âˆ£
> ð‘ƒ
> âˆ£
> ,
> âˆ£
> ðº
> âˆ£
> )
> )
> otherwise
> S
> length
> â€‹
> ={
> 1.0
> max(0.0,1.0âˆ’
> max(1,âˆ£Pâˆ£,âˆ£Gâˆ£)
> âˆ£âˆ£Pâˆ£âˆ’âˆ£Gâˆ£âˆ£
> â€‹
> )
> â€‹
> ifÂ âˆ£Pâˆ£=âˆ£Gâˆ£
> otherwise
> â€‹
> Combined Row Score Formula
> RowÂ Score
> =
> 0.55
> â‹…
> ð¹
> 1
> full
> +
> 0.25
> â‹…
> ð¹
> 1
> partial
> +
> 0.15
> â‹…
> ð¹
> 1
> LCS
> +
> 0.05
> â‹…
> ð‘†
> length
> RowÂ Score=0.55â‹…F1
> full
> â€‹
> +0.25â‹…F1
> partial
> â€‹
> +0.15â‹…F1
> LCS
> â€‹
> +0.05â‹…S
> length
> â€‹
> Additional Rules
> Empty-vs-empty sequence components score 1.0; empty-vs-nonempty components score 0.0.
> Non-finite values or malformed outputs receive a score of 0.0 for that row.
> All component and row scores are clamped to
> [
> 0
> ,
> 1
> ]
> [0,1].
> Sample Submission Format
> Submit a UTF-8 CSV with exactly two columns in this order: id, locale_patch_json.
> Code snippet
> id,locale_patch_json
> s2s08_0123456789abcdef,"{""ordered_patch"":[]}"
> Every test id must appear exactly once.
> Extra, missing, or duplicate id rows will invalidate the submission.
> A row with syntactically invalid JSON receives a score of 0.0 for that row.
> What Not To Use
> Use only the released challenge files.
> Do not use network access, external websites, or hidden identifier lookups.
> Do not use external corpora, pre-trained model weights, or synthetic training labels.
> All model fitting, lexicon generation, and calibration must take place inside the submitted solver script.
> Test rows may be used only for inference. Adapting to or pseudo-labeling test rows is strictly prohibited.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Hardware Patch Set Selection and Dependency Ordering

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74sqwsc0a9dt278m05426fbd8c5fdq
- DOMAIN exactly as displayed: Sequence To Sequence
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
> For each hardware failure case, predict which candidate patch cards belong to the verified repair, place those cards in dependency order, and classify how broadly the repair crosses the design. This is a structured code-understanding task built from real accepted repairs, not a request to generate unrestricted source code.
> In pre-silicon triage, several edits can look locally plausible while only one coordinated subset satisfies the failure report, interface dependencies, and verification evidence. Selecting an incomplete set can preserve the original failure; selecting an unrelated hunk can introduce a new regression. The challenge models this intermediate engineering decision after candidate edits exist but before they are accepted as one repair.
> Each case contains a sanitized failure report, a verification excerpt, and eight shuffled before-and-after patch cards. Some cards are genuine parts of the accepted fix. The remaining cards are difficult decoys drawn from other repair cases in the same repository and on the same side of the train/test boundary. Paths, revisions, URLs, and source identifiers are removed, while code identifiers are consistently renamed within each case.
> The three predictions answer different engineering questions:
> | Output | Meaning |
> |---|---|
> | `repair_coalition` | The set of patch cards that belong to the accepted repair. |
> | `repair_order` | The accepted cards in their original repair dependency order. |
> | `repair_scope` | Whether the repair is local, crosses modules, propagates through an interface, or changes a verification contract. |
> Dataset
> The prepared collection contains 1,485 training cases and 360 test cases. All variants of one original hardware bug remain in one split, and every decoy card is sourced from that same split. Exact patch packets and individual patch-card payloads are checked for duplication across train and test.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Public inputs and all three target columns for training. |
> | `test.csv` | Public inputs for hidden test cases. |
> | `sample_submission.csv` | A schema-valid baseline submission. |
> Input Columns
> | Column | Data type | Description |
> |---|---|---|
> | `case_id` | string | Opaque unique case identifier. |
> | `failure_packet` | string | Sanitized description of the observed hardware failure. |
> | `candidate_patch_packet` | JSON string | Array of eight cards. Each card has `card`, `unit_kind`, `before`, and `after` fields. Card IDs are `H1` through `H8`. |
> | `verification_packet` | string | Sanitized reproducer signal or verification-diff excerpt. |
> unit_kind is one of rtl, implementation, verification, integration, or documentation. It describes the engineering role of the hidden source file, not whether the card is correct.
> Target Columns
> | Column | Data type | Valid form |
> |---|---|---|
> | `repair_coalition` | pipe-delimited string | One to four unique card IDs, such as `H2|H5|H8`. Order is ignored for this field. |
> | `repair_order` | greater-than-delimited string | The same accepted cards in order, such as `H5>H2>H8`. |
> | `repair_scope` | categorical string | `local_unit`, `cross_module`, `interface_chain`, or `verification_contract`. |
> The training scope distribution is:
> | Scope | Rows |
> |---|---:|
> | `local_unit` | 859 |
> | `cross_module` | 449 |
> | `interface_chain` | 112 |
> | `verification_contract` | 65 |
> Evaluation
> Submissions are evaluated with the Verified Patch Coalition Score:
> Score = 0.50 * CoalitionScore
> + 0.30 * RepairOrderScore
> + 0.20 * ScopeScore
> Minimum score: 0.0
> Maximum score: 1.0
> Higher is better.
> CoalitionScore
> For one case, let T be the true card set and P the submitted card set:
> set_f1(T, P) = 2 * |T intersect P| / (|T| + |P|)
> An invalid coalition receives 0. CoalitionScore is the mean row-level set F1.
> RepairOrderScore
> The order strings are split on >. Let d be token-level Levenshtein distance:
> edit_similarity = 1 - d(T, P) / max(|T|, |P|, 1)
> row_order_score = 0.35 * edit_similarity + 0.65 * exact_order_match
> RepairOrderScore is the mean row score. A malformed sequence receives 0.
> The submitted order must contain exactly the same card set as the submitted repair_coalition. An order containing a missing or additional card receives 0 for this component, even when the order string is otherwise well formed.
> ScopeScore
> For every scope class present in the hidden answers, recall is the fraction of rows of that true class assigned the same class. ScopeScore is the unweighted mean of those per-class recalls. This prevents the common local_unit class from dominating the component.
> Submission Format
> Write the final CSV to ./working/submission.csv with exactly these columns in this order:
> case_id,repair_coalition,repair_order,repair_scope
> Example:
> case_id,repair_coalition,repair_order,repair_scope
> c_07f6229e60ce6fe1b335,H2|H5|H8,H5>H2>H8,interface_chain
> The grader rejects extra or reordered columns, duplicate IDs, missing IDs, unknown IDs, and extra rows. Coalition and order fields are limited to four unique card IDs and 40 characters.
> Why This Matters
> Real hardware repairs often combine a small causal edit with propagation changes in neighboring modules or verification logic. Selecting a plausible-looking hunk is not enough: a usable repair portfolio must include the complete coalition and preserve the dependency order in which the changes make sense.
> Expected And Allowed Methods
> Suitable approaches include compact code encoders, learned cross-encoders over the failure and candidate cards, listwise selection models, and constrained decoders that enforce set and order validity. CPU-friendly pretrained code representations may be used locally within the runtime limit.
> What Not To Use
> Do not derive predictions from case_id, row order, source URLs, hidden repository identities, or reverse lookup of original pull requests. Do not exploit duplicate handling, malformed CSV behavior, grader behavior, or submission ordering. Lookup tables, filename rules, and deterministic keyword-only patch selectors are not valid primary solving methods. The core decision must come from a learned model of the failure, verification evidence, and patch semantics.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Community Post Revision Patch Challenge

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76dt2aecsaf7zr8c095n9vr58c25tq
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Background and Overview
> The Community Post Revision Patch is a machine learning challenge focused on natural language processing and structured text generation. The primary objective is to perform from-scratch human revision patch generation. Specifically, participants must generate the canonical token patch that transforms a post body into its updated version, guided solely by the human editor's revision summary.
> This is strictly a from-scratch track: models must be fitted exclusively on the supplied public training split. Furthermore, all evaluated solutions are subject to a strict computational envelope and must run on CPU infrastructure alone.
> Dataset Information
> The challenge provides a set of public files generated to support the training and evaluation of your models. Based on the data preparation pipeline, the released files are:
> train.csv: The primary training set containing the prior post text, the editor's summary, and the gold-standard patch JSON.
> test.csv: The evaluation set. Models must predict the valid patch JSON for these rows based on the provided input JSON.
> sample_submission.csv: A valid submission template providing the exact header and one weak valid payload ({"ops":[]}) per test row.
> DATA_MANIFEST.json: A metadata file containing row counts for the train and test splits, and the required payload-column name.
> Data Schema and Contract
> The following ASCII table outlines the structure of the data files and the strict JSON contracts required for the input and output features:
> +-------------+-------------------+-----------------------------------------------------------------------+
> | Column Name | Data Type         | Description                                                           |
> +-------------+-------------------+-----------------------------------------------------------------------+
> | id          | UTF-8 String      | Opaque string identifier. IDs are randomized hashes and must not be   |
> |             |                   | used to infer target labels or source metadata.                       |
> +-------------+-------------------+-----------------------------------------------------------------------+
> | input_json  | UTF-8 JSON Object | Serialized inside CSV. Contains `previous_text` (string) and          |
> |             |                   | `edit_summary` (string). Tokenization relies on Unicode \w+|[^\w\s]. |
> +-------------+-------------------+-----------------------------------------------------------------------+
> | patch_json  | UTF-8 JSON Object | Serialized inside CSV. Represents the canonical token patch.          |
> | (Payload)   |                   | Structure: `ops: [{at: integer, delete: [token,...], insert:          |
> |             |                   | [token,...]}, ...]`                                                   |
> |             |                   | Indices address the original token list. Operations must be applied   |
> |             |                   | sequentially from the greatest `at` index to the least.               |
> +-------------+-------------------+-----------------------------------------------------------------------+
> Evaluation Metric
> The grader script evaluates the predicted patch against the gold-standard patch. For each row, the score is determined using two distinct factors:
> Operation Set F1 (P): Evaluates the precision of the exact canonical operations. Let P be the set of predicted operations and G be the gold operations represented as (at, delete tuple, insert tuple).
> ð¹
> 1
> (
> ð‘ƒ
> ,
> ðº
> )
> =
> 1.0
> F1(P,G)=1.0 when both sets are empty.
> ð¹
> 1
> (
> ð‘ƒ
> ,
> ðº
> )
> =
> 0.0
> F1(P,G)=0.0 when only one set is empty.
> Otherwise,
> ð¹
> 1
> (
> ð‘ƒ
> ,
> ðº
> )
> =
> 2
> âˆ£
> ð‘ƒ
> âˆ©
> ðº
> âˆ£
> âˆ£
> ð‘ƒ
> âˆ£
> +
> âˆ£
> ðº
> âˆ£
> F1(P,G)=
> âˆ£Pâˆ£+âˆ£Gâˆ£
> 2âˆ£Pâˆ©Gâˆ£
> â€‹
> .
> Sequence Matcher Ratio (R): Measures the similarity between the token sequences produced by applying the submitted patch and the gold patch to the original text.
> Row Score: Calculated using the weighted formula
> 0.65
> ð‘ƒ
> +
> 0.35
> ð‘…
> 0.65P+0.35R. Note: Any invalid patch application (e.g., negative indices, out-of-bounds indices, or non-matching deletion targets) raises an error during patch application and results in a score of
> 0.0
> 0.0 for that row.
> Final Score: The final score is the arithmetic mean of all row scores across the test set, clamped strictly to the interval
> [
> 0
> ,
> 1
> ]
> [0,1]. A perfect answer scores exactly
> 1.0
> 1.0.
> Submission Format
> Submissions must be a single UTF-8 encoded CSV file containing exactly two columns in the following explicit order: id,patch_json.
> Submission Rules:
> IDs must occur exactly once and must exactly match the IDs present in test.csv.
> The payload cell (patch_json) must contain a valid JSON string matching the operation contract defined in the data schema.
> A malformed JSON payload in a single row receives a zero score for that specific row without invalidating otherwise well-formed rows.
> Fatal Errors: Submitting a file with the wrong header, duplicate IDs, missing/extra IDs, or an incorrect total row count yields an overall score of
> 0.0
> 0.0.
> Example Submission Row:
> id,patch_json
> edit_0123456789abcdef,"{""ops"":[]}"
> Resource Envelope
> Evaluated solutions run under a strict, containerized computational envelope:
> Hardware Limit: A maximum of 10 CPU cores and 62 GB of RAM. GPU execution is completely unavailable.
> Time Limit: Solutions must successfully execute and output their predictions within a 90-minute window.
> Network Constraint: Network access is completely disabled.
> Rules and What Not To Use
> To preserve the integrity of this from-scratch challenge, participants must strictly adhere to the following constraints:
> No External Assets: You must not use external datasets, pretrained weights, hosted foundation models, APIs, or network lookups.
> No Source Hunting: Do not perform source-record searches, reverse-image/source matching, or participate in answer sharing.
> No Leakage Exploitation: Do not attempt to utilize raw organizer files, hidden answers, source IDs, URLs, or timestamps.
> No Label Inference: Do not attempt to infer labels from filenames or row IDs. They are completely opaque and randomized by design.
> Strict Isolation: You must build, train, and infer only using the released public files.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Whale-Song Next-Cycle Phrase-Bank Reassembly

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx773v673b8p8498j3xzkqjz4s8b4ypq
- DOMAIN exactly as displayed: Sequence To Sequence
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
> Humpback-whale song is organized as an ordered sequence of phrases, and successive renditions preserve broad structure while changing phrase choice, repetition, and timing. Your task is to reconstruct position-marked contiguous blocks from a session's next observed song cycle.
> Cases sharing a transition_id belong to one current-to-next-cycle transition. They provide the same immediately preceding current_cycle, up to two earlier non-target anchor cycles, and one transition-shared unordered candidate_phrase_types bank. The bank contains every exact phrase type used anywhere in the hidden next cycle plus similar phrases seen only in the visible context. Each case identifies one block position; you must decide which phrase IDs belong in that block, how often each repeats, and in what order.
> Dataset
> Public Files
> train.jsonl contains 405 labeled cases from 76 transitions and 48 sessions, one compact JSON object per line.
> validation.jsonl contains 112 labeled cases from 28 transitions and 16 sessions.
> test.jsonl contains 106 unlabeled cases from 23 transitions and 16 sessions; together they cover 679 hidden target phrase occurrences and omit only the target field.
> sample_submission.csv contains one row per test case and exactly two columns: string case_id and string ordering_json; every provided ordering_json is the zero-score dummy [].
> dataset_summary.json records the schema version, raw-source counts, case and transition counts, construction rules, submission contract, and metric definition.
> JSONL Features
> Field: case_id; type: string; description: opaque identifier for one target block, such as C0123456789ABCDEF.
> Field: transition_id; type: string; description: opaque identifier shared by all sibling blocks from one current-to-next-cycle transition, such as T0123456789ABCDEF.
> Field: history; type: array<object>; description: zero to two earlier non-target anchor-cycle objects in chronological order.
> Field: history[].phrases; type: array<array<string>>; description: ordered phrase occurrences in one anchor cycle, where each inner array is one ordered phrase of Uxxx unit tokens.
> Field: current_cycle; type: object; description: the observed cycle immediately preceding the hidden next cycle.
> Field: current_cycle.phrases; type: array<array<string>>; description: ordered phrase occurrences in the current cycle using the same nested representation as history.
> Field: target_block_index; type: integer; description: one-based position of this contiguous block within its transition.
> Field: target_block_count; type: integer; description: total number of contiguous target blocks for the transition.
> Field: candidate_phrase_types; type: array<object>; description: transition-shared shuffled phrase dictionary containing every phrase type from the complete hidden next cycle plus context-only decoys.
> Field: candidate_phrase_types[].phrase_id; type: string; description: transition-local Pxxx identifier for one exact unit sequence.
> Field: candidate_phrase_types[].units; type: array<string>; description: ordered Uxxx transcription-unit sequence defining the phrase type; each token denotes equality of one nominal acoustic-unit class within the transition, not duration or numeric magnitude.
> Field: target_phrase_count; type: integer; description: required length of every nonempty prediction for this block; hidden test values range from 5 to 7.
> Field: target; type: array<string>; description: ordered gold Pxxx phrase-ID sequence, present only in train and validation.
> Each exact ordered unit sequence has one transition-local phrase ID, so repeated occurrences of the same phrase reuse the same Pxxx value. Sibling blocks share the same Uxxx mapping, phrase IDs, visible context, and candidate bank. Tokens have no meaning across different transitions.
> Objective
> For every test case, emit a JSON list of candidate phrase IDs that reconstructs the indicated block of the next cycle. The list must contain exactly target_phrase_count entries and may repeat IDs. Candidate display order is randomized and is not a target-order hint.
> Evaluation
> For each transition_id, predictions and gold blocks are concatenated in ascending target_block_index order. Let p_t and g_t be the resulting full predicted and target sequences for transition t. The final score is:
> score = max(0, 1 - sum_t LevenshteinDistance(p_t, g_t) / sum_t length(g_t))
> Levenshtein distance counts candidate-ID insertions, deletions, and substitutions. The score ranges from 0 to 1 and is maximized. An exact reconstruction scores 1; a submission containing [] for every row scores 0. The hidden denominator is 679 target phrase occurrences, and one block contains at most 7, so changing one row can affect at most 7 / 679 = 0.010310 of the score.
> Submission
> Required Format
> Submit a CSV with exactly these columns in this order:
> case_id,ordering_json
> The submission must contain every test case_id exactly once and no extra IDs. ordering_json must be valid JSON. A nonempty value must be a list of exactly target_phrase_count strings, every string must be a phrase ID from that case's bank, and repeated valid IDs are allowed. The empty list [] is the only length exception and exists solely to make the sample submission a zero-score format template. Malformed JSON, unknown IDs, wrong lengths, missing rows, duplicate rows, extra rows, missing values, or reordered or extra columns are rejected.
> Valid Submission Example
> The following illustrative rows use valid lengths of five and seven; replace the identifiers and lists with the actual test cases and match each case's declared target_phrase_count:
> case_id,ordering_json
> C0123456789ABCDEF,"[""P004"",""P004"",""P011"",""P006"",""P004""]"
> C0FEDCBA987654321,"[""P003"",""P002"",""P002"",""P008"",""P008"",""P005"",""P003""]"
> Rules
> Use only the supplied public challenge files. External source lookup, matching cases back to source rows or public mirrors, private-file access, hardcoded test answers, and grader exploitation are prohibited. Solutions must run offline on CPU within the platform limit and must not download data, install packages, or require a GPU.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Auditable OCR Repair Transduction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78px7tychqkkfr63q5w4nv698c1fae
- DOMAIN exactly as displayed: Sequence To Sequence
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
> Digitized historical newspapers become searchable and analyzable only when their text is transcribed reliably. Older typefaces, worn print, page noise, and layout variation can cause OCR systems to drop characters, invent characters, or confuse similar glyphs. Those errors interfere with archival search, text mining, and close reading.
> This benchmark uses bounded regions from German historical newspaper pages. Its diplomatic transcriptions preserve historical spelling and character choices rather than silently modernizing the text. The challenge is therefore to repair recognition errors without rewriting authentic language from the page.
> Task
> Treat each ocr_primary string as a short source tape with a cursor. Recover an executable repair trace that advances across that tape and reproduces the diplomatic newspaper transcription. The trace must identify what to keep, delete, substitute, or insert; submitting corrected prose directly is not allowed.
> This representation makes every prediction replayable and locally auditable. It also prevents a solver from hiding broad rewriting behind a superficially fluent transcription. A successful system must remove genuine OCR damage while preserving historical spelling, glyph choices, and typography that belong in the source.
> Each record contains two observations of the same bounded newspaper region. The primary sequence was recognized from the full-resolution scan, and ocr_secondary was recognized from a binarized version. They are outputs of the same OCR engine, so the second sequence is paired preprocessing evidence, not an independent ensemble member. Bounded OCR context from the neighboring regions is included as additional evidence.
> The required output is a canonical variable-length operation sequence. This is a constrained sequence-to-sequence problem: the predicted trace consumes ocr_primary under a fixed grammar and must terminate exactly at the end of that source.
> Data Files
> train.csv contains inputs and labeled repair programs.
> test.csv contains inputs without repair programs.
> sample_submission.csv contains the required test identifiers and the dummy ABSTAIN value.
> Record Schema
> | Column | Type | Description |
> | --- | --- | --- |
> | case_id | string | Opaque example identifier |
> | ocr_primary | UTF-8 string | Source sequence consumed by the repair program |
> | ocr_secondary | UTF-8 string | Auxiliary OCR sequence from alternative image preprocessing |
> | context_before | UTF-8 string | Bounded preceding-region OCR context, possibly empty |
> | context_after | UTF-8 string | Bounded following-region OCR context, possibly empty |
> | repair_program | string | Canonical edit program; present only in train.csv and submissions |
> The split unit is larger than an individual text region. Every region from one newspaper page stays on the same side of the split, and pages joined by exact duplicate diplomatic regions are grouped together. Original filenames, page identifiers, and region identifiers are removed from the solver-facing tables.
> Illustrative Record
> The following synthetic row demonstrates the table layout and is not a quotation from the corpus. Its labeled program transforms cat into cut.
> | case_id | ocr_primary | ocr_secondary | context_before | context_after | repair_program |
> | --- | --- | --- | --- | --- | --- |
> | demo_0001 | cat | cat | empty | empty | K S:75 K E |
> Output Language
> The repair trace is a space-separated sequence drawn from five token forms:
> K copies the next character of ocr_primary and consumes it.
> D deletes the next character of ocr_primary and consumes it.
> S:HEX substitutes the next source character with the Unicode scalar encoded by HEX and consumes the source character.
> I:HEX inserts the Unicode scalar encoded by HEX without consuming a source character.
> E ends the program after the complete source has been consumed.
> HEX contains one to six hexadecimal digits. Surrogate code points and values above 10FFFF are invalid. E must be the final token. Programs may contain at most 1,800 tokens and may decode to at most 800 characters.
> For example, the source cat can be transformed to cut with:
> K S:75 K E
> Every training trace is derived deterministically from its aligned primary OCR and diplomatic target. Multiple valid traces can occasionally decode to the same string, but structural credit is tied to the canonical alignment supplied by the benchmark.
> Evaluation
> The grader first executes each submitted trace against its corresponding source tape. Let d(source, target) be the Unicode-character Levenshtein distance from ocr_primary to the private diplomatic transcription, and let d(prediction, target) be the distance after executing the predicted trace. Every scored source differs from its private target, so d(source, target) is nonzero. This is a property of the test data, not a submission-validity rule: an allK trace is accepted and graded, but it leaves the source unchanged and therefore receives no error-reduction credit. Per-record error reduction is:
> g = clip((d(source, target) - d(prediction, target)) / d(source, target), 0, 1)
> The mean of g over the complete test set is G. A second view evaluates whether the trace repaired the text in the expected way. Exact canonical edit events are pooled across test records to compute separate F_S, F_D, and F_I values for substitutions, deletions, and insertions. An event includes its source-cursor position and the substituted, deleted, or inserted character.
> Text recovery and the three operation families are combined through arithmetic and geometric components:
> A = 0.40*G + 0.20*F_S + 0.20*F_D + 0.20*F_I
> M = G^0.40  *F_S^0.20*  F_D^0.20 * F_I^0.20
> score = 0.50*A + 0.50*M
> Higher is better. The arithmetic term retains useful partial credit; the geometric term requires capability across the full repair language, so strong substitution performance cannot conceal failure on deletion or insertion events. Replaying ocr_primary unchanged scores 0, and the reserved ABSTAIN value also scores 0. The exact private canonical traces score 1.
> Submission
> Write ./working/submission.csv with exactly these columns:
> case_id,repair_program
> ocr_0123456789abcdef,K K S:65 K E
> Include every test case_id exactly once. Missing values, extra columns, duplicate or absent identifiers, unknown operations, invalid Unicode scalars, source text left unconsumed at E, and outputs beyond the documented bounds are rejected.
> CPU-feasible approaches may learn character confusions, sparse contextual features, structured edit models, or constrained decoders from the supplied tables. External answer files, external corpora, network services, APIs, runtime installation, and solve-time downloads are outside the task.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Prompt Template Compiler Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx782zqnt060qtjrwdqf2h67qx8c27t7
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Prompt Template Compiler Repair
> 1. Overview
> Prompt templates are small programs that convert a dataset record into the text shown to a language model and the target text that the model should produce. For example, a template may insert a question field, loop over answer options, or use an {% if ... %} block to select a target.
> This challenge uses human-authored Jinja templates derived from PromptSource, an open collection of prompts for many natural-language datasets. The source families cover tasks such as question answering, sentiment analysis, paraphrase detection, natural-language inference, summarization, and multiple-choice reasoning. The templates therefore use different fields and formatting conventions, but share the Jinja prompt-programming language.
> Multiple parts of each template have been removed and replaced by numbered markers. Your job is to predict:
> the missing Jinja text for every marker;
> every dataset field referenced by the complete original template;
> whether the template produces a class label or generated text; and
> whether its answer choices are absent, static, or dynamically generated.
> In simple terms: repair the broken prompt program and describe how the repaired program runs.
> 2. Dataset scale and split
> The expert release contains 6,055 examples:
> +-------+------+------------------+------------+--------------+-------------+-------------+
> | Split | Rows | Dataset families | Two holes | Three holes  | Four holes  | Five holes   |
> +-------+------+------------------+------------+--------------+-------------+-------------+
> | Train | 5,062| 141              | 1,711      | 1,412        | 1,057       | 882         |
> | Test  | 993  | 38               | 374        | 304          | 181         | 134         |
> | Total | 6,055| 179              | 2,085      | 1,716        | 1,238       | 1,016       |
> +-------+------+------------------+------------+--------------+-------------+-------------+
> Splitting is performed by dataset_family. Every example from one family is placed entirely in train or entirely in test, so the two splits have zero family overlap. This prevents a solution from succeeding by memorizing another template from the same family. IDs are opaque and contain no target information.
> Every row requires at least two repairs and contains a contiguous prefix of hole markers:
> a two-hole row contains <HOLE_0> and <HOLE_1>; and
> a three-hole row additionally contains <HOLE_2>;
> a four-hole row additionally contains <HOLE_3>; and
> a five-hole row additionally contains <HOLE_4>.
> Markers are never skipped. For example, a row cannot contain <HOLE_0> and <HOLE_2> without <HOLE_1>.
> 3. Data files and columns
> train.csv
> +----------------------+----------------------------+----------------------------------------------+
> | Column               | Type                       | Description                                  |
> +----------------------+----------------------------+----------------------------------------------+
> | id                   | string                     | Opaque unique row ID.                        |
> | dataset_family       | string                     | Source dataset family, such as winogrande or |
> |                      |                            | paws-x.                                      |
> | broken_template      | string                     | Prompt program with two to five Jinja        |
> |                      |                            | fragments replaced by hole markers.          |
> | field_cards_json     | JSON array of strings      | Candidate dataset-field names. Includes all  |
> |                      |                            | true fields plus up to 20 plausible decoys   |
> |                      |                            | from the same family. A candidate is not     |
> |                      |                            | necessarily used.                            |
> | answer_choice_card   | string                     | Original answer-choice information. none     |
> |                      |                            | means no choices; plain text represents      |
> |                      |                            | static choices; Jinja delimiters represent   |
> |                      |                            | dynamically computed choices.                |
> | hole_kinds_json      | JSON array of strings      | Expected hole kind in marker order:          |
> |                      |                            | jinja_expression, jinja_control, or          |
> |                      |                            | jinja_comment. Length equals marker count.   |
> | label                | JSON object encoded as a   | Gold prediction object using the submission  |
> |                      | CSV string                 | schema in Section 5.                         |
> +----------------------+----------------------------+----------------------------------------------+
> test.csv
> Contains the same input columns as train.csv, but does not contain label.
> sample_submission.csv
> Contains exactly two columns:
> +----------------------+--------------------------------+----------------------------------------------+
> | Column               | Type                           | Description                                  |
> +----------------------+--------------------------------+----------------------------------------------+
> | id                   | string                         | One test ID copied exactly from test.csv.    |
> |                      |                                | Every test ID appears once.                  |
> | prediction           | JSON object encoded as a        | Placeholder prediction using the same        |
> |                      | CSV string                     | four-key JSON schema required for           |
> |                      |                                | submissions.                                 |
> +----------------------+--------------------------------+----------------------------------------------+
> The file demonstrates CSV quoting and JSON escaping. Its predictions are deliberately weak and are not a modeling baseline.
> 4. Example input
> A two-hole row may look like this (line breaks abbreviated for readability):
> dataset_family: winogrande
> broken_template: <HOLE_0> What does _ refer to? {{ option1 }} or {{ option2 }}?
> ||| {% if answer == '1' %} {{ option1 }} {% else %} {{ option2 }} <HOLE_1>
> field_cards_json: ["answer","int","option1","option2","sentence"]
> answer_choice_card: {{option1}} ||| {{option2}}
> hole_kinds_json: ["jinja_expression","jinja_control"]
> Here, int may be a decoy, the first missing fragment is an output expression, and the second is a control fragment such as a closing block. The prediction must repair both holes and also report the fields and execution modes for the complete template.
> 5. Submission format
> Submit one file named submission.csv with exactly two columns in this order:
> id,prediction
> There must be exactly one row for every test ID. Missing, unknown, empty, or duplicate IDs invalidate the entire submission. Extra columns also invalidate the entire submission.
> prediction must be a JSON object with exactly four keys:
> {
> "repairs": [
> {"hole": 0, "text": "{{ question }}"},
> {"hole": 1, "text": "{% endif %}"}
> ],
> "used_fields": ["answer_choices", "question"],
> "target_mode": "classification",
> "choice_mode": "dynamic"
> }
> Complete CSV example
> The following is a correctly formatted one-row submission.csv. Because JSON uses double quotes, CSV escaping writes each internal double quote twice:
> id,prediction
> ptr_9d9d4fc3a4a1d27e,"{""repairs"":[{""hole"":0,""text"":""{{ sentence1 }}""},{""hole"":1,""text"":""{{ sentence2 }}""},{""hole"":2,""text"":""{{ answer_choices[label] }}""}],""used_fields"":[""answer_choices"",""label"",""sentence1"",""sentence2""],""target_mode"":""classification"",""choice_mode"":""static""}"
> This example illustrates file formatting only. Participants must generate the appropriate prediction for each test row and must include all 993 test IDs exactly once.
> Rules:
> repairs must contain one object for each predicted hole. hole is an integer from 0 through 4, and text is the non-empty replacement string.
> Repair objects may appear in any array order, but every hole index must be unique.
> For a complete prediction, the repair indices must equal the markers in that row. Thus a two-hole row should predict indices {0,1}.
> used_fields is the set of all fields referenced anywhere in the complete original template, not only inside the repaired fragments. Jinja identifiers are case-sensitive.
> target_mode is exactly classification or generation.
> choice_mode is exactly none, static, or dynamic.
> choice_mode="none" should be paired with target_mode="generation".
> Additional JSON keys, malformed JSON, invalid types, or oversized predictions score zero for that row.
> 6. Evaluation metric
> Let G be the set of gold hole indices for a row and P the set of predicted hole indices. For each gold hole i, let g_i be its gold text and let p_i be the predicted text, or the empty string if i was not predicted.
> 6.1 Text normalization and structural tokens
> The grader tokenizes repair text into Jinja delimiters, comparison operators, identifiers, and remaining non-whitespace symbols. Examples of tokens are {{, question, |, lower, }}, {%, if, and ==. Tokens are case-folded for repair comparison.
> norm(x) is the structural-token sequence of x joined with single spaces. Therefore differences in whitespace do not matter, while identifiers, operators, delimiters, filters, and control words do matter.
> 6.2 Component formulas
> Complete normalized repair exactness
> Exact = I[P = G and norm(p_i) = norm(g_i) for every i in G]
> where I[condition] is 1 when the entire condition is true and 0 otherwise. This component is all-or-nothing at row level: repairing four out of five holes does not earn the 65% exactness component. Such a prediction can still earn partial credit through structural-token F1 and the other components.
> Structural-token F1
> For each gold hole, token occurrences are treated as multisets. If TP_i is the number of overlapping token occurrences, then:
> TokenF1_i = 2 * TP_i / (number of predicted tokens + number of gold tokens)
> StructuralF1 = (1 / |G|) * sum over i in G of TokenF1_i
> The F1 value is zero when only one token multiset is empty and one when both are empty.
> Used-field F1
> Field names are case-folded for scoring and treated as sets:
> FieldF1 = 2 * |PredictedFields intersect GoldFields| /
> (|PredictedFields| + |GoldFields|)
> It is one when both sets are empty and zero when only one set is empty.
> Mode accuracies
> TargetAccuracy = I[predicted target_mode = gold target_mode]
> ChoiceAccuracy = I[predicted choice_mode = gold choice_mode]
> Hole alignment F1
> AlignmentF1 = 2 * |P intersect G| / (|P| + |G|)
> Validity
> Validity is 1 when P = G and either all repairs are exact or the predicted fragments pass delimiter and control-block balance checks. Otherwise it is 0.
> 6.3 Row and final score
> Before penalties, the row score is:
> BaseRowScore = 0.65 * Exact
> + 0.10 * StructuralF1
> + 0.08 * FieldF1
> + 0.04 * TargetAccuracy
> + 0.04 * ChoiceAccuracy
> + 0.04 * AlignmentF1
> + 0.05 * Validity
> The weights sum to 1.00.
> If P is not exactly equal to G, multiply BaseRowScore by 0.50.
> If choice_mode="none" is paired with a target mode other than generation, multiply the result by 0.85.
> Malformed prediction JSON scores 0 for that row.
> The final leaderboard score is the arithmetic mean over all N test rows:
> FinalScore = (1 / N) * sum of RowScore_j for j = 1..N
> Scores are clipped to the interval [0,1]. A perfect submission scores exactly 1.0. A malformed file contract, including wrong columns, missing rows, duplicate IDs, or unknown IDs, scores 0.0 overall.
> 7. Runtime and resource rules
> CPU only: at most 10 CPU cores and 62 GB RAM.
> Total training plus test inference time: 90 minutes.
> Network access, remote models, hosted APIs, downloads, and hidden upstream source lookup are prohibited.
> Train only from the supplied public files and generate all test predictions in the same run.
> Preinstalled packages may be used, but package installation during execution is prohibited.
> Runs must be deterministic and must keep numerical-library threads within the CPU limit.
> 8. Why the task is difficult
> Every row contains multiple missing fragments, and up to five fragments may interact across distant parts of a prompt. Control blocks opened before one hole may branch or close in another. Field candidates contain up to 20 realistic family-level decoys. Answer-choice behavior must agree with the target mode. Finally, train and test use different dataset families. Successful systems must combine local syntax, long-range Jinja structure, learned prompt conventions, and consistency across all four output components. Exact reconstruction carries 65% of the score, so generic but merely well-formed Jinja cannot pass through partial-credit components alone.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Biosignal Sequence To Symbol Decoding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bqvcez06mrbg993tmqhh9y98c67s8
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat shikum's score of 0.796!

Full challenge description from page:

> Leaderboard
> (20)
> Your Submissions
> Biosignal Sequence To Symbol Decoding
> Overview
> This is a sequence-to-sequence transduction task. Each input is a session: an unordered group of 50 source sequences, every one a length-2560 sequence of 18-dimensional vectors. The required output is a single target sequence of 50 symbols drawn from a fixed 50-symbol vocabulary, one symbol per source sequence, emitted in the order the session's sequences are indexed. A session was produced by running a person through a fixed catalogue of 50 short media items while a wearable array recorded them; the log recording which item drove which excerpt was lost, and reconstructing that log is the transduction target. Every catalogue item was presented exactly once per session, so a session's target sequence is a permutation of the vocabulary.
> The difficulty comes from where the signal lives. The source sequences respond to a catalogue item only indirectly and weakly, every wearer has an idiosyncratic baseline, and the evaluation sessions come from wearers who appear nowhere in the training corpus — so anything memorized about a particular body does not transfer. The vocabulary, by contrast, is shared: the same 50 items drive every session, so each symbol leaves a faint signature that is consistent across people and is present in the training corpus. Source sequences are short, the acquisition hardware is low-cost and drops elements irregularly, and the 18 feature dimensions arrive from three independent devices with separate clocks and noise floors. No pretrained checkpoint exists for this input representation, so the source-sequence encoding and its mapping onto the symbol vocabulary must both be learned from the supplied training pairs.
> Dataset
> The corpus comprises 67 training sessions (3,259 labelled source sequences) and 40 evaluation sessions (2,000 source sequences), each source sequence stored as a NumPy array alongside a CSV index. Sessions are disjoint between the two splits.
> Public files
> public/train.csv — one row per training source sequence, labelled with the vocabulary symbol that produced it.
> Columns: recording_id, session_id, signal_file, stimulus_id
> public/test.csv — one row per evaluation source sequence, without the symbol. Fifty rows per session, presented in scrambled position order.
> Columns: recording_id, session_id, slot, signal_file
> public/signals/<recording_id>.npy — one NumPy array per source sequence. Each is float32 with shape (2560, 18): 2560 sequence positions by 18 feature dimensions.
> public/sample_submission.csv — a valid submission in the required format.
> Private file
> private/answers.csv — organizer only. Columns: session_id, assignment.
> Column descriptions
> The fields appearing across the public and private files are as follows.
> recording_id (string) — unique identifier for one source sequence, e.g. rec_6c3a6c9734e0b304. Appears once in exactly one of train.csv or test.csv.
> session_id (string) — anonymized identifier for the session a source sequence belongs to, e.g. sess_e01c2613ccb899cd. Sessions are disjoint between the training and evaluation splits. In train.csv this field groups the sequences of one wearer and can be used to build session-disjoint cross-validation folds; in test.csv it marks which 50 sequences form one evaluation session.
> slot (integer) — index of a source sequence within its evaluation session, from 1 to 50. This index is scrambled and carries no information about which symbol applies; it exists only to fix the order in which symbols are read from the submitted target sequence. Present in test.csv only.
> signal_file (string) — path to the source sequence's array, relative to public/.
> stimulus_id (string) — the vocabulary symbol that produced the source sequence, one of S01 through S50. Present in train.csv only.
> assignment (string) — a session's target sequence: 50 whitespace-separated symbols, the symbol at position i corresponding to the source sequence whose slot is i. Present in private/answers.csv and required in the submission.
> Feature dimension order
> Every array uses the same fixed ordering along its second axis.
> Dimensions 0–13 — a 14-channel cortical potential array, in fixed montage order.
> Dimension 14 — electrodermal activity.
> Dimension 15 — surface temperature.
> Dimension 16 — thoracic expansion.
> Dimension 17 — peripheral pulse.
> Dimensions 14–17 were acquired at a lower native resolution than the shared 2560-position grid and are carried onto it by interpolation, so they vary smoothly across neighbouring positions and contain no detail finer than their own acquisition resolution. All 18 dimensions are supplied in their original physical units and are not normalized.
> Symbol vocabulary
> The vocabulary holds 50 symbols, S01 through S50, organized into five families of ten: S01–S10, S11–S20, S21–S30, S31–S40, and S41–S50. Symbols within a family share broad content characteristics; symbols in different families do not.
> Every session was run over the full vocabulary, emitting each of the 50 symbols exactly once, and no session repeats a symbol. Each evaluation session is complete: all 50 of its source sequences are present, so an evaluation session's true target sequence is a permutation of the vocabulary. Training sessions are not all complete — source sequences whose input streams could not be aligned were dropped, leaving between 39 and 50 per training session (29 of the 67 are complete).
> Data example
> A truncated row from train.csv:
> recording_id,session_id,signal_file,stimulus_id
> rec_6c3a6c9734e0b304,sess_e01c2613ccb899cd,signals/rec_6c3a6c9734e0b304.npy,S27
> Submission format
> Submit a CSV with exactly two columns and a header row:
> session_id — a session identifier from test.csv
> assignment — 50 whitespace-separated vocabulary symbols
> Exactly one row per distinct session_id in test.csv, no more and no fewer. Duplicate session_id values are rejected. Every assignment must contain exactly 50 symbols, and every symbol must be one of S01–S50; a submission violating either rule is rejected. The symbol at position i is scored against the source sequence whose slot equals i in that session. Repeated symbols within a target sequence are accepted and scored as written, although no session's true target sequence repeats a symbol.
> session_id,assignment
> sess_e01c2613ccb899cd,S01 S02 S03 S04 S05 S06 S07 S08 S09 S10 S11 S12 S13 S14 S15 S16 S17 S18 S19 S20 S21 S22 S23 S24 S25 S26 S27 S28 S29 S30 S31 S32 S33 S34 S35 S36 S37 S38 S39 S40 S41 S42 S43 S44 S45 S46 S47 S48 S49 S50
> Evaluation
> The metric is the Sequence Assignment Score (SAS), a weighted blend of exact symbol agreement and family-level partial credit, averaged over evaluation sessions.
> For one session, let p be the 50 emitted symbols and t the 50 true symbols, compared position by position. Let family(s) map a vocabulary symbol to its family index, (int(s[1:]) - 1) // 10.
> def session_score(p, t):
> exact  = sum(a == b for a, b in zip(p, t)) / 50
> family = sum(family(a) == family(b) for a, b in zip(p, t)) / 50
> return 0.75 * exact + 0.25 * family
> SAS = mean(session_score(p, t) for each evaluation session)
> The exact term carries weight 0.75 and the family term weight 0.25. The two terms are nested: a position scored correct on the exact term also counts toward the family term, so a fully correct session scores 0.75 + 0.25 = 1.0.
> The final value is clamped into [0.02, 1.0]. Every evaluation session contributes equally to the mean regardless of how well it scores.
> A submission that ignores the source sequences scores at chance in expectation. With 50 symbols in 5 families of 10, a symbol chosen without reference to the input matches exactly with probability 1/50 = 0.02 and lands in the correct family with probability 10/50 = 0.20, giving 0.75 × 0.02 + 0.25 × 0.20 = 0.065. This is the chance baseline.
> The supplied sample_submission.csv is not a random submission: it is a fixed constant target sequence, the symbols S01 through S50 in ascending order, written identically for every session. Because each session's position order is scrambled independently of that ordering, a fixed target sequence carries no information about which source sequence sits at which position, so its expected score is the same 0.065; the value it actually attains on this evaluation set is 0.061, the difference being ordinary finite-sample variation over 40 sessions rather than any property of the ordering. A perfect reconstruction of every session scores 1.0. Higher is better.
> What Not To Use (Prohibited Methods)
> Do not attempt to identify the underlying media catalogue or obtain any external description, transcript, annotation, or timing track for the 50 vocabulary symbols, and do not use any such material to align source sequences with symbols.
> Do not use any external biosignal archive, wearable-acquisition corpus, or published multichannel collection that may contain the same sessions, wearers, or presentations. Do not match source-sequence arrays, session identifiers, or file hashes against any external source.
> Do not attempt to reconstruct the original presentation order of an evaluation session from anything other than the supplied source-sequence arrays. The slot field is scrambled; treating it, the row order of test.csv, or the lexicographic order of recording_id as evidence about symbol identity is prohibited.
> Do not hardcode session-to-assignment mappings, per-recording_id constants, or memorized lookups of any kind.
> Do not tune against the private answer key in any form, including probing the leaderboard to fit per-session or per-symbol corrections.
> Do not incorporate any material derived from the evaluation targets into training. Only public/train.csv, public/test.csv, and the supplied source-sequence arrays may inform the model.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Dialogue Patchchain Splice Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70cnf2nrf06x7e7j6t6wrf218c4rv2
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat tsushima's score of 80.301!

Full challenge description from page:

> Leaderboard
> (24)
> Your Submissions
> Overview
> Dialogue Patchchain Splice Reconstruction is a high-difficulty, pretrained seq2seq challenge over Chinese multi-turn service conversations.
> Each test sample exposes a structured anchor together with four shuffled conversational packets. Three packets belong to one hidden continuation. The remaining packet is an intruder: it is genuine, fluent dialogue material, but it does not belong to the three-hop continuation being reconstructed.
> The prediction is not a class label and not a free-form reply. It is an executable patchchain.
> For every hidden hop, the model must simultaneously:
> Identify which packet belongs next.
> Reject the packet that does not belong to the continuation.
> Recover the chronological order of the three retained packets.
> Infer which opaque state registers change.
> Generate the new Unicode values carried by those registers.
> Predict each register's binary activity bit.
> Preserve consistency when the generated patches are replayed from the visible anchor.
> A conceptual target looks like:
> P03:+G01.K07=故宫@1;+G02.K11=4.5分以上@1||P01:+G02.K03=北京市东城区@1||P04:+G03.K18=桔子水晶酒店@1
> This means:
> P03 is the first hidden hop.
> P01 is the second hidden hop.
> P04 is the third hidden hop.
> P02 is the intruder packet.
> Each stage emits the state changes caused by that hop.
> The central problem is therefore trajectory splicing under latent state semantics.
> A successful model has to weave three pieces of dialogue back into the correct temporal path while generating the structured state mutations that make that path executable.
> Prediction Object
> Every sample contains:
> One sample_id.
> One visible anchor_state.
> Four shuffled dialogue packets.
> Three hidden continuation packets.
> One hidden intruder packet.
> One hidden three-stage patchchain.
> Each packet contains:
> packet_id
> system_text
> user_text
> The four local packet IDs are:
> P01
> P02
> P03
> P04
> Packet IDs are local symbols. P03 in one sample has no relationship to P03 in another sample.
> Exactly three packet IDs must appear in the prediction.
> The omitted packet is the predicted intruder.
> The Hidden Splice
> The three valid packets originate from one local dialogue trajectory, but they are presented out of chronological order.
> Conceptually, the hidden continuation is:
> anchor -> packet A -> state 1 -> packet B -> state 2 -> packet C -> state 3
> The participant sees the anchor and the four shuffled candidates, but not:
> Which three packets form the continuation.
> Which packet is the intruder.
> Which true packet comes first.
> Which state registers change at each hop.
> The intermediate states after hop 1 and hop 2.
> The final hidden state after hop 3.
> This makes the target a coupled reconstruction problem rather than three independent predictions.
> A packet that is plausible after the anchor may become impossible after another packet is inserted first. Likewise, a state patch that is locally plausible can become inconsistent when replayed through later stages.
> Packet Semantics
> A packet contains one local system-user exchange.
> Typical packets may contain:
> A recommendation followed by a refinement.
> A failed search followed by relaxed constraints.
> An entity answer followed by a new information request.
> A place reference followed by a transportation request.
> A clarification followed by a revised preference.
> A confirmation followed by a cross-service dependency.
> A short acknowledgment whose meaning depends on an earlier entity.
> The intruder is not random noise.
> It may resemble the valid packets in:
> Service type.
> Entity morphology.
> Constraint shape.
> Dialogue-act style.
> Value type.
> Surface vocabulary.
> A model therefore cannot rely on the assumption that the obviously unrelated packet is always the decoy.
> Why This Is a Relay Problem
> Suppose the anchor represents a partially resolved itinerary.
> A first hidden packet establishes an attraction. A later packet asks for a restaurant near that attraction. A third packet requests transportation from the selected restaurant.
> If the model places the restaurant packet before the attraction packet, several locally sensible predictions can still become globally wrong.
> The challenge therefore behaves like a relay:
> One packet changes the state frontier.
> The next packet inherits that altered frontier.
> The third packet inherits both previous changes.
> The grader explicitly replays the submitted patchchain through three checkpoints.
> Earlier errors can therefore remain visible later instead of disappearing after one token-level comparison.
> Anchor Register
> anchor_state is the visible structured state immediately before the hidden splice begins.
> Example:
> G01.K04=免费@1;G01.K09=故宫@1;G02.K03=@0;G02.K11=4.5分以上@0
> Every anchor atom follows:
> Gxx.Kyy=value@b
> where:
> Gxx is a local goal lane.
> Kyy is an opaque register code.
> value is a Unicode text payload.
> b is a binary activity bit.
> The bit is always:
> 0
> 1
> The anchor is not merely context text. It is the executable starting memory against which every predicted stage is applied.
> Goal Lanes
> Goal lanes use symbols such as:
> G01
> G02
> G03
> Goal lanes are local to a sample trajectory.
> G02 in one sample has no semantic identity outside that sample.
> A single sample may contain several lanes because one conversation can maintain multiple linked sub-goals at the same time.
> A generated patch may therefore:
> Modify the currently active lane.
> Return to an older lane.
> Activate a value in another visible lane.
> Replace a value already stored in the anchor.
> Mutate several lanes during one hop.
> Opaque Register Codes
> State register codes use:
> K01
> K02
> K03
> ...
> Unlike goal lanes, a K-code has a consistent latent role throughout the released dataset.
> The challenge does not publish a human-readable register dictionary.
> Participants are expected to induce the K-code semantics from training examples.
> Repeated supervision may reveal that one code behaves like a location-like field, another like a rating-like field, and another like a transport endpoint. The model must learn these correspondences rather than receive them as a public ontology.
> This latent-register layer is important because the task is not simply Chinese text generation with readable slot names.
> Patch Algebra
> A stage patch is a finite set of register mutations.
> There are two operation types.
> Set Mutation
> A set mutation has the form:
> +Gxx.Kyy=value@b
> Example:
> +G02.K11=4.5分以上@1
> A set mutation means that after the current hop, the specified register must contain the supplied normalized value and activity bit.
> It is used for both:
> Creating a register that was not previously present.
> Replacing the value or bit of an existing register.
> Delete Mutation
> A delete mutation has the form:
> -Gxx.Kyy
> It removes that register from the current state.
> Deletion is valid but less frequent than setting or replacing a value.
> Stage Syntax
> One stage has the form:
> packet_id:patch
> Example:
> P03:+G01.K07=故宫@1;+G02.K11=4.5分以上@1
> Multiple mutations inside the same stage are separated by semicolons.
> Mutation order inside one stage has no semantic meaning. Training targets use a deterministic canonical order.
> If a selected packet produces no emitted mutation, the stage may be written as:
> P03:-
> Complete Patchchain
> A valid prediction contains exactly three stages separated by:
> ||
> Example:
> P03:+G01.K07=故宫@1||P01:+G02.K11=4.5分以上@1||P04:+G03.K18=桔子水晶酒店@1
> The stage positions are chronological.
> Stage 1 is applied to the visible anchor.
> Stage 2 is applied to the state produced by stage 1.
> Stage 3 is applied to the state produced by stage 2.
> The three packet IDs must be distinct.
> The omitted fourth packet is the predicted intruder.
> Escaping Reserved Characters
> The patch grammar reserves several ASCII delimiters.
> When these characters occur inside a generated value, the target serialization uses:
> % -> %25
> | -> %7C
> ; -> %3B
> = -> %3D
> @ -> %40
> Ordinary Chinese characters remain unchanged.
> The evaluator decodes these escapes before comparing values.
> Why Naive Classification Is Insufficient
> A four-way classifier does not solve the benchmark.
> Even after identifying the intruder, the remaining three packets still have six possible chronological permutations.
> The model must also emit a structured patch for every selected stage.
> Two predictions can therefore choose exactly the same packet set while describing different hidden trajectories:
> P03 -> P01 -> P04
> P01 -> P03 -> P04
> The second route may cause different state mutations because packet interpretation depends on the frontier inherited from earlier stages.
> The benchmark couples:
> Intruder rejection.
> Temporal ordering.
> Latent register induction.
> Unicode value generation.
> Binary status prediction.
> Executable multi-stage state consistency.
> Challenge Regime
> This is a Pretrained Fine-Tuning challenge.
> Pretrained text representations are allowed.
> Participants may fine-tune compact pretrained:
> Chinese encoder-decoder models.
> Multilingual encoder-decoder models.
> Small text-to-text transformers.
> Denoising seq2seq models.
> Pretrained encoders paired with learned structured decoders.
> Compact encoder-decoder architectures with auxiliary routing heads.
> Training from random initialization is also permitted, but it is not required.
> The intended solution class is learned sequence modeling.
> Machine-Learning Requirement
> The semantic predictor must be learned from data.
> Eligible systems include:
> Fine-tuned seq2seq transformers.
> Learned pointer-generator models.
> Neural packet-order models.
> Neural patch decoders.
> Multi-task routing and generation models.
> Learned constrained decoders.
> Compact recurrent encoder-decoder systems.
> Neural reranking followed by neural structured generation.
> CPU-compatible neural ensembles.
> The following are not valid primary solutions:
> Hand-authored dialogue rules.
> Manual K-code dictionaries.
> Pure regular-expression parsers.
> Deterministic slot-filling scripts with no learned predictor.
> TF-IDF-only matching.
> Bag-of-words retrieval as the complete prediction system.
> Hard-coded packet ordering rules.
> Grammar-constrained decoding is allowed when it only prevents malformed output.
> Compute Envelope
> The execution environment provides:
> 10 CPU cores.
> 62.5 GiB RAM.
> No GPU.
> The task is intended for compact CPU-capable fine-tuning and inference.
> Useful strategies include:
> Freezing lower pretrained layers.
> Fine-tuning only upper layers.
> Parameter-efficient adaptation supported by the chosen framework.
> Short encoder windows.
> Cached tokenization.
> Cached frozen representations.
> Restricted structural output vocabularies.
> Small beam widths.
> Separate route and patch losses.
> Copy-aware decoding for entity values.
> Remote model APIs are not allowed.
> Released Files
> The public package contains:
> train.jsonl
> test.jsonl
> sample_submission.csv
> There is no official validation file.
> There is no public ontology file and no public K-code dictionary.
> train.jsonl
> Each line contains one JSON object.
> sample_id
> Type: string.
> This is the submission alignment identifier.
> Do not use the identifier itself as a predictive feature.
> anchor_state
> Type: string.
> This is the serialized state before the hidden three-hop continuation.
> Example:
> G01.K04=免费@1;G01.K09=故宫@1;G02.K03=@0
> packets
> Type: list of four objects.
> Each object contains:
> packet_id
> system_text
> user_text
> packet_id is one of:
> P01
> P02
> P03
> P04
> Exactly three packets belong to the hidden continuation.
> patchchain
> Training only.
> Type: string.
> This is the complete three-stage target program.
> Example:
> P03:+G01.K07=故宫@1||P01:+G02.K11=4.5分以上@1||P04:+G03.K18=桔子水晶酒店@1
> test.jsonl
> The test file contains the same public inputs as train.jsonl, except patchchain is omitted.
> The evaluation data does not expose:
> The intruder packet.
> The three-packet route.
> Intermediate state snapshots.
> Hidden patch mutations.
> Human-readable register meanings.
> Source trajectory identifiers.
> Construction metadata.
> Validation Discipline
> A hidden dialogue trajectory can contribute more than one derived example.
> When creating local validation, keep examples from the same trajectory together whenever possible.
> Do not split near-duplicate trajectory windows across training and validation.
> Useful grouped-validation precautions include keeping together:
> Packet copies from the same local trajectory.
> Neighboring dialogue windows.
> Cached anchor states.
> Auxiliary route labels.
> Patch-operation labels.
> Final-state targets.
> Hard negatives derived from the same trajectory.
> A naive example-level split can overestimate generalization when neighboring windows share conversational material.
> Submission Format
> A submission contains exactly two columns:
> sample_id
> prediction
> Example:
> sample_id,prediction
> DPRR_ABC123,P03:+G01.K07=故宫@1||P01:+G02.K11=4.5分以上@1||P04:+G03.K18=桔子水晶酒店@1
> Every prediction must contain exactly three stages.
> For a valid sample prediction:
> Every stage begins with P01, P02, P03, or P04.
> The three packet IDs are distinct.
> Every state key follows Gxx.Kyy.
> Every set mutation contains a value and binary bit.
> Every stage follows the published patch grammar.
> Malformed sample predictions receive zero component credit for that sample.
> The submission itself must contain:
> Every expected sample_id.
> No extra IDs.
> No duplicate IDs.
> Exactly the two published columns in the published order.
> Use sample_submission.csv exactly.
> Evaluation
> Submissions are scored from 0.01 to 100.
> Higher is better.
> The evaluator measures several different properties because the target is both linguistic and executable.
> The published components are:
> Exact Patch Atom F1.
> Soft Argument F1.
> Replay Trace Agreement.
> Route Exact Position.
> Route LCS.
> Route Set F1.
> Exact Program Rate.
> There are no hidden metric weights.
> A perfect submission receives exactly 100.
> Value Normalization
> Before comparing generated values, the evaluator:
> Decodes the published percent escapes.
> Applies Unicode NFKC normalization.
> Collapses consecutive whitespace to one ASCII space.
> Removes leading and trailing whitespace through the same collapse operation.
> The same normalization is applied to prediction and gold values.
> Exact Patch Atom F1
> Every emitted mutation is converted into a stage-bound semantic atom.
> A set atom contains:
> Stage index.
> Operation kind.
> State key.
> Normalized value.
> Activity bit.
> A delete atom contains:
> Stage index.
> Operation kind.
> State key.
> Packet ID is intentionally not part of the patch atom because routing is scored separately.
> For one sample, let:
> P = set of predicted exact patch atoms.
> G = set of gold exact patch atoms.
> Then:
> AtomF1 = 2 × |P ∩ G| / (|P| + |G|)
> If both sets are empty:
> AtomF1 = 1
> The dataset-level value A is the arithmetic mean of sample AtomF1 values.
> This component requires exact structural generation.
> A nearly correct entity value does not count as an exact atom match. Near-matches are handled separately by Soft Argument F1.
> Character F1 for Generated Values
> Soft value comparison uses a Unicode character multiset F1.
> After normalization, let:
> Cp[c] be the predicted count of character c.
> Cg[c] be the gold count of character c.
> Character overlap is:
> I = sum over characters c of min(Cp[c], Cg[c])
> Then:
> CharF1 = 2 × I / (len(predicted) + len(gold))
> Special cases:
> If both values are empty, CharF1 = 1.
> If only one value is empty, CharF1 = 0.
> This gives partial credit for small copying or generation errors without requiring an external tokenizer.
> Soft Argument F1
> Operations are aligned by:
> Stage index.
> Operation kind.
> State key.
> For every matching predicted/gold operation key:
> A matching delete receives similarity 1.
> A set mutation receives:
> OperationSimilarity = 0.85 × CharF1(value) + 0.15 × BitMatch
> where:
> BitMatch = 1 when the predicted activity bit is correct.
> BitMatch = 0 otherwise.
> Let:
> M = summed operation similarity over shared operation keys.
> Np = number of predicted operations.
> Ng = number of gold operations.
> Then:
> SoftArgumentF1 = 2 × M / (Np + Ng)
> If both programs contain no operations:
> SoftArgumentF1 = 1
> The dataset-level value G is the arithmetic mean across samples.
> This component rewards:
> Correct register selection.
> Near-correct Unicode values.
> Correct activity bits.
> Appropriate mutation count.
> Replay Trace Agreement
> The prediction is executed from the visible anchor.
> For every sample:
> Parse the visible anchor.
> Apply predicted stage 1 to one state copy.
> Apply gold stage 1 to another state copy.
> Compare the changed state frontier.
> Repeat after stage 2.
> Repeat after stage 3.
> At one checkpoint, the changed frontier is the union of all state keys touched by either program up to that checkpoint.
> Unchanged anchor registers do not inflate replay credit.
> For each frontier key, one point is awarded when:
> Both replayed states contain the same normalized value and same activity bit.
> or:
> Both replayed states have deleted that key.
> Checkpoint agreement is:
> matching frontier keys / frontier key count
> The sample ReplayTrace score is the arithmetic mean of the three checkpoint agreements.
> The dataset-level value T is the arithmetic mean across samples.
> Replay Trace Agreement makes early errors persistent. A wrong mutation can continue to damage later checkpoints until another predicted operation repairs it.
> Route Exact Position
> Compare the three predicted packet IDs with the three gold packet IDs by chronological position.
> Example:
> Gold:
> P03 P01 P04
> Prediction:
> P03 P04 P01
> Only one of three positions is exact.
> Therefore:
> RouteExact = 1 / 3
> The dataset-level value E is the arithmetic mean across samples.
> Route LCS
> The packet route is also evaluated by longest common subsequence.
> For one sample:
> RouteLCS = LCS_length(predicted_route, gold_route) / 3
> For:
> Gold:
> P03 P01 P04
> Prediction:
> P03 P04 P01
> The LCS length is 2.
> Therefore:
> RouteLCS = 2 / 3
> The dataset-level value L is the arithmetic mean across samples.
> Route Set F1
> Ignore packet order and compare the predicted and gold packet sets.
> Let:
> Rp = predicted route set.
> Rg = gold route set.
> Then:
> RouteSetF1 = 2 × |Rp ∩ Rg| / (|Rp| + |Rg|)
> Because valid predictions contain three distinct packet IDs, this component mainly measures intruder rejection.
> The dataset-level value S is the arithmetic mean across samples.
> Exact Program Rate
> A sample receives exact-program credit only when:
> The three packet IDs are exactly correct in order.
> Every stage contains exactly the same semantic mutations as gold.
> Mutation order inside one stage is ignored.
> Let X be the fraction of evaluation samples with an exact semantic patchchain.
> Final Score
> Let:
> A = Exact Patch Atom F1.
> G = Soft Argument F1.
> T = Replay Trace Agreement.
> E = Route Exact Position.
> L = Route LCS.
> S = Route Set F1.
> X = Exact Program Rate.
> First define the patch fidelity harmonic mean:
> PatchCore = 0, if A + G = 0
> otherwise:
> PatchCore = 2 × A × G / (A + G)
> Then fold in executable state agreement:
> StateCore = 0, if PatchCore + T = 0
> otherwise:
> StateCore = 2 × PatchCore × T / (PatchCore + T)
> Define route-position fidelity:
> RouteCore = 0, if E + L = 0
> otherwise:
> RouteCore = 2 × E × L / (E + L)
> Then:
> Route = sqrt(RouteCore × S)
> The final score is:
> Dialogue Patchchain Splice Reconstruction Score = 100 × StateCore^1.20 × (0.55 + 0.45 × Route) × (0.92 + 0.08 × X)
> The result is clipped to:
> [0.01, 100]
> A perfect prediction has:
> A = 1
> G = 1
> T = 1
> E = 1
> L = 1
> S = 1
> X = 1
> Therefore:
> PatchCore = 1
> StateCore = 1
> RouteCore = 1
> Route = 1
> Final Score = 100
> The 1.20 exponent keeps executable state reconstruction central without making the benchmark purely exact-match.
> The route factor ensures that selecting the correct packets is not enough when chronology is wrong.
> The exact-program factor gives a modest reward for fully reconstructed trajectories without erasing graded partial credit.
> Reproducing the Metric Locally
> For every local validation sample:
> Parse the visible anchor state.
> Split the prediction on || and verify exactly three stages.
> Verify that the three packet IDs are distinct and belong to P01 through P04.
> Parse all set and delete mutations.
> Decode escaped values.
> Apply NFKC and whitespace normalization.
> Build exact stage-bound patch-atom sets and compute AtomF1.
> Match operations by stage, operation kind, and state key.
> Compute Unicode character F1 for matched set-operation values.
> Combine value similarity and bit correctness into Soft Argument F1.
> Replay predicted and gold patches from the anchor through three checkpoints.
> Compare only the cumulative changed frontier at each checkpoint.
> Compute Route Exact Position.
> Compute the three-token route LCS.
> Compute Route Set F1.
> Check semantic exact-program equality.
> Average every component across validation samples.
> Compute PatchCore.
> Compute StateCore.
> Compute RouteCore.
> Compute Route.
> Apply the published final formula.
> Clip to [0.01, 100].
> The provided grader.py implements this procedure directly.
> Modeling Directions
> The task is naturally suited to multi-objective seq2seq learning.
> A useful model can share one text representation while learning separate signals for:
> Packet membership.
> Packet chronology.
> Register selection.
> Value generation.
> Activity-bit prediction.
> Final patchchain serialization.
> Input Serialization
> One possible serialization is:
> ANCHOR <state> P01 <system> <user> P02 <system> <user> P03 <system> <user> P04 <system> <user>
> Participants may use any deterministic representation.
> Useful special markers can distinguish:
> Anchor boundaries.
> Packet boundaries.
> System and user turns.
> Goal lanes.
> Register codes.
> Stage positions.
> Direct Seq2Seq Fine-Tuning
> A straightforward learned baseline can fine-tune a compact pretrained encoder-decoder model with:
> Input: anchor plus all four packets.
> Target: complete three-stage patchchain.
> The model must learn:
> Intruder rejection.
> Packet chronology.
> Latent K-code semantics.
> Register mutation structure.
> Unicode value copying.
> Activity bits.
> Patch syntax.
> Teacher forcing is sufficient for an initial system.
> A stronger decoder can constrain the three stage-leading packet IDs so that the same packet cannot be selected twice.
> Route Head Plus Patch Decoder
> A compact multi-task architecture can share one encoder and use:
> A route head for packet membership and chronology.
> A patch decoder for stage mutations.
> Useful route objectives include:
> Three-position pointer loss.
> Intruder classification.
> Pairwise precedence.
> Permutation likelihood.
> The patch decoder can then condition on either gold routes during training, predicted routes during inference, or a scheduled mixture of both.
> State-Aware Encoding
> The anchor already exposes explicit structure.
> A model may encode anchor atoms separately from natural-language text using:
> Goal-lane embeddings.
> K-code embeddings.
> Bit embeddings.
> Value text encodings.
> Cross-attention between packet text and anchor atoms.
> This can help distinguish:
> New register creation.
> Value replacement.
> Activity-bit changes.
> Cross-lane mutations.
> Previously resolved versus unresolved information.
> Copy-Aware Generation
> Many target values occur in:
> The visible anchor.
> A selected system utterance.
> A selected user utterance.
> An earlier selected packet.
> Useful learned mechanisms include:
> Pointer-generator decoding.
> Copy-biased attention.
> Encoder-decoder models with strong pretrained copying behavior.
> Restricted generation over structural tokens plus open text spans.
> Exact copying matters because both exact patch atoms and replay agreement depend on value fidelity.
> Auxiliary Supervision
> Participants may derive auxiliary targets from released training labels.
> Examples include:
> Intruder identity.
> Packet position.
> Mutation count per stage.
> Changed K-codes.
> Changed G-lanes.
> Value-replacement indicators.
> Activity-bit transitions.
> Final cumulative state.
> These auxiliary labels are allowed because they are derived only from released training supervision.
> Practical CPU Baseline
> A practical neural baseline can:
> Read train.jsonl.
> Serialize each anchor and its four packets.
> Add special tokens for packet IDs and patch syntax.
> Fine-tune a compact pretrained Chinese or multilingual seq2seq checkpoint.
> Use modest encoder lengths.
> Train directly against the complete patchchain.
> Decode with a small beam.
> Enforce distinct packet IDs at stage starts.
> Reject malformed beams.
> Submit the highest-scoring valid generated patchchain.
> A stronger CPU system may add:
> An intruder classification loss.
> A packet pointer head.
> Copy-aware value decoding.
> Changed-register auxiliary prediction.
> Final-state reconstruction loss.
> Hard-negative training over the intruder packet.
> Fine-Tuning Rules
> Participants may use:
> Public pretrained text checkpoints.
> Public pretrained tokenizers.
> Public pretrained Chinese language models.
> Public pretrained multilingual text models.
> Public pretrained encoder-decoder architectures.
> General-purpose language pretraining.
> Participants may fine-tune all or part of the selected model on released challenge data.
> The following remain disallowed:
> Hidden test labels.
> Private evaluator files.
> Manual annotation of evaluation samples.
> External labeled copies of the evaluation conversations.
> External lookup tables that reveal the hidden K-code ontology.
> Retrieval of hidden source annotations.
> Submission-feedback reconstruction of hidden patchchains.
> Allowed Resources
> Participants may use:
> Released challenge files.
> Public pretrained text checkpoints.
> Public pretrained tokenizers.
> Standard machine-learning libraries.
> Standard deep-learning libraries.
> Standard Unicode libraries.
> Beam search.
> Grammar-constrained decoding.
> Auxiliary targets derived from released training labels.
> Neural ensembles that fit the runtime limits.
> Disallowed Predictive Shortcuts
> Participants may not use:
> sample_id as a predictive feature.
> JSONL row order as a predictive feature.
> Manual packet routing.
> Hand-labeled K-code semantics from evaluation data.
> Hard-coded evaluation patchchains.
> Rule-only semantic parsers.
> TF-IDF-only routing systems.
> External search engines at inference time.
> Remote LLM APIs.
> Private challenge artifacts.
> Typical Failure Patterns
> Right Packets, Wrong Chronology
> The model rejects the intruder but swaps two valid packets.
> Route Set F1 may remain perfect while Route Exact Position, Route LCS, and replay consistency fall.
> Right Route, Wrong Registers
> The three packets are ordered correctly, but the model maps the dialogue semantics onto the wrong K-codes.
> Routing remains strong while patch and replay components fall.
> Right Register, Imperfect Value
> The correct register is selected but an entity name or constraint is copied imperfectly.
> Exact Patch Atom F1 drops, while Soft Argument F1 can still award graded credit.
> Locally Plausible Patch, Broken Frontier
> A first-stage error survives into later checkpoints.
> Replay Trace Agreement penalizes the resulting state drift.
> Anchor Echoing
> Simply copying the visible anchor does not produce inflated replay credit because the evaluator compares only the cumulative changed frontier.
> Duplicate Packet IDs
> A hidden continuation never uses the same packet twice.
> Predictions that repeat a packet ID are invalid for that sample.
> Scope and Limitations
> The benchmark models structured service dialogue rather than unrestricted open-domain conversation.
> Its hidden register inventory is finite, and some registers appear more frequently than others.
> Some values are easier to copy than others. Short acknowledgments can also be ambiguous without earlier context.
> The benchmark measures:
> Multi-hop dialogue interpretation.
> Intruder rejection.
> Temporal splice recovery.
> Latent register induction.
> Structured Unicode value generation.
> Executable state-transition consistency.
> It does not directly measure:
> Open-web retrieval.
> Current factual verification.
> Long-form assistant helpfulness.
> External database execution.
> Free-form response quality.
> Expected Outcome
> A strong submission should be able to:
> Fine-tune within the CPU-only environment.
> Infer the latent K-code inventory from supervision.
> Distinguish one plausible intruder from three continuation packets.
> Recover the hidden packet chronology.
> Generate exact or near-exact register mutations.
> Copy entity and constraint values accurately.
> Preserve state consistency through all three replay checkpoints.
> Produce syntactically valid executable patchchains.
> The prediction objective is:
> splice the hidden three-hop continuation back onto the visible anchor and emit the state patchchain that makes the reconstruction executable.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Opaque OCR Continuation Path Induction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx799hcypcczf9js7g95m9n7kn8c1g63
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat douglas's score of 0.313!

Full challenge description from page:

> Leaderboard
> (25)
> Your Submissions
> Overview
> Digitized archives often preserve a page's OCR while losing its immediate neighbours during migration, selective export, or rebinding. An archivist may then know one surviving anchor page and have a small pool of plausible nearby pages, without knowing which candidates belong to the same local run or on which side of the anchor they occur.
> Each case is an anchor-conditioned directed-path problem. Nine anonymous candidate nodes are supplied. Exactly five form one latent continuation path: two predecessors, the anchor, and two successors. The other four are contextual impostors selected from the same monthly binder, date, language, and document family but from a different source run.
> The task therefore combines two decisions that ordinary page ordering does not separate: reject candidates that do not belong to the anchor's local continuation, then orient the retained nodes into a valid directed path. The candidate set is not a shuffled document whose every page must be placed. Broad metadata is deliberately non-discriminative, and direction matters.
> Instance-Permuted OCR Evidence
> Public OCR uses an independently permuted lexical alphabet in every case. A code such as tok_9a13ef02 has a stable meaning only among the nine candidates in that case. The same underlying word receives the same code inside the case, but the code is deliberately unrelated to codes in every other case.
> The following structural markers are preserved:
> <lb>: a source line boundary.
> <num>: a removed numeric expression.
> <ref>: a removed URL or address-like reference.
> <cut>: the omitted middle of a long page.
> <mask>: a challenge-hidden lexical occurrence.
> This instance-level permutation removes global vocabulary and source-name shortcuts while preserving within-case recurrence, lexical transport, punctuation, line structure, and OCR behavior. A solver cannot learn that one particular token means one particular word. It must learn transferable relations between candidate pairs and decode them jointly under a new symbol permutation.
> Token masking and dropout create incomplete local evidence. Continuation can therefore depend on several weak signals agreeing across the path rather than one repeated phrase.
> Path Grammar
> Every case provides:
> exactly nine candidate pages with IDs P00 through P08;
> one anchor_page_id that belongs to the candidate set;
> one unknown five-node continuation path.
> The predicted path must:
> contain exactly five unique candidate IDs;
> place the supplied anchor in the third position;
> order two predecessors before the anchor;
> order two successors after the anchor;
> use > as the only separator.
> Example path:
> P07>P02>P05>P01>P08
> If P05 is the anchor, the example is structurally valid.
> Dataset
> The public dataset contains:
> train.csv: 3,499 labeled page-chain reconstruction cases.
> test.csv: 745 unlabeled cases requiring predicted chains.
> sample_submission.csv: 745 structurally valid example predictions, one for every test case.
> Entire monthly source binders are disjoint between training and test. Candidate pages from one case never reveal source page numbers, dates, filenames, language labels, document-family labels, or original lexical text.
> train.csv Columns
> case_id (string): anonymous unique training-case identifier.
> anchor_page_id (string): candidate ID that must occupy position three.
> candidate_pages (JSON string): list of nine objects, each containing page_id (string) and opaque page_text (string).
> target_page_chain (string): ordered five-page target joined with >.
> test.csv Columns
> case_id (string): anonymous unique test-case identifier.
> anchor_page_id (string): candidate ID that must occupy position three.
> candidate_pages (JSON string): list of nine candidate page objects without the target order.
> sample_submission.csv Columns
> case_id (string): test identifier copied from test.csv.
> predicted_page_chain (string): predicted five-page chain.
> Evaluation
> The score is bounded in [0, 1], where higher is better:
> Score = 0.80 * DirectedAdjacencyF1 + 0.20 * ExactChainAccuracy
> The weights sum to 1.00, and each component appears exactly once.
> DirectedAdjacencyF1
> A five-page chain contains four directed edges between consecutive pages. The grader compares the four predicted edges with the four target edges.
> A directed edge is correct only when both page IDs and their direction match.
> Every valid prediction and target contains four edges, so row-level precision and recall are equal.
> For one row, DirectedAdjacencyF1 = matching directed edges / 4.
> The reported component is the mean row-level value across scored cases.
> Reversing a correct pair receives no credit because page continuity is directional.
> ExactChainAccuracy
> This is the fraction of cases whose complete five-page prediction exactly equals the target chain.
> Malformed chain rows receive zero credit and are not silently reordered, deduplicated, clipped, or repaired. Structural CSV violations such as missing required IDs, duplicate IDs, or extra columns raise an error.
> Submission
> Submit a CSV with exactly two columns. Example:
> Header: case_id,predicted_page_chain
> Row: CHAINTST_1a2b3c4d5e6f70,P07>P02>P05>P01>P08
> Row: CHAINTST_7f6e5d4c3b2a10,P03>P00>P06>P04>P01
> Every required test case_id must appear exactly once. Additional rows outside the scored answer partition are ignored after required-ID and duplicate-ID validation.
> Allowed And Prohibited Methods
> Allowed
> Train CPU-compatible sequence, sparse-text, graph, pairwise-link, ranking, or constrained-decoding models using the supplied public files.
> Use equality patterns, line boundaries, punctuation, token recurrence, page-length cues, and learned directional continuity features.
> Build binder-like grouped local validation partitions using only public information.
> Use generally pretrained models only when training and inference remain within the CPU runtime limit.
> Prohibited
> Searching for or matching cases against the original archive or another external copy.
> Recovering source filenames, page numbers, dates, binder identities, original words, or source metadata.
> Hardcoding test chains, manually ordering test cases, or constructing external source-order lookup tables.
> Exploiting row order, case hashes, sample-submission values, or private-answer assumptions.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Time-Resolved Sensor Coalition Utility Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bvme5fa7tf2z469xffyz2rn8c1b7m
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat mehulmathodia's score of 0.546!

Full challenge description from page:

> Leaderboard
> (17)
> Your Submissions
> Time-Resolved Sensor Coalition Utility Reconstruction
> Overview
> This is a structured sequence-to-sequence regression challenge. For every case_id, reconstruct a 24-step sequence of complete five-sensor coalition-utility lattices. Each time step has 31 continuous outputs—one for every non-empty subset of five regional weather sensors—so one answer is a 24 by 31 matrix.
> The utility of a coalition measures how well that subset alone could recover an anomaly-stressed hidden state derived from a real Indian target weather station during a 72-hour outage, while accounting for missing channels and a small sensor-activation cost. The hidden target state is never released. A strong solver must infer how target-site behavior evolves through the outage, evaluate interacting sensor subsets, and preserve both temporal changes and coalition marginal gains.
> The observations come from real NOAA Integrated Surface Database instruments, not a synthetic problem generator. Test target sites are absent from labeled training, and the labeled years and test year are disjoint.
> Objective and output order
> Predict target_sequence with shape 24 by 31 for each test case.
> Rows are chronological three-hour outage steps.
> Columns are coalition bitmasks 1 through 31, in that exact order.
> Bit j selects regional sensor j+1 from the NPZ sensor axis. Using zero-based matrix indices, index 0 is sensor 1 alone (mask 00001), index 1 is sensor 2 alone (mask 00010), index 2 is sensors 1 and 2 (mask 00011), and index 30 is all five sensors (mask 11111).
> Every utility lies in [0,1].
> The output is not a raw weather trajectory. It is the full time-varying utility lattice induced by the unobserved target state and the observed regional panel.
> Exact coalition utility
> The first three channels of neighbor_values are standardized temperature, dew point, and sea-level pressure. At each hidden step, let regional sensor j have distance d_j km and weight:
> w_j = 1 / (50 + d_j)
> For each physical channel, let Q_all be the mask-aware weighted mean of all five available regional sensors. The latent residual coordinate R is the target station's standardized value minus this regional field, divided by 0.25 and clipped to [-4,4], as documented in the raw dataset. The challenge's hidden state is:
> H = Q_all + 0.90 * R
> R is the only unreleased term at test time. It is derived from observed target-station weather, but because the residual coordinate was normalized by 0.25, the 0.90 task coefficient deliberately amplifies the original station-local anomaly by a factor of 3.6. Therefore H is a challenge-specific stress-test state, not a claim that the amplified value is an unmodified meteorological measurement. The released regional panel still determines every coalition estimate, mask, coverage value, and sensor cost.
> For coalition S, compute its mask-aware weighted estimate Q_S separately for the three physical channels. Then define:
> coverage_S = number of supported physical channels / 3
> error_S    = mean(abs(H - Q_S)) over supported channels
> cost_S     = 0.04 * (number of sensors in S - 1) / 4
> utility_S  = clip(coverage_S * exp(-error_S / 0.14) - cost_S, 0, 1)
> If a coalition supports no physical channel, its utility is zero after clipping. Missing observations are determined by neighbor_mask, never by testing whether a value equals zero.
> This definition is provided so solvers can exploit the lattice structure. The unchanged sample submission computes every released deterministic term and sets R = 0; it is a valid structural baseline, not a near-answer. Improving it requires predicting the missing local residual from target context, regional evolution, masks, geometry, profile, and phase.
> Dataset
> Files
> Path	Description
> train.csv	1,772 labeled outage episodes.
> test.csv	223 unlabeled episodes from held-out target sites in a held-out year.
> sample_submission.csv	Complete valid structural baseline that assumes zero local residual.
> train_features.npz	Numeric feature arrays aligned to train.csv through feature_row.
> test_features.npz	Numeric feature arrays aligned to test.csv through feature_row.
> CSV columns
> Column	Availability	Description
> case_id	train, test	Opaque identifier used only for submission alignment. Do not use it as a predictor.
> feature_row	train, test	Zero-based row in the corresponding NPZ feature arrays.
> target_sequence	train only	JSON numeric matrix with shape 24 by 31, ordered as described above.
> train.csv has exactly case_id,feature_row,target_sequence. test.csv has exactly case_id,feature_row and contains no hidden utility.
> NPZ feature arrays
> The training and test NPZ files contain the same seven keys. Their first dimension matches the corresponding CSV.
> Array	Per-case shape	Description
> target_context	(24,5)	Every row is one three-hour step. Rows 0–11 provide 36 context hours immediately before the outage; rows 12–23 provide a separate 36 context hours immediately after it. These 72 context hours do not include the hidden 72-hour outage. Channels are three local residuals followed by standardized east-west and north-south target-site wind. Missing values are zero-filled.
> target_context_mask	(24,5)	1 for an observed target-context value and 0 for a zero-filled missing value.
> neighbor_values	(5,48,5)	Five regional stations over 48 consecutive three-hour steps (144 hours). Channels are standardized temperature, dew point, sea-level pressure, east-west wind, and north-south wind. Outage steps 12–35 are 24 three-hour steps, totaling 72 hours.
> neighbor_mask	(5,48,5)	1 for an observed regional value and 0 for a zero-filled missing value.
> neighbor_meta	(5,4)	Distance/2,000 km, sine of bearing, cosine of bearing, and clipped elevation difference/3,000 m. Recover distance in km by multiplying the first column by 2,000.
> site_profile	(12,5)	Target-site monthly median profile from earlier observations; channels match target_context.
> phase	(4,)	Day-of-year sine/cosine and UTC-hour sine/cosine at the outage midpoint.
> Temperature and dew point are divided by 20 °C. Sea-level pressure is centered at 1,013.25 hPa and divided by 20 hPa. Wind components are divided by 10 m/s. Numeric weather channels are clipped to [-4,4]; wind is contextual input only.
> The split contains 15 training target sites from 2021–2023 and 8 different test target sites from 2024. Eight additional stations are context-only. No target site, case ID, exact feature row, or target sequence is shared across splits.
> Evaluation
> Higher is better. The theoretical score range is [0.01,1.0].
> For one case, let Y and P be hidden and predicted 24 by 31 matrices.
> PointMAE  = mean(abs(Y - P))
> ChangeMAE = mean(abs(diff(Y, time) - diff(P, time)))
> PointScore  = exp(-PointMAE / 0.10)
> ChangeScore = exp(-ChangeMAE / 0.08)
> For every directed lattice edge formed by adding one sensor to a non-empty coalition, compare the hidden and predicted marginal utility gain at all 24 steps:
> MarginalMAE   = mean(abs(hidden_gain - predicted_gain)) over all edges and steps
> MarginalScore = exp(-MarginalMAE / 0.08)
> At each time step, compute Pearson correlation across the 31 coalition utilities. A constant hidden or predicted vector receives correlation zero; negative correlations are clipped to zero. CorrelationScore is the mean over 24 steps.
> RawRowScore = 0.45 * PointScore
> + 0.25 * ChangeScore
> + 0.20 * MarginalScore
> + 0.10 * CorrelationScore
> RowScore   = 0.01 + 0.99 * RawRowScore
> FinalScore = mean(RowScore over all test cases)
> The metric's hard floor of 0.01 applies only to one scalar repeated across every case, time, and coalition. It is not the practical public-data baseline. On the frozen 223-case test split, the following deterministic CPU ladder is measured with the exact grader:
> Submission	Construction	Score
> Global scalar	One constant everywhere; special-cased by the grader	0.0100
> Random uniform	Median over 20 fixed seeds	0.0326
> Unchanged sample_submission.csv	Exact coalition calculation with R = 0	0.1246
> Training-mean residual	Set each of the 24 by 3 residual positions to its training-set mean, then apply the exact coalition calculation	0.1435
> Residual Extra Trees diagnostic	Fit a CPU Extra Trees regressor to the 24 by 3 training residual and apply the exact coalition calculation	0.4169
> Training-mean utility lattice	Repeat the elementwise mean 24 by 31 training target; public-only	0.4176
> Target-context plus phase Extra Trees	Case-level public-only regression	0.4421
> Endpoint residual interpolation	Linearly bridge the last observed pre-outage and first observed post-outage target residuals	0.4593
> Creator public CPU reference	Invert positive training utilities into a residual proxy, learn an endpoint correction, then rebuild the lattice	0.4726
> Oracle plus Gaussian residual noise, sigma 0.30	Sensitivity diagnostic, not a contestant baseline	0.4992
> Oracle plus Gaussian residual noise, sigma 0.20	Sensitivity diagnostic, not a contestant baseline	0.5655
> Oracle plus Gaussian residual noise, sigma 0.10	Sensitivity diagnostic, not a contestant baseline	0.6980
> Oracle plus Gaussian residual noise, sigma 0.05	Sensitivity diagnostic, not a contestant baseline	0.8152
> Exact hidden answer	Private answer file	1.0000
> The training-mean residual and residual Extra Trees rows are creator diagnostics computed from the training residual before it is transformed into utilities. They establish target sensitivity but do not expose test residuals. The training-mean lattice, target-context model, endpoint interpolation, and creator reference use public files only. Scores are rounded to four decimals; calibration and release-validation reports contain the unrounded results.
> Submission
> Write the final file to ./working/submission.csv with exactly these columns in this order:
> Column	Description
> case_id	Test identifier copied unchanged from test.csv.
> target_sequence	JSON numeric matrix with exactly 24 rows and 31 columns.
> Requirements:
> Include exactly 223 rows, one for every test case_id.
> IDs may be reordered because grading aligns by case_id.
> Duplicate, missing, blank, extra, or unknown IDs reject the submission.
> Values must be finite and lie within [-0.25,1.25]. The natural utility range is [0,1]; the wider parser range permits ordinary numerical overshoot.
> Malformed JSON, wrong shapes, nulls, infinities, or extra columns reject the submission.
> Compute and resource rules
> This is a CPU-only challenge. Use the provided offline CPU environment. The deterministic creator reference algebraically inverts usable training-coalition labels into a latent residual proxy, fits scikit-learn Extra Trees to a time-local endpoint correction, and rebuilds the lattice with the published formula. It requires no accelerator, internet access, hosted API, closed model, or external dataset.
> Do not attempt source-record matching, decode case_id, use external observations, or locate hidden station-time records. General-purpose libraries already installed in the environment are allowed.
> What makes the task interesting
> The target has two coupled axes. Across time, the hidden local state changes through a long outage. Across the subset lattice, adding a sensor can help, add no coverage, or incur enough cost to reduce utility. The 31 outputs are therefore neither independent regressions nor a simple monotone ranking. A good solution must combine bidirectional target context, regional trajectories, masks, geometry, seasonality, and the known coalition construction while generalizing to unseen target sites and year.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## SkyFill: Grammar-Constrained Aviation Code Infilling

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7e8wqacx58gkvgb6cb55dq0h8c48k6
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat shiva_dev's score of 67.779!

Full challenge description from page:

> Leaderboard
> (16)
> Your Submissions
> SkyFill: Grammar-Constrained Aviation Code Infilling
> Overview
> The NOAA Aviation Weather Center distributes completed METAR and SPECI surface-weather observations. These reports encode wind, visibility, weather, clouds, temperature, and pressure as a compact sequence of grammar-constrained groups. SkyFill models transmission repair: two non-remark groups are removed from each completed report and must be restored exactly.
> Station identity and observation time are replaced by <STATION> and <OBS_TIME> inside public reports, and stations receive opaque tokens. This prevents direct report lookup while retaining report type and local code context. Test stations never occur in training. The task is sequence infilling for fine-tuning, not weather forecasting.
> Objective
> Replace <MASK_1> and <MASK_2> with the exact omitted whitespace-delimited METAR groups.
> Dataset
> train.csv has 333 rows:
> Column	Type	Meaning
> example_id	string	Unique opaque report ID
> station_token	string	Opaque station-group identifier
> report_type	categorical string	METAR or SPECI
> masked_report	string	Completed report with station/time redacted and exactly two mask markers
> missing_group_1	string	Original group at <MASK_1>
> missing_group_2	string	Original group at <MASK_2>
> test.csv has 67 rows and the first four columns above, omitting only the two targets. Test station tokens never occur in train. sample_submission.csv has 67 rows and exactly the three submission columns documented below.
> Submission Format
> The submission must have exactly three columns: example_id (string), missing_group_1 (string), and missing_group_2 (string), with one unique row per test example. Answers must contain only the replacement group, not a mask marker.
> example_id,missing_group_1,missing_group_2
> M_00E9CC3B96901E68,BKN110,A3000
> The example is a labelled public training row.
> Evaluation
> Normalize every answer by converting it to uppercase, collapsing whitespace, and trimming. For normalized strings p and y, let d(p,y) be character-level Levenshtein distance and
> s(p,y) = 1 - d(p,y) / max(|p|, |y|, 1).
> For each row, let s1 and s2 be the two similarities, e1 and e2 indicate exact normalized recovery of each group, and e12 indicate that both groups are exact. The row score is:
> 25*s1^2 + 25*s2^2 + 20*e1 + 20*e2 + 105*e12 - 45
> The final score is the mean row utility and is clipped to [0,150]; higher is better. Exact recovery of both groups scores 150. Before final clipping, every row pays a 45-point incomplete-repair penalty, and only an exact two-group restoration earns the 105-point joint term. A correct group still earns its exact-group credit, and squared edit similarity still distinguishes close attempts from unrelated strings, but neither can substitute for completing the whole report.
> This coupling reflects the operational structure of METAR repair: leaving either blank incorrect can change the decoded wind, visibility, weather, cloud, temperature, or pressure state. The metric therefore treats the two replacements as one repaired message while retaining continuous diagnostic credit for each group. Predictions that scored 121/150 under the previous linear character metric can score at most 112.300/150 (74.87%) under this contract if their outputs are unchanged.
> Missing rows, duplicate IDs, nulls, wrong columns, or any ID mismatch score 0.
> Not Allowed Methods
> Internet access, live weather feeds, or external APIs at inference time.
> Looking up held-out reports or reconstructing them from timestamps in an external archive.
> Using private answers, grader internals, or files outside the public package.
> Manual labeling or per-test-row hard-coding.
> Pretrained language models and models trained or fine-tuned solely on the supplied public data are allowed.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Evidence-Grounded Clause Patch Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fy19sm179v9gav6f95mvmn58apm9x
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat minipeepee's score of 0.742!

Full challenge description from page:

> Leaderboard
> (20)
> Your Submissions
> Overview
> Legislative revision is a state-transition problem. A policy explanation describes what should change, but the operational result is a precise sequence of insertions, deletions, and replacements in a legal clause. Near-final drafts can be especially dangerous because a version that misses one small edit may still read naturally.
> Each case contains:
> a short amendment context explaining the policy change;
> the clause before revision;
> four incomplete revised-clause proposal cards;
> a bank of candidate patch operations grounded in those cards.
> No card is guaranteed to be the complete revision. Each card mixes supported and unsupported changes. Every proposed edit locus has one competing operation from each of the four cards; supported loci require exactly one of those operations, while unsupported loci require none. Reconstruct the supported patch ledger by selecting the context-grounded operations across the cards. A correct ledger normally references multiple cards, so selecting one proposal and diffing it is insufficient.
> One supported operation carries a rationale-grounded audit qualifier assembled from the supplied amendment context. Competing qualifiers use other plausible context fragments. This private redline layer makes the target a new evidence-conditioned revision rather than a recoverable copy of a published clause.
> All clauses use explicit whitespace-separated tokens. Legal reference codes are anonymous and case-specific. Training and test cases come from disjoint law families, and every test source appears only once. The public split contains 1,080 training cases and 150 test cases.
> Patch Operations
> Token spans use zero-based, half-open indexing: start:end contains tokens from start through end - 1.
> Three operations are available:
> REPLACE|card|base_start:base_end|card_start:card_end
> DELETE|card|base_start:base_end
> INSERT|card|base_position|card_start:card_end
> Example ledger:
> REPLACE|R02|14:17|14:20 ; INSERT|R00|39|42:47 ; DELETE|R03|61:64
> Operations may reference different revision cards. Every submitted operation must occur verbatim in that case's proposal_operations bank. Operation order does not affect scoring.
> Dataset
> train.csv contains 1,080 labeled revision cases.
> test.csv contains 150 unique-source cases with patch ledgers withheld.
> sample_submission.csv contains one random but syntactically valid ledger for every test case.
> train.csv Columns
> case_id (string): anonymous training identifier.
> amendment_context (string): tokenized policy explanation associated with the revision.
> base_clause (string): clause text before the amendment, rendered as whitespace-separated tokens.
> revision_cards (string): four incomplete proposal clauses labeled R00 through R03.
> proposal_operations (string): semicolon-separated operation bank available for selection.
> patch_ledger (string): gold semicolon-separated patch operations.
> test.csv Columns
> case_id (string): anonymous test identifier.
> amendment_context (string): policy explanation.
> base_clause (string): tokenized pre-revision clause.
> revision_cards (string): four incomplete proposal clauses.
> proposal_operations (string): candidate operation bank; the supported subset is withheld.
> sample_submission.csv Columns
> case_id (string): test identifier copied from test.csv.
> pred_patch_ledger (string): example generated patch ledger.
> Submission Format
> Write ./working/submission.csv with exactly these columns:
> case_id,pred_patch_ledger
> Example rows:
> RCTE_1a32d91102ce,REPLACE|R02|14:17|14:20 ; INSERT|R00|39|42:47
> RCTE_93f47c29ab11,DELETE|R00|8:11
> Submission rules:
> Every test case_id must appear exactly once.
> Missing IDs, unknown IDs, duplicate IDs, and extra columns are rejected.
> A valid non-empty ledger may contain between one and twelve operations.
> Every card and token span must exist in that case.
> Every operation must be copied exactly from that case's proposal_operations bank.
> Base spans may not overlap, two insertions cannot use the same base position, and duplicate operations are invalid.
> Empty or malformed generated ledgers receive zero credit for that row instead of failing the complete grading run.
> Evaluation
> The score is bounded in [0, 1], and higher is better:
> Score = 0.40 * PatchOperationF1 + 0.60 * ExactPatchLedgerAccuracy
> The weights sum to exactly 1.00. No hidden track or additional multiplier is used.
> PatchOperationF1
> For each case, the predicted and gold patch operations are treated as sets. A true positive must match the operation type, provenance card, base span, and proposal-card span exactly. Selecting a conflicting or unsupported proposal creates a false positive, while omitting a supported proposal creates a false negative.
> With TP, FP, and FN denoting correct, additional, and missed operations:
> RowPatchF1 = 2 * TP / (2 * TP + FP + FN)
> PatchOperationF1 is the arithmetic mean of row F1 over the complete test set.
> ExactPatchLedgerAccuracy
> The fraction of test cases where the complete predicted operation set exactly equals the gold operation set. Order and surrounding whitespace are ignored. This majority-weight component rewards globally consistent reconstruction rather than independent local guesses.
> Allowed And Prohibited Methods
> Allowed:
> CPU-compatible retrieval, sparse text, sequence alignment, compact encoder, and constrained-generation models trained on the public data.
> Deterministic parsing and constrained selection over the supplied proposal-operation bank.
> Generic pretrained text encoders that fit the platform runtime.
> Prohibited:
> Searching external legal databases for the original clause history.
> Reconstructing hidden law identifiers, public source order, or private labels.
> Hardcoded test ledgers or manually prepared source-to-answer maps.
> Reading private platform files or using external prediction APIs.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Audio-Guided Articulator Sequence Inpainting

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx714g58a3s903ppp2y4ztty9s8bvx2t
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat sa3dola's score of 0.710!

Full challenge description from page:

> Leaderboard
> (15)
> Your Submissions
> Overview
> This is a CPU-only audio and multimodal sequence-to-sequence challenge. Speech-production systems often observe lips and jaw motion more easily than internal tongue motion, yet tongue shape is central to many Mandarin contrasts. Solvers must recover a masked internal articulator sequence from real speech-derived evidence: compact audio features plus visible electromagnetic-articulography context from lips, jaw, nose, and reference sensors.
> Each row is a short utterance represented by one public .npz payload. The payload contains a deidentified, frame-aligned visible-articulator panel and four audio-derived channels. For every test row, generate the hidden 3D articulator sequence for the requested tongue sensor: tongue_tip, tongue_blade, or tongue_dorsum.
> The public rows use opaque IDs and local paths only. Original filenames, speaker IDs, session IDs, dates, source paths, stimulus indices, prompt text, TextGrid labels, and source list positions are not participant inputs. Public arrays are normalized, temporally aligned, and source-deidentified during preparation, so the intended route is to learn speech-production structure from the provided training data rather than matching files back to the upstream corpus.
> The output is a time-indexed articulatory sequence, so the challenge belongs to audio, multimodal, sequence-to-sequence, from-scratch, and generative recovery. It is not ASR, transcript generation, speaker identification, EEG decoding, EMG decoding, table-field modeling, single-label inference, or source-corpus retrieval.
> This is a CPU-only challenge. Every valid solution must run with 10 CPU cores, 62 GB RAM, and a maximum runtime of 1.5 hours. All preprocessing, model training or adaptation, inference, and submission writing must finish inside that single CPU run.
> Task
> For every test id, use the row's public input payload and requested target_sensor to emit one hidden tongue-sensor sequence. The emitted payload must be a compressed .npz, base64-encoded in pred_ema_b64.
> The target object is a dense geometric sequence: a float32 array with shape [T,3], where T is the row's n_frames. The three coordinates should describe the hidden tongue sensor through the utterance. A submission may also include an optional valid_mask inside the .npz.
> Successful solutions should recover both the position pattern and the movement dynamics. A solution that emits only a static average shape, only follows the lips, or only exploits duration will miss important scored structure.
> Intended Approach
> Strong solutions should train compact architectures from scratch, as long as the full pipeline runs offline on CPU within the time limit. The best approaches should use the provided speech-audio features and visible EMA context jointly, not metadata or lookup shortcuts.
> Useful CPU-feasible routes include a shared sequence model for visible_ema and audio_feat, a target-sensor embedding, continuity-aware smoothing, compact one-dimensional neural models, lightweight attention over local windows, frame-level sequence heads over learned features, and calibrated post-processing that respects continuity. Validation should select models by the disclosed full metric, not a single coordinate-distance term alone.
> CPU feasibility has been measured on the prepared data. On the rebuilt 1977-train/523-test package, the sample prior scores 0.120329, the strongest single CPU probe scores 0.237402, and the strongest two/three-method CPU ensemble scores 0.250263, leaving substantial headroom to a perfect score of 1.0. Use vectorized loading, bounded training loops, and a runtime guard so submission validation always completes before 1.5 hours.
> What Not To Use / What Not To Do
> Do not use the internet, external datasets, source-archive lookup, recovered source filenames, recovered prompts, source speaker IDs, source material IDs, or external answer services while solving.
> Do not use row position, IDs, payload paths, file sizes, byte hashes, archive metadata, private files, grader internals, malformed-input behavior, hard-coded answer maps, manual test labels, or hosted APIs as answer channels. Do not silently disable the learned model and fall back to a metadata or lookup shortcut when inference fails.
> Use only the provided public challenge data and learned or signal-processing models trained from that data.
> Evaluation
> Higher is better. The score is a transparent structured sequence-recovery metric:
> row_score =
> 0.40 * payload_sequence_match
> + 0.42 * delta_agreement
> + 0.10 * motion_shape_agreement
> + 0.08 * mask_agreement
> final_score =
> 0.85 * mean(row_score)
> + 0.10 * worst_mean_by_hidden_speaker_group
> + 0.05 * worst_mean_by_material_family
> The four row components are:
> | Component | Meaning |
> |---|---|
> | payload_sequence_match | Exponential match score from the frame-level coordinate distance, scaled by the gold payload's centered movement scale. |
> | delta_agreement | Frame-delta correlation clipped to [0,1], i.e. max(0, corr); uncorrelated, opposite, or degenerate deltas receive 0. |
> | motion_shape_agreement | Speed-profile agreement with a small path-length sanity term. |
> | mask_agreement | Mean agreement with the gold valid mask, or 1 when no optional submitted mask is supplied. |
> Hidden speaker and material groups are used only for robustness, and the hidden test split contains multiple speaker groups and balanced material families. Their labels are not public because they would expose source identity and material family.
> All terms lie in [0,1]; the theoretical minimum is 0.0, the theoretical maximum is 1.0, and a perfect valid submission scores exactly 1.0. There is no score cap, arbitrary power, or hidden suppression curve.
> Submission-level structure is strict. Missing, extra, or shuffled columns; duplicate IDs; missing or foreign IDs; unreadable private answers; and unsafe global schema mismatches raise an invalid-submission error. In an otherwise structurally valid submission, row-local malformed payloads, missing values, non-finite arrays, wrong shapes, invalid masks, or overlong base64 strings receive 0 for that row without crashing the grader. Grader errors do not reveal private labels, hidden groups, split logic, or answer content.
> Dataset
> The prepared public data contain 2,500 short utterance examples: 1,977 labeled training rows and 523 hidden-target test rows. Input paths are relative to public/.
> File overview
> | Item | Type / count | Description |
> |---|---|---|
> | train.csv | 1,977 rows | Labeled examples with one hidden tongue payload per row. |
> | test.csv | 523 rows | Hidden-target examples with the same public input fields. |
> | train/inputs/*.npz | 1,977 files | Frame-aligned visible EMA and audio-feature payloads for training rows. |
> | test/inputs/*.npz | 523 files | Frame-aligned visible EMA and audio-feature payloads for test rows. |
> | dataset_manifest.json | JSON | Row counts, public tensor shapes, sensor sets, and deidentification summary. |
> | sample_submission.csv | 523 rows | Valid weak baseline with the exact required schema. |
> Each input .npz contains:
> | Key | Dtype and shape | Description |
> |---|---|---|
> | visible_ema | float32, [T,18] | Visible EMA context from upper lip, lower lip, lower jaw/incisor, nose, left reference, and right reference. |
> | audio_feat | float32, [T,4] | Short-window RMS energy, zero-crossing rate, mean absolute waveform difference, and frame-to-frame RMS-energy delta. |
> | visible_mask | bool, [T] | Valid-frame mask after preparation. |
> The visible EMA channels are arranged as upper lip, lower lip, lower jaw/incisor, nose, left reference, and right reference, each with x, y, and z coordinates in the prepared articulography frame.
> train.csv columns
> | Column | Type | Description |
> |---|---|---|
> | id | string | Opaque row key used for alignment only. |
> | input_path | string | Relative path to the row's public NPZ payload. |
> | target_sensor | enum string | Requested hidden sensor: tongue_tip, tongue_blade, or tongue_dorsum. |
> | n_frames | integer | Required payload length T. |
> | target_ema_b64 | base64 string | Training label payload; decodes to a compressed NPZ with values: float32 [T,3]. |
> test.csv columns
> | Column | Type | Description |
> |---|---|---|
> | id | string | Opaque row key used for submission alignment. |
> | input_path | string | Relative path to the row's public NPZ payload. |
> | target_sensor | enum string | Requested hidden sensor: tongue_tip, tongue_blade, or tongue_dorsum. |
> | n_frames | integer | Required payload length T. |
> Test rows omit target_ema_b64.
> Submission
> Write submission.csv with exactly 523 rows and exactly these columns as shown:
> | Column | Type | Constraint |
> |---|---|---|
> | id | string | Exact test ID set; each ID appears once. |
> | pred_ema_b64 | base64 string | Compressed NPZ output payload. |
> Each pred_ema_b64 value must decode to a compressed .npz with:
> | NPZ key | Required? | Dtype and shape | Meaning |
> |---|---|---|---|
> | values | yes | float32, [T,3] | Submitted hidden tongue-sensor coordinates. |
> | valid_mask | no | bool, [T] | Optional submitted valid-frame mask. |
> T must equal that row's n_frames. Values must be finite.
> Sample submission
> id,pred_ema_b64
> ema_0123456789abcdef,UEsDBBQAAAAI...
> ema_fedcba9876543210,UEsDBBQAAAAI...

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Mine Inspection Activity Chain Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bn49aykgrvbb8g1t496805h8c5r27
- DOMAIN exactly as displayed: Sequence To Sequence
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
> Each item is an anonymized mine inspection history. A US mine is inspected repeatedly over its operating life by federal safety inspectors, and every inspection records an activity code describing what kind of inspection was performed — regular safety and health check, spot inspection, hazard-complaint response, sampling visit, technical assistance, and so on. Grouping the inspection rows by mine and ordering them by inspection start date yields, for each mine, its ordered chain of activity-code events.
> Your task is activity-chain reconstruction: given a mine's anonymized kind bucket (coal vs metal/non-metal), operator bucket (which large operator, if any, runs it), and a prefix of its first several inspections, forecast the ordered sequence of remaining activity-code events the mine will accumulate across subsequent inspections.
> This matters operationally: forecasting the remainder of a mine's inspection cadence from an opening prefix lets a safety-oversight programme anticipate where scheduled and reactive inspections will land, plan inspector routing, and pre-position enforcement capacity before those inspections actually happen.
> Data
> train.csv, test.csv, and sample_submission.csv are UTF-8 CSV with a header.
> Training
> train.csv — columns item_id, mine_kind, operator_bucket, chain. chain is the full ordered inspection history for the mine, encoded as a space-separated list of AC## activity-group tokens (for example AC00 AC12 AC00 AC03 AC00). The first token is the earliest observed inspection for the mine. Use these chains to learn the inspection dynamics.
> Test
> test.csv — columns item_id, mine_kind, operator_bucket, prefix_chain. The prefix_chain exposes the first 20-45% of the mine's inspections (length varies per mine); the remaining chain is withheld.
> sample_submission.csv
> A weak baseline that predicts, for every test mine, the single globally-most-common next activity group. It scores far below any real model.
> metadata.json
> Keys task, columns, submission_columns, submission_note, metric, files. Informational.
> Task
> For each test mine, output the ordered sequence of remaining activity-code events after the given prefix — one row per predicted event, in order.
> Evaluation
> Composite chain score in [0, 1], averaged over test cases. For each mine, comparing your predicted remaining chain to the gold chain:
> chain_sim — normalized edit similarity 1 - Levenshtein / max-length on the ordered activity-group sequences.
> set_recall — the fraction of distinct activity groups appearing in the gold remaining chain that also appear in the predicted remaining chain (ignores order and multiplicity).
> length_acc — 1 - min(1, |len_pred - len_gold| / max(1, len_gold)), rewarding predicting the right number of remaining events.
> The case score is 0.60 * chain_sim + 0.25 * set_recall + 0.15 * length_acc. A case with no predicted rows scores 0. The final score is the mean over all test cases, higher is better.
> Submission format
> A UTF-8 CSV with a header and exactly these columns, in order:
> item_id,position,activity_group
> item_id — string; a test mine id.
> position — integer >= 0; the 0-based order of this event within your predicted remaining chain.
> activity_group — string; the predicted activity-group code for this event.
> Example
> For a test set containing two mines mine_abc123def456 (predicting 4 remaining events) and mine_ghi789jkl012 (predicting 3 remaining events), a valid submission looks like:
> item_id,position,activity_group
> mine_abc123def456,0,AC00
> mine_abc123def456,1,AC03
> mine_abc123def456,2,AC00
> mine_abc123def456,3,AC12
> mine_ghi789jkl012,0,AC00
> mine_ghi789jkl012,1,AC00
> mine_ghi789jkl012,2,AC07
> Notes on the example:
> Each row is a single predicted event; the full remaining chain for one mine spans several rows.
> position restarts at 0 for every new item_id and increases by 1 for each subsequent event.
> Different mines can have different predicted chain lengths.
> Every test item_id from test.csv should appear at least once (otherwise that case scores 0).
> Requirements (violations rejected as invalid): exactly the columns above; only known test item_ids; integer position >= 0; no duplicate (item_id, position); at most 40 predicted events per mine. A case with no predicted rows earns 0 on that case. A blank activity_group cell simply fails to match.
> Allowed
> Any classical or neural sequence model fitted on the provided data.
> TF-IDF, n-gram language models, hidden Markov models, RNN/Transformer trained from scratch, or gradient-boosted models on hand-crafted sequence features.
> Solutions must run on the provided CPU environment within the platform time budget.
> What Not To Use
> No external datasets or annotations for this domain, and no off-the-shelf model already trained on this corpus. Pretrained general-purpose backbones are fine, but the codes are opaque so they confer no lookup advantage.
> No network access at run time. Every prediction must come from a model that consumes the released inputs only.
> No attempting to identify or retrieve the source mines.
> No hardcoded per-item_id predictions, no row-order shortcuts, no use of any answer file.
> No GPU or CUDA execution — solutions must remain within the CPU budget.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Nosopath: Clinical Concept Trace Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dbtwzcmny0q41n2xbdp4j858c2sdq
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, small-data, medical, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 60.411

Full challenge description from page:

> Nosopath: Clinical Concept Trace Recovery
> Overview
> Clinical notes often mention several related disease findings in a short span, while the normalized concept identity is a hidden ontology-level structure. In this challenge, each row contains a lossy Spanish clinical window with 2 to 4 marked disease mentions. The task is to recover the ordered normalization trace: for every marked mention, predict its semantic relation type and normalized concept code.
> The mention surfaces are partially masked, non-query disease mentions are replaced by nuisance markers, and numeric identifiers are zeroed. Each marked mention includes a shuffled candidate-code set containing the correct code plus plausible decoys. The intended first-order approach is to combine the masked mention text, local clinical context, candidate-code ambiguity, and relation patterns learned from train rows.
> Evaluation Metric
> For row i, let T_i be the true set of trace tokens and \widehat{T}_i be the predicted set. A token has the form mK|REL|CODE, where REL is one of EXACT, NARROW, COMPOSITE, or NOMAP.
> For sets P and T, let c=|P\cap T|, precision p=c/|P|, and recall r=c/|T|. The F1 score is F(P,T)=2pr/(p+r). If c=0, then F(P,T)=0.
> Full trace score: F_i^{full}=F(\widehat{T}_i,T_i).
> Code score: form slot-code tokens mK|CODE; F_i^{code} is the F1 between predicted and true slot-code sets.
> Relation macro-F1: for each relation r, compare the set of slots assigned relation r. Average F1 over relation classes that appear in either prediction or truth to get F_i^{rel}.
> Order similarity: let D_i be the Levenshtein edit distance between predicted and true ordered trace-token sequences. Let L_i=\max(|\widehat{T}_i|,|T_i|,1), and Q_i=1-D_i/L_i.
> Row score: R_i=0.45F_i^{full}+0.30F_i^{code}+0.15F_i^{rel}+0.10Q_i.
> Final score: S=100\times\operatorname{clip}_{[0,1]}\left(\frac{1}{N}\sum_i R_i\right).
> Malformed row traces receive zero for that row. The minimum score is 0, meaning no credited recovery. The maximum score is 100, meaning every concept code, semantic relation, and sequence position is correct.
> Measured on the shipped files and grader:
> Perfect answers: 100.000000.
> First-candidate sample submission: 19.462153.
> Majority shortcut: 15.997743.
> Span dictionary: 58.012847.
> Span-prefix dictionary: 59.256324.
> Lexical candidate ranker: 62.961086.
> Dataset
> The public package contains four files:
> train.csv - 468 labeled rows.
> id - integer row identifier.
> evidence - lossy clinical text window. Query mentions are marked inline as [m0] ... [/m0], [m1] ... [/m1], and so on. Digits in the clinical text are replaced with 0; the interiors of marked mention words are partially masked with *; non-query disease mentions appear as [DISEASE] or [COND] placeholders. Each row ends with a candidate block such as || CANDIDATES: m0=CODE,CODE,... ; m1=CODE,CODE,..., where each marked mention has a shuffled list of candidate normalized concept codes.
> trace - ordered target string. It contains one space-separated token per marked mention, ordered by mention slot from m0 upward. Each token has the form mK|REL|CODE, where REL is EXACT, NARROW, COMPOSITE, or NOMAP, and CODE is the selected normalized concept code.
> test.csv - 480 query rows.
> id - integer row identifier.
> evidence - same structure as in train.csv, but without the trace target column.
> sample_submission.csv - 480 valid predictions using the first listed candidate with relation EXACT.
> metadata.json - row counts, id ranges, score range, and public balance counts.
> Ids are zero-based and split by file: train.csv uses ids 0 through 467, and test.csv uses ids 468 through 947. Therefore the example submission ids 468, 469, and 470 are test ids.
> Rows are split by source document, so no source document contributes windows to both train and test. The test set is balanced over mention count and whether the trace contains a narrow or composite normalization. The nuisance marker style is retained as an unscored visible distractor and kept approximately balanced. Source document identifiers, source filenames, offsets, raw spans, raw codes outside the trace, split keys, and nuisance labels are not present in public files.
> Submission
> Submit a CSV with a header and exactly 480 rows. Columns must appear in this exact order:
> id - integer - a test identifier appearing exactly once.
> trace - string - space-separated tokens of the form mK|REL|CODE, ordered from m0 through the last marked mention.
> The number of tokens must match the marked mentions in the row evidence. Example using real test identifiers:
> id,trace
> 468,m0|EXACT|66058000 m1|EXACT|77176002
> 469,m0|NARROW|228272008 m1|EXACT|389026000 m2|EXACT|389026000
> 470,m0|EXACT|5291005 m1|EXACT|126634001 m2|EXACT|253883006
> Rows may be reordered because scoring aligns by id. Duplicate, missing, unknown, or extra identifiers; a wrong row count; extra or reordered columns; or a missing header cause a clean submission-level rejection. Within an otherwise valid submission, malformed tokens, duplicate slots, skipped slots, unknown relation strings, NaN, or infinite values receive zero for that row.
> What Not to Use
> Always choosing the first candidate ignores clinical context and scores 19.462153.
> A majority-code shortcut fails because candidate order and nuisance marker style are balanced independently of the answer.
> Exact string lookup is brittle because query mentions are partially masked and clinical variants differ across documents.
> Treating each mention independently loses useful context from neighboring diagnoses and case narrative.
> External source alignment is blocked by opaque ids, document-level splitting, masked numbers, removed filenames, and stripped offsets.
> Expected solutions use candidate ranking, Spanish clinical context, masked mention morphology, relation calibration, and sequence consistency across the marked window.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Time-Aware Skill Extraction From Resumes

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f91z7j9xnpbfk67758kv5tx83recx
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: small-data, text, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.511

Full challenge description from page:

> Overview
> This challenge introduces time-aware skill extraction: given the Experience section of a resume, systems must predict not only which skills appear in a candidate's profile, but how many months of accumulated experience the candidate has with each skill.
> This distinction matters. Listing a skill on a resume is easy; understanding whether it reflects two months, two years, or ten years of experience is much more valuable for downstream applications such as:
> candidate ranking,
> job matching,
> talent search,
> workforce analytics,
> and skill-based profiling.
> In real hiring settings, a candidate who briefly used a skill in a single role should not be treated the same as a candidate who applied it consistently across multiple years of work experience. This challenge therefore focuses on time-aware extraction, where systems must infer both:
> the relevant skill labels, and
> the corresponding months of experience associated with each skill.
> The objective of the challenge is to develop models that can read the Experience section of resumes and produce structured outputs in the form of:
> [
> {"skill": "sales", "months": 252},
> {"skill": "cash management", "months": 132}
> ]
> Solving this task requires a system to perform, in one pipeline: skill identification and normalization to a closed set of categories, temporal grounding of each skill to the date ranges of the roles where it was used, and aggregation across roles with union handling of overlapping periods. None of these steps is evaluated in isolation; only the final per-skill duration profile is scored.
> Relation to existing tasks
> Skill extraction from resumes and job postings is well studied, and public models exist that tag skill or duration spans at the token level. However, to our knowledge, no public benchmark evaluates per-skill experience duration as an end target. Span-level tasks stop at "this text mentions sales"; this challenge asks "this candidate has 84 months of sales experience". Producing that answer requires composing entity normalization, temporal interval arithmetic, cross-role aggregation, and overlap handling. The evaluation metric is also task-specific: a Soft Skill-Month F1 that jointly scores skill identification and duration accuracy.
> Dataset
> Each row in the dataset corresponds to one resume entry and contains the experience text plus the skill-duration annotations.
> Files
> train.csv — labeled training data
> test.csv — unlabeled test data for prediction
> Fields
> | Column | Type | Description |
> |--------|------|-------------|
> | id | int | Unique identifier for the resume entry |
> | Experience | string | Text from the resume’s experience section|
> | skills_with_months_json | string (JSON) | a JSON array of objects, each with a 'skill' and 'months' value |
> Example
> Input row
> id: 17
> Experience: Senior Sales Associate, May 2010 - Present. Managed retail sales, merchandising, cash handling, and customer operations...
> Target
> [
> {"skill": "sales", "months": 188},
> {"skill": "sales & merchandising", "months": 188},
> {"skill": "cash management", "months": 188}
> ]
> Month calculation rules
> Skill durations are measured in months and follow these rules:
> Count months inclusively
> 05/2014–08/2015 = 16 months
> May–Aug 2015 = 4 months
> 2011–2014 = 48 months
> For Present / Current / Now, use:
> CURRENT_DATE = 31 December 2025
> If only years are given, assume:
> January of the start year
> December of the end year
> If a range is written like May–Aug 2015, assume both months are in 2015
> If the same skill appears in multiple role entries, add the months across those entries
> If overlapping roles contain the same skill, do not double count the overlap:
> use the union of the overlapping dates, not the sum of both spans
> Scope simplifications
> To keep the task focused and feasible:
> only the Experience section is provided, not the full resume
> and the annotation uses general skill categories rather than highly granular skill mentions.
> Submission
> Submit a submission.csv with two columns:
> id
> skills_with_months_json
> Evaluation
> Submissions are evaluated using Soft Skill-Month F1, a metric designed for this task, averaged across all resumes. Standard extraction metrics ignore duration entirely, and standard regression metrics ignore which skills were found; Soft Skill-Month F1 evaluates both jointly.
> For a given resume:
> let G be the set of gold skills,
> let P be the set of predicted skills.
> For each skill that appears in both the gold and the prediction, we compute a month similarity score as:
> sim(m_true, m_pred) = min(m_true, m_pred) / max(m_true, m_pred)
> This gives:
> 1.0 if the predicted number of months is exactly correct,
> a value between 0 and 1 if it is close,
> and lower values as the prediction gets farther from the true duration.
> The score for one resume is:
> Score = 2 × sum of similarity scores over matched skills / (number of gold skills + number of predicted skills)
> The final leaderboard score is the average of this score across all resumes.This metric is well suited to the task because it:
> rewards predicting the correct skills,
> rewards accurate month estimates,
> penalizes missing and extra skills,
> and gives partial credit when the predicted duration is close to the gold value.
> Submission format
> | Column | Type | Description |
> |--------|------|-------------|
> | `id` | int | The unique identifier from the test set |
> | `skills_with_months_json` | string (JSON) | Your predicted list of skill-duration pairs|
> Example submission
> id,skills_with_months_json
> 18,"[{""skill"": ""sales"", ""months"": 188}, {""skill"": ""cash management"", ""months"": 188}]"
> 19,"[{""skill"": ""data analysis"", ""months"": 36}]"
> Notes
> skills_with_months_json must be a valid JSON array.
> skills_with_months_json is only present in train.csv and is the column participants must predict for test.csv
> Doubled quotes ("") in JSON fields are normal CSV escaping and will be read correctly by standard tools such as pandas.read_csv().
> What not to use
> The following are not allowed:
> Generative / instruction-tuned LLMs, whether via API (GPT, Claude, Gemini, etc.) or run locally (Llama, Qwen, etc.), for prediction, pseudo-labeling, or data augmentation.
> External APIs or online services at inference time. Solutions must run fully offline.
> Hand-crafted skill lists or keyword-to-skill dictionaries as the skill prediction mechanism. Skill identification must come from a model trained on the provided data. (Hand-crafted features feeding into a trained model are fine.)
> Manual labeling of the test set, in whole or in part.
> The following are allowed:
> Rule-based code for date parsing and month computation (this part of the task is deterministic).
> Pretrained encoder models under 1B parameters (e.g., BERT, RoBERTa, DeBERTa, sentence-transformers), fine-tuned on the provided data.
> Classical ML (sklearn, gradient boosting, CRFs, etc.).

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Tabletop Spatial Event Graph Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76bszy2r2xe73fsrx4pjd47d8c4efq
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: video, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.525

Full challenge description from page:

> Overview
> Twelve people took part in a controlled tabletop study. In each recorded episode, one person rearranged three everyday objects while speaking in German about the manipulation. A fixed camera captured the table, and a tracking system recorded the position and confidence of every object over time.
> The three objects receive new anonymous IDs in every episode. Words that directly reveal an object or spatial relation are masked, but the remaining speech timing and tokens are retained. Your goal is to reconstruct the episode's grounded event graph: which anonymous object moved, which spatial relation it established, which object or objects it used as references, and when the event occurred.
> This is not ordinary action classification. One episode can contain several overlapping pieces of evidence and a variable number of structured events.
> Task
> For every episode, predict between 1 and 16 event objects. Each event contains:
> the anonymous object that moved;
> one relation from nextto, inbetween, behind, infrontof, or beyond;
> two reference objects for inbetween, or one reference object for every other relation;
> inclusive start and end bins on a 64-bin normalized annotation timeline.
> The event-list order does not affect scoring. Timing is evaluated through each event's start_bin and end_bin.
> The prepared dataset contains 33 training episodes from eight people and 18 test episodes from four different people. All episodes from one person remain in one split. Consequently, no test person appears in the training data.
> Dataset
> Public Files
> train.csv: 33 episodes with public inputs and answer_json labels.
> test.csv: 18 episodes with the same public inputs but no labels.
> sample_submission.csv: deterministic pseudo-random event graphs demonstrating the required output grammar.
> episodes/*.npz: object trajectories and their time/channel axes.
> frames/*.npz: uniformly sampled grayscale video frames.
> previews/*.jpg: eight-frame visual summaries of the videos.
> episodes/*.npz
> Each episode archive contains:
> Array	Type and shape	Description
> time	float32, (128,)	Monotonically increasing object-tracking timestamps in seconds.
> object_trace	float16, (128, 3, 4)	Interpolated object measurements. Axis 1 selects one anonymous object; axis 2 contains x, y, z, and tracking confidence.
> channel_ids	string, (3,)	Anonymous object ID for each axis-1 channel of object_trace, in the same order.
> The 128 trajectory samples describe the tracking timeline. They are separate from the 64 target bins: target bins normalize the annotated action interval, while the trajectory timestamps retain the tracking system's seconds.
> frames/*.npz and Previews
> frames is a uint8 array with shape (64, 96, 128): 64 grayscale frames, each 96 pixels high and 128 pixels wide, sampled uniformly across the full video.
> Each preview JPEG concatenates eight of those frames for quick inspection. The NPZ frames remain the modeling input.
> CSV Columns
> Column	Type	Description
> id	string	Unique episode identifier.
> episode_path	string	Path to the NPZ containing time, object_trace, and channel_ids.
> frames_path	string	Path to the NPZ containing the 64 video frames.
> preview_path	string	Path to the eight-frame JPEG preview.
> words_json	JSON array	Timed speech tokens. Each object has start and end times in seconds relative to the first annotation, plus a string token. Direct object terms are replaced by <object> and explicit spatial-relation terms by <relation>; all other retained tokens remain unchanged.
> object_ids_json	JSON array	The three valid anonymous object IDs. These are the same IDs stored in channel_ids.
> answer_json	JSON object, train only	An object with one key, events, containing the event objects defined in the Submission Format section.
> For target timing, the earliest annotated boundary is bin 0 and the latest is bin 63. Intermediate boundaries are mapped linearly and rounded to the nearest integer. Therefore start_bin and end_bin are normalized episode positions, not raw frame indices or tracking timestamps.
> Submission Format
> Submit exactly two columns in this order:
> id,answer_json
> Rows must appear in the same order as test.csv. Each answer_json value must contain exactly one key, events, whose value is a list of 1 to 16 objects. Every event must contain exactly:
> actor: one ID from that row's object_ids_json.
> relation: nextto, inbetween, behind, infrontof, or beyond.
> references: a sorted list of distinct IDs that excludes actor. It must contain two IDs exactly when relation is inbetween; otherwise it must contain one.
> start_bin and end_bin: integers satisfying 0 <= start_bin <= end_bin <= 63.
> For a row whose ID is ae_example and whose valid objects are object_21bf, object_a91c, and object_e412, this is a complete valid submission row:
> id,answer_json
> ae_example,"{""events"":[{""actor"":""object_a91c"",""relation"":""inbetween"",""references"":[""object_21bf"",""object_e412""],""start_bin"":22,""end_bin"":31}]}"
> Evaluation
> Let a predicted event be p and a true event be t.
> Event Identity
> Let A(p,t) be 1 when the actors match and 0 otherwise. Let R(p,t) be 1 when the relations match and 0 otherwise. Let J(p,t) be Jaccard similarity between the two reference sets:
> J(p,t) = |references_p intersect references_t| / |references_p union references_t|.
> The identity similarity is:
> I(p,t) = (A(p,t) + R(p,t) + J(p,t)) / 3.
> Temporal Similarity
> Bins are inclusive. For intervals [sp, ep] and [st, et]:
> intersection = max(0, min(ep, et) - max(sp, st) + 1)
> union = max(ep, et) - min(sp, st) + 1
> T(p,t) = intersection / union.
> Pair similarity is Q(p,t) = I(p,t) T(p,t).
> Episode Aggregation
> Suppose a row contains m predicted events and n true events. Both counts are at least 1. The grader constructs the complete m-by-n matrix of Q values and uses maximum-weight one-to-one assignment. Exactly min(m,n) pairs are assigned; unmatched events contribute zero.
> Define:
> S = sum of assigned Q values / max(m,n).
> X = number of assigned pairs with Q exactly 1 / max(m,n).
> C = exp(-|m-n| / 2).
> The episode score is:
> 0.15 S + 0.85 (S X C)^(1/3).
> S provides soft credit for partially correct identity, references, and timing. The coupled term requires exact complete events and penalizes an incorrect event count. The final score is the arithmetic mean over all test episodes. Scores range from 0 to 1, and higher is better. A perfect submission scores 1.
> Any malformed row, invalid object ID, illegal relation/reference combination, missing or extra ID, incorrect column order, or other submission-schema violation makes the complete submission score 0.
> Expected Approach
> Strong solutions will combine visual motion, anonymous object trajectories, the timing of partially redacted speech, spatial geometry, event segmentation, and constrained graph decoding. The held-out-person split tests whether those relationships transfer beyond the movement and speaking patterns seen during training.
> What Not To Use
> Do not use GPU acceleration.
> Do not use internet access, external APIs, hosted inference, or external datasets.
> Do not recover answers from private files, hidden metadata, source-corpus lookup, or hardcoded test mappings.
> Do not manually label the test cases.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Coordinate-Free Functional Vision Field Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx774tmn6qg05dy7qx21kfbqb58c190p
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.405

Full challenge description from page:

> Coordinate-Free Functional Vision Field Repair
> Overview
> Your objective is to reconstruct 14 masked locations in a coordinate-free functional visual-field graph. For every masked node, predict its current sensitivity bin, its change bin relative to an earlier test, and its local edge-strength bin. Also predict one token summarizing the relative sensitivity of the two masked regions.
> Standard automated perimetry measures how dim a light can be detected at fixed locations while a person maintains fixation. It is used to characterize functional visual-field patterns and change. These measurements are not photographs of sight, do not reproduce a person's subjective experience, and must not be interpreted as a universal answer to what blind people see.
> Each row uses two consecutive tests from one eye. The earlier test supplies only the 14 anchor values at the hidden locations. The current test supplies the other 38 locations. The 52 locations form a graph, but node labels are independently permuted in every row and exact coordinates are not released. A useful model must combine temporal anchors, visible current context, graph connectivity, and the relationship between two separated masked regions.
> This is a CPU Sequence-to-Sequence challenge. The intended approach is a compact graph-sequence model trained from scratch on the released examples. It is not an image-classification or diagnosis task.
> Dataset
> All public files are under ./dataset/public/.
> train.csv: 5,294 labelled graph-repair rows.
> test.csv: 2,104 held-out graph-repair rows without answers.
> sample_submission.csv: valid uninformative output at approximately uniform chance.
> dataset_metadata.json: public task dimensions and privacy controls.
> Patients are disjoint between train and test. Exactly one consecutive-test pair is selected per eye, so no source field is repeated across public rows.
> Columns
> id string): opaque identifier assigned only after patient splitting and packet shuffling.
> prompt string): shared sequence-repair instruction.
> field_packet_json JSON string): coordinate-free graph and visible evidence.
> answer_format_json JSON string): required arrays, lengths, order, and allowed tokens.
> answer_json JSON string, train only): target repair ledger.
> Field Packet
> field_packet_json contains:
> task string): task marker.
> node_count integer): always 52 scored visual-field nodes.
> graph_edges array): undirected pairs of zero-based node indices.
> masked_indices array): 14 target nodes in output order.
> mask_regions array): two seven-node lists; region A is first and region B is second.
> previous_anchor_bins array): earlier-test sensitivity bins for the 14 masked nodes, aligned with masked_indices.
> current_sensitivity_bins array): 52 current-test bins; -1 marks each masked node.
> time_gap_bin string): VERY_SHORT, SHORT, MEDIUM, or LONG.
> bin_order object): ordered token vocabularies for sensitivity, change, and edge values.
> Sensitivity bins run from 0 for the lowest source-derived sensitivity band to 6 for the highest. Change bins run from 0 for the strongest decrease to 6 for the strongest increase. Edge bins run from 0 for the smoothest local neighborhood to 3 for the strongest local contrast. The source dB thresholds are not released, and raw measurements never appear in public packets.
> Target Ledger
> answer_json contains exactly:
> {"current_bins":[0,1,2,3,4,5,6,0,1,2,3,4,5,6],"change_bins":[3,3,2,4,1,5,0,3,2,4,1,5,0,6],"edge_bins":[0,1,2,3,0,1,2,3,0,1,2,3,0,1],"profile_token":"REGION_A_LOWER"}
> All three arrays have length 14 and align exactly with masked_indices. profile_token is one of:
> REGION_A_LOWER: region A has distinctly lower current sensitivity than region B.
> REGION_B_LOWER: region B has distinctly lower current sensitivity than region A.
> BOTH_LOW: the two regions are similar and both fall in the lower profile band.
> BOTH_PRESERVED: the two regions are similar and fall in the higher profile band.
> Evaluation
> For each row, the grader calculates exact token accuracy for the 14 current bins, 14 change bins, and 14 edge bins, plus exact profile-token accuracy.
> row_score = 0.45 * current_bin_accuracy
> + 0.30 * change_bin_accuracy
> + 0.15 * edge_bin_accuracy
> + 0.10 * profile_exact
> The raw score rewards both average performance and robustness:
> raw_score = 0.70 * mean_row_score
> + 0.10 * weakest_severity_mean
> + 0.10 * weakest_mask_geometry_mean
> + 0.10 * weakest_change_volatility_mean
> weakest_severity_mean is the minimum row-score mean among the LOW, MID, and HIGH current-field sensitivity groups present in the scored partition. Training-derived tercile thresholds define these groups.
> weakest_mask_geometry_mean is the minimum mean among CENTRAL, MIXED, and PERIPHERAL dual-mask geometry groups present in the scored partition. Training-derived terciles of the two source-region eccentricities define these groups.
> weakest_change_volatility_mean is the minimum mean among STABLE, VARIABLE, and VOLATILE hidden-region change groups present in the scored partition. Training-derived terciles of mean absolute masked change define these groups.
> The robustness labels are private because some depend on hidden target values. Every group is represented in the full held-out set.
> Uniform random predictions have exact chance value:
> chance_floor = 0.45 / 7 + 0.30 / 7 + 0.15 / 4 + 0.10 / 4
> = 19 / 112
> The reported score is chance corrected:
> reported_score = clip((raw_score - 19/112) / (1 - 19/112), 0, 1)
> The score ranges from 0 to 1 and is maximized.
> Submission Format
> Submit exactly two columns in this order:
> id,answer_json
> vfr_0123456789abcdef,"{""current_bins"":[0,1,2,3,4,5,6,0,1,2,3,4,5,6],""change_bins"":[3,3,2,4,1,5,0,3,2,4,1,5,0,6],""edge_bins"":[0,1,2,3,0,1,2,3,0,1,2,3,0,1],""profile_token"":""REGION_A_LOWER""}"
> Requirements:
> Include exactly one row for every test id.
> Use exactly the columns id,answer_json in that order.
> Use valid JSON with exactly the four documented keys.
> Each array must contain exactly 14 integer tokens in the documented range.
> Use one of the four documented profile tokens.
> Missing, extra, unknown, or duplicate IDs are rejected.
> The runtime command is:
> python3 [solution.py](http://solution.py) <public_dir> <submission_out>
> Rules
> Training and inference must run on CPU using only standard libraries available in the execution environment.
> Train a local sequence, graph, or structured model from scratch on the released labelled rows.
> Use only files under the supplied public directory at runtime.
> Do not search external visual-field repositories, papers, or databases to match public packets to source tests.
> Do not reverse node permutations, public IDs, packet strings, or quantized patterns into source patient or eye identifiers.
> Do not use raw upload files, hidden preparation metadata, private answers, exact source coordinates, exact ages, gender, or laterality as prediction signals.
> Do not hardcode test IDs, source records, output ledgers, fixed node positions, or row order.
> Do not use hosted prediction APIs, runtime downloads, external datasets, pretrained checkpoints, or private or gated assets.
> Do not present predictions as diagnoses or simulations of an individual's subjective vision.
> Expected Output
> Write the completed submission CSV to the path supplied as the second command-line argument.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Paired-Site Multisensor Blackout Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx777ggjd5h928qpar01128by58c16wm
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.584

Full challenge description from page:

> Paired-Site Multisensor Blackout Reconstruction
> Overview
> This is a sequence-to-sequence reconstruction challenge. For each case, reconstruct three synchronized 24-step sensor trajectories missing from the middle of one monitoring site's half-day sequence. You receive a complete aligned sequence from a donor site, the recipient site's measurements outside the blackout, and every recipient support channel that remains available during the blackout.
> The data comes from paired precision-agriculture monitoring in Kolkata, India. A central logger outage can remove a related family of measurements at one site while another site and other sensor families continue operating. Your model must combine temporal continuity, cross-sensor relationships, and cross-site transfer. The target is a continuous 3 × 24 sequence, not a class label or a single regression value.
> Objective
> For every case_id, predict the recipient site's missing target-family values at ordered positions 12 through 35 inclusive. Flatten the 3 × 24 prediction in row-major order: all 24 values for the first target channel, then all 24 for the second, then all 24 for the third.
> Each stored half-day sequence has 48 ordered steps. In the original measurements, adjacent steps were 15 minutes apart. Absolute dates and site names are withheld.
> Public Files
> | Path | Description |
> |---|---|
> | train.npz | 166 training cases with observed tensors, masks, metadata tokens, and target sequences. |
> | test.npz | 56 held-out cases with the same inputs but no target array. |
> | channel_catalog.csv | Stable channel-index names and target-family membership. |
> | sample_submission.csv | Valid nonconstant submission with every test ID. |
> Load NumPy archives with np.load(path, allow_pickle=False).
> NPZ Arrays
> Shared input arrays
> | Array | Type and shape | Meaning |
> |---|---|---|
> | case_id | Unicode string, (N,) | Opaque submission key. It contains no date, site, split, or answer. |
> | observed | float32, (N, 2, 48, 11) | Robust-normalized sensor tensor in (case, site_role, step, channel) order. Site role 0 is the complete donor; role 1 is the recipient. |
> | observed_mask | uint8, same shape as observed | 1 means observed; 0 marks the recipient target-family blackout. Masked values in observed are exactly zero. |
> | target_group | uint8, (N,) | Target-family index 0, 1, or 2. |
> | period_band | uint8, (N,) | Anonymous within-day band 0 or 1. |
> | direction_token | uint8, (N,) | Anonymous donor/recipient direction 0 or 1. |
> train.npz additionally contains:
> | Array | Type and shape | Meaning |
> |---|---|---|
> | target | float32, (166, 3, 24) | Recipient ground-truth trajectories for steps 12 through 35, in target-group channel order. |
> test.npz has N = 56 and contains no target array.
> Channel Catalog and Target Groups
> | Index | Channel | Target group |
> |---:|---|---|
> | 0 | volumetric_moisture | 0 — calibration |
> | 1 | sensor_board_temperature | 1 — thermal/depth |
> | 2 | raw_capacitive_response | 0 — calibration |
> | 3 | sensor_supply_voltage | 0 — calibration |
> | 4 | atmospheric_pressure | support only |
> | 5 | atmospheric_temperature | support only |
> | 6 | soil_temperature | 1 — thermal/depth |
> | 7 | moisture_level_15cm | 1 — thermal/depth |
> | 8 | moisture_volume_15cm | 2 — hydraulic-volume |
> | 9 | aggregate_moisture | 2 — hydraulic-volume |
> | 10 | moisture_volume_percent | 2 — hydraulic-volume |
> Target-group channel order is fixed:
> Group 0: [0, 2, 3]
> Group 1: [1, 6, 7]
> Group 2: [8, 9, 10]
> All numeric values are dimensionless robust-normalized responses. Public observed values are lightly and deterministically perturbed to prevent exact-value fingerprints; training targets and private answers use the unperturbed normalized trajectories.
> Split Design
> The 222 cases come from 111 complete paired days with two non-overlapping half-day periods per day. Sixteen opaque calendar-week time blocks are the highest split unit. Their sizes are not uniform because the first and last calendar weeks are partial. The four selected held-out blocks contain 56 cases in total; the remaining twelve blocks contain 166 training cases. Every case from a block stays in one split. Only one donor-to-recipient direction exists for an interval, so a hidden recipient trajectory never appears as the donor input of a sibling row.
> Evaluation
> Submissions use the Paired-Site Blackout Reconstruction Score. Higher is better. The score range is [0.01, 1.0], and an exact submission scores 1.0.
> For each case, let Y and P be the true and predicted 3 × 24 arrays.
> MAE       = mean(abs(P - Y))
> DeltaMAE  = mean(abs(diff(P, time) - diff(Y, time)))
> LevelScore    = exp(-MAE / 0.65)
> DynamicsScore = exp(-DeltaMAE / 0.45)
> For each of the three channels, compute the Pearson correlation across 24 steps. A correlation is clipped to [0, 1]; a constant predicted or target channel receives zero for that channel. ShapeScore is the mean of the three clipped correlations.
> RawRowScore = 0.50 * LevelScore
> + 0.30 * DynamicsScore
> + 0.20 * ShapeScore
> RowScore = 0.01 + 0.99 * RawRowScore
> FinalScore = mean(RowScore over test cases)
> The metric rewards absolute reconstruction, step-to-step dynamics, and sequence shape. It is valid on any non-empty answer shard.
> Submission Format
> Write the final CSV to ./working/submission.csv with exactly these columns in this order:
> case_id,trajectory
> trajectory must be a JSON array string containing exactly 72 finite numeric values in [-8, 8], flattened in target-group row-major order. Include exactly one row for each of the 56 test IDs. IDs may appear in any row order, but duplicates, omissions, unknown IDs, malformed JSON, nulls, NaNs, infinities, out-of-range values, and extra user columns reject the submission. One backend-managed visibility column is accepted and ignored.
> Resource Rules
> The challenge is configured for CPU Default — 10 cores — 62.5 GiB RAM.
> The intended workflow is fully offline and uses only libraries already present in the Eris/Kaggle image.
> Do not call hosted APIs or use external datasets, source-record lookup, timestamp/site fingerprinting, hidden answers, submission feedback, or challenge-specific pretrained checkpoints.
> Do not use case_id, row order, filenames, archive order, or split artifacts as predictors.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Dialogue Schema Migration

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx797m0k7ztyrq9cb3t9khfbwh8agxdj
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top score: 0.916

Full challenge description from page:

> Dialogue Schema Migration
> Overview
> Conversational systems often replace one service API with another while retaining years of historical dialogue annotations. The two interfaces may encode the same fact under unrelated field identifiers, use different value representations, or omit a concept entirely.
> Your task is to migrate an ordered assistant semantic trace from a source API into a destination API. Each row provides protected dialogue evidence, the source trace, and natural-language definitions for both schemas. Produce the complete destination-native trace with provenance links back to every consumed source field.
> This is not dialogue-state tracking: the source trace is supplied. It is not response generation: the assistant reply is supplied. It is not plan repair: no trace is corrupted and no edit operation is requested. The required artifact is a new semantic trace under a different interface.
> The challenge is CPU-only. Training and inference must finish within 90 minutes on 10 CPU cores and 62 GB RAM.
> What Makes Migration Non-Trivial
> Public field identifiers are deterministic vendor-style codes such as field_19ac40e712; identifiers from different schemas do not reveal correspondence. Protected natural-language field definitions carry the semantic evidence. Definitions use controlled synonym replacement and sparse schema-local masking, so they preserve meaning without reproducing source schema cards verbatim.
> Gold migrations use four reviewed behaviors:
> Equivalent concepts migrate to the legal destination field even when the identifiers differ.
> A source fact with no compatible destination representation becomes unmapped.
> Equivalent APIs may encode a value differently. For example, a stop count can become a Boolean non-stop flag, and a ride-sharing Boolean can become a ride type.
> Adjacent identical destination assertions may coalesce into one item while retaining both source fields in source_slots.
> The mapping labels were built from reviewed domain-local concepts, not nearest-name similarity. The test set contains 12 complete schema pairs absent from training. More strongly, its five destination APIs and all of their field identifiers are absent from training in either source or destination role. Solvers must transfer from related APIs and field definitions rather than recover a test mapping table.
> Dataset
> train.csv: 19,784 labeled migration cases with columns id, dialogue, assistant_reply, source_schema, destination_schema, source_trace, and destination_trace.
> test.csv: 5,033 cases with columns id, dialogue, assistant_reply, source_schema, destination_schema, and source_trace. It omits the destination_trace target.
> sample_submission.csv: submission template with exactly two string columns, id and destination_trace. It contains every test id once and initializes destination_trace to the JSON array string []. Replace that placeholder with each predicted trace without changing the IDs or column order.
> All rows from one source dialogue remain on one side of the split. Train and test have zero source-dialogue overlap, zero schema-pair overlap, and zero overlap between test destination field identifiers and any training field identifier. IDs are opaque and row order has no meaning.
> Dataset contract version: dsm-v5-protected-schema-20260715. Valid IDs begin with dsm5_. The public files do not contain migration_examples. If those conditions or the stated row counts are not present, the dataset is a stale challenge version.
> Features
> id (string): opaque case identifier.
> dialogue (string): protected recent conversation context. Source values are replaced by stable within-row semantic placeholders, and sparse tokens are pseudonymized to prevent verbatim corpus lookup.
> assistant_reply (string): protected assistant response associated with the source trace.
> source_schema (JSON string): source service description and an array of legal fields, each with opaque name and natural-language description.
> destination_schema (JSON string): destination service description and its legal fields in the same format.
> source_trace (JSON string): ordered JSON array of source actions. Every item has act (string), slot (source field code string), and values (JSON array of strings).
> destination_trace (JSON string, train only): ordered JSON array containing the gold migrated actions. Every item has act (string), slot (legal destination field code or unmapped), values (JSON array of strings), and source_slots (non-empty JSON array of consumed source field codes).
> Placeholders such as VALUE_01, STOPS_ZERO, STOPS_POSITIVE, BOOL_TRUE, BOOL_FALSE, RIDE_SHARED, and RIDE_PRIVATE are part of the released protected representation. They are not raw source values.
> Output Grammar
> destination_trace must be a JSON array. Every item must contain exactly these keys:
> act: communicative action copied to the destination assertion.
> slot: a field code listed in that row's destination_schema, or unmapped.
> values: JSON array of strings in the destination representation.
> source_slots: non-empty JSON array of source field codes consumed by the item.
> Example:
> [{"act":"inform","slot":"field_19ac40e712","values":["VALUE_01"],"source_slots":["field_d2482a681f"]}]
> Unrepresentable example:
> [{"act":"inform","slot":"unmapped","values":["VALUE_01"],"source_slots":["field_d2482a681f"]}]
> Items retain communicative order. Each source action must be consumed exactly once, except that a coalesced item may list multiple consumed source fields. Do not invent field identifiers or values.
> Evaluation
> Important: the leaderboard score is baseline-normalized. It is not the raw weighted sum alone. The grader first computes the raw composite utility U, computes a single test-wide all-unmapped fallback utility B, and returns clip((U - B) / (1 - B), 0, 1).
> The grader validates JSON structure and destination-field legality for every row.
> Full migrated-item F1 (50%)
> Items are compared as multisets of the complete tuple:
> (act, destination slot, normalized values, source_slots)
> Precision and recall penalize extra and missing assertions. Their harmonic mean is the item F1. Acts and values are lowercased and whitespace-collapsed; field identifiers remain exact.
> Provenance alignment F1 (15%)
> The tuples (destination slot, source_slots) are compared as multisets with precision, recall, and F1. This rewards correct schema correspondence only when it is attached to the correct source provenance.
> Exact trace rate (35%)
> The complete normalized JSON trace must match, including item order, values, and provenance. JSON object key order does not matter; array order does.
> The three components first form raw migration utility:
> U = 0.50 * full_item_F1 + 0.15 * provenance_alignment_F1 + 0.35 * exact_trace_rate
> The grader also evaluates the no-migration fallback on the same rows. That fallback preserves every source act and value but emits every source item as unmapped with its original source field in source_slots. Let its test-wide raw utility be B. This is one aggregate constant computed from the private gold traces; it does not depend on a participant's submission.
> Final migration skill lift:
> max(0, min(1, (U - B) / (1 - B)))
> This chance-style adjustment removes credit available from declaring every fact unmapped. Scores at or below the fallback are reported as 0; perfect migrations score exactly 1.0. Since B is fixed test-wide, the transformation is monotonic above the fallback but changes the reported score scale.
> The final score is finite and clipped to [0, 1]; higher is better. Malformed JSON, wrong item keys or types, an illegal destination field, an empty source_slots list, or failure to consume every source action exactly once receives zero raw utility for that row. Consumption is checked as a multiset of source-field occurrences, so partial traces, duplicated provenance, and invented source fields are invalid. Wrong CSV columns, duplicate IDs, missing IDs, extra IDs, stale ID prefixes, or a stale private-answer contract reject the submission.
> Why Standard SGD Recipes Are Insufficient
> A dialogue-state tracker predicts facts under one supplied schema; it does not translate an already-recorded trace between non-isomorphic interfaces.
> SGD-X tests paraphrases of an equivalent schema; this task changes the field inventory and value representation while preserving provenance.
> Ontology matching predicts correspondences but does not emit ordered, value-grounded dialogue actions or explicit unmapped facts.
> Response generation verbalizes a semantic input; this task transforms one structured semantic representation into another.
> A complete solver needs schema-semantic transfer, unseen-API generalization, value conversion, provenance-aware coverage, and constrained structured decoding.
> Submission Format
> Submit a CSV with exactly these columns, in this order:
> id,destination_trace
> There must be exactly one row for each test ID. Use a CSV library because JSON strings contain commas and quotes.
> Correctly formatted example (illustrative IDs and fields only):
> id,destination_trace
> dsm5_example_001,"[{""act"":""inform"",""slot"":""field_19ac40e712"",""values"":[""VALUE_01""],""source_slots"":[""field_d2482a681f""]}]"
> dsm5_example_002,"[{""act"":""inform"",""slot"":""unmapped"",""values"":[""VALUE_02""],""source_slots"":[""field_a102b3c4d5""]}]"
> In the real submission, replace the illustrative IDs with every id from test.csv and use only destination fields legal for that row.
> Requirements and Prohibited Methods
> Use CPU computation only and stay within the 90-minute limit.
> Learn from train.csv; test destination APIs must be treated as unseen schema inputs.
> Do not use GPUs, hosted inference services, external model APIs, hidden labels, or private files.
> Do not search protected dialogue strings or reverse-map cases to the public source corpus.
> Do not exploit IDs, row order, file hashes, or external hand-authored mappings for the hidden APIs.
> Do not fit vectorizers, thresholds, schema mappings, or model parameters on the unlabeled test rows.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Idle Motion Direction Forecasting

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7352zb9kq8y5kjcht493y9b98axah1
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top score: 0.334

Full challenge description from page:

> Idle Motion Direction Forecasting
> The Problem
> A character standing idle is never perfectly still. It sways, shifts its weight, drifts, and settles, in small involuntary movements. Given a moment of that motion, what happens next? Not a copy of a target pose supplied in advance, but the motion the body is about to produce on its own. Predicting continuation is different from filling a gap between two known keyframes: there is no future anchor to aim at, so the only way to know where the motion is going is to read where it has been.
> This challenge asks a model to write out that continuation as a symbolic score. Given a context window of recent idle motion, generate the sequence of motion-direction tokens for the frames that follow. The model sees the recent per-frame motion and produces, in order, one token per future frame naming how the body moves at that moment: whether it is still, and if not, which part of the body leads the movement and whether that movement is building or fading.
> This is a sequence generation task grounded in motion dynamics. The input is a motion sequence and the output is a token sequence conditioned on it. The model must read the rhythm of the recent movement, extrapolate the momentum forward, and emit a direction token for each future frame. Natural approaches are temporal neural networks: a recurrent or temporal-convolutional or transformer encoder over the context that decodes a token per future step, or any sequence-to-sequence model that maps the motion context to the future token stream. It is generation of what comes next, not interpolation toward a given end.
> What makes this challenge distinct
> There is no target to interpolate toward. In gap-filling tasks a future keyframe is provided and a straight-line blend between the endpoints is a strong baseline. Here the future is withheld entirely. Nothing can be interpolated, because there is no endpoint. The continuation has to be generated from the context alone, which removes the closed-form shortcut and leaves only the modelling of motion dynamics.
> Predicting motion, not stillness. The tokens describe movement, derived from how the pose changes frame to frame. The lazy forecast, that nothing will move, maps to predicting the still token for every future frame. That forecast fails, because idle bodies do move, and the moving tokens make up more than half of all frames. Recovering when and how the body moves next is the whole task.
> Direction, not exact pose. The output is a symbolic description of motion, not a reconstruction of exact joint angles. This isolates the question of where the motion is heading from the question of precise numerical pose. The model commits to a direction of movement per frame and is judged on getting that right across the horizon.
> Person-disjoint split. The ten test subjects never appear in training. Idle style is personal, so the model cannot memorise how one individual drifts. It must learn the general dynamics of how idle motion continues and apply them to people it has never seen.
> Data
> The motion is human idle motion capture at 30 frames per second, using a 22-joint skeleton. This challenge works in velocity space: the input is the frame-to-frame change of the joint rotations, 66 channels per frame, with root translation excluded so absolute placement cannot leak.
> Each case is one row. The features are the CTX context frames of velocity, flattened frame by frame then channel by channel: the first 66 values are context frame 0, the next 66 are frame 1, and so on for all 45 context frames. The label is the sequence of 30 direction tokens for the frames that follow the context.
> The five direction tokens:
> Token   Meaning
> ------- --------------------------------------------------
> STILL   the body is essentially still at that frame
> UP_A    upper body leads the motion and the motion is building
> UP_B    upper body leads the motion and the motion is fading
> LO_A    lower body leads the motion and the motion is building
> LO_B    lower body leads the motion and the motion is fading
> In the CSV the tokens are encoded as integers: STILL is 0, UP_A is 1, UP_B is 2, LO_A is 3, LO_B is 4.
> train.csv columns:
> Column      Type    Description
> ----------- ------- --------------------------------------------------
> id          str     Opaque case identifier
> v{t}_c{c}   float   Context velocity, frame t (0 to 44), channel c (0 to 65)
> y{t}        int     Direction token for future frame t (0 to 29); label
> test.csv columns:
> Column      Type    Description
> ----------- ------- --------------------------------------------------
> id          str     Opaque case identifier
> v{t}_c{c}   float   Context velocity, frame t (0 to 44), channel c (0 to 65)
> The y columns are withheld in the test set. The reference future tokens for the test cases are held privately.
> Dataset facts:
> Quantity              Value
> --------------------- --------------------------------------------------
> Source                human idle motion capture, velocity space
> Context length        45 frames (1.5 seconds at 30 fps)
> Forecast horizon      30 frames (1 second), 30 output tokens
> Channels per frame    66 joint rotation velocity channels
> Feature width         2,970 values per case (45 frames x 66 channels)
> Vocabulary            5 direction tokens
> Training cases        3,956
> Test cases            1,006
> Split                 person-disjoint; the 10 test subjects are unseen
> Evaluation
> Each predicted token sequence is aligned to the reference by position: the first token describes the first future frame, and so on. Grading compares the tokens at every future position and computes a macro-averaged F1 across the five direction tokens. For each token, precision, recall, and F1 are computed treating that token as the positive class, and the five F1 scores are averaged with equal weight.
> for each token in {STILL, UP_A, UP_B, LO_A, LO_B}:
> precision = correct predictions of this token / all predictions of this token
> recall    = correct predictions of this token / all reference positions of this token
> f1        = 2 * precision * recall / (precision + recall)
> score = mean(f1 over the five tokens)
> Macro averaging means every token matters equally regardless of how many frames carry it, so recovering the moving tokens is as important as the common STILL token. A predicted value that is missing, out of range, or not one of the five valid tokens counts as incorrect at that position. Higher is better, in the range 0 to 1.
> For calibration under this exact metric:
> Strategy                                          Macro-F1
> ------------------------------------------------- --------
> Predict STILL for every future frame              about 0.12
> Random tokens of the correct length               about 0.18
> The still-everywhere baseline near 0.12 is the key number. It is the forecast that nothing moves, and it scores zero on the four moving tokens that make up more than half of all frames. Beating it requires reading the context dynamics and generating where the motion is heading, which is what a temporal model learns and a constant or random guess cannot.
> Compute budget
> Your solution must train and produce its submission within the following limits:
> Resource   Limit
> ---------- --------------------------------------------------
> CPU        10 cores
> RAM        62.5 GB
> Runtime    90 minutes, end to end (training plus inference)
> GPU        none
> The task is designed to fit comfortably on CPU. Each case is a short sequence and the dataset is modest, so a compact sequence-to-sequence model trains in minutes, not the full budget.
> Submission
> Submit a CSV with one row per test case. The sample_submission.csv file lists every test id with a full-length placeholder sequence, so it is a valid submission out of the box and shows the exact format the grader expects.
> Column      Type    Description
> ----------- ------- --------------------------------------------------
> id          str     Case id from test.csv
> y{t}        int     Predicted direction token for future frame t (0 to 29)
> Include the header row and one prediction per test id, with all 30 token columns y0 through y29. Each token is an integer from 0 to 4. Rows may appear in any order, since they are joined to the answers on the id column. A submission missing any required test id, or missing any of the 30 token columns, is rejected. A token that is missing or outside the range 0 to 4 counts as incorrect at that position.
> Constraints
> Allowed. Any HuggingFace model or from-scratch architecture trained on the provided training data only. Recurrent networks, temporal convolutional networks, transformers, and encoder-decoder sequence-to-sequence models are all suitable. You may transform the velocity features, normalise the channels, address the token imbalance with weighting or resampling, cross-validate on the training cases, and ensemble your own trained models.
> Model required. The continuation must be generated by a model that reads the context and produces the future token sequence. Emitting a constant token, or any fixed rule that does not read the context dynamics, is not a valid solution: the still-everywhere forecast is the floor the task is defined against.
> No external data of any kind. No other motion capture datasets, no idle animation corpora, and no external motion priors or pretrained motion models. The forecast must come from your own model trained on the provided data. Do not attempt to identify or recover the source recordings in order to look up the hidden tokens from any external source.
> No hosted or closed model APIs. A submission has to be reproducible from your own trained model. Do not call external services, network APIs, or remote models at inference time.
> Compute. The solution must respect the compute budget above: 10 CPU cores, 62.5 GB RAM, no GPU, and a 90 minute end-to-end runtime covering both training and inference.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Counterstep: Contact Change-Log Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7axybkdm57sz2p7cbwg7x1ds8bq5xd
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, generative, small-data, feature-engineering, medical, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 63.302

Full challenge description from page:

> Counterstep: Contact Change-Log Reconstruction
> Overview
> Each row is a lossy symbolic record of a repeated human movement. You can observe coarse pelvis and lower-back pose symbols and their position-to-position changes, but all measurements below the hips are withheld. Your task is to reconstruct the sparse change log of the hidden ground-contact process. Each submitted string must state the initial contact mode, every later mode change, the exact position where each change starts, and a final sequence-length marker.
> This differs from predicting a label at every position: unchanged spans are omitted from the output, so a valid answer is a variable-length program of change records. Recovering such a log can support motion restoration and sensor-dropout auditing when lower-body measurements are missing. The truth is derived deterministically from synchronized heel trajectories, while only the visible trunk observations are coarsened or made unavailable. Source participants are separated across train and test. A useful first approach is to fuse pose and change evidence across neighboring positions, infer the hidden contact process, and compress only its state changes into the required log.
> Change-Log Grammar
> Each change record contains a two-letter mode followed immediately by a two-digit position:
> LU00 - left-only contact starts at position 00 while the ungrounded heel is rising.
> LD14 - left-only contact starts at position 14 while the ungrounded heel is descending.
> RU23 - right-only contact starts at position 23 while the ungrounded heel is rising.
> RD31 - right-only contact starts at position 31 while the ungrounded heel is descending.
> DB38 - bilateral contact starts at position 38.
> Z40, Z48, or Z56 - required final record giving the observed sequence length.
> The first contact record must start at 00. Later positions must be strictly increasing and smaller than the final length. Adjacent records must use different modes. A valid log contains 2 through 16 space-separated records in total, including its final Z record.
> The visible strings use this grammar:
> pose_stream - one space-separated symbol per observed position. Each symbol has six dot-separated components. A0 through A9 are coarse pose bins and A_ is unavailable.
> velocity_stream - one space-separated symbol per observed position. Each symbol has six dot-separated components. V0 through V9 are coarse change bins and V_ is unavailable.
> display_code - D0 or D1, a deliberately balanced nuisance code with no relationship to the hidden contact log.
> Both visible streams in a row have the same length: 40, 48, or 56 positions.
> Evaluation Metric
> The Counterstep Change-Log Score ranges from 0 to 100 and is maximized. Let the five contact modes be C = {LU, LD, RU, RD, DB}.
> For each mode c, a predicted change record is a true positive only when an unused true record has the same mode and exact position. Let TP_c, FP_c, and FN_c be the aggregate counts over the test set. Then F1_c = 2 × TP_c / (2 × TP_c + FP_c + FN_c), with F1_c = 0 when the denominator is zero, and F = (1 / 5) × Σ_(c in C) F1_c.
> For timing credit, each true change record is paired with the nearest unused predicted record of the same mode. If their positions are t and p, its value is s = exp(−|p − t| / 2). A true record with no available prediction of the same mode receives zero. T is the mean of s over every true change record in the test set. Extra predictions are penalized through F.
> For each row, let a be the predicted mode sequence and b the true mode sequence after removing positions and the final Z record. Let LCS(a, b) be their longest-common-subsequence length. The row value is o = LCS(a, b) / max(|a|, |b|, 1). O is the mean of o over all 600 rows.
> The final score is Score = 100 × clip(0.45 × F + 0.35 × T + 0.20 × O, 0, 1).
> A malformed log or final Z length that disagrees with the visible sequence length receives zero on all three terms for that row. Invalid output cannot create an abstention advantage.
> The theoretical minimum is 0. A score of 100 requires exact reconstruction of every valid change log. Reproduced public-data references on the shipped files are: valid constant 8.544532, position template 19.196567, framewise conditional model 49.817729, contextual gradient-boosted model 53.816620, continuity-aware decoder 55.078241, and contextual BiGRU 57.736934. These are achievable baselines, not estimates of the theoretical ceiling.
> Dataset
> train.csv
> Contains 1,800 labeled symbolic sequences.
> id - integer - fresh row identifier from 0 through 1,799.
> pose_stream - string - lossy six-component pose symbols at 40, 48, or 56 ordered positions.
> velocity_stream - string - lossy six-component change symbols at the same positions.
> display_code - string - balanced nuisance code D0 or D1.
> contact_log - string - variable-length target containing contact-mode changes and a final length record.
> test.csv
> Contains 600 query sequences with IDs 1,800 through 2,399. Its columns are id, pose_stream, velocity_stream, and display_code. It never contains contact_log.
> sample_submission.csv
> Contains all 600 test IDs and a syntactically valid constant log with the correct final length for each row.
> Submission
> Submit a CSV with a header and exactly 600 rows. Columns and order must be exactly:
> id - integer - one unique test identifier.
> contact_log - string - 2 through 16 legal space-separated records, ending in Z40, Z48, or Z56 to match the row's visible length.
> Duplicate, missing, unknown, or extra IDs are rejected. Extra or reordered columns are rejected. Row order is irrelevant. Empty, malformed, repeated-mode, non-increasing, and out-of-range logs receive worst-case row credit without crashing the grader.
> Example using real test IDs:
> id,contact_log
> 1800,LU00 Z56
> 1801,RU00 RD18 DB36 Z56
> 1802,RD00 DB17 LU29 Z40
> What Not to Use
> TF-IDF and other bag-of-words methods are prohibited because they discard ordered positions and change timing.
> A majority-mode log cannot locate real contact changes.
> Independent symbol lookup misses the coupled pose, velocity, and continuity clues.
> Emitting one label per visible position violates the sparse submission grammar.
> display_code is balanced within every length and split and has no causal relationship to the target.
> Source lookup cannot recover answers because participant labels, trial names, original measurements, and absolute source positions are absent from public files.
> Expected approaches fuse both visible symbol streams contextually, decode a coherent hidden process, and emit only its ordered changes.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Recall Bulletin Structure Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70eve39es967h5cxf6b1zg9x8aqpqx
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.487

Full challenge description from page:

> Recall Bulletin Structure Reconstruction
> Overview
> Public-safety recall bulletins contain four editorial sections: product description, hazard explanation, reported incidents, and consumer remedy. During document migration, the section headers and opening sentence can survive while later paragraphs become detached and shuffled. Restoring those continuations requires linking references across fragments and recovering native discourse transitions.
> Each row supplies the transformed headline, the labeled first native sentence of each section, and 5 to 18 shuffled continuation cards. Predict which anchor each continuation belongs after and restore the exact native successor chain inside every section.
> The target comes directly from the expert-published bulletin fields and sentence order. Preparation does not generate prose, section labels, or order labels.
> Task
> For each case_id, output four ordered continuation lists:
> {"description":["CARD_2","CARD_5"],"hazard":[],"incidents":["CARD_6"],"remedy":["CARD_3","CARD_4"]}
> Every displayed card must appear exactly once. A list may be empty when its labeled anchor has no detached continuation.
> Dataset
> public/train.csv contains 750 unique bulletin cases with reconstruction targets.
> public/test.csv contains 329 unique held-out bulletin cases without targets.
> public/sample_submission.csv demonstrates valid JSON and card conservation.
> private/answers.csv contains hidden native continuation membership and order for grading only and is not available to solvers.
> Columns
> case_id string): opaque bulletin identifier.
> context_packet string): transformed headline and product context.
> section_anchor_packet string): the transformed first native sentence for each labeled section, shown as DESCRIPTION_ANCHOR, HAZARD_ANCHOR, INCIDENTS_ANCHOR, and REMEDY_ANCHOR.
> card_packet string): shuffled detached continuation fragments labeled CARD_#. Card numbering is random and carries no section or order information.
> card_count integer): number of continuation cards, from 5 through 18.
> reconstruction_json JSON string, train only): ordered native continuation lists for the four sections.
> Content-bearing words, product identifiers, names, numbers, contacts, and URLs receive row-local lexical aliases. The same source token repeats consistently inside one bulletin but its alias does not transfer to another row. A small set of grammatical function words and punctuation remains readable. This preserves within-document reference and discourse evidence while preventing a global section vocabulary from identifying the answer.
> Exact duplicate source records are removed before case construction. Rows sharing a native source-bulletin group are always kept together. Every eligible source group from 2018 onward is hidden for testing, and a deterministic 13% sample of older source groups is added to the hidden partition to reduce evaluation noise. The partitions share no source group, case ID, or complete transformed packet. Every case ID is derived from the full source record rather than from a potentially repeated bulletin number, and uniqueness is asserted during preparation.
> Evaluation
> Scores range from 0 to 1 and higher is better.
> CardSectionAccuracy is the fraction of cards assigned to the correct native section. It is chance-corrected against uniform four-section assignment:
> SectionSkill = max(0, (CardSectionAccuracy - 0.25) / 0.75)
> NativeSuccessorAccuracy compares directed native continuation links. Each non-empty list contributes one link from its labeled SECTION_START anchor to its first card and one link for every consecutive card pair. It is the fraction of hidden links reproduced exactly.
> ExactReconstruction is 1 only when all four ordered lists exactly match; otherwise it is 0.
> Score = 0.30 * mean(SectionSkill)
> + 0.50 * mean(NativeSuccessorAccuracy)
> + 0.20 * mean(ExactReconstruction)
> A completely incorrect reconstruction scores 0; the exact native reconstruction scores 1.
> Submission Format
> Submit a UTF-8 CSV with exactly these columns:
> case_id,reconstruction_json
> RBR_0123456789abcdef,"{""description"":[""CARD_2""],""hazard"":[],""incidents"":[""CARD_1""],""remedy"":[""CARD_3""]}"
> Requirements:
> Include every test case_id exactly once, with no missing, duplicate, or unknown IDs.
> Use exactly the keys description, hazard, incidents, and remedy.
> Each value must be an ordered JSON list; empty lists are valid.
> Use every card from that row exactly once and do not add cards.
> Write the CSV to the exact output path supplied by the platform.
> Allowed
> CPU-only pairwise discourse models, anchor-conditioned encoders, structured decoders, compact neural models, and ensembles trained using the public files.
> Joint use of the context, all four section anchors, and all continuation cards.
> At most 10 CPU cores, 62 GB RAM, and 1.5 hours end-to-end.
> Prohibited
> No GPU or accelerator computation.
> No external recall archive, source-page lookup, web search, cached markup, hosted inference API, or closed external model service.
> Do not reconstruct original recall identifiers, products, companies, URLs, dates, or source records.
> Do not use private answers, grader internals, test IDs, row order, filenames, hashes, or hard-coded test reconstructions.
> This benchmark is for research evaluation and does not replace official recall notices or consumer-safety instructions.

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## DataSeek: Research Catalog Interaction Trail Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71sc3kz4hjzkpz1cj79pjqbd8c6qkn
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, small-data, feature-engineering, generative, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 8.576

Full challenge description from page:

> Overview
>
> Each row is one real search session in a research-data catalog. A user issued one to four queries, received ranked result cards, and then viewed, previewed, or opened some records. Your task is to reconstruct that ordered interaction trail.
>
> The input has three synchronized text views. query_view lists the user's ordered query states. candidate_view contains shuffled, session-local result cards with title fragments, subjects, and the query ranks at which each card appeared. flow_view lists the ordered interactions with route type, a complementary title fragment, record kind, and a coarse time bucket. Candidate aliases such as c03 are deliberately local to one row.
>
> Predict one variable-length program. Every operation has the form ACTION:QUERY:CANDIDATE. V means a detail view, P means an in-page preview, and O means an outbound open. q0 through q3 identify query states in chronological order; c00 through c59 identify shuffled candidate cards. For example, V:q0:c04 O:q1:c04 says that the same card was first viewed from query 0 and later opened from query 1.
>
> Targets are deterministic transformations of genuine logged interactions. No label is randomized or flipped. The challenge comes from joining disjoint title fragments, query semantics, subjects, ranks, timing, and repeated-event memory while preserving event order. Use only the supplied files. External data, source lookup, pretrained models, and pretrained embeddings are not allowed.
>
> Evaluation Metric
>
> A program is split on single spaces. Every token must match ACTION:QUERY:CANDIDATE exactly:
>
> ACTION is V, P, or O.
>
> QUERY is q0, q1, q2, or q3.
>
> CANDIDATE is c00 through c59; submitted aliases that do not occur in that row receive no useful match credit.
>
> A program must contain 2 through 32 operations. There is no NOOP form because every scored session contains at least two real interactions.
>
> Tokens are parsed left to right into (action, query, candidate) tuples. For row 
> 𝑖
> i, let the true sequence be 
> 𝑌
> 𝑖
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
> Y
> i
> 	​
>
> =(y
> 1
> 	​
>
> ,…,y
> m
> 	​
>
> ) and the prediction be 
> 𝑃
> 𝑖
> =
> (
> 𝑝
> 1
> ,
> …
> ,
> 𝑝
> 𝑛
> )
> P
> i
> 	​
>
> =(p
> 1
> 	​
>
> ,…,p
> n
> 	​
>
> ).
>
> Exact-trail recovery is 
> 𝑄
> 𝑖
> =
> 1
> Q
> i
> 	​
>
> =1 when 
> 𝑌
> 𝑖
> =
> 𝑃
> 𝑖
> Y
> i
> 	​
>
> =P
> i
> 	​
>
>  as ordered sequences and 
> 𝑄
> 𝑖
> =
> 0
> Q
> i
> 	​
>
> =0 otherwise.
>
> Ordered similarity 
> 𝐷
> 𝑖
> D
> i
> 	​
>
>  is one minus a weighted Levenshtein distance divided by 
> max
> ⁡
> (
> 𝑚
> ,
> 𝑛
> ,
> 1
> )
> max(m,n,1). Insertions and deletions cost 1. An exact substitution costs 0. A substitution costs 0.35 when action and candidate match but query differs, 0.55 when query and candidate match but action differs, 0.75 when only candidate matches, and 1 otherwise. The result is clipped below at 0.
>
> Exact-operation recovery 
> 𝐸
> 𝑖
> E
> i
> 	​
>
>  is multiset F1 over complete tuples. If 
> 𝐼
> 𝑖
> I
> i
> 	​
>
>  is the multiplicity-counted intersection, then 
> 𝐸
> 𝑖
> =
> 2
> ∣
> 𝐼
> 𝑖
> ∣
> /
> (
> 𝑚
> +
> 𝑛
> )
> E
> i
> 	​
>
> =2∣I
> i
> 	​
>
> ∣/(m+n). Link recovery 
> 𝐿
> 𝑖
> L
> i
> 	​
>
>  uses the same multiset F1 after each tuple is reduced to (query, candidate).
>
> The final score is:
>
> 100
> ×
> clip
> ⁡
> (
> 1
> 𝑁
> ∑
> 𝑖
> [
> 0.45
> 𝑄
> 𝑖
> +
> 0.25
> 𝐷
> 𝑖
> +
> 0.20
> 𝐸
> 𝑖
> +
> 0.10
> 𝐿
> 𝑖
> ]
> ,
> 0
> ,
> 1
> )
> .
> 100×clip(
> N
> 1
> 	​
>
> i
> ∑
> 	​
>
> [0.45Q
> i
> 	​
>
> +0.25D
> i
> 	​
>
> +0.20E
> i
> 	​
>
> +0.10L
> i
> 	​
>
> ],0,1).
>
> A malformed program, missing value, NaN, infinity, invalid character, or program longer than 32 operations receives zero on all four terms for that row. Invalid predictions do not create an abstention advantage. A score of 100 requires every action, query link, candidate, and sequence position to be exact.
>
> Measured references on the frozen 394-row holdout and this exact grader are: constant sample 1.46, literal lexical alignment 6.80, rank-one reconstruction 25.74, fragment-length heuristic 34.66, from-scratch pairwise logistic decoder 40.36, and perfect 100.00.
>
> Dataset
>
> Participant files:
>
> train.csv contains 500 labeled sessions.
>
> test.csv contains 394 unlabeled sessions.
>
> sample_submission.csv contains all 394 test identifiers with valid placeholder programs.
>
> Columns in train.csv:
>
> sample_id - string - opaque row identifier, such as s000be7e6c3b2.
>
> trail_lane - string - balanced nuisance value l0 or l1.
>
> query_count - integer - number of chronological query states, from 1 through 4.
>
> session_span - string - coarse elapsed-time band: short, medium, or long.
>
> query_view - string - ordered query cards separated by || . Example: q0@t0|text=cancer|class=collection|advanced=0|spatial=0|years=none-none || q1@t3|text=skin~cancer|class=collection|advanced=0|spatial=0|years=none-none.
>
> candidate_view - string - shuffled result cards separated by || . Example: c03|title=victoria~survey|subjects=cancer~health|seen=q0r01,q1r04 means candidate c03 appeared at rank 1 for query 0 and rank 4 for query 1.
>
> flow_view - string - chronological interaction breadcrumbs separated by || . Example: e0@t1|route=detail|hint=cancer~registry|kind=collection || e1@t3|route=outbound|hint=registry|kind=collection.
>
> trail_program - string - ordered target, such as V:q0:c03 O:q1:c03.
>
> test.csv has the same seven query columns and never contains trail_program. In the compact views, ~ joins words inside one field, t0 through t4 are increasing coarse time buckets, r01 is rank 1, none is a genuine missing field, and query/candidate/event cards use qN, cNN, and eN aliases respectively.
>
> For every interacted record, the candidate title fragment and flow hint are deterministic, order-preserving subsets drawn from disjoint source-token positions in the same title; together they retain every title token used by the task. A repeated word can therefore occur in both fragments when it occupied different source positions. Single-token titles are shown in both views. This makes every target recoverable from supplied evidence without exposing a direct record identifier.
>
> The split is disjoint by query-theme group. A source record interacted with in test never appears anywhere in a training candidate set. Exact and high-similarity query sequences are filtered from train, while every action class remains represented on both sides.
>
> Submission
>
> Submit exactly 394 data rows plus a header. Columns must be exactly:
>
> sample_id - string - one identifier copied from test.csv.
>
> trail_program - string - one valid non-empty program using the grammar above.
>
> A correctly formatted excerpt using real test IDs is:
>
>
> sample_id,trail_program
>
> s002874fc3de4,V:q0:c02 O:q3:c02
>
> s00535078bf92,P:q0:c07 V:q0:c11
>
>
> These predictions are illustrative, not disclosed answers. Row order does not affect scoring. Duplicate, missing, or unknown IDs, an incorrect row count, and extra or reordered columns are rejected cleanly.
>
> What Not to Use
>
> The valid two-operation placeholder V:q0:c00 V:q0:c00 scores only 1.46.
>
> Literal title-token overlap scores 6.80 because paired title fragments are disjoint by construction.
>
> Always choosing the top-ranked result reaches only 25.74.
>
> Fragment length and rank reach 34.66 but cannot resolve semantically similar candidates or query refinements.
>
> trail_lane is exactly balanced inside every output-length and leading-action stratum.
>
> Candidate position is hash-shuffled independently within each session, and aliases have no cross-row meaning.
>
> Source session IDs and source record IDs are absent from participant files.
>
> The intended CPU route is to parse all three views, learn pairwise event-to-candidate compatibility from train, use query and subject context to join complementary fragments, maintain candidate identity across repeated events, infer the latest compatible query state, and decode the complete trail in flow order.
>
>  
>
> Submissions
> 2
> Top Score
> 8.576
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

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Sign Language Routing Signature Prediction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75j0191scxhc833q8f5tn84x8c81gr
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top score: —

Full challenge description from page:

> Cross-Signer Early-Routing Utility
> Overview
>
> You are given a variable-length sequence of 3-D hand landmark coordinates from an assistive sign-language interface. Predict a compact three-symbol routing signature for each sequence: the first two alphabetic symbols plus a length cue S for 2–5 symbols, M for 6–10, or L for 11 or more). This signature can route an early partial caption to a small autocomplete candidate set before a complete caption is available. A useful system should recognize hand shape and movement patterns that carry across people, rather than memorizing a person or capture setup.
>
> The inputs are already compact numeric landmarks. Each public sequence exposes only the first 60% of the real compact sequence, with later frames withheld; this makes the routing decision genuinely early rather than a full-sequence transcription proxy. Each exposed prefix has up to 64 time steps, with 21 hand landmarks and three coordinates per landmark. The coordinate system is wrist-relative and scale-normalized. The test distribution contains people not represented in the labeled training rows, so validation should measure person-independent routing.
>
> Dataset
> File descriptions
>
> train.csv -- 2,401 labeled training rows. It contains one hashed sequence ID and its three-symbol routing signature target.
>
> test.csv -- 600 unlabeled test rows. It contains one hashed sequence ID per sequence.
>
> train_features.npy -- A float32 array with shape (2401, 64, 63). The first dimension follows train.csv; each row is a padded or resampled sequence.
>
> test_features.npy -- A float32 array with shape (600, 64, 63). The first dimension follows test.csv.
>
> train_lengths.npy -- 2,401 integer observed-frame counts for train_features.npy.
>
> test_lengths.npy -- 600 integer observed-frame counts for test_features.npy.
>
> sample_submission.csv -- A valid-format example with non-empty random routing signatures.
>
> Column descriptions
>
> id (string) -- A unique 12-character hexadecimal sequence identifier. The same ID appears in the corresponding feature-array row.
>
> target (string, train.csv only) -- A three-symbol routing signature: the first two alphabetic symbols of the underlying fingerspelling followed by S, M, or L for the underlying phrase-length bucket. Whitespace is ignored by the grader.
>
> The feature arrays use the following fixed order for each frame:
>
> 21 landmarks, each with x, y, and z coordinates, flattened to 63 float32 values.
>
> Rows after the observed length are padding and must be ignored using the matching length array. Only the observed prefix is present; later source frames cannot be recovered from the public arrays.
>
> Evaluation
>
> Submissions are scored with Signer-Balanced Early-Routing Utility, a maximize metric in [0, 1]. Text is Unicode-normalized, uppercased, and reduced to alphabetic characters before scoring. A normalized prediction must contain exactly three letters and end in S, M, or L; malformed rows are rejected before scoring.
>
> For a predicted signature p and reference signature r, define:
>
>
> edit_similarity = 1 - levenshtein(p, r) / max(len(p), len(r), 1)
>
> row_utility = 0.75  *max(edit_similarity, 0) + 0.25*  float(p == r)
>
> score = mean(mean(row_utility for rows in group) for group in test_groups)
>
>
> The final mean is over hidden capture-person groups, so a frequent person cannot dominate the score. Partial credit reflects useful routing overlap, while the exact-match component rewards a complete prefix-and-length cue. All valid predictions have the same three-symbol length, so the edit component measures prefix and bucket substitutions rather than rewarding padding.
>
> Submission
>
> Submit a CSV file with exactly one prediction for every row in test.csv.
>
> id (string) -- The 12-character hexadecimal ID copied from test.csv.
>
> target (string) -- Your predicted non-NaN three-symbol routing signature.
>
> Example:
>
>
> id,target
>
> bf464dc74ada,GSM
>
> af432af29daa,MEL
>
> Requirements
>
> The file must contain exactly 600 data rows, one for every row in test.csv.
>
> Every test ID must appear exactly once; do not add or remove IDs.
>
> The column names must be exactly id,target and the file must be UTF-8 CSV.
>
> Predictions must be strings and must not be NaN. After normalization, every prediction must contain exactly three alphabetic symbols, with S, M, or L as the final symbol. Empty and arbitrary-length predictions are invalid.
>
> Use the matching feature-array row and observed-frame count for each test ID.
>
> Allowed methods
>
> Train any local machine-learning model using the public training rows and public feature arrays.
>
> Use sequence models, temporal pooling, learned alignments, augmentation of training inputs, and standard CPU-compatible scientific Python libraries.
>
> Use public training labels for model selection, but keep test inputs out of training and target tuning.
>
> What Not To Use
>
> Do not reverse-map hashed IDs to an external labeled archive or signature list; that bypasses the intended landmark-to-routing learning problem.
>
> Do not match a public feature row to an outside copy with known annotations or cached predictions; the score is intended to measure a trained model's generalization to unseen people.
>
> Do not recover targets from row order, file order, array padding, or ID hash patterns. These are identifiers and storage details, not supervision.
>
> Do not replace learned routing-signature prediction with a manually keyed handshape-to-signature lookup table or hard-coded answer list.
>
>  
>
> Submissions
> 0
> Top Score
> —
> Created
> Aug 11, 2026
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

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Context-Aligned Token Role Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx782c0vf1zczpd50atdv7g0v58c443z
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.744

Full challenge description from page:

> Overview
>
> Recover both word boundaries and a token-level syntactic role sequence from a whitespace-free sentence. The input is a real sentence with formatting boundaries removed. Training rows provide the reviewed segmentation and one role tag for every resulting token; test rows provide only the character sequence.
>
> This is a joint normalization task for downstream search, translation, and syntax-aware text processing. A boundary is useful only when its attached role is aligned to the same character span. The evaluation therefore scores boundary placement and (character_end, role) events together instead of treating POS tagging as an independent text-classification problem.
>
> The hidden test is a fixed generalization holdout rather than a purely iid random sample. It includes reserved corpus material and lower-frequency lexical combinations, so validation should measure transfer to new sentence content instead of memorisation of repeated full tokens.
>
> Dataset
> train.csv
>
> id (str) -- Opaque row identifier.
>
> text (str) -- Whitespace-free input sentence. Preserve all characters and their order.
>
> segmentation (str) -- Reviewed sentence with whitespace marking token boundaries.
>
> pos_tags (str) -- Space-delimited role labels in one-to-one order with segmentation.split().
>
> test.csv
>
> id (str) -- Opaque row identifier.
>
> text (str) -- Whitespace-free sentence whose boundaries and role sequence must be recovered.
>
> sample_submission.csv
>
> id (str) -- Test-row identifier.
>
> segmentation (str) -- Predicted whitespace-restored sentence.
>
> pos_tags (str) -- Space-delimited predicted role labels, one per predicted token.
>
> Evaluation
>
> Submit one row for every test id. Removing whitespace from segmentation must reproduce the corresponding test text. The number of space-delimited pos_tags must equal the number of tokens in segmentation.
>
> For a segmentation s, let B(s) be the set of character offsets after whitespace runs. For (s, p), let E(s,p) contain one pair (character_end, role) for every token, including the final character offset. We compute:
>
>
> boundary_f1 = F1(B(predicted_segmentation), B(truth_segmentation))
>
> aligned_role_f1 = F1(E(predicted_segmentation, predicted_roles), E(truth_segmentation, truth_roles))
>
> joint_exact = mean(normalize(predicted_segmentation) == normalize(truth_segmentation)
>
>                    and normalize(predicted_roles) == normalize(truth_roles))
>
> score = 0.50  *mean(boundary_f1) + 0.35*  mean(aligned_role_f1) + 0.15 * joint_exact
>
>
> The score is maximize-bounded in [0, 1]. Boundary F1 is the largest component because usable token offsets matter most; aligned role F1 has substantial weight because a syntactic label attached to the wrong span is not useful downstream; joint exactness rewards complete records.
>
> Submission
>
> Submit submission.csv with exactly these columns:
>
> id (str) -- Each test identifier exactly once.
>
> segmentation (str) -- Whitespace-restored text preserving the supplied characters.
>
> pos_tags (str) -- One predicted role label per predicted token.
>
> Example:
>
>
> id,segmentation,pos_tags
>
> ab6ee454d9025244,"' ຊີວິດຂ້ອຍ ...",PUNCT N N
>
> Requirements
>
> Include every test row exactly once; do not add extra rows or columns.
>
> Preserve every non-whitespace character and its order.
>
> Keep the number of role labels equal to the number of predicted tokens.
>
> Use role strings observed in the training data or another clearly learned label representation.
>
> The metric direction is maximize.
>
> What Not To Use
>
> Do not use an external copy of the underlying corpus, segmentation files, or POS-tag files to look up held-out sentences; that bypasses the joint learning task.
>
> Do not submit a cached mapping from full input strings to segmentation or role sequences.
>
> Do not replace the learned model with a hand-written tokenizer, punctuation parser, or fixed role lookup. Cleaning and Unicode-aware preprocessing are allowed, but both boundary and role predictions must be materially learned from training rows.
>
>  
>
> Submissions
> 1
> Top Score
> 0.744
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

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Maritime Track Maneuver Vision

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7adqrea1dnm9sw7fz5h2dgjh8c2kss
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.636

Full challenge description from page:

> Overview
>
> This Computer Vision and Sequence-to-Sequence challenge uses a current 96 x 96 RGB crop of a tracked maritime object, together with geometry and motion measured only up to that frame. Predict the object-centre correction needed at each of the next eight video frames relative to a constant-velocity extrapolation from the past eight-frame track.
>
> The output is a real-valued future correction sequence, not a class label. It models a practical tracker handoff: a constant-velocity tracker can provide the initial forecast, while a learned visual model predicts how the target will deviate when it turns, accelerates, or changes apparent motion. The split is sequence-disjoint across 18 labeled acquisition sequences and 6 hidden acquisition sequences; a source sequence never appears in both sides.
>
> To avoid filling the benchmark with trivial constant-velocity windows, a row is retained only when at least one of its next eight real correction vectors has magnitude at least 0.01 current-box scales. This fixed source filter is applied before the sequence-disjoint partitions and does not balance classes or duplicate rows.
>
> Dataset
> File descriptions
>
> images/train/<id>.jpg and images/test/<id>.jpg — lossy 96 x 96 RGB crops made from the current frame only.
>
> train.csv — labeled rows containing one current-object crop path, past-only geometry, and 16 future correction targets.
>
> test.csv — unlabeled rows with the same input columns as train.csv, without the future correction targets.
>
> sample_submission.csv — correctly formatted, non-degenerate example continuous predictions.
>
> Column descriptions
>
> id (string) — Opaque 16-character row identifier. It is not a sequence or frame identifier.
>
> group_key (string) — Opaque acquisition-group token. Rows sharing a token came from one source sequence; test tokens are unseen during training.
>
> image_path (string) — Path to the current-frame crop, relative to dataset/public/.
>
> object_type (string) — Observed object family: Boat or USV in this curated subset.
>
> center_x (float) — Current bounding-box centre x-coordinate normalized by current frame width.
>
> center_y (float) — Current bounding-box centre y-coordinate normalized by current frame height.
>
> bbox_width (float) — Current bounding-box width normalized by current frame width.
>
> bbox_height (float) — Current bounding-box height normalized by current frame height.
>
> area_ratio (float) — Current bounding-box area divided by current frame area.
>
> aspect_ratio (float) — Current bounding-box width divided by current bounding-box height.
>
> past_dx (float) — Centre displacement from eight frames earlier to the current frame, normalized by frame width.
>
> past_dy (float) — Centre displacement from eight frames earlier to the current frame, normalized by frame height.
>
> past_motion_ratio (float) — Past centre displacement divided by the square root of the current box area.
>
> future_correction_dx_1 (float, train.csv only) — Future-frame-1 x correction relative to constant-velocity extrapolation, normalized by current box scale.
>
> future_correction_dy_1 (float, train.csv only) — Future-frame-1 y correction relative to constant-velocity extrapolation, normalized by current box scale.
>
> future_correction_dx_2 (float, train.csv only) — Future-frame-2 x correction relative to constant-velocity extrapolation, normalized by current box scale.
>
> future_correction_dy_2 (float, train.csv only) — Future-frame-2 y correction relative to constant-velocity extrapolation, normalized by current box scale.
>
> future_correction_dx_3 (float, train.csv only) — Future-frame-3 x correction relative to constant-velocity extrapolation, normalized by current box scale.
>
> future_correction_dy_3 (float, train.csv only) — Future-frame-3 y correction relative to constant-velocity extrapolation, normalized by current box scale.
>
> future_correction_dx_4 (float, train.csv only) — Future-frame-4 x correction relative to constant-velocity extrapolation, normalized by current box scale.
>
> future_correction_dy_4 (float, train.csv only) — Future-frame-4 y correction relative to constant-velocity extrapolation, normalized by current box scale.
>
> future_correction_dx_5 (float, train.csv only) — Future-frame-5 x correction relative to constant-velocity extrapolation, normalized by current box scale.
>
> future_correction_dy_5 (float, train.csv only) — Future-frame-5 y correction relative to constant-velocity extrapolation, normalized by current box scale.
>
> future_correction_dx_6 (float, train.csv only) — Future-frame-6 x correction relative to constant-velocity extrapolation, normalized by current box scale.
>
> future_correction_dy_6 (float, train.csv only) — Future-frame-6 y correction relative to constant-velocity extrapolation, normalized by current box scale.
>
> future_correction_dx_7 (float, train.csv only) — Future-frame-7 x correction relative to constant-velocity extrapolation, normalized by current box scale.
>
> future_correction_dy_7 (float, train.csv only) — Future-frame-7 y correction relative to constant-velocity extrapolation, normalized by current box scale.
>
> future_correction_dx_8 (float, train.csv only) — Future-frame-8 x correction relative to constant-velocity extrapolation, normalized by current box scale.
>
> future_correction_dy_8 (float, train.csv only) — Future-frame-8 y correction relative to constant-velocity extrapolation, normalized by current box scale.
>
> For step h, the correction target is the real future centre minus the current centre plus h/8 times the observed past eight-frame displacement. The correction is divided by sqrt(current_box_width_pixels * current_box_height_pixels). The target uses only real annotated future frames during preparation; solvers receive only current/past public inputs.
>
> Evaluation
>
> Submissions are scored using future_trajectory_conservative_utility, maximized from 0 to 1. The grader computes the Euclidean correction error at each of the eight horizons. Later horizons receive larger weights 1, 2, ..., 8). Underpredicting the magnitude of a real correction receives factor 2.0; overpredicting receives factor 0.85, because a tracker can tolerate reserving extra search area more readily than missing a maneuver.
>
>
> def evaluate(y_true, y_pred):
>
>     error = l2_norm(y_pred - y_true, axis=2)  # shape: rows x 8
>
>     true_mag = l2_norm(y_true, axis=2)
>
>     pred_mag = l2_norm(y_pred, axis=2)
>
>     factor = where(pred_mag < true_mag, 2.0, 0.85)
>
>     weights = array([1, 2, 3, 4, 5, 6, 7, 8]) / 36
>
>     penalty = sum(error  *factor*  weights, axis=1)
>
>     return mean(1 / (1 + penalty / 0.05))
>
> Submission
>
> Submit one row for every id in test.csv.
>
> id (string) — The exact opaque identifier from test.csv.
>
> future_correction_dx_1 through future_correction_dx_8 (float) — Predicted x corrections for horizons 1 through 8.
>
> future_correction_dy_1 through future_correction_dy_8 (float) — Predicted y corrections for horizons 1 through 8.
>
> Example:
>
>
> id,future_correction_dx_1,future_correction_dy_1,future_correction_dx_2,future_correction_dy_2,future_correction_dx_3,future_correction_dy_3,future_correction_dx_4,future_correction_dy_4,future_correction_dx_5,future_correction_dy_5,future_correction_dx_6,future_correction_dy_6,future_correction_dx_7,future_correction_dy_7,future_correction_dx_8,future_correction_dy_8
>
> 016f7d26ed4c4654,0.01,-0.02,0.01,-0.02,0.02,-0.03,0.02,-0.03,0.03,-0.04,0.03,-0.04,0.04,-0.05,0.04,-0.05
>
> 023240e1c17ccde7,-0.01,0.00,-0.02,0.00,-0.02,0.01,-0.03,0.01,-0.03,0.01,-0.04,0.02,-0.04,0.02,-0.05,0.02
>
> Requirements
>
> The file must contain exactly the number of rows in test.csv, one for each test observation.
>
> Every id from test.csv must be present exactly once.
>
> Use the exact 17 columns and order shown above.
>
> All 16 predictions must be finite real-valued numbers; NaN and infinite values are rejected.
>
> Train a learned multi-output trajectory model using the public current/past columns. The RGB crop is an available auxiliary visual input for multimodal solutions; a constant-velocity baseline is allowed for calibration but is not a complete learned solution.
>
> Do not use external network access, future frames, future annotations, raw source labels, or upstream lookup at solution time.
>
> What Not To Use
>
> Do not reconstruct the hidden future corrections from raw annotation files or future frames.
>
> Do not infer a source sequence or frame number from image filenames, directory names, pixel hashes, or external reverse lookup.
>
> Do not copy future trajectories from the upstream dataset or memorize a public-row-to-answer map.
>
> Do not use a fixed constant-velocity output as the main method; it is the challenge baseline, not a learned solution.
>
>  
>
> Submissions
> 72
> Top Score
> 0.636
> Created
> Aug 9, 2026
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Rankings finalizing
> Lockdown
>
> New writes are paused for up to one hour while pre-cutoff submissions finish, then the roster freezes from available scores.
>
> Closing in 9h 59m
>
> Submit your solution before the deadline. Payouts are processed after the challenge closes.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Pre-Event Power Response Routing

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75v5dnfn53znf4n1dw2kha818c9pxe
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top score: 0.359

Full challenge description from page:

> Overview
>
> Power-monitoring operators do not only need an anomaly flag. Before an event fully develops, they need to choose the first response route: inspect the equipment or escalate a compound condition, investigate supply quality, or check telemetry. They also need an urgency estimate.
>
> Each solver-facing row is a six-channel, 60-second sequence ending 60–150 seconds before a real controlled event. Predict the response route and urgency as one compact sequence label. The source station, calendar day, event identifier, and source labels are withheld.
>
> This is a sequence to sequence task over real measured signals. The evaluation is event-balanced: every hidden event contributes total weight one across its available lead-time windows, so an event with more valid windows cannot dominate the score.
>
> Dataset
> File descriptions
>
> train.csv — labeled lead-time sequences from five calendar-day segments of each monitoring recording.
>
> test.csv — unlabeled lead-time sequences from two complete calendar-day segments held out from each recording.
>
> sample_submission.csv — valid submission format with deterministic placeholder labels.
>
> Column descriptions
>
> id — unique 16-character hexadecimal sequence identifier.
>
> voltage_V_sequence — JSON array of 60 measured voltage values.
>
> current_A_sequence — JSON array of 60 measured current values.
>
> power_W_sequence — JSON array of 60 measured active-power values.
>
> frequency_Hz_sequence — JSON array of 60 measured frequency values.
>
> power_factor_sequence — JSON array of 60 measured power-factor values.
>
> wifi_rssi_dBm_sequence — JSON array of 60 measured telemetry-strength values.
>
> target — training-only label in the form route|urgency.
>
> The three route labels are:
>
> equipment_escalation — inspect the connected load or operating condition; compound events use this route because they require escalation at the first decision point.
>
> supply_quality — investigate voltage, frequency, power-quality, or outage behavior.
>
> sensor_telemetry — check the measurement or communications path.
>
> The four urgency labels are incipient, low, medium, and urgent. The source’s high and critical states are intentionally combined into urgent because both require immediate operator escalation before finer-grained diagnosis.
>
> Evaluation
>
> Split every predicted target at the first |. Give each row the inverse of its hidden event group’s row count, so each event contributes total weight one. Then compute:
>
>
> event_weight = 1.0 / hidden_event_group_row_counts
>
> route_f1 = macro_f1(true_route, predicted_route,
>
>                     labels=["equipment_escalation", "supply_quality",
>
>                             "sensor_telemetry"], sample_weight=event_weight)
>
> urgency_f1 = macro_f1(true_urgency, predicted_urgency,
>
>                       labels=["incipient", "low", "medium", "urgent"],
>
>                       sample_weight=event_weight)
>
> score = 0.65  *route_f1 + 0.35*  urgency_f1
>
>
> The score is bounded in [0, 1] and higher is better. The route term receives more weight because a wrong first response can send a technician to the wrong subsystem; urgency remains important for dispatch order.
>
> Submission
>
> Submit exactly one row per id in test.csv.
>
> id — the exact test sequence identifier.
>
> target — one route and one urgency joined by a single pipe, for example supply_quality|urgent.
>
> Example:
>
>
> id,target
>
> 00052a6150a995b0,supply_quality|incipient
>
> 0030c306300ab36a,supply_quality|urgent
>
> Requirements
>
> Include every test id exactly once.
>
> Use only the three route labels and four urgency labels defined above.
>
> Use exactly one | separator and lowercase labels.
>
> Keep all six sequence columns out of the submission.
>
> The score is calculated on hidden event groups; do not assume row-level class balance.
>
> What Not To Use
>
> Do not use the source archive, source station files, source event IDs, source calendar-day identifiers, or the source’s label columns.
>
> Do not recover target labels by matching sequence values or hashed IDs to the source release or its released analysis code.
>
> Do not use the source detector flag, threshold, precomputed entropy features, or any source-derived label proxy; they are intentionally absent from train.csv and test.csv.
>
> Do not generate synthetic signal windows or inject artificial faults. The intended data are the supplied measured windows.
>
> Do not replace the learned model with a threshold-only or hand-written physical rule; a genuine model trained on the labeled sequences is required.
>
> Do not use a fixed lookup table keyed by sequence order, row ID, or source identity instead of learning from the labeled sequences.
>
>  
>
> Submissions
> 73
> Top Score
> 0.359
> Created
> Aug 11, 2026
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Rankings finalizing
> Lockdown
>
> New writes are paused for up to one hour while pre-cutoff submissions finish, then the roster freezes from available scores.
>
> Closing in 10h 31m
>
> Submit your solution before the deadline. Payouts are processed after the challenge closes.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Indian Monsoon Rain-Cell Evolution Sequence Forecasting

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7btfdfr2neycw7va26zjdpeh8c8x86
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top score: 0.518

Full challenge description from page:

> Overview
>
> This is a sequence-to-sequence forecasting problem. For each case, use ten
>
> consecutive daily rainfall grids to predict a variable-length structured sequence
>
> describing the rain cells that will appear during the following five days.
>
> The output is not a future rainfall raster or a single class. Each future day may
>
> contain as many as four cell tokens. A token jointly describes a cell's evolution
>
> event, coarse location, mean-intensity tier, area tier, and movement direction.
>
> The task therefore tests temporal representation learning, analog retrieval,
>
> structured decoding, and generalization to later Indian monsoon seasons.
>
> Use only the prepared public data and offline libraries available in the challenge
>
> environment. The intended compute tier is **CPU Default: 10 cores and 62.5 GiB
>
> RAM**. Internet access, hosted APIs, external datasets, source re-identification,
>
> and external challenge-specific models or code are prohibited.
>
> For every case_id in test.csv, predict one canonical event_sequence covering
>
> future days 1 through 5. Every day must contain either one dry token or one to four
>
> rain-cell tokens.
>
> Scientific Provenance and Benchmark Positioning
>
> The rainfall fields are observation-derived, not synthetic. They are an
>
> Indian-domain transformation of CHIRPS v2, which combines satellite infrared
>
> measurements with in-situ rain-gauge observations. The authoritative scientific
>
> record is Funk et al. (2015), [*The climate hazards infrared precipitation with
>
> stations—a new environmental record for monitoring
>
> extremes*](https://doi.org/10.1038/sdata.2015.66), Scientific Data 2, 150066.
>
> This challenge introduces the **Monsoon Cell Evolution Sequence Protocol,
>
> version 1.0 (MCESP-1)**. MCESP-1 is the original combination of:
>
> a five-day, variable-cardinality rain-cell lineage language;
>
> canonical tokens that jointly encode birth, continuation, split, merge, or dry
>
> topology with sector, intensity, area, and movement;
>
> forecasting those tokens before the corresponding cells are observed; and
>
> the Monsoon Cell Evolution Sequence Score, which combines optimal within-day
>
> object matching, lifecycle edit similarity, and count agreement.
>
> The Target Sequence and Evaluation sections below are the normative MCESP-1
>
> prose specification. The supplied grade.py is its executable scoring reference.
>
> A recommended citation for the protocol is: *Indian Monsoon Rain-Cell Evolution
>
> Sequence Forecasting: Monsoon Cell Evolution Sequence Protocol v1.0 (MCESP-1),
>
> Project Eris benchmark specification, 2026.*
>
> The closest established precipitation benchmark is Weather4cast at NeurIPS 2022
>
> (Gruca et al., 2022, PMLR 220:292–313).
>
> Weather4cast predicts high-resolution rain-radar movies from multi-band satellite
>
> imagery under spatio-temporal shifts: its supervised output is a dense future
>
> movie. MCESP-1 instead predicts a sparse, variable-length object-lineage sequence
>
> from daily rainfall histories. A prediction can therefore have plausible rainfall
>
> mass yet be wrong because it misses a birth, split, merge, cell count, or event
>
> order—errors that dense pixel objectives do not represent explicitly.
>
> Atmospheric trackers such as CoCoMET v1.0 (Hahn et al., 2025,
>
> Geoscientific Model Development 18:5971–5996)
>
> identify and analyze mergers and splits after all relevant frames have already
>
> been observed. CoCoMET motivates the physical relevance of lifecycle topology,
>
> but it is not a forecast benchmark and does not define the MCESP-1 token language,
>
> chronological prediction split, or composite score. Thus, this task evaluates a
>
> different capability: predicting future graph-topology changes and serializing
>
> them consistently under uncertainty.
>
> Public Dataset
>
> | Path | Contents |
>
> |---|---|
>
> | train.csv | 1,632 labeled training cases. |
>
> | test.csv | 211 unlabeled, chronologically held-out cases. |
>
> | rain_contexts.npz | Rainfall input arrays and public training future rasters. |
>
> | sample_submission.csv | A valid five-day dry-sequence submission with all test IDs. |
>
> The held-out cases come from later monsoon seasons than the training cases.
>
> Complete 15-day test blocks do not overlap. Opaque IDs contain no date, location,
>
> or target information. Exact input grids, individual grids, complete target
>
> strings, and IDs do not cross the train/test boundary.
>
> CSV Columns
>
> | Column | Type | Files | Meaning |
>
> |---|---|---|---|
>
> | case_id | non-empty string | train, test | Opaque row identifier used for submission alignment. |
>
> | region_code | categorical string | train, test | One of r1, r2, r3, r4, r5, or r6; these identify six fixed rainfall subregions. |
>
> | season_phase | float, minimum 0 and maximum 1 | train, test | Relative position within that case's monsoon season. |
>
> | context_index | integer | train, test | Row index into the matching context array. |
>
> | event_sequence | canonical token string | train only | Hidden five-day output format defined below. |
>
> No CSV field is nullable.
>
> Rainfall Arrays
>
> Load rain_contexts.npz with numpy.load(..., allow_pickle=False).
>
> | Array | Type and shape | Meaning |
>
> |---|---|---|
>
> | train_contexts | uint16, (1632,10,44,44) | Ten input days for each training row. |
>
> | train_future | uint16, (1632,5,44,44) | Five observed future days for training only; useful for learning cell dynamics. |
>
> | test_contexts | uint16, (211,10,44,44) | Ten input days for each test row. |
>
> | missing_value | uint16 scalar, 65535 | No-data/ocean sentinel. |
>
> Valid rainfall values are tenths of a millimetre per day. Divide by 10 for
>
> mm/day. Arrays are aligned to CSV rows through context_index. Small
>
> deterministic measurement perturbations of at most 0.1 mm are part of the data
>
> and require no correction.
>
> Target Sequence
>
> A rain cell is an 8-connected wet component after a 3 by 3 closing operation.
>
> Wet pixels have at least 8 mm/day of rain. Components smaller than four pixels
>
> are discarded, and at most the four cells with greatest rainfall mass are kept.
>
> Cells on consecutive days are linked when either (a) a two-pixel dilation of the
>
> earlier cell overlaps at least 8% of the smaller cell's area, or (b) their
>
> centroids are at most 5.5 pixels apart. A merge has at least two linked parents;
>
> a split is the child of a parent that links to at least two current cells.
>
> Movement is measured from the rainfall-mass-weighted centroid of linked parents;
>
> displacement below one pixel is O, otherwise direction is rounded to the nearest
>
> 45-degree compass direction. These rules let you reproduce training labels from
>
> train_future, but the five future test grids are withheld and must be forecast.
>
> Each token has this exact grammar:
>
>
> D{day}_{event}_{sector}_{intensity}_{area}_{direction}
>
>
> For example, D2_S_06_2_1_NE describes a day-2 split cell in sector 06, with
>
> intensity tier 2, area tier 1, moving northeast.
>
> | Field | Allowed values | Meaning |
>
> |---|---|---|
>
> | day | one of 1, 2, 3, 4, or 5 | Forecast day. |
>
> | event | B, C, S, M, D | Birth, continuation, split, merge, or dry day. |
>
> | sector | a two-digit integer from 00 through 15, inclusive | Cell centroid in a row-major 4 by 4 grid: 00 is upper-left and 15 is lower-right. |
>
> | intensity | one of 0, 1, 2, or 3 | Mean rainfall tier: 0 is below 15; 1 is at least 15 and below 30; 2 is at least 30 and below 60; 3 is at least 60 mm/day. |
>
> | area | one of 0, 1, 2, or 3 | Cell-area tier: 0 is 4 through 9; 1 is 10 through 24; 2 is 25 through 59; 3 is at least 60 pixels. |
>
> | direction | one of O, N, NE, E, SE, S, SW, W, or NW | Movement from linked parent cell(s); O means no movement or no parent. |
>
> Event semantics are:
>
> B: the current cell has no linked cell on the preceding day.
>
> C: one preceding cell links only to this current cell.
>
> S: one preceding cell links to multiple current cells.
>
> M: multiple preceding cells link to the current cell.
>
> D: no retained rain cell exists that day. Its only valid form is
>
> D{day}_D_00_0_0_O and it must be that day's sole token.
>
> Join tokens with |. Include one to four tokens for every day. Tokens must be
>
> sorted by day and, within a day, by (sector,event,intensity,area). The direction
>
> is not a sort key. Hidden test sequences contain a minimum of 5 and a maximum of
>
> 19 tokens.
>
> Submission
>
> Write the final CSV to ./working/submission.csv with exactly 211 rows and these
>
> columns:
>
>
> case_id,event_sequence
>
>
> Here are the header and first three data rows of a correctly formatted submission.
>
> The complete file continues with the remaining 208 test IDs, for 211 data rows in
>
> total:
>
>
> case_id,event_sequence
>
> mc_006f8c8f3ce56d0a8d83,D1_D_00_0_0_O|D2_D_00_0_0_O|D3_D_00_0_0_O|D4_D_00_0_0_O|D5_D_00_0_0_O
>
> mc_01c44cd5d92a03b4de11,D1_D_00_0_0_O|D2_D_00_0_0_O|D3_D_00_0_0_O|D4_D_00_0_0_O|D5_D_00_0_0_O
>
> mc_06f17c7e329fd4766082,D1_D_00_0_0_O|D2_D_00_0_0_O|D3_D_00_0_0_O|D4_D_00_0_0_O|D5_D_00_0_0_O
>
>
> Requirements:
>
> Include every test case_id exactly once; do not invent, omit, or duplicate IDs.
>
> event_sequence must be non-empty, at most 800 characters, and obey the grammar
>
> and canonical ordering above.
>
> Include all five days and at most four tokens per day.
>
> Add no columns. One platform-managed column named is_public, visibility, or
>
> _visibility is accepted and ignored.
>
> Malformed sequences, wrong ID sets, duplicate IDs, blank IDs, or unsupported
>
> columns reject the submission with a validation error.
>
> Evaluation
>
> Submissions are ranked by the Monsoon Cell Evolution Sequence Score. Higher
>
> is better. The theoretical minimum is 0.00, the theoretical maximum is 1.00,
>
> and an exact submission scores 1.00.
>
> For two cell tokens, define a weighted similarity:
>
>
> token_similarity = 0.28 * event_exact
>
>                  + 0.30 * sector_proximity
>
>                  + 0.14 * intensity_proximity
>
>                  + 0.12 * area_proximity
>
>                  + 0.16 * direction_proximity
>
>
> sector_proximity is one minus the Manhattan distance between 4 by 4 sector
>
> coordinates divided by 6. Intensity and area proximity are one minus tier
>
> difference divided by 3. Compass directions use circular distance in 45-degree
>
> steps; any comparison between O and a compass direction has distance 1.
>
> For each day, the grader finds the maximum-similarity one-to-one matching between
>
> hidden and predicted tokens and divides the matched sum by the larger token count.
>
> DayScore is the mean of the five day scores. EventEditSimilarity is one minus
>
> the Levenshtein distance between the ordered day+event sequences divided by the
>
> larger sequence length. CountSimilarity is one minus the absolute total-token
>
> count difference divided by the larger count.
>
>
> RowScore = 0.65 * DayScore
>
>          + 0.20 * EventEditSimilarity
>
>          + 0.15 * CountSimilarity
>
> FinalScore = mean(RowScore over evaluated cases)
>
>
> The grader aligns rows by case_id and supports any non-empty private answer
>
> shard used by the platform.
>
>  
>
> Submissions
> 12
> Top Score
> 0.518
> Created
> Aug 11, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> 7/12
> solvers beat AI
> Closing soon
>
> Prize pool active — closing countdown started. At 12, up to 12 solvers will be selected to continue.
>
> Closing in 11h 52m
>
> Submit your solution before the deadline. Payouts are processed after the challenge closes.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Lexical Construal Graph Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7eeapg30ja9ww0nwq0jt6g598c6x0x
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: multimodal, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: —

Full challenge description from page:

> Hard Lexical Construal Graph Reconstruction
> 1. Overview
>
> Online business reviews contain expressions whose meaning depends on several words and on the relationships between those words. For example, the expression “have a good experience” can behave as one lexical unit even though other words occur inside it. Relational words such as with, for, in, and possessives also connect a semantic governor to an object while expressing a contextual role.
>
> This challenge uses English web-review sentences from STREUSLE, a manually annotated lexical-semantics corpus built over the reviews portion of the English Web Treebank. Given each sentence and basic token information, build a CPU-trainable model that predicts:
>
> Lexical units: strong or weak multiword expressions, including discontinuous expressions.
> Construal frames: a relational trigger, its governor and object, its structural configuration, its contextual scene role, and its lexical function.
>
> This is a structured prediction task rather than ordinary token classification. Test lemmas and dependency arcs are hidden, test documents never occur in training, and sentences with no annotated structure are retained as genuine negative examples.
>
> 2. Dataset files
>
> The platform runs prepare.py over the raw STREUSLE source and creates the following participant-facing files.
>
> File	Format	Contents
> train.csv	CSV	Labeled training examples with columns id,text,tokens_json,target_json.
> test.csv	CSV	Unlabeled evaluation examples with columns id,text,tokens_json.
> label_inventory.json	JSON	All permitted categorical output labels.
> sample_submission.csv	CSV	One valid empty prediction for every test ID, with columns id,prediction_json,confidence.
>
> Private evaluation answers are not available to participants.
>
> 2.1 CSV columns
> Column	Type	Available in	Description
> id	string	train, test, submission	Opaque unique row identifier beginning with h_. It contains no document identity.
> text	string	train, test	Human-readable English review sentence.
> tokens_json	JSON-encoded string	train, test	Ordered array of public token objects described below.
> target_json	JSON-encoded string	train only	Gold structured annotation with lexical_units and construals. It has the same schema required in prediction_json.
> prediction_json	JSON-encoded string	submission	Predicted structured annotation using exactly the target schema.
> confidence	floating-point number	submission	Confidence that the entire predicted row exactly matches the gold row; must be finite and between 0.0 and 1.0, inclusive.
> 2.2 tokens_json
>
> Each element of the token array has exactly these public features:
>
> Field	Type	Description
> i	integer	One-based contiguous token index.
> form	string	Surface token appearing in the review.
> upos	categorical string	Universal Dependencies part-of-speech tag such as NOUN, VERB, ADP, or PRON.
> feats	string	Pipe-separated Universal Dependencies morphology, or _ when absent.
>
> Example:
>
> [  
>   {"i":1,"form":"They","upos":"PRON","feats":"Case=Nom|Number=Plur"},  
>   {"i":2,"form":"helped","upos":"VERB","feats":"Tense=Past|VerbForm=Fin"}  
> ]  
>
> Lemmas, dependency heads, dependency relations, source document IDs, and native annotations are deliberately withheld from test inputs.
>
> 2.3 label_inventory.json
>
> The inventory has exactly four arrays of strings:
>
> {  
>   "strengths":["strong","weak"],  
>   "mwe_categories":["N","V.LVC.full","V.VPC.full","WEAK"],  
>   "supersenses":["NONE","n.PERSON","p.Topic","v.stative"],  
>   "construal_configs":["default","possessive","subordinating"]  
> }  
>
> The example is abbreviated; use the supplied file for the complete arrays. A predicted strength must occur in strengths, category in mwe_categories, and config in construal_configs.
>
> There is one shared semantic-label inventory: supersenses. The lexical-unit field supersense and both construal fields scene and function must draw from this same supersenses array. There are no separate scene_supersenses or function_supersenses arrays. Sharing the inventory is intentional because a supersense may describe a lexical expression, a contextual scene role, or a trigger's lexical function. For example, if p.Topic occurs in supersenses, it is valid syntactically in any of those three fields, although a model must learn from training data when it is semantically appropriate.
>
> A lexical-unit lemma is a normalized string learned from training and is not a categorical inventory entry.
>
> 3. Target and prediction schema
>
> target_json and prediction_json are JSON objects with exactly two keys:
>
> {  
>   "lexical_units":[  
>     {  
>       "token_ids":[2,5],  
>       "strength":"strong",  
>       "category":"V.LVC.full",  
>       "lemma":"have <2> experience",  
>       "supersense":"v.stative"  
>     }  
>   ],  
>   "construals":[  
>     {  
>       "trigger":7,  
>       "config":"default",  
>       "governor":5,  
>       "object":9,  
>       "scene":"p.Stimulus",  
>       "function":"p.Topic"  
>     }  
>   ]  
> }  
> 3.1 Lexical-unit fields
> Field	Type	Meaning
> token_ids	nonempty array of unique increasing integers	Exact member tokens. Do not include intervening gap tokens.
> strength	inventory string	strong for a fixed lexical expression or weak for a looser association.
> category	inventory string	Grammatical/lexical MWE category. Uncategorized weak expressions use WEAK.
> lemma	nonempty string	Normalized expression lemma. Native notation such as <2> denotes a two-token gap.
> supersense	string from the shared supersenses array	Coarse lexical-semantic class, or NONE when no supersense is assigned.
>
> For “have a good experience,” tokens have and experience may have token_ids:[1,4]; [1,2,3,4] would incorrectly fill the discontinuity.
>
> 3.2 Construal fields
> Field	Type	Meaning
> trigger	positive integer	One-based index of the relational trigger.
> config	inventory string	Structural configuration of the relation.
> governor	nonnegative integer	Index of the semantic governor; 0 means no annotated/root endpoint.
> object	nonnegative integer	Index of the semantic object; 0 means no annotated endpoint.
> scene	string from the shared supersenses array	Role required by the surrounding situation.
> function	string from the shared supersenses array	Meaning contributed by the trigger itself.
>
> Both arrays may be empty. Every object must have exactly the documented fields. Duplicate objects, additional fields, malformed JSON, invalid indices, and non-finite confidence values make the submission structurally invalid.
>
> 4. Submission format
>
> Submit one CSV file containing exactly these columns in this order:
>
> id,prediction_json,confidence  
>
> Every test ID must occur exactly once. JSON embedded in CSV must follow normal CSV escaping: each internal double quote is doubled and the complete JSON value is enclosed in double quotes.
>
> Complete correctly formatted example with two rows:
>
> id,prediction_json,confidence  
> h_0123456789abcdef01,"{""lexical_units"":[],""construals"":[]}",0.15  
> h_abcdef012345678901,"{""lexical_units"":[{""token_ids"":[2,5],""strength"":""strong"",""category"":""V.LVC.full"",""lemma"":""have <2> experience"",""supersense"":""v.stative""}],""construals"":[{""trigger"":7,""config"":""default"",""governor"":5,""object"":9,""scene"":""p.Stimulus"",""function"":""p.Topic""}]}",0.82  
>
> The supplied sample_submission.csv contains all real test IDs and valid empty JSON predictions. Replace its predictions and confidence values while preserving the header and ID set.
>
> 5. Evaluation metric
>
> The grader computes five corpus-level F1 components, an exact-row accuracy component, and a confidence-calibration component.
>
> For each corpus-level component, every predicted and gold structure is converted into a set item prefixed by its row ID. Therefore, a structure predicted in the wrong sentence does not match. For predicted set P and gold set G:
>
> TP = |P intersection G|  
> FP = |P - G|  
> FN = |G - P|  
> F1(P,G) = 2*TP / (2*TP + FP + FN)  
>
> If both sets are empty, F1 is defined as 1; if only one is empty, F1 is 0.
>
> The five set representations and weights are:
>
> Symbol	Set item after row ID	Weight
> F_member	(token_ids, strength) for every lexical unit	0.20
> F_lexical	(token_ids, strength, category, lemma, supersense)	0.20
> F_trigger	(trigger) for every construal	0.10
> F_arc	(trigger, governor, object)	0.20
> F_semantic	(trigger, config, scene, function)	0.20
>
> For test row i, let e_i = 1 when its complete parsed prediction is exactly equal to the complete gold object after canonical sorting, and e_i = 0 otherwise. With N test rows:
>
> Exact = (1/N) * sum_i e_i  
> Calibration = (1/N) * sum_i [1 - (confidence_i - e_i)^2]  
>
> Thus confidence is calibrated against complete-row correctness using one minus Brier loss. The final score is:
>
> Score = 0.20*F_member  
>       + 0.20*F_lexical  
>       + 0.10*F_trigger  
>       + 0.20*F_arc  
>       + 0.20*F_semantic  
>       + 0.05*Exact  
>       + 0.05*Calibration  
>
> The score is clipped to [0,1]. A perfect prediction with confidence 1.0 on every row scores exactly 1.0. A structurally invalid submission—including missing or duplicate IDs, incorrect columns, invalid JSON, or out-of-range confidence—scores 0.0.
>
> 6. Rules and compute limits
>
> Use only the supplied public challenge files. External corpora, pretrained lexicons, web services, source-review lookup, manual test labeling, hard-coded test IDs, and test-feedback adaptation are prohibited. The solution must train a genuine statistical or machine-learning model offline.
>
> Training plus inference must finish within 90 minutes using at most 10 CPU cores and 62 GB RAM. GPU execution is not permitted.
>
>  
>
> Submissions
> 0
> Top Score
> —
> Created
> Aug 11, 2026
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

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Cross-Lingual Counterfactual Edit Footprint Localization

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76tg1zc453m7nwf2aes3tb458b2h3r
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top score: 0.351

Full challenge description from page:

> Semantic Ripple: Cross-Lingual Counterfactual Edit Footprint Localization
> The problem
>
> A compact edit in one language does not necessarily remain compact, contiguous, or positionally aligned when the same change is expressed in another language.
>
> Changing a Dusun sentence from "every day" to "sometimes," from one subject to several subjects, or from a completed action to an intended action may replace one token in English, affect several tokens in Malay, or require an insertion at a boundary with no direct positional counterpart in Dusun.
>
> This challenge asks you to localize that hidden cross-lingual ripple.
>
> Each example is built from two naturally occurring rows in a parallel Dusun-English-Malay corpus. The rows express closely related meanings but differ through a compact semantic edit. You are shown four encoded sequences:
>
> Dusun before
> Dusun after
> English before
> Malay before
>
> The edited English and Malay sequences are hidden.
>
> Your model must predict the structural footprint of the hidden edit in both target languages. Each language has two outputs:
>
> Output       Meaning
> --------------------------------------------------------------------------------
> Token mask   Existing token positions that are replaced or removed
> Gap mask     Token boundaries where one or more new tokens are inserted
>
>
> For a visible sequence containing n tokens, the token mask contains n bits and the gap mask contains n + 1 bits. Gap 0 is before the first token, gap n is after the final token, and every other gap lies between neighbouring tokens.
>
> Example:
>
> Encoded English before:  ta vek roni pex
> Token positions:          0  1   2    3
> Gap positions:           0  1   2    3  4
>
> Token mask:              0010
> Gap mask:                00010
>
>
> This footprint means that token position 2 changes and new material is inserted between token positions 2 and 3.
>
> The released text is not readable Dusun, English, or Malay. There are three independent language-specific symbolic vocabularies: one shared by the two Dusun views, one for English, and one for Malay. Token identities do not overlap across languages. What remains learnable is how recurring semantic changes in the encoded Dusun pair propagate into recurring English and Malay structures.
>
> This is not translation generation, candidate retrieval, sentence matching, or conventional word alignment. The required prediction is the unseen token-and-boundary footprint of a counterfactual semantic edit in two languages simultaneously.
>
> Dataset
>
> The source material contains aligned Dusun, English, and Malay sentences. The preparation process deterministically selects compact natural edit pairs, chooses one direction for each pair, groups related examples before splitting, and encodes all released sequences.
>
> Every encoded token is separated by one space. The values in english_length and malay_length therefore specify the exact token-mask lengths.
>
> The current release contains:
>
> File                     Rows
> --------------------------------
> train.csv                1,962
> test.csv                   438
> sample_submission.csv      438
>
> train.csv
> Column                    Type      Description
> --------------------------------------------------------------------------------
> id                        string    Opaque hashed example identifier
> encoded_dusun_before      string    Encoded Dusun sequence before the edit
> encoded_dusun_after       string    Encoded Dusun sequence after the edit
> encoded_english_before    string    Encoded English sequence before the edit
> encoded_malay_before      string    Encoded Malay sequence before the edit
> english_length            integer   Tokens in encoded_english_before
> malay_length              integer   Tokens in encoded_malay_before
> english_token_mask        string    English replacement/deletion mask
> english_gap_mask          string    English insertion-boundary mask
> malay_token_mask          string    Malay replacement/deletion mask
> malay_gap_mask            string    Malay insertion-boundary mask
>
> test.csv
>
> test.csv contains the same seven input columns and omits the four target masks.
>
> sample_submission.csv
> Column                    Type      Description
> --------------------------------------------------------------------------------
> id                        string    Identifier from test.csv
> english_token_mask        string    Binary mask of length english_length
> english_gap_mask          string    Binary mask of length english_length + 1
> malay_token_mask          string    Binary mask of length malay_length
> malay_gap_mask            string    Binary mask of length malay_length + 1
>
>
> The sample predicts no change at any position. It demonstrates the required format and is not a useful predictive solution.
>
> Evaluation
>
> English and Malay are evaluated separately. Within one language, the token mask and the gap mask are scored as two independent channels.
>
> Dice localization
>
> Dice rewards partial overlap between the predicted and true changed positions:
>
> Dice(P, T) = 2 × |P ∩ T| / (|P| + |T|)
>
>
> Here, P is the set of predicted changed positions in one channel and T is the corresponding true set. Both counts are pooled across the whole test split before the ratio is taken, so a rare true insertion is worth as much as a frequent token replacement and a submission that never predicts an insertion earns nothing on the gap channel.
>
> The two channel scores are averaged with equal weight:
>
> channel_dice = 0.50 × token_dice + 0.50 × gap_dice
>
>
> Token masks are dense and gap masks are sparse. Scoring the two channels separately stops the dense token mask from absorbing the localization credit that belongs to the sparse insertion mask.
>
> Exact-footprint accuracy
>
> An example receives exact credit for a language only when every token bit and every gap bit for that language is correct:
>
> Exact(P, T) = 1 when P = T
>               0 otherwise
>
> Final score
>
> For each language:
>
> exact_accuracy = fraction of exactly correct footprints
>
> language_score = 0.60 × channel_dice + 0.40 × exact_accuracy
>
>
> The final score is the harmonic mean of the English and Malay language scores:
>
> final_score = 2 × english_score × malay_score
>               --------------------------------
>               english_score + malay_score
>
>
> If both language scores are zero, the final score is zero. Higher is better, and a perfect submission scores 1.0.
>
> Every retained example contains at least one true English change and at least one true Malay change. Predicting all-zero masks therefore scores zero. The exact-footprint component also prevents a broad positional span from receiving most of the available score merely by covering the true edit, and marking every token position while predicting no insertion is a weak strategy because it forfeits the entire gap channel.
>
> Extra ids and extra columns are ignored. A missing official id receives zero exact credit and still contributes its true changed positions to the Dice denominators, so omitting difficult rows cannot raise a score. Duplicate ids or malformed masks make a submission invalid.
>
> Submission
>
> Submit one CSV with one row for every id in test.csv.
>
> Column                    Required value
> --------------------------------------------------------------------------------
> id                        Exact test identifier
> english_token_mask        english_length binary digits
> english_gap_mask          english_length + 1 binary digits
> malay_token_mask          malay_length binary digits
> malay_gap_mask            malay_length + 1 binary digits
>
>
> Example:
>
> id,english_token_mask,english_gap_mask,malay_token_mask,malay_gap_mask
> ripple_13d89a53e4c39a22,"0010","00010","010","0000"
> ripple_f42d87c15c8b019e,"10001","000000","0011","00001"
>
>
> Masks may contain only 0 and 1. Load the four target columns with dtype=str when reading train.csv; otherwise CSV type inference may remove leading zeroes. The grader can restore leading zeroes when an otherwise valid submitted mask was interpreted as an integer, but it cannot repair an overlong mask or a value containing other characters.
>
> Row order does not matter.
>
> What to use
>
> A valid submission must train a predictive model from the released training data.
>
> A natural design encodes the Dusun before-and-after sequences, constructs a representation of their semantic difference, and conditions token-level and gap-level classifiers over the visible English and Malay sequences.
>
> Suitable approaches include:
>
> Character-level or learned-subword encoders
> Bidirectional recurrent networks
> Compact convolutional sequence models
> Small Transformer encoders
> Cross-attention between the Dusun edit and target tokens
> Separate token and insertion-gap prediction heads
> Joint English-Malay prediction objectives
> Contrastive or consistency auxiliary losses
> Ensembles trained entirely inside the submission script
>
> General-purpose pretrained model weights are permitted when they were not trained or adapted specifically for this challenge, its source corpus, or its hidden test examples.
>
> The predictions must come from the trained model. Deterministic post-processing may enforce mask lengths, thresholds, and output validity, but it must not replace learning as the primary prediction mechanism.
>
> What not to use
>
> Do not search for, download, reconstruct, or match against the original Dusun-English-Malay corpus or any mirror, derivative, translation memory, dictionary, or parallel resource built from it.
>
> Do not use web search, live retrieval, machine-translation services, closed prediction APIs, hosted databases, or outside corpora to recover the hidden edited sentences or their footprints.
>
> Do not seek or reconstruct organizer-only assets such as the preparation script, raw row identifiers, pseudo-word mappings, edit-pair selection, private answers, or encoding seeds.
>
> Do not derive predictions from id, reverse hashed identifiers, manually label test rows, hardcode test-specific answers, or share recovered plaintext and cipher mappings.
>
> TF-IDF, bag-of-words, BM25, count vectorizers, hashing vectorizers, sparse cosine retrieval, lexical n-gram retrieval, and hand-written equivalents are not permitted.
>
> Manual substitution tables, fixed decryption systems, hand-authored translation rules, deterministic dictionaries, and rule-only lookup pipelines without a trained predictive model are not permitted.
>
> External fine-tuning data is not permitted. All challenge-specific training and adaptation must occur inside the submitted solution using only the released training split.
>
> Compute
> Resource   Limit
> -----------------------------------------------
> CPU        10 cores
> RAM        62.5 GB
> Runtime    90 minutes, including training and inference
> GPU        none
>
>
> The task is designed for compact sequence models. Its main difficulty is learning how an observed semantic edit changes position and form across languages, not large-scale computation.
>
> Submissions
> 4
> Top Score
> 0.351
> Created
> Jul 23, 2026
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

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Resilient Workforce Module Selection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx700meqnpbj2j4nyeshcpgfbn88fa6z
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.561

Full challenge description from page:

> Overview
>
> Workforce planners often have more operational duties to support than a limited training budget can cover. A plan that looks efficient can also be fragile: if one selected module is cancelled or unavailable, essential duties may lose all support.
>
> Each packet contains eight anonymized work-task statements and six candidate training-module briefs. Select exactly three modules. A good portfolio covers many tasks under normal operation and retains coverage after the loss of any one selected module.
>
> This is a fine-tuning benchmark for compact text encoders combined with robust discrete optimization. Training packets provide task-to-module coverage supervision. Test packets require estimating that latent coverage graph and optimizing the submitted portfolio; no canonical portfolio label is predicted.
>
> Portfolio Semantics
>
> Candidate letters are local to each packet and have no meaning across packets. Task slots and candidate letters are independently permuted for every packet during preparation. Submit three distinct letters in alphabetical order.
>
> For a selected portfolio:
>
> A task has nominal coverage when at least one selected module covers it.
> For each possible single-module loss, remove that module and recompute task coverage.
> Failure coverage is the lowest coverage fraction across the three possible losses.
>
> Different portfolios can be equally optimal. The grader evaluates the portfolio itself rather than comparing it with one stored answer set.
>
> Evaluation
>
> The score is maximized and ranges from 0 to 1.
>
> For each packet:
>
>
> portfolio_utility = 0.40  *nominal_coverage + 0.60*  failure_coverage
>
> mean_portfolio_utility = mean utility across all 20 valid portfolios
>
> row_score = max(0, (portfolio_utility - mean_portfolio_utility)
>
>                    / (best_possible_portfolio_utility - mean_portfolio_utility))
>
>
> nominal_coverage is the fraction of eight tasks covered by at least one selected module. failure_coverage is the minimum covered fraction after separately removing each selected module. mean_portfolio_utility is the mean raw utility across the 20 valid portfolios. best_possible_portfolio_utility is the maximum utility among those portfolios.
>
> Test packets are assigned deterministically to hidden public and private leaderboard partitions. The public score is the mean row_score over the public partition, and the private score is the mean over the private partition; both use the same formula and range. Because values below mean_portfolio_utility are clipped to zero while values above it retain positive credit, a uniformly random portfolio does not have expected score zero. Its exact expected score over the complete fixed test set, obtained by averaging row_score over all 20 portfolios for every packet, is 0.269184. Every optimal portfolio receives full row credit even when several optima exist.
>
> Dataset
>
> Public files:
>
> | File | Rows | Description |
>
> |---|---:|---|
>
> | train_packets.csv | 2400 | Training packet inputs. |
>
> | train_coverage.csv | 115200 | Binary task-to-module coverage supervision for training packets. |
>
> | test_packets.csv | 1200 | Held-out packet inputs. |
>
> | sample_submission.csv | 1200 | Valid submission template. |
>
> train_packets.csv and test_packets.csv columns:
>
> | Column | Type | Meaning |
>
> |---|---|---|
>
> | packet_id | string | Anonymous packet identifier. |
>
> | task_1 through task_8 | string | Anonymized operational task statements. |
>
> | module_A through module_F | string | Candidate training-module briefs. |
>
> train_coverage.csv columns:
>
> | Column | Type | Meaning |
>
> |---|---|---|
>
> | packet_id | string | Training packet identifier. |
>
> | task_slot | integer | Task position from 1 through 8. |
>
> | module_letter | string | Local candidate letter A through F. |
>
> | covers | integer | 1 if the module covers the task and 0 otherwise. |
>
> The split is disjoint by underlying occupation group. Preparation replaces source packet identifiers with salted pseudorandom identifiers, independently permutes the eight task slots in every packet, and independently remaps the six candidate modules to local letters while applying the same mappings to coverage supervision and hidden scoring data. Original occupation names, source codes, task identifiers, activity identifiers, dates, source row order, and administrative fields are not included. Task text is transformed to reduce exact-source reconstruction.
>
> Submission
>
> Submit exactly these columns, in this order:
>
>
> packet_id,module_1,module_2,module_3
>
> bundle_0123456789abcdef1234,A,C,F
>
> bundle_fedcba9876543210abcd,B,D,E
>
>
> Requirements:
>
> Include exactly one row for every test packet_id.
> Use letters A through F only.
> Select exactly three distinct modules.
> List selected letters in alphabetical order.
> Do not include extra columns.
> Save the file as ./working/submission.csv.
> A row containing an empty, missing, non-finite, unknown, malformed, repeated, or out-of-order module value receives zero row credit. A submission with an invalid column schema or an incomplete, extra, unknown, or duplicated packet_id set receives zero on both leaderboard partitions.
> Restrictions
>
> Use only the released public files and locally available modeling tools or model weights. Network access, remote APIs, hosted inference or training services, external datasets, external record lookup, and source-row reconstruction are prohibited. Hidden files, private coverage data, packet IDs, hashes, row order, and grader internals may not be used as predictive features. Local text-model adaptation, coverage estimation, robust optimization, calibration, and ensembling are allowed.
>
>  
>
> Submissions
> 1
> Top Score
> 0.561
> Created
> Jun 12, 2026
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

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Lane-Free Traffic Interaction Sequence Forecasting

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx721gw9c9dqyw62979vkjrjad8c9p4v
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU-only; no GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat passbaseline's score of 0.698!

Full challenge description from page:

> Lane-Free Traffic Interaction Sequence Forecasting Overview Forecast how seven anonymous road users will move together in lane-free Indian traffic. Each case provides two synchronized observations. Your output is a cost-ordered future motion-coupling tree: six undirected edges connecting actors whose five-step displacement responses are most similar, with each edge labelled by the future step at which the pair's velocities converge most closely. This is a CPU-only Sequence To Sequence task over real trajectories from a lane-free urban road in Surat, India. It is not vehicle classification, coordinate regression, a maneuver-label task, or a synthetic-generator puzzle. All seven actors are symmetric. Solvers must forecast multi-agent motion, compare all 21 possible actor pairs, predict time-localized velocity convergence, rank pairwise coupling, and enforce a global spanning-tree constraint. Public data provenance The uploaded episode package is derived from the public research release Extended vehicular trajectory data from India, Version 1, published by Mendeley Data on 22 July 2020: DOI: 10.17632/7skffnwgtb.1 Public record: Mendeley Data Creators: Narayana Raju, Shriniwas Arkatkar, and Gaurang Joshi, Sardar Vallabhbhai National Institute of Technology License: CC BY 4.0 The primary record documents four-camera, 0.5-second trajectory observations of 591 vehicles over a 535-metre section of Dumas Road, Surat, India. A supporting methodological publication is Data Driven Approach for Modeling of Driver Behavior Under Heterogeneous Traffic Conditions. The uploaded challenge data reorganizes the trajectories into seven-actor episodes; preparation then removes source identifiers, applies case-wise actor permutation and rigid coordinate transformation, exposes two frames, and derives new labels from five withheld frames. These transformations do not replace or obscure the public provenance above. Objective For every test case_id, predict motion_coupling_tree for the five hidden frames following the last public observation. A token such as A1~A4:T3 means that the undirected pair A1–A4 belongs to the hidden future coupling tree and reaches its smallest velocity gap at hidden future step 3. Tokens are ordered by increasing displacement-response cost, so the first token is the most tightly motion-coupled retained edge. Public files | File | Rows | Columns | Purpose | |---|---:|---|---| | train.csv | 1,485 | case_id, context_json, motion_coupling_tree | Labeled development cases. | | test.csv | 190 | case_id, context_json | Participant-disjoint evaluation cases with labels withheld. | | sample_submission.csv | 190 | case_id, motion_coupling_tree | Deterministic valid-format example, not a baseline. | case_id is an opaque alignment key. It contains no source vehicle ID, time, actor type, original row order, split clue, or target information. Input contract Every context_json object contains exactly: | Key | Value | |---|---| | dt | 0.5 seconds. | | actors | 'A1','A2','A3','A4','A5','A6','A7']. | | types | Seven vehicle classes aligned with the actor axis. | | feature_order | ['x','y','vx','vy','ax','ay']. | | history | Numeric tensor with axis order [frames, actors, features] and exact shape [2, 7, 6]. | | forecast_steps | 5. | The two public frames occur at relative times 0.0 and 0.5 seconds. Thus two frames contain one interval and span exactly 0.5 seconds. The five hidden future frames occur 0.5, 1.0, 1.5, 2.0, and 2.5 seconds after the final public frame. The six per-actor features are: | Feature | Unit | Meaning | |---|---|---| | x, y | metres | Centre position in a case-local rotated coordinate system. | | vx, vy | metres/second | Cartesian velocity. | | ax, ay | metres/second² | Cartesian acceleration. | Allowed type values are auto, bike, bus, car, truck, and lcv. The seven original actor slots are independently permuted and renamed A1–A7 in every case. A1 is not an ego vehicle and has no privileged role. Positions are translated around the group at the final public frame, and position, velocity, and acceleration are rotated together by a case-specific angle. Hidden target construction The target is derived exclusively from the five withheld motion frames. No pre-existing categorical annotation is read when labels are created. Let p_i(0) be actor i's position at the final public frame and p_i(k) its position at hidden future step k. Define its displacement response as: u_i(k) = p_i(k) - p_i(0), for k = 1,...,5. For every unordered actor pair (i,j), define motion-coupling cost: c_ij = sqrt((1/5) * sum from k=1 to 5 of ||u_i(k) - u_j(k)||²). Low cost means the two actors exhibit similar future displacement responses, regardless of their absolute positions. Also assign convergence time Tq, where q is the first hidden step minimizing ||v_i(k) - v_j(k)||. The deterministic tree procedure is: Calculate c_ij and Tq for all 21 unordered pairs. Sort pairs by (c_ij, smaller actor number, larger actor number). Run Kruskal's algorithm in that order. Retain an edge only if it does not create a cycle. Stop after six edges connect all seven actors. Serialize retained edges in the same increasing-cost order. This produces one temporal minimum-spanning tree per case. Individual edge choices are globally coupled: an otherwise strong pair is excluded if it would close a cycle. Output grammar A target contains six tokens. Examples: | Value | Meaning | |---|---| | A1~A4:T3 | A1–A4 is retained and has minimum velocity gap at hidden step 3. | | A2~A7:T5 | A2–A7 is retained and converges most closely at the final hidden step. | A multiple-token sequence is written as: A1A4:T3|A2A7:T5 Here, the A1–A4 displacement responses are more similar than A2–A7 because their token appears first. Each token must match A~A:T, where 1 <= i < j <= 7 and 1 <= q <= 5. Tokens are joined by | with no spaces. Edges must be unique and the complete submitted graph must be acyclic. A complete prediction has six edges, although a valid partial forest or NONE is accepted for honest partial credit. A malformed or cyclic row receives zero for that row. Submission Write ./working/submission.csv with exactly: | Column | Requirement | |---|---| | case_id | Every test ID exactly once. | | motion_coupling_tree | One valid ordered forest string. | The file must contain exactly 190 data rows. Missing, extra, blank, unknown, or duplicate IDs; changed column order; or any unexpected participant-defined columns are rejected. Motion-Coupling Tree Score For each valid row, remove :Tq suffixes to obtain the ordered edge lists, then compute: RankedEdgeF1 = 2 × LCS(hidden edges, predicted edges) / (number hidden edges + number predicted edges); EdgeF1, set F1 over phase-stripped edges; TimedEdgeF1, set F1 over complete edge-and-time tokens; and Exact, equal to 1 only when the complete ordered token list is exact. When both relevant lists or sets are empty, that component equals 1. The row score is: 0.40 × RankedEdgeF1 + 0.30 × EdgeF1 + 0.25 × TimedEdgeF1 + 0.05 × Exact. The final score is the mean over all 190 rows and is bounded to [0.0, 1.0]. Higher is better. There is no constant-output penalty, diversity bonus, corpus-level gate, or rule based on the number of unique predictions. Every row uses the same formula. Arbitrarily changing one output helps only when it creates real overlap with that row's hidden answer. Closest-work comparison The closest identified research is Park et al., [Leveraging Future Relationship Reasoning for Vehicle Trajectory Prediction, published at ICLR 2023 (OpenReview paper). Its future-relationship graph is an internal representation used with lane/map information to produce continuous multimodal trajectories, evaluated with trajectory-displacement criteria. This challenge changes what must be learned and submitted: | Dimension | Park et al. (ICLR 2023) | This challenge | |---|---|---| | Public evidence | Trajectory history plus lane/map structure and lane-waypoint occupancy | Exactly two motion frames; no lane or map input | | Role of pair relations | Stochastic latent/intermediate structure for a trajectory decoder | Deterministic supervised prediction target | | Required output | Continuous future trajectories | Six cost-ranked, time-labelled graph edges | | Global constraint | Relations support trajectory generation | Submitted edges must form one seven-node minimum-spanning tree | | Temporal relation label | Not the submitted benchmark object | First of five future steps minimizing each retained pair's velocity gap | | Evaluation object | Coordinate forecasts using trajectory errors | Edge identity, edge rank, convergence time, and exact structured sequence | The new learning problem is therefore not "trajectory prediction with a graph model." It is future graph-sequence forecasting: infer a hidden temporal relationship graph itself from a deliberately short, map-free observation, serialize it under a global combinatorial constraint, and receive partial credit separately for topology, rank, and timing. The source data and the tree algorithm are public, but neither determines a test answer without forecasting the withheld multi-agent response. Split and integrity design The raw dataset's existing development/evaluation roles are retained: 1,485 development cases and 190 later, participant-disjoint evaluation cases. The 101 physical vehicles appearing in evaluation do not occur in development panels. Original source IDs, absolute timestamps, source actor labels, original order, and pre-existing annotations are absent from prepared public data. The original seven actor slots are case-wise permuted, coordinates are group-centred and rotated, and new opaque case IDs are generated. There is zero train/test ID overlap and zero exact context overlap. The source workbook and raw uploaded file are not available in the solver runtime. External source matching is prohibited; use only the prepared public files. CPU requirement This challenge is designed for the CPU tier. The supplied offline reference calibrates 12 damped-acceleration settings on public training labels, forecasts five frames, and decodes a seven-node tree. It runs locally in about four seconds using approximately 105 MiB peak resident memory. It makes no network calls and uses no GPU. &nbsp;
> $700 Pool
> Closes in 10h 5m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Structured Abstract Protocol Reassembly

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7603w9zbbah7nwv5hxgghxys8e2t8k
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat masonjr's score of 0.146!

Full challenge description from page:

> Structured Abstract Protocol Reassembly Overview Biomedical abstracts often follow a rhetorical protocol: context establishes the research question, methods describe the study, results report the evidence, and concluding sections interpret the findings. In this challenge, that structure has been removed. For each abstract, you receive its title and 12–64 shuffled text units. Your task is to reconstruct the complete abstract by predicting: the original order of every text unit; the boundary of every section; and the original heading assigned to each section. The section count and heading vocabulary are not provided for test examples. Solving the task requires joint reasoning about local coherence, long-range discourse, biomedical study design, and variation in journal conventions. Compute setting This is a from-scratch, CPU-only sequence prediction challenge. Training and inference together must finish within 90 minutes using at most 10 CPU cores and 62 GB of RAM. Network access, external corpora, and pretrained model weights are not permitted. Data files | File | Contents | |---|---| | train.csv | Labeled examples: id, input_json, abstract_protocol_json | | test.csv | Unlabeled examples: id, input_json | | train_groups.csv | Opaque group IDs for leakage-aware local validation | | sample_submission.csv | Required submission columns and schema-valid placeholder outputs | | DATA_MANIFEST.json | Dataset dimensions and metric identifier | The training set contains 4,965 abstracts and the test set contains 629. The split is made over connected components rather than individual rows. Two rows are placed in the same component if they share a normalized journal label, share a normalized title, or have verified Jaccard similarity of at least 0.85 between their token 5-shingle sets; transitive links are closed with union-find. A deterministic hash assigns each entire component to one side, so no journal template, exact-title family, detected near duplicate, or transitive chain created by those relations can straddle training and test. The preparation audit also verifies disjoint journal labels, component IDs, and exact serialized inputs after generation. This prevents direct copying and reduces journal-style memorization as sources of test performance; it does not claim to remove every possible semantic relationship between distinct biomedical studies. train_groups.csv exposes the resulting opaque component identifier for training rows. Keep every shared group_id on one side when creating a development split so local validation preserves the same leakage barrier. Input format input_json contains an article title and a shuffled list of text units: { "article_title": "Example biomedical study", "shuffled_abstract_sentences": [ {"id": "u_31f...", "text": "A shuffled abstract unit."}, {"id": "u_a82...", "text": "Another shuffled abstract unit."} ] } Each unit has an opaque ID used only as a reference in the prediction. Neither the ID spelling nor the displayed list position encodes the answer. Units are indivisible: do not split, merge, rewrite, or generate text. The field name shuffled_abstract_sentences is part of the data schema. Its entries are punctuation-based text units and may occasionally contain more than one linguistic sentence. Every abstract contains 3–10 nonempty reference sections, with at least two sections containing multiple units. Prediction format Submit a UTF-8 CSV with exactly two columns in this order: id,abstract_protocol_json Every test ID must appear exactly once. Submission row order is arbitrary. abstract_protocol_json must be a JSON object with exactly two keys: { "sentence_order": ["u_a", "u_c", "u_d", "u_b"], "section_sequence": [ {"heading": "Background", "sentence_ids": ["u_a", "u_c"]}, {"heading": "Methods", "sentence_ids": ["u_d"]}, {"heading": "Results", "sentence_ids": ["u_b"]} ] } This shortened object illustrates the schema; actual examples contain at least 12 units. The prediction must satisfy all of the following conditions: sentence_order contains every input unit ID exactly once. section_sequence contains between 1 and 64 predicted sections. Every section contains exactly heading and sentence_ids. Every heading is a nonempty string of at most 512 characters. Every section contains at least one unit ID. Concatenating the section ID lists equals sentence_order exactly. No extra fields, duplicate JSON keys, unknown IDs, omitted IDs, or repeated IDs are allowed. The JSON payload may contain at most 131,072 characters. Use a CSV writer so quotes inside JSON are escaped correctly. Heading matching Predict the heading as it appears in the data. Distinctions such as Conclusion and Conclusions are meaningful. Before comparison, headings undergo Unicode NFKC normalization, case folding, whitespace trimming, and internal whitespace collapsing. Synonyms are not mapped, words are not stemmed, and punctuation is not removed. Repeated headings are allowed and represent separate sections. Evaluation The leaderboard score is the arithmetic mean of per-abstract scores. Scores range from 0 to 1, with higher values indicating better reconstruction. For each row: | Component | Weight | Definition | |---|---:|---| | Exact protocol | 40% | The complete ordered sequence of headings and ordered section ID lists matches | | Exact sections | 25% | Multiset F1 over (heading, complete ordered section-ID tuple) | | Labeled adjacency | 15% | Multiset F1 over consecutive unit pairs within each labeled section | | Labeled boundaries | 10% | Multiset F1 over consecutive section transitions, including both headings and boundary unit IDs | | Global triples | 10% | Multiset F1 over consecutive ID triples in the reconstructed abstract | Multiset F1 is: 2 × matched multiplicity / (predicted count + reference count) For one abstract, let E be exact-protocol accuracy (1 for an exact match, otherwise 0), S exact-section multiset F1, A labeled-adjacency multiset F1, B labeled-boundary multiset F1, and T global-triple multiset F1. The complete per-abstract equation is: row_score = 0.40 × E + 0.25 × S + 0.15 × A + 0.10 × B + 0.10 × T final_score = arithmetic mean(row_score over every test abstract) The five components are constructed as follows: E: compare the complete ordered list of normalized headings and ordered section-ID tuples. It is 1 only when the two lists are identical. S: form a multiset containing one (normalized heading, complete ordered section-ID tuple) item per section. A: for each section, form (normalized heading, left_ID, right_ID) for every consecutive pair inside that section. B: for every consecutive pair of sections, form (left normalized heading, last left ID, right normalized heading, first right ID). T: form (ID_i, ID_i+1, ID_i+2) for every consecutive triple in sentence_order. Apply the stated multiset-F1 formula independently to S, A, B, and T, then combine the five values exactly once with the weights above. The weights sum to 1. Empty/empty component multisets score 1; empty/nonempty component multisets score 0. Why the metric uses these weights The required output is one complete protocol: every unit must be in the correct global position, every boundary must be correct, and every section must have the correct heading. Exact protocol therefore receives the largest single weight (40%) because it measures the actual end-to-end deliverable and prevents a collection of locally plausible fragments from being treated as equivalent to a usable reconstruction. It is binary because there is only one condition under which the complete reconstructed protocol is correct. The exact term does not make a near-perfect row score zero. It removes only its 0.40 exact-match contribution; the remaining 60% is deliberately graduated. Exact-section F1 rewards intact rhetorical blocks, adjacency and boundary F1 localize ordering and segmentation progress, and global-triple F1 rewards heading-independent discourse order. Giving these partial measures the majority of the score preserves useful ranking among imperfect systems, while the 40% plurality ensures that solving the full joint task is materially more valuable than accumulating overlapping local matches. The 25/15/10/10 allocation orders partial evidence by task significance: a complete correctly labeled section is stronger evidence than an internal pair, a section transition, or a heading-independent triple. The components overlap by design at different structural scales, so none of the local components is allowed to dominate the exact end-to-end criterion. If both multisets are empty, the component score is 1. If only one is empty, it is 0. Exact-section matches do not depend on the section's predicted position; the exact protocol, boundaries, and global triples capture ordering. A fully correct prediction scores 1.0. Copying every input ID provides no automatic coverage credit. Recovering headings without recovering their complete ordered sections earns only limited credit. Invalid submissions The following errors invalidate the entire submission and produce a score of 0: incorrect or reordered CSV columns; malformed CSV structure; missing or extra test IDs; or duplicate test IDs. Malformed JSON or a structurally invalid prediction produces a score of 0 for the affected row only. Other rows remain scoreable. Non-finite JSON constants such as NaN and Infinity are invalid. Allowed information Models may use only the released contestant files. All model fitting, lexicon construction, feature extraction, and calibration must occur within the submitted solver. Do not use network access, external datasets, outside websites, identifier lookup, pretrained weights, hidden annotations, or synthetic training labels. Test examples may be used only for inference and may not be used for fitting or tuning. &nbsp;
> $700 Pool
> Closes in 3h 52m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Otolith Cohort Panel Match and Consensus Signature

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78794dae60mq41mqsnffg1118e2hpe
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat shashikantgupta's score of 0.268!

Full challenge description from page:

> Otolith Cohort Panel Match and Consensus Signature Overview and Objective This is a sequence-to-sequence / NLP challenge. Every column is text: the input is one free-text query string and the output is a generated JSON string holding an ordered token sequence. No numeric feature matrix is released, by design — the growth measurements reach the solver only as words. Atlantic cod lay down one growth increment in the otolith each year, and the width of that increment records how good that year was for the fish. Fish born in the same year grow in step with one another: a cohort shares a growth signature that outlives the noise of any single individual. Fisheries scientists exploit that synchrony to tell which archived otoliths belong together. This benchmark turns the procedure into a text task; it does not claim to date any real specimen. You are predicting two things per case, and they are separate pieces of work: which candidate panel in the archive was drawn from the same birth cohort as the query panel, or NONE if the archive holds no such panel; and the consensus growth signature of the query panel itself, as an ordered sequence of six token IDs. The second is not recoverable from the first. The query lists its fish one by one and never shows their consensus, and the candidate panels belong to other draws of fish, so the signature has to be built from the query panel rather than copied from anywhere in the case. The signature is written, not chosen: it is an ordered sequence of six tokens that the solver composes position by position, and no candidate in the case carries it. That is the generation half of the task; the panel selection is the retrieval half. Both are emitted as one JSON string. query → prediction_json {"cohort_match":{"match":{"A1":"P04"},"signature":["tikaot","zekali","jikayu","agkaen","tirinu","jirida"]}} Preparation converts every measured increment width to a stable opaque token and drops the population, the calendar year, the cohort, and every fish identifier. These transformations define the benchmark representation; they are not claimed to prevent reconstruction, and identifying the source records is prohibited by the rules below. Dataset The public files are: train.csv — 1070 training cases with answers. test.csv — 240 test cases without answers. sample_submission.csv — one structurally valid row per test case, naming that case's own archives with NONE and an empty signature. Its score is 0.0088. The hidden evaluator file answers.csv is not solver-visible; it carries the string columns id and prediction_json. Each row is one case: id — type string; opaque case identifier, oto_ followed by 12 hex characters. query — type string; a fixed instruction, then the query panel, then the archive: the query panel is ten bracketed groups, one per fish, each holding six tokens in age order — the fish's growth profile from age 1 to age 6; the archive is written A1:: P01() P02() …, holding between 6 and 12 candidate panels; each candidate is summarised by its own six-token consensus. prediction_json — type string; train only. The target object described under Submission. Tokens are drawn from a global vocabulary of 48 words. The same token always denotes the same measured growth value at the same age position, in every case and in both splits. A token that appears at position 3 never appears at any other position. Tokens are contest encodings — not species names, specimen numbers, identifiers, or credentials. Exactly one candidate in an archive can come from the query panel's cohort, and in 42 of the 240 test cases none does, so NONE is a real answer rather than an escape hatch. Split integrity Whole (population, cohort) groups are assigned to a visibility pool before a single case is generated, and every panel in a case is drawn from within one pool. Consequently: 114 cohort groups: 80 train, 17 public, 17 private. No group appears in two pools, and no group was moved between pools to hit a case count — the split is fixed by group before any case exists, and the pools differ only in how many panel pairs they draw from the groups they already own. No fish, and no cohort, is ever seen in both train.csv and test.csv: 3428 fish in train, 784 and 870 in the two test halves, with 0 shared between any two pools. The test set is scored in two halves built from disjoint cohort groups, so the halves share no fish and no panel. Candidate panels inside a case always come from the same population as the query, so population identity is never the shortcut. Residual risk, stated plainly: neighbouring cohorts of one population experienced overlapping years at sea, so a train cohort and a test cohort can still resemble each other without sharing a fish. Distractor cohorts inside a case are kept at least three years away from the query cohort, but nothing prevents that closeness across the split. Submission Write a CSV with exactly two columns in this order: id,prediction_json Every prediction_json value must decode to an object with the single key cohort_match, whose value has exactly the two keys match and signature: {"cohort_match":{"match":{"A1":"P04"},"signature":["tikaot","zekali","jikayu","agkaen","tirinu","jirida"]}} match must carry exactly the archive names the case supplies. Each value is either a panel id of the form P07 or the literal NONE. signature must be an array of at most six token strings. It may be empty to abstain. Values are matched after trimming whitespace; archive names and panel ids are case-insensitive, tokens are lowercase. Rows may appear in any order, but the submission must contain all 240 test ids exactly once. Use sample_submission.csv as the template. The grader raises an error on missing columns, duplicate ids, or any test id absent from the submission. A row scores 0 — without failing the run — when its prediction_json is malformed JSON, is missing or adds a key, names an archive the case does not have, carries a panel id that is not well formed, holds a signature longer than six tokens, or holds a token outside the vocabulary. Evaluation Higher is better. The metric is CPMS (Cohort Panel Match Score), bounded to [0, 1]. Let N be the number of scored cases. For case c, with levenshtein the token-level edit distance — each insertion, deletion or substitution of one whole token costs one, and characters inside a token are never compared: A = correct archive selections / number of archives E = 1 if the predicted signature equals the gold signature exactly, else 0 Q = 1 if E = 1 and every archive selection is correct, else 0 T = 1 - levenshtein(predicted, gold) / max(len(predicted), len(gold), 1) row_score = 0.05 * A * 2 + 0.90 * Q + 0.05 * T * 2 CPMS = (1 / N) * sum_c row_score_c Nine tenths of the weight pays only for the complete capsule — the archive right and the signature exact. The two squared side terms keep the ordering strict, so a submission whose signature is closer in token edit distance always outranks one that is further away instead of both collapsing to zero. The score is bounded to [0, 1], the sample_submission.csv placeholder scores 0.0088, and the gold answers score exactly 1. Reference points Published so a mid-range score is not mistaken for signal. All are scored on the full test set. | Predictor | CPMS | |---|---:| | All NONE, empty signature — the sample submission | 0.0088 | | Random panel, signature copied from one query fish | 0.0058 | | Token-overlap heuristic on the raw tokens | 0.0087 | | Shape-matching oracle that is told what the tokens encode | 0.1209 | The first three treat the tokens as bare symbols and go nowhere. The fourth is an oracle: it is handed the meaning of the encoding, which a solver has to work out from the training pairs instead. Read it as the bar a good method should be aiming at, not as a limit — it is far below the 1.0 a full solution scores. Absolute numbers are low by design. Recovering the archive alone is worth 0.05; recovering the signature alone earns only the edit term. Compute This challenge runs on CPU. Nothing in the pack needs a GPU: the pipeline that builds it and the scorer that grades it import only pandas, numpy and the standard library, and the strongest reference predictor published above is plain NumPy arithmetic over the token bags. Building the whole pack takes about five seconds and scoring the test set about one second on an ordinary CPU. A solver is free to bring heavier machinery, but the task does not reward it: the work is reading two bags of tokens and committing to one capsule, not training on volume. A CPU-only entrant is not at a disadvantage. Rules Use only the supplied public challenge files. Prohibited: Web lookup of any kind, during development or at run time. External copies of the source growth-increment corpus, or any otolith, fisheries, or growth-chronology database. Reverse-identification of the source records — recovering populations, calendar years, cohorts or specimen identifiers by any means. Pretrained assets built on the source corpus, or any resource that embeds records from it. Hardcoded per-id answers, private-file access, and grader exploitation. Treating tokens as secrets, keys or credentials; they are none of those. Emitting columns other than id and prediction_json. General-purpose code and libraries already present in the execution environment are permitted, provided they neither contain nor retrieve source records or source-specific pretrained assets. The complete solution must run offline, with no internet access and no package installation at run time. &nbsp;
> $700 Pool
> Closes in 6h 3m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.

## Multi-Goal Proof Program Generation with Cache Constraints

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cdmqbvy5kk02z87b3b8rvbx8c6shg
- DOMAIN exactly as displayed: Sequence To Sequence
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat safwan188's score of 0.632!

Full challenge description from page:

> Multi-Goal Proof Program Generation with Cache Constraints Overview Compact reasoning services often cannot keep every intermediate claim in working memory. They must decide which natural-language statements are premises, which statements are derived conclusions, which derivation should run next, and which derived statements must remain cached for later steps. A plausible proof graph can still fail in production if a required intermediate is evicted too early. This challenge models that compilation problem. Each episode contains two science questions and their target hypotheses, plus one shuffled bank containing source facts, intermediate conclusions, the two final hypotheses, and same-topic donor statements. You must return one complete executable proof program for both goals. Every program step names one to four exact bank statements as premises, one exact bank statement as its conclusion, and the derived statements retained after the step. Every episode uses the same fixed cache capacity of exactly three derived-statement slots. The cache_capacity field repeats the value 3 so programs can validate the execution contract; it does not indicate that capacity varies between episodes. The source is a human-authored collection of science questions, facts, and multi-step entailment trees. Preparation filters source proofs to three through eight annotated steps, deduplicates each premise set, removes steps outside the backward dependency closure of the target hypothesis, clusters related questions into semantic families, allocates whole families to one split, pairs two proofs inside a family, and adds donor statements only after the split. The resulting task is not ordinary question answering or proof generation: the required output is an executable dual-goal cache program whose dependency and retention decisions are checked step by step. The challenge is CPU-only. The prepared action space is bounded, and a sparse or compact-encoder pipeline can train and decode within the 90-minute limit on 10 CPU cores and 62 GB RAM. Dataset The prepared release contains: train.csv: 1,788 labeled episodes from 36 semantic families. test.csv: 660 unlabeled episodes from 12 different semantic families. sample_submission.csv: one legal empty program for every test episode. answers.csv: private grading state. This file is not available to contestants. manifest.json: public release counts and cache capacity. All questions from a semantic family remain in one partition. Proof pairing, donor mining, and episode construction occur after family allocation. Exact episode IDs, questions, and target hypotheses do not cross the train/test boundary. Features Fields in train.csv: episode_id: string. Opaque unique episode identity. goal_1_question: string. First source science question. goal_1_hypothesis: string. First natural-language claim that the program must derive. goal_2_question: string. Second same-family science question. goal_2_hypothesis: string. Second natural-language claim that the program must derive. statement_bank_json: string containing a JSON array of unique natural-language statements. The array mixes usable facts, usable intermediate conclusions, both goals, and same-topic donors. execution_contract_json: string containing a JSON object with integer cache_capacity (always 3 in this release), integer goal_count, integer max_steps, and string premises_per_step. The capacity field is constant and is included for explicit program validation, not as a varying episode feature. predicted_program: string containing the target JSON program described below. This is the supervised target column and appears only in training. The feature columns in test.csv exactly match the feature columns in train.csv. predicted_program is the sole training target and is therefore absent from test.csv. Fields in sample_submission.csv: episode_id: string. Must match one test identity exactly once. predicted_program: string containing a JSON array. The sample uses an empty array. Private answers.csv contains episode_id, predicted_program (the actual gold JSON program, using the same column name and format as submissions). There are no required helper columns. The grader derives leaf facts, dependency edges, the two terminal goals, and the maximum step count from this goal-pruned gold program; cache capacity is always three. Program Format and Execution predicted_program must decode to a JSON array of zero or more step objects. Every step must have exactly these keys: premises: an array of one to four distinct exact strings from that episode's released statement bank. Premise order does not matter. conclusion: one exact bank string. A conclusion may appear at most once in the program. retain: an array of distinct exact bank strings containing at most three entries, matching the fixed cache_capacity value of 3 in every episode. Leaf facts are streamable and do not occupy the derived-statement cache. A derived statement can be used as a later premise only if it is present in the cache immediately before that later step. For one step to execute: its conclusion and unordered premise set must match one hidden annotated entailment edge; every intermediate premise must already be cached; retain must be a subset of the previously cached derived statements plus the new conclusion; only derived conclusions, not leaf facts or donor statements, may be retained; and the retained set must contain at most three derived statements. This limit is identical for all episodes. After a valid step, the cache becomes exactly its retain set. Final hypotheses are recorded as completed goals even when they are not retained. Execution stops at the first semantically invalid step. Schema errors such as malformed JSON, more than 16 steps (the global limit), or duplicate conclusions reject the submission. Structurally valid but incorrect strings or dependencies are prediction errors, not parser errors: they cannot match a gold edge or execute it. Matching conclusions and edges still receive the partial credit defined below. A program exceeding its episode-specific step budget receives zero for that row. Consequently, moving a syntactically valid program to another episode does not abort scoring; it is scored against that episode's gold proof. JSON whitespace and object-key order do not affect scoring; step-array order does. Evaluation The score is the mean row score and is bounded to the interval from 0 to 1. For each row define: Goal fraction G: the fraction of the two hypotheses successfully derived before execution stops. Executed coverage C: the fraction of hidden gold conclusions successfully derived before execution stops. Execution utility U: 0.70 G + 0.30 C. Dependency edge F1 E: set F1 between submitted and gold edges. An edge is the exact conclusion string paired with its unordered exact premise-string set. Conclusion F1 N: set F1 between submitted and gold conclusion strings. Complete certificate X: 1 only when the program has exactly the gold number of steps, contains exactly all gold edges, executes every gold conclusion, and derives both goals; otherwise 0. Set F1 uses 2 precision recall / (precision + recall). It is 0 when only one set is empty. The row score is: 0.55 U + 0.20 E + 0.15 N + 0.10 X These proportions follow the operational priority of a cache-constrained proof compiler: 55% execution utility is the majority component because a program's primary purpose is to run successfully under the cache contract, rather than merely resemble an annotated proof. Within execution utility, goals receive 70% because deriving both requested hypotheses is the user-visible outcome. Executed coverage receives 30% so a program that reaches one goal through a short or accidental path cannot ignore most required reasoning. Thus goals contribute 38.5% and coverage contributes 16.5% of the complete row score. 20% dependency-edge F1 directly measures whether the submitted premise sets justify their conclusions. This preserves credit for correctly inferred proof structure even if one ordering or retention mistake stops execution early. 15% conclusion F1 is deliberately smaller than edge F1. Recognizing which statements are derived is useful progress, but it omits both their justifications and cache schedule and therefore cannot be leaderboard-competitive by itself. 10% complete-certificate credit separates fully correct end-to-end programs from collections of individually plausible steps. It requires exact graph recovery, complete execution, and both goals, while leaving 90% graded continuously so one localized error does not erase all signal. Consequently, 75% of the score is tied directly to successful execution or exact dependency recovery, and another 10% requires complete executable correctness. Identifying conclusion-like statements alone can earn at most the intentionally limited 15% conclusion component. Optimizing the metric therefore prioritizes the same behavior as the task objective: derive both goals through valid dependencies while keeping every required intermediate available within the fixed cache. Submission Format Submit a CSV with exactly two columns in this order: episode_id,predicted_program Every test ID must appear exactly once. JSON must be CSV-escaped. A complete two-row example is: episode_id,predicted_program cache_001,"[{""premises"":[""fact alpha"",""fact beta""],""conclusion"":""derived claim"",""retain"":[""derived claim""]}]" cache_002,"[]" The example strings are illustrative; actual predictions must use exact strings from each row's released bank. Requirements Use CPU computation only, with at most 10 CPU cores and 62 GB RAM. Finish end to end within 90 minutes. Fit vectorizers, models, thresholds, and calibration only on train.csv. Produce one deterministic program per test episode. Use only exact row-local statement-bank strings in program fields. What Not To Use Do not use GPU, CUDA, TPU, or another accelerator. Do not access answers.csv, private grading state, hidden targets, or platform internals. Do not reverse-map questions or statements to source corpora, a search engine, or an external table of published proof trees. Do not fit or adapt models, vectorizers, vocabularies, indexes, thresholds, or calibrators on the complete test corpus. Documented row-local decoding is allowed. Do not use internet retrieval to recover source IDs, original split labels, or proof annotations. &nbsp;
> Closes in 2h 37m
> 12 / 12 continuing slots

Inspiration note: Useful because it turns messy source evidence into an ordered, validated token or text sequence.


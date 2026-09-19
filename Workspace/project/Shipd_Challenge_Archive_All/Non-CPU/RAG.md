# Non-CPU RAG Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed Non-CPU examples in this document: 10

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.

## In-Force Safety-Statement Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77cfqb1bjbetev6abt65qat58a576j
- DOMAIN exactly as displayed: RAG
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat nolifecoderz's score of 0.516!

Full challenge description from page:

> Overview
> You are given a collection of official product-safety documents for a set of products. Each product's safety information is re-issued over time as a sequence of dated revisions, and different suppliers may maintain their own documents for the same product. Over successive revisions, individual safety statements are added, removed, or re-worded, and the exact set of statements "in force" changes.
> Crucially, the revision dates and ordering are stated only inside the document prose, in ordinary natural language (e.g. "put into effect in the spring of 2018, superseding the prior 2016 issuance"). There is no separate date column and no version number. All product, supplier, section, and statement identifiers are opaque codes with no external meaning.
> Your task: for each query — a product, a safety section, and an as-of date — output the exact SET of atomic safety statements that were in force on that date, selected from a candidate pool supplied with the query.
> This is not question answering. The same query at two different as-of dates has different answers, and the correct set typically mixes statements that entered the document at different revisions — so simply returning "the most recent revision's statements" scores near zero (see Evaluation).
> Files
> corpus/products/<product_id>/versions.jsonl — the revision documents. One JSON object per line with fields: doc_id (string, opaque document id), product_id (string), section (string), and text (string). The text is continuous prose: a natural-language issuance/supersession note followed by the section's safety content as it read in that revision. The documents for a product are shuffled — the revision order is not given and must be inferred from the prose dates.
> statements/pool.jsonl — the atomic candidate statements referenced by the queries. One JSON object per line with fields: stmt_id (string, opaque), product_id (string), section (string), and text (string, the normalized atomic claim). A statement's claim wording is a normalized paraphrase — it is not a verbatim substring of the revision documents, and near-duplicate re-wordings of the same clinical point appear as distinct stmt_ids.
> train.csv — labeled queries. Columns:
> query_id (string) — unique query identifier.
> product_id (string) — the product this query is about; maps to corpus/products/<product_id>/.
> section (string) — one of contraindications, boxed_warning, interactions, warnings.
> as_of_date (string) — the as-of date in ISO YYYY-MM-DD format. This value is exact (not obfuscated).
> candidate_stmt_ids (string) — pipe-delimited (|) list of stmt_ids forming this query's candidate pool (typically a few dozen ids, more for products with deep revision histories). Your answer must be a subset of these.
> gold_stmt_ids (string) — pipe-delimited list of the stmt_ids that were in force on as_of_date. This is the training label; it is a subset of candidate_stmt_ids and may be empty.
> test.csv — unlabeled queries. Same columns as train.csv except gold_stmt_ids is absent.
> sample_submission.csv — a valid baseline submission (predicts the full candidate pool for each query). Columns: query_id (string), pred_stmt_ids (string).
> Submission format
> Produce submission.csv with exactly two columns:
> query_id (string) — one row for every query_id in test.csv, no more, no fewer, no duplicates.
> pred_stmt_ids (string) — pipe-delimited (|) list of predicted in-force stmt_ids for that query. Each predicted id should be from that query's candidate_stmt_ids; ids outside the pool are ignored. An empty string is a valid prediction (predict nothing).
> Evaluation
> Predictions are scored by a statement-weighted set-F1, averaged over test queries. For each query, let P be your predicted set (intersected with the candidate pool) and G the gold in-force set. Each statement s carries a weight w(s):
> w(s) = 0.15 if s is still present in the product/section's most recent revision (a stable statement), and
> w(s) = 1.0 otherwise (a statement that has since been superseded).
> Then, with W(A) = Σ_{s∈A} w(s):
> weighted_precision = W(P ∩ G) / W(P)            (= 1 if P and G are both empty; 0 if only P is empty)
> weighted_recall    = W(P ∩ G) / W(G)            (= 1 if G is empty)
> F1(query)          = 2·wp·wr / (wp + wr)         (0 if wp + wr = 0)
> final score        = mean of F1(query) over all test queries, clipped to [0.01, 1.0]
> The weighting means that correctly recovering the superseded statements in force on the as-of date — the ones that differ from today's document — dominates the score. Returning the current revision's statements, or the entire candidate pool, both score poorly.
> The grader is strict: a submission that omits a required query_id, contains a duplicate query_id, or is missing a required column is rejected.
> Notes and constraints
> The train/test split is by product: test products are disjoint from train products, so a solution cannot memorize per-product answers and must generalize the temporal-reasoning skill.
> Identifiers are opaque and re-keyed; there is no external resource to look them up in.
> Revision dates live only in the document prose and are phrased in varied natural language; they are not recoverable from file names, line order, or document ordering.
> Determining which revisions contain a given candidate statement is a fuzzy matching problem: wording drifts across revisions, and near-duplicate re-wordings are distinct candidates that were in force in different date ranges.
> A single candidate statement can be in force at one as-of date and not at another.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Deidentified Weather Report Pair Retrieval

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cfwkmrp521012kgkn9kt5ms8a5sg9
- DOMAIN exactly as displayed: RAG
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
> Weather episodes often contain multiple event reports from the same weather system. In this RAG and NLP benchmark, each row is a closed candidate-ranking case: one deidentified query report profile is paired with eight deidentified candidate report profiles. Your task is to rank the eight candidates so the candidate report from the same hidden episode grouping as the query appears first.
> A report profile is a generated, non-verbatim text summary of coarse evidence cues in a single event report. It describes broad language patterns such as water, wind, winter, infrastructure, human exposure, response activity, impact mechanism, affected setting, extent, measurements, and timing language using categorical phrasing rather than original narrative sentences. An event family is a coarse string label for the general weather-impact type, such as a flood-like, wind-like, hail-like, winter-like, heat-like, or coastal-like family.
> The participant-facing data retains only these coarse event-family labels and generated report profiles. It removes raw report narratives, state and county names, exact locations, exact timestamps, raw source names, event IDs, episode IDs, and hidden impact measurements. Strong systems should combine retrieval, representation learning, prompt engineering, and fine-tuning to match related evidence under this deidentification. Candidate sets are built with close distractors that often share the same coarse profile signature, so broad event-family or keyword matching alone is not expected to perform well.
> The scored target is only the row-local rank of candidate IDs. The task does not ask for impact severity, property damage, casualty counts, duration, event type, or weather-category labels.
> Dataset
> The prepared public dataset contains four files:
> public/train.csv: CSV training rows with a query profile, eight candidate profiles, and the relevant candidate ID.
> public/test.csv: CSV scoring rows with the same query and candidate fields, but without the relevant candidate ID.
> public/sample_submission.csv: CSV example with the required submission columns. It is valid but intentionally weak.
> public/submission_schema.md: Markdown reference for the required columns, row-matching rule, accepted ranking separators, and malformed-value behavior.
> Both train.csv and test.csv include case_id, query fields, and eight candidate blocks numbered candidate_0 through candidate_7. Each row always has exactly eight candidate IDs.
> case_id (string): opaque row identifier used to join submissions to test cases.
> query_event_family (string): coarse weather-impact family for the query report.
> query_report_profile (string): generated deidentified evidence profile for the query report.
> candidate_i_id (string): opaque identifier for candidate i in that row.
> candidate_i_event_family (string): coarse weather-impact family for candidate i.
> candidate_i_report_profile (string): generated deidentified evidence profile for candidate i.
> relevant_candidate_id (string, train only): candidate ID from the same hidden episode grouping as the query report.
> Evaluation
> Submissions are scored from 0.01 to 100, higher is better. Each row is scored by reciprocal rank:
> row_score = 1 / rank_of_relevant_candidate
> row_score = 0 if the relevant candidate is not in the submitted ranking
> score = 100 * mean(row_score over test rows)
> The final score is clipped into the inclusive range 0.01 to 100. Candidate IDs outside the row-specific candidate set are ignored after the CSV contract is satisfied. Wrong columns, missing IDs, extra IDs, duplicate IDs, and direct target-column submissions are rejected.
> Submission
> Submit one CSV file named submission.csv with exactly one row for every case_id in public/test.csv. The required columns, in order, are case_id and ranked_candidate_ids. List candidate IDs from most to least relevant, separated by spaces, commas, semicolons, or pipes. Each ranked_candidate_ids value is a string containing one to eight candidate IDs from that row. A full ranking of all eight candidates is recommended. Shorter rankings are valid, but omitted candidates receive no reciprocal-rank credit if the relevant candidate is omitted. Copying public/sample_submission.csv to submission.csv is a valid weak fallback.
> Example submission rows:
> case_id,ranked_candidate_ids
> seer_te_00000_139d8ac10e,cand_te_951ad3022c08 cand_te_3a7bfedd44ed cand_te_f084d27f6a1d cand_te_06c494705716 cand_te_8f387e803646 cand_te_754810ebba8b cand_te_f29e7819197e cand_te_1876e2b68611
> seer_te_00001_5ce6e291ca,cand_te_b97b4f4f9698 cand_te_4c92a3c756c8 cand_te_c8ce9a4eb128 cand_te_c50ae1b635ff cand_te_d97f2cfc2b20 cand_te_59dd2a923530 cand_te_30ff9a774224 cand_te_c53033254288
> What Not To Use
> Allowed: retrieval over the public candidate profiles, pretrained language models, embeddings, fine-tuning on public/train.csv, prompt engineering over the public files, and tabular or linear rankers trained only on the public prepared files.
> Prohibited: querying source archives, search engines, news archives, external weather databases, or any other retrieval source to look up hidden episode groupings for test rows. Do not use raw event IDs, raw episode IDs, hidden answer files, private test labels, row order, file metadata, or manual lookup to reconstruct the targets. OCR and object detection are not part of this benchmark.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Comparative Afterlife Passage Bridge Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78azcv6w30gwmgk899nzdrhn8brqcp
- DOMAIN exactly as displayed: RAG
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Given three ordered context passages and six retrieved candidate passages, assign exactly one candidate to each of two missing positions. The reconstructed sequence has five positions: visible passage, missing gap 1, visible passage, missing gap 2, visible passage.
> The records come from historical public-domain writing about death, the soul, immortality, judgment, rebirth, and imagined post-death destinations. The benchmark does not ask whether any metaphysical claim is true. It measures source-local discourse reconstruction across philosophical dialogue, scriptural prose, historical exposition, theological prose, and narrative verse.
> This is a retrieval-augmented language task. Candidate text is stored in a separate public passage corpus and is referenced by opaque passage IDs. Content-bearing terms, names, and numbers have been privacy transformed, so useful systems must combine retrieval, local continuity, discourse cues, repeated concepts, and joint assignment rather than searching for the original wording.
> Dataset
> All public files are under ./dataset/public/.
> train.csv: 279 labeled reconstruction rows.
> test.csv: 257 held-out reconstruction rows from entirely held-out works.
> passage_corpus.csv: 2,609 candidate passages referenced by train and test rows.
> sample_submission.csv: a valid weak submission with the required schema.
> The train and test splits share no source works, candidate passage IDs, or exact visible contexts. Every candidate passage used in test appears in exactly one test row.
> train.csv and test.csv
> id string): opaque reconstruction-row identifier.
> prompt string): row-level task instruction.
> visible_context_json JSON string): an object with slot_0 through slot_4. slot_1 and slot_3 contain the missing-gap markers; the other three values contain transformed context passages.
> candidate_ids_json JSON string): a list of exactly six distinct passage IDs available for the row.
> answer_format_json JSON string): the required answer keys and candidate-assignment contract.
> answer_json JSON string, train only): the correct candidate assignment for gap_1 and gap_2.
> passage_corpus.csv
> passage_id string): opaque candidate passage identifier.
> passage_text string): privacy-transformed candidate text.
> Tokens such as lex_12ab34cd are stable opaque lexical symbols. They may repeat where the same transformed term recurs, but they are not labels and do not encode candidate correctness. The <num> marker replaces source numbers.
> Target
> For every test row, retrieve the six candidate texts from passage_corpus.csv and produce this object:
> {"gap_1":"bridge_0123456789abcd","gap_2":"bridge_fedcba98765432"}
> The two values must be different and must both occur in that row's candidate_ids_json list. gap_1 is the passage between slot_0 and slot_2; gap_2 is the passage between slot_2 and slot_4.
> Evaluation
> For one row, define:
> gap_1_correct: 1 if the first assignment is exact, otherwise 0.
> gap_2_correct: 1 if the second assignment is exact, otherwise 0.
> set_overlap: the number of correctly retrieved gold passages, ignoring which gap they were assigned to, divided by 2.
> exact_pair: 1 only when both gap assignments are exact, otherwise 0.
> Because there are exactly two distinct submitted passages and two distinct gold passages, set_overlap can only be 0, 0.5, or 1. exact_pair can equal 1 only when both gap-correctness values and set_overlap also equal 1. The four weighted components are therefore jointly bounded, and row_score always lies in [0, 1]; an exact reconstruction scores exactly 1.0.
> The row score is:
> row_score = 0.25 * gap_1_correct
> + 0.25 * gap_2_correct
> + 0.20 * set_overlap
> + 0.30 * exact_pair
> The final score rewards both average quality and robustness:
> score = 0.65 * mean_row_score
> + 0.15 * weakest_form_family_mean
> + 0.10 * weakest_topic_density_mean
> + 0.10 * weakest_negative_hardness_mean
> For each robustness axis, weakest means the minimum row-score mean among the groups present in the scored partition. The hidden groups are derived from source form, local topic density, and distractor similarity. Scores range from 0 to 1, and higher is better.
> Submission Format
> Submit exactly two columns in this order:
> id,answer_json
> aft_0123456789abcdef,"{""gap_1"":""bridge_0123456789abcd"",""gap_2"":""bridge_fedcba98765432""}"
> aft_fedcba9876543210,"{""gap_1"":""bridge_aaaabbbbccccdd"",""gap_2"":""bridge_11112222333344""}"
> Requirements:
> Include every test id exactly once and no other IDs.
> answer_json must be valid JSON with exactly gap_1 and gap_2.
> Both values must be distinct candidate IDs allowed for that row.
> Do not add columns or rows.
> What Not To Use
> Do not search the web, public ebook repositories, or external corpora to identify or recover the original passages.
> Do not reverse engineer opaque lexical symbols into source words, authors, titles, or editions.
> Do not use source filenames, source order, hidden preparation artifacts, private answers, or challenge-generation internals.
> Do not infer answers from row IDs, passage IDs, candidate-list position, or global option frequency alone.
> Do not hardcode test IDs, candidate assignments, exact public rows, or manually reconstructed source sequences.
> Do not use hosted prediction APIs or private/gated data.
> Systems may train or fine-tune open local models using only the released public files. Retrieval indexes, lexical models, sequence models, and learned joint assignment methods are allowed.
> Expected Output
> Write the completed file to ./working/submission.csv.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Inverse Evidence Program Induction for Multi-Turn Retrieval

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7d4jkasdmpcs4qccw5x76mhd8bnzgd
- DOMAIN exactly as displayed: RAG
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: generative
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Retrieval-augmented systems often represent supporting evidence as a structured state connecting conversation turns to documents.
> In multi-turn settings, this evidence state can become corrupted when:
> relevant evidence is omitted;
> distractors are inserted;
> evidence is copied to the wrong turn;
> evidence assignments are swapped between related turns;
> stale retrieval state is carried forward;
> several turn-document assignments are modified together.
> This challenge formulates the problem as inverse evidence program induction.
> For each case, you are given:
> an ordered multi-turn information-seeking conversation;
> a shuffled pool of exactly 64 candidate documents;
> an opaque domain token;
> a corrupted turn-to-document evidence program.
> The correct evidence state is hidden.
> Your task is to infer a sparse structured patch that transforms the observed corrupted program into the hidden correct program.
> Formally, let:
> C = observed corrupted evidence program
> Z = hidden correct evidence program
> P = predicted inverse repair program
> The objective is to predict P such that:
> Apply(C, P) = Z
> This is not a conventional single-query retrieval task. A strong solution must jointly model:
> semantic relevance;
> conversational history;
> cross-turn evidence relationships;
> missing and injected evidence;
> structured graph edits;
> valid constrained output generation.
> The benchmark evaluates both whether the predicted edit program is correct and whether applying it recovers the correct hidden evidence state.
> Research Formulation
> The task can be viewed as recovery of a latent structured state from a partially corrupted observation.
> The latent state is a bipartite evidence graph:
> conversation turns ↔ supporting documents
> The observed input contains a corrupted serialization of that graph.
> Instead of directly predicting the complete graph from scratch, participants must induce its inverse transformation program: a sparse sequence of additions and removals that explains how the observed state should be corrected.
> This formulation jointly evaluates:
> Conversational Retrieval
> Determine which documents support each turn while accounting for previous turns and conversational dependencies.
> Latent State Reconstruction
> Recover the hidden evidence structure underlying a noisy or incomplete observed program.
> Cross-Turn Reasoning
> Detect evidence that has been misplaced, reused incorrectly, copied, contaminated, or swapped between turns.
> Inverse Program Prediction
> Predict the edit operations required to transform the corrupted program into the hidden target program.
> Constrained Structured Decoding
> Generate a syntactically and semantically valid patch under strict execution rules.
> The evaluation set contains heterogeneous corruption profiles. Only one profile preserves the number of documents assigned to every affected turn. Therefore, preserving the observed per-turn document count is not a universal solution.
> Evidence-State Representation
> Let the ordered conversation turns be represented by tokens such as:
> TA
> TB
> TC
> TD
> Let the case-local candidate documents be represented by tokens such as:
> DAA
> DAB
> DAC
> ...
> An evidence edge:
> (TA, DAB)
> means that document DAB is assigned as supporting evidence for turn TA.
> The complete evidence state is serialized as an evidence program.
> Evidence-Program Grammar
> TURN>DOCUMENT[,DOCUMENT...] commands separated by one space
> Example:
> TA>DBG,DBJ TB>DAR,DAX TC>DCC TD>DBG
> This program represents:
> TA supported by DBG and DBJ;
> TB supported by DAR and DAX;
> TC supported by DCC;
> TD supported by DBG.
> Turn tokens indicate conversation order.
> Document tokens are anonymous and local to one case. For example, DBG in one case has no relationship to DBG in another case.
> Task
> For every evaluation case, predict a patch that transforms the supplied corrupted_program into the hidden correct evidence program.
> A repair may require the model to:
> remove an injected distractor;
> restore omitted supporting evidence;
> reverse a hard same-turn replacement;
> repair evidence copied from another turn;
> reverse a cross-turn swap;
> restore a broken evidence-reuse relationship;
> correct several coordinated graph edits;
> handle changes in the number of documents assigned to a turn.
> Gold patches contain between 4 and 8 edit operations.
> Every gold patch affects at least two conversation turns.
> No training or evaluation case is a no-op. Every case requires a non-empty repair patch.
> A submitted patch may contain at most 10 operations.
> Turns that do not require an edit must be omitted from the patch.
> Patch Language
> A patch is a space-separated sequence of turn-specific edit commands.
> Patch Grammar
> TURN>[+|-]DOCUMENT[,[+|-]DOCUMENT...] commands separated by one space
> Use:
> -DOCUMENT
> to remove a document from a turn.
> Use:
> +DOCUMENT
> to add a document to a turn.
> Example
> Suppose the corrupted evidence program is:
> TA>DBG,DBJ TB>DAR,DAX TC>DCC TD>DBG
> A valid patch is:
> TA>-DBJ,+DAR TB>-DAX,+DBG TC>-DCC,+DBG
> After applying the patch, the repaired program becomes:
> TA>DBG,DAR TB>DBG,DAR TC>DBG TD>DBG
> The patch performs these operations:
> remove (TA, DBJ);
> add (TA, DAR);
> remove (TB, DAX);
> add (TB, DBG);
> remove (TC, DCC);
> add (TC, DBG).
> The absence of a turn command means that the patch leaves that turn unchanged.
> Order-Invariant Patch Semantics
> The grader interprets a valid patch as a set of edit operations.
> Therefore:
> turn-command order does not affect scoring;
> removal and addition order does not affect scoring;
> document order within a command does not affect scoring.
> For example, these patches represent the same operation set:
> TA>-DBJ,+DAR TB>-DAX,+DBG
> TB>+DBG,-DAX TA>+DAR,-DBJ
> Both are valid provided that every operation is legal for the corresponding corrupted program.
> Duplicate or contradictory operations are invalid.
> Corruption Profiles
> Each case is generated from one of three corruption profiles.
> The profile is provided for training cases and hidden for evaluation cases.
> balanced_replacement
> Correct evidence edges are replaced by hard distractor edges across multiple turns.
> For each affected turn, the corrupted and correct programs contain the same number of assigned documents.
> This profile tests semantic discrimination under cardinality-preserving corruption.
> asymmetric_cardinality
> The corrupted program contains combinations of:
> missing supporting evidence;
> injected distractors;
> partial evidence loss;
> evidence reuse disruption;
> hard replacements.
> At least one affected turn has a different number of assigned documents in the corrupted and correct programs.
> This profile prevents the use of a universal same-cardinality decoding rule.
> cross_turn_hybrid
> The corrupted program contains cross-turn interactions such as:
> evidence copied from one turn to another;
> evidence swapped between turns;
> cross-turn contamination;
> coupled edits affecting several turns.
> These interactions are combined with additional missing, injected, or replaced evidence.
> This profile requires joint reasoning over the complete conversation rather than independent turn-level retrieval.
> Corruption categories may overlap. For example, a turn swap is also a form of cross-turn contamination.
> Candidate Documents
> Every case contains exactly 64 candidate documents.
> The candidate pool contains:
> all hidden supporting documents required by the conversation;
> query-level hard negatives;
> conversation-level hard negatives;
> cross-turn distractors;
> split-safe documents used to complete the pool.
> Candidate documents are provided in a separate Parquet file.
> Each candidate is represented by:
> case_id
> document_token
> document_text
> Candidate order is deterministically shuffled.
> Candidate row position and token identity must not be treated as relevance signals.
> Conversation Format
> The conversation_text field contains an ordered sequence of turns.
> Example:
> TA: What conditions are required for the process to begin?
> ||
> TB: How does temperature affect that process?
> ||
> TC: What happens when the temperature becomes too high?
> The separator:
> ||
> marks the boundary between conversation turns.
> Turn tokens such as TA, TB, and TC specify turn order but do not encode the topic, answer, corruption type, or relevance label.
> Data Provenance
> The challenge is derived from RECOR, a reasoning-focused benchmark for multi-turn conversational retrieval spanning 11 domains.
> The source data contains:
> complete multi-turn conversations;
> ordered turn-level queries;
> domain-specific document collections;
> turn-level supporting-document annotations.
> The preparation process converts the original retrieval annotations into supervised inverse-program targets.
> The resulting benchmark evaluates recovery of a hidden conversational evidence state rather than ordinary ranked retrieval alone.
> Public Files
> The challenge provides:
> train_cases.csv
> train_candidates.parquet
> test_cases.csv
> test_candidates.parquet
> sample_submission.csv
> challenge_metadata.json
> train_cases.csv
> Contains one row per labelled training case.
> | Column | Type | Description |
> |---|---|---|
> | case_id | string | Anonymous training-case identifier |
> | conversation_id | string | Anonymous source-conversation group identifier |
> | domain_token | string | Opaque domain token |
> | conversation_text | string | Ordered multi-turn conversation |
> | corrupted_program | string | Observed corrupted evidence program |
> | corruption_profile | string | Training-only corruption-profile label |
> | target_patch | string | Gold inverse program that repairs the corrupted state |
> Training data may contain multiple independently remapped corruption variants derived from the same source conversation.
> For local validation, split by conversation_id rather than by individual rows. Cases sharing one conversation_id must remain in the same validation fold.
> train_candidates.parquet
> Contains exactly 64 candidate-document rows for every training case.
> | Column | Type | Description |
> |---|---|---|
> | case_id | string | Training-case identifier |
> | document_token | string | Case-local anonymous document token |
> | document_text | string | Candidate-document text |
> Rows belonging to one case are identified by their shared case_id.
> test_cases.csv
> Contains one row per evaluation case.
> | Column | Type | Description |
> |---|---|---|
> | case_id | string | Anonymous evaluation-case identifier |
> | conversation_id | string | Anonymous evaluation-conversation identifier |
> | domain_token | string | Opaque domain token |
> | conversation_text | string | Ordered multi-turn conversation |
> | corrupted_program | string | Observed evidence program that must be repaired |
> The following information remains private:
> target patch;
> target evidence program;
> corruption profile;
> edit count;
> hard-case membership;
> source identifiers;
> original document identifiers.
> test_candidates.parquet
> Contains exactly 64 candidate-document rows for every evaluation case.
> | Column | Type | Description |
> |---|---|---|
> | case_id | string | Evaluation-case identifier |
> | document_token | string | Case-local anonymous document token |
> | document_text | string | Candidate-document text |
> sample_submission.csv
> Contains the required submission structure:
> case_id,patch
> The sample patches illustrate formatting only.
> They are not intended to be correct predictions and may contain fewer operations than the hidden gold patches.
> challenge_metadata.json
> Contains public benchmark configuration, including:
> challenge identifier;
> task identifier;
> candidate-pool size;
> token formats;
> evidence-program grammar;
> patch grammar;
> corruption-profile names;
> minimum and maximum gold edit counts;
> maximum submitted operations;
> training and evaluation case counts;
> evaluation metric;
> score direction;
> score range;
> leakage-control declarations.
> Submission Format
> Submit one CSV file containing exactly these two columns in this order:
> case_id,patch
> Every evaluation case_id must appear exactly once.
> Example:
> case_id,patch
> test_case_001,"TA>-DBJ,+DAR TB>-DAX,+DBG"
> test_case_002,"TA>-DCC TC>-DBG,+DAF"
> The identifiers shown above illustrate formatting only.
> The operations in each submitted patch must be valid for the corresponding case.
> The patch field must always be non-empty.
> There is no no-op token because every evaluation case requires at least one repair.
> Do not submit placeholders such as:
> NO_OP
> NONE
> EMPTY
> TA>
> Turns requiring no changes must simply be omitted from the patch.
> Submission-Level Validation
> The complete submission receives a score of 0 when:
> the file cannot be read;
> the file exceeds the maximum allowed size;
> the required columns are missing;
> additional columns are included;
> the columns are not ordered as case_id,patch;
> a required evaluation case is missing;
> an evaluation case appears more than once;
> an unknown case_id is included;
> a case_id is empty, padded with whitespace, or malformed.
> Case-Level Patch Validation
> Within an otherwise valid submission, an invalid patch receives zero credit for that case.
> A patch is invalid when it:
> is empty;
> uses a no-op placeholder;
> exceeds the permitted character limit;
> contains control characters or non-ASCII characters;
> contains tabs or line breaks;
> uses malformed spacing;
> violates the patch grammar;
> references an unknown turn;
> references a document outside the case's candidate pool;
> repeats a turn command;
> repeats the same edit;
> contains both addition and removal for the same turn-document pair;
> adds a document already assigned to that turn;
> removes a document not currently assigned to that turn;
> leaves any turn with an empty evidence set;
> contains more than 10 operations.
> Evaluation
> A submission is evaluated in two complementary spaces:
> program space — whether the predicted inverse operations match the hidden target patch;
> state space — whether applying the patch recovers the hidden correct evidence state.
> The raw score is:
> RawScore =
> 0.40 × OverallPatchOperationF1
> + 0.20 × OverallRepairedEvidenceF1
> + 0.15 × HardCaseComposite
> + 0.15 × WorstProfileComposite
> + 0.10 × ExactRepairAccuracy
> Patch Operation F1
> Each operation is represented as:
> (turn, operation, document)
> Examples:
> (TA, -, DBJ)
> (TA, +, DAR)
> For each case, the submitted operation set is compared with the hidden gold operation set using F1.
> This component rewards correct additions and removals while penalizing:
> omitted operations;
> incorrect operations;
> unnecessary operations.
> OverallPatchOperationF1 is the mean case-level operation F1 across the full evaluation set.
> Repaired Evidence F1
> The submitted patch is applied to the corrupted evidence program.
> For each turn, the resulting document set is compared with the hidden correct document set using set F1.
> The turn-level values are averaged within each case and then across all evaluation cases.
> This component gives partial credit when the recovered evidence state is substantially correct even when the predicted inverse program does not exactly match every gold operation.
> Exact Repair Accuracy
> A case is counted as exactly repaired only when:
> the submitted operation set exactly equals the hidden gold operation set; and
> applying the submitted patch produces the hidden target evidence program for every turn.
> ExactRepairAccuracy is the fraction of evaluation cases repaired exactly.
> Hard Case Composite
> A deterministic private subset of structurally difficult cases is scored separately.
> Hard cases emphasize combinations such as:
> longer conversations;
> larger edit programs;
> variable-cardinality corruption;
> evidence reuse;
> multiple affected turns;
> cross-turn contamination;
> ambiguous hard negatives;
> coupled graph edits.
> For each hard case:
> HardCaseScore =
> 0.65 × PatchOperationF1
> + 0.35 × RepairedEvidenceF1
> HardCaseComposite is the mean hard-case score across the private hard cohort.
> Worst Profile Composite
> Performance is calculated separately for each corruption profile.
> For each case:
> ProfileCaseScore =
> 0.65 × PatchOperationF1
> + 0.35 × RepairedEvidenceF1
> Profile means are calculated independently for:
> balanced_replacement
> asymmetric_cardinality
> cross_turn_hybrid
> The final profile component is:
> WorstProfileComposite =
> minimum profile mean
> This prevents a system from achieving a high score by specializing in only one corruption family.
> A robust model must perform across both cardinality-preserving and cardinality-changing corruptions.
> Baseline Normalization
> The raw score is normalized against the strongest fixed preparation-time baseline.
> FinalScore =
> clip(
> (RawScore - BaselineRawScore) /
> (1 - BaselineRawScore),
> 0,
> 1
> )
> The fixed baseline collection includes:
> an unchanged-program baseline;
> random valid repair programs;
> query-only sparse-retrieval repair;
> history-aware sparse-retrieval repair;
> a trained structure-only red-team model.
> The strongest raw baseline is selected once during preparation.
> BaselineRawScore remains private and is identical for every participant submission.
> The final score is clipped to:
> [0, 1]
> Higher scores are better.
> Data Separation and Leakage Control
> The preparation pipeline enforces:
> complete source-conversation separation between training and evaluation;
> disjoint training and evaluation gold document identifiers;
> disjoint normalized gold document text between training and evaluation;
> local remapping of candidate identifiers for every case;
> opaque source-conversation identifiers;
> opaque domain tokens;
> removal of reference answers from public evaluation inputs;
> removal of reasoning annotations from public evaluation inputs;
> removal of target-bearing retrieval fields from public evaluation inputs;
> deterministic candidate shuffling;
> candidate-position concentration audits;
> case-local lexical masking;
> different lexical mappings across cases;
> validation of every private target patch;
> exact reconstruction of every hidden target program;
> independent processing of evaluation cases.
> Candidate token values, candidate order, case_id, and conversation_id must not be used as memorization or relevance features.
> Modelling Requirement
> A valid solution must train or fine-tune a model using the supplied training data.
> Suitable approaches include:
> history-aware cross-encoders;
> dense bi-encoder retrieval;
> late-interaction retrieval;
> learning-to-rank models;
> neural turn-document edge classification;
> graph neural networks;
> structured prediction;
> sequence-to-sequence inverse-program generation;
> constrained repair decoding;
> jointly trained retrieval-and-repair models;
> learned scoring followed by combinatorial decoding.
> Sparse retrieval and frozen representations may be used as:
> candidate-scoring features;
> initialization;
> auxiliary signals;
> candidate-generation mechanisms.
> However, the final solution must contain a component genuinely trained or fine-tuned on the supplied challenge data.
> An inference-only system with no challenge-specific training or fine-tuning is not considered a valid trained solution.
> Recommended Modelling Pipeline
> A competitive system may:
> parse the conversation into ordered turns;
> parse the corrupted evidence program;
> join every case with its 64 candidate documents;
> encode each turn with conversational history;
> score candidate documents for every turn;
> estimate whether each observed edge should remain or be removed;
> estimate which missing edges should be added;
> model cross-turn edge relationships;
> infer the likely corruption structure;
> decode a sparse legal repair program;
> validate the patch before submission.
> The decoder should enforce:
> valid turn tokens;
> valid case-local document tokens;
> legal additions;
> legal removals;
> non-empty repaired turn assignments;
> no duplicate operations;
> no contradictory operations;
> the 10-operation limit.
> Recommended Validation Strategy
> Because training data may contain multiple variants derived from the same source conversation:
> create validation folds grouped by conversation_id;
> keep all cases sharing a conversation_id in one fold;
> report results separately for each corruption profile;
> track Patch Operation F1;
> track Repaired Evidence F1;
> track Exact Repair Accuracy;
> track the worst profile score;
> verify that every generated patch is executable;
> verify that no repaired turn becomes empty;
> avoid selecting models only on balanced-replacement performance.
> Restrictions
> The following are prohibited:
> external datasets;
> external answer keys;
> internet access during execution;
> downloading additional corpora during execution;
> reverse matching anonymous cases against external RECOR copies;
> cached evaluation predictions;
> hardcoded evaluation patches;
> manually encoded evaluation answers;
> using case_id as a predictive feature;
> using conversation_id as a memorization key;
> using candidate token identity as a relevance signal;
> using candidate order or row position as a relevance signal;
> test-set pseudo-labelling;
> cross-case test calibration;
> allowing one evaluation case to influence another;
> exploiting public-file row order;
> using an inference-only pipeline with no genuine challenge-specific training.
> Every evaluation case must be processed independently.
> Compute Environment
> The challenge runs on an NVIDIA A10G GPU.
> Suitable models should remain practical for this environment, including:
> compact transformer encoders;
> cross-encoders;
> dense retrievers;
> late-interaction models;
> learning-to-rank systems;
> graph-based models;
> structured decoders;
> small constrained optimization procedures.
> Objective Summary
> ordered multi-turn conversation
> + 64 case-local candidate documents
> + observed corrupted evidence program
> ↓
> infer the hidden conversational evidence state
> ↓
> predict a sparse inverse edit program
> ↓
> apply additions and removals
> ↓
> recover the hidden correct evidence program
> The goal is not simply to rank relevant documents.
> The goal is to induce the structured inverse program that explains how a corrupted multi-turn evidence state must be transformed into its hidden correct state.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Grounding Sanskrit Commentary: Verse Retrieval over the Bhagavad Gita

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dat75rad3tbp20wye7evtns8bk8h9
- DOMAIN exactly as displayed: RAG
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Eight historical commentators wrote line-by-line Sanskrit commentaries on the Bhagavad
> Gita between roughly the 10th and 18th centuries. Each passage of commentary glosses one
> specific verse — but in the manuscript tradition that link is carried by layout and
> editorial convention, not by the text itself. Strip the running heads and you are left
> with a passage of Sanskrit prose and the question: **which of the 701 verses is this
> about?**
> You are given the full verse corpus as a searchable index and a set of commentary
> passages as queries. For each query, return a ranked list of candidate verses.
> Quoted verse material has been removed from every query. Most commentators open by
> reciting the verse before explaining it, which would reduce the task to substring search.
> Every 6-character sequence occurring in a passage's own verse has been deleted from it,
> retaining about 93% of the original characters: the commentator's exposition, argument,
> and paraphrase, but not the words of the verse itself.
> What remains is genuine semantic grounding. You must recognise which verse a passage is
> about from how it is discussed — the objection being answered, the doctrinal term being
> defined, the chain of reasoning — rather than from shared strings. The corpus offers four
> parallel views of each verse (Devanagari, romanized IAST, English translation, word-by-word
> gloss).
> Evaluation
> Submissions are scored using MRR@10 (mean reciprocal rank, cut off at rank 10).
> For each query, if the correct verse appears at rank r ≤ 10, that query scores 1/r;
> otherwise it scores 0. The final score is the mean over all queries, bounded in [0, 1].
> Reciprocal rank rather than accuracy@1 because retrieval usually feeds a downstream
> reader that sees several candidates. A system that surfaces the right verse at rank 2
> is meaningfully better than one that misses entirely, and the metric should say so.
> Duplicate ids within a row are collapsed, keeping first position. Anything past rank 10
> is ignored. Row order does not matter; rows are aligned on id.
> Dataset
> Files in public/:
> verses.csv — the retrieval corpus, all 701 Bhagavad Gita verses
> train.csv — 3,072 labeled commentary→verse pairs
> test.csv — 520 commentary passages to locate
> sample_submission.csv — 520 rows in the expected format
> verses.csv — the corpus
> | Column | Type | Description |
> |--------|------|-------------|
> | verse_id | string | Verse identifier, e.g. bg_2_47. This is what you retrieve |
> | chapter | int | Chapter number, 1–18 |
> | verse | int | Verse number within the chapter |
> | sanskrit | string | Verse text in Devanagari |
> | iast | string | Romanized IAST transliteration of the same text |
> | translation_en | string | English translation (Swami Sivananda) |
> | word_meanings | string | Word-by-word gloss, Sanskrit term to English |
> All 701 verses are present, including every verse targeted by the test queries. The
> corpus is the index — nothing is withheld from it.
> train.csv — labeled pairs
> | Column | Type | Description |
> |--------|------|-------------|
> | id | string | Query identifier, e.g. q_01843. Assigned at random; carries no information |
> | commentator | string | Which of the eight commentators wrote the passage |
> | text | string | Commentary passage, Devanagari and spaces only, quoted verse material removed |
> | verse_id | string | Label. The verse this passage glosses |
> test.csv — queries
> | Column | Type | Description |
> |--------|------|-------------|
> | id | string | Query identifier, e.g. q_01843. Assigned at random; carries no information |
> | commentator | string | Which of the eight commentators wrote the passage |
> | text | string | Commentary passage, same normalization and quote removal as train |
> Split
> The 701 verses were partitioned before splitting. train.csv contains labeled pairs for
> 525 verses; every test query targets one of the other 175. **Test verses have no labeled
> training examples at all**, so this is zero-shot retrieval against corpus text — the
> training pairs are available for tuning and calibration, not for learning verse-specific
> vocabulary. Test queries are capped at three per verse so that heavily-commented verses
> do not dominate the score.
> Query text carries no verse identifier: the source edition's running ।।2.47।। markers
> are removed, along with all Latin characters, digits, and ASCII punctuation.
> Submission
> Submit a CSV with one row per test query, giving up to 10 verse ids in rank order,
> most confident first, separated by spaces:
> | Column | Type | Description |
> |--------|------|-------------|
> | id | string | Query identifier from test.csv |
> | verse_ids | string | Up to 10 verse_id values, space-separated, best first |
> id,verse_ids
> q_01843,bg_2_47 bg_2_48 bg_3_1 bg_2_50 bg_18_66
> q_00296,bg_9_22 bg_9_23 bg_12_6
> q_03510,bg_1_1
> Requirements
> Must contain exactly 520 rows, one per test query.
> Include a header row.
> Exactly two columns, named id and verse_ids.
> id values must match test.csv exactly, with no duplicates.
> Fewer than 10 ids is allowed; only the first 10 are scored.
> Ids not present in verses.csv score zero but do not invalidate the submission.
> Row order is not significant.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Multi-Statute Authority Retrieval from Legal Records

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7d2r6be0k7bckadcmy0stk6d8awsxg
- DOMAIN exactly as displayed: RAG
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Legal records frequently refer to several interacting statutory authorities. In this challenge, each row contains a real case record or legal query in which explicit statutory citations have been removed, plus eighty anonymized candidate authority passages. Recover every authority linked to the record and emit their candidate tokens as one variable-length, space-separated sequence.
> The number of relevant authorities is given by authority_slots. Candidate tokens are local to one row and carry no meaning across rows. Relevant authorities must be returned in the same left-to-right order in which their tokens appear in candidate_authorities. A useful first approach is to retrieve similar training records, infer their governing statutes, and align those statutes to the current candidate set.
> Evaluation Metric
> For row i, let G_i be the set of gold tokens and P_i the submitted set.
> precision_i = |P_i ∩ G_i| / |P_i|.
> recall_i = |P_i ∩ G_i| / |G_i|.
> F_i = 2 × precision_i × recall_i / (precision_i + recall_i). A zero denominator gives zero.
> Let C_i be the number of gold token pairs that are both submitted and appear in their correct relative order. Let T_i = |G_i| × (|G_i| − 1) / 2 be the total number of gold token pairs. When T_i is greater than zero, O_i = C_i / T_i. When T_i = 0, define O_i = 1 because there are no gold token pairs to order.
> E_i = 1 when the submitted token sequence exactly equals the gold sequence, and E_i = 0 otherwise.
> R_i = 0.65 × F_i + 0.20 × O_i + 0.15 × E_i.
> Final score = 100 × clip(mean of all R_i values, 0, 1), where clip(x, 0, 1) limits x to the interval from 0 through 1.
> Invalid tokens, repeated tokens, missing predictions, non-string values, incorrect sequence lengths, and malformed sequences receive zero for that row. The minimum is 0 and a perfect submission is 100.
> Measured public-file baselines are: perfect 100.00, empty sample submission 0.00, constant A00 A01 0.48, and lexical retrieval with the disclosed slot count 3.05. A sparse TF-IDF CPU retrieval ladder scores 41.45, 48.71, 54.51, 57.81, 58.91, and 59.34 as its neighborhood evidence increases from 3 to 80 training records.
> Dataset
> train.csv contains:
> sample_id - string - opaque row identifier.
> case_text - string - real legal record with explicit authority citations removed by the source corpus.
> candidate_authorities - string - eighty entries separated by || , each formatted as A00 :: authority text.
> authority_slots - integer - number of relevant authority tokens to return, from two through five.
> target_authorities - string - ordered, space-separated relevant candidate tokens.
> test.csv contains the same query columns but no target_authorities.
> sample_submission.csv contains the required submission columns and test IDs.
> Submission
> The CSV must contain exactly these columns in this order:
> sample_id - string - an ID appearing exactly once in test.csv.
> target_authorities - string - exactly authority_slots distinct tokens, separated by single spaces and ordered by their appearance in the candidate list.
> The submission requires exactly 1,225 data rows plus a header. Missing, duplicate, unknown, or extra IDs and any extra or reordered columns are rejected cleanly. Valid tokens are A00 through A79.
> A correctly formatted submission looks like this:
> sample_id,target_authorities
> ac_009cc0af6cfee81a,A00 A01 A02 A03 A04
> ac_00e80e13c78bd246,A00 A01 A02
> ac_00fb2f7470b0a709,A00 A01 A02
> These are real test IDs and the example contains the required number of distinct tokens for each row. The token choices only illustrate valid formatting and are not disclosed answers.
> What Not to Use
> A constant token sequence ignores that tokens are randomized independently for each row.
> Majority labels cannot transfer between rows because candidate-token identities are local.
> Plain word overlap misses authorities expressed through facts rather than quoted statutory language.
> Selecting only one passage cannot recover the coupled two-to-five-authority target.
> External source lookup is unnecessary and the released rows omit original source identifiers.
> Expected solutions combine sparse retrieval over training records, legal phrase features, candidate passage matching, and constrained sequence decoding.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Locating the Provision a Bill Amends

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bab4tqx8mk59y0eq52mtaxs8dthmc
- DOMAIN exactly as displayed: RAG
- Challenge collection: Non-CPU
- Status: Not displayed; challenge detail page timed out
- Difficulty: Medium
- Compute: Not displayed; challenge detail page timed out
- GPU: Not displayed; challenge detail page timed out
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage card score context: Beat passbaseline's score of 0.565!

Full challenge description from page:

> Locating the Provision a Bill Amends Overview Given the statutory language proposed by an amendment, retrieve the United States Code section it would change. Rank five section IDs from the supplied corpus. The target comes from the machine-readable citation in the source bill XML. The amendment text contains proposed insertions or replacements. Preparation masks recognized citation patterns, named Acts and multi-digit numbers with REF], [ACT] and [NUM]. The surrounding legal substance remains. Masking is pattern based; it is not a guarantee that every identifying phrase has disappeared. This is an offline retrieval task over the provided files, on the CPU tier. Data | File | Rows | Purpose | |---|---:|---| | corpus.csv | 55,939 | Candidate provisions from 51 title identifiers, 2023 Code edition | | train.csv | 6,681 | Training amendment features; same columns as test.csv | | train_labels.csv | 6,681 | Public training targets keyed by instruction ID | | train_groups.csv | 6,681 | Training-only bill groups and Congress for validation | | test.csv | 2,073 | Amendment text to retrieve against the corpus | | sample_submission.csv | 2,073 | Example of the required output schema | train.csv and test.csv have exactly the same feature columns: | Column | Type | Description | |---|---|---| | instruction_id | string | Stable identifier derived from the visible text | | amendment_text | string | Masked proposed language, at most 8,000 characters | train_labels.csv: | Column | Type | Description | |---|---|---| | instruction_id | string | Joins one-to-one with train.csv | | target_section_id | string | Correct corpus ID, such as 16/1533 | corpus.csv: | Column | Type | Description | |---|---|---| | section_id | string | Unique candidate ID, formatted as title/section | | heading | string | Section heading, up to 300 characters; 131 are empty | | text | string | Section body, up to 3,000 characters; four are empty | train_groups.csv: | Column | Type | Description | |---|---|---| | instruction_id | string | Joins one-to-one with train.csv | | bill_group | string | Group shared by instructions from the same training bill | | congress | string | 116, 117 or 118 | Training contains 2,536 bills; evaluation contains 802 bills from Congress 119. No raw bill group appears on both sides. The largest evaluation bill contributes 197 rows, so rows should not be treated as independent bills. Join train.csv to train_labels.csv on instruction_id to obtain supervised training pairs. The ID sets match exactly and each ID is unique in both files. Validation Use the training grouping file when choosing a method. A useful development split trains on Congresses 116-117 and validates on 118. Alternatively, hold out complete bill groups. Fit any learned representation, calibration or model-selection step using training/development data only. You may index and fit unsupervised text representations on the supplied candidate corpus. Exact duplicate text is collapsed, and identical normalized text carrying different raw targets is excluded. Near-duplicate clustering is also applied. The final split was separately checked for cross-split 8-word-shingle Jaccard similarity of at least 0.8. Submission Write your predictions to submission.csv. Submit a CSV with these columns in exactly this order: instruction_id,pred_1,pred_2,pred_3,pred_4,pred_5 Include exactly one row for each ID in test.csv. Each prediction must be a nonempty string equal to a section_id in corpus.csv. Supply five distinct IDs per row, ordered from most likely to least likely. Do not add columns or pad values with whitespace. Invalid submissions are rejected rather than repaired. Metric The score is MRR@5, averaged over evaluation instructions. An instruction receives 1/r if its target occurs at rank r <= 5, and zero otherwise. MRR@5 = sum(reciprocal_rank_at_5 for each instruction) / number_of_instructions Higher is better; the range is 0 to 1. Perfect first-place answers score 1.0. Putting every target fifth scores 0.2. The metric weights instructions equally; it does not macro-average over bills. Rules No particular model, mandatory training step, or external checkpoint is required. The rubrics distinguish required resource/output constraints from recommended development practices. Use the supplied public files and the platform's installed local packages. Evaluation inputs are for inference only: no fitting, vocabulary/statistics estimation, pseudo-labeling, threshold selection or model selection on test.csv. Do not search for or download source bills, external datasets or evaluation answers, and do not use remote inference or web lookup. The source texts are public, so this resource restriction is essential to the task. Do not install packages or download models. The supplied CPU reference requires no external checkpoint. Source Bill XML and the 2023 United States Code are from the United States Government Publishing Office, GovInfo. Attribution: U.S. Government Publishing Office, GovInfo, and the originating legislative offices. Government-work reuse policy: [https://www.govinfo.gov/about/policies. &nbsp;
> $700 Pool
> Ranks finalizing

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## IonWeave Peak Witness

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7d5qydy3zccek0yjc909mnc18dy5ta
- DOMAIN exactly as displayed: RAG
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat pvduy's score of 0.703!

Full challenge description from page:

> IonWeave Peak Witness Overview IonWeave Peak Witness is a research-grade retrieval-augmented generation challenge over real experimental tandem mass spectra. For each query, you receive one anonymized spectrum packet containing 24 peak objects and a shared corpus of 600 evidence documents. You must produce one structured JSON answer that: selects the hidden-replicate recurrence winner from each of eight matched intensity-rank strata, then ranks those eight witnesses by reliability; and retrieves and cites the three corpus documents most useful for that recurrence judgment. The evidence corpus contains 600 reliability-annotated acquisition documents from 300 molecular connectivity groups that do not appear in test. It is intentionally shared: every query retrieves over all 600 corpus rows, and no per-query candidate list appears in train.csv or test.csv. A useful solver must retrieve analog evidence, interpret recurring fragment and neutral-loss patterns, learn from labeled training queries, and emit a schema-valid answer. The task is not molecule identification, property regression, or ordinary row classification. The molecular identity, formula, SMILES, taxonomy, source record ID, and other identity-bearing fields are absent from participant data. Public query, peak, and document IDs are independently randomized 20-character tokens and carry no semantic or ordering information. This prepared release is restricted to positive-ion spectra because no negative-ion cohort survived every strict replicate and cross-instrument filter. Polarity is therefore a fixed cohort constraint, not a modeling feature, and is intentionally omitted from participant-facing tables rather than exposed as a constant column. An ion condition is defined by full InChIKey, ionization polarity, and precursor m/z rounded to 0.1 Da. Molecular split groups are coarser: they use the first connectivity block of the InChIKey. Entire connectivity groups are assigned to one role only. The corpus and labeled training side contain 1,600 groups, the hidden test side contains 400 groups, and their connectivity-group overlap is exactly zero. The target for a test molecule is derived from five distinct replicate spectra that are not exposed in the query or corpus. Evaluation The score is the mean of a weighted two-part nDCG score over all test queries. Higher is better. Scores are finite and bounded from 0 to 1. For a query peak, hidden recurrence gain is computed from five held-out replicate spectra. A query peak matches a hidden peak when their fragment positions differ by at most five 0.01 Da bins, or 0.05 Da. Let r be the fraction of hidden spectra with a match and let a be the mean relative intensity among matched occurrences. Its continuous hidden gain is: peak_gain = r * (0.75 + 0.25 * a) The intensity scale in this formula is fully specified as follows. Within each hidden spectrum, every raw peak intensity is divided by the maximum raw peak intensity in that same spectrum before truncation. This produces a relative-intensity fraction in [0,1]. The hidden matching map then retains at most the 64 strongest valid peaks, rounds fragment and precursor-minus-fragment positions to 0.01 Da bins, removes repeated fragment bins by keeping the strongest occurrence, and discards non-finite, negative-intensity, or out-of-range peaks. For a query peak and one hidden spectrum, the matched occurrence is the retained hidden peak with the largest relative-intensity fraction inside the inclusive fragment_bin +/- 5 window. Let m be the number of the five hidden spectra with a positive match. Then r = m / 5, and a is the arithmetic mean of the m matched relative-intensity fractions. If m = 0, both r and a are defined as 0. Thus a is a raw normalized fraction, not the public integer intensity_level on the 0 through 7 scale. The 32 strongest distinct source peaks are divided into eight consecutive intensity-rank strata of four. Within each stratum, the peak with the highest hidden recurrence gain is the witness. Its closest hidden-recurrence runner-up is withheld, and the public packet contains the witness plus the other two lower-recurrence peaks. Episodes with a zero or tied stratum winner are excluded. The eight stratum winners retain their continuous hidden gains for scoring; all 16 distractors have relevance zero. These 24 scoring gains are rounded to eight decimal places in private truth. This outcome-conditioned, within-stratum construction prevents public intensity rank from copying the answer. Each of the 600 corpus documents also has a continuous gain for each query: citation_gain(query, document) = 0.25 * token_jaccard + 0.75 * profile_cosine The token Jaccard term uses sets built from the 24 public peak objects on each side. Because fragment_bin and loss_bin are in 0.01 Da units, integer floor division by 1,000 creates 10 Da cells and division by 2,500 creates 25 Da cells. Each peak contributes four typed tokens: ("f", fragment_bin // 1000); ("l", loss_bin // 1000); ("fi", fragment_bin // 2500, intensity_level // 2); and ("li", loss_bin // 2500, intensity_level // 2). Duplicate tokens collapse because this is a set. If the query set is Tq and the document set is Td, token_jaccard = |Tq intersect Td| / |Tq union Td|, with value 0 for an empty union. The profile cosine term compares two sparse vectors over typed 10 Da cells. For every one of the 24 query peaks, its hidden recurrence gain from the formula above is assigned to keys ("f", fragment_bin // 1000) and ("l", loss_bin // 1000); this includes the raw recurrence gains of distractors even though distractor relevance is set to zero for peak nDCG. If multiple peaks share a key, the vector stores their maximum gain. For every one of the 24 evidence peaks, reliability_level / 7 is assigned to the corresponding fragment and loss keys, again taking the maximum within a key. Missing keys have value 0. profile_cosine is the ordinary dot product divided by the product of the two full sparse-vector L2 norms, and is defined as 0 if either norm is 0. The final citation gain is rounded to eight decimal places in private truth. Every document at or above the third-highest citation-gain cutoff retains its continuous relevance. The ideal denominator uses three documents, with opaque document ID used only for deterministic ordering. Documents below the cutoff have relevance zero. For either component, with a zero-based submitted rank j, the discounted cumulative gain is: DCG@k = sum(relevance[item_j] / log2(j + 2) for j in range(k)) nDCG@k = DCG@k / ideal_DCG@k The per-query score and final score are: row_score = 0.82 * peak_nDCG@8 + 0.18 * citation_nDCG@3 final_score = mean(row_score over every test query) The following reference implementation defines the metric after submission structure and JSON validity have been checked: import math def retained_relevance(all_gains, k): ordered = sorted(all_gains, key=lambda item: (-all_gains[item], item)) cutoff = all_gains[ordered[k - 1]] return {item: gain for item, gain in all_gains.items() if gain >= cutoff} def ndcg_at_k(predicted_order, all_gains, k): relevance = retained_relevance(all_gains, k) dcg = sum( relevance.get(item, 0.0) / math.log2(rank + 2.0) for rank, item in enumerate(predicted_order[:k]) ) ideal = sorted(relevance.values(), reverse=True)[:k] idcg = sum(value / math.log2(rank + 2.0) for rank, value in enumerate(ideal)) return dcg / idcg if idcg > 0.0 else 0.0 def score_row(peak_ranking, citations, peak_gains, citation_gains): peak_score = ndcg_at_k(peak_ranking, peak_gains, 8) citation_score = ndcg_at_k(citations, citation_gains, 3) return 0.82 * peak_score + 0.18 * citation_score A structurally valid CSV with malformed, missing, oversized, non-string, or schema-invalid answer_json content receives zero for the affected row. A structurally invalid CSV raises a clean ValueError instead of receiving a score. Dataset The participant-visible directory is ./dataset/public/ and contains four CSV files. train.csv train.csv contains 2,600 labeled queries and these columns: id (string): Random 20-character query identifier. instrument_family (string): Harmonized instrument family for the query acquisition. precursor_bin (integer): Precursor m/z rounded to the nearest whole dalton. peaks_json (JSON string): List of exactly 24 peak objects in randomized order. answer_json (JSON string): Training answer with exactly eight ranked peak IDs and three ranked citations. Each object in peaks_json contains: peak_id (string): Random 20-character identifier local to that peak. fragment_bin (integer): Fragment m/z in 0.01 Da units. Divide by 100 to recover the bin-center m/z. Exact duplicate fragment bins are removed before the 24 query peaks are selected. loss_bin (integer): Precursor-minus-fragment neutral loss in 0.01 Da units. Divide by 100 to recover the bin-center loss. intensity_level (integer): Square-root-compressed relative-intensity level min(7, floor(8 * sqrt(relative_intensity))), where relative_intensity is the raw intensity divided by that spectrum's maximum raw intensity. rank_band (integer): Intensity-rank stratum from 0 through 7. Exactly three public candidates occur in each stratum, and exactly one is the hidden-replicate witness. test.csv test.csv contains 400 unlabeled queries and the same columns as train.csv except answer_json. It contains only query features and intentionally has no citation-candidate or evaluation-target column. corpus.csv corpus.csv contains 600 evidence documents, two distinct acquisitions from each of 300 molecular connectivity groups that do not appear in test. Its columns are: doc_id (string): Random 20-character evidence-document identifier. instrument_family (string): Harmonized instrument family for the evidence acquisition. precursor_bin (integer): Precursor m/z rounded to the nearest whole dalton. witness_peaks_json (JSON string): List of 24 evidence peak objects with empirical recurrence annotations. Each object in witness_peaks_json contains: fragment_bin (integer): Fragment m/z in 0.01 Da units. loss_bin (integer): Neutral loss in 0.01 Da units. intensity_level (integer): The same square-root-compressed relative-intensity level from 0 through 7 used for query peaks. rank_band (integer): Intensity-rank band from 0 through 7. reliability_level (integer): Quantized as min(7, max(0, int(round(7 * hidden_recurrence_gain)))), using Python's ties-to-even round semantics. sample_submission.csv sample_submission.csv contains 400 label-free format examples with these columns: id (string): Test query identifier. answer_json (JSON string): Structured prediction in the required format. Across train and test there are 72,000 distinct randomized peak IDs. Every query has 24 distinct peak IDs. Every query's citation universe is the same complete set of 600 unique doc_id values in corpus.csv; corpus documents are designed to be reused across queries, as in a normal shared RAG index. Submission Write ./working/submission.csv with exactly two columns, in this order: id,answer_json. Each answer_json cell must be a JSON object with exactly two keys: peak_ranking: A JSON list of exactly eight unique peak_id values from that row's peaks_json, ordered from most to least likely to recur. citations: A JSON list of exactly three unique doc_id values from corpus.csv, ordered from most to least useful. The outer CSV must quote and escape JSON according to normal CSV rules. The two rows below use real randomized test, peak, and corpus IDs but contain only the label-free sample ordering. id,answer_json 8b8k2mrxn9r2avnzddjf,"{""peak_ranking"":[""eh2nsspxz72fg726hq2g"",""ccm8276tj6qaph9fre2d"",""g7cje25dhywbz2862kjb"",""84pzaewv365rpbx2bxna"",""mp4bu5ngr4uxypz9x7ht"",""3gjh4eh6y4yvrcmezth8"",""yz8um8b7hx67rqndkfma"",""f49wgjxdhesxvk6cgp5z""],""citations"":[""22s9y3xhuj3ak87v7kh7"",""246cgepy8764vu4ardzm"",""257m9p8pggxmmwq628ac""]}" epafc5qvweqmfcwxq3ak,"{""peak_ranking"":[""h3ms9ed82nsyry3yexzt"",""xyhz4cmqwxpr8ky8kyk4"",""6tjyf4t6bwhetvhvv5t3"",""hf2zjwvkvgk7868p5cpz"",""rw79yd498eeuxw9x2tje"",""hpppf9pfbte28k6c76mx"",""92eegmx7v5g3gy3ktwj6"",""m78mybyk5dk7cang4au2""],""citations"":[""22s9y3xhuj3ak87v7kh7"",""246cgepy8764vu4ardzm"",""257m9p8pggxmmwq628ac""]}" Requirements Submit exactly 400 rows, one for every test ID. The CSV header and column order must be exactly id,answer_json; extra, missing, or renamed columns are rejected. IDs may be in any row order, but they must be unique and their set must match the test ID set exactly. Missing, duplicate, or foreign IDs are rejected. answer_json must be a string no longer than 4,096 characters and must parse as strict JSON. The JSON object must contain exactly peak_ranking and citations, with no extra or missing keys. The peak list must contain exactly eight unique valid peak IDs from the same query. The citation list must contain exactly three unique valid document IDs from the shared corpus.csv index. A NaN cell, infinity token, malformed JSON, wrong list length, duplicate item, or out-of-corpus item receives the worst row score of 0. Your notebook must read only ./dataset/public/ and write the single file ./working/submission.csv. The full solution must complete within 1.5 hours. Runtime downloads are unavailable and do not extend the limit. Use fixed seeds and deterministic data handling so the submitted result can be reproduced. What Not to Use Do not use external datasets, online spectral libraries, web search, hosted model APIs, or runtime downloads. Do not use pretrained model weights or embeddings. Train only from the provided public files. Do not recover, predict, obtain, or look up molecule names, SMILES, InChIKeys, formulas, taxonomy labels, source record IDs, spectral-library accessions, or other hidden identities and then use them anywhere in the solution. This prohibition covers direct lookup tables and identity-derived feature engineering, embeddings, joins, retrieval keys, grouping variables, validation folds, pseudo-labels, reranking signals, and final predictions. Do not join or approximately match public spectra to outside chemical or spectral records, even if the outside identity field is later discarded. Do not hardcode test IDs, peak IDs, document IDs, row order, or the sample submission's arbitrary ordering. Feature engineering is allowed when every input is derived solely from the provided public columns, such as fragment and neutral-loss bins, public intensity and rank levels, precursor bins, instrument families, corpus reliability levels, and public training answers. A representation learned from those public fields alone is allowed even if it captures general chemical regularities. It becomes prohibited if it is trained, supervised, initialized, joined, or otherwise anchored to hidden identity or structure labels, an external spectral collection, pretrained weights, or any non-public record. These restrictions require harness-side network and filesystem isolation in addition to grader checks. Extra Modeliing Information IonWeave uses a target mechanism where it asks which observed peak wins a hidden cross-acquisition recurrence trial inside each matched intensity stratum, not which masked values complete the visible spectrum. It also requires ranked evidence retrieval from other molecular groups, and it scores citations by their agreement with a hidden empirical recurrence profile. Connectivity-disjoint evaluation prevents solving the task by recognizing a molecule seen during training. The design-stage is unique because the supervised object is cross-acquisition peak reliability with retrieval-grounded evidence, rather than spectrum reconstruction or molecule identification.
> All-solver grace
> Grace ends in 54m
> $700 Pool
> Lockdown

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Archival Series Filing Context Retrieval

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7e4d0yhc7s6v5j8fhxexc1td8dype6
- DOMAIN exactly as displayed: RAG
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat 3tmvne's score of 0.569!

Full challenge description from page:

> Archival Series Filing Context Retrieval Place each folder description into the archival series that originally held it. For each query, you receive a catalog of 3 to 12 sibling series and their scope descriptions. Predict one series from that query's catalog. Archival filing reflects the work that produced a record. A grant proposal, a report about the resulting research, and a publicity clipping about the same project can belong to different series. Likewise, a person's correspondence may sit in an office's administrative records rather than a series named after the letter's subject. The challenge is to learn how a folder's purpose fits a local filing context, using real archivist-authored descriptions and recorded hierarchy edges as supervision. Series identities change between contexts. Test contexts come from provenance families held out of training, so memorizing a global class number is insufficient. The recorded placement is the target; descriptions can be incomplete, and the task does not assert that every filing decision can be recovered with certainty. Groups defined only by physical box runs and identical ambiguous query descriptions have been excluded. The motivation follows Watanabe and de Sousa (2026), whose survey of automatic records classification highlights the loss of relational archival context. This challenge uses changing sibling catalogs and held-out provenance families to measure that contextual distinction. Related practical work includes Nouws' ArchMapper (2026), an application for manually linking files and folders to retention-schedule series. Here the learning target is an existing archival hierarchy edge. Automatic retrieval must handle changing sibling catalogs and provenance families absent from training. Public data Your script receives the public directory as sys.argv[1]. Paths below are relative to that directory. All identifiers are opaque, case-sensitive strings. They carry no ordering, time, or source information. train.csv: one labeled folder per row. query_id is a unique query identifier of the form q_ followed by 20 lowercase hexadecimal characters. provenance_id is an opaque string of the form p_ followed by 20 lowercase hexadecimal characters; it groups related archival sources. Keep all rows with the same provenance_id together when constructing your validation split. context_id identifies the candidate catalog to use. text is the normalized folder title with any available scope description. selection is the correct candidate's candidate_id. test.csv: the same query_id, provenance_id, context_id, and text feature columns, with selection withheld. Produce one prediction for every row. contexts.json: a JSON array of objects. Each object has a string context_id and a candidates array. Each candidate has a string candidate_id of the form s_ followed by 20 lowercase hexadecimal characters, and a string text containing the series title and scope. Candidate IDs are unique to their context. This file contains catalogs for both train and test contexts. It contains no folder-to-series assignments for test queries. sample_submission.csv: a well-formed random selection from each test query's catalog. It illustrates the format; its selections are independent of the answers. model/: an unmodified pretrained passage reranker, tokenizer, model card and license, supplied for offline use. Load it with AutoTokenizer and AutoModelForSequenceClassification from Transformers, using local_files_only=True. It has not been fine-tuned on this task. You may fine-tune it on the provided labels. model_info.json: the checkpoint's name, pinned revision and license. Names detected by catalog authority tags and a fixed entity recognizer have been replaced by consistent local aliases for people, organizations, places and named items. Dates, numeric catalog references, source IDs and physical container positions are not features. Undetected names can remain in prose. Descriptions are normalized to ASCII, with folder text capped at 160 whitespace tokens and series text at 512. Row and candidate orders are shuffled. Submission Write a CSV directly to the exact file path in sys.argv[2]. Required columns are query_id and selection. For each public test query, select a candidate_id from its own context. IDs below are illustrative; use the actual public IDs when solving. query_id,selection q_124ac567d890ef123abc,s_987ab654c321de456fab q_56de789ab012cf345678,s_123bc456d789ef012abc Rows and columns may be reordered. An extra CSV index column named Unnamed: ... is ignored. Do not output a ranked list, score vector, or candidate text. If your model ties, choose any single candidate; the grader evaluates that choice. Evaluation The score is top-1 accuracy over the graded query set A: accuracy = (1 / |A|) * sum(1[predicted_selection(q) == true_selection(q)] for q in A). Higher is better. The theoretical range is [0, 1]. Every graded query has equal weight. Test contains 3833 queries from 16 provenance groups, 39 contexts and 23 source descriptions. Each of the public and private leaderboard partitions contains eight complete provenance groups; no group, source or context crosses those partitions. A group contributes at most 256 test queries. Visibility labels remain private. The platform may grade a subset of test rows. A complete submission works unchanged for such a subset; extra ungraded rows and their prediction values are ignored, while duplicate submission query keys are always invalid. Missing required columns, duplicate query keys, a missing graded query, or a missing or malformed prediction on a graded row gives 0.0 for that grading call. Prediction IDs must follow the documented string format. A syntactically valid ID that is not the correct series is incorrect for that row. Empty or malformed inputs also receive 0.0. There is no partial credit within a query and no score offset. Extra platform answer columns such as visibility do not affect scoring. Compute The intended tier is A10G. Use only the provided data, supplied weights, and libraries already installed in the Kaggle image. No runtime downloads or installations are needed. The exported script must finish loading, any training, inference and CSV writing in under 30 minutes. Keep a margin for startup and output. Use writable temporary directories for library caches. Do not assume that the runtime user has a username or that the parent of the supplied output file is writable. For PyTorch/Transformers, set TORCHINDUCTOR_CACHE_DIR to a writable temporary directory before importing them. Rules Use only the provided data and the generic checkpoint included with it. Do not recover any test placement by locating a folder or series in the original archive, another finding-aid export, a search engine, or equivalent external data. Do not use externally recovered answer tables, hardcoded source-to-target joins, or model outputs obtained through an external service. Learn from the provided training labels and the supplied context descriptions. Predict test placements from the released evidence; do not attempt to access private answers, raw annotations, preparation internals, or hidden split metadata. &nbsp;
> $700 Pool
> Closes in 5h 55m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## KineScope: Multimodal RAG Evidence Calibration

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79195shybpn6h1mha0pg915h8ebrrr
- DOMAIN exactly as displayed: RAG
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 0.454!

Full challenge description from page:

> KineScope: Multimodal RAG Evidence Calibration Overview Retrieval-augmented systems that answer questions about long field recordings often retrieve compact event representations rather than raw frames. The difficult part is not merely finding something visually similar: the system must decide whether the retrieved evidence supports the temporal relation implied by the query. KineScope is an LLM Evaluation / multimodal RAG evidence-grounding benchmark. Each row contains two anonymized event representations: a query event in the left_ block and a retrieved evidence event in the right_ block. Predict a continuous support score for the query's comparative claim that its event is more persistent than the retrieved event. This is not ordinary object recognition and not a generic independent-row tabular task. Evaluation acquisition sessions are disjoint from training sessions, so a useful evaluator must learn a transferable query-evidence relation rather than memorize a recording, event, or retrieval position. Objective For every row in test.csv, predict one floating-point prediction in [0, 1]: values near 0: the retrieved evidence contradicts the claim because the query event is much less persistent; values near 0.5: the evidence is neutral because the events have similar persistence; values near 1: the retrieved evidence strongly supports the claim because the query event is much more persistent. The score is continuous: both ordering and support magnitude matter. Calibration uses a training-only reference distribution; hidden targets never define the scale. Why this is a RAG evaluation task The left block is the query representation and the right block is the retrieved candidate representation. The submitted value evaluates the candidate's evidential support for a fixed comparative answer, making this a learned multimodal RAG re-ranker/evaluator. No text generation is required, and the output is not an event class or source identity. Each released occurrence is a private projection of temporal visual statistics. The query and evidence blocks use the same anonymous coordinate system, but every occurrence has independent nuisance variation. Exact-vector matching cannot reconnect occurrences or identify their parent observations. Grounding targets combine temporal extent with motion morphology, are normalized within protected acquisition sessions, and are converted to a continuous training-referenced percentile scale. Session averages, camera signatures, a global prior, and duration-only rules are insufficient. Pair order is meaningful: swapping query and evidence reverses the relation. CSV order, identifier spelling, numeric formatting, and vector norms carry no target information. Dataset Split Protected acquisition sessions are assigned before any query-evidence pair or occurrence is generated. No source event or protected session crosses train/evaluation or public/private boundaries. The prepared release contains: 3,630 labelled training query-evidence pairs; 800 evaluation pairs; 255 public and 545 private evaluation pairs; equal sampling across five broad support bands in training, public, and private partitions. The evaluation-to-training row ratio is approximately 22%. Every evaluation pair belongs to exactly one visibility partition. Files train.csv: id, 64 left_ query features, 64 right_ retrieved-evidence features, and continuous target in [0,1]. test.csv: the same identifiers and features without target. sample_submission.csv: the exact required id,prediction schema with a varied label-free example. data_manifest.json: dimensions, target range, neutral baseline, and release row counts. Feature columns are ordered left_0 through left_63, followed by right_0 through right_63. All feature values are finite floating-point numbers. id is an opaque record key, not a feature. Modelling Guidance A strong baseline compares query and evidence with antisymmetric and symmetric features such as left - right, abs(left - right), and coordinate interactions, then learns support calibration from train.csv. Nonlinear pair encoders, Siamese networks, and ensembles can capture additional cross-block interactions. Validation should hold out complete groups of related training rows. Random row validation can be optimistic because related rows may share acquisition conditions. Evaluation The leaderboard uses normalized RMSE skill relative to the neutral evidence prediction 0.5: RMSE = sqrt(mean((prediction - target)^2)) null_RMSE = sqrt(mean((0.5 - target)^2)) score = max(0, 1 - RMSE / null_RMSE) Scores lie in [0, 1], higher is better, and exact answers score 1.0. Predicting 0.5 everywhere scores exactly 0.0 on full, public, and private answers. Valid but worse predictions are clipped to 0.0. The grader aligns rows by id, so submission row order has no effect. The same formula is applied independently to public and private answer subsets. Submission Format Submit a CSV with exactly these columns in this order: id,prediction 0123456789abcdefabcd,0.73 abcdef0123456789abcd,0.18 Every test ID must appear exactly once. Predictions must be finite numeric values in [0,1]. Wrong or reordered columns, missing rows, duplicate IDs, unknown IDs, non-numeric values, non-finite values, and out-of-range values raise a structural validation error. Restrictions Use only the released challenge files. Do not use external media, labels, datasets, APIs, pretrained event models, hosted embeddings, or challenge-specific checkpoints. Do not attempt to identify parent recordings, source events, acquisition sessions, or the upstream dataset. Do not exploit IDs, row order, hashes, CSV byte layout, numeric formatting, repeated-submission probing, or leaderboard feedback. Do not adapt a model using hidden labels or manually label evaluation rows. Generate the final submission automatically from supplied training pairs and evaluation features. &nbsp;
> 4 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.


# CPU Fine-Tuning Challenge Examples

Scrape timestamp: 2026-07-14T00:00:00+05:30

Confirmed CPU examples in this document: 0

These entries are included because the challenge detail page displayed this domain and the challenge is part of the CPU-only challenge collection.

## AuditClause -Evidence Conditioned Semantic Fault Localization

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dbaa3gz3rkv8j7weej2pvtn8amx1w
- DOMAIN exactly as displayed: Fine-Tuning
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Federal accounting policies are frequently reviewed against a large body of standards, interpretations, technical bulletins, technical releases, and implementation guidance. A draft memo can appear professionally written while changing a single word that reverses an obligation, swaps an accounting treatment, assigns responsibility to the wrong party, or applies a requirement at the wrong time.
> This challenge asks you to audit short policy memos at the clause level.
> Each episode contains:
> one evaluation instruction;
> an evidence packet containing between 3 and 6 standards excerpts;
> a memo containing between 3 and 6 independently identified clauses.
> For every memo clause, predict whether it is fully supported by the evidence packet. When it is not supported, identify the precise semantic fault type.
> This is an NLP challenge. It is not response ranking, ordinary document retrieval, or question answering. The output is a structured clause-by-clause semantic audit.
> Real-world context and data origin
> The challenge is prepared from a 2,914-page public United States government handbook that consolidates federal accounting concepts, accounting standards, interpretations, technical bulletins, technical releases, and staff implementation guidance. The source material is current through June 30, 2025.
> The preparation pipeline:
> extracts sentence-centered evidence windows from the handbook;
> preserves the surrounding context needed to interpret each selected sentence;
> creates a short memo clause through meaning-preserving paraphrase;
> leaves the clause faithful or applies one controlled semantic fault;
> assigns the resulting clause label after the transformation;
> shuffles evidence and memo-clause order independently.
> The target labels do not exist in the source handbook. Identifying the original document does not reveal a test answer because every memo, clause ID, transformation, and label is created during preparation. Every distinction required for scoring is visible in the supplied evidence packet.
> Objective
> For each test episode, assign exactly one of the seven allowed labels to every clause_id.
> The labels are:
> supported — the clause preserves the meaning of a supplied evidence excerpt.
> modality_shift — obligation strength or permission is changed, such as may versus must.
> treatment_swap — the accounting action is changed, such as recognition versus disclosure.
> role_reversal — responsibility or party identity is reversed, such as lessee versus lessor.
> category_swap — an accounting category is replaced by an opposing category, such as asset versus liability.
> timing_reversal — the applicable time or sequence is reversed, such as before versus after.
> scope_negation — scope, exception, quantification, or negation is materially changed.
> A clause must be labelled supported only when its complete meaning is grounded in one of the supplied excerpts. Similar vocabulary alone is insufficient.
> Dataset files
> train.csv
> Contains 4,000 labelled training episodes.
> Columns:
> sample_id — unique episode identifier.
> instruction — clause-audit instruction for the episode.
> evidence — JSON list containing 3 to 6 evidence objects.
> memo_clauses — JSON list containing 3 to 6 memo-clause objects.
> labels — JSON object mapping every clause ID to one allowed label.
> An evidence cell has this structure:
> [
> {
> "evidence_id": "e_12ab34cd56ef",
> "source_type": "standard",
> "text": "Evidence excerpt text..."
> },
> {
> "evidence_id": "e_98fe76dc54ba",
> "source_type": "technical_release",
> "text": "Another evidence excerpt..."
> }
> ]
> Possible source_type values are:
> concept
> standard
> interpretation
> technical_bulletin
> technical_release
> staff_guidance
> A memo_clauses cell has this structure:
> [
> {
> "clause_id": "c_a1b2c3d4e5f6",
> "text": "The memo clause text..."
> },
> {
> "clause_id": "c_1029384756ab",
> "text": "Another memo clause..."
> }
> ]
> A training labels cell has this structure:
> {
> "c_a1b2c3d4e5f6": "supported",
> "c_1029384756ab": "timing_reversal"
> }
> test.csv
> Contains 600 unlabelled test episodes.
> It has the same columns as train.csv except that labels is omitted.
> sample_submission.csv
> Contains:
> sample_id
> labels
> The file is pre-filled with supported for every clause. It is only a schema example and a valid starting file. The pre-filled values are not predictions supplied by the challenge and are not expected to score well.
> Submission format
> Write the final file to:
> ./working/submission.csv
> The submission must contain exactly these columns:
> sample_id
> labels
> Each labels value must be a valid JSON object that maps every clause ID in that episode to exactly one allowed label.
> Example:
> sample_id,labels
> te_91f0a2b3c4d5e6f7,"{""c_1029384756ab"":""timing_reversal"",""c_a1b2c3d4e5f6"":""supported""}"
> For every episode:
> every clause ID must appear exactly once;
> no unknown clause ID may be included;
> no clause may be omitted;
> every value must be one of the seven allowed labels.
> A submission is rejected when it contains missing or extra sample IDs, duplicate sample IDs, malformed JSON, missing clause IDs, unknown clause IDs, or unknown labels.
> Evaluation
> Raw metric
> The raw metric is clause-level macro F1 across the seven labels.
> For each label:
> F1 = 2 precision recall / (precision + recall)
> The raw score is the unweighted mean of the seven class-specific F1 values. Consequently, the frequent supported class cannot dominate the metric and rare semantic fault types remain important.
> Skill normalization
> The leaderboard score is normalized against a fixed, reproducible lexical-alignment baseline.
> B = 0.6669957123097011
> score = clip((macro_f1 - B) / (1 - B), 0, 1)
> Higher is better.
> Theoretical minimum: 0.0
> Theoretical maximum: 1.0
> A perfect submission scores 1.0.
> The supplied sample submission scores 0.0.
> Exact normalization baseline
> The fixed baseline is produced as follows:
> Lowercase and tokenize every evidence excerpt and memo clause with the pattern [a-z][a-z0-9'-]{1,}.
> Remove this fixed stopword set:
> an and are as at be been being by for from has have if in into is it its of on or that the their this to was were when which with would than then there these those such under upon also each other more most same through within
> Align each memo clause to the evidence excerpt having the highest binary-token cosine similarity:
> similarity = shared_tokens / sqrt(clause_tokens * evidence_tokens)
> Count evidence-to-clause contrast hits using these groups:
> modality_shift:
> should→may, shall→may, must→may, may→must,
> required→optional, requires→permits, require→permit,
> is expected to→may, is required to→may, is permitted to→must,
> should→is permitted to, may→is required to,
> shall→is permitted to, must→is permitted to
> treatment_swap:
> recognize→disclose, recognized→disclosed,
> recognition→disclosure, disclose→recognize,
> disclosed→recognized, disclosure→recognition,
> recognize→report, disclose→record,
> recognized→reported, disclosed→recorded
> role_reversal:
> lessee→lessor, lessor→lessee,
> transferor→transferee, transferee→transferor,
> debtor→creditor, creditor→debtor,
> buyer→seller, seller→buyer
> category_swap:
> asset→liability, assets→liabilities,
> liability→asset, liabilities→assets,
> revenue→expense, revenues→expenses,
> expense→revenue, expenses→revenues,
> exchange→nonexchange, nonexchange→exchange
> timing_reversal:
> before→after, after→before,
> current→future, future→current,
> initially→subsequently, subsequently→initially,
> initial→subsequent, subsequent→initial,
> before→following, after→prior to
> scope_negation:
> only→generally, all→some, any→no,
> except→including, unless→when
> Predict the class with the largest number of contrast hits.
> Break ties in this fixed order:
> modality_shift, treatment_swap, role_reversal,
> category_swap, timing_reversal, scope_negation
> Predict supported when no contrast group has a hit.
> The fixed baseline obtains raw macro F1 equal to B on the hidden test set. This fully specifies both the normalization value and the method used to obtain it.
> What makes this challenge distinct
> This challenge does not ask models to rank candidate responses or retrieve one relevant passage.
> A model must jointly perform:
> clause-to-evidence alignment inside a variable-size packet;
> semantic entailment checking;
> contradiction detection;
> fine-grained error typing;
> structured multi-clause output generation.
> The same surface term can be correct in one episode and faulty in another. For example, must is not inherently an error; it becomes a modality_shift only when the aligned evidence supports weaker permission.
> Compute and runtime
> Solutions must use CPU computation only.
> The grading environment provides:
> 10 CPU cores;
> 62.5 GiB RAM;
> an expected maximum runtime of 1.5 hours.
> The submitted script must perform preprocessing, training, inference, and submission generation end to end within that budget.
> Allowed
> The following are allowed:
> general-purpose pretrained language-model weights obtained through installed libraries;
> genuine model training or fine-tuning inside the submitted script;
> compact cross-encoders, natural-language-inference models, token encoders, and learned clause classifiers;
> train-only cross-validation, early stopping, and calibration;
> lexical or structural features used as auxiliary inputs to a genuinely trained model;
> multiple trained models inside one end-to-end script;
> independent per-episode inference or ordinary production-style mini-batches;
> fixed random seeds and deterministic preprocessing.
> Not allowed
> The following are prohibited:
> GPU or CUDA use;
> external training datasets, external corpora, or external labelled examples;
> searching for or reconstructing the original source document to solve test episodes;
> runtime package installation;
> downloading custom code or research repositories from GitHub;
> loading self-hosted or previously fine-tuned challenge-specific weights;
> inference-only solutions with no real training or fine-tuning;
> pure regex, substitution tables, lexical matching, TF-IDF, BM25, or other rule-only pipelines as the primary solution;
> generating additional synthetic training examples outside the supplied training data;
> pseudo-labelling the test set;
> test-time adaptation or calibration based on the overall test distribution;
> using sample IDs, clause IDs, evidence order, clause order, or row order as predictive features;
> sharing information across test episodes during inference;
> loading cached embeddings or predictions from an earlier submission run.
> A frozen embedding model may be one component, but a major part of the final evaluator must be genuinely trained or fine-tuned on the released training episodes.
> Suggested solution direction
> A strong CPU solution may:
> parse each evidence packet and memo;
> retrieve the most likely evidence excerpt for each clause;
> fine-tune a compact pretrained cross-encoder or natural-language-inference model;
> train a seven-class clause classifier with class-aware loss;
> validate with source-family-aware folds;
> optionally ensemble a small number of CPU-feasible folds;
> output one label for every clause in every test episode.
> The challenge rewards evidence-conditioned semantic evaluation. Memorizing isolated trigger words is not sufficient because the correct label depends on the relationship between the clause and its aligned evidence.

Inspiration note: Useful because it frames fine-tuning as evidence-conditioned semantic fault localization, with contract/legal-style text and structured error spans rather than generic classification.

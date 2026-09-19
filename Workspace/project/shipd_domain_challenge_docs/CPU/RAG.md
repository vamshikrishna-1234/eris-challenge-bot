# CPU RAG Challenge Examples

Scrape timestamp: 2026-07-19T00:00:00+05:30

Confirmed CPU examples in this document: 6

These entries are included because the challenge detail page displayed this domain and the challenge is part of the CPU-only challenge collection.

## Subsurface Report Continuity Ranking
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71e8pz8hb950w840xp2zpjyd8a69ph
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↓ Lower is better
- Tags: text
- Best/top context found: Added from user-provided Shipd CPU-only challenge URL on 2026-07-14; no leaderboard rank context captured.

Full challenge description from page:

> Subsurface Report Continuity Ranking
> Overview
> Technical subsurface reports are often recovered from OCR pipelines as disconnected page snippets. A useful retrieval system must stitch those snippets back into coherent local sequences before analysts can inspect licensing history, seismic interpretation, prospect updates, and resource assessments. When source text cannot be exposed, privacy-preserving retrieval may operate on de-identified token-equality traces instead of readable pages.
> In this RAG challenge, each row gives a lossy token trace from the trailing excerpt of one OCR page and five token traces derived from candidate pages. Exactly one candidate comes from the true next page in the same hidden report. Your task is to rank all five candidates from most likely to least likely continuation.
> Every source token is replaced with a row-local term_### handle, and a deterministic 10% subset is omitted. Equal handles within a row represent the same original token. Handles do not carry meaning across rows. Token order is preserved after omission. This removes source identity while retaining within-slate lexical recurrence and sequence structure.
> This is a document-retrieval problem, not a source-lookup task. Strong solutions should compare within-row handle recurrence, boundary order, trace length, and repeated-token structure while accounting for OCR-derived truncation and deterministic token omission.
> Candidate slates are constructed so that whole-trace handle overlap is similar to the true continuation. Plain overlap counting is therefore weak; useful retrieval signal comes from ordered handle transitions, repeated short sequences, and context-tail to candidate-head continuity.
> Dataset
> File descriptions
> train.csv -- 180 labeled continuity-ranking rows. Each row contains one context, five candidate continuation traces, and the correct candidate label.
> test.csv -- 180 unlabeled continuity-ranking rows with the same input columns, but without correct_candidate.
> sample_submission.csv -- A template with random candidate permutations for every test row.
> Column descriptions
> id (string) -- Unique 12-character hex identifier for each ranking row.
> context (string) -- Lossy token trace derived from the final 1000-character OCR excerpt of a report page.
> candidate_a (string) -- Lossy candidate-page token trace labeled A.
> candidate_b (string) -- Lossy candidate-page token trace labeled B.
> candidate_c (string) -- Lossy candidate-page token trace labeled C.
> candidate_d (string) -- Lossy candidate-page token trace labeled D.
> candidate_e (string) -- Lossy candidate-page token trace labeled E.
> correct_candidate (string) -- Train-only label indicating which candidate is the true continuation.
> Evaluation
> Submissions are scored with Normalized Reciprocal Rank Loss. Lower is better. This is the complement of reciprocal rank, normalized so that placing the correct candidate last scores 100.
> def normalized_reciprocal_rank_loss(correct_label, submitted_ranking):
> labels = submitted_ranking.split("|")
> rank_index = labels.index(correct_label)
> reciprocal_rank_loss = 1.0 - 1.0 / (rank_index + 1.0)
> worst_loss = 1.0 - 1.0 / len(labels)
> return 100.0 * reciprocal_rank_loss / worst_loss
> The final score is the mean loss over all test rows. Correct ranks from first through fifth incur losses of 0, 62.5, 83.33, 93.75, and 100. A random full ranking has an expected score of about 67.92.
> Submission
> Submit a CSV file with one ranked permutation for every row in test.csv.
> id (string) -- The row identifier from test.csv.
> ranking (string) -- A pipe-separated permutation of all five labels: A|B|C|D|E.
> Example:
> id,ranking
> 9edbfd9e611f,B|D|C|A|E
> 9d679a940ff8,E|A|C|B|D
> f1e8ade264bc,A|C|B|E|D
> Requirements
> The file must contain exactly 180 rows plus the header.
> Every id from test.csv must be present exactly once.
> Every ranking value must contain each of A, B, C, D, and E exactly once.
> File format: .csv only, with exact column names id,ranking.
> What Not To Use
> Do not use external copies of the original technical-report corpus, report PDFs, or web mirrors to recover held-out page order.
> Do not reverse-search public snippets to identify source filenames, document identifiers, page numbers, or the true next page.
> Do not build lookup tables from source report names, page-order maps, or external OCR exports. The intended task is continuity ranking from the public excerpts only.

Inspiration note: Useful because it makes retrieval over de-identified sequence traces CPU-friendly: solvers rank candidate continuations rather than training a heavy generative model.

## Grounded Quantity Context Scoring

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70qd66kmscg6ketk5121bd5x8a7k6g
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd CPU-only challenge URL on 2026-07-14; no leaderboard rank context captured.

Full challenge description from page:

> Grounded Quantity Context Scoring
> Overview
> Retrieval-augmented question answering systems often need to choose a small grounding context before extracting a numerical answer. Your task is to assign a utility score to each topic-context pair so a RAG pipeline can keep the most useful context rows for quantity-grounded answering.
> Each topic is represented as an anonymized lexical profile for a quantity-seeking request. Each context row contains anonymized title and abstract profiles produced with the same token mapping. Numeric values are masked before tokenization, so the task focuses on answer-yield context utility instead of direct quantity copying. A high-scoring solution should learn which context rows are likely to contain concentrated measurement evidence for the requested profile, not just which rows share the most common tokens.
> Dataset
> File descriptions
> topics.csv -- Quantity-seeking topics represented as anonymized lexical token profiles.
> contexts.csv -- Anonymized title and abstract profiles for scientific context rows.
> train.csv -- Labeled topic-context rows with the target variable utility.
> test.csv -- Held-out topic-context rows without the target variable.
> sample_submission.csv -- A template with the required row_id and utility_score columns, filled with random baseline predictions.
> Column descriptions
> row_id (string) -- Unique hashed identifier for a topic-context row.
> topic_id (string) -- Unique hashed identifier for a quantity-seeking topic.
> evidence_id (string) -- Unique hashed identifier for a context row.
> query_profile (string) -- Space-separated anonymized lexical tokens for the topic request.
> title_profile (string) -- Space-separated anonymized lexical tokens for a context title.
> abstract_profile (string) -- Space-separated anonymized lexical tokens for a context abstract. Numeric values are masked before tokenization.
> utility (float) -- Training target. Higher values mean the context row contains more distinct masked quantity evidence for grounding the topic. Broad topical relevance alone can still have low utility.
> Evaluation
> Submissions are scored using RAG Answer-Yield Utility@3. For each topic, the grader evaluates the three context rows with the largest submitted utility_score values. True utility is accumulated with logarithmic position discount and normalized by the best possible three-row context set for that topic. Topic scores are averaged.
> from math import log2
> from statistics import mean
> def discounted_utility(utilities):
> return sum(utility / log2(position + 2)
> for position, utility in enumerate(utilities))
> def topic_score(topic_rows):
> # topic_rows contains all submitted rows for one topic.
> # Each row has a submitted utility_score and a hidden true utility.
> submitted = sorted(
> topic_rows,
> key=lambda row: (-row.utility_score, row.row_id),
> )[:3]
> ideal = sorted(
> topic_rows,
> key=lambda row: (-row.utility, row.row_id),
> )[:3]
> achieved = discounted_utility([row.utility for row in submitted])
> best = discounted_utility([row.utility for row in ideal])
> return 1.0 if best == 0 else achieved / best
> score = mean(topic_score(topic) for topic in topics)
> Scores range from 0 to 1, and higher is better.
> Submission
> Submit a CSV file with a score for every row in test.csv.
> row_id (string) -- The exact pair identifier from test.csv.
> utility_score (float) -- Your predicted context utility score. Larger values indicate stronger grounding context for that topic.
> Example:
> row_id,utility_score
> row_ac4427a3c403,0.7342
> row_6958a50c0735,0.1125
> row_508b3dfa5e93,0.4819
> Requirements
> The file must contain exactly one row for every row in test.csv.
> Every row_id from test.csv must be present exactly once.
> Predictions must be finite numeric values.
> File format: .csv only, with exact column names row_id,utility_score.
> What Not To Use
> Do not use web search, external article databases, or outside copies of the underlying context records to recover hidden relevance judgments or quantity annotations.
> Do not reverse-map hashed topic or evidence identifiers to original corpus identifiers.
> Do not submit cached labels or lookup tables from outside the provided public files; solutions should infer context utility from the anonymized topic and context profiles.

Inspiration note: Useful because it frames RAG as context utility ranking over anonymized profiles, using top-k discounted utility rather than direct answer extraction.

## Cross-Temporal FDA Report Ranking

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79dq9ebfpxh6x2bcqcndd0j98am5t5
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, medical, small-data
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Rare regulatory concepts can change surface form as devices, manufacturers, and reporting practices evolve. An analyst may have an official terminology definition and a few historical examples, yet still need to recognize the same underlying problem in later reports from an unfamiliar device context.
> Each query in this challenge contains three independent forms of real evidence:
> an official IMDRF term and definition;
> the official top-level terminology-family name; and
> two real historical FDA-originated reports carrying the same withheld leaf annotation.
> The query is paired with 24 real reports from a later period. Exactly one candidate shares the anchors' withheld source leaf annotation. The other 23 are taxonomy-near negatives selected from the closest available related branches; eight are additionally mined for high non-TF-IDF token overlap with the supplied definition and anchors. Participants rank the candidates from most to least likely to express the same regulatory concept as the definition and historical anchors.
> The leaf code itself is not included in any prepared public file. Train, validation, and test are disjoint at the top-level taxonomy-family level, not merely at the individual-label level. Test therefore evaluates analogy transfer to both unseen leaf concepts and unseen terminology families under temporal change.
> This is a cross-temporal, dual-anchor regulatory analogy-retrieval task. It is not report classification, ordinary label retrieval, code prediction, or uncertainty estimation.
> All terms and definitions are official terminology text. Every anchor and candidate is a deterministically obfuscated view of one real FDA-originated report. Relevance is derived directly from the original source annotations. No synthetic reports, generated definitions, paraphrases, artificial examples, or model-generated labels are used.
> Target Output
> For every test query_id, predict:
> ranked_candidate_ids
> The value is a pipe-separated sequence of candidate IDs ordered from highest to lowest predicted relevance.
> Example:
> cand_17a61ed24ab048d52d89b62e|cand_a058bad83c41a9f135971ec0|cand_64dbe8ac90275f14263076ef
> A ranking may contain zero through 24 candidates. If the relevant candidate is omitted, that query receives a reciprocal rank of 0. Including all 24 candidates guarantees that the relevant report is ranked, but its position determines the score.
> Only candidate IDs belonging to the corresponding query_id are valid. Candidate row order and identifier order contain no relevance signal.
> Evaluation
> Submissions are evaluated using Mean Reciprocal Rank (MRR).
> For each query:
> RR = 1 / rank_of_relevant_candidate
> If the relevant candidate is not submitted, RR = 0. The final score is:
> MRR = mean(RR across all graded queries)
> MRR is bounded in [0, 1]; higher is better. The grader returns standard MRR directly, without offsets, clipping, rescaling, or model-specific rules. Ranking order is evaluated as a sequence and is never converted to a set.
> With one relevant item among 24 candidates, the theoretical expected MRR of a uniformly random complete ranking is 0.157332. This is an expectation, not a score offset or floor; a submission that omits every candidate scores 0.0.
> Organizer Baselines
> The following frozen reference methods were evaluated once on the complete private test set. None was tuned against private labels:
> | Baseline | MRR |
> |---|---:|
> | Theoretical uniform-random expectation | 0.157332 |
> | Deterministic shuffled sample order | 0.167034 |
> | Report-length ordering | 0.162582 |
> | Non-TF-IDF definition token-frequency cosine | 0.218147 |
> | Non-TF-IDF dual-anchor token-frequency cosine | 0.151697 |
> | Frozen all-MiniLM-L6-v2 definition embedding | 0.217546 |
> | Frozen all-MiniLM-L6-v2 dual-anchor embedding | 0.198718 |
> | Frozen all-MiniLM-L6-v2 definition-plus-anchor embedding | 0.215357 |
> The MiniLM baselines use mean pooling, 128-token truncation, cosine ranking, no fine-tuning, and no challenge-specific training. These results establish substantial headroom below 1.0; a stock semantic retriever does not approach the previously observed 0.69 agent score.
> Under an independent uniform-rank reference model, the standard error of mean reciprocal rank is approximately 0.00967 for 450 queries, compared with 0.01636 for the former 270-query, nine-candidate design. The expanded test therefore improves leaderboard resolution while retaining standard, unmodified MRR.
> Dataset
> The prepared challenge contains:
> public/train.csv
> public/validation.csv
> public/test.csv
> public/sample_submission.csv
> public/prepared_schema.txt
> private/answers.csv
> The source concepts are 57 extreme-tail IMDRF leaf annotations. Every selected concept occurs 5-29 times in the 2015-2023 source training period, at least 5 times in January-June 2024, and at least 10 times in July 2024-June 2025.
> | Split | Leaf concepts | Top-level families | Queries | Candidate rows |
> |---|---:|---:|---:|---:|
> | Train | 15 | 8 | 216 | 5,184 |
> | Validation | 7 | 3 | 98 | 2,352 |
> | Test | 35 | 17 | 450 | 10,800 |
> Each concept contributes up to 20 distinct later-period positive reports. Train concepts contribute 5-20 queries, validation concepts contribute 5-20 queries, and test concepts contribute 10-20 queries. Every query contains two historical anchors, one relevant later-period candidate, eight mined hard negatives, and 15 additional taxonomy-near negatives.
> Files And Columns
> public/train.csv and public/validation.csv contain labeled candidate pairs:
> query_id: episode-local anonymized query identifier.
> query_term: official IMDRF term; the source code is withheld.
> query_definition: official IMDRF definition.
> family_term: official name of the concept's top-level taxonomy family.
> anchor_text_1: query-locally obfuscated text of the first real historical anchor.
> anchor_text_2: query-locally obfuscated text of a second distinct real historical anchor.
> candidate_id: episode-local candidate identifier.
> event_text: query-locally obfuscated text of one real later-period candidate report.
> relevance: 1 for the one matching candidate and 0 for a hard negative.
> public/test.csv contains the same columns except relevance, which is withheld.
> public/sample_submission.csv contains:
> query_id: matching test query identifier.
> ranked_candidate_ids: pipe-separated candidate ranking in deterministic shuffled input order.
> private/answers.csv contains:
> query_id: matching test query identifier.
> candidate_ids: complete candidate pool for validation.
> relevant_candidate_ids: the single withheld relevant candidate.
> public/prepared_schema.txt provides a compact machine-readable summary of these schemas.
> Cross-Temporal Construction
> All anchors come from real 2015-2023 reports. Train and validation candidate pools come from January-June 2024. Test candidate pools come from July 2024-June 2025.
> For each query, positives are later-period reports carrying the same original leaf annotation as both anchors. Negatives do not carry that annotation. Immediate-parent negatives are selected first; broader-ancestor negatives are used only when necessary.
> Within the closest available hierarchy depth, eight negatives are mined by raw token-frequency cosine overlap with the official query text and both anchors. No inverse-document-frequency values or TF-IDF features are used. The remaining 15 negatives are deterministically sampled from the same depth-first taxonomy pools. Duplicate source records and duplicate report narratives are excluded within each query. This mixture prevents a stock lexical or semantic retriever from solving the task while retaining real, taxonomy-confusable candidates.
> The two anchors are distinct reports. Every positive report is used at most once for a given concept, and no concept contributes more than 20 episodes. Reports are never generated, summarized, paraphrased, or combined into synthetic narratives. The only text transformation is the deterministic token obfuscation described below.
> Query-Local Obfuscation
> Report text is protected against exact lookup in public MAUDE mirrors using one-way query-local token replacement:
> Official IMDRF terminology words longer than two characters remain readable.
> Only an explicit fixed list of function words remains readable among short tokens.
> Numbers, short non-function acronyms, names, model identifiers, manufacturers, and all other content tokens are replaced by query-salted hash tokens.
> One source token maps consistently across both anchors and all 24 candidates within a query, preserving local repetition and analogy evidence.
> The mapping changes across queries, so no global token dictionary or cross-query lookup key exists.
> Punctuation and token order are retained; no new semantic content is introduced.
> Raw report text and original report identifiers do not appear in prepared public files. The obfuscation changes representation only; it does not create reports, change row membership, or determine relevance.
> Family-Disjoint Generalization
> Concepts are grouped by their top-level IMDRF taxonomy family before splitting. An entire family belongs to exactly one challenge split:
> Train: 15 concepts from 8 families.
> Validation: 7 concepts from 3 different families.
> Test: 35 concepts from 17 families absent from both train and validation.
> The split is deterministic and capacity-constrained. It also enforces minimum coverage of 8 train families, 3 validation families, and 15 test families without hard-coding any family or leaf code. No test leaf or top-level family serves as a labeled query in train or validation. Validation measures transfer to unseen families before private test evaluation.
> Target Provenance
> Relevance means that the candidate and both anchors carry the same withheld leaf code in the original regulatory annotations. It is not determined by lexical overlap, document length, candidate position, an annotation-geometry formula, or any public auxiliary column.
> These source annotations are operational regulatory labels, not claims of clinically validated causality. The challenge evaluates recovery of the source annotation relationship only.
> Leakage And Stability Safeguards
> Public query IDs are derived from split, hidden concept, and episode ordinal, not report IDs.
> Candidate IDs are derived only from query ID and shuffled position. Original FDA record identifiers never appear in prepared files or public identifiers.
> Candidate order is deterministic but independent of relevance; position and identifier order are prohibited as features.
> Query-local token salts prevent exact report matching and prevent a reusable global content-token mapping.
> The 450 test queries cover 35 hidden leaf concepts, with 10-20 distinct positive-report episodes per concept.
> Each private answer row contains one complete query and its candidate pool, so leaderboard splitting cannot divide an episode.
> The target cannot be recomputed from public columns; it requires the withheld original annotation.
> All documented public columns are emitted by prepare.py; no promised auxiliary training signal is missing.
> Text fields use standard CSV quoting and may contain commas, quotation marks, and embedded line breaks.
> What Makes This Task Different
> The task combines four generalization requirements:
> definition grounding from official terminology;
> analogy matching from two real historical exemplars;
> temporal transfer to later reports; and
> ontology-family transfer to families absent from training.
> The output is an episode-level future-report ranking, not a code set. The source code is withheld, test families are unseen, and the matching function must triangulate terminology semantics with two historical narratives. A fixed classification head, per-label threshold, or direct MADE-style multi-label prediction output cannot solve or emit this task without being redesigned.
> CPU Environment
> All solutions run with 10 CPU cores and 62.5 GiB RAM. No GPU or external accelerator is available.
> Suitable approaches include exact terminology matching, token-overlap features, character-overlap features, hierarchy-aware lexical features, CPU-compatible compact sentence embeddings, pairwise ranking, and calibrated similarity ensembles.
> TF-IDF representations, TF-IDF similarity, and TF-IDF-derived ranking features are not allowed.
> Real-Data Requirement
> Only the supplied official terminology and real reports may be used as task-specific data. The following are prohibited:
> generated or manually fabricated reports;
> generated definitions, summaries, paraphrases, or hypothetical reports;
> back-translation or augmentation that creates new text;
> synthetic positives, negatives, or SMOTE-style feature vectors; and
> external MAUDE/openFDA reports used as extra examples or for test-record matching.
> Deterministic normalization, CPU-compatible embeddings computed from supplied text, class weighting, and resampling references to unchanged prepared rows are allowed because they do not create synthetic observations.
> What Not To Use
> Private labels, private relevant-candidate IDs, or grader leakage.
> Original report IDs, hidden preparation artifacts, row order, query IDs, or candidate IDs as prediction features.
> External record matching against MAUDE, openFDA, dataset mirrors, caches, or search engines.
> Synthetic data or generated text.
> TF-IDF methods or TF-IDF-derived features.
> GPU or external accelerator execution.
> Hard-coded answer reconstruction or submission-parser exploits.
> Expected solutions should learn a general matching function across terminology, historical examples, and later candidate reports.
> Submission Format
> Write the final file to:
> ./working/submission.csv
> It must contain exactly these columns in this order:
> query_id,ranked_candidate_ids
> Example:
> query_id,ranked_candidate_ids
> query_0123abcd45ef67890123abcd,cand_17a61ed24ab048d52d89b62e|cand_a058bad83c41a9f135971ec0
> query_abcdef0123456789abcdef01,cand_901dca734b18e45f23a067bc
> query_13579bdf2468ace013579bdf,
> Submission Requirements
> Include every test query_id exactly once.
> ranked_candidate_ids may be empty or contain unique IDs from that query, separated by |.
> Candidate order must run from highest to lowest predicted relevance.
> Unknown IDs, cross-query IDs, duplicates, whitespace, empty separator elements, missing queries, and extra columns are invalid.
> Readable invalid submissions receive 0.0. A missing or unreadable file is handled by the platform submission loader before grade.py is called.

Inspiration note: Useful because it frames retrieval as cross-temporal regulatory report ranking, with small-data medical text features and a ranking metric that rewards finding historically relevant evidence.

## Compromised Sources: Corpus-Level Poison Forensics for Retrieval

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dfnbhm6kgn7n32ctmd6w3gn8ahfpm
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> A retrieval-augmented system does not read one document in isolation. It reads from a
> shared corpus, and the same source publishes many of the passages it retrieves across many
> different questions. When an attacker compromises a source, every passage from that source
> becomes suspect, not just the one in front of you. Defending the system means identifying
> the compromised sources, and to do that you have to look across the whole corpus, because no
> single retrieval result gives it away.
> Each sample is one retrieval result: a question, and the ten passages returned for it. Every
> passage is tagged with the numeric id of the source that published it, and the same sources
> recur throughout the dataset. Some passages carry an injected claim, a fluent sentence that
> asserts an answer to the question outright. Compromised sources tend to assert false answers;
> honest sources tend to assert correct ones, though neither is perfectly consistent. Whether a
> passage carries a claim at all is independent of its source, so the mere presence of a claim
> tells you nothing.
> Within a single retrieval result you cannot tell a compromised source from an honest one. A
> claim that looks wrong might come from an honest source having an off day, and a claim that
> looks right might come from a compromised source that told the truth this once. The signal
> only emerges when you pool a source across the many questions it appears in and ask whether,
> on balance, it tends to contradict the answer supported by the underlying evidence.
> The original passage text was never edited. Only whole sentences were inserted, so the
> genuine evidence that answers each question is still present, and the true answer is always
> recoverable by reading it.
> For every question you must report two things: the true answer, and the set of passages that
> came from a compromised source. A passage counts as compromised if its source is compromised,
> even when the passage itself carries no claim or happens to state the truth.
> Evaluation
> Two components are combined per question and averaged over all questions. The first is the
> SQuAD-style token-level F1 between your predicted answer and the true answer. The second is
> the set F1 between the passage indices you flag as coming from a compromised source and the
> true set. The answer counts for 0.25 and the compromised-passage detection for 0.75.
> from collections import Counter
> import re
> import string
> def normalize(text):
> s = str(text).lower()
> s = s.translate(str.maketrans("", "", string.punctuation))
> s = re.sub(r"\b(a|an|the)\b", " ", s)
> return " ".join(s.split())
> def token_f1(pred, gold):
> p, g = normalize(pred).split(), normalize(gold).split()
> if not p or not g:
> return float(p == g)
> common = Counter(p) & Counter(g)
> n = sum(common.values())
> if n == 0:
> return 0.0
> precision, recall = n / len(p), n / len(g)
> return 2.0 * precision * recall / (precision + recall)
> def set_f1(pred_ids, gold_ids):
> p, g = set(pred_ids), set(gold_ids)
> if not p and not g:
> return 1.0
> if not p or not g:
> return 0.0
> inter = len(p & g)
> if inter == 0:
> return 0.0
> precision, recall = inter / len(p), inter / len(g)
> return 2.0 * precision * recall / (precision + recall)
> def evaluate(rows):
> total = 0.0
> for pred_answer, gold_answer, pred_ids, gold_ids in rows:
> total += 0.25 * token_f1(pred_answer, gold_answer) + 0.75 * set_f1(pred_ids, gold_ids)
> return total / len(rows)
> Scores range from 0.0 to 1.0. A placeholder answer with nothing flagged scores about 0.10.
> Flagging all ten passages in every row scores about 0.22. Approaches that judge each
> retrieval result on its own, without estimating source reliability across the corpus, top out
> around 0.34. Because a source's reliability must be inferred from only a dozen or so of its
> claims, the two source populations overlap and perfect detection is not possible; a strong
> solution is expected to score in the 0.5 to 0.65 range, not near 1.0.
> Relation to prior work
> The attack model comes from PoisonedRAG (arXiv:2402.07867), which showed that planting a few
> crafted passages in a retrieval index is enough to make a RAG system repeat a false answer,
> and from CPA-RAG (arXiv:2505.19864) on covert variants. The defensive goal of tracing which
> retrieved content was poisoned is the subject of RAGForensics (arXiv:2504.21668).
> This challenge departs from all of them in what it asks for. Those works judge poisoning one
> query at a time: given a retrieval result, decide which passages in it are malicious. Here the
> unit of compromise is the source, not the passage. A passage is to be quarantined because of
> who published it, so a passage from a compromised source must be flagged even when it carries
> no claim at all, or happens to state the truth. That label is invisible within any single
> retrieval result and can only be recovered by pooling a source's behaviour over the many
> questions it appears in. The test split further uses source ids that never occur in train, so
> reliability cannot be memorised from the training labels and must be estimated on the test
> corpus itself.
> Dataset
> Built from HotpotQA in its distractor configuration, the multi-hop open-domain question
> answering benchmark over English Wikipedia (Yang et al., 2018, arXiv:1809.09600), released
> under CC BY-SA 4.0. Each sample is one retrieval result: a question, its ten passages, and the
> source id of each passage. The source attribution, the compromised sources and the injected
> claims are not part of HotpotQA. They were added offline for this challenge and exist nowhere
> else, so the labels cannot be recovered from the public release.
> Files available in public/:
> train.csv -- 12,000 labeled samples
> id (int): Row index, 0-based
> question (string): The natural language question
> passages (string): A JSON list of exactly 10 passage strings, indexed 0 to 9
> source_ids (string): A JSON list of 10 integers, the source id of each passage in order
> answer (string): The true answer, a short span
> quarantine_ids (string): Pipe-separated indices of the passages that come from a compromised source, for example 2|5|7. An empty string means none of the ten do.
> test.csv -- 4,000 unlabeled samples
> id (int): Row index, 0-based
> question (string): The natural language question
> passages (string): A JSON list of exactly 10 passage strings, indexed 0 to 9
> source_ids (string): A JSON list of 10 integers, the source id of each passage in order
> sample_submission.csv -- A correctly formatted placeholder submission
> id (int): Row index from test.csv
> answer (string): Placeholder answer
> quarantine_ids (string): Empty placeholder
> A source appears in only about 25 passages spread across the split, roughly a dozen of which
> carry a claim, so its reliability must be judged from a small and noisy sample by aggregating
> its behaviour over many rows. Load the passages and source ids with json.loads.
> Submission
> Submit a CSV with exactly three columns:
> id (int): Row index from test.csv, 0 to 3,999
> answer (string): Your predicted answer to the question
> quarantine_ids (string): Pipe-separated indices of the passages you believe come from a compromised source, or an empty string if you believe none do
> Example:
> id,answer,quarantine_ids 0,Batemans Bay,0|4 1,1948, 2,yes,3|7|9 3,Aldous Huxley,5
> Requirements:
> Exactly 4,000 rows, one per test sample
> A header row
> Column names exactly id, answer and quarantine_ids
> Every index in quarantine_ids must be an integer from 0 to 9, with no repeats
> An empty quarantine_ids cell is valid and means you believe no passage is from a compromised source
> What not to use
> Do not download HotpotQA, or any mirror or derivative of it, to look up gold answers. The
> answer must be recovered from the passages you are given. Note that this would gain you very
> little in any case: the answer is worth only 0.25 of the score, ordinary extractive question
> answering over the provided passages already recovers most of it, and it does nothing at all
> for the compromised-source detection that carries the remaining 0.75.
> The source attribution and the poisoning exist only in this challenge and appear in no public
> release, so the quarantine labels cannot be looked up anywhere.
> Do not use any external question answering API, search engine, or web lookup at inference
> time. Everything you need is inside the provided passages.
> Do not attempt to obtain or reconstruct the private answer key.
> Your solution must run on CPU alone, within the platform time limit.

Inspiration note: Useful because it makes RAG safety concrete at corpus scale: identify compromised sources rather than only answering queries, with an output shape aimed at retrieval forensics.

## Auditable Evidence Opening Under Paragraph Budgets

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx762bjavqmvy9rjmkbmcpggth89wtbx
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU-only
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Auditable Evidence Opening Under Paragraph Budgets
> In production evidence systems, access is observable and costly: every opened paragraph consumes latency, context budget, and money. This challenge asks you to solve masked multi-step questions from a candidate evidence pool and to submit the ordered evidence-opening trace your system claims to use, not just the final answer.
> For each test row you receive a question, a tight integer budget, and a corpus_json list of candidate paragraphs with opaque paragraph ids. Your submission must contain a short answer string, an ordered program_json list of paragraph ids opened in order, and a row-level confidence. The grader rewards answer correctness only when the submitted trace is valid, stays within budget, and covers enough hidden supporting evidence; bloated access traces are penalized heavily.
> The public text is entity-masked with row-local aliases such as ent_3fa91b02, and paragraph ids are salted opaque ids. This masking is part of the data contract: learn to retrieve and reason from the provided train split rather than searching for public benchmark rows.
> This is not an executable-code benchmark and not a context-packing diagnostic. The scored object is a self-reported, auditable evidence-opening trace over row-local opaque paragraph ids. The model must decide which paragraphs to claim as opened, in what order, and when the evidence is sufficient to answer under the visible budget.
> The intended solution is a trained or fine-tuned evidence planner: for example, a cross-encoder or dual-encoder reranker trained on public/train.csv, a small sequence-to-sequence model that emits paragraph ids, or an iterative policy that selects the next paragraph from the remaining pool after reading the question and already opened evidence. Zero-shot prompting or dumping a large top-k list is not the intended approach.
> What Not To Do, using any of the approaches below is grounds for solution rejection regardless of leaderboard score:
> Do not search external source-dataset mirrors, official raw files, web pages, public QA datasets, or paper examples to recover hidden answers or support ids.
> Do not submit broad top-k or open-all traces that ignore the row budget.
> Do not use hosted or closed-source APIs at training or inference time, including distillation from such systems.
> Do not exploit raw ids, row order, file metadata, source split names, hidden answer files, or grader behavior.
> Do not submit a hard-coded answer map, manual labels for test rows, or a solution that does not learn from public/train.csv.
> Enforcement on invalid approaches: submissions or writeups that rely on source lookup, external labeled versions of the hidden rows, broad budget-ignoring evidence dumps, private-file access, hosted APIs, or rule-only answer maps may be rejected before payout even if the CSV happens to score.
> Evaluation
> The grader validates the submission schema exactly, then scores each row.
> Structural submission failures are rejected with a generic invalid-submission error: missing, extra, or reordered columns; duplicate ids; or missing or extra ids.
> Row-local failures make only that row score 0.0: invalid JSON in program_json, a non-list JSON value, a non-string paragraph id, repeated paragraph ids, paragraph ids not present in that row's corpus, overlong JSON, overlong answer strings, a program longer than the row budget, or a missing, non-finite, non-numeric, or out-of-range confidence value.
> For answerable rows, A is the best normalized token F1 between the submitted answer and the hidden answer aliases. If A < 0.80, the row raw score is 0. C_set is the fraction of hidden support ids opened, C_order is the longest-common-subsequence coverage of opened support ids against the hidden ordered support program, and C = 0.55*C_set + 0.45*C_order. If C < 0.67, the row raw score is 0. Let E = min(1, min_support_count / max(program_length, 1)). The answerable raw row score is:
> Raw = A * C^2 * E^2
> For unanswerable rows, the hidden answer is INSUFFICIENT. The raw row score is 1 only when the submitted answer is INSUFFICIENT and the program is within budget; otherwise it is 0.
> Partial raw credit is deliberately compressed so a row needs nearly exact answer and support evidence to look strong:
> Task = Raw^1.60
> Calibration is multiplicative and cannot rescue a wrong row:
> Cal = 1 - abs(confidence - Task)
> Row = Task * (0.90 + 0.10 * Cal^2)
> The final score is:
> Final = 0.62 * mean(Row)
> + 0.28 * worst mean(Row) over support-depth/answerability groups
> + 0.10 * worst mean(Row) over answer-shape groups
> Higher is better. The theoretical minimum is 0.0; the theoretical maximum is 1.0. A perfect submission with exact answers, minimal support programs, and confidence 1.0 scores exactly 1.0. The shipped sample submission is a weak INSUFFICIENT baseline and scores about 0.124 on the prepared split.
> Dataset
> Files shipped to participants are listed below.
> The training file contains questions, candidate paragraph pools, budgets, answers, and train-only support programs. The test file contains only questions, candidate paragraph pools, and budgets. The sample submission contains the exact required submission columns.
> Training columns:
> corpus_json is a compact JSON list. Each item has pid, title, and text. The support_program_json column is present only in train and contains one valid ordered support program using the public paragraph ids for that row.
> In public/train.csv, id is the public row key, question is the masked multi-step question, budget is the maximum number of paragraph ids that may be opened, corpus_json is the candidate evidence pool, answer is the train answer string, support_program_json is a train-only ordered support program, min_support_count is the number of required support paragraphs, and answerable is the train-only answerability flag.
> Test columns:
> The test file has no answer, support id, answerability, support-depth, answer-shape, raw source id, source split, or composition metadata columns.
> In public/test.csv, id is the public row key, question is the masked multi-step question, budget is the maximum number of paragraph ids that may be opened, and corpus_json is the candidate evidence pool.
> Submission format:
> Submit exactly these four columns in this order. program_json must be a JSON list of unique paragraph ids from the row's own corpus_json. Repeated ids are not allowed.
> Example submission rows:
> id,answer,program_json,confidence
> q_000a2cd9821258,INSUFFICIENT,[],0.2
> q_000e2ba9825cee,INSUFFICIENT,[],0.2
> q_000e85b4baa30b,INSUFFICIENT,[],0.2

Inspiration note: Useful because it frames RAG as auditable evidence selection under paragraph budgets, emphasizing source-grounded retrieval and concise justification rather than free-form answering.

## Cross-Community Duplicate Question Retrieval

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c16xxg7bj7519949aa92phn8agd1h
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> Dataset source is visible after the challenge closes.
> Description
> Leaderboard
> (1)
> Your Submissions
> Cross-Community Duplicate Question Retrieval
> Overview
> Domain: NLP (semantic text retrieval under domain shift). When a Q&A community closes a question as a duplicate, moderators record exactly which earlier question it duplicates. Your task: given the title and body of a duplicate-closed question — exactly as its author first wrote it — rank the community's question pool and retrieve the original question(s) it duplicates.
> Duplicates are rarely copies. The same problem gets asked with different vocabulary, more or less detail, from a different angle, or with the key fact buried in a story. Matching them requires modeling what a question is about, not just which words it shares with another.
> The central difficulty is cross-community generalization: training queries come from 33 communities, but every test query comes from one of 8 communities that contribute zero training queries. Anything tuned to the topics of the training communities must transfer on the strength of its method, not its vocabulary. Validation should therefore be grouped by community_id (community-disjoint), mirroring the train/test relationship.
> All text is real (written by actual askers, 2009–2021, initial revisions only). All labels are real moderation outcomes: the recorded duplicate links of the respective communities.
> Dataset Info
> File structure:
> | File | Rows | Description |
> |------|------|-------------|
> | corpus.csv | 161,439 | Candidate question pools for all 41 communities (about 4,000 docs each) |
> | train_queries.csv | 27,109 | Duplicate-closed questions from 33 communities, with gold targets |
> | test_queries.csv | 5,883 | Duplicate-closed questions from the 8 held-out communities, no targets |
> | sample_submission.csv | 5,883 | Format example (5 arbitrary pool docs per query) |
> Columns:
> | Column | Type | Description |
> |--------|------|-------------|
> | doc_id | string | Unique pool-document identifier (salted hash), corpus.csv only |
> | query_id | string | Unique query identifier (salted hash), query files only |
> | community_id | string | Anonymized community identifier; present in every file. The 8 test community_id values have no rows in train_queries.csv |
> | title | string | Question title as first posted |
> | body | string | Question body as first posted, Markdown, truncated to 2,500 characters |
> | targets | string | Space-separated doc_id(s) of the gold duplicate target(s) (train_queries.csv only; usually one, sometimes several) |
> Data characteristics:
> Retrieval is within-community: a query's gold targets always belong to the same community's pool, and rankings of documents from other communities can never be correct.
> Pools contain the gold targets of that community's queries plus a random sample of the community's other questions.
> Queries never appear as pool documents, and no query's text is byte-identical to any document of its community's pool.
> About 94% of queries have exactly one gold target; the rest have two or more.
> Query counts per test community range from about 500 to 1,400.
> Evaluation
> Submissions are scored with Mean Average Precision at 5 (MAP@5). For each query, you submit 5 ranked candidate doc_ids (most likely duplicate target first). With G the query's set of gold target documents:
> AP@5  = (1 / min(|G|, 5)) * sum over ranks k = 1..5 of
> rel(k) * (number of gold docs among the top k) / k
> MAP@5 = mean of AP@5 over all 5,883 test queries
> where rel(k) = 1 if the k-th ranked doc_id is in G, else 0. Higher is better; the score ranges from 0 to 1. Placing a gold target at rank 1 scores 1.0 for that query; at rank 5, 0.2.
> Sample Submission
> Submit a CSV with exactly the two columns query_id and predictions, in that order, containing exactly 5,883 rows — each test query_id exactly once. predictions is a single string of exactly 5 space-separated, distinct doc_ids, ranked most-likely first.
> query_id,predictions
> q_0a1b2c3d4e5f,d_1a2b3c4d5e6f d_2b3c4d5e6f70 d_3c4d5e6f7081 d_4d5e6f708192 d_5e6f708192a3
> Submissions with missing or unknown query_id values, duplicate rows, extra columns, missing cells, malformed doc_ids, repeated doc_ids within a row, or a count other than 5 are rejected.
> What to Use
> Any retrieval or ranking approach built from the provided data with libraries pre-installed in the Kaggle Docker image (scikit-learn, scipy, PyTorch, LightGBM, etc.), running on CPU within the time limit.
> The training communities' gold links — for tuning retrieval parameters, training rerankers or representations, and for building community-disjoint validation splits that mirror the unseen-community test condition.
> Both fields of every question (titles and bodies carry complementary signal), and the structure of the candidate pools.
> What Not to Use
> No external data, no internet access, and no downloads of any kind at run time; no challenge-specific or private checkpoints. Only the provided files and whatever is already available offline in the grading environment may be used.
> Do not use community_id as a predictive feature value; test community values never occur in training queries. It identifies which pool to rank and enables grouped validation.
> Do not attempt to de-anonymize communities or match questions against public Q&A archives; identifiers are salted specifically to keep the task self-contained.

Inspiration note: Useful because it turns duplicate-question retrieval into a community-shifted RAG benchmark, with a clean top-k output shape and a strong emphasis on retrieval generalization rather than memorized vocabulary.

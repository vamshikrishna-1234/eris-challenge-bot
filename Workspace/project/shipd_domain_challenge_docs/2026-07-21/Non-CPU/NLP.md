# Non-CPU NLP Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed Non-CPU examples in this document: 27

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.

## Long Range Dependency Bridge Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73taenmmfrnfz47yzst86rbn8bj2hn
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat bunnys's score of 59.462!

Full challenge description from page:

> Long Range Dependency Bridge Recovery
> Overview
> Long public-sector reports are often processed in stages, leaving partial linguistic annotations that preserve local structure but lose the long-range arcs connecting subjects, clauses, modifiers, and complements. Each row in Arcweave contains one Swedish sentence represented through a lossy token view, a morphology view, a partial dependency graph, and weak same-section context. Four to eight scored long-range dependency bridges have been withheld. Additional non-query support arcs may also be absent from partial_arcs; only the tokens explicitly listed in query_tokens belong in the output.
> Predict the scored bridges as one variable-length, space-separated arc sequence. Every target is derived from the real dependency annotation: no label noise, random answer corruption, prompt-based judging, or artificial score cap is used. Train and test documents are disjoint. Rows are evenly divided between two observable input-fidelity profiles at every query length. Syntax-rich rows show base POS labels for query tokens and retain most support arcs. Lexical-sparse rows mark query morphology as QUERY|F#, expose lossy prefix/suffix-and-length signatures in token_view, and retain a smaller partial graph. The intended first-order approach is to detect the profile, combine its available lexical and morphological evidence with retained arcs, and decode all scored heads jointly.
> The 18 possible relation labels, in their published order, are SUBJECT, PASSIVE_SUBJECT, OBJECT, NOMINAL_MOD, POSSESSIVE, ADJECTIVAL, CLAUSAL_MOD, OBLIQUE, ADVERBIAL, DETERMINER, CASE_MARKER, CLAUSE_MARKER, AUXILIARY, COORDINATE, COORD_MARKER, COMPLEMENT, FIXED, and MISC.
> Evaluation Metric
> Let
> 𝑁
> =
> 1200
> N=1200 be the number of test rows and
> 𝑀
> =
> 7200
> M=7200 the total number of withheld arcs. Each true arc has a relation
> 𝑟
> 𝑘
> r
> k
> ​
> and zero-based head index
> ℎ
> 𝑘
> h
> k
> ​
> ; a prediction supplies
> 𝑟
> ^
> 𝑘
> r
> ^
> k
> ​
> and
> ℎ
> ^
> 𝑘
> h
> ^
> k
> ​
> . Both head indices are the integer suffixes of the right-hand T## labels and refer to positions in the full sentence shown by token_view and morph_view; they are never positions within the shorter query_tokens list. For example, true head T14 gives
> ℎ
> 𝑘
> =
> 14
> h
> k
> ​
> =14, predicted head T11 gives
> ℎ
> ^
> 𝑘
> =
> 11
> h
> ^
> k
> ​
> =11, and the absolute head distance is
> ∣
> 11
> −
> 14
> ∣
> =
> 3
> ∣11−14∣=3.
> Relation macro-F1 is computed over the 18 published labels. For relation
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
> ). A zero denominator contributes zero. The relation term is
> 𝑅
> =
> (
> 1
> /
> 18
> )
> ∑
> 𝑐
> 𝐹
> 1
> 𝑐
> R=(1/18)∑
> c
> ​
> F1
> c
> ​
> .
> Head proximity is
> 𝐻
> =
> (
> 1
> /
> 𝑀
> )
> ∑
> 𝑘
> =
> 1
> 𝑀
> exp
> ⁡
> (
> −
> ∣
> ℎ
> ^
> 𝑘
> −
> ℎ
> 𝑘
> ∣
> /
> 2
> )
> H=(1/M)∑
> k=1
> M
> ​
> exp(−∣
> h
> ^
> k
> ​
> −h
> k
> ​
> ∣/2). A malformed or invalid arc contributes zero to
> 𝐻
> H.
> Labeled-arc accuracy is
> 𝐴
> =
> (
> 1
> /
> 𝑀
> )
> ∑
> 𝑘
> =
> 1
> 𝑀
> 1
> [
> 𝑟
> ^
> 𝑘
> =
> 𝑟
> 𝑘
> ∧
> ℎ
> ^
> 𝑘
> =
> ℎ
> 𝑘
> ]
> A=(1/M)∑
> k=1
> M
> ​
> 1[
> r
> ^
> k
> ​
> =r
> k
> ​
> ∧
> h
> ^
> k
> ​
> =h
> k
> ​
> ].
> Whole-sequence exactness is
> 𝑄
> =
> (
> 1
> /
> 𝑁
> )
> ∑
> 𝑖
> =
> 1
> 𝑁
> 1
> [
> 𝑦
> ^
> 𝑖
> =
> 𝑦
> 𝑖
> ]
> Q=(1/N)∑
> i=1
> N
> ​
> 1[
> y
> ^
> ​
> i
> ​
> =y
> i
> ​
> ], where equality requires every query arc in row
> 𝑖
> i to have the correct relation and head in the required query-token order.
> A sequence is invalid if it is missing, malformed, uses an unknown relation, repeats or omits a query token, changes query-token order, or names a head outside that row's token range. For every arc in an invalid row, the grader substitutes the next relation in the published cyclic order relative to the true label. These substituted wrong relations are included in the global confusion counts used to compute relation macro-F1 (R), producing the same false-positive and false-negative effects as ordinary wrong relation predictions. Invalid rows contribute literal zero to head proximity (H), labeled-arc accuracy (A), and whole-sequence exactness (Q). Thus invalid output cannot be used as a cheaper abstention.
> The final score is
> 𝑆
> =
> 100
> ×
> clip
> ⁡
> (
> 0.25
> 𝑅
> +
> 0.20
> 𝐻
> +
> 0.20
> 𝐴
> +
> 0.35
> 𝑄
> 2
> ,
> 0
> ,
> 1
> )
> S=100×clip(0.25R+0.20H+0.20A+0.35Q
> 2
> ,0,1). Squaring (Q) makes complete multi-bridge recovery increasingly valuable without changing any target or imposing a score cap. Higher is better. The theoretical minimum is 0 and exact recovery of every sequence is 100.
> Measured references on the shipped public files are: malformed or invalid output 0.00, format-valid constant sample submission 3.11, POS-mode heuristic 14.25, trained sparse structural model 34.56, 12-epoch bidirectional GRU arc parser 52.20, 40-epoch version of the same parser 52.23, and perfect 100.00.
> Dataset
> The target length is genuinely variable. In train.csv, each query length from four through eight occurs in exactly 1,000 rows. In test.csv, each length occurs in exactly 240 rows. Consequently, the mean is exactly six bridges per row, which gives 30,000 training bridges and 7,200 test bridges; individual rows still contain four, five, six, seven, or eight query tokens.
> The public/ directory contains:
> train.csv — 5,000 labeled rows and 30,000 target bridges.
> sample_id — integer — consecutive identifier with no source or target information.
> context_view — string — two lossily lexicalized companion sentences from the same report section, separated by ||.
> token_view — string — ordered T##=value tokens; function words may remain, while content is represented by broad-family-and-length masks or lossy prefix/suffix-and-length signatures.
> morph_view — string — ordered morphology entries. Non-query tokens retain POS|FEATURES; query tokens show either a base POS or the profile marker QUERY|F#.
> partial_arcs — string — retained support arcs formatted as SOURCE:RELATION>HEAD; absence from this field does not make a token a scored query.
> query_tokens — string — four to eight T## tokens whose long-range arcs must be recovered, in required output order.
> target_arcs — string — training target sequence in the same order as query_tokens.
> test.csv — 1,200 query rows and exactly the six input columns sample_id, context_view, token_view, morph_view, partial_arcs, and query_tokens.
> sample_submission.csv — 1,200 rows illustrating the required submission columns.
> All token indices are zero-based within their sentence. A target token such as T07:SUBJECT>T14 means that token T07 bears relation SUBJECT to head token T14. Public identifiers, public row order, masking channel, and file layout do not encode the answers.
> Submission
> Submit a CSV with a header and exactly 1,200 data rows. It must contain these columns:
> sample_id — integer — every test identifier exactly once; row order may differ from test.csv.
> target_arcs — string — one arc for every row-specific query token, space-separated and in the exact order shown by query_tokens.
> Every arc must use T##:RELATION>T##. The left-hand token sequence must exactly equal the row's query_tokens, without omissions or duplicates. Relations must come from the published inventory. Missing required columns, duplicate column names, duplicate/missing/unknown identifiers, or a wrong row count raise a clear validation error. Extra columns are ignored, and required columns may appear in either order. Missing, non-string, malformed, unknown-relation, or structurally invalid predictions receive worst-case credit for the affected row and never crash the grader.
> Examples using real test identifiers and their actual query-token layouts:
> sample_id,target_arcs
> 0,T00:NOMINAL_MOD>T03 T04:NOMINAL_MOD>T03 T05:NOMINAL_MOD>T03 T07:NOMINAL_MOD>T03 T14:NOMINAL_MOD>T03
> 1,T14:OBLIQUE>T21 T17:NOMINAL_MOD>T21 T21:SUBJECT>T05 T24:NOMINAL_MOD>T21 T25:OBJECT>T21 T27:COORDINATE>T21 T36:COMPLEMENT>T21
> These rows demonstrate formatting only and are not disclosed answers.
> What Not to Use
> A constant relation and adjacent head ignore morphology and score only 3.11.
> POS lookup alone cannot distinguish attachment direction, passive structure, clause boundaries, competing long-distance heads, or QUERY|F# rows; it scores 14.25.
> Treating every source token absent from partial_arcs as a target fails because unscored support arcs are also removed; query_tokens is the only target list.
> Treating query arcs independently misses the 30% whole-sequence term and cannot enforce a coherent completed graph.
> Sorting token identifiers supplies no information because identifiers only represent sentence position.
> The context view alone cannot recover exact token-level heads.
> Prompt injection or instruction following is irrelevant: grading is deterministic numeric comparison, and report text is never executed.
> Exact-source lookup is not an intended approach; source identifiers and rare lexical keys are removed, and content masking makes direct alignment unreliable.
> Expected solutions combine profile-aware sequence encoding, lexical-signature and morphology modeling, partial-graph reasoning, candidate-head scoring, and joint decoding across all bridges in a row.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Ordering Workplace Tasks by Their Importance to the Job

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72w4x5bt3dtybe8ztz4n61h189tar8
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat supegirl's score of 0.560!

Full challenge description from page:

> Ordering Workplace Tasks by Their Importance to the Job
> Overview
> Every occupation is a bundle of concrete tasks, and some are far more central to
> the job than others — a nurse's "monitor patient vital signs" is core, while
> "order medical supplies" is peripheral. In a large occupational survey, job
> incumbents rated, on a 1–5 scale, how important each task is to their
> occupation. This challenge asks you to recover that importance ordering from
> the task wording alone, for tasks that have been deliberately matched so the easy
> explanations are held constant.
> Each item gives you K = 8 task statements, all drawn from the same broad
> occupational field and sitting in a narrow importance band. Your job is to
> order them from most to least important. Because the tasks are close in importance
> and share vocabulary, the only usable signal is a fine reading of how central
> each task sounds — not its length, not a single keyword.
> Task
> For every item in test.csv, output that item's candidate task-ids re-emitted
> in your predicted order — most important first.
> This is a ranking task: the output is a permutation of the given ids, not a
> number and not a class label. There is no importance rating and no occupation
> label in the inputs; you infer the order from the task text and the training
> examples.
> Why it is hard
> Importance is a noisy human consensus. Each task's rating is the mean of
> ~50–90 incumbents' 1–5 judgements, so it is only partially determined by the
> wording — even a perfect content model cannot reproduce the order exactly, and
> the achievable score is capped well below 1.0.
> The items are matched to remove the easy shortcuts. Within one item:
> all tasks come from the same broad occupational field, so field-level
> differences in what "important" means are held roughly constant;
> all tasks sit in a narrow importance band, so you cannot simply separate
> obviously-core from obviously-trivial duties — you must discriminate finely
> among tasks that were all rated comparably;
> because banded tasks in one field share vocabulary, ordering by task
> length or by a single "leadership"/"manage" verb is ≈ chance.
> What remains is genuine but limited signal: how essential vs. incidental a
> duty reads. A content model that captures this reaches item-level ordering
> only ≈ 0.54; trivial strategies (length, or sorting by the opaque id) are ≈
> 0.50. Perfect is 1.0, so there is real — but deliberately bounded — headroom,
> and stronger models score measurably above weaker ones.
> Data
> tasks.csv — the text for every task-id used anywhere:
> id (string): opaque task identifier (carries no ranking signal).
> text (string): the workplace task statement (e.g. "Analyze operations to
> evaluate performance of a company or its staff in meeting objectives.").
> train.csv — labelled items:
> id (string): unique item identifier.
> candidates (string): the K task-ids for this item, |-separated, in
> scrambled order.
> ranked (string): the same ids, |-separated, in the correct order
> (most-important first).
> test.csv — items to order: id, candidates (scrambled ids).
> sample_submission.csv — a valid submission in the required format (it echoes
> the presented order, which scores ≈ 0.50).
> Tasks are split so that training and test tasks never overlap — you must
> generalise to unseen tasks.
> Worked example
> An item might contain 8 tasks all from healthcare occupations, all rated around
> 4.0/5 in importance. Ordering them by length or by whether they contain "manage"
> tells you nothing (they match on field and importance level). The order comes down
> to which duties read as core practice versus administrative or occasional — a
> distinction you learn from the training orderings and apply to the test item.
> Submission Format
> A CSV with exactly two columns: id and ranked.
> Exactly one row per id in test.csv, no duplicates, and no extra rows — the
> full submission must have exactly as many rows as test.csv.
> ranked is the item's candidate task-ids, |-separated, in your predicted order
> (most-important first). Re-emit exactly the ids given for that item, each
> exactly once.
> The contract is enforced strictly — a malformed submission is rejected, not
> scored. The grader raises an error (rather than assigning a partial score) if the
> columns are wrong, an id is null / duplicated / missing / unknown, there are extra
> rows, or any ranked cell is not an exact permutation of that item's candidates
> (an empty cell, a repeated id, a dropped candidate, or an unknown token all fail).
> A valid ordering never triggers this — only genuinely malformed output does.
> Evaluation
> Metric — Salience Ordering Score (SOS). For each item we take the Spearman
> rank correlation between your order and the true importance order, rescale it to
> [0, 1] as (rho + 1) / 2, and average over all test items. Only the ORDER
> matters; you never output a numeric rating.
> An unchanged (scrambled) order scores ≈ 0.50; a perfect order scores 1.0; the
> exact reverse scores 0.0.
> Because each item's tasks share a field, an importance band, and vocabulary,
> ordering by length or by the opaque id is ≈ chance (0.50). A content model that
> reads task centrality reaches ≈ 0.54 — clear but tightly bounded headroom; the
> ceiling is well below 1.0 because importance is a noisy consensus only partly
> determined by the wording.
> Approaches
> Featurise the task text (TF-IDF / bag-of-phrases / a text embedding) and fit a
> learning-to-rank model (pairwise or listwise) or a regressor on the training
> orderings, then order each test item by the predicted salience.
> The signal is in what the task is about and how central it reads (verbs of
> core practice vs. support/administration), not surface length; a semantic text
> encoder should beat a bag-of-words model — which is exactly where the score
> spread between weaker and stronger solutions comes from.
> Validate locally by holding out a slice of training items and computing SOS
> before predicting the test set.
> What Not To Use
> Do not attempt to identify the underlying source database and look up the
> tasks or their importance ratings from any external collection, portal, or API.
> Do not hard-code answers. The intended solution is a content model that
> learns to order tasks from the provided training items and generalises to unseen
> tasks.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Forecasting Post-Approval Drug Safety Escalations

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75wwrh9p4ev4a460pejrmvqx89rjyp
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat mdluffy's score of 0.213!

Full challenge description from page:

> Overview
> When a prescription drug first reaches the market, its product labeling reflects only what was known at approval. Over the following years, serious risks are often discovered, and the label is escalated — a new Warning is added, a new Contraindication is introduced, or (most seriously) a Boxed Warning is issued.
> You are given the early label of each drug — the sections written around the time it first reached the market, with the product's identity removed. Your job is to forecast the safety escalation that the drug will later accrue: how severe it will be, which body systems it will concern, and how soon it will happen. You never see the drug's later labels; you must predict the future from the early text and the pharmacology it describes.
> This is a forecasting task, not a description task. The early adverse-reaction profile, the mechanism of action, and the pharmacologic class carry real but noisy signal about which organ systems are vulnerable. Most drugs never receive a major escalation, so a useful model must learn to tell the difference.
> Data files
> All text has been de-identified: brand names, generic/ingredient names, manufacturer names, and product codes have been replaced with placeholders such as [PRODUCT] or [ID], and the wording has been lightly normalized. Do not attempt to re-identify the underlying products; identity is not part of the task and re-identification is treated as a rule violation.
> train.csv
> One row per drug, with the early-label inputs and the gold targets. Columns:
> id — string. Opaque unique identifier for the drug item.
> indications_text — string. Early-label "Indications and Usage" section (masked).
> mechanism_text — string. Early-label mechanism of action / clinical pharmacology (masked).
> adverse_reactions_text — string. Early-label "Adverse Reactions" section (masked). Primary signal.
> warnings_text — string. Early-label warnings & precautions (masked). The baseline safety state.
> contraindications_text — string. Early-label contraindications (masked).
> boxed_warning_present_t0 — integer (0 or 1). Whether the early label already carried a boxed warning.
> route — string. Route of administration (e.g. oral, injection, topical, unknown).
> product_type — string. Product category (e.g. human prescription drug).
> sev — integer in {0,1,2,3}. TARGET. Severity of the future escalation (see below).
> organ_systems — string. TARGET. Pipe-joined set of body-system codes the escalation concerns; empty if sev = 0.
> horizon — string in {none,early,late}. TARGET. How soon the first escalation appears.
> test.csv
> Same input columns as train.csv (id, indications_text, mechanism_text, adverse_reactions_text, warnings_text, contraindications_text, boxed_warning_present_t0, route, product_type) but without the three target columns. Predict the targets for these rows.
> sample_submission.csv
> A valid submission with the required columns and default values. Columns: id, severity_pred, organ_systems_pred, horizon_pred.
> Target definitions
> sev — escalation severity (ordinal, 0–3). The most serious new safety element the drug acquires after the early label:
> 0 — no major safety escalation.
> 1 — a new Warning / Precaution about a serious risk.
> 2 — a new Contraindication.
> 3 — a new Boxed Warning.
> organ_systems — affected body systems (multi-label). The set of systems the escalation concerns, as a pipe-joined (|) subset of these 16 codes (empty string when sev = 0):
> hepatic, cardiovascular, thrombosis, infection, malignancy, hypersensitivity, hematologic, renal, neurologic, psychiatric, endocrine_metabolic, gastrointestinal, respiratory, reproductive, dermatologic, musculoskeletal.
> horizon — timing bucket. none if no escalation; early if the first escalation appears less than 2 years after the early label; late if 2 years or more.
> Submission format
> A CSV named submission.csv with these columns, one row per id in test.csv:
> id — string. Must cover the test id set exactly (one row per test id, no extras or duplicates).
> severity_pred — integer in {0,1,2,3}.
> organ_systems_pred — pipe-joined subset of the 16 codes above; empty string if you predict no escalation.
> horizon_pred — one of none, early, late.
> Note: the submission columns severity_pred, organ_systems_pred, and horizon_pred correspond to the training targets sev, organ_systems, and horizon respectively.
> The submission must cover the test id set exactly: any missing id, unknown/extra id, duplicate id, or a missing id column is rejected (the grader raises rather than scoring a malformed submission).
> Evaluation metric
> Each submission is scored by a composite in [0, 1] (higher is better):
> score = 0.20 * sev_term + 0.30 * organ_micro + 0.15 * organ_macro + 0.25 * severe_f1 + 0.10 * horizon_term
> sev_term = max(0, quadratic-weighted Cohen's kappa) between severity_pred and gold sev (rewards ordinal closeness; robust to the large sev = 0 majority).
> organ_micro = micro-averaged F1 between the predicted and gold body-system sets, pooled over all test rows — including no-escalation rows (sev = 0), where the gold set is empty and any body system you predict counts as a false positive. It is frequency-weighted (dominated by the common organ systems) and is the stable core of the score.
> organ_macro = macro-averaged F1 over the body-system codes, each code weighted equally regardless of how rare it is. This rewards forecasting the rarer organ systems, so handling class imbalance — not just predicting the common ones — pays off.
> severe_f1 = F1 of the binary call "will this drug receive a high-severity escalation" (sev >= 2, i.e. a new contraindication or boxed warning). This is the hardest and most valuable forecast; a solution that plays safe with low severity scores 0 here.
> horizon_term = balanced-accuracy skill of horizon_pred over the rows that truly escalate (sev > 0), normalized against chance; 0 if there are no escalating rows.
> An all-default submission (severity_pred=0, empty organs, horizon_pred=none) scores ~0. Every F1 term penalizes over-prediction, so spraying organ systems or over-calling severity is not rewarded — calibration matters. The organ_macro and severe_f1 terms deliberately widen the gap between naive and careful solutions.
> Notes and rules
> The test set holds out entire therapeutic classes not seen in training. Solutions that memorize class→outcome associations from training will generalize poorly; read the pharmacology.
> The decision for every submitted column must come from a trained model (an encoder or a fine-tuned/generative language model over the label text), not from hardcoded rules, keyword lexicons, or lookup tables. Curated keyword lists may be used only as auxiliary features, never as the detector for a graded column.
> Escalations are relatively rare and organ-system profiles are imbalanced. Handle the imbalance (class weighting, focal/oversampling, thresholds) rather than collapsing to the majority.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Descriptive Passage Item Grounding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76v853kenhx7n7pkhrx5egdh8bpfrf
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: text, Dataset source is visible after the challenge closes., Leaderboard, (0)
- Best/top context found: Beat cosmicescape's score of 0.201!

Full challenge description from page:

> Descriptive Passage Item Grounding
> Overview
> Each task presents one descriptive passage — a short piece of text written about a single real-world item — together with a fixed slate of 20 candidate items. Exactly one candidate is the item the passage was written about; the other 19 are decoys. A system must output a calibrated probability distribution over the slate: its belief that each candidate is the item the passage describes.
> The passage never names the item and never repeats its identifiers — it only describes the experience of the item in free text. Each candidate is represented solely by its content: a tag profile, a locale, and a short content summary distilled from independent text about it. The difficulty is that the 19 decoys are chosen to be the same-category candidates whose content summary is the closest surface-lexical match to the passage itself — the strongest word-overlap distractors — so that shallow term overlap between the passage and a candidate's summary points at the decoys as much as at the true item, and the surface tags and text length shared across the slate do not identify it.
> Tasks are stratified into five difficulty tiers by how tightly the decoys crowd the true item on this passage-to-content match — from tiers where the true item is the clear surface match, to tiers where the decoys match the passage as well as or better than the true item does — and the five tiers are weighted equally, so a system must ground passages against easy and adversarial slates alike. Because the required output is a full belief distribution rather than a single pick, scoring rewards calibrated confidence: mass on the true item earns credit, an even spread earns the chance baseline, and confident mass on a wrong item is penalized.
> Dataset
> Public files
> items.csv — one row per candidate item. Columns: item_id, tags, locale, region, tier, traits, content_summary.
> train.csv — labeled tasks. Columns: task_id, passage, difficulty, slate, chosen_item_id.
> test.csv — unlabeled tasks. Columns: task_id, passage, difficulty, slate.
> sample_submission.csv — a valid submission in the required format (uniform distributions).
> Private file (organizer only)
> answers.csv — columns: task_id, difficulty, target_position (1-based index of the described item in the slate). Used only for scoring; never distributed.
> Column descriptions
> Every column in the public files is described below.
> item_id (string) — unique item identifier (e.g. item_3a9f1c…).
> tags (string) — comma-separated content tags for the item (e.g. Coffee, Breakfast, Cafe).
> locale (string) — the locale the item belongs to.
> region (string) — coarse region code.
> tier (integer) — item price/level tier 1–4, or -1 if unknown.
> traits (string) — semicolon-separated key=value item traits (e.g. OutdoorSeating=True;GoodForKids=False).
> content_summary (string) — a short concatenation of snippets of independent text about the item (|-separated), describing what the item is like. This is the sole content signal for grounding.
> task_id (string) — unique task identifier; one row per task and one submission row per task_id.
> passage (string) — the descriptive text to ground; written about the true item, with its name and identifiers removed.
> difficulty (string) — the difficulty tier of the task, one of t1, t2, t3, t4, t5 (increasing crowding of the decoys around the true item in passage-to-content surface match; t5 is hardest).
> slate (string) — the candidate slate: exactly 20 item_ids separated by ;, in a fixed order. Your probabilities are aligned to this order.
> chosen_item_id (string, train only) — the item_id in the slate the passage describes. Present in train.csv only.
> Each item_id in a task's slate has its content row in items.csv. The difficulty field indicates how strongly the decoys compete with the true item on passage-to-content surface match.
> Data example
> A truncated train.csv row:
> task_id,passage,difficulty,slate,chosen_item_id
> task_tr000001,"cozy spot for a quick espresso before work, friendly staff …",t3,item_a;item_b;item_c;…;item_t,item_c
> Submission format
> Submit a CSV named submission.csv with exactly one row per test task_id and exactly these 21 columns:
> task_id,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20
> pk is the probability that the k-th item in that task's slate (fixed order) is the item the passage describes. Values are non-negative floats.
> The 20 probabilities in each row must sum to 1.0 (tolerance ±0.02; values are renormalized before scoring).
> Every test task_id must appear exactly once. Submissions with missing ids, unknown ids, duplicate ids, extra columns, missing columns, negative values, or non-finite values are rejected.
> Sample submission (uniform belief on every row):
> task_id,p1,p2,…,p20
> task_te000000,0.05,0.05,…,0.05
> Evaluation
> Metric: Tier-Balanced Calibrated Grounding Score (higher is better).
> Each task's predicted distribution is scored by a blend of a ranking term (does the true item rank near the top of the slate?) and a calibration term (a strictly-proper log score on the probability mass placed on the true item). Per-task scores are averaged within each of the five difficulty tiers, and the metric is the mean of the five tier averages, so every tier — including the hardest — contributes one fifth regardless of how many tasks it has.
> For a task with predicted distribution p over the 20 slate positions and true position t:
> p = renormalize(p)                                  # sum to 1
> g = (# of positions with p > p[t])                  # strictly greater
> k = (# of positions with p == p[t])                 # size of the tied block (includes t)
> # expected reciprocal rank over the tied ranks g+1 .. g+k (what a random
> # tie-break scores in expectation), so information-free jitter buys nothing:
> rr   = mean(1.0 / r for r in range(g + 1, g + k + 1))          # in [1/20, 1]
> cal  = 1.0 + math.log(max(p[t], 1e-9)) / math.log(20.0)        # normalized log score
> cal  = min(1.0, cal)                                # uniform -> 0, certain-correct -> 1, confident-wrong -> negative
> base = 0.5 * rr + 0.5 * cal                          # per-task score (can be negative)
> Aggregate:
> TIERS = ["t1", "t2", "t3", "t4", "t5"]
> tier_mean_r = mean(base_i for tasks i in tier r)     # for each tier r
> score = mean(tier_mean_r for r in TIERS)             # equal-weight macro-average
> score = max(0.02, min(1.0, score))                   # floor 0.02, ceiling 1.0
> Component summary:
> rr — reciprocal rank of the true item in the predicted ordering; ties are credited at the expected reciprocal rank over the tied positions (the mean of 1/r across the ranks the tied block occupies), so an even spread scores the chance rank and adding information-free noise to break ties gives no advantage. Rewards ranking the true item near the top of the slate.
> cal — a strictly-proper normalized log score on the probability assigned to the true item; 1/20 (uniform) maps to 0, certainty on the truth maps to 1, and placing little mass on the true item while being confident elsewhere drives it negative. Capped above at 1 (no lower cap), so overconfident-wrong predictions are penalized; the final macro-averaged score is floored at 0.02.
> base — the equal blend 0.5·rr + 0.5·cal per task.
> score — the equal-weight mean of the five per-tier averages, clamped to a floor of 0.02 and ceiling 1.0.
> Baseline (uniform / random) expected score: ≈ 0.09. A constant-uniform submission and a random-noise ranking both score the chance baseline of ≈ 0.09 (the calibration term is 0 for a uniform belief, and the expected reciprocal rank of the true item over a 20-item slate is (1/20)·Σ_{r=1..20} 1/r ≈ 0.18, so base ≈ 0.5·0.18 ≈ 0.09). Higher is better.
> What Not To Use (Prohibited Methods)
> This challenge measures semantic grounding of a descriptive passage to the item it describes. The following are prohibited:
> No external text-to-item lookup. Do not retrieve, scrape, or reconstruct the original source of any passage, and do not match a passage, item_id, item text, or locale back to an external corpus to recover which item a passage describes.
> No id-based hardcoding. Do not build any mapping from task_id or item_id directly to a target position or probability. Predictions must come from the provided passage and item content only.
> No train/test leakage. Do not use any test-set target signal, and do not tune on the private target distribution.
> No manual labeling of the test set. The submission must be model-generated; do not hand-assign probabilities by inspecting individual test tasks.
> No name/identifier recovery. Passages have their item name and identifiers stripped; do not attempt to re-derive them from external sources to shortcut the grounding.
> Generic prohibitions also apply: no external answer keys, no id-to-target lookups, no memorized external mappings.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Precedence Transfer: Does the Governing Concern Survive a Change of Readership

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71kne5rqd2x4fm9vm7ban5h18bjxbb
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat aegistran's score of 0.587!

Full challenge description from page:

> Overview
> Predict how two reviewers' rulings on the same draft relate to each other.
> Each row gives you a commissioning brief, the piece drafted against it, and the name of a second readership the item is being re-issued to. Two reviewers read that draft: one for the readership it was commissioned for, one for the readership it is being re-issued to. Each picks the single condition of the brief that governs the piece for their constituency, or rules that none does.
> You do not predict either ruling. You predict the relation between them - whether they landed on the same condition, on different ones, or whether one of them found nothing to act on. There are five possible relations, listed under "The five values of transfer_outcome" below. The metric is macro-averaged F1 over those five.
> The data is entirely simulated. A generator fixes each job's readership, facts and defects, and a language model writes the brief and draft prose from that specification at build time; both reviewers' decisions come from the generator, not from any real organisation's files. The generator scripts ship with the dataset. Nothing here is a real desk, person, document or figure.
> Why this is hard
> When a piece has to satisfy more than one constituency, the requirement that governs it is not fixed. A ward bulletin and a regulator's submission can carry identical defects and still be governed by different concerns. Teams that syndicate one item to several readerships live with this constantly, and they mostly discover it by re-running the review.
> The target is second-order and identity-invariant. You can name both governing conditions correctly and still get it wrong, because what is being asked is whether they coincide. You can get it right knowing neither identity, because "both cleared" and "the concern changed" are answerable without naming anything. No defect, no edit, no version pair and no measure of effort appears anywhere in the label.
> Each reviewer's decision is a draw, not a formula. Two conditions can be close enough in weight that which one governs is genuinely unsettled, and a condition can be live without being binding - real but tolerated on the day. Because the label compares two decisions, it inherits that unsettledness twice over. A sizeable share of these relations cannot be recovered from the text by any model, and the ceiling is far from perfect by construction.
> What is recoverable is the structure underneath: how a constituency's priorities re-order the same set of conditions. That ordering is stated nowhere. It exists only as a regularity across the training outcomes, and learning it is the whole of the available headroom.
> Data
> Each row is one draft, the brief it was written from, and the readership it is being re-issued to.
> id - string. Opaque row key. Carries no signal.
> reissued_to - string, one of four constituencies. The second readership.
> brief - long text, about 126 words, given as labelled lines. It states the desk and the readership it was commissioned for; the item to lead with; a secondary item to also cover; one fact explicitly not yet confirmed; one topic explicitly out of scope; and two named sources with the statement each of them made.
> draft - long text, 85 to 115 words. The piece as drafted: fluent, confident, usually mostly right.
> transfer_outcome - the target. One of five string values, listed below. Present in train.csv only.
> train.csv has 4,464 rows and all five columns. test.csv has 1,024 rows and carries id, reissued_to, brief and draft.
> The five values of transfer_outcome
> Predict exactly one of these for every test row, spelled exactly as shown:
> both_clear - neither reviewer found a governing condition; the piece stands for both constituencies.
> same_concern - both reviewers were governed by the same condition of the brief.
> different_concern - both were governed, but by different conditions; the concern changed with the readership.
> released - a condition governed for the original readership but none governs for the new one; the piece travels more freely than it did.
> newly_binding - nothing governed originally, but a condition binds for the new readership.
> Submission format
> A CSV with exactly two columns, id and transfer_outcome, one row for every id in test.csv, in any order.
> id,transfer_outcome row_00003,different_concern row_00017,both_clear row_00042,released
> A submission with missing ids, extra ids, duplicate ids, or any value outside the five is rejected rather than scored. A sample_submission.csv is provided; it is a degenerate placeholder and scores 0.
> Evaluation
> Macro-averaged F1 over the five values: the unweighted mean of the five per-class F1 scores, so the rare relations count exactly as much as the common ones. Range 0 to 1, higher is better. A submission that leans on only one or two values is scored down accordingly.
> Notes
> The test set is drawn entirely from desks that do not appear in the training data: different industries, different subject matter, different people, different house vocabulary. None of the specific topics transfer. What transfers is how constituencies re-order the same conditions, which is the same everywhere.
> The text is short and the corpus is a few thousand rows. This is a comprehension problem rather than a scale problem, and a well-chosen compact encoder, fine-tuned on the pairing of brief and draft, is enough to do well inside a modest compute and latency budget.
> What not to use
> No external APIs, hosted models or network calls at inference time.
> No external data sources beyond what is provided.
> No training on the test split, and no pseudo-labelling of test rows.
> No hardcoded lookup tables, and no fingerprinting of row identifiers - the ids carry no signal.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Cross-Solvent Dissolution Behavior from Molecular Structure

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74feetxw7vmsr0hch291n60d8bkswg
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: text, chemistry, molecular, Dataset source is visible after the challenge closes.
- Best/top context found: Beat mailliwa's score of 0.527!

Full challenge description from page:

> Overview
> This is a reading-and-reasoning audit, not a lookup. A process-chemistry notebook is full of quick solubility notes: a technician drops a compound into a solvent at some temperature and jots down how well it seemed to dissolve. Before those notes are trusted downstream, someone has to read each one on its own and reason about a single question: given only the two molecular structures and the temperature, does the claimed outcome hold up as chemically sensible, or has the note over-sold or under-sold how well the compound really dissolves?
> You are given, in each account, the compound (as a SMILES structure), the solvent it was placed in (also as a SMILES structure), the temperature, and the technician's claimed outcome. The account never tells you whether the claim is right. You judge that by reasoning about how the compound's structure and the solvent's structure act on each other -- which is hard precisely where it matters, because the naive "like dissolves like" rule of thumb quietly fails when a specific functional-group interaction, ring system, or hydrogen-bonding pattern takes over. Read each account and return one verdict:
> consistent - the claimed outcome matches how the compound actually behaves overstated - the note claims it dissolves better than it really does understated - the note claims it dissolves worse than it really does
> What makes this more than a rule check is that the truth is not written down anywhere in the account. The same solvent that barely wets one compound freely dissolves another, and a small change to a compound can move it across the scale, so there is no shortcut that reads the verdict straight off the text -- and the claimed outcome on its own tells you nothing about whether it is right. You have to learn, from many worked examples, how structure and solvent combine to set the real behaviour, and then apply that understanding to solvents whose chemistry the worked examples never showed you.
> Dataset
> The real behaviour decides the truth, and the claimed outcome in each note is a controlled restatement of it that is sometimes faithful and sometimes shifted. (Provenance and licence for the underlying measurements are given on the dataset card.) There are three files: train.csv (supervised), test.csv (no label), and sample_submission.csv (a format example). Every file is a UTF-8 CSV with a header row and one account per data row.
> train.csv -- columns, in order:
> id -- data type: string. A unique, opaque record identifier such as train_00042. It carries no signal (do not key predictions off it).
> record -- data type: string (a single free-text sentence pair; its internal structure is detailed below).
> verdict -- data type: string, categorical, taking exactly one of three values: consistent, overstated, understated. This is the target column you are learning to reproduce. The three values are approximately balanced across the training rows.
> test.csv -- columns, in order:
> id -- data type: string (same opaque form as in train.csv).
> record -- data type: string (identical format to the train.csv record column).
> test.csv has NO verdict column; you predict it for every test id.
> sample_submission.csv -- columns, in order:
> id -- data type: string. Exactly the set of ids in test.csv, one row each.
> verdict -- data type: string, categorical, one of consistent / overstated / understated.
> This file is a correctly formatted example: it assigns the single constant value "consistent" to every row. It exists only to show the exact expected header and format; it deliberately scores near zero and is not a useful prediction.
> The record field. Every record is a single sentence pair that always follows the same fixed template and packs four pieces of information, each of which you can parse out directly with a simple pattern:
> solute structure -- data type: string, a SMILES notation of the compound.
> solvent structure -- data type: string, a SMILES notation of the solvent.
> temperature -- data type: numeric (float), in kelvin, roughly in the 240-430 K range.
> claimed level -- data type: string, categorical, taking one of two values, "moderately" or "well": the amount of dissolving the lab note asserts (the CLAIM being audited, not the answer). Your verdict judges that claim against how the compound truly behaves: consistent if the truth matches the claim, overstated if the compound truly dissolves LESS than the note claims, understated if it truly dissolves MORE.
> For example, a record reads:
> A compound with molecular structure CC(=O)Nc1ccc(O)cc1 is stirred into a solvent with molecular structure CCO and held at 298 K. A preliminary lab note claims the compound dissolves well.
> Here the solute SMILES is CC(=O)Nc1ccc(O)cc1, the solvent SMILES is CCO, the temperature is 298 (K), and the claimed level is "well". No solvent name, class, polarity value, or measured solubility number is ever given -- only the two structures, the temperature, and the claim you must judge.
> The generalisation you are being tested on
> The evaluation accounts are doubly unfamiliar. Every one involves BOTH a solvent from a chemical family and a compound that never appear in training -- train and test share zero solvents and zero compounds. You therefore cannot recognise a test solvent or recall a test compound from memory; in particular, copying the verdict the same compound received in training under other solvents does not work, because that compound is absent from training. You have to read each unfamiliar account and reason out its verdict from the two structures and the temperature alone. The three verdicts are shared between training and evaluation; only the specific solvents and compounds differ.
> How submissions are judged
> Submissions are scored by the macro-averaged F1 across the three verdicts -- the unweighted mean of the three per-verdict F1 scores -- so every verdict counts equally regardless of how common it is. An audit that names a single verdict for every row, or uses only two of the three, is explicitly down-weighted to discourage degenerate guessing. Because real dissolution behaviour near a boundary is genuinely borderline, some claims are intrinsically impossible to adjudicate with certainty, so a perfect score is not attainable; strong audits settle the clear cases and lose only the ambiguous ones.
> Submission format
> A CSV with a header and exactly two columns:
> id,verdict test_00000,consistent test_00001,overstated test_00002,understated
> Every test id must appear exactly once, and every value must be one of consistent, overstated, understated.
> What not to use
> No external data. Do not use any outside solubility dataset, table, API, or internet lookup to recover or match the underlying measurements; the provided training file is the only permitted supervision. Building an audit around an external solubility database is out of scope and against the rules.
> No training on the evaluation set. Do not self-train, pseudo-label, or fit thresholds on the evaluation accounts, and do not use their structures to reverse-engineer the outcome behind the claim.
> No hardcoded lookups or id fingerprinting. The ids are opaque and carry no signal; do not key verdicts off them. The claimed outcome alone does not determine the verdict.
> A well-chosen, compact molecular structure model is entirely sufficient here; the task rewards understanding the structure-behaviour relationship, not raw model scale, and the compute and time budget are modest.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## BenchLink: Cross-Document Hearing Grounding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71mazbqmvwqat2dx2gjtprsh8b33b9
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: A10G
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: text, small-data, Dataset source is visible after the challenge closes., Leaderboard
- Best/top context found: Beat hitlocation's score of 40.349!

Full challenge description from page:

> BenchLink: Cross-Document Hearing Grounding
> Overview
> Public court archives can lose the relationship between an oral-hearing fragment and the written case record to which it belongs. Each row in this challenge contains a bench_packet built around one real judicial question and six anonymized candidate dossiers. Every dossier combines real advocate passages with material from a linked case record. Select the dossier that comes from the same hearing as the bench packet by assigning a relevance score to every candidate.
> Names, dates, application numbers, source identifiers, and a deterministic portion of the visible words have been removed. The five distractors come from different hearings chosen to resemble the true case, and all six dossiers receive the same query-conditioned passage-selection process. Solving the task therefore requires multilingual semantic grounding across the question, surrounding judicial context, advocacy, legal issues, and disposition language. This is a fixed-slate information-retrieval problem; no text generation or sequence reconstruction is required.
> The intended first-order approach is to encode the bench packet and the labeled sections of each dossier with a multilingual long-context model, learn a pairwise relevance function from train.csv, and normalize the six scores within each row. A second-stage reranker can compare the precise legal issue raised by the judge with the advocate and case-record evidence.
> Evaluation Metric
> There are N = 642 test rows and K = 6 candidates per row. For row i, let sᵢⱼ be the submitted score for candidate j and let yᵢ be the true candidate slot.
> A row is valid only when all six scores are finite real numbers in [0, 1] and their sum is positive. For a valid row, define pᵢⱼ = sᵢⱼ / Σₗ sᵢₗ. An invalid row contributes zero to every component below.
> Let ẑᵢ = argmaxⱼ pᵢⱼ, with the lowest-index slot selected on an exact tie. Define a = (1/N) Σᵢ 𝟙[ẑᵢ = yᵢ], where the indicator is zero for an invalid row. Chance-adjusted selection accuracy is A = clip((a − 1/K) / (1 − 1/K), 0, 1).
> For a valid row, define its pairwise win rate as wᵢ = (1/(K − 1)) Σⱼ≠yᵢ (𝟙[pᵢyᵢ > pᵢⱼ] + 0.5 × 𝟙[pᵢyᵢ = pᵢⱼ]). Set wᵢ = 0 for an invalid row. Chance-adjusted pairwise discrimination is P = clip(2 × ((1/N) Σᵢ wᵢ) − 1, 0, 1).
> For a valid row, calibrated gold mass is cᵢ = clip(1 + ln(max(pᵢyᵢ, 10⁻¹⁵)) / ln(K), 0, 1). Set cᵢ = 0 for an invalid row and define C = (1/N) Σᵢ cᵢ.
> The final score is S = 100 × clip(0.30A + 0.50P + 0.20C, 0, 1).
> Higher is better. Uniform confidence across all six candidates scores exactly 0.00; a perfect one-hot ranking scores exactly 100.00. On the shipped files, a permitted raw token-count overlap control scores 28.80, while a public-only pretrained multilingual semantic encoder with train-selected score calibration reaches 41.60. The overlap control uses only unweighted token counts: it does not compute document frequencies, inverse-document-frequency weights, or TF–IDF vectors. Neither baseline uses private labels, source identifiers, or external source lookup.
> Dataset
> The public/ directory contains:
> train.csv — 1,101 labeled queries from 97 hearings.
> sample_id — integer — Fresh public identifier.
> language_code — string — Language of the focal judicial utterance; en or fr.
> render_code — string — Balanced presentation style, either r00 or r01; it is not predictive of the correct slot.
> bench_packet — string — The focal judicial question with optional neighboring context.
> candidate_c0 through candidate_c5 — string — Six anonymized candidate dossiers.
> relevance_c0 through relevance_c5 — integer — One-hot relevance labels; exactly one value is 1 in each row.
> test.csv — 642 unlabeled queries from 52 hearings, containing only sample_id, language_code, render_code, bench_packet, and candidate_c0 through candidate_c5.
> sample_submission.csv — 642 rows with the required submission columns and uniform example scores.
> The train and test hearings are disjoint. Candidate dossiers never cross that split. Correct slots are exactly balanced in the test set with 107 rows in each of c0 through c5. <mask> represents deterministic lexical removal, <name> replaces a likely proper name, and <num> replaces a number. Candidate order, row order, text length, and the two rendering styles do not encode the answer.
> Submission
> Submit a CSV with a header and exactly 642 data rows. Columns must appear in this exact order:
> sample_id — integer or equivalent string — Every test identifier exactly once.
> score_c0 — float — Relevance score for candidate_c0.
> score_c1 — float — Relevance score for candidate_c1.
> score_c2 — float — Relevance score for candidate_c2.
> score_c3 — float — Relevance score for candidate_c3.
> score_c4 — float — Relevance score for candidate_c4.
> score_c5 — float — Relevance score for candidate_c5.
> Scores must be finite and in [0, 1]. They do not have to sum to one because the grader normalizes each valid row. A missing, duplicated, or unknown identifier, the wrong row count, or missing, extra, duplicated, or reordered columns raises a validation error. Malformed score rows receive no credit and cannot be used as abstentions.
> Example using real test identifiers:
> sample_id,score_c0,score_c1,score_c2,score_c3,score_c4,score_c5
> 0,0.10,0.15,0.20,0.35,0.12,0.08
> 1,0.28,0.08,0.17,0.11,0.21,0.15
> The numbers demonstrate syntax only. Infer the scores from the corresponding rows in test.csv.
> What Not to Use
> Simple unweighted lexical overlap, such as raw token-count, set-overlap, or Jaccard features, is permitted for diagnostics, baselines, and submissions.
> TF–IDF is prohibited in every role, including feature construction, candidate scoring, model input, ensembles, and final submissions. More generally, do not use corpus-level inverse-document-frequency weights or TF–IDF sparse vectors. The permitted token-overlap baseline above is not TF–IDF because every token retains equal weight.
> Source-site lookup or reconstruction from external hearing identifiers is prohibited; public rows intentionally exclude those identifiers.
> Candidate position and render_code are balanced and cannot provide a ranking shortcut.
> Dossier length varies as a nuisance property, while correct slots are balanced; length is not reliable evidence of provenance.
> A majority-slot or uniform-confidence submission scores at the metric floor.
> Comparing only the focal sentence misses supporting material in the neighboring context, advocacy sections, and linked case record.
> Expected solutions use multilingual contextual encoders, section-aware long-context representations, pairwise relevance learning, and calibrated within-slate reranking.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Cross-Dataset Zero-Shot Topic Inference

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78pxfmv0fw0ckmz1d9drwsa18bsxhw
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> The objective of this challenge is to perform Zero-Shot Compositional Topic Demixing.
> In a traditional topic classification benchmark, models are fed a single, cohesive text and asked to categorize it. This benchmark introduces a radical structural twist: Semantic Chimeras.
> We have framed classification as a Natural Language Inference (NLI) task, but heavily adversarial. You will be provided with a text and a candidate_topic string.
> Crucially, 50% of the text inputs are Chimeras—concatenations of two text snippets drawn from completely unrelated distributions (e.g., merging a World News article with a tweet about Sadness). Your task is to predict whether the candidate_topic matches any part of the provided text 1) or does not match at all 0).
> The Difficulty: The training dataset is built from specific domains and classes (e.g., world news and emotion states). However, the hidden test set is built from completely different source datasets with entirely unseen target topics (e.g., regional news and movie sentiment).
> Because the test set uses entirely unseen datasets, the chimeras encountered during evaluation (e.g., Politics + Negative Sentiment) are cross-domain compositions that have never been observed during training. To succeed, your model must softly segment the text, ignore adversarial distractors, and demonstrate true zero-shot semantic generalization.
> Dataset Sizes & Split
> Training Set: ~20,000 text-topic pairs.
> Test Set: ~10,000 text-topic pairs.
> Important Data Split Note: The Train and Test sets are strictly source-dataset disjoint. You will be tested on text domains and candidate topics that do not exist in the training data.
> File Schemas
> public/train.csv*
> id (string): The one-way hashed identifier of the text-topic pair.
> text (string): The raw source text.
> candidate_topic (string): A proposed label or category for the text.
> label (integer): The ground truth label. 1 if the text matches the candidate topic, 0 if it does not.
> public/test.csv*
> id (string): The one-way hashed identifier of the text-topic pair.
> text (string): The raw source text.
> candidate_topic (string): A proposed label or category for the text.
> Evaluation
> Submissions are evaluated on Area Under the ROC Curve (ROC-AUC) between the predicted probability of a match 1) and the observed target.
> Submission Format
> Your submission must be a CSV file with exactly two columns: id and label.
> The label can be a binary class 0 or 1) or a continuous probability predicting the likelihood of a match.
> Example
> id,label
> id_a1b2c3d4e5f6,0.1
> id_c3d4e5f6g7h8,0.9
> Prohibited Shortcuts
> Competitors are strictly prohibited from utilizing the following bypasses:
> Public Lookup: Attempting to search the internet or HuggingFace to reverse-engineer the original source dataset of the test set and look up the true classes. Although the test source names are fully hidden, zero-shot scraping of public datasets to cheat is prohibited.
> Hash Reversal: Attempting to crack or reverse the one-way hashes used for id.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Climate Evidence Calibration Ledger

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx763se1x2yps7nzdayjy3874n8bsxdx
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Accepted
- Difficulty: Hard
- Compute: Not shown/captured
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Scientific assessments communicate not only a claim but also how strongly the available evidence supports it. Your objective is to recover the four missing ordinal calibration entries for a climate-assessment claim: the lower and upper likelihood levels and the lower and upper confidence levels.
> Each row contains one masked claim together with selected passages from its traceable evidence base and its discussion of limitations. The formal calibration phrase has been removed from the claim. The source's later explanation that explicitly repeats the answer is not present. A useful model must connect the claim to the strength, consistency, scope, and uncertainty of its supporting evidence.
> The rows come from a recent public-domain national climate assessment. Public text is privacy-transformed by masking numbers, report references, explicit calibration words, and regularly spaced content tokens. Entire source chapters are assigned to only one split, so test chapters and their source passages never appear in training.
> This is an NLP structured-reconstruction task. It is not forecasting and it is not ordinary topic classification.
> Dataset
> All public files are under ./dataset/public/.
> train.csv: 294 labeled calibration instances.
> test.csv: 142 held-out instances from source chapters absent from training.
> sample_submission.csv: a valid target-independent sample that cycles evenly through the allowed single-level cards and does not encode training-label frequencies.
> Columns
> id string): opaque row identifier with no source or label meaning.
> prompt string): task instruction for the row.
> claim_packet string): a structured text packet with CLAIM, EVIDENCE_1, EVIDENCE_2, and LIMITATIONS_1 sections. The claim contains exactly one [MISSING_CALIBRATION] marker. Other masked calibration locations can appear as [OTHER_CALIBRATION].
> answer_format_json JSON string): required keys and allowed ordinal values.
> answer_json JSON string, train only): the four target ledger entries.
> Target Ledger
> answer_json contains exactly these keys:
> likelihood_floor: one of NONE, LIKELY, VERY_LIKELY, VIRTUALLY_CERTAIN.
> likelihood_ceiling: one of NONE, LIKELY, VERY_LIKELY, VIRTUALLY_CERTAIN.
> confidence_floor: one of NONE, LOW, MEDIUM, HIGH, VERY_HIGH.
> confidence_ceiling: one of NONE, LOW, MEDIUM, HIGH, VERY_HIGH.
> floor cannot exceed ceiling. NONE means that the published calibration phrase did not contain that axis, so both endpoints for that axis must be NONE together. For a single-level phrase, floor and ceiling are equal. A phrase spanning levels, such as a medium-to-high confidence statement, uses different endpoints.
> Evaluation
> Higher is better. Scores range from 0 to 1.
> For each likelihood or confidence endpoint:
> exact token: 1.00
> one ordinal step away, with neither token equal to NONE: 0.55
> two ordinal steps away, with neither token equal to NONE: 0.20
> farther away or a NONE mismatch: 0.00
> The two likelihood endpoint credits are averaged into likelihood_score. The two confidence endpoint credits are averaged into confidence_score.
> exact_tuple is 1 only when all four entries are exact, otherwise 0.
> presence_score is the mean of two binary checks: whether likelihood is present or absent correctly, and whether confidence is present or absent correctly.
> row_score = 0.50 * exact_tuple
> + 0.20 * confidence_score
> + 0.20 * likelihood_score
> + 0.10 * presence_score
> The final score rewards both overall accuracy and robustness. For each robustness axis, rows are grouped using hidden source-derived metadata and the mean row score is calculated for every group represented in the scored partition. The weakest mean is the minimum of those group means.
> Topic family groups: physical system, natural system, sector, response system, regional system, and synthesis.
> Calibration groups: confidence-only and likelihood-bearing.
> Intensity groups: lower confidence, high or likelihood, and very-high or certain.
> score = 0.60 * mean_row_score
> + 0.15 * weakest_topic_family_mean
> + 0.15 * weakest_calibration_group_mean
> + 0.10 * weakest_intensity_group_mean
> Submission Format
> Submit a CSV with exactly two columns in this order:
> id,answer_json
> clu_0123456789abcdef,"{""confidence_ceiling"":""HIGH"",""confidence_floor"":""HIGH"",""likelihood_ceiling"":""VERY_LIKELY"",""likelihood_floor"":""VERY_LIKELY""}"
> clu_fedcba9876543210,"{""confidence_ceiling"":""MEDIUM"",""confidence_floor"":""MEDIUM"",""likelihood_ceiling"":""NONE"",""likelihood_floor"":""NONE""}"
> Requirements:
> Include exactly one row for every test id.
> Do not include missing, duplicate, extra, or unknown IDs.
> answer_json must be valid JSON with exactly the four required keys.
> Use only allowed uppercase tokens.
> Both floor values must be less than or equal to their matching ceiling values.
> For either axis, its two endpoints must both be NONE or both be active values.
> What Not To Use
> Do not search the web, report mirrors, snippets, or external corpora using released claim text to recover the omitted phrases.
> Do not use external copies of the source assessment, traceable accounts, annotations, or calibration mappings.
> Do not reverse public IDs, row order, masking patterns, or packet strings into source chapter or answer lookups.
> Do not use private answers, hidden split metadata, preparation artifacts, or challenge scripts as prediction oracles.
> Do not hardcode answers for held-out rows or exact public packet strings.
> Hosted closed-model APIs are not allowed. Local open models and models trained on the public training split are allowed.
> Write predictions to ./working/submission.csv.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Prenatal Development Age-Card Reattachment

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx714ce3xmvevtmzvz2h5y3r6n8bstva
- DOMAIN exactly as displayed: NLP
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
> Predict which detached gestational-age card restores the masked timing in a scientific statement about human prenatal development.
> During evidence curation, a developmental statement and its age profile can become separated. The statement may describe when a structure forms, a pathway appears, a tissue differentiates, an organ matures, or a prenatal transition begins. Each row provides one timing-masked evidence statement and five row-local age cards. Exactly one card contains the gestational range or ranges originally reported by that statement.
> This is an NLP temporal-alignment challenge, not a diagnosis task and not advice about an individual pregnancy. The records are derived from independently published CC BY 4.0 scientific articles. Test articles are completely absent from training. Article titles, authors, journals, DOI values, source IDs, citations, and explicit gestational ages are not released in the public challenge files.
> The objective is to predict selected_card for every test row.
> Dataset
> All public files are under ./dataset/public/.
> train.csv: 181 labeled prenatal evidence rows.
> test.csv: 82 held-out rows from 51 articles absent from training.
> sample_submission.csv: a valid deterministic weak submission.
> The preparation pipeline uses 263 evidence records from 173 independently licensed articles. The train/test split contains no shared article groups, row IDs, or exact public evidence strings. There are 142 distinct native age profiles across the complete prepared corpus.
> Columns
> case_id (string): opaque row identifier derived from the public packet only.
> prompt (string): row-level task instruction.
> evidence_text (string): citation-normalized evidence with all explicit gestational timing replaced by <gestational_age> and direct trimester names replaced by <gestational_phase>. Other standalone numbers may appear as <num>. Rare source-specific terms use collision-prone lex_### tokens; each token is a privacy bucket shared by multiple possible source words, while common developmental and anatomical language remains readable.
> age_cards_json (JSON string): exactly five row-local candidate cards.
> answer_format_json (JSON string): required answer schema.
> organ_family (string): public broad system group used by the robustness metric. Values are NEURAL_SENSORY, CARDIO_RESPIRATORY, PLACENTAL_IMMUNE, VISCERAL_ENDOCRINE, or MUSCULOSKELETAL.
> candidate_region (string): public candidate-set timing group used by the robustness metric. Values are EARLY_CANDIDATES, MIDDLE_CANDIDATES, or LATE_CANDIDATES.
> decoy_hardness (string): public candidate-construction group used by the robustness metric. Values are DENSE_NEIGHBORS, MIXED_NEIGHBORS, or BROAD_NEIGHBORS.
> answer_json (JSON string, train only): the correct card assignment.
> Each object in age_cards_json has this structure:
> {"card_id":"AGE_2","age_ranges":[{"start_week":9,"end_week":12}]}
> An age card contains one to three reported ranges. Endpoints are gestational weeks from 5 through 40. Decimal endpoints are possible when the source reported them. Card IDs are row-local and have no meaning across cases.
> Target
> For each test row, select the one card whose age_ranges restore every <gestational_age> marker in the evidence statement.
> The answer must be a JSON object with exactly one key:
> {"selected_card":"AGE_2"}
> The selected value must be one of the five card_id values in that row's age_cards_json.
> Evaluation
> Scores range from 0 to 1, and higher is better.
> For each age profile, define its center as the mean of all range midpoints. Define its shape from the number of ranges and the mean range width.
> For one row:
> ExactCard is 1 when the selected card is correct and 0 otherwise.
> AgeProximity is 1 for the exact card. For a wrong card it is 0.50 when the center is within 2 weeks of the gold center, 0.25 within 4 weeks, 0.10 within 8 weeks, and 0 otherwise.
> ProfileShape gives 0.5 when the predicted and gold profiles contain the same number of ranges, plus 0.5 when their mean-width categories match. Mean width is the arithmetic mean of end_week - start_week across a card's ranges. The categories are point when mean width is 0, short when it is greater than 0 and at most 3 weeks, medium when it is greater than 3 and at most 8 weeks, and long when it is greater than 8 weeks.
> The row score is:
> row_score = 0.75 * ExactCard + 0.20 * AgeProximity + 0.05 * ProfileShape
> The final score rewards average quality and robustness:
> score = 0.70 * mean_row_score + 0.10 * weakest_organ_family_mean + 0.10 * weakest_candidate_region_mean + 0.10 * weakest_decoy_hardness_mean
> For every robustness axis, weakest means the minimum row-score mean among the public labels present in that scored partition. The grader groups rows using the released organ_family, candidate_region, and decoy_hardness columns, so the grouping rule is fully reproducible from public data.
> candidate_region is computed from the five released cards. First compute each card center as defined above, then average the five card centers. Values at most 12 are EARLY_CANDIDATES, values greater than 12 and at most 24 are MIDDLE_CANDIDATES, and values greater than 24 are LATE_CANDIDATES.
> decoy_hardness records the public decoy-selection schedule. DENSE_NEIGHBORS uses the nearest available profile ranks 0, 1, 2, and 3 on the required sides of the gold profile; MIXED_NEIGHBORS uses ranks 0, 2, 5, and 9; BROAD_NEIGHBORS uses ranks 0, 5, 15, and the farthest available rank, with deterministic filling when a side contains fewer distinct profiles. Every component lies in [0, 1], so the final score is also bounded in [0, 1].
> Submission Format
> Submit exactly two columns in this order:
> case_id,answer_json PNA_0123456789abcdef,"{""selected_card"":""AGE_2""}" PNA_fedcba9876543210,"{""selected_card"":""AGE_0""}"
> Requirements:
> Include every test case_id exactly once and no other IDs.
> answer_json must be valid JSON with exactly selected_card.
> The value must reference a card present in that row.
> Do not add columns or rows.
> Allowed
> Models trained or fine-tuned using only the released public challenge files.
> Open-weight local language encoders, token models trained from scratch, retrieval models, pairwise rankers, and constrained candidate scorers.
> Joint use of the evidence text and every field in the five candidate cards.
> One A10G GPU, up to 10 CPU cores, 62 GB RAM, and 1.5 hours end to end.
> Prohibited
> Searching Europe PMC, PubMed, journal sites, web snippets, or external corpora to recover the masked gestational ages.
> Reverse-mapping lex_### tokens to source words, article identities, authors, titles, DOI values, or source records.
> External prenatal timelines, medical databases, private or gated data, hosted prediction APIs, or hidden answer sources.
> Hardcoded assignments by case_id, row order, card position, exact public evidence string, or challenge-generation artifact.
> Reading private answers, grader files, source archives, or any path outside the provided public directory and requested output path.
> Runtime Contract
> The entrypoint receives the public dataset directory and exact submission path:
> python3 [solution.py](http://solution.py) <public_dir> <submission_out>
> The solution must write the completed CSV to submission_out.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Discourse Scope Transition Path Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f4bpv3gz6cv38qcsq6h41wn8dsax0
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Not displayed; challenge detail page timed out
- Difficulty: Medium
- Compute: Not displayed; challenge detail page timed out
- GPU: Not displayed; challenge detail page timed out
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage card score context: Beat nishantycg5's score of 81.309!

Full challenge description from page:

> Overview Discourse Scope Transition Path Reconstruction is a structured conversational-language challenge over paired semantic checkpoints in naturally occurring multi-turn dialogue. Each sample contains an ordered conversational passage with two marked focus turns: An earlier entry checkpoint. A later exit checkpoint. Each checkpoint contains four competing scope hypotheses extracted from its corresponding turn. Exactly one hypothesis at each checkpoint reproduces the hidden annotated scope. After recovering both scopes, the model must reconstruct three latent paths describing how the semantic record changes between the two checkpoints: A discourse-frame path. A referent-class path. An annotation-lattice path. A submission predicts: entry_scope exit_scope frame_path referent_path lattice_path All outputs are short categorical codes. Participants do not generate text, offsets, JSON structures, explanations, or variable-length programs. A conceptual prediction is: H02, H04, FP07, RP11, LP03 This means: H02 is the selected scope at the entry checkpoint. H04 is the selected scope at the exit checkpoint. FP07 describes the ordered discourse-frame transition. RP11 describes the ordered referent-class transition. LP03 describes the ordered structural transition. The code inventories remain stable throughout the challenge, but their readable meanings are not published. Their behavior must be induced from the released training examples. The target is an ordered transition object rather than an extracted answer. Exact character boundaries, semantic function, referent behavior, and annotation structure must be interpreted jointly across two points in the same conversation. All evaluation is deterministic. No language model, embedding service, human judgment, or semantic similarity API is used by the grader. Conversational Material The released conversations were produced through controlled human dialogue rather than synthetic response generation. Two participants occupy stable conversational channels. One channel advances the exchange through open questions, follow-up prompts, clarifications, and requests for examples. The other supplies personal judgments, descriptions, examples, qualifications, familiarity statements, and other naturally phrased responses. The prompting side avoids forcing a fixed vocabulary wherever possible. This allows the responding participant to introduce relevant expressions using their own language rather than selecting from a predefined menu. Consequently, the corpus contains: Short context-dependent replies. Long explanations containing several relevant expressions. Positive and negative judgments. Neutral descriptions. Statements of familiarity or recognition. Named and unnamed referents. Pronouns and compressed references. Nested semantic regions. Multiple annotations sharing one turn. Different surface forms expressing similar discourse functions. The challenge operates on this native conversational structure. It does not convert the material into conventional question-answer pairs, generate synthetic answers, or score whether a response is subjectively appropriate. Prediction Object Every sample contains: sample_id partition_key dialogue_passage entry_checkpoint exit_checkpoint The hidden target contains: entry_scope exit_scope frame_path referent_path lattice_path The entry checkpoint appears earlier in the conversation than the exit checkpoint. The model must reconstruct the ordered semantic path: Entry scope → conversational progression → exit scope The two scope decisions cannot always be made independently. The intervening dialogue can clarify whether a later phrase continues the same kind of discourse relation, changes the kind of referent under discussion, or moves between an inner and outer annotation layer. Dialogue Passage dialogue_passage contains the complete ordered conversational region surrounding both checkpoints. Each turn contains: turn_key channel content turn_key is local to the sample and identifies the turn referenced by a checkpoint. The conversational channels are: CH01 CH02 Their human-readable participant names are not supplied. Their interaction patterns are stable and can be learned from training data. The passage includes: Context preceding the entry checkpoint. The entry focus turn. Any retained turns between the checkpoints. The exit focus turn. The dialogue may establish: A broad subject that becomes more specific. A named example introduced after a general statement. A person associated with a previously discussed work. A qualification of an earlier judgment. A contrast between two categories. A descriptive statement following an evaluative one. A short reply whose referent was introduced several turns earlier. A transition from recognition to a more explicit judgment. Two scopes that share a semantic class despite using different words. The temporal order is public. The hidden object is the semantic trajectory carried through that order. Semantic Checkpoints Each checkpoint identifies one focus turn and provides four competing scope hypotheses. An entry checkpoint contains: turn_key scope_hypotheses An exit checkpoint contains the same fields. Each hypothesis contains: hypothesis_id left right surface The four local hypothesis identifiers are: H01 H02 H03 H04 Hypothesis identifiers have no meaning outside their checkpoint. H02 at the entry checkpoint does not correspond to H02 at the exit checkpoint. Offsets use half-open character intervals. For every hypothesis: surface == content[left:right] Exactly one hypothesis at each checkpoint reproduces the hidden annotated scope. Scope Competition The hypotheses are competing interpretations of the same local linguistic region. They are not unrelated answer choices. A checkpoint may distinguish among scopes such as: thrillers psychological thrillers like psychological thrillers I generally like psychological thrillers Another may distinguish among: Christopher Nolan films by Christopher Nolan really enjoy films by Christopher Nolan I really enjoy films by Christopher Nolan Every candidate is a valid substring, and several may be grammatically and semantically plausible. The alternatives systematically cover difficult boundary decisions, including: Removing an evaluative predicate. Adding a leading discourse marker. Excluding a negation. Including an adjacent explanation. Selecting a compact referent instead of its surrounding relation. Selecting a wide clause instead of its embedded referent. Choosing the wrong occurrence of repeated surface text. Crossing a coordination boundary. Adding or removing modifiers. Extending into a neighboring semantic region. Candidate order is independently shuffled for every checkpoint. Hypothesis position does not encode correctness, length, class, or transition identity. The candidate interface makes exact scope recovery directly measurable while avoiding the brittleness of asking models to generate arbitrary character offsets. Ordered Frame Path Every hidden scope carries one of four underlying discourse-frame classes. The entry scope has an entry frame, and the exit scope has an exit frame. frame_path represents their ordered pair: Entry frame → Exit frame The public path inventory uses opaque identifiers: FP01 FP02 FP03 FP04 FP05 FP06 FP07 FP08 FP09 FP10 FP11 FP12 FP13 FP14 FP15 FP16 The mapping from ordered frame pairs to FP codes is stable but unpublished. A path distinguishes both membership and direction. A transition from the first latent frame to the third is different from a transition from the third frame to the first. The four underlying frame classes capture recurring conversational functions. Depending on context, a scope may behave like: A compact identifying expression. A wider subjective relation. A descriptive characterization. Another discourse relationship involving a referent. These descriptions characterize the general space without revealing the code mapping. The frame path therefore records whether the conversation: Preserves the same kind of semantic function. Moves from a compact referent to a wider relational statement. Moves from a relational statement to a description. Changes from description to another form of entity relationship. Returns to a previously observed frame. Follows any other ordered combination in the four-state inventory. Participants infer these transitions from labeled trajectories rather than receiving a readable discourse ontology. Ordered Referent Path Every hidden scope also carries one of four underlying referent classes. referent_path represents the ordered pair: Entry referent class → Exit referent class The public inventory contains: RP01 RP02 RP03 RP04 RP05 RP06 RP07 RP08 RP09 RP10 RP11 RP12 RP13 RP14 RP15 RP16 The mapping is stable but unpublished. The four underlying classes capture recurring kinds of entities and concepts found in cultural discussion. Their behavior can be inferred from signals such as: Capitalization. Naming structure. Category terminology. Person-like references. Title-like phrases. Descriptive modifiers. The preceding question. Pronoun antecedents. Associations introduced earlier in the passage. The kinds of predicates applied to the referent. An RP code records direction as well as class membership. A trajectory that begins with a broad category and moves to a named example differs from one that begins with a named example and broadens into a category-level statement. This ordered representation captures local semantic movement without requiring identity-level entity linking that is not explicitly present in the released supervision. Ordered Lattice Path A focus turn may contain several hidden semantic regions with different character boundaries. One scope may: Stand independently. Enclose another annotated region. Be enclosed by a larger annotated region. Participate in shared-boundary or more complex layered structure. Each checkpoint is therefore assigned one of four underlying lattice states. lattice_path represents: Entry lattice state → Exit lattice state The public inventory contains: LP01 LP02 LP03 LP04 LP05 LP06 LP07 LP08 LP09 LP10 LP11 LP12 LP13 LP14 LP15 LP16 The mapping is stable but unpublished. The lattice state is determined through exact relationships between annotated character intervals in the same turn. It does not depend on a learned evaluator. Conceptually, the four structural states represent: Independent scope. Outer scope containing another annotation. Inner scope contained by another annotation. Layered scope involving shared extent, simultaneous relationships, or nontrivial overlap. The ordered lattice path reveals how annotation structure changes through the conversational passage. For example, an entry checkpoint may select a wide relational statement containing a compact referent. The exit checkpoint may select an isolated named example. Another sample may move in the opposite direction, from a compact inner referent to a larger statement expressing how the speaker relates to it. Document-level rhetorical frameworks generally model relations between clauses or discourse units. Here, the structural target is grounded in exact conversational character intervals and follows their movement across two temporal checkpoints. The task is therefore neither rhetorical tree prediction nor connective classification; the recovered path joins span geometry with latent conversational semantics. Path Identifiability The path codes do not appear in the conversation text. They must be inferred from training examples. However, they are not arbitrary sample-level labels. Every path code corresponds to one stable ordered pair of underlying states. A model can learn the system by comparing: Repeated surface patterns. Similar checkpoint boundaries. Different contexts sharing one path code. The same entry behavior followed by different exit behaviors. Reversed transitions. Self-transitions. Nested and non-nested scope combinations. Because the codes are directional, reversing the two checkpoints generally changes the correct target. This discourages bag-of-words classification over the complete passage. The model must identify which linguistic behavior belongs to the entry position and which belongs to the exit position. Coupled Reconstruction The five prediction fields describe one semantic trajectory. They are evaluated separately for partial credit, but they should not be modeled as unrelated outputs. The selected scopes determine which semantic records are being compared. A one-token boundary difference can change: The underlying frame. The structural lattice state. The resulting frame path. The resulting lattice path. Referent interpretation can also depend on scope width. A compact name-like region may point to a different referent behavior than the surrounding clause. The temporal passage constrains the exit checkpoint. An earlier turn may introduce the antecedent needed to classify a later pronoun, while an intervening question may clarify whether the later scope continues or changes the active semantic frame. The complete reconstruction therefore requires: Two exact localization decisions. Directional discourse interpretation. Directional referent interpretation. Directional span-structure interpretation. Consistency across the resulting path. Public Structural Invariants Every released sample obeys the following rules: The dialogue passage contains at least two turns. The entry checkpoint precedes the exit checkpoint. Both checkpoint turns occur in the published passage. Each checkpoint contains exactly four hypotheses. Every hypothesis is a valid substring of its checkpoint turn. Every hypothesis uses half-open character offsets. Every published surface matches its offsets exactly. The four offset pairs within a checkpoint are distinct. Exactly one hypothesis per checkpoint matches the hidden target scope. Entry and exit targets are nonempty. Every frame path belongs to FP01 through FP16. Every referent path belongs to RP01 through RP16. Every lattice path belongs to LP01 through LP16. Path mappings remain stable throughout the challenge. Hypothesis order is independently shuffled. Original conversation identifiers are not exposed. Public identifiers contain no target information. Released Dataset The public package contains: train.jsonl test.jsonl sample_submission.csv There is no public answer file. There is no public path dictionary. There is no public mapping from path codes to underlying state pairs. There is no official validation file. Training Data Each line of train.jsonl contains one JSON object. Training rows contain: sample_id partition_key dialogue_passage entry_checkpoint exit_checkpoint entry_scope exit_scope frame_path referent_path lattice_path sample_id Type: string. This field is used only for submission alignment. It has no semantic meaning and must not be used as a predictive feature. partition_key Type: string. An opaque grouping identifier for related conversational material. Participants should use it to create leakage-safe local validation splits. The identifier value itself has no semantic meaning. dialogue_passage Type: list of turn objects. Each turn contains: turn_key channel content Turns appear in chronological order. entry_checkpoint Type: object. Contains: turn_key scope_hypotheses The referenced turn is the earlier semantic checkpoint. exit_checkpoint Type: object. Contains: turn_key scope_hypotheses The referenced turn is the later semantic checkpoint. scope_hypotheses Type: list of four objects. Each object contains: hypothesis_id left right surface entry_scope Training only. Type: string. One of: H01 H02 H03 H04 exit_scope Training only. Type: string. One of: H01 H02 H03 H04 frame_path Training only. Type: string. One of FP01 through FP16. referent_path Training only. Type: string. One of RP01 through RP16. lattice_path Training only. Type: string. One of LP01 through LP16. Test Data Each line of test.jsonl contains: sample_id partition_key dialogue_passage entry_checkpoint exit_checkpoint The test file omits: entry_scope exit_scope frame_path referent_path lattice_path The test data does not expose: Underlying frame classes. Underlying referent classes. Underlying lattice states. Path-code mappings. Original annotation names. Original conversation identifiers. Original source row positions. Construction metadata. Hidden annotations outside the two targets. Conversation-Disjoint Split The official split is performed by complete conversation. Every example derived from one conversation remains entirely within training or entirely within test. This includes: Different checkpoint pairs. Different annotations from the same turn. Inner and outer scopes. Neighboring conversational passages. Repeated references. Alternative hypothesis configurations. Reversed semantic patterns occurring in the same dialogue. No conversation contributes context to one split and targets to another. Local Validation Participants should split local validation by partition_key. A random row split may place closely related checkpoint pairs on both sides. Related examples can share: One checkpoint. One focus turn. Nearly identical lead-ins. Different target annotations from the same turn. Inner and outer members of one annotation lattice. Overlapping conversational windows. Grouping by partition_key provides a more reliable estimate of generalization to unseen conversations. Submission Format The submission contains exactly six columns: sample_id entry_scope exit_scope frame_path referent_path lattice_path Example: DSPR_7A29F4,H02,H04,FP07,RP11,LP03 Valid scope values are: H01 H02 H03 H04 Valid frame paths are: FP01 through FP16 Valid referent paths are: RP01 through RP16 Valid lattice paths are: LP01 through LP16 Every expected sample_id must appear exactly once. Invalid submissions include: Missing samples. Extra samples. Duplicate sample identifiers. Missing columns. Extra columns. Incorrect column order. Unknown scope identifiers. Unknown path codes. Blank predictions. Use sample_submission.csv exactly. There is no free-form prediction grammar. A valid row requires only five short categorical predictions. Evaluation Submissions are evaluated using the Discourse Scope Transition Path Reconstruction Score. The score ranges from: 0.01 to 100 Higher is better. A perfect reconstruction receives exactly 100. The metric contains seven published components: Entry Scope Accuracy. Exit Scope Accuracy. Mean Scope Overlap. Frame Path Macro F1. Referent Path Macro F1. Lattice Path Macro F1. Complete Trajectory Accuracy. There are no hidden metric weights, hidden subsets, or learned evaluation components. Entry and Exit Scope Accuracy For each checkpoint: Correct hypothesis selection receives 1. Incorrect selection receives 0. Let the dataset-level entry accuracy be: Entry Let the dataset-level exit accuracy be: Exit The combined exact scope value is: ScopeExact = sqrt(Entry × Exit) The geometric mean requires reasonable localization at both checkpoints. Mean Scope Overlap At each checkpoint, the selected hypothesis interval is compared with the hidden target interval using character intersection-over-union: SpanIoU = intersection length / union length Identical intervals receive 1. Disjoint intervals receive 0. A contracted or expanded alternative can receive partial credit according to its actual boundary overlap. The overlap values are averaged across both checkpoints and all samples. Let this value be: Overlap Frame Path Macro F1 F1 is calculated separately for every supported FP code and then macro-averaged. Let the result be: FramePath Each directional path receives equal class-level importance, preventing common self-transitions from dominating the metric. Referent Path Macro F1 F1 is calculated separately for every supported RP code and macro-averaged. Let the result be: ReferentPath Lattice Path Macro F1 F1 is calculated separately for every supported LP code and macro-averaged. Let the result be: LatticePath Only path codes represented in the official target inventory are included. Every test path also appears in the released training data. Complete Trajectory Accuracy A sample receives complete-trajectory credit only when all five predictions are correct: Correct entry scope. Correct exit scope. Correct frame path. Correct referent path. Correct lattice path. Otherwise, it receives zero. Let the dataset-level fraction be: Complete This component rewards internally consistent reconstruction without replacing the graded partial-credit components. Final Score First calculate localization quality: Localization = sqrt(ScopeExact × Overlap) Then calculate path quality: PathCore = (FramePath × ReferentPath × LatticePath)^(1/3) The final score is: Discourse Scope Transition Path Reconstruction Score = 100 × Localization^0.50 × PathCore^0.50 × (0.85 + 0.15 × Complete) The result is clipped to: [0.01, 100] A perfect prediction has: Entry = 1 Exit = 1 Overlap = 1 FramePath = 1 ReferentPath = 1 LatticePath = 1 Complete = 1 and receives exactly: 100 The multiplicative structure prevents a system from succeeding through only scope localization or only majority-path prediction. Close scope boundaries receive partial overlap credit, but incorrect boundary decisions still damage exact scope and complete-trajectory recovery. Macro-averaged path evaluation ensures that uncommon semantic transitions remain important. Reproducing the Metric Locally For each validation sample: Read the predicted entry and exit hypotheses. Compare both choices with their gold hypotheses. Retrieve the corresponding character intervals. Calculate entry and exit span intersection-over-union. Accumulate predictions for every frame-path class. Accumulate predictions for every referent-path class. Accumulate predictions for every lattice-path class. Check whether the complete five-field trajectory is exact. Calculate the three macro F1 values. Calculate ScopeExact. Calculate Localization. Calculate PathCore. Apply the final formula. Clip the result to the published range. No tokenizer, ontology file, external model, or private semantic resource is needed to reproduce the score. Challenge Regime This is a pretrained fine-tuning challenge. Pretrained models are allowed. Participants may use: Pretrained bidirectional encoders. Pretrained encoder-decoder models. Decoder-only language models. Instruction-tuned language models. Long-context encoders. Multi-task classification heads. Span-ranking architectures. Parameter-efficient fine-tuning. Model ensembles. Training from random initialization is permitted but not required. Compute The execution environment provides one NVIDIA A10G GPU. The environment supports: Mixed-precision training. Full fine-tuning of compact or medium-sized encoders. Parameter-efficient tuning of larger models. Batched hypothesis scoring. Joint path classification. Cross-encoder reranking. Small neural ensembles. Cached passage representations. Remote inference APIs are not allowed. All predictions must be produced inside the competition environment. Modeling Directions A direct baseline can encode: The complete dialogue passage. The entry hypotheses. The exit hypotheses. A shared encoder can feed: An entry-scope classification head. An exit-scope classification head. A frame-path classification head. A referent-path classification head. A lattice-path classification head. A stronger model can construct representations for the selected or candidate entry-exit pairs. There are sixteen possible ordered hypothesis pairs: 4 × 4 = 16 Each pair can be combined with learned path representations. Useful approaches include: Cross-encoding every entry-exit hypothesis pair. Hierarchical encoding of turns and candidate spans. Boundary representations using tokens inside and outside each hypothesis. Joint scope-pair classification. Multi-task path prediction. Contrastive training over correct and incorrect scope pairs. Auxiliary prediction of individual latent states. Consistency losses between predicted states and path codes. Complete-trajectory reranking. Ensembles combining local boundary and full-passage models. A high-capacity system may internally recover the latent entry and exit classes, then map their ordered pair to the public path code. Another system may predict the opaque path directly. Both approaches produce the same simple categorical submission. Useful Signals Potential signals include: Scope length. Tokens immediately outside a candidate. Clause boundaries. Negation. Intensifiers. Evaluative predicates. Descriptive constructions. Familiarity expressions. Capitalization. Possessive syntax. Person-like names. Title-like phrases. Category terminology. Pronoun antecedents. The question preceding each checkpoint. Semantic continuity between checkpoints. Whether the later turn narrows or broadens the subject. Whether a candidate contains another plausible candidate. Whether an entry and exit scope share structural behavior. Whether the frame appears stable or directional. Whether the referent family changes across the passage. No individual lexical heuristic determines the complete trajectory. Difficult Cases Expected difficult cases include: Two checkpoints with almost identical surface language but different frames. Different surface language representing the same latent path. Entry and exit candidates differing by one boundary token. Negation just outside a compact hypothesis. A compact inner referent competing with a wider relation. Pronouns resolved through earlier turns. Named expressions resembling ordinary phrases. Descriptive statements resembling evaluations. Familiarity statements resembling positive judgment. Transitions that reverse common conversational patterns. Rare directional path codes. Shared-boundary annotations. Layered lattice states. Correct local scopes paired with the wrong directional path. Correct path behavior inferred from incorrectly selected scopes. Long intervening dialogue between checkpoints. Later turns that qualify or partially reverse earlier statements. Allowed Resources Participants may use: Released challenge files. Public pretrained language models. Public pretrained tokenizers. Standard numerical libraries. Standard machine-learning libraries. Standard deep-learning frameworks. Unicode-processing libraries. Locally derived features. Auxiliary targets derived from released training labels. Ensembles that fit the runtime limits. Disallowed Resources Participants may not use: Hidden test targets. Private evaluator files. Manual annotation of test samples. External copies of evaluation conversations. External answer-key lookup. Original source identifiers for label recovery. Hard-coded test predictions. Submission-feedback reconstruction. Remote language-model APIs. Online human annotation. sample_id as a predictive feature. partition_key as a semantic feature. Row order as a predictive feature. Filename order as a predictive feature. General pretrained language knowledge is allowed. Direct evaluation-target recovery is not. Limitations The challenge focuses on short and medium-length conversational passages rather than document-scale discourse. The underlying frame, referent, and lattice inventories are finite. Some directional paths are naturally more frequent than others, which is why the official metric evaluates path codes using macro F1. The benchmark does not directly evaluate: Open-web retrieval. Long-form generation. Response helpfulness. Recommendation quality. Current factual knowledge. Document-level rhetorical parsing. Free-form dialogue generation. It isolates the reconstruction of an evolving semantic record across two conversational checkpoints. Expected Outcome A successful system should: Interpret two locations in a shared conversational history. Select exact scopes from closely related alternatives. Use context to resolve short or ambiguous expressions. Infer stable latent semantic states from training data. Recover directional frame transitions. Recover directional referent transitions. Recover directional annotation-structure transitions. Generalize across conversation-disjoint partitions. Produce a reliable six-column categorical submission. Train and infer efficiently on one A10G GPU. The final objective is: Recover the paired semantic scopes and decode the latent discourse, referent, and lattice paths connecting them across the conversation.
> $700 Pool
> Closes in 10h 19m
> 8 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Vietnamese Persona Fragment Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cvvzgq1n42pm6g2jqenpnzs88wxw9
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat morax's score of 0.729!

Full challenge description from page:

> Vietnamese Persona Fragment Reconstruction Overview Large persona collections are often assembled through independent generation, enrichment, and export stages. One person may have separate professional, cultural, recreational, travel, and lifestyle descriptions. When identifiers are removed or records are joined incorrectly, fluent and individually plausible fragments can be attached to the wrong profile. Each case in this challenge contains six anonymized anchor profiles and six shuffled fragment bundles written in Vietnamese. The six bundles have a one-to-one set of primary owners. Five bundles are internally clean. One bundle contains two fragments from its primary owner and one fragment copied from a different anchor in the same case. Your model must reconstruct the complete bundle-to-anchor assignment, identify the contaminated bundle, identify the donor anchor that supplied the foreign fragment, and locate the contaminated slot inside that bundle. Bundle assignment is only an intermediate step: the primary research objective is end-to-end provenance repair—detecting a coherent-looking cross-profile fault and tracing both where it entered and which in-context profile supplied it. This is not ordinary persona classification or independent pairwise record linkage. Anchor and bundle labels are local to one case, every valid owner prediction must form a permutation, and the repair decision depends on all six profiles jointly. Cases use hard-negative cohorts whose members have similar demographic and topical characteristics. Direct identifiers, names, source-row keys, exact ages, and explicit demographic columns are not released. Rare exact phrases that directly join an anchor to its bundle are masked during data preparation. The intended solution learns cross-view semantic compatibility and performs constrained global matching. The task represents quality control for synthetic-data pipelines, customer-profile enrichment, survey integration, and privacy-preserving record reconciliation: detecting when a coherent-looking profile has been assembled from more than one latent source. Data Provenance and Privacy The challenge narratives are synthetic adult personas written in standard Vietnamese; they are not records of real people. The demographic prior is documented by two exact official publications from Vietnam's national statistics authority: Results of the 2024 Mid-term Population and Housing Census for population structure, sex, province, residence, and urban-rural context, and Results of the Viet Nam Household Living Standards Survey 2024 for education, employment, occupation, household conditions, and regional living context. These publications document the population-level conditioning evidence; they contain no challenge cases or answers. The resulting synthetic profiles cover six Vietnamese provinces and centrally administered municipalities and reflect Vietnamese occupation, education, residence, and cultural contexts rather than translations of a generic English persona benchmark. Creator-side transformation retains seven complementary narrative views per selected profile—cultural background, skills, career goals, sports, arts, travel, and culinary behavior—but removes record identifiers, personal names, exact ages, structured demographic fields, and original row order. Repeated proper entities and rare exact tokens shared between anchor and lifestyle views are masked. These operations preserve the Vietnamese cross-view semantic problem while preventing catalog lookup, exact-name joins, and demographic elimination. Before challenge assembly, the synthetic-persona construction follows a documented generate-then-audit pipeline. Population tables define categorical priors for adult demographic, education, occupation, region, and residence variables. A probabilistic graphical model samples a structured persona state from those priors; where no public joint table is available, demographic effects are modeled as independent conditional inputs rather than presented as observed individual-level correlations. A Vietnamese text generator then renders the seven narrative views from the sampled state. Automated consistency checks and local cultural review are applied before a profile is eligible for challenge construction. The statistical publications above provide population-level grounding only: no surveyed person, household response, or census micro-record is converted into a challenge persona. Unlike a conventional persona corpus that releases independent records for generation or retrieval, the challenge-generation pipeline is a reproducible sequence of five transformations: retain adult Vietnamese profiles with all seven required narrative views; form exact context cells on sex, region, residence zone, occupation category, and education level using creator-only structured attributes; order profiles inside each cell by a fixed six-dimensional TF-IDF/SVD representation of skills and interests, then place adjacent profiles into non-overlapping six-person hard-negative cohorts; remove identifiers and demographic fields, mask repeated entities and rare exact anchor-to-view link tokens, and split complete cohorts before generating any target; and independently shuffle anchor and bundle labels inside each case, then replace one bundle slot with an unused view from another cohort member and record the owner, donor, bundle, and slot targets. This pipeline changes both the learning unit and the research question. The released unit is not an independently generated persona but a closed, confusable six-profile system with a known single-source integrity violation. Every transformation needed to reproduce the task is stated here, while the withheld creator-only attributes cannot be exploited by participants. The hard-negative step is deterministic. For every eligible profile r, define: context_key(r) = (sex, region, residence_zone, occupation_category, education_level) and concatenate its creator-side skills list and interests list into semantic_text(r). Fit word unigram-and-bigram TF-IDF with min_df=5, max_df=0.65, max_features=18000, and sublinear term frequency. Reduce the resulting matrix to six dimensions using truncated SVD with random_state=91027. Within each exact context_key, lexicographically sort by the six SVD coordinates, partition consecutive records into groups of six, and discard only the final incomplete remainder. No profile is sampled twice. This definition makes cohort construction reproducible and explains why simple demographic blocking or random-negative performance does not characterize the released task. What Makes This Different The closest related setup identified during platform review, PerspectiveGap, assigns shuffled text fragments to globally labeled roles under distractor conditions. This challenge instead combines four constraints in one case-level recovery problem: a latent six-by-six identity permutation, one semantically plausible cross-profile contamination, identification of both the contamination donor and its exact slot, and an exact-recovery premium tied to a complete usable repair. Anchor, bundle, donor, and slot tokens are local to each case, so a solver cannot learn a global label dictionary or treat the six matches as unrelated classifications. The hard negatives are constructed specifically from the Vietnamese persona domain. Creator-side structured attributes first place profiles into exact context cells sharing sex, region, residence zone, occupation category, and education level. Within each cell, profiles are ordered in a six-dimensional semantic neighborhood derived from their skills and interests, then adjacent profiles are grouped into cohorts of six. The attributes and neighborhood coordinates used for cohort creation are not released. Consequently, each candidate set is deliberately similar both demographically and topically, while the correct links depend on complementary evidence spread across Vietnamese cultural, professional, goal, sport, art, travel, and culinary narratives. Every selected profile appears in exactly one cohort, and complete cohorts are kept intact across train, test, public, and private boundaries. Contamination is injected only after splitting by replacing one of three bundle fragments with an unused lifestyle view from another member of the same hard-negative cohort. The donor is therefore a plausible in-context alternative rather than an arbitrary out-of-domain distractor. This construction turns ordinary persona text into a controlled multi-view provenance audit that jointly tests semantic association, global matching, anomaly localization, and source attribution. Explicit Comparison with Public Prior Work | Public work | Standard prediction unit and output | Structural difference in this challenge | | --- | --- | --- | | PerspectiveGap | Routes shuffled information fragments to predefined multi-agent roles and measures required coverage and distractor leakage. | Identities here are latent and case-local; outputs must form a six-way bijection and must attribute one injected cross-identity fragment to its donor and slot. Role routing does not perform entity provenance repair. | | Meddies Persona VIE | Provides independent synthetic Vietnamese patient profiles as context for healthcare dialogue, intake-note, triage, and workflow generation. | This challenge is non-clinical and does not evaluate persona generation. It transforms profiles into disjoint six-identity hard-negative systems and scores reconstruction plus localization and attribution of a controlled cross-profile integrity fault. | | DeepMatcher | Learns match versus non-match decisions for labeled record pairs, including textual and dirty entity-matching cases. | Six pair scores cannot be accepted independently: all 36 anchor-bundle relations compete inside one permutation, and a mostly correct bundle can contain a foreign fragment requiring source diagnosis. | | Ditto | Serializes two records and fine-tunes a language model for binary sequence-pair entity matching. | Pair classification supplies compatibility edges but neither enforces the complete local bijection nor predicts contaminated bundle, donor identity, and within-bundle location. | | Clean-Clean Entity Resolution with bipartite graph matching | Converts similarities between two duplicate-free sources into matched record pairs using bipartite graph algorithms. | It supplies the closest standard analogue to the ownership permutation, but assumes each record is internally attributable to one entity and has no target for a single foreign component, its source, or its position. | Accordingly, the novelty claim is not that pairwise text similarity or Hungarian assignment is new. Those are admissible components. The new evaluation unit is a closed repair transaction in which global entity assignment and fine-grained provenance failure must be solved consistently. A conventional entity matcher can generate the 36 compatibility edges, but it does not by itself define or solve the three contamination targets or the exact joint-repair objective. Why Fragment Assignment Alone Is Insufficient An ownership matcher can assign a bundle correctly from its two clean fragments while remaining unable to identify the foreign fragment, its donor, or even which bundle is contaminated. The benchmark therefore treats ownership reconstruction as a prerequisite for the central provenance audit, not as a substitute for it. The required repair triple is coupled to the permutation: donor_owner must refer to a different member of the same six-profile cohort, and contaminated_slot must locate the evidence that violates the predicted primary ownership. Frozen held-out baselines demonstrate this separation. A valid random submission scores approximately 0.1590 on the combined metric. A word-overlap Jaccard matcher with Hungarian assignment improves owner accuracy to 0.3722, compared with the 0.1667 chance level, yet obtains only 0.1842 contaminated-bundle accuracy, 0.1737 donor accuracy, and 0.3192 slot accuracy. Those audit results remain near their chance references of 0.1667, 0.2000, and 0.3333, and the combined score is only 0.2533. Thus surface fragment assignment partially recovers ownership but provides essentially no solution to contamination tracing. A stronger no-learning TF-IDF plus Hungarian pipeline reaches 0.3285 on the same combined objective, while a supervised semantic compatibility model trained on the released cases reaches 0.3723. The gap shows that training on cross-view relations adds measurable value, but both results remain far below exact repair. These baselines make the intended novelty testable: progress must come from jointly modeling constrained identity reconstruction, within-cohort anomaly localization, and donor attribution rather than relabeling an existing fragment-assignment solution. Reference Compositional Baseline The reference baseline deliberately combines standard components; none is claimed as a new algorithm. It first reconstructs clean training identities from released labels. Word unigram-bigram and character 3-4-gram TF-IDF features are projected into a 192-dimensional latent space. Ridge mappings between anchor and fragment representations plus lexical and latent similarities produce eleven features for each of the 108 anchor-slot candidates in a case. Histogram gradient-boosted compatibility scorers add ranks and within-case standardized scores. Owner evidence is aggregated across each bundle using mean, top-two, minimum, and maximum slot compatibility. A Hungarian assignment converts the resulting six-by-six matrix into the required owner permutation. Conditional on those predicted owners, an auxiliary contamination classifier compares every owner's compatibility with the best alternative anchor at all 18 bundle slots. Its highest-probability cell supplies the contaminated bundle and slot; the highest-scoring non-owner anchor at that cell supplies the donor. This composition is a concrete baseline for the complete contract rather than six disconnected classifiers. On a fixed 7,000-case training and 1,000-case validation split, this baseline obtains 0.5532 owner accuracy, 0.2340 contaminated-bundle accuracy, 0.2320 donor accuracy, 0.3680 slot accuracy, 0.0230 exact joint accuracy, and a 0.3591 challenge score. The result clarifies what the benchmark measures: standard matching and assignment components recover much of the ownership structure, while within-cohort provenance repair remains the limiting capability. The benchmark contribution is therefore the reproducible cohort construction, coupled output contract, and diagnostic evaluation of this unresolved composition—not a claim that TF-IDF, gradient boosting, or Hungarian assignment is individually novel. Task For every test case, predict nine values: the primary owner of bundle B0; the primary owner of bundle B1; the primary owner of bundle B2; the primary owner of bundle B3; the primary owner of bundle B4; the primary owner of bundle B5; which bundle is contaminated; which anchor donated the foreign fragment; and which slot in the contaminated bundle contains that fragment. Anchor tokens are A0 through A5. Bundle tokens are B0 through B5. Slot tokens are S0 through S2. Tokens are assigned independently inside every case and have no meaning across cases. Each primary owner appears exactly once across the six bundles. The donor is always different from the primary owner of the contaminated bundle. Dataset The prepared challenge contains 14,400 independent cases: 12,000 labeled training cases; 2,400 unlabeled test cases; six anchor profiles per case; six shuffled fragment bundles per case; and three fragments per bundle. Every case is built from six different latent profiles. A latent profile is used in only one challenge case and never crosses the training and test boundary. Closely related hard-negative groups are also kept on one side of the split. Test visibility is assigned by complete case. A case and all nine of its targets are always entirely public or entirely private. Case Records Each line of train.jsonl or test.jsonl is one JSON object. Anchors The anchors object has six keys, A0 through A5. Each anchor contains three complementary descriptions: background - cultural and social background; skills - professional and personal capabilities; and goals - career goals and longer-term ambitions. These descriptions establish the latent identity that bundles must be matched against. Direct names, UUIDs, exact ages, and catalog identifiers are not provided. Bundles The bundles object has six keys, B0 through B5. Every bundle contains three passages named S0, S1, and S2. The passages are drawn from lifestyle views covering sports, arts, travel, and culinary behavior. The selected view types and slot order are randomized separately for every profile. For a clean bundle, all three slots originate from its primary owner. For the single contaminated bundle, two slots originate from its primary owner and one slot originates from the donor anchor. The six primary owners always form a one-to-one assignment. The foreign fragment does not change the primary owner of the contaminated bundle. Training Targets Training records additionally contain a targets object with: owner_b0 through owner_b5 - primary owner token for each bundle; contaminated_bundle - one of B0 through B5; donor_owner - one of A0 through A5; and contaminated_slot - one of S0, S1, or S2. The targets object is absent from test.jsonl. Files train.jsonl Labeled training cases. Each record contains case_id, anchors, bundles, and targets. test.jsonl Unlabeled test cases. Each record contains case_id, anchors, and bundles. sample_submission.csv A complete submission template with one row for every test case and all required prediction columns. Evaluation The final submission score ranges from 0.001 to 1.0, and higher is better. Individual case scores range from 0.0 to 1.0; the 0.001 floor is applied only after the case scores are averaged into the final submission score. For test case i, define bundle-owner accuracy as: owner_accuracy_i = (1 / 6) * sum over j=0..5 of I(predicted_owner_bj = true_owner_bj) Define three audit indicators: bundle_hit_i = I(predicted_contaminated_bundle = true_contaminated_bundle) donor_hit_i = I(predicted_donor_owner = true_donor_owner) slot_hit_i = I(predicted_contaminated_slot = true_contaminated_slot) Define exact joint recovery as: joint_hit_i = I(all six owner predictions are correct AND bundle_hit_i = 1 AND donor_hit_i = 1 AND slot_hit_i = 1) The per-case score is: case_score_i = (0.45 * owner_accuracy_i) (0.15 * bundle_hit_i) (0.15 * donor_hit_i) (0.10 * slot_hit_i) (0.15 * joint_hit_i) The five coefficients sum to 0.45 + 0.15 + 0.15 + 0.10 + 0.15 = 1.00. Every * shown above is a multiplication operator. Metric Design Rationale The metric has two deliberate layers. The first 0.85 is decomposable partial credit: it measures how much of the reconstruction and contamination diagnosis is correct, so models that improve one part of the task receive measurable credit even before they solve a complete case. The remaining 0.15 is an exact-recovery premium. In the intended quality-control workflow, a case is ready for automatic repair only when all six owners and the entire contamination triple are jointly correct; one wrong field still requires human reconciliation. A solver that never produces a fully usable repair is therefore intentionally prevented from reaching the perfect score, while its partial progress remains visible. The component weights reflect the structure and difficulty of the output. Reconstructing the six-way one-to-one ownership map is the central task and receives 0.45, with partial credit per correctly assigned bundle. Identifying the contaminated bundle and its donor are separate six-way decisions that each receive 0.15. Locating the contaminated slot is a lower-entropy three-way decision, so it receives the smaller weight 0.10 and cannot dominate the score through easy guessing. The 0.15 joint term is not a second estimate of any single field: it measures the non-additive operational outcome that the complete repair is usable without correction. Independent audit credit and the joint premium serve different purposes rather than double-counting the same quality goal. The independent terms preserve diagnostic resolution and stable ranking among imperfect systems; the joint term distinguishes systems that combine those parts coherently into exact end-to-end recovery. The nominal 0.85 ceiling of the partial-credit layer is thus intentional, transparent, and subordinate to the documented exact-recovery objective. The final score is the arithmetic mean over all evaluated cases: score = (1 / N) * sum over i=1..N of case_score_i The six owner predictions in every row must be a permutation of A0, A1, A2, A3, A4, and A5. The predicted donor must differ from the predicted primary owner of the predicted contaminated bundle. File-level structural and identifier errors reject the complete submission with a descriptive validation exception. These errors include missing, extra, duplicate, or reordered columns; a missing or extra row; a non-DataFrame input; and a missing, extra, blank, malformed, or duplicate case_id. The exception identifies the violated contract so the file can be corrected. Prediction-value errors are scored locally. A row receives case_score_i = 0 if any of its nine predictions is blank, non-string, non-finite, surrounded by whitespace, or an unknown token; if its six owner values are not an exact permutation of A0 through A5; or if its donor equals the predicted primary owner of its predicted contaminated bundle. Other valid rows retain their normal scores. If the resulting submission mean is below 0.001, the reported score is clipped to 0.001. Submission Format Submit one CSV file with exactly these columns in exactly this order: case_id owner_b0 owner_b1 owner_b2 owner_b3 owner_b4 owner_b5 contaminated_bundle donor_owner contaminated_slot A correctly formatted submission begins as follows: case_id,owner_b0,owner_b1,owner_b2,owner_b3,owner_b4,owner_b5,contaminated_bundle,donor_owner,contaminated_slot C000012,A4,A0,A5,A1,A3,A2,B3,A5,S1 In this example, bundle B3 has primary owner A1, while its foreign fragment came from A5 and appears in slot S1. Column names, case identifiers, anchor tokens, bundle tokens, and slot tokens are case-sensitive. Training Guidance This is a supervised fine-tuning challenge. Useful approaches include: fine-tuning a compact Vietnamese or multilingual text encoder; contrastive learning between anchor and fragment representations; cross-encoder scoring of anchor-fragment compatibility; bipartite assignment or a differentiable matching layer for the six-owner permutation; auxiliary prediction of bundle coherence, donor identity, and contaminated slot; and an ensemble in which lexical features support, but do not replace, a trained semantic model. The released data is compact enough for CPU text pipelines and compact encoders. A GPU can accelerate fine-tuning but is not required for a valid solution. Expected Output For every test case, return the one-to-one assignment of six bundles to six case-local anchors together with the complete contamination repair triple: contaminated bundle, donor anchor, and contaminated slot. What Not to Use Do not search for, download, or match against external copies of the underlying persona collection. Do not reconstruct hidden UUIDs, names, source-row order, generation seeds, or original record identifiers. Do not use external persona corpora, demographic lookup tables, source-generator prompts, or template dictionaries to identify records. Do not build a hand-written phrase table that maps generator-specific wording directly to test assignments. Lightweight lexical features are allowed only as supporting inputs to a model trained on the released challenge data. Do not manually label test cases or create test-specific owner, donor, or slot rules after inspecting individual test records. Do not infer targets from case IDs, JSON order, row order, token spelling, file offsets, or public/private leaderboard probing. Do not access private answers, grader internals, hidden preparation artifacts, or grading-environment data. Solutions must learn from released training cases and generalize to unseen case-local identities and hard-negative cohorts. &nbsp;
> $700 Pool
> Closes in 40m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Review-Panel Ground Attribution for Assistant Response Comparisons

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75j8rhsnww4qfvhgmr65wtjs8byr64
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Review-Panel Ground Attribution for Assistant Response Comparisons
> Overview Before a comparison reaches a review panel, someone has to guess what the panel is going to end up arguing about. Get that guess right and the item goes to a reviewer who can actually adjudicate it - a language specialist, someone who can run the code, someone with the domain to spot a missing step. Get it wrong and the item comes back unresolved, or resolved by whoever happened to be free. That guess is the task here, and it is a forecast about people, not a verdict about text. Each record is one comparison that a three-person panel has already worked through, where all three reviewers independently landed on the same ground. You get what the panel got: the user's request and the two candidate responses, as the bounded excerpts a review queue actually displays. You do not get a single word the reviewers wrote - their write-ups are held back, and they are the only thing the label is built from. Read the exchange and name the ground the panel argued on. The three grounds correctness - the panel argued about something being WRONG: a factual, logical or mathematical mistake, an invented detail, or code that is buggy, does not run, or produces the wrong result. instruction_compliance - the panel argued about whether a response DID WHAT WAS ASKED: answered in the wrong language, ignored a stated constraint on length, count, format or style, answered a different question, drifted off topic, or declined an in-scope request. completeness - the panel argued about HOW MUCH relevant ground a response covered: parts of a multi-part request left out, missing steps, a shallower or less actionable explanation, fewer useful details or examples. Nothing is wrong; there is simply less of it. What separates this from scoring a response is that the target is a property of the panel's reasoning, not of either response. You are not asked which answer won, and you cannot get there by working out which is better: a panel converges on correctness whichever way it ruled, and two comparisons with identical verdicts routinely turn on different grounds. Panels that pulled apart - where the three reviewers justified their calls on different grounds - are excluded entirely, so every record here has one answer three people independently agreed on. Dataset Three files are provided. train.csv - 2,370 labelled rows. Columns: record_id, exchange, decisive_dimension. test.csv - 720 unlabelled rows to predict. Columns: record_id, exchange. sample_submission.csv - the required submission shape, filled with a single ground so that it scores at the floor. Columns: record_id - string. Opaque row identifier of the form rec_00000. Carries no information about the answer. exchange - string, the only input feature. Holds the user's request and the two candidate responses under [REQUEST], [RESPONSE A] and [RESPONSE B] markers. Long passages appear as an opening and a closing segment separated by [...], which is the display budget a review queue works under. Which candidate appears as A and which as B is randomised per record and carries no information. Mean length about 725 characters. decisive_dimension - string, the target. One of correctness, instruction_compliance, completeness. The training and evaluation sets are exactly balanced across the three. Submission Submit a CSV with exactly two columns, record_id and decisive_dimension, one row per evaluation record in test.csv, using exactly the three dimension names above. A correctly formatted submission looks like this: record_id,decisive_dimension rec_00007,correctness rec_00019,completeness rec_00042,instruction_compliance rec_00058,correctness Every record_id in test.csv must appear exactly once. sample_submission.csv ships the same shape, filled with a single dimension so it scores at the floor. Generalization Panels work across a wide spread of natural and programming languages, and an attribution system is deployed on locales it was not trained on. The evaluation records are drawn entirely from locales that appear nowhere in the training data. Related locales are represented in training - for every held-out natural language there are others from its family, and for every held-out programming language there are others sharing its lineage - so the notion generalises, but any signal tied to specific vocabulary will not survive the move. Because the evaluation set is drawn from locales that never appear in training, a random split of the training rows will overstate how a model will do on the evaluation set: it lets a model lean on locale-specific vocabulary that is worthless on the unseen evaluation locales. Validate the way you are scored - hold whole languages out of your training fold and read your estimate off them. Scoring Macro-F1 across the three dimensions, rescaled so that a submission which merely reproduces the label frequencies scores 0: score = max(0, (macro_F1 - 1/3) / (2/3)) Higher is better; the score lies in [0, 1]. Macro averaging means every dimension counts the same, so leaning on the easiest one does not pay. Submissions with missing, duplicated or unrecognised records, or with dimension names outside the three above, are rejected rather than scored. Review queues are rebuilt continuously as new response pairs arrive, so an attribution system is only useful if it is cheap to rebuild on each refresh. The corpus is deliberately small and the reference solution finishes comfortably inside the challenge's modest runtime budget; nothing here rewards scale for its own sake. Source and attribution The corpus is derived from NVIDIA HelpSteer3 (CC-BY-4.0), whose preference records carry per- reviewer written justifications. Those justifications were read offline to derive the dimension label and are not distributed with this challenge. What Not To Use No external data. In particular, do not retrieve, download or reconstruct the upstream HelpSteer3 corpus or any other annotation corpus, and do not attempt to match evaluation records back to an external source in order to recover reviewer text. The label is derived from material deliberately withheld; recovering it from outside the challenge data is not a solution to this task. No external API calls and no hosted or remote model inference at grading time. Do not use the evaluation split as supervision, directly or through self-labelling. No hardcoded lookups keyed on record_id, and no fingerprinting of individual evaluation rows. No attempt to identify the reviewers or the assistant systems behind the responses.
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Spatial Witness Arbitration

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75v2hfqvb271gj0p82p0ffvs8dr122
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat draken_dev's score of 93.029!

Full challenge description from page:

> Overview Spatial Witness Arbitration is a multi-case language reasoning challenge built around incomplete descriptions of geometric worlds. Each record behaves like a compact arbitration hearing: four cases describe objects, blocks, attributes, and spatial relationships, but one decisive statement has been withheld from every narrative. The missing statements are mixed into a shared witness pool containing six entries. Four witnesses genuinely belong to the presented cases, while two are adversarial statements selected from highly compatible worlds. They may use the same colors, shapes, block names, and directional language as the real evidence without fitting any case completely. A separate verdict pool contains eight possible conclusions. Four are correct and four are deliberately plausible alternatives. The unused verdicts include neighboring objects, inverse relations, alternate blocks, constituent choices, and open-world outcomes that resemble the expected answer form. The challenge is not solved by locating one relevant sentence. A successful system must determine which witness completes each narrative, reason over the completed world, select the correct verdict, and preserve a globally valid assignment across the entire board. A locally attractive decision may become impossible when another case requires the same witness or verdict. Every slot identifier is local to one board. W03 and V06 have no stable meaning across samples. Memorizing slot frequencies or treating the codes as semantic labels does not provide a dependable shortcut. Challenge Objective For every board, predict two values for each of its four cases: The correct witness slot from W01 through W06. The correct verdict slot from V01 through V08. The four selected witnesses must be distinct. Two witness entries remain unused. The four selected verdicts must also be distinct. Four verdict entries remain unused. A complete solution must: Identify objects, attributes, and block membership. Track directional, containment, contact, and distance relations. Resolve references such as “this shape,” “the second square,” and “the object below the triangle.” Distinguish explicit facts from implied, contradicted, and unknown relations. Compare all four cases against the shared candidate pools. Reject evidence that is lexically similar but structurally incompatible. Produce a board-level assignment without duplicate routes. Arbitration Board Each case contains a spatial narrative, one withheld position, and a question with its original alternatives. Block A contains a medium yellow square and a small blue circle. The circle is below the square. [WITHHELD WITNESS] Which object is to the right of the small blue circle? Each board also provides: Six witness entries: W01 through W06. Eight verdict entries: V01 through V08. Four real witnesses and two adversarial witnesses. Four correct verdicts and four adversarial verdicts. Slot order is independently shuffled for every board. Abbreviated Example Case 1: Block A contains a large black square and a small blue circle. [WITHHELD WITNESS] Which object is above the small blue circle? Case 2: A yellow triangle and a black square are inside block C. The black square is below the yellow triangle. [WITHHELD WITNESS] Which shape touches the right edge of block C? Candidate witnesses: W01: The yellow triangle touches the right edge of block C. W02: The medium square is to the left of the black circle. W03: The large black square is above the small blue circle. W04: Block B is below block A. W05: A small triangle is inside block B. W06: The blue circle is near the yellow square. Candidate verdicts: V01: the small blue circle V02: the yellow triangle V03: the large black square V04: block A V05: the black square V06: neither object V07: block C V08: the medium square For the displayed cases: Case 1 uses witness W03 and verdict V03. Case 2 uses witness W01 and verdict V02. Actual boards always contain four cases. The remaining assignments must be solved at the same time. Dataset Scale The prepared release contains: 1,000 training boards. 236 test boards. 1,236 boards in total. 4,000 labeled training board-case instances. 944 test board-case instances. 4,944 board-case instances in total. Four cases per board. Six witness candidates per board. Eight verdict candidates per board. 14 candidate entries per board. 56 possible case-to-candidate pairings before global constraints are applied. Eight final route labels per board. The training partition provides 8,000 supervised route labels: one witness assignment and one verdict assignment for each of its 4,000 board-case instances. The test partition evaluates 1,888 hidden route labels across 944 board-case instances. A board, rather than an isolated case, is the fundamental learning and evaluation unit. Each training row represents one constrained joint assignment over four cases, six witnesses, and eight verdicts. The prepared training partition therefore contains 1,000 supervised joint-assignment examples. The release uses two deterministic arbitration layouts for every eligible four-case source group. The layouts preserve the underlying spatial problems while changing case positions, adversarial candidate selection, witness-slot ordering, verdict-slot ordering, and the resulting route labels. The training partition contains 500 source groups expanded into 1,000 arbitration boards. The test partition contains 118 source groups expanded into 236 arbitration boards. The split is performed at the spatial-world level before board-layout generation. Questions derived from the same narrative remain in one partition even when they ask about different entities or use different descriptions. Both layouts derived from a source group remain in the same partition, preventing alternate questions or augmented layouts from leaking across training and test data. The test-to-train board ratio is 23.6%. The test partition represents approximately 19.1% of all prepared boards. Dataset Files The challenge release contains: train.csv test.csv sample_submission.csv Training Data Identification: sample_id is the unique board identifier. Incomplete cases: case_1 case_2 case_3 case_4 Witness pool: witness_W01 witness_W02 witness_W03 witness_W04 witness_W05 witness_W06 Verdict pool: verdict_V01 verdict_V02 verdict_V03 verdict_V04 verdict_V05 verdict_V06 verdict_V07 verdict_V08 Training labels: case_1_witness case_1_verdict case_2_witness case_2_verdict case_3_witness case_3_verdict case_4_witness case_4_verdict Valid witness labels are W01 through W06. Valid verdict labels are V01 through V08. Within every row: Each case contains exactly one [WITHHELD WITNESS] marker. The four correct witness labels are distinct. Exactly two witness slots are unused. The four correct verdict labels are distinct. Exactly four verdict slots are unused. Candidate numbering is independently randomized. Test Data test.csv contains the same board features without the eight routing labels. Each test row provides: One board identifier. Four incomplete spatial cases. Six candidate witnesses. Eight candidate verdicts. Participants submit the missing witness and final verdict for every case. Submission Format Submissions must contain exactly nine columns: sample_id,case_1_witness,case_1_verdict,case_2_witness,case_2_verdict,case_3_witness,case_3_verdict,case_4_witness,case_4_verdict Example: sample_id,case_1_witness,case_1_verdict,case_2_witness,case_2_verdict,case_3_witness,case_3_verdict,case_4_witness,case_4_verdict SWA-000001,W03,V06,W01,V02,W05,V08,W04,V04 SWA-000002,W02,V01,W06,V07,W01,V05,W03,V08 Submission requirements: Every test sample_id must appear exactly once. Witness predictions must use W01 through W06. Verdict predictions must use V01 through V08. A witness slot cannot be assigned to multiple cases on the same board. A verdict slot cannot be assigned to multiple cases on the same board. Column names and column order must match sample_submission.csv. Additional columns are not accepted. Blank values are not accepted. Missing, duplicate, or unexpected identifiers are not accepted. Malformed submissions raise an explicit grading error. Evaluation The score combines witness selection, verdict selection, coupled case resolution, and complete-board consistency. Let W be witness accuracy across all cases: W = correct witness assignments / total cases Let V be verdict accuracy across all cases: V = correct verdict assignments / total cases Let C be coupled case accuracy. A case receives coupled credit only when both its witness and verdict are correct: C = cases with both assignments correct / total cases Let B be complete-board accuracy. A board is complete only when all eight predictions are correct: B = completely correct boards / total boards The balanced routing term is: Routing = sqrt(W × V) The arbitration coherence term is: Coherence = 0.70 × C + 0.30 × B The final leaderboard score is: Score = 100 × Routing^0.55 × Coherence^0.45 Scores are clipped to [0.01, 100]. A perfect submission receives exactly 100.0. The geometric routing term prevents strong verdict selection from hiding weak witness selection, or the reverse. Coupled accuracy rewards systems that use the correct witness to reach the correct conclusion. Complete-board accuracy separates globally coherent systems from pipelines that repeatedly leave one case unresolved. All components use exact hidden labels. Evaluation uses no generative model, semantic judge, external API, or subjective assessment. Spatial Language Cases may involve: Left and right. Above and below. Near and far. Inside and containment. Touching and boundary contact. Connection and disconnection. Relations between blocks. Relations between objects in the same block. Relations inherited through block placement. Objects may be distinguished by: Color. Shape. Size. Block membership. Ordinal numbering. Boundary contact. Relations to other objects. Descriptions may refer to objects through phrases such as: The square below the yellow object. The circle touching the edge of a block. The second medium black shape. The object inside the block above block C. The shape to the left of the triangle. A system must preserve these distinctions throughout the case. Treating objects with similar surface descriptions as interchangeable produces incorrect routes. Open-World Arbitration The narratives distinguish among: Explicit facts. Facts implied by inverse relations. Facts implied by valid spatial chains. Facts contradicted by the narrative. Relations that are not established. Missing information is not automatically false. Some verdicts represent uncertainty rather than contradiction, so binary positive-versus-negative reasoning is insufficient. Witness Difficulty A correct witness must agree with: The entities already introduced. Their attributes and numbering. Their block membership. The grammatical position of the withheld sentence. Existing spatial relations. The question being asked. The resulting verdict. Assignments required by the other cases. The two unused witnesses are selected to remain locally tempting. They can: Use the correct relation with the wrong entities. Reverse the relevant direction. Match the shape but not its color or size. Refer to the correct object in the wrong block. Introduce a contradiction. Support an attractive but incorrect verdict. Compete with a real witness for the same case. Verdict Difficulty The four unused verdicts are selected to resemble correct conclusions in form and vocabulary. Verdict traps include: The unselected alternative explicitly written in the question. One constituent answer when the correct conclusion is both of them. The inverse spatial relation. A neighboring object. The correct shape with the wrong size or color. An object from another block. A truth state that confuses contradiction with uncertainty. An answer associated with another case on the board. This design makes the verdict pool materially harder than random corpus negatives. In multi-target records, both of them is treated as the aggregate conclusion while its constituent alternatives become high-priority traps. Split Integrity The challenge uses world-grouped splitting before board construction rather than row-level random splitting. All questions sharing the same normalized spatial narrative remain in one partition. No spatial world appears in both training and test data. Both arbitration layouts derived from a source group remain in the same partition. Board identifiers are unique and newly generated for each layout. Case positions are deterministically permuted between layouts. Witness and verdict candidate slots are independently reshuffled. Variant-aware decoy selection changes the adversarial candidate configuration where compatible alternatives are available. Original source ordering is not exposed. Training and test board identifiers do not overlap. Training and test source-story keys do not overlap. A source case may appear in two deterministic arbitration layouts within its assigned partition. These layouts are not treated as separate source annotations. They are permutation-aware board constructions that expose different joint-assignment configurations while preserving the original spatial reasoning target. The 1,000-board training set provides 1,000 supervised joint-assignment examples. Its 4,000 case positions are board-case instances rather than 4,000 independent spatial worlds. The separate 236-board evaluation set contains 944 hidden board-case instances. Baseline Approaches A practical neural baseline can use a frozen sentence-transformer or embedding model without fine-tuning: Encode the four incomplete cases and six witness candidates in batches on the A10G. Construct a neural 4 × 6 witness-compatibility matrix from semantic similarity and query-aware representations. Use maximum-weight bipartite matching to choose four distinct witnesses. Insert each selected witness into its case at [WITHHELD WITNESS]. Encode every completed case against all eight verdict candidates. Construct a second 4 × 8 compatibility matrix. Apply constrained assignment so the four selected verdict slots are distinct. This produces a genuine pretrained-ML baseline while preserving the board-level constraints. It should outperform shallow word matching, but it will still fail when a decoy is semantically close while reversing direction, switching containers, or changing the referent of a relational question. A stronger baseline can add a frozen cross-encoder reranker: Use the bi-encoder to shortlist witness and verdict routes. Score complete (case, witness) and (restored case, verdict) pairs with a pretrained cross-encoder. Calibrate witness and verdict scores on the 502 labeled training boards. Search several high-scoring witness permutations instead of committing greedily. Rerank joint witness-verdict configurations under the uniqueness constraints. Add a lightweight spatial consistency verifier for inverse, transitive, containment, and negation conflicts. The model weights remain frozen; training data is used for prompt selection, score calibration, thresholding, and validation rather than parameter fine-tuning. Stronger Approaches Competitive systems may combine: Frozen sentence-transformer retrieval. Zero-shot or few-shot cross-encoder reranking. Quantized 7B–14B instruction-model inference. Whole-board prompting that exposes all four cases and both shared banks together. Multi-prompt ensembling or self-consistency within the runtime budget. Spatial entity extraction. Relation normalization. Scene-graph induction. Constraint propagation. Hungarian matching. Integer programming. Candidate elimination. Board-level verification. Ensembles of neural, semantic, and symbolic compatibility scores. One effective inference pipeline can: Extract entities, attributes, and relations from every case. Represent each incomplete case as a provisional spatial graph. Insert every witness candidate into every case. Measure contradictions and unresolved references. Score all 24 case-to-witness combinations. Select four distinct witnesses under a global assignment constraint. Complete the four spatial worlds. Score all 32 case-to-verdict combinations. Select four distinct verdicts. Verify every selected witness-verdict pair. Export the nine required columns. Runtime and Resources The competition environment provides: One NVIDIA A10G GPU. A maximum end-to-end runtime of 1.5 hours. No requirement to train or fine-tune a model. The intended workload is batched inference with frozen pretrained models. Participants may use sentence transformers, cross-encoders, quantized instruction models, neural rerankers, or hybrid neural-symbolic systems, provided the complete submission is produced within the 1.5-hour limit. The intended computational profile includes: Batched neural embedding of cases, witnesses, and verdicts. 4 × 6 witness compatibility scoring for each board. 4 × 8 verdict compatibility scoring for each board. Cross-encoder or instruction-model verification of ambiguous routes. Small spatial-graph consistency checks. Hungarian matching, beam search, or constrained joint decoding over each board. The test partition contains 236 boards and 944 board-case instances. Evaluating all 56 direct case-to-candidate pairings per board produces 13,216 initial pairings, leaving enough of the runtime budget for neural reranking, permutation search, and verification passes. Strong submissions should use pretrained semantic representations or local language-model reasoning as the primary compatibility signal, then enforce the challenge's discrete global constraints during decoding.
> $700 Pool
> 1 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## GrantSwap: Reciprocal Funder Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7b795arcddwxwfs2ytqvqjm18e323p
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat lock's score of 0.742!

Full challenge description from page:

> GrantSwap: Reciprocal Funder Repair Overview Each example contains two works from the same venue and publication year. A single funder from each work was swapped into the other work's observed portfolio. Recover which observed funder is foreign to each work. Titles, venue context, publisher, year, the two observed portfolios, and an opaque public funder catalog are available. The split holds out complete venue groups. A system must use the supplied metadata to infer the reciprocal correction and should not depend on memorizing a venue's usual funding pattern. Evaluation For each test pair (i), let (b_i) and (c_i) be the submitted base and contrast removals, and (b_i^,c_i^) the hidden removals. Let (G) be the set of venue groups. The score is the macro average of exact joint recovery by venue: $$ \mathrm{Score}=\frac{1}{|G|}\sum_{g\in G}\frac{1}{|I_g|}\sum_{i\in I_g}\mathbf{1}[b_i=b_i^\land c_i=c_i^]. $$ The score is in ([0,1]) and is maximized. Macro-averaging by venue gives a large venue the same influence as a small venue, measuring transfer across independent publication contexts instead of rewarding performance concentrated in venues with many pairs. Each submitted removal should be a funder present only on that side's observed portfolio (the side-exclusive candidates). A malformed or impossible prediction receives zero for that row; it does not invalidate the other rows. Rows within a venue group have equal weight, and venue groups have equal weight. Structural submission errors such as missing test IDs, duplicate IDs, wrong row count, or wrong columns are rejected. The split assigns every normalized venue to exactly one partition before pairs are formed. Holding out complete venues prevents memorizing venue-specific funder priors or recurring publisher patterns. Opaque funder IDs do not by themselves guarantee independence because an ID may occur across venues; the venue holdout addresses that shared-entity leakage by requiring pair-specific evidence on unseen venues. This is a transfer test across contexts, not a claim that opaque IDs alone prevent leakage. Dataset The prepared public directory contains: train.csv: 1,031 training pairs containing features only. train_targets.csv: 1,031 labels keyed by example_id. test.csv: 325 unlabelled test pairs. funder_catalog.csv: 11,906 rows mapping opaque funder IDs to deposited names and key type. sample_submission.csv: a valid-schema example with 325 rows. The test file contains inputs only; it has no removal, insertion, repaired-portfolio, or hidden-answer columns. The two signal columns are the observed inputs from which the removal decision must be inferred. example_id (string): opaque pair identifier. container_title (string): shared deposited venue text. publisher (string): base-work publisher text. publication_year (integer): shared publication year. base_title (string): base-work title. contrast_title (string): contrast-work title. base_signal (JSON string array): opaque signal values supplied for the base work; these are inputs, not evaluation targets. They encode the observed deposited records used to infer the repair. contrast_signal (JSON string array): opaque signal values supplied for the contrast work; these are inputs, not evaluation targets. They encode the observed deposited records used to infer the repair. train_targets.csv contains example_id plus base_remove_funder_id (string), base_insert_funder_id (string), contrast_remove_funder_id (string), and contrast_insert_funder_id (string), the two swapped IDs and their reciprocal restorations; base_repaired_funder_ids and contrast_repaired_funder_ids (JSON string arrays), the complete uncorrupted portfolios. Join labels to features by example_id. funder_catalog.csv contains funder_id (string), funder_name (string), and source_key_type (string, exactly doi or name). Submission example_id (string): each test ID exactly once. base_remove_funder_id (string): one side-exclusive ID to remove from the base portfolio. contrast_remove_funder_id (string): one side-exclusive ID to remove from the contrast portfolio. The submitted CSV must contain exactly 325 data rows and this header: example_id,base_remove_funder_id,contrast_remove_funder_id GS_004A39A382A6C160,GF_2CCC48D86C227FC4,GF_37BF3BB4E50813DD GS_00A1B2C3D4E5F607,GF_1111111111111111,GF_2222222222222222 Every ID must match GF_ followed by 16 uppercase hexadecimal characters. No missing, duplicate, unknown, or non-finite values are allowed. What not to use Do not query search engines, funder registries, or any other external service during inference. Do not read private/, evaluator answers, hidden files, or grader implementation details to obtain test labels. Do not manually annotate test rows or hard-code test predictions. Do not repeatedly submit variants only to probe the grader for hidden answers. Models and indexes built only from the supplied public files are allowed. Normal local preprocessing, text modeling, and deterministic candidate-ranking code are allowed. &nbsp;
> $700 Pool
> Closes in 2h 11m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Evidence-Cut Adjudication Lattice Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78wanchsy0c8mb577fnm0jt18dvngm
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat lock's score of 55.175!

Full challenge description from page:

> Overview Evidence-Cut Adjudication Lattice Reconstruction is a structured factuality challenge built around competing responses, missing source regions, repair alignment, and latent annotation trajectories. Each board contains four factuality cases. Every case shows one question, two competing responses, reference documents with two removed regions, eight claim candidates, ten repair candidates, and ten trajectory candidates. The eight removed source regions from the four cases are shuffled into one shared evidence bank. For every case, predict the complete route: response → claim → decisive evidence → repair → trajectory The task is not ordinary factuality classification. The model must determine which response was actually adjudicated, which proposition inside that response was targeted, which removed source region supplied the decisive evidence, which repair applies, and which three-state trajectory explains the cut, restored, and repaired worlds. The four decisive evidence predictions on a board must use four distinct entries from the shared bank, so evidence routing is globally coupled. Core Construction Each case contains two [REFERENCE REGION REMOVED] markers. Both missing regions are genuine text removed from that case's visible documents, and both appear somewhere in the board-level evidence bank. One is the decisive annotation basis. The other is a nuisance region: relevant source material from the same case that does not define the target adjudication route. This means identifying where an evidence fragment belongs is not enough. A model must distinguish source ownership from adjudicative relevance. The two responses are labeled R1 and R2. One contains the annotated proposition. The other is a companion response to the same question and may contain similar entities, dates, quantities, predicates, or an alternate factual account. No field tells participants which response is the annotation-bearing response. Prediction Targets For each case i, submit five categorical predictions: case_i_response: R1 or R2; case_i_claim: H01 through H08; case_i_evidence: E01 through E08; case_i_repair: C01 through C10; case_i_trajectory: T01 through T10. Response, claim, repair, and trajectory namespaces are case-local and may repeat across cases. Evidence is board-global. The four submitted evidence codes must be distinct. A conceptual route such as R2 → H05 → E03 → C08 → T04 means that R2 contains the annotated proposition, H05 identifies that proposition, E03 is the decisive removed evidence, C08 is the applicable repair, and T04 is the complete adjudication trajectory. Participants submit only categorical codes. No free-form evidence, corrections, or explanations are required. Case Contents Each case_i field contains a JSON object with: language; question; documents; responses; claim_candidates; trajectory_candidates. responses contains exactly R1 and R2. claim_candidates contains exactly H01 through H08. trajectory_candidates contains exactly T01 through T10. Across a case's documents there are exactly two [REFERENCE REGION REMOVED] markers. The public payload does not expose source-topic IDs, annotation IDs, hidden response provenance, source record IDs, model identities, or preparation metadata. Claim Candidates Exactly one claim candidate identifies the proposition addressed by the hidden annotation. Hard alternatives may include: overlapping shorter or longer spans; neighboring propositions from the same response; propositions from the companion response; source sentences with similar entities or predicates; claims with the same answer type but a different factual relation. Several candidates may be valid spans of R1 or R2. Claim selection and response selection are therefore coupled. Shared Evidence Bank The board-level evidence bank contains exactly eight entries, E01 through E08. Every entry is a real region removed from one of the four displayed cases. Each case contributes two entries: one decisive region; one nuisance region. Exactly four entries are decisive targets, one per case, and those four target codes are distinct. The nuisance regions are not unrelated random negatives. They come from the same cases and can share entities, dates, quantities, answer types, or factual relations with the target claim. There are 8P4 = 1,680 legal four-case evidence assignments before the other route choices are considered. Exact constrained decoding is therefore inexpensive once candidate scores are available. Repair Banks repair_bank is a board-level JSON object with one local bank for each case. Every local bank contains C01 through C10. Repair codes have no meaning across cases. C03 in case 1 and C03 in case 4 may contain completely different repairs and may both be correct. Repairs may be textual corrections or explicit actions such as deletion, qualification, no factual replacement, or marking content as outside the question. Hard negatives are designed to be locally plausible. A correct date replacement may compete with other date replacements; a numerical correction may compete with similar quantities; and a deletion or qualification may face other action-compatible alternatives. The correct repair must align with the selected response, claim, and decisive evidence. Trajectory Reconstruction Every trajectory card contains three states: K0: the evidence-cut world; K1: the restored adjudication state; K2: the state after repair. Cards also contain: restoration_transition; repair_transition; evidence_relation; repair_action. The stable states are: SUPPORTED; CONTRADICTED; UNVERIFIABLE; NO_FACT; OFF_QUESTION; MIXED; EVIDENCE_DETACHED; REPAIR_UNCERTIFIED. Evidence relations are SUPPORT, COUNTEREVIDENCE, INSUFFICIENT, NONE, IRRELEVANT, and MIXED. Repair actions are REPLACE, QUALIFY, DELETE, NO_CHANGE, NO_REPLACEMENT, and MARK_OUTSIDE_QUESTION. A trajectory such as K0=EVIDENCE_DETACHED, K1=CONTRADICTED, K2=SUPPORTED, evidence_relation=COUNTEREVIDENCE, repair_action=REPLACE describes a contradicted claim whose decisive evidence was removed and whose repair produces a supported final state. Several trajectory candidates can share the same final K2 state. Final-state classification is therefore insufficient. Trajectory banks are constructed to avoid simple field-frequency recovery. The correct card is not identifiable by taking a unique modal value for its fields across the candidate bank. Why the Five Routes Are Coupled A locally plausible prediction can still form an impossible chain. For example: the selected claim may belong to R1 while the chosen repair modifies a proposition found only in R2; the selected evidence may genuinely belong to the case but be the nuisance cut rather than the decisive cut; the evidence may contradict the claim while the selected trajectory describes a supporting relation; two cases may independently prefer the same evidence code even though a valid board requires distinct decisive routes. Competitive systems should therefore score complete routes or retain multiple hypotheses until board-level decoding. Multilingual and Context Regime Cases may contain English or Chinese material, and a board may be monolingual or multilingual. The language code is public. Text remains in its source language. Long documents are deterministically windowed while preserving both removed-region markers. The task is not open-web retrieval, but participants should expect enough context that naive full cross-encoding of every candidate combination can be expensive. Released Files The public package contains: train.csv; test.csv; sample_submission.csv; The release contains exactly: 1,000 training boards, representing 4,000 cases; 250 test boards, representing 1,000 cases. train.csv Feature columns are: sample_id; difficulty; case_1; case_2; case_3; case_4; evidence_bank; repair_bank. Training additionally contains twenty targets: five labels for each of the four cases. For case 1 they are case_1_response, case_1_claim, case_1_evidence, case_1_repair, and case_1_trajectory, with the same pattern repeated for cases 2 through 4. The four evidence labels in every training row are distinct. test.csv Test rows contain the same public feature columns as training but omit all target columns. The test set does not expose the annotation-bearing response, target claim, decisive evidence, applicable repair, trajectory card, or hidden source grouping. Submission Format Use sample_submission.csv exactly. The submission contains sample_id plus five predictions for each of four cases, for 21 columns total. The required order is: sample_id, case_1_response, case_1_claim, case_1_evidence, case_1_repair, case_1_trajectory, case_2_response, case_2_claim, case_2_evidence, case_2_repair, case_2_trajectory, case_3_response, case_3_claim, case_3_evidence, case_3_repair, case_3_trajectory, case_4_response, case_4_claim, case_4_evidence, case_4_repair, case_4_trajectory For every row: response codes must be R1 or R2; claim codes must be H01 through H08; evidence codes must be E01 through E08; the four evidence codes must be distinct; repair codes must be C01 through C10; trajectory codes must be T01 through T10. Every expected sample_id must appear exactly once. Missing rows, extra rows, duplicate IDs, invalid codes, repeated evidence routes, missing values, extra columns, or incorrect column order produce a grading error. Evaluation The metric rewards complete adjudication reconstruction rather than disconnected marginal predictions. Five exact component accuracies are calculated across all cases: P: response accuracy; H: claim accuracy; E: evidence accuracy; C: repair accuracy; T: trajectory accuracy. Define marginal reconstruction as: R = (P × H × E × C × T)^(1/5) Define J as coupled case accuracy. A case counts toward J only when all five predictions for that case are correct. Define B as complete-board accuracy. A board counts toward B only when all four cases, meaning all twenty route predictions, are correct. The final score is: Score = 100 × R^0.35 × J^0.50 × (0.90 + 0.10 × B) The result is clipped to [0.01, 100]. A perfect submission receives exactly 100.0. The geometric term prevents one easy component from compensating for a failed component, while the large coupled-case term makes complete five-link reconstruction the central objective. The provided grader reproduces the metric directly. There are no hidden semantic judges, hidden metric subsets, or generated-text similarity checks. Split Integrity The official train/test split is group-disjoint over hidden source families. Connected questions, documents, responses, annotations, and derived candidates stay entirely within one partition. Exact normalized duplicate questions and documents are grouped before partition assignment. Hidden grouping identifiers are not participant-facing. For local validation, keep all derivatives of a board together, including pair expansions, cached embeddings, auxiliary labels, and candidate-scoring records. Difficulty difficulty uses descriptive bands D1 through D4. The band summarizes factors such as context length, response ambiguity, similarity between decisive and nuisance evidence, monolingual evidence competition, and trajectory ambiguity. It is not a prediction target. Compute and Model Policy The execution environment provides one NVIDIA A10G GPU and a 90-minute end-to-end runtime limit. The A10G is part of the intended challenge regime, not an optional convenience. Eligible submissions must use a learned neural text model on the GPU as an integral part of the final semantic predictor. The model may be pretrained, fine-tuned on the released training data, adapter-tuned, partially frozen, or used as a learned scorer, but neural scores produced with the GPU must directly influence the submitted response, claim, evidence, repair, or trajectory routes. A CPU-only end-to-end solution is not eligible. CPU computation remains allowed for data loading, tokenization, caching, lightweight preprocessing, bookkeeping, candidate enumeration, validity checks, and exact structured decoding after neural scoring. Public pretrained models are allowed, including multilingual or language-specific encoders, cross-encoders, long-context models, NLI models, neural graph models, compact sequence models, and eligible neural ensembles. Useful strategies include mixed precision, parameter-efficient fine-tuning, cached neural representations, batched candidate scoring, candidate pruning, and exact board-level assignment. The 90-minute limit covers data loading, feature construction, any training or adaptation performed during the run, inference, structured decoding, and submission writing. Learned-Model Requirement The semantic decisions submitted to the grader must be materially produced by learned neural modeling. Classical or deterministic methods may support the pipeline, but they may not serve as the primary predictor or independently determine the final route. The following are not eligible as integral final-answer systems: TF-IDF, BM25, bag-of-words, or character-frequency retrieval used as the decisive semantic scorer; rule-based or regular-expression systems that determine response, claim, evidence, repair, or trajectory labels; hand-authored factuality, repair, trajectory, or routing heuristics used as the primary decision mechanism; classical statistical ML used as the decisive predictor, including logistic regression, naive Bayes, linear or kernel SVMs, nearest-neighbor classifiers, random forests, gradient-boosted trees, or similar non-neural models; combinations of the above that effectively reproduce a CPU-only final predictor. These methods may still be used for diagnostics, indexing, inexpensive candidate pruning, auxiliary features, or tie-breaking provided that a GPU-executed neural model remains materially responsible for the semantic scores used in the final prediction. Grammar and permutation constraints are also allowed when they only enforce valid output structure. Disallowed Resources Participants may not use: hidden test targets or private evaluator files; manual or online human annotation of test cases; external answer-key lookup keyed to challenge samples;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Governance Proposal Review-Queue Ranking

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74a0jqqaperf9ghtkz7xs9gs8e4gqj
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat bunnys's score of 0.661!

Full challenge description from page:

> Governance Proposal Review-Queue Ranking Overview Governance moderators need to decide which proposals deserve extra discussion before a vote closes. This challenge asks you to produce a continuous review-priority score for authentic proposals using only proposal-time text and metadata. The hidden relevance target is a practical review trigger: a proposal is relevant when opposing voting power is at least 20% of its decisive yes-plus-no voting power. Abstentions and platform-specific non-binary choices are not counted in that fraction. The threshold is an operational early-warning rule for queue ordering, not a claim that every dissenting proposal should be rejected. The test set is a chronological future holdout within each platform, so it measures forward generalisation rather than random memorisation. The evaluator gives each platform equal weight and gives more influence to proposals with unusually high participation within their own platform, so a useful system must rank difficult cases within each ecosystem rather than learn only that one platform is more contentious than another. Dataset File descriptions train.csv -- 10,987 feature-only training rows. It contains proposal-time inputs and no vote outcome column. train_targets.csv -- Public relevance targets keyed by id. It has exactly the same unique, non-null ID set as train.csv, exactly one row per training feature row, and no test IDs. test.csv -- 2,748 feature-only future-holdout rows. It has the same feature columns and order as train.csv. sample_submission.csv -- Random finite ranking scores with the required id,prediction schema. Column descriptions id (string) -- Deterministic 16-character hexadecimal identifier. It is required in the submission but must not be used as a lookup key. platform (string) -- Source governance system: snapshot, sns, or polkadot. category (string) -- Proposal-time source category, combining the source space, SNS topic/action, or Polkadot call section/topic. created_at (string) -- Proposal creation or voting-start timestamp in UTC ISO-8601 form. title (string) -- Proposal title after deterministic removal of URLs, account-like identifiers, numbers, and image payloads. body (string) -- Proposal summary/content after the same deterministic text cleanup. [LINK], [ACCOUNT], [IDENTIFIER], [NUMBER], and [IMAGE] are intentional tokens. text_chars (integer) -- Character count of the cleaned title and body combined. title_chars (integer) -- Character count of the cleaned title. section_count (integer) -- Markdown heading count in the cleaned body. link_count (integer) -- Count of raw URL matches plus Markdown link matches in the source body before cleanup; it is a structural signal, not a vote field. number_token_count (integer) -- Count of numeric tokens in the raw body before number replacement. choice_count (integer) -- Number of choices in the source proposal record. train_targets.csv contains id and target, where target=1 means the hidden dissent fraction is at least 0.20 and target=0 otherwise. It is a public training sidecar because train and test must expose identical model-feature columns; it does not contain evaluator influence weights. The preparation contract guarantees set(train_targets.id) == set(train.id), unique and non-null IDs in both files, equal row counts, and set(train_targets.id).isdisjoint(set(test.id)). Load both files and join on id with a one-to-one validation; silently dropping unmatched training rows is invalid. Evaluation Submissions are scored with Platform-Balanced Influence-Weighted Average Precision (PIW-AP). Higher is better, and the score is in [0, 1]. For each test row, the hidden source tally defines target = 1[dissent_fraction >= 0.20], where dissent_fraction = no / (yes + no). Let M = yes + no and let median_M(platform) be the median decisive voting power for that platform over all eligible source records. The hidden influence weight is w = clip(1 + log(1 + M / median_M(platform)), 1, 4). The final score is the arithmetic mean of weighted average precision computed separately for snapshot, sns, and polkadot; each platform therefore contributes one third of the score. import numpy as np import pandas as pd from sklearn.metrics import average_precision_score PLATFORM_ORDER = ("polkadot", "snapshot", "sns") PLATFORM_STRIDE = 10_000_000_000_000 LABEL_STRIDE = 5_000_000_000_000 WEIGHT_SCALE = 1_000_000_000_000 def _payload(value): code = float(value) if not np.isfinite(code) or code != np.floor(code): raise Exception("Private answer payloads must be finite integer codes.") platform_index, remainder = divmod(int(code), PLATFORM_STRIDE) label, weight_code = divmod(remainder, LABEL_STRIDE) if not 0 float: if list(submission.columns) != ["id", "prediction"]: raise Exception("Submission columns must be exactly id,prediction in that order.") if list(answers.columns) not in (["id", "prediction"], ["id", "prediction", "visibility"]): raise Exception("Answer columns are invalid.") if len(submission) != len(answers): raise Exception("Submission and answers must contain the same number of rows.") if submission["id"].isna().any() or submission["id"].duplicated().any(): raise Exception("Submission IDs must be non-null and unique.") if answers["id"].isna().any() or answers["id"].duplicated().any(): raise Exception("Answer IDs must be non-null and unique.") if "visibility" in answers.columns and not answers["visibility"].astype(str).str.lower().isin({"public", "private"}).all(): raise Exception("Answer visibility must be public or private.") submitted = submission.sort_values("id").reset_index(drop=True) expected = answers.sort_values("id").reset_index(drop=True) if submitted["id"].astype(str).tolist() != expected["id"].astype(str).tolist(): raise Exception("Submission IDs must match test IDs exactly.") try: raw_priority = submitted["prediction"].astype(float).to_numpy() except (TypeError, ValueError) as exc: raise Exception("Predictions must be finite ranking scores in [0, 1].") from exc if not np.isfinite(raw_priority).all(): raise Exception("Predictions must be finite ranking scores in [0, 1].") if ((raw_priority 1)).any(): raise Exception("Predictions must be finite ranking scores in [0, 1].") priority = raw_priority decoded = [_payload(value) for value in expected["prediction"]] labels = np.asarray([row[0] for row in decoded], dtype=int) platforms = np.asarray([row[1] for row in decoded]) weights = np.asarray([row[2] for row in decoded], dtype=float) scores = [] for platform in ("polkadot", "snapshot", "sns"): mask = platforms == platform if mask.sum() < 2 or labels[mask].sum() == 0: raise Exception("Every platform partition must contain a positive example.") scores.append(average_precision_score(labels[mask], priority[mask], sample_weight=weights[mask])) return float(np.mean(scores)) The evaluator rejects missing, duplicated, unknown, or mismatched IDs; NaN, infinite, or out-of-range ranking scores; and malformed private numeric payloads. The [0, 1] bound is a strict submission-format and validation requirement, not a request for calibrated probabilities. After that check, PIW-AP evaluates relative ordering within each platform; a strictly monotone rescaling has the same ranking effect only when every rescaled value remains in [0, 1]. Ties are accepted but receive average-precision tie handling and provide no ordering advantage. The private answer file stores its hidden label, platform, and influence weight in one packed integer prediction value and may carry an additional evaluator-only visibility column with values public or private; neither is part of a solver submission. Submission Submit one normalized review-priority score for every row in test.csv. id (string) -- Exact identifier from test.csv. prediction (float) -- Continuous ranking score used to order proposals by likelihood of reaching the 20% dissent review trigger. It must be finite and in [0, 1]; this bound is a hard format rule, while the metric rewards its relative ordering within each platform rather than probability calibration. Example using real test IDs: id,prediction 7e44259e94b87e6f,0.73 c0e2678b77a6d03d,0.41 5e9fc7c066081e07,0.18 Requirements The file must contain exactly 2,748 data rows, one for every test ID. Columns must be exactly id,prediction in that order. IDs must be unique and must match test.csv exactly. Every prediction must be a finite numeric ranking score in [0, 1]. Use UTF-8 CSV with no index column and no extra columns. Train only on the public training files. The answer-side tally, influence weight, and post-vote status are not public features. Allowed Methods Train text-ranking, retrieval, or neural language models using the public training data. Use platform, category, timestamps, cleaned text, and the supplied structural counts as proposal-time inputs. Use standard GPU-compatible NLP libraries or a pretrained text encoder when its weights are available in the execution environment and no external answer lookup is performed. Select model settings with a public-only chronological validation scheme. What Not To Use Platform is a valid proposal-time context feature. A solver may condition its model on platform, fit separate platform calibrations, stratify validation by platform, or use platform interactions with the title, body, category, timestamp, and structural counts. A platform-only constant baseline is format-valid, but it ties every proposal within that platform and therefore provides no within-platform ordering advantage; useful models distinguish proposals using their available proposal-time evidence. Do not use source proposal IDs, author/proposer identifiers, raw wallet or account identifiers, raw vote totals, or post-vote fields as features; the cleaned files intentionally remove or hash these fields. Do not add synthetic proposals, model-generated labels, cached test answers, or an externally downloaded labeled governance corpus. Do not hardcode predictions by id, row order, source category, or a manually curated list of proposals. &nbsp;
> $700 Pool
> Closes in 6h 38m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Same-Book Future Triplet Order

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7eyr45x8ssfrewce9ykm4hn98bm7ha
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat avinash_reddy's score of 0.532!

Full challenge description from page:

> Same-Book Future Triplet Order Overview Each item gives one English literary anchor passage and three candidate passages cand_0, cand_1, cand_2. All four passages always come from the same source book. Every candidate occurs later in the book than the anchor. The three candidates are shown in a random presentation order. Your job is to recover the candidates' true chronological order in the book. Output order as a permutation of presentation indices 0,1,2 listed from earliest to latest. Example: 2,0,1 means cand_2 is earliest among the three, then cand_0, then cand_1. This is same-book future-passage ordering for GPU pairwise / listwise rankers. It is not 4-way intruder detection (no odd-one-out), not pick-one successor multiple choice, not sentence unshuffling inside one passage, not quotation-span recovery, not punctuation restoration, not reporting-verb choice, not gap regression, and not time-to-event ranking. Labeled items are in train.csv. Unlabeled items are in test.csv. Use only files under ./dataset/public/. Why this is hard: all three candidates are true later passages from the same book, so book/author identity and "does this belong?" cues do not help. Candidates are length-matched and separated in index space. Items are built from non-overlapping source-index intervals (the whole span from anchor through the latest candidate is consumed), and cross-row near-duplicate passages with high five-gram containment are removed, so neither exact reuse nor overlapping-interval / near-copy chains can reveal order. Test items use many held-out source books with book- and label-aware sampling for stable evaluation. Chance accuracy among the six permutations is 1/6. Strong solutions typically need dense encoders or cross-encoders (GPU recommended). Output rules order must be a permutation string of 0,1,2 with commas and no spaces, such as 0,1,2 or 2,0,1. Every digit 0, 1, and 2 must appear exactly once. Indices refer to the candidate columns as presented cand_0 / cand_1 / cand_2), not to any hidden book index. Evaluation Scored by exact-match accuracy in [0, 1]. Higher is better. For each item, score 1 if the predicted order string exactly equals the gold order, else 0. The challenge score is the mean over test items. Pseudocode: def evaluate(items): return mean(1.0 if pred_order == true_order else 0.0 for each item) A constant 0,1,2 guess is near chance (~1/6). Dataset Files in ./dataset/public/: train.csv — labeled training data (360 rows) test.csv — unlabeled test data (270 rows) sample_submission.csv — example submission format Column descriptions: item_id (string) — present only in test.csv and in the submission file; not present in train.csv anchor (string) — earlier passage; present in train.csv and test.csv cand_0, cand_1, cand_2 (string) — later same-book passages in shuffled presentation order order (string) — gold permutation earliest→latest; present in train.csv only; required in submission train.csv columns: anchor, cand_0, cand_1, cand_2, order test.csv columns: item_id, anchor, cand_0, cand_1, cand_2 sample_submission.csv columns: item_id, order Source note: built from a curated multi-book corpus of US public-domain English literary editions (same underlying corpus as the attached dataset). Chronological order is derived from in-book passage indices offline; it is not an upstream published field. Exact edition titles, catalog paths, and download URLs are intentionally not listed here (anti-scraping). Reviewers: see ./dataset/private/reviewer_book_list.json written by prepare. Use only files under ./dataset/public/. Submission Format Write predictions to ./working/submission.csv as a CSV with a header row and exactly these columns: item_id (string) — must cover every test.csv item_id exactly once (row order may differ) order (string) — permutation of 0,1,2 earliest→latest Requirements: Exactly 270 data rows (one per test item), plus the header row No null or empty values; no duplicate item_id values order must be a valid permutation string Scoring merges on item_id, so reordering submission rows does not change the score Example (format only; quote order because it contains commas): item_id,order FTO_ab12cd34ef56,"2,0,1" FTO_99aa88bb77cc,"0,1,2" What not to use External datasets, APIs, model downloads beyond what the configured Kaggle Docker / GPU image allows, or web scraping of source editions Test labels or any file under ./dataset/private/ Hardcoded item_id-to-order lookup tables Packages beyond what the standard Kaggle Python Docker image preinstalls &nbsp;
> $700 Pool
> Closes in 7h 32m
> 6 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Context-Dependent Marker Resolution

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77z4yn168e511gpc1kma4j8s8asszs
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat balaji's score of 0.290!

Full challenge description from page:

> Overview A source is a sequence of tokens. Scattered through it are markers: short tokens that stand in for a longer word. The catch is that the same short surface resolves to different full forms depending on where it sits — the marker π̅ might stand for one word beside a number and a different word beside a name; the marker κ̅ might be one thing in a heading and another in a closing line. There is no lookup table that settles it. The resolution has to be read off the local context — the tokens around the marker. You are given, per source, its full token sequence and the positions of the markers in it. For each marked position you must supply the marker's full form — the complete word it stands for in that place. The surface is not the answer. A marker's short form is genuinely ambiguous: across the corpus a given surface takes several full forms, and the split is decided by context, not by the surface. Always guessing a surface's most common full form leaves most of the hard cases wrong. The text is anonymised. Every token has been passed through a fixed, length-preserving letter substitution applied consistently across the whole corpus. Word shapes, repetition, and the co-occurrence structure that carries the context signal are all preserved; the substitution only prevents matching the released text against any outside source. Solve it from the released tokens alone. Data All files are UTF-8 CSV with a header row. Token sequences and marker lists are stored as JSON strings inside cells (parse them with a JSON reader). train.csv — one row per revealed source test.csv — one row per source to resolve sample_submission.csv item_id,resolutions ed_1a2b3c4d5e6f,7:;15:;23: One row per source. resolutions packs that source's markers as position:full_form pairs joined by ;. This sample fills each marker with its surface's most common full form (ignoring context) — it scores near zero. metadata.json A JSON object with keys task, columns, submission_columns, submission_note, metric, and files. Informational; the grader does not read it. Train / test split Sources are split by whole document: each source is assigned entirely to train.csv or to test.csv by a fixed, salted hash of its id (~80% train / 20% test), so a source is never divided across the two files. No test source, and none of its gold resolutions, is visible during training — the evaluation cannot be passed by memorising a particular source's answers, and there is no source-level overlap between the splits. The split is deliberately designed to reward context resolution, not table lookup: Ambiguous surfaces recur on both sides. A marker surface that takes several full forms appears in both train and test, and which form is correct is fixed by the local context, not by the surface. So a surface→most-frequent-form table learned from train is wrong on the contested markers: the constant-per-surface baseline scores only ≈0.10 document exact-resolution, far below what a context-aware method reaches. Memorising train resolutions does not transfer. Unseen surfaces. About one test marker in six uses a surface that never appears in training, so those must be resolved from context and word shape rather than looked up at all. The document-level metric compounds this. Because a source scores only when every one of its markers is exact, resolving just the easy, unambiguous markers cannot carry a source across the line — the ambiguous markers, which require reading the surrounding tokens, decide each source. Together these mean a high score requires genuine generalisation of context-dependent resolution to unseen sources, not recall of resolutions seen in training. Task For each test source and each of its marker positions, predict the full form the marker resolves to **at that position** given the surrounding tokens. Evaluation Document exact-resolution — the fraction of test sources for which every marker is resolved to the exact gold full form (case- and character-exact). A source counts only if all of its markers are correct; getting most of a source's markers right but one wrong scores that source zero. The final score is that fraction over all test sources, in [0, 1], higher is better. Because the score is per-source all-or-nothing, it compounds over each source's markers: a method that only gets the easy, unambiguous markers cannot carry a source across the line — the contested markers have to be resolved from context too. Submission format A UTF-8 CSV with a header and exactly these columns: item_id,resolutions ed_1a2b3c4d5e6f,7:;15: item_id — string; a test source id. One row per source (ids unique). resolutions — string; that source's marker resolutions packed as position:full_form pairs joined by ;. Give one pair for each position in the source's positions; position is a 0-based token index and full_form is your predicted resolution. A marker whose pair is missing, blank, or malformed simply scores that marker wrong — and because scoring is per-source all-or-nothing, that fails its source. For a repeated item_id the first row is used. Requirements (violations rejected as invalid): exactly the columns above, in that order; no null item_id; no duplicate item_id; no unknown item_id (every id must be a test source). Allowed Any approach: a context classifier over the tokens around each marker, a sequence model trained from scratch on the revealed sources, a nearest-context retrieval scheme, or a per-surface disambiguator conditioned on neighbouring tokens. Use only libraries already in the runtime; everything must run offline and on CPU (the data is tiny). What Not To Use No runtime installs or downloads — no pip/conda/apt installs and no fetching or vendoring extra packages, code, or model files; use only what is in the runtime. No external data or network access — no external corpora, lexicons, or resolution tables, and no downloading data over the network. No remote or dynamic models — no hosted inference APIs, gated checkpoints, trust_remote_code=True, or torch.hub.load(). No attempting to identify or retrieve the source corpus or any external key to it, and no use of any answer/label file. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Unseen-Headword Lexical Unit Discovery and Sense Linking

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76evz0499a56nzckgmzmsr0d8e3qfa
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat ismaildos4's score of 0.526!

Full challenge description from page:

> Overview Identify contextually ambiguous lexical units in multilingual sentences and link each to its dictionary meaning. Test headwords have no labeled training occurrences, but their definitions are supplied. You must transfer contextual disambiguation to new vocabulary, locate units yourself, including multiword units, and distinguish competing definitions. Only headword/part-of-speech groups with at least two distinct definitions are in scope. Dataset The release has 1,200 training sentences, 300 test sentences and 128,931 dictionary senses across ten languages. Parallel sentence groups are assigned wholly to one partition; repeated inputs connect groups before splitting and conflicting duplicates are excluded. A fixed hash ordering then selects the compact sentence subset inside each partition without changing any retained target. Related passages may still recur. Independently, a deterministic headword split reserves approximately one fifth of (language, case-folded lemma) groups for testing. All parts of speech and senses for a reserved headword stay out of training labels. The dictionary's target_split specifies which entries are eligible for each partition. Training inputs can incidentally contain reserved words, but no annotated unit with a reserved headword is supplied as a training target. Definitions remain available for both sets: this tests transfer from labeled headwords to dictionary-only headwords, not prediction without lexical evidence. | File | Fields | |---|---| | train.csv, test.csv | task_id: string; language: language code; tokens: JSON string array | | dictionary.csv | sense_id: string; language: code; lemma: headword; upos: part of speech; definition: natural-language definition; target_split: train or test | | train_labels.csv | task_id, units | | sample_submission.csv | Output format for all test IDs | Language codes are bg, da, en, es, et, hu, it, nl, pt, sl. Sentences contain at most 160 tokens. Reference units are native annotations whose source sense ID maps unambiguously to an available entry. Each eligible (language, case-folded lemma, upos) group has at least two distinct nonempty definition strings in the source inventory. All its eligible senses are supplied, not a short candidate list per token. Training sentences have at least two in-scope units; test sentences have at least one. Missing definitions, monosemous groups, non-content words and inconsistent assignments are excluded. Dictionary coverage and annotation practices vary by language. Source tokenization is authoritative. A multiword unit may be discontinuous. Submission Submit UTF-8 CSV with exactly task_id,units, in that order. Include each test ID once. units is a JSON array of at most 200 objects: token_indices: nonempty array of distinct zero-based token indices identifying the whole unit. Index order is irrelevant. sense_id: one identifier from dictionary.csv, formatted s_ followed by 24 hexadecimal characters. task_id,units example,"[{""token_indices"":[2,4],""sense_id"":""s_0123456789abcdef01234567""}]" The ID in this example illustrates syntax only. For test submissions, return only units linked to dictionary entries whose target_split is test; entries marked train are outside the test objective. Use actual dictionary IDs. An empty array is permitted. Evaluation The score is micro F1 over complete (token-index set, sense_id) pairs. Both the complete lexical unit and its meaning must match. This evaluates a usable semantic link rather than separately rewarding an incorrect sense or incomplete phrase. score = 2 × TP / (2 × TP + FP + FN) Counts are summed across sentences. Duplicate identical predictions count once. Scores range from 0 to 1; gold scores 1. If the denominator is zero, return 1. Malformed row content contributes all reference units as FN and max(1, reference_unit_count) FP. Incorrect but well-formed units contribute FP. Invalid CSV headers or ID sets are rejected. Row order has no effect. What Not To Use GPU training and general-purpose pretrained models are allowed. Do not use external annotated sense corpora, source copies, challenge-specific checkpoints, answer dictionaries, hosted APIs, manual test annotation. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The maximum end-to-end runtime is 1.5 hours, including data loading, training or adaptation, inference, structured decoding, validation, and submission writing. &nbsp;
> $700 Pool
> 4 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Adversarial Glossary Body Selection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7b04m5mdc5mw2nb3ve79pvg98c12gy
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat moatasem's score of 0.809!

Full challenge description from page:

> Adversarial Glossary Body Selection Overview Each example is a small regulatory glossary window with a twist that breaks plain closed-set STS matching: terms_json — M defined-term strings (M ∈ {5,6,7,8}) bodies_json — M+2 masked definition bodies alias_bank_json — an unaligned bag of surface aliases / acronyms (no map from alias → term) Exactly M of the bodies are the true definitions for the M terms (after independent shuffling and [TERM] masking of exact headword strings). The remaining 2 bodies are adversarial near-duplicate distractors mined from other windows in the same split: high token overlap with a true body, but the wrong definition. Residual lexical cues can remain after masking (acronyms, morphology, distinctive wording). Recover which body defines which term. Emit assignment — a comma-separated list of M integers — where assignment[k] is the index in bodies_json of the body that defines terms_json[k]. Hard constraints: Values must lie in 0 .. len(bodies_json)-1 All M indices must be distinct (injection into the larger body list; two terms may not claim the same body) Choosing a distractor body is always wrong for that term Format-only example (M=3, so 5 bodies): terms_json: ["Approved insurance provider","Conservation plan","Best drained condition"] bodies_json: five masked paragraphs (3 gold + 2 near-dup distractors), order scrambled alias_bank_json: e.g. ["AIP","NRCS","BDC","EPA"] — not aligned to term order assignment: 1,4,0 (three distinct indices into the five bodies) This is adversarial injective body selection under headword masking and an unaligned alias bank. It is not open-ended definition generation, free-form NER, span extraction, intrusion detection, survival ranking, or plain square glossary↔label matching without distractors. Use only ./dataset/public/. Row counts are in metadata.json (currently 4,380 train / 1,000 test after quality filters). Why this is hard Near-duplicate distractors punish pure semantic similarity ranking Square Hungarian on M×M is the wrong inductive bias; you must select among M+2 candidates [TERM] masking only reduces exact string leakage alias_bank_json helps with acronyms but does not tell you which alias belongs to which term Held-out source partitions + cross-split near-duplicate filters block train→test retrieval of the same glossary Input and output Input: terms_json, bodies_json, alias_bank_json Infer M = len(terms_json) and n_bodies = len(bodies_json) (n_bodies = M+2) Output: assignment — e.g. 2,0,1,4,3 — M distinct indices into 0 .. n_bodies-1 Evaluation Metric: injection-gated pair accuracy on [0, 1] (higher is better). For each test item_id: Parse assignment into integers (length must equal M) If it is not an injection into 0 .. n_bodies-1 (wrong length, OOB, or duplicates) → score 0 Else score = fraction of positions matching gold Final score = unweighted mean over items def item_score(pred, gold, M, n_bodies): if not is_injection(pred, M, n_bodies): return 0.0 return mean(pred[k] == gold[k] for k in range(M)) Grading matches rows by item_id (submission row order does not affect the score). Dataset Public files under ./dataset/public/: train.csv — labeled test.csv — unlabeled sample_submission.csv — format example metadata.json — short task summary Columns: item_id (string) — test / submission; opaque RDT_… id terms_json (string) — JSON array of M terms bodies_json (string) — JSON array of M+2 masked bodies (gold + distractors) alias_bank_json (string) — JSON array of unaligned alias strings assignment (string) — gold injection; train / submission only train.csv: terms_json, bodies_json, alias_bank_json, assignment test.csv: item_id, terms_json, bodies_json, alias_bank_json sample_submission.csv: item_id, assignment Source note: curated multi-partition corpus of US public-domain federal regulatory definition sections. Terms/bodies are real; gold pairings and distractors are derived offline. Upstream paths/URLs are omitted here (anti-scraping). Use only ./dataset/public/. Submission Write ./working/submission.csv with: item_id — every test id exactly once assignment — predicted injection, e.g. 3,0,2,1,4 Requirements: Header required; one row per test item; no null/empty fields Prefer the same row order as test.csv; scoring is by item_id Quote assignment fields (they contain commas) item_id,assignment RDT_ab12cd34ef56,"2,0,1,4,3" RDT_99aa88bb77cc,"0,3,1,2,5,4" What not to use External datasets, APIs, web scraping, or downloading extra model weights / checkpoints / embeddings Anything under ./dataset/private/ Hardcoded item_id → assignment tables Packages outside the standard Kaggle Python Docker image GPU-only libraries / GPU-required workflows Pretrained-model policy: Pretrained artifacts already present in the Kaggle Python Docker image are allowed (no network fetch). Downloading additional pretrained artifacts is forbidden. Fitting vectorizers/models from ./dataset/public/train.csv only is always allowed.
> $700 Pool
> 4 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## TED CPV Taxonomy Routing

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76k35paaqcc83g9nkz1hn1a18dyw1j
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview Public-procurement teams receive notices in several languages and need to route each notice to the right procurement desk before a human reviews the details. The useful destination is not only an exact category: a prediction in the same CPV group or division can still send a notice to the correct broad service family. Given the buyer-written text of a TED competition notice and its language, predict the four-digit CPV class of its primary procurement code. The challenge is a forward-looking classification task: training notices end before the fixed February 2026 cutoff, while test notices arrive from the following six months. The challenge adds no synthetic examples, generated text, translations, or labels. This is an NLP lane challenge: the target is a language-aware text-routing output, not a tabular classification task. Dataset File descriptions train.csv — 326,154 labeled notices published before 2026-02-05. test.csv — 81,830 notices published on or after 2026-02-05. The publication date is withheld from this file, but the language is supplied. Test rows are deterministically shuffled after the forward split, and notices whose class had no pre-cutoff training support are excluded from this closed-set task. sample_submission.csv — one valid, randomized CPV-class prediction per test ID. Column descriptions id (string) — an opaque, stable identifier for one notice. It is not the source publication number. language (string) — one of de, es, fr, it, or pl. text (string) — the source release's buyer-written title and description in the notice's own language, with exact primary-CPV code literals deterministically redacted by preparation. Whitespace and control characters are normalized, and exceptionally long public fields are capped at 100,000 characters for portable delimited-file parsing. No prose is generated or translated. cpv_class (string, training only) — the primary CPV class, encoded as C followed by the first four digits of the source's eight-digit primary CPV code. The test IDs and their order are the same in test.csv and sample_submission.csv. The holdout is chronological, not a random row split; rows are shuffled after the split so row position is not a publication-time feature; and no publication date column is provided to the solver. Evaluation The grader compares each predicted class with the hidden primary class. CPV is hierarchical, so the score gives useful partial credit: 1.0 — exact four-digit CPV class. 2/3 — different class but the same first three CPV digits (same CPV group). 1/3 — different group but the same first two CPV digits (same CPV division). 0.0 — different division. The row utilities are averaged inside each true CPV division, identified by the first two digits of the hidden four-digit class, and those division means are averaged equally. This prevents high-volume procurement families from dominating the result while preserving the operational value of correct broad routing. import pandas as pd def score(answers, submission): truth = answers["cpv_class"].astype(str) pred = submission["cpv_class"].astype(str) exact = pred.eq(truth) same_group = pred.str[1:4].eq(truth.str[1:4]) same_division = pred.str[1:3].eq(truth.str[1:3]) utility = exact.astype(float) utility += ((~exact) & same_group).astype(float) * (2.0 / 3.0) utility += ((~same_group) & same_division).astype(float) * (1.0 / 3.0) divisions = truth.str[1:3] division_scores = pd.DataFrame({ "division": divisions, "utility": utility, }).groupby("division")["utility"].mean() return float(division_scores.mean()) The score is bounded in [0, 1] and higher is better. CPV prefix levels are used because same-division routing is materially more useful than an unrelated category, while exact-class routing is the desired outcome. Submission Submit a CSV named submission.csv. Include exactly two columns, in this order: id, cpv_class. Include exactly one row for every ID in test.csv; IDs must be unique. Each cpv_class must be C followed by exactly four digits, for example C4500. Example: id,cpv_class ted_58b51e39223e707d81b0,C4500 Requirements Train from the supplied public notices and labels; the main predictive signal must come from the notice text and language. Do not add synthetic notices, generated translations, paraphrases, or generated labels. Ordinary preprocessing and model-training augmentation over supplied text is allowed only if it does not introduce new labeled examples. A solution should evaluate on time-forward, language-aware validation rather than relying only on a random row split. Do not use the public row order as a proxy for publication time; test rows are shuffled after preparation. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Feedback-Guided Edit Localization

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fcrjb2esef95zzgnr5p6dtn8e7vf6
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat aneeshm44's score of 0.486!

Full challenge description from page:

> Overview Given a conversation, a draft answer, and human feedback, predict where a human editor changed the draft or inserted new material. Return an edit-location mask, not a rewritten answer. Editing assistants must connect critiques to specific text without rewriting untouched content. Real human feedback and revisions of model-written answers provide examples of code errors, missing explanations, language mistakes, and irrelevant passages. Predict the recorded edit locations, not a new revision. Dataset UTF-8 CSVs contain JSON arrays in individual string cells. Parse CSV and JSON separately. | File | Contents | |---|---| | train.csv | 6,443 labeled examples. Columns, in order: case_id, dialogue, draft, editor_feedback, edit_mask. | | test.csv | 1,418 unlabeled examples. Columns, in order: case_id, dialogue, draft, editor_feedback. | | sample_submission.csv | Input-only baseline for every test ID; columns case_id,edit_mask. | Private answers.csv uses the ordered columns case_id,edit_mask. No auxiliary media files are needed. Input Columns | Column | Type | Contents | |---|---|---| | case_id | string | Opaque example identifier. | | dialogue | JSON-encoded string | Chronological array of objects with string role and content fields; at most 24,000 encoded characters. | | draft | string | Original answer, including punctuation, code, and whitespace. It contains 12 to 640 evaluation tokens. | | editor_feedback | JSON-encoded string | Nonempty array of human-written critiques; at most 12,000 encoded characters. Critiques can disagree in emphasis. | The Edit Mask | Column | Type | Meaning | |---|---|---| | edit_mask | string | Letter E followed by a binary word of length 2*N+1, where N is the draft's evaluation-token count. | Evaluation tokens are exactly those returned by Python re.findall(r"\w+|", draft, flags=re.UNICODE). Whitespace is not a token; a run of word characters is one token and each remaining non-whitespace character is its own token. Matching is case-sensitive. After removing the leading E, use zero-based bit positions: | Bit position | Meaning of 1 | |---|---| | 2*i, for i = 0 through N | New material was inserted at gap i: before token i, or after the last token when i = N. | | 2*i+1, for i = 0 through N-1 | Original token i was deleted or replaced. | A 0 means no corresponding edit. The prefix prevents CSV readers from converting masks to numbers or dropping leading zeros. Total encoded length is 26 to 1,282 characters. For an illustrative three-token draft A B C changed to A X C, the mask would be E0001000. This short illustration explains the indexing only; real submitted examples have at least twelve draft tokens. Ground Truth and Scope References use difflib.SequenceMatcher(..., autojunk=False) on draft and human-revision tokens. Deletions and replacements mark original tokens; only pure insertions mark gaps. Replacements do not also mark gaps. Equal tokens remain zero; whitespace-only edits are ignored. This reproducible alignment defines the target. Revisions and change summaries are withheld. Empty critiques, oversized contexts, and no-edit cases are excluded. Repeated prompts and exact repeated draft/revised answers are grouped before splitting; duplicate inputs count once. References reflect an editor's choice, including optional stylistic changes. Prepared Distribution | Measure | Training | Test | |---|---|---| | original tokens | 1818831 | 400821 | | changed tokens | 568272 | 122873 | | insertions | 21901 | 4748 | Submission Format Write the final CSV to ./working/submission.csv. The exact ordered header is case_id,edit_mask. Both columns are strings. Include every test ID exactly once; rows may be reordered. Missing, extra, duplicate, null, malformed, or unknown IDs reject the file, as do missing, extra, duplicate, or reordered columns. Do not add an index. Labeled training example; use the corresponding test IDs in your submission: | case_id | edit_mask | |---|---| | case_e2a0ebbb0dad7ddafd4c79bc | E0101010101010101010101010101010101010101010101000 | Only the E prefix and binary characters are valid. The number of bits must match the supplied draft. Whitespace, JSON arrays, replacement text, and trailing comments are not accepted as masks. Evaluation Minimum score: 0.0. Maximum score: 1.0. Higher is better. Metric: Feedback-to-Edit Score. Each mask defines three event sets: Changed-token events: odd bit positions set to 1. Insertion-gap events: even bit positions set to 1. Edit-run events: the (start,end) intervals of maximal consecutive 1 bits in the prefix-free mask, with end excluded. For each event type, match events within the same example, then sum true positives (TP), false positives (FP), and false negatives (FN) over the evaluated examples. Its micro F1 is 2TP / (2TP+FP+FN). If both prediction and truth contain no events of a type over the entire evaluated set, its F1 is 1. Final score = 0.55 * ChangedTokenF1 + 0.25 * InsertionGapF1 + 0.20 * EditRunF1. The 55% token term evaluates existing content, 25% separates omissions from replacements, and 20% rewards localized runs over scattered edits. Unchanged background bits earn no direct credit. For an invalid mask, each component receives zero TP, FN equal to that example's reference event count, and FP equal to the prefix-free reference mask length. Invalid predictions therefore remain in the micro-average denominator. Reference-format failures raise an error rather than being repaired or clipped. Local Reference Checks | Check | Score | |---|---| | Exact answers | 1.000000 | | Supplied sample submission | 0.000000 | | Literal training-mode string, not adjusted to draft length | 0.000000 | The mode string is invalid for most mask lengths; its zero does not establish difficulty. Learned GPU and hosted agent baselines are unmeasured. Practical Starting Point Fine-tune a compact encoder conditioned on dialogue and feedback, with token-change and gap-insertion heads. Preserve evaluation-token offsets and use prompt-grouped internal validation. The competition environment provides access to a single NVIDIA A10G GPU. The entire pipeline must finish within 1.5 hours, including data loading, training or adaptation, inference, decoding, validation, and submission generation. Allowed Methods and Data Boundaries Public-training-data models, content-based nearest neighbors, and internal validation are allowed. Local pretrained resources must comply with licensing and platform rules. Select models using training data, not hidden outcomes. What Not To Use Do not retrieve evaluation labels through source-text searches, source IDs, external answer tables, or checkpoints trained on hidden annotations. Do not predict from case IDs, filenames, sizes, row order, or hashes. Other participants' outputs, external inference services, and evaluator manipulation are prohibited. Opaque IDs do not make source text unsearchable; source lookup remains prohibited. &nbsp;
> $700 Pool
> Closes in 4h 56m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Anchored Entity Chain Completion

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ergvjwkyn5vjpt4qnm8y7kh8e640c
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat amtech's score of 0.373!

Full challenge description from page:

> Overview Given a news article and one marked mention, recover every other mention referring to that same entity. Return complete token spans, including aliases, descriptions and pronouns. The target is a complete entity record: an unrelated mention contaminates the record, while an omitted mention leaves it incomplete. Dataset There are 1,200 training queries from 561 documents and 300 test queries from 135 different documents. Each query represents a distinct native entity chain with at least three mentions; one mention is supplied as the anchor. No entity is repeated with different anchors to multiply the row count. Exact repeated documents are excluded, and a deterministic whole-document split keeps all queries from an article together. Queries are selected by fixed hash order inside the existing document-disjoint partitions. Complete token sequences, anchors and reference mention chains are retained. News topics and named people may recur across different articles. Documents contain 50–1,500 tokens. Every anchor is a complete native mention represented by distinct, zero-based token positions. Indices refer to the supplied token sequence, not character offsets. A mention may be discontinuous. Queries sharing an article are related examples, not independent documents. Public news text contains names; annotations provide one reference analysis and may omit defensible alternative links. Submission Submit UTF-8 CSV with exactly task_id,mentions, in that order, including each test ID once. mentions is a JSON array of at most 500 distinct mention spans. Each span is a nonempty array of distinct integer token indices from 0 to 1,499, within the supplied document. Return all other mentions of the anchor entity; do not return the anchor itself. Ordering of mentions and indices is irrelevant. An empty array is allowed. task_id,mentions example,"[[12,13],[48],[91,93]]" Evaluation The metric is exact complete-chain recovery accuracy: score = number_of_exactly_recovered_queries / number_of_queries A query is correct only when the unordered set of predicted token spans exactly equals the reference set. There is no partial credit for recovering only easy name repetitions while missing pronouns or including a different entity. This measures completeness of the native entity record, not general linguistic correctness under every possible interpretation. Scores range from 0 to 1; gold scores 1. Duplicate mentions, malformed JSON, invalid types or invalid global index ranges score zero for that query. Incorrect headers, missing/extra IDs and duplicate IDs are rejected. Row order has no effect. Expected Approach Train an anchor-conditioned mention detector and linking model. Score complete candidate spans against the marked anchor, including pronouns and aliases, rather than relying only on repeated names. For an efficient implementation: Parse each document once and reuse its tokenization across anchors. Cache encoder embeddings only while the encoder is frozen. Use overlapping windows for long articles, preserving exact source-token offsets and a representation of the anchor in every window. Prune low-scoring mention candidates before pair scoring. Support discontinuous mentions with token-index sets rather than forcing every span to be contiguous. Validate by document group and tune the selection threshold for exact complete-chain recovery. Remove the anchor and duplicate mentions before serialization. What Not To Use GPU training and general-purpose pretrained language models are allowed. Do not use external annotated coreference corpora, source copies, challenge-specific checkpoints, hard-coded test answers, hosted APIs, manual annotation of test articles. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The complete solution must finish within 60 minutes end to end, including data loading, preprocessing, feature extraction, training or adaptation, validation, inference, structured decoding and submission writing. This is a total execution limit, not a separate allowance for each stage. The platform may terminate execution at the limit; use elapsed-time checks and retain the best completed model so that a valid submission is written before the deadline. Start with a small end-to-end run and write a valid full-test submission early. Use a wall-clock timer from process start, avoid exhaustive searches and large ensembles, and reserve at least the final 10 minutes for inference and submission checks; increase this reserve if measured throughput requires it. Cache encoder outputs only while the encoder is frozen. &nbsp;
> Closes in 3h 27m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Gavel Loom: Multi-Session Debate Graph Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79j58d8td8gskmabdz2zmnxx8e8dj9
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat krsna-dev's score of 0.588!

Full challenge description from page:

> Gavel Loom: Multi-Session Debate Graph Reconstruction Overview Gavel Loom is a structured NLP challenge built from real Turkish parliamentary speech, not synthetic language. Parliamentary archives preserve long debates, but damaged exports and partial retrieval can separate related passages and erase their local order. Your task is to reconstruct that missing discourse structure. Each puzzle_id contains twelve shuffled excerpts drawn from three different source speeches. Each source speech contributes four visible excerpts that form one directed chain. A short span of the original speech between consecutive visible excerpts is withheld, so matching an exact cut boundary is not enough. For every excerpt, predict the id of the next visible excerpt in the same latent speech. Predict END] when the excerpt is the final visible node in its chain. A complete puzzle therefore contains exactly three disjoint directed paths, each with four nodes. The available participant data consists of labeled training puzzles, unlabeled test puzzles, and a submission-format example under ./dataset/public/. Evaluation Submissions are ranked by the Weighted Directed Chain Reconstruction Score, abbreviated WDCRS. Higher is better. Its range is [0, 1]. Let N be the true nonterminal nodes and F the true terminal nodes. Every i in N has a positive hidden difficulty weight w_i between 1.0 and 1.65. The weight is 1 + 0.65 × (1 - Jaccard), where Jaccard is the set-token overlap between the current excerpt and its true successor using case-folded alphabetic tokens of at least four characters. The three components are: E, weighted exact-successor accuracy: sum(w_i × 1[pred_i = next_i]) / sum(w_i) over i in N. C, weighted same-chain accuracy: sum(w_i × 1[pred_i is a different node in the same hidden chain and puzzle]) / sum(w_i) over i in N. T, terminal accuracy: sum(1[pred_i = [END]]) / |F| over i in F. The final score is: WDCRS = 0.51 × E + 0.35 × C + 0.14 × T The denominators above normalize each component before combination. Exact successor recovery has the largest individual weight. Same-chain credit is partial structural credit and does not replace the exact-edge objective. The concise function below defines the metric for a structurally valid submission. The common grader handles schema, ID-set, and malformed-value validation described under Requirements. y_true is evaluator-owned and contains id, chain_key, next_id, is_terminal, and difficulty_weight. The hidden chain_key is globally unique per latent chain. y_pred is the submitted two-column frame. import numpy as np END_TOKEN = "[END]" def evaluate(y_true, y_pred): merged = y_true.merge( y_pred.rename(columns={"next_id": "prediction"}), on="id", how="left", validate="one_to_one", ) terminal = merged["is_terminal"].astype(bool).to_numpy() weights = merged["difficulty_weight"].to_numpy(float) true_next = merged["next_id"].to_numpy(str) predicted_next = merged["prediction"].to_numpy(str) exact = predicted_next == true_next id_to_chain = dict(zip(merged["id"], merged["chain_key"], strict=True)) same_chain = np.zeros(len(merged), dtype=bool) for row, candidate in enumerate(predicted_next): current_id = merged.iloc[row valid_relation = ( not terminalrow] and candidate not in {END_TOKEN, current_id} and candidate in id_to_chain ) same_chain[row] = valid_relation and ( id_to_chain[candidate] == merged.iloc[row ) nonterminal = ~terminal E = np.average(exact[nonterminal], weights=weights[nonterminal]) C = np.average(same_chain[nonterminal], weights=weights[nonterminal]) T = np.mean(predicted_next[terminal] == END_TOKEN) return float(np.clip(0.51 * E + 0.35 * C + 0.14 * T, 0.0, 1.0)) Dataset All participant-visible files are inside ./dataset/public/. train.csv Contains 18,252 labeled nodes from 1,521 puzzles. Every puzzle has twelve rows. id (string) — random opaque node identifier, unique across the training file. puzzle_id (string) — random opaque identifier shared by the twelve nodes in one puzzle. text (string) — one visible Turkish discourse excerpt. next_id (string) — the next node ID in the true chain, or [END] for a terminal node. test.csv Contains 5,064 unlabeled nodes from 422 puzzles. Every puzzle has twelve rows. id (string) — random opaque node identifier, unique across the test file. puzzle_id (string) — random opaque identifier shared by the twelve nodes in one puzzle. text (string) — one visible Turkish discourse excerpt. sample_submission.csv Contains 5,064 rows and demonstrates the required submission schema. Its [END] values form a label-free structural baseline, not revealed test labels. id (string) — one test ID, with every test ID appearing exactly once. next_id (string) — placeholder successor prediction. Train and test are held out by complete source parliamentary session. The 4,563 training sessions and 1,266 test sessions have zero overlap. Their randomized node IDs have zero overlap, and exact excerpt text has zero cross-split overlap. The CSV row order and the lexicographic order of both identifiers are random and carry no sequence information. Submission Submit exactly one file named submission.csv. It must be a comma-separated UTF-8 file with exactly 5,064 data rows and this exact header order: id,next_id nd_kuzylyk2p74i57d4,nd_idkmvj7lr4aa7si2 nd_idkmvj7lr4aa7si2,[END] These are real test IDs and demonstrate syntax only; the shown next_id values are not disclosed labels. Your full file must contain every test id exactly once. The training target and submission prediction use the same representation: another node ID or the literal token [END]. Requirements Submit exactly 5,064 data rows, excluding the header. Use exactly two columns named id,next_id in that order. Missing, renamed, reordered, or additional columns cause a ValueError. Copy the complete test id set exactly once. Missing, duplicated, null, or foreign values in the id column cause a ValueError. A meaningful next_id is either another node ID from the same puzzle_id or the exact case-sensitive token [END]. This is a categorical output, so there is no numeric prediction range. A self-loop, cross-puzzle node, unknown node, or incorrectly placed [END] receives no exact or applicable structural credit. Such content does not change the required ID-row coverage. A null, empty, non-finite-like string, or value longer than 128 characters in next_id is converted to an invalid prediction and receives worst credit for the affected row. The final score remains finite. Each correct puzzle contains exactly three [END] predictions and three disjoint paths of four nodes. The grader scores rows rather than rejecting a structurally inconsistent graph, but constrained decoding is strongly recommended. Maximize WDCRS; the valid score interval is [0, 1]. Runtime is limited to 90 minutes. The intended hardware is one NVIDIA GPU, and the supplied reference approach requires CUDA. Read inputs only from ./dataset/public/ and write the final file to ./working/submission.csv. What Not to Use Do not use pretrained model weights, external datasets, external embeddings, search indexes, or manually collected text. Do not make runtime downloads or network calls. Do not query Zenodo, the parliamentary website, search engines, or another copy of the proceedings to recover original order, withheld spans, identities, or source sessions. Do not derive features from CSV row position, lexicographic id, or lexicographic puzzle_id; these surfaces are randomized and inert. These restrictions are part of the participation contract. The score function alone cannot detect every external-data or answer-key violation, so the execution harness and review process enforce them. Extra Modelling Information Gavel Loom requires joint recovery of three confusable source speeches inside one twelve-node candidate set, with real intervening spans removed at every transition. It evaluates a forest of three directed paths, awards separately normalized exact-edge and same-chain credit, and holds out complete parliamentary sessions rather than random rows. These changes make chain identity, discourse direction, terminal detection, and globally valid decoding distinct learned subproblems.
> Closes in 3h 33m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Cross-Script Thread Recovery on Wikipedia Talk Pages

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bfvvj092cdm0j998g44vr358eard9
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: Not displayed; detail page unavailable
- GPU: Not displayed; detail page unavailable
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 0.409!

Full challenge description from page:

> OverviewA Wikipedia talk page is not a conversation. It is several conversations, arriving in one stream, in the order editors happened to post. Someone answers a thread that has been quiet for two weeks while another thread is being opened three lines above. A reader untangles this without effort, and so does a model that can lean on indentation, on signatures, or on who is talking to whom.This challenge removes all three and moves the language.You train on Greek talk pages and you are scored on Chinese ones. The venue is identical on both sides - same site, same conventions, same rhythm of editing - so the structure you can learn is real structure. The lexicon, however, is gone twice over: the two languages share no vocabulary, and Chinese is not written with spaces, so anything learned as a Greek word feature is worth exactly nothing at test time. So is anything learned about Greek editors: there is no author column, and every editor handle known on a page has been replaced inside the message text by the token .What is left to learn is the part that was never language-specific - that a reply resembles what it answers even across scripts, that a conversation occupies a contiguous stretch of a page's attention, that a burst of edits is one thread rather than four, that the gap before a message carries information but only relative to the pace of that particular page.The taskFor every message in every test page, say which conversation it belongs to.You are given, per page, the messages in the order they were posted, each with the elapsed time since the first message on that page and the message text. You are not given the author, the indentation, the section heading, or the number of conversations to find. You choose the grouping, and you choose your own label strings.Datatrain_messages.csv - 21,146 messages over 279 Greek pages train_conversations.csv - the true conversation of every training message test_messages.csv - 9,921 messages over 47 Chinese pages test_queries.csv - the 9,921 messages you must label sample_submission.csv - a valid submission that puts every message on a page in one conversationfile_id — the page; a conversation never crosses onemsg_index — position of the message in that page's stream, from 0t_offset — seconds since the first message on that pagetext — the message, with every known handle replaced by and every IP address by Training is 2.1x the size of the test set, and every training message carries its label.EvaluationA predicted conversation counts only if it matches a true conversation exactly - the same set of messages, none missing and none added. Precision and recall are pooled over the test pages and combined into F1.precision = (exactly matched conversations) / (predicted conversations) recall = (exactly matched conversations) / (true conversations) score = 2 precision recall / (precision + recall)Higher is better, the range is 0 to 1, and there are no other terms and no hidden weights.Conversations are compared within a page. Reusing a label on two different pages never merges them, so your labelling scheme cannot help you or hurt you - only the grouping counts.Partial structure is worth nothing. A conversation with one message missing scores the same as one that was never found, and merging two conversations costs the same as merging ten. The score moves only when a whole conversation comes out right. That is deliberate: it is the property that makes a one-line rule fail here, and it is the reason the numbers below are as low as they are.What you are up againstEvery number below was produced by the grader shipped with this challenge, on this exact split.the shipped sample_submission.csv (one conversation per page) — 0.0000every message its own conversation — 0.0512link each message to the one before it — 0.0000best "new conversation after a silence of N" rule, N tuned over a decade-wide grid — 0.1799nearest earlier message by shared vocabulary — 0.0553published reference: trained pair ranker + connected-component decode — 0.3222The silence rule is quoted at its best threshold over the whole grid, not at a plausible one, because that is the number a solver finds in an afternoon. It is the bar. The reference beats it on 42 of the 47 test pages, not on a handful of outliers.Note what the second and third rows mean together. Splitting on every message scores more than zero, and chaining every message scores exactly zero, so the metric is not rewarding either extremeit is rewarding getting whole threads right.Design notesWhy the language moves and the venue does not. An earlier version of this design trained on multi-party chat and tested on talk pages. It was built and measured, and it failed: a trained ranker scored 0.0190 where the silence rule scored 0.1747, because the two venues do not share a timescale and an exact-match metric rewards the correlated errors a gap rule makes over the scattered errors a transferred model makes. Holding the venue fixed and moving only the language keeps the transfer real without making it hopeless.Which pages are in the test set. Only pages whose threads genuinely interleave: a page's excess switch rate - how much more often the stream changes thread than a page of contiguous blocks wouldmust be at least 0.20. On a page of contiguous blocks there is nothing to disentangle and the silence rule already solves it. 47 Chinese pages clear that bar; they carry 2,301 conversations.What was withheld, and what it was worth. Author identity is the big one. It is not withheld to make the task fashionable: clustering a page by author alone scores 0.50-0.58 on the venue this corpus comes from, which is above anything in the table above. This is a challenge about structure precisely because identity has been taken away.Ties to a page's own pace. Talk-page gaps span seconds to months, and a threshold that suits one page is wrong for the next. The reference uses gaps rank-normalised within a page alongside raw gaps; a reference built only on raw seconds is a weak instance of the idea and would condemn the design for the wrong reason.Allowed, and not allowedAny method, trained from scratch or pretrained. Multilingual pretrained encoders are fair game and are the obvious way to attack the cross-script gap.No external data and no network. The grading sandbox has none. In particular: this data is derived from the public WikiConv corpus, whose reply structure is published upstream. Recovering the test labels from the upstream corpus, from a Wikipedia dump, or from any copy of either is outside the task and defeats its purpose.No use of the test conversations' structure beyond what the files give you. Treat each test page on its own terms.Your script must be deterministic and must finish inside the compute budget.Submissionsubmission.csv, exactly two columns:query_id,conversation_id Q000001,a Q000002,a Q000003,bOne row per query_id in test_queries.csv, no extra columns, no missing rows. The conversation_id values are yours to name.SourceWikipedia talk-page conversations from WikiConv (Hua, Danescu-Niculescu-Mizil, Taraborelli, Thain, Sorensen and Dixon, WikiConv: A Corpus of the Complete Conversational History of a Large Online Collaborative Community, EMNLP 2018), Greek and Chinese releases, both CC BY 4.0. The conversation structure is the corpus's own reply graph, reconstructed by its authors from the talk-page revision history - not a rater's opinion and not a model's output. Comment text is Wikipedia editor content under CC BY-SA. &nbsp;
> Closes in 3h 10m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Article-Scoped Discourse Link Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dftyj8xhy55t6xb42k5x7ss8bkmpy
- DOMAIN exactly as displayed: NLP
- Challenge collection: Non-CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat the top user's score of 0.821!

Full challenge description from page:

> Overview Recover how a proposition connects to the other arguments in its source article. Each query supplies a sentence and a proposition taken from a human-written question, but with the relation-bearing question prefix removed. Select its answer argument from an article-wide bank and recover the missing relation. Several different links can be annotated for the same proposition. The bank includes answers to other questions about the article, not fabricated negative text. Finding a nearby or lexically similar phrase is not sufficient: a reason, result, qualification and example can refer to different aspects of the same event. Dataset There are 1,200 training queries and 300 test queries. Whole article families are split by a fixed hash; articles sharing an identical normalized source sentence are connected before splitting. Article families do not cross the split. A fixed hash ordering selects the compact query subset inside each partition. Only referenced article banks are included, and each retained bank preserves all its candidates. Repeated queries from one article are related examples. Similar topics and paraphrases may still recur across articles. Banks contain 8–256 distinct argument strings. IDs are shuffled within each bank and reveal no answer order. A link is {"relation":"What is the reason","argument_id":"a012"}. The 17 allowed relation strings are: After what; Before what; Despite what; Except when; In what case; In what manner; Instead of what; Since when; Unless what; Until when; What is an alternative to; What is an example of; What is contrasted with; What is similar to; What is the reason; What is the result of; While what. These are the original annotation categories, not interchangeable natural-language paraphrases. Human answers can be grammatically edited rather than verbatim source spans. Annotations are not an exhaustive inventory of every plausible relation; rare categories and disagreements limit coverage. Rows without an annotated relation are excluded, not treated as negative labels. Submission Submit UTF-8 CSV with exactly task_id,links, in that order, once per test query. links is a JSON array of at most 64 distinct (relation, argument_id) pairs. The same argument may participate in several relations. Use bank-local IDs; return an empty array when abstaining. task_id,links example_query,"[{""relation"":""What is the reason"",""argument_id"":""a012""}]" Evaluation The score is mean typed-link set F1, from 0 to 1, higher better. For each query: F1 = 2 × |predicted links intersection reference links| / (number of predicted links + number of reference links) A link matches only when both its relation and argument ID are correct. This measures recovery of the complete semantic link while allowing partial credit when several links are present. References are nonempty; empty predictions score 0, exact references score 1. An out-of-bank ID cannot match. Link order and CSV row order do not affect scoring. Malformed JSON, invalid relation strings, duplicate links or arrays longer than 64 score 0 for that row. Wrong columns, duplicate IDs or missing/extra test rows invalidate the file. Expected Approach Train a compact query–argument scorer with a multi-label relation head. Condition on the sentence, proposition and auxiliary, then predict complete relation–argument links rather than selecting just one answer. For an efficient implementation: Load each article bank once and cache tokenization. With a frozen encoder, encode each distinct argument once and reuse its embedding across queries. Retrieve a short candidate list within the correct bank and rerank it with the learned scorer. Check candidate recall on training validation data before narrowing the list. Use other arguments in the same training bank as negatives and tune relation thresholds on held-out banks; do not force a single link per query. Batch similar-length query–argument pairs and serialize only valid bank-local IDs and allowed relation strings. What Not To Use GPU training and generic pretrained language models are allowed. Execution is offline and may use only the supplied data. Do not use source-corpus copies, external corpora, challenge-specific parsing checkpoints, hosted APIs, web lookup, manually labeled test answers or hard-coded predictions. Compute Environment The competition runtime provides one NVIDIA A10G GPU. The complete solution must finish within 60 minutes end to end, including data loading, preprocessing, feature extraction, training or adaptation, validation, inference, structured decoding and submission writing. This is a total execution limit, not a separate allowance for each stage. The platform may terminate execution at the limit; use elapsed-time checks and retain the best completed model so that a valid submission is written before the deadline. Start with a small end-to-end run and write a valid full-test submission early. Use a wall-clock timer from process start, avoid exhaustive searches and large ensembles, and reserve at least the final 10 minutes for inference and submission checks; increase this reserve if measured throughput requires it. Cache encoder outputs only while the encoder is frozen. &nbsp;
> Closes in 7h 23m
> 12 / 12 continuing slots

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.


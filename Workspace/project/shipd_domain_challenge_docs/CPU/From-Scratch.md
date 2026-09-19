# CPU From Scratch Challenge Examples

Scrape timestamp: 2026-07-14T00:00:00+05:30

Confirmed CPU examples in this document: 3

These entries are included because the challenge detail page displayed this domain and the challenge is part of the CPU-only challenge collection.

## Historical Object Era Modeling From Scratch

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx764qd2y4wm05nrwnc57ex88589b5zs
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↓ Lower is better
- Tags: image, feature-engineering, large-scale
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Historical Object Era Modeling From Scratch
> Overview
> You are given anonymized sparse-text metadata features for historical museum and archival object records. Your task is to build a CPU-only model from scratch that predicts the chronological era of each held-out object.
> This is a hard From Scratch challenge, but it is designed to be solvable on CPU within the allowed runtime. The public data does not expose original record IDs, original record URLs, original titles, original date strings, parsed years, exact collection names, source row order, or readable vocabulary. Text fields have been converted into salted hashed token sets, numeric year information has been removed, and public features have been deliberately sparsified.
> The target is an ordinal era bucket with 18 fine-grained chronological classes. Several neighboring classes cover only 5, 10, 15, or 25 years, so broad century-level reasoning is not enough. A strong solution must learn subtle chronology signals from sparse material-culture metadata: object categories, people or organization references, place references, collection vocabulary, material descriptions, physical-description tokens, and record-type signals.
> The train/test construction is intentionally difficult. Held-out records are not sampled as independent random rows. The preparation pipeline groups records by coarse metadata families before assigning held-out examples, reducing near-duplicate leakage between train and test and creating a distribution shift across object families.
> CPU Compatibility
> This challenge is intended for CPU execution only. A competitive solution should run on a machine with 10 CPU cores and 62 GB RAM within a 1.5 hour limit.
> Recommended CPU-friendly approaches include sparse vectorization, feature hashing, regularized linear classifiers, online/SGD classifiers, calibrated one-vs-rest models, compact gradient-boosted models over engineered counts, or small shallow neural networks trained from random initialization. Solvers do not need a GPU, pretrained language model, external embedding model, or large LLM.
> Files
> public/train.csv contains labeled training records.
> | Column | Type | Description |
> |---|---|---|
> | object_id | string | Anonymized public identifier for one object record. |
> | record_type_token | string | Hashed token representing the source record type. |
> | title_tokens | string | Sparse salted hashed tokens derived from title text. |
> | object_type_tokens | string | Sparse salted hashed tokens derived from object-type/category text. |
> | topic_tokens | string | Sparse salted hashed tokens derived from topic text. |
> | name_tokens | string | Sparse salted hashed tokens derived from associated-name text. |
> | place_tokens | string | Sparse salted hashed tokens derived from place text. |
> | culture_tokens | string | Sparse salted hashed tokens derived from culture text. |
> | physical_tokens | string | Sparse salted hashed tokens derived from physical-description or material text. |
> | set_tokens | string | Sparse salted hashed tokens derived from collection or set-name text. |
> | note_tokens | string | Sparse salted hashed tokens derived from note text. |
> | metadata_flags | string | Space-separated field-presence flags. |
> | label | string | Fine-grained historical era label. |
> public/test.csv contains the same columns except label.
> public/class_labels.csv lists the valid era labels, ordinal positions, and year ranges.
> public/sample_submission.csv shows the required probability submission format.
> Objective
> Predict a calibrated probability distribution over 18 historical era classes for every row in test.csv.
> Valid labels:
> | Label | Ordinal position | Year range |
> |---|---:|---|
> | era_pre_1750 | 0 | before 1750 |
> | era_1750_1799 | 1 | 1750-1799 |
> | era_1800_1824 | 2 | 1800-1824 |
> | era_1825_1849 | 3 | 1825-1849 |
> | era_1850_1864 | 4 | 1850-1864 |
> | era_1865_1879 | 5 | 1865-1879 |
> | era_1880_1894 | 6 | 1880-1894 |
> | era_1895_1909 | 7 | 1895-1909 |
> | era_1910_1924 | 8 | 1910-1924 |
> | era_1925_1939 | 9 | 1925-1939 |
> | era_1940_1954 | 10 | 1940-1954 |
> | era_1955_1969 | 11 | 1955-1969 |
> | era_1970_1984 | 12 | 1970-1984 |
> | era_1985_1999 | 13 | 1985-1999 |
> | era_2000_2009 | 14 | 2000-2009 |
> | era_2010_2014 | 15 | 2010-2014 |
> | era_2015_2019 | 16 | 2015-2019 |
> | era_2020_onward | 17 | 2020 onward |
> Because the labels are chronological, confusing adjacent era buckets is less severe than placing most probability mass many decades away. The metric rewards both calibration and ordinal awareness.
> Intended Approach
> Strong CPU-only solutions should:
> build sparse feature matrices from the hashed token columns;
> handle empty and highly sparse token fields robustly;
> combine token features, record-type features, and field-presence flags;
> train models from scratch using only the public training data;
> create validation splits that simulate grouped holdout behavior rather than only random row splits;
> calibrate predicted probabilities across all 18 classes;
> use the ordinal class order when tuning, ensembling, or post-processing predictions.
> The intended solution family is sparse text classification from scratch, not tabular regression. Good approaches include regularized logistic regression, SGDClassifier with log loss, linear one-vs-rest classifiers with probability calibration, compact CPU gradient boosting on engineered sparse-count features, or small neural models trained from random initialization.
> Disallowed Methods
> Do not use original record IDs, original record URLs, original date strings, parsed years, original titles, external copies of the underlying collection metadata, or external historical lookup tables to identify held-out records.
> Do not use GPU-only methods, pretrained language models, external embeddings, large LLM inference, reverse-engineered hashed tokens, hardcoded predictions by object_id, or manual matching of public rows to external records.
> Use only the public challenge files for training and inference.
> Evaluation
> Submissions are evaluated using an ordinal multiclass log loss:
> row_score = -log(p_true) + 0.06 * expected_ordinal_distance
> where:
> p_true is the submitted probability assigned to the true era class;
> expected_ordinal_distance is the probability-weighted absolute distance between each era class and the true class.
> The final score is the mean row score. Lower is better. The theoretical best score is 0. There is no finite upper bound for invalidly confident probability predictions, so configure the grading maximum as infinity.
> Submission Format
> Submit a CSV with exactly these columns:
> | Column | Type | Description |
> |---|---|---|
> | object_id | string | Must match one row from test.csv. |
> | era_pre_1750 | float | Predicted probability for era_pre_1750. |
> | era_1750_1799 | float | Predicted probability for era_1750_1799. |
> | era_1800_1824 | float | Predicted probability for era_1800_1824. |
> | era_1825_1849 | float | Predicted probability for era_1825_1849. |
> | era_1850_1864 | float | Predicted probability for era_1850_1864. |
> | era_1865_1879 | float | Predicted probability for era_1865_1879. |
> | era_1880_1894 | float | Predicted probability for era_1880_1894. |
> | era_1895_1909 | float | Predicted probability for era_1895_1909. |
> | era_1910_1924 | float | Predicted probability for era_1910_1924. |
> | era_1925_1939 | float | Predicted probability for era_1925_1939. |
> | era_1940_1954 | float | Predicted probability for era_1940_1954. |
> | era_1955_1969 | float | Predicted probability for era_1955_1969. |
> | era_1970_1984 | float | Predicted probability for era_1970_1984. |
> | era_1985_1999 | float | Predicted probability for era_1985_1999. |
> | era_2000_2009 | float | Predicted probability for era_2000_2009. |
> | era_2010_2014 | float | Predicted probability for era_2010_2014. |
> | era_2015_2019 | float | Predicted probability for era_2015_2019. |
> | era_2020_onward | float | Predicted probability for era_2020_onward. |
> Requirements:
> include exactly one row for every test object;
> do not include duplicate object_id values;
> do not add extra columns;
> probabilities must be finite and non-negative;
> each row must have a positive probability sum.

Inspiration note: Useful because it packages a CPU-only sparse metadata classification problem as a from-scratch ordinal probability task, with hashed token features, grouped holdout shift, and an ordinal log-loss metric.

## Parser Attachment Disagreement Prediction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fe85cat86f2z93s7s5146nn8ag5se
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Task
> Give the same raw sentence to 25 different parsers and they mostly agree on its syntactic structure — but not everywhere. At a prepositional phrase that could modify either a noun or a verb, at a coordination whose scope is unclear, at a word that could be an auxiliary or a main verb, the parsers split: some attach the word one way, some another. Those split points are the fault lines of the sentence's syntax — the places where the analysis is genuinely contested.
> You are given English sentences, tokenised. For every token, predict a single bit: is its attachment contested (the 25 parsers disagree on its head beyond a 15% margin) or settled?
> A token's contestedness is a property of the whole population of parses — it does not exist for a single parser, and no file or tool reports it. The 25 parser outputs were used once, offline, to compute the labels and are not given to you. So you cannot look the answer up; you must learn, from the words alone, where independent parsers are likely to disagree.
> This is genuinely hard. Roughly 23% of tokens are contested. Some of the signal is lexical (a word like "that" is often contested), but that alone gets you almost nowhere — the productive signal is structural: the surrounding context that makes a particular occurrence ambiguous. Expect scores well below 1.
> Data
> All files are under ./dataset/public/.
> File | Rows | Contents
> train.parquet | 20,624 | Labelled tokens, grouped into sentences.
> test.parquet | 4,145 | Same columns, contested withheld.
> sample_submission.csv | 4,145 | A correctly-formatted example (random labels; scores ~0).
> Train and test are document-disjoint: no source document (and therefore no near-duplicate sentence) is shared between them.
> Columns
> Column | Type | Description
> token_id | int64 | Row identifier. Opaque — assigned after the split and shuffled; it carries no signal.
> sentence_id | int64 | Groups tokens into sentences. Opaque (reassigned per split).
> position | int64 | 0-based position of the token within its sentence. Order by this to reconstruct the sentence.
> token | str | The surface form (word or punctuation).
> contested | int64 | Train only. The label: 1 if the 25 parsers disagree on this token's head, else 0.
> Submission
> Write ./working/submission.csv with exactly these two columns, in this order, one row per test token_id:
> token_id,contested
> 0,0
> 1,1
> 2,0
> 3,0
> The grader rejects a submission that has extra or missing columns, columns in the wrong order, an unknown / missing / duplicate token_id, a row count other than 4,145, or a contested value outside {0, 1}.
> Evaluation
> The score (maximise, in [0, 1]) is the Matthews Correlation Coefficient between your predicted contested labels and the true labels over all test tokens:
> TP = # tokens contested in BOTH prediction and truth
> TN = # tokens contested in NEITHER
> FP = # predicted contested but actually settled
> FN = # predicted settled but actually contested
> MCC = (TP·TN − FP·FN) / sqrt( (TP+FP)(TP+FN)(TN+FP)(TN+FN) )     # 0 if the denominator is 0
> score = clip(MCC, 0, 1)
> MCC, not accuracy or F1, is used deliberately. The classes are imbalanced (~23% contested), so "predict settled everywhere" is 77% accurate — but under MCC it has FP = TP = 0, a zero numerator, and scores exactly 0.000. So does "predict contested everywhere", and so does a random guess. A high-recall "flag every rare word" rule is punished for its low precision. Under MCC, only calibrated, genuinely discriminative predictions score at all.
> What to use
> Train a model from scratch on the provided data — a 1-D sequence model (BiLSTM / small transformer / CNN-CRF) over the token sequence is the natural fit. The productive paths are (a) using sentence context, not just the token in isolation — attachment ambiguity is created by the surroundings; (b) adding character / sub-word features so rare words are not simply unknown; and (c) calibrating the decision threshold for MCC on held-out training data rather than taking a default 0.5. The whole task fits comfortably on CPU: the reference solution trains in a few minutes on 10 cores.
> What not to use
> No internet access. Use only libraries already present; you cannot download packages, pretrained weights, or embeddings.
> No external parsers, taggers, or treebanks (spaCy, Stanza, UDPipe, the CoNLL-2018 outputs, UD releases, …). The task is to predict parser disagreement, not to reproduce it by running parsers.
> No hardcoded per-token_id answers. token_id, sentence_id and position are opaque and carry no signal — a model that reads them scores 0.000. Predictions must come from the words.
> Benchmark details
> Every figure below is this challenge's metric (MCC) on the shipped, document-disjoint test split — it shows how far apart the trivial and the genuine solutions sit.
> Regime | Method | MCC
> Floor | constant (all settled / all contested), random valid labels | 0.000
> Leakage probes | model on token_id / position / sentence_id only | 0.000
> Shortcut boundary | "rare word ⇒ contested" frequency lookup | 0.149
> Shortcut boundary | per-word-form majority-label lookup | 0.124
> Achievable frontier | context model (surrounding words) → linear classifier | 0.218
> Achievable frontier | from-scratch char-aware BiLSTM tagger (reference) | 0.258
> Open frontier | anything above the reference | > 0.258
> The lower boundary is hard. Every method that ignores context — a constant, an id/position model, or a pure word-identity lookup — is pinned at ≤0.15; only calibrated, context-aware models move the score.
> The upper frontier is open. The reference is far below 1, and better modelling of the structural context that makes a particular occurrence ambiguous has real room to climb; the reference itself varies 0.239–0.277 across seeds.
> Construction. Labels are built once, offline, by collating the 25 parser analyses and marking a token contested when more than 15% of them disagree with the plurality head; the split is document-disjoint (no near-duplicate sentence is shared); token_id/sentence_id are assigned after the split and shuffled; the reference trains from scratch in a few minutes on 10 CPU cores.

Inspiration note: Useful because it frames parser disagreement as a from-scratch CPU text/feature-engineering task, using linguistic ambiguity signals rather than pretrained NLP models.

## Geological Cohort Partition Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bn3ccdbz80ra77g4wdsvyhn8atgmw
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> Latent Provenance Cohort Partition
> Overview
> This is a from-scratch modelling task. You are given panels of mineral specimens, each specimen
> described only by a coarse composition signature (eight small integer bins). Every specimen formed in
> one of several hidden geological provenance cohorts (its source setting), and the specimens in a panel
> were drawn from a handful of those cohorts. Nowhere are you told a specimen's cohort. Your job is to
> recover, for each panel, the hidden partition of its specimens into cohorts - expressed as a
> co-provenance affinity for every pair of specimens (how likely two specimens share a cohort). You must
> build and train a model from scratch - no pretrained or foundation model knows this mapping; the link
> between coarse composition and provenance cohort must be learned entirely from the provided training
> examples.
> What the records represent (real-world scenario). Each specimen is a mineral grain, described by the
> coarse-binned amounts of eight major oxides. A grain's chemistry is shaped by the geological setting it
> formed in, so composition carries a provenance signal - but only statistically and non-linearly: at
> the coarse resolution served, each composition cell holds a mixture of settings, so no fixed formula or
> single-threshold rule reads a specimen's provenance from its composition. The provenance is inferred in
> aggregate, never read off, and even a strong model recovers only part of each partition.
> The decision object. Each instance is one panel: K = 16 anonymous specimens drawn from
> G in {3, 4, 5} latent cohorts (G is given per panel), roughly K/G specimens per cohort, each specimen
> from a distinct source group, order independently shuffled, item ids 0..15. For every unordered pair
> (i, j) you submit a co-provenance affinity in [0, 1] - your predicted probability that specimens
> i and j came from the same cohort. The grader reads this soft affinity matrix and scores how well
> it recovers the partition, both as a pairwise ranking and as the induced grouping. You are not
> labelling cohorts (labels are arbitrary - the scoring is fully partition/label-invariant) and not
> classifying each specimen; you are recovering a cohort partition.
> Why it is hard. Every panel is biased toward the confusable metamorphic cluster of settings, whose
> composition ranges overlap heavily, and the served signature is deliberately coarse and mixture-filled.
> A single-feature or linear separation folds these overlapping cohorts together; only a model that has
> learned the non-linear, aggregate composition->provenance regularities from the training pool can pull
> them apart, and even then the partition is only partly recoverable - so the achievable score is well short
> of a perfect reconstruction.
> Provenance and scientific grounding
> The specimens are real mineral-composition measurements - genuine analytical records, not synthetic.
> That a detrital mineral's major-element composition discriminates its source-rock setting is a
> standard provenance principle in sedimentary petrology (see Morton & Hallsworth (1999), "Processes
> controlling the composition of heavy mineral assemblages," Sedimentary Geology 124). Recovering a
> partition from a pairwise affinity is scored by two established, chance-corrected measures: the Adjusted
> Rand Index (Hubert & Arabie (1985), "Comparing partitions," Journal of Classification 2) applied to
> a deterministic normalized-cut spectral grouping (Ng, Jordan & Weiss (2002); von Luxburg (2007),
> "A tutorial on spectral clustering," Statistics and Computing 17), together with a pooled
> pairwise-ranking skill (Mann-Whitney / Somers' D). The challenge adapts this real measurement corpus
> and these methods into a single partition-recovery task; the exact signature construction and cohort
> assignment are applied author-side, and the full source citation is documented with the accompanying
> dataset (not needed to solve the task).
> The served signature (per specimen)
> Each specimen is shown only as a coarse composition signature - eight small integer bins, one per major
> oxide, standardised and quantised on the training pool:
> feature values meaning
> f0 integer 0..3 coarse bin of (log) oxide 1
> f1 integer 0..3 coarse bin of (log) oxide 2
> f2 integer 0..3 coarse bin of (log) oxide 3
> f3 integer 0..3 coarse bin of (log) oxide 4
> f4 integer 0..3 coarse bin of (log) oxide 5
> f5 integer 0..3 coarse bin of (log) oxide 6
> f6 integer 0..3 coarse bin of (log) oxide 7
> f7 integer 0..3 coarse bin of (log) oxide 8
> There is no provenance label, no raw concentration, and no source id in the served panels - those are the
> latent quantities you infer. The bins are coarse by design: each (f0..f7) cell holds a mixture of
> provenance cohorts, so a composition lookup gives at best a cohort distribution, never a cohort. Only a
> model that has learned which composition regions are enriched in which cohort (from the training pool)
> can turn the signature into useful co-provenance affinities.
> Data
> public/ contains a labelled training pool and the test panels (a hidden private/answers.csv is held by
> the grader):
> file rows columns
> train/analyses_train.csv 5555 unit_id, f0..f7, setting (7-class provenance label)
> train/panels_train.csv 11200 panel_id, item_id, f0..f7, group_label
> train/panels_train_meta.csv 700 panel_id, n_groups
> test/panels_test.csv 6400 panel_id, item_id, f0..f7
> test/panels_test_meta.csv 400 panel_id, n_groups (G)
> sample_submission.csv 48000 panel_id, i, j, affinity
> train/analyses_train.csv - a flat pool of 5555 labelled specimens: its signature (f0..f7)
> and its latent provenance setting (one of seven cohorts: AM, BS/GS, EC/UHP, GR, IG,
> MA, MS). This is your core training material - learn, from scratch, how the coarse signature maps to
> provenance. The training specimens come from different source groups than the test panels (a
> group-disjoint split), so you must generalise, not memorise.
> train/panels_train.csv - 700 training panels of K = 16 specimens with their cohort partition
> revealed (group_label in {0..G-1}, panel-local), so you can train and validate the full
> signature -> affinity -> partition pipeline end to end.
> test/panels_test.csv - 400 test panels of K = 16 specimens (signatures only). The partition is
> withheld. panels_test_meta.csv gives the number of cohorts G per panel.
> sample_submission.csv - a valid template (all C(16,2) = 120 pairs per test panel). It is a weak
> public-only starter; replace its affinity column with your model's output.
> Column data types:
> column type description
> unit_id string opaque specimen id (train only; carries no information)
> panel_id string opaque panel id, e.g. pn_a1b2...
> item_id, i, j integer 0..15 specimen slot within a panel
> f0..f7 integer 0..3 the coarse composition signature
> setting string provenance cohort (train analyses only)
> group_label integer 0..G-1 panel-local cohort id (train panels / answers only)
> n_groups integer {3,4,5} number of cohorts G in the panel
> affinity float [0,1] your predicted co-provenance probability for a pair (submission)
> Submission
> Submit a CSV with a header and one row per unordered pair (i, j) of every test panel - columns
> panel_id, i, j, affinity:
> panel_id,i,j,affinity
> pn_a1b2c3d4,0,1,0.82
> pn_a1b2c3d4,0,2,0.10
> pn_a1b2c3d4,1,2,0.71
> ...
> pn_a1b2c3d4,14,15,0.33
> For each panel with K = 16 specimens provide all C(16,2) = 120 pairs (so 400 x 120 = 48 000 rows).
> Only the relative order and the block structure of affinity matter - higher = more likely same
> cohort. A submission that omits a required column raises a ValueError; a duplicate (panel_id, i, j) raises a ValueError. A missing pair is treated as affinity 0; a non-finite affinity is treated
> as 0. Out-of-range or unknown ids are ignored.
> How the submission is scored
> In practical terms. The score is one number in [0, 1], higher is better. It measures how well your
> affinities recover the hidden cohort partition - judged two ways at once: (A) do same-cohort pairs get
> higher affinity than different-cohort pairs (pooled over all panels)? and (B) does the grouping implied by
> your affinity matrix match the true partition? A constant, random, or all-equal affinity scores ~0;
> because the signature is coarse and the cohorts confusable, a strong learned model lands around ~0.25-0.35
> and the weak public baseline sits near ~0.015. No non-exact submission reaches 0.6 - the response is
> capped at 0.55. The exact recipe:
> Submissions are scored by a single deterministic grade(submission, answers) -> float (numpy / pandas
> only). For each panel the grader assembles your affinities into a symmetric K x K matrix S
> (missing/non-finite -> 0).
> Facet A - pooled pairwise co-membership rank-skill. Pool every unordered pair of every panel; a pair is
> positive if its two specimens share a cohort, negative otherwise. Take the deterministic Mann-Whitney
> (midrank) AUC of S separating positives from negatives:
> A_raw = P(S_pos > S_neg) + 0.5 * P(tie)
> A = clip(2 * A_raw - 1, 0, 1)
> Facet B - partition recovery (adjusted Rand). Per panel, induce a hard partition from S by a
> deterministic normalized-cut spectral clustering into G groups (a fixed per-panel seed drives a
> deterministic k-means on the Laplacian embedding), then score it against the truth with the
> Adjusted Rand Index:
> B_p = max( AdjustedRandIndex(truth_p, spectral(S_p, G)), 0 )
> B = mean over panels of B_p
> Fuse + ramp.
> M     = sqrt(A * B)
> M'    = clip((M - DB) / (1 - DB), 0, 1)
> score = 1.0 if A >= 1-EPS and B >= 1-EPS
> = min(CEIL, M'^POW) otherwise
> Constants (identical to grade.py):
> CEIL = 0.55
> DB   = 0.02
> POW  = 2.0
> EPS  = 1e-9
> Properties
> Perfect - affinities that exactly separate the cohorts on every panel (A = 1, B = 1) -> 1.0.
> No-skill - a constant, all-equal, or random affinity -> A ~= 0 (no pooled ranking skill) -> M = 0 ->
> 0.0 exactly (the geometric mean guarantees it regardless of B; the dead-band absorbs residual noise).
> What not to use
> You must solve this with a model trained from scratch on the provided training pool that maps a
> specimen's coarse composition signature to its provenance, turned into co-provenance affinities.
> Submissions that reach the answer by non-ML means are rejected.
> Banned - all rule-based / non-learned approaches.
> No hand-written rules, fixed formulae, hard-coded thresholds, hand-authored decision trees, discriminant
> diagrams, or heuristics that map a signature (or a pair of signatures) to an affinity by a fixed recipe.
> In particular, a fixed "same/similar composition bin => same cohort" rule, a single-oxide threshold, or
> a nearest-centroid/nearest-neighbour label rule is prohibited - the bins are coarse and cohort-mixed,
> so which composition regions belong to which provenance can only be learned from the training pool,
> not computed. (A hand-rule and a purely linear model both score far below a learned non-linear model here,
> by construction.)
> No constant, near-constant, all-equal, or id-derived affinity - the same value for every pair, or
> anything parsed from the opaque panel_id / unit_id or from slot indices. These carry no ranking skill
> and are scored to ~0.
> No manual / human labelling of the test specimens, and no outsourcing the partitioning to an
> annotation service.
> Banned - source lookup & label recovery (disqualifying).
> Re-identifying or matching a served specimen against any external mineral-composition / geochemistry
> dataset, archive, repository, or search engine - by its signature, its oxide bins, or any fingerprint - to
> read off its provenance setting or the panel partition. The signature is coarsened and quantised on a
> private split, specimens are drawn from a private subsample, source groups are hashed to opaque ids,
> and the split is group-disjoint, specifically to prevent this. (Even an attacker holding the full public
> source recovers far less than an honest model trained on the provided pool.)
> Retrieving the target (provenance / partition) from an external dataset, API, or service, and
> reverse-engineering the label pipeline to recompute it instead of learning it.
> Cached / hard-coded / memorised partitions or provenance labels of any kind.

Inspiration note: Useful because it turns provenance recovery into a pair-affinity partition task, which is a strong from-scratch challenge pattern with structured outputs and a nontrivial scoring design.

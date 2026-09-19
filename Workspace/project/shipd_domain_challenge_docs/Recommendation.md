# Recommendation Challenge Examples

Scrape timestamp: 2026-07-02T00:00:00+05:30

Confirmed examples in this document: 8

These entries are included because the challenge detail page displayed this domain. Titles were not used for classification.

## Mailshot Early-Response Priority Ranking
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72vbmh3svrdqp7hnvf3pxyt189tpvq
- DOMAIN exactly as displayed: Recommendation
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> You are given anonymized interaction histories from a recurring outbound email system. Each row represents one candidate recipient for one future mailshot. Your task is to assign a numeric priority score to each candidate so that recipients most likely to open quickly are ranked near the top of each campaign list.
> The target is not simple open/no-open classification. Fast opens are more valuable than late opens, and the evaluation only rewards the top-ranked candidates within each campaign. Good solutions should model recipient history, response recency, and early-open propensity while respecting the chronological setup.
> Dataset
> File descriptions
> train.csv -- 178,210 candidate-recipient rows containing 11 input columns and the target variable response_grade. This is your labeled training data.
> test.csv -- 36,000 candidate-recipient rows containing the same 11 input columns, but without response_grade.
> sample_submission.csv -- A template showing the required submission format with id and response_score columns, filled with random baseline scores.
> Column descriptions
> id (string) -- Unique 12-character hex identifier for each candidate recipient row.
> campaign_code (string) -- Anonymized campaign identifier. Ranking is evaluated separately within each campaign.
> recipient_id (string) -- Stable anonymized recipient identifier. The same recipient may appear in multiple campaigns.
> campaign_serial (int) -- Relative chronological campaign index used for temporal validation.
> prior_sends (int) -- Number of earlier mailshots sent to this recipient before the current campaign.
> prior_open_count (int) -- Number of earlier mailshots this recipient opened.
> prior_fast_open_count (int) -- Number of earlier mailshots this recipient opened within 24 hours.
> prior_open_rate (float) -- prior_open_count / prior_sends.
> prior_fast_open_rate (float) -- prior_fast_open_count / prior_sends.
> fast_given_open_rate (float) -- prior_fast_open_count / prior_open_count; zero when the recipient has no prior opens.
> campaigns_since_last_open (int) -- Number of campaign steps since the recipient's most recent prior open; 999 means no prior open was observed.
> response_grade (int) -- Target variable in train.csv only. 2 means opened within 24 hours, 1 means opened later than 24 hours, and 0 means no open was observed.
> Evaluation
> Submissions are scored using campaign-averaged NDCG@50. Higher is better.
> For each campaign, candidates are sorted by your submitted response_score in descending order. Relevance gains are computed from hidden response_grade values using gain = 2 ** response_grade - 1, so fast opens receive the largest reward. The discounted cumulative gain for your top 50 ranking is divided by the ideal top 50 ranking for that campaign. The final score is the mean NDCG@50 across all test campaigns.
> import numpy as np
> def dcg_at_50(relevance):
> top = np.asarray(relevance[:50], dtype=float)
> gains = (2.0 ** top) - 1.0
> discounts = np.log2(np.arange(2, len(top) + 2, dtype=float))
> return float(np.sum(gains / discounts))
> def campaign_ndcg_at_50(true_grade, predicted_score):
> order = np.argsort(-np.asarray(predicted_score, dtype=float))
> ranked = np.asarray(true_grade, dtype=float)[order]
> ideal = np.sort(np.asarray(true_grade, dtype=float))[::-1]
> ideal_dcg = dcg_at_50(ideal)
> if ideal_dcg == 0:
> return 0.0
> return dcg_at_50(ranked) / ideal_dcg
> Submission
> Submit a CSV file with one score for every row in test.csv.
> id (string) -- The 12-character hex identifier from test.csv.
> response_score (float) -- Your priority score. Higher scores should indicate candidates you want ranked earlier within their campaign.
> Example:
> id,response_score
> 001c7cf18f75,0.73
> 00230243138d,0.18
> 00369f7e7f77,0.62
> Requirements
> The file must contain exactly 36,000 rows plus a header, one for each row in test.csv.
> Every id from test.csv must be present exactly once.
> All response_score values must be finite numeric values.
> File format: .csv only, with exact column names id,response_score.
> Allowed Methods
> Train ranking, regression, or classification models on train.csv.
> Engineer features from the public history columns in train.csv and test.csv.
> Use campaign-grouped validation and recommender-system metrics such as NDCG or average precision.
> What Not To Use
> Do not use external mirrors, public copies, public notebooks, or repository files for this email interaction log to recover held-out campaign outcomes.
> Do not map the anonymized row, campaign, or recipient identifiers back to non-public identifiers.
> Do not submit cached labels, hardcoded row-level answers, or scores tuned from repeated leaderboard probing.
> Do not use a purely hand-coded lookup table as the main prediction path; the intended task is ranking from learned or statistically estimated recipient-response behavior.

Inspiration note: Useful because it turns ranking and prioritization into an explicit ordered-output challenge with direct scoring.

## Film Genre Graph Recommendation
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74kgk30c5pe2drjdfgsa1cn189vw5m
- DOMAIN exactly as displayed: Recommendation
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↓ Lower is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> You are given anonymized film graph records. Each row contains opaque tokens for a film's surrounding graph facts: people, organizations, countries, languages, and locations connected to that film. Five candidate genre-link tokens are shown for the same film.
> Your task is to rank the five candidate genre tokens from most likely to least likely to be a true missing genre link for that film.
> This is a recommendation problem over a real entity graph. The public tokens are stable across train and test, so useful solutions can learn recurring relationships such as production context, creative teams, languages, and graph neighborhoods. The tokens are intentionally anonymized; the benchmark is about modeling the provided graph structure, not recognizing a public film record.
> Dataset
> File descriptions
> train.csv -- 2,262 labeled film-graph recommendation rows with anonymized context tokens, five candidate genre tokens, and the target target_option.
> test.csv -- 639 rows with the same input columns as train.csv, but without target_option.
> sample_submission.csv -- A template with the required id and option_order columns, filled with deterministic random rankings.
> Column descriptions
> id (string) -- Unique 12-character hexadecimal row identifier.
> year_bucket (string) -- Coarse release-year bucket token.
> context_tokens (string) -- Space-separated union of all anonymized graph context tokens for the film.
> director_tokens (string) -- Opaque tokens for connected director facts.
> cast_member_tokens (string) -- Opaque tokens for connected cast-member facts.
> country_of_origin_tokens (string) -- Opaque tokens for connected country facts.
> original_language_tokens (string) -- Opaque tokens for connected language facts.
> screenwriter_tokens (string) -- Opaque tokens for connected screenwriter facts.
> composer_tokens (string) -- Opaque tokens for connected composer facts.
> producer_tokens (string) -- Opaque tokens for connected producer facts.
> distributed_by_tokens (string) -- Opaque tokens for connected distributor facts.
> production_company_tokens (string) -- Opaque tokens for connected production-company facts.
> narrative_location_tokens (string) -- Opaque tokens for connected narrative-location facts.
> candidate_A (string) -- Candidate genre-link token A.
> candidate_B (string) -- Candidate genre-link token B.
> candidate_C (string) -- Candidate genre-link token C.
> candidate_D (string) -- Candidate genre-link token D.
> candidate_E (string) -- Candidate genre-link token E.
> target_option (string) -- Train-only correct candidate option label.
> Evaluation
> Submissions are scored using Genre Link Rank Loss. Lower is better.
> For each row, the hidden answer contains the correct candidate option. Your submitted order receives loss based on the rank of that option:
> def row_loss(order, target):
> rank_index = order.index(target)  # 0 for first place, 4 for last place
> return 100 * rank_index / 4
> The final score is the mean row loss, bounded from 0 to 100.
> Submission
> Submit a CSV file with one ranked option list for every row in test.csv.
> id (string) -- The row identifier from test.csv.
> option_order (string) -- A pipe-separated permutation of A, B, C, D, and E, ordered from most likely to least likely true genre link.
> Example:
> id,option_order
> 8fdca2bff7cb,D|C|E|A|B
> e4b2dbbe1683,D|C|E|A|B
> c104aa78ed60,A|D|B|C|E
> Requirements
> The file must contain exactly 639 rows plus a header.
> Every id from test.csv must appear exactly once.
> option_order must be a complete permutation of A|B|C|D|E.
> File format: .csv only, with exact column names id,option_order.
> What Not To Use
> Do not try to reverse-engineer opaque tokens back to public film, person, company, country, language, location, or genre records.
> Do not use external graph dumps, source identifiers, public entity pages, or cached lookup tables to recover hidden test links.
> Do not infer the answer from row order, generated token hashes, or candidate letter frequency; those are deterministic packaging details, not film evidence.
> Do not submit a fixed option order or a pure candidate-popularity rule as the main method; candidate sets include same-surface hard negatives, so graph context matters.

Inspiration note: Useful because it turns ranking behavior into an explicit ordered-output task with domain-specific loss.

## Geometry-Preserving Completion of a Sparse Phenotypic Trait Matrix
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78qqaavbthmh6amnqxz5rafd89z30z
- DOMAIN exactly as displayed: Recommendation
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> In brief: you are given a large, mostly-empty table of standardized measurements (rows =
> anonymized organisms, columns = standardized traits); for a set of rows, four specific columns are
> hidden, and you must fill them in — scored not on raw accuracy alone but on how faithfully your
> filled-in values reproduce the joint statistical structure of the hidden block. The data derive
> from a real, openly-licensed comparative-biology trait compilation (a curated database of
> whole-organism life-history measurements); the specific taxa, traits and cohorts are anonymized and
> the values standardized, so the task is solved from the matrix's internal structure rather than by
> identifying anything. The full scoring formula is in Scoring below.
> This challenge couples sparse low-rank matrix completion with a multivariate
> structural-fidelity estimand. The substrate is a sparsely-observed, standardized
> taxon × trait matrix — anonymized organisms as rows, standardized phenotypic life-history
> attributes as columns — supplied as (entity_id, channel_id, value) triples, the incomplete
> dyadic matrix canonical to collaborative filtering. For a designated cohort of taxa, a
> mutually-covarying tetrad of life-history coordinates is redacted; you must reconstruct
> those coordinates by exploiting the matrix's latent low-rank and allometric structure.
> The estimand is what distinguishes the task. Conventional completion is optimized under an
> elementwise (Frobenius / RMSE) loss; here the reconstruction is adjudicated by a composite
> structural-fidelity functional that requires the reconstructed sub-ensemble to preserve the
> multivariate geometry of the redacted block — its across-taxon rank order, its per-coordinate
> second moments (dispersion), the ordinary-least-squares allometric gradient on a scalar
> size covariate, the leading eigenvector of the block's empirical covariance operator, and the
> full inter-coordinate correlation structure — jointly with elementwise concordance. The
> estimand is therefore geometry-preserving inference: a completion that attains low RMSE while
> contracting dispersion, decorrelating the coordinates, or rotating the principal covariation axis
> is penalized. Low-rank / latent-factor completion, allometric regressors, neighbourhood
> collaborative filtering, and iterative conditional reconstruction all apply directly.
> Data
> train.csv                 # entity_id, channel_id, value        (observed matrix entries)
> test.csv                  # row_id, entity_id, channel_id        (redacted entries to reconstruct)
> entities.csv              # entity_id, cohort                    (per-taxon cohort covariate)
> sample_submission.csv     # row_id, value                       (deterministic-random baseline)
> A sparse matrix in edge-list (triple) form; taxa, traits and cohorts are opaque tokens and values
> are z-scored logarithms carrying a small anonymizing perturbation, so the array is solved from its
> internal covariance structure alone.
> Size: about 2,150 taxa × 28 traits; about 24,000 observed entries in train.csv;
> about 2,650 redacted entries (about 660 test taxa × their 4 redacted coordinates).
> train.csv — the observed matrix as (row, column, value) triples:
> entity_id — string; an anonymized taxon (a matrix row).
> channel_id — string; an anonymized standardized trait (a matrix column).
> value — float; the standardized (z-scored log, perturbed) entry.
> An (entity_id, channel_id) pair not present is an unobserved entry; the matrix is sparse.
> test.csv — the redacted entries to reconstruct: row_id (unique id), plus the entity_id
> and channel_id of the redacted coordinate. Each test taxon has its four target coordinates
> redacted.
> entities.csv — entity_id, cohort; the coarse anonymized taxonomic cohort of each
> taxon (a grouping covariate you may condition on).
> The size covariate s used by the S_ALLO scoring term. s is each taxon's standardized
> body-size. It is not a separate file: body-size is itself one of the observed trait columns,
> present in train.csv for every test taxon (only the four target coordinates are redacted), so the
> allometric size structure is fully available to you in the data. The grader references this
> body-size column (recorded per test taxon as ref_scalar in the private answer key) to evaluate
> S_ALLO; you never submit s — you only submit your reconstructed target values.
> sample_submission.csv — row_id, value, a deterministic-random placeholder. Edit value.
> Scoring — the composite structural-fidelity functional
> Scored in [0, 1] (higher is better). The grader marshals your reconstructed entries into an
> N × 4 coordinate matrix (each test taxon's four redacted coordinates). For target coordinate
> k let f_k, y_k, b_k be the vectors over test taxa of your value, the truth, and the
> baseline (each taxon's per-cohort median of that coordinate, from the observed entries). All
> values are in standardized (z-scored log) units.
> Constants: W_T = 0.04, POWER = 2.00, SCALE = 1.20, LAM = 0.30, BASE = 0.40,
> SCALE_D = 0.35, SCALE_B = 0.35, SCALE_A = 0.30.
> Stage 1 — the point-concordance gate (skill over the per-cohort baseline). For each of the
> four coordinates, two scaled-error skills, each 1 for an exact reconstruction and 0 for one no
> better than the per-cohort baseline; averaged over the four:
> S_MAE_k  = clip( 1 −  Σ_i|f_k − y_k| / Σ_i|b_k − y_k| ,                 0, 1 )
> S_RMSE_k = clip( 1 −  sqrt( Σ_i(f_k − y_k)² / Σ_i(b_k − y_k)² ) ,       0, 1 )
> point    = mean_k [ 0.5·S_MAE_k + 0.5·S_RMSE_k ]
> point multiplies the structural terms, so a reconstruction no better than the baseline at
> recovering the levels — including a random or constant submission — is annihilated regardless of
> its geometry.
> Stage 2 — six structural-fidelity terms, each in [0, 1] and 1 for an exact reconstruction,
> quantifying preservation of the reconstructed cloud's multivariate geometry:
> S_RANK = mean_k clip( spearman(f_k, y_k), 0, 1 )                        # across-taxon rank order
> S_DIST = mean_k exp( −|std(f_k) − std(y_k)| / SCALE_D )                 # per-coordinate second moment
> S_BIAS = mean_k exp( −|mean(f_k − y_k)| / SCALE_B )                     # first-moment (offset) fidelity
> S_ALLO = mean_k exp( −|slope(f_k on s) − slope(y_k on s)| / SCALE_A )   # OLS allometric gradient on covariate s
> S_PACE = clip( pearson( F·v₁ , Y·v₁ ), 0, 1 )                          # leading covariance eigenvector (below)
> S_COV  = clip( 1 − mean_offdiag |corr(F) − corr(Y)| , 0, 1 )           # inter-coordinate correlation operator
> slope(f_k on s) is the ordinary-least-squares gradient of reconstructed coordinate k on the
> taxon's standardized size covariate s (the body-size described above).
> F, Y are the N×4 reconstructed and true coordinate matrices; v₁ is the leading
> eigenvector of Y's empirical covariance operator (the dominant covariation axis). corr(·) is
> the 4×4 coordinate correlation matrix.
> Blended (arithmetic mean for robustness, geometric mean to demand competence on every axis):
> shape = (S_RANK + S_PACE + S_COV) / 3
> dyn   = (S_DIST + S_ALLO) / 2
> calib = S_BIAS
> aux_a = 0.50·shape + 0.30·dyn + 0.20·calib
> aux_g = ( max(shape,1e−6) · max(dyn,1e−6) · max(calib,1e−6) ) ^ (1/3)
> aux   = (1 − LAM)·aux_a + LAM·aux_g
> Stage 3 — modulate, floor, shape. The structural fidelity modulates the gated concordance; a
> transcendental tolerance term keeps a trivial submission strictly positive:
> comp  = point · ( BASE + (1 − BASE)·aux )
> TOL   = mean over all redacted entries of  exp( −|value − truth| / SCALE )
> score = clip( (1 − W_T)·comp^POWER  +  W_T·TOL ,  0,  1 )
> An exact reconstruction → point = 1, every structural term = 1 → comp = 1 → 1.0. A
> reconstruction no better than the per-cohort baseline → point = 0 → comp = 0. Earning score
> requires beating the baseline on the levels and reproducing the across-taxon rank order,
> dispersion, offset, allometric gradient, dominant covariation eigenvector and inter-coordinate
> correlation operator.
> Reproducing the score locally. The functional is a pure function of your reconstructed
> values versus the truth (the baseline is each taxon's per-cohort median; the S_ALLO term uses
> the taxon's standardized body-size as its covariate). Redact the four target coordinates for part
> of the observed matrix, compute per-cohort medians from the rest, use the body-size column as the
> covariate, and apply the same formula.
> Submission Format
> Submit a CSV with exactly these columns — row_id, value — one row per row_id in test.csv
> (the provided sample_submission.csv already has this format — edit value):
> row_id — string; the redacted-entry identifier from test.csv (must match exactly).
> value — a finite real number; your reconstructed standardized value for that coordinate.
> Requirements (a submission that violates any of these is rejected): columns row_id, value
> present (and only these two); the row_id set matches test.csv exactly (no missing, extra or
> duplicate ids); every value finite; header row included.
> What Not To Use
> Solvers must solve this with machine learning (a trained completion / reconstruction
> model). The reconstructed values must come from a model fitted on the provided observed entries
> and reading each test entity's observed channels. Submissions that reach the answer by non-ML
> means will be rejected.
> Not allowed
> Non-ML / "raw logic" solutions. No hand-written rules or fixed formulas. In particular,
> submitting the per-cohort baseline (each entity's cohort median), a constant, a
> global mean, or any value that ignores the entity's own observed channels is a non-ML shortcut
> and is prohibited — the per-cohort baseline is exactly the reference the metric measures the
> skill over, and beating it requires learning the cross-channel relationships.
> Re-identifying the array / external retrieval. Entity and channel identifiers are opaque
> tokens, the cohort is an opaque partition label, and the values are standardized (z-scored log)
> with an irrecoverable per-cell perturbation added, so nothing is directly identifiable and
> the exact values cannot be recovered even in principle from an outside source. Do not attempt
> to re-identify what real objects the rows, columns or values correspond to (from the value
> pattern, the distribution, or any side information) in order to retrieve the redacted entries
> from any external database, published table, corpus or search engine. The task is to
> reconstruct the redacted entries from the provided array, not to look them up.
> Matching the array back to a source. Do not fingerprint, de-standardize, or align the
> provided values against any external dataset to recover the redacted entries.
> Hard-coding or memorising the answer. Do not embed a table of values or per-entry predictions
> looked up offline. Every reconstructed value must be produced by the model from the observed
> array at inference time.
> External label sources keyed to these specific rows or columns.
> Allowed
> Standard modelling tooling: missing-value handling, feature engineering, scaling, regularisation,
> cross-validation, multi-output modelling and ensembling.
> General world knowledge about how structure-preserving completion works (that the channels
> co-vary along a dominant contrast, that they share a gradient against the scalar covariate, that
> entities in a cohort are similar) applied to the provided data. This is method knowledge, not
> answer lookup.
> The rule of thumb: the values you submit must come from a trained model that reconstructs each
> redacted entry from the observed array — not from a constant, the per-cohort baseline,
> re-identifying the array, or retrieving the answer from an outside source.

Inspiration note: Useful because it frames ranking, completion, or choice prediction around sparse context and a leaderboard-friendly utility metric.

## Constraint-Aware Session Bundle Recommendation
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a0xgppncte2ayttnmgtzvkx89xta7
- DOMAIN exactly as displayed: Recommendation
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Operational teams often recommend the next best artifact, checklist, routing action, or support module from a constrained candidate set. The best recommendation depends on user history, request context, item metadata, budget and latency limits, risk tags, and channel compatibility.
> This challenge is a synthetic recommendation benchmark generated by a deterministic local script. The generator creates a catalog of operational items with category, action style, preferred channel, risk tag, region bias, latency, cost, and reliability. It also creates synthetic users with repeated historical preferences. For every query, the generator samples a user, request urgency, channel, region, latency cap, budget cap, recent item history, and a set of 20 candidate items. The hidden target is the item selected from the top of a noisy latent utility model. Public files do not expose latent vectors, hidden scores, raw ids, or private split metadata.
> Your task is to rank the candidate items for each test query and place the true next item as high as possible in the top five recommendations.
> Evaluation
> Submissions are scored using MAP@5 with one relevant item per query. Higher is better.
> score_i = 1 / rank_of_true_item   if the true item appears in ranks 1..5
> score_i = 0                       otherwise
> The final score is the mean of score_i over all test queries. Submission rows are validated strictly: empty recommendation strings, malformed item ids, duplicate recommendation tokens, more than five item ids, and item ids outside that row's candidate set are invalid and will raise an error.
> Dataset
> The prepared dataset contains:
> public/item_catalog.csv - public item metadata.
> public/train.csv - labeled historical recommendation queries.
> public/test.csv - unlabeled held-out queries.
> public/sample_submission.csv - valid dummy-format predictions.
> item_catalog.csv columns:
> item_id (string): public item identifier.
> item_name (string): synthetic item name.
> category (string): item category.
> action_style (string): item action family.
> preferred_channel (string): channel where the item usually performs best.
> risk_tag (string): operational risk marker.
> region_bias (string): region where the item tends to be useful.
> latency_minutes (int): expected handling latency.
> unit_cost (float): synthetic cost.
> reliability (float): synthetic reliability estimate.
> train.csv columns:
> id (string): query identifier.
> user_id (string): public user identifier shared across train and test.
> urgency (string): request urgency.
> request_channel (string): channel for this recommendation.
> region (string): request region.
> max_latency_minutes (int): latency cap for acceptable items.
> budget_cap (float): budget cap for acceptable items.
> primary_category_hint (string): user's strongest historical category.
> secondary_category_hint (string): user's secondary historical category.
> recent_item_ids (string): pipe-separated recent public item ids.
> candidate_item_ids (string): pipe-separated candidate item ids for this query.
> target_item_id (string): training label.
> test.csv has the same public input columns except target_item_id.
> Submission
> Submit a CSV named submission.csv with exactly these columns:
> id: query identifier from test.csv.
> recommended_items: up to five item ids ordered from best to fifth-best.
> Example CSV:
> id,recommended_items
> qry_0017a4bc,itm_0aa1b233 itm_4c98dd02 itm_8be013af itm_f102ac77 itm_21bc09de
> qry_03cc92ad,itm_9fa03c1e itm_1200bbfa itm_a8910cdd itm_008ab319 itm_dd0c4fe2
> qry_0821de44,itm_777e1a03 itm_201a10cd itm_19fb4d10 itm_bca99002 itm_8931ab61
> Requirements:
> Exactly one row per test query.
> Include the header row.
> No missing, duplicate, or unexpected id values.
> Recommend at most five item ids per row.
> Every recommended id must be well-formed, unique within the row, and present in that row's candidate_item_ids.
> Recommendation strings may separate ids with spaces, commas, pipes, or semicolons.
> Empty recommendation strings are invalid.
> Do not include scores, explanations, markdown, or extra columns.
> What Not To Use
> Do not use hidden targets, hidden utility scores, raw ids, private files, or any data outside the downloadable public files.
> Do not infer answers from row order, id ranges, sample-submission constants, or split position.
> Do not hard-code per-id predictions or manually label test queries.
> Do not use external datasets, web searches, hosted inference APIs, downloaded packages, or extra recommendation corpora.
> Modeling Guidance
> Strong approaches may combine candidate expansion, item metadata features, user-history aggregates, collaborative filtering over user_id, learning-to-rank style models, and constraint-aware reranking. A global popularity rule should score poorly because each query has its own candidate set and constraints; a better model must learn how context, history, item metadata, and candidate competition interact.

Inspiration note: Useful because it frames ranking, completion, or choice prediction around sparse context and a leaderboard-friendly utility metric.

## Independent Local Token Evidence Selection
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71d7qpyxbw09s30rqxxd3tvh89sw3b
- DOMAIN exactly as displayed: Recommendation
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, generative
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Many production text systems must decide which short evidence snippets support an information need without exposing raw documents. Examples include compliance review, incident monitoring, search-quality auditing, and newsroom triage, where sensitive source text may be converted into privacy-preserving token sketches before modeling.
> In this challenge, each row represents one anonymized retrieval case. You receive:
> a query sketch containing anonymous local tokens;
> 16 candidate evidence-card sketches;
> training labels showing which cards support the query.
> Your goal is to submit the card IDs for the three evidence cards that independently support each test query. The task is intentionally not source lookup, sentence ordering, or clique recovery. Strong solutions should learn query-card relevance from the supplied training rows.
> The released files are transformed from a permissively licensed public text corpus. Solver-facing data omits original text, source row identifiers, sentence boundaries, sentence counts, sentence lengths, and stable cross-row token identities.
> Target Semantics
> Each sample has exactly 16 candidate evidence cards:
> card IDs are c00, c01, ..., c15;
> each query has exactly 28 space-separated local token IDs;
> each evidence card has exactly 52 space-separated local token IDs;
> local token IDs match the pattern uNNN, such as u017;
> token IDs are local to one row only, so u017 in one row is unrelated to u017 in another row;
> exactly three cards are true supporting evidence cards.
> The hidden target for each test row is an unordered set of three card IDs. The submitted target_sequence may list one, two, or three distinct card IDs. Submitting fewer than three IDs is valid, but it is usually penalized through lower recall because every row has three true target cards.
> Evaluation
> The metric is mean order-independent set F1. Higher is better. The score is bounded from 0 to 1.
> For each row:
> P = set of submitted card IDs
> T = set of three true card IDs
> precision = |P ∩ T| / |P|
> recall = |P ∩ T| / |T|
> F1 = 2 * precision * recall / (precision + recall)
> Submissions must contain at least one card ID for every row, so |P| > 0. Since every answer has exactly three true cards, |T| = 3. If there are no correct submitted cards, then |P ∩ T| = 0 and the row F1 is defined as 0.
> The final leaderboard score is the arithmetic mean of row F1 over all test rows. Card order is ignored; c02 c09 c14 and c14 c02 c09 receive the same score.
> Dataset
> The preparation script produces the following structure:
> public/
> train.csv
> test.csv
> sample_submission.csv
> metadata.json
> private/
> answers.csv
> Files
> train.csv is public and has 22,000 rows. Columns are sample_id, query_tokens, evidence_cards, and target_sequence.
> test.csv is public and has 5,500 rows. Columns are sample_id, query_tokens, and evidence_cards.
> sample_submission.csv is public and has 5,500 rows. Columns are sample_id and target_sequence.
> metadata.json is public and contains dataset constants plus preparation notes.
> answers.csv is private and has 5,500 rows. Columns are sample_id, target_sequence, and positive_count.
> generate_dataset.py is included in the uploaded archive for reviewer reproducibility. It is not copied into the prepared public dataset by prepare.py.
> Column definitions
> sample_id is a string row identifier. Prepared training IDs start with train_; prepared test IDs start with test_.
> query_tokens is a string containing exactly 28 space-separated local token IDs. Each token has the form uNNN, for example u017.
> evidence_cards is a string containing exactly 16 card blocks. Card blocks are separated by a double-pipe delimiter. Each block starts with a card ID such as c04: followed by exactly 52 space-separated local token IDs.
> target_sequence is a string containing card IDs separated by spaces. In train.csv and private answers.csv, it contains exactly three distinct target card IDs. In submissions, it may contain one to three distinct card IDs.
> positive_count is an integer in private answers.csv. It is always 3.
> Metadata fields
> metadata.json includes these fields: version, task_type, source_license, source_transformation, train_rows, test_rows, cards_per_sample, positive_cards_per_sample, query_tokens_per_sample, tokens_per_card, source_entity_overlap_between_train_test, prepared_public_transform, prepared_id_format, prepared_train_rows, and prepared_test_rows.
> Submission
> Submit a CSV with exactly these columns in this order:
> sample_id,target_sequence
> test_7e3b8c9a4b14,c02 c09 c14
> test_91aa04d33f20,c00 c05 c12
> Rules:
> include every sample_id from test.csv exactly once;
> do not include training IDs;
> target_sequence must contain one to three distinct card IDs;
> valid card IDs are c00 through c15;
> duplicate card IDs in a row are invalid;
> order does not matter for scoring.
> Restrictions
> Use only public challenge files and allowed Kaggle-runtime libraries. Do not use private answers, source lookup, external data matching, row-order shortcuts, file-order shortcuts, hardcoded test labels, or hidden metadata. Legitimate methods may train on train.csv and infer query-card relevance from the public token/card structure.

Inspiration note: Useful because it frames ranking, completion, or choice prediction around sparse context and a leaderboard-friendly utility metric.

## Wikipedia Link Recommendation Ranking
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a8acnn5nc7wnt92ybmhb3j989vbgx
- DOMAIN exactly as displayed: Recommendation
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↓ Lower is better
- Tags: Not shown/captured
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> You are given anonymized Wikipedia navigation recommendation cases. Each case has one source page and a slate of five candidate destination pages. Your task is to recommend the candidate destination most likely to show the strongest momentum-adjusted next-month demand, then rank the remaining candidates.
> The target is not raw popularity. Training labels use:
> adjusted_score = log1p(next_month_clicks) - 0.75 * log1p(current_month_clicks)
> The correct option for a case is the candidate with the highest adjusted score. Lower evaluation scores are better.
> Dataset
> File descriptions:
> train.csv: One row per training recommendation case, with anonymized source-page ID, language, a JSON candidate slate, and the correct training option.
> test.csv: One row per test recommendation case, with anonymized source-page ID, language, and a JSON candidate slate. Targets are omitted.
> sample_submission.csv: A valid random submission with one row per test case.
> Column descriptions:
> id: Recommendation case identifier. Each id appears once in train.csv and test.csv.
> source_id: Anonymized source-page identifier.
> language: Wikipedia edition code.
> candidate_options: JSON list of five candidate destination objects. Each object has an option label, a salted candidate_id, and historical recommendation signals.
> target_option: Training-only label for the winning candidate option.
> target_adjusted_scores: Training-only JSON object with adjusted demand scores for the five candidates.
> Candidate slate fields:
> option: Candidate label, one of A, B, C, D, or E.
> candidate_id: Anonymized candidate destination identifier.
> signals: Binned and ranked historical navigation evidence for that candidate, including pair history, source-page outbound activity, candidate inbound activity, and within-slate ranks.
> Evaluation
> Submit a complete recommendation ordering of the five candidate options for every test case. The grader computes weighted rank loss:
> loss_for_case = 100 * rank_index_of_true_option / 4
> final_score = weighted_average(loss_for_case)
> The true option ranked first receives 0 loss for that case. The true option ranked last receives 100 loss for that case. Case weights are based on hidden next-month traffic volume.
> Submission
> Submission columns:
> id: Test case identifier.
> option_order: A pipe-separated permutation of A|B|C|D|E, ordered from most likely winner to least likely winner.
> Example:
> id,option_order
> nav_00d0c20fa432f0,B|C|A|E|D
> nav_00f90de01d7554,B|C|D|A|E
> nav_01be414ff0b688,A|C|D|B|E
> Requirements:
> Include exactly one row for every test id.
> Use exactly the columns id and option_order.
> Each option_order must be a valid permutation of A|B|C|D|E.
> Do not submit missing, duplicate, or extra IDs.
> Use only the provided public files. Do not use external Wikimedia Clickstream dumps, source-page reconstruction, reverse-mapping of anonymized IDs, or other source lookup to identify hidden test labels.

Inspiration note: Useful because it frames ranking, completion, or choice prediction around sparse context and a leaderboard-friendly utility metric.

## Polling Firm Bias Network Reconstruction
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74j54pn583pk3xs2ze74k8n98591h7
- DOMAIN exactly as displayed: Recommendation
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, small-data
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Polling averages fail when every firm is treated as equally trustworthy. Some firms have persistent house effects, some drift over a campaign, some publish copied or fabricated numbers, and some move together because they share hidden herding behavior rather than because they are measuring the electorate well.
> Your task is to build a pollster trust recommender. For each election, use the public poll observations to recommend the final outcome and a reliability profile for every polling firm: house effect, drift rate, fake-pollster flag, herding group, and methodology quality. The firm profiles act like item recommendations for an aggregator deciding which pollsters to trust, downweight, or group together.
> This is practical for polling aggregation and source-quality review. A useful aggregator should not only average results; it should recommend which firms are reliable, which firms are biased, which firms are copying each other, which suspicious firms should be downweighted, and which observed co-movement is just regional or sponsor-driven noise. Each test row contains 10-14 firms and roughly 150-400 poll observations, so the hidden task is hundreds of firm-level trust recommendations plus one aggregate outcome recommendation per election.
> The private split stresses recommendation generalization across new elections. Training examples include labeled firm profiles, while held-out elections include stronger regional co-movement, delayed releases, sponsor effects, adversarial fake pollsters, and directed 3-firm herding chains. Good solutions should learn firm reliability, source similarity, and trust-network structure rather than submit constant zero-bias profiles or independent per-firm averages.
> Dataset
> File descriptions
> train.csv -- 1,000 labeled elections. Each row contains public poll observations and the train-only ground_truth profile.
> test.csv -- 500 held-out elections with the same public input columns as train.csv, but without ground_truth.
> sample_submission.csv -- Submission template with the required election_id and analysis columns, filled with random valid JSON predictions.
> Column descriptions
> election_id (string) -- Unique 12-character hexadecimal election identifier.
> n_firms (int) -- Number of polling firms in the election, from 10 to 14.
> n_days (int) -- Campaign length in days.
> polls (string) -- JSON array of poll observations for the election.
> ground_truth (string) -- Train-only JSON target containing the true outcome and firm profiles.
> Poll observation fields
> firm_id (string) -- Firm identifier such as F00.
> day (int) -- Fieldwork end day used by the simulator's polling schedule.
> field_start_day (int) -- First day of the survey fieldwork window.
> field_end_day (int) -- Final day of the survey fieldwork window.
> release_day (int) -- Public release day, which may lag fieldwork and can reveal lead-lag copying.
> region (string) -- Synthetic polling region such as R0.
> sponsor_type (string) -- Sponsor category: nonpartisan, media, party_a, party_b, or interest_group.
> sample_size (int) -- Number of respondents.
> mode (string) -- Polling mode: phone, online, panel, or mixed.
> likely_voter_screen (boolean) -- Whether the poll used a likely-voter screen.
> result (float) -- Reported vote share for candidate A.
> margin_of_error (float) -- Reported sampling margin of error.
> Ground truth fields
> ground_truth.outcome (float) -- True final vote share for candidate A.
> ground_truth.firms (array) -- One profile object per firm.
> firm_id (string) -- Firm identifier matching the poll observations.
> house_effect (float) -- Signed systematic bias toward candidate A.
> drift_rate (float) -- Per-day change in the firm's house effect.
> is_fake (boolean) -- Whether the firm is a fake pollster.
> herding_group (int) -- Hidden herding cluster label. 0 means independent; shared positive integers indicate firms in the same herding group.
> quality_score (float) -- Methodology reliability score from 0.0 to 1.0.
> Evaluation
> Submissions are scored with a composite firm-recommendation score. Higher is better.
> herding_mult = 0.5 + 0.5 * max(0, adjusted_rand_index(pred_groups, true_groups))
> score = herding_mult * (
> 0.20 * outcome_score
> + 0.25 * bias_score
> + 0.20 * fake_score
> + 0.20 * drift_score
> + 0.15 * methodology_score
> )
> Component definitions:
> outcome_score = 1 - clip(abs(pred_outcome - true_outcome) / 0.07, 0, 1)
> bias_score = 1 - mean(clip(abs(pred_bias - true_bias) / 0.03, 0, 1))
> fake_score is F1 over fake-pollster labels.
> drift_score = 1 - mean(clip(abs(pred_drift - true_drift) / 0.001, 0, 1))
> methodology_score = 1 - mean(clip(abs(pred_quality - true_quality) / 0.25, 0, 1))
> The herding multiplier uses Adjusted Rand Index over herding-group assignments. Group 0 is treated as independent singletons, not as one shared cluster. A model that estimates individual firms but misses the network structure is scaled down.
> Submission
> Submit a CSV file with one row for every election in test.csv.
> election_id (string) -- The election identifier from test.csv.
> analysis (string) -- JSON object with one outcome prediction and one profile per firm.
> Example:
> election_id,analysis
> 56ac2c594181,"{""outcome"":0.523,""firms"":[{""firm_id"":""F00"",""house_effect"":0.018,""drift_rate"":-0.0003,""is_fake"":false,""herding_group"":1,""quality_score"":0.82}]}"
> 53e59f14f2ac,"{""outcome"":0.497,""firms"":[{""firm_id"":""F00"",""house_effect"":-0.006,""drift_rate"":0.0001,""is_fake"":false,""herding_group"":0,""quality_score"":0.74}]}"
> The firms array must contain every firm that appears in that election's polls JSON.
> Requirements
> Include exactly 500 rows plus the header.
> Use exactly the columns election_id,analysis.
> Every election_id from test.csv must appear exactly once.
> analysis must be valid JSON.
> Each firm profile must include firm_id, house_effect, drift_rate, is_fake, herding_group, and quality_score.
> No missing, empty, or NaN values.
> Write the final file to ./working/submission.csv.
> What Not To Use
> Do not hard-code recommendations by election_id, row order, poll JSON hash, or sample-submission values.
> Do not treat firm IDs such as F00 as the same real pollster across elections. Firm IDs are local to each election, so memorizing train profiles by firm ID is not a valid trust model.
> Do not rely on a fixed profile template such as all firms having zero house effect, all firms being independent, one repeated quality score, or one fixed fake-pollster rate.
> Do not assign herding groups from firm index alone, such as always pairing adjacent firms or always placing every firm in one cluster.
> Do not use leaderboard probing to tune row-level labels, cluster IDs, or per-election constants for the held-out elections.

Inspiration note: Useful because it frames ranking, completion, or choice prediction around sparse context and a leaderboard-friendly utility metric.

## Multilingual Psychology Next-Click Recommendation
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx764xz0v6cbk8d8mgy309sa3x89tzjr
- DOMAIN exactly as displayed: Recommendation
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> You are given transformed multilingual psychology navigation records. Each recommendation query represents one psychology-related source page. For that source page, you receive exactly 160 candidate destination pages. Your task is to assign a ranking score to each candidate so that pages with stronger observed next-click behavior are ranked highest.
> This is a recommendation challenge, not classification or regression. The target is an implicit-feedback ranking signal derived from aggregate page-to-page navigation counts. Strong solutions should learn how language edition, masked page-title structure, psychology term hints, source activity, candidate popularity, and source-candidate term overlap affect the likelihood of a user moving from the source page to a candidate page.
> The solver-facing files use anonymized query and candidate identifiers. Original page titles are masked, and exact raw click counts are not included in the test rows. Candidate sets include many hard negatives: pages from the same psychology term family, high-popularity pages, and random same-language candidates that look plausible but were not observed as retained next-click targets for that query.
> Files
> public/train.csv contains labeled query-candidate examples.
> | Column | Type | Description |
> |---|---|---|
> | query_id | string | Anonymized source-page recommendation request identifier. |
> | candidate_id | string | Anonymized candidate destination identifier. |
> | wiki | string | Language-edition code. |
> | source_title_hint | string | Masked source page title. |
> | candidate_title_hint | string | Masked candidate page title. |
> | source_term_hints | string | Pipe-delimited psychology term hints found in the source title. |
> | candidate_term_hints | string | Pipe-delimited psychology term hints found in the candidate title. |
> | source_activity_bucket | string | Bucketed outgoing click activity for the source page. |
> | candidate_popularity_bucket | string | Bucketed incoming click activity for the candidate page in the source data. |
> | same_term_family | string | Whether the source and candidate share at least one psychology term hint. |
> | relevance | integer | Training label: 0 for unobserved candidate, 1-3 for increasing observed click strength. |
> public/test.csv contains the same columns as train.csv except relevance. Every test query has exactly 160 candidate rows.
> public/sample_submission.csv shows the required submission format using random finite placeholder scores.
> public/data_dictionary.csv contains brief descriptions of the prepared solver-facing columns.
> Objective
> For every query_id, rank all candidate pages by expected next-click relevance. Higher submitted score values should correspond to candidates that are more likely to be clicked from the source page.
> Good solutions should:
> rank observed high-click candidates above weak or unobserved candidates;
> learn separate behavior patterns across language editions;
> use masked title structure without relying on exact source titles;
> combine global candidate popularity with query-specific source and term features;
> handle multilingual psychology terms and sparse implicit feedback;
> separate true next-click targets from same-topic hard negatives;
> optimize the first position, the top three, and the top ten simultaneously;
> recover multiple relevant candidates rather than only the single most popular page;
> avoid treating the task as a single global popularity ranking.
> Intended Approach
> Recommended approaches include:
> training a learning-to-rank model such as LambdaMART, gradient boosted trees, or a neural ranker;
> building per-language validation folds grouped by query_id;
> engineering pairwise features from source and candidate title hints, psychology term hints, and popularity buckets;
> using collaborative-filtering style baselines over query-candidate interactions;
> calibrating scores per language edition so that candidates are comparable within each query group.
> Disallowed Methods
> Do not use external pageview, clickstream, search, or page-title lookup data to identify test rows.
> Do not reverse-match masked titles to original pages.
> Do not hardcode predictions by query_id or candidate_id.
> Do not use candidate order in test.csv as a signal; rows may be sorted for file stability rather than recommendation strength.
> General pretrained models and public multilingual text knowledge are allowed as long as they are not used to recover exact source page identities or unavailable click counts.
> Evaluation
> Submissions are evaluated using a top-heavy blended ranking metric with language-balanced averaging. For each query_id, candidates are sorted by submitted score in descending order. Ties are broken deterministically by candidate_id.
> The relevance labels are:
> | Relevance | Meaning |
> |---:|---|
> | 0 | Candidate was not observed as a retained next-click target for this query. |
> | 1 | Candidate was observed with lower click strength. |
> | 2 | Candidate was observed with medium click strength. |
> | 3 | Candidate was observed with the strongest click strength for that query. |
> For one query and cutoff k:
> DCG@k = sum((2^relevance_i - 1) / log2(rank_i + 1)) for ranks 1..k
> IDCG@k = DCG@k of the ideal ranking for that query
> NDCG@k = DCG@k / IDCG@k
> The per-query score is:
> AP@10 = average precision over relevant candidates in the top 10
> query_score = 0.40 NDCG@10 + 0.25 NDCG@3 + 0.20 NDCG@1 + 0.15 AP@10
> The final score is:
> language_score = mean(query_score over all query_id groups in the same language edition)
> score = mean(language_score over language editions)
> The score ranges from 0 to 1, and higher is better. A perfect ranking receives 1.0. The NDCG@1 and NDCG@3 components make the challenge much stricter: it is not enough to place relevant pages somewhere in the top ten; the strongest candidates must be near the very first positions. The AP@10 component also rewards recovering several relevant candidates rather than only guessing one high-scoring page. The language-balanced averaging prevents a solution from winning by focusing only on the largest language edition.
> Submission Format
> Submit a CSV with exactly these columns:
> | Column | Type | Description |
> |---|---|---|
> | query_id | string | Must match one query-candidate row from test.csv. |
> | candidate_id | string | Must match one candidate for the corresponding query_id. |
> | score | float | Higher values mean the candidate should be ranked higher for that query. |
> Example:
> query_id,candidate_id,score
> q_008ab583c56cb3,c_0097b0f92eb569,0.312
> q_008ab583c56cb3,c_03d297f06ba3e4,0.774
> q_008ab583c56cb3,c_049b0b07c792b9,0.128
> Requirements:
> include exactly one row for each row in test.csv;
> do not include duplicate query_id, candidate_id pairs;
> do not add extra columns;
> all score values must be finite numbers;
> scores only need to be comparable within the same query_id.

Inspiration note: Useful because it frames ranking, completion, or choice prediction around sparse context and a leaderboard-friendly utility metric.

# CPU Recommendation Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed CPU examples in this document: 8

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.
## Hackage Missing Dependency Ranking

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dgy5eh0v5jw6k5awq5cc6b18b08ep
- DOMAIN exactly as displayed: Recommendation
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Be the first to climb the leaderboard!

### Full Challenge Description

> Hackage Missing Dependency Ranking
> Overview
> Build a CPU-only Haskell dependency-recovery ranker.
> For each test query, you are given a Hackage package metadata summary with one real direct dependency withheld. You are also given a fixed catalog of candidate Hackage packages. Your task is to rank the candidate packages so that the missing dependency appears as early as possible.
> This models a practical package-maintenance and developer-tooling problem. When a Cabal manifest is incomplete, stale, partially generated, or being migrated between build systems, a dependency assistant should suggest the likely missing library using the surrounding package text, dependency context, changelog language, and Haskell ecosystem conventions.
> The prepared task is harder than exact string search. Source package names and withheld target names are removed from the public query text. The candidate set includes real Hackage packages with related descriptions and overlapping dependency neighborhoods. The hidden evaluation emphasizes both ordinary queries and two difficult subsets: dependencies that are rare in the public training labels, and package queries with sparse dependency context.
> Your complete solution must run on CPU and finish within 1.5 hours, including training, validation, inference, and creation of the submission file. GPU, TPU, and other accelerators are not allowed.
> Dataset
> dataset/public/
> ├── train.csv
> ├── train_labels.csv
> ├── test.csv
> ├── candidate_packages.csv
> └── sample_submission.csv
> train.csv
> id,query_text,known_dependencies
> Columns:
> id: integer training-query identifier. It is unique within train.csv and is the key used by train_labels.csv.
> query_text: normalized metadata text for the source package. It includes fields such as synopsis, description, changelog notes, license, latest major version, and known direct dependencies, after masking the source and withheld target package names.
> known_dependencies: JSON list of package-name strings. These are visible direct or test/benchmark dependencies from the source metadata after the withheld target is removed.
> train_labels.csv
> id,target_candidate_id
> Columns:
> id: integer key matching exactly one row in train.csv.
> target_candidate_id: integer key into candidate_packages.csv. This is the withheld dependency for the training query.
> test.csv
> id,query_text,known_dependencies
> Columns are the same as train.csv, but labels are hidden and used only for final grading. Every test id must appear exactly once in the submission.
> candidate_packages.csv
> candidate_id,package_name,license_name,synopsis,description,changelog_excerpt,own_dependencies
> Columns:
> candidate_id: integer identifier of a rankable candidate package.
> package_name: Hackage package name.
> license_name: package-specific license name from the source metadata after normalization.
> synopsis: short package summary.
> description: normalized package description text.
> changelog_excerpt: normalized changelog or release-note text, capped during preparation.
> own_dependencies: JSON list of the candidate package's own public dependency names.
> The candidate table is shared by the training and test splits. Join target_candidate_id in train_labels.csv to candidate_id in candidate_packages.csv for supervised training.
> sample_submission.csv
> A valid format-only submission with one row per test query:
> id,ranked_candidates
> The sample ranks the first 20 candidate IDs for every query. It is provided only to illustrate the required file shape, not as a competitive baseline.
> Submission format
> Write predictions to:
> working/submission.csv
> The CSV must contain exactly two columns:
> id,ranked_candidates
> ranked_candidates must be a JSON list of exactly 20 unique integer candidate IDs, ordered from most likely to least likely. Candidate IDs must come from candidate_packages.csv.
> Example row:
> 17,"[812,44,2190,6,137,991,73,521,187,415,1320,902,11,305,76,144,278,601,930,38]"
> Every test id must appear exactly once. Do not include scores, package names, extra columns, or fewer or more than 20 candidate IDs.
> Evaluation
> The score is a weighted ranking metric:
> 0.55 × overall MRR@20
> 0.20 × overall nDCG@20
> 0.15 × rare-target MRR@20
> 0.10 × sparse-context MRR@20
> There is exactly one relevant candidate for each test query.
> For one query, let rank be the 1-based position of the true target candidate in the submitted list. If the true target is absent from the top 20, both query-level scores are zero.
> reciprocal_rank@20 = 1 / rank
> nDCG@20            = 1 / log2(rank + 1)
> The overall MRR@20 and overall nDCG@20 components average these query-level values over all test queries. The rare-target MRR@20 component is computed only on a hidden subset whose target dependencies are comparatively infrequent in the public training labels. The sparse-context MRR@20 component is computed only on a hidden subset whose source package has relatively few visible dependency-context cues.
> The score range is mathematically 0.0 to 1.0, and higher is better.
> This metric rewards placing the true missing dependency early, not merely somewhere in a long list. The rare-target and sparse-context components prevent a solution from relying only on the most frequent packages or on large visible dependency neighborhoods.
> Allowed methods
> Models trained on the provided public training queries, labels, and candidate package table.
> Classical information retrieval, text similarity, graph features, and conventional machine-learning methods.
> General-purpose pretrained language or embedding models, provided they are already available locally, run on CPU within the time limit, and are not Hackage-, Cabal-, or dependency-reconstruction-specific checkpoints.
> Feature engineering from public metadata fields, including query text, known dependencies, candidate text, candidate package names, candidate licenses, and public candidate dependency lists.
> Local validation using only the public training split.
> CPU-compatible ensembling, reranking, and post-processing within the 1.5-hour total limit.
> Not allowed
> GPU, TPU, or other accelerator use.
> External APIs, or remote models during solution execution.
> Recovering source package names for test queries through exact text lookup, external metadata lookup, search-engine lookup, source-row reconstruction, filename recovery, or other re-identification techniques.
> Using original or mirrored hidden labels for test queries.
> Hackage-, Cabal-, Stackage-, or all-cabal-metadata-specific pretrained dependency-recommendation checkpoints.
> Manual annotation of test queries.
> Hard-coding test predictions.
> Exploiting row order, IDs, candidate ordering, masking artifacts, preparation implementation details, or grader behavior instead of modeling package dependency relevance.

Inspiration note: Useful for ordered route/workflow reconstruction outputs with explicit consistency constraints.

## Subject-Heading Salience Ranking

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7emme6dymaqt8p56r9wg33nx8agt58
- DOMAIN exactly as displayed: Recommendation
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
> This is a within-group recommendation / learning-to-rank task over library catalogue records.
> Each record is a catalogued work: a short title plus a set of 3-8 subject headings, shown in a
> fixed, random order. Your job is to rank the headings by the cataloguer's salience — the
> primary "aboutness" heading first, broad / geographic / form headings last. The output is a ranking
> (a permutation of the record's headings) — not a class label.
> Task
> train.csv gives records with their true (cataloguer) heading order revealed, to learn from.
> For every record in test.csv, read the title and the (shuffled) headings and output ranked:
> those same headings reordered from most to least salient.
> Why it is hard
> The headings are shown in a random order that is uncorrelated with the true salience order, so
> there is no positional shortcut. The true order is also uncorrelated with alphabetical order
> (the pool is not filtered on alphabetical order), so sorting — or reverse-sorting — the headings
> alphabetically carries no signal either: salience must be inferred from content.
> The signal is indirect and noisy: how specific a heading is (how rarely it is used), how much it
> overlaps the title, whether it is a personal name / topical term / geographic or form heading, and
> how it relates to its sibling headings all nudge the order.
> Per-record heading counts are small (3-8) and cataloguing practice is inconsistent, so the ceiling
> sits well below 1.0.
> Data
> Three files are provided.
> train.csv — labelled records, with columns:
> record_id (string) — a 16-character hexadecimal record identifier.
> title (string) — the work's title.
> headings (string) — the record's subject headings in a fixed random order, |||-separated.
> ranked (string) — the true cataloguer order of those headings, |||-separated (train only).
> test.csv — records to rank, with columns record_id, title, headings (no ranked).
> sample_submission.csv — a correctly-formatted example (headings left in the shown order;
> scores ≈ 0).
> Records are disjoint between train and test.
> Submission Format
> Produce a CSV with exactly two columns, one row per record_id in test.csv (no duplicates):
> record_id (string) — the record identifier, copied from test.csv.
> ranked (string) — a |||-separated list of that record's headings in your predicted salience
> order (most salient first). It must be a permutation of exactly the record's headings; a
> malformed row scores 0 for that record.
> Example (submission.csv):
> record_id,ranked
> 7b3f1c9a0b7e2d45,Immigrants--United States ||| Assimilation (Sociology) ||| United States
> a2c4e6081a2b3c4d,Photosynthesis ||| Plant physiology ||| Chloroplasts
> Evaluation
> Metric — mean per-record Spearman rank correlation, with a single aggregate floor at 0.
> For one test record with K headings (3 ≤ K ≤ 8): your ranked list assigns each heading a
> predicted rank p_i (1 = first in your list, …, K = last), and the cataloguer's true order assigns
> it rank t_i. The per-record score is Spearman's rank correlation between the two rank vectors:
> rho = 1 - ( 6 * sum_i (p_i - t_i)^2 ) / ( K * (K^2 - 1) )
> Because the ranks are a permutation of 1…K there are no ties, so this equals the Pearson correlation
> of the two rank vectors. rho = +1 for the exact order, 0 for an uncorrelated order, -1 for the
> reverse.
> Aggregation and edge cases:
> Malformed record → 0. If a record's ranked value is not a valid permutation of exactly
> that record's headings (a heading missing, duplicated, or not belonging to the record), that record
> scores rho = 0. It is not dropped — it still counts in the mean.
> Final score. Average rho over all N scored records, then apply the floor once:
> score = max(0, (1/N) * sum rho). The floor is applied only to the final mean, never per
> record — an individual record may have a negative rho that pulls the mean down. A perfect
> submission scores 1.0.
> For reference, a feature-based gradient-boosted ranker (heading specificity + title overlap + form
> cues) reaches mean Spearman ≈ 0.25; a stronger character-n-gram + LambdaMART solver ≈ 0.35+.
> A random order, the shown-order sample, and sorting the headings alphabetically or
> reverse-alphabetically all score ≈ 0.
> Approaches
> Build per-(record, heading) features — global heading document-frequency (specificity), title
> token overlap, heading length, personal-name / geographic-subdivision cues, sibling overlap — and
> learn a pointwise or pairwise ranker from the training orders; sort each test record.
> Validate locally by holding out records and computing mean per-record Spearman.
> Relationship to Prior Work
> This task is deliberately not subject-heading assignment or indexing — the family that
> includes LCSH heading-assignment benchmarks (e.g. LCSHBench, arXiv:2606.04382) and MeSH automatic
> indexing (MTI / MeSHNow, PMC3168302). It differs on three independent axes:
> Target — a procedural artifact, not semantic relevance. Assignment/indexing predicts which headings are relevant to a work (an aboutness judgment). Here the assigned headings are given;
> the target is the cataloguer's entry order — a clerical sequence that cataloguing guidance
> itself deems non-substantive ("heading order is not significant beyond the first, which should
> agree with the classification"). Recovering a listing sequence and judging relevance are different
> learning problems with different signal.
> Structure — closed-set reordering, no controlled vocabulary, no retrieval. Indexing benchmarks range over the full controlled vocabulary (hundreds of thousands of LCSH / tens of thousands of
> MeSH terms) as extreme multi-label classification or retrieval. Here there is no vocabulary and
> no membership decision: the 3-8 headings are provided and only their order is predicted.
> Output & metric — a within-record permutation scored by rank correlation, not a label set / ranked-vocabulary scored by Recall@k / nDCG / F1.
> What Not To Use
> No lookup. The titles are real bibliographic strings, so the cataloguer's heading order could
> in principle be looked up. Do not try to identify the records and retrieve their catalogue
> entries from any library catalogue, MARC record, or search engine — the task is inferring the
> salience order from the provided text, and any submission relying on such lookups is out of scope.
> Do not hard-code answers. The intended solution generalises to unseen records.
> Submissions
> 44

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Masked Curated Shelf Completion

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73mv0k6kdk3d61k8jjy8p63d8bmkqr
- DOMAIN exactly as displayed: Recommendation
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
> A curated shelf is a human-made set of books connected by a theme, purpose, mood, historical period, audience, or other organizing idea. In this challenge, part of each shelf is visible and the remaining membership must be recovered from a difficult candidate set.
> Each row provides:
> a short, partially masked list_hint;
> four masked book cards known to belong to the same shelf;
> twenty candidate book cards with row-local ids.
> Exactly two candidates are hidden members of that shelf. Rank up to five candidate ids from most likely to least likely.
> The candidate pools are contrast sets. Incorrect candidates were selected because they resemble the visible shelf, so broad genre matching or global popularity alone is not enough.
> Dataset
> train.csv contains 1,500 rows and test.csv contains 1,000 rows.
> The columns are:
> sample_id string): Anonymous row identifier matching ^sample_[0-9a-f]{24}$.
> context_json JSON string encoded in CSV): Contains list_hint and known_books.
> candidates_json JSON string encoded in CSV): A list of exactly twenty candidate cards.
> target_json JSON string encoded in CSV, train only): The two correct candidate ids.
> Example context_json:
> {
> "list_hint": "women in [MASKED] history",
> "known_books": [
> {
> "title_pattern": "voices from the [TERM]",
> "subject_clues": ["social movements", "political history"],
> "year_bucket": "1975_1999",
> "language": "eng",
> "author_count": "one"
> }
> ]
> }
> The real rows contain exactly four objects in known_books.
> Each candidate card has exactly:
> book_id string): Row-local id matching ^B\d{3}$.
> title_pattern string): Lossy title with distinctive terms normalized.
> subject_clues JSON list of strings): One or two masked catalog clues.
> year_bucket string): Coarse first-publication interval or unknown.
> language string): Compact language bucket.
> author_count string): none, one, or multiple.
> Example candidates_json:
> [
> {
> "book_id": "B001",
> "title_pattern": "the [TERM] movement",
> "subject_clues": ["civil rights", "social conditions"],
> "year_bucket": "1950_1974",
> "language": "eng",
> "author_count": "one"
> },
> {
> "book_id": "B002",
> "title_pattern": "a history of [TERM]",
> "subject_clues": ["politics and government"],
> "year_bucket": "2000_2024",
> "language": "eng",
> "author_count": "multiple"
> }
> ]
> Example target_json:
> ["B001", "B014"]
> Candidate ids are randomized independently inside every row. They do not identify the same book across rows.
> Task
> For each test row, submit an ordered JSON list containing zero to five candidate ids. Put the most likely shelf member first.
> Only the supplied public files may be used. External catalog lookup, record matching, or outside datasets are not part of the task.
> Permitted and Prohibited Methods
> Lexical overlap, semantic similarity, handcrafted ranking rules, and learned models are permitted as complete solutions or as preprocessing components, provided every decision is derived only from the supplied public challenge files.
> The following are prohibited:
> external book catalogs, APIs, websites, pretrained retrieval indexes, or downloaded metadata;
> recovering original catalog records or reader-created lists through text matching;
> predictions based on sample_id, candidate ids, CSV row order, filenames, paths, or hidden metadata;
> manually encoded candidate-to-target mappings or hardcoded answer tokens;
> private test labels, test-derived statistics, or decisions based on the test-input distribution;
> reconstructing removed source-list identity, provenance, user identity, or external identifiers.
> Candidate identifiers are local to one row and have no meaning across rows. sample_id is an anonymous join key only and must not be used as a predictive feature.
> Submission Format
> Submit a CSV with exactly these columns, in this order:
> sample_id
> prediction_json
> prediction_json is a JSON list encoded inside the CSV cell.
> Example:
> sample_id,prediction_json
> sample_0123456789abcdef01234567,"[""B014"",""B001"",""B009"",""B003"",""B020""]"
> Every test id must appear exactly once. Extra ids, missing ids, extra columns, malformed JSON, duplicate candidate ids, unknown candidate ids, and lists longer than five are rejected before scoring.
> Evaluation
> The score is mean Average Precision at 5 (MAP@5), bounded from 0 to 1, with higher better.
> For one row, let the ordered submitted ids be p1, p2, ..., pk, where 0 <= k <= 5, and let G be the set of two correct ids.
> hit(i) = 1 if pi is in G, otherwise 0
> precision@i = (hit(1) + ... + hit(i)) / i
> AP@5 = [sum from i=1 to k of precision@i * hit(i)] / 2
> The final score is:
> MAP@5 = mean(AP@5 over all 1,000 test rows)
> An empty prediction receives 0 for that row because every reference contains two answers. A perfect ordering that places both correct ids in the first two positions receives 1.0. Incorrect candidates before a correct candidate reduce its precision contribution.
> Reference Baselines
> The challenge creator measured the following deterministic reference scores on the packaged split:
> independent random ranking: 0.1243;
> public-card overlap ranker using title patterns, subject clues, year buckets, and the four known cards: 0.0888;
> train-only learned pair model using the same public card fields: 0.3645.
> The public-card overlap method is permitted as either a final submission method or a preprocessing component. These figures are reference implementations, not guaranteed leaderboard thresholds.
> Practical Notes
> The shelves are sets; the order of the four known cards is not meaningful.
> A shelf can represent a narrow topic, a cross-genre idea, a reading purpose, or a curator-specific connection.
> Distinctive names, numbers, and rare terms are partially normalized.
> Candidate pools contain close semantic negatives rather than random books.
> Train and test lists were separated after overlap and near-duplicate filtering.
> Originality Review
> The nearest established research family is user-generated item-list continuation, including work on playlist, board, and book-list completion. General book recommendation and book-genre prediction are also adjacent task families.
> This challenge is not a direct copy of those tasks:
> it uses a new 2,500-row snapshot derived from Open Library reader-created Lists;
> each query is an unordered masked shelf rather than a chronological user history;
> all candidate ids are row-local, preventing item-id memorization;
> every row contains exactly two positives inside a twenty-book hard contrast set;
> source titles and subject metadata are transformed into lossy cards;
> direct target-bearing hint terms and rare entities are normalized;
> negatives are selected from semantically adjacent non-members rather than sampled randomly;
> overlap components and near-duplicate lists are kept within one side of the split;
> evaluation is a single, strict macro MAP@5 score over the two hidden members.
> A newly released benchmark called LCSHBench is also nearby in the broad library-metadata domain, but it predicts controlled Library of Congress Subject Headings from bibliographic records. This challenge predicts hidden membership in human-curated book sets and never asks participants to generate or retrieve a subject heading.
> The exact data transformation, candidate construction, masking policy, 1,500/1,000 split, row-local ids, and scoring contract are new to this challenge.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## DutyBridge: Multi-Duty Transfer Portfolio Recommendation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77cvjhgfk80apsy59r79s45h8c3neq
- DOMAIN exactly as displayed: Recommendation
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> DutyBridge: Multi-Duty Transfer Portfolio Recommendation
> Overview
> Given 2â€“4 duties from one source occupation and a graph of possible transfer evidence, predict exactly two target occupations that together cover every duty. For each duty, identify the selected occupation, task, and Detailed Work Activity (DWA) supporting the transfer, then report the pair's occupational-group diversity and job-zone difference.
> The data comes from ONET, a United States Department of Labor occupational database that organizes occupations, their task statements, and standardized work activities. A DWA is a normalized activity category, such as inspecting mechanical equipment, that can connect differently worded tasks across occupations. ONET job zones run from 1 to 5 and summarize how much education, experience, and training an occupation typically requires; a larger number represents greater preparation. Each scenario supplies the highest job zone allowed for its recommendations.
> The source duties do not disclose their task or DWA identifiers. Learn how duty language maps to DWA evidence from training examples, then reconcile that evidence against each row's candidate graph. A lexical contrast duty resembles the source language while sharing no source DWA, so surface similarity alone is unreliable.
> Structural Difference
> This is joint constrained set selection, not occupation similarity or candidate ranking. A prediction must infer several source-duty DWA mappings, choose a two-occupation portfolio whose members are both used, ground every duty in a supplied graph edge, and return a verifiable diversity certificate. Candidate graphs include plausible alternative portfolios and lexical no-shared-DWA contrasts. No formula defining the preferred portfolio is supplied.
> Dataset
> The deterministic prepared dataset contains 210 scenarios: 162 train and 48 test, making test 22.86%. Source occupations and five-segment DWA families are split-disjoint. The public test inputs contain no source task IDs or source DWA IDs.
> Public Split
> train.csv contains 162 rows and ten columns. test.csv contains 48 rows and the first seven input columns only:
> Column	Type	Files	Description
> example_id	string	train, test	Stable scenario identifier.
> source_occupation_title	string	train, test	Human-readable source occupation.
> source_job_zone	integer	train, test	O*NET job zone for the source.
> max_job_zone	integer	train, test	Maximum allowed zone for either recommendation.
> source_duties_json	JSON array	train, test	2-4 objects with string fields duty_token and text.
> lexical_contrast_duty	string	train, test	Similar-sounding duty that does not share the source DWA family.
> candidate_graph_json	JSON array	train, test	Permitted recommendation/evidence edges described below.
> portfolio_occupation_ids	string	train	Two lexicographically ordered O*NET-SOC codes separated by `
> evidence_chains	string	train	One chain per source duty in duty_token:occupation_id:target_task_id:dwa_id form, joined with `
> diversity_certificate	string	train	major_groups=N;zone_span=N for the selected pair.
> Each object in candidate_graph_json has occupation_id, occupation_title, major_group, target_task_id, target_task_text, dwa_id, and dwa_name as strings, plus job_zone as an integer.
> sample_submission.csv has 48 rows and four string columns: example_id, portfolio_occupation_ids, evidence_chains, and diversity_certificate. Every row is a complete, gradeable lexicographically-first example using two occupations and graph-backed chains; participants may replace those predictions.
> One projected training example has source title Transportation Vehicle, Equipment and Systems Inspectors, Except Aviation, source job zone 2, maximum job zone 3, portfolio 47-5044.00|53-6051.01, and certificate major_groups=2;zone_span=1. The actual train.csv row also includes its complete duty list, candidate graph, and evidence chains.
> Evaluation
> native_score = 25*portfolio_f1 + 40*evidence_chain_accuracy + 5*certificate_accuracy + 5*valid_structure_rate + 35*joint_exact_accuracy - 15*duplicate_portfolio_rate - 10*unsupported_chain_rate - 5*invalid_certificate_rate.
> Every component is calculated per row and then averaged across the 48 test rows:
> portfolio_f1 is set F1 between the two submitted occupation IDs and the two gold IDs: 2*|intersection|/(|gold set|+|submitted set|). It is zero when the row structure is invalid.
> evidence_chain_accuracy is the fraction of gold duty tokens whose complete submitted chain exactly matches the gold chain. Chains are matched by duty token, so their order does not matter. It is zero when the row structure is invalid.
> certificate_accuracy is 1 when the complete submitted certificate string equals the gold certificate and 0 otherwise.
> valid_structure_rate is 1 when the portfolio contains exactly two entries, every chain matches the required four-part grammar, duty tokens are unique, and the submitted duty-token set equals the gold duty-token set. Otherwise it is 0.
> joint_exact_accuracy is 1 only when structure is valid, the occupation set is exact, every evidence chain is exact, and the certificate is exact.
> duplicate_portfolio_rate is 1 when an occupation ID is repeated in the submitted portfolio and 0 otherwise.
> unsupported_chain_rate is 1 when any successfully parsed chain names an occupation outside the submitted portfolio and 0 otherwise.
> invalid_certificate_rate is 1 unless the certificate matches major_groups=N;zone_span=N with nonnegative integers.
> The native range is [-30, 110], and higher is better. The positive terms total 110. A structurally invalid row can simultaneously incur all three penalties without earning structure credit, giving the -30 lower endpoint. Report the mean of at least five independent runs for stochastic methods.
> Submission Format
> Start from sample_submission.csv and retain this exact column order. Portfolio IDs are pipe-separated and lexicographically ordered. Each evidence chain is duty_token:occupation_id:target_task_id:dwa_id; chains are pipe-separated, and every chain occupation must occur in the submitted portfolio.
> example_id,portfolio_occupation_ids,evidence_chains,diversity_certificate
> DBP_0000000000000000,13-0000.00|29-0000.00,S1:13-0000.00:1234:4.A.2.a.1|S2:29-0000.00:5678:4.A.3.b.2,major_groups=2;zone_span=1
> Not Allowed Methods
> Manual lookup or annotation of evaluation rows or their originating records.
> Recovering answers from answer files, grader internals, file order, hashes, or IDs.
> Joining evaluation data to external O*NET copies, web services, search engines, or APIs.
> Hard-coding predictions for particular example_id values.
> Claiming a DWA or task edge absent from the row's candidate graph.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## HydroRelay: Fault-Tolerant Gauge Portfolio Recommendation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx785ff2y8f8ha6mn0mnqmbnrh8c0r7z
- DOMAIN exactly as displayed: Recommendation
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> HydroRelay: Fault-Tolerant Gauge Portfolio Recommendation
> Overview
> HydroRelay uses a frozen snapshot of approved daily streamflow observations from 24 active Maryland gauges in the United States Geological Survey National Water Information System. The source covers 2020 through 2025, and discharge is measured in cubic feet per second. Each prepared case represents a historical relay-selection decision: the target gauge provides its preceding 90 daily values, while six synchronized candidate gauges provide the same 90-day history and their following 14 days. The target's following 14 days reveal policy quality in training and are withheld for test evaluation.
> Recommend a five-gauge relay portfolio and failover assignment that remains useful when any one primary donor becomes unavailable. For every case, select three primary donors, select two different standby donors, and assign one standby to replace each primary. Also submit the four consequence traces produced by applying the published relay estimator to the recommended policy.
> This is a coupled recommendation and recovery-planning problem rather than six independent gauge rankings. A donor can improve normal relay behavior yet create the worst contingency when its assigned standby is activated. Every recommendation is therefore tested in four linked worlds: all primaries available, primary 1 unavailable, primary 2 unavailable, and primary 3 unavailable. The worst contingency carries 70% of the loss, so a balanced five-gauge portfolio can outperform a locally stronger but fragile primary set.
> Recommendation Task
> For each test case, submit:
> three distinct primary tokens selected from the six candidates;
> two distinct standby tokens selected from the remaining candidates;
> a mapping from every primary to one of the two selected standbys;
> the 14-day no-failure estimator trace produced by the recommended portfolio; and
> three 14-day fault traces, one for the failure of each primary.
> The candidate futures make the consequence of a submitted recommendation exactly reproducible. Participants choose the resilient portfolio and mapping, then derive the four numeric traces with the published estimator. The withheld target future is used during preparation to identify the gold resilient policy. Each row labels its six donors locally as D1 through D6; labels do not identify the same physical gauge across rows.
> Dataset
> All numeric series are nonnegative daily discharge values in cubic feet per second. The deterministic public split contains 322 training cases and 80 test cases, so test represents 19.90% of the 402 prepared examples. Ten gauges are reserved as test-only targets before any candidates are selected. They never occur as donors or training targets. The other 14 gauges supply the training targets and the only eligible donor pool.
> Test cases use eight windows per held-out target, separated by 112 days. A 14-day hidden future therefore cannot reappear inside another test case's 90-day target history. Public rows omit physical target identifiers and calendar dates, and row-local donor labels prevent cross-row gauge lookup. Preparation also performs an exact subsequence audit and stops if any hidden 14-day test future occurs verbatim in a public array.
> Public Split
> train.jsonl contains 322 JSON objects. Each object has:
> Field	Type	Description
> example_id	string	Unique case identifier.
> target_history	array of 90 numbers	Target observations through the cutoff.
> target_future	array of 14 numbers	Training target used to learn or tune a policy.
> candidates	object with keys D1â€“D6	Row-local donor tokens mapped to history and future, arrays of 90 and 14 numbers respectively.
> reference_policy	object	Training reference with primary (3 strings), standby (2 strings), and failover (primary-to-standby mapping).
> test.jsonl contains 80 JSON objects with example_id, target_history, and candidates. It omits target_future and reference_policy.
> sample_submission.csv contains 80 complete, gradeable data rows generated by the lexical policy D1,D2,D3 as primaries and D4,D5 as standbys. It has these columns:
> Column	Type	Description
> example_id	string	Must match one test identifier.
> primary	JSON array of 3 strings	Three distinct candidate tokens.
> standby	JSON array of 2 strings	Two other distinct candidate tokens.
> failover	JSON object	Maps every primary token to one selected standby.
> base_forecast_cfs	JSON array of 14 numbers	Deterministic estimator trace with all primaries available.
> fault_forecasts_cfs	JSON object	Maps each primary token to its deterministic 14-number failure-world trace.
> A training record begins with an opaque example_id followed by target_history, the six locally labelled candidate records, target_future, and reference_policy. No station identifier or calendar date is published in the prepared split.
> Policy Trace Estimator
> For target history T and candidate history/future pair (H, F), calculate the median over 90 days of log(T + 0.01) - log(H + 0.01). Add that offset to each log-flow in F, transform back, and average the three active donor traces. In a failure world, replace only the failed primary with its assigned standby. This is the deterministic procedure participants use to derive their submitted traces. The exact-full component described below requires every submitted trace to match its gold trace within 1e-4.
> Evaluation
> Gold Policy Construction
> During preparation, every legal relay policy is evaluated against the withheld 14-day target future. For target values y and a policy trace p, mean absolute log error is:
> MALE(y, p) = (1 / 14) * sum from t=1 to 14 of
> |log(y[t] + 0.01) - log(p[t] + 0.01)|
> The 0.01 offset is fixed and is the same offset used by the relay estimator. Preparation calculates a base error and three single-primary-failure errors, then minimizes:
> selection_loss = 0.30 * base_MALE + 0.70 * max(the three fault_MALE values)
> All 480 legal policies over the six supplied candidates are considered:
> 20 choices of 3 primaries from 6
> * 3 choices of 2 standbys from the remaining 3
> * 8 mappings assigning each of 3 primaries to either standby
> = 480 policies
> The policy with the lowest selection_loss, with deterministic lexical tie-breaking, becomes the gold answer. This exhaustive selection defines the target recommendation; selection_loss is not the competition score.
> Competition Score
> Each valid row receives the following points:
> 25 * primary_set_F1
> + 15 * standby_set_F1
> + 20 * failover_edge_F1
> + 15 * base_trace_similarity
> + 20 * fault_trace_similarity
> + 25 * exact_policy
> + 30 * exact_full
> For the primary and standby components, set F1 is 2 * overlap / (gold set size + submitted set size). The failover component applies the same formula to sets of (primary, assigned standby) edges. A missing overlap receives zero.
> Trace similarity compares a submitted trace p with its gold trace g:
> trace_MALE(g, p) = (1 / 14) * sum from t=1 to 14 of
> |log(g[t] + 0.01) - log(p[t] + 0.01)|
> trace_similarity = max(0, 1 - trace_MALE)
> base_trace_similarity applies this calculation to the no-failure trace. fault_trace_similarity is the mean similarity for the three gold primary keys; a missing gold fault key contributes zero.
> exact_policy is 1 only when the primary set, standby set, and complete failover mapping all equal the gold policy. exact_full is 1 only when exact_policy is 1 and the base trace plus all three gold-key fault traces match the gold values within 1e-4; otherwise these indicators are zero.
> The final relay_policy_alignment_points score is the arithmetic mean of row points across all 80 test cases. Higher is better and the native range is [0, 150]. Invalid JSON, an incorrect header or test-ID set, duplicate or unknown IDs, tokens outside D1â€“D6, illegal selections, incorrectly sized arrays, nonnumeric values, or nonfinite values stop grading with a diagnostic error. Row-level errors include the offending example_id.
> For a stochastic method, evaluate at least five complete submissions and report their mean rather than selecting the best run. Deterministic methods require only one run.
> Submission Format
> Start from sample_submission.csv and preserve the exact header. JSON values must remain CSV-quoted. This is one valid-format row:
> example_id,primary,standby,failover,base_forecast_cfs,fault_forecasts_cfs
> HR_6F31487E22C51A,"[""D1"",""D2"",""D3""]","[""D4"",""D5""]","{""D1"":""D4"",""D2"":""D4"",""D3"":""D5""}","[20.839099,21.112959,20.684262,19.986864,19.429372,18.795205,18.802705,18.131706,17.879597,17.809272,20.487651,31.495481,23.909305,70.175631]","{""D1"":[22.871952,23.365026,20.654479,19.99736,21.544422,19.31717,20.385667,20.251963,20.44734,18.078782,20.821913,33.660829,27.411812,109.554099],""D2"":[19.418289,19.722511,16.939395,16.136713,17.571172,15.653726,16.408882,15.681178,15.974874,14.160571,14.692474,18.613628,19.23906,75.951451],""D3"":[16.67063,16.660021,16.442238,16.189559,15.435783,14.696904,14.773082,14.196907,13.854851,13.568737,16.381223,26.421183,19.168511,51.736743]}"
> Not Allowed Methods
> Do not query external hydrologic services, reconstruct target futures from an outside source, use lookup tables keyed by identifiers or dates, alter benchmark files, or change the submission schema. Every portfolio recommendation and estimator trace must be derived from the supplied public task data.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Solvent Quartet: Cold-Solute Solubility Ranking

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dgrtzv4r4pakey7nbztpqpx8bz315
- DOMAIN exactly as displayed: Recommendation
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Solvent Quartet: Cold-Solute Solubility Ranking Overview Selecting a binary solvent system requires understanding interactions between a solute, both solvents, their composition, and temperature. A mixture that works well for one molecule may be a poor choice for another. Your task is to learn these preferences from experimentally grounded training rankings and recommend the order of four candidate mixtures for previously unseen solutes. Each dataset row is one complete solute bundle. A bundle contains 1–32 independent ranking contexts for the same solute. Within a context, the four candidates share the same measured temperature and fraction type. Their actual compositions lie within the same 0.10-wide composition window but need not be identical. Always use the candidate's actual fraction_a and fraction_b, not the window center. Rank all four candidates within every context, from highest to lowest experimentally measured mole-fraction solubility. This remains a chemistry learning-to-rank / recommendation task, not prediction of absolute solubility. Every test solute is absent from training. All contexts for one solute are contained in one answer row, preventing row-level public/private leaderboard assignment from dividing that solute. Candidate selection limits the usefulness of simple solvent preferences. Training quartets are selected using solute-cross-fitted ordinal priors. Held-out quartets are mined against four priors fitted exclusively on the final public training rankings: query-weighted solvent-pair ranks, solute-balanced solvent-pair ranks, solvent-component ranks, and solvent-pair matchup preferences. Both each prior and its reversal are considered. This is a deliberately selected hard-negative evaluation distribution, not a random sample of all solvent-selection decisions. Evaluation The metric is solute-balanced mean weighted pairwise ranking accuracy, between 0 and 1; higher is better. For a context, let s_i denote the private measured LogS(mole_fraction) for candidate i. Define the weight of each unordered candidate pair: w_ij = min(abs(s_i - s_j) / 0.50, 1.0) A pair receives c_ij = 1 when the submitted order puts the more soluble candidate first, and 0 otherwise: context_score = sum(w_ij * c_ij) / sum(w_ij) solute_score = mean(context_score over the contexts in that solute's bundle) final_score = mean(solute_score over the solutes being evaluated) Every solute therefore has equal final weight, whether it has one context or 32. Every context within a solute has equal weight. A perfect set of rankings scores 1; reversing all correct rankings scores 0. Uniform random permutations have expected score 0.5. This expectation is not the guaranteed score of one particular random submission. Training targets expose the correct order and the six pair weights, allowing exact local evaluation without exposing absolute LogS. Pair weights are always in this order: (C1,C2), (C1,C3), (C1,C4), (C2,C3), (C2,C4), (C3,C4) Selected quartets have LogS ranges from 0.30 through 1.60 and adjacent sorted gaps of at least 0.018, so the weight denominator is strictly positive. Duplicate experimental measurements at the same complete chemical and experimental condition are aggregated by median LogS; no measurement is interpolated and no experimental label is synthesized. Dataset The provided release has 130 training solutes containing 3,112 contexts and 57 test solutes containing 975 contexts. A context contains exactly four candidates. Use only prepared challenge files as task data. train.jsonl One JSON object per line: | Field | Type | Meaning | |---|---|---| | query_id | string | Unique identifier for the complete solute bundle. | | validation_group | string | Opaque solute identity for grouped validation; not a predictive feature. | | solute_smiles | string | Source SMILES of the solute. | | compound_name | string | Source solute name. | | fda_approved | boolean | The source release's FDA-approval metadata; not a current regulatory assertion. | | contexts | list of objects | Between 1 and 32 ranking contexts for this solute. | | targets | object | Mapping from every context_id to its training ranking and six pair weights. | Each context has: | Field | Type | Meaning | |---|---|---| | context_id | string | Context-local identifier such as Q001, unique within its solute bundle. | | temperature_k | number | Actual shared experimental temperature in kelvin. | | fraction_type | string | mass or mole, applying to all fractions in this context. | | composition_anchor | number | Selection-window center, one of 0.1, 0.2, …, 0.9; not a measured replacement composition. | | candidates | list of four objects | The actual measured candidate solvent mixtures. | Each candidate has: | Field | Type | Meaning | |---|---|---| | candidate_id | string | Exactly one of C1, C2, C3, C4; independently assigned within each context. | | solvent_a_name | string | Source name of solvent A. | | solvent_a_smiles | string | Source SMILES of solvent A. | | fraction_a | number | Actual measured fraction of solvent A under fraction_type. | | solvent_b_name | string | Source name of solvent B. | | solvent_b_smiles | string | Source SMILES of solvent B. | | fraction_b | number | Actual measured fraction of solvent B under fraction_type. | Solvents A and B are ordered lexicographically by their source SMILES. Fractions are swapped with their solvents when needed. Each fraction is strictly between zero and one, and the two sum to one within numerical precision. Candidate A fractions are selected in the same half-open decile window [anchor - 0.05, anchor + 0.05), with a 1e-12 numerical allowance in the binning operation. For each solvent pair, the nearest actual measurement to the anchor is used; no center-composition measurement is fabricated. A training target value has exactly two entries: | Entry | Type | Meaning | |---|---|---| | ranking | list of four strings | All candidate IDs ordered from highest to lowest solubility. | | pair_weights | list of six numbers | Exact metric weights, in the pair order given above. | Candidate IDs and context IDs have no global class meaning. Never group unrelated Q001 contexts or treat C1 as a globally preferred solvent. test.jsonl Exactly the same feature structure as training, but without targets. Every test validation_group and solute_smiles occurs in exactly one row, and neither overlaps training. Predict every context independently; the bundle is an evaluation and serialization unit, not permission to adapt to the test distribution. sample_submission.csv A complete format example with 57 rows and valid, arbitrary C1 C2 C3 C4 permutations. Its score is incidental; it is not a learned baseline or a valid end-to-end ML solution by itself. dataset_metadata.json Contains release version, preparation seed, actual split and context counts, source checksum, composition-window width, and scoring/aggregation metadata. It contains no held-out targets or row-level visibility assignments. Submission Write ./working/submission.csv with exactly these two columns, in this order: | Column | Type | Meaning | |---|---|---| | query_id | string | Complete solute-bundle identifier copied from test.jsonl. | | ranking | JSON object serialized into one CSV string cell | Mapping from every context_id in this solute bundle to a space-separated permutation of its four candidate IDs. | Example for a bundle with one context: query_id,ranking TES_98be546908335cfa,"{""Q001"":""C3 C1 C4 C2""}" For a bundle with several contexts, the same cell contains all its entries, for example {"Q001":"C3 C1 C4 C2","Q002":"C2 C4 C1 C3"}. These are format illustrations, not label disclosures. Use json.dumps and pandas.DataFrame.to_csv(..., index=False) rather than manually escaping the CSV. The complete submission must contain exactly 57 rows, one for each test solute bundle. Include each ID exactly once, no extra IDs or columns, and a header. Row order does not matter. Within each JSON object, include every required context exactly once and no unknown contexts. Each context prediction must contain all four candidate IDs exactly once, separated by spaces. JSON key order does not matter. The reserved string DUMMY, either as the entire ranking cell or as one context's value, is accepted as an explicit abstention and scores zero for that bundle or context. It is not a competitive strategy. Other malformed JSON, duplicate keys, missing contexts, invalid permutations, duplicate IDs, missing IDs, or extra IDs raise a validation error rather than silently receiving a misleading score. Validation and solver rules Use solute-grouped validation built only from training bundles. Never split contexts from the same solute across local fitting and validation folds. Evaluate the actual solute-macro metric, not a query-weighted or pair-count-weighted surrogate. Pairwise training examples mechanically derived from the supplied rankings are permitted; they must not introduce new solutes, measurements, or invented labels. The final predictive system must perform genuine model training or fine-tuning within one independent end-to-end script. Molecular representations and deterministic features may support a learned model, but a rule-only, lookup-only, solvent-popularity-only, or inference-only system is not a compliant solution. This challenge is not designated a mandatory Fine-Tuning challenge. Use only libraries preinstalled in the configured Kaggle Docker environment. Do not install packages at runtime. General-purpose pretrained weights may be loaded through mechanisms allowed by the Eris guidebook, but challenge-specific previously trained checkpoints, external chemical datasets or databases, source-dataset downloads, and hosted prediction APIs are prohibited. The supplied reference requires no network access or pretrained weights; this is not a blanket ban on guidebook-permitted backbone downloads. No private answers, raw creator files, or source-record identifiers may be used as solver data. No solver-generated synthetic training dataset, pseudo-labeling, full-test-distribution calibration, training-sample reweighting based on test data, or test-time adaptation is allowed. Predicting a context in isolation must not require seeing other test solutes or their predictions. Read task data from ./dataset/public/ and write outputs only under ./working/. Complete the end-to-end run within 60 minutes, reserving time for inference and serialization; stop training by approximately 3,000 seconds. CPU-only solutions are allowed. Genuine learned models are required regardless of whether CPU or GPU is used.
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## AeroForge: Mission-Briefed Aerodynamic Shortlist Ranking

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dvgx6q52863z13p6t5sp9b98ea9cp
- DOMAIN exactly as displayed: Recommendation
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> AeroForge: Mission-Pair Aerodynamic Shortlist Ranking Overview Aerodynamic design programs screen far more candidate profiles than they can afford to study deeply, and the same shortlist is usually judged against more than one mission. At the screening stage the working questions are "how should these profiles be ordered for this brief" and, just as important, "how does that order change when the brief changes". AeroForge poses both as one context-aware ranking recommendation problem. Every scored row is a closed cluster of about twelve anonymous candidate profiles; inside it sit 24 six-candidate shortlists, and each shortlist comes with a mission pair, two briefs that value the physical terms differently. The task is to rank every shortlist under each of its two briefs the way a high-fidelity flow solver would order it, best candidate first. Behind the scenes, every shortlisted candidate was evaluated by a Reynolds-averaged flow solver, and the hidden relevance orderings are computed from its measured force coefficients. Those coefficients are never released. A useful recommender therefore has to learn a transferable geometry-to-aerodynamics surrogate from the labeled training shortlists, combine it with each brief, and get the counterfactual right: which candidate pairs swap order between the two briefs and which do not. How the Hidden Orderings Are Built The physical structure of the relevance score is the core of the benchmark. Each candidate's hidden utility under a brief combines solver measurements taken at two flow conditions, one cruise-like and one near the aggressive end of the operating envelope: an efficiency term that rewards lift relative to drag at the cruise-like condition; a high-lift term at the aggressive condition, which the brief credits only to the degree it tolerates pitching moment (profiles that make lift also make nose-down moment); a stall-margin term, passed through a soft hinge, computed from how the lift response changes between the two conditions; a pitching-moment penalty whose weight is a soft threshold in the brief's moment tolerance: negligible for tolerant briefs, growing steadily once tolerance drops below the brief's comfort point; a robustness term that rewards consistent efficiency across both conditions; an unobserved counterfactual variation term that is never released, perturbs each realized ordering, and caps attainable skill below one. Each brief reweights these physical terms, and the reweighting happens inside the utility, before the ordering is fixed. The brief-independent part of the score, the quality a profile keeps under an average brief, is deliberately small: most of every ordering is decided by how the current brief trades the terms off, so no profile is good for every brief and a model that only learns average quality recovers little. In training, the two briefs of a case are always drawn independently, so their orderings differ by construction: about half of all candidate pairs swap order between the two briefs of a case, and the leading candidate changes in most cases. Evaluation adds counterfactual tracks whose brief pairs are never seen in training (see below). The scored object is the whole ordering under each brief and the change between them, so middle-of-the-shortlist relations matter, not only the winner. Because a cluster's profiles recur across its 24 shortlists under different briefs, a row is also a small transfer test in itself: the same dozen geometries must be ordered consistently under many different trade-offs. Inputs: One Cluster Row, 24 Shortlists, Two Briefs Each The context modality holds, for every shortlist of a row, a pair of six-value mission vectors: cruise-efficiency emphasis, high-lift emphasis, pitching-moment tolerance, stall-margin emphasis, and two nuisance weights, once for brief 1 and once for brief 2. The candidate modality holds, for every shortlist of a row, a six-by-sixteen tensor with one anonymous 16-value geometry descriptor per slot, shared by both briefs of that shortlist. The 24 shortlists of a row draw only from that row's own cluster of geometries, so the same descriptor recurs inside a row and never appears in any other row. Descriptors are fixed keyed nonlinear projections of chordwise camber and thickness structure: a keyed two-stage smooth mixing of the geometry's principal structure, identical everywhere, so a recommender can learn one reusable geometry-to-quality mapping. The released values contain no coordinates, no coefficients, no identifiers, and no dimension that corresponds to a named geometric feature, and the physical terms are smooth but clearly nonlinear functions of the descriptor, so linear scorers on raw descriptors underfit while models that learn a representation do not. All brief and geometry values are float16 inside [-2.5, 2.5]. Shortlist slots are labeled with the letters A through F: letter A is index 0 on the slot axis of the geometry tensor, B is index 1, and so on. Slots are freshly permuted per shortlist after both hidden orderings are fixed, so a letter names a position inside the current shortlist, never a reusable item. The modalities must be aligned by row, shortlist, brief, and slot before fusion; flattening a shortlist into one long feature vector is a legitimate baseline, but it discards the set structure and the shared-shortlist coupling that the answer orderings depend on. Files and Column Contract train.csv: 497 labeled rows (11,928 shortlists) with columns id, array_index, target. test.csv: 249 unlabeled rows (5,976 shortlists) with columns id, array_index. validation_blocks.csv: columns id, block with block values 0 through 4; join by id, never by file order. train_brief.npy and test_brief.npy: mission pairs with shapes (497, 24, 2, 6) and (249, 24, 2, 6); axis 1 is the shortlist within the row, axis 2 is the brief (index 0 is brief 1, index 1 is brief 2). train_geometry.npy and test_geometry.npy: descriptor tensors with shapes (497, 24, 6, 16) and (249, 24, 6, 16); axis 1 is the shortlist within the row, axis 2 the slot. sample_submission.csv: the exact submission schema. data_manifest.json: dimensions, bounds, balance, split semantics, and public-file checksums. id is a stable opaque row identifier. target holds the hidden orderings of all 24 shortlists of the row, in tensor order, as 24 entries joined by semicolons; each entry is two six-letter strings joined by a hyphen, best candidate first: the entry DAFBEC-BFACED means that under brief 1 the profile at slot D leads and slot C trails, while under brief 2 slot B leads and slot D trails. Training array_index values run from 0 to the number of training rows minus one and index the training tensors directly; test values continue from there, so compute local_test_index = array_index - number_of_training_rows before indexing a test tensor. Split Design and the Frontier Slice Candidate geometries are grouped into near-duplicate families before anything else, and each complete family is assigned to exactly one side: 5,998 geometries train, 2,998 evaluate. Evaluation shortlists draw only from evaluation-side families that appear in no training shortlist, so the quality of an evaluation geometry cannot be looked up from training labels and has to be generalized from its descriptor. Within each side, complete families are then packed into closed clusters of about twelve geometries and every cluster becomes exactly one row, so no geometry and no family ever appears in two rows. This is what makes the leaderboard geometry-independent: the platform assigns visibility per row, and a geometry seen in a public row can therefore never occur in a private row. Training rows are assembled inside five family-disjoint blocks, and validation_blocks.csv records that partition, so cross-validation on the provided blocks estimates transfer to unseen geometry rather than interpolation between related shapes. The evaluation set additionally crosses a second axis: about 30 percent of evaluation briefs are frontier briefs whose strongest mission emphasis lies beyond the envelope spanned by every training brief, so roughly half of the evaluation shortlists carry at least one frontier brief. No training case carries such a brief. Because the brief enters the hidden utility through low-order smooth structure (weights that are linear in the emphasis components, a product of lift emphasis with moment tolerance, and a soft threshold in tolerance), a model that has learned the physical trade-off structure extrapolates to frontier briefs. Frontier briefs are sharper than in-envelope ones, so a model that carries the learned structure beyond the envelope can score higher there, whereas one that memorizes brief clusters or clamps at the training envelope forfeits that gain. Rehearse this before submitting: hold out the outer shell of the training brief envelope and check that your model still ranks well on it. Under brief 1, every slot letter leads exactly 4 of the 24 shortlists in every row. Within a row no unordered six-candidate shortlist repeats and per-geometry reuse is capped; the realized values are recorded in data_manifest.json. Released row order is shuffled independently, and one row carries a complete cluster with all of its shortlists and mission pairs, so the platform's public/private assignment always keeps a cluster whole. The sample template balances leading letters under brief 1 inside every row independently of the hidden answers, its measured score against them is bounded at the floor, and it cannot be inverted into an answer. Counterfactual Tracks Every training shortlist carries an independent pair: brief 2 is a fresh draw with no relation to brief 1. The evaluation set keeps that regime for two thirds of its shortlists and adds two held-out single-factor intervention tracks for the remaining third, spread across every row. In a tolerance intervention, brief 2 is brief 1 with only the pitching-moment tolerance moved, by at least a substantial step, while every other component is held fixed; in an emphasis intervention, brief 2 is brief 1 with only the three emphasis components redrawn, again by at least a substantial step, while tolerance and the nuisance weights are held fixed. No training shortlist contains such a pair, so the tracks ask a question the training data never poses directly: which candidate pairs swap when exactly one factor of the brief changes. The tracks are learnable from the independent pairs because the hidden utility is one shared low-order structure; a model that has learned how each brief component enters the trade-off answers the isolated what-if correctly, whereas a model that only fits the joint pattern of independent pairs attributes reversals to the wrong factor and loses reversal skill there. Intervention pairs differ on fewer candidate pairs than independent ones, so their reversal skill is normalized over fewer swaps and is measured with more noise, which is reported in the audit below. Track membership is not released; every shortlist is scored by the same formula. Provenance and Abstraction Boundary The reviewer-private build starts from a checksum-pinned public corpus of streamlined lifting-surface geometries evaluated by a Reynolds-averaged flow solver. Only geometry landmarks and integral force coefficients are consumed; coordinates, parameterization vectors, coefficient values, meshes, indices, and filenames stay outside every solver-facing file, and this description intentionally does not identify the corpus. The relevance orderings are derived from the solver's measurements through the documented utility mechanism, not from priors or hand labels. The mission weights are synthetic screening preferences rather than measured flight conditions, and the benchmark claims screening skill, not certification of any physical design. Evaluation Each case is scored on two things. The first is ordinary ranking quality: the Kendall rank correlation between the submitted and hidden ordering under each brief, averaged over the two briefs, tau_case = (tau(pred_1, true_1) + tau(pred_2, true_2)) / 2 where each tau is (concordant_pairs - discordant_pairs) / 15 over the 15 slot pairs. The second is reversal skill. For every slot pair, the change between the two briefs is the sign under brief 1 minus the sign under brief 2, so it is nonzero exactly on the pairs that swap order. Reversal skill is the cosine similarity between the submitted change pattern and the hidden change pattern over the 15 pairs, reversal_case = sum_pairs(change_pred * change_true) / sqrt(sum_pairs(change_pred^2) * sum_pairs(change_true^2)) The two hidden orderings of a shortlist always differ, so the hidden change pattern is never empty. The final score averages both parts over every evaluated shortlist with equal weight: score = max(0.001, 0.5 * mean(tau_case) + 0.5 * mean(reversal_case)) Reversal skill has two provable properties. If a submission gives the same ordering under both briefs, the term is exactly zero for that shortlist, whatever the ordering is, so a brief-agnostic recommender can earn at most half of the scale no matter how good its single ordering is. And because the cosine normalizes by the submitted change as well, predicting swaps on pairs that do not swap costs as much as missing real ones: the term is 1 exactly when the submitted pair reproduces every hidden swap and no other, and a submission that swaps everything scores no better than one that swaps nothing. A random or constant submission averages zero on both parts. Chance-level systems, the balanced sample template included, land on the platform floor 0.001; a perfect recommender scores 1.0. Higher is better; the grading configuration is Maximize with minimum 0.001 and maximum 1.0. Replacing a growing fraction of cases with random orderings lowers the score smoothly and monotonically. Rows are matched by id, so the physical order of the submitted CSV never affects the result, and the same deterministic scorer is applied to the full, public, and private answer sets. Submission Format Submit one CSV with exactly these two columns in this order: id,prediction aer_0123456789abcdef01234567,DAFBEC-BFACED;ABCDEF-FEDCBA;CABDFE-DAFBEC;... aer_fedcba9876543210fedcba98,BFACED-CABDFE;FEDCBA-ABCDEF;DAFBEC-BFACED;... Copy every id from test.csv exactly once. Each prediction is exactly 24 entries joined by semicolons, one per shortlist of the row in tensor order (the example above is truncated with ...). Each entry is two six-letter strings joined by a single hyphen: first the ordering under brief 1, then under brief 2, each using every letter A through F exactly once with your best candidate first; case and whitespace around entries are tolerated, and the two orderings of an entry may be identical if you believe nothing swaps. Wrong or reordered columns, extra user columns, missing IDs, duplicated IDs, unexpected IDs in a full submission, and a Boolean prediction column are rejected with an explicit error. A single unreadable entry, whether numeric, truncated, missing its second ordering, using a repeated or illegal letter, or otherwise not two slot permutations, contributes zero to both parts for its own shortlist; a row with the wrong number of entries contributes zero for all of its shortlists; the rest of the submission is scored normally. Preregistered Baselines and Shortcut Audit The audit runs constant and reversed orderings, array-index and row-order rotation cycles, per-dimension ascending and descending sort rules, brief-scaled single-dimension sort rules, descriptor-norm and centroid-distance orderings, a nearest-neighbour training-rank lookup, the balanced sample template, and 64 independently salted ID rules, all scored through the shipped grader on every shortlist of every row. Constants, cycles, the template, and ID rules sit at or below 0.01, and the strongest audited no-training rule reaches 0.1274, below every trained control and far below the strong tier; every brief-agnostic rule is additionally capped at half the scale by construction. Three preregistered trained controls score 0.3421, 0.4212, and 0.5622: a flattened whole-row model that ignores the slot structure, a linear brief-by-descriptor slot scorer, and a shared-encoder set network ensemble blended with a slot-aligned boosted ranker; a slot-aligned boosted ranker alone scores 0.5174 and a single set network 0.5467, so the ladder separates flattening, linear scoring, tree scoring, and representation learning. Adjacent gaps are 0.0791 and 0.1409. Across 100 row-level 30/70 visibility assignments, each keeping every geometry cluster whole, the largest public-score standard deviation is 0.0073, the adjacent gaps are 10.90 and 19.41 times that value, and the control order is preserved in every simulated public and private slice. Frontier briefs are more decisive, so every control scores higher on shortlists that carry one: the strong control moves from 0.5386 on shortlists with two in-envelope briefs to 0.5859 on shortlists with at least one frontier brief, the flattened control from 0.3254 to 0.3588. The slice therefore tests whether learned trade-off structure carries beyond the training envelope; it is not a hidden difficulty spike. On the counterfactual tracks the strong control scores 0.5740 on independent pairs, 0.4922 on the 996 tolerance-intervention shortlists and 0.5847 on the 996 emphasis-intervention shortlists, against 0.3506, 0.2842 and 0.3660 for the flattened control; the noise-free oracle that knows the true coefficients reaches 0.6669, 0.5797 and 0.6822 on the same tracks, which bounds what any model can recover there. The difficulty is structural: family-disjoint evaluation geometry, an out-of-envelope brief slice, held-out single-factor intervention tracks, per-case mission pairs with genuine reversals scored as such, keyed nonlinear many-to-fewer descriptors, bounded candidate reuse, no repeated unordered shortlists, and counterfactual variation that caps even a perfect surrogate below the maximum. Slot letters, IDs, array indexes, row order, and leading-letter frequency explain none of the trained performance. The server-generated public/private assignment is audited again after preparation, before agent runs begin. Why It Is Learnable, and How Training and evaluation share one descriptor system, one mission-weight semantics, and one relevance mechanism while using disjoint candidate geometry, so reusable structure exists without any lookup key. For brief c and candidate descriptor x_j, an effective family estimates utility(j | c, x_j) = small_profile_quality(x_j) + mission_tradeoff(c, x_j) + nonlinear_margin_terms(c, x_j) - thresholded_moment_penalty(c, x_j) scores the shortlist once per brief with the same scorer, and submits the slots sorted by estimated utility under each. Because reversal skill rewards exactly the pairs that swap between the two briefs and penalizes swaps predicted elsewhere, it is worth training the brief-dependent part of the scorer explicitly: the two training orderings of every shortlist are a labeled counterfactual pair, and pairwise or listwise objectives on the difference between the two briefs use strictly more signal than learning either ordering alone. Because one scorer must apply to every slot and both briefs, shared-weight candidate encoders, factorization models with a learned geometry representation, gradient-boosted rankers over slot-aligned interaction features, and permutation-equivariant set networks all preserve the needed structure; the geometry side rewards learned nonlinear representations over raw-descriptor linear scoring. Validate on validation_blocks.csv; its blocks were fixed at the geometry-family level before source information was removed from the release. Positioning Aerodynamic machine learning usually exposes the regression object directly: RANS surrogate benchmarks such as AirfRANS, the ML4CFD competition data and AFBench ask a model to predict coefficients or a flow field per geometry, with train and test drawn from overlapping shape distributions and accuracy, rank correlation of predicted coefficients, or out-of-distribution error as the metric, and multi-point shape-optimization benchmarks such as ShapeBench score one weighted objective per design. Ranking and slate benchmarks, in turn, score top-1 or top-k retrieval of one ordering against relevance obtained from logs or human annotation. AeroForge matches none of them. Its scored object is a counterfactual pair: two complete physical orderings of the same shortlist under two briefs, with half of the metric reserved for the change between them, a quantity that any brief-agnostic surrogate, however accurate, scores zero on by construction, and that over-predicting swaps cannot inflate. Generalization is doubly out-of-distribution, with unseen geometry families and a slice of briefs outside the training envelope, and the graded structure of every ordering comes from a mission-weighted composite over real solver measurements. On top of that, a third of the evaluation shortlists are held-out single-factor interventions on the brief, a counterfactual generalization track with no analogue in surrogate or ranking benchmarks: it scores whether a model attributes a reversal to the right mission factor, not merely whether it ranks well on the brief distribution it was trained on. The primary evaluation axis is therefore whether a model recovers the geometry-conditioned preference reversals that the physical composite induces, at every depth of the ordering, under both shifts and under isolated interventions at once. Compute This is a CPU challenge. The tensors are compact; a complete pipeline with block validation, slot-aligned feature construction, pairwise ranking training on both briefs, and inference fits in roughly 10 to 15 minutes on the 10-core CPU tier. A small permutation-equivariant network trained from scratch is feasible; pretrained models and large accelerators are unnecessary. Domain AeroForge is a Recommendation challenge in the learning-to-rank family. Each shortlist is a context-item matching problem: two anonymous mission briefs, acting as contexts, must be scored against one ephemeral six-item candidate shortlist, and the deliverable is the recommended ordering of that shortlist under each brief, for all shortlists of a row. All predictive input lives in the two aligned NumPy modalities; the CSV files carry only opaque IDs, array addresses, blocks, and training orderings. Because candidates exist only inside their own case and item identity is never reused, per-item memorization has no traction: the challenge rewards context-aware utility ranking of the kind used in slate recommenders, applied to a physical screening domain, and scores the counterfactual response to a change of context. Rules and What Not To Use Use only the supplied solver-facing challenge files. Do not use external datasets, geometry libraries, aerodynamic solvers, pretrained models, web lookup, or manual labeling. Do not attempt to identify, retrieve, or reconstruct the upstream corpus, its geometries, or its coefficient tables. Do not use IDs, array indexes, row order, letter frequency, file metadata, or platform metadata as prediction signals. Treat every prediction entry as an ordering of the current shuffled shortlist under the stated brief, never as reusable item labels. Do not probe the evaluation set through repeated submissions or pseudo-label private cases. Submit only the required id,prediction CSV and keep the full solution within the CPU resource limit. &nbsp;
> 0 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## CounterPhase: Resource-Contention Offset Recommendation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72tn4e1cz0j80x12atw70nrh8bnkar
- DOMAIN exactly as displayed: Recommendation
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> CounterPhase: Resource-Contention Offset Recommendation Overview This is a Recommendation challenge over counterfactual launch plans for two machine-learning jobs that must share constrained infrastructure. Starting both jobs at the same instant is not always best. Their accelerator, memory, processor, storage, and network pressure can crest together, producing a short but severe capacity collision. A modest launch offset may separate those peaks without changing either job. The useful offset depends on interactions between the two demand traces, not on the average load of either job alone. Each case supplies one anonymous reference sequence and six anonymous candidate co-run sequences. Every candidate contains exactly the same second-job measurements under a different cyclic launch phase. Recommend the candidate slot with the lowest hidden upper-tail contention utility. The task is not workload classification, anomaly detection, clock recovery, or next-value forecasting. It asks for a deployment action under a learned counterfactual utility. The six candidates are statistically identical when examined separately; only their time-resolved interaction with the reference sequence can distinguish them. Objective For every evaluation case, predict one integer candidate slot: 0, 1, 2, 3, 4, or 5. The correct slot is the counterfactual launch plan that best controls combined upper-tail pressure, simultaneous resource saturation, and sustained four-step overload. Candidate order is randomized independently for every case. Slot numbers have no ordinal or operational meaning. Operational interpretation The reference and candidate panels are two disjoint observations of a paired execution. Four latent capacity pools are used only by the organizer to evaluate the six possible co-runs. The target action minimizes a fixed weighted utility over those pools. Participants do not receive the latent capacity axes or the utility values. They receive independently transformed anonymous panels and labelled training examples. The learning problem is therefore to infer which cross-panel temporal interactions predict harmful co-saturation, then rank the six actions within each case. Data The release contains 448 labelled training cases and 192 evaluation cases. One complete paired execution produces exactly one case and one scored row. The public files are: train.csv, containing id and integer target. test.csv, containing evaluation id values. train_sequences.npz, containing the training id, query, and candidates arrays. test_sequences.npz, containing the corresponding evaluation arrays. sample_submission.csv, containing a format-valid constant template independent of hidden targets. data_manifest.json, containing dimensions, legal labels, and release counts. In each sequence archive, query has shape (cases, 64, 12) and candidates has shape (cases, 6, 64, 12). The embedded id array is the authoritative join key to the CSV. Do not assume that file order has predictive meaning. The two 12-channel panels come from disjoint metric families and are transformed independently. Values are robustly normalized within one execution, resampled over normalized progress, projected into anonymous coordinates, passed through a bounded nonlinearity, and clipped to [-1, 1]. Split design The independent unit is a complete paired execution. Units are partitioned before launch candidates, target slots, or row order are generated. No execution, raw trace, or derived sequence appears in both training and evaluation. Repeated executions from every retained operating stratum occur on both sides so the task measures action learning rather than extrapolation to absent task families. Source-facing names and identifiers are removed. Public case IDs are keyed hashes that do not encode the target, source row, chronology, operating stratum, or launch phase. Because one independent execution becomes one scored row, a public/private visibility assignment cannot split an execution across leaderboard sides. Anti-shortcut construction All six candidates in a case are cyclic rotations of exactly the same values. Candidate means, variances, histograms, extrema, smoothness summaries, missingness, and duration are therefore identical. There is no privileged unshifted action: the optimum is defined by reduced co-saturation, not by restoring an original clock. Target slots are exactly balanced in evaluation and nearly balanced in training. Candidate order and the common cyclic anchor are generated independently of execution identity. A candidate-only classifier, fixed slot rule, identifier lookup, and marginal-load ranking cannot recover the target. Research boundary Prior interference-aware co-location systems generally predict the slowdown of a job pair and then choose a machine placement, resource allocation, or admission decision. Prior cluster schedulers likewise optimize queues of jobs from explicit resource requests or online performance feedback. CounterPhase fixes the job pair and hardware context, withholds semantic counter identities, and instead asks for the best relative launch phase among six complete counterfactual rollouts. Its target is a lower-tail decision over upper-tail multi-resource collision, not a slowdown regression or a clock-alignment label. The combination of disjoint anonymous observation panels, within-case rotation-equivalent actions, learned worst-window utility, and one-shot offset recommendation changes the required solution: neither a standard workload classifier, a static bin-packing rule, nor a temporal synchronization objective supplies the answer. Evaluation The base statistic is six-way Hit@1 accuracy. The leaderboard first removes the exact balanced chance level and then applies a monotone calibration: Scores range from 0.0 to 1.0, and higher is better. A perfect submission scores 1.0. Every constant-slot submission scores 0.0 on the complete balanced evaluation set. Predictions at or below chance also score 0.0; no fraction of the leaderboard score is free. The exponent does not change the ordering of submissions above chance. It spreads the practically useful region while preserving both endpoints. Empirical controls All controls below were evaluated on the frozen 192-case split with the production grader. A direct anonymous-panel cosine matcher scores about 0.063, while a candidate energy-correlation rule scores 0.0. Three compact learned controls using only released training data score approximately 0.23, 0.33, and 0.39. They use a lag-summary multilayer perceptron, a set-wise tree ensemble, and a regularized cross-panel linear model. These results show both a learnable signal and substantial unsaturated headroom. The organizer audit also verifies exact candidate-only distributional invariance, zero train/evaluation unit crossings, oracle score 1.0, constant score 0.0, strict degradation ordering, and stable public/private rankings under equal-quality unit-level perturbations. Modeling guidance A useful solution should compare the reference against every candidate and preserve candidate-axis equivariance. Suitable approaches include lag-aware cross-covariance features, temporal convolutional encoders, attention over paired progress steps, learned upper-tail pooling, or a contrastive pair scorer followed by within-case ranking. Group validation by complete case. Do not split time steps or candidate slots into separate validation rows. Submission format Submit a CSV with exactly two columns:csv id,prediction cor_0123456789abcdef0123,4 cor_abcdef01234567890123,1 ` Every evaluation id must occur exactly once. prediction must be a finite, non-Boolean integer from 0 through 5. Extra columns, extra IDs, missing IDs, duplicate IDs, invalid labels, and reordered columns are structural errors. Submission row order does not affect scoring. Constraints Train only from the files released with this challenge. Do not use external telemetry corpora, pretrained weights, external APIs, or internet retrieval. Produce predictions automatically without manual labeling of evaluation cases. Do not infer targets from identifiers, row order, file order, or serialization artifacts. Compute This is a CPU challenge. The released tensors are compact, and the verified linear, tree, and small-neural controls train in seconds to minutes. A complete solution should comfortably fit within a 10-to-15-minute training budget on the platform CPU tier.
> 0 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.


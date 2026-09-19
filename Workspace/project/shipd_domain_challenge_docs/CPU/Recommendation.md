# CPU Recommendation Challenge Examples

Scrape timestamp: 2026-07-19T00:00:00+05:30

Confirmed CPU examples in this document: 2

These entries are included because the challenge detail page displayed this domain and the challenge is part of the CPU-only challenge collection.

## Masked Scholarly Neighbor Retrieval

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ewk1y9ff0grt9wpz38xbrmh8ah6kh
- DOMAIN exactly as displayed: Recommendation
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> You are given de-identified representations of real scholarly articles sampled from a public scholarly metadata index. The raw source contains titles, reconstructed abstracts, venues, institutions, keywords, and a topic hierarchy, but the public files contain no source ids, DOI values, raw text, venue names, institution names, keyword strings, or topic names.
> This is a CPU-only recommendation and retrieval challenge. For each held-out query article, return a ranked list of candidate article ids that are scholarly neighbors of the query. A relevant neighbor is a candidate article that shares the hidden fine-grained source topic with the query. Solvers rank candidate articles rather than predicting topic labels.
> Each article has a 96-dimensional semantic vector built by projecting sentence-level TF-IDF representations into a dense latent space and pooling the title, abstract sentences, and keyword phrase. The vocabulary, projection basis, sentence text, and raw metadata are not released, so the vectors are not reversible into the source text. Coarse metadata buckets are provided separately.
> The split is deliberately out of domain. Entire scholarly subfields are assigned either to labeled training queries or to hidden test queries, never both. Consequently, all fine-grained test topics are also absent from the labeled training queries. Candidate articles cover both partitions, so success requires learning a generalizable similarity or ranking rule rather than memorizing topic-specific labels.
> Evaluation
> Submissions are scored with mean average precision at 10, abbreviated MAP@10. Higher is better, with a maximum score of 1.0.
> For each test query:
> relevant: the set of hidden relevant candidate ids for that query.
> predicted: the ordered list of up to 10 candidate ids submitted for that query.
> hit_at_rank_r: 1 if the candidate at rank r is relevant, otherwise 0.
> hits_so_far_r: the number of relevant candidates found from rank 1 through rank r.
> &nbsp;
> precision_at_r = hits_so_far_r / r
> average_precision_at_10 = (
> sum(precision_at_r for each rank r <= 10 where hit_at_rank_r == 1) / min(len(relevant), 10)
> )
> score = mean(average_precision_at_10 over all test queries)
> &nbsp;
> The placeholder `NO_CANDIDATE` receives zero credit. A malformed prediction, duplicate candidate, mixed placeholder, or list longer than 10 gives that query a score of 0.0 while grading continues. Missing or duplicate query rows, a mismatched query-id set, or incorrect columns make the whole submission structurally invalid.
> &nbsp;
> ## Dataset
> The prepared public dataset contains:
> &nbsp;
> - `public/train_queries.csv`: labeled query articles from training subfields.
> - `public/test_queries.csv`: held-out query articles from disjoint subfields.
> - `public/candidate_articles.csv`: the candidate article pool to rank for every query.
> - `public/train_query_embeddings.npy`: 96-dimensional vectors aligned with `train_queries.csv`.
> - `public/test_query_embeddings.npy`: 96-dimensional vectors aligned with `test_queries.csv`.
> - `public/candidate_embeddings.npy`: 96-dimensional vectors aligned with `candidate_articles.csv`.
> - `public/sample_submission.csv`: dummy placeholder predictions that score 0.0.
> - `private/answers.csv`: hidden relevant candidate ids for grading.
> &nbsp;
> The row at `embedding_row` in the corresponding `.npy` file belongs to that CSV record. All embedding arrays are `float32` and have shape `(number_of_csv_rows, 96)`.
> &nbsp;
> Query and candidate CSV columns:
> &nbsp;
> - `query_id` or `candidate_id` (string): opaque row id assigned after deterministic splitting.
> - `embedding_row` (int): row index into the matching embedding array.
> - `publication_period` (string): coarse publication-period bucket.
> - `language` (string): normalized language bucket.
> - `work_type` (string): normalized scholarly-work type bucket.
> - `source_type` (string): normalized source type bucket.
> - `oa_status` (string): normalized open-access status bucket.
> - `title_length_bucket` (string): bucketed title word count.
> - `abstract_length_bucket` (string): bucketed abstract word count.
> - `author_count_bucket` (string): bucketed author count.
> - `country_count_bucket` (string): bucketed count of author countries.
> - `institution_count_bucket` (string): bucketed count of distinct institutions.
> - `reference_count_bucket` (string): bucketed referenced-work count.
> - `citation_count_bucket` (string): bucketed cited-by count at source-fetch time.
> - `location_count_bucket` (string): bucketed source-location count.
> &nbsp;
> `train_queries.csv` also contains `relevant_candidate_ids`, a space-separated string of candidate ids relevant to that training query. `answers.csv` has the same `query_id,relevant_candidate_ids` structure for hidden test queries.
> &nbsp;
> ## Submission
> Submit a CSV named `submission.csv` with exactly these columns:
> &nbsp;
> - `query_id` (string): the row identifier from `test_queries.csv`; include every test query exactly once.
> - `candidate_ids` (string): up to 10 ranked candidate ids from `candidate_articles.csv`, separated by spaces, or the single placeholder `NO_CANDIDATE`.
> &nbsp;
> Example `submission.csv`:
> &nbsp;
> query_id,candidate_ids
> q_00000,cand_00104 cand_01092 cand_00411 cand_00077 cand_02018
> q_00001,cand_00333 cand_00291 cand_01840
> q_00002,NO_CANDIDATE
> &nbsp;
> Requirements:
> &nbsp;
> - Include exactly one row per test query id and include the header row.
> - Use only candidate ids from `candidate_articles.csv` or the single placeholder `NO_CANDIDATE`.
> - Do not combine `NO_CANDIDATE` with candidate ids.
> - Do not submit more than 10 candidate ids for any query.
> - Do not include missing ids, duplicate query ids, extra query ids, extra columns, probabilities, explanations, or markdown.
> &nbsp;
> ## What Not To Use
> Use only the provided public files and libraries already available in the Kaggle/Eris runtime. The challenge is designed for CPU-only solutions under a 1.5 hour limit on 10 CPU cores and 62 GB RAM.
> &nbsp;
> Do not use external scholarly metadata databases, search engines, DOI resolvers, source article pages, topic-name tables, exact titles, exact abstracts, raw source files, external metadata dumps, runtime downloads, or package installation.
> &nbsp;
> Do not hard-code per-query predictions, infer labels from row order, manually label test queries, exploit malformed CSV parsing, or use private files.
> &nbsp;
> ## Modeling Guidance
> Useful CPU approaches include cosine or angular nearest-neighbor retrieval in the semantic space, metric learning on labeled training queries, local candidate-density correction, rank aggregation with coarse metadata similarity, and small retrieval ensembles. Because test subfields are absent from training labels, validation should also hold out complete training subfields rather than randomly splitting individual rows.
> &nbsp;

Inspiration note: Useful because it frames recommendation as masked scholarly neighbor retrieval, using graph/text proximity and ranking-style outputs instead of a generic classifier.

## Predicting a Species' Unrecorded Ecological Associates Across Clades

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70av85pmyq2xkp19whgk1vpn8agykd
- DOMAIN exactly as displayed: Recommendation
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
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
> Predicting a Species' Unrecorded Ecological Associates Across Clades
> Overview
> Field surveys never capture every ecological association a species has — every other species
> it pollinates, eats, is eaten by, or is parasitised by. Records are always partial: some
> associates are documented, many are missed. A recurring question in ecology is therefore to
> infer, from the associates already documented for a species, which other species it is
> likely associated with.
> In this challenge each row is one focal species together with a partial list of its
> documented associates. From that partial list, infer the species' undocumented associates,
> drawn from a fixed set of 200 candidate species (labelled i0 … i199). A species may have
> one or several undocumented associates.
> The signal is how associates pattern together across the whole collection of species — but
> the twist is that the test species belong to taxonomic clades absent from the training
> set. A solution must therefore generalise association patterns across the tree of life,
> to lineages it has never seen, rather than memorising them.
> You are given 2,660 training species (partial records → undocumented associates) and must
> infer the undocumented associates for each of the 1,249 test species from unseen clades.
> Data provenance
> The records are built from a large public-domain (CC0) aggregation of real
> species-association observations (who pollinates / eats / parasitises whom), compiled from
> many field studies and natural-history collections. For each focal species we take the
> associates it is recorded with. Species are relabelled i0 … i199; their real identities are
> not provided. Because field sampling is incomplete and imperfect, the records are partial and
> noisy.
> Encoding
> Input format (one row)
> <observed partner labels, space-separated>
> Example input:
> i12 i45 i61 i103 i118
> Each label i0 … i199 is a partner species from the fixed vocabulary; the meaning of each
> label is not given.
> Target
> The held-out partners of the same focal species, as space-separated labels:
> i7 i88 i140
> Dataset
> Arrays are in NumPy .npz format.
> train.npz — 2,660 training neighbourhoods. Keys:
> ids — (2660,) int64 row identifiers, 0 … 2659.
> input_str — (2660,) string, the observed partner labels.
> target_str — (2660,) string, the held-out partner labels.
> test.npz — 1,249 neighbourhoods to complete. Keys: ids (int64, 2660 … 3908),
> input_str (string). The held-out partners are withheld.
> IDs are globally unique across the dataset: test ids continue exactly where the
> training ids end, so no id appears in both splits.
> sample_submission.csv — a correctly-formatted example submission (predicts the four
> most common partners for every neighbourhood).
> The train and test neighbourhoods are split by the focal species' clade (taxonomic
> order), so the test focals belong to clades not seen in training.
> Evaluation
> Micro-averaged F1 over the partner labels of all 1,249 test neighbourhoods (higher is
> better, range 0–1).
> For each neighbourhood, the recommended label set is compared to the held-out label set.
> True positives, false positives, and false negatives are pooled across all test
> neighbourhoods, then:
> precision = TP / (TP + FP)
> recall    = TP / (TP + FN)
> F1        = 2 × precision × recall / (precision + recall)
> Worked example
> Held-out partners: i7 i88 i140. You recommend i7 i90 i140.
> i7 and i140 are in both → 2 TP. i90 is recommended but not held-out → 1 FP. i88 is
> held-out but not recommended → 1 FN. This neighbourhood contributes TP=2, FP=1, FN=1.
> Submission format
> Submit submission.csv with exactly two columns and one row per test id
> (1,249 rows plus a header):
> id (int) — the test id from test.npz.
> prediction (string) — the predicted associates as space-separated labels i0 … i199, or
> an empty string to predict none.
> Example:
> id,prediction
> 2660,i7 i88 i140
> 2661,i3 i51
> 2662,i0
> Every id in test.npz must appear exactly once. The grader rejects labels outside
> i0 … i199, duplicate labels within a row, duplicate ids, and missing/extra ids.
> What not to use
> No external data. Train only on train.npz.
> No test labels. The held-out partners are withheld — produce recommendations purely
> from the test inputs and a model learned on the training data.
> Reproducible inference. Fixed seeds, deterministic decoding — re-running on test.npz
> must reproduce the same submission.csv.

Inspiration note: Useful because it makes recommendation feel like ecological link completion under clade shift, with a compact set-valued output and a nice generalization constraint.

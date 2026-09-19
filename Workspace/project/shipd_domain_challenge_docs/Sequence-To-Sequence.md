# Sequence To Sequence Challenge Examples

Scrape timestamp: 2026-07-01T06:39:43+05:30

Confirmed examples in this document: 33

These entries are included only because the challenge detail page displayed this target domain. Titles were not used for classification.

## Byte-Level LLM Pretraining: The MIPS32 Autopsy
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71wk4sghz0yr7s86ht6vk0vn8445ne
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Hard
- GPU: H100
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: komilpamar ranked 1st (leaderboard #4, score 0.7158); hoang_phuc_6868 ranked 2nd (leaderboard #8, score 0.7125); gallantknight ranked 3rd (leaderboard #41, score 0.6983); arin ranked #4 (leaderboard #21, score 0.6917)

Full challenge description from page:

> Overview
> In the high-stakes world of systems programming and malware analysis, an optimizing compiler acts like a destructive, one-way cryptographic hash. When high-level C code is translated to machine code using Aggressive Optimization -O3), loops are unrolled, instructions are reordered, and all human-readable semantic clues are obliterated.
> The Challenge: This is a foundational, from-scratch language model training challenge. You are provided with roughly 10,000 algorithmic C functions cross-compiled to the embedded MIPS32 architecture. Because standard pretrained foundation models are utterly blind to MIPS bytecode, you cannot rely on zero-shot inference, agentic wrappers, or simple fine-tuning.
> Your task is to train a custom byte-level language model from scratch (e.g., a custom miniature Transformer architecture, or a linear-scaling State-Space Model like Mamba) capable of ingesting raw hexadecimal machine noise and mapping it back to the exact, chronologically ordered sequence of C Standard Library calls (e.g., ["scanf", "malloc", "printf", "free"]) that the original algorithm executed.
> Hardware & Execution: To support the training and execution of custom foundation architectures, this challenge provisions elite compute. Your training and inference pipeline must run within the platform limits utilizing an NVIDIA H100.
> The Pretraining Traps (Why Standard Models Fail)
> To enforce the "train from scratch" requirement, this dataset relies on several adversarial mechanics that neutralize standard API wrappers:
> The Tokenizer Massacre: Standard pretrained models use Byte-Pair Encoding (BPE) optimized for human language. When fed a 2,000-character string of raw MIPS hex, standard BPE tokenizers chunk the data arbitrarily, destroying the 4-byte architectural boundaries of the instructions. You MUST build and train a custom Byte-Level Tokenizer for your model.
> The "O3" Scramble: Because the code was compiled at -O3, the sequence of library calls in the hex does not cleanly mirror the source code linearly. The compiler has vectorized math and shifted conditional branches, forcing your model to learn actual execution flow rather than simple text matching.
> Quadratic Context Choking: A single algorithmic function can produce thousands of characters of pure hexadecimal. You will need to optimize your model's attention mechanism (e.g., FlashAttention-2 on the H100) or pivot to linear-scaling architectures to prevent Out-Of-Memory errors on these massive context windows.
> Evaluation
> Submissions are evaluated using Mean Normalized Edit Distance (NED).
> Because you are predicting a chronological sequence of events, standard accuracy or binary log-loss is insufficient. You will receive partial credit for predicting the correct library calls with minor chronological transposition or omission errors.
> For a single row, the Normalized Edit Distance is calculated as:
> NED = 1.0 - [ LevenshteinDistance(Y_true, Y_pred) / max(Length(Y_true), Length(Y_pred)) ]
> A perfect chronological match yields 1.0.
> A completely incorrect sequence (or a malformed JSON output) yields 0.0.
> The final leaderboard score is the mean of the NED across all rows in the test set.
> Goal: Maximize this score. The closer to 1.0, the better.
> Dataset
> You are provided with a strictly constrained dataset of 9,958 compiled machine code samples.
> File Descriptions
> train.csv: Contains exactly 7,958 training samples with both the raw hex inputs and the ground truth sequence labels.
> test.csv: Contains exactly 2,000 test samples with the labels hidden.
> sample_submission.csv: A dummy submission file demonstrating the correct JSON-string array format.
> Data Dictionary
> | Column | Type | Description |
> |---|---|---|
> | id | String | A unique identifier for the compiled algorithm (e.g., bin_87190035f8cb2e13). |
> | mips_hex_string | String | The fully stripped, -O3 optimized executable .text section of the MIPS32 binary, represented as a continuous, dense hexadecimal string. (Present in both train and test). |
> | target_sequence | String | The ground truth label formatted as a valid JSON array string. An ordered sequence of standard C library functions (e.g., ["scanf", "abs", "printf"]). (Present only in train.csv). |
> Submission
> Submit a CSV file with exactly 2,000 rows. Your submission must include the id column and exactly one target column (String) named target_sequence.
> Crucial: The target_sequence MUST be a valid, stringified JSON array. If your model hallucinates conversational text (e.g., "The sequence is ["scanf"]"), outputs a raw Python list instead of a JSON string, or misses the column name, the automated grader will fail to parse it and assign a score of 0.0 for that row.
> | id | target_sequence |
> |---|---|
> | bin_f0653df1d6e434de | ["scanf", "malloc", "printf"] |
> | bin_1e5db8f54cb24ffc | ["puts"] |
> | bin_8ce0e4efd08b3b34 | [] |

Inspiration note: Useful because it turns noisy context into an ordered or generated sequence, with an output shape that can be scored by exact, semantic, or alignment-aware metrics.

## Clause Fragment Ordering Challenge
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79bnsvp46bwbcqwa7q5dfq3d827t6n
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: kindasomethin ranked 1st (leaderboard #10, score —); stetsenko ranked 2nd (leaderboard #15, score —)

Full challenge description from page:

> Overview
> Legal contracts are structured documents where meaning depends heavily on logical flow, cross-references, and sequential reasoning. Clauses are carefully ordered to define obligations, rights, exceptions, and conditions in a coherent progression. Disrupting this order can obscure meaning and break logical dependencies.
> In this competition, participants are given shuffled sentence fragments extracted from real-world legal contract clauses. The fragments are derived from real-world legal contract filings in the insurance and financial domains. Each clause has been segmented into 5–10 semantically meaningful fragments and randomly reordered.
> Objective
> Your task is to reconstruct the original correct order of the shuffled fragments for each clause.
> For every sample in the dataset:
> You are provided a set of shuffled text fragments.
> You must predict the correct sequential ordering that restores the original clause structure.
> The output should be a permutation of fragment indices representing the reconstructed order.
> Evaluation
> Submissions are evaluated using normalized Kendall–Tau distance, computed independently for each sample after strict ID alignment.
> The final leaderboard score is:
> Score=1.0−average normalized Kendall–Tau distance\textbf{Score} = 1.0 - \text{average normalized Kendall–Tau distance}Score=1.0−average normalized Kendall–Tau distance
> 1.0 = perfect ordering
> 0.0 = completely reversed ordering (worst case)
> Higher scores indicate better performance.
> Scoring Procedure
> For each sample:
> Submission rows are matched to ground-truth rows strictly by id.
> The predicted fragment order must be a valid permutation of the true fragment indices.
> The normalized Kendall–Tau distance is computed as: number of discordant fragment pairs/(nC2)
> Where:
> n= number of fragments in the sample
> (nC2)=n(n−1)/2 is the maximum possible number of pairwise comparisons
> The final leaderboard score is the mean score across all samples.
> Why Kendall–Tau?
> Kendall–Tau is ideal for clause and fragment ordering because it:
> Measures relative ordering accuracy, not just exact matches
> Provides partial credit for nearly correct orderings
> Is a standard metric for ranking and permutation tasks
> Is robust to local swaps and minor perturbations
> Unlike exact-match accuracy, Kendall–Tau captures how structurally coherent a predicted ordering is.
> Dataset
> The prepared dataset consists of three CSV files in the public directory:
> public/train.csv
> Training set with correct labels for model development.
> | Column        | Type   | Description                                                   |
> | --------------| ------ | --------------------------------------------------------------|
> | id            | string | Unique sample identifier (e.g., sample_0)                     |
> | fragments     | string | Pipe-separated (|) shuffled clause fragments                  |
> | correct_order | string | Comma-separated indices indicating the original fragment order|
> Statistics:
> 152 training samples
> 5-10 fragments per sample
> All text anonymized ([ORG], [DATE], [AMOUNT], [NUM], [PERCENT], [DUR], [PERSON])
> Average fragment length: 150-300 characters
> public/test.csv
> Test set without labels (fragments only).
> | Column      | Type   | Description                                                |
> | ----------- | ------ | ---------------------------------------------------------- |
> | `id`        | string | Unique sample identifier (e.g., `sample_152`)              |
> | `fragments` | string | Pipe-separated shuffled clause fragments (no order labels) |
> Statistics:
> 83 test samples
> 5-10 fragments per sample
> Same anonymization as training set
> public/sample_submission.csv
> Template file showing required submission format.
> | Column            | Type   | Description                                |
> | ----------------- | ------ | ------------------------------------------ |
> | `id`              | string | Sample identifier from `test.csv`          |
> | `predicted_order` | string | Comma-separated indices of predicted order |
> Submission
> Submit a CSV file with the following format:
> | Column            | Type   | Description                                            |
> | ----------------- | ------ | ------------------------------------------------------ |
> | `id`              | string | Sample identifier from `test.csv`                      |
> | `predicted_order` | string | Comma-separated indices in predicted order (0-indexed) |
> Sample Submission:
> | id         | predicted_order |
> | ---------- | --------------- |
> | sample_152 | 0,1,2,3,4       |
> | sample_153 | 3,1,0,2         |
> | sample_154 | 1,2,0           |
> | ...        | ...             |
> Requirements:
> Must contain exactly 83 rows (one per test sample, plus header)
> Must include header row: id, predicted_order
> Each predicted_order must be a valid permutation of indices (e.g., for 5 fragments: 0,1,2,3,4 or 4,2,0,1,3)
> All sample IDs from test.csv must be included
> CSV encoding: UTF-8
> No extra columns or whitespace
> Submissions will be rejected if:
> IDs do not exactly match the ground truth IDs
> Duplicate IDs are present
> Fragment counts mismatch
> The predicted order is not a valid permutation
> Order format is not comma-separated integers

Inspiration note: Useful because it turns noisy context into an ordered or generated sequence, with an output shape that can be scored by exact, semantic, or alignment-aware metrics.

## Constrained Biomedical Text Simplification
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ewc05s9jyke11nnrqndjjex8354m4
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: ahmed_salah7 ranked 1st (leaderboard #6, score —); haidang ranked 3rd (leaderboard #24, score —); shivank ranked #7 (leaderboard #27, score —)

Full challenge description from page:

> Overview
> Biomedical research papers use complex technical language inaccessible to general audiences. This challenge asks you to generate accessible summaries of biomedical research abstracts under per-example six-axis constraints: lexical exclusion (restricted terms that must NOT appear), lexical inclusion (required anchor terms that MUST appear), readability calibration (a target Flesch-Kincaid grade level each summary must match), relational anchoring (concept link pairs that must co-occur within the same sentence), evaluation emphasis (per-example scoring weight profiles with ranges from 0.03 to 0.47 that shift evaluation priorities based on constraint difficulty), and behavioral verification through constraint variants (paired test entries sharing the same abstract but with different constraint profiles, where identical outputs are penalized). This six-axis constraint setup transforms free-form summarization into a structurally constrained text generation problem requiring simultaneous vocabulary control, per-example readability calibration, relationship preservation, evaluation-aware adaptive optimization, and demonstrated constraint responsiveness.
> You must balance six competing objectives: content faithfulness to the source (ROUGE-L), vocabulary novelty (abstractiveness), compliance with per-example term restrictions (constraint compliance), inclusion of required anchor terms (required term coverage), per-example readability calibration (readability proximity to the target FK grade level), and preservation of concept link relationships (concept link coverage). Crucially, each test example specifies its own scoring weight profile (with weights ranging from 0.03 to 0.47) that shifts evaluation emphasis toward whichever axes are most difficult for that example, requiring evaluation-aware adaptive optimization rather than a uniform generation strategy. Additionally, approximately 18% of test entries are constraint variants: pairs of entries that share the same abstract but specify different constraint profiles. A variant adaptation multiplier penalizes agents that produce identical summaries for these paired entries, directly verifying that agents genuinely respond to constraint differences rather than applying template strategies.
> You are provided with a training set of preprocessed biomedical abstracts paired with expert written accessible summaries. Each row also includes biomedical subdomain keywords, a set of restricted terms derived from corpus level document frequency analysis, a set of required anchor terms derived from author assigned keywords, and a target Flesch-Kincaid readability grade level derived from the reference summary. Your task is to produce accessible summaries for a held out set of test abstracts that avoid using the specified restricted terms, include the required anchor terms, and match the target readability level. The abstracts cover a wide range of biomedical topics including genetics, cell biology, ecology, neuroscience, and epidemiology.
> Abstracts have been preprocessed and contain approximately 120 words on average. The corresponding accessible summaries contain approximately 177 words on average. Summaries should simplify technical terminology while preserving key findings, introducing novel vocabulary, including all required anchor terms, excluding all restricted terms, and matching the per-example target readability level. Reference summaries average 51% novel unigrams (words not found in their source abstract). Target readability grades range from 10 to 20 on the Flesch-Kincaid scale, requiring agents to vary simplification depth per example.
> Evaluation
> Submissions are scored using a per-example weighted composite metric. Each test row specifies its own scoring weight profile in the scoring_emphasis column, and the final score is the mean of per-row weighted composites:
> row_score = w_rouge * rouge_l + w_abs * abstractiveness + w_comp * constraint_compliance + w_req * required_term_coverage + w_read * readability_proximity + w_link * concept_link_coverage
> final_score = mean(row_score for all test rows)
> Where w_rouge, w_abs, w_comp, w_req, w_read, and w_link are read from the scoring_emphasis column for each row. Weights are derived per example from constraint difficulty and range from approximately 0.03 to 0.47. Default fallback weights (rouge=0.30, abs=0.20, comp=0.20, req=0.10, read=0.10, link=0.10) apply only when scoring_emphasis is missing.
> ROUGE-L F1 (default weight 0.30): measures the longest common subsequence between your predicted summary and the reference summary at the word level. Precision and recall are computed from the LCS length, and the F1 score is their harmonic mean
> Abstractiveness (default weight 0.20): the fraction of words in your predicted summary that do not appear in the source abstract. This penalizes extractive copying and rewards genuine vocabulary transformation
> Constraint compliance (default weight 0.20): the fraction of restricted terms from the restricted_terms column that do NOT appear as words in your predicted summary (case insensitive word match). For example, if an example has 5 restricted terms and your summary contains 1 of them, the compliance score is 4/5 = 0.80. Examples with no restricted terms receive full compliance (1.0)
> Required term coverage (default weight 0.10): the fraction of required anchor terms from the required_terms column that DO appear as words in your predicted summary (case insensitive word match). For example, if an example has 3 required terms and your summary contains 2 of them, the coverage score is 2/3 = 0.67. Examples with no required terms receive full coverage (1.0)
> Readability proximity (default weight 0.10): measures how close your summary's Flesch-Kincaid grade level is to the per-example target_readability value. The Flesch-Kincaid grade is computed as FK = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59. Full credit is given when the summary FK grade is within 1 grade level of the target. Beyond that, the score decays linearly to zero at 5 grade levels away: max(0, 1 - (|FK_pred - target| - 1) / 4)
> Concept link coverage (default weight 0.10): the fraction of concept link pairs from the concept_links column that are satisfied. A concept link pair (e.g., term1:term2) is satisfied when both terms appear in the same sentence of your predicted summary (case insensitive word match). For example, if an example has 3 concept link pairs and your summary co-locates both terms in the same sentence for 2 of them, the coverage score is 2/3 = 0.67. Examples with no concept links receive full coverage (1.0)
> Actual weights for each component vary per example based on the scoring_emphasis profile, with individual weights ranging from 0.03 to 0.47 depending on constraint difficulty.
> Variant adaptation multiplier: Approximately 18% of test rows are constraint variants, paired entries that share the same abstract but have different constraint profiles (different restricted terms, required terms, and target readability). These pairs are linked by the variant_group column. For each variant pair, a Jaccard distance is computed between the two predicted summaries. Both rows in the pair receive a multiplier: score *= 0.85 + 0.15 * jaccard_distance. If the two predictions are identical (jaccard_distance = 0), both receive a 15% penalty (multiplier = 0.85). If the predictions are completely different (jaccard_distance = 1), no penalty is applied (multiplier = 1.0). Non-variant rows are unaffected.
> The final score is the mean of all per-row weighted composites (including variant multipliers) across all test examples. Higher scores are better.
> Dataset
> Files
> train.csv — Training data containing preprocessed biomedical abstracts paired with accessible summaries, subdomain keywords, and restricted terms
> test.csv — Test abstracts, keywords, and restricted terms for which you must generate accessible summaries
> sample_submission.csv — Example submission file showing the required format
> Features
> id — Unique integer identifier for each row
> abstract — The preprocessed biomedical research abstract
> keywords — Newline separated biomedical subdomain tags describing the research area (e.g., genetics, neuroscience, epidemiology)
> restricted_terms — Pipe delimited list of up to 5 technical terms that must not appear verbatim in the generated summary (e.g., braziliensis|phosphate|cytochrome|dimeric|dimerization). These terms are derived from corpus level document frequency and represent domain specific vocabulary that should be paraphrased or omitted
> required_terms — Pipe delimited list of up to 3 anchor terms that must appear verbatim in the generated summary (e.g., genetics|infection|protein). These terms are derived from author assigned keywords that appear in the abstract, representing core concepts that must be preserved in the accessible summary
> target_readability — Integer Flesch-Kincaid grade level (10 to 20) that the generated summary should match. Each example has a different target derived from the reference summary's readability, requiring per-example calibration of simplification depth
> concept_links — Pipe delimited list of up to 3 colon separated concept link pairs that must co-occur within the same sentence of the generated summary (e.g., cells:tissue|protein:function|genetic:disease). These pairs are derived from content words that co-occur in reference summary sentences and represent key conceptual relationships that must be preserved. Pairs are selected by specificity (rarest co-occurring word pairs first) and never overlap with that example's restricted terms
> scoring_emphasis — Pipe delimited key=value pairs specifying the evaluation weight profile for each example (e.g., rouge=0.18|abs=0.28|comp=0.22|req=0.12|read=0.10|link=0.10). Weights are derived from continuous per-example constraint difficulty scores: each constraint axis contributes a proportional bonus up to +0.40 based on its difficulty level, then weights are normalized to sum to 1.0. Individual weights range from 0.03 to 0.47, meaning some examples are heavily content-dominated (high rouge weight) while others are heavily constraint-dominated (high comp or abs weight). Agents should read these weights and adapt generation strategy to prioritize the most heavily weighted components for each example
> variant_group — Integer linking constraint-variant pairs. Approximately 18% of test entries share an abstract with another entry but have different constraint profiles (different restricted terms, required terms, and target readability). Both entries in a pair share the same variant_group value. Agents that produce identical summaries for variant pairs receive a 15% score penalty on those rows. Empty for standalone entries and all training entries
> summary — The corresponding accessible summary in plain language (training data only)
> Submission
> Submissions must be in CSV format with the following columns:
> id — The integer identifier matching each row in test.csv
> summary — Your predicted accessible summary for the corresponding abstract. Must not contain any of the restricted terms specified in the corresponding row of test.csv
> id,summary
> 0,This study examines how kidney cells develop...
> 1,Researchers investigated a fungal disease...
> Requirements:
> File must contain exactly the same number of rows as test.csv
> Each id in test.csv must appear exactly once
> No missing values are allowed
> Each summary should be a coherent plain language description of the corresponding abstract
> Summaries should target 120 to 200 words for conciseness
> Summaries must avoid using the restricted terms listed for each example
> Summaries must include the required anchor terms listed for each example
> Summaries should preserve concept link relationships by co-locating each concept link pair within the same sentence
> Summaries should be calibrated to the target Flesch-Kincaid readability grade level specified for each example
> Agents should adapt generation strategy based on the per-example scoring_emphasis profile, prioritizing components with higher weights for each example
> Some test entries share the same abstract with different constraint profiles (linked by variant_group). Agents should produce different summaries for each entry in a variant pair to avoid the 15% adaptation penalty

Inspiration note: Useful because it turns noisy context into an ordered or generated sequence, with an output shape that can be scored by exact, semantic, or alignment-aware metrics.

## Cross-Lingual Cloze Alignment Challenge
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a8bjv91416trr9657jbe2ss82xfww
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: fate1997 ranked 1st (leaderboard #1, score —)

Full challenge description from page:

Overview
Text simplification is a core NLP task with applications in education, accessibility, and content adaptation. In this challenge, you must build a system that takes complex text and generates three simplified versions at different reading levels.
Unlike standard text simplification benchmarks that target a single output level, this challenge requires multi-target generation: for each input passage, your model must simultaneously produce simplifications at three distinct complexity levels. Lower levels demand shorter sentences, simpler vocabulary, and more concrete language, while higher levels can handle slightly more detail and complexity.
Task
Given an original text passage, generate three simplified versions at increasing complexity:
level_1 -- the most simplified version (very short, very simple words, concrete concepts only)
level_2 -- a moderately simplified version (short, simple, slightly more detail than level 1)
level_3 -- the least simplified version (simple but can include a bit more context and slightly longer sentences)
Evaluation
Submissions are scored using a composite metric that combines content quality with proper level differentiation:
Score = 0.75 x Average_ROUGE_L + 0.25 x OrderingScore
Average ROUGE-L F1 (weight 0.75): ROUGE-L measures the longest common subsequence between your prediction and the reference at the token level. F1 balances precision and recall. This is computed separately for each level and then averaged across all three levels.
OrderingScore (weight 0.25): The fraction of test examples where the word counts of your three outputs follow the expected ordering: len(level_1) < len(level_2) < len(level_3). This rewards models that properly differentiate between complexity levels rather than producing identical or incorrectly ordered outputs.
The final score ranges from 0.0 to 1.0 (higher is better).
Submission Format
Your submission must be a CSV file with the following columns:
id (integer) -- the unique identifier for each test example
level_1 (string) -- your simplified text at level 1
level_2 (string) -- your simplified text at level 2
level_3 (string) -- your simplified text at level 3
The file must include a header row. Row order does not matter. Example:
id,level_1,level_2,level_3 15458,Dogs are pets.,Dogs are friendly pets that live with people.,Dogs are friendly household pets that have lived with people for thousands of years. 15459,Water is wet.,Water is a liquid we drink every day.,Water is a clear liquid that is essential for all living things on Earth.
See sample_submission.csv for the expected format.
Dataset
The training set contains 15,458 examples of text passages paired with human-written simplified versions at three levels. The test set contains 1,718 examples for which you must generate simplifications.
File descriptions
train.csv -- training data with original text and all three simplified target columns
test.csv -- test data with original text only (no targets)
sample_submission.csv -- a correctly formatted example submission with placeholder text
Data fields
id (integer) -- unique identifier for each example
text (string) -- the source text passage to be simplified (typically graduate-level reading difficulty)
level_1 (string) -- (train only) human-written simplification at the most simplified level (average ~16 words)
level_2 (string) -- (train only) human-written simplification at the intermediate level (average ~19 words)
level_3 (string) -- (train only) human-written simplification at the least simplified level (average ~24 words)
Key characteristics
Source passages are written at a high reading difficulty and average ~134 words
Level 1 simplifications average ~16 words (roughly 88% reduction from original)
Level 2 simplifications average ~19 words (roughly 86% reduction)
Level 3 simplifications average ~24 words (roughly 82% reduction)
Simplifications are not mere truncations -- they rephrase content using level-appropriate vocabulary and sentence structure
The three target levels produce progressively more detailed output as the level increases

Inspiration note: Useful because it turns noisy context into an ordered or generated sequence, with an output shape that can be scored by exact, semantic, or alignment-aware metrics.

## Multi-Level Text Simplification
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ds58ek7nbyf3dkm30spb84h833s4y
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: hoang_phuc_6868 ranked 1st (leaderboard #8, score —); nxify ranked 2nd (leaderboard #17, score —); mikegoodman ranked 3rd (leaderboard #34, score —)

Full challenge description from page:

> Overview
> Text simplification is a core NLP task with applications in education, accessibility, and content adaptation. In this challenge, you must build a system that takes complex text and generates three simplified versions at different reading levels.
> Unlike standard text simplification benchmarks that target a single output level, this challenge requires multi-target generation: for each input passage, your model must simultaneously produce simplifications at three distinct complexity levels. Lower levels demand shorter sentences, simpler vocabulary, and more concrete language, while higher levels can handle slightly more detail and complexity.
> Task
> Given an original text passage, generate three simplified versions at increasing complexity:
> level_1 -- the most simplified version (very short, very simple words, concrete concepts only)
> level_2 -- a moderately simplified version (short, simple, slightly more detail than level 1)
> level_3 -- the least simplified version (simple but can include a bit more context and slightly longer sentences)
> Evaluation
> Submissions are scored using a composite metric that combines content quality with proper level differentiation:
> Score = 0.75 x Average_ROUGE_L + 0.25 x OrderingScore
> Average ROUGE-L F1 (weight 0.75): ROUGE-L measures the longest common subsequence between your prediction and the reference at the token level. F1 balances precision and recall. This is computed separately for each level and then averaged across all three levels.
> OrderingScore (weight 0.25): The fraction of test examples where the word counts of your three outputs follow the expected ordering: len(level_1) < len(level_2) < len(level_3). This rewards models that properly differentiate between complexity levels rather than producing identical or incorrectly ordered outputs.
> The final score ranges from 0.0 to 1.0 (higher is better).
> Submission Format
> Your submission must be a CSV file with the following columns:
> id (integer) -- the unique identifier for each test example
> level_1 (string) -- your simplified text at level 1
> level_2 (string) -- your simplified text at level 2
> level_3 (string) -- your simplified text at level 3
> The file must include a header row. Row order does not matter. Example:
> id,level_1,level_2,level_3 15458,Dogs are pets.,Dogs are friendly pets that live with people.,Dogs are friendly household pets that have lived with people for thousands of years. 15459,Water is wet.,Water is a liquid we drink every day.,Water is a clear liquid that is essential for all living things on Earth.
> See sample_submission.csv for the expected format.
> Dataset
> The training set contains 15,458 examples of text passages paired with human-written simplified versions at three levels. The test set contains 1,718 examples for which you must generate simplifications.
> File descriptions
> train.csv -- training data with original text and all three simplified target columns
> test.csv -- test data with original text only (no targets)
> sample_submission.csv -- a correctly formatted example submission with placeholder text
> Data fields
> id (integer) -- unique identifier for each example
> text (string) -- the source text passage to be simplified (typically graduate-level reading difficulty)
> level_1 (string) -- (train only) human-written simplification at the most simplified level (average ~16 words)
> level_2 (string) -- (train only) human-written simplification at the intermediate level (average ~19 words)
> level_3 (string) -- (train only) human-written simplification at the least simplified level (average ~24 words)
> Key characteristics
> Source passages are written at a high reading difficulty and average ~134 words
> Level 1 simplifications average ~16 words (roughly 88% reduction from original)
> Level 2 simplifications average ~19 words (roughly 86% reduction)
> Level 3 simplifications average ~24 words (roughly 82% reduction)
> Simplifications are not mere truncations -- they rephrase content using level-appropriate vocabulary and sentence structure
> The three target levels produce progressively more detailed output as the level increases

Inspiration note: Useful because it turns noisy context into an ordered or generated sequence, with an output shape that can be scored by exact, semantic, or alignment-aware metrics.

## Neural Dialect Next-Token Prediction
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f09arfsyyt93es4xa5yw89d849mzm
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: yenwee0804 ranked 1st (leaderboard #2, score —); rzotime ranked 3rd (leaderboard #13, score —); osman0 ranked #4 (leaderboard #43, score —)

Full challenge description from page:

> Overview
> Language models learn to predict the next token by capturing statistical patterns in sequential data. But what happens when the "language" isn't human language at all — but sequences generated by hidden neural networks with unknown weights?
> This challenge asks you to train a model that can approximate the behavior of unknown neural network "teachers" from their output sequences alone. Each teacher (called a "dialect") is an MLP with fixed random weights that takes 16 preceding tokens as context and samples the next token from its softmax output distribution. You never see the teacher weights — only the sequences they produced.
> Unlike standard next-token prediction benchmarks that operate on natural language, code, or well-known datasets, this challenge presents a fundamentally different problem: learning to approximate stochastic black-box neural network functions over abstract token sequences. There is no grammar to learn, no semantics to exploit, no pre-existing knowledge to leverage. The underlying "rules" are continuous neural network weight matrices — not discrete patterns that can be reverse-engineered or looked up.
> The core difficulty is few-shot adaptation to unseen functions. The training set contains 80 dialects. The test set introduces 20 completely new dialects with different underlying weight matrices. For each test dialect, you receive only 200 labeled examples as a burn-in signal, then must predict the next token for 1,000 subsequent positions. Your model must generalize across function families — not memorize specific dialects.
> The vocabulary consists of 512 abstract tokens (T0 through T511) with no semantic meaning. The 16-token context window combined with the 512-token vocabulary ensures that every context in the dataset is unique — there are zero repeated contexts across the entire dataset. This makes lookup tables, frequency counting, and memorization-based approaches completely ineffective. Pre-trained language models (GPT, LLaMA, etc.) provide zero advantage, as their linguistic knowledge is irrelevant to sequences from random MLPs.
> Evaluation
> Submissions are scored using Top-1 Accuracy — the fraction of test positions where your predicted token exactly matches the ground-truth token.
> Metric
> Top-1 Accuracy — for each test row, your predicted next_token is compared to the true next_token sampled by the hidden teacher model. A prediction is correct if and only if it is an exact string match.
> Scoring Formula
> Score
> =
> Number of correct predictions
> Total test rows
> Score=
> Total test rows
> Number of correct predictions
> Higher is better. The score is a float between 0.0 and 1.0.
> Baselines
> Method Expected Score Random guessing (1/512) ~0.2% Always predict most frequent token per dialect ~3% Well-trained small transformer 5–20%
> The gap between the frequency baseline (~3%) and a well-trained model (5–20%) provides substantial room for solver improvement. Models that learn the underlying MLP dynamics and adapt quickly to new dialects via the burn-in context will score highest.
> ## Grading Logic
> def grade(submission_path, answers_path): submission = pd.read_csv(submission_path) answers = pd.read_csv(answers_path)
> # Validate: matching IDs, no duplicates, correct row count if set(submission.id) != set(answers.id): return 0.0 if submission.id.duplicated().any(): return 0.0 merged = answers.merge(submission, on='id', suffixes=('_true', '_pred')) correct = (merged.next_token_true == merged.next_token_pred).sum() accuracy = correct / len(merged) return accuracy
> # Dataset
> All data is provided as UTF-8 encoded CSV files.
> ## Training data: `train.csv`
> **Columns:**
> - `id` (int): Row identifier
> - `dialect_id` (int): Identifies which teacher model generated this example (0–99)
> - `position` (int): Position of the target token within the dialect's sequence
> - `context` (string): The 16 preceding tokens, space-separated (e.g., `"T45 T12 T200 T78 T134 T56 T90 T23 T301 T455 T67 T189 T400 T234 T12 T89"`)
> - `next_token` (string): Ground-truth next token sampled from the teacher's distribution (e.g., `"T167"`)
> **Key properties:**
> - Each row is an independent prediction example: given a dialect and 16-token context, predict the next token.
> - Contains full data from 80 training dialects (0–79): ~7,984 rows per dialect.
> - Also contains 200 labeled burn-in rows from each of the 20 test dialects (80–99). These burn-in examples help your model recognize the test dialects' patterns before making predictions.
> - Token vocabulary: 512 tokens (`T0` through `T511`), all appearing in the dataset.
> - The teacher model uses a context window of 16 tokens. Positions start at 16 (the first 16 tokens of each dialect serve as the initial seed).
> - Sequences within each dialect are continuous — position `n` follows directly from position `n-1`.
> - Every context in the dataset is unique (100% unique contexts) — no two rows share the same 16-token context.
> ## Test data: `test.csv`
> **Columns:**
> - `id` (int): Row identifier, matching submission
> - `dialect_id` (int): Test dialect identifier (80–99)
> - `position` (int): Position within the dialect's sequence (216–1215)
> - `context` (string): The 16 preceding tokens, space-separated
> **Key properties:**
> - `next_token` is not included in the test file.
> - 20 test dialects × 1,000 rows each = 20,000 total test rows.
> - Positions are contiguous within each dialect, following directly after the burn-in data in `train.csv`.
> - You must predict the next token using only the dialect_id, context, and any patterns learned from training data (including burn-in examples).
> # Submission Format
> Your submission must be a CSV file named `submission.csv`.
> **Columns:**
> - `id` (int): Row identifier copied directly from `test.csv`
> - `next_token` (string): Your predicted next token (e.g., `"T167"`)
> **Requirements:**
> - Must include a header row: `id,next_token`
> - Exactly one row for every `id` in `test.csv` — no missing, duplicate, or extra IDs.
> - `next_token` must be a valid token from the vocabulary (`T0` through `T511`).
> - Any submission that violates these requirements will receive a score of 0.0.
> **Example:**
> id,next_token 0,T167 1,T42 2,T88 3,T201 4,T5
> &nbsp;

Inspiration note: Useful because it turns noisy context into an ordered or generated sequence, with an output shape that can be scored by exact, semantic, or alignment-aware metrics.

## Rosetta Stone: Ancient Egyptian Translation Challenge
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cbt0s70a29mvx7f57zwxmh5849cvf
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: kindasomethin ranked 1st (leaderboard #10, score —); yenwee0804 ranked 2nd (leaderboard #2, score —); arin ranked 3rd (leaderboard #21, score —)

Full challenge description from page:

> Overview
> Can you build a translation system for a language that has been dead for over 1,500 years?
> You are given 80,000 parallel sentence pairs mapping ancient Egyptian transliteration to German. The Egyptian text uses a specialized transliteration system with characters that no modern tokenizer handles. About 40% of test inputs have characters replaced with a damage marker (░) simulating degraded papyrus.
> Your model must perform two tasks: restore the damaged Egyptian text to its original form, and translate it into German. This mirrors real Egyptology work where scholars must first reconstruct missing text before interpreting it.
> Standard pretrained tokenizers and multilingual models were not trained on Egyptian transliteration, so solutions typically benefit from custom tokenization and domain adaptation. From-scratch training, fine-tuned multilingual encoder-decoders, and hybrid OCR-plus-restoration pipelines are all valid approaches — the challenge is designed around the difficulty of the language, not a specific training regime.
> Evaluation
> Submissions are scored using a composite of restoration quality and translation quality:
> Score = 0.40 x Restoration_chrF+++ 0.60 x Translation_chrF++
> Restoration chrF++ (40%): chrF++ between your restored Egyptian text and the original undamaged text, averaged over damaged test inputs only. Clean (undamaged) inputs are excluded from this component since restoration is trivial for them.
> Translation chrF++ (60%): chrF++ between your German translation and the reference German, averaged over all test inputs.
> chrF++ computes precision and recall over character n-grams (n=1 to 6) and word n-grams (n=1 to 2), with beta=2 weighting. Deterministic and tokenizer-agnostic.
> Score range: 0.0 to 1.0. Higher is better.
> Dataset
> public/train.csv: 80,000 parallel pairs for training (clean, undamaged)
> public/test.csv: 5,000 inputs to restore and translate (some with damage markers)
> public/sample_submission.csv: example output format
> private/answers.csv: original Egyptian + German references
> Column descriptions for train.csv:
> id (string): unique pair identifier
> egyptian (string): ancient Egyptian transliteration (source, clean)
> german (string): German translation (target)
> Column descriptions for test.csv:
> id (string): unique pair identifier
> egyptian (string): transliteration to restore and translate (may contain ░ damage markers)
> Submission
> Submit a CSV file with restored Egyptian text and German translations for every test input.
> Columns:
> id (string): identifier matching test.csv
> restored_egyptian (string): your restoration of the Egyptian text (replace ░ markers with predicted characters, or copy unchanged for clean inputs)
> german_translation (string): your German translation
> Example:
> id,restored_egyptian,german_translation
> RS_a1b2c3d4e5f6,"ḏd-mdw jn ꜣs,t wr,t","Worte sprechen durch Isis, die Große."
> RS_f1e2d3c4b5a6,"ḥtr tp,j ꜥꜣ n ḥm =f","Das erste große Pferdegespann seiner Majestät."
> Requirements:
> Must contain exactly 5,000 rows
> Must include a header row
> Both restored_egyptian and german_translation must be non-empty strings
> No duplicate IDs

Inspiration note: Useful because it turns noisy context into an ordered or generated sequence, with an output shape that can be scored by exact, semantic, or alignment-aware metrics.

## Biochemical Raman Spectral Language Modeling
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70zgz892byrrt4qfmy02a6ad88p4pv
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: singhking ranked 1st (leaderboard #33, score —); arin ranked 2nd (leaderboard #21, score —); poggerman ranked 3rd (leaderboard #20, score —); oguricapu ranked #4 (leaderboard #32, score —)

Full challenge description from page:

> Overview
> Raman instruments produce ordered intensity patterns that can be converted into a compact spectral language. In this benchmark, each sample is represented as a text sequence made from intensity-state tokens, local trend tokens, and peak or valley markers. Some positions in each sequence have been replaced by masktoken.
> Your task is to train a sequence model that infills the missing spectral-language tokens. Each test sequence has fifteen masked positions: every peak or valley marker is hidden, and the remaining masks cover local intensity and trend states. The private split uses held-out acquisition sessions, so models must learn reusable token context rather than memorizing one session's local patterns.
> This is a self-supervised pretraining task for spectral data. Real Raman pipelines often face dropped channels, noisy local bands, instrument drift, and limited labeled assays. Learning to reconstruct masked spectral-language tokens encourages a model to capture local peak context and session-stable motif structure before it is reused for downstream sample screening, quality control, or assay triage.
> Dataset
> File descriptions
> train.csv -- 1,231 masked spectral-language sequences with the true missing tokens.
> test.csv -- 2,039 masked spectral-language sequences with the same fields, but without the true missing tokens.
> train.jsonl -- Instruction/response mirror of train.csv for language-model training workflows.
> test.jsonl -- Instruction-only mirror of test.csv for language-model inference workflows.
> sample_submission.csv -- A template showing the required submission format with id and missing_tokens columns filled with random valid-looking tokens.
> Column descriptions
> id (string) -- Unique 12-character hashed identifier for each sequence.
> masked_sequence (string) -- Ordered whitespace-separated spectral-language tokens. The token masktoken marks each missing position to recover.
> mask_positions (string) -- Space-separated zero-based token positions of the masked entries in masked_sequence. The order of these positions is the required output order.
> missing_tokens (string) -- Target field in train.csv only. Space-separated original tokens for the positions listed in mask_positions.
> Evaluation
> Submissions are scored by session-balanced weighted token recovery. For each row, the grader compares the submitted missing_tokens string with the true missing tokens in private answers, in mask_positions order.
> Token weights are deterministic:
> Peak and valley marker tokens, such as peak1_band_08 or valley2_band_01, have weight 3.00.
> Trend tokens, such as trend_fall2 or trend_rise1, have weight 1.25.
> Extreme amplitude tokens amp_m3 and amp_p3 have weight 1.15.
> Other amplitude tokens have weight 1.00.
> The row score is the sum of correctly recovered token weights divided by the sum of all token weights for that row. The final score first averages row scores within each hidden acquisition-session group, then averages those session scores. These hidden groups are used only by the official grader to prevent one easier acquisition session from dominating the leaderboard. Higher scores are better.
> Public train.csv includes the true missing_tokens, so you can reproduce the token-weight part of the metric on local validation folds. The hidden session balancing is applied only to the private test split.
> def token_weight(token):
> if token.startswith(("peak", "valley")):
> return 3.00
> if token.startswith("trend_"):
> return 1.25
> if token in {"amp_m3", "amp_p3"}:
> return 1.15
> return 1.00
> def row_score(true_text, pred_text):
> true_tokens = true_text.split()
> pred_tokens = pred_text.split()
> if len(true_tokens) != len(pred_tokens):
> raise ValueError("Each row must predict the expected number of tokens")
> weights = [token_weight(token) for token in true_tokens]
> correct_weight = sum(
> weight for truth, pred, weight in zip(true_tokens, pred_tokens, weights)
> if truth == pred
> )
> return correct_weight / sum(weights)
> def official_score(submission, answers):
> submission_by_id = submission.set_index("id")
> session_scores = {}
> for row in [answers.to](http://answers.to)_dict("records"):
> pred_text = submission_by_id.loc[row["id"], "missing_tokens"]
> score = row_score(row["missing_tokens"], pred_text)
> session_scores.setdefault(row["session_group"], []).append(score)
> return sum(sum(scores) / len(scores) for scores in session_scores.values()) / len(session_scores)
> Submission
> Submit a CSV file with one prediction for every row in test.csv.
> id (string) -- The 12-character identifier from test.csv.
> missing_tokens (string) -- Space-separated predicted tokens, in the same order as mask_positions.
> Example:
> id,missing_tokens
> 264b6dfd8639,valley1_band_13 peak2_band_17 peak3_band_07 valley1_band_16 peak1_band_22 valley1_band_03 peak1_band_14 valley2_band_17 valley1_band_02 peak3_band_15 peak2_band_16 valley1_band_17 valley1_band_06 peak3_band_09 peak2_band_11
> 7a2208890a21,valley1_band_07 peak3_band_12 peak3_band_11 valley1_band_03 peak2_band_23 peak2_band_19 valley2_band_19 valley1_band_17 valley1_band_03 peak2_band_15 peak3_band_11 peak2_band_12 peak3_band_20 peak1_band_08 valley1_band_03
> 1faa080ad21c,peak3_band_17 peak2_band_15 peak3_band_08 peak1_band_15 amp_z0 amp_z0 peak2_band_23 trend_rise1 valley1_band_13 valley1_band_11 valley1_band_09 valley1_band_12 valley2_band_18 valley1_band_12 peak2_band_16
> Requirements
> The file must contain exactly 2,039 rows plus the header.
> Every id from test.csv must be present exactly once.
> Each missing_tokens value must contain exactly as many whitespace-separated tokens as there are positions in that row's mask_positions.
> Missing predictions, duplicate ids, extra columns, or rows with the wrong token count are rejected.
> File format: .csv only, with exact column names id,missing_tokens.
> Prohibited Approaches
> Do not hardcode lookup tables of test ids, full masked strings, or expected token outputs.
> Do not build the main solution as a regular-expression system, a handwritten imputation table, or a large collection of fixed token rules. Small diagnostic checks are fine, but the submitted method should train a model from public training rows.
> Do not treat masked_sequence as unordered categorical columns. It is an ordered text sequence; solutions should use sequence-aware features, token n-grams, learned embeddings, masked-language-model objectives, or other NLP-style representations.
> Do not fit text vectorizers, feature selectors, or calibration steps on combined train and test data. Any preprocessing statistics must be learned from the public training data only.

Inspiration note: Useful because it turns noisy context into an ordered or generated sequence, with an output shape that can be scored by exact, semantic, or alignment-aware metrics.

## Single Cell Hidden Probe Sequence Reconstruction
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dyqetgq5gmpe6406597akps88ew9g
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Home page recommendation/context: Beat urwashi's score of 0.311!

Full challenge description from page:

Single Cell Hidden Probe Sequence Reconstruction
Overview
This challenge is a sequence-to-sequence learning problem on single-cell expression data.
Each biological observation is represented as an anonymized source sequence. The source sequence encodes the observed part of a small expression panel, biological and acquisition context, assay and sample metadata, panel damage indicators, and quantized observed expression tokens.
For each training row, the target is a hidden probe-signature sequence. The target is an ordered token sequence describing which hidden probes are active and how strongly they are expressed.
For each test row, your task is to generate the hidden probe-signature sequence.
The private evaluation set contains several robustness stress cases:
Rows from a shifted acquisition or biological context domain.
Held-out sample groups that reduce near-duplicate leakage.
Rows where part of the observed panel has been deterministically zeroed.
Rare hidden signature patterns that are uncommon in training.
A strong solution should learn to translate the observed expression-context sequence into the hidden probe-signature sequence. Random row validation will likely overestimate private performance.
Files
The prepared public data contains:
train.csv — training examples with source and target sequences.
test.csv — test examples with source sequences only.
sample_submission.csv — required submission format.
sequence_vocabulary.csv — list of valid source and target tokens.
observed_panel.csv — anonymized metadata for observed expression tokens.
target_panel.csv — anonymized metadata for hidden target tokens.
README.md — short summary of the prepared files.
The private data contains:
answers.csv — private ground truth target sequences and hidden evaluation subset flags.
Task
For every row in test.csv, generate one predicted_sequence.
The model input is the source_sequence column.
The desired model output is the hidden target_sequence.
This is a sequence reconstruction problem. The output length varies by row. Some rows have no active hidden probes, while other rows have many active hidden probes.
Source Sequence Format
Each source_sequence is a whitespace-separated sequence of tokens.
Example:
DOM_004 ASSAY_001 CTX_018 GENCTX_003 COND_002 SEX_001 STAGE_000 SAMPLE_001 PANEL_NORMAL TOTAL_Q18 NZ_Q42 O000_Q00 O001_Q03 O002_Q00 O003_Q11 O004_Q01
Token groups include:
DOM_* — anonymized coarse acquisition or context domain.
ASSAY_* — anonymized assay or measurement technology.
CTX_* — anonymized fine-grained biological context.
GENCTX_* — anonymized higher-level biological context.
COND_* — anonymized condition or status category.
SEX_* — anonymized sex metadata where available.
STAGE_* — anonymized development or stage metadata where available.
SAMPLE_* — anonymized sample or suspension type category.
PANEL_NORMAL or PANEL_DAMAGE_* — observed panel condition.
TOTAL_Q* — quantized total observed panel signal.
NZ_Q* — quantized number of nonzero observed probes.
O000_Q* through O079_Q* — quantized observed expression probe tokens.
The order of tokens in the source sequence is fixed and meaningful.
Target Sequence Format
Each target sequence is a whitespace-separated sequence of hidden probe tokens.
Valid hidden probe tokens have this form:
T##_B#
where:
T00 through T15 identify the hidden target probe.
B1, B2, and B3 indicate low, medium, and high positive hidden signal.
Hidden probes with no or near-zero signal are omitted from the sequence.
The canonical target sequence is ordered by descending hidden signal bin, then by target index.
Example:
T06_B3 T13_B3 T03_B2 T09_B2 T01_B1 T07_B1 T10_B1 T14_B1
If no hidden probe is active, the target sequence is:
NONE
Important details:
B0 is never written in the target sequence.
Zero or near-zero hidden probes are represented by omission.
The token order matters.
Duplicate target tokens are not valid and will hurt the score.
Unknown or malformed tokens are treated as sequence errors.
Columns In train.csv
train.csv contains:
id — stable row identifier.
source_sequence — input sequence for the model.
target_sequence — ground-truth output sequence for the model.
Columns In test.csv
test.csv contains:
id — stable row identifier.
source_sequence — input sequence for the model.
It does not contain target_sequence.
Sequence Vocabulary File
sequence_vocabulary.csv contains valid tokens used by the prepared dataset.
Columns:
token — token string.
token_type — one of metadata, observed_expression, summary, target_probe, or special.
description — short anonymized description.
train_count — number of occurrences in training source or target sequences where applicable.
Observed Panel File
observed_panel.csv contains metadata for observed expression tokens.
Columns:
observed_index — observed probe position.
source_token_prefix — matching source token prefix such as O000.
feature_code — anonymized observed feature identifier.
damage_group — deterministic missing-probe group affecting this observed feature, or none.
Target Panel File
target_panel.csv contains metadata for hidden target tokens.
Columns:
target_index — hidden target probe position.
target_token_prefix — target token prefix such as T00.
target_code — anonymized hidden target identifier.
train_active_count — number of training rows where this target appears in the target sequence.
train_b1_count — number of training rows where this target appears as B1.
train_b2_count — number of training rows where this target appears as B2.
train_b3_count — number of training rows where this target appears as B3.
Submission Format
Submit a CSV file with exactly one row for every id in test.csv.
The required columns are:
id
predicted_sequence
Example:
id,predicted_sequence
cell_0a12f4b8e91d,T06_B3 T13_B3 T03_B2 T09_B2 T01_B1 T07_B1
cell_3be7d0c91a44,NONE
cell_f829a6610c02,T05_B3 T14_B3 T02_B2 T03_B1 T11_B1
The predicted_sequence column must contain a whitespace-separated sequence of valid target tokens, or NONE.
Missing IDs, duplicate IDs, extra IDs, missing predictions, or extra submission columns are invalid submissions.
Evaluation
Submissions are scored using a weighted sequence reconstruction score. Higher is better. The minimum possible score is 0 and the maximum possible score is 1.
The final leaderboard score is:
score =
0.45 * sequence_score_all_private_rows
+ 0.25 * sequence_score_shifted_domain_rows
+ 0.20 * sequence_score_damaged_panel_rows
+ 0.10 * sequence_score_rare_signature_rows
For each evaluated row, three sequence-level similarities are computed:
row_score =
0.50 * normalized_edit_similarity
+ 0.30 * exact_token_f1
+ 0.20 * order_lcs_similarity
The components are:
normalized_edit_similarity rewards generating the correct sequence with few insertions, deletions, or substitutions.
exact_token_f1 rewards recovering the correct hidden probe and bin tokens.
order_lcs_similarity rewards placing the recovered target tokens in the correct order.
The subset scores are the mean row score over the corresponding private rows.
Malformed target tokens are treated as wrong sequence tokens. Duplicate target IDs, unknown target IDs, invalid bin values, and non-canonical tokens reduce the score.
Modeling Notes
Good approaches may include:
Treating source_sequence and target_sequence as text-like token sequences.
Encoder-decoder transformers or other sequence models.
Retrieval-augmented nearest-neighbor sequence generation.
Sequence-aware validation split by held-out domain, sample group, or panel condition.
Data augmentation by masking observed probe tokens.
Hybrid approaches that infer latent hidden probe activity and decode into a canonical sequence.
Do not rely only on a random row split. Related rows from the same context, sample group, or acquisition domain can be very similar, and random validation can overestimate private performance.
Restrictions
Use only the prepared public files provided in this challenge.
Do not use external datasets, internet lookup, source reconstruction, row-ID memorization, private labels, hidden answer files, or leaderboard probing.

Inspiration note: Useful because it asks solvers to map structured scientific inputs into an ordered/generated output sequence with task-specific validation.

## Tandem Mass Spectrometry Fragmentation Edit Sequence Prediction
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx789mk6qcw72r8gq1kzxcvccx89g0b3
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Home page recommendation/context: Beat fate1997's score of 0.645!

Full challenge description from page:

Tandem Mass Spectrometry Fragmentation Edit Sequence Prediction
Overview
This is a chemistry sequence-to-sequence challenge derived from anonymized and transformed experimental tandem mass spectrometry measurements.
Collision energy does not merely scale an MS/MS spectrum. Increasing energy can extinguish existing fragments, preserve stable fragments, reactivate pathways seen at lower energy, or create previously unseen fragments. Different instrument responses additionally warp the mass axis and alter intensity as a function of mass-to-charge ratio.
Each sample provides two 256-position spectral sequences from the same molecule: a low-energy observation and a later-energy context observation. The two sequences were measured through different instrument-response transforms. Sparse calibration-anchor sequences describe those transforms and a third target transform.
The required output is a 256-token fragmentation edit program describing how the molecular fragmentation state changes at the higher target collision energy in the target instrument frame. This is not direct spectrum copying or ordinary peak-probability output. Every token jointly represents the previous state, the target state, and the causal transition between them.
The five output tokens are:
0 - stable absence: no significant context peak and no significant target peak.
1 - extinction: a context peak disappears at the target energy.
2 - persistence: a context peak remains present at the target energy.
3 - recurrence: a low-energy peak absent from the context state returns at the target energy.
4 - novel emergence: a target peak appears without a corresponding low-energy or context peak.
Solvers must align both observed sequences into the target response frame, infer collision-dependent fragmentation transitions, and emit the ordered edit-token sequence. Training and test molecular groups are disjoint, and all records are anonymized before task construction.
Evaluation
Submissions are evaluated using Structured Fragmentation Edit Score, bounded to [1e-9, 1]. Higher is better.
The score combines:
55% global macro token F1: F1 is calculated independently for each of the five operation tokens and then averaged. This prevents the frequent stable-absence token from dominating the score.
45% ordered event F1: Nonzero edit events are matched within each sample. A predicted event matches when it has the correct operation token and falls within one mass bin of an unmatched target event. This allows a small calibration discretization tolerance while preserving operation identity and sequence order.
score = 0.55 * macro_token_f1 + 0.45 * mean_ordered_event_f1
The grading direction is Maximize. The minimum configured score is 1e-9, an effective zero, and the maximum is 1.
Dataset
Observed spectra contain 256 float32 intensity bins. Bin i represents normalized fragment mass fraction [i/256, (i+1)/256) relative to precursor mass. Observed intensities are square-root transformed and normalized so the strongest bin equals one.
Training targets are uint8 arrays containing the edit tokens 0 through 4.
Public files
train.csv - Metadata for 9,000 training sequences.
train_low.npy - Low-energy observations, shape (9000, 256).
train_context.npy - Context-energy observations, shape (9000, 256).
train_calibration.npy - Calibration anchors, shape (9000, 3, 12, 2).
train_targets.npy - Fragmentation edit-token sequences, shape (9000, 256).
test.csv - Metadata for 2,400 test sequences.
test_low.npy - Low-energy test observations, shape (2400, 256).
test_context.npy - Context-energy test observations, shape (2400, 256).
test_calibration.npy - Test calibration anchors, shape (2400, 3, 12, 2).
sample_submission.csv - Required output structure.
Metadata columns
id (integer) - Prepared sequence identifier.
low_energy (float) - Collision energy of the low observation.
context_energy (float) - Collision energy of the context observation.
target_energy (float) - Collision energy represented by the output edit sequence.
energy_step_ratio (float) - (target_energy - context_energy) / (context_energy - low_energy).
precursor_mz (float) - Precursor mass-to-charge ratio.
parent_mass (float) - Neutral parent molecular mass.
instrument_code (integer) - 0 for Orbitrap and 1 for QTOF.
adduct_code (integer) - 0 for [M+H]+ and 1 for [M+Na]+.
Calibration anchors
Calibration axis 1 contains three responses:
Index 0 - low-observation response.
Index 1 - context-observation response.
Index 2 - target response.
Each response contains 12 anchors. Canonical positions are 12 evenly spaced values from 0.03 through 0.97. At each anchor, channel 0 is its observed normalized mass position and channel 1 is its relative intensity gain. Interpolation between anchors estimates the continuous mass-axis mapping and response curve.
Submission
Submit a CSV containing exactly 2,400 rows with columns in this order:
id,t000,t001,...,t255
id must match each ID from test.csv exactly once.
t000 through t255 must be integer tokens from 0 through 4.
Include the header row and do not include an index column.
Missing values, fractional tokens, unknown tokens, missing IDs, or duplicate IDs are rejected.
Important Restrictions
Use only the provided challenge files; external spectral datasets and record linkage are prohibited.
Do not derive outputs from row IDs, file order, hidden files, or preparation randomness.
General-purpose pretrained models and chemistry libraries are allowed when they do not introduce external spectrum or molecule lookup data.

Inspiration note: Useful because it asks solvers to map structured scientific inputs into an ordered/generated output sequence with task-specific validation.
---

<!-- GOOGLE_DRIVE_APPEND_2026_07_01 -->
**Google Drive Folder Append (2026-07-01T08:30:33+05:30)**

These entries came from the two shared Google Drive folders. They may duplicate earlier examples because this append intentionally preserves all shared accepted/approved challenge specs. Drive entries use folder/domain labels when present and inference from the folder/spec text when no explicit DOMAIN field is available.

## Marketplace Listing Attribute Canonicalization
- Challenge URL: https://drive.google.com/drive/folders/1YsNaJguYVAGL5iRR8L5PMDdx_-fsxWVp
- Source file: cd.txt
- DOMAIN used for this document: Sequence To Sequence (from Drive domain folder or folder name)
- Status: From Google Drive accepted-challenge collection
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: See description if specified
- Tags: Not shown/captured
- Best/top context found: Google Drive: Drive folder 1 / Sequence To Sequence / Marketplace Listing Attribute Canonicalization

Full challenge description from Drive:

> Overview
> Marketplace catalogs depend on clean, normalized product records for search ranking, deduplication, moderation, and downstream quality systems. In practice, sellers submit noisy drafts with inconsistent casing, shorthand attributes, locale-specific size formats, keyword stuffing, and partially missing structured hints. In this challenge, your task is to generate the canonical marketplace attribute string for each draft listing.
> Each row is one seller-created listing draft. The dataset provides the raw seller text (raw_title, raw_bullets, raw_description), marketplace context, and noisy extracted hints. Your output must be a single normalized string in an exact key order, containing 8 canonical attributes: brand, product type, variant, color, size, pack count, material, and condition.
> This is a sequence-to-sequence normalization benchmark. Strong solutions should read the raw listing text directly, normalize abbreviations and locale-specific forms, use metadata carefully, and enforce the exact target format. Weak solutions usually trust the hint columns too much or produce free-form text that does not match the required canonical schema.
> Evaluation
> Submissions are scored using Rarity-Weighted Structured Attribute Accuracy.
> For each listing:
> Parse the predicted canonical_listing_spec into 8 required key-value fields.
> Parse the ground-truth canonical_listing_spec into the same 8 fields.
> Compute a weighted partial score and an exact-row indicator, then blend:
> row_score = 0.70 × weighted_partial + 0.30 × exact_row_match
> Where:
> weighted_partial = Σ FIELD_WEIGHTS[k] × (pred_k == truth_k) across all 8 fields; weights sum to 1.0
> exact_row_match = 1.0 if all 8 fields are correct, else 0.0
> The final challenge score is the mean row score across all test listings.
> Field Weights
> Field weights are derived from the training label distribution. For each field, the weight is proportional to the minority fraction (1 − P_majority) — fields whose dominant value is very common (e.g. condition=new at 89.5% of train) receive near-zero weight, while fields with diverse value distributions (e.g. brand, variant) receive the highest weight. This means correctly predicting a rare brand or unusual variant contributes far more to the score than always predicting condition=new.
> Field	Majority class	P_majority	Weight
> brand	luma	0.064	0.1651
> product_type	tote bag	0.105	0.1580
> variant	mini	0.071	0.1639
> color	clear	0.114	0.1564
> size	na	0.305	0.1227
> pack_count	1	0.617	0.0676
> material	plastic	0.163	0.1477
> condition	new	0.895	0.0186
> A model that always predicts the majority class for every field scores 0.176, compared to 0.292 under equal field weights.
> The exact-row-match component (30% of the score) rewards models that get every attribute right simultaneously, not just approximately correct on the easy fields.
> Higher is better. A perfect score of 1.0 means every field matches exactly on every test listing.
> Dataset
> The prepared dataset contains a strict chronological split of marketplace listing drafts:
> public/train.csv — 23,813 labeled listings from 2024-01-02 08:00:00 through 2024-05-24 19:59:00
> public/test.csv — 6,187 unlabeled listings from 2024-05-25 08:00:00 through 2024-06-30 19:59:00
> public/sample_submission.csv — example submission showing the required output schema
> private/answers.csv — hidden ground-truth canonical strings for scoring
> Important dataset characteristics:
> each row is one listing draft; there is no candidate expansion or grouping
> train.csv contains 16 feature columns plus the target column canonical_listing_spec
> test.csv contains the same 16 feature columns without the target
> the main modeling signal is in raw_title, raw_bullets, and raw_description
> the hint fields brand_hint, color_hint, size_hint, pack_count_hint, and material_hint are frequently missing and are actively wrong in roughly 22-32% of non-empty cases; they cannot be trusted without corroboration from the raw text
> taxonomy_hint is often broadened or replaced with an entirely different product category; it is a weak signal at best
> approximately 18% of rows per field have all mentions suppressed from text and the matching hint set to blank; the model must fall back to priors or cross-field reasoning for those rows
> variant descriptions use a paraphrase vocabulary that partially shifts in the test period; some test-period phrasings do not appear in any training row
> the target always follows the same fixed key order:
> brand=<...>; product_type=<...>; variant=<...>; color=<...>; size=<...>; pack_count=<...>; material=<...>; condition=<...>
> The prepared files contain these columns:
> Identifiers and Marketplace Context
> Column	Type	Description
> listing_id	string	Unique listing identifier used in submissions
> created_at	datetime	Listing creation timestamp
> seller_id	string	Seller identifier
> seller_tier	categorical	Seller maturity tier: new, growth, established, or premium
> marketplace_region	categorical	Marketplace operating region
> locale	categorical	Seller locale
> taxonomy_hint	string	Noisy or coarse taxonomy path hint
> price_local	float	Seller-entered local price
> Raw Listing Text
> Column	Type	Description
> raw_title	string	Seller-created title draft with noise and shorthand
> raw_bullets	string	Pipe-separated bullet-style seller notes
> raw_description	string	Longer free-form draft description
> Noisy Extracted Hints
> Column	Type	Description
> brand_hint	string	Noisy extracted brand hint, sometimes stale or missing
> color_hint	string	Noisy extracted color hint, sometimes missing
> size_hint	string	Noisy extracted size or compatibility hint, sometimes missing
> pack_count_hint	string	Noisy extracted pack-count hint, sometimes missing
> material_hint	string	Noisy extracted material hint, sometimes missing
> Target
> Column	Type	Description
> canonical_listing_spec	string	Canonical normalized attribute string in fixed key order
> Submission
> Submit a submission.csv file with the following format:
> Column	Type	Description
> listing_id	string	Listing identifier copied from test.csv
> canonical_listing_spec	string	Predicted canonical attribute string in the exact required schema
> Example:
> listing_id,canonical_listing_spec
> lst_023859,"brand=aurora; product_type=wireless earbuds; variant=pro; color=white; size=na; pack_count=1; material=plastic; condition=new"
> lst_023860,"brand=novara; product_type=phone case; variant=magnetic; color=black; size=iphone 15; pack_count=2; material=silicone; condition=new"
> What Not To Use

Inspiration note: Useful as a transformation task pattern where inputs must be converted into a structured target sequence under domain-specific rules.

## Financial Audit Report Multi-Tier Summarization
- Challenge URL: https://drive.google.com/drive/folders/1WHaexnE2-KuW3v1hrtNho0NoCbXsW0ls
- Source file: cd.txt
- DOMAIN used for this document: Sequence To Sequence (from Drive domain folder or folder name)
- Status: From Google Drive accepted-challenge collection
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: See description if specified
- Tags: Not shown/captured
- Best/top context found: Google Drive: Drive folder 1 / Sequence To Sequence / Financial Audit Report Multi-Tier Summarization

Full challenge description from Drive:

> Financial Audit Report Multi-Tier Summarization
> Overview
> In the rapidly evolving landscape of global financial surveillance, regulatory bodies are confronted with an unprecedented volume of "Audit Telemetry Dockets". These dockets are complex amalgamations of high-frequency trade sequences, encrypted internal communications, and fragmented procedural filings. The Global Surveillance Archive (GSA)—a fictionalized international body established to monitor systemic market risks—collects this data across multiple nexus nodes.
> To maintain systemic stability, the GSA requires an automated Forensic Synthesis Engine capable of generating a Tri-Tier Final Directive from these massive dockets. This engine must distill raw telemetry into three distinct strategic layers:
> Forensic Chronology: A granular, step-by-step reconstruction of identified anomalies and trade sequences (for deep forensic analysis).
> Strategic Impact Summary: A concise, thematic assessment of market-wide risks and institutional exposure (for senior decision-makers).
> Operational Directive: A high-priority, single-sentence notification of the core deviation or "Status Green" (for real-time enforcement).
> The challenge is to handle documents exceeding 50,000 characters while maintaining logical consistency across all three tiers of the final report.
> Evaluation
> Submissions are scored using the Composite Integrity Index (CII). This metric evaluates semantic accuracy and internal logical alignment.
> CII Formula
> CII = 0.4 * ROUGE_L(Chronology) + 0.2 * ROUGE_L(Impact) + 0.2 * ROUGE_L(Directive) + 0.2 * Consistency(Impact, Directive)
> Metric Details
> ROUGE-L: Standard LCS-based F1 score for each tier.
> Consistency Score: Measures the Semantic Entailment between the Strategic Impact Summary and the Operational Directive.
> Formula: Consistency = |Meaningful_Tokens(Directive) ∩ Tokens(Impact)| / |Meaningful_Tokens(Directive)|
> Meaningful tokens are defined as alphanumeric words with length > 3 characters.
> Dataset
> File Structure
> train.csv — Historical audits with curated final directives.
> test.csv — Unlabeled telemetry dockets for prediction.
> sample_submission.csv — Template showing the required FAR format.
> Features
> train.csv
> Column	Type	Description
> id	string	Unique docket identifier (e.g., FAR-A1B2C3D4).
> audit_telemetry	string	The full text of the source report with obfuscated terminology and injected system headers.
> final_directive	string	[TARGET] The report containing the three specific forensic markers.
> test.csv
> Column	Type	Description
> id	string	Unique docket identifier.
> audit_telemetry	string	The source text to be synthesized.
> Submission Format
> Submit a CSV file with exactly two columns: id and final_directive.
> Column	Type	Description
> id	string	Row identifier from test.csv.
> final_directive	string	The synthesized report with required markers.
> Marker Requirements:
> [FORENSIC_CHRONOLOGY]
> [STRATEGIC_IMPACT_SUMMARY]
> [OPERATIONAL_DIRECTIVE]
> Reports must contain all three markers in the specified order. Failure to include a marker will result in a 0.0 score for that section.
> Example Submission Row
> FAR-A1B2C3D4,"[FORENSIC_CHRONOLOGY] Forensic analysis identified a series of layering orders originating from Node-X... [STRATEGIC_IMPACT_SUMMARY] The Trading Firm engaged in market manipulation through spoofing. [OPERATIONAL_DIRECTIVE] Immediate corrective action and enhanced monitoring are recommended."
> Intended Solution Approach (What To Use)
> Extractive-then-Abstractive Pipelines: Use a two-stage approach — first extract key sections from the long document using positional or section-based heuristics, then abstractively summarize each tier.
> Long-Context Language Models: Fine-tune long-context architectures (e.g., Longformer, LED, or LLaMA-based models) to handle the full document length directly.
> Section-Aware Encoding: Leverage the natural document structure (section headers, paragraph boundaries) to guide tier-specific extraction.
> Multi-Task Training: Train a single model with separate decoder heads or prompts for each of the three summary tiers.
> Prohibited Approaches (What Not To Use)
> To maintain the integrity of the benchmark, the following approaches are strictly forbidden:
> No External LLM APIs: You may not use external API calls to models such as GPT-4, Claude, Gemini, or any commercial LLM endpoints. All inference must be performed locally within the compute budget.
> No Source Document Lookup: Do not attempt to reverse-engineer the obfuscation to recover original source documents from public archives. The audit telemetry has been intentionally transformed.
> No Hardcoded Answers: Do not submit static, pre-written responses or rule-based dictionary lookups that simply replay memorized training set targets.
> No Test Set Exploitation: Unsupervised clustering or alignment exclusively on test.csv without generalizing from training data is prohibited.
> What Not To Use
> No External LLM APIs: You may not use external API calls to models such as GPT-4, Claude, Gemini, or any commercial LLM endpoints. All inference must be performed locally within the compute budget.
> No Source Document Lookup: Do not attempt to reverse-engineer the obfuscation to recover original source documents from public archives. The audit telemetry has been intentionally transformed.
> No Hardcoded Answers: Do not submit static, pre-written responses or rule-based dictionary lookups that simply replay memorized training set targets.
> No Test Set Exploitation: Unsupervised clustering or alignment exclusively on test.csv without generalizing from training data is prohibited.

Inspiration note: Useful as a transformation task pattern where inputs must be converted into a structured target sequence under domain-specific rules.

## UAV Mesh Grammar Decompilation accepted
- Challenge URL: https://drive.google.com/drive/folders/1h5V6gjehyq-yLnkdw3By0yu8NKKAMlev
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: Sequence To Sequence (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: Accepted (from Drive folder name)
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: Not shown/captured
- Tags: Not shown/captured
- Best/top context found: UAV Mesh Grammar Decompilation_accepted from shared Google Drive folder

Full challenge description from Drive:

> # Challenge creation form — fill-in (3D Mesh to Grammar String Reconstruction)
> Copy each section below into the corresponding field on the challenge creation page. The challenge must use the accepted paired dataset you already created.
> ---
> ## 1) Difficulty (Required)
> **Select:** **Hard**
> *(3D geometry to compositional grammar is a structured-prediction task with a non-standard output vocabulary, aggressive geometric perturbation on every mesh, and ~40% noise on training labels. A strong agent that fine-tunes a 3D backbone plus a grammar-constrained decoder is expected to plateau well below the theoretical ceiling.)*
> ---
> ## 2) Challenge Title (Required)
> **Paste this in the Title field:**
> ```
> 3D Mesh to Grammar String Reconstruction
> ```
> ---
> ## 3) Problem Description (Required)
> *The challenge prompt solvers will see. Must be complete and unambiguous. Use the editor's headings (H1, H2), lists, and code blocks as below.*
> **Paste this in the Problem Description field:**
> ```markdown
> # 3D Mesh to Grammar String Reconstruction
> ## Overview
> You are given the 3D triangular mesh of a small unmanned aerial vehicle (UAV). Your task is to recover the **grammar string** that describes how the vehicle was assembled from primitive components.
> Every UAV in this benchmark was constructed by a compositional grammar whose alphabet encodes (a) the identity and size of each component and (b) how components are connected. Your model must invert the 3D geometry back into that symbolic description.
> The input for each test row is one perturbed triangular mesh (stored as a NumPy `.npz` archive) plus two noisy numeric hints (rounded and jittered weight and thrust). The output is a single grammar string per mesh.
> This is a 3D-to-sequence reconstruction task with a structured graph-level metric. Simple encoder-decoder models that emit grammar tokens directly from vertex point clouds are a reasonable baseline, but the target is not a plain sequence — it is a small labelled graph, with typed nodes, unordered edges, and a small operator vocabulary between consecutive nodes. Combined with the ~40% label noise on the training set, the aggressive full-3D geometric perturbation applied to every mesh, and the obfuscated grammar alphabet (see below), naive encoder-decoder setups plateau quickly.
> ## Grammar Specification
> Each grammar string is a concatenation of two blocks:
> 1. A non-empty sequence of **component blocks**, each of the form `*<letter><TYPE_CODE>` optionally followed by an **operator token**: `-`, `+`, `++`, `+++`, etc. (any non-empty run of `-` and/or `+` characters).
> 2. Zero or more **connection tokens**, each of the form `^<letter1><letter2>`.
> Token-level regex (predictions must match this):
> ```
> ^(\*[a-z][A-Z]{2}\d(?:[-+]+)?)+(\^[a-z][a-z])*$
> ```
> **Component block: `*<letter><TYPE_CODE>`**
> - `<letter>` is a single lowercase ASCII letter `a`–`z`. This is a local, per-UAV identifier for the component. The first component in the string is usually named `a`, the second `b`, etc., but the grader does **not** depend on this exact labelling — only on which letters appear in which connection tokens. Letters are never compared to the ground-truth letters directly; they are resolved to the component's `TYPE_CODE` before comparison.
> - `<TYPE_CODE>` is exactly three characters: two uppercase letters followed by a single digit. The first letter encodes the **component family** (hub, arm, motor, strut, etc.), the second letter encodes the **component sub-type / orientation**, and the digit `0`–`9` encodes the **size bucket** (smaller digits = smaller components, larger digits = larger components). The exact letter-pair alphabet used in this challenge has been **deterministically remapped** at prepare-time, so it does not match any letter palette you may have seen in public UAV-design datasets. You must learn the vocabulary from the provided `train.csv` alone.
> **Operator between consecutive components**
> The operator token, if present, is one of `-`, `+`, `++`, `+++`, etc. (any non-empty run of `-` and/or `+` characters, matched by the regex fragment `[-+]+`). It encodes the **relative orientation** of the next component with respect to the previous one (roughly: "in-plane", "above", "stacked above", and repeated/combined application thereof). A component block without a trailing operator means the next component attaches at the default orientation. Each complete run of `-`/`+` is treated as a single operator token by the grader. Operators contribute 10% of the final score, so getting the broad mix of operator tokens right matters while exact per-position alignment does not.
> **Connection token: `^<letter1><letter2>`**
> Each `^xy` token declares an **unordered undirected edge** between the component labelled `x` and the component labelled `y`. Connections appear at the end of the string, after all component blocks. The order in which connection tokens are listed is irrelevant.
> **Example (illustrative only; the actual alphabet in `train.csv` is different):**
> ```
> *aAA0-*bRA3++*cAR1++*dGA3*eAG1^ab^ac^ad^ae
> ```
> Parsed:
> - 5 components: `(a, AA0)`, `(b, RA3)`, `(c, AR1)`, `(d, GA3)`, `(e, AG1)`.
> - 3 operators: `-`, `++`, `++`.
> - 4 connections: `{a,b}`, `{a,c}`, `{a,d}`, `{a,e}` — component `a` is connected to every other component (a typical "hub plus four arms" topology).
> ## Evaluation
> Submissions are scored with a composite, structured metric that compares the **graph-level content** of the predicted grammar string to the ground truth. The grader parses both the predicted and the ground-truth `grammar_string` into four objects:
> - **Node multiset.** The multiset of `TYPE_CODE` values across all parsed components. Per-UAV letter labels are NOT compared.
> - **Typed edge multiset.** For every connection `^xy`, the grader looks up the `TYPE_CODE` of components `x` and `y` in the **predicted** grammar and records the sorted pair `(TYPE_CODE_x, TYPE_CODE_y)`. These typed pairs are compared as a multiset. This makes the metric invariant to arbitrary letter relabellings inside the predicted string.
> - **Operator multiset.** The multiset of non-empty operator tokens (each a non-empty run of `-` and/or `+` characters, e.g. `-`, `+`, `++`, `+++`) between consecutive components.
> - **Grammar validity.** `1.0` if the predicted string matches the grammar regex above AND contains at least one component; otherwise `0.0`.
> Each of the three multisets is compared with **multiset Jaccard** (intersection size over union size; `1.0` if both are empty).
> **Per-row score:**
> ```
> Row = 0.40 * NodeJaccard
> + 0.40 * EdgeTypedJaccard
> + 0.10 * OperatorJaccard
> + 0.10 * GrammarValidity
> ```
> **Final score** is the arithmetic mean of Row scores across all test rows, clipped to `[0, 1]`. Grading direction is **Maximize**. Minimum `0.0`, Maximum `1.0`.
> **Submissions that score exactly `0.0` automatically (to match `grade.py`):**
> - the submission is missing the `image_id` column or the `grammar_string` column (extra columns are ignored);
> - `image_id` contains any duplicate value;
> - the submission has a different row count than the hidden answers file;
> - the set of `image_id` values does not exactly match the set of `image_id` values in the answers file (equivalently, any test `image_id` is missing or any unknown `image_id` is present);
> - any `grammar_string` value is `NaN` / missing (non-string scalar values that are not NaN, e.g. numeric `0`, are tolerated: the grader coerces them with `astype(str)` before scoring, but they will parse as an invalid grammar and contribute `0` on every sub-score);
> - any uncaught exception is raised during grading.
> Note that `grade.py` uses `issubset` for column checks, so including additional helper columns beyond `image_id` and `grammar_string` does not trigger a zero; they are simply ignored.
> ## Dataset
> After the prepare script runs, solvers see the following files in `public/`:
> - `train/<image_id>.npz` — for each training `image_id`, a NumPy archive with keys `vertices` (float32 array, shape `(N, 3)`, vertex positions) and `faces` (int32 array, shape `(M, 3)`, triangle indices into `vertices`).
> - `test/<image_id>.npz` — same format, for test rows. No ground-truth label is provided.
> - `train.csv` — four columns: `image_id`, `grammar_string`, `noisy_weight_lb`, `noisy_thrust_lb`. Approximately 1,120 rows.
> - `test.csv` — three columns: `image_id`, `noisy_weight_lb`, `noisy_thrust_lb`. Approximately 280 rows.
> - `sample_submission.csv` — two columns: `image_id`, `grammar_string`. All predicted strings are a trivial placeholder. The file is a valid submission (correct columns, correct row count) but scores very low.
> In `private/` (not visible to solvers): `answers.csv` — `image_id`, `grammar_string`. Ground truth for the test set.
> **Training data properties solvers should know:**
> - `image_id` is a seeded permutation of `0..N-1` and is unrelated to any upstream mesh index.
> - Every mesh has been irreversibly perturbed at prepare-time: a full 3D rotation about a random axis by an angle in roughly `[-90°, +90°]` (so meshes are NOT presented in any canonical axis-aligned frame), a uniform scale in `[0.75, 1.25]`, additive Gaussian vertex jitter with `sigma = 0.020 * bbox_diag`, and random 15–30% vertex dropout (with face indices rewritten and dangling faces removed). Byte-level and vertex-hash matching against any external mesh corpus will not recover training labels, and pose-normalisation heuristics that assume an upright/forward canonical frame will not work.
> - The **grammar alphabet has been deterministically remapped** at prepare-time. The uppercase letters and digits that make up each `TYPE_CODE` are a seeded bijection over the full A–Z and 0–9 sets, so the token palette you see in `train.csv` is disjoint from any token palette used by any upstream public vehicle-design dataset. You must learn the vocabulary from `train.csv` alone.
> - `noisy_weight_lb` is rounded to the nearest 5 lb and jittered by ±25% Gaussian. `noisy_thrust_lb` is rounded to the nearest 25 lb and jittered by ±25%. Test-set noise uses the same distribution. These hints are deliberately weak — they convey rough order-of-magnitude information about the vehicle only, and a retrieval/nearest-neighbour solution over these two scalars alone will not generalise.
> - Approximately 40% of train-set `grammar_string` labels carry between 1 and 3 stacked local corruptions (independently drawn from: flipped size digit, flipped type-code letter, dropped edge, added spurious edge, swapped edge endpoint). Test labels and `private/answers.csv` are clean. This noise simulates realistic annotator disagreement and caps the achievable score of pure memorisation or naive-retrieval approaches well below the theoretical ceiling.
> - Different meshes may share the same `grammar_string`. Many UAV topologies (for example, "hub plus four identical arms") recur across the population. Two distinct training rows can have identical `grammar_string` values but different 3D meshes, different weights, and different thrust values. `image_id` is unique, and no `image_id` appears in both train and test.
> ## Submission
> Submit a single CSV file that **must contain at least** the following two columns (extra columns are permitted and will be ignored by the grader):
> | Column           | Type   | Description                                                             |
> |------------------|--------|-------------------------------------------------------------------------|
> | `image_id`       | int    | Row identifier from `test.csv` (one row per `image_id`; no duplicates). |
> | `grammar_string` | string | Predicted grammar string for that mesh. Should satisfy the regex above. |
> **Requirements (enforced by `grade.py`):**
> - Header row present. The two required column names must appear exactly as `image_id` and `grammar_string` (case-sensitive). Additional columns beyond these two do not cause rejection (the grader uses `issubset` for the column check) but are not used.
> - The set of `image_id` values must be exactly equal to the set of `image_id` values in `test.csv` (approximately 280 rows). Any missing or unknown `image_id` forces the final score to `0.0`.
> - Row count must equal the number of rows in the hidden answers file. Duplicate `image_id` values force the final score to `0.0`.
> - `grammar_string` values must be non-NaN. Non-string scalar values that are not NaN are tolerated (the grader coerces them via `astype(str)`), but anything that does not parse into `nodes`, `edges`, and operator tokens under the grammar regex will score `0` on every sub-score for that row. Empty strings and malformed strings are accepted (no rejection) but score `0` on Validity and typically `0` on the Jaccard terms too.
> **Example submission rows (illustrative — the actual alphabet in `train.csv` will differ because of the prepare-time remap):**
> ```csv
> image_id,grammar_string
> 0,*aAA0-*bRA3++*cAR1++*dGA3*eAG1^ab^ac^ad^ae
> 1,*aAA1*bRA0^ab
> 2,*aAA0-*bAA0-*cAA0-*dAA0^ab^ac^ad
> ```
> ```
> *(If the editor uses rich text instead of markdown, use H1 for the main title, H2 for each top-level section, and bullet lists and the tables as shown.)*
> ---
> ## 4) Tags
> **Select one or more:** **3d**, **structured-prediction**, **sequence-to-sequence**
> ---
> ## 5) Grading Configuration (Required)
> **Grade direction:** **Maximize**
> **Theoretical minimum:** **0**
> **Theoretical maximum:** **1**
> ---
> ## 6) Grading Script (Required)
> **Choose:** **Custom** (do not use the template as-is; paste the script below).
> **Paste this entire script into the Grading Script field:**
> ```python
> from __future__ import annotations
> import re
> from collections import Counter
> import pandas as pd
> REQUIRED_SUB_COLS = {"image_id", "grammar_string"}
> REQUIRED_ANS_COLS = {"image_id", "grammar_string"}
> W_NODE = 0.40
> W_EDGE = 0.40
> W_OPS = 0.10
> W_VALID = 0.10
> _COMP_RE = re.compile(r"\*([a-z])([A-Z]{2}\d)")
> _CONN_RE = re.compile(r"\^([a-z])([a-z])")
> _VALID_RE = re.compile(
> r"^(\*[a-z][A-Z]{2}\d(?:[-+]+)?)+(\^[a-z][a-z])*$"
> )
> def _parse(s: str):
> if not isinstance(s, str) or not s:
> return [], set(), [], False
> s_stripped = s.strip()
> nodes = []
> edges = set()
> ops = []
> comps = list(_COMP_RE.finditer(s_stripped))
> for m in comps:
> nodes.append((m.group(1), m.group(2)))
> for i in range(len(comps) - 1):
> between = s_stripped[comps[i].end(): comps[i + 1].start()].strip()
> if between:
> ops.append(between)
> for m in _CONN_RE.finditer(s_stripped):
> a, b = m.group(1), m.group(2)
> if a != b:
> edges.add(frozenset({a, b}))
> valid = bool(nodes) and bool(_VALID_RE.match(s_stripped))
> return nodes, edges, ops, valid
> def _multiset_jaccard(a, b):
> if not a and not b:
> return 1.0
> inter = sum((a & b).values())
> union = sum((a | b).values())
> if union == 0:
> return 1.0
> return float(inter) / float(union)
> def _node_jaccard(pred_nodes, true_nodes):
> return _multiset_jaccard(
> Counter(t for _, t in pred_nodes),
> Counter(t for _, t in true_nodes),
> )
> def _edge_typed_jaccard(pred_nodes, pred_edges, true_nodes, true_edges):
> pred_map = {L: T for L, T in pred_nodes}
> true_map = {L: T for L, T in true_nodes}
> def _typed(edge_set, lmap):
> out = []
> for e in edge_set:
> u, v = list(e)
> tu = lmap.get(u)
> tv = lmap.get(v)
> if tu is None or tv is None:
> out.append(("??", "??"))
> else:
> out.append(tuple(sorted((tu, tv))))
> return Counter(out)
> return _multiset_jaccard(_typed(pred_edges, pred_map), _typed(true_edges, true_map))
> def _op_jaccard(pred_ops, true_ops):
> return _multiset_jaccard(Counter(pred_ops), Counter(true_ops))
> def _row_score(pred, truth):
> pn, pe, po, pv = _parse(pred)
> tn, te, to, _ = _parse(truth)
> row = (
> W_NODE * _node_jaccard(pn, tn)
> + W_EDGE * _edge_typed_jaccard(pn, pe, tn, te)
> + W_OPS * _op_jaccard(po, to)
> + W_VALID * (1.0 if pv else 0.0)
> )
> return float(max(0.0, min(1.0, row)))
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> try:
> if not REQUIRED_SUB_COLS.issubset(set(submission.columns)):
> return 0.0
> if not REQUIRED_ANS_COLS.issubset(set(answers.columns)):
> return 0.0
> if submission["image_id"].duplicated().any():
> return 0.0
> if answers["image_id"].duplicated().any():
> return 0.0
> if len(submission) != len(answers):
> return 0.0
> if set(submission["image_id"]) != set(answers["image_id"]):
> return 0.0
> sub = submission[["image_id", "grammar_string"]].copy()
> if sub["grammar_string"].isna().any():
> return 0.0
> sub["grammar_string"] = sub["grammar_string"].astype(str)
> merged = answers[["image_id", "grammar_string"]].merge(
> sub, on="image_id", how="left", suffixes=("_true", "_pred")
> )
> if merged["grammar_string_pred"].isna().any():
> return 0.0
> scores = [
> _row_score(str(p), str(t))
> for p, t in zip(
> merged["grammar_string_pred"].tolist(),
> merged["grammar_string_true"].tolist(),
> )
> ]
> if not scores:
> return 0.0
> return float(max(0.0, min(1.0, sum(scores) / len(scores))))
> except Exception:
> return 0.0
> ```
> ---
> ## 7) Data Preparation Pipeline
> **Input — raw/:**
> The dataset you selected provides the raw inputs. The uploaded dataset zip contains:
> - `metadata.csv` — five columns: `src_id`, `grammar_string`, `weight_lb`, `thrust_lb`, `feasibility`. One row per source UAV.
> - `meshes/<src_id>.npz` — NumPy archive per source UAV with keys `vertices` (float32, Nx3) and `faces` (int32, Mx3).
> **Script — prepare.py:**
> Choose **Custom** and paste the script below.
> **Paste this entire script into the prepare.py editor:**
> ```python
> from __future__ import annotations
> import re
> from pathlib import Path
> TRAIN_FRACTION = 0.80
> TOTAL_ROWS = 1400
> LABEL_NOISE_FRACTION = 0.40
> LABEL_NOISE_EDITS_MIN = 1
> LABEL_NOISE_EDITS_MAX = 3
> WEIGHT_ROUND_LB = 5.0
> WEIGHT_JITTER_FRAC = 0.25
> THRUST_ROUND_LB = 25.0
> THRUST_JITTER_FRAC = 0.25
> MESH_ROT_DEG_MAX = 90.0
> MESH_SCALE_MIN = 0.75
> MESH_SCALE_MAX = 1.25
> MESH_JITTER_FRAC = 0.020
> MESH_VERT_DROPOUT_MIN = 0.15
> MESH_VERT_DROPOUT_MAX = 0.30
> CURATION_SEED     = 0xC17A4D83
> ID_PERM_SEED      = 0x7F2A9E51
> SPLIT_SEED        = 0x9E3B2C84
> MESH_XFORM_SEED   = 0x4A8D16F2
> NUMERIC_HINT_SEED = 0xB52E91C7
> LABEL_NOISE_SEED  = 0x38F7D216
> _COMP_RE = re.compile(r"\*([a-z])([A-Z])([A-Z])(\d)")
> _CONN_RE = re.compile(r"\^([a-z])([a-z])")
> def _corrupt_grammar(s, rng):
> kinds = [
> "flip_size_digit", "flip_type_letter", "drop_connection",
> "add_connection", "swap_connection_endpoint",
> ]
> rng.shuffle(kinds)
> for kind in kinds:
> try:
> if kind == "flip_size_digit":
> comps = list(_COMP_RE.finditer(s))
> if not comps:
> continue
> m = comps[rng.randint(0, len(comps))]
> old_d = int(m.group(4))
> pool = [d for d in range(5) if d != old_d]
> new_d = pool[rng.randint(0, len(pool))]
> return s[: m.start(4)] + str(new_d) + s[m.end(4):]
> if kind == "flip_type_letter":
> comps = list(_COMP_RE.finditer(s))
> if not comps:
> continue
> m = comps[rng.randint(0, len(comps))]
> old = m.group(3)
> pool = [c for c in "LMNOP" if c != old]
> new = pool[rng.randint(0, len(pool))]
> return s[: m.start(3)] + new + s[m.end(3):]
> if kind == "drop_connection":
> conns = list(_CONN_RE.finditer(s))
> if not conns:
> continue
> m = conns[rng.randint(0, len(conns))]
> return s[: m.start()] + s[m.end():]
> if kind == "add_connection":
> letters = sorted({m.group(1) for m in _COMP_RE.finditer(s)})
> if len(letters) < 2:
> continue
> a = letters[rng.randint(0, len(letters))]
> b = letters[rng.randint(0, len(letters))]
> while b == a:
> b = letters[rng.randint(0, len(letters))]
> return s + f"^{a}{b}"
> if kind == "swap_connection_endpoint":
> conns = list(_CONN_RE.finditer(s))
> letters = sorted({m.group(1) for m in _COMP_RE.finditer(s)})
> if not conns or len(letters) < 2:
> continue
> m = conns[rng.randint(0, len(conns))]
> which = rng.randint(1, 3)
> old = m.group(which)
> pool = [c for c in letters if c != old]
> if not pool:
> continue
> new = pool[rng.randint(0, len(pool))]
> start = m.start(which)
> end = m.end(which)
> return s[:start] + new + s[end:]
> except Exception:
> continue
> return s
> def _rotz(deg):
> import numpy as np
> r = np.deg2rad(deg)
> c, s = np.cos(r), np.sin(r)
> return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]], dtype=np.float32)
> def _perturb_mesh(verts, faces, rng):
> import numpy as np
> verts = np.asarray(verts, dtype=np.float32).copy()
> faces = np.asarray(faces, dtype=np.int32).copy()
> angle = float(rng.uniform(-MESH_ROT_DEG_MAX, MESH_ROT_DEG_MAX))
> R = _rotz(angle)
> centroid = verts.mean(axis=0)
> verts = (verts - centroid) @ R.T + centroid
> scale = float(rng.uniform(MESH_SCALE_MIN, MESH_SCALE_MAX))
> verts = (verts - centroid) * scale + centroid
> bbox_min = verts.min(axis=0)
> bbox_max = verts.max(axis=0)
> diag = float(np.linalg.norm(bbox_max - bbox_min))
> if diag > 0:
> sigma = MESH_JITTER_FRAC * diag
> verts += rng.normal(0.0, sigma, size=verts.shape).astype(np.float32)
> n = len(verts)
> if n > 4:
> drop_frac = float(rng.uniform(MESH_VERT_DROPOUT_MIN, MESH_VERT_DROPOUT_MAX))
> n_drop = int(n * drop_frac)
> if n_drop > 0:
> drop_idx = rng.choice(n, size=n_drop, replace=False)
> keep_mask = np.ones(n, dtype=bool)
> keep_mask[drop_idx] = False
> old_to_new = -np.ones(n, dtype=np.int64)
> old_to_new[keep_mask] = np.arange(int(keep_mask.sum()))
> verts = verts[keep_mask]
> faces_new = old_to_new[faces]
> face_keep = (faces_new >= 0).all(axis=1)
> faces = faces_new[face_keep].astype(np.int32)
> return verts.astype(np.float32), faces.astype(np.int32)
> def _noisy_numeric(val, round_to, jitter_frac, rng):
> import numpy as np
> if not np.isfinite(val):
> return 0.0
> jittered = float(val) * (1.0 + rng.normal(0.0, jitter_frac))
> return float(round(jittered / round_to) * round_to)
> def prepare(raw: Path, public: Path, private: Path) -> None:
> import numpy as np
> import pandas as pd
> raw = Path(raw); public = Path(public); private = Path(private)
> public.mkdir(parents=True, exist_ok=True)
> private.mkdir(parents=True, exist_ok=True)
> (public / "train").mkdir(parents=True, exist_ok=True)
> (public / "test").mkdir(parents=True, exist_ok=True)
> def _locate_raw(root):
> import shutil
> best = None
> for p in [root] + [d for d in root.rglob("*") if d.is_dir()]:
> has_meta = (p / "metadata.csv").exists()
> has_mesh = (p / "meshes").is_dir() and any((p / "meshes").glob("*.npz"))
> if has_meta and has_mesh:
> return p
> if has_meta and best is None:
> best = p
> if best is not None:
> mc = [d for d in root.rglob("meshes") if d.is_dir() and any(d.glob("*.npz"))]
> if mc:
> tgt = best / "meshes"
> if not tgt.exists():
> try: tgt.symlink_to(mc[0], target_is_directory=True)
> except Exception:
> try: shutil.copytree(mc[0], tgt)
> except Exception: pass
> return best
> npz = list(root.rglob("*.npz"))
> if npz and npz[0].parent.name == "meshes":
> return npz[0].parent.parent
> return root
> orig_raw = raw
> raw = _locate_raw(raw)
> if not (raw / "metadata.csv").exists() or not (raw / "meshes").is_dir():
> print("[prepare] DEBUG: orig raw =", orig_raw, " resolved =", raw)
> try:
> for p in sorted(orig_raw.rglob("*"))[:60]:
> print("  ", p.relative_to(orig_raw), "/" if p.is_dir() else "")
> except Exception as e:
> print("  tree dump failed:", e)
> meta = pd.read_csv(raw / "metadata.csv")
> mesh_dir = raw / "meshes"
> have = [int(s) for s in meta["src_id"].tolist() if (mesh_dir / f"{int(s):05d}.npz").exists()]
> meta = meta[meta["src_id"].isin(have)].reset_index(drop=True)
> if len(meta) < TOTAL_ROWS:
> raise RuntimeError(f"Only {len(meta)} usable rows but TOTAL_ROWS={TOTAL_ROWS}.")
> def _bucket(s):
> s = str(s).lower()
> if "couldnotstabilize" in s or "infeasible" in s or "fail" in s:
> return "infeasible"
> if "marginal" in s or "couldnothover" in s:
> return "marginal"
> return "feasible"
> meta["_bucket"] = meta["feasibility"].apply(_bucket)
> curation_rng = np.random.RandomState(CURATION_SEED)
> bucket_targets = {
> "feasible": int(TOTAL_ROWS * 0.40),
> "marginal": int(TOTAL_ROWS * 0.30),
> "infeasible": TOTAL_ROWS - int(TOTAL_ROWS * 0.40) - int(TOTAL_ROWS * 0.30),
> }
> picks = []
> for b, want in bucket_targets.items():
> pool = meta[meta["_bucket"] == b].index.to_numpy()
> if len(pool) == 0:
> continue
> take = min(want, len(pool))
> picks.extend(int(i) for i in curation_rng.choice(pool, size=take, replace=False))
> shortfall = TOTAL_ROWS - len(picks)
> if shortfall > 0:
> remaining = [i for i in range(len(meta)) if i not in set(picks)]
> picks.extend(int(i) for i in curation_rng.choice(
> remaining, size=min(shortfall, len(remaining)), replace=False
> ))
> meta = meta.iloc[sorted(picks)].reset_index(drop=True)
> n_total = len(meta)
> meta["image_id"] = (
> np.random.RandomState(ID_PERM_SEED).permutation(n_total).astype(int).tolist()
> )
> split_rng = np.random.RandomState(SPLIT_SEED)
> train_parts, test_parts = [], []
> for _, grp in meta.groupby("_bucket", sort=True):
> grp = grp.sort_values("image_id").reset_index(drop=True)
> idx = np.arange(len(grp))
> split_rng.shuffle(idx)
> n_train = int(round(len(grp) * TRAIN_FRACTION))
> train_parts.append(grp.iloc[idx[:n_train]])
> test_parts.append(grp.iloc[idx[n_train:]])
> train_df = pd.concat(train_parts, axis=0).reset_index(drop=True)
> test_df = pd.concat(test_parts, axis=0).reset_index(drop=True)
> assert set(train_df["image_id"]).isdisjoint(set(test_df["image_id"]))
> assert set(train_df["src_id"]).isdisjoint(set(test_df["src_id"]))
> def _xform_rng(iid):
> return np.random.RandomState((MESH_XFORM_SEED ^ (int(iid) * 2654435761)) & 0xFFFFFFFF)
> for split_name, df in (("train", train_df), ("test", test_df)):
> out_dir = public / split_name
> for _, row in df.iterrows():
> iid = int(row["image_id"])
> sid = int(row["src_id"])
> with np.load(str(mesh_dir / f"{sid:05d}.npz")) as d:
> v = d["vertices"]; f = d["faces"]
> v2, f2 = _perturb_mesh(v, f, _xform_rng(iid))
> np.savez_compressed(str(out_dir / f"{iid:06d}.npz"), vertices=v2, faces=f2)
> hint_rng = np.random.RandomState(NUMERIC_HINT_SEED)
> def _add_hints(df):
> df = df.copy()
> df["noisy_weight_lb"] = [
> _noisy_numeric(v, WEIGHT_ROUND_LB, WEIGHT_JITTER_FRAC, hint_rng)
> for v in df["weight_lb"].tolist()
> ]
> df["noisy_thrust_lb"] = [
> _noisy_numeric(v, THRUST_ROUND_LB, THRUST_JITTER_FRAC, hint_rng)
> for v in df["thrust_lb"].tolist()
> ]
> return df
> train_df = _add_hints(train_df)
> test_df = _add_hints(test_df)
> noise_rng = np.random.RandomState(LABEL_NOISE_SEED)
> n_train = len(train_df)
> n_flip = int(round(n_train * LABEL_NOISE_FRACTION))
> if n_flip > 0:
> flip_idx = noise_rng.choice(n_train, size=n_flip, replace=False)
> new_labels = train_df["grammar_string"].to_numpy().copy()
> for i in flip_idx:
> new_labels[i] = _corrupt_grammar(str(new_labels[i]), noise_rng)
> train_df = train_df.copy()
> train_df["grammar_string"] = new_labels
> train_out = (
> train_df[["image_id", "grammar_string", "noisy_weight_lb", "noisy_thrust_lb"]]
> .sort_values("image_id").reset_index(drop=True)
> )
> train_out.to_csv(str(public / "train.csv"), index=False)
> test_out = (
> test_df[["image_id", "noisy_weight_lb", "noisy_thrust_lb"]]
> .sort_values("image_id").reset_index(drop=True)
> )
> test_out.to_csv(str(public / "test.csv"), index=False)
> sample = test_out[["image_id"]].copy()
> sample["grammar_string"] = "*aMM0"
> sample.to_csv(str(public / "sample_submission.csv"), index=False)
> answers = (
> test_df[["image_id", "grammar_string"]]
> .sort_values("image_id").reset_index(drop=True)
> )
> answers.to_csv(str(private / "answers.csv"), index=False)
> ```
> **Then run "Run Prepare"** to confirm the pipeline produces `public/` (`train/`, `test/`, `train.csv`, `test.csv`, `sample_submission.csv`) and `private/` (`answers.csv`).
> ---
> ## 8) What Not To Use
> Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score.
> - **Purely rule-based mesh-to-grammar pipelines.** The grammar-reconstruction logic must be learned from `public/train/*.npz` + `public/train.csv`. Hand-coded geometric rules that emit `*<letter><TYPE_CODE>` + `^xy` tokens without consulting the training data are prohibited.
> - **Identifying or downloading the upstream source of the meshes / grammar strings.** Any pipeline step that queries external corpora to recover the clean `(mesh, grammar_string)` pairs is prohibited.
> - **Pretrained checkpoints with mesh-part-segmentation supervision on this domain.** Generic object-level 3D backbones (PointNet, PointNet++, DGCNN, Point-BERT, PointTransformer, etc.) and generic 2D/3D foundation models are allowed.
> - **Mesh-hash / vertex-hash / geometric-fingerprint lookup against any public 3D-mesh index** to recover upstream identity.
> - **Reverse-engineering the `TYPE_CODE` vocabulary** from the `prepare.py` source, filesystem probes, or external token palettes. The vocabulary must be learned from `public/train.csv` alone.
> - **Hosted / closed-source API models at any stage** (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.), including distillation or pseudo-labelling from such teachers. Only open-weights models and self-trained pipelines are permitted.
> - **Grader / filesystem exploitation.** Hard-coded answer dictionaries, probes for `private/answers.csv`, or any channel other than `public/train/*`, `public/train.csv`, `public/test/*`, `public/test.csv`, and `public/sample_submission.csv`.
> - **Ensembles mixing allowed and prohibited components.** A single prohibited component contaminates the whole ensemble.
> Zero-shot use of generic open-weights 3D backbones is permitted as long as the checkpoint was not trained with part-segmentation supervision on this domain.
> ---
> ## 9) Agent Evaluation Runs
> No form fill. Agent evaluations run automatically when you submit the challenge for review.
> ---
> ## Checklist before submitting
> - [ ] Difficulty: Hard
> - [ ] Challenge Title: 3D Mesh to Grammar String Reconstruction
> - [ ] Problem Description: pasted (Overview, Evaluation, Dataset, Submission, What Not To Use)
> - [ ] Tags: 3d, structured-prediction, sequence-to-sequence
> - [ ] Grading: Maximize; min 0; max 1
> - [ ] Grading Script: full custom `grade.py` pasted
> - [ ] Data Preparation: raw = `metadata.csv` + `meshes/*.npz`; `prepare.py` pasted; "Run Prepare" succeeded
> - [ ] Challenge is tied to the accepted dataset

Inspiration note: Useful as a transformation task pattern where inputs must be converted into a structured target sequence under domain-specific rules.

## Synthetic Morphological Inflection Engine
- Challenge URL: https://drive.google.com/drive/folders/1pIBw3NdK5VGzQbAxutmm1n-S5Yh9-pV9
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: Sequence To Sequence (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: From Google Drive challenge collection
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: See description if specified
- Tags: Not shown/captured
- Best/top context found: Google Drive: Drive folder 2 / inferred / Synthetic Morphological Inflection Engine

Full challenge description from Drive:

> # Challenge creation form — fill-in
> ## 1) Difficulty
> **Select:** **Hard**
> ---
> ## 2) GPU Tier
> **Select:** **A10G** — standard ML workload; the model size is capped under 50 M parameters and the data is small text.
> ---
> ## 3) Challenge Title
> ```
> Synthetic Contextual Sequence Transduction
> ```
> ---
> ## 4) Problem Description
> # Synthetic Contextual Sequence Transduction
> ## Overview
> Sequence transduction — mapping one token sequence to another through learned rules — is a fundamental capability in language modelling. When the underlying transformation is hidden, multi-step, and context-dependent, recovering it from examples alone becomes a non-trivial induction problem.
> This challenge presents a fully synthetic transformation system. Each input is a short token string consisting of a context token, a base token, and five categorical control codes. The corresponding output is a short character sequence. The mapping is entirely synthetic and does not appear in any natural-language corpus, so pretrained models cannot transfer their knowledge of any real language; the solver must induce the mapping from the labelled training pairs alone.
> Your task is to predict the target character sequence for each test input.
> The following solver behaviours will cause the submission to be rejected on review, regardless of leaderboard score:
> - Pretrained weights from any general-purpose language model, sequence-to-sequence model, or foundation model. All model weights must be randomly initialised. The challenge tests rule induction from the provided training pairs alone, and pretrained weights bypass that test.
> - Total trainable parameter count above 50 million. Architecture choice is free, but the parameter budget is a hard cap. Brute-force memorisation through over-parameterised models is out of scope.
> - Hosted or closed-source API models at any stage of training or inference — OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, and similar — and any distillation or pseudo-labelling from such teachers. Only open-weights or self-trained pipelines are permitted, and only when randomly initialised.
> - Hand-written rule engines, regex tables, or symbolic simulators that produce predictions without any learned parameters fitted on `public/train.csv`. The challenge specifically tests learning the mapping; rule-based shortcuts are out of scope.
> - Using test labels or test-set statistics during training, validation, or feature engineering. Any form of test-set leakage will cause the submission to be rejected.
> - Leaderboard probing — large numbers of submissions crafted to binary-search the test set, or any strategy whose effectiveness depends on repeated scoring of probe submissions.
> - Grader or platform exploitation — hard-coded `sample_id` to `target` dictionaries, filesystem probes for the private answers file, attempts to read `private/answers.csv`, or any channel other than `public/`.
> - Ensembles mixing allowed and prohibited components. A single prohibited component contaminates the whole ensemble.
> ## Evaluation
> Submissions are scored using **per-character positional accuracy** across all test samples. For each sample, the predicted and true target strings are compared character-by-character from the left. Missing positions in a shorter prediction and extra positions in a longer prediction both count as incorrect.
> Concretely, for each sample the grader takes `max(len(predicted), len(true))` as the number of positions to score. Positions where both strings have a character and those characters match contribute one correct count; all other positions contribute zero. The final score is the sum of correct positions divided by the sum of total positions across all test samples.
> Higher is better. Theoretical minimum is 0.0; theoretical maximum is 1.0.
> Approximate scores for several common solver strategies:
> - The placeholder baseline that writes `"aaaaaa"` for every sample scores around 0.03.
> - Copying the base token directly into the output scores around 0.35.
> - A trained sequence-to-sequence model that captures the dominant mapping typically scores in the 0.50 to 0.75 range.
> Structural failures force the final score to 0.0:
> - Missing the `sample_id` or `target` column in the submission.
> - Duplicate `sample_id` values in submission or answers.
> - Submission length not matching the number of test samples.
> - Set of `sample_id` values not exactly matching the set in `test.csv`.
> - Any unhandled exception raised during grading.
> Extra columns beyond the two required are ignored.
> ## Dataset
> After preparation, the public directory contains:
> - `train.csv` — labelled training pairs, with columns `sample_id`, `source`, `target`.
> - `test.csv` — unlabelled test inputs, with columns `sample_id` and `source` only.
> - `sample_submission.csv` — placeholder baseline that writes a default string for every test row.
> Training-data columns:
> - `sample_id` (int) — unique identifier.
> - `source` (str) — space-separated input string `<context> <base> <CODE1> <CODE2> <CODE3> <CODE4> <CODE5>`.
> - `target` (str) — output character sequence to be predicted.
> Test-data columns: the same as training minus the `target` column.
> The five categorical control codes use the following value sets:
> - `CODE1` — one of `PRS`, `PST`, `FUT`, `PRF`, `HAB`.
> - `CODE2` — one of `SG`, `DU`, `PL`.
> - `CODE3` — one of `NOM`, `ACC`, `DAT`, `GEN`.
> - `CODE4` — one of `IND`, `SBJ`, `IMP`.
> - `CODE5` — one of `ACT`, `MID`, `PAS`, `CAU`.
> Example `source` value:
> ```
> ve dibnasle PRF SG GEN SBJ MID
> ```
> ## Submission
> Submit a CSV file `submission.csv` with the following columns:
> - `sample_id` (int) — identifier from `test.csv`.
> - `target` (str) — predicted output character sequence.
> Requirements:
> - The file must contain one row per test sample plus a header row.
> - `sample_id` values must be unique and exactly match the set in `public/test.csv`.
> - Every `target` value must be a non-empty string.
> - Extra columns beyond the two required are ignored.
> Example, first five rows of a valid submission:
> ```csv
> sample_id,target
> 22500,gradila
> 22501,binsuke
> 22502,naritu
> 22503,kembashi
> 22504,porolen
> ```
> ---
> ## 5) Tags
> **Select:** `text`, `small-data`
> ---
> ## 6) Grading Configuration
> - **Grade direction:** **Maximize**
> - **Theoretical minimum:** `0.0`
> - **Theoretical maximum:** `1.0`
> ---
> ## 7) Grading Script
> **Select:** `Custom`
> ```python
> """
> grade.py — Synthetic Contextual Sequence Transduction
> Metric: per-character positional accuracy across all samples.
> For each sample, characters are compared position-by-position.
> Missing positions (shorter prediction) count as incorrect.
> Extra positions (longer prediction) count as incorrect.
> Returns 0.0 for any structurally invalid submission.
> """
> import pandas as pd
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> try:
> if "sample_id" not in submission.columns or "target" not in submission.columns:
> return 0.0
> if "sample_id" not in answers.columns or "target" not in answers.columns:
> return 0.0
> if submission["sample_id"].duplicated().any():
> return 0.0
> if answers["sample_id"].duplicated().any():
> return 0.0
> if len(submission) != len(answers):
> return 0.0
> if set(submission["sample_id"]) != set(answers["sample_id"]):
> return 0.0
> merged = answers.merge(
> submission, on="sample_id", how="left", suffixes=("_true", "_pred")
> )
> if merged["target_pred"].isna().any():
> return 0.0
> true_vals = merged["target_true"].astype(str).values
> pred_vals = merged["target_pred"].astype(str).values
> total_correct = 0
> total_positions = 0
> for t, p in zip(true_vals, pred_vals):
> max_len = max(len(t), len(p))
> if max_len == 0:
> continue
> correct = sum(1 for i in range(min(len(t), len(p))) if t[i] == p[i])
> total_correct += correct
> total_positions += max_len
> if total_positions == 0:
> return 0.0
> return float(max(0.0, min(1.0, total_correct / total_positions)))
> except Exception:
> return 0.0
> ```
> ---
> ## 8) Prepare Script
> ```python
> """
> prepare.py — Synthetic Contextual Sequence Transduction
> Reads raw/data.csv.
> Produces:
> public/  train.csv   (sample_id, source, target)
> test.csv    (sample_id, source)
> sample_submission.csv  (sample_id, target placeholder)
> private/ answers.csv (sample_id, target)
> """
> from pathlib import Path
> def prepare(raw: Path, public: Path, private: Path) -> None:
> import pandas as pd
> raw = Path(raw)
> public = Path(public)
> private = Path(private)
> public.mkdir(parents=True, exist_ok=True)
> private.mkdir(parents=True, exist_ok=True)
> df = pd.read_csv(str(raw / "data.csv"))
> df = df.sample(frac=1, random_state=42).reset_index(drop=True)
> split = int(len(df) * 0.75)
> train_df = df.iloc[:split].copy()
> test_df = df.iloc[split:].copy()
> assert len(set(train_df["sample_id"]) & set(test_df["sample_id"])) == 0
> train_df[["sample_id", "source", "target"]].to_csv(
> str(public / "train.csv"), index=False
> )
> test_df[["sample_id", "source"]].to_csv(
> str(public / "test.csv"), index=False
> )
> test_df[["sample_id", "target"]].to_csv(
> str(private / "answers.csv"), index=False
> )
> sub = test_df[["sample_id"]].copy()
> sub["target"] = "aaaaaa"
> sub.to_csv(str(public / "sample_submission.csv"), index=False)
> ```
> ---
> ## 9) What Not To Use
> Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score.
> - Pretrained weights from any general-purpose language model, sequence-to-sequence model, or foundation model. All model weights must be randomly initialised.
> - Total trainable parameter count above 50 million.
> - Hosted or closed-source API models at any stage of training or inference (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.), and any distillation or pseudo-labelling from such teachers.
> - Hand-written rule engines, regex tables, or symbolic simulators that produce predictions without any learned parameters fitted on `public/train.csv`.
> - Using test labels or test-set statistics during training, validation, or feature engineering.
> - Leaderboard probing — large numbers of submissions crafted to binary-search the private test set.
> - Grader or platform exploitation — hard-coded `sample_id` to `target` dictionaries, filesystem probes for `private/answers.csv`, or any channel other than `public/`.
> - Ensembles mixing allowed and prohibited components. A single prohibited component contaminates the whole ensemble.

Inspiration note: Useful as a transformation task pattern where inputs must be converted into a structured target sequence under domain-specific rules.

## Restoring the Diacritical Points of a Classical Syriac Codex
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7aj7rqkt55k1zrepbw37pn9189ccm5
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Classical Syriac is written as a consonantal skeleton: the meaning-bearing diacritical points — the Seyame that marks plurals, the dots above and below that separate otherwise-identical letters and disambiguate readings, and a long tail of rarer Syriac points — are layered on top. Strip those points away and the text is still readable as letters but loses much of its grammatical and lexical precision. This challenge asks your model to put them back.
> You are given the unpointed (consonantal) skeleton of each line from a 1545 AD Serto manuscript, and must output the fully pointed (diacritised) line. This is a diacritic-restoration / vocalisation problem — the same family as Arabic or Hebrew diacritisation — not handwritten-text recognition: there are no images, only text. The difficulty is that the points are sparse (about 5% of characters carry one), ambiguous (the same skeleton can take different points depending on grammar and context), and long-tailed (a handful of Syriac points appear only a few times in the whole codex), so a model must actually understand the language, not memorise.
> Task
> For each test line you are given its skeleton (the line with all diacritical points removed). Output the pointed line — the skeleton with every diacritical point restored to its correct base character. Keep the consonantal backbone exactly as given; your job is to add the points, not to change the letters.
> Evaluation
> Setup. A "mark" is any combining diacritic (Unicode category Mn) or Syriac point (U+0730–U+074A). Every base (non-mark) character carries a mark-string — the (possibly empty) sequence of marks attached to it; e.g. a base with one dot-above has mark-string "̇", a base with no point has mark-string "". All strings are Unicode NFC-normalised before scoring. Your predicted line is aligned to the gold line by their consonantal backbones (the base characters, which you were given as the skeleton), giving, at each base position, a (gold_mark, pred_mark) pair. The composite in [0, 1], higher better:
> Score = 0.30 * DiacriticF1 + 0.45 * MacroMarkF1 + 0.25 * ExactLineMatch
> DiacriticF1 (0.30) — micro-averaged F1 over all (gold_mark, pred_mark) base positions, pooled across every test line. Each position is counted as follows:
> True positive (TP): gold_mark is non-empty and pred_mark == gold_mark.
> False negative (FN): gold_mark is non-empty and pred_mark != gold_mark (you missed it, left it empty, or restored the wrong mark).
> False positive (FP): pred_mark is non-empty and pred_mark != gold_mark. This covers two cases: predicting a mark on a base whose gold_mark is empty (spurious mark), and predicting the wrong non-empty mark where the gold had a different one.
> Note a position where the gold has a mark and you predict a different non-empty mark counts as both an FN and an FP. A position where both gold_mark and pred_mark are empty counts as nothing. Then Precision = TP/(TP+FP), Recall = TP/(TP+FN), DiacriticF1 = 2·TP / (2·TP + FP + FN).
> MacroMarkF1 (0.45 — the dominant term) — computed per distinct mark-type, then averaged equally. The mark-types are the set of distinct non-empty gold_mark strings that occur in the test gold. For one mark-type L, over all base positions:
> TP(L): gold_mark == L and pred_mark == L.
> FN(L): gold_mark == L and pred_mark != L.
> FP(L): pred_mark == L and gold_mark != L (you predicted L where the gold was a different mark, or empty).
> F1(L) = 2·TP(L) / (2·TP(L) + FP(L) + FN(L)) (defined as 0 if that denominator is 0). MacroMarkF1 is the simple mean of F1(L) over all mark-types L. Because every type weighs the same, the rare Syriac points (each seen only a handful of times) count as much as the common Seyame and dots, so restoring only the frequent marks caps this term — it rewards handling the long tail.
> ExactLineMatch (0.25) — the fraction of test lines whose full predicted pointed string exactly equals the gold (after NFC normalisation).
> Dataset
> Text only; all fields are UTF-8 strings; there are no missing values. The data is 2,079 training lines and 704 test lines, split page-level from a single codex so test lines come from pages held out of training.
> public/train.csv — one row per training line (2,079 rows). Columns:
> line_id (string) — unique salted line identifier, e.g. SYR_a1b2c3d4e5f6.
> skeleton (string) — the consonantal line with all diacritical points removed (the model input).
> pointed (string) — the gold fully-diacritised line (the target).
> Example row (skeleton → pointed; the pointed form adds the points):
> line_id,skeleton,pointed
> SYR_a1b2c3d4e5f6,ܒܚܘܪܒܐ ܛܝܒܘ,ܒ݁ܚܘܪܒܐ ܛܝܒܘ
> public/test.csv — one row per test line (704 rows): line_id, skeleton. The pointed form is withheld.
> public/sample_submission.csv — a skeleton-echo baseline (predicts the unpointed text unchanged; restores nothing, scores ~0.05).
> public/metadata.json — a JSON object documenting the task. Keys:
> task (string) — one-line task description.
> submission_columns (list of strings) — the two required submission column names (["line_id", "pointed"]).
> composite_weights (object) — maps DiacriticF1/MacroMarkF1/ExactLineMatch to their weights 0.30/0.45/0.25.
> diacritics (string) — the definition of a mark (combining marks category Mn and Syriac points U+0730–U+074A) and a note on their sparsity/long tail.
> submission_note (string) — the submission requirement (one row covering every test line_id).
> Submission Format
> Submit a CSV at ./working/submission.csv with exactly these columns:
> line_id,pointed
> SYR_a1b2c3d4e5f6,ܒ݁ܚܘܪܒܐ ܛܝܒܘ
> SYR_b2c3d4e5f6a1,ܘܗ݇ܘܐ ܒܝܘܡܬܐ
> Requirements (strict — the grader rejects a violating submission rather than repairing it):
> Exactly the two columns line_id, pointed; no extra columns; no null/duplicate line_ids. Save the CSV UTF-8.
> One row for every test line_id — your submission must cover all of them. Missing a required line_id (or duplicate/null ids) causes the submission to be rejected; rows for any id outside the graded set are simply ignored.
> Preserve the consonantal backbone of the given skeleton and add the diacritical points; output as a UTF-8 Syriac string.
> Approach Guidelines
> This is sequence labelling / restoration over the skeleton: a character-level encoder (or a SMILES-style constrained decoder, or an LLM prompted to point the text) that predicts, for each base character, which point(s) to attach. Modelling morphology and context (plural agreement for Seyame, lexical disambiguation for the dots) is the core skill.
> Mind the long tail. MacroMarkF1 makes the rare Syriac points worth as much as the common ones; a model that only restores the three frequent marks is capped.
> Don't over-point. Spurious marks are false positives; precision matters as much as recall.
> What Not To Use
> Matching the skeletons against the source manuscript or any external Syriac corpus/edition (string search, alignment, or lookup) to read off the gold pointing. Line ids are salted; recovering the diacritised form from the originating manuscript transcription is prohibited.
> Any external pre-pointed Syriac text tied to this manuscript used to look up answers for these specific lines.
> Hardcoded {skeleton → pointed} tables, or training on the test lines.

Inspiration note: Useful as a sequence-to-sequence pattern where a noisy or incomplete source sequence must be transformed into a normalized target sequence under domain-specific rules.

## Schema-Action Edit Ledger Recovery
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cg896r3jh01wckvg8dhapf989nfxt
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, generative
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Fine-tuning data for tool-using assistants often contains small but consequential disagreements between a user request, an action schema, and a recorded structured trace. This challenge turns those disagreements into a candidate edit-ledger recovery task.
> Each row gives a masked request card, an anonymized action-schema catalog, a corrupted structured trace, and a list of candidate atomic edits. Your task is to select the ordered candidate edit ids that repair the corrupted trace. The candidates include correct edits and close decoys, such as the right argument with the wrong value signature, the right value signature assigned to the wrong argument, an unnecessary delete operation, or a wrong replacement action name.
> The request card does not expose raw argument values directly. Instead, values are represented by typed value slots and compact value signatures. This makes the task a schema-action alignment problem rather than a direct copy task. Strong solutions must compare the masked request, tool descriptions, parameter descriptions, corrupted trace, and candidate edits.
> Dataset
> The prepared public data contains 1125 labeled training rows and 375 test rows. The split is grouped so that repeated request templates and schema templates are isolated to either training or test.
> Files:
> train.csv: Labeled examples with public evidence fields and answer_json.
> test.csv: Unlabeled examples with the same public evidence fields, without answer_json.
> sample_submission.csv: Example submission file with the required columns.
> Columns:
> id (string): Unique task id.
> prompt (string): Task instruction.
> request_card_json (JSON object): Masked user request and typed value-slot cards.
> tool_catalog_json (JSON list): Available anonymized action schemas. Each schema has name, description, and parameters.
> corrupted_call_json (JSON list): Incorrect trace to audit. Argument values are represented by value-signature cards rather than raw literals.
> candidate_edits_json (JSON list): Candidate atomic edits. Each candidate has an edit_id, operation type, call index, and operation-specific fields.
> candidate_count (integer): Number of candidate edits in the row.
> answer_json (JSON object, train only): Correct ordered edit-id ledger.
> Candidate edit operations include:
> set_name: Replace the action name at a call index.
> set_arg: Set or replace one argument at a call index using a value-signature card.
> delete_arg: Remove one argument from a call index.
> Submission Format
> Submit a CSV with columns id and answer_json in any order.
> answer_json must be a JSON object with exactly one key:
> edit_ids (JSON list of strings): Ordered candidate edit ids that form the repair ledger.
> Example submission CSV:
> id,answer_json
> fcpr_0a1b2c3d4e5f6a7b,"{""edit_ids"":[""e03_a1b2"",""e11_c3d4"",""e07_e5f6""]}"
> fcpr_9f8e7d6c5b4a3210,"{""edit_ids"":[""e00_1234"",""e04_abcd""]}"
> Evaluation
> Each row receives a score from 0 to 1:
> row_score = 0.62 * exact_ledger + 0.22 * edit_id_f1 + 0.10 * ordered_prefix_score + 0.06 * edit_count_score
> Metric definitions:
> exact_ledger: 1 if the submitted edit_ids list exactly matches the true ordered list, otherwise 0.
> edit_id_f1: Standard set F1 over submitted and true edit ids, ignoring order.
> ordered_prefix_score: Length of the initial correctly ordered prefix divided by the true edit count. If the first two submitted ids match the first two true ids and the third differs, the prefix length is 2.
> edit_count_score: 1 - abs(submitted_edit_count - true_edit_count) / true_edit_count, clipped to a minimum of 0.
> For edit_id_f1, precision is correct submitted ids divided by submitted ids, recall is correct submitted ids divided by true ids, and F1 is 2 * precision * recall / (precision + recall). If both submitted and true sets are empty, F1 is 1.
> The final leaderboard score is the arithmetic mean of row_score across all test rows.
> What Not To Use
> Hardcoded mappings from task ids to answers.
> Manual lookup of original upstream examples.
> External copies of the exact generated public/test rows.
> Hidden files or answer files not included in the public data.
> Reconstructing answers from package-generation internals instead of the public task fields.

Inspiration note: Useful as a sequence-to-sequence pattern where structured, noisy, or partial inputs must be transformed into a normalized target sequence with strict output format.

## Code Behavior Fingerprint Recovery
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7edk930p64eynrqgtg2jfxfh89mrwv
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, generative
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Fine-tuning data for coding assistants often includes generated solutions that pass obvious cases but fail hidden edge cases. This challenge asks you to recover a compact behavior fingerprint for a candidate solution.
> Each row gives a programming task, a candidate Python solution, and a non-executable blueprint describing the shape of hidden tests. Your task is to infer the hidden pass/fail signature. You are not asked to write code or execute public tests; the output is a structured JSON behavior record.
> Dataset
> The prepared public data contains 1200 labeled training rows and 400 test rows. Each row is derived from a code-instruction example by preserving the task and candidate solution, replacing exact hidden tests with coarse test blueprints, and using the hidden execution results as the target fingerprint.
> Files:
> train.csv: Labeled examples with public fields and answer_json.
> test.csv: Unlabeled examples with the same public task fields.
> sample_submission.csv: Valid baseline submission with the required columns.
> Columns:
> id (string): Unique task id.
> prompt (string): Task instruction.
> problem_statement (string): Programming task.
> candidate_code (string): Candidate Python solution.
> test_blueprint_json (JSON list): Coarse summaries of hidden tests. These are descriptors, not executable tests.
> mask_length (integer): Number of hidden test outcomes represented by pass_mask.
> answer_json (JSON object, train only): Correct behavior fingerprint.
> Submission Format
> Submit a CSV with exactly these columns, in any order:
> id
> answer_json
> answer_json must be a JSON object with these fields:
> pass_mask (string): Binary string where 1 means the corresponding hidden test passes and 0 means it fails.
> fail_count (integer): Number of zeroes in pass_mask.
> score_bucket (string): sNN, where NN is the number of passing tests padded to two digits.
> Example answer_json value:
> {"pass_mask":"1101011110","fail_count":3,"score_bucket":"s07"}
> Example submission CSV:
> id,answer_json
> ctbr_eb585f23ba45d0caf4,"{""pass_mask"":""1111111111"",""fail_count"":0,""score_bucket"":""s10""}"
> ctbr_f23af8a80e9692da65,"{""pass_mask"":""1101011110"",""fail_count"":3,""score_bucket"":""s07""}"
> Evaluation
> Each row receives a score from 0 to 1:
> row_score = 0.50 * mask_similarity + 0.22 * fail_count_score + 0.18 * score_bucket_exact + 0.10 * exact_object
> Metric definitions:
> mask_similarity: 0.55 * hamming_agreement + 0.45 * failed_position_f1.
> hamming_agreement: Fraction of positions where the submitted pass_mask equals the true pass_mask. Length mismatches are treated as wrong positions.
> failed_position_f1: Standard set F1 over positions where the mask value is 0.
> fail_count_score: 1 - absolute_count_error / true_mask_length, clipped to [0, 1].
> score_bucket_exact: 1 when score_bucket matches exactly, otherwise 0.
> exact_object: 1 when pass_mask, fail_count, and score_bucket all match exactly, otherwise 0.
> For F1, precision is correct submitted failed positions divided by submitted failed positions, recall is correct submitted failed positions divided by true failed positions, and F1 is 2 precision * recall / (precision + recall). If both submitted and true failed-position sets are empty, F1 is 1.
> The final leaderboard score is the arithmetic mean of row_score across all test rows.
> What Not To Use
> Hardcoded mappings from task ids to answers.
> Manual lookup of original upstream examples.
> External copies of the exact generated public/test rows.
> Hidden files or answer files not included in the public data.
> Reconstructing answers from package-generation internals.

Inspiration note: Useful as a sequence-to-sequence pattern where structured, noisy, or partial inputs must be transformed into a normalized target sequence with strict output format.

## Robot Action Spine Recovery From Goal-Directed Video
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79f6wdp0wb5jv517qd2wkrnh89qdy1
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: video, feature-engineering, multimodal
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> This challenge uses real tabletop robot manipulation episodes. Each row gives a natural-language goal and a time window in a robot-camera video. Your task is to recover the ordered action spine for that window.
> An action spine is a compact temporal summary of the robot's behavior. The video window is divided into eight equal-duration bins. For each bin, the label is one token describing the dominant end-effector movement direction and gripper state during that part of the clip. Movement tokens use robot-frame directions such as x_pos, x_neg, y_pos, y_neg, z_pos, and z_neg; each is paired with open or closed. When the end effector is mostly stationary, the token is still_open or still_closed.
> The output is a structured temporal behavior record, not a single task category. Correct solutions must preserve the order of the eight bins, not just identify which motions appear somewhere in the video.
> Dataset
> The public data contains labeled training rows and unlabeled test rows. Video files are stored under videos/.
> Files:
> train.csv: Labeled rows with public evidence fields and answer_json.
> test.csv: Unlabeled rows with the same public evidence fields, without answer_json.
> sample_submission.csv: Example submission file with the required columns.
> videos/: MP4 robot-camera clips referenced by the CSV files.
> Columns:
> id (string): Unique row id.
> video (string): Relative path to the MP4 file under videos/.
> prompt (string): Challenge instruction asking for the ordered action spine.
> language_goal (string): Natural-language manipulation goal for the robot episode.
> episode_key (string): Anonymized trajectory identifier. A trajectory is one recorded robot episode.
> window_start_seconds (float): Start time of the evidence window in the video.
> window_end_seconds (float): End time of the evidence window in the video.
> fps (integer): Video frame rate.
> bin_count (integer): Number of equal-duration action-spine bins. This challenge uses 8.
> answer_json (JSON object, train only): Ground-truth action-spine object with sequence, switch_count, and dominant.
> Submission Format
> Submit a CSV with columns id and answer_json in any order.
> answer_json must contain:
> sequence (JSON list of strings): Exactly eight ordered action tokens, one per temporal bin, such as x_pos_open, z_neg_closed, or still_open.
> switch_count (integer): Number of adjacent token changes in sequence. For example, ["a","a","b"] has one switch.
> dominant (string): Most frequent token in sequence.
> Example submission CSV:
> id,answer_json
> bridge_0a1b2c3d4e5f6a7b,"{""sequence"":[""still_open"",""x_pos_open"",""x_pos_open"",""x_pos_open"",""still_closed"",""y_neg_closed"",""y_neg_closed"",""still_closed""],""switch_count"":4,""dominant"":""x_pos_open""}"
> bridge_9f8e7d6c5b4a3210,"{""sequence"":[""still_closed"",""z_pos_closed"",""z_pos_closed"",""z_pos_closed"",""x_neg_open"",""still_open"",""y_pos_open"",""still_open""],""switch_count"":5,""dominant"":""z_pos_closed""}"
> Evaluation
> Each row is scored from 0 to 1:
> row_score = 0.45 * position_accuracy^2 + 0.25 * token_f1^2 + 0.15 * switch_count_score + 0.10 * dominant_exact + 0.05 * exact_object
> Metric definitions:
> position_accuracy: Fraction of the eight sequence positions where the submitted token exactly matches the true token. If 6 of 8 positions match, this term is 6/8.
> token_f1: Multiset F1 over sequence tokens, ignoring order. Precision is matched submitted tokens divided by submitted token count, recall is matched true tokens divided by true token count, and F1 is 2 * precision * recall / (precision + recall).
> switch_count_score: max(0, 1 - abs(submitted_switch_count - true_switch_count) / max(1, true_sequence_length - 1)).
> dominant_exact: 1 if the submitted dominant token exactly matches the true dominant token, otherwise 0.
> exact_object: 1 if the parsed submitted JSON object exactly matches the parsed true object after normalization, otherwise 0.
> The final score is the arithmetic mean of row scores.
> What Not To Use
> Hardcoded mappings from row ids to answers.
> Manual lookup of ids or filenames outside the released public data.
> External copies of these exact rows with labels.
> Files or answer keys outside the released public data.

Inspiration note: Useful as a sequence-to-sequence pattern where structured, noisy, or partial inputs must be transformed into a normalized target sequence with strict output format.

## Reef Survey Abundance Sequence Reconstruction
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7b4e14vgh6d8mjy2cwcywj7588nymz
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-03; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> You are given anonymized ecological survey sequences. Each row represents one held-out survey station as an ordered sequence of observation tokens. Every observation token contains transformed survey context, spatial bins, habitat and depth groups, taxon codes, length groups, and protocol indicators. The original station identity is hidden, so the only usable signal is the structure of the sequence and the categorical relationships inside the observation tokens.
> Your task is to reconstruct an abundance-label sequence for each station. The prediction must contain exactly one output token for every input observation token, in the same order. The labels are:
> N - no individuals recorded for that observation.
> S - exactly one individual recorded.
> L - low abundance, from 2 to 4 individuals.
> H - high abundance, 5 or more individuals.
> This is intentionally not a simple row lookup task. The prepared split holds out entire station groups, stratified across survey wave, sub-region, and coarse station-level abundance profile. Feature names and categorical values are remapped, and the public features are transformed from the raw survey fields. Strong solutions should model taxon, length, habitat, depth, location, seasonal, and within-sequence context while handling a zero-heavy and long-tailed label distribution.
> Evaluation
> Submissions are scored using token-level macro F1 over the four labels. Higher is better.
> from sklearn.metrics import f1_score
> TOKENS = ["N", "S", "L", "H"]
> def evaluate(y_true_sequences, y_pred_sequences):
> y_true = []
> y_pred = []
> for true_seq, pred_seq in zip(y_true_sequences, y_pred_sequences):
> true_tokens = true_seq.split()
> pred_tokens = pred_seq.split()
> if len(true_tokens) != len(pred_tokens):
> raise ValueError("Predicted sequence length must match the answer sequence length.")
> y_true.extend(true_tokens)
> y_pred.extend(pred_tokens)
> return f1_score(y_true, y_pred, labels=TOKENS, average="macro", zero_division=0)
> Macro F1 gives equal weight to rare L and H tokens, so predicting only the majority label is a weak baseline.
> Dataset
> The downloadable prepared dataset contains only the public files solvers should use:
> public/train.csv - labeled training sequences.
> public/test.csv - unlabeled held-out sequences.
> public/sample_submission.csv - a valid majority-token baseline.
> train.csv columns:
> id (int): random sequence identifier.
> sequence_length (int): number of observation tokens in the sequence.
> input_sequence (string): observation tokens separated by ;. Each observation is a comma-separated set of key=value fields.
> target_sequence (string): whitespace-separated abundance labels for the training sequence.
> test.csv columns:
> id (int): random sequence identifier.
> sequence_length (int): number of observation tokens in the sequence.
> input_sequence (string): observation tokens separated by ;. Each observation is a comma-separated set of key=value fields.
> sample_submission.csv columns:
> id (int): sequence identifier from test.csv.
> target_sequence (string): example whitespace-separated label sequence using N, S, L, and H.
> Observation fields include transformed survey wave, seasonal bin, spatial bins, depth and visibility bins, missingness flags, habitat/stratum groups, taxon code, taxon hash bucket, length group, and protocol indicator.
> What Not To Use
> Do not use hidden or external information to reconstruct the held-out labels. In particular:
> Do not use private answers, reviewer notes, or any non-public target labels.
> Do not use row-order shortcuts, sequential ID patterns, or hard-coded per-id predictions.
> Do not reverse-map the anonymized tokens to the original station identities and then look up held-out labels.
> Do not hand-label the test sequences or use external labels beyond the provided public training file.
> Submission
> Submit a CSV named submission.csv with exactly two columns:
> id (int): sequence identifier from test.csv.
> target_sequence (string): whitespace-separated labels using only N, S, L, and H.
> Example CSV rows:
> id,target_sequence
> 800003,N S N L
> 800017,N N S
> 800024,H L N N S
> Requirements:
> Exactly one row per test sequence.
> Include the header row.
> No missing or duplicate id values.
> Each predicted sequence must have the same number of labels as that row's sequence_length.
> Every predicted label must be one of N, S, L, or H.
> Do not use hidden row-order shortcuts or hard-coded per-id labels.

Inspiration note: Useful because it maps structured, noisy evidence into ordered output sequences with exact-format validation and partial-credit metrics.

## Layered Image Compositing Program Repair
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76jt5n8vdknf4rnz0ap0rjtn89g1h2
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: image, feature-engineering, generative
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-03; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Professional graphics and VFX pipelines often outlive the metadata that created their renders. A project may retain its source layers, a damaged layer program, a broken full-resolution render, and only a degraded thumbnail of the intended result. Repairing such a project requires identifying which program instructions are wrong and recovering executable corrections.
> Each sample contains a background, four RGBA source layers, the current 28-token compositing program, its broken render, and a lightly degraded 64×64 reference of the intended render. Your task is to output the corrected 28-token program.
> This is counterfactual visual-program repair. Solvers must reason about how alternative program tokens would change a render, including noncommutative layer order, geometry, opacity, and blend interactions. A standard image classifier, detector, or segmentation model does not directly produce the required executable program.
> Exactly three non-order program fields are corrupted per sample, each on a different source layer. Every selected corruption is verified to produce a clear render change in the combined broken program. The four z_rank fields are supplied as valid structural context and must remain a permutation of 0,1,2,3; they are not selected as repair fields in this revision.
> Program Language
> The program contains four fixed layer blocks. Each block has seven integer tokens in this order:
> x, y, rotation, scale, blend, opacity, z_rank
> Token ranges and meanings:
> x: 0..4, horizontal placement on a five-position grid.
> y: 0..4, vertical placement on a five-position grid.
> rotation: 0..3, representing 0°, 90°, 180°, and 270°.
> scale: 0..2, representing small, medium, and large.
> blend: 0..2, representing normal, multiply, and screen.
> opacity: 0..3, representing 0.70, 0.80, 0.90, and 1.00.
> z_rank: 0..3. Across the four layer blocks, z ranks must be a permutation of 0,1,2,3.
> The flattened sequence positions are t00 through t27. Positions 0..6 describe layer 0, 7..13 layer 1, 14..20 layer 2, and 21..27 layer 3.
> Evaluation
> Submissions are scored using Counterfactual Program Repair Score, bounded to [1e-9, 1]. Higher is better.
> score = 0.45 * changed_field_accuracy
> + 0.30 * edit_set_f1
> + 0.15 * all_token_accuracy
> + 0.10 * exact_program_rate
> changed_field_accuracy evaluates only the three fields that differ between the damaged and intended programs.
> edit_set_f1 compares the submitted edits against the true edit set. An edit is correct only when its field and replacement value are both correct.
> all_token_accuracy checks the complete 28-token output.
> exact_program_rate requires every token in a sample to match.
> Copying the current program preserves many tokens but receives no credit on the two main repair components.
> The grading direction is Maximize. Configure minimum 1e-9 and maximum 1.
> Dataset
> Public files
> train.csv - IDs and current program tokens for 5,000 training samples.
> train_backgrounds.npy - Background RGB images, shape (5000, 3, 64, 64), uint8.
> train_layers.npy - Four RGBA layers per sample, shape (5000, 4, 4, 64, 64), uint8.
> train_broken_renders.npy - Broken RGB renders, shape (5000, 3, 64, 64), uint8.
> train_target_previews.npy - Lightly degraded full-resolution intended references, shape (5000, 3, 64, 64), uint8.
> train_targets.npy - Correct 28-token programs, shape (5000, 28), uint8.
> test.csv - IDs and current program tokens for 1,500 test samples.
> test_backgrounds.npy - Test backgrounds, shape (1500, 3, 64, 64).
> test_layers.npy - Test RGBA layers, shape (1500, 4, 4, 64, 64).
> test_broken_renders.npy - Test broken renders, shape (1500, 3, 64, 64).
> test_target_previews.npy - Test intended references, shape (1500, 3, 64, 64).
> sample_submission.csv - Required submission structure.
> train.csv and test.csv contain id followed by c00 through c27, where c denotes the current damaged program. Array row order matches CSV row order.
> Submission
> Submit exactly 1,500 rows with columns:
> id,t00,t01,...,t27
> Every token must be an integer in its documented field range. Each submitted z-order must be a permutation of 0,1,2,3. Missing IDs, duplicate IDs, fractional tokens, invalid ranges, and invalid z-orders are rejected.
> Example of a correctly formatted submission:
> id,t00,t01,t02,t03,t04,t05,t06,t07,t08,t09,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24,t25,t26,t27
> 5000,2,1,0,1,1,3,1,2,3,1,2,2,1,3,1,2,3,2,2,2,2,2,2,1,0,1,1,0
> 5001,1,3,3,1,1,3,2,4,1,0,0,0,0,1,4,2,0,1,0,0,0,1,1,2,0,2,2,3
> The example values illustrate formatting only. A real submission must contain exactly one row for every ID in test.csv.
> Restrictions
> Use only the provided challenge files.
> Do not access hidden files, derive targets from IDs, or reverse-engineer generation seeds.
> General-purpose pretrained vision models are allowed.

Inspiration note: Useful because it maps structured, noisy evidence into ordered output sequences with exact-format validation and partial-credit metrics.

## Proto-Form Reconstruction: Recovering Ancestral Words From Cognate Sets
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fmnvm685xc9gq4xtjakshzd89p89c
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, generative
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-03; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> When languages descend from a common ancestor, their words for the same concept
> (cognates) diverge through regular sound changes. Historical linguists run this
> process in reverse, the comparative method, comparing cognates across
> descendant ("daughter") languages to reconstruct the word as it was in the shared
> ancestor (the proto-form).
> This challenge automates that task. For each item you are given a set of cognate
> word-forms in several daughter languages and the target proto-language label; you must
> predict the reconstructed proto-form as a sequence of phonemes.
> The corpus spans 20 language families worldwide (e.g. Proto-Lalo, Proto-Chuukic,
> Proto-Germanic, Proto-Bai, Proto-Karen, Proto-Uralic, Proto-Hmong-Mien, Proto-Tupi).
> It is genuinely hard and low-resource: each family has its own phoneme inventory and
> sound-correspondence rules, examples per family are limited, and a strong solution
> must learn family-conditioned regularities rather than a single global mapping.
> Word-forms are written as space-separated phonemes (a standardized IPA-like
> transcription) , the representation linguists actually use.
> Evaluation
> Submissions are scored by the mean normalized phoneme edit-distance similarity
> (1 − NED), the standard metric for computational proto-language reconstruction.
> For each row, the prediction and the gold proto-form are split into phoneme tokens
> on whitespace; we compute the token-level Levenshtein distance, normalize by the
> longer length, and subtract from 1:
> NED = levenshtein(pred_tokens, gold_tokens) / max(len(pred_tokens), len(gold_tokens))
> row_score = 1 − NED (in [0, 1])
> final score = mean of row_score over all test rows.
> Higher is better; a prediction identical to the reference scores 1.0. The metric
> is averaged per-row (micro), so it does not depend on family balance.
> import numpy as np
> def _lev(a, b):
> if not a: return len(b)
> if not b: return len(a)
> prev = list(range(len(b) + 1))
> for i, ai in enumerate(a, 1):
> cur = [i]
> for j, bj in enumerate(b, 1):
> cur.append(min(prev[j] + 1, cur[-1] + 1, prev[j-1] + (ai != bj)))
> prev = cur
> return prev[-1]
> def evaluate(preds, golds):
> s = []
> for p, g in zip(preds, golds):
> pt, gt = str(p).split(), str(g).split()
> m = max(len(pt), len(gt))
> s.append(1.0 if m == 0 else 1.0 - _lev(pt, gt) / m)
> return float(np.mean(s))
> Reference points on the held-out test set (to calibrate expectations):
> constant most-common ≈ 0.06, copying a daughter form ≈ 0.26, and a non-learning
> retrieval shortcut (nearest training input → its proto-form) ≈ 0.29. Reconstruction
> genuinely differs from any single descendant, so these shortcuts stay low — a model
> that learns the sound correspondences should clear them by a wide margin, with ample
> headroom below 1.0.
> Dataset
> Files in public/:
> train.csv — 4,862 labeled rows: id, proto_language, num_daughters, cognate_set, proto_form.
> test.csv — 794 rows to reconstruct: same columns except proto_form.
> sample_submission.csv — the exact submission format (with placeholder text).
> Column meanings:
> id — (string) Opaque unique identifier (e.g. cog_0134e1fba15e).
> proto_language — (string) The target ancestor / family label (e.g. Proto-Germanic). Use it to condition the model.
> num_daughters — (int) Number of daughter forms provided (≥ 2).
> cognate_set — (string) The daughter word-forms, formatted Language: p h o n e m e s and separated by | (e.g. Woleaian: y a ʐ e m oː i | Sonsorolese: e l e m a u ð).
> proto_form — (string) Target (train only): the reconstructed ancestral word as space-separated phonemes (e.g. a r e m a u t i). May carry tone/length marks ¹ ² ³, ː) and a leading - for bound morphemes.
> Submission
> Submit a CSV with exactly these two columns:
> id — (string) Row identifier from test.csv.
> proto_form — (string) Your predicted proto-form, as space-separated phonemes.
> Example rows:
> id,proto_form
> cog_0134e1fba15e,a r e m a u t i
> cog_016b7229e6ee,tsʰ j æ n ¹
> Requirements
> Exactly 794 rows, one per id in test.csv; include the header row.
> id values must match test.csv exactly — no missing, extra, or duplicate ids.
> Every proto_form must be a non-null text string (empty strings are allowed but
> score poorly). Numeric / NaN / infinite values are rejected.
> Exactly the columns id,proto_form — extra columns are rejected.
> Allowed / Prohibited Methods
> Allowed
> Training or fine-tuning any sequence-to-sequence / language model on the provided
> train.csv (from scratch or via transfer learning from a pretrained model).
> Any preprocessing, tokenization, alignment, data augmentation, and decoding
> strategy; use of proto_language as conditioning.
> Prohibited
> No external gold lookup. Do not retrieve, download, or match the cognate sets
> against any external comparative-linguistics database, etymological dictionary, or
> wordlist to recover reference proto-forms. Work only from the provided train.csv.
> No hardcoding. Do not embed answers, per-id lookups, or precomputed target
> strings; do not reconstruct targets from the original raw source files.
> No non-ML shortcut solutions. Copying a daughter form, a constant, or plain
> nearest-neighbor retrieval of a training proto-form — without a learned
> reconstruction model — does not satisfy the task (and is capped near the ~0.29
> baseline by design).
> No test-set leakage. Do not train on, fit to, or peek at the test targets, and
> do not use the target at inference time.
> Notes
> The held-out set was de-duplicated and scrubbed of near-duplicate inputs relative
> to training, so memorizing or retrieving the nearest training example will not get
> you far — the benchmark rewards learning the sound-correspondence regularities.
> The split is stratified by family: every family in the test set is represented
> in training. (The test set covers 18 of the 20 families; two near-duplicate-heavy
> families were fully scrubbed from the held-out set.)
> Compute budget: the solution must run end-to-end within the challenge time/GPU
> limit, reading from ./dataset/public/ and writing ./working/submission.csv.

Inspiration note: Useful because it maps structured, noisy evidence into ordered output sequences with exact-format validation and partial-credit metrics.

## From Catalogue Prose to a Relation Graph of Art
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70wtfcmw46wdjswqmw9s5eyh89dwqa
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Museum and auction catalogues describe artworks in dense, free-flowing prose: who made a piece, what it depicts, what it is made of, what its forms symbolise, which movement it belongs to. Turning that prose into a structured relation graph — the machine-readable backbone of every digital art catalogue — is a hard reading-comprehension problem, because the relations are implicit, directed, and densely interrelated across a single description.
> This challenge asks your model to do exactly that. Given the text of an art-object description, output the full set of directed, typed relations it expresses — (head, relation, tail) triples such as (Abendwolken, created by, Gabriele Münter) or (the sky, has characteristic, luminous). The relations span both catalogue metadata (creator, genre, material, movement, date) and depicted content (objects, people, colours, postures, symbolism) — 12 relation types in all, several of them rare.
> For each test description, output every directed relation you can extract as a (head, relation, tail) triple. There are 12 relation types: has characteristic, depicts, contains, created by, instance of, symbolizes, influenced by, has genre, created in, made from material, fabrication method, has movement. You are not given the entities — you must find the head and tail text spans and the relation between them.
> Evaluation
> The final score is a weighted composite of three micro-averaged F1 terms. Score range: 0.0 (worst) to 1.0 (perfect); higher is better.
> Score = 0.60 * StrictRelationF1
> + 0.25 * UntypedPairF1
> + 0.15 * RareRelationF1
> How a match is decided. Each predicted relation is a triple (head, relation, tail) and is compared only against the gold relations of the same document (a prediction can never match a relation in a different document). Before comparison, head and tail are lowercased and whitespace-normalised (runs of spaces/newlines collapsed to single spaces, then trimmed); the relation type must match exactly (one of the 12 listed types); the triple is directed, so (A, r, B) and (B, r, A) are different. Within a document the gold relations and your predicted relations are each treated as a set (exact-duplicate triples are collapsed).
> How Precision, Recall and micro-F1 are computed. For each term, every prediction is labelled against the per-document gold set, then counts are pooled globally across all test documents (this is what "micro" means here):
> True Positive (TP) — a predicted triple that exactly matches a gold triple in its document.
> False Positive (FP) — a predicted triple with no matching gold triple in its document.
> False Negative (FN) — a gold triple that no prediction matched in its document.
> Then, over the pooled global counts: Precision = TP / (TP + FP), Recall = TP / (TP + FN), and micro-F1 = 2·TP / (2·TP + FP + FN) (equivalently the harmonic mean of the pooled Precision and Recall). If TP + FP + FN = 0 the term is defined as 0.0.
> The three terms differ only in what counts as a "triple" when forming the per-document sets:
> StrictRelationF1 (weight 0.60) — the dominant term. The triple key is the full (head, relation, tail). You must get the entity spans and the relation type right.
> UntypedPairF1 (weight 0.25) — the triple key is just (head, tail), ignoring the relation type. Partial credit for finding that two entities are related even if you label the relation wrong.
> RareRelationF1 (weight 0.15) — identical to StrictRelationF1 but computed only over relations whose type is one of the seven long-tail types (symbolizes, influenced by, has genre, created in, made from material, fabrication method, has movement); all other predictions and gold relations are excluded from this term. This stops a model from scoring only on the common has characteristic / depicts relations.
> Dataset
> The release contains four CSV files plus a metadata JSON. All text fields are UTF-8 strings; there are no missing values.
> **public/train.csv** — one row per training description. Columns:
> doc_id (string) — unique salted document identifier (e.g. ART_a1b2c3d4e5f6); the join key to train_relations.csv.
> text (string) — the full art-object description prose (the model input; may contain newlines).
> **public/train_relations.csv** — one row per gold relation in the training descriptions (a doc_id appears on as many rows as it has relations). Columns:
> doc_id (string) — document identifier; foreign key to train.csv.
> head (string) — surface text of the relation's head entity (e.g. Abendwolken).
> relation (categorical string) — one of the 12 relation types (e.g. created by).
> tail (string) — surface text of the relation's tail entity (e.g. Gabriele Münter).
> **public/test.csv** — one row per test description; relations withheld (same schema as train.csv). Columns:
> doc_id (string) — unique salted document identifier; use these values in your submission.
> text (string) — the art-object description prose to extract relations from.
> **public/sample_submission.csv** — a valid example submission with the exact required columns doc_id, head, relation, tail. It is an honest frequency-prior baseline (it predicts the 25 most frequent training relations on every test document) and scores ≈ 0.02 — a non-trivial floor to beat, not a real extraction.
> **public/metadata.json** — a JSON object documenting the task. Keys:
> task (string) — one-line task description.
> submission_columns (list of strings) — the four required submission column names.
> relation_types (list of strings) — the 12 valid relation-type values.
> composite_weights (object) — maps StrictRelationF1/UntypedPairF1/RareRelationF1 to their weights 0.60/0.25/0.15.
> matching (string) — the head/tail/relation matching rule.
> submission_note (string) — how submission rows are handled.
> Submission Format
> Submit a CSV at ./working/submission.csv with one row per predicted relation and exactly these columns:
> doc_id,head,relation,tail
> ART_a1b2c3d4e5f6,Abendwolken,created by,Gabriele Münter
> ART_a1b2c3d4e5f6,the sky,has characteristic,luminous
> ART_b2c3d4e5f6a1,the figure,depicts,a saint
> Requirements (strict — the grader rejects a violating submission rather than repairing it):
> Exactly the four columns doc_id, head, relation, tail — unexpected extra columns are rejected; no null values.
> Use doc_ids from test.csv. A document with no predicted relations simply has no rows; rows referencing doc_ids outside the graded test set are ignored.
> Duplicate identical triples within a document are collapsed (the metric is set-based).
> Approach Guidelines
> This is joint entity + relation extraction at the document level — a generative or span-based extractor (a fine-tuned encoder–decoder, or an LLM prompted to emit triples) is the natural approach. Getting the entity span text exactly right (head/tail) is as important as the relation type, since matching is on the normalised span.
> Mind the long tail. RareRelationF1 rewards the rare relation types; a model that only emits has characteristic / depicts caps out. Constrain decoding to the 12 valid relation types.
> Directionality matters — (artwork, created by, artist) is not (artist, created by, artwork).
> What Not To Use
> Matching the provided descriptions against any external text/image collection to recover the gold relations — by string search, embedding retrieval, or reverse lookup of the source catalogue. The document ids are salted; recovering the originating catalogue entry to read off structured metadata is prohibited.
> Any external art-catalogue knowledge base or annotated relation-extraction corpus used to train, fine-tune, or look up answers for these specific descriptions.
> Hardcoded {doc_id → relations} lookup tables.
> Training on the test descriptions in any form.

Inspiration note: Useful because it maps structured, noisy evidence into ordered or generated outputs with exact-format validation.

## Table Structure Gap Reconstruction
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx754d1ynsqyr331bee2ga6g3x89pg0q
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: multimodal, image, feature-engineering
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> This challenge uses real rendered scientific table images paired with table-structure token sequences. Each row shows a table image and an OTSL-style structural token sequence with multiple masked spans. The task is to reconstruct every missing structural span.
> The target is not cell text OCR. It is the table topology encoded by structural tokens such as filled cells, empty cells, span-continuation cells, header cells, and row boundaries. The harder rows mask several non-adjacent spans, often including rare structural tokens, so a solution must use the image, row/column dimensions, token context, and mask hints together.
> Dataset
> Images are stored under images/.
> Files:
> train.csv: Labeled rows with table-image references, masked structural-token context, mask hints, and answer_json.
> test.csv: Unlabeled rows with the same public fields as train.csv, without answer_json.
> sample_submission.csv: Example submission file with the required columns.
> images/: Rendered table images referenced by the CSV files.
> Columns:
> id (string): Unique row id.
> image (string): Relative path to the table image under images/.
> prompt (string): Task instruction.
> rows (integer): Table grid row count.
> cols (integer): Table grid column count.
> masked_otsl_json (JSON list): OTSL context tokens with placeholders such as <MASK_0>, <MASK_1>, and <MASK_2>.
> mask_hints_json (JSON list): Public mask hints. Each item gives a mask_id and the number of missing tokens for that mask.
> gap_count (integer): Number of masked spans in the row.
> total_gap_length (integer): Total number of missing tokens across all spans.
> vocabulary_json (JSON list): Valid OTSL tokens.
> answer_json (JSON object, train only): Ground-truth multi-span object.
> Submission Format
> Submit a CSV with columns id and answer_json in any order.
> answer_json must be a JSON object with exactly one key:
> spans (JSON list): Reconstructed spans. Each span object must contain:
> mask_id (string): Mask id such as <MASK_0>.
> start_index (integer): Start index of the missing span in the original unmasked token sequence.
> missing_tokens (JSON list of strings): Reconstructed token span.
> gap_length (integer): Number of submitted missing tokens.
> Example submission CSV:
> id,answer_json
> ptab_0a1b2c3d4e5f6a7b,"{""spans"":[{""mask_id"":""<MASK_0>"",""start_index"":18,""missing_tokens"":[""ched"",""fcel"",""nl"",""fcel""],""gap_length"":4},{""mask_id"":""<MASK_1>"",""start_index"":47,""missing_tokens"":[""lcel"",""fcel"",""ucel"",""fcel"",""nl""],""gap_length"":5}]}"
> ptab_9f8e7d6c5b4a3210,"{""spans"":[{""mask_id"":""<MASK_0>"",""start_index"":12,""missing_tokens"":[""srow"",""ched"",""ched"",""nl""],""gap_length"":4},{""mask_id"":""<MASK_1>"",""start_index"":39,""missing_tokens"":[""fcel"",""ecel"",""fcel"",""nl"",""lcel""],""gap_length"":5}]}"
> Evaluation
> Each row receives a score from 0 to 1:
> row_score = 0.48 * exact_object + 0.24 * exact_span_mean + 0.18 * token_position_accuracy_squared_mean + 0.04 * start_index_score_mean + 0.04 * gap_length_score_mean + 0.02 * mask_id_set_score
> Metric definitions:
> exact_object: 1 if all submitted spans exactly match the true spans after normalization, otherwise 0.
> exact_span_mean: Mean exact-match score over true mask ids. A span scores 1 only when its mask_id, start_index, missing_tokens, and gap_length all match.
> token_position_accuracy_squared_mean: For each true span, position-wise token accuracy between submitted and true missing_tokens, squared; then averaged over spans. Squaring is intentional because scattered partial token guesses should not dominate the score.
> start_index_score_mean: Mean of max(0, 1 - abs(submitted_start_index - true_start_index) / 12) over spans.
> gap_length_score_mean: Mean length score over spans. A span receives 1 when the submitted length is exact; otherwise it receives max(0, 1 - abs(submitted_gap_length - true_gap_length) / max(1, true_gap_length)).
> mask_id_set_score: 1 if the submitted mask-id set exactly matches the true mask-id set, otherwise 0.
> The final leaderboard score is the arithmetic mean of row_score across all test rows.
> What Not To Use
> Hardcoded mappings from row ids to answers.
> Manual lookup of ids or filenames outside the released public data.
> External copies of these exact rows with labels.
> Files or answer keys outside the released public data.

Inspiration note: Useful because it maps structured, noisy evidence into ordered or generated outputs with exact-format validation.

## Glycan Structure Assembly From Composition
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70996bt8as1mtr853qcyr2ms89p1j7
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Task
> A glycan is a branched tree of monosaccharides joined by glycosidic linkages (each with an anomeric configuration and a pair of attachment positions, e.g. a1-3, b1-4, a2-6). Its composition — how many of each monosaccharide it contains — is easy to obtain (e.g. by mass), but composition alone does not determine the structure: the same set of sugars can be wired into many different trees, and which one nature builds is set by biosynthetic enzymes whose linkage evidence is not in the composition. Across this data, most compositions correspond to several distinct structures.
> Your task is to assemble the structure from the composition: given the monosaccharide composition, the glycan class, and the coarse taxonomic domain, generate the full linkage-resolved glycan tree. This rewards learning the biosynthetic grammar — conserved cores, class-specific antennae, allowed linkages — and applying it to compositions the model has never seen. It is intrinsically bounded: because the composition underdetermines the linkages, exact assembly is impossible in general, so the achievable score has a hard ceiling well below the top of the scale.
> Why it is generation, not lookup. The test set is a held-out set of whole compositions (a private, salted split — not a nameable taxonomic group), so every test structure is absent from the training set, and every test composition is deliberately structurally ambiguous — it maps to several distinct known structures — so no test answer can be resolved to a single record; only a coarse context is given (composition + class + broad domain, never the finer taxonomy). The model must build the specific linkage-resolved isomer for a composition it has never seen, from the learned biosynthetic grammar. The provided sample_submission is only a format example (a single-monosaccharide placeholder that scores ≈0) — not a solution to build on. For reference, a no-learning nearest-composition copy (copying the closest known structure of the same class) captures the shared core but not the isomer-defining linkages and scores only ≈0.44 under the metric below; the scoring is built to credit the discriminating linkages, so generating them is where the skill and the headroom are.
> Data
> All files are under ./dataset/public/.
> File	Contents
> train.csv	id, composition, glycan_class, Domain, structure — labeled training glycans.
> test.csv	id, composition, glycan_class, Domain — the structure is withheld.
> sample_submission.csv	A correctly-formatted format example only (a single-monosaccharide placeholder; scores ≈0) — not a baseline to build on.
> Columns
> composition (string) — space-separated monosaccharide:count tokens, e.g. Hex:5 HexNAc:4 Neu5Ac:2. This is the set of building blocks; it does not fix the linkages.
> glycan_class (string) — the glycan type: N, O, lipid, free, repeat, …
> Domain (string) — coarse taxonomy (Eukarya / Bacteria); the finer taxonomy (kingdom, genus) is deliberately withheld.
> structure (string, train only) — the target: the IUPAC-condensed linkage-resolved glycan (e.g. Man(a1-3)[Man(a1-6)]Man(b1-4)GlcNAc(b1-4)GlcNAc).
> Submission
> Write ./working/submission.csv with exactly these two columns, in this order, one row per test id. For example:
> id,structure
> 6,[GlcA(b1-2)]Man(a1-3)Man(a1-3)[Xyl(b1-2)]Man(a1-3)Man
> 10,Glc(a1-6)Glc(a1-4)Glc(a1-6)Glc(a1-4)Glc
> 21,Gal(a1-3)Gal(b1-4)[Fuc(a1-3)]Glc-ol
> structure is your generated IUPAC-condensed glycan string (the values above are format illustrations, not answers). The grader rejects a submission with the wrong columns/order, a missing/extra/duplicate id, or far more rows than the test set. A malformed or unparseable structure is not rejected — it simply scores 0 for that row.
> Evaluation
> The score (higher is better, Maximize, in [0, 1]) is the mean linkage-bond F1 weighted toward the discriminating linkages. From each structure the grader extracts the multiset of (monosaccharide, linkage, monosaccharide) bonds (the two monosaccharides order-normalised) and compares your generated structure to the truth by a weighted F1, where each bond is weighted by its inverse frequency across the held-out structures so that the conserved-core bonds most glycans share carry little weight while the variable linkages that pick out the specific isomer and branch topology carry most of it.
> Let the held-out set contain N true structures. For a bond b, let df(b) be the number of held-out true structures that contain b, and let p[b] and t[b] be the counts of b in the predicted and true bond multisets of a given row. The per-row weighted F1 is:
> w(b)      = ln( (N + 1) / (df(b) + 0.5) )       # inverse-frequency weight: ~0 for ubiquitous bonds,
> # large for rare ones; = ln((N+1)/0.5) if b is in no true structure
> TP        = sum over b of  w(b) * min(p[b], t[b])
> P_tot     = sum over b of  w(b) * p[b]
> T_tot     = sum over b of  w(b) * t[b]
> precision = TP / P_tot
> recall    = TP / T_tot
> F1_row    = 2 * precision * recall / (precision + recall)
> score     = mean of F1_row over all test rows, clipped to [0, 1]
> F1_row = 1 when the predicted and true bond multisets are both empty, and F1_row = 0 when TP = 0 (including a missing prediction). Because the conserved core carries little weight, a no-learning nearest-composition copy scores only ≈0.44; recovering the variable linkages scores well above it (a generator that recovers most of them approaches ≈0.6 and beyond), while the composition's underdetermination of those linkages holds the achievable maximum well below 1.
> What to use
> Train a conditional generator over the glycan alphabet: a sequence-to-sequence transformer that emits the IUPAC string token by token, a graph-generation model, or an autoregressive decoder conditioned on the composition, class, and domain. Learning the biosynthetic grammar (cores, antennae, permissible linkages) and making it transfer to unfamiliar compositions is the productive path.
> What not to use
> No internet at inference and no external glycan structure databases or lookup services; train your model on the provided data (you may pip-install open-weight models and libraries at the start). The public context is deliberately coarse and cannot be matched to a unique source structure.
> No hardcoded per-id structures; submissions must be generated by your model.

Inspiration note: Useful because it maps structured inputs into ordered/generated outputs with strict format and partial-credit scoring.

## Transcode: Reconstructing a Hidden Sequence from Multiple Encoded Sources
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7agm6g8jwn90nk2cx56rbd7588fc82
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, small-data
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Each item is a single hidden underlying sequence that several independent sources have
> each recorded in their own way. Every source rewrites the underlying sequence through a
> fixed, hidden systematic substitution system — a source-specific set of rules that maps
> the underlying symbols to that source's symbols in a regular, context-sensitive fashion. You
> never observe the underlying sequence or any source's rules directly.
> For each item you are given three source encodings (sequences of abstract integer
> symbols) and the id of a fourth target source; your task is to output the sequence the
> target source would have produced for that same underlying item. The target source is chosen
> so that its encoding differs substantially from the three you are given, so copying is not
> enough — you must learn each source's systematic substitutions from many training items and
> combine the complementary evidence across the given sources, since different sources pin down
> different parts of the target.
> This is a sequence-to-sequence problem: variable-length symbol sequences in → a
> variable-length symbol sequence out. The per-source substitution systems are the hidden
> structure; they are never given and must be inferred by combining weak, partial evidence
> across many items and several source views. Symbols are an abstract integer alphabet and all
> source ids are opaque, so no external dictionary or pretrained prior transfers — everything
> must be learned from the provided training pairs. (The data is derived from real, anonymized
> symbolic records; see the dataset Source for provenance and license.)
> Anti-shortcut (balanced distractor). On exactly half of the items (balanced within each
> source group) one of the three given encodings is an intruder: a genuine encoding from
> that source, but of a different underlying item. You are not told which items contain an
> intruder, nor which of the three encodings it is. A method that trusts every source equally
> is misled; a robust method must detect the encoding that is inconsistent with the others and
> down-weight it.
> Intended approach. From the training items, learn each source's systematic
> symbol-to-symbol substitutions relative to the others; then, for a test item, fuse the three
> source encodings per position — discounting an inconsistent one — and decode the target
> source's sequence.
> Evaluation
> For each test item i, let p_i be your predicted symbol sequence and g_i the true
> target sequence. Let lev(p, g) be the token-level Levenshtein (edit) distance between two
> symbol sequences. Define the normalized edit distance
> NED_i = lev(p_i, g_i) / max(len(p_i), len(g_i), 1), so that NED_i ∈ [0, 1].
> The score combines a graded similarity term and a strict exact-match term:
> Similarity term: Sim = (1 / N) · Σ_i (1 − NED_i)
> Exact term: Exact = (1 / N) · Σ_i 1[ p_i = g_i ] (1 if the sequences are identical, else 0)
> Final score: Score = 100 · clip( 0.55 · Sim + 0.45 · Exact , 0 , 1 )
> where N is the number of test items and clip(x, 0, 1) bounds x to [0, 1].
> Maximum = 100: every predicted sequence is exactly correct NED_i = 0 and p_i = g_i for all i). A perfect submission scores exactly 100.
> Minimum = 0: every prediction is maximally wrong or empty NED_i = 1 for all i).
> Higher is better. Predictions are compared as sequences of whitespace-separated tokens;
> order matters and length matters.
> Measured reference scores (computed with the shipped grader on the test split):
> Empty / blank predictions: 0
> Constant guess — each target source's most frequent training sequence: ~9
> Nearest-neighbour retrieval (copy the training target of the most similar item): ~19 — below the copy baseline, confirming the split leaks nothing.
> Copy a single given encoding (naive): ~31
> Robust consensus (medoid) of the three given encodings: ~37
> Learned per-source substitution model with robust fusion (competent, intended baseline): ~43
> Strongest learned models reach a practical ceiling of about: ~50
> A perfect submission scores 100, but the underlying records contain irregular, item-specific
> exceptions that no method can recover, so the practical ceiling is around 50 — there is no
> achievable path into the 60s. The intended learned model reaches the low-to-mid 40s; the gap
> between copying a single encoding (~31) and a model that has genuinely learned the per-source
> substitutions (~43) is where the competition lives.
> Dataset
> All files are UTF-8 CSV with a header row.
> train.csv — 4486 rows, one per training item:
> sample_id — string — opaque unique item id.
> group — string — opaque source-group code; sources in the same group share a related substitution regime (their systematic mappings are comparable). Structure does not carry across groups.
> donor_langs — string — the ids of the three given source encodings, space-separated (e.g. L091 L078 L057). Source ids are consistent across the whole dataset.
> donor_forms — string — the three given encodings, separated by | , each a sequence of space-separated integer symbols, aligned by position to donor_langs (e.g. 302 20 123 | 5 9 31 | 5 40 2).
> query_lang — string — the id of the target source whose encoding you must reconstruct.
> target_form — string — the target source's encoding, space-separated integer symbols.
> test.csv — 1484 rows, identical columns to train.csv except target_form is
> omitted. Predict it.
> sample_submission.csv — 1484 rows — a valid submission skeleton with the correct columns
> and ids (its pred_form values are blank and score 0).
> Notes (not columns): the integer alphabet has 510 symbols; symbol identities are arbitrary (a
> private re-encoding); the half of items carrying an intruder encoding are balanced within
> each source group and are not flagged.
> Submission
> A CSV with a header and exactly these two columns, in this order:
> sample_id — string — must match the test ids exactly (every test id present, once).
> pred_form — string — your predicted encoding for the target source, as space-separated integer symbols (e.g. 5 40 2). May be empty, but an empty or invalid prediction is scored exactly like a fully wrong one (no abstain advantage).
> Exactly 1484 data rows. The grader rejects a submission that has missing, duplicate,
> unknown, or extra ids, the wrong row count, or columns other than sample_id,pred_form.
> Non-numeric, NaN, or out-of-range tokens are treated as wrong tokens for that row (they never
> crash the grader).
> Example of a correctly formatted submission (header plus the first few rows; the
> pred_form values shown are illustrative predicted sequences):
> sample_id,pred_form
> s44a0aa82610,436 376
> sd503717f12b,15 217 342 364
> sf1b273793bf,345 430 270
> Each row pairs a test sample_id with your predicted target sequence as space-separated
> integer symbols. The full file must contain exactly one row for every id in test.csv.
> What Not to Use
> Copying a single given encoding (first / longest / nearest): the target source differs substantially from the given ones, so copying scores ~31 and is actively degraded by the planted intruder encoding.
> A constant or per-source most-frequent guess:** ignores the input; scores ~9.
> Naive fusion that trusts all three encodings equally (plain averaging/voting): the balanced intruder punishes it; robust, outlier-aware fusion is required.
> Pretrained or external knowledge / dictionaries: symbols are an abstract re-encoding and source ids are opaque, so no external prior and no lookup of any source database transfers.
> Treating it as classification of whole sequences: outputs are open-ended sequences; novel target sequences appear at test time.
> What is expected: learn each source's systematic symbol substitutions from the training
> pairs, then fuse the three given encodings per position — different sources are reliable
> for different parts of the target — while down-weighting an inconsistent (intruder) encoding,
> and decode the target source's sequence.

Inspiration note: Useful because it maps structured inputs into ordered/generated outputs with strict format and partial-credit scoring.

## Protein Sequence Design for Liquid-Liquid Phase Separation
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dmm639awvqef6yden4z1wxn89rrqv
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: generative
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Liquid-liquid phase separation (LLPS) is a physical process where proteins spontaneously demix from solution to form membrane-less organelles — dynamic compartments that organize cellular biochemistry. These condensates are central to stress response, gene regulation, and synaptic signaling. When LLPS goes awry, it drives protein aggregation in ALS, frontotemporal dementia, and other neurodegenerative diseases.
> The Task
> Given a target specification — a desired critical concentration (Csat), condensate morphology, RNA-dependence, and a set of environmental conditions (pH, salt, temperature, crowding) — your model must generate a novel amino acid sequence that phase-separates with those exact properties under those exact conditions.
> This is the inverse design problem: instead of predicting what a given sequence does (the forward problem solved by existing benchmarks), you must create a sequence that does what you want. Success means your designed sequence, when evaluated, exhibits the target Csat, forms the target morphology, and shows the correct RNA-dependence — all under the specified conditions.
> Where the Data Comes From
> The training data is derived from the known biophysics of LLPS established over two decades of experimental research. Sequence determinants — sticker-spacer architecture, charge patterning, prion-like domains, RGG motifs — and their condition-dependent effects on phase behavior are well-characterized from in vitro experiments on thousands of proteins catalogued in databases such as LLPSDB and RNAPSEC. The data generation uses a computational model calibrated to these experimental observations, capturing the same physical principles that govern real LLPS: charge screening by salt, hydrophobic driving forces modulated by temperature, excluded volume effects from macromolecular crowding, and the sequence grammar that distinguishes functional liquid droplets from pathological fibrillar aggregates.
> The training data and the evaluation use two independently-calibrated models that agree on the underlying physics but differ in their detailed parameterization. This reflects the real-world challenge of training on one set of experimental measurements and predicting behavior under conditions measured by a different laboratory with different techniques.
> Dataset
> Training Data (train.csv)
> ~75,000 rows: 15,000 proteins x 5 environmental conditions each. This is forward mapping data — you receive sequences with their measured LLPS outcomes under specific conditions.
> Features (21 columns):
> protein_id (str) — Protein identifier, groups the 5 environmental conditions together
> env_condition_id (str) — Unique row identifier for each protein-condition pair
> sequence (str) — Amino acid sequence in single-letter code, 50–450 residues
> length (int) — Sequence length in residues
> pH (float) — Solution pH, range [4.0, 9.0]
> salt_concentration_mM (float) — Salt concentration in mM, range [0, 500]
> temperature_C (float) — Temperature in degrees Celsius, range [4, 45]
> crowding_agent (str) — Macromolecular crowder: PEG, Ficoll, Dextran, or none
> crowding_percent (float) — Crowder concentration in % w/v, range [0, 20]; 0 when agent is none
> fraction_disordered (float) — Fraction of disorder-promoting residues (D, E, K, R, S, P, Q, G, N, A)
> net_charge_at_pH (float) — Net charge computed via Henderson-Hasselbalch at the given pH
> hydropathy (float) — Mean Kyte-Doolittle hydropathy index
> sticker_count_YRWF (int) — Count of sticker residues under SimA definition: Y, R, W, F
> sticker_count_YFWH (int) — Count of sticker residues under SimB definition: Y, F, W, H
> prion_like_score (float) — Q/N/Y/G enrichment score, range [0, 1]
> rgg_motif_count (int) — Number of non-overlapping RGG and RG motifs
> kappa (float) — Charge patterning parameter, 0 = well-mixed charges, 1 = strongly segregated blocks
> aromatic_clustering (float) — Proximity of aromatic residues (Y, F, W), range [0, 1]
> block_ratio (float) — Ratio of longest same-charge block to average block length
> hydrophobic_moment (float) — Amphiphilicity measure from sliding-window hydropathy variance
> complexity (float) — Shannon entropy of 2-mer composition normalized to [0, 1]
> Targets (4 columns):
> phase_separates (int) — 1 if LLPS occurs under these conditions, 0 otherwise
> csat_uM (float) — Critical saturation concentration in micromolar; undefined for non-LLPS rows
> droplet_morphology (str) — Condensate type: liquid_droplet, gel_like, fibrillar_aggregate, or amorphous_aggregate; undefined for non-LLPS rows
> rna_dependent (float) — 1.0 if RNA promotes LLPS, 0.0 otherwise; undefined for non-LLPS rows
> Test Data (test.csv)
> 500 design target specifications — NO sequences provided. Each row is a desired LLPS behavior that you must design a sequence to achieve.
> target_id (str) — Target identifier, 0-indexed from target_0000 to target_0499
> difficulty (str) — Difficulty tier: easy, medium, or hard
> target_morphology (str) — Desired condensate morphology to achieve
> target_csat_uM (float) — Desired critical concentration in micromolar
> target_rna_dependent (int) — Desired RNA dependence: 0 or 1
> target_pH (float) — pH at which the design is evaluated
> target_salt_mM (float) — Salt concentration in mM at which the design is evaluated
> target_temp_C (float) — Temperature in degrees Celsius at which the design is evaluated
> target_crowding_agent (str) — Crowding agent: PEG, Ficoll, Dextran, or none
> target_crowding_percent (float) — Crowder concentration in % w/v
> Difficulty Tiers
> Easy — 200 targets. Moderate Csat, liquid droplet morphology, common conditions (pH 6–8, salt 50–300 mM, temp 20–37 °C)
> Medium — 200 targets. Wide Csat range, any morphology, broader condition ranges
> Hard — 100 targets. Extreme conditions, rare morphology combinations, edge cases (e.g., fibrillar aggregates at low temperature, liquid droplets at extreme pH, RNA-dependent gel at high salt)
> Evaluation
> Your submitted sequences are evaluated by SimB (a held-out physical model embedded in grade.py). SimB uses different features and functional forms than SimA (which generated the training data). Each sequence is simulated at the specified target conditions.
> Scoring Metrics
> Score = CsatProximity x (0.50 x MorphMatch + 0.20 x RNAAcc + 0.16 x SeqQuality + 0.14 x LengthEff)
> All metrics are multiplied by Csat Proximity. A sequence that misses the Csat target receives near-zero total credit regardless of other scores. Sequences that fail to phase-separate under target conditions score 0 for all metrics.
> 1. Csat Proximity (gate)
> Gaussian falloff in log-space, scaled by target-specific tolerance. Tolerance varies by difficulty: easy = 0.80, medium = 0.60, hard = 0.45 log10 units. A floor of 0.02 is applied to Csat proximity to prevent total zero-gating on near-misses.
> CsatProximity = exp( -0.5 x ( |log10(Csat_achieved) - log10(Csat_target)| / tolerance )^2 )
> Sequences that do not phase-separate under the target conditions score 0.
> 2. Morphology Match (x 0.50)
> Asymmetric penalty matrix — confusing a functional liquid droplet for a pathological fibril costs more than the reverse. Non-LLPS sequences score 0.
> Liquid droplet predicted correctly: 1.0. Predicted as gel: 0.6. Predicted as fibrillar: 0.1. Predicted as amorphous: 0.3.
> Gel predicted correctly: 1.0. Predicted as liquid: 0.7. Predicted as fibrillar: 0.3. Predicted as amorphous: 0.5.
> Fibrillar predicted correctly: 1.0. Predicted as liquid: 0.0. Predicted as gel: 0.4. Predicted as amorphous: 0.5.
> Amorphous predicted correctly: 1.0. Predicted as liquid: 0.4. Predicted as gel: 0.5. Predicted as fibrillar: 0.5.
> 3. RNA Dependence Accuracy (x 0.20)
> Binary accuracy: 1.0 if rna_dependent matches the target value, 0.0 otherwise.
> 4. Sequence Quality (x 0.16)
> Starts at 1.0 and deducts for non-protein-like patterns. Each penalty is applied independently; final score is clamped to [0, 1].
> Any single amino acid exceeds 35% of the sequence: deduct 0.15 x (freq - 0.35) / 0.65
> Any single amino acid exceeds 50%: deduct an additional 0.25
> Shannon entropy of 2-mer composition below 0.15: deduct 0.3
> Mean hydropathy outside [-2.5, 2.5]: deduct 0.2
> Fraction of disorder-promoting residues (D, E, K, R, S, P, Q, G, N, A) below 0.15: deduct 0.3
> 5. Length Efficiency (x 0.14)
> Piecewise-linear score based on sequence length, clamped to [0, 1]. Shorter sequences that achieve the target specification score higher.
> L up to 100 AA: 1.00
> L = 101–200 AA: 0.95
> L = 201–300 AA: 0.90
> L = 301–400 AA: 0.85
> L over 400 AA: 0.85 - 0.05 x (L - 400) / 200
> Difficulty Weighting
> Target scores are weighted by difficulty in the composite average:
> Easy: x0.8
> Medium: x1.0
> Hard: x1.3
> Hard targets contribute more to your final score.
> Baselines
> Random 150-AA diverse sequence (500 different sequences): 0.08
> Copy training protein with best-matching Csat, morphology, and RNA profile: 0.16
> Submission
> Submit a CSV with the following columns:
> target_id (str) — Must match test.csv exactly, in the same order
> sequence (str) — Your designed amino acid sequence (single-letter code, 50–600 AA)
> Example (IDs are 0-indexed, matching test.csv):
> target_id,sequence
> target_0000,MYGGRGGYNNQSSYGAPQ...
> target_0001,MFRGGYNNQSSYGGPQQSY...
> target_0002,MKLRGGWGGSYNQQQGSYQ...
> Requirements:
> Exactly 500 rows (one per target in test.csv)
> All 20 standard amino acids allowed: A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y
> Sequence length: 50–600 residues
> No homopolymers, no simple repeats, no whitespace, uppercase only
> A sample_submission.csv with a placeholder sequence is provided
> Rules
> Allowed
> Any generative approach: diffusion models, autoregressive LMs, GANs, VAEs, evolutionary algorithms, Bayesian optimization, reinforcement learning, combinatorial search, or any hybrid strategy
> Pretrained protein language models (ESM-2, ProtBERT, ProtT5, Ankh, ProGen2, EvoDiff, ProteinMPNN, etc.)
> Training a forward predictor on train.csv to guide generation
> Any strategy for conditioning generation on target specifications
> Sequence optimization via gradients, MCMC, simulated annealing, genetic algorithms, or any search method
> External data from public protein databases (UniProt, UniRef, Pfam) or LLPS literature — must be disclosed
> Ensembles of up to 5 distinct models
> PyTorch, TensorFlow, JAX, or any deep learning framework
> Not Allowed
> Copying exact training protein sequences — generated sequences must be novel
> Reverse-engineering or probing grade.py to recover SimB parameters
> Using 3D structure prediction (AlphaFold, ESMFold, RosettaFold) during inference; offline analysis is permitted
> Closed-source LLM APIs (GPT-4, Claude, Gemini, etc.) during inference
> Manual design — all 500 targets must be generated by your automated system

Inspiration note: Useful because it maps rich inputs into ordered/generated outputs with exact formatting and task-specific validation.

## Biomedical Evidence Aggregation for Disease Risk Factor Profiling
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ej9hf3vc43wk8hwe3ttqydx89cpfc
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> For any given disease, the biomedical literature scatters its lifestyle determinants across many separate abstracts: one paper reports that a factor raises risk, another that a different factor is protective, a third that an apparent link is actually null. Consolidating that scattered evidence into a single, signed risk-factor profile for the disease is a core step in evidence synthesis — and it is exactly what this challenge automates.
> You are given a disease together with a dossier of biomedical abstracts that mention it. Your model must read the whole dossier and emit the disease's consolidated lifestyle-factor profile: the set of (lifestyle_factor, polarity) edges, where each polarity says how that factor relates to the disease. This is an evidence-aggregation task, not a per-sentence or per-abstract extraction task — a factor's polarity must be decided from the dossier as a whole, and a single disease's profile is assembled from up to ~30 abstracts.
> Task
> For each test disease, output its profile as a set of (lifestyle_factor, polarity) edges. There are 4 polarity classes, describing the factor's established relationship to the disease across the dossier:
> RISK — the factor increases the disease's risk / is a positive determinant (e.g. smoking → lung cancer).
> PROTECTIVE — the factor lowers risk, prevents, treats, or controls the disease (e.g. physical activity → depression).
> ASSOCIATED — a significant statistical association is reported, but the direction is not established.
> NEUTRAL — the literature reports no significant association between the factor and the disease.
> You must recover the lifestyle-factor text and assign the correct polarity. The dossier may mention several diseases; only factors tied to the target disease belong in its profile.
> Evaluation
> The score is a weighted composite of three micro-averaged F1 terms. Score range: 0.0 (worst) to 1.0 (perfect); higher is better.
> Score = 0.55 * StrictProfileF1
> + 0.30 * MacroPolarityF1
> + 0.15 * UntypedFactorF1
> How a match is decided. Each predicted edge is a pair (lifestyle_factor, polarity) and is compared only against the gold edges of the same disease. Before comparison lifestyle_factor is lowercased and whitespace-normalised (runs of whitespace collapsed, then trimmed); polarity must match exactly (one of RISK, PROTECTIVE, ASSOCIATED, NEUTRAL). Each disease's gold edges and your predicted edges are treated as sets (duplicate edges collapse).
> How Precision, Recall and micro-F1 are computed. For each term, every predicted edge is labelled against the per-disease gold set, then counts are pooled globally across all test diseases:
> True Positive (TP) — a predicted edge that matches a gold edge of the same disease.
> False Positive (FP) — a predicted edge with no matching gold edge of that disease.
> False Negative (FN) — a gold edge that no prediction matched for that disease.
> Then Precision = TP / (TP + FP), Recall = TP / (TP + FN), and micro-F1 = 2·TP / (2·TP + FP + FN). If TP + FP + FN = 0 the term is 0.0.
> The three terms:
> StrictProfileF1 (0.55) — dominant. Micro-F1 with the edge key (lifestyle_factor, polarity): both the factor text and its polarity must be right.
> MacroPolarityF1 (0.30) — computed per polarity (restrict gold and predictions to one polarity, take that polarity's micro-F1) and averaged equally over the 4 polarities. The infrequent polarities (NEUTRAL, ASSOCIATED) count as much as RISK / PROTECTIVE, so you cannot ignore them.
> UntypedFactorF1 (0.15) — micro-F1 with the key (lifestyle_factor) alone, ignoring polarity. Partial credit for finding the right factor even if you mis-sign it.
> Dataset
> The release contains three CSV files plus a metadata JSON. All text fields are UTF-8 strings; there are no missing values.
> **public/train.csv** — one row per training disease (the unit of the task). Columns:
> disease_id (string) — unique salted disease identifier (e.g. DRP_a1b2c3d4e5f6); the join key to train_profile.csv.
> disease_name (string) — the disease's surface name (e.g. obesity).
> n_abstracts (integer) — number of abstracts in this disease's dossier.
> dossier (string) — the concatenated abstract texts for this disease, separated by the literal delimiter \n\n===== ABSTRACT BREAK =====\n\n. This is the model input.
> **public/train_profile.csv** — one row per gold edge of the training diseases. Columns:
> disease_id (string) — disease identifier; foreign key to train.csv.
> lifestyle_factor (string) — surface text of the lifestyle factor (e.g. cigarette smoking).
> polarity (categorical string) — one of RISK, PROTECTIVE, ASSOCIATED, NEUTRAL.
> **public/test.csv** — one row per test disease; profiles withheld (same schema as train.csv: disease_id, disease_name, n_abstracts, dossier).
> **public/sample_submission.csv** — a valid example submission with the exact required columns disease_id, lifestyle_factor, polarity. It is an honest frequency-prior baseline (it predicts the 20 most frequent training edges on every test disease) and scores ≈ 0.04 — a non-trivial floor to beat, not a real profile.
> **public/metadata.json** — a JSON object documenting the task. Keys: task (string), submission_columns (list of the three required column names), polarities (list of the 4 polarity values), composite_weights (object mapping StrictProfileF1/MacroPolarityF1/UntypedFactorF1 to 0.55/0.30/0.15), matching (string), and submission_note (string).
> Submission Format
> Submit a CSV at ./working/submission.csv with one row per predicted edge and exactly these columns:
> disease_id,lifestyle_factor,polarity
> DRP_a1b2c3d4e5f6,cigarette smoking,RISK
> DRP_a1b2c3d4e5f6,physical activity,PROTECTIVE
> DRP_b2c3d4e5f6a1,coffee consumption,NEUTRAL
> Requirements (strict — the grader rejects a violating submission rather than repairing it):
> Exactly the three columns disease_id, lifestyle_factor, polarity; no extra columns; no null values.
> polarity must be one of RISK, PROTECTIVE, ASSOCIATED, NEUTRAL (other values never match). Save the CSV UTF-8.
> Use disease_ids from test.csv. A disease with no predicted edges has no rows; rows for disease_ids outside the graded test set are ignored.
> Approach Guidelines
> This is literature-level evidence aggregation: read the whole dossier for a disease and decide each factor's net polarity, resolving complementary or conflicting reports. A retrieval/extraction model followed by per-factor polarity aggregation, or an LLM prompted to emit the consolidated profile, are natural approaches.
> Get the factor span right. Matching is on the normalised lifestyle_factor text; boundary variants (physical activity vs regular physical activity) do not match, and this is the dominant source of difficulty.
> Sign every factor, including the unglamorous classes. MacroPolarityF1 makes NEUTRAL (no-association) and ASSOCIATED (undirected) worth as much as RISK/PROTECTIVE.
> Attribute to the right disease. A dossier can mention more than one disease; factors for other diseases are distractors.
> What Not To Use
> Matching the dossiers against any external corpus (PubMed, an annotated relation/association dataset, a knowledge base) to recover the gold profile by id, string search, or embedding retrieval. Disease ids are salted so the source records are not named by id, but the abstract text is shipped verbatim — do not search for or retrieve the originating publications or their annotations to recover the gold edges; aggregate the profile only from the dossier you are given.
> Any external annotated lifestyle/disease association corpus used to train, fine-tune, or look up answers for these specific diseases.
> Hardcoded {disease_id → profile} tables, or training on the test diseases in any form.

Inspiration note: Useful because it maps rich inputs into ordered/generated outputs with exact formatting and task-specific validation.

## Story Packet Evidence Trace Restoration
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fgas5q66tvetb65fvzzdww189vywh
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, generative
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Each row contains a lossy story packet: a compressed narrative memory made from a title-free story summary, a few structural hints, and a probe asking about one event, motivation, relationship, or outcome. The original answer trace has been removed. Your task is to restore that trace as a compact JSON object with two parts:
> answer: the short phrase that resolves the probe.
> support_phrase: the focused phrase from the packet that shows why the answer is justified.
> This is not an answer-only reading task over full original narratives. The packet is deliberately compressed and anonymized, and the target is a paired answer-and-evidence trace. Strong submissions must identify the specific narrative moment being queried, avoid nearby distractor events, and return a support phrase that is narrow enough to audit the answer.
> Dataset
> The prepared challenge files contain 2,592 labeled training rows and 1,008 evaluation rows. The split is grouped by underlying story before anonymization, so evaluation story packets are not reused in training.
> Files:
> train.csv: Labeled examples with public input fields and answer_json.
> test.csv: Evaluation examples with the same public input fields but without answers.
> sample_submission.csv: A valid low-information submission with all evaluation ids.
> Columns:
> id (string): Opaque task id.
> story_uid (string): Anonymized story grouping key.
> context_bundle (string): Story packet containing compressed narrative context, structural hints, and task framing.
> question (string): Probe to resolve from the story packet.
> answer_json (JSON object string, train only): Reference answer trace.
> The expected answer object has exactly:
> answer (string): Brief answer phrase, at most 260 characters.
> support_phrase (string): Focused support phrase, at most 700 characters.
> Submission Format
> Submit a CSV with exactly these columns, in any order:
> id
> answer_json
> Each answer_json value must be a JSON object with exactly answer and support_phrase. Both fields must be non-empty strings. Extra keys, malformed JSON, duplicate ids, missing ids, extra ids, extra columns, and values outside the field limits are rejected before scoring.
> Example submission:
> id,answer_json
> nqa_lcar_0026ef96823e,"{""answer"":""by disabling the device mechanism"",""support_phrase"":""locates the cobalt bombs and disables the transmission mechanism""}"
> nqa_lcar_0051f359f000,"{""answer"":""the missing family member"",""support_phrase"":""the family searches for the missing relative""}"
> nqa_lcar_00701c2b38b3,"{""answer"":""because the plan failed"",""support_phrase"":""the plan fails and the group changes course""}"
> Evaluation
> Scores are bounded from 0 to 1, with higher better.
> For each row:
> row_score = 0.70 * answer_token_f1 + 0.30 * support_phrase_token_f1
> Definitions:
> answer_token_f1 is standard token F1 between submitted answer and the reference answer.
> support_phrase_token_f1 is standard token F1 between submitted support_phrase and the reference support phrase.
> For each F1 term, precision is overlapping token count divided by submitted token count, recall is overlapping token count divided by reference token count, and F1 is 2 * precision * recall / (precision + recall).
> The final leaderboard score is the arithmetic mean of row scores across all evaluation rows. A perfect private-answer submission scores exactly 1.0.
> What Not To Use
> Hardcoded mappings from task ids to answers.
> Lookup of original narratives, story titles, hidden grouping ids, or exact upstream examples.
> Non-public files, answer files, row order, or package-generation internals.
> External copies of the exact generated evaluation rows.

Inspiration note: Useful because it maps rich inputs into ordered/generated outputs with exact formatting and task-specific validation.

## Avian Abundance Sequence Completion
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72zzbftsskr666vhywn75xbx89xb5z
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Each example is an abundance sequence of a wild bird population — the number of
> individuals of one species recorded at one long-running monitoring site over successive
> annual surveys. Tracking how such populations rise, fall and fluctuate is central to
> wildlife monitoring and conservation: it is how declines, recoveries and shifting ranges
> are detected. This challenge frames that as a sequence-to-sequence problem: given the
> earlier part of a population's abundance sequence (the input), reconstruct the held-out
> final block of the sequence (the output) — a map from an input sequence to an output
> sequence, learned across thousands of populations.
> Concretely, each sequence is split into two parts:
> an input part — the surveys you are shown, and
> an output part — the final H = 5 values, held out, that your model must reproduce.
> Your model is an encoder–decoder / sequence-to-sequence map: it reads the input part and
> produces the H output values. The sequences are anonymised and standardised — each is
> identified only by an opaque ID (s#####) and a position index t, with no species, site or
> year labels, and its values are z-scored (each sequence centred and scaled by the
> statistics of its own input part). What remains is the shape of the population's dynamics
> — its level shifts, its survey-to-survey variability, its tendency to revert or to drift.
> Your model must map the input part to the output part from that shape alone.
> The signal is cross-population: a model trained across many species-site sequences learns
> the shared dynamics of how bird populations evolve (a recent trend tends to carry over a
> little; sharp excursions tend to pull back; noisy populations stay noisy) that let it
> reconstruct the held-out block better than simply repeating the last observed value. That
> last-value baseline is the reference to beat.
> (Only genuine surveys enter a sequence: a year in which a site was not surveyed — e.g. a
> cancelled survey season — is omitted rather than recorded as a zero, so the sequences carry
> real population dynamics, not survey-effort artefacts.)
> Data
> train.csv                 # series_id, t, value            (complete sequences, input + output)
> test.csv                  # series_id, t, value, row_id    (input elements + the positions to produce)
> sample_submission.csv     # row_id, score                  (a deterministic-random baseline)
> This is a tabular sequence dataset — everything is in the CSVs.
> Size: 12,000 sequences (8,400 train / 3,600 test); each has at least 30
> elements, of which the last H = 5 form the output block (18,000 output values to
> produce in all).
> **train.csv** — complete sequences for training (both the input and output parts are
> given, so you can learn the input→output map):
> series_id — string; anonymised sequence ID.
> t — integer; position within the sequence (0, 1, 2, …).
> value — float; the standardised value at position t.
> **test.csv** — one file holding, for every test sequence, both its input rows and its
> output rows. Columns series_id, t, value, row_id:
> input rows — value is filled in (the element you are given) and row_id is
> empty;
> output rows — value is empty (this is what you produce) and row_id is
> set (the identifier you submit a prediction for). So each test sequence appears as several input rows (with values, no row_id) followed by
> exactly H output rows (no value, with row_id).
> **sample_submission.csv** — row_id, score for exactly the output rows, pre-filled with
> a deterministic-random placeholder (draw your own model's outputs to replace it). Edit
> the score column.
> baseline. For each test sequence let f be your H-element output, y the true
> output, and b the baseline output (the sequence's final input element, repeated).
> "Global" sums run over every (sequence, position); "per-sequence" quantities are averaged
> over sequences.
> Constants: W_T = 0.035, POWER = 0.50, SCALE = 1.10, LAM = 0.30, BASE = 0.40,
> SCALE_V = 0.60, SCALE_T = 0.40, SCALE_B = 0.40.
> Step 1 — the point-accuracy gate (skill over the baseline). Two scaled-error skills,
> each 1 for a perfect output and 0 for one no better than the baseline b:
> S_ABS = clip( 1 −  ( Σ|f − y| ) / ( Σ|b − y| ) ,               0, 1 )      # scaled absolute-error skill
> S_SQ  = clip( 1 −  sqrt( Σ(f − y)² / Σ(b − y)² ) ,             0, 1 )      # scaled squared-error skill
> point = 0.5·S_ABS + 0.5·S_SQ
> point multiplies everything below, so an output no better than the baseline at hitting
> the values — including random noise, which is worse than the baseline — scores ~0 however
> well it mimics the sequence's wiggle.
> Step 2 — six quality modulators. Absolute measures in [0, 1], each equal to 1 for a
> perfect output, rewarding getting the shape of the output block (not just its level)
> right:
> S_CORR  = mean over sequences of  clip( pearson(f, y), 0, 1 )                # output shape
> S_DIR   = mean over positions of  [ sign(f − b) == sign(y − b) ]           # direction relative to b
> S_PEAK  = mean over sequences of  [ argmax(f) == argmax(y) ]               # position of the largest element
> S_VOL   = mean over sequences of  exp( −|std(f) − std(y)| / SCALE_V )       # element-to-element spread
> S_TREND = mean over sequences of  exp( −|slope(f) − slope(y)| / SCALE_T )   # net slope across the block
> S_BIAS  = exp( −| mean(f − y) | / SCALE_B )                                 # freedom from a constant offset
> where slope(·) is the least-squares slope of the H output values against their position
> index. These are grouped and blended (arithmetic mean for robustness, geometric mean to
> reward being good on all axes at once):
> shape = (S_CORR + S_DIR + S_PEAK) / 3
> dyn   = (S_VOL + S_TREND) / 2
> calib = S_BIAS
> aux_a = 0.50·shape + 0.30·dyn + 0.20·calib
> aux_g = ( max(shape, 1e−6) · max(dyn, 1e−6) · max(calib, 1e−6) ) ^ (1/3)
> aux   = (1 − LAM)·aux_a + LAM·aux_g
> Step 3 — combine, floor, shape. The quality modulates the gated skill; a small
> transcendental tolerance term keeps a trivial submission strictly positive; the shaping
> exponent expands the (intrinsically compressed) skill range:
> comp  = point · ( BASE + (1 − BASE)·aux )
> TOL   = mean over all (sequence, position) of  exp( −|f − y| / SCALE )
> score = clip( (1 − W_T)·comp^POWER  +  W_T·TOL ,  0,  1 )
> A perfect output → point = 1 and every modulator = 1 → comp = 1, TOL = 1 →
> 1.0. Any output no better than the last-value baseline at hitting the level (the
> random sample, or a reversed output) → point = 0 → comp = 0, leaving only the small
> W_T·TOL. Beating the baseline on point accuracy and matching the output block's shape,
> direction, spread, slope, offset and peak position is what earns score. The output block is
> short and the sequences are noisy, so a strong model stays well under 0.5.
> Verified behaviour (real test set, ~18,000 output values / ~3,600 sequences):
> Exact output → 1.000.
> Sample submission (the deterministic-random placeholder) → ≈ 0.015; a reversed output →
> ≈ 0.013; the last-value baseline itself → ≈ 0.018 (all trivial, no floor).
> Emitting each sequence's input-part mean (a non-learned shortcut) → ≈ 0.05.
> A learned sequence-to-sequence model (gradient boosting / an ensemble / an encoder–decoder
> over the training pairs) → ≈ 0.30–0.35; reaching much higher requires resolving
> survey-to-survey moves the standardised input does not determine.
> Reproducing the score locally. The metric is a pure function of your output versus the
> truth (the baseline is just each sequence's final input element). Hold out the last 5
> elements of each train.csv sequence and apply the same formula; the score rises
> monotonically as your output approaches the true output.
> Submission Format
> Submit a CSV with exactly these columns — row_id, score — and one row per row_id in
> test.csv (the provided sample_submission.csv already has this format — edit its score
> values):
> row_id — string; the output-row identifier from test.csv (must match exactly).
> score — a finite real number; your predicted standardised value at that
> (sequence, position).
> Example (same columns as sample_submission.csv):
> row_id,score
> bf_0a91c3d27e5b40,0.41
> bf_1c8d40b9a3e2f7,-0.85
> bf_2e5a7c6b1d0f93,0.12
> Requirements (a submission that violates any of these is rejected):
> Columns row_id, score present (and only these two); the row_id set must match the
> output rows of test.csv exactly (no missing, extra or duplicate ids).
> Every score is a finite number.
> Include the header row.
> What Not To Use
> Solvers must solve this with machine learning (a trained sequence-to-sequence model).
> The predicted output values must come from a model fitted on the provided training pairs
> and reading each test sequence's input part. Submissions that reach the answer by non-ML
> means will be rejected.
> Not allowed
> Non-ML / "raw logic" solutions. No hand-written rules or fixed formulas that map an
> input sequence to an output. In particular, submitting the last-element baseline
> (repeat the input's final element across the output), a constant, the input mean, or
> any value that is not produced by a trained model is a non-ML shortcut and is prohibited —
> the last-element baseline is exactly the reference the metric measures the skill over,
> and beating it requires learning the input→output mapping.
> De-anonymising the sequences / external lookup. The sequence IDs are opaque and the
> values are standardised (z-scored), with every external label removed. Do not attempt
> to re-identify what a sequence corresponds to (from its shape, its values, or any side
> information) in order to retrieve the hidden output from an outside dataset, database,
> repository, API or search engine. The task is to produce the output from the provided
> input, not to look the answer up.
> Matching a sequence back to a source. Do not fingerprint, de-standardise, or align the
> provided sequences against any external collection to recover the output values.
> Hard-coding or memorising the answer. Do not embed a table of output values or
> per-row predictions looked up offline. Every score must be produced by the model from
> the sequence's input part at inference time.
> External label sources keyed to these specific sequences.
> Allowed
> Any genuinely learned sequence-to-sequence model — a global model trained across the
> provided training pairs (gradient boosting / random forest on lag & summary features, a
> linear / state-space model, an RNN / temporal-CNN / transformer encoder–decoder), a
> per-sequence model, or an ensemble — fitted on train.csv and reading each test sequence's
> input part.
> Standard sequence-modelling / ML tooling: feature engineering from the input part (lags,
> differences, slope, spread, periodicity), smoothing, decomposition, regularisation,
> probabilistic outputs, and ensembling.
> General world knowledge about how sequence modelling works (that a recent level shift
> and mean-reversion carry information, that these values evolve multiplicatively, etc)
> applied to the provided sequences. This is method knowledge, not answer lookup.
> The rule of thumb: the values you submit must come from a trained sequence-to-sequence model
> that infers each sequence's output from its input — not from a constant, the last-element
> baseline, de-anonymising the sequences, or retrieving the answer from an outside source.

Inspiration note: Useful because it maps rich inputs into ordered/generated outputs with exact formatting and task-specific validation.

## Recovering Hidden Phrases in Bird-Song Syntax
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx789e2yn66jhqe7shm7jagvz989yq7v
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> The sequences in this challenge are the songs of a songbird. When a bird sings, it strings together discrete phrase types from its learned repertoire into long song bouts — and the order is not random: birdsong has a real syntax, a grammar of which phrase tends to follow which. But that grammar is not a formal language and not like human text: at many points the bird makes a genuine stochastic choice among several continuations (a branch point), the grammar varies from individual to individual (each bird has its own idiosyncratic syntax), and the dependencies are non-Markovian — properties that separate animal vocal syntax from the synthetic / formal-language sequences and human-language token streams that usual next-symbol predictors are built for.
> Your task: model this vocal syntax from the songs and recover a hidden phrase from its surrounding context. Because the singer genuinely branches, exact recovery has an irreducible ceiling: a majority-phrase baseline scores only ~0.05, a first-order (bigram) model ~0.27, and even a strong from-scratch sequence model only ~0.53 — no model reaches 1.0, because a share of positions are real biological choice, not a deterministic pattern waiting to be cracked.
> Each phrase type is encoded as an opaque symbol (S000…) rather than its acoustic label, so the challenge is purely about learning the sequential syntax from the data — no external birdsong model, phrase inventory, or recording can help.
> Data
> train.json — full song bouts to learn the syntax from: [{"seq_id": ..., "symbols": ["S037", "S004", ...]}, ...]. Each list is one bird's song bout as an ordered sequence of phrase-type symbols. This is your only training data.
> test.json — test items: [{"item_id": ..., "context": ["S012", "MASK", "S088", ...]}, ...]. Each context is the run of phrases immediately preceding a hidden phrase — the left context only (what comes after is not given). Predict the single phrase at the hidden position (i.e. the next phrase after the context). A "MASK" marks another hidden position and carries no information.
> sample_submission.csv — a valid submission with a dummy baseline.
> Task
> For each item_id in test.json, predict the next phrase (symbol) given its left context.
> Evaluation
> Top-1 accuracy: the fraction of test items whose predicted phrase exactly matches the held-out phrase. Higher is better, in [0, 1].
> Submission format
> A CSV with exactly two columns:
> item_id,symbol
> IT_ade4e7d4c26e,S037
> IT_0b3d824bc723,S112
> item_id — every item_id from test.json, each exactly once.
> symbol — your predicted phrase symbol (a single token, e.g. S037).
> Requirements (violations are rejected as invalid submissions): exactly the columns item_id,symbol; no nulls; no missing, duplicate, or extra item_id.
> Allowed
> Training a sequence model from scratch on the provided song bouts: an n-gram / variable-order Markov model, an RNN/LSTM/GRU, a transformer, or any count-based or neural model of the phrase-transition syntax.
> Any feature of the left context (recent phrases, positional patterns, phrase frequencies, per-bout adaptation). Treat "MASK" as an unknown placeholder.
> Prohibited
> No external data or pretrained models — the phrase symbols are relabelled and specific to this collection, so only the provided song bouts are informative. Do not attempt to reverse the symbol relabelling, identify the source recordings, or use an external birdsong / bioacoustic model.
> No use of any answer/label file; predictions must come from your model.

Inspiration note: Useful because it maps rich inputs into ordered/generated outputs with exact formatting and task-specific validation.

## Chess Move-Prefix Outcome Distribution Prediction
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78k17efgs9yn7t07m77a7yrn89wc46
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, Based on dataset:, Lichess Standard Rated Chess PGN Archives January-March 2013, Download Data
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> You are given early-to-midgame chess move prefixes as SAN token strings. Each row represents a real aggregate cohort of games that share the visible prefix pattern, not a single game. This is an NLP-style symbolic sequence modeling task: map a SAN token sequence to a calibrated three-class outcome distribution for the hidden cohort: white win, draw, and black win.
> The public rows contain only an opaque id, the SAN move_prefix, prefix_ply_count, and side_to_move. They do not contain player names, game IDs, dates, source filenames, ratings, event/site/round tags, ECO/opening names, termination, result tags, raw order, or full continuations. Training rows include empirical outcome rates for aggregate cohorts; test rows hide those rates in private/answers.csv.
> What to use: fine-tune a compact text/sequence encoder on the public rows, train a SAN-token model from scratch, build n-gram or transformer-style language features, fit calibrated probabilistic classifiers/regressors, and validate calibration on the public training labels. What not to use: external PGN lookup, engine evaluation, best-move solving, source archive reconstruction, row-order side channels, or grader exploitation. The intended challenge is sequence-to-distribution learning from the visible prefix only.
> Evaluation
> Submissions provide four values per test row: three class probabilities and a confidence score. The grader first validates the exact schema and ID set. Structural CSV errors return 0.0; malformed row-local prediction values give only that row zero contribution rather than crashing or zeroing the whole file.
> For valid submissions, the grader computes a composite probability skill score:
> S_brier = clip(1 - mean_valid_rows(sum((p - y)^2)) / BRIER_REF, 0, 1)
> S_log   = clip(1 - mean_valid_rows(CE(y, p) - CE(y, y)) / LOG_REF, 0, 1)
> S_conf  = clip(1 - mean_valid_rows(abs(confidence - max(y))) / CONF_REF, 0, 1)
> S_worst = lowest hidden-group Brier skill, with malformed rows counted as zero rows in their group
> Composite = 0.55*S_brier + 0.20*S_log + 0.10*S_conf + 0.15*S_worst
> Final = valid_row_fraction * (0.12 + 0.88*Composite)
> y is the hidden empirical outcome distribution. p is the submitted distribution after row-wise normalization. BRIER_REF, LOG_REF, and CONF_REF are fixed constants derived from the prepared training split, not hidden test marginals. The valid-row fraction makes malformed rows contribute zero while preserving smooth scoring for the remaining rows. Structurally invalid submissions still score exactly 0.0. A perfect submission that predicts the hidden distribution and sets confidence to the largest hidden class probability scores exactly 1.0.
> Higher is better. Theoretical minimum: 0.0. Theoretical maximum: 1.0.
> Dataset
> Participants receive public/train.csv, public/test.csv, and public/sample_submission.csv. public/train.csv contains one row per labeled aggregate prefix cohort, including the empirical target rates and the hidden cohort size for training only. public/test.csv contains the same visible prefix fields without target rates or cohort size. public/sample_submission.csv is a valid weak template based on public training priors.
> The visible test input columns are id, move_prefix, prefix_ply_count, and side_to_move. The train-only label columns are white_win_rate, draw_rate, black_win_rate, and cohort_game_count; the three rate columns are the empirical cohort target distribution.
> File overview
> Item	Description
> public/train.csv	Labeled prefix cohorts
> public/test.csv	Unlabeled prefix cohorts
> public/sample_submission.csv	Valid weak template
> private/answers.csv	Hidden target rates
> Train columns
> Column	Type	Description
> id	int	Opaque row id
> move_prefix	string	SAN tokens
> prefix_ply_count	int	Prefix length
> side_to_move	string	Next side
> white_win_rate	float	Cohort white-win rate
> draw_rate	float	Cohort draw rate
> black_win_rate	float	Cohort black-win rate
> cohort_game_count	int	Train cohort size
> The three rate columns are nonnegative and sum to 1. cohort_game_count is shown only for training rows so solvers can learn how empirical cohort size relates to calibration.
> Test columns
> Column	Type	Description
> id	int	Opaque row id
> move_prefix	string	SAN tokens
> prefix_ply_count	int	Prefix length
> side_to_move	string	Next side
> Test rows hide all target rates, cohort sizes, source identifiers, and continuations. id and row order are salted and shuffled; they carry no source-order or split signal.
> Submission format
> Column	Type	Constraint
> id	int	Match test ids
> white_win_prob	float	[0, 1]
> draw_prob	float	[0, 1]
> black_win_prob	float	[0, 1]
> confidence	float	[0, 1]
> The three probability columns should be finite floats in [0, 1]; valid nonzero rows are normalized before scoring. A row with malformed, non-finite, out-of-range, or all-zero probability values receives zero row-level contribution for that row only. confidence should be finite and in [0, 1]; malformed, non-finite, or out-of-range confidence also makes only that row contribute zero.
> Submission
> Submit a CSV with exactly these columns in this order: id, white_win_prob, draw_prob, black_win_prob, confidence.
> Example:
> id,white_win_prob,draw_prob,black_win_prob,confidence
> 105,0.52,0.05,0.43,0.52
> 418,0.45,0.08,0.47,0.47
> 912,0.61,0.03,0.36,0.61
> The full submission must contain exactly one row for every id in public/test.csv. Duplicate IDs, missing IDs, extra IDs, missing columns, or extra/reordered columns return 0.0. Malformed probability or confidence cells are not useful, but they zero only the affected row.
> What Not To Do
> Using any of these approaches is grounds for solution rejection on review, regardless of leaderboard score:
> External PGN or game-database lookup to reconstruct hidden test cohorts, source rows, continuations, or outcomes.
> Chess-engine evaluation, Stockfish labels, best-move prediction, puzzle solving, or engine-assisted position scoring.
> Full-game result lookup, opening-book table lookup, or exact source archive counting instead of learning from public/train.csv.
> Player/rating/date/source metadata reconstruction or exploiting row order, file metadata, salted ID patterns, or source import details.
> Hosted or closed-source APIs for training, inference, pseudo-labeling, or distillation.
> Grader or platform exploitation, including malformed probability rows, hidden-file probing, or hard-coded answer dictionaries.
> Enforcement on Invalid Approaches
> Solutions that rely on source lookup, engine solving, hard-coded source reconstruction, hidden-file access, or format exploitation may be rejected before payout even if the submitted CSV receives a high score. Valid approaches must train or fit from the public training file and make predictions from the visible prefix fields only.

Inspiration note: Useful because it maps rich inputs into ordered/generated outputs with exact formatting and task-specific validation.

## Faithful Author-Highlights Generation from Biomedical Articles
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72s7x8hcz19babxgc0dqmqj989wb0q
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: medical
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Many biomedical journals ask authors to distill a paper into a short list of "highlights" — three to five sentences stating the key findings. Writing good highlights is a genuine distillation task: it means reading the full article and extracting what actually matters, in the authors' own framing, without drifting into claims the paper doesn't support and without simply parroting the abstract.
> This challenge asks you to reproduce that skill. Given the full body text of a biomedical article, generate its author-highlights. You are scored not only on how well your highlights match the real ones, but on whether they stay faithful to the article and genuinely distill the body rather than copying the abstract.
> The task is deliberately built to reward real comprehension and generation. Extractive shortcuts (lifting the abstract, or copying the opening of the body) and fabricated or generic text all score poorly. It is a task for generative language models, not for classification or regression.
> What makes this challenge distinct
> Two design choices separate this from ordinary summarization:
> First, the train and test sets are journal-disjoint. Every journal that appears in the test set is absent from training. You cannot learn one journal's house style and replay it; you must generate highlights for venues you have never seen, which forces genuine distillation over template-matching.
> Second, scoring includes an explicit anti-copying term. Many articles' abstracts overlap heavily with their highlights, so a model that simply returns the abstract would look deceptively good under naive similarity. This challenge measures your highlights against the abstract and penalizes copying above the level authors naturally use, so the cheap shortcut does not work.
> Evaluation
> Each prediction is scored by a composite of three components, then averaged over the test articles. All three are computed on content tokens: the text is lowercased, split into alphanumeric tokens (regex [a-z0-9]+), and a fixed English stopword list plus single-character tokens are removed. Let P be the content-token sequence of your highlights, R the reference (author) highlights, B the article body, and A the article abstract, each tokenized the same way.
> The per-article score is:
> score = coverage  -  0.50 * hallucination  -  0.35 * abstract_copying
> clipped to the range [0, 1]. If P is empty, the article scores 0. The final leaderboard value is the mean of this per-article score over all test articles.
> coverage — the average of a ROUGE-1 F1 and a ROUGE-2 F1 between P and R:
> for n in {1, 2}:
> Pn = multiset of n-grams of P
> Rn = multiset of n-grams of R
> inter_n = sum over n-grams of min(count in Pn, count in Rn)   # multiset intersection
> precision_n = inter_n / (total n-grams in Pn)
> recall_n    = inter_n / (total n-grams in Rn)
> f1_n = 2*precision_n*recall_n / (precision_n + recall_n)       # 0 if precision_n+recall_n = 0
> coverage = (f1_1 + f1_2) / 2                                       # equal-weighted average
> (n-grams are counted as multisets, so repeated n-grams contribute their counts; the intersection is the standard multiset intersection.)
> hallucination — the fraction of your highlights' unique content tokens that do not appear anywhere in the body:
> hallucination = 1  -  |set(P) ∩ set(B)| / |set(P)|
> "appear in the body" means the exact content token is present in the body's token set (unigram membership). Higher = more ungrounded content. (If P is empty this term is not reached, since an empty prediction already scores 0.)
> abstract_copying — token-set Jaccard overlap between your highlights and the abstract, with the authors' natural reuse level subtracted and the remainder renormalized:
> copy_raw = |set(P) ∩ set(A)| / |set(P) ∪ set(A)|          # Jaccard; 0 if P or A empty
> abstract_copying = max(0, copy_raw - 0.20) / (1 - 0.20)   # baseline 0.20 subtracted, renormalized to [0,1]
> The baseline 0.20 is the median highlights-to-abstract Jaccard observed among real author highlights, so overlap at or below that natural level incurs no penalty; only copying above it is penalized, scaled so that maximal copying (Jaccard = 1) gives a penalty of 1.
> For calibration under this exact metric: the authors' own highlights score about 0.90 (the practical ceiling), a partial or incomplete distillation scores in the middle, and abstract-copying (~0.06), body-copying, generic, or fabricated submissions score near zero.
> Dataset
> All files are in public/. The reference highlights for the test articles are held privately.
> File                  | Description
> ----------------------|-------------------------------------------------------
> train.csv             | id, body, highlights  -- article bodies with their real
> | author-highlights, for training / few-shot / fine-tuning.
> test.csv              | id, body  -- article bodies to generate highlights for.
> sample_submission.csv | id, highlights  -- a trivial example of the output format.
> train.csv columns:
> Column     | Type | Description
> -----------|------|-----------------------------------------------------------
> id         | str  | Article identifier.
> body       | str  | Full article body text (whitespace-normalised, long-form).
> highlights | str  | The author-written highlights (target to learn from).
> test.csv columns:
> Column | Type | Description
> -------|------|--------------------------------------------------------------
> id     | str  | Article identifier. Predict highlights for every row.
> body   | str  | Full article body text.
> Dataset facts:
> Quantity            | Value
> --------------------|------------------------------------------------
> Source              | biomedical journal articles under licenses
> | permitting reuse (details in private dataset metadata)
> Split               | journal-disjoint (test journals unseen in training)
> Training articles   | 526
> Test articles       | 175
> Object              | one article body -> one highlights list
> Target              | author-written highlights (typically 3-5 findings)
> Body length         | long-form (tens of thousands of characters)
> Submission
> Submit a CSV with one row per test article:
> Column     | Type | Description
> -----------|------|-----------------------------------------------------------
> id         | str  | Test article id from test.csv.
> highlights | str  | Your generated highlights for that article.
> Example of a correctly formatted submission (highlights shortened here for illustration; each cell holds the full generated highlights text for that article, quoted so any commas are safe):
> id,highlights
> 01ac770549fb5ad2,"A low-loading Pt/Ni-N-CNT catalyst was developed using carbon nanotube templates. The N-doped carbon layer uniformly encapsulates the skeleton. Catalytic activity matched commercial Pt/C at a fraction of the loading."
> 022314ace0c4a3e7,"Patients receiving the intervention showed a significant reduction in symptom severity at 12 weeks. The effect persisted at 6-month follow-up. No serious adverse events were attributed to the treatment."
> 0233e7818f56c015,"A new finite-element model predicts stress distribution in the implant under cyclic loading. Predicted fatigue life agreed with experimental data within 8 percent. The approach generalizes to other geometries."
> Include the header row.
> Provide a prediction for every test id; missing ids score as empty for that article.
> Rows with ids not in the test set are ignored.
> Quote the highlights field so that internal commas do not break the CSV.
> A note on strategy: the metric rewards highlights that (a) match the authors' key findings, (b) stay grounded in the article body, and (c) are genuinely distilled rather than copied from the abstract. Returning the abstract, returning the start of the body, or writing generic sentences will score near zero. Because the test journals are unseen in training, favour approaches that generalize distillation behaviour over ones that memorize a house style.
> What not to use
> Submissions relying on any of the following are illegitimate and will be rejected:
> Recovering the private reference highlights or abstracts for the test articles from any source other than your own model's generation from the provided body. Submissions must be generated from the article body given in test.csv, not retrieved or reconstructed from any external lookup. The journal-disjoint split and the composite metric are designed so that genuine generation is what the score reflects.
> Calling external services, network APIs, or remote models at grading time. The solution must produce the submission from the provided inputs without live external calls.
> Legitimate solutions read the provided article body and generate highlights from it.

Inspiration note: Useful because it maps rich inputs into ordered/generated outputs with exact formatting and task-specific validation.

## Leaf Symptom Evidence Ledger
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74ep23hjzb3psh8yzd0fzkqd8a105p
- DOMAIN exactly as displayed: Sequence To Sequence
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, image, multimodal
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-08; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Each example contains one leaf image, a packet of short question-answer evidence snippets, and a structured leaf-health claim. The claim may contain wrong host, diagnosis, symptom, severity, or lesion-zone slots. The goal is to audit the claim against the image and evidence packet, then submit a structured repair ledger.
> You must predict seven fields:
> | Output | What it represents |
> |---|---|
> | `claim_patch_set` | The contradicted claim slots and their corrected values. |
> | `symptom_evidence_set` | Canonical visual and text evidence tokens supporting the audit. |
> | `morphology_zone_vector` | A `3x3` lesion-zone vector over the leaf image. |
> | `severity_score_vector` | Lesion load, spatial spread, and clustering severity. |
> | `repair_order` | Ordered audit operations used to repair or accept the claim. |
> | `host_context` | Host plant category. |
> | `ledger_status` | Final audit status for the record. |
> This is not plant disease classification and it is not ordinary visual question answering. The prepared records model a plant-health review workflow where a visual finding, a short evidence packet, and a partially wrong ledger must be reconciled. A good solution must identify visual symptom evidence, estimate lesion distribution across the image, resolve host context, and repair only the contradicted slots.
> Dataset
> The prepared dataset contains:
> | Item | Value |
> |---|---:|
> | Training rows | 2200 |
> | Test rows | 600 |
> | Exact submission score | 1.0 |
> | Sample submission score | 0.056144024962797634 |
> The prepared files are:
> | Path | Type | Description |
> |---|---|---|
> | `dataset/public/train.csv` | CSV file | Training rows with public inputs and all target columns. |
> | `dataset/public/test.csv` | CSV file | Test rows with public inputs only. |
> | `dataset/public/images/` | directory | Public leaf images referenced by `image_path`. File names are opaque. |
> | `dataset/public/sample_submission.csv` | CSV file | Submission template with the exact required schema. |
> | `dataset/private/answers.csv` | CSV file | Private answer file with `sample_id` and all seven target columns. |
> Input Columns
> | Column | Type | Description |
> |---|---|---|
> | `sample_id` | string | Opaque public identifier. |
> | `image_path` | string | Relative path to the public leaf image. |
> | `qa_evidence_packet` | string | Short evidence snippets labeled `s1`, `s2`, and so on. Each snippet contains a question and answer about host, health, symptoms, cause, or diagnosis context. |
> | `faulty_ledger_claim` | string | A readable claim containing host, diagnosis, symptom, severity, and primary-zone slots. One or more slots may be wrong. |
> | `claim_slots` | string | Machine-readable claim slots in `key=value` form. |
> Example input values:
> | Column | Example value |
> |---|---|
> | `sample_id` | `leaf_0123456789abcdefab` |
> | `image_path` | `images/leaf_0123456789abcdefab.jpg` |
> | `qa_evidence_packet` | `s1 Q: What plant is shown? A: tomato. s2 Q: Are spots visible? A: yes, dark lesions are visible near the center.` |
> | `faulty_ledger_claim` | `host=tomato; diagnosis=late_blight; symptom=spotted_lesions; severity=moderate; zone=center` |
> | `claim_slots` | `host=tomato|diagnosis=late_blight|symptom=spotted_lesions|severity=moderate|zone=center` |
> Target Columns
> | Column | Type | Description |
> |---|---|---|
> | `claim_patch_set` | pipe-separated token set | Repairs for only the contradicted claim slots. Use tokens such as `host=tomato`, `diagnosis=early_blight`, `symptom=necrotic_lesions`, `severity=light`, or `zone=upper_left`. Use `none` when the claim is already consistent. |
> | `symptom_evidence_set` | pipe-separated token set | Canonical symptom and zone evidence tokens, such as `spotted_lesions`, `chlorotic_yellowing`, `necrotic_lesions`, `diffuse_spread`, or `zone_center`. |
> | `morphology_zone_vector` | JSON integer array | Length-9 row-major `3x3` vector of lesion-evidence buckets. Zone order is `upper_left`, `upper_mid`, `upper_right`, `mid_left`, `center`, `mid_right`, `lower_left`, `lower_mid`, `lower_right`. Values are integers from `0` through `4`. |
> | `severity_score_vector` | JSON integer array | Length-3 vector `[lesion_load, zone_spread, lesion_cluster]`. Each value is an integer from `0` through `4`. |
> | `repair_order` | ordered token sequence | Audit operation sequence separated by `>`, such as `inspect_image>read_evidence_packet>repair_diagnosis>verify_repairs`. |
> | `host_context` | categorical string | One of `apple`, `blueberry`, `cherry`, `corn`, `grape`, `orange`, `peach`, `pepper`, `potato`, `raspberry`, `soybean`, `squash`, `strawberry`, or `tomato`. |
> | `ledger_status` | categorical string | One of `clean`, `healthy_leaf`, `minor_repair`, `major_repair`, or `conflict_review`. |
> Example target values:
> | Column | Example value |
> |---|---|
> | `claim_patch_set` | `diagnosis=early_blight` |
> | `symptom_evidence_set` | `spotted_lesions|necrotic_lesions|zone_center` |
> | `morphology_zone_vector` | `[0,1,2,1,3,2,0,1,1]` |
> | `severity_score_vector` | `[3,3,2]` |
> | `repair_order` | `inspect_image>read_evidence_packet>repair_diagnosis>verify_repairs` |
> | `host_context` | `tomato` |
> | `ledger_status` | `minor_repair` |
> Submission Format
> Write the final submission CSV to exactly ./working/submission.csv.
> If the runtime root is /workspace, the equivalent absolute path is /workspace/working/submission.csv.
> The submission must contain exactly these columns in this order:
> | Order | Column |
> |---:|---|
> | 1 | `sample_id` |
> | 2 | `claim_patch_set` |
> | 3 | `symptom_evidence_set` |
> | 4 | `morphology_zone_vector` |
> | 5 | `severity_score_vector` |
> | 6 | `repair_order` |
> | 7 | `host_context` |
> | 8 | `ledger_status` |
> Example submission row:
> | Column | Example value |
> |---|---|
> | `sample_id` | `leaf_0123456789abcdefab` |
> | `claim_patch_set` | `diagnosis=early_blight` |
> | `symptom_evidence_set` | `spotted_lesions|necrotic_lesions|zone_center` |
> | `morphology_zone_vector` | `[0,1,2,1,3,2,0,1,1]` |
> | `severity_score_vector` | `[3,3,2]` |
> | `repair_order` | `inspect_image>read_evidence_packet>repair_diagnosis>verify_repairs` |
> | `host_context` | `tomato` |
> | `ledger_status` | `minor_repair` |
> Every sample_id from dataset/public/test.csv must appear exactly once. Extra columns, missing columns, reordered columns, duplicate IDs, wrong row count, extra IDs, missing IDs, malformed JSON vectors, wrong vector shapes, oversized strings, or invalid categorical values cause grading to fail or receive zero for the affected component.
> Evaluation
> Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> The final score is:
> Component Summary
> | Component | Inputs | Weight | Formula |
> |---|---|---:|---|
> | VisualSymptomScore | `morphology_zone_vector`, `severity_score_vector`, `symptom_evidence_set` | 0.42 | `0.50 * ZoneScore + 0.20 * SeverityScore + 0.30 * SymptomSetScore` |
> | ClaimRepairScore | `claim_patch_set`, `repair_order` | 0.28 | `0.65 * ClaimPatchScore + 0.35 * RepairOrderScore` |
> | HostContextScore | `host_context` | 0.15 | Inverse-frequency weighted macro F1 over host categories. |
> | LedgerStatusScore | `ledger_status` | 0.15 | Inverse-frequency weighted macro F1 over ledger-status categories. |
> Metric Details
> ZoneScore: Parses morphology_zone_vector as a length-9 JSON vector with values from 0 through 4. Row score is (1 - exact_weight) * active_entry_score + exact_weight * exact_vector_match, with exact_weight = 0.58. Active entries are positions where the true or predicted value is nonzero. True nonzero positions receive weight 3.0; other active positions receive weight 1.0.
> SeverityScore: Parses severity_score_vector as a length-3 JSON vector with values from 0 through 4. It uses the same vector formula as ZoneScore, with exact_weight = 0.50.
> SymptomSetScore and ClaimPatchScore: Tokens are split on |, ;, or ,. Row score is (1 - exact_weight) * token_F1 + exact_weight * exact_set_match, with exact_weight = 0.62.
> RepairOrderScore: Tokens are split on >. Row score is (1 - exact_weight) * normalized_Levenshtein_similarity + exact_weight * exact_sequence_match, with exact_weight = 0.70.
> Category components use inverse-frequency weighted macro F1 over classes present in the answer file.
> Invalid JSON, wrong shapes, non-finite values, out-of-range values, overlong strings, overlong token lists, and invalid categories receive zero for the affected component. Ground-truth values are validated strictly and are not clipped.
> The final weighted score is clipped to [0.0, 1.0]. An exact submission scores 1.0.
> What Not To Use
> Do not use lookup tables or deterministic mappings from sample_id, public row order, image file names, hash prefixes, split labels, source file names, source archive order, CSV order, compression artifacts, or duplicated image artifacts to recover target values.
> Do not hardcode labels for individual public rows, scrape private answer files, alter the grader, or exploit any source-specific identifier leakage. A valid solution should infer the structured ledger outputs from the supplied public image, evidence packet, and claim text.

Inspiration note: Useful because it maps structured multimodal or textual inputs into ordered repair ledgers, records, or generated outputs with task-specific validation.

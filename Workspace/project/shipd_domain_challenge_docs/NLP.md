# NLP Challenge Examples

Scrape timestamp: 2026-07-01T06:39:43+05:30

Confirmed examples in this document: 27

These entries are included only because the challenge detail page displayed this target domain. Titles were not used for classification.

## One-Shot NLI Misinformation Challenge
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dagtwhqaca8ka0k4ny2z4md82yj07
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Easy
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: ghost ranked 1st (leaderboard #47, score —); usamaasif ranked 3rd (leaderboard #16, score —); lady_faye1998 ranked #5 (leaderboard #25, score —); nxify ranked #8 (leaderboard #17, score —)

Full challenge description from page:

> Overview
> In this challenge, participants are tasked with predicting the category of a given text AND providing a logical rationale for that prediction. This evaluation focuses on fine-grained misinformation classification and qualitative reasoning verification.
> The dataset is designed to simulate a wide range of human-AI interactions where misinformation might occur. The dataset covers multiple domains, including:
> Science & Technology (e.g., misconceptions in physics, tech myths)
> History & Geography (e.g., temporal errors, location displacement)
> Health & Economics (e.g., medical misinformation, market fallacies)
> Daily Life (e.g., common urban legends)
> This is a One-Shot Learning NLP challenge. The training set is intentionally kept to only 3 samples (one for each category), forcing participants to develop models that can generalize effectively from extreme data scarcity or leverage large-scale external knowledge to reason through new examples.
> Evaluation
> The final score is a Composite Score that balances classification accuracy and reasoning quality:
> 𝑆
> 𝑐
> 𝑜
> 𝑟
> 𝑒
> =
> 0.6
> ×
> 𝐹
> 1
> 𝑚
> 𝑎
> 𝑐
> 𝑟
> 𝑜
> +
> 0.4
> ×
> 𝑆
> 𝑖
> 𝑚
> 𝑠
> 𝑒
> 𝑚
> 𝑎
> 𝑛
> 𝑡
> 𝑖
> 𝑐
> Score=0.6×F1
> macro
> +0.4×Sim
> semantic
> 1. Multi-class Categorization
> Evaluates the model's precision in identifying the category across 3 classes.
> Metric: Macro-averaged F1-Score.
> Formuala:
> 𝐹
> 1
> 𝑚
> 𝑎
> 𝑐
> 𝑟
> 𝑜
> =
> 1
> 𝑁
> ∑
> 𝑖
> =
> 1
> 𝑁
> 𝐹
> 1
> 𝑖
> F1
> macro
> =
> N
> 1
> ∑
> i=1
> N
> F1
> i
> , where
> 𝐹
> 1
> 𝑖
> F1
> i
> is the F1-score for class
> 𝑖
> i and
> 𝑁
> =
> 3
> N=3.
> Example code:
> from sklearn.metrics import f1_score
> macro_f1 = f1_score(y_true_labels, y_pred_labels, average='macro')
> 2. Semantic Rationale
> Evaluates the logical quality of your explanation. Your rationale is compared against expert-verified ground truth rationales using semantic vector similarity.
> Model: all-MiniLM-L6-v2 .
> Metric: Mean Cosine Similarity.
> Formuala:
> 𝑆
> 𝑖
> 𝑚
> (
> 𝑆
> ,
> 𝐴
> )
> =
> 𝐸
> 𝑠
> 𝑢
> 𝑏
> ⋅
> 𝐸
> 𝑎
> 𝑛
> 𝑠
> ∥
> 𝐸
> 𝑠
> 𝑢
> 𝑏
> ∥
> ×
> ∥
> 𝐸
> 𝑎
> 𝑛
> 𝑠
> ∥
> Sim(S,A)=
> ∥E
> sub
> ∥×∥E
> ans
> ∥
> E
> sub
> ⋅E
> ans
> ,
> Where
> 𝐸
> 𝑠
> 𝑢
> 𝑏
> E
> sub
> and
> 𝐸
> 𝑎
> 𝑛
> 𝑠
> E
> ans
> are the embedding vectors, and
> ∥
> ⋅
> ∥
> ∥⋅∥ denotes the
> 𝐿
> 2
> L
> 2
> norm.
> Example code:
> from sentence_transformers import SentenceTransformer, util
> model = SentenceTransformer('all-MiniLM-L6-v2')
> embeddings_sub = model.encode(texts_sub, convert_to_tensor=True)
> embeddings_ans = model.encode(texts_ans, convert_to_tensor=True)
> cosine_sims = util.cos_sim(embeddings_sub, embeddings_ans)
> avg_sim = cosine_sims.diagonal().mean().item()
> Dataset
> The dataset is provided in 3 files:
> train.csv: contains 3 samples (including id, inquiry, answer, category, rationale).
> test.csv: contains 197 samples (including id, inquiry, answer).
> sample_submission.csv: submission template for participants.
> Column Descriptions
> | Column | Type | Role | Description |
> | :--- | :--- | :--- | :--- |
> | id | Integer | ID | Unique record identifier. |
> | inquiry | String | Feature | The question or initial background/premise. |
> | answer | String | Feature | The provided explanation or reasoning. |
> | category | Integer | Target | 0: incorrect_question, 1: correct, 2: misleading. |
> | rationale | String | Target | Your logical explanation for the chosen category. |
> Category Details
> 0 (incorrect_question): The question itself is based on a false premise. The explanation follows and justifies this false premise.
> 1 (correct): Both the question and the explanation are factually accurate and logically sound.
> 2 (misleading): The question is a valid inquiry, but the provided explanation is factually incorrect, pseudoscientific, or logically flawed.
> Submission
> Your submission must be a CSV file containing exactly 197 rows (one for each test sample). The order of columns must follow the standard: id , category , rationale
> Sample Submission
> id,category,rationale
> 0,0,Your rationale
> 1,0,Your rationale
> 2,0,Your rationale
> ...
> Important
> Ensure all predictions are based on formal logic and verifiable facts. Incorrect questions (category 0) often contain blatant factual or temporal errors.
> Rows must align with test.csv IDs. Failure to match IDs or provide the correct number of rows will result in an error during grading.
> Empty or placeholder rationales will significantly lower your score due to the Semantic Similarity component.

Inspiration note: Useful because it centers linguistic judgment in a small prediction target, a reusable pattern for NLI, text trust, language modeling, or readability-style tasks.

## Old Norse Saga Language Model Training
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74qeveah3egh0k7tvjnc76mx84688s
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Hard
- GPU: H100
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: dominico ranked 1st (leaderboard #38, score —); gallantknight ranked 2nd (leaderboard #41, score —); osman0 ranked #9 (leaderboard #43, score —); shivank ranked #15 (leaderboard #27, score —)

Full challenge description from page:

> Overview
> Old Norse is one of the most morphologically complex Germanic languages ever recorded. A single noun like "konungur" (king) inflects into over a dozen surface forms encoding grammatical case, number, and definiteness. Verbs conjugate across person, number, tense, and mood. This inflectional richness creates an enormous vocabulary from a small set of roots, making Old Norse a stress test for language models that must learn word relationships from limited data.
> This challenge provides 35 Icelandic sagas totaling approximately 800,000 tokens and asks you to train a language model from random initialization within 30 minutes on a single GPU. Your model must learn enough Old Norse vocabulary, morphology, and narrative convention to predict masked words in sentences from 7 held-out sagas it has never seen. Pre-trained English models cannot handle Old Norse -- the characters, case system, and vocabulary have no overlap with modern training data. The only path is training from scratch on the saga corpus itself.
> Dataset
> Training corpus corpus.txt): Plain text concatenation of 35 Old Norse sagas in modernized Icelandic orthography. Approximately 4 million characters (~800,000 tokens). Contains Old Norse special characters including thorn (þ), eth (ð), and accented vowels (á, é, í, ó, ú, ý, æ, ö). Chapter divisions appear as numbered "kafli" headings. This is the only permitted training data.
> Test data test.jsonl): 1,500 multiple-choice cloze items extracted from 7 held-out sagas not included in the training corpus. Each line is a JSON object with these fields:
> id (string) -- Unique item identifier in NRS-XXXXXXXXXXXX format
> masked_sentence (string) -- A sentence with one content word replaced by the token [BLANK]
> option_a (string) -- First candidate word
> option_b (string) -- Second candidate word
> option_c (string) -- Third candidate word
> option_d (string) -- Fourth candidate word
> Exactly one option is the original word from the saga text. The three distractors are drawn from the same saga with matching grammatical suffixes, similar corpus frequency, and topical relevance.
> Sample submission sample_submission.csv): Correctly formatted submission with random option labels. Use as a format reference.
> Evaluation
> Submissions are scored by accuracy: the fraction of test items where the predicted option matches the correct answer.
> score = correct_predictions / 1500
> Score range: [0.0, 1.0] (higher is better). Random baseline picking uniformly among A, B, C, D scores approximately 0.25.
> Submission
> CSV file with two columns:
> id (string) -- Must match the IDs in test.jsonl exactly
> correct_option (string) -- Predicted answer: one of A, B, C, or D
> Example rows:
> id,correct_option
> NRS-00042DBC3F,B
> NRS-0031CAB4F3,A
> NRS-009D954333,D
> Requirements
> Exactly 1,500 rows matching the test set IDs
> Both id and correct_option columns present
> Predictions compared case-insensitively after whitespace stripping
> Empty or NaN predictions count as incorrect

Inspiration note: Useful because it centers linguistic judgment in a small prediction target, a reusable pattern for NLI, text trust, language modeling, or readability-style tasks.

## Biomedical QA Intrusion Quality Scoring
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70mzyymffs7djr6wp20znma189cpjs
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Home page recommendation/context: Beat jesuisnadi's score of 0.790!

Full challenge description from page:

Biomedical Answer Intrusion Ranking
Overview
Biomedical QA systems often assemble candidate answer pools from retrieved items, generated alternatives, and human-authored distractors. Some candidates belong with the displayed question, while others are fluent biomedical answers that were written for a nearby but different question. This challenge asks you to score whether each candidate answer is an intruder in the displayed question's answer pool.
The labeled set is intentionally small: it represents a limited expert labeling budget. A larger unlabeled pool is included so solvers can use representation learning, pseudo-labeling, calibration, or other semi-supervised strategies. The private test split uses unseen biological question groups, variable numbers of intruder candidates per question, and near-topic intruders selected to avoid simple lexical, answer-length, or repeated-answer-frequency shortcuts.
This is practical for scientific answer-pool quality control. A deployed system needs to catch plausible but off-question candidates before ranking or generation, especially when the candidate is biologically fluent and topically close enough to pass a shallow keyword check.
Dataset
File descriptions
train.csv -- 2,000 labeled candidate-answer rows from 500 biological questions.
train_unlabeled.csv -- 6,000 additional public candidate-answer rows without labels.
test.csv -- 16,000 unlabeled candidate-answer rows from 4,000 held-out biological questions.
sample_submission.csv -- A template showing the required submission format with random answer_intrusion scores.
Column descriptions
id (string) -- Unique 12-character hexadecimal identifier for each candidate-answer row.
question_id (string) -- Shared identifier linking candidate rows from the same biological question.
candidate_slot (integer) -- Deterministic slot number within a question, from 1 to 4. Slot number is not a reliable target signal.
question (string) -- Biological question text.
candidate_answer (string) -- Candidate answer text to compare with the displayed question.
answer_intrusion (float/integer) -- Target in train.csv and prediction column in submissions. In training labels, 1 means the candidate answer is an off-question intruder; 0 means it belongs to the displayed question's answer pool.
Evaluation
Submissions are scored using row-level AUC Lift. Higher is better.
answer_intrusion is treated as the prediction score for the positive class. First, ROC AUC is computed over all candidate rows. The final score is the lift above random ranking:
def evaluate(y_true, answer_intrusion):
auc = roc_auc(y_true, answer_intrusion)
return max(0.0, min(1.0, 2.0 * auc - 1.0))
A random ranking scores 0.0; perfect ranking scores 1.0. The score is bounded between 0 and 1.
Submission
Submit a CSV file with one answer-intrusion score for every row in test.csv.
id (string) -- The candidate-answer row identifier from test.csv.
answer_intrusion (float) -- A finite value between 0 and 1, where higher means the candidate is more likely to be an off-question answer-pool intruder.
Example:
id,answer_intrusion
53bca78f9768,0.07935
40334c4522b7,0.698422
426b4e60e186,0.913862
1e9e40f67161,0.381265
Requirements
The file must contain exactly one row for every row in test.csv, plus the header.
Every id from test.csv must be present exactly once.
answer_intrusion values must be numeric, finite, and between 0 and 1 inclusive.
File format must be .csv with exact column names id,answer_intrusion.
What Not To Use
Do not search exact question or answer text on the web or in public answer-key corpora to recover held-out provenance.
Do not use cached row records, external lookup tables, or checkpoints/adapters trained specifically to identify rows from this QA corpus.
Do not reverse-map candidate ids, row order, or candidate slots back to hidden row identifiers or original option letters.
Do not submit a hardcoded table of held-out answer_intrusion values recovered from outside the provided public files.

Inspiration note: Useful because it turns nuanced language or biological text judgment into a compact supervised prediction target with clear held-out scoring.

## Microbial DNA Compositional Motif Restoration
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75mshatktzvf18qhhstcpnf589h7e5
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Home page recommendation/context: Beat pokymono's score of 0.250!

Full challenge description from page:

Microbial DNA Compositional Motif Restoration
Overview
Microbial genomes carry distinctive DNA compositional signatures: the frequencies of short nucleotide motifs (k-mers) vary systematically across species and even across genomic islands within a genome. This challenge poses the restoration of a missing compositional motif from a contig's signature.
Each genome contig is written as a short sequence of its most frequent hexamer (6-mer) motifs, in rank order, as opaque integer k-mer tokens — its "compositional signature." One mid-rank token has been removed (masked); the task is to restore the missing k-mer token, drawing on the contig's other top k-mers and on the k-mer profile across sibling contigs from the same genome (genome context).
The masked token is one hexamer from a fixed vocabulary of 1 024 tokens (the 1 024 most frequent hexamers in the corpus — the only tokens that ever appear in the data). Rather than a single guess, you submit a ranked list of up to 10 candidate tokens per contig and are scored by where the gold token lands in your ranking (partial credit), so a near-miss still counts. K-mer identities are anonymised (opaque integer ids), and genomes are disjointly split between train and test, so the restoration must be learned from the training contigs: no external genomic knowledge, atlas, or pretrained model applies.
Dataset
public/train.csv — id, genome_context, kmer_seq
kmer_seq (string): the contig's top-16 most frequent k-mers as space-separated opaque integer tokens, in rank order (the full, unmasked signature)
genome_context (string): the top-16 k-mers pooled across the contig's sibling contigs from the same genome — the genomic context
public/test.csv — id, genome_context, masked_kmer_seq, mask_index
masked_kmer_seq (string): the contig's signature with one mid-rank token replaced by ?
mask_index (int): 0-based position of the ?
public/sample_submission.csv — a valid baseline submission
Train and test contigs come from disjoint genomes. The vocabulary is fixed at the 1 024 tokens appearing in train.csv, and every masked k-mer is one of them — so the candidate set is fully known from the training data.
Evaluation
Submissions are scored with K-mer Restoration Rank (KRR) — the mean reciprocal rank of the gold token within each contig's submitted ranked candidate list, with a cutoff of 10. For one contig, if the gold token is the r-th entry of your ranked list (r ≤ 10) it scores 1/r; if it is absent (or below rank 10) it scores 0. KRR is the mean over all test contigs:
KRR = mean over contigs of ( 1 / rank_of_gold_in_your_list )   # 0 if gold not in top 10
Score is in [0, 1]; higher is better. Unlike a top-1 exact match, this gives partial credit: ranking the gold token 3rd scores 1/3 instead of 0, so a stronger model that pushes the gold token up the list separates clearly on the leaderboard.
Reference baselines (public training data only)
The task is solvable well above the most-frequent floor by learning k-mer co-occurrence and genome context. It remains hard: the masked token is in the genome context only about a third of the time, so a co-occurrence ranker reaches only ~0.14, with the gold token landing in its top 10 about 31% of the time (Recall@10 ≈ 0.31). A stronger context-aware sequence model can realistically push KRR into roughly the 0.20–0.30 range — a clear, separable gain over the cheap baseline — by improving both recall and the rank of the gold token; a solver with no model of the anonymised tokens collapses toward the floor.
Submission Format
Submit a CSV with exactly two columns:
id: contig identifier from test.csv
predicted_kmer_ids: your ranked candidate tokens for the masked position — 1 to 10 integer k-mer ids, best first, space-separated, in one cell
id,predicted_kmer_ids
3a1f9c2b7e4d0581,512 77 1024 9 311
c8b2d90f3e61a744,77 512 6
...
Strict format requirements (submission rejected on violation):
Exactly the columns id and predicted_kmer_ids — no extra columns.
One row for every test id, no duplicate ids. Every test id must be present; extra rows whose id is not in the test set are ignored.
Each predicted_kmer_ids cell is a non-empty, duplicate-free list of at most 10 integer tokens, ranked best-first; no NaN / missing values.
Approaches
Masked sequence modeling: train a bidirectional model (transformer/BiLSTM) over the compositional signatures with random masking, conditioning on genome_context, then rank the vocabulary by the model's probability for the held-out position and submit the top 10.
Co-occurrence / association models: estimate k-mer–k-mer co-occurrence and k-mer–genome-context association from the training signatures, with backoff, and rank candidate tokens — a strong, cheap baseline.
Genome-context conditioning: use genome_context to bias the ranking toward k-mers consistent with the genome's overall compositional profile.
Submit a ranked top-10, not a single guess — partial credit rewards getting the gold token into your list even when it is not your top pick.
Validate KRR on a held-out split of the training contigs before predicting the test set.
Prohibited Methods
De-anonymisation / external lookup: recovering real k-mer sequences behind the opaque tokens, or matching signatures against any external genome database / reference / model.
Source identification: identifying or retrieving the originating organism or genome. Ids are opaque; tokens are anonymised.
Hard-coded answers: producing answers by any means other than a model built from the provided training data.
Valid solutions learn k-mer co-occurrence and genome context from train.csv and apply them to restore the masked tokens.
Configuration
Direction: maximize
Min Score: 0.0
Max Score: 1.0
Difficulty: Hard
GPU Tier: A10G

Inspiration note: Useful because it turns nuanced language or biological text judgment into a compact supervised prediction target with clear held-out scoring.
---

<!-- GOOGLE_DRIVE_APPEND_2026_07_01 -->
**Google Drive Folder Append (2026-07-01T08:30:33+05:30)**

These entries came from the two shared Google Drive folders. They may duplicate earlier examples because this append intentionally preserves all shared accepted/approved challenge specs. Drive entries use folder/domain labels when present and inference from the folder/spec text when no explicit DOMAIN field is available.

## representation_learning
- Challenge URL: https://drive.google.com/drive/folders/1_qeNu_-NLCXKjIuZb0jQWNHNsnXzqNIC
- Source file: challenge_description.txt
- DOMAIN used for this document: NLP (from Drive domain folder or folder name)
- Status: From Google Drive accepted-challenge collection
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: See description if specified
- Tags: Not shown/captured
- Best/top context found: Google Drive: Drive folder 1 / NLP / representation_learning

Full challenge description from Drive:

> Representation Learning for Compositional Generalization from Survey Reports
> Overview
> This challenge is a representation-learning benchmark, not a prediction task. You are given 10,000 textual field-survey reports describing crystalline specimens collected from various environments. Your job is to produce a learned embedding vector for every single report — both the 7,500 labeled training reports and the 2,500 unlabeled test reports. You do not submit label predictions. You submit a single (10000, D) matrix of embeddings.
> After you submit, the grader applies the standard self-supervised linear-probe protocol used to benchmark representation-learning methods in the literature (SimCLR, MoCo, DINO, CLIP, sentence-transformers). It standardizes the embeddings using statistics fit on the training rows, trains eight independent linear logistic-regression probes (one per target label) on top of the training embeddings, and evaluates each probe on the test embeddings. Your score is the mean accuracy across probes, with extra weight placed on test rows whose (primary_crystal, environment) combination never appears in the training set.
> The central tension of the task is compositional generalization. A report-level embedding that memorizes surface patterns of specific (crystal, environment) co-occurrences will score well on the seen portion of the test set but fail on the unseen-pair subset. An embedding that captures the underlying family-level and zone-level structure of the domain will transfer. You are being evaluated on the geometric quality of your embedding space, not on your ability to predict one specific label.
> Task
> Read the 10,000 reports in ./dataset/public/train.csv and ./dataset/public/test.csv.
> Produce one embedding vector of dimension D (where 1 <= D <= 512) for each report.
> Write a CSV to ./working/submission.csv with 10,000 rows covering every id, and columns id, emb_0, emb_1, ..., emb_{D-1}.
> The grader trains 8 linear probes on your training embeddings and evaluates them on your test embeddings.
> Your final score is 0.5 * overall_mfa + 0.5 * unseen_pair_mfa, where each term is the mean of per-field test accuracies.
> Crystal Families and Environment Zones
> The 24 crystal types group into 6 families, and the 10 environments group into 3 zones. These groupings are latent structure in the data. Embeddings that recover this hierarchy generalize to unseen pairs; embeddings that treat each crystal and environment as an atomic token do not.
> Crystal families:
> pyrogenic: vexirite, ignivane, solcrete, thermolux
> cryogenic: glacimite, frostyne, cryolux, nivalite
> pressurized: gravicite, densyte, compranite, pressovane
> radiative: luminyte, spectrite, pulsarite, novaflux
> volatile: tremvite, zephyrium, aerolith, fluxenite
> hybrid: pyroglace, voltanite, pressolux, cryovane
> Environment zones:
> thermal: thermoclast ridge, magmaflux vent, pyroclast basin, geotherm pocket
> stable: lithovault, statizone, cryofield
> reactive: soluflux channel, electroplasm fault, cascadium trench
> Label Vocabularies
> The grader trains one probe per field. The exact-match accuracy of each probe against the private test labels is averaged to compute MFA.
> primary_crystal (24 values):
> vexirite, ignivane, solcrete, thermolux
> glacimite, frostyne, cryolux, nivalite
> gravicite, densyte, compranite, pressovane
> luminyte, spectrite, pulsarite, novaflux
> tremvite, zephyrium, aerolith, fluxenite
> pyroglace, voltanite, pressolux, cryovane
> formation_pattern (12 values):
> dendric, lamellux, fractoid, helicoid
> clustoid, spinoid, vorticial, fibrillux
> strandoid, orbicular, tessellux, helixoid
> environment (10 values):
> thermoclast ridge, magmaflux vent, pyroclast basin, geotherm pocket
> lithovault, statizone, cryofield
> soluflux channel, electroplasm fault, cascadium trench
> stability_class (10 values, ordered from most stable to least stable):
> inert
> dormant
> stable
> semi-stable
> metastable
> oscillating
> critical
> pre-cascade
> cascade-imminent
> volatile
> threat_level (7 values): integers 0, 1, 2, 3, 4, 5, 6.
> recommended_protocol (10 values):
> passive-observation
> standard-survey
> extended-monitoring
> enhanced-tracking
> priority-extraction
> cryo-stabilization
> resonance-dampening
> containment-alpha
> containment-omega
> evacuation-protocol
> secondary_action (5 values):
> log-and-archive
> schedule-followup
> flag-for-review
> dispatch-specialist-team
> initiate-quarantine-zone
> hazard_vector (8 values):
> thermal-runaway
> structural-collapse
> radiative-burst
> chemical-dissolution
> electromagnetic-surge
> seismic-cascade
> phase-inversion
> none-detected
> Dataset
> Files are provided at ./dataset/public/.
> ./dataset/public/train.csv — 7,500 rows. Columns:
> id — unique integer identifier for each report.
> report_text — the raw textual survey report.
> primary_crystal — one of the 24 crystal values.
> formation_pattern — one of the 12 pattern values.
> environment — one of the 10 environment values.
> stability_class — one of the 10 ordered stability values.
> threat_level — integer 0 through 6.
> recommended_protocol — one of the 10 protocol values.
> secondary_action — one of the 5 action values.
> hazard_vector — one of the 8 hazard values.
> ./dataset/public/test.csv — 2,500 rows. Columns:
> id — unique integer identifier.
> report_text — the raw textual survey report.
> (No label columns are provided for test rows. Labels are held out privately by the grader.)
> ./dataset/public/sample_submission.csv — 10,000-row template:
> id — every id from train.csv and test.csv, appearing exactly once.
> emb_0, emb_1, ..., emb_15 — 16 embedding columns, all zeros. This is only a structural template; submitting it unchanged will score at chance.
> Submission Format
> Write your submission to ./working/submission.csv.
> Path: exactly ./working/submission.csv (relative to the run directory).
> Rows: exactly 10,000. Every id from train.csv and every id from test.csv must appear exactly once. Extra ids, missing ids, and duplicate ids all cause the submission to be rejected.
> Columns: id followed by emb_0, emb_1, emb_2, ..., emb_{D-1}, in that order, where D is your chosen embedding dimension.
> Embedding dimension D must satisfy 1 <= D <= 512.
> All embedding values must be finite floats. No NaN, no Inf, no strings, no missing cells.
> The id column must contain integers.
> You may freely choose the embedding dimension, the representation-learning method, and whether train and test embeddings come from a single model or a joint pipeline. The only constraint is that the final CSV passes validation.
> Evaluation
> The grader runs the following deterministic protocol.
> Load ./working/submission.csv. Confirm exactly 10,000 rows, all required ids present exactly once, 1 <= D <= 512, and all embedding values finite.
> Partition the embedding matrix into train_emb (7,500 rows) and test_emb (2,500 rows) using the ids from train.csv and test.csv.
> Fit sklearn.preprocessing.StandardScaler on train_emb only. Apply the fitted scaler to both train_emb and test_emb. This zero-centers and unit-variance-normalizes each embedding dimension using training statistics.
> For each of the 8 target fields:
> Instantiate sklearn.linear_model.LogisticRegression(C=1.0, max_iter=2000, random_state=42).
> Fit it on standardized train_emb with the field's training labels.
> Predict on standardized test_emb.
> Compute exact-match accuracy against the held-out private test labels.
> Compute overall_mfa as the mean of the 8 per-field accuracies over all 2,500 test rows.
> Compute unseen_pair_mfa as the mean of the 8 per-field accuracies restricted to the subset of test rows whose true (primary_crystal, environment) pair is not present anywhere in train.csv. This subset is approximately 15% of the test set (roughly 375 rows).
> Compute final_score = 0.5 * overall_mfa + 0.5 * unseen_pair_mfa.
> The unseen-pair split is fixed in advance based on the private test labels. Solvers cannot observe which test rows fall into this subset, but can approximate it by identifying underrepresented or missing (crystal, environment) pairs in the training set.
> This scoring protocol follows the standard self-supervised linear-probe evaluation used in representation-learning papers (SimCLR, MoCo, DINO, CLIP, and sentence-transformer benchmarks) to measure the quality of learned features. A logistic-regression probe with these exact hyperparameters is a well-calibrated measure of linear separability.
> Key Challenges
> Compositional generalization. About 15% of test rows use (crystal, environment) pairs that never appear in the training set. Embeddings that capture the 6 crystal families and 3 environment zones — the latent compositional structure of the domain — will generalize to these unseen pairs. Embeddings that memorize surface statistics of specific pair co-occurrences will collapse on the unseen-pair subset and pull down the final score.
> Multi-concept representation. A single embedding vector must simultaneously support linear recovery of 8 different concepts: the crystal identity, the formation pattern, the environment, the stability class, the threat level, the recommended protocol, the secondary action, and the hazard vector. The embedding space must be informative along all of these axes, not only the easiest ones.
> Partial observability. Approximately 30% of training reports omit 2 to 3 crystal properties that would otherwise appear. Your embedding must be robust to missing features and still place incomplete reports near their complete counterparts in embedding space.
> Label noise. The derived fields (recommended_protocol, secondary_action, hazard_vector, and others that depend on upstream labels) have 10 to 15 percent injected label noise in the training set. A linear probe trained on noisy labels will never reach 1.0 accuracy on the clean private test set. The effective ceiling for any one field is approximately 0.88.
> Invented vocabulary. Crystal names, formation patterns, environments, protocols, and hazards are all invented terms with no prior semantic content in pretrained language models. Zero-shot inference from generic embeddings will not suffice; the embedding method must learn structure from this specific training corpus.
> Submission Example
> A valid submission begins like this. The example below uses 6 embedding dimensions for illustration; you may use any D from 1 to 512.
> id,emb_0,emb_1,emb_2,emb_3,emb_4,emb_5
> 0,0.1234,-0.5678,0.9012,-0.3456,0.7890,-0.1234
> 1,-0.2345,0.6789,-0.0123,0.4567,-0.8901,0.2345
> 2,0.3456,-0.7890,0.1234,-0.5678,0.9012,-0.3456
> 3,-0.4567,0.8901,-0.2345,0.6789,-0.0123,0.4567
> ...
> 9999,0.5678,-0.9012,0.3456,-0.7890,0.1234,-0.5678
> Requirements
> File path: ./working/submission.csv exactly.
> File format: CSV with a header row.
> Row count: exactly 10,000 data rows (plus the header).
> Id coverage: every id in train.csv and every id in test.csv must be present exactly once.
> Column order: id first, then emb_0, emb_1, ..., emb_{D-1} in numeric order.
> Embedding dimension: integer D with 1 <= D <= 512.
> Embedding values: finite floats only. No NaN, no Inf, no strings, no empty cells.
> Id type: integer.
> No trailing commas, no extra columns, no extra rows.
> What Not To Use
> What NOT to Submit
> Do not submit one-hot encodings of any label (or labels you predicted yourself) as the embedding. The linear probe is trained on your vectors, so smuggling predicted labels in will not help on the unseen-pair subset, which by construction contains (crystal, environment) combinations absent from training. A memorized per-row label cannot compositionally generalize.
> Do not submit raw TF-IDF, bag-of-words, or character n-gram vectors as the embedding without any learning. These representations are typically high-dimensional and sparse, and when projected to D <= 512 dimensions without a learned objective they score weakly under the linear-probe protocol. TF-IDF baselines are known to underperform learned embeddings on this style of benchmark.
> Do not call external network APIs from within the grading environment. The grader runs offline. Any embedding that requires live API access at grading time will fail. All embeddings must be materialized into the submission CSV before grading begins.
> Do not submit random or uninformative embeddings and expect them to score. The 16-dim zero matrix in sample_submission.csv is only a template; submitting it produces chance-level accuracy on every probe.
> Do not submit embeddings of dimension greater than 512 or less than 1, or embeddings containing any non-finite value. Such submissions are rejected before scoring.

Inspiration note: Useful as an NLP benchmark pattern with rich text inputs, a clear prediction column, and room for semantic reasoning beyond keywords.

## Adversarial Textual Alignment Scoring
- Challenge URL: https://drive.google.com/drive/folders/158SLEvPlAZvQ5p3TkU26mcb8OXWeCpo9
- Source file: cd.txt
- DOMAIN used for this document: NLP (from Drive domain folder or folder name)
- Status: From Google Drive accepted-challenge collection
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: See description if specified
- Tags: Not shown/captured
- Best/top context found: Google Drive: Drive folder 1 / NLP / Adversarial Textual Alignment Scoring

Full challenge description from Drive:

> Adversarial Semantic Alignment Mapping (ASAM)
> Overview
> In advanced Natural Language Processing (NLP), determining the relationship between two sentences requires more than a simple categorical label (e.g., "True" or "False"). The Adversarial Semantic Alignment Mapping (ASAM) challenge task agents with predicting a Semantic Entailment Logic Consistency (SELC) score.
> This score represents the degree of logical consistency between a premise and a hypothesis, mapped to a continuous scale from 0.0 to 1.0.
> 1.0: Perfect entailment/consistency.
> 0.5: Neutral/unrelated relationship.
> 0.0: Strong contradiction or logical conflict.
> The challenge is "adversarial" because the scoring function is not a simple linear mapping. It incorporates domain-specific biases and structural textual features (such as length interactions) that a model must learn from the provided training data.
> Real-World Context
> This task simulates a "Reasoning Audit" system used in automated fact-checking. The dataset is a derivative of a standard multi-genre linguistic corpus covering diverse domains such as:
> Fiction: Creative and narrative text.
> Government: Formal reports and documents.
> Slate: Journalistic and opinion pieces.
> Telephone: Transcribed spoken conversations.
> Each domain (obfuscated as a domain_code) follows a slightly different logical weighting, forcing the agent to generalize across different linguistic styles.
> Dataset
> Statistics
> Total Samples: 10,000
> Train Set: 8,000 rows
> Test Set: 2,000 rows
> Score Distribution: Mean ~0.52, Std ~0.22.
> File Structure
> train.csv — Labeled text pairs with SELC scores.
> test.csv — Unlabeled text pairs for evaluation.
> sample_submission.csv — Template demonstrating the submission format.
> Data Example
> pair_id	premise_text	hypothesis_text	domain_code	alignment_score
> ALN-7B8...	The report was released on Friday.	The document was made public.	DOM-A1B2	0.8920
> ALN-9C1...	I am going to the park.	It is raining outside.	DOM-C3D4	0.4510
> ALN-2F4...	The cat is black.	The cat is white.	DOM-A1B2	0.1250
> Evaluation
> Submissions are evaluated using the Variance Alignment Metric (VAM), which is mathematically equivalent to the R-squared (Coefficient of Determination).
> Formula
> VAM = 1.0 - (Sum of Squared Residuals / Total Sum of Squares)
> 0.0: Baseline performance (equivalent to predicting the mean).
> 1.0: Perfect alignment with the target logic.
> Example: If the actual scores are [0.8, 0.2] and you predict [0.7, 0.3], the residuals are small, resulting in a high VAM.
> Submission Format
> Submit a CSV file with exactly two columns: pair_id and alignment_score.
> Column	Type	Description
> pair_id	string	Unique identifier from test.csv.
> alignment_score	float	Predicted alignment value between 0.0 and 1.0.
> Example
> pair_id,alignment_score
> ALN-3A7F2C01D8AB,0.8723
> ALN-9E12B4F7A3CD,0.1456
> Constraints & "What Not To Use"
> To ensure a fair and competitive environment, the following are strictly prohibited:
> No External LLM APIs: Use of GPT-4, Claude, Gemini, or any other external proprietary LLM APIs is strictly prohibited.
> No Source Recovery: You may not attempt to identify or recover the original source datasets to perform exact-match lookups.
> No Reverse Engineering of Formulae: You may not use automated symbolic search to "decrypt" the underlying mathematical formula without demonstrating learning from the textual features.
> No Rule-Only Shortcuts: Solutions that rely solely on hardcoded heuristics without analyzing the semantic content will be disqualified.
> Self-Contained Logic: Your agent must learn the mapping from the provided train.csv.
> What Not To Use
> No External LLM APIs: Use of GPT-4, Claude, Gemini, or any other external proprietary LLM APIs for scoring is strictly prohibited.
> No Reverse Engineering of Formulae: You may not use automated symbolic regression or brute-force search to "decrypt" the underlying mathematical formula without demonstrating learning from the textual features.
> No Rule-Only Shortcuts: Solutions that rely solely on hardcoded rules (e.g., "if word count > 10, score = 0.5") without analyzing the semantic content of the pairs will be disqualified.
> Self-Contained Logic: Your agent must learn the mapping from the provided train.csv.

Inspiration note: Useful as an NLP benchmark pattern with rich text inputs, a clear prediction column, and room for semantic reasoning beyond keywords.

## Synthetic Redaction Field Type Inference approved
- Challenge URL: https://drive.google.com/drive/folders/1dc0BUiG010AyGs5i1hacoJezKV4S7LDc
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: NLP (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: Approved (from Drive folder name)
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: Not shown/captured
- Tags: Not shown/captured
- Best/top context found: Synthetic Redaction Field Type Inference_approved from shared Google Drive folder

Full challenge description from Drive:

> # Challenge creation form — fill-in
> **Platform status:** **Approved** — *Synthetic Redaction Field Type Inference Under Template Shift* (pairs with accepted dataset *Synthetic Redaction Field Type Inference Corpus*).
> ---
> ## 1) Difficulty
> **Select:** **Hard**
> ---
> ## 2) Challenge Title
> ```
> Synthetic Redaction Field Type Inference Under Template Shift
> ```
> ---
> ## 3) Problem Description
> # Synthetic Redaction Field Type Inference Under Template Shift
> ## Overview
> This is an **NLP** challenge that models the task a redaction-review officer performs when asked "what kind of information was hidden behind this black bar?" The model receives a short English passage as its sole input and must infer a hidden linguistic attribute of that passage under distribution shift — reasoning happens purely over the language in the text; there are no numeric feature columns, no categorical feature columns, and no identifier-based shortcuts. The black bar itself carries **zero signal** (the pixels inside are pure black); the only recoverable evidence is the surrounding natural-language text: the form header, the preceding sentence fragment, and the trailing style tokens.
> Every example in this corpus is a short English passage of 15–40 words with exactly one `[REDACTED]` token embedded inside it. The solver reads the passage as text and assigns one of 8 hidden field-type tags (T0..T7, anonymized at release — internal semantics span names, dates, case numbers, addresses, monetary amounts, phone numbers, source identifiers, and a catch-all "other" tag). Every passage begins with a short opaque **template marker token** that identifies which synthetic document template the passage was drawn from. A prefix cue phrase precedes the redaction and a style phrase trails it.
> **The dataset exhibits a meaningful distribution shift between train and test.** Some template markers appear in training with full labelled data. Other template markers appear **only at test time** — the solver has never seen labelled examples of these markers and must generalise by reasoning over the text alone. Roughly 40 % of test rows come from these held-out markers.
> The grammar is **template-conditional**: the relationship between a prefix cue phrase and the correct type tag depends on the marker the passage was drawn from. A solver that hard-codes a single global cue → type dictionary will be wrong on many templates.
> **What makes this problem challenging:**
> - **The Template Collision Trap**: the same surface cue phrase (e.g. *"identified as"*, *"located at"*, *"reachable at line"*) resolves to different type tags under different templates. Template-agnostic models cap around 0.23 macro-F1.
> - **The Hold-Out Marker Shift**: a substantial fraction of test rows carry template markers that do not appear in the training split. Models that learn per-marker lookups score high on in-distribution test rows and collapse on the held-out slice. Overall macro-F1 for such models lands around 0.51.
> - **The Adversarial Surface Cue**: roughly 12 % of rows (both train and test) are adversarial — the prefix cue phrase was sampled to deliberately mismatch the true type tag under that row's template. A solver that ever trusts the surface cue unconditionally loses the adversarial bucket.
> - **Per-template deviation**: individual templates within the same broad family still differ from each other in how some cue phrases are interpreted. Models must learn both the shared family behaviour and the per-template corrections from training data.
> - **Irreducible label noise (~ 8 %)**: randomly flipped labels cap the theoretical ceiling around 0.85 macro-F1.
> **Why current pretrained LLMs do not shortcut this:**
> - The template marker vocabulary is synthetic and carries zero priors from any pretraining corpus. Zero-shot prompting cannot recover the hidden template-conditional semantics.
> - Type labels are released as opaque integer tags 0..7 (the internal PII-like semantics are NOT exposed to the agent), so an LLM cannot bolt on a pretrained NER tagger and reverse-engineer the label mapping from column names.
> - The surface cue → type mapping is deliberately broken on adversarial rows, so any in-context-learning strategy that trusts English semantics ("reachable at line X obviously means a phone number") gets punished proportionally to the adversarial fraction.
> **Training envelope:** A10G (24 GB) GPU, ≤ 1 hour wall-clock budget. Any approach is valid — TF-IDF + classical ML, fine-tuning a ≤ 3 B-param open-weights LM, or training a small transformer from scratch on the 7,680-row training set. No closed-source APIs.
> ## Evaluation
> Submissions are scored using **macro-averaged F1** over the 8 redaction type tags (T0..T7). Macro weighting prevents the dominant tag T0 (~ 27 %) from masking failures on the long-tail tags T6 and T7. **Higher is better.** Minimum: 0.0, Maximum: 1.0.
> A strict validator returns **0.0** if any of the following fails:
> - submission missing `redaction_id` or `redaction_type` columns
> - duplicate `redaction_id` values in the submission or the answer set
> - `set(submission.redaction_id) != set(answers.redaction_id)` (missing or extra rows)
> - `len(submission) != len(answers)`
> - any predicted `redaction_type` not castable to an integer in `[0, 7]`
> - NaN or null values in predictions
> ## Dataset
> - `train.csv` — 7,680 rows: `redaction_id` (int), `passage` (string, the event text with one `[REDACTED]` token), `redaction_type` (int, 0..7).
> - `test.csv` — 3,360 rows: `redaction_id` (int), `passage` (string). No labels. A substantial fraction of test rows carry **held-out template markers** whose marker tokens do not appear anywhere in `train.csv`; the solver must generalise to them without labelled examples.
> - `sample_submission.csv` — 3,360 rows: `redaction_id` (int), `redaction_type` (int, constant 0 baseline). Shows the required submission format; macro-F1 ≈ 0.054.
> ### Column reference
> | Column | Type | Description |
> |--------|------|-------------|
> | redaction_id | int | Unique redaction-event identifier (shuffled, not sequential per template) |
> | passage | string | 15–40 word English-language passage containing exactly one `[REDACTED]` token, a template marker `<TPL-XY>` at the start, and a template-specific style suffix |
> | redaction_type | int | Hidden field type, 0..7. Anonymized (semantics not disclosed to the solver). Present in `train.csv` only. |
> ## Submission
> Submit a CSV file with exactly 3,360 rows (one per test `redaction_id`), a header row, and two columns:
> | Column | Type | Description |
> |--------|------|-------------|
> | redaction_id | int | Identifier copied from `test.csv` |
> | redaction_type | int | Predicted type, integer in `[0, 7]` |
> **Example of a correctly formatted submission file:**
> ```
> redaction_id,redaction_type
> 0,3
> 1,0
> 2,7
> 3,1
> 4,0
> ...
> ```
> ---
> ## 4) Tags
> **Select:** `text`
> ---
> ## 5) Grading Configuration
> - **Grade direction:** **Maximize**
> - **Theoretical minimum:** `0`
> - **Theoretical maximum:** `1`
> ---
> ## 6) Grading Script
> **Select:** `Custom`
> ```python
> import pandas as pd
> import numpy as np
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> """
> Score a submission against ground truth answers.
> Args:
> submission: The agent's predictions (loaded from submission.csv)
> answers: Ground truth labels (loaded from private/answers.csv)
> Returns:
> A float score in [0.0, 1.0]. Higher is better.
> Macro-averaged F1 over the 8 redaction types (0..7).
> """
> try:
> if "redaction_id" not in submission.columns:
> return 0.0
> if "redaction_type" not in submission.columns:
> return 0.0
> if submission["redaction_id"].duplicated().any():
> return 0.0
> if answers["redaction_id"].duplicated().any():
> return 0.0
> if set(submission["redaction_id"]) != set(answers["redaction_id"]):
> return 0.0
> if len(submission) != len(answers):
> return 0.0
> ans = answers[["redaction_id", "redaction_type"]].copy()
> sub = submission[["redaction_id", "redaction_type"]].copy()
> merged = ans.merge(
> sub, on="redaction_id", how="left", suffixes=("_true", "_pred")
> )
> if len(merged) == 0:
> return 0.0
> if merged["redaction_type_pred"].isna().any():
> return 0.0
> try:
> y_true = merged["redaction_type_true"].astype(int).values
> y_pred = merged["redaction_type_pred"].astype(int).values
> except (ValueError, TypeError):
> return 0.0
> n_classes = 8
> if (y_pred < 0).any() or (y_pred >= n_classes).any():
> return 0.0
> f1s: list[float] = []
> for c in range(n_classes):
> tp = int(((y_pred == c) & (y_true == c)).sum())
> fp = int(((y_pred == c) & (y_true != c)).sum())
> fn = int(((y_pred != c) & (y_true == c)).sum())
> if tp + fp == 0:
> precision = 0.0
> else:
> precision = tp / (tp + fp)
> if tp + fn == 0:
> recall = 0.0
> else:
> recall = tp / (tp + fn)
> if precision + recall == 0:
> f1 = 0.0
> else:
> f1 = 2.0 * precision * recall / (precision + recall)
> f1s.append(f1)
> macro_f1 = float(np.mean(f1s))
> return float(max(0.0, min(1.0, macro_f1)))
> except Exception:
> return 0.0
> ```
> ---
> ## 7) Prepare Script
> ```python
> from pathlib import Path
> def prepare(raw: Path, public: Path, private: Path) -> None:
> """Split raw_data/redactions.csv into public/ and private/ splits.
> Split policy (high level)
> -------------------------
> - Rows flagged "mixed" in the `split_hint` column are stratified
> per-template into an 80 / 20 train / test partition.
> - Rows flagged "test_only_heldout" in `split_hint` are assigned
> entirely to the test partition (distribution shift; their
> template markers are not present in the training split).
> - Adversarial rows (where the surface prefix phrase is
> deliberately mismatched to the true label under that row's
> template) are left in place in both partitions.
> Columns written to public/
> --------------------------
> public/train.csv            -- redaction_id, passage, redaction_type
> public/test.csv             -- redaction_id, passage
> public/sample_submission.csv-- redaction_id, redaction_type
> (constant 0; macro-F1 ~ 0.054)
> Columns written to private/
> ---------------------------
> private/answers.csv         -- redaction_id, redaction_type
> Organiser-side columns (template_id, true_type, is_adversarial,
> split_hint) are never written to the solver-facing files. They
> exist in raw_data/redactions.csv for organiser auditing only.
> """
> import random as _rnd
> import numpy as np
> import pandas as pd
> raw, public, private = Path(raw), Path(public), Path(private)
> public.mkdir(parents=True, exist_ok=True)
> private.mkdir(parents=True, exist_ok=True)
> df = pd.read_csv(raw / "redactions.csv")
> required = {"redaction_id", "passage", "template_id", "true_type",
> "is_adversarial", "split_hint"}
> missing = required - set(df.columns)
> if missing:
> raise ValueError(f"redactions.csv missing columns: {missing}")
> assert df["redaction_id"].is_unique, "duplicate redaction_id in raw"
> rng_split = _rnd.Random(271828182)
> np_rng = np.random.RandomState(77)
> held_mask = df["split_hint"] == "test_only_heldout"
> held = df.loc[held_mask].copy()
> mixed = df.loc[~held_mask].copy()
> train_rows: list[pd.DataFrame] = []
> test_rows: list[pd.DataFrame] = []
> for t, grp in mixed.groupby("template_id", sort=True):
> grp = grp.sort_values("redaction_id").reset_index(drop=True)
> n = len(grp)
> idx = list(range(n))
> rng_split.shuffle(idx)
> n_train = int(round(n * 0.80))
> train_rows.append(grp.iloc[idx[:n_train]])
> test_rows.append(grp.iloc[idx[n_train:]])
> train_df = pd.concat(train_rows, axis=0).reset_index(drop=True)
> test_mixed_df = pd.concat(test_rows, axis=0).reset_index(drop=True)
> test_df = pd.concat([test_mixed_df, held], axis=0).reset_index(drop=True)
> assert set(train_df["redaction_id"]) & set(test_df["redaction_id"]) == set(), (
> "train/test redaction_id overlap"
> )
> assert (
> set(train_df["redaction_id"]) | set(test_df["redaction_id"])
> ) == set(df["redaction_id"]), "lost or duplicated redaction_ids"
> all_new_ids = list(range(len(df)))
> np_rng.shuffle(all_new_ids)
> old_ids_ordered = (
> train_df["redaction_id"].tolist() + test_df["redaction_id"].tolist()
> )
> id_map = {old: new for old, new in zip(old_ids_ordered, all_new_ids)}
> train_df["redaction_id"] = train_df["redaction_id"].map(id_map)
> test_df["redaction_id"] = test_df["redaction_id"].map(id_map)
> train_df = train_df.sort_values("redaction_id").reset_index(drop=True)
> test_df = test_df.sort_values("redaction_id").reset_index(drop=True)
> train_out = train_df[["redaction_id", "passage", "true_type"]].rename(
> columns={"true_type": "redaction_type"}
> )
> train_out.to_csv(public / "train.csv", index=False)
> test_public = test_df[["redaction_id", "passage"]].copy()
> test_public.to_csv(public / "test.csv", index=False)
> sample = test_public[["redaction_id"]].copy()
> sample["redaction_type"] = 0
> sample.to_csv(public / "sample_submission.csv", index=False)
> answers = test_df[["redaction_id", "true_type"]].rename(
> columns={"true_type": "redaction_type"}
> )
> answers = answers.sort_values("redaction_id").reset_index(drop=True)
> answers.to_csv(private / "answers.csv", index=False)
> print(f"Train: {len(train_out)} rows")
> print(f"Test:  {len(test_public)} rows "
> f"(of which held-out-template: {int(held_mask.sum())}, "
> f"adversarial: {int(test_df['is_adversarial'].sum())})")
> print(f"Train class balance:\n"
> f"{train_out['redaction_type'].value_counts().sort_index()}")
> ```
> ---
> ## 8) Evaluation Rubrics
> ### Rubric 1
> - **Type:** DATA_HANDLING
> - **Importance:** REQUIRED
> - **Criteria:** Correctly parses the `passage` string and identifies at minimum the leading template marker (`<TPL-XY>`) and at least one prefix cue phrase per row, without crashing on any passage.
> - **Rationale:** The template marker is the only observable signal that identifies which hidden template governs a row's cue → type mapping. Solutions that discard it or fail to parse it lose the ability to condition predictions on the template at all.
> ### Rubric 2
> - **Type:** MODELING
> - **Importance:** REQUIRED
> - **Criteria:** The prediction pipeline produces a different output distribution across different template markers on the training set (i.e., the model is template-conditional, not a single template-agnostic decoder that ignores the `<TPL-XY>` marker token).
> - **Rationale:** The surface cue phrase resolves to different types under different template groups. A template-agnostic model caps around 0.23 macro-F1 on this task; template-conditional learning is required to exceed the baseline.
> ### Rubric 3
> - **Type:** MODELING
> - **Importance:** REQUIRED
> - **Criteria:** Produces valid non-null integer predictions in `[0, 7]` for every row in `test.csv`, with no missing `redaction_id` values.
> - **Rationale:** The strict grader returns 0.0 if any row is missing, any value is out of range, or any prediction is NaN. A submission that cannot be scored is indistinguishable from a zero-score solution.
> ### Rubric 4
> - **Type:** MODELING
> - **Importance:** RECOMMENDED
> - **Criteria:** Employs an explicit strategy for the held-out test rows whose template markers never appear in training — for example, structural pattern extraction from `test.csv`, unsupervised cue-phrase clustering, or a deliberate uniform / rank-transfer fallback. The strategy must be visible in the code, not an accidental side-effect of the default model.
> - **Rationale:** Roughly 40 % of test rows carry held-out marker tokens. Strong in-distribution baselines collapse on this slice. Any lift on held-out markers is the single largest source of human-agent gap.
> ### Rubric 5
> - **Type:** TRAINING
> - **Importance:** RECOMMENDED
> - **Criteria:** Validates the model on a held-out slice of `train.csv` whose template markers or passage structures differ from the slice used to fit parameters — not a uniform random 10 % split — before generating final test predictions.
> - **Rationale:** A uniform random validation split understates the held-out-marker risk. A template-disjoint validation split surfaces the held-out-generalisation problem during development rather than at scoring time.
> ### Rubric 6
> - **Type:** MODELING
> - **Importance:** RECOMMENDED
> - **Criteria:** Does not take the prefix cue phrase as unconditional evidence for a single tag; the prediction for a given cue phrase varies across templates in training data, and the training loss or decoding procedure explicitly tolerates cue-label mismatch on ~ 12 % of rows.
> - **Rationale:** ~ 12 % of rows are adversarial — the cue phrase was deliberately chosen to resolve to the wrong tag under that row's template. A solver that always trusts the cue loses the adversarial bucket entirely.
> ### Rubric 7
> - **Type:** CODE_QUALITY
> - **Importance:** UNIVERSAL
> - **Criteria:** Does not read, peek at, or use `private/answers.csv` anywhere in the pipeline, and does not train on the test passages.
> - **Rationale:** Any use of the ground-truth test labels produces inflated scores that do not reflect genuine capability. Training on test passages without labels is permissible; training *with* test labels is not.

Inspiration note: Useful as an NLP benchmark pattern with rich text inputs, a clear prediction column, and room for semantic reasoning beyond keywords.

## Synthetic Annotator Consensus Prediction_approved
- Challenge URL: https://drive.google.com/drive/folders/1NIRUX2BYfTRjaikjJFeqYeBWHBe7ad2V
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: NLP (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: Accepted/approved from Drive folder name
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: See description if specified
- Tags: Not shown/captured
- Best/top context found: Google Drive: Drive folder 2 / inferred / Synthetic Annotator Consensus Prediction_approved

Full challenge description from Drive:

> # Challenge creation form — fill-in
> **Platform status:** **Approved** — *Robust Ordinal State Inference Under Multi-Channel Corruption* (full title: Synthetic Robust Ordinal State Inference Under Multi-Channel Corruption).
> Tie this challenge to the **accepted dataset**: Synthetic Multi-Channel Ordinal Telemetry Records.
> ---
> ## 1) Difficulty
> **Select:** **Hard**
> ---
> ## 2) Challenge Title
> ```
> Synthetic Robust Ordinal State Inference Under Multi-Channel Corruption
> ```
> ---
> ## 3) Problem Description
> # Synthetic Robust Ordinal State Inference Under Multi-Channel Corruption
> ## Overview
> This is an **LLM Evaluation** challenge that models the problem of **determining the true quality level of LLM-generated responses when multiple automated scoring pipelines disagree, some pipelines are unreliable, and a fraction actively produce misleading quality assessments with inflated confidence**. Unlike standard LLM evaluation benchmarks that assume a single reliable judge, this challenge requires robust ordinal inference from multiple corrupted, sparse, and adversarially manipulated scoring channels.
> The dataset simulates 12,000 LLM-generated response items, each assessed by a subset of 600 independent scoring channels (automated evaluation pipelines with distinct internal configurations). Each channel produces an ordinal quality reading (0–5) accompanied by a **self-reported confidence score**, collected under one of **4 evaluation contexts** (representing different prompt categories or evaluation protocols). Channels belong to one of **5 hierarchical source groups** reflecting different pipeline architectures. A separate expert adjudication process established a **reference quality level** for each item.
> Each channel's scoring fidelity depends on an unobserved latent property of the response being evaluated — creating a **channel × item-property interaction** that cannot be captured by per-channel quality metrics. This models the real-world phenomenon where an automated LLM judge may score technical content accurately but struggle with creative writing, or vice versa.
> Your task: predict the reference quality level for each test item, given its anonymized feature vector, the channel profiles, and a **severely reduced set of channel readings** (2–3 per test item, compared to 5–8 per training item).
> **What makes this problem uniquely challenging:**
> - **Adversarial confidence manipulation**: approximately 5% of test readings are **injected spurious scores from channels not originally assigned to those items**. These corrupted readings carry **deliberately inflated confidence scores** (0.78–0.96), designed to appear more trustworthy than genuine readings. Naively trusting high-confidence readings degrades performance — the confidence signal is an **adversarial trap** that must be detected and mitigated.
> - **Channel × item-property interaction**: the same scoring channel may produce accurate quality assessments for items with certain latent characteristics and severely degraded assessments for others. This non-separable interaction means per-channel reliability estimates are insufficient — the model must jointly reason about channel profiles and item feature vectors.
> - **Asymmetric density transfer**: training items have 5–8 readings each while test items have only 2–3. Models must generalize from a high-density training regime to an extremely sparse test regime. Feature-space proximity between training and test items provides a potential cross-item transfer signal.
> - **Multi-context evaluation variation**: readings were collected under 4 different evaluation contexts (`reading_context` 0–3). Channel scoring fidelity may vary across contexts, adding a third interaction dimension.
> - **Hierarchical source structure**: channels are grouped into 5 source groups reflecting different pipeline architectures. Group membership partially predicts fidelity patterns but the relationship is non-trivial and interacts with item properties.
> - **Decoy feature dimensions**: both item and channel feature vectors contain uninformative dimensions mixed with genuine ones. Feature selection is part of the challenge.
> - **Irreducible reference noise**: ~8% of reference levels reflect genuine expert disagreement, capping theoretical performance.
> ## Evaluation
> Submissions are scored using **Quadratic Weighted Kappa (QWK)**, which treats the ordinal states 0–5 as an ordered scale and penalizes predictions far from the reference more heavily than near-misses. **Higher is better.** Minimum: 0.0, Maximum: 1.0.
> ## Dataset
> - `train_readings.csv` — 62,448 training scoring channel outputs: item_id (int), source_id (int), reading (int, ordinal quality 0–5), confidence (float, self-reported reading confidence 0.05–0.99), reading_context (int, evaluation context 0–3)
> - `test_readings.csv` — ~6,300 test scoring channel outputs: same columns, only 2–3 readings per item plus ~5% injected high-confidence spurious readings
> - `train_labels.csv` — 9,600 rows: item_id (int), reference_level (int, expert-adjudicated quality level 0–5)
> - `items.csv` — 12,000 response items: item_id (int), plus 12 anonymized numeric feature columns (x_00 through x_11, float)
> - `sources.csv` — 600 scoring channels: source_id (int), plus 11 anonymized numeric feature columns (e_00 through e_10, float), source_group (int, channel group 0–4)
> - `sample_submission.csv` — 2,400 rows: item_id (int), reference_level (int, baseline prediction). Shows the required submission format.
> ### Feature Details
> | Column | Type | Description |
> |--------|------|-------------|
> | item_id | int | Unique response item identifier |
> | source_id | int | Unique scoring channel identifier |
> | reading | int | Ordinal quality reading produced by the channel (0–5) |
> | confidence | float | Self-reported reading confidence (0.05–0.99). Caution: spurious readings carry inflated confidence. |
> | reading_context | int | Evaluation context under which the reading was produced (0–3) |
> | reference_level | int | Ground-truth quality level from expert adjudication (0–5, train only) |
> | x_00 through x_11 | float | Anonymized item feature attributes (mix of informative and decoy) |
> | e_00 through e_10 | float | Anonymized channel profile attributes (mix of informative and decoy) |
> | source_group | int | Hierarchical channel group assignment (0–4) |
> ## Submission
> Submit a CSV file with exactly 2,400 rows (one per test item), a header row, and two columns:
> | Column | Type | Description |
> |--------|------|-------------|
> | item_id | int | Item identifier from test_readings.csv |
> | reference_level | int | Predicted quality level (integer 0–5) |
> **Example of a correctly formatted submission file:**
> item_id,reference_level
> 3,4
> 7,2
> 15,5
> 22,1
> ...
> ---
> ## 4) Tags
> **Select:** `feature-engineering`
> ---
> ## 5) Grading Configuration
> - **Grade direction:** **Maximize**
> - **Theoretical minimum:** `0`
> - **Theoretical maximum:** `1`
> ---
> ## 6) Grading Script
> **Select:** `Custom`
> ```python
> import pandas as pd
> import numpy as np
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> """
> Score a submission against ground truth answers.
> Args:
> submission: The agent's predictions (loaded from submission.csv)
> answers: Ground truth labels (loaded from private/answers.csv)
> Returns:
> A float score between 0.0 and 1.0. Higher is better.
> Quadratic Weighted Kappa on ordinal reference levels.
> """
> try:
> if "item_id" not in submission.columns or "reference_level" not in submission.columns:
> return 0.0
> if submission["item_id"].duplicated().any():
> return 0.0
> if answers["item_id"].duplicated().any():
> return 0.0
> ans_cols = answers[["item_id", "reference_level"]].copy()
> sub_cols = submission[["item_id", "reference_level"]].copy()
> merged = ans_cols.merge(
> sub_cols, on="item_id", how="left", suffixes=("_true", "_pred")
> )
> if len(merged) == 0:
> return 0.0
> if merged["reference_level_pred"].isna().any():
> return 0.0
> if set(submission["item_id"]) != set(answers["item_id"]) or len(submission) != len(answers):
> return 0.0
> y_true = merged["reference_level_true"].astype(int).values
> y_pred = merged["reference_level_pred"].astype(int).values
> n_classes = 6
> conf = np.zeros((n_classes, n_classes), dtype=float)
> for t, p in zip(y_true, y_pred):
> t_c = min(max(int(t), 0), n_classes - 1)
> p_c = min(max(int(p), 0), n_classes - 1)
> conf[t_c, p_c] += 1.0
> w = np.zeros((n_classes, n_classes), dtype=float)
> for i in range(n_classes):
> for j in range(n_classes):
> w[i, j] = ((i - j) ** 2) / ((n_classes - 1) ** 2)
> row_sum = conf.sum(axis=1)
> col_sum = conf.sum(axis=0)
> n = conf.sum()
> if n == 0:
> return 0.0
> expected = np.outer(row_sum, col_sum) / n
> num = (w * conf).sum()
> den = (w * expected).sum()
> if den == 0:
> return 1.0
> qwk = 1.0 - num / den
> return float(max(0.0, qwk))
> except Exception:
> return 0.0
> ```
> ---
> ## 7) Prepare Script
> ```python
> from pathlib import Path
> def prepare(raw: Path, public: Path, private: Path) -> None:
> import random as _rnd
> import numpy as np
> import pandas as pd
> raw, public, private = Path(raw), Path(public), Path(private)
> items = pd.read_csv(raw / "items.csv")
> annotators = pd.read_csv(raw / "annotators.csv")
> annotations = pd.read_csv(raw / "annotations.csv")
> consensus = pd.read_csv(raw / "consensus.csv")
> rng = _rnd.Random(314159265)
> np_rng = np.random.RandomState(77)
> all_items = sorted(items["item_id"].tolist())
> rng_split = _rnd.Random(271828182)
> rng_split.shuffle(all_items)
> split_idx = int(len(all_items) * 0.8)
> train_ids = set(all_items[:split_idx])
> test_ids = set(all_items[split_idx:])
> item_feat_cols = sorted([c for c in items.columns if c.startswith("if_")])
> n_real_if = len(item_feat_cols)
> n_decoy_if = 4
> all_if_labels = [f"x_{i:02d}" for i in range(n_real_if + n_decoy_if)]
> rng.shuffle(all_if_labels)
> if_rename = {item_feat_cols[i]: all_if_labels[i] for i in range(n_real_if)}
> items = items.rename(columns=if_rename)
> items = items.drop(columns=["topic", "true_label"])
> n_items_total = len(items)
> for j in range(n_real_if, n_real_if + n_decoy_if):
> items[all_if_labels[j]] = np_rng.normal(0, 1, n_items_total).round(4)
> ann_feat_cols = sorted([c for c in annotators.columns if c.startswith("af_")])
> n_real_af = len(ann_feat_cols)
> n_decoy_af = 3
> all_af_labels = [f"e_{i:02d}" for i in range(n_real_af + n_decoy_af)]
> rng.shuffle(all_af_labels)
> af_rename = {ann_feat_cols[i]: all_af_labels[i] for i in range(n_real_af)}
> annotators = annotators.rename(columns=af_rename)
> n_ann_total = len(annotators)
> for j in range(n_real_af, n_real_af + n_decoy_af):
> annotators[all_af_labels[j]] = np_rng.normal(0, 1, n_ann_total).round(4)
> grp_feat = annotators[all_af_labels[1]].values
> boundaries = np.percentile(grp_feat, [20, 40, 60, 80])
> annotators["source_group"] = np.digitize(grp_feat, boundaries).astype(int)
> annotators = annotators.rename(columns={"annotator_id": "source_id"})
> annotations = annotations.rename(columns={"annotator_id": "source_id"})
> old_ids = sorted(annotators["source_id"].tolist())
> new_ids = list(range(len(old_ids)))
> rng.shuffle(new_ids)
> id_map = {old_ids[i]: new_ids[i] for i in range(len(old_ids))}
> annotators["source_id"] = annotators["source_id"].map(id_map)
> annotations["source_id"] = annotations["source_id"].map(id_map)
> annotations = annotations.rename(columns={"label": "reading"})
> train_ann = annotations[annotations["item_id"].isin(train_ids)].copy()
> test_ann_full = annotations[annotations["item_id"].isin(test_ids)].copy()
> test_ann_rows = []
> for item_id in sorted(test_ids):
> item_anns = test_ann_full[test_ann_full["item_id"] == item_id]
> n_keep = rng.randint(2, 3)
> n_keep = min(n_keep, len(item_anns))
> indices = sorted(item_anns.index.tolist())
> rng.shuffle(indices)
> kept = indices[:n_keep]
> test_ann_rows.append(item_anns.loc[kept])
> test_ann = pd.concat(test_ann_rows, ignore_index=True)
> np_rng_conf = np.random.RandomState(999)
> ann_feat_lookup = annotators.set_index("source_id")[all_af_labels[0]]
> for df_ref in [train_ann, test_ann]:
> base = df_ref["source_id"].map(ann_feat_lookup).values.astype(float)
> conf = 0.5 + 0.3 * np.tanh(base * 0.6)
> conf = conf + np_rng_conf.normal(0, 0.08, len(df_ref))
> df_ref["confidence"] = np.clip(conf, 0.05, 0.99).round(3)
> np_rng_noise = np.random.RandomState(555)
> n_noise = int(len(test_ann) * 0.05)
> noise_items = np_rng_noise.choice(sorted(test_ids), n_noise)
> noise_sources = np_rng_noise.choice(sorted(annotators["source_id"]), n_noise)
> noise_readings = np_rng_noise.randint(0, 6, n_noise)
> noise_conf = np_rng_noise.uniform(0.78, 0.96, n_noise).round(3)
> noise_df = pd.DataFrame({
> "item_id": noise_items,
> "source_id": noise_sources,
> "reading": noise_readings,
> "confidence": noise_conf,
> })
> test_ann = pd.concat([test_ann, noise_df], ignore_index=True)
> test_ann = test_ann.drop_duplicates(
> subset=["item_id", "source_id"], keep="first"
> )
> test_ann = test_ann.sort_values("item_id").reset_index(drop=True)
> train_ann = train_ann.sort_values("item_id").reset_index(drop=True)
> np_rng_ctx = np.random.RandomState(777)
> train_ann["reading_context"] = np_rng_ctx.randint(0, 4, len(train_ann))
> test_ann["reading_context"] = np_rng_ctx.randint(0, 4, len(test_ann))
> consensus = consensus.rename(columns={"consensus_label": "reference_level"})
> train_labels = consensus[consensus["item_id"].isin(train_ids)].copy()
> test_labels = consensus[consensus["item_id"].isin(test_ids)].copy()
> train_labels = train_labels.sort_values("item_id").reset_index(drop=True)
> test_labels = test_labels.sort_values("item_id").reset_index(drop=True)
> test_modes = test_ann.groupby("item_id")["reading"].agg(
> lambda x: int(x.mode().iloc[0])
> ).reset_index()
> test_modes.columns = ["item_id", "reference_level"]
> sample_sub = test_modes.sort_values("item_id").reset_index(drop=True)
> items = items.sort_values("item_id").reset_index(drop=True)
> annotators = annotators.sort_values("source_id").reset_index(drop=True)
> public.mkdir(parents=True, exist_ok=True)
> private.mkdir(parents=True, exist_ok=True)
> train_ann.to_csv(public / "train_readings.csv", index=False)
> test_ann.to_csv(public / "test_readings.csv", index=False)
> train_labels.to_csv(public / "train_labels.csv", index=False)
> items.to_csv(public / "items.csv", index=False)
> annotators.to_csv(public / "sources.csv", index=False)
> sample_sub.to_csv(public / "sample_submission.csv", index=False)
> test_labels.to_csv(private / "answers.csv", index=False)
> ```
> ---
> ## 8) Evaluation Rubrics
> ### Rubric 1
> - **Type:** DATA_HANDLING
> - **Importance:** REQUIRED
> - **Criteria:** Correctly loads and links all provided CSV files without data loss, duplication, or column misalignment.
> - **Rationale:** The dataset spans multiple tables with different schemas. Incorrect linking produces corrupt inputs.
> ### Rubric 2
> - **Type:** DATA_HANDLING
> - **Importance:** REQUIRED
> - **Criteria:** Handles variable-length inputs per item (items may have different numbers of associated readings) without crashing or producing NaN predictions.
> - **Rationale:** Items have different amounts of available information. Fixed-length assumptions will cause failures.
> ### Rubric 3
> - **Type:** CODE_QUALITY
> - **Importance:** REQUIRED
> - **Criteria:** Produces a valid submission CSV with exactly 2,400 rows, columns item_id and reference_level, where reference_level is an integer in [0, 5].
> - **Rationale:** Incorrectly formatted or incomplete submissions will fail the grader or score zero.
> ### Rubric 4
> - **Type:** MODELING
> - **Importance:** REQUIRED
> - **Criteria:** Achieves QWK above the sample submission baseline on the test set, producing predictions that span at least 4 of the 6 ordinal levels.
> - **Rationale:** A solution that predicts a single constant or near-constant value across all items demonstrates no meaningful modeling, even if QWK is non-negative.
> ### Rubric 5
> - **Type:** MODELING
> - **Importance:** REQUIRED
> - **Criteria:** Incorporates information from at least two of the provided data tables (beyond just train_labels.csv) in the prediction pipeline.
> - **Rationale:** Predictions based solely on readings or solely on item features ignore the multi-table structure that is central to the problem.
> ### Rubric 6
> - **Type:** MODELING
> - **Importance:** RECOMMENDED
> - **Criteria:** Prediction quality does not catastrophically degrade for items where available readings disagree with each other (i.e., high variance in readings for a single item).
> - **Rationale:** Items with conflicting readings are the hardest cases. A robust solution must handle disagreement rather than failing silently.
> ### Rubric 7
> - **Type:** AGENT_BEHAVIOR
> - **Importance:** RECOMMENDED
> - **Criteria:** Evaluates intermediate predictions on a held-out portion of training data before generating final test predictions.
> - **Rationale:** Without internal validation, there is no way to assess whether the model is functioning correctly before submission.
> ### Rubric 8
> - **Type:** CODE_QUALITY
> - **Importance:** UNIVERSAL
> - **Criteria:** Does not access test set reference levels or leak private answer data into the prediction pipeline.
> - **Rationale:** Using ground-truth test labels produces inflated scores that do not reflect genuine capability.

Inspiration note: Useful as an NLP benchmark pattern with rich text inputs, a clear prediction column, and room for semantic reasoning beyond keywords.

## less novel Synthetic Context-Driven Slate Selection
- Challenge URL: https://drive.google.com/drive/folders/1mYqcOS4hpgDylbAj3wSIsHjFoRjBWpkm
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: NLP (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: Accepted/approved example from shared Drive folder
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: Not shown/captured
- Tags: Not shown/captured
- Best/top context found: less_novel_Synthetic Context-Driven Slate Selection from shared Google Drive folder

Full challenge description from Drive:

> # Challenge creation form — fill-in
> Tie this challenge to the **accepted dataset**: Synthetic Contextual Item Selection Logs with Preference Dynamics.
> ---
> ## 1) Difficulty
> **Select:** **Hard**
> ---
> ## 2) Challenge Title
> ```
> Synthetic Context-Driven Slate Selection
> ```
> ---
> ## 3) Problem Description
> # Synthetic Context-Driven Slate Selection
> ## Overview
> This challenge requires **predicting which item a user will select from a personalized candidate slate**, given the user's profile, item attributes, and contextual conditions at the time of the query. Each query presents a user with a slate of 10 candidate items under specific contextual conditions (6 anonymized context features). The task is to predict which one of the 10 candidates the user selects.
> The dataset contains 400 anonymized users, 800 anonymized items, and 20,000 selection queries split into 15,000 training queries and 5,000 test queries. Users are described by 7 anonymized profile features (`UF_00` through `UF_06`), items by 10 anonymized attribute features (`IF_00` through `IF_09`), and each query includes 6 anonymized context features (`C_00` through `C_05`). All original feature names have been removed.
> **What makes this problem challenging:**
> - **Context-dependent preferences**: the same user may prefer entirely different items depending on the contextual conditions of the query. User preferences are not static — they shift across different context combinations. Identifying which context features drive preference shifts, and how, is central to the task.
> - **Slate-specific choices**: each query has a unique slate of 10 candidates. The model must reason about relative item appeal within each specific candidate set, not just global item popularity.
> - **Mixed entity features**: user profiles, item attributes, and query context must all be combined. Some features within each entity carry signal; others do not.
> - **Noisy selections**: approximately 12% of selections are not preference-driven, capping theoretical accuracy at approximately 0.88.
> Your task: for each of the 5,000 test queries, predict the `chosen_item_id` (one of the 10 candidate items listed for that query).
> ## Evaluation
> Submissions are scored using **accuracy** (fraction of correctly predicted selected item IDs). **Higher is better.** Minimum: 0.0, Maximum: 1.0.
> ## Dataset
> - `users.csv` — 400 user profiles: user_id (int), UF_00 through UF_06 (7 features, mix of float and int)
> - `items.csv` — 800 item descriptions: item_id (int), IF_00 through IF_09 (10 features, mix of float and int)
> - `train_queries.csv` — 15,000 training queries: query_id (int), user_id (int), C_00 through C_05 (6 context features, int)
> - `train_candidates.csv` — 150,000 rows (10 per query): query_id (int), item_id (int) — lists the 10 candidate items for each training query
> - `train_labels.csv` — 15,000 rows: query_id (int), chosen_item_id (int) — the item selected in each training query
> - `test_queries.csv` — 5,000 test queries: query_id (int), user_id (int), C_00 through C_05 (same structure as train)
> - `test_candidates.csv` — 50,000 rows (10 per query): query_id (int), item_id (int) — the 10 candidates for each test query
> - `sample_submission.csv` — 5,000 rows: query_id (int), chosen_item_id (int, placeholder 0). Shows the required format.
> ### Feature Details
> **User features (users.csv)**
> | Column | Type | Description |
> |--------|------|-------------|
> | user_id | int | Unique user identifier (0–399) |
> | UF_00 | float | Anonymized user feature |
> | UF_01 | int | Anonymized user feature (6 levels: 0–5) |
> | UF_02 | float | Anonymized user feature |
> | UF_03 | int | Anonymized user feature (4 levels: 0–3) |
> | UF_04 | float | Anonymized user feature |
> | UF_05 | float | Anonymized user feature |
> | UF_06 | float | Anonymized user feature |
> **Item features (items.csv)**
> | Column | Type | Description |
> |--------|------|-------------|
> | item_id | int | Unique item identifier (0–799) |
> | IF_00 | float | Anonymized item feature |
> | IF_01 | float | Anonymized item feature |
> | IF_02 | float | Anonymized item feature |
> | IF_03 | int | Anonymized item feature (5 levels: 0–4) |
> | IF_04 | int | Anonymized item feature (18 levels: 0–17) |
> | IF_05 | float | Anonymized item feature |
> | IF_06 | float | Anonymized item feature |
> | IF_07 | float | Anonymized item feature |
> | IF_08 | float | Anonymized item feature |
> | IF_09 | float | Anonymized item feature |
> **Context features (train_queries.csv / test_queries.csv)**
> | Column | Type | Description |
> |--------|------|-------------|
> | query_id | int | Unique query identifier |
> | user_id | int | User presented with the slate |
> | C_00 | int | Anonymized context feature (6 levels: 0–5) |
> | C_01 | int | Anonymized context feature (4 levels: 0–3) |
> | C_02 | int | Anonymized context feature (3 levels: 0–2) |
> | C_03 | int | Anonymized context feature (10 levels: 0–9) |
> | C_04 | int | Anonymized context feature (120 levels: 1–120) |
> | C_05 | int | Anonymized context feature (5 levels: 0–4) |
> ## Submission
> Submit a CSV file with the following format:
> | Column | Type | Description |
> |--------|------|-------------|
> | query_id | int | Query identifier from test_queries.csv |
> | chosen_item_id | int | Predicted item_id selected by the user (must be one of the 10 candidates for that query) |
> **Requirements:**
> - Must contain exactly 5,000 rows (one per test query).
> - Include a header row.
> - Each `chosen_item_id` must be a valid `item_id` from the corresponding query's candidate slate in test_candidates.csv.
> **Example of a correctly formatted submission file:**
> ```
> query_id,chosen_item_id
> 3,142
> 8,505
> 14,27
> 19,688
> 24,311
> ```
> ---
> ## 4) Tags
> **Select:** `feature-engineering`
> ---
> ## 5) Grading Configuration
> - **Grade direction:** Maximize
> - **Theoretical minimum:** 0
> - **Theoretical maximum:** 1.0
> ---
> ## 6) Grading Script
> ```python
> import pandas as pd
> import numpy as np
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> """
> Score a submission against ground truth answers.
> Args:
> submission: The agent's predictions (loaded from submission.csv).
> answers: Ground truth labels (loaded from private/answers.csv).
> Returns:
> A float score in [0.0, 1.0]. Higher is better (accuracy).
> Returns 0.0 for invalid or malformed submissions.
> """
> try:
> if "query_id" not in submission.columns or "chosen_item_id" not in submission.columns:
> return 0.0
> if submission["query_id"].duplicated().any():
> return 0.0
> if answers["query_id"].duplicated().any():
> return 0.0
> if (
> set(submission["query_id"]) != set(answers["query_id"])
> or len(submission) != len(answers)
> ):
> return 0.0
> merged = answers.merge(
> submission, on="query_id", how="left", suffixes=("_true", "_pred")
> )
> if len(merged) == 0:
> return 0.0
> col_true = "chosen_item_id_true" if "chosen_item_id_true" in merged.columns else "chosen_item_id"
> col_pred = "chosen_item_id_pred" if "chosen_item_id_pred" in merged.columns else "chosen_item_id"
> if merged[col_pred].isna().any():
> return 0.0
> accuracy = float((merged[col_true] == merged[col_pred]).mean())
> if np.isnan(accuracy):
> return 0.0
> return accuracy
> except Exception:
> return 0.0
> ```
> ---
> ## 7) Prepare Script
> ```python
> from pathlib import Path
> def prepare(raw: Path, public: Path, private: Path) -> None:
> import random as _rnd
> import numpy as np
> import pandas as pd
> raw, public, private = Path(raw), Path(public), Path(private)
> users = pd.read_csv(raw / "users.csv")
> items = pd.read_csv(raw / "items.csv")
> queries = pd.read_csv(raw / "queries.csv")
> SPLIT_SEED = 271828
> TRAIN_FRAC = 0.75
> np_rng = np.random.RandomState(SPLIT_SEED)
> # ---- Anonymize user columns ----
> u_cols = [c for c in users.columns if c != "user_id"]
> rng_u = _rnd.Random(314159)
> shuf_u = list(u_cols)
> rng_u.shuffle(shuf_u)
> u_map = {orig: f"UF_{i:02d}" for i, orig in enumerate(shuf_u)}
> users = users.rename(columns=u_map)
> users["UF_06"] = np_rng.normal(0, 1, len(users)).round(3)
> # ---- Anonymize item columns ----
> i_cols = [c for c in items.columns if c != "item_id"]
> rng_i = _rnd.Random(161803)
> shuf_i = list(i_cols)
> rng_i.shuffle(shuf_i)
> i_map = {orig: f"IF_{i:02d}" for i, orig in enumerate(shuf_i)}
> items = items.rename(columns=i_map)
> items["IF_08"] = np_rng.normal(0, 1, len(items)).round(3)
> items["IF_09"] = np_rng.uniform(0, 1, len(items)).round(3)
> # ---- Anonymize context columns ----
> ctx_orig = ["time_slot", "device_code", "day_type",
> "referral_code", "session_length", "entry_point"]
> rng_c = _rnd.Random(141421)
> shuf_c = list(ctx_orig)
> rng_c.shuffle(shuf_c)
> c_map = {orig: f"C_{i:02d}" for i, orig in enumerate(shuf_c)}
> queries = queries.rename(columns=c_map)
> # ---- Split queries 75/25 ----
> all_qids = sorted(queries["query_id"].tolist())
> rng_split = _rnd.Random(SPLIT_SEED)
> rng_split.shuffle(all_qids)
> split_pt = int(len(all_qids) * TRAIN_FRAC)
> train_qids = set(all_qids[:split_pt])
> test_qids = set(all_qids[split_pt:])
> train_q = queries[queries["query_id"].isin(train_qids)].copy()
> test_q = queries[queries["query_id"].isin(test_qids)].copy()
> train_q = train_q.sort_values("query_id").reset_index(drop=True)
> test_q = test_q.sort_values("query_id").reset_index(drop=True)
> # ---- Expand candidates into separate table ----
> def _expand(df):
> exp = df[["query_id", "candidates"]].copy()
> exp["candidates"] = exp["candidates"].astype(str).str.split("|")
> exp = exp.explode("candidates").rename(columns={"candidates": "item_id"})
> exp["item_id"] = exp["item_id"].astype(int)
> return exp.reset_index(drop=True)
> train_cands = _expand(train_q)
> test_cands = _expand(test_q)
> ctx_new = sorted(c_map.values())
> # ---- Write ----
> public.mkdir(parents=True, exist_ok=True)
> private.mkdir(parents=True, exist_ok=True)
> users.to_csv(public / "users.csv", index=False)
> items.to_csv(public / "items.csv", index=False)
> train_q[["query_id", "user_id"] + ctx_new].to_csv(
> public / "train_queries.csv", index=False
> )
> train_cands.to_csv(public / "train_candidates.csv", index=False)
> train_q[["query_id", "chosen_item_id"]].to_csv(
> public / "train_labels.csv", index=False
> )
> test_q[["query_id", "user_id"] + ctx_new].to_csv(
> public / "test_queries.csv", index=False
> )
> test_cands.to_csv(public / "test_candidates.csv", index=False)
> sample = test_q[["query_id"]].copy()
> sample["chosen_item_id"] = 0
> sample.to_csv(public / "sample_submission.csv", index=False)
> test_q[["query_id", "chosen_item_id"]].to_csv(
> private / "answers.csv", index=False
> )
> print(f"Train queries: {len(train_q)}")
> print(f"Test queries:  {len(test_q)}")
> print(f"Train candidates rows: {len(train_cands)}")
> print(f"Test candidates rows:  {len(test_cands)}")
> print(f"Users: {len(users)}, Items: {len(items)}")
> ```
> ---
> ## 8) Evaluation Rubrics
> ### Rubric 1
> - **Type:** DATA_HANDLING
> - **Importance:** REQUIRED
> - **Criteria:** Correctly loads and joins the multi-file dataset (user profiles, item attributes, query contexts, candidate slates, and training labels) without data loss or type errors.
> - **Rationale:** The challenge requires combining information across 5+ CSV files with different schemas and join keys. Failure to parse or join any file correctly makes meaningful modeling impossible.
> ### Rubric 2
> - **Type:** CODE_QUALITY
> - **Importance:** REQUIRED
> - **Criteria:** Produces a valid submission CSV with exactly 5,000 rows containing columns query_id and chosen_item_id, where each chosen_item_id is a valid item_id from the candidate slate of the corresponding query.
> - **Rationale:** Missing columns, wrong row counts, or item IDs not in the candidate slate will score zero or produce meaningless accuracy.
> ### Rubric 3
> - **Type:** MODELING
> - **Importance:** REQUIRED
> - **Criteria:** Achieves accuracy above the random-from-slate baseline (~0.10) on the test set, producing query-specific item selections rather than a constant or random choice.
> - **Rationale:** Random selection from each slate of 10 candidates yields ~10% accuracy and demonstrates no useful learning from the training data.
> ### Rubric 4
> - **Type:** MODELING
> - **Importance:** RECOMMENDED
> - **Criteria:** Incorporates both user profile features and item attribute features when scoring candidate items, rather than relying solely on global item popularity.
> - **Rationale:** Global item popularity achieves ~0.31 accuracy. Modeling user-item compatibility is necessary to exceed this ceiling.
> ### Rubric 5
> - **Type:** CODE_QUALITY
> - **Importance:** UNIVERSAL
> - **Criteria:** Does not access private answer data or test set ground-truth chosen_item_id values during the prediction pipeline.
> - **Rationale:** Using ground-truth test labels produces inflated scores that do not reflect genuine capability.

Inspiration note: Useful as an NLP benchmark pattern with rich text inputs, a clear prediction column, and room for semantic reasoning beyond keywords.

## Latent Selection Function Inference From Obfuscated Behavioral Traces accepted
- Challenge URL: https://drive.google.com/drive/folders/1mSiaPxJ3xKGkkD9_78eEDXHPU09ljOkK
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: NLP (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: Accepted (from Drive folder name)
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: Not shown/captured
- Tags: Not shown/captured
- Best/top context found: Latent Selection Function Inference From Obfuscated Behavioral Traces_accepted from shared Google Drive folder

Full challenge description from Drive:

> # Challenge creation form — fill-in
> Tie this challenge to the **accepted dataset**: Synthetic Session Behavioral Interaction Signal Logs.
> ---
> ## 1) Difficulty
> **Select:** **Hard**
> ---
> ## 2) Challenge Title
> ```
> Latent Selection Function Inference From Obfuscated Behavioral Traces
> ```
> ---
> ## 3) Problem Description
> # Latent Selection Function Inference From Obfuscated Behavioral Traces
> ## Overview
> This challenge requires **inferring a latent selection function from obfuscated multi-signal behavioral traces**. Each data record captures a user's interaction with an item during a session, but all signal names are anonymized, behavioral measurements have been statistically transformed (per-session z-scored, globally quantile-binned), and noise interactions have been injected. The task is to predict the **outcome of a hidden decision process** — which item was selected — given only the transformed signals, anonymized user profiles, and an obfuscated item catalog.
> The core difficulty lies in three interacting factors that, to our knowledge, have not been combined in a single prediction task before:
> 1. **Dual-regime decision process** — Approximately 20% of sessions follow a "passive interest" regime where the selected item is determined entirely by latent user-item feature compatibility (not by behavioral engagement signals). The remaining ~80% follow an "active engagement" regime where behavioral signals dominate. Participants must discover and model both regimes without explicit regime labels — a latent mixture that cannot be solved by any single-strategy model.
> 2. **Adversarial signal obfuscation** — All feature names are anonymous codes carrying no semantic meaning. Two behavioral signals have been per-session z-score normalized (destroying absolute scale) and globally quantile-binned (discretizing continuous values). User and item features have been independently noised and renamed. Additionally, ~1–3 noise interactions are injected per session, revisit sequences are merged for ~25% of sessions, and sequential positions are perturbed for ~20% of sessions.
> 3. **Cold-start inference** — ~15% of test users have no profile in the user table, requiring the model to infer the decision purely from within-session behavioral evidence for those cases.
> Unlike standard prediction tasks where feature semantics are known, this challenge requires jointly solving feature interpretation, regime discovery, and outcome prediction under adversarial obfuscation.
> ## Evaluation
> Submissions are scored using **accuracy** (fraction of correctly predicted selected item IDs). **Higher is better.** Minimum: 0.0, Maximum: 1.0, Random baseline: ~0.10.
> ## Dataset
> - `train_sessions.csv` — 12,000 training sessions (~210K rows): session_id (int), user_id (int), item_id (int), event_type (string, one of four interaction event codes), signal_1 (float, per-session normalized behavioral signal, zero-mean), signal_2 (int, binned behavioral signal 1–5), seq_pos (int, position in session, may be perturbed)
> - `train_labels.csv` — 12,000 rows: session_id (int), purchased_item_id (int)
> - `test_sessions.csv` — 3,000 test sessions (~53K rows): same columns as train_sessions.csv
> - `items.csv` — 500 items: item_id (int), cat_code (string, anonymized category CAT_01–CAT_20), tier_code (string, anonymized tier PT_V/W/X/Y/Z), if_1/if_2/if_3 (float, anonymized numeric features)
> - `users.csv` — ~2,700 users (some test users intentionally excluded): user_id (int), uf_1/uf_2/uf_3 (string, anonymized categorical features), uf_4/uf_5 (string, anonymized categorical features), uf_6/uf_7/uf_8 (float, anonymized continuous features)
> - `sample_submission.csv` — 3,000 rows: session_id (int), purchased_item_id (int, placeholder value 0). Shows the required submission format with one row per test session.
> ## Submission
> Submit a CSV file with exactly 3,000 rows (one per test session), a header row, and two columns:
> | Column | Type | Description |
> |--------|------|-------------|
> | session_id | int | Session identifier from test_sessions.csv |
> | purchased_item_id | int | Predicted purchased item_id (must be a valid item_id from items.csv) |
> **Example of a correctly formatted submission file:**
> session_id,purchased_item_id
> 3,42
> 8,305
> 14,127
> 19,88
> ...
> ---
> ## 4) Tags
> **Select:** `feature-engineering`
> ---
> ## 5) Grading Configuration
> - **Grade direction:** **Maximize**
> - **Theoretical minimum:** `0`
> - **Theoretical maximum:** `1`
> ---
> ## 6) Grading Script
> **Select:** `Custom`
> ```python
> import pandas as pd
> import numpy as np
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> try:
> if "session_id" not in submission.columns or "purchased_item_id" not in submission.columns:
> raise ValueError("Submission must have columns: session_id, purchased_item_id")
> if submission["session_id"].duplicated().any():
> raise ValueError("Submission contains duplicate session_id values")
> if answers["session_id"].duplicated().any():
> raise ValueError("Answers contains duplicate session_id values")
> if len(submission) != len(answers):
> raise ValueError(
> f"Submission must have exactly {len(answers)} rows, got {len(submission)}"
> )
> sub_ids = set(submission["session_id"])
> ans_ids = set(answers["session_id"])
> if sub_ids != ans_ids:
> missing = ans_ids - sub_ids
> extra = sub_ids - ans_ids
> if missing:
> raise ValueError(f"Submission missing session_ids: {len(missing)}")
> if extra:
> raise ValueError(f"Submission has extra session_ids: {len(extra)}")
> merged = answers.merge(
> submission, on="session_id", how="left",
> suffixes=("_true", "_pred")
> )
> if merged["purchased_item_id_pred"].isna().any():
> raise ValueError("Submission has missing predictions after merge")
> accuracy = (
> merged["purchased_item_id_true"] == merged["purchased_item_id_pred"]
> ).mean()
> score = float(accuracy)
> if np.isnan(score):
> return 0.0
> return score
> except ValueError:
> raise
> except Exception as e:
> raise RuntimeError(f"Grading failed: {e}") from e
> ```
> ---
> ## 7) Prepare Script
> ```python
> from pathlib import Path
> import hashlib
> import random as _rnd
> import numpy as np
> import pandas as pd
> from sklearn.model_selection import train_test_split
> def _det_seed(key: str) -> int:
> return int(hashlib.md5(key.encode()).hexdigest(), 16) % (2**32)
> def prepare(raw: Path, public: Path, private: Path) -> None:
> interactions = pd.read_csv(raw / "interactions.csv")
> items = pd.read_csv(raw / "items.csv")
> users = pd.read_csv(raw / "users.csv")
> purchases = pd.read_csv(raw / "purchases.csv")
> rng = _rnd.Random(_det_seed("prepare_42"))
> np_rng = np.random.RandomState(42)
> cat_ids = sorted(items["category"].unique())
> shuffled_cats = list(cat_ids)
> rng.shuffle(shuffled_cats)
> cat_map = {orig: f"CAT_{i:02d}" for i, orig in enumerate(shuffled_cats)}
> tier_ids = sorted(items["price_tier"].unique())
> tier_labels = ["PT_W", "PT_X", "PT_Y", "PT_Z", "PT_V"]
> rng.shuffle(tier_labels)
> tier_map = {orig: tier_labels[i] for i, orig in enumerate(tier_ids)}
> items["category"] = items["category"].map(cat_map)
> items["price_tier"] = items["price_tier"].map(tier_map)
> items["attr_1"] += np_rng.normal(0, 0.3, len(items))
> items["attr_2"] += np_rng.normal(0, 0.3, len(items))
> items["attr_3"] += np_rng.normal(0, 0.3, len(items))
> items = items.rename(columns={
> "attr_1": "if_1", "attr_2": "if_2", "attr_3": "if_3",
> "category": "cat_code", "price_tier": "tier_code",
> })
> items = items.round({"if_1": 3, "if_2": 3, "if_3": 3})
> users["pref_cat_1"] = users["pref_cat_1"].map(cat_map)
> users["pref_cat_2"] = users["pref_cat_2"].map(cat_map)
> users["pref_cat_3"] = users["pref_cat_3"].map(cat_map)
> users["tier_low"] = users["tier_low"].map(tier_map)
> users["tier_high"] = users["tier_high"].map(tier_map)
> users["pref_1"] += np_rng.normal(0, 0.4, len(users))
> users["pref_2"] += np_rng.normal(0, 0.4, len(users))
> users["pref_3"] += np_rng.normal(0, 0.4, len(users))
> users = users.rename(columns={
> "pref_cat_1": "uf_1", "pref_cat_2": "uf_2", "pref_cat_3": "uf_3",
> "tier_low": "uf_4", "tier_high": "uf_5",
> "pref_1": "uf_6", "pref_2": "uf_7", "pref_3": "uf_8",
> })
> users = users.round({"uf_6": 3, "uf_7": 3, "uf_8": 3})
> interactions["dwell_seconds"] = interactions.groupby(
> "session_id"
> )["dwell_seconds"].transform(
> lambda x: (x - x.mean()) / x.std() if x.std() > 0 else x * 0.0
> ).round(3)
> interactions["scroll_pct"] = pd.qcut(
> interactions["scroll_pct"], q=5, labels=[1, 2, 3, 4, 5], duplicates="drop"
> ).astype(int)
> all_item_ids = items["item_id"].tolist()
> noise_rows = []
> for sid in interactions["session_id"].unique():
> sess = interactions[interactions["session_id"] == sid]
> uid = sess["user_id"].iloc[0]
> max_pos = sess["position"].max()
> n_noise = rng.randint(1, 3)
> for j in range(n_noise):
> noise_rows.append({
> "session_id": sid,
> "user_id": uid,
> "item_id": rng.choice(all_item_ids),
> "action_type": "view",
> "dwell_seconds": round(np_rng.normal(0, 0.8), 3),
> "scroll_pct": rng.randint(1, 5),
> "position": max_pos + j + 1,
> })
> noise_df = pd.DataFrame(noise_rows)
> interactions = pd.concat([interactions, noise_df], ignore_index=True)
> merge_sessions = set()
> for sid in interactions["session_id"].unique():
> if _det_seed(f"merge_{sid}") % 100 < 25:
> merge_sessions.add(sid)
> merged_parts = []
> for sid, group in interactions.groupby("session_id"):
> if sid in merge_sessions:
> agg = group.groupby("item_id").agg({
> "session_id": "first", "user_id": "first",
> "action_type": "last", "dwell_seconds": "max",
> "scroll_pct": "max", "position": "max",
> }).reset_index()
> merged_parts.append(agg)
> else:
> merged_parts.append(group)
> interactions = pd.concat(merged_parts, ignore_index=True)
> perturbed_parts = []
> for sid, group in interactions.groupby("session_id"):
> if _det_seed(f"pos_{sid}") % 100 < 20:
> group = group.copy()
> positions = group["position"].values.copy()
> n = len(positions)
> for i in range(n):
> if rng.random() < 0.3:
> j = rng.randint(0, n - 1)
> positions[i], positions[j] = positions[j], positions[i]
> group["position"] = positions
> perturbed_parts.append(group)
> interactions = pd.concat(perturbed_parts, ignore_index=True)
> interactions = interactions.rename(columns={
> "dwell_seconds": "signal_1",
> "scroll_pct": "signal_2",
> "action_type": "event_type",
> "position": "seq_pos",
> })
> session_ids = sorted(purchases["session_id"].unique())
> train_sids, test_sids = train_test_split(
> session_ids, test_size=0.2, random_state=42
> )
> train_sids_set = set(train_sids)
> test_sids_set = set(test_sids)
> train_ints = interactions[interactions["session_id"].isin(train_sids_set)]
> test_ints = interactions[interactions["session_id"].isin(test_sids_set)]
> train_purchases = purchases[purchases["session_id"].isin(train_sids_set)]
> test_purchases = purchases[purchases["session_id"].isin(test_sids_set)]
> test_user_ids = test_ints["user_id"].unique()
> cold_users = set()
> for uid in test_user_ids:
> if _det_seed(f"cold_{uid}") % 100 < 15:
> cold_users.add(uid)
> users_public = users[~users["user_id"].isin(cold_users)]
> public.mkdir(parents=True, exist_ok=True)
> private.mkdir(parents=True, exist_ok=True)
> train_ints.to_csv(public / "train_sessions.csv", index=False)
> train_purchases.to_csv(public / "train_labels.csv", index=False)
> test_ints.to_csv(public / "test_sessions.csv", index=False)
> items.to_csv(public / "items.csv", index=False)
> users_public.to_csv(public / "users.csv", index=False)
> sample = test_purchases[["session_id"]].copy()
> sample["purchased_item_id"] = 0
> sample.to_csv(public / "sample_submission.csv", index=False)
> test_purchases.to_csv(private / "answers.csv", index=False)
> ```
> ---
> ## 8) Evaluation Rubrics
> ### Rubric 1
> - **Type:** DATA_HANDLING
> - **Importance:** REQUIRED
> - **Criteria:** Correctly loads and parses the multi-file dataset (session interactions, item catalog, user profiles, training labels) without data loss or encoding errors.
> - **Rationale:** The dataset spans multiple CSV files with mixed data types (integers, floats, categorical codes). Incorrect parsing or failed joins will produce broken predictions.
> ### Rubric 2
> - **Type:** CODE_QUALITY
> - **Importance:** REQUIRED
> - **Criteria:** Produces a valid submission CSV containing exactly 3,000 rows with columns `session_id` and `purchased_item_id`, where each `purchased_item_id` is a valid item_id.
> - **Rationale:** An incorrectly formatted submission will fail the grader. The agent must produce output matching the specified schema exactly.
> ### Rubric 3
> - **Type:** MODELING
> - **Importance:** REQUIRED
> - **Criteria:** Achieves accuracy meaningfully above random baseline (~0.10) on the test set.
> - **Rationale:** A solution scoring at or near 0.10 indicates no meaningful learning — functionally equivalent to random selection from each session's item set.
> ### Rubric 4
> - **Type:** AGENT_BEHAVIOR
> - **Importance:** RECOMMENDED
> - **Criteria:** Evaluates intermediate results on a validation split and iterates on the approach if initial accuracy is near baseline.
> - **Rationale:** Good engineering practice involves measuring progress and adjusting strategy when results are poor.
> ### Rubric 5
> - **Type:** CODE_QUALITY
> - **Importance:** UNIVERSAL
> - **Criteria:** Does not use test set labels or leak information from the private answers into the prediction pipeline.
> - **Rationale:** Using ground-truth test labels produces artificially inflated scores that do not reflect genuine model capability.

Inspiration note: Useful as an NLP benchmark pattern with rich text inputs, a clear prediction column, and room for semantic reasoning beyond keywords.

## novel challenge code switched accepted
- Challenge URL: https://drive.google.com/drive/folders/1dZVYPBAwPy_hMGSzF9ej9VJvleqy13In
- Source file: CHALLENGE_DESCRIPTION.md
- DOMAIN used for this document: NLP (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: Accepted (from Drive folder name)
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: Not shown/captured
- Tags: Not shown/captured
- Best/top context found: novel_challenge_code_switched_accepted from shared Google Drive folder

Full challenge description from Drive:

> # Challenge: Predict Resolution Hours from Code-Switched Complaints
> **Challenge title (for platform):** PREDICT RESOLUTION HOURS FROM CODE-SWITCHED SUPPORT COMPLAINTS
> **Difficulty:** Medium
> ---
> ## Overview
> You are given **code-switched customer support complaints**: each document mixes English with tokens from a fictional language (Verani). Your task is to predict the **resolution time in hours** (continuous regression) for each complaint.
> The prepared dataset provides training data (complaint text, category, and resolution hours) and test data (complaint text and category only). You must produce a CSV of predictions for each test row, one prediction per `id`. Submissions are scored with **Root Mean Squared Error (RMSE)**; **lower is better**.
> Real-world context: triage systems that estimate handling time from mixed-language or code-switched tickets can improve routing and SLA planning. This benchmark uses synthetic data to avoid licensing issues while testing NLP and feature-engineering skills.
> ---
> ## Evaluation
> Submissions are scored using **RMSE (Root Mean Squared Error)**. Lower is better.
> **Grading direction:** Minimize.
> **Formula:**
> ```text
> RMSE = sqrt( mean( (y_true - y_pred)^2 ) )
> ```
> **Theoretical minimum:** 0 (perfect predictions).
> **Theoretical maximum:** Unbounded; for config display you may set an upper bound (e.g. 200). The actual target range in the data is 0.5–168 hours.
> ---
> ## Dataset (prepared)
> After the prepare script runs, solvers see:
> **In `public/`:**
> - **train.csv** — id, text, category, target. Exactly 22,400 rows (80% of 28,000).
> - **test.csv** — id, text, category. Exactly 5,600 rows. No target column.
> - **sample_submission.csv** — id, prediction. Example format; prediction values are placeholders.
> **In `private/` (not visible to solvers):**
> - **answers.csv** — id, target. Ground truth for test set only.
> **Column types:** `id` (int), `text` (string), `category` (string), `target` (float, resolution hours).
> ---
> ## Submission
> Submit a single CSV file with **exactly** these columns:
> | Column     | Type  | Description |
> |------------|-------|-------------|
> | id         | int   | Row identifier from test.csv (one per test row). |
> | prediction | float | Predicted resolution time in hours. |
> **Requirements:**
> - Must contain exactly **5,600 rows** (one per test sample). No duplicate ids.
> - Must include header row.
> - Column names must be `id` and `prediction`. No other columns are used for grading; extra columns are ignored but the grader requires `prediction` to exist and be numeric.
> ---
> ## Formatting note
> Keep the problem description readable: use separate sections and code blocks only where needed (e.g. for the RMSE formula or submission table), not one single code block for the entire description.

Inspiration note: Useful as an NLP benchmark pattern with rich text inputs, a clear prediction column, and room for semantic reasoning beyond keywords.

## novel challenge 4 risk memos accepted
- Challenge URL: https://drive.google.com/drive/folders/1GqT1fdP9fOpbORqADL3Wu-GfYf7_mbmk
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: NLP (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: Accepted (from Drive folder name)
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: Not shown/captured
- Tags: Not shown/captured
- Best/top context found: novel_challenge_4_risk_memos_accepted from shared Google Drive folder

Full challenge description from Drive:

> # Challenge creation form — fill-in (novel_challenge_4)
> Tie this challenge to the **accepted dataset**: ORBIT Supply-Chain Risk Memos — Disruption Severity Tier (Synthetic).
> ---
> ## 1) Difficulty
> **Select:** **Medium**
> ---
> ## 2) Challenge Title
> ```
> NLP Severity Prediction from Obfuscated Supply-Chain Risk Memos
> ```
> ---
> ## 3) Problem Description
> ```markdown
> # NLP Severity Prediction from Obfuscated Supply-Chain Risk Memos
> ## Overview
> This is an **NLP** task requiring **natural language understanding** of heavily obfuscated, multi-section risk memos written in English from a simulated supply-network monitoring system. Each memo follows the **ORBIT protocol** (Operational Risk Briefing & Impact Taxonomy) — a fictional structured reporting format with typed section headers and natural language narrative.
> Your goal is to build an **NLP pipeline** that reads, parses, and interprets these text documents to predict a severity label. Each memo describes a potential supply disruption and contains 2–5 ORBIT sections:
> - **[ORBIT:VECTOR]** — identifies the disruption source with an anonymized risk code (`ORB-CODE`) and a narrative description. In ~55% of memos the narrative text is redacted (`[narrative redacted]`). In surviving narratives, 1–3 words may be randomly dropped.
> - **[ORBIT:IMPACT]** — reports shortfall and cycle counts replaced by single tokens (`<QTY>`, `<PERIOD>`) and a masked downstream effect (`[MASKED]`).
> - **[ORBIT:MITIGATION]** (sometimes present, ~50%) — describes countermeasures with a masked effectiveness rating (`[MASKED]`).
> - **[ORBIT:CASCADE]** (sometimes present, ~50%) — describes propagation depth (`<DEPTH>`) and a masked rate (`[MASKED]`).
> - **[ORBIT:NOTE]** (sometimes present, ~20%) — analyst notes containing tier-irrelevant boilerplate text (distractor section).
> **Important preprocessing already applied:**
> - The `[ORBIT:VERDICT]` section (which explicitly states the tier) has been **removed**.
> - All specific risk codes (ORB-V1…V7, ORB-I1…I7, ORB-M1…M5) are **masked** to `ORB-CODE`.
> - All numeric values (shortfall amounts, cycle counts, cascade depth) are replaced with **single placeholder tokens** (`<QTY>`, `<PERIOD>`, `<DEPTH>`).
> - Categorical severity terms (effectiveness ratings, cascade rates, downstream impact) are **masked** to `[MASKED]`.
> - ~55% of memos have the VECTOR narrative **redacted**; ~30% of surviving narratives have 1–3 words randomly **dropped**.
> - ~35% of memos have their section order **shuffled**.
> - ~30% of rows have the `region` column **missing** (NaN).
> - ~20% of rows have the `commodity_class` column **missing** (NaN).
> **Why this is hard:** Narrative templates are shared across tiers (the same phrasing can appear at any severity level), numeric values are fully masked, and most narratives are redacted. The remaining signal is subtle and distributed across multiple weak cues — no single feature determines the tier.
> Your task is to predict the **disruption severity tier** for each text memo. There are 5 tiers (ordinal):
> - **tier_1_minor** (~28%) — routine fluctuation, negligible downstream impact
> - **tier_2_moderate** (~24%) — notable disruption, low-to-moderate downstream effect
> - **tier_3_significant** (~22%) — material disruption requiring intervention
> - **tier_4_severe** (~16%) — major disruption with cascading effects
> - **tier_5_critical** (~10%, minority) — catastrophic failure, emergency response
> Submissions are scored using **quadratic-weighted Cohen's Kappa**. This metric is designed for ordinal classification: it penalizes predictions that are far from the true tier (e.g. predicting tier_1 when truth is tier_5) much more than close misclassifications (tier_3 vs tier_4). **Higher is better.**
> ## Evaluation
> **Metric:** Quadratic-weighted Cohen's Kappa.
> Cohen's Kappa measures agreement between predicted and true labels, adjusted for chance. The quadratic weighting assigns a cost proportional to the squared distance between the predicted and true tier index (0–4), making it ideal for ordinal tasks.
> **Grading direction:** Maximize.
> **Theoretical minimum:** -1 (systematic disagreement, worse than chance)
> **Theoretical maximum:** 1 (perfect agreement)
> ## Dataset (prepared)
> **In public/:**
> - **train.csv** — id, memo, num_sections, region, commodity_class, label. Exactly 25,600 rows (stratified 80% split).
> - **test.csv** — id, memo, num_sections, region, commodity_class. Exactly 6,400 rows. No label column.
> - **sample_submission.csv** — id, label. Example format with placeholder labels.
> **In private/ (not visible to solvers):** answers.csv — id, label.
> **Column descriptions:**
> | Column          | Type   | Description |
> |-----------------|--------|-------------|
> | id              | int    | Unique memo identifier |
> | memo            | string | Heavily obfuscated multi-section ORBIT risk memo. Risk codes masked to ORB-CODE, all numbers replaced with single tokens (<QTY>, <PERIOD>, <DEPTH>), categorical terms [MASKED], ~55% narratives redacted, ~30% of surviving narratives word-dropped, ~35% section order shuffled, distractor [ORBIT:NOTE] sections present in ~20%. |
> | num_sections    | int    | Number of ORBIT sections in the memo (2–5) |
> | region          | string | Fictional region. One of: norath, veldan, crymara, esthos, lunavar, torwen. ~30% missing (NaN). |
> | commodity_class | string | Fictional commodity. One of: synth-ore, bio-compound, flux-crystal, plasma-stock, neuro-fiber, cryo-element, photon-alloy, gravity-mesh. ~20% missing (NaN). |
> | label           | string | Severity tier. One of: tier_1_minor, tier_2_moderate, tier_3_significant, tier_4_severe, tier_5_critical |
> ## Submission
> Submit a CSV with exactly these columns:
> | Column | Type   | Description |
> |--------|--------|-------------|
> | id     | int    | Memo identifier from test.csv (one per test row) |
> | label  | string | Predicted severity tier |
> **Requirements:**
> - Exactly **6,400 rows** (one per test memo). No duplicate ids.
> - Header row required.
> - Label values must be one of the 5 valid tiers listed above.
> **Example of a correctly formatted submission (first few rows):**
> ```
> id,label
> 50,tier_2_moderate
> 51,tier_4_severe
> 52,tier_1_minor
> 53,tier_3_significant
> 54,tier_5_critical
> ...
> ```
> (Your file must have 6,400 rows total, one per test id, with no duplicates.)
> ```
> ---
> ## 4) Tags
> **Select:** **text**
> ---
> ## 5) Grading Configuration
> **Grade direction:** **Maximize**
> **Theoretical minimum:** **-1**
> **Theoretical maximum:** **1**
> ---
> ## 6) Grading Script (Custom)
> ```python
> import pandas as pd
> import numpy as np
> VALID_LABELS = {
> "tier_1_minor", "tier_2_moderate", "tier_3_significant",
> "tier_4_severe", "tier_5_critical",
> }
> LABEL_ORDER = [
> "tier_1_minor", "tier_2_moderate", "tier_3_significant",
> "tier_4_severe", "tier_5_critical",
> ]
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> """
> Score a submission using quadratic-weighted Cohen's Kappa.
> Args:
> submission: The agent's predictions (loaded from submission.csv). Columns: id, label.
> answers: Ground truth labels (loaded from private/answers.csv). Columns: id, label.
> Returns:
> A float score in [-1, 1]. Direction: maximize.
> Raises:
> ValueError: If the submission format is invalid.
> RuntimeError: If an unexpected error occurs.
> """
> try:
> if "id" not in submission.columns or "label" not in submission.columns:
> raise ValueError("Submission must have columns: id, label")
> if submission["id"].duplicated().any():
> raise ValueError("Submission must not contain duplicate id values")
> if answers["id"].duplicated().any():
> raise ValueError("Answers file must not contain duplicate id values")
> if len(submission) != len(answers):
> raise ValueError(
> f"Submission must have exactly {len(answers)} rows, got {len(submission)}"
> )
> sub_ids = set(submission["id"])
> ans_ids = set(answers["id"])
> if sub_ids != ans_ids:
> missing = ans_ids - sub_ids
> extra = sub_ids - ans_ids
> if missing:
> raise ValueError(f"Submission missing ids: {len(missing)} (e.g. {list(missing)[:5]})")
> if extra:
> raise ValueError(f"Submission has extra ids: {len(extra)}")
> if submission["label"].isna().any():
> raise ValueError("Submission has missing (NaN) label values")
> sub_labels = set(submission["label"].dropna().unique())
> invalid = sub_labels - VALID_LABELS
> if invalid:
> raise ValueError(f"Invalid label values: {invalid}. Must be one of {VALID_LABELS}")
> merged = answers.merge(submission, on="id", how="left", suffixes=("_true", "_pred"))
> if merged["label_pred"].isna().any():
> raise ValueError("Submission has missing predictions for some rows after merge")
> y_true = merged["label_true"].values
> y_pred = merged["label_pred"].values
> label_to_idx = {lab: i for i, lab in enumerate(LABEL_ORDER)}
> y_true_idx = np.array([label_to_idx[l] for l in y_true])
> y_pred_idx = np.array([label_to_idx[l] for l in y_pred])
> if np.ptp(y_pred_idx) == 0:
> return float(0.0)
> from sklearn.metrics import cohen_kappa_score
> kappa = cohen_kappa_score(y_true_idx, y_pred_idx, weights="quadratic")
> if np.isnan(kappa):
> return float(0.0)
> return float(kappa)
> except ValueError:
> raise
> except Exception as e:
> raise RuntimeError(f"Grading failed: {e}") from e
> ```
> ---
> ## 7) Data Preparation Pipeline
> **Input:** raw dataset file **data.csv** (id, memo, region, commodity_class, label).
> **Script — prepare.py:**
> *(See prepare.py file — updated v2 with aggressive obfuscation. Key changes from v1: all numbers → single tokens, 55% narrative redaction, 30% word-drop on survivors, 35% section shuffle, 30% missing region, 20% missing commodity, 50% NOTE section stripping.)*
> Run **Run Prepare** after pasting.
> ---
> ## 8) Evaluation Rubrics
> Add each via "Add Rubric":
> **1** — DATA_HANDLING | REQUIRED
> **Criterion:** Loads and uses the `memo` column from train/test; does not rely solely on `region`, `commodity_class`, or `num_sections`.
> **Rationale:** The memo text is the primary input containing ORBIT risk codes, shortfall estimates, and cascade information. Ignoring it means the model cannot learn the structured cues critical to severity prediction.
> **2** — FEATURE_ENGINEERING | RECOMMENDED
> **Criterion:** Extracts structured features from the obfuscated memo (e.g. section presence patterns, narrative redaction status, [ORBIT:NOTE] distractor detection) and combines them with text features.
> **Rationale:** After aggressive obfuscation (all numbers masked to single tokens, most narratives redacted), remaining signal is distributed across weak structural cues; combining multiple features is essential.
> **3** — FEATURE_ENGINEERING | RECOMMENDED
> **Criterion:** Handles missing metadata gracefully — ~30% of rows have region as NaN, ~20% have commodity_class as NaN. Uses imputation or treats missingness as a feature rather than dropping rows.
> **Rationale:** Dropping rows with missing metadata would lose a significant fraction of training data; missingness itself may carry weak signal.
> **4** — TRAINING | RECOMMENDED
> **Criterion:** Uses a proper train/validation split or cross-validation with stratification for model selection; does not tune or select models using the test set.
> **Rationale:** Class imbalance (tier_5_critical ~10%) means unstratified splits can misrepresent minority class performance.
> **5** — CODE_QUALITY | REQUIRED
> **Criterion:** Submission CSV has columns `id` and `label` with exactly one row per test id, no duplicate ids, and all labels are one of the 5 valid severity tiers.
> **Rationale:** Grader expects this format and valid labels; wrong format or invalid labels cause grading failure.
> **6** — DATA_HANDLING | RECOMMENDED
> **Criterion:** Accounts for the class imbalance (tier_5_critical ~10% vs tier_1_minor ~28%) using techniques such as stratified sampling, class weights, oversampling, or ordinal-aware loss functions.
> **Rationale:** The grading metric (quadratic-weighted Kappa) penalizes distant misclassifications; ignoring imbalance risks systematically misclassifying the minority tiers.
> **7** — UNIVERSAL | UNIVERSAL
> **Criterion:** Does not use test set or test labels for training, feature computation, or normalization.
> **Rationale:** Universal anti-leakage criterion.
> ---
> ## 9) Agent Evaluation Runs
> No fill; runs on submit.
> ---
> ## Checklist
> - [ ] Dataset: ORBIT Supply-Chain Risk Memos — Disruption Severity Tier (Synthetic) accepted and selected
> - [ ] Difficulty: Medium
> - [ ] Title: NLP Severity Prediction from Obfuscated Supply-Chain Risk Memos
> - [ ] Problem description: 25,600 / 6,400 rows, 5 tiers, quadratic-weighted Cohen's Kappa, maximize, min -1 max 1, inline submission example
> - [ ] Tags: text
> - [ ] Grading: Maximize; min -1; max 1
> - [ ] Grading script: quadratic Cohen's Kappa (sklearn); merge left; id/length/label validation; try/except; constant predictions return 0.0
> - [ ] Prepare (v2): strip VERDICT/REF/NOTE(50%); mask codes; ALL numbers→single tokens; mask categorical terms; redact ~55% narratives; word-drop ~30% survivors; shuffle ~35% sections; missing region ~30%; missing commodity ~20%; stratified 80/20 split; Run Prepare succeeded
> - [ ] 7 rubrics added (2 REQUIRED, 4 RECOMMENDED, 1 UNIVERSAL)

Inspiration note: Useful as an NLP benchmark pattern with rich text inputs, a clear prediction column, and room for semantic reasoning beyond keywords.

## novel challenge 3 Agent Negotiation accepted
- Challenge URL: https://drive.google.com/drive/folders/1xhs4cxn_9hlvuqHd8Jutp9asa8S3RdQd
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: NLP (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: Accepted (from Drive folder name)
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: Not shown/captured
- Tags: Not shown/captured
- Best/top context found: novel_challenge_3_Agent Negotiation_accepted from shared Google Drive folder

Full challenge description from Drive:

> # Challenge creation form — fill-in (novel_challenge_3)
> Tie this challenge to the **accepted dataset**: Multi-Agent Negotiation Transcripts — Deal Outcome (Synthetic).
> ---
> ## 1) Difficulty
> **Select:** **Medium**
> ---
> ## 2) Challenge Title
> ```
> PREDICT NEXARI PROTOCOL SESSION CONVERGENCE STATE FROM OBFUSCATED MULTI-AGENT LOGS
> ```
> ---
> ## 3) Problem Description
> ```markdown
> # Predict Nexari Protocol Session Convergence State from Obfuscated Multi-Agent Logs
> ## Overview
> You are given **obfuscated interaction logs** from a simulated **autonomous agent coordination system**. In this system, two agents (tagged [BUYER] and [SELLER]) communicate through a fictional protocol called **Nexari** to resolve resource allocation disputes. Each log represents one **coordination session**.
> The raw logs have undergone a **multi-stage obfuscation pipeline** that strips direct indicators of the session outcome. Your task is to reconstruct the **convergence state** — the final resolution of the session — from the degraded signal that remains. This simulates a real-world scenario where telemetry data is incomplete, partially redacted, and noisy.
> **Obfuscation pipeline applied to every session:**
> 1. **Tail truncation:** The last 2 messages of each session are removed. The convergence state label reflects the true outcome of the *complete* session — you must predict it from incomplete context.
> 2. **Action-token collapse:** All typed Nexari protocol tokens (originally distinct action types) have been collapsed to a single generic `NEXO:ACTION` marker. The original action vocabulary is not recoverable.
> 3. **Numeric quantization:** All precise numeric parameters have been replaced with coarse-grained buckets (`<500>`, `<1500>`, `<3000>`, `<5000>`, `<5000+>`). Fine-grained parameter trajectories are lost.
> 4. **Positional noise:** In ~20% of sessions, intermediate messages have been shuffled. Message ordering is not always reliable.
> 5. **Metadata dropout:** The `sector` field (coordination domain) is blank for ~15% of sessions.
> Each session converges to one of 4 terminal states:
> - **deal_accepted** — both agents reached a mutually confirmed allocation (~30%)
> - **deal_rejected** — one agent issued a terminal refusal (~25%)
> - **counter_proposed** — the session ended with a pending unresolved revision (~28%)
> - **timeout** — the session expired before either agent acted decisively (~17%, minority class)
> The convergence state must be inferred from residual signals:
> 1. **Linguistic patterns** — phrasing in each message (willingness, resistance, delay language)
> 2. **Quantized parameter shifts** — how bucketed values change across messages
> 3. **Session structure** — message count, speaker balance, presence of system messages
> 4. **Domain context** — when the sector field is available
> This challenge tests robustness to **information loss, noise, and missing data** — skills critical for real-world deployed ML systems.
> ## Evaluation
> **Metric:** Inverse-frequency-weighted macro F1 (custom).
> For each of the 4 convergence classes, compute class-level F1 = 2 × precision × recall / (precision + recall). Then weight each F1 by (N / n_class) where N = total samples and n_class = count for that class. Normalize weights to sum to 1. The final score is the weighted sum.
> This metric penalizes models that ignore the minority class. The rarest class (timeout, ~17%) carries the highest weight.
> **Grading direction:** Maximize.
> **Theoretical minimum:** 0
> **Theoretical maximum:** 1
> ## Dataset (prepared)
> **In public/:**
> - **train.csv** — id, transcript, num_turns, sector, label. Exactly 22,500 rows (stratified 75% split).
> - **test.csv** — id, transcript, num_turns, sector. Exactly 7,500 rows. No label column.
> - **sample_submission.csv** — id, label. Example format with placeholder labels.
> **In private/ (not visible to solvers):** answers.csv — id, label.
> **Column descriptions:**
> | Column     | Type   | Description |
> |------------|--------|-------------|
> | id         | int    | Unique session identifier |
> | transcript | string | Obfuscated interaction log. Last 2 messages removed; all protocol tokens collapsed to NEXO:ACTION; numeric parameters quantized to buckets; ~20% of sessions have shuffled intermediate messages. Messages separated by `\|\|\|`. Speaker tags: [BUYER], [SELLER], or [SYSTEM]. |
> | num_turns  | int    | Number of messages in the provided (truncated) transcript. |
> | sector     | string | Coordination domain. One of: energy, defense, biotech, logistics, manufacturing. **Blank for ~15% of rows.** |
> | label      | string | Convergence state. One of: deal_accepted, deal_rejected, counter_proposed, timeout |
> ## Submission
> Submit a CSV with exactly these columns:
> | Column | Type   | Description |
> |--------|--------|-------------|
> | id     | int    | Session identifier from test.csv (one per test row) |
> | label  | string | Predicted convergence state: deal_accepted, deal_rejected, counter_proposed, or timeout |
> **Requirements:**
> - Exactly **7,500 rows** (one per test session). No duplicate ids.
> - Header row required.
> - Label values must be one of the 4 valid convergence states listed above.
> **Example of a correctly formatted submission (first few rows):**
> ```
> id,label
> 0,deal_accepted
> 1,counter_proposed
> 2,deal_rejected
> 3,timeout
> 4,deal_accepted
> ...
> ```
> (Your file must have 7,500 rows total, one per test id, with no duplicates.)
> ```
> ---
> ## 4) Tags
> **Select:** **text**, **feature-engineering**
> ---
> ## 5) Grading Configuration
> **Grade direction:** **Maximize**
> **Theoretical minimum:** **0**
> **Theoretical maximum:** **1**
> ---
> ## 6) Grading Script (Custom)
> ```python
> import pandas as pd
> import numpy as np
> VALID_LABELS = {"deal_accepted", "deal_rejected", "counter_proposed", "timeout"}
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> """
> Score a submission against ground truth using frequency-weighted macro F1.
> Args:
> submission: The agent's predictions (loaded from submission.csv). Columns: id, label.
> answers: Ground truth labels (loaded from private/answers.csv). Columns: id, label.
> Returns:
> A float score in [0, 1]. Direction: maximize.
> Raises:
> ValueError: If the submission format is invalid.
> RuntimeError: If an unexpected error occurs.
> """
> try:
> if "id" not in submission.columns or "label" not in submission.columns:
> raise ValueError("Submission must have columns: id, label")
> if submission["id"].duplicated().any():
> raise ValueError("Submission must not contain duplicate id values")
> if answers["id"].duplicated().any():
> raise ValueError("Answers file must not contain duplicate id values")
> if len(submission) != len(answers):
> raise ValueError(
> f"Submission must have exactly {len(answers)} rows, got {len(submission)}"
> )
> sub_ids = set(submission["id"])
> ans_ids = set(answers["id"])
> if sub_ids != ans_ids:
> missing = ans_ids - sub_ids
> extra = sub_ids - ans_ids
> if missing:
> raise ValueError(f"Submission missing ids: {len(missing)} (e.g. {list(missing)[:5]})")
> if extra:
> raise ValueError(f"Submission has extra ids: {len(extra)}")
> sub_labels = set(submission["label"].dropna().unique())
> invalid = sub_labels - VALID_LABELS
> if invalid:
> raise ValueError(f"Invalid label values: {invalid}. Must be one of {VALID_LABELS}")
> if submission["label"].isna().any():
> raise ValueError("Submission has missing (NaN) label values")
> merged = answers.merge(submission, on="id", how="left", suffixes=("_true", "_pred"))
> if merged["label_pred"].isna().any():
> raise ValueError("Submission has missing predictions for some rows after merge")
> y_true = merged["label_true"].values
> y_pred = merged["label_pred"].values
> classes = sorted(VALID_LABELS)
> total = len(y_true)
> class_f1s = []
> class_weights = []
> for cls in classes:
> true_pos = np.sum((y_true == cls) & (y_pred == cls))
> false_pos = np.sum((y_true != cls) & (y_pred == cls))
> false_neg = np.sum((y_true == cls) & (y_pred != cls))
> precision = true_pos / (true_pos + false_pos) if (true_pos + false_pos) > 0 else 0.0
> recall = true_pos / (true_pos + false_neg) if (true_pos + false_neg) > 0 else 0.0
> f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
> class_count = np.sum(y_true == cls)
> weight = (total / class_count) if class_count > 0 else 0.0
> class_f1s.append(f1)
> class_weights.append(weight)
> total_weight = sum(class_weights)
> if total_weight == 0:
> return float(0.0)
> class_weights = [w / total_weight for w in class_weights]
> score = sum(f * w for f, w in zip(class_f1s, class_weights))
> return float(score)
> except ValueError:
> raise
> except Exception as e:
> raise RuntimeError(f"Grading failed: {e}") from e
> ```
> ---
> ## 7) Data Preparation Pipeline
> **Input:** raw dataset file **data.csv** (id, transcript, num_turns, sector, label).
> **Script — prepare.py:**
> Paste the full prepare.py from the `novel_challenge_3/prepare.py` file (contains truncation, token masking, price redaction, turn shuffling, missing value injection, and 75/25 split). Too long for inline — copy directly from the file.
> Run **Run Prepare** after pasting.
> ---
> ## 8) Evaluation Rubrics
> Add each via "Add Rubric":
> **1** — DATA_HANDLING | REQUIRED
> **Criterion:** Loads and uses the `transcript` column from train/test; does not drop it or use only `num_turns` and `sector`.
> **Rationale:** The interaction log is the primary input containing phrasing patterns and turn structure. Ignoring it means the model cannot learn session-level cues critical to resolution state prediction.
> **2** — DATA_HANDLING | RECOMMENDED
> **Criterion:** Handles missing values in the `sector` column (~15% missing) using imputation, a dedicated "unknown" category, or a model that natively handles nulls.
> **Rationale:** Sector is missing for ~15% of rows. Dropping those rows or crashing on nulls loses data and hurts performance on the minority class.
> **3** — FEATURE_ENGINEERING | RECOMMENDED
> **Criterion:** Extracts at least one feature from phrasing patterns in the transcript (e.g. presence of concession language, stalling phrases, refusal phrases, or turn-level sentiment).
> **Rationale:** Since protocol tokens are masked to NEXO:ACTION, the English phrasing is the primary signal carrier. Models that ignore phrase-level content will underperform.
> **4** — FEATURE_ENGINEERING | RECOMMENDED
> **Criterion:** Engineers at least one feature from bucketed price trajectories (e.g. how price range buckets shift across turns, or the distribution of bucket types).
> **Rationale:** Exact prices are redacted but bucket patterns still carry information about concession dynamics.
> **5** — TRAINING | RECOMMENDED
> **Criterion:** Uses a proper train/validation split or cross-validation with stratification for model selection; does not tune or select models using the test set.
> **Rationale:** Class imbalance (timeout ~17%) means random splits can misrepresent minority class performance. Stratified validation matters for this task.
> **6** — CODE_QUALITY | REQUIRED
> **Criterion:** Submission CSV has columns `id` and `label` with exactly one row per test id, no duplicate ids, and all labels are one of the 4 valid resolution states.
> **Rationale:** Grader expects this format and valid labels; wrong format or invalid labels cause grading failure.
> **7** — UNIVERSAL | UNIVERSAL
> **Criterion:** Does not use test set or test labels for training, feature computation, or normalization.
> **Rationale:** Universal anti-leakage criterion.
> ---
> ## 9) Agent Evaluation Runs
> No fill; runs on submit.
> ---
> ## Checklist
> - [ ] Dataset: Multi-Agent Negotiation Transcripts — Deal Outcome (Synthetic) accepted and selected
> - [ ] Difficulty: Medium
> - [ ] Title: PREDICT DEAL OUTCOME FROM MULTI-AGENT NEGOTIATION TRANSCRIPTS
> - [ ] Problem description: 24,000 / 6,000 rows, 4 classes, freq-weighted macro F1, maximize, min 0 max 1
> - [ ] Tags: text, feature-engineering
> - [ ] Grading: Maximize; min 0; max 1
> - [ ] Grading script: custom freq-weighted macro F1; merge left; id/length/label validation; try/except
> - [ ] Prepare: stratified split; data.csv → train/test/sample_submission/answers; Run Prepare succeeded
> - [ ] 7 rubrics added (2 REQUIRED, 4 RECOMMENDED, 1 UNIVERSAL)

Inspiration note: Useful as an NLP benchmark pattern with rich text inputs, a clear prediction column, and room for semantic reasoning beyond keywords.

## Drug-Label Statement Relationship Typing
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77xaqg52nvhfgnnvxa09nfw9890ehn
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: feature-engineering, text
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Each test instance is a bundle of 8 short clinical statements, every statement taken from
> a different drug's prescribing label and a different labelling section, with the
> section heading and the drug's own name removed. For each of the 28 unordered pairs of
> statements in a bundle you must predict a relation in {0, 1, 2}:
> A statement's section is the real label section it was drawn from; sections are grouped into a
> small number of families by communicative role (what the statement does for the reader —
> e.g. prescribe vs restrict vs report vs profile). This grouping deliberately
> cross-cuts the obvious topic split: for instance a warning and an adverse-reaction
> statement read as similar "safety" text but belong to different families. The exact section
> inventory and the section→family grouping are consistent across train and test — you learn
> them from the labelled training bundles, not from any published table.
> The task is a supervised sentence-pair relation problem. Train ships labelled bundles (so
> both the section reading and the family grouping are learnable); test ships unlabelled bundles.
> Why it is hard (and rewards learning)
> The section heading is removed, so the section must be inferred from the statement's
> content. Adjacent sections are genuinely confusable (a warning vs a precaution vs an
> adverse reaction), which caps even a strong reader well below a perfect score.
> The family grouping is not the obvious topic grouping, so a solver that clusters by
> surface topic gets the family relation wrong. The grouping is learnable only from the
> training relations.
> The relation graph is a property of how statements were randomly assembled across drugs
> for each bundle, so it is not a field of any single record — there is nothing to look up. The
> only path is learning to read the statements.
> Dataset
> public/ contains:
> Column data types and meaning:
> Each bundle contributes exactly 28 pairs (seg_i < seg_j over segments 0…7). Train pairs
> are fully labelled. There are 3000 train bundles and 1400 test bundles, drawn from disjoint
> sets of source drugs.
> Submission
> Submit a CSV file with one row per test pair (exactly 28 × 1400 = 39200 rows) plus a
> header, and exactly these four columns:
> Every (instance_id, seg_i, seg_j) pair in the test set must appear exactly once.
> Duplicate, missing, or unknown pairs, relation values outside {0, 1, 2}, or non-numeric
> values are rejected with an error. sample_submission.csv is a complete, correctly-formatted
> template. Row order does not matter.
> Example (first rows of a valid submission):
> instance_id,seg_i,seg_j,relation
> b6c8cd2b55f1,0,1,1
> b6c8cd2b55f1,0,2,0
> b6c8cd2b55f1,1,2,2
> How the submission is scored
> Submissions are scored by a single deterministic function grade(submission, answers)
> returning a float in [0, 1] (higher is better). All i<j pairs of all test bundles are
> pooled; let t be the true relation and p the predicted relation per pair.
> **Family-detection skill A** — chance-corrected agreement on same-family vs unrelated:
> a_t = 1[t != 0] ,  a_p = 1[p != 0]
> A   = max(0, MCC(a_t, a_p))           ; if A < 0.02 then A = 0   (dead-band -> chance = 0)
> where MCC is the Matthews correlation of two binary vectors,
> MCC = (TP*TN - FP*FN) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN))     (0 if any factor is 0)
> **Section-resolution skill B** — chance-corrected agreement on same-section vs
> same-family-different-section, restricted to the pairs where truth and prediction both
> say same-family, and scaled by how many true same-family pairs were captured:
> S    = { pairs with t in {1,2} AND p in {1,2} }
> b_t  = 1[t == 2] ,  b_p = 1[p == 2]      (over S)
> B    = max(0, MCC(b_t, b_p)) * ( |S| / |{pairs with t in {1,2}}| )
> Fusion (family detection gates, section resolution is the bonus) and shaping:
> raw   = 0.5 * A + 0.5 * sqrt(A * B)
> score = raw ** STRICT ,   clipped to [0, 1]
> with the fixed constant
> STRICT = 2.0
> A = 0 forces raw = 0 (you cannot earn section credit without detecting families); raw = 1
> (and score = 1.0 exactly) iff A = 1 and B = 1.
> Properties
> Perfect (p = t on every pair) → 1.0.
> No-skill — a constant relation, a random relation, or a systematically inverted relation
> — → 0.0 (chance-corrected; the dead-band snaps a chance-level family agreement to exactly 0).
> Irreducible ceiling. Because adjacent label sections are genuinely confusable from a
> single statement, even a strong reader tops out near 0.42; a strong classical bag-of-words
> baseline reaches about 0.33, and a cheap keyword baseline about 0.015.
> Invalid submissions (missing columns; duplicate, missing, or unknown pairs; relation not in
> {0, 1, 2}; non-numeric values; seg_i >= seg_j) raise a ValueError.
> What Not To Use
> Solvers must solve this with machine learning / NLP. The predicted relation for every
> pair must come from a model trained on the provided training relations and reading the
> held-out statement text. Submissions that reach the answer by non-ML means will be rejected.
> Not allowed
> Non-ML / "raw logic" solutions. No hand-written keyword→section rules, hard-coded
> look-up tables, or regexes that map phrases to a section or family. In particular, a
> constant relation, an all-unrelated submission, or any relation assignment that
> ignores the text is a non-ML shortcut and is prohibited — those score essentially zero anyway,
> and beating them requires actually reading the statements.
> Assuming the obvious topic grouping. The family grouping is by communicative role and
> deliberately cross-cuts the surface topic (a warning and an adverse-reaction statement are in
> different families). A hand-built "group by topic" rule is not a learned model and gets the
> family relation wrong; the grouping must be learned from the training relations.
> Recovering the answer by external lookup. Do not attempt to re-identify a statement's
> source drug label through any external resource, search engine, or online service in order to
> read off its section. The relation graph is a property of how statements were randomly
> assembled across drugs for each bundle; it is not a field of any single record, and the family
> grouping is specific to this task. The only legitimate path is the supervised mapping in the
> training relations.
> External label sources keyed to these specific statements or bundles.
> Allowed
> Any genuinely learned model — a fine-tuned transformer (BERT/DeBERTa/…), an autoregressive
> (GPT-style) LM fine-tuned for classification, a sentence-pair classifier, a text encoder +
> classifier head, a gradient-boosted model on learned features, an ensemble — trained on the
> provided training relations.
> Generic pretrained language-model backbones used as a starting point, and pretrained
> embeddings.
> Either modelling strategy: predicting pair relations directly as a sentence-pair classifier,
> or classifying each statement's latent section and deriving the relation.
> Standard NLP tooling: tokenisation, augmentation, paraphrase handling, class balancing,
> output-head design, ensembling, and threshold calibration.
> Any libraries you like in your own modelling pipeline that produces the submission CSV.
> The rule of thumb: every relation you submit must come from a trained model that infers the
> statements' sections and family grouping from the text and the training labels — not from a
> hand-built rule set, a constant, the obvious topic split, or re-identifying a statement's source
> label.

Inspiration note: Useful as an NLP pattern with textual evidence, relation labels, and clear discrete outputs that reward semantic understanding beyond keywords.

## Chemical Hazard Lot Priority
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx775f5n2kweej9mnvwtfwjvnx89mv5b
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↓ Lower is better
- Tags: text
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Chemical safety teams often review groups of substances rather than isolated compounds. Each case in this challenge is a short chemical safety evidence report describing four anonymized candidate lots, A through D. Every report combines coarse molecular descriptor language with warning-phrase summaries derived from physical-description text.
> Your task is to submit a ranked hazard-priority manifest for the four lots in each case. The hidden priority signal combines health, fire/reactivity, chronic/environmental, and within-lot label-conflict evidence. Public reports do not include chemical names, identifiers, structures, exact physical descriptions, GHS codes, or GHS labels.
> This is a Chemistry challenge with text-derived evidence: warning phrases from source physical descriptions have been reduced to coarse language-fraction statements, then embedded in a per-case lot report with chemistry descriptor bins. There are no instruction-following prompts or prompt-injection strings. A useful model must learn how chemistry descriptors and warning-language summaries rank safety pressure across structurally held-out chemical groups.
> Dataset
> File descriptions
> train.csv -- 5,000 labeled chemical safety reports. Each row contains one lot_evidence text report and the target priority_manifest.
> test.csv -- 1,600 held-out chemical safety reports with the same evidence-report format, without priority_manifest.
> sample_submission.csv -- A template showing the required submission format with random lot rankings.
> Column descriptions
> case_id (string) -- Unique hashed identifier for each case.
> lot_evidence (string) -- Natural-language chemical safety report for the four lots. Each lot section states lot size, coarse chemistry descriptor bins, and physical-warning language fractions from source description text.
> priority_manifest (string) -- Target column in train.csv only. A compact JSON object with a ranked_lots list ordered from highest to lowest hidden hazard priority.
> Evaluation
> Submissions are scored with weighted priority-order loss. Lower is better.
> For each case, the grader checks all six pairwise orderings among lots A through D. A pair is penalized when the lot with the higher hidden priority score is placed below the lot with the lower hidden priority score. Each pair is weighted by the absolute hidden-priority gap, so reversing two nearly tied lots hurts less than reversing a clear chemistry-safety separation:
> row_loss = 100 * weighted_wrong_pair_gap / total_pair_gap
> score = mean(row_loss)
> The best possible score is 0. A random valid ranking scores around 50 on this prepared split.
> Submission
> Submit a CSV file with one ranked manifest for every row in test.csv.
> case_id (string) -- The exact identifier from test.csv.
> priority_manifest (string) -- A JSON object with one key, ranked_lots, whose value is a list containing each of A, B, C, and D exactly once, ordered from highest to lowest predicted hazard priority.
> Example:
> case_id,priority_manifest
> CHL-01F7CB89B276,"{""ranked_lots"":[""B"",""A"",""D"",""C""]}"
> CHL-896CD3E2CE9A,"{""ranked_lots"":[""B"",""D"",""A"",""C""]}"
> Requirements
> The file must contain exactly 1,600 rows plus the header.
> Every case_id from test.csv must be present exactly once.
> The column names must be exactly case_id,priority_manifest.
> Every priority_manifest value must be valid JSON.
> ranked_lots must contain each candidate lot exactly once.
> File format: .csv only.
> What Not To Use
> Do not use exact chemical names, CAS numbers, structure identifiers, GHS statement codes, or raw source labels recovered outside the public files.
> Do not reverse-map anonymized lot features to individual source compounds or raw row identifiers. The public rows are intended as aggregate modeling inputs, not lookup keys.
> Do not manually rank held-out lots through web search or regulatory database search. The challenge is meant to evaluate automated Chemistry modeling from the public training cases.

Inspiration note: Useful as an NLP pattern with domain text, evidence-like fields, and discrete or calibrated outputs that reward semantic reasoning beyond surface keywords.

## Historical OCR Temporal Intrusion Detection
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79j4csve52gmv9nw26b1qtgs89gxss
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-02; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> This challenge is a text-only historical document forensics benchmark.
> Each sample contains a noisy historical OCR passage divided into several numbered segments. Most segments are temporally consistent with each other: they come from the same hidden publication-era profile and share similar historical language, print style, OCR texture, vocabulary, and document rhythm. However, exactly one segment is a temporal intrusion. It is a plausible historical OCR segment, but it does not belong to the same hidden era distribution as the surrounding passage.
> The task is to identify which segment is the temporal intruder.
> Participants are not asked to predict the year, decade, century, or literary epoch of a document. Instead, they must perform local temporal consistency analysis: given a group of noisy OCR segments that appear to form one historical document, determine which segment is out of place.
> The intruding segment may still look historically old. It may discuss a similar topic, use formal prose, contain old names or places, or include misleading historical dates. The challenge is to detect the segment whose language, OCR artifacts, spelling conventions, vocabulary, punctuation, typography-derived noise, or historical reference style does not match the rest of the passage.
> A strong model must act like a historical document examiner. It must compare segments against each other, infer the shared temporal profile of the majority, and localize the segment that breaks that profile.
> Motivation
> Large digitized text collections often contain fragmented, noisy, or incorrectly merged OCR output. Pages may be spliced, metadata may be unreliable, scans may be grouped incorrectly, and text extraction pipelines may accidentally join material from different documents or print periods. In archival settings, the problem is often not simply “what year is this document from?” but rather “does this document contain a fragment that does not belong?”
> Standard historical text dating tasks are usually absolute classification tasks. A model receives one passage and predicts a year, decade, century, or epoch. That formulation is useful, but it can reward simple topic cues, common-period priors, and direct chronological references. If the passage mentions a dated event, a person, or an institution, the model may guess the approximate period without actually understanding whether the text is internally consistent.
> This benchmark asks a more forensic question.
> The model must detect a local inconsistency inside a multi-segment historical passage. It must determine which segment does not match the surrounding temporal profile. This requires comparative reasoning across segments rather than independent classification of one excerpt.
> A weak system may try to date every segment separately and pick the one with the most unusual predicted date. That can help, but it is not enough. The intruder may be close in time, topically similar, or written in a conservative style. Some host segments may contain misleading references to older events. Some intruders may contain no explicit dates. Some segments may be noisy enough that the temporal signal is distributed across spelling, OCR texture, grammar, punctuation, and vocabulary rather than obvious content.
> The challenge rewards models that understand historical OCR as an internal consistency problem.
> Task
> For each sample, participants are given one segmented OCR passage.
> Each sample contains exactly eight numbered text segments:
> segment_1_text
> segment_2_text
> segment_3_text
> segment_4_text
> segment_5_text
> segment_6_text
> segment_7_text
> segment_8_text
> Exactly one segment is the temporal intruder.
> Participants must submit one numeric score for each segment. Higher scores should mean that the segment is more likely to be the intruder.
> The segment with the highest submitted score is treated as the predicted intruder.
> Scores do not need to be probabilities. They do not need to be between 0 and 1. They do not need to sum to 1. Only the within-sample ranking induced by the scores matters.
> Prepared Dataset
> The released challenge data contains:
> train.csv
> test.csv
> sample_submission.csv
> The prepared package may also include private answer files used only by the grading environment and a reproducibility notebook. Participants do not need to run the notebook to solve the challenge.
> train.csv contains labeled training samples. Each row is one temporal intrusion problem with eight OCR segments and one hidden intruder label.
> test.csv contains unlabeled evaluation samples. It has the same public input columns as the training file, but the intruder label is hidden.
> sample_submission.csv contains the required submission format. It has one row per test sample and eight score columns, one score for each segment.
> The public files do not expose exact publication years, decade labels, source identifiers, document identifiers, page numbers, language metadata, country metadata, temporal distances, private difficulty flags, or hidden grouping information.
> Each sample must be solved from the visible OCR text alone.
> Features
> The public dataset uses a segmented portfolio-style schema.
> sample_id
> Data type: string
> Description: A unique public identifier for the sample. It is used only for row matching. It should not be treated as a predictive signal.
> segment_1_text
> Data type: string
> Description: The first OCR segment in the sample. It may be part of the temporally consistent majority or it may be the intruder.
> segment_2_text
> Data type: string
> Description: The second OCR segment in the sample.
> segment_3_text
> Data type: string
> Description: The third OCR segment in the sample.
> segment_4_text
> Data type: string
> Description: The fourth OCR segment in the sample.
> segment_5_text
> Data type: string
> Description: The fifth OCR segment in the sample.
> segment_6_text
> Data type: string
> Description: The sixth OCR segment in the sample.
> segment_7_text
> Data type: string
> Description: The seventh OCR segment in the sample.
> segment_8_text
> Data type: string
> Description: The eighth OCR segment in the sample.
> Each segment is a noisy historical OCR text excerpt. Segments may contain archaic spelling, OCR errors, broken words, inconsistent spacing, punctuation artifacts, multilingual text, old typography effects, named entities, dates, page-layout residue, or generic prose.
> intruder_segment
> Data type: integer categorical label
> Description: The training label in train.csv. It is an integer from 1 to 8. A value of 1 means segment_1_text is the temporal intruder. A value of 8 means segment_8_text is the temporal intruder.
> The public test file does not include intruder_segment.
> train.csv Columns
> sample_id is a string. It uniquely identifies the training sample.
> segment_1_text through segment_8_text are strings. Each column contains one numbered OCR segment.
> intruder_segment is an integer from 1 to 8. It identifies which segment is temporally inconsistent with the other segments in the same sample.
> test.csv Columns
> sample_id is a string. It uniquely identifies the test sample.
> segment_1_text through segment_8_text are strings. Each column contains one numbered OCR segment.
> test.csv does not include intruder_segment, publication-year fields, decade fields, source metadata, document identifiers, temporal-distance labels, or private difficulty labels.
> sample_submission.csv Columns
> sample_id is a string. It must match a sample_id from test.csv.
> segment_1_score through segment_8_score are numeric values. Higher scores indicate that the corresponding segment is more likely to be the temporal intruder.
> Scores are used only to rank segments within each sample.
> Submission Format
> Submit a CSV with exactly these columns in exactly this order:
> sample_id,segment_1_score,segment_2_score,segment_3_score,segment_4_score,segment_5_score,segment_6_score,segment_7_score,segment_8_score
> Each sample_id must appear exactly once.
> All segment score values must be finite numeric values.
> Example submission:
> sample_id,segment_1_score,segment_2_score,segment_3_score,segment_4_score,segment_5_score,segment_6_score,segment_7_score,segment_8_score
> TS000001,0.12,0.91,0.33,0.04,0.78,0.20,0.16,0.55
> TS000002,0.81,0.11,0.06,0.38,0.72,0.44,0.09,0.15
> TS000003,0.03,0.21,0.67,0.64,0.08,0.32,0.17,0.95
> Invalid submissions include missing rows, extra rows, duplicate sample_id values, missing columns, extra columns, columns in the wrong order, non-numeric scores, NaN values, or infinite values.
> Evaluation
> Submissions are scored using the Historical Intrusion Localization Score on a 0 to 100 scale. Higher is better.
> For each test sample, the submitted segment scores are sorted from highest to lowest. The hidden intruder is the segment that is privately labeled as temporally inconsistent with the rest of the sample.
> The final score is:
> 100 * (
> 0.60 * Top1IntruderAccuracy
> + 0.20 * MeanReciprocalRank
> + 0.10 * MajorityConsistencyRank
> + 0.10 * HardCaseScore
> )
> Top1IntruderAccuracy is the fraction of test samples where the highest-scored submitted segment is exactly the hidden intruder.
> MeanReciprocalRank gives partial credit for ranking the hidden intruder near the top. If the hidden intruder is ranked first, the reciprocal rank is 1.0. If it is ranked second, the reciprocal rank is 0.5. If it is ranked eighth, the reciprocal rank is 0.125. This component is averaged across all test samples.
> MajorityConsistencyRank rewards separating the intruder from the temporally consistent majority. For each sample, the hidden intruder is compared against each of the seven non-intruder segments. A comparison receives full credit if the intruder receives a higher submitted score than the non-intruder segment. Tied scores receive half credit. This component is averaged across all intruder-versus-majority comparisons and all test samples.
> HardCaseScore is computed on a deterministic hidden hard-case subset. Hard cases may include samples where the intruder is close in time to the majority, the segments share similar topics, the OCR noise is heavy, the majority contains misleading historical dates, the intruder uses conservative or archaic language, or the temporal inconsistency is visible only through subtle style and OCR-distribution clues.
> On the hard-case subset, the grader computes:
> HardTop1IntruderAccuracy
> HardMeanReciprocalRank
> HardMajorityConsistencyRank
> The hard-case component is:
> HardCaseScore =
> 0.60 * HardTop1IntruderAccuracy
> + 0.25 * HardMeanReciprocalRank
> + 0.15 * HardMajorityConsistencyRank
> If the hidden test split contains no hard-case rows, HardCaseScore is computed over the full test set.
> Intended Methods
> Participants may use any ML text-based modeling approach that relies only on the provided public data.
> Rules
> Participants should predict from the provided public OCR segments only.
> Participants must not use private answer files, hidden labels, hidden years, hidden decades, hidden temporal distances, source metadata, row order, file structure, sample identifiers, or any non-public fields as shortcuts.
> Participants must not attempt to recover hidden labels by searching exact excerpts in external catalogs, search engines, archives, or other databases. The intended task is internal temporal-consistency reasoning from the provided OCR text, not document reverse lookup.
> Participants may train on train.csv, create their own validation split, and submit predictions for test.csv.
> Participants may use general-purpose pretrained language models, but external resources must not be used to directly identify the source document, exact publication year, or hidden metadata of test excerpts.
> This makes the benchmark closer to historical document forensics than ordinary text dating.
> The goal is to build a model that can identify temporal intrusions inside segmented historical OCR passages.
> A high-scoring solution should detect the inconsistent segment even when the intruder is plausible, historically styled, topically similar, close in time, or obscured by OCR noise.
> The best systems will combine historical language understanding, OCR robustness, comparative ranking, and document-level consistency reasoning.

Inspiration note: Useful as an NLP pattern with domain text, evidence-like fields, and discrete or calibrated outputs that reward semantic reasoning beyond surface keywords.

## Scientific Abstract Discourse Bridge Prediction
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75ser30c82swh78v6dnmp14589nrf4
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-03; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Scientific abstracts often move through recognizable discourse bridges: context leads to a research gap, a gap motivates a method, a method leads to evidence, evidence supports findings, and findings lead to implications.
> In this challenge, the goal is to identify the discourse bridge between two adjacent obfuscated abstract fragments. Each example contains a left_fragment and a right_fragment from the same arXiv abstract. Common function words and discourse markers are preserved, while most content words are replaced by per-example salted hash tokens such as w0427.
> This is a single-task NLP discourse-understanding challenge. Participants submit one bridge label for each test example.
> Target Output
> For each test row, predict one label:
> bridge_type
> The valid labels are:
> context_to_gap: the left fragment gives background or context and the right fragment introduces a limitation, gap, or need.
> gap_to_method: the left fragment motivates a problem and the right fragment introduces an approach, method, model, or framework.
> method_to_evidence: the left fragment describes an approach and the right fragment discusses experiments, data, evaluation, comparisons, or benchmarks.
> evidence_to_finding: the left fragment gives evidence or evaluation setup and the right fragment states results, improvements, findings, or observations.
> finding_to_implication: the left fragment states a finding and the right fragment gives a conclusion, implication, limitation, or future direction.
> Evaluation
> Submissions are scored using Macro F1-score.
> For each valid bridge_type, the grader computes precision, recall, and F1-score from the submitted labels and the private true labels. The final score is the unweighted mean of the class-level F1-scores.
> The score ranges from 0.0 to 1.0. Higher is better.
> Macro F1 is used so that all bridge types matter, including less frequent discourse transitions.
> Dataset
> The prepared challenge dataset contains:
> public/train.csv
> public/test.csv
> public/sample_submission.csv
> public/prepared_schema.txt
> private/answers.csv
> The public training set contains adjacent obfuscated fragment pairs with known bridge labels. The public test set contains adjacent obfuscated fragment pairs whose bridge labels are withheld for private grading.
> Files And Columns
> public/train.csv - training discourse-bridge examples.
> sample_id: unique anonymized text example identifier.
> left_fragment: obfuscated sentence before the discourse bridge.
> right_fragment: obfuscated sentence after the discourse bridge.
> bridge_type: target discourse bridge label.
> validation_fold: deterministic validation fold assignment.
> public/test.csv - test discourse-bridge examples.
> sample_id: unique anonymized test identifier.
> left_fragment: obfuscated sentence before the discourse bridge.
> right_fragment: obfuscated sentence after the discourse bridge.
> public/sample_submission.csv - required submission format.
> sample_id: matching test identifier.
> bridge_type: predicted discourse bridge label.
> private/answers.csv - private grading labels with sample_id and withheld bridge_type values.
> Text Properties
> Each input row contains two adjacent sentence fragments from the same scientific abstract. The fragments are shown in their original local order, but the discourse relationship between them is withheld.
> To reduce source-text leakage, the prepared public release does not include raw titles, raw abstracts, original arXiv ids, author names, subject categories, exact filenames, or unmodified sentence text. Most content words are replaced with per-example salted hash tokens. The same source token maps consistently within a single example, preserving local repetition, but the mapping changes across examples to avoid a reusable global vocabulary.
> The intended input is the pair of obfuscated fragments. Metadata that would reveal position, source identity, subject category, or original wording is not included in the prepared public files.
> What Not To Use
> The following approaches are not allowed:
> Private labels or answer leakage: Do not access, reconstruct, cache, or manually encode private answers.
> Filename, id, or row-order rules: Do not use sample_id, row order, hidden metadata, or original identifiers as an answer lookup.
> Hidden preparation artifacts: Do not use non-public raw abstracts, original arXiv ids, subject categories, hash salts, sentence-splitting artifacts, or preparation files.
> External record matching: Do not match private test rows to external arXiv records or other external sources to recover the original abstract text.
> Hard-coded answer reconstruction: Do not attempt to reconstruct answers from hidden files, grader behavior, or non-public data.
> Submission-parser or grader exploits: Do not exploit bugs in validation, parsing, scoring, or file handling.
> Expected approach: use NLP discourse-understanding methods to infer the bridge label from the two obfuscated fragments. Text-pair models, local coherence features, discourse-marker features, validation folds, calibration, and ensembling are all reasonable approaches.
> Submission Format
> You must write your final submission CSV to exactly this path:
> ./working/submission.csv
> The CSV must contain exactly these columns in this order:
> sample_id,bridge_type
> Example rows:
> bridge_0123abcd45ef678901,gap_to_method
> bridge_abcdef0123456789ab,method_to_evidence
> Submission Requirements
> The file must exist at ./working/submission.csv.
> It must contain one row per test sample_id; every sample_id from public/test.csv must be present.
> Duplicate sample_id rows are not allowed.
> The columns must appear exactly as:
> sample_id,bridge_type
> Each bridge_type value must be one of:
> context_to_gap, gap_to_method, method_to_evidence, evidence_to_finding, finding_to_implication
> If the file is missing, unreadable, has the wrong columns, contains duplicate or missing sample_ids, or contains an invalid bridge_type label, the submission receives a score of 0.0.
> Extra columns are invalid.

Inspiration note: Useful because it converts nuanced text understanding into a compact label prediction with strict schema and discourse-aware target design.

## Adverse Report Suspect Medication Ordering
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7apsnexq65gdy0xpm51p6zyd89r9za
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↓ Lower is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-03; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Post-market adverse-event reports often list several medications for the same patient event. Some products are marked as higher-attention suspect medications, while others are co-reported background therapies. This challenge asks you to rank the medication cards in each report from most likely to least likely to carry that hidden suspect-report role.
> The data is intentionally anonymized to reduce source lookup risk. Medication indications and report context are reduced to coarse profiles, exact product names are withheld, and each row contains lossy clinical context plus anonymized candidate cards. A useful model should learn which candidate-profile patterns tend to receive higher safety-review attention inside a multi-medication row rather than relying on a single shortcut.
> This is a biology and pharmacovigilance NLP ranking task. In real safety review workflows, this kind of ordering helps focus human attention on the co-reported products most likely to need manual review first.
> Dataset
> File descriptions
> train.csv -- 1,567 anonymized safety-review packet rows containing 8,529 medication candidate cards and 19,444 within-packet candidate-pair ordering comparisons. Includes lossy report context, anonymized candidate cards, candidate count, and the target ranked_candidate_ids.
> test.csv -- 219 held-out safety-review packet rows containing 1,171 medication candidate cards and 2,619 candidate-pair ordering comparisons. Uses the same input columns as train.csv, but without ranked_candidate_ids.
> sample_submission.csv -- A template with every test id and a random complete medication ordering for each row.
> Column descriptions
> id (string) -- Unique 14-character hashed identifier for each report row.
> patient_sex (string) -- Lossy patient sex category: female, male, or unknown.
> patient_age_group (string) -- Coarse age bucket such as adult_45_64, older_65_79, or unknown.
> seriousness_flags (string) -- Semicolon-delimited serious-outcome profile, or none.
> reporter_qualification (string) -- Coarse reporter type such as physician, consumer, or other_health_professional.
> country_region (string) -- Coarse country or region bucket such as US, EU, GB, JP, or other.
> reaction_profile (string) -- Lossy reaction-term profile with grouped clinical reaction families and capped term counts.
> candidate_medications (string) -- JSON list of medication candidate cards. Each card contains candidate_id and a lossy indication profile.
> candidate_count (integer) -- Number of medication candidates in the row.
> ranked_candidate_ids (string) -- Train-only target. Candidate ids separated by |, ordered from highest to lowest hidden suspect-report role.
> Evaluation
> Submissions are scored with normalized pairwise suspect-order loss. Lower is better.
> For each report, every pair of candidates with different hidden role scores is compared. A penalty is added when the submitted order places the lower-role candidate ahead of the higher-role candidate. Pair weights are the absolute hidden-score gap, with a 1.25 multiplier for pairs involving the highest hidden role in that report. The row loss is normalized by the maximum possible pairwise penalty, then scaled to 0-100. The final score is the mean row loss across all test rows.
> def evaluate(predicted_order, hidden_scores):
> penalty = 0.0
> total = 0.0
> max_score = max(hidden_scores.values())
> for left, right in candidate_pairs:
> if hidden_scores[left] == hidden_scores[right]:
> continue
> weight = abs(hidden_scores[left] - hidden_scores[right])
> if hidden_scores[left] == max_score or hidden_scores[right] == max_score:
> weight *= 1.25
> total += weight
> if predicted_order.ranks_lower_role_before_higher_role(left, right):
> penalty += weight
> return 100.0 * penalty / total
> Submission
> Submit a CSV file with your medication ordering for every row in test.csv.
> id (string) -- The report id from test.csv.
> ranked_candidate_ids (string) -- Every candidate id from that row's candidate_medications, ordered from most likely to least likely to carry the higher hidden suspect-report role, separated by |.
> Example:
> id,ranked_candidate_ids
> 01e02a1dfd6348,M4|M3|M2|M5|M1
> 034eddeaa9bd45,M1|M2|M3|M4|M5
> Requirements
> The file must contain exactly 219 rows plus the header.
> Every id from test.csv must be present exactly once.
> Each ranked_candidate_ids value must contain every candidate id from that row exactly once.
> Candidate ids must be separated with |, with no extra ids and no duplicate ids.
> File format: .csv only, with exact column names id,ranked_candidate_ids.
> What Not To Use
> Do not reverse-search medication profile combinations in external adverse-event databases to recover the hidden source report role. That bypasses the intended ranking problem.
> Do not use public dashboards, API endpoints, mirrors, or downloadable safety-report files to map the benchmark rows back to original report identifiers or role codes.
> Do not build lookup tables from exact medication-profile combinations outside the supplied public training file. The task is to model the supplied anonymized candidate profiles, not recover held-out source rows.
> Do not manually relabel test rows by searching medication-card profile text on the web.

Inspiration note: Useful because it converts nuanced language or clinical text signals into a constrained ranking/label target with clear validation rules.

## Mars Mission Multi-Label Concept Tagging
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72wtytkwrynmbcq7cqeq0wex89mccw
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, large-scale, feature-engineering
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> You are given a collection of technical and scientific documents about Mars missions and Mars science — their titles, abstracts, and (for many of them) full body text. Each document was annotated by domain experts with a set of concept tags from a controlled vocabulary of 78 concepts. The tag names have been anonymized (each is an opaque token such as concept_0042), so the task can only be solved by reading and understanding the document text — there is no way to recover the tags by matching strings or by looking anything up.
> Your job: for each test document, read its text and predict the set of concept tags it was annotated with. This is a natural-language understanding problem — the tags are semantic concepts, not words copied from the document. In fact 0% of the gold tags appear verbatim in the text (they are anonymized tokens), so success depends entirely on modeling the language of each document.
> Two properties make the task hard:
> Semantic inference over text. Tags are expert-assigned concepts. A model must learn, from the training documents, what language is associated with each concept token and infer the right tags for unseen documents.
> Temporal generalization. Evaluation is a temporal hold-out: the test documents are the most recent ~22% of each document collection. A solution must generalize to newer documents and newer mission topics, not memorize the past.
> The corpus is heterogeneous: documents come from two distinct collections (marked A and B), range from a single short abstract to a long multi-page report with realistic text-extraction noise, and carry a long-tailed distribution of concepts (a mean of 1.22 tags per document, median 1, up to 6).
> Evaluation
> Submissions are scored by example-based (sample-averaged) F1 between the predicted tag set and the gold tag set, averaged over all test documents. The metric is in the range [0, 1] and higher is better.
> For each document i with predicted set P_i and gold set G_i:
> precision_i = |P_i ∩ G_i| / |P_i|
> recall_i = |P_i ∩ G_i| / |G_i|
> f1_i = 0 if precision_i + recall_i == 0, else 2 * precision_i * recall_i / (precision_i + recall_i)
> The final score is the mean of f1_i over the test set. (If both predicted and gold sets are empty a document scores 1.0; every test document here has at least one gold tag, so an empty prediction scores 0 for that document.) Tags are compared case-insensitively after trimming whitespace; tag order does not matter.
> Reference implementation of the metric:
> def evaluate(y_true, y_pred):
> # y_true, y_pred: dict mapping id -> set of concept-tag strings
> total = 0.0
> for i, gold in y_true.items():
> pred = y_pred.get(i, set())
> if not gold and not pred:
> total += 1.0
> continue
> inter = len(pred & gold)
> if inter == 0:
> continue
> precision = inter / len(pred)
> recall = inter / len(gold)
> total += 2 * precision * recall / (precision + recall)
> return total / len(y_true)
> Dataset
> After preparation the data is provided under public/:
> train.csv.gz — 7,077 labelled documents with columns: id, source, year, title, abstract, body, labels.
> test.csv.gz — 2,081 documents with columns: id, source, year, title, abstract, body (no labels).
> sample_submission.csv — a correctly formatted example submission.
> Column meanings:
> id (string) — anonymized document identifier (e.g. doc_000313); the value you must key predictions on.
> source (string) — which collection the document came from: A or B (an anonymized categorical feature).
> year (integer) — document year.
> title (string) — document title (natural-language text).
> abstract (string) — document abstract (natural-language text).
> body (string) — leading extracted full text, natural-language (up to 8,000 characters; empty for documents that have no extracted body).
> labels (string, train only) — the gold tag set, serialized as pipe-separated anonymized concept tokens, e.g. concept_0007|concept_0016.
> The test set has 2,081 documents across the two collections. Rows in train.csv.gz and test.csv.gz are in randomized order — row position carries no information, so do not rely on order.
> Submission format
> Submit a CSV with exactly two columns, id and labels, and exactly one row per test id (2,081 data rows plus the header). Rows may be in any order — the grader merges on id, so a shuffled submission scores identically. The labels value is the predicted tag set serialized as pipe-separated concept tokens (the same format as the train labels column). Predict at least one tag per document.
> Example (using real test ids):
> id,labels
> doc_000313,concept_0018|concept_0046
> doc_002702,concept_0052
> doc_008782,concept_0004
> Requirements
> Output exactly 2,081 data rows — one per id in test.csv.gz. The id set must match the test set exactly: no missing ids, no extra ids, no duplicates. Rows may appear in any order.
> The file must have exactly the two columns id and labels (column names are matched case-insensitively). Any additional column is rejected — write your CSV without a row-index column (e.g. df.to_csv(path, index=False)). The grader also accepts id supplied as the CSV index instead of a column.
> Serialize each prediction as pipe-separated concept tokens. Only the | character separates tokens; tokens themselves never contain |.
> Predicted tokens outside the 78-tag vocabulary are allowed but can only reduce precision (they never match a gold tag). Predict at least one tag per row; an empty prediction scores 0 for that document.
> Tags are matched case-insensitively after whitespace trimming; a missing or empty labels cell is treated as an empty prediction (scores 0 for that row).
> What not to use
> This must be solved as a text-modeling problem on the provided data only:
> Train only on public/train.csv.gz. Do not use any external dataset, and do not access the network or any external service at solve time (the run harness provides no network).
> Do not attempt to look up, search for, or otherwise identify the original source documents online, and do not try to reverse-engineer the split, the tag vocabulary, or the answer key. The document ids and concept tags are anonymized precisely so that no external lookup can recover the labels — predictions must come from your own model trained on the provided text.
> General-purpose, offline, pre-existing language models and embeddings may be used to represent the text, but the prediction of a document's tag set must be produced by your own model.

Inspiration note: Useful because it turns nuanced language understanding or extraction into a compact target with clear schema and scoring.

## Entity Extraction from Transformed Astrophysics Literature
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx747e6e3n00mnw02fw0pmmh0h89sncx
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, clustering, generative
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Build a token-classification model for astronomy and astrophysics literature. Each example is a window from a scientific article paragraph. The text has been converted into a leakage-controlled token stream: common function words and punctuation remain readable, while most content words are represented as stable shape-preserving lexical codes such as lex_1a2b3c4_CAP_L.
> The real-world scenario is scientific information extraction under distribution drift. Astronomers and digital-library teams need to identify instruments, missions, citations, formulas, grants, observatories, wavelengths, celestial objects, and related entities in long technical prose. This challenge keeps the scientific sequence-labeling structure, but removes direct source IDs and exact public token strings so the test labels cannot be recovered by matching rows against the original public corpus.
> The prepared public data has 15,678 labeled training windows and 4,364 unlabeled test windows. Windows are split by source article group before segmentation, so content from the same article is not shared across train and test.
> Evaluation
> Submissions are scored with a weighted composite metric. Higher is better.
> 0.70 * strict_typed_entity_micro_f1
> + 0.20 * rare_entity_type_macro_f1
> + 0.10 * boundary_micro_f1
> Definitions:
> strict_typed_entity_micro_f1: an entity is correct only when start token, end token, and entity type all match.
> rare_entity_type_macro_f1: macro F1 over rare scientific/document entity types such as Archive, Dataset, Grant, Observatory, Proposal, Survey, URL, and related low-frequency classes.
> boundary_micro_f1: span boundary F1 ignoring type, included to reward correct segmentation even when a difficult type is confused.
> Invalid BIO transitions are repaired only for scoring by converting invalid I-X tags to B-X. If more than 1% of predicted tags require repair, the final score receives a 2% penalty. Unknown tag values fail validation.
> Dataset
> The prepared public data contains:
> public/
> ├── train.csv
> ├── test.csv
> └── sample_submission.csv
> train.csv columns:
> test.csv columns:
> The tokens column is a JSON array inside a CSV cell. The token strings are not raw article tokens. They preserve useful sequence cues such as repeated lexical identity, capitalization class, approximate length, punctuation, URLs, and numeric shape, but are designed to prevent direct source-text lookup.
> Label Space
> Use BIO tags with O for non-entity tokens. Every entity type can appear with B- and I- prefixes:
> Allowed tag examples: O, B-Instrument, I-Instrument, B-Citation, I-Citation, B-Wavelength, I-Wavelength.
> Submission
> Submit a CSV file named submission.csv:
> Requirements:
> Include exactly one row for each row in test.csv.
> Include the header row.
> Do not include duplicate IDs.
> Each predicted tag list must have the same length as the corresponding token list.
> Tags must be O or a valid B-/I- tag from the label space above.
> Example:
> id,tags
> ast_01d3b25549f04fa7,"[""O"", ""B-Instrument"", ""O"", ""B-Citation"", ""I-Citation""]"
> ast_0f874c70a6b7d2b1,"[""O"", ""O"", ""B-Wavelength"", ""I-Wavelength""]"

Inspiration note: Useful because it turns nuanced language understanding or extraction into a compact target with clear schema and scoring.

## Biodiversity Occurrence Coordinate Reconstruction
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ba9885vknn1z7gtqt7z9fsh89rr1w
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Biodiversity occurrence records describe where an organism was observed or collected. In this challenge, each example is an anonymized text card describing broad occurrence evidence such as country, continent, taxonomic context, occurrence basis, curation-note density, event timing, and bucketed curation profiles.
> Your task is to reconstruct the hidden decimal latitude and longitude for the occurrence record. The public card deliberately does not include coordinate bands, exact locality, source occurrence ids, species names, collector names, or dataset keys.
> This is a text-grounded geolocation reconstruction task. Good solutions should learn spatial regularities from the training cards while handling held-out taxonomic names and noisy occurrence metadata.
> Dataset
> The prepared files are:
> train.csv: Text-card references plus the reference answer_json.
> test.csv: Held-out text-card references without coordinates.
> cards/: Plain-text occurrence evidence cards referenced by the CSV files.
> sample_submission.csv: A deliberately weak valid coordinate submission example.
> CSV fields:
> id: Opaque row id.
> evidence_file: Relative path to the plain-text card under cards/.
> prompt: Row instruction.
> answer_json: Training only. The hidden coordinate object.
> Each evidence card contains coarse natural-language evidence:
> Country code and continent.
> Occurrence basis.
> Broad kingdom and class group.
> Taxonomic-depth and name-interpretation hints.
> Coordinate-uncertainty reporting level.
> Interpretation-note density.
> Event-date detail and coarse event-day slot.
> Query, issue-family, taxon-lineage, dataset-curation, institution, collection, recorder-team, and identifier-team buckets. These are lossy buckets, not source identifiers or names.
> The card does not contain exact coordinates or coordinate bands.
> Submission Format
> Submit a CSV with exactly two columns: id and answer_json. Column order does not matter, but missing columns, extra columns, duplicate ids, missing ids, wrong ids, wrong row counts, malformed JSON, and invalid values are rejected.
> answer_json must be valid JSON with exactly these numeric keys:
> latitude: decimal latitude in [-90, 90].
> longitude: decimal longitude in [-180, 180].
> Example:
> id,answer_json
> occ_geo_example_1,"{""latitude"":32.74006,""longitude"":35.69904}"
> Evaluation
> The score is based on great-circle distance between the submitted coordinate and the reference coordinate.
> For each row:
> distance_km = haversine_distance(submitted_coordinate, reference_coordinate)
> row_score = max(0, 1 - distance_km / 75)
> Haversine distance
> Given two coordinates (lat1, lon1) and (lat2, lon2) in degrees, the great-circle distance is:
> φ1, φ2   = radians(lat1), radians(lat2)
> Δφ       = radians(lat2 - lat1)
> Δλ       = radians(lon2 - lon1)
> a = sin²(Δφ / 2) + cos(φ1) · cos(φ2) · sin²(Δλ / 2)
> distance_km = 2 · R · asin(min(1, √a))
> where R = 6371.0088 km is the mean Earth radius.
> The final score is:
> final_score = mean(row_score) over all private test rows.
> A perfect private-answer submission scores exactly 1.0; predictions at least 75 km away receive 0.0 for that row.
> What Not To Use
> External lookup of public test rows in public occurrence databases.
> Exact coordinates, source occurrence ids, dataset keys, publishing organization ids, species names, collector names, identifier names, private answer files, or generation internals.
> Hardcoded mappings from row ids, file names, row order, or repeated text cards to private coordinates.

Inspiration note: Useful because it turns nuanced language understanding or extraction into a compact target with clear schema and scoring.

## French Biomedical Cloze Arbitration
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx798a0h21anp3fdjry8v49h5989s8yk
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↓ Lower is better
- Tags: Not shown/captured
- Best/top context found: Added from user-provided Shipd challenge URL batch on 2026-07-04; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> You are given a French biomedical passage and a cloze question with one [MASK] span. Each row contains two candidate biomedical entities from the same source context. Predict the probability that candidate A is the better fill for the masked span.
> This is a biomedical language-understanding task. Strong solutions should use the passage, the masked question, and both candidates together rather than relying on candidate frequency or option position.
> Direct mentions of the two candidates in the passage are redacted as [CANDIDATE_ENTITY], so candidate mention counts and first-occurrence positions are not useful shortcuts. Other source entities are shown only as row-local placeholders such as [ENTITY_0], preserving coreference without exposing biomedical names from the source passage.
> Dataset
> File descriptions:
> train.csv -- Labeled French biomedical cloze rows with a passage, question, two candidates, and the correct option.
> test.csv -- Unlabeled rows with the same fields but without the correct option.
> sample_submission.csv -- Example submission with random valid probabilities.
> Column descriptions:
> id -- Unique hashed row identifier.
> passage -- French biomedical context passage.
> question -- French cloze question containing [MASK] and row-local entity placeholders.
> candidate_a -- First candidate entity.
> candidate_b -- Second candidate entity.
> correct_option -- Training target only. The correct candidate, either A or B.
> Evaluation
> Submissions are scored by binary log loss on the probability assigned to candidate A:
> y = 1 if correct_option == "A" else 0
> score = mean(-(y  *log(probability_a) + (1 - y)*  log(1 - probability_a)))
> Lower is better. Probabilities are clipped only inside the grader for numerical stability.
> Submission
> Submit a CSV file with one probability for every row in test.csv.
> id -- The row identifier from test.csv.
> probability_a -- A numeric probability from 0 to 1 that candidate A is correct.
> Example:
> id,probability_a
> 00187f2a9f0c,0.731
> 0032d6ab11ad,0.284
> 00664ef5ad79,0.512
> Requirements:
> Include exactly the columns id,probability_a.
> Include every test id exactly once.
> Keep probability_a finite and between 0 and 1.
> Write the final file to ./working/submission.csv.
> What not to use:
> Do not search for external mirrors or source answer keys for held-out rows.
> Do not infer labels from candidate position, row order, hashed ids, or source split artifacts.
> Do not submit hard-coded memorization of public examples.
> Do not ignore the passage and masked question when estimating candidate probabilities.

Inspiration note: Useful because it turns language understanding into a compact, schema-constrained prediction target with clear scoring.

## Biomedical Evidence Slot Reconstruction
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73zjz079q3vthjg33rj2cq3589rh9q
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↓ Lower is better
- Tags: Not shown/captured
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Scientific paragraphs often lose a key evidence fragment during extraction, summarization, or note assembly. The useful model is not just a claim verifier: it must decide where a missing biomedical evidence fragment belongs inside the surrounding paragraph flow.
> For each example, you are given a local paragraph window with numbered insertion slots and one withheld evidence fragment. The public text is a row-local lexical sketch: each visible fragment is reduced to two coarse bucket tokens, so exact prose and source wording are not exposed. Predict the slot where the evidence sketch should be inserted. Strong solutions should use row-internal bucket continuity and paragraph-position patterns rather than treating this as a multiple-choice claim task.
> The hidden split holds out complete document groups, so rows from the same source document do not appear in both training and test.
> Dataset
> File descriptions
> train.csv -- 813 labeled examples. Each row contains a local paragraph window with slot markers, a withheld evidence fragment, the number of valid slots, and the correct JSON insertion plan.
> test.csv -- 264 unlabeled examples with the same input columns as train.csv, but without insertion_plan.
> sample_submission.csv -- A template showing the required id and insertion_plan columns with random valid slot choices.
> Column descriptions
> id (string) -- Unique 12-character hashed identifier for each example.
> paragraph_with_slots (string) -- Row-local bucket sketch of a biomedical paragraph after one evidence fragment has been removed. Valid insertion points, including within-sentence positions, are marked as [SLOT_0], [SLOT_1], and so on.
> evidence_sentence (string) -- The withheld row-local evidence sketch that must be inserted back into the paragraph.
> slot_count (integer) -- Number of valid insertion slots for the row. Valid slot values are integers from 0 through slot_count - 1.
> insertion_plan (string) -- Correct JSON insertion plan in train.csv only. Format: {"slot": <integer>}.
> Evaluation
> Submissions are scored with composite insertion loss. Lower is better.
> def row_loss(predicted_slot, gold_slot, slot_count):
> max_error = max(gold_slot, slot_count - 1 - gold_slot, 1)
> ordinal_loss = abs(predicted_slot - gold_slot) / max_error
> exact_miss_loss = 0.0 if predicted_slot == gold_slot else 1.0
> return 100.0  *(0.70*  ordinal_loss + 0.30 * exact_miss_loss)
> The final score is the mean row loss over all test rows. A perfect submission scores 0. A valid but randomly sampled slot baseline scores about 57.
> Submission
> Submit a CSV file with one JSON insertion plan for every row in test.csv.
> id (string) -- The row identifier from test.csv.
> insertion_plan (string) -- JSON object with exactly one key, slot, whose value is an integer from 0 through slot_count - 1 for that row.
> Example:
> id,insertion_plan
> e205d161e3b8,"{""slot"":3}"
> 7b08362126e6,"{""slot"":4}"
> 3bc56285731f,"{""slot"":3}"
> Requirements
> The file must contain exactly 264 rows plus the header.
> Every id from test.csv must be present exactly once.
> Every insertion_plan value must be valid JSON with exactly one integer field named slot.
> The predicted slot must be in range for that row: 0 <= slot < slot_count.
> File format: .csv only, with exact column names id,insertion_plan.
> What Not To Use
> Do not try to reconstruct the hidden prose behind the public bucket sketches using web search, cached maps, or external corpus lookup. The task is to model insertion from the provided public files.
> Do not use cached row maps, mirrored corpora, sketch-to-source matches, or lookup tables to link public rows back to hidden insertion slots.
> Do not submit a fixed-position heuristic as the primary method. The split and metric are designed to require row-specific discourse and biomedical-context modeling.

Inspiration note: Useful because it turns messy language evidence into a crisp span, class, ranking, or structured-output target with measurable scoring.

## Customer Support Ticket Multi-Output Outcome Forecasting
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78nt8xcbmney43qwvzzc3e5h82xkw4
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, large-scale, generative, reinforcement-learning
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Modern customer-support systems must decide what is likely to happen immediately after a customer submits a ticket. This challenge simulates a real operational setting where early predictions influence routing, escalation, automation, and retention workflows.
> Given one noisy customer-support message plus lightweight historical metadata, participants must forecast three future-facing behavioural outcomes at ticket-arrival time.
> Plaintext
> +----------------------+-----------------+-----------------------------------------------------------------------+
> | Target               | Type            | What the model must infer                                             |
> +----------------------+-----------------+-----------------------------------------------------------------------+
> | Emotional_Trajectory | Multi-class, 3  | Whether customer emotion will stabilize, escalate, or de-escalate     |
> | Resolution_Channel   | Multi-class, 4  | Which support pathway should handle the ticket                        |
> | Recurrence_Risk      | Multi-class, 3  | Whether the issue is isolated, repeated, or chronic                   |
> +----------------------+-----------------+-----------------------------------------------------------------------+
> Public features exclude post-resolution information such as agent replies, final status, feedback, and resolution time. The main feature, Customer_Query_Text, contains informal, noisy support language with urgency cues, typos, abbreviations, and escalation context. Strong solutions must combine semantic text understanding with temporal customer-history features.
> Why This Challenge Is Difficult
> This is not a single-label support classifier. It is a coordinated multi-output forecasting task under temporal drift.
> Plaintext
> +-----------------+---------------------------+----------------------------------------------------------+
> | Dimension       | Common Support Benchmark  | This Challenge                                           |
> +-----------------+---------------------------+----------------------------------------------------------+
> | Prediction time | After resolution          | At the exact moment the ticket arrives                   |
> | Task shape      | One target                | Three coordinated future outcomes                        |
> | Text style      | Clean text                | Noisy support messages with typos and informal phrasing  |
> | Context         | Current ticket only       | Current text plus prior interaction history              |
> | Evaluation      | Plain accuracy/macro-F1   | Strict full-row, critical-row, rare-class, and temporal  |
> | Split           | Random split              | Strict future holdout by timestamp                       |
> | Business risk   | Generic classification    | Missed escalation and chronic risk are heavily penalized |
> +-----------------+---------------------------+----------------------------------------------------------+
> Dataset Summary
> Plaintext
> +-------------------------+----------------------------------------------------+
> | Property                | Value                                              |
> +-------------------------+----------------------------------------------------+
> | Raw source rows         | 1,200                                              |
> | Public train rows       | 720                                                |
> | Public test rows        | 480                                                |
> | Split type              | Strict temporal split                              |
> | Train timestamp range   | 2025-12-02T12:21:19 to 2026-01-13T13:40:19         |
> | Test timestamp range    | 2026-01-13T14:15:19 to 2026-02-09T20:53:19         |
> | Synthetic customers     | 200 pseudo-customers                               |
> | Unique train texts      | 714 unique Customer_Query_Text values              |
> | Missing history values  | Only first-contact train rows contain history NaNs |
> | Public targets          | Present in train.csv, withheld from test.csv       |
> +-------------------------+----------------------------------------------------+
> Files Provided
> Plaintext
> +-----------------------+------+------+----------------------------------------------------------------+
> | File                  | Rows | Cols | Description                                                    |
> +-----------------------+------+------+----------------------------------------------------------------+
> | train.csv             | 720  | 16   | Public labelled training data with all features and targets    |
> | test.csv              | 480  | 13   | Public unlabelled test data with targets removed               |
> | sample_submission.csv | 480  | 4    | Submission template; row order must be preserved exactly       |
> | answers.csv           | 480  | 5    | Private labels used only by the grader                         |
> +-----------------------+------+------+----------------------------------------------------------------+
> Training Columns
> Plaintext
> +-------------------------+----------+----------+-------------------------------------------------------+
> | Column                  | Type     | Nullable | Description                                           |
> +-------------------------+----------+----------+-------------------------------------------------------+
> | Ticket_ID               | string   | No       | Anonymised ticket identifier, format TID######        |
> | Customer_Country        | category | No       | Customer country                                      |
> | Customer_Language       | category | No       | Customer language                                     |
> | Channel                 | category | No       | Support channel: chat, email, web, or WhatsApp        |
> | Query_Category          | category | No       | Broad issue category                                  |
> | Query_Subcategory       | category | No       | More specific issue subtype                           |
> | Customer_Query_Text     | text     | No       | Main NLP feature: noisy customer message              |
> | Sentiment_Score         | float    | No       | Current message sentiment in [-1.0, 1.0]              |
> | Timestamp               | datetime | No       | Used for strict temporal ordering                     |
> | Prior_Ticket_Count      | integer  | No       | Number of earlier messages from this pseudo-customer  |
> | Days_Since_Last_Contact | float    | Yes      | Days since previous message; NaN on first contact     |
> | Prior_Avg_Sentiment     | float    | Yes      | Mean sentiment over prior messages; NaN on first      |
> | Prior_Unresolved_Count  | integer  | No       | Count of prior unresolved high-touch interactions     |
> | Emotional_Trajectory    | category | No       | Target 1                                              |
> | Resolution_Channel      | category | No       | Target 2                                              |
> | Recurrence_Risk         | category | No       | Target 3                                              |
> +-------------------------+----------+----------+-------------------------------------------------------+
> Test Columns
> test.csv has the same feature columns as train.csv, but without the three target columns. The submission must copy Ticket_ID values from sample_submission.csv exactly.
> Target Labels
> 1. Emotional_Trajectory
> Plaintext
> +---------------+------------------------------------------------------+-------------+
> | Label         | Meaning                                              | Train Count |
> +---------------+------------------------------------------------------+-------------+
> | Stable        | Customer emotion is expected to remain steady        | 375         |
> | Escalating    | Frustration or urgency is likely to increase         | 257         |
> | De-escalating | Customer is likely to calm down with correct handling| 88          |
> +---------------+------------------------------------------------------+-------------+
> 2. Resolution_Channel
> Plaintext
> +----------------+------------------------------------------------------+-------------+
> | Label          | Meaning                                              | Train Count |
> +----------------+------------------------------------------------------+-------------+
> | Self-Service   | Documentation, FAQ, or self-help is enough           | 209         |
> | Bot-Resolvable | A normal bot workflow can resolve the ticket         | 293         |
> | Specialist     | Domain expert or deep technical support is needed    | 33          |
> | Executive      | Senior, retention, or high-risk handling is needed   | 185         |
> +----------------+------------------------------------------------------+-------------+
> 3. Recurrence_Risk
> Plaintext
> +------------------+---------------------------------------------------+-------------+
> | Label            | Meaning                                           | Train Count |
> +------------------+---------------------------------------------------+-------------+
> | First-Occurrence | The current issue appears isolated                | 406         |
> | Repeat-Pattern   | Similar friction is appearing again               | 266         |
> | Chronic          | Long-running unresolved negative pattern          | 48          |
> +------------------+---------------------------------------------------+-------------+
> Submission Format
> Submissions must be CSV files with exactly four columns in exactly this order:
> Code snippet
> Ticket_ID,Emotional_Trajectory,Resolution_Channel,Recurrence_Risk
> TID000001,Stable,Bot-Resolvable,First-Occurrence
> TID000002,Escalating,Executive,Chronic
> TID000003,De-escalating,Specialist,Repeat-Pattern
> Plaintext
> +----------------------+----------------------------------------------------------+
> | Column               | Valid Values                                             |
> +----------------------+----------------------------------------------------------+
> | Ticket_ID            | Must exactly match sample_submission.csv                 |
> | Emotional_Trajectory | Stable, Escalating, De-escalating                        |
> | Resolution_Channel   | Self-Service, Bot-Resolvable, Specialist, Executive      |
> | Recurrence_Risk      | First-Occurrence, Repeat-Pattern, Chronic                |
> +----------------------+----------------------------------------------------------+
> Evaluation Metric
> The official metric is a strict temporal critical-row score. It is intentionally harder than ordinary macro-F1 because support systems must get the full operational decision correct, especially for high-risk customers.
> Rows are sorted by private timestamp and split into two equal temporal tiers:
> Plaintext
> +------------+------+--------------+
> | Tier       | Rows | Final Weight |
> +------------+------+--------------+
> | Older half | 240  | 0.25         |
> | Newer half | 240  | 0.75         |
> +------------+------+--------------+
> Note: The newer half receives higher weight to reward robustness under future concept drift.
> Per-Tier Formula
> Plaintext
> Score_Tier = 0.45 * Full_Row_Exact_Match
> + 0.20 * Critical_Row_Exact_Match
> + 0.15 * Harmonic_Field_Macro_F1
> + 0.10 * Rare_Class_Recall
> + 0.10 * Emotional_Cost_Accuracy
> Final_Score = 0.25 * Score_Older_Half + 0.75 * Score_Newer_Half
> Metric Components
> Plaintext
> +--------------------------+--------------------------------------------------------------------------+
> | Component                | Meaning                                                                  |
> +--------------------------+--------------------------------------------------------------------------+
> | Full_Row_Exact_Match     | All three target columns must be correct on the same row                 |
> | Critical_Row_Exact_Match | Full-row exact match only on high-risk rows                              |
> | Harmonic_Field_Macro_F1  | Harmonic mean of the three target-level macro-F1 scores                  |
> | Rare_Class_Recall        | Average recall on high-value rare classes                                |
> | Emotional_Cost_Accuracy  | Cost-normalised emotional accuracy with heavier penalties for misses     |
> +--------------------------+--------------------------------------------------------------------------+
> Critical Conditions
> A critical row is any private test row where at least one of these is true:
> Plaintext
> +-------------------------------------------------+
> | Critical Condition                              |
> +-------------------------------------------------+
> | True Emotional_Trajectory is Escalating         |
> | True Resolution_Channel is Specialist           |
> | True Resolution_Channel is Executive            |
> | True Recurrence_Risk is Chronic                 |
> +-------------------------------------------------+
> Rare-Class Recall Targets
> Plaintext
> +----------------------+-------------------------+
> | Target Column        | Rare / High-Value Class |
> +----------------------+-------------------------+
> | Emotional_Trajectory | De-escalating           |
> | Resolution_Channel   | Specialist              |
> | Resolution_Channel   | Executive               |
> | Recurrence_Risk      | Chronic                 |
> +----------------------+-------------------------+
> Emotional Mistake Costs
> Wrong emotional predictions are not treated equally. Missing an escalating customer is the most dangerous error.
> Plaintext
> +---------------+-----------------+--------------+
> | True Label    | Predicted Label | Mistake Cost |
> +---------------+-----------------+--------------+
> | Stable        | Escalating      | 1.20         |
> | Stable        | De-escalating   | 1.10         |
> | Escalating    | Stable          | 2.00         |
> | Escalating    | De-escalating   | 1.60         |
> | De-escalating | Stable          | 1.10         |
> | De-escalating | Escalating      | 1.35         |
> +---------------+-----------------+--------------+
> Strict Validation Rules
> The grader rejects submissions that violate any of these rules:
> Plaintext
> +-----+-----------------------------------------------------------------------------+
> | No. | Rule                                                                        |
> +-----+-----------------------------------------------------------------------------+
> | 1   | The CSV must contain exactly the four required columns and no others        |
> | 2   | Column order must match sample_submission.csv exactly                       |
> | 3   | Every Ticket_ID must match the private answer file exactly                  |
> | 4   | Row order must remain unchanged                                             |
> | 5   | Duplicate Ticket_ID values are rejected                                     |
> | 6   | Missing or blank predictions are rejected                                   |
> | 7   | Labels must use exact canonical spelling, hyphenation, and casing           |
> | 8   | Extra index columns such as Unnamed: 0 are rejected                         |
> +-----+-----------------------------------------------------------------------------+
> Recommended Modelling
> Strong solutions should treat this as a structured multi-output NLP forecasting task. Useful approaches include transformer text encoders, multi-task classification heads, class-balanced losses, temporal validation splits, and calibration/error analysis for critical rows.
> What Not To Use
> Do not use post-resolution fields, hidden target columns, external lookup tables, row-order tricks, hard-coded answer maps, manually reverse-engineered private labels, or leakage from the private answer file. Simple majority-class baselines and isolated threshold rules are unlikely to score well under the strict full-row and critical-row metric.

Inspiration note: Useful because it turns messy language evidence into a crisp span, class, ranking, or structured-output target with measurable scoring.

## Dialogue State Continuation Ranking
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73ztx29ma3mvm60w32sbsj0x88mewj
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↓ Lower is better
- Tags: text
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Customer service conversations often fail when an assistant gives a fluent reply that does not fit the current dialogue state. The next response must respect the user's latest request, the slots already collected, and the stage of the service workflow. This challenge asks you to rank five candidate assistant continuations for each dialogue context.
> Each row contains a redacted conversation context and five real assistant replies. Slot values such as locations, names, times, and counts have been replaced by slot-type placeholders, so exact entity matching is not enough. A good solution needs to model the transition implied by the dialogue state: asking for a missing detail, presenting a valid option, rejecting an unavailable choice, or committing to a completed action.
> This is a ranking task. Your submission should order the five options from best continuation to worst continuation. The hidden grader gives most credit for placing the true next assistant turn first, but it also gives partial credit for putting close near-misses above weaker distractors.
> Dataset
> File descriptions
> train.csv -- 1,000 dialogue-ranking examples. Each row contains a redacted dialogue context, five candidate assistant continuations, and the labeled ideal_order.
> test.csv -- 450 dialogue-ranking examples with the same input columns as train.csv, but without ideal_order.
> sample_submission.csv -- A template showing the required submission format with id and option_order, filled with random option permutations.
> Column descriptions
> id (string) -- Unique 12-character hex identifier for each ranking example.
> service_family (string) -- Coarse service workflow family for the conversation.
> context_turns (integer) -- Number of recent turns included in dialogue_context.
> slot_count_before (integer) -- Number of distinct redacted slot types observed before the candidate continuation.
> dialogue_context (string) -- Recent conversation history with speaker labels and redacted slot values.
> option_A (string) -- Candidate assistant continuation A.
> option_B (string) -- Candidate assistant continuation B.
> option_C (string) -- Candidate assistant continuation C.
> option_D (string) -- Candidate assistant continuation D.
> option_E (string) -- Candidate assistant continuation E.
> ideal_order (string) -- Training-only pipe-separated option ranking from best to worst, such as C|A|E|B|D.
> Evaluation
> Submissions are scored using transition-weighted normalized rank loss. Lower is better. A score of 0 is the ideal ranking for every row, while 100 is the worst valid ranking for every row.
> For each row, the hidden answers contain graded relevance values for the five options. The actual next assistant turn has the highest relevance. A close near-miss from the same workflow stage has lower relevance, and weaker distractors have lower or zero relevance. Rows whose true continuation contains slot evidence or a commitment action receive slightly higher weight than simple acknowledgement turns.
> The row loss is normalized by the true best and worst possible option orders:
> import math
> def dcg(order, relevance):
> total = 0.0
> for rank, label in enumerate(order, start=1):
> rel = relevance[label]
> total += (2 ** rel - 1) / math.log2(rank + 1)
> return total
> def row_loss(predicted_order, relevance):
> ideal = sorted("ABCDE", key=lambda label: (-relevance[label], label))
> worst = sorted("ABCDE", key=lambda label: (relevance[label], label))
> best_dcg = dcg(ideal, relevance)
> worst_dcg = dcg(worst, relevance)
> if best_dcg == worst_dcg:
> return 0.0
> return (best_dcg - dcg(predicted_order, relevance)) / (best_dcg - worst_dcg)
> def evaluate(rows):
> weighted_loss = sum(row.weight * row_loss(row.order, row.relevance) for row in rows)
> return 100 * weighted_loss / sum(row.weight for row in rows)
> Submission
> Submit a CSV file with one ranked option list for every row in test.csv.
> id (string) -- The 12-character hex identifier from test.csv.
> option_order (string) -- A pipe-separated permutation of A, B, C, D, and E, ordered from best continuation to worst continuation.
> Example:
> id,option_order
> 00cc0a7ae397,A|D|C|E|B
> 015b794e972c,C|A|E|B|D
> 01850ca81ef4,D|B|A|C|E
> Requirements
> The file must contain exactly 450 rows plus the header.
> Every id from test.csv must be present exactly once.
> option_order must contain each option label exactly once.
> File format: .csv only, with exact column names id,option_order.
> What Not To Use
> Do not use external copies, mirrors, or search-engine results that contain the exact underlying conversations. That bypasses the intended dialogue-state ranking problem by recovering held-out next turns.
> Do not rely on conversation identifiers, row order, hidden file names, or other reverse maps from the public examples to external dialogue records.
> Do not submit a pure hardcoded or template-only ranker based on option letters, text frequency, or fixed response phrases. The public options are frequency-balanced, and the task is meant to reward learned context-response matching.
> Do not manually label the test rows by searching distinctive snippets from the dialogue context or candidate responses.

Inspiration note: Useful because it turns messy language evidence into a crisp span, class, ranking, or structured-output target with measurable scoring.

## Recovering the Anagram Fodder in a Cryptic Crossword Clue
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx754brbm3nrhjn5t6q99sv1k589vn65
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> In a cryptic crossword, every clue stitches together a definition of the answer and some wordplay that spells the answer a second way. One of the most common wordplay devices is the anagram: a run of words in the clue -- the fodder -- whose letters are rearranged to form the answer, signalled by an anagram indicator (a word like shredded, cooked, wild, drunk, at sea that hints at scrambling).
> For example, in the clue
> Chaperone shredded corset
> the answer is ESCORT. Here Chaperone is the definition, shredded is the anagram indicator, and corset is the fodder -- rearrange the letters of corset and you get escort.
> Your task is not to solve the clue (you never need the answer). Your task is to recover the fodder: output the exact contiguous run of clue words whose letters are anagrammed into the answer. The hard part is telling the fodder apart from the definition and the indicator: the fodder can sit anywhere in the clue, be one word or several, and the clues are given without the answer's letter-count, so you cannot simply look for a run of the right length -- you have to understand the clue's structure.
> Data
> train.csv -- the training pairs. Columns:
> clue -- the cryptic clue text (presented without the answer enumeration).
> fodder -- the gold anagram fodder for that clue: the contiguous run of clue words that anagrams into the answer. This is the only supervision you may train on.
> test.csv -- the query items. Columns:
> item_id -- opaque unique id for the query.
> clue -- the cryptic clue text. Predict its anagram fodder. The test clues come from different setters than the training clues (see Notes), so your model must generalize across cryptic-crossword styles.
> sample_submission.csv -- a valid submission with fodder set to the first word of each clue (a dummy baseline that scores low but above zero).
> Every clue in the data is a genuine anagram clue: exactly one contiguous run of its words anagrams into the answer, and that run is the target.
> Task
> For each item_id in test.csv, read the clue and output the fodder -- the contiguous run of words whose letters rearrange into the answer.
> Evaluation
> Exact fodder accuracy -- the fraction of query clues whose predicted fodder exactly matches the gold fodder after normalization:
> accuracy = mean( normalize(predicted) == normalize(gold) )   over all queried clues
> Normalization extracts the letter-only word tokens, lowercases them, and joins them with single spaces (so casing, surrounding punctuation and apostrophes do not matter). Within those bounds the match is exact: you must recover the correct contiguous set of fodder words, in order. A prediction that is off by one word, includes the indicator, or grabs the definition scores zero for that item. Higher is better; the score is in [0, 1].
> Submission format
> A CSV with exactly two columns:
> item_id -- every item_id from test.csv, each exactly once.
> fodder -- your predicted fodder span (a contiguous stretch of the clue text).
> Example:
> item_id,fodder
> CAF_ade4e7d4c26e,corset
> CAF_0b3d824bc723,brains a
> Requirements (violations are rejected as invalid submissions):
> Exactly the columns item_id,fodder, in that order.
> No missing, duplicate, or extra item_id; every required item_id present exactly once.
> fodder must be a non-empty string containing at least one word, with no nulls.
> Allowed
> Fine-tuning a pretrained language model (e.g. a masked or sequence-to- sequence encoder) on the provided train.csv pairs to tag or extract the fodder span, or training a sequence tagger / boundary classifier from scratch on the same pairs.
> Using the full clue text as context and any features you derive from it (token positions, capitalization, punctuation, part-of-speech, candidate anagram indicators, letter statistics, and so on).
> Deterministic post-processing of your model's output (e.g. snapping the prediction to the nearest contiguous run of clue words).
> Prohibited
> No external cryptic-crossword databases, published clue/answer/annotation collections, answer keys, or online cryptic solvers/lookups. The fodder must be inferred from the clue text and the provided training pairs only.
> Do not look up a clue, its answer, or its published annotation anywhere outside this dataset, and do not attempt to identify the source collection and retrieve an external copy of it.
> No use of any answer/label file; the fodder must be predicted by your model, not read from the gold spans.

Inspiration note: Useful because it turns messy language evidence into a crisp span, class, ranking, or structured-output target with measurable scoring.

## Python Library API Drift Forecasting Triage
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70h0e052rwbwmgsrnw45pky589vm4x
- DOMAIN exactly as displayed: NLP
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Predict a structured next-release API drift card from a natural-language report about an anonymized Python library snapshot. Each report describes the current API surface, recent movement from the previous release, frequent symbol tokens, and a forecast horizon. A good solution must infer how the next release is likely to change: whether the API grows or contracts, whether classes/functions/methods shift, whether call signatures become simpler or more complex, and how risky that next release is for downstream migration tooling.
> This is an NLP/code-metadata forecasting challenge. The useful signal is expressed as compact text reports about Python API surfaces, not as raw source files or package names. The task is relevant to LLM pretraining corpus curation, IDE autocomplete metadata quality, static-analysis tooling, and package-migration planning.
> Dataset
> The prepared data contains 420 training rows and 150 hidden test rows. The source subset is derived from 685 MIT-licensed pylibsmeta package-version snapshots and 570 adjacent-version pairs. The prepared size is intentionally bounded: enough rows for pattern learning, far below 1,000,000 rows, and small enough for weak devices.
> You receive these public files:
> train.jsonl: labeled training reports.
> test.jsonl: hidden evaluation reports without target cards.
> sample_submission.csv: schema-valid dummy submission.
> Each row in train.jsonl is one JSON object with these fields:
> id: string row identifier.
> api_snapshot_report: natural-language report for one anonymized package-version snapshot and forecast horizon.
> api_drift_card: string target card for training rows only.
> Each row in test.jsonl has the same public fields except it does not include api_drift_card.
> Example training-style row:
> {"id":"train_00001","api_snapshot_report":"An anonymized Python package snapshot belongs to package group 9a13c122f011 at encoded version 000100000000. The requested forecast horizon is 4 release steps. Current API surface summary: 812 extracted symbols, 115 classes, 221 top-level functions, 942 methods, average callable arity 2.410, maximum callable arity 12, variadic callable share 0.0440, and 3 async-related symbol hints. Previous-release movement: symbol delta +0.0620, method delta +0.1180, and average-arity delta +0.2100. Frequent API symbol tokens: client request response config session auth token endpoint handler.","api_drift_card":"size_delta=expand;object_shift=method_gain;call_shift=more_config;migration_risk=high"}
> Example test-style row:
> {"id":"test_00001","api_snapshot_report":"An anonymized Python package snapshot belongs to package group 2d0080d5c15a at encoded version 000200010000. The requested forecast horizon is 8 release steps. Current API surface summary: 143 extracted symbols, 8 classes, 89 top-level functions, 51 methods, average callable arity 1.720, maximum callable arity 7, variadic callable share 0.0110, and 0 async-related symbol hints. Previous-release movement: symbol delta -0.0140, method delta +0.0000, and average-arity delta -0.0900. Frequent API symbol tokens: path file parse option command logger main."}
> Submission Format
> Submit a CSV with exactly these columns in this order:
> id,api_drift_card
> The id column is a string test identifier. The api_drift_card column is a semicolon-delimited string with exactly four slots in this order:
> size_delta=<size>;object_shift=<shift>;call_shift=<call>;migration_risk=<risk>
> Example submission rows:
> test_00001,size_delta=stable;object_shift=balanced;call_shift=stable;migration_risk=low
> test_00002,size_delta=surge;object_shift=method_gain;call_shift=more_async;migration_risk=volatile
> Every test id must appear exactly once. Duplicate ids, missing ids, unknown ids, wrong columns, malformed cards, invalid slot order, invalid slot values, empty cards, NaN or infinity values, and cards longer than 170 characters are invalid.
> Allowed Card Values
> Allowed size_delta values are:
> contract
> stable
> expand
> surge
> Allowed object_shift values are:
> class_gain
> function_gain
> method_gain
> balanced
> Allowed call_shift values are:
> simpler
> stable
> more_config
> more_async
> Allowed migration_risk values are:
> low
> medium
> high
> volatile
> Evaluation
> The score is weighted slot accuracy averaged across hidden test rows. Higher is better. The finite score range is 0.0 to 1.0.
> Per-slot weights are explicit:
> size_delta weight = 0.32.
> object_shift weight = 0.24.
> call_shift weight = 0.21.
> migration_risk weight = 0.23.
> For each row, compute row_score = 0.32 times the size_delta exact-match indicator, plus 0.24 times the object_shift exact-match indicator, plus 0.21 times the call_shift exact-match indicator, plus 0.23 times the migration_risk exact-match indicator.
> These four weights sum to exactly 1.0, so a row with all four slots correct receives exactly 1.0.
> The final score is:
> final_score = mean(row_score over all test rows)
> A perfect submission scores 1.0. Partial credit is given only for slots that exactly match the hidden answer after normalization.
> What Not To Use
> Do not use original upstream filenames, source repository lookup, internet search, private platform files, hidden future snapshots, hidden answers, row order, or external package metadata. The public split intentionally uses anonymized package ids and does not include original package names or source filenames.

Inspiration note: Useful because it turns messy language evidence into a crisp span, class, ranking, or structured-output target with measurable scoring.

# CPU RAG Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed CPU examples in this document: 18

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.

## Regulatory Incident-to-Investigation Link Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cfwq5pyxxet9cp7bw6y4t098akefc
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Beat kris's score of 0.836!

Full challenge description from page:

> Safety surveillance records often contain two independently written views of the same case: an initial field incident account and a later technical investigation. During de-identification, archive migration, or evidence consolidation, the explicit key connecting those views can be lost. Your objective is to rank the three investigation records most likely to match each initial incident account. Recovering that link is important because the later investigation may confirm, reject, or refine the mechanism suggested by the initial account.
> This challenge evaluates retrieval of the matching investigation record from a hard candidate slate. Each query is a leakage-controlled initial incident packet. A shared corpus contains transformed investigation packets. For every query, exactly one of 12 candidate investigation IDs is the genuine investigation from the same original regulatory case. The other 11 candidates come from the same hidden manufacturer group and are preferentially matched on device and problem metadata, so organization identity, device family, and generic boilerplate are not enough to solve the task.
> The target is an original report-to-investigation relationship. It is not a generated label, medical-code prediction task, generic text classification problem, or lookup by source identifier.
> Task
> For every case_id in public/test.csv, rank the three most likely investigation IDs from that row's candidate_ids.
> The prediction must contain exactly three unique, space-separated IDs in best-to-worst order:
> INVR_31d98ab23f20e974 INVR_703ad15a965cf988 INVR_c384f01dbb793d12
> Only IDs listed in that case's 12-element candidate_ids array are valid.
> Dataset
> public/train.csv contains 2,930 incident queries, candidate slates, and the genuine matching investigation ID.
> public/test.csv contains 758 incident queries and candidate slates with the matching ID withheld.
> public/investigation_corpus.csv contains 3,688 candidate investigation documents used by both splits.
> public/sample_submission.csv contains a valid weak ranking constructed from candidate order.
> private/answers.csv contains hidden test pairings and is available only to the grader.
> Manufacturer groups are disjoint between train and test: 48 groups occur in train, 12 different groups occur in test, and overlap is zero.
> Columns
> | File | Column | Data type | Description |
> |---|---|---|---|
> | train.csv | case_id | String | Opaque query identifier. |
> | train.csv | incident_packet | String | Transformed initial incident account. |
> | train.csv | candidate_ids | JSON array of strings | Exactly 12 allowed investigation IDs. |
> | train.csv | correct_investigation_id | String | Genuine matching investigation ID. |
> | test.csv | case_id | String | Opaque query identifier. |
> | test.csv | incident_packet | String | Transformed initial incident account. |
> | test.csv | candidate_ids | JSON array of strings | Exactly 12 allowed investigation IDs. |
> | investigation_corpus.csv | investigation_id | String | Opaque document identifier. |
> | investigation_corpus.csv | investigation_packet | String | Transformed technical investigation account. |
> Incident packets contain 22 to 180 space-separated tokens, with a median of 54. Investigation packets contain 19 to 220 tokens, with a median of 141. They contain readable operational words, punctuation, redaction markers such as entity_redacted, masking markers such as token_masked, and coarse lexical-shape tokens such as lex_f_m for less-common words.
> Query and investigation IDs use independent namespaces and reveal no source relationship. Manufacturer, brand, model, catalog, lot, report-key, exact-date, URL, email, and long-number identifiers are removed. Query/document masking is independent, and exact duplicate query and investigation texts are excluded.
> Evaluation
> Scores range from 0 to 1 and higher is better.
> For a test case, let rank be the position of the genuine investigation in the submitted top-three list. Define:
> ReciprocalRankAt3 = 1 / rank, if rank is 1, 2, or 3
> 0, otherwise
> Top1Accuracy = 1, if rank is 1
> 0, otherwise
> The final score is:
> Score = 0.70 * mean(ReciprocalRankAt3)
> + 0.30 * mean(Top1Accuracy)
> This rewards finding the correct evidence record while placing extra emphasis on a correct first recommendation.
> Submission Format
> Submit submission.csv with exactly these columns in this order:
> case_id,ranked_investigation_ids
> MEDQ_0123456789abcdef,INVR_31d98ab23f20e974 INVR_703ad15a965cf988 INVR_c384f01dbb793d12
> MEDQ_fedcba9876543210,INVR_9b07a8756befa213 INVR_1851f7d032c58461 INVR_706a44f230509db8
> Include exactly one row for every case_id in public/test.csv, with no missing, duplicate, or extra IDs. Each ranking must contain exactly three unique IDs drawn from that case's candidate slate. Malformed rankings fail validation. Write the final file to ./working/submission.csv.
> Allowed
> Fit CPU models only on the provided public files.
> Use sparse retrieval, BM25-style methods, latent semantic models, compact models initialized from scratch, learning-to-rank, cross-view feature models, or CPU ensembles.
> Use the complete public investigation corpus and candidate slates during inference.
> Use at most 10 CPU cores, 62 GB RAM, and 1.5 hours total runtime.
> Prohibited
> No GPU, CUDA, GPU-only libraries, pretrained language models, externally fitted tokenizers, hosted model APIs, or closed inference services.
> Do not retrieve external incident archives, source records, manufacturer catalogs, report IDs, answer maps, or related regulatory data.
> Do not identify source rows using exact-phrase search, source-file matching, reconstructed identifiers, product lookup, or external database joins.
> Do not use private files, hidden answers, grader internals, row order, filenames, hashes, malformed inputs, or filesystem side channels.
> Do not submit candidate-order constants, fixed rankings, or source-key reconstruction as the primary solution.
> This benchmark is for machine-learning evaluation only and must not be used for medical or device-safety decisions.

Inspiration note: Useful because it frames retrieval as ranking evidence records under hard candidate constraints, a strong pattern for realistic RAG benchmarks.

## Retrieval-Augmented Narrative Question Answering

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fwntbc6dzp93jb9nrsmndhd8agsfz
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat azd_sid4's score of 0.410!

Full challenge description from page:

> This challenge tests retrieval-augmented question answering over a large corpus of passages drawn from a long-form narrative text. Participants are given a corpus of ~1,000 self-contained narrative passages and a set of natural-language questions. For each question, a solution must:
> Retrieve the single passage from the corpus that supports answering the question, or declare the question unanswerable if no passage in the corpus actually supports it.
> Generate a natural-language answer grounded in that passage — or, if the question is unanswerable, explicitly say so in a sentence (e.g. "This cannot be answered from the given passages.") rather than leaving the answer blank or guessing.
> Evaluation
> Submissions are scored with the Grounded Retrieval Score (GRS), which combines retrieval correctness with semantic answer quality, per question:
> GRS
> 𝑖
> =
> 𝑅
> 𝑖
> ⋅
> (
> 0.7
> +
> 0.3
> ⋅
> 𝐴
> 𝑖
> )
> GRS
> i
> ​
> =R
> i
> ​
> ⋅(0.7+0.3⋅A
> i
> ​
> )
> 1. Retrieval component
> 𝑅
> 𝑖
> R
> i
> ​
> :
> 𝑅
> 𝑖
> =
> 1
> [
> predicted_passage_id
> 𝑖
> =
> gold_passage_id
> 𝑖
> ]
> R
> i
> ​
> =1[predicted_passage_id
> i
> ​
> =gold_passage_id
> i
> ​
> ]
> A hit requires an exact match against the gold passage ID. For genuinely unanswerable questions, the gold ID is the literal string UNANSWERABLE, so
> 𝑅
> 𝑖
> =
> 1
> R
> i
> ​
> =1 only if the submission also predicts UNANSWERABLE.
> 2. Answer component
> 𝐴
> 𝑖
> A
> i
> ​
> :
> Every question — answerable or not — has a real reference sentence to match against: for unanswerable questions, the reference is an explicit refusal sentence rather than an empty string. This means a blank answer_text never scores well, on any row.
> 𝐴
> 𝑖
> =
> cos
> ⁡
> (
> 𝑒
> 𝑝
> 𝑟
> 𝑒
> 𝑑
> ,
> 𝑒
> 𝑟
> 𝑒
> 𝑓
> )
> ⋅
> 𝐿
> 𝑖
> A
> i
> ​
> =cos(e
> pred
> ​
> ,e
> ref
> ​
> )⋅L
> i
> ​
> where
> 𝑒
> 𝑝
> 𝑟
> 𝑒
> 𝑑
> ,
> 𝑒
> 𝑟
> 𝑒
> 𝑓
> e
> pred
> ​
> ,e
> ref
> ​
> are mean-pooled, L2-normalized sentence embeddings of the predicted and reference answers from sentence-transformers/all-MiniLM-L6-v2 and
> 𝐿
> 𝑖
> =
> min
> ⁡
> (
> 1
> ,
> 2
> ⋅
> ∣
> ref_answer
> ∣
> ∣
> pred_answer
> ∣
> )
> L
> i
> ​
> =min(1,
> ∣pred_answer∣
> 2⋅∣ref_answer∣
> ​
> )
> is a length penalty that discourages dumping the entire retrieved passage as the "answer" instead of a concise response.
> Final score is the mean of
> GRS
> 𝑖
> GRS
> i
> ​
> over all test questions, range
> [
> 0
> ,
> 1
> ]
> [0,1].
> File Structure
> passages.csv — 1,048 rows × 3 columns, CSV UTF-8, the retrieval corpus.
> train.csv — 4,295 rows × 4 columns, CSV UTF-8, labeled example questions with their source passage and reference answer.
> test.csv — 1,095 rows × 2 columns, CSV UTF-8, questions to answer (no labels).
> sample_submission.csv — 1,095 rows × 3 columns, CSV UTF-8, submission template.
> Column Descriptions
> passages.csv
> passage_id (string): Unique passage identifier.
> section_label (string): Coarse section label the passage belongs to.
> passage_text (string): Full text of the passage.
> train.csv
> id (string): Unique row ID.
> query_text (string): The question.
> passage_id (string): Correct passage ID from passages.csv.
> reference_answer (string): Reference answer to the question.
> test.csv
> id (string): Unique row ID.
> query_text (string): The question to answer.
> Submission
> Participants submit a submission.csv file with th following format
> id (string): Must match test.csv exactly.
> passage_id (string): A passage_id from passages.csv, or the literal string UNANSWERABLE (case-insensitive).
> answer_text (string): Free-text answer. If the question is unanswerable, write "This question cannot be answered from the passages provided." — do not leave this blank.
> Requirements:
> Must contain exactly the same rows as test.csv (do not hardcode a row count).
> passage_id must be non-null for every row.
> answer_text must be present for every row; a blank answer scores poorly on every row, including unanswerable ones.
> Example Submission
> id,passage_id,answer_text
> test_00000,psg_00000,placeholder answer text
> test_00001,psg_00000,placeholder answer text
> ...
> Prohibited:
> Using any copy of the original source text this dataset was built from, in any form — downloading it, attaching it as a separate dataset, bundling it with a solution, or reproducing it from memory — to recover passages or answers not present in the files provided by this challenge. Only passages.csv and train.csv may be used as knowledge sources; a submission that answers a withheld/unanswerable question correctly using outside knowledge of the source text is a rules violation, not a scoring success.
> Reverse-engineering or brute-forcing passage_id values to infer labels.
> Hardcoding any ID and answer mapping.
> Using data outside what is provided in this challenge.

Inspiration note: Useful because it frames retrieval as ranking evidence records under hard candidate constraints, a strong pattern for realistic RAG benchmarks.

## Name Collision: Open-World Referent Attribution

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx735ryhfnp2sa2gpbvskqgjfx8ah0cy
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat hair0nfire's score of 0.772!

Full challenge description from page:

> Background
> When a retrieval-augmented system is asked about a person, the passages it retrieves are keyed on the person's name — and names are not unique. The retrieved pool routinely mixes evidence about the intended person with evidence about different people who share the same name, and, just as often, the intended person is not in the retrieved pool at all. A faithful system must do two things that ordinary retrieval cannot: attribute each passage to the correct individual when that individual is present, and refuse to attribute — abstain — when the queried person is absent, rather than confidently stitch together an impostor's biography.
> This challenge grades exactly that open-world, selective behaviour. To force the model onto the biographical signal, the shared name is redacted to the placeholder [PERSON] in every passage, so the name gives you nothing: passages can only be told apart by their surrounding context.
> Task
> Each row gives you:
> a query: one short biographical sentence about a single target person (name redacted to [PERSON]), and
> a passages pool: a list of short biographical sentences, each also mentioning [PERSON].
> There are two kinds of row, and you are not told which kind a row is:
> Answerable — the target person is represented in the pool. Some pool passages are about the target; the rest are about different people who share the (redacted) name. You should return the pool passages about the target.
> Unanswerable — the target person is not in the pool at all (every passage is about a same-name impostor). You should abstain: return an empty selection.
> Deciding whether the target is present is part of the task. Selecting impostor passages for an absent target is penalised exactly like missing a present target.
> Data files
> All files are UTF-8 CSVs.
> train.csv — training rows. Columns:
> id (string) — unique row identifier, e.g. nc_000042 (ids are unique across train.csv and test.csv).
> query (string) — one biographical sentence about the target person; name redacted to [PERSON].
> passages (string) — a JSON array of objects {"pid": <int>, "text": <string>}. pid is a small integer local to the row (pool positions are shuffled, so pid order carries no signal); text is one name-redacted biographical sentence.
> train_labels.csv — supervision for the training rows. Columns:
> id (string) — matches a train.csv id.
> selected_pids (string) — the space-separated pids of the passages about the target person. An empty cell marks an unanswerable training row (the target is absent; the correct answer is to abstain).
> test.csv — test rows, same columns as train.csv (id, query, passages). No labels.
> sample_submission.csv — a valid submission (columns id, selected_pids) covering every test.csv id, in the required format.
> Submission format
> Produce submission.csv with exactly these two columns:
> id (string) — every id in test.csv, each exactly once (no missing, extra, or duplicate ids).
> selected_pids (string) — the space-separated integer pids you attribute to the target for that row, e.g. 0 3 7. An empty cell is a valid, first-class answer: it means abstain (you judge the target to be absent from the pool).
> Every pid you list must be one of that row's pool pids, without repetition. The grader rejects a submission whose id-set differs from the test id-set, or whose selected_pids cell is not a set of unique non-negative integers, or that contains a pid that is not one of the row's pool ids.
> Evaluation
> The score has two equally weighted halves — how well you decide whether the target is present, and how well you attribute when it is. A row is answerable if the target is in the pool (its gold set G is non-empty) and unanswerable otherwise (G empty). Let P be the set of pids you submit for a row; you answer the row if P is non-empty and abstain if P is empty.
> Attribution = the mean set-F1 over the answerable rows only: F1 = 2·|P∩G| / (|P| + |G|) (an answerable row you abstain on scores 0).
> Abstention = max(0, sensitivity + specificity − 1), where sensitivity = fraction of answerable rows you answer, and specificity = fraction of unanswerable rows you abstain on. This equals 0 for any constant strategy (always-answer or always-abstain) and 1 for a perfect present/absent detector.
> final = 0.5 · Attribution + 0.5 · Abstention, in [0, 1] (higher is better).
> Because the two halves are explicit and equally weighted, no trivial strategy scores well. Published reference points on this data: always-abstaining ≈ 0.01, always-selecting-everything ≈ 0.17, and an off-the-shelf dense retriever with a threshold tuned on the labels ≈ 0.40. Real score comes only from detecting presence and attributing correctly, and attribution is where the headroom is — none of these baselines has claimed it.
> Notes
> Test rows come from name groups unseen in training — the disambiguation and abstention skills must generalise, not be memorised per name.
> The name carries no signal (it is redacted identically everywhere), and pool position is shuffled. Attribution and the present/absent decision must come from biographical coherence across passages.
> predictions must be produced by your model from the provided data; recovering the original identities or labels from outside sources is not a valid solution.

Inspiration note: Useful because it frames retrieval as ranking evidence records under hard candidate constraints, a strong pattern for realistic RAG benchmarks.

## FWS Refuge Evidence Route Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx714cwmchpyg49s1sv9v9mf218ap8h1
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> FWS Refuge Evidence Route Reconstruction
> Build a CPU-friendly RAG and sequence reconstruction system for wildlife-refuge operations evidence. You are given anonymized, lossy evidence snippets derived from public U.S. Fish and Wildlife Service National Wildlife Refuge System infrastructure records. For each case, reconstruct the ordered route of evidence IDs that best supports the requested sanctuary operations intent.
> This is hard because each sanctuary can have many candidate evidence rows across trails, water structures, gates, access points, roads, parking, property records, buildings, blinds, and fences. The answer is not a single class label; it is an ordered evidence route. Good solutions need to retrieve the right sanctuary evidence, respect the case intent, rank records within each source family, and output a constrained sequence.
> CPU Compatibility
> The challenge is designed for CPU-only solutions within 1.5 hours on about 10 CPU cores and 62 GB RAM. No GPU training, large language model inference, hosted embedding service, or external source lookup is required. Strong approaches can use sparse text features, TF-IDF, hashing vectorizers, grouped validation, lightweight rankers, and deterministic post-processing.
> Public Files
> evidence_catalog.csv
> ColumnDescriptionevidence_idPublic anonymized evidence identifier. This is the token to submit.sanctuary_idPublic anonymized sanctuary/group identifier. Use it to filter candidates for a case.source_familyEvidence family such as TRAIL, WATER_LINE, GATE, ROAD, or PARKING.regionFWS region when available.stateState abbreviation when available.resource_typeSource resource type when available, such as NWR or WPA.passageLossy normalized evidence text. Direct source URLs, GUIDs, emails, and many source-specific free-text phrases are removed or converted to keyword summaries.
> train.csv
> ColumnDescriptioncase_idPublic case identifier.sanctuary_idSanctuary identifier shared with evidence_catalog.csv.case_typeIntent type for the evidence route.regionFWS region when available.stateState abbreviation when available.resource_typeSource resource type when available.candidate_evidence_countNumber of evidence rows in evidence_catalog.csv for this case's sanctuary_id.family_countsSemicolon-separated string of source-family counts, formatted like ACCESS:2; GATE:5; ROAD:1.query_textNatural-language route reconstruction request.target_evidence_idsTraining answer sequence, with evidence IDs separated by the space-pipe-space separator.
> test.csv
> Same columns as train.csv, except it does not include target_evidence_ids.
> sample_submission.csv
> ColumnDescriptioncase_idTest case identifier.predicted_evidence_idsEmpty dummy prediction column showing the required submission schema.
> source_family_catalog.csv
> ColumnDescriptionsource_familyEvidence family token used in evidence_catalog.csv.descriptionShort explanation of the evidence family.
> case_intent_catalog.csv
> ColumnDescriptioncase_typeIntent type appearing in train.csv and test.csv.intent_summaryShort natural-language description of the intent.family_order_hintOrdered family hint using the same space-pipe-space separator.max_scored_evidence_idsMaximum number of evidence IDs scored for each row. This value is 6.
> Prediction Task
> For each row in test.csv, predict an ordered sequence of evidence_id values from evidence_catalog.csv. Candidate evidence should come from rows with the same sanctuary_id as the case. Submit the IDs in the order that best reconstructs the requested evidence route.
> Use this exact separator between IDs:
> |
> This separator is one space, then a vertical bar, then one space. The hidden target sequence has at most 6 evidence IDs. The grader parses at most the first 6 submitted IDs per row. IDs after the first 6 are ignored. Extra incorrect IDs inside the first 6 can lower precision.
> Submission Format
> Submit a CSV with exactly one row per test case and these required columns:
> ColumnDescriptioncase_idMust match a test case ID exactly.predicted_evidence_idsOrdered evidence IDs separated by the space-pipe-space separator. Empty strings are allowed but score zero for that row.
> Example:
> case_id,predicted_evidence_ids
> case_0123456789abcdef,ev_water_line_0123456789abcdef | ev_gate_fedcba9876543210 | ev_road_0011223344556677
> Structural submission errors raise an error: missing required columns, duplicate case_id values, missing test IDs, or extra unknown IDs. Bad row-level predictions, unknown evidence IDs, malformed evidence IDs, or empty sequences receive reduced or zero row credit rather than crashing the grader.
> Evaluation Metric
> Higher is better. The public score range is 0 to 1.
> For each case, the grader parses the submitted sequence and computes three components.
> ordered_lcs_f1 measures ordered sequence agreement:
> ordered_lcs_f1 = 0, if the predicted sequence or target sequence is empty
> ordered_lcs_f1 = (2 * LCS_length(predicted, target)) / (len(predicted) + len(target)), otherwise
> evidence_set_f1 measures unordered exact evidence-ID overlap:
> precision = count(unique predicted IDs that are in the target set) / count(unique predicted IDs)
> recall = count(unique predicted IDs that are in the target set) / count(unique target IDs)
> evidence_set_f1 = 0, if precision and recall are both 0
> evidence_set_f1 = (2 * precision * recall) / (precision + recall), otherwise
> family_set_f1 uses the same F1 formula as evidence_set_f1, but compares evidence families parsed from ID prefixes such as ev_water_line_..., ev_gate_..., and ev_road_....
> The row score is:
> case_score = (0.50 * ordered_lcs_f1) + (0.35 * evidence_set_f1) + (0.15 * family_set_f1)
> The final score is:
> score = mean(case_score over all test cases)
> An exact sequence match receives 1.0 for that case. Empty or fully invalid predictions receive 0.0 for that case.
> Rules And Restrictions
> Use only the provided public challenge files.
> Do not use external lookup to identify raw FWS source rows, raw refuge names, raw organization codes, GlobalIDs, ObjectIDs, or answer-construction details.
> Do not scrape or query FWS/ArcGIS sources during solving.
> Do not use the raw upload archive as a lookup table for test answers.
> CPU-compatible methods are expected; GPU training and hosted model inference are outside the intended solution path.
> Keep predictions constrained to evidence IDs from evidence_catalog.csv.
> Recommended CPU Approach
> Create a local validation split by sanctuary_id or by case groups. For each case, filter evidence_catalog.csv to the matching sanctuary_id, parse the case intent and family-order hint, build sparse text features from query_text and passage, and learn a lightweight ranker from train.csv. The public passages are lossy summaries, so strong solutions should learn source-family and normalized-attribute patterns from the labeled training routes instead of assuming a visible keyword argmax rule.

Inspiration note: Useful because it frames retrieval around evidence routing or constrained candidate matching rather than generic document QA.

## Future Paper Oracle: Evidence-Grounded Research Gap Audit and Question Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bkrn6zm55b2paj869efgdn989nthm
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> 1. Overview
> Future Paper Oracle is a structured scientific-literature reasoning challenge.
> Each sample contains:
> A proposed future research question.
> A literature packet containing paper titles, abstracts, and selected paper sections.
> Some references directly support a specific unresolved research direction. Others are only topically related or act as distractors.
> The objective is to determine whether the exact proposed research question is justified by the supplied literature.
> For every test sample, participants must predict:
> support_status
> gap_type
> evidence_refs
> repaired_question
> A strong solution should behave like a careful researcher or peer reviewer. It should:
> Inspect the supplied evidence.
> Identify the research gap actually supported by the literature.
> Distinguish direct evidence from nearby but irrelevant material.
> Detect unsupported, altered, vague, or conflicting claims.
> Select the references that directly ground the research direction.
> Make the smallest necessary repair to the proposed question.
> All four predicted fields must express one coherent scientific judgment.
> For example, when a candidate question is classified as off_scope, the selected references and repaired question should describe the closest research direction actually supported by the literature packet rather than the unrelated candidate.
> The task is not to generate an arbitrary new research idea.
> It is to audit and, when necessary, minimally repair a proposed research question using only the supplied evidence.
> 2. Prediction Objective
> For each row in test.csv, participants must evaluate the relationship between the candidate research question and its literature packet.
> The submission must determine:
> Whether the candidate is supported, partly supported, contradicted, underspecified, or outside the scope of the evidence.
> Which category best describes the grounded research gap.
> Which local references directly support that grounded direction.
> What the evidence-grounded research question should be.
> The predictions must be based on the supplied literature packet for that sample.
> Broad scientific plausibility is not sufficient.
> A question may sound reasonable in the wider research literature while still being unsupported by the specific packet provided for the sample.
> 3. What the Challenge Evaluates
> Future Paper Oracle combines:
> Scientific evidence retrieval.
> Research-gap identification.
> Fine-grained textual entailment.
> Contradiction detection.
> Distractor rejection.
> Gap-type classification.
> Evidence selection.
> Constrained question repair.
> Cross-field consistency checking.
> A successful model must distinguish several different situations.
> The candidate may be:
> Fully justified by the packet.
> Mostly correct but altered in one important detail.
> Based on a premise contradicted by the packet.
> Too vague to express the actual research gap.
> Unrelated to the grounded direction despite sharing terminology.
> The main difficulty is that scientific papers often contain several nearby topics, methods, limitations, and future-work directions.
> Topical similarity alone is therefore insufficient.
> The model must identify which claims are directly supported and which details change the meaning of the intended research direction.
> 4. Public Dataset Structure
> The public dataset is organized as follows:
> public/
> ├── train.csv
> ├── test.csv
> ├── sample_submission.csv
> └── contexts/
> ├── train/
> │   └── <training_id>.json
> └── test/
> └── <test_id>.json
> Paths stored in the context_file column are relative to the public dataset directory.
> For example:
> contexts/train/TR8C14A92F03BE.json
> Each CSV row corresponds to one proposed research question and one JSON literature packet.
> 5. Training Data
> train.csv contains the following columns:
> id
> context_file
> candidate_question
> field
> support_status
> gap_type
> evidence_refs
> repaired_question
> 5.1 id
> Type: string.
> A unique anonymized sample identifier.
> Training identifiers begin with:
> TR
> Identifiers do not encode the answer, field, source papers, or sample difficulty.
> 5.2 context_file
> Type: string.
> The relative path to the JSON literature packet associated with the row.
> Example:
> contexts/train/TR8C14A92F03BE.json
> 5.3 candidate_question
> Type: string.
> The proposed future research question that must be evaluated against the supplied literature.
> 5.4 field
> Type: string.
> The broad computer-science research area associated with the sample.
> Possible values may include:
> machine_learning
> natural_language_processing
> computer_vision
> artificial_intelligence
> robotics
> software_engineering
> security_privacy
> information_retrieval
> distributed_systems
> networking
> human_computer_interaction
> sound_audio
> information_theory
> The field provides broad topical context. It does not reveal the correct support status or gap type.
> 5.5 support_status
> Type: string.
> The relationship between the exact candidate question and the supplied literature.
> Allowed values:
> supported
> partial
> contradicted
> underspecified
> off_scope
> 5.6 gap_type
> Type: string.
> The primary research-gap category associated with the evidence-grounded research direction.
> Allowed values:
> method_gap
> application_gap
> evaluation_gap
> data_gap
> robustness_gap
> efficiency_gap
> theory_gap
> safety_gap
> mixed
> none
> The value none is used only when support_status is supported.
> 5.7 evidence_refs
> Type: string.
> A pipe-separated set of local reference identifiers that directly supports the grounded research direction.
> Example:
> R1|R3
> Reference identifiers are local to the sample.
> 5.8 repaired_question
> Type: string.
> The evidence-grounded version of the proposed research question.
> When support_status is supported, this value is exactly equal to candidate_question.
> For other statuses, it contains the smallest appropriate correction or replacement.
> 6. Test Data
> test.csv contains:
> id
> context_file
> candidate_question
> field
> The following fields are hidden and must be predicted:
> support_status
> gap_type
> evidence_refs
> repaired_question
> 6.1 Test identifiers
> Test identifiers begin with:
> TS
> Each test identifier must appear exactly once in the submission.
> 6.2 Hidden labels
> The hidden fields follow the same definitions and allowed values as the corresponding columns in train.csv.
> 7. Sample Submission
> sample_submission.csv contains:
> Every test identifier.
> The exact required submission columns.
> The required column order.
> The columns are:
> id
> support_status
> gap_type
> evidence_refs
> repaired_question
> Participants should use sample_submission.csv as the authoritative starting point for submission generation.
> Do not add, remove, rename, or reorder columns.
> 8. Context Files
> Each row points to one JSON literature packet.
> A context file follows this general structure:
> {
> "id": "TS8C14A92F03BE",
> "field": "machine_learning",
> "candidate_question": "How can uncertainty-aware retrieval be integrated into long-context language models?",
> "references": [
> {
> "ref_id": "R1",
> "title": "Reference title",
> "abstract": "Reference abstract text...",
> "sections": {
> "INTRODUCTION": "Selected section text...",
> "METHOD": "Selected section text...",
> "EXPERIMENTS": "Selected section text..."
> }
> }
> ]
> }
> Each reference may contain:
> ref_id
> title
> abstract
> sections
> 8.1 ref_id
> A local reference identifier such as:
> R1
> R2
> R3
> Reference identifiers are meaningful only within one sample.
> R1 in one literature packet is unrelated to R1 in another packet.
> 8.2 title
> The paper title.
> 8.3 abstract
> The available abstract text.
> 8.4 sections
> A JSON object containing selected paper-section text.
> Section names and available content vary between references.
> A solution must not assume that every paper contains:
> The same section names.
> The same number of sections.
> A method section.
> An experiments section.
> Full paper text.
> Some references may contain only an abstract and a small number of sections. Others may contain substantially more text.
> 8.5 Supporting references and distractors
> A packet may contain:
> References that directly support the grounded research direction.
> References that support only part of the direction.
> References that use related terminology.
> References that discuss a similar method or task.
> Distractors that are topically close but scientifically irrelevant to the intended gap.
> A distractor may discuss a similar:
> Method.
> Task.
> Application.
> Terminology.
> Research field.
> Topical similarity does not make a reference valid evidence.
> 9. Prediction Fields
> 9.1 support_status
> Predict exactly one of:
> supported
> partial
> contradicted
> underspecified
> off_scope
> supported
> Use supported when the exact candidate question is justified by the supplied literature.
> Broad topical similarity is not sufficient.
> The important parts of the candidate should be grounded, including its:
> Method.
> Task.
> Limitation.
> Application.
> Scope.
> Setting.
> Constraint.
> Intended outcome.
> For supported samples:
> gap_type = none
> repaired_question = candidate_question
> The repaired question must copy the candidate exactly, including capitalization, punctuation, and whitespace.
> partial
> Use partial when the central research direction is relevant but one or more important details are missing, altered, broadened, weakened, or unsupported.
> Examples include:
> Changing the intended method.
> Extending the question to an unsupported application.
> Removing an important constraint.
> Broadening a narrow research problem.
> Changing the intended objective.
> Preserving the broad topic while weakening the actual research gap.
> Adding a setting that is not supported by the packet.
> A partial candidate should usually be repaired by preserving the supported wording and changing only the problematic detail.
> contradicted
> Use contradicted when the candidate contains a premise that conflicts with the supplied literature.
> Examples include assuming that a method is already:
> Robust.
> Efficient.
> Scalable.
> Theoretically guaranteed.
> Privacy-preserving.
> Secure.
> Well evaluated.
> Reliable under conditions where the literature reports an unresolved limitation.
> The repaired question should remove or correct the conflicting premise.
> underspecified
> Use underspecified when the candidate is too vague to express the actual research gap.
> An underspecified question may mention only a broad topic while omitting the detail that makes the research direction meaningful.
> Missing information may include:
> Method.
> Task.
> Limitation.
> Evaluation setting.
> Application.
> Constraint.
> Target population.
> Intended outcome.
> The repaired question should restore the missing specificity.
> off_scope
> Use off_scope when the candidate describes a research direction not justified by the supplied literature packet.
> The candidate may:
> Belong to the same broad field.
> Use similar terminology.
> Mention a related method.
> Refer to a nearby application.
> However, its central method, application, task, objective, or problem is unrelated to the grounded direction.
> For off-scope samples, replace the unsupported candidate with the closest research question directly supported by the packet.
> 9.2 gap_type
> Predict exactly one of:
> method_gap
> application_gap
> evaluation_gap
> data_gap
> robustness_gap
> efficiency_gap
> theory_gap
> safety_gap
> mixed
> none
> method_gap
> Use method_gap when the grounded direction requires a new or modified:
> Model.
> Algorithm.
> Architecture.
> Objective.
> Training procedure.
> Optimization strategy.
> Inference mechanism.
> Retrieval method.
> Generation method.
> application_gap
> Use application_gap when an existing method or approach must be adapted to a new:
> Task.
> Domain.
> Deployment setting.
> Environment.
> Population.
> Modality.
> Real-world application.
> evaluation_gap
> Use evaluation_gap when the central limitation involves missing or insufficient:
> Metrics.
> Benchmarks.
> Baselines.
> Comparisons.
> Ablations.
> Human evaluation.
> Validation procedures.
> Evaluation coverage.
> data_gap
> Use data_gap when the grounded problem is caused by:
> Missing datasets.
> Limited training data.
> Insufficient annotations.
> Weak domain coverage.
> Unavailable modalities.
> Low-resource settings.
> Poor sample diversity.
> robustness_gap
> Use robustness_gap when the main limitation concerns:
> Generalization.
> Domain shift.
> Noise.
> Uncertainty.
> Reliability.
> Out-of-distribution behavior.
> Adversarial conditions.
> Sensitivity to changing environments.
> efficiency_gap
> Use efficiency_gap when the central limitation concerns:
> Computation.
> Memory.
> Latency.
> Communication cost.
> Scalability.
> Model size.
> Compression.
> Energy consumption.
> Deployment resources.
> theory_gap
> Use theory_gap when the literature identifies a missing:
> Proof.
> Formal explanation.
> Convergence result.
> Theoretical guarantee.
> Bound.
> Principled characterization.
> safety_gap
> Use safety_gap when the grounded direction concerns:
> Safety.
> Security.
> Privacy.
> Fairness.
> Bias.
> Harmful behavior.
> Alignment.
> Misuse.
> Trustworthiness.
> mixed
> Use mixed when multiple gap categories are jointly central to the grounded direction and no single category adequately describes it.
> Do not use mixed merely because several minor limitations are mentioned.
> none
> Use none only when:
> support_status = supported
> Every non-supported status must use a gap type other than none.
> 9.3 evidence_refs
> The evidence_refs field must contain the reference identifiers that directly support the grounded research direction.
> Use pipe-separated identifiers.
> Correct:
> R1|R3
> Incorrect:
> ["R1", "R3"]
> Incorrect:
> Paper A|Paper B
> Incorrect:
> 1|3
> Reference order does not affect evaluation.
> Only identifiers present in the sample’s references array may be submitted.
> The selected references should directly support:
> The identified research gap.
> The submitted gap_type.
> The repaired research question.
> The overall scientific judgment.
> The references do not necessarily need to support the flawed wording of the original candidate.
> This is particularly important for:
> contradicted
> underspecified
> off_scope
> For an off-scope candidate, the submitted evidence should support the replacement direction expressed by repaired_question.
> Select references that directly support the grounded direction.
> Avoid including every topically related reference.
> Selecting distractors reduces evidence precision.
> Omitting directly relevant references reduces evidence recall.
> 9.4 repaired_question
> The repaired question must be:
> Non-empty.
> Specific.
> Concise.
> Answerable.
> Written as a research question.
> Grounded in the supplied literature.
> For supported
> Copy the candidate exactly:
> repaired_question = candidate_question
> For partial
> Preserve the supported wording and modify only the unsupported, altered, missing, or overly broad part.
> For contradicted
> Remove or correct the premise that conflicts with the literature.
> For underspecified
> Restore the missing scientific detail, such as the:
> Method.
> Task.
> Limitation.
> Application.
> Scope.
> Setting.
> Constraint.
> Intended outcome.
> For off_scope
> Replace the candidate with the closest research question supported by the literature packet.
> Avoid generic repairs such as:
> How can machine learning models be improved?
> Prefer specific questions grounded in the packet.
> Example:
> How can uncertainty-aware retrieval be integrated into long-context language models to reduce hallucinations in scientific question answering?
> A strong repair preserves every supported part of the candidate and changes only what is necessary.
> Unnecessary rewriting may reduce similarity to the hidden grounded answer.
> 10. Minimal-Repair Principle
> The goal is not to rewrite every question from scratch.
> Use the following behavior:
> supported
> Copy the candidate unchanged.
> partial
> Preserve the supported wording and correct only the unsupported detail.
> contradicted
> Preserve the valid research direction while correcting the conflicting premise.
> underspecified
> Add the missing scientific detail without replacing supported content unnecessarily.
> off_scope
> Replace the unsupported direction with the closest evidence-grounded research question.
> The repaired question should remain as close as possible to the intended grounded direction.
> 11. Submission Format
> Submit a CSV file with exactly these five columns in this order:
> id,support_status,gap_type,evidence_refs,repaired_question
> Example:
> id,support_status,gap_type,evidence_refs,repaired_question
> TS8C14A92F03BE,supported,none,R1,"How can uncertainty-aware retrieval be integrated into long-context language models?"
> TS31F0B92AAC72,partial,robustness_gap,R2|R3,"How can vision-language navigation models be made more robust in cluttered indoor environments?"
> TSA702BC91D044,off_scope,application_gap,R2,"How can retrieval-augmented generation be adapted to improve factual consistency in scientific question answering?"
> Submission requirements:
> Every test ID must appear exactly once.
> IDs must be copied unchanged.
> No additional IDs may be included.
> No test IDs may be omitted.
> Duplicate IDs are not allowed.
> Columns must use the exact required names.
> Columns must appear in the required order.
> support_status must use one documented label.
> gap_type must use one documented label.
> evidence_refs must use valid local reference identifiers.
> repaired_question must be non-empty.
> CSV quoting must be valid.
> Use sample_submission.csv as the starting point for submission generation.
> 12. Evaluation
> The final score ranges from:
> 0.01 to 1.00
> Higher scores are better.
> The raw score is a weighted sum:
> raw_score = 0.25 × support_status_macro_f1 + 0.20 × evidence_reference_f1 + 0.15 × gap_type_macro_f1 + 0.30 × repaired_question_similarity + 0.10 × grounded_consistency
> The reported score is:
> final_score = min(1.00, max(0.01, raw_score))
> Intermediate metric values are not rounded.
> The displayed final score may be rounded to six decimal places.
> All test rows contribute equally unless a metric explicitly uses macro averaging across classes.
> 12.1 Common Text Normalization
> The repaired-question metrics use the following deterministic normalization procedure.
> For each submitted or hidden repaired question:
> Convert the value to a Unicode string.
> Apply Unicode NFKC normalization.
> Convert all letters to lowercase.
> Extract tokens using the regular expression: [a-z0-9]+
> Preserve the extracted tokens in their original order.
> For example:
> How can Long-Context LMs reduce hallucinations?
> is tokenized as:
> how
> can
> long
> context
> lms
> reduce
> hallucinations
> The normalized character string is created by joining the extracted tokens with one ASCII space:
> how can long context lms reduce hallucinations
> As a result:
> Capitalization does not affect similarity.
> Punctuation does not affect similarity.
> Repeated whitespace does not affect similarity.
> Hyphenated expressions are treated as separate tokens.
> The submitted and hidden repaired questions are normalized independently.
> 12.2 Support-Status Macro-F1
> This component evaluates predictions across the five support-status labels:
> supported
> partial
> contradicted
> underspecified
> off_scope
> For each class c:
> precision_c = TP_c / (TP_c + FP_c)
> recall_c = TP_c / (TP_c + FN_c)
> The class F1 score is:
> F1_c = 2 × TP_c / (2 × TP_c + FP_c + FN_c)
> If the denominator is zero:
> F1_c = 0
> The support-status component is:
> support_status_macro_f1 = (F1_supported + F1_partial + F1_contradicted + F1_underspecified + F1_off_scope) / 5
> Every documented class is included in the average, even when the submitted predictions never use that class.
> Macro-F1 gives equal importance to each support-status category.
> A model should evaluate the exact candidate question rather than classify every scientifically plausible question as supported.
> 12.3 Evidence-Reference F1
> Submitted and hidden evidence references are compared as unordered sets.
> The submitted evidence_refs value is parsed as follows:
> Split the value on the pipe character.
> Remove surrounding whitespace from each identifier.
> Remove empty identifiers.
> Remove duplicate identifiers.
> Treat the remaining identifiers as an unordered set.
> For example:
> R3|R1|R3
> is interpreted as:
> {R1, R3}
> For row i, let:
> P_i be the submitted reference set.
> G_i be the hidden reference set.
> M_i be the intersection of P_i and G_i.
> Row-level evidence precision is:
> evidence_precision_i = |M_i| / |P_i|
> Row-level evidence recall is:
> evidence_recall_i = |M_i| / |G_i|
> Row-level evidence F1 is:
> E_i = 2 × |M_i| / (|P_i| + |G_i|)
> Empty-set rules:
> If both P_i and G_i are empty, E_i = 1.
> If exactly one is empty, E_i = 0.
> The overall score is:
> evidence_reference_f1 = (E_1 + E_2 + ... + E_N) / N
> Reference order does not affect this component.
> Selecting distractor references reduces precision.
> Omitting directly grounded references reduces recall.
> Identifiers absent from the sample’s references array are invalid and cannot match a hidden reference.
> 12.4 Gap-Type Macro-F1
> This component evaluates predictions across the ten gap-type labels:
> method_gap
> application_gap
> evaluation_gap
> data_gap
> robustness_gap
> efficiency_gap
> theory_gap
> safety_gap
> mixed
> none
> For each class c:
> F1_c = 2 × TP_c / (2 × TP_c + FP_c + FN_c)
> If the denominator is zero:
> F1_c = 0
> The gap-type component is:
> gap_type_macro_f1 = sum of the ten class F1 scores / 10
> Every documented gap-type class is included.
> Macro averaging prevents common labels from dominating the score.
> Participants should identify the primary grounded gap rather than defaulting to broad labels such as method_gap or mixed.
> 12.5 Repaired-Question Similarity
> For each row, the submitted repaired question is compared with the hidden grounded question using:
> Q_i = 0.45 × token_f1_i + 0.35 × normalized_character_similarity_i + 0.20 × token_bigram_f1_i
> Each subscore ranges from 0 to 1.
> The overall repaired-question score is:
> repaired_question_similarity = (Q_1 + Q_2 + ... + Q_N) / N
> Token F1
> Token F1 compares the normalized token sequences as multisets.
> A multiset preserves the number of times each token occurs.
> Let:
> p_t(w) be the number of occurrences of token w in the submitted question.
> g_t(w) be the number of occurrences of token w in the hidden question.
> The token overlap is:
> token_overlap = sum over tokens w of min(p_t(w), g_t(w))
> Let:
> n_p be the total number of submitted tokens.
> n_g be the total number of hidden tokens.
> Then:
> token_f1 = 2 × token_overlap / (n_p + n_g)
> Empty-input rules:
> If n_p = 0 and n_g = 0, then token_f1 = 1.
> If exactly one is zero, then token_f1 = 0.
> Repeated tokens are counted according to their number of occurrences.
> Normalized Character Similarity
> Let:
> s_p be the normalized submitted string.
> s_g be the normalized hidden string.
> d(s_p, s_g) be the standard Levenshtein edit distance using unit-cost insertion, deletion, and substitution.
> L be the greater of the two string lengths.
> Then:
> normalized_character_similarity = 1 - d(s_p, s_g) / L
> If both normalized strings are empty:
> normalized_character_similarity = 1
> The result is clipped to:
> [0, 1]
> Spaces are included when calculating both the string lengths and the edit distance.
> Token-Bigram F1
> A token bigram is an ordered pair of adjacent normalized tokens.
> For example, the token sequence:
> uncertainty
> aware
> retrieval
> contains two bigrams:
> uncertainty aware
> aware retrieval
> Let:
> p_b(b) be the submitted count of bigram b.
> g_b(b) be the hidden count of bigram b.
> The bigram overlap is:
> bigram_overlap = sum over bigrams b of min(p_b(b), g_b(b))
> Let:
> m_p be the number of submitted bigrams.
> m_g be the number of hidden bigrams.
> Then:
> token_bigram_f1 = 2 × bigram_overlap / (m_p + m_g)
> Empty-input rules:
> If m_p = 0 and m_g = 0, then token_bigram_f1 = 1.
> If exactly one is zero, then token_bigram_f1 = 0.
> The repaired-question metric rewards preservation of important scientific content, including the:
> Problem.
> Method.
> Mechanism.
> Limitation.
> Application.
> Setting.
> Scope.
> Intended outcome.
> Generic repairs receive low similarity scores.
> Unnecessary paraphrasing may reduce similarity, so minimal evidence-grounded repairs are preferred.
> 12.6 Grounded Consistency
> Grounded Consistency is calculated deterministically.
> It does not contain manual, subjective, or unspecified deductions.
> For each row i, define:
> S_i = 1 when submitted support_status equals the hidden support_status; otherwise 0.
> G_i = 1 when submitted gap_type equals the hidden gap_type; otherwise 0.
> E_i as the row-level Evidence-Reference F1.
> Q_i as the row-level Repaired-Question Similarity.
> L_i as the status-gap legality indicator.
> A_i as the status-repair action indicator.
> Status-Gap Legality
> L_i = 1 in either of these cases:
> support_status is supported and gap_type is none.
> support_status is not supported and gap_type is not none.
> Otherwise:
> L_i = 0
> Therefore:
> supported with a nonnone gap type receives L_i = 0.
> A non-supported status with gap_type = none receives L_i = 0.
> Status-Repair Action
> Exact equality means the candidate and repaired questions are byte-for-byte identical, including capitalization, punctuation, and whitespace.
> Normalized equality means the two questions are identical after Common Text Normalization.
> A_i = 1 in either of these cases:
> support_status is supported and repaired_question is exactly equal to candidate_question.
> support_status is not supported and repaired_question is not normalized-equal to candidate_question.
> Otherwise:
> A_i = 0
> This enforces the following behavior:
> A supported prediction must copy the candidate exactly.
> A non-supported prediction must make a substantive normalized change.
> Changing only capitalization, punctuation, or whitespace does not count as a repair.
> Evidence-Question Joint Score
> Evidence and question agreement is measured with the harmonic mean of E_i and Q_i.
> If E_i + Q_i > 0:
> H_i = 2 × E_i × Q_i / (E_i + Q_i)
> If E_i + Q_i = 0:
> H_i = 0
> This score is high only when both the selected references and repaired question agree with the grounded answer.
> Row-Level Grounded Consistency
> The row-level score is:
> C_i = 0.25 × L_i + 0.20 × A_i + 0.20 × H_i + 0.15 × G_i × Q_i + 0.20 × S_i × Q_i
> The overall component is:
> grounded_consistency = (C_1 + C_2 + ... + C_N) / N
> Each row-level score ranges from 0 to 1.
> The fixed contributions are:
> 0.25 for a valid relationship between support_status and gap_type.
> 0.20 for performing the repair action required by the predicted status.
> 0.20 for joint agreement between evidence_refs and repaired_question.
> 0.15 for agreement between gap_type and the repaired question.
> 0.20 for agreement between support_status and the repaired question.
> Examples:
> Predicting supported with a nonnone gap removes the entire 0.25 status-gap contribution.
> Predicting a non-supported status with gap_type = none removes the entire 0.25 contribution.
> Predicting supported without copying the candidate exactly removes the entire 0.20 repair-action contribution.
> Predicting off_scope while leaving the candidate unchanged removes the entire 0.20 repair-action contribution.
> Submitting no correct evidence references makes E_i = 0, which makes the evidence-question contribution zero.
> Selecting unrelated references reduces E_i and therefore reduces H_i.
> Predicting the wrong gap type makes G_i = 0, removing the 0.15 gap-question contribution.
> Predicting the wrong support status makes S_i = 0, removing the 0.20 status-question contribution.
> A generic or unrelated repair produces a low Q_i, reducing several consistency contributions.
> All four submitted fields should therefore express one coherent judgment:
> support_status
> gap_type
> evidence_refs
> repaired_question
> 13. Intended Solving Approach
> Future Paper Oracle is best treated as a structured evidence-comparison task rather than an open-ended paper-generation task.
> A strong CPU-compatible solution may use the following pipeline.
> 13.1 Decompose the candidate question
> Identify the candidate’s central components, such as:
> Method.
> Task.
> Limitation.
> Application.
> Setting.
> Scope.
> Constraint.
> Intended outcome.
> This may be performed with a learned classifier, encoder, sequence tagger, compact language model, or another permitted semantic model.
> 13.2 Segment the literature packet
> Split references into manageable evidence units such as:
> Titles.
> Abstracts.
> Paragraphs.
> Section excerpts.
> Fixed-length passages.
> A solution is not required to process every complete paper packet in one model call.
> 13.3 Retrieve candidate evidence
> Use a learned retrieval or relevance model to identify passages that directly address candidate components.
> Useful evidence often includes:
> Explicit limitations.
> Unresolved problems.
> Negative findings.
> Future-work statements.
> Missing evaluations.
> Assumptions.
> Failure cases.
> Scope restrictions.
> Proposed extensions.
> Retrieval should prioritize direct support rather than broad topical similarity.
> 13.4 Compare candidate claims with evidence
> For each important candidate component, determine whether it is:
> Supported.
> Unsupported.
> Missing.
> Broadened.
> Altered.
> Contradicted.
> Unrelated.
> This comparison may use:
> Semantic embeddings.
> Natural-language-inference models.
> Learned classifiers.
> Rerankers.
> Compact cross-encoders.
> Sequence encoders.
> Supervised models trained on the public training data.
> 13.5 Predict a consistent judgment
> Use component-level evidence to jointly determine:
> support_status
> gap_type
> evidence_refs
> The outputs should not be predicted independently without consistency checks.
> For example:
> supported requires gap_type = none.
> Non-supported statuses require a nonnone gap.
> Selected references should support the repaired question.
> The repaired question should reflect the predicted gap type.
> 13.6 Select direct evidence references
> Select the smallest appropriate set of references that directly supports the grounded research direction.
> Avoid selecting all topically related references.
> Passage-level relevance scores may be aggregated to the reference level.
> 13.7 Apply minimal question repair
> Question repair should be treated as constrained editing whenever possible.
> Recommended behavior:
> supported: copy the candidate exactly.
> partial: replace or remove only unsupported details.
> contradicted: correct the conflicting premise.
> underspecified: insert the missing scientific detail.
> off_scope: replace the question with the closest supported direction.
> A large generative model is not required.
> A repair may be constructed using:
> Extractive phrase selection.
> Span replacement.
> Template-guided editing.
> Sequence-to-sequence generation.
> A compact instruction model.
> Nearest-neighbor retrieval from training repairs.
> Deterministic editing guided by learned semantic predictions.
> 13.8 Validate the final row
> Before writing the submission, verify that:
> Labels are valid.
> supported uses gap_type = none.
> Other statuses do not use none.
> Every evidence identifier exists in the local packet.
> Evidence references align with the repaired question.
> The repaired question is non-empty.
> Supported questions are copied exactly.
> The CSV schema and column order are correct.
> 14. CPU-Efficient Implementation Guidance
> Submitted solutions must run entirely in the provided CPU-only evaluation environment.
> Participants are encouraged to minimize unnecessary inference.
> Practical approaches include:
> Encoding each passage once.
> Encoding each candidate question once.
> Batching model inference.
> Caching reference and passage representations.
> Using sparse retrieval before neural reranking.
> Running cross-encoders only on shortlisted passages.
> Limiting generation to the final repair step.
> Using quantized models.
> Using distilled sentence encoders.
> Training lightweight classifiers on public training data.
> Combining lexical and semantic features.
> Using multiprocessing where permitted.
> Truncating or segmenting long sections instead of processing entire packets at once.
> A competitive solution does not require:
> A GPU.
> A large language model.
> A full-context generative pipeline.
> 15. Permitted Methods
> Participants may use methods that run entirely within the evaluation environment, including:
> Pretrained CPU-compatible language models.
> Compact instruction-tuned models.
> Quantized language models.
> Sentence-embedding models.
> Natural-language-inference models.
> Learned rerankers.
> Sparse retrieval.
> Dense retrieval.
> Hybrid lexical-semantic retrieval.
> Supervised classifiers trained on public training data.
> Multilabel classifiers.
> Sequence encoders.
> Sequence taggers.
> Cross-encoders.
> Gradient-boosted models.
> Linear models.
> Nearest-neighbor methods.
> Extractive evidence selection.
> Constrained question-editing systems.
> Retrieval-augmented pipelines using only supplied packets.
> Prompt engineering.
> Rule-based consistency validation.
> Deterministic post-processing.
> Ensembles of permitted models.
> Hybrid solutions are allowed.
> For example, a solution may combine:
> TF-IDF retrieval.
> A learned sentence encoder.
> A compact evidence classifier.
> Deterministic consistency rules.
> Constrained question repair.
> All required models, weights, tokenizers, assets, and dependencies must be available to the submitted notebook under the competition’s execution rules.
> No GPU is available during evaluation.
> Participants are responsible for ensuring that the complete inference pipeline is practical on CPU.
> 16. Prohibited Methods
> Participants may not:
> Manually label the private test set.
> Access hidden test labels.
> Access private competition data.
> Use unreleased challenge information.
> Use external paper repositories.
> Use external search engines.
> Use author pages.
> Use citation databases.
> Use online APIs or external inference services.
> Retrieve additional paper text from outside the supplied packets.
> Supplement supplied evidence with external scientific sources.
> Exploit row order.
> Exploit sample identifiers.
> Exploit filenames.
> Exploit deterministic construction artifacts.
> Exploit serialization details.
> Infer labels from unintended metadata signals.
> Submit outputs produced through manual private-test inspection.
> Use information unavailable through public competition files.
> Fabricate evidence identifiers.
> Cite references absent from the corresponding packet.
> Use a repaired question unrelated to the submitted evidence.
> Submit the same generic repaired question for every row.
> External scientific knowledge must not replace or override the supplied packet.
> A model may contain general pretrained knowledge, but every prediction must be grounded in the provided evidence.
> The task is not to determine whether a research question is plausible in the broader scientific literature.
> It is to determine whether the question is justified by the literature packet supplied for that sample.
> 17. Intended Challenge
> Future Paper Oracle asks systems to perform evidence-grounded scientific judgment across four linked outputs.
> A strong solution must:
> Determine whether the exact candidate is justified.
> Identify the primary research gap.
> Select the references that directly support that gap.
> Produce the closest evidence-grounded research question.
> Keep all four outputs mutually consistent.
> The main challenge is not generating a novel research idea.
> It is auditing and minimally repairing a proposed future research question using only the supplied scientific evidence.

Inspiration note: Useful because it frames retrieval around evidence routing or constrained candidate matching rather than generic document QA.

## Coded Symptom-to-Disease Diagnosis

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fkdhtx5yx2kcghpgmkqvvkd8atjyt
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> You are given short first-person patient stories written in everyday, non-technical
> language. For each story you must decide which disease best explains the patient, choosing
> from a small list of candidate diseases -- or decide that none of the listed diseases fits.
> Every disease and every clinical symptom is replaced by an opaque code, so the task cannot be
> solved by recalling medical facts about named diseases. Instead you must read a provided
> knowledge base that describes each disease by its clinical symptom profile, map the patient's
> lay wording onto those clinical findings, and reason about which disease is supported.
> Concretely, for each item you predict two things:
> answer: the single candidate disease code that best explains the patient, or the literal string NONE when no listed disease is a genuine fit.
> evidence: the symptom codes from the chosen disease's profile that the patient's story actually supports (the grounding for your answer).
> This is a retrieval-and-reasoning task, not a lookup. The link between a lay complaint such as
> "waking up drenched in sweat" and a clinical finding such as night sweats is never stated; you
> must bridge it. Surface keyword matching between the story and the profiles is deliberately
> weak, so lexical shortcuts score near the random floor.
> This is not disease-name classification. Standard symptom-to-diagnosis datasets map patient text
> onto a fixed list of named diseases, which a model can often answer from memory; the opaque codes
> remove that shortcut, so the task is retrieval and reasoning over the knowledge base rather than
> recall. It brings together, in one task, elements that existing symptom-to-diagnosis classifiers,
> synthetic patient-diary phenotyping sets, and knowledge-base diagnostic datasets implement only in
> part: anonymized disease and symptom codes, a lay-to-clinical retrieval bridge, a per-item
> differential decided partly by negative (explicitly denied) evidence, calibrated abstention when no
> candidate fits, and evidence-grounded scoring. In effect it operationalizes the standard clinical
> differential-diagnosis workflow -- gather the history, narrow the candidates with confirming and
> excluding findings, then commit to a diagnosis or defer -- over an anonymized knowledge base.
> What the task requires
> Solving an item well exercises three distinct modes of clinical reasoning:
> Relevance and abduction: infer the patient's findings from lay speech and pick the disease whose profile most completely explains them.
> Differential confirmation: use negative evidence. Patients also state what they do NOT have (for example "no, I have not noticed any drooping"). A candidate whose profile requires an explicitly denied finding should be ruled out even when it shares the presenting complaint.
> Abstention: recognize when the patient clearly has a salient finding that no listed disease accounts for, and answer NONE rather than forcing a best-guess match.
> Source and provenance
> The items are SYNTHETIC patient vignettes. Diseases and symptoms are organized in the spirit of
> standard clinical reference terminologies for disorders and findings, such as ICD-10 and
> SNOMED CT, which enumerate diseases and their characteristic manifestations. The data is
> distributed as opaque codes only. The mapping from a code back to a real disease or symptom
> name is withheld, so the cited terminologies indicate the domain and the shape of the data,
> not the answer key. Nothing here is medical advice; the data must not be used for real clinical
> decisions.
> File Structure
> test.csv - the items to solve (features only).
> train.csv - labeled example items with the same fields plus the answer and evidence.
> disease_profiles.csv - the disease knowledge base.
> symptom_glossary.csv - the symptom knowledge base.
> sample_submission.csv - a correctly formatted submission with placeholder predictions.
> Features
> test.csv and train.csv:
> id (string) - unique item identifier.
> narrative (string) - the patient's account of their complaint in lay language, including any findings they explicitly deny.
> candidates (string) - a semicolon-separated list of candidate disease codes to choose from.
> answer (string, train only) - the correct disease code, or NONE.
> evidence (string, train only) - a semicolon-separated list of supporting symptom codes, empty when the answer is NONE.
> disease_profiles.csv (the knowledge base of diseases):
> disease_code (string) - an opaque disease identifier such as D1A2B3C4D.
> symptom_codes (string) - a semicolon-separated list of the symptom codes that make up this disease's clinical profile.
> symptom_glossary.csv (the knowledge base of symptoms):
> symptom_code (string) - an opaque symptom identifier such as Y1A2B3C4.
> clinical_description (string) - a short clinical description of the finding, phrased in medical terms rather than lay terms.
> Evaluation
> Each item contributes two component scores, and the final score is their weighted mean over all
> items:
> answer score - 1.0 if your predicted answer exactly matches the correct disease code (or both are NONE), else 0.0.
> evidence score - the Jaccard overlap between your predicted set of symptom codes and the correct set. An empty prediction matched against an empty correct set scores 1.0.
> The final score is 0.75 mean(answer score) + 0.25 mean(evidence score).
> Higher is better. The theoretical range is 0.0 to 1.0, and submitting the exact answer key scores
> 1.0. Trivial strategies sit near the floor: a constant answer scores about 0.12, and a keyword or
> TF-IDF similarity solver, picking by candidate profile size, or any classifier over the candidate
> profiles' structure all score roughly 0.04 to 0.15, because they cannot read the narrative. A strong
> reasoning solver scores well below 1.0, since the opaque codes block recall and the lay-to-clinical
> gap blocks surface matching.
> Submission
> Submit a CSV with exactly these columns: id, answer, evidence.
> Provide one row per id in test.csv.
> answer is a disease code drawn from that item's candidates, or the literal NONE.
> evidence is a semicolon-separated list of symptom codes from the chosen disease's profile, or empty when answer is NONE.
> Example rows:
> te_0a1b2c3d4e, D1A2B3C4D, Y11111111;Y22222222
> te_1b2c3d4e5f, D9F8E7D6C, Y33333333
> te_2c3d4e5f6a, NONE,
> What Not To Use
> Do not attempt to reverse the codes to real disease or symptom names; the mapping is not provided and is not required. The knowledge base contains everything needed to solve an item.
> Do not rely on keyword overlap between the narrative and the profiles; it is intentionally uninformative.
> Do not use external medical databases keyed on real names; the anonymization makes them inapplicable and they will not improve the score.
> Expected Output
> For every test item, a chosen candidate disease code (or NONE) plus the supporting symptom
> codes. Ground each answer in the knowledge base: pick the disease whose profile your evidence
> codes come from, and only cite symptom codes that the patient's story supports.

Inspiration note: Useful because it frames retrieval around evidence routing or constrained candidate matching rather than generic document QA.
## Contract Workflow Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73hv1ssdgb0dma6hej13krbs8asvma
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Beat pardeep-singh's score of 0.287!

### Full Challenge Description

> Contract Workflow Reconstruction (CWR)
> Overview
> Legal contracts encode an implicit execution workflow: an ordered, conditional web of events (signing, regulatory approval, closing, termination triggers) connected by temporal and dependency relationships stated across the document ("Closing shall occur no later than the third Business Day after satisfaction of the conditions set forth in Article VI," "the Company shall pay the Termination Fee within 2 business days of such termination").
> This challenge is deliberately not a relation-extraction task. Existing contract-understanding work asks a model to extract structure that is present in the text — label a clause, classify an obligation, read off a relation from the sentence that states it. CWR does the opposite: it ablates the evidence. For each target, the exact phrase that asserts a relationship between two events is surgically removed from the document and replaced with a placeholder token [MASKED-1], [MASKED-2], ...). The asserting connective is gone. There is nothing local left to extract.
> Your task is to reconstruct each removed relationship — its type, its two endpoint events, and its numeric time parameter when applicable — from everything except the deleted evidence. Because the one place that relationship was stated has been deleted, the answer is by construction not recoverable by extraction. It can only be recovered by global document-consistency reasoning: triangulating from surviving cross-references elsewhere in the agreement, the scope of defined terms, the partial order the rest of the workflow implies, and the fact that a valid contractual workflow cannot contradict itself. A model that has merely learned to pattern-match connective phrases ("within N days of", "subject to", "prior to") will fail here, because those phrases are exactly what was removed.
> Every document comes with its own candidate node list, provided in candidate_nodes.csv, built only from events that are independently identifiable elsewhere in that specific document's surviving text. You select the two endpoints from that per-document list and classify the relationship type between them. A minority of documents are additionally tamper-perturbed by scrambling the presentation order of some numbered subsections (see Dataset) — so document position cannot be trusted as a proxy for logical order, forcing genuine reasoning over content rather than layout.
> Evaluation
> Submissions are scored using a partial-credit structured accuracy metric. Each masked instance earns credit as follows:
> 1.0 — predicted_type matches the true type AND both predicted_from and predicted_to match the true endpoints.
> 0.3 — predicted_type matches the true type AND exactly one of the two endpoints matches.
> 0.0 — otherwise (including any case where the type is wrong, even if both endpoints are right).
> Valid edge types are TEMPORAL_PRECEDENCE, CONDITIONAL_DEPENDENCY, and CROSS_REFERENCE.
> The final score is the mean credit across all graded instances, ranging from 0.0 to 1.0. Nothing else contributes to the score — in particular, the optional predicted_days column is accepted but never scored.
> Dataset
> public/train/<doc_id>.txt and public/test/<doc_id>.txt — corrupted, anonymized contract text files. Each is a plain-text merger agreement (tens of thousands of words) with party names replaced by role placeholders such as [TARGET], [ACQUIRER], [MERGER SUB], [SELLER], [PARTY A], [PARTY B], and containing one or more [MASKED-k] placeholder tokens, such as [MASKED-1] and [MASKED-2], where a structural relationship was removed. Document IDs are opaque, e.g. doc_0001 and doc_0002, and carry no information about the underlying source. Otherwise the text is the real, unmodified body of the agreement — headings, section numbering, and surrounding prose are all intact.
> public/train_labels.csv — ground truth for train-set masks only, one row per masked instance:
> doc_id (string) — matches a filename in public/train/
> mask_id (int) — which [MASKED-k] placeholder within that document this row answers
> type (string) — one of TEMPORAL_PRECEDENCE, CONDITIONAL_DEPENDENCY, CROSS_REFERENCE
> from_node (string) — the source endpoint, drawn from that document's candidate list
> to_node (string) — the target endpoint, drawn from that document's candidate list
> days (int or blank) — the numeric day-count parameter when the masked relationship had one; blank otherwise. Present for informational completeness only — not currently used in scoring (see Evaluation).
> order_scrambled (boolean: True or False) — whether this document is one of the minority with scrambled subsection order (see below)
> public/candidate_nodes.csv — the closed candidate list of valid endpoint values, one row per document/candidate pair:
> doc_id (string) — matches a filename in public/train/ or public/test/
> candidate_node_label (string) — a label that is independently recoverable from that document's surviving (unmasked) text; none are included simply because they happen to be a correct answer elsewhere
> public/sample_submission.csv — expected submission format and columns (see Submission below, including a concrete example), seeded with a neutral nearest-candidate heuristic rather than a trivial constant, so its score is a genuine easy-baseline reference point.
> A minority of documents additionally have the presentation order of some numbered subsections scrambled (content moved, numbering left in place) — flagged via the order_scrambled column — to test whether your approach relies on document position as a proxy for chronological/logical order, which will not reliably work on those documents.
> Submission
> Submit a CSV with exactly one row per doc_id/mask_id pair present in public/test/. Columns:
> doc_id (string) — document identifier
> mask_id (int) — which [MASKED-k] placeholder within that document
> predicted_type (string) — one of TEMPORAL_PRECEDENCE, CONDITIONAL_DEPENDENCY, CROSS_REFERENCE
> predicted_from (string) — must be drawn from that document's candidate_nodes.csv list
> predicted_to (string) — must be drawn from that document's candidate_nodes.csv list
> predicted_days (int or blank, optional) — accepted but not currently scored; may be omitted from the submission entirely
> Example — a valid submission's first few rows might look like:
> doc_id,mask_id,predicted_type,predicted_from,predicted_to,predicted_days
> doc_0001,1,TEMPORAL_PRECEDENCE,Satisfaction of Closing Conditions,Closing,
> doc_0001,2,CROSS_REFERENCE,Section 7.1,Adverse Recommendation Change,
> doc_0002,1,CONDITIONAL_DEPENDENCY,Effective Time,Merger,
> The full expected format and header are also provided directly in public/sample_submission.csv.
> Requirements:
> Every doc_id/mask_id pair in the test set must have exactly one row — no duplicates, no missing rows, no extra rows.
> predicted_type, predicted_from, and predicted_to must be present (non-blank) on every row.
> predicted_type must be one of the three valid enum values.
> predicted_from and predicted_to should each be drawn from the document's candidate list; values outside it cannot match and will score 0 for that component.
> Only these six columns are accepted: doc_id, mask_id, predicted_type, predicted_from, predicted_to, predicted_days. predicted_days may be omitted entirely, but no other, additional column name may appear.
> Notes for solvers
> Documents average tens of thousands of words — far beyond most transformer context windows. You will need a strategy for handling long documents (chunking, retrieval, hierarchical summarization) rather than assuming the whole document fits in one context window.
> Identifying material is scrubbed throughout: party names become role placeholders, and email addresses, URLs, law-firm names, street addresses, city/state/ZIP, monetary amounts, and explicit calendar dates are replaced with [EMAIL], [URL], [LAW FIRM], [ADDRESS], [AMOUNT], [DATE] and similar tokens. None of this affects the workflow structure you are asked to reconstruct — the scrubbed items are never endpoints of a graded relationship. Do not rely on party or deal identity as a signal, and do not attempt to de-anonymize documents.
> The masked span is deliberately narrow (tight around the connective phrase, not the whole surrounding sentence) — most of the document's context survives intact and is your primary evidence source.
> What Not to Use
> Do not use any private label, hidden metadata, or ground-truth file other than public/train_labels.csv.
> Do not attempt to identify, search for, or download the original source corpus this dataset was derived from — document identifiers and party names are deliberately anonymized specifically to prevent this, and doing so is a violation of the intended evaluation regardless of whether it happens to succeed.
> Do not use any external annotation set, third-party dataset, or corpus that could contain unmasked versions of these documents.
> Do not exploit submission-format loopholes (duplicate rows, malformed values, or any other means of inflating a score without improving predictions) — the grader rejects these, but attempting to find new ones is out of scope for a genuine solution.
> Any external data source or resource used in a submitted solution must be disclosed alongside the submission. Top-ranked submissions are subject to end-to-end reproduction, including an audit of any disclosed or attached external data — undisclosed use of an external corpus discovered at that stage disqualifies the submission.

Inspiration note: Useful for ordered route/workflow reconstruction outputs with explicit consistency constraints.
## Curatorial Search Query Challenge

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70awrs25r05gwtcm1mw4n3958b22wn
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Beat krishna_ram's score of 0.691!

### Full Challenge Description

> Curatorial Search Query Challenge
> Overview
> This is a RAG and prompt-engineering challenge about search-query design. For each row, write one compact search query that retrieves the correct hidden museum-object document from a private mini-corpus.
> In plain terms: you are given a curatorial search need and a row-local bank of allowed query terms. Your submission is not the answer object ID. Your submission is the query string that a retrieval system will run. The grader runs your query against a hidden set of object documents containing one target and many hard decoys.
> The source data comes from Smithsonian Open Access metadata. Rows are generated from source-disjoint object records and anonymous composite retrieval corpora, so looking up a public Smithsonian record cannot directly reveal the hidden target document or the best query.
> This is not classification, regression, image recognition, or ordinary QA. It evaluates whether a solver can choose discriminative retrieval terms under a strict query budget.
> Dataset Files
> train.csv contains:
> id: string. Unique training row ID.
> need_card: JSON object. The search need, facet clues, query-budget rules, and task note.
> term_bank: JSON list of strings. Row-local terms allowed in the submitted query.
> max_query_terms: integer. Maximum number of submitted query terms. Always 12.
> target_query: string. Training-only canonical query that retrieves the hidden target document.
> test.csv contains the same public columns as train.csv, but omits target_query.
> sample_submission.csv contains:
> id: string. Test row ID.
> predicted_query: string. Dummy query. The sample scores 0.
> need_card
> need_card is a JSON object with:
> task: string. Natural-language description of the kind of search needed.
> query_budget_terms: object with integer min and max values.
> literal_clues: list of strings. One target-relevant term copied into the public need; it is useful but insufficient by itself.
> facet_clues: list of objects. Each clue has:
> facet: string. One of title, object, place, person, date, material, topic, or culture.
> hint: string. Explains what kind of term may be useful.
> candidate_hint_count: integer. Count of source facet hints used when the row was generated; it is not a target label.
> note: string. Reminder that the hidden corpus contains hard decoys.
> term_bank
> term_bank is a JSON list of allowed normalized query terms. Terms are lowercase ASCII tokens such as france, porcelain, aviation, or blount. Terms are row-local: a term can be useful in one row and useless in another.
> Output Query Grammar
> Submit exactly one query string per row in the predicted_query column.
> Rules:
> The query must contain 3 to 12 terms.
> Terms are separated by single spaces after normalization.
> Every term must appear in the row's term_bank.
> Terms must be unique within a query.
> Valid terms match [a-z0-9][a-z0-9_-]{1,34}.
> Do not submit JSON, document IDs, natural-language explanations, Boolean operators, punctuation, or multiple candidate queries.
> Example valid query:
> france porcelain pitcher floral
> ## **Evaluation**
> Structurally invalid submission files are rejected. Examples include missing columns, extra columns, duplicate IDs, unknown IDs, missing rows, or wrong column order.
> Invalid row-level queries score 0 for that row. Examples include too few terms, too many terms, repeated terms, terms outside the row's `term_bank`, punctuation, document IDs, or malformed text.
> The grader aligns rows by `id`, not by row order. For each valid row, the grader runs the submitted query against a private 48-document mini-corpus using a deterministic BM25-style lexical retriever.
> For each row:
> - `Retrieval` depends on the hidden target document rank:
> - rank 1: `1.00`
> - rank 2: `0.55`
> - rank 3 to 5: `0.25`
> - rank 6 to 10: `0.10`
> - below rank 10: `0.00`
> - `FacetCoverage` is the fraction of hidden required query terms present in the submission.
> - `QueryPrecision` is the fraction of submitted terms that are hidden required query terms. If the target is not ranked first, this precision credit is halved.
> - `ExactQuery` is 1 when the submitted query exactly equals the canonical query, otherwise 0.
> If `ExactQuery` is 1, the row score is exactly 1. Otherwise:
> row_score = 0.64 * Retrieval
> 0.20 * FacetCoverage
> 0.10 * QueryPrecision
> 0.06 * ExactQuery
> Hidden rows are balanced across five private search families:
> - `material_place`
> - `maker_period`
> - `function_topic`
> - `title_medium`
> - `unit_contrast`
> Family labels are not present in public files. For each family:
> family_mean = mean(row_score for rows in that family) worst_family_mean = minimum family_mean over the five families
> The final score is:
> final_score = 0.86 * mean(row_score over all rows) + 0.14 * worst_family_mean
> The score is finite and bounded in `[0, 1]`. The sample submission scores 0. A perfect oracle scores 1.
> Participants can test query syntax and train-set behavior locally, but cannot compute the hidden retrieval score without the private mini-corpora.
> ## **Submission Format**
> Submit a CSV with exactly two columns in this order:
> - `id`: string. Test row ID.
> - `predicted_query`: string. Space-separated query terms.
> Example:
> id,predicted_query 0a12bc34de56f789,france porcelain pitcher floral
> ## **What Not To Use**
> - Do not submit Smithsonian record IDs, document aliases, URLs, JSON, Boolean syntax, or prose.
> - Do not assume public collection lookup reveals the answer. Hidden documents are generated as anonymous source-disjoint retrieval corpora with hard decoys.
> - Do not spam all terms from `term_bank`; the query budget and precision component penalize broad unfocused queries.
> - Do not optimize only one facet type. The worst-family component penalizes ignoring maker, date, place, material, title, or topic clues.
> ## **Benchmark Boundary**
> This is not MS MARCO, BEIR, ordinary passage retrieval, museum-object classification, or answer generation. Solvers do not rank provided documents directly and do not submit object IDs. They must craft a compact executable query artifact from curatorial clues and a row-local term bank, then the hidden grader measures how that query behaves against private hard-decoy corpora.

Inspiration note: Useful for benchmark designs where the model outputs a retrieval/search strategy, not just an answer.
## Evidence-Guided Sustainability Claim Retrieval and Ledger Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77ry0z55e2admt0sraf4tcw58b2m7n
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context: Beat aegistran's score of 72.513!

### Full Challenge Description

> 1. Overview
> Evidence-Guided Sustainability Claim Retrieval and Ledger Reconstruction is a structured natural-language reasoning challenge about recovering the factual history behind a damaged corporate sustainability claim.
> Each case begins with a sustainability ledger that appears credible.
> Its values, dates, units, targets, and scope descriptions resemble the language found in real corporate reports. Any individual field may appear reasonable when viewed alone.
> However, the ledger cannot automatically be trusted.
> One or more fields may have been copied from the wrong passage, attached to the wrong reporting year, interpreted using the wrong unit, broadened beyond the stated organizational scope, or confused with a future commitment rather than an achieved result.
> For every case, participants receive:
> One partially corrupted sustainability ledger.
> Twelve shuffled evidence passages.
> Exactly five passages belonging to one hidden sustainability metric thread.
> Seven authentic distractor passages.
> Eight structured repair candidates.
> One hidden corruption category.
> Participants must predict:
> The evidence candidate representing the baseline.
> The evidence candidate representing the prior result.
> The evidence candidate representing the current result.
> The evidence candidate representing the future target.
> The evidence candidate defining the shared scope or methodology.
> The corruption category affecting the draft ledger.
> The index of the best repair candidate.
> The five selected evidence candidates must be distinct.
> They correspond to the semantic roles:
> baseline
> prior_result
> current_result
> future_target
> scope_method
> The other seven evidence passages are distractors.
> The challenge is not ordinary document classification.
> It is not sentiment analysis.
> It is not a simple numerical-extraction problem.
> It is not enough to find passages containing the same percentage, year, metric name, or unit as the draft ledger.
> A distractor may contain:
> The same percentage as the correct target.
> The same unit as the correct current result.
> The same metric family as the hidden thread.
> The same reporting year.
> A related corporate commitment.
> A valid fact from another organization.
> A valid result from another reporting period.
> A facility-level statement that resembles an organization-wide result.
> A future commitment that resembles a measured outcome.
> A measured outcome that resembles a future commitment.
> A baseline reference belonging to another target.
> A methodological note that applies to a different accounting boundary.
> The participant must reconstruct one coherent sustainability narrative.
> The selected baseline, prior result, current result, future target, and scope passage must all refer to the same metric, direction, unit, organizational boundary, baseline, and temporal interpretation.
> The final output is therefore not a collection of unrelated predictions.
> It is one compact reconstruction of the complete audit case.
> 2. Dataset, Files, and Participant-Facing Fields
> The challenge is derived from a collection of corporate environmental, social, governance, and sustainability reports.
> The source collection contains approximately:
> 5,436 report records.
> Five processing snapshots.
> 2.05 GB of report text and metadata.
> Reports from multiple organizations and economic sectors.
> Cleaned report text.
> Raw extracted report text.
> Automatically analyzed report text.
> Organization descriptions.
> Publication years.
> Document categories.
> Source URLs.
> Original filenames.
> The reports discuss subjects including:
> Greenhouse gas emissions.
> Scope 3 and value-chain emissions.
> Energy consumption.
> Renewable electricity.
> Water withdrawal and consumption.
> Waste generation.
> Waste diversion and recycling.
> Biodiversity.
> Occupational safety.
> Workforce diversity.
> Leadership diversity.
> Supply-chain auditing.
> Responsible sourcing.
> Community investment.
> Net-zero commitments.
> Carbon intensity.
> Environmental compliance.
> Governance targets.
> Sustainability-linked financing.
> Source Deduplication
> The original processing snapshots are not interpreted as independent reports.
> Several snapshots may contain alternate extraction, translation, cleaning, or analysis outputs for the same underlying document.
> Before challenge construction, source records are deduplicated using combinations of:
> Normalized source URLs.
> Normalized filenames.
> Organization and publication year.
> Text fingerprints.
> MinHash similarity.
> SimHash similarity.
> Opening-text hashes.
> Closing-text hashes.
> Report-title similarity.
> Document-length similarity.
> All versions of one underlying report remain in the same challenge split.
> Cases generated from the same report also remain in the same split.
> Organizations appearing in the test set do not appear in training.
> This prevents models from succeeding by memorizing organization-specific wording or repeated versions of the same report.
> Public Package
> The participant-facing package contains:
> packets/
> train.csv
> test.csv
> sample_submission.csv
> prepare.py
> preparation.ipynb
> SOURCE_ATTRIBUTION.txt
> The preparation source and notebook document the main dataset-construction process, including:
> Source deduplication.
> Split construction.
> Case generation.
> Ledger corruption.
> Corruption-label assignment.
> Repair-candidate generation.
> Gold-repair selection.
> Repair-similarity calculation.
> Private source paths, hidden test answers, credentials, and any information that would reveal private labels must be removed before the preparation materials are released.
> Each file inside packets/ contains one complete audit case.
> The packet is the primary model input for that case.
> Private Package
> The private evaluation package may contain:
> answers.csv
> case_manifest.csv
> source_split_manifest.csv
> preparation_summary.json
> These files are used for evaluation, validation, and split-integrity checks.
> They are not released as participant inputs.
> Packet JSON Structure
> Each packet is stored as one UTF-8 JSON object.
> The top-level fields are:
> sample_id
> draft_ledger
> evidence
> repair_candidates
> field_dictionary
> sample_id
> Type: String.
> A unique opaque case identifier.
> It must not be used as a predictive feature.
> The identifier does not encode:
> Evidence membership.
> Evidence role.
> Corruption type.
> Repair index.
> Source organization.
> Source report.
> Case difficulty.
> draft_ledger
> Type: JSON object.
> The participant-facing structured sustainability claim.
> It contains the following eleven fields:
> metric
> direction
> unit
> baseline_year
> prior_value
> prior_year
> current_value
> current_year
> target_value
> target_year
> scope
> metric
> Type: String.
> The normalized sustainability metric represented by the ledger.
> Examples include:
> Operational greenhouse gas emissions.
> Value-chain greenhouse gas emissions.
> Operational energy consumption.
> Renewable-energy share.
> Water withdrawal and consumption.
> Operational waste generation.
> Waste diversion and recycling.
> Workforce gender representation.
> Leadership gender representation.
> Supplier sustainability assurance.
> Workplace safety performance.
> direction
> Type: String.
> The direction in which the metric changes or is intended to change.
> Typical values include:
> increase
> decrease
> unit
> Type: String.
> The normalized measurement unit or measurement mode associated with the ledger.
> The unit helps distinguish claims that may contain the same numerical value but represent different kinds of measurement.
> baseline_year
> Type: Integer.
> The reference year against which later results or targets are compared.
> prior_value
> Type: Number.
> An earlier measured value or progress value belonging to the hidden thread.
> prior_year
> Type: Integer.
> The year associated with prior_value.
> current_value
> Type: Number.
> The most recent measured value represented by the case.
> current_year
> Type: Integer.
> The year associated with current_value.
> target_value
> Type: Number.
> The future target value represented by the case.
> target_year
> Type: Integer.
> The year associated with target_value.
> scope
> Type: String.
> The normalized organizational, geographic, operational, or methodological boundary of the claim.
> Examples include:
> Scope 1 and Scope 2 operations.
> Scope 3 value-chain activity.
> Global operations.
> Selected sites.
> Supply-chain activity.
> Workforce coverage.
> Market-based accounting.
> Location-based accounting.
> Intensity-based measurement.
> Absolute measurement.
> A restated reporting boundary.
> evidence
> Type: JSON array.
> The array contains exactly twelve evidence objects.
> Each evidence object contains:
> candidate_id
> text
> candidate_id
> Type: Integer.
> Allowed values are 0 through 11.
> Candidate IDs are unique within one packet.
> The ordering is randomized independently for every case.
> text
> Type: String.
> A normalized sustainability-report passage.
> Passages are bounded in length and may contain:
> Numerical values.
> Reporting years.
> Baseline years.
> Target years.
> Metric terminology.
> Directional language.
> Scope qualifiers.
> Accounting-method descriptions.
> Statements of achieved results.
> Statements of future commitments.
> Exactly five passages belong to the hidden metric thread.
> The other seven are authentic distractors.
> repair_candidates
> Type: JSON array.
> The array contains exactly eight repair objects.
> Each repair object contains:
> repair_id
> patch
> repair_id
> Type: Integer.
> Allowed values are 0 through 7.
> Repair IDs are unique within one packet.
> Repair order is randomized independently for every case.
> patch
> Type: JSON array.
> A structured list of proposed ledger edits.
> An empty patch represents a no-change repair.
> Every non-empty patch operation contains:
> field
> value
> field
> Type: String.
> The ledger field to replace.
> It refers to one of the eleven supported draft-ledger fields.
> value
> Type: String, integer, number, or null.
> The replacement value assigned to the specified field.
> field_dictionary
> Type: JSON object.
> A compact packet-level explanation of selected ledger fields.
> It may describe fields such as:
> unit
> baseline_year
> prior_value
> current_value
> target_value
> scope
> The field dictionary is descriptive.
> It does not contain hidden labels.
> Public Text Normalization
> Evidence passages are normalized to reduce direct source identification while preserving the information needed for the challenge.
> Normalization may include:
> Organization-name replacement.
> Product-name replacement.
> Facility-name replacement.
> URL removal.
> Email removal.
> Footer removal.
> Header removal.
> Whitespace normalization.
> Unicode normalization.
> Standardization of common unit spellings.
> Replacement of rare named locations with generic placeholders.
> The following information is preserved whenever relevant:
> Numerical values.
> Units.
> Years.
> Comparison phrases.
> Baseline language.
> Target language.
> Scope language.
> Methodological qualifiers.
> Increase or decrease direction.
> Absolute-versus-intensity distinctions.
> 3. Evaluation
> The primary metric is the Baseline-Normalized Compact Grounded Ledger Reconstruction Score.
> Higher scores are better.
> The metric contains three task components:
> Thread Reconstruction Utility.
> Corruption Diagnosis Utility.
> Repair Selection Utility.
> Each component is first calculated as a raw utility.
> The evaluator then normalizes that raw utility against the strongest constant no-skill strategy for the same component.
> This prevents submissions that ignore the individual case contents from receiving substantial credit merely because of class imbalance, candidate-position imbalance, or highly similar repair candidates.
> 3.1 Overall Formula
> Let:
> (T_{\text{raw}}) be Raw Thread Reconstruction Utility.
> (C_{\text{raw}}) be Raw Corruption Diagnosis Utility.
> (R_{\text{raw}}) be Raw Repair Selection Utility.
> (B_T) be the thread no-skill baseline.
> (B_C) be the corruption no-skill baseline.
> (B_R) be the repair no-skill baseline.
> Each component is normalized as:
> [
> T = \max\left(0,\frac{T_{\text{raw}}-B_T}{1-B_T}\right)
> ]
> [
> C = \max\left(0,\frac{C_{\text{raw}}-B_C}{1-B_C}\right)
> ]
> [
> R = \max\left(0,\frac{R_{\text{raw}}-B_R}{1-B_R}\right)
> ]
> A no-skill result receives a normalized utility near 0.
> A perfect result receives a normalized utility of 1.
> A result below the no-skill baseline is clipped to 0.
> The final score is:
> [
> \text{Final Score}
> ==================
> 100 \times
> \left(
> \frac{8}{17}T
> \frac{3}{17}C
> \frac{6}{17}R
> \right)
> ]
> Equivalently:
> [
> \text{Final Score}
> ==================
> 100 \times
> (0.470588T + 0.176471C + 0.352941R)
> ]
> The relative importance of thread, corruption, and repair is preserved from the original weighting scheme after removing the confidence component.
> The score is clipped to the range from 0 through 100.
> The metric rewards:
> Recovery of the correct five evidence candidates.
> Correct assignment of each evidence role.
> Exact reconstruction of the complete five-role thread.
> Correct corruption diagnosis.
> Selection of repairs that are close to the hidden correct ledger.
> Selection of the unique gold repair.
> Performance above the strongest constant no-skill strategy.
> 3.2 Thread Reconstruction Utility
> Each prediction identifies one evidence candidate for each of five roles:
> Baseline.
> Prior result.
> Current result.
> Future target.
> Scope and methodology.
> Let the five gold candidate IDs form the gold role assignment.
> Let the five submitted candidate IDs form the predicted role assignment.
> Raw Thread Reconstruction Utility combines three measurements.
> Evidence-Set Overlap
> The submitted five candidate IDs are treated as a set.
> The gold five candidate IDs are also treated as a set.
> For one case:
> [
> \text{Evidence-Set Overlap}
> ===========================
> \frac{\text{number of candidate IDs appearing in both sets}}{5}
> ]
> This component ignores role assignment.
> It rewards finding the correct evidence even when one or more passages are assigned to the wrong role.
> Mean Evidence-Set Overlap is calculated over all test cases.
> Role-Edge Accuracy
> The evaluator compares every role-specific prediction directly with its gold candidate.
> One role edge is correct when the submitted candidate for that role equals the gold candidate for that role.
> For one case:
> [
> \text{Role-Edge Accuracy}
> =========================
> \frac{\text{number of correctly assigned roles}}{5}
> ]
> A candidate only receives role-edge credit when it is attached to the correct semantic role.
> Mean Role-Edge Accuracy is calculated over all test cases.
> Exact Thread Accuracy
> A case has an exact thread when all five submitted role assignments are correct:
> baseline_candidate is correct.
> prior_candidate is correct.
> current_candidate is correct.
> target_candidate is correct.
> scope_candidate is correct.
> Exact Thread Accuracy is the fraction of test cases with a completely exact five-role assignment.
> Raw Thread Formula
> Raw Thread Reconstruction Utility is:
> [
> T_{\text{raw}}
> ==============
> 0.25 \times \text{Mean Evidence-Set Overlap}
> 0.50 \times \text{Mean Role-Edge Accuracy}
> 0.25 \times \text{Exact Thread Accuracy}
> ]
> This component gives partial credit for recovering useful evidence while placing the greatest weight on correct role-specific relationships.
> Thread No-Skill Baseline
> The thread no-skill baseline is the highest Raw Thread Reconstruction Utility achievable by submitting the same fixed valid five-role assignment for every test case.
> The fixed prediction must:
> Assign one candidate ID to each of the five roles.
> Use candidate IDs from 0 through 11.
> Use five distinct candidate IDs.
> Remain identical for every test case.
> The evaluator considers the strongest such constant ordered assignment.
> This baseline removes credit arising from candidate-position imbalance or global role-position regularities that can be exploited without reading the case evidence.
> The normalized Thread Reconstruction Utility is:
> [
> T
> =
> \max\left(0,\frac{T_{\text{raw}}-B_T}{1-B_T}\right)
> ]
> 3.3 Corruption Diagnosis Utility
> The participant submits one categorical corruption_type.
> The prediction is compared directly with the hidden corruption category.
> A case receives:
> 1 when the submitted category is exactly correct.
> 0 otherwise.
> Raw Corruption Diagnosis Utility is the mean exact corruption accuracy over all test cases:
> [
> C_{\text{raw}}
> ==============
> \text{Mean Exact Corruption Accuracy}
> ]
> No partial credit is awarded between different corruption categories.
> Corruption No-Skill Baseline
> The corruption no-skill baseline is the highest accuracy achievable by predicting the same corruption category for every test case.
> It is equal to the frequency of the most common hidden corruption category in the evaluation set.
> This baseline removes credit obtained solely by predicting the majority corruption label.
> The normalized Corruption Diagnosis Utility is:
> [
> C
> =
> \max\left(0,\frac{C_{\text{raw}}-B_C}{1-B_C}\right)
> ]
> 3.4 Repair Selection Utility
> Each case contains eight repair candidates.
> The participant selects one candidate using repair_index.
> Raw repair scoring combines:
> The hidden similarity of the selected repair to the correct ledger.
> Whether the exact gold repair index was selected.
> Candidate-Ledger Agreement
> Each repair patch is applied to the draft ledger.
> The resulting ledger is compared with the hidden correct ledger.
> The evaluated fields and weights are:
> metric, weight 3.
> direction, weight 2.
> unit, weight 2.
> baseline_year, weight 2.
> prior_value, weight 2.
> prior_year, weight 1.
> current_value, weight 3.
> current_year, weight 2.
> target_value, weight 3.
> target_year, weight 2.
> scope, weight 3.
> The total field weight is 25.
> Field Agreement is:
> [
> \text{Field Agreement}
> ======================
> \frac{\text{sum of weights for correctly reconstructed fields}}{25}
> ]
> String and integer fields must match the hidden values.
> Numerical values are compared using a small numerical tolerance.
> Minimality Factor
> A repair should not receive full credit merely because it reaches the correct final ledger through unnecessary edits.
> Let:
> (g) be the number of edits in the gold minimal patch.
> (e_k) be the number of edits in candidate repair (k).
> The minimality factor for candidate (k) is:
> [
> \text{Minimality Factor}_k
> ==========================
> \min\left(1,\frac{g+1}{e_k+1}\right)
> ]
> A candidate that changes more fields than the gold repair receives a penalty.
> A candidate that changes too few fields is not directly penalized by this factor, but its incomplete final ledger lowers Field Agreement.
> Repair Similarity
> For candidate (k):
> [
> \text{Repair Similarity}_k
> ==========================
> \text{Field Agreement}_k
> \times
> \text{Minimality Factor}_k
> ]
> Every candidate similarity lies between 0 and 1.
> The gold repair has similarity 1.
> The private evaluator stores the eight repair similarities for each case.
> Selected Repair Similarity
> Selected Repair Similarity is the mean hidden similarity of the repair candidates chosen by participants.
> This gives partial credit when the selected repair is close to the hidden correct ledger.
> Exact Repair Accuracy
> A case receives exact-repair credit when the submitted repair_index equals the hidden gold repair index.
> Exact Repair Accuracy is the fraction of cases with the exact gold repair.
> Raw Repair Formula
> Raw Repair Selection Utility is:
> [
> R_{\text{raw}}
> ==============
> 0.75 \times \text{Mean Selected Repair Similarity}
> 0.25 \times \text{Exact Repair Accuracy}
> ]
> This component rewards near-correct reconstruction while preserving a separate incentive to identify the unique smallest correct patch.
> Repair No-Skill Baseline
> The repair no-skill baseline is the highest Raw Repair Selection Utility achievable by selecting the same repair index for every test case.
> For each fixed repair index from 0 through 7, the evaluator calculates:
> Mean Selected Repair Similarity for that fixed index.
> Exact Repair Accuracy for that fixed index.
> The corresponding raw repair utility.
> The strongest fixed repair index becomes the repair no-skill baseline.
> This specifically removes credit obtained from always selecting a generally strong candidate, such as a no-change patch that preserves most already-correct ledger fields.
> The normalized Repair Selection Utility is:
> [
> R
> =
> \max\left(0,\frac{R_{\text{raw}}-B_R}{1-B_R}\right)
> ]
> 3.5 Metric Interpretation
> The no-skill baselines are calculated from the private answer table and remain the same for every participant submission.
> They do not depend on a participant’s predictions.
> The normalization has the following interpretation:
> A component score equal to its strongest constant baseline maps to 0.
> A component score below that baseline also maps to 0.
> A component score between the baseline and perfection is scaled proportionally.
> A perfect component score maps to 1.
> The detailed evaluator may report, for each component:
> Raw utility.
> No-skill baseline.
> Baseline-normalized utility.
> Supporting diagnostic statistics.
> Only the baseline-normalized utilities contribute to the final leaderboard score.
> 4. Prediction Task and Novelty
> Most claim-verification benchmarks begin with a trusted claim and ask whether one passage supports it.
> This challenge begins from a different premise:
> The claim itself may be damaged.
> The draft ledger is not merely the query.
> It is part of the forensic problem.
> A model that treats every ledger field as trustworthy may retrieve evidence supporting the corruption rather than evidence recovering the underlying truth.
> Most evidence-retrieval tasks evaluate passages independently.
> Here, five passages must be recovered together.
> A passage that looks convincing alone may become incompatible when placed beside the proposed baseline, current result, future target, or scope statement.
> Most timeline-reconstruction tasks provide events already known to belong together.
> Here, seven of the twelve passages are distractors.
> The model must discover the hidden metric thread before it can reconstruct its internal roles.
> Most numerical-reasoning benchmarks emphasize finding the right number.
> Here, the same number may appear in several incompatible contexts.
> A value such as 50 percent may describe:
> A future emissions-reduction target.
> A current recycling rate.
> A reduction at one manufacturing facility.
> The share of renewable electricity.
> A workforce-diversity goal.
> A supplier-assurance threshold.
> A result reported by another organization.
> A comparison against another baseline year.
> The number alone is not the answer.
> Its meaning depends on:
> The metric.
> The unit.
> The direction.
> The reporting year.
> The baseline year.
> The organizational scope.
> Whether the value is measured or planned.
> Which other passages belong to the same thread.
> Most fact-correction tasks permit unrestricted generated text.
> This challenge instead provides eight bounded repair candidates.
> Only one candidate is the unique smallest correct repair.
> The alternatives may:
> Correct the value but damage the year.
> Correct the year but broaden the scope.
> Reach the correct final ledger through unnecessary edits.
> Copy a valid number from irrelevant evidence.
> Convert a target into an achieved result.
> Convert an achieved result into a target.
> Correct one field while leaving another corruption untouched.
> Replace the correct metric with a related metric.
> Make no change to a corrupted ledger.
> The benchmark therefore combines:
> Evidence retrieval.
> Hard-negative rejection.
> Hidden-thread discovery.
> Semantic role assignment.
> Temporal claim reconstruction.
> Numerical interpretation.
> Unit reasoning.
> Baseline reasoning.
> Scope resolution.
> Target-versus-actual reasoning.
> Corruption diagnosis.
> Counterfactual repair ranking.
> Minimum-edit recovery.
> Baseline-normalized evaluation.
> The defining question is not whether one passage discusses a similar topic.
> The defining question is whether five passages jointly form the exact claim history that explains the ledger and its smallest justified repair.
> 5. Hidden Claim Threads
> Every case contains exactly one hidden sustainability metric thread.
> The thread is represented by five evidence passages with distinct roles.
> Baseline
> The baseline passage establishes the reference point used to interpret later progress, performance, or commitments.
> It may specify:
> A baseline year.
> A baseline quantity.
> A reference condition.
> A methodological restatement.
> A recalculated historical baseline.
> The beginning of a target period.
> The baseline role is semantic.
> It is not determined by the passage’s location in the packet or source report.
> Prior Result
> The prior-result passage describes an earlier measured outcome between the baseline and the current reporting period.
> It may provide:
> An earlier percentage reduction.
> An earlier absolute value.
> A previous reporting-year result.
> Earlier progress toward the same target.
> A prior intensity measurement.
> A previously disclosed operational outcome.
> Current Result
> The current-result passage describes the most recent measured outcome represented by the case.
> It may provide:
> A current value.
> A cumulative reduction.
> A year-on-year change.
> An absolute quantity.
> Current progress against a baseline.
> The latest disclosed intensity or rate.
> The current result represents an achieved or measured state.
> It must not be confused with a future target.
> Future Target
> The future-target passage describes a commitment associated with a future date or future operating condition.
> It may provide:
> A target value.
> A target year.
> A net-zero commitment.
> An interim reduction target.
> A planned threshold.
> A future coverage goal.
> A future target may use the same value and unit as a current result while representing a completely different temporal status.
> Scope and Method
> The scope-method passage defines how the other four passages should be interpreted.
> It may specify:
> Organizational coverage.
> Geographic coverage.
> Included emissions scopes.
> Whether measurement is absolute or intensity-based.
> Whether acquisitions are included.
> Whether divestments are excluded.
> Whether accounting is market-based or location-based.
> Whether the result applies only to selected sites.
> Whether supplier activity is included.
> Whether a reporting boundary was restated.
> The scope passage may not contain the headline numerical value.
> Its role is to establish what the numbers mean.
> Temporal Structure
> Four roles form an ordered sequence:
> Baseline.
> Prior result.
> Current result.
> Future target.
> The scope-method passage applies across the complete sequence.
> A representative hidden thread may describe:
> A 2019 baseline.
> A 12 percent reduction by 2021.
> An 18 percent reduction by 2023.
> A 50 percent reduction target by 2030.
> The scope passage may establish that the thread concerns global Scope 1 and Scope 2 operational emissions.
> The temporal order represents meaning.
> It does not represent:
> Candidate order in the packet.
> Original page order.
> Extraction order.
> Source-file order.
> The order in which passages appear in a report.
> 6. Hard Distractors
> Every case contains seven authentic distractor passages.
> Distractors are not random text.
> They are not corrupted Unicode, artificial word salad, or unrelated generic sentences.
> They are selected because they can plausibly compete with the true evidence.
> A distractor may share:
> The source organization.
> The source report.
> The economic sector.
> The metric family.
> The unit.
> The numerical value.
> The publication year.
> The target vocabulary.
> The direction of change.
> The same general sustainability topic.
> Distractors may come from:
> Another metric in the same report.
> Another section of the same report.
> Another year from the same organization.
> Another organization with a similar target.
> A methodological note that does not apply to the target metric.
> A table footnote using the same number.
> A regional result rather than a global result.
> A facility-level result rather than an organization-wide result.
> A supplier metric rather than an operational metric.
> An achieved result rather than a future target.
> A future target rather than an achieved result.
> Several distractors may form a plausible alternative thread.
> A model may therefore identify five passages that appear mutually compatible while still describing:
> The wrong metric.
> The wrong scope.
> The wrong reporting period.
> The wrong baseline.
> The wrong organization.
> The wrong accounting method.
> A passage is correct because it contributes to the globally coherent hidden ledger.
> Similarity to one draft-ledger field is not sufficient.
> 7. Corruption Categories
> The draft ledger is generated from the hidden correct ledger and then optionally corrupted.
> The allowed corruption categories are:
> clean
> wrong_metric
> wrong_value
> wrong_unit
> wrong_year
> direction_flip
> scope_shift
> baseline_shift
> target_as_actual
> actual_as_target
> foreign_fact
> multi_error
> Clean
> The draft ledger is already correct.
> The unique correct repair makes no changes.
> Wrong Metric
> The ledger uses the wrong sustainability metric.
> Its numerical values and years may still be plausible.
> For example, a water-withdrawal reduction may be represented as an emissions reduction.
> Wrong Value
> At least one of the following contains an incorrect number:
> prior_value
> current_value
> target_value
> The incorrect number may be taken from another true or distractor passage in the same packet.
> Wrong Unit
> The magnitude may be plausible while the unit or measurement mode is incorrect.
> Examples include:
> Percentage points instead of percent.
> Tonnes instead of a percentage.
> Absolute measurement instead of intensity.
> One normalized measurement family replaced by another.
> Wrong Year
> A prior-result year, current-result year, or target year is incorrect.
> The substituted year may still appear elsewhere in the case.
> Direction Flip
> An increase is represented as a decrease, or a decrease is represented as an increase.
> Scope Shift
> The ledger is assigned to the wrong organizational or methodological boundary.
> Examples include:
> Selected sites becoming global operations.
> Scope 2 becoming Scope 1 and Scope 2.
> Market-based accounting becoming location-based accounting.
> Operational activity becoming supply-chain activity.
> Baseline Shift
> The comparison is attached to the wrong baseline year.
> The result may be real while its reference point is incorrect.
> Target as Actual
> A future target is copied into the current-result fields.
> The draft may incorrectly present a future commitment as an achieved outcome.
> Actual as Target
> A measured current result is copied into the target fields.
> The draft may incorrectly present an achieved outcome as a future commitment.
> Foreign Fact
> One or more fields are imported from another metric thread or distractor passage.
> The imported fact may be authentic in its original context.
> It is incorrect within the current ledger.
> Multi-Error
> The draft contains several interacting errors.
> A multi-error case may combine:
> A wrong value.
> A wrong year.
> A direction flip.
> A scope shift.
> The correct repair must resolve the complete corruption rather than only its most visible component.
> 8. Repair Candidates
> Every case contains exactly eight repair candidates.
> A repair candidate is a structured patch applied to the draft ledger.
> A patch may:
> Replace one field.
> Replace several fields.
> Restore a missing value.
> Replace an unsupported value.
> Make no changes.
> The candidate set may include:
> The exact gold patch.
> A no-change patch.
> Individual fragments of the gold patch.
> A patch containing all gold edits plus one unnecessary edit.
> A patch changing the wrong metric.
> A patch changing the wrong unit.
> A patch changing the wrong year.
> A patch copying a plausible distractor value.
> Exactly one repair candidate is the unique smallest patch that produces the hidden correct ledger.
> A repair that reaches the correct final ledger through unnecessary edits is not treated as equivalent to the gold repair.
> This distinction is deliberate.
> The task evaluates whether a model can:
> Recover the correct final ledger.
> Preserve fields that were already correct.
> Avoid unsupported edits.
> Identify the smallest evidence-justified correction.
> Near-correct repairs receive partial metric credit through their hidden Repair Similarity.
> Because repair utility is normalized against the strongest fixed repair-index strategy, a generally safe candidate such as a no-change patch does not automatically receive substantial leaderboard credit.
> 9. Training Data
> train.csv contains one row per labeled training case.
> Its columns are:
> sample_id
> packet_file
> baseline_candidate
> prior_candidate
> current_candidate
> target_candidate
> scope_candidate
> corruption_type
> repair_index
> sample_id
> Type: String.
> The opaque case identifier.
> It must not be used as a predictive feature.
> packet_file
> Type: String.
> The relative path to the corresponding packet JSON file.
> A representative value is:
> packets/ledger_a1b2c3d4e5f6.json
> ### `baseline_candidate`
> Type: Integer.
> The candidate ID of the true baseline passage.
> Allowed values are 0 through 11.
> ### `prior_candidate`
> Type: Integer.
> The candidate ID of the true prior-result passage.
> Allowed values are 0 through 11.
> ### `current_candidate`
> Type: Integer.
> The candidate ID of the true current-result passage.
> Allowed values are 0 through 11.
> ### `target_candidate`
> Type: Integer.
> The candidate ID of the true future-target passage.
> Allowed values are 0 through 11.
> ### `scope_candidate`
> Type: Integer.
> The candidate ID of the true scope-method passage.
> Allowed values are 0 through 11.
> The five role-specific candidate IDs are always distinct.
> ### `corruption_type`
> Type: String.
> The hidden corruption category.
> It must be one of the twelve allowed labels.
> ### `repair_index`
> Type: Integer.
> The index of the unique smallest correct repair.
> Allowed values are 0 through 7.
> Repair candidate order is randomized independently for every case.
> ---
> ## 10. Test Data
> `test.csv` contains one row per evaluation case.
> Its columns are:
> * `sample_id`
> * `packet_file`
> ### `sample_id`
> Type: String.
> The opaque evaluation-case identifier.
> ### `packet_file`
> Type: String.
> The relative path to the corresponding packet JSON file.
> Gold role assignments, corruption categories, repair indices, and repair similarities are hidden.
> Test cases follow the same structural rules as training cases:
> * Exactly twelve evidence passages.
> * Exactly five true evidence members.
> * Exactly one true passage for each semantic role.
> * Exactly seven distractors.
> * Exactly eight repair candidates.
> * Exactly one corruption category.
> * Exactly one gold repair.
> The private test split emphasizes:
> * Organizations not present in training.
> * Uncommon sustainability topics.
> * Multi-error ledgers.
> * Scope shifts.
> * Baseline shifts.
> * Target-versus-actual confusion.
> * Similar-number distractors.
> * Plausible alternative evidence threads.
> * Repairs with similar final ledgers but different edit counts.
> ---
> ## 11. Submission Schema
> The official submission must contain exactly eight columns:
> * `sample_id`
> * `baseline_candidate`
> * `prior_candidate`
> * `current_candidate`
> * `target_candidate`
> * `scope_candidate`
> * `corruption_type`
> * `repair_index`
> Participants should use `sample_submission.csv` as the authoritative template for column names and column order.
> ### Role-Specific Candidate Predictions
> The following columns contain evidence candidate IDs:
> * `baseline_candidate`
> * `prior_candidate`
> * `current_candidate`
> * `target_candidate`
> * `scope_candidate`
> Each value must be an integer from 0 through 11.
> The five submitted values must be distinct within each row.
> The participant submits one direct candidate assignment for each role.
> The submission does not contain twelve membership probabilities or candidate-level role distributions.
> ### `corruption_type`
> Type: String.
> The selected corruption category.
> Allowed values are:
> * `clean`
> * `wrong_metric`
> * `wrong_value`
> * `wrong_unit`
> * `wrong_year`
> * `direction_flip`
> * `scope_shift`
> * `baseline_shift`
> * `target_as_actual`
> * `actual_as_target`
> * `foreign_fact`
> * `multi_error`
> ### `repair_index`
> Type: Integer.
> The selected repair candidate.
> Allowed values are 0 through 7.
> ### Legacy Confidence Columns
> For backward compatibility, the evaluator may also accept the following four legacy columns when all four are present together:
> * `p_thread`
> * `p_corruption`
> * `p_repair`
> * `p_audit`
> These legacy values:
> * Do not contribute to the score.
> * Do not affect any component utility.
> * Are not included in the official `sample_submission.csv`.
> * Should not be included in new submissions.
> When legacy confidence columns are supplied, they must still contain finite numeric values from 0 through 1.
> Supplying only some of the four legacy columns is invalid.
> ---
> ## 12. Correctly Formatted Submission Example
> The following is a complete correctly formatted one-row submission.
> Submission Header
> sample_id,baseline_candidate,prior_candidate,current_candidate,target_candidate,scope_candidate,corruption_type,repair_index
> Submission Row
> ledger_example001,0,1,2,3,4,clean,0
> This row is structurally valid but intentionally uninformative.
> It predicts:
> Candidate 0 as the baseline.
> Candidate 1 as the prior result.
> Candidate 2 as the current result.
> Candidate 3 as the future target.
> Candidate 4 as the scope-method passage.
> clean as the corruption category.
> Repair candidate 0.
> Participants must preserve the exact official column names and replace the example values with model-generated predictions.
> The official submission format does not require confidence values.
> 13. Submission Validation
> A submission is invalid and receives a score of 0 when any of the following occurs:
> The submission is not a valid table.
> A required column is missing.
> An unknown extra column is present.
> A column name is duplicated.
> A required sample_id is missing.
> An unknown sample_id is included.
> A sample_id appears more than once.
> A sample_id is blank.
> The submission contains the wrong number of rows.
> A role-specific candidate value is non-numeric.
> A role-specific candidate value is not an integer.
> A role-specific candidate value is outside 0 through 11.
> The same evidence candidate is assigned to more than one role in one row.
> corruption_type is missing.
> corruption_type is not one of the twelve allowed categories.
> repair_index is non-numeric.
> repair_index is not an integer.
> repair_index is outside 0 through 7.
> The submission does not contain every required test sample_id exactly once.
> Only some of the four optional legacy confidence columns are supplied.
> A supplied legacy confidence value is non-numeric.
> A supplied legacy confidence value is NaN.
> A supplied legacy confidence value is infinite.
> A supplied legacy confidence value is below 0.
> A supplied legacy confidence value is above 1.
> The following columns are the only optional extra columns accepted for backward compatibility:
> p_thread
> p_corruption
> p_repair
> p_audit
> All four must be supplied together.
> They are validated but ignored during scoring.
> Submission row order does not affect scoring.
> The evaluator merges predictions with hidden answers by sample_id.
> The evaluator does not:
> Access external services.
> Run participant models.
> Download additional data.
> Infer missing submission values.
> Use legacy confidence values in the score.
> The evaluator only:
> Validates the submitted table.
> Loads hidden labels and repair similarities.
> Compares the five submitted role assignments.
> Compares the corruption category.
> Scores the selected repair.
> Calculates no-skill baselines from the hidden answer table.
> Normalizes the three component utilities.
> Calculates the published metric.
> The evaluator is CPU-only and uses bounded memory.
> 14. Restrictions, Data Integrity, and Responsible Use
> Participants must base predictions primarily on the supplied case packets.
> Predictions may not use:
> sample_id as a predictive feature.
> Packet filename patterns.
> CSV row order.
> File sizes.
> File modification times.
> JSON formatting differences.
> Candidate-ordering artifacts.
> Compression characteristics.
> Hidden source identifiers.
> Recovered organization identities.
> Original report URLs.
> Original source filenames.
> External copies of the reports.
> Internet searches for exact source passages.
> Hardcoded private-test predictions.
> Manual lookup of private test cases.
> The benchmark is designed to evaluate evidence-grounded claim reconstruction.
> It is not designed to evaluate source identification, company recognition, or metadata exploitation.
> The benchmark concerns consistency between supplied evidence and a hidden normalized ledger.
> It does not certify that:
> An organization is environmentally responsible.
> A sustainability report is truthful.
> A future target will be achieved.
> A reported metric has been independently verified.
> An organization complies with regulations.
> An organization is suitable for investment.
> The labels represent the intended interpretation of the supplied challenge case.
> They do not constitute:
> Legal advice.
> Financial advice.
> Regulatory advice.
> Investment advice.
> Independent sustainability assurance.
> Source attribution and applicable license notices must be preserved in the released competition package.
> The released preparation source and notebook are provided for auditability.
> They must not contain:
> Private-test answers.
> Hidden labels for unreleased cases.
> Credentials or access tokens.
> Private source-system paths.
> Personal information not otherwise licensed for release.
> Information that permits direct reconstruction of private evaluation labels.
> 15. Modeling Guidance, Restrictions, and Summary
> The challenge is designed for machine-learning systems that jointly learn:
> Candidate-level evidence representations.
> Relationships between candidate passages.
> Hidden claim-thread membership.
> Semantic and temporal evidence roles.
> Ledger-corruption characteristics.
> Repair-candidate compatibility.
> Complete-case consistency.
> A successful model should not treat the required outputs as unrelated prediction tasks.
> Evidence selection affects role assignment.
> Role assignment determines the reconstructed claim thread.
> The reconstructed thread affects which corruption explanation is plausible.
> The corruption category affects which repairs are compatible with the draft ledger.
> The repair decision determines whether the complete audit is coherent.
> Because the evaluation components are normalized against constant no-skill baselines, systems must use case-specific evidence to receive meaningful leaderboard credit.
> Strategies that always predict:
> The same evidence-role assignment.
> The most common corruption category.
> The same repair index.
> A no-change repair.
> should receive little or no normalized credit unless they outperform the corresponding private no-skill baseline.
> The provided environment includes:
> 10 CPU cores.
> 64 GB RAM.
> No GPU.
> Participants should favor models that can be trained and evaluated within these limits.
> Practical approaches may use:
> Compact neural encoders.
> Shared candidate embeddings.
> Cached text representations.
> Batched candidate-pair evaluation.
> Lightweight attention layers.
> Reduced-dimensional evidence features.
> Efficient cross-validation.
> Small ensembles.
> Multi-task classification architectures.
> Candidate-set encoders.
> Pairwise or listwise ranking objectives.
> Learned compatibility functions.
> Joint evidence-and-repair models.
> Distilled language representations that run efficiently on CPU.
> The core task is to recover one coherent and evidence-grounded sustainability claim history.
> A strong submission must identify:
> Which five passages belong together.
> Which semantic role each passage performs.
> How the draft ledger was corrupted.
> Which repair is the smallest complete correction.
> The final score rewards performance above the strongest constant strategy rather than rewarding structural validity alone.

Inspiration note: Useful for benchmark designs where the model outputs a retrieval/search strategy, not just an answer.

## Dyadic Understanding Checkpoint Retrieval

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74eghbt99h9mmwr7jbgthv5s8b4wqw
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> The data come from real German conversations in which one person explains how to play a board game to another person. After each conversation, the explainer and explainee separately review the recording. Each pauses at moments where they believe the explainee understood, partly understood, failed to understand, or misunderstood something.
> A candidate moment is a timestamp mentioned by at least one participant during that later review. A dyadic checkpoint is a candidate mentioned by both participants. Your task is retrieval: order each conversation's candidates so that dyadic checkpoints appear before one-party checkpoints.
> For every candidate, the input contains only behavior from the original conversation before that timestamp: speech transcript, discourse functions, backchannels, gaze, and gestures. The later review comments are not included. The private set contains entirely unseen explainers. This tests whether a retrieval system can identify transferable signs of jointly noticed understanding events. Such rankings can help analysts select a small number of explanation moments for closer review.
> Dataset
> File descriptions
> train.csv: candidate moments from training explainers. Each row includes its conversation group, interaction context, numeric summaries, and retrieval relevance.
> test.csv: candidates from four unseen explainers. It has the same inputs but no relevance column.
> sample_submission.csv: example finite retrieval scores for every test candidate.
> Column descriptions
> id: anonymized candidate identifier.
> conversation_id: retrieval-group identifier. Candidates are ranked only against candidates with the same value.
> explainer_group_id: anonymized explainer identifier. Use this for group-disjoint validation.
> context: a time-ordered text serialization of annotations ending during the 30 seconds before the candidate timestamp.
> speech_turns: count of explainer and explainee speech annotations in that interval.
> explainee_turns: count of explainee speech annotations.
> backchannels: count of short explainee feedback events.
> head_gestures: count of explainee head gestures.
> discourse_events: count of forward, backward, and dialogue-control annotations.
> gaze_events: count of explainer, explainee, and mutual-gaze annotations.
> deictic_gestures: count of explainer pointing gestures.
> context_words: whitespace-delimited token count of context.
> checkpoint_relevance: train-only relevance grade. 2 means both participants marked the candidate; 0 means exactly one participant marked it.
> The context field uses repeated blocks:
> [T-018] EXPLAINER: ... [T-006] EXPLAINEE: ... [T-004] BACKCHANNEL: ja [T-002] HEAD_GESTURE: nod_r
> T-018 means the annotation began 18 seconds before the candidate timestamp. Role labels identify the annotation source or type. Text and symbolic labels remain in their original time order.
> Evaluation
> Submissions are scored with Explainer-Balanced Checkpoint Retrieval. Within each conversation_id, candidates are ordered by descending checkpoint_score. Equal scores are resolved by ascending id.
> For relevance grades (r_i \in {0,2}) at ranked positions (i):
> DCG@5  = sum((2^r_i - 1) / log2(i + 1)) for i = 1..min(5, n)
> NDCG@5 = DCG@5 / ideal_DCG@5
> ideal_DCG@5 is the DCG of the same candidates sorted by true relevance. If a validation conversation contains no relevant candidate, its NDCG is 0.
> For Average Precision, grade 2 is relevant and grade 0 is not:
> AP = sum(precision_at_i * is_relevant_i) / number_of_relevant_candidates
> If a validation conversation contains no relevant candidate, its AP is 0.
> The conversation score is:
> conversation_score = 0.7  *NDCG@5 + 0.3*  AP
> Conversation scores are first averaged within each held-out explainer. Those explainer averages are then averaged equally. Scores range from 0 to 1; higher is better. No decision threshold is used.
> Submission
> The submission must contain:
> id: every test candidate identifier exactly once.
> checkpoint_score: any finite real number. Higher values rank earlier within a conversation.
> Example:
> id,checkpoint_score
> 0df725e91e62bc,-0.4182
> 81ac3505cef6a3,1.2079
> d0ce9b240d9e42,0.0364
> Requirements
> Include exactly the columns id and checkpoint_score.
> Include exactly one row for every test id.
> Scores must be finite numeric values.
> Rank candidates within each conversation_id.
> Train and infer on CPU within the platform runtime.
> Prohibited methods
> Do not use cached relevance labels or hard-coded test rankings.
> Do not match public contexts against the original released corpus to recover candidate identities or hidden relevance.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## AxiomSplice: Retrieved Proof-Graph Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75xn5kz7yp957ky2jk5v4f6x8bmbg8
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> AxiomSplice: Retrieved Proof-Graph Repair
> An AxiomSplice example is a scientific argument with one deliberate fracture.
> The conclusion is still visible and most of the proof graph remains intact, but
> one supporting fact has been removed, displaced by a decoy, or dropped from a
> multi-premise inference. Recovering the answer text is not the task. You must
> diagnose the fracture, retrieve the exact absent fact from a shared 11,752-fact
> bank, and reconstruct only the edge that makes the argument structurally whole.
> The prediction object is therefore a provenance-preserving graph splice, not a
> passage relevance judgment or a generated explanation. Each submitted row must
> name the damage mechanism, identify the evidence node, and state the repaired
> inference edge.
> Structural Difference: Minimal Graph Surgery
> AxiomSplice combines three decisions that are usually scored in isolation:
> fault localization by type, collection-level fact retrieval, and exact
> topological repair. Every example has exactly one deterministic fracture,
> applied only after source examples have been assigned to their public split:
> missing_premise: one premise reference is replaced by MISSING_FACT.
> decoy_premise: one valid premise reference is replaced by a plausible but incorrect corpus fact.
> dropped_operand: one premise reference is removed from an otherwise valid multi-premise edge.
> The target is the coupled triple (fault_type, retrieved_fact_id, repaired_edge). The final field is not free-form prose: it must be a complete
> proof edge grounded by the retrieved fact and connected to the correct companion
> premises, destination node, and conclusion text.
> Nearby task family	What AxiomSplice requires instead
> Passage or answer retrieval	Retrieve an atomic fact that is absent from the damaged proof and use it in a scored graph edit.
> Natural-language inference classification	Diagnose a concrete proof fracture and reconstruct its missing topology.
> Explanation generation	Return one canonical edge rather than an unconstrained rationale or an entire proof.
> Proof verification	Alter an invalid graph by the smallest source-grounded repair instead of only accepting or rejecting it.
> The required fact is never already cited in the corrupted test proof. Systems
> must search the supplied collection; rereading the damaged graph cannot reveal
> the missing identifier.
> Public Split
> The public data contains:
> train.csv: 1,479 labeled repair examples.
> test.csv: 358 repair examples without target columns.
> fact_corpus.csv: 11,752 normalized, deduplicated retrieval facts.
> sample_submission.csv: a schema-valid submission template with one row per test example.
> prepare.py reads one unified raw collection, removes normalized duplicate
> question-hypothesis pairs, assigns each remaining example by a deterministic
> fingerprint, and only then constructs its corruption. Upstream train, dev, and
> test labels are not used as challenge partitions. Normalized duplicate facts
> collapse to one fact ID.
> The test-to-train ratio is 358 / 1,479 = 24.2%, within the required 15% to
> 25% band.
> train.csv
> Column	Type	Description
> example_id	string	Opaque repair-example identifier.
> question	string	Scientific question that motivated the proof.
> hypothesis	string	Final claim supported by the undamaged proof.
> corrupted_proof	string	Semicolon-separated proof graph containing exactly one corruption.
> fault_type	string	One of missing_premise, decoy_premise, or dropped_operand.
> retrieved_fact_id	string	Correct premise ID from fact_corpus.csv.
> repaired_edge	string	Complete canonical edge after the correct fact is restored.
> test.csv
> test.csv contains example_id, question, hypothesis, and corrupted_proof.
> fact_corpus.csv
> Column	Type	Description
> fact_id	string	Opaque unique ID for one normalized fact.
> fact_text	string	Natural-language scientific fact available for retrieval.
> Proof Syntax
> Edges have the form:
> premise_a & premise_b -> int1: intermediate conclusion
> The final edge may target hypothesis. A proof is a semicolon-separated sequence of edges. Premise order is not meaningful; the grader sorts premise references before comparing repaired edges. Whitespace and letter case are also normalized. The edge must otherwise match exactly, including its target and intermediate-conclusion text.
> Submission Format
> Submit submission.csv with exactly these columns and one row for every example_id in test.csv:
> example_id,fault_type,retrieved_fact_id,repaired_edge
> AX_0123456789ABCDEF,missing_premise,F_0123456789AB,"F_0123456789AB & int1 -> hypothesis"
> AX_FEDCBA9876543210,decoy_premise,F_FEDCBA987654,"F_FEDCBA987654 & F_ABCDEF012345 -> int2: matter changes state when thermal energy is added"
> Use only the three documented fault_type values. retrieved_fact_id must be copied exactly from the corpus. Do not submit an entire proof in repaired_edge; submit only the repaired edge.
> Metric
> The score is:
> 0.15 * fault_type_accuracy
> + 0.35 * retrieved_fact_id_accuracy
> + 0.50 * canonical_repaired_edge_accuracy
> All three components use exact matching after the documented edge canonicalization. Scores range from 0 to 1, and higher is better.
> Metric Dependency
> repaired_edge necessarily contains the selected retrieved_fact_id. A wrong
> fact therefore normally loses both the 0.35 retrieved-fact component and the
> 0.50 grounded-edge component. Operationally, retrieving and correctly
> splicing the fact controls up to 0.85 of the score, while fault diagnosis is
> independently worth 0.15.
> This dependency is intentional: a proof cannot be repaired with a fact that
> was not retrieved. The edge component still tests whether that fact is inserted
> with the correct companion premises, target node, and intermediate conclusion.
> Multi-Run Reporting
> Stochastic systems must be evaluated with at least five independent runs. The
> reported capability score is the arithmetic mean across runs, never the best
> run. Reports must also include the sample standard deviation, minimum, maximum,
> and number of runs. Different runs must use independently selected seeds while
> keeping the dataset, metric, and system configuration fixed.
> Not Allowed Methods
> Matching test text against online copies, cached source records, source IDs, answer keys, or published proof files.
> Internet access, remote APIs, hosted search services, or external corpora during prediction.
> Manual labeling or per-example inspection of the test set for the purpose of writing answers.
> Reading grader internals, answer files, platform secrets, or any file not provided to participants.
> Hard-coding test identifiers, retrieved fact IDs, repaired edges, or source-to-target lookup tables.
> Pretrained models are allowed. Participants may train on train.csv and may build local lexical, dense, graph, or hybrid indexes using only the supplied public files.
> Submissions
> 34

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Role-Constrained Medical Device Incident Precedent Retrieval

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78dxgs8ea2aq34new1bn3t458c2bnc
- DOMAIN exactly as displayed: RAG
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
> Select four different precedents from a twenty-candidate incident catalog. Assign one precedent to each required role: mechanism match, harm match, remediation match, and boundary case.
> This models evidence retrieval during postmarket medical-device review. A safety reviewer rarely needs four copies of the nearest narrative. The useful portfolio separates distinct questions: which prior report best matches the technical failure, which best matches the patient consequence, which documents a comparable corrective action, and which shares the mechanism but reaches a different outcome that limits an overbroad conclusion.
> Every case contains one query packet and twenty shuffled candidate packets. Source words are converted to a stable 8,192-token collision vocabulary before publication, and direct report identifiers are removed. The four reference roles are derived from linked problem codes, event type, patient outcomes, remedial-action codes, and narrative overlap. Candidate IDs are randomized independently for every query.
> Every source report is assigned to exactly one split before queries, role witnesses, and distractors are constructed. A practical CPU solution can cache sparse or compact text representations, train four role-specific relevance functions, and solve the small no-reuse assignment for each packet. The 8,000 labeled retrieval packets are sized for the 10-core, 62 GB, 1.5-hour CPU limit, and no accelerator-only operation is required.
> Dataset
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | 8,000 labeled query-and-candidate packets. |
> | `test.csv` | 1,600 packets constructed only from held-out source reports. |
> | `sample_submission.csv` | One schema-valid fixed portfolio for every test case. |
> CSV Columns
> | Column | Data type | Availability | Description |
> |---|---|---|---|
> | `case_id` | string | train, test | Opaque row identifier used only for submission alignment. |
> | `query_packet` | token string | train, test | Collision-coded incident evidence for the report under review. |
> | `candidate_packet` | multiline token string | train, test | Twenty candidate incidents labeled `c00` through `c19`. |
> | `precedent_portfolio` | canonical role sequence | train only | Four different candidate IDs assigned to the four retrieval roles. |
> train.csv contains all four columns. test.csv contains case_id, query_packet, and candidate_packet only.
> Public Token Representation
> Tokens v0000 through v8191 are stable collision buckets derived from normalized source words. Numeric strings share a common normalized input before bucketing. Different words can map to the same public token, and the reverse source vocabulary is not supplied. This keeps repeated language learnable while preventing exact-phrase source lookup.
> The query has the form:
> query: v1032 v7710 v0194 v1032 v4821 ...
> The candidate catalog contains exactly twenty newline-separated records:
> c00: v6120 v1032 v4481 ...
> c01: v2290 v0612 v7710 ...
> ...
> c19: v0194 v3370 v4481 ...
> The complete query-and-candidate packet is unique within each split, and no complete packet occurs in both splits. Repeated fragments can occur because real surveillance narratives often use standard reporting language.
> Retrieval Roles
> | Role | Required evidence relationship |
> |---|---|
> | `mechanism` | Strong match to the query's coded device-problem evidence while downweighting candidates selected mainly by harm or remedy. |
> | `harm` | Strong match to event type or patient outcome while downweighting a merely identical technical mechanism. |
> | `remedy` | Comparable reported remediation, with mechanism-only matches downweighted. |
> | `boundary` | Similar technical mechanism but a different event outcome, useful as a boundary on causal interpretation. |
> The canonical role order is mechanism, harm, remedy, boundary. Each role uses a different candidate. Reference candidates are selected from authentic linked report evidence with deterministic role scoring and deterministic tie resolution.
> Target Grammar
> Tokens use <role>:<candidate_id> and are joined by > in canonical role order:
> mechanism:c12>harm:c04>remedy:c17>boundary:c02
> Candidate IDs range from c00 through c19. Reusing a candidate, omitting a role, changing role order in the serialized target, or adding a fifth token is invalid.
> Candidate-Position Balance
> Each role occupies all twenty candidate positions in both splits. In training, the count per role-position ranges from 351 to 461. In test, it ranges from 62 to 100. Candidate position is therefore not a useful shortcut.
> Submission Format
> Write the final file to ./working/submission.csv.
> It must contain exactly these columns in this order:
> | Column | Data type | Required content |
> |---|---|---|
> | `case_id` | string | One exact test identifier. |
> | `precedent_portfolio` | canonical string | Four role tokens using four distinct candidate IDs. |
> Example:
> | case_id | precedent_portfolio |
> |---|---|
> | `pp_62f6bc185c83d5df80ef` | `mechanism:c12>harm:c04>remedy:c17>boundary:c02` |
> Include exactly one row for every test ID. Extra columns, reordered columns, duplicate IDs, missing IDs, unknown IDs, blank IDs, and row-count mismatches reject the submission. One backend-managed visibility column is accepted and removed before schema validation. Portfolio strings longer than 71 characters or values that violate the grammar receive zero for all row-level components.
> Evaluation
> Submissions use the Incident Precedent Portfolio Score:
> Score = 0.55 * RolePositionScore + 0.20 * PortfolioCoverageScore + 0.25 * PortfolioExactScore
> For each row, parse the four hidden candidate IDs as Y[role] and the submitted IDs as P[role].
> RolePositionScore
> For hidden row r, let A[r] be the fraction of the four roles assigned their exact hidden candidate. Let A_raw be the mean of A[r] over all hidden rows. Randomly selecting one candidate for a fixed role has expectation 1/20 = 0.05. Chance correction removes this passive credit after hidden-set averaging:
> RolePositionScore = clip((A_raw - 0.05) / 0.95, 0, 1)
> No row is independently chance-corrected or clipped.
> PortfolioCoverageScore
> Ignore roles temporarily and compare the submitted set of four candidates with the hidden set of four:
> C[r] = size(hidden_set[r] intersection submitted_set[r]) / 4
> Let C_raw be the mean of C[r] over all hidden rows. A uniformly selected four-candidate set has expected overlap fraction 4/20 = 0.20. Therefore:
> PortfolioCoverageScore = clip((C_raw - 0.20) / 0.80, 0, 1)
> Chance correction is applied once, after hidden-set averaging.
> PortfolioExactScore
> exact_row is 1 only when all four role assignments are correct and is 0 otherwise. PortfolioExactScore is the mean over all test cases.
> Minimum score: 0.0.
> Maximum score: 1.0.
> Higher is better. Exact hidden answers score 1.0.
> What Makes This Interesting
> Standard retrieval rewards several near-duplicate neighbors. This benchmark asks for a deliberately heterogeneous evidence portfolio whose members play noninterchangeable roles. It combines role-conditioned retrieval, hard-negative discrimination, and a no-reuse assignment constraint in one prediction.
> The boundary role is especially important. It rewards evidence that is technically similar but outcome-divergent, which is often what prevents unsafe generalization in real postmarket review. The task is not diagnosis and does not ask the model to infer causality.
> What Not To Use
> Do not use case_id, row order, CSV order, token-string length, candidate position, hashes, or split artifacts as predictors.
> Do not identify reports through external databases, narrative fingerprints, source mirrors, product-code lookup, or report-key reconstruction.
> Do not build source-record, filename, device-family, or hash lookup tables for test inference.
> Do not exploit repeated narrative fragments, malformed CSVs, parser behavior, or leaderboard feedback to infer hidden portfolios.
> Do not tune on withheld test answers or perform test-time adaptation through repeated submissions.
> Hosted or closed-model APIs are not allowed at inference time. Local open-weight models are allowed.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Government Report Evidence Retrieval and Confidence Challenge

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77gnp5np6v9sbsgyzs74y2xs8c5wk6
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat pvduy's score of 0.739!

Full challenge description from page:

> Leaderboard
> (15)
> Your Submissions
> TraceCal-Gov: Selective Reliability over Hierarchical Government Reports
> Overview
> TraceCal-Gov is a zero-label benchmark for selective, evidence-grounded retrieval over long government reports. For every private question, a system must make one auditable decision with three linked outputs: a concise answer, a ranked list of supporting report sections, and the probability that both the answer and its provenance are reliable.
> The central research question is not merely whether a model can recover a fact. It is whether a pretrained system, given no task-specific labeled examples, can search a fixed collection of long hierarchical documents, cite the correct source at the required granularity, and recognize which of its own answer-citation pairs should be trusted.
> The source collection is the GovReport-QS dataset card (CC BY 4.0): 1,714 English-language U.S. government reports with explicit section hierarchies. Its original split contains 1,371 training reports, 171 validation reports, and 172 test reports. TraceCal-Gov releases all 1,714 reports as the immutable search corpus, uses only the 172 original test reports as sources for private questions, and retains the other 1,542 reports as realistic retrieval distractors.
> The 3,000 private questions and short-answer/evidence labels are newly constructed for this benchmark; no GovReport-QS question-summary pair is reused as a test item. Candidate answers were extracted as unique spans from held-out sections. Questions were generated from those spans, filtered for ambiguity, answer leakage, duplicates, and overlap with upstream questions, and checked by an independent round-trip QA model. The final set covers entities, years, money, dates, percentages, durations, and quantities.
> There is no public train or development question set and no public answer, evidence, confidence, or answer-type label. This is a deliberate cold-start evaluation regime rather than a missing-data convenience: it prevents tuning on task examples, fixes the universe of admissible evidence, makes unsupported citations falsifiable, and tests whether retrieval, reading, provenance, and self-assessment transfer together.
> Prior-work boundary
> TraceCal-Gov reuses a public document collection, but it does not reuse the upstream learning task or evaluation protocol. The benchmark layer—private questions, short answers, section-level evidence targets, overlapping retrieval passages, confidence target, and joint scoring harness—is new.
> | Benchmark | Participant supervision | Document and evidence regime | Reliability target |
> |---|---|---|---|
> | GovReport-QS | Public hierarchical question-summary annotations | Long U.S. government reports; designed for hierarchical question-summary generation | No submitted probability for answer-plus-citation correctness |
> | HotpotQA | 113k labeled Wikipedia QA pairs with public training data | Multi-document Wikipedia reasoning with sentence-level supporting facts | Answer and supporting-fact evaluation, without a chance-corrected confidence component |
> | TraceCal-Gov | No public QA labels or development questions | Closed collection of long hierarchical reports; passage retrieval but parent-section citation | Probability that answer F1 reaches 0.8 and a gold section is ranked in the top three, scored against a no-skill reference |
> The distinction matters operationally. HotpotQA primarily measures supervised multi-hop answer production with sentence-level explanations. GovReport-QS supplies hierarchical question-summary annotations. TraceCal-Gov instead measures cold-start selective reliability: a system must resolve evidence across long reports, translate passage retrieval into stable section citations, produce a short factual answer, and assign useful confidence to the coupled answer-and-provenance event. Neither of the two closest resources evaluates this combination as a single closed-corpus protocol.
> Dataset
> The released corpus contains 65,696 overlapping passages from 43,767 sections. Search operates over passages, but citation scoring operates over sections. Multiple passage_id values can therefore share one parent section_id. Systems must submit section IDs as evidence; passage IDs are invalid evidence predictions.
> corpus.jsonl
> Each JSON line contains one searchable passage:
> | Field | Type | Meaning |
> |---|---|---|
> | passage_id | string | Unique retrieval-passage identifier |
> | section_id | string | Parent-section identifier used for evidence scoring |
> | document_id | string | Source-report identifier |
> | document_title | string | Title of the government report |
> | section_path | list[string] | Ordered hierarchy of headings leading to the section |
> | section_depth | integer | Depth of the section in the report hierarchy |
> | chunk_index | integer | Zero-based passage position inside its section |
> | text | string | Passage content available for retrieval and answering |
> test.csv
> | Field | Type | Meaning |
> |---|---|---|
> | query_id | string | Unique question identifier and submission join key |
> | question | string | English question to answer from the corpus |
> The test file contains 3,000 rows and does not include labels.
> sample_submission.csv
> | Field | Type | Meaning |
> |---|---|---|
> | query_id | string | Must cover every test identifier exactly once |
> | answer | string | Concise predicted answer |
> | evidence_ids | string | Ranked list of at most eight unique section IDs joined with | |
> | confidence | float | Value in [0,1] estimating that the answer is correct and grounded by a gold section in the top three submitted evidence IDs |
> Evaluation
> The score is a joint reliability contract rather than a collection of interchangeable metrics. Answer credit measures factual recovery, evidence credit measures whether the claim can be traced to the right report section, and confidence credit measures whether the system can distinguish dependable answer-citation pairs from failures. A system cannot maximize the benchmark by optimizing only retrieval, only generation, or only uncertainty. Higher is better.
> Answer-type macro F1 — 45%
> Answer text uses case-insensitive multiset token F1 after Unicode normalization. Scores are first averaged within each hidden answer-type group—entity, year, money, date, percentage, duration, and quantity—and then macro-averaged across the seven groups. This prevents the more frequent entity questions from dominating evaluation.
> Evidence reciprocal rank — 35%
> The first submitted gold section_id receives 1/rank. A question receives zero evidence credit when no gold section occurs within the submitted list. Ranking the decisive section first therefore matters.
> Chance-corrected grounded-confidence skill — 20%
> A prediction is labeled correct-and-grounded when answer F1 is at least 0.8 and a gold section appears among its top three evidence IDs. Submitted confidence is evaluated against this binary event with a chance-corrected Brier Skill Score.
> For one submission, let BS be its mean squared Brier error, let r be its observed correct-and-grounded rate, and let BS_ref be the Brier error of the constant forecast r. This follows the standard Brier Skill Score reference-forecast construction: score improvement relative to a constant climatology-like forecast rather than raw Brier accuracy without a reference. The component is:
> calibration_skill = max(0, min(1, 1 - BS / BS_ref))
> The constant base-rate forecast therefore receives zero skill, so low confidence on uniformly incorrect answers cannot earn a free score. If BS_ref is zero because every outcome is negative, calibration skill is zero. If every outcome is positive, the component uses clipped 1 - BS; this preserves a maximum score of one for a genuinely perfect system and removes any incentive to deliberately spoil an answer. In the ordinary mixed-outcome case, confidence earns credit only when it distinguishes more reliable predictions from less reliable ones better than the no-skill reference.
> The grader returns:
> 0.45 macro_answer_F1 + 0.35 evidence_MRR + 0.20 * calibration_skill
> The grader clips negative Brier skill to zero and clamps the final result to [0,1]. Configure the challenge with minimum score 0 and maximum score 1.
> Submission
> Submit one CSV row for every query_id:
> query_id,answer,evidence_ids,confidence
> Q_2c935ad449c9a381,example answer,SEC_a|SEC_b,0.82
> Include every test ID exactly once and add no extra IDs.
> Separate ranked evidence IDs with | and submit no more than eight distinct IDs.
> Use only identifiers beginning with SEC_; never submit a passage_id.
> Set confidence to a numeric value from 0 to 1.
> Represent a missing answer or evidence prediction with an empty string.
> Keep each answer at no more than 1,000 characters and each evidence ID at no more than 128 characters.
> Compute Environment
> Solutions run on 10 CPU cores with 62.5 GiB RAM and no GPU. Pretrained models are allowed, but the complete inference pipeline must fit this CPU environment. Cache corpus representations, batch inference, and restrict expensive reranking to a compact candidate set.
> Integrity Rules
> Produce test predictions programmatically and reproducibly.
> Do not manually research or label individual test questions.
> Do not use leaked private labels or organizer artifacts.
> Pretrained models and public external resources are permitted unless platform-wide rules state otherwise.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Multi-Hop Science Fact Retrieval and Reasoning

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a12mxr6dkqjyj96w31pgqf98c53j0
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat duongnguyen's score of 0.878!

Full challenge description from page:

> Leaderboard
> (16)
> Your Submissions
> Two-Fact Bridge Map
> 1. Overview
> Two-Fact Bridge Map is a retrieval and structured-reasoning challenge based on QASC (Question Answering via Sentence Composition), a dataset of eight-way multiple-choice questions about grade-school science. The questions cover topics such as biology, Earth science, physics, chemistry, energy, weather, and the environment. QASC was created by the Allen Institute for AI and is distributed under CC BY 4.0.
> Each question is answerable by composing two science facts. Your task is to predict all three parts of that proof:
> the correct multiple-choice answer label;
> the two supporting fact IDs in the correct order; and
> the lexical bridge terms shared by the supporting facts.
> For example, a question about clouds may require one fact stating that clouds contain water vapor and another stating that water vapor condenses into droplets. The shared concept connects the two facts into a proof chain. Predicting only the answer is not sufficient for a competitive score.
> This hard version supplies 64-72 candidate facts per question. The distractors are selected because they overlap with the question, correct and incorrect answer choices, one or both gold facts, or likely bridge vocabulary. Candidate lists therefore contain plausible but incomplete and misleading chains.
> 2. Prediction target
> For every row in test.csv, return one JSON object with exactly three fields:
> {"answer":"F","facts":["f_first","f_second"],"bridge":["water","vapor"]}
> answer is the label of the selected answer choice.
> facts contains exactly two distinct fact IDs. Order matters: the first value predicts the source fact1 and the second predicts the source fact2.
> bridge contains the canonical lexical bridge between the predicted gold facts. It may be an empty array when the gold facts have no shared content token under the canonical rules below.
> 3. Dataset files
> The prepared public dataset contains exactly three files:
> | File | Format | Purpose |
> |---|---|---|
> | train.csv | CSV | Labeled examples for training and validation. |
> | test.csv | CSV | Unlabeled examples for which predictions must be submitted. |
> | sample_submission.csv | CSV | A schema example with deliberately weak predictions. |
> 3.1 train.csv columns
> | Column | Data type | Description |
> |---|---|---|
> | id | string | Unique opaque row identifier. |
> | question | string | Natural-language grade-school science question. |
> | choices_json | JSON-encoded array | Ordered objects with string fields label and text, for example [{"label":"A","text":"heat"}, ...]. |
> | candidate_facts_json | JSON-encoded array of objects | The 64-72 distinct candidate facts. Each object has a string fact_id and string text. Both gold facts are included. |
> | label | JSON-encoded object | Gold target containing answer, ordered facts, and bridge in exactly the same structure required for predictions. |
> 3.2 test.csv columns
> test.csv contains id, question, choices_json, and candidate_facts_json with the same types and meanings as in train.csv. It does not contain label.
> 3.3 Candidate-fact object fields
> | Field | Data type | Description |
> |---|---|---|
> | fact_id | string | Unique opaque identifier referenced by labels and predictions. |
> | text | string | Science evidence sentence used for retrieval and reasoning. |
> Fact IDs contain no semantic information. Models should reason over each embedded text value and return its associated fact_id.
> 3.4 sample_submission.csv columns
> | Column | Data type | Description |
> |---|---|---|
> | id | string | Test ID copied exactly from test.csv. |
> | prediction | JSON-encoded object | Predicted answer, ordered facts, and bridge. |
> The sample demonstrates file syntax only and should not be treated as a useful baseline.
> 4. Canonical bridge rules
> The target bridge is computed deterministically from the two gold fact texts:
> Tokenize each fact with the case-insensitive regular expression [a-z0-9]+(?:'[a-z0-9]+)?.
> Convert tokens to lowercase.
> Remove the following fixed stopwords:
> a an and are as at be been being by can could did do does for from had has
> have how i if in into is it its may more most not of on or our should than
> that the their then there these they this those through to was were what
> when where which who why will with would you your
> Keep tokens that occur in both facts.
> Remove repeated bridge tokens while preserving their first-occurrence order in the first fact.
> No stemming, lemmatization, synonym expansion, external lexicon, or semantic matching is used. During grading, submitted bridge strings are trimmed and compared case-insensitively.
> 5. Submission format
> Upload a UTF-8 CSV file named submission.csv with exactly these two columns in this order:
> id,prediction
> Example:
> id,prediction
> q_example,"{""answer"":""F"",""facts"":[""f_first"",""f_second""],""bridge"":[""water"",""vapor""]}"
> Submission requirements:
> Include every test ID exactly once.
> Do not include missing, duplicate, or unknown IDs.
> Do not add columns.
> prediction must be valid JSON with exactly answer, facts, and bridge; extra keys are invalid.
> answer must be one alphabetic character. It is uppercased before comparison.
> facts must contain exactly two distinct, nonempty strings.
> bridge must contain at most 12 distinct, nonempty strings, each no longer than 64 characters.
> Duplicate bridge values after trimming and case-folding are invalid.
> A file-level column, row-count, or ID-set error gives the entire submission a score of 0.0. Malformed or schema-invalid JSON gives only the affected row a score of zero.
> 6. Evaluation metric
> Let the prediction for one row be (a_p, [p_1,p_2], B_p) and the gold target be (a_g, [g_1,g_2], B_g). Let I(condition) equal 1 when the condition is true and 0 otherwise.
> ### 6.1 Answer accuracy
> A = I(uppercase(a_p) = uppercase(a_g))
> ### 6.2 Ordered-fact accuracy
> O = (I(p_1 = g_1) + I(p_2 = g_2)) / 2
> Thus `O` is `0`, `0.5`, or `1`. Reversing both gold facts gives `O = 0` because neither ordered position is correct.
> ### 6.3 Evidence-set F1
> Treat the two predicted facts and two gold facts as sets `P` and `G`:
> E = 2 * |P intersection G| / (|P| + |G|)
> Since valid predictions contain two distinct fact IDs and gold targets also contain two, `E` is `0`, `0.5`, or `1`. Fact order does not affect this component.
> ### 6.4 Bridge multiset F1
> After trimming and lowercasing bridge strings, let `count_p(t)` and `count_g(t)` be the multiplicities of term `t`:
> M = sum over t of min(count_p(t), count_g(t))
> B = 2 * M / (|B_p| + |B_g|)
> If both bridge arrays are empty, `B = 1`. If exactly one is empty, `B = 0`.
> ### 6.5 Exact joint chain
> J = I(A = 1 and O = 1 and B = 1)
> The joint component requires the answer, both ordered fact positions, and the complete bridge to be exact.
> ### 6.6 Weighted sum and mandatory cap
> First calculate:
> R_raw = 0.10A + 0.25O + 0.10E + 0.10B + 0.45*J
> Then apply the joint-chain cap:
> R = R_raw if J = 1
> R = min(R_raw, 0.49) if J = 0
> The cap **overrides the weighted sum** whenever the joint chain is not exact. Component weights do not permit a non-exact row to score `0.50` or higher. An answer-only prediction can earn at most `0.10` from the answer component. A perfect row has `A=O=E=B=J=1` and scores exactly `1.0`.
> The final leaderboard score is the arithmetic mean over all hidden rows:
> Leaderboard score = (1 / N) * sum from i=1 to N of R_i
> ## 7. Split construction and leakage control
> The packaged QASC training and validation records are combined before creating a new deterministic train/test split. Records are connected when they share either a normalized question or the same unordered normalized gold fact pair. Each connected component is assigned wholly to train or test. This prevents normalized duplicate questions and repeated proof pairs from appearing across both partitions.
> Opaque IDs are generated deterministically and must not be interpreted or mapped back to upstream row identifiers.
> ## 8. Resource and usage constraints
> The complete submitted solution, including training and test inference, must finish within 90 minutes using at most 10 CPU cores and 62 GB RAM.
> The following are prohibited:
> - network access or external search engines;
> - external corpora or evidence banks;
> - remote embedding or language-model APIs;
> - upstream QASC row-ID lookup;
> - installing packages during execution;
> - solutions that require a GPU; and
> - manually encoded test-answer tables.
> Use only the supplied challenge files and packages already available in the execution environment.
> ## 9. Practical modeling direction
> A competitive CPU system can combine sparse question-to-fact retrieval, answer-aware hard-negative reranking, pairwise fact compatibility, bridge prediction, and constrained joint decoding over `(answer, fact1, fact2, bridge)`. Independent top-two retrieval or answer-only classification is intentionally insufficient.
> &nbsp;

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Support Boundary Recovery From Confusable Contract Evidence

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74d4t57hp39hx0s060ygcrfh8atyx1
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat laddulal's score of 0.671!

Full challenge description from page:

> Leaderboard
> (17)
> Your Submissions
> Overview
> Document-grounded systems must distinguish genuine support from evidence that is merely tempting. A useful audit therefore needs both a positive certificate and a counterfactual boundary witness: the segment that most strongly resembles support for an unsupported query but still fails to establish its missing fact.
> Each case contains two query cards, twelve shuffled evidence segments, and eight candidate answer spans from one commercial agreement. Exactly one query is supported by one answer candidate in one evidence segment. The other query asks for a plausible detail certified absent from the supplied text. One source-certified absence-context segment is designated as the boundary confuser because it has the greatest normalized token-set similarity to the unsupported query before private transformation. Ties are resolved deterministically. All local IDs are independently reassigned in every case.
> Natural-language words use a case-local private vocabulary. Query, evidence, and answer observations are independently thinned, shuffled, and padded to fixed field-specific sizes with indistinguishable synthetic features. Tokens remain comparable inside a case, but source order, source length, full strings, and dataset-wide word identities are not exposed.
> Your task is to identify the answerable query, select its answer span, attach the supporting evidence segment, and localize the boundary confuser for the unsupported twin. Train and test are disjoint by agreement group.
> Dataset
> The public files are:
> train.csv: query packets, evidence packets, and gold dual-boundary certificates.
> test.csv: query and evidence packets without targets.
> sample_submission.csv: valid example predictions.
> train.csv Columns
> case_id (string): anonymous case identifier.
> query_cards (JSON string): two objects containing query_id and question.
> evidence_packet (JSON string): twelve objects containing evidence_id and text.
> answer_candidates (JSON string): eight objects containing answer_id and candidate text.
> target_query_id (string): the answerable query ID, either Q0 or Q1.
> target_answer_id (string): supported answer candidate ID from A00 through A07.
> target_evidence_id (string): supporting evidence ID from E00 through E11.
> target_confuser_evidence_id (string): strongest certified-absence confuser ID from E00 through E11.
> test.csv Columns
> case_id (string)
> query_cards (JSON string)
> evidence_packet (JSON string)
> answer_candidates (JSON string)
> sample_submission.csv Columns
> case_id (string)
> pred_query_id (string)
> pred_answer_id (string)
> pred_evidence_id (string)
> pred_confuser_evidence_id (string)
> The prepared dataset contains two independently shuffled variants per certified document pair. Variants from the same agreement always remain in the same partition.
> Evaluation
> Higher scores are better, and the score is bounded in [0, 1].
> Score = 0.12 * QueryChoiceAccuracy + 0.13 * AnswerChoiceAccuracy + 0.20 * SupportEvidenceAccuracy + 0.20 * ConfuserEvidenceAccuracy + 0.35 * ExactDualCertificateAccuracy
> QueryChoiceAccuracy
> The fraction of cases where pred_query_id identifies the answerable query.
> AnswerChoiceAccuracy
> The fraction of cases where pred_answer_id identifies the supported answer span.
> SupportEvidenceAccuracy
> The fraction of cases where pred_evidence_id exactly identifies the supporting segment.
> ConfuserEvidenceAccuracy
> The fraction of cases where pred_confuser_evidence_id identifies the designated boundary confuser. The confuser is selected only from the source-certified absence context and cannot be the supporting segment.
> ExactDualCertificateAccuracy
> The fraction of cases where the query ID, answer candidate ID, supporting evidence ID, and confuser evidence ID are all exactly correct.
> The five displayed terms are the complete metric. There are no private track weights.
> Submission
> Submit exactly five columns: case_id, pred_query_id, pred_answer_id, pred_evidence_id, and pred_confuser_evidence_id.
> Example:
> case_id,pred_query_id,pred_answer_id,pred_evidence_id,pred_confuser_evidence_id
> SUP_12ab34cd56ef78,Q1,A04,E07,E02
> SUP_98fe76dc54ba32,Q0,A01,E02,E09
> Every test ID must appear exactly once. Missing IDs, unknown IDs, duplicate IDs, and extra columns raise an error. An invalid query, answer, support-evidence, or confuser-evidence code makes all metric components zero for that row rather than terminating grading.
> Allowed And Prohibited Methods
> Allowed methods:
> CPU-compatible sparse retrieval, lexical entailment models, compact encoders, extractive QA models, and constrained pipelines.
> Training only with the supplied public data.
> Deterministic normalization and output validation.
> Prohibited methods:
> Looking up agreements, questions, or answer spans in external corpora, or reverse-engineering the private vocabulary.
> Hardcoded test answers, source-document maps, or manually encoded evidence IDs.
> Using row order, case IDs, query order, or segment order as answer shortcuts.
> A non-ML external matching system that recovers source answers.
> Solutions must train and run within 1.5 hours using 10 CPU cores and 62 GB of RAM.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Cross-Lingual Constitutional Passage Retrieval

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx727qvcq5jdyeyg14hmqvg7258c5tck
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top score: 0.742

Full challenge description from page:

> Overview
> Each item is a Bangla-language question about the Constitution of Bangladesh, and your task is cross-lingual passage retrieval: rank a corpus of English constitutional passages by how well each one answers the question, and return the top 10 doc ids ranked from most to least relevant.
> The corpus (corpus.csv) contains ~3,000 English constitutional passages — the full set of answers that appear anywhere in the source. Training pairs (train.csv) give you Bangla questions with their known correct doc id, so you can learn the cross-lingual alignment from the data alone.
> Data
> train.csv, test.csv, corpus.csv, and sample_submission.csv are UTF-8 CSV with a header.
> corpus.csv
> Columns doc_id, passage.
> doc_id is a string like A0001, A0002, ..., A3179. There are roughly 3,000 passages in total (exact count depends on deduplication during the build).
> passage is the English constitutional statement itself.
> Training
> train.csv — columns item_id, question_bn, true_doc_id.
> question_bn is the Bangla question.
> true_doc_id is the corpus doc id that is the correct answer to the question.
> Test
> test.csv — columns item_id, question_bn.
> Same schema as training but with the true_doc_id column removed.
> sample_submission.csv
> A weak baseline that returns the same fixed top-10 doc ids for every test query. It scores near zero because it ignores the query entirely.
> metadata.json
> Keys task, columns, submission_columns, submission_note, metric, files. Informational.
> Task
> For each test query, return a comma-separated list of exactly 10 distinct doc ids from the corpus, ranked from most relevant (position 1) to least relevant (position 10).
> Evaluation
> Score in [0, 1], higher is better. For each test query:
> Let rank = the 1-indexed position of the true doc id in the predicted top-10.
> If the true doc id appears in the top-10, RR = 1 / rank; otherwise RR = 0.
> The final score is the Mean Reciprocal Rank at 10 (MRR@10) across the test queries: the mean of the per-query RR values.
> The random-permutation floor is roughly 0.003 (10 slots out of ~3,000); a naive character n-gram TF-IDF baseline stays near zero because Bangla and English do not share vocabulary; a well-tuned cross-lingual ranker trained on the provided pairs can reach above 0.3. The ceiling is 1.0.
> Submission format
> A UTF-8 CSV with a header and exactly these columns, in order:
> item_id,predicted_ranking
> item_id — string; a test item id.
> predicted_ranking — string; a comma-separated list of exactly 10 distinct corpus doc ids, in descending order of predicted relevance.
> Example
> For a test set with two queries, a valid submission looks like:
> item_id,predicted_ranking
> q_a1b2c3d4e5f6a1,A0421,A0155,A2903,A0088,A1244,A0055,A2011,A1600,A3170,A0002
> q_a1b2c3d4e5f6a2,A0088,A0421,A0002,A3170,A1600,A2903,A2011,A0155,A1244,A0055
> Notes on the example:
> Every test item_id from test.csv must appear exactly once (missing rows are rejected).
> Duplicate item_id rows are rejected.
> predicted_ranking must contain exactly 10 distinct corpus doc ids; malformed rankings score 0 for that item but are not rejected.
> Requirements (violations rejected as invalid): exactly the columns above; no null item_id; no duplicate item_id; only known test item_ids; every test item_id must appear.
> Allowed
> Any classical or neural cross-lingual retrieval approach fitted on the provided data.
> Character n-gram TF-IDF, cross-lingual embedding models trained from scratch on the parallel training pairs, small MLPs mapping Bangla feature vectors to English feature vectors, or learning-to-rank models using both signals.
> Solutions must run on the provided CPU environment within the platform time budget.
> What Not To Use
> No external Bangla-English bilingual embedding models or translation dictionaries. The task tests whether a solver can learn the cross-lingual alignment from ~2,500 parallel pairs; downloading a pretrained bilingual model sidesteps the challenge.
> No network access at run time.
> No hardcoded per-item_id predictions, no row-order shortcuts, no use of any answer file.
> No GPU or CUDA execution — solutions must remain within the CPU budget.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## EffectiveKnot: Regulatory Correction Instruction Grounding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70kjdv99m1p567v690p00bpd8drynr
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top score: 0.892

Full challenge description from page:

> EffectiveKnot: Regulatory Correction Instruction Grounding
> Overview
> The Electronic Code of Federal Regulations (eCFR) is continuously maintained. When an editorial or publishing error is discovered, the correction record states an operation such as revising a paragraph, restoring text, removing an authority citation, correcting a heading, or redesignating a structural unit. These instructions are compact, but their meaning depends on several coupled details: the action verb, the kind of unit being changed, and the locator of that unit inside the regulation.
> This challenge uses complementary evidence views. The query masks the action, locator, and unit simultaneously. Each of 24 candidate views preserves exactly one of those slot types while masking the other two, all numbers, and additional semantic terms. The preserved slot type is fixed per source correction and declared in the context. Exactly one candidate comes from the source instruction, but no public table exposes its complete text or labels.
> Select the official instruction that fits the masked residue and corrected section, then submit its action family, target locator, affected unit, and canonical operation sequence.
> This is an evidence-grounding task rather than historical state reconstruction. The data does not contain the complete erroneous pre-correction section, so the challenge does not claim that a participant can derive the edit by diffing before and after text. The candidate instruction, residue, hierarchy, and corrected section together define the supported decision.
> Prediction Objective
> For every row in test.csv, predict five fields:
> action_id: the opaque ID of the matching instruction among the 24 candidates.
> action_family: the canonical operation family derived from that instruction.
> target_locator: the first explicit paragraph locator, or a unit-level fallback when no paragraph locator is present.
> affected_unit: the structural kind affected by the instruction.
> operation_sequence_json: the ordered JSON array [affected_unit, target_locator, action_family].
> The last four fields are not independent free-form descriptions. They form a typed representation of the selected correction instruction. A submission should therefore select an instruction and emit a mutually consistent program.
> Public Evidence
> section_context has two labelled parts:
> correction view: contains the source instruction with all action, locator, unit, and numeric slots masked, plus deterministic semantic masking.
> corrected section: contains the official section text retrieved for the frozen source snapshot. Numbers and a deterministic subset of long words are masked. The same source correction receives the same context in all candidate-pool scenarios.
> The residue preserves surrounding drafting language. For example, connective phrases, the number of coordinated operations, and unmasked anchors may distinguish a heading correction from a paragraph redesignation even when the direct label words are absent.
> candidate_actions_json contains exactly 24 objects with an opaque action_id and a partially masked instruction view. Candidate views preserve only the slot type named by hidden slot; the other structural slots and selected semantic terms are hidden. Distractors preferentially share the gold family and unit. Candidate order has no meaning.
> Because the two sides use different masking policies, replaying one mask over public full text cannot recover the answer. Solvers must align surviving fragments, use corrected-section and hierarchy evidence, select a candidate, and combine the complementary views to reconstruct the program.
> Canonical Label Rules
> Labels are constructed deterministically from the official corrective_action field.
> Action Family
> The allowed values are:
> Label	Construction rule
> remove	The instruction contains removed, deleted, or reserved language.
> redesignate	The instruction contains a redesignation form.
> add	The instruction contains added, inserted, reinstated, or restored language.
> revise	All remaining retained correction instructions.
> Precedence is remove, redesignate, add, then revise.
> Affected Unit
> The allowed values are authority, heading, table, paragraph, and section. Authority, heading, and table terms take precedence. An explicit parenthesized locator implies paragraph; otherwise the fallback is section.
> Target Locator
> The target is the first contiguous parenthesized locator, such as (b) or (g)(1)(i). If no locator is present, the target is the affected-unit label. The challenge does not attempt to split one source instruction into several atomic edits.
> Dataset And Split
> Preparation uses 96 frozen correction records and generates three candidate-pool scenarios per record. After deterministic deduplication, it produces 231 training rows and 57 test rows. The public action corpus contains 92 distinct normalized instructions.
> Complete CFR titles are assigned to exactly one split before masking, candidate selection, and scenario creation. All corrections and all scenario siblings from a title remain together. This blocks direct reuse of title-specific corrections or section text across train and test.
> All three scenarios for one correction use the identical correction residue and identical corrected-section mask. Only distractor selection and candidate order vary. Comparing sibling rows therefore cannot reconstruct complementary masked tokens. General federal drafting conventions remain shared across titles because transfer across those conventions is the intended learning problem.
> The title-level split does not make the records statistically independent. Agencies can use similar correction language across titles, and some generic instruction patterns recur. Results should be interpreted as performance on unseen CFR titles within this collection, not all regulatory publishing systems.
> Public Files
> File	Rows	Purpose
> train.csv	231	Six public inputs followed by all five targets.
> test.csv	57	The same six public inputs with targets withheld.
> action_corpus.csv	92	Opaque IDs with fully masked shapes, token counts, and clause counts. It contains no target labels or complete instructions.
> sample_submission.csv	57	A complete, nonblank six-column lexical baseline with the exact submission schema.
> Private answers.csv contains only example_id and the five target columns. No target column occurs in test.csv.
> Input Columns
> Column	Type	Meaning
> example_id	string	Opaque identifier beginning EK_.
> section_context	string	Masked correction residue followed by masked corrected-section text.
> hierarchy_shape_json	JSON object	Presence/missing map for subtitle, chapter, subchapter, part, subpart, and section hierarchy levels.
> date_gap_days	integer	Calendar days between the recorded error and correction dates.
> candidate_actions_json	JSON array	Exactly 24 objects containing action_id and a complementary masked instruction view.
> operation_vocabulary_json	JSON array	Allowed action families: add, redesignate, remove, and revise.
> Evaluation
> Scores range from 0 to 1, and higher is better. Each structurally valid row receives:
> 0.45 * action selection accuracy
> 0.12 * action-family accuracy
> 0.12 * target-locator accuracy
> 0.11 * affected-unit accuracy
> 0.20 * exact coherent operation-sequence accuracy
> The five weights sum to 1.00; the leaderboard score is the mean row score.
> Before receiving component credit, a row must contain a syntactically valid opaque action ID, an allowed family and unit, and a three-string sequence exactly equal to [affected_unit, target_locator, action_family]. Invalid or contradictory rows receive zero. Retrieval now carries 45%, so generic label prediction cannot approach a strong score without grounding the correct candidate.
> The components intentionally separate retrieval from structured interpretation. Selecting the correct action_id without emitting its program receives partial credit; emitting correct generic labels without grounding the exact instruction cannot receive retrieval or joint credit.
> A wrong global schema, empty submission, missing or extra ID, or duplicate ID scores 0. A malformed JSON sequence loses the sequence, coherence, and joint components for its row. Exact private answers score 1.0. The evaluator is deterministic.
> Submission Format
> Submit exactly these columns in this order:
> example_id,action_id,action_family,target_locator,affected_unit,operation_sequence_json
> EK_0123456789ABCDEF,AC_1111111111111111,revise,(b),paragraph,"[""paragraph"",""(b)"",""revise""]"
> Start from sample_submission.csv. Submit one row for every test identifier and do not add public input columns.
> Not Allowed Methods
> External eCFR, Federal Register, search-engine, or regulatory-database queries during training or inference.
> Recovering masked CFR titles, section numbers, citations, correction IDs, or source URLs.
> Pretrained language models, pretrained embeddings, or learned tokenizers obtained outside the supplied data.
> Manual test labelling, hard-coded test answers, private-answer access, grader inspection, or repeated leaderboard probing.
> Randomly initialized local models, n-gram systems, retrieval indexes, parsers, and deterministic algorithms trained or constructed only from the supplied public files are allowed.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Czech Poetry Cross-Witness Passage Retrieval and Attested Reading Selection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75rn2ye6gbxg5vk3y01t6yex8ar2kb
- DOMAIN exactly as displayed: RAG
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.437

Full challenge description from page:

> Overview and Objective
>
> Czech-language poems often survive in several historical versions from manuscripts, books, and periodicals. Literary editors transcribed the poem lines and mapped corresponding lines across versions. Editors call each version a witness; here that simply means one recorded textual version of the same poem. The benchmark turns those editorial line mappings into simulated missing-line cases, not claims of physical damage to the sources.
>
> You are predicting (1) which segment ID in each of the five reference witnesses corresponds to the missing query line, and (2) the token-ID sequence representing the authentic wording of the missing query line itself.
>
> Each case shows the context around one missing Czech poem line and five groups of candidate passages, one group for each historical textual version. Choose the candidate passage that matches the missing line in each of the five versions, then choose the omitted query witness's authentic recorded wording from the center lines of those matched passages. The submission represents the first output as five segment IDs and the second as ordered token IDs.
>
> This is an extractive historical-text matching task. The reading is a finite candidate selection, not free-form text generation: a non-empty prediction is legal only when it exactly equals a candidate-center sequence supplied in the case. The correct reading is attested in at least one aligned reference; it is never generated by combining unattested fragments.
>
> Preparation converts the transcribed tokens to globally stable opaque IDs and removes provenance fields. These transformations define the benchmark representation but are not claimed to prevent reconstruction; external source lookup is prohibited by the rules.
>
> Dataset
>
> The public files are:
>
> train.jsonl: 940 training cases with public answer objects.
> validation.jsonl: 252 validation cases with public answer objects.
> test.jsonl: 388 test cases without answer objects or direct target fields.
> dataset_summary.json: split counts, identifier patterns, special-token metadata, metric metadata, and the submission schema.
> sample_submission.csv: exactly the string columns case_id and prediction_json, with one structurally valid row per test case. It uses NONE for every evidence selection and an empty reading, and its score is exactly 0.
>
> The hidden evaluator file answers.csv is not solver-visible. It has the string columns case_id and answer_json; each packed object contains the target evidence and reading plus the case-specific values required for strict validation.
>
> Each JSONL line is one case object:
>
> case_id — type string; opaque case identifier.
> query — type object; ordered transformed context around the omitted center.
> left — type string array; tokens from up to two preceding verse lines in source order, including the documented line-boundary token when both lines exist.
> right — type string array; tokens from up to two following verse lines in source order, including the documented line-boundary token when both lines exist.
> references — type object array; exactly five reference witnesses in case-specific order.
> witness_id — type string; opaque witness identifier.
> segments — type object array; 5 to 24 candidate passages for the witness.
> segment_id — type string; opaque candidate identifier.
> left — type string array; ordered context before the candidate center.
> center — type non-empty string array; ordered opaque tokens for the candidate verse line.
> right — type string array; ordered context after the candidate center.
> answer — type object, train and validation only; target structured output.
> evidence — type object; one witness-to-segment entry for each of the five reference witnesses.
> reading — type non-empty string array; the authentic omitted query reading.
>
> The vocabulary is global across cases, so equal token IDs represent equal normalized source tokens throughout the public dataset. A documented mask token may appear in context, and a documented boundary token separates adjacent context lines. Neither special token may appear in a predicted reading.
>
> Complete poem documents are kept as whole split groups: 49 documents supply 940 train cases, 10 supply 252 validation cases, and 20 supply 388 test cases. No document or textual witness crosses a split, and parallel JSON and TEI encodings are never treated as independent examples.
>
> Submission
>
> Write ./working/submission.csv with exactly two columns in this order:
>
> case_id,prediction_json
>
>
>
> Every prediction_json value must decode to an object with exactly two keys:
>
> {"evidence":{"W1":"S03","W2":"NONE","W3":"S11","W4":"S07","W5":"S04"},"reading":["T000002","T000017"]}
>
>
> evidence must contain exactly the five witness IDs supplied by that case. Each value must be a segment ID belonging to that witness or the literal string NONE.
> reading must be an array of globally valid token-ID strings. A non-empty reading must exactly match an attested candidate-center sequence allowed by the case. It may be empty to abstain.
>
> Rows may appear in any order. An actual submission must contain all 388 case IDs from test.jsonl exactly once.
>
> The grader rejects wrong columns, duplicate or unknown case IDs, missing or extra cases, empty cells, malformed JSON, extra JSON keys, missing witness keys, cross-witness segment IDs, unknown token IDs, special tokens in readings, or non-attested reading sequences.
>
> Evaluation
>
> Higher scores are better. Let N be the number of scored cases and define clip(x, 0, 1) = min(1, max(0, x)).
>
> For case c, let a_raw,c be the fraction of its five evidence selections that are correct. If evidence slot i has K_(c,i) candidate segments, define the case's uniform-chance evidence rate and adjusted alignment as:
>
> a_raw,c = correct evidence selections in case c / 5
> a0,c    = (1 / 5) * sum_i (1 / K_(c,i))
> A_c     = clip((a_raw,c - a0,c) / (1 - a0,c), 0, 1)
>
>
>
> Define exact reading correctness, complete recovery, and normalized token edit similarity as follows. Here levenshtein is token-level edit distance: each insertion, deletion, or substitution of one token ID costs one, and characters inside a token ID are never compared separately.
>
> E_c = 1 if the predicted reading exactly equals the gold reading, else 0
> Q_c = 1 if E_c = 1 and all five evidence selections are correct, else 0
> T_c = 1 - levenshtein(predicted_c, gold_c) / max(len(predicted_c), len(gold_c), 1)
>
>
>
> The final score is the mean of additive case contributions:
>
> score = (1 / N) * sum_c [0.05*A_c^2 + 0.90*Q_c + 0.05*T_c^2]
>
>
>
> The dominant component rewards only complete recovery of the authentic reading and all five alignments in the same case. The score is bounded to [0,1], the all-abstain sample scores exactly 0, and the oracle scores exactly 1.
>
> Rules
>
> Use only the supplied public challenge files. Web lookup, external copies of the source corpus, reverse-identification of source documents or witnesses, hardcoded test answers, private-file access, and grader exploitation are prohibited. General-purpose code and libraries already available in the execution environment are allowed when they do not contain or retrieve source records or pretrained source-specific assets.
>
> The complete solution must run offline without internet access or runtime package installation.
>
> Submissions
> 9
> Top Score
> 0.437
> Created
> Jul 19, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> 2/12
> solvers beat AI
> How closing works
>
> 3 more distinct solvers needed to activate the $650 prize pool and start the closing countdown. At 12, up to 12 solvers will be selected to continue.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.


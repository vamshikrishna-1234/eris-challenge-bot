# CPU NLP Challenge Examples

Scrape timestamp: 2026-07-14T00:00:00+05:30

Confirmed CPU examples in this document: 4

These entries are included because the challenge detail page displayed this domain and the challenge is part of the CPU-only challenge collection.

## Will It Return? Entity Persistence Forecasting in Nigerian Pidgin News

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75wj7jn992778vdpv0gga0d58amrwc
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> News articles introduce many people, places, organizations, events, products, dates, and monetary amounts. Some are incidental and disappear immediately; others become part of the article's continuing narrative. Your task is to forecast that future discourse behavior before the rest of the article is revealed.
> Each example contains the first 35% of a Nigerian Pidgin article. One named-entity mention is surrounded by <TARGET>...</TARGET>. The target has appeared exactly once in the visible prefix and does not occur in the title. Predict whether the same normalized entity surface appears again anywhere in the hidden 65% of the article:
> RETURN: the entity surface appears at least once in the hidden suffix.
> NO_RETURN: it does not appear again.
> This is not named-entity recognition. The mention and its entity type are already supplied. The target is a future, set-level discourse property: it only exists after comparing the observed mention with the withheld set of later mentions, and it is not stored as a field in the source corpus.
> The benchmark removes entity surfaces that occur in more than one source article. It also groups near-duplicate articles before splitting, so memorizing a recurring name or retrieving another version of the same story does not solve the task.
> Data
> All files are under ./dataset/public/.
> | File | Rows | Contents | |---|---:|---| | train.parquet | 329 | Labelled entity-prefix examples | | test.parquet | 110 | The same input columns with future_return withheld | | sample_submission.csv | 110 | Random valid predictions demonstrating the submission format |
> Training labels contain 249 NO_RETURN and 80 RETURN examples. The hidden test labels contain both classes. Train and test are disjoint by connected near-duplicate article component and by normalized entity surface.
> Columns
> | Column | Type | Description | |---|---|---| | example_id | string | Opaque identifier assigned after splitting and shuffling | | mention | string | The target entity surface as it first appears | | entity_type | string | Source entity type: PERSON, LOCATION, DATE, ORGANIZATION, EVENT, PRODUCT, or MONEY | | title | string | Article title; the normalized target surface is guaranteed not to occur here | | prefix_text | string | First 35% of the article, with the sole visible target occurrence marked by <TARGET> tags | | future_return | string | Train only: RETURN or NO_RETURN |
> Submission
> Write ./working/submission.csv with exactly two columns in this order:
> example_id,future_return
> er_0123456789abcdef,NO_RETURN
> er_fedcba9876543210,RETURN
> The file must contain exactly one row for each of the 110 test example_id values. Row order is arbitrary. The grader rejects extra, missing, duplicated, blank, or unknown IDs; missing values; extra or reordered columns; and labels outside the exact vocabulary NO_RETURN, RETURN.
> Evaluation
> The score is the binary Matthews Correlation Coefficient, clipped to [0, 1]. Higher is better.
> Let RETURN be the positive class and count:
> TP = predicted RETURN and true RETURN
> TN = predicted NO_RETURN and true NO_RETURN
> FP = predicted RETURN and true NO_RETURN
> FN = predicted NO_RETURN and true RETURN
> MCC = (TP*TN - FP*FN) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN))
> score = clip(MCC, 0, 1)
> If the denominator is zero, MCC is defined as zero. Consequently, predicting either label for every row scores exactly 0.0. The metric rewards discrimination rather than the majority-class frequency.
> What to use
> Train from scratch using the supplied text. Useful signals include the target's local grammatical role, whether it is presented as a principal actor or incidental detail, the surrounding reporting verbs, entity type, paragraph position, and how the title frames the story. Word or character n-grams, linear classifiers, small CNNs, recurrent models, and compact transformers can all run comfortably on CPU.
> A strong lightweight approach extracts a local window around <TARGET>, combines it with mention and entity_type, trains a word n-gram classifier, and calibrates its decision threshold with out-of-fold predictions.
> What not to use
> No internet, package installation, hosted model APIs, or runtime downloads.
> No pretrained language-model weights or external entity databases.
> Do not attempt to recover or scrape the withheld article suffix from BBC URLs or other sources.
> Do not predict from example_id; identifiers are cryptographically opaque and assigned after the grouped split.
> Do not assume article rows are independent during local validation; several candidate entities can come from one article.

Inspiration note: Useful because it frames CPU NLP as entity-level temporal forecasting in a low-resource language/news setting, with a prediction target beyond ordinary classification.

## Cross-Lingual Frame Consistency Audit

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ahra9dp0e6ph5xfnhc04nrh8a0exx
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Each test case is a localization audit packet for a voice-assistant semantic parser. You receive one primary utterance, two supporting utterances in other locales, and a proposed semantic frame. The proposed frame may be correct, partially stale, copied from a nearby intent, missing a slot type, or supported by inconsistent evidence.
> Your job is to predict the repaired frame and the type of audit failure:
> the true scenario
> the true intent
> the true slot-type signature
> the slot-count bucket implied by that signature
> the corruption type in the proposed packet
> whether the multilingual evidence is internally consistent
> This is not a plain intent-classification benchmark. A strong solution should compare the utterance text, support evidence, proposed frame, and learned label relationships. The score rewards multilingual representation learning, structured slot reasoning, corruption detection, and logically consistent outputs.
> Public Files
> FileDescription./dataset/public/train.csvLabeled audit packets for training. Includes all input columns and target columns../dataset/public/test.csvUnlabeled audit packets for prediction. Includes only input columns../dataset/public/sample_submission.csvValid submission skeleton with the required columns and row count. Its values are intentionally simplistic../dataset/public/consistency_constraints.csvPublic consistency hints for legal slot-count buckets, corruption-to-evidence relationships, known slot types, and observed intent-scenario relationships.
> The private grader uses hidden target labels and hidden stratification buckets. Public test rows do not contain the target columns, source row identifiers, source split names, or annotated slot spans.
> Input Columns
> ColumnTypeDescriptioncase_idstringOpaque test case identifier.primary_localestringLocale code for the primary utterance.primary_scriptstringCoarse script bucket for the primary locale.primary_utterancestringMain utterance whose semantic frame must be audited.support_locale_astringLocale code for the first supporting utterance.support_utterance_astringFirst supporting utterance.support_locale_bstringLocale code for the second supporting utterance.support_utterance_bstringSecond supporting utterance.proposed_scenariostringProposed high-level scenario. It may be wrong.proposed_intentstringProposed intent. It may be wrong.proposed_slot_signaturestringProposed sorted pipe-separated slot-type signature, or NONE. It may be wrong.proposed_slot_count_bucketstringProposed slot-count bucket: zero, one, two, or three_plus.
> Extra Public File Columns
> consistency_constraints.csv has the following columns:
> ColumnTypeDescriptionconstraint_typestringConstraint group name, such as intent_scenario, corruption_evidence, known_slot_type, or slot_count_bucket.keystringConstraint key. For example, an intent label, corruption label, slot type, or bucket name.valuestringConstraint value associated with the key.
> This challenge does not use support_snippet_ids or evidence_json columns. Evidence is represented by the separate support_locale_a, support_utterance_a, support_locale_b, and support_utterance_b columns.
> Hidden Targets
> The private answer file contains the following target columns for each public test case_id:
> ColumnTypeDescriptionscenariostringTrue repaired scenario.intentstringTrue repaired intent.slot_signaturestringTrue sorted pipe-separated slot-type signature, or NONE.slot_count_bucketstringTrue slot-count bucket implied by slot_signature.corruption_typestringAudit failure class for the proposed packet.evidence_consistentinteger1 if the support utterances are consistent with the repaired frame, otherwise 0.
> The private answer file also contains hidden bucket columns used only for stratified scoring. These buckets are not available to participants.
> Output Targets
> TargetAllowed ValuesScoring RolescenarioScenario labels observed in the public training labels.Exact-match scenario reconstruction.intentIntent labels observed in the public training labels.Exact-match intent reconstruction and intent-scenario consistency.slot_signatureNONE, or sorted slot labels separated by the pipe character.Slot-set Jaccard and exact-match scoring.slot_count_bucketzero, one, two, or three_plus.Exact-match bucket scoring and consistency with slot_signature.corruption_typeclean, intent_swap_same_scenario, intent_swap_cross_scenario, slot_drop, slot_add_distractor, evidence_mismatch, or frame_transplant.Macro-F1 failure-mode scoring and evidence consistency checks.evidence_consistent0 or 1.Exact-match evidence audit scoring.
> Exact Evaluation Metric
> Higher is better. Let there be N hidden test rows. For row i, let predicted values use a hat, such as scenario_hat_i, and hidden truth values use no hat.
> Slot Parsing
> For any slot_signature, parse NONE or an empty string as the empty set. Otherwise split on the pipe character and strip whitespace.
> For each row:
> slot_jaccard_i =
> 1                                      if predicted and true slot sets are both empty
> 0                                      if exactly one slot set is empty
> |predicted_slots_i intersect true_slots_i| / |predicted_slots_i union true_slots_i| otherwise
> slot_exact_i = 1[predicted_slots_i == true_slots_i]
> Aggregate slot scores:
> slot_jaccard = mean_i(slot_jaccard_i)
> slot_exact = mean_i(slot_exact_i)
> Label Components
> scenario_accuracy = mean_i(1[scenario_hat_i == scenario_i])
> intent_accuracy = mean_i(1[intent_hat_i == intent_i])
> slot_count_accuracy = mean_i(1[slot_count_bucket_hat_i == slot_count_bucket_i])
> evidence_accuracy = mean_i(1[evidence_consistent_hat_i == evidence_consistent_i])
> corruption_macro_f1 is the unweighted macro-F1 over the corruption labels present in the hidden truth. For each true corruption label c:
> precision_c = TP_c / (TP_c + FP_c), or 0 if the denominator is 0
> recall_c = TP_c / (TP_c + FN_c), or 0 if the denominator is 0
> f1_c = 2 * precision_c * recall_c / (precision_c + recall_c), or 0 if both are 0
> corruption_macro_f1 = mean_c(f1_c)
> Logical Consistency Penalty
> Each row receives four consistency checks:
> intent_scenario_ok_i = 1 if predicted scenario is a valid scenario for the predicted intent in the hidden test label map, else 0
> slot_bucket_ok_i = 1 if predicted slot_count_bucket equals the bucket implied by predicted slot_signature and is one of the four allowed buckets, else 0
> corruption_evidence_ok_i = 1 if predicted evidence_consistent matches the expected value for the predicted corruption_type, else 0
> known_corruption_ok_i = 1 if predicted corruption_type is one of the seven allowed corruption labels, else 0
> Expected evidence values by predicted corruption type:
> corruption_typeExpected evidence_consistentclean1intent_swap_same_scenario1intent_swap_cross_scenario1slot_drop1slot_add_distractor1evidence_mismatch0frame_transplant0
> The row and aggregate logical consistency scores are:
> logical_consistency_i = mean(intent_scenario_ok_i, slot_bucket_ok_i, corruption_evidence_ok_i, known_corruption_ok_i)
> logical_consistency = mean_i(logical_consistency_i)
> Component Score
> component_score =
> 0.12 * scenario_accuracy
> + 0.24 * intent_accuracy
> + 0.20 * slot_jaccard
> + 0.08 * slot_count_accuracy
> + 0.16 * corruption_macro_f1
> + 0.07 * evidence_accuracy
> + 0.08 * logical_consistency
> + 0.05 * slot_exact
> Stratified Score
> The grader computes a row-quality score with the same weights, but using row-level exact corruption correctness rather than macro-F1:
> row_quality_i =
> 0.12 * 1[scenario_hat_i == scenario_i]
> + 0.24 * 1[intent_hat_i == intent_i]
> + 0.20 * slot_jaccard_i
> + 0.08 * 1[slot_count_bucket_hat_i == slot_count_bucket_i]
> + 0.16 * 1[corruption_type_hat_i == corruption_type_i]
> + 0.07 * 1[evidence_consistent_hat_i == evidence_consistent_i]
> + 0.08 * logical_consistency_i
> + 0.05 * slot_exact_i
> For each hidden bucket column, the grader averages row_quality_i within each bucket value:
> Hidden Bucket ColumnPurposeprimary_scriptBalances performance across script groups.slot_count_bucket_trueBalances performance across slot complexity.corruption_type_trueBalances performance across failure modes.difficulty_bucketBalances performance across combined script, slot, and corruption difficulty strata.
> stratified_score = mean(all per-bucket row_quality means across the four hidden bucket columns)
> Final Score
> raw_score = clip(0.75 * component_score + 0.25 * stratified_score, 0, 1)
> final_score = raw_score ^ 4
> The exponent is a monotonic calibration step. It preserves ranking, keeps a perfect submission at 1.0, and makes high leaderboard scores require consistently strong performance across all output targets and hidden buckets.
> Submission Format
> Submit a CSV file named submission.csv with exactly 1,200 rows and exactly these columns:
> ColumnTypeRequirementcase_idstringMust match one ID from test.csv. Every test ID must appear exactly once.scenariostringPredicted repaired scenario. Missing values are invalid.intentstringPredicted repaired intent. Missing values are invalid.slot_signaturestringNONE or sorted pipe-separated slot labels. Missing values are invalid.slot_count_bucketstringMust be zero, one, two, or three_plus for full consistency credit. Missing values are invalid.corruption_typestringMust be one of the seven allowed corruption labels for full consistency credit. Missing values are invalid.evidence_consistentintegerMust be binary: 0 or 1. Non-binary values are rejected.
> Validation requirements:
> Exactly 1,200 rows.
> Header row is required.
> No duplicate case_id values.
> Submitted ID set must exactly match test.csv.
> No missing values in target columns.
> evidence_consistent must be parseable as binary 0 or 1.
> Unknown scenario, intent, slot_count_bucket, slot_signature, or corruption_type strings are not separately rejected, but they receive no exact-match credit and can reduce logical consistency.
> Concrete valid CSV example:
> case_id,scenario,intent,slot_signature,slot_count_bucket,corruption_type,evidence_consistent
> mfra_00000000000000,alarm,alarm_set,date|time,two,slot_drop,1
> mfra_11111111111111,music,play_music,music_genre,one,intent_swap_same_scenario,1
> mfra_22222222222222,weather,weather_query,NONE,zero,evidence_mismatch,0
> The example above illustrates formatting only. Use the actual case_id values from test.csv.

Inspiration note: Useful because it turns CPU NLP into cross-lingual consistency auditing, asking models to compare semantic frames across languages rather than solve ordinary classification.

## Finding the Spliced-In Sentence in a Literary Passage

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f3wxwv554yc63k1x4sqs4yn8ajeff
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> Finding the Spliced-In Sentence in a Literary Passage
> Overview
> A well-written passage of prose reads as a coherent chain of sentences: each one follows
> from the last in topic, tone, and narrative thread. In this challenge every passage is a run
> of consecutive sentences from a real book - but exactly one sentence has been replaced by
> a sentence spliced in from a different book. The spliced-in sentence is chosen so that it
> shares vocabulary with the passage and reads plausibly on its own; what gives it away is that
> it does not fit the flow of the passage - it breaks the thread the surrounding sentences
> build.
> Given the passage, identify the position of the spliced-in (intruding) sentence.
> You are given 1,500 training passages (each labelled with its intruder position) and must
> predict the intruder position for each of the 4,092 test passages.
> Data provenance
> The passages are drawn from a large public-domain collection of classic English-language
> books. Each book is segmented into sentences; one sentence in a passage is replaced by a
> sentence taken from a different book, and every sentence is automatically paraphrased
> (neural back-translation), so the passages do not correspond verbatim to any single source
> text. The task is related to work on discourse coherence and sentence-level text
> modelling in NLP.
> Encoding
> Input format (one row)
> A passage of 5-8 sentences, each prefixed by a position marker [S0] [S1] ...:
> [S0] <sentence 0> [S1] <sentence 1> [S2] <sentence 2> ... [Sk] <sentence k>
> Example input (a real training passage, intruder at position 3):
> [S0] "It'll be yours, my dear, whatever Aunt Jane decides. [S1] It's a compact one, and I'll seal it with a kiss." She jumped up and kneeled next to Beth and kissed her fervently. [S2] "Now we should be friends?" she asked recklessly. [S3] I didn't leave a ring with her. [S4] Such generosity, which was fed by acting, and Louise's art was too airy to be real.
> Here [S3] is the intruder - plausible in isolation, but it does not belong to the affectionate
> scene the other sentences build.
> Parse the passage with the regex \\[S(\\d+)\\]; the markers are always contiguous
> [S0] ... [Sk] with k between 4 and 7.
> Target
> The integer position of the intruding sentence - a single value 0 ... 7. For the example
> above:
> 3
> Dataset
> Arrays are in NumPy .npz format.
> train.npz - 1,500 training passages. Keys:
> ids - (1500,) int64 row identifiers, 0 ... 1499.
> input_str - (1500,) string, the marked passage.
> target_str - (1500,) string, the intruder position (an integer as a string).
> test.npz - 4,092 passages to label. Keys: ids (int64, 1500 ... 5591),
> input_str (string). The intruder position is withheld.
> IDs are globally unique across the dataset: test ids continue exactly where the
> training ids end.
> sample_submission.csv - a correctly-formatted example submission (predicts the single
> most common intruder position for every passage).
> The train and test passages come from different books, so the test passages are from books
> not seen in training.
> Evaluation
> Accuracy - the fraction of test passages whose intruder position is predicted exactly
> (higher is better, range 0-1). The final score is the mean over all 4,092 test rows.
> Worked example
> Intruder position: 3. You predict 3 -> correct (contributes 1). You predict 5 -> wrong
> (contributes 0).
> Submission format
> Submit submission.csv with exactly two columns and one row per test id
> (4,092 rows plus a header):
> id (int) - the test id from test.npz.
> prediction (int) - the predicted intruder position, a single integer 0 ... 7.
> Example:
> id,prediction
> 1500,3
> 1501,0
> 1502,6
> Every id in test.npz must appear exactly once. The grader rejects predictions outside
> 0 ... 7, empty predictions, duplicate ids, and missing/extra ids.
> What not to use
> No external data. Train only on train.npz - do not fetch external book corpora to
> match sentences against.
> No test labels. The intruder positions are withheld - produce predictions purely from
> the test inputs and a model learned on the training data.
> Reproducible inference. Fixed seeds, deterministic decoding - re-running on test.npz
> must reproduce the same submission.csv.

Inspiration note: Useful because it makes coherence failure localization the target, with a clean single-index output and a strong discourse-modeling angle that fits CPU-only NLP well.

## OpenAPI Shadow-Key Canary Incident Forensics

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f4ng2ynr7666w5c8hwbb3k18atyk5
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, large-scale
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-19; no leaderboard rank context captured.

Full challenge description from page:

> OpenAPI Shadow-Key Canary Incident Forensics
> Overview
> You are auditing transformed API ledgers. Each row starts from a real OpenAPI operation and is converted into a shadow-key ledger: original words are replaced by stable pseudotokens such as w0012_5 and u003_7, where the suffix records token length but the original word is hidden.
> Every row contains one main operation sketch, five related shadow operations, and twelve key cards. Exactly two key cards have an incorrect visible ledger_state. One additional key card is a hidden canary: its visible ledger_state is already correct, but it is deliberately chosen to resemble the corrupted pair and create a hard false-positive trap.
> Your task is to submit one compact forensic patch that:
> identifies the two corrupted cards,
> identifies the one canary card that must be kept unchanged,
> repairs the state and evidence source for each corrupted card,
> classifies the pair-level incident signature.
> This is a structured NLP forensics challenge over real API contract language. It is not ordinary keyphrase extraction, endpoint classification, schema typing, table regression, API diffing, compatibility-drift detection, or a simple contract repair benchmark. Strong solutions need to compare local operation evidence, cross-operation vault evidence, key-shape metadata, required flags, field types, security hints, route hints, request/response hints, noisy neighboring operations, and canary false positives.
> The challenge is CPU-only. Solutions must run within 1.5 hours on 10 CPU cores and 62 GB RAM. Suitable approaches include classical retrieval, sparse text features, constrained decoding, rule systems, gradient boosted trees, linear models, and small CPU-friendly NLP models.
> Dataset
> The prepared files are generated from the uploaded APIs.guru OpenAPI source corpus.
> train.csv
> | Column | Type | Description |
> |---|---|---|
> | id | string | Unique row id for the prepared shadow-ledger example. |
> | operation_sketch | string | Main operation evidence. It includes method=, pseudotokenized route=, api_hint=, tag_hint=, and text_hint= fields. |
> | key_vault | string | Five related shadow operations labeled A01 through A05. Each anchor contains method, route, text hint, and comma-separated key_hints. These anchors provide cross-operation evidence, especially for vault-mirror incidents. |
> | contract_registry | string | Twelve key cards labeled K01 through K12. Each card includes key, parts, shape, dtype, required, note, and visible ledger_state. Exactly two visible ledger_state values are wrong, and one correct card is the hidden canary. |
> | audit_note | string | Short reminder of the repair, canary, and incident-signature task. |
> | repair_delta | string | Ground-truth patch for training rows. This includes FIX, KEEP, both SET_Kxx values, both SRC_Kxx values, and SIG. Hidden for test rows. |
> test.csv
> | Column | Type | Description |
> |---|---|---|
> | id | string | Unique row id for the prepared test example. |
> | operation_sketch | string | Same structure as train.csv. |
> | key_vault | string | Same structure as train.csv. |
> | contract_registry | string | Same structure as train.csv. |
> | audit_note | string | Same structure as train.csv. |
> sample_submission.csv
> | Column | Type | Description |
> |---|---|---|
> | id | string | Test row id. |
> | prediction | string | Your structured repair patch, canary id, and incident signature. |
> Key Card Format
> Each line in contract_registry has this structure:
> K03 key=w0007_4_w0018_6; parts=2; shape=camel; dtype=string; required=Y; note=w0041_8 w0009_5; ledger_state=FILTER_KEY
> Field meanings:
> K03: visible card id used in your patch.
> key: pseudotokenized key or field name.
> parts: number of identifier pieces in the original key.
> shape: identifier shape such as camel, snake, dash, upper, or plain.
> dtype: OpenAPI type when available, otherwise unknown.
> required: Y if the field/parameter is required, otherwise N.
> note: pseudotokenized description text for that key.
> ledger_state: visible state label. Two labels are corrupted; the canary label is correct.
> Canary Card
> The canary is a correct key card that should not be repaired. It is selected as a high-confusion near miss using similarities to the corrupted pair, including state family, source family, identifier shape, data type, required flag, and pseudotoken overlap. This makes the task false-positive resistant: a model must distinguish the two truly corrupted cards from one tempting card that looks suspicious but is already correct.
> Submit the canary as KEEP=Kxx.
> Valid Ledger States
> Each repaired card must use one of these state labels:
> PATH_BIND: key is bound to a path variable or route slot.
> FILTER_KEY: query/filter style input key.
> WINDOW_KEY: pagination, cursor, limit, offset, count, or windowing key.
> AUTH_CONTROL: authentication, authorization, token, header, cookie, or security-control key.
> MUTATION_FIELD: request-body field used to create or modify a resource.
> IDENTITY_REF: id, uuid, slug, reference, or foreign-key style field.
> RESPONSE_SIGNAL: response status, error, success, reason, message, or state signal.
> OUTPUT_VALUE: ordinary response value.
> VAULT_ALIAS: key best explained by a related anchor operation in key_vault.
> Valid Evidence Sources
> Each repaired card must also include one source label:
> PATH
> QUERY
> HEADER
> BODY
> RESPONSE
> SECURITY
> A01
> A02
> A03
> A04
> A05
> NONE
> Use A01 through A05 when the best evidence is a related operation in key_vault.
> Incident Signatures
> After repairing the two corrupted cards, classify the pair with one SIG= value. The signature is a latent incident type derived from the corrected states and evidence sources.
> Valid signatures:
> DUAL_VAULT_MIRROR: both repairs are explained by two different vault anchors.
> VAULT_MIRROR: at least one repair is explained by a vault anchor or a VAULT_ALIAS state.
> CONTROL_GATE: at least one repaired state is AUTH_CONTROL and no vault rule applies.
> IDENTITY_TRACE: at least one repaired state is IDENTITY_REF and no earlier signature rule applies.
> BODY_RESPONSE_BRIDGE: one repaired source is BODY and one repaired source is RESPONSE, with no earlier signature rule applying.
> INPUT_WINDOW: both repaired states are from PATH_BIND, FILTER_KEY, or WINDOW_KEY, with no earlier signature rule applying.
> RESPONSE_ECHO: at least one repaired state is RESPONSE_SIGNAL or OUTPUT_VALUE, with no earlier signature rule applying.
> LOCAL_BIND: fallback local incident when none of the above rules apply.
> The priority order is exactly the order shown above.
> Submission
> Submit one CSV with exactly these columns:
> id,prediction
> osk_example_001,"FIX=K03,K09 | KEEP=K06 | SET_K03=FILTER_KEY | SRC_K03=QUERY | SET_K09=VAULT_ALIAS | SRC_K09=A02 | SIG=VAULT_MIRROR"
> Patch fields:
> FIX=K03,K09 lists the two corrupted key-card ids.
> KEEP=K06 lists the one correct canary card that should not be changed.
> SET_K03=FILTER_KEY assigns the corrected ledger state for K03.
> SRC_K03=QUERY assigns the evidence source for K03.
> SIG=VAULT_MIRROR assigns the incident signature for the repaired pair.
> Repeat SET_Kxx= and SRC_Kxx= for both fixed cards.
> Predictions should be short patch strings. Long explanations, JSON objects, extra candidate lists, or prose answers are not valid submission style and may be penalized.
> Evaluation
> The leaderboard score is the mean row score over all test rows. Higher is better. The theoretical score range is 0 to 1.
> For each row, the grader parses your prediction and the hidden repair_delta.
> Sub-metrics
> localization_f1: F1 score between the predicted FIX key ids and the true corrupted key ids. It is calculated as (2 localization_precision localization_recall) / (localization_precision + localization_recall), with 0 if precision and recall are both 0.
> state_accuracy: among the two true corrupted cards, the fraction whose SET_Kxx state exactly matches the hidden state.
> source_accuracy: among the two true corrupted cards, the fraction whose SRC_Kxx source exactly matches the hidden source.
> canary_accuracy: 1 if the submitted KEEP=Kxx exactly matches the hidden canary card; otherwise 0.
> signature_accuracy: 1 if the submitted SIG= value exactly matches the hidden incident signature; otherwise 0.
> complete_case: 1 if the two FIX ids, both states, both sources, the KEEP canary, and the SIG signature are all correct; otherwise 0.
> fallback_token_f1: a small backup F1 over non-generic tokens in the prediction and truth after removing words such as fix, set, keep, canary, key, state, and source.
> length_penalty: min(prediction_token_count, truth_token_count) / max(prediction_token_count, truth_token_count). Empty predictions use a token count of 1 for this calculation.
> Row Score
> row_score = length_penalty * (
> 0.04 * localization_f1
> + 0.16 * state_accuracy
> + 0.16 * source_accuracy
> + 0.16 * canary_accuracy
> + 0.16 * signature_accuracy
> + 0.30 * complete_case
> + 0.02 * fallback_token_f1
> )
> Exact full patch matches receive 1.0 for the row. Missing, invalid, or unrelated predictions can score 0.0.
> What You Should Use
> Train on the provided train.csv rows.
> Use CPU-friendly retrieval over operation_sketch, key_vault, and contract_registry.
> Use structured features from parts, shape, dtype, required, note, route evidence, response evidence, security evidence, and anchor overlap.
> Model false-positive traps because the KEEP canary is intentionally similar to the corrupted pair.
> Model the pair interaction between the two repairs, because the SIG label depends on their combined states and sources.
> Validate on held-out training rows because the metric rewards complete two-card repairs, canary discrimination, and correct incident signatures.
> What You Should Not Use
> Do not use internet lookup or source OpenAPI spec lookup at prediction time.
> Do not train or run GPU-only models.
> Do not submit prose explanations, JSON objects, or multiple candidate patches per row.

Inspiration note: Useful because it turns API-contract repair into a compact forensic patch prediction task, with structured pair reasoning and an explicit canary false-positive trap.

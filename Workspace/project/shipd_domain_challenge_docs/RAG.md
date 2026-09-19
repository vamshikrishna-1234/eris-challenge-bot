# RAG Challenge Examples

Scrape timestamp: 2026-07-01T06:39:43+05:30

Confirmed examples in this document: 15

These entries are included only because the challenge detail page displayed this target domain. Titles were not used for classification.

## Cost Efficient RAG Optimization
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77jfkzrny5rehcn0q9kc0wm9836zhp
- DOMAIN exactly as displayed: RAG
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: duongnguyen ranked 1st (leaderboard #3, score —); safwan188 ranked 3rd (leaderboard #26, score —); lady_faye1998 ranked #4 (leaderboard #25, score —)

Full challenge description from page:

> Overview
> In production retrieval-augmented generation (RAG) systems, every retrieved token costs money and competes for limited context window space. Retrieving too many passages dilutes the model's attention and inflates API costs, while retrieving too few risks missing critical evidence. The most effective RAG pipelines must solve an optimization problem: find the minimum evidence needed for a correct answer.
> This challenge tests your ability to build a cost-efficient RAG system that balances answer quality against retrieval cost. Each query comes with a pool of 10–25 candidate document chunks drawn from heterogeneous knowledge sources (text passages, table excerpts, and knowledge-graph triples). Your system must:
> Select evidence efficiently — choose only the chunks that are essential for answering, avoiding irrelevant or redundant context
> Answer the question — produce a short answer grounded in the selected evidence
> The scoring metric explicitly rewards precision and compression: systems that answer correctly while selecting fewer, more targeted chunks outscore systems that dump the entire pool into context.
> Evaluation
> Submissions are scored using a composite answer quality + retrieval efficiency metric:
> score = 0.5 x answer_F1 + 0.5 x evidence_efficiency
> Where:
> answer_F1 is the token-level F1 between predicted and gold answer (after lowercasing, removing articles and punctuation)
> evidence_efficiency combines two signals:
> Evidence precision: what fraction of your selected chunks are actually gold evidence
> Context compression: what fraction of the total pool you chose NOT to include
> evidence_efficiency = 0.3 + 0.4 x precision + 0.3 x compression
> precision = |selected_chunks ∩ gold_chunks| / |selected_chunks|
> compression = 1 - |selected_chunks| / total_pool_size
> The evidence_efficiency component ranges from 0.3 (selected everything, none gold) to 1.0 (selected only gold evidence, left everything else out). The additive formulation rewards both dimensions independently: a system with poor answers but excellent retrieval still earns partial credit, and vice versa. Higher is better.
> Submission Format
> Submit a CSV file with three columns:
> id — the query identifier (hash-based string)
> evidence_ids — comma-separated chunk markers identifying your selected evidence (e.g., "C3,C7"). Leave empty only if you determine no chunk is relevant.
> answer — your predicted answer text
> The file must contain one row per test query. All IDs must be present. Example:
> id,evidence_ids,answer
> q_5556508bc0,"C3,C7",Upa River
> q_15a0c3adbe,C2,692
> q_a6af90533b,"C1,C4,C9",Harrison Ford
> Dataset
> Data fields:
> id — unique hash-based identifier for each query
> query — the natural-language question
> context — the candidate chunk pool, formatted as [C1] chunk text\n[C2] chunk text\n... where each chunk may be a text passage, table excerpt, or knowledge-graph triple
> num_chunks — number of chunks in the pool
> evidence_ids (train only) — comma-separated markers of gold evidence chunks
> answer (train only) — the gold-standard short answer
> Files:
> train.csv — training data with queries, chunk pools, gold evidence, and answers
> test.csv — test data with queries and chunk pools (no evidence or answers)
> sample_submission.csv — a valid submission file with default predictions

Inspiration note: Useful because it converts retrieval/query/evidence behavior into a compact measurable target, a strong pattern for hallucination or retrieval-quality challenges.

## GhostRAG - Ghost Knowledge Diagnosis
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dazd6gkrgxwdv4bpgtgxj1h837b01
- DOMAIN exactly as displayed: RAG
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: akhil989899 ranked 1st (leaderboard #49, score —); akhil989899 ranked — (leaderboard #49, score —)

Full challenge description from page:

> Overview
> A B2B fintech company with 180 engineers, 20 production microservices and years of accumulated engineering documentation. The organisation, its employees, its documents, and its queries are entirely synthetic, generated using a seeded procedural generator.
> The knowledge base spans 18 document types — runbooks, postmortems, architecture decision records, Slack archives, tickets, changelogs, configuration files, observability dashboards, RFCs, and more — authored by 16 named employees across 5 engineering squads. Five of these employees have departure dates, meaning knowledge they held may no longer be accessible through the people currently at the company. Every document was generated to reflect realistic engineering writing: full-length content, service-specific terminology, cross-references between documents, and deliberate gaps where knowledge was never written down.
> When an engineer asks a question, a retrieval pipeline searches this knowledge base. Sometimes it fails, and the reasons vary. The failure might be a vocabulary mismatch — the answer exists, but the system used the wrong terms to search for it. It might be a documentation gap — the answer was never written down. It might be ghost knowledge — the information is real, but it lives only inside a person's head, implied by indirect traces across multiple documents, and recoverable only by identifying who holds it and how to reach them.
> Your task is to examine each query and diagnose exactly why retrieval failed - and what should be done about it.
> Evaluation
> Submissions are scored using a composite metric (0–1, higher is better). Scoring is strictly cascading: if your failure_type prediction is wrong for a row, that row scores 0 on all downstream components regardless of what else you predicted.
> import numpy as np
> from sklearn.metrics import precision_recall_fscore_support
> def jaccard(pred_str, true_str):
> pred = set(str(pred_str).split("|")) - {"", "nan"}
> true = set(str(true_str).split("|")) - {"", "nan"}
> if not true: return 1.0 if not pred else 0.0
> if not pred: return 0.0
> tp, fp, fn = len(pred & true), len(pred - true), len(true - pred)
> return max(0.0, (tp - 0.5 * fp) / (tp + fp + fn))
> def evaluate(submission, answers):
> merged = answers.merge(submission, on="query_id", suffixes=("_true", "_pred"))
> classes = sorted(["A", "B", "C", "MULTIHOP", "PARTIAL_ANSWER", "ADVERSARIAL",
> "LONGCONTEXT", "IMPLICIT_CONTEXT", "CROSS_SYSTEM", "TEMPORAL"])
> _, recall, fscore, _ = precision_recall_fscore_support(
> merged["failure_type_true"], merged["failure_type_pred"],
> labels=classes, average=None, zero_division=0
> )
> macro_f1 = np.mean(fscore)
> abc = merged[merged["failure_type_true"].isin(["A", "B", "C"])]
> type_correct_abc = abc["failure_type_true"] == abc["failure_type_pred"]
> action_acc = (type_correct_abc & (abc["recommended_action_true"] == abc["recommended_action_pred"])).mean() if len(abc) else 0.0
> c = merged[merged["failure_type_true"] == "C"]
> type_correct_c = c["failure_type_true"] == c["failure_type_pred"]
> holder_acc = c.apply(
> lambda r: jaccard(r["ghost_holder_pred"], r["ghost_holder_true"])
> if r["failure_type_true"] == r["failure_type_pred"] else 0.0, axis=1
> ).mean() if len(c) else 0.0
> mean_jaccard = c.apply(
> lambda r: jaccard(r["signal_doc_ids_pred"], r["signal_doc_ids_true"])
> if r["failure_type_true"] == r["failure_type_pred"] else 0.0, axis=1
> ).mean() if len(c) else 0.0
> zero_recall_penalty = float((recall == 0).sum()) * 0.008
> wrong_mask     = merged["failure_type_true"] != merged["failure_type_pred"]
> high_conf_mask = merged["confidence_score_pred"] >= 0.7
> confidence_penalty = float((0.05 * merged.loc[wrong_mask & high_conf_mask, "confidence_score_pred"] ** 2).sum())
> raw = 0.40 * macro_f1 + 0.30 * action_acc + 0.15 * holder_acc + 0.15 * mean_jaccard
> return float(np.clip(raw - zero_recall_penalty - confidence_penalty, 0.0, 1.0))
> Component weights:
> | Component                            | Weight | Condition                      |
> |--------------------------------------|--------|--------------------------------|
> | `failure_type` macro-F1 (10 classes) | 40%    | All rows                       |
> | `recommended_action` accuracy        | 30%    | A / B / C rows only, cascading |
> | `ghost_holder` Jaccard               | 15%    | Type C rows only, cascading    |
> | `signal_doc_ids` Jaccard             | 15%    | Type C rows only, cascading    |
> Penalties:
> Zero-recall: -0.008 per failure_type class with zero recall in the submission
> Calibration : For each row where failure_type is wrong and confidence_score ≥ 0.7, subtract 0.05 × confidence_score²
> Note: ghost_holder and signal_doc_ids use FP-penalised Jaccard - predicting extra wrong values actively reduces your score.
> Dataset
> Structure:
> public/
> train.csv
> test.csv
> sample_submission.csv
> train.csv is a mixed-row file. A single CSV that stores three distinct tables unified under a shared column space. Each row_type only populates the columns that belong to it — all other columns for that row will be empty. This is expected: name, role, and squad will be empty on corpus and query rows because those are employee-only fields; doc_id, content, and author will be empty on employee and query rows; and so on. Filter on row_type before working with any subset.
> Filter on row_type to work with each table independently. for example
> train = pd.read_csv("train.csv")
> corpus_df = train[train["row_type" == "corpus"]]
> employee_df = train[train["row_type"] == "employee"]
> query_df    = train[train["row_type"] == "query"]
> row_type = corpus — 548 engineering documents. The knowledge base.
> | Column   | Type | Description                                               |
> |--------  |------|-----------------------------------------------------------|
> | doc_id   | str  | Unique document ID                                        |
> | doc_type | str  | One of: runbook, postmortem, adr, wiki, ticket,           |
> |          |      | slack_snippet, code_comment, meeting_notes, email_thread, |
> |          |      | design_doc, pr_description, onboarding, changelog,        |
> |          |      | sla_document, config, rfc, git_artifact, observability    |
> | title    | str  | Document title                                            |
> | service  | str  | The microservice this document pertains to                |
> | author   | str  | Authoring employee name                                   |
> | date     | str  | Date last modified, `YYYY-MM-DD`                          |
> | content  | str  | Full document text in Markdown                            |
> row_type = employee— 16 employees.
> | Column | Type | Description |
> |---|---|---|
> | `name` | str | Full name |
> | `role` | str | Job title |
> | `squad` | str | Team |
> | `joined` | str | Start date, `YYYY-MM-DD` |
> | `departed` | str | Departure date, `YYYY-MM-DD`. Empty if currently active |
> | `status` | str | `active` or `departed` |
> | `specialisms` | str | Pipe-separated services and domains of expertise |
> | `authored_doc_count` | int | Number of corpus documents authored |
> | `authored_doc_ids` | str | Pipe-separated doc IDs authored (up to 20) |
> | `referenced_in_count` | int | Number of corpus documents that reference this employee |
> | `referenced_doc_ids` | str | Pipe-separated doc IDs referencing this employee |
> row_type = query — 1,872 labelled training queries.
> | Column | Type | Description |
> |---|---|---|
> | `query_id` | str | Unique query identifier |
> | `query_text` | str | The engineer's question |
> | `service` | str | The microservice the query concerns. |
> | `difficulty` | str | `easy`, `medium`, or `hard` |
> | `failure_type` | str | Ground truth label |
> | `ghost_holder` | str | For Type C only: pipe-separated ghost holder role(s). Empty for all other types |
> Note: recommended_action and signal_doc_ids are not provided in training query rows. These must be derived.
> Training labels include intentional noise: approximately 7% of Type A rows are mislabelled as B, 4% of Type B rows as A, and 5% of Type C rows have an incorrect ghost_holder. The training class distribution is heavily skewed toward B — models that do not account for this will under-predict minority classes on test.
> test.csv — 407 unlabelled query rows. No row_type column
> | Column | Type | Description |
> |---|---|---|
> | `query_id` | str | Unique query identifier |
> | `query_text` | str | The engineer's question |
> | `service` | str | The microservice the query concerns |
> | `difficulty` | str | `easy`, `medium`, or `hard` |
> Failure types:
> | Type            | Meaning                                                   |
> |-----------------|-----------------------------------------------------------|
> | A               | Answer exists in corpus; BM25 missed it (vocab mismatch)  |
> | B               | Answer was never written down                             |
> | C               | Knowledge exists but is held by a specific person or role |
> | MULTIHOP        | Answer requires synthesising 3+ documents                 |
> | PARTIAL_ANSWER  | Corpus partially answers; fragments are missing           |
> | ADVERSARIAL     | Corpus contains misleading look-alike documents           |
> | LONGCONTEXT     | Answer is buried deep in a long document                  |
> | IMPLICIT_CONTEXT| Answer requires domain inference, not direct lookup       |
> | CROSS_SYSTEM    | Answer spans multiple services                            |
> | TEMPORAL        | A stale document gives a confidently wrong answer         |
> Type A - recommended_action: reindex
> Type B - recommended_action:document
> Type C — recommended_action : ghost_holder
> ghost_holder to recommended_action mapping :
> | `ghost_holder` | `recommended_action` |
> |---|---|
> | `former_employee` | `archive_search` |
> | `senior_engineer` | `interview` |
> | `architect` | `reconstruct` |
> | `engineering_manager` | `escalate` |
> | `external_vendor` | `vendor_contact` |
> | `on_call_rotation` | `incident_review` |
> Some Type C rows have pipe-separated ghost_holder values (e.g. former_employee|senior_engineer), indicating knowledge distributed across multiple holders. The ghost_holder and signal_doc_ids fields in your submission are scored with FP-penalised Jaccard — partial credit is available for multi-holder predictions, but incorrectly predicting additional holders will reduce your score.
> Submission
> Submit a CSV file with the following format:
> | Column             | Type  | Description                                        |
> |--------------------|-------|----------------------------------------------------|
> | query_id           | str   | Row identifier from test.csv                       |
> | failure_type       | str   | One of the 10 failure types listed above           |
> | recommended_action | str   | Remediation action; empty string for non-A/B/C rows|
> | ghost_holder       | str   | Ghost holder role(s); empty string for non-C rows  |
> | signal_doc_ids     | str   | Pipe-separated corpus doc IDs; empty string for    |
> |                    |       | non-C rows                                         |
> | confidence_score   | float | Your probability of the failure_type being correct |
> Example rows:
> query_id,failure_type,recommended_action,ghost_holder,signal_doc_ids,confidence_score
> qid_00039,A,reindex,,,0.85
> qid_00804,B,document,,,0.92
> qid_00057,C,reconstruct,architect,pos_0145|des_0146,0.78
> qid_00012,MULTIHOP,,,,0.55
> Requirements:
> Must contain exactly 407 rows (one per row in test.csv )
> Use empty string (not NaN) for inapplicable fields
> query_id values must exactly match those in test.csv

Inspiration note: Useful because it converts retrieval/query/evidence behavior into a compact measurable target, a strong pattern for hallucination or retrieval-quality challenges.

## Interplanetary Knowledge Graph RAG Challenge
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7e4eptn4hd4nd5b8w8mvr4j582y4f1
- DOMAIN exactly as displayed: RAG
- Status: Accepted
- Difficulty: Hard
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: duongnguyen ranked 1st (leaderboard #3, score —); caspian ranked 3rd (leaderboard #12, score —); haidang ranked #5 (leaderboard #24, score —)

Full challenge description from page:

> Overview
> The Meridian Compact is a fictional interplanetary confederation spanning 60 star systems, 45 political factions, and centuries of governance history. Its knowledge is stored across a fragmented knowledge graph (4,491 nodes, 16,153 edges) and a corpus of 4,370 natural language archive documents drawn from seven institutional archives: Diplomatic Archives, Personnel Records, Legal Codex, Historical Chronicles, Trade Registry, Scientific Archives, Colonial Registry, Organizational Directory, and Xenological Encyclopedia.
> Your task is to build a Retrieval-Augmented Generation (RAG) system that answers complex multi-hop questions about the Meridian Compact by retrieving relevant information from the knowledge graph and document corpus, then reasoning across multiple pieces of evidence to produce a correct answer.
> Questions range from 2-hop lookups ("Which star system is governed by the faction that Kael Voss belongs to?") to 5-hop chains requiring traversal across persons, organizations, technologies, resources, colonies, and star systems. The dataset also includes temporal reasoning questions (filtering by year ranges), aggregation questions (counting entities), and negation questions (identifying entities that lack certain relationships).
> This is not a simple retrieval task. Naive keyword search will fail on multi-hop questions because the answer entity is never co-mentioned with the question entity in any single document. Agents must chain evidence across multiple retrieved passages or traverse the knowledge graph structure to arrive at the correct answer.
> Evaluation
> Submissions are scored using Token-level F1 (SQuAD-style):
> For each question, the predicted and ground-truth answers are normalized (lowercased, punctuation removed, articles stripped), then tokenized. F1 is computed over the token overlap:
> precision = |common_tokens| / |predicted_tokens|
> recall    = |common_tokens| / |ground_truth_tokens|
> F1        = 2 * precision * recall / (precision + recall)
> The final score is the mean F1 across all 500 test questions. Higher is better. A perfect score is 1.0.
> def evaluate(y_true, y_pred):
> """
> y_true: list of ground-truth answer strings
> y_pred: list of predicted answer strings
> Returns: mean token-level F1 score
> """
> import re, string
> from collections import Counter
> import numpy as np
> def normalize(text):
> text = str(text).lower()
> text = re.sub(r"\b(a|an|the)\b", " ", text)
> text = text.translate(str.maketrans("", "", string.punctuation))
> return " ".join(text.split()).strip()
> def token_f1(pred, gt):
> p_tok = normalize(pred).split()
> g_tok = normalize(gt).split()
> if not g_tok and not p_tok:
> return 1.0
> if not g_tok or not p_tok:
> return 0.0
> common = Counter(p_tok) & Counter(g_tok)
> nc = sum(common.values())
> if nc == 0:
> return 0.0
> prec = nc / len(p_tok)
> rec = nc / len(g_tok)
> return 2 * prec * rec / (prec + rec)
> return float(np.mean([token_f1(p, g) for p, g in zip(y_pred, y_true)]))
> Dataset
> File Structure
> public/
> ├── knowledge_graph/
> │   ├── nodes.jsonl          # 4,491 KG nodes (entities)
> │   └── edges.jsonl          # 16,153 KG edges (relationships)
> ├── corpus/
> │   └── documents.jsonl      # 4,370 natural language archive documents
> ├── train.jsonl              # 1,000 training questions WITH answers
> ├── test.jsonl               # 500 test questions WITHOUT answers
> ├── sample_submission.csv    # Example submission format
> └── dataset_stats.json       # Summary statistics
> private/
> └── answers.csv              # Ground truth answers for test questions
> Knowledge Graph Schema
> Node Types (12):
> Type Count Key Attributes StarSystem 60 name, sector, population, climate_class, discovery_year Colony 400 name, founding_year, population, status Faction 45 name, ideology, founding_year, member_count Person 1,500 name, role, species, birth_year Law 800 name, domain, enacted_year, status Treaty 250 name, signed_year, status, scope Resource 70 name, resource_type, scarcity Technology 300 name, domain, discovery_year, danger_level Event 500 name, event_type, year, location, severity Organization 300 name, org_type, founded_year, mandate Species 75 name, traits, avg_lifespan TradeRoute 200 name, established_year, status, danger_rating
> Edge Types (26): GOVERNS, ALLIED_WITH, HOSTILE_TO, COLONIZED, LOCATED_IN, MEMBER_OF, WORKS_AT, BORN_IN, AUTHORED, DISCOVERED, NEGOTIATED, CAUSED, INVOLVED_IN, REPRESENTED, ENACTED, SIGNED, PARTICIPATED_IN, REGULATES, PROHIBITS, SUPERSEDES, REQUIRES, EXPORTS, IMPORTS, HEADQUARTERED_IN, LED_BY, OVERSEES, ENFORCES, SPONSORS, TRIGGERED, CONNECTS, PRIMARILY_TRADES, HOMEWORLD, ADMINISTERS, REPRESENTS
> Document Corpus
> Each document is a natural language passage derived from a subgraph of the KG, organized by archive:
> Archive Description Approx. Count Diplomatic_Archives Faction profiles & treaty records ~295 Personnel_Records Person dossiers ~1,500 Legal_Codex Law records ~800 Historical_Chronicles Event narratives ~500 Trade_Registry Trade route bulletins ~200 Scientific_Archives Technology reports ~300 Colonial_Registry Colony entries ~400 Organizational_Directory Organization directories ~300 Xenological_Encyclopedia Species encyclopedias ~75
> Question Types
> Type Count (Train) Count (Test) Hops Description multi_hop_2 ~267 ~133 2 Two-step reasoning chains multi_hop_3 ~267 ~133 3 Three-step reasoning chains multi_hop_4 ~200 ~100 4 Four-step reasoning chains multi_hop_5 ~100 ~50 5 Five-step reasoning chains temporal ~67 ~33 1-2 Temporal filtering by year ranges aggregation ~67 ~33 1 Counting entities with specific properties negation ~33 ~17 1 Identifying absence of relationships
> Submission
> Submit a CSV file named submission.csv with the following format:
> Column Type Description question_id string Question identifier from test.jsonl (e.g., TEST-00001) answer string Predicted answer text
> Requirements:
> Must contain exactly 500 rows (one per test question)
> Include header row
> Each question_id must match an ID from test.jsonl
> No duplicate question_id values
> The answer column should contain the predicted entity name or value
> Example:
> question_id,answer
> TEST-00001,Vega Prime
> TEST-00002,Solari Concord
> TEST-00003,42
> ...

Inspiration note: Useful because it converts retrieval/query/evidence behavior into a compact measurable target, a strong pattern for hallucination or retrieval-quality challenges.

## RAG Hallucination Detection From Query Semantics
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dr6xe5qb1pafnx3e1mkg4t182wh0a
- DOMAIN exactly as displayed: RAG
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: feature-engineering, large-scale, generative
- Best/top context found: fate1997 ranked 1st (leaderboard #1, score —)

Full challenge description from page:

Dataset
The training split (train.csv) exposes 63 fully-labelled questions with answers, accepted aliases, question types, and ground-truth passage IDs.
The test split (test.csv) contains 147 questions with no answer fields. The corpus (corpus.csv) of 645 passages is shared between train and test.
Files
corpus.csv -- 645 passages from the Shahnameh, each tagged with the chapter it came from
train.csv -- 63 questions with answers, aliases, types, and ground-truth passage IDs
test.csv -- 147 questions to answer
sample_submission.csv -- example submission format
corpus.csv
passage_id (string): stable identifier, P0000 to P0644
chapter (string): corpus-internal section label the passage was drawn from
text (string): the passage text (roughly 1000-1200 characters)
length (int): character count
train.csv and test.csv
id (int): unique question identifier
question (string): the natural-language question
answer (string, train only): the canonical answer string
answer_aliases (JSON list, train only): all accepted answer spellings
question_type (string, train only): one of relation_*, event_fact, multi_hop, location_object
ground_truth_passage_ids (JSON list, train only): passage IDs that contain evidence for the answer
Question types
relation_* (e.g. relation_father, relation_son, relation_wife, relation_slayer, and similar suffixes) -- direct kinship or action-based relations between entities. The question refers to one entity via an epithet and asks for a related entity.
event_fact -- deed-based questions ("Who led the revolt against the serpent-shouldered tyrant?") about specific actions in the corpus.
multi_hop -- two-step reasoning: first identify an unnamed entity by its epithet, then answer a relation or fact about it.
location_object -- ask for a place, weapon, mount, or artefact.
Submission
Submit a CSV with three columns:
id (int): must match a test.csv id exactly once. Test ids are arbitrary 7-digit integers drawn from the range 1000000-9999999; they are not sequential and do not overlap with train ids.
predicted_answer (string): your answer for the question
retrieved_passage_ids (string): pipe-separated list of passage IDs, ordered from most to least relevant. Only the first three are scored.
Example (the exact id values shown are illustrative — use whatever ids appear in your test.csv):
id,predicted_answer,retrieved_passage_ids
2345678,ExampleName,P0123|P0124|P0098
3456789,ExamplePlace,P0050|P0049|P0051
Requirements:
Row count must equal the number of test questions (one prediction per question).
Each id must appear exactly once and must match a test id.
predicted_answer is compared after lowercasing, article removal, and diacritic stripping.
retrieved_passage_ids may contain any number of entries, but only the first three are scored.
Intended approach
A solution is expected to be a real retrieval-augmented-generation pipeline. The score is deliberately split between retrieval (40 percent) and answer generation (60 percent) so both components must work
Embed the corpus with a pretrained sentence embedder and index the 645 passage vectors.
Embed each question with the same embedder and retrieve the top-k passages by similarity; optionally rerank with a cross-encoder or combine with BM25.
Read and answer with a pretrained language model (Llama, Mistral, Qwen, Flan-T5, or a small extractive QA head finetuned on train.csv) given the question plus the retrieved passages. Prompt it to emit a short entity or place name, not prose.
Normalise the generated string against the answer_aliases lookup built from train.csv.

Inspiration note: Useful because it converts retrieval/query/evidence behavior into a compact measurable target, a strong pattern for hallucination or retrieval-quality challenges.

## Shahnameh Retrieval Augmented Question Answering
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ezrxqck9czzcw0f3ess3ykn854rks
- DOMAIN exactly as displayed: RAG
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: decoder ranked 1st (leaderboard #45, score —); yenwee0804 ranked 2nd (leaderboard #2, score —); akhil989899 ranked #4 (leaderboard #49, score —); sa3dola ranked #5 (leaderboard #11, score —)

Full challenge description from page:

> Dataset
> The training split (train.csv) exposes 63 fully-labelled questions with answers, accepted aliases, question types, and ground-truth passage IDs.
> The test split (test.csv) contains 147 questions with no answer fields. The corpus (corpus.csv) of 645 passages is shared between train and test.
> Files
> corpus.csv -- 645 passages from the Shahnameh, each tagged with the chapter it came from
> train.csv -- 63 questions with answers, aliases, types, and ground-truth passage IDs
> test.csv -- 147 questions to answer
> sample_submission.csv -- example submission format
> corpus.csv
> passage_id (string): stable identifier, P0000 to P0644
> chapter (string): corpus-internal section label the passage was drawn from
> text (string): the passage text (roughly 1000-1200 characters)
> length (int): character count
> train.csv and test.csv
> id (int): unique question identifier
> question (string): the natural-language question
> answer (string, train only): the canonical answer string
> answer_aliases (JSON list, train only): all accepted answer spellings
> question_type (string, train only): one of relation_*, event_fact, multi_hop, location_object
> ground_truth_passage_ids (JSON list, train only): passage IDs that contain evidence for the answer
> Question types
> relation_* (e.g. relation_father, relation_son, relation_wife, relation_slayer, and similar suffixes) -- direct kinship or action-based relations between entities. The question refers to one entity via an epithet and asks for a related entity.
> event_fact -- deed-based questions ("Who led the revolt against the serpent-shouldered tyrant?") about specific actions in the corpus.
> multi_hop -- two-step reasoning: first identify an unnamed entity by its epithet, then answer a relation or fact about it.
> location_object -- ask for a place, weapon, mount, or artefact.
> Submission
> Submit a CSV with three columns:
> id (int): must match a test.csv id exactly once. Test ids are arbitrary 7-digit integers drawn from the range 1000000-9999999; they are not sequential and do not overlap with train ids.
> predicted_answer (string): your answer for the question
> retrieved_passage_ids (string): pipe-separated list of passage IDs, ordered from most to least relevant. Only the first three are scored.
> Example (the exact id values shown are illustrative — use whatever ids appear in your test.csv):
> id,predicted_answer,retrieved_passage_ids
> 2345678,ExampleName,P0123|P0124|P0098
> 3456789,ExamplePlace,P0050|P0049|P0051
> Requirements:
> Row count must equal the number of test questions (one prediction per question).
> Each id must appear exactly once and must match a test id.
> predicted_answer is compared after lowercasing, article removal, and diacritic stripping.
> retrieved_passage_ids may contain any number of entries, but only the first three are scored.
> Intended approach
> A solution is expected to be a real retrieval-augmented-generation pipeline. The score is deliberately split between retrieval (40 percent) and answer generation (60 percent) so both components must work
> Embed the corpus with a pretrained sentence embedder and index the 645 passage vectors.
> Embed each question with the same embedder and retrieve the top-k passages by similarity; optionally rerank with a cross-encoder or combine with BM25.
> Read and answer with a pretrained language model (Llama, Mistral, Qwen, Flan-T5, or a small extractive QA head finetuned on train.csv) given the question plus the retrieved passages. Prompt it to emit a short entity or place name, not prose.
> Normalise the generated string against the answer_aliases lookup built from train.csv.

Inspiration note: Useful because it converts retrieval/query/evidence behavior into a compact measurable target, a strong pattern for hallucination or retrieval-quality challenges.

## Wikimedia Page Retrieval Challenge
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78yce4wpjqkcyt5mjdq3pdh981jwv2
- DOMAIN exactly as displayed: RAG
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: dominico ranked 1st (leaderboard #38, score —); shivank ranked 3rd (leaderboard #27, score —)

Full challenge description from page:

> Overview
> When humans research a complex topic, they open multiple pages, follow links from one to another, and piece together the answer across sources.
> This challenge asks solvers to do the same: given a research question, retrieve the ordered set of 2–5 documents from a large opaque corpus that together answer it. Many questions require chain-of-retrieval — reading an initial document to discover which subsequent documents are needed. The corpus provides only opaque doc_ids and plaintext — no titles, categories, or structural metadata.
> Questions follow three implicit retrieval patterns (labels are not provided per question):
> Sequential (~38%): Document A must be read to discover Document B exists.
> Bridged (~33%): Documents are connected through context not stated in the question.
> Parallel (~29%): All documents can be found independently from the question.
> Evaluation
> Chain-Aware Precision-Weighted F-score (F-0.5) with an order bonus.
> Set accuracy uses F-0.5 (precision weighted 2x over recall):
> F-0.5 = 1.25 × P × R / (0.25 × P + R)
> Each question has 2–5 ground truth documents. Submitting fewer means lower recall; submitting more tanks precision. The grader does not reject submissions outside this range — it scores them, and F-0.5 handles the penalty naturally.
> Order bonus (chain questions only): Kendall tau over correctly retrieved documents, contributing up to ±20%:
> score = F-0.5 × (1 + 0.25 × tau) / 1.25     # sequential/bridged
> score = F-0.5                                  # parallel
> Final score = mean across all 1,200 test questions. Higher is better.
> Data
> File	Rows	Columns
> corpus.csv	~318K	doc_id, text
> questions_train.csv	300	qid, question, doc_ids
> questions_test.csv	1,200	qid, question
> sample_submission.csv	1,200	qid, doc_ids
> doc_ids are pipe-separated and ordered for chain questions.
> Training questions include ground truth doc_ids. Test questions do not.
> Submission
> CSV with 1,200 rows and columns qid, doc_ids.
> qid,doc_ids
> 849,doc_042871|doc_093102
> 1146,doc_007234|doc_055891|doc_112003
> Every qid from questions_test.csv must appear exactly once — no missing, extra, or duplicate rows
> doc_ids are pipe-separated, ordered by consultation sequence
> Duplicate doc_ids within a question are ignored
> Precision-weighted scoring penalizes over-retrieval

Inspiration note: Useful because it converts retrieval/query/evidence behavior into a compact measurable target, a strong pattern for hallucination or retrieval-quality challenges.

## Shahnameh Retrieval Augmented Question Answering
- Challenge URL: https://drive.google.com/drive/folders/1ZZkNylj8lXYRxrnbSvrxL_oZiUvtvaNr
- Source file: cd.txt
- DOMAIN used for this document: RAG (from Drive domain folder or folder name)
- Status: From Google Drive accepted-challenge collection
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: See description if specified
- Tags: Not shown/captured
- Best/top context found: Google Drive: Drive folder 1 / RAG / Shahnameh Retrieval Augmented Question Answering

Full challenge description from Drive:

> Build a retrieval-augmented question answering system over a corpus of 645 English-language prose passages drawn from a Persian heroic-epic tradition. The corpus is provided in full; no external text is required or relevant. Passages have been chunked, cleaned, and re-indexed for this challenge, and the transliteration scheme, chapter boundaries, and alias sets are specific to the distribution given here.
> Each question asks about an entity, event, relation, or place that appears somewhere in the provided passages. Questions deliberately avoid using the canonical name of the answer where an alternative exists -- a question about a hero might instead refer to him as "the one who killed his own son" or "the wielder of the ox-headed mace". The correct answer must be retrieved from the provided passages and generated in the canonical form used internally by the corpus.
> A good solution must do two things well:
> Retrieve passages relevant to the question, despite the question using epithets, paraphrases, or multi-hop references that do not literally occur in the text.
> Generate a short answer string that matches the canonical character name (or an accepted alias).
> Evaluation
> Each test question is scored on two axes:
> Answer F1 (60%): token-overlap F1 between the predicted answer and the best-matching canonical name or alias, after lowercasing, diacritic stripping, article removal, and punctuation normalization.
> Retrieval Hit@3 (40%): 1.0 if any ground-truth passage appears in the top-3 retrieved passage IDs, else 0.0.
> score = 0.6 * mean(answer_f1) + 0.4 * mean(hit@3)
> Score range: [0.0, 1.0]. A sample submission of constant answers scores around 0.10; perfect answers with perfect retrieval score 1.0.
> Dataset
> The training split (train.csv) exposes 63 fully-labelled questions with answers, accepted aliases, question types, and ground-truth passage IDs.
> The test split (test.csv) contains 147 questions with no answer fields. The corpus (corpus.csv) of 645 passages is shared between train and test.
> Files
> corpus.csv -- 645 passages from the Shahnameh, each tagged with the chapter it came from
> train.csv -- 63 questions with answers, aliases, types, and ground-truth passage IDs
> test.csv -- 147 questions to answer
> sample_submission.csv -- example submission format
> corpus.csv
> passage_id (string): stable identifier, P0000 to P0644
> chapter (string): corpus-internal section label the passage was drawn from
> text (string): the passage text (roughly 1000-1200 characters)
> length (int): character count
> train.csv and test.csv
> id (int): unique question identifier
> question (string): the natural-language question
> answer (string, train only): the canonical answer string
> answer_aliases (JSON list, train only): all accepted answer spellings
> question_type (string, train only): one of relation_*, event_fact, multi_hop, location_object
> ground_truth_passage_ids (JSON list, train only): passage IDs that contain evidence for the answer
> Question types
> relation_* (e.g. relation_father, relation_son, relation_wife, relation_slayer, and similar suffixes) -- direct kinship or action-based relations between entities. The question refers to one entity via an epithet and asks for a related entity.
> event_fact -- deed-based questions ("Who led the revolt against the serpent-shouldered tyrant?") about specific actions in the corpus.
> multi_hop -- two-step reasoning: first identify an unnamed entity by its epithet, then answer a relation or fact about it.
> location_object -- ask for a place, weapon, mount, or artefact.
> Submission
> Submit a CSV with three columns:
> id (int): must match a test.csv id exactly once. Test ids are arbitrary 7-digit integers drawn from the range 1000000-9999999; they are not sequential and do not overlap with train ids.
> predicted_answer (string): your answer for the question
> retrieved_passage_ids (string): pipe-separated list of passage IDs, ordered from most to least relevant. Only the first three are scored.
> Example (the exact id values shown are illustrative — use whatever ids appear in your test.csv):
> id,predicted_answer,retrieved_passage_ids
> 2345678,ExampleName,P0123|P0124|P0098
> 3456789,ExamplePlace,P0050|P0049|P0051
> Requirements:
> Row count must equal the number of test questions (one prediction per question).
> Each id must appear exactly once and must match a test id.
> predicted_answer is compared after lowercasing, article removal, and diacritic stripping.
> retrieved_passage_ids may contain any number of entries, but only the first three are scored.
> Intended approach
> A solution is expected to be a real retrieval-augmented-generation pipeline. The score is deliberately split between retrieval (40 percent) and answer generation (60 percent) so both components must work
> Embed the corpus with a pretrained sentence embedder and index the 645 passage vectors.
> Embed each question with the same embedder and retrieve the top-k passages by similarity; optionally rerank with a cross-encoder or combine with BM25.
> Read and answer with a pretrained language model (Llama, Mistral, Qwen, Flan-T5, or a small extractive QA head finetuned on train.csv) given the question plus the retrieved passages. Prompt it to emit a short entity or place name, not prose.
> Normalise the generated string against the answer_aliases lookup built from train.csv.
> What Not To Use
> Rule-based QA pipelines (hand-written inference rules, manually constructed knowledge graphs, dependency-parse-to-answer matchers, semantic parsers with hand-crafted grammars)
> Hand-coded entity / relation lookup dictionaries
> Regex or template-to-answer rule sets
> Pretrained Shahnameh or Persian-literature QA / manuscript models
> Web search, encyclopedia, or knowledge-graph APIs (Google Search, Wikipedia API, Wolfram Alpha, scholarly-database lookups)
> Constrained decoding that restricts the reader's output to a pre-enumerated answer vocabulary
> Ready to Solve
> This challenge has been reviewed and approved. Start solving to submit your solution!
> Start New Solution
> Submission Credits
> 6/6
> Learn more about submission credits
> 30/10
> solver slots
> Closing soon
> Solver threshold reached — prize pool is active and closing countdown has started. Submit before the deadline! At 8 solvers above AI, lockdown begins (+ 2 wildcard slots).
> Closing in 9m
> Submit your solution before the deadline. Payouts are processed after the challenge closes.
> Creator reward for this problem
> $
> 400
> –
> 500

Inspiration note: Useful as a retrieval-grounded task pattern with explicit context selection, answer scoring, and a metric-friendly prediction target.

## Palimpsest-CV-Adversarial Multi Task Resume Intelligence
- Challenge URL: https://drive.google.com/drive/folders/1xuoZsmDhjjl2Uy9Xmqdkq5T4Dl6cvjIZ
- Source file: challenge_desc.txt
- DOMAIN used for this document: RAG (from Drive domain folder or folder name)
- Status: From Google Drive accepted-challenge collection
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: See description if specified
- Tags: Not shown/captured
- Best/top context found: Google Drive: Drive folder 1 / RAG / Palimpsest-CV-Adversarial Multi Task Resume Intelligence

Full challenge description from Drive:

> Palimpsest-CV: Adversarial Multi-Task Resume Intelligence under Longitudinal Drift
> Overview
> Modern automated resume review systems are increasingly responsible for who gets hired, yet they are evaluated almost exclusively on static, single-task benchmarks (e.g., "does CV match job posting?"). Real hiring pipelines demand far more: matching candidates to roles, flagging fabricated claims, answering specific factual questions about a candidate's history, detecting AI-generated content, producing structured human-readable summaries — and, crucially, explaining how a suspected fabrication was performed and reconstructing the honest original underneath it. A palimpsest is a manuscript from which the original writing has been scraped off and overwritten; this challenge is named for a corresponding modeling target that, to our knowledge, has no precedent in any public benchmark: given a rewritten CV, recover the scraped-off original. The five standard tasks listed above plus this sixth Palimpsest Recovery task are the challenge's six graded subtasks.
> This challenge asks an agent to build one foundational representation of a resume that powers six heterogeneous downstream tasks simultaneously, graded as a single composite score. The underlying dataset is a purely synthetic longitudinal corpus (2010-01-01 through 2026-06-30) of ~200,000 candidates, 800 synthetic companies with acquisition/bankruptcy timelines, 200 canonical job roles whose semantic meaning drifts over time, and a taxonomy of ~2,500 skills with emergence, renaming, and obsolescence events. Adversarial "twin" CVs differ from their honest counterparts by a single fabricated edit whose exact field and exact honest value are recorded in the ground truth; Palimpsest Recovery asks agents to re-derive both. A subset of CVs are machine-generated using one of six distinct "style signatures" — but only five are present in training. Five entire industries (aerospace, biotech, climate-tech, maritime, space) are held out of train and appear only at test time, testing true zero-shot industry generalization. A small percentage of CVs contain poison skills — plausible-looking inventions that do not exist in the canonical taxonomy — and the agent must not reward them.
> The private test set is drawn from 2025–2026 only, so any agent that memorizes skill–role associations from prior epochs will systematically under-perform when skill semantics have drifted. Rule-based systems, keyword matchers, and simple fine-tuned classifiers all fail on at least one sub-task by construction. The challenge is designed to reward agents that (a) build a shared representation across tasks, (b) use external tables (companies.csv, skills.csv, career_events.csv) as retrieval context for RAG and for Palimpsest Recovery, and (c) validate with temporal and subgroup-aware splits during training.
> Evaluation
> Submissions are scored by a composite score in [0, 100] (higher is better), equal to the unweighted mean of six subtask scores, each normalized to [0, 100]:
> 1. Role matching (ranking) — metric: 100 × NDCG@10 over 200 canonical roles. Range: [0, 100].
> 2. Fabrication detection — metric: 100 × F1 on twin-vs-honest binary. Range: [0, 100].
> 3. RAG question answering — metric: 100 × token-F1 (SQuAD-style, per-answer mean). Range: [0, 100].
> 4. AI-authorship detection — metric: 100 × AUC-ROC on AI-vs-human (incl. unseen signature). Range: [0, 100].
> 5. Review generation — metric: 100 × macro-F1 across strengths/gaps/red_flags keyword sets. Range: [0, 100].
> 6. Palimpsest Recovery (NEW — no prior benchmark) — jointly predict, per row: edit_type ∈ {none, company, tenure, skill-date, title, cross-ref}, the single edit_target field/event that was rewritten (e.g., "company_id@event_2", "skills_text", or "responsibilities_text@event_1"; "none" for honest rows), and honest_value — the string the fabricator overwrote, restored to its honest form (empty string for honest rows). The cross-ref edit type specifically targets cross-candidate references in responsibilities_text — the fabricator rewrote "collaborated with candidate_N" to point at a different candidate whose own CV disagrees, so reconstructing the honest candidate_N requires multi-document reasoning over the full around 200 k-candidate corpus, not just intra-document features. The per-row score is:
> honest rows: 1.0 if edit_type == "none" (no false alarm), else 0.0.
> twin rows: (1/3) × 𝟙[edit_type correct] + (1/3) × 𝟙[edit_target correct] + (1/3) × token-F1(honest_value, gold). Subtask score = 100 × mean-per-row. Honest and twin rows are weighted by their natural test frequency (30% twins in private test).
> If a subtask submission is missing for a row, that subtask defaults to its chance baseline (0 for NDCG, 0.5 for AUC, empty string for QA → 0 token-F1, "none" / empty for Palimpsest Recovery → honest-only credit). The submission must not crash the grader; malformed rows are skipped with a logged warning.
> def composite_score(ndcg10, fab_f1, rag_f1, ai_auc, review_f1, recovery_score):
> return 100.0 * (ndcg10 + fab_f1 + rag_f1 + ai_auc + review_f1 + recovery_score) / 6.0
> Palimpsest Recovery is graded from twin_manifest.csv, which records twin_id, honest_id, edit_type, edit_target, and honest_value for every fabricated CV. twin_manifest.csv is private — it lives in raw/ for auditability and is joined into private/answers.csv by prepare.py, but never copied to public/. See DO_NOT_USE.md for the explicit prohibition on re-deriving it.
> Dataset
> The prepared dataset lives in dataset/public/ and dataset/private/:
> dataset/
> ├── public/
> │   ├── train.csv                  #  all 5 label columns present
> │   ├── test.csv                   #  no label columns (same row set as private/answers.csv)
> │   ├── companies.csv              #  synthetic companies: id, name, birth_year, death_year, parent_id, industry, hq_region
> │   ├── skills.csv                 #  skills: skill_id, canonical_name, aliases, emerged_year, obsolete_year, family
> │   ├── roles.csv                  #  canonical roles: role_id, name, description, year_introduced, seniority_axis
> │   ├── career_events.csv          # rows: candidate_id, company_id, role_id, start_date, end_date, responsibilities_text
> │   ├── rag_questions.csv          # 1 question per test candidate: question_id, candidate_id, question_text, question_template_id
> │   └── sample_submission.csv      # one row per test candidate, chance-baseline values (see example below)
> └── private/
> └── answers.csv                # ground-truth labels for all 5 subtasks, keyed on candidate_id
> train.csv / test.csv columns
> Shared columns:
> candidate_id (int64) — unique candidate identifier (primary key).
> created_date (date YYYY-MM-DD) — date the CV was authored.
> region (string) — one of 50 synthetic regions.
> age_bucket (string) — one of "<25", "25-34", "35-44", "45-54", "55+".
> education_level (string) — one of "high_school", "bachelor", "master", "phd", "other".
> summary_text (string) — free-form narrative summary (200–600 chars).
> skills_text (string) — comma-separated declared skills (may contain poison skills).
> portfolio_projects_count (int32) — declared projects.
> portfolio_publications_count (int32) — declared publications.
> portfolio_patents_count (int32) — declared patents.
> industry (string) — primary industry of most-recent job.
> language_mix (string) — "en" or "en+<lang>" for code-switched CVs.
> Label columns (train only):
> true_role_ids (string, JSON list[int]) — top-10 ground-truth role IDs in rank order.
> fabrication_flag (int32) — 0 honest, 1 adversarial twin.
> rag_answer (string) — ground-truth answer to this CV's RAG question.
> ai_signature_id (int32) — -1 human, else 0..5 signature (train has 0..4).
> is_ai (int32) — 0 human, 1 AI-generated.
> review_strengths (string, JSON list[str]) — canonical keyword set.
> review_gaps (string, JSON list[str]) — canonical keyword set.
> review_red_flags (string, JSON list[str]) — canonical keyword set.
> edit_type (string) — gold edit class ∈ {"none", "company", "tenure", "skill-date", "title", "cross-ref"}. "none" for honest rows. (Palimpsest Recovery supervision.)
> edit_target (string) — gold target field (e.g., "company_id@event_2"); "none" for honest rows. (Palimpsest Recovery supervision.)
> honest_value (string) — gold original value before the fabricator's edit; "" for honest rows. (Palimpsest Recovery supervision.)
> Career events for each candidate must be joined via candidate_id. Questions for test candidates are in rag_questions.csv. No rag_questions row is issued for train candidates — the training label rag_answer is the gold answer to a question auto-generated from that candidate's career_events rows at dataset-build time, so during training the agent sees the answer but not the question text; at inference the agent sees the question text (from rag_questions.csv) but not the answer.
> career_events.csv columns
> event_id (int64) — primary key for the event row.
> candidate_id (int64) — foreign key to train.csv / test.csv.
> company_id (int64) — foreign key to companies.csv.
> role_id (int64) — foreign key to roles.csv, range [0, 199].
> start_date (date YYYY-MM-DD) — event start date.
> end_date (date YYYY-MM-DD) — event end date. The sentinel 2999-01-01 means "current employment".
> responsibilities_text (string) — templated paragraph describing the role's responsibilities. May reference other candidates by ID ("collaborated with candidate_128473"), which is required for multi-hop RAG.
> declared_title (string) — free-form title string as it appears on the CV. May differ stylistically from roles.name (e.g., "Senior ML Engineer II" vs. canonical "SOFTWARE_ENGINEER").
> claimed_impact_value (float) — quantitative impact claim (revenue, user count, percentage). Sometimes inflated in twin CVs — cross-check against company size / tenure is a fabrication signal.
> claimed_impact_unit (string) — "usd", "users", or "pct".
> companies.csv columns
> company_id (int64) — primary key.
> name (string) — synthetic company name (e.g., "Flowtrain Systems").
> birth_year (int32) — year the company was founded, in [1990, 2024].
> death_year (int32) — year the company was dissolved, or -1 if still active through 2026.
> parent_id (int64) — company ID of the acquirer, or -1 if not acquired. Acquisition resolution is required for several RAG templates.
> parent_acquired_year (int32) — year of acquisition, or -1.
> industry (string) — one of 40 synthetic industries. Held-out industries appear only in test.
> hq_region (string) — one of 50 synthetic regions (e.g., "REG_NA_01").
> market_cap_tier (string) — "micro", "small", "mid", "large", or "mega", as of 2026 (or death year).
> skills.csv columns
> skill_id (int64) — primary key.
> canonical_name (string) — normalized skill name (e.g., "react", "prompt-engineering"). Poison skills are NOT in this file — the taxonomy is the ground-truth whitelist.
> aliases (JSON list[str]) — alternate spellings / case variants. Parse with json.loads.
> emerged_year (int32) — year this skill first plausibly existed in the synthetic world.
> renamed_to_skill_id (int64) — ID of the post-rename skill, or -1 if never renamed.
> rename_year (int32) — year of the rename, or -1.
> obsolete_year (int32) — year the skill became obsolete, or -1 if still current.
> family (string) — one of ~30 high-level families (e.g., "ML_FRAMEWORK", "WEB_FRONTEND", "STATS"). Used by the review_strengths keyword set.
> roles.csv columns
> role_id (int64) — primary key, range [0, 199]. This is the ID used in role_top10.
> name (string) — canonical role name (e.g., "SOFTWARE_ENGINEER", "PROMPT_ENGINEER").
> description (string) — one-sentence description of the role.
> year_introduced (int32) — year before which this role did not exist as a titled position (PROMPT_ENGINEER is 2023; FLASH_DEVELOPER is 2003 and obsolete after 2015).
> seniority_axis (string) — "ic", "staff", "manager", "director", or "exec".
> industry_affinity (JSON list[str]) — industries where this role is most common. Parse with json.loads.
> rag_questions.csv columns (test only)
> question_id (int64) — primary key.
> candidate_id (int64) — foreign key to test.csv; exactly one row per test candidate.
> question_text (string) — natural-language question requiring a multi-hop join over career_events.csv and companies.csv.
> question_template_id (int32) — internal template ID (0–4). Provided for diagnostics; not required for scoring.
> Submission
> Submit a single submission.csv with exactly one row per candidate_id in test.csv. Columns:
> candidate_id (int64) — must match a row in test.csv.
> role_top10 (string) — JSON-encoded list of 10 role IDs, ordered by descending predicted relevance. Example: "[12, 44, 3, 87, ...]".
> fabrication_score (float) — probability in [0, 1] that the CV is a fabricated twin.
> rag_answer (string) — free-form short answer (≤ 200 chars) to this CV's question from rag_questions.csv.
> ai_score (float) — probability in [0, 1] that the CV is AI-generated.
> review_strengths (string) — JSON list of ≤ 10 strings (canonical keywords).
> review_gaps (string) — JSON list of ≤ 10 strings.
> review_red_flags (string) — JSON list of ≤ 10 strings.
> edit_type (string) — one of "none", "company", "tenure", "skill-date", "title", "cross-ref". "none" means the CV is predicted honest. "cross-ref" indicates the agent believes a "collaborated with candidate_N" reference in responsibilities_text was rewritten to point at a non-overlapping candidate — this is the multi-document primitive and is the hardest class to get right. (Palimpsest Recovery output.)
> edit_target (string) — the rewritten field, formatted as "<column>@event_<k>" where k is the 0-indexed event position in the candidate's career_events sorted by start_date, OR "skills_text" for the skill-date edit type, OR "none" for predicted-honest rows. Examples: "company_id@event_2", "end_date@event_0", "role_id@event_1", "skills_text", "none". (Palimpsest Recovery output.)
> honest_value (string) — the agent's reconstruction of the overwritten original value as a string. Empty string for predicted-honest rows. For company edits, this is the name of the honest company (looked up from companies.csv, not the raw company_id). For tenure edits, an ISO date ("YYYY-MM-DD"). For skill-date edits, the canonical name of the poison skill that should be removed. For title edits, the honest declared_title string. (Palimpsest Recovery output.)
> Requirements:
> Must contain exactly len(test.csv) rows.
> Include header row.
> role_top10 must be a JSON list of length 10, with integer role IDs in [0, 199] (duplicates allowed but heavily penalized by NDCG).
> String list columns must parse as valid JSON via json.loads. Rows that fail to parse score 0 on that subtask but do not crash the grader.
> Missing rows are scored at the chance baseline for every subtask and count against the total length check.
> Example rows
> Header and two example rows (CSV-formatted, with the JSON string columns properly json.dumps-encoded and quoted). The first row is an honest candidate; the second is a detected fabricated twin where the agent localized a tenure-inflation edit on the candidate's first job and predicts the honest end-date was 2019-08-01:
> candidate_id,role_top10,fabrication_score,rag_answer,ai_score,review_strengths,review_gaps,review_red_flags,edit_type,edit_target,honest_value
> 184201,"[12, 44, 3, 87, 102, 19, 56, 71, 188, 140]",0.08,"REG_EU_14",0.62,"[""ML_FRAMEWORK"", ""STATS"", ""CLOUD""]","[""DATABASE""]","[]","none","none",""
> 184202,"[71, 56, 3, 12, 102, 19, 44, 87, 188, 140]",0.93,"mid",0.04,"[""WEB_FRONTEND""]","[""STATS"", ""CLOUD""]","[""tenure-inflation""]","tenure","end_date@event_0","2019-08-01"
> The sample_submission.csv shipped in public/ follows the same schema with chance-baseline values (role_top10 = "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]", fabrication_score = 0.5, rag_answer = "", ai_score = 0.5, each review list "[]", edit_type = "none", edit_target = "none", honest_value = ""). Copy it as a starting template and overwrite with your predictions.
> Config
> See config.yaml:
> name: Palimpsest-CV
> difficulty: hard
> domain: multimodal   # tabular + text with retrieval components
> grade:
> direction: maximize
> minimum: 0.0
> maximum: 100.0
> Leakage & Rule-Based Resistance
> Temporal split prevents agents from seeing 2025–2026 data during training.
> Industry holdout prevents memorization of industry-role priors that would trivialize role matching.
> Unseen AI signature prevents fingerprint classifiers from generalizing trivially.
> Twin pairs in train expose the fabrication-detection concept, but the test set doubles the twin density and perturbs along different edit axes (company-fabrication in train, date-inflation and cross-field contradictions in test).
> Skills taxonomy is versioned: the emerged_year and obsolete_year columns are only correct when joined against companies.csv properly — agents that ignore the taxonomy will reward poison skills.
> RAG answers are never substrings of summary_text alone; they always require joining career_events.csv, sometimes further joined on companies.csv (e.g., "the company's HQ region").
> No label column of the test set is derivable from a deterministic rule on a single input column.
> What Not To Use
> Palimpsest-CV — What Not To Use
> This document lists techniques, libraries, and practices that are prohibited or grounds for rejection on this challenge. It complements RUBRICS.md (positive criteria) with negative criteria. Each item notes whether it is an AUTO-REJECT (solution will not be graded), a REJECT (solution will be graded but marked invalid in the final review), or a STRONGLY DISCOURAGED practice (the grader does not block it, but reviewers will flag it and it typically fails at least one rubric).
> 1. Data leakage — AUTO-REJECT
> These are hard leakage violations. Any submission found to use them is disqualified regardless of its composite score.
> Do not read dataset/private/answers.csv under any circumstance — not for training, not for validation, not for "sanity checking," not via an intermediate pickle, not by re-ordering rows to match it. The private answers are the graded targets.
> Do not fit any supervised preprocessor on test labels. TF-IDF vocabularies, tokenizers, scalers, PCA bases, retrieval indexes, and LSH buckets may be fit on the text of test.csv (unsupervised, test text is provided) but never on any column from answers.csv.
> Do not use ai_signature_id as a feature for the is_ai subtask. The column deterministically encodes the label (is_ai == int(ai_signature_id != -1)). This is explicitly a trap — training on it produces >0.99 validation AUC and <0.6 test AUC because signature 5 is absent from training.
> Do not reconstruct fabrication_flag, edit_type, edit_target, or honest_value from twin_manifest.csv at inference time. The manifest is present in raw/ for auditability only; it is not shipped to public/, and no solution should attempt to scrape, read, or re-derive it from the file system. This prohibition applies to all six Palimpsest Recovery label columns — an auto-reject if a solution reads twin_manifest.csv from any path.
> Do not perform a random train/validation split. The private test is drawn exclusively from 2025–2026 and from five held-out industries. A uniformly shuffled split leaks future information and inflates validation metrics. Use a temporal + subgroup validation split.
> Do not concatenate train + test + answers for any fit step. Concatenating unlabeled train + test text for an unsupervised preprocessor is allowed by; concatenating anything with labels from answers.csv is not.
> 2. External services and commercial LLM APIs — AUTO-REJECT
> This is a closed-data, closed-budget benchmark. Solutions must run entirely within the Kaggle Python Docker image on a single machine in ≤ 30 minutes with ≤ 24 GB VRAM. Reaching out to external services defeats the point.
> No calls to commercial LLM APIs (OpenAI, Anthropic, Google Gemini, Cohere, Mistral-hosted, xAI, Perplexity, or any hosted inference endpoint). This includes the "reasoning" endpoints, requests.post to any chat completion URL, and SDK wrappers for them.
> No calls to embedding APIs (OpenAI text-embedding-3-*, Cohere embeddings, Voyage, Vertex AI embeddings, etc.).
> No web scraping at train or inference time — no requests.get, no urllib, no httpx, no Playwright/Selenium. Solutions must operate on the files shipped in raw/ and dataset/.
> No external search APIs (Brave, Google, Bing, SerpAPI, You.com, Tavily).
> No managed vector stores (Pinecone, Weaviate Cloud, Qdrant Cloud, Chroma Cloud). A local FAISS / HNSW / numpy index fit on the training corpus is fine.
> No downloading pretrained weights at runtime from Hugging Face Hub, GitHub releases, S3, or arbitrary URLs. Any pretrained model used must be available inside the Kaggle Python Docker image or pre-staged as a dataset attachment declared in metadata.yaml.
> 3. External data — AUTO-REJECT
> The benchmark is purely synthetic. Mixing in real-world resume or company data defeats the leakage-resistance design and raises copyright issues.
> No public resume datasets — no Kaggle "resume parser" datasets, no HR corpora, no Indeed/Monster/LinkedIn/Handshake scrapes, no LHR/ESCO occupational ontologies. Every canonical role, skill, and company in this challenge is synthetic.
> No real company taxonomies — no Crunchbase dumps, no NAICS/SIC codes, no Fortune-500 lists, no S&P industry maps. The 800 synthetic companies have fictional names by design.
> No real skill taxonomies — no O*NET, no ESCO, no Stack Overflow tag corpora, no GitHub topic graphs. Joining against any of these leaks real-world priors that do not match the synthetic world's drift pattern.
> No pretrained resume-parsers (e.g., Sovren, HireAbility, RChilli, pyresparser, HuggingFace resume-ner models). Their priors are from real CVs and will incorrectly reward real-world skills over synthetic ones.
> No paid datasets of any kind. If a library's fetch_* function makes a network call on first use, either vendor the data into the submission or don't use the function.
> 4. Prohibited libraries and frameworks — REJECT
> Some libraries technically run inside the Docker image but are incompatible with the challenge's synthetic-world design or with the reproducibility requirement.
> Scraping libraries (scrapy, playwright, selenium, beautifulsoup4 used for live HTTP, pyppeteer). Note: beautifulsoup4 for offline parsing of shipped files is fine.
> Non-deterministic retrieval services (pinecone-client, weaviate-client, qdrant-client in "cloud" mode). Local-mode clients that persist an index to disk within the submission are allowed.
> Proprietary or closed-source inference runtimes (openai, anthropic, google-generativeai, cohere, mistralai SDKs when used to hit the hosted API — they're effectively wrappers around the banned endpoints above).
> Autograd-unfriendly symbolic engines used as ML models (sympy-based classifiers, z3-solver as a ranker). Symbolic use for feature engineering is fine; using them as the primary model is not.
> Any library not in the Kaggle Python Docker image unless you vendor it into the submission and it runs fully offline. Verify with pip freeze inside the image before submitting.
> 5. Anti-patterns specific to this challenge — STRONGLY DISCOURAGED
> These are not automatic rejections, but each one triggers at least one failing and will cap the composite score.
> Training is_ai as a 5-way classifier over signatures 0–4. Signature 5 is unseen in training. The classifier will confidently mis-map signature 5 to one of the training classes, destroying AUC. Use binary is_ai or an anomaly/open-set score.
> Embedding skills_text as raw free-form tokens without grounding to skills.csv. This rewards poison skills (3% of honest CVs, 10% of twin CVs).
> Blind concatenation of skills across a career history without emerged_year vs start_date consistency checks. Cross-field contradictions are a gold fabrication signal; ignoring them both inflates role-match scores and misses twin edits.
> Relying solely on summary_text + skills_text. RAG questions require multi-hop joins across career_events and companies.
> Six independent heads with no shared representation. The 30-minute budget makes this impractical at 200k candidates and 3M events; rubric #6 requires at least two subtasks share a base encoder.
> Training six separate copies of the same model on identical data. Different from the above — this is just wasteful and exceeds the compute budget.
> Treating held-out industries as noise and dropping them from the test submission. These rows must be scored. Missing rows default to the chance baseline and cost you NDCG@10 on exactly the subgroup the rubric cares about.
> Optimizing for a single subtask. Composite is a mean of six; a model that wins NDCG@10 alone caps at 100/6 ≈ 16.7/100.
> Dropping code-switched (language_mix != "en") rows from training. They are 10% of the data and appear at the same rate in test.
> Using uniformly sampled validation batches over the full train time range. Validation should respect the time ordering to be a faithful proxy for 2025–2026 test performance. Rubric #1.
> Always predicting edit_type = "none" for Palimpsest Recovery. This is the chance baseline — it gets full credit on honest rows and zero on the 30% of private-test rows that are twins. It caps the subtask at ~70 before zero-for-twins dragging it to ~47, and caps composite at about 75/6 ≈ 12.5 from this subtask alone. A competent solution predicts a non-"none" edit for at least the rows where fabrication_score > 0.5, and grounds honest_value in the candidate's own career_events rather than hallucinating.
> Predicting edit_target with an off-by-one event_k. Event positions in edit_target (e.g., "company_id@event_2") are defined by sorting the candidate's career_events rows ascending by start_date and 0-indexing. Using the raw CSV order, or 1-indexing, costs the whole edit_target credit on every twin row even when the edit type is correct.
> Pasting fabrication_score into edit_type or vice-versa. They are independent outputs — fabrication_score is a float in [0, 1], edit_type is a string from a 6-value vocabulary. Mixing them up is silently accepted by the grader (string coerces to "none") and costs both subtasks.
> Ignoring cross-ref as a rare class. cross-ref is ~15% of all twin rows. An agent that never predicts cross-ref (e.g., a 4-way classifier trained on the other edit types) forfeits roughly 0.15 × 30% × 100 / 3 ≈ 1.5 composite points on the Palimpsest Recovery subtask. More importantly: recovering the honest candidate_N requires a retrieval index over the entire 200 k-candidate corpus, not just the candidate's own career_events rows. An agent that scopes Palimpsest Recovery to intra-document features alone cannot score above zero on cross-ref twins.
> Reconstructing cross-ref honest_value by copying the rewritten mention. The rewritten "collaborated with candidate_N" points at the wrong candidate by construction; the grader's honest_value is the original candidate ID that was overwritten. An agent that outputs the rewritten ID scores 0 on the honest_value component of that row.
> Quick checklist before submitting
> A well-behaved submission satisfies all of the following. Run through this list before you submit.
> My solution never opens dataset/private/answers.csv.
> My validation split is time-ordered and holds out at least one entire industry.
> My is_ai predictor does not see ai_signature_id at any training step.
> My skills_text pipeline is grounded against skills.csv — poison skills do not propagate into features.
> My career-event features respect skills.emerged_year vs start_date consistency.
> I do not hit any external API, download any URL, or use any external dataset.
> My submission.csv has exactly len(test.csv) rows, all columns present, list columns are json.dumps-encoded.
> My solution runs in under 30 minutes on the reference machine.
> Running my solution twice on the same seed produces near-identical scores (within 1.0 composite point).

Inspiration note: Useful as a retrieval-grounded task pattern with explicit context selection, answer scoring, and a metric-friendly prediction target.

## Synthetic Temporal Evidence Verification
- Challenge URL: https://drive.google.com/drive/folders/1vheRLh-QByCGP3DZQ92-TwhHMk3tL80r
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: RAG (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: Accepted/approved example from shared Drive folder
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: Not shown/captured
- Tags: Not shown/captured
- Best/top context found: Synthetic Temporal Evidence Verification from shared Google Drive folder

Full challenge description from Drive:

> # Challenge creation form — fill-in
> Tie this challenge to the **accepted dataset**: Synthetic Temporal Knowledge Base With Source Credibility Dynamics.
> ---
> ## 1) Difficulty
> **Select:** **Hard**
> ---
> ## 2) Challenge Title
> ```
> Synthetic Temporal Evidence Verification
> ```
> ---
> ## 3) Problem Description
> # Synthetic Temporal Evidence Verification
> ## Overview
> This is a **RAG** challenge requiring **claim verification against a temporal knowledge base with dynamic source credibility, contradictions, retractions, and adversarial sources**. The problem models a scenario where factual claims must be verified using a corpus of dated documents from multiple sources, but sources disagree, some sources are unreliable, corrections may themselves be wrong, and the evidence available depends on a temporal cutoff.
> The knowledge base contains 600 anonymized documents spanning the years 2010–2025, authored by 30 coded sources across 8 topic categories. Documents describe events, people, and locations in a completely fictional domain — all entity names are opaque coded identifiers (e.g., `LOC-007`, `PER-012`, `EVT-003`), so no pre-trained world knowledge can help. Some documents explicitly correct or retract earlier documents. Sources have hidden topic-dependent credibility that changes over time.
> For each claim, an "as-of" year is specified. Only documents published in or before that year are admissible as evidence. The task is to predict the verification verdict: one of 4 coded classes representing the claim's truth status given the available temporal evidence.
> **What makes this problem uniquely challenging:**
> - **Topic-dependent source credibility**: a source may be highly reliable on one topic but consistently wrong on another. Source reliability cannot be assessed globally — it must be estimated per topic from training data patterns.
> - **Temporal credibility decay**: source reliability changes over time. A source accurate in early years may become unreliable later (or vice versa). The "as-of" date determines both which documents are visible AND the effective credibility of each source at that time.
> - **Temporal traps**: later documents are NOT always more reliable. Some "corrections" introduce new errors that are subsequently re-corrected by even later documents. Naive "trust the newest" strategies fail.
> - **Adversarial sources**: approximately 5 sources have high apparent credibility but periodically inject factual errors. These sources appear trustworthy across most documents, making their errors hard to detect.
> - **Copycat sources**: approximately 15% of sources replicate content from a hidden "parent" source. When multiple sources agree, it may reflect genuine consensus OR correlated noise from a single underlying source.
> - **Sparse evidence**: approximately 10% of claims have 0–2 relevant documents, forcing verification under extreme uncertainty.
> - **Multi-step reasoning**: verification requires retrieving relevant documents by matching topic and entity references, filtering by the as-of date, assessing source credibility, resolving contradictions, and producing a final verdict — a multi-layer reasoning chain.
> - **Irreducible noise**: ~12% of verdicts are randomly assigned, capping theoretical Macro F1 at approximately 0.88.
> Your task: for each test claim, given the claim text, its as-of year, and the full knowledge base, predict the verification verdict.
> ## Evaluation
> Submissions are scored using **Macro F1** across the following 4 verdict classes:
> | Code | Meaning |
> |------|---------|
> | V-A | Claim is supported by the available evidence |
> | V-B | Claim is refuted by the available evidence |
> | V-C | Claim is partially true (some aspects supported, others not) |
> | V-D | Insufficient evidence to determine the claim's truth status |
> Macro F1 computes the F1 score for each of the 4 classes independently and averages them, giving equal weight to minority classes. **Higher is better.** Minimum: 0.0, Maximum: 1.0.
> ## Dataset
> - `knowledge_base.csv` — 600 documents: document_id (int), year (int, 2010–2025), source_name (string, coded source e.g. SRC-007), topic (string, coded category e.g. CAT-03), location (string, coded e.g. LOC-012), person (string, coded e.g. PER-005), event (string, coded e.g. EVT-009), fact_number (int), text (string, full document content with coded entity references), relevance_score (float), confidence_index (float)
> - `train_claims.csv` — 3,900 training claims: claim_id (int), claim_text (string, the factual assertion with coded entity references), as_of_year (int), verdict (string, one of V-A / V-B / V-C / V-D)
> - `test_claims.csv` — 1,300 test claims: claim_id (int), claim_text (string), as_of_year (int) — verdict withheld
> - `sample_submission.csv` — 1,300 rows: claim_id (int), verdict (string, baseline constant prediction). Shows the required submission format.
> ### Feature Details
> | Column | Type | Description |
> |--------|------|-------------|
> | document_id | int | Unique document identifier |
> | year | int | Document publication year (2010–2025) |
> | source_name | string | Coded source identifier (SRC-000 through SRC-029) |
> | topic | string | Coded topic category (CAT-00 through CAT-07) |
> | location | string | Coded location (LOC-000 through LOC-015) |
> | person | string | Coded person (PER-000 through PER-015) |
> | event | string | Coded event (EVT-000 through EVT-015) |
> | fact_number | int | Reference number cited in the document |
> | text | string | Full free-text document content with all entities replaced by coded identifiers |
> | relevance_score | float | Numeric document feature (0–1 range) |
> | confidence_index | float | Numeric document feature (0–1 range) |
> | claim_id | int | Unique claim identifier |
> | claim_text | string | The factual assertion to verify, with coded entity references |
> | as_of_year | int | Temporal cutoff year — only documents published on or before this year are admissible |
> | verdict | string | Coded verification verdict (one of V-A, V-B, V-C, V-D) — train only |
> ## Submission
> Submit a CSV file with the following format:
> | Column | Type | Description |
> |--------|------|-------------|
> | claim_id | int | Claim identifier from test_claims.csv |
> | verdict | string | Predicted verdict code (one of: V-A, V-B, V-C, V-D) |
> **Requirements:**
> - Must contain exactly 1,300 rows (one per test claim).
> - Include a header row.
> - Each verdict value must be one of the 4 valid codes: `V-A`, `V-B`, `V-C`, `V-D`.
> **Example of a correctly formatted submission file:**
> claim_id,verdict
> 5,V-A
> 12,V-C
> 18,V-B
> 23,V-D
> 31,V-A
> 42,V-C
> 57,V-D
> 68,V-B
> ---
> ## 4) Tags
> **Select:** `text`, `feature-engineering`
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
> if "claim_id" not in submission.columns or "verdict" not in submission.columns:
> return 0.0
> if submission["claim_id"].duplicated().any():
> return 0.0
> if answers["claim_id"].duplicated().any():
> return 0.0
> if set(submission["claim_id"]) != set(answers["claim_id"]) or len(submission) != len(answers):
> return 0.0
> merged = answers.merge(
> submission, on="claim_id", how="left", suffixes=("_true", "_pred")
> )
> if len(merged) == 0:
> return 0.0
> col_true = "verdict_true" if "verdict_true" in merged.columns else "verdict"
> col_pred = "verdict_pred" if "verdict_pred" in merged.columns else "verdict"
> if merged[col_pred].isna().any():
> return 0.0
> y_true = merged[col_true].astype(str).str.strip()
> y_pred = merged[col_pred].astype(str).str.strip()
> all_classes = sorted(set(y_true.tolist()))
> f1_scores = []
> for cls in all_classes:
> tp = ((y_pred == cls) & (y_true == cls)).sum()
> fp = ((y_pred == cls) & (y_true != cls)).sum()
> fn = ((y_pred != cls) & (y_true == cls)).sum()
> precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
> recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
> if precision + recall > 0:
> f1 = 2 * precision * recall / (precision + recall)
> else:
> f1 = 0.0
> f1_scores.append(f1)
> macro_f1 = float(np.mean(f1_scores)) if f1_scores else 0.0
> if np.isnan(macro_f1):
> return 0.0
> return macro_f1
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
> kb = pd.read_csv(raw / "knowledge_base.csv")
> claims = pd.read_csv(raw / "claims.csv")
> rng = _rnd.Random(299792458)
> np_rng = np.random.RandomState(65)
> unique_sources = sorted(kb["source_name"].unique().tolist())
> source_codes = [f"SRC-{i:03d}" for i in range(len(unique_sources))]
> rng.shuffle(source_codes)
> source_map = {unique_sources[i]: source_codes[i] for i in range(len(unique_sources))}
> kb["source_name"] = kb["source_name"].map(source_map)
> unique_locs = sorted(kb["location"].unique().tolist())
> loc_codes = [f"LOC-{i:03d}" for i in range(len(unique_locs))]
> rng.shuffle(loc_codes)
> loc_map = {unique_locs[i]: loc_codes[i] for i in range(len(unique_locs))}
> kb["location"] = kb["location"].map(loc_map)
> unique_people = sorted(kb["person"].unique().tolist())
> person_codes = [f"PER-{i:03d}" for i in range(len(unique_people))]
> rng.shuffle(person_codes)
> person_map = {unique_people[i]: person_codes[i] for i in range(len(unique_people))}
> kb["person"] = kb["person"].map(person_map)
> unique_events = sorted(kb["event"].unique().tolist())
> event_codes = [f"EVT-{i:03d}" for i in range(len(unique_events))]
> rng.shuffle(event_codes)
> event_map = {unique_events[i]: event_codes[i] for i in range(len(unique_events))}
> kb["event"] = kb["event"].map(event_map)
> unique_topics = sorted(kb["topic"].unique().tolist())
> topic_codes = [f"CAT-{i:02d}" for i in range(len(unique_topics))]
> rng.shuffle(topic_codes)
> topic_map = {unique_topics[i]: topic_codes[i] for i in range(len(unique_topics))}
> kb["topic"] = kb["topic"].map(topic_map)
> def _obfuscate_text(text):
> result = str(text)
> for orig, code in sorted(source_map.items(), key=lambda x: -len(x[0])):
> result = result.replace(orig, code)
> for orig, code in sorted(loc_map.items(), key=lambda x: -len(x[0])):
> result = result.replace(orig, code)
> for orig, code in sorted(person_map.items(), key=lambda x: -len(x[0])):
> result = result.replace(orig, code)
> for orig, code in sorted(event_map.items(), key=lambda x: -len(x[0])):
> result = result.replace(orig, code)
> for orig, code in sorted(topic_map.items(), key=lambda x: -len(x[0])):
> result = result.replace(orig, code)
> return result
> kb["text"] = kb["text"].apply(_obfuscate_text)
> claims["claim_text"] = claims["claim_text"].apply(_obfuscate_text)
> verdict_map = {
> "SUPPORTED": "V-A",
> "REFUTED": "V-B",
> "PARTIALLY_TRUE": "V-C",
> "INSUFFICIENT_EVIDENCE": "V-D",
> }
> claims["verdict"] = claims["verdict"].map(verdict_map)
> kb = kb.rename(columns={"doc_id": "document_id"})
> doc_ids = sorted(kb["document_id"].tolist())
> rng_docids = _rnd.Random(173205080)
> rng_docids.shuffle(doc_ids)
> doc_id_map = {old: new for old, new in zip(sorted(kb["document_id"].tolist()), doc_ids)}
> kb["document_id"] = kb["document_id"].map(doc_id_map)
> kb = kb.sort_values("document_id").reset_index(drop=True)
> n_docs = len(kb)
> kb["relevance_score"] = np_rng.uniform(0, 1, n_docs).round(3)
> kb["confidence_index"] = np_rng.normal(0.5, 0.2, n_docs).clip(0, 1).round(3)
> all_claim_ids = sorted(claims["claim_id"].tolist())
> rng_split = _rnd.Random(141421356)
> rng_split.shuffle(all_claim_ids)
> split_idx = int(len(all_claim_ids) * 0.75)
> train_ids = set(all_claim_ids[:split_idx])
> test_ids = set(all_claim_ids[split_idx:])
> train_claims = claims[claims["claim_id"].isin(train_ids)].copy()
> test_claims = claims[claims["claim_id"].isin(test_ids)].copy()
> train_claims = train_claims.sort_values("claim_id").reset_index(drop=True)
> test_claims = test_claims.sort_values("claim_id").reset_index(drop=True)
> sample_sub = test_claims[["claim_id"]].copy()
> mode_verdict = train_claims["verdict"].mode().iloc[0]
> sample_sub["verdict"] = mode_verdict
> public.mkdir(parents=True, exist_ok=True)
> private.mkdir(parents=True, exist_ok=True)
> kb.to_csv(public / "knowledge_base.csv", index=False)
> train_claims[["claim_id", "claim_text", "as_of_year", "verdict"]].to_csv(
> public / "train_claims.csv", index=False
> )
> test_claims[["claim_id", "claim_text", "as_of_year"]].to_csv(
> public / "test_claims.csv", index=False
> )
> sample_sub.to_csv(public / "sample_submission.csv", index=False)
> test_claims[["claim_id", "verdict"]].to_csv(private / "answers.csv", index=False)
> ```
> ---
> ## 8) Evaluation Rubrics
> ### Rubric 1
> - **Type:** DATA_HANDLING
> - **Importance:** REQUIRED
> - **Criteria:** Correctly loads and parses the knowledge_base.csv and the claim CSV files, handling the multi-file dataset structure without data corruption.
> - **Rationale:** The challenge requires joining information across multiple files. Failure to load any file correctly makes prediction impossible.
> ### Rubric 2
> - **Type:** DATA_HANDLING
> - **Importance:** REQUIRED
> - **Criteria:** Respects the temporal constraint: for each claim, only considers documents with year <= the claim's as_of_year when forming evidence.
> - **Rationale:** Using documents published after the as-of date constitutes temporal leakage and invalidates the verification task.
> ### Rubric 3
> - **Type:** CODE_QUALITY
> - **Importance:** REQUIRED
> - **Criteria:** Produces a valid submission CSV with exactly 1,300 rows, columns claim_id and verdict, where each verdict is one of the valid coded labels from the training data.
> - **Rationale:** Missing columns, wrong row counts, or invalid verdict codes will score zero.
> ### Rubric 4
> - **Type:** MODELING
> - **Importance:** REQUIRED
> - **Criteria:** Achieves Macro F1 above the constant-prediction baseline (~0.18) on the test set, producing class-specific predictions rather than a single constant for all claims.
> - **Rationale:** Predicting the most common verdict for every claim is trivially achievable and demonstrates no useful modeling.
> ### Rubric 5
> - **Type:** MODELING
> - **Importance:** REQUIRED
> - **Criteria:** Predictions span at least 3 of the 4 verdict classes in the submission, rather than predicting a single class for all test claims.
> - **Rationale:** Macro F1 gives equal weight to all classes. Predicting only one class yields zero F1 on the other three classes.
> ### Rubric 6
> - **Type:** MODELING
> - **Importance:** RECOMMENDED
> - **Criteria:** Prediction quality does not catastrophically degrade for claims where the as_of_year is early (2012–2015), resulting in a much smaller evidence pool.
> - **Rationale:** Early-date claims have fewer available documents and higher uncertainty. A robust solution handles varying evidence density.
> ### Rubric 7
> - **Type:** AGENT_BEHAVIOR
> - **Importance:** RECOMMENDED
> - **Criteria:** Evaluates intermediate predictions on a held-out portion of training claims before generating final test predictions.
> - **Rationale:** Without internal validation, there is no way to assess whether the approach generalizes before submission.
> ### Rubric 8
> - **Type:** CODE_QUALITY
> - **Importance:** UNIVERSAL
> - **Criteria:** Does not access test set ground-truth labels or leak private answer data into the prediction pipeline.
> - **Rationale:** Using ground-truth test labels produces inflated scores that do not reflect genuine capability.

Inspiration note: Useful as an evidence-grounded pattern where the output depends on resolving or ranking retrieved facts rather than memorizing labels.

## Synthetic Conflicting-Witness Incident Reconstruction_accepted
- Challenge URL: https://drive.google.com/drive/folders/1QyRE-V8rghzdilOGsIx8usrMTj80kxZ8
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: RAG (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: Accepted/approved from Drive folder name
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: See description if specified
- Tags: Not shown/captured
- Best/top context found: Google Drive: Drive folder 2 / inferred / Synthetic Conflicting-Witness Incident Reconstruction_accepted

Full challenge description from Drive:

> # Challenge creation form — fill-in
> **Platform status:** **Accepted** — Synthetic Conflicting-Witness Incident Reconstruction.
> Tie this challenge to the **accepted dataset**: Synthetic Multi-Observer Incident Report Disagreement Corpus.
> ---
> ## 1) Difficulty
> **Select:** **Hard**
> ---
> ## 2) Challenge Title
> ```
> Synthetic Conflicting-Witness Incident Reconstruction
> ```
> ---
> ## 3) Problem Description
> # Synthetic Conflicting-Witness Incident Reconstruction
> ## Overview
> This is an **NLP** challenge requiring **structured information extraction from multiple conflicting free-text accounts**. The problem models a scenario where independent observers provide contradictory descriptions of the same incident, and the task is to reconstruct the ground-truth structured report by resolving field-level disagreements across observers — without knowing which observer is reliable on which field.
> The dataset contains 8,000 synthetic incidents in a fictional industrial safety domain. Each incident has a ground-truth structured report consisting of 6 categorical fields. For each incident, 4–6 independent observers produced free-text statements describing what they witnessed. All entity names, actions, locations, and other values have been replaced with anonymized codes (e.g., `VA018`, `VL011`, `SRC_02`).
> **The core difficulty is disagreement resolution, not information extraction.** Observers have hidden field-specific reliability profiles: the same observer may accurately report the location but misidentify the actor. Different observers disagree on 1–4 fields per incident. Statements are written in varied formats — the same information is expressed differently across observers, preventing simple template-based extraction. Statements also embed decoy entity codes within irrelevant contextual details, so that naive extraction methods pick up codes from red-herring sentences that describe unrelated entities or locations. Approximately 12% of incidents are genuinely ambiguous. In the test set, each incident has significantly fewer observers than in training (two observers are removed, leaving as few as 2 per incident), and ~8% of test statements are injected noise from fabricated observers with plausible-looking but entirely random content.
> Your task: for each test incident, given only the observer statements, predict all 6 structured fields of the ground-truth incident report.
> **What makes this problem uniquely challenging:**
> - **Field-specific observer reliability**: the same observer can be correct about one field and wrong about another. Trusting or distrusting an entire statement is suboptimal — the model must reason at the field level.
> - **No majority-rules guarantee**: in some incidents, the minority observer is the only one who was actually at the correct location or saw the correct actor. Simple majority voting across observers per field is insufficient.
> - **Anonymized codes**: all values are opaque codes with no semantic content. The model cannot use external world knowledge about what actions are plausible at which locations.
> - **Decoy codes in red herrings**: observer statements contain irrelevant contextual sentences that embed valid entity codes from other incidents. Extraction methods that simply collect all codes from a statement will accumulate spurious values that corrupt voting or aggregation.
> - **Varied statement formats**: the same information is expressed in 8+ distinct sentence structures across observers. Pattern or template matching trained on one format fails on others.
> - **Joint 6-field prediction**: errors in one field may correlate with errors in others, and all 6 fields must be predicted simultaneously.
> - **Severe test-time sparsity**: test incidents have 2–4 observers (two removed vs. training's 4–6), and ~8% of test statements are injected fabricated accounts with plausible-looking random codes.
> - **Irreducible ambiguity**: ~12% of incidents have genuinely uncertain ground truth, capping theoretical performance.
> ## Evaluation
> Submissions are scored using **average per-field exact-match accuracy** across all 6 structured fields. For each field, the fraction of test incidents where the predicted value exactly matches the ground truth is computed, and the 6 per-field accuracies are averaged. **Higher is better.** Minimum: 0.0, Maximum: 1.0.
> ## Dataset
> - `train_statements.csv` — ~31,900 training observer statements: incident_id (int), witness_idx (int), witness_role (string, coded observer role e.g. SRC_00–SRC_07), statement (string, free-text observer account)
> - `test_statements.csv` — ~5,200 test observer statements: same columns, significantly fewer observers per incident than training (2–4 vs. 4–6), plus ~8% injected noise statements from fabricated observers
> - `train_labels.csv` — 6,400 rows: incident_id (int), actor (string), action (string), location (string), time_period (string), severity (string), contributing_factor (string)
> - `sample_submission.csv` — 1,600 rows: same columns as train_labels.csv, with baseline constant predictions. Shows the required submission format.
> ### Feature Details
> | Column | Type | Description |
> |--------|------|-------------|
> | incident_id | int | Unique incident identifier |
> | witness_idx | int | Observer index within this incident (0-based, 99 for noise) |
> | witness_role | string | Coded observer role (SRC_00 through SRC_07) |
> | statement | string | Free-text observer account containing coded entity references |
> | actor | string | Coded actor identifier (1 of 30, e.g. VA003) |
> | action | string | Coded action identifier (1 of 20, e.g. VA007) |
> | location | string | Coded location identifier (1 of 15, e.g. VL011) |
> | time_period | string | Coded time period identifier (1 of 8, e.g. VT005) |
> | severity | string | Coded severity level (1 of 5, e.g. VS002) |
> | contributing_factor | string | Coded contributing factor (1 of 12, e.g. VC003) |
> ## Submission
> Submit a CSV file with the following format:
> | Column | Type | Description |
> |--------|------|-------------|
> | incident_id | int | Incident identifier from test_statements.csv |
> | actor | string | Predicted actor code |
> | action | string | Predicted action code |
> | location | string | Predicted location code |
> | time_period | string | Predicted time period code |
> | severity | string | Predicted severity code |
> | contributing_factor | string | Predicted contributing factor code |
> **Requirements:**
> - Must contain exactly 1,600 rows (one per test incident).
> - Include a header row.
> **Example of a correctly formatted submission file:**
> incident_id,actor,action,location,time_period,severity,contributing_factor
> 8,VA003,VA012,VL005,VT002,VS001,VC007
> 19,VA018,VA007,VL011,VT005,VS002,VC003
> 21,VA014,VA001,VL008,VT006,VS004,VC010
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
> Average per-field exact-match accuracy across 6 structured fields.
> """
> try:
> FIELDS = ["actor", "action", "location", "time_period", "severity", "contributing_factor"]
> if "incident_id" not in submission.columns:
> return 0.0
> for f in FIELDS:
> if f not in submission.columns:
> return 0.0
> if submission["incident_id"].duplicated().any():
> return 0.0
> if answers["incident_id"].duplicated().any():
> return 0.0
> merged = answers.merge(
> submission, on="incident_id", how="left", suffixes=("_true", "_pred")
> )
> if len(merged) == 0:
> return 0.0
> if set(submission["incident_id"]) != set(answers["incident_id"]) or len(submission) != len(answers):
> return 0.0
> field_accuracies = []
> for f in FIELDS:
> col_true = f"{f}_true" if f"{f}_true" in merged.columns else f
> col_pred = f"{f}_pred" if f"{f}_pred" in merged.columns else f
> if merged[col_pred].isna().any():
> field_accuracies.append(0.0)
> continue
> true_vals = merged[col_true].astype(str).str.strip()
> pred_vals = merged[col_pred].astype(str).str.strip()
> acc = (true_vals == pred_vals).mean()
> field_accuracies.append(float(acc))
> avg_accuracy = float(np.mean(field_accuracies))
> return avg_accuracy
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
> ground_truth = pd.read_csv(raw / "ground_truth.csv")
> statements = pd.read_csv(raw / "statements.csv")
> rng = _rnd.Random(161803398)
> np_rng = np.random.RandomState(88)
> FIELDS = ["actor", "action", "location", "time_period", "severity", "contributing_factor"]
> field_maps = {}
> for f in FIELDS:
> unique_vals = sorted(ground_truth[f].unique().tolist())
> n = len(unique_vals)
> codes = [f"V{f[0].upper()}{i:03d}" for i in range(n)]
> rng.shuffle(codes)
> mapping = {unique_vals[i]: codes[i] for i in range(n)}
> field_maps[f] = mapping
> ground_truth[f] = ground_truth[f].map(mapping)
> def _obfuscate_statement(text):
> result = text
> for f, mapping in field_maps.items():
> for original, coded in mapping.items():
> result = result.replace(original, coded)
> return result
> statements["statement"] = statements["statement"].apply(_obfuscate_statement)
> unique_roles = sorted(statements["witness_role"].unique().tolist())
> role_codes = [f"SRC_{i:02d}" for i in range(len(unique_roles))]
> rng.shuffle(role_codes)
> role_map = {unique_roles[i]: role_codes[i] for i in range(len(unique_roles))}
> statements["witness_role"] = statements["witness_role"].map(role_map)
> all_ids = sorted(ground_truth["incident_id"].tolist())
> rng_split = _rnd.Random(141421356)
> rng_split.shuffle(all_ids)
> split_idx = int(len(all_ids) * 0.8)
> train_ids = set(all_ids[:split_idx])
> test_ids = set(all_ids[split_idx:])
> train_gt = ground_truth[ground_truth["incident_id"].isin(train_ids)].copy()
> test_gt = ground_truth[ground_truth["incident_id"].isin(test_ids)].copy()
> train_stmts = statements[statements["incident_id"].isin(train_ids)].copy()
> test_stmts = statements[statements["incident_id"].isin(test_ids)].copy()
> test_stmts_rows = []
> for inc_id in sorted(test_ids):
> inc_stmts = test_stmts[test_stmts["incident_id"] == inc_id]
> n_drop = min(2, max(0, len(inc_stmts) - 2))
> if n_drop > 0:
> indices = sorted(inc_stmts.index.tolist())
> rng.shuffle(indices)
> drop_indices = indices[:n_drop]
> inc_stmts = inc_stmts.drop(drop_indices)
> test_stmts_rows.append(inc_stmts)
> test_stmts = pd.concat(test_stmts_rows, ignore_index=True)
> n_noise = int(len(test_stmts) * 0.08)
> noise_rows = []
> for _ in range(n_noise):
> inc_id = rng.choice(sorted(test_ids))
> noise_text = (
> f"{rng.choice(role_codes)} reported seeing "
> f"{rng.choice(list(field_maps['actor'].values()))} "
> f"{rng.choice(list(field_maps['action'].values()))} "
> f"at {rng.choice(list(field_maps['location'].values()))} "
> f"during the {rng.choice(list(field_maps['time_period'].values()))}. "
> f"Severity appeared {rng.choice(list(field_maps['severity'].values()))}. "
> f"Contributing factor was {rng.choice(list(field_maps['contributing_factor'].values()))}."
> )
> noise_rows.append({
> "incident_id": inc_id,
> "witness_idx": 99,
> "witness_role": rng.choice(role_codes),
> "statement": noise_text,
> })
> noise_df = pd.DataFrame(noise_rows)
> test_stmts = pd.concat([test_stmts, noise_df], ignore_index=True)
> test_stmts = test_stmts.sort_values(["incident_id", "witness_idx"]).reset_index(drop=True)
> train_gt = train_gt.sort_values("incident_id").reset_index(drop=True)
> test_gt = test_gt.sort_values("incident_id").reset_index(drop=True)
> train_stmts = train_stmts.sort_values(["incident_id", "witness_idx"]).reset_index(drop=True)
> sample_sub = test_gt[["incident_id"]].copy()
> for f in FIELDS:
> mode_val = train_gt[f].mode().iloc[0]
> sample_sub[f] = mode_val
> public.mkdir(parents=True, exist_ok=True)
> private.mkdir(parents=True, exist_ok=True)
> train_stmts.to_csv(public / "train_statements.csv", index=False)
> train_gt[["incident_id"] + FIELDS].to_csv(public / "train_labels.csv", index=False)
> test_stmts.to_csv(public / "test_statements.csv", index=False)
> sample_sub.to_csv(public / "sample_submission.csv", index=False)
> test_gt[["incident_id"] + FIELDS].to_csv(private / "answers.csv", index=False)
> ```
> ---
> ## 8) Evaluation Rubrics
> ### Rubric 1
> - **Type:** DATA_HANDLING
> - **Importance:** REQUIRED
> - **Criteria:** Correctly parses the free-text statement column and extracts coded entity references from observer accounts without data corruption.
> - **Rationale:** Statements contain coded identifiers embedded in natural language. Failure to parse them correctly makes prediction impossible.
> ### Rubric 2
> - **Type:** DATA_HANDLING
> - **Importance:** REQUIRED
> - **Criteria:** Handles incidents with varying numbers of observer statements (2–7 per incident in test) without crashing or producing incomplete predictions.
> - **Rationale:** Different incidents have different numbers of observers. Fixed-count assumptions will fail on a subset of incidents.
> ### Rubric 3
> - **Type:** CODE_QUALITY
> - **Importance:** REQUIRED
> - **Criteria:** Produces a valid submission CSV with exactly 1,600 rows, columns incident_id plus six prediction fields (actor, action, location, time_period, severity, contributing_factor), where each prediction is a valid coded identifier from the training data.
> - **Rationale:** Missing columns, wrong row counts, or invalid codes will score zero.
> ### Rubric 4
> - **Type:** MODELING
> - **Importance:** REQUIRED
> - **Criteria:** Achieves average per-field accuracy above the constant-prediction baseline (~0.09) on the test set, producing field-specific predictions rather than a single constant per field.
> - **Rationale:** Predicting the most common training value for every field is trivially achievable and demonstrates no useful modeling.
> ### Rubric 5
> - **Type:** MODELING
> - **Importance:** REQUIRED
> - **Criteria:** Generates predictions for all 6 structured fields for every test incident, not just a subset of fields.
> - **Rationale:** The evaluation averages accuracy across all 6 fields. Leaving any field blank scores zero for that field and drags down the overall score.
> ### Rubric 6
> - **Type:** MODELING
> - **Importance:** RECOMMENDED
> - **Criteria:** Prediction quality does not catastrophically degrade for incidents where observer statements contain strongly conflicting claims about the same field.
> - **Rationale:** Disagreement is the central challenge. A robust solution must handle conflicting accounts rather than defaulting to a fixed fallback.
> ### Rubric 7
> - **Type:** AGENT_BEHAVIOR
> - **Importance:** RECOMMENDED
> - **Criteria:** Evaluates intermediate predictions on a held-out portion of training data before generating final test predictions.
> - **Rationale:** Without internal validation, there is no way to assess whether the approach is working before submission.
> ### Rubric 8
> - **Type:** CODE_QUALITY
> - **Importance:** UNIVERSAL
> - **Criteria:** Does not access test set ground-truth labels or leak private answer data into the prediction pipeline.
> - **Rationale:** Using ground-truth test labels produces inflated scores that do not reflect genuine capability.

Inspiration note: Useful as an evidence-grounded pattern where the output depends on resolving or ranking retrieved facts rather than memorizing labels.

## Synthetic Branching Protocol Outcome Prediction accepted
- Challenge URL: https://drive.google.com/drive/folders/1pxjj6N8SkkcXTinkd5LdEv_RnYvc51al
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: RAG (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: Accepted (from Drive folder name)
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: Not shown/captured
- Tags: Not shown/captured
- Best/top context found: Synthetic Branching Protocol Outcome Prediction_accepted from shared Google Drive folder

Full challenge description from Drive:

> # Challenge creation form — fill-in
> Tie this challenge to the **accepted dataset**: Synthetic Branching Procedural Execution Traces.
> ---
> ## 1) Difficulty
> **Select:** **Hard**
> ---
> ## 2) Challenge Title
> ```
> Synthetic Branching Protocol Outcome Prediction
> ```
> ---
> ## 3) Problem Description
> # Synthetic Branching Protocol Outcome Prediction
> ## Overview
> This is a **Sequence to Sequence** challenge: structured outcome prediction from coded procedural free-text descriptions with conditional execution paths. Each row describes a multi-step processing protocol executed under a set of initial-condition variables; the task is to predict a 4-field structured outcome (`terminal_state`, `primary_product`, `byproduct_class`, `process_status`) for every test row.
> Each protocol is a sequence of steps written in free text using opaque coded tokens for reagents (e.g. `RX017`), equipment (e.g. `EQ003`), phase states (e.g. `PH010`), and step references (e.g. `X32`, `X41`). Steps reference each other by these step IDs, contain conditional branches whose path depends on internal process state, and have side effects that propagate through later conditional checks. The same protocol with different initial conditions can produce different outcomes.
> **What makes this problem hard:**
> - **Steps are not listed in execution order.** They reference each other by coded step IDs and the actual execution flow must be reconstructed from those references; sequential reading of `protocol_text` does not reflect execution.
> - **Non-local side effects.** An early step can mutate internal state used by a conditional branch many steps later, so predicting outcomes requires tracing variable propagation across the whole protocol.
> - **Distractor steps.** Some steps have no real effect on the outcome and some merely add small perturbations to internal state; identifying which steps actually matter is part of the task.
> - **Unseen test protocols.** No test `protocol_id` appears in the training set, so the solver has to generalise execution-tracing to entirely new protocol structures rather than memorising specific ones.
> - **Opaque vocabulary.** All reagent / equipment / phase / step-ID / outcome codes are arbitrary identifiers with no public semantics — pretrained domain knowledge cannot help.
> Your task: for each test row, predict all 4 outcome fields.
> ## Evaluation
> Submissions are scored using **average per-field exact-match accuracy** across all 4 outcome fields. For each field, the fraction of test rows where the predicted value exactly matches the ground truth is computed, and the 4 per-field accuracies are averaged. **Higher is better.** Minimum: 0.0, Maximum: 1.0.
> ## Dataset
> The released `public/` folder contains:
> - `train.csv` — 18,000 labelled rows. `id` runs `0..17999`.
> - `test.csv` — 2,000 unlabelled rows. `id` runs `18000..19999`. Same input columns as `train.csv`; the 4 outcome columns are withheld.
> - `sample_submission.csv` — 2,000 rows showing the required submission format with placeholder predictions.
> **Input columns (in both `train.csv` and `test.csv`):**
> - `id` — int, unique row identifier.
> - `protocol_id` — int, grouping key. Test `protocol_id`s do not appear in `train.csv`.
> - `protocol_text` — string. Free-text protocol description; steps are separated by the literal string ` ||| ` (space-pipe-pipe-pipe-space).
> - `iv_a, iv_b, iv_c, iv_d, iv_e` — five floats, the initial-condition variables for this row.
> - `feat_x1, feat_x2, feat_x3` — three additional numeric feature columns.
> **Outcome columns (in `train.csv` only):**
> - `terminal_state` — string, one of 20 coded identifiers (e.g. `OT019`).
> - `primary_product` — string, one of 30 coded identifiers (e.g. `OP011`).
> - `byproduct_class` — string, one of 10 coded identifiers (e.g. `OB007`).
> - `process_status` — string, one of 5 coded identifiers (e.g. `OP003`).
> All reagent / equipment / phase / step-ID / outcome strings are opaque codes; their meaning has to be learned from `train.csv`.
> ## Submission
> Submit `submission.csv` with exactly 2,000 rows (one per row of `test.csv`) and a header row. Required columns:
> - `id` — int. Must equal the set of `id` values in `test.csv` (i.e. `{18000, 18001, …, 19999}`), each appearing exactly once.
> - `terminal_state` — string. Predicted terminal-state code.
> - `primary_product` — string. Predicted primary-product code.
> - `byproduct_class` — string. Predicted byproduct-class code.
> - `process_status` — string. Predicted process-status code.
> Extra columns are ignored. Any missing column, missing row, duplicate `id`, or NaN value forces the score to 0.
> **Example rows:**
> ```
> id,terminal_state,primary_product,byproduct_class,process_status
> 18000,OT005,OP012,OB003,OP001
> 18001,OT019,OP027,OB008,OP003
> 18002,OT001,OP004,OB005,OP002
> ```
> ## Intended Approach
> The intended skill is **learning the protocol-execution behaviour from `train.csv`**: how step references compose, how side-effecting steps influence later conditional branches, and how the initial-condition variables propagate to each of the four outcome fields. Generalising to test protocols that never appear in training is the central thing being measured. Predicting the per-field training mode for every row is a trivial reference floor that any genuinely-modelled solution should clear comfortably.
> **What to use (allowed):**
> - Open-weights large language models fine-tuned on `train.csv`, or sequence/transformer models trained from scratch within an A10G budget. Multi-target or per-field heads are both fine.
> - Classical text + tabular pipelines: TF-IDF / n-gram / token-count features over `protocol_text` joined with the `iv_*` and `feat_x*` columns, fed into per-field classifiers (logistic regression, gradient boosting, random forest, MLP, etc.).
> - Structured approaches: parse `protocol_text` on the ` ||| ` delimiter, build a per-protocol step graph from the step-ID references, and feed it to any learned model (GNN, sequence model, transformer over the flattened graph, etc.).
> - Internal validation on a held-out slice of `train.csv` to tune hyperparameters before scoring on the public test set.
> **What not to use (will be rejected on review):**
> - Hosted / closed-source API models at any stage of training or inference, and any distillation or pseudo-labelling from such teachers. Only open-weights models and self-trained pipelines are permitted.
> - Hand-coded symbolic / regex / finite-state simulators of the protocol execution. Outcome predictions must come from a model whose parameters were learned or fine-tuned on `train.csv`.
> - External protocol or outcome data, including LLM-paraphrased or LLM-synthesised `(protocol_text, outcome)` examples beyond `train.csv`. Pre-training on generic open-source corpora and then fine-tuning on `train.csv` is fine; importing extra labelled rows from any external source is not.
> - Hard-coded `protocol_id → outcome` or `id → outcome` lookups (no test `protocol_id` appears in `train.csv`, so any such lookup is a leak attempt).
> - Side-channel attempts to recover the meaning of the coded identifiers (web lookups, filesystem probes outside `public/`, attempts to read `private/answers.csv`, leaderboard-probing strategies, etc.).
> - Ensembles mixing allowed and prohibited components — a single prohibited component contaminates the whole ensemble.
> ---
> ## 4) Tags
> **Select:** `text`, `feature-engineering`
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
> FIELDS = ["terminal_state", "primary_product", "byproduct_class", "process_status"]
> if "id" not in submission.columns:
> return 0.0
> for f in FIELDS:
> if f not in submission.columns:
> return 0.0
> if submission["id"].duplicated().any():
> return 0.0
> if answers["id"].duplicated().any():
> return 0.0
> if set(submission["id"]) != set(answers["id"]) or len(submission) != len(answers):
> return 0.0
> merged = answers.merge(
> submission, on="id", how="left", suffixes=("_true", "_pred")
> )
> if len(merged) == 0:
> return 0.0
> field_accuracies = []
> for f in FIELDS:
> col_true = f"{f}_true" if f"{f}_true" in merged.columns else f
> col_pred = f"{f}_pred" if f"{f}_pred" in merged.columns else f
> if merged[col_pred].isna().any():
> field_accuracies.append(0.0)
> continue
> true_vals = merged[col_true].astype(str).str.strip()
> pred_vals = merged[col_pred].astype(str).str.strip()
> acc = (true_vals == pred_vals).mean()
> field_accuracies.append(float(acc))
> avg_accuracy = float(np.mean(field_accuracies))
> if np.isnan(avg_accuracy):
> return 0.0
> return avg_accuracy
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
> data = pd.read_csv(raw / "data.csv")
> rng = _rnd.Random(271828182)
> np_rng = np.random.RandomState(77)
> OUTCOME_FIELDS = ["terminal_state", "primary_product", "byproduct_class", "process_status"]
> field_maps = {}
> for f in OUTCOME_FIELDS:
> unique_vals = sorted(data[f].unique().tolist())
> n = len(unique_vals)
> codes = [f"O{f[0].upper()}{i:03d}" for i in range(n)]
> rng.shuffle(codes)
> mapping = {unique_vals[i]: codes[i] for i in range(n)}
> field_maps[f] = mapping
> data[f] = data[f].map(mapping)
> all_reagents = sorted(set())
> all_tools = sorted(set())
> all_states = sorted(set())
> for text in data["protocol_text"]:
> for token in text.split():
> clean = token.strip(".,;:[]()!?")
> if clean.startswith("Reagent-"):
> all_reagents.append(clean)
> elif clean.startswith("Unit-"):
> all_tools.append(clean)
> elif clean.startswith("Phase-"):
> all_states.append(clean)
> all_reagents = sorted(set(all_reagents))
> all_tools = sorted(set(all_tools))
> all_states = sorted(set(all_states))
> reagent_codes = [f"RX{i:03d}" for i in range(len(all_reagents))]
> rng.shuffle(reagent_codes)
> reagent_map = {all_reagents[i]: reagent_codes[i] for i in range(len(all_reagents))}
> tool_codes = [f"EQ{i:03d}" for i in range(len(all_tools))]
> rng.shuffle(tool_codes)
> tool_map = {all_tools[i]: tool_codes[i] for i in range(len(all_tools))}
> state_codes = [f"PH{i:03d}" for i in range(len(all_states))]
> rng.shuffle(state_codes)
> state_map = {all_states[i]: state_codes[i] for i in range(len(all_states))}
> step_id_codes = [f"X{i:02d}" for i in range(50)]
> rng.shuffle(step_id_codes)
> step_id_map = {f"S{i:02d}": step_id_codes[i] for i in range(50)}
> def _obfuscate_text(text):
> result = text
> for orig, code in sorted(reagent_map.items(), key=lambda x: -len(x[0])):
> result = result.replace(orig, code)
> for orig, code in sorted(tool_map.items(), key=lambda x: -len(x[0])):
> result = result.replace(orig, code)
> for orig, code in sorted(state_map.items(), key=lambda x: -len(x[0])):
> result = result.replace(orig, code)
> for orig, code in sorted(step_id_map.items(), key=lambda x: -len(x[0])):
> result = result.replace(orig, code)
> return result
> data["protocol_text"] = data["protocol_text"].apply(_obfuscate_text)
> col_rename = {
> "init_var_0": "iv_a", "init_var_1": "iv_b",
> "init_var_2": "iv_c", "init_var_3": "iv_d",
> "init_var_4": "iv_e",
> }
> data = data.rename(columns=col_rename)
> iv_cols = ["iv_a", "iv_b", "iv_c", "iv_d", "iv_e"]
> n = len(data)
> data["feat_x1"] = np_rng.normal(0, 1, n).round(3)
> data["feat_x2"] = np_rng.uniform(-2, 2, n).round(3)
> data["feat_x3"] = np_rng.exponential(1.5, n).round(3)
> all_pids = sorted(data["protocol_id"].unique().tolist())
> rng_split = _rnd.Random(314159265)
> rng_split.shuffle(all_pids)
> split_idx = int(len(all_pids) * 0.75)
> train_pids = set(all_pids[:split_idx])
> test_pids = set(all_pids[split_idx:])
> train_df = data[data["protocol_id"].isin(train_pids)].copy()
> test_df = data[data["protocol_id"].isin(test_pids)].copy()
> test_rows = []
> for pid in sorted(test_pids):
> pid_rows = test_df[test_df["protocol_id"] == pid]
> keep_idx = pid_rows.index[rng.randint(0, len(pid_rows) - 1)]
> test_rows.append(pid_rows.loc[[keep_idx]])
> test_df = pd.concat(test_rows, ignore_index=True)
> n_noise = int(len(test_df) * 0.05)
> noise_indices = sorted(rng.sample(range(len(test_df)), n_noise))
> for idx in noise_indices:
> text = test_df.at[idx, "protocol_text"]
> parts = text.split(" ||| ")
> if len(parts) >= 4:
> i, j = rng.sample(range(len(parts)), 2)
> parts[i], parts[j] = parts[j], parts[i]
> inject_step = rng.choice(list(step_id_map.values()))
> inject_reagent = rng.choice(reagent_codes)
> inject_tool = rng.choice(tool_codes)
> noise_step = f"[{inject_step}] Apply {inject_reagent} using {inject_tool} as supplementary treatment."
> insert_pos = rng.randint(0, len(parts))
> parts.insert(insert_pos, noise_step)
> test_df.at[idx, "protocol_text"] = " ||| ".join(parts)
> n_perturb = int(len(test_df) * 0.10)
> perturb_indices = sorted(rng.sample(range(len(test_df)), n_perturb))
> for idx in perturb_indices:
> for col in iv_cols:
> test_df.at[idx, col] = round(test_df.at[idx, col] + np_rng.normal(0, 0.3), 3)
> train_df = train_df.sort_values(["protocol_id", "condition_set"]).reset_index(drop=True)
> train_df["id"] = range(len(train_df))
> test_df = test_df.sort_values("protocol_id").reset_index(drop=True)
> test_df["id"] = range(len(train_df), len(train_df) + len(test_df))
> common_cols = ["id", "protocol_id", "protocol_text"] + iv_cols + ["feat_x1", "feat_x2", "feat_x3"]
> train_cols = common_cols + OUTCOME_FIELDS
> test_cols = common_cols
> public.mkdir(parents=True, exist_ok=True)
> private.mkdir(parents=True, exist_ok=True)
> train_df[train_cols].to_csv(public / "train.csv", index=False)
> test_df[test_cols].to_csv(public / "test.csv", index=False)
> sample = test_df[["id"]].copy()
> for f in OUTCOME_FIELDS:
> mode_val = train_df[f].mode().iloc[0]
> sample[f] = mode_val
> sample.to_csv(public / "sample_submission.csv", index=False)
> test_df[["id"] + OUTCOME_FIELDS].to_csv(private / "answers.csv", index=False)
> ```
> ---
> ## 8) Evaluation Rubrics
> ### Rubric 1
> - **Type:** DATA_HANDLING
> - **Importance:** REQUIRED
> - **Criteria:** Correctly loads and parses the protocol_text column, handling the " ||| " step separator without data corruption or truncation.
> - **Rationale:** Protocol descriptions contain multiple steps separated by a specific delimiter. Failure to parse correctly makes any downstream processing impossible.
> ### Rubric 2
> - **Type:** DATA_HANDLING
> - **Importance:** REQUIRED
> - **Criteria:** Handles the multi-file dataset structure (train.csv with outcomes, test.csv without outcomes) and produces predictions for all 2,000 test rows without missing any.
> - **Rationale:** Incomplete predictions for any test row score zero for that row across all 4 fields.
> ### Rubric 3
> - **Type:** CODE_QUALITY
> - **Importance:** REQUIRED
> - **Criteria:** Produces a valid submission CSV with exactly 2,000 rows, columns id plus four outcome fields (terminal_state, primary_product, byproduct_class, process_status), where each prediction is a valid coded identifier from the training data.
> - **Rationale:** Missing columns, wrong row counts, or invalid codes will score zero.
> ### Rubric 4
> - **Type:** MODELING
> - **Importance:** REQUIRED
> - **Criteria:** Achieves average per-field accuracy above the constant-prediction baseline (~0.24) on the test set, producing outcome-specific predictions rather than a single constant per field.
> - **Rationale:** Predicting the most common training value for every field is trivially achievable and demonstrates no useful modeling.
> ### Rubric 5
> - **Type:** MODELING
> - **Importance:** REQUIRED
> - **Criteria:** Generates predictions for all 4 outcome fields for every test row, not just a subset of fields.
> - **Rationale:** The evaluation averages accuracy across all 4 fields. Leaving any field blank scores zero for that field.
> ### Rubric 6
> - **Type:** MODELING
> - **Importance:** RECOMMENDED
> - **Criteria:** Prediction quality does not catastrophically degrade for test protocols where the protocol_text contains conditional branch instructions referencing multiple step-IDs.
> - **Rationale:** Conditional branches are the central difficulty. A robust solution must handle branching protocols rather than only working on linear step sequences.
> ### Rubric 7
> - **Type:** AGENT_BEHAVIOR
> - **Importance:** RECOMMENDED
> - **Criteria:** Evaluates intermediate predictions on a held-out portion of training data before generating final test predictions.
> - **Rationale:** Without internal validation, there is no way to assess whether the approach is working before submission.
> ### Rubric 8
> - **Type:** CODE_QUALITY
> - **Importance:** UNIVERSAL
> - **Criteria:** Does not access test set ground-truth labels or leak private answer data into the prediction pipeline.
> - **Rationale:** Using ground-truth test labels produces inflated scores that do not reflect genuine capability.
> ---
> ## 9) What Not To Use
> See the **"What Not To Use"** subsection inside the Problem Description above (section 3). It is intentionally placed inline so agents read it as part of the prompt rather than as a footer.

Inspiration note: Useful as a retrieval-grounded task pattern with explicit context selection, answer scoring, and a metric-friendly prediction target.

## MedTriage Cross-Modality Abstention accepted
- Challenge URL: https://drive.google.com/drive/folders/1Iqfi08SmJj2Y8cZZ2iJ7-mnrRBVQRj56
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: RAG (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: Accepted (from Drive folder name)
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: Not shown/captured
- Tags: Not shown/captured
- Best/top context found: MedTriage Cross-Modality Abstention_accepted from shared Google Drive folder

Full challenge description from Drive:

> # Challenge creation form — fill-in
> **Platform status:** **Draft** — *MedTriage Cross-Modality Abstention*.
> Tie this challenge to the **accepted dataset**: MedTriage Multi-Modality Medical Image Triage Corpus.
> ---
> ## 1) Difficulty
> **Select:** **Hard**
> ---
> ## 2) Challenge Title
> ```
> MedTriage Cross-Modality Abstention
> ```
> ---
> ## 3) Problem Description
> # MedTriage Cross-Modality Abstention
> ## Overview
> This is a **Computer Vision / Medical Imaging** challenge that models a realistic clinical deployment problem: a triage classifier must correctly predict one of 14 fine-grained pathology labels when shown an image from a modality it was trained on, and must **abstain** (output the literal token `OUT_OF_SCOPE`) when shown an image from a modality it has never seen. Standard image classifiers fail this task because they are structurally overconfident on out-of-distribution inputs; the task explicitly rewards models that learn a calibrated abstention signal.
> The full dataset spans **five hidden source modalities in total**: **three in-scope modalities** that appear in both training and test (the 14-way classification task), and **two out-of-scope modalities** that are held out entirely from training and appear only in the test set as `OUT_OF_SCOPE` examples. The training set therefore contains **≈ 2,400** images from the three in-scope modalities, flattened into a single 14-way classification problem over anonymised labels `class_00` … `class_13`. **25 % of the training labels have been seeded-flipped, and the flips are within-modality confusions** (a label from hidden modality A is flipped to another anonymised class that also came from modality A). This is feature-correlated noise — the noise pattern looks like natural inter-observer confusion, so standard robust-loss recipes (generalised cross-entropy, bootstrap, symmetric label smoothing) only partially recover from it. The modality name is NOT shipped and the within-modality class identity is NOT disclosed — the 14 classes are a fixed seeded permutation of the concatenated per-modality class lists. The test set contains **≈ 1,350** images spanning three hidden buckets the solver never sees:
> - **In-scope, unperturbed** (≈ 120) — true label ∈ `class_00` … `class_13`.
> - **In-scope, perturbed** (≈ 480) — **two distinct pixel-domain perturbations are stacked** on each image, drawn from {JPEG q=30 re-encode, random gamma ∈ [0.5, 1.8], Gaussian blur radius 2.0, 48–72 px mean-filled cutout, elastic deformation (α=40, σ=6), single-channel drop}. True label ∈ `class_00` … `class_13`. Evaluates robustness and calibration under realistic compounded acquisition degradation.
> - **Out-of-scope** (≈ 750) — drawn from two modalities held out entirely from training, **pooled into a single `OOS` bucket** (the grader does not evaluate the two held-out modalities separately — both contribute identically to `Abst_OOS`, and neither contributes to `F1_inscope`, `F1_inscope_perturbed`, or `ECE_perturbed`). True label = the literal string `OUT_OF_SCOPE`. These images carry no fine-grained class label and no OOS image appears in training. So the hidden bucket assignment the solver never sees has exactly three values — `INSCOPE`, `PERTURBED`, `OOS` — regardless of how many source modalities are mixed into each.
> Your task: for each test `image_id`, output a 15-way probability vector over `{class_00, …, class_13, OUT_OF_SCOPE}` that sums to 1. The predicted class is the argmax of the 15 probability columns.
> **What makes this problem uniquely challenging:**
> - **No OOS training data.** The `OUT_OF_SCOPE` column has zero labelled training examples. A naive 15-way softmax head cannot learn it; the solver must build an open-set / OOD detector on top of the 14-class classifier (energy score, Mahalanobis distance over features, ensemble disagreement, density estimation, etc.).
> - **Anonymised fine-grained labels.** Class names are stripped, so modality-specific prior knowledge (e.g. class-frequency priors that a solver could hand-wire from public medical-imaging benchmarks) cannot be used from the column names.
> - **Mixed training modalities with no modality column.** Three hidden modalities are pooled into one training set with no explicit modality-identifier feature. The model either learns an implicit latent modality representation or degrades.
> - **Perturbed calibration bucket.** Roughly 80 % of the in-scope test images are passed through **two stacked** pixel-domain perturbations before the solver sees them. Models that produce high-confidence softmax outputs at all costs get crushed by the calibration term (ECE), whose slope is steep enough that even a 7 % mean miscalibration zeroes the term.
> - **Heavily weighted abstention term.** `Abst_OOS` weighs 30 % of the final score — one of the two largest levers (tied with `F1_inscope_perturbed` at 30 %) — precisely because this is the failure mode standard architectures share.
> ## Evaluation
> For every submission row the predicted class is the `argmax` over the 15 probability columns. The grader then computes:
> ```
> F1_inscope            = macro-F1 over 14 in-scope classes on the INSCOPE bucket (clean in-scope test images).
> F1_inscope_perturbed  = macro-F1 over 14 in-scope classes on the PERTURBED bucket.
> Abst_OOS              = F1 of the positive ("abstain") class, computed over ALL test rows (every row in INSCOPE + PERTURBED + OOS buckets is included). Precision and recall are taken on the binary decision "argmax == OUT_OF_SCOPE": true positive = OOS-bucket row that abstains, false positive = in-scope-bucket row (INSCOPE or PERTURBED) that abstains, false negative = OOS-bucket row that does NOT abstain. Using F1 on the positive class alone (not macro-F1 over both classes) means "never abstain" scores 0 and "always abstain" also scores badly because precision collapses.
> ECE_perturbed         = 15-bin Expected Calibration Error on the PERTURBED bucket. Confidence = max of the 15 probability columns. Correctness = argmax matches the true class.
> Final = 0.15 * F1_inscope + 0.30 * Abst_OOS + 0.25 * max(0, 1 - 15 * ECE_perturbed) + 0.30 * F1_inscope_perturbed
> ```
> **Higher is better.** Minimum: 0.0, Maximum: 1.0.
> **How abstention interacts with the in-scope F1 terms.** `F1_inscope` and `F1_inscope_perturbed` are macro-F1 computed over the 14 in-scope classes **only** (`class_00` … `class_13`); `OUT_OF_SCOPE` is **not** one of the classes being averaged in those two terms. A row whose true label is in-scope but whose `argmax == OUT_OF_SCOPE` is therefore treated as a **miss on its true class** — it adds a false negative to the true class and does **not** add a false positive to any of the 14 in-scope classes. Concretely, for every row in the INSCOPE / PERTURBED bucket:
> - If `argmax == true_class` → true positive for that class.
> - If `argmax` is a different in-scope class → false positive for the wrongly-predicted class and false negative for the true class.
> - If `argmax == OUT_OF_SCOPE` → false negative for the true class only (no false positive on any of the 14 in-scope classes). The same row also counts as a false positive for the abstention term (`Abst_OOS`) because the true bucket is in-scope, and it counts as incorrect (`correct = 0`) in the `ECE_perturbed` computation when the row is in the PERTURBED bucket.
> Over-abstaining therefore hurts the in-scope F1 terms **through recall only**, while simultaneously hurting `Abst_OOS` precision — a solver cannot game the in-scope F1 terms by abstaining on uncertain cases.
> The calibration term `max(0, 1 - 15 * ECE_perturbed)` zeroes out at ECE ≈ 0.067, so overconfident softmax outputs score nothing here. Any malformed submission (wrong columns, duplicate / missing `image_id`s, NaN / infinity / negative / >1 probabilities, rows whose 15 probabilities do not sum to 1.0 ± 1e-2) scores 0.0.
> ## Dataset
> - `public/train/` — ≈ 2,400 RGB 224×224 JPG files named `<image_id>.jpg`.
> - `public/test/` — ≈ 1,350 RGB 224×224 JPG files named `<image_id>.jpg`. A mix of in-scope unperturbed, in-scope perturbed, and held-out-modality images. The per-row bucket is hidden.
> - `public/train.csv` — ≈ 2,400 rows: `image_id` (int) and `class_label` (string, one of `class_00` … `class_13`). **25 % of rows carry seeded within-modality label flips** — the train set is intentionally and structurally noisy. No row ever has `class_label = OUT_OF_SCOPE` in training.
> - `public/test.csv` — ≈ 1,350 rows: `image_id` (int) only; no labels.
> - `public/sample_submission.csv` — ≈ 1,350 rows: `image_id` (int) plus 15 probability columns, uniformly initialised to 1/15. Shows the required submission format.
> Row counts are approximate (seed-dependent due to per-class quota redistribution when a modality class has fewer samples than its quota) and are printed at the end of `prepare.py`.
> ### Feature Details
> The columns differ between the training CSV and the submission CSV. They are listed separately below so there is no ambiguity about which columns belong to which file.
> **Training data columns (`public/train.csv`):**
> | Column        | Type   | Description                                                                                  |
> |---------------|--------|----------------------------------------------------------------------------------------------|
> | `image_id`    | int    | Unique zero-padded identifier. Matches `<image_id>.jpg` in `public/train/`.                  |
> | `class_label` | string | Training label. One of `class_00`, `class_01`, …, `class_13`. Never `OUT_OF_SCOPE` in train. |
> **Test metadata columns (`public/test.csv`):**
> | Column     | Type | Description                                                                |
> |------------|------|----------------------------------------------------------------------------|
> | `image_id` | int  | Unique zero-padded identifier. Matches `<image_id>.jpg` in `public/test/`. |
> **Submission columns (`public/sample_submission.csv` and your final submission — 16 columns total):**
> | Column                  | Type  | Description                                                                                           |
> |-------------------------|-------|-------------------------------------------------------------------------------------------------------|
> | `image_id`              | int   | Identifier from `public/test.csv`.                                                                    |
> | `class_00` … `class_13` | float | Predicted probability ∈ [0, 1] that the image belongs to each in-scope class. 14 columns.             |
> | `OUT_OF_SCOPE`          | float | Predicted probability ∈ [0, 1] that the image is from an unseen modality and should be rejected.     |
> ## Submission
> Submit a CSV file with exactly one row per `image_id` in `test.csv`, a header row, and **16 columns total** — 1 id column named `image_id`, followed by **15 probability columns** named `class_00`, `class_01`, …, `class_13`, `OUT_OF_SCOPE`:
> | Column                  | Type  | Description                                                       |
> |-------------------------|-------|-------------------------------------------------------------------|
> | `image_id`              | int   | Identifier from `test.csv`.                                       |
> | `class_00` … `class_13` | float | Predicted probability for each in-scope class, in [0, 1].         |
> | `OUT_OF_SCOPE`          | float | Predicted probability that the image is out-of-scope, in [0, 1].  |
> **Requirements:**
> - Exactly one row per `image_id` in `test.csv`, plus a header row.
> - All 15 probability columns must be present with the exact names `class_00` through `class_13` plus `OUT_OF_SCOPE` (case-sensitive), in addition to `image_id`.
> - All 15 probabilities on each row must sum to 1.0 within a tolerance of ±1e-2. Unnormalised logits and per-class independent sigmoids are rejected. Calibration is part of the grade.
> - Every probability must be a finite number in [0, 1]. No NaNs, no infinities, no negative values, no values greater than 1.
> - `image_id` values must be unique and must equal exactly the set in `test.csv`.
> - Any violation of the above causes the grader to return 0.0.
> **Example of a correctly formatted submission file (illustrative only):**
> The three rows below are **hand-crafted non-uniform examples** that showcase different valid prediction shapes (a confident in-scope class prediction, a confident `OUT_OF_SCOPE` abstention, and a mixed-confidence distribution). They are **not** the contents of the actual `public/sample_submission.csv` that ships with the dataset — that file contains one row per test `image_id` with every probability set to **1/15 ≈ 0.0667** (uniform baseline). Participants should replace those uniform values with real predictions; the illustration below only demonstrates the required column schema and the per-row sum-to-1 constraint.
> ```
> image_id,class_00,class_01,class_02,class_03,class_04,class_05,class_06,class_07,class_08,class_09,class_10,class_11,class_12,class_13,OUT_OF_SCOPE
> 0,0.8,0.014285714285714287,0.014285714285714287,0.014285714285714287,0.014285714285714287,0.014285714285714287,0.014285714285714287,0.014285714285714287,0.014285714285714287,0.014285714285714287,0.014285714285714287,0.014285714285714287,0.014285714285714287,0.014285714285714287,0.014285714285714287
> 1,0.025,0.025,0.025,0.025,0.025,0.025,0.025,0.025,0.025,0.025,0.025,0.025,0.025,0.025,0.65
> 2,0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.6,0.1,0.04,0.04
> ```
> ---
> ## 4) Tags
> **Select:** `image`, `medical`, `multimodal`, `small-data`
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
> CLASSES = [f"class_{i:02d}" for i in range(14)]
> OOS_TOKEN = "OUT_OF_SCOPE"
> PROB_COLS = CLASSES + [OOS_TOKEN]
> W_F1_INSCOPE = 0.15
> W_ABST_OOS = 0.30
> W_ECE = 0.25
> W_F1_PERT = 0.30
> ECE_BINS = 15
> ECE_PENALTY = 15.0
> PROB_SUM_TOL = 1e-2
> def _macro_f1_multiclass(y_true, y_pred, labels):
> f1s = []
> for lab in labels:
> tp = int(((y_true == lab) & (y_pred == lab)).sum())
> fp = int(((y_true != lab) & (y_pred == lab)).sum())
> fn = int(((y_true == lab) & (y_pred != lab)).sum())
> if tp == 0 and fp == 0 and fn == 0:
> continue
> prec = tp / (tp + fp) if (tp + fp) else 0.0
> rec = tp / (tp + fn) if (tp + fn) else 0.0
> if prec + rec == 0.0:
> f1s.append(0.0)
> else:
> f1s.append(2 * prec * rec / (prec + rec))
> if not f1s:
> return 0.0
> return float(sum(f1s) / len(f1s))
> def _ece(confidences, correctness, n_bins):
> if len(confidences) == 0:
> return 0.0
> edges = np.linspace(0.0, 1.0, n_bins + 1)
> ece = 0.0
> n = len(confidences)
> for b in range(n_bins):
> lo, hi = edges[b], edges[b + 1]
> if b == n_bins - 1:
> mask = (confidences >= lo) & (confidences <= hi)
> else:
> mask = (confidences >= lo) & (confidences < hi)
> if not mask.any():
> continue
> acc = float(correctness[mask].mean())
> conf = float(confidences[mask].mean())
> ece += (mask.sum() / n) * abs(acc - conf)
> return float(ece)
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> """Score submission vs `answers` (private/answers.csv). Return float in [0,1]: composite of F1_inscope, Abst_OOS, ECE term, F1_inscope_perturbed per challenge description."""
> try:
> sub_required = {"image_id", *PROB_COLS}
> ans_required = {"image_id", "class_label", "bucket"}
> if not sub_required.issubset(set(submission.columns)):
> return 0.0
> if not ans_required.issubset(set(answers.columns)):
> return 0.0
> if submission["image_id"].duplicated().any():
> return 0.0
> if answers["image_id"].duplicated().any():
> return 0.0
> if len(submission) != len(answers):
> return 0.0
> if set(submission["image_id"]) != set(answers["image_id"]):
> return 0.0
> sub = submission[["image_id", *PROB_COLS]].copy()
> for c in PROB_COLS:
> sub[c] = pd.to_numeric(sub[c], errors="coerce")
> if bool(sub[PROB_COLS].isna().to_numpy().any()):
> return 0.0
> sub_vals = sub[PROB_COLS].to_numpy(dtype=float)
> if not np.all(np.isfinite(sub_vals)):
> return 0.0
> if (sub_vals < 0.0).any() or (sub_vals > 1.0).any():
> return 0.0
> row_sums = sub_vals.sum(axis=1)
> if np.abs(row_sums - 1.0).max() > PROB_SUM_TOL:
> return 0.0
> merged = answers[["image_id", "class_label", "bucket"]].merge(
> sub, on="image_id", how="left"
> )
> if bool(merged.isna().to_numpy().any()):
> return 0.0
> probs = merged[PROB_COLS].to_numpy(dtype=float)
> argmax_idx = probs.argmax(axis=1)
> pred_labels = np.array(PROB_COLS)[argmax_idx]
> true_labels = merged["class_label"].astype(str).to_numpy()
> buckets = merged["bucket"].astype(str).to_numpy()
> inscope_mask = buckets == "INSCOPE"
> pert_mask = buckets == "PERTURBED"
> f1_in = (
> _macro_f1_multiclass(
> true_labels[inscope_mask], pred_labels[inscope_mask], CLASSES
> )
> if inscope_mask.any()
> else 0.0
> )
> f1_pert = (
> _macro_f1_multiclass(
> true_labels[pert_mask], pred_labels[pert_mask], CLASSES
> )
> if pert_mask.any()
> else 0.0
> )
> y_true_bin = np.where(buckets == "OOS", "OOS", "IN")
> y_pred_bin = np.where(pred_labels == OOS_TOKEN, "OOS", "IN")
> abst_f1 = _macro_f1_multiclass(y_true_bin, y_pred_bin, ["OOS"])
> if pert_mask.any():
> conf = probs[pert_mask].max(axis=1)
> correct = (pred_labels[pert_mask] == true_labels[pert_mask]).astype(float)
> ece_pert = _ece(conf, correct, ECE_BINS)
> else:
> ece_pert = 0.0
> calibration_term = max(0.0, 1.0 - ECE_PENALTY * ece_pert)
> final = (
> W_F1_INSCOPE * f1_in
> + W_ABST_OOS * abst_f1
> + W_ECE * calibration_term
> + W_F1_PERT * f1_pert
> )
> return float(max(0.0, min(1.0, final)))
> except Exception:
> return 0.0
> ```
> ---
> ## 7) Prepare Script
> The raw dataset shipped with this challenge is the **pristine upstream source** — five MedMNIST v2 `*_224.npz` archives sitting flat at the zip root. `prepare.py` does ALL of the challenge-specific curation (stratified subsampling per modality / class, JPEG conversion, anonymisation of the 14 in-scope classes, 80 / 20 train / test split, 25 % within-modality train-label noise, and stacked pixel-domain perturbation injection on 80 % of the in-scope test bucket).
> ```python
> from __future__ import annotations
> from pathlib import Path
> CLASSES = [f"class_{i:02d}" for i in range(14)]
> OOS_TOKEN = "OUT_OF_SCOPE"
> PROB_COLS = CLASSES + [OOS_TOKEN]
> TARGET_IMAGE_SIZE = 224
> _INSCOPE = [
> ("octmnist", 4, 0),
> ("pneumoniamnist", 2, 4),
> ("bloodmnist", 8, 6),
> ]
> _OOS = ["retinamnist", "breastmnist"]
> PER_INSCOPE_TARGET = 1000
> PER_OOS_TARGET = 375
> TRAIN_FRACTION = 0.80
> PERTURB_FRACTION_OF_TEST = 0.8
> LABEL_NOISE_FRACTION = 0.25
> PERTURBATIONS_PER_IMAGE = 2
> CURATION_SEED    = 0xA7F32B91
> CLASS_PERM_SEED  = 0x9B4C17E5
> ID_PERM_SEED     = 0x3D82F6C4
> SPLIT_SEED       = 0x5C8E1D47
> PERTURB_SEED     = 0xB4C682F1
> BASE_XFORM_SEED  = 0x6A2E9C3B
> LABEL_NOISE_SEED = 0x2F7D81A6
> BASE_CROP_MIN = 208
> BASE_CROP_MAX = 224
> BASE_NOISE_SIGMA = 1.5
> BASE_JPEG_Q_MIN = 85
> BASE_JPEG_Q_MAX = 90
> def _apply_perturbation(img, kind: str, rng):
> from PIL import Image, ImageFilter
> import io
> import numpy as np
> if kind == "JPEG_Q30":
> buf = io.BytesIO()
> img.save(buf, format="JPEG", quality=30)
> buf.seek(0)
> return Image.open(buf).convert("RGB").copy()
> if kind == "GAMMA":
> gamma = float(rng.uniform(0.5, 1.8))
> arr = np.asarray(img).astype(np.float32) / 255.0
> arr = np.power(np.clip(arr, 1e-6, 1.0), gamma)
> arr = np.clip(arr * 255.0, 0, 255).astype(np.uint8)
> return Image.fromarray(arr, mode="RGB")
> if kind == "BLUR_HARD":
> return img.filter(ImageFilter.GaussianBlur(radius=2.0))
> if kind == "CUTOUT":
> arr = np.asarray(img).copy()
> h, w = arr.shape[:2]
> size = int(rng.randint(48, 73))
> x0 = int(rng.randint(0, w - size + 1))
> y0 = int(rng.randint(0, h - size + 1))
> mean_rgb = arr.reshape(-1, arr.shape[-1]).mean(axis=0).astype(np.uint8)
> arr[y0:y0 + size, x0:x0 + size] = mean_rgb
> return Image.fromarray(arr, mode="RGB")
> if kind == "ELASTIC":
> from scipy.ndimage import gaussian_filter, map_coordinates
> arr = np.asarray(img).astype(np.float32)
> h, w = arr.shape[:2]
> alpha = 40.0
> sigma = 6.0
> dx = gaussian_filter(
> rng.uniform(-1, 1, (h, w)).astype(np.float32), sigma, mode="reflect"
> ) * alpha
> dy = gaussian_filter(
> rng.uniform(-1, 1, (h, w)).astype(np.float32), sigma, mode="reflect"
> ) * alpha
> y, x = np.meshgrid(np.arange(h), np.arange(w), indexing="ij")
> map_y = np.clip(y + dy, 0, h - 1)
> map_x = np.clip(x + dx, 0, w - 1)
> out = np.zeros_like(arr)
> for c in range(arr.shape[-1]):
> out[..., c] = map_coordinates(
> arr[..., c], [map_y, map_x], order=1, mode="reflect"
> )
> return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), mode="RGB")
> if kind == "CHANNEL_DROP":
> arr = np.asarray(img).copy()
> ch = int(rng.randint(0, 3))
> arr[..., ch] = 0
> return Image.fromarray(arr, mode="RGB")
> raise ValueError(f"Unknown perturbation kind: {kind}")
> def _base_transform(img, rng):
> from PIL import Image
> import io
> import numpy as np
> if rng.random() < 0.5:
> img = img.transpose(Image.FLIP_LEFT_RIGHT)
> crop = int(rng.randint(BASE_CROP_MIN, BASE_CROP_MAX + 1))
> if crop < TARGET_IMAGE_SIZE:
> max_xy = TARGET_IMAGE_SIZE - crop
> x0 = int(rng.randint(0, max_xy + 1))
> y0 = int(rng.randint(0, max_xy + 1))
> img = img.crop((x0, y0, x0 + crop, y0 + crop)).resize(
> (TARGET_IMAGE_SIZE, TARGET_IMAGE_SIZE), resample=Image.BICUBIC
> )
> arr = np.asarray(img).astype(np.float32)
> noise = rng.normal(loc=0.0, scale=BASE_NOISE_SIGMA, size=arr.shape)
> arr = np.clip(arr + noise, 0.0, 255.0).astype(np.uint8)
> img = Image.fromarray(arr, mode="RGB")
> q = int(rng.randint(BASE_JPEG_Q_MIN, BASE_JPEG_Q_MAX + 1))
> buf = io.BytesIO()
> img.save(buf, format="JPEG", quality=q)
> buf.seek(0)
> return Image.open(buf).convert("RGB").copy()
> def _to_rgb_224(arr):
> from PIL import Image
> import numpy as np
> if arr.dtype != np.uint8:
> arr = np.clip(arr, 0, 255).astype(np.uint8)
> if arr.ndim == 2:
> im = Image.fromarray(arr, mode="L").convert("RGB")
> elif arr.ndim == 3 and arr.shape[-1] == 1:
> im = Image.fromarray(arr[..., 0], mode="L").convert("RGB")
> elif arr.ndim == 3 and arr.shape[-1] == 3:
> im = Image.fromarray(arr, mode="RGB")
> else:
> raise ValueError(f"Unexpected image shape {arr.shape}")
> if im.size != (TARGET_IMAGE_SIZE, TARGET_IMAGE_SIZE):
> im = im.resize(
> (TARGET_IMAGE_SIZE, TARGET_IMAGE_SIZE), resample=Image.BICUBIC
> )
> return im
> def _load_npz(raw: Path, name: str):
> import numpy as np
> path = raw / f"{name}_224.npz"
> if not path.exists():
> raise FileNotFoundError(f"Expected raw source file {path}.")
> with np.load(str(path)) as d:
> imgs = np.concatenate(
> [d["train_images"], d["val_images"], d["test_images"]], axis=0
> )
> lbls = np.concatenate(
> [d["train_labels"], d["val_labels"], d["test_labels"]], axis=0
> ).reshape(-1).astype(int)
> return imgs, lbls
> def _stratified_pick(labels, n_target, n_classes, rng):
> import numpy as np
> per_class = n_target // n_classes
> remainder = n_target - per_class * n_classes
> quotas = [per_class + (1 if c < remainder else 0) for c in range(n_classes)]
> picks: list[int] = []
> leftover = 0
> deficit_classes: list[int] = []
> for c in range(n_classes):
> idx = np.where(labels == c)[0]
> want = quotas[c]
> if len(idx) == 0:
> leftover += want
> continue
> if len(idx) <= want:
> picks.extend(idx.tolist())
> leftover += (want - len(idx))
> else:
> deficit_classes.append(c)
> chosen = rng.choice(idx, size=want, replace=False)
> picks.extend(chosen.tolist())
> if leftover > 0 and deficit_classes:
> pool = []
> for c in deficit_classes:
> avail = np.setdiff1d(
> np.where(labels == c)[0], np.array(picks, dtype=int)
> )
> pool.extend(avail.tolist())
> if pool:
> pool_arr = np.array(pool, dtype=int)
> take = min(leftover, len(pool_arr))
> extra = rng.choice(pool_arr, size=take, replace=False)
> picks.extend(extra.tolist())
> return sorted(picks)
> def _inverse_perm(perm):
> import numpy as np
> inv = np.full(len(perm), -1, dtype=int)
> for i, p in enumerate(perm):
> inv[p] = i
> assert (inv >= 0).all(), "permutation is not a bijection"
> return inv
> def prepare(raw: Path, public: Path, private: Path) -> None:
> import numpy as np
> import pandas as pd
> raw = Path(raw)
> public = Path(public)
> private = Path(private)
> public.mkdir(parents=True, exist_ok=True)
> private.mkdir(parents=True, exist_ok=True)
> train_img_dir = public / "train"
> test_img_dir = public / "test"
> train_img_dir.mkdir(parents=True, exist_ok=True)
> test_img_dir.mkdir(parents=True, exist_ok=True)
> curation_rng = np.random.RandomState(CURATION_SEED)
> n_classes_total = sum(n for _, n, _ in _INSCOPE)
> column_perm = (
> np.random.RandomState(CLASS_PERM_SEED)
> .permutation(n_classes_total)
> .tolist()
> )
> inv = _inverse_perm(column_perm)
> staging_rows: list[dict] = []
> staged_inscope: dict[int, np.ndarray] = {}
> staged_oos: dict[int, np.ndarray] = {}
> next_stage = 0
> for name, n_classes, offset in _INSCOPE:
> imgs, lbls = _load_npz(raw, name)
> picks = _stratified_pick(lbls, PER_INSCOPE_TARGET, n_classes, curation_rng)
> for idx in picks:
> sid = next_stage
> next_stage += 1
> global_c = offset + int(lbls[idx])
> anon = f"class_{int(inv[global_c]):02d}"
> staging_rows.append(
> {"_stage_id": sid, "modality": name,
> "class_label": anon, "is_oos": 0}
> )
> staged_inscope[sid] = imgs[idx]
> del imgs, lbls
> for name in _OOS:
> imgs, lbls = _load_npz(raw, name)
> n_classes = int(lbls.max()) + 1 if len(lbls) else 1
> picks = _stratified_pick(lbls, PER_OOS_TARGET, n_classes, curation_rng)
> for idx in picks:
> sid = next_stage
> next_stage += 1
> staging_rows.append(
> {"_stage_id": sid, "modality": name,
> "class_label": OOS_TOKEN, "is_oos": 1}
> )
> staged_oos[sid] = imgs[idx]
> del imgs, lbls
> n_total = next_stage
> id_perm = (
> np.random.RandomState(ID_PERM_SEED)
> .permutation(n_total)
> .astype(int)
> .tolist()
> )
> inscope_images: dict[int, np.ndarray] = {}
> oos_images: dict[int, np.ndarray] = {}
> all_rows: list[dict] = []
> for row in staging_rows:
> sid = int(row["_stage_id"])
> new_id = int(id_perm[sid])
> new_row = {
> "image_id": new_id,
> "modality": row["modality"],
> "class_label": row["class_label"],
> "is_oos": row["is_oos"],
> }
> if row["is_oos"]:
> oos_images[new_id] = staged_oos[sid]
> else:
> inscope_images[new_id] = staged_inscope[sid]
> all_rows.append(new_row)
> staging_rows.clear()
> staged_inscope.clear()
> staged_oos.clear()
> labels = pd.DataFrame(all_rows).sort_values("image_id").reset_index(drop=True)
> is_oos = labels["class_label"] == OOS_TOKEN
> inscope = labels.loc[~is_oos].copy()
> oos = labels.loc[is_oos].copy()
> rng = np.random.RandomState(SPLIT_SEED)
> train_parts, test_inscope_parts = [], []
> for (_mod, _cls), grp in inscope.groupby(
> ["modality", "class_label"], sort=True
> ):
> grp = grp.sort_values("image_id").reset_index(drop=True)
> n = len(grp)
> idx = np.arange(n)
> rng.shuffle(idx)
> n_train = int(round(n * TRAIN_FRACTION))
> train_parts.append(grp.iloc[idx[:n_train]])
> test_inscope_parts.append(grp.iloc[idx[n_train:]])
> train_df = pd.concat(train_parts, axis=0).reset_index(drop=True)
> test_inscope = pd.concat(test_inscope_parts, axis=0).reset_index(drop=True)
> noise_rng = np.random.RandomState(LABEL_NOISE_SEED)
> n_train = len(train_df)
> n_flip = int(round(n_train * LABEL_NOISE_FRACTION))
> if n_flip > 0:
> mod_to_classes = {
> m: sorted(grp["class_label"].unique().tolist())
> for m, grp in train_df.groupby("modality")
> }
> flip_idx = noise_rng.choice(n_train, size=n_flip, replace=False)
> new_labels = train_df["class_label"].to_numpy().copy()
> modalities = train_df["modality"].to_numpy()
> for i in flip_idx:
> current = new_labels[i]
> pool = [c for c in mod_to_classes[modalities[i]] if c != current]
> if not pool:
> continue
> new_labels[i] = pool[int(noise_rng.randint(0, len(pool)))]
> train_df = train_df.copy()
> train_df["class_label"] = new_labels
> pert_rng = np.random.RandomState(PERTURB_SEED)
> pert_mask = pert_rng.random(len(test_inscope)) < PERTURB_FRACTION_OF_TEST
> test_inscope["bucket"] = np.where(pert_mask, "PERTURBED", "INSCOPE")
> oos_test = oos.copy()
> oos_test["bucket"] = "OOS"
> test_df = pd.concat([test_inscope, oos_test], axis=0).reset_index(drop=True)
> def _xform_rng(iid: int):
> return np.random.RandomState(
> (BASE_XFORM_SEED ^ (int(iid) * 2654435761)) & 0xFFFFFFFF
> )
> for iid in train_df["image_id"]:
> iid = int(iid)
> arr = inscope_images[iid]
> im = _to_rgb_224(arr)
> im = _base_transform(im, _xform_rng(iid))
> im.save(
> str(train_img_dir / f"{iid:06d}.jpg"),
> format="JPEG", quality=92, optimize=True,
> )
> kinds = ("JPEG_Q30", "GAMMA", "BLUR_HARD", "CUTOUT", "ELASTIC", "CHANNEL_DROP")
> for _, row in test_df.iterrows():
> iid = int(row["image_id"])
> bucket = row["bucket"]
> arr = oos_images[iid] if bucket == "OOS" else inscope_images[iid]
> im = _to_rgb_224(arr)
> im = _base_transform(im, _xform_rng(iid))
> if bucket == "PERTURBED":
> chosen = pert_rng.choice(
> len(kinds), size=PERTURBATIONS_PER_IMAGE, replace=False
> )
> for kidx in chosen:
> im = _apply_perturbation(im, kinds[int(kidx)], pert_rng)
> im.save(
> str(test_img_dir / f"{iid:06d}.jpg"),
> format="JPEG", quality=92, optimize=True,
> )
> train_df[["image_id", "class_label"]].sort_values("image_id").reset_index(
> drop=True
> ).to_csv(str(public / "train.csv"), index=False)
> test_list = test_df[["image_id"]].sort_values("image_id").reset_index(drop=True)
> test_list.to_csv(str(public / "test.csv"), index=False)
> sample = test_list.copy()
> uniform = 1.0 / len(PROB_COLS)
> for c in PROB_COLS:
> sample[c] = uniform
> sample.to_csv(str(public / "sample_submission.csv"), index=False)
> test_df[["image_id", "class_label", "bucket"]].sort_values(
> "image_id"
> ).reset_index(drop=True).to_csv(str(private / "answers.csv"), index=False)
> ```
> ---
> ## 8) GPU Tier
> **Select:** **A10G** — standard single-GPU training of a 14-way medical image classifier on ≈ 2,400 images at 224×224 with a natural-image pretrained vision backbone (ResNet, DenseNet, ViT-B/S, DINOv2). Fits comfortably in 24 GB of VRAM. H100-class compute is not required.
> ---
> ## 9) What Not To Use
> Using any of the approaches below is grounds for solution rejection on review, regardless of leaderboard score.
> * **Identifying / downloading the upstream source images.** Do NOT attempt to pixel-hash, reverse-image-search, or otherwise match `public/train/` or `public/test/` images back to any external public image collection in order to recover the original per-image labels, modality identity, or class-name mapping that `prepare.py` anonymised away. Do NOT download any external image archive at training or inference time to reconstruct the mapping. The 14 anonymised classes and the OOS membership must be learned from `public/` alone.
> * **Hard-coded abstention rules based on source knowledge.** Building a rule-based "if it looks like modality X → abstain" classifier from external guesses about which modalities are held out. The abstention decision must come from an OOD / open-set mechanism trained on the provided in-scope data, not from externally-supplied modality tags.
> * **Hosted / closed-source API models** at any stage of training or inference (OpenAI, Anthropic, Google, Cohere, Mistral-API, xAI, etc.), including any distillation / pseudo-labelling from such teachers. Only open-weights models and self-trained pipelines are permitted.
> * **Externally pretrained OOD detectors or classifiers trained on the same underlying images.** Loading third-party checkpoints whose training set overlaps with the upstream collection these images were drawn from, if the overlap would give away the anonymised class or modality identity. Generic ImageNet / DINOv2 / CLIP / natural-image backbones are fine as long as they were not trained on the specific medical-imaging source.
> * **Probability-vector hacks that game the grader.** Submitting per-class independent sigmoids, unnormalised logits rescaled to sum to 1 only for the validator, deliberately over-smoothed distributions to artificially lower ECE while the argmax remains confident, or any trick that tries to decouple the argmax from the reported probability mass. Calibration is part of the grade.
> * **Grader / platform exploitation.** Hard-coded answer dictionaries, filesystem probes for `private/answers.csv`, attempts to read the `bucket` column, or any other channel that is not `public/train/` + `public/train.csv` + `public/test/` + `public/test.csv`.
> * **Ensembles mixing allowed and prohibited components.** An ensemble is allowed only if every component is itself trained (or used zero-shot) within the rules above. One prohibited component contaminates the whole ensemble.

Inspiration note: Useful as a retrieval-grounded task pattern with explicit context selection, answer scoring, and a metric-friendly prediction target.

## Multi-Source Compliance Resolution Challenge accepted
- Challenge URL: https://drive.google.com/drive/folders/1bZgeW-ObiqNIjMxoUNrjejACCvdqb7bF
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: RAG (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: Accepted (from Drive folder name)
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: Not shown/captured
- Tags: Not shown/captured
- Best/top context found: Multi-Source Compliance Resolution Challenge_accepted from shared Google Drive folder

Full challenge description from Drive:

> # Challenge creation form — fill-in
> Tie this challenge to the **accepted dataset**: Multi-Source Compliance Inspection Resolution Dataset (Synthetic).
> ---
> ## 1) Difficulty
> **Select:** **Hard**
> ---
> ## 2) Challenge Title
> ```
> Multi-Source Compliance Resolution Challenge
> ```
> ---
> ## 3) Problem Description
> ```markdown
> # Multi-Source Compliance Resolution Challenge
> ## Overview
> This is a **sequence-to-sequence** task requiring **multi-document reasoning**, **rule interpretation**, and **structured output generation**.
> You are given fictional environmental compliance inspection data. For each facility visit, 2–4 independent inspectors filed separate fragments describing their findings. These fragments may **contradict each other** — different inspectors may report different violations, and some fragments may be partially corrupted (`[CORRUPTED]` spans).
> Each row also includes a **compliance codebook** — a set of 4–15 natural language rules specific to that row. These rules govern:
> - **Contradiction resolution:** Whether a violation is confirmed if *any* inspector reports it, or only if a *majority* do.
> - **Severity escalation:** Conditions that raise the severity level (e.g., violation count thresholds, facility sector, corrupted data fallback).
> - **Action assignment:** Mapping from severity levels to required actions.
> - **Penalty mapping:** Mapping from actions to penalty tiers, with optional caps.
> Your task is to **read the inspector fragments, apply the codebook rules in order, and produce the exact 6-field structured verdict string**.
> **Output format:**
> ```
> FACILITY:KRX-0447 | VIOLATIONS:leak,emission_excess | COUNT:2 | SEVERITY:elevated | ACTION:reinspect_30d | PENALTY:tier_B
> ```
> **Why this is hard:**
> - **Multi-source contradictions:** Inspectors disagree; you must apply the correct reconciliation rule (any-flags vs majority-vote) for each violation type.
> - **Variable codebook:** Rules change per row — you cannot memorize a single rule set.
> - **Chained inference:** PENALTY depends on ACTION, which depends on SEVERITY, which depends on reconciled VIOLATIONS. One mistake cascades.
> - **Decoy rules:** Some codebook rules reference violation types not present in any fragment — they must be correctly ignored.
> - **Corrupted fragments:** Missing data triggers fallback rules that override normal severity.
> - **Rule ordering:** Rules are applied sequentially; later rules can override earlier ones.
> ## Evaluation
> Submissions are scored using **per-field exact match accuracy** across all 6 verdict fields, averaged over all test rows.
> For each row:
> - Parse both the predicted and true verdict into 6 fields (FACILITY, VIOLATIONS, COUNT, SEVERITY, ACTION, PENALTY).
> - Compare each field: exact match = 1, mismatch = 0.
> - Row score = (number of matching fields) / 6.
> Final score = mean of all row scores. **Higher is better.** Range: [0.0, 1.0].
> **Baseline scores:**
> - All-default verdict: ~0.24
> - Perfect: 1.0
> ## Dataset (prepared)
> **In public/:**
> - **train.csv** — id, input, verdict. Exactly 16,000 rows (stratified 80% split by severity).
> - **test.csv** — id, input. Exactly 4,000 rows. No verdict column.
> - **sample_submission.csv** — id, verdict. Example format with placeholder verdicts.
> **In private/ (not visible to solvers):** answers.csv — id, verdict.
> **Column descriptions:**
> | Column  | Type   | Description |
> |---------|--------|-------------|
> | id      | int    | Unique row identifier |
> | input   | string | Multi-line text: 2–4 inspector fragments + compliance codebook (4–15 rules). Rules may be shuffled, paraphrased, or include decoy rules referencing absent violation types. ~25% of fragments have injected noise sentences. |
> | verdict | string | 6-field structured verdict: `FACILITY:X \| VIOLATIONS:Y \| COUNT:Z \| SEVERITY:W \| ACTION:A \| PENALTY:P` |
> **Verdict fields:**
> | Field      | Values | Description |
> |------------|--------|-------------|
> | FACILITY   | e.g. KRX-0447 | Facility ID from fragments |
> | VIOLATIONS | comma-separated list or "none" | Confirmed violations after reconciliation |
> | COUNT      | integer | Number of confirmed violations |
> | SEVERITY   | negligible, low, moderate, elevated, high, critical | Derived severity after all escalation rules |
> | ACTION     | no_action, log_only, reinspect_30d, reinspect_7d, immediate_halt, partial_shutdown, full_shutdown | Action derived from severity mapping rules |
> | PENALTY    | none, tier_A, tier_B, tier_C, tier_D, tier_E | Penalty derived from action mapping rules, possibly capped |
> ## Submission
> Submit a CSV with exactly these columns:
> | Column  | Type   | Description |
> |---------|--------|-------------|
> | id      | int    | Row identifier from test.csv |
> | verdict | string | Predicted 6-field verdict string |
> **Requirements:**
> - Exactly **4,000 rows** (one per test row). No duplicate ids.
> - Header row required.
> - Verdict must follow the exact format: `FACILITY:X | VIOLATIONS:Y | COUNT:Z | SEVERITY:W | ACTION:A | PENALTY:P`
> **Example:**
> ```
> id,verdict
> 42,FACILITY:KRX-0447 | VIOLATIONS:leak,emission_excess | COUNT:2 | SEVERITY:elevated | ACTION:reinspect_30d | PENALTY:tier_B
> 99,FACILITY:VLN-1234 | VIOLATIONS:none | COUNT:0 | SEVERITY:negligible | ACTION:no_action | PENALTY:none
> ```
> ```
> ---
> ## 4) Tags
> **Select:** **text**, **generative**
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
> VERDICT_FIELDS = ["FACILITY", "VIOLATIONS", "COUNT", "SEVERITY", "ACTION", "PENALTY"]
> def _parse_verdict(verdict_str: str) -> dict:
> if not isinstance(verdict_str, str):
> return {}
> fields = {}
> for part in verdict_str.split(" | "):
> if ":" in part:
> key, val = part.split(":", 1)
> fields[key.strip()] = val.strip()
> return fields
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> """
> Score using per-field exact match on structured verdict strings.
> Args:
> submission: Agent predictions. Columns: id, verdict.
> answers: Ground truth. Columns: id, verdict.
> Returns:
> Float in [0, 1]. Direction: maximize.
> """
> try:
> if "id" not in submission.columns or "verdict" not in submission.columns:
> raise ValueError("Submission must have columns: id, verdict")
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
> raise ValueError(f"Submission missing ids: {len(missing)}")
> if extra:
> raise ValueError(f"Submission has extra ids: {len(extra)}")
> merged = answers.merge(submission, on="id", how="left", suffixes=("_true", "_pred"))
> if merged["verdict_pred"].isna().any():
> raise ValueError("Submission has missing predictions for some rows after merge")
> row_scores = []
> for _, row in merged.iterrows():
> true_fields = _parse_verdict(row["verdict_true"])
> pred_fields = _parse_verdict(row["verdict_pred"])
> if not true_fields:
> row_scores.append(0.0)
> continue
> matches = 0
> total = len(VERDICT_FIELDS)
> for field in VERDICT_FIELDS:
> true_val = true_fields.get(field, "")
> pred_val = pred_fields.get(field, "")
> if true_val == pred_val:
> matches += 1
> row_scores.append(matches / total)
> if not row_scores:
> return 0.0
> score = float(np.mean(row_scores))
> if np.isnan(score):
> return 0.0
> return score
> except ValueError:
> raise
> except Exception as e:
> raise RuntimeError(f"Grading failed: {e}") from e
> ```
> ---
> ## 7) Data Preparation Pipeline
> **Input:** raw dataset file **data.csv** (id, input, verdict).
> **Script — prepare.py:**
> *(See prepare.py file — obfuscation includes: 60% rule shuffling, 40% fragment shuffling, 50% decoy rule injection, 30% rule paraphrasing, 25% noise injection into fragments. Stratified 80/20 split by severity.)*
> Run **Run Prepare** after pasting.
> ---
> ## 8) Evaluation Rubrics
> Add each via "Add Rubric":
> **1** — DATA_HANDLING | REQUIRED
> **Criterion:** Parses the multi-line input text to extract inspector fragments and codebook rules as separate structured components.
> **Rationale:** The input contains two distinct sections (fragments and codebook) that must be parsed independently. Treating the entire input as flat text loses the structural information needed for rule application.
> **2** — FEATURE_ENGINEERING | RECOMMENDED
> **Criterion:** Extracts violation types mentioned in each inspector fragment and tracks which inspector reported which violations.
> **Rationale:** Contradiction resolution rules (any-flags vs majority-vote) require knowing per-inspector violation reports, not just the union of all mentioned violations.
> **3** — MODELING | RECOMMENDED
> **Criterion:** Implements or learns the codebook rule application logic, applying rules sequentially to derive the verdict fields in dependency order (violations → severity → action → penalty).
> **Rationale:** The chained dependency structure means fields must be derived in order; applying rules out of order or independently will produce incorrect verdicts.
> **4** — DATA_HANDLING | RECOMMENDED
> **Criterion:** Handles corrupted fragments (`[CORRUPTED]` spans) by detecting corruption markers and applying fallback rules from the codebook rather than ignoring or hallucinating the missing content.
> **Rationale:** ~15% of fragments are corrupted; the codebook specifies explicit fallback severity rules for corrupted data that override normal derivation.
> **5** — FEATURE_ENGINEERING | RECOMMENDED
> **Criterion:** Identifies and correctly ignores decoy codebook rules that reference violation types not present in any inspector fragment.
> **Rationale:** ~50% of prepared rows contain decoy rules; applying them would incorrectly add violations or change severity for non-existent findings.
> **6** — CODE_QUALITY | REQUIRED
> **Criterion:** Submission CSV has columns `id` and `verdict` with exactly one row per test id, no duplicate ids, and verdict strings follow the required 6-field pipe-delimited format.
> **Rationale:** Grader expects this exact format; malformed verdicts will score 0 on all fields.
> **7** — TRAINING | RECOMMENDED
> **Criterion:** Uses the training data to learn or validate rule interpretation patterns, rather than relying solely on zero-shot LLM generation without reference to training examples.
> **Rationale:** The variable codebook and paraphrased rules mean that learning from training examples (where both input and verdict are visible) provides signal about rule semantics and edge cases.
> **8** — UNIVERSAL | UNIVERSAL
> **Criterion:** Does not use test set verdicts for training, feature computation, or rule calibration.
> **Rationale:** Universal anti-leakage criterion.
> ---
> ## 9) Agent Evaluation Runs
> No fill; runs on submit.
> ---
> ## Checklist
> - [ ] Dataset: Multi-Source Compliance Inspection Resolution Dataset (Synthetic) accepted and selected
> - [ ] Difficulty: Hard
> - [ ] Title: Multi-Source Compliance Resolution Challenge
> - [ ] Problem description: 16,000 / 4,000 rows, 6-field verdict, per-field exact match, maximize, min 0 max 1
> - [ ] Tags: text, generative
> - [ ] Grading: Maximize; min 0; max 1
> - [ ] Grading script: per-field exact match; merge left; id/length validation; try/except
> - [ ] Prepare: shuffle rules 60%, shuffle fragments 40%, decoy rules 50%, paraphrase 30%, noise 25%; stratified 80/20 split
> - [ ] 8 rubrics added (2 REQUIRED, 5 RECOMMENDED, 1 UNIVERSAL)

Inspiration note: Useful as an evidence-grounded pattern where the output depends on resolving or ranking retrieved facts rather than memorizing labels.

## Contradictory Evidence Retrieval Challenge
- Challenge URL: https://drive.google.com/drive/folders/1fUUCc16vEMDJGFge63zhIDkhLdZkI2L0
- Source file: CHALLENGE_FORM_FILL.md
- DOMAIN used for this document: RAG (inferred from Drive folder/spec text when no explicit domain field was present)
- Status: Accepted/approved example from shared Drive folder
- Difficulty: Not shown/captured
- GPU: Not shown/captured
- Scoring: Not shown/captured
- Tags: Not shown/captured
- Best/top context found: Contradictory Evidence Retrieval Challenge from shared Google Drive folder

Full challenge description from Drive:

> # Challenge creation form — fill-in
> Tie this challenge to the **accepted dataset**: Multi-Stance Claim Verification Passage Corpus (Synthetic).
> ---
> ## 1) Difficulty
> **Select:** **Hard**
> ---
> ## 2) Challenge Title
> ```
> Contradictory Evidence Retrieval Challenge
> ```
> ---
> ## 3) Problem Description
> ```markdown
> # Contradictory Evidence Retrieval Challenge
> ## Overview
> This is a **RAG (Retrieval-Augmented Generation)** task requiring **evidence retrieval**, **contradictory reasoning**, and **structured output generation**.
> You are given fictional scientific claims, each paired with a corpus of 8–15 evidence passages from fictional research institutions. Your task is to analyze the passages, determine which ones constitute genuine evidence for or against the claim, assess the overall stance, and produce a structured verdict.
> **What makes this hard:**
> - **Near-miss distractors:** Some passages mention the same substance or the same effect as the claim, but not both. They appear topically relevant but are not actual evidence.
> - **Hedged passages:** Some passages mention the correct substance and effect but use uncertain, preliminary, or inconclusive language. These should not be counted as evidence.
> - **Contradictory evidence:** Supporting and contradicting passages coexist. The model must weigh them to determine the overall stance.
> - **Confidence estimation:** Confidence depends on the ratio of evidence imbalance, requiring the model to count and compare evidence types accurately.
> - **Evidence ID tracking:** The model must identify the exact passage IDs of all genuine evidence passages (both supporting and contradicting), excluding distractors and hedged passages.
> **Input per row:**
> - A **claim** sentence asserting that a fictional substance improves a material property under specific conditions.
> - A **passages** field containing 8–15 numbered passages `[P1]`, `[P2]`, etc.
> **Output per row:**
> A structured verdict string with 3 fields:
> ```
> STANCE:support | EVIDENCE_IDS:2,5,7,9 | CONFIDENCE:medium
> ```
> - **STANCE:** `support`, `contradict`, or `insufficient`
> - **EVIDENCE_IDS:** Comma-separated 1-indexed passage IDs of all genuine evidence passages (both supporting and contradicting), or `none`
> - **CONFIDENCE:** `high`, `medium`, or `low`
> ## Evaluation
> Submissions are scored using **per-field exact match accuracy** across all 3 verdict fields, averaged over all test rows.
> For each row:
> - Parse both the predicted and true verdict into 3 fields (STANCE, EVIDENCE_IDS, CONFIDENCE).
> - Compare each field: exact match = 1, mismatch = 0. For EVIDENCE_IDS, the comparison is set-based (order does not matter within the comma-separated list).
> - Row score = (number of matching fields) / 3.
> Final score = mean of all row scores. **Higher is better.** Range: [0.0, 1.0].
> **Baseline scores:**
> - Constant guess: ~0.18
> - Perfect: 1.0
> ## Dataset (prepared)
> **In public/:**
> - **train.csv** — id, claim, passages, verdict. Exactly 16,000 rows (stratified 80% split by stance).
> - **test.csv** — id, claim, passages. Exactly 4,000 rows. No verdict column.
> - **sample_submission.csv** — id, verdict. Example format with placeholder verdicts.
> **In private/ (not visible to solvers):** answers.csv — id, verdict.
> **Column descriptions:**
> | Column   | Type   | Description |
> |----------|--------|-------------|
> | id       | int    | Unique row identifier |
> | claim    | string | A sentence asserting that a fictional substance improves a specific material property under specific environmental conditions. |
> | passages | string | 8–17 numbered passages `[P1]`, `[P2]`, etc. Each passage is a single sentence from a fictional research institution describing experimental findings. Passages may have institution names abbreviated, years redacted, methods removed, or cross-references to other passage IDs injected. Some rows include additional hedged decoy passages added during preparation. |
> | verdict  | string | 3-field structured verdict: `STANCE:<stance> | EVIDENCE_IDS:<ids> | CONFIDENCE:<conf>` |
> **Verdict fields:**
> | Field        | Values | Description |
> |--------------|--------|-------------|
> | STANCE       | support, contradict, insufficient | Overall stance of evidence toward the claim |
> | EVIDENCE_IDS | comma-separated integers or "none" | IDs of all genuine evidence passages (sorted ascending) |
> | CONFIDENCE   | high, medium, low | Confidence level derived from evidence balance |
> ## Submission
> Submit a CSV with exactly these columns:
> | Column  | Type   | Description |
> |---------|--------|-------------|
> | id      | int    | Row identifier from test.csv |
> | verdict | string | Predicted 3-field verdict string |
> **Requirements:**
> - Exactly **4,000 rows** (one per test row). No duplicate ids.
> - Header row required.
> - Verdict must follow the exact format: `STANCE:<stance> | EVIDENCE_IDS:<ids> | CONFIDENCE:<conf>`
> **Example:**
> ```
> id,verdict
> 42,STANCE:support | EVIDENCE_IDS:2,5,7,9 | CONFIDENCE:medium
> 99,STANCE:contradict | EVIDENCE_IDS:1,3,6 | CONFIDENCE:high
> ```
> ```
> ---
> ## 4) Tags
> **Select:** **text**, **generative**
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
> VERDICT_FIELDS = ["STANCE", "EVIDENCE_IDS", "CONFIDENCE"]
> def _parse_verdict(verdict_str: str) -> dict:
> if not isinstance(verdict_str, str):
> return {}
> fields = {}
> for part in verdict_str.split(" | "):
> if ":" in part:
> key, val = part.split(":", 1)
> fields[key.strip()] = val.strip()
> return fields
> def _normalize_evidence_ids(ids_str: str) -> str:
> ids_str = ids_str.strip().lower()
> if ids_str in ("none", "", "n/a"):
> return "none"
> try:
> ids = sorted(int(x.strip()) for x in ids_str.split(",") if x.strip())
> return ",".join(str(i) for i in ids)
> except ValueError:
> return ids_str
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> """
> Score using per-field exact match on structured verdict strings.
> Args:
> submission: Agent predictions. Columns: id, verdict.
> answers: Ground truth. Columns: id, verdict.
> Returns:
> Float in [0, 1]. Direction: maximize.
> """
> try:
> if "id" not in submission.columns or "verdict" not in submission.columns:
> raise ValueError("Submission must have columns: id, verdict")
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
> raise ValueError(f"Submission missing ids: {len(missing)}")
> if extra:
> raise ValueError(f"Submission has extra ids: {len(extra)}")
> merged = answers.merge(submission, on="id", how="left", suffixes=("_true", "_pred"))
> if merged["verdict_pred"].isna().any():
> raise ValueError("Submission has missing predictions for some rows after merge")
> row_scores = []
> for _, row in merged.iterrows():
> true_fields = _parse_verdict(row["verdict_true"])
> pred_fields = _parse_verdict(row["verdict_pred"])
> if not true_fields:
> row_scores.append(0.0)
> continue
> matches = 0
> total = len(VERDICT_FIELDS)
> for field in VERDICT_FIELDS:
> true_val = true_fields.get(field, "")
> pred_val = pred_fields.get(field, "")
> if field == "EVIDENCE_IDS":
> true_val = _normalize_evidence_ids(true_val)
> pred_val = _normalize_evidence_ids(pred_val)
> if true_val.strip().lower() == pred_val.strip().lower():
> matches += 1
> row_scores.append(matches / total)
> if not row_scores:
> return 0.0
> score = float(np.mean(row_scores))
> if np.isnan(score):
> return 0.0
> return score
> except ValueError:
> raise
> except Exception as e:
> raise RuntimeError(f"Grading failed: {e}") from e
> ```
> ---
> ## 7) Data Preparation Pipeline
> **Input:** raw dataset file **data.csv** (id, claim, passages, verdict).
> **Script — prepare.py:**
> *(See prepare.py file — obfuscation includes: 35% passage paraphrasing via synonym substitution, 50% institution name abbreviation, 30% method citation removal, 25% year redaction, 20% cross-reference noise injection, 40% hedged decoy passage injection, full passage shuffle with evidence ID remapping. Stratified 80/20 split by stance.)*
> Run **Run Prepare** after pasting.
> ---
> ## 8) Evaluation Rubrics
> Add each via "Add Rubric":
> **1** — DATA_HANDLING | REQUIRED
> **Criterion:** Parses the claim and numbered passages from the input, correctly extracting each passage's text and its passage ID.
> **Rationale:** The input contains a claim and 8–17 numbered passages that must be individually parsed. Treating passages as a single block of text loses the per-passage identity needed for evidence ID prediction.
> **2** — MODELING | REQUIRED
> **Criterion:** Produces a verdict string in the exact required format with all 3 fields (STANCE, EVIDENCE_IDS, CONFIDENCE) separated by ` | `.
> **Rationale:** The grader parses the verdict by splitting on ` | ` and `:`. Malformed verdicts will score 0 on all fields.
> **3** — TRAINING | RECOMMENDED
> **Criterion:** Uses the training data to learn patterns from examples where both input and verdict are visible, rather than relying solely on zero-shot generation.
> **Rationale:** The training set provides 16,000 labeled examples that reveal the relationship between passage content and verdict fields. Models that leverage this signal will outperform zero-shot approaches.
> **4** — DATA_HANDLING | RECOMMENDED
> **Criterion:** Handles obfuscation artifacts in passages, including abbreviated institution names, redacted years (`[YEAR]`), removed method citations, and injected cross-references (`cf. PN`).
> **Rationale:** The preparation pipeline introduces these artifacts; models that are robust to them will perform better than those that rely on clean passage formatting.
> **5** — UNIVERSAL | UNIVERSAL
> **Criterion:** Does not use test set verdicts for training, feature computation, or model calibration.
> **Rationale:** Universal anti-leakage criterion.
> ---
> ## 9) Agent Evaluation Runs
> No fill; runs on submit.
> ---
> ## Checklist
> - [ ] Dataset: Contradictory Evidence Retrieval Dataset (Synthetic) accepted and selected
> - [ ] Difficulty: Hard
> - [ ] Title: Contradictory Evidence Retrieval Challenge
> - [ ] Problem description: 16,000 / 4,000 rows, 3-field verdict, per-field exact match, maximize, min 0 max 1
> - [ ] Tags: text, generative
> - [ ] Grading: Maximize; min 0; max 1
> - [ ] Grading script: per-field exact match with evidence ID normalization; merge left; id/length validation; try/except
> - [ ] Prepare: paraphrase 35%, abbreviate institutions 50%, remove methods 30%, redact years 25%, cross-references 20%, hedged decoys 40%; full shuffle; stratified 80/20 split
> - [ ] 5 rubrics added (2 REQUIRED, 2 RECOMMENDED, 1 UNIVERSAL)

Inspiration note: Useful as an evidence-grounded pattern where the output depends on resolving or ranking retrieved facts rather than memorizing labels.

## Mobile App Privacy Policy Evidence Routing
- Challenge URL: https://shipd.ai/quests/eris/challenges/jx790vw136j4rm7tx9zdqjp5zh89wx4t
- DOMAIN exactly as displayed: RAG
- Status: Accepted
- Difficulty: Medium
- GPU: A10G
- Scoring: ↓ Lower is better
- Tags: Not shown/captured
- Best/top context found: Added from pending Shipd retry batch on 2026-07-06; no leaderboard rank context captured.

Full challenge description from page:

> Overview
> Privacy-policy assistants need to answer user questions by finding the small parts of a long policy that actually support the answer. This challenge asks you to rank policy segments for privacy questions using expert relevance annotations.
> Each row in test.csv is one candidate policy segment for a question. For every query_id, rank the five candidate segments most likely to be relevant. The hidden labels come from expert PrivacyQA annotations, but this task uses a new deterministic policy-disjoint split from the source train file rather than the published PrivacyQA test split.
> This is an NLP / RAG-style evidence-routing task. Strong solutions should learn privacy-policy language, not only keyword overlap. Many irrelevant segments share words like "data", "information", "share", "collect", and "third party" with the question, while the relevant segment often depends on the specific privacy practice being asked about.
> Dataset
> File descriptions
> train.csv -- 102,099 candidate policy segments from 710 labeled questions. It includes the target relevance.
> test.csv -- 30,978 candidate policy segments from 215 held-out questions. It has the same input columns as train.csv, without relevance.
> train.jsonl -- Query-level mirror of the training data with candidate segments grouped under each question and relevant candidate IDs included.
> test.jsonl -- Query-level mirror of the test data with candidate segments grouped under each question and no labels.
> corpus.txt -- Plain-text public training corpus containing grouped questions and candidate policy segments.
> sample_submission.csv -- A random valid submission with one row per query_id and five pipe-separated candidate IDs.
> Column descriptions
> query_id (string) -- Hashed identifier for a privacy question. All rows with the same query_id form one ranking group.
> policy_id (string) -- Hashed identifier for the privacy policy containing the candidate segments.
> candidate_id (string) -- Hashed identifier for one candidate policy segment.
> question (string) -- Deidentified user question about a privacy practice.
> policy_segment (string) -- Deidentified candidate sentence or segment from the policy.
> relevance (integer) -- Training target only. 1 means an expert marked the segment as relevant to the question; 0 means it was not marked relevant.
> Evaluation
> Submissions are scored using Privacy Evidence Routing Loss. Lower is better.
> For each query_id, the grader reads your five ranked candidate IDs and computes:
> utility = 0.70  *ndcg_at_5 + 0.30*  average_precision_at_5
> score = 100 * (1 - mean(utility over queries))
> ndcg_at_5 rewards placing relevant policy segments near the top. average_precision_at_5 rewards retrieving multiple relevant segments when a question has more than one relevant segment. A perfect submission scores 0; a poor ranking approaches 100.
> Submission
> Submit a CSV file with one row for every question in test.csv.
> query_id (string) -- The hashed question identifier from test.csv.
> ranked_candidate_ids (string) -- Exactly five candidate_id values from that query group, ordered best to worst and separated by |.
> Example:
> query_id,ranked_candidate_ids
> 0143731fd93e,3cf97dd50a51|8b0eb026585d|36d0469f1f38|226cde2f30a2|ea37ed474dd4
> 03ff2b827b37,1e9673b1cd99|6e89e79a692e|47aa3ff894ee|2a954fca65b3|bd00b4447427
> Requirements
> The file must contain exactly 215 rows plus the header.
> Every query_id from test.csv must appear exactly once.
> Each ranked_candidate_ids value must contain exactly five candidate IDs.
> Candidate IDs must be valid for that same query_id.
> Candidate IDs may not be repeated within a row.
> File format: .csv only, with exact column names query_id,ranked_candidate_ids.
> What Not To Use
> Do not attempt to recover held-out relevance labels.
> Do not reverse map hashed IDs back to source DocID, QueryID, or SentID values.
> Do not search exact policy segments or questions on the web to identify the original app policy record.
> Do not hardcode query-specific candidate rankings or cached labels from outside dataset/public/.

Inspiration note: Useful because it makes retrieval, evidence selection, or citation routing the measurable core of the challenge.

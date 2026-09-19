# CPU LLM Evaluation Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed CPU examples in this document: 7

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.

## Code Summary Faithfulness Without Identifier Names

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a2gg0a7eckbzk6kr6smv9858a6r5c
- DOMAIN exactly as displayed: LLM Evaluation
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat krishrighty's score of 0.608!

Full challenge description from page:

> Judging Whether a Code Summary Is Faithful to Its Function
> Overview
> Language models are increasingly used to write and rewrite the one-sentence summaries that document code, and the critical quality question is whether a produced summary is faithful to the function or whether it hallucinates: it attributes a role to the wrong argument, and so asserts something the code does not do. A confidently wrong summary is worse than none at all.
> This challenge is a faithfulness / hallucination-detection task, an evaluation of a candidate output rather than a generation task. You are given a Python function and a candidate one-sentence summary of it, and you must judge whether the summary is faithful to the code. Two things stand in the way, and each removes a different shortcut.
> The evidence is executable code, not prose, and it is the only evidence. The parameters of every function have been renamed to p0, p1, p2 and so on. Nothing can be inferred from what they are called. The summary's claim is about program semantics: which argument is consumed where, which name is bound to which value, what the control flow guards and what is returned. To judge it you have to trace the function, recover the role each parameter plays in its logic, and check the summary's assignment of roles against it.
> And you are never told which training example is faithful. The training pairs arrive in bags of five, and for each bag you are given only a number: how many of its five summaries are faithful, always between 1 and 4. Never 0 and never 5, so a count never pins down an individual verdict. A judge that expects a label on every training pair has nothing to train on; the per-example verdicts have to be recovered from the bag totals first. Removing the names defeats a solver that reads the summary alone; removing the per-example labels defeats one that trains an ordinary supervised detector on the pairs.
> Task
> Given a code (a Python function with its docstring removed and its parameters renamed) and a candidate docstring, output your verdict as prediction: 1 if the summary is faithful to the code, 0 if it contains a hallucinated inconsistency.
> Worked example
> Consider this function and this summary:
> def load(p0, p1):
> with open(p1, "rb") as fh:
> p0.load_state_dict(pickle.load(fh))
> return p0
> "Load a p0 from the given p1."
> That pair is faithful: p1 is opened, p0 receives the state. Now the same function with a different candidate summary:
> "Load a p1 from the given p0."
> That one is hallucinated, and the only thing that says so is the body.
> Had the parameters kept their real names, model and path, you would not need the body at all. Everybody knows that models are loaded and paths are read from, so a judge could answer from English alone and never look at the code. The opaque names take that away.
> Why the easy answers do not work
> For every function in this challenge, the faithful and the hallucinated example share the identical code, character for character. The corruption exchanges two parameters inside the summary and leaves the body untouched. Each of the following was measured on this exact split, where a coin flip scores 0.500 and judging everything one way scores 0.333:
> Word overlap or keyword matching cannot help: both summaries draw on the same parameters and the same vocabulary.
> A bag-of-words model over the summary scores 0.53, and over the code and summary together 0.53. There is nothing lexical to find.
> Reading the parameter names cannot help, because there are no names, only p0, p1, p2.
> Counting positions cannot help. The parameters are renamed by their position in the signature, and the signature itself is shuffled first, so the numbering never sees the summary. "Does the summary mention p0 first?" scores 0.533, "are the numbers in ascending order?" scores 0.526, and "does the summary mention them in the order the code does?" scores 0.524. All three are chance.
> A fluency or grammar check cannot help: the corrupted summary is left grammatical, and only parameters at least two words apart are ever exchanged.
> A tool or lookup cannot help: no off-the-shelf checker decides whether a summary describes a function, and the function has been rewritten.
> Where a function offers several swappable parameter pairs, the pair whose usage in the body is hardest to tell apart is the one exchanged. The remaining path is to understand the program.
> Data
> All inputs are under dataset/public/:
> train.csv: training pairs, without a per-example verdict. Columns:
> id (string): unique row id.
> code (string): the Python function source, docstring removed, parameters renamed to p0, p1, ...
> docstring (string): a candidate one-sentence summary.
> bag_id (string): the bag this pair belongs to. Every bag holds exactly five pairs.
> train_bags.csv: the only training supervision. Columns:
> bag_id (string): a bag of five training pairs.
> n_faithful (int): how many of that bag's five summaries are faithful. Always between 1 and 4: a bag that came out all faithful or all hallucinated is not released, so a count never gives away an individual verdict. Which ones are faithful is never stated.
> test.csv: pairs to judge; columns id, code, docstring (no target).
> sample_submission.csv: a correctly formatted example for every test id (its baseline judges everything faithful).
> The reference verdicts for the test pairs are held out privately and used only for scoring. The two verdicts are balanced (about 50% faithful).
> Train and test share no code. Functions are grouped before anything else happens, by their source class where the name gives one and otherwise by the shape of their syntax tree, and a group goes wholly to one side. A near-duplicate of a test function cannot be sitting in the training set.
> Evaluation
> Verdicts are scored by macro-averaged F1 over the two verdicts (faithful and hallucinated), so judging everything one way does not win:
> for each verdict v in {0, 1}:  F1_v = 2*TP / (2*TP + FP + FN)
> score = mean(F1_0, F1_1)                              (higher is better, range 0 to 1)
> Judging everything one way scores about 0.333, a coin flip scores 0.500, a perfect judgement scores 1. A learned judge over structural usage features, trained on labels recovered from the bag counts, reaches 0.53 in local checks, so there is real headroom for a solver that genuinely reads the code.
> Submission format
> Write ./working/submission.csv with exactly these columns:
> id,prediction
> c_1a2b3c4d5e6f7a8b,1
> c_2b3c4d5e6f7a8b9c,0
> ...
> One row per id in test.csv. Any id you leave out is counted as a wrong prediction, so cover them all; rows for ids that are not in test.csv are ignored.
> prediction is 1 (faithful) or 0 (hallucinated). Start from sample_submission.csv to guarantee the correct id set, and write with index=False.
> Constraints
> Read the challenge inputs only from ./dataset/public/. Write your output only to ./working/submission.csv.
> No package installs (no pip or conda install). You may use the preinstalled libraries (numpy, pandas, scikit-learn, nltk, pytorch, transformers, and so on) and pretrained models from the standard model hubs.
> Must finish within the grading time budget on the provided hardware.
> What Not To Use
> Do not retrieve this challenge's source functions or their original docstrings to recover the verdicts (for example by looking the code up on the public internet). Judge only from the provided code and docstring.
> Do not hardcode outputs or otherwise bypass learning from the data.
> A learning-based judge is expected, and because no pair carries its own label, the bag counts have to be used indirectly: infer each pair's verdict from the counts and train on the inferred labels, iterate that against your own predictions, or optimise a bag-level objective directly. On top of that, the judge has to read the code, since the names give nothing away: a model that encodes the function with the candidate summary and checks their agreement, features derived from the function's structure (argument positions, bindings, control flow, return expression), or a preinstalled language model prompted to trace the function and decide whether the summary assigns each parameter its true role.

Inspiration note: Useful because it evaluates model outputs or reasoning artifacts through compact evidence-based judgments instead of generic preference scoring.

## Minimum Evidence Certificates for LLM Judge Failure

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71t7qrky2j33yj30dydzrc1x89nprk
- DOMAIN exactly as displayed: LLM Evaluation
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Automated judges can fail differently across evaluation criteria and scenario conditions. A useful audit should do more than label every trace independently: it should return a compact, mechanically checkable set of examples that demonstrates the failure pattern.
> In this challenge, each scenario contains 45 encoded evaluation traces spanning five criteria and three automated judges. Your submission must generate a five-claim audit certificate. The certificate must prove that the judge panel exhibits both high-score and low-score failures, while supplying one correct witness for every criterion and covering all three judges.
> The grader verifies the certificate directly against hidden audited scores. There is no single target certificate: many different five-trace sets can receive full credit. The task is constrained evidence selection with a verifiable output contract rather than independent pointwise predictions.
> The records come from controlled assistant-response evaluations under anonymous scenario, system, cohort, criterion, and judge conditions. Free-text rationales are represented by stable token codes. All scenario groups in test are absent from train.
> Witness States
> For a trace, define delta = judge_score - audited_score.
> State	Hidden condition	Meaning
> JUDGE_HIGH	delta >= 1.0	The automated judge scored at least one point too high.
> JUDGE_LOW	delta <= -1.0	The automated judge scored at least one point too low.
> NO_WITNESS	-1.0 < delta < 1.0	The trace cannot serve as a failure witness.
> Training traces include witness_state. Test traces do not.
> Task
> For each test scenario, submit one audit_certificate containing exactly five distinct trace claims.
> Certificate grammar:
> TRACE_ID:JUDGE_HIGH;TRACE_ID:JUDGE_LOW;TRACE_ID:JUDGE_HIGH;TRACE_ID:JUDGE_HIGH;TRACE_ID:JUDGE_LOW
> A full-valid certificate must satisfy every condition below:
> Every claimed direction is correct for its trace.
> The five correct traces cover all five criterion_code values.
> The five correct traces cover all three judge_code values.
> The correct claims include at least one JUDGE_HIGH and one JUDGE_LOW witness.
> Because the certificate has five claims and there are five criteria, a full-valid certificate contains exactly one correct witness per criterion.
> Dataset
> The public dataset contains three files.
> File	Rows	Description
> train_scenarios.jsonl	14	Training scenarios containing 45 labeled evaluation traces each.
> test_scenarios.jsonl	4	Held-out scenarios containing 45 unlabeled evaluation traces each.
> sample_submission.csv	4	Syntactically valid example certificates with placeholder claims.
> train_scenarios.jsonl Fields
> Field	Type	Description
> scenario_id	string	Unique anonymous scenario identifier.
> traces	array of objects	Exactly 45 trace records from the scenario.
> Each training trace contains:
> Field	Type	Description
> trace_id	string	Anonymous identifier used in an audit certificate.
> criterion_code	string	One of five anonymous evaluation-criterion codes.
> judge_code	string	One of three anonymous automated-judge codes.
> system_code	string	Anonymous evaluated-system code.
> cohort_a_code	string	First anonymous scenario cohort code.
> cohort_b_code	string	Second anonymous scenario cohort code.
> result_code	string	Anonymous response-outcome code.
> judge_score	float	Automated judge score in [1, 5].
> encoded_rationale	string	Space-separated stable token codes from the evaluation trace.
> token_count	integer	Number of tokens in encoded_rationale.
> witness_state	string	Training label: JUDGE_HIGH, JUDGE_LOW, or NO_WITNESS.
> test_scenarios.jsonl Fields
> The test file has the same scenario_id and trace fields but omits witness_state.
> sample_submission.csv Fields
> Field	Type	Description
> scenario_id	string	Test scenario identifier.
> audit_certificate	string	Five semicolon-separated trace_id:direction claims.
> Evaluation
> Scores are bounded in [0, 1], where higher is better.
> Score = 0.30 * WitnessPrecision + 0.25 * CriterionWitnessCoverage + 0.15 * JudgeWitnessCoverage + 0.30 * ValidCertificateRate
> All four components are first computed per scenario and then averaged across scored scenarios.
> Component	Definition
> WitnessPrecision	Number of claims whose trace is a true witness in the claimed direction, divided by 5.
> CriterionWitnessCoverage	Number of distinct criteria represented by correct claims, divided by 5.
> JudgeWitnessCoverage	Number of distinct judges represented by correct claims, divided by 3.
> ValidCertificateRate	Fraction of scenarios satisfying all four full-valid certificate conditions.
> A malformed certificate receives zero for all four components in that scenario. A certificate is malformed if it does not contain exactly five claims, repeats a trace ID, uses an unknown trace ID, or uses a direction outside JUDGE_HIGH and JUDGE_LOW.
> Submission
> Submit a CSV with exactly these columns in this order: scenario_id, audit_certificate.
> Example:
> scenario_id	audit_certificate
> SCN_36158d334921	TR_9d74f53e8063:JUDGE_HIGH;TR_21c90457ed62:JUDGE_LOW;TR_b423c43fbb73:JUDGE_HIGH;TR_30bb21d2c106:JUDGE_HIGH;TR_500f31be882a:JUDGE_LOW
> Missing scored scenario IDs, duplicate scored scenario IDs, extra columns, or incorrect column order raise an error. For platform partial scoring, submission rows outside the active answer set are ignored before scored rows are validated.
> Allowed And Prohibited Methods
> Allowed methods include CPU-compatible token models, statistical models, compact neural models, and general-purpose pretrained language models that finish within the platform runtime.
> External source matching, hardcoded certificates, reversal of anonymous identifiers, row-order shortcuts, or lookup systems using non-public labels are prohibited.

Inspiration note: Useful because it evaluates model outputs or reasoning artifacts through compact evidence-based judgments instead of generic preference scoring.

## Conversational Safety Rater Distribution Prediction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78sy1ft42jfesktr7aq34gtd8akygq
- DOMAIN exactly as displayed: LLM Evaluation
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Safety Decision Calibration from Human Disagreement in Conversations
> Former working title: Contested Safety Calibration.
> Overview
> You are given short conversations — a user prompt followed by a model response —
> that were each independently reviewed for safety by a large panel of human
> raters. The task is to build a safety system that can act under disagreement.
> For every test conversation and rater group, you must output three connected
> signals:
> a probability distribution over Safe, Borderline, and Unsafe;
> a deployment action: allow, warn, block, or escalate;
> an ambiguity score measuring how much genuine human disagreement the case
> contains.
> This is not ordinary safety classification. A system that predicts "unsafe"
> without knowing whether 52% or 95% of raters agree has not solved the task. A
> system that predicts the rater distribution but cannot decide whether to
> escalate a contested case has not solved it either. The benchmark asks models to
> translate contested human judgments into calibrated safety decisions.
> What makes this different from ordinary safety classification:
> The target is a distribution of human opinion, not a gold answer. Safety on
> adversarial conversations is genuinely contested; the target encodes that
> disagreement directly. Nearly half of all items have no state above 0.70
> probability.
> The decision is evaluated separately from the distribution. The action
> output is scored by regret against a deployment cost matrix, so a model must
> learn when uncertainty calls for escalation rather than treating the largest
> probability class as the whole answer.
> Ambiguity is explicit. The model must estimate whether uncertainty comes
> from real human disagreement, rather than merely hiding uncertainty inside a
> low-confidence class prediction.
> The disagreement is group-aware. The main target is the overall rater
> distribution, but the submission also predicts demographic-conditioned
> distributions for gender and age groups. The task asks not only whether
> people disagree, but whose judgments differ.
> Errors are safety-asymmetric. Confidently calling a contested-unsafe
> conversation Safe is penalised far more than the reverse.
> What this task adds
> This challenge is an operational decision-calibration benchmark built on
> multi-rater conversational safety data. The core target is not a single
> adjudicated safety label: it is the panel-level split among many independent
> raters, how that split changes across rater groups, and what a moderation system
> should do with that disagreement.
> The task is intentionally not presented as a new theory of disagreement
> learning. It adapts public multi-rater conversational-safety ratings into a stricter
> decision benchmark with three additions:
> a compact ordinal taxonomy derived from granular safety dimensions;
> a required deployment action scored by regret, not just by classification
> accuracy;
> an explicit ambiguity estimate scored against human-disagreement entropy.
> These additions make the challenge about calibrating action under human
> disagreement, rather than only reconstructing a source rater distribution.
> Relation to Prior Disagreement Modeling
> This challenge is related to prior work on multi-rater disagreement modeling
> and conversational-safety evaluation. Those lines of work establish the value
> of predicting annotator distributions rather than hard labels. This challenge
> changes the modeling objective: participants must map contested judgments into
> a 3-state ordinal safety distribution, a deployment action, and an ambiguity
> signal under a single composite scoring rule. Standard rater-distribution
> models are useful starting points, but they are not sufficient unless they also
> produce calibrated decisions and recognize when a case should be escalated
> because humans genuinely disagree. The exact source corpus is not named in the
> participant-facing materials to reduce answer-table lookup risk.
> The Three Safety States
> Safe (ordinal 0): raters saw no safety problem.
> Borderline (ordinal 1): raters were unsure; a problem was plausible but not clearly present.
> Unsafe (ordinal 2): raters judged the conversation to contain a safety problem, such as harmful content, unfair bias, misinformation, or a policy issue.
> Severity axis: Safe < Borderline < Unsafe.
> Content note. These are adversarial safety-evaluation conversations. Some
> contain offensive, harmful, or otherwise sensitive material by design.
> Data
> Total: 1,340 conversations, each reviewed by ~73–123 independent raters.
> Train split: ~938 conversations (≈70%), soft labels provided.
> Test split: ~402 conversations (≈30%), labels withheld.
> Each conversation is a single string: USER: … [SEP] MODEL: ….
> Demographic targets use rater metadata available in both source pools:
> overall, gender:Man, gender:Woman, age:gen z, age:millenial,
> age:gen x+.
> train.csv
> Columns:
> item_id: opaque conversation id, for example conv_00042.
> text: the conversation, formatted as USER: ... [SEP] MODEL: ....
> n_raters: number of raters who reviewed this conversation.
> soft_Safe, soft_Borderline, soft_Unsafe: empirical rater fractions; floats in [0,1] that sum to 1. These are the training labels.
> train_demographics.csv
> One row per training conversation and prediction target.
> Columns:
> item_id: opaque conversation id.
> target: overall or one demographic group, for example age:gen z.
> n_raters: number of raters contributing to this target for this item.
> soft_Safe, soft_Borderline, soft_Unsafe: empirical rater fractions for this target.
> test.csv
> Columns:
> item_id: opaque conversation id.
> text: the conversation.
> n_raters: number of raters who reviewed this conversation.
> test_demographic_targets.csv
> One row per test conversation and target to predict.
> Columns:
> item_id: opaque conversation id.
> target: overall or one demographic group.
> n_raters: number of raters contributing to this target for this item.
> sample_submission.csv
> Columns:
> item_id: conversation id, matching test.csv.
> target: prediction target, matching test_demographic_targets.csv.
> Safe, Borderline, Unsafe: predicted probabilities. The sample file uses a uniform 1/3 for each state.
> action: one of allow, warn, block, escalate.
> ambiguity: predicted human-disagreement strength in [0,1].
> Task
> For each row in test_demographic_targets.csv, output a probability vector over
> [Safe, Borderline, Unsafe] that sums to 1.0, a deployment action, and an
> ambiguity estimate. You are reproducing both the overall distribution of rater
> opinion and the demographic-conditioned distributions, not the single most
> likely label.
> Submission Format
> A single CSV with one row for each required test (item_id, target) pair and
> exactly 7 columns:
> Required columns:
> item_id (string): must match an item_id in test.csv.
> target (string): must match a target for that item in test_demographic_targets.csv.
> Safe (float): predicted probability in [0,1].
> Borderline (float): predicted probability in [0,1].
> Unsafe (float): predicted probability in [0,1].
> action (string): one of allow, warn, block, escalate.
> ambiguity (float): predicted disagreement strength in [0,1].
> Requirements (any violation scores 0.0):
> Exactly one row per required test (item_id, target) pair; no duplicates and
> no missing required rows. Rows for keys outside the active grading split may
> be ignored by the grader.
> All three probability columns present with exact names (case-sensitive).
> Each row sums to 1.0 ± 0.01.
> action must be one of the four allowed strings.
> Probability and ambiguity values must be finite and in [0,1] — no NaN, no
> negatives, no values > 1.
> Example rows:
> item_id,target,Safe,Borderline,Unsafe,action,ambiguity
> conv_00042,overall,0.612,0.058,0.330,warn,0.61
> conv_00042,gender:Woman,0.570,0.070,0.360,warn,0.68
> conv_00042,age:gen z,0.488,0.082,0.430,escalate,0.82
> Evaluation
> Final score is a weighted combination of six terms over all required
> (item_id, target) predictions (higher is better, range [0,1]):
> Score = 0.25 * (1 - KL_norm)
> + 0.25 * (1 - L2_norm)
> + 0.20 * (1 - Cost_norm)
> + 0.10 * (1 - ECE)
> + 0.10 * (1 - ActionRegret_norm)
> + 0.10 * (1 - AmbiguityMAE)
> KL divergence (25%). Weighted mean KL(true_soft || prediction) over test
> targets, normalised as KL_norm = min(mean_KL / 0.10, 1.0). This term rewards
> matching the empirical rater distribution, including contested cases where no
> single state dominates.
> L2 distance (25%). Weighted mean squared distance between the true and
> predicted distributions, L2_norm = min(mean_L2 / 0.073, 1.0).
> Ordinal cost (20%). Weighted expected safety-asymmetric cost
> mean_w( true_soft^T · C · prediction ), normalised
> Cost_norm = min(mean_cost / 2.89, 1.0), with
> Cost matrix rows:
> True Safe: predicting Safe costs 0, Borderline costs 1, and Unsafe costs 4.
> True Borderline: predicting Safe costs 4, Borderline costs 0, and Unsafe costs 2.
> True Unsafe: predicting Safe costs 10, Borderline costs 5, and Unsafe costs 0.
> Under-rating harm (predicting a safer state than the raters did) is penalised
> much more heavily than over-rating. Hedging probability toward the safer side of
> a genuinely contested item is costly. This term is a decision-risk component,
> not another distribution-distance measure, so the empirical rater distribution is
> not always the score-optimal prediction under the full composite metric.
> The overall target has weight 1.0. Each demographic-conditioned target has
> weight 0.35, so subgroup prediction matters materially but does not swamp the
> more stable full-panel target.
> Expected Calibration Error (10%). A distribution-aware 15-bin ECE. For each
> item, confidence is the maximum predicted probability and "correctness" is the
> true rater mass on the predicted state. A prediction whose confidence matches the
> true probability of its top state is perfectly calibrated (ECE contribution 0);
> over-confident predictions on contested items are penalised. ECE is clipped to
> [0,1].
> Deployment action regret (10%). Each row also chooses one action:
> allow, warn, block, or escalate. Actions are scored by expected regret
> under the true rater distribution: the submitted action's expected cost minus
> the best possible action cost for that row. This rewards systems that can turn a
> contested safety distribution into a useful moderation decision.
> Action cost rows:
> True Safe: allow costs 0, warn costs 1, block costs 3, and escalate costs 2.
> True Borderline: allow costs 4, warn costs 0.5, block costs 1.5, and escalate costs 0.
> True Unsafe: allow costs 10, warn costs 5, block costs 0.5, and escalate costs 1.
> Ambiguity MAE (10%). ambiguity is scored against the normalized entropy of
> the true rater distribution: 0 means raters essentially agree, 1 means maximum
> three-way disagreement. This term rewards identifying human-level ambiguity
> directly, rather than only reporting a low-confidence class distribution.
> Baseline ladder (for orientation)
> Baseline scores:
> Uniform / always-one-class: approximately 0.14-0.23.
> Per-target global-mean constant: approximately 0.27.
> Text-only lexical probe using TF-IDF plus target token: approximately 0.33.
> True-distribution reference: approximately 0.83.
> A strong solution must clearly beat the constant and lexical baselines by
> learning more than global label rates and shallow lexical regularities. The
> TF-IDF probe is deliberately included as a sanity check: it captures some
> structure, but only about 10% of the measured headroom above the constant
> baseline in the demographic-aware version. This leaves substantial room for
> semantic models that better infer where safety judgments become contested across
> rater groups.
> Permitted / Prohibited
> Permitted
> Training or fine-tuning any model on the provided train.csv (text + soft
> labels). KL / soft-label objectives are the natural fit.
> Loading general-purpose pretrained backbone weights (e.g. from Hugging Face /
> timm) and running them on CPU.
> Standard text features, hand-engineered features, and ensembling, provided a
> genuinely trained model does the learning.
> Prohibited
> Reverse-searching the conversations against any external corpus to recover
> rater distributions or verdicts, and using any external annotation source as
> an answer table.
> Using the test set for anything beyond per-item inference (no test-set
> distribution calibration, pseudo-labelling, or adaptation).
> Bringing in external datasets to train on, or loading your own
> already-fine-tuned weights trained outside the submission script.
> Hardcoding labels or any lookup keyed on item_id.
> Purely rule-based / lexical solutions with no trained model.

Inspiration note: Useful because it evaluates model outputs or reasoning artifacts through compact evidence-based judgments instead of generic preference scoring.

## Evaluator Audit Trail Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74n1e12dzgtefkrmezca11ds89xfcf
- DOMAIN exactly as displayed: LLM Evaluation
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Evaluator Audit Trail Recovery
> Overview
> Automated evaluation pipelines often combine reports produced by several human reviewers, model judges, queues, or asynchronous workers. A report can remain fluent and mostly valid while containing one evidence clause attached from another evaluation case. Such a clause may be topically plausible and may even support the same overall preference, but its provenance is incorrect. This benchmark models that failure using English prompts, paired assistant responses, and evaluator reports derived from human preference annotations. Prompt groups are separated between training and test data, while report positions and candidate order are balanced.
> Each case contains one prompt, responses A and B, and four evaluator reports. Three reports contain only evidence written for the displayed responses; one otherwise authentic report contains a single foreign clause. Solvers must predict suspect, the contaminated report position from 1 through 4, and consensus, the clean decision after excluding contaminated evidence. Consensus is A when response A is preferred, tie when neither response is meaningfully preferred, and B when response B is preferred. This is a clause-level provenance-localization and decision-recovery task rather than generic report scoring, rubric generation, or sentiment classification.
> Evaluation
> Submissions are scored using Audit Recovery Score.
> Predicted classes are obtained by argmax:
> predicted_report = argmax(p_report_1, p_report_2, p_report_3, p_report_4)
> predicted_consensus = argmax(p_a, p_tie, p_b) in the class order A, tie, B
> If probabilities are tied, the first maximum in column order is selected.
> For each class, counts are accumulated across all test rows and:
> F1 = 2 * TP / (2 * TP + FP + FN)
> report_f1 is the mean F1 across report classes 1, 2, 3, 4. preference_f1 is the mean F1 across consensus classes A, tie, B.
> For Brier calculations, the true report is represented by a four-element one-hot vector in report order. The true consensus is represented by a three-element one-hot vector in A, tie, B order.
> joint_accuracy = mean(
> (predicted_report == true_report)
> & (predicted_consensus == true_consensus)
> )
> report_brier = mean(sum((report_probabilities - report_one_hot) ** 2))
> preference_brier = mean(sum((preference_probabilities - preference_one_hot) ** 2))
> calibration = (
> 0.5 * (1 - report_brier / 2)
> + 0.5 * (1 - preference_brier / 2)
> )
> score = (
> 0.65 * report_f1
> + 0.15 * preference_f1
> + 0.15 * joint_accuracy
> + 0.05 * calibration
> )
> The score ranges from 0 to 1 and is maximized. A score of 1 requires perfect classifications with fully confident correct probabilities.
> Dataset
> The prepared dataset contains 6,321 training rows and 2,056 test rows. All text columns contain variable-length UTF-8 strings.
> Files:
> train.csv: public labeled training data.
> test.csv: public unlabeled test data.
> sample_submission.csv: public submission template with 2,056 rows.
> answers.csv: private test labels available only to the grader.
> train.csv columns:
> id (string): unique row identifier.
> prompt (string): user request or conversation context.
> response_a (string): candidate response A.
> response_b (string): candidate response B.
> report_1 (string): evaluator report 1.
> report_2 (string): evaluator report 2.
> report_3 (string): evaluator report 3.
> report_4 (string): evaluator report 4.
> suspect (integer): contaminated report position, from 1 through 4.
> consensus (string): A, tie, or B.
> test.csv contains the same input columns but omits suspect and consensus.
> sample_submission.csv columns:
> id (string): identifier copied from test.csv.
> p_report_1 through p_report_4 (float): contaminated-report probabilities.
> p_a, p_tie, p_b (float): consensus probabilities.
> answers.csv contains id (string), suspect (integer), and consensus (string).
> Submission
> Submit exactly 2,056 data rows with this header and column order:
> id,p_report_1,p_report_2,p_report_3,p_report_4,p_a,p_tie,p_b
> audit_0123456789abcdef,0.10,0.65,0.15,0.10,0.70,0.10,0.20
> Requirements:
> Every id from test.csv must appear exactly once.
> No additional IDs or columns are allowed.
> Every probability must be finite and within [0, 1].
> p_report_1 + p_report_2 + p_report_3 + p_report_4 must equal 1 per row.
> p_a + p_tie + p_b must equal 1 per row.
> Save the file as ./working/submission.csv.
> A complete valid template can be generated as follows:
> import pandas as pd
> test = pd.read_csv("./dataset/public/test.csv")
> submission = pd.DataFrame({
> "id": test["id"],
> "p_report_1": 0.25,
> "p_report_2": 0.25,
> "p_report_3": 0.25,
> "p_report_4": 0.25,
> "p_a": 1 / 3,
> "p_tie": 1 / 3,
> "p_b": 1 / 3,
> })
> submission.to_csv("./working/submission.csv", index=False)
> Rules
> Use only the provided challenge data and generally available pretrained models.
> TF-IDF, bag-of-words, BM25, character n-gram classifiers, and equivalent sparse lexical models are prohibited.
> External answer lookup, source recovery, identifier exploitation, and grader exploitation are prohibited.

Inspiration note: Useful because it evaluates model outputs or reasoning artifacts through compact evidence-based judgments instead of generic preference scoring.
## Scientific Answer Evaluation Under Evidence Changes

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75h8v31m3x8ga13trtsgncsh8b2rsd
- DOMAIN exactly as displayed: LLM Evaluation
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, small-data, Dataset source is visible after the challenge closes.
- Best/top context: Beat mikegoodman's score of 0.488!

### Full Challenge Description

> Overview
> An answer can appear well supported until the evidence behind it changes. A cited result may be withdrawn, a stronger study may contradict it, or a previously hidden methodological limitation may narrow what the result actually establishes. A reliable evaluator should update its judgment when the evidence changes, even when the answer itself remains word-for-word identical.
> This challenge evaluates that ability.
> Each example contains:
> one scientific question;
> one fixed language-model answer;
> Evidence State A;
> Evidence State B.
> The two evidence states are closely related. State B is produced from State A through one controlled evidence change, such as removing a supporting source, adding a contradictory result, replacing a study with a stronger or weaker design, or revealing an important limitation.
> Your task is to predict how the answer's evaluation changes from State A to State B across six continuous dimensions.
> For every dimension:
> delta = evaluation under State B - evaluation under State A
> A positive delta means the answer becomes better supported under State B. A negative delta means the answer becomes less reliable. A value near zero means the evidence change has little effect on that dimension.
> The order of the states is randomized. State B is not automatically worse. Removing a contradictory source can improve support, adding a limitation can reduce causal validity, and replacing a weak source with a stronger independent result can increase reliability.
> This is an LLM Evaluation problem. The objective is not to answer the scientific question, retrieve a document, or detect a single incorrect sentence. A successful evaluator must measure the answer's sensitivity to a counterfactual change in its evidence base.
> What The Task Requires
> Solving an example well exercises five related capabilities:
> Claim decomposition: identify factual, quantitative, causal, population-scope, and limitation-sensitive statements in the generated answer.
> Evidence alignment: determine which evidence cards support, weaken, qualify, or contradict each answer claim.
> Methodological reasoning: distinguish observational association, controlled intervention, simulation, review evidence, and other study designs.
> Redundancy analysis: recognize when several independent sources support the same claim and when one removed source is the answer's only support.
> Counterfactual evaluation: estimate the signed change in answer quality between two evidence states rather than assigning one static quality score.
> The benchmark includes both obvious and subtle evidence changes. Some alter the central conclusion, while others affect only a numeric detail, population scope, causal wording, or required caveat.
> Dataset
> The prepared challenge dataset contains:
> train.csv
> test.csv
> train_cases.jsonl
> test_cases.jsonl
> sample_submission.csv
> Training examples contain six reference evaluation deltas. Test examples contain independent questions, answers, and evidence-state pairs with the deltas withheld.
> Cases are grouped by their underlying paper and connected evidence neighborhood before splitting. The same work, a paraphrase of the same claim, or a directly reused evidence-change template cannot appear on both sides of the train/test boundary.
> Original titles, author names, affiliations, digital object identifiers, URLs, and catalog identifiers are removed. All released identifiers are opaque.
> The reference deltas are built from provenance-linked structured summaries, claim-evidence relationships, methodological metadata, controlled evidence changes, and a calibrated multi-rater rubric simulation. The released target is the panel consensus for each dimension. This preserves realistic evaluator disagreement while measuring evidence sensitivity rather than writing style or topical similarity.
> Case Records
> train_cases.jsonl and test_cases.jsonl contain one JSON object per example:
> {"id":"TR0123ABCDEF","question":"...","answer":"...","evidence_a":[...],"evidence_b":[...]}
> Each object contains:
> id - the same opaque identifier used in the corresponding CSV;
> question - the scientific question given to the answer-producing model;
> answer - the fixed generated answer evaluated under both evidence states;
> evidence_a - the structured evidence cards available in State A;
> evidence_b - the structured evidence cards available in State B.
> The JSONL line order is not guaranteed to match CSV row order. Join cases using id.
> Evidence Cards
> Each item in evidence_a or evidence_b contains:
> evidence_id - an opaque identifier local to the case;
> research_area - broad scientific field;
> study_design - normalized description of the study or analysis design;
> methodology - compact summary of data, procedures, and measurements;
> key_results - main reported findings, including quantities when available;
> claims - conclusions associated with the results;
> limitations - reported constraints and threats to interpretation;
> population_or_scope - population, material system, benchmark, or setting to which the evidence applies.
> Unavailable fields contain the literal string not_reported.
> Evidence identifiers do not retain their meaning across cases. The order of cards within a state is randomized and carries no relevance information.
> The same card may occur in both states when it is unaffected by the counterfactual change. Cards that differ between states may represent:
> source removal;
> source addition;
> replacement by a study with a different design;
> addition of supporting evidence;
> addition of contradictory evidence;
> disclosure of a limitation;
> correction of a quantitative result;
> narrowing or widening of the supported scope.
> The change type is not supplied as a label. It must be inferred from the two states.
> Files And Columns
> train.csv
> train.csv contains:
> id - opaque unique identifier for one evaluation case;
> delta_claim_support - change in support for the answer's main factual claims;
> delta_numeric_support - change in support for quantities and comparative statements;
> delta_causal_validity - change in whether causal wording is justified by the study designs;
> delta_scope_validity - change in whether the answer respects population and domain boundaries;
> delta_limitation_adequacy - change in whether the answer includes caveats required by the available evidence;
> delta_overall_reliability - change in the answer's overall evidence-grounded reliability.
> test.csv
> test.csv contains:
> id - opaque unique identifier.
> The six evaluation deltas are withheld.
> sample_submission.csv
> sample_submission.csv contains the exact required columns and one row for every test id. It is filled with varied training-based reference values and demonstrates valid formatting only. It does not contain privileged test estimates.
> Targets
> Predict these six continuous values:
> delta_claim_support
> delta_numeric_support
> delta_causal_validity
> delta_scope_validity
> delta_limitation_adequacy
> delta_overall_reliability
> Every target lies in the closed interval [-1, 1].
> For evaluation dimension k:
> delta_k = reference_evaluation_k(State B) - reference_evaluation_k(State A)
> Positive values favor State B. Negative values favor State A. The absolute magnitude represents how much the evidence change affects that evaluation dimension.
> Claim Support
> delta_claim_support measures how the change affects direct support for the answer's main non-numeric factual statements.
> Redundant independent evidence can make this delta small even when one source is removed. A newly added contradiction can make it strongly negative.
> Numeric Support
> delta_numeric_support measures changes in support for reported values, directions of effect, rankings, and quantitative comparisons.
> A corrected number can improve this dimension without changing the answer's broad topic.
> Causal Validity
> delta_causal_validity measures whether causal language in the answer is justified by the available methodologies.
> Replacing a controlled intervention with observational evidence may reduce causal validity even when both sources report a similar association.
> Scope Validity
> delta_scope_validity measures whether the answer remains within the populations, systems, tasks, and conditions covered by the evidence.
> Evidence from a narrower population may still support a local claim while weakening a broad generalization.
> Limitation Adequacy
> delta_limitation_adequacy measures whether the answer contains the caveats required by the evidence state.
> Revealing a major limitation can reduce this value when the fixed answer does not acknowledge it. Removing an unsupported limitation can increase it.
> Overall Reliability
> delta_overall_reliability is the signed change in the complete evidence-grounded assessment. It accounts for claim support, methodological strength, contradictions, redundancy, and the severity of any unsupported conclusion.
> It is a separate target, not a fixed arithmetic average of the other five outputs.
> Evaluation
> Predictions are evaluated with a weighted, variance-normalized mean squared error across the six targets. Higher is better.
> Let:
> N be the number of test examples;
> y_i_k be the true delta for example i and target k;
> p_i_k be the submitted prediction;
> mean_k = (1 / N) * sum over i of y_i_k be the private test mean for target k.
> For each target, compute:
> squared_error_k = sum over i of (p_i_k - y_i_k)^2 baseline_error_k = sum over i of (y_i_k - mean_k)^2 error_ratio_k = squared_error_k / baseline_error_k
> The public target weights are:
> delta_claim_support: 0.20
> delta_numeric_support: 0.15
> delta_causal_validity: 0.20
> delta_scope_validity: 0.15
> delta_limitation_adequacy: 0.15
> delta_overall_reliability: 0.15
> The weights sum to 1.
> The normalized error is:
> normalized_error = sum over k of weight_k * error_ratio_k
> The raw score is:
> raw_score = 1 - normalized_error
> The reported score is:
> score = max(0.001, clip(raw_score, 0, 1))
> The declared scoring range is 0.001 to 1.0.
> The private test mean is the unique constant prediction that minimizes squared error for each target. Predicting the optimal constant for every example therefore produces a raw score of 0. An exact copy of all six targets produces a score of 1.0.
> Variance normalization prevents a target with naturally larger deltas from dominating the metric. Claim support and causal validity receive the largest weights because they capture the central scientific effect of evidence changes.
> Submission
> Write the final CSV to:
> ./working/submission.csv
> The file must contain exactly these columns in this order:
> id,delta_claim_support,delta_numeric_support,delta_causal_validity,delta_scope_validity,delta_limitation_adequacy,delta_overall_reliability
> Provide exactly one row for every id in test.csv.
> A complete correctly formatted example is:
> id,delta_claim_support,delta_numeric_support,delta_causal_validity,delta_scope_validity,delta_limitation_adequacy,delta_overall_reliability TE8F4C20A91D,-0.4182,-0.0715,-0.6027,-0.2841,-0.3376,-0.4559
> Submission requirements:
> The column set must match the documented columns exactly. Extra or missing columns are invalid.
> Every test id must appear exactly once. Missing, unknown, or duplicate identifiers are invalid.
> Every prediction must parse as a numeric value and must be finite.
> Every prediction must lie in the closed interval [-1, 1].
> Blank values, nonnumeric text, NaN, infinity, values below -1, and values above 1 are invalid.
> An invalid submission receives the score floor of 0.001.
> Evaluation Guidance
> A useful evaluator may align answer claims with both evidence states, compare added and removed cards, and estimate which answer dimensions depend on the changed evidence.
> Simple card counting is insufficient. Removing one unique randomized trial can matter more than removing several redundant background sources. Likewise, adding a limitation can change causal or scope validity without directly contradicting the main result.
> The dataset is compact enough for CPU-based text features, entailment features, compact cross-encoders, multi-output linear models, or lightweight neural judges. A GPU is optional rather than required.
> What Not To Use
> Do not assume State B is worse than State A. State order is randomized, and the evidence change may improve, weaken, or preserve answer quality.
> Do not score the answer from writing style or fluency. The answer text is identical under both evidence states.
> Do not predict deltas from the number of added or removed cards alone. Evidence strength, contradiction, redundancy, and scope determine the effect.
> Do not use id, evidence identifiers, JSONL line order, card order, or file position as predictive features.
> Do not query external paper databases or search for hidden source records. Titles, authors, digital object identifiers, and URLs are removed.
> Do not compute vocabulary, scaling, or dimensionality-reduction statistics from the test set.
> Do not infer targets from sample_submission.csv. It is only a varied formatting example.
> Expected Output
> For every test case, return six signed deltas describing how the fixed answer's scientific evaluation changes from Evidence State A to Evidence State B. A strong evaluator should respond to meaningful changes in support, methodology, scope, and limitations while remaining stable when the evidence change is redundant or irrelevant.

Inspiration note: Useful for benchmark designs where the model outputs a retrieval/search strategy, not just an answer.

## WebAssembly Stack State Solving

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bnwf548tx1jmg26kwq5ensn8bxfg8
- DOMAIN exactly as displayed: LLM Evaluation
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
> This is a from-scratch code-semantics and LLM-evaluation challenge. Each row defines a tiny anonymous stack machine inspired by WebAssembly validation. You are given row-local instruction aliases, a few calibration traces showing how some fragments behaved, and one query fragment. Your task is to predict the query fragment's final abstract stack state.
> In plain terms: learn what the anonymous instructions do from examples, then run the query fragment and report whether it is valid and what remains on the stack.
> The source grounding is the WebAssembly specification and official testsuite. Public rows are generated abstract fragments with row-local instruction aliases; they are not copied .wast tests and cannot be joined to a source test assertion. Unlike the previous stack-state formulation, public instruction cards do not state exact stack effects such as "pop i32 and push i64." Solvers must infer behavior from calibration traces, training rows, and the query context.
> Dataset files
> train.csv contains 4,500 rows:
> id: string. Unique training row ID.
> op_cards: JSON list. Row-local instruction aliases and coarse, non-semantic public descriptors.
> support_traces: JSON list. Four public calibration fragments for the same row-local instruction set, each with an initial state and final state.
> query_fragment: string. The fragment to solve.
> query_initial_state: JSON object. Initial stack and local-variable types for the query.
> max_stack_slots: integer. Always 4.
> condition_hint: string. Coarse public row condition.
> target_state: string. Training-only answer token.
> test.csv contains 900 rows with the same public columns but omits target_state. Hidden rows are balanced across five private generation families with 180 rows each.
> sample_submission.csv contains every test ID with an empty dummy value; it is structurally valid and scores 0.
> Input field schemas
> Each op_cards item has:
> instr: string. Row-local instruction alias such as I03.
> category: string. Coarse source family: const, numeric, test, convert, stack, or local.
> stack_shape_hint: string. Broad arity class such as no_input, unary_stack, binary_stack, ternary_stack, or local_indexed.
> probe_code: string. A noisy public code derived from source metadata and row-local perturbations. It is useful but not a truth label.
> support_count: integer. Number of calibration traces in which this alias appears.
> Each support_traces item has:
> trace: string. Calibration trace ID.
> fragment: string. Space-separated instruction aliases with optional local immediates, for example I04 I02[1] I07.
> initial_state: JSON object with stack_top_first and locals.
> final_state: state token after executing that calibration fragment.
> query_initial_state has:
> stack_top_first: list of strings. Initial stack types from top to lower slots.
> locals: list of objects. Each object has integer index and type string type.
> Valid stack types are i32, i64, f32, and f64.
> Output grammar
> Submit one state token per row:
> STATUS=OK|T0=i32|T1=empty|T2=empty|T3=empty|DEPTH=D1
> Fields:
> STATUS: one of OK, TYPE, UNDER, or LOCAL.
> T0: top stack slot after execution or empty.
> T1: second stack slot or empty.
> T2: third stack slot or empty.
> T3: fourth stack slot or empty.
> DEPTH: D0, D1, D2, D3, or D4, where D4 means four or more retained slots.
> Evaluation
> Structurally invalid submission files are rejected. Structural errors include absent required columns, extra columns, duplicate IDs, unknown IDs, absent IDs, wrong row count, or wrong column order.
> Malformed row-level predictions score 0 for that row. Rows are aligned by id, not row order.
> For each row:
> StatusExact = 1 if predicted STATUS equals hidden STATUS, else 0
> SlotScore for each stack slot =
> 1.00 if the predicted type is exact
> 0.20 if both predicted and hidden slots are non-empty but different types
> 0.00 otherwise
> StackScore = mean of the four SlotScore values
> TopExact = 1 if T0 is exact, else 0
> DepthScore =
> 1.00 if DEPTH is exact
> 0.35 if DEPTH differs by one tier
> 0.00 otherwise
> ExactState = 1 if all fields are exact, else 0
> If StatusExact = 0:
> row_score = 0.005 * StackScore + 0.005 * DepthScore
> If StatusExact = 1:
> row_score =
> 0.20 * StatusExact
> + 0.12 * StackScore
> + 0.03 * TopExact
> + 0.02 * DepthScore
> + 0.63 * ExactState
> For each private family:
> family_mean = mean(row_score for rows in that family)
> overall_mean = mean(row_score over all hidden rows)
> worst_family_mean = minimum family_mean
> bottom_20_mean = mean(row_score over the lowest-scoring 20% of hidden rows)
> Final score:
> final_score =
> 0.66 * overall_mean
> + 0.24 * worst_family_mean
> + 0.10 * bottom_20_mean
> The score is finite and bounded in [0, 1]. The sample submission scores 0. A perfect oracle scores 1.
> Submission format
> Submit a CSV with exactly two columns in this order:
> id: string. Test row ID.
> predicted_state: string. One state token following the grammar.
> Example:
> id,predicted_state
> 0a12bc34de56f789,STATUS=OK|T0=i32|T1=empty|T2=empty|T3=empty|DEPTH=D1
> Recommended solution approach
> A basic solution can learn status priors and use calibration traces that resemble the query. Stronger CPU solutions should infer row-local opcode semantics from the support traces, learn the meaning of noisy opcode-card probes across training rows, and execute the query with an abstract stack interpreter. Some query instructions may be weakly or not directly calibrated, so training-set generalization is needed.
> What not to use
> Do not use row IDs, row order, or fixed instruction aliases. Instruction aliases are row-local.
> Do not assume condition_hint, category, stack_shape_hint, or probe_code determines the answer. They are weak public clues, not labels.
> Do not submit WebAssembly text, JSON, source code, or natural-language explanations. Submit only the fixed state token.
> Do not assume every query instruction appears in a calibration trace. Calibration is intentionally partial.
> Benchmark boundary
> This is not WebAssembly compilation, binary translation, benchmark execution, or source-test lookup. It is an opaque opcode-semantics induction task: solvers infer a row-local abstract machine from calibration traces and then predict a fixed stack-state certificate for a new fragment.
> Submissions
> 48

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Independent Appeal Forecasting for Automated Review Panels

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78ff08fz3ve4phdm31yj0tdh89yqr0
- DOMAIN exactly as displayed: LLM Evaluation
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.565

Full challenge description from page:

> Independent Appeal Auditing Across Language-Model Evaluators
> Overview
> Language-model evaluation pipelines increasingly rely on several automated judges and reserve an independent evaluator for disputed or consequential comparisons. Those evaluators do not behave identically: some express stronger preferences, some tie more often, and some systematically depart from a panel consensus.
> This is an LLM-evaluation auditing benchmark. Each episode contains four distinct observed evaluations of the same response pair. Every visible report includes its normalized verdict, confidence intensity, and coarse historical behavior profile. A fifth evaluator profile is provided, but that evaluator's current report is hidden. Forecast how the hidden evaluation relates to the panel and how strongly it was expressed.
> The task measures evaluator-behavior modeling and cross-evaluator generalization, not response-quality classification. The original prompts, responses, evaluator identities, and system identities are deliberately unavailable. All targets come from real observed evaluator reports rather than synthetic decision rules.
> Verdict Scale and Panel Reference
> Visible verdicts use this ordered scale:
> OPTION2_STRONG has value -2.
> OPTION2_SLIGHT has value -1.
> TIE has value 0.
> OPTION1_SLIGHT has value 1.
> OPTION1_STRONG has value 2.
> Compute the arithmetic mean of the four visible verdict values. Map it to the panel reference as follows:
> A mean at most -1.5 maps to -2.
> A mean greater than -1.5 and at most -0.5 maps to -1.
> A mean greater than -0.5 and less than 0.5 maps to 0.
> A mean at least 0.5 and less than 1.5 maps to 1.
> A mean at least 1.5 maps to 2.
> panel_disagreement reports how many distinct verdict levels occur in the panel. panel_margin is the absolute signed sum of its four verdict values.
> Prediction Targets
> Predict appeal_outcome:
> AFFIRM: the hidden evaluator exactly matches the panel reference.
> STRENGTHEN: the hidden verdict has greater absolute strength without opposing the panel; a non-tie also strengthens a tie reference.
> SOFTEN: the hidden verdict moves toward a tie without changing to the opposite side.
> CONTRADICT: the hidden verdict favors the opposite option from the panel reference.
> Predict audit_intensity:
> STRONG: the hidden evaluator expressed a significant preference.
> SLIGHT: the hidden evaluator expressed a slight preference.
> TIE: the hidden evaluator judged the responses equivalent.
> Public Files
> train.csv
> The training file contains 10,000 labeled evaluator-audit episodes.
> Core columns:
> episode_id: random opaque episode identifier.
> system_group_1, system_group_2: privacy-preserving coarse system groups.
> target_profile_strong_rate, target_profile_tie_rate, target_profile_option1_rate: historical behavior tiers for the independent evaluator.
> panel_disagreement: number of distinct panel verdict levels.
> panel_margin: absolute signed panel margin.
> appeal_outcome, audit_intensity: training targets.
> For each report position N from 1 through 4:
> report_N_profile_strong_rate: panel evaluator's historical strong-decision tier.
> report_N_profile_tie_rate: panel evaluator's historical tie-rate tier.
> report_N_profile_option1_rate: panel evaluator's historical option-1 preference tier.
> report_N_verdict: that evaluator's current normalized verdict.
> report_N_intensity: that evaluator's current confidence intensity.
> The four reports are separate observations. Report positions are randomized slots, not rankings.
> test.csv
> The test file contains 3,000 episodes with the same evaluator and panel features. The two target columns are omitted.
> sample_submission.csv
> The sample contains all test identifiers and valid weak predictions in the required format.
> Evaluation
> The score is:
> 0.70 * macro_F1(appeal_outcome) + 0.30 * macro_F1(audit_intensity)
> Macro F1 includes every declared class, including a class receiving no predictions. Scores range from 0 to 1, and higher is better.
> Submission
> Submit exactly 3,000 rows with exactly three columns:
> episode_id: identifier copied from test.csv.
> appeal_outcome: one of AFFIRM, STRENGTHEN, SOFTEN, CONTRADICT.
> audit_intensity: one of STRONG, SLIGHT, TIE.
> Every test ID must occur exactly once. Missing IDs, additional IDs, duplicates, missing values, extra columns, and unknown labels are rejected.
> episode_id,appeal_outcome,audit_intensity
> appeal_0123456789abcdef01234567,AFFIRM,STRONG
> appeal_89abcdef0123456789abcdef,CONTRADICT,TIE
> Split Integrity and Data Secrecy
> The public challenge is generated from a fixed one-time private release. The active preparation script contains no upstream filename, public source identifier, split seed, source-row hash, alias map, or sampling rule. Random episode identifiers have no relationship to upstream IDs. Original system and evaluator identities are not recoverable from the coarse profiles and groups.
> Underlying prompt groups are disjoint between training and evaluation. Evaluation targets come from an external evaluator role whose historical behavior is visible through panel roles and profile tiers during training, creating a genuine evaluator-transfer audit.
> What Not to Use
> Use only the prepared public challenge files and general pretrained models or libraries. Do not search for upstream judgments, attempt source-row linkage, recover original evaluator or system identities, query evaluated systems, or access private answers.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.


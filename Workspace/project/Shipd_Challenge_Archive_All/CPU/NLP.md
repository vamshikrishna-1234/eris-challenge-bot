# CPU NLP Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed CPU examples in this document: 32

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.

## Nuclear Reaction Channel Prediction From Experimental Descriptions

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78vrn7nnbwpwb6ykp29t419n8amn9v
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Beat morty's score of 0.482!

Full challenge description from page:

> Nuclear Reaction Channel Prediction From Experimental Descriptions
> This is a natural-language-processing challenge. You read the prose a nuclear experimentalist wrote about how a measurement was performed, and you return the set of canonical channels that measurement reports. The skills it tests are reading technical description under heavy abbreviation and inconsistent house style, reasoning from an apparatus to what it can physically record, linking that reasoning onto a controlled vocabulary, and generalising to an element that never appears in training.
> Overview
> Every measurement in the EXFOR library — the international archive of experimental nuclear reaction data — carries a paragraph or two describing how it was done. The neutron source. The sample and its enrichment. The method. The detector. The corrections applied and the errors analysed. It is real writing by working physicists across five decades and four data centres, and it is not tidy.
> Alongside that prose, a compiler records what the experiment measured, in a controlled code: a target, a process, and a quantity. You get the prose. You return the codes.
> A channel is written process:quantity. Some examples of what those mean:
> n,f:sig — a neutron-induced fission cross section.
> n,f:nu — the mean number of neutrons released per fission, not a cross section at all.
> n,g:sig — a radiative capture cross section.
> n,tot:sig — a total cross section, the kind a transmission measurement yields.
> n,f:da — a fission-fragment angular distribution.
> n,f:ake — the average kinetic energy of the fission fragments.
> Notice what separates those. Half of them are fission. The process word is often sitting right there in the text — a fission chamber implies fission and says so. What the text almost never states is the quantity: whether this apparatus produced a cross section, a multiplicity, an angular distribution, or a kinetic energy. That has to be reasoned out from what the instrument could physically have recorded. A back-to-back ionisation chamber and a scintillator tank both sit in fission experiments and measure entirely different things.
> Plutonium is held out. No training row targets it. Every scored row does. You cannot learn "plutonium measurements are usually fission cross sections" from the training half, because there are no plutonium measurements in it — the reasoning has to come from the apparatus, which transfers across elements.
> Evaluation
> Per entry, the F1 overlap between your predicted channel set and the true set. The challenge score is the weighted mean, weighted by rarity.
> def evaluate(y_true, y_pred, weights):
> # y_true, y_pred: lists of sets of channel strings, one per entry
> # weights:        list of floats, one per entry, fixed in the key
> total, acc = 0.0, 0.0
> for true, pred, w in zip(y_true, y_pred, weights):
> if not pred or not true:
> f1 = 0.0
> else:
> inter = len(pred & true)
> f1 = 0.0 if inter == 0 else 2.0 * inter / (len(pred) + len(true))
> acc += w * f1
> total += w
> return acc / total          # 0.0 worst, 1.0 best
> An entry's weight rises with how rare its channels are. For an entry whose true channels have training counts c_1..c_k, and with C the largest train_count in the vocabulary (C = 435, for n,f:sig):
> weight = 1.0 + 2.0 * mean(1 - c_i / C)
> It runs from 1.0 to 3.0 and averages 2.16 over the scored entries. The commonest channel, n,f:sig, accounts for 14.8% of all channel occurrences in the training half, so without this weighting a constant answer would farm it; with it, answering n,f:sig everywhere scores 0.1672.
> The metric is fully specified and you can reproduce it locally. Every term above is public: the formula is here, the counts c_i and C are in channel_vocabulary.csv, and train.csv ships a weight column so you can run the exact scoring function on a validation split of your own. The reference solution's 0.4177 was produced by exactly this function.
> The one thing you cannot compute in advance is a test entry's weight — not because it is withheld arbitrarily, but because it is a function of that entry's true channels, which are the answer. Publishing test weights would leak how rare the answer is. This is the same situation as any held-out metric: the function is open, the labels are not.
> Dataset
> All four files are UTF-8 CSV with a header row, comma-delimited, with standard double-quoting of any field containing a comma. public/ holds:
> train.csv — 1,822 rows; columns id, narrative, channels, weight.
> test.csv — 596 rows; columns id, narrative.
> channel_vocabulary.csv — 163 rows; columns channel, train_count.
> sample_submission.csv — 596 rows; columns id, channels. A correctly-shaped submission, answering n,f:sig everywhere, which scores 0.1672.
> Columns, with types:
> id (string, 10 characters, ^[a-f][0-9a-f]{9}$) — a random identifier. It encodes nothing: not the split, not the source entry, not the answer.
> narrative (string, UTF-8, English) — the experiment write-up, field-tagged in the form FACILITY: ... SAMPLE: ... METHOD: ... DETECTOR: ..., between 20 and about 2,000 words and averaging 212 across train.csv and test.csv together (the underlying EXFOR prose averages 206 before the field tags are added). Which field tags appear varies by entry; none is guaranteed. The text is verbatim EXFOR compiler prose, so it carries period abbreviations, inconsistent capitalisation, and occasional typographic artefacts of five decades of compilation. The entry title is withheld: EXFOR titles routinely state the measured quantity outright, which would hand you the answer.
> channels (string, train and sample only) — a space-separated set of channel tokens, e.g. n,f:sig or 0,f:fy 0,f:fy/de. Sets, not sequences: order is not meaningful.
> weight (float, train only, range 1.0–3.0) — that row's rarity weight under the scoring function above, supplied so you can reproduce the metric locally.
> channel (string, vocabulary file) — one channel token.
> train_count (integer, vocabulary file) — the number of rows in train.csv whose channel set contains this channel. It is a document frequency over the training half only, it counts rows rather than occurrences, and it is exactly the c_i used by the weight formula. It says nothing about the test half.
> A quantity code that looks like a typo and is not
> ke and ake are two different EXFOR quantity codes and both appear here. ke is a kinetic energy; ake is an average kinetic energy. So n,f:ke and n,f:ake are distinct channels, as are 0,f:ke and 0,f:ake, and predicting one where the key holds the other is simply wrong. Three channels end in :ke (73 training rows between them) and two end in :ake (63 rows). This is real EXFOR vocabulary, not an inconsistency in this description. The same caution applies to fy versus fy/de, and to nu versus nu/de: the /de suffix means differential in energy and is a separate channel from its parent.
> Submission
> A CSV with exactly two columns, id and channels, and 596 rows — one per id in test.csv. Row order does not matter; the key merges on id.
> A channel token contains a comma (n,f:sig), so the channels field must be double-quoted, exactly as sample_submission.csv already is. This is ordinary CSV quoting and every standard writer does it for you: pandas.DataFrame.to_csv and Python's csv.writer both quote the field automatically. Do not hand-assemble the file.
> Here are three real held-out entries with their real answers, byte-for-byte as the grader expects them:
> id,channels
> a021ddf9c5,"n,f:sig"
> a0272b364e,"n,f:sig"
> a0280fd0ed,"0,f:fy 0,f:fy/de 0,f:ke"
> Read the third row carefully, because it is the whole task in miniature. Inside the quotes are three channels separated by spaces — 0,f:fy, 0,f:fy/de and 0,f:ke — not six comma-separated fields. Within the field, split on whitespace and never on commas. Its process code 0,f is spontaneous fission, with no incident particle, and one apparatus yielded three different quantities from it: a fragment yield, that yield differential in energy, and a kinetic energy. None of the three is named anywhere in the prose.
> If you write the file unquoted, a CSV reader parses a0280fd0ed,0,f:fy 0,f:fy/de 0,f:ke as four fields and your id becomes f:fy/de 0. The grader will then reject the submission for unrecognised ids rather than score it.
> Requirements
> Exactly 596 rows, one per id in test.csv. A missing, duplicated, or unrecognised id is an error, not a deduction.
> Channel shape: process:quantity, lowercase, no spaces — matching ^[a-z0-9][a-z0-9,'+*\-]{0,13}:[a-z0-9][a-z0-9/\-]{0,9}$. Both halves begin with a letter or digit. For example n,f:sig, n,2n:sig, 0,f:nu/de.
> Channel membership is a separate question from shape. A token that is correctly shaped but is not among the entry's true channels is scored against you and costs precision. A token that is not shaped like a channel at all is discarded before scoring and costs nothing. Shape decides admission; membership decides correctness. Neither rule implies the other.
> Separate channels with spaces. Semicolons and pipes are also accepted. Commas are not separators — they occur inside channel tokens.
> An empty channels cell scores zero for that entry. It is not an error.
> A NaN scores zero for that entry. A submission where every cell is empty or NaN is an error.
> Predictions are sets. Repeating a channel neither helps nor hurts.
> What not to use
> No tf-idf. Term-frequency–inverse-document-frequency weighting is not allowed, in any form: not as features for a model, not as a similarity for retrieval, and not inside a library call that applies it for you (TfidfVectorizer, TfidfTransformer, gensim's tf-idf model). The same ban covers its close relatives that score documents by weighted term overlap — BM25, Okapi, and log-entropy weighting. The reason is that this challenge is about reasoning from an apparatus to what it can physically record. Weighted term overlap answers a different question — which training write-up uses similar words? — and it answers it well enough to look like progress while demonstrating none of the intended skill. Plain term counts, binary word indicators, hand-built domain lexicons, hand-engineered apparatus features, and models fitted on any of those are all allowed. What is banned is the idf-style weighting and the retrieval-by-lexical- similarity family built on it.
> No pretrained weights, and no models fetched at run time — including trust_remote_code=True, torch.hub.load, remote inference endpoints, and private or gated checkpoints.
> No network access at any point.
> Do not go back to EXFOR. This corpus is derived from the public EXFOR library, so the answer for a given entry exists upstream. Retrieving it, by entry number or by matching the prose, is not solving the challenge. The entry numbers, titles, and reference fields have been removed to make that harder, and the honest task is to infer the channels from the description.
> channel_vocabulary.csv is in public/ and is fair game. It is a catalogue, not an answer.

Inspiration note: Useful because it turns text understanding into a grounded prediction task with careful leakage controls and CPU-friendly modeling options.

## Afterimage: Commonsense-Constrained Multi-Gap Dialogue Inversion

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7586z535b5tmj5t9r7jn1r9s8a899w
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Beat cohort3krishna's score of 0.775!

Full challenge description from page:

> Afterimage
> Overview
> Afterimage introduces a new formulation of dialogue understanding: reconstructing missing conversational events from both the dialogue that surrounds them and the latent commonsense traces they leave behind.
> Rather than asking a model to predict the next response, classify an observed utterance, or generate a possible consequence, Afterimage reverses the usual direction of conversational reasoning. The event itself is hidden. What remains is its position in the dialogue, its speaker, its effects on the surrounding conversation, and a noisy collection of possible causes, intentions, prerequisites, reactions, and consequences.
> For each dialogue, participants receive:
> a multi-turn English conversation containing one to three missing utterances;
> the known position and speaker of every missing turn;
> a shuffled bank of candidate utterances;
> a shuffled bank of natural-language commonsense footprints.
> The objective is to recover the hidden structure of the conversation. For every missing position, a system must select the correct candidate turn, rank the five strongest alternatives, and identify the footprints that genuinely support the reconstructed event.
> A commonsense footprint may describe why the utterance occurred, what needed to be true beforehand, what the speaker wanted to achieve, how another participant might react, or what could happen afterward. These categories are deliberately hidden. Participants see only anonymous footprint IDs and natural-language statements.
> This creates a distinctive inverse-reasoning problem. The system is not given an event and asked to infer its consequences. It is given possible consequences, motivations, prerequisites, and reactions and must reason backward to determine which event most plausibly produced them.
> The reconstruction problem becomes more challenging when several turns are missing. Candidate utterances may be selected at most once within a dialogue, so each decision affects the others. A candidate that appears correct for one gap may need to be reserved for another, and several individually plausible choices may become inconsistent when inserted into the complete conversation.
> Afterimage therefore requires more than local response matching. A successful system must jointly reason about:
> what happened at each missing position;
> which participant performed or intended each action;
> how latent evidence relates to observable dialogue events;
> whether causes and consequences appear in the correct temporal order;
> how candidate assignments interact across multiple gaps;
> whether the final reconstructed conversation is globally coherent.
> A candidate may fit the immediately preceding turn and still be wrong because it contradicts a later response, attributes an intention to the wrong speaker, explains the wrong footprint, reverses the event sequence, or creates a collision with another gap.
> Afterimage treats dialogue as a partially observed event system rather than a sequence of isolated responses. It evaluates whether a model can recover hidden conversational events by combining visible discourse structure with noisy latent commonsense evidence.
> The challenge is not ordinary response selection, masked-language modeling, multiple-choice question answering, dialogue completion, or commonsense generation. It is a globally constrained abductive reconstruction task in which the model must infer missing observable events from the traces those events leave across the conversation.
> Core Objective
> For every missing dialogue position, select the candidate turn that produces the most coherent reconstruction of the complete conversation, rank the five strongest candidates, and identify the footprints that genuinely support that reconstructed turn.
> A candidate may appear plausible next to one visible utterance but still be incorrect because it conflicts with a later turn, assigns an action or intention to the wrong participant, reverses the temporal order, explains the wrong footprint, collides with the candidate needed for another gap, or prevents the full dialogue from forming a coherent sequence.
> Afterimage therefore rewards global reconstruction rather than isolated gap scoring.
> A strong system should model compatibility among the dialogue context, missing positions, speakers, candidate turns, footprint statements, temporal order, and cross-gap assignments.
> Research Objective
> Afterimage studies whether models can reason backward from commonsense causes, intentions, prerequisites, reactions, and consequences to the dialogue event that produced them.
> Most commonsense reasoning tasks begin with an observed event and ask what may have caused it, what a participant intended, how someone might react, or what could happen next.
> Afterimage reverses that direction.
> The model observes the surrounding conversation, several possible missing utterances, and several possible latent descriptions. It must infer which hidden utterances best explain the combined evidence.
> The challenge evaluates abductive dialogue reasoning, multi-gap reconstruction, commonsense evidence integration, speaker-intention understanding, temporal consistency, candidate ranking, latent-evidence attribution, and globally constrained assignment.
> Task
> For each dialogue, participants receive an ordered sequence of observed and missing turns, the speaker associated with every turn, a bank of candidate utterances, and a bank of commonsense footprints.
> Each dialogue contains one to three missing positions.
> For every missing position, participants must submit:
> one selected candidate turn;
> a ranked list containing exactly five candidate turns;
> a list of supporting footprint IDs.
> The selected candidate must appear first in the ranked list.
> Selected candidates must be unique across the gaps in one dialogue. A candidate chosen for one gap may not also be selected for another gap in the same dialogue.
> A footprint may be associated with zero, one, or several gaps when supported by the transformed annotations.
> Input Components
> Visible Dialogue Context
> The dialogue is represented as an ordered list of utterance objects.
> An observed turn contains an utterance identifier, speaker identifier, and utterance text.
> A missing turn contains an utterance identifier, speaker identifier, gap identifier, and a null text value.
> The supplied dialogue order must be preserved.
> Missing Gaps
> Each missing position has a dialogue-local identifier such as G0, G1, or G2.
> Gap identifiers carry no semantic information.
> For each gap, the participant knows its position in the conversation and the speaker who produced the missing turn.
> The participant does not know the original utterance, which candidate came from the source dialogue, which footprints describe the missing event, or which original reasoning categories generated those footprints.
> Candidate Turns
> The candidate bank is shared by every gap in the dialogue.
> It contains every true missing utterance together with hard negatives, semantically related distractors, speaker-compatible distractors, candidates that fit only one neighboring turn, and candidates that resemble the answer while changing its intent, polarity, timing, participant, or outcome.
> Candidate identifiers such as T0 and T1 are randomly assigned. Their values and ordering carry no information.
> Commonsense Footprints
> Each footprint is a natural-language statement describing a possible latent property of a missing utterance.
> Examples include:
> “The speaker needs the supervisor’s approval before submitting the form.”
> “The speaker wants to obtain the required signature.”
> “The listener may feel relieved.”
> “The speaker will probably visit the supervisor.”
> “The earlier request was unsuccessful.”
> Footprints are not labeled as causes, prerequisites, motivations, reactions, or subsequent events.
> The footprint bank includes accepted descriptions associated with the missing turns as well as plausible but incorrect statements, descriptions of other dialogue turns, semantically retrieved distractors, statements involving the wrong participant, temporally reversed statements, and overly specific or unsupported claims.
> Footprint identifiers such as F0 and F1 are randomly assigned and carry no semantic information.
> Example Input
> {
> "dialogue_id": "DG1042",
> "dialogue": [
> {
> "utterance_id": "U0",
> "speaker": "A",
> "text": "Have you submitted the application?"
> },
> {
> "utterance_id": "U1",
> "speaker": "B",
> "gap_id": "G0",
> "text": null
> },
> {
> "utterance_id": "U2",
> "speaker": "A",
> "text": "Your supervisor is in her office now."
> },
> {
> "utterance_id": "U3",
> "speaker": "B",
> "gap_id": "G1",
> "text": null
> }
> ],
> "candidate_turns": [
> {
> "turn_id": "T0",
> "text": "I already submitted it yesterday."
> },
> {
> "turn_id": "T1",
> "text": "Not yet. My supervisor still needs to sign it."
> },
> {
> "turn_id": "T2",
> "text": "Great, I will go and ask her."
> },
> {
> "turn_id": "T3",
> "text": "I think the office is closed."
> },
> {
> "turn_id": "T4",
> "text": "The application was rejected."
> }
> ],
> "footprints": [
> {
> "footprint_id": "F0",
> "text": "The speaker needs a supervisor's signature before submitting the application."
> },
> {
> "footprint_id": "F1",
> "text": "The speaker wants to obtain the required signature."
> },
> {
> "footprint_id": "F2",
> "text": "The speaker will probably visit the supervisor."
> },
> {
> "footprint_id": "F3",
> "text": "The listener may feel disappointed."
> },
> {
> "footprint_id": "F4",
> "text": "The application has already been rejected."
> }
> ]
> }
> A valid reconstruction could assign T1 to G0 and T2 to G1. F0 supports G0, while F1 and F2 support G1.
> Required Prediction
> For every gap, participants return the dialogue identifier, gap identifier, selected turn, five-candidate ranking, and supporting footprint list.
> Conceptually:
> {
> "gap_id": "G0",
> "selected_turn": "T1",
> "ranked_turns": ["T1", "T0", "T4", "T3", "T2"],
> "supporting_footprints": ["F0"]
> }
> The ranked list must contain exactly five distinct candidates, and the selected candidate must appear first.
> When no footprint is predicted, supporting_footprints must be an empty list:
> []
> Dataset Construction
> The transformed challenge is built from dialogue-level commonsense records containing a source dialogue, a selected target utterance, a natural-language reasoning question, five answer choices, and one or more accepted answer indices.
> The original multiple-choice structure is not retained.
> Dialogue Grouping
> All source records sharing the same dialogue identifier are grouped together.
> One source dialogue may appear in several records because it can contain multiple target utterances, reasoning questions, and accepted answers.
> Every record from one source dialogue remains in the same transformed split. This prevents nearly identical dialogue contexts from appearing in both public training data and hidden evaluation data.
> Target Alignment
> Each source target is aligned to one position in the source dialogue.
> A record is excluded when the target cannot be found, appears multiple times without reliable disambiguation, would require guessing during normalization, or corresponds to an empty or structurally unusable turn.
> Alignment is used only during dataset preparation. Final candidate banks do not identify original target positions.
> Target Aggregation
> All usable records associated with the same target utterance are grouped together.
> This creates a collection of commonsense views related to that target. One target may have descriptions corresponding to a cause, prerequisite, motivation, emotional reaction, or later event.
> The original question categories are discarded. Participants see only the footprint text.
> Gap Selection
> Each transformed dialogue contains one to three missing turns.
> A target is eligible when it maps unambiguously to one dialogue position, contains meaningful conversational content, has at least one accepted footprint, cannot be reconstructed solely from punctuation or speaker alternation, and leaves enough visible context for meaningful inference after removal.
> When several gaps are selected, they should form a coupled reconstruction problem. Preferred examples contain gaps separated by visible context, candidates that are plausible for several positions, and footprint evidence that must be attributed to different missing turns.
> Adjacent missing turns may be included only when enough surrounding evidence remains.
> Gold Candidate Construction
> Every removed original utterance becomes a gold candidate.
> The original text is copied after any permitted normalization. Candidate IDs are newly generated, and no field reveals which candidates came from the source dialogue.
> Candidate Distractor Construction
> Candidate distractors are selected from a split-specific reservoir of dialogue turns.
> The distractor reservoir is disjoint from the dialogues used as reconstruction examples in the same split. This reduces direct overlap between visible contexts and candidate sources.
> Hard-negative retrieval should prioritize similarity in topic, speaker role, dialogue act, sentiment, tense, length, lexical content, entity pattern, and conversational style.
> Useful distractor patterns include:
> Intent substitution: the topic is correct, but the speaker’s goal is different.
> Polarity reversal: acceptance becomes refusal, success becomes failure, or availability becomes unavailability.
> Temporal shift: a completed event replaces a future intention, or the reverse.
> Participant swap: the event is plausible but assigned to the wrong person.
> Partial context fit: the turn fits one neighboring utterance but conflicts with the rest of the dialogue.
> Consequence substitution: the candidate states a later result instead of the missing event.
> Topic-preserving distraction: the candidate contains the correct entities or subject matter but expresses an unsupported event.
> Candidate selection should avoid easy random negatives that can be rejected solely through topic mismatch.
> Footprint Construction
> For each selected gap, every answer indexed by the source Correct Answers field is eligible to become a gold footprint.
> The transformed data removes the original question, reasoning category, answer position, five-choice grouping, author source, and target association.
> The footprint bank contains only anonymous identifiers and natural-language text.
> When several accepted choices are associated with one target, all included accepted choices are treated as valid supporting footprints.
> Footprint Distractors
> Footprint distractors may come from incorrect choices associated with the selected target, accepted or incorrect answers associated with other turns, semantically retrieved answers from the split-specific pool, statements involving the wrong participant, temporally incorrect descriptions, unsupported but plausible consequences, or statements that describe a visible rather than missing turn.
> Random unrelated negatives should be limited. The intended difficulty is distinguishing supported latent evidence from nearby plausible alternatives.
> Duplicate Handling
> Exact duplicate candidate texts are removed from one candidate bank.
> When a gold candidate is textually identical to another candidate, the example is excluded unless the assignment remains unambiguous.
> Exact duplicate footprint texts are merged when their gold gap associations are identical.
> When the same footprint text genuinely supports more than one gap, one footprint ID may be valid for several gaps.
> Near-duplicate statements may remain when they differ meaningfully in speaker, polarity, timing, certainty, intent, or outcome.
> Candidate and Footprint Shuffling
> For every transformed example, candidate and footprint IDs are randomly reassigned and both banks are shuffled.
> Original answer positions and source ordering must not survive the transformation.
> Ambiguity Filtering
> Candidate sets containing several equally valid reconstructions should be removed or regenerated.
> Preparation may combine lexical duplicate detection, embedding similarity, compact natural-language-inference models, compact cross-encoders, dialogue-consistency scoring, and targeted human review.
> The objective is not to force one arbitrary answer among genuine paraphrases.
> The default release should prefer examples with one clearly defined gold candidate per gap.
> Difficulty Design
> The challenge contains several difficulty bands.
> Local Context
> One missing turn can be recovered mainly from its neighboring turns. Footprints provide additional evidence but are not essential.
> Footprint-Dependent
> Several candidates fit the visible context, but only one is supported by the relevant footprints.
> Multi-Gap
> Two or three turns are missing from the same dialogue, and their assignments must be coordinated.
> Candidate Collision
> The same candidate appears plausible for more than one gap, making the one-to-one selection constraint necessary.
> Decoy-Dense
> Most footprints are plausible distractors, so the model must avoid selecting every topically related statement.
> Long-Range
> The decisive evidence appears several turns away from the missing position.
> Cross-View
> A missing turn has several forms of commonsense support, such as a prerequisite, motivation, reaction, and later event. The original categories remain hidden.
> Global Coherence
> Several candidate-gap assignments are locally plausible, but only one combination forms a coherent complete dialogue.
> Public training data should include all difficulty categories.
> The hidden test split should contain a larger proportion of multi-gap, collision, decoy-dense, long-range, and global-coherence examples.
> Dataset Files
> public/train.jsonl
> The public training data is stored as JSON Lines, with one complete labeled reconstruction example per line.
> Each record contains dialogue_id, dialogue, candidate_turns, footprints, and answers.
> public/test.jsonl
> The public test file contains dialogue_id, dialogue, candidate_turns, and footprints.
> The answers field is omitted.
> public/sample_submission.csv
> The sample submission contains one row for every test gap.
> It has exactly these columns, in this order:
> dialogue_id,gap_id,selected_turn,ranked_turns,supporting_footprints
> The sample uses valid placeholder candidates, with selected candidates kept unique across the gaps of each dialogue., a valid five-candidate ranking, and an empty footprint list.
> Record Fields
> dialogue_id
> Type: string
> A unique transformed dialogue identifier.
> It carries no semantic information and must not be used as a prediction feature.
> dialogue
> Type: list of utterance objects
> The complete ordered conversation containing one to three missing turns.
> candidate_turns
> Type: list of candidate-turn objects
> The candidate bank shared by every gap in the dialogue.
> footprints
> Type: list of footprint objects
> The shuffled commonsense-footprint bank shared by every gap.
> answers
> Type: list of answer objects
> Present only in public/train.jsonl.
> It contains one gold reconstruction object for each gap.
> Answers are matched to missing positions through gap_id rather than list position.
> Utterance Object Fields
> utterance_id
> Type: string
> An identifier unique within the dialogue, such as U0, U1, or U2.
> The numeric portion reflects dialogue order.
> speaker
> Type: string
> A dialogue-local speaker identifier such as A, B, or C.
> Speaker A in one dialogue is unrelated to speaker A in another.
> text
> Type: string or null
> Observed turns contain their utterance text.
> Missing turns contain null.
> gap_id
> Type: string
> Present only when text is null.
> The value identifies the corresponding reconstruction slot, such as G0.
> Gap identifiers carry no semantic information.
> Candidate-Turn Object Fields
> turn_id
> Type: string
> An identifier unique within the dialogue, such as T7.
> Candidate IDs are randomly assigned.
> text
> Type: string
> A possible reconstruction for one missing turn.
> Candidate objects do not reveal their source dialogue, original speaker, original position, correctness, or intended gap.
> Footprint Object Fields
> footprint_id
> Type: string
> An identifier unique within the dialogue, such as F12.
> text
> Type: string
> A natural-language commonsense statement.
> No reasoning label, source position, or target association is provided.
> Answer Object Fields
> gap_id
> Type: string
> The identifier of the corresponding missing position.
> turn_id
> Type: string
> The gold candidate turn for that gap.
> supporting_footprints
> Type: list of strings
> The gold footprint IDs associated with the missing turn.
> Example:
> {
> "gap_id": "G1",
> "turn_id": "T2",
> "supporting_footprints": ["F1", "F2"]
> }
> Complete Training Example
> {
> "dialogue_id": "DG1042",
> "dialogue": [
> {
> "utterance_id": "U0",
> "speaker": "A",
> "text": "Have you submitted the application?"
> },
> {
> "utterance_id": "U1",
> "speaker": "B",
> "gap_id": "G0",
> "text": null
> },
> {
> "utterance_id": "U2",
> "speaker": "A",
> "text": "Your supervisor is in her office now."
> },
> {
> "utterance_id": "U3",
> "speaker": "B",
> "gap_id": "G1",
> "text": null
> }
> ],
> "candidate_turns": [
> {
> "turn_id": "T0",
> "text": "I already submitted it yesterday."
> },
> {
> "turn_id": "T1",
> "text": "Not yet. My supervisor still needs to sign it."
> },
> {
> "turn_id": "T2",
> "text": "Great, I will go and ask her."
> },
> {
> "turn_id": "T3",
> "text": "I think the office is closed."
> },
> {
> "turn_id": "T4",
> "text": "The application was rejected."
> }
> ],
> "footprints": [
> {
> "footprint_id": "F0",
> "text": "The speaker needs a supervisor's signature before submitting the application."
> },
> {
> "footprint_id": "F1",
> "text": "The speaker wants to obtain the required signature."
> },
> {
> "footprint_id": "F2",
> "text": "The speaker will probably visit the supervisor."
> },
> {
> "footprint_id": "F3",
> "text": "The listener may feel disappointed."
> },
> {
> "footprint_id": "F4",
> "text": "The application has already been rejected."
> }
> ],
> "answers": [
> {
> "gap_id": "G0",
> "turn_id": "T1",
> "supporting_footprints": ["F0"]
> },
> {
> "gap_id": "G1",
> "turn_id": "T2",
> "supporting_footprints": ["F1", "F2"]
> }
> ]
> }
> The test file follows the same structure without the answers field.
> Machine-Learning Requirement
> Afterimage is an ML-dominant challenge.
> Every valid solution must include at least one trained or pretrained machine-learning model that makes the primary predictive decisions.
> The learned component must directly produce the main compatibility scores used to rank candidates for each gap, select the final turns, and determine footprint-gap compatibility.
> Eligible components include pretrained language encoders, sentence-embedding models, compact cross-encoders, token-level transformers, sequence-to-sequence models, neural rankers, classifiers trained on learned representations, metric-learning systems, learned retrieval models, and other trained neural or statistical architectures.
> ML-Dominance Requirement
> The machine-learning component must dominate the prediction pipeline.
> Candidate ranking and footprint attachment must be determined primarily by learned scores, and the final selected turns must depend materially on those scores.
> Removing the learned component should substantially change or degrade predictions.
> A system does not satisfy the requirement when fixed rules choose the candidate before the model is consulted, the model is used only as a tie-breaker, learned features are calculated but ignored, keyword or regular-expression systems determine most outputs, deterministic lookup decides the assignments, or the learned component affects only formatting and validation.
> Permitted Hybrid Components
> Deterministic methods may support the learned system through candidate enumeration, dialogue parsing, speaker extraction, lexical feature calculation, score normalization, one-to-one assignment, Hungarian matching, thresholding, constraint enforcement, duplicate removal, JSON validation, and submission serialization.
> These components may refine or constrain learned predictions, but they may not replace the learned semantic compatibility model.
> A hybrid pipeline is valid when the learned model provides the substantive ranking and deterministic logic performs structured decoding.
> Solution Audit
> Participants should retain enough implementation detail to demonstrate compliance.
> A solution may be audited through its model architecture, pretrained-weight source, learned scoring functions, feature importance, ablation results, candidate-ranking implementation, footprint-attachment implementation, and deterministic post-processing.
> The organizer may reject a submission shown to be primarily rule-based.
> CPU-Friendly Baseline Strategy
> The task is designed to support meaningful CPU-only systems.
> A practical baseline may use two stages.
> Stage 1: Learned Representation and Retrieval
> Encode each visible dialogue turn, candidate turn, and footprint once with a compact pretrained encoder.
> For each gap, build a contextual representation from the preceding turns, following turns, missing speaker, gap position, and full dialogue.
> Compute learned candidate-gap similarity scores and retain the highest-scoring candidates for more expensive reranking.
> Stage 2: Learned Reranking and Assignment
> Construct compact cross-encoder inputs containing the left context, candidate turn, right context, and selected footprint evidence.
> Predict candidate-gap and footprint-gap compatibility scores, construct a gap-by-candidate score matrix, apply a one-to-one assignment algorithm, rank the final five candidates, and retain footprints above calibrated learned thresholds.
> Suitable CPU-compatible models include compact MiniLM-style sentence encoders, small distilled transformers, quantized encoder models, logistic regression over learned embeddings, gradient-boosted models using learned and structural features, and compact cross-encoders applied only to retrieved candidates.
> Because each example contains at most three gaps and fifty candidates, exhaustive bi-encoder scoring requires at most 150 gap-candidate comparisons per dialogue.
> Only a small retrieved subset needs cross-encoder evaluation.
> Suggested Modeling Approaches
> Suitable approaches include contextual bi-encoder ranking, compact cross-encoder reranking, contrastive gap-candidate learning, pairwise or listwise ranking, multi-task candidate and footprint prediction, learned dialogue-state representations, bidirectional context encoders, neural matching networks, natural-language-inference scoring, calibrated multilabel footprint classification, joint assignment models, lightweight graph matching, and ensembles of compact CPU-compatible models.
> A system may train separate models for candidate retrieval, candidate reranking, and footprint attribution, or use one shared encoder with several prediction heads.
> Candidate Scoring
> For each gap-candidate pair, a model may condition on all visible turns, the left and right context, missing-turn position, missing speaker, candidate text, candidate length, dialogue-act representation, footprint evidence, and other candidate assignments.
> Useful learned representations include gap-context embeddings, candidate embeddings, element-wise differences, embedding products, contextual cross-attention, contradiction probability, previous-turn compatibility, next-turn compatibility, and full-dialogue coherence.
> Hand-written lexical features may supplement learned representations but should not dominate them.
> Footprint Attribution
> For each footprint-gap pair, the model must estimate whether the footprint supports the missing turn assigned to that gap.
> The model may condition on the footprint text, selected candidate, visible context, missing speaker, gap position, and other selected turns.
> Footprint prediction is multilabel. Every released gold gap has at least one supporting footprint. Participants may still submit an empty footprint list when their system predicts that none of the supplied footprints are sufficiently supported.
> A footprint may be valid for more than one gap when permitted by the annotations.
> Thresholds may be global, gap-conditioned, candidate-conditioned, or calibrated separately for different footprint-bank sizes.
> Joint Assignment
> Candidate selection is globally constrained within each dialogue.
> A candidate may fill at most one gap.
> Let g be the number of gaps, c the number of candidates, and S[i, j] the learned compatibility score for assigning candidate j to gap i.
> The final assignment should maximize total learned compatibility while enforcing candidate uniqueness.
> Participants may use the Hungarian algorithm, integer linear assignment, beam search, constrained dynamic programming, exhaustive search for the small gap count, or another deterministic optimizer over learned scores.
> Because each dialogue contains at most three gaps, exact assignment is computationally inexpensive.
> Confidence and Ranking
> The system must return a top-five ranking for every gap.
> The ranking should use the final learned candidate scores after any global adjustment.
> The selected candidate must appear first.
> Rankings may not contain duplicate IDs, unknown IDs, or candidates from another dialogue.
> A candidate selected for another gap may appear lower in a ranking, but the final selected candidates must remain unique.
> Submission Format
> Submit one CSV file containing exactly these columns, in this order:
> dialogue_id,gap_id,selected_turn,ranked_turns,supporting_footprints
> The submission must contain exactly one row for every expected test gap.
> dialogue_id and gap_id must be copied exactly from public/test.jsonl.
> selected_turn must be one candidate ID from the corresponding dialogue’s candidate_turns list.
> ranked_turns has the logical data type “JSON array serialized as CSV text.” It must decode to a list of exactly five distinct candidate IDs, and the first item must equal selected_turn.
> supporting_footprints is also a JSON array serialized as CSV text. It contains zero or more footprint IDs from the corresponding dialogue.
> Use [] when no footprint is predicted.
> A correctly formatted submission may look like this:
> dialogue_id,gap_id,selected_turn,ranked_turns,supporting_footprints
> DG1042,G0,T1,"[""T1"",""T0"",""T4"",""T3"",""T2""]","[""F0""]"
> DG1042,G1,T2,"[""T2"",""T3"",""T0"",""T1"",""T4""]","[""F1"",""F2""]"
> After CSV parsing, the first ranked_turns value must decode to:
> ["T1", "T0", "T4", "T3", "T2"]
> Its supporting_footprints value must decode to:
> ["F0"]
> The complete JSON list is enclosed in CSV double quotes. Every double quote inside the JSON value is escaped by writing it twice.
> Predictions must use valid JSON with double-quoted strings. Python lists using single quotation marks are invalid.
> The recommended approach is to serialize the two list fields with json.dumps() and write the file using pandas.DataFrame.to_csv(index=False). The CSV writer will apply the required quoting automatically.
> For example:
> ranking_value = json.dumps(ranked_turn_ids)
> footprint_value = json.dumps(selected_footprint_ids)
> submission_rows.append({
> "dialogue_id": dialogue_id,
> "gap_id": gap_id,
> "selected_turn": selected_turn_id,
> "ranked_turns": ranking_value,
> "supporting_footprints": footprint_value
> })
> submission = pandas.DataFrame(
> submission_rows,
> columns=[
> "dialogue_id",
> "gap_id",
> "selected_turn",
> "ranked_turns",
> "supporting_footprints"
> ]
> )
> submission.to_csv("submission.csv", index=False)
> The submission must not contain an index column or any additional columns.
> Submission Requirements
> Each expected row must use the correct dialogue_id and gap_id, contain a valid selected candidate, provide exactly five distinct ranked candidates, place selected_turn first, and contain a valid JSON footprint list.
> All candidate and footprint IDs must belong to the corresponding dialogue.
> The ranking and footprint list may not contain duplicate IDs.
> Across all rows for one dialogue, selected candidates must be unique, and every expected gap must appear exactly once.
> Candidate and footprint IDs are case-sensitive.
> Invalid Prediction Handling
> Predictions are evaluated independently by gap whenever possible.
> A gap row is invalid when the expected row is missing or duplicated, selected_turn is blank or unknown, ranked_turns is invalid JSON or not a list, the ranking has the wrong length, the ranking contains duplicates, selected_turn is not first, a ranked candidate is unknown, supporting_footprints is invalid JSON or not a list, or a footprint ID is unknown or duplicated.
> An invalid gap receives zero for gap assignment accuracy, reciprocal rank, and footprint attachment F1.
> Other valid gaps remain eligible for credit.
> When two or more gaps in one dialogue select the same candidate, every colliding gap receives zero assignment credit and zero reciprocal-rank credit. The dialogue also receives zero exact-reconstruction credit.
> Non-colliding gaps remain eligible for footprint credit.
> Rows with blank or unknown identifiers are ignored. A missing expected row receives zero credit.
> The complete submission receives a score of 0.0 only when the CSV cannot be read, required columns are missing, additional columns are present, or columns are not in the required order.
> Evaluation
> Afterimage uses a maximization score ranging from 0.0 to 1.0.
> Higher scores are better.
> The final score is:
> Score = 0.40 × Gap Assignment Accuracy + 0.20 × Ranked Candidate MRR + 0.20 × Footprint Attachment Micro F1 + 0.15 × Exact Dialogue Recovery + 0.05 × Dialogue-Balanced Assignment Accuracy
> Gap Assignment Accuracy
> Weight: 0.40
> A gap receives credit when selected_turn matches the gold candidate.
> The metric is calculated globally across all expected gaps.
> Gap Assignment Accuracy =
> number of correctly selected gaps /
> total number of expected gaps
> A selection is incorrect when the wrong candidate is chosen, the row is invalid, or the selected candidate is reused by another gap in the same dialogue.
> This is the primary reconstruction metric.
> Ranked Candidate MRR
> Weight: 0.20
> For every gap, the reciprocal rank of the gold candidate is calculated from ranked_turns.
> Reciprocal Rank =
> 1 / rank of the gold candidate
> The possible values are:
> first: 1.0;
> second: 0.5;
> third: approximately 0.3333;
> fourth: 0.25;
> fifth: 0.2;
> absent: 0.0.
> Ranked Candidate MRR =
> sum of reciprocal-rank values /
> total number of expected gaps
> An invalid ranking receives 0.0.
> This component rewards systems that rank the correct reconstruction highly even when the top selection is wrong.
> Footprint Attachment Micro F1
> Weight: 0.20
> A footprint attachment is represented by:
> (dialogue_id, gap_id, footprint_id)
> Counts are accumulated globally across all expected gaps.
> TP_footprint is the number of predicted attachments that exactly match a gold attachment.
> FP_footprint is the number of predicted attachments that do not match a gold attachment.
> FN_footprint is the number of gold attachments that were not predicted.
> Precision =
> TP_footprint /
> (TP_footprint + FP_footprint)
> Recall =
> TP_footprint /
> (TP_footprint + FN_footprint)
> Footprint Attachment Micro F1 =
> 2 × TP_footprint /
> (2 × TP_footprint + FP_footprint + FN_footprint)
> A footprint is correct only when it is attached to the correct gap. A correct footprint assigned to the wrong gap is incorrect.
> An empty footprint list is valid.
> When both the prediction and target are empty for one gap, that gap contributes no positive or negative footprint item to the corpus-level calculation.
> Exact Dialogue Recovery
> Weight: 0.15
> A dialogue receives a score of 1 only when every gap selects the correct candidate, no candidate is reused, and every gap row is valid.
> Otherwise, the dialogue receives 0.
> Footprint predictions do not affect this component.
> Exact Dialogue Recovery =
> number of exactly reconstructed dialogues /
> total number of test dialogues
> A dialogue with one incorrect gap receives no exact credit.
> Dialogue-Balanced Assignment Accuracy
> Weight: 0.05
> Assignment accuracy is calculated separately within each dialogue.
> For dialogue d:
> Dialogue Accuracy_d =
> number of correctly selected gaps in d /
> number of expected gaps in d
> The final metric is:
> Dialogue-Balanced Assignment Accuracy =
> sum of Dialogue Accuracy values /
> number of test dialogues
> This prevents dialogues with more missing turns from contributing disproportionately.
> Compute Environment
> The official environment provides 10 CPU cores, 64 GB RAM, and no GPU, TPU, or other accelerator.
> The complete pipeline must run in this environment, including model loading, data reading, preprocessing, dialogue encoding, candidate encoding, footprint encoding, retrieval, learned reranking, footprint prediction, global assignment, validation, and submission generation.
> Internet access and remote inference services are unavailable during official prediction.
> Models requiring CUDA are not suitable.
> Compact and quantized pretrained models are permitted when they run locally within the available memory.
> CPU Feasibility
> Each dialogue contains at most 3 gaps, 50 candidate turns, and 80 footprints.
> This produces at most 150 gap-candidate pairs and 240 gap-footprint pairs.
> A compact bi-encoder can score all pairs efficiently.
> More expensive cross-encoder evaluation may be limited to the top 5 to 10 candidates and top 10 to 20 footprints for each gap.
> Recommended practices include encoding each text once, caching candidate and footprint embeddings, reusing full-dialogue representations, batching similar-length inputs, using vectorized similarity calculations, quantizing compact encoders, restricting cross-encoding to retrieved items, and applying exact deterministic assignment after learned scoring.
> A valid solution does not require a large generative model.
> Allowed Resources
> Participants may use the released training and test files; local pretrained language or embedding models; compact encoder or decoder models; quantized models; classical ML models trained on learned representations; and fine-tuning on the public training data.
> Contrastive training, pairwise or listwise ranking, hard-negative mining, locally built retrieval indexes, generic tokenization or linguistic libraries, lexical and structural features, deterministic assignment, validation, score calibration, caching, and ensembles are permitted within the compute limits.
> Synthetic examples may be created only from the public training data.
> Models and weights must be reproducibly available to ordinary participants.
> Prohibited Methods
> Participants may not access hidden test answers, manually label test gaps, search for original dialogue sentences or annotations online, retrieve source answers from external datasets, use search engines or online encyclopedias during prediction, use external factual databases to identify test dialogues, or use remote inference and hosted language-model services.
> Participants may not infer answers from candidate IDs, footprint IDs, row order, source-file positions, or hidden metadata. They may not reconstruct original answer groupings, manually encode answers for recognized test examples, exploit malformed-output behavior, submit a primarily rule-based system, or require unavailable hardware.
> Keyword matching, regular expressions, and deterministic heuristics are allowed only as supporting components within an ML-dominant pipeline.
> Public-Training Use
> Public training data may be used to learn dialogue-context representations, candidate compatibility, previous-turn and next-turn coherence, speaker-goal patterns, temporal consistency, footprint compatibility, candidate ranking, footprint attribution, confidence calibration, and global assignment adjustments.
> Hard negatives may be mined from the public training data.
> Participants must not manually assign test answers or retrieve individual test dialogues from external sources.
> Reproducibility
> Participants should retain enough information to reproduce their predictions.
> This includes model names and versions, pretrained-weight sources, quantization settings, preprocessing steps, training splits, hard-negative construction, feature definitions, ranking and footprint losses, threshold values, retrieval settings, assignment algorithms, random seeds, dependency versions, and prediction commands.
> The complete pipeline must be reproducible without a GPU or remote service.
> Solutions may be audited for compliance with the ML-dominance requirement.
> Additional Notes
> Participants should not assume that gaps can be solved independently, candidate or footprint order indicates relevance, every footprint belongs to exactly one gap, every valid footprint shares words with the candidate, lexical overlap determines correctness, the turn fitting the previous utterance is globally coherent, every gap has the same number of footprints, or adjacent turns necessarily share the same sentiment.
> A strong system must determine what event is missing, which candidate best fits the complete conversation, which latent statements support that event, which statements are distractors, how several missing events interact, and which combination produces the most coherent dialogue.
> Afterimage evaluates whether a model can reconstruct hidden conversational events from both visible context and their latent commonsense footprints.
> The task is solved not by predicting what follows a single utterance, but by jointly recovering several missing turns from the traces they leave across the conversation.

Inspiration note: Useful because it turns text understanding into a grounded prediction task with careful leakage controls and CPU-friendly modeling options.

## Dialogue Memory Compression

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx708fa310265k45j14hzhrb6x8aj8qj
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Beat rzotime's score of 0.125!

Full challenge description from page:

> Dialogue Memory Compression: What to Keep Before the Conversation Ends
> Overview
> An online assistant reading a live conversation cannot store every turn — as each turn arrives it must decide, on the spot, whether that turn is worth remembering. It has to commit while the conversation is still unfolding: it does not yet know how the conversation will continue, and it does not know what it will later be asked.
> This challenge evaluates exactly that decision on real multi-party technical-support chats. For each conversation you are given only its opening turns — the part seen so far by a memory system that is still listening. For every visible turn you must output a keep_score expressing how much that turn is worth retaining. Later — invisibly to you — a set of human questions is asked about the complete conversation, and each turn's true value is how much of that questioning it turns out to support. Your ranking of the visible turns is compared against those hidden values.
> You never see the questions, and you never see the rest of the conversation. Speakers are anonymized. The task is to predict future information demand from an incomplete conversation alone.
> Dataset Description
> Overview
> Each record is one visible turn from a real multi-party technical-support conversation. A conversation is split into speaker turns; only the opening portion of each conversation (roughly its first half) is ever shown, representing what an online memory system would have observed so far. Training conversations carry a revealed label for how much question-answering demand each visible turn attracted; test conversations do not.
> File Structure
> Prepared files live under ./dataset/public/:
> train.csv — labeled training conversations (visible turns, with demand labels).
> test.csv — held-out conversations to rank (visible turns, no labels).
> sample_submission.csv — a valid submission demonstrating the required format.
> dataset_manifest.json — summary counts and the metric name.
> Columns
> train.csv
> One row per visible turn, with the demand labels revealed:
> id (string) — turn id, dialogue_id__turn_id.
> dialogue_id (string) — conversation id.
> turn_id (int) — 0-based position of the turn among the visible turns.
> n_visible (int) — number of visible turns in this conversation.
> speaker (string) — anonymized per-conversation speaker id S0, S1, …).
> speaker_turns (int) — number of visible turns contributed by this speaker.
> text (string) — the turn text (lightly pre-tokenized, as in the source).
> token_len (int) — whitespace token count of text.
> query_count (int) — label: number of answerable questions (about the full conversation) whose answer is in this turn.
> is_evidence (int) — label: 1 if query_count > 0, else 0.
> test.csv
> One row per visible turn, without labels. Columns: id, dialogue_id, turn_id, n_visible, speaker, speaker_turns, text, token_len. Assign a keep_score to every row.
> Notes
> Redacted placeholders. A small number of highly specific identifiers in text — IP addresses, URLs, hardware/device ids, and chat handles — are replaced with generic placeholder tokens: <URL>, <EMAIL>, <IP>, <ID>. This affects a minority of turns and is applied identically to train.csv and test.csv; treat these tokens as ordinary words when processing the text.
> Pre-tokenization. Text is lightly pre-tokenized as in the source (e.g. does n't, spaced punctuation). token_len counts whitespace tokens on this text as-is.
> n_visible varies per conversation* — it is not a fixed window size, and only the visible turns for a given conversation are ever shown (never the full original conversation).
> Evaluation Methodology
> Submissions are scored by the mean per-conversation top-weighted Kendall rank correlation between your keep_score and a hidden, confound-adjusted per-turn demand target, using scipy.stats.weightedtau.
> Why confound-adjusted, not raw demand
> Raw per-turn demand (how many questions about the full conversation a turn answers) is partly explained by simple structural properties of a turn — its position in the conversation, its length, how many turns the conversation has, how active its speaker is. Scoring directly against raw demand would let a submission that only tracks those structural properties, without reading the turn content at all, score competitively. To make the score depend on understanding what a turn actually says, the grading target has had what a model using only structural features (turn position, relative position, token length, log token length, conversation size, speaker turn count — no text) can already explain subtracted out. This adjustment model is fit once on the held-out set's own structural features and true demand; you never see it or its output directly, only the resulting adjusted target through your score.
> Concretely: target = query_count - structural_only_prediction(position, length, conversation size, speaker activity). Your keep_score is compared against this target, not against raw query_count.
> Per-conversation score
> from scipy.stats import weightedtau
> import numpy as np
> def evaluate(keep_score, target):               # per conversation, target = confound-adjusted demand
> if np.unique(target).size < 2:               # unscorable (removed from the test set)
> return None
> if np.unique(keep_score).size < 2:           # no ranking information -> no credit
> return 0.0
> return weightedtau(keep_score, target)[0]
> weightedtau places more weight on agreement near the top of the ranking, so correctly identifying the turns that carry the most (adjusted) future demand matters more than ordering the low-demand tail.
> Final score
> The final score is max(0, mean of the per-conversation values over all scorable conversations), reported in [0, 1]. A ranking that perfectly matches the hidden demand scores 1.0; an uninformative or anti-correlated one scores 0.0. There is no budget and no ceiling below 1.0 — a perfect submission is achievable in principle and is not artificially capped.
> The grader is lenient about submission content: as long as your run writes a submission.csv, it always receives a score. Missing rows, duplicate ids, non-numeric / NaN scores, or extra columns are handled gracefully — affected turns simply contribute no ranking information for their conversation. The worst possible outcome is a real 0.0; the grader never raises an error on a malformed submission.
> Submission Format
> Submit submission.csv with exactly these columns:
> id (string) — turn id from test.csv.
> keep_score (float) — how much to retain this turn (higher = keep first).
> One row per turn in test.csv, each id present exactly once, plus a header row.
> Important: Only Within-Conversation Order Matters
> Only the relative ordering of keep_score within each conversation is scored — the absolute scale is irrelevant, and scores are not compared across conversations. A submission with the same keep_score for every turn in a conversation carries no ranking information and scores 0.0 for that conversation specifically, so ensure your scores actually vary within each conversation's turns.
> Requirements
> keep_score must be finite and numeric.
> Read only from ./dataset/public/; write submission.csv to ./working/.
> CPU only; must finish within the time limit.
> Example Submission CSV Snippet
> id,keep_score
> t00042__0,0.13
> t00042__1,0.87
> t00042__2,0.41
> t00043__0,0.55
> t00043__1,0.09
> What Not to Use
> Do not use the private ground truth query_count, the questions, or any part of a conversation beyond its shipped visible turns) — none of this is available to you, and any attempt to obtain it defeats the task.
> Do not try to reconstruct hidden test-side labels by matching test.csv text against train.csv, against each other, or against any external copy of this data you might locate — every shipped conversation is unique to its split; no such match will return valid signal, and relying on one is disqualifying.
> Do not attempt to identify, search for, or download the original source dataset this challenge is built from. The task must be solved from the provided files alone.
> Do not use a GPU or any approach that assumes GPU availability. The evaluation environment is CPU-only; solutions must complete within the stated time limit on CPU.
> Do not use network access, external APIs, or pretrained models fetched over the network. Solve using only the provided files and standard CPU-based Kaggle Docker libraries.

Inspiration note: Useful because it turns text understanding into a grounded prediction task with careful leakage controls and CPU-friendly modeling options.

## Masked Patent Claim Lineage Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fycf7xm6k89svyjtvrpc6bx8ag9zc
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Patent claims are the numbered legal statements that define what an invention covers. Later claims often depend on earlier claims: they narrow, extend, or add conditions to a previous claim instead of restating the full invention. In this challenge, that parent-child structure is represented as a dependency ledger.
> Each row is an anonymized patent claim set. The original patent number, title, source URL, inventor fields, assignee fields, dates, and other provenance metadata are not public. Claims are represented only by row-local ids such as C001, C002, and C003.
> The task is to recover the hidden claim dependency ledger. A valid ledger is a JSON list of directed edges from a dependent claim to the earlier claim it depends on. Explicit references and selected shortcut-bearing expressions have been normalized, so participants must infer parent-child structure from the remaining semantics, narrowing operations, local roles, and graph constraints.
> This is not a patent classification task and not a retrieval task. Strong solutions must compare multiple plausible earlier claims within each row and decide which claim each dependent claim actually narrows or extends.
> The row ids and claim ids are local to this package. The same claim id in two different rows has no shared meaning.
> Dataset
> The prepared challenge files contain 300 completed training rows and 200 held-out evaluation rows. Each row is one local patent claim set.
> Files:
> train.csv: Public input fields plus the reference target.
> test.csv: Evaluation inputs without answers.
> sample_submission.csv: A valid low-information submission with all evaluation ids.
> Public columns:
> sample_id (string): Opaque anonymized row id.
> claims (JSON string encoded in CSV): Ordered JSON list of claim objects for the row.
> target (JSON string encoded in CSV, train/private only): Reference dependency ledger.
> Claim fields:
> cid (string): Local claim id such as C001.
> text (string): Normalized claim text.
> Claim-set structure:
> Each row contains 12 to 54 claims.
> Claim ids are contiguous within a row: C001, C002, ..., up to that row's final claim id.
> Each row has 8 to 50 dependency edges.
> The dependency structure is a directed acyclic graph over the local claims.
> A child claim may have more than one parent in rare cases.
> Every submitted parent must appear before its child, so an edge like {"child":"C009","parent":"C003"} is valid in direction, but {"child":"C003","parent":"C009"} is invalid.
> C001 is always a root claim and cannot be used as a child in a valid dependency edge.
> Example claims value from train.csv format, shortened for readability:
> [
> {
> "cid": "C001",
> "text": "A non-invasive method of measuring the temperature ... the method comprising measuring a [TECH] temperature ..."
> },
> {
> "cid": "C002",
> "text": "A method as claimed in claim [REF], wherein further comprising [TECH] a [TECH] ..."
> },
> {
> "cid": "C003",
> "text": "A method as claimed in claim [REF], wherein the [TECH] comprises counting a stabilisation time ..."
> }
> ]
> Example target value from train.csv format:
> [
> {"child": "C002", "parent": "C001"},
> {"child": "C003", "parent": "C002"},
> {"child": "C004", "parent": "C002"}
> ]
> Text markers:
> [REF]: An explicit claim-number reference was present, but its number or range is hidden.
> [TECH]: A shortcut-bearing technical term was normalized. This is a generic marker, not a stable entity id; two [TECH] occurrences do not necessarily refer to the same entity.
> [ORD]: An ordinal or role-order qualifier was normalized.
> [REL]: A directional or positional qualifier was normalized.
> [VALUE]: A numeric or measurement expression was normalized.
> The public claim order is topologically valid: every true parent appears before its child. Source adjacency is not preserved, and adjacent claim ids do not imply a dependency. Claim ids are reassigned after this ordering and carry no meaning beyond the row.
> Prediction Target
> For each test.csv row, predict the hidden dependency ledger as a JSON list. Each edge object has exactly:
> child (string): Local dependent claim id, such as C008.
> parent (string): Local earlier parent claim id, such as C003.
> The order of edge objects inside the JSON list does not matter. Duplicate edges are not allowed.
> Submission Format
> Submit a CSV with exactly these columns, in this order:
> sample_id
> prediction
> The prediction column must be a JSON string encoded inside the CSV cell. It must decode to a JSON list of edge objects.
> Malformed JSON, missing columns, extra columns, duplicate ids, missing ids, extra ids, duplicate edges, invalid claim ids, unknown claim ids for that row, and edges where the parent does not precede the child are rejected before scoring.
> Example submission:
> sample_id,prediction
> sample_0123456789abcdef0123456789abcdef,"[{""child"":""C002"",""parent"":""C001""},{""child"":""C003"",""parent"":""C001""}]"
> sample_fedcba9876543210fedcba9876543210,"[{""child"":""C002"",""parent"":""C001""},{""child"":""C005"",""parent"":""C003""},{""child"":""C006"",""parent"":""C005""}]"
> Evaluation
> Scores are bounded from 0 to 1, with higher better. A perfect private-answer submission scores exactly 1.0.
> For each row, define an edge key as:
> edge_key = (child, parent)
> For any set of submitted and reference edges, ordinary F1 is:
> precision = |submitted_edge_keys intersection reference_edge_keys| / |submitted_edge_keys|
> recall    = |submitted_edge_keys intersection reference_edge_keys| / |reference_edge_keys|
> edge_f1   = 2  *precision*  recall / (precision + recall)
> Edge-case handling:
> If both the submitted edge set and reference edge set are empty, that F1 component is 1.0.
> If exactly one of the submitted or reference edge sets is empty, that F1 component is 0.0.
> If there are submitted and reference edges but no correct overlap, that F1 component is 0.0.
> In this challenge the reference rows contain dependency edges, so submitting [] for every row receives 0.0.
> The final metric has three components:
> weighted_edge_f1
> This is global edge F1 over all evaluation rows, but each edge receives a difficulty weight before computing precision and recall.
> For an edge (child, parent), define:
> distance = numeric(child) - numeric(parent)
> where numeric("C008") = 8.
> Edge weights are:
> 2.50 if parent != C001 and distance > 1
> 1.75 if parent != C001 and distance == 1
> 1.25 if parent == C001 and distance > 1
> 1.00 if parent == C001 and distance == 1
> Then:
> weighted_precision = weight(correct_edges) / weight(submitted_edges)
> weighted_recall    = weight(correct_edges) / weight(reference_edges)
> weighted_edge_f1   = 2  *weighted_precision*  weighted_recall
> / (weighted_precision + weighted_recall)
> hard_edge_f1
> Hard edges are the subset of edges where:
> parent != C001 and distance > 1
> hard_edge_f1 is ordinary set F1 computed only on those hard edges across all evaluation rows.
> mean_row_f1
> For each row, compute ordinary set F1 between that row's submitted edges and reference edges. mean_row_f1 is the arithmetic mean of those row-level F1 values.
> The final score is:
> score = 0.55 * weighted_edge_f1
> + 0.30 * hard_edge_f1
> + 0.15 * mean_row_f1
> Invalid submissions are rejected before scoring.
> Originality
> This challenge is an adapted semantic reconstruction task built from public patent-claim data. The nearest public resource family consists of patent-claim datasets and claim-parsing tools that extract dependency references from explicit claim text.
> This benchmark changes that task substantially. It is not a direct claim-reference extraction problem. Explicit parent references are masked, source identifiers are removed, local claim ids are anonymized, and the claim order is transformed while preserving only valid parent-before-child structure. In addition, distinctive repeated technical continuity terms are normalized into generic placeholders such as [TECH], so participants cannot solve the task by simple string matching between a dependent claim and an earlier claim.
> The target is a hidden lineage graph over local claim ids. The public input contains only the transformed claim packet, not source patent identifiers, provenance fields, original claim numbering, or external lookup keys.
> The scoring also differs from standard claim parsing. The metric emphasizes hard non-root and non-nearest dependency edges, which makes trivial star, chain, or nearest-neighbor strategies weak. The challenge is therefore framed as small-data masked semantic lineage recovery rather than ordinary patent parsing or public benchmark replication.
> External patent lookup, source matching, or reconstruction from outside records is not part of the task.
> What Not To Use
> External lookup, record matching, or attempts to identify the original source records.
> Original source ids, URLs, titles, dates, people, organizations, non-public files, answer files, row order, package-generation internals, or hardcoded id-to-graph maps.
> Precomputed copies of the exact evaluation rows or answers from outside the supplied public challenge files.

Inspiration note: Useful because it turns text understanding into a grounded prediction task with careful leakage controls and CPU-friendly modeling options.

## Vietnamese Mancala Outcome Forecasting

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx736npd0pw44ddb90h46wnd5d8a613t
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Vietnamese Mancala Outcome Forecasting
> Overview
> Each item in this competition is a narrated transcript of the opening and middle of a single Ô Ăn Quan match — a traditional two-player Vietnamese mancala game — written in colloquial Vietnamese. The narration follows the two sides (A and B) as they scoop and sow stones and capture cells, but it stops partway through the match, before the game is decided. Your task is to forecast how the finished game turns out: for each transcript you submit a probability distribution over five final-margin outcomes, from a decisive win for one side, through a close game, to a decisive win for the other.
> The point of cutting the narration short is that the ending is genuinely undetermined by what you are shown. Tallying the captures described so far tells you who is ahead at the cut, but Ô Ăn Quan positions swing: a side sitting on a large mandarin cell, or holding stones poised over a soon-to-be-capturable configuration, can overturn a lead in the remaining moves. Recovering the eventual outcome therefore requires reading the narrated moves for what they imply about the board that is left standing at the cut — which stones sit where, whose turn it is, which captures are set up — and learning, from the training transcripts and their known endings, how such mid-game situations tend to resolve. Alongside the forecast, each test match asks you to recover the match ledger the narration implies at the cut — both sides' captured-point totals, how many mandarin cells remain uncaptured, and which side holds the next turn.
> The scenario is deliberately noisy. The narration is informal and varied — the same move or capture is described many different ways, quantities are sometimes given loosely, and filler commentary is interleaved with the substantive moves. Transcripts are cut at different fractions of the game, so some end with the outcome nearly settled and others while it is wide open. Because the five outcomes are not equally common, the metric macro-averages across the true outcome classes so that a model cannot do well merely by always predicting the most frequent ending.
> The competition is sized to run end-to-end — loading, training, and inference — within 1.5 hours on a single CPU node (10 cores, 62 GB RAM, no GPU).
> Dataset
> All CSV files are UTF-8 encoded with a byte-order mark; if your CSV reader is not BOM-aware, open them with encoding utf-8-sig.
> Public files
> public/train.csv — one row per training match: the narrated partial transcript, the cut fraction, an ASCII snapshot of the board at the cut, the four ledger values at the cut (captured points per side, mandarins remaining, side to move), and the true final outcome.
> public/test.csv — one row per test match, with the transcript and cut fraction only; no outcome.
> public/sample_submission.csv — a correctly-formatted example submission (uniform distribution) that scores a small non-zero value.
> Private file (organizer only)
> private/answers.csv — columns: id, outcome, final_margin, and the true ledger values at the cut (score_a, score_b, quan_remaining, to_move).
> Column descriptions
> Every column in the public files and the submission is described below.
> id (string) — unique match identifier, e.g. game_5f2ac91d. Present in train.csv, test.csv, and the submission.
> transcript (string) — the colloquial Vietnamese narration of the opening and middle of the match, cut before the game ends. The primary input. Present in train.csv and test.csv.
> cut_fraction (float) — the fraction of the full match's moves that the narration covers, in (0, 1). Present in train.csv and test.csv.
> board_ascii (string) — an exact ASCII rendering of the board at the moment the narration stops: the two mandarin cells (Q while the mandarin is in place, x once captured, followed by the stone count), the five dan cells of each side (. for empty, otherwise the stone count), both running scores, and the side to move (luot:). Present in train.csv only; test matches provide the narration and cut fraction only.
> score_a (integer) — points side A has captured by the cut. Present in train.csv only.
> score_b (integer) — points side B has captured by the cut. Present in train.csv only.
> quan_remaining (integer) — mandarin cells still uncaptured at the cut: 0, 1, or 2. Present in train.csv only.
> to_move (string) — the side to move at the cut, A or B. Present in train.csv only.
> outcome (string) — the true final-margin class, one of A_big, A_slim, close, B_slim, B_big (defined in Evaluation). Present in train.csv only.
> final_margin (integer) — the signed final score margin (A minus B) from which outcome is derived; provided for analysis. Present in train.csv only.
> prob_A_big … prob_B_big (float) — submission-only: your forecast probability for each of the five outcome classes, each in [0, 1], summing to 1.0 within 0.02.
> pred_score_a (integer) — submission-only: your estimate of side A's captured points at the cut (non-negative); values above 500 are rejected as malformed.
> pred_score_b (integer) — submission-only: your estimate of side B's captured points at the cut (non-negative); values above 500 are rejected as malformed.
> pred_quan_remaining (integer) — submission-only: your estimate of the mandarin cells still uncaptured at the cut, one of 0, 1, or 2.
> pred_to_move (string) — submission-only: the side you infer to move next at the cut, A or B (case-insensitive).
> Data example
> A single truncated train.csv row:
> id,transcript,cut_fraction,board_ascii,score_a,score_b,quan_remaining,to_move,outcome,final_margin
> game_5f2ac91d,"Một ván Ô ăn quan giữa bên A và phe B. Người B thu được một ô. ...",0.55,"Q5 | 6  .  4  .  2 | ...",12,9,1,B,A_slim,13
> Submission format
> A CSV with exactly these columns and one row per test match:
> id,prob_A_big,prob_A_slim,prob_close,prob_B_slim,prob_B_big,pred_score_a,pred_score_b,pred_quan_remaining,pred_to_move
> The file must include a header row with exactly these column names.
> id — the test match id. Every test id must appear exactly once; missing, unknown, or duplicate ids are rejected.
> prob_A_big … prob_B_big — your forecast probability for each of the five outcome classes, each in [0, 1]. The five values must sum to 1.0 within a tolerance of 0.02; they are renormalised before scoring.
> pred_score_a, pred_score_b — your estimate of each side's captured points at the cut (non-negative integers; values above 500 are rejected as malformed).
> pred_quan_remaining — your estimate of how many mandarin cells remain uncaptured at the cut: 0, 1, or 2.
> pred_to_move — the side you infer to move next at the cut: A or B (case-insensitive).
> Every column is required in every row; empty cells are rejected.
> Sample submission row:
> game_5f2ac91d,0.2,0.2,0.2,0.2,0.2,6,6,2,A
> Evaluation
> Metric: forecast skill blended with ledger-recovery credit. Higher is better; the score lies in [0.02, 1.0].
> Outcome component. For a match with true outcome class c and predicted distribution p:
> brier(i) = sum over classes k of (p_k - [k == c])^2      # in [0, 2]
> raw(i)   = 1 - 0.5 * brier(i)                             # in [0, 1]
> Per-match values are grouped by the true outcome class and averaged within each class; the five class means are combined by an unweighted mean into macro, so rare decisive outcomes count as much as common close games. The macro value is then expressed as skill over the uniform forecast, which scores 0.6 on this scale:
> outcome_skill = clamp((macro - 0.6) / 0.4, 0, 1)
> Outcome classes. The true class is derived from the signed final margin (A minus B): A_big — margin ≥ 25; A_slim — 9 ≤ margin < 25; close — −9 < margin < 9; B_slim — −25 < margin ≤ −9; B_big — margin ≤ −25.
> Ledger component. Per match:
> score_part = mean over the two sides of max(0, 1 - |pred_score - true_score| / 6)
> quan_part  = 1 if pred_quan_remaining is exactly right else 0
> move_part  = 1 if pred_to_move is exactly right else 0
> state(i)   = 0.5 * score_part + 0.3 * quan_part + 0.2 * move_part
> state_mean is the plain mean of state(i) over all test matches (state is the grader's internal name for the ledger credit). The / 6 linear decay gives no credit for a side's captured-point estimate that is 6 or more points off.
> Final score.
> score = max(0.02, min(1.0, 0.65 * outcome_skill + 0.35 * state_mean))
> The floor of 0.02 ensures a valid submission never returns exactly zero; it is a platform requirement, not part of the metric. A uniform forecast with constant ledger guesses scores near the bottom of the scale because outcome_skill is 0 and the constant guesses earn only incidental credit. The ledger component exists because the ledger is deliberately never shown for test matches — it must be recovered from the narration; the asymmetric credit (linear for point totals, exact-match for the mandarin count and the turn holder) reflects that the latter two are fully determined by a correct reading while point totals can only be estimated.
> What Not To Use (Prohibited Methods)
> Do not attempt to reconstruct or re-simulate the exact game generator to compute the deterministic continuation of a test match; the forecast must be learned from the training transcripts and their outcomes, not produced by reverse-engineering the data-generating program.
> Do not use any external Ô Ăn Quan engine, solver, or move database to roll a test position forward to its exact ending.
> Do not use the id string or the row order of the CSVs as a predictive signal.
> Standard prohibitions also apply: no external answer keys, no id-based hardcoding, no train/test leakage, and no tuning on the private labels.

Inspiration note: Useful because it turns text understanding into a grounded prediction task with careful leakage controls and CPU-friendly modeling options.

## Narrative Causal Graph Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71d56gw7gzs9cf2psgb9etc58any1q
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Beat rekht's score of 0.513!

Full challenge description from page:

> Narrative Causal Graph Recovery
> Overview
> Human stories are more than ordered sentences: actions depend on earlier events, descriptions establish conditions, and protagonists can act, receive actions, or do both. Recovering that structure is useful for privacy-preserving narrative-quality assessment, long-context memory systems, and tools that check whether generated stories remain causally coherent.
> For each target sentence, select the causal predecessors explicitly identified by human readers in the three dependency fields, classify the sentence as an action or description, and identify the protagonist's role. The separate PREVIOUS ACTION annotation is not treated as a causal edge. Two independent annotation passes define the hidden target, and evaluation preserves their disagreement instead of collapsing subjective judgments into a false single truth.
> To protect participant text and block public-source lookup, every word is replaced by a stable opaque lexical token before release. Each target and candidate is represented by exactly 12 tokens, and each row exposes exactly 8 shuffled earlier candidates with coarse distance buckets. This preserves repeated-word identity and causal-learning signal without exposing raw words, sentence lengths, story lengths, or ordered story fingerprints. No generated sentences or labels are added. The holdout contains complete unseen stories.
> Dataset
> File descriptions
> train.csv -- 421 target-candidate observations from 19 complete stories, including six label columns from two annotators.
> test.csv -- 118 target-candidate observations from 6 complete held-out stories, with labels removed.
> sample_submission.csv -- Submission template with seeded non-constant example predictions.
> Column descriptions
> id (string) -- Unique 12-character hexadecimal identifier for the prediction row.
> target_text (string) -- Fixed-size 12-token privacy sketch of the target sentence. Equal w_........ tokens represent equal case-folded words across the dataset.
> candidate_context (string) -- Eight shuffled earlier candidate sentences. Each line has a candidate ID c00 through c07), coarse distance bucket d1 through d4 or d5plus), and a fixed-size 12-token privacy sketch.
> parents_a1 (string, train only) -- Pipe-separated causal candidate IDs from annotator 1; empty when none were marked.
> parents_a2 (string, train only) -- Pipe-separated causal candidate IDs from annotator 2; empty when none were marked.
> type_a1 (string, train only) -- Annotator 1 narrative function: action or description.
> type_a2 (string, train only) -- Annotator 2 narrative function: action or description.
> role_a1 (string, train only) -- Annotator 1 protagonist role: none, agent, object, or both.
> role_a2 (string, train only) -- Annotator 2 protagonist role using the same four values.
> Evaluation
> Submissions are scored with Dual-Annotator Narrative Graph Score. It combines three bounded components:
> For each row, compute set F1 between predicted causal parents and each annotator's parent set, then average over both annotators and all rows. Weight: 55%.
> Compute macro-F1 for narrative_type against each annotator separately, then average. Weight: 20%.
> Compute macro-F1 for protagonist_role against each annotator separately, then average. Weight: 25%.
> score = 0.55  *mean_dual_parent_set_f1 + 0.20*  mean_dual_type_macro_f1 + 0.25 * mean_dual_role_macro_f1
> The score ranges from 0 to 1; higher is better. Averaging against both annotation passes gives partial credit when a prediction matches one reasonable human reading but not the other.
> Submission
> Submit a CSV file with one prediction for every row in test.csv.
> id (string) -- Exact row identifier from test.csv.
> parent_ids (string) -- Empty, one candidate ID, or unique pipe-separated candidate IDs such as c02|c07.
> narrative_type (string) -- Exactly action or description.
> protagonist_role (string) -- Exactly none, agent, object, or both.
> Example:
> id,parent_ids,narrative_type,protagonist_role
> 4c356c839454,c02|c07,action,agent
> 731cbc879d59,,description,object
> Requirements
> The file must contain exactly 118 rows plus the header.
> Every id from test.csv must appear exactly once.
> Columns must be exactly id,parent_ids,narrative_type,protagonist_role in that order.
> parent_ids must contain only c00 through c07; duplicates are invalid.
> Missing values are allowed only to represent an empty parent_ids set.
> File format: CSV only.
> What Not To Use
> Do not reverse or bypass the privacy tokenization to recover annotations from external copies of participant stories or annotation files; that defeats the intended causal-structure modeling task.
> Do not build a row-order or identifier lookup against a mirrored annotation table; opaque IDs and story-level holdout are intended to prevent target recovery.
> Do not submit fixed story templates or hand-coded answers for individual held-out narratives; predictions must generalize from the provided labeled stories.

Inspiration note: Useful because it turns text understanding into a grounded prediction task with careful leakage controls and CPU-friendly modeling options.

## Redacted Text Authorship Clustering

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bab2345dk4kbyh1w0178fe58ah5th
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat dev_natha's score of 0.666!

Full challenge description from page:

> You are handed 432 redacted prose passages (~210 words each), scrambled together with no author labels. Every content word — every noun, verb, adjective, adverb, name and topic word — has been blacked out with a length-preserving mask (####). Only the closed-class skeleton survives: function words (articles, pronouns, prepositions, conjunctions, auxiliaries), punctuation, contractions, and sentence structure.
> The passages were written by exactly 12 different authors, each represented by passages drawn from several books. Your job is to recover the hidden authorship from the skeleton alone: partition the passages into 12 groups so that each group contains all and only the passages written by one author.
> This is an unsupervised, transfer problem. You are given a labelled training corpus of passages from 16 completely different authors (disjoint from the 12 in the test set), redacted the same way. You may use it freely to design and validate a representation of writing style, but you can never train a classifier on the authors you actually have to separate — they do not appear in the training data.
> The twist that makes this hard: redaction removes topic and vocabulary by construction, so there is nothing left to cluster on except style — function-word habits, punctuation rhythm, sentence length and construction, the density and placement of masked content, and character n-gram patterns over the skeleton. The classic stylometry shortcuts that quietly lean on content words (topical char n-grams, rare-word frequencies) are gone; what remains is the syntactic fingerprint. A strong solution learns a topic-free style representation from the redacted skeleton that generalises to authors it has never seen, then clusters with it.
> Real-world analogues: de-anonymising redacted leaked documents, forensic linguistics on censored text, detecting sock-puppet accounts by grammatical habit, and settling disputed authorship.
> Evaluation
> Submissions are scored with the Adjusted Rand Index (ARI) between your predicted clustering and the true authorship partition of the test passages.
> ARI measures agreement between two partitions while correcting for chance. It is invariant to cluster names — only the grouping matters, not which integer you assign to a cluster — so you do not need to guess which cluster is which author.
> ARI = 1.0 — perfect recovery of the authorship partition.
> ARI ≈ 0.0 — no better than a random assignment (as are degenerate submissions such as all-one-cluster or all-distinct).
> ARI can be slightly negative for worse-than-random labelings.
> from sklearn.metrics import adjusted_rand_score
> def evaluate(y_true_author_id, y_pred_cluster):
> return adjusted_rand_score(y_true_author_id, y_pred_cluster)
> The number of authors, K = 12, is given. You may submit any integer cluster labels; you are not required to produce exactly 12 non-empty clusters, but ARI rewards matching the true 12-way partition.
> Dataset
> Prepared files live under ./dataset/public/:
> train.csv — 960 labelled, redacted passages from 16 training authors (disjoint from the test authors). Columns: passage_id, author_id (0–15), book_id (Project Gutenberg id, so you can build cross-book validation), text.
> test.csv — 432 unlabelled, redacted passages from 12 held-out authors. Columns: passage_id, text. Order is shuffled and carries no information.
> sample_submission.csv — a correctly formatted example submission.
> challenge_meta.json — small metadata blob, including n_test_authors (K).
> All passages are ~210 words of running prose extracted from public-domain Project Gutenberg books and then redacted (content words replaced by length-preserving #### masks). Each test author contributes 36 passages spread across 3 books; classes are exactly balanced.
> Submission
> Write ./working/submission.csv with one row per test passage:
> passage_id (str) — Test passage id, exactly as in test.csv.
> cluster (int) — Cluster label you assign (labels are arbitrary).
> Requirements
> Exactly 432 rows, one per passage_id in test.csv, plus a header.
> Every passage_id from test.csv must appear exactly once.
> cluster may be any integer labels; passages you believe share an author must share a cluster label. Cluster label names are ignored by the metric.
> Not Allowed
> GPU usage — CPU only.
> Training a classifier on the test authors (they are disjoint from training and unlabelled, so this is impossible by design).
> Using external author labels, book titles, or any outside information to identify test passages.
> Producing a submission that does not cover every passage_id in test.csv exactly once.

Inspiration note: Useful because it turns text understanding into a grounded prediction task with careful leakage controls and CPU-friendly modeling options.

## Recovering Injury Codes from Redacted Incident Reports

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bp58hfjhkh2r9gb3eez5bw98a9qd2
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat kris's score of 0.579!

Full challenge description from page:

> What Happened on the Floor: Recovering Injury Codes from Redacted Incident Reports
> The problem
> An occupational safety inspector visits the site of a serious workplace accident, writes up what happened, and files a set of coded fields summarizing it: how severe the injury was, what kind of event caused it, what part of the body it struck, and what object inflicted it. You are given the write-up. You produce seven codes: five describing the primary worker, and two describing the incident as a whole.
> Each row is one incident, and the report describes it whole: the worksite, the task in progress, the machine or material involved, the moment things went wrong, and sometimes more than one worker hurt at once. Five of the seven codes describe the incident's primary worker: severity, event, injury, body part, and source. They are coupled, since a fall from a scaffold, a crushed hand, a fractured skull, and a struck-by-object source are four descriptions of one physical event, and predicting them independently produces combinations that never occur and loses ground on the rare codes.
> The other two codes are about the incident as a whole, and they are the part of this task that does not exist anywhere else. Many workplace accidents injure more than one person. multiple asks whether this incident hurt more than one worker; spread asks whether the injured workers came out at different severity levels, one killed and another only bruised. Neither can be read off a single worker's record. A model has to comprehend the entire narrative and reason about everyone in it. The public injury-coding datasets cannot pose these questions at all, because they were built by flattening each incident to one worker and discarding the rest. That structure is gone from them and preserved here.
> The same multi-worker structure quietly complicates the five per-worker codes. When several people are hurt in one incident, they are not hurt the same way: across multi-worker incidents the victims differ on body part 38 percent of the time, on event 14 percent, and on severity 48 percent. The five codes are scored against the primary worker, the one on the lowest injury line, so a model reading a shared narrative cannot simply detect that some injury appears somewhere in the text. It has to bind the right injury to the right worker, attributing the fractured skull to the person who fell and the burn to the person who did not. That is an attribution problem, not a lookup, and it has no analogue in a benchmark where every narrative already belongs to exactly one worker.
> There is a deliberate obstacle. Inspectors write the ending into the report: Employee #1 was killed. Remained hospitalized. Was treated and released. A model that reads those phrases is not inferring severity, it is copying it, and even a simple word-count model exploits exactly this to reach a quadratic-weighted kappa of about 0.85 on the raw text. So the endings are gone. Every word naming death, hospitalization, ambulances, treatment, or medical disposition has been scrubbed from wherever it appears, about 6 percent of the characters, while the rest of the sentence around it stays. "Employee #1 was killed when the scaffold collapsed at 26 feet" becomes "Employee #1 was when the scaffold collapsed at 26 feet": the outcome is gone, the mechanism is not. In the text you receive, residual outcome words measure 0.0000.
> Calendar dates are stripped too, for a different reason. A date reveals which side of the time boundary a row falls on and helps pin down a specific real incident; it says nothing about the accident itself. Clock times stay, since hour of day carries a little signal about shift and lighting.
> What is left is the mechanism, and mechanism is all you get. The height of the fall, the type of press, the substance in the tank, the point of contact. On the redacted text that same word-count trick loses a meaningful share of its power on severity, since the outcome keyword it was copying is gone. Some of what remains is legitimately mechanism: an electrocution or a decapitation is severe because of what it is, not because a disposition word said so, and a model that reasons this way is doing exactly what the task rewards. Closing the rest of the distance is the work.
> Severity is graded on an inverted ordinal scale. Code 1 is a fatality, the worst outcome; code 3 is non-hospitalized, the mildest. Anyone who reindexes the labels, applies an ordinal loss, or fits a regression without checking direction will have the penalty pointing the wrong way.
> Training and evaluation are separated in time, not sampled at random. Training incidents predate 2009; evaluation incidents follow. The mix shifts across that line, with fatalities dropping from 47.4 percent of training incidents to 37.8 percent of evaluation incidents, so a model tuned to the training frequencies arrives miscalibrated. Splitting train.csv at random to validate will flatter you.
> The mildest severity class cannot be fully recovered from the text. A hand amputation that led to admission and one that did not are described in the same words; whether it counted as hospitalization depended on how far the hospital was, what the employer required, and how the inspector filed a borderline case, none of which reaches the page. And the word hospital is scrubbed from the text you receive in any case, so the distinction has to be inferred from the mechanism of the injury rather than read off a disposition keyword. Part of this class is legible in the mechanism and part is simply noise.
> And the tail is where the points are. Macro F1 counts every class the same, so source, with 48 classes and 13 of them under 25 evaluation examples, rewards the rare codes far more than the common ones. Nailing the frequent classes is nearly free and worth almost nothing.
> The two whole-incident heads are minority signals hidden in redacted prose. Multi-victim incidents are a small fraction of the set, and a model that always answers "one worker, single severity" scores zero on both, since they are graded on the positive class. Finding the incidents that injured several people, and the narrower set that injured them unequally, means catching cues the redaction leaves behind: plural workers, several tasks running at once, a collapse or release that swept up a crew. A simple word-count baseline clears the trivial floor on both by a wide margin without coming close to solving them, so there is real signal, and real distance left to close.
> Dataset
> train.csv
> Column          Type     Description
> ──────────────────────────────────────────────────────────────────────────
> id        string   Opaque hashed incident identifier
> report    string   Redacted accident narrative
> age       float    Age of the injured worker, nullable
> sex       string   M or F, nullable
> severity  int      Target. Primary worker severity, ordinal inverted. 3 classes
> event     int      Target. Kind of event. 14 classes
> injury    int      Target. Kind of injury. 22 classes
> bodypart  int      Target. Body part affected. 31 classes
> source    int      Target. Object or substance that inflicted it. 48 classes
> spread    int      Target. 1 if workers hurt at differing severities. Binary
> multiple  int      Target. 1 if more than one worker was injured. Binary
> test.csv
> Column          Type     Description
> ──────────────────────────────────────────────────────────────────────────
> id        string   Opaque hashed incident identifier
> report    string   Redacted accident narrative
> age       float    Age of the injured worker, nullable
> sex       string   M or F, nullable
> label_space.json
> Valid class codes for each head, taken from the training split. spread and multiple are binary (0 or 1).
> sample_submission.csv
> A valid but deliberately weak submission: the training mode on every head. It scores about 0.009.
> Rows: 91,127 training, 16,720 evaluation. Each row is one incident. Training incidents occurred through 2008, evaluation incidents after 2008. Narrative length: median 424 characters, 95th percentile approximately 1,150, maximum 8,537. Nullity: age 0.06 percent train and 0.38 percent test, sex 0.01 percent train and 0.36 percent test.
> Class codes are contiguous integers from 1. One class, injury code 19, occurs in training and not in evaluation. The codes are opaque: their meanings are not released and are not required to solve the task. Nothing about the task depends on knowing that code 7 means one thing rather than another, only on predicting which code an inspector assigned.
> severity
> Code   Meaning                       Train share   Test share
> ────────────────────────────────────────────────────────────
> 1      Fatality, most severe               0.474        0.378
> 2      Hospitalized                        0.426        0.505
> 3      Non-hospitalized, least severe      0.100        0.116
> Evaluation
> Each head is scored independently. The final score is the unweighted mean of the seven head scores.
> 1. Severity, quadratic-weighted kappa. With k = 3 ordered classes, observed agreement O, expected agreement E under independent marginals, and weights w_ij = (i - j)^2 / (k - 1)^2:
> kappa = 1 - ( sum_ij w_ij · O_ij ) / ( sum_ij w_ij · E_ij )
> The weight matrix is therefore
> pred 1   pred 2   pred 3
> true 1    0.00     0.25     1.00
> true 2    0.25     0.00     0.25
> true 3    1.00     0.25     0.00
> Confusing fatality with non-hospitalized is penalised four times as heavily as an adjacent-class error. A constant prediction scores 0.0.
> 2. Four categorical heads (event, injury, bodypart, source), macro F1. Let C be the set of classes present in the evaluation labels for that head. For each class c in C, F1_c is the harmonic mean of precision and recall, with F1_c = 0 where precision and recall are both zero:
> macro_f1 = ( 1 / |C| ) · sum_{c in C} F1_c
> The label set C is fixed to classes present in the evaluation labels. It is not the union of true and predicted labels, and it is not the training label space. Predicting a class that never occurs in evaluation costs only the precision of the classes it displaces. It does not enter the average as an additional zero.
> 3. Two incident heads (spread, multiple), binary F1 on the positive class. Each is scored as the F1 of the 1 label. The positive case is the minority, so a model that always predicts 0 scores zero on these heads.
> 4. Final score.
> final_score = ( kappa_severity
> + macro_f1_event
> + macro_f1_injury
> + macro_f1_bodypart
> + macro_f1_source
> + binary_f1_spread
> + binary_f1_multiple ) / 7
> Score range is 0 to 1. Higher is better. A perfect submission scores exactly 1.0.
> Reference points
> Strategy                                          Final score
> ──────────────────────────────────────────────────────────────
> Predict the training mode for every head                0.009
> Uniform random over the training label space            0.036
> Sample from the training class prior                    0.038
> Perfect oracle                                          1.000
> For orientation only: a plain word-count model with one linear classifier per head, no tuning, and neither age nor sex, lands well above the trivial baselines listed above and far below a perfect score, training in a few minutes on the allotted hardware. It is a floor, not a suggested method, and exact per-head figures are omitted so as not to anchor solutions to one representation. What matters is the shape of the difficulty: severity is the most tractable head; the long-tailed categorical heads (source, injury, bodypart) are harder because macro F1 weights their rare classes equally; and the two incident heads, spread and multiple, reward finding a small positive minority hidden in redacted prose.
> On severity, the mildest class is the hard one, for a reason that more data will not fix. A hand injury that led to admission and one that did not are described in the same words; whether it counted as hospitalization turned on facts the report never records. Some of that class is legible in the mechanism and some is simply noise.
> Compute
> Solutions run on 10 CPU cores, 62.5 GB RAM, no GPU, within a 90-minute wall-clock limit for training and inference combined. The training corpus is 91,127 incidents with a median narrative length of 424 characters, well under 100 MB of text, so memory is never the constraint.
> The reference baseline finishes in a few minutes, leaving most of the budget free. The envelope comfortably fits richer feature pipelines or a single fine-tune of a small pretrained text encoder; the short documents keep even an encoder-based approach within time. What does not fit is a large model ensemble or many-epoch training, so the budget rewards one well-chosen model over brute force. The strongest approach on this corpus is open; the baseline is only a floor.
> Submission Format
> Submit a CSV with the following columns:
> Column           Type   Description
> ────────────────────────────────────────────────────────────
> id         string Must match id from test.csv
> severity   int    Predicted severity code (primary worker)
> event      int    Predicted event code
> injury     int    Predicted injury code
> bodypart   int    Predicted body part code
> source     int    Predicted source code
> spread     int    1 if workers hurt at differing severities, else 0
> multiple   int    1 if more than one worker injured, else 0
> Example:
> id,severity,event,injury,bodypart,source,spread,multiple
> inc_8e084c98ef98f1e4,2,4,7,12,31,0,0
> inc_203113b20aa31215,1,7,10,4,15,1,1
> Requirements:
> Exactly one row per id in test.csv
> Include the header row
> All seven prediction columns present, integer valued, no nulls
> Rows are aligned by the id column. Order does not matter
> Additional columns are ignored
> A submission violating any requirement is rejected rather than scored. Class codes outside the training label space are legal and always wrong. They are scored, not rejected.
> Out of bounds
> Any outside collection of accident reports. Your codes must be predicted by a model from the released text, not recovered by matching evaluation rows against an external source to look up the original filing.
> Closed or hosted model APIs for generating predictions. Predictions must come from a model you run yourself, so results stay reproducible and tied to what your model learned.
> Web search or retrieval at inference.
> Hardcoding predictions. Manually assigning codes by inspecting evaluation items, rather than predicting them, is not permitted.
> TF-IDF features. Term-frequency-inverse-document-frequency weighting, in any form or under any library, is not an allowed representation. This includes TfidfVectorizer, TfidfTransformer, and hand-rolled equivalents. The task is meant to reward representations that capture meaning and structure rather than reweighted term counts; plain counts, hashed features, learned embeddings, and pretrained encoders are all fine.
> Notes on the data
> Narratives were reconstructed from a fixed-width 80-character storage format that splits words mid-token. The source CSV export strips trailing padding, so joining lines without re-padding corrupts approximately a quarter of all narratives into text such as working onthe roof. This is already corrected in the released data.
> Duplicate narratives, which the source system re-files under distinct identifiers, were removed before splitting. There are no exact-text duplicates within either split or across the boundary.
> The five per-worker heads are taken from each incident's primary worker, the one on the lowest injury line, whom the narrative consistently describes. Multi-worker incidents are kept in full rather than discarded: their additional workers are what make the spread and multiple heads answerable, even though the narrative rarely lets you attach a separate code tuple to each individual.
> Equipment brand names, serial numbers, and fall heights are mechanism, not disposition. They were deliberately preserved. They are signal.

Inspiration note: Useful because it turns text understanding into a grounded prediction task with careful leakage controls and CPU-friendly modeling options.

## Cycle-Consistency Auditing of Clinical-Trial Record Batches

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79rktrjc1cf0zrbr83g69nk98an1r8
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Cycle-Consistency Auditing of Clinical-Trial Record Batches
> Overview
> Clinical-trial information is often transferred between protocol-management systems, registries, internal databases, and analysis pipelines. During these transfers, treatment-group descriptions can become detached from their original population criteria or cyclically reassigned across several records.
> A batch may still look complete even though every population is linked to the wrong regimen, making this corruption difficult to detect through ordinary missing-value or schema checks.
> This is a batch-level clinical record-integrity task built from real treatment-group narratives. Each example contains three population-criteria documents and three presented regimen descriptions. The three source trials study the same anonymized treatment, so all regimens remain superficially plausible for the batch.
> Your task is to determine whether the complete three-record assignment is authentic or cyclically corrupted:
> Predict A when every population_i is paired with its authentic regimen_i from the same source trial.
> Predict B when all three regimens have been cyclically reassigned, so none of the displayed population–regimen links is authentic.
> This is not independent candidate selection. A solution must evaluate the joint one-to-one consistency of all three displayed links. The two corruption directions are both used, preventing a fixed positional shortcut.
> Why the Task Is Difficult
> Every batch is built from three different trials involving the same underlying treatment. When possible, the trials are matched by phase and selected for similar population language. Consequently, a corrupted regimen may still describe a credible dose, schedule, route, or procedure for the anonymized treatment.
> The three links must be considered together. Evidence that is weak or ambiguous for one pair may become useful when compared with the other two pairs and the one-to-one assignment constraint.
> The splits are constructed from connected components of treatments, source trials, population narratives, and regimen narratives. A treatment, source trial, or exact narrative appearing in validation or hidden testing does not appear in training.
> Models must therefore learn transferable cross-document consistency patterns instead of memorizing known trials or treatments.
> Source intervention names, trial identifiers, database identifiers, chemical structures, and treatment classification codes are excluded from model inputs. Candidate order, row order, and anonymized IDs carry no target information.
> This benchmark evaluates batch record integrity only. It does not evaluate treatment safety or effectiveness and must not be used for diagnosis, prescribing, participant recruitment, or other patient-level decisions.
> Data Preparation and Privacy
> The challenge files were produced from licensed clinical-trial treatment-group records. Only the text and labels required for this batch-integrity task are distributed to participants.
> Source intervention names are used only during preparation for grouping and masking. Source trial identifiers, database identifiers, chemical structures, classification codes, adverse-event targets, and event-frequency fields are excluded from every public challenge file.
> Dataset attribution and licensing information are maintained separately in the dataset’s License & Source section. They are intentionally not repeated in this challenge prompt because exposing a direct source location could allow hidden record associations to be reconstructed instead of learned from the provided training data.
> Evaluation
> Submissions are evaluated using chance-corrected balanced accuracy.
> Recall is calculated separately for class A and class B:
> balanced_accuracy = (recall_A + recall_B) / 2
> The reported score is:
> score = max(0, 2 * balanced_accuracy - 1)
> A constant or chance-level solution scores 0.0, while a perfect solution scores 1.0. Both classes receive equal weight even if their frequencies differ slightly.
> Dataset
> The public data directory contains four UTF-8 CSV files. Text fields may contain punctuation, numbers, clinical abbreviations, and line breaks, so CSV quoting must be preserved when reading the files.
> train.csv
> Contains 2,587 labeled training batches. Its columns are:
> id — string. Unique anonymized identifier in the format train_link_00000.
> population_1 — string. Masked eligibility and exclusion criteria for the first displayed record.
> regimen_1 — string. Regimen currently attached to population_1.
> population_2 — string. Masked eligibility and exclusion criteria for the second displayed record.
> regimen_2 — string. Regimen currently attached to population_2.
> population_3 — string. Masked eligibility and exclusion criteria for the third displayed record.
> regimen_3 — string. Regimen currently attached to population_3.
> label — string categorical target. A means all three displayed links are authentic; B means the three regimens have been cyclically reassigned.
> validation.csv
> Contains 555 labeled validation batches. Its columns are:
> id — string. Unique anonymized identifier in the format validation_link_00000.
> population_1, population_2, population_3 — strings containing the three masked population-criteria documents.
> regimen_1, regimen_2, regimen_3 — strings containing the three displayed regimen descriptions.
> label — string categorical target containing exactly A or B under the same definition used in train.csv.
> The treatments, source trials, population narratives, and regimen narratives in this file do not appear in train.csv.
> test.csv
> Contains 555 unlabeled hidden-test batches. Its columns are:
> id — string. Unique anonymized identifier in the format test_link_00000.
> population_1, population_2, population_3 — strings containing the three masked population-criteria documents.
> regimen_1, regimen_2, regimen_3 — strings containing the three displayed regimen descriptions.
> This file does not contain label. Participants must generate one prediction for every test ID.
> sample_submission.csv
> Contains 555 rows and demonstrates the required submission structure. Its columns are:
> id — string. A test identifier copied exactly from test.csv.
> prediction — string. Required prediction column containing exactly A or B.
> The sample uses a deterministic, randomly shuffled, approximately balanced mixture of dummy predictions: 278 A values and 277 B values. These placeholders are not model predictions and carry no information about the hidden labels.
> The row order does not need to match test.csv because the grader aligns predictions by id. Every test ID must nevertheless occur exactly once.
> Submission
> Submit a CSV with exactly two columns:
> id,prediction
> Example:
> id,prediction
> test_link_00000,A
> test_link_00001,B
> test_link_00002,A
> Submission Requirements
> The header must be exactly id,prediction.
> Include every test id exactly once.
> Do not include duplicate, missing, or unknown IDs.
> Every prediction must be exactly A or B.
> Lowercase values, probabilities, blank cells, and other values are invalid.
> Do not include an index or additional columns.
> Malformed submissions fail validation instead of receiving a partial score.
> Rules
> The only valid prediction signals are the six population_i and regimen_i text fields in the supplied public files.
> The following approaches are prohibited:
> Hardcoding predictions for particular test IDs or rows.
> Using row order, file layout, byte representation, or ID formatting as a prediction signal.
> Recovering masked treatment or trial identities through external registries, search engines, cached corpora, or another copy of the source records.
> Joining supplied narratives to an external registry or corpus to recover their original associations.
> Reconstructing intervention names, trial IDs, database IDs, chemical structures, or classification codes and using them as lookup keys.
> Using external linkage tables, private datasets, or manually created mappings for hidden test records.
> Calling an external inference API or accessing the internet during training or inference.
> Using private, role-gated, API-key-based, or non-reproducible models or artifacts.
> Publicly available pretrained language models may be used only when they are already available in the execution environment, run entirely within the CPU and time limits, and are genuinely trained or adapted using the supplied training batches.
> Classical models trained from the provided data are also allowed. Pretraining does not permit external retrieval or reconstruction of source records.
> This challenge tests whether a model can audit the global cycle consistency of three masked population–regimen links for previously unseen treatments and trials.
> A score obtained through source lookup, identity recovery, hidden metadata, or hardcoded mappings is invalid regardless of its numerical value

Inspiration note: Useful because it turns text understanding into a grounded prediction task with careful leakage controls and CPU-friendly modeling options.

## PolicyProbe: Adaptive Identification of Multi-Agent Operating Rules

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bxaxcx7cft7f1fx6k8d6nax89p0ev
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Many organizations use several specialized AI agents rather than relying on one general-purpose system. For example, one agent may handle account questions, another may process operational requests, another may review restricted cases, and another may serve as an escalation destination.
> The behavior of such a system depends on an operating rulebook. That rulebook determines which agent owns each capability, when a request should be transferred, which exceptions take priority, how multi-intent requests are handled, and what each agent should do when no specific rule applies.
> PolicyProbe models the task of testing a multi-agent system whose active operating rulebook is unknown.
> Each episode represents a self-contained simulated deployment. It contains four local agents, several possible natural-language rulebooks, and a collection of diagnostic user requests. One candidate rulebook is treated as the active rulebook during each grader execution.
> The candidate rulebooks are synthetic but are designed to represent realistic operational routing configurations. They describe capabilities, ownership assignments, conditional exceptions, escalation behavior, linked-request handling, and receiving-agent-specific fallbacks. Agent letters are randomized across episodes, so Agent A does not consistently represent the same department or role.
> The diagnostic requests represent controlled test interactions that an evaluator could send to the system before deployment or during a safety review. Each request is sent to one specified receiving agent and has an associated cost. The cost represents the time, operational effort, or evaluation resources required to perform that test.
> The participant does not directly interact with a live hidden system. Instead, the participant must predict the response that each candidate rulebook would produce for each available diagnostic request. These predictions are then used to construct an adaptive decision graph.
> At each probe node, the graph selects a diagnostic request. The observed action determines which branch is followed. Different observations may therefore lead to different follow-up requests.
> The goal is to identify the active candidate rulebook accurately while using as little of the available diagnostic budget as possible.
> Every episode provides:
> several candidate rulebooks written in natural language;
> a bank of diagnostic requests;
> the receiving agent for each request;
> a cost for each request;
> an observation space;
> a total diagnostic budget;
> a maximum graph depth;
> a maximum number of graph nodes; and
> a noise allowance of either 0 or 1.
> Each uncorrupted request produces one canonical action:
> answer_with_A
> answer_with_B
> answer_with_C
> answer_with_D
> delegate_to_A
> delegate_to_B
> delegate_to_C
> delegate_to_D
> refuse
> When the episode permits observation noise, one observed action may instead be changed to another valid action or to:
> observation_missing
> Participants must:
> use at least one learned machine-learning model to interpret the natural-language rulebooks, the diagnostic requests, or both;
> estimate how every candidate would respond to every available request;
> construct a valid adaptive decision graph;
> identify the active candidate using low-cost requests;
> remain within all graph, depth, and cost limits;
> account for possible observation corruption when noise is enabled; and
> assign a probability distribution over all candidates at every leaf.
> The grader executes the submitted graph separately for every candidate rulebook in the episode.
> Higher scores reward:
> correct candidate identification under uncorrupted observations;
> correct candidate identification when one observation is corrupted;
> strong separation between candidate pairs;
> low worst-case diagnostic cost;
> low average diagnostic cost; and
> well-calibrated candidate probabilities.
> Submission Environment
> Participants must submit a .ipynb notebook.
> The notebook will run with:
> 10 CPU cores;
> 62 GB RAM; and
> no GPU.
> The notebook must:
> load the public competition files;
> run the participant’s learned model;
> estimate candidate-by-probe actions;
> construct and validate decision graphs; and
> generate the final submission CSV.
> All processing performed on the test set must occur inside the submitted notebook.
> CPU-compatible models are recommended, including:
> classifiers;
> embedding models;
> natural-language-inference models;
> rerankers;
> sequence encoders;
> compact instruction-tuned models;
> distilled models; and
> quantized models.
> A large language model is not required.
> Canonical Observations
> Every uncorrupted probe produces exactly one of:
> answer_with_A
> answer_with_B
> answer_with_C
> answer_with_D
> delegate_to_A
> delegate_to_B
> delegate_to_C
> delegate_to_D
> refuse
> For episodes with observation noise, the grader may additionally produce:
> observation_missing
> Baseline
> sample_submission.csv contains a uniform graph with one leaf for every test episode.
> The baseline assigns the same probability to every candidate.
> A uniform probability distribution does not identify a candidate because the true candidate must have a probability strictly greater than every other candidate probability. Ties for the highest probability are counted as incorrect.
> A nontrivial graph or a non-uniform terminal prediction is therefore required to receive a positive identification score.
> Machine-Learning Requirement
> Every valid solution must use at least one learned model for an essential part of test-time semantic reasoning.
> The learned component must materially affect either:
> the estimated candidate-by-probe response matrix; or
> the submitted decision graph.
> A learned model may be used for:
> interpreting candidate rulebook text;
> interpreting diagnostic request text;
> matching capabilities to policy clauses;
> detecting request conditions;
> interpreting multi-intent requests;
> predicting candidate-by-probe actions; or
> estimating response probabilities.
> After learned semantic interpretation, deterministic planning methods may be used, including:
> dynamic programming;
> beam search;
> branch-and-bound;
> minimax search;
> integer programming;
> constraint programming;
> Monte Carlo tree search; and
> information-gain optimization.
> Pure keyword matching, regular expressions, fixed phrase rules, deterministic template parsing, or manually encoded capability dictionaries do not satisfy the requirement by themselves.
> Rulebook Semantics
> Each episode contains four local agents:
> Agent A
> Agent B
> Agent C
> Agent D
> The letters have no fixed operational meaning across episodes.
> Candidate rulebooks may define:
> capability ownership;
> standard routing behavior;
> condition-specific exceptions;
> precedence between rules;
> handling of requests containing two linked intents; and
> fallback behavior for each receiving agent.
> Standard Routing
> Every listed capability has one owner.
> For a standard request containing one intent:
> the owner answers directly; and
> any other receiving agent delegates to the owner.
> Conditions
> Supported request conditions include:
> ordinary;
> international;
> urgent;
> restricted or disputed; and
> after hours.
> A condition-specific instruction may override standard capability ownership, depending on the precedence rule stated in the candidate rulebook.
> Linked Requests
> A request may contain two connected intents.
> Rules for linked requests are applied before standard routing.
> A linked-request rule may:
> use the result associated with the first intent;
> use the result associated with the second intent;
> delegate to a specified agent; or
> refuse.
> Fallbacks
> When no capability rule or linked-request rule matches, the fallback instruction for the receiving agent is used.
> Execution under an uncorrupted candidate rulebook is deterministic.
> Observation Noise
> Every episode has an integer noise_budget equal to either 0 or 1.
> Noise Budget 0
> When noise_budget = 0, every observation is uncorrupted.
> Noise Budget 1
> When noise_budget = 1, at most one observation may be corrupted during an evaluated execution.
> The corrupted observation may be replaced by:
> another action listed in observation_space_json; or
> observation_missing.
> The replacement must differ from the uncorrupted action.
> Only one observation is changed. Any later observations remain uncorrupted.
> For every candidate, the grader evaluates:
> the fully uncorrupted execution; and
> every allowed execution in which one observation along that candidate’s uncorrupted path is replaced.
> A candidate receives adversarial identification credit only if every evaluated execution still identifies that candidate correctly.
> Public Files
> The package contains:
> public/
> ├── train.csv
> ├── test.csv
> └── sample_submission.csv
> Dataset Schema
> train.csv
> train.csv contains complete training episodes, including the uncorrupted candidate-by-probe response matrix.
> Columns:
> episode_id
> Type: string
> A unique identifier for the episode.
> candidate_policies_json
> Type: JSON-encoded string
> Contains a list of candidate rulebook objects. Every object contains a string candidate_id and a string policy_text.
> probe_bank_json
> Type: JSON-encoded string
> Contains a list of diagnostic request objects. Every object contains a string probe_id, a receiving-agent letter, a natural-language request, and a numeric probe cost.
> observation_space_json
> Type: JSON-encoded string
> Contains a list of canonical action strings that occur as uncorrupted observations in the episode.
> audit_budget
> Type: positive integer
> The maximum total probe cost allowed on any structural root-to-leaf path.
> maximum_depth
> Type: positive integer
> The maximum number of probe nodes allowed on any structural root-to-leaf path.
> maximum_nodes
> Type: positive integer
> The maximum total number of nodes allowed in the submitted graph. Probe nodes and leaf nodes both count toward this limit.
> noise_budget
> Type: integer
> The value is either 0 or 1.
> A value of 0 means observations are uncorrupted. A value of 1 means the grader evaluates every allowed single-observation corruption in addition to the uncorrupted execution.
> response_matrix_json
> Type: JSON-encoded string
> Contains the uncorrupted canonical action produced by every candidate-and-probe pair.
> test.csv
> test.csv contains the same public episode fields and uses the same data types as train.csv, except that response_matrix_json is omitted.
> Participants must estimate the missing candidate-by-probe responses.
> sample_submission.csv
> sample_submission.csv contains:
> episode_id
> Type: string
> Must match an episode identifier from test.csv.
> audit_tree_json
> Type: JSON-encoded string
> Contains the participant’s submitted graph for that episode.
> The sample file demonstrates formatting only and is not intended to provide a competitive solution.
> Candidate Rulebook Field
> candidate_policies_json decodes to a list such as:
> [
> {
> "candidate_id": "P123",
> "policy_text": "Operational policy candidate P123..."
> }
> ]
> Candidate order is randomized and has no predictive meaning.
> Probe Bank Field
> probe_bank_json decodes to a list such as:
> [
> {
> "probe_id": "Q123",
> "receiving_agent": "B",
> "request": "The user request...",
> "cost": 2
> }
> ]
> Field types:
> probe_id: string;
> receiving_agent: string containing A, B, C, or D;
> request: string;
> cost: positive integer.
> Probe identifiers are randomized and contain no semantic information.
> Observation Space Field
> observation_space_json is a JSON list of strings containing every uncorrupted canonical action that occurs in the episode.
> observation_missing is excluded because it is only introduced during noisy evaluation.
> Response Matrix Field
> response_matrix_json maps each candidate identifier and probe identifier to one canonical action.
> Example:
> {
> "P1": {
> "Q1": "answer_with_A",
> "Q2": "delegate_to_C"
> },
> "P2": {
> "Q1": "answer_with_A",
> "Q2": "answer_with_A"
> }
> }
> Suggested Pipeline
> 1. Interpret Candidate Rulebooks
> Use a learned model to identify or represent:
> capability owners;
> condition-specific exceptions;
> precedence rules;
> linked-request rules; and
> fallback actions.
> 2. Interpret Diagnostic Requests
> For each request, identify or represent:
> the relevant capability;
> a second capability when two intents are present;
> the applicable condition;
> the receiving agent;
> relevant rulebook clauses; and
> whether fallback behavior applies.
> 3. Predict Candidate Responses
> For every candidate and probe, predict one of:
> answer_with_<AGENT>
> delegate_to_<AGENT>
> refuse
> Predictions may be hard labels or probability distributions.
> 4. Construct the Decision Graph
> Use deterministic planning or search to:
> choose informative, low-cost probes;
> partition candidates by predicted observation;
> use branch-specific follow-up probes;
> respect the budget, depth, and node limits;
> introduce redundant evidence for noisy episodes;
> merge equivalent continuation states through shared subgraphs; and
> assign calibrated candidate probabilities at leaves.
> CPU Efficiency
> Useful optimizations include:
> encoding each candidate rulebook once;
> encoding each probe once;
> batching inference;
> caching repeated representations;
> predicting structured rulebook attributes before evaluating probes;
> pruning probes with low discriminative value;
> using quantized CPU-compatible models; and
> parallelizing independent episodes.
> Submission Format
> The notebook must generate a CSV containing exactly one row for each episode in test.csv.
> The CSV must contain exactly these columns:
> episode_id,audit_tree_json
> The value of audit_tree_json must be valid JSON after CSV decoding.
> Its top-level structure must be:
> {
> "root": "N0",
> "nodes": []
> }
> Missing episodes, duplicate episodes, malformed JSON, or invalid graphs receive zero for the affected episode.
> Complete Submission Example
> A minimal submission file containing two example episodes could appear as follows:
> episode_id,audit_tree_json
> E001,"{""root"":""N0"",""nodes"":[{""node_id"":""N0"",""node_type"":""leaf"",""candidate_probabilities"":{""P1"":0.7,""P2"":0.2,""P3"":0.1}}]}"
> E002,"{""root"":""N0"",""nodes"":[{""node_id"":""N0"",""node_type"":""probe"",""probe_id"":""Q8"",""branches"":{""answer_with_A"":""N1"",""default"":""N2""}},{""node_id"":""N1"",""node_type"":""leaf"",""candidate_probabilities"":{""P4"":0.8,""P5"":0.2}},{""node_id"":""N2"",""node_type"":""leaf"",""candidate_probabilities"":{""P4"":0.2,""P5"":0.8}}]}"
> The doubled quotation marks shown inside audit_tree_json are standard CSV escaping for quotation marks contained inside a field.
> Candidate identifiers and probe identifiers in a real submission must match the corresponding test episode.
> Probe Nodes
> A probe node must contain exactly:
> {
> "node_id": "N0",
> "node_type": "probe",
> "probe_id": "Q123",
> "branches": {
> "answer_with_A": "N1",
> "delegate_to_B": "N2",
> "observation_missing": "N3",
> "default": "N4"
> }
> }
> Requirements:
> probe_id must exist in the episode’s probe bank;
> every branch target must reference an existing node;
> valid branch labels are the nine uncorrupted actions, observation_missing, and __default__;
> exact branches take priority over __default__;
> every uncorrupted observation must be explicitly covered or handled by __default__;
> when noise_budget = 1, observation_missing must be explicitly covered or handled by __default__; and
> every structural branch counts during depth and cost validation.
> Using __default__ is the simplest way to guarantee complete observation coverage.
> Leaf Nodes
> A leaf node must contain exactly:
> {
> "node_id": "N7",
> "node_type": "leaf",
> "candidate_probabilities": {
> "P1": 0.10,
> "P2": 0.75,
> "P3": 0.15
> }
> }
> The probability object must:
> contain every candidate exactly once;
> contain no unknown candidate;
> use finite numeric values;
> use values between 0.0 and 1.0; and
> sum to 1.0 within 1e-6.
> The true candidate is identified only when its probability is strictly greater than every other candidate probability.
> Ties for the highest probability are incorrect.
> Graph Constraints
> Every graph must satisfy all of the following:
> exactly one valid root;
> unique node identifiers;
> valid branch references;
> no cycles;
> no unreachable nodes;
> no more than maximum_nodes total nodes;
> no more than maximum_depth probe nodes on any path;
> no path cost greater than audit_budget; and
> no repeated use of the same probe on one root-to-leaf path.
> Shared subgraphs are permitted.
> Probe nodes and leaf nodes both count toward the node limit.
> All structural branches, including __default__ and observation_missing, are considered during depth and cost validation.
> Evaluation
> The final score is the following weighted sum:
> final_score
> = 0.25 × clean_identification
> 0.25 × adversarial_identification
> 0.15 × pairwise_separation
> 0.15 × worst_case_efficiency
> 0.10 × expected_efficiency
> 0.10 × leaf_calibration
> The weights sum to 1.00.
> Each component is calculated independently and then multiplied by its stated weight.
> Clean Identification
> clean_identification is the fraction of candidates correctly identified under uncorrupted observations.
> A candidate is correctly identified when its probability at the reached leaf is strictly greater than every other candidate probability.
> Adversarial Identification
> For episodes with noise_budget = 1, a candidate is successful only if it is correctly identified under:
> the uncorrupted execution; and
> every permitted execution containing one corrupted observation along its uncorrupted path.
> For episodes with noise_budget = 0:
> adversarial_identification = clean_identification
> Pairwise Separation
> A pair of candidates is separated when:
> the first candidate is ranked above the second at the first candidate’s uncorrupted leaf; and
> the second candidate is ranked above the first at the second candidate’s uncorrupted leaf.
> Pairwise separation gives partial credit to graphs that distinguish many candidate pairs even when they do not perfectly identify every candidate.
> Worst-Case Efficiency
> For episodes with noise_budget = 0:
> quality = clean_identification
> For episodes with noise_budget = 1:
> quality
> = 0.40 × clean_identification
> 0.60 × adversarial_identification
> Worst-case efficiency is:
> worst_case_efficiency
> = quality × (1 - Cmax / audit_budget)
> Cmax is the maximum total probe cost among all evaluated executions for the episode.
> A graph that exceeds the budget is invalid rather than receiving a negative efficiency value.
> Expected Efficiency
> Expected efficiency is:
> expected_efficiency
> = quality × (1 - Cavg / audit_budget)
> Cavg is the mean total probe cost across all evaluated executions for the episode.
> Leaf Calibration
> For an episode with K candidates:
> brier = Σk (pk - yk)²
> Here:
> pk is the submitted probability for candidate k; and
> yk is 1 for the true candidate and 0 for every other candidate.
> The Brier score of a uniform probability distribution is:
> uniform_brier = 1 - 1/K
> Calibration skill is:
> calibration_skill
> = clip((uniform_brier - brier) / uniform_brier, 0, 1)
> The leaf_calibration component is the resulting calibration skill.
> A correct one-hot distribution scores 1.0.
> A uniform distribution scores 0.0.
> Invalid Graphs
> An episode receives zero if its graph contains an issue such as:
> malformed JSON;
> duplicate JSON keys;
> unexpected fields;
> an invalid root;
> a root with a parent;
> duplicate node identifiers;
> missing branch targets;
> cycles;
> unreachable nodes;
> unknown probes;
> invalid branch labels;
> incomplete observation coverage;
> more nodes than allowed;
> excessive structural depth;
> excessive structural path cost;
> repeated probes on one path;
> incorrect candidate keys;
> invalid probabilities; or
> probabilities that do not sum to one.
> The grader does not repair malformed or invalid graphs.
> Prohibited Methods
> Participants may not use:
> hidden response matrices;
> hidden structured rulebooks;
> generation seeds;
> manually obtained test labels; or
> external interaction with a hidden deployed system.
> Participants may not infer outputs from:
> episode ordering;
> candidate ordering;
> probe ordering;
> candidate identifiers;
> probe identifiers;
> filename patterns; or
> JSON serialization artifacts.
> Participants may not:
> modify probe text;
> create new probes;
> combine multiple probes into synthetic probes;
> exceed the diagnostic budget through external interactions;
> retrieve source records to recover hidden construction information; or
> use unreleased competition information.
> Only probes from the corresponding episode’s probe bank may appear in the submitted graph.
> Intended Challenge
> PolicyProbe combines:
> learned understanding of natural-language operating rules;
> learned interpretation of diagnostic requests;
> candidate-specific action prediction;
> adaptive decision planning;
> constrained graph construction; and
> robust experimental design under possible observation corruption.
> The main semantic task is estimating how every candidate rulebook responds to every available diagnostic request.
> The planning task is using those estimates to construct a valid adaptive graph that identifies candidates accurately, uses inexpensive requests, produces calibrated probabilities, and remains reliable when one observation is corrupted.

Inspiration note: Useful because it turns text understanding into a grounded prediction task with careful leakage controls and CPU-friendly modeling options.

## Six-Statement Intruder Localization and Consensus Restoration

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7a4bp0rv127gedcxhehq24h18ahzrp
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Six-Statement Intruder Localization and Consensus Restoration
> Overview
> Each case contains a short anonymized scientific prompt and six anonymized support statements. Five of the six statements belong to the same underlying case. One statement has been cross-attached from a different case while preserving similar technical style, entity aliases, measurement language, and outcome wording. The task is to identify the cross-attached statement and recover the original consensus label that would be supported by the five consistent statements.
> This is a local provenance recovery problem over a compact statement bundle. The public text has been transformed with stable lexical aliases, numeric placeholders, hashed row identifiers, and shuffled row order. These transformations remove source-specific surface strings while keeping repeated terminology and within-case consistency signals. Solvers must reason over how the six statements fit together rather than relying on exact phrase lookup or source memorization.
> Evaluation
> Submissions are scored using Bundle Recovery Score. Higher is better. Scores are bounded between 0 and 1.
> For each row, the predicted intruder slot is the largest probability among:
> p_s0, p_s1, p_s2, p_s3, p_s4, p_s5
> The predicted consensus label is the largest probability among:
> p_yes, p_no, p_maybe
> The final score is:
> score =
> 0.45 * slot_macro_f1
> + 0.35 * label_macro_f1
> + 0.15 * joint_accuracy
> + 0.05 * calibration_score
> Metric components:
> slot_macro_f1: standard macro-F1 over the six intruder-slot classes 0, 1, 2, 3, 4, and 5.
> label_macro_f1: standard macro-F1 over the three consensus classes yes, no, and maybe.
> joint_accuracy: the fraction of rows where both the intruder slot and consensus label are correct.
> calibration_score: 1 - 0.5 * (slot_half_brier + label_half_brier), clipped to [0, 1].
> For each probability group, half-Brier is 0.5 * sum((p_k - y_k)^2) averaged over rows, where y_k is the one-hot target. This bounds each Brier term between 0 and 1, so a worst-case calibrated submission maps to 0 without premature clipping. The grader normalizes submitted probability groups before scoring, so each row is evaluated as a six-way slot distribution and a three-way label distribution.
> Dataset
> The prepared public dataset contains four CSV files:
> train.csv: labeled training rows with anonymized prompts, six anonymized statements, an intruder-slot label, and a consensus label.
> test.csv: held-out rows with the same public input columns as train.csv, but without labels.
> sample_submission.csv: example submission file with the exact required prediction columns.
> answers.csv: hidden grading labels used only by the platform grader.
> train.csv
> id: string obfuscated row identifier.
> question: string anonymized scientific prompt.
> sentence_0: string anonymized candidate statement in slot 0.
> sentence_1: string anonymized candidate statement in slot 1.
> sentence_2: string anonymized candidate statement in slot 2.
> sentence_3: string anonymized candidate statement in slot 3.
> sentence_4: string anonymized candidate statement in slot 4.
> sentence_5: string anonymized candidate statement in slot 5.
> suspect_idx: integer label from 0 to 5; this is the cross-attached statement slot.
> answer: string consensus label. One of yes, no, or maybe.
> test.csv
> id: string obfuscated row identifier.
> question: string anonymized scientific prompt.
> sentence_0: string anonymized candidate statement in slot 0.
> sentence_1: string anonymized candidate statement in slot 1.
> sentence_2: string anonymized candidate statement in slot 2.
> sentence_3: string anonymized candidate statement in slot 3.
> sentence_4: string anonymized candidate statement in slot 4.
> sentence_5: string anonymized candidate statement in slot 5.
> sample_submission.csv
> id: string row identifier from test.csv.
> p_s0: float probability that sentence_0 is the cross-attached statement.
> p_s1: float probability that sentence_1 is the cross-attached statement.
> p_s2: float probability that sentence_2 is the cross-attached statement.
> p_s3: float probability that sentence_3 is the cross-attached statement.
> p_s4: float probability that sentence_4 is the cross-attached statement.
> p_s5: float probability that sentence_5 is the cross-attached statement.
> p_yes: float probability that the restored consensus label is yes.
> p_no: float probability that the restored consensus label is no.
> p_maybe: float probability that the restored consensus label is maybe.
> Submission
> Submit a CSV file with exactly 1,928 prediction rows plus a header.
> Required columns:
> id,p_s0,p_s1,p_s2,p_s3,p_s4,p_s5,p_yes,p_no,p_maybe
> Example:
> id,p_s0,p_s1,p_s2,p_s3,p_s4,p_s5,p_yes,p_no,p_maybe
> test_0e1836a2fdc861dd,0.08,0.13,0.51,0.09,0.11,0.08,0.72,0.15,0.13
> test_3a190edc77c6eb25,0.19,0.16,0.12,0.10,0.34,0.09,0.21,0.62,0.17
> Requirements:
> Every id from test.csv must appear exactly once.
> All required probability columns must be present.
> All probability values must be finite and non-negative.
> The six slot probabilities must have positive total mass for every row.
> The three consensus probabilities must have positive total mass for every row.
> File format must be .csv with the exact column names shown above.
> Rules
> Do not try to recover hidden labels or source identifiers.
> Do not search public text on the web to identify source records.
> Do not hardcode test-row labels or use any files outside the provided public dataset.

Inspiration note: Useful because it turns text understanding into a grounded prediction task with careful leakage controls and CPU-friendly modeling options.

## Conserved Device-Code Allocation Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx711xq0vxy30sk54t3yknzym58apa72
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: medical
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Quality-control teams sometimes receive a batch of closely related incident reports whose categorical annotations have become detached from their source rows during export or merging. The codes are still present and none is missing, but their row assignments must be reconstructed.
> Each challenge case contains three real medical-device incident narratives from the same manufacturer, product family, and event class. The three reports originally carried three different, naturally recorded device-problem codes. You receive the three narratives and the conserved pool of those three codes, including their official descriptions, but not the original row-to-code links.
> Assign every candidate code to exactly one report. The task is solved jointly: using a code for one report removes it from consideration for the other two. This conservation constraint makes the benchmark a three-way structured allocation problem rather than three independent text classifications.
> Task
> For every case_id, predict assignment_sequence as three space-separated code tokens:
> DPC_for_REPORT_A DPC_for_REPORT_B DPC_for_REPORT_C
> Every candidate code shown in that row must appear exactly once in the prediction.
> Dataset
> public/train.csv contains labeled three-report allocation cases.
> public/test.csv contains the same inputs without assignment_sequence.
> public/sample_submission.csv shows valid candidate-preserving permutations.
> private/answers.csv contains hidden assignments and is available only to the grader.
> Columns
> case_id string): opaque identifier for one three-report allocation case.
> report_a string): transformed narrative for the first report.
> report_b string): transformed narrative for the second report.
> report_c string): transformed narrative for the third report.
> candidate_code_catalog string): the conserved pool of three DPC_#### tokens and their official descriptions. Display order has no relationship to report order.
> assignment_sequence string, train only): the three code tokens aligned with reports A, B, and C.
> The narratives preserve source-view markers, order, technical context, and repeated-token structure. Source keys, organization and product identifiers, numbers, dates, exact problem-description phrases, highly label-specific singleton cues, and low-frequency source-specific words are removed or transformed. Manufacturer groups are disjoint between training and test.
> Evaluation
> Scores range from 0 to 1, where higher is better.
> For each row:
> FieldAccuracy = number of correctly assigned reports / 3
> ExactAllocation = 1 if all three assignments are correct, otherwise 0
> row_score = 0.65  *FieldAccuracy + 0.35*  ExactAllocation
> Score = mean(row_score)
> A fully deranged assignment can score 0; the exact correct allocation scores 1.
> Submission Format
> Submit a UTF-8 CSV with exactly these columns:
> case_id,assignment_sequence
> CCA_0123456789abcdef,DPC_1069 DPC_1546 DPC_2907
> CCA_fedcba9876543210,DPC_1384 DPC_1069 DPC_4001
> Requirements:
> Include exactly one row for every test case_id, without missing, duplicate, or unknown IDs.
> Provide exactly three distinct DPC_#### tokens per row.
> The prediction must be a permutation of the three tokens in that row's candidate_code_catalog.
> Token one is assigned to report_a, token two to report_b, and token three to report_c.
> Write the output to the exact submission path supplied by the platform.
> Allowed
> CPU-only pair scorers, structured assignment models, compact neural text models, and global permutation decoders trained using the public files.
> Jointly compare all three reports and all three candidate descriptions.
> Use at most 10 CPU cores, 62 GB RAM, and 1.5 hours end-to-end.
> Prohibited
> No GPU or accelerator computation.
> No external incident archives, device databases, source-record retrieval, web search, or hosted inference APIs.
> Do not reconstruct raw report keys, manufacturer identities, product identifiers, or exact source records.
> Do not use private answers, grader internals, test IDs, file order, filenames, hashes, or hard-coded test predictions.
> This benchmark is for research evaluation only and must not be used for medical, regulatory, or device-safety decisions.

Inspiration note: Useful because it turns text understanding into a grounded prediction task with careful leakage controls and CPU-friendly modeling options.
## Regulatory Cross-Reference Target Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx774wcd4khd0w6cp7x6jqwzfh8avwgn
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, Dataset source is visible after the challenge closes.
- Best/top context: Be the first to climb the leaderboard!

### Full Challenge Description

> Overview
> In this challenge, you must identify the regulatory passage that is the hidden target of a cross-reference.
> Each row contains one anonymized query paragraph and four anonymized candidate regulatory passages. The query paragraph originally cited another section, but the visible section number has been replaced before public release. Exactly one of the four candidates is the passage that the hidden reference points to.
> The data comes from real federal regulatory text. During preparation, raw section numbers, headings, words, punctuation, and source ordering information are hidden. Query words are converted into stable opaque QW_... tokens, candidate-passage words are converted into separate stable opaque CW_... tokens, punctuation is converted into P_... tokens, and numbers are converted into coarse number bands. This preserves useful language structure while preventing direct lookup of the original regulation text.
> This is a CPU-compatible NLP retrieval and alignment task. The decoy candidates are selected from related regulatory material and are overlap-matched before anonymization whenever possible. Query tokens and candidate tokens use separate opaque namespaces, so exact shared-token overlap cannot directly identify the answer. A good solution must learn from public labels which candidate passage is functionally connected to the hidden reference.
> Evaluation
> Submissions are scored using exact-choice accuracy. Higher is better.
> For each row, target_choice is correct if it matches the candidate label for the true cross-reference target. A perfect submission scores 1.0. Randomly choosing among four candidates should score near 0.25.
> Evaluation formula:
> score = mean(target_choice_pred == target_choice_true)
> Dataset Files
> The prepared dataset contains these files:
> public/train.csv - Labeled training rows.
> public/test.csv - Unlabeled test rows.
> public/sample_submission.csv - Example submission format with placeholder predictions.
> private/answers.csv - Hidden answer key used by the grader.
> Each row is one hidden-reference recovery problem with one query paragraph and four candidate target passages.
> Columns
> id (string): Unique anonymized row identifier.
> query_tokens (string): Opaque token sequence for the paragraph containing the hidden cross-reference.
> candidate_a_tokens (string): Opaque token sequence for candidate passage a.
> candidate_b_tokens (string): Opaque token sequence for candidate passage b.
> candidate_c_tokens (string): Opaque token sequence for candidate passage c.
> candidate_d_tokens (string): Opaque token sequence for candidate passage d.
> candidate_profiles (string): Compact public summary of candidate length and simple structural hints.
> target_choice (string): Training label only. Correct candidate label for the hidden reference.
> The test file contains all public columns except target_choice.
> Encoded Text Format
> Query words appear as stable opaque QW_... codes. Candidate-passage words appear as separate stable opaque CW_... codes. The same original query-side word maps consistently to the same query token, and the same original candidate-side word maps consistently to the same candidate token, but query and candidate vocabularies are intentionally separated.
> Punctuation appears as P_... codes. Numbers are replaced by coarse bands such as QUERY_NUM_SMALL, CANDIDATE_NUM_MEDIUM, or CANDIDATE_NUM_LARGE.
> Example token sequence:
> QW_2a4c19d8bf QW_7bb830c3d0 P_3a2f91ee QW_c9a07e2b10 QUERY_NUM_MEDIUM
> Submission Format
> Submit a CSV file named submission.csv. It must contain exactly two columns in this exact order:
> id (string): The exact row id from public/test.csv.
> target_choice (string): The selected candidate label. Valid values are a, b, c, or d.
> Example submission:
> id,target_choice xref_03f48289e58a1d91,a xref_09c8df773a671bf0,d xref_14a4bc68e33e4e12,b
> Requirements:
> Include exactly one row for every row in public/test.csv.
> Do not include duplicate ids.
> Use only a, b, c, or d in target_choice.
> Preserve the exact column order: id,target_choice.
> Write the file to ./working/submission.csv.
> What Not To Use
> Do not use online lookup, regulatory section-number search, external copies of the source regulations, or any source URL reconstruction to identify hidden answers.
> Do not attempt to reverse-map opaque tokens back to original regulatory words, section numbers, headings, or passages.
> Do not use raw token overlap, bag-of-words similarity, or TF-IDF similarity as the final prediction mechanism. These methods may be used only for preprocessing, diagnostics, or intermediate features inside a learned model trained on the public labels.
> Do not hardcode answers from leaderboard probing, cached private labels, or any external answer list.
> Do not assume candidate order has meaning. Candidate order is shuffled independently for every row.

Inspiration note: Useful as inspiration for sequence assembly/reconstruction rather than flat classification.
## Paragraph Intruder Detection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fbsv43yttx8yq49bp9wr8b18apk4e
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering, text, Dataset source is visible after the challenge closes.
- Best/top context: Beat indra_me's score of 0.332!

### Full Challenge Description

> Paragraph Intruder Detection
> Overview
> Each item gives four English prose paragraphs as a JSON list in narrative order. Exactly three paragraphs are consecutive paragraphs from the same public-domain book. Exactly one paragraph is an intruder: a length-matched paragraph taken from elsewhere in the same book (a distant passage, not adjacent) or, when needed, from another book by the same author.
> Your job: output the index of the intruder paragraph (0, 1, 2, or 3).
> This is hard local-coherence / intrusion detection. Cross-book, cross-author swaps are not used in this release, because those break narrative identity too obviously for strong language models. It is not paragraph-boundary segmentation, not sentence-boundary detection, not paragraph reordering, not phonetic span extraction, and not time-to-event ranking.
> Labeled pairs are in train.csv. Unlabeled items are in test.csv. Use only files under ./dataset/public/.
> Why this is hard: the intruder matches authorial style and often the same work, so character names, dialect, and topic words may still fit. Length matching removes naive length cues. Test items use held-out host books. A uniform random guess scores about 0.25.
> Index rules
> parts_json is a JSON array of exactly four non-empty paragraph strings.
> Positions are 0-based: first paragraph is index 0.
> Exactly one index is the intruder.
> Output intruder_index as a single character string: 0 or 1 or 2 or 3.
> Evaluation
> Scored by exact index-match accuracy in [0, 1]. Higher is better.
> A prediction matches if, after stripping whitespace, it equals the gold intruder_index. The score is the mean over test items.
> Pseudocode:
> def evaluate(y_true_index, y_pred_index):
> matches = [a.strip() == b.strip() for a, b in zip(y_true_index, y_pred_index)]
> return sum(matches) / len(matches)
> Uniform random among four indices scores about 0.25. A real solution should beat that clearly.
> Dataset
> Files in ./dataset/public/:
> train.csv — labeled training data (6,500 rows)
> test.csv — unlabeled test data (1,200 rows)
> sample_submission.csv — example submission format
> metadata.json — short optional task summary
> Column descriptions:
> item_id (string) — present only in test.csv and in the submission file; not present in train.csv
> parts_json (string) — JSON array of four paragraphs; present in train.csv and test.csv
> intruder_index (string) — gold index 0/1/2/3; present in train.csv only; required in submission
> train.csv columns: parts_json, intruder_index
> test.csv columns: item_id, parts_json
> sample_submission.csv columns: item_id, intruder_index
> Source note: built from a curated multi-book corpus of US public-domain English literary prose. Intruders are same-book distant passages or same-author passages. Upstream headers/footers were stripped. Exact book titles, catalog IDs, and download URLs are intentionally not listed in this public description (anti-scraping). Reviewers receive the private title/catalog list separately. Use only files under ./dataset/public/.
> Submission Format
> Write predictions to ./working/submission.csv as a CSV with a header row and exactly these columns:
> item_id (string) — must match test.csv one-to-one, same row order, no duplicates
> intruder_index (string) — predicted 0, 1, 2, or 3
> Requirements:
> Exactly 1,200 data rows (one per test item), plus the header row
> No null or empty values
> intruder_index must be one of: 0, 1, 2, 3
> Example (format only):
> item_id,intruder_index
> PID_ab12cd34ef56,2
> PID_99aa88bb77cc,0
> What not to use
> External datasets, APIs, model downloads, or web scraping
> Test labels or any file under ./dataset/private/
> Hardcoded item_id-to-index lookup tables
> Packages beyond what the standard Kaggle Python Docker image preinstalls

Inspiration note: Useful as inspiration for corrupted-clue recovery where the model must identify and repair unreliable evidence.
## Contaminated Manuscript Identification

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx788b3g4bwtehypyapajg45rx8axdeg
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, Dataset source is visible after the challenge closes.
- Best/top context: Beat krishna_ram's score of 0.629!

### Full Challenge Description

> Contaminated Manuscript Identification
> Overview
> This is a natural language processing task in computational philology, the study of how the
> wording of written works changes as they are copied by hand. You are given collections of
> manuscripts. Each manuscript is a short text, written as a sequence of word readings at the same
> fixed set of positions, so a manuscript is a line of natural-language tokens and two manuscripts
> can be read and compared word by word.
> When a work survives only through hand copies, the copies form a family: each scribe worked from
> one exemplar, reproducing its wording except for the occasional changed word. Some scribes,
> though, worked from more than one source at once, so their text is a blend, mostly one line of
> the wording but with stretches pulled in from an unrelated line. Reading the manuscripts and
> telling the single-source copies apart from these blended, mixed-source ones is the task.
> You are given only the manuscripts, as text. The family relationships and the copying are all
> hidden; the wording is the only evidence. For each tradition you report the set of mixed-source
> manuscripts. The tell is linguistic, not statistical bulk: not that a manuscript's wording
> differs from the others (ordinary copying does that), and not that it agrees with many (a popular
> exemplar does that too), but that the words where it departs from its closest relative line up,
> suspiciously, with one specific distant manuscript. Some manuscripts blend in so few words that
> their wording stays within the range of ordinary copying and cannot be told apart; those cases
> are not recoverable, and a good solution accepts that rather than guessing.
> Relation to prior work
> Computational philology and stemmatology reconstruct manuscript family trees from textual
> variants using parsimony and distance methods (for example the artificial benchmark study of
> Roos and Heikkila, Digital Scholarship in the Humanities 2009) and, more recently, learned
> placement of manuscripts on a tree. Mixed-source copying, where a scribe draws on more than one
> exemplar (called contamination in that literature, and studied via exemplar-change tests such as
> Windram, Howe and Spencer 2005), is repeatedly singled out as an open problem the standard
> tree-shaped methods are not built to handle. Existing work treats it as unsupervised structure
> discovery on a single real tradition. This challenge instead poses it as a large-scale
> supervised text benchmark: thousands of traditions with known answers, a held-out test split,
> and a set-F1 harness over the mixed-source manuscripts. The target is a set of documents, not a
> tree, and the signal is cross-line wording agreement rather than overall similarity, which is
> what makes it a distinct framing rather than a reskin of tree reconstruction.
> Evaluation
> For each tradition the set of manuscripts you name is compared with the true set by set F1,
> and the result is averaged over all traditions.
> def set_f1(pred_ids, gold_ids):
> p, g = set(pred_ids), set(gold_ids)
> if not p and not g:
> return 1.0
> if not p or not g:
> return 0.0
> inter = len(p & g)
> if inter == 0:
> return 0.0
> precision, recall = inter / len(p), inter / len(g)
> return 2.0 * precision * recall / (precision + recall)
> def evaluate(rows):
> return sum(set_f1(p, g) for p, g in rows) / len(rows)
> Scores run from 0.0 to 1.0. About one tradition in seven is clean, with no contamination, so
> naming nothing there is correct; a submission that names nothing anywhere scores about 0.15.
> Naming every manuscript scores about 0.23. A perfect score is not attainable, because lightly
> contaminated copies are indistinguishable from honest ones. A strong solution is expected to
> land around 0.45 to 0.55.
> Dataset
> Each tradition is generated: a hidden family of copies, copying with occasional word changes,
> and some manuscripts blended from a second line. The word readings are drawn from a real
> public-domain English text, so the manuscripts read as ordinary word sequences. The families,
> the copying and the mixed-source blending are all created for this challenge and appear in no
> public source.
> Files available in public/:
> train.csv -- 10,000 labelled traditions
> id (int): Row index, 0-based
> manuscripts (string): A JSON list of manuscripts. Each manuscript is a space-separated string of readings, one reading per locus. Every manuscript in a tradition has the same number of loci.
> n_mss (int): Number of manuscripts in the tradition, between 12 and 20
> contaminated (string): Pipe-separated indices (into the manuscripts list) of the contaminated manuscripts, for example 3|9. Empty when the tradition is clean.
> test.csv -- 4,000 unlabelled traditions
> id (int): Row index, 0-based
> manuscripts (string): A JSON list of manuscripts, as above
> n_mss (int): Number of manuscripts in the tradition
> sample_submission.csv -- A correctly formatted placeholder
> id (int): Row index from test.csv
> contaminated (string): Empty placeholder
> Manuscript order within a tradition is shuffled and carries no information about the tree.
> Load the manuscripts with json.loads, then split each on spaces to get its per-locus
> readings.
> Submission
> Submit a CSV with exactly two columns:
> id (int): Row index from test.csv, 0 to 3,999
> contaminated (string): Pipe-separated indices of the manuscripts you judge contaminated, for example 3|9, or an empty string if you judge the tradition clean
> Example:
> id,contaminated
> 0,3|9
> 1,
> 2,5|11|14
> 3,7
> Requirements:
> Exactly 4,000 rows, one per test tradition
> A header row
> Column names exactly id and contaminated
> Indices are 0-based into that tradition's manuscript list, with no repeats within a cell
> An empty cell is valid and is the correct answer for a clean tradition
> What not to use
> Do not try to identify the public-domain text the reading vocabulary was drawn from and look
> anything up in it. It supplies words only; the trees, the copying and the contamination are
> generated for this challenge, so there is no external key to find.
> Do not use any external API or web lookup at inference time. Every tradition is
> self-contained: the manuscripts in front of you are all the evidence there is.
> Do not attempt to obtain or reconstruct the private answer key.
> Your solution must run on CPU alone, within the platform time limit.

Inspiration note: Useful for dynamic evidence evaluation rather than static answer grading.

## Process Ambiguity Contour Labeling

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78vkm6612zyq3cvdgxag9kys8b4zy9
- DOMAIN exactly as displayed: NLP
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
> Predict one CLEAR or AMBIGUOUS token for every statement position in each variable-length process-language window. The ordered output is an ambiguity contour: it shows where unclear language opens, persists, and closes as a reader moves through a document.
> This is a Natural Language Processing sequence-labeling task, not independent row classification. Each example contains three to seven consecutive statements represented as privacy-protected token sequences. A model must interpret linguistic evidence across the ordered window, including references, modality, temporal language, conditions, negation, and vague specifications. Evaluation documents are entirely absent from training.
> All source statements are real human-written operational prose and all targets come from human ambiguity annotations. The privacy transform retains coarse linguistic evidence while withholding confidential wording and preventing repeated text from becoming a lookup key.
> The practical use is document review triage. A correct contour lets a review system open a clarification thread when ambiguity appears, keep it active across consecutive unclear statements, and close it when the language becomes operationally clear.
> Dataset
> File descriptions
> train.csv -- 162 labeled process-language windows from 56 documents.
> test.csv -- 41 unlabeled windows from 15 held-out documents.
> sample_submission.csv -- Deterministic random valid ambiguity contours in the required format.
> Column descriptions
> id (string) -- Unique 16-character hexadecimal window identifier.
> document_id (string) -- Opaque document identifier for grouped validation; present only in train.csv.
> initial_scope (string) -- Ambiguity state immediately before the first sequence position: CLEAR or AMBIGUOUS.
> step_count (integer) -- Number of statement positions in the window, from 3 through 7.
> text_sequence (string) -- Ordered privacy signatures separated by || . Each signature contains exactly 18 space-separated tokens.
> scope_sequence (string) -- Ordered labels using CLEAR and AMBIGUOUS, one per statement position; present only in train.csv and required in submissions.
> Signature tokens have these meanings:
> length_short, length_medium, or length_long -- A randomized coarse sentence-length band.
> cue_temporal, cue_conditional, cue_reference, cue_vague, cue_negation, and cue_modal -- Noisy indicators for broad linguistic cue families.
> number -- A retained numeric-token indicator.
> lex_00 through lex_23 -- Occurrence-keyed lexical buckets that do not expose source words.
> || -- Boundary between consecutive statement signatures.
> Concrete three-step test example:
> id: 0ebd577434e2d112
> initial_scope: CLEAR
> step_count: 3
> text_sequence:
> length_short lex_15 cue_negation lex_23 lex_05 lex_16 cue_modal lex_16 lex_03 lex_07 cue_temporal lex_09 cue_conditional lex_08 cue_vague lex_23 lex_17 lex_02 ||
> length_long lex_15 lex_09 cue_temporal lex_16 lex_04 lex_23 lex_03 lex_01 cue_reference lex_08 lex_15 lex_12 lex_04 cue_modal lex_21 lex_18 lex_16 ||
> length_medium lex_18 lex_16 lex_00 cue_reference lex_08 lex_16 lex_00 cue_conditional lex_16 lex_19 lex_07 lex_05 lex_21 lex_16 lex_12 lex_03 cue_modal
> The output for this row must contain exactly three labels, preserving the same order.
> Evaluation
> Submissions are scored with Scope Trajectory Fidelity (STF). Higher is better; the score ranges from 0 to 1.
> STF combines three sequence-quality components:
> state_macro_f1 -- Macro F1 over CLEAR and AMBIGUOUS across all statement positions. Equal class weighting prevents the frequent clear state from dominating.
> transition_macro_f1 -- Macro F1 over four handoff events derived from adjacent states: stable_clear, scope_opens, scope_persists, and scope_closes. The first event uses initial_scope as its preceding state.
> document_fidelity -- Documents receive equal weight. Within each document, the grader averages squared row-level token accuracy. Squaring rewards coherent, mostly correct contours more than the same number of correct labels scattered across weak windows.
> score = (
> 0.55 * state_macro_f1
> + 0.30 * transition_macro_f1
> + 0.15 * document_fidelity
> )
> Each component lies in [0, 1], so STF also lies in [0, 1]. A perfect set of contours scores 1.
> Submission
> Submit one ordered ambiguity contour for every row in test.csv.
> id (string) -- Exact identifier from test.csv.
> scope_sequence (string) -- Space-separated sequence containing only CLEAR and AMBIGUOUS.
> Example:
> id,scope_sequence
> 0ebd577434e2d112,AMBIGUOUS CLEAR CLEAR
> 0071cfe7a9a900c1,CLEAR CLEAR AMBIGUOUS AMBIGUOUS CLEAR
> Requirements
> The file must contain exactly 41 data rows, one for every test ID.
> Columns must be exactly id,scope_sequence in that order.
> IDs must be unique and match test.csv exactly.
> Every sequence token must be CLEAR or AMBIGUOUS.
> Each output sequence must contain exactly step_count labels for that test row.
> Sequences must contain between 3 and 7 labels.
> Missing values and empty sequences are invalid.
> File format: UTF-8 CSV.
> What Not To Use
> Do not reverse-map privacy signatures to source sentences, document identities, or external annotation rows.
> Do not recover test contours from publication supplements, mirrors, cached annotations, or source-position lookup.
> Do not hardcode outputs by test ID, row order, signature fingerprint, or a recovered privacy key.
> A fixed hand-written contour rule without a model trained on train.csv is not a valid solution.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Redacted Coreference Resolution in Long-Form Prose

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79b123th9grftmf2bfy113w18ag4vm
- DOMAIN exactly as displayed: NLP
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
> A passage of narrative prose refers to the same people, places, and things over and over: by name, by a descriptive phrase, and above all by pronouns. Recovering which expressions point to the same underlying entity is the task of coreference resolution, and it is what lets a reader follow who did what to whom across a paragraph.
> In this challenge each item is a passage with a set of marked mentions (the spans of text that refer to entities). To keep the task about reasoning rather than string matching, every proper name has been replaced by the placeholder token [NAME], so two mentions that happen to share a name cannot be linked by surface form alone: you must use pronoun agreement, grammatical role, discourse recency, and the surrounding wording to decide what refers to what.
> For every marked mention you decide two things. First, its antecedent: point to an earlier marked mention in the same passage that refers to the same entity, or answer NEW if this is the first mention of its entity in the passage. Second, its entity_type: the kind of entity the mention refers to. Because entity_type is a property of the referent, a pronoun's type must be inferred from what it stands for, not from the pronoun's own surface.
> The passages come from long-form literary prose written by many different authors across two centuries. What makes the task hard is genuine ambiguity: when several people have been introduced and the text says that he took it from her, careful human annotators can and do disagree about the exact antecedent. A strong solution recovers most of the structure; none recovers all of it.
> Task
> Mentions within a passage are given in reading order, and a mention's antecedent, when it has one, is always an earlier mention of the same passage. The first mention of each entity in a passage has antecedent NEW. Predict, for every mention, its antecedent (an earlier mention id, or NEW) and its entity_type.
> Evaluation
> Your antecedent predictions induce a clustering of the mentions in each passage: mentions joined directly or transitively by predicted antecedent links form one predicted entity, and a mention that is answered NEW and that no later mention links to is a singleton. This predicted clustering is compared to the true clustering with the standard coreference score.
> The final score is in [0, 1], higher is better, and combines a linking term with a typing term:
> score = 0.70 x link_component + 0.30 x type_score
> The linking term uses the cluster-level coreference metric, so it rewards recovering whole entities and penalizes both merging two distinct entities and splitting one entity apart. Linking every mention to the nearest same-type mention, or leaving everything unlinked, both score far below a model that recovers the true entities.
> passage_link -- the average of the MUC, B-cubed, and CEAFe F1 scores (the CoNLL average) between the predicted and true clustering of that passage's mentions.
> link_component -- the mean passage link score combined with a worst-period term so a solution cannot lean on one era of writing: link_component = 0.70 x mean(passage_link) + 0.30 x (lowest per-period mean passage_link). A period is scored only if it has at least fifteen test passages.
> type_score -- the macro F1 of the predicted entity_type over all test mentions, averaged over the full seven-type vocabulary so that spurious type predictions are penalized and the rare types count as much as person.
> The placeholder sample_submission.csv (every mention NEW, every type PER) scores about 0.24. A competent classical pipeline -- a type classifier plus a trained mention-pair antecedent ranker -- scores about 0.61. The maximum of 1.0 is not reachable in practice because of the irreducible ambiguity described above.
> Dataset
> All files are under ./dataset/public/, one row per mention.
> train.csv -- about 8100 mentions across 298 labeled passages.
> test.csv -- about 4100 mentions across 150 passages, labels withheld.
> sample_submission.csv -- a valid submission with placeholder predictions.
> Columns of train.csv:
> passage_id (string) -- the passage a mention belongs to.
> period (string) -- a coarse era bucket for the passage, early or late.
> mention_id (string) -- a globally unique opaque mention identifier.
> mention_order (int) -- the mention's position in reading order within its passage, with 0 the first.
> mention_start, mention_end (int) -- the mention's token span in passage_text, inclusive, counting space-separated tokens from 0.
> mention_text (string) -- the mention's surface text, with proper names shown as [NAME].
> passage_text (string) -- the full passage as space-separated tokens, with proper names redacted to [NAME]; identical for all mentions of a passage.
> antecedent (string) -- training label: the mention_id this mention corefers with, or NEW for the first mention of its entity.
> entity_type (string) -- training label: one of PER, LOC, FAC, GPE, VEH, ORG, OTHER.
> The seven entity types are PER (person), LOC (location), FAC (facility or built structure), GPE (geo-political entity), VEH (vehicle), ORG (organization), and OTHER.
> Columns of test.csv are passage_id, period, mention_id, mention_order, mention_start, mention_end, mention_text, and passage_text, with the labels withheld.
> Notes:
> Antecedents never cross passage boundaries; every candidate is within the same passage and earlier in reading order.
> About a third of mentions are the first of their entity, so their true antecedent is NEW.
> Person mentions dominate, but the rarer types are worth recovering because the type score weights all seven types equally.
> Submission
> Write a CSV to ./working/submission.csv with exactly these columns:
> mention_id (string) -- a mention identifier from test.csv.
> antecedent (string) -- the predicted earlier mention_id in the same passage, or NEW.
> entity_type (string) -- one of PER, LOC, FAC, GPE, VEH, ORG, OTHER.
> Requirements:
> Provide one row for every test mention_id; missing rows are scored as worst-case for the affected mentions.
> antecedent must be NEW or a mention_id that occurs earlier in the same passage. An unknown, later, or self-referential antecedent is treated as NEW when the clustering is built, so a bad link simply fails to merge.
> entity_type must be one of the seven listed values.
> The grader is robust to formatting: a missing row, an unknown antecedent, or an out-of-vocabulary type is treated as a worst-case prediction for that mention rather than rejecting the whole file, so a complete, well-formed submission is required to reach the achievable ceiling.
> What Not To Use
> Solve the task from the provided passages, not by recovering their source. Specifically, do not search for, download, or match the passage text against any external text collection to recover entity identities or coreference links; do not reconstruct opaque mention_id or passage_id values back to any source records or undo the [NAME] redaction by external lookup; do not use any external labeled coreference data or manual labeling of test rows; and do not exploit row order or file metadata as a signal.
> Everything needed is in ./dataset/public/. General-purpose libraries and pretrained text encoders are allowed. The solution must run on CPU within the time budget.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Provenance of Agreement

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75n5af857kq1z026hd2cncw58bx9ng
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Provenance of Agreement
> When several short public posts about the same item say the same thing, the agreement itself carries almost no information about where it came from. The posters may have converged because the item really is that way; each may have been reacting to what was already visible above them; the accounts may all trace back to one writer; or a set of genuinely different writers may have started from the same supplied framing. These readings are generically confounded: they produce agreement that looks alike sentence by sentence, and telling them apart is a long-standing identification problem rather than a matter of spotting a bad post. The work here adapts the influence-versus-homophily identification problem (Shalizi and Thomas, 2011) and the sequential-influence experiments of Salganik, Dodds and Watts (2006) to a setting where the only evidence is the text itself.
> Each row is one bundle: five short posts written about a single item inside one observation window, given in the order they were posted, each line carrying the hours elapsed since the first post and the posting account's handle. Read the bundle and say what best accounts for the agreement in it.
> The bundles are not scraped. They are produced by a simulator that draws one of the five accounts below, plays it out over five separate posting accounts, and writes the result up, so what actually happened behind every bundle is known exactly and the answer is never an annotator's guess.
> The reading you have to give
> For each bundle, write one of these five readings in the explanation column:
> item_driven - the posters arrived at the same view separately, because the item has the property they are describing.
> cascade - the view formed in sequence: each later poster is working from what was already visible above, not from an independent look at the item.
> common_source - the agreeing posts trace back to a single writer working through several accounts.
> prompt_driven - the posters are different people who each began from the same supplied framing, and wrote it up in their own words.
> no_common_cause - there is nothing shared to point to: what looks like agreement is incidental, and the posts are not tied together.
> What separates the readings
> No single line settles it. What separates the five readings is how the agreement is distributed across the bundle: how much of it is the same wording rather than the same point, whether it is spread evenly or builds up in posting order, how the posts are spaced in time, and how much independent detail each poster brings that nobody else mentions. A reader who weighs those against each other does well; one who looks for a giveaway phrase does not.
> Dataset
> Three files. train.csv has 3000 rows, test.csv and sample_submission.csv have 1000 each.
> file	column	type	meaning
> train.csv	id	string	row key, train_0000 upwards
> train.csv	bundle	string	the five posts of one bundle, one per line, newline separated
> train.csv	explanation	string	the target: one of the five readings above
> test.csv	id	string	row key, test_0000 upwards
> test.csv	bundle	string	same format as in train.csv
> sample_submission.csv	id	string	every id in test.csv, in order
> sample_submission.csv	explanation	string	a constant placeholder answer, scoring 0
> Every line inside bundle has the form
> +12.4h @handleofposter: the text of the post.
> where the leading number is the hours elapsed since the first post of that bundle (so the first line is always +0.0h), the handle is the posting account, and the rest is the post itself. The five lines are in posting order, and the five handles in a bundle are always five different accounts.
> The test bundles are about kinds of item that appear nowhere in the training data, so every content noun in them is unseen and nothing that keys on what the item is will carry over. What does carry over is the shape of the agreement itself.
> Submission
> One row per test id, exactly the ids in test.csv, no duplicates.
> id,explanation test_0000,cascade test_0001,item_driven test_0002,common_source
> Evaluation
> The quantity to maximise is score below - the composite, not raw macro_f1. It runs from 0 to 1 and higher is better.
> macro_f1 = unweighted mean of the F1 score of each of the five readings skill = max(0, (macro_f1 - 0.2) / 0.8) diversity = min(1, max(0, (1 - p_max) / 0.25)) score = skill * diversity
> p_max is the share of the most frequent answer in the submission. With five readings in play and roughly equal numbers of each, a uniform random guess sits at macro_f1 0.2, so the score is chance-corrected: guessing is worth 0 rather than a fifth of the range. The diversity factor is 1.0 while p_max is at most 0.75 and falls linearly to 0 as p_max approaches 1, so a submission that answers the same way on every row - which is what sample_submission.csv does - scores 0.
> Some bundles genuinely admit more than one reading, and a share of the answers reflects that, so no submission can reach 1.0.
> For scale, measured with this scorer on the held-out categories: a word-and-bigram term-frequency model with logistic regression scores 0.00 and a nearest-neighbour model on the same features 0.01 - out of distribution they both collapse onto a single answer, which the diversity factor then zeroes. A model given only cheap counts (bundle length, word count, digit count, the last elapsed time, and how many distinct words the bundle uses) reaches 0.21. Reading the relations between the posts is worth several times either, and that gap is where the work is.
> What Not To Use
> No external APIs, network calls or remote inference at grading time.
> No external datasets. Everything needed is in train.csv.
> No training on the test bundles, no pseudo-labelling of the test split, no transductive use of test.csv of any kind.
> No hardcoded lookup tables keyed on ids, handles, or exact bundle text; no id fingerprinting.
> Term frequency over the bundle text is fine as preprocessing, but a bag-of-words model is not by itself the task: which words appear is not what separates the readings, and scored on its own it lands at the bottom of the range. What carries the signal is the relation between the posts.
> Submissions
> 79

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Dialect Meaning Under Source Shift

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx751bhj70dm276kpbpmcpc5zh8bts7n
- DOMAIN exactly as displayed: NLP
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
> A Yemeni Arabic proverb packs a cultural lesson into a few dialect words whose literal reading rarely gives the meaning: "he growled a camel" is not about camels. Reading one correctly means recognizing the figurative intent behind unfamiliar dialect, and doing it for proverbs and sources never seen before. This challenge tests exactly that transfer. It matters because most figurative-language and dialect resources are tiny and source-bound, so a model that only memorizes one anthology's phrasing looks good and then fails on the next collection. Here the test set is drawn entirely from an anthology held out of training, so the score reflects genuine cross-source understanding of what a proverb means, not recall of how one book worded it. It is a compact, low-resource probe of figurative and cross-dialect meaning, built so the surface words deliberately do not carry the answer.
> Task
> Match each masked Yemeni Arabic proverb to its intended Modern Standard Arabic (MSA) explanation. Every row offers 12 candidate explanations labeled A through L, exactly one of which is correct. Training and test are separated by source: the entire test set comes from an anthology that contributes nothing to training, so a solution has to generalize beyond memorized source style.
> Files and Fields
> All files are under dataset/public/.
> train.jsonl: one JSON object per line, with these fields:
> id (string): unique row identifier.
> proverb (string): the Yemeni Arabic proverb; [gap] marks deterministically masked tokens.
> candidates (list of exactly 12 strings): the candidate MSA explanations in fixed order, where index 0 is label A, index 1 is B, and so on through index 11 as label L.
> target (string): the correct label, one letter A through L. Present in train.jsonl only.
> test.jsonl: one JSON object per line, identical to train.jsonl but without target:
> id (string), proverb (string), candidates (list of exactly 12 strings).
> sample_submission.csv: a correctly formatted submission covering every test row, with columns:
> id (string): the test row id.
> prediction (string): one label A through L.
> Worked Example
> This is a complete prepared test example:
> proverb: كركر جمل.
> A: للدلالة عل الرضى بأخطاء المحب.
> B: للدلالة على سوء التدبير والتفكير.
> C: يضرب به للصبر والقناعة بالقليل.
> D: للدلالة عل عدم فهم المخاطب.
> E: كناية عن فشل المخاطب في أمر ما.
> F: يقال لمن يستخف بالأمور.
> G: للدلالة على [gap] شيء على شيء آخر.
> H: يضرب للشخص الذي لا يفهم.
> I: [gap] للرجل الكريم يقي سمعته بماله.
> J: يضرب للرجل الذي لا يتقن أي عمل.
> K: للدلالة على الصبر الميؤوس منه.
> L: یقال هذا المثل لربط الأمور بأسبابها.
> The correct label is H.
> Evaluation
> The score is exact accuracy: correct predictions / number of test rows. Higher is better. Labels are exactly balanced across A through L, so a constant or random label scores 0.083333.
> Submission
> Write ./working/submission.csv with exactly two columns, id and prediction. Requirements:
> exactly one row for every test id, and no id that is not in the test set;
> prediction is a single label from A through L;
> no extra columns, no missing or duplicated ids.
> A submission that violates any of these is rejected. A correctly formatted submission looks like this:
> id,prediction
> meaning_0a1b2c3d4e5f6a7b8c,H
> meaning_1b2c3d4e5f6a7b8c9d,C
> meaning_2c3d4e5f6a7b8c9d0e,L
> Start from sample_submission.csv, which already lists every test id, and write it with index=False.
> Measured Difficulty and Shortcuts
> There are 4,740 train rows and 552 test rows. Labels are exactly balanced, giving a chance floor and constant-label score of 0.083333. A lexical word and character overlap baseline scores 0.452899 under the candidate masking: well above the 0.083 chance level, so surface overlap does carry real signal, but far short of solving the task, so most of the remaining headroom toward a correct answer has to come from aligning figurative meaning rather than words. Candidate frequency, first candidate, and rarest global words all score at chance (0.083333); shortest candidate and fewest gaps sit at 0.086957 and 0.085145. Every candidate is reused exactly 12 times within its candidate group, forcing a query-blind candidate scorer to chance across the cycle.
> The difficulty knob is the candidate masking rate and the candidate count K. Raising either makes matching harder; lowering it exposes more meaning-bearing words.
> What Not To Use
> TF-IDF and bag-of-words are preprocessing only, never the prediction mechanism. A raw lexical word or character overlap ranker already reaches 0.452899, about 78 percent of a strong learned model's score, purely from surface token overlap that survives the masking. The scorer only checks predictions and cannot inspect your method, so this is a rule of the task, not an automated filter: you may tokenize, vectorize, or compute overlap features as inputs to a model, but the decision of which explanation matches must come from a learned representation of figurative meaning, not from ranking candidates by lexical similarity to the proverb.
> Do not infer the label from candidate position, length, gap count, or global candidate frequency. Every candidate is reused exactly 12 times within its group, so these query-blind shortcuts are forced to chance and any lift from them is an artifact.
> Do not use the public test rows for model selection, and do not attempt to recover the source anthology or its published explanations from any external archive.
> Runtime Environment
> Runs are scored on CPU with no GPU, with 62 GB RAM and a 90-minute limit. Package installation is not allowed; the preinstalled stack (numpy, scipy, pandas, scikit-learn, pytorch, transformers, sentence-transformers) is available, and a compact Arabic or multilingual text encoder may be downloaded and used or lightly adapted on CPU. A learned representation is expected, subject to the What Not To Use rules above. Your code must read from ./dataset/public/ and write ./working/submission.csv.
> Submissions
> 51

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Contextual Numeric Claim Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73qd4j3t7ws1vn4xhc3vg8h18bhaw7
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: ↑ Higher is better

Full challenge description from page:

> Overview
> A document-quality pipeline has flagged one numeric corruption inside a Wikipedia paragraph, but neither the damaged mention nor its original value is known. Each item exposes four tracked numeric mentions and eight format-compatible replacement candidates. Identify the damaged mention and rank all eight candidates from most to least likely original value.
> This is joint fault localization and value restoration. Every tracked value stays syntactically valid, the inserted value uses a compatible numeric form, mention and candidate identifiers are opaque, and complete test articles never appear in training. The text is real human-authored WikiText-2 prose.
> Detection and repair are scored independently. The ranking term no longer requires getting the mention right: reciprocal-rank credit is awarded on every row from the submitted candidate order alone, whether or not the damaged mention was identified. Only the small exact-match bonus requires both halves at once.
> Candidate geometry is deliberately uninformative. Every tracked mention contributes the same number of replacement candidates, placed on either side of that mention at comparable numeric distance. Numeric proximity therefore tells you which mention a candidate belongs to, and nothing else: it does not indicate which mention was damaged, and within a mention's own candidates it does not indicate which value was original. Both halves of the task have to be settled from linguistic and document context.
> Dataset
> Each UTF-8 JSONL line is one object.
> train.jsonl
> Schema illustration, not a dataset row:
> {
> "item_id": "it_example",
> "corrupted_text": "The population rose from [m_a]12,400 to [m_b]81,000 between [m_c]1998 and [m_d]2004 .",
> "tracked_mentions": [
> {"mention_id": "m_a", "displayed_value": "12,400"},
> {"mention_id": "m_b", "displayed_value": "81,000"},
> {"mention_id": "m_c", "displayed_value": "1998"},
> {"mention_id": "m_d", "displayed_value": "2004"}
> ],
> "replacement_candidates": [
> {"candidate_id": "c_1", "value": "9,800"},
> {"candidate_id": "c_2", "value": "15,600"},
> {"candidate_id": "c_3", "value": "62,000"},
> {"candidate_id": "c_4", "value": "104,000"},
> {"candidate_id": "c_5", "value": "1983"},
> {"candidate_id": "c_6", "value": "2009"},
> {"candidate_id": "c_7", "value": "1991"},
> {"candidate_id": "c_8", "value": "2016"}
> ],
> "corrupt_mention_id": "m_b",
> "correct_candidate_id": "c_3"
> }
> Field notes:
> item_id is a string, unique across the whole challenge.
> corrupted_text is a string. Each tracked mention's token is prefixed inline with [mention_id]. Exactly one numeric value in this text has been replaced.
> tracked_mentions is a list of exactly four objects, each with string fields mention_id and displayed_value.
> replacement_candidates is a list of exactly eight objects, each with string fields candidate_id and value.
> corrupt_mention_id is a string and appears only in train.jsonl.
> correct_candidate_id is a string and appears only in train.jsonl.
> test.jsonl
> Identical input fields. corrupt_mention_id and correct_candidate_id are omitted.
> dataset_info.json
> seed is an integer.
> tracked_mentions is the integer 4.
> replacement_candidates is the integer 8.
> candidates_per_mention is the integer 2.
> train_items and test_items are integers.
> test_stratum_counts is an object mapping each of year, count, structured to an integer.
> split_unit is the string document.
> sample_submission_score is the float 0.0.
> sample_submission.csv
> Three string columns, one row per test item:
> item_id,corrupt_mention_id,replacement_ranking
> it_example,PLACEHOLDER,PLACEHOLDER
> The unchanged sample scores exactly 0.0.
> Submission format
> Submit a CSV with exactly these three columns, in this order:
> item_id — string. Every test item_id exactly once, no extras, no duplicates.
> corrupt_mention_id — string. One of that item's four mention_id values.
> replacement_ranking — string. All eight of that item's candidate_id values, space separated, best first, each used exactly once.
> Example row:
> item_id,corrupt_mention_id,replacement_ranking
> it_example,m_b,c_3 c_4 c_1 c_2 c_7 c_5 c_6 c_8
> The grader rejects wrong column names, wrong column order, missing or duplicate item_id values, extra or missing rows, empty fields, mention IDs that do not belong to the item, rankings that are not a permutation of that item's eight candidates, and PLACEHOLDER mixed with real predictions.
> Evaluation
> For row i, let D_i be 1 when the damaged mention is identified correctly and 0 otherwise. Let r_i be the rank from 1 to 8 of the true replacement candidate. Let E_i be 1 only when D_i = 1 and r_i = 1. Detection and ranking are scored independently, so ranking earns credit even when detection misses.
> G_i = 0.45 * D_i + 0.35 * (1 / r_i) + 0.20 * E_i
> A uniformly random valid submission picks one of four mentions and one of 8! rankings. With H_8 = 1 + 1/2 + ... + 1/8 = 2.717857, its expected gain is:
> C = 0.45 * (1/4) + 0.35 * (H_8/8) + 0.20 * (1/32)
> = 0.237656
> For any row group R:
> Skill(R) = clip((mean(G_i over R) - C) / (1 - C), 0, 1)
> Private rows are grouped into three numeric strata of roughly equal size: year, count, and structured. There is no weakest-stratum term.
> FinalScore = 0.80 * Skill(all rows)
> + 0.20 * mean(Skill(year), Skill(count), Skill(structured))
> The result is in [0,1]; higher is better. Random expected performance maps to zero, perfect repair maps to one.
> Reference baseline
> A statistical reference that uses no pretrained model scores 0.143 on the released split. It repairs the training paragraphs, estimates a shrunken Gaussian over magnitude for every (context word, numeric family) pair, and fits a conditional-logit model over the four mentions, keeping the fitted weights only when cross-validated top-1 accuracy beats a single raw feature. It localises the damaged mention on 37.6% of rows against a 25% chance rate.
> For comparison on the same split: the unchanged sample submission scores 0.0, a uniformly random valid submission scores below 0.05, and a submission that reasons only about numeric distance and never reads the text scores below 0.03. Perfect repair scores 1.0.
> Rules
> CPU only: 10 cores, 62 GB RAM, maximum 5,400 seconds.
> No internet, runtime downloads, external data, or hardcoded answers.
> No regular expressions and no TF-IDF.
> Use only libraries preinstalled in the Kaggle Docker image.
> Learn from the supplied training examples and text.
> Why this is difficult
> The inserted value is format-compatible and every tracked mention stays grammatically plausible, so there is no surface tell. Candidates sit at comparable numeric distance on both sides of the mention they belong to, so numeric proximity cannot substitute for reading: after localization there is still a genuine contextual choice left, and both halves of the score have to be earned separately. Evaluation is document-disjoint, so article-specific facts cannot be memorised from training.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Maintenance Intent Token Cloze Restoration

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx71jgdk1t7adky7varrp0v2pn8axy3q
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Maintenance Intent Token Cloze Restoration
> Overview
> Maintenance commits often summarize a concrete source-code change in just a few words. In this CPU-friendly NLP/code-text challenge, each row shows an anonymized commit-intent sequence where two important word-like tokens have been replaced by MASK_C1 and MASK_C2. The row also includes anonymized patch-evidence tokens from the corresponding file change. Your task is to restore the two missing intent word tokens in order. The missing target tokens are always W_-prefixed word-like tokens.
> The examples come from real maintenance commits, but the public data is transformed into opaque stable tokens. This makes the task a language-and-evidence restoration problem rather than a lookup task. Solvers must connect the surrounding intent context with the patch evidence and output the missing W_ token sequence.
> This is not a tabular challenge, not a regression challenge, not a commit-history reconstruction task, and not a patch-marker labeling task. Each row is an independent sequence restoration problem over anonymized text/code evidence.
> Evaluation
> Submissions are scored using exact token restoration rate. The grader compares the submitted two-token W_ sequence against the private answer sequence for each row and returns the fraction of masked positions restored exactly.
> def evaluate(y_true_tokens, y_pred_tokens):
> correct = 0
> total = 0
> for true_seq, pred_seq in zip(y_true_tokens, y_pred_tokens):
> for true_token, pred_token in zip(true_seq, pred_seq):
> correct += int(true_token == pred_token)
> total += 1
> return correct / total
> Higher scores are better. The public grading range is 0 to 1.
> Dataset
> The prepared dataset contains training rows, test rows, and a sample submission. Every row contains exactly two masked intent positions. The training file includes the correct missing W_ token sequence, while the test file withholds it.
> Files in public/:
> train.csv - Training examples with completed missing W_ token sequences.
> test.csv - Test examples with missing W_ token sequences withheld.
> sample_submission.csv - Example submission with placeholder W_ token predictions.
> Files in private/:
> answers.csv - Ground-truth missing W_ token sequences for the test rows.
> Columns
> | File | Column | Type | Description |
> |------|--------|------|-------------|
> | train.csv | id | string | Opaque row identifier. |
> | train.csv | masked_intent_tokens | string | Space-separated anonymized intent sequence. Hidden positions appear as MASK_C1 and MASK_C2. |
> | train.csv | evidence_patch_tokens | string | Space-separated anonymized evidence tokens from the corresponding patch. Word-like units use W_ prefixes, numeric bands use PATCH_NUM_*, and punctuation uses P_ prefixes. |
> | train.csv | mask_ids | string | Space-separated mask identifiers, always C1 C2 in the order to restore. |
> | train.csv | target_tokens | string | Space-separated ground-truth missing W_ tokens for the masks in mask_ids order. Target tokens are always word-like W_ tokens, not PATCH_NUM_* numeric bands or P_* punctuation tokens. |
> | test.csv | id | string | Opaque row identifier for submission matching. |
> | test.csv | masked_intent_tokens | string | Same format as the training masked_intent_tokens column. |
> | test.csv | evidence_patch_tokens | string | Same format as the training evidence_patch_tokens column. |
> | test.csv | mask_ids | string | Space-separated mask identifiers to restore. |
> | sample_submission.csv | id | string | Test row identifier. |
> | sample_submission.csv | target_tokens | string | Placeholder W_ token sequence in the required submission format. |
> | answers.csv | id | string | Test row identifier. |
> | answers.csv | target_tokens | string | Private ground-truth missing W_ token sequence. |
> Example
> masked_intent_tokens:
> W_12ab34cd56 MASK_C1 W_8fa901bc22 MASK_C2 P_991a22bb
> evidence_patch_tokens:
> PATCH_NUM_SMALL W_46cc10de92 W_91a0ef3321 W_d4129ac501 P_88db116a W_77f9cd4510
> mask_ids:
> C1 C2
> A valid prediction contains the two restored opaque W_ tokens:
> W_46cc10de92 W_d4129ac501
> ## Submission
> Submit a CSV file named `submission.csv` with exactly these columns in this order:
> | Column | Type | Description |
> |--------|------|-------------|
> | `id` | string | Row identifier from `test.csv`. |
> | `target_tokens` | string | Two space-separated `W_` tokens corresponding to `mask_ids`. `PATCH_NUM_*` and `P_*` tokens are not valid submission targets. |
> Example:
> id,target_tokens
> cloze_011e31e31f9a5ceb,W_46cc10de92 W_d4129ac501
> cloze_027eadd7f77b384c,W_783ab00121 W_9aa34db441
> Requirements:
> - Include exactly one row for every row in `test.csv`.
> - Preserve the `id` values exactly.
> - Provide exactly two `W_` tokens per row.
> - Do not submit `PATCH_NUM_*` numeric-band tokens or `P_*` punctuation tokens as targets.
> - Match the order of `mask_ids`.
> - Write predictions to `./working/submission.csv`.
> ## What Not To Use
> Do not use internet access, external packages, repository lookup, commit lookup, raw source lookup, or any data outside `./dataset/public/`. Do not hardcode outputs for specific test IDs. Do not attempt to reverse the opaque token mapping or reconstruct the original raw source text. Solutions should learn from the provided public training rows and produce generalizable missing `W_` token sequences for the test rows.
> &nbsp;

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Factual Probe Lexical Backbone Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77pgxk010qpa7nnh30h86g918c1we7
- DOMAIN exactly as displayed: NLP
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
> Factual Probe Lexical Backbone Reconstruction is a structured NLP challenge about recovering a graph that is defined by answers the model never directly receives.
> Every sample contains eighteen factual questions.
> Each question has one distinct short factual answer.
> The released input contains the questions, not those answer strings.
> Exactly two of the eighteen visible questions are partially obscured with one <veil> token.
> The hidden answers are normalized and compared pairwise using a published lexical-affinity function.
> This creates a complete weighted graph over the eighteen question nodes.
> There are:
> 18 nodes.
> 153 possible undirected edges.
> 17 edges in the target tree.
> The target is the maximum-spanning tree induced by the eighteen unseen answer strings.
> Participants do not submit answers.
> Participants submit one numeric score for every possible node pair.
> The evaluator ranks those 153 scores and applies a deterministic maximum-spanning-tree decoder.
> The objective is therefore:
> infer which question pairs should be linked in the lexical backbone formed by their unseen factual answers.
> The challenge is not ordinary question answering.
> It is not question similarity.
> It is not same-answer clustering.
> It is not passage retrieval.
> It is not entity classification.
> Two questions can be topically unrelated yet become adjacent because their unseen answers have similar surface forms.
> Two visibly similar questions can remain far apart because their unseen answers are lexically different.
> A successful model must reason through an intermediate representation that is never directly supervised at test time:
> Understand each factual question.
> Infer likely properties of its answer.
> Estimate how answer surfaces relate across question pairs.
> Rank many competing links.
> Recover a globally valid tree.
> Problem Intuition
> Consider eighteen questions as eighteen factual probes.
> Each probe points toward one hidden short answer.
> The questions are observable.
> The answer strings are latent.
> The final graph is generated from the latent strings rather than from the visible questions themselves.
> For example, two questions about completely different subjects may imply answers sharing:
> A surname.
> A location term.
> A title word.
> A numeric pattern.
> A prefix.
> A suffix.
> Those hidden answer strings may therefore receive high lexical affinity.
> Conversely, two questions about the same broad topic may imply answer strings with almost no lexical overlap.
> Visible semantic similarity is therefore only an indirect signal.
> The model must learn which properties of a question predict the surface form of its likely answer.
> Eighteen-Node Panel
> Every sample contains exactly eighteen labeled nodes:
> Q01
> Q02
> Q03
> Q04
> Q05
> Q06
> Q07
> Q08
> Q09
> Q10
> Q11
> Q12
> Q13
> Q14
> Q15
> Q16
> Q17
> Q18
> Each node contains one natural-language factual question.
> Each underlying answer identity is distinct within that panel.
> The graph target always spans all eighteen nodes.
> Partial Question Occlusion
> Exactly two questions in every panel contain one literal:
> <veil>
> The marker replaces one content-bearing word from the original question.
> For example:
> who directed the <veil> adaptation released in 1998
> The missing question word is not a prediction target.
> The remaining sixteen questions are fully visible.
> This limited occlusion prevents the benchmark from becoming a pure exact-question lookup task while preserving enough information for factual inference.
> The graph target is still generated from the same underlying answer.
> Hidden Answer Normalization
> The target graph is deterministic.
> Each unseen answer is normalized using the following procedure.
> Apply Unicode NFKC normalization.
> Convert to lowercase.
> Extract alphanumeric word tokens.
> Remove a leading a, an, or the when present.
> Preserve the remaining normalized tokens.
> Concatenate those tokens without spaces to obtain a compact string.
> Conceptually:
> The Example Name
> becomes:
> tokens  = ["example", "name"]
> compact = "examplename"
> Lexical Pair Affinity
> Every unordered pair of hidden answers receives one affinity value.
> Five components are used.
> Character Bigram Dice
> Create the set of adjacent two-character substrings from each compact answer.
> CharDice =
> 2 Ã— |Bigrams(A) âˆ© Bigrams(B)|
> / (|Bigrams(A)| + |Bigrams(B)|)
> If both bigram sets are empty, the value is 1.
> If exactly one is empty, the value is 0.
> Token Jaccard
> Let TA and TB be the normalized answer-token sets.
> TokenJaccard =
> |TA âˆ© TB|
> / |TA âˆª TB|
> If both sets are empty, the value is 1.
> ### Prefix Agreement
> Prefix =
> common_prefix_length(A, B) / max(len(A), len(B))
> Suffix Agreement
> Suffix =
> common_suffix_length(A, B)
> / max(len(A), len(B))
> Length Agreement
> Length =
> 1
> - |len(A) - len(B)|
> / max(len(A), len(B))
> The value is clipped to [0, 1].
> Final Affinity
> Affinity =
> 0.45 Ã— CharDice
> + 0.25 Ã— TokenJaccard
> + 0.10 Ã— Prefix
> + 0.10 Ã— Suffix
> + 0.10 Ã— Length
> Higher values indicate stronger lexical similarity between the two unseen answer surfaces.
> The affinity is about answer form, not semantic relatedness.
> Backbone Construction
> With eighteen nodes there are:
> 18 choose 2 = 153
> candidate edges.
> The target backbone is the maximum-spanning tree over the complete affinity graph.
> Construction uses deterministic Kruskal decoding.
> Candidate edges are ordered by:
> Higher affinity first.
> Lower first node index on exact ties.
> Lower second node index on remaining ties.
> Starting from an empty graph:
> Visit edges in that order.
> Accept an edge when it does not create a cycle.
> Reject an edge when it would create a cycle.
> Stop after seventeen accepted edges.
> The result is one connected acyclic graph containing every node.
> Moderately Confusable Panels
> Panels are not assembled randomly.
> Question-answer records are first grouped by broad hidden-answer form, including:
> Numeric versus textual shape.
> Answer token count.
> Compact answer length.
> Candidate records are then ordered within those neighborhoods using hidden surface characteristics.
> Panel construction prefers groups containing several plausible alternatives near the selected neighborhood boundary.
> The benchmark therefore contains hard negatives without forcing every test panel into an extreme near-tie regime.
> Training and test use closely matched construction rules.
> Test panels use only a modestly tighter ambiguity preference.
> This keeps the problem difficult while preserving a learnable relationship between released training examples and evaluation examples.
> Train/Test Separation
> The official split is based on normalized hidden answer identity.
> All examples associated with one normalized answer identity belong wholly to one partition.
> The same normalized answer identity cannot occur in both released training and test panels.
> Training records may participate in a small number of independently constructed training panels.
> Test records are used at most once across test panels.
> Node order is deterministically scrambled within each panel.
> Prediction Target
> For every test sample, submit one numeric score for every unordered pair of Q01 through Q18.
> Example edge-score columns include:
> Q01__Q02_score
> Q01__Q18_score
> Q05__Q12_score
> Q11__Q17_score
> Q17__Q18_score
> The submission contains exactly:
> 1 sample_id column.
> 153 edge-score columns.
> Total:
> 154 columns.
> Scores:
> Must be finite numbers.
> May be negative.
> May exceed 1.
> Do not need to be probabilities.
> Do not need to sum to one.
> The evaluator uses their relative ordering within each sample.
> Participants do not directly submit seventeen selected edges.
> Complete Submission Example
> The following is a structurally valid one-row submission containing every required column.
> sample_id,Q01__Q02_score,Q01__Q03_score,Q01__Q04_score,Q01__Q05_score,Q01__Q06_score,Q01__Q07_score,Q01__Q08_score,Q01__Q09_score,Q01__Q10_score,Q01__Q11_score,Q01__Q12_score,Q01__Q13_score,Q01__Q14_score,Q01__Q15_score,Q01__Q16_score,Q01__Q17_score,Q01__Q18_score,Q02__Q03_score,Q02__Q04_score,Q02__Q05_score,Q02__Q06_score,Q02__Q07_score,Q02__Q08_score,Q02__Q09_score,Q02__Q10_score,Q02__Q11_score,Q02__Q12_score,Q02__Q13_score,Q02__Q14_score,Q02__Q15_score,Q02__Q16_score,Q02__Q17_score,Q02__Q18_score,Q03__Q04_score,Q03__Q05_score,Q03__Q06_score,Q03__Q07_score,Q03__Q08_score,Q03__Q09_score,Q03__Q10_score,Q03__Q11_score,Q03__Q12_score,Q03__Q13_score,Q03__Q14_score,Q03__Q15_score,Q03__Q16_score,Q03__Q17_score,Q03__Q18_score,Q04__Q05_score,Q04__Q06_score,Q04__Q07_score,Q04__Q08_score,Q04__Q09_score,Q04__Q10_score,Q04__Q11_score,Q04__Q12_score,Q04__Q13_score,Q04__Q14_score,Q04__Q15_score,Q04__Q16_score,Q04__Q17_score,Q04__Q18_score,Q05__Q06_score,Q05__Q07_score,Q05__Q08_score,Q05__Q09_score,Q05__Q10_score,Q05__Q11_score,Q05__Q12_score,Q05__Q13_score,Q05__Q14_score,Q05__Q15_score,Q05__Q16_score,Q05__Q17_score,Q05__Q18_score,Q06__Q07_score,Q06__Q08_score,Q06__Q09_score,Q06__Q10_score,Q06__Q11_score,Q06__Q12_score,Q06__Q13_score,Q06__Q14_score,Q06__Q15_score,Q06__Q16_score,Q06__Q17_score,Q06__Q18_score,Q07__Q08_score,Q07__Q09_score,Q07__Q10_score,Q07__Q11_score,Q07__Q12_score,Q07__Q13_score,Q07__Q14_score,Q07__Q15_score,Q07__Q16_score,Q07__Q17_score,Q07__Q18_score,Q08__Q09_score,Q08__Q10_score,Q08__Q11_score,Q08__Q12_score,Q08__Q13_score,Q08__Q14_score,Q08__Q15_score,Q08__Q16_score,Q08__Q17_score,Q08__Q18_score,Q09__Q10_score,Q09__Q11_score,Q09__Q12_score,Q09__Q13_score,Q09__Q14_score,Q09__Q15_score,Q09__Q16_score,Q09__Q17_score,Q09__Q18_score,Q10__Q11_score,Q10__Q12_score,Q10__Q13_score,Q10__Q14_score,Q10__Q15_score,Q10__Q16_score,Q10__Q17_score,Q10__Q18_score,Q11__Q12_score,Q11__Q13_score,Q11__Q14_score,Q11__Q15_score,Q11__Q16_score,Q11__Q17_score,Q11__Q18_score,Q12__Q13_score,Q12__Q14_score,Q12__Q15_score,Q12__Q16_score,Q12__Q17_score,Q12__Q18_score,Q13__Q14_score,Q13__Q15_score,Q13__Q16_score,Q13__Q17_score,Q13__Q18_score,Q14__Q15_score,Q14__Q16_score,Q14__Q17_score,Q14__Q18_score,Q15__Q16_score,Q15__Q17_score,Q15__Q18_score,Q16__Q17_score,Q16__Q18_score,Q17__Q18_score
> FPB_example_001,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
> The zero values are only a format example.
> Equal values are resolved using the published edge-index tie-breaking rule.
> For actual submissions:
> Use sample_submission.csv as the authoritative header.
> Keep every column in the supplied order.
> Include every evaluated sample_id exactly once.
> Provide one finite numeric value for every edge-score column.
> Do not add or remove columns.
> Challenge Type
> This is a supervised structured NLP graph-prediction challenge.
> Pretrained language models are allowed.
> Eligible systems include:
> BERT-family encoders.
> RoBERTa-family encoders.
> DeBERTa-family encoders.
> Distilled transformer models.
> Compact sentence encoders.
> Pairwise cross-encoders.
> Learned bi-encoders.
> Small encoder-decoder models.
> Graph neural networks.
> Learned edge-ranking models.
> Structured tree predictors.
> Eligible learned ensembles.
> Pretrained factual knowledge can be useful because the graph depends on factual answers that are not visible in the input.
> Machine-Learning Requirement
> Predictions must come from a learned system.
> At least one predictive component must contain parameters fitted from the released training data.
> Those parameters may be initialized from a public pretrained model.
> Eligible approaches include:
> Learning edge likelihood from question pairs.
> Learning latent answer-form embeddings.
> Internally predicting likely answers with a compact model.
> Training pairwise compatibility heads over question representations.
> Training a panel-level graph network.
> Learning edge rankings before deterministic tree decoding.
> Combining learned answer hypotheses with learned discriminative scores.
> The complete predictive method may not be purely:
> Hand-written keyword rules.
> Raw lexical similarity between visible questions.
> Static question-type tables.
> Manual answer dictionaries.
> Hard-coded graph templates.
> Manual test labeling.
> Deterministic heuristics with no fitted predictive component.
> The spanning-tree decoder itself may be deterministic.
> Compute
> The execution environment provides:
> 10 CPU cores.
> 62.5 GiB RAM.
> No GPU.
> The graph itself is small:
> 18 nodes.
> 153 candidate edges.
> 17 selected edges.
> Most compute is expected to come from language encoding and edge scoring.
> Practical CPU methods include:
> Frozen transformer embeddings.
> Distilled encoders.
> Quantized inference.
> Cached question representations.
> Lightweight pairwise heads.
> Candidate-edge pruning.
> Compact cross-encoders for difficult pairs.
> Small generative models for internal answer hypotheses.
> Released Files
> The released package contains exactly:
> train.jsonl
> test.jsonl
> sample_submission.csv
> No answer dictionary, hidden affinity matrix, graph manifest, or additional helper sidecar is released.
> train.jsonl
> Each line is one JSON object.
> sample_id
> Type:
> string
> Unique sample identifier used for alignment.
> Do not use it as a predictive feature.
> questions
> Type:
> list of eighteen objects
> Each object contains:
> node
> text
> Example:
> {"node":"Q07","text":"who wrote the <veil> novel"}
> Exactly two question texts contain <veil>.
> The other sixteen are fully visible.
> tree_edges
> Training only.
> Type:
> list of seventeen strings
> Example:
> Q03-Q11
> The seventeen edges form one connected tree over Q01 through Q18.
> The answer strings and pairwise affinity values are not released.
> test.jsonl
> Each line contains:
> sample_id
> questions
> The tree_edges field is omitted.
> Exactly two questions contain one <veil> marker.
> sample_submission.csv
> Contains exactly:
> sample_id
> all 153 edge-score columns
> The supplied file is the authoritative submission schema.
> Submissions are invalid when they contain:
> Missing sample IDs.
> Extra sample IDs.
> Duplicate sample IDs.
> Missing columns.
> Extra columns.
> Reordered columns.
> Blank edge values.
> Non-numeric values.
> NaN.
> Positive infinity.
> Negative infinity.
> Prediction Decoding
> For every submitted row:
> Read the 153 edge scores.
> Associate each score with its Qxx-Qyy pair.
> Sort candidates by descending submitted score.
> Break ties by lower first node index.
> Break remaining ties by lower second node index.
> Apply Kruskal cycle checking.
> Accept legal edges until seventeen have been selected.
> The decoded prediction is always one legal spanning tree.
> Evaluation
> Submissions are scored from 0.01 to 100.0.
> Higher is better.
> A perfect submission receives exactly 100.0 points.
> The metric measures four forms of partial structural recovery plus exact-tree completion:
> Edge Recovery.
> Split Recovery.
> Distance Recovery.
> Degree Recovery.
> Exact Tree Recovery.
> Each sample is scored independently.
> The final leaderboard score is the arithmetic mean of those per-sample scores.
> This prevents one unusually poor panel from collapsing the score of the full dataset.
> Edge Recovery
> Both trees contain exactly seventeen edges.
> EdgeRecovery =
> shared predicted/true edges
> / 17
> Literal adjacency is the dominant component of the metric.
> Split Recovery
> Removing one tree edge produces two connected components.
> Each edge therefore defines one node bipartition.
> For every edge:
> Remove the edge.
> Compute both components.
> Keep the smaller component.
> If both contain nine nodes, keep the lexicographically smaller sorted tuple.
> Each tree yields seventeen canonical splits.
> SplitRecovery =
> shared canonical splits
> / 17
> Distance Recovery
> A tree contains one unique path between every node pair.
> There are 153 unordered node pairs.
> DistanceRecovery =
> node pairs with exactly matching tree distance
> / 153
> Degree Recovery
> For node i:
> d_pred(i) is predicted degree.
> d_true(i) is true degree.
> DegreeError =
> sum_i |d_pred(i) - d_true(i)|
> / 34
> Then:
> DegreeRecovery =
> clip(1 - DegreeError, 0, 1)
> Exact Tree Recovery
> ExactTree = 1
> when all seventeen predicted edges are correct.
> Otherwise:
> ExactTree = 0
> Per-Sample Structural Score
> First calculate:
> Structure =
> 0.55 Ã— EdgeRecovery
> + 0.15 Ã— SplitRecovery
> + 0.15 Ã— DistanceRecovery
> + 0.15 Ã— DegreeRecovery
> Then calculate:
> Completion =
> 0.92
> + 0.08 Ã— ExactTree
> The sample score is:
> SampleScore =
> 100
> Ã— Structure^1.20
> Ã— Completion
> The sample score is clipped to:
> [0.01, 100]
> The final challenge score is:
> Score =
> mean(SampleScore over all evaluated samples)
> A perfect prediction has:
> Structure = 1
> Completion = 1
> SampleScore = 100
> Therefore a perfect submission receives exactly:
> 100.0
> Metric Behavior
> The metric is designed to give stable partial credit.
> Edge recovery is dominant, while split, path-distance, and degree agreement reward meaningful near-misses.
> Exact-tree recovery provides an additional completion bonus without acting as a binary gate.
> Controlled tree perturbations give approximately the following behavior:
> Exact tree: 100.
> One changed edge: about 80.
> Two changed edges: about 70.
> Three changed edges: about 64.
> Four changed edges: about 59.
> Five changed edges: about 54.
> Unrelated random tree: roughly low teens on average.
> These values are illustrative controlled perturbations, not guaranteed model scores.
> Reproducing The Metric Locally
> For every validation sample:
> Produce 153 edge scores.
> Decode one maximum-spanning tree using the published rule.
> Measure literal edge overlap.
> Derive and compare canonical tree splits.
> Compare all 153 pairwise path distances.
> Compare the eighteen node degrees.
> Check exact tree equality.
> Calculate the weighted Structure term.
> Apply the completion multiplier.
> Calculate the per-sample score.
> Average sample scores.
> No external model, semantic judge, or retrieval service is used by the metric.
> Intended Modeling Approaches
> Pairwise Edge Ranking
> Construct 153 question pairs from every training panel.
> Train a learned ranker to place gold tree edges above non-tree alternatives.
> Possible models include:
> Compact cross-encoders.
> Bi-encoder interaction heads.
> Pairwise MLPs.
> Ranking losses.
> Hard-negative sampling.
> Latent Answer-Form Prediction
> A model can predict properties of the unseen answer from its question.
> Possible internal representations include:
> Expected answer token count.
> Approximate character length.
> Numeric or textual answer form.
> Person/place/title-like structure.
> Learned latent lexical embeddings.
> Pairwise compatibility can then be estimated from those representations.
> Internal Answer Generation
> A compact pretrained QA model can generate a likely answer hypothesis for each question.
> Those hypotheses can be normalized with the published affinity rule.
> The resulting affinity scores can be:
> Used directly.
> Blended with learned pair scores.
> Supplied to a graph-level reranker.
> The generated answers are intermediate model state, not submission output.
> Panel-Level Graph Learning
> Encode all eighteen questions jointly.
> Construct the complete candidate graph.
> Use graph attention or message passing to refine edge scores based on competing relationships elsewhere in the panel.
> Possible auxiliary objectives include:
> Edge classification.
> Degree prediction.
> Pairwise tree-distance prediction.
> Tree-level ranking.
> Structured Ranking
> The final decoder is known in advance.
> Models may therefore optimize edge order directly using:
> Pairwise ranking objectives.
> Maximum-margin tree learning.
> Cycle-aware negatives.
> Graph-level reranking.
> Differentiable spanning-tree approximations.
> Practical CPU Baseline
> A practical CPU solution may:
> Encode all eighteen questions with a compact pretrained encoder.
> Cache the node embeddings.
> Create features for all 153 pairs.
> Train a lightweight pairwise ranker.
> Score all candidate test edges.
> Decode using the official maximum-spanning-tree rule.
> A stronger CPU solution may additionally:
> Generate one internal answer hypothesis per node.
> Compute the published answer-affinity features.
> Blend those features with learned pair scores.
> Refine ambiguous edges with a compact cross-encoder.
> Decode the final graph.
> Validation And Leakage
> Local validation should split by complete panel.
> All derivatives of one panel must remain together, including:
> Node-level examples.
> Pair examples.
> Edge labels.
> Cached embeddings.
> Generated answer hypotheses.
> Candidate affinity matrices.
> Graph augmentations.
> Hard-negative sets.
> Do not place derivatives of one panel into both local training and validation.
> Allowed Resources
> Participants may use:
> Released challenge files.
> Public pretrained language models.
> Associated public tokenizer files.
> Standard NLP libraries.
> Standard numerical libraries.
> Standard machine-learning frameworks.
> Standard deep-learning frameworks.
> Standard graph libraries.
> Standard spanning-tree implementations.
> Auxiliary labels derived only from released training targets.
> Eligible learned ensembles.
> Disallowed Resources
> Participants may not use:
> Unreleased evaluation targets.
> Manual test annotation.
> Search-engine lookup of exact test questions.
> External factual databases queried specifically for test rows.
> Hard-coded hidden test edges.
> sample_id as a predictive feature.
> Row order as a predictive feature.
> Submission-feedback reconstruction of hidden targets.
> Purely rule-based or non-learned prediction systems are not eligible.
> Limitations
> The backbone represents lexical similarity among normalized answer surfaces.
> It is not a semantic ontology.
> Two unrelated answers can become neighbors because their strings overlap.
> Two semantically related answers can be distant because their normalized surfaces differ.
> Two question texts per panel are intentionally partially obscured.
> The benchmark evaluates recovery of the controlled lexical backbone rather than real-world semantic graph structure.
> Expected Outcome
> A successful system should:
> Infer useful factual-answer properties from question language.
> Remain robust to two partially obscured questions.
> Distinguish visible question similarity from latent answer-surface similarity.
> Rank 153 candidate edges.
> Handle moderately confusable alternatives.
> Recover literal adjacency.
> Preserve larger tree cuts.
> Preserve pairwise path structure.
> Recover leaf and hub patterns.
> Produce exact trees on some panels.
> Run efficiently in the CPU-only environment.
> The prediction objective is:
> score all question pairs so that maximum-spanning-tree decoding reconstructs the seventeen-edge lexical backbone induced by the eighteen unseen factual answers.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Complaint Route Relations

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx712expepxrtnycgtcwxvqksd8byvr0
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Complaint Route Relations
> Overview
> Operational taxonomies are normally learned as a direct mapping from one document to one named category. This challenge removes that mapping entirely. No product name, issue name, or single-document taxonomy target is released. Instead, you must infer the latent hierarchical concordance between two independently submitted complaint narratives.
> Each row is a new prediction unit: an unordered pair of narratives. The target reveals only whether the pair agrees at both hidden hierarchy levels, agrees at the broad level but diverges at the fine level, or diverges at the broad level. A solver therefore cannot train an ordinary complaint-to-product or complaint-to-issue classifier from the released labels. It must learn a symmetric comparison function from pair supervision.
> Each row contains narrative_a and narrative_b. Predict exactly one relation_type:
> same_route: both complaints were assigned to the same product family and the same issue route.
> same_family: both complaints were assigned to the same product family but different issue routes.
> different_family: the complaints were assigned to different product families.
> The labels are balanced, so robust solutions must distinguish fine-grained semantic concordance from broad topical concordance. Pair order carries no meaning: swapping narrative_a and narrative_b must not change the intended class.
> This is a CPU-only NLP challenge. Models must be trained or fitted only on the released training data. External record lookup and reconstruction of removed metadata are prohibited.
> What Makes This Task Distinct
> This is not a conventional single-narrative taxonomy-classification task:
> The prediction unit is a pair of independently authored narratives, not one complaint.
> The original broad and fine category names are absent from every released file.
> The target is a three-state hierarchical relation, not a product or issue label.
> Pair supervision does not identify the hidden category of either narrative individually.
> The relation is symmetric, so models should be invariant to pair orientation.
> Every narrative is used once, preventing train-to-test retrieval of repeated documents or reconstruction of a shared pair graph.
> Train and test contain balanced relation classes rather than the original collection's category frequencies.
> The intended modeling problem is latent hierarchy comparison under weak relational supervision: determine how deeply two texts agree without being shown the hidden nodes that produced that relationship.
> Dataset
> The released dataset contains three files:
> train.csv: 19,200 labeled narrative pairs.
> test.csv: 4,800 unlabeled narrative pairs.
> sample_submission.csv: 4,800 example prediction rows with exactly two columns, id and relation_type. It contains every test ID once and uses valid class-name placeholders to demonstrate the required output structure.
> Columns:
> id: string. Opaque unique pair identifier.
> narrative_a: string. First privacy-scrubbed consumer complaint narrative.
> narrative_b: string. Second privacy-scrubbed consumer complaint narrative.
> relation_type: categorical string. Training target, present only in train.csv.
> Every underlying narrative occurs in exactly one pair in the complete derived dataset, so no narrative is shared between training and test rows. Narratives are predominantly English and range from 160 to 4,000 characters after whitespace normalization.
> Evaluation
> The score uses two quantities computed over all test rows:
> macro_F1: calculate F1 separately for different_family, same_family, and same_route, then take their arithmetic mean.
> worst_class_F1: the lowest of those same three per-class F1 values.
> score = 0.75 * macro_F1 + 0.25 * worst_class_F1
> Both components are in the interval from 0 to 1. The formula is fully reproducible on any labeled validation split using the released training data. The worst-class term prevents a solution from obtaining a strong score by abandoning the most difficult relation class.
> The score is bounded from 0 to 1, and higher is better.
> Submission Format
> Submit a CSV with exactly these columns in this order: id, relation_type.
> Example:
> id,relation_type
> rel_0123456789abcdef,same_route
> rel_fedcba9876543210,different_family
> Requirements:
> Include exactly 4,800 prediction rows plus the header.
> Include every test id exactly once.
> Do not include duplicate or extra IDs.
> Use only same_route, same_family, or different_family.
> Do not include additional columns.
> Runtime and Modeling Rules
> The solution must run on CPU within 30 minutes.
> Fit all learned preprocessing and model parameters using train.csv only.
> Use test.csv only for final transformation and prediction.
> Do not use hosted inference services or network access.
> Do not use external datasets, removed category labels, external complaint archives, search engines, or narrative-to-record lookup tables.
> Do not reverse-map opaque IDs or narratives to records outside the released files.
> Do not use hidden/private answers or reconstruct removed metadata fields.
> General-purpose pretrained models are permitted only if already available through the runtime and used without network access, but they are not required.
> Data Context
> The text consists of real-world consumer financial-service complaint narratives released for research after privacy processing. The collection is observational and is not a statistical sample of all consumers or all experiences in financial markets. The class label describes agreement between hidden operational routing levels; it does not judge whether a complaint is true, severe, or legally valid. Formal provenance, attribution, and licensing are maintained separately in the dataset metadata and are intentionally omitted here to protect the integrity of the held-out evaluation.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Policy Role Continuation in EU Legislation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74psjpav6fzbgqpc2kh7kfns8bq27a
- DOMAIN exactly as displayed: NLP
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
> Policy analysts often code a document one policy-design span at a time. A useful assistant should not only recognize the current span's role; it should anticipate the next coding decision from the local legislative wording, the current role, and where the article currently is. Your task in this natural language processing challenge is to predict the canonical policy-design role bundle attached to the next annotated span in the same article.
> Every example comes from real legislative text and a human annotation sequence to challenge solver's skill to process natural language. The target is a bundle, not a free-form explanation. The public rows conceal document and article identifiers so that solutions must use the supplied language and structural features rather than memorizing document identity. Natural language processing techniques will be important here.
> Dataset
> File descriptions
> train.csv: labeled public examples for model development.
> test.csv: public examples from held-out legal instruments; the target column is omitted.
> sample_submission.csv: correctly shaped example submission with valid, non-constant bundle values.
> Column descriptions
> Each row in train.csv and test.csv contains:
> id: stable opaque identifier for the example.
> current_text: the current human-annotated span.
> context: up to 55 real legislative tokens immediately before the current span.
> current_bundle: the canonical role bundle assigned to the current span.
> position_fraction: the current event's normalized position in its article's retained event sequence.
> span_length: character length of the current annotated span.
> next_bundle: the target in train.csv only.
> The allowed atomic roles are Actor, Compliance, InstrumentType, Objective, Reference, Resource, Reversibility, and Time. A multi-role value joins distinct roles with |, in exactly that order.
> Evaluation
> For each example, the prediction and answer are parsed into sets of atomic roles. We compute an F1 score independently for each of the eight roles, average those eight values to obtain macro role F1, and also compute exact canonical-bundle accuracy. The final score is:
> score = 0.8  *macro_role_f1 + 0.2*  exact_bundle_accuracy
> The metric gives rare policy-design roles equal influence to frequent roles while retaining a practical reward for getting the whole operational bundle exactly right. It is bounded to [0, 1] and higher is better.
> Equivalent scoring logic is:
> roles = ["Actor", "Compliance", "InstrumentType", "Objective",
> "Reference", "Resource", "Reversibility", "Time"]
> macro_role_f1 = mean(
> f1(role_predictions[role], role_answers[role]) for role in roles
> )
> score = 0.8  *macro_role_f1 + 0.2*  mean(predicted == answer)
> Submission
> Submit one CSV file with exactly these columns:
> id: every test identifier exactly once.
> next_bundle: one valid canonical bundle for each test identifier.
> Example:
> id,next_bundle
> 00006fe8788d0593,Compliance|InstrumentType
> 0030510f230e12b6,Compliance|Resource
> 0041dcc414dfc6c1,InstrumentType|Reference
> Requirements
> Preserve the test row identifiers; do not add or remove rows.
> Use only the public files and ordinary computation available in the challenge environment.
> Return a non-empty canonical bundle made from the eight allowed roles.
> Separate co-occurring roles with | and keep them in canonical order.
> Your final file must be named submission.csv when submitted through the platform.
> What not to use
> Do not treat the opaque id as a document identity token or attempt to reverse it.
> Do not use any external label lookup, answer cache, or document-level mapping to recover the held-out bundles.
> Do not place the target bundle or a future annotated span into features.
> Do not assume that a random row split is valid: adjacent rows share article structure, while the evaluation examples come from unseen legal instruments.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Danish Lexical Relation Neighborhood

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74031n57bs9ceh1xjp8a65bn8c3brn
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Danish Lexical Relation Neighborhood
> 1. Overview
> Objective: For each test row, select the candidate Danish synsets that are semantic neighbours
> of the focus synset and predict the directed relation type connecting the focus to each selected
> candidate. The required output is one JSON relation bundle per test row.
> DanNet is a Danish lexical-semantic network, or wordnet. It groups words into synsets, which
> are sets of lemmas expressing a shared concept. A synset may include a Danish definition and usage
> examples. Typed links connect synsets. For example, a broader concept is a hypernym and a narrower
> concept is a hyponym. Other links describe parts, members, topics, agents, patients, and results.
> In this challenge, each row presents one focus card and 24 shuffled candidate cards. A
> card is a human-readable representation of a synset containing its lemmas, definition, examples,
> and an opaque ID. Most candidates may be distractors, so the model must perform both neighbour
> selection and relation-type prediction.
> This is useful for lexical-resource completion, dictionary navigation, semantic search, language
> understanding, and Danish NLP systems that need structured knowledge rather than only text
> similarity.
> 2. Task
> For every row in test.csv, predict zero or more directed, typed relations from the focus card
> to cards in that row's candidate list. Produce one JSON relation bundle for every test id.
> For example, if a candidate denotes a broader class of the focus concept, predict hypernym.
> If a candidate is merely a distractor, do not include it in relations.
> 3. Data files
> +-----------------------+--------------------------------------+-----------------------------+
> | File                  | Columns                              | Description                 |
> +-----------------------+--------------------------------------+-----------------------------+
> | train.csv             | id,focus_card_json,                  | Training inputs + gold      |
> |                       | candidate_cards_json,label           | relation bundles.           |
> | test.csv              | id,focus_card_json,                  | Prediction inputs only.     |
> |                       | candidate_cards_json                 |                             |
> | sample_submission.csv | id,prediction                        | Schema-valid weak example.  |
> +-----------------------+--------------------------------------+-----------------------------+
> The organizer also holds a private answers.csv file for grading. It is not a contestant input.
> All CSV files use UTF-8. JSON objects and arrays are stored as serialized text inside CSV cells.
> The id column is an opaque string and is the join key; row order has no meaning.
> 4. Input columns and card schemas
> id
> A unique opaque string identifying the row. Copy each test ID exactly into your submission.
> focus_card_json
> A JSON object describing the source synset:
> {
> "card_id": "w_80a18c2ace11a317",
> "lemmas": ["monument"],
> "definition": "bygningsvÃ¦rk, statue e.l. der er rejst for at Ã¦re â€¦",
> "examples": ["Et dansk brugseksempel."]
> }
> +------------+----------------+----------------------------------------+
> | Field      | JSON type      | Description                            |
> +------------+----------------+----------------------------------------+
> | card_id    | string         | Opaque ID of the focus synset.         |
> | lemmas     | array[string]  | One or more Danish words or expressions|
> |            |                | in the synset.                         |
> | definition | string         | Danish definition; it can be empty.    |
> | examples   | array[string]  | Zero to three Danish usage examples.   |
> +------------+----------------+----------------------------------------+
> candidate_cards_json
> A JSON array containing exactly 24 candidate objects in deterministic shuffled order. Each item
> has the following schema:
> {
> "candidate_id": "w_72135d38941f3188",
> "lemmas": ["bygningsvÃ¦rk"],
> "definition": "stÃ¸rre menneskeskabt konstruktion",
> "examples": []
> }
> +---------------+----------------+----------------------------------------+
> | Field         | JSON type      | Description                            |
> +---------------+----------------+----------------------------------------+
> | candidate_id  | string         | Opaque ID used when predicting a       |
> |               |                | relation to this candidate.            |
> | lemmas        | array[string]  | One or more Danish words or expressions|
> |               |                | in the candidate synset.               |
> | definition    | string         | Danish definition; it can be empty.    |
> | examples      | array[string]  | Zero to three Danish usage examples.   |
> +---------------+----------------+----------------------------------------+
> Candidate order is not informative. Some candidates are true neighbours; the rest are
> deterministic distractors.
> label in train.csv
> The training label is JSON text with exactly the same semantic schema required for a submitted
> prediction:
> {
> "relations": [
> {"candidate_id": "w_72135d38941f3188", "relation": "hypernym"},
> {"candidate_id": "w_f229139c4d15e292", "relation": "hyponym"}
> ]
> }
> relations is an array. Each object identifies a candidate from that row and its directed
> relation from the focus. An empty array means that no relation is predicted. Array order is not
> scored.
> 5. Relation vocabulary
> The relation string must be one of these 24 values:
> +--------------------------------------+----------------------------------------------+
> | Labels                               | Interpretation                               |
> +--------------------------------------+----------------------------------------------+
> | hypernym, hyponym                    | Broader-class and narrower-class relations.  |
> | instance_hypernym, instance_hyponym  | Instance-to-class and class-to-instance      |
> |                                      | relations.                                   |
> | similar, also                        | Similar-meaning and "also see" lexical links.|
> | domain_topic, has_domain_topic       | Topic-domain relation and its reverse.       |
> | mero_part, holo_part                 | Part-of and has-part directions.             |
> | mero_member, holo_member             | Member-of and has-member directions.         |
> | mero_substance, holo_substance       | Substance/material-of and has-substance      |
> |                                      | directions.                                  |
> | mero_location, holo_location         | Locative-part and containing-location        |
> |                                      | directions.                                  |
> | agent, patient, result               | Participant or result associated with an     |
> |                                      | event/action concept.                        |
> | involved_agent, involved_patient,    | Reverse-direction involvement links for      |
> | involved_result                      | agent, patient, and result roles.            |
> | co_agent_instrument,                 | DanNet's paired co-agent/instrument role     |
> | co_instrument_agent                  | links.                                       |
> +--------------------------------------+----------------------------------------------+
> Submission format
> Submit a UTF-8 file named submission.csv with exactly two columns in this order:
> id,prediction
> The file must contain exactly one row for every test.csv ID, with no missing, duplicate, or
> unknown IDs. Each prediction cell must be a valid JSON object containing a relations array of
> at most 100 objects. Every relation object must contain string fields candidate_id and
> relation. Use candidate IDs from the same test row.
> Here is a correctly CSV-escaped three-row example (header plus two predictions):
> id,prediction
> dan_example_001,"{""relations"":[{""candidate_id"":""w_72135d38941f3188"",""relation"":""hypernym""}]}"
> dan_example_002,"{""relations"":[]}"
> The example IDs are illustrative; your submission must use the actual IDs from test.csv.
> 7. Evaluation
> The final leaderboard value is the arithmetic mean of the row scores. Each row score is a
> weighted sum of five components and lies in [0,1].
> For any two sets P and G, set F1 is:
> F1(P,G) = 2 Ã— |P âˆ© G| / (|P| + |G|)
> If both sets are empty, F1 is 1; if exactly one is empty, F1 is 0.
> Let P be the predicted set of (candidate_id, relation) pairs and G the gold set.
> +-------------------------+--------+----------------------------------------------+
> | Component               | Weight | Exact row-level rule                         |
> +-------------------------+--------+----------------------------------------------+
> | Labelled-edge F1        | 50%    | F1(P,G) over complete (candidate_id,         |
> |                         |        | relation) pairs.                             |
> | Neighbour F1            | 20%    | Set F1 over candidate IDs after discarding   |
> |                         |        | relation labels.                             |
> | Relation-label macro-F1 | 15%    | Mean candidate-ID set F1 across each relation|
> |                         |        | label appearing in the gold set.             |
> | Consistency             | 10%    | 1 if no candidate ID occurs more than once;  |
> |                         |        | otherwise 0.                                 |
> | Bundle validity         | 5%     | 1 if all predicted pairs are unique and both |
> |                         |        | strings in every pair are non-empty; else 0. |
> +-------------------------+--------+----------------------------------------------+
> These two checks enforce different constraints. Consistency requires every candidate_id to
> appear at most once, regardless of relation label. Bundle validity requires every complete
> (candidate_id, relation) pair to be unique. Therefore, predicting the same candidate_id twice
> with two different relation labels fails Consistency but does not, by itself, fail Bundle validity;
> repeating the identical candidate-and-relation pair fails both checks.
> Thus:
> row_score = 0.50 Ã— labelled_edge_F1
> + 0.20 Ã— neighbour_F1
> + 0.15 Ã— relation_label_macro_F1
> + 0.10 Ã— consistency
> + 0.05 Ã— bundle_validity
> final_score = mean(row_score over all test rows)
> An exactly correct relation set receives 1.0 for the row. Invalid JSON, a non-object prediction,
> a missing relations field, wrong field types, or more than 100 relation objects receives 0 for
> that row. A malformed row does not invalidate other correctly formatted rows. At file level, a
> wrong column set, duplicate ID, missing ID, unknown ID, or wrong row count makes the entire
> submission score 0.
> 8. Split integrity
> The organizer assigns every synset to a partition before constructing rows. Relations crossing
> the partition boundary are excluded, and distractors are drawn only from the focus partition.
> Cards with identical lemmas, definitions, and examples are co-located. Consequently, train and
> test share neither opaque card IDs nor complete card text, which prevents reconstruction of hidden
> relations through repeated synsets. Opaque identifiers also prevent direct use of upstream DanNet
> IDs.
> 9. Runtime and allowed resources
> The complete training and inference run must finish within 90 minutes using at most 10 CPU cores
> and 62 GB RAM. GPU access and network access are unavailable.
> Use only the supplied public challenge files and packages already installed in the execution
> environment. Do not install packages during the run or use:
> external wordnets or dictionaries;
> remote translation, language-model, or other web APIs;
> hidden DanNet identifiers or organizer-only files;
> manually encoded answer tables; or
> GPU-only models.
> A learned or algorithmic model must be central to the solution.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Oral History Turn Splice Reranking

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74kd0y0y64tb81h3tzbesr458c194c
- DOMAIN exactly as displayed: NLP
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
> Three turns have fallen out of an oral-history transcript. Twelve authentic-looking turns, labeled A through L, are available for repair. Select the turn for each gap and emit the three placements in transcript order.
> This is a constrained reranking task, not open-ended generation. The solver must choose three turns from a fixed candidate list and place them into the correct gaps. Real oral-history archives can lose individual lines when transcript pages are merged, OCR is corrected, or annotations are transferred between formats. Nearby turns provide incomplete evidence because informal conversation contains interruptions, short acknowledgements, topic shifts, and unfinished statements.
> Nine of the twelve candidates are authentic turns from elsewhere in the same recorded conversation. They sound natural in isolation and often share the same speakers and topics. The challenge is to use discourse evidence such as question-answer structure, reference continuity, speaker response, and local topic flow rather than generic sentence fluency.
> Some contexts also contain [WITHHELD_NON_TARGET]. This marker denotes a turn reserved as the answer to a different hidden case. It is not one of the three gaps to solve and has no corresponding submission operation. Reserving these turns prevents one hidden answer from being exposed as ordinary context elsewhere in the public test set.
> Dataset
> The prepared data contains 2,200 training cases and 350 test cases. Contiguous 72-turn source blocks are assigned to one partition before cases are created. Public identifiers are opaque hashes and do not preserve conversation, page, line, or generation order.
> Test construction uses a reservation pass before any public packets are written. Its three answer turns are unique to that test row. The same normalized text cannot appear in another test row's visible context, in another test row's candidate list, or anywhere in public training text. When a reserved turn falls inside another test context window, it is replaced by [WITHHELD_NON_TARGET]. The preparation script validates these conditions and aborts if any exposure is found.
> Files
> | Path | Description |
> |---|---|
> | `train.csv` | Transcript packets, candidate packets, and the correct splice program. |
> | `test.csv` | Transcript and candidate packets with the splice program withheld. |
> | `sample_submission.csv` | Schema-valid fixed prediction. |
> Columns
> | Column | Data type | Availability | Description |
> |---|---|---|---|
> | `case_id` | string | train and test | Opaque case identifier. |
> | `context_packet` | JSON array of 13 strings | train and test | Ordered local turns containing exactly the three numbered gaps. Test rows can additionally contain `[WITHHELD_NON_TARGET]` markers, which require no prediction. |
> | `candidate_packet` | JSON array of objects | train and test | Twelve objects with an `id` from `A` through `L` and a candidate `turn` string. |
> | `splice_program` | canonical string | train only | Three gap assignments in `g1`, `g2`, `g3` order, joined by a single `>` character. |
> Transcript Language And Turn Content
> All transcript turns are written in informal spoken German from naturally occurring youth conversations recorded in Cologne. The collection includes conversations among multilingual speakers, monolingual speakers, and a mixed group. In this context, multilingual describes the speakers' linguistic backgrounds; the prepared turn text is not a parallel translation corpus and does not switch between six labeled transcript languages.
> A turn is one continuous contribution by a speaker after consecutive transcript lines from that same speaker have been joined. Turns range from short responses such as ach so, ja genau, or nee gar nich to longer fragments describing events or answering questions. They can contain colloquial spelling, discourse particles, repetitions, unfinished clauses, laughter or pause notation, overlap markers, and masked or unintelligible material inherited from the conversation transcript. Candidate and context strings therefore represent spontaneous dialogue rather than edited written German.
> Speaker identifiers and original transcript line numbers are not included in the public packets. Solvers must infer placement from the wording and local discourse sequence available in context_packet and candidate_packet.
> Example input:
> | Field | Example JSON value |
> |---|---|
> | `context_packet` | `["ach so","[GAP_1]","ja genau","[WITHHELD_NON_TARGET]","[GAP_2]","und dann","[GAP_3]"]` |
> | `candidate_packet` | `[{"id":"A","turn":"nee gar nich"},{"id":"B","turn":"ich weiÃŸ"}]` |
> The real candidate packet always contains all twelve labels, even though the shortened example shows two.
> Submission Format
> Write the final file to ./working/submission.csv.
> The file must contain exactly two string columns in this order: case_id, then splice_program.
> | case_id | splice_program |
> |---|---|
> | `dlg_0123456789abcdef0123` | `g1:H>g2:C>g3:K` |
> The program grammar is g1:X>g2:Y>g3:Z, where X, Y, and Z are three distinct candidate letters from A through L. The single > character separates operations. In the example above, candidate H fills the first gap, C fills the second, and K fills the third.
> Programs may contain at most 32 characters. They must contain three operations separated by single > characters, use gap numbers in ascending order, use candidate letters A through L, and use three distinct candidates.
> Evaluation
> The Oral History Turn Splice Score combines exact recovery with two partial-credit checks.
> The final formula is Score = 0.50 * ExactProgramScore + 0.35 * ChanceCorrectedGapScore + 0.15 * OrderScore.
> ExactProgramScore
> For each case, this value is 1 only when all three gap assignments are correct and 0 otherwise. The component is the mean over test cases.
> ChanceCorrectedGapScore
> Let a_i be the fraction of the three gaps assigned the correct candidate. A random candidate has probability 1/12 of matching a gap. For each case, gap_i = max(0, (a_i - 1/12) / (1 - 1/12)). The component is ChanceCorrectedGapScore = mean(gap_i) over all test cases.
> OrderScore
> Order credit is available only when the submitted candidate set is exactly the correct three-candidate set. The three candidate pairs are checked for the correct relative gap order. Let r_i be the fraction of those pairs in the correct order. When the candidate sets match, order_i = max(0, 2 * r_i - 1). Otherwise, order_i = 0. The component is OrderScore = mean(order_i) over all test cases.
> A malformed program receives zero for every component on that case. Minimum score: 0.0. Maximum score: 1.0. Higher is better.
> Archival Consequence
> The benchmark measures whether a model can rerank real conversational turns under discourse constraints rather than continue text generically. Correct placement may depend on question-answer relations, pronoun reference, lexical reprise, repair structure, or a speaker responding to an earlier interruption. The distractors remain natural conversation from the same recording, which makes surface fluency an unreliable shortcut.
> The framing is intentionally different from ordinary cloze completion: no new text is generated, distractors are source-real turns, and scoring separately measures exact placement, per-gap recovery, and relative ordering of the selected turns.
> Discourse Models
> Suitable CPU methods include multilingual sentence embeddings, BM25-style retrieval, compact cross-encoders, discourse-marker features, speaker-turn language models, and constrained reranking. Validation should preserve contiguous source blocks and should never construct adjacency evidence from other hidden rows.
> What Not To Use
> The splice program must follow these transcript-integrity rules:
> Do not identify source pages or transcript line numbers through external phrase search.
> Do not map public text back to an external copy of the conversation or its transcript.
> Do not derive answers from opaque IDs, row order, JSON order outside the documented semantics, or hidden split artifacts.
> Do not exploit malformed submissions, missing rows, duplicate IDs, extra columns, or grader behavior.
> Do not use private answers or leaderboard probing as labels.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Composite Reprint Provenance Segmentation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70z34a7ng4yn8n7wmxca6r2d8c1gb5
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Historical newspapers often carried locally edited versions of syndicated reports. This challenge asks you to identify the sources of a damaged composite passage and locate the single point where its provenance changes.
> Every case provides twelve ordered query_blocks and six aligned candidate versions. The candidates form three authentic reprint pairs from six distinct newspaper titles. The opening query blocks come from one candidate, and the closing blocks come from a candidate in a different pair. Each true contributor therefore has a close same-story rival among the candidates.
> Each query block contains one short position-free word fragment sampled from its contributor and passed through a noisy many-to-one glyph channel. Every case independently draws its full character-to-glyph mapping and the names of the eight glyph symbols, so neither a glyph such as a nor a source-letter grouping has stable cross-case identity. One latent channel is shared by all twelve query blocks inside a case. Candidate blocks contain normalized historical OCR. Literal matching and any cross-case substitution table are intentionally weak; the task requires joint case-local channel fitting, word alignment, and structured one-switch decoding.
> Every test case has a new glyph mapping that must be inferred from that case. The complete solution must run offline on CPU and write ./working/submission.csv.
> Rules
> You may:
> use all files in the public dataset directory;
> train or fit models from scratch on train.jsonl;
> use validation.jsonl for calibration and model selection; and
> use Python and packages already available in the execution environment.
> You may not:
> use pretrained weights, pretrained models, external embeddings, or external tokenizers;
> use external datasets, external corpora, source lookup, or manual answer lookup;
> access the internet, make network requests, call external APIs, or download files;
> install additional packages; or
> read private challenge files or hidden labels.
> Dataset
> The public directory contains:
> encoder_spec.json - deterministic normalization, latent-channel scope, candidate-pair structure, and permitted training contract.
> train.jsonl - labeled model-training cases.
> validation.jsonl - labeled schedule-selection cases.
> test.jsonl - unlabeled provenance-segmentation cases.
> dataset_summary.json - split sizes, cluster counts, and preparation version.
> sample_submission.csv - a valid all-abstention submission.
> Each JSONL case contains:
> case_id - an opaque identifier matching Q[0-9A-F]{16}.
> query_blocks - exactly twelve degraded text strings in reading order.
> candidates - exactly six case-local candidate objects in display order.
> target - present only in train.jsonl and validation.jsonl.
> Each candidate object contains a candidate_id from P0 through P5 and exactly twelve aligned authentic OCR blocks. Candidate IDs have no identity outside their own case. Display order is deterministically shuffled and does not encode provenance.
> Each labeled target contains left_candidate_id, right_candidate_id, and switch_block. The two candidate IDs are distinct. switch_block is an integer from 1 through 11: blocks with zero-based indices below it come from the left candidate and all remaining blocks come from the right candidate.
> Train, validation, and test are disjoint by the underlying story-reuse components. Source titles, dates, locations, issue numbers, archive positions, and source identifiers are not public.
> Evaluation
> A submitted ordered candidate pair and switch imply one provenance label for every query block. For block index i, the predicted label is left_candidate_id when i < switch_block and right_candidate_id otherwise. The case score is the fraction of the twelve predicted labels equal to the authentic block provenance. The final score is the mean case score over the hidden test set.
> One case is one evaluation unit. Its twelve block labels are jointly determined by the same left candidate, right candidate, and switch triple; the blocks are not twelve independent leaderboard examples.
> Scores are maximized and lie in [0, 1]. An exact oracle scores 1. The exact abstention row ABSTAIN,ABSTAIN,-1 scores 0 for that case.
> Submission
> Write ./working/submission.csv with exactly these columns in this order:
> case_id,left_candidate_id,right_candidate_id,switch_block
> Include every test case_id exactly once. A non-abstaining row must contain two distinct IDs from P0 through P5 and an integer switch from 1 through 11. To abstain, use the exact triple ABSTAIN,ABSTAIN,-1.
> Example non-abstaining row:
> Q0123456789ABCDEF,P4,P1,7
> Wrong columns, missing or extra cases, duplicate case IDs, missing values, malformed IDs, leading or trailing whitespace, identical candidate IDs, unknown candidates, nonintegral switches, partial abstentions, and switches outside the allowed range are rejected.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Literary Graph Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx726x7ccpbfccsrj1dd9z6rfx8c5svt
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat killshark's score of 0.722!

Full challenge description from page:

> Leaderboard
> (19)
> Your Submissions
> Literary Graph Reconstruction
> 1. Overview and real-world context
> Literary works describe people, places, actions, and dialogue across long narrative contexts. A useful literary-analysis system must do more than identify isolated names: it must determine which mentions refer to the same character, which words express events, and who speaks each quotation. These connected predictions form a discourse graph that can support character-network analysis, digital-humanities research, quotation indexing, narrative search, reading-assistance tools, and training data for document-level information extraction.
> This challenge is derived from LitBank, a corpus of public-domain English literary fiction with expert linguistic annotations. The packaged source combines LitBank-style entity, event, coreference, and quotation-attribution layers. Character offsets and quotation coordinates are aligned to one shared tokenization, then converted into bounded passages. No model-generated labels are used.
> Your objective is to reconstruct a joint graph for every unseen passage by predicting:
> typed entity-mention spans;
> event-trigger spans;
> coreference links between entity mentions; and
> quotation spans linked to their speakers.
> The hidden partition contains complete works that are absent from training. Overlapping passages from one work never occur in both partitions. A successful model must therefore generalize across authors, character inventories, narrative voices, historical spelling, and dialogue styles.
> 2. Dataset scale and split
> The deterministic prepared dataset contains 1,719 passages from 99 usable literary works.
> Partition	Passages	Literary works	Labels available
> Training	1,391	79	Yes
> Test	328	20	No
> Train/test work overlap is zero. Passages contain 48–176 tokens. The training labels contain 33,977 entity mentions, 10,399 event triggers, 20,150 coreference chain edges, and 1,991 attributed quotations.
> 3. Data files
> train.csv
> The training file contains four columns:
> Column	Data type	Meaning
> id	UTF-8 string	Unique opaque passage identifier. It carries no title or author information.
> tokens_json	JSON-encoded array<string>	Passage tokens in reading order. Every target span indexes this array.
> sentence_breaks_json	JSON-encoded array<integer>	Exclusive sentence-end token offsets. The last offset equals the passage length.
> label	JSON-encoded object	Gold graph containing the four target arrays described in Section 4.
> test.csv
> The test file contains id, tokens_json, and sentence_breaks_json with exactly the same types and meanings as in training. It has no label column.
> sample_submission.csv
> This file contains all test IDs and schema-valid empty graph objects. It demonstrates CSV and JSON escaping only; it is deliberately noncompetitive.
> 4. Annotation and target schema
> All spans are zero-based, half-open token intervals [start,end). The token at start is included and the token at end is excluded. For example, [3,5) selects tokens 3 and 4.
> The label object and every submitted prediction object require exactly these target fields:
> Field	Explicit type	Meaning
> entities	array<[integer,integer,string]>	Typed mention spans [start,end,type].
> events	array<[integer,integer]>	Event-trigger spans [start,end], usually verbs or event-denoting words.
> coref_edges	array<[integer,integer]>	Undirected links between indices in that row's entities array. Linked mentions refer to the same discourse entity.
> quote_speakers	array<{quote:[integer,integer],speaker:integer}>	A quotation span and the index of its speaker in that row's entities array.
> Entity types
> Type	Meaning	Typical example
> PER	Person or character	Elizabeth, the doctor
> FAC	Facility or constructed place	the house, the station
> LOC	Non-geopolitical location	the forest, the river
> GPE	Country, city, or geopolitical area	England, London
> VEH	Vehicle	the carriage, the ship
> ORG	Organization or organized group	the council, the army
> COREF_MENTION	A coreference endpoint without a separate entity-layer type	pronouns such as she, him, or they
> COREF_MENTION exists because pronouns and other referring expressions can be essential to a coreference chain even when they are not annotated as named/entity-layer mentions.
> Relation conventions
> A coreference edge [a,b] refers to entries entities[a] and entities[b].
> Coreference edges are undirected and should be supplied once.
> Each gold cluster is encoded compactly as a deterministic chain over its mentions, not as every possible mention pair.
> A quote's speaker is also an index into the submitted entities array.
> At most one speaker should be submitted for a given quote span.
> Relation scoring uses the entity spans and types selected by the submitted indices. Correct-looking indices attached to incorrect entities receive no relation credit.
> Example decoded graph:
> {
> "entities": [[3, 5, "PER"], [18, 19, "COREF_MENTION"]],
> "events": [[7, 8]],
> "coref_edges": [[0, 1]],
> "quote_speakers": [{"quote": [9, 17], "speaker": 0}]
> }
> 5. Submission format
> Upload one UTF-8 CSV named submission.csv with exactly two columns in this order:
> id,prediction
> CSV example (JSON quotation marks are doubled according to CSV escaping rules):
> id,prediction
> lrg_0123456789abcdef0123,"{""entities"":[[3,5,""PER""],[18,19,""COREF_MENTION""]],""events"":[[7,8]],""coref_edges"":[[0,1]],""quote_speakers"":[{""quote"":[9,17],""speaker"":0}]}"
> Submission requirements:
> include exactly one row for every ID in test.csv;
> copy every ID unchanged;
> use exactly the columns id,prediction in that order;
> include all four required prediction fields, even when an array is empty;
> use finite standard JSON—NaN and Infinity are forbidden;
> keep every span within the passage and every relation index within the submitted entity list.
> A missing or extra column, missing ID, unknown ID, duplicate ID, or incorrect row count makes the entire file score 0.0. Invalid JSON or an invalid graph schema contributes no predicted items for that row but does not crash or invalidate other correctly formatted rows.
> 6. Evaluation metric
> The score is computed over all test passages using corpus-level multiset micro-F1. For each extraction component:
> [
> F_1 = \frac{2TP}{|P|+|G|},
> ]
> where P is the multiset of submitted items, G is the multiset of gold items, and TP is the size of their multiset intersection. Items are tagged by row ID before pooling. Duplicate predictions therefore increase |P| and are penalized. Empty gold arrays do not award true-negative credit.
> Component	Weight	Exact comparison item
> Typed entities	20%	(row_id,start,end,type)
> Events	20%	(row_id,start,end)
> Coreference	30%	(row_id,unordered_typed_endpoint_span_pair)
> Quote attribution	25%	(row_id,quote_span,typed_speaker_span)
> Graph integrity	5%	Formula below
> Exact graph-integrity formula
> For each valid predicted row, define six values in [0,1]:
> U_entities = number of unique entity records / number of entity records;
> U_events = number of unique event records / number of event records;
> U_edges = number of unique coreference edges / number of coreference edges;
> U_quotes = number of unique quote-speaker records / number of quote-speaker records;
> C_edges = fraction of canonicalized edges whose first entity index is smaller than the second;
> F_quotes = number of unique quote spans / number of quote-speaker records.
> When the relevant array is empty, its ratio is defined as 1. An invalid row has integrity 0. The row integrity is
> [
> I_r = \frac{U_{entities}+U_{events}+U_{edges}+U_{quotes}+C_{edges}+F_{quotes}}{6}.
> ]
> Let mean(I) be the arithmetic mean across all test rows, and let F_entity and F_event be the corpus micro-F1 values. The reported graph-integrity component is gated by successful node recovery:
> [
> I = mean(I)\sqrt{F_{entity}F_{event}}.
> ]
> Thus a structurally tidy but empty prediction receives no integrity credit.
> The final score is
> [
> Score = 0.20F_{entity}+0.20F_{event}+0.30F_{coref}+0.25F_{quote}+0.05I.
> ]
> The score is clipped to [0,1]. A canonical perfect submission scores exactly 1.0; the supplied empty sample scores 0.0.
> 7. Execution and usage constraints
> The complete training and inference pipeline must finish within 90 minutes using at most 10 CPU cores and 62 GB RAM. Network access, remote model APIs, external copies of the books or annotations, reconstruction of hidden titles or upstream identifiers, and GPU-only solutions are prohibited. Use only the released data and packages already installed in the execution environment.
> 8. Why this challenge is difficult
> Entity boundaries and types must be correct before their coreference or quotation relations can receive credit. The two relation tasks account for 55% of the score. The complete-work split prevents memorizing characters across overlapping passages, while corpus-level micro-F1 prevents empty or relation-free examples from inflating performance. Strong solutions must combine local syntax, narrative context, mention detection, event extraction, cluster reasoning, and quotation attribution.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Line-Level Fix Prediction For Rejected Submissions

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78m2vj4zpynb4sv2dpvrd99d8bvwax
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top score: 0.288

Full challenge description from page:

> Background
> Each item is the raw source code of a program that a person submitted to an automated programming judge and that the judge rejected — the program compiles and runs to completion, but it produces a wrong answer, runs too slowly (time-limit exceeded), or hits a runtime error. You are also given the natural-language statement of the problem the program was trying to solve.
> The program contains a small logic mistake. The author later fixed it, changing only a few lines, and the fixed version was accepted. Your job is to find the mistake statically: you do not get the failing input, an execution trace, or a compiler error (the program already compiles and runs). The wrong line looks almost exactly like its correct neighbours — a flipped comparison, an off-by-one bound, the wrong variable, a +/- swap — so locating it requires reasoning about the whole program in the context of the problem.
> Task
> For each test program, predict the set of 1-indexed line numbers of that program that were modified or deleted to fix the bug. A line is labelable if it is non-blank; only labelable lines can be part of the answer, and predictions on blank lines are ignored.
> Files
> The dataset contains the following files.
> train.csv — one row per training program. Columns:
> id (string): unique identifier of the program; also the basename of its code and statement files.
> lang (string): the programming language, either Python or C++.
> label (string): space-separated 1-indexed line numbers of train/<id>.txt that were changed to fix the bug (the supervision signal). May contain one to three numbers.
> train/<id>.txt — the buggy source code of training program <id> (UTF-8 text, one program per file; lines are 1-indexed top to bottom).
> train/<id>.stmt.txt — the natural-language problem statement for training program <id>.
> test.csv — one row per test program. Columns:
> id (string): unique identifier of the test program.
> lang (string): the programming language, either Python or C++.
> test/<id>.txt — the buggy source code of test program <id> (labels withheld).
> test/<id>.stmt.txt — the natural-language problem statement for test program <id>.
> sample_submission.csv — a correctly-formatted example submission (see below).
> The training and test programs come from disjoint problems: no problem in the test set appears in training, so the task rewards generalizing bug-localization reasoning rather than memorizing problem-specific code.
> Submission format
> Produce a CSV with a header row and exactly two columns:
> id (string): the test program id. Every id in test.csv must appear exactly once.
> lines (string): space-separated 1-indexed line numbers you predict were changed. May be empty (which scores zero for that program).
> Example (matching sample_submission.csv):
> id,lines
> s0f1e2d3c4b5a6f7,4
> s9a8b7c6d5e4f3a2,12 13
> s1c2d3e4f5a6b7c8,
> Evaluation
> Submissions are scored with a precision-weighted micro F-score (F₀.₅) pooled over all labelable lines of the whole test set. With TP = predicted lines that were truly changed, FP = predicted lines that were not, and FN = truly-changed lines that were missed:
> precision = TP / (TP + FP)
> recall    = TP / (TP + FN)
> F0.5      = 1.25 * precision * recall / (0.25 * precision + recall)
> Predicted lines outside a program's labelable (non-blank) set are discarded before scoring. Because the score weights precision over recall (β = 0.5), over-flagging is penalized — blanketing a file with guesses collapses precision and the score. An empty submission scores at the metric floor.
> Rules
> CPU only; no GPU; no internet at run time.
> Notes
> Labels are derived from real human fixes and are therefore mildly noisy; a small number of changed lines may reflect incidental edits. Bug difficulty ranges widely — from a single wrong operator to a multi-line rework — which is reflected in the spread of achievable scores.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Grant Award-Size Bracket Prediction from Descriptions

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7aq1cry5e682hnasq0nvpbk98a1bkz
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, generative, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.654

Full challenge description from page:

> Grant Award-Size Bracket Prediction from Descriptions
> Overview
> Every funded grant has an award amount, but here that amount is hidden. You are given
> only a free-text description of what the grant funds — and every number and spelled-out
> dollar figure has been reduced to a single placeholder, so neither the figure nor its
> magnitude survives. Your job is to place each grant into one of
> four ordered award-size brackets (0 = smallest funding … 3 = largest) from the
> wording alone. Because the amount itself is never shown, you must infer scale from the
> kind of grant and its program language — a genuinely under-determined, ordinal
> prediction problem.
> Task
> For every item in test.csv, read the redacted description and output its
> award-size bracket as an integer 0, 1, 2, or 3 in the bracket column.
> Brackets are quartiles of the true award amount over the whole collection, so the
> four classes are roughly equal in size (~25% each). Bracket order is meaningful:
> 0 < 1 < 2 < 3 in funding size.
> Why it is hard
> The amount is not in the text. Each number — and each dollar figure — is
> collapsed to a single # / $# placeholder (not one # per digit, so the
> placeholder length reveals nothing about the amount's size) and spelled-out dollar
> amounts ("one thousand dollars") are removed, so you cannot read the figure or its
> magnitude off the page. Left un-redacted, most descriptions literally contain the
> award value and the task is trivial; with it removed, only the grant type and
> program vocabulary remain.
> Scale is loosely constrained. Within the modest funding range these grants span,
> wording pins the bracket only partially — a "community youth arts" line and a
> "regional infrastructure" line skew small and large respectively, but many
> descriptions are ambiguous.
> What remains is real but bounded signal. A bag-of-words model reaches
> QWK ≈ 0.44 on held-out grants (majority-guess QWK = 0.00). A model with
> stronger language understanding does better, but the missing amount keeps agreement
> well below 1.0.
> Data
> Three files are provided. Each row is one grant, keyed by id.
> train.csv — labelled items, with three columns — id, description, and
> bracket (the label):
> test.csv — items to solve: the same id and description columns, without the
> bracket label.
> sample_submission.csv — a valid submission in the exact required format (predicts the
> most common training bracket for every item, which scores QWK ≈ 0.00 because it makes
> no distinctions). See Submission Format below.
> Text characteristics. description is English free text describing what a grant
> funds, drawn from an openly-licensed collection of grant-program descriptions. Each is
> typically one short paragraph — a median of about 75 words (~515 characters), with
> most falling between ~35 and ~125 words. Each number — and each dollar figure — has
> been collapsed to a single # / $# placeholder (one token per figure, not one #
> per digit) and spelled-out dollar amounts (e.g. "one thousand dollars") removed, so
> neither the award figure nor its magnitude remains in the text. A representative row
> reads:
> "Funds are unrestricted and can cover any education-related expense including tuition,
> books, transportation, childcare and more."
> (Where the original text contained a number — for example an award figure or a year —
> the whole number is shown as a single # (a dollar figure as $#), regardless of how
> many digits it had; the sentence above happens to contain none.)
> Grants are split so the grants in the test set never appear in training; brackets are
> computed from the same quartile edges across the whole collection (~25% of items per
> bracket).
> Worked example
> A description like Support for a summer reading program at a rural public library
> tends to fall in a lower bracket; Establish a shared core facility for regional research groups tends to fall in a higher one. The challenge is that the exact figure
> is invisible and many descriptions do not signal their scale, so the four brackets are
> only partly separable from the words.
> Submission Format
> A CSV with exactly two columns, in this order:
> Exactly one row per id in test.csv, no duplicates.
> bracket is an integer in {0, 1, 2, 3}. Out-of-range or unparseable values are
> clamped to the nearest valid bracket (unparseable → 0).
> A valid submission looks exactly like this (matching sample_submission.csv, which
> predicts the most common training bracket for every row):
> id,bracket
> 3f9a1c07b2e45d68,2
> a01d7e4b9c3f2016,0
> 7c2b8f13a6d09e45,3
> d48e0a5f1b7c2639,1
> b6103e9a4c8d2f57,2
> Here the first data row assigns item 3f9a1c07b2e45d68 to bracket 2, the second
> assigns a01d7e4b9c3f2016 to bracket 0, and so on — one line per test item, header
> included.
> Evaluation
> Metric — Quadratic-Weighted Kappa (QWK). QWK measures ordinal agreement between the
> predicted and true brackets, corrected for chance. It rewards being close on the
> ordinal scale — predicting bracket 2 when the truth is 3 costs far less than predicting 0
> — and penalises each disagreement by the squared bracket distance.
> How it is computed. With K = 4 ordered brackets (0, 1, 2, 3) over N scored test
> items:
> **Observed matrix O** (size K×K): O[i][j] = the number of items whose true bracket is i and predicted bracket is j.
> **Weight matrix W** (size K×K): W[i][j] = (i − j)² / (K − 1)² — here (K − 1)² = 9. A correct prediction (i = j) has weight 0; the largest possible error (|i − j| = 3) has weight 1.
> **Expected matrix E** (size K×K): E[i][j] = (r[i] × c[j]) / N, where r[i] is the number of items with true bracket i and c[j] the number predicted j — i.e. the
> agreement expected if predictions were independent of the truth.
> Kappa is one minus the ratio of observed to expected weighted disagreement:
> QWK = 1 − ( Σ_ij  W[i][j] · O[i][j] )
> / ( Σ_ij  W[i][j] · E[i][j] )
> (both sums run over all i, j in 0..K−1).
> The result is **clamped to [0, 1]**: 1.0 is perfect agreement, 0.0 is chance-level,
> and below-chance (negative) agreement floors at 0.0. A malformed, missing, or
> out-of-range predicted bracket is coerced to the nearest valid class (unparseable → 0)
> before scoring, so it still counts as a (usually wrong) ordinal prediction.
> Reference points. Majority-guessing (one constant bracket for every item) scores
> 0.00; a bag-of-words baseline scores ≈ 0.44. The ceiling stays well below 1.0
> because the redacted amount under-determines the exact bracket.
> Approaches
> Learn the description→bracket mapping from the training labels — an ordinal or
> multi-class text classifier, or a model that reasons about the likely scale of a
> grant from its purpose and program language.
> Because the metric is ordinal, calibrating predictions toward the correct region
> (rather than betting on a single class) helps QWK even when the exact bracket is
> uncertain.
> Validate locally by holding out a slice of training items and computing QWK.
> What Not To Use
> Do not attempt to identify the source grant records and look up their award
> amounts from any external database, funder portal, or search engine. The amount is
> removed on purpose so the task is inferring scale from wording, not retrieving it.
> Do not hard-code answers. The intended solution generalises to unseen grants.

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## DerogationRelay: Exception-to-Obligation Binding

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75xd5q0gbkdaaxt75bg9mbe18ds9e7
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.989

Full challenge description from page:

> Overview
>
> EU legislation frequently displaces a general rule with “by (way of) derogation from ...” or “notwithstanding ...”. A sentence can also contain article numbers in its heading, later supporting citations, and qualifications such as “without prejudice to”. Those references are not necessarily governed by the exception operator.
>
> This challenge asks for clause-reference adjudication. Each row supplies one masked exception clause and one proposed locator. Decide whether that locator is inside the operator's immediate syntactic complement, reconstruct the complete ordered locator set that is inside the complement, emit a binding edge only for a governed proposal, classify the operator, and classify the proposed provision's modality.
>
> The frozen raw EUR-Lex snapshot is unchanged. Public identifiers are opaque and explicit article and paragraph references in clauses are replaced with [binding].
>
> Prediction Targets
>
> For every test row submit exactly:
>
> Column	Required value
> example_id	The test identifier.
> scope_verdict	governed or outside_operator_scope.
> governed_locators_json	Ordered JSON list of all governed [article_id, paragraph_token] locators. Use "" for article scope.
> proposed_binding_edge_json	[source_article_id, target_article_id, scope] for a governed proposal, otherwise [].
> operator_class	derogation or notwithstanding.
> proposed_modality	Modality of the proposed provision, whether or not it is governed.
>
> Modalities are prohibition, mandatory, permission, definition_or_scope, and other, with precedence in that order. Paragraph proposals are classified from the paragraph text; article proposals use the full article.
>
> Construction
>
> The preparation script independently parses the complement immediately following by derogation from, by way of derogation from, or notwithstanding. It stops at the complement-closing comma or a separate qualification introduced by forms such as without prejudice to, subject to, provided that, or in the case of. Only locally resolvable Article and paragraph locators in that span enter gold. Coordinated references retain textual order and numeric paragraph ranges are expanded.
>
> Every eligible clause produces six distinct proposal rows:
>
> one row for each distinct governed locator;
> resolvable references elsewhere in the same sentence, in textual order, as hard negatives; and
> deterministic same-act article or paragraph locators as additional decoys.
>
> No proposal locator repeats within a clause. The six rows share clause context but pose different decisions; they are not candidate-order or masking replicas. Every row also requires reconstruction of the entire governed set, preventing the binary verdict from being the sole task.
>
> Dataset
>
> Preparation creates 276 train rows from 46 clauses and 72 test rows from 12 clauses. Train and test use disjoint complete legal acts: 12 train acts and six test acts. Each clause contributes exactly six rows and stays wholly within one split.
>
> Public file	Rows	Contents
> train.csv	276	Eight inputs and five targets.
> test.csv	72	The same eight inputs; no target columns.
> article_corpus.csv	967	Masked article and paragraph cards.
> sample_submission.csv	72	Structurally complete target-only baseline.
> task_vocabulary.json	1 object	Counts and allowed labels.
>
> Input columns are example_id, clause_id, source_article_id, masked_exception_clause, candidate_article_ids_json, proposed_locator_json, operator_vocabulary_json, and verdict_vocabulary_json. Each candidate list contains 32 distinct article IDs and includes every governed and proposed article. clause_id groups the six distinct adjudications for one clause.
>
> The article corpus provides article_id, act_token, masked_heading, masked_text, paragraph_cards_json, resource_type, and relative_year. A paragraph card contains an opaque paragraph_token and its masked text.
>
> Evaluation
>
> The score is the mean row score in [0,1]. Each row has 100 points:
>
> 25  correct scope verdict  
> 20  governed-locator set F1  
> 15  exact ordered governed-locator list  
> 15  exact proposed edge (including correct empty edge)  
>  8  correct operator  
>  7  correct proposed modality  
>  5  internally coherent verdict/edge structure  
>  5  exact joint prediction  
>
> Locator F1 is 2 * |gold intersection prediction| / (|gold| + |prediction|). Exact ordered retrieval distinguishes reference order. Coherence requires one three-field edge for governed and [] for outside_operator_scope. Malformed JSON or labels lose affected components for that row. An incorrect global column schema, missing/extra IDs, duplicate IDs, or empty submission scores zero. Exact gold scores 1.0.
>
> Why This Metric Measures The Task
>
> The weighting follows the decisions required to bind an exception clause to the rule it displaces. Seventy-five of the 100 points measure binding itself. The scope_verdict receives 25 points because the primary legal-reading decision is whether the proposed locator is grammatically governed by the exception operator. Recovering the complete governed set receives another 35 points: set F1 contributes 20 points so a partially recovered multi-reference clause receives proportionate credit, while 15 points require the exact published order because order aligns locators with their corresponding modalities and distinguishes a complete reconstruction from an unordered bag of citations. The proposed edge receives 15 points because a usable binding must connect the supplied source article to the adjudicated target with the correct article-or-paragraph scope; correctly returning an empty edge for an out-of-scope proposal is equally important because it prevents false legal links.
>
> The remaining 25 points measure interpretation and output reliability. Operator classification receives 8 points and modality receives 7: these fields are relevant to understanding the exception, but neither can compensate for retrieving the wrong provision, so together they carry less weight than any complete binding reconstruction. Structural coherence receives 5 points to ensure that a governed verdict is accompanied by exactly one compatible edge and an outside_operator_scope verdict by no edge. The final 5-point joint term rewards a fully correct dossier and prevents a system that predicts each marginal field independently from being treated as equivalent to one that produces a single consistent legal reading.
>
> Using both partial and exact components avoids two undesirable metric behaviors. Pure exact match would give the same zero credit to a nearly complete multi-locator answer and an unrelated answer; pure component averaging would let frequent operator or modality labels hide failed retrieval. Under this metric, binding-related errors dominate the score, partial locator recovery is recognized, and complete internally consistent answers remain distinguishable. The score is therefore a proxy for textual exception-to-provision binding within this frozen corpus. It does not measure whether a model has determined the provision's ultimate legal effect, validity, temporal applicability, or interaction with legislation outside the supplied act.
>
> The grader is self-contained and accepts only the submission and private target DataFrames; it does not import preparation logic or public inputs.
>
> Submission Format
> example_id,scope_verdict,governed_locators_json,proposed_binding_edge_json,operator_class,proposed_modality  
> DR_0123456789ABCDEF,governed,"[[""EA_1111111111111111"",""PG_2222222222222222""]]","[""EA_AAAAAAAAAAAAAAAA"",""EA_1111111111111111"",""paragraph""]",derogation,mandatory  
> Rules
>
> Use only the supplied public files. External legal databases, recovery of masked source identifiers, private answers, grader or preparation internals, manual test labelling, hard-coded test outputs, and repeated leaderboard probing are prohibited. Local retrieval, deterministic parsing, and models trained or run only on supplied public data are allowed.
>
>  
>
> Submissions
> 72
> Top Score
> 0.989
> Created
> Sep 4, 2026
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> 12/12
> continuing solver slots
> Lockdown
>
> The 12-solver continuing roster was selected from the standings after the one-hour grace period.
>
> Closing in 9h 15m
>
> Submit your solution before the deadline. Payouts are processed after the challenge closes.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.

## Unseen Folio Genre Census

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79wx2v9chgm40eza2af990jd8ed6xz
- DOMAIN exactly as displayed: NLP
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Overview Each query shows a partial set of short historical Greek epigrams from one manuscript. Other catalogued epigrams from that manuscript are withheld completely. Predict the six-count editorial genre census of the withheld remainder. This is an NLP task: infer an aggregate genre composition from Greek text. The revealed and hidden epigrams are two subsets of an existing manuscript, not earlier and later observations. There is no time axis or future outcome to forecast. You never receive the hidden texts, and you do not predict a label for any revealed epigram. Use the wording, themes, and mixture of the revealed epigrams together with the published manuscript size to estimate how many hidden epigrams belong to each opaque genre code g0 through g5. One epigram can contribute to more than one genre count. Evaluation For each manuscript, the grader compares the predicted vector p with the hidden gold vector y using Bray-Curtis similarity: S = 1 - sum(abs(p - y)) / (sum(p) + sum(y)) The denominator is always positive because every hidden epigram has at least one editorial genre. The leaderboard score is the unweighted mean over manuscripts. Higher is better. Scores range from zero to one, and exact vectors score one. Dataset Files train.jsonl contains training inputs. train.csv mirrors those inputs for platform compatibility; revealed_occurrences is compact JSON in one CSV field. train_labels.csv contains one six-count target vector per training query. validation.jsonl and validation_labels.csv use the same schemas for model selection. validation.csv mirrors the validation inputs with compact JSON in revealed_occurrences. test.jsonl contains the evaluation inputs without targets. test.csv mirrors the test inputs with the same four logical fields. sample_submission.csv contains every required test query and the exact output columns. README.md defines field types, Unicode handling, bounds, and examples. Columns Each JSONL input row contains: query_id: an opaque query identifier. total_count: the number of eligible epigrams catalogued for this manuscript. hidden_count: the number of those epigrams absent from the public row. revealed_occurrences: a list of opaque occurrence IDs paired with their Greek text. Source manuscript identifiers, shelf marks, dates, titles, locations, people, and catalogue row numbers are absent. Manuscripts linked by any repeated eligible text are kept in the same split, so exact repeated text cannot bridge training, validation, and test. Submission Submit one row for every test query with exactly these columns: query_id,g0,g1,g2,g3,g4,g5 q_example,1,0,2,0,1,0 Every genre value should be a finite integer from zero through that row's hidden_count. Query IDs must be unique and must match the test set exactly. A wrong column set, missing row, extra row, or duplicate ID is a file-level error. An unusable genre value gives that manuscript a score of zero while other valid rows remain scorable. Compute Solutions run offline on the CPU tier with a 90-minute limit. Include all code needed to train or infer within that budget. Tune choices on the provided training and validation manuscripts; the evaluation manuscripts form a separate group-held split. What not to use Do not search for the original corpus, manuscript catalogue, or hidden epigram texts. Do not use external copies of source records, catalogue identifiers, shelf marks, or lookup tables to reconstruct answers. Do not infer source identities by probing online services or external databases. Do not use test-time internet access, external APIs, or manually recovered hidden labels. Do not modify the public files or rely on row order as a source identifier. Your solution may use the supplied public files and ordinary offline libraries or pretrained model weights available in the execution environment. It must produce predictions from the released inputs alone. Notes Genre codes are intentionally opaque. They are stable across all public splits, and the training labels provide the only permitted supervision for their meanings.
> 0 / 12 beat AI

Inspiration note: Useful because it uses an unusual structured-output task pattern outside standard tabular prediction.


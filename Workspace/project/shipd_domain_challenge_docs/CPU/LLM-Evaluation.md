# CPU LLM Evaluation Challenge Examples

Scrape timestamp: 2026-07-14T00:00:00+05:30

Confirmed CPU examples in this document: 0

These entries are included because the challenge detail page displayed this domain and the challenge is part of the CPU-only challenge collection.

## Fragmented Response Evaluation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx735hhf6sa9h847r8n6xmpva18ak9ep
- DOMAIN exactly as displayed: LLM Evaluation
- Challenge collection: CPU-only
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: None / CPU-only
- Scoring: ↑ Higher is better
- Tags: Not shown
- Best/top context found: Added from user-provided Shipd challenge URL on 2026-07-17; no leaderboard rank context captured.

Full challenge description from page:

> Evaluation logs are not always intact. Truncation, field extraction errors, and detached text spans can leave candidate LLM responses incomplete before a human-preference evaluator sees them. This challenge asks you to reconstruct three damaged assistant responses from a shared fragment bank and then rank the restored responses in the order chosen by human annotators.
> Each episode contains:
> one real user instruction;
> three assistant responses in random order, each with one contiguous span replaced by [MISSING_SEGMENT];
> four detached natural-language fragments in random order: one correct fragment for each damaged response and one hard donor fragment from a lexically related but different conversation tree.
> Your submission is a JSON array containing the three fully restored response strings in best-to-worst human-preference order. This is a joint LLM Evaluation and NLP integrity task: fragment assignment and response evaluation must agree in one natural-language output.
> Dataset
> Public files:
> train.csv: 1,594 labeled episodes.
> test.csv: 530 unlabeled episodes.
> sample_submission.csv: 530 valid placeholder outputs.
> Entire source conversation trees are confined to one split. Source message IDs, user IDs, tree IDs, ranks, timestamps, donor identities, and source row order are not public. No exact damaged response or fragment occurs in both public train and test.
> Columns:
> query_id: string. Opaque episode identifier.
> instruction: string. User request against which the assistant responses were ranked.
> damaged_responses_json: JSON array of exactly three strings in arbitrary order. Every string contains [MISSING_SEGMENT] exactly once.
> fragment_bank_json: JSON array of exactly four detached text fragments in arbitrary order.
> gold_ranking: train only. JSON array of three reconstructed full response strings in human-preference order, best first.
> The donor fragment comes from a reserved conversation tree in the same partition. During local raw construction, donor prompts are matched to episode prompts with TF-IDF, making the extra fragment topically plausible.
> Evaluation
> The final score is bounded to [0,1] and higher is better. An exact normalized target array receives 1.0 for the row. Otherwise four components are used.
> Ordered content: 25 percent
> For each submitted position, token F1 is computed against the gold response at the same rank and averaged over the three positions. Text is lowercased and tokenized into alphanumeric tokens plus individual punctuation/operator tokens. Repeated tokens use multiset counts.
> Fragment integrity: 35 percent
> The grader finds the one-to-one assignment between submitted and gold responses that maximizes total token F1. It then detects released bank fragments as exact substrings after lowercasing and whitespace collapse.
> A detected (submitted response, fragment) pair is correct only when the fragment is the hidden fragment for that response's assigned identity. Precision is correct pairs divided by all detected bank-fragment pairs; recall is correct pairs divided by three. Their F1 is the fragment-integrity score. Copying multiple fragments into every response therefore loses precision.
> Human-preference order: 30 percent
> Using the same best identity assignment, the grader measures the three pairwise ordering decisions. Pairwise accuracy is adjusted above the 0.50 chance floor:
> clip((pairwise_accuracy - 0.50) / 0.50, 0, 1)
> This skill is multiplied by mean identity token F1. Unrelated placeholder text cannot obtain preference credit from an arbitrary tie in identity assignment.
> Exact reconstruction and ranking: 10 percent
> The normalized three-response array must exactly equal the hidden array. Normalization lowercases and collapses whitespace; it does not remove words or punctuation.
> The final score is 25 percent ordered content F1, 35 percent fragment-integrity F1, 30 percent confidence-weighted preference skill, and 10 percent exact array accuracy.
> Submission Format
> Submit a CSV with exactly these columns in this order:
> query_id,reconstructed_ranking
> reconstructed_ranking must be a JSON array of exactly three distinct non-empty strings. The first string is the predicted best response. Each string may contain at most 6,000 characters and the three strings together at most 15,000 characters. CSV quoting must preserve JSON quotes, commas, and newlines.
> Example logical value:
> ["fully restored best response","fully restored second response","fully restored third response"]
> The file must contain every test query_id exactly once, with no duplicate, missing, or extra rows.
> Requirements
> Use CPU computation only, within 90 minutes on 10 CPU cores and 62 GB RAM.
> Fit vectorizers, compatibility models, reward models, thresholds, and calibration on public training data only.
> Restore responses using the released damaged cards and fragment bank.
> Rank the reconstructed natural-language responses; do not submit identifiers or numeric scores.
> What Not To Use
> Do not reverse-map text to OpenAssistant or any external mirror, ranking, ID, or annotation.
> Do not use hidden ranks, private answers, source IDs, tree IDs, donor identities, or source row order.
> Do not use external APIs, hosted LLM judges, web lookup, or human annotation of test rows.
> Do not fit or adapt a representation globally on the complete test corpus.
> Do not use GPU or CUDA-only dependencies.

Inspiration note: Useful because it makes LLM evaluation a CPU benchmark around fragmented/partial responses, encouraging robust rubric-style scoring rather than answer generation.

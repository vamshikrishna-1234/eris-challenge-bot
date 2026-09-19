# CPU From Scratch Challenge Examples

Scrape timestamp: 2026-09-15T06:45:43+05:30

Confirmed CPU examples in this document: 62

These entries will be appended when the recurring Shipd homepage scan finds new matching challenges and confirms their displayed DOMAIN on the challenge detail page.

## Chess Puzzle Difficulty Pair Ranking

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73qrmdqyqcq85gp39r9t6q0x8aqqrn
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Beat abu2win's score of 0.619!

Full challenge description from page:

> Chess Puzzle Difficulty Pair Ranking
> Overview
> Some chess positions are easy to solve and some are hard, and the difference is not simply how
> many pieces are on the board. A crowded middlegame can hide a one-move fork, while a sparse
> endgame can demand a deep, precise sequence. On Lichess, every tactical puzzle carries a
> difficulty rating earned from how real players fare against it.
> This challenge gives you PAIRS of chess positions and asks which position of each pair is the
> HARDER puzzle. You never solve the puzzle and you never output a move -- for each pair you output
> a single bit saying which side is more difficult. It is a learning-to-rank task: you are given
> only pairwise ORDER comparisons to train on -- never a numeric difficulty -- and must reproduce
> that ordering on unseen pairs by reading how hard each position's hidden tactic is.
> Data
> All files are UTF-8, comma-delimited CSV with a header row. A position is a standard FEN string.
> train.csv — labeled training PAIRS to learn ranking from, with columns:
> pair_id — type string: pair id.
> fen_a — type string: the first chess position in Forsyth-Edwards Notation.
> fen_b — type string: the second position.
> harder — type integer: the pairwise ORDER label -- 0 if fen_a is the harder position, 1 if fen_b is. This column appears only in train.csv.
> test.csv — the pairs to judge, with the same pair_id, fen_a, fen_b columns but with NO
> harder.
> Note: no numeric difficulty value is provided anywhere. Training supplies only pairwise order
> comparisons, and the task is to reproduce that order on unseen pairs -- a learning-to-rank
> setting, not numeric prediction. The two positions of a pair always differ in difficulty by a
> clear margin.
> sample_submission.csv — a valid example submission in exactly the format the grader expects.
> task_manifest.json — documentation only: task, submission columns, metric.
> Task
> For each pair_id, output harder -- 0 if fen_a is the harder puzzle, 1 if fen_b is.
> Evaluation
> Score is pairwise accuracy: the fraction of pairs whose harder position you identify correctly.
> score = (number of pairs answered correctly) / (number of pairs)
> Random guessing scores about 0.5. Range is 0 to 1.
> Submission
> Submit a CSV with exactly these columns, one row per test pair_id:
> pair_id,harder
> pair_0a1b2c3d4e5f,0
> pair_1122aabbccdd,1
> pair_id — type string: a test pair id, matching test.csv exactly.
> harder — type integer: 0 if fen_a is harder, 1 if fen_b is harder.
> Every test pair_id must appear exactly once, or the submission is rejected.
> Appropriate Approaches
> Train a pairwise RANKING model FROM SCRATCH on the training pairs -- for example encode each board from its FEN (piece placement, material, king safety, mobility, phase) into a difficulty score with a shared encoder, and train it so the harder side of each training pair scores higher (a siamese / RankNet-style objective). At test time, compare the two encoded positions. A model that reads the board spatially can beat simple counts.
> Counting pieces or legal moves barely beats chance; difficulty comes from the latent tactic, not from crowdedness, so a learned board representation is the load-bearing component.
> Difficulty prediction from a position alone is intrinsically noisy, so validate on a held-out split of the training positions and expect modest accuracy.
> Runtime and environment rules
> Compute is CPU only, with no GPU; the solution must finish within 1.5 hours on 10 cores, 62 GB RAM.
> No internet access at runtime: no downloads, no installs; use only libraries already provided.
> Train everything FROM SCRATCH on the provided positions. No pretrained weights or engines.
> What Must Not Be Used
> No pretrained model weights, and no chess engine or opening/tablebase database.
> No external data or network access.
> Do not try to identify a position's original puzzle or look up its rating in any external or offline resource; reconstructing the ratings is out of scope and treated as cheating.

Inspiration note: Useful because it forces models to learn the task signal from supplied data only, which is ideal for fair CPU-only challenge design.

## Chess Position Evaluation - Learning Value Functions from Raw Board States

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79w7myffhaa5x6jnda9p84j18ahxqq
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: reinforcement-learning
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Given a chess position as a raw 8×8×12 binary tensor — no features, no piece-square tables, no mobility counts — train a neural network to predict the expected game outcome from that position. This is the value function problem: the same core component that made AlphaZero work. If you can accurately evaluate any position, you can play chess.
> You cannot use tree search at inference time. You cannot engineer features from the board. Your model must look at the raw grid of pieces and learn spatial patterns — pawn chains, open files, king safety, piece coordination, passed pawns — entirely from data. This is a genuine computer vision problem on an 8×8 grid, not a tabular classification task.
> Every major chess AI benchmark focuses on move prediction or engine strength through search. AlphaZero (2017) used self-play RL + MCTS on TPU clusters to learn value + policy jointly. Leela Chess Zero runs distributed GPU self-play but still needs MCTS at inference. Maia Chess (2019-2020) predicts human moves at specific ELO — supervised imitation, not value learning. Kaggle chess competitions reduced positions to handcrafted features for XGBoost move classification. This challenge is different in three fundamental ways:
> It measures value function quality, not move-matching accuracy. A model that predicts "the player to move has a 0.7 expected outcome" is correct even if the human played a different move than the model would prefer. Value functions are the core of RL; move prediction is behavioral cloning.
> It bans feature engineering. You receive positions as raw 8×8×12 binary tensors. Your model must learn that a knight on f3 controls e5 and g5, that doubled pawns are weak, that an open g-file near the opponent's king is dangerous. This forces genuine spatial reasoning — a small CNN on a grid — the same inductive bias that made AlphaZero's architecture work. XGBoost and LightGBM treat each of the 768 board squares as independent features and cannot capture translation-invariant spatial patterns like "a rook on an open file" regardless of which file, making them structurally unsuitable for this task.
> It provides game sequences for TD-learning in training, but tests on i.i.d. positions. The training data groups positions by game in temporal order for TD(λ) learning. The test data shuffles positions globally — removing game boundaries, ELO ratings, and temporal grouping — so evaluation measures pure per-position value estimation without sequential context.
> The Value Function Problem
> In reinforcement learning, the value function V(s) answers: "From the perspective of the player about to move, what is the expected outcome?"
> V(s) = 1.0 means the player to move is winning. V(s) = 0.5 means the position is equal. V(s) = 0.0 means the player to move is losing.
> This is the player-to-move convention — the same convention used by AlphaZero and throughout the RL literature. The training labels, test answers, and your submission predictions all use this perspective. If White is winning but Black is to move, V(s) = 0.0 (Black is losing). If White is winning and White is to move, V(s) = 1.0.
> Learning V(s) from data is hard for several reasons:
> Sparse signal: You only see the final outcome (win/draw/loss), not the evaluation of each intermediate position
> Temporal structure: Positions in a game are correlated — V(s_t) and V(s_{t+1}) should be close unless a blunder occurred
> Perspective flip: When the turn changes after a move, the evaluation must flip: if White just moved and had V(s) = 0.8, the same board from Black's perspective should be 1 − 0.8 = 0.2. The sides array tells you who is to move, enabling this symmetry.
> Calibration matters: A model that outputs 0.9 for a position that is actually drawn is worse than one that outputs 0.55
> Your training data provides three signals, from weakest to strongest:
> Game outcome (supervised): Each position is labeled with the final result (1.0, 0.5, 0.0). Training on this alone gives a naive value function — "positions from won games are good, positions from lost games are bad."
> Temporal proximity (TD-learning): V(s_t) and V(s_{t+1}) should differ by at most a small amount, because one move rarely changes the evaluation dramatically. A sharp drop in V(s) after a move often indicates a blunder — and your model should detect that.
> Perspective symmetry (self-supervised): Given a position with White to move and its flipped twin (same board, Black to move), the evaluations should sum to 1.0: V(s_white_to_move) + V(s_black_to_move) = 1.0. You can generate self-supervised training pairs by flipping the board and side. This doubles your effective data and enforces consistency.
> A solution that uses all three signals will outperform one that treats each position independently.
> A convolutional neural network with 3×3 or 5×5 kernels over the 8×8 board naturally captures local piece interactions. The same kernel that detects "knight + pawn chain on the queenside" works regardless of whether the structure is on a3-b2 or h3-g2. This is the same architectural insight behind AlphaZero's ResNet trunk: chess positions have 2D spatial structure, and translation-equivariant processing is the right inductive bias.
> Data
> Files
> You are provided with two NumPy archive files:
> train.npz — Training data. Load with np.load(). Contains the following named arrays:
> Key	Type	Shape	Description
> boards	uint8	(N, 8, 8, 12)	Binary board tensors. N ≈ 5.2M positions across ~122K unbroken sequences. Train positions whose board also appears in test are removed; if a removal falls inside a game, the game is split into unbroken sub-sequences (no silent holes for TD-learning to cross).
> outcomes	float32	(N,)	Game outcome from the player-to-move's perspective: 1.0 = won, 0.5 = drew, 0.0 = lost. Regression target.
> sides	int8	(N,)	Which player moves next: 0 = White, 1 = Black
> castling	int8	(N,)	Castling rights as 4-bit integer: bit3=K, bit2=Q, bit1=k, bit0=q
> elos	int16	(N,)	ELO rating of the player to move
> game_boundaries	int32	(G, 2)	Start/end indices for each unbroken sequence (G ≈ 122K). Sequence i spans positions [game_boundaries[i,0], game_boundaries[i,1]). A game with an internal leakage overlap is split into multiple contiguous entries, so every entry is a clean temporal run for TD-learning.
> num_games	int	scalar	Total number of games G
> num_positions	int	scalar	Total number of positions N
> test.npz — Test data. Does NOT contain outcomes, elos, game_boundaries, or num_games. Positions are shuffled globally into i.i.d. order — no temporal or game-level grouping. Contains only:
> Key	Type	Shape	Description
> boards	uint8	(M, 8, 8, 12)	Binary board tensors. M ≈ 3,128 unique positions (deduplicated) from expert-level games (ELO ≥ 2000).
> sides	int8	(M,)	Player to move: 0 = White, 1 = Black
> castling	int8	(M,)	Castling rights (same encoding as train)
> num_positions	int	scalar	Total number of test positions M
> sample_submission.csv — Template for predictions. Each row maps a position_id to the prediction placeholder.
> Board Representation
> Each board position is a binary tensor of shape (8, 8, 12):
> Channel	Piece	Channel	Piece
> 0	White Pawn	6	Black Pawn
> 1	White Knight	7	Black Knight
> 2	White Bishop	8	Black Bishop
> 3	White Rook	9	Black Rook
> 4	White Queen	10	Black Queen
> 5	White King	11	Black King
> Value is 1 where a piece occupies a square, 0 otherwise. The board is oriented with White's home rank at the bottom (rank index 7).
> sides and castling are stored as separate 1D arrays, not appended to the board tensor. This keeps the tensor purely about piece positions.
> Temporal Structure (Training Only)
> In train.npz, positions are grouped by game and ordered by move number (positions 6 through end of game). The game_boundaries array maps each game to its position range. This temporal order enables three techniques beyond supervised learning:
> TD(λ) training: V(s_t) should be close to r + γ·V(s_{t+1}), where r is 0 for all moves except the last (where r = game_outcome)
> Blunder detection: A large |V(s_t) − V(s_{t+1})| indicates a game-changing move — useful for attention-weighting training examples
> Opening-to-endgame progression: Early positions have high uncertainty, late positions have low uncertainty — a well-calibrated model should reflect this
> Test positions have no temporal structure — they are shuffled globally into i.i.d. order. Your model must evaluate each test position independently, using only the board state, side to move, and castling rights.
> Data Split
> Train/test split is by game ID — all positions from a given game are in either train or test, never both. The test set is filtered to higher-rated play (ELO ≥ 2000) and deduplicated to unique chess positions (board + side + castling), so the model is never evaluated twice on the same position. No positions from the same game appear in both sets. In train, any position whose board also appears in test is removed; if that removal falls inside a game, the game is split into unbroken sub-sequences rather than leaving a hole.
> Submission Format
> Submit a CSV file with exactly these columns:
> Column	Type	Description
> position_id	str	Position identifier from sample_submission.csv (e.g., pos_000000)
> predicted_value	float	Your predicted outcome from the player-to-move's perspective (0.0–1.0). Same convention as the outcomes training labels.
> Example submission rows:
> position_id,predicted_value
> pos_000000,0.782
> pos_000001,0.691
> pos_000002,0.734
> pos_000003,0.412
> pos_000004,0.388
> Evaluation
> Submissions are evaluated using a three-component metric:
> Score = 0.40 × Normalized_MSE + 0.30 × Calibration + 0.30 × Rank_Correlation
> Component 1: Normalized MSE (40%)
> Mean squared error between predicted value and actual game outcome, normalized by a constant-prediction baseline:
> Normalized_MSE = 1 − MSE(predictions) / MSE(baseline_predicts_0.5)
> Where MSE(baseline_predicts_0.5) is the error of always predicting 0.5 (draw) for every position. Getting the absolute value right is essential for use as an evaluation function in actual play.
> Component 2: Expected Calibration Error (30%)
> ECE with quantile (equal-mass) binning across 10 bins. Predictions are sorted and split into 10 groups of equal size. For each bin, the average prediction is compared to the actual win rate:
> Calibration_raw = 1 − (1/K) × Σ |avg_pred_bin_i − actual_win_rate_bin_i|
> Where K is the number of bins with ≥10 samples. An undercoverage penalty is applied when the central 90% (5th–95th percentile) of predictions spans less than 50% of the [0, 1] range: the score is multiplied by a factor that decreases with the narrower spread. The percentile spread — not max minus min — is used so that a single stray outlier cannot masquerade as full coverage. This penalizes models that only output a narrow range of values (e.g., always predicting 0.4–0.6) — a well-calibrated model must use the full [0, 1] range.
> A perfectly calibrated model that spans the full probability range scores 1.0. Calibration rewards trustworthy predictions — if your model outputs 0.8, positions with that prediction should actually be won ~80% of the time.
> Component 3: Rank Correlation (30%)
> Spearman rank correlation between predicted values and actual game outcomes, normalized:
> Rank_Correlation = (Spearman_Correlation + 1.0) / 2.0
> This measures whether the model correctly orders positions — "position A is more favorable for the player to move than position B" — even if the absolute values are off. Rank ordering is the core of move selection: pick the move leading to the highest-evaluated position.
> A naive model that always predicts 0.5 gets Normalized MSE = 0.0, Calibration ≈ 0.49 (well-calibrated at the single prediction point, but penalized for zero prediction spread), and Rank Correlation = 0.5 → composite score ≈ 0.30. A strong neural value network should reach composite score ≥ 0.55.
> What Is NOT Being Tested
> Move prediction accuracy — This is NOT a "guess what the human played" challenge
> Engine match strength — We do not run your model against Stockfish
> Search depth — No tree search at inference time; one forward pass per position
> Constraints & Rules
> What IS Allowed
> CNN, transformer, or any architecture that processes the 8×8 grid directly
> Data augmentation: board flipping (horizontal symmetry), rotation (for training set expansion)
> Temporal-difference learning (TD(λ), TD(0)) on training game sequences
> Self-supervised pretraining tasks (e.g., predict the next board state, masked piece prediction)
> Multi-task learning (predict outcome + next move as auxiliary task)
> Any library in the standard ML Docker image (PyTorch, TensorFlow, JAX)
> What IS NOT Allowed
> Computing explicit piece-square tables, mobility counts, attack maps, pawn structure features
> Using a chess engine (Stockfish, Leela, etc.) at any point — training or inference
> Pretrained models — you must train from scratch
> Tree search at inference time
> External data — only the provided .npz files

Inspiration note: Useful because it forces models to learn the task signal from supplied data only, which is ideal for fair CPU-only challenge design.

## Ocean Core Sediment Correlation and Sensor Bridge Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79fyy8330vae93x6fnkv36j18a5qhy
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: small-data
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Plain language objective: for each row, decide which pieces of nearby sediment cores line up to form one continuous record, mark the matching horizon between cores, name the transition type, and fill in short missing sensor windows.
> Scientists drill several nearby holes because one sediment core usually has gaps, disturbed material, or incomplete recovery. A hole is one drilled borehole at the same local site. The holes are anonymous in this challenge: original source names are replaced inside each row by IDs such as H0, H1, and H2, and cores are replaced by IDs such as C00 and C01. This anonymization prevents source lookup and makes the task depend on the sensor patterns rather than original filenames, site names, or raw depths.
> Each public row contains two to four anonymous holes from one local drilling episode. For every anonymous hole/core, you receive row-local sequences from physical-property sensors: a bulk-density proxy (gra), natural gamma radiation (ngr), and whole-round magnetic susceptibility (ms) when present. You also receive row-local core and section boundary markers.
> The public sensor arrays include several masked bridge windows listed in bridge_query_json. Those windows are real source-derived proxy measurements withheld from the public arrays. Your submission must recover both the expert correlation structure and the missing compact bridge values.
> For every test row, submit one structured record:
> segments_json: ordered selected core intervals that form the local continuous record.
> ties_json: equivalent-horizon tie points between selected intervals when the transition is a true tie.
> transition_type: one of tie, append, gap, or end.
> bridge_json: recovered values for the masked proxy bridge windows.
> confidence: row-level confidence in [0, 1].
> This is a structured scientific reconstruction task, not a tabular classification task, not a regression leaderboard, and not a single pairwise alignment score. Useful solutions must compare multi-hole, multi-sensor sequence patterns, obey physical interval boundaries, decide which intervals belong in the expert record, distinguish true ties from append/gap/end transitions, and infer withheld bridge values from surrounding and cross-hole evidence.
> Only CPU solutions are allowed. The solution runtime limit is 1.5 hours on 10 CPU cores and 62 GB RAM. Practical approaches include constrained dynamic programming, cross-sensor sequence matching, compact feature models, local imputation models, small CPU temporal models, and train-only calibration. Runtime internet use, source-data lookup, private-file access, and external hosted inference are not allowed.
> Task
> For each test row, parse sensor_sequences_json and bridge_query_json, compare the anonymous core profiles, and output a compact correlation-and-bridge record. The row-local IDs inside the public JSON cells are the only valid hole/core IDs in your answer. Core intervals use integer sample indices from 0 to sequence_length - 1.
> segments_json is a JSON list of segment objects. A segment is one chosen interval from one anonymous core. Each object must contain exactly hole, core, start, and end. The hole value is a row-local hole id such as H0; the core value is a row-local core id such as C02; start and end are integer sample indices. The list should be in local record order. A typical row has two selected intervals.
> ties_json is a JSON list of two-endpoint lists. A tie point says that two positions in different row-local cores represent the same sediment layer. Each endpoint string must use the format Hn:Cxx:index, such as H1:C07:148. A true tie usually has one pair connecting the end of the first selected interval to the start of the next selected interval. Append, gap, and end transitions may have an empty ties_json list.
> transition_type must be one of tie, append, gap, or end. tie means the two intervals meet at a matched sediment layer; append means the next interval follows without a scored tie point; gap means the record has missing material between intervals; end marks the end of the local record.
> bridge_json is a JSON list of bridge-window objects. Each object must contain exactly hole, core, sensor, start, end, and values. The first five fields should identify a window from bridge_query_json; sensor is one of gra, ngr, or ms. The values field is a list of eight finite numeric values representing the masked normalized proxy bridge in order across that window.
> Train and validate only from the public challenge files. Public row IDs, row order, anonymous hole/core IDs, JSON lengths, masked-window counts, and file sizes are not source keys. A strong solution should learn reusable sensor-pattern, interval, and bridge-imputation reasoning from labeled training rows, then apply it to unseen drilling families.
> Intended Approach
> This challenge is intended for from-scratch CPU modeling over the provided public sequences. Reasonable approaches include parsing the row-local JSON into aligned sensor arrays, normalizing within each row, extracting cross-sensor similarity features, using constrained DTW or dynamic programming to propose candidate tie horizons, training compact CPU models to rank physically valid segment/tie candidates, and using local multi-sensor context to impute the bridge windows. Validate using only public training rows, including modality ablations such as GRA-only, NGR-only, magnetic-susceptibility-only, bridge-only, and boundary-only checks to make sure the final system is using the sensor evidence rather than metadata shortcuts.
> Submissions should keep the structured record internally consistent: selected intervals must use valid row-local hole/core IDs, start/end indices must stay inside each sequence, true ties should connect selected interval boundaries, non-tie transitions should not invent tie points, and bridge windows should match the public bridge queries. The best solutions should combine sequence alignment, interval selection, transition recovery, masked proxy repair, and confidence calibration instead of optimizing one field in isolation.
> What Not To Do
> Using any of the approaches below is grounds for rejection on review, regardless of leaderboard score.
> Do not look up original source expeditions, sites, holes, filenames, raw depths, timestamps, table rows, checksums, or official labels for hidden rows.
> Do not use runtime internet access or external copies of the source records to identify test episodes or recover masked bridge values.
> Do not use private files, hidden answers, row order, opaque ID hashes, JSON length, file size, masked-window count, or filesystem metadata as answer channels.
> Do not reduce the task to transition-type classification, one-channel dynamic time warping, bridge-window mean filling, or a fixed segment template that ignores the sensor sequences.
> Do not submit malformed JSON, duplicate IDs, extra columns, non-finite confidence, overlong JSON, impossible indices, invalid bridge values, or invalid row-local references as a format exploit.
> Do not use hosted APIs, closed-source teacher services, or external geological-correlation services for hidden-row interpretation.
> Enforcement on invalid approaches: submissions may be reviewed for source lookup, runtime network use, private-file access, metadata-only behavior, masked-window shortcutting, and solutions that avoid the structured correlation-and-bridge contract. Prohibited approaches can be rejected before payout even if the CSV is structurally valid.
> Evaluation
> Higher is better. Minimum score: 0.0. Maximum score: 1.0. A perfect submission scores exactly 1.0.
> Each row receives five main component scores:
> S: selected-segment score.
> T: tie-point score.
> R: transition score.
> B: masked bridge-window score.
> K: consistency score.
> The final row formula is:
> core = 0.32*S + 0.16*T + 0.16*R + 0.26*B + 0.10*K
> confidence_calibration = max(0, 1 - abs(predicted_confidence - true_confidence))
> raw_row_score = core * (0.92 + 0.08*confidence_calibration)
> row_score = raw_row_score ^ 1.25
> The exponent 1.25 is a disclosed joint-correctness strictness term. It keeps partial credit available, but it reduces the value of shallow half-solutions such as fixed full-core intervals, bridge-window zero filling, transition-only guesses, or segment templates that miss the tie horizons.
> The segment score S is a greedy soft F1 over submitted segment objects. A predicted segment can match a true segment only when hole and core are identical. For a matching pair:
> interval_iou = overlap_length / union_length
> endpoint_score = max(0, 1 - (abs(pred_start - true_start)
> + abs(pred_end - true_end)) / 30)
> segment_pair_score = 0.70*interval_iou + 0.30*endpoint_score
> The tie score T is a greedy soft F1 over submitted tie endpoint pairs. A tie endpoint has format Hn:Cxx:index. An endpoint earns:
> endpoint_score = 1 - abs(pred_index - true_index) / 5
> but only when the predicted and true endpoints have the same row-local hole and core and the index error is at most 4. Otherwise endpoint credit is 0. A tie-pair score is the better of the direct and reversed endpoint pairing.
> The bridge score B is a greedy soft F1 over submitted bridge-window objects. A bridge prediction can match a true bridge window only when hole, core, and sensor are identical. For a matching pair:
> window_iou = overlap_length / union_length
> mae = mean absolute error over the 8 submitted values
> value_score = max(0, 1 - mae)
> bridge_pair_score = window_iou * value_score
> Greedy soft F1 means that predicted objects and true objects are matched one-to-one in descending pair-score order. If M is the sum of matched pair scores, then:
> precision = M / number_of_predictions
> recall = M / number_of_true_objects
> soft_f1 = 2*precision*recall / (precision + recall)
> If both lists are empty, the score for that head is 1.0. If only one list is empty, the score is 0.0.
> The transition score R is 1.0 when transition_type exactly matches one of tie, append, gap, or end, and 0.0 otherwise.
> The consistency score K checks whether the submitted pieces agree with each other. Rows with fewer than two submitted segments receive K = 0. For a tie transition, submitted tie endpoints should land within four indices of submitted segment starts or ends, and K is the fraction of submitted tie endpoints that do so. For non-tie transitions, K = 1.0 when no ties are submitted and K = 0.35 when ties are submitted anyway.
> The final leaderboard score blends average row quality with robustness on private physical groups:
> Final = 0.76 * mean(row_score)
> + 0.24 * mean(worst_group_score_per_axis)
> For each private axis, the grader computes the mean row score in every group bucket and takes the lowest bucket mean. The private axes cover source family, transition category, selected-span length, and sensor-coverage regime. These groups are used only to reward solutions that work across difficult cases; they are not output fields and are not random hash buckets.
> Wrong columns, reordered columns, missing IDs, extra IDs, duplicate IDs, illegal transition enums, nonnumeric confidence, non-finite confidence, confidence outside [0, 1], or overlong JSON cells raise InvalidSubmissionError. Malformed row-local JSON or semantically invalid row-local references give zero for that row rather than crashing the whole submission.
> Dataset
> The public prepared data contains labeled training rows, hidden-label test rows, and a sample submission. Each row is one local correlation-and-bridge episode. Sensor sequences and bridge queries are stored directly in CSV JSON cells.
> File overview
> Item	Description
> train.csv	Inputs plus labels
> test.csv	Test inputs only
> sample_submission.csv	Valid weak template
> sample_submission.csv has the exact required submission columns and one placeholder row for every test id; it is a schema and weak-baseline template, not a source of hidden labels.
> train.csv columns
> Column	Type	Description
> id	string	Opaque row id
> hole_count	int	Number of row holes
> core_count	int	Number of row cores
> sequence_length	int	Samples per core
> sensor_sequences_json	JSON	Public sensor data
> bridge_query_json	JSON	Masked bridge windows
> segments_json	JSON	Train segments
> ties_json	JSON	Train ties
> transition_type	string	Train transition
> bridge_json	JSON	Train bridge values
> confidence	float	Train confidence
> Plain train-column details: id is an opaque row identifier; hole_count and core_count describe the row-local episode size; sequence_length is the number of sample positions per core; sensor_sequences_json contains the public GRA, NGR, magnetic-susceptibility, mask, and section-marker arrays; bridge_query_json lists the masked windows and value-bin count. The train-only target columns are segments_json, ties_json, transition_type, bridge_json, and confidence.
> test.csv columns
> Column	Type	Description
> id	string	Opaque row id
> hole_count	int	Number of row holes
> core_count	int	Number of row cores
> sequence_length	int	Samples per core
> sensor_sequences_json	JSON	Public sensor data
> bridge_query_json	JSON	Masked bridge windows
> Plain test-column details: id is the row identifier that must appear in the submission; hole_count, core_count, and sequence_length define the row-local structure; sensor_sequences_json is the public sensor/boundary evidence for that hidden-label episode; bridge_query_json lists the bridge windows to recover. Test rows do not include segments_json, ties_json, transition_type, bridge_json, or confidence.
> Public JSON schemas
> sensor_sequences_json is a JSON list of core objects. Each core object has this schema:
> Field	Type	Meaning
> hole	string	Row-local hole id
> core	string	Row-local core id
> n	int	Array length
> section_markers	list	Section spans
> gra	list	Density proxy
> ngr	list	Gamma radiation
> ms	list	Magnetic proxy
> gra_mask	list	GRA presence
> ngr_mask	list	NGR presence
> ms_mask	list	MS presence
> Sensor arrays have length n. Mask arrays also have length n and use 1 where the sensor value is present and 0 where the sensor did not cover the row-local index or is part of a bridge query. Missing sensor values appear as JSON null. Section markers are row-local index spans and do not expose raw depths.
> Shortened sensor_sequences_json example, with arrays shortened for display:
> [
> {
> "hole": "H0",
> "core": "C00",
> "n": 160,
> "section_markers": [
> {"section": "S01", "start": 0, "end": 42},
> {"section": "S02", "start": 43, "end": 89}
> ],
> "gra": [0.14, null, -0.06],
> "ngr": [-0.22, -0.18, -0.04],
> "ms": [null, null, null],
> "gra_mask": [1, 0, 1],
> "ngr_mask": [1, 1, 1],
> "ms_mask": [0, 0, 0]
> }
> ]
> bridge_query_json is a JSON object with bins and windows. bins is always 8. windows lists the masked windows whose binned values must be recovered in bridge_json.
> bridge_query_json schema:
> Field	Type	Meaning
> bins	int	Value count
> windows	list	Masked windows
> Each object in windows has:
> Field	Type	Meaning
> hole	string	Row-local hole id
> core	string	Row-local core id
> sensor	string	gra, ngr, or ms
> start	int	Window start
> end	int	Window end
> Example:
> {
> "bins": 8,
> "windows": [
> {"hole": "H0", "core": "C01", "sensor": "ngr", "start": 125, "end": 140},
> {"hole": "H1", "core": "C00", "sensor": "gra", "start": 25, "end": 40}
> ]
> }
> For each query window, bridge_json should repeat hole, core, sensor, start, and end, then add values, a list of eight finite numbers:
> undefined
> [
> {
> "hole": "H0",
> "core": "C01",
> "sensor": "ngr",
> "start": 125,
> "end": 140,
> "values": [0.18, 0.21, 0.17, -0.05, -0.22, -0.31, -0.19, 0.04]
> }
> ]
> ## Submission
> Write `./working/submission.csv` with a header row and exactly one row for every `id` in `test.csv`. The header must contain these six columns in this exact order: `id,segments_json,ties_json,transition_type,bridge_json,confidence`.
> ### Submission format
> | Column | Type | Constraint |
> |---|---|---|
> | `id` | string | Same set as test |
> | `segments_json` | JSON | Max 6 segments |
> | `ties_json` | JSON | Max 6 ties |
> | `transition_type` | string | Native enum |
> | `bridge_json` | JSON | Max 6 windows |
> | `confidence` | float | In `[0,1]` |
> Example:
> id,segments_json,ties_json,transition_type,bridge_json,confidence
> oc_0123456789abcdef,"[{""hole"":""H1"",""core"":""C07"",""start"":12,""end"":148},{""hole"":""H0"",""core"":""C08"",""start"":9,""end"":156}]","[[""H1:C07:148"",""H0:C08:9""]]",tie,"[{""hole"":""H1"",""core"":""C07"",""sensor"":""ngr"",""start"":136,""end"":151,""values"":[0.18,0.21,0.17,-0.05,-0.22,-0.31,-0.19,0.04]}]",0.82
> oc_fedcba9876543210,"[{""hole"":""H2"",""core"":""C03"",""start"":25,""end"":149},{""hole"":""H2"",""core"":""C04"",""start"":4,""end"":138}]","[]",append,"[{""hole"":""H0"",""core"":""C01"",""sensor"":""gra"",""start"":42,""end"":57,""values"":[-0.44,-0.31,-0.08,0.12,0.35,0.41,0.22,0.05]}]",0.61
> undefined

Inspiration note: Useful because it forces models to learn the task signal from supplied data only, which is ideal for fair CPU-only challenge design.

## Butterfly Warning Pattern and Species Disentanglement

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74n5dszgq2sja247k5mwdand8ap070
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Beat shikum's score of 0.820!

Full challenge description from page:

> Mimicry disentanglement: Separating A Warning Pattern From Animal Wearing It
> Overview
> Heliconius butterflies are the classic case of Müllerian mimicry. Unrelated but equally unpalatable species that fly together converge on the same warning pattern, because a shared signal spreads the cost of teaching predators. The consequence is that a Heliconius wing advertises a mimicry ring — a locally convergent phenotype — and not the animal's ancestry. Two butterflies of different species can be almost indistinguishable to the eye, while two butterflies of the same species from different valleys can look nothing alike.
> You are given one standardised dorsal wing image per specimen: a two-panel composite, forewing on the left, hindwing on the right, segmented onto a black background. From that image alone you must report two things about each test specimen:
> mimicry_ring — which convergent warning phenotype the specimen advertises.
> species — which of the two co-mimic species it actually belongs to, Heliconius erato or Heliconius melpomene.
> These two labels are close to orthogonal by construction, and that is the whole problem. Colour and pattern layout carry the ring. Ancestry has to be read off the things mimicry does not copy faithfully: wing outline, proportion, venation and scale texture.
> The test set holds out whole subspecies. Every geographic race in the test set is absent from training, and within a ring the training species-mix frequently points the wrong way. In training, for example, every cyrbia-patterned specimen is H. erato; in the test set, cyrbia-patterned specimens are H. melpomene. A model that learns ring -> species from the training data and applies it will score below chance on species. Points are concentrated on exactly those specimens, so the task is to predict the pattern and the ancestry without letting the first answer contaminate the second.
> Evaluation
> The score is a weighted combination of two macro-F1 terms, both computed only over the label values that occur in the answer key, so a perfect submission scores exactly 1.0:
> score = 0.45 * macro_F1(mimicry_ring) + 0.55 * weighted_macro_F1(species)
> macro_F1(mimicry_ring) is the unweighted macro-averaged F1 over the four rings.
> weighted_macro_F1(species) is the macro-averaged F1 over the two species where each specimen i contributes with a deception weight w_i, computed from the training split as
> w_i = 1 + 2 * (1 - p_train(species_i | ring_i))
> where `p_train(species_i | ring_i)` is the fraction of training specimens carrying specimen `i`'s
> true ring that are also its true species. A specimen whose ring is dominated in training by the
> *other* species carries the maximum weight of 3.0; a specimen whose ring already points at the
> right species carries a weight near 1.0. In this test set `w` ranges from 1.23 to 3.00 with a mean
> of 2.20, and 55 of the 281 specimens sit at the maximum of 3.0.
> Weighted macro-F1 is the ordinary macro-F1 with per-sample weights folded into the true-positive, false-positive and false-negative counts:
> import numpy as np
> def macro_f1(y_true, y_pred, labels, weights):
> scores = []
> for c in labels:
> t = (y_true == c); p = (y_pred == c)
> tp = float(weights[t & p].sum())
> fp = float(weights[(~t) & p].sum())
> fn = float(weights[t & (~p)].sum())
> denom = 2.0 * tp + fp + fn
> scores.append(0.0 if denom <= 0 else 2.0 * tp / denom)
> return float(np.mean(scores))
> def evaluate(y_true_ring, y_pred_ring, y_true_sp, y_pred_sp, w):
> ones = np.ones(len(y_true_ring), dtype=float)
> s_ring = macro_f1(y_true_ring, y_pred_ring, sorted(set(y_true_ring)), ones)
> s_sp   = macro_f1(y_true_sp,   y_pred_sp,   sorted(set(y_true_sp)),   w)
> return 0.45 * s_ring + 0.55 * s_sp
> A cell whose value is missing, NaN, or outside the allowed vocabulary is scored as an incorrect prediction. The final score is clipped to [0.0, 1.0]; higher is better.
> Dataset
> The prepared data lives under dataset/public/:
> train.csv — 1,621 rows, columns:
> id (string) — specimen identifier.
> image (string) — path to the image relative to dataset/public/, e.g. images/wg_01000000.png.
> subspecies (string) — the geographic race of this training specimen. Provided for training rows only. It is the grouping key of the split: no subspecies in train.csv appears in the test set. Use it if you want validation folds that behave like the real test set.
> mimicry_ring (string) — target 1 for this training specimen.
> species (string) — target 2 for this training specimen.
> test.csv — 281 rows, columns id and image only.
> images/ — 1,902 PNG files, 224 x 448, 8-bit RGB; left 224 x 224 panel is the forewing, right panel is the hindwing, both dorsal surfaces, non-wing pixels set to black.
> sample_submission.csv — a correctly formatted, label-free submission.
> Allowed values:
> mimicry_ring — one of cyrbia, dennis_rayed, postman, postman_yellowbar.
> species — one of erato, melpomene.
> Training composition, for orientation: the ring dennis_rayed splits almost evenly between the two species (400 erato against 399 melpomene), postman runs 139 erato against 208 melpomene, postman_yellowbar runs 12 erato against 93 melpomene, and cyrbia is erato only (370 specimens, 0 melpomene).
> Submission
> Write exactly one file, working/submission.csv, with exactly the columns id, mimicry_ring, species, one row per test id:
> id,mimicry_ring,species
> wg_01000106,dennis_rayed,erato
> wg_01000113,postman,melpomene
> wg_01000156,cyrbia,melpomene
> Requirements
> Exactly 281 rows plus the header, one for each id in test.csv, no duplicates and no extra ids.
> Exactly the three columns id, mimicry_ring, species, in any row order. The grader joins on id, so ordering does not matter, but an unexpected or missing column is rejected.
> Every mimicry_ring value must be one of the four allowed rings; every species value must be one of the two allowed species. Values outside those sets, empty cells and NaN are scored as incorrect rather than rejected.
> A submission whose mimicry_ring and species columns are both entirely empty or NaN is rejected.
> What not to use
> No pretrained weights of any kind — no ImageNet backbones, no foundation models, no timm/torchvision checkpoints, no CLIP. Train only on the provided training rows.
> No external data and no network access at run time.
> Do not attempt to recover museum accession codes or the split logic.
> CPU only. The reference solution runs in a few minutes on 10 cores and needs no accelerator.

Inspiration note: Useful because it forces models to learn the task signal from supplied data only, which is ideal for fair CPU-only challenge design.

## Axis and Polarity: Spatial Relations from Jaw Vibration

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ag2nvvegejqvhtc6f2ekdmd8aq6r9
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Axis and Polarity: Spatial Relations from Jaw Vibration
> Domain: From Scratch / Non-acoustic Speech — relational classification from paired Mandarin jaw-vibration signals.
> Task
> Predict the spatial relation between two non-acoustic command recordings. Each example is constructed from two separate isolated recordings made by the same source participant. Each input contains two one-dimensional jaw-vibration waveforms captured by a flexible piezoelectric sensor while 90 dB background noise was present. The two hidden commands always come from the six directional controls: forward, backward, right, left, up, and down.
> Treat forward, right, and up as the positive direction on their respective axes, and backward, left, and down as the negative direction. Return one of three relations:
> INVERSE_AXIS: opposite directions on the same axis: forward/backward, right/left, or up/down.
> CROSS_SAME_POLARITY: different axes, with both directions positive or both directions negative.
> CROSS_MIXED_POLARITY: different axes, with one positive direction and one negative direction.
> Here, polarity means the sign of a spatial control vector, not electrical or waveform polarity. This is not isolated command recognition. Individual command labels are never evaluated or exposed. The target exists only for a pair, and a successful model must learn the joint axis-and-sign relation between unfamiliar-speaker signals.
> The nearest prior is Yuan et al.'s original Non-acoustic Speech Dataset task of recognizing one isolated command. The exact delta is that this benchmark never predicts a command: it predicts one of three signed spatial relations that exists only between two different commands under a speaker-disjoint split.
> All recordings from a participant remain on one side of the split. Test participants never appear in training. Every selected waveform occurs in exactly one pair. Within every participant and relation, each hidden command appears exactly 18 times on each pair side. A single waveform therefore carries no command-frequency or side-frequency class clue. The construction selects 7,128 of 7,256 eligible directional recordings; 128 are left unused to preserve this exact balance.
> Data
> train.parquet contains 2,592 labelled pairs. test.parquet contains 972 unlabelled pairs. All signals are mono signed 16-bit PCM sampled at 16 kHz.
> pair_id (str): opaque pair identifier assigned only after the participant split and shuffle.
> signal_a (list<int16>): first jaw-vibration waveform.
> signal_b (list<int16>): second jaw-vibration waveform.
> relation (str): training target: INVERSE_AXIS, CROSS_SAME_POLARITY, or CROSS_MIXED_POLARITY. Absent from test.
> sample_submission.csv contains the required submission columns and seeded random valid labels.
> Submission
> Submit a CSV with exactly these columns in this order:
> pair_id,relation
> pair_0123456789abcdefabcd,INVERSE_AXIS
> pair_abcdef0123456789abcd,CROSS_MIXED_POLARITY
> Include every test pair_id exactly once. Do not add rows, columns, or index fields. Labels are case-sensitive and must use the exact three-value vocabulary above.
> Evaluation
> Submissions are scored with the multiclass Matthews Correlation Coefficient. Let C be the 3 × 3 confusion matrix, s the number of test examples, c the trace of C, p_k the number of predictions in class k, and t_k the number of true examples in class k:
> MCC = (c × s - Σ_k p_k t_k) / sqrt((s² - Σ_k p_k²)(s² - Σ_k t_k²))
> If the denominator is zero, MCC is defined as 0. The reported score is clip(MCC, 0, 1). Higher is better; perfect predictions score 1, while constant and chance predictions score approximately 0.
> What to use
> Per-waveform centering and amplitude normalization.
> Short-time spectra, temporal envelopes, or learned one-dimensional convolutional features.
> Symmetric pair representations such as absolute feature differences, products, and means.
> Style-clustered or robustness-oriented validation, swap augmentation, and class-balanced training.
> A small Siamese or two-tower network trained entirely from scratch on the public pairs.
> What not to use
> Internet access, hosted APIs, runtime downloads, or external datasets.
> Pretrained speech, audio, language, or embedding models.
> Any attempt to reconstruct source filenames, participant identities, or hidden command metadata.
> pair_id as a predictive feature.
> The benchmark is designed for CPU-only training: 10 CPU cores, 62 GB RAM, and a 90-minute limit.

Inspiration note: Useful because it forces models to learn the task signal from supplied data only, which is ideal for fair CPU-only challenge design.

## Decoding Transformation Sequences on Unseen Typefaces

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7e2n9xkmeaxect1tfs6q39t98a7q7r
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Blind Trajectory Recovery in Morphological Space
> Overview This challenge introduces a novel computer vision benchmark focused on procedural state inference. Your task is to deduce the unobservable generation trajectory of typographic symbols.
> Each example in this dataset is a 40x40 grayscale glyph rendered from a real typeface. After the initial rendering, a hidden, four-step procedural transformation recipe is applied to the spatial structure of the glyph. Because the final output is contrast-renormalized, models cannot rely on pixel-intensity shortcuts. Instead, they must learn to interpret the complex topological residue left behind when non-commutative spatial transformations interact.
> The Task The objective is to recover the exact four-step transformation trajectory, in chronological order, from the final image alone. The four procedural steps are:
> a: erosion (morphological structural thinning)
> b: dilation (morphological structural thickening)
> c: affine-left (geometric skewing)
> d: affine-right (geometric skewing)
> The target variable for an image is a space-separated string of the four letters in chronological order (e.g., b a d c). Predictions are scored by mean per-position accuracy.
> Zero-Shot Typographic Generalization To ensure models learn the mathematical topological signatures rather than memorizing specific visual structures, the dataset split is strictly typeface-disjoint. The 73 source typefaces are partitioned, and 18 are reserved exclusively for the test pool. Every test image is derived from a typeface the model has never encountered.
> Why the task is intrinsically difficult Later transformations partially mask earlier ones, meaning recovering the first step in the trajectory is mathematically harder than the last. Successive skews compose, and erosions/dilations partially invert one another. Consequently, the exact chronological trajectory is intrinsically ambiguous, and the maximum achievable accuracy is capped well below 1.0.
> However, the procedural steps are strictly non-commutative, providing a crucial learnable signal. An erosion followed by a dilation (a topological opening) destroys thin features entirely, whereas a dilation followed by an erosion (a topological closing) fills in gaps and rounds corners differently. This structural residue provides genuine, chronological evidence.
> The difficulty, honestly All figures below are measured on the typeface-disjoint holdout (glyphs from typefaces never seen during training).
> Always predicting the most common step at each position: ~0.25 (chance—the four states are perfectly balanced).
> A gradient-boosted model over hand-crafted structural glyph features (ink, stroke gradients, second moments, and topological residuals): ~0.489
> A small convolutional network trained from scratch with four output heads: ~0.485 (plateaus after ~10 epochs).
> Position by position, the gradient-boosted model scores about 0.433, 0.439, 0.463, and 0.619—the final transformation is the most legible and the first the most obscured, exactly as theoretical masking predicts.
> Note: Because test typefaces are completely unseen, competitors must validate by holding out whole typefaces from their training set rather than relying on random subsets.
> Example Walkthrough Two real rows from the training data (the images are files under images/train/):
> id: train_00000, image: images/train/train_00000.jpg -> ops: "c d c c"
> id: train_00001, image: images/train/train_00001.jpg -> ops: "d b b d"
> Read each label left to right, one letter per chronological step. For the first image (c d c c), the sequence of transformations is explicitly: c (affine-left), followed by d (affine-right), followed by c (affine-left again), followed by c (affine-left a final time).
> Evaluation Submissions are scored by mean per-position accuracy. For each item, the predicted and true strings are split into whitespace-separated tokens and compared position by position over the four positions; the item's score is the fraction of positions predicted exactly, and the final score is the mean over all items, between 0 and 1 (higher is better).
> Dataset Structure Inside public/:
> images/train/ and images/test/: the 40x40 grayscale JPEG glyphs, one file per item.
> train.csv: contains id, image_path, and ops (four space-separated transformation letters).
> test.csv: contains id and image_path only.
> sample_submission.csv: a valid format reference with blank predictions.
> summary.json: JSON object describing the split (n_train and n_test).
> Split sizes: 6,000 training images and 1,500 test images.
> Submission Format One CSV, a header plus one row per test item:
> Code snippet
> id,prediction
> test_00000,c d c c
> test_00001,b a d c
> Strict Challenge Constraints This challenge enforces specific platform guidelines designed to test fundamental algorithm design. Solutions violating these will be rejected:
> Hardware / Time Limits: This is a strictly CPU-only challenge. Your solution must be solvable using only CPU computation (the environment provides 10 CPU cores and 62.5 GB RAM). Total runtime for training and inference combined must strictly not exceed 1.5 hours.
> Prohibited Approaches: Do not frame this as a tabular or regression challenge. Solutions relying on pure tabular regression are banned.
> Pretrained Weights: You must train a model entirely from scratch. Pretrained weights, foundational models, or pretrained feature extractors (e.g., ResNet, VGG) are strictly prohibited. The goal is learning the morphological signatures, not leveraging prior natural-image representations.
> Augmentation Limits: Do not use horizontal-flip augmentation. A horizontal flip geometrically exchanges affine-left with affine-right, meaning it will silently corrupt your sequence labels.
> Hardcoding / Gaming: Predictions copied from the answers, lookup tables keyed to item identifiers, or anything that bypasses learning from the images will be rejected.

Inspiration note: Useful because it forces models to learn the task signal from supplied data only, which is ideal for fair CPU-only challenge design.
## SVG Path Sequence-to-Text Translation

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ak3hs39akq2bnbtd9nwf67h8an717
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering, small-data, image, Dataset source is visible after the challenge closes.
- Best/top context: Be the first to climb the leaderboard!

### Full Challenge Description

> From Scratch: Sequence-to-Sequence SVG Parsing
> Overview This is a from-scratch sequence-to-sequence (seq2seq) generation challenge. There are no images, no rasterization libraries, and no pre-trained vision models that apply here. You are handed a raw mathematical sequence of drawing instructions for a single shape, expressed entirely in the local coordinate space of the designer who authored it. Everything above those raw curve commands is yours to implement.
> Nearly a hundred independent design teams each decided that a particular sequence of Bezier curves signifies a "house," while a different sequence signifies a "magnifying glass." Your task is to build a from-scratch seq2seq generative model. Given a shape's raw SVG path syntax as the input sequence, you must process it and generate the target semantic text sequence that captures its universal geometric meaning.
> Relationship to Prior Art (Novelty & Constraints) While recent benchmarks explore vector graphics, this challenge introduces critical structural constraints that define a distinct seq2seq generative problem class. We explicitly differentiate this challenge from existing literature:
> Pure Sequence Parsing vs. VGBench: VGBench (arXiv:2407.10972) evaluates LLMs on vector understanding but often permits rendered previews or Vision-Language Model (VLM) approaches. This challenge strictly forbids rasterization, forcing pure mathematical sequence-to-sequence generation.
> Algorithmic Efficiency vs. LLM4SVG & OmniSVG: Works like LLM4SVG (arXiv:2412.11102) and OmniSVG empower large models for complex SVG tasks, typically relying on massive parameter counts and GPU acceleration. We deliberately impose a tight 1.5h CPU-only compute budget, demanding lightweight algorithmic seq2seq architectures over brute-force scaling.
> Out-of-Distribution (OOD) Extrapolation vs. HiVG, DuetSVG, & AutomaTikZ: While these works explore joint image/SVG modeling and text-guided synthesis, our dataset strictly evaluates zero-shot grammatical generalization. We enforce a strict disjoint-author split, evaluating solely on 19 held-out design studios whose stroke conventions and grid systems are completely unseen during training.
> Resource Constraints
> The work is deliberately CPU-sized to test algorithmic translation efficiency over brute-force compute. Solutions have a strict limit of at most 1.5 hours on 10 CPU cores and 62.5 GiB RAM.
> Data Files
> The dataset consists of three files.
> train.csv: The training set containing 11,896 aligned sequence-text pairs from 76 design teams.
> id (string): An opaque, salted digest identifier. Unrelated to text token, design team, or split order.
> view_w (integer): Viewbox width in the source team's arbitrary units (e.g., 16, 20, 24, 32, 48, 512, 1024).
> view_h (integer): Viewbox height in the same units. Not always equal to view_w.
> body (string): The shape's raw drawing instructions. Coordinates are expressed in the team's local view_w/view_h units. Path data uses standard absolute and relative vector commands. Example: <path fill="currentColor" d="M12 3L2 12h..."/>
> concept (string): The canonical text string generated to describe the geometry.
> test.csv: The evaluation set containing 3,373 raw sequences from 19 held-out design teams.
> id (string): Opaque identifier.
> view_w (integer): Viewbox width.
> view_h (integer): Viewbox height.
> body (string): Raw drawing sequence.
> sample_submission.csv: A validly formatted submission file demonstrating the expected output schema.
> id (string): Opaque identifier.
> concept (string): The generated semantic text string.
> Leakage Controls & Sanitization
> Disjoint splits: No design team appears in both phases.
> Deduplication: Exact-duplicate bodies are removed corpus-wide to prevent byte-identical sequences from straddling the split.
> Sanitization: Identifier, class, and aria attributes are stripped. Any metadata elements are removed. Any vector whose raw sequence still contained its own concept string was entirely dropped.
> Anonymization: Team and icon names are never published.
> Evaluation
> Submissions are evaluated using a Macro-Averaged String Retrieval Score calculated across the entire vocabulary of expected text tokens.
> For each unique text token
> 𝑣
> v in the vocabulary, we calculate the F1-score (harmonic mean of precision and recall) of its exact generation matches. Let:
> 𝑀
> 𝑎
> 𝑡
> 𝑐
> ℎ
> 𝑒
> 𝑠
> 𝑣
> Matches
> v
> ​
> : The number of times the text token
> 𝑣
> v was correctly generated for its corresponding geometry.
> 𝐸
> 𝑥
> 𝑝
> 𝑒
> 𝑐
> 𝑡
> 𝑒
> 𝑑
> 𝑣
> Expected
> v
> ​
> : The total number of times the text token
> 𝑣
> v appears in the ground-truth evaluation set.
> 𝐺
> 𝑒
> 𝑛
> 𝑒
> 𝑟
> 𝑎
> 𝑡
> 𝑒
> 𝑑
> 𝑣
> Generated
> v
> ​
> : The total number of times your model output the text token
> 𝑣
> v.
> The retrieval score for a specific text token
> 𝑣
> v is calculated as:
> 𝑅
> 𝑒
> 𝑡
> 𝑟
> 𝑖
> 𝑒
> 𝑣
> 𝑎
> 𝑙
> 𝑣
> =
> 2
> ×
> 𝑀
> 𝑎
> 𝑡
> 𝑐
> ℎ
> 𝑒
> 𝑠
> 𝑣
> 𝐺
> 𝑒
> 𝑛
> 𝑒
> 𝑟
> 𝑎
> 𝑡
> 𝑒
> 𝑑
> 𝑣
> +
> 𝐸
> 𝑥
> 𝑝
> 𝑒
> 𝑐
> 𝑡
> 𝑒
> 𝑑
> 𝑣
> Retrieval
> v
> ​
> =
> Generated
> v
> ​
> +Expected
> v
> ​
> 2×Matches
> v
> ​
> ​
> (Note: If the denominator is zero, the score for that text token is defined as
> 0.0
> 0.0. Chance retrieval is approximately
> 0.004
> 0.004).
> The final score is the unweighted mean across all unique text tokens in the vocabulary
> 𝑉
> V:
> 𝑆
> 𝑐
> 𝑜
> 𝑟
> 𝑒
> =
> 1
> ∣
> 𝑉
> ∣
> ∑
> 𝑣
> ∈
> 𝑉
> 𝑅
> 𝑒
> 𝑡
> 𝑟
> 𝑖
> 𝑒
> 𝑣
> 𝑎
> 𝑙
> 𝑣
> Score=
> ∣V∣
> 1
> ​
> ∑
> v∈V
> ​
> Retrieval
> v
> ​
> Submission Format
> Write the final CSV to ./working/submission.csv.
> The concept column must be a string representing one of the expected text tokens in the vocabulary, exactly as spelled in train.csv. Matching is case-insensitive and surrounding whitespace is ignored. Every test id must appear exactly once. Missing ids, duplicate ids, or a missing concept column make the submission invalid.
> Your submission must include a header and be formatted exactly as follows:
> Code snippet
> id,concept
> 0004f0a4d1e2c9,home
> 0012a3b4c5d6e7,search
> 0023b4c5d6e7f8,arrow-right
> Challenge Rules (What Not To Use)
> Do not infer the text from id, row order, CSV order, file size, or any split artefact.
> Strict Web Search Ban: Do not match the published bodies against external vector repositories, APIs, indexes, or search-engine results.
> Do not use external semantic annotations as an inference-time input.
> Do not adapt models using the hidden evaluation sequences.

Inspiration note: Useful as inspiration for route/path reconstruction outputs with explicit evidence structure.
## Mouse Trace to Caption Binding Assignment

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73w4mexbta14fhdxp1qdxrvs8ay19x
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: image, small-data, Dataset source is visible after the challenge closes.
- Best/top context: Beat shikum's score of 0.663!

### Full Challenge Description

> Mouse Trace to Caption Binding Assignment
> Overview
> The Lantern Room preserves narrated visual descriptions for an accessibility archive. During a migration, the ordered phrase cards survived and five trace footprints survived, but the clock linking each phrase to its footprint was lost. The points inside each footprint also lost their temporal order. Your job is to restore the five bindings.
> This is a from-scratch Computer Vision challenge. Every record contains one real photograph, five consecutive natural-language phrases, and five shuffled candidates derived from the human narrator's real mouse trace. Predict which candidate belongs to each phrase. The answer is a one-to-one assignment: language, trace geometry, coarse trace rhythm, localized image appearance, and global consistency can all matter.
> The data contains 4,778 training records and 1,222 test records. Whole anonymous annotator groups are held out: 94 annotators occur only in training and 20 different annotators occur only in test. Source photographs are also unique and disjoint. Public record ids, candidate tokens, and image filenames are independently randomized hexadecimal strings and carry no source identity, split key, order, or label information.
> Evaluation
> The metric is the mean Strict Lantern Binding Score. For one record, let the true and predicted bindings be lists of five candidate tokens in phrase order.
> Position agreement P is the fraction of the five phrases assigned the correct token.
> Exact agreement E is 1 only when the complete five-token binding is correct, and 0 otherwise.
> The row score is 0.80 P + 0.20 E.
> The final score is the arithmetic mean of all 1,222 row scores. Higher is better. The range is 0.0 to 1.0.
> There is no credit for merely preserving relative order. The exact-agreement term rewards a globally coherent solution, while position agreement preserves useful separation among imperfect models.
> The following function is the metric calculation after rows have been aligned by id:
> import numpy as np
> def evaluate(y_true, y_pred):
> def row_score(truth, predicted):
> truth = list(truth)
> predicted = list(predicted)
> if len(truth) != 5 or len(predicted) != 5:
> return 0.0
> if len(set(predicted)) != 5 or set(predicted) != set(truth):
> return 0.0
> position = sum(a == b for a, b in zip(truth, predicted)) / 5
> exact = float(position == 1.0)
> return 0.80  *position + 0.20*  exact
> return float(np.mean([
> row_score(truth, predicted)
> for truth, predicted in zip(y_true, y_pred)
> ]))
> The official grader first performs a strict one-to-one merge on id. A content-invalid binding receives 0.0 for that row. Structural submission errors raise a clean ValueError.
> Dataset
> The prepared public data has this structure:
> train.csv — training records and known bindings.
> test.csv — held-out-annotator records without bindings.
> sample_submission.csv — a label-free display-order baseline in the required submission format.
> images/ — 6,000 metadata-stripped JPEG images with longest side at most 320 pixels.
> train.csv
> id (string) — randomized 16-character record id.
> image_path (string) — relative path to the randomized JPEG under images/.
> phrases (JSON array of five strings) — consecutive narrative phrases in their original language order.
> regions (JSON array of five objects) — shuffled candidate trace footprints.
> binding (string) — five candidate tokens separated by >, in phrase order.
> test.csv
> id (string) — randomized 16-character record id.
> image_path (string) — relative path to the randomized JPEG under images/.
> phrases (JSON array of five strings) — consecutive narrative phrases in their original language order.
> regions (JSON array of five objects) — shuffled candidate trace footprints.
> Each region object contains:
> token (string) — randomized 8-character candidate token used in the submission.
> bbox (array of four numbers) — normalized [x0, y0, x1, y1] robust trace-extent box.
> focus_bbox (array of four numbers) — normalized box around the central 30% of the real trace coordinates, capped to localize image evidence.
> centroid (array of two numbers) — normalized robust trace center.
> trace_cloud (array of twelve coordinate pairs) — real interior mouse points with timestamps removed and point order independently shuffled.
> trace_stats (object) — coarse real-window summaries: point_count, duration, path_length, and mean_speed.
> The five phrases remain ordered, while the region array is shuffled independently. No timestamp, trace endpoint, within-cloud point order, source image id, anonymous annotator id, upstream filename, or exact source clock is public. duration is only a candidate-side summary; phrase timing is held out and must be inferred indirectly from language.
> Submission
> Submit one CSV with exactly two columns in exactly this order: id,binding. Include exactly one row for every test id. Within binding, list all five candidate tokens exactly once, separated by the ASCII > character, in phrase order.
> This format-valid example uses real test ids and candidate tokens. It illustrates format only and does not disclose the answers:
> id,binding
> 85a02a254334000d,3ea1ca37>9b3345a5>e4a55a6b>d944e6a4>e0a03d63
> 7a891639486cd4ec,a362ef4c>ccb17fe8>9b25177b>4d5240bb>a7e52ee2
> 33ffaf74b5b0f3ce,a4df5fb0>1e1f3229>99c99065>21df7952>55e4b268
> Requirements
> The file must have exactly 1,222 rows and exactly the columns id,binding in that order.
> Every test id must appear once. Missing, duplicate, foreign, empty, overlong, or renamed ids are structural errors.
> Extra or renamed columns are structural errors.
> Each binding must contain exactly the five tokens supplied in that row's regions, each used once.
> Whitespace around tokens is ignored.
> Missing values, non-finite values, overlong cells, wrong or Unicode separators, unknown tokens, repeated tokens, list-valued cells, and malformed permutations receive the worst row score of 0.0.
> An entirely content-invalid submission receives the finite score 0.0.
> The grader merges on id; CSV row order has no effect.
> The solution must run on CPU within 90 minutes using at most 10 CPU cores and 62 GB RAM.
> What not to use
> Do not use pretrained image, text, or multimodal weights.
> Do not use external corpora, external images, source websites, web APIs, or runtime downloads.
> Do not hardcode test ids, candidate tokens, or a saved test submission.
> Fit every learned transform on the supplied training records only.
> The intended setting is network-disabled from-scratch learning. Enforcement of the external-data and pretrained-weight rules belongs to the execution harness in addition to this contract.
> #Some extra modelling Information
> This challenge defines a different inference mechanism.
> It removes synchronization, trace endpoints, and within-footprint point order; shuffles five same-image candidates; retains only unordered real trace evidence and coarse rhythm summaries; and requires one globally consistent permutation under an annotator-group holdout.
> Neither caption generation nor mask prediction solves that reconstruction. A successful system must learn language-to-geometry, language-to-rhythm, and language-to-appearance compatibility without a pretrained multimodal encoder.

Inspiration note: Useful for matching/binding tasks across heterogeneous evidence streams.
## Ranking Disordered Voices by Roughness Against Breathiness

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7datmf5vtyb0nmz4yzwfdryh8ar2pn
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: audio, medical, small-data, feature-engineering, Dataset source is visible after the challenge closes.
- Best/top context: Beat nolifecoderz's score of 0.375!

### Full Challenge Description

> Ranking Disordered Voices by Roughness Against Breathiness
> Overview
> When a clinician assesses a disordered voice, they do it by ear. The patient holds a vowel and reads a few standard sentences, and the clinician listens for what is wrong with the sound. Two of the things they listen for are roughness and breathiness, and they are not degrees of the same problem. Roughness is irregular vibration of the vocal folds, a sound that grates. Breathiness is air escaping through folds that fail to close, a sound that leaks. They call for different treatment, and telling which one dominates is a large part of what the assessment is for.
> No instrument does this. Jitter, shimmer and harmonic-to-noise ratio all correlate with a voice being disordered, and none of them separates these two qualities, because irregular vibration and escaping air both raise the same noise measures. That is the whole difficulty, and it is measurable: on this data, a ranking built on how severely disordered the panel judged each voice scores 0.04 against the roughness-breathiness contrast, which is chance. Knowing how bad a voice is tells you nothing about which of the two it is.
> This challenge asks you to make that separation from the audio, and to rank the recordings by it: which voices did the clinical panel hear as rough rather than breathy, and which the other way round.
> Two things stand between you and it.
> The clinicians disagree, including with themselves. You are given every rating, raw. Four clinicians rated every training recording, each of them twice on separate occasions, on both clinical scales, and the ratings are released one row per rating with nothing averaged. A clinician's two passes at the same voice agree with each other only at a rank correlation of about 0.35 to 0.59 on this contrast. The panel as a whole is far steadier: two clinicians against the other two agree at 0.71 on average, which by the Spearman-Brown correction puts the reliability of the full four-clinician target at about 0.83. That is the ceiling here, because it is how well the target agrees with itself. The consensus you are scored against is never given to you; it has to be recovered from opinions that contradict each other.
> The obvious signal is the wrong one. Overall severity is easy and useless here. The same acoustic descriptors that reach a rank correlation of 0.66 against panel severity reach far less against this contrast, and a ranking built on severity itself scores 0.00. How disordered a voice is and which of the two qualities dominates are separate questions, and only the second one is asked. Nothing about the speaker is provided to lean on either: no diagnosis, no age, no gender, no rating of any kind for the test recordings.
> Task
> For every recording_id in test.csv, output a real-valued score where a higher score means the panel heard the voice as more rough relative to breathy, and a lower score means more breathy relative to rough. Only the ranking your scores induce is read, so the scale is free.
> Data
> All inputs are under dataset/public/:
> audio/<recording_id>.wav: the recording, mono, 44.1 kHz. Each is one speaker producing sustained vowels and the six sentences of the standard clinical protocol. Median length about 23 seconds. One recording per speaker, so training and test speakers are entirely separate people.
> train_ratings.csv: the training material, one row per single rating, nothing averaged. Columns:
> recording_id (string): the recording rated, matching a file in audio/.
> scale (string): CAPE-V, a 0 to 100 visual analogue scale, or GRBAS, a 0 to 3 ordinal scale.
> dimension (string): what was judged. CAPE-V has severity, roughness, breathiness, strain, pitch, loudness; GRBAS has grade, roughness, breathiness, asthenia, strain.
> rater (string): which clinician, r1 to r4. The same four rated everything, so a clinician's habits are learnable.
> session (integer): 1 or 2. Each clinician rated every recording twice, at different times.
> rating (float): the rating itself, on that row's scale.
> test.csv: column recording_id, the recordings to rank. No ratings of any kind are given for these.
> sample_submission.csv: a correctly formatted submission for every test recording. Its scores are an arbitrary placeholder, so it is valid and ranks nothing meaningful.
> The panel consensus for the test recordings is held out privately and used only for scoring.
> How the audio was prepared, and why. These voices come from a public research database that publishes the very ratings this challenge scores, so a clip that could be matched back to its source would hand over the answer. Salted ids are not enough, because a recording can be matched by its sound. Every clip released here is therefore re-derived: a randomly shaped filter is applied that keeps changing every 0.4 seconds, and the 0.4-second segments are then shuffled. Roughness and breathiness are properties of how the voice sounds moment to moment, and both survive this intact, which is why the reference still works. What does not survive is the pattern that identifies a particular speaker. Measured: matching a released clip back to its source recording with cepstral-mean-subtracted MFCCs, the standard channel-robust method, falls from 100% on untouched audio to 7% here. The clips will sound chopped up. That is deliberate, and the task does not depend on the words or the order they come in.
> Evaluation
> Submissions are scored by Spearman's rank correlation between your scores and the panel's consensus contrast on the fine scale, which is the mean CAPE-V roughness minus the mean CAPE-V breathiness over all four clinicians and both sessions:
> score = max(0, spearman(your score, panel roughness - panel breathiness))
> Ties are handled with averaged ranks. A perfect ranking scores 1, and because the result is clipped at 0, an unrelated ranking and a reversed one both score 0. For calibration on this exact split:
> ApproachSpearmanThe supplied sample submission0.00Ranking by how severely disordered the panel judged the voice0.00Classical acoustic descriptors with a gradient-boosted model (the reference)0.21The panel's agreement with itself, which is the ceiling0.83
> Most of the distance between 0.21 and 0.83 is still open.
> Submission format
> Write ./working/submission.csv with exactly these columns:
> recording_id,score
> v_1a2b3c4d5e6f7a,12.5
> v_2b3c4d5e6f7a8b,-8.0
> ...
> Exactly one row per recording_id in test.csv, and no others. A submission that omits a recording, repeats one, or names an unknown one is rejected.
> score is any finite real number; only the order it induces is used.
> Start from sample_submission.csv to guarantee the correct id set, and write with index=False.
> Constraints
> Read the challenge inputs only from ./dataset/public/. Write your output only to ./working/submission.csv.
> CPU only: 10 cores, 62 GB of memory, and a hard limit of 1.5 hours for the whole run. There is no GPU. The reference solution finishes in a couple of minutes, so there is room to train something of your own.
> Train from scratch. No pretrained weights of any kind. Do not download a checkpoint from a model hub and do not initialise from anything trained elsewhere. Every parameter you use must be fitted on the data provided here. Pretrained speaker-recognition models exist precisely to tell one voice from another, which is the thing this challenge deliberately removes, so they are out of scope.
> No package installs (no pip or conda install). You may use the preinstalled libraries (numpy, scipy, pandas, scikit-learn, pytorch, and so on).
> A few source recordings carry slightly malformed WAV headers. scipy.io.wavfile.read handles them with a warning; make sure your loader does not crash on them.
> What Not To Use
> Do not try to identify the source recordings or look up their published ratings. The audio was re-derived specifically to make that fail, and the measured match rate is 7%, but do not attempt it. Judge from the provided audio and the raw training ratings.
> Do not hardcode outputs or otherwise bypass learning from the data.
> A learning-based approach is expected. The raw ratings are the interesting part: they disagree, so how you turn eight opinions per recording into something to fit against is a real modelling decision, and a clinician who contradicts themselves is evidence about how uncertain that voice is, not just noise to average away. On the audio side, the two qualities differ in where their noise sits and how the harmonic structure breaks down, so descriptors of spectral shape, harmonic strength and the high-frequency band are the natural place to start, and a small model of your own trained on those, or on the spectrogram directly, is the natural next step.

Inspiration note: Useful because it introduces a distinctive task pattern, output shape, or leakage-control trick that can inspire new challenge ideas.
## From-Scratch Protein Family Pair-Dependency Modeling

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75ztsrvyksb2t1j7h9cas1jx89g8k8
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↓ Lower is better
- Tags: text, feature-engineering, small-data, medical, Dataset source is visible after the challenge closes.
- Best/top context: Beat racer34's score of 0.299!

### Full Challenge Description

> From-Scratch Protein Family Pair-Dependency Modeling
> Related protein sequences contain structured information that is not visible from isolated residues alone. Within a protein-family context, pairs of positions may show coordinated dependency patterns driven by structural compatibility, compensatory substitution, functional pressure, stability constraints, or shared family-level effects. This challenge asks participants to build a model or algorithm from scratch to assign dependency-priority values to held-out residue pairs in unseen anonymized family contexts using only the released sequence-family tables.
> Problem Domain
> This is a From Scratch modeling challenge in Biology & Bioinformatics / Molecular Informatics.
> Participants must build their own modeling pipeline, feature extraction approach, ranking method, or algorithmic solution from the released sequence-family tables. No pretrained model, external structure file, contact map, interaction graph, public label table, internet access, or hidden metadata is required.
> Each anonymized protein-family context acts as an independent modeling context. The candidate rows are residue-position pairs. Participants must infer which residue pairs should receive higher family-conditioned dependency-priority values.
> The central task is:
> Given an unseen protein-family context, build a from-scratch method that assigns coupling_index values to residue pairs according to their family-conditioned dependency priority.
> Overview
> This benchmark, codename EPILOCK, is focused on from-scratch residue-pair dependency modeling across anonymized protein-family contexts.
> Each family context is represented by a reference amino-acid sequence, aligned sequence records, sparse single-position observations, and residue-pair rows. For each pair row, the column coupling_index provides the target dependency-priority value for two residue positions within the same family context. Participants must assign one coupling_index value per held-out pair_id.
> The main difficulty is cross-context generalization: training and test pairs come from disjoint family contexts, so successful methods must transfer beyond context-specific memorization. The official assessment emphasizes within-context ordering, meaning that placing stronger residue-pair dependencies above weaker ones inside each unseen family context matters more than global calibration alone.
> A useful from-scratch solution must combine evidence from aligned sequence variation, conservation patterns, sparse local observations, and pair-level features. Simple metadata, row order, sequence length, position distance, or single-position observations alone are intentionally insufficient.
> This is not a single-sequence scoring task, not a binary contact-map recovery task, not ordinary mutation-effect modeling, and not a lookup problem over known public interaction labels. The goal is to model residue-pair dependency priority from the released sequence-family evidence.
> Task
> You are given prepared public sequence-family tables.
> Build a from-scratch method using only the released files.
> Submit one coupling_index value for each test pair_id.
> Submitted entries are assessed mainly by within-context pair-ordering quality.
> Lower official score is better.
> Training rows provide coupling_index examples within [-1, 1].
> Submitted entries must be finite and lie in [-1, 1].
> Public Data Files and Features
> All files are linked by landscape_id, an anonymized identifier for a protein-family context. Residue-pair rows are linked across files by landscape_id together with pos_i and pos_j.
> Training and test pairs come from disjoint family contexts, so participants should use context-aware validation rather than random row splits.
> landscapes.csv
> ColumnTypeDescriptionlandscape_idstringAnonymized identifier for a protein-family context.seq_lenintegerNumber of residue positions in the family context; also the aligned-record width.wt_sequencestringReference amino-acid sequence using the alphabet ACDEFGHIKLMNPQRSTVWY.
> alignments.csv
> ColumnTypeDescriptionlandscape_idstringIdentifier linking the aligned sequence record to a family context.seq_indexintegerRow index of the aligned sequence record within that context's family table.sequencestringAligned amino-acid sequence with length equal to seq_len.
> singles.csv
> ColumnTypeDescriptionlandscape_idstringFamily-context identifier.posinteger0-based residue position.aa_fromstringReference amino acid at the position.aa_tostringSubstituted amino acid.single_effectnumeric value in [-1, 1]Sparse single-position observation for a residue substitution.
> train.csv
> ColumnTypeDescriptionpair_idstringAnonymized identifier for a residue-position pair.landscape_idstringFamily context containing the pair.seq_lenintegerSequence length / aligned-record width.pos_iinteger0-based first position of the pair.pos_jinteger0-based second position of the pair, with pos_i < pos_j.coupling_indexnumeric value in [-1, 1]Pair-dependency target for training rows; higher entries indicate stronger residue-pair dependency priority within the family context.
> test.csv
> ColumnTypeDescriptionpair_idstringAnonymized identifier for a test residue-position pair.landscape_idstringFamily context containing the test pair.seq_lenintegerSequence length / aligned-record width.pos_iinteger0-based first position of the pair.pos_jinteger0-based second position of the pair, with pos_i < pos_j.
> sample_submission.csv
> ColumnTypeDescriptionpair_idstringTest pair identifier.coupling_indexnumeric value in [-1, 1]Submitted value; must be finite and in [-1, 1].
> sample_submission.csv is a format template only — its placeholder entries are not labels, priors, or hints.
> Biological Meaning of coupling_index
> In protein-family analysis, residue positions are often constrained by more than their individual amino-acid preferences. Two positions may show a dependency because a change at one site is compatible only with particular states at another site, or because both sites participate in a shared structural, functional, or stability-related constraint.
> The column coupling_index is a bounded benchmark field representing the family-conditioned priority of a dependency signal between two residue positions. Higher entries indicate stronger evidence that the two positions behave as a coordinated pair within the same family context. Lower entries indicate weaker or absent pair-level dependency.
> The field is designed around residue-pair reasoning patterns commonly encountered in protein-family analysis, including:
> structural compatibility pressure between positions;
> compensatory substitution behavior;
> family-specific conservation and variability;
> stability- or function-related constraints;
> indirect dependencies mediated by other positions;
> separation of local single-position effects from joint pair-level evidence.
> coupling_index should be interpreted as a residue-pair dependency-priority value. It is not provided as a direct contact map, structure file, distance matrix, or experimental interaction table. The competition objective is to infer this hidden pair-dependency ordering from the released sequence-family evidence.
> The exact construction of the hidden endpoint is intentionally not disclosed. This protects the held-out answers from deterministic reconstruction and keeps the task focused on generalizable from-scratch modeling.
> Biological Validation Rationale
> The released records are structured to preserve the evidence patterns needed for biologically meaningful residue-pair reasoning:
> all sequences use the standard 20-letter amino-acid alphabet;
> each family context has a reference sequence and aligned sequence records of shared width;
> positions exhibit heterogeneous conservation and variability;
> sparse single-position observations provide local residue-level information;
> residue-pair rows require joint reasoning over two positions;
> family contexts are disjoint between training and evaluation;
> shallow metadata such as identifiers, row order, sequence length, and position distance are insufficient;
> single-position observations alone are insufficient;
> rank-aware assessment rewards recovery of pair-signal ordering inside unseen family contexts.
> This setup reflects a common bioinformatics workflow: using related sequences to prioritize residue pairs whose joint behavior is stronger than expected from isolated positions or simple positional metadata.
> The benchmark is controlled and reproducible, but the reasoning task is biologically motivated: identify which residue pairs should appear higher in a family-specific dependency-priority list after comparing sequence variation across a family context.
> Modeling Column
> coupling_index is the modeling column used for submissions.
> Training rows include examples within [-1, 1].
> Held-out rows are assessed by the platform.
> Higher entries correspond to higher family-conditioned pair-dependency priority.
> Lower entries correspond to weaker or absent pair-dependency priority.
> Submitted entries must be finite and in [-1, 1].
> The exact construction of the hidden endpoint is not disclosed.
> Evaluation
> The official metric is the Weighted Pair-Rank Dependency Score. It is a non-standard, minimize-oriented metric bounded to [0, 1]. It blends a bounded pairwise consistency component, valid-range/sign consistency, and the correctness of within-context ordering of the pair-dependency signal.
> For each evaluated pair
> 𝑘
> k with submitted score
> 𝑝
> 𝑘
> p
> k
> ​
> and ground-truth
> 𝑡
> 𝑘
> t
> k
> ​
> (with
> sign
> ⁡
> (
> 0
> )
> =
> 0
> sign(0)=0):
> 𝑒
> 𝑘
> =
> ∣
> 𝑝
> 𝑘
> −
> 𝑡
> 𝑘
> ∣
> 2
> ,
> 𝑠
> 𝑘
> =
> 1
> !
> [
> sign
> ⁡
> (
> 𝑝
> 𝑘
> )
> ≠
> sign
> ⁡
> (
> 𝑡
> 𝑘
> )
> ]
> ⋅
> ∣
> 𝑡
> 𝑘
> ∣
> +
> ∣
> 𝑝
> 𝑘
> ∣
> 2
> ,
> ℓ
> 𝑘
> =
> 0.6
> ⋅
> 𝑒
> 𝑘
> +
> 0.4
> ⋅
> 𝑠
> 𝑘
> e
> k
> ​
> =
> 2
> ∣p
> k
> ​
> −t
> k
> ​
> ∣
> ​
> ,s
> k
> ​
> =1![sign(p
> k
> ​
> )
> 
> =sign(t
> k
> ​
> )]⋅
> 2
> ∣t
> k
> ​
> ∣+∣p
> k
> ​
> ∣
> ​
> ,ℓ
> k
> ​
> =0.6⋅e
> k
> ​
> +0.4⋅s
> k
> ​
> 𝐿
> pair
> =
> ∑
> 𝑘
> 𝑤
> 𝑘
> ⋅
> ℓ
> 𝑘
> ∑
> 𝑘
> 𝑤
> 𝑘
> ,
> 𝐿
> rank
> =
> ∑
> 𝑔
> 𝑚
> 𝑔
> ⋅
> 1
> −
> 𝜌
> 𝑔
> 2
> ∑
> 𝑔
> 𝑚
> 𝑔
> ,
> SCORE
> =
> 0.2
> ⋅
> 𝐿
> pair
> +
> 0.8
> ⋅
> 𝐿
> rank
> L
> pair
> ​
> =
> ∑
> k
> ​
> w
> k
> ​
> ∑
> k
> ​
> w
> k
> ​
> ⋅ℓ
> k
> ​
> ​
> ,L
> rank
> ​
> =
> ∑
> g
> ​
> m
> g
> ​
> ∑
> g
> ​
> m
> g
> ​
> ⋅
> 2
> 1−ρ
> g
> ​
> ​
> ​
> ,
> SCORE=0.2⋅L
> pair
> ​
> +0.8⋅L
> rank
> ​
> ​
> where:
> 𝑒
> 𝑘
> e
> k
> ​
> is the bounded pairwise consistency term;
> 𝑠
> 𝑘
> s
> k
> ​
> is the sign-consistency penalty;
> ℓ
> 𝑘
> ℓ
> k
> ​
> is the per-pair consistency contribution;
> 𝑤
> 𝑘
> w
> k
> ​
> is an internal evaluation emphasis factor used by the scorer;
> 𝜌
> 𝑔
> ρ
> g
> ​
> is the within-context Spearman rank correlation between submitted values and reference values inside family context
> 𝑔
> g;
> 𝑚
> 𝑔
> m
> g
> ​
> is the number of assessed pairs in family context
> 𝑔
> g.
> Contexts with constant submissions or fewer than 5 assessed pairs contribute a neutral value to the ordering term.
> Lower score is better.
> Submission Handling
> Submissions are matched to the evaluation set by pair_id in an order-independent way, comparing IDs as whitespace-stripped strings.
> Structurally malformed submissions receive the controlled worst official score of 1.0. This includes wrong, extra, missing, or duplicate columns; duplicate, missing, or unexpected IDs; and empty files.
> Individual invalid entries, including non-numeric entries, NaN, ±Inf, or entries outside [-1, 1], receive the worst per-pair contribution and are not silently clipped. Valid constant submissions are accepted, but they do not provide useful within-context ordering.
> Submission Format
> ColumnTypeRequiredConstraintspair_idstringYesMust exactly match the test IDs; no duplicates, missing, or extra IDs.coupling_indexnumeric valueYesMust be finite and in [-1, 1].
> Example of a correctly formatted submission file:
> pair_id,coupling_index
> pair_000001,0.42
> pair_000002,0.08
> pair_000003,0.77
> Submitted entries must be finite and lie in [-1, 1]. Exactly these two columns, in this order; one row per test pair_id; no index column; no extra columns. Write the final file to:
> ./working/submission.csv
> Why This Benchmark Is Distinct
> The benchmark is organized around many anonymized family contexts, not one reusable family table.
> Training and evaluation contexts are disjoint, so context memorization is not enough.
> The task is a from-scratch context-aware residue-pair modeling challenge, not a binary contact-label task.
> The official assessment combines bounded consistency with rank-dominant within-context ordering.
> Public evidence is distributed across reference sequences, aligned sequence records, sparse single-position observations, and pair rows.
> No explicit structure file, contact map, distance matrix, or interaction graph is provided.
> Identifiers, row order, length, and position distance are intentionally insufficient.
> The task evaluates cross-family residue-pair dependency modeling under controlled and reproducible conditions.
> What Makes the Task Hard
> Cross-context transfer is central: training and test family contexts do not overlap.
> Pair ordering must be inferred from finite family-level evidence.
> Local single-position observations are useful but incomplete.
> Some dependencies are direct, while others are indirect or context-dependent.
> Similar residue pairs can have different priority depending on the surrounding family context.
> Correct ordering inside each unseen context matters more than global calibration alone.
> Shallow tabular shortcuts are intentionally insufficient.
> The challenge rewards pair-aware biological reasoning rather than memorization.
> Why This Transfers to Real Residue-Pair Modeling
> Many bioinformatics workflows require prioritizing residue pairs when direct experimental labels or structure files are unavailable. In those settings, related sequences provide indirect evidence: conservation, coordinated variation, local substitution effects, and family-specific constraints can all help identify pairs worth further analysis.
> This benchmark captures that workflow in a controlled from-scratch modeling form. Participants must use sequence-family tables to model pair-dependency signals inside held-out family contexts. The rank-aware assessment rewards the ability to place stronger pair dependencies above weaker ones within each unseen context, which is aligned with residue-pair screening, candidate-pair prioritization, and exploratory protein-family analysis.
> Scope and Limitations
> The released endpoint should be treated as a benchmark pair-dependency field.
> The task is intended for modeling, ranking, and prioritization of residue-pair dependencies.
> It is not a definitive structural-contact annotation task.
> It does not provide participants with explicit contact maps, structure files, distance matrices, or experimental interaction tables.
> The benchmark is designed for controlled, reproducible assessment of cross-family pair-dependency ordering.
> The hidden endpoint construction is not disclosed to prevent leakage and deterministic reconstruction.
> Public documentation explains the biological motivation and validation rationale without exposing private answers or hidden construction details.
> Validation Advice
> Hold out whole family contexts, mirroring the train/test separation.
> Avoid random row splits — pairs from one context share a family table, so random splits overstate cross-context transfer.
> Check whether your ordering within each context is stable across held-out contexts.
> Track both value agreement and within-context ranking quality during local validation.
> Common Traps
> Treating identifiers or row order as meaningful.
> Distance-only reasoning between positions.
> Treating single-position observations as sufficient.
> Treating sample-submission entries as hints.
> Using random row splits instead of context-aware validation.
> Adding extra columns to the submission file.
> Submitting values outside [-1, 1].
> Data Use Notes
> pair_id and landscape_id are opaque strings; do not parse meaning from them.
> Positions are 0-based.
> Sequences use the 20-letter amino-acid alphabet ACDEFGHIKLMNPQRSTVWY.
> No external data or network access is required; use only the released challenge files.
> The sample submission is a template, not a prior.
> Execution Requirements
> Participants must build their solution using only the released challenge files.
> The benchmark is designed for reproducible execution on the provided CPU environment and does not require GPU acceleration.
> Solutions must comply with the platform execution rules, resource limits, and challenge constraints.
> External datasets, pretrained models, online services, internet access, hidden challenge artifacts, or additional non-public resources must not be used.
> The intended solution workflow is fully compatible with CPU-only execution. Efficient feature engineering, statistical analysis, classical machine learning, or other from-scratch approaches are sufficient for solving the benchmark within the provided execution environment.

Inspiration note: Useful for graph/scaffold reconstruction tasks with decoys and consistency scoring.

## Latent Market Contagion Graph and Intervention Ledger Recovery

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx739d1eyd8rm366n8xbjwv21x8bg913
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: finance
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Stress-testing a connected market requires more than predicting a single loss number. A risk system must infer which assets transmit stress to which others, distinguish transmission mechanisms, forecast how severity evolves round by round, estimate the effect of a targeted support action, and explain the resulting cascade in causal order.
> Plain-language objective: infer how stress travels through one anonymous market, predict the five-round outcome with and without one support action, and submit the hidden graph, both trajectories, the ordered activation ledger, and confidence.
> Each example describes one anonymous synthetic market with 7–10 assets. You receive normalized per-asset attributes, safe macro context, noisy partial evidence about directed exposures, and four partially observed five-round stress probes. A separate query identifies an asset to shock and an asset to support. Your job is to recover the latent typed directed contagion backbone and predict both the factual and intervention trajectories, together with an ordered activation ledger and calibrated confidence.
> The corpus is procedurally generated from independent latent market worlds rather than copied from real institutions. Each world samples normalized balance-sheet resilience, liquidity, funding, credit, cross-asset, and macro-stress proxies; it then samples a typed directed exposure network and simulates several shocks over five rounds. The four public probes are incomplete, noisy views of that same world. The held-out query uses a new shock/support pair and a shared hidden innovation, so participants must learn graph structure and propagation behavior rather than reproduce a deterministic public formula. All values are synthetic proxies, not measurements of real assets or institutions.
> This is a CPU-only structured graph-and-sequence challenge. Solutions must finish within 1.5 hours on 10 CPU cores and 62 GB RAM. The intended solution is a compact graph/event neural network trained from random initialization on the supplied labelled training worlds. The CSV files are indexes and structured targets; the modeling inputs are fixed multi-axis NPZ tensors. This is not a tabular classification task and not scalar regression.
> Use only the active asset slots indicated by node_mask; asset indices are local to each row and range from 0 to n_assets-1. Padding slots must be ignored. Four edge mechanisms are allowed: cross_asset, funding, credit, and liquidity. Severity tiers are categorical integers: 0 means inactive and 1..4 indicate increasing stress. Backbone strength tiers are 1..3.
> For every test row predict:
> backbone_json: the typed directed hidden contagion graph.
> query_profile_json: the factual five-round severity matrix.
> intervention_profile_json: the five-round severity matrix after the specified support action.
> activation_ledger_json: the ordered first-activation ledger for the factual query.
> confidence: the estimated probability that the structured row is substantially correct.
> The factual and intervention profiles share the same unobserved market innovation for a row, so their difference represents the support action rather than unrelated resampling. Predictions should express expected behavior learned across training worlds; the hidden innovation is a legitimate source of uncertainty and should be reflected in confidence.
> Intended approach
> A suitable baseline builds per-asset embeddings from node_features, aggregates the masked probe trajectories and actions, performs message passing over candidate directed pairs using exposure_hints, and decodes edge classes plus round-by-asset severity classes. The activation ledger can be decoded autoregressively or derived with a constrained event head. Train the compact network from scratch on CPU; batches of 128–256 small graphs keep the workload efficient. The measured 226,431-parameter reference trains for 18 epochs in 36.37 seconds on ten CPU threads, infers all 1,180 test rows in 0.41 seconds, and uses about 810 MiB peak process memory. A stronger system can use multiple message-passing blocks, masked temporal attention over probes, structured decoding, consistency-aware losses, and small calibrated ensembles while remaining comfortably inside the 90-minute limit. Use only the labelled training split for validation, model selection, and confidence calibration.
> Relation to prior work
> Graph inference from cascades traditionally targets recovery of graph edges from observed propagation, as in Pouget-Abadie and Horel, 2015. Financial-network reconstruction work estimates hidden directed/weighted exposure structure and systemic-risk properties from partial information, as in Cimini et al., 2015. Reverse stress testing instead searches for shocks that produce a target loss, as in Grigat and Caccioli, 2017.
> This benchmark combines capability axes those tasks usually separate: multi-probe latent typed-graph recovery, factual multi-round forecasting, a targeted intervention counterfactual, an ordered parent/mechanism ledger, and calibrated cross-output consistency. The target is not merely a graph statistic, a final scalar, a trigger class, or a JSON wrapper around one of those tasks.
> What Not To Do
> Do not access or probe private files, answer keys, hidden split metadata, or organizer-only artifacts.
> Do not replay, reverse engineer, or copy outputs from the corpus generator or raw target table. Solve from public/ inputs and labelled training examples only.
> Do not use IDs, CSV order, NPZ row order, file sizes, hashes, archive metadata, or serialization details as prediction features.
> Do not submit fixed templates, hand-authored rule tables, nearest-row answer dictionaries, or hard-coded output maps as the primary method.
> Do not use hosted or closed-source APIs, GPUs, accelerators, or runtime internet for training, inference, pseudo-labeling, or distillation.
> Do not use pretrained weights or external datasets tailored to contagion reconstruction. The required model must be trained from scratch on the supplied training split.
> Do not exploit malformed JSON, non-finite values, duplicate IDs, parser limits, or grader behavior.
> Do not classify the market or predict only a scalar while leaving the graph, temporal profiles, or ledger as decorative constants.
> Enforcement on invalid approaches: rule-only solutions, generator replay, source lookup, hard-coded answer recovery, private-data access, GPU-dependent systems, or methods that avoid learned CPU graph-and-sequence modeling may be rejected before payout regardless of leaderboard score.
> Evaluation
> Higher is better. Every valid row receives four task scores and one consistency score.
> For set F1, F1(P,G)=1 when both sets are empty, 0 when exactly one is empty, and otherwise 2|P∩G|/(|P|+|G|).
> G_exact = F1 of (source,destination,mechanism,strength_tier) edges
> G_topo  = F1 of (source,destination) edges
> G       = 0.80*G_exact + 0.20*G_topo
> Q = exact categorical accuracy over all 5*n_assets factual profile cells
> I = exact categorical accuracy over all 5*n_assets intervention cells
> Ledger events are matched one-to-one by asset. For a matched event:
> round_credit     = max(0, 1 - abs(pred_round-true_round)/2)
> parent_credit    = 1 if parents match, else 0
> mechanism_credit = 1 if mechanisms match, else 0
> severity_credit  = 1 exact, 0.5 adjacent tier, else 0
> event_credit     = 0.35*round_credit + 0.25*parent_credit
> + 0.20*mechanism_credit + 0.20*severity_credit
> L = 2*sum(event_credit)/(n_pred_events+n_true_events)
> If both ledgers are empty, L=1; if exactly one is empty, L=0.
> Consistency C is computed only from the participant's own graph, factual profile, and ledger. For each of the n_assets active asset slots, let f_a be the first round whose predicted factual severity is positive, or none if every predicted severity is zero. Let e_a be that asset's predicted ledger event, if present. Define R_a=1 when e_a is direct (parent=-1 and mechanism="direct"), or when the predicted backbone contains the edge (e_a.parent,a) with exactly e_a.mechanism; otherwise R_a=0.
> if f_a is none:                 c_a = 1[e_a is absent]
> if f_a exists and e_a absent:  c_a = 0
> otherwise:                     c_a = 0.40*1[e_a.round = f_a]
> + 0.30*1[e_a.severity_tier = Q[f_a,a]]
> + 0.30*R_a
> C = (1/n_assets) * sum(c_a over active asset slots)
> base  = 0.30*G + 0.25*Q + 0.23*I + 0.22*L
> joint = min(G,Q,I,L)
> task  = (0.60*base + 0.40*joint) * (0.92 + 0.08*C)
> calibration = 1 - abs(confidence-task)
> row_score   = task * (0.95 + 0.05*calibration)
> Final       = mean(row_score)
> The theoretical range is [0,1]. A perfect valid submission scores exactly 1.0. Structural file errors—wrong or reordered columns, duplicate IDs, missing/extra IDs, or non-finite/out-of-range confidence—raise InvalidSubmissionError. A row with malformed, oversized, out-of-range, or internally inconsistent JSON safely receives zero for that entire row; other rows continue to score normally.
> Dataset
> All participant-visible files are under public/. train.csv contains 4,820 labelled rows and test.csv contains 1,180 unlabelled rows. signal_row indexes the first dimension of the corresponding NPZ file. The split holds out complete market-world families: no query, tensor packet, or asset permutation from one world crosses the boundary.
> File overview
> | Item | Description |
> |---|---|
> | `train.csv` | Train index and labels |
> | `test.csv` | Test index only |
> | `sample_submission.csv` | Valid weak template |
> | `train_signals.npz` | Training tensors |
> | `test_signals.npz` | Test tensors |
> | `tensor_schema.json` | Tensor dimensions |
> The NPZ keys, data types, shapes, and axis meanings are:
> | Key | Data type | Shape | Meaning |
> |---|---|---|---|
> | `node_features` | `float32` | `[rows,10,8]` | Eight normalized attributes for each padded asset slot |
> | `node_mask` | `int8` | `[rows,10]` | `1` for an active asset slot and `0` for padding |
> | `exposure_hints` | `float32` | `[rows,10,10,3]` | Three noisy evidence channels for each ordered source/destination pair |
> | `probe_trajectories` | `float32` | `[rows,4,5,10]` | Normalized continuous stress, indexed by probe, round, and asset |
> | `probe_mask` | `int8` | `[rows,4,5,10]` | `1` where a probe value is observed and `0` where it is hidden |
> | `probe_actions` | `int16` | `[rows,4,3]` | Three action fields for each of the four public probes |
> | `macro_features` | `float32` | `[rows,6]` | Six normalized market-wide context values |
> | `query` | `int16` | `[rows,4]` | Four integer fields specifying the held-out shock and support action |
> All float32 feature channels are synthetic normalized proxies. Their channel order is fixed:
> | Tensor | Channel | Feature name | Data type | Description |
> |---|---:|---|---|---|
> | `node_features` | 0 | normalized market size | `float32` | Relative size of the anonymous asset within its market world |
> | `node_features` | 1 | liquidity buffer | `float32` | Capacity to absorb short-term liquidity stress |
> | `node_features` | 2 | funding resilience | `float32` | Resistance to disruption in funding channels |
> | `node_features` | 3 | cross-asset concentration | `float32` | Dependence on cross-asset transmission channels |
> | `node_features` | 4 | funding dependence | `float32` | Reliance on external or interconnected funding |
> | `node_features` | 5 | credit fragility | `float32` | Sensitivity to counterparty credit stress |
> | `node_features` | 6 | capital buffer | `float32` | Capacity to absorb propagated losses |
> | `node_features` | 7 | anonymous sector coordinate | `float32` | Source-neutral latent position used to express sector similarity |
> | `exposure_hints` | 0 | exposure intensity | `float32` | Noisy evidence for the magnitude of a directed exposure |
> | `exposure_hints` | 1 | mechanism coordinate | `float32` | Noisy numeric clue about the exposure mechanism; it is not a target token |
> | `exposure_hints` | 2 | node similarity | `float32` | Noisy similarity between the source and destination attributes |
> | `macro_features` | 0 | credit stress | `float32` | Market-wide credit pressure |
> | `macro_features` | 1 | broad volatility | `float32` | General market volatility level |
> | `macro_features` | 2 | cross-asset coupling | `float32` | Market-wide strength of cross-asset co-movement |
> | `macro_features` | 3 | funding pressure | `float32` | Market-wide funding strain |
> | `macro_features` | 4 | liquidity strain | `float32` | Market-wide liquidity pressure |
> | `macro_features` | 5 | policy accommodation | `float32` | Market-wide support or accommodation context |
> The integer action tensors use these fields:
> Tensor	Field	Feature name	Data type	Description
> probe_actions	0	trigger asset	int16	Row-local asset index shocked in that public probe
> probe_actions	1	shock tier	int16	Categorical initial shock tier from 1 through 3
> probe_actions	2	reserved zero	int16	Reserved field; always zero in this version
> query	0	trigger asset	int16	Row-local asset index for the factual shock
> query	1	shock tier	int16	Factual initial shock tier from 1 through 3
> query	2	support asset	int16	Row-local asset index receiving the intervention
> query	3	support tier	int16	Intervention strength tier from 1 through 3
> train.csv columns
> | Column | Type | Description |
> |---|---|---|
> | `id` | string | Opaque row id |
> | `signal_row` | int | NPZ row index |
> | `n_assets` | int | Active asset count |
> | `backbone_json` | string | Edge labels |
> | `query_profile_json` | string | Factual labels |
> | `intervention_profile_json` | string | Support labels |
> | `activation_ledger_json` | string | Event labels |
> ### test.csv columns
> Column	Type	Description
> id	string	Opaque row id
> signal_row	int	NPZ row index
> n_assets	int	Active asset count
> ## Submission
> Write `./working/submission.csv` with exactly these columns in this exact order:
> Column	Type	Constraint
> id	string	Exact test id set
> backbone_json	JSON string	Edge list
> query_profile_json	JSON string	5 × n_assets tiers
> intervention_profile_json	JSON string	5 × n_assets tiers
> activation_ledger_json	JSON string	Ordered event list
> confidence	float	Finite in [0,1]
> `backbone_json` is a JSON list with at most `n_assets*(n_assets-1)` unique directed edges. Every edge must contain exactly:
> {"source":0,"destination":2,"mechanism":"funding","strength_tier":2}
> `query_profile_json` and `intervention_profile_json` are lists of exactly five lists, each containing exactly `n_assets` plain integers from 0 through 4.
> `activation_ledger_json` contains at most one event per asset and must be sorted by `(round,asset)`. Every event must contain exactly:
> {"asset":2,"round":1,"parent":0,"mechanism":"funding","severity_tier":1}
> Use `parent:-1` with `mechanism:"direct"` for an exogenous activation. Any nonnegative parent must have activated in an earlier round and the mechanism must be one of the four backbone mechanisms.
> Example format-valid weak row (shown only as syntax; it is not a private answer):
> id,backbone_json,query_profile_json,intervention_profile_json,activation_ledger_json,confidence mcl_0042c076b1240630,[],"[[0,0,0,1,0,0,0,0],[1,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1],[2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2]]","[[0,0,0,1,0,0,0,0],[1,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1],[2,2,2,2,1,2,2,1],[2,2,2,2,2,2,2,2]]","[{""asset"":3,""mechanism"":""direct"",""parent"":-1,""round"":0,""severity_tier"":1}]",0.15
> &nbsp;

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Gravitational-Wave Signal Detection and Characterization

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx781frsh43sbtpx18k4m0p8nh8bt9mn
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Easy
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> A gravitational-wave observatory records a noisy strain time series containing two very different kinds of loud events: real astrophysical signals (the chirp of two merging compact objects) and detector glitches (instrumental transients that are not astrophysical). A real analysis has to do three things at once: find the genuine signals, and — for each one — measure the physical properties of the source. This challenge asks for all three on 1-second strain segments.
> For every test segment you output three things: a detection score (how likely it holds a real signal), an estimate of the source's chirp mass, and an estimate of its mass ratio. Noise and glitches are the "background"; only the signal segments are real events.
> These three quantities are independent skills, which is the point of the challenge. Detecting that a chirp is present tells you nothing about which chirp it is: a strong detector recovers neither parameter for free (both come out at chance). And the two parameters are themselves independent — chirp mass sets the frequency sweep, mass ratio sets the asymmetry — so being good at one does not make you good at the other. The score is the average of the three, so you must genuinely master detection and characterization. A detection-only solution recovers neither parameter — both come out at chance — so it is capped near one third of the total score.
> All three are hard enough to require a trained deep model: the test signals used for detection are near the detection threshold (weak), glitches are adversarial, and estimating masses from a 1-second strain segment needs a learned representation of the chirp.
> Task
> For each test segment output three numbers: score (higher = more likely to contain a signal), mc (estimated chirp mass), and q (estimated mass ratio). You train on the provided segments, which are labelled background (0) or signal (1), and the signal rows carry their true chirp mass and mass ratio.
> Required approach. Your solution must train a deep-learning model on the provided data — for example a 1-D convolutional or transformer network, typically with a shared body and separate heads for detection and for the two parameters. A hand-crafted-feature model, an off-the-shelf unsupervised detector, or any approach that does not learn the chirp morphology does not reach the score a trained deep model does.
> Evaluation
> Submissions are scored with GWScore ∈ [0, 1], higher is better — the average of three independent sub-scores, each in [0, 1]:
> Detection efficiency. For a fixed false-alarm rate a, set the threshold at the score above which a fraction a of the background segments (noise and glitches) fall; the detection efficiency at that false-alarm rate is the fraction of weak true signals (near-threshold, SNR ≤ 9) scored above the threshold. This sub-score averages the detection efficiency at a = 0.005 and a = 0.02.
> Chirp-mass agreement. The rank agreement between your mc estimates and the true chirp masses over the true-signal segments, measured by Kendall's tau (1 = perfect ranking, 0 = random) clipped to [0, 1].
> Mass-ratio agreement. The same rank agreement for your q estimates against the true mass ratios.
> GWScore = (detection efficiency + chirp-mass agreement + mass-ratio agreement) / 3.
> You output mc and q for every test segment; only the true-signal segments are used for the two parameter sub-scores. Only the ranking of your parameter estimates matters (any monotonic units are fine), and only the ordering of your detection scores matters. A random or constant submission scores ≈ 0.01.
> Dataset
> The prepared public dataset:
> train_X.npy — training strain segments, a float32 array of shape (55000, 2048): 55,000 one-second segments at 2048 Hz.
> train_y.npy — training labels, int8 shape (55000,): 1 = signal, 0 = background (noise or glitch).
> train_mc.npy — float32 shape (55000,): the true chirp mass of each signal row (NaN for background rows).
> train_q.npy — float32 shape (55000,): the true mass ratio (in (0, 1]) of each signal row (NaN for background rows).
> test_X.npy — test strain segments, float32 shape (31000, 2048). Row i has id t00000+i (row 0 is t00000, up to t30999).
> sample_submission.csv — a valid submission in the required format.
> The strain is whitened; you may apply any further preprocessing. The training signals span a range of strengths so you can learn the chirp and its parameters; the detection sub-score is measured only on the weak (near-threshold) test signals.
> Submission
> Submit a CSV with exactly these four columns:
> id (string) — a test id matching a row of test_X.npy.
> score (float) — detection score (higher = more likely a signal).
> mc (float) — estimated chirp mass for that segment.
> q (float) — estimated mass ratio for that segment.
> Every test id must appear exactly once, and every value must be finite. Example:
> id,score,mc,q
> t00000,0.97,21.4,0.83
> t00001,0.02,18.9,0.55
> t00002,0.61,25.1,0.40
> Requirements
> Columns must be exactly id,score,mc,q.
> Every test id must appear exactly once.
> Every score, mc, and q must be a finite number (output an estimate for every segment, signal or not).
> Write the final submission to ./working/submission.csv. UTF-8.
> Baselines
> A constant or random submission scores ≈ 0.01.
> A detection-only solution recovers neither parameter — both come out at chance — so it is capped near 0.33 (one third of the total score).
> A reference multi-task 1-D CNN (shared body, three heads) scores ≈ 0.45.
> A strong all-round solver reaches ≈ 0.58 and above by pushing all three skills; there is wide headroom, especially on mass ratio (the hardest of the three).
> Allowed And Prohibited
> Allowed:
> Train deep neural networks (1-D CNNs, temporal convolutional nets, transformers, recurrent nets), including multi-task shared bodies or separate specialised models per sub-task.
> Any preprocessing of the strain (band-pass filtering, whitening, normalisation, resampling), data augmentation, and ensembling.
> Standard open-source deep-learning libraries (PyTorch, etc.).
> Prohibited:
> Do not use external datasets or any information beyond the provided files.
> Do not train on, adapt to, or fit statistics from the test segments — the labels are withheld.
> Do not hardcode outputs or use per-id answer tables.
> Do not use external LLM APIs or any model-generated labels in your submission.
> A trained deep-learning model is required — not a hand-crafted-feature model on its own, and not an off-the-shelf unsupervised detector used without training.
> Submissions
> 43

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Masked Z-Slab Tensor Continuity Prediction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7cgezky3dagjseejja0cpntx8b4qhr
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: medical
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Train a model from scratch to recover a compact summary of a hidden z-slab inside a 3D cellular microscopy tensor. Each row contains a stack of intensity slices from a tiny cell-volume crop. A contiguous six-slice slab has been replaced by a fill value in the public tensor; the row metadata tells you where the missing slab begins and ends.
> Your task is to predict a structured continuity record for the withheld slab. The target does not ask for a full reconstructed image or a single category. It asks for quantized mean and high-percentile intensity profiles, quadrant-level brightness cards, bright rim faces, high-texture cell cards, and three continuity labels comparing the hidden slab with its neighboring visible slices.
> Objective
> For every id, predict one hidden-slab continuity record:
> Output field	What it represents
> mean_profile	Six integer bins describing mean intensity for each hidden z slice.
> p90_profile	Six integer bins describing 90th-percentile intensity for each hidden z slice.
> quadrant_cards	Brightness cards for four quadrants on each hidden z slice.
> rim_faces	Boundary faces of the hidden slab that are brighter than the slab average.
> texture_cards	The eight highest-texture lattice cells in the hidden slab.
> continuity_signature	Entry, exit, and variance-change labels relative to neighboring visible slices.
> This is a masked tensor modeling task. A useful solution must learn local 3D continuity and intensity texture from the training examples, then infer the hidden slab summary from the visible context.
> Dataset
> Files:
> train.csv: labeled training rows.
> test.csv: rows to predict.
> sample_submission.csv: schema-valid example submission.
> measurement_tensor.npz: NumPy array file containing masked 3D measurement tensors under key windows.
> Columns in train.csv:
> id (string): row id.
> prompt (string): task instruction.
> packet_json (JSON string): tensor index, hidden-slab location, fill value, and context.
> answer_format_json (JSON string): allowed values and output limits.
> answer_json (JSON string): target hidden-slab continuity record.
> Columns in test.csv:
> id (string): row id.
> prompt (string): task instruction.
> packet_json (JSON string): tensor index, hidden-slab location, fill value, and context.
> answer_format_json (JSON string): allowed values and output limits.
> packet_json fields:
> array_file (string): measurement_tensor.npz.
> array_key (string): windows.
> array_index (integer): index into the tensor array.
> tensor_shape_zyx (array of three integers): [40, 40, 40].
> hidden_z_start (integer): first hidden slice index.
> hidden_z_stop_exclusive (integer): one past the final hidden slice index.
> xy_grid (object): four rows by four columns for cell summaries.
> context_family (string): broad acquisition-pattern family.
> fill_value (integer): intensity value used to replace the hidden slab.
> visible_intensity_summary (object): binned visible-context intensity summary.
> Target JSON
> Submit one object per row:
> mean_profile (array of six integers): each value is 0 through 9.
> p90_profile (array of six integers): each value is 0 through 9.
> quadrant_cards (array of objects): up to 24 cards. Each card has:
> z_offset (integer): 0 through 5 within the hidden slab.
> quadrant (string): upper_left, upper_right, lower_left, or lower_right.
> mean_bin (integer): 0 through 9.
> rim_faces (array of strings): any of y_min, y_max, x_min, x_max, z_entry, z_exit.
> texture_cards (array of objects): up to eight cards. Each card has:
> z_offset (integer): 0 through 5 within the hidden slab.
> xy_cell (string): one of r00_c00 through r03_c03.
> mean_bin (integer): 0 through 9.
> p90_bin (integer): 0 through 9.
> texture_bin (integer): 0 through 9.
> continuity_signature (object):
> entry_delta (string): sharp_down, down, flat, up, or sharp_up.
> exit_delta (string): sharp_down, down, flat, up, or sharp_up.
> variance_shift (string): lower, similar, or higher.
> Evaluation
> The score is the mean row score:
> 0.18 * mean_profile_score + 0.18 * p90_profile_score + 0.20 * quadrant_card_f1 + 0.08 * rim_face_f1 + 0.26 * texture_card_f1 + 0.10 * continuity_score
> mean_profile_score is the exact-match rate over the six mean_profile bins.
> p90_profile_score is the exact-match rate over the six p90_profile bins.
> quadrant_card_f1 is duplicate-aware F1 over complete (z_offset, quadrant, mean_bin) tuples.
> rim_face_f1 is set F1 over submitted and true rim-face labels. If both sets are empty, the score is 1; if only one is empty, it is 0.
> texture_card_f1 is duplicate-aware F1 over complete (z_offset, xy_cell, mean_bin, p90_bin, texture_bin) tuples.
> continuity_score is the exact-match rate over entry_delta, exit_delta, and variance_shift.
> For duplicate-aware F1, matches are the sum of minimum predicted and true tuple counts. Precision is matches divided by predicted tuple count, recall is matches divided by true tuple count, and F1 is 2 * precision * recall / (precision + recall). If both sides are empty the score is 1; if only one side is empty the score is 0.
> Malformed row JSON or invalid field values score 0 for that row. A submission with wrong columns, missing ids, duplicate ids, extra ids, or wrong row count is rejected.
> Learning Challenge
> The missing slab is not visible in the tensor, but the surrounding slices carry continuity cues. The strongest submissions should learn slice-to-slice texture evolution, local brightness persistence, rim effects, and small high-texture regions directly from the supplied training tensors.
> Submission
> Submit a CSV with exactly:
> id (string)
> answer_json (JSON string)
> Example:
> id,answer_json
> mt_1111111111111111,"{\"mean_profile\":[3,3,4,4,4,3],\"p90_profile\":[5,5,6,6,5,5],\"quadrant_cards\":[{\"z_offset\":0,\"quadrant\":\"upper_left\",\"mean_bin\":3}],\"rim_faces\":[\"x_max\"],\"texture_cards\":[{\"z_offset\":2,\"xy_cell\":\"r01_c03\",\"mean_bin\":4,\"p90_bin\":6,\"texture_bin\":3}],\"continuity_signature\":{\"entry_delta\":\"flat\",\"exit_delta\":\"down\",\"variance_shift\":\"similar\"}}"
> mt_2222222222222222,"{\"mean_profile\":[0,0,0,0,0,0],\"p90_profile\":[0,0,0,0,0,0],\"quadrant_cards\":[],\"rim_faces\":[],\"texture_cards\":[],\"continuity_signature\":{\"entry_delta\":\"flat\",\"exit_delta\":\"flat\",\"variance_shift\":\"similar\"}}"
> What Not To Use
> Do not use external datasets or source copies.
> Do not use GPU acceleration for training or inference.
> Do not use web lookup of held-out rows.
> Do not use hard-coded test ids or answer dictionaries.
> Do not use hosted inference or annotation services.
> Do not use pretrained biomedical-tensor, domain-specific, or foundation-model checkpoints.
> Do not manually annotate test rows.
> Submissions
> 21

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Impedance Spectra Battery Health Prognostics

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f01fr9ahwwcp6zdgnjnangs8b4v27
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: audio
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Each record is one complex Electrochemical Impedance Spectroscopy (EIS) sweep measured on a real lithium-ion cell: the cell's small-signal electrical response recorded at 60 frequencies, ordered from 20 kHz down to 0.02 Hz. Impedance is a complex quantity, so every record is two aligned length-60 sequences — the real part z_real and the imaginary part z_imag, in ohms — indexed by the same fixed frequency grid. As a cell wears out, the shape of this sequence evolves: the high-frequency series resistance drifts, the mid-frequency charge-transfer arc grows, and the low-frequency diffusion tail changes slope. That evolution is the signal you must read.
> From a single sweep you must emit a two-field diagnostic record that answers two genuinely independent questions about that measurement:
> **soh — how worn is this cell?** A continuous degradation score, reported as present discharge capacity divided by the cell's fresh capacity. Only its ordering is scored, so any monotone rescaling of a correct ordering scores identically.
> **condition — under what operating condition was this sweep taken?** One of six opaque codes (cond_a … cond_f) identifying the electrical state the cell was held in during the measurement.
> The two fields are independent by measurement, not by assumption. Across the released data the rank correlation between the condition code and the degradation score is ≈ 0.01: every operating condition occurs across the full health range, and every health level occurs under every condition. Neither field can be derived from the other, and no ordering copied from one will score on the other — the score is only reachable by answering both questions separately.
> That independence is the point of the task. Both effects are written into the same 60-point curve at once: wear and operating condition each deform the spectrum, and they overlap in the frequency bands where they act. Reading both from one sweep means disentangling the part of the spectral shape that tracks irreversible wear from the part that tracks the reversible measurement condition — which is the actual difficulty of interpreting impedance in the field, where the operating condition at measurement time is rarely known.
> Two properties define the difficulty. (1) Held-out operating cohort. The evaluation sweeps come from cells run under an operating cohort that is absent from the training pool, and whose impedance response, initial capacity, and per-cycle fade kinetics all differ. A model that memorises the training cells' absolute impedance-to-capacity mapping transfers poorly; characterising the train→evaluation difference from the data is part of the task. (2) Entangled operating condition. The operating condition deforms the same curve that wear does, and the absolute impedance level also carries per-cell calibration spread. Raw impedance magnitude therefore does not cleanly indicate health: a healthy cell under one condition can present a larger magnitude than a worn cell under another. The degradation reading must come from a representation that separates the two effects rather than one that reads overall level.
> Data files
> Exactly three files are released, all inside <public_dir>:
> **train.parquet** — parquet, 5,876 rows. The training sweeps. Contains sample_id, group_id, z_real, z_imag, and both target columns soh and condition.
> **test.parquet** — parquet, 1,818 rows. The evaluation sweeps, drawn from the held-out operating cohort. Contains sample_id, z_real, z_imag only. Both target columns soh and condition are absent from this file, and so is group_id.
> **sample_submission.csv** — csv, 1,818 rows. A formatting template only: the correct three columns in the correct order, filled with placeholder constants. Its values are not predictions and carry no information.
> Every column of the released data, with its type and meaning:
> **sample_id** — string. Opaque unique identifier of one impedance sweep, and the join key for your submission (e.g. sp_00093350cd5a7d9b). Present in train.parquet, test.parquet and the submission. Carries no information about the targets and no row-order signal.
> **group_id** — string. Opaque identifier of the physical cell a sweep came from (e.g. cell_4484b6dd); 8 distinct cells, 420–972 sweeps each. Present in **train.parquet only**. Use it to hold out whole cells during cross-validation.
> **z_real** — listfloat, length 60. Real part of the complex impedance in ohms, ordered along the frequency grid below (20 kHz → 0.02 Hz). Range ≈ 0.23 … 33.08. Present in train.parquet and test.parquet.
> **z_imag** — listfloat, length 60. Imaginary part of the complex impedance in ohms, on the same frequency grid and in the same order. Range ≈ −29.04 … 0.73; negative values are capacitive. Present in train.parquet and test.parquet.
> **soh** — float, target. Degradation score: present discharge capacity divided by the cell's fresh capacity. Range 0.0007 … 1.0000 (≈ 1.0 fresh, 0.8 at end-of-life, lower once past it). Present in **train.parquet only**; you predict it for test.parquet. Only its ordering is scored.
> **condition** — string, target. The operating-condition code the sweep was recorded under: exactly one of cond_a, cond_b, cond_c, cond_d, cond_e, cond_f. The six codes are opaque and carry no ordering — they are labels, not a scale — and they are near-evenly represented (1,259–1,329 sweeps each across the pool). Present in **train.parquet only**; you predict it for test.parquet.
> The same information as a table:
> The frequency grid (Hz) — identical for every row and both channels, descending:
> 20004.5, 15829.1, 12516.7, 9909.44, 7835.48, 6217.25, 4905.29, 3881.27, 3070.98, 2430.78,
> 1923.15, 1522.44, 1203.84, 952.866, 754.276, 596.719, 471.963, 373.209, 295.473, 233.877,
> 185.059, 146.358, 115.778, 91.6721, 72.517, 57.3682, 45.3629, 35.9313, 28.4091, 22.482,
> 17.7961, 14.0681, 11.1448, 8.81772, 6.97545, 5.5173, 4.36941, 3.45686, 2.73547, 2.16054,
> 1.70952, 1.35352, 1.07079, 0.84734, 0.67072, 0.53067, 0.41976, 0.33183, 0.26261, 0.20791,
> 0.16452, 0.13007, 0.10309, 0.08153, 0.06443, 0.05102, 0.04042, 0.03192, 0.02528, 0.01999
> Loading example:
> import numpy as np, pandas as pd
> df = pd.read_parquet(f"{public_dir}/train.parquet")
> Zr = np.stack(df["z_real"].to_numpy())     # (5876, 60) real part
> Zi = np.stack(df["z_imag"].to_numpy())     # (5876, 60) imaginary part
> X  = np.stack([Zr, Zi], axis=1)            # (5876, 2, 60) two-channel frequency sequence
> Submission Format
> Write a CSV to <submission_out> with exactly these three columns, in this order:
> **sample_id** — string. The sweep identifier, copied from test.parquet. One row per evaluation sweep.
> **soh** — float. Your degradation score for that sweep. Only its ordering across rows is scored, so it need not lie on the true capacity-fraction scale; any monotone rescaling of a correct ordering scores identically.
> **condition** — string. The operating-condition code you believe the sweep was recorded under. Must be exactly one of cond_a, cond_b, cond_c, cond_d, cond_e, cond_f.
> Example of a correctly formatted file (first rows shown):
> sample_id,soh,condition
> sp_00093350cd5a7d9b,0.94,cond_c
> sp_0012e1d1e5e9f86b,0.87,cond_a
> sp_00415586dd5b7103,0.81,cond_f
> Requirements:
> Exactly 1,818 rows plus a header row exactly sample_id,soh,condition.
> One row per evaluation sweep; sample_id values must match the evaluation index.
> soh must be finite, numeric and non-null. condition must be one of the six codes above — any other string is treated as a wrong answer for that row, never as an error.
> A missing target column, wrong row count, misaligned identifiers, or majority-missing values makes the submission invalid and it scores the floor.
> Evaluation Metric
> The two fields answer independent questions, so each is scored on its own terms and the two are averaged with equal weight:
> score = 0.5 * max(0, Spearman(soh_pred, soh_true))  +  0.5 * macroF1(condition_pred, condition_true)
> The degradation field is scored by Spearman rank correlation because the evaluation cells belong to an unseen operating cohort whose absolute scale cannot be inferred from training data; ordering is the capability that genuinely transfers, and the component is invariant to any monotone rescaling of your output. The condition field is scored by macro-F1 over the six codes — unweighted across codes, so a rare code counts as much as a common one and predicting one code everywhere cannot buy a good score.
> import numpy as np, pandas as pd
> COND_CODES = ["cond_a", "cond_b", "cond_c", "cond_d", "cond_e", "cond_f"]
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> sub = submission.set_index("sample_id"); ans = answers.set_index("sample_id")
> if any(c not in sub.columns for c in ["soh", "condition"]):  return 0.0
> if len(sub) != len(ans):                                     return 0.0
> sub = sub[~sub.index.duplicated(keep="first")]
> if len(sub.index.intersection(ans.index)) < 0.8 * len(ans):  return 0.0
> # --- component 1: degradation ORDERING (Spearman, floored at 0) ---
> pred = pd.to_numeric(sub["soh"], errors="coerce").reindex(ans.index)
> if pred.isna().mean() > 0.5:                                 return 0.0
> pred = pred.replace([np.inf, -np.inf], np.nan).fillna(pred.median())
> pr, tr = pred.rank(), ans["soh"].rank()
> r = 0.0 if pr.std() == 0 or tr.std() == 0 else float(np.corrcoef(pr, tr)[0, 1])
> s_soh = max(0.0, r)
> # --- component 2: operating-condition identification (macro-F1) ---
> pc = sub["condition"].reindex(ans.index)
> if pc.isna().mean() > 0.5:                                   return 0.0
> pc = pc.where(pc.isin(COND_CODES), "__invalid__").to_numpy()
> tc = ans["condition"].to_numpy()
> f1s = []
> for c in COND_CODES:
> tp = float(((pc == c) & (tc == c)).sum())
> fp = float(((pc == c) & (tc != c)).sum())
> fn = float(((pc != c) & (tc == c)).sum())
> denom = 2 * tp + fp + fn
> f1s.append(0.0 if denom == 0 else 2 * tp / denom)        # zero-denominator mask
> s_cond = float(np.mean(f1s))
> return float(min(1.0, max(0.0, 0.5 * s_soh + 0.5 * s_cond)))
> Higher is better. Score range: floor 0.0, cap 1.0.
> What degenerate submissions score, exactly:
> A **constant soh** has no rank variance, so the first component is 0.0. A randomly ordered or inverted one is also floored to 0.0.
> A **single constant condition** over six near-balanced codes yields macro-F1 ≈ 0.048, so the second component is ≈ 0.048.
> sample_submission.csv is both of those at once and scores ≈ **0.024** — near the floor, and it returns a number rather than raising.
> Neither field can carry the other. Perfect knowledge of the degradation ordering with no condition ability caps at ≈ 0.52; perfect condition identification with no ordering ability caps at 0.50. Only answering both reaches 1.0.
> Any structurally invalid submission returns 0.0 rather than an error.
> Intended Solution Class & CPU Modeling Guardrails
> The intended approach is deep sequence learning over the raw two-channel frequency sweep, trained from scratch natively on CPU:
> Encode the (2, 60) frequency sequence with a 1-D convolutional or attention encoder over the frequency axis, pool it, and emit both fields from a shared trunk with two heads — one continuous ordering score, one over the six condition codes. Because absolute calibration cannot transfer to the unseen cohort, shape the representation and your validation around ordering degradation rather than reproducing an in-domain impedance-to-capacity table.
> The two heads need different information from the same curve. A representation that collapses the sweep to overall level will read one field at the cost of the other; the encoder has to keep the frequency-resolved structure that separates reversible condition effects from irreversible wear. Sharing a trunk between the two heads is a reasonable way to force that separation, but neither field's answer can be read off the other's.
> Validate for the held-out cohort. Random k-fold validation that mixes a cell's sweeps across folds will badly overstate your score. Hold out whole cells using group_id, and expect the true evaluation gap to be larger still.
> Hard gates:
> CPU deep learning is required and sufficient. The data is small-N (5,876 training sweeps, ≈ 6 MB) and sized so a 1-D CNN with two heads trains end-to-end on 10 cores in minutes — the reference implementation finishes in about 4 minutes. Budget accordingly (torch.set_num_threads, modest widths, length-60 inputs).
> Anti-heuristic / anti-tabular gate. Reducing each sweep to a handful of summary numbers (series resistance, arc height, a fixed low-frequency magnitude) and fitting a shallow model to that table — the classical equivalent-circuit-feature approach — is the performance floor, not a solution, and is banned as the primary representation, as are hand-tuned equivalent-circuit fits and hardcoded thresholds. Your primary representation must be learned from the raw sequence.
> No transductive learning. Do not pseudo-label, fit, or train on the unlabelled evaluation sweeps. test.parquet is evaluation-only; the held-out cohort must remain unseen at training time.
> Environment & Runtime Constraints
> Your code runs in an automated, isolated, offline pipeline:
> Hardware: 10 CPU cores, 62 GB RAM, no GPU.
> Time limit: the entire train + validate + inference loop must finish in under 1.5 hours.
> No internet: pip install, wget, torch.hub.load, and external API calls fail immediately.
> Preinstalled libraries only: the Kaggle Docker image (numpy, pandas, scipy, scikit-learn, torch, transformers, timm, …).
> Pretrained weights: permitted only if they load natively through preinstalled packages via a public model ID; trust_remote_code=True and torch.hub.load() are disabled. None are needed — training from scratch on the sweeps is intended.
> Data: all challenge data is provided under <public_dir>; read only from there. Do not call datasets.load_dataset(...), reach the Hugging Face Hub, or touch any external source at runtime.
> The I/O Command Line Contract
> Your script (solution.py) must parse paths from the command line — no hardcoded directories:
> python3 solution.py <public_dir> <submission_out>
> sys.argv[1] (public_dir): directory containing train.parquet, test.parquet, sample_submission.csv.
> sys.argv[2] (submission_out): absolute path where your script must write the final prediction CSV. Create any missing parent directories before writing.
> Notes for solvers
> The task rewards a learned separation of wear from operating condition in the spectral shape. Cheap summary features are weak here on purpose: reducing the sweep to a few scalars discards exactly the frequency-resolved structure that distinguishes the two effects, and because the evaluation cells form an unseen operating cohort, an in-domain calibration does not carry over.
> Build validation that mirrors the real generalization: hold out whole cells via group_id, and treat any in-domain score as an optimistic upper bound on your evaluation score.
> Budget your effort across both fields. They are scored with equal weight and are uncorrelated, so the marginal return on a field you have neglected is usually larger than further tuning the one you have already fitted. There is no shortcut that converts skill on one into score on the other.
> What Not To Use
> Do not use sample_id, row or file order, or file position as features — identifiers are opaque and the order is randomized.
> Do not attempt to look up, match, or reconstruct the original measurements from any external database, publication, or pretrained artifact; identifiers are removed and the released values carry anonymization perturbations.
> Do not compute statistics from, fit to, or pseudo-label the evaluation set (test.parquet).
> Do not infer targets from sample_submission.csv — it is a formatting example whose values are placeholders.
> Do not reduce the sweep to a hand-crafted summary-statistic table, a fixed equivalent-circuit fit, or hardcoded thresholds as the primary representation.
> Do not attempt to derive one submission field from the other — they are uncorrelated by measurement (|rank correlation| ≈ 0.01), so copying, rescaling, or bucketing one into the other scores no better than guessing on that field.
> Do not call hosted or closed-model APIs at inference time; the container is offline.
> Submissions
> 11

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## From Scratch Medical Cardiac Signal Modeling

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7164g1n7reth0zx4wb72vtss8bva23
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: medical
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> This is a from scratch medical signal-modeling challenge. Participants train a compact model from scratch on the public labeled rows, then apply that model to each test row. The model receives observed cardiovascular channels from one eight-second interval and must submit two artifacts for the same interval: a 2000-sample target-sensor waveform and a cardiac event ledger.
> The source corpus is an open cardiovascular signal database with 338 thirty-second synchronized recordings from 32 healthy volunteers. During acquisition, an electrocardiograph, phonocardiograph, photoplethysmograph, and chest accelerometer were recorded at the same time. Challenge preparation creates one deidentified eight-second public example per source recording, so the 258 training rows plus 80 test rows correspond to the 338 source recordings.
> Each public row contains an observed_npz file with the sensors available for that interval. One modality named in target_modality is withheld from the inputs, such as acc_chest, ppg_carotid_660, ppg_brachial_800, ecg_v3, ecg_v4, or pcg_apex. The submitted waveform must describe that target modality on the row-local 250 Hz timestamp grid.
> The public rows use opaque IDs and local paths only. Original subject IDs, recording filenames, recording times, demographic rows, source paths, exact crop starts, and source row order are not participant inputs. Public arrays are normalized, transformed, and resampled during preparation, so the intended route is to train from scratch on cross-sensor cardiac structure in the provided training data rather than matching files back to the upstream corpus.
> This is not scalar regression, health classification, heart-rate estimation, ordinary table prediction, raw observed-channel copying, or source-corpus retrieval. The score couples a from scratch medical waveform model with a cardiac event ledger: a plausible-looking trace without aligned events loses score, and a ledger without local waveform impulses loses score.
> The official solver tier is CPU. Every valid solution must run on CPU only within 1.5 hours on 10 CPU cores and 62 GB RAM. All preprocessing, from scratch model training, inference, and submission writing must finish inside that single run.
> From Scratch Training Regime
> The required learning route is from scratch. Model parameters must be initialized inside the submitted run and learned only from the public challenge files. Deterministic signal-processing steps are allowed, but the central waveform and ledger estimates should come from a model trained from scratch on the provided train rows.
> Appropriate from scratch approaches include compact 1D convolutional models, small randomly initialized multimodal signal encoders, tree ensembles over train-derived signal features, kernel or basis-expansion waveform heads, train-fold event detectors, target-modality embeddings learned from train rows, and calibrated post-processing learned from public validation folds.
> Do not rely on external model weights, hosted inference, source archive lookup, subject reconstruction, raw filenames, row order, or manual answer maps. A solution that mostly uses metadata, interpolation, nearest-neighbor copying, observed-channel copying, or static target templates is outside the intended from scratch modeling route even if it produces a syntactically valid submission.
> Task
> For every test id, use the row's public observed-sensor payload and requested target_modality to estimate one withheld physiological waveform. The waveform must be submitted as a compressed .npz, base64-encoded in pred_signal_b64.
> The returned waveform payload is a row-aligned float32 array with shape [2000,1], aligned to timestamps from 0.000 to 7.996 seconds at 250 Hz. A submission may also include an optional valid_mask inside the .npz.
> Each row must also include event_ledger_json, a compact JSON ledger of cardiac events supported by the submitted waveform and observed context. Allowed event types are r_peak, pulse_arrival, pcg_impulse, chest_impulse, and target_qrs.
> Successful from scratch solutions should model both waveform morphology and cardiac timing. A solution that returns only a static average waveform, only copies an observed channel, or only exploits duration and target priors will miss important scored structure.
> Intended Approach
> Strong solutions should train from scratch. The best approaches should use ECG, PCG, PPG, and ACC evidence jointly, not metadata or lookup shortcuts.
> Useful routes include band-limited filtering, robust peak proposals, pulse-arrival alignment, target-modality embeddings, temporal smoothing, DTW-style alignment features, compact 1D convolutional models trained from scratch, small multimodal signal encoders trained from scratch, learned cardiac sensor models, gradient boosting over sensor features, and calibrated post-processing that respects continuity and event consistency.
> Validation should be built from the public training set using grouped or clustered folds so that row order, IDs, and file paths cannot become answer channels. The private split holds out complete subject families, so source-like memorization and nearest-neighbor shortcuts are intentionally weak.
> Local difficulty checks show substantial headroom. The sample baseline scores about 0.312689, metadata-only scores about 0.172679, observed-sensor linear interpolation scores about 0.219008, nearest-neighbor waveform matching scores about 0.208464, PCG-only beat templates score about 0.195068, ECG-only event copying scores about 0.220155, and a perfect oracle scores exactly 1.0.
> What Not To Do
> Using any of the approaches below is grounds for rejection on review, regardless of leaderboard score.
> Do not use the internet, external datasets, source-archive lookup, recovered subject IDs, recovered recording names, raw timestamps, demographic rows, source paths, or external answer services while solving.
> Do not use row order, IDs, payload paths, file sizes, byte hashes, archive metadata, private files, grader internals, malformed-input behavior, hard-coded answer maps, manual test labels, or hosted APIs as answer channels.
> Do not silently disable the from scratch model and fall back to a metadata, interpolation, nearest-neighbor, observed-channel-copy, or lookup shortcut when inference fails.
> Do not reduce the task to scalar heart-rate estimation, ordinary health classification, target-channel mean regression, static-average prediction, or raw observed-sensor copying.
> Do not use unauthorized compute outside the selected CPU tier, hosted inference APIs, remote services, external model checkpoints, or runtime-downloaded weights.
> Do not read private files, exploit the grader, or submit malformed base64 or JSON as a format attack.
> Use only the provided public challenge data and from scratch learned or signal-processing models trained from that data.
> Evaluation
> Higher is better. The score is a transparent from scratch medical signal-modeling metric.
> Waveform agreement is computed on the submitted values[:,0] and the private target. Correlations use the best lag within 10 samples, which is 0.04 seconds at 250 Hz. RMSE is computed after clipping both arrays to [-8,8].
> waveform_score =
> 0.55 * best_shifted_waveform_correlation
> + 0.25 * best_shifted_derivative_correlation
> + 0.20 * exp(-RMSE / 1.15)
> Events are matched greedily within each event type. Matching tolerance is 0.08 seconds for r_peak and target_qrs, and 0.12 seconds for pulse_arrival, pcg_impulse, and chest_impulse. For each event type with at least one submitted or private event, precision is matches / max(1, submitted_count), recall is matches / max(1, private_count), and event_F1 is the usual harmonic mean. matched_timing_quality is the mean of max(0, 1 - timing_error / tolerance) over matched pairs, or 0 when there are no matches.
> event_score =
> mean over nonempty event types of
> 0.72 * event_F1
> + 0.28 * matched_timing_quality
> Continuity checks that the submitted waveform is covered, smooth enough, and not collapsed to a constant value.
> coverage =
> mean(valid_mask) if valid_mask is present, otherwise 1.0
> smoothness =
> exp(-max(0, percentile(abs(diff(values[:,0])), 95) - 1.2) / 2.0)
> variance_quality =
> min(1.0, std(values[:,0]) / 0.35)
> continuity_score =
> clip(0.45 * coverage
> + 0.35 * smoothness
> + 0.20 * variance_quality, 0, 1)
> Consistency checks whether submitted target-side events have local impulses in the submitted waveform. Relevant ledger types are pulse_arrival, pcg_impulse, chest_impulse, and target_qrs. If none of those event types are submitted, consistency_score is 0.35. Otherwise, for the first 48 relevant events, the grader converts each event time to round(t * 250), opens a +-8 sample window, and compares the maximum local absolute gradient with the 80th percentile absolute gradient of the whole submitted waveform.
> consistency_score =
> impulse_aligned_event_count / max(1, min(relevant_event_count, 48))
> The row and final scores are:
> core =
> 0.60 * waveform_score
> + 0.25 * event_score
> + 0.10 * continuity_score
> + 0.05 * consistency_score
> row_score =
> core  *(1 - 0.06*  abs(confidence - core))
> final_score =
> 0.76 * mean(row_score)
> + 0.10 * lowest target-modality mean
> + 0.08 * lowest event-density mean
> + 0.06 * lowest target-family mean
> The row confidence value should be the participant's estimate of that row's core quality after considering waveform shape, event timing, continuity, and ledger-waveform consistency. It is not a separate clinical label. Estimate it from public validation folds: use higher values for rows where the from scratch model has stable waveform and event agreement, and lower values for noisy or ambiguous rows. The confidence term is a small transparent calibration factor; it cannot turn a weak waveform or invalid ledger into a high-scoring row.
> The final robustness terms are worst-group means over three medically meaningful groupings. target_modality groups use the public target_modality values. target_family groups are derived from the public target prefix: ECG targets, PPG targets, PCG targets, and ACC targets. event_density groups are sparse, medium, or dense cardiac-event rows; in public train folds, solvers can reproduce the same grouping from event_ledger_json using event counts <=14, 15 to 24, and >24. Test group labels are not extra required outputs, but these terms are optimizable by training and validating from scratch models that perform consistently across target modalities, sensor families, and low-to-high event-density rows instead of overfitting only the global average.
> All terms lie in [0,1]; the theoretical minimum is 0.0, the theoretical maximum is 1.0, and a perfect valid submission scores exactly 1.0. There is no score cap, arbitrary power, or hidden suppression curve.
> Submission-level structure is strict. Missing, extra, or reordered columns; duplicate IDs; missing or foreign IDs; unreadable private answers; non-finite confidence; confidence outside [0,1]; and unsafe global schema mismatches raise an invalid-submission error. In an otherwise structurally valid submission, row-local malformed base64, invalid .npz payloads, missing values, non-finite arrays, wrong shapes, invalid masks, malformed event JSON, invalid event types, negative times, impossible timestamps, or overlong strings receive 0 for that row or head without crashing the grader. Grader errors do not reveal private labels, groups, split logic, or answer content.
> Dataset
> Prepared files are under public/. Paths in train.csv and test.csv are relative to public/. The prepared public data contain 338 short physiological examples: 258 labeled training rows and 80 test rows.
> The public data does not expose original subject IDs, recording filenames, recording times, demographic rows, source paths, exact crop starts, or source row order.
> All signal values are dimensionless float32 normalized sensor units after challenge preparation. They are not raw millivolts, acceleration units, acoustic pressure units, optical counts, or physical clinical units. Timestamps are row-local seconds.
> File overview
> | Item | Description |
> |---|---|
> | public/train.csv | 258 train rows |
> | public/test.csv | 80 test rows |
> | public/sample_submission.csv | weak template |
> | public/signal_schema.json | NPZ schema |
> | public/train/signals/*.npz | train arrays |
> | public/test/signals/*.npz | test arrays |
> Input NPZ contents
> Each row's observed_npz points to a compressed .npz containing:
> | Key | Shape | Meaning |
> |---|---|---|
> | values | [2000,n] | observed matrix |
> | timestamps | [2000] | seconds at 250 Hz |
> | channels | [n] | column names |
> The channels array names the sensor represented by each column in values. Public rows may expose any available subset except the requested target modality.
> | Family | Channels | Meaning |
> |---|---|---|
> | ECG | four leads | electrical trace |
> | PCG | apex sound | heart sound |
> | Carotid PPG | two wavelengths | neck pulse |
> | Brachial PPG | two wavelengths | arm pulse |
> | Chest ACC | chest axis | body motion |
> ECG channel names are ecg_i, ecg_ii, ecg_v3, and ecg_v4; they contain normalized cardiac electrical traces with QRS-like spikes and lower-amplitude morphology. PCG is pcg_apex; it contains normalized heart-sound impulses around mechanical cardiac events. Carotid PPG channels are ppg_carotid_660 and ppg_carotid_800; they contain normalized optical pulse traces with pulse upstroke and decay. Brachial PPG channels are ppg_brachial_660 and ppg_brachial_800; they are similar optical pulse traces, usually delayed from ECG activity. Chest ACC is acc_chest; it contains normalized chest accelerometer motion with body-motion and cardiac impulse content.
> train.csv columns
> | Column | Type | Description |
> |---|---|---|
> | id | string | opaque row id |
> | observed_npz | string | observed NPZ path |
> | target_modality | string | requested modality |
> | observed_modalities_json | string | observed channels |
> | duration_sec | float | always 8.0 |
> | sample_rate_hz | float | always 250.0 |
> | n_observed_channels | integer | channel count |
> | target_signal_b64 | string | train target NPZ |
> | event_ledger_json | string | train event ledger |
> test.csv columns
> | Column | Type | Description |
> |---|---|---|
> | id | string | opaque row id |
> | observed_npz | string | observed NPZ path |
> | target_modality | string | requested modality |
> | observed_modalities_json | string | observed channels |
> | duration_sec | float | always 8.0 |
> | sample_rate_hz | float | always 250.0 |
> | n_observed_channels | integer | channel count |
> Test rows omit target_signal_b64 and event_ledger_json.
> Submission format
> Submit ./working/submission.csv with exactly 80 rows and exactly these columns in exactly this order.
> | Column | Type | Constraint |
> |---|---|---|
> | id | string | exact test ID set |
> | pred_signal_b64 | string | base64 NPZ payload |
> | event_ledger_json | string | JSON event ledger |
> | confidence | float | row core estimate |
> Each pred_signal_b64 value must decode to a compressed .npz with:
> | NPZ key | Required? | Shape | Meaning |
> |---|---|---|---|
> | values | yes | [2000,1] | submitted waveform |
> | timestamps | yes | [2000] | row-local seconds |
> | valid_mask | no | [2000,1] | valid-sample mask |
> Values must be finite float32 values within the normalized sensor range [-12,12]. Timestamps must be float32 and must match the row-local 250 Hz grid from 0.000 to 7.996 seconds. valid_mask, when present, must be a uint8 array.
> event_ledger_json may be either a list of event objects or an object with an events list. Each event object has type, t, and confidence.
> Example:
> id,pred_signal_b64,event_ledger_json,confidence
> sst_0123456789abcdef01,UEsDBBQAAAAI...,"{""events"":[{""type"":""r_peak"",""t"":0.744,""confidence"":0.81}]}",0.44
> sst_fedcba9876543210ff,UEsDBBQAAAAI...,"{""events"":[{""type"":""pulse_arrival"",""t"":0.912,""confidence"":0.76}]}",0.39
> Submissions
> 0

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## CAP-Chain Sleep Microstructure Event Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx712rpyf7nca7hwc23sq7dfss8bgq3w
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: medical
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> You are given de-identified 5-minute NREM EEG episodes. Each episode contains two or three standardized EEG channels sampled at 64 Hz. Your task is to reconstruct the medical event map inside the episode: phase-A events, the A1/A2/A3 subtype for each phase-A event, the intervening phase-B intervals, and the boundaries of each complete CAP chain.
> In plain terms, you are turning a short multichannel EEG segment into a timed table of EEG microstructure events. A phase-A event is an activation event with subtype A1, A2, or A3. A phase-B event is the interval between two neighboring phase-A events in the same valid chain. A valid chain starts with A, ends with A, alternates A/B/A/B/A or longer, and contains at least three A events and two B events.
> The public metadata gives only the opaque episode identifier, tensor row index, sampling rate, sample count, channel count, and anonymous channel-role names. It does not contain subject identifiers, recording names, original filenames, clinical labels, absolute timestamps, annotation row numbers, source row order, or original channel labels.
> The reference labels come from expert sleep microstructure annotations. The phase-A labels are expert A1, A2, and A3 events. Phase-B labels are derived only when two consecutive expert A events belong to the same valid chain and the intervening B interval is less than 60 seconds. Chain boundaries are derived from the first and last A event in each valid chain. Episodes with a chain crossing the visible episode boundary are not used for scoring.
> There is no released inter-rater uncertainty label. The submission schema therefore asks for calibrated confidence values, not invented ambiguity classes. Confidence is rewarded when high-confidence events and chains match the reference and low-confidence objects are wrong or unmatched.
> This is a signal-annotation research benchmark, not a diagnostic tool. Do not infer, predict, or report diagnosis, subject identity, treatment status, or any other clinical status.
> Task
> For every test episode, submit:
> A chronological event list containing A1, A2, A3, and B events.
> A discrete onset bin and duration bin for every event. Bins are 2 seconds wide.
> Chain IDs linking events that belong to the same CAP chain.
> A chain-boundary list with start and end bins for each submitted chain.
> A confidence value from 0 to 1 for every event and chain.
> This is not sleep-stage classification, binary event detection, scalar regression, or a fixed-template parsing task. Strong submissions must learn signal evidence and also produce CAP-chain objects that satisfy the required alternation and boundary rules.
> Intended Approach
> Strong solutions should train compact models from scratch on the provided public training and validation episodes. For this challenge, the intended model-learning route is an EEG or physiological-signal encoder with structured temporal heads that recover the coupled event, subtype, duration, and chain-boundary object.
> The challenge is configured for CPU-only solving. Practical methods include learned EEG encoders, compact temporal convolutional networks, multi-output temporal heads, HMM/CRF-style chain assignment, dynamic-programming chain repair, and spectral or wavelet features feeding learned models. Solvers must train and infer with CPU computation within the platform runtime budget. Solutions should learn from the public training and validation episodes rather than using row order, external corpus lookup, or recovered annotation files.
> What Not To Do
> Do not use external corpus lookup, EEG-window fingerprinting, recovered original filenames, original timestamps, original record IDs, source row order, annotation files, clinical labels, private files, hardcoded answers, manual test labeling, or grader exploitation. Do not reduce the task to scalar regression, ordinary sleep-stage prediction, tabular metadata classification, a fixed timing template, or a rule-only parser that ignores the EEG signal.
> Enforcement On Invalid Approaches
> Submissions or solution writeups that obtain labels through public-corpus matching, private-file access, metadata reconstruction, hardcoded IDs, manual labeling, hosted or external inference, or rule-only shortcuts may be rejected even if the CSV is structurally valid. The intended evidence is learned medical EEG microstructure modeling from scratch.
> Dataset
> The public dataset contains train, validation, and test manifests; train and validation labels; NumPy signal tensors; metadata; and a sample submission. Paths in manifests are relative to the public root.
> Public Files
> train.csv Columns
> The training input table is train/manifest.csv.
> Training labels are in train/labels.csv.
> test.csv Columns
> The test input table is test/manifest.csv.
> The test manifest has no event labels, chain labels, original recording identifiers, original filenames, absolute times, annotation IDs, clinical labels, or original channel names.
> Submission Format
> Submit one CSV row for every test episode_id, using these columns in this exact order.
> events_json must be valid JSON for a list with at most 80 objects. Each object must have exactly:
> onset_bin and duration_bin use 2-second bins. Event bin k begins at 2*k seconds from the episode start. Each event covers the half-open interval [onset_bin, onset_bin + duration_bin), so the event end is exclusive.
> chains_json must be valid JSON for a list with at most 12 objects. Each object must have exactly:
> Each event must reference one submitted chain. A submitted chain covers the half-open interval [start_bin, end_bin), so end_bin is exclusive. For a well-aligned chain, end_bin should equal the final A event's onset_bin + duration_bin. Within each chain, a valid CAP pattern alternates A/B/A/B/A or longer, starts and ends with A, has at least three A events and two B events, and keeps the chain boundary around the first and last A event.
> Sample submission preview
> These are the literal header and first five rows of the generated sample_submission.csv. The complete file contains one row for every test episode and uses the same three-column order.
> episode_id,events_json,chains_json
> ep_00530e26eb21317431f1,"[{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":2,""event_type"":""A1"",""onset_bin"":38},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":8,""event_type"":""B"",""onset_bin"":40},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":4,""event_type"":""A2"",""onset_bin"":48},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":18,""event_type"":""B"",""onset_bin"":52},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":2,""event_type"":""A1"",""onset_bin"":70}]","[{""chain_id"":""c0"",""confidence"":0.35,""end_bin"":72,""start_bin"":38}]"
> ep_02f0fb8c92c24e4e11ab,"[{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":2,""event_type"":""A1"",""onset_bin"":38},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":8,""event_type"":""B"",""onset_bin"":40},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":4,""event_type"":""A2"",""onset_bin"":48},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":18,""event_type"":""B"",""onset_bin"":52},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":2,""event_type"":""A1"",""onset_bin"":70}]","[{""chain_id"":""c0"",""confidence"":0.35,""end_bin"":72,""start_bin"":38}]"
> ep_03702c22e5edb4b86166,"[{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":2,""event_type"":""A1"",""onset_bin"":38},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":8,""event_type"":""B"",""onset_bin"":40},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":4,""event_type"":""A2"",""onset_bin"":48},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":18,""event_type"":""B"",""onset_bin"":52},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":2,""event_type"":""A1"",""onset_bin"":70}]","[{""chain_id"":""c0"",""confidence"":0.35,""end_bin"":72,""start_bin"":38}]"
> ep_0393d841a8d630f59c9d,"[{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":2,""event_type"":""A1"",""onset_bin"":38},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":8,""event_type"":""B"",""onset_bin"":40},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":4,""event_type"":""A2"",""onset_bin"":48},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":18,""event_type"":""B"",""onset_bin"":52},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":2,""event_type"":""A1"",""onset_bin"":70}]","[{""chain_id"":""c0"",""confidence"":0.35,""end_bin"":72,""start_bin"":38}]"
> ep_04b30f6a0d070ea59417,"[{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":2,""event_type"":""A1"",""onset_bin"":38},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":8,""event_type"":""B"",""onset_bin"":40},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":4,""event_type"":""A2"",""onset_bin"":48},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":18,""event_type"":""B"",""onset_bin"":52},{""chain_id"":""c0"",""confidence"":0.35,""duration_bin"":2,""event_type"":""A1"",""onset_bin"":70}]","[{""chain_id"":""c0"",""confidence"":0.35,""end_bin"":72,""start_bin"":38}]"
> ## Evaluation
> The official metric is `CAPChainScore`, a transparent 0-to-1 medical event-and-chain score. Higher is better. A perfect valid submission scores exactly `1.0`; a structurally invalid submission is rejected; a row-local malformed JSON or impossible event schema scores `0.0` for that row.
> All matching is done separately for each episode.
> ### Temporal Event Score
> Submitted and reference events are matched one-to-one. A submitted event can match a reference event only when the phase family agrees: A events match A events, and B events match B events. For an eligible pair:
> onset_gap = abs(pred.onset_bin - ref.onset_bin)
> duration_gap = abs(pred.duration_bin - ref.duration_bin)
> The pair is accepted only when both gaps are at most 3 bins. Its quality is:
> event_quality = 0.5 * max(0, 1 - onset_gap/3)
> + 0.5 * max(0, 1 - duration_gap/3)
> Eligible pairs are sorted by total gap and accepted greedily while both events remain unmatched.
> TemporalScore = 1 if P + R = 0
> 2 * sum(event_quality) / (P + R) otherwise
> ### Subtype Macro-F1
> For matched A events, A1, A2, and A3 are scored as a three-class macro-F1. For each subtype, a correctly matched event with the same subtype is a true positive. A matched A event with the wrong subtype adds one false positive for the submitted subtype and one false negative for the reference subtype. An unmatched submitted A event is a false positive for its subtype. An unmatched reference A event is a false negative for its subtype. B events do not affect this term.
> SubtypeF1[class] = 2TP[class] / (2TP[class] + FP[class] + FN[class])
> SubtypeMacroF1 = mean of defined subtype F1 values across A1, A2, and A3
> ### Chain Boundary Score
> Submitted and reference chains are matched one-to-one by interval overlap. Chain intervals are half-open: `[start_bin, end_bin)`. For a submitted chain `p` and reference chain `r`:
> iou = overlap([p.start_bin,p.end_bin), [r.start_bin,r.end_bin)) / union
> start_gap = abs(p.start_bin - r.start_bin)
> end_gap = abs(p.end_bin - r.end_bin)
> boundary_quality = 0.5 * max(0, 1 - start_gap/6)
> + 0.5 * max(0, 1 - end_gap/6)
> chain_quality = 0.5 * iou + 0.5 * boundary_quality
> Pairs with zero overlap are not eligible. Eligible pairs are matched greedily by descending quality.
> ChainScore = 1 if P + R = 0
> 2 * sum(chain_quality) / (P + R) otherwise
> ### CAP-Chain Consistency Score
> The CAP-chain consistency score uses only the submitted event and chain objects. It rewards chains that obey the CAP alternation rule and events that reference a chain declared in the same submitted row:
> chain_ratio = valid_chains / submitted_chains
> event_ratio = events_in_valid_chains / submitted_events
> linked_event_ratio = submitted_events_whose_chain_id_appears_in_chains_json / submitted_events
> ChainConsistencyScore = 0.45chain_ratio + 0.45event_ratio + 0.10*linked_event_ratio
> An empty event and chain submission receives CAP-chain consistency score `0.0` on these scored episodes. A valid chain must alternate A/B/A/B/A or longer, start and end with A, contain at least three A events and two B events, use one submitted chain ID, and keep the chain boundary aligned with its first and last A event. One-bin overlaps caused by 2-second quantization are tolerated; gross overlaps are invalid.
> ### Calibration Score
> For each submitted event or chain confidence `c`, the target is the matched quality for that object, or `0` if it is unmatched.
> CalibrationScore = max(0, 1 - 2 * mean((c - target)^2))
> An empty submission receives calibration `0.0` when the reference is non-empty.
> ### Final Score
> EpisodeScore = clip(0.35TemporalScore
> + 0.25SubtypeMacroF1
> + 0.20ChainScore
> + 0.15ChainConsistencyScore
> + 0.05*CalibrationScore, 0, 1)
> The final score is the mean episode score within each test recording group, followed by the mean across test groups.
> Wrong columns or column order, duplicate IDs, missing IDs, extra IDs, foreign IDs, malformed IDs, or answer-file ID problems raise `InvalidSubmissionError`. Row-local malformed JSON, non-finite values, invalid types, out-of-range bins or confidences, excessive JSON length, excessive event count, excessive chain count, impossible chain references, non-chronological events, or impossible schemas score `0.0` for that row without leaking private labels.
> &nbsp;
> Submissions
> 0

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Phonemic Transcription Retrieval

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72ffekq15czdy74ncfkxx7bx8bwv03
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Easy
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview:
> This is an information retrieval task. You are given a fixed corpus of 8,000 short documents and a set of 2,000 search queries. For each query you must search the corpus, rank the documents by relevance, and return the identifiers of the ten most relevant documents.
> The output is a ranked list of document identifiers, not text. Every value you submit is the identifier of a document that already exists in the supplied corpus. The task is ranking documents that are given to you, exactly as in the ranking step of a search engine.
> Queries and documents are written in two different symbol systems. A query is an English headword spelled in the Latin alphabet. A document is a phonemic transcription written in International Phonetic Alphabet symbols. Exactly one document in the corpus is the correct transcription of each query headword; that document is relevant, and the other 7,999 are not.
> Every document in the corpus has exactly the same number of phonemes, so document length carries no information that distinguishes one candidate from another.
> The corpus is also deliberately confusable. It is built so that every document has at least one, and on average four, other documents differing from it by exactly one phoneme. Getting a transcription almost right is therefore not enough: a single wrong phoneme puts a competing document ahead of the correct one. Precision at the level of the individual phoneme is what separates submissions here.
> What makes a document relevant:
> A document is relevant to a query when it is the phoneme sequence that the query headword is pronounced as. Relevance is therefore a correspondence between spelling and sound, not a correspondence between symbols. The two sides use different inventories: a letter is a unit of spelling, a phoneme is a unit of sound, and the mapping between them is many-to-many. A single letter can map to two phonemes, two letters can map to one phoneme, and a letter can map to nothing at all. Where a symbol appears to be shared between the two sides, the coincidence is usually misleading rather than helpful.
> The correspondence is compositional: a headword's transcription is built from its letters in order, under broad regularities plus a large set of exceptions. This is what makes the task learnable for headwords that never appear in training, and it is what a ranker has to model.
> Query noise:
> Some letters in the queries have been replaced by an underscore, in the manner of a damaged or partially legible word list. Only queries are degraded; corpus documents are intact. About 15 percent of letters are replaced in the training queries and about 36 percent in the evaluation queries, so evaluation queries are noisier than training queries. At least three letters of every query remain visible, and no two queries are identical after replacement.
> The replacement rate is high enough to matter. At this rate slightly under half of the evaluation queries are consistent with more than one word in the corpus, so for those queries the visible letters do not pin down a single answer and some irreducible uncertainty remains. This is deliberate: it keeps the task from collapsing into recovering the query word and then applying a rule.
> Evaluation:
> Metric: MAP@10, mean average precision at rank cut-off 10, a standard information retrieval ranking metric. Higher is better. Score range 0.0 to 1.0.
> Each query has exactly one relevant document, so MAP@10 reduces to mean reciprocal rank truncated at ten: a query scores 1/r when its relevant document is ranked at position r within your first ten results, and 0 when it is not in your first ten. The reported score is the mean over all queries.
> Only the first ten identifiers of each ranked list are scored. Identifiers beyond the tenth are ignored, and a repeated identifier is collapsed to its first occurrence.
> Dataset:
> Files in public/:
> corpus.csv - the retrieval corpus, 8,000 documents. This is the collection you search. doc_id - string - unique document identifier, the letter D followed by six digits. doc_text - string - the document: a phonemic transcription in IPA symbols, including stress marks. Every document has the same phoneme count once stress marks are removed.
> train.csv - 60,000 labelled query-document relevance pairs for training a ranker. pair_id - string - identifier of the training pair, the letter T followed by six digits. query_text - string - a training query: an English headword of 4 to 12 letters with about 15 percent of its letters replaced by underscores. relevant_doc_text - string - the transcription that is relevant to that training query, intact. Training transcriptions vary in length; only the corpus is length-uniform.
> test.csv - 2,000 evaluation queries. query_id - string - unique query identifier, the letter Q followed by six digits. query_text - string - the query headword to search with, about 36 percent of its letters replaced by underscores.
> sample_submission.csv - a correctly formatted submission containing placeholder rankings. query_id - string - identifier matching test.csv. retrieved_doc_ids - string - a placeholder ranked list; replace with your own rankings.
> For every query in test.csv the relevant document is present in corpus.csv. No headword appears in both train.csv and corpus.csv, and no transcription appears in both, so nothing in the evaluation set can be recovered by looking it up in the training data.
> Submission:
> Submit a CSV file with exactly two columns:
> query_id - string - must match a query_id from test.csv. retrieved_doc_ids - string - your ranked list of doc_id values, most relevant first, separated by single spaces. Provide up to ten identifiers.
> The submission must contain one row per evaluation query plus a header row. Every identifier must be a doc_id taken from corpus.csv. No extra columns are permitted.
> Example: query_id,retrieved_doc_ids Q000000,D004821 D000117 D006433 D002056 D007781 D001290 D006644 D003508 D005972 D005163 Q000001,D002914 D005105 D000662 D004470 D007218 D001837 D006053 D003396 D007729 D005541 Q000002,D007388 D001004 D005926 D000473 D003610 D003152 D004847 D002265 D006739 D004081
> Rules:
> The only valid ranking signal is the letter content of the query and the symbol content of the corpus documents.
> The following approaches are not allowed:
> Using query_id or doc_id, their numeric suffixes, or the row order of any provided file as a ranking signal. Identifiers are assigned after independent shuffles and carry no information about which document is relevant to which query.
> Using document length as a ranking feature. Every corpus document has the same phoneme count once stress marks are removed, so length is constant by construction and any apparent gain is noise.
> Treating the task as surface string matching between the two symbol systems. A character n-gram ranker over queries and documents scores about 0.058 MAP@10 here, barely above the floor. Submitting one is permitted but will not work; what is prohibited is presenting it as a solution to the intended task.
> Consulting an external pronunciation dictionary, phonemiser, grapheme-to-phoneme library, or any other outside resource that maps English spelling to phonemes, in order to look up a query's transcription instead of learning the correspondence from the supplied training pairs. This includes offline dictionaries bundled with a package, text-to-speech front ends, and querying any model for the purpose of recalling a known pronunciation. The correspondence must be learned from train.csv.
> Hardcoding rankings for specific query_id values.
> Using private, role-gated, or API-key-based models, or calling any external inference API at ranking time.
> Using non-reproducible external weights or artifacts that are not publicly available.
> The intended task is to learn the correspondence between spelling and sound from the supplied pairs and use it to rank candidate transcriptions. Because letters are replaced in the queries, a strong ranker must also infer what the missing letters contribute from the surrounding spelling. The approaches listed above bypass this by substituting identifier bookkeeping, a constant-valued feature, surface overlap, or an external lookup table for the correspondence being measured.
> Compute and model policy:
> This task runs on CPU. No GPU is required and none is provided. It is sized to be comfortably trainable on a CPU: queries are at most 12 letters, documents are 7 phonemes, and the combined symbol inventory is only a few dozen letters plus a few dozen phonemes, so a purpose-built character-level ranker needs on the order of a million parameters and trains on the 60,000 supplied pairs in minutes.
> A large pretrained language model is neither necessary nor practical here. Its subword vocabulary is a poor fit for a relation defined over individual letters and phonemes, it is far larger than this problem needs, and it will not fit the CPU budget. Training a small character-level ranker from scratch on the supplied pairs is the expected approach; a sequence model that aligns letters to phonemes is a natural fit.
> Submissions
> 98

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Heartbeat Interval Summary Learning

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bpdke8t1jvnsnfja40qnnmd8bwpqb
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> Train a randomly initialized model to predict heartbeat interval summary values. For each row, use the released interval-bin arrays and context fields to predict five target groups: interval-bin counts, short/mid/long counts, section-level mean and variability, adjacent-interval contrast counts, and overall interval consistency checks.
> The records are derived from wearable physiological monitoring sessions with heartbeat events annotated at a fixed sampling rate. Heartbeat timing is converted into binned inter-beat intervals, so useful models need to learn patterns such as stable intervals, sudden shorter or longer intervals, local variability, and how released interval arrays relate to the target summary values.
> The output is a fixed-schema set of numeric and categorical prediction heads, stored in JSON for submission. The task does not ask for clinical diagnosis or patient identity. Pretrained biosignal, ECG, wearable-signal, audio, temporal-signal, or foundation-model checkpoints are not allowed.
> Dataset
> The files are:
> train.csv: training rows with input fields and the target JSON record.
> test.csv: test rows with the same input fields but without the target.
> sample_submission.csv: a valid submission file with randomized nonzero placeholder records.
> Columns in train.csv:
> id (string): row identifier.
> panel_a_interval_bins_json (JSON array of integers): twelve released interval-bin values from one local event-interval array.
> panel_b_interval_bins_json (JSON array of integers): twelve released interval-bin values from a second local event-interval array.
> focus_interval_total (integer): number of interval measurements represented by the target state descriptor. Values range from 4 to 8.
> interval_context_json (JSON object): acquisition constants, released-array summaries, and schema reminders.
> answer_json (JSON object): target state descriptor using the schema in the Target Record section.
> Columns in test.csv:
> id (string)
> panel_a_interval_bins_json (JSON array of integers)
> panel_b_interval_bins_json (JSON array of integers)
> focus_interval_total (integer)
> interval_context_json (JSON object)
> interval_context_json contains:
> sampling_rate_hz (integer): sampling rate used to derive event intervals.
> rr_bin_width_ms (integer): interval-bin width in milliseconds.
> panel_a_summary (object): mean_rr_bin (integer) and variability_bin (string) for released array A.
> panel_b_summary (object): mean_rr_bin (integer) and variability_bin (string) for released array B.
> target_schema (object): compact reminder of the required target fields.
> Interval classes are defined from interval-bin values:
> short: bin value <= 70
> mid: bin value from 71 through 90
> long: bin value >= 91
> Target Record
> Submit one answer_json object per row with exactly these top-level keys:
> focus_interval_counts (array): count records for interval bins in the target state.
> interval_class_counts (array): short/mid/long count records using the thresholds above.
> section_summary (array): summary records for up to four target-state sections.
> contrast_pair_counts (array): count records for adjacent-bin contrasts inside the target state.
> interval_distribution_checks (object): global summary and context-edge consistency fields.
> Each object in focus_interval_counts must contain:
> rr_bin (integer): interval-bin value.
> count (integer): number of target-state intervals with that bin.
> Each object in interval_class_counts must contain:
> interval_class (string): one of short, mid, or long.
> count (integer): number of target-state intervals in that class.
> Each object in section_summary must contain:
> section (string): one of s1, s2, s3, or s4.
> mean_rr_bin (integer): rounded mean interval bin for that section.
> variability_bin (string): one of stable, mild, variable, or irregular.
> Section assignment uses focus_interval_total. For n target-state interval bins, interval index i is assigned by f = (i + 0.5) / n: s1 if f < 0.25, s2 if 0.25 <= f < 0.50, s3 if 0.50 <= f < 0.75, and s4 otherwise. This formula also applies when n is not divisible by four. If a section receives no interval, omit that section record.
> Each object in contrast_pair_counts must contain:
> contrast (string): one of lower, steady, or higher.
> count (integer): number of adjacent target-state interval pairs with that contrast.
> For adjacent contrasts, a change of at least 2 bins is higher, a change of at most -2 bins is lower, and all smaller changes are steady.
> interval_distribution_checks must contain:
> mean_rr_bin (integer): rounded mean of all target-state interval bins.
> min_rr_bin (integer): minimum target-state interval bin.
> max_rr_bin (integer): maximum target-state interval bin.
> variability_bin (string): one of stable, mild, variable, or irregular.
> edge_a_relation (string): lower, steady, or higher, comparing the edge of released array A with the first interval represented by the target state.
> edge_b_relation (string): lower, steady, or higher, comparing the final interval represented by the target state with the edge of released array B.
> contrast_switch_count (integer): number of target-state positions where the non-steady contrast sign changes.
> Submission
> Submit a CSV with exactly two columns:
> id (string): copied from test.csv.
> answer_json (JSON object encoded as a CSV string): prediction using the schema above.
> Use sample_submission.csv as the escaping reference for the CSV format. Malformed JSON receives zero for that row. Wrong columns, missing IDs, duplicate IDs, extra IDs, or wrong row counts are rejected.
> Evaluation
> The score is the mean row score over all test rows. Higher is better.
> row_score = 0.26 * focus_interval_score + 0.12 * interval_class_score + 0.24 * section_score + 0.16 * contrast_score + 0.22 * distribution_check_score
> focus_interval_score is duplicate-aware F1 over interval-bin counts. The scorer treats repeated records as repeated items, so two copies of the same bin count as two predicted items. Exact bin matches receive full credit. During matching, a predicted bin that is off by one from an unmatched true bin receives 0.20 credit. Precision is matched predicted count divided by total predicted count. Recall is matched true count divided by total true count. F1 is 2 * precision * recall / (precision + recall), or 0 when both precision and recall are zero.
> interval_class_score is duplicate-aware F1 over complete (interval_class, count) records. Repeated identical records are counted with multiplicity; overlap for a record is min(predicted_count_for_that_record, true_count_for_that_record).
> section_score is the mean over s1, s2, s3, and s4. For each section, 0.75 of the score comes from mean_rr_bin: exact match receives 1.0, off by one receives 0.20, and any larger error receives 0.0. The remaining 0.25 comes from exact variability_bin match. If both prediction and truth omit an empty section, that section scores 1.0; if only one side omits it, that section scores 0.0.
> contrast_score is duplicate-aware F1 over complete (contrast, count) records using the same multiset-overlap rule.
> distribution_check_score is:
> 0.28 * mean_rr_bin_score + 0.14 * min_rr_bin_score + 0.14 * max_rr_bin_score + 0.14 * variability_match + 0.10 * edge_a_relation_match + 0.10 * edge_b_relation_match + 0.10 * contrast_switch_count_score
> The three interval-bin scores use 1.0 for an exact match, 0.20 if off by one, and 0.0 otherwise. contrast_switch_count_score is 1.0 for an exact match, 0.25 if off by one, and 0.0 otherwise. Variability and edge-relation fields require exact matches.
> What Not To Use
> Do not use GPU acceleration.
> Do not use pretrained ECG, wearable-signal, biosignal, audio, temporal-signal, or foundation-model checkpoints.
> Do not use external heartbeat recordings, annotation databases, medical waveform corpora, or source repositories outside the released files.
> Do not use internet lookup, reverse lookup, APIs, or manual completion for test rows.
> Do not use subject identifiers, raw timestamps, or any private files.
> Do not hard-code answers by row ID.
> Submissions
> 50

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## UAV Motion-State Inference from Partial Sensor Measurements

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70wahrc04wgtz2nkgmjevqfn8bss29
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview
> This is a From Scratch structured multi-target prediction challenge. For each UAV sensor window, predict a fixed matrix of 24 categorical values: heading, vertical movement, and horizontal speed for each of eight predefined route blocks.
> Every row always has the same 24 categorical target columns, and each column has a small fixed integer range. There is no generated text or variable-length output. The challenge is to learn useful sensor representations from randomly initialized models and combine partial UWB ranging, inertial, attitude, and height measurements over the complete window.
> The reference positions used to construct the targets are absent from all public files. Some observable sensor values are also unavailable, as they can be in real wireless and onboard telemetry. A successful model must infer motion consistently across four range channels and complementary onboard measurements.
> From Scratch Rules
> All learned encoders, embeddings, feature extractors, and prediction heads must be randomly initialized and trained exclusively on the supplied files.
> The following are prohibited:
> Pretrained models or pretrained embeddings
> External datasets or externally trained components
> Source-record retrieval or matching against the original source
> TF-IDF features or external text/vector representations
> Manual lookup of hidden source trajectories
> Hand-designed numeric preprocessing, constrained inference, and models trained from random initialization on train.csv are allowed.
> Fixed Target Matrix
> Each 64-step input window is divided into eight fixed consecutive route blocks. For every block k from 0 through 7, predict three integer targets:
> block_k_heading: integer 0 through 7. These are eight heading sectors centred at successive 45-degree offsets from the UAV's initial recorded yaw. Horizontal displacement below 0.08 metres uses class 0.
> block_k_vertical: integer 0 for displacement below −0.12 metres, 1 for displacement from −0.12 through 0.12 metres, or 2 for displacement above 0.12 metres.
> block_k_speed: integer 0 for horizontal displacement below 0.12 metres, 1 for displacement from 0.12 up to 0.55 metres, or 2 for displacement of at least 0.55 metres.
> The eight blocks are fixed target positions, not variable-length tokens. Adjacent blocks may have identical states.
> Evaluation Metric
> A submission row is valid only when all 24 target cells are finite integers within their documented ranges. An invalid row receives zero for every metric component on that row. Structural quantities are derived from the fixed matrix only for evaluation: consecutive blocks with identical heading, vertical, and speed values form one run.
> For heading classes, circular distance is:
> δh(a,b) = min(|a − b|, 8 − |a − b|)
> The per-block attribute quality is:
> qblock = 0.50 × exp(−δh / 0.75) + 0.25 × 1[predicted vertical = true vertical] + 0.25 × exp(−|predicted speed − true speed| / 0.50)
> A = mean(qblock) over the eight fixed blocks
> For boundary quality, let P and T contain the positions after blocks 0 through 6 where the predicted and true state changes, respectively. When both sets are empty, B = 1; when exactly one set is empty, B = 0. Otherwise:
> B = 0.5 × mean over p in P of exp(−min over t in T |p − t|) + 0.5 × mean over t in T of exp(−min over p in P |t − p|)
> For structural alignment, compress consecutive identical block states into runs. A run's duration is the number of consecutive fixed route blocks contained in that run, so it is an integer from 1 through 8. The quality between predicted run i and true run j is:
> q(i,j) = 0.40 × exp(−δh(i,j) / 0.75) + 0.20 × 1[vertical_i = vertical_j] + 0.20 × exp(−|speed_i − speed_j| / 0.50) + 0.20 × exp(−|duration_i − duration_j|)
> Runs are aligned in temporal order using a dynamic program whose first row and first column are zero:
> D[i,j] = max(D[i−1,j], D[i,j−1], D[i−1,j−1] + q(i,j))
> Q = 2 × D[m,n] / (m + n)
> Here, m and n are the predicted and true numbers of runs. The final score is:
> row_score = 0.30 × B + 0.40 × A + 0.30 × Q
> Score = 100 × mean(row_score)
> The score is clipped to the interval from 0 to 100. A score of 100 requires all 24 target cells, every derived boundary, and every derived run to be correct.
> Measured on the shipped files and grader, a constant fixed-matrix prediction scores 33.581493, a public-only Extra-Trees block model scores 48.747562, and a randomly initialized temporal convolution-plus-attention model scores 55.180178. These are reproducible references, not score caps.
> Dataset
> train.csv
> Contains 14,135 labelled sensor windows.
> Input columns:
> sample_id — string — Opaque row identifier.
> range_stream — string — Sixty-four space-separated tokens; each token contains four period-separated UWB range codes.
> motion_stream — string — Sixty-four space-separated tokens; each token contains six period-separated gyroscope and acceleration codes.
> attitude_stream — string — Sixty-four space-separated tokens; each token contains five period-separated quaternion and height codes.
> packet_code — string — Balanced recorder packet code p0 or p1; it identifies neither a flight nor a target.
> Target columns are the 24 fixed integer columns block_0_heading, block_0_vertical, block_0_speed, continuing in the same order through block_7_heading, block_7_vertical, and block_7_speed.
> test.csv
> Contains 6,942 unlabelled windows with the five input columns above. Complete flights are held out, and no flight contributes windows to both train and test.
> sample_submission.csv
> Contains every test sample_id and all 24 target columns in the required order. Its values form a valid constant example prediction.
> metadata.json
> Documents the public stream layout, channel order, code ranges, missing-value code, and fixed target schema. It contains no answers, source identifiers, trajectories, or hidden group membership.
> Range fields use codes 00 through 63; all other numeric input fields use 00 through 31. The code xx denotes an unavailable measurement. Observable values were independently withheld at rates of 18% for range fields, 10% for motion fields, and 8% for attitude and height fields. Targets were not altered.
> Submission
> Submit a CSV with exactly 6,942 rows and exactly 25 columns. The exact order is sample_id, followed for each block k = 0, 1, ..., 7 by block_k_heading, block_k_vertical, and block_k_speed.
> The complete header is:
> sample_id,block_0_heading,block_0_vertical,block_0_speed,block_1_heading,block_1_vertical,block_1_speed,block_2_heading,block_2_vertical,block_2_speed,block_3_heading,block_3_vertical,block_3_speed,block_4_heading,block_4_vertical,block_4_speed,block_5_heading,block_5_vertical,block_5_speed,block_6_heading,block_6_vertical,block_6_speed,block_7_heading,block_7_vertical,block_7_speed
> A valid formatting example using real test ID 1 is shown below. Its target values are the public constant sample prediction and are not disclosed ground truth:
> 1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1
> The header is required. Extra or reordered columns, duplicate IDs, missing IDs, unknown IDs, and incorrect row counts are rejected. Row order does not matter. Invalid target cells give that row zero rather than changing any legitimate score.
> Modelling Direction
> A useful first approach is to learn local motion evidence from range differences and inertial changes, aggregate each set of eight sensor steps into its corresponding fixed route block, and predict the three correlated targets with separate randomly initialized heads. Stronger approaches can share contextual information across all eight blocks and use constrained inference to improve state-change consistency.
> Submissions
> 33

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Gait Contact Cycle Reconstruction From Muscle Signals

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74qve6gt30pg9cb6yjd1tmvs8bwtmt
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering
- Best/top context found: ↑ Higher is better

Full challenge description from page:

> Overview
> Each row contains a two-second walking window recorded from lower-limb muscle and joint-angle sensors. The left and right foot-contact sensors are withheld. Your task is to reconstruct the foot-contact cycle for that same window: the left/right contact runs, which time cells contain contact, where contact transitions occur, and the coarse gait phase across the window.
> This is a training-from-scratch signal modeling problem. The public signal preserves the time-varying muscle and joint-angle patterns that normally accompany stance, toe-off, swing, and heel-strike events, but the target foot-contact channels themselves are not included.
> Dataset
> The public files are:
> train.csv: training rows with public signal references and target JSON.
> test.csv: held-out rows with public signal references and no target JSON.
> signals.npz: compressed int16 signal tensor for both training and test rows.
> sample_submission.csv: schema-valid example submission.
> train.csv columns:
> id (string): row identifier.
> signal_packet_json (JSON string): describes where to find the signal tensor for this row.
> answer_format_json (JSON string): compact schema reminder for the required answer.
> answer_json (JSON string): target contact-cycle record.
> test.csv columns:
> id (string): row identifier.
> signal_packet_json (JSON string): signal file, row index, shape, sampling rate, duration, value encoding, and channel names.
> answer_format_json (JSON string): compact schema reminder for the required answer.
> signals.npz contains:
> signals (int16 array): shape [row_count, 12, 400]. Each row is a two-second window sampled at 200 Hz after deterministic normalization.
> row_ids (string array): row ids aligned to the first dimension of signals.
> channels (string array): the 12 public channels, including right hip angle, right knee angle, and ten lower-limb sEMG channels.
> The public signal values are per-window robust-z values, clipped and stored as int16. They are intended to preserve waveform shape, timing, and relative channel activity, not physical voltage units.
> Target JSON
> Submit one JSON object per test row:
> {
> "contact_run_cards": [
> {"side": "left", "start_cell": "t04", "end_cell": "t12", "duration_bin": "medium"}
> ],
> "left_contact_cells": ["t04", "t05"],
> "right_contact_cells": ["t20", "t21"],
> "transition_events": [
> {"side": "left", "edge": "on", "cell": "t04"},
> {"side": "right", "edge": "off", "cell": "t22"}
> ],
> "phase_cells": [
> {"cell": "t00", "phase": "right_contact"}
> ],
> "summary": {
> "left_contact_cell_count": 18,
> "right_contact_cell_count": 21,
> "double_support_cell_count": 5,
> "transition_count": 4
> }
> }
> Field definitions:
> left_contact_cells (array of strings): cells from t00 through t63 where the left foot is in contact.
> right_contact_cells (array of strings): cells from t00 through t63 where the right foot is in contact.
> contact_run_cards (array of objects): contiguous contact intervals. Each object has side (left or right), start_cell, end_cell, and duration_bin (short, medium, long, or extended). At most 20 run cards may be submitted.
> transition_events (array of objects): each object has side (left or right), edge (on for contact start or off for contact end), and cell (t00 through t63). At most 24 events may be submitted.
> phase_cells (array of 32 objects): exactly one object for each t00 through t31. phase must be one of left_contact, right_contact, double_support, or flight_or_gap.
> summary (object): four integer counts matching the predicted contact cells and transitions.
> Submission
> Submit a CSV with exactly two columns:
> id (string): must match a test row id.
> answer_json (JSON string): predicted contact-cycle record using the schema above.
> Example:
> id,answer_json
> gait_1111111111111111,"{""contact_run_cards"":[{""side"":""left"",""start_cell"":""t04"",""end_cell"":""t04"",""duration_bin"":""short""},{""side"":""right"",""start_cell"":""t20"",""end_cell"":""t20"",""duration_bin"":""short""}],""left_contact_cells"":[""t04""],""right_contact_cells"":[""t20""],""transition_events"":[{""side"":""left"",""edge"":""on"",""cell"":""t04""}],""phase_cells"":[{""cell"":""t00"",""phase"":""right_contact""},{""cell"":""t01"",""phase"":""right_contact""},{""cell"":""t02"",""phase"":""left_contact""},{""cell"":""t03"",""phase"":""left_contact""},{""cell"":""t04"",""phase"":""double_support""},{""cell"":""t05"",""phase"":""flight_or_gap""},{""cell"":""t06"",""phase"":""right_contact""},{""cell"":""t07"",""phase"":""right_contact""},{""cell"":""t08"",""phase"":""left_contact""},{""cell"":""t09"",""phase"":""left_contact""},{""cell"":""t10"",""phase"":""double_support""},{""cell"":""t11"",""phase"":""flight_or_gap""},{""cell"":""t12"",""phase"":""right_contact""},{""cell"":""t13"",""phase"":""right_contact""},{""cell"":""t14"",""phase"":""left_contact""},{""cell"":""t15"",""phase"":""left_contact""},{""cell"":""t16"",""phase"":""double_support""},{""cell"":""t17"",""phase"":""flight_or_gap""},{""cell"":""t18"",""phase"":""right_contact""},{""cell"":""t19"",""phase"":""right_contact""},{""cell"":""t20"",""phase"":""left_contact""},{""cell"":""t21"",""phase"":""left_contact""},{""cell"":""t22"",""phase"":""double_support""},{""cell"":""t23"",""phase"":""flight_or_gap""},{""cell"":""t24"",""phase"":""right_contact""},{""cell"":""t25"",""phase"":""right_contact""},{""cell"":""t26"",""phase"":""left_contact""},{""cell"":""t27"",""phase"":""left_contact""},{""cell"":""t28"",""phase"":""double_support""},{""cell"":""t29"",""phase"":""flight_or_gap""},{""cell"":""t30"",""phase"":""right_contact""},{""cell"":""t31"",""phase"":""right_contact""}],""summary"":{""left_contact_cell_count"":1,""right_contact_cell_count"":1,""double_support_cell_count"":0,""transition_count"":1}}"
> Evaluation
> The final score is the mean row score. Each row score is:
> 0.10 * side_contact_score + 0.40 * run_score + 0.30 * transition_score + 0.10 * phase_score + 0.10 * summary_score
> Definitions:
> side_contact_score is the average of duplicate-aware F1 for left_contact_cells and right_contact_cells.
> run_score is duplicate-aware F1 over exact (side, start_cell, end_cell, duration_bin) contact-run cards.
> transition_score is duplicate-aware F1 over exact (side, edge, cell) transition triples.
> phase_score is duplicate-aware F1 over exact (cell, phase) pairs for the 32 phase cells.
> summary_score is the mean of four count closeness terms. For left, right, and double-support counts, closeness is max(0, 1 - abs(predicted - true) / 64). For transition count, closeness is max(0, 1 - abs(predicted - true) / 16).
> Duplicate-aware F1 counts the minimum multiplicity of each predicted and true item as a match. Precision is matched predicted items divided by total predicted items. Recall is matched true items divided by total true items. If both predicted and true sets are empty, F1 is 1.0; if only one is empty, F1 is 0.0.
> Malformed JSON, invalid field values, duplicate phase cells, missing required fields, more than 20 contact-run cards, or more than 24 transition events score zero for that row. Wrong columns, wrong row count, missing ids, duplicate ids, or extra ids are rejected.
> What Not To Use
> Do not use external datasets or source copies.
> Do not use GPU acceleration for training or inference.
> Do not look up held-out rows on the internet.
> Do not hard-code test ids or answer dictionaries.
> Do not use hosted inference APIs or manual annotation of test rows.
> Do not use pretrained gait, biosignal, or contact-event checkpoints.
> Do not infer answers from files or fields that are not listed as public inputs.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## CauseLedger: Recall-Cause Reconstruction from Product Evidence

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx701paqptf2tdr6w3y4p4jnzx8btvf4
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: Not shown/captured
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text
- Best/top context found: ↑ Higher is better

Full challenge description from page:

> Task
> Train a language model from random initialization to recover two missing
> evidence spans from a food-recall record and assign the recall to a normalized
> hazard family. This is a joint structured-generation task: a strong system must
> learn regulatory phrasing, product identity patterns, and causal hazard cues
> rather than solve a single-label classification problem.
> Each example contains a product description with one <PRODUCT_GAP> and a
> recall-reason narrative with one <CAUSE_GAP>. Predict the exact text removed
> at each marker and one of the seven allowed hazard families.
> Structural Difference
> This is not ordinary recall classification and it is not generic masked-token
> prediction. The model must recover two semantically different, variable-length
> spans from separate regulatory fields and make a third ontology-level decision
> that must agree with both reconstructions. A classifier cannot produce the
> missing evidence, while an unconstrained denoising model receives no credit for
> hazard-family consistency. Standard recall-search systems are also insufficient
> because source lookup is prohibited and recall events are grouped across the
> public split. The intended solution is a single evidence-conditioned language
> model trained from random initialization on the supplied corpus.
> Public Split
> The prepared public data contains:
> File	Rows	Purpose
> public/train.csv	21,295	Training records with inputs and all three targets.
> public/test.csv	5,619	Records requiring predictions.
> public/sample_submission.csv	5,619	Submission template with the required IDs and columns.
> Recall events are assigned as indivisible groups using event_id together
> with normalized recalling-firm identity. Consequently, products reported under
> the same recall event do not cross from training into test. The grouping makes
> memorization of repeated notices less useful and tests evidence-conditioned
> language recovery.
> train.csv
> Column	Description
> record_id	Stable challenge identifier.
> masked_product_description	Product description containing exactly one <PRODUCT_GAP>.
> masked_reason_for_recall	Recall reason containing exactly one <CAUSE_GAP>.
> classification	FDA hazard class supplied as evidence.
> distribution_pattern	Distribution narrative supplied as evidence.
> code_info	Lot, batch, date, or product codes when available.
> product_type	Source product category.
> product_span	Text removed at <PRODUCT_GAP>.
> cause_span	Text removed at <CAUSE_GAP>.
> hazard_family	Normalized hazard target.
> test.csv
> test.csv has the same seven input columns as train.csv and omits
> product_span, cause_span, and hazard_family.
> Allowed hazard families are:
> microbial, undeclared_allergen, foreign_material,
> chemical_contaminant, labeling_or_packaging, process_or_quality, and
> other.
> Submission Format
> Submit submission.csv with exactly one row per record_id and these columns:
> record_id,product_span,cause_span,hazard_family
> CL-001799da02fefd2b,16 ounce jars,possible Salmonella contamination,microbial
> CL-0020821cbd40c0d0,dark chocolate bars,undeclared milk,undeclared_allergen
> Text containing commas must be CSV quoted according to standard CSV rules.
> Start from public/sample_submission.csv to preserve all required IDs.
> Metric
> The boundary-aware score is:
> 0.15 * product ordered-token F1
> + 0.20 * cause ordered-token F1
> + 0.15 * hazard macro-F1
> + 0.10 * product exact accuracy
> + 0.15 * cause exact accuracy
> + 0.10 * evidence-pair exact accuracy
> + 0.15 * full-record exact accuracy
> Text normalization lowercases each span, replaces non-alphanumeric runs with a
> single space, and trims surrounding whitespace. Ordered-token F1 uses the
> longest common token subsequence, so matching words receive credit only when
> they remain in the correct order; inserting a list of candidate words reduces
> precision. It does not compare unordered character bags.
> product exact accuracy and cause exact accuracy require the corresponding
> normalized span to match completely. evidence-pair exact accuracy requires
> both spans to be exact on the same record. full-record exact accuracy further
> requires the correct hazard family. Hazard macro-F1 gives equal weight to all
> seven families. Thus, partial reconstructions remain measurable, but a score
> near 1 requires precise span boundaries, correct word order, and joint
> cross-field consistency. Scores range from 0 to 1; higher is better.
> From-Scratch Requirement
> All learned parameters and all learned tokenization components must be trained
> only from public/train.csv, beginning from random initialization. Participants
> may design any neural architecture and may derive self-supervised corruptions
> or auxiliary targets solely from the supplied public training records.
> Not Allowed Methods
> Pretrained language models, pretrained encoders, pretrained embeddings, or
> pretrained tokenizers of any kind.
> Training text, labels, lexicons, model weights, or synthetic examples derived
> from any dataset other than the supplied public training file.
> Internet access, web search, or external recall databases
> during training or inference.
> Exact, fuzzy, hashed, or metadata-based lookup of records using recall IDs,
> event IDs, product text, firm identity, dates, or any other source attribute.
> Manual labeling or correction of test predictions.
> Test-label recovery, repeated grading-feedback probing, or any use of
> information produced by the grading system beyond the final aggregate score.
> Ensembling with, distilling from, or otherwise consulting a model trained on
> data outside public/train.csv.
> General-purpose numerical libraries, randomly initialized model
> implementations, and deterministic text-processing algorithms are allowed.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Pathway Diagram Interaction Program Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7b79n9wg8w650fzf22t7xh6n8bvg51
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Pathway Diagram Interaction Program Repair
> Overview
> Real pathway diagrams are compact engineering drawings for biological processes: boxes, ovals, arrows, inhibition marks, and typed interaction symbols describe how entities influence one another. Automated pathway tooling often starts with a nearly correct graph, then needs a careful repair pass when a direction is flipped, an interaction type is wrong, or an edge is missing or spurious.
> In this challenge, each row gives an anonymized pathway-style diagram image and a corrupted proposed directed graph. Nodes are labelled n0, n1, and so on in the image and in proposed_graph_json. Your job is to emit the minimal JSON repair program that transforms the proposed graph into the graph shown in the image.
> This is a From Scratch challenge and must run on CPU only within 1.5 hours on 10 CPU cores and 62 GB RAM. The intended solution is a learned local model or hybrid from-scratch pipeline trained on the public examples: small image encoders, graph features, edge-candidate scoring, constrained decoding, and lightweight ensembles are appropriate.
> What Not To Use:
> Pretrained vision-language models, hosted APIs, or external diagram-understanding services.
> Source lookup, raw pathway files, source filenames, public pathway databases, or reverse-image matching.
> Row id, file order, image hash, file size, or metadata shortcuts.
> Parser-only systems that ignore the public training labels and rely only on fixed drawing rules.
> Hardcoded answers, private answer access, grader probing, or prepare-script introspection.
> GPU-only methods or large fine-tuning runs that violate the CPU budget.
> Enforcement on invalid approaches: submissions may be rejected before payout if they solve by source lookup, metadata shortcuts, fixed template inversion, or any method outside the intended from-scratch pathway-diagram repair task.
> Intended Approach
> A strong CPU solution should use the training diagrams to learn how node shapes, arrowheads, inhibition bars, line labels, and edge geometry correspond to graph edits. Practical approaches include generating candidate node pairs from proposed_graph_json, extracting image patches around candidate edges, training small CPU-friendly classifiers for add/delete/relabel/reverse decisions, and decoding a valid edit program with graph consistency checks.
> Evaluation
> Submit one repair_json program per test row plus a confidence. The grader executes your program on the row's proposed graph, compares the repaired graph with the hidden target graph, and also checks whether your program matches the minimal repair.
> Allowed operations:
> ADD_EDGE: add a directed typed edge.
> DELETE_EDGE: remove a directed typed edge.
> RELABEL_EDGE: change an existing edge type.
> REVERSE_EDGE: reverse an existing edge direction.
> Per-row scoring:
> GraphScore = 0.65*typed_edge_F1
> + 0.20*directed_pair_F1
> + 0.15*type_accuracy
> EditScore  = F1 over minimal edit operations
> CountScore = max(0, 1 - abs(pred_count - true_count) / true_count)
> Correctness = 0.62*GraphScore
> + 0.26*EditScore
> + 0.12*CountScore
> Calibration = 1 - abs(confidence - Correctness)
> RowScore    = 0.97*Correctness + 0.03*Calibration
> Final score:
> Final = 0.74*mean(RowScore)
> + 0.10*worst pathway bucket
> + 0.08*worst density bucket
> + 0.08*worst render style
> Hidden buckets are private robustness groups. Higher is better. The theoretical minimum is 0.0; the theoretical maximum is 1.0. A perfect valid reference scores exactly 1.0.
> Structural submission errors raise an invalid-submission error: wrong columns, reordered columns, duplicate ids, missing ids, extra ids, non-finite confidence, or confidence outside [0,1]. Row-local malformed or oversized repair_json values score zero for that row without leaking answers.
> Dataset
> The released data is under public/. Paths are relative to the public/ root.
> File overview
> | Item | Description |
> |---|---|
> | train.csv | Inputs + labels |
> | test.csv | Inputs only |
> | train/images/ | Train diagrams |
> | test/images/ | Test diagrams |
> | metadata.json | Public schema info |
> | sample_submission.csv | Weak valid sample |
> train.csv columns
> | Column | Type | Description |
> |---|---|---|
> | id | string | Opaque row id |
> | image_path | string | Diagram image path |
> | proposed_graph_json | string | Corrupted graph |
> | prompt | string | Row instruction |
> | repair_json | string | Train target |
> test.csv columns
> | Column | Type | Description |
> |---|---|---|
> | id | string | Opaque row id |
> | image_path | string | Diagram image path |
> | proposed_graph_json | string | Corrupted graph |
> | prompt | string | Row instruction |
> proposed_graph_json
> proposed_graph_json is a JSON object with nodes, edges, allowed_edge_types, and allowed_ops. Each node has id and kind. Each edge has src, dst, and type. Edge types are:
> activation, binding, catalysis, conversion, inhibition, stimulation, transcription
> Submission
> Submit a CSV with exactly one row per test id and exactly these columns in this order:
> | Column | Type | Constraint |
> |---|---|---|
> | id | string | Same ids as test |
> | repair_json | string | JSON edit list |
> | confidence | float | In [0,1] |
> Example:
> id,repair_json,confidence
> PDR_example01,"[{""op"":""ADD_EDGE"",""src"":""n0"",""dst"":""n2"",""type"":""conversion""}]",0.58
> PDR_example02,"[{""op"":""REVERSE_EDGE"",""src"":""n4"",""dst"":""n1"",""type"":""inhibition""}]",0.61
> Operation schemas:
> ADD_EDGE:     {"op":"ADD_EDGE","src":"n0","dst":"n1","type":"conversion"}
> DELETE_EDGE:  {"op":"DELETE_EDGE","src":"n0","dst":"n1","type":"conversion"}
> RELABEL_EDGE: {"op":"RELABEL_EDGE","src":"n0","dst":"n1","from_type":"activation","to_type":"inhibition"}
> REVERSE_EDGE: {"op":"REVERSE_EDGE","src":"n0","dst":"n1","type":"conversion"}
> For REVERSE_EDGE, src and dst name the existing edge endpoints before the operation is applied; the operation reverses that edge in the repaired graph.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## FiberCharge: Optical-Electrical Retired Battery Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77fakft4zqz0e5asr3xd7nw98aqn5y
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> FiberCharge: Optical-Electrical Retired Battery Reconstruction
> Objective
> Each example is one real retired battery cell represented by a compact optical/electrical diagnostic packet. The packet contains ten aligned measurement positions from the first three minutes of a controlled response: packet-axis coordinate, voltage change from the first sample, sign-level normalized current, masked optical-fiber wavelength change, and an optical observation mask.
> For every test episode_id, submit four source-measured outputs:
> chemistry: one of LFP or LMO.
> soh: continuous state of health under the documented nominal-capacity definition.
> capacity_q00 through capacity_q23: complete-discharge voltage values sampled at fixed capacity fractions.
> optical_q00 through optical_q31: hidden optical-fiber wavelength deltas inside the withheld diagnostic segment.
> The hidden capacity and optical targets are measured from the same physical cell as the public packet. They are not synthetic extrapolations and should not be treated as decorative copies of a single scalar label.
> Task
> Load each .npz packet referenced by test.csv and predict exactly one row for each episode_id. Use the public diagnostic arrays jointly with the training rows and their targets to recover cell-level properties, capacity-response shape, and missing optical measurements from compact multimodal evidence.
> The useful signal is the paired optical/electrical response shape. Metadata, file order, and source identity have been removed from the public files, so a strong solution should learn from the signal arrays rather than from lookup keys.
> Intended Approaches
> Treat this as a CPU-capable from-scratch or fine-tuning scientific representation-learning problem with multiple coupled heads. Strong solutions will fine-tune an offline open-source numerical or sensor encoder, or train their own compact architecture from scratch, using only public/train.csv and the referenced packet arrays. Useful approaches include:
> compact neural encoders over fixed-length packet arrays, such as residual MLPs, small convolutional blocks, or cross-channel attention models;
> multimodal fusion over voltage, current, observed optical signal, and the optical mask;
> multi-output heads or ensembles for chemistry, SOH, complete-discharge response, and optical repair;
> feature baselines using slopes, extrema, early-response shape, mask-aware interpolation features, and chemistry-aware calibration;
> uncertainty-aware validation across the four heads, because improving only one head leaves substantial score unused.
> Electrical-only, optical-only, constant-prior, and interpolation-only solutions are useful diagnostics, but the intended solver should exploit complementary information from both modalities.
> From-scratch path: initialize a compact model randomly and train it only on public/train.csv plus the referenced packets. The packet schema is small enough for many local validation runs under the 10-core CPU budget, and learning the task-specific optical/electrical representation is the central challenge.
> Fine-tuning path: adapting an open-source, offline numerical or sensor encoder is allowed when all weights are available before the run and all tuning uses only the public training split. Generic pretrained language or vision models are not expected to carry the battery-sensor structure by themselves, so a solution still needs task-specific fitting on the released packet arrays.
> Compute And Method Constraints
> This challenge is configured for CPU-only solving. Plan for 10 CPU cores, 62 GB RAM, and a maximum solution runtime of 1.5 hours. The intended competitive route is to train or adapt a compact offline model on public/train.csv and the referenced packet arrays.
> Classical feature pipelines are allowed as validation baselines, but the benchmark is written for efficient CPU-based model development. Hosted APIs, runtime downloads, closed remote inference, private files, and answer-dictionary shortcuts are not permitted.
> What Not To Do
> Do not search for, download, fingerprint, or join against the original public source archive.
> Do not use source filenames, source cell IDs, original row order, absolute collection paths, absolute timestamps, battery model strings, or source checksums.
> Do not infer answers from prepared file sizes, packet byte hashes, episode-id hashes, train/test row order, filesystem metadata, mtimes, or hidden split-specific constants.
> Do not use private files, answer dictionaries, hosted APIs, network lookup, runtime-downloaded teacher predictions, or manual source matching.
> Do not collapse the task into a fixed chemistry guess, a scalar SOH-only model, a capacity curve copied from SOH, or a local interpolation-only optical repair rule.
> Do not submit malformed CSVs or values designed to exploit grader parsing, clipping, range checks, or error handling.
> Enforcement on invalid approaches: submissions may be reviewed for source lookup, external calls, metadata-only behavior, fixed answer maps, private-answer access, and approaches that avoid the required multimodal reconstruction contract. The goal is learned optical/electrical evidence reconstruction, not recovery of upstream source labels.
> Data
> Prepared data is provided to solvers under public/.
> File Overview
> | Item | Description |
> |---|---|
> | train.csv | 161 training episodes with opaque IDs, packet paths, chemistry labels, SOH labels, capacity-response labels, and hidden-optical labels |
> | test.csv | 96 test episodes with opaque IDs and packet paths only |
> | signals/*.npz | 257 compressed NumPy diagnostic packets, one per retained physical cell |
> | query_times.csv | Query-index map for capacity_qNN and optical_qNN columns |
> | signal_schema.json | Packet arrays, shapes, units, input-window definition, SOH definition, capacity query fractions, and optical query positions |
> | sample_submission.csv | Format-valid weak prior submission with one row per test episode_id |
> train.csv Columns
> | Column | Type | Meaning |
> |---|---|---|
> | episode_id | string | Opaque public row ID |
> | signal_path | string | Relative path to the packet under public/ |
> | chemistry | string | Train-only chemistry label, one of LFP or LMO |
> | soh | float | Train-only continuous state-of-health label |
> | capacity_q00 through capacity_q23 | float | Train-only complete-discharge voltage targets in volts |
> | optical_q00 through optical_q31 | float | Train-only hidden optical-fiber wavelength-delta targets in nanometers |
> test.csv Columns
> | Column | Type | Meaning |
> |---|---|---|
> | episode_id | string | Opaque public row ID |
> | signal_path | string | Relative path to the packet under public/ |
> There are no target columns in test.csv.
> query_times.csv Columns
> | Column | Type | Meaning |
> |---|---|---|
> | target_head | string | Target family, either capacity or optical |
> | column | string | Submission column name such as capacity_q00 or optical_q00 |
> | signal_index | integer or blank | Packet sample index where applicable |
> | relative_time_s | float or blank | Optical query coordinate in seconds where applicable |
> | capacity_fraction | float or blank | Capacity-response query fraction where applicable |
> Signal Packet Schema
> | Array | Type | Shape | Meaning |
> |---|---|---|---|
> | relative_time_s | float32 | (10,) | Packet-axis coordinates from 0 to 180 seconds |
> | voltage_delta_v | float32 | (10,) | Voltage relative to the first public sample, quantized to 0.5 V |
> | current_norm | float32 | (10,) | Current divided by max packet magnitude and quantized to sign-level values |
> | optical_delta_nm_masked | float32 | (10,) | Optical wavelength delta with hidden interval samples set to zero |
> | optical_observed_mask | uint8 | (10,) | 1 for observed optical samples and 0 for hidden samples |
> The packet arrays share a common sample axis of length 10. The public input axis is [0, 20, 40, 60, 80, 100, 120, 140, 160, 180] seconds. In the public optical array, packet positions inside the hidden segment are masked: the 60, 80, 100, and 120 second packet entries have optical_observed_mask = 0 and optical_delta_nm_masked = 0. The 32 optical_qNN targets are denser source measurements over the same withheld segment at two-second spacing from 60 through 122 seconds, so most optical query coordinates are not public packet samples.
> Target Column Groups
> | Target group | Type | Meaning |
> |---|---|---|
> | chemistry | string enum | Class label with allowed values LFP and LMO |
> | soh | float | Measured full-discharge capacity divided by chemistry nominal capacity |
> | capacity_q00 through capacity_q23 | float vector | Source-measured full capacity-test discharge voltage sampled at 24 fixed capacity fractions from 0.05 to 0.95 |
> | optical_q00 through optical_q31 | float vector | Source-measured optical-fiber wavelength deltas at 32 fixed hidden query positions from 60 to 122 seconds |
> The split is disjoint by physical cell. The prepared data retains 257 source-quality cells after excluding 8 cells with nonphysical optical dropouts.
> Submission Format
> Submit exactly one CSV row per episode_id in test.csv. Columns must appear in exactly this order:
> episode_id,chemistry,soh,capacity_q00,...,capacity_q23,optical_q00,...,optical_q31
> chemistry must be LFP or LMO.
> Submission Columns
> | Column | Type | Constraint |
> |---|---|---|
> | episode_id | string | Exact same ID set as test.csv, with no missing, extra, duplicate, or foreign IDs |
> | chemistry | string enum | LFP or LMO |
> | soh | float | Finite value in [0.40, 1.10] |
> | capacity_q00 through capacity_q23 | float vector | Finite voltages in [2.0, 4.3] |
> | optical_q00 through optical_q31 | float vector | Finite wavelength deltas in [-0.10, 0.10] |
> Accepted numeric ranges:
> soh: [0.40, 1.10]
> capacity_qNN: [2.0, 4.3] volts
> optical_qNN: [-0.10, 0.10] nm
> Example:
> episode_id,chemistry,soh,capacity_q00,capacity_q01,capacity_q02,capacity_q03,capacity_q04,capacity_q05,capacity_q06,capacity_q07,capacity_q08,capacity_q09,capacity_q10,capacity_q11,capacity_q12,capacity_q13,capacity_q14,capacity_q15,capacity_q16,capacity_q17,capacity_q18,capacity_q19,capacity_q20,capacity_q21,capacity_q22,capacity_q23,optical_q00,optical_q01,optical_q02,optical_q03,optical_q04,optical_q05,optical_q06,optical_q07,optical_q08,optical_q09,optical_q10,optical_q11,optical_q12,optical_q13,optical_q14,optical_q15,optical_q16,optical_q17,optical_q18,optical_q19,optical_q20,optical_q21,optical_q22,optical_q23,optical_q24,optical_q25,optical_q26,optical_q27,optical_q28,optical_q29,optical_q30,optical_q31
> fc_01689c3aefbd6b3c51,LFP,0.80670786,3.506758,3.496130,3.489702,3.483783,3.478186,3.471994,3.464398,3.455814,3.448615,3.443075,3.438025,3.432547,3.426006,3.418398,3.409540,3.399441,3.387975,3.375882,3.362429,3.345745,3.325261,3.305248,3.274925,3.170149,0.000087,0.000155,0.000155,0.000273,0.000230,0.000304,0.000335,0.000348,0.000373,0.000348,0.000509,0.000596,0.000609,0.000683,0.000621,0.000801,0.000683,0.000807,0.000752,0.000739,0.000839,0.000894,0.000969,0.000969,0.001012,0.000932,0.001099,0.001062,0.001137,0.001248,0.001248,0.001248
> ## Evaluation
> The metric is a bounded deterministic composite. Higher is better. The theoretical minimum is `0.0` and the theoretical maximum is `1.0`. A perfect valid submission scores exactly `1.0`.
> For one row, the score is:
> row_score =
> 0.10 * chemistry_accuracy
> 0.30 * soh_score
> 0.12 * capacity_response_score
> 0.18 * hidden_optical_score
> 0.30 * continuous_balance_score
> Continuous components use bounded linear tolerances:
> soh_score = max(0, 1 - abs(pred - truth) / 0.030)
> capacity_response_score = mean(max(0, 1 - abs(pred - truth) / 0.040))
> hidden_optical_score = mean(max(0, 1 - abs(pred - truth) / 0.0012))
> continuous_balance_score = min(soh_score, capacity_response_score, hidden_optical_score)
> The final score is not the simple mean of row scores. Private answer rows are grouped by chemistry and SOH band. The grader computes the mean row score in each private group, averages those group scores equally, and combines that macro score with the mean of the lowest-scoring 25% of test rows:
> macro_stratum_score = mean(mean(row_score within each private chemistry/SOH stratum))
> lower_quartile_score = mean(lowest 25% of row_score values)
> final_score = 0.65 macro_stratum_score + 0.35 lower_quartile_score
> The balance, macro-stratum, and lower-quartile terms are deterministic and use only documented target errors plus private labels already needed for grading. They reward submissions that recover SOH, capacity response, and hidden optical response across the full private test distribution instead of optimizing only the easiest cells or one output family.
> Structural submission errors raise `InvalidSubmissionError`. This includes wrong column names, wrong column order, missing rows, extra rows, duplicate IDs, foreign IDs, malformed files, non-UTF-8 files, NUL bytes, and oversized files.
> Row-local value failures score `0.0` for that affected row without leaking private labels. This includes invalid chemistry enums, nonfinite numeric values, and numeric values outside the accepted ranges.
> The public `sample_submission.csv` is a weak prior template and scores `0.1273959063`.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Minority Serovar Cell Detection

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx79t81352wwa69asf3j5a3m4n8c3d42
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Overview:
> A food-safety laboratory screens a suspect batch by imaging it under a hyperspectral microscope. One field of view yields a few dozen individual bacterial cells, and each cell gives a reflectance spectrum across 302 wavebands from 401 nm to 1001 nm. Most of those cells belong to the strain that dominates the sample. Some may not.
> Detecting the ones that do not is the point. A batch carrying a second, minority strain alongside the dominant one is the case that conventional screening handles worst: culture-based serotyping reports what grows best, and a strain present at a few percent can be reported as absent. It is also the case that matters, because the minority strain is not reliably the less dangerous one.
> Your task is per cell. For every cell in every evaluation sample, output 1 if that cell belongs to a different serovar from the sample's dominant one, and 0 if it belongs to the dominant serovar. A sample may contain no foreign cells at all, and reporting a clean sample as clean is scored as a correct answer.
> Each sample contains exactly 16 cells. Between 0 and 4 of them are foreign, and roughly one sample in nine is clean. The number of foreign cells is never told to you and is not recoverable from the sample size, which is fixed at 16 regardless. Deciding how many cells to flag, including flagging none, is part of the task.
> Why this is not outlier detection:
> Every sample also contains 2 cells that come from a different microscope field but the SAME serovar as the dominant one. These are not foreign and must not be flagged.
> This matters more than it sounds. Cells imaged in one field share an acquisition: the same illumination, the same focus, the same detector state. So the cells from that second field genuinely look different from the rest of the sample, for reasons that have nothing to do with which serovar they are. A method that simply ranks cells by how far they sit from the sample's average spectrum will find those cells and flag them, and be wrong. That is measurable rather than hypothetical: on this evaluation set, flagging the three cells furthest from the sample mean scores 0.195, and the cosine version scores 0.214, against 0.108 for flagging nothing at all. Distance from the crowd is a weak signal here, and a partly misleading one.
> What separates a real solution is modelling what the serovars themselves look like, then asking which cells disagree with the sample's dominant one. That requires learning from the labelled training cells, not from the geometry of a single sample.
> How to approach it:
> This challenge is meant to be solved by training a model from scratch on the supplied training data. The training file gives every training cell's serovar, so the natural route is to train a serovar classifier on those cells, apply it to the 16 cells of an evaluation sample, take the dominant serovar across the sample, and flag the cells that disagree with it. A reference implementation of exactly that idea, using multinomial logistic regression on the raw 302 wavebands and a probability threshold, scores 0.372 on this evaluation set. That is the number to beat, and it is a long way below a perfect score.
> There are no pretrained models for this modality. A 302-band reflectance spectrum from a single bacterium is not an image, not text and not audio, and no public backbone has been trained on anything of the kind, so transfer learning has nothing to transfer. Everything you use has to be fitted on the training data provided here. That is a feature of the problem, not a restriction imposed on it.
> All of this runs comfortably on CPU. There are 15,888 training rows of 302 floats each; a small multilayer perceptron, a one-dimensional convolutional network over the spectrum, or gradient boosting all train in minutes without a GPU. Spectroscopic preprocessing is likely to pay for itself: band smoothing, first and second derivatives, and reducing 302 correlated wavebands to a smaller basis are standard for this kind of data and are cheap.
> Split:
> Training samples and evaluation samples are built from disjoint sets of microscope fields. No field that contributed a cell to training contributes any cell to evaluation. A model therefore has to generalise to acquisitions it has never seen, which is the deployment condition. Evaluation spectra also carry slightly more detector noise than training spectra.
> Evaluation:
> Metric: mean per-sample F1. Higher is better. Score range 0.0 to 1.0.
> For one sample, take the set of cells you flagged and the set of cells that are genuinely foreign. The sample scores 2 times the number of cells in both sets, divided by the sum of the two set sizes. A sample with no foreign cells scores 1.0 if you flag none of its cells, and 0.0 if you flag any. The reported score is the mean over all 490 evaluation samples, so every sample counts equally regardless of how many foreign cells it holds.
> Because a sample is scored as a set, flagging everything does not work: it collects every foreign cell but drowns them among twelve or more correct ones, and it scores 0 on every clean sample. Flagging all 16 cells of every sample scores 0.234 on this evaluation set.
> Dataset:
> public/train.csv - 15,888 training cells, forming 993 training samples. row_id - string - identifier of this cell within the challenge, train_ followed by six digits. sample_id - string - identifier of the sample this cell belongs to, train_s followed by five digits. The 16 rows sharing a sample_id are one microscope field of view. cell_index - integer - position of the cell within its sample, 0 to 15. Assigned after shuffling, so it carries no information about whether the cell is foreign. nm_401p00 through nm_1000p90 - float - 302 reflectance values, one per waveband, named for the wavelength in nanometres with the decimal point written as the letter p. serovar - string - the serovar of this cell, one of Enteritidis, I4, Infantis, Johannesburg, Kentucky. Supplied for training cells only. is_contaminant - integer - the training target, 1 if this cell's serovar differs from its sample's dominant serovar, 0 otherwise.
> public/test.csv - 7,840 evaluation cells, forming 490 evaluation samples. Same columns as train.csv except that serovar and is_contaminant are not supplied. row_id - string - identifier of this cell, test_ followed by six digits. sample_id - string - identifier of the sample, test_s followed by five digits. cell_index - integer - position within the sample, 0 to 15. nm_401p00 through nm_1000p90 - float - 302 reflectance values.
> public/sample_submission.csv - a correctly formatted submission with 7,840 rows. It predicts 0 for every cell, which is the same as declaring every sample clean; it shows the format, it is not an answer. row_id - string - identifier of the cell, matching test.csv. prediction - integer - 0 or 1.
> Submission:
> Submit a CSV with a header row and exactly two columns, in this order. row_id - string - identifier of the cell, exactly as it appears in test.csv. prediction - integer - 1 if you judge this cell to belong to a different serovar from its sample's dominant serovar, 0 otherwise.
> Example of a valid submission:
> row_id,prediction test_000000,0 test_000001,0 test_000002,1 test_000003,0
> Requirements: exactly 7,840 rows plus the header; one row for every row_id in test.csv and no others; no duplicate row_id. Values of 0 and 1 are expected; a probability between 0 and 1 is accepted and is treated as a flag when it reaches 0.5.
> Rules:
> The only valid input signal is the 302 reflectance values of the cells, considered together with the other cells of the same sample.
> The following approaches are not allowed:
> Hardcoding predictions for specific evaluation rows or samples.
> Using row_id, cell_index, row position within the file, or any other bookkeeping field as a prediction signal. Cell order within a sample is shuffled and the correlation between cell_index and the answer is -0.005.
> Recovering the answer by matching evaluation spectra against an external copy of the underlying measurements. The spectra originate in published laboratory work, so a table pairing similar spectra with their serovar and their field of origin exists outside this challenge. Looking up an evaluation cell there, by nearest-neighbour matching or any other means, recovers both its serovar and the field it came from, which is the entire answer. This is prohibited. The restriction is load-bearing: the challenge measures whether a model can learn a spectral signature that generalises to unseen acquisitions, and a lookup answers a different question entirely.
> Using private, role-gated, or API-key-based models, or calling any external inference API at inference time.
> Using non-reproducible external weights or artifacts not publicly available.
> The intended task is to learn, from labelled training cells, what distinguishes one serovar's spectrum from another's, and then to apply that within a sample to separate the dominant strain from a minority one. Ranking cells by distance from the sample average does not do this and has been measured to perform poorly, because the sample deliberately contains same-serovar cells from a second acquisition that such a method flags incorrectly. Reading the answer out of an external copy of the source measurements does not do it either.
> Pretrained model policy:
> Training from scratch is the expected route and no pretrained model is applicable, because no public backbone has been trained on single-cell hyperspectral reflectance. If you nonetheless use a pretrained component, it must be publicly available and reproducible, and the fitting that produces your predictions must genuinely use the supplied training cells. A real solution generalises to microscope fields that never appear in training, which is what the split is built to test.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Solar Wind Turbulence Prediction from Hourly Averages

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c7dfrhsyc8pcptyr3txqw1n8c0s8m
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Solar Wind Turbulence Prediction from Hourly Averages
> Overview
> Almost everything about the solar wind that matters for how it couples to the Earth lives below the hour. Directional discontinuities in the interplanetary magnetic field, the level of AlfvÃ©nic turbulence, the sudden field rotations that trigger reconnection â€” these are minute-scale phenomena. The OMNI reference series has one-minute resolution only from 1995 onward. Hourly resolution goes back to 1963. Three solar cycles of the space age are therefore invisible to every modern sub-hour event catalogue, not because nobody measured them, but because what survives is already averaged.
> This challenge asks whether that averaging can be partly undone by a model.
> Each case is a twelve-hour stretch of real solar wind. You receive only the hourly means of
> the standard OMNI moments for those twelve hours: the mean magnetic-field vector, the mean
> velocity vector, mean speed, density, temperature, flow pressure, plasma beta and AlfvÃ©n Mach
> number. You do not receive the standard deviations, the RMS columns, the per-minute point
> counts, the mean of the scalar field magnitude, the timestamps, or the spacecraft ids. From those
> twelve rows of averages you must reconstruct three properties of the one-minute record hidden
> inside them: which hours were the most magnetically turbulent, how many directional
> discontinuities each hour contained, and how the window behaved overall.
> The honest reason this is hard: an hourly mean is a boxcar average followed by decimation, and the
> within-hour detail sits in that operator's null space. No amount of algebra on the published means
> recovers it, and there is no deconvolution to run. What is recoverable is statistical. Solar-wind
> plasma comes in regimes â€” fast AlfvÃ©nic streams out of coronal holes, slow dense wind, stream
> interaction regions, ejecta â€” and each regime carries a characteristic minute-scale fluctuation
> signature. The published moments say a great deal about which regime you are in. Turning that into
> a per-hour ranking and a per-hour discontinuity count is a learning problem, and only a learning
> problem.
> Two details are worth knowing before you start. First, the mean field vector is published but
> the mean of the scalar field magnitude is not: the two differ by exactly the amount the field
> fluctuated inside the hour, and publishing both would hand over the answer. Second, the hourly
> means of plasma beta and AlfvÃ©n Mach number are means of quantities that depend non-linearly on
> the minute-scale field, so they do carry partial information about the fluctuation level. That is
> a real, legitimate signal and you are meant to find it â€” it is one of the things that separates a
> trained model from a rule.
> Whole calendar years are held out for the test set, spread across the solar cycle, so the test
> windows come from solar-wind conditions the training years never contained.
> Relation to Prior Work
> Hourly solar-wind data has been studied for decades and coarse-to-fine inference is an active
> area, so it is worth being precise about what has and has not been done, because the difference is
> the whole task.
> Thatcher and MÃ¼ller (2013), Synthetic four-solar-cycle solar wind at 1 AU generated from the OMNI data set, J. Geophys. Res. Space Physics, doi:10.1002/jgra.50150, is the nearest neighbour on the same data backbone. It seeds on hourly solar-wind data and synthesises series for ecliptic longitudes that were never observed, using the category-based constrained random walk of Thatcher and MÃ¼ller (2011), doi:10.1029/2011JA017027. Its extrapolation is spatial and its output cadence is hourly â€” it fills a 1 AU ring across four solar cycles, a span the 1-minute record does not even cover. It never produces minute-scale structure, and it has no held-out minute-scale truth to be scored against.
> Lockwood et al. (2022), Solar Windâ€“Magnetosphere Coupling Functions: Pitfalls, Limitations, and Applications, Space Weather, doi:10.1029/2021SW002989, and the surrounding coupling-function literature quantify how much less accurate an hourly mean becomes as intra-hour data availability falls. That characterises the error budget of the forward averaging operator. It does not invert it.
> Borovsky (2003, 2019) conditions sub-hour turbulence properties on hourly-derivable plasma regime, which is the physics this challenge leans on. But that work reads the fluctuation level straight out of the hourly RMS and sigma columns â€” precisely the columns deleted here â€” and reports descriptive statistics, not a held-out prediction.
> Probabilistic temporal downscaling and temporal super-resolution in weather, wind and solar generation, and hydrology (the HourGlass family and its relatives) share the coarse-to-fine-in-time shape. They reconstruct a continuous high-cadence field and are scored by pointwise or distributional error against it.
> What this benchmark asks for is neither a synthesised series nor an error bar. It is three coupled discrete objects â€” a within-window permutation of the twelve hours by hidden fluctuation amplitude, a per-hour ordinal burst word, and a regime certificate constrained to stay coherent with that permutation â€” scored by one chance-corrected composite, on entire held-out calendar years, with every variance-bearing input column (the RMS pair, the sigmas, the point counts and the mean-of-|B| scalar) removed so the answer cannot be read off the inputs. No prior work poses that combination, and the discrete formulation is what makes the ranking and the coherence constraint scoreable at all.
> Evaluation
> Every case carries three coupled targets, and the score is a weighted mean of three components,
> each averaged over the test cases:
> Score = 0.36 * BurstScore + 0.34 * RankScore + 0.30 * CertificateScore
> BurstScore â€” how many discontinuities did each hour contain? burst_word has one character
> per hour, in chronological order, giving the tier (A lowest â€¦ E highest) of that hour's hidden
> directional-discontinuity count. Credit per character is 1.0 for the exact tier, 0.5 for
> off-by-one and 0 otherwise, so a near-miss still earns something. The mean character credit is
> then chance-corrected against 0.38. That constant is not the uniform-random rate: because the
> tiers are quintiles, a constant word scores 1.0 on one tier and 0.5 on its two neighbours, so
> it earns (1 + 0.5 + 0.5) / 5 = 0.40 credit against a perfectly uniform tier distribution, and
> 0.407 measured on the actual training distribution. 0.38 sits just below that on purpose, so a
> schema-valid placeholder submission registers the small non-zero score the platform currently
> requires instead of exactly zero â€” a submission that ignores the data still scores essentially
> nothing here however cleverly its constant word is chosen. A 25% share of the component is
> reserved for getting the whole twelve-character word exactly right.
> RankScore â€” which hours were the most turbulent? turbulence_order ranks the twelve hours by
> their hidden sub-hour magnetic fluctuation amplitude, most turbulent first. It is scored by
> Kendall tau against the hidden ranking. The tau is averaged over cases before being floored at
> zero: a random ranking has mean tau 0, so guessing lands on exactly 0 with no dead band and no way
> to farm a floor out of windows that happen to come out concordant. 20% of the component is
> reserved for the exact permutation.
> CertificateScore â€” how did the window behave overall? regime_certificate carries three
> tokens: peak (which hour holds the largest hidden fluctuation amplitude), level (tier of the
> window's mean fluctuation amplitude) and alfven (tier of the window's AlfvÃ©nicity, the
> correlation between the minute-scale velocity and field fluctuations). Token accuracy is
> chance-corrected against 0.16. That is below the naive 1/5 = 0.20 because only two of the three
> tokens are five-way tier choices: peak names one of the twelve hours, so its chance rate is
> 1/12. Averaging the three per-token rates gives (1/12 + 1/5 + 1/5) / 3 = 0.161, which rounds to
> the published 0.16 â€” the same reasoning as BURST_BASE, where 0.38 sits just below the 0.40
> a constant word earns against uniform tiers. A certificate whose three tokens are all guessed
> therefore scores zero on this component. 35% of the component is reserved for all three tokens
> being right. A certificate is coherent only when its peak token names the hour your own
> turbulence_order puts first; an incoherent certificate keeps only a quarter of its score, so the
> three outputs have to agree with each other.
> The tier cut-points are quintiles of the training distribution and are published verbatim in
> tier_definitions.json, so the targets are fully determined â€” no guessing at thresholds.
> A perfect submission scores exactly 1.0.
> Runnable reference scorer â€” this is exactly how submissions are graded:
> import re
> import pandas as pd
> REQUIRED = ["case_id", "burst_word", "turbulence_order", "regime_certificate"]
> HOURS, TIER_SYMBOLS = 12, "ABCDE"
> W_BURST, W_RANK, W_CERT = 0.36, 0.34, 0.30
> BURST_BASE, TOKEN_BASE, INCOHERENT = 0.38, 0.16, 0.25
> BURST_RE = re.compile(r"^[A-E]{12}$")
> ORDER_RE = re.compile(r"^h(?:[1-9]|1[0-2])(?:>h(?:[1-9]|1[0-2])){11}$")
> CERT_RE = re.compile(r"^peak:h(\d{1,2})>level:l([0-4])>alfven:a([0-4])$")
> def _burst(v):
> t = str(v).strip().replace(" ", "").upper()
> return t if BURST_RE.match(t) else None
> def _order(v):
> t = str(v).strip().replace(" ", "").lower()
> if not ORDER_RE.match(t):
> return None
> hs = [int(x[1:]) - 1 for x in t.split(">")]
> return hs if len(set(hs)) == HOURS else None
> def _cert(v):
> t = str(v).strip().replace(" ", "").lower()
> m = CERT_RE.match(t)
> if not m:
> return None
> peak = int(m.group(1)) - 1
> return None if not 0 <= peak < HOURS else (peak, int(m.group(2)), int(m.group(3)))
> def _ranks(order):
> r = [0] * HOURS
> for pos, h in enumerate(order):
> r[h] = pos
> return r
> def _tau(a, b):
> c = d = 0
> for i in range(len(a)):
> for j in range(i + 1, len(a)):
> s = (a[i] - a[j]) * (b[i] - b[j])
> c += s > 0
> d += s < 0
> return (c - d) / (c + d) if (c + d) else 0.0
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> missing = [c for c in REQUIRED if c not in submission.columns]
> if missing:
> raise ValueError(f"Submission is missing required columns: {missing}")
> sub, ans = submission[REQUIRED].copy(), answers[REQUIRED].copy()
> sub["case_id"] = sub["case_id"].astype(str).str.strip()
> ans["case_id"] = ans["case_id"].astype(str).str.strip()
> if sub["case_id"].duplicated().any():
> raise ValueError("Duplicate case_id values are not allowed in the submission")
> if len(sub) != len(ans):
> raise ValueError(f"Submission has {len(sub)} rows, expected {len(ans)}")
> sub = sub.sort_values("case_id").reset_index(drop=True)
> ans = ans.sort_values("case_id").reset_index(drop=True)
> if not sub["case_id"].equals(ans["case_id"]):
> raise ValueError("Submission case_id values must match the expected ids exactly")
> n = len(ans)
> b_exact = b_credit = r_exact = r_tau = c_exact = c_token = 0.0
> for i in range(n):
> tb, to, tc = (_burst(ans.at[i, "burst_word"]), _order(ans.at[i, "turbulence_order"]),
> _cert(ans.at[i, "regime_certificate"]))
> pb, po, pc = (_burst(sub.at[i, "burst_word"]), _order(sub.at[i, "turbulence_order"]),
> _cert(sub.at[i, "regime_certificate"]))
> if pb is not None:
> d = [abs(TIER_SYMBOLS.index(p) - TIER_SYMBOLS.index(t)) for p, t in zip(pb, tb)]
> b_credit += sum(1.0 if x == 0 else (0.5 if x == 1 else 0.0) for x in d) / HOURS
> b_exact += pb == tb
> if po is not None:
> r_tau += _tau(_ranks(po), _ranks(to))
> r_exact += po == to
> if pc is not None:
> w = 1.0 if (po is not None and po[0] == pc[0]) else INCOHERENT
> c_token += w * sum(p == t for p, t in zip(pc, tc)) / 3.0
> c_exact += w * (pc == tc)
> burst = 0.25 * (b_exact / n) + 0.75 * max(0.0, (b_credit / n - BURST_BASE) / (1 - BURST_BASE))
> rank = 0.20 * (r_exact / n) + 0.80 * max(0.0, r_tau / n)
> cert = 0.35 * (c_exact / n) + 0.65 * max(0.0, (c_token / n - TOKEN_BASE) / (1 - TOKEN_BASE))
> return float(min(1.0, max(0.0, W_BURST * burst + W_RANK * rank + W_CERT * cert)))
> Structural problems with the file â€” missing columns, duplicate, missing or unknown case_id
> values, the wrong number of rows â€” raise a ValueError and the submission is rejected. A
> malformed value inside an otherwise valid row is not fatal: that row scores 0 on the component
> it broke and everything else still scores. Surrounding whitespace and wrong letter case are
> forgiven.
> Dataset
> Files in public/:
> **train.csv** â€” 20,756 labelled windows; the index columns followed by the three targets.
> **test.csv** â€” 886 held-out windows; the index columns only.
> **sample_submission.csv** â€” submission template carrying placeholder targets.
> **train_signals.npz** â€” the published hourly-mean tensor for the training windows.
> **test_signals.npz** â€” the published hourly-mean tensor for the test windows.
> **tensor_schema.json** â€” tensor shapes, axis meanings, channel names and units.
> **tier_definitions.json** â€” the published quintile cut-points for the three tiered quantities.
> Index columns, present in both train.csv and test.csv:
> **case_id** (string) â€” opaque window identifier, e.g. sw_3f9c1a2b7d4e5061a2. Used only to
> align your predictions with the hidden rows; it encodes nothing about the window.
> **signal_row** (int) â€” row index into the first axis of the matching NPZ file.
> Target columns, present in train.csv only:
> **burst_word** (string) â€” twelve characters from ABCDE, one per hour h1â€¦h12 in
> chronological order, giving the tier of that hour's hidden directional-discontinuity count.
> Example CEBBADDCCEEB.
> **turbulence_order** (string) â€” the twelve hours ranked by hidden sub-hour fluctuation
> amplitude, most turbulent first, joined by >. Example
> h5>h4>h6>h3>h7>h2>h8>h1>h9>h12>h10>h11.
> **regime_certificate** (string) â€” three >-separated tokens. Example
> peak:h5>level:l3>alfven:a4.
> Tensor contents (train_signals.npz, test_signals.npz):
> The twelve channels, in order:
> index 0 â€” Bx_gsm_mean (Bx)
> index 1 â€” By_gsm_mean (By)
> index 2 â€” Bz_gsm_mean (Bz)
> index 3 â€” Vx_gse_mean (Vx)
> index 4 â€” Vy_gse_mean (Vy)
> index 5 â€” Vz_gse_mean (Vz)
> index 6 â€” flow_speed_mean (speed)
> index 7 â€” proton_density_mean (density)
> index 8 â€” log10_temperature_mean (temperature)
> index 9 â€” flow_pressure_mean (flow pressure)
> index 10 â€” log10_plasma_beta_mean (plasma beta)
> index 11 â€” alfven_mach_mean (AlfvÃ©n Mach number)
> That is twelve channels â€” Bx, By, Bz, Vx, Vy, Vz, speed, density, temperature, flow pressure,
> plasma beta and AlfvÃ©n Mach number â€” matching axis 2 of hourly_means and the channels list in
> tensor_schema.json, which carries the same names in the same order. Units and full descriptions:
> | # | Channel | Unit | Meaning |
> |---:|---|---|---|
> | 0 | Bx_gsm_mean | nT | hourly mean of the field vector's x component |
> | 1 | By_gsm_mean | nT | hourly mean of the field vector's y component, GSM |
> | 2 | Bz_gsm_mean | nT | hourly mean of the field vector's z component, GSM |
> | 3 | Vx_gse_mean | km/s | hourly mean of the flow velocity's x component, GSE |
> | 4 | Vy_gse_mean | km/s | hourly mean of the flow velocity's y component, GSE |
> | 5 | Vz_gse_mean | km/s | hourly mean of the flow velocity's z component, GSE |
> | 6 | flow_speed_mean | km/s | hourly mean bulk speed |
> | 7 | proton_density_mean | n/cc | hourly mean proton density |
> | 8 | log10_temperature_mean | logâ‚â‚€ K | hourly mean of logâ‚â‚€ proton temperature |
> | 9 | flow_pressure_mean | nPa | hourly mean dynamic pressure |
> | 10 | log10_plasma_beta_mean | logâ‚â‚€ | hourly mean of logâ‚â‚€ plasma beta |
> | 11 | alfven_mach_mean | â€” | hourly mean AlfvÃ©n Mach number |
> Every value is a mean over the valid minutes of that hour. There are no standard deviations, no
> RMS columns, no point counts, no mean-of-|B| scalar, no timestamps, no day-of-year, and no
> spacecraft identifiers anywhere in the published files. Values are finite. Hours are kept only
> where coverage is good enough for the hourly means and the hidden statistics to be trustworthy.
> Total size of public/ is about 6.5 MB.
> Submission
> Write a CSV with exactly one row for every case_id in test.csv â€” 886 rows plus a header â€”
> and exactly these four columns in this order:
> case_id,burst_word,turbulence_order,regime_certificate
> Example:
> case_id,burst_word,turbulence_order,regime_certificate
> sw_3f9c1a2b7d4e5061a2,CEBBADDCCEEB,h5>h4>h6>h3>h7>h2>h8>h1>h9>h12>h10>h11,peak:h5>level:l3>alfven:a4
> sw_71d0e4c8ab29f3d5c6,AABCCDDEEEDC,h1>h2>h3>h9>h8>h7>h6>h5>h4>h10>h11>h12,peak:h1>level:l1>alfven:a0
> Requirements:
> Every case_id from test.csv present exactly once. Duplicate, missing or unknown ids are
> rejected with an error.
> burst_word: exactly twelve characters, each one of A B C D E.
> turbulence_order: exactly the twelve tokens h1â€¦h12, each once, joined by >.
> regime_certificate: exactly peak:h<1-12>>level:l<0-4>>alfven:a<0-4>.
> Row order does not matter. Extra columns are ignored.
> File format: .csv only.
> sample_submission.csv is a correctly formatted template carrying placeholder values only.
> Allowed
> Any model you train yourself inside your submission script: gradient-boosted trees, linear and
> kernel models, multilayer perceptrons, convolutional or recurrent networks over the twelve-hour
> sequence, set or sequence transformers over the hours, ensembles of any of these.
> Any feature engineering on top of the published tensors: field magnitude, clock and cone angles,
> hour-to-hour differences and rotation angles, derived plasma quantities, window-level summaries,
> normalisation per window or per regime.
> Multi-task training across the three targets, and decoding that enforces coherence between them.
> Cross-validation, hyperparameter search and model selection â€” all of it on the supplied training
> rows only.
> Test-time augmentation and calibration that would work identically on a single unseen window in
> production.
> Not Allowed
> Rule-based or purely algorithmic solutions. A hand-written threshold rule, a fitted
> per-window analytic model, a lookup table, or any pipeline in which no model is actually trained
> does not count as a solution however well it scores. The point of this challenge is a learned
> mapping from hourly regime to minute-scale structure.
> Recovering the answer from the source archive. The hidden targets are properties of the OMNI
> 1-minute record. Do not attempt to identify a window's date and read the minute-scale data out
> of OMNI, OMNIWeb, CDAWeb, SPDF, ACE/Wind/Geotail instrument archives, or any mirror, index or
> locally embedded copy of them. Matching the published hourly means against a re-derived hourly
> series to recover timestamps is the same prohibited move. There is no internet access at solve
> time and external datasets are not permitted, so the only legitimate source of an answer is a
> model trained on the supplied training rows.
> Hard-coded answers. No embedded per-window answer maps, no answer dictionaries keyed on
> case_id or signal_row, no offline-computed constants standing in for a model's output. If you
> found a real pattern, train a model to find and use it.
> Using metadata as a predictor. Do not derive predictions from case_id, signal_row, row
> order, file sizes, byte hashes, archive order, or any other artefact of how the files were
> produced.
> Using the test set for anything beyond single-window inference. No pseudo-labelling, no
> test-time training, no reweighting training data using the test rows, no calibrating against the
> test set's overall distribution.
> Pretrained weights and external data. This is a From-Scratch challenge: train on the supplied
> training rows alone. No pretrained time-series or space-weather models, no external solar-wind
> catalogues, no reanalysis products, no geomagnetic index series beyond what is published here.
> Hosted or closed-model APIs, at training or inference time.
> Exploiting the grader. No duplicate ids, extra columns, malformed values, parser limits or any
> other attempt to game grading behaviour rather than predict the targets.
> Hardware & Compute
> Target hardware: CPU only. 10 CPU cores, 62 GB RAM. No GPU is available. Nothing in your
> solution may assume CUDA, a GPU-only library path, or GPU-scale batch sizes.
> Time budget: the full end-to-end run â€” data preparation, training and inference â€” must
> complete in under 1.5 hours on that hardware. Build a safeguard into your script that stops
> training and starts writing the submission when you reach the last five to ten minutes, so you
> always produce a file.
> Libraries: only what is already installed in the Kaggle Python Docker image (numpy, pandas,
> scipy, scikit-learn, xgboost, LightGBM, PyTorch CPU, TensorFlow CPU, and so on). No pip installs,
> no external dependencies of any kind.
> Internet: there is no internet access at solve time at all â€” no package downloads, no
> model-weight downloads, no hosted LLM or other API calls. This challenge needs no base model, so
> nothing is bundled beyond the dataset itself.
> Your choice of features and method is entirely your own, scoped to those preinstalled libraries.
> The whole dataset is a few megabytes and loads into memory as float32 in under a second, so a
> compact model trains many times over inside the budget on ten cores.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## GFAP Spatial Moment Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dr7p7mvs6xxv5jy02aw5vas8bzn3p
- DOMAIN exactly as displayed: From Scratch
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
> GFAP Spatial Moment Reconstruction is a hard, from-scratch CPU computer-vision challenge.
> For every microscopy field and published spatial program, predict four cellular burden measurements inside each of sixteen terminal territories.
> Each sample contains:
> One processed GFAP-stained microscopy image.
> One image-specific hierarchical territory program.
> Sixteen terminal territories.
> Four target burden channels per terminal territory.
> Sixty-four numeric values to predict.
> There are no candidate answer panels.
> The model must reconstruct the spatial measurements directly from the image.
> The four target channels are:
> Cell count.
> Cell-footprint burden.
> Cell-elongation burden.
> Cell-contrast burden.
> The same microscopy field appears under four different territory programs. The image stays the same while the spatial question changes.
> A successful model must therefore learn a reusable visual representation of the field and integrate that evidence over new hierarchical regions.
> Prediction Target
> Every sample has sixteen terminal territories.
> For each terminal territory, predict:
> count
> footprint
> elongation
> contrast
> This produces:
> 16 Ã— 4 = 64
> non-negative outputs per sample.
> The terminal territories exactly partition the released image.
> A cell contributes to exactly one terminal territory according to the center of its source annotation box after image transformation.
> Training rows provide the true 16 Ã— 4 target matrix.
> Test rows omit it.
> Why This Is Harder Than Cell Counting
> The challenge does not ask only for the total number of labeled cells.
> The same field is queried through four different spatial programs.
> A model must determine:
> Where the cells are.
> How their burden is distributed.
> How large their source boxes are.
> How elongated their source boxes are.
> How their local staining differs from the field background.
> Which side of each changing hierarchy boundary their centers occupy.
> A prediction can have the correct global total and still be wrong because burden was allocated to the wrong territories.
> Likewise, a model can place counts correctly while failing on morphology or stain-related burden.
> The evaluation reconstructs the complete 31-node hierarchy from the sixteen terminal predictions and scores errors at multiple spatial scales.
> Source Data
> The source dataset contains GFAP-stained rat brain microscopy fields with manually annotated cell bounding boxes.
> Source properties include:
> 1,200 microscopy images.
> Approximately 15,000 annotated cells.
> 8-bit TIF images.
> Original dimensions of approximately 990 Ã— 708 pixels.
> One annotation text file per image.
> One object category: Cell.
> CC0 licensing.
> The source bounding boxes are used during challenge preparation to construct training targets.
> Participants do not receive the original annotation files in the challenge package.
> Released Images
> Each source field is converted to grayscale, robustly normalized, and letterboxed to:
> 384 Ã— 288
> The image content is preserved without geometric cropping.
> Training and test fields are disjoint.
> A released field may be referenced by four rows because every field is evaluated under four different spatial programs.
> Spatial Programs
> Each program is a depth-four binary rectangle hierarchy.
> The program contains:
> 31 total nodes.
> 15 internal nodes.
> 16 terminal territories.
> Node order follows binary-heap order.
> Node 1 is the complete field.
> Nodes 2 and 3 are its children.
> The hierarchy continues until Nodes 16 through 31, which are the terminal territories.
> Every internal node is divided into exactly two rectangular children.
> The children:
> Do not overlap.
> Leave no gap.
> Exactly cover their parent.
> Share one horizontal or vertical boundary.
> Programs vary in:
> Split orientation.
> Boundary position.
> Territory width.
> Territory height.
> Aspect ratio.
> Branch geometry.
> Depth-specific subdivision pattern.
> The complete geometry is public.
> Coordinate Convention
> Coordinates use the released 384 Ã— 288 image coordinate system.
> The upper-left corner is:
> (0, 0)
> x increases from left to right.
> y increases from top to bottom.
> Rectangles are half-open:
> x_min <= x < x_max
> y_min <= y < y_max
> A center lying exactly on a shared boundary therefore belongs to only one child.
> Target Channels
> The source annotation boxes are transformed into released-image coordinates.
> Let:
> w be the transformed annotation-box width.
> h be the transformed annotation-box height.
> m_cell be mean released-image intensity inside the transformed box.
> m_field be the median non-zero intensity of the released field.
> Each annotated cell contributes four non-negative values.
> Count
> Every cell contributes:
> count = 1
> Footprint
> Every cell contributes:
> footprint = sqrt(w Ã— h) / 24
> This is a scale-sensitive burden derived from the annotation-box footprint.
> Elongation
> Every cell contributes:
> elongation = 1 + min(abs(log((w + 1) / (h + 1))), 1.5)
> Nearly square boxes remain close to 1.
> More anisotropic boxes contribute more.
> Contrast
> Every cell contributes:
> contrast = 0.5 + min(abs(m_cell - m_field) / 96, 1.5)
> This measures how strongly the annotated cell region differs from the field's typical non-zero intensity.
> Territory Aggregation
> A cell is assigned to one terminal territory using its transformed annotation-box center.
> Its four channel values are added to that territory.
> For terminal territory t:
> target[t, channel] = sum of that channel over cells centered inside t
> This produces the released training target:
> target_leaf_moments
> with shape:
> 16 Ã— 4
> The four channel columns always appear in this order:
> count
> footprint
> elongation
> contrast
> Hierarchical Structure
> Only the sixteen terminal values are predicted directly.
> The evaluator reconstructs internal-node values by addition.
> For any channel:
> parent = left_child + right_child
> This means one terminal mistake also affects every ancestor containing that territory.
> The metric therefore measures both:
> Fine local accuracy.
> Coarse regional accuracy.
> Correct global totals alone are insufficient.
> Repeated Fields
> Every microscopy field is associated with exactly four spatial programs.
> The four rows share:
> The same field image.
> The same underlying annotated cells.
> The same field-level morphology.
> They differ in:
> Territory boundaries.
> Hierarchical geometry.
> Terminal allocations.
> All rows sharing one field_id must remain in the same local validation partition.
> Random row-level splitting is invalid because it exposes the same microscopy image on both sides of the split.
> Challenge Type
> This is a From Scratch neural computer-vision challenge.
> The primary predictive model must be trainable and initialized without pretrained weights.
> Eligible architectures include:
> Compact convolutional encoders.
> Small residual CNNs.
> Depthwise-separable CNNs.
> Patch-based image encoders.
> Small vision transformers trained entirely from scratch.
> Region-aware neural networks.
> Coordinate-conditioned pooling networks.
> Cross-attention over image and territory tokens.
> Hierarchical regression networks.
> Comparable trainable systems using released training data only.
> The neural model must be the principal source of predictive performance.
> Compute
> The intended environment provides:
> 10 CPU cores.
> 62.5 GiB RAM.
> No GPU.
> The benchmark is designed for compact CPU-trainable systems.
> Released Dataset
> The public package contains:
> images/
> train/
> test/
> train.jsonl
> test.jsonl
> moment_schema.json
> sample_submission.csv
> There is no separate validation file.
> images/train/
> Contains the processed microscopy fields referenced by training samples.
> One image is referenced by four rows.
> images/test/
> Contains the processed test fields.
> Training and test fields are disjoint.
> train.jsonl
> Each line contains one JSON object.
> sample_id
> Type: string.
> Unique identifier for one field-program sample.
> Use it only for alignment.
> Do not use it as a predictive feature.
> field_id
> Type: string.
> Groups the four spatial programs derived from one microscopy field.
> Use it for grouped validation and optional feature caching.
> Do not use the identifier itself as a predictive feature.
> image_file
> Type: string.
> Relative path to the released PNG.
> image_width
> Type: integer.
> Always:
> 384
> image_height
> Type: integer.
> Always:
> 288
> program_nodes
> Type: list of 31 objects.
> Each object contains:
> node_id
> parent_id
> depth
> x_min
> y_min
> x_max
> y_max
> children
> Nodes appear in binary-heap order.
> Nodes 16 through 31 are the sixteen terminal territories.
> channel_names
> Type: list of four strings.
> Always:
> count
> footprint
> elongation
> contrast
> ### target_leaf_moments
> Training only.
> Type: list of sixteen lists.
> Each terminal list contains four finite non-negative values in `channel_names` order.
> Shape:
> `16 Ã— 4`
> ## test.jsonl
> Contains the same public input fields as training except:
> `target_leaf_moments`
> is omitted.
> The test set does not expose:
> - Source annotation files.
> - Source bounding boxes.
> - Cell centers.
> - Per-cell morphology targets.
> - Original numeric filenames.
> - Hidden test moment values.
> ## moment_schema.json
> Defines:
> - Image dimensions.
> - Tree depth.
> - Node count.
> - Terminal count.
> - Programs per field.
> - Channel order.
> - Channel formulas.
> - Node order.
> - Coordinate convention.
> - Target shape.
> - Submission columns.
> - Field-grouping rule.
> # Submission Format
> Submit one row for every test sample.
> The first column is:
> `sample_id`
> The remaining 64 columns correspond to the sixteen terminal territories and four channels.
> For each terminal territory the columns are:
> leaf_01_count
> leaf_01_footprint
> leaf_01_elongation
> leaf_01_contrast
> then the same four channels for `leaf_02`, continuing through `leaf_16`.
> The complete submission therefore contains:
> `1 + 16 Ã— 4 = 65 columns`
> All values must be:
> - Numeric.
> - Finite.
> - Non-negative.
> Values do not need to be integers.
> `sample_submission.csv` provides the exact required order.
> Invalid submissions include:
> - Missing samples.
> - Extra samples.
> - Duplicate `sample_id` values.
> - Missing columns.
> - Extra columns.
> - Incorrect column order.
> - Non-numeric values.
> - Negative values.
> - NaN.
> - Positive infinity.
> - Negative infinity.
> # Evaluation
> Submissions are evaluated using the **Spatial Moment Reconstruction Score** from 0.01 to 100.
> Higher is better.
> A perfect submission receives 100.
> The metric first scores each of the four channels separately, then combines them into one sample score.
> ## Reconstructing the Hierarchy
> For each channel, the sixteen submitted terminal values become Nodes 16 through 31.
> Internal nodes are reconstructed bottom-up using:
> `parent = left_child + right_child`
> This produces a complete 31-node predicted hierarchy.
> The same operation is applied to the hidden truth.
> ## Root Similarity
> The root represents the complete-field total for that channel.
> Define:
> `root_error = abs(predicted_root - true_root) / (true_root + 1)`
> Then:
> `RootSimilarity = exp(-2 Ã— root_error)`
> ## Multiscale Tree Similarity
> Each node receives a depth weight:
> - Depth 0: 0.20
> - Depth 1: 0.35
> - Depth 2: 0.50
> - Depth 3: 0.75
> - Depth 4: 1.00
> Deeper territories therefore receive greater weight.
> For a channel, define:
> `floor = 0.35 Ã— true_root / 16 + 0.25`
> For every node:
> `relative_error_node = abs(predicted_node - true_node) / (true_node + floor)`
> The weighted arithmetic mean of these 31 relative errors is:
> `TreeError`
> Then:
> `TreeSimilarity = exp(-1.75 Ã— TreeError)`
> ## Terminal Distribution Similarity
> For one channel, normalize the sixteen predicted terminal values by their predicted sum.
> Normalize the sixteen true terminal values by their true sum.
> Let the resulting distributions be p and q.
> Their total-variation distance is:
> `TV = 0.5 Ã— sum(abs(p - q))`
> Then:
> `DistributionSimilarity = 1 - TV`
> If both totals are zero, this component is defined as 1.
> If exactly one total is zero, it is defined as 0.
> ## Channel Score
> For each channel:
> `ChannelScore = 0.20 Ã— RootSimilarity + 0.50 Ã— TreeSimilarity + 0.30 Ã— DistributionSimilarity`
> Each channel score lies in `[0, 1]`.
> ## Sample Score
> Let the four channel scores be:
> - C_count
> - C_footprint
> - C_elongation
> - C_contrast
> The sample score is their geometric mean:
> `SampleScore = (C_count Ã— C_footprint Ã— C_elongation Ã— C_contrast)^(1/4)`
> The geometric mean prevents excellent performance on one easy channel from hiding failure on another.
> ## Dataset Aggregation
> Let:
> `MeanScore = mean(SampleScore)`
> Let:
> `Q25 = 25th percentile of SampleScore`
> For each test field, take the minimum SampleScore across its four spatial programs.
> Then:
> `WeakestProgramScore = mean(field minimum scores)`
> Define:
> `Core = (MeanScore Ã— Q25 Ã— WeakestProgramScore)^(1/3)`
> Finally:
> `Spatial Moment Reconstruction Score = 100 Ã— Core^2.20`
> The result is clipped to:
> `[0.01, 100]`
> There are no hidden subsets or hidden metric weights.
> The lower-quartile and weakest-program terms prevent a model from achieving a high score by solving only favorable fields or one preferred territory layout.
> # Local Metric Reproduction
> To reproduce the official score:
> 1. Group local validation by `field_id`.
> 2. Read the sixteen predicted terminal vectors.
> 3. Reconstruct all 31 hierarchy nodes by addition.
> 4. Calculate Root Similarity for each channel.
> 5. Calculate weighted Tree Similarity for each channel.
> 6. Calculate Terminal Distribution Similarity.
> 7. Combine them into four Channel Scores.
> 8. Take their geometric mean to obtain SampleScore.
> 9. Calculate MeanScore.
> 10. Calculate the 25th percentile.
> 11. Calculate the minimum program score for every field.
> 12. Average those field minima.
> 13. Apply the published final formula.
> # Intended Modeling Approaches
> A useful system should learn an image representation that supports region-conditioned measurement.
> ## Shared Image Encoder
> Encode the complete microscopy field once.
> CPU-friendly options include:
> - Compact CNNs.
> - Small residual networks.
> - Depthwise-separable CNNs.
> - Lightweight patch encoders.
> - Small vision transformers trained from random initialization.
> Because one image appears under four programs, its visual feature map can be reused.
> ## Territory Pooling
> Use the public rectangle coordinates to pool visual features for the sixteen terminal territories.
> Possible methods include:
> - ROI pooling.
> - Average pooling over feature-map rectangles.
> - Coordinate-aware attention.
> - Region tokens.
> - Multi-resolution pooling.
> The model can then predict four moment channels for every terminal.
> ## Hierarchical Modeling
> The 31-node hierarchy provides useful structure even though only terminals are submitted.
> A training model may reconstruct parent nodes and use auxiliary losses at multiple depths.
> This can encourage both:
> - Fine terminal accuracy.
> - Coarse branch consistency.
> ## Multi-Channel Heads
> The four targets measure related but different properties.
> A model may use:
> - One shared encoder with four output heads.
> - Shared terminal embeddings followed by channel-specific regressors.
> - Joint positive-output heads.
> - Auxiliary count supervision.
> - Cross-channel consistency losses.
> ## Repeated-Field Training
> All four programs from one field can share one encoded visual feature map.
> This reduces CPU cost and encourages the model to learn reusable spatial evidence rather than memorize one partition.
> # Practical CPU Baseline
> A practical baseline may:
> 1. Load a 384 Ã— 288 field.
> 2. Encode it using a compact CNN initialized from scratch.
> 3. Keep a spatial feature map rather than only a global embedding.
> 4. Pool features for all sixteen terminal rectangles.
> 5. Append normalized rectangle geometry.
> 6. Predict four non-negative values for every terminal.
> 7. Reconstruct internal-node predictions during training.
> 8. Optimize terminal and hierarchical regression losses.
> 9. Cache or reuse one field encoding across its four programs.
> 10. Validate using a grouped `field_id` split.
> A stronger model may combine:
> - Multi-scale feature maps.
> - Region-aware attention.
> - Explicit hierarchy tokens.
> - Multi-depth auxiliary losses.
> - Program-conditioned cross-attention.
> - Field-grouped minibatches.
> - Eligible ensembles of independently initialized models.
> # From-Scratch Requirements
> All trainable predictive parameters must begin from random initialization.
> A valid primary solution must include a trainable neural image model optimized using the released training examples.
> Allowed resources include:
> - Released challenge files.
> - Public neural architecture source code without pretrained weights.
> - Standard numerical libraries.
> - Standard image-processing libraries.
> - Standard deep-learning frameworks.
> - Standard augmentation libraries.
> - Fixed coordinate calculations.
> - Auxiliary targets derived only from released training labels.
> - Minor handcrafted features fused into the learned model.
> # Disallowed Methods
> The following are prohibited as primary predictors:
> - Pretrained image encoders.
> - Pretrained backbones.
> - Pretrained adapters.
> - Pretrained checkpoints.
> - External microscopy or biomedical image datasets.
> - External visual pretraining.
> - Foundation-model image features.
> - Teacher predictions from pretrained systems.
> - Manual test annotation.
> - External copies of source annotations.
> - External source-image matching.
> - Fixed thresholding as the primary predictor.
> - Hand-authored morphology pipelines as the primary predictor.
> - Connected-component enumeration as the primary predictor.
> - Nearest-neighbor retrieval as the primary predictor.
> - Classical regression or tree ensembles as the primary predictor.
> - Hard-coded use of `sample_id`, `field_id`, filenames, or row order.
> - Test-specific manual correction.
> - Hidden test-answer reconstruction.
> The learned neural system must be the principal source of predictive performance.
> # Validation and Leakage
> All four rows sharing one `field_id` reference the same microscopy image.
> They must remain together during local splitting.
> The same rule applies to:
> - Crops.
> - Resized copies.
> - Augmented copies.
> - Cached feature maps.
> - Region embeddings.
> - Derived auxiliary targets.
> - Pseudo-labeled variants.
> Random row-level splitting is invalid.
> Useful local reporting includes:
> - Unique field count.
> - Sample count.
> - Count-channel performance.
> - Footprint-channel performance.
> - Elongation-channel performance.
> - Contrast-channel performance.
> - Mean SampleScore.
> - Q25 SampleScore.
> - Weakest-program performance.
> - Final official score.
> # Scientific Context
> GFAP staining highlights astrocytic structures and related tissue patterns.
> The source images vary in:
> - Cell morphology.
> - Staining strength.
> - Tissue texture.
> - Cell density.
> - Object size.
> - Elongation.
> - Clustering.
> - Partial visibility.
> - Background intensity.
> - Scanning artifacts.
> - Preparation artifacts.
> The challenge uses annotation boxes to derive structured spatial measurements, but those source annotations are not released to participants.
> This is a machine-learning benchmark rather than a clinical instrument.
> # Limitations
> The source material is rat brain tissue rather than human tissue.
> The source annotation provides bounding boxes rather than segmentation masks.
> The four target channels are benchmark-specific summaries derived from those boxes and the released grayscale field.
> They do not represent:
> - Cell segmentation.
> - Cell subtype classification.
> - Three-dimensional morphology.
> - Clinical diagnosis.
> - Treatment response.
> - Exact biological cell area.
> A cell contributes to one terminal territory according to its annotation-box center even if its box crosses a territory boundary.
> Rectangular programs are structured abstractions and do not preserve every detail of the original cellular arrangement.
> Models should not be used directly for diagnosis, treatment, or medical decision-making.
> # Expected Outcome
> A successful system should:
> - Learn GFAP cellular visual evidence from scratch.
> - Estimate spatial cell burden without access to source annotations.
> - Recover count, footprint, elongation, and contrast burden.
> - Interpret changing hierarchical territory geometry.
> - Remain accurate at both coarse and fine spatial scales.
> - Transfer one field representation across four different programs.
> - Avoid concentrating performance only on easy fields or easy partition layouts.
> - Train efficiently in a CPU-only environment.
> The prediction objective is:
> **reconstruct a 16 Ã— 4 spatial moment field for every published microscopy territory program.**

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Local Formal Proof Spine Repair Challenge

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ewcqxh1js6a2ahk9yn544kx834xpk
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Background
> As formal mathematics libraries grow, maintaining and refactoring large-scale proof repositories becomes increasingly complex. The Lean 4 proof assistant's mathematical library (mathlib4) is a massive, actively maintained corpus of formalized mathematics. This challenge focuses on a highly specific task within this domain: Local Formal-Proof Spine Repair. It tests a system's ability to reconstruct a specific, missing tactic line within a formal proof based strictly on local context, rather than asking for unrestricted, open-ended theorem proving. This capability is crucial for tools designed for damaged-source repair, proof refactoring assistance, and tactic-pattern mining.
> Overview
> This is a From Scratch artifact-repair task. Participants are tasked with restoring exactly one missing tactic line in a real Lean theorem proof. Instead of generating a full proof, your model must act as a contextual repair tool.
> Given a bounded, tactic-bearing proof block where a single line has been replaced with a <GAP> token, you must predict:
> The exact source line removed (missing_text).
> The local reference tokens used in that line (references).
> The leading tactic spine (spine).
> This benchmark evaluates exact-source artifact recoveryâ€”meaning a semantically valid alternative that closes the proof goal but does not match the original human-written syntax will receive partial rather than full credit.
> Dataset Information
> The dataset is derived directly from the official mathlib4-master.zip source archive. The preparation script processes .lean files exclusively from the Mathlib/ directory, identifying named theorem and lemma blocks that use := by proofs. Declaration names are uniformly rewritten to TARGET to prevent data leakage, and specific archive paths, authors, and source coordinates are stripped out. To minimize neighboring-theorem leakage, the data is split based on whole two-level module families before any gaps are sampled.
> The public data distribution includes the following files:
> train.csv: The training set containing the masked context and the ground truth answer_json.
> test.csv: The evaluation set containing only the masked inputs.
> sample_submission.csv: A template demonstrating the required submission format.
> task_metadata.json: Basic metadata about the task, row counts, and target descriptions.
> Dataset Schema
> The input files are provided in CSV format. The following ASCII table details the columns provided:
> Plaintext
> +--------------------+--------+----------------------------------------------------------------+
> | Column Name        | Type   | Description                                                    |
> +--------------------+--------+----------------------------------------------------------------+
> | id                 | string | Unique hashed identifier for the specific proof gap.           |
> | declaration_kind   | string | The type of Lean declaration (e.g., 'theorem' or 'lemma').     |
> | statement_text     | string | The theorem statement, with the declaration renamed to TARGET. |
> | local_context_text | string | Nearby binder/open context (up to the last 25 lines/5000 char).|
> | proof_with_gap     | string | The proof block containing exactly one <GAP> token.            |
> | gap_token_count    | string | The exact number of tokens in the missing human-written line.  |
> | answer_json        | string | Ground truth JSON (present ONLY in train.csv).                 |
> +--------------------+--------+----------------------------------------------------------------+
> Evaluation Metrics
> The challenge uses a composite scoring system to evaluate the precise recovery of the missing artifact. Predictions are parsed from JSON strings and scored per-row based on the following weighted formula:
> 0.45 * Character Edit Similarity: Normalized edit similarity between the predicted and actual missing text.
> 0.20 * Missing-Token F1: F1 score of the whitespace-separated tokens in the missing text.
> 0.15 * Reference F1: F1 score of the local reference tokens used.
> 0.10 * Spine F1: F1 score of the leading tactic spine.
> 0.05 * Exact Bundle: Binary score (1.0 or 0.0) awarded only if the entire JSON prediction exactly matches the ground truth.
> 0.05 * Confidence Calibration: Calculated as 1 - abs(confidence - edit_similarity). Requires the model to accurately estimate its own performance.
> Final Score Calculation:
> The overall leaderboard score is calculated as: 0.90 * (Mean of all row scores) + 0.10 * (Mean of the worst-performing hidden tactic group). An exact oracle prediction scores 1.0.
> Sample Submission Format
> Submissions must be a CSV file containing exactly three columns: id, prediction_json, and confidence.
> prediction_json must be a valid JSON string containing exactly three keys: missing_text (string), references (list of unique strings), and spine (list of unique strings).
> confidence must be a finite float between 0.0 and 1.0.
> Example Submission Row:
> Code snippet
> id,prediction_json,confidence
> p_1a2b3c4d5e6f7g8h,"{""missing_text"":""simpa using h"",""references"":[""h""],""spine"":[""simpa""]}",0.85
> What Not to Use / Strict Constraints
> To maintain the integrity of this "From Scratch" recovery task, the following approaches and resources are strictly prohibited:
> Pretrained code or language models (LLMs).
> External theorem-library checkouts or theorem-search datasets.
> Source-text search mechanisms.
> Web access or external APIs.
> Source-path or original declaration name recovery attempts.
> Test labels or evaluation adaptation.
> GPUs. (The full offline run must fit within 90 minutes, utilizing a maximum of 10 CPU cores and 62 GB RAM).
> Learned components, parsers, and models written by you are permitted, provided their parameters and vocabularies are derived exclusively from the provided public training files.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Operon Reassembly in an Unread Genome

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx77jr76b47eatg40dqmx5ns0n8c10gj
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Operon Reassembly in an Unread Genome
> Overview
> Bacteria and archaea pack functionally related genes into operons: short runs of
> genes sitting shoulder to shoulder on the same strand, transcribed together as one
> message. The order of the genes inside an operon is not arbitrary. The same operon
> turns up in genome after genome with its genes in the same sequence, because that
> order is part of how the machine works â€” a permease before its ATP-binding partner, a
> sensor beside its response regulator. Read enough genomes and the arrangement becomes
> predictable from the proteins alone.
> Each case here is one real four-gene operon lifted out of an anonymous genome. Its
> four proteins are handed to you shuffled, as slots q1â€“q4, stripped of names,
> coordinates, strands and any hint of which came first. Alongside them you get
> RNA-level evidence about the genome that produced them â€” its complete transfer-RNA
> gene complement and its 16S ribosomal RNA gene â€” and nothing else. Not one of that
> genome's coding sequences is ever shown to you.
> Two things have to be put back:
> The arrangement. Which order were these four genes transcribed in?
> The DNA. Write out the coding sequence this genome actually uses for each of the
> four proteins.
> The second half is a dialect problem. The genetic code is redundant â€” eighteen of the
> twenty amino acids have two to six synonymous codons â€” and every genome has a habitual
> way of choosing among them, shaped by its mutational background and by the make-up of
> its tRNA pool. One genome writes leucine CTG almost every time; another writes the
> same leucine TTA. With no coding sequence from the hidden genome available, that
> habit cannot be counted. It has to be predicted from the tRNA repertoire, from the
> ribosomal marker that places the genome phylogenetically, and from the proteins.
> The hidden genomes are drawn from taxonomic orders that appear nowhere in the
> training data, so the nearest training relative is genuinely distant.
> Neither half is close to solved. A codon table can be recovered well enough to get a
> useful score fairly quickly; the arrangement is where the headroom is, and closing it
> means learning to recognise what a protein is from its sequence alone, from scratch,
> on CPU.
> Evaluation
> Submissions are scored by the Operon Reassembly Score, in [0, 1], higher better.
> Each hidden genome is scored on both halves and the per-genome results are averaged,
> so every genome counts equally.
> Arrangement. The submitted order is compared with the true transcription order,
> judged up to reversal â€” shuffled protein content does not reveal which end of an
> operon is the promoter end, so a correctly ordered but reversed answer is fully
> correct. Each case scores
> row = 0.70 * exact_order_match + 0.30 * adjacency_F1
> where adjacency_F1 is the fraction of the three true neighbour pairs that come out
> adjacent in the submitted order. A genome's mean row score is then chance-corrected
> against the score of guessing at random:
> CHANCE        = 0.70 / 12 + 0.30 * 0.5          # = 0.2083
> Arrangement_g = max(0, (mean_row - CHANCE) / (1 - CHANCE))
> A constant order, a random order, or any rule that ignores the proteins is worth
> essentially nothing here â€” such a submission lands around 0.03 on this half, against
> 0.72 for the reference bound. There is no way to buy arrangement credit without
> actually telling the four proteins apart.
> Dialect. Each submitted slot sequence is compared with the real coding sequence
> codon by codon, at every position whose amino acid has more than one synonymous codon.
> A correct codon is not worth the same everywhere; each synonymous site carries a weight
> w = (1 - p_ref(true codon)) ** 2
> where p_ref(c) is the frequency of codon c inside its amino-acid family, pooled
> over all hidden reference sequences. Reproducing the codon nearly every prokaryote
> would have used is worth little; getting right the choices that actually distinguish
> this genome from the prokaryotic average is worth close to a full point. The reference
> frequencies depend only on the hidden sequences, so they are identical for everyone
> and no submission can shift them; a close approximation is computable from
> train_operons.csv.
> Dialect_g = sum(w * hit) / sum(w)          over that genome's synonymous sites
> score     = mean over genomes of (0.55 * Arrangement_g + 0.45 * Dialect_g)
> Runnable reference scorer â€” this is exactly how submissions are graded:
> import re
> from collections import Counter, defaultdict
> import pandas as pd
> BASES = "TCAG"
> CODONS = [a + b + c for a in BASES for b in BASES for c in BASES]
> AAS = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
> CODON2AA = dict(zip(CODONS, AAS))
> FAMILY_SIZE = Counter(CODON2AA[c] for c in CODONS if CODON2AA[c] != "*")
> DEGENERATE = {c: CODON2AA[c] for c in CODONS
> if CODON2AA[c] != "*" and FAMILY_SIZE[CODON2AA[c]] > 1}
> CLEAN = str.maketrans({"U": "T", "u": "T", " ": None, "\t": None,
> "\n": None, "\r": None, "-": None})
> W_ARRANGEMENT, W_DIALECT, W_EXACT, W_ADJACENCY = 0.55, 0.45, 0.70, 0.30
> CHANCE = W_EXACT / 12 + W_ADJACENCY * 0.5
> def codons(v):
> s = str(v).translate(CLEAN).upper()
> return [s[i:i + 3] for i in range(0, len(s) - len(s) % 3, 3)]
> def order(v):
> f = [int(m.group(1)) - 1 for m in re.finditer(r"q([1-9])", str(v), re.I)]
> return f if len(f) == 4 and sorted(f) == [0, 1, 2, 3] else None
> def arrangement_row(pred, true):
> p = order(pred)
> if p is None:
> return 0.0
> t = order(true)
> exact = 1.0 if (p == t or p == t[::-1]) else 0.0
> tp = {frozenset((t[i], t[i + 1])) for i in range(3)}
> pp = {frozenset((p[i], p[i + 1])) for i in range(3)}
> return W_EXACT * exact + W_ADJACENCY * (len(tp & pp) / len(tp))
> def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
> # ... structural validation of columns, row count, duplicate and unknown ids ...
> pred_arr = dict(zip(submission["id"].astype(str), submission["arrangement"]))
> pred_cds = dict(zip(submission["id"].astype(str), submission["slot_cds"]))
> truth, pooled = {}, Counter()
> for rid, org, arr, slot_cds in answers.itertuples(index=False):
> slots = [codons(s) for s in str(slot_cds).split("|")]
> truth[str(rid)] = (org, arr, slots)
> for s in slots:
> pooled.update(c for c in s if c in DEGENERATE)
> fam_total = Counter()
> for c, n in pooled.items():
> fam_total[DEGENERATE[c]] += n
> weight = {c: (1.0 - pooled[c] / fam_total[DEGENERATE[c]]) ** 2 for c in pooled}
> arr = defaultdict(lambda: [0.0, 0])
> dia = defaultdict(lambda: [0.0, 0.0])
> for rid, (org, true_arr, true_slots) in truth.items():
> a = arr[org]
> a[0] += arrangement_row(pred_arr.get(rid, ""), true_arr); a[1] += 1
> got = str(pred_cds.get(rid, "")).split("|")
> d = dia[org]
> for k, tc_list in enumerate(true_slots):
> pc = codons(got[k]) if k < len(got) else []
> for i, tc in enumerate(tc_list):
> if tc not in DEGENERATE:
> continue
> w = weight.get(tc, 1.0)
> d[1] += w
> if i < len(pc) and pc[i] == tc:
> d[0] += w
> scores = []
> for org, (total, count) in arr.items():
> hit, denom = dia[org]
> corrected = max(0.0, (total / count - CHANCE) / (1.0 - CHANCE))
> scores.append(W_ARRANGEMENT * corrected + W_DIALECT * (hit / denom))
> return float(sum(scores) / len(scores))
> Grading is forgiving about surface form: case is ignored, U is accepted for T,
> whitespace and dashes are stripped, and the slot order tokens may be written q1 or
> Q1. It is not forgiving about content â€” a codon that does not match exactly scores
> nothing, and a sequence shorter than its protein loses every position it fails to
> cover. A malformed value loses only the component it corrupts: an unparseable
> arrangement scores zero for that case's arrangement without touching its dialect
> score, and vice versa. Structurally invalid submissions (missing columns, wrong row
> count, duplicate ids, unknown or missing ids) raise an error rather than scoring.
> Dataset
> Training covers 768 genomes; the hidden set covers 48 genomes drawn from 39 taxonomic
> orders that do not occur in training at all.
> Files:
> train_operons.csv â€” 22,983 labelled operons; columns
> id, organism_id, slot_proteins, arrangement, slot_cds.
> train_trna.csv â€” the transfer-RNA gene complement of every training genome;
> columns organism_id, amino_acid, anticodon, copy_number.
> train_rrna16s.csv â€” the 16S ribosomal RNA gene of every training genome;
> columns organism_id, rrna_16s.
> test_operons.csv â€” 1,253 operons to reassemble; columns
> id, organism_id, slot_proteins.
> test_trna.csv â€” the transfer-RNA gene complement of every hidden genome.
> test_rrna16s.csv â€” the 16S ribosomal RNA gene of every hidden genome.
> sample_submission.csv â€” submission template; columns id, arrangement, slot_cds.
> Columns:
> id (string) â€” unique case identifier, op_... in training and tp_... in the
> hidden set.
> organism_id (string) â€” opaque identifier of the genome the operon came from,
> e.g. gnm_1f0c2ad934. It carries no information beyond grouping: organism names,
> lineages, GC content, genome size, gene names and coordinates are not distributed.
> slot_proteins (string) â€” the four proteins of the operon in slot order
> q1|q2|q3|q4, |-separated, one letter per residue over the standard twenty. The
> slot order is a fresh random shuffle for every case and means nothing. The initiator
> residue and the stop codon have been trimmed, so each string is the mature reading
> frame body.
> arrangement (string) â€” target (training only): the four slots in transcription
> order, written q3q1q4q2. This example says gene q3 is transcribed first, then
> q1, then q4, then q2.
> slot_cds (string) â€” target (training only): the genome's real coding sequence
> for each slot, |-separated in slot order, over the alphabet ACGT. Part k is
> exactly 3 * len(slot_proteins[k]) nucleotides and its codon i translates to
> residue i of slot k under the standard genetic code. Note that slot_cds follows
> the slots, not the arrangement â€” the two targets are independent.
> amino_acid (string) â€” the amino acid a transfer-RNA gene is annotated for.
> anticodon (string) â€” that gene's anticodon triplet, read on the tRNA, e.g.
> TAA. The codon it pairs with is the reverse complement.
> copy_number (int) â€” how many genes in that genome carry this amino-acid /
> anticodon combination. Gene dosage is the standard stand-in for how abundant the
> corresponding tRNA is in the cell.
> rrna_16s (string) â€” the genome's 16S ribosomal RNA gene over ACGT, roughly
> 1,200â€“1,800 nucleotides. It says nothing directly about codon usage or gene order,
> but it does say which genomes are relatives.
> Example row (train_operons.csv), truncated:
> id:            op_3f9ac1d5e0b7
> organism_id:   gnm_1f0c2ad934
> slot_proteins: MKQLSDLIAT...|GTVIENAHFV...|LLSAWQPFRE...|AIDTQVVLKG...
> arrangement:   q3q1q4q2
> slot_cds:      ATGAAACAGCTG...|GGCACCGTGAT...|CTGCTGAGCGC...|GCGATTGATAC...
> Example rows (train_trna.csv):
> organism_id,amino_acid,anticodon,copy_number
> gnm_7a6f29a043,A,GGC,1
> gnm_7a6f29a043,A,TGC,2
> gnm_7a6f29a043,C,GCA,1
> gnm_7a6f29a043,D,GTC,3
> TGC read on the tRNA pairs with the alanine codon GCA; the same tRNA also reads
> GCT, GCC and GCG through wobble at the third position, which is the kind of
> relationship the model has to work out for itself.
> Every operon in the data is a real one: four genes in a row on the same replicon and
> the same strand, with every intergenic gap at most 50 bp. Cases are further restricted
> to operons whose neighbour pairs recur across the training genomes, so every hidden
> arrangement is one that a model could in principle have learned â€” the difficulty is in
> recognising the proteins, not in guessing a one-off gene order.
> The split is by taxonomic order: not one of the 48 hidden genomes shares an order â€” and
> therefore no family, genus or species â€” with any training genome. No coding sequence,
> gene, GC statistic or codon count from a hidden genome appears anywhere in the public
> files; its transfer-RNA and 16S ribosomal RNA genes are all you are given about it.
> Submission
> A CSV with exactly the columns id, arrangement and slot_cds, one row per row of
> test_operons.csv; the id column must match test_operons.csv exactly, with no
> duplicates and no missing rows.
> id,arrangement,slot_cds
> tp_9d09a4c4ae0c,q3q1q4q2,ATGAAACAG...|GGCACCGTG...|CTGCTGAGC...|GCGATTGAT...
> tp_4670704abc6a,q1q4q2q3,AGCATTGAA...|AACCTGTAT...|TTTCAGGGC...|AAAACCGCG...
> 1,253 rows plus a header.
> arrangement lists all four of q1â€“q4 exactly once, in transcription order.
> Either direction is accepted.
> slot_cds holds four |-separated nucleotide strings in slot order q1..q4,
> each 3 * len(protein) characters over ACGT, in frame with the given protein.
> Row order does not matter. Case is ignored and U is accepted for T.
> sample_submission.csv is a correctly formatted placeholder â€” a fixed slot order and
> a single repeated codon â€” and scores essentially zero.
> Allowed
> Training any model from scratch on the supplied training operons â€” protein encoders
> (convolutional, recurrent, attention-based, k-mer embedding), pairwise or
> set-to-sequence orderings, permutation decoders, autoregressive codon decoders, and
> ensembles of these.
> Any way of turning the transfer-RNA table and the 16S rRNA gene into a conditioning
> vector: dosage features, wobble-pairing features, k-mer profiles, learned encoders,
> dimensionality reduction fitted on the training genomes.
> Self-supervised or contrastive pretraining on the provided proteins and coding
> sequences, auxiliary objectives, and multi-task setups that share a representation
> between the arrangement and dialect halves.
> Exact or approximate search over the twelve distinct orders, structured decoding,
> and consistency constraints between the two outputs.
> Standard modelling craft: augmentation, class balancing, label smoothing, negative
> sampling, calibration, hyper-parameter search inside the submission script,
> cross-validation over held-out training genomes, and ensembling.
> Grouping training genomes by inferred similarity and learning how dialect and gene
> order vary across them. Learning relationships between genomes from the provided data
> is part of the problem.
> Not Allowed
> This is a training challenge. Both outputs must come from a model genuinely
> trained or fine-tuned inside your submission script. A hand-written codon table, a
> fixed or random slot order, a hard-coded rule, or any pipeline from which the learned
> component could be deleted without changing the output is not an acceptable solution,
> regardless of what it scores.
> No external biological data or models. No codon usage databases, no reference
> genomes, no operon or gene-neighbourhood databases (OperonDB, DOOR, STRING, KEGG and
> the like), no protein family databases (Pfam, COG, InterPro), no pretrained DNA,
> codon or protein language models (ESM, ProtBert, DNABERT, Nucleotide Transformer,
> CaLM and similar), and no alignment tools shipped with external reference databases.
> The only sequence data your model may learn from is what is in the public files.
> No de-anonymisation. Do not attempt to identify a hidden genome or a hidden
> protein â€” from the 16S gene, the tRNA complement, the protein sequences, or anything
> else â€” in order to look up its real gene order or codon usage. The identifiers are
> opaque on purpose. If you find something in the public files that reveals a hidden
> answer, report it by tagging the reviewers instead of using it.
> No use of the hidden set beyond one genome at a time. Reasoning about a single
> organism_id using its own cases is fine â€” that is one genome's worth of evidence and
> is how the problem would arrive in practice. Pooling across hidden genomes is not. No
> pseudo-labelling, no fitting model parameters on test proteins, no test-time
> adaptation, no calibration against test-set-wide statistics.
> No hard-coded outputs, no answer dictionaries, no tuning against submission
> feedback, and no exploiting identifiers, row order, file order, string lengths or any
> other artefact of how the files were written.
> Hardware & Compute
> Target hardware: CPU only â€” 10 CPU cores and 62 GB of RAM. There is no GPU.
> Nothing here needs one; the intended solution is a compact model trained from scratch
> on protein and codon tokens.
> Time budget: the complete end-to-end run â€” data preparation, feature building,
> training and inference, all inside one independent script â€” must finish in under
> 1.5 hours on that hardware. Build a safeguard into your script that stops training
> and writes the submission once you approach the limit.
> Libraries: only what is already preinstalled in the Kaggle Python Docker image
> (numpy, pandas, scikit-learn, xgboost, lightgbm, PyTorch CPU, TensorFlow CPU and so
> on). No pip installs and no external dependencies of any kind.
> No internet access at solve time, at all. No hosted LLM or model API calls, no
> package downloads, no fetching model weights. This challenge needs no base model, so
> none is bundled; everything your solution requires is in the public files.
> The choice of features, architecture, objective and decoding strategy is entirely
> yours, scoped to preinstalled libraries and the provided data.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## 'Missing Semantic Role Prediction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73vtxh25nzdwfpcrjwf8vrys8bx25y
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> 1. Background and Overview
> Language understanding isn't just about parsing grammar; it's about playing detective to determine "who did what to whom, when, and where."
> The Objective: The primary goal of this challenge is to predict missing semantic roles. You are provided with a sentence, a target predicate (the action), and a "visible bundle" of already answered QA roles (the known evidence). Your mission is to deduce the semantic blind spots by generating the 1 to 2 missing question-answer pairs required to complete the predicate's full semantic frame.
> The Catch: This is a pure, From Scratch representation learning challenge. You must recover the exact natural language questions, their seven grammatical slot values, and the precise answer spans directly from the textâ€”using nothing but your own custom-built architecture.
> 2. Dataset Architecture
> Derived from tens of thousands of human-interrogated texts, our preparation pipeline identifies robust predicates containing 3 to 18 usable QA roles and surgically redacts 1 or 2 of them to serve as your prediction targets.
> To ensure absolute benchmark integrity, document metadata, sentence IDs, and worker IDs have been wiped and hashed into opaque identifiers. Document-level hashing ensures zero data leakage between training and testing environments.
> The Classified Files
> train.csv: Your training ground. Contains the visible context roles alongside the hidden target roles. (~30,000+ rows)
> test.csv: The live test environment. Contains only the visible evidence. (~6,000+ rows)
> sample_submission.csv: A pre-formatted template for your algorithmic verdicts.
> task_metadata.json: Operational parameters, including the strict 7-slot order (["wh", "aux", "subj", "verb", "obj", "prep", "obj2"]).
> Data Schema
> Plaintext
> +----------------------+-----------+-----------------------------------------------------------------------+
> | Column Name          | Data Type | Description                                                           |
> +----------------------+-----------+-----------------------------------------------------------------------+
> | id                   | STRING    | Opaque, anonymized unique identifier for the instance/row.            |
> | sentence             | STRING    | The complete, tokenized text of the source sentence.                  |
> | predicate_index      | INTEGER   | The 0-based word index of the target verb/predicate in the sentence.  |
> | predicate            | STRING    | The specific verb predicate token being analyzed.                     |
> | predicate_forms_json | JSON      | Morphological inflections of the target predicate (e.g., past, stem). |
> | visible_qas_json     | JSON      | The unmasked QA roles provided as context. Contains question,         |
> |                      |           | slots, and answers.                                                   |
> | answer_json          | JSON      | (Train only) The 1-2 masked semantic roles your model must learn to   |
> |                      |           | predict.                                                              |
> +----------------------+-----------+-----------------------------------------------------------------------+
> 3. Evaluation Matrix
> Submissions face a ruthless semantic matching framework. Any malformed JSON, schema violation, or out-of-bounds index immediately results in a 0 for that row. Surviving predictions are graded between 0 and 1 using a five-pillar weighted formula.
> Per-Row Scoring Formula
> The Absolute Truth (40% - Exact QA-Artifact F1): Exact triplet match F1 of the (question, slots, answers) between your prediction and the ground truth.
> The Forgiving Detective (30% - Soft Bidirectional Match): A softened metric computing maximum bidirectional similarity: token-level F1 for questions (45%), exact match F1 for slots (25%), and exact match F1 for answer spans (30%).
> The Spatial Overlap (15% - Global Answer-Span F1): F1 overlap of all predicted answer spans versus all true answer spans in the target bundle, entirely independent of the generated question.
> The Perfect Frame (10% - Exact Bundle Match): A binary, all-or-nothing reward (1 if the predicted QA set perfectly matches the ground truth set, 0 otherwise).
> The Self-Awareness Bonus (5% - Confidence Calibration): Scored as 1 - abs(confidence - exact_qa_f1). Rewards algorithms that accurately predict their own Exact QA F1 score.
> Final Aggregation
> Because deducing two missing roles is exponentially harder than deducing one, the final score balances average performance with worst-case robustness: Final Score = (0.90 Mean Row Score) + (0.10 Worst Hidden-Bundle-Size Mean Score)
> 4. Submission Protocol
> Your algorithm must output a CSV file containing exactly three columns: id, prediction_json, and confidence.
> prediction_json: A JSON string containing a single key "qas" that maps to a list of up to 2 dictionary objects (as you are predicting a maximum of 2 missing roles).
> The Object Anatomy: Each dictionary must contain "question", "slots" (strictly the 7 QA-SRL slots: wh, aux, subj, verb, obj, prep, obj2), and "answers".
> Answer Coordinates: Defined by start-inclusive and end-exclusive token indices (start, end) and the matching string (text).
> confidence: A float between 0 and 1 representing the model's self-assessed Exact QA F1 expectation.
> Example Payload (submission.csv):
> Code snippet
> id,prediction_json,confidence
> q_1a2b3c4d5e6f7g8h,"{""qas"":[{""question"":""Who ate something?"",""slots"":{""wh"":""who"",""aux"":""_"",""subj"":""_"",""verb"":""past"",""obj"":""something"",""prep"":""_"",""obj2"":""_""},""answers"":[{""start"":0,""end"":1,""text"":""Alice""}]}]}",0.85
> q_8h7g6f5e4d3c2b1a,"{""qas"":[{""question"":""Where did someone go?"",""slots"":{""wh"":""where"",""aux"":""did"",""subj"":""someone"",""verb"":""go"",""obj"":""_"",""prep"":""_"",""obj2"":""_""},""answers"":[{""start"":5,""end"":7,""text"":""to school""}]},{""question"":""When did someone go somewhere?"",""slots"":{""wh"":""when"",""aux"":""did"",""subj"":""someone"",""verb"":""go"",""obj"":""somewhere"",""prep"":""_"",""obj2"":""_""},""answers"":[{""start"":8,""end"":9,""text"":""yesterday""}]}]}",0.92
> 5. The Rules & Constraints
> This is a test of pure algorithmic ingenuity. You are stepping into the ring bare-knuckled. Leave your massive parameter weights at the door.
> No Pretrained Titans: You may NOT use pretrained language models (BERT, RoBERTa, T5, LLaMA), pretrained QA pipelines, or external static embeddings (GloVe, Word2Vec). All tokenizers, embeddings, and learned representations must be instantiated and trained strictly on the provided train.csv.
> No Outside Intelligence: Zero access to external parsers, PropBank, FrameNet, original QA-SRL databases, source sentence scraping, or web/API calls.
> No Test Gaming: Test adaptation, pseudo-labeling the test set, or metric-gaming during inference is strictly forbidden.
> Hardware Isolation: Your inference code must execute entirely offline within a 90-minute time limit on standard CPU architecture (max 10 CPU cores, 62 GB RAM). GPUs are strictly prohibited for inference.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Cameraâ€“LiDAR Warp Field Recovery from Scratch

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70hwmczte9r8rn68pdnw61kn8byvqh
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Cameraâ€“LiDAR Warp Field Recovery from Scratch
> Overview
> Each episode contains two views of the same railway scene:
> an RGB camera image; and
> a sparse LiDAR depth projection that has been displaced away from its correct image locations.
> The displacement is not one global translation. It changes smoothly across the image. Your task is to recover that spatially varying warp as a 4 Ã— 6 grid of direction tokens. A successful solution must learn from the released training episodes how camera structure and sparse depth geometry agree. There is no scalar class or regression target for an episode; every prediction is a structured field containing 24 coupled decisions.
> Train and test are separated by physical scene group. Frames from a test scene never appear in training. File names and row identifiers are opaque. Before the scored warp is generated, every episode receives a private crop, optional reflection, smooth common geometric transform, and RGB tone transform. Consequently, public source calibration does not directly reproduce the private targets.
> From-Scratch Track
> This is a from-scratch computer-vision challenge. Every scored solution must contain at least one predictive component whose parameters are fitted using the released training episodes and their code_matrix targets.
> Allowed
> Neural networks initialized from random weights and trained on the released training set.
> Models implemented with standard numerical or deep-learning libraries, provided no pretrained parameters are loaded.
> Image gradients, depth normalization, sparse convolutions, correlation volumes, geometric interpolation, and other non-recognizing preprocessing.
> Solver-generated augmentations or synthetic perturbations made only from released training inputs and labels.
> Analytic geometry or optimization combined with a component that is genuinely fitted on the released training data.
> Architecture definitions and general-purpose software packages that contain no learned parameters.
> Not allowed
> Pretrained models or weights of any kind, including visual encoders, foundation models, depth models, optical-flow models, and checkpoint-derived feature extractors.
> External datasets, external feature banks, upstream sensor files, map data, or precomputed calibration resources.
> Internet access, remote APIs, source-corpus lookup, or matching released frames against public copies.
> Fitting on test inputs, pseudo-labeling test rows, or manually constructing predictions for specific test identifiers.
> Importing parameters obtained from another dataset or an earlier run that used information outside this challenge.
> Compliance may be checked during solution review. The submitted training and inference pipeline must run offline in the evaluation environment.
> Task
> The RGB image is 384 pixels wide and 256 pixels high. The candidate depth PNG is a 16-bit single-channel image with the same shape:
> 0 means that no LiDAR return occupies that pixel;
> a positive value is forward depth in millimetres.
> The unknown warp is controlled by a grid with four rows and six columns. Grid centres span x = 12 through 371 and y = 68 through 247. The matrix uses raster order: within each row, controls run from left to right; rows then run from top to bottom. Thus code_matrix[0][0] is the top-left control, code_matrix[0][5] is the top-right control, and code_matrix[3][5] is the bottom-right control.
> Each control is one of eight direction tokens. The direction pairs stored in task_manifest.json are unit vectors with Euclidean length 1. The grader multiplies each unit vector by step_pixels = 16, so every control produces a displacement of exactly 16 pixels. The actual (delta_x, delta_y) displacements are:
> d0: right, (16, 0) pixels
> d1: down-right, (11.3137, 11.3137) pixels
> d2: down, (0, 16) pixels
> d3: down-left, (âˆ’11.3137, 11.3137) pixels
> d4: left, (âˆ’16, 0) pixels
> d5: up-left, (âˆ’11.3137, âˆ’11.3137) pixels
> d6: up, (0, âˆ’16) pixels
> d7: up-right, (11.3137, âˆ’11.3137) pixels
> Between control centres, the vector field is obtained by bilinear interpolation. Outside the rectangle of control centres, coordinates are clamped to the nearest grid boundary before interpolation.
> If a candidate LiDAR location is c, its predicted aligned location is
> ð‘”
> ^
> =
> ð‘
> +
> ð¹
> ð‘‡
> ^
> (
> ð‘
> )
> ,
> g
> â€‹
> =c+F
> T
> â€‹
> (c),
> where
> ð‘‡
> ^
> T
> is the submitted token grid and
> ð¹
> ð‘‡
> ^
> F
> T
> â€‹
> is its interpolated 16-pixel vector field.
> Dataset
> The public release contains 131 training episodes and 58 test episodes. Training episodes come from 13 physical scene groups; test episodes come from six different groups. Group identifiers are used only while constructing the split and are not released as model features.
> train.csv
> id â€” Data type: string. Opaque unique episode identifier.
> rgb_file â€” Data type: string. Relative path to the RGB JPEG.
> candidate_depth_file â€” Data type: string. Relative path to the misaligned 16-bit depth PNG.
> image_shape â€” Data type: JSON array of integers. Image height and width; always [256,384].
> grid_shape â€” Data type: JSON array of integers. Control-grid rows and columns; always [4,6].
> code_matrix â€” Data type: JSON array of arrays of strings. Gold 4 Ã— 6 direction-token grid.
> test.csv
> test.csv contains the same id, rgb_file, candidate_depth_file, image_shape, and grid_shape fields as train.csv. It does not contain code_matrix.
> Image directories
> rgb/ â€” 8-bit, three-channel JPEG camera crops.
> candidate_depth/ â€” 16-bit, one-channel PNG depth projections. Zero is background; positive values are millimetres.
> sample_submission.csv
> id â€” Data type: string. One test identifier.
> code_matrix â€” Data type: JSON string. One 4 Ã— 6 token grid. The sample alternates d0 and d4 only to demonstrate formatting; it is not a baseline recommendation.
> task_manifest.json
> The manifest records task, train_rows, test_rows, image_shape, grid_shape, direction_tokens, direction_vectors, step_pixels, grid_bounds_xy, and metric. The metric object contains the exact public constants used below: row component weights, anchor sigma, and final aggregation weights.
> Evaluation
> Let
> ð‘‡
> ð‘–
> T
> i
> â€‹
> be the private 4 Ã— 6 token grid and
> ð‘‡
> ^
> ð‘–
> T
> i
> â€‹
> the submitted grid for row
> ð‘–
> i.
> Token agreement
> Token agreement is exact accuracy over the 24 controls:
> ð‘ˆ
> ð‘–
> =
> 1
> 24
> âˆ‘
> ð‘Ÿ
> =
> 1
> 4
> âˆ‘
> ð‘
> =
> 1
> 6
> 1
> â£
> [
> ð‘‡
> ^
> ð‘–
> ,
> ð‘Ÿ
> ,
> ð‘
> =
> ð‘‡
> ð‘–
> ,
> ð‘Ÿ
> ,
> ð‘
> ]
> .
> U
> i
> â€‹
> =
> 24
> 1
> â€‹
> r=1
> âˆ‘
> 4
> â€‹
> c=1
> âˆ‘
> 6
> â€‹
> 1[
> T
> i,r,c
> â€‹
> =T
> i,r,c
> â€‹
> ].
> Geometric anchor quality
> Each test row has 320 private LiDAR correspondences. For anchor
> ð‘—
> j,
> ð‘
> ð‘–
> ð‘—
> c
> ij
> â€‹
> is the displaced candidate coordinate and
> ð‘”
> ð‘–
> ð‘—
> g
> ij
> â€‹
> is its calibrated target coordinate. The submitted field predicts
> ð‘”
> ^
> ð‘–
> ð‘—
> =
> ð‘
> ð‘–
> ð‘—
> +
> ð¹
> ð‘‡
> ^
> ð‘–
> (
> ð‘
> ð‘–
> ð‘—
> )
> .
> g
> â€‹
> ij
> â€‹
> =c
> ij
> â€‹
> +F
> T
> i
> â€‹
> â€‹
> (c
> ij
> â€‹
> ).
> Anchor quality is
> ð´
> ð‘–
> =
> 1
> 320
> âˆ‘
> ð‘—
> =
> 1
> 320
> exp
> â¡
> â£
> (
> âˆ’
> âˆ¥
> ð‘”
> ^
> ð‘–
> ð‘—
> âˆ’
> ð‘”
> ð‘–
> ð‘—
> âˆ¥
> 2
> 2
> 2
> (
> 5.5
> )
> 2
> )
> .
> A
> i
> â€‹
> =
> 320
> 1
> â€‹
> j=1
> âˆ‘
> 320
> â€‹
> exp(âˆ’
> 2(5.5)
> 2
> âˆ¥
> g
> â€‹
> ij
> â€‹
> âˆ’g
> ij
> â€‹
> âˆ¥
> 2
> 2
> â€‹
> â€‹
> ).
> The row score is
> ð‘†
> ð‘–
> =
> 0.30
> ð‘ˆ
> ð‘–
> +
> 0.70
> ð´
> ð‘–
> .
> S
> i
> â€‹
> =0.30U
> i
> â€‹
> +0.70A
> i
> â€‹
> .
> Let
> ð‘›
> n be the number of test rows and
> ð‘˜
> =
> âŒˆ
> ð‘›
> /
> 4
> âŒ‰
> k=âŒˆn/4âŒ‰. Let
> ð‘Š
> W be the mean of the
> ð‘˜
> k lowest row scores. The final score is
> Score
> â¡
> =
> 0.85
> (
> 1
> ð‘›
> âˆ‘
> ð‘–
> =
> 1
> ð‘›
> ð‘†
> ð‘–
> )
> +
> 0.15
> ð‘Š
> .
> Score=0.85(
> n
> 1
> â€‹
> i=1
> âˆ‘
> n
> â€‹
> S
> i
> â€‹
> )+0.15W.
> The worst-quartile term rewards methods that remain reliable across scenes instead of solving only the easiest views. There are no private difficulty buckets or undocumented weights.
> Zero-displacement diagnostic
> A direct no-warp diagnostic leaves every candidate coordinate unchanged, so
> ð‘”
> ^
> ð‘–
> ð‘—
> =
> ð‘
> ð‘–
> ð‘—
> g
> â€‹
> ij
> â€‹
> =c
> ij
> â€‹
> . The submission grammar has no zero-magnitude tokenâ€”all eight valid controls have magnitude 16 pixelsâ€”so this is not a valid submission file. For a comparable diagnostic score, token accuracy is set to zero and only the resulting anchor quality contributes.
> On the frozen test targets, the no-warp field has mean anchor quality 0.031396, mean row score 0.021977, worst-quartile row mean 0.016905, and final diagnostic score 0.021216. This confirms that leaving the LiDAR projection in place is far below a learned alignment method.
> Submission Format
> Submit one CSV containing exactly these columns in this order:
> id â€” Data type: string. Each test identifier exactly once.
> code_matrix â€” Data type: JSON string. Exactly four arrays, each containing six tokens from d0 through d7.
> Example:
> id,code_matrix
> e_0123456789abcdef,"[[""d0"",""d0"",""d1"",""d1"",""d2"",""d2""],[""d0"",""d1"",""d1"",""d2"",""d2"",""d3""],[""d7"",""d0"",""d1"",""d2"",""d3"",""d4""],[""d7"",""d7"",""d0"",""d1"",""d2"",""d3""]]"
> Python example:
> import json
> import pandas as pd
> test = pd.read_csv("test.csv")
> default_grid = [["d0"] * 6 for _ in range(4)]
> submission = pd.DataFrame({
> "id": test["id"],
> "code_matrix": [json.dumps(default_grid, separators=(",", ":"))] * len(test),
> })
> submission.to_csv("submission.csv", index=False)
> Missing IDs, extra IDs, duplicate IDs, extra columns, malformed JSON, incorrect grid dimensions, and unknown tokens are rejected.
> Evaluation Environment
> Solutions run offline CPU only. Internet access is disabled. Training must occur during the submitted run from random initialization using the released training data; downloading weights or data at runtime is not possible and is not permitted.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Strata Witness Panel

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx72p6731et96r3srsje884vpd8bzgb7
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Strata Witness Panel
> Overview
> Field teams often date a rock layer from a collection of co-occurring fossils rather than from a single specimen. Some taxa span enormous intervals, some are locally diagnostic, and a seemingly precise conclusion may collapse if one identification is later withdrawn.
> Each row contains an anonymized fossil assemblage with aligned taxon and family tokens. Select exactly three taxa as its chronological witness panel. A strong panel should define a narrow interval consistent with the held-out collection, remain informative after any one witness is removed, and avoid three redundant representatives of the same family.
> This is a From Scratch model-development benchmark. The useful representations must be learned from the released training panels and co-occurrence structure. It is not an ordinary fixed-label classifier: candidate sets differ by row, token identities are anonymous, and the grader evaluates the submitted panel's utility rather than exact equality to one stored tuple.
> Panel Semantics
> taxon_tokens and family_tokens are space-delimited lists with matching positions. If the fourth taxon token is selected, its family is the fourth family token. Candidate order carries no chronological or quality information.
> A submission selects three distinct tokens present in that row's taxon_tokens. Panel order is ignored.
> Evaluation
> The score is maximized and ranges from 0 to 1. Invalid panels receive zero row credit.
> For evaluation only, each candidate taxon has a hidden robust temporal envelope [lo_i, hi_i] and support count n_i, estimated from the training partition. Let c be the midpoint of the held-out collection's accepted age interval. For any selected subset S:
> L = max(lo_i for i in S)
> H = min(hi_i for i in S)
> If L <= H:
> distance = max(L - c, c - H, 0)
> width = H - L
> Otherwise:
> distance = min(abs(c - L), abs(c - H)) + (L - H)
> width = 0
> Define:
> Q(S, W, D) = exp(-distance / D)
> *(0.68 + 0.32*  exp(-width / W))
> * min(1, sqrt(min(n_i for i in S) / 6))
> For a three-taxon panel P:
> panel_utility = 0.64 * Q(P, 52, 12)
> + 0.26 * mean(Q(P without j, 86, 18) for j in P)
> + 0.10 * family_diversity
> family_diversity is the number of distinct aligned family tokens in the panel divided by 3.
> The row score is a skill score against the median feasible panel:
> row_score = clip(
> (panel_utility - median_feasible_utility)
> / (best_feasible_utility - median_feasible_utility),
> 0,
> 1,
> )
> When every feasible panel has the same utility, every valid panel receives full row credit. The final score is the mean row score over all 500 test rows. This gives full credit to every tied optimum and does not require matching one canonical panel.
> Dataset
> Public files:
> | File | Rows | Description |
> |---|---:|---|
> | train.csv | 2000 | Training assemblages and expert witness panels. |
> | test.csv | 500 | Publication-disjoint held-out assemblages without panels. |
> | sample_submission.csv | 500 | Valid submission template. |
> train.csv columns:
> | Column | Type | Meaning |
> |---|---|---|
> | id | string | Anonymous collection identifier. |
> | region_token | string | Anonymous broad paleogeographic region. |
> | environment_token | string | Anonymous depositional-material context. |
> | n_taxa | integer | Number of candidates in the row. |
> | taxon_tokens | string | Space-delimited candidate taxon tokens. |
> | family_tokens | string | Space-delimited family tokens aligned with taxon_tokens. |
> | witness_panel | string | Three distinct selected taxon tokens. |
> test.csv has the same columns except witness_panel.
> The split is disjoint by source publication. Source collection numbers, publication identifiers, taxon names, coordinates, geological ages, and original row order are not released. Test candidates have training support, but held-out publications and assemblage combinations are unseen.
> Submission
> Submit exactly these columns, in this order:
> id,witness_panel
> swp_0123456789abcdefabcd,T03A1C9D554B210 T51F0D6224AC108 TAF26E55D1E4377
> swp_fedcba9876543210abcd,T0B741C33809412 T64E233CAF25D08 TE7A912DC885013
> Requirements:
> Include exactly one row for every test id.
> Select exactly three distinct tokens from that row's taxon_tokens.
> Separate tokens with single spaces; panel order does not affect scoring.
> Do not include extra columns.
> Save the file as ./working/submission.csv.
> Restrictions
> Train all predictive parameters from scratch using only the released public files.
> Do not use pretrained models, pretrained embeddings, external databases, internet lookup, source-record reconstruction, or manually curated fossil ranges.
> Do not use row IDs, hashes, candidate order, hidden files, or grader internals as predictive features.
> CPU-compatible feature learning, set encoders, interaction models, validation, calibration, and ensembling are allowed.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## In-Context CAD Constraint Sequence Completion

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7azfxawz2txzxqbt7cjre2t18bhfac
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> In-Context CAD Constraint Sequence Completion
> Overview
> This is a from-scratch sequence-to-sequence challenge about geometric design intent.
> Every episode contains three real CAD sketches originating from the same design document:
> two support sketches show complete geometry and complete constraint sequences; and
> one query sketch shows its geometry and only the beginning of its constraint sequence.
> Your task is to generate the missing continuation of the query sequence in the original designer-authored order.
> A constraint records a geometric relationship such as coincidence, parallelism, perpendicularity, tangency, or equal size, together with the entities or endpoints it connects. The continuation is therefore not a class label. It is a variable-length program that must predict relation identity, entity binding, and sequence order together.
> Relation names are encoded independently in every episode as r00 through r08. For example, r03 might represent perpendicularity in one episode and coincidence in another. The two complete support sketches and the observed query prefix provide the evidence needed to infer the local meanings. Entity IDs are also local to each sketch.
> All scored targets come from constraint sequences authored in real CAD documents. Dataset construction only withholds a suffix, normalizes coordinates, permutes entity IDs, and applies a local relation codebook. It does not generate target constraints.
> Train and test are disjoint by source CAD document. Coordinate normalization, coarse quantization, reflection, rotation, entity permutation, and removal of source identifiers prevent direct record matching from serving as the task.
> From-Scratch Requirement
> Every scored solution must include at least one genuine, non-trivial predictive component whose parameters are fitted during the submitted run using train.jsonl and its continuation targets. Learning only a constant prediction, output-length prior, or global frequency table does not satisfy this requirement.
> Allowed
> Transformers, recurrent networks, graph networks, pointer decoders, and retrieval or alignment components initialized from random weights.
> Models trained only on the released training episodes.
> Statistical or symbolic models whose parameters are estimated from released training targets.
> Constrained decoding, graph matching, dynamic programming, and geometric feature engineering when combined with a component fitted on training data.
> Self-supervised pretraining performed during the submitted run using only the released challenge files.
> Synthetic examples or augmentations generated exclusively from released training episodes.
> Standard software libraries that provide implementations but no learned parameters.
> Not allowed
> Pretrained language, code, vision, graph, or CAD models; pretrained embeddings; checkpoints; adapters; or external tokenizers with learned parameters.
> External CAD files, constraint corpora, geometry datasets, source snapshots, or additional training examples.
> Internet access, remote APIs, source-dataset lookup, CAD-document retrieval, or matching episodes against a public corpus.
> Using the hidden test rows for fitting, pseudo-label selection, or parameter tuning.
> Hard-coded predictions for test identifiers.
> A fixed heuristic with no predictive component fitted from the released training targets.
> The complete training and inference pipeline must run offline. Compliance may be checked during solution review.
> Episode Structure
> Each episode has two support objects, a query geometry sequence, an observed query-constraint prefix, andâ€”on training rowsâ€”the gold continuation.
> Geometry primitives
> Every primitive is one space-separated string beginning with a local entity ID.
> Examples:
> e00 line x03 y05 x27 y05 c0
> e01 point x16 y16 c0
> e02 circle x12 y20 r06 c1
> e03 arc x15 y15 r08 x07 y15 x23 y15 cw c0
> The primitive kinds are line, point, circle, and arc.
> x00 through x31 and y00 through y31 are normalized coordinate bins.
> r01 through r31 are normalized radius bins.
> c0 denotes ordinary geometry and c1 denotes construction geometry.
> cw and ccw denote arc direction.
> Entity IDs run consecutively from e00 within each sketch. IDs do not refer to the same entity across support and query sketches.
> Constraint grammar
> Each constraint is one string:
> relation_token:reference
> relation_token:reference|reference
> Examples:
> r03:e01
> r07:e00.end|e04.start
> r02:e03|e06.start
> Relation tokens range from r00 through r08. Their meanings are permuted independently for every episode but remain consistent across its two supports and query.
> Radius-bin tokens (r01 through r31) occur only inside geometry primitive strings. Relation tokens (r00 through r08) occur only at the start of constraint strings, immediately before :. Although the two token ranges share the letter r, their positions and string grammars make them unambiguous.
> A reference is an entity ID with an optional endpoint suffix:
> a line supports the base ID, .start, and .end;
> an arc supports the base ID, .start, .end, and .center;
> a circle supports the base ID and .center; and
> a point supports only the base ID.
> When a constraint has two references, they appear in lexicographic order.
> Every gold continuation contains between three and ten constraints. Its length is not disclosed in the test input. Every relation token needed by a gold continuation appears at least once in the episode's supports or observed prefix.
> Dataset
> The public release contains 1,200 training episodes and 300 test episodes.
> train.jsonl
> Each line is one JSON object:
> id â€” type: string; opaque unique episode identifier.
> supports â€” type: array of two objects; complete support sketches from the same source document as the query.
> query_geometry â€” type: array of strings; complete normalized query primitive sequence.
> observed_constraints â€” type: array of strings; visible prefix of the query's real constraint sequence.
> continuation â€” type: array of strings; gold missing suffix in designer-authored order.
> Each support object contains:
> geometry â€” type: array of strings; normalized primitive sequence.
> constraints â€” type: array of strings; complete constraint sequence for that support.
> test.jsonl
> Test rows contain id, supports, query_geometry, and observed_constraints. The private continuation is omitted.
> sample_submission.csv
> id â€” type: string; one test identifier.
> continuation_json â€” type: JSON string; predicted ordered array of zero to twelve constraint strings.
> The sample predicts r00:e00 for every test row. It demonstrates serialization only and is not a recommended solution.
> task_manifest.json
> task â€” type: string; machine-readable task identifier.
> primary_domain â€” type: string; sequence-to-sequence and from-scratch domain label.
> train_rows and test_rows â€” type: integers; public split counts.
> supports_per_episode â€” type: integer; value two.
> primitive_count_min and primitive_count_max â€” type: integers; values four and eighteen.
> continuation_length_min and continuation_length_max â€” type: integers; gold range three through ten.
> maximum_predicted_constraints â€” type: integer; value twelve.
> relation_tokens â€” type: array of strings; complete r00 through r08 vocabulary.
> entity_token_pattern â€” type: string; valid entity-reference description.
> submission_columns â€” type: array of strings; required CSV column order.
> row_metric â€” type: object; all published row-component weights.
> final_metric â€” type: object; all published aggregation weights.
> source_document_split â€” type: object; train/test source-group counts and zero-overlap guarantee.
> Evaluation
> Let
> ð‘ƒ
> ð‘–
> P
> i
> â€‹
> be the submitted ordered constraint sequence for episode
> ð‘–
> i, and let
> ðº
> ð‘–
> G
> i
> â€‹
> be its non-empty gold continuation.
> Exact constraint multiset F1
> Let
> ð‘
> ð‘ƒ
> (
> ð‘¥
> )
> c
> P
> â€‹
> (x) and
> ð‘
> ðº
> (
> ð‘¥
> )
> c
> G
> â€‹
> (x) be the multiplicities of complete constraint string
> ð‘¥
> x in the prediction and gold sequence. Define multiset overlap
> ð¼
> (
> ð‘ƒ
> ð‘–
> ,
> ðº
> ð‘–
> )
> =
> âˆ‘
> ð‘¥
> min
> â¡
> (
> ð‘
> ð‘ƒ
> (
> ð‘¥
> )
> ,
> ð‘
> ðº
> (
> ð‘¥
> )
> )
> .
> I(P
> i
> â€‹
> ,G
> i
> â€‹
> )=
> x
> âˆ‘
> â€‹
> min(c
> P
> â€‹
> (x),c
> G
> â€‹
> (x)).
> Then
> ð¸
> ð‘–
> =
> 2
> ð¼
> (
> ð‘ƒ
> ð‘–
> ,
> ðº
> ð‘–
> )
> âˆ£
> ð‘ƒ
> ð‘–
> âˆ£
> +
> âˆ£
> ðº
> ð‘–
> âˆ£
> .
> E
> i
> â€‹
> =
> âˆ£P
> i
> â€‹
> âˆ£+âˆ£G
> i
> â€‹
> âˆ£
> 2I(P
> i
> â€‹
> ,G
> i
> â€‹
> )
> â€‹
> .
> This component requires both the correct relation token and the correct entity references. An empty prediction has
> ð¸
> ð‘–
> =
> 0
> E
> i
> â€‹
> =0.
> Relation-token multiset F1
> Remove the colon and references from every constraint, retaining only its rNN token. Applying the same multiset-F1 definition to those token sequences gives
> ð‘‡
> ð‘–
> T
> i
> â€‹
> . This provides partial credit for recovering local relation identity with incorrect binding.
> Ordered continuation score
> Let
> LCS
> â¡
> (
> ð‘ƒ
> ð‘–
> ,
> ðº
> ð‘–
> )
> LCS(P
> i
> â€‹
> ,G
> i
> â€‹
> ) be the length of a longest common subsequence of complete constraint strings. Define
> ð¿
> ð‘–
> =
> 2
> LCS
> â¡
> (
> ð‘ƒ
> ð‘–
> ,
> ðº
> ð‘–
> )
> âˆ£
> ð‘ƒ
> ð‘–
> âˆ£
> +
> âˆ£
> ðº
> ð‘–
> âˆ£
> .
> L
> i
> â€‹
> =
> âˆ£P
> i
> â€‹
> âˆ£+âˆ£G
> i
> â€‹
> âˆ£
> 2LCS(P
> i
> â€‹
> ,G
> i
> â€‹
> )
> â€‹
> .
> An empty prediction has
> ð¿
> ð‘–
> =
> 0
> L
> i
> â€‹
> =0.
> Row and final scores
> The row score is
> ð‘†
> ð‘–
> =
> 0.45
> ð¸
> ð‘–
> +
> 0.20
> ð‘‡
> ð‘–
> +
> 0.35
> ð¿
> ð‘–
> .
> S
> i
> â€‹
> =0.45E
> i
> â€‹
> +0.20T
> i
> â€‹
> +0.35L
> i
> â€‹
> .
> Let
> ð‘
> N be the number of test rows and let
> ð‘˜
> =
> âŒˆ
> ð‘
> /
> 5
> âŒ‰
> k=âŒˆN/5âŒ‰. Let
> ð‘Š
> W be the mean of the
> ð‘˜
> k lowest row scores. The final score is
> Score
> â¡
> =
> 0.90
> (
> 1
> ð‘
> âˆ‘
> ð‘–
> =
> 1
> ð‘
> ð‘†
> ð‘–
> )
> +
> 0.10
> ð‘Š
> .
> Score=0.90(
> N
> 1
> â€‹
> i=1
> âˆ‘
> N
> â€‹
> S
> i
> â€‹
> )+0.10W.
> There are no hidden task buckets or undocumented weights.
> Submission Format
> Submit one CSV containing exactly these columns in this order:
> id â€” type: string; every test identifier exactly once.
> continuation_json â€” type: JSON string; an ordered array containing at most twelve valid constraint strings.
> Example:
> id,continuation_json
> ep_0123456789abcdef,"[""r03:e01"",""r07:e00.end|e04.start""]"
> ep_fedcba9876543210,"[""r02:e03|e06.start""]"
> Python serialization example:
> import json
> import pandas as pd
> with open("test.jsonl", encoding="utf-8") as handle:
> test = [json.loads(line) for line in handle if line.strip()]
> rows = []
> for episode in test:
> rows.append({
> "id": episode["id"],
> "continuation_json": json.dumps(["r00:e00"], separators=(",", ":")),
> })
> submission = pd.DataFrame(rows, columns=["id", "continuation_json"])
> getattr(submission, "to_" + "csv")("submission.csv", index=False)
> Compute Environment
> Submitted solutions run in a CPU-only environment with no GPU access. Internet access is disabled. The available CPU resources, memory, and time limit are shown by the challenge runner.
> Practical Starting Direction
> A useful starting system can encode primitive geometry as an entity graph, infer local relation-token behavior from the two supports, and decode query constraints with pointers to valid entities and endpoints. Constrained decoding can guarantee grammar validity. A stronger system should model both geometric compatibility and the document-specific ordering patterns demonstrated by the supports.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Drinov Orthography Safe Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c7vze6n8cgw96e43aw3tt158c045y
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Drinov Orthography Safe Repair
> Overview
> Historical newspaper OCR needs conservative repair. A system must correct scanning mistakes without silently modernizing authentic spelling. This challenge asks you to repair real OCR passages from nineteenth-century Bulgarian newspapers written in Drinov orthography.
> Every target was manually corrected by the source annotators. The source test documents are entire newspaper issues held apart from the numbered training documents. There is no generated corruption or synthetic text.
> The practical goal is archival search text that is more accurate while retaining historically meaningful glyphs such as Ñ£ and Ñ«. A model that copies every OCR passage leaves real errors unresolved; a model that aggressively rewrites the passage destroys evidence about the original orthography.
> Dataset
> File descriptions
> train.csv -- 1,076 labeled repair chunks from 149 source documents.
> test.csv -- 112 OCR chunks from 14 document-disjoint newspaper issues, without repaired text.
> sample_submission.csv -- Correctly formatted non-constant example text drawn deterministically from training targets.
> Column descriptions
> Columns in train.csv:
> id -- Opaque 14-character identifier for one source-document chunk.
> ocr_text -- Real OCR output, including historical spelling and recognition errors.
> repaired_text -- Manually corrected text that preserves the source orthography.
> Columns in test.csv:
> id -- Opaque 14-character identifier for one held-out chunk.
> ocr_text -- Real OCR output to repair.
> Evaluation
> Submissions are scored with the Conservative Orthography Repair Score:
> initial_error = levenshtein(ocr_text, repaired_text)
> remaining_error = levenshtein(prediction, repaired_text)
> introduced_edits = levenshtein(ocr_text, prediction)
> progress = initial_error - remaining_error
> repair_gain = clip(progress / max(initial_error, 1), 0, 1)
> safe_edit_precision = clip(progress / max(introduced_edits, 1), 0, 1)
> score = (
> 0.50 * mean(repair_gain)
> + 0.30 * mean(safe_edit_precision)
> + 0.20 * heritage_glyph_f1
> )
> repair_gain measures how much of the original OCR error was removed. safe_edit_precision penalizes changes that do not move the text toward the manual transcription. heritage_glyph_f1 is computed from position-aligned matches of the historical glyphs Ñ£Ñ«Ñ§Ñ­Ñ©Ñ¯Ñ±Ñ³Ñµ, so modernizing those characters loses credit. The score ranges from 0 to 1 and is maximized.
> Submission
> Submit a CSV containing:
> id -- Every test identifier exactly once.
> repaired_text -- One non-empty UTF-8 repair for the corresponding OCR passage.
> Example:
> id,repaired_text
> 8f8c19d85efc79,"- 344 - Ð¸Ð¼Ð°ÑˆÐµ Ð¿Ð¸ÑÐºÐ°, Ð¿Ð¾-Ð´ÐµÐ±ÐµÐ»Ð°..."
> 5b07f1cfa101f5,"ÐŸÑ€Ñ£Ð´Ð¸ Ð²ÑÐ¸Ñ‡ÐºÐ¾ Ñ‚Ñ€Ñ£Ð±Ð²Ð° Ð´Ð° ÑÐµ Ð¾Ñ‚Ð±Ñ£Ð»Ñ£Ð¶Ð¸..."
> Requirements
> Include exactly the columns id,repaired_text in that order.
> Preserve every test id; do not add, omit, or duplicate rows.
> Keep every prediction non-empty and valid UTF-8.
> Train a contextual sequence model from randomly initialized parameters on the labeled repair actions during the CPU run.
> Preserve historical orthography rather than converting it to modern Bulgarian.
> Use only files under ./dataset/public/ at solution time.
> Allowed methods
> Train byte-, character-, subword-, or mixed-granularity contextual sequence models from random initialization.
> Use train-only document-aware validation, class weighting, and deterministic ensembling.
> Learn confusion patterns as auxiliary features when a trained contextual model remains the main method.
> What Not To Use
> Do not use pretrained model weights, external copies of the source transcriptions, newspaper search, or answer lookup tables.
> Do not create synthetic corruptions, generated repair pairs, back-translations, or pseudo-labels.
> Do not modernize the target orthography with dictionaries or spelling converters.
> Do not submit a fixed confusion map or other rule-only/inference-only system as the main method.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Discourse-Entity Coherence Graph

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx728gd33dwy9fx2ejbse9sfy988f1wb
- DOMAIN exactly as displayed: From Scratch
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
> Each row centers on one focus sentence plus up to two neighboring sentences on each side from a real document. The public view preserves sentence offsets, token order, repeated token identity, mention spans, and local token indices, but the lexical surface is deterministically obfuscated to reduce direct source lookup. Your job is to predict the labeled mention, discourse, connective, and transition relationships that form one internally consistent local graph for the focus sentence.
> The scored graph has five interacting parts:
> focus-sentence mention labels: entity_type and information_status
> local entity-continuity edges between mention ids
> eRST rhetorical attachments from focus-sentence tokens
> PDTB connective senses from focus-sentence tokens
> the centering transition label for the focus sentence
> This is a structured prediction task, not five unrelated classifiers. Strong submissions use the local interaction between mention identity, discourse structure, connective cues, and transition state.
> Task
> For each test id, submit one JSON object in prediction_json with exactly these top-level keys:
> mentions
> continuity
> erst
> pdtb
> transition
> mentions is a list of objects with exactly id, entity_type, and information_status.
> continuity is a list of objects with exactly source, target, and relation.
> erst is a list of objects with exactly source_token, target_offset, target_token, and relation. If the rhetorical parent falls outside the visible window, use "target_offset":"outside" and "target_token":0.
> pdtb is a list of objects with exactly source_token, connective_type, and sense.
> transition is one label from the public inventory.
> The public files expose only local mention candidates and local token indices. Every predicted mention id must come from that row's mentions_json.
> Intended Approach
> Treat this as a CPU-capable NLP structured prediction challenge for discourse parsing, entity graph recovery, and local coherence modeling. It is a from-scratch modeling task, not a computer vision, audio, tabular regression, or fine-tuning benchmark. Strong solutions can be built entirely from the public training files with offline from-scratch modeling.
> Useful approaches include:
> compact token or character encoders trained from random initialization on the obfuscated token stream
> mention-aware sequence tagging or span scoring for the focus sentence
> graph decoders or constrained structured prediction over mention ids and token indices
> multi-head training that shares one encoder across mention, continuity, eRST, PDTB, and transition heads
> rule-based validity checks during decoding so ids, offsets, and token references remain legal
> CPU-friendly baselines such as sparse lexical features, linear models, CRF-style decoding, or compact neural encoders are all valid. The intended difficulty comes from jointly recovering several coherent annotation layers, not from hidden APIs or heavy infrastructure.
> From-scratch path: initialize a compact model randomly and train it only on public/train.csv, label_inventory.json, and the public row-local JSON fields. The dataset is small enough for repeated CPU validation runs, and learning the task-specific discourse/entity representation is the central challenge.
> Fine-tuning path: this challenge is not intended as a fine-tuning benchmark. Pretrained weights, pretrained embeddings, external fine-tuned checkpoints, external corpora, hosted APIs, and runtime downloads are not allowed.
> What Not To Use
> Do not use:
> pretrained weights, pretrained embeddings, or external fine-tuned checkpoints
> external corpora, APIs, retrieval systems, or manual source reconstruction
> hard-coded test ids, hidden-label dictionaries, grader exploits, or malformed-file probing
> private files, answer leakage, or adaptation to withheld-label feedback
> hosted inference services or methods that cannot run within the stated offline CPU budget
> Submissions built around source lookup, metadata shortcuts, hard-coded ids, or grader abuse can be rejected even if they produce a numeric score.
> Evaluation
> The theoretical minimum is 0.0 and the theoretical maximum is 1.0. A perfect valid submission scores exactly 1.0.
> For each row, the grader first parses prediction_json. If the JSON is malformed or violates the row-local schema, that row receives 0.0. Otherwise, the grader computes these component scores:
> mentions F1 with weight 0.22: compare sets of (id, entity_type, information_status) tuples.
> continuity F1 with weight 0.18: compare sets of (source, target, relation) tuples.
> eRST endpoint F1 with weight 0.12: compare sets of (source_token, target_offset, target_token) tuples, ignoring the relation label.
> eRST labeled-edge F1 with weight 0.15: compare sets of (source_token, target_offset, target_token, relation) tuples.
> PDTB labeled sense F1 with weight 0.12: compare sets of (source_token, connective_type, sense) tuples.
> transition accuracy with weight 0.10: 1.0 if the predicted transition exactly equals the gold transition, else 0.0.
> exact full-graph match with weight 0.06: 1.0 only if the complete parsed prediction object exactly equals the gold object, else 0.0.
> confidence calibration with weight 0.05: 1.0 - abs(confidence - quality), where quality is the unweighted mean of the row's semantic component scores before adding confidence calibration.
> For any F1 component:
> precision = true_positives / predicted_count
> recall = true_positives / gold_count
> f1 = 2  *precision*  recall / (precision + recall)
> If both the predicted and gold sets for a list component are empty, that component is skipped for that row rather than treated as an automatic point. If exactly one side is empty, its F1 is 0.0.
> The component weights are not additive bonuses on top of another score. They form a weighted average:
> row_score = sum(component_weight * component_value) / sum(included_component_weights)
> The row score is clipped to [0.0, 1.0] as a safety guard.
> The final submission score is:
> final = 0.90  *mean_row_score + 0.10*  worst_genre_mean
> Whole-file structural failures raise InvalidSubmissionError. This includes wrong, missing, extra, or reordered columns; blank, duplicate, missing, or foreign ids; and non-finite or out-of-range confidence values. Row-local malformed prediction_json content does not crash the submission; that row simply receives zero credit.
> Dataset
> The prepared release contains 3816 training rows and 1067 test rows built from 113 commercially usable documents across six genres: academic, biography, court, interview, news, and voyage.
> Prepared data is provided to solvers under public/.
> File Overview
> | Item | Description |
> |---|---|
> | train.csv | 3816 training rows with opaque ids, local sentence windows, mention candidates, and train-only target graphs |
> | test.csv | 1067 test rows with opaque ids, local sentence windows, and mention candidates only |
> | sample_submission.csv | Format-valid weak prior submission with one row per test id |
> | label_inventory.json | Allowed entity, information-status, continuity, eRST, PDTB, and transition labels observed in training |
> train.csv Columns
> | Column | Type | Meaning |
> |---|---|---|
> | id | string | Opaque public row identifier |
> | context_json | JSON string | Local sentence window with offsets -2 through 2 and obfuscated token lists |
> | mentions_json | JSON string | Local mention candidates with mention id, sentence offset, token span, and obfuscated mention text |
> | answer_json | JSON string | Train-only target graph containing mention labels, continuity edges, eRST edges, PDTB senses, and transition label |
> test.csv Columns
> | Column | Type | Meaning |
> |---|---|---|
> | id | string | Opaque public row identifier |
> | context_json | JSON string | Local sentence window with offsets -2 through 2 and obfuscated token lists |
> | mentions_json | JSON string | Local mention candidates with mention id, sentence offset, token span, and obfuscated mention text |
> There are no target columns in test.csv.
> Target Object
> | Target field | Type | Meaning |
> |---|---|---|
> | mentions | list of objects | Focus-sentence mention labels with id, entity_type, and information_status |
> | continuity | list of objects | Local entity-continuity edges with source, target, and relation |
> | erst | list of objects | eRST rhetorical attachments with source_token, target_offset, target_token, and relation |
> | pdtb | list of objects | PDTB connective predictions with source_token, connective_type, and sense |
> | transition | string enum | Centering transition label from label_inventory.json |
> Submission
> Submit submission.csv with exactly these columns in exactly this order:
> id
> prediction_json
> confidence
> confidence must be a finite float in [0, 1]. The row order does not matter. The id set must match the test set exactly.
> Submission Columns
> | Column | Type | Constraint |
> |---|---|---|
> | id | string | Exact same ID set as test.csv, with no missing, extra, duplicate, blank, or foreign IDs |
> | prediction_json | JSON string | One graph object with exactly mentions, continuity, erst, pdtb, and transition |
> | confidence | float | Finite value in [0, 1] |
> First five rows from sample_submission.csv:
> id,prediction_json,confidence
> r_0004db253dc6e5ac,"{""mentions"":[],""continuity"":[],""erst"":[],""pdtb"":[],""transition"":""UNKNOWN""}",0.0
> r_01009cc8a6506e59,"{""mentions"":[],""continuity"":[],""erst"":[],""pdtb"":[],""transition"":""UNKNOWN""}",0.0
> r_01114a34ecf84831,"{""mentions"":[],""continuity"":[],""erst"":[],""pdtb"":[],""transition"":""UNKNOWN""}",0.0
> r_017f7b0c5e2b9291,"{""mentions"":[],""continuity"":[],""erst"":[],""pdtb"":[],""transition"":""UNKNOWN""}",0.0
> r_01872497e136f27f,"{""mentions"":[],""continuity"":[],""erst"":[],""pdtb"":[],""transition"":""UNKNOWN""}",0.0
> Compute
> This bundle is currently configured for offline CPU execution:
> up to 10 CPU cores
> up to 62 GB RAM
> 90 minutes total runtime
> no network access

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Worker Hand Trajectory Program

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7c72x2f2qbza2z1cx35ghs5h8c2w06
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Background
> Tracking and reconstructing 3-D human hand motion from visual streams is a core challenge in human-robot interaction, industrial ergonomics, and automated activity analysis. While physical motion capture setups rely on intrusive markers or specialized sensor arrays, video-based perception systems must deduce 3-D spatial movement directly from visual frame sequences.
> Reconstructing continuous spatial hand trajectories from sampled RGB frame strips requires translating temporal visual cues into structured, run-length encoded 3-D motion programs. By parameterizing 3-D movement vectors into discretized spatial directions, velocity bands, and rotational changes, models can compact continuous physical trajectories into inspectable, symbolic motion sequences.
> Overview
> The Worker Hand Trajectory Program challenge is a from-scratch video-to-sequence reconstruction task. Given an input RGB frame strip sampled across a physical hand movement, models must infer and reconstruct the chronologically ordered 3-D trajectory motion program.
> Each step in the predicted trajectory program corresponds to a contiguous segment defined by four attributes:
> dir3: Discretized 3-D spatial movement vector (e.g., "X+Y0Z-").
> speed: Quantized speed / velocity band (e.g., "Q2").
> turn: Quantized rotational change / turn band (e.g., "T1").
> run: Run length / duration across frames.
> Execution Constraints & Limits
> Compute Budget: 10 CPU cores
> Memory Limit: 62 GB RAM
> Wall-Clock Time Limit: 5,400 seconds (1.5 hours) for complete end-to-end execution (training + test inference).
> Hardware Envelope: Strictly CPU execution (no GPU/accelerator access).
> Network: Disabled during execution.
> Dataset Description
> The public dataset comprises CSV files containing metadata and serialized JSON payloads, paired with a media/ directory containing image assets (RGB frame strips).
> Data splitting is strictly group-aware based on contiguous capture blocks to mitigate data leakage between training and testing splits. Unique identifiers are anonymized with a wht09_ prefix.
> Public Files & Directory Structure
> train.csv: Public training dataset containing opaque row IDs, serialized input JSON objects (with media references), and ground-truth trajectory programs.
> test.csv: Evaluation dataset containing opaque row IDs and serialized input JSON objects for inference.
> sample_submission.csv: Submission template containing test IDs and default empty payload predictions ({"trajectory_program":[]}).
> DATA_MANIFEST.json: Dataset manifest recording train/test row counts, payload column names, and media file counts.
> media/: Directory containing image frame strip files referenced in input_json.media_files.
> Public File Schemas & Data Types
> Plaintext
> +-----------------------+-------------------------+------------------------+-------------------------------------------------------------------------+
> | File                  | Column                  | Data Type              | Description                                                             |
> +-----------------------+-------------------------+------------------------+-------------------------------------------------------------------------+
> | train.csv             | id                      | Opaque UTF-8 string    | Unique identifier for the train sample (e.g., wht09_012345...).         |
> | train.csv             | input_json              | Serialized JSON object | Input metadata containing array of relative media file paths.           |
> | train.csv             | trajectory_program_json | Serialized JSON object | Target ground-truth 3-D trajectory motion program.                      |
> | test.csv              | id                      | Opaque UTF-8 string    | Unique opaque identifier for the test sample.                           |
> | test.csv              | input_json              | Serialized JSON object | Input metadata containing array of relative media file paths.           |
> | sample_submission.csv | id                      | Opaque UTF-8 string    | Unique identifier corresponding to test example.                        |
> | sample_submission.csv | trajectory_program_json | Serialized JSON object | Predicted 3-D trajectory motion program payload.                        |
> +-----------------------+-------------------------+------------------------+-------------------------------------------------------------------------+
> JSON Structure Definitions
> Input JSON Schema (input_json)
> JSON
> {
> "media_files": [
> "media/wht09_0123456789abcdef_0.png"
> ]
> }
> media_files (array of strings): Array of relative paths pointing to the RGB frame strip image files under media/.
> Target JSON Schema (trajectory_program_json)
> JSON
> {
> "trajectory_program": [
> {
> "dir3": "X+Y0Z-",
> "speed": "Q2",
> "turn": "T1",
> "run": 2
> }
> ]
> }
> trajectory_program (array of objects): Chronologically ordered list of 3-D trajectory segments. Each object contains:
> dir3 (string): 3-D movement direction vector representation.
> speed (string): Quantized speed/velocity level.
> turn (string): Quantized angular/rotational change level.
> run (number): Segment run length / step duration.
> Evaluation Metrics
> Predictions are evaluated row by row against ground-truth targets. The final leaderboard score is the unweighted arithmetic mean of individual row scores, strictly clamped to [0, 1].
> For candidate step sequence
> ð‘ƒ
> P and ground-truth step sequence
> ðº
> G, each step is represented as a 3-attribute token tuple
> ð‘¡
> =
> (
> dir3
> ,
> speed
> ,
> turn
> )
> t=(dir3,speed,turn). Let
> ð‘ƒ
> tok
> P
> tok
> â€‹
> and
> ðº
> tok
> G
> tok
> â€‹
> denote the ordered lists of 3-D token tuples.
> The row score is computed as a weighted combination of four metric components:
> 1. Ordered 3-D Token LCS-F1 (
> ð¹
> 1
> LCS
> F1
> LCS
> â€‹
> , Weight: 55%)
> Evaluates the sequential alignment of predicted 3-D token tuples against ground truth using Longest Common Subsequence (LCS) F1:
> ð¹
> 1
> LCS
> (
> ð‘ƒ
> tok
> ,
> ðº
> tok
> )
> =
> {
> 1.0
> if
> âˆ£
> ð‘ƒ
> tok
> âˆ£
> =
> 0
> and
> âˆ£
> ðº
> tok
> âˆ£
> =
> 0
> 2
> Ã—
> ð¿
> ð¶
> ð‘†
> (
> ð‘ƒ
> tok
> ,
> ðº
> tok
> )
> âˆ£
> ð‘ƒ
> tok
> âˆ£
> +
> âˆ£
> ðº
> tok
> âˆ£
> otherwise
> F1
> LCS
> â€‹
> (P
> tok
> â€‹
> ,G
> tok
> â€‹
> )={
> 1.0
> âˆ£P
> tok
> â€‹
> âˆ£+âˆ£G
> tok
> â€‹
> âˆ£
> 2Ã—LCS(P
> tok
> â€‹
> ,G
> tok
> â€‹
> )
> â€‹
> â€‹
> ifÂ âˆ£P
> tok
> â€‹
> âˆ£=0Â andÂ âˆ£G
> tok
> â€‹
> âˆ£=0
> otherwise
> â€‹
> 2. Token Multiset F1 (
> ð¹
> 1
> multiset
> F1
> multiset
> â€‹
> , Weight: 25%)
> Evaluates token tuple overlap regardless of sequence position using multiset F1:
> ð¹
> 1
> multiset
> (
> ð‘ƒ
> tok
> ,
> ðº
> tok
> )
> =
> 2
> âˆ‘
> ð‘¡
> min
> â¡
> (
> count
> ð‘ƒ
> (
> ð‘¡
> )
> ,
> count
> ðº
> (
> ð‘¡
> )
> )
> âˆ£
> ð‘ƒ
> tok
> âˆ£
> +
> âˆ£
> ðº
> tok
> âˆ£
> F1
> multiset
> â€‹
> (P
> tok
> â€‹
> ,G
> tok
> â€‹
> )=
> âˆ£P
> tok
> â€‹
> âˆ£+âˆ£G
> tok
> â€‹
> âˆ£
> 2âˆ‘
> t
> â€‹
> min(count
> P
> â€‹
> (t),count
> G
> â€‹
> (t))
> â€‹
> 3. Run-Length Similarity (
> ð‘†
> run
> S
> run
> â€‹
> , Weight: 15%)
> Measures the agreement of step run values across aligned positions
> ð‘–
> âˆˆ
> [
> 0
> ,
> min
> â¡
> (
> âˆ£
> ð‘ƒ
> âˆ£
> ,
> âˆ£
> ðº
> âˆ£
> )
> âˆ’
> 1
> ]
> iâˆˆ[0,min(âˆ£Pâˆ£,âˆ£Gâˆ£)âˆ’1]:
> ð‘†
> run
> =
> 1
> max
> â¡
> (
> âˆ£
> ð‘ƒ
> âˆ£
> ,
> âˆ£
> ðº
> âˆ£
> ,
> 1
> )
> âˆ‘
> ð‘–
> =
> 0
> min
> â¡
> (
> âˆ£
> ð‘ƒ
> âˆ£
> ,
> âˆ£
> ðº
> âˆ£
> )
> âˆ’
> 1
> min
> â¡
> (
> ð‘Ÿ
> ð‘ƒ
> ,
> ð‘–
> ,
> ð‘Ÿ
> ðº
> ,
> ð‘–
> )
> max
> â¡
> (
> ð‘Ÿ
> ð‘ƒ
> ,
> ð‘–
> ,
> ð‘Ÿ
> ðº
> ,
> ð‘–
> ,
> 1
> )
> S
> run
> â€‹
> =
> max(âˆ£Pâˆ£,âˆ£Gâˆ£,1)
> 1
> â€‹
> âˆ‘
> i=0
> min(âˆ£Pâˆ£,âˆ£Gâˆ£)âˆ’1
> â€‹
> max(r
> P,i
> â€‹
> ,r
> G,i
> â€‹
> ,1)
> min(r
> P,i
> â€‹
> ,r
> G,i
> â€‹
> )
> â€‹
> 4. Program Length Score (
> ð‘†
> len
> S
> len
> â€‹
> , Weight: 5%)
> Measures sequence length agreement between predicted step count
> âˆ£
> ð‘ƒ
> âˆ£
> âˆ£Pâˆ£ and ground-truth step count
> âˆ£
> ðº
> âˆ£
> âˆ£Gâˆ£:
> ð‘†
> len
> =
> {
> 1.0
> if
> âˆ£
> ð‘ƒ
> âˆ£
> =
> âˆ£
> ðº
> âˆ£
> max
> â¡
> (
> 0.0
> ,
> 1.0
> âˆ’
> âˆ£
> âˆ£
> ð‘ƒ
> âˆ£
> âˆ’
> âˆ£
> ðº
> âˆ£
> âˆ£
> max
> â¡
> (
> 1
> ,
> âˆ£
> ð‘ƒ
> âˆ£
> ,
> âˆ£
> ðº
> âˆ£
> )
> )
> otherwise
> S
> len
> â€‹
> ={
> 1.0
> max(0.0,1.0âˆ’
> max(1,âˆ£Pâˆ£,âˆ£Gâˆ£)
> âˆ£âˆ£Pâˆ£âˆ’âˆ£Gâˆ£âˆ£
> â€‹
> )
> â€‹
> ifÂ âˆ£Pâˆ£=âˆ£Gâˆ£
> otherwise
> â€‹
> Total Row Score Formula
> RowÂ Score
> =
> 0.55
> â‹…
> ð¹
> 1
> LCS
> +
> 0.25
> â‹…
> ð¹
> 1
> multiset
> +
> 0.15
> â‹…
> ð‘†
> run
> +
> 0.05
> â‹…
> ð‘†
> len
> RowÂ Score=0.55â‹…F1
> LCS
> â€‹
> +0.25â‹…F1
> multiset
> â€‹
> +0.15â‹…S
> run
> â€‹
> +0.05â‹…S
> len
> â€‹
> Additional Rules
> Exact byte-for-byte semantic matches score 1.0.
> Syntactically invalid JSON payloads, missing keys, or malformed structures receive a score of 0.0 for that row.
> Sample Submission Format
> Submit a UTF-8 CSV file with exactly two columns in this order: id, trajectory_program_json.
> Code snippet
> id,trajectory_program_json
> wht09_0123456789abcdef,"{""trajectory_program"":[{""dir3"":""X+Y0Z-"",""speed"":""Q2"",""turn"":""T1"",""run"":2}]}"
> Every test id must appear exactly once.
> Extra, missing, or duplicate id rows will invalidate the entire submission.
> Row order is unrestricted, but column headers must match sample_submission.csv exactly.
> What Not To Use
> Pretrained Models & Weights: Solutions must train a model from scratch using only the supplied train.csv and media/ assets. Using pretrained vision, video, OCR, or multimodal backbones is strictly prohibited.
> External Data & Lookups: Network access, external datasets, web downloads, and private data lookup are forbidden.
> Test Adaptation: Pseudo-labeling test data, test-time training adaptation, or hardcoding predictions based on test IDs or metadata is prohibited.
> GPU Execution: GPU acceleration is disabled. Solutions must execute entirely on 10 CPU cores within the 5,400-second wall-clock limit.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Lichess Tactical Line Bundle Challenge

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx750r2d52y15k05qxz736fexn8azjj0
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> Background
> Tactical evaluation and continuation prediction are fundamental problems in automated reasoning and game AI. In chess, tactical positions require calculating concrete, forced lines of play where a single suboptimal move invalidates the entire variation. Beyond calculating move lines, identifying the underlying tactical motifsâ€”such as forks, pins, skewers, and multi-ply checkmatesâ€”requires recognizing abstract positional and functional patterns across pieces.
> This challenge presents a from-scratch structured sequence-and-set reconstruction task. Rather than framing chess as a simplified win/loss outcome classification or single-move prediction task, models must reconstruct the complete target tactical move sequence following a setup move and correctly classify the set of native tactical themes that characterize the position.
> Overview
> Given an initial board state in Forsythâ€“Edwards Notation (FEN) and an opponent's initial setup move in Universal Chess Interface (UCI) notation, the primary goal is to predict:
> Target Move Line (moves): The exact sequence of forced continuation moves (2 to 9 plies) in UCI format.
> Tactical Motif Set (themes): The set of native tactical tags describing the tactical patterns in the variation.
> Confidence Score (confidence): A calibrated float value in
> [
> 0
> ,
> 1
> ]
> [0,1] estimating the reliability of the predicted move sequence.
> All learned evaluation functions, move-ranking heuristics, and motif classifiers must be fitted strictly from the provided training data without relying on pre-trained engines or external chess databases.
> Dataset Information
> The benchmark consists of structured tabular files containing chess tactical scenarios split into training and evaluation sets.
> File Manifest
> train.csv: Contains tactical scenario inputs along with ground-truth continuations and theme labels (answer_json).
> test.csv: Contains tactical scenario inputs for evaluation. Ground-truth continuations and themes are withheld.
> sample_submission.csv: Demonstrates the exact format required for submission.
> Schema & Column Specification
> Inputs (train.csv and test.csv)
> +------------------+--------------------+-----------------------+--------------------------------------------------------------------------------------------------------+
> | Column Name      | Data Type          | Field Type            | Description                                                                                            |
> +------------------+--------------------+-----------------------+--------------------------------------------------------------------------------------------------------+
> | id               | String             | Metadata              | Unique, opaque row identifier for each tactical scenario.                                              |
> | fen              | String             | Input                 | Forsythâ€“Edwards Notation (FEN) string representing the board state prior to the setup move.            |
> | setup_move       | String             | Input                 | The opponent's initial setup move in UCI format (e.g., e2e4) that triggers the tactical sequence.      |
> | solution_plies   | Integer / String   | Input                 | Target length of the forced tactical continuation sequence (number of half-moves, bounded between 2 and 9). |
> | rating_band      | String             | Input                 | Categorical difficulty rating range for the position (e.g., 1400-1599).                                |
> | answer_json      | String (JSON)      | Target (train only)   | JSON string containing ground-truth targets: {"moves": [...], "themes": [...]}.                        |
> +------------------+--------------------+-----------------------+--------------------------------------------------------------------------------------------------------+
> Submission Format (sample_submission.csv)
> +-----------------+---------------+------------+--------------------------------------------------------------------------------------------------------------+
> | Column Name     | Data Type     | Field Type | Description                                                                                                  |
> +-----------------+---------------+------------+--------------------------------------------------------------------------------------------------------------+
> | id              | String        | Metadata   | Unique scenario identifier corresponding to test.csv.                                                        |
> | prediction_json | String (JSON) | Prediction | Formatted JSON string containing predicted move sequence and themes: {"moves": [...], "themes": [...]}.      |
> | confidence      | Float         | Prediction | Numerical score in [0, 1] reflecting model confidence in the predicted move line.                            |
> +-----------------+---------------+------------+--------------------------------------------------------------------------------------------------------------+
> Evaluation Metrics
> Submissions are evaluated row-by-row using a composite scoring function that balances move sequence precision, prefix matching, motif classification, exact bundle alignment, and confidence calibration.
> 1. Row-Level Score Calculation
> For each row
> ð‘–
> i, the predicted object
> ð‘ƒ
> =
> moves
> ,
> themes
> P=moves,themes and confidence
> ð‘
> âˆˆ
> [
> 0
> ,
> 1
> ]
> câˆˆ[0,1] are compared against ground truth
> ðº
> =
> moves
> ,
> themes
> G=moves,themes:
> RowÂ Score
> âˆ—
> ð‘–
> =
> 0.50
> â‹…
> ð‘†
> âˆ—
> LCSF1
> +
> 0.20
> â‹…
> ð‘†
> Prefix
> +
> 0.20
> â‹…
> ð‘†
> ThemeF1
> +
> 0.05
> â‹…
> ð‘†
> Exact
> +
> 0.05
> â‹…
> ð‘†
> Calib
> RowÂ Scoreâˆ—i=0.50â‹…Sâˆ—LCSF1+0.20â‹…S
> Prefix
> â€‹
> +0.20â‹…S
> ThemeF1
> â€‹
> +0.05â‹…S
> Exact
> â€‹
> +0.05â‹…S
> Calib
> â€‹
> Where:
> Longest Common Subsequence F1 (
> ð‘†
> LCSF1
> S
> LCSF1
> â€‹
> ):
> ð‘†
> LCSF1
> =
> 2
> â‹…
> LCS
> (
> ð‘ƒ
> moves
> ,
> ðº
> moves
> )
> âˆ£
> ð‘ƒ
> moves
> âˆ£
> +
> âˆ£
> ðº
> moves
> âˆ£
> S
> LCSF1
> â€‹
> =
> âˆ£P
> moves
> â€‹
> âˆ£+âˆ£G
> moves
> â€‹
> âˆ£
> 2â‹…LCS(P
> moves
> â€‹
> ,G
> moves
> â€‹
> )
> â€‹
> Exact-Prefix Coverage (
> ð‘†
> Prefix
> S
> Prefix
> â€‹
> ): Fraction of consecutive matching moves from the start of the sequence:
> ð‘†
> Prefix
> =
> lengthÂ ofÂ initialÂ exactÂ moveÂ prefixÂ match
> max
> â¡
> (
> âˆ£
> ðº
> moves
> âˆ£
> ,
> âˆ£
> ð‘ƒ
> moves
> âˆ£
> ,
> 1
> )
> S
> Prefix
> â€‹
> =
> max(âˆ£G
> moves
> â€‹
> âˆ£,âˆ£P
> moves
> â€‹
> âˆ£,1)
> lengthÂ ofÂ initialÂ exactÂ moveÂ prefixÂ match
> â€‹
> Theme Set F1 (
> ð‘†
> ThemeF1
> S
> ThemeF1
> â€‹
> ): Harmonic mean of precision and recall over predicted theme sets:
> ð‘†
> ThemeF1
> =
> 2
> â‹…
> âˆ£
> ð‘ƒ
> themes
> âˆ©
> ðº
> themes
> âˆ£
> âˆ£
> ð‘ƒ
> themes
> âˆ£
> +
> âˆ£
> ðº
> themes
> âˆ£
> S
> ThemeF1
> â€‹
> =
> âˆ£P
> themes
> â€‹
> âˆ£+âˆ£G
> themes
> â€‹
> âˆ£
> 2â‹…âˆ£P
> themes
> â€‹
> âˆ©G
> themes
> â€‹
> âˆ£
> â€‹
> Exact Bundle Match (
> ð‘†
> Exact
> S
> Exact
> â€‹
> ): Binary indicator equal to
> 1.0
> 1.0 if
> ð‘ƒ
> moves
> =
> =
> ðº
> moves
> P
> moves
> â€‹
> ==G
> moves
> â€‹
> and
> ð‘ƒ
> themes
> =
> =
> ðº
> themes
> P
> themes
> â€‹
> ==G
> themes
> â€‹
> , otherwise
> 0.0
> 0.0.
> Confidence Calibration (
> ð‘†
> Calib
> S
> Calib
> â€‹
> ): Rewards accurate self-assessment of move sequence accuracy:
> ð‘†
> Calib
> =
> 1.0
> âˆ’
> âˆ£
> ð‘
> âˆ’
> ð‘†
> LCSF1
> âˆ£
> S
> Calib
> â€‹
> =1.0âˆ’âˆ£câˆ’S
> LCSF1
> â€‹
> âˆ£
> Note: Malformed JSON strings, invalid move syntaxes, non-unique theme lists, or out-of-bound confidence values (
> ð‘
> âˆ‰
> [
> 0
> ,
> 1
> ]
> câˆˆ
> /
> [0,1]) result in a score of
> 0.0
> 0.0 for that row.
> 2. Final Composite Score
> The final benchmark score combines overall performance across all test scenarios with worst-case performance across hidden theme groups:
> FinalÂ Score
> =
> 0.90
> Ã—
> ð‘†
> â€¾
> âˆ—
> all
> +
> 0.10
> Ã—
> min
> â¡
> âˆ—
> ð‘”
> âˆˆ
> Groups
> (
> ð‘†
> â€¾
> ð‘”
> )
> FinalÂ Score=0.90Ã—
> S
> âˆ—all+0.10Ã—minâˆ—gâˆˆGroups(
> S
> g
> â€‹
> )
> ð‘†
> â€¾
> all
> S
> all
> â€‹
> is the arithmetic mean score across all test rows.
> ð‘†
> â€¾
> ð‘”
> S
> g
> â€‹
> is the mean score within hidden evaluation group
> ð‘”
> g.
> Scoring is bounded between
> 0.0
> 0.0 and
> 1.0
> 1.0.
> Sample Submission Format
> Predictions must be submitted in CSV format with three columns: id, prediction_json, and confidence.
> id,prediction_json,confidence
> c_001a2b3c4d5e6f7g,"{""moves"":[""e2e4"",""e7e5""],""themes"":[""fork"",""short""]}",0.85
> c_123b4c5d6e7f8g9h,"{""moves"":[""g1f3"",""d7d5"",""c2c4""],""themes"":[""advantage"",""middlegame""]}",0.62
> JSON Prediction Object Rules
> moves: Ordered list of valid UCI move strings (e.g., ["e2e4", "e7e5"]). Max 20 moves.
> themes: List of unique theme identifier strings (e.g., ["fork", "pin"]). Max 60 themes per row. No duplicate strings allowed within a single list.
> confidence: Finite numeric value in
> [
> 0
> ,
> 1
> ]
> [0,1].
> Constraints and Rules (What Not to Use / Do)
> To ensure a fair comparison focused on learning tactical representations directly from provided data:
> No Pretrained Models or Engines: Do not use pre-trained chess neural networks (e.g., LCZero, Maya), engine executables (e.g., Stockfish, Komodo), or third-party chess API services.
> No External Data: External chess corpora, opening books, endgame tablebases, puzzle databases, or web scraping are strictly prohibited.
> No Ground Truth/Source Lookups: Do not attempt to look up game positions, source URLs, or original puzzle identifiers.
> Allowed Custom Logic: Participants are permitted to implement custom move-generation legal checkers, board representations, and search algorithms from scratch. However, all learned weights, evaluation metrics, and pattern probabilities must be derived solely from the provided train.csv.
> Execution & Hardware Bounding: Solutions must execute offline within a maximum runtime of 90 minutes using up to 10 CPU cores and 62 GB RAM. No GPU acceleration is available or permitted during evaluation.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## TraceBound: Source-Aligned Statement Decomposition

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7795mb5nmbp18f9pgwsvexvn88e5p5
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> # TraceBound: Source-Aligned Statement Decomposition
> Overview
> Given one long factual sentence, rewrite it as two or more shorter sentences with the same meaning. For every output token, also predict either the source-token position it copies or -1 when it introduces new wording.
> The dataset is a licensed, curated collection of encyclopedia-derived sentence edits spanning people, places, events, organizations, creative works, science, history, and culture. Each usable example pairs one dense factual sentence with human-authored shorter reference sentences. Organizer preparation filters for strong meaning preservation and derives the token links through deterministic monotonic matching between the source and reference text; source names and raw identifiers are not part of the participant files.
> The task models traceable editing for knowledge bases and technical reference material, where each concise statement must retain the source facts, their order, and an inspectable link to the original wording.
> Every generated token must carry either the zero-based position of the source token it copies or -1 when the wording is inserted or rewritten. The statement list also records where the dense source is decomposed. Fluent text alone is insufficient: the output must jointly preserve content order, choose useful statement boundaries, and expose the copy/insert evidence behind the wording.
> This is a CPU-only, from-scratch structured NLP transduction task. It is not ordinary text classification, unconstrained paraphrase generation, or a pretrained-model benchmark.
> Task
> For each test id, encode the complete decomposition and provenance trace as one JSON object in prediction_json. The object must have exactly these top-level keys:
> sentences
> alignments
> sentences is a list of 1 to 8 nonempty strings. The gold targets always contain at least 2 simpler sentences, but the grader accepts any valid 1 to 8 sentence prediction.
> alignments is a list with the same length as sentences. Each inner alignment list must contain exactly one integer for each token in the corresponding output sentence.
> Alignment values have this meaning:
> -1 means the output token is an insertion or rewrite.
> Any nonnegative integer is a zero-based source-token index.
> A copied token must match the referenced source token case-insensitively under the grader tokenizer.
> Copied source indices must be nondecreasing within each output sentence.
> The grader normalizes text with Unicode NFKC and whitespace collapse, then tokenizes with:
> \w+(?:['â€™]\w+)?|[^\w\s]
> Predictions may contain at most 400 output tokens and 250,000 UTF-8 bytes of serialized JSON.
> Intended Approach
> Treat this as constrained sequence transduction with four coupled decisions: content preservation, statement-boundary placement, source-token copying, and insertion/rewrite detection. Strong solutions can be trained from random initialization using only the public training files and offline CPU execution.
> Useful approaches include:
> a compact randomly initialized encoder-decoder or monotonic edit transducer
> tokenizers and insertion vocabularies learned only from train.csv
> a pointer head over source positions paired with an insertion/rewrite head
> a boundary head or constrained decoder for the ordered statement list
> joint decoding or reranking that rewards textual faithfulness and legal provenance links
> validation during decoding so JSON shape, token counts, and copy indices remain legal
> All learned parameters, embeddings, tokenizers, and features must be initialized or learned from the released public training split only.
> What Not To Use
> Do not use:
> pretrained or frozen language models, checkpoints, adapters, embeddings, or representations
> external text, paraphrase corpora, dictionaries, synthetic examples, or organizer-only raw files
> hosted inference, remote APIs, network downloads, or internet access
> hard-coded test ids, hidden-label dictionaries, private files, source lookup, or grader/platform exploitation
> Submissions built around lookup, metadata shortcuts, source reconstruction, or malformed-file probing can be rejected even if they produce a numeric score.
> Evaluation
> The metric is the TraceBound structure-gated evidence score.
> The theoretical minimum is 0.0 and the theoretical maximum is 1.0. A perfect valid prediction for every row scores exactly 1.0.
> For each row, the grader first parses and validates prediction_json. If the row JSON is malformed or violates the row-local schema, that row receives 0.0. Whole-file structural failures raise InvalidSubmissionError; this includes wrong, missing, extra, or reordered columns; missing rows; extra rows; duplicate ids; or foreign ids.
> An exact canonical text-and-alignment object receives row score 1.0. Every other valid row first receives this evidence score:
> evidence_score =
> 0.50 * content_order_ratio
> + 0.33 * copy_alignment_edge_F1
> + 0.17 * insertion_edge_F1
> row_score = evidence_score * split_structure_score
> The three evidence weights sum to 1.00. The separate structure multiplier ensures that copying most of the source without recovering its statement decomposition cannot receive generous partial credit. Exact canonical recovery receives 1.0 through the explicit exact branch.
> Component definitions:
> content_order_ratio is the SequenceMatcher ratio between the predicted and gold output-token sequences after case folding.
> split_structure_score is the average of sentence_count_similarity and boundary_F1, computed as 0.5 x sentence_count_similarity + 0.5 x boundary_F1.
> sentence_count_similarity is 1 - abs(predicted_sentence_count - gold_sentence_count) / max(predicted_sentence_count, gold_sentence_count, 1).
> boundary_F1 compares cumulative output-token boundary positions between predicted and gold sentence lists.
> copy_alignment_edge_F1 compares multisets of (sentence_index, token_position, source_index) for copied tokens.
> insertion_edge_F1 compares multisets of (sentence_index, token_position, token_text) for insertion or rewrite tokens.
> For each F1 component:
> precision = overlap_count / predicted_count
> recall = overlap_count / gold_count
> F1 = 2  *precision*  recall / (precision + recall)
> If both compared multisets are empty, that F1 component is 1.0. If exactly one side is empty, it is 0.0.
> The final submission score is the mean row score over all test rows:
> final_score = mean(row_score)
> Scores are clipped to [0.0, 1.0] as a safety guard.
> Dataset
> The prepared release contains 47,051 training rows and 11,611 hidden test rows selected from 58,662 usable unique high-entailment examples. The split is grouped by a normalized, label-free source-template signature so near-template families do not cross train and test.
> Prepared data is provided under public/.
> File overview:
> train.csv: training rows with ids, source sentences, and train-only target programs.
> test.csv: test rows with ids and source sentences only.
> sample_submission.csv: a schema-valid identity/no-split baseline with one row per test id.
> dataset_metadata.json: public counts and split metadata.
> train.csv columns:
> id: opaque unique row id.
> complex_sentence: the dense source sentence to decompose.
> target_json: train-only canonical target object. Its sentences field is the reference list of simplified output sentences. Its alignments field is a parallel list of integer arrays, one array per output sentence, where each integer is either -1 for an inserted/rephrased token or a zero-based source-token index for a copied token.
> test.csv columns:
> id: opaque unique row id.
> complex_sentence: the dense source sentence to decompose.
> There are no target columns in test.csv.
> Submission
> Submit submission.csv with exactly these columns in exactly this order:
> id
> prediction_json
> The id set must match test.csv exactly, with no missing, extra, duplicate, blank, or foreign ids. Row order does not matter.
> prediction_json must be one JSON object with exactly sentences and alignments.
> First five rows from sample_submission.csv:
> id,prediction_json
> s_e4c9e36e93e2a5d05b42,"{""alignments"":[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]],""sentences"":[""He was previously credited to be one of Malaysia's youngest professional mentalist and magician also public voted as one of Malaysia's top 10 magicians.""]}"
> s_1d99c261c786b20b3027,"{""alignments"":[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]],""sentences"":[""After several self-released albums and mixtapes, he released \""Camp\"", his first album for the label, on November 15,2011.""]}"
> s_0e94d670b71fb2e6ee84,"{""alignments"":[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]],""sentences"":[""The current acting president of Wolfson College is Jon Stallworthy, a noted poet and literary critic and Fellow of the British Academy and Royal Society of Literature; he will be succeeded in October 2008 by Hermione Lee.""]}"
> s_74acb79119180a0abbba,"{""alignments"":[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]],""sentences"":[""Tiara's dad tricked his friend and then, soon they become poor, and they are kicked out of their house.""]}"
> s_d264fdc941fc839f32d1,"{""alignments"":[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]],""sentences"":[""Upon graduation from the course, these cadets are qualified to conduct PDS trainings in their respective school units, as well as attaining the PDS AI badge and a Certificate.""]}"
> Compute
> This bundle is configured for offline CPU execution:
> up to 10 CPU cores
> up to 62 GB RAM
> 90 minutes total runtime
> no network access

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Tabula Rasa ECG Trace Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73kpa6gcxzgpaqhkeqbnsb9n82ehss
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: â†‘ Higher is better
- Tags: Not shown/captured
- Best/top context found: Not shown/captured

Full challenge description from page:

> 1. Background
> In an era increasingly reliant on massive, pre-trained foundation models, this challenge poses a fundamental test of sample-efficient representation learning: Can an architecture map continuous, uncompressed wave data into highly structured, multi-modal symbolic sequences entirely from scratch?
> Standard automated signal processing often reduces complex waveforms to isolated anomaly classifications or simple peak-detection tasks. This challenge demands much more. Given raw, uncompressed 2-channel digitized ambulatory ECG signals, models must simultaneously learn digital filtering, morphological feature extraction, and complex temporal dependencies to emit an integrated, time-ordered sequence of discrete point-in-time events (beats) alongside continuous state intervals (rhythms).
> This is a pure tabula rasa (blank slate) structured sequence reconstruction task. Stripped of pre-trained backbones, external datasets, and hardware accelerators, you must design a highly efficient architecture capable of discovering these complex physiological grammar rules directly from the raw digitized bitstream..
> 2. Overview
> Given a 12-second, 2-channel ambulatory ECG signal (4,320 samples per channel), the goal is to generate a structured prediction for each episode containing three elements.
> Critical Domain Clarification (Ticks): The 12-second window is quantized at 20 Hz, yielding exactly 240 discrete time intervals.
> Beat Trace (beats): An ordered list of beat objects. Each beat requires a discrete time tick and a cardiologist-resolved beat symbol. The beat tick domain is strictly bounded to
> [
> 0
> ,
> 239
> ]
> [0,239].
> Rhythm Spans (rhythms): An ordered list of continuous rhythm intervals defined by start_tick, end_tick, and a rhythm string label. The domain satisfies
> 0
> â‰¤
> start_tick
> <
> end_tick
> â‰¤
> 240
> 0â‰¤start_tick<end_tickâ‰¤240. Note that end_tick may equal 240; this acts explicitly as a sentinel boundary value representing the absolute end of the episode window, which is distinct from valid point-in-time beat ticks.
> Confidence Score (confidence): A scalar value between 0 and 1 estimating the reliability of the predicted beat sequence.
> All feature extractors, digital filters, sequence models, and beat/rhythm classifiers must be developed and trained from scratch using only the provided training episodes.
> 3. Dataset Information
> The challenge package includes metadata CSV files, task metadata, and binary compressed NumPy arrays (.npz) containing the raw signal data. Subject boundaries have been strictly separated between train and test splits to prevent waveform-neighborhood leakage.
> Target Space & Vocabularies
> Valid Beat Symbols: Models must predict from a closed set of valid cardiologist-resolved beat identifiers. The complete set of valid beat symbols is discoverable directly from the provided training set targets.
> Valid Rhythm Labels: Rhythm labels are strings representing standard clinical rhythm annotations (e.g., representing Normal, Tachycardia, and Fibrillation variants). The complete set of valid rhythm labels is discoverable directly from the provided training set targets.
> Public Files
> +-----------------------+-----------------------------------------------------------------------------------------+
> | File / Path           | Description                                                                             |
> +-----------------------+-----------------------------------------------------------------------------------------+
> | train.csv             | Metadata, paths, and ground-truth targets for all training episodes.                    |
> | test.csv              | Metadata and paths for all test episodes (targets withheld).                            |
> | sample_submission.csv | Template demonstrating the required JSON-in-CSV submission structure.                   |
> | task_metadata.json    | Core parameters (duration_seconds=12, ticks_per_second=20).                             |
> | signals/*.npz         | Compressed archives containing the two-channel raw digitized ECG arrays for each row.   |
> +-----------------------+-----------------------------------------------------------------------------------------+
> Tabular Metadata (train.csv & test.csv)
> +----------------+-------------+---------------------+-------------------------------------------------------------------------------------+
> | Column Name    | Data Type   | Field Type          | Description                                                                         |
> +----------------+-------------+---------------------+-------------------------------------------------------------------------------------+
> | id             | String      | Metadata / Key      | Unique opaque identifier for the 12-second ECG episode.                             |
> | signal_path    | String      | File Path           | Relative path to the binary compressed NPZ file containing raw waveform data.       |
> | duration_ticks | Integer     | Input Parameter     | Total episode duration in 20 Hz discrete ticks (always 240 for 12-second episodes). |
> | answer_json    | String/JSON | Target (train only) | Ground-truth JSON string containing target "beats" and "rhythms" lists.             |
> +----------------+-------------+---------------------+-------------------------------------------------------------------------------------+
> Signal Files (signals/*.npz)
> Plaintext
> +-------------+--------------+----------------------------------------------------------------+
> | Key Name    | Data Type    | Description                                                    |
> +-------------+--------------+----------------------------------------------------------------+
> | adc         | Int16 Array  | Raw digitized two-channel ECG signal array of shape (4320, 2). |
> | sample_rate | Int16 Scalar | Nominal sampling frequency of the waveform in Hertz.           |
> +-------------+--------------+----------------------------------------------------------------+
> 4. Evaluation Metrics
> Submissions are evaluated per row using a composite metric balancing tolerant beat matching, timing precision, rhythm span overlap, exact trace matching, and confidence calibration.
> 4.1 Row-Level Score
> For each row
> ð‘–
> i, the score is calculated as:
> RowÂ Score
> âˆ—
> ð‘–
> =
> 0.60
> â‹…
> ð¹
> âˆ—
> 1
> macro
> +
> 0.15
> â‹…
> ð‘†
> timing
> +
> 0.15
> â‹…
> ð‘†
> rhythm
> +
> 0.05
> â‹…
> ð‘†
> exact
> +
> 0.05
> â‹…
> ð‘†
> calib
> RowÂ Scoreâˆ—i=0.60â‹…Fâˆ—1
> macro
> +0.15â‹…S
> timing
> â€‹
> +0.15â‹…S
> rhythm
> â€‹
> +0.05â‹…S
> exact
> â€‹
> +0.05â‹…S
> calib
> â€‹
> Where:
> Macro-Averaged Tolerant Beat F1 (
> ð¹
> 1
> macro
> F
> 1
> macro
> â€‹
> ): A predicted beat matches ground-truth if symbols are identical and time ticks differ by no more than 2 ticks (100 ms). Greedy minimum-distance matching is used to pair predictions and ground truth. To prevent class-imbalance exploitation, F1 is macro-averaged across all
> ð¶
> C unique beat symbol classes present in the ground truth for that row:
> ð¹
> 1
> macro
> =
> 1
> ð¶
> âˆ‘
> ð‘
> =
> 1
> ð¶
> ð¹
> 1
> (
> ð‘
> )
> F
> 1
> macro
> â€‹
> =
> C
> 1
> â€‹
> âˆ‘
> c=1
> C
> â€‹
> F
> 1
> (c)
> â€‹
> (where
> ð¹
> 1
> (
> ð‘
> )
> F
> 1
> (c)
> â€‹
> is the tolerant F1 score calculated exclusively for beat class
> ð‘
> c).
> Matched Timing Quality (
> ð‘†
> timing
> S
> timing
> â€‹
> ): Evaluates temporal precision exclusively among successfully matched beat pairs.
> ð‘†
> timing
> =
> 1
> âˆ£
> ð‘€
> âˆ£
> âˆ‘
> (
> ð‘
> ,
> ð‘”
> )
> âˆˆ
> ð‘€
> (
> 1
> âˆ’
> âˆ£
> ð‘
> tick
> âˆ’
> ð‘”
> tick
> âˆ£
> 3
> )
> S
> timing
> â€‹
> =
> âˆ£Mâˆ£
> 1
> â€‹
> âˆ‘
> (p,g)âˆˆM
> â€‹
> (1âˆ’
> 3
> âˆ£p
> tick
> â€‹
> âˆ’g
> tick
> â€‹
> âˆ£
> â€‹
> )
> (If
> âˆ£
> ð‘€
> âˆ£
> =
> 0
> âˆ£Mâˆ£=0,
> ð‘†
> timing
> S
> timing
> â€‹
> defaults to 0.0).
> Label-Aware Rhythm Overlap (
> ð‘†
> rhythm
> S
> rhythm
> â€‹
> ): Evaluates Intersection-over-Union (IoU) of matching rhythm intervals across the episode's time ticks. To penalize monolithic, single-label predictions, the score is macro-averaged across all
> ð¿
> L unique rhythm classes present in the episode's ground truth and predictions:
> ð‘†
> rhythm
> =
> 1
> ð¿
> âˆ‘
> ð‘™
> =
> 1
> ð¿
> (
> 0.5
> â‹…
> Recall
> rhythm
> (
> ð‘™
> )
> +
> 0.5
> â‹…
> Precision
> rhythm
> (
> ð‘™
> )
> )
> S
> rhythm
> â€‹
> =
> L
> 1
> â€‹
> âˆ‘
> l=1
> L
> â€‹
> (0.5â‹…Recall
> rhythm
> (l)
> â€‹
> +0.5â‹…Precision
> rhythm
> (l)
> â€‹
> )
> Where
> Recall
> rhythm
> (
> ð‘™
> )
> Recall
> rhythm
> (l)
> â€‹
> is the average of the maximum IoU for each ground-truth interval of label
> ð‘™
> l against all predicted intervals of label
> ð‘™
> l, and
> Precision
> rhythm
> (
> ð‘™
> )
> Precision
> rhythm
> (l)
> â€‹
> is the average of the maximum IoU for each predicted interval of label
> ð‘™
> l against all ground-truth intervals of label
> ð‘™
> l. If both predicted and ground-truth rhythm sets are empty, the score is
> 1.0
> 1.0; if exactly one is empty, the score is
> 0.0
> 0.0.
> Exact Trace Match (
> ð‘†
> exact
> S
> exact
> â€‹
> ): Binary
> 1.0
> 1.0 if the predicted beat and rhythm sequences perfectly align with ground truth in both timing and labels.
> Confidence Calibration (
> ð‘†
> calib
> S
> calib
> â€‹
> ): Evaluates how accurately the model estimates its own performance across the dataset using Expected Calibration Error (ECE). Confidence scores across the entire test set are grouped into 10 uniform bins (
> [
> 0.0
> ,
> 0.1
> )
> ,
> [
> 0.1
> ,
> 0.2
> )
> ,
> â€¦
> ,
> [
> 0.9
> ,
> 1.0
> ]
> [0.0,0.1),[0.1,0.2),â€¦,[0.9,1.0]). For each bin
> ð‘
> b, the absolute difference between the mean predicted confidence (
> ð‘
> Ë‰
> ð‘
> c
> Ë‰
> b
> â€‹
> ) and the mean observed macro F1 score (
> ð‘“
> Ë‰
> ð‘
> f
> Ë‰
> â€‹
> b
> â€‹
> ) is calculated:
> ð¸
> ð¶
> ð¸
> =
> âˆ‘
> ð‘
> =
> 1
> 10
> ð‘›
> ð‘
> ð‘
> âˆ£
> ð‘
> Ë‰
> ð‘
> âˆ’
> ð‘“
> Ë‰
> ð‘
> âˆ£
> ECE=âˆ‘
> b=1
> 10
> â€‹
> N
> n
> b
> â€‹
> â€‹
> â€‹
> c
> Ë‰
> b
> â€‹
> âˆ’
> f
> Ë‰
> â€‹
> b
> â€‹
> â€‹
> Where
> ð‘
> N is the total number of test rows and
> ð‘›
> ð‘
> n
> b
> â€‹
> is the number of rows in bin
> ð‘
> b. The final calibration score is:
> ð‘†
> calib
> =
> 1.0
> âˆ’
> ð¸
> ð¶
> ð¸
> S
> calib
> â€‹
> =1.0âˆ’ECE
> This single scalar
> ð‘†
> calib
> S
> calib
> â€‹
> is calculated globally over the entire test set and distributed uniformly to all rows.
> 4.2 Final Leaderboard Score
> FinalÂ Score
> =
> 0.90
> Ã—
> ð‘†
> â€¾
> all
> +
> 0.10
> Ã—
> min
> â¡
> ð‘”
> âˆˆ
> Groups
> (
> ð‘†
> â€¾
> ð‘”
> )
> FinalÂ Score=0.90Ã—
> S
> all
> â€‹
> +0.10Ã—min
> gâˆˆGroups
> â€‹
> (
> S
> g
> â€‹
> )
> ð‘†
> â€¾
> all
> S
> all
> â€‹
> is the arithmetic mean score across all test rows.
> ð‘†
> â€¾
> ð‘”
> S
> g
> â€‹
> is the mean score within hidden evaluation groups (based on dominant rhythm typologies).
> Note: Malformed JSON predictions, invalid schema structures, or out-of-bound values yield 0.0 for that row. File-level schema errors yield 0.0 for the entire submission.
> 5. Sample Submission Format
> Predictions must be submitted in CSV format with three columns: id, prediction_json, and confidence.
> JSON Prediction Object Schema
> JSON
> {
> "beats": [
> {"tick": 37, "symbol": "N"},
> {"tick": 78, "symbol": "N"},
> {"tick": 119, "symbol": "V"}
> ],
> "rhythms": [
> {"start_tick": 0, "end_tick": 240, "label": "N"}
> ]
> }
> CSV Submission Example
> Code snippet
> id,prediction_json,confidence
> e_0123456789abcdef,"{""beats"":[{""tick"":37,""symbol"":""N""}],""rhythms"":[{""start_tick"":0,""end_tick"":240,""label"":""N""}]}",0.85
> e_fedcba9876543210,"{""beats"":[{""tick"":12,""symbol"":""V""},{""tick"":55,""symbol"":""N""}],""rhythms"":[{""start_tick"":0,""end_tick"":120,""label"":""VT""},{""start_tick"":120,""end_tick"":240,""label"":""N""}]}",0.72
> 6. What Not To Use / Constraints
> No Pre-trained ECG Models: You may not use pre-trained biomedical neural networks, foundation model backbones, or third-party clinical arrhythmia classification packages.
> No External Datasets: The use of external ECG corpora, signal databases, or annotated clinical repositories is strictly prohibited. You must learn representations solely from train.csv.
> No Internet / APIs: All signal processing and model execution must run completely offline without external network calls.
> No Source Record Lookups: Participants must not attempt to deanonymize the opaque episode IDs or map them back to real-world clinical databases.
> No GPU / Accelerators: The entire training, fitting, and inference pipeline must execute exclusively on the CPU.
> Hardware & Time Limits:
> 10 CPU Cores
> 62 GB RAM
> Maximum Execution Time: 90 Minutes (Includes both your training/fitting routine and the generation of test predictions).

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Held-Source Vocal Ornament Path Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fhp5sm033rs0v59mbf0dge18bshac
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Leaderboard
> (0)
> Your Submissions
> Overview
> Plain language objective: Given a short Hindustani vocal audio excerpt, reconstruct the complete ornament path in that excerpt. An ornament is a short expressive pitch gesture such as a slide, turn, or grace-note-like movement. The model must output a coherent ordered path of gesture spans and the directed transitions between neighboring spans, not a transcript of lyrics, not framewise tags, and not a single class label.
> Each audio excerpt is divided into a fixed time grid. A start_bin or end_bin is an integer position on that grid, where bin_hz = 20 means 20 bins per second. For example, start_bin = 40 means the gesture starts around 2 seconds into the excerpt.
> The core task is path reconstruction under a held-source split: a strong solution must infer how many ornament spans are present, assign each span a legal label, place its start and end bins, and keep the neighboring-label transitions consistent across the full excerpt.
> This challenge belongs only to the From Scratch domain. Participants train from the supplied public training records and may not use hosted inference or external source lookup. The source material is real-world and non-tabular, not synthetic benchmark prose.
> The dataset card identifies the raw source as a derivative of the public Raga Ornamentation Detection (ROD) release, and Saraga-style Hindustani vocal corpora are the closest public family of related work. Those resources primarily support detecting or annotating ornament spans with onset and offset times.
> This benchmark changes the evaluated object from independent span detection to row-local path reconstruction. The submitted object must be a valid ordered JSON path with span identities, labels, legal time bins, and transition edges. The adjacency head changes the solver behavior: predicting the correct individual spans is not enough if the model scrambles the path order or breaks neighboring-label continuity. The hidden split is grouped by upstream source family, so public training rows do not contain labeled copies of the held-out source group.
> Dataset
> The dataset is a prepared, opaque derivative of a real licensed research collection. Raw scale: approximately 2.4 GB of annotated Hindustani vocal recordings and deposited ornament labels. Exact attribution and license information are kept in the separately displayed dataset form so that the challenge statement does not expose lookup breadcrumbs.
> Public input: An opaque audio excerpt plus a row manifest describing the legal time grid and row-local label space. Artist, raga, recording name, expert identity, and upstream timestamps are withheld.
> train.csv has id, manifest_path, prompt, and target_json. test.csv has the same input columns without target_json. sample_submission.csv has the exact submission header and ID order. Manifest paths are relative to the public output directory.
> File Overview
> Item	Description
> train.csv	Public training rows and structured targets
> test.csv	Public held-out inputs with targets removed
> sample_submission.csv	Exact submission header and ID order
> packets/*/manifest.json	Opaque row-local input manifest
> CSV Columns
> Column	Type	Description
> id	string	Opaque row identifier
> manifest_path	string	Relative packet-manifest path
> prompt	string	Short instruction for the row
> target_json	JSON string	Training-only structured target
> Manifest JSON
> Each packets/<id>/manifest.json gives the participant-visible inputs for one row.
> Field	Type	Description
> id	string	Same row ID as the CSV
> audio_path	string	Relative path to the WAV excerpt
> bin_hz	integer	Time bins per second
> max_bin	integer	Last legal time-bin index
> event_count_hint	integer	Approximate event count
> legal_labels	string list	Labels allowed in this row
> expert_source_hidden	boolean	Source identity is hidden
> Target JSON
> A JSON object has two top-level keys: events and transitions. Together they define the reconstructed ornament path for one excerpt.
> events is an ordered list. Each event object has:
> Field	Type	Description
> event_id	string	Row-local event ID
> label	string	Ornament type from legal_labels
> start_bin	integer	Start time-bin, 0 <= start_bin < end_bin
> end_bin	integer	End time-bin, end_bin <= max_bin
> transitions is an ordered list connecting consecutive events in the predicted path. If event E001 is followed by E002, the transition is {"from":"E001","to":"E002","label_pair":"H>Me"} where label_pair joins the two event labels.
> Example target or prediction object:
> {
> "events": [
> {"event_id": "E001", "label": "H", "start_bin": 12, "end_bin": 31},
> {"event_id": "E002", "label": "Me", "start_bin": 44, "end_bin": 58},
> {"event_id": "E003", "label": "G", "start_bin": 72, "end_bin": 83}
> ],
> "transitions": [
> {"from": "E001", "to": "E002", "label_pair": "H>Me"},
> {"from": "E002", "to": "E003", "label_pair": "Me>G"}
> ]
> }
> All handles inside a row are opaque and row-local. A solver must emit one JSON object per row. Unknown handles, duplicate assignments where uniqueness is required, malformed JSON, or structurally oversized JSON receive zero for that row.
> Submission
> Submit submission.csv with columns in this exact order: id,prediction_json. The ID sequence must exactly match test.csv; extra, missing, duplicated, or reordered IDs invalidate the submission. prediction_json is the task JSON described above.
> Column	Type	Constraint
> id	string	Exact held-out ID and row order
> prediction_json	JSON string	One bounded task object per row
> Example submission.csv:
> id,prediction_json
> A123EXAMPLE0001,"{""events"":[{""event_id"":""E001"",""label"":""H"",""start_bin"":10,""end_bin"":28},{""event_id"":""E002"",""label"":""Me"",""start_bin"":39,""end_bin"":55}],""transitions"":[{""from"":""E001"",""to"":""E002"",""label_pair"":""H>Me""}]}"
> A123EXAMPLE0002,"{""events"":[{""event_id"":""E001"",""label"":""G"",""start_bin"":8,""end_bin"":20}],""transitions"":[]}"
> Evaluation
> Each valid row is compared with the hidden target using two implementation-agnostic structured heads. The first rewards recovery of the span facts; the second rewards the path order:
> Head	Weight	Definition
> Atomic structured facts	0.70	Set F1 over recursively extracted JSON key/value and list-member facts
> Ordered adjacency	0.30	Set F1 over adjacent members of every ordered JSON list
> The row score is 0.70 * fact_F1 + 0.30 * adjacency_F1; the final score is the mean over rows. Range: [0,1]. The theoretical minimum is 0.0; an exact valid submission scores exactly 1.0. A malformed row receives zero without crashing the grader. Submission-level schema or ID errors are rejected.
> For a set comparison, precision = matched_predicted_items / predicted_items, recall = matched_predicted_items / gold_items, and F1 = 2 * precision * recall / (precision + recall). If both sets are empty, that F1 is 1.0; if only one side is empty, it is 0.0.
> The fact score rewards matching JSON fields and list members, such as label = "H", start_bin = 12, and the full event object appearing in the events list. The adjacency score rewards correct neighboring structure inside ordered lists, such as event E001 immediately before event E002. This means a solution gets credit for predicting the right labels and times, and separate credit for preserving the sung ornament path instead of treating spans as independent detections.
> Generalization Contract
> Whole upstream source families are kept together in one split; related excerpts do not cross between train and test. Public IDs and output filenames are hash-derived opaque handles. Private answers, source paths, original row order, exact held-out group names, and split-group labels never enter public test files.
> Practical CPU Modeling Guidance
> Official resources: 10 CPU cores, 62 GB RAM, 1.5 hours wall-clock, no GPU. Suitable ingredients: Log-mel/chroma features, compact CRF/HMM or small temporal CNN, duration priors, and Viterbi decoding. Keep training and inference offline and cache compact features.
> Intended Approaches
> Strong solutions are expected to learn from the provided training data and may train their own CPU-friendly architectures from scratch. Reasonable approaches include extracting compact audio features, training a small temporal sequence model or structured decoder, and using dynamic programming to produce a legal ordered path of spans and transitions. The intended path is genuine from-scratch sequence reconstruction on the supplied examples, not source lookup, hosted inference, framewise label copying, or reduction to independent event classification.
> What Not To Use
> hosted or closed-source inference APIs, runtime downloads, or GPU-only workflows;
> source-corpus lookup, reverse media search, audio fingerprint lookup, recovered source filenames, IDs, URLs, mtimes, or file-size side channels;
> private-file access, hard-coded hidden answers, grader exploitation, or manual labelling of test rows;
> malformed/oversized CSV or JSON, duplicate IDs, or impossible row-local handles;
> reducing the task to classification or continuous regression instead of emitting the required structure.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Cell Event Program Recovery from Fluorescence Traces

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx726phae2dhhnv26kwxyzm9y98aste7
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Pending Review
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Be the first to climb the leaderboard!

Full challenge description from page:

> Leaderboard
> (0)
> Your Submissions
> Overview
> Each row contains a short anonymized sensor log from a real yeast cell experiment. Think of it as a multivariate time series: for each observed cell, you receive one value sequence for brightness, one value sequence for cell size, and a validity mask that says which frames are usable.
> Your task is to predict the ordered event list hidden in that time series. For each cell, identify whether and when two event types happen: bud_onset, meaning a visible growth event starts, and trace_exit, meaning the tracked cell leaves or ends before the recording finishes.
> This challenge belongs to the From Scratch domain. Participants may train models on the supplied public training rows, but may not use hosted inference, GPU-only workflows, private files, or external source lookup.
> Dataset
> The public data is derived from real cell-cycle microscopy experiments. The raw upload contains microscope image examples, cell-tracking resources, MATLAB analysis files, and per-cell trace files. The challenge input is a prepared trace packet, not the raw images.
> For each example, open the row's manifest_path. The manifest has this structure:
> {
> "id": "Y123EXAMPLE",
> "frame_count": 120,
> "cells": [
> {
> "cell_id": "C1A2B3C4D",
> "fluorescence": [0.13, 0.20, -0.05],
> "relative_area": [0.98, 1.01, 1.04],
> "valid": [1, 1, 1]
> }
> ]
> }
> frame_count is the number of time steps. Each item in cells is one tracked cell. fluorescence is the normalized brightness sequence, relative_area is the normalized size sequence, and valid is a same-length 0/1 mask. cell_id is an anonymized handle that must be reused exactly in predictions for that row.
> train.csv has id, manifest_path, prompt, and target_json. test.csv has the same input columns without target_json. sample_submission.csv has the required submission header and held-out ID order. Manifest paths are relative to the public output directory.
> File Overview
> Item	Description
> train.csv	Training inputs and targets
> test.csv	Held-out inputs
> sample_submission.csv	Submission template
> packets/*/manifest.json	Trace packet
> CSV Columns
> Column	Type	Description
> id	string	Row identifier
> manifest_path	string	Manifest path
> prompt	string	Task instruction
> target_json	JSON string	Train target only
> Target JSON
> The target is a JSON object with one key, events. Its value is an ordered list of event objects:
> {
> "events": [
> {"cell_id": "C1A2B3C4D", "event": "bud_onset", "frame_bin": 37},
> {"cell_id": "C1A2B3C4D", "event": "trace_exit", "frame_bin": 91}
> ]
> }
> cell_id must be one of the cell_id values in that row's manifest. event must be bud_onset or trace_exit. frame_bin is an integer time step from 0 to frame_count - 1. Events should be sorted by time when possible.
> Submission
> Submit submission.csv with columns in this exact order: id,prediction_json. The ID sequence must exactly match test.csv; extra, missing, duplicated, or reordered IDs invalidate the submission.
> Example:
> id,prediction_json
> Y123EXAMPLE,"{""events"":[{""cell_id"":""C1A2B3C4D"",""event"":""bud_onset"",""frame_bin"":37}]}"
> Y456EXAMPLE,"{""events"":[]}"
> Column	Type	Constraint
> id	string	Exact test ID order
> prediction_json	JSON string	Event-list object
> Evaluation
> The score is the mean row score over all held-out rows. Each row is scored by comparing the predicted JSON object with the hidden target JSON object.
> For a JSON object, the grader extracts two token sets:
> Token set	Meaning
> facts	All key/value facts and list members
> order	Adjacent list-member pairs
> For each token set, precision is matches / predicted_tokens, recall is matches / target_tokens, and F1 = 2 * precision * recall / (precision + recall). If both sets are empty, that F1 is 1.0; if only one side is empty, it is 0.0.
> The row score is:
> 0.70 * F1(facts) + 0.30 * F1(order)
> The final score is the mean of all row scores. The score range is [0, 1]. A perfect submission scores 1.0. A malformed JSON row, unknown cell_id, oversized JSON object, wrong columns, duplicate IDs, missing IDs, or wrong row order receives zero or is rejected by the grader.
> Generalization Contract
> Rows from the same microscope position are kept together in one split, so closely related traces do not appear in both train and test. Public IDs and packet filenames are anonymized. Hidden answers, source paths, original row order, and split-group labels are not included in public test files.
> Practical CPU Modeling Guidance
> Official resources: 10 CPU cores, 62 GB RAM, 1.5 hours wall-clock, no GPU. Suitable approaches include time-series feature extraction, change-point detection, compact temporal models, dynamic programming, and cross-cell consistency checks. Keep training and inference offline.
> What Not To Use
> hosted inference APIs, runtime downloads, or GPU-only workflows;
> external source lookup, reverse media search, recovered source filenames, IDs, URLs, or file-size side channels;
> private-file access, hard-coded hidden answers, grader exploitation, or manual labelling of test rows;
> malformed or oversized CSV/JSON, duplicate IDs, impossible row-local handles, or reordered rows;
> reducing the task to a single classification label or continuous regression target instead of emitting the required event-list JSON.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Head Motion Prediction from Eye Coordination

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76wdf8e3qsav2tafsm6rnbys8c7jee
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat arin's score of 0.446!

Full challenge description from page:

> Leaderboard
> (24)
> Your Submissions
> Overview
> Train a compact sensor encoder from random initialization using fixed 160 x 6 coordination tensors. Each tensor contains left- and right-eye direction vectors in a row-local 3D frame. Five bounded prediction heads describe the associated head movement: displacement bins, dominant movement direction, eye-to-head lag bin, coupling class, and path-length bin.
> Every row is an independent fixed-size representation-learning example. The intended solution learns shared eye-motion features and fits the five heads jointly; it does not produce an open-ended continuation. Subjects are separated between training and test data, so useful representations must generalize coordination patterns to people absent from training.
> Do not use GPU acceleration. Train models only from the released challenge data; pretrained models and external data are not allowed.
> Dataset
> train.csv: labeled training rows.
> test.csv: unlabeled test rows.
> coordination_windows.npz: float32 array named windows, shaped (rows, 160, 6).
> sample_submission.csv: random, schema-valid submission.
> CSV columns:
> id (string): anonymized row identifier.
> array_index (integer): row in coordination_windows.npz/windows.
> coordination_contract_json (JSON string): contains window_shape ([160,6]), target_head_rows ([56,104], with the end excluded), coordinate_frame (row_local), delta_bin_range ([-12,12]), and lag_range ([-12,12]).
> answer_json (JSON string, training only): the five-head target record defined below.
> Channels 0-2 and 3-5 are the left- and right-eye direction vectors in a row-local 3D coordinate frame. The target summarizes head motion at rows 56 through 103 of the same transformed recording; no head-direction channel is released.
> Target Record
> answer_json contains:
> head_delta_bins: integer x, y, and z displacement bins in [-12,12].
> dominant_axis: one of x_negative, x_positive, y_negative, y_positive, z_negative, z_positive.
> eye_head_peak_lag: integer in [-12,12]; positive means the head-speed peak occurs later than the eye-speed peak.
> coupling_state: opposed, weak, or coupled, based on eye-speed/head-speed correlation.
> path_length_bin: integer from 0 through 24, obtained by binning the total head-direction path length in the hidden interval.
> Evaluation
> For each integer field, exact agreement receives 1, an error of one bin receives 0.35, an error of two bins receives 0.10, and larger errors receive 0. The three displacement-bin credits are averaged. The row score is:
> 0.42 * mean_delta_closeness + 0.20 * dominant_axis_exact + 0.18 * lag_closeness + 0.12 * coupling_exact + 0.08 * path_length_closeness
> Exact categorical terms are 1 for equality and 0 otherwise. The leaderboard score is the mean row score. Malformed row JSON scores zero; wrong columns or an incorrect id set rejects the submission.
> Submission
> Submit exactly two columns in this order:
> id (string)
> answer_json (JSON string using the schema above)
> CSV quoting must escape each inner double quote by doubling it. The included sample_submission.csv demonstrates the required encoding.
> Two correctly quoted rows look like this:
> id,answer_json
> coord_19a24e60bf817d32ac,"{""head_delta_bins"":{""x"":2,""y"":-1,""z"":0},""dominant_axis"":""x_positive"",""eye_head_peak_lag"":3,""coupling_state"":""coupled"",""path_length_bin"":8}"
> coord_b5163df047ac920e51,"{""head_delta_bins"":{""x"":-2,""y"":0,""z"":1},""dominant_axis"":""x_negative"",""eye_head_peak_lag"":-1,""coupling_state"":""weak"",""path_length_bin"":5}"

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Rail Corridor Structure Profiling

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70sbxk4caw8xbgdaprdz691n8c5d8g
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat mrnguyen's score of 0.829!

Full challenge description from page:

> Leaderboard
> (17)
> Your Submissions
> Rail Corridor Structure Profiling
> Overview
> This is a from-scratch learning task over raw 3-D point tensors: no pretrained
> representation of this modality is supplied, and the training split is the only source of
> supervision. The objective is to profile where sparse trackside structures occur along a rail
> corridor. Each item is a tile: roughly 40 metres of an
> electrified railway corridor captured as an unlabelled cloud of 3-D points, each point
> carrying a position and a reflectivity value. The tile is divided into eight equal
> along-track bins, and for each bin you predict the probability that each of two structure
> classes occupies it.
> The two classes are deliberately sparse. Markers are flat, ground-level features that
> have almost no vertical relief — they occupy about 4% of bins. Panels are the small
> upright trackside elements such as boards and signal heads, occupying about 3% of bins.
> Everything else in the corridor — the running track, the overhead wiring and its supports,
> the surrounding ground, vegetation and structures — is present in the point cloud but is not
> labelled and is not scored, so the sparse targets must be separated from a dense and highly
> repetitive background. Over 99% of the points in a tile belong to that unlabelled
> background.
> Three properties of the data shape the difficulty. The targets are rare, at roughly 4% and 3%
> of bins. The structures are small: a marker may contribute only a few dozen points out of the
> tens of thousands in a tile. And the reflectivity channel is capped at the top of its range,
> so the most reflective surfaces in the corridor are not distinguishable from one another.
> Dataset
> Public files
> train.csv — one row per training tile, with the occupancy targets.
> Columns: tile_id, points_file, group_id, n_points, span_m, and the 16 target
> columns marker_1 … marker_8, panel_1 … panel_8.
> test.csv — one row per test tile, without targets.
> Columns: tile_id, points_file, n_points, span_m.
> tiles/<tile_id>.npy — the point cloud for one tile. A NumPy array of dtype int16 and
> shape (n_points, 4). There is one such file per row of train.csv and test.csv.
> sample_submission.csv — a valid submission in the required format.
> Private file
> answers.csv — the occupancy targets for the test tiles. Held by the organisers.
> Column descriptions
> The columns of train.csv and test.csv are as follows.
> tile_id (string) — unique identifier of the tile, e.g. tile_a8bf13572d14a2ee. Use this
> to join a row to its submission row.
> points_file (string) — path of the tile's point array, relative to the public directory,
> e.g. tiles/tile_a8bf13572d14a2ee.npy.
> group_id (string) — identifier of the continuous stretch of corridor a tile was cut
> from. Tiles sharing a group_id are physically adjacent. Present in train.csv only; use
> it to build cross-validation folds that keep adjacent tiles out of the validation fold.
> n_points (integer) — number of points in the tile's array.
> span_m (float) — along-track length of the tile in metres, i.e. the extent of the x
> axis. The eight scored bins are equal-width divisions of [0, span_m].
> marker_1 … marker_8 (integer, 0 or 1) — target. 1 if the ground-level marker class
> occupies that along-track bin. Bin 1 is nearest x = 0. train.csv only.
> panel_1 … panel_8 (integer, 0 or 1) — target. 1 if the upright trackside panel class
> occupies that along-track bin. train.csv only.
> The four columns of each tiles/<tile_id>.npy array are as follows.
> column 0 (int16) — position along the corridor, in centimetres, starting at 0 at the
> tile's beginning and increasing to span_m * 100.
> column 1 (int16) — lateral offset from the centre of the track, in centimetres, in the
> range −900 to 900. Negative is one side of the track, positive the other.
> column 2 (int16) — height above the plane of the running track, in centimetres, in the
> range −100 to 800.
> column 3 (int16) — reflectivity of the return, an integer from 0 to 96. Values are
> clipped at the top of the range, so the most reflective surfaces are indistinguishable from
> one another.
> Every tile has been resampled to a uniform 0.15 m resolution, so point density does not vary
> systematically between tiles.
> A bin counts as occupied when at least 5 points of that structure class fall inside it,
> measured on the same resampled cloud that is published.
> Data example
> A row of train.csv:
> tile_id,points_file,group_id,n_points,span_m,marker_1,...,marker_8,panel_1,...,panel_8
> tile_a8bf13572d14a2ee,tiles/tile_a8bf13572d14a2ee.npy,grp_398576ecdae7064a,68665,41.55,0,...,0,0,...,0
> The first three rows of the corresponding array, as (x_cm, lateral_cm, height_cm, reflectivity):
> [[829 773 266   9]
> [846 790 274  11]
> [842 771 264  11]]
> Submission format
> A CSV with a header row and exactly one row per test tile, in any order.
> Required columns, exactly 17 and no others:
> tile_id — must match a tile_id in test.csv. Every test tile must appear exactly once;
> missing tiles and unknown tiles are both rejected.
> marker_1 … marker_8 — probability that the marker class occupies that bin.
> panel_1 … panel_8 — probability that the panel class occupies that bin.
> Every probability must be a number in [0, 1]. Blank cells, non-numeric values, values
> outside the range, and duplicate tile_id values are rejected.
> tile_id,marker_1,marker_2,marker_3,marker_4,marker_5,marker_6,marker_7,marker_8,panel_1,panel_2,panel_3,panel_4,panel_5,panel_6,panel_7,panel_8
> tile_17af920b7edc5cf7,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1
> tile_f7135bf15f9583e6,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1
> Evaluation
> The metric is the Trackside Occupancy Calibration Score (TOCS). Higher is better.
> Each of the two structure classes is scored independently over all test bins, then the two
> class scores are averaged with equal weight. Because the classes are averaged equally, the
> rarer class cannot be ignored in favour of the other.
> For one class, over every (tile, bin) cell in the test set:
> # y = 1 if the class occupies the cell, else 0
> # p = the submitted probability for that cell
> # ref = the fixed reference rate for the class
> brier_skill = 1 - sum((y - p)**2) / sum((y - ref)**2)
> brier_skill = max(-1.0, brier_skill)          # floored at -1.0
> gini = max(0.0, 2 * auc(y, p) - 1)            # auc uses average ranks for ties
> class_score = 0.80 * brier_skill + 0.20 * gini
> TOCS = mean(class_score for each class)
> TOCS = max(0.02, min(1.0, TOCS))              # clamped to [0.02, 1.0]
> The fixed reference rates are 0.04 for the marker class and 0.03 for the panel class.
> These are constants, not recomputed from a submission, so the calibration term measures
> improvement over always predicting the class's background rate.
> The calibration term carries a weight of 0.80 and the ranking term 0.20. The
> calibration term alone is what a well-calibrated but undiscriminating prediction earns; the
> ranking term credits ordering the cells correctly even when the absolute probabilities are
> off. The Brier skill component is floored at −1.0 so that one badly mis-calibrated class
> cannot dominate the average, and the Gini component is floored at 0.0 so that ranking
> worse than chance is not penalised twice. The final score is clamped to the range
> [0.02, 1.0].
> If either class had no occupied cells or no unoccupied cells in the test set it could not be
> scored and grading fails rather than silently averaging over one class; the published test
> split contains both outcomes for both classes.
> Ties in the submitted probabilities are resolved by average rank, so a prediction that is
> constant across cells receives a Gini of exactly 0, and adding arbitrarily small noise to a
> constant prediction cannot improve the score.
> Baseline: predicting each class's reference rate in every cell gives a Brier skill of 0
> and a Gini of 0, so it scores 0 before the clamp and 0.02 as reported. That is the chance
> level. The supplied sample_submission.csv uses a constant 0.1 in every cell, which is worse
> than the reference rate before clamping and therefore also scores 0.02. A perfect
> submission scores 1.0.
> What Not To Use (Prohibited Methods)
> Do not use any external answer key, pre-computed annotation, or label file for these tiles
> or for any corridor survey they may resemble.
> Do not attempt to identify, download, or match against any external 3-D survey corpus of
> railway or road corridors, whether by point-cloud registration, geometric fingerprinting,
> reflectivity signature, or any published asset inventory. The tiles are re-cropped,
> resampled, re-framed to a local origin and re-identified; recovering an external source and
> transferring its per-point annotations back onto the test tiles is prohibited.
> Do not hardcode predictions against tile_id values, or build any lookup that maps a
> tile_id, a row position, a file size, or a point count to a target. Predictions must be a
> function of the point geometry and reflectivity in the tile.
> Do not use group_id to infer test targets. It is provided for cross-validation on the
> training split only, and is deliberately absent from test.csv; reconstructing which test
> tiles are adjacent in order to propagate labels between them is prohibited.
> Do not manually inspect and annotate test tiles by hand, or use any human labelling of the
> test set, in whole or in part.
> Do not tune any decision, threshold, or calibration against the private targets by
> repeated submission; the submitted model must be selected using the training split alone.
> Do not exploit the resampling or clipping used to build the tiles — for example by trying
> to invert the 0.15 m resampling or the reflectivity cap to recover the original survey
> values — in order to identify the source data.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Cell Colony Instance Topology Challenge

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dm4rpkg8zzw5task86mftrx8c78gn
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat arin's score of 0.814!

Full challenge description from page:

> Leaderboard
> (19)
> Your Submissions
> Background
> Mapping cellular networks through high-resolution microscopy is a foundational protocol in histopathology, pharmacological screening, and spatial transcriptomics. Deciphering the spatial orchestration, clustering density, and structural connectivity of these networks yields critical data on cell-to-cell signaling and proliferation dynamics. While traditional instance segmentation produces dense, computationally expensive pixel-level masks, analyzing population architecture requires a purely structural approach. By modeling colonies as architectural graphs—where vertices represent cellular centroids with discrete physical footprint labels, and edges encode the immediate neighborhood proximity—researchers gain a highly optimized, segmentation-free blueprint of biological tissues.
> Overview
> This competition presents a structural network synthesis objective that completely circumvents standard pixel-wise regression or dense mask generation. Given a raw microscopy scan, participants must engineer pipelines that fully reconstruct the hidden topological graph of the cellular cluster. This requires isolating individual cellular vertices (centroids), classifying their physical footprint into one of five discrete scale bands, and projecting a bounded nearest-neighbor connectivity mesh that charts the microcellular neighborhood.
> This represents a strict ab initio (from scratch) algorithmic track. Every trainable component must originate from a completely random initialization and learn exclusively from the distributed public learning corpus. The execution protocol enforces a stringent offline computing envelope: a maximum 90-minute runtime utilizing strictly CPU hardware (maximum 10 cores, 62 GB RAM). Successful architectures might integrate blob detection heuristics, topological watershed operations, distance transforms, k-nearest-neighbor clustering, or highly optimized, randomly initialized convolutional graph networks.
> Dataset Public Files
> The provided dataset consists of structured CSV manifests mapping to a directory of microscopy images, along with configuration metadata.
> train.csv: The primary learning manifest containing image metadata and the ground-truth topological networks (cells_json and edges_json).
> test.csv: The holdout evaluation manifest containing solely the image identifiers, file paths, and dimensions for inference.
> sample_submission.csv: A compliant template demonstrating the expected CSV layout and empty payload strings for the network predictions.
> task_metadata.json: A configuration parameter file defining the valid footprint bands (tiny, small, medium, large, giant) and split row statistics.
> images/: A directory hosting all .png microscopy scans referenced within the manifests.
> Dataset Information
> Core CSV Manifests
> +-----------------------+-------------+---------+--------------------------------------------------------------+
> | File                  | Column      | Type    | Description                                                  |
> +-----------------------+-------------+---------+--------------------------------------------------------------+
> | train.csv             | image_id    | String  | Opaque identifier for the specific microscopy scan.          |
> | train.csv             | image_path  | String  | Relative directory path locating the visual asset.           |
> | train.csv             | width       | Integer | Image width in horizontal pixels.                            |
> | train.csv             | height      | Integer | Image height in vertical pixels.                             |
> | train.csv             | cells_json  | JSON    | Target array representing cellular vertices and scale bands. |
> | train.csv             | edges_json  | JSON    | Target array detailing nearest-neighbor links between cells. |
> | test.csv              | image_id    | String  | Opaque identifier for the holdout evaluation scan.           |
> | test.csv              | image_path  | String  | Relative directory path locating the evaluation asset.       |
> | test.csv              | width       | Integer | Image width in horizontal pixels.                            |
> | test.csv              | height      | Integer | Image height in vertical pixels.                             |
> | sample_submission.csv | image_id    | String  | Identifier corresponding directly to test.csv records.       |
> | sample_submission.csv | cells_json  | JSON    | Your predicted cellular vertices payload.                    |
> | sample_submission.csv | edges_json  | JSON    | Your predicted nearest-neighbor links payload.               |
> +-----------------------+-------------+---------+--------------------------------------------------------------+
> JSON Schema Breakdown
> cells_json Payload Structure This payload must be an array of up to 700 dictionary objects, each representing an identified cellular vertex.
> +-------+---------+---------------------------------------------------------------------------------+
> | Field | Type    | Description                                                                     |
> +-------+---------+---------------------------------------------------------------------------------+
> | cid   | String  | A local node ID (max 32 chars) uniquely identifying the cell (e.g., "c1").      |
> | x     | Integer | The horizontal pixel coordinate of the cellular centroid.                       |
> | y     | Integer | The vertical pixel coordinate of the cellular centroid.                         |
> | size  | String  | The quantized area scale: "tiny", "small", "medium", "large", or "giant".       |
> +-------+---------+---------------------------------------------------------------------------------+
> edges_json Payload Structure This payload must be an array of up to 1500 dictionary objects, mapping the bounded topological connections between cells.
> +-------+--------+-----------------------------------------------------------------------------+
> | Field | Type   | Description                                                                 |
> +-------+--------+-----------------------------------------------------------------------------+
> | a     | String | The `cid` of the primary connected cell. Must exist in cells_json.          |
> | b     | String | The `cid` of the secondary connected cell. Must exist in cells_json.        |
> +-------+--------+-----------------------------------------------------------------------------+
> Evaluation Metrics
> Submissions undergo a row-by-row comparative analysis against a hidden ground-truth set. For a given image, let
> 𝑃
> P denote the predicted vertices and
> 𝐺
> G denote the ground-truth vertices. The image diagonal is defined as
> 𝐷
> =
> width
> 2
> +
> height
> 2
> D=
> width
> 2
> +height
> 2
> ​
> .
> First, predictions and ground-truth nodes are paired via a greedy matching algorithm. A prediction is a valid candidate for a ground-truth cell if the Euclidean distance between them is strictly less than the threshold
> 𝑇
> =
> max
> ⁡
> (
> 0.035
> ⋅
> 𝐷
> ,
> 3
> )
> T=max(0.035⋅D,3). Matches are resolved greedily based on the shortest distance. Let
> 𝑀
> M represent the final set of matched cell pairs.
> The overarching row score aggregates precisely four targeted sub-metrics:
> 1. Radius-Matched Vertex F1 (
> 𝐹
> 1
> 𝑝
> 𝑜
> 𝑖
> 𝑛
> 𝑡
> F1
> point
> ​
> , Weight: 35%)
> Evaluates the success of centroid localization utilizing a standard F1 score over the valid matches.
> 𝐹
> 1
> 𝑝
> 𝑜
> 𝑖
> 𝑛
> 𝑡
> =
> 2
> ∣
> 𝑀
> ∣
> max
> ⁡
> (
> ∣
> 𝑃
> ∣
> +
> ∣
> 𝐺
> ∣
> ,
> 1
> )
> F1
> point
> ​
> =
> max(∣P∣+∣G∣,1)
> 2∣M∣
> ​
> 2. Footprint Scale Accuracy (
> 𝑆
> 𝑠
> 𝑖
> 𝑧
> 𝑒
> S
> size
> ​
> , Weight: 15%)
> Evaluates the precision of assigning the correct physical footprint category among the successfully matched pairs. Let
> 𝑁
> =
> max
> ⁡
> (
> ∣
> 𝑃
> ∣
> ,
> ∣
> 𝐺
> ∣
> ,
> 1
> )
> N=max(∣P∣,∣G∣,1) represent the denominator.
> 𝑆
> 𝑠
> 𝑖
> 𝑧
> 𝑒
> =
> 1
> 𝑁
> ∑
> (
> 𝑝
> ,
> 𝑔
> )
> ∈
> 𝑀
> 𝐼
> (
> size
> 𝑝
> =
> =
> size
> 𝑔
> )
> S
> size
> ​
> =
> N
> 1
> ​
> ∑
> (p,g)∈M
> ​
> I(size
> p
> ​
> ==size
> g
> ​
> )
> 3. Topology Edge F1 (
> 𝐹
> 1
> 𝑒
> 𝑑
> 𝑔
> 𝑒
> F1
> edge
> ​
> , Weight: 25%)
> Evaluates the structural neighborhood map. The local cid strings within the predicted edges are translated to the ground-truth cid strings using the established node matches
> 𝑀
> M. These mapped predicted edges are then compared against ground-truth edges using a multiset F1 formula.
> 4. Degree-Distribution Similarity (
> 𝑆
> 𝑑
> 𝑒
> 𝑔
> 𝑟
> 𝑒
> 𝑒
> S
> degree
> ​
> , Weight: 15%)
> Measures how closely the connectivity density of the predicted graph matches the ground truth. Node degrees are capped at a maximum of 6. A frequency histogram
> 𝐻
> H of node degrees is calculated for both mapped predictions and ground truth across all shared bins
> 𝑏
> b.
> 𝑆
> 𝑑
> 𝑒
> 𝑔
> 𝑟
> 𝑒
> 𝑒
> =
> max
> ⁡
> (
> 0
> ,
> 1
> −
> ∑
> 𝑏
> ∣
> 𝐻
> 𝑃
> (
> 𝑏
> )
> −
> 𝐻
> 𝐺
> (
> 𝑏
> )
> ∣
> max
> ⁡
> (
> ∑
> 𝑏
> 𝐻
> 𝑃
> (
> 𝑏
> )
> +
> ∑
> 𝑏
> 𝐻
> 𝐺
> (
> 𝑏
> )
> ,
> 1
> )
> )
> S
> degree
> ​
> =max(0,1−
> max(∑
> b
> ​
> H
> P
> ​
> (b)+∑
> b
> ​
> H
> G
> ​
> (b),1)
> ∑
> b
> ​
> ∣H
> P
> ​
> (b)−H
> G
> ​
> (b)∣
> ​
> )
> Total Row Score
> Note: There are exactly four sub-metrics whose weights intentionally sum to 0.90 (0.35 + 0.15 + 0.25 + 0.15). There is no omitted fifth metric; the row score formula explicitly divides by this 0.90 constant to rescale the final aggregate score perfectly into the standard
> [
> 0
> ,
> 1
> ]
> [0,1] interval.
> Row Score
> =
> 0.35
> ⋅
> 𝐹
> 1
> 𝑝
> 𝑜
> 𝑖
> 𝑛
> 𝑡
> +
> 0.15
> ⋅
> 𝑆
> 𝑠
> 𝑖
> 𝑧
> 𝑒
> +
> 0.25
> ⋅
> 𝐹
> 1
> 𝑒
> 𝑑
> 𝑔
> 𝑒
> +
> 0.15
> ⋅
> 𝑆
> 𝑑
> 𝑒
> 𝑔
> 𝑟
> 𝑒
> 𝑒
> 0.90
> Row Score=
> 0.90
> 0.35⋅F1
> point
> ​
> +0.15⋅S
> size
> ​
> +0.25⋅F1
> edge
> ​
> +0.15⋅S
> degree
> ​
> ​
> Final Leaderboard Formulation
> To guarantee the model generalizes across diverse biological conditions rather than just excelling on sparsely populated images, the final metric merges the global mean row score with the minimum group mean row score. The evaluation groups are defined by the underlying cellular density (sparse, medium, dense).
> Final Score
> =
> 0.90
> ⋅
> Mean
> (
> Row Score
> )
> +
> 0.10
> ⋅
> MinGroupMean
> (
> Row Score
> )
> Final Score=0.90⋅Mean(Row Score)+0.10⋅MinGroupMean(Row Score)
> (Scores are clipped strictly to
> [
> 0
> ,
> 1
> ]
> [0,1]. Exact topological matches yield a flawless 1.0. Invalid syntax or architectural violations yield 0.0 for that specific row).
> Sample Submission Format
> Submit a UTF-8 encoded CSV file containing exactly three columns arranged in this precise order: image_id, cells_json, edges_json. Ensure JSON payloads are properly string-escaped utilizing double quotes "".
> Code snippet
> image_id,cells_json,edges_json
> cell_a1b2c3d4e5f6,"[{""cid"":""c1"",""x"":120,""y"":45,""size"":""medium""},{""cid"":""c2"",""x"":160,""y"":80,""size"":""small""}]","[{""a"":""c1"",""b"":""c2""}]"
> Every image_id from the evaluation split must appear exactly once.
> Row sequencing is irrelevant, but missing identifiers, duplicated identifiers, or extraneous columns will trigger an immediate pipeline failure.
> What Not To Use
> Pre-existing Weights & External Data: This track is strictly "From Scratch". The integration of pretrained model weights, hosted embeddings, external corpora, or foundation-model priors is entirely banned.
> Hardware Envelope Restrictions: The submitted pipeline must execute entirely offline within 90 minutes. You are restricted to a maximum of 10 CPU cores and 62 GB of RAM. GPU acceleration is completely disabled.
> Evaluation-Set Contamination: Holdout records may only be queried for forward-pass inference. Employing holdout images to calibrate pseudo-labels, adjust topological thresholds, or modify internal statistical distributions is forbidden.
> Source Reconstruction: Do not attempt to bypass the challenge constraints by un-salting the opaque identifiers or hunting down original filenames.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Thermal Lattice Masked Encoder Training

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx766szrmjgsgzj9xrc1fgdnmd8c7501
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat ahmedtambal's score of 0.838!

Full challenge description from page:

> Leaderboard
> (16)
> Your Submissions
> Overview
> Build one spatial encoder for fixed 3 x 9 x 9 thermal-field tensors from metal deposition experiments. In the current plane, an interior 3 x 3 block is masked. For each row, infer four linked parts of that same field: nine masked-cell code indices, the ordering of those cells from hottest to coolest, the direction of global hotspot movement, and four whole-field zone counts.
> The four parts are generated from one thermal state and should be learned jointly. Complete deposition runs, rather than individual lattice examples, are separated between training and test data. This prevents related fields from one experiment appearing on both sides of the split.
> Do not use GPU acceleration. Pretrained models and external datasets are not allowed.
> Learning Setup
> Initialize the spatial encoder and all output heads randomly, then train them only on the released rows. The central modeling object is the shared lattice representation: masked-cell codes, heat rank, hotspot movement, and zone populations are coupled probes of that representation. Independent lookup tables or separately fitted heads do not capture the required cross-head structure.
> Dataset
> train.csv: labeled lattice windows.
> test.csv: unlabeled lattice windows.
> thermal_lattices.npz: float32 array windows with shape (rows,3,9,9).
> sample_submission.csv: random valid predictions.
> Columns are id (string), array_index (integer), masked_top and masked_left (integer coordinates of the hidden block), lattice_contract_json (JSON metadata), and, in training, answer_json (JSON target).
> lattice_contract_json contains array_shape ([3,9,9]), masked_patch_shape ([3,3]), temperature_bin_width (2 calibrated units), and temperature_bin_range ([0,900]). answer_json is an object containing hidden_temperature_bins (nine integers), hidden_heat_rank (nine position strings), hotspot_drift (string), and temperature_zone_counts (four integers); their valid values are defined below.
> The first two planes are complete readings 40 and 20 source steps before the current reading. The third plane is the current reading and contains -1 in the hidden block. Values outside the hidden block are row-locally calibrated temperature readings. Rows are selected from periods with the largest 40-step heat-field changes in each run.
> Target Record
> hidden_temperature_bins: nine row-major categorical code indices from 0 through 900. Adjacent indices represent a difference of 2 calibrated temperature units.
> hidden_heat_rank: a permutation of p00 through p22, hottest first.
> hotspot_drift: one of nw, n, ne, w, steady, e, sw, s, se.
> temperature_zone_counts: four nonnegative integers summing to 81. They count readings below 100 C, from 100 C to below 300 C, from 300 C to below 600 C, and at least 600 C.
> Evaluation
> For each temperature-bin or zone-count integer, exact agreement receives 1, an error of one receives 0.45, an error of two receives 0.15, and larger errors receive 0. Rank score is the exact-position rate across the nine entries. Hotspot drift uses exact match.
> The row score is 0.58*temperature_score + 0.20*rank_score + 0.12*hotspot_drift_exact + 0.10*zone_count_score. The final score is the mean over rows. Malformed row JSON scores zero. Wrong columns, missing ids, duplicate ids, or extra ids reject the submission.
> Submission
> Submit exactly id,answer_json in that order. answer_json must contain all four fields above. Use ordinary CSV quoting; inner JSON quotes must be doubled. See sample_submission.csv for the encoding.
> Two correctly quoted rows look like this:
> id,answer_json
> heat_19b3ac257f409de681,"{""hidden_temperature_bins"":[108,111,116,104,109,114,101,106,110],""hidden_heat_rank"":[""p02"",""p12"",""p01"",""p22"",""p11"",""p21"",""p00"",""p10"",""p20""],""hotspot_drift"":""ne"",""temperature_zone_counts"":[12,48,19,2]}"
> heat_b06743fe21d598ca04,"{""hidden_temperature_bins"":[84,87,90,82,86,89,80,83,88],""hidden_heat_rank"":[""p02"",""p12"",""p22"",""p01"",""p11"",""p21"",""p00"",""p10"",""p20""],""hotspot_drift"":""steady"",""temperature_zone_counts"":[24,50,7,0]}"

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Multisensor Grasp Phase Trace Challenge

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx747z3kek49hx4nksheq67nzd8c6ypv
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat singhking's score of 0.519!

Full challenge description from page:

> Leaderboard
> (15)
> Your Submissions
> Background
> Understanding human hand and arm dynamics is critical for applications in biomechanics, rehabilitation assessment, and advanced prosthetic control. While video-based hand tracking provides spatial information, interpreting the physical intent and effort of a grasp requires capturing the underlying muscular activation and kinematic movement.
> Multimodal sensor arrays—combining surface electromyography (sEMG) to measure muscle electrical activity with inertial measurement units (IMUs) to track acceleration and rotation—offer a rich window into these dynamics. The challenge lies in translating these continuous, noisy, and high-dimensional signal streams into discrete, meaningful action phases: precisely identifying when a user transitions from approaching an object, to securing a grasp, to finally releasing it.
> Overview
> The Multisensor Grasp Phase Trace challenge is a structured-prediction task requiring models to analyze multimodal time-series signals to classify hand posture and segment the temporal boundaries of a grasp action.
> To prevent simple baseline algorithms from overfitting, this dataset has been aggressively modified. The training distribution is severely capped to test zero-shot generalization, and the inputs contain intentionally injected distractor variables.
> Given a resampled 16-channel signal trial (combining accelerometer, gyroscope, sEMG data, and deterministic noise channels), algorithms must predict:
> A categorical posture token representing the overarching hand configuration.
> The exact start and end step indices for three strictly ordered temporal phases: approach, grasp, and release.
> This is a CPU-only, from-scratch challenge. It is explicitly designed as a structured temporal segmentation task, distinct from standard scalar classification or bounding-box regression benchmarks. Competitors must initialize their models randomly and learn strictly from the provided public training split.
> Dataset Public Files
> The provided dataset consists of structured CSV manifests mapping to a directory of compressed signal archives.
> train.csv: The primary training manifest containing trial IDs, metadata, sequence lengths, and the ground-truth posture and phase targets.
> test.csv: The held-out evaluation manifest containing only trial IDs, signal paths, and sequence lengths.
> sample_submission.csv: A valid template demonstrating the expected CSV layout and target JSON string escaping.
> task_metadata.json: An overarching configuration file defining valid posture categories, the sample rate (50 Hz), channel names, and split statistics.
> signals/: A directory containing .npz (NumPy compressed archive) files. Each file represents a single multimodal sensor trial.
> Dataset Information
> Core CSV Manifests
> +-----------------------+-------------+---------+-------------------------------------------------------------+
> | File                  | Column      | Type    | Description                                                 |
> +-----------------------+-------------+---------+-------------------------------------------------------------+
> | train.csv             | trial_id    | String  | Opaque identifier for the specific sensor trial.            |
> | train.csv             | signal_path | String  | Relative path to the .npz archive in the signals/ directory.|
> | train.csv             | n_steps     | Integer | Total number of temporal steps in the signal sequence.      |
> | train.csv             | posture     | String  | Target categorical posture label.                           |
> | train.csv             | phases_json | JSON    | Target temporal boundaries for the three grasp phases.      |
> | test.csv              | trial_id    | String  | Opaque identifier for the test sensor trial.                |
> | test.csv              | signal_path | String  | Relative path to the test .npz archive.                     |
> | test.csv              | n_steps     | Integer | Total number of temporal steps in the signal sequence.      |
> | sample_submission.csv | trial_id    | String  | Identifier corresponding directly to test.csv rows.         |
> | sample_submission.csv | posture     | String  | Your predicted posture label.                               |
> | sample_submission.csv | phases_json | JSON    | Your predicted temporal phase boundaries.                   |
> +-----------------------+-------------+---------+-------------------------------------------------------------+
> Signal Archive Structure (.npz files)
> Each trial file in the signals/ directory can be loaded via numpy.load() and contains the following arrays:
> +--------------+-------------------+-------------------------------------------------------------------------+
> | Array Key    | Shape/Type        | Description                                                             |
> +--------------+-------------------+-------------------------------------------------------------------------+
> | signal       | Float32 [N, 16]   | The primary temporal sequence data. N is the number of steps (n_steps). |
> |              |                   | 16 channels: 3x Accel, 3x Gyro, 8x sEMG, and 2x Distractor Noise.       |
> | sample_rate  | Int16 Scalar      | The standardized sample rate in Hz (50).                                |
> | channels     | String Array [16] | The ordered labels for the 16 channels (e.g., "acc_x", "distractor_1"). |
> +--------------+-------------------+-------------------------------------------------------------------------+
> Target JSON Schema (phases_json)
> The target JSON must be an array of exactly three objects, each defining a continuous phase.
> +--------+---------+--------------------------------------------------------------------------+
> | Field  | Type    | Description                                                              |
> +--------+---------+--------------------------------------------------------------------------+
> | phase  | String  | Must be exactly one of: "approach", "grasp", or "release".               |
> | start  | Integer | The 0-based index marking the beginning of the phase (inclusive).        |
> | end    | Integer | The index marking the end of the phase (exclusive).                      |
> +--------+---------+--------------------------------------------------------------------------+
> Evaluation Metrics
> Submissions are evaluated row-by-row against a hidden ground-truth set. This challenge strictly uses Hard Constraint Gates; models must achieve specific structural goals before any partial credit is awarded.
> For a given trial, let
> 𝑃
> P represent the predicted phases and
> 𝐺
> G represent the ground-truth phases.
> 1. Hard Constraint Gates (All-or-Nothing Prerequisites)
> Before any temporal bounding score is calculated, the prediction must perfectly satisfy two baseline requirements:
> Posture Match (
> 𝐴
> A): The predicted posture token must exactly match the ground-truth posture.
> Transition-Order Validity (
> 𝑉
> V): The predicted JSON array must contain exactly the 3 required phases in the correct temporal order, spanning the entire sequence without gaps or overlaps (i.e., start is
> 0
> 0, end equals n_steps, and adjacent phases seamlessly share boundaries).
> If either condition fails, the entire Row Score is strictly evaluated as 0.0.
> 2. Phase Overlap / IoU (
> 𝑂
> O)
> Evaluates the temporal Intersection over Union for each of the three named phases
> 𝑝
> ∈
> {
> approach
> ,
> grasp
> ,
> release
> }
> p∈{approach,grasp,release}. Note: An aggressive threshold floor is applied; any phase IoU below 0.50 yields
> 0.0
> 0.0 for that phase.
> 𝐼
> 𝑜
> 𝑈
> 𝑟
> 𝑎
> 𝑤
> (
> 𝑃
> 𝑝
> ,
> 𝐺
> 𝑝
> )
> =
> max
> ⁡
> (
> 0
> ,
> min
> ⁡
> (
> end
> 𝑃
> ,
> end
> 𝐺
> )
> −
> max
> ⁡
> (
> start
> 𝑃
> ,
> start
> 𝐺
> )
> )
> max
> ⁡
> (
> end
> 𝑃
> ,
> end
> 𝐺
> )
> −
> min
> ⁡
> (
> start
> 𝑃
> ,
> start
> 𝐺
> )
> IoU
> raw
> ​
> (P
> p
> ​
> ,G
> p
> ​
> )=
> max(end
> P
> ​
> ,end
> G
> ​
> )−min(start
> P
> ​
> ,start
> G
> ​
> )
> max(0,min(end
> P
> ​
> ,end
> G
> ​
> )−max(start
> P
> ​
> ,start
> G
> ​
> ))
> ​
> 𝐼
> 𝑜
> 𝑈
> (
> 𝑃
> 𝑝
> ,
> 𝐺
> 𝑝
> )
> =
> {
> 𝐼
> 𝑜
> 𝑈
> 𝑟
> 𝑎
> 𝑤
> (
> 𝑃
> 𝑝
> ,
> 𝐺
> 𝑝
> )
> if
> 𝐼
> 𝑜
> 𝑈
> 𝑟
> 𝑎
> 𝑤
> ≥
> 0.50
> 0.0
> otherwise
> IoU(P
> p
> ​
> ,G
> p
> ​
> )={
> IoU
> raw
> ​
> (P
> p
> ​
> ,G
> p
> ​
> )
> 0.0
> ​
> if IoU
> raw
> ​
> ≥0.50
> otherwise
> ​
> 𝑂
> =
> 1
> 3
> ∑
> 𝑝
> 𝐼
> 𝑜
> 𝑈
> (
> 𝑃
> 𝑝
> ,
> 𝐺
> 𝑝
> )
> O=
> 3
> 1
> ​
> ∑
> p
> ​
> IoU(P
> p
> ​
> ,G
> p
> ​
> )
> 3. Boundary Tolerance (
> 𝐵
> B)
> Awards partial credit for predicting boundaries that are highly precise, applying a steep non-linear exponential decay based on the total index distance. (Predictions that are merely "close enough" will drop sharply to zero).
> 𝐵
> 𝑝
> =
> exp
> ⁡
> (
> −
> ∣
> start
> 𝑃
> −
> start
> 𝐺
> ∣
> +
> ∣
> end
> 𝑃
> −
> end
> 𝐺
> ∣
> 6.0
> )
> B
> p
> ​
> =exp(−
> 6.0
> ∣start
> P
> ​
> −start
> G
> ​
> ∣+∣end
> P
> ​
> −end
> G
> ​
> ∣
> ​
> )
> 𝐵
> =
> 1
> 3
> ∑
> 𝑝
> 𝐵
> 𝑝
> B=
> 3
> 1
> ​
> ∑
> p
> ​
> B
> p
> ​
> Total Row Score
> Provided the constraint gates are passed, the individual row score aggregates the temporal metrics evenly:
> Row Score
> =
> 0.50
> ⋅
> 𝐵
> +
> 0.50
> ⋅
> 𝑂
> Row Score=0.50⋅B+0.50⋅O
> Final Leaderboard Score
> To heavily penalize models that overfit to common patterns while failing on edge-case subjects, the final metric heavily weights the minimum group (worst-subject) mean row score:
> Final Score
> =
> 0.70
> ⋅
> Mean
> (
> 𝑆
> row
> )
> +
> 0.30
> ⋅
> MinGroupMean
> (
> 𝑆
> row
> )
> Final Score=0.70⋅Mean(S
> row
> ​
> )+0.30⋅MinGroupMean(S
> row
> ​
> )
> (Scores are clipped strictly to
> [
> 0
> ,
> 1
> ]
> [0,1]. Exact matches yield a perfect
> 1.0
> 1.0. Invalid JSON syntax, extra fields, or structural violations immediately yield
> 0.0
> 0.0 for that specific row).
> Sample Submission Format
> Submit a UTF-8 encoded CSV file with exactly three columns in this order: trial_id, posture, phases_json. Ensure JSON payloads are correctly string-escaped using double quotes "".
> Code snippet
> trial_id,posture,phases_json
> grasp_a1b2c3d4e5f6,"Cylinder","[{""phase"":""approach"",""start"":0,""end"":45},{""phase"":""grasp"",""start"":45,""end"":120},{""phase"":""release"",""start"":120,""end"":180}]"
> Every trial_id from the test set must be present exactly once.
> Row order does not matter, but missing IDs, duplicate IDs, or unexpected formatting will invalidate the entire file.
> What Not To Use
> Pretrained Models & External Data: This is a strictly "From Scratch" track. The use of pretrained model weights, hosted embeddings, external signal corpora, or foundation-model features is prohibited. The training size has been artificially capped to punish data-hungry baselines.
> Hardware Envelope Restrictions: The solution must execute completely offline within 90 minutes. You are bound to a maximum of 10 CPU cores and 62 GB RAM. GPU usage is strictly disabled.
> Test-Set Leakage: Test rows may only be used for forward-pass inference. You are forbidden from using test rows to fit pseudo-labels, thresholds, or adapt statistical representations.
> Source Reconstruction: Do not attempt to infer targets by un-salting the prepared IDs or matching the signal sequences to upstream external copies of the dataset.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Walkway Vibration Footstrike Event Program Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ab40wjm52mvhy98h655sscs8azbj7
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat dongfuhan's score of 0.639!

Full challenge description from page:

> Leaderboard
> (9)
> Your Submissions
> # Walkway Vibration Footstrike Event Program Reconstruction
> This is a CPU From Scratch structured signal-decoding challenge. Each CSV row points to a real four-channel floor-vibration waveform. The central task is to train from the released rows and reconstruct a row-local footstrike event program: an ordered list of impacts with side, timing bin, and longitudinal walkway zone for unseen participants. It is not Computer Vision, Object Detection, tabular prediction, ordinary gait classification, or scalar regression.
> Overview
> Each row is a short walking passage captured only through synchronized floor-mounted vibration sensors and a stable sensor-layout file. Your task is to recover the complete event program for that passage: every foot strike in chronological order, the left/right striking foot, the onset-time bin, the longitudinal walkway zone, and a small auxiliary gait-mode label.
> The prepared corpus contains 746 public training rows and 301 public test rows from participant-disjoint adult walking trials. The recordings come from a real walkway-scale setup: four floor-mounted vibration sensors sampled at 500 Hz around an approximately 7.3-meter walking path. Each waveform channel measures footstep-induced floor vibration, so the solver must learn how impact timing, propagation, relative channel energy, and sensor geometry jointly explain the hidden strike program.
> The scored object is a coupled event program, not a bundle of independent gait parameters. A prediction that only identifies the gait style, counts steps, emits a generic alternating template, or finds large vibration peaks will miss core credit because every strike must be matched in time, left/right identity, zone, and order.
> The event-program contract is row-local and physical: the grader compares a predicted ordered route through strike times and walkway zones against the hidden ordered route for the same vibration segment. Gait mode is kept as a small 3 percent auxiliary output, so it cannot compensate for a wrong or incomplete strike program.
> Task
> For every test ID, submit:
> event_program: ordered tokens separated by > .
> gait_mode: one of NORMAL, FLEXED_KNEE, TOE_WALK, or FOOT_DRAG.
> Each event token has the form <foot>@<time_bin>:<zone_name>. The foot is L or R. The time bin is a zero-padded integer from 000 through 120, using 0.1-second bins. The zone name is the full token Z0, Z1, Z2, Z3, Z4, or Z5, ordered along the walkway.
> Example submission row:
> fp_abc123def4567890,L@018:Z2 > R@041:Z3 > L@066:Z4 > R@091:Z5,TOE_WALK
> Intended Approach
> Train a compact sequence model from random initialization on the supplied public training data. This is a multi-sensor footstrike event-program reconstruction problem in the From Scratch domain. Pretrained weights, external encoders, hosted models, and runtime-downloaded models are not permitted.
> A strong starting point uses a small 1D CNN or TCN over the four synchronized vibration channels, decodes per-bin footfall evidence, and applies a lightweight dynamic-programming or HMM-style sequence decoder for plausible event order. Other valid From Scratch routes include DSP peak candidates followed by learned event classification, multichannel relative-energy and time-difference features with a learned structured decoder, or a compact transformer trained only on the released train rows.
> The intended model should use the four-channel waveform and train labels together. Gait mode can be useful context, but it is intentionally auxiliary and cannot dominate the score.
> Public Files
> train.csv: public training rows with waveform path, sensor-layout path, sampling rate, duration metadata, event_program, and gait_mode.
> test.csv: public test rows with waveform path, sensor-layout path, sampling rate, and duration metadata only.
> signals/*.npy: float32 arrays with shape (n_samples, 4), one synchronized four-channel waveform per row. Values are normalized vibration amplitudes that preserve useful relative channel timing and energy; they are not calibrated physical engineering units.
> sensor_layout.json: stable four-sensor layout, legal gait modes, timing-bin constants, walkway dimensions, and zone definitions.
> sample_submission.csv: valid weak sample submission with the exact required columns.
> All paths in CSV files are relative to the public data root.
> The public sensor_layout.json is authoritative for geometry and legal constants. It records sampling_rate_hz = 500, time_bin_seconds = 0.1, max_time_bin = 120, legal gait modes, the six zone names Z0 through Z5, longitudinal zone edges in meters, approximate walkway dimensions, and four sensor entries. The sensor entries map stable channels to sensor names and positions: channel 0 is S1 at (3.31, 0.0) meters, channel 1 is S2 at (5.31, 0.0), channel 2 is S3 at (2.31, 2.0), and channel 3 is S4 at (4.31, 2.0).
> Train Columns
> id: opaque row ID with no source-row meaning.
> signal_path: relative path to the .npy waveform.
> sensor_layout_path: relative path to sensor_layout.json.
> sampling_rate_hz: integer sampling rate, always 500.
> n_samples: number of waveform samples.
> duration_s: row-local waveform duration.
> event_program: ordered training event sequence.
> gait_mode: training gait-mode label.
> Test Columns
> id: opaque row ID with no source-row meaning.
> signal_path: relative path to the .npy waveform.
> sensor_layout_path: relative path to sensor_layout.json.
> sampling_rate_hz: integer sampling rate, always 500.
> n_samples: number of waveform samples.
> duration_s: row-local waveform duration.
> The test file does not include event labels, gait labels, participant identifiers, original filenames, source timestamps, or source trial order.
> Submission
> Submit submission.csv with exactly these columns in this order: id, event_program, gait_mode.
> Requirements:
> The submitted ID set must exactly match test.csv.
> Each ID must appear exactly once.
> No missing, duplicate, unknown, or extra IDs are allowed.
> No extra columns, missing columns, or reordered columns are allowed.
> event_program must contain valid ordered event tokens separated by > .
> Invalid row-level event text or invalid gait-mode text scores zero for the affected row or head without exposing labels.
> Evaluation
> The final score is 0.97 times mean_event_program_score plus 0.03 times gait_mode_macro_f1.
> For one row, let R be the number of reference events and P be the number of predicted events. The grader computes several deterministic one-to-one greedy match sets. Candidate pairs are sorted by absolute onset-bin difference, then reference index, then prediction index. A predicted event can match at most one reference event, and a reference event can match at most one predicted event.
> Each row event-program score is:
> 0.68 times strict_token_f1
> + 0.14 times exact_time_f1
> + 0.10 times near_time_f1
> + 0.05 times count_score
> + 0.03 times strict_order_score
> The component formulas are:
> strict_token_f1 = 2 * M_strict / (P + R)
> where M_strict counts exact one-to-one matches with the same time bin, L/R foot, and zone
> exact_time_f1 = 2 * M_exact_time / (P + R)
> where M_exact_time counts exact-bin one-to-one matches without requiring foot or zone correctness
> near_time_f1 = 2 * M_near_time / (P + R)
> where M_near_time counts one-to-one matches within plus or minus one 0.1-second bin
> count_score = min(P, R) / max(P, R)
> strict_order_score = LIS(strict matched reference indices in predicted order) / M_strict when M_strict > 0, otherwise 0
> If P = R = 0, the row score is 1.0 only for mathematical completeness. Every scored hidden row contains real footstrike events, so an empty event program cannot exploit this edge case and receives 0 on nonempty rows.
> LIS is the length of the longest increasing subsequence. This metric is intentionally centered on complete event-token reconstruction: a row can receive small credit for near timing and count, but high scores require the same ordered foot, exact time bin, and zone tokens. Events farther away than one bin do not help any timing component. Gait mode is scored separately with macro F1 over NORMAL, FLEXED_KNEE, TOE_WALK, and FOOT_DRAG.
> Theoretical minimum is 0.0. Theoretical maximum is 1.0. A perfect oracle submission returns exactly 1.0.
> Compute
> This build follows the CPU-only task contract: train and infer within 1.5 hours on 10 CPU cores and 62 GB RAM. The challenge is framed as From Scratch only. A compact 1D CNN, TCN, or similar locally trained sequence model is the intended neural route; H100 or A10G hardware is unnecessary for the measured scale.
> What Not To Use
> Using these approaches can cause review rejection regardless of leaderboard score:
> Do not use upstream auxiliary annotation files, original source filenames, participant identities, source timestamps, source row order, or recovered source trial identity at inference time.
> Do not perform public-source waveform fingerprinting, checksum matching, nearest-neighbor retrieval against the raw corpus, or any lookup that maps prepared test rows back to hidden answers.
> Do not infer labels from row IDs, file sizes, file modification times, public CSV row order, absolute paths, or platform artifacts.
> Do not use pretrained waveform, audio, embedding, foundation, generative, or externally trained model weights. Train model parameters only from the released public training rows.
> Do not submit a gait-mode-only, event-template-only, scalar-regression-only, or ordinary peak-count solution as the final method.
> Do not use private answer files, hidden split construction, or grader behavior as a signal.
> Do not call hosted APIs or use external labels unavailable in the public training files.
> This is a gait-signal research benchmark. It is not a diagnostic system.
> Sample Submission Preview
> These are the literal header and first five rows of the generated sample_submission.csv. The complete file contains one row for every test ID and uses the same three-column order.
> id,event_program,gait_mode
> fp_008c7e8ac4cc0365,R@024:Z0 > L@031:Z0 > R@036:Z0 > L@042:Z1 > R@048:Z1 > L@053:Z2 > R@059:Z2 > L@065:Z2 > R@071:Z3 > L@077:Z3,NORMAL
> fp_00dae1a35e7fcc2e,R@020:Z5 > L@026:Z5 > R@032:Z5 > L@037:Z4 > R@042:Z4 > L@048:Z3 > R@055:Z3 > L@061:Z2 > R@067:Z2 > L@073:Z1,NORMAL
> fp_0280e54981e9c61c,L@022:Z5 > R@028:Z4 > L@034:Z4 > R@039:Z3 > L@045:Z2 > R@049:Z1 > L@055:Z1 > R@060:Z0 > L@066:Z0,NORMAL
> fp_02d3b89f65ada52e,R@010:Z0 > L@015:Z1 > R@020:Z1 > L@025:Z2 > R@032:Z3 > L@038:Z3 > R@043:Z4 > L@048:Z5 > R@053:Z5 > L@059:Z5,NORMAL
> fp_03aee985bdeaed11,R@017:Z0 > L@024:Z0 > R@029:Z1 > L@035:Z1 > R@040:Z2 > L@045:Z3 > R@051:Z3 > L@057:Z4 > R@064:Z5 > L@070:Z5,NORMAL

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Pediatric Wrist Finding Occupancy Grids

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7ahx6wmwde3c4r932p0661kn8c4f6e
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: Not shown/captured
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat jesuisnadi's score of 0.556!

Full challenge description from page:

> Leaderboard
> (7)
> Your Submissions
> Pediatric Wrist Finding Occupancy Grids
> Overview
> Each item is a single pediatric wrist radiograph. The task is to learn — from raw pixels, with a model trained from scratch — a coarse spatial field describing where clinically annotated findings sit inside the image. The image is partitioned into a fixed 5×5 grid of 25 cells, and for every cell you must output the probability that the cell overlaps at least one annotated abnormality (fracture, foreign body, implant, periosteal reaction, bone lesion, bone anomaly, soft-tissue swelling, or pronator-quadratus sign).
> The competition supplies only the raw grayscale radiographs and, for the training split, the per-cell occupancy labels. No pretrained image backbones may be used — the entire difficulty is in learning a spatial representation of wrist anatomy and injury from a modest labeled corpus. The task is hard because findings are small, spatially concentrated, and highly imbalanced across cells. Each per-cell probability is scored on two axes: discrimination — for each cell, whether images that actually have a finding there are scored above images that do not — and magnitude fidelity — whether the probability value matches the true occupancy rate rather than merely ordering images correctly. Both axes give credit only above the population occupancy field, so a model that outputs the population-average occupancy for every image earns nothing on either axis; positive credit requires reading the pixels of this radiograph to say both which images have a finding in each cell and how strongly.
> Dataset
> Public files
> train.csv — one row per training radiograph, with per-cell occupancy labels.
> Columns: id, image, group_id, cell_0 … cell_24
> test.csv — one row per test radiograph. No labels.
> Columns: id, image
> images/ — grayscale PNG radiographs referenced by the image column (train and test images share this directory; test images carry no label anywhere in the public release).
> sample_submission.csv — a valid, correctly-shaped submission holding the population per-cell base-rate field (the same fixed 25-value vector in every row).
> Private file (organizer only)
> answers.csv — columns id, cell_0 … cell_24 — the held-out per-cell occupancy labels for the test split.
> Column descriptions
> The public CSVs use the following columns:
> id (string) — unique identifier for a radiograph row (generic token; no source information encoded).
> image (string) — filename of the radiograph inside images/ (e.g. img_a1b2c3d4e5f6a7b8.png).
> group_id (string) — anonymized patient grouping identifier, present in train.csv only. Multiple radiographs may share a group_id; use it to build patient-disjoint local cross-validation folds. It is deliberately absent from test.csv.
> cell_0 … cell_24 (int, 0 or 1) — training labels only. The image is divided into a 5×5 grid indexed row-major (cell_0 is the top-left cell, cell_4 the top-right, cell_24 the bottom-right). A cell is 1 if at least one annotated abnormality region overlaps that cell by area, else 0.
> The grid indexing (row-major, 5 columns × 5 rows) is the same for every image regardless of aspect ratio: cell boundaries are computed as equal fractional splits of the image width and height.
> Data example
> A truncated train.csv row:
> id,image,group_id,cell_0,cell_1,cell_2,...,cell_12,cell_13,...,cell_24
> r_0000af31,img_a1b2c3d4e5f6a7b8.png,grp_5c1e,0,0,0,...,1,1,...,0
> Submission format
> Submit a CSV named submission.csv with exactly these 26 columns:
> id,prob_0,prob_1,...,prob_24
> Exactly one row per id in test.csv (no missing ids, no unknown ids, no duplicates).
> prob_i is the predicted probability in [0, 1] that grid cell i overlaps at least one finding. The 25 values are independent per-cell probabilities and do not need to sum to 1.
> Every row must contain all 25 probability columns; blank cells are not allowed.
> Header row required.
> Sample submission — the population per-cell base-rate field (the same fixed vector in every row; this is the metric's chance baseline and encodes only the population spatial prior, which earns no credit):
> id,prob_0,prob_1,...,prob_12,...,prob_24
> r_0000af31,0.003,0.008,...,0.567,...,0.007
> r_0000c92d,0.003,0.008,...,0.567,...,0.007
> Evaluation
> Metric: macro Grid Occupancy Fidelity (GOF). Each per-cell probability is scored on two axes — a discrimination term (how well it orders images by whether the cell is occupied) and a magnitude term (how well its value matches the true occupancy rate) — each macro-averaged over the active cells and blended with a fixed weight ALPHA = 0.80 on the magnitude term.
> For each cell c ∈ {0..24}, let y_ic ∈ {0,1} be the true occupancy of cell c in test image i, p_ic the submitted probability, and b_c the cell's population occupancy rate over the test split. Over all N test images:
> # --- axis 1: discrimination (ordering) ---
> AUC_c    = P( p_ic > p_jc | y_ic = 1, y_jc = 0 )   # ROC-AUC via the Mann-Whitney
> # U statistic; ties credited at 0.5
> gini_c   = max(0, 2 * AUC_c - 1)                    # 0 = chance ordering, 1 = perfect
> # --- axis 2: magnitude (squared-error reduction over the population field) ---
> sqerr_c  = mean_i (p_ic - y_ic)^2                   # mean squared error of the probability field
> ref_c    = b_c * (1 - b_c)                          # squared error of the constant population field b_c
> mag_c    = max(0, 1 - sqerr_c / ref_c)             # 0 = no better than the population field, 1 = perfect
> # active cells: those whose population occupancy rate b_c is in [0.02, 0.98] (both classes present)
> discrimination = mean_c(active) gini_c
> magnitude      = mean_c(active) mag_c
> headline = ALPHA * magnitude + (1 - ALPHA) * discrimination   # ALPHA = 0.80
> score    = max(0.02, min(1.0, headline))                      # clamp to [0.02, 1.0]
> Scoring notes (all applied inside grade()):
> Two axes, blended 0.80 / 0.20. The headline is 0.80 × magnitude + 0.20 × discrimination. The discrimination axis depends only on the ordering of the probabilities across images; the magnitude axis additionally depends on their value. A submission that orders images perfectly but is wildly over- or under-valued scores full marks on discrimination yet 0 on magnitude, so it cannot exceed 0.20.
> Both axes are floored at 0 per cell (max(0, …)) before averaging, so a single badly-ordered or badly-valued cell cannot drag the headline negative; each cell contributes only credit above chance ordering / above the population field.
> The population field is the reference. ref_c = b_c(1 - b_c) is the squared error of the best constant predictor (the population occupancy rate itself). The magnitude term measures the fractional reduction in squared error below that constant field: a submission must beat per-image what the population field achieves, which requires using the image.
> Discrimination ties credited at 0.5. Ties are resolved with Mann-Whitney midranks, so a constant prediction scores exactly AUC_c = 0.5 → gini_c = 0, and an information-free perturbation of a constant field cannot improve the discrimination axis.
> Active cells only. A cell whose population occupancy rate is below 0.02 or above 0.98 has too few of one class to score reliably and is excluded; both means are equal-weight over the remaining active cells, weighting sparse peripheral cells and dense central cells equally.
> **A constant / population-field submission earns 0** on both axes (gini_c = 0 from ties; mag_c = 0 because it is the population field) and lands at the 0.02 floor.
> Higher is better. Score is clamped to [0.02, 1.0].
> Grade direction: Maximize. Score bounds: Min = 0.02, Max = 1.0.
> Chance baseline: a constant field, or any submission that reproduces the per-cell population occupancy rates without using image content, earns 0 on both axes (AUC_c = 0.5 → gini_c = 0; mag_c = 0) and lands at the 0.02 floor.
> What Not To Use (Prohibited Methods)
> This challenge scores a learned-from-scratch spatial representation of the radiograph. The following are prohibited:
> No pretrained weights of any kind. Models must be trained from scratch on the provided train.csv images only. Do not initialize from ImageNet, RadImageNet, medical foundation models, or any externally pretrained backbone, encoder, or feature extractor. The task is a from-scratch representation-learning problem; transfer learning defeats its purpose.
> No external radiograph datasets, annotations, or answer keys. Do not download, match, or align the test images against any external wrist / pediatric / musculoskeletal radiograph collection, and do not use any external bounding boxes, segmentation masks, occupancy grids, or lesion annotations to reconstruct test labels.
> No image re-identification. Do not attempt to match test images (by pixel content, perceptual hash, embedding similarity, DICOM/PNG artifacts, or reverse image search) back to any public image corpus in order to recover their annotations.
> No id- or filename-based hardcoding. Do not map id or image values to memorized targets, and do not exploit any ordering, hashing, or grouping structure of the ids to infer labels.
> No train/test leakage or private-label tuning. Do not use group_id to link train and test rows (it is not present in the test split), and do not tune against the private answer file.
> No manual labeling of the test set. Test occupancy grids must be produced by your trained model, not by human inspection of the radiographs.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Match Marine Casualty Reports to Motion Evidence

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx76akgh5da5m6f5n097k52b958c5vc1
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: text, feature-engineering, small-data, multimodal, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.346

Full challenge description from page:

> Match Marine Casualty Reports to Motion Evidence
> Overview
> Your task is to identify which of eight anonymous vessel-motion records belongs to a protected marine-casualty report. For every case, rank all eight candidate IDs from most likely to least likely.
> The authentic target comes from the source corpus's confirmed Coast Guard investigation-to-AIS linkage. Preparation selects at most one case per MMSI and never uses the traffic normal pool as a decoy source. Each slate contains the authentic incident-day track plus seven confirmed incident-day tracks from other cases in the same split. Candidate IDs C0 through C7 are local to one case and carry no meaning across cases.
> Raw report prose, vessel names, MMSI, IMO, official numbers, case identifiers, dates, timestamps, coordinates, ports, and waterway names are not public. Reports are converted into a finite nonverbatim event ontology. Motion observations are reduced to coarse day-level bands and within-slate ordinal relationships.
> Dataset
> The public directory contains:
> train.jsonl
> validation.jsonl
> test.jsonl
> schema.json
> dataset_summary.json
> sample_submission.csv
> The deterministic preparation applies this count funnel:
> | Stage | Rows remaining | Explanation |
> | --- | ---: | --- |
> | Confirmed source links | 2,680 | All confirmed investigation-to-MMSI rows before challenge filtering. |
> | One selected row per MMSI | 2,046 | 634 additional rows are removed because their MMSI already has a selected row. |
> | Prepared challenge cases | 2,045 | One selected MMSI has no usable incident-day motion summary. |
> | Training split | 1,348 | Labeled rows in train.jsonl. |
> | Validation split | 276 | Labeled rows in validation.jsonl. |
> | Test split | 421 | Unlabeled rows in test.jsonl; labels are private. |
> The split counts sum to the prepared total: 1,348 + 276 + 421 = 2,045. The source total 2,680 is therefore a pre-deduplication quantity, not the expected sum of the three prepared splits.
> Every JSONL row is one JSON object with:
> case_id string): Q followed by sixteen uppercase hexadecimal characters;
> report_card object): a nonverbatim structured casualty description;
> candidate_motion_cards array<object>): exactly eight cards with local IDs C0 through C7; and
> target_candidate_id string): the authentic candidate ID, present only in train.jsonl and validation.jsonl.
> report_card contains these string or string-array fields:
> vessel_group string): one of FISHING, TUG_TOW, PASSENGER, CARGO, TANKER, or OTHER.
> event_types array<string>): one or more of GROUNDING, COLLISION, ALLISION, FIRE_OR_OVERHEAT, FLOODING, PROPULSION_LOSS, STEERING_LOSS, POWER_LOSS, MACHINERY_FAILURE, PERSON_OVERBOARD, CAPSIZE_OR_SINKING, POLLUTION_EVENT, or fallback OTHER_REPORTABLE_EVENT.
> operating_context array<string>): one or more of UNDERWAY, MOORED_OR_DOCKED, ANCHORED, TOWING_OPERATION, FISHING_OPERATION, CONFINED_WATERWAY, OFFSHORE_OPERATION, ADVERSE_ENVIRONMENT, or fallback UNSPECIFIED_CONTEXT.
> reported_consequences array<string>): one or more of INJURY, FATALITY, DAMAGE, POLLUTION, LOSS_OF_CONTROL, NO_REPORTED_INJURY, NO_REPORTED_DAMAGE, or fallback UNSPECIFIED_CONSEQUENCE.
> response_actions array<string>): one or more of SHUTDOWN, TEMPORARY_REPAIR, TOW_OR_ESCORT, EVACUATION_OR_RESCUE, RETURNED_TO_SERVICE, or fallback UNSPECIFIED_RESPONSE.
> Each candidate motion card contains:
> candidate_id string): one of C0 through C7.
> vessel_type_group string): one of FISHING, TUG_TOW, PASSENGER, CARGO, TANKER, OTHER, or MISSING.
> length_group string): one of LE_15_M, 15_30_M, 30_60_M, 60_120_M, GT_120_M, or MISSING.
> motion_profile object), with four string fields:
> reporting_density_band: SPARSE, MODERATE, DENSE, or VERY_DENSE;
> mean_speed_band: MOSTLY_STATIONARY, SLOW_OR_MANEUVERING, MODERATE_TRANSIT, or FAST_TRANSIT;
> underway_share_band: RARELY_UNDERWAY, MIXED, or MOSTLY_UNDERWAY; and
> daily_extent_band: LOCAL, REGIONAL, BROAD, or LONG_RANGE.
> within_slate_rank object): the same four motion dimensions, each represented by LOWEST, LOWER, MIDDLE, HIGHER, or HIGHEST.
> Candidates are drawn after splitting. Preparation prefers confirmed tracks with the same broad AIS type and length band as the target, falls back to type-only pools when necessary, and uses a stage-wide pool only when fewer than eight same-type cases exist. Target positions are balanced to within one case in every split.
> Submission
> Write ./working/submission.csv with exactly these columns in this order:
> case_id,ranked_candidate_ids
> Q0123456789ABCDEF,"[""C3"",""C1"",""C6"",""C0"",""C5"",""C2"",""C7"",""C4""]"
> Include every test case_id exactly once. ranked_candidate_ids must be either:
> a JSON list containing a complete permutation of C0 through C7, ordered best to worst; or
> the exact JSON empty list [], which abstains for that case.
> Partial rankings, duplicate or unknown candidate IDs, malformed JSON, non-string items, missing or extra cases, duplicate case IDs, and reordered or additional CSV columns are rejected.
> Evaluation
> For a non-abstaining case, let r be the one-indexed rank of the authentic candidate. Its normalized reciprocal-rank score is:
> (8 / r - 1) / 7
> The official score is the macro mean across all test cases. Higher is better. The range is [0, 1]: rank one scores 1, rank eight scores 0, and abstention scores 0. The supplied sample abstains on every case and therefore scores exactly 0; an oracle scores exactly 1.
> Modeling Rules
> Use only the public challenge files. The intended CPU approach trains all parameters from scratch on the labeled training cases, uses validation cases for model selection, scores the eight report-card/motion-card pairs, and converts scores into a full ranking.
> External corpora, source-corpus lookup, reverse identification of protected cases, private-file access, solve-time internet, external APIs, downloads, package installation, and pretrained model assets are prohibited. The complete solution must load the public files, fit, infer, and write ./working/submission.csv within the assigned CPU job.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Level–Flow Series Pairing Across Disjoint Periods

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx736qe16r1ncyas0d2eg6v0n98bxy9k
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.966

Full challenge description from page:

> Overview
> This is a from-scratch challenge: models are trained from scratch on the
> provided time series. No pretrained weights are used, required, or expected.
> A river gauging station does not measure flow. It measures water level, and
> converts level into flow using a rating curve fitted to its own channel geometry.
> Every channel has a different cross-section, so the level-to-flow relationship is
> a property of the site.
> Each case gives 15 water level series and 15 river flow series recorded at the
> same 15 stations, shuffled independently. Recover which flow series shares a
> station with which level series.
> What is being learned, stated precisely. The two series in a pair come from
> different time periods and are each normalised by their own median, so the
> station's transfer function is not identifiable from them: an arbitrary unknown
> monotone transfer, composed with a hydrologic input distribution that itself
> changes between the two periods, cannot be pinned down from two marginals alone.
> This task does not ask for that transfer function and does not score it. What is
> learnable, and what the reference exploits, is a **station-invariant statistical
> fingerprint associated with rating-curve shape** — regularities that hold across
> stations well enough to tell which level record and which flow record came from
> the same channel, without ever identifying the channel's response curve.
> Prediction Objective
> For each case, output a one-to-one pairing: for every level slot, the flow
> slot recorded at the same station. Every flow slot must be used exactly once.
> The pairing is a permutation, not fifteen independent decisions. Assigning a flow
> to one level removes it from every other.
> Why This Is Not Series Matching
> The familiar version of this problem — planted matching, graph alignment,
> matching correlated time series — assumes the two collections **share a
> realisation**: two views of one process, co-observed, differing by noise.
> Correlation is then both signal and solution.
> That assumption does not hold here, by construction:
> The periods do not overlap. Level is drawn from the first half of the record
> and flow from the second. The two series in a true pair were never simultaneously
> observed and share no weather, no storm, no realisation.
> This was measured during construction. In a 50-station variant where level and
> flow were released over the same period, correlating the two series and solving
> the assignment optimally recovered the pairing at 0.9705, against a chance level
> of 1/50 = 0.02. After the periods were split so that no pair shares a time window,
> the strongest non-learned method found scores 0.1669 at 15 stations.
> The two modalities are different quantities. Level is a distance, flow is a
> volume rate.
> Magnitude is removed. Each series is divided by its own median, so a large
> river cannot be matched to a large river by size.
> What survives is how a site behaves: how sharply it responds, how it recedes
> after a peak, how its flow distribution is stretched relative to its level
> distribution. These are statistical consequences of channel geometry, and they
> transfer across stations — which is what makes the task learnable without the
> transfer function being identifiable.
> Dataset
> train.csv — 361 cases. test.csv — 86 cases, same columns without
> answer_json. sample_submission.csv — 86 rows, a valid placeholder.
> train.csv
> | Column | Type | Description |
> |---|---|---|
> | case_id | string | Unique opaque case identifier, e.g. case_00e2da30c696 |
> | levels_json | string (JSON) | Array of 15 arrays; each inner array is 504 floats — 21 days of hourly mean water level, divided by that series' own median, 4 decimals |
> | flows_json | string (JSON) | Array of 15 arrays in the same format, holding river flow from a different, non-overlapping period |
> | station_count | int | Stations in the case. Always 15 |
> | answer_json | string (JSON) | Ground truth: {"pairing": [...]}, a permutation of 0–14 |
> test.csv
> case_id (string), levels_json (JSON string), flows_json (JSON string),
> station_count (int).
> How the slots line up
> Position in levels_json is the level slot; position in flows_json is the flow
> slot. The two orderings are shuffled independently, so slot i in one has no
> relationship to slot i in the other.
> In answer_json, element i of pairing is the flow slot belonging to level
> slot i: pairing[0] == 7 means level slot 0 and flow slot 7 were recorded at
> the same station.
> Splits are station-disjoint. No gauging station contributes to both files, so
> a solver cannot memorise one site during training and reuse it. Test stations are
> unseen, and slot or case memorisation does not transfer.
> Evaluation
> Scored by chance-corrected pairing accuracy, averaged over test cases.
> For each case, with n stations:
> score = (fraction correctly paired - 1/n) / (1 - 1/n)
> With n = 15, chance is 1/15 ≈ 0.0667 correct fraction (i.e., on average 1 out of
> 15 pairs correct), which maps to a score of 0.0. A perfect pairing scores 1.0.
> The mean across cases is clipped to [0, 1].
> Because a random permutation is the zero point, no hedging strategy has a
> positive expected score. Any pairing chosen without reading the data has an
> expected score of exactly 0.0; the identity pairing measures 0.0075 on this test
> split, which is sampling noise across 86 cases.
> Submission
> A CSV with exactly two columns, case_id and prediction_json, one row per test
> case — no more and no fewer:
> case_id,prediction_json
> case_00e2da30c696,"{""pairing"":[3,7,0,11,2,14,5,1,9,4,13,6,8,12,10]}"
> case_031e3925d937,"{""pairing"":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]}"
> pairing must be a permutation of 0 to 14. The grader requires the submission's
> case id set to match the test set exactly: unknown ids, missing ids, duplicated
> ids and extra columns are all rejected.
> Rules
> No external data. Do not fetch, reconstruct, or join against Environment
> Agency feeds or any other hydrometric source.
> No hardcoded predictions. Do not embed case-to-answer maps.
> No test labels. Fit and tune on train.csv only.
> No external packages beyond those preinstalled in the runtime. The
> reference needs only numpy, pandas, scipy and scikit-learn. Run
> pip list if unsure.
> Reference Points
> Measured through the shipped grader on the held-out split:
> | | score |
> |---|---|
> | any fixed pairing, e.g. the identity (expected 0.0) | 0.0075 |
> | strongest hand-built method found during construction | 0.1669 |
> | reference solution, learned, CPU, about one minute | 0.3164 |
> The reference is a floor. It characterises each series independently before
> pairing, discarding the fact that within a case every assignment constrains the
> others, and it summarises 504 points into a fixed handful of numbers before any
> learning happens.
> Relation to Prior Work
> The scientific kernel is not new and the closest work is worth naming.
> Tourian et al. (2013), quantile-function discharge estimation from satellite
> altimetry, is the nearest neighbour: it maps non-overlapping stage and discharge
> records onto each other through their quantile functions. It solves a known
> correspondence for one station at a time and is scored on discharge error. Here
> the correspondence is the unknown, fifteen candidates compete under a one-to-one
> constraint, and scoring is chance-corrected pairing accuracy.
> Le Coz et al. (2014), BaRatin and **Mansanarez et al. (2019), Stage-Period-
> Discharge models** estimate rating curves and their uncertainty from gaugings at
> known times. Both assume the pairing is given; they are the inverse of this task.
> Elmi (2021) and related nonparametric quantile-mapping extensions inherit the
> assumption of known station identity.
> None addresses the combinatorial layer. Median normalisation removes the
> magnitude cue quantile mapping leans on, station-disjoint splits forbid fitting a
> curve per site, and the one-to-one constraint couples every assignment. This task
> deliberately does not attempt what those methods do — it does not estimate a
> rating curve, and does not claim the transfer function is recoverable from the
> released data.
> Runtime
> The solution must run end to end inside the notebook, reading from
> ./dataset/public/ and writing ./working/submission.csv, within the platform
> time limit. CPU only — no accelerator is required or assumed.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## RelMix: From-Scratch Relation Profile Reconstruction

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7507vvb60p6t7te5x8dbxtjn8bxtvn
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering, large-scale, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.565

Full challenge description from page:

> RelMix: From-Scratch Relation Profile Reconstruction
> Problem domain: From scratch
> Overview
> Wikidata is a large, community-maintained database of facts about the real
> world. It records entities such as people, places, organisations, films and
> species, and connects them with typed relations, sometimes called properties.
> A relation is a labelled fact type: for example "occupation", "country of
> citizenship", "educated at", or "member of". A single entity can use the same
> relation several times over, since a person may hold three occupations or two
> citizenships. Wikidata5M is a standard research extract of that database,
> containing about 21 million such facts.
> For any entity you can count, for each relation, how many times that entity uses
> it. Those 16 counts form the entity's outgoing relation profile, and that
> profile is what you must reconstruct. Rather than exact counts, each is reduced
> to an activity tier: whether the entity uses the relation not at all, once,
> a few times, or many times.
> The profile itself is never published. What you receive is context around the
> entity: quantised summaries of the facts that point at it, and of what its
> neighbouring entities look like, with five of the eight context groups hidden.
> Nothing computed from the entity's own outgoing facts appears anywhere in the
> released files.
> The identities of the 16 relations are not published, so they cannot be looked
> up. Your task is to infer, from context alone, how active each of the 16
> relations is for each entity.
> All models train from scratch on the provided data. No pretrained model,
> external graph or lookup service is required or permitted.
> Task
> For every test case, predict 16 outputs, tier_r00 through tier_r15, each an
> integer from 0 to 3:
> | Tier | Meaning | Outgoing occurrences |
> |---:|---|---|
> | 0 | entity never uses this relation | none |
> | 1 | entity uses it once | exactly one |
> | 2 | entity uses it a few times | 2 to 4 |
> | 3 | entity uses it many times | 5 or more |
> Why this is inference, not decoding
> No released number sums, counts or approximates a scored relation. There is no
> coarse outgoing total, no outgoing degree, and no missing-value pattern that
> depends on the target. The only route to an answer is statistical: the visible
> context indicates what kind of entity this is, and the kind of entity predicts
> how active each relation will be.
> The released view is also non-identifying. On the shipped test split, 97.82% of
> rows share their exact released view with at least one other row, and the
> largest identical-view bucket holds 114 rows. A released view does not pick out
> the entity it came from.
> Dataset
> train.csv        40,000 rows, context + targets
> validation.csv    8,000 rows, context + targets
> test.csv         12,000 rows, context only
> sample_submission.csv
> metadata.json
> [README.md](http://README.md)
> Splits are disjoint: no entity appears in more than one split.
> Input columns
> Present in train.csv, validation.csv and test.csv.
> | Column | Type | Description |
> |---|---|---|
> | case_id | string | Opaque, split-local identifier for one entity |
> | inc_stream | string | Eight space-separated tokens: incoming activity per coarse group |
> | nbr_stream | string | Eight space-separated tokens: neighbour profile per coarse group |
> | degree_stream | string | Four space-separated tokens: aggregate context summaries |
> Target columns
> Present in train.csv and validation.csv only. These are the values you
> predict for test.csv.
> | Column | Type | Description |
> |---|---|---|
> | tier_r00 | integer 0 to 3 | Activity tier of hidden relation 0 for this entity |
> | tier_r01 | integer 0 to 3 | Activity tier of hidden relation 1 |
> | tier_r02 | integer 0 to 3 | Activity tier of hidden relation 2 |
> | tier_r03 | integer 0 to 3 | Activity tier of hidden relation 3 |
> | tier_r04 | integer 0 to 3 | Activity tier of hidden relation 4 |
> | tier_r05 | integer 0 to 3 | Activity tier of hidden relation 5 |
> | tier_r06 | integer 0 to 3 | Activity tier of hidden relation 6 |
> | tier_r07 | integer 0 to 3 | Activity tier of hidden relation 7 |
> | tier_r08 | integer 0 to 3 | Activity tier of hidden relation 8 |
> | tier_r09 | integer 0 to 3 | Activity tier of hidden relation 9 |
> | tier_r10 | integer 0 to 3 | Activity tier of hidden relation 10 |
> | tier_r11 | integer 0 to 3 | Activity tier of hidden relation 11 |
> | tier_r12 | integer 0 to 3 | Activity tier of hidden relation 12 |
> | tier_r13 | integer 0 to 3 | Activity tier of hidden relation 13 |
> | tier_r14 | integer 0 to 3 | Activity tier of hidden relation 14 |
> | tier_r15 | integer 0 to 3 | Activity tier of hidden relation 15 |
> All 16 targets use the identical tier scale defined in the Task section. Each
> column refers to one specific relation, consistent across every row and every
> split. The relation identities are withheld, so the columns are named
> positionally.
> Stream encoding
> Streams are space-separated integers, for example:
> 9 9 0 3 0 9 9 9
> Quantisation. Token 0 means a count of 0, token 1 means 1, token 2 means 2,
> token 3 means 3, token 4 means 4 to 5, token 5 means 6 to 9, token 6 means 10 to
> 20, and token 7 means 21 or more. The value 9 marks a withheld group.
> Withholding. Exactly five of the eight coarse groups are withheld per case,
> at the same positions in inc_stream and nbr_stream. Which five varies by
> case.
> inc_stream* gives incoming activity across the eight coarse groups, that
> is, how many facts point at this entity. Note that this population is rarely the
> target of these relations, so incoming tokens are zero in the large majority of
> cases. nbr_stream carries most of the usable signal.
> nbr_stream* gives the quantised mean outgoing profile of up to 16
> neighbouring entities. This describes other entities, not the case entity.
> degree_stream* holds four tokens, in order: summed incoming activity over
> the visible groups, sampled neighbour count, mean relation diversity of those
> neighbours, and the number of visible groups with non-zero incoming activity.
> Grouping. The 16 relations map to 8 coarse groups, two per group. The exact
> assignment is published in metadata.json as group_membership. It is a stated
> fact, not something to reverse-engineer.
> Submission format
> Exactly 17 columns: case_id, then tier_r00 through tier_r15, matching
> sample_submission.csv.
> case_id,tier_r00,tier_r01,tier_r02,tier_r03,tier_r04,tier_r05,tier_r06,tier_r07,tier_r08,tier_r09,tier_r10,tier_r11,tier_r12,tier_r13,tier_r14,tier_r15
> tes_0123456789abcdef0123,0,1,0,2,0,0,1,0,0,0,0,1,0,0,0,0
> Every test case_id must appear exactly once, and every value must be an
> integer from 0 to 3. Row order does not affect the score.
> A submission scores 0.0 if it has wrong, missing, extra or reordered columns; if
> it is empty; if a case_id is missing, repeated or unknown; or if any cell is
> blank, non-numeric, fractional or outside the range 0 to 3. Tiers written in
> decimal form such as 2.0 are accepted, and a stray unnamed index column is
> tolerated. The grader accepts either the complete test submission or the exact
> leaderboard slice supplied by the platform.
> Evaluation
> The challenge uses balanced macro-recall over tiers.
> Notation
> For N graded cases and 16 relations, let y[i][j] be the true tier of relation
> j for case i, and p[i][j] be the predicted tier. Let M = 10 be the minimum
> support a tier needs to count.
> Formula
> For relation j and tier t, the number of cases truly at that tier is:
> n[j][t] = count of i where y[i][j] == t
> A tier is scored only if it has enough support. The set of scored tiers for
> relation j is:
> S[j] = { t in {0,1,2,3} : n[j][t] >= M }
> For each scored tier, recall is the fraction of those cases predicted correctly:
> recall[j][t] = ( count of i where y[i][j] == t and p[i][j] == t ) / n[j][t]
> The score for relation j is the unweighted mean of its scored-tier recalls, and
> relation j is included only if at least two of its tiers are scored:
> score[j] = ( sum over t in S[j] of recall[j][t] ) / |S[j]|      when |S[j]| >= 2
> Let J be the set of relations satisfying that condition. The final score is:
> final score = ( sum over j in J of score[j] ) / |J|
> Properties
> Scores range from 0.0 to 1.0, and higher is better. A perfect reconstruction
> scores 1.0.
> Because each tier contributes equally regardless of how common it is, predicting
> the most common tier everywhere cannot win: it earns recall 1.0 on that one tier
> and 0.0 on every other, so score[j] is at most 1 / |S[j]|.
> The support floor M = 10 exists for stability. Recall measured on a handful of
> rows has resolution 1/n and is mostly noise.
> One consequence follows directly from the formula: the metric is **not additive
> across slices**. On a smaller graded set, fewer tiers reach M, so |S[j]|
> shrinks and a constant predictor scores higher. A constant submission scores
> 0.3021 on the full 12,000-row test set and about 0.3507 on a 25 percent slice.
> All ladder figures below are measured on the full test set.
> Measured solver ladder
> Measured on the shipped pipeline, full 12,000-row test set:
> | Approach | Score |
> |---|---:|
> | Random tiers | 0.2527 |
> | All-zero, majority tier, or best constant per relation | 0.3021 |
> | Per-relation gradient boosting with prior-power decoding | 0.4862 to 0.4893 |
> | Perfect reconstruction | 1.0000 |
> Three independent solver runs on this pipeline scored 0.4575, 0.4689 and 0.5054.
> A learned model roughly doubles the gap between the constant floor and the
> ceiling, but captures only part of the available headroom. The context
> constrains the profile without determining it.
> Suggested approaches
> Per-relation gradient boosting, random forests, multinomial linear models,
> shallow neural networks, multi-output estimators, chained models that condition
> each output on earlier ones, and ensembles of relation-specific predictors.
> Because the metric weights each tier equally, decoding matters as much as the
> model. Re-weighting predicted probabilities against the class prior is typically
> worth more than extra model capacity.
> Useful feature engineering includes expanding each stream position into its own
> feature, missing-position indicators, entity-versus-neighbour contrasts,
> aggregates over the visible groups, the withholding pattern itself, and
> correlations among the 16 targets.
> All training begins from random or default initialisation using only the
> provided data.
> Compute
> CPU tier: 10 cores, 62.5 GiB RAM. The prepared files are compact tabular data
> and do not require GPU acceleration.
> Determinism and integrity
> Preparation is fully deterministic: a fixed seed, deterministic relation
> selection resolved as a fixed point against eligibility, deterministic entity
> ordering, split construction and withholding, stable output sorting, canonical
> CSV and JSON formatting, and SHA-256 output hashes. Two independent full runs
> over the 21.3 million triple source produce byte-identical output.
> Each private answer row is hash-bound to its targets, the test-manifest total,
> the manifest digest and the metric version. A malformed submission receives 0.0.
> A damaged private answer key raises an internal grading error rather than
> silently assigning a participant a score of zero.
> Data leakage protection
> The prepared files contain no Wikidata entity identifiers, property
> identifiers, aliases, source edges or exact relation counts. Case identifiers
> are opaque and split-local. Participants must use only the supplied files.
> Source dataset
> RelMix is derived from Wikidata5M structured knowledge-graph triples. Wikidata
> structured data is distributed under Creative Commons CC0 1.0 Universal. The
> separately distributed Wikipedia article-text corpus is not used.
> Limitations
> The challenge covers 16 relations, selected for tier balance over the sampled
> population.
> Exact counts are collapsed into four activity tiers.
> The case population is drawn from entities with a substantive outgoing
> profile, which in this graph means they are rarely the target of these
> relations. inc_stream is therefore zero in almost all cases, and two of the
> four degree_stream tokens are near-constant. nbr_stream and the sampled
> neighbour count carry most of the usable signal. This is a property of the
> source graph under the eligibility rule, not an error in preparation.
> Some activity tiers occur far less often than others. Tiers with fewer than 10
> examples in the graded set do not contribute.
> The task evaluates local relation-profile reconstruction, not unrestricted
> knowledge-graph completion.
> Wikidata may contain incomplete, outdated or incorrect information.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Locating a Ship at Sea from Its Weather Log

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx712txfqz7xy6cehpqs8za4r18c11bh
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: small-data, feature-engineering, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.396

Full challenge description from page:

> Locating a Ship at Sea from Its Weather Log
> Overview
> A sailing ship of the eighteenth or early nineteenth century kept a daily log: which way the wind blew, how hard, whether it rained, how far the ship ran that day. Now imagine the navigator's position column torn off. Could you still say where on the world's oceans the ship was? That is this challenge — and it is a from-scratch modelling problem: you must design and train your own model, from random initialization, on the provided voyages alone. Each item is ten consecutive days of real observations from a real voyage — wind direction in degrees, a four-level wind force, rain and fog flags, the day's relative run, and the calendar month — with every identifying detail removed: no ship, no route, no nationality, no dates beyond the month, and no positions. Your model must read the meteorological signature alone and place the ship's final day into one of eleven ocean regions: the northeast trades, the equatorial calms, the southern westerlies, the monsoon seas, and their kin. The answer for each segment is the position the ship's own navigator recorded that day — historical measurement, not annotation.
> Real-World Motivation
> The great climate reconstruction projects that digitized centuries of ship logbooks face a persistent problem: many logbook pages carry weather observations but damaged, missing, or unreadable positions. A model that can infer where observations were taken from the observations themselves is a direct tool for georeferencing orphaned historical weather data — and a clean scientific test of a deeper question: how much positional information does surface weather alone carry? The age of sail is the ideal laboratory: ships moved slowly, sampled the wind field densely, and sailed through the most structured wind climate on Earth — trade belts, doldrums, monsoons, and westerlies that a skilled sailor could read like a map.
> What Makes This Different
> No existing benchmark poses this formulation: recovering where on Earth an instrumental record was taken, from the record alone — inverse georeferencing of orphaned observations. The neighbouring task families all differ at the root. Trajectory and destination prediction benchmarks take position tracks as input and ask where a vehicle goes next; here positions are exactly what is withheld, and no coordinates ever appear in the input. Geolocation benchmarks infer place from photographs or text, modalities saturated with visual and linguistic cues; none use a multi-day numeric weather sequence. Weather forecasting benchmarks predict future weather from located observations; this task inverts that arrow entirely. And the historical-climatology literature built on digitized logbooks treats every observation's position as given, using located weather to reconstruct past climate; using the weather to recover the position reverses the field's own direction of inference. The data is engineered against shortcuts, as measured during design: observations were normalized into language-free numeric form so neither vocabulary nor units can betray a ship's nationality and habitual routes; a model reading only the calendar month scores 0.00 (sailing schedules do not give the answer away); a model reading only the final day's wind scores 0.05. The signal genuinely lives in the multi-day sequence — steadiness, direction, force, and their changes — and it is genuinely bounded: the southeast trades of the Atlantic and Indian Oceans blow alike, hemispheres mirror each other, and ten days of wind cannot always break the tie. Real weather, honestly ambiguous.
> Data
> train.csv — 16,971 rows, columns: id (string, format SV followed by six digits, e.g. SV004217), month (integer 1–12), days (string, described below), region (string, the target).
> test.csv — 3,076 rows, columns: id, month, days (no region column).
> sample_submission.csv — the required format, filled with random regions. The days string holds ten day-records joined by "|", oldest first; each day-record is five comma-separated fields: wind direction in degrees (16-point compass, 0 = north, empty if unrecorded), wind force (0 calm/light, 1 moderate, 2 strong, 3 storm, empty if the historical term could not be mapped), rain flag (0/1), fog flag (0/1), relative day's run (distance rescaled within the voyage, empty if unrecorded). Splits are disjoint by voyage — no test segment comes from any voyage seen in training — and the test split is approximately balanced across regions.
> Target and Submission
> Submit a CSV with exactly two columns: id, region.
> Exactly one row per test id; no missing or duplicate ids.
> region must be exactly one of: Asian-seas, Caribbean-Gulf, Equatorial-Atlantic, Indian-trades, N-Atlantic-trades, NE-Atlantic-Biscay, NW-Atlantic, NW-Europe, S-Atlantic-trades, S-Atlantic-westerlies, Southern-Ocean-East.
> Example of a correctly formatted submission.csv:
> id,region
> SV000007,N-Atlantic-trades
> SV000012,Southern-Ocean-East
> Evaluation
> Chance-Normalized Macro-F1 across the eleven regions, range 0–1, higher is better: score = clip((macroF1 − 1/11) / (1 − 1/11), 0, 1). Macro averaging over an approximately balanced test split means constant and prior-copying submissions score 0.00. Anchors, all measured during design: random and most-frequent-region submissions score 0.00; a model reading only the calendar month scores 0.00; a model reading only the final day's wind scores 0.05; a hand-engineered sequence-feature model with a small trained network scores about 0.20. Stronger sequence models have real headroom above that — and a real ceiling well below 1.0, because mirrored wind belts make some segments honestly undecidable. The score measures how much of the ocean's wind geography a model actually learns.
> Compute
> This is a from-scratch modelling challenge designed for CPU solving within the platform time limit: you design and train your own model, with every learned parameter initialized randomly and estimated only from the provided train.csv. The sequences are short and numeric; feature engineering plus compact trained models — or small sequence networks trained from scratch — fit comfortably in the CPU budget. The score range separates models by how well they turn ten days of wind into a place on the globe.
> Restrictions / Prohibited Methods
> No source retrieval: do not attempt to identify the underlying logbook collections, and do not query, download, or match segments against any historical logbook database, climate archive, or other external source to recover positions. Predictions must come from a model trained on the provided training data. Violations are grounds for rejection regardless of score.
> No hard-coded per-id answers.
> No pretrained or foundation models of any kind, and no features, embeddings, weights, pseudo-labels, or initialisation learned from other data. Every learned parameter must start randomly and be trained only on the provided train.csv. No hosted or closed-source API models at any stage (training, distillation, pseudo-labelling, or inference).
> No probing for private answers, no training or calibrating on the test segments' hidden regions, no grader or platform side channels.

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## The River's Handwriting

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70s8pn700dqtks6jk5zrnpb58drd43
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: feature-engineering, small-data, Dataset source is visible after the challenge closes.
- Best/top context found: Top score: 0.610

Full challenge description from page:

> Overview
>
> Every stream has habits. A mountain creek fed by snowmelt breathes in a daily rhythm, rising each afternoon and falling overnight. A river below a hydropower dam moves in blunt steps when the turbines start. An urban stream spikes within minutes of rain and empties almost as fast, while a broad lowland river barely changes across a week. None of this is about how much water flows: it is about how the water moves. That is the river's handwriting.
>
> Each row of this dataset shows you seven stream gauges, labeled a through g. Each gauge is introduced by three labeled days of its 15-minute flow record. Then come six query days, each recorded by one of those seven gauges on a day you have not been shown. Your job is to say, for each query day, which gauge recorded it.
>
> Two or more query days may come from the same gauge, and some gauges may have no query day at all: there is no one-of-each guarantee. The answer for a row is a string of six letters from abcdefg, one per query day, repeats allowed.
>
> What Makes This Hard
>
> The size of the river is not the answer. Every published day is the shape of its log-flow, standardized within the day, plus a single number giving that day's log-space variability. The absolute flow level — the obvious giveaway that separates a great river from a creek — never appears.
>
> Different days are genuinely different. The reference days and the query days never overlap, so pointwise similarity is the wrong tool: the same gauge under different weather produces visibly different days. What persists is the dynamics — how fast rises climb and recessions drain, whether the day carries a clean diurnal cycle, how spiky or smooth the record is at 15-minute resolution.
>
> The test gauges are new. No gauge in the test rows ever appears in a training row. A model that memorizes the training gauges learns the wrong thing; what must transfer is a learned notion of "these two days move like the same river", applicable to rivers it has never seen.
>
> Where The Answers Come From
>
> Every answer is a recorded fact. Each published day is a real day of 15-minute discharge measured by a real stream gauge, and the target simply names which of the row's gauges recorded it. Nothing is simulated and no curve is edited; the only transformations are quality screening, resampling to a fixed 96-point grid, and the within-day standardization described above.
>
> From-Scratch Requirement
>
> Every submitted solution must train a genuine predictive component using the released training rows, and that component must materially determine the submitted assignments. The training must happen inside solution.py during the graded run: loading weights fitted beforehand, or shipping a model with the submission, does not satisfy this. Network access is disabled during evaluation.
>
> Allowed approaches include:
>
> a learned pairwise verifier: features of a query day and a reference day in, probability they share a gauge out, trained on the training rows where the links are given;
> learned day embeddings trained from scratch on the released rows, with queries assigned by distance to the row's references;
> engineered dynamical features feeding any standard model, with the row resolved by aggregating scores over each gauge's three reference days;
> small sequence models over the 96-point shapes, initialised with random weights and trained only on the released rows; and
> standard numerical and machine-learning libraries already present in the evaluation environment.
> What Not To Use
> No external datasets, and in particular no external hydrological archive. Do not attempt to identify the underlying gauges, sites or dates, or to retrieve any flow record, by matching the published shapes against any public archive. This is grounds for automatic disqualification.
> No pretrained weights of any kind, including time-series foundation models, and no weights reached indirectly through a library or a cached model package.
> No features, embeddings or labels produced by a pretrained model.
> No external APIs, no network calls at grading time, and no remote inference.
> No use of the test set beyond ordinary per-row inference: no training on test rows, no pseudo-labelling, and no fitting, calibrating, thresholding or normalising with statistics pooled across the test set.
> No linking across test rows. The same underlying gauge may appear in more than one test row; matching days between different test rows, or carrying any information from one test row into another, is test-set use and is prohibited. Each row must be answered from that row's own references and queries plus what was learned from the training rows.
> No fixed hand-written pipeline that has no component fitted from the released labels.
> No hardcoded lookup tables, no fingerprinting of row identifiers or row order, and no manually supplied answers. Row identifiers are opaque and row order is randomised; both carry nothing.
> Evidence
>
> Every row is one JSON file holding two keys.
>
> references — type: object; keys a through g, one per reference gauge. Each value is an array of exactly 3 days. Each day is an object with shape — type: array, 96 numbers rounded to 4 decimals, the day's log-flow resampled to a 15-minute grid and standardized to mean zero and unit variance within the day — and log_sigma — type: number, the natural log of that day's log-space standard deviation before standardization.
> queries — type: array; exactly 6 day objects of the same form, in answer order.
>
> All 27 days of a row come from the same seasonal window of the same year, so seasonal contrast is never the shortcut. Reference days and query days are disjoint, and no day is reused anywhere in the dataset.
>
> One further public column matters for scoring: spread_band, a letter from a to d. It bands each row by how far apart the row's seven reference gauges sit in a small fixed feature distance computed from the published days themselves (mean absolute step, diurnal amplitude, lag-one autocorrelation, and log_sigma, averaged per gauge and compared pairwise). Rows whose gauges are alike are genuinely harder; the metric uses the bands so that easy spread-out rows cannot carry the score alone. It carries nothing beyond what the published days already show.
>
> Validating Your Model
>
> The leakage unit is the gauge. Every site was hashed to one side of the split, so the training and test rows draw from disjoint sets of gauges.
>
> Validate the same way: hold out entire rows, and if you build your own gauge-labeled pool from the training rows, hold out whole reference groups rather than individual days. A verifier that has seen a gauge's other days during training will look better on that gauge than it will on the truly unseen gauges of the test split.
>
> Evaluation
>
> The row score is the fraction of the six query days assigned to their recording gauge, in 
> [
> 0
> ,
> 1
> ]
> [0,1].
>
> Let 
> 𝑀
> all
> M
> all
> 	​
>
>  be the mean row score over all test rows and 
> 𝑀
> tight
> M
> tight
> 	​
>
>  the unweighted mean of the per-band means, where rows are grouped by spread_band. The final score is
>
> Score
> ⁡
> =
> 0.80
>  
> 𝑀
> all
> +
> 0.20
>  
> 𝑀
> tight
> ,
> Score=0.80M
> all
> 	​
>
> +0.20M
> tight
> 	​
>
> ,
>
> bounded to 
> [
> 0
> ,
> 1
> ]
> [0,1]. There are no hidden buckets. Guessing one letter everywhere scores about one seventh.
>
> Dataset
>
> The prepared public data contains:
>
> train.csv — labeled training rows;
> test.csv — unlabeled test rows;
> sample_submission.csv — submission template;
> task_manifest.json — public dimensions and scoring constants; and
> payload/ — one JSON file per row holding that row's reference and query days.
> train.csv
> id — type: string; opaque unique row identifier: the letter g followed by 16 hexadecimal characters.
> evidence_file — type: string; relative path to this row's JSON file.
> spread_band — type: string; a letter from a to d, the row's reference-spread band.
> gauges — type: string; the gold assignment, one letter per query day.
> test.csv
>
> test.csv contains the same columns except gauges.
>
> sample_submission.csv
> id — type: string; one required test identifier per row.
> gauges — type: string; the constant string aaaaaa. It uses no evidence and scores about one seventh.
> task_manifest.json
> task — type: string; stable task identifier.
> primary_modality — type: string; the kind of evidence a row carries.
> split — type: object; row counts, the leakage unit and the disjointness guarantee.
> signals — type: object; reference and query geometry, points per day and the day form. Every row has the same geometry — 7 reference gauges, 3 labeled days each and 6 query days — so it is published here once rather than repeated as a column in every row.
> target — type: object; grammar and the absence of a one-of-each guarantee.
> metric — type: object; the two aggregation weights and the bucket column.
> submission — type: object; required columns and the string length.
> evaluation_environment — type: object; CPU, memory, GPU and network configuration.
> from_scratch — type: object; training requirement and pretrained-weight policy.
> Submission Format
>
> Submit one CSV with exactly these columns in this order:
>
> id — type: string; must match the test identifiers exactly, with no missing, extra or duplicate values.
> gauges — type: string; exactly 6 characters from abcdefg, repeats allowed. Position i names the gauge of query day i in the row's published order.
>
> A prediction that is not six letters from abcdefg scores zero for that row and leaves other rows unaffected.
>
> A concrete two-row CSV example is shown below without a fenced code block:
>
> Header: id,gauges
> First row: g0a1b2c3d4e5f6071,gabdea
> Second row: g9f8e7d6c5b4a3021,aaffgc
>
> The example identifiers are illustrative and are not release rows.
>
> A Practical Starting Point
>
> A reasonable first system can be built in four stages:
>
> Describe each day with dynamical features: mean absolute 15-minute step, autocorrelations at several lags, rise fraction, recession and rise slopes, diurnal and semi-diurnal harmonic amplitudes and phase, spike rate, peak count, and the published log_sigma.
> Build a pair dataset from the training rows: every (query day, reference day) pair inside a row, labeled by whether they share a gauge. Train a verifier on pair features — absolute feature differences plus a few direct shape comparisons.
> Assign each query to the reference gauge whose three days give the highest aggregated verification score.
> Keep the split honest: validate on held-out rows, and remember the test gauges are new — a verifier that keys on individual training gauges will not transfer.
>
> Two findings from building the reference solution are worth passing on.
>
> Plain correlation between days is the weakest serious route. Two days of the same river under different weather do not line up pointwise; nearest-reference matching on raw day shapes clears random comfortably and then stalls. The signal that transfers lives in dynamical invariants, not in the curves themselves.
>
> Aggregate over the three reference days. Any single reference day can be an odd one — a storm, a maintenance dip. Scoring a query against a gauge's best two of three days is markedly steadier than trusting any single comparison.
>
> Compute Environment
>
> Submitted solutions run in a CPU-only environment with 10 CPU cores and 62 GB of RAM. No GPU or network access is available. Training, inference and decoding must all fit within those limits.
>
> Expected Output
>
> Your script receives the public dataset directory and exact submission CSV path as two positional arguments.
>
> It may read only the files listed under Dataset above, all of which live inside that directory. No answer or label file for the test rows exists anywhere the script can reach. It must write only the submission CSV at the given path, and must not depend on any file left behind by an earlier run.
>
>  
>
> Submissions
> 5
> Top Score
> 0.610
> Created
> Sep 4, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> 0/12
> solvers beat AI
> How closing works
>
> Be the first to solve this challenge! 5 distinct solvers with graded solutions are needed to activate the $650 prize pool and start a closing countdown. At 12, up to 12 solvers will be selected to continue.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Wireless CSI Phase Topology Inference

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7em6mptf9fc029wkfwaazrs98c9v18
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Accepted
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: ↑ Higher is better
- Tags: Not shown/captured
- Best/top context found: Top score: —

Full challenge description from page:

> Domain: 4D wireless sensing and scientific deep learning.
>
> Overview
>
> Modern WiFi hardware measures a complex channel response across time, antenna elements, and
> frequency. These measurements are not just signal-strength readings. Their real and imaginary
> components form a changing wave field in which signal nulls can appear, exchange order, and
> reconnect as multipath paths interfere.
>
> Your task is to recover a compact global certificate of that hidden evolution from partially observed
> complex CSI packets. Each packet is an 8-step field over a 4 by 4 antenna plane and 32 frequency
> bins. Missing entries, phase drift, multipath clutter, and held-out propagation regimes make it
> unsafe to treat a null as a stable local blob.
>
> For every packet, predict a six-token signed braid code and the probability of an odd reconnection
> parity. The braid code is a canonical summary of global crossing events. A positive or negative token
> states the orientation of a crossing; zero means that the remaining code position is unused. This is
> not indoor localization, human activity recognition, or scene reconstruction. It is a structured
> scientific inference task over the topology of a complex wave field.
>
> Dataset
> File	Rows	Description
> train.csv	3,000	Packet paths and both training targets.
> test.csv	600	Packet paths with targets withheld.
> sample_submission.csv	600	A valid weak submission in the required schema.
> packets/	3,600 .npz files	Native complex CSI field packets.
> starter.py	1	Compact CPU-only learned baseline.
> Input columns
> Column	Type	Description
> id	string	Opaque submission identifier.
> packet_path	string	Relative path to the matching NumPy packet.
> Training target columns
> Column	Type	Description
> braid_code	six space-separated integers	Six canonical signed crossing tokens, each in -3 through 3.
> reconnection_parity	integer	0 for even and 1 for odd parity of the hidden reconnection certificate.
> Native packet arrays
>
> Each packet is loaded with numpy.load(path, allow_pickle=False).
>
> Array	Type	Shape	Description
> field	float16	(8, 2, 4, 4, 32)	Time, real/imaginary component, antenna row, antenna column, frequency-bin complex field. Missing values are stored as zero.
> mask	uint8	(8, 4, 4, 32)	One for an observed complex field entry and zero for a missing entry. The same mask applies to both real and imaginary components.
>
> Every packet is an independent field episode. Evaluation episodes use fresh null paths, multipath
> draws, phase offsets, and masks while sharing broad radio-response families with training.
>
> Evaluation
>
> Let T be the six true braid tokens and P the six submitted tokens. Let q be the submitted
> probability of odd reconnection and y the binary parity target.
>
> token_accuracy is the mean exact agreement over all six token positions. exact_accuracy is the
> fraction of packets with all six tokens correct. The parity component uses Brier loss.
>
> [
> \text{ParityQuality} = \exp\left(-4 \cdot \frac{1}{n}\sum_i(q_i-y_i)^2\right)
> ]
>
> [
> \text{RawScore} = 0.55,\text{TokenAccuracy} + 0.25,\text{ExactAccuracy} + 0.20,\text{ParityQuality}
> ]
>
> [
> \text{Score} = 0.0001 + 0.9999,\text{RawScore}
> ]
>
> Higher is better. The score is bounded in [0.0001, 1.0]; a perfect submission scores 1.0.
>
> import numpy as np  
>   
> token_accuracy = np.mean(predicted_tokens == true_tokens)  
> exact_accuracy = np.mean(np.all(predicted_tokens == true_tokens, axis=1))  
> parity_quality = np.exp(-4 * np.mean((parity_probability - true_parity) ** 2))  
> score = 0.0001 + 0.9999 * (0.55 * token_accuracy + 0.25 * exact_accuracy + 0.20 * parity_quality)  
> Submission
>
> Submit a CSV with exactly 600 rows and exactly these columns in this order:
>
> id,braid_code,reconnection_parity
>
> braid_code must contain exactly six space-separated integer tokens in [-3, 3].
> reconnection_parity must be a finite probability in [0, 1].
>
> id,braid_code,reconnection_parity  
> 0,"-1 2 0 0 0 0",0.347000  
>
> Identifiers must match test.csv exactly once. Extra or missing rows, duplicate identifiers,
> incorrect columns, non-finite values, and malformed braid codes are rejected.
>
> Expected approach
>
> This challenge is intended for a genuinely trained model. A practical CPU-only solution can use
> phase-aware normalization, mask-aware 3D convolutions over time, frequency, and the antenna plane,
> then a shared structured decoder for the six code positions and parity. The supplied starter is a
> small learned baseline, not a competitive ceiling. Training compact models from scratch on the
> released data is expected to fit within the 10-core, 1.5-hour runtime.
>
> Allowed and Prohibited Approaches
>
> Allowed approaches include training from scratch on the released packets, CPU-friendly convolutional
> or transformer-style models, self-supervised pretraining on the released packet fields, phase-aware
> augmentation, and deterministic topology-consistency decoding applied to learned scores.
>
> Prohibited approaches include external datasets or pretrained checkpoints, internet access during a
> run, hardcoded test predictions, deriving predictions from ids, filenames, row order, or packet order,
> reconstructing labels from private files, test-label calibration, and exploiting submission parsing or
> grader behavior. A valid solution must include a model genuinely trained on the released challenge
> data; an inference-only analytic detector is not an accepted final approach.
>
>  
>
> Submissions
> 0
> Top Score
> —
> Created
> Aug 11, 2026
> Start New Solution
> Ready to Solve
>
> This challenge has been reviewed and approved. Start solving to submit your solution!
>
> Submission Credits
> 6/6
> Learn more about submission credits
> 0/12
> solvers beat AI
> How closing works
>
> Be the first to solve this challenge! 5 distinct solvers with graded solutions are needed to activate the $650 prize pool and start a closing countdown. At 12, up to 12 solvers will be selected to continue.
>
> CREATOR REWARD FOR THIS PROBLEM
> $400–500
> Help

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## The Eight Tongues

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx73d826zvmzsejn84kqwpqnp18dt1bq
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat adrian's score of 0.486!

Full challenge description from page:

> The Eight Tongues Overview Translation is supposed to disappear. A good English rendering of Balzac reads as English, and so does a good rendering of Tolstoy — and yet the two Englishes are not the same English. The source language leans on its translator: French arrives with long qualifying clauses and abstract nouns, Russian with patronymic rhythm and bare directness, Latin with periodic architecture, Norwegian with short declaratives. Linguists call the residue translationese, and it survives astonishing abuse. Here it must survive the worst abuse of all: the sentences are destroyed, every name and rare word is deleted, and only the counts of common English words remain. Each row of this dataset shows you eight anonymous word-bags — the common-word vocabularies of eight passages of English literary translations, word order destroyed — one passage translated from each of eight source languages, in shuffled order. The languages carry fixed anonymous letters a through h that are consistent across the whole dataset: whatever language letter c is in one row, it is in every row. Your job is to name, for each published bag in order, the language letter it was translated from. The answer for a row is a string of eight letters, a permutation of abcdefgh, because each row holds exactly one passage per language. What Makes This Hard The sentences are gone. No word order, no syntax, no phrases — only tokens and counts. Whatever a parser would tell you is deleted; only distributional habits survive. The rare words are gone too. The vocabulary is restricted at the source to the corpus's most frequent English words, shipped in VOCABULARY.json. No character names, no place names, no topic words, no borrowed exotica — the crutch of spotting an obviously Russian name never appears. The signal is in how translations of each language bend ordinary English: which connectives, pronouns, auxiliaries and common nouns they reach for, and how often. The languages are anonymous and the letters must be learned. Nothing says which letter is which language. The mapping is fixed across the dataset, so it can be learned from the training rows — but only by finding eight stable distributional signatures. The authors are cold. The split is by original author: every test passage is translated from an author (and hence from works) the training rows never showed you. What transfers is the signature of a language's translations, not the vocabulary of particular books. Where The Answers Come From Every answer is a recorded fact of the public catalogue: each bag comes from a real passage of a real catalogued English translation, and the language label is the source language of the original author, taken from a curated list of canonical authors — no author on the list wrote in more than one of the eight languages. Passages come from the trimmed body of each book, so translator prefaces and licence boilerplate are excluded. From-Scratch Requirement Every submitted solution must train a genuine predictive component using the released training rows, and that component must materially determine the submitted assignments. The training must happen inside solution.py during the graded run: loading weights fitted beforehand, or shipping a model with the submission, does not satisfy this. Network access is disabled during evaluation. Allowed approaches include: a per-bag language classifier — multinomial models, logistic regression, gradient boosting, small neural networks — over the published vocabulary counts, decoded per row by the one-per-language structure (Hungarian assignment on the eight probability rows); bag statistics (function-word shares, type-token ratios, length-normalised count profiles) feeding any standard model; learned representations of the count vectors, initialised from random weights and trained only on the released rows; and standard numerical and machine-learning libraries already present in the evaluation environment. What Not To Use No external datasets, and in particular no text corpus, catalogue, search engine or language resource. Do not attempt to identify the underlying works, or to retrieve any text, by matching the published bags against any catalogue or search index. This is grounds for automatic disqualification. No pretrained weights of any kind — no language models, no word embeddings (word2vec, GloVe, fastText or newer), and no weights reached indirectly through a library or a cached model package. No features, embeddings or labels produced by a pretrained model. No external APIs, no network calls at grading time, and no remote inference. No use of the test set beyond ordinary per-row inference: no training on test rows, no pseudo-labelling, and no fitting, calibrating, thresholding or normalising with statistics pooled across the test set. No linking across test rows: matching bags between different test rows, or carrying any information from one test row into another, is test-set use and is prohibited. Each row must be resolved from that row's own eight bags plus what was learned from the training rows. No fixed hand-written pipeline that has no component fitted from the released labels. No hardcoded lookup tables, no fingerprinting of row identifiers or row order, and no manually supplied answers. Row identifiers are opaque and row order is randomised; both carry nothing. Evidence Every row is one JSON file holding a single key. bags — type: array; eight objects in answer order, each mapping frequent-English tokens to positive integer counts. Every token appears in VOCABULARY.json; each bag keeps 180 to 350 total tokens. Twin-content bags were never used, and passages never overlap on the page. One further public column matters for scoring: blend_band, a letter from a to d banding each row by the mean pairwise distance between its eight normalised count vectors. It groups rows by how alike the row's bags look, and the metric uses the bands so that easy varied rows cannot carry the score alone. It carries nothing beyond what the published bags already show. Evaluation The row score is the fraction of the eight bags assigned to their true language letter, in $[0, 1]$; a perfect assignment scores one. A random permutation averages one correct of eight, about 0.13 — stated here so nobody mistakes the floor for skill. Let $M_{\text{all}}$ be the mean row score over all test rows and $M_{\text{alike}}$ the unweighted mean of the per-band means, where rows are grouped by blend_band. The final score is $$ \operatorname{Score} = 0.80M_{\text{all}} + 0.20M_{\text{alike}}, $$ bounded to $[0,1]$. There are no hidden buckets. Dataset The prepared public data contains: train.csv — labeled training rows; test.csv — unlabeled test rows; sample_submission.csv — submission template; VOCABULARY.json — the fixed published vocabulary; task_manifest.json — public dimensions and scoring constants; and payload/ — one JSON file per row holding that row's eight bags. train.csv id — type: string; opaque unique row identifier, the letter t followed by sixteen hex characters. evidence_file — type: string; relative path to this row's JSON file. Release filenames use a second opaque namespace: a file name is not the row id. blend_band — type: string; a letter from a to d, the row's look-alike band. tongue — type: string; the gold assignment, a permutation of abcdefgh naming each bag's language letter in order. test.csv test.csv contains the same columns except tongue. sample_submission.csv id — type: string; one required test identifier per row. tongue — type: string; the identity permutation abcdefgh. It uses no evidence and scores about 0.13, the random floor. VOCABULARY.json vocabulary — type: array of strings; the fixed frequent-English token list, sorted; every published bag token appears here. size — type: integer; the vocabulary length. task_manifest.json task — type: string; stable task identifier. primary_modality — type: string; the form of the published evidence. split — type: object; row counts, the leakage unit and the author-disjoint guarantee. signals — type: object; bags per row, the vocabulary size, the kept-token bounds, the bag form and the composition rule. target — type: object; the assignment grammar. metric — type: object; the row formula, the two aggregation weights and the bucket column. submission — type: object; required columns and the string length. evaluation_environment — type: object; CPU, memory, GPU and network configuration. from_scratch — type: object; training requirement and pretrained-weight policy. Submission Format Submit one CSV with exactly these columns in this order: id — type: string; must match the test identifiers exactly, with no missing, extra or duplicate values. tongue — type: string; exactly 8 characters, a permutation of abcdefgh, naming each published bag's language letter in order. A prediction that is not a permutation of abcdefgh scores zero for that row and leaves other rows unaffected. A concrete two-row CSV example is shown below without a fenced code block: Header: id,tongue First row: 0a1b2c3d4e5f6071,gcabdefh Second row: 9f8e7d6c5b4a3021,abcdefgh The example identifiers are illustrative and are not release rows. A Practical Starting Point A reasonable first system can be built in four stages: Load VOCABULARY.json and turn every bag into a normalised count vector. Train a multinomial classifier — logistic regression is a strong start — on the training bags, labelled by the letters their rows assign them. Decode each test row by Hungarian assignment on the eight bags' class log-probabilities, using the one-per-language row structure. Respect the split: validate on held-out original authors, because the test authors are ones the model never saw. Compute Environment Submitted solutions run in a CPU-only environment with 10 CPU cores and 62 GB of RAM. No GPU or network access is available. Training, inference and decoding must all fit within those limits. Expected Output Your script receives the public dataset directory and exact submission CSV path as two positional arguments. It may read only the files listed under Dataset above, all of which live inside that directory. No answer or label file for the test rows exists anywhere the script can reach. It must write only the submission CSV at the given path, and must not depend on any file left behind by an earlier run. &nbsp;
> $700 Pool
> 4 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## The Lost Anchor

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7f39rn34hbq06fej3hwgb1vn8ds6ys
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat masry1's score of 0.618!

Full challenge description from page:

> The Lost Anchor Overview An ocean drifter is a small ball of electronics with a long tail: fifteen metres below the surface float hangs a holey-sock drogue, a fabric cylinder that anchors the buoy to the water around it. With the drogue attached, the drifter goes where the ocean goes. And then, one day — a shark bite, a chafed tether, a storm — the tail is gone. The buoy still floats, still transmits, still traces a path across the sea; but now the wind pushes it along and the waves pump it forward, and the path it draws is subtly no longer the ocean's own. The drifter program tracks this failure with a submergence sensor and records, for every buoy, the date its anchor was lost. Strip away that sensor and the calendar, and only the kinematics remain. Each row of this dataset shows you twelve 20-day velocity records from twelve different drifting buoys, all drawn from one ocean neighbourhood and one season, in shuffled order. Exactly five of the records were measured after the drifter lost its drogue; the other seven with the drogue still attached. Your job is to mark the five. The answer for a row is a string of twelve letters, y (drogue lost) or n (drogue attached), containing exactly five y — the number of undrogued records is always five and is public. What Makes This Hard The detector is withheld. The program's operational discriminant — the submergence/tether sensor stream that the quality-control analysts actually use — is not published, and neither are dates, positions or identifiers. Only the six-hourly east and north velocity components remain. Region and season are held fixed. All twelve records in a row lie within 20 degrees of latitude and 40 degrees of longitude of one another and within one quarter of the year, chosen by the same nearest-to-anchor rule for both classes. The background circulation — trades, gyres, storms — is shared; what differs is how each buoy rides it. Faster is a hint, not an answer. An undrogued buoy slips downwind, so raw speed carries real signal — and stalls quickly: a drogued drifter in a jet outruns an undrogued one in the doldrums, and within a matched neighbourhood the speed distributions overlap heavily. The rest of the signal lives in finer structure: how the velocity spins, how energy sits at the inertial band versus the slow eddies, how the wind's gusts print through. The test drifters are ones you never saw. The split is by drifter, and both classes come from the same instruments: every drifter in the release lived through both phases of its life. What must transfer is how a lost anchor changes the motion — not which buoy is which. Where The Answers Come From Every answer is a recorded fact. Each record is a real 20-day slice of a real drifter's quality-controlled six-hourly velocity series, and the label comes from the drogue-loss date recorded in the program's own metadata after analyst review. A five-day guard zone around the loss date is excluded, so no record straddles the event. Nothing is simulated and no series is edited; the only transformations are segmenting, screening and rounding. From-Scratch Requirement Every submitted solution must train a genuine predictive component using the released training rows, and that component must materially determine the submitted masks. The training must happen inside solution.py during the graded run: loading weights fitted beforehand, or shipping a model with the submission, does not satisfy this. Network access is disabled during evaluation. Allowed approaches include: a learned per-record classifier — features of one velocity record in, probability the drogue was lost out — trained on the labeled records the training rows provide; engineered kinematic and spectral features (speed statistics, acceleration, spin and looping measures, rotary spectra, the asymmetry between clockwise and counter-clockwise energy, autocorrelation) feeding any standard model; small convolutional or recurrent networks over the raw 80-sample velocity series, initialised with random weights and trained only on the released rows; decoding with the known count: scoring the twelve records and marking the top five, rather than thresholding records independently; and standard numerical, signal-processing and machine-learning libraries already present in the evaluation environment. What Not To Use No external datasets, and in particular no external drifter, wind or current archive. Do not attempt to identify the underlying drifters, dates or places, or to retrieve any track or metadata record, by matching the published series against any public archive. This is grounds for automatic disqualification. No pretrained weights of any kind, including time-series foundation models, and no weights reached indirectly through a library or a cached model package. No features, embeddings or labels produced by a pretrained model. No external APIs, no network calls at grading time, and no remote inference. No use of the test set beyond ordinary per-row inference: no training on test rows, no pseudo-labelling, and no fitting, calibrating, thresholding or normalising with statistics pooled across the test set. No linking across test rows: matching records between different test rows, or carrying any information from one test row into another, is test-set use and is prohibited. Each row must be resolved from that row's own twelve records plus what was learned from the training rows. No fixed hand-written pipeline that has no component fitted from the released labels. No hardcoded lookup tables, no fingerprinting of row identifiers or row order, and no manually supplied answers. Row identifiers are opaque and row order is randomised; both carry nothing. Evidence Every row is one JSON file holding a single key. records — type: array; twelve record objects in answer order. Each has ve — type: array, 80 numbers, the eastward velocity in metres per second at six-hour steps — and vn — type: array, 80 numbers, the northward velocity. All values are rounded to 4 decimals. Records with gaps beyond 21 days of span, speeds above 3.5 m/s, degenerate channels, or a twin-duplicate of another record were never used. One further public column matters for scoring: blend_band, a letter from a to d banding each row by the mean pairwise distance between its twelve speed profiles. Rows whose records all look alike (a) are genuinely harder than varied rows (d); the metric uses the bands so that easy varied rows cannot carry the score alone. It carries nothing beyond what the published series already show. Validating Your Model The leakage unit is the drifter. Every drifter in the release lived through both phases, and drifters are split-disjoint: every training drifter stays in training, every test drifter stays in test. Validate the same way: hold out entire drifters, not just rows. The same drifter contributes many records, so a random row-level split leaks — your validation records would come from buoys whose personal noise and home currents your model already memorised, and the score would flatter drifter fingerprinting that transfers nothing. Evaluation For a row, let $v$ be the fraction of the five true undrogued positions your mask marks y. A random legal mask already gets $v = 5/12$ on average, so the row score is a skill score over that floor: $$ R = \frac{v - 5/12}{1 - 5/12}, $$ so a perfect mask scores one and a chance mask scores zero. Nothing is rectified row by row: a row that lands under the floor scores negative, which is exactly what makes a uniformly random submission average zero rather than some positive residue of luck. Read a leaderboard number as skill over chance, not as a fraction found. A mask that is not twelve y/n letters containing exactly five y is scored as zero overlap for that row - the worst any legal mask could do - so a malformed entry can never beat a guess. Let $M_{\text{all}}$ be the mean row score over all test rows and $M_{\text{alike}}$ the unweighted mean of the per-band means, where rows are grouped by blend_band. The final score is $$ \operatorname{Score} = 0.80\,M_{\text{all}} + 0.20\,M_{\text{alike}}, $$ bounded to $[0,1]$ once, at the end, after the two terms are combined. There are no hidden buckets. Dataset The prepared public data contains: train.csv — labeled training rows; test.csv — unlabeled test rows; sample_submission.csv — submission template; task_manifest.json — public dimensions and scoring constants; and payload/ — one JSON file per row holding that row's twelve records. train.csv id — type: string; opaque unique row identifier. evidence_file — type: string; relative path to this row's JSON file. blend_band — type: string; a letter from a to d, the row's look-alike band. undrogued — type: string; the gold mask, twelve letters y or n with exactly five y. test.csv test.csv contains the same columns except undrogued. sample_submission.csv id — type: string; one required test identifier per row. undrogued — type: string; a weak but real baseline mask: the five records with the highest minimum speed. It scores 0.1102 - above chance, because an undrogued buoy is pushed by the wind even when the water around it is slack, so its quietest hours are still not very quiet. It is a floor to beat, not a starting model; the trained reference sits four times higher. task_manifest.json task — type: string; stable task identifier. split — type: object; row counts, the leakage unit and the drifter-disjoint guarantee. signals — type: object; records per row, the undrogued count, the channels, points per record, the record form and the composition rule. target — type: object; the mask grammar and the known count. metric — type: object; the row formula, the two aggregation weights, the bucket column and the chance-level note. submission — type: object; required columns and the string length. evaluation_environment — type: object; CPU, memory, GPU and network configuration. from_scratch — type: object; training requirement and pretrained-weight policy. Submission Format Submit one CSV with exactly these columns in this order: id — type: string; must match the test identifiers exactly, with no missing, extra or duplicate values. undrogued — type: string; exactly 12 characters, each y or n, containing exactly five y. Position i refers to the i-th record in the row's published order. A prediction that is not twelve letters y/n with exactly five y is scored as zero overlap for that row - $R = -5/7$, the worst any legal mask could do - and leaves other rows unaffected. A malformed row is not a free skip: it costs you more than a guess would. A concrete two-row CSV example is shown below without a fenced code block: Header: id,undrogued First row: 0a1b2c3d4e5f6071,ynyynnnnyynn Second row: 9f8e7d6c5b4a3021,yyyyynnnnnnn The example identifiers are illustrative and are not release rows. A Practical Starting Point A reasonable first system can be built in four stages: For every record, compute kinematic and spectral features: mean, spread and upper-quantile speed, acceleration magnitude, the spin and meandering of the velocity vector, the rotary spectrum of the complex velocity and the asymmetry between its clockwise and counter-clockwise halves, the spectral slope, and the high-frequency energy fraction; add a speed histogram and a pooled log-spectrum. Build a record dataset from the training rows — every record, labeled by its row's mask — and train a per-record classifier. Decode with the known count: score the twelve records and mark the five most anchor-less, rather than thresholding records independently. Respect the split: validate on held-out drifters, because the test drifters are ones the model never saw. Two findings from building the reference solution are worth passing on. Speed is real but capped. Ranking records by mean speed — the wind-slip intuition — clears random by a clear margin and then stalls: within a region- and season-matched row, currents move drogued buoys as fast as wind moves undrogued ones, and no other single number does better. The signature is in the joint motion. What separates a lost anchor is the combination — how much energy rides the near-inertial band, how the velocity vector spins and loops, how gusty the acceleration is, how the speed distribution leans. A classifier that reads these together roughly half-again outperforms the best single rule; the headroom above it belongs to models that read the raw complex velocity series. Compute Environment Submitted solutions run in a CPU-only environment with 10 CPU cores and 62 GB of RAM. No GPU or network access is available. Training, inference and decoding must all fit within those limits. Expected Output Your script receives the public dataset directory and exact submission CSV path as two positional arguments. It may read only the files listed under Dataset above, all of which live inside that directory. No answer or label file for the test rows exists anywhere the script can reach. It must write only the submission CSV at the given path, and must not depend on any file left behind by an earlier run. &nbsp;
> $700 Pool
> Closes in 7h 35m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Anonymous Wearable Packet Binding and Clock Repair

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx75ya747kbygmsvde9w4hmsk58ap35p
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat dominico's score of 0.853!

Full challenge description from page:

> Anonymous Wearable Packet Binding and Clock Repair Overview A person is running while an optical motion-capture system and an instrumented treadmill record the movement, and several body-worn inertial sensors record it at the same time. The inertial streams arrive as an anonymous pool: their identities are stripped, their axes are rotated, and each one runs on its own drifting clock. Your job is to put the pool back together against the reference recording. For each row you receive one reference window, and a pool of seven anonymous packets. Some of those packets were measured on the person in this window; the rest are decoys taken from unrelated recordings. You must decide which packets belong here, say which body site each retained packet was worn on, and supply monotone clock anchors that align each retained packet to the reference timeline. This is not sensor-placement classification. A packet cannot be placed by looking at it alone, because a decoy from an unrelated recording looks like an ordinary packet; the decision requires comparing it against this row's reference evidence. Nor is it plain synchronisation, because you do not know which packet you are synchronising. The three parts are one answer: an alignment attached to the wrong body site earns nothing. Each site token is one of s0 through s5, each packet token is one of p0 through p6, and a binding is written p3>s1. Every retained packet also carries five clock anchors. A row's answer has three to six bindings; a body site and a packet may each be used at most once. From-Scratch Requirement Every submitted solution must train a genuine predictive component using the released training rows, and that component must materially determine the predictions. Network access is disabled during evaluation. Allowed approaches include: temporal convolutional, recurrent, attention, or graph models initialised with random weights and trained only on the released rows; learned similarity between a packet and the reference evidence, learned placement models, and learned rankers over candidate alignments; deterministic signal processing, correlation, dynamic programming and assignment algorithms used around a trained component; augmentation built only from the released public files; and standard numerical, signal-processing, optimisation and machine-learning libraries already present in the evaluation environment. What Not To Use No pretrained weights of any kind, and no weights reached indirectly through a library or a cached model package. No features, embeddings or labels produced by a pretrained model. No external datasets. In particular, do not attempt to identify, retrieve or align these recordings against any external corpus, and do not use any external source to recover their provenance, participant identity or ordering. No external APIs, no network calls at grading time, and no remote inference. No training on the test rows and no pseudo-labelling of them. No fixed hand-written signal-processing pipeline that has no component fitted from the released labels. No hardcoded lookup tables, no fingerprinting of row identifiers or row order, and no manually supplied answers. Evidence Every row is one compressed archive holding three arrays, all sampled at 100 Hz over an 800-frame window, which is 8.00 seconds. points — type: array; shape 19 by 3 by 800. Nineteen optical marker trajectories in millimetres, centred on the pelvis so that treadmill drift and absolute position carry no information. force — type: array; shape 2 by 800. Vertical ground reaction force in Newtons for each of the two platforms, converted from the raw transducer voltages with the calibration matrix supplied by the capture system. packets — type: array; shape 7 by 6 by 800. The anonymous pool. Channels 0 to 2 are acceleration and channels 3 to 5 are angular velocity. Each packet has been transformed independently. Its acceleration and angular-velocity triads share one random 3D rotation, so raw axis directions cannot be matched against the markers, and quantities that survive rotation, such as magnitude, are the natural place to start. Its amplitude is rescaled, noise is added, and it is quantised. Above all, each packet runs on its own clock. A packet frame does not correspond to the reference frame with the same index. The mapping from packet frame to reference frame is monotone increasing, starts at an unknown offset of up to 60 frames either side, and advances at an unknown mean rate between 0.90 and 1.10 reference frames per packet frame, with small local jitter on top. Clock Anchors For every packet you retain, report the reference frame that its packet frames 80, 240, 400, 560 and 720 correspond to. The five values must be non-decreasing whole numbers. Every packet you bind must appear in anchors with exactly five of them, and no packet you did not bind may appear there; a row that breaks either rule scores zero, however good its bindings are. An anchor that is $\Delta$ frames away from the truth is worth $$ q = \exp\left[-\frac{1}{2}\left(\frac{\Delta}{4}\right)^{2}\right], $$ and nothing at all beyond 15 frames. One frame is 10 milliseconds, so a perfect anchor is worth 1.00, four frames away is worth about 0.61, and anything past 150 milliseconds is worthless. Validating Your Model The test rows come from nine participants who appear in no training row. Decoy packets are always drawn from within the same split, so no packet crosses the boundary either. A random split of the training rows will therefore be optimistic, because it lets a model meet the same participant on both sides of a fold. To get an estimate that tracks the test set, hold out whole participants: the training rows carry no participant column, but a model selected on a participant-held-out estimate is the one that will transfer, and building such a split from the structure you can observe is part of the problem. Evaluation A row is scored on both halves at once. Let $B$ be the submitted set of bindings and $B^{*}$ the gold set. Binding quality is their F1, $$ F = \frac{2\,|B \cap B^{}|}{|B| + |B^{}|}. $$ Anchor quality is measured only where the binding is already right. For every gold binding, a correctly bound packet contributes the mean of its five anchor qualities and anything else contributes zero; the total is divided by the number of gold bindings. Call that $Q$. The row score is the geometric mean $$ S = \sqrt{F \times Q}. $$ The geometric mean is what binds the two halves together: a perfect set of bindings with useless clocks scores zero, and perfect clocks attached to the wrong sites also score zero. Let $n$ be the number of test rows and let $q = \lceil n/4 \rceil$. Let $W$ be the mean of the $q$ lowest row scores. The final score is $$ \operatorname{Score} = 0.85\left(\frac{1}{n}\sum_{i=1}^{n} S_i\right) + 0.15\,W. $$ The score is bounded to $[0,1]$. There are no hidden buckets or private slice weights. An empty program receives zero. Dataset The prepared public data contains: train.csv — labeled training rows; test.csv — unlabeled test rows; sample_submission.csv — submission template; task_manifest.json — public dimensions and scoring constants; and payload/ — one compressed archive of evidence arrays per row. train.csv id — type: string; opaque unique row identifier. evidence_file — type: string; relative path to this row's evidence archive. binding_program — type: string; JSON object holding the gold bindings and anchors. The packet pool size is fixed for every row and is published once in task_manifest.json as signals.packet_count. test.csv test.csv contains the same id and evidence_file columns. It does not contain binding_program. sample_submission.csv id — type: string; one required test identifier per row. binding_program — type: string; the sample submits no bindings and scores zero. task_manifest.json task — type: string; stable task identifier. split — type: object; row counts, the leakage unit, and the disjointness guarantee. signals — type: object; rate, window length, marker count, and pool geometry. target — type: object; binding range, anchor positions, and the anchor tolerance constants. metric — type: object; row formula and the two aggregation weights. submission — type: object; required columns and the program length limit. evaluation_environment — type: object; CPU, memory, GPU and network configuration. from_scratch — type: object; training requirement and pretrained-weight policy. Submission Format Submit one CSV with exactly these columns in this order: id — type: string; must match the test identifiers exactly, with no missing, extra or duplicate values. binding_program — type: string; a JSON object with exactly the keys bindings and anchors, at most 4,096 characters. bindings is a list of strings such as p3>s1. anchors maps each bound packet token to its five non-decreasing reference frames. A program is rejected, and that row scores zero, if a packet or a site is used twice, if a bound packet has no anchors, if anchors names a packet that is not bound, if a list does not hold exactly five whole numbers, or if the anchors decrease. A whole number written as a JSON float, such as 102.0, is accepted; 102.5 is not. The submission itself is rejected, and nothing is scored, if it carries any column beyond the two above, if the two columns are out of order, if an identifier is duplicated, if a required test identifier is missing, or if it carries identifiers that are not test rows. A concrete two-row CSV example is shown below without a fenced code block: Header: id,binding_program First row: w0a1b2c3d4e5f6071,"{""anchors"":{""p0"":[12,102,199,301,405],""p3"":[5,92,190,290,392]},""bindings"":[""p0>s2"",""p3>s0""]}" Second row: w9f8e7d6c5b4a3021,"{""anchors"":{},""bindings"":[]}" The doubled quotation marks are standard CSV escaping around the JSON object. Follow sample_submission.csv for the exact column order. The example identifiers are illustrative and are not release rows. A Practical Starting Point A reasonable first system can be built in four stages: Reduce each packet to quantities that survive rotation, such as acceleration magnitude and angular-velocity magnitude, and reduce the reference to gait traces such as total vertical force and marker vertical motion. Propose candidate clocks by scanning offset and rate, and keep several well-separated candidates per packet rather than only the best one. Train a model to choose among those candidates, and separately train a placement model and a decoy detector. Decode with an assignment step so that each site is used once. Two findings from building the reference solution are worth passing on. The strongest correlation peak is usually the wrong one. Running is quasi-periodic, so a candidate that is a whole stride away still matches well. Picking the best raw correlation lands inside the scoring tolerance about one time in seven. What separates the true stride from its neighbours is consistency: a true alignment holds across every quarter of the window, while a wrong-stride alignment has to distort its rate and then drifts. Stack your stages out of fold. A decoy detector that reads a candidate score produced in-sample by its own ranker will learn a threshold that does not exist at test time. Measured on the pilot, the same quantity reads 0.80 in-sample and 0.20 out of fold, and the in-sample version made the whole system reject nearly every packet. Compute Environment Submitted solutions run in a CPU-only environment with 10 CPU cores and 62 GB of RAM. No GPU or network access is available. Training, inference and decoding must all fit within those limits. Expected Output Your script receives the public dataset directory and exact submission CSV path as two positional arguments. &nbsp;
> $700 Pool
> Closes in 2h 38m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Geographic Metadata Prediction from Rainfall Signatures

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7dak7j8q3kd3zag22z928hvh8ag6qb
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat abu2win's score of 29.989!

Full challenge description from page:

> Challenge Overview This competition tasks your model with recovering four hidden geographic metadata attributes for 1,500 anonymous locations using only their multi-year daily rainfall time series as evidence. There are no coordinates, no maps, and no external reference data. The rainfall signature is the sole input signal. The core problem is from scratch: given several years of daily millimeter rainfall readings at an anonymous location, classify that location's continent, latitudinal climate zone, primary land cover type, and secondary land sub-classification. Models must learn to distinguish desert from rainforest, temperate from torrid, and plateau from river delta purely from how rain falls over time—its seasonality, intensity distribution, wet-dry cycle structure, and long-run statistics. What You Are Solving Each of the 1,500 evaluation locations has a complete multi-year daily rainfall record. From that record alone, your pipeline must predict four categorical attributes simultaneously: continent — which of seven continental regions the location belongs to geographic_zone — which of four latitudinal climate bands it falls in primary_land_type — which of eight major land cover categories describes it secondary_land_type — which of fifteen finer-grained sub-classifications applies There are no coordinate clues. The location_id is a 16-character deterministic hash with no recoverable spatial information. All geographic signal must be extracted from the rainfall time series itself. Dataset File Rows Contents train_rain.csv 2,000 location_id, all 4 metadata columns, full daily rainfall sequence test.csv 1,500 location_id, full daily rainfall sequence only (no metadata) sample_submission.csv 1,500 Correctly structured output template with placeholder values answers.csv 1,500 Private ground truth — not released during the competition Rainfall columns are named by date in YYYY-MM-DD format and record daily precipitation in millimeters. Approximately 2% of values are missing at random across both splits and must be handled by your pipeline. Row order in your submission must exactly match the row order in test.csv. Target Columns and Valid Classes continent Asia, South America, North America, Africa, Oceania, Europe, Seven seas (open ocean) geographic_zone North Temperate, South Torrid, North Torrid, South Temperate primary_land_type Agricultural Land, Savanna / Grassland, Forest, Desert / Barren, Rainforest, Urban / Developed, Shrubland, Coastal secondary_land_type Rural Plain, Tribal Land, Mountain, Cold Desert, Suburban Sprawl, Floodplain, Rainforest Blend, River Delta, Industrial Zone, Village, Plateau, Volcanic Terrain, Town Center, Fishing Community, Marshy Land Every predicted string must exactly match one of the values listed above, including capitalisation, spacing, and special characters such as the slash in Savanna / Grassland. Submission Format A single CSV file with exactly 1,500 rows and 5 columns, preserving the original row order from test.csv: location_id,continent,geographic_zone,primary_land_type,secondary_land_type 7e3ac4d91fb82a16,Asia,North Temperate,Forest,Mountain d8b25a03c1a8e2fd,Africa,South Torrid,Savanna / Grassland,Rural Plain Evaluation Submissions are scored on a Composite Error Score $S_{\text{error}} \in [0, 100]$. Lower is better. A perfect classifier scores 0. A model predicting the modal class on every target scores approximately 100. The score is the sum of four independently computed error terms, one per target column: $$S_{\text{error}} = T_1 + T_2 + T_3 + T_4$$ T1 — Continent (weight 22.0, metric: Balanced Accuracy) $$T_1 = 22.0 \times \left(1 - \text{BalancedAccuracy}(\hat{y}{\text{continent}},, y{\text{continent}})\right)$$ Balanced Accuracy is the mean per-class recall across all continent classes. It is used here because the continent distribution is skewed — open ocean and small continents are underrepresented — and a model that ignores minority classes must still be penalised. $T_1 = 0$ when every continent is classified perfectly. $T_1 = 22.0$ when balanced accuracy is 0. T2 — Geographic Zone (weight 25.0, metric: Macro F1) $$T_2 = 25.0 \times \left(1 - \text{MacroF1}(\hat{y}{\text{zone}},, y{\text{zone}})\right)$$ Macro F1 is the unweighted mean of per-class F1 scores across the four geographic zones. The four zone classes are roughly balanced, so each zone contributes equally to the term regardless of frequency. $T_2 = 0$ at perfect macro F1. $T_2 = 25.0$ at macro F1 of 0. T3 — Primary Land Type (weight 24.8, metric: Weighted F1) $$T_3 = 24.8 \times \left(1 - \text{WeightedF1}(\hat{y}{\text{primary}},, y{\text{primary}})\right)$$ Weighted F1 is the mean of per-class F1 scores weighted by the true support of each class. It is used here because the eight primary land types occur at different frequencies, and the metric naturally reflects real-world land cover distributions by penalising errors on common classes more heavily than errors on rare ones. $T_3 = 0$ at perfect weighted F1. $T_3 = 24.8$ at weighted F1 of 0. T4 — Secondary Land Type (weight 28.2, metric: Matthews Correlation Coefficient) $$T_4 = 28.2 \times \left(1 - \max!\left(0,; \text{MCC}(\hat{y}{\text{secondary}},, y{\text{secondary}})\right)\right)$$ MCC is bounded in $[-1, 1]$. Negative MCC values are floored to 0 before computing the error term, so the worst possible contribution from $T_4$ is 28.2 regardless of how badly a model performs. MCC is used here because the fifteen secondary land sub-classes are severely imbalanced. Unlike accuracy or F1, MCC accounts for all four cells of each pairwise confusion simultaneously and produces a reliable signal even when class frequencies differ by an order of magnitude. $T_4 = 0$ when MCC is 1. $T_4 = 28.2$ when MCC is 0 or negative. Score Bounds The four weights sum to exactly 100: $$22.0 + 25.0 + 24.8 + 28.2 = 100.0$$ Each term is independently bounded in $[0,, w_i]$ where $w_i$ is its weight, so the total score is strictly bounded in $[0, 100]$. No term can compensate for another: a perfect score on three targets does not mask failure on the fourth. What Not To Do Do not use any external geospatial or climate dataset. This includes ERA5, WorldClim, CHIRPS, MODIS land cover, Koppen climate maps, or any other third-party spatial or meteorological data source. All features must be derived solely from the provided rainfall columns. Do not use any pre-trained foundation model. Models pre-trained on geospatial, remote sensing, climate, or general-purpose time-series data are prohibited. Your model must be trained entirely from scratch using only the provided training split. Do not attempt to reverse-engineer the location_id hash. The identifier is a truncated SHA-256 hash of the underlying coordinate. No spatial information is recoverable from it and any attempt to decode or cross-reference it constitutes a rules violation. Do not submit NaN, null, or empty values in any cell. Every row must have a non-null string prediction for all four metadata columns. Submissions containing missing values will be rejected without scoring. Do not use class strings outside the defined vocabulary. Predicted values must exactly match the valid class strings as listed, including case, spacing, and punctuation. Variants such as "savanna/grassland", "Savanna/Grassland", or "Desert" are invalid and will cause submission rejection. Do not add, drop, or rename any columns. The submission must contain exactly five columns: location_id, continent, geographic_zone, primary_land_type, secondary_land_type, in that order. Any deviation from this schema will cause grading failure. Do not alter or reorder the location_id column. Row order must match test.csv exactly. Sorting, shuffling, or filtering rows will misalign predictions with ground truth and produce incorrect scores. Do not submit duplicate location_id values. Each of the 1,500 evaluation locations must appear exactly once. Duplicates will trigger a validation error before scoring. Do not exceed the one-hour total runtime limit. Your full pipeline including data loading, feature engineering, model training, and inference must complete within 60 minutes on the provided CPU environment. Do not use GPU compute resources. The competition environment is CPU-only. Pipelines requiring CUDA or GPU-accelerated libraries will fail on the evaluation infrastructure. Targets must remain as their original string class values throughout. No re-, inverse-mapping Do not use purely statistical baselines such as predicting the modal class, sampling from the training distribution, or assigning labels by rainfall mean matching. Your model must learn a genuine mapping from rainfall features to geographic class. Submissions that score at or below the modal-class baseline on all four targets will be disqualified. &nbsp;
> $700 Pool
> 0 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Retraction Discovery from Anonymised Abstract Vocabulary

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx74j69tsp1c9sj0re1npgmryn8dypfz
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat nahi's score of 0.432!

Full challenge description from page:

> Retraction Discovery from Anonymised Abstract Vocabulary Overview This is a from-scratch discovery task with a fixed budget. Every row is a self-contained selection problem: twelve anonymous items, of which exactly five carry the property being sought. The count is known and binding, so the answer is one joint selection per row rather than twelve independent labels, and the predictive component that produces it must be trained from randomly initialised parameters inside the submitted script. The property is retraction. A paper is published, indexed, cited — and then, months or years later, its publisher pulls it. By the time that happens the text that got it through review is still sitting in the abstract, and nobody can name in one number what separates it from an honest abstract of the same journal, the same year and the same field. Each row holds twelve anonymous word bags — the vocabulary of twelve scientific abstracts, each reduced to lowercase tokens and counts with the word order destroyed — in shuffled order. All twelve articles were published in the same year and belong to the same broad field. Exactly five were later retracted by their publishers; seven never were. Your job: mark the five. The answer for a row is a string of twelve letters, y for a later-retracted article and n for one that stands, with exactly five y, aligned with the published order of the bags. Where The Answers Come From Every answer is a recorded fact of a public archive. Each bag is a real abstract from OpenAlex, and the label is the retraction flag OpenAlex carries for that article is_retracted), which it takes from Crossref's ingestion of the Retraction Watch database. The flag, the title, the authors, the venue, the year, the field, the citation count and every identifier are withheld from the payload. Nothing in the published numbers states the verdict; it has to be read out of the words. Retraction is a verdict of the community rather than a property of the text, and some withdrawn papers carry no trace of it in their abstract — an authorship dispute, an ethics finding, a duplicated figure. Those rows are part of the task as it exists in the world. Six construction facts shape what is learnable: The venue is composed away. Wherever the venue supplies one, each retracted article is paired with a never-retracted article of its own journal and year, and the remaining decoys come from other journals that also hold retracted articles: 46 percent of decoys are venue-matched, at least three in every row. A journal's house style therefore sits on both sides of the answer. The year and the field are shared across all twelve items of a row, so neither era vocabulary nor topic separates the five from the seven. Size is banded. A row's longest bag holds at most about 1.8 times the tokens of its shortest (a within-row spread of at most 0.6 natural-log units, median 0.48), and length grips nothing: ranking a row's bags by total tokens scores about 0.12 on test rows, indistinguishable from the random floor. The vocabulary is capped at the 10,000 most document-frequent tokens of the corpus; rare names and one-off jargon are gone, so there is nothing to look up and no author to recognise. Numerals are not removed: 648 of the 9,973 published vocabulary types carry a digit and 71 per cent of bags hold at least one, so a model may use them; what the cap removes is the rare figure that would identify a paper, not arithmetic in general. The journals and the authors are cold. The split is by journal — every test row comes from venues no training row showed — and any article whose author list touches both sides was removed before rows were composed. Training rows reuse abstracts. The 13,800 training bag slots draw on 6,271 distinct abstracts, up to four copies each, while the 3,444 test bags are all distinct. Every copy stays inside one journal group, so grouped validation is unaffected — but repetition is a training-only artefact: marking a row's five most-repeated bags scores 0.19 on training rows against a 0.11 floor, and reaches nothing on test. Three latent correlates were measured on withheld metadata and are disclosed because none of them is published: within-row rules on citation count, author count and pre-cap abstract length reach 0.12, 0.17 and 0.12 respectively. Transporting a row's correct mask to its neighbour scores 0.10, indistinguishable from chance. For scale, one published baseline: a plain logistic regression on L2-normalised token counts, its vocabulary fitted on the training rows alone, scored per abstract and decoded by marking each row's five highest, reaches 0.3725 on the test rows, and stock variants of it — TF-IDF weighting, row-relative centring, an SGD or hinge loss — all land between 0.371 and 0.383, so that is the level of the stock linear family rather than of one lucky configuration. With 287 test rows and a per-row standard deviation of 0.2550, a test score carries a standard error of about 0.015. Evidence Every row is one JSON file holding a single key. bags — type: array; twelve objects in published order. Each object maps a lowercase token (a string) to its count in that abstract (a positive integer). A token is a whitespace-separated word with leading and trailing .,;:()[]{}"'!? removed and nothing else, so numerals and word-internal punctuation survive and forms such as 0.001, 95%, p=0.001 and hyphenated compounds are ordinary tokens; the vocabulary is the corpus's 10,000 most document-frequent tokens, so a bag holds only those. No titles, sentences or word order are published, and every bag holds between 60 and 500 tokens in total. Evaluation Each row is scored by the skill of the marked five over the floor a random mask would reach. If overlap is the fraction of your five marks that were truly retracted, the row score is $$ R = \max\left(0,\ \frac{\mathrm{overlap} - 5/12}{1 - 5/12}\right), $$ so a perfect mask scores one and a random mask about zero. Because each row is clipped at zero, a random submission averages a little above zero over many rows; that is a property of the clipping, not skill. Let $M_{\mathrm{all}}$ be the mean row score over all test rows and $M_{\mathrm{alike}}$ the unweighted mean of the per-band means, where rows are grouped by the public blend_band column. The final score is $$ 0.80\,M_{\mathrm{all}} + 0.20\,M_{\mathrm{alike}}, $$ bounded to the interval from 0 to 1. There are no hidden buckets. blend_band bands each row by the mean pairwise cosine distance between its twelve bags, so rows whose abstracts read alike are priced separately and no easy stratum carries the score alone; it carries nothing beyond what the published bags already show. A cell that is not a legal mask — anything other than twelve letters from y and n with exactly five y — is treated as a wrong answer rather than a broken submission: that row scores zero and every other row is still scored. Validating Your Model The leakage unit is the journal, with authors kept apart on top of it: every test row comes from journals and authors no training row showed. Journal identity is withheld, so validation_groups.json supplies the grouping: every training bag carries an opaque token, and two bags share a token exactly when they came from the same journal. Hold out tokens. It is an item-level grouping rather than row-level folds because a row draws its twelve bags from 7 to 12 different journals — a retracted article and its venue-matched decoy share one — and over the training rows the "shares a journal" graph is a single connected component: no split of whole rows can be journal-disjoint. A suggested five-way assignment of tokens to folds ships alongside, and 2,128 of the 2,629 training journals contribute more than one bag, so the grouping bites. From-Scratch Requirement Every submitted solution must train a genuine predictive component using the released training rows, and that component must materially determine the submitted masks. The training must happen inside solution.py during the graded run, from randomly initialised parameters: loading weights fitted beforehand, shipping a model with the submission, or reaching pretrained parameters through a library does not satisfy this. Network access is disabled during evaluation. Allowed Approaches bag statistics — length, vocabulary size, hapax share, digit share, mean token length, type-token ratio — feeding any standard model, scored per abstract and decoded by taking the five highest; hashed or explicit vocabulary vectors, with the vocabulary defined by the training rows, feeding linear models, gradient boosting, or small neural networks initialised with random weights and trained only on the released rows; relational features that compare an abstract with the other eleven in its row; any decode that respects the exactly-five budget, including assignment or ranking decoders; and standard numerical and machine-learning libraries already present in the evaluation environment. What Not To Use No external datasets, and in particular no bibliographic archive, no OpenAlex, Crossref, PubMed or Retraction Watch copy, no citation index and no text corpus of any kind. Do not attempt to identify the underlying articles, authors or venues, or to recover any withheld field, by matching the published bags against anything not released here. This is grounds for automatic disqualification. No pretrained weights of any kind — no language models, no word embeddings, no sentence encoders, no tokenizers trained elsewhere — and no features, embeddings or labels produced by a pretrained model. No external APIs, no network calls at grading time, and no remote inference. No use of the test set beyond ordinary per-row inference: no training on test rows, no pseudo-labelling, and no fitting, calibrating, thresholding or normalising with statistics pooled across the test set — including vocabulary or document-frequency statistics computed over test bags. No linking across test rows: matching bags between different test rows, clustering the test set by vocabulary, or carrying any information from one test row into another is test-set use and is prohibited. Each row must be resolved from that row's own twelve bags plus what was learned from the training rows. No fixed hand-written pipeline that has no component fitted from the released labels. No hardcoded lookup tables, no fingerprinting of row identifiers or row order, and no manually supplied answers. Row identifiers are opaque and row order is randomised; both carry nothing. Dataset The prepared public data contains: train.csv — labeled training rows; test.csv — unlabeled test rows; sample_submission.csv — submission template; validation_groups.json — journal groups for validating on the training rows; task_manifest.json — public dimensions and scoring constants; and payload/ — one JSON file per row holding that row's twelve bags. train.csv id — type: string; opaque unique row identifier, the letter w followed by sixteen hex characters. evidence_file — type: string; relative path of the row's JSON file. blend_band — type: string; one of a, b, c, d, the row's look-alike band. withdrawn — type: string; twelve letters, y for a later-retracted article and n otherwise, exactly five y, aligned with the order of bags. test.csv test.csv contains the same id, evidence_file and blend_band columns. It does not contain withdrawn. sample_submission.csv id — type: string; one required test identifier per row. withdrawn — type: string; a valid mask that reads no evidence. The template rotates the five marks through the twelve positions, so a row's five marks are wherever the rotation puts them; a real prediction marks any five. validation_groups.json leakage_unit — type: string; the journal. grouping — type: string; what a shared token means. why_not_folds — type: string; why the grouping is per item rather than per row. applies_to — type: string; training rows only. n_groups, n_folds — type: integer; the counts. group_of — type: object; training row id to its twelve group tokens, in published bag order. fold_of_group — type: object; group token to a suggested fold, f0 through f4. task_manifest.json task — type: string; stable task identifier. primary_modality — type: string; the form of the published evidence. split — type: object; row counts, the leakage unit and the journal-disjoint guarantee. validation — type: object; the groups file, the grouping it carries, the level it applies at and the rows it covers. signals — type: object; items per row, true per row, the item form and the row composition. target — type: object; the mask grammar and the exactly-five guarantee. metric — type: object; the exact row and final aggregation constants used by the grader. submission — type: object; column names and mask length. evaluation_environment — type: object; CPU, memory, GPU and network configuration. from_scratch — type: object; training requirement and pretrained-weight policy. Submission Format Submit one CSV with exactly these columns in this order: id — type: string; every test identifier exactly once, with no duplicates and nothing else. withdrawn — type: string; twelve letters from y and n with exactly five y, one letter per bag in published order. Faults of the submission as a whole are refused outright rather than scored: any column other than id and withdrawn, those two columns in a different order, a duplicate identifier, a missing test identifier, or an identifier that is not a test row. A concrete two-row CSV example is shown below without a fenced code block: Header: id,withdrawn First row: w0123456789abcdef,ynnynyynnnny Second row: wfedcba9876543210,nnyyynnnynny The example identifiers are illustrative and are not release rows. Intended Use and Known Limitations This is a benchmark for from-scratch text models, meant for practitioners building such models and for research-integrity researchers; every identifier is withheld and no score here says anything about any real paper, author or journal. Its limits are stated rather than hidden: the retraction flag is a Crossref/Retraction Watch snapshot and misses unregistered or later retractions; retraction rates are very uneven across fields, years and publishers, which the row composition neutralises inside a row but which shapes the dataset's mix; many retractions are for reasons that leave no trace in the abstract, which caps the attainable score; and the word-bag form with a 10,000-token vocabulary discards word order and rare terminology by design, though common numerals remain. The full list is in the dataset description. Compute Environment Solutions are evaluated on CPU only — 10 cores, 62 GB of memory, no GPU, no network — within a wall-clock budget of ninety minutes for training and inference together. &nbsp; &nbsp;
> $700 Pool
> Closes in 5h 9m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Palimpsest — Recovering The Layering Of An Occluded Neurophysiological Stream

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx78g1zvs0htk7cs6revghqn8s8c5nsj
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Medium
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat civil_dept's score of 0.685!

Full challenge description from page:

> The problem A palimpsest is a manuscript whose earlier writing was scraped away so a later text could be written over it. The earlier text is not faint — it is gone — and what a scholar reconstructs is the arrangement: which layer sat on top, where, and which layers were present underneath while contributing nothing visible. Each item here is one 1-D array of 3,000 measurements, assembled from several real de-identified overnight neurophysiological recordings, each contributed by a different person. Those source recordings act as layers that occlude one another according to a hidden schedule. At every position exactly one layer is written into the array; the others contribute nothing at all. Every value in the array is copied verbatim from exactly one layer. No value is ever a sum, average or fade of two layers — an occluded layer is erased, not buried under noise. Switching happens only on frame boundaries, so all 2 values of any given frame come from the same layer and every frame label is unambiguous. Your task is to reconstruct the layering. Items are grouped into blocks, and a block is the unit you are scored on Items do not stand alone. They come in blocks. A block is a set of **30 items built from the same 6 source recordings** — the same six people, recombined 30 different ways with independently drawn depth orders, filters, gains and schedules. Blocks partition the source recordings: a recording belongs to exactly one block and appears in no other. That makes the block, not the item, the independent unit — so a block is one row everywhere: one row of train.csv, one row of test.csv, one row of your submission, one array file, and one unit of the score. This is also a resource. Within a block the same six layer identities recur across all 30 items, so evidence pooled across a block's items can help you resolve any one of them — while the depth order is redrawn per item, so the block never tells you the answer. Data Every item is 3,000 float16 measurements: 60 seconds at 50 measurements per second, normalised to zero mean and unit variance. Each block's items are stored together, so a block's array has shape (30, 3000). Predictions are made on a coarser frame grid of exactly 1,500 frames per item; each frame spans 2 consecutive array positions. Each item contains 3, 4 or 5 occluding layers, numbered by depth rank, where rank 1 is frontmost. The number of layers is not given to you; for a training item it is simply the largest value appearing in that item's visible sequence. Beneath them lies a **bed layer** that is always active and is never itself graded; it is labelled 0 and guarantees the array is never empty. Files | Path | Contents | |---|---| | train.csv | one row per training block: the id and both label columns | | test.csv | one row per test block: the ids you must predict | | sample_submission.csv | a valid, correctly-formatted submission filled with random labels; it scores at the floor | | train/.npy | one training block, float16, shape (30, 3000) | | test/.npy | one test block, float16, shape (30, 3000) | | meta.json | grid constants: array length, frame count, items_per_block (30), block counts, dtype | Columns of train.csv block_id — string. Opaque identifier. Matches the filename train/.npy. visible_rle — string. The block's 30 visible-layer sequences, serialised and separated by |, in array-row order. Each segment is a run-length encoding over 1,500 frames with values 0–5. buried_rle — string. The block's 30 buried-count sequences, same serialisation. Values 0–4. Columns of test.csv block_id — string. Opaque identifier. Matches the filename test/.npy. Every block holds exactly 30 items. That count is published once, as items_per_block in meta.json, and is the first dimension of every block array; it is not repeated per row. Columns of sample_submission.csv block_id — string. visible_rle — string. 30 |-separated segments of randomly drawn valid runs. buried_rle — string. 30 |-separated segments of randomly drawn valid runs. The sample's labels are a random draw, independent of the answers: it demonstrates the format and scores at the floor. Overwrite every cell with your predictions. The two quantities to predict For every item of every test block: 1. visible — which layer is on top. For each of the 1,500 frames, an integer in 0..5: the depth rank of the layer written into the array at that frame, or 0 if the bed layer is showing. This requires segmenting the array, grouping the fragments that belong to the same layer, and ordering those layers by depth. 2. buried — how many layers were erased. For each of the 1,500 frames, an integer in 0..4: how many layers were active at that frame but occluded by a layer in front of them, and therefore contributed nothing. A frame where the frontmost layer is showing and two deeper layers happen to be active scores buried = 2. buried counts layers that are, by construction, absent from the array at that frame. It is inferable only from what your model learns about how layers behave across the sequence. Encoding Each item's sequence is run-length encoded: space-separated value:length tokens, in frame order, whose lengths sum to exactly 1,500. 0:120 2:45 1:300 0:1035 means frames 0–119 have value 0, frames 120–164 have value 2, frames 165–464 have value 1, and frames 465–1499 have value 0. Run lengths must be positive integers. Consecutive runs may repeat a value; that is accepted. A block's 30 item encodings are then joined with |, in array-row order — segment k describes row k of that block's .npy: 0:120 2:1380|1:1500|0:60 3:1440| ... |2:900 1:600 Submission format A file named submission.csv with exactly these three columns: block_id,visible_rle,buried_rle b3f9a1c04b27,0:120 2:1380|1:1500|...,0:400 1:1100|0:1500|... One row per block_id in test.csv. Every test block must be present exactly once. Each cell must contain exactly 30 segments separated by | — one per array row (items_per_block in meta.json). visible_rle values must lie in 0..5; buried_rle values in 0..4. Every segment must cover exactly 1,500 frames. Duplicate ids, missing ids, the wrong number of segments, malformed encodings, out-of-range values, blank entries, and segments that do not cover exactly 1,500 frames are all rejected, not partially credited. Evaluation For each item: score_item = 0.5 * kappa_visible + 0.5 * kappa_buried kappa_visible — Cohen's kappa between your visible sequence and the true one, over the 6 labels 0..5, unweighted. kappa_buried — Cohen's kappa between your buried sequence and the true one, over the 5 labels 0..4, with linear weights, so being off by one costs less than being off by three. A block's score is the mean over its 30 items. The final score is the **mean over blocks**, clipped once to [0.01, 1.0]. Blocks are weighted equally, because the block is the independent unit. Both terms are chance-corrected: a constant prediction, a random prediction, and the supplied sample_submission.csv all score at the floor. A perfect submission scores exactly 1.0. Partial credit is continuous in both terms. The two terms reward different capabilities. kappa_visible rewards segmentation, grouping and depth ordering. kappa_buried rewards learning how long layers tend to stay active, and is worth half the score on its own — a submission that segments perfectly but predicts a constant buried sequence forfeits half the available points. Rules: Train from randomly initialised weights. **Pretrained weights, foundation models and transfer learning are not permitted**. Both predicted columns must come from a trained model. A hand-written rule that emits either column without a learned component does not satisfy the task. Deleting the trained model must leave the pipeline unable to produce a submission. CPU only. No GPU. 1.5 hours total for training and full inference. Split design and leakage safeguards Sizes. Roughly 98 training blocks and 66 test blocks, 30 items each. The split is defined on people, and a person belongs to exactly one row. Items are assembled from a pool of 989 de-identified overnight recordings, each from a different person. Those recordings are partitioned into disjoint blocks of 6 **before any item is built**, and a block's items draw their layers only from that block's own six recordings. Blocks are then assigned wholly to train or to test. Because a recording belongs to exactly one block, and a block is exactly one row, **no source recording can appear in two rows** — so no recording can straddle the train/test boundary, and none can straddle the public/private leaderboard boundary however rows are assigned to it. This is verified rather than asserted, and holds in every simulated assignment. Why the training labels do not give away the test schedules. Every item's schedule is an independent draw from the generator. No schedule is shared between two items, and no per-item schedule parameter is published anywhere. What the training labels do reveal is the distribution the schedules are drawn from — how long layers tend to stay active, how often they switch, how depth relates to visible time. **Learning that distribution is the intended task**, and it is the only route to the buried column, which is by construction absent from the array itself. Knowing the distribution tells you nothing specific about any individual test item beyond what its own array supports. Two further consequences worth stating. Expected visible time is deliberately **equalised across depth ranks**, so a layer's depth cannot be read off how long it is visible. And because roughly half of all discontinuities are decoys rather than layer changes, the count of detectable seams does not reveal the number of layer changes. &nbsp;
> Closes in 1h 20m
> 12 / 12 continuing slots

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Epitope Window Localisation From Antigen Tokens

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7bqxmktd3nk0betbym0ps0sd8e44pv
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Not displayed; detail page unavailable
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Beat 15_luz's score of 0.198!

Full challenge description from page:

> Epitope Window Localisation From Antigen Tokens Part 1: Overview You are given a long token sequence representing a viral protein (the antigen). Your model must output a fixed-length token sequence representing the window that surrounds one of that protein's epitopes. The antigens are derived from real protein sequences carrying annotated linear peptide epitopes, but every amino acid has been replaced by a deterministic integer token using a private salted substitution cipher combined with a coarse positional encoding. Token values lie in the range 0 to 159, where 0 is the padding token and 1 to 159 are the synthetic amino-acid-plus-position tokens. The mapping is private and irreversible by design. The only way to solve the task is to learn the sequence patterns present in the training set itself, with parameters trained from a random initialization, since no pretrained checkpoint carries signal about a cipher generated fresh for this challenge. The target window is a contiguous slice of the input. Except where the epitope sits within 25 tokens of a protein terminus, in which case the window is clipped and padded with 0s, the answer is exactly input[k : k+50] for some offset k. The task is a localisation task, and that is what the score measures: where your window sits, not how many of its tokens happen to coincide with the answer. Up to 25 tokens of positional slack is forgiven; see Part 4. Train and test antigens are disjoint and are drawn from the same deterministic hash-based partition of the antigen population, so memorisation cannot transfer and there is no distribution shift unrelated to the task itself. Two properties of this construction determine what a good solution looks like. First, the score is corrected against chance on a per-row basis, and that correction is the expected score of a window placed uniformly at random over every legal offset on that antigen. It is not the score of any particular fixed strategy, and it is not a maximum over an enumerated list of strategies. Per-row values are free to go negative and the only floor is applied once, to the final mean. Together those choices neutralise the entire class of input-independent strategies rather than a handful of named members: a rule that ignores the antigen scores above chance where it happens to land near an epitope and below chance where it does not, and the two cancel before any floor is reached. There is no credit available from a prediction that does not read the antigen; every such strategy reports exactly 0.000000. Second, test antigens are restricted to those carrying at most two annotated windows and to those where a blind guess is not already likely to succeed. Because the grader keeps the best-matching annotated window, a densely annotated protein makes almost any placement nearly right. Densely annotated proteins are excellent supervision and remain in the training split; they are simply not used to score you. The scale is deliberately kept open. The mean headroom per row, meaning one minus the row's chance level, is 0.8593, the smallest on any row is 0.6025, and no row falls below 0.6. Scoring 1.0 would require locating a true window on all 301 test antigens. This challenge is built to be solved entirely on CPU. No GPU is provided and none is needed. Antigens run up to 7,107 tokens long against a vocabulary of only 160 token values, so the intended solutions lean on fast vectorised operations and modestly sized models. Every reference number quoted here was produced on CPU only, on the exact files this challenge ships. Part 2: Data File Structure Three public CSV files are provided, plus one private file that only the grading script reads. 2.1 train.csv 12,281 rows drawn from 585 antigens. Columns: id, input, output. Ids run 0 through 12280. Median antigen length is 561 tokens and the longest training antigen is 3,898 tokens. The single longest antigen overall, 7,107 tokens, falls in the test set. Each row is one annotated epitope on one antigen, so the same antigen can appear in several rows. The training split deliberately retains the heavily annotated proteins excluded from scoring: 244 antigens for carrying more than two annotated windows, and 35 for having a chance level too high to be worth scoring. Some training antigens carry hundreds of annotated epitopes, which is a large amount of supervision if your feature extraction is vectorised and a performance trap if it is not. A shortened example, with the middle of each field elided: id,input,output 0,112 88 88 16 72 152 32 128 16 64 64 16 24 16 ... 39 7 31 47,79 103 63 63 71 103 39 71 55 103 31 31 103 55 ... 151 7 143 103 2.2 test.csv 301 rows drawn from 301 antigens, one row per antigen. Columns: id, input only. Ids run 12281 through 12581. Median antigen length is 696 tokens, the shortest is 202 and the longest is 7,107. Of the 301 test antigens, 244 carry exactly one annotated window and 57 carry two; none carries more. A shortened example: id,input 12281,112 136 96 64 56 56 8 152 32 152 8 152 136 152 ... 14 14 22 94 38 94 38 150 134 126 86 38 Because test.csv has one row per antigen even when that antigen carries two annotated epitopes, the ground truth cannot live in test.csv. A single input column has nowhere to put more than one answer, which is what section 2.4 is for. 2.3 sample_submission.csv 301 rows, one per test id. Columns: id, prediction. A format example only: it is the 50 tokens at the middle of each antigen, a content-free strategy, and it scores 0.000000. A shortened example: id,prediction 12281,50 50 58 98 50 58 50 50 58 130 50 34 50 50 58 ... 51 59 99 51 51 115 51 59 35 51 51 51 35 59 2.4 The private answers file, grader-only, not shipped to you It mirrors test.csv row for row: one row per antigen, same order, same ids. It carries five columns: id, antigen_tokens, output, true_spans, and baseline. antigen_tokens holds the same token sequence as the public test file's input column, repeated so the grading script is self-contained and can never be run against a mismatched input file. true_spans holds every annotated window for that antigen packed into one field, as semicolon-separated start:end token-offset pairs. This is the ground truth the grader scores against. A real example row carrying two valid windows: id,antigen_tokens,output,true_spans,baseline 12286,... antigen tokens, omitted ...,... 50-token window, omitted ...,901:951;2048:2098,0.053106 output is the single largest annotated window on that antigen, in the same form train.csv carries. The grader does not read it, because an antigen with two annotated windows cannot be represented by one window. baseline is that row's own chance level, explained in Part 4. Across the 301 test rows it has mean 0.1407 and median 0.1228, ranging from 0.0126 on the longest and sparsest antigens to 0.3975 on the shortest. When the grader scores a prediction it splits true_spans on ";" and each piece on ":" to recover a list of start and end pairs, then compares your prediction against every pair and keeps whichever gives the best score. You are never penalised for locating a different but equally valid epitope on the same protein. 2.5 Column reference id: unique integer, globally unique across train and test. input: space-separated integers, the tokenised antigen. In train.csv and test.csv. output: exactly 50 space-separated integers. The epitope, 8 to 30 tokens long, plus 10 tokens of flanking context on each side, clipped at the protein boundary and padded with 0s to length 50 when clipping happens. Padding is only ever appended at the end of a clipped window, and 0 is also a legitimate token value in its own right, so do not strip zeros indiscriminately when recovering offsets. antigen_tokens, true_spans, baseline: private answers file only, described above. Part 3: Submission Format Submit a CSV with exactly two columns, id and prediction. id must include every test id exactly once, in any order. prediction is a string of space-separated integers. Predictions may be any length. 50 tokens is the natural choice since it matches the training outputs, and lengths far from 50 are penalised automatically by the metric. A prediction that cannot be parsed as integers, including an empty string or a missing value, is scored as a raw 0, which is negative for that row after the chance correction. Averaged over every row that comes to minus 0.181069, worse than any other strategy measured, so blank rows drag down the rows you did answer. Submit your best guess on every row. Example submission file: id,prediction 12281,50 50 58 98 50 58 50 50 58 130 50 34 50 50 58 ... 51 59 99 51 51 115 51 59 35 51 51 51 35 59 12282,59 99 52 52 60 36 100 12 36 36 ... 12 156 52 12 100 12283,157 29 125 125 5 117 157 45 37 13 ... 45 6 14 158 110 Part 4: Evaluation The metric is computed in three stages per row, then averaged. 4.1 Anchoring Your prediction is slid over the antigen and placed at the offset with the largest number of exact token matches. Only the first 400 tokens of a long prediction are used to find the offset, but the prediction's full length determines the span once placed. Anchoring is a single vectorised sliding-window comparison, so it stays fast even on the longest antigens. That placement defines your predicted span, clipped to the protein. If several offsets tie for the best match count, the worst-scoring one is used, because a prediction that fits equally well in many places has not demonstrated that it located anything. 4.2 Raw score The raw score is a shift-tolerant intersection-over-union between your anchored span and the true window span. Plain intersection-over-union is the size of the intersection divided by the size of the union. The shift-tolerant version slides your anchored span by up to 25 tokens in either direction before applying that formula and keeps the best result. A shift of 0 is always included, so this can only help a prediction that was already well placed. Two worked examples. Each takes the true window, 50 tokens long, and displaces it by d tokens; the prediction is an exact slice of the antigen, so anchoring places it back at its own offset, d tokens from the true span. With d equal to 15, the best shift is minus 15, inside the tolerance, cancelling the displacement exactly. Intersection 50, union 50, raw score 1.0. With d equal to 40, the best shift is minus 25, the full tolerance, leaving 15 tokens of residual misalignment. Intersection 35, union 50 plus 50 minus 35, which is 65. Raw score 35 divided by 65, which is 0.538462. In general, for any displacement d larger than the tolerance, intersection is 75 minus d and union is 25 plus d, so the raw score is (75 minus d) divided by (25 plus d): 0.538462 at d equal to 40, 0.333333 at 50, and exactly 0 at 75 where the spans no longer touch. Those are clean cases away from the termini. A whole submission built by displacing every true window by 40 tokens scores a mean raw 0.6153 here, higher than 0.538462, because near a terminus the displacement is clipped by the end of the protein, and on a two-window antigen the displaced prediction sometimes matches the other window better. Predicting far too many tokens, such as dumping the whole input, still collapses the score regardless of tolerance, because the union grows with your prediction's length and no shift fixes that. If the antigen has two annotated epitopes the grader scores against each and keeps the better match. Reproducing a true window exactly, or within tolerance, gives a raw score of 1. 4.3 Chance correction Every test row carries its own baseline: the expected raw score of a window placed uniformly at random over every legal offset on that antigen, computed under the identical shift-tolerant metric. It is a property of the antigen and its annotated windows alone, not the score of any named strategy and not a maximum over a family of them. Your adjusted score for the row is your raw score minus that baseline, divided by one minus that baseline. Per-row values may be negative. 4.4 Final score The final score is the mean of the adjusted per-row scores across all 301 test rows, floored at zero. The floor is applied once, to the mean, and never per row. Per-row cancellation still happens in full before the floor is reached, so a blind rule's lucky rows are still cancelled by its unlucky ones; the floor only clips the negative tail of the aggregate. A per-row floor, by contrast, would let a bimodal content-free strategy bank the rows it hit and have the floor absorb the rows it missed, which is the defect this metric exists to avoid. The reported score therefore lies in the closed interval from 0 to 1, with a content-free baseline at exactly 0 and the known answers at exactly 1. Part 5: Reference Scores And Metric Design Every figure here was measured on the exact files this challenge ships. 5.1 Measured scores A perfect prediction, reproducing a true window on every row, scores 1.000000. Every content-free strategy reports exactly 0.000000, each having a negative mean before the floor. Their unfloored means, which show the correction rather than the floor is doing the work, are minus 0.018382 for the first 50 tokens, plus 0.003204 for a slice ten tokens in, minus 0.003448 for the last 50 tokens, minus 0.041180 for the middle 50 tokens, minus 0.055384 for all zeros, minus 0.079117 for the whole input dumped verbatim, minus 0.0956 on average for fifty uniformly random tokens across ten trials, and minus 0.181069 for an empty or unparseable prediction. The fixed-position class was swept exhaustively rather than sampled. Taking the 50 tokens centred at fraction f of the antigen, for 201 values of f from 0 to 1, gives adjusted scores with mean plus 0.0013 and standard deviation 0.0258, minimum minus 0.0436 and maximum plus 0.0531 at f equal to 0.130. The class is centred on zero and its maximum is the largest of 201 correlated estimates drawn from a zero-centred distribution, about two standard deviations above the mean, which is what the maximum of a sweep that size is expected to look like. It is not evidence that a positional rule works. A reference from-scratch CPU solver scores 0.1207 and 0.1233 on two independent seeds, a mean of 0.1220 with a seed-to-seed spread of 0.0026 and a per-row standard error of 0.0277. It is a small ensemble of gradient-boosted classifiers over prefix-sum window features: single-token composition of the candidate 50-token window, the composition of each half, dipeptide composition, the composition of a wider 150-token context, and the window's relative position in the protein. Training offsets were recovered from train.csv by exact substring search; every offset within 10 tokens of a true window start was treated as a positive, negatives were drawn only from offsets at least 60 tokens from any annotated window, and per-offset scores were smoothed before the argmax. That solver places a true window within tolerance on 24.3 percent of test antigens. An unensembled single member of the same family scores 0.0791 and 0.0807 on two seeds, so averaging a handful of members lifts the result by about half again for a few minutes of extra CPU. Separation between the reference and the content-free class is best read against the class distribution rather than its maximum, since the maximum of a 201-point sweep is selected for being the largest and sits above the class mean whether or not any rule works. Against the distribution, the reference at 0.1220 sits about 4.7 standard deviations above the class mean of plus 0.0013 using the class's own standard deviation of 0.0258. Against the maximum of plus 0.0531 it clears by about 2.5 standard errors. Both are reported because they answer different questions. 5.2 Why this metric rather than a standard one Per-residue F1, the usual choice in this area, gives substantial credit to strategies that read nothing. Measured here, treating the union of annotated windows as the positive residue set, a fixed 50-token slice at the start scores 0.1000, a slice at one quarter 0.1002, a slice at the end 0.1092, and dumping the whole input 0.1528, against 0.9646 for a perfect prediction. A content-free dump therefore keeps roughly a sixth of the available scale. Under the metric used here those same strategies report exactly 0.000000. A per-row chance correction is used rather than a single global constant because chance level varies enormously with protein length and annotation count: across the 301 test rows it ranges from 0.0126 to 0.3975, a spread of 31.7 times. A global constant would over-correct the easy rows and under-correct the hard ones. 5.3 Why the tolerance is 25 tokens Tolerance helps a model that is systematically close, but it also helps a blind rule that lands nearby, and the second effect eventually dominates. The value was chosen by sweeping it and measuring the separation between the reference model and the fixed-position class in units of that class's own standard deviation. At tolerance 0 the separation is 2.40; at 10 it is 3.48; at 15, 3.94; at 20, 4.33; at 25, 4.63; at 30, 4.72; at 40, 4.50; at 50, 3.87; and at 75 it collapses to 1.87, where blind rules score almost as well as the model. The separation sits on a plateau between 25 and 30 and falls away on both sides. The value 25 is the conservative end: 30 is marginally higher but statistically indistinguishable, and the smaller tolerance demands more localisation accuracy. Widening beyond the plateau would make the task easier to score well on while making it worse at telling solutions apart. 5.4 What to aim for Treat 0.12 as the level to beat and 0.05 as the highest figure any content-free rule reached in the exhaustive sweep. The signal here is real but weak: the reference locates the window on about a quarter of antigens and misses on the rest. The scale above it is wide open, with a mean headroom of 0.8593 per row and no row below 0.6. Part 6: Task And Goal Predict where the epitope window lies in antigens your model has never seen. Test antigens are new, so memorisation will not work, and positional priors are priced into the chance correction. You must learn the sequence and composition patterns that mark epitope regions from scratch, within a CPU-only budget. A practical route: recover each training window's exact offset within its antigen. The window is a contiguous slice, so an exact substring search on the first twenty tokens of the output finds it directly and cheaply. Then train a per-position or per-window scorer from that supervision, and at inference emit the 50 tokens around whichever position your scorer ranks highest. This is the route used to produce the reference score. Three things measurably moved the reference. Treating offsets near a true window start as positives, rather than only the exact start, gives far more training signal and a smoother objective. Drawing negatives only from offsets well clear of any annotated window stops the model being punished for near-misses it should be rewarded for. Averaging a small ensemble took the same feature set from about 0.080 to about 0.122, the single largest improvement measured, for a few minutes of extra CPU. Beyond that, the reference throws away most of what it has learned at the final ranking step: it scores every candidate window in isolation and takes an argmax. Attacking that step is the most promising direction. Aggregate evidence across overlapping windows rather than scoring each independently. Calibrate the per-window score so it is comparable across proteins of very different lengths, which matters because the candidate count ranges from about 150 to over 7,000. Use a cheap first pass to shortlist candidate offsets and a second-stage model to re-rank the shortlist with features too expensive to compute everywhere. Other CPU-friendly options include sequence models that use token order rather than only frequency, and self-supervised pretraining on the pool of unlabelled antigen sequences before fine-tuning on the labelled windows. Since placement error up to 25 tokens is forgiven, spend effort on identifying the right region rather than on the last few tokens of precision. One consequence of the test construction is worth exploiting. Test antigens carry at most two annotated windows while the training split retains the densely annotated proteins, which average about 21 annotated windows against 1.19 for test antigens. A random training antigen is therefore far easier to hit by luck than a test antigen. If you build a validation set by sampling training antigens carrying only one or two annotated windows, it will match the test distribution far better than a random sample of training rows, and your local estimate of your own score will be correspondingly more trustworthy. Part 7: What To Use And What Not To Use 7.1 Use Vectorised numpy wherever you touch a full antigen: sliding-window comparisons, and especially cumulative or prefix sums, so token counts inside any candidate window are constant-time lookups instead of being recomputed at every offset. This is how the grader's anchoring stays fast on a 7,000-token antigen, and it is what makes a per-position scorer tractable on CPU. CPU-native libraries for the model: scikit-learn, LightGBM, XGBoost or CatBoost in CPU mode, logistic regression, or gradient boosting all train quickly here. The reference was produced with exactly this kind of model. Small, shallow architectures if you go the deep-learning route: a modest 1D convolutional network, a small GRU or LSTM, or a transformer restricted to local or windowed attention. The vocabulary is only 160 tokens, so a large model buys nothing but slower training. Precomputed per-antigen statistics, calculated once and reused across candidate offsets. Batched feature extraction and inference as array operations rather than Python loops over tokens or offsets. Loop overhead is the most common way this task becomes slow, and it is what makes negative-sampling code blow up on antigens carrying hundreds of annotated epitopes. Use a coverage mask with a cumulative sum to test candidate-window overlap in constant time. Any use of the provided training data, including recovering exact window offsets by substring search. Self-supervised objectives you build yourself, such as masked-token, next-token or contrastive modelling, from the antigen token sequences in train.csv and test.csv. That is still training from scratch on this challenge's own data. Ensembling across training runs. Averaging three members of the same family raised the reference from about 0.080 to about 0.122. 7.2 Avoid Full unwindowed self-attention across entire antigens up to 7,107 tokens. The quadratic cost at that length is the most common CPU trap here; a chunked, local or windowed design avoids it while still capturing local context. Large embedding dimensions or oversized hidden layers. The vocabulary is 160 tokens, so a large embedding table adds training time without useful capacity. GPU-only libraries or kernels. None exist in this environment and code requiring them will fail to run. Recomputing window features with nested Python loops over every candidate offset. Use prefix sums or vectorised arrays. Beam search or ensembling over an unbounded candidate set spanning every position in every antigen. Narrow the candidates with a cheap first pass, then spend heavier compute on the shortlist. Any strategy that ignores antigen content. Fixed-position slices, whole-input dumps, constant outputs and random tokens all report exactly 0.000000, because the chance correction is the expectation of a blind placement and there is no per-row floor to let lucky rows survive the averaging. The only way to score above zero is to read the input. Treating the 25-token tolerance as licence to skip localisation and guess position coarsely. It forgives small offset error on an otherwise content-driven prediction, and it is already priced into the chance baseline, which is computed under the identical tolerant metric. Submitting blanks or unparseable predictions on rows you are unsure about. They contribute an unfloored minus 0.1811 and drag down the rows you did answer. Stripping zero tokens when recovering training window offsets. Padding is appended only at the end of a clipped window and 0 is a legitimate token value elsewhere, so indiscriminate stripping corrupts the probe and silently mislocates windows. Pretrained weights of any kind, including general-purpose language models, protein language models such as ESM or ProtBERT, or any embedding table pretrained outside this challenge. The private cipher means no such checkpoint carries usable signal, and large checkpoints assume GPU-scale compute this environment does not provide. Attempting to reverse-engineer the private token mapping or to identify the underlying proteins. The salt is secret and the transformation is irreversible by design, and this holds regardless of how a request is framed. External datasets, knowledge bases or biological databases used to augment the training data. Sharing or publishing the raw data or derived representations outside the platform. Treating the task as multi-class classification over a fixed set of whole output sequences. The task is to locate and emit a window, not to pick a label from a closed set. All information needed to succeed is inside the training data this challenge provides, and every reference solution used to calibrate it ran on CPU alone. &nbsp;
> Closes in 6m
> 9 / 12 beat AI

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Cell Event Program Recovery from Fluorescence Traces

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx70r1j1j5v4ahkwa1tnrh7rx58e5fnm
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Draft
- Difficulty: Hard
- Compute: CPU
- GPU: CPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> Cell Event Program Recovery from Fluorescence Traces Overview Each row contains a short anonymized sensor log from a real yeast cell experiment. Think of it as a multivariate time series: for each observed cell, you receive one value sequence for brightness, one value sequence for cell size, and a validity mask that says which frames are usable. Your task is to predict the ordered event list hidden in that time series. For each cell, identify whether and when two event types happen: bud_onset, meaning a visible growth event starts, and trace_exit, meaning the tracked cell leaves or ends before the recording finishes. This challenge belongs to the From Scratch domain. Participants may train models on the supplied public training rows, but may not use hosted inference, GPU-only workflows, private files, or external source lookup. Dataset The public data is derived from real cell-cycle microscopy experiments. The raw upload contains microscope image examples, cell-tracking resources, MATLAB analysis files, and per-cell trace files. The challenge input is a prepared trace packet, not the raw images. For each example, open the row's manifest_path. The manifest has this structure: { "id": "Y123EXAMPLE", "frame_count": 120, "cells": [ { "cell_id": "C1A2B3C4D", "fluorescence": [0.13, 0.20, -0.05], "relative_area": [0.98, 1.01, 1.04], "valid": [1, 1, 1] } ] } frame_count is the number of time steps. Each item in cells is one tracked cell. fluorescence is the normalized brightness sequence, relative_area is the normalized size sequence, and valid is a same-length 0/1 mask. cell_id is an anonymized handle that must be reused exactly in predictions for that row. train.csv has id, manifest_path, prompt, and target_json. test.csv has the same input columns without target_json. sample_submission.csv has the required submission header and held-out ID order. Manifest paths are relative to the public output directory. File Overview | Item | Description | |---|---| | train.csv | Training inputs and targets | | test.csv | Held-out inputs | | sample_submission.csv | Submission template | | packets/*/manifest.json | Trace packet | CSV Columns | Column | Type | Description | |---|---|---| | id | string | Row identifier | | manifest_path | string | Manifest path | | prompt | string | Task instruction | | target_json | JSON string | Train target only | Target JSON The target is a JSON object with one key, events. Its value is an ordered list of event objects: { "events": [ {"cell_id": "C1A2B3C4D", "event": "bud_onset", "frame_bin": 37}, {"cell_id": "C1A2B3C4D", "event": "trace_exit", "frame_bin": 91} ] } cell_id must be one of the cell_id values in that row's manifest. event must be bud_onset or trace_exit. frame_bin is an integer time step from 0 to frame_count - 1. Events should be sorted by time when possible. Submission Submit submission.csv with columns in this exact order: id,prediction_json. The id values must exactly match test.csv; extra, missing, or duplicated IDs invalidate the submission. Row order is not important because the grader aligns rows by id. Example: id,prediction_json Y123EXAMPLE,"{""events"":[{""cell_id"":""C1A2B3C4D"",""event"":""bud_onset"",""frame_bin"":37}]}" Y456EXAMPLE,"{""events"":[]}" | Column | Type | Constraint | |---|---|---| | id | string | Exact test ID order | | prediction_json | JSON string | Event-list object | Evaluation The score is the mean row score over all held-out rows. Each row is scored by comparing the predicted JSON object with the hidden target JSON object. For a JSON object, the grader extracts two token sets: | Token set | Meaning | |---|---| | facts | All key/value facts and list members | | order | Adjacent list-member pairs | For each token set, precision is matches / predicted_tokens, recall is matches / target_tokens, and F1 = 2 precision recall / (precision + recall). If both sets are empty, that F1 is 1.0; if only one side is empty, it is 0.0. The row score is: 0.70 F1(facts) + 0.30 F1(order) Metric rationale: this task is event-program recovery, so the grader rewards the structured content of the predicted JSON rather than a single flat label. The facts component gives credit for recovering the correct row-local cell handle, event type, and exact annotated frame_bin values. The curated labels are discrete frame annotations, so a near-miss frame is treated as an incorrect frame-bin fact, while the same prediction can still receive credit for the correct cell_id and event facts. The order component rewards the temporal event sequence, which matters when multiple events are emitted for the same cell or row. The final score is the mean of all row scores. The score range is [0, 1]. A perfect submission scores 1.0. A malformed JSON row, unknown cell_id, oversized JSON object, wrong columns, duplicate IDs, or missing IDs receives zero or is rejected by the grader. Generalization Contract Rows from the same microscope position are kept together in one split, so closely related traces do not appear in both train and test. Public IDs and packet filenames are anonymized. Hidden answers, source paths, original row order, and split-group labels are not included in public test files. Practical CPU Modeling Guidance Official resources: 10 CPU cores, 62 GB RAM, 1.5 hours wall-clock, no GPU. Suitable approaches include time-series feature extraction, change-point detection, compact temporal models, dynamic programming, and cross-cell consistency checks. Keep training and inference offline. What Not To Use hosted inference APIs, runtime downloads, or GPU-only workflows; external source lookup, reverse media search, recovered source filenames, IDs, URLs, or file-size side channels; private-file access, hard-coded hidden answers, grader exploitation, or manual labelling of test rows; malformed or oversized CSV/JSON, duplicate IDs, missing IDs, or impossible row-local handles; reducing the task to a single classification label or continuous regression target instead of emitting the required event-list JSON. &nbsp;
> 3h ago
> $400–$500
> Draft

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

## Cross-Era Map Partial Correspondence

- Challenge URL: https://shipd.ai/quests/eris/challenges/jx7fx3zbc6v19fm77j4n5xygf18ag6xh
- DOMAIN exactly as displayed: From Scratch
- Challenge collection: CPU
- Status: Draft
- Difficulty: Hard
- Compute: A10G/GPU
- GPU: A10G/GPU
- Scoring: Higher is better
- Tags: Not shown/captured
- Best/top context found: Homepage-card-only capture; detail page unavailable.

Full challenge description from page:

> # Cross-Era Map Partial Correspondence Overview Recover a partial one-to-one correspondence between labeled positions on a stylized historical map and anonymized clue tiles from a separately rendered archival-image channel. Only a subset of historical anchors has a candidate counterpart, and many candidate tiles are hard negatives that must be reported as unmatched. Each row supplies one map image, exact normalized positions for row-local historical IDs such as H03, and a set of row-local candidate IDs such as M08. Candidate evidence is visual rather than geometric: the candidate record identifies a tile in clue_sheets.npy, but contains no candidate coordinate, distance signature, global coordinate, source ID, seed match, or target match count. A correct solution must learn cross-domain visual similarity, reject plausible nearby negatives, and decide which anchors have no counterpart. This is a from-scratch multimodal structured-matching task. It is not coordinate registration, latitude/longitude prediction, source retrieval, or map-category classification. Only CPU solutions are allowed. The runtime limit is 1.5 hours on 10 CPU cores with 62 GB RAM. The full clue tensor is uint8 and can be memory-mapped with NumPy. Task For every test row, predict: matches_json: one-to-one {historical_id, modern_id} pairs. unmatched_modern_json: candidate IDs whose clue tiles do not correspond to any historical anchor in that row. confidence: finite row confidence in 0,1]. The map coordinates locate the Hxx anchors. Candidate identity must come from its clue tile. The clue channel is generated independently from the archival scan, while the public map uses a different stylized rendering. Clues vary in crop scale, tone, edge mixture, polarity, mirror/flip, anisotropic affine shear, rotation up to 30 degrees, resampling, and occluder position/shape. Distractors are real same-map patches, mostly sampled near annotated anchors, not artificial noise. Do not assume every historical anchor has a match. anchor_count and candidate_count describe the two input sets; neither reveals how many pairs belong in matches_json. Historical anchors without a counterpart are represented by omission from matches_json. Every candidate omitted from the predicted pairs should appear in unmatched_modern_json. Intended Approach A strong CPU solution can memory-map clue_sheets.npy, extract multi-scale map patches around each Hxx, and learn a compact cross-domain pair scorer from released rows. Useful inputs include gradient-orientation histograms, local keypoint geometry, frequency/texture summaries, and a small Siamese or metric-learning network trained from scratch. Train on both random and near-anchor hard negatives. At inference, augment the pairwise score matrix with dummy/unmatched states or apply a validation-calibrated rejection threshold before partial Hungarian assignment. Use grouped validation by source map or visually related sheet family. Compact CNNs trained only on released rows are allowed. A classical local-feature pipeline remains a useful baseline, but exhaustive pixel correlation plus forced full assignment is intentionally insufficient. Evaluation Higher is better. The theoretical range is exactly [0,1], and a perfect valid submission with confidence 1.0 scores exactly 1.0. For each row: S_match = F1 over exact (historical_id, modern_id) pairs S_unknown = F1 over unmatched candidate IDs core = 0.82 × S_match + 0.18 × S_unknown cal = max(0, 1 - abs(confidence - core)) row_score = 0.95 × core + 0.05 × cal The final score is: Final = 0.85 * mean(row_score) 0.15 * min(mean(row_score) for each hidden geographic region) The hidden geographic groups are physical regions derived from the source map's human GCP geography. The held-out split contains multiple regions and keeps every source map and related map-sheet family wholly in one split. Split Design and Limitations The deterministic split uses 79 source maps from 67 visually related sheet families for 1,027 training rows and holds out 34 source maps from 28 different families for 442 evaluation rows. No source map or related sheet family crosses the split, so repeated editions and visually similar sheets cannot leak from public training data into evaluation. The held-out rows span five physical geographic regions with 143, 26, 26, 195, and 52 rows; the worst-region term therefore measures performance on every region rather than only the largest groups. The corpus is not globally representative. Its five regions are imbalanced, some publishers and historical map styles are more common than others, and 79 public source maps cannot expose every scan condition present in held-out families. The fixed 640-pixel map scale and deterministic transformation ranges model a bounded matching problem rather than every form of real archival degradation. Solvers should group validation by source map or related sheet family and expect performance to vary with typography, cartographic density, aging, and scan quality. Every term is bounded and monotonic. Adding a correct pair, removing an incorrect pair, improving the unmatched set, or moving confidence closer to row correctness cannot lower the score when other predictions are fixed. There is no threshold cap, exponent, hidden cliff, exact-recovery multiplier, or global residual-error penalty. Malformed row-local JSON, repeated local IDs, unknown local IDs, or assigning a candidate as both matched and unmatched gives zero for that row. Wrong or reordered columns, missing/extra/duplicate test IDs, nonnumeric or non-finite confidence, confidence outside [0,1], unreadable CSV, or oversized input raises InvalidSubmissionError. Source and Attribution Anchor locations derive from human-created ground control points in the official Allmaps open-data snapshot. Historical map images come from the official IIIF manifests and image services listed in the approved dataset's SOURCE_MANIFEST.json. Allmaps annotation metadata is CC0 1.0; individual image rights comprise 109 Public Domain Mark 1.0 records, three CC BY 4.0 records, and one CC BY 3.0 record. Cite Allmaps and the corresponding IIIF providers/manifests when discussing or redistributing derived artifacts. Allmaps project: [https://allmaps.org/ Official Allmaps open-data file: https://files.allmaps.org/maps.ndjson Public Files | Item | Description | |---|---| | train.csv | Labeled training rows | | test.csv | Hidden-label test inputs | | images/*.jpg | Opaque processed maps | | clue_sheets.npy | Candidate tile tensor | | sample_submission.csv | Weak valid baseline | clue_sheets.npy is a uint8 array with shape [N,464,384]. Each sheet has four tile columns and four padded tile rows. A tile at zero-based tile_index is extracted as: column = tile_index % 4 row = tile_index // 4 tile = sheets[index, row116:row116+96, column96:column96+96] The remaining 20 pixels in each tile row display the matching Mxx label. clue_sheet_index selects the first tensor dimension. Unused padded tiles are not listed in candidate_clues_json. train.csv Columns | Column | Type | Description | |---|---|---| | id | string | Opaque row ID | | map_image | path | Processed map image | | clue_sheet_index | int | Tensor row index | | historical_anchors_json | JSON | Hxx and normalized xy | | candidate_clues_json | JSON | Mxx and tile index | | anchor_count | int | Historical anchors | | candidate_count | int | Candidate clue tiles | | matches_json | JSON | Target partial one-to-one pairs | | unmatched_modern_json | JSON | All target candidate IDs without a counterpart | test.csv Columns | Column | Type | Description | |---|---|---| | id | string | Opaque row ID | | map_image | path | Processed map image | | clue_sheet_index | int | Tensor row index | | historical_anchors_json | JSON | Hxx and normalized xy | | candidate_clues_json | JSON | Mxx and tile index | | anchor_count | int | Historical anchors | | candidate_count | int | Candidate clue tiles | Submission Write ./working/submission.csv with exactly these columns in this order and one row for every test ID. | Column | Type | Constraint | |---|---|---| | id | string | Exact test ID | | matches_json | JSON | Unique H/M pairs | | unmatched_modern_json | JSON | Unique candidate IDs | | confidence | float | Finite [0,1] | Example: id,matches_json,unmatched_modern_json,confidence hmapv_0123456789abcd,"[{""historical_id"":""H00"",""modern_id"":""M04""}]","[""M07""]",0.61 matches_json must be a JSON list of objects with exactly historical_id and modern_id. IDs are row-local; do not invent IDs outside that row. A modern ID cannot appear in more than one pair or in both prediction fields. What Not To Use / What Not To Do Do not use reverse image search, public Allmaps annotation lookup, IIIF URL lookup, map-title lookup, source-image retrieval, or an external gazetteer for hidden rows. Do not use original filenames, source IDs, collection IDs, raw URLs, hashes, file sizes, mtimes, row order, or ID decoding as answer channels. Do not use hosted vision, OCR, geocoding, map-matching, or closed-source teacher APIs. Do not use GPU training; stay within the CPU contract. Do not inspect private files, hidden answers, grader internals, filesystem side channels, or platform state. Do not exploit malformed JSON, duplicate IDs, extra columns, non-finite values, or resource-exhaustion payloads. Submissions can be reviewed for prohibited lookup, network use, hidden-file access, metadata-only behavior, and approaches that avoid the visual correspondence contract. A prohibited solution may be rejected before payout even if its CSV is structurally valid. Platform Configuration Difficulty: Hard Compute tier: CPU Tags: image, feature-engineering, multimodal, large-scale Grade direction: Maximize Minimum score: 0.0 Maximum score: 1.0 &nbsp;
> 1h ago
> $400–$500
> Draft

Inspiration note: Useful because it requires task-specific representations without relying on pretrained model shortcuts.

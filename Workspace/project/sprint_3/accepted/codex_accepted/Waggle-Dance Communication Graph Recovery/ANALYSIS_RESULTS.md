# Analysis Results

Rows: train=414, test=339

## Scores

- perfect: 1.000000000000
- sample: 0.122632237663
- empty_no_track: 0.001840913609
- train_graph_prior: 0.122632237663
- metadata_only: 0.082239810063
- spam_everything_no_track: 0.128992013128
- simple_trajectory_heuristic: 0.130554055593
- row_malformed_json: 0.995832401897
- invalid_missing_column: InvalidSubmissionError

## Subgroup Counts

- crowding_level: {'medium': 275, 'low': 43, 'high': 21}
- tracking_confidence_level: {'high': 174, 'medium': 113, 'low': 52}
- duration_bucket: {'medium': 129, 'long': 124, 'short': 86}
- waggle_count_bucket: {'moderate': 127, 'many': 122, 'few': 90}
- comb_side: {'side_a': 269, 'side_b': 70}
- date_group: {'session_b553db': 215, 'session_364748': 124}

## Worst Subgroup Scores

- sample: {'crowding_level': 0.10279269839729895, 'tracking_confidence_level': 0.11211294254928914, 'duration_bucket': 0.12020941677191739, 'waggle_count_bucket': 0.0927983105509029, 'comb_side': 0.1105114429901764, 'date_group': 0.11817200178380237}
- simple_trajectory_heuristic: {'crowding_level': 0.12301790607969754, 'tracking_confidence_level': 0.12300845273220666, 'duration_bucket': 0.12615703522545024, 'waggle_count_bucket': 0.1129540081153058, 'comb_side': 0.1217095852627506, 'date_group': 0.12556562776935679}

## Source Reversibility Scan

- PASS: no raw source ids, timestamps, dates, filenames, or object/string NPZ fields found in public prepared files.

## Shortcut And Reverse-Engineering Audit

- Metadata nearest-label-copy score: 0.128684566158
- File-size nearest-label-copy score: 0.132319095494
- File-size summary: {'test_bytes_min_median_max': [33474, 145181, 222636], 'strongest_abs_hidden_target_correlation': 0.41981181446903615}
- Public ID checks: {'all_match_pattern': True, 'unique_across_train_test': True, 'lexicographic_train_fraction_first_100': 0.52, 'lexicographic_train_fraction_last_100': 0.63}
- Raw coordinate overlap probe: {'status': 'measured', 'public_pairs_checked': 12000, 'sampled_raw_pairs': 324312, 'exact_round2_hits': 0, 'hit_rate': 0.0}
- Strict submission checks:
  - sample: 0.122632237663
  - shuffled_rows: 0.122632237663
  - wrong_order: InvalidSubmissionError
  - extra_column: InvalidSubmissionError
  - missing_column: InvalidSubmissionError
  - missing_row: InvalidSubmissionError
  - extra_row: InvalidSubmissionError
  - nan_confidence: InvalidSubmissionError
  - inf_confidence: InvalidSubmissionError
  - out_of_range_confidence: InvalidSubmissionError
  - duplicate_id: InvalidSubmissionError
  - one_bad_json: 0.122031496816
  - one_overlong_json: 0.122031496816
  - one_invalid_dancer: 0.122031496816
  - one_invalid_interval: 0.122031496816
  - one_duplicate_role: 0.122031496816
  - one_self_edge: 0.122031496816

## CPU Timing

- Heuristic rows: 339
- Heuristic seconds: 21.358
- Seconds per 1000 rows: 63.004
- Estimate: Feature extraction plus a compact CPU model should fit well under 1.5 hours for this prepared split.

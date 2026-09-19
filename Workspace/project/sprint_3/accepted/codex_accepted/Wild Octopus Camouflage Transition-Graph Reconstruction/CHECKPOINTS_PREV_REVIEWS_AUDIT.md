# Checkpoint and previous-review audit

The current live rules and `rules/prev_reviews.txt` were read before the MEVA pivot. The recurring accepted-challenge requirements are covered as follows:

- strict exact submission columns/order, duplicate-ID and row-set rejection: `grade.py::_validate_frames`;
- malformed row-local JSON scores zero without collapsing the submission: `grade.py::_parse_graph` and `_sanity_smoke.py`;
- canonical JSON with duplicate-key, vocabulary, range, ordering, and node/edge-cap checks: `grade.py`;
- one global salted opaque-ID function, sorted CSVs, no source names/timestamps/groups in public files: `prepare.py`;
- strongest available session grouping and a minimum held-out-group count: `prepare.py` source contract;
- raw upload below 1 GB, flat official-only archive, and CC BY 4.0 rights: `SOURCE_VERIFICATION.md`, `DATA_ACQUISITION.md`;
- participant description tables, intended CPU approaches, What Not To Use, enforcement, evaluation, and sample format: `CHALLENGE_FORM_FILL.md`;
- data dictionary with complete official field descriptions and license/source: `DATASET_FORM_FILL.md`;
- retrieval/metadata shortcut probes and train-prior baselines: `_analyze.py`;
- deterministic oracle/sample/invalid-submission tests: `_sanity_smoke.py`.

The stale octopus source-gate notes were replaced where they conflicted with the actual MEVA files. The fixed output-folder name is retained solely because it was required by the user; no participant-facing document claims that the corpus contains octopus footage.

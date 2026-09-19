# Mechanical-audit exceptions

`challenge_audit.py` is a useful first-pass checker, but it assumes every raw archive has a CSV and that every challenge uses numeric-confidence fields. The only reported failure is therefore a false positive:

- `OFFICIAL_RAW_FILES_ONLY.zip includes csv data`: MEVA is a real-data YAML/AVI corpus. Its official annotations are YAML; adding a generated CSV would violate the untouched-raw rule. The archive contains 21 official AVI videos, 42 official YAML files, seven official documentation files, and the CC BY 4.0 LICENSE.

Non-blocking warnings have the same explanation or are covered by stronger runtime checks:

- The salted SHA-256 `_public_id` function is the deliberate split-safe opaque-ID map; collision and source-video hash uniqueness are asserted in `prepare.py`.
- YAML packets are validated for required fields, spans, labels, actor/type linkage, and non-empty content; a CSV NaN check is not applicable.
- The graph submission has no confidence field, so finite-confidence validation is not applicable.
- The organizer output root is `prepared/public` and `prepared/private`, not a `pub/public` tree.
- Sparse subgroup-repair warnings are not applicable because no sparse-label repair is performed; the five held-out session groups are checked directly with a 30-row minimum.
- The dataset-form CSV/media warnings reflect the legitimate non-tabular raw format and official AVI media.

Independent runtime checks in `_sanity_smoke.py` and `_analyze.py` pass: 479 train / 175 test, oracle 1.0, sample 0.144708, 654 CRF-12 MP4s totaling 460,026,529 bytes, opaque IDs, and no source tokens. The raw-frame retrieval probe found no near-exact matches.

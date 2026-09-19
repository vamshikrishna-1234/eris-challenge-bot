# Live-rule requirement matrix (MEVA pivot)

| Requirement | Status | Evidence |
|---|---|---|
| Source and license | pass | `SOURCE_VERIFICATION.md`, archived CC BY 4.0 LICENSE |
| Raw files only | pass | 70-member untouched archive; no prepared assets |
| Real-world ML value | pass | video activity graph reconstruction |
| Grouped split | pass | 15 session groups frozen in `prepare.py` |
| Scale | pass | 479 train / 175 test after prepare |
| CPU feasibility | pass | 32-frame clips; MobileNet/GRU reference |
| Strict columns and IDs | pass | `_validate_frames` in `grade.py` |
| Row-local malformed JSON | pass | `_parse_graph` returns zero row score |
| Perfect score | pass | `_sanity_smoke.py` asserts 1.0 |
| Sample headroom | pass | smoke: sample 0.127315, oracle 1.0 |
| Lookup stress | pass | no source tokens; prior probe min Hamming 65 and near-exact 0 |
| Public metadata isolation | pass | opaque IDs; source fields stripped |
| Required forms/paste files | pass | forms and byte-identical paste files |

The earlier wild-octopus gate failure is preserved in the historical audit files but is not a claim about this pivoted challenge.

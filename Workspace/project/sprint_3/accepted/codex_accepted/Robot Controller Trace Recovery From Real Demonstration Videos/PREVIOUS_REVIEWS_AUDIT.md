# Previous Reviews Audit

This file maps the repeated lessons in `rules/prev_reviews.txt` to the current challenge state.

## Source, License, And Raw Upload

[p] Real-data gate: source is an official Zenodo robotics dataset, not synthetic. `SOURCE_VERIFICATION.md` records title, version, files, sizes, MD5s, license, direct URL, contents, and the missing-gripper caveat.

[p] License gate: `CC BY 4.0` allows redistribution, reuse, adaptation, and commercial use with attribution. This is stated in both source and dataset docs.

[p] Raw upload cleanliness: preferred upload is direct official URL import for `PandaHandover_Real_Val.zip`. Manual fallback uploads only the unmodified official ZIP, not prepared splits or derived labels.

[p] Dataset form discipline: `DATASET_FORM_FILL.md` describes only the raw official archive, file layout, trajectory columns, license, source, and notes. It does not mention grading, splits, scoring, hidden answers, or challenge mechanics.

## Participant-Facing Description

[p] Tables: `CHALLENGE_FORM_FILL.md` has real markdown tables for file overview, train columns, test columns, and submission format.

[p] Source-neutrality: the visible challenge description does not name Zenodo, the exact source archive, source checksums, raw filenames, or raw IDs.

[p] What Not To Use: source lookup, metadata-only solutions, rule-only templates, external hosted APIs, hidden-answer leakage, and continuous-regression-only reductions are prohibited inside the platform-visible Overview and in the separate form field.

[p] Prep-detail leakage: the visible problem statement avoids exact preprocessing transforms, derivation thresholds, split construction details, source file IDs, source checksums, and raw archive names.

[p] Submission clarity: the prompt gives exact `./working/submission.csv` path, exact column order, JSON object schemas, allowed enum values, confidence range, and parseable CSV examples.

[p] No rubric clutter: no rubric section, no grading YAML block, and no "What makes this challenging" section.

## Split, Leakage, And Shortcuts

[p] Split leakage: `prepare.py` keeps all six source files for one motion sample in the same split, uses salted opaque hash-token public IDs, sorts outputs by ID, strips raw IDs, and checks hash uniqueness before ID mapping.

[p] File/path leakage: public video names are derived from opaque IDs and not raw filenames. `_analyze.py` checks for raw-id-like text, forbidden source columns, overlapping public paths, duplicate IDs, and exact public state overlap across train/test.

[p] File length shortcut: prepared public clips are normalized to a fixed frame count and padded to a fixed byte size. `_analyze.py` runs duration-only and state-exact transfer baselines.

[p] Public-media lookup: the CREMA-D-style lesson is relevant here because exact public video clips could otherwise be matched back to a named upstream corpus. Mitigations are source-neutral prose, transformed/re-encoded/noised/compressed public clips, fixed-size public video files, coarse binned public state instead of raw values, opaque hash-token IDs, no raw filenames/IDs, fixed frame count, explicit no-lookup enforcement, and `_source_lookup_probe.py` for a full public/raw video retrieval audit.

## Grader And Baselines

[p] Strict structural validation: `grade.py` enforces exact columns/order, duplicate-ID rejection, answer duplicate rejection, row-set equality, finite confidence, confidence range, JSON length caps, row-local schema/range checks, CSV byte-size cap, NUL-byte rejection, and unsupported-control-character rejection.

[p] Row-local malformed JSON: malformed JSON or invalid row-local object schemas return zero for that entire row rather than crashing or collapsing the whole submission.

[p] Perfect and sample behavior: `_sanity_smoke.py` verifies perfect score is exactly `1.0` and sample is non-degenerate but weak, about `0.136` on the smoke fixture.

[p] No validity-only inflation: score is based on segment, waypoint, event, and calibration credit; there are no automatic validity points for merely well-formed JSON.

[p] No inner-merge exploit: grader compares exact ID sets and lengths before scoring, so missing rows, extra rows, and duplicate rows score `0.0`.

## Prepare Entrypoint And Determinism

[p] Platform entrypoint: `prepare.py` exposes `prepare(raw: Path, public: Path, private: Path) -> None` and keeps `main()` only as a CLI wrapper.

[p] Deterministic outputs: split, public ID mapping, video transforms, sample baseline, and label derivation are deterministic.

[p] Missing data/schema checks: trajectory pickles must be Pandas DataFrames with exact expected joint/Cartesian columns and no NaN values. Public train/test/private CSVs are checked for missing values before writing.

## Remaining Review Risks

[w] Real-source media retrieval remains the main residual risk. The challenge now includes `_source_lookup_probe.py`; run it after materializing the full official raw archive and prepared split, and harden or pivot if rank-1/rank-5 recovery exceeds the configured thresholds.

[w] The source has no explicit gripper state. The challenge intentionally avoids true gripper-open/close targets and documents this in `SOURCE_VERIFICATION.md` and the visible Dataset section.

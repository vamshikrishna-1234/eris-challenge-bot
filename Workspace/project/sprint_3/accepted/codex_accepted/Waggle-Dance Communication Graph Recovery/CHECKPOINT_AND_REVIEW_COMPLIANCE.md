# Checkpoint and Review Compliance

Checked on 2026-07-19 IST after building the clean raw source package and preparing the real split.

## Final Build State

* Raw source ZIP: `waggle_dance_raw_subset.zip`
* Raw source ZIP size: 738,696,915 bytes, about 738.7 MB decimal.
* Raw source ZIP SHA-256: `39D881C8BBCD2B8558539D31A604F8541125A83933CAA6CF42B94F36F07A1C30`
* Prepared rows: 414 train, 339 test.
* Prepared public/private size: about 163.0 MB.
* Public prepared data remains under 500 MB. It is smaller than the nominal 250-400 MB target because the real trajectory NPZ files compress well even with the added dense tensors; no artificial padding was added.

## Required Checks

| Check | Status | Evidence |
|---|---|---|
| Real source/license verified | PASS | `SOURCE_VERIFICATION.md` |
| Novelty gate before build | PASS | `SOURCE_VERIFICATION.md` |
| CPU-only design | PASS | `CHALLENGE_FORM_FILL.md` |
| Raw data not synthetic | PASS | official Zenodo files only |
| Clean raw subset justified | PASS | track ZIP members are date CSVs |
| Raw package under 1 GB | PASS | 738.7 MB ZIP |
| No pre-baked splits in raw | PASS | source ZIP excludes public/private |
| Prepare deterministic | PASS | `_sanity_smoke.py` |
| Split by date and dancer | PASS | `prepare.py` |
| Public source IDs stripped | PASS | `_analyze.py` source scan, `EXPLOIT_REVERSE_ENGINEERING_AUDIT.md`, and `TRAJECTORY_SOURCE_LOOKUP_AUDIT.md` |
| Public NPZ finite/no object arrays | PASS | focused Caspian audit checked every public NPZ |
| MIN_GROUP_TEST guard | PASS | `prepare.py` and real split |
| Perfect score exactly 1 | PASS | `grade.py` check: 0.9999999999999998 |
| Sample weak and valid | PASS | train-prior sample score 0.12263223766283594 |
| Invalid structural handling | PASS | invalid missing column raises `InvalidSubmissionError` |
| Malformed/invalid row JSON degrades | PASS | `_sanity_smoke.py`, `_analyze.py`; impossible local dancer id now zeroes the affected row |
| Metadata-only weak | PASS | 0.08223981006320294 |
| Train graph prior weak | PASS | 0.12263223766283594 |
| Spam-everything no-track weak | PASS | 0.12899201312837794 |
| Simple trajectory baseline weak | PASS | 0.13055405559277142 |
| Exact/rounded/source feature overlap checked | PASS | `_analyze.py` reports no findings; raw-coordinate overlap probe found `0/12000` exact rounded hits |
| Trajectory source-fingerprint checked | PASS | rank-1 raw candidate recovery reduced from `40/40` to `1/40`; median rank `65.5` |
| File-size shortcut checked | PASS | metadata plus file-size nearest-label copy scores `0.132319`, near weak heuristic and far below perfect |
| Grade exploit/spam templates checked | PASS | `GRADE_EXPLOIT_AUDIT.md`; tracked spam baseline `0.128992` |
| Subgroups populated | PASS | `_analyze.py` |
| Paste files synced | PASS | challenge audit |

## Audit Result

Command:

```powershell
python "C:\Users\vamsh\.codex\skills\challenge-builder\scripts\challenge_audit.py" --challenge "D:\create_challenge_synthetic_output_folder\sprint_3\codex_output_folders_sprint_3\Waggle-Dance Communication Graph Recovery"
```

Result: `failures=0 warnings=11`.

Non-blocking warnings:

* Dataset file structure mentions CSV assets: expected for a real tabular/trajectory source package.
* Dataset form has non-empty features/columns: expected and required as a data dictionary.
* Static split-ID/hash/raw-NaN warnings: `prepare.py` uses salted SHA-256 public IDs, duplicate-ID checks, required-column checks, numeric coercion/drop checks, and real smoke/analyze validation; the audit script did not recognize every custom pattern.
* Static grader column warnings: `grade.py` enforces exact ordered columns and raises `InvalidSubmissionError` on structural invalidity; verified by smoke/analyze.
* Raw ZIP media warning: the ZIP contains CSV trajectory files, not media; the generic audit label is conservative.
* Challenge description mentions `sample_submission.csv`: required participant-facing file overview.
* No image/video/audio path column warnings: expected, because the public artifacts are trajectory NPZ files referenced by `episode_npz`.

## Remaining Changes

No blocking changes remain before submission. The only notable residual note is that the prepared split is about 163.0 MB rather than 250-400 MB because compressed real trajectory tensors are storage-efficient; it remains below the 500 MB cap and should not be padded artificially.

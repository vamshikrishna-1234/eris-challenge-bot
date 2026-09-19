# Checkpoints And Previous Reviews Recheck

Challenge: Urban Noise Source-Mix And Enforcement Priority Profiling

Recheck date: 2026-07-16

## Commands Run

```text
python _sanity_smoke.py
python _analyze.py
python C:\Users\vamsh\.codex\skills\challenge-builder\scripts\challenge_audit.py --challenge "D:\create_challenge_synthetic_output_folder\sprint_3\codex_output_folders_sprint_3\Urban Noise Source-Mix And Enforcement Priority Profiling" --root "D:\create_challenge_synthetic_output_folder\sprint_3\codex_output_folders_sprint_3"
```

Additional checks:

* Inspected `sonyc_ust_official_selected_source_files.zip` members.
* Ran a pitch-free time-envelope fingerprint probe comparing all 1,000 prepared public WAVs against all 1,000 official raw WAVs in `audio-0.tar.gz`.
* Read `C:\Users\vamsh\Downloads\create_challenge_synthetic\rules\checkpoints` line by line.
* Read `C:\Users\vamsh\Downloads\create_challenge_synthetic\rules\prev_reviews.txt`, all 2,641 lines.

## Current Mechanical Results

| Check | Result |
|---|---:|
| `raw_data` directory exists | false |
| Upload zip members | 4 |
| Upload zip contains public/private | false |
| Upload zip contains prepared CSVs | false |
| Train rows | 701 |
| Test rows | 299 |
| Public prepared bytes | 288,331,032 |
| Sample score | 0.1433879071797786 |
| Perfect score | 1.0 |
| Malformed all-core score | 0.0 |
| Train-prior baseline | 0.3247976184598513 |
| Duration-only baseline | 0.32479826817274976 |
| ID-hash metadata-only baseline | 0.2924186824467303 |
| Simple audio feature baseline | 0.40405913002734317 |
| Challenge audit failures | 0 |

Upload zip members:

```text
annotations.csv
dcase-ust-taxonomy.yaml
README.md
audio-0.tar.gz
```

## Public Audio Source-Reversibility Probe

The ordinary metadata probes pass: no raw filenames, source-like paths, source metadata columns, split labels, sensor ids, annotator ids, or variable durations are exposed.

However, a stronger public-audio fingerprint probe fails. I compared each prepared public WAV to every official raw WAV using only a pitch-free time-envelope representation and allowed the 9-second prepared clip to align to any 9-second window inside the 10-second raw clip.

| Probe | Result |
|---|---:|
| Public clips compared | 1,000 |
| Raw shifted candidates | 11,000 |
| Top-1 raw clip recovery | 993 / 1,000 |
| Top-1 recovery rate | 0.993 |
| Top-5 recovery rate | 1.0 |
| Median true rank | 1 |

This means the current prepared public audio is practically reversible to the official source clip despite salted ids, renamed paths, fixed duration, and non-exact byte hashes. Because the official annotations are public, this is a hard source-lookup risk under the latest previous-review standard for public real-audio challenges.

## Checkpoints File Line-By-Line

| Line | Checkpoint | Status | Evidence |
|---:|---|---|---|
| 1 | `check for :` | n/a | Header. |
| 2 | Data Leakage | fail | Metadata leakage is closed, but audio-source reversibility is not: envelope probe recovers 99.3% of raw clips at rank 1. |
| 3 | Baseline score is not too high | pass | Sample 0.1434; train prior 0.3248; simple audio feature 0.4041; perfect 1.0. |
| 4 | Class distribution is fine | pass | Hidden test minima: priority 29, nuisance 8, source family 13, pressure 62, complexity 23. |
| 5 | No missing data anywhere | pass | Smoke test passes and prepared train/test/sample/answers have no NaN. |
| 6 | What not to use section present | pass | Present inline and in final `## What Not To Use`. |
| 7 | Source reversibility checked | fail | Checked with metadata, exact hash/name/size, and time-envelope audio matching; the time-envelope probe recovers raw clips. |
| 8 | Novelty checked before build | fail | Nearest benchmark documented, but local novelty is estimated 5/10 and the current user constraint requires 6+. Prior SONYC challenge was rejected. |
| 9 | blank line | n/a | Separator. |
| 10 | `checkpoints from Caspian:` | n/a | Header. |
| 11 | status legend | n/a | Legend. |
| 12 | dataset and audio/text quality header | n/a | Header. |
| 13 | source and licensing | pass | Official Zenodo/README license is CC BY 4.0; SOURCE_VERIFICATION documents version, URLs, sizes, and MD5s. |
| 14 | raw assets only | pass | Single upload zip contains only unchanged official source files and no train/test/answers/prepared clips. |
| 15 | speech/text domain fit | n/a | Environmental audio, not ASR/TTS/code-switching/text. |
| 16 | synthetic sanity check | n/a | Real-data challenge. |
| 17 | challenge design and evaluation header | n/a | Header. |
| 18 | novelty | fail | Source/task remains SONYC-derived and documented novelty is 5/10, below the new 6+ constraint. |
| 19 | real-world ML value | pass | Urban source-mix and enforcement-priority profiling is meaningful monitoring work. |
| 20 | fair split and OOD testing | pass | Grouped split; no train/test id overlap; hidden group minima guarded. |
| 21 | metric and headroom | pass | Baselines leave >30 points to perfect; simple audio baseline beats metadata/prior. |
| 22 | robust grader header | n/a | Header. |
| 23 | input validation | pass | Grader rejects wrong/reordered columns, duplicate ids, row-set mismatch, NaN/inf/out-of-range confidence, oversized strings. |
| 24 | no internal leaks | pass | Structural error messages expose schema/validity only, not labels, split logic, or answer keys. |
| 25 | agent-code safeguards | n/a | No solver pipeline is shipped. |
| 26 | leakage and shortcuts header | n/a | Header. |
| 27 | feature isolation | fail | Public CSV features are isolated, but public audio itself is source-reversible by time-envelope matching. |
| 28 | no rule leaks | pass | Participant prose does not expose source filenames, split construction, salt, exact transforms, or target derivation rules. |
| 29 | anti-regex/anti-lookup | fail | Regex/metadata lookup is blocked, but source-audio lookup is feasible at 99.3% top-1 against public raw audio. |

## Previous Reviews Full-Line Coverage

I read all 2,641 lines of `prev_reviews.txt`. The line ranges below cover the file and call out transferable lessons that materially affect this challenge.

| Lines | Review lesson family | Status for this challenge |
|---:|---|---|
| 1-38 | Metadata/prefix lookup, parseable public features, baseline headroom. | pass for CSV metadata; fail for public-audio source lookup. |
| 39-131 | Dataset validator layout, strict merge/id checks, max/min score consistency. | pass: exact id set, duplicate rejection, min 0/max 1, sample >0.12. |
| 132-226 | Prompt formatting, hidden rule/noise leakage, What Not To Use inside visible description. | pass: What Not To Use is visible; exact transforms not disclosed. |
| 227-450 | Prepare determinism, id shuffling/salting, path correctness, JSON guards, sample floor. | pass: salted ids, sorted outputs, paths exist, JSON capped, sample 0.1434. |
| 451-873 | Novelty framing and forward/orthogonal target lessons. | warn/fail: target is more than plain tags, but source family remains close to SONYC. |
| 874-1308 | Borderline novelty, source fields/schema names, tables/prose definitions, malformed JSON behavior. | mostly pass; novelty remains below current 6+ threshold. |
| 1309-1435 | Positive-review targets: grouped split, strict grader, no raw masks/leak fields, accepted cleanup. | pass except public-audio source reversibility. |
| 1436-1560 | Agent saturation/headroom, CPU neural baselines, metric reweighting. | pass: weak baselines and CPU-compatible public size. |
| 1561-1650 | Public-audio fingerprinting and SONYC rejection lessons. | fail: line 1632 rejects the earlier SONYC tag task; line 1649 requires source-fingerprint stress tests. This challenge fails the stronger envelope probe. |
| 1651-1738 | Structural vs row-local malformed behavior and explicit validation. | pass: structural errors reject; row-local malformed values score 0 for affected heads. |
| 1739-2069 | Real-data pivot, source/URL import filenames, problem quality, dataset form data dictionary. | pass: official-source zip documented; dataset form avoids grading prose. |
| 2070-2326 | Baseline strictness, calibration-only credit, novelty prompt/schema scan. | pass for calibration/malformed; fail/warn for novelty. |
| 2327-2460 | Single visible description block, accepted CV/audio description expectations, compute constraints. | mostly pass; CPU limit now explicit. Submission is still not a top-level sibling heading, so this is a minor formatting warning. |
| 2461-2562 | CLI/prepare callable, archive extraction layout, novelty displayed score must reach threshold. | pass for `prepare(raw, public, private)` and zip/extracted layouts; fail for novelty because documented estimate is 5/10 and user requires 6+. |
| 2563-2597 | Public real-audio source lookup standard: pitch-free envelope, duration, hash, source-label transfer. | fail: pitch-free envelope top-1 recovery is 99.3%, far above accepted-style thresholds. |
| 2598-2641 | Disabled classification/novelty wording, complete problem description, weak fixed baselines. | pass on anti-classification wording and baseline strength; novelty remains unresolved. |

## Verdict

Not all lines pass.

Hard blockers before submission:

1. Source reversibility / anti-lookup fails under the latest public-audio standard. Prepared public WAVs can be mapped back to official raw files with 99.3% top-1 recovery using a simple time-envelope probe.
2. Novelty is below the new hard target. The current source verification says 5/10, and previous reviews explicitly rejected the plain SONYC sibling challenge. The new user constraint requires 6+.

Mechanical items that do pass:

* Source/license verification.
* Raw upload zip contents.
* CPU-only wording.
* Strict grader validation.
* Public CSV metadata stripping.
* Grouped split/id uniqueness/sample/perfect checks.
* Baseline headroom.

Recommendation: do not submit this version as-is if the platform enforces the latest public-audio lookup standard or the 6+ novelty gate. A viable fix needs a substantive redesign, not only wording: either use a non-public/less lookupable source, create many-to-one transformed composites with labels that cannot be read from a single upstream clip, or pivot away from SONYC source-family labels to a genuinely different target.

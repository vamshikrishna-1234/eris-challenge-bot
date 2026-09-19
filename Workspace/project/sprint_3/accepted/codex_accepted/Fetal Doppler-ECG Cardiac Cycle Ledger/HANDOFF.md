# Handoff - Fetal Doppler-ECG Cardiac Cycle Ledger

## Files Created

```text
CHALLENGE_FORM_FILL.md
DATASET_FORM_FILL.md
SOURCE_VERIFICATION.md
HANDOFF.md
generate.py
prepare.py
grade.py
PASTE_THIS_PREPARE.txt
PASTE_THIS_GRADE.txt
zip_raw_for_upload.py
_sanity_smoke.py
_analyze.py
```

## Source And Import

Use official NInFEA v1.0.0 on PhysioNet:

```text
https://physionet.org/content/ninfea/1.0.0/
https://physionet.org/files/ninfea/1.0.0/
https://physionet.org/content/ninfea/get-zip/1.0.0/
```

Preferred platform import: direct import of the official ZIP URL `https://physionet.org/content/ninfea/get-zip/1.0.0/`. The directory-index URL `https://physionet.org/files/ninfea/1.0.0/` can import only a ~1 KB HTML `downloaded-file` on platforms without recursive index import.

Fallback: download official files unchanged with PhysioNet's `wget` or unsigned S3 command and upload the unchanged tree, or run `zip_raw_for_upload.py` to make a clean official-source ZIP. Do not upload a prepared raw ZIP or generated train/test split.

Source gate: PASS. PhysioNet lists NInFEA as open access, ODC-By v1.0, 2.0 GB uncompressed, 792.9 MB ZIP. Required files are `pwd_images/*.bmp`, `wfdb_format_ecg_and_respiration/*.hea`, `wfdb_format_ecg_and_respiration/*.dat`, `RECORDS`, `LICENSE.txt`, and `SHA256SUMS.txt`.

## Challenge Design

The challenge is framed as a structured clinical evidence ledger:

* multimodal input and target construction: Doppler strip image plus ECG/electrophysiology and maternal respiration signal snippet, with cycle quality based on cross-modal agreement;
* strict metric behavior: envelope/quality/count credit is event-gated, and confidence cannot create standalone score on wrong rows;
* structured output: cycle event ledger, Doppler envelope array, quality flags, calibrated row confidence;
* CPU-only: 10 CPU cores, 62 GB RAM, 1.5 hour solver budget;
* split-leak controls: record-group split, salted opaque ids, de-identified fixed-dimension BMP/fixed-shape NPY public assets, no public source filenames, no exact source times, no subject/session ids.

## Tests Run

```text
python -m py_compile grade.py prepare.py _sanity_smoke.py _analyze.py
python _sanity_smoke.py
python _analyze.py <temporary_public> <temporary_private>
python C:\Users\vamsh\.codex\skills\challenge-builder\scripts\challenge_audit.py --challenge "D:\create_challenge_synthetic_output_folder\sprint_3\codex_output_folders_sprint_3\Fetal Doppler-ECG Cardiac Cycle Ledger" --root "D:\create_challenge_synthetic_output_folder\sprint_3\codex_output_folders_sprint_3"
```

Smoke results on a synthetic official-shaped fixture:

```json
{
  "train_rows": 90,
  "test_rows": 18,
  "perfect_score": 1.0,
  "sample_score": 0.2904260934864993,
  "malformed_score": 0.9444444444444445
}
```

Baseline sweep on the same fixture:

```json
{
  "sample": 0.2904260934864993,
  "train_prior": 0.33845757725945735,
  "metadata_only": 0.3338379616791957,
  "empty_valid": 0.0,
  "neutral_envelope_wrong_events": 0.10547138796244468,
  "best_fixed_periodic": {
    "score": 0.3857003671690051,
    "count": 15,
    "phase": 0.5
  },
  "perfect": 1.0,
  "structural_scores": {
    "wrong_columns": 0.0,
    "duplicate_ids": 0.0,
    "one_malformed_row": 0.9444444444444445
  },
  "source_leak_scan": {
    "train": {"leaky_columns": [], "source_value_columns": []},
    "test": {"leaky_columns": [], "source_value_columns": []}
  },
  "id_leak_scan": {
    "overlap_count": 0,
    "boundary_leak": false
  },
  "artifact_size_scan": {
    "image_unique_sizes": 1,
    "signal_unique_sizes": 1
  }
}
```

Audit result:

```text
SUMMARY failures=0 warnings=3
```

Remaining audit warnings:

* `.cursor/rules/challenge-creation.mdc exists`: audit root-shape warning from running outside the main workspace rule tree; not a challenge-content issue.
* `no upload zip found in challenge folder`: intentional; preferred upload is direct official PhysioNet ZIP URL import, not a preprocessed raw ZIP.
* `pub/public directory not found`: intentional; only temporary smoke public/private outputs were materialized, and no preprocessed prepared split is shipped as an official artifact.

## Remaining Risks

* The full official NInFEA corpus was not downloaded locally in this handoff, so the smoke fixture validates mechanics but not full-corpus row counts or full-corpus baseline values.
* Public source matching is impossible to eliminate completely because NInFEA is public. The design avoids making source recovery reveal a separate official answer table, strips public raw ids/times, and explicitly prohibits source-row lookup.
* The novelty score depends on visible framing. Keep the title and opening focused on "cardiac cycle evidence ledger"; avoid rewriting it as fetal heart-rate estimation or Doppler envelope detection.

## Review Status

Ready for user review and platform source-import testing. Not yet final-submission-ready until `prepare.py` is run once against the official PhysioNet import tree and `_analyze.py` is rerun on the resulting full prepared split.

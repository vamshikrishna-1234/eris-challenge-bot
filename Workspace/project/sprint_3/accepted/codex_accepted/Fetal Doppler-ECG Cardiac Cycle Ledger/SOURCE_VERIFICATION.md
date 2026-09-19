# Source Verification - Fetal Doppler-ECG Cardiac Cycle Ledger

## Intended Source

Source dataset: NInFEA: Non-Invasive Multimodal Foetal ECG-Doppler Dataset for Antenatal Cardiology Research v1.0.0.

Official PhysioNet page: https://physionet.org/content/ninfea/1.0.0/

Official file index URL: https://physionet.org/files/ninfea/1.0.0/

Official ZIP import URL: https://physionet.org/content/ninfea/get-zip/1.0.0/

DOI: https://doi.org/10.13026/c4n5-3b04

## Access And License

PhysioNet lists the database as open access. The access policy says anyone can access the files as long as they follow the specified license. The file license is Open Data Commons Attribution License v1.0 (ODC-By).

The license text permits sharing, modifying, and using the database subject to attribution. Section 3.1 of ODC-By grants worldwide, royalty-free rights that explicitly include commercial use and do not exclude any field of endeavour. It also requires attribution/notice when publicly using produced works. The challenge documentation and dataset form include the required source and license notices.

Source gate result: PASS for commercial challenge use, reuse, direct import, and redistribution of official raw files with attribution. The preferred upload path is the official PhysioNet ZIP endpoint, because the platform URL importer may download only the small HTML directory index when given the file-index URL.

## Access Restrictions

No credentialed access gate was shown for the files. PhysioNet displays terminal download instructions:

```text
wget -r -N -c -np https://physionet.org/files/ninfea/1.0.0/
aws s3 sync --no-sign-request s3://physionet-open/ninfea/1.0.0/ DESTINATION
```

## File Sizes And Layout

PhysioNet reports total uncompressed size of 2.0 GB and a downloadable ZIP of 792.9 MB. A HEAD check of `https://physionet.org/content/ninfea/get-zip/1.0.0/` returned `content-type: application/zip`, `content-length: 831389363`, and a PhysioNet ZIP filename.

Top-level official items:

```text
bin_format_ecg_and_respiration/
code/
pwd_images/
wfdb_format_ecg_and_respiration/
LICENSE.txt
RECORDS
SHA256SUMS.txt
```

`RECORDS` lists 60 WFDB records: `wfdb_format_ecg_and_respiration/1` through `wfdb_format_ecg_and_respiration/60`.

The `pwd_images/` folder contains matching numbered `.bmp` Doppler strip images. Example page sizes include `1.bmp` at 8.1 MB, `10.bmp` at 11.5 MB, and records ranging from a few MB to tens of MB.

The `wfdb_format_ecg_and_respiration/` folder contains matching numbered `.dat` and `.hea` files. Example header `1.hea` reports 34 signals, 2048 Hz, and 57,490 samples. The signal names include 24 abdominal unipolar channels, 3 thoracic ECG channels, maternal respiration (`matrsp`), saw, sync, and unused DC channels.

## Raw Files Needed

Required for this challenge:

```text
pwd_images/*.bmp
wfdb_format_ecg_and_respiration/*.hea
wfdb_format_ecg_and_respiration/*.dat
RECORDS
LICENSE.txt
SHA256SUMS.txt
```

Optional but acceptable in a clean official upload:

```text
bin_format_ecg_and_respiration/*.bin
code/*
```

`prepare.py` uses only the PWD bitmap strips and WFDB ECG/respiration files. It does not require the MATLAB code or binary-format duplicate files.

## Recommended Platform Import Procedure

Preferred path:

1. In the dataset source-file/import UI, import the official ZIP URL `https://physionet.org/content/ninfea/get-zip/1.0.0/`.
2. Confirm that the rebuilt tree exposes either an official ZIP file or extracted folders containing `pwd_images/`, `wfdb_format_ecg_and_respiration/`, `RECORDS`, `LICENSE.txt`, and `SHA256SUMS.txt`.
3. Run `prepare.py` with the rebuilt official source directory as `raw`.

Do not use `https://physionet.org/files/ninfea/1.0.0/` as the platform import URL unless the importer explicitly supports recursive directory indexes. In the current platform UI this URL can import only a ~1 KB `downloaded-file`, which is the HTML listing rather than the dataset.

Fallback path if the platform cannot import the official URL:

1. Download the official files unchanged with `wget -r -N -c -np https://physionet.org/files/ninfea/1.0.0/` or the unsigned S3 sync command shown by PhysioNet.
2. Upload the unchanged official file tree directly, or run `zip_raw_for_upload.py` on the unchanged official root to make a clean source-file ZIP.
3. Do not upload a preprocessed raw ZIP, train/test split, prepared segment package, private answer file, or generated labels.

## Novelty Gate

Closest neighbors found before implementation:

1. NInFEA's own intended use: fetal ECG extraction and signal-processing research with simultaneous Doppler/PWD and respiration.
2. NInFEA-related PWD tasks: Doppler envelope extraction and automatic recognition/detection of fetal atrioventricular activity or measurable cardiac cycles.
3. Fetal QRS and fetal heart-rate benchmarks on PhysioNet-style abdominal ECG data.
4. Recent ECG-to-Doppler reconstruction papers using NInFEA-like paired ECG and Doppler envelopes.

Novelty judgment: upper-recombined, estimated 6/10 to 7/10 if the visible challenge stays focused on the clinical evidence-ledger contract. The challenge is not just canonical fetal QRS detection, heart-rate regression, or Doppler envelope extraction because a valid submission must jointly align three inputs, produce a structured cardiac-cycle event ledger with cycle boundaries, provide a Doppler envelope array, classify each cycle's usable/uncertain/artifact quality from cross-modal agreement, and calibrate row confidence. It also scores subgroup robustness over hidden acquisition/quality axes.

Novelty risk: if the title or first paragraphs are rewritten as "fetal heart-rate estimation" or "Doppler envelope detection", the platform novelty checker may collapse it into existing NInFEA/PWD benchmarks. The public description therefore emphasizes "evidence ledger" and explicitly bans reduction to source-row lookup, direct heart-rate regression, or a one-signal fetal QRS benchmark.

## Source Reversibility

The prepared public rows use salted opaque numeric ids and do not expose record numbers, subject identifiers, original filenames, exact source start times, or raw order. Public artifacts are row-local transformed strips/signals, not source filenames. Private labels are deterministic cycle/evidence records derived by `prepare.py` from official raw signals and strip images.

Residual risk: because the upstream source is public, a participant may try to identify the raw record by media matching. The hidden target is deliberately not an official annotation table or subject metadata; source recovery alone does not reveal a separate answer key. The participant-visible rules nevertheless prohibit source-row lookup, raw record/timing reconstruction, and using hidden PhysioNet metadata.

## Sources Consulted

- PhysioNet NInFEA v1.0.0 source page: https://physionet.org/content/ninfea/1.0.0/
- NInFEA license file: https://physionet.org/content/ninfea/1.0.0/LICENSE.txt
- NInFEA RECORDS: https://physionet.org/content/ninfea/1.0.0/RECORDS
- NInFEA WFDB header example: https://physionet.org/content/ninfea/1.0.0/wfdb_format_ecg_and_respiration/1.hea
- NInFEA SHA256SUMS: https://physionet.org/content/ninfea/1.0.0/SHA256SUMS.txt

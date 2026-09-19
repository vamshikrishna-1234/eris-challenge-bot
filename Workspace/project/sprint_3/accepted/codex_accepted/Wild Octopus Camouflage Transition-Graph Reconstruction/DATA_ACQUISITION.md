# Data acquisition and upload procedure

This is the acquisition record for the MEVA pivot. The archive is untouched official data and is not a processed challenge dataset.

## 1. Preferred import-from-URL method

Run `python generate.py --output <raw-dir>` to download the frozen manifest. Stable official URL patterns, expected names, licenses, and checks are:

- Video: `https://mevadata-public-01.s3.amazonaws.com/drops-123-r13/<YYYY-MM-DD>/<HH>/<basename>.r13.avi`; each expected byte count and S3 ETag is frozen in `generate.py`.
- Activity annotations: `https://gitlab.kitware.com/meva/meva-data-repo/-/raw/421841a75577b697c314e952e585aecbb1b99e17/annotation/DIVA-phase-2/MEVA/kitware/<YYYY-MM-DD>/<HH>/<basename>.activities.yml`.
- Type annotations: the same pinned URL with `.types.yml`.
- Official documentation: the repository `LICENSE`, `README.md`, annotation-list README, `documents/activity-names.txt`, `documents/KPF-specification-v4.pdf`, and `documents/MEVA-Annotation-Definitions.pdf`.

The source license is CC BY 4.0. The 21 videos have the exact byte sizes in `generate.py`; annotation/document URLs are pinned to commit `421841a75577b697c314e952e585aecbb1b99e17` and verified by non-empty content and SHA-256 at download time. The complete official tree is below 1,000,000,000 bytes.

## 2. Direct official download and upload fallback

If URL import is unavailable, download the same 21 video files and matching 42 YAML files plus the seven official documentation files through a normal browser or `curl` using the URLs above. Preserve every official directory and filename. Verify the video byte counts and the CC BY 4.0 `LICENSE` before upload. Upload only those untouched files as the dataset's raw source.

## 3. Clean transport package when URL imports fail

The exact fallback is:

`D:\create_challenge_synthetic_output_folder\sprint_3\codex_output_folders_sprint_3\Wild Octopus Camouflage Transition-Graph Reconstruction\OFFICIAL_RAW_FILES_ONLY.zip`

It contains 70 official members, 970,257,026 uncompressed bytes, and is 969,981,917 bytes on disk. SHA-256:

`fd878a4b013dd818888d12fd619cd17622df9b1cb1c43bf62db61f3aab3404cd`

Upload this one file as the raw-data fallback. Do not add `prepared/`, CSVs, clips, frames, split files, generated labels, caches, or source code to the archive.

## 4. Preparation boundary

The archive is untouched CC BY 4.0 source data. Extraction, validation, annotation/video synchronization, non-overlapping window selection, anonymizing crop/re-encoding, opaque ID generation, grouped split construction, target graph derivation, and public/private asset creation occur reproducibly only inside `prepare.py`.

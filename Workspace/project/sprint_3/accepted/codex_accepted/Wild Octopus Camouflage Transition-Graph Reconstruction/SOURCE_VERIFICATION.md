# Source, License, and Linkage Verification

Checked 2026-07-15. The original wild-octopus candidate was rejected before construction because its official package contains only seven videos and 290.109 seconds. This artifact therefore uses the verified MEVA subset already present in the raw transport archive.

## Official source and rights

- Source project: Multiview Extended Video with Activities (MEVA), Kitware Inc. and IARPA.
- Official data repository: https://gitlab.kitware.com/meva/meva-data-repo (annotation/document commit `421841a75577b697c314e952e585aecbb1b99e17`)
- Official video bucket: https://mevadata-public-01.s3.amazonaws.com/
- License: Creative Commons Attribution 4.0 International (CC BY 4.0), as stated verbatim in the archived `LICENSE` file. This permits commercial reuse, redistribution, and derivatives with attribution.
- Rights caveat: CC BY 4.0 is copyright licensing; the MEVA LICENSE also reserves privacy, publicity, and other personality rights. Organizers should confirm their platform's commercial-use and human-footage/privacy policy before publication and retain the required Kitware/IARPA attribution.
- Raw archive: `OFFICIAL_RAW_FILES_ONLY.zip`, 969,981,917 bytes; SHA-256 `fd878a4b013dd818888d12fd619cd17622df9b1cb1c43bf62db61f3aab3404cd`.
- Archive members: 70 untouched official files (21 `.r13.avi` videos, 42 official YAML annotation files, the official annotation list, activity vocabulary, specification PDFs, README, and LICENSE). Uncompressed member bytes: 970,257,026.

## Exact selected files and groups

`generate.py` contains the frozen URL/byte manifest for every selected video and annotation. The 21 videos are five-minute, 29.97-30 FPS MEVA clips from school, bus, and hospital cameras. The frozen `SOURCE_SPECS` table assigns 15 strongest-available recording-session groups; all clips from a group stay in one split. Sixteen source clips are train and five are held out for test, yielding 479 train windows and 175 test windows without neighboring-window overlap. The held-out groups are event-bearing EO sessions; IR sessions are retained in train because their official annotations contain only empty intervals.

## Annotation linkage and target derivation

Each selected video basename has exactly one official `activities.yml` and one `types.yml` under the matching date/hour directory. `prepare.py` checks membership in the official `list-of-annotated-meva-clips.txt`, exact video byte counts, unique source hashes, non-empty YAML, and CC BY license text before decoding. Activity spans (`tsr0` frame ranges), activity labels (`act2`), actor identifiers, and actor type labels (`cset3`) are read only from those official files. Nodes are clipped frame spans with documented `(agent, action, context, roles)` tuples. The `MEVA-Annotation-Definitions.pdf` contains the coupled-activities table; `prepare.py` transcribes that finite official table and applies it only when the two official spans overlap or are within one second. `temporal_overlap` and `temporal_next` use only source frame ranges. No guessed label pair is introduced.

## Prepared-media privacy and retrieval controls

Preparation performs deterministic frame sampling, motion-centered square cropping, horizontal flip/perspective/color/noise transforms, median-background softening, metadata stripping, and H.264 re-encoding inside `prepare.py`. Public IDs are salted SHA-256 digests of source basename and window start; source names, timestamps, annotation IDs, groups, and raw paths never appear in public CSVs. Windows are separated by a 0.5-second guard and no source group crosses train/test. `_analyze.py` runs filename/timestamp scans, raw-name scans, public-ID reversibility checks, file-size constancy checks, and a metadata-only baseline; it does not use private answers.

## Feasibility gates

- Independent groups: 15 (pass; held-out test groups: 5).
- Non-overlapping prepared items: 654 total (479 train, 175 test; pass).
- Public media: approximately 439 MB at 256x256, 32 frames, 4 FPS (pass; measured after CRF-12 deterministic preparation; per-clip byte range 414,018-961,477).
- Graph support: positive, multi-node, and official-pair rows are asserted in `prepare.py` before output.
- CPU budget: the reference uses 32-frame CPU MobileNet/ResNet embeddings plus a small GRU/structured decoder; no end-to-end large video transformer is required.

The octopus source remains documented in the historical audit files only; it is not part of this challenge's source claim or raw package.

Use the reusable eris-challenge-factory skill. The user has approved BatVision and explicitly requested this separate task to pursue the challenge end to end. This is a feasibility-first task with conditional build continuation, NOT a claim that the full-build readiness gate has passed. Run the bounded missing checks here, record evidence, and build in this same task only if they pass. Do not open another task or silently replace the dataset.

EXACT TASK TITLE: BatVision Complementary Sight-Echo Recovery
Category: From Scratch ONLY. Do not also label it Fine-Tuning. GPU preferred; use CPU only if the actual workload makes GPU unjustified or infeasible. Do not mislabel CPU-only methods as GPU training.
Model preference: gpt-5.6-sol with xhigh reasoning.
Project: C:\Users\vamsh\Downloads\create_challenge_synthetic
Requested final output: E:\create_challenge_synthetic_output_folder\sprint_5\BatVision Complementary Sight-Echo Recovery
Registry: C:\Users\vamsh\Downloads\create_challenge_synthetic\challenge_registry\batvision-complementary-sight-echo-recovery.json
Keep initial pilot evidence under challenge_registry\pilot_evidence\batvision-complementary-sight-echo-recovery; only promote to full build after measured readiness. Preserve all unrelated existing files.

CURRENT USER CONSTRAINTS
GPU preferred, CPU fallback permitted. CV, object detection, sequence-to-sequence, NLP and other ML domains are allowed. Avoid generic classification, tabular prediction, or ordinary regression disguised with a JSON wrapper or decorative extra heads. Novelty must credibly meet at least 6/10; no fabricated scores or guarantees. Plan for a 1.5-hour complete solve budget and confirm the currently applicable hardware/memory limits from living rules before final configuration. Historical CPU-only announcements in old files do not override the user's latest GPU preference.
The user explicitly waives public-source lookup as a blocking gate. Document residual risk honestly and record the waiver, not a fictitious passed attack. This does NOT waive direct answer leakage, duplicated train/test scenes, unobservable targets, licensing, reproducibility, independent evaluation, or novelty.

TASK CONTRACT TO VALIDATE
Input: real synchronized RGB scene image with controlled missing regions, an intact binaural echo channel and a second echo channel with controlled gaps, plus explicit availability masks and genuinely necessary acquisition calibration.
Output: recovered native depth map and restored binaural echo signal, with clear validity conventions. Score restoration on withheld portions, so copying observed data does not earn most credit. Do not require confidence or invented uncertainty gold unless supported by a defensible calibration evaluation.
Simple meaning: repair complementary failures in a robot's visual and acoustic sensing using evidence that survives in the other sensor.
Preserve the audio-output goal. Base64-encoded WAV or bounded numeric arrays are only transport encodings, not novelty; decide the platform-compatible submission schema after actual sample inspection.
Do not automatically add a depth-to-echo physics consistency score: off-camera reflectors, unknown materials and multipath make depth alone insufficient to determine the complete echo. Do not reward two plausible but unrelated heads either. Measure cross-modal benefit through ablations. Exact missing waveform phase may be unidentifiable; test suitable multiresolution spectral, envelope and binaural timing metrics without arbitrary score shaping.

OFFICIAL SOURCES AND LICENSE
Official project: https://amandinebtto.github.io/Batvision-Dataset/
Authors' code and source links: https://github.com/AmandineBtto/Batvision-Dataset
Author README: https://raw.githubusercontent.com/AmandineBtto/Batvision-Dataset/main/README.md
Original official download share: https://cloud.minesparis.psl.eu/index.php/s/qurl3oySgTmT85M
Author-linked repository mirror: https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi:10.57745/HYLZNL
Paper: https://arxiv.org/abs/2303.07257
The official README explicitly states the DATASET is CC BY-SA 4.0. License terms: https://creativecommons.org/licenses/by-sa/4.0/
Retain attribution, source/version notices and change notices; distribute adapted dataset material under CC BY-SA 4.0 or an actually compatible license. Check that platform distribution terms permit compliance; do not promise exclusive/proprietary dataset rights. Do not infer code licensing from dataset licensing. A guessed raw GitHub /main/LICENSE URL returned 404, so do not cite it as a retrieved license file; use the authors' explicit dataset statement and inspect repository/mirror metadata.
Verified source description: paired RGB-D imagery and 0.5-second binaural echoes sampled at 44.1 kHz. BV1 and BV2 are distinct collections; BV2 has location-specific directories with train/val/test CSVs. This is not proof that the upstream random splits are appropriate.
Known closest benchmark: authors supply an audio-only U-Net for echo-to-depth prediction. The proposed joint complementary-failure task must be materially different and actually require both modalities; simply bundling familiar tasks does not establish originality.

MEASURED VS MISSING EVIDENCE
License statement and native modality description verified on official documentation. No no-hit scan should be treated as full semantic duplicate clearance. Previous local full-description archive keyword scan found no explicit BatVision hit, but a fresh semantic comparison is required.
NOT YET MEASURED: raw subset bytes/direct links, downloadable members, native sample validation, post-filter usable pairs, independent room/route/session counts, held-out split stability, simple/fused baselines, solution runtime. These are pilot gates, not completed build evidence. Never fabricate them or repeat the previous failed pattern of treating many adjacent frames as independent scenes.

SOURCE PACKAGING (IMPORTANT)
Prefer direct import from official raw file URLs. Source pages, cloud share HTML and repository landing pages are NOT validated raw import links. Resolve and test real stable file URLs and report names, byte sizes and checksums.
Aim for an untouched source package below 1 GB; if insufficient for robust independent evaluation, target below 3 GB. The user allows approximately 3-5 GB as an outer range, not permission for an unlimited archive. Prepared data ideally near/below 500 MB when scientifically adequate. Base64 overhead must be budgeted.
With <=4-5 source URLs, prefer official URL import; fallback is download and upload those EXACT official files unchanged.
With >5 necessary URLs, create one clean ZIP of byte-identical downloaded official files, preserving filenames and provenance, plus an external source manifest. No preprocessed or postprocessed raw package.
ALL cropping, resizing, resampling, masking/corruption, sample selection within files, splits, anonymization, target derivation and prepared-data size reduction belong in prepare.py. Selecting a bounded set of complete official files is permitted; rewriting source files before upload is not.
Prefer remote metadata and bounded source inspection before bulk acquisition. Do not download a huge archive to the laptop merely to discover its size. No platform upload/submission, paid services or author contact unless separately authorized.

BOUNDED PILOT
1. Inspect actual matched records and depth validity/synchronization; verify usable rights and source member access.
2. Inventory physical rooms/locations, routes, consecutive capture families, dates and recording sessions. Treat neighboring frames as dependent. Report raw and post-filter independent-group counts. Do not invent a universal minimum number of rooms; establish stable group-held-out validation with enough diversity and evaluate group variation.
3. Resolve a compact untouched raw source route that preserves sufficient train/test diversity. If only oversized monoliths exist, investigate author-provided mirrors or unchanged individual members before declaring a blocker.
4. Run image-only depth, echo-only authors' baseline, copied-other-ear/delay-gain audio, interpolation/spectral templates, independent-head restoration, and a compact fused from-scratch model. Check no-op and copied-input metric behavior and estimated full-budget runtime.
5. Audit modality necessity, target determinacy, task novelty and share-alike distribution compatibility. Record a reviewer premortem and measured readiness card. No decorative heads, artificially hostile thresholds or inflated novelty score.
6. If a gate fails, try a bounded source-grounded salvage within this dataset. If unsalvageable, report the precise measured blocker and stop without creating pretend ready artifacts. Do not automatically archive yourself. If gates pass, continue into full build without asking for duplicate approval.

FULL BUILD AFTER PASS
Read and follow current .cursor\rules\challenge-creation.mdc, rules\LATEST.md, rules\checkpoints, rules\prev_reviews.txt, rules\challenge_template_file_creation.txt, relevant accepted examples and current factory references. Resolve missing paths honestly.
Duplicate roots include project Shipd_Challenge_Archive_All, Shipd_Challenge_Archive_Novel, shipd_domain_challenge_docs, registry, and E:\create_challenge_synthetic_output_folder\sprint_3, sprint_4 and sprint_5. Do not modify the user's Google Sheet.
Implement complete required package: deterministic prepare.py, strict grade.py, aligned PASTE_THIS copies where required, description/forms, sample submission, baseline, tests, licenses/attribution, source manifest, source-verification/readiness reports and DATA_IMPORT_PROCEDURE.md. Grader must bound decoded payload sizes and safely reject malformed arrays, NaN/Inf, wrong IDs/shapes and unsafe NPZ object loading. Perfect oracle 1.0; weak sample valid; no hidden arbitrary weights or score powers.
Separate public train/test inputs from private test targets; ensure prepare is deterministic and equivalent on official direct imports vs untouched-file ZIP. Record actual runtime and all limitations; no unrun check marked passed.
At completion give: final title/category/compute, absolute output folder, measured raw/prepared sizes and split counts, tests/baselines, and numbered data procedure:
A. exact validated official import URLs (preferred);
B. downloading and uploading unchanged official files if URL import fails;
C. exact path/checksum of clean source ZIP when >5 URLs are required.
Keep registry and returned status synchronized. Do not submit the challenge on Shipd from this task without separate authorization.


FRESH OFFICIAL MIRROR METADATA (parent verified immediately before dispatch)
The Dataverse API returned released version 1 and the full Attribution-ShareAlike 4.0 legal terms in termsOfUse (license field is null; do not mistake that for absent licensing). Files are unrestricted:
627779 Batvision_Dataset-0.tar.gz 36,858,622,568 bytes
627781 Batvision_Dataset-1.tar.gz 37,038,443,764 bytes
627782 Batvision_Dataset-2.tar.gz 37,196,220,168 bytes
627790 Batvision_Dataset-3.tar.gz 36,560,507,311 bytes
627791 Batvision_Dataset-4.tar.gz 20,882,628,724 bytes
API: https://entrepot.recherche.data.gouv.fr/api/datasets/:persistentId/?persistentId=doi:10.57745/HYLZNL
Each mirror archive exceeds even 5 GB. Do NOT present those as compliant direct-import files or download them wholesale. FIRST inspect the authors' original cloud share for individual complete records or smaller official archives; validate a compact acquisition path and independence before training. Compressed tar byte-range fetching is not automatically selective member access. If no practical untouched compact route exists, report the packaging blocker honestly. Source licensing is confirmed, but compact source access is not.

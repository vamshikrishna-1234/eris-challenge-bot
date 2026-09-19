# Opaque Security Clip Action Ledger Recovery

This artifact is a documented pivot from the requested wild-octopus source. The Zenodo/Dryad octopus package failed the mandatory scale and independence gate (seven videos, 290.109 seconds). The actual files retained in this output folder are a different, verified real-data source: the Multiview Extended Video with Activities (MEVA) subset from Kitware/IARPA, licensed CC BY 4.0.

The pivot is intentional and keeps the required structured objective: a source-neutral 256x256, 32-frame video is mapped to a variable-length JSON graph of annotated activity spans and typed temporal/coupling edges. The selected MEVA subset has 21 official five-minute clips, 15 non-overlapping recording-session groups, 479 train items and 175 test items after deterministic preparation, and a raw official-only transport archive below 1 GB.

Read `SOURCE_VERIFICATION.md` for source, license, checksums, and linkage evidence; `DATA_ACQUISITION.md` for URL and fallback import instructions; `CHALLENGE_FORM_FILL.md` and `DATASET_FORM_FILL.md` for the participant-facing forms; and `_sanity_smoke.py`/`_analyze.py` for deterministic validation and shortcut audits. Preparation materializes 654 clips (479 train, 175 test), with 460,026,529 bytes of public media in the latest CRF-12 run. `CHECKPOINTS_LINE_AUDIT.csv` and `AUDIT_EXCEPTIONS.md` record the final mechanical checks and the documented YAML/AVI false positive.

The directory name is preserved because it was the user-required output location; the challenge title and all participant/source documentation use the truthful MEVA name above.

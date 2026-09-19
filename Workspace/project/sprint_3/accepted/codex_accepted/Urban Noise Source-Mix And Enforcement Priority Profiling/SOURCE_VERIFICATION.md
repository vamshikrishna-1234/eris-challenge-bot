# Source Verification

Checked on 2026-07-06 against the official Zenodo HTML page and API record.

## Official Source

Primary source page: https://zenodo.org/records/3966543

Official API record: https://zenodo.org/api/records/3966543

Dataset title: SONYC Urban Sound Tagging (SONYC-UST): a multilabel dataset from an urban acoustic sensor network

DOI: https://doi.org/10.5281/zenodo.3966543

Zenodo metadata version: 2.3.0

Publication date: 2020-09-14

License id in Zenodo metadata: `cc-by-4.0`

The official record and bundled README describe SONYC-UST as real urban acoustic sensor audio from the SONYC network in New York City, with 10-second recordings, volunteer and verified annotations, 23 fine-grained classes grouped into 8 coarse classes, `annotations.csv`, `dcase-ust-taxonomy.yaml`, `README.md`, and official audio tarballs. The API file list totals about 13.3 GB, so this challenge uses one bounded official audio shard plus metadata files.

## Selected Official Files

These are the only files that should be URL-imported or directly uploaded unchanged as raw source files:

| File | Official URL | Size bytes | MD5 |
|---|---|---:|---|
| `annotations.csv` | https://zenodo.org/api/records/3966543/files/annotations.csv/content | 14,488,305 | `70b507b15bb4cfcce4870925302f276b` |
| `dcase-ust-taxonomy.yaml` | https://zenodo.org/api/records/3966543/files/dcase-ust-taxonomy.yaml/content | 1,081 | `6c1cca1c4c383a6ebb0cb71cb74fe3a9` |
| `README.md` | https://zenodo.org/api/records/3966543/files/README.md/content | 11,340 | `bdfa3a4c0d90053f622b52afa0fc86f7` |
| `audio-0.tar.gz` | https://zenodo.org/api/records/3966543/files/audio-0.tar.gz/content | 721,618,074 | `bbb4dbae7d2e58e18d24878b9ee1eb51` |

Total selected official source size: 736,118,800 bytes, about 736.1 MB decimal. This is below the requested approximate 1 GB source cap. Locally downloaded `audio-0.tar.gz` was verified with MD5 `bbb4dbae7d2e58e18d24878b9ee1eb51`; `prepare.py` checks this hash before using the archive.

For faster single-file upload, I also created `sonyc_ust_official_selected_source_files.zip` on 2026-07-16. This zip is a transfer bundle only: it contains the four selected official files unchanged at the zip root, with no prepared split, no derived audio, no private answers, and no generated metadata. Zip size is 736,119,248 bytes and zip SHA-256 is `0d1e24f36e3e0c0e09c7871231e98740ec99d36227e2a1544ab0c116fe1de471`.

The smaller `audio-18.tar.gz` shard was inspected and rejected for the final source selection because it contains only 510 WAVs and too little verified construction/saw coverage. In the inspected metadata join it had 48 verified rows, with zero verified machinery-impact positives and zero verified powered-saw positives. `audio-0.tar.gz` contains 1000 WAVs and gives better rare-source coverage while keeping the selected source under 1 GB.

## Raw Layout Expected By `prepare.py`

Preferred URL import layout:

```text
annotations.csv
dcase-ust-taxonomy.yaml
README.md
audio-0.tar.gz
```

If the platform auto-extracts the audio archive, `prepare.py` also accepts an extracted official directory:

```text
annotations.csv
dcase-ust-taxonomy.yaml
README.md
audio-0/*.wav
```

Single-file upload fallback:

```text
sonyc_ust_official_selected_source_files.zip
```

`prepare.py` accepts the single-file fallback if the platform retains the zip instead of extracting it. If the platform extracts it, the expected root contents are the same four official files shown above.

No processed `raw.zip`, `raw_upload.zip`, derived audio, split CSV, label table, or answer file should be uploaded. The optional convenience zip is only a file-transfer bundle of unchanged official source files. All annotation parsing, label derivation, grouped splitting, public audio transformation, ID salting, target construction, and public/private output creation happens in `prepare.py`.

## License And Redistribution

The official Zenodo metadata lists license id `cc-by-4.0`, Creative Commons Attribution 4.0 International. The bundled README states that SONYC-UST is offered under CC BY 4.0 and links to https://creativecommons.org/licenses/by/4.0/.

CC BY 4.0 allows sharing and adaptation for any purpose, including commercial use, provided attribution is given, the license is linked, and changes are indicated. The selected platform source files are unchanged official Zenodo files, and the prepared public WAVs are transformed derivatives with attribution retained in the dataset documentation. I found no official terms on the verified source pages that block commercial challenge use, transformation, redistribution, or direct platform URL import.

Recommended attribution: Mark Cartwright, Jason Cramer, Ana Elisa Mendez Mendez, Yu Wang, Ho-Hsiang Wu, Vincent Lostanlen, Magdalena Fuentes, Graham Dove, Charlie Mydlarz, Justin Salamon, Oded Nov, and Juan Pablo Bello, SONYC Urban Sound Tagging dataset, DOI 10.5281/zenodo.3966543, CC BY 4.0.

## Label Provenance

Targets are derived only from official `annotations.csv` columns and the official taxonomy. `source_mix_json` uses the eight official coarse source families after renaming to source-neutral broad groups: `engine`, `machinery_impact`, `powered_saw`, `alert_signal`, `music`, `human_voice`, `dog`, and `other_impact`. The weights combine verified annotations when present, volunteer vote proportions, and volunteer proximity labels (`near`, `far`, `notsure`) into bounded source-family strengths.

`dominant_source`, `nuisance_pattern`, `enforcement_priority`, and `confidence` are deterministic aggregations of those official presence, fine-class, proximity, verified-label, and volunteer-agreement fields. Construction machinery, powered saws, alert signals, loud/social sound, animal/other impact, and diffuse traffic mixtures are separated in the target schema. This is not an external or arbitrary toy label source.

Public train/test CSVs do not expose original filenames, sensor ids, block/location coordinates, time fields, original split labels, annotator ids, annotation rows, source row order, or hidden grouping axes. Prepared audio filenames and public ids are salted opaque hashes. Public WAVs are 16 kHz transformed excerpts with deterministic loudness normalization, slight source-preserving coloration, dither, fades, and crop offsets so they are not exact source copies.

## Novelty Gate

Closest neighbors:

| Neighbor | Overlap | Difference |
|---|---|---|
| SONYC-UST / DCASE 2020 Urban Sound Tagging | Same source audio and annotation taxonomy | Canonical task predicts clip-level sound tags, often with optional spatiotemporal context |
| Prior rejected local SONYC challenge | Same source and plain tag objective | Rejected because it reused the 8 coarse tags as the task |
| Urban complaint triage systems | Similar real-world use case | Usually not public audio benchmarks with volunteer proximity and verified consensus labels |

Novelty judgment: borderline pass, estimated 5/10. The source dataset and standard AST/CRNN audio-tagging solution family are close, and the local review history explicitly warns that a plain SONYC tag-vector challenge is a blocker. This build avoids the rejected formulation by making the scored target a compact source-mix and enforcement-priority profile rather than the canonical fine/coarse multilabel tag vector. It uses volunteer proximity, verified-label availability, annotator agreement, fine-class severity, and multi-source nuisance grouping to form continuous mixture weights, a practical priority tier, a nuisance pattern, a dominant-source decision, and a calibrated confidence target.

The novelty is not high because a strong SONYC tagger can still be adapted as an important component. The reason the gate passes rather than stops is that a tagger alone is not the submitted output: solvers must learn source strength/proximity cues, ambiguous mixtures, construction/social/alert priority tradeoffs, and calibrated reliability under hidden subgroup scoring. If the platform novelty checker treats any SONYC-derived annotation aggregation as too close to DCASE, the correct pivot is to leave the SONYC tag family entirely, not to polish wording.

## Local Verification Summary

Local prepared split from the selected official source files:

| Check | Result |
|---|---:|
| Public train rows | 701 |
| Public test rows | 299 |
| Prepared public size | 288,331,032 bytes |
| Sample submission score | 0.1433879071797786 |
| Perfect submission score | 1.0 |
| Malformed all-core submission score | 0.0 |
| Train-prior baseline | 0.3247976184598513 |
| Duration-only baseline | 0.32479826817274976 |
| ID-hash metadata-only baseline | 0.2924186824467303 |
| Simple energy/spectral kNN baseline | 0.40405913002734317 |

Leakage probes in `_analyze.py` found zero raw filename hits in public CSVs, zero forbidden metadata tokens, zero source-like public audio paths, and one constant public duration value (`9.0` seconds), so duration alone is weak and source lookup is not enabled by public metadata.

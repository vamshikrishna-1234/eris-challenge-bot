# Source Verification

Verified on 2026-07-04 IST against the official Zenodo API record and Creative Commons license deed.

## Official Source

Primary source page: https://zenodo.org/records/3371780

Official API record: https://zenodo.org/api/records/3371780

Dataset title: GuitarSet

DOI: https://doi.org/10.5281/zenodo.3371780

Selected official source files for platform URL import:

| File | Official URL | Size |
|---|---|---:|
| annotation.zip | https://zenodo.org/api/records/3371780/files/annotation.zip/content | 39,132,574 bytes |
| audio_mono-mic.zip | https://zenodo.org/api/records/3371780/files/audio_mono-mic.zip/content | 656,927,981 bytes |

Total selected official source import size: 696,060,555 bytes, about 696.1 MB decimal. This is below the requested 1 GB raw-source cap. The selected files are imported directly from Zenodo; there is no `raw_upload.zip` and no repackaged raw archive. After platform URL import, the validator may expose the extracted contents as `annotation/` and `audio_mono-mic/` directories rather than top-level `.zip` files.

Files intentionally excluded:

| Excluded file | Size | Reason |
|---|---:|---|
| audio_hex-pickup_original.zip | 3,210,735,945 bytes | Over the 1 GB source cap |
| audio_hex-pickup_debleeded.zip | 3,607,349,578 bytes | Over the 1 GB source cap |
| audio_mono-pickup_mix.zip | 683,145,360 bytes | Not needed; would push selected imports over 1 GB |

## License

The official Zenodo metadata lists the license id as `cc-by-4.0`, Creative Commons Attribution 4.0 International. The Creative Commons deed for CC BY 4.0 allows sharing and adaptation for any purpose, including commercial use, provided attribution is given, license information is linked, changes are indicated, and no additional legal restrictions are applied.

CC BY 4.0 and "Creative Commons Attribution 4.0 International" are in the workspace-approved license list. The license gate passed: I found no official terms on the verified source pages that block commercial reuse, transformation, redistribution, or platform upload/import.

## Attribution And Citation

Dataset creators listed by Zenodo: Qingyang Xi, Rachel M. Bittner, Johan Pauwels, Xuzhou Ye, and Juan P. Bello.

Recommended academic citation from the official record:

```text
Q. Xi, R. Bittner, J. Pauwels, X. Ye, and J. P. Bello, "GuitarSet: A Dataset for Guitar Transcription", in 19th International Society for Music Information Retrieval Conference, Paris, France, Sept. 2018.
```

Prepared public audio clips are source-rate excerpts derived from the official mono microphone recordings without added noise, EQ, phase randomization, or de-identification transforms; attribution to GuitarSet and the CC BY 4.0 license must be retained.

## Real-Data Handling

This is a real-data build. The platform dataset source should import the two official Zenodo URLs listed in `URL_IMPORT_LIST.txt` directly. The dataset form describes the validator-visible extracted directories, `annotation/` and `audio_mono-mic/`; `prepare.py` handles both those extracted directory layouts and local official zip-file layouts. It performs all parsing, filtering, segment selection, note extraction, split assignment, target construction, public/private file creation, and public audio materialization.

The public split does not expose source filenames, original JAMS filenames, performer IDs, raw track IDs, source timestamps, raw note onset/duration values, source event order, style/progression/key/tempo fields, raw row order, or annotation member paths. Public IDs, event IDs, event order, and audio filenames are salted SHA-256-derived or row-local opaque values. `clip_start_s` is the start of the prepared clip and is always 0.0, not the source-track timestamp. Only mono microphone audio is used; no string-isolated hexaphonic pickup channels are exposed.

The prepared public audio consists of bounded short WAV clips under `public/audio/`, not copies of full GuitarSet recordings. `prepare.py` cuts source-rate mono microphone excerpts without synthetic noise, EQ, phase randomization, or other perturbation so the guitar audio remains realistic.

## Novelty Gate

Closest public neighbors:

| Neighbor | Overlap | Difference |
|---|---|---|
| GuitarSet canonical transcription | Same source and guitar annotations | Usually predicts pitch/onset/notes from audio |
| Generic AMT benchmarks | Audio to note events | Do not require guitar string/fret realization |
| Symbolic MIDI-to-tab work | Note skeleton to string/fret | Lacks real audio/timbre evidence |
| End-to-end guitar tab transcription | Audio to full tablature | Usually includes pitch/onset detection |

Novelty judgment: passed, estimated 6/10. GuitarSet's canonical use is automatic guitar transcription from audio: recover note activity, pitch contours, and related musical annotations. This challenge deliberately removes the ordinary pitch transcription head from the public test problem by providing a compact note skeleton with opaque event IDs and MIDI pitch. The hidden target is the performed tablature realization: which string and fret were used for each already-known pitch event. This changes the ML problem because most guitar pitches have multiple physically valid string/fret positions, and a pitch-only transcription can be correct while the tablature is wrong.

The nearest symbolic neighbor is MIDI-to-tab or score-to-tab assignment, where a solver infers string/fret from notes alone using playability priors. This build adds real mono microphone audio, held-out performer grouping, and hidden robustness axes over style, polyphony, ambiguity, fret range, and note density. A strong solution should use audio timbre, context, and training examples to improve beyond a pitch-only/string-prior assignment. It is therefore not the same as plain note transcription and not merely a smaller reshuffle of GuitarSet's canonical AMT task.

Potential weakness and mitigation: because the source annotations and source audio are public, a test note skeleton plus public audio can in principle be matched against GuitarSet by an external lookup attack. `prepare.py` still uses short clips, opaque salted IDs, row-salted event IDs/order, source-neutral public challenge prose, no original timestamps, no raw note onset/duration values, no source filenames, no player/style metadata, and selected ambiguous windows whose public pitch-set signatures are non-unique and label-diverse in the raw candidate pool. The participant-facing challenge explicitly bans external source-corpus lookup, public annotation search, audio fingerprinting, filename/timestamp matching, and isolated-string audio. `_analyze.py` includes exact-skeleton, pitch-signature, and media-fingerprint source-lookup stress tests so this tradeoff is measured rather than hidden.

Measured on the prepared split generated locally on 2026-07-04 after removing audio perturbations and tightening the grader: 359 train rows, 233 test rows, 592 prepared public WAV clips, and zero missing values in train, test, or answers. Exact public-skeleton uniqueness is 0.000, exact public-skeleton recovered source-track fraction is 0.000, pitch-signature uniqueness is 0.000, pitch-class signature uniqueness is 0.000, recovered source-track fraction is 0.000, and the source-lookup pitch-signature baseline scores 0.312181. The media-fingerprint-plus-raw-annotation stress baseline scores 0.952637 and its candidate top-1 source-window recovery is 1.000 versus a 0.141 random-candidate expectation; this is documented as a banned external lookup attack, not an allowed modeling baseline. The train pitch-prior baseline scores 0.308631, the simple audio random-forest baseline scores 0.310704, the sample submission scores 0.131483, and the perfect oracle scores exactly 1.000000.

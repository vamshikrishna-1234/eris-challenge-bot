# Source Verification

Checked on 2026-07-05.

## Gate Decision

PASS for a real-speech source pivot.

The earlier ODSS concept used an official published dataset, but ODSS contains generated TTS audio as part of the raw source. Per the user correction, this revision replaces ODSS with Mini LibriSpeech SLR31, an official OpenSLR subset of real human audiobook speech. The challenge title is now `Audiobook Reader Verification and Unknown-Reader Detection`, with no ODSS dependency and no generated-audio source.

## Primary Source

Official OpenSLR record:

```text
https://www.openslr.org/31/
```

Verified from the official page:

* Resource title: `Mini LibriSpeech ASR corpus`.
* Identifier: SLR31.
* Summary: subset of LibriSpeech corpus for regression testing.
* Category: Speech.
* License: CC BY 4.0.
* Official downloads include `dev-clean-2.tar.gz`, `train-clean-5.tar.gz`, and `md5sum.txt`.

Official source files selected:

| File | Size | MD5 | Use |
|---|---:|---|---|
| `dev-clean-2.tar.gz` | 126,046,265 bytes | `6d7ab67ac6a1d2c993d050e16d61080d` | held-out real readers |
| `train-clean-5.tar.gz` | 332,954,390 bytes | `5df7d4e78065366204ca6845bb08f490` | known-reader examples |

Total selected source size: 459,000,655 bytes, about 438 MiB.

## Import Procedure

Preferred platform source import:

```text
https://openslr.trmal.net/resources/31/dev-clean-2.tar.gz
https://openslr.trmal.net/resources/31/train-clean-5.tar.gz
```

Optional checksum source:

```text
https://openslr.trmal.net/resources/31/md5sum.txt
```

`prepare.py` accepts the official tarballs at the raw root or `raw/raw_upload/`, an extracted `LibriSpeech/` tree, or the platform's validator-visible top-level `dev-clean-2/` and `train-clean-5/` directories containing FLAC files and transcript files.

No custom processed raw archive is created. If URL import fails, manually upload the same unmodified official tarballs only.

## License And Attribution Handling

License: CC BY 4.0.

Required attribution:

```text
Mini LibriSpeech ASR corpus, OpenSLR SLR31.
Source: https://www.openslr.org/31/
License: Creative Commons Attribution 4.0 International.
LibriSpeech corpus creators and LibriVox source readers should be cited where appropriate.
```

Derived public clips are modified from source FLAC files by bounded selection, opaque filename assignment, 16 kHz WAV conversion, and mild speech-preserving de-identification. Attribution and CC BY 4.0 license notices should be retained for redistributed derived artifacts.

## Challenge Label Provenance

The task is open-set reader provenance from real speech:

* Readers with public training examples receive salted public provenance tokens such as `reader_000`.
* Public training is few-shot enrollment: each known reader contributes only a small number of labeled public clips.
* Hidden test contains held-out short utterances from those known readers and utterances from hard-selected readers absent from public training.
* Rows from absent readers are labeled `UNKNOWN`.
* Gold `known_reader_score` is `1.0` for known training readers and `0.0` for absent readers.

Public metadata is source-neutral and non-leaky: it contains only opaque ids, de-identified audio paths, duration, and coarse utterance-length bucket. It strips source subset, original path, speaker id, chapter id, transcript text, and raw row order. Public WAV filenames are salted opaque ids.

## Source Reversibility Controls

Mini LibriSpeech is public, so exact source reconstruction is a known risk. This build reduces public-source lookup risk by:

* removing original speaker, chapter, transcript, and source path metadata from public CSVs;
* writing public audio under salted opaque ids;
* converting to 16 kHz WAV;
* applying deterministic speech-preserving time, spectral, echo/compression, and dither changes in `prepare.py`;
* shortening public clips and using independent train/test channel rendering to reduce exact public-source matching while preserving reader evidence;
* including `_analyze.py` leakage scans for forbidden public columns, path tokens, id overlap, simple metadata baselines, and an optional raw-backed audio fingerprint probe.

The challenge form also explicitly forbids source lookup, fingerprint matching, transcript search, and commercial speaker-recognition APIs.

## Novelty Gate

Closest neighbors: LibriSpeech/OpenSLR ASR tasks and open-set speaker identification or speaker verification benchmarks.

This challenge is not a LibriSpeech ASR clone:

* Transcripts are not public inputs.
* The output is an open-set provenance JSON, not a word transcript.
* The unknown-reader class is required, so closed-set speaker classification is insufficient.
* The prepared challenge is few-shot and hard-open-set: known readers have only a few enrollment clips, test clips are short and channel-shifted, and unknown readers are selected to be acoustically closer to the known-reader cohort.
* The metric combines known-vs-unknown ranking, macro-F1 over reader tokens plus `UNKNOWN`, same-reader consistency, worst-group robustness, and calibration.
* Public metadata and filenames strip source ids and original chapter/speaker structure.

Novelty judgment: acceptable, about 6/10. It reuses real LibriSpeech audio and overlaps with speaker recognition, so it belongs in the recombined band. The task differs materially from canonical LibriSpeech ASR and ordinary closed-set speaker ID by requiring de-identified open-set reader provenance with explicit unknown decisions and calibrated robustness.

## ODSS Decision

ODSS is no longer used. It was removed because, while official and licensed, its raw source includes generated TTS audio. The revised build uses Mini LibriSpeech real human speech only.

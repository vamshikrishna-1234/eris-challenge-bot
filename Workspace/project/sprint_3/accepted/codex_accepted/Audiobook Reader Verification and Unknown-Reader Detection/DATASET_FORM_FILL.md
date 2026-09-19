# Dataset creation form - fill-in

## Dataset name

```text
Mini LibriSpeech Real Audiobook Speech Archives
```

## Overview

Mini LibriSpeech is an official OpenSLR subset of the LibriSpeech ASR corpus created for regression testing. It contains real read audiobook speech, FLAC audio files, and per-chapter transcript text files. The selected official OpenSLR URL imports are auto-extracted by the platform, so the validator-visible dataset tree contains the two top-level subset directories shown below.

## File structure

```text
dev-clean-2/                               extracted Mini LibriSpeech subset
dev-clean-2/<speaker>/<chapter>/*.flac     real speech audio
dev-clean-2/<speaker>/<chapter>/*.trans.txt
train-clean-5/                             extracted Mini LibriSpeech subset
train-clean-5/<speaker>/<chapter>/*.flac   real speech audio
train-clean-5/<speaker>/<chapter>/*.trans.txt
```

* `dev-clean-2/` is the extracted Mini LibriSpeech development-clean subset.
* `train-clean-5/` is the extracted Mini LibriSpeech train-clean subset.
* Each subset directory contains real audiobook FLAC files organized by speaker and chapter.
* `*.trans.txt` files contain utterance ids and transcript text for each chapter directory.

## FLAC path fields

`subset` (string): top-level subset folder such as `dev-clean-2` or `train-clean-5`.

`speaker` (string/integer): LibriSpeech speaker identifier from the directory path.

`chapter` (string/integer): LibriSpeech chapter identifier from the directory path.

`filename` (string): FLAC filename, usually `<speaker>-<chapter>-<utterance>.flac`.

## .trans.txt columns

`utterance_id` (string): utterance id matching a FLAC filename stem.

`transcript_text` (string): transcript text for the read audiobook utterance.

## License

Creative Commons Attribution 4.0 International (CC BY 4.0), matching the OpenSLR Mini LibriSpeech page.

## Source

Official OpenSLR record: https://www.openslr.org/31/

Official source URLs imported by the platform:

```text
https://openslr.trmal.net/resources/31/dev-clean-2.tar.gz
https://openslr.trmal.net/resources/31/train-clean-5.tar.gz
https://openslr.trmal.net/resources/31/md5sum.txt
```

## Notes

* The `dev-clean-2` source download is 126,046,265 bytes with MD5 `6d7ab67ac6a1d2c993d050e16d61080d`.
* The `train-clean-5` source download is 332,954,390 bytes with MD5 `5df7d4e78065366204ca6845bb08f490`.
* The selected official source archives total 459,000,655 bytes, about 438 MiB, comfortably below a 1 GB source budget.
* The corpus consists of real human audiobook speech rather than locally generated audio.

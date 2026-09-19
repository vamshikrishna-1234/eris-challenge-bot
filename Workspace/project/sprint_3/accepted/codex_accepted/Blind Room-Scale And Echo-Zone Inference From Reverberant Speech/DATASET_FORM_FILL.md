# Dataset creation form - fill-in

## Dataset name

```text
ACE Reverberant Speech Room-Scale And Echo-Zone Profiles
```

## Overview

This dataset is derived from the official Acoustic Characterization of Environments (ACE) Corpus. It uses measured single-channel room impulse responses, matched room noise, anechoic speech utterances, official T60/DRR measurements, room dimensions, and source/microphone condition metadata.

The raw source files are official Zenodo archives and official ACE reference documents imported unmodified. The prepared public view consists of short 16 kHz mono reverberant speech clips with opaque ids and bucketed acoustic-environment labels for training rows.

## File structure

```text
ACE_Corpus_RIRN_Single.tbz2       official single-channel RIR and noise archive
ACE_Corpus_Speech.tbz2            official anechoic speech archive
ACE_Corpus_Data.tbz2              official T60/DRR metadata archive
ACE_Corpus_instructions_v01.pdf   official ACE corpus usage and organization notes
ACE_Corpus_Microphone_arrangements_v02.pdf
                                    official microphone/source arrangement reference

Data/
  20150225T195903_test_t60_DRR_measurement_results.csv
Speech/
  *.wav                           anechoic speech utterances
Single/
  .../*.wav                       single-channel RIR and room-noise WAV files
```

The platform source-file area should contain the three official `.tbz2` archives plus the two official ACE PDF reference documents listed above. `ACE_Corpus_instructions_v01.pdf` documents the ACE corpus package organization and usage notes. `ACE_Corpus_Microphone_arrangements_v02.pdf` documents the microphone-array and source arrangement reference material used to interpret the room/acoustic-condition metadata. If archives are extracted before processing, the `Data/`, `Speech/`, and `Single/` folders above are the expected official content layout. No custom raw upload zip is part of this dataset.

## Official metadata columns

`20150225T195903_test_t60_DRR_measurement_results.csv` contains one row per measured room/acoustic condition, channel, and frequency band.

- `Test ID:` (integer): row identifier in the official measurement table.
- `Ver:` (integer): official metadata version.
- `fs:` (integer): measurement sample rate.
- `Room:` (string/integer): ACE room identifier such as `502`, `803`, `611`, `503`, `403a`, `508`, or `EE_lobby`.
- `Session ID:` (integer): ACE recording-session/source-microphone condition id.
- `Mic Pos:` (integer): official microphone-position code.
- `Source Pos:` (integer): official source-position code.
- `Config:` (string): microphone configuration used for the measurement, such as `Crucif` or `Lin8Ch`.
- `Rec Type:` (string): recording type, with `IR` for impulse-response measurements.
- `RIR:` (string): official RIR basename.
- `Freq band:` (integer/string): official frequency-band index.
- `Centre freq:` (float): center frequency for the band.
- `Channel:` (integer): microphone channel.
- `DRR:` (float): direct-to-reverberant ratio for that band/channel.
- `DRR Mean (Ch):` (float): channel-mean DRR for that band.
- `T60 AHM:` (float): T60 estimate for that band/channel.
- `T30 ISO:` (float): ISO T30 estimate.
- `T20 ISO:` (float): ISO T20 estimate.
- `T60 AHM Mean (Ch):` (float): channel-mean T60 estimate for that band.
- `T30 ISO Mean (Ch):` (float): channel-mean T30 estimate.
- `T20 ISO Mean (Ch):` (float): channel-mean T20 estimate.
- `ISO AHM Ints:` (string/float): official interval metadata.
- `FB DRR :` (float): fullband DRR for the row.
- `FB DRR Mean (Ch):` (float): fullband mean DRR by channel.
- `FB T60 AHM:` (float): fullband T60 estimate.
- `FB T30 ISO:` (float): fullband T30 estimate.
- `FB T20 ISO:` (float): fullband T20 estimate.
- `FB T60 AHM Mean (Ch):` (float): fullband mean T60 by channel.
- `FB T30 ISO Mean (Ch):` (float): fullband mean T30 by channel.
- `FB T20 ISO Mean (Ch):` (float): fullband mean T20 by channel.
- `DRR direct +:` (float): official DRR direct-window metadata.
- `DRR direct -:` (float): official DRR direct-window metadata.

## Raw audio naming convention

Official speech WAV files are named by ACE talker and utterance code inside the speech archive. Official RIR and noise WAV files are organized by single-channel acoustic condition and include room/configuration/noise tokens in the source filenames. Those raw identifiers are source metadata only; prepared public filenames use salted opaque ids.

## Prepared public columns

`public/train.csv` columns:

- `sample_id` (string): salted opaque prepared clip id.
- `audio_path` (string): relative path to a prepared 16 kHz mono WAV clip.
- `prompt` (string): generic prompt describing the acoustic-profile task.
- `room_volume_bucket` (string): bucketed room scale, one of `small`, `medium`, `large`, `very_large`.
- `rt60_bucket` (string): bucketed reverberation, one of `dry`, `moderate`, `reverberant`, `very_reverberant`.
- `source_mic_distance_bucket` (string): bucketed source-microphone distance, one of `near`, `mid`, `far`, `unknown_or_uncertain`.
- `echo_zone` (string): acoustic-zone category, one of `direct_dominant`, `balanced`, `reverberant_dominant`, `noisy_uncertain`.
- `confidence` (float): row-level label reliability value in `[0, 1]`.

`public/test.csv` columns:

- `sample_id` (string): salted opaque prepared clip id.
- `audio_path` (string): relative path to a prepared 16 kHz mono WAV clip.
- `prompt` (string): generic prompt describing the acoustic-profile task.

`public/sample_submission.csv` columns:

- `sample_id` (string): salted opaque prepared clip id.
- `room_volume_bucket` (string): placeholder room-scale bucket.
- `rt60_bucket` (string): placeholder reverberation bucket.
- `source_mic_distance_bucket` (string): placeholder distance bucket.
- `echo_zone` (string): placeholder echo-zone category.
- `confidence` (float): placeholder confidence value in `[0, 1]`.

## License

Creative Commons Attribution 4.0 International (CC BY 4.0), matching the official ACE Corpus Zenodo record. Attribution to the ACE Corpus creators and the official ACE corpus publication is required.

## Source

Official Zenodo record: https://zenodo.org/records/6257551

Selected source files:

- `ACE_Corpus_RIRN_Single.tbz2`
- `ACE_Corpus_Speech.tbz2`
- `ACE_Corpus_Data.tbz2`
- `ACE_Corpus_instructions_v01.pdf`
- `ACE_Corpus_Microphone_arrangements_v02.pdf`

## Notes

- The selected official source files total about 544 MiB as displayed by the platform upload view, below the 1 GB source-data budget.
- Prepared public audio is 16 kHz mono PCM WAV, uses salted filenames that do not reveal source room, RIR, speech, source, microphone, or noise identifiers, and includes mild speech-preserving perturbations to reduce direct source-audio matching.
- The source corpus contains measured real room acoustics rather than a synthetic renderer.
- Any tiny local fixture material is only for script validation and is not part of the dataset source.

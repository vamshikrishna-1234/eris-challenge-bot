# Dataset creation form - fill-in

**Platform status:** Draft

## Dataset name

```
GuitarSet Mono Microphone Audio And JAMS Annotations
```

## Overview

This dataset consists of the official GuitarSet annotations and mono microphone audio from Zenodo record 3371780. GuitarSet contains real acoustic guitar performances with time-aligned JAMS annotations, including note events, pitch contours, chords, beats, keys, string/fret positions, and performance metadata. The dataset endpoint should contain the official Zenodo URL-imported source contents as `annotation/` and `audio_mono-mic/` directories, not a custom archive and not precomputed public/private splits.

## File structure

```
annotation/           extracted official JAMS annotations
audio_mono-mic/       extracted official mono microphone WAV audio
```

* `annotation/` contains the official `.jams` annotation files, one annotation file per performance.
* `audio_mono-mic/` contains the official mono microphone `.wav` recordings aligned to the annotations.
* These directories are the platform-visible extracted contents of the official Zenodo URL imports.

## Features

Raw JAMS annotation objects include the following important fields:

`file_metadata.title` (string): recording title from the annotation file.

`file_metadata.duration` (float): performance duration in seconds.

`annotations[].namespace` (string): JAMS annotation namespace such as `note_midi`, `pitch_contour`, `chord`, `beat_position`, `tempo`, or `key_mode`.

`annotations[].annotation_metadata.data_source` (string): per-string source index for string-level note and pitch annotations.

`annotations[].data[].time` (float): annotation onset time in seconds.

`annotations[].data[].duration` (float): annotation duration in seconds.

`annotations[].data[].value` (number, string, or object): namespace-specific value, such as MIDI pitch, chord label, beat position, tempo, or key.

`annotations[].data[].confidence` (number or null): confidence value when supplied by the annotation.

Raw WAV audio files include the following properties:

`wav_samples` (PCM audio): mono microphone waveform samples for each guitar performance.

`sample_rate` (integer): WAV sampling rate supplied by the source file.

`duration` (float): audio duration aligned with the corresponding JAMS annotation.

Raw filenames follow GuitarSet's source naming convention:

`player` (string): two-digit performer code embedded in the source filename.

`excerpt` (string): musical excerpt/style/progression token embedded in the source filename.

`tempo` (integer-like string): tempo token embedded in the source filename.

`key` (string): musical key token embedded in the source filename.

`take_type` (string): source take type, usually `comp` or `solo`.

## License

Creative Commons Attribution 4.0 International (CC BY 4.0). Attribution to the GuitarSet creators and a link to the license must be retained, and changes must be indicated when derived files are distributed.

## Source

Official Zenodo record: https://zenodo.org/records/3371780

Official source URLs:

```
https://zenodo.org/api/records/3371780/files/annotation.zip/content
https://zenodo.org/api/records/3371780/files/audio_mono-mic.zip/content
```

Recommended citation:

```text
Q. Xi, R. Bittner, J. Pauwels, X. Ye, and J. P. Bello, "GuitarSet: A Dataset for Guitar Transcription", in 19th International Society for Music Information Retrieval Conference, Paris, France, Sept. 2018.
```

## Notes

* The official annotation source import is 39,132,574 bytes before platform extraction.
* The official mono microphone audio source import is 656,927,981 bytes before platform extraction.
* Total selected raw source import size before platform extraction is 696,060,555 bytes, below 1 GB.
* The larger hexaphonic pickup archives are not part of this dataset upload.
* The source files are real recorded performances and annotations, not synthetic generated data.

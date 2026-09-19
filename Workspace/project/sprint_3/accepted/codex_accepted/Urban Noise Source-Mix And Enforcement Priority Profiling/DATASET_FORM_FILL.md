# Dataset creation form - fill-in

## Dataset name

```text
SONYC-UST Urban Acoustic Sensor Audio And Source Annotations
```

## Overview

This dataset is a bounded official-source subset of SONYC Urban Sound Tagging version 2.3.0 from Zenodo record 3966543. It contains the official annotation CSV, official machine-readable taxonomy, official README, and one official audio tarball with real 10-second New York City urban acoustic sensor recordings. The raw source files are imported unchanged from Zenodo, either as separate official URLs or as one convenience zip containing only those official files, and do not contain prepared train/test splits or derived challenge clips.

## File structure

```text
annotations.csv             official SONYC-UST annotation table
dcase-ust-taxonomy.yaml     official fine/coarse label taxonomy
README.md                   official dataset README and license notes
audio-0.tar.gz              official selected audio shard
audio-0/*.wav               possible extracted audio-shard layout
sonyc_ust_official_selected_source_files.zip
                            optional unchanged-file upload bundle
```

* `annotations.csv` contains volunteer annotations, SONYC-team annotations, verified ground-truth rows, source filenames, coarse location/time metadata, fine/coarse presence fields, and volunteer proximity fields.
* `dcase-ust-taxonomy.yaml` defines the 23 fine labels grouped into 8 coarse source families.
* `README.md` documents version 2.3, source provenance, label taxonomy, column meanings, conditions of use, and CC BY 4.0 license.
* `audio-0.tar.gz` is the selected official Zenodo audio shard and contains 1000 mono 48 kHz 16-bit PCM WAV recordings under an `audio-0/` directory.
* If the platform extracts the archive, `audio-0/*.wav` is the expected validator-visible extracted layout for those source recordings.
* `sonyc_ust_official_selected_source_files.zip` is an optional single-file upload bundle containing only `annotations.csv`, `dcase-ust-taxonomy.yaml`, `README.md`, and `audio-0.tar.gz` unchanged at the zip root.

## annotations.csv columns

`split` (string): official source split label.

`sensor_id` (integer): official acoustic sensor identifier.

`audio_filename` (string): official source WAV filename.

`annotator_id` (integer): anonymous annotator id; positive values are volunteer annotators, negative values are SONYC team annotators, and `0` is verified ground truth.

`borough` (integer): coarse NYC borough code.

`block` (integer): coarse city-block code.

`latitude` (float): block-level latitude coordinate.

`longitude` (float): block-level longitude coordinate.

`year` (integer): recording year.

`week` (integer): week of year.

`day` (integer): day of week with Monday as 0.

`hour` (integer): hour of day.

Fine presence columns (integer `1`, `0`, or `-1`): `1-1_small-sounding-engine_presence`, `1-2_medium-sounding-engine_presence`, `1-3_large-sounding-engine_presence`, `1-X_engine-of-uncertain-size_presence`, `2-1_rock-drill_presence`, `2-2_jackhammer_presence`, `2-3_hoe-ram_presence`, `2-4_pile-driver_presence`, `2-X_other-unknown-impact-machinery_presence`, `3-1_non-machinery-impact_presence`, `4-1_chainsaw_presence`, `4-2_small-medium-rotating-saw_presence`, `4-3_large-rotating-saw_presence`, `4-X_other-unknown-powered-saw_presence`, `5-1_car-horn_presence`, `5-2_car-alarm_presence`, `5-3_siren_presence`, `5-4_reverse-beeper_presence`, `5-X_other-unknown-alert-signal_presence`, `6-1_stationary-music_presence`, `6-2_mobile-music_presence`, `6-3_ice-cream-truck_presence`, `6-X_music-from-uncertain-source_presence`, `7-1_person-or-small-group-talking_presence`, `7-2_person-or-small-group-shouting_presence`, `7-3_large-crowd_presence`, `7-4_amplified-speech_presence`, `7-X_other-unknown-human-voice_presence`, and `8-1_dog-barking-whining_presence`.

Fine proximity columns (string): `1-1_small-sounding-engine_proximity`, `1-2_medium-sounding-engine_proximity`, `1-3_large-sounding-engine_proximity`, `1-X_engine-of-uncertain-size_proximity`, `2-1_rock-drill_proximity`, `2-2_jackhammer_proximity`, `2-3_hoe-ram_proximity`, `2-4_pile-driver_proximity`, `2-X_other-unknown-impact-machinery_proximity`, `3-1_non-machinery-impact_proximity`, `4-1_chainsaw_proximity`, `4-2_small-medium-rotating-saw_proximity`, `4-3_large-rotating-saw_proximity`, `4-X_other-unknown-powered-saw_proximity`, `5-1_car-horn_proximity`, `5-2_car-alarm_proximity`, `5-3_siren_proximity`, `5-4_reverse-beeper_proximity`, `5-X_other-unknown-alert-signal_proximity`, `6-1_stationary-music_proximity`, `6-2_mobile-music_proximity`, `6-3_ice-cream-truck_proximity`, `6-X_music-from-uncertain-source_proximity`, `7-1_person-or-small-group-talking_proximity`, `7-2_person-or-small-group-shouting_proximity`, `7-3_large-crowd_proximity`, `7-4_amplified-speech_proximity`, `7-X_other-unknown-human-voice_proximity`, and `8-1_dog-barking-whining_proximity`. Values are `near`, `far`, `notsure`, or `-1`.

Coarse presence columns (integer `1`, `0`, or `-1`): `1_engine_presence`, `2_machinery-impact_presence`, `3_non-machinery-impact_presence`, `4_powered-saw_presence`, `5_alert-signal_presence`, `6_music_presence`, `7_human-voice_presence`, and `8_dog_presence`.

## dcase-ust-taxonomy.yaml contents

`fine` (mapping): nested mapping from coarse id and fine id to fine label names.

`coarse` (mapping): mapping from coarse id to coarse label names: engine, machinery-impact, non-machinery-impact, powered-saw, alert-signal, music, human-voice, and dog.

## Audio files

Each WAV in `audio-0.tar.gz` is an official 10-second real urban acoustic sensor recording. The inspected files are mono, 48 kHz, 16-bit PCM WAV with 480,000 samples per clip.

## License

Creative Commons Attribution 4.0 International (CC BY 4.0). The Zenodo metadata lists license id `cc-by-4.0`, and the official README states that SONYC-UST is offered under CC BY 4.0.

## Source

Official Zenodo record: https://zenodo.org/records/3966543

Official API record: https://zenodo.org/api/records/3966543

Official selected source URLs:

```text
https://zenodo.org/api/records/3966543/files/annotations.csv/content
https://zenodo.org/api/records/3966543/files/dcase-ust-taxonomy.yaml/content
https://zenodo.org/api/records/3966543/files/README.md/content
https://zenodo.org/api/records/3966543/files/audio-0.tar.gz/content
```

Recommended citation: Cartwright, M., Cramer, J., Mendez, A.E.M., Wang, Y., Wu, H., Lostanlen, V., Fuentes, M., Dove, G., Mydlarz, C., Salamon, J., Nov, O., Bello, J.P. SONYC-UST-V2: An Urban Sound Tagging Dataset with Spatiotemporal Context. Proceedings of the Workshop on Detection and Classification of Acoustic Scenes and Events (DCASE), 2020.

## Notes

* The selected official source files total 736,118,800 bytes, about 736.1 MB decimal, before platform extraction.
* The optional upload bundle `sonyc_ust_official_selected_source_files.zip` is 736,119,248 bytes and contains only the same four official files unchanged.
* The full Zenodo record is about 13.3 GB and should not be fully imported for this dataset.
* `audio-0.tar.gz` has official MD5 `bbb4dbae7d2e58e18d24878b9ee1eb51` and contains 1000 WAV files.
* The source files are real recorded urban acoustic sensor audio and annotations, not synthetic generated data.
* Do not upload a processed raw zip or raw_upload zip for this dataset. The optional convenience zip is only a transfer bundle of official source files, with no prepared public/private files.

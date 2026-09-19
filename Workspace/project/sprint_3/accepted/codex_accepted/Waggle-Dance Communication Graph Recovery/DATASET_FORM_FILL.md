# Dataset creation form - fill-in

## Dataset name

```text
Honey-Bee Waggle-Dance Trajectories, Dance Events, and Follower Interactions
```

## Overview

This dataset is a clean raw subset of the official Zenodo record `Data used in Machine learning reveals the waggle drift's role in the honey bee dance communication system`. It contains official 2019 honey-bee dance-event CSVs, waggle-phase detections, follower/attendance interactions, manually annotated per-frame behavior labels, feeder experiment provenance, and unchanged date-level track CSV members extracted from the official `Berlin2019_tracks.zip` archive. The track files contain real observation-hive detections for many individually tracked bees with camera side, time, track identifiers, bee identifiers, confidence, hive-plane position, and body orientation.

## File structure

```text
Berlin2019_dances.csv
Berlin2019_dances_with_manually_verified_times.csv
Berlin2019_feeder_experiment_log.csv
Berlin2019_followers.csv
Berlin2019_waggle_phases.csv
Berlin2019_dance_classifier_labels.csv
Berlin2019_tracks/
Berlin2019_tracks/2019-08-25.csv
Berlin2019_tracks/2019-08-27.csv
Berlin2019_tracks/2019-08-28.csv
Berlin2019_tracks/2019-08-29.csv
Berlin2019_tracks/2019-09-02.csv
Berlin2019_tracks/2019-09-05.csv
Berlin2019_tracks/2019-09-10.csv
Berlin2019_tracks/2019-09-11.csv
SOURCE_MANIFEST.csv
CHECKSUMS_SHA256.txt
LICENSE.txt
EXTRACTION_NOTES.md
```

* `Berlin2019_dances.csv`: official automatic dance detections.
* `Berlin2019_dances_with_manually_verified_times.csv`: official manually verified timing sample.
* `Berlin2019_feeder_experiment_log.csv`: official feeder experiment provenance.
* `Berlin2019_followers.csv`: official attendance and follower interactions.
* `Berlin2019_waggle_phases.csv`: official waggle-phase detections.
* `Berlin2019_dance_classifier_labels.csv`: official manually annotated per-frame behavior labels.
* `Berlin2019_tracks/*.csv`: unchanged date-level CSV members from the official track ZIP.
* `SOURCE_MANIFEST.csv`: source URL, checksum, and extraction notes for each included raw file.
* `CHECKSUMS_SHA256.txt`: SHA-256 checksums for the package contents.
* `LICENSE.txt`: source attribution and CC BY 4.0 license statement.
* `EXTRACTION_NOTES.md`: notes describing the clean raw subset extraction.

## Berlin2019_dances.csv columns

* `dancer_id` (integer): original tracked individual bee identifier.
* `dance_id` (integer): original unique dance identifier.
* `ts_from` (ISO timestamp): automatic dance start time.
* `ts_to` (ISO timestamp): automatic dance end time.
* `cam_id` (integer): camera side identifier, `0` or `1`.
* `median_x` (float): median dance x position in hive-plane millimeters.
* `median_y` (float): median dance y position in hive-plane millimeters.
* `feeder_cam_id` (float): feeder camera identifier when available.

## Berlin2019_dances_with_manually_verified_times.csv columns

* `dance_id` (integer): original unique dance identifier.
* `dancer_id` (integer): original tracked individual bee identifier.
* `cam_id` (integer): camera side identifier, `0` or `1`.
* `feeder_cam_id` (float): feeder camera identifier when available.
* `dance_start` (ISO timestamp): manually verified dance start time.
* `dance_end` (ISO timestamp): manually verified dance end time.

## Berlin2019_followers.csv columns

* `dance_id` (integer): original unique dance identifier.
* `follower_id` (integer): original tracked individual bee identifier.
* `ts_from` (ISO timestamp): interaction start time.
* `ts_to` (ISO timestamp): interaction end time.
* `label` (string): `attendance` or `follower`.
* `cam_id` (integer): camera side identifier, `0` or `1`.

## Berlin2019_waggle_phases.csv columns

* `timestamp` (ISO timestamp): waggle-phase detection time.
* `cam_id` (integer): camera side identifier, `0` or `1`.
* `x_median` (float): median waggle-phase x position.
* `y_median` (float): median waggle-phase y position.
* `waggle_angle` (float): body orientation angle in radians.

## Berlin2019_dance_classifier_labels.csv columns

* `timestamp` (ISO timestamp): annotated individual-frame time.
* `frame_id` (integer): original video-frame identifier.
* `bee_id` (integer): original tracked individual bee identifier.
* `label` (string): one of `nothing`, `waggle`, or `follower`.

## Berlin2019_feeder_experiment_log.csv columns

* `date` (date): experiment date.
* `feeder_cam_id` (integer): feeder camera identifier.
* `coordinates` (string): feeder longitude and latitude when available.
* `time_opened` (ISO timestamp): feeder opening time.
* `time_closed` (ISO timestamp): feeder closing time.
* `sucrose_solution` (string): sucrose solution description.

## Berlin2019_tracks/*.csv columns

* `cam_id` (integer): camera side identifier, `0` or `1`.
* `timestamp` (ISO timestamp): detection timestamp.
* `frame_id` (integer): original video-frame identifier.
* `track_id` (integer): original short-track identifier.
* `bee_id` (integer): original tracked individual bee identifier.
* `bee_id_confidence` (float): tracking-system confidence in `[0,1]`.
* `x_pos_hive` (float): hive-plane x position in millimeters.
* `y_pos_hive` (float): hive-plane y position in millimeters.
* `orientation_hive` (float): thorax orientation in radians when available.

## SOURCE_MANIFEST.csv columns

* `path` (string): package-relative raw file path.
* `source_url` (string): official Zenodo URL or official archive URL.
* `source_file` (string): official source filename.
* `source_checksum` (string): official Zenodo checksum when available.
* `source_size_bytes` (integer): official file or archive-member size.
* `sha256` (string): SHA-256 checksum of the packaged file.
* `note` (string): short source or extraction note.

## License

Creative Commons Attribution 4.0 International (`CC BY 4.0`). This license permits copying, redistribution, adaptation, and commercial use when attribution is provided and license terms are preserved.

## Source

Zenodo record: `https://zenodo.org/records/7928121`

DOI: `10.5281/zenodo.7928121`

Record title: `Data used in Machine learning reveals the waggle drift's role in the honey bee dance communication system`

Creators: David M. Dormagen, Benjamin Wild, Fernando Wario, and Tim Landgraf.

## Notes

* The included `Berlin2019_tracks/*.csv` files are unchanged date-level members extracted from the official `Berlin2019_tracks.zip` archive.
* The package excludes the full 1.4 GB track ZIP and the 2021 ground-truth ZIP to keep the upload bounded.
* The clean source package contains raw source files and provenance files only.
* Approximate package size is expected to stay below 1 GB when zipped with deflate compression.

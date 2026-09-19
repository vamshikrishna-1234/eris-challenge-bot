# Dataset creation form - fill-in

## Dataset name

```
NOAA GOES-16 GLM Level-2 Lightning Detection Hierarchies
```

## Overview

Five untouched NOAA GOES-16 Geostationary Lightning Mapper Level-2 Lightning Detections NetCDF4 files. The raw product contains the official event-to-group-to-flash hierarchy and physical detection measurements. The files are imported directly from NOAA's public Open Data Dissemination Program. They are not renamed, subset, converted, or preprocessed before upload.

The five objects total 2,901,827 bytes and contain 81,527 events, 33,715 groups, and 2,514 flashes. File hashes, counts, and the detailed source verification are recorded in `SOURCE_VERIFICATION.md`.

## File structure

```
*.nc    five untouched official GLM-L2-LCFA NetCDF4 objects
```

The platform may place URL imports in nested directories; keep the original object basenames and byte contents unchanged.

## Features and columns

`number_of_events` (dimension): number of detected optical lightning events in the object.

`number_of_groups` (dimension): number of native groups in the object.

`number_of_flashes` (dimension): number of native flashes in the object.

`event_id` (integer): native event identifier.

`event_parent_group_id` (integer): native link from event to parent group.

`event_time_offset` (time offset): event time relative to the product epoch.

`event_lat`, `event_lon` (degrees): native earth location of the optical event.

`event_energy` (energy): native optical event energy.

`group_id` (integer): native group identifier.

`group_parent_flash_id` (integer): native link from group to parent flash.

`group_time_offset`, `group_frame_time_offset` (time offsets): native group timing.

`group_lat`, `group_lon`, `group_area`, `group_energy`, `group_quality_flag`: native group measurements and quality metadata.

`flash_id` (integer): native flash identifier.

`flash_time_offset_of_first_event`, `flash_time_offset_of_last_event` (time offsets): native flash timing.

`flash_lat`, `flash_lon`, `flash_area`, `flash_energy`, `flash_quality_flag`: native flash measurements and quality metadata.

Global attributes describe the GOES project, GOES-East orbital slot, GLM instrument, NASA Level-2 processing level, creation time, production site, calibration lookup tables, and product title.

## License

CC0 1.0 (Public Domain)

## Source

NOAA GOES-16 Geostationary Lightning Mapper Level-2 Lightning Detections product (`GLM-L2-LCFA`), accessed through NOAA Open Data on AWS.

Source URL: https://registry.opendata.aws/noaa-goes/

## Notes

- The included upload archive contains only five byte-identical official NOAA NetCDF files plus an attribution note.
- Do not rename, subset, convert, or alter the official NetCDF objects before upload.
- Credit NOAA and do not imply endorsement.

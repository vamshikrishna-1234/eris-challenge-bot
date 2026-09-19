# Dataset creation form - fill-in

## Dataset name

```text
MEVA Activity and Actor-Type Annotated Video Subset
```

## Overview

This corpus is a bounded, untouched-file subset of the Multiview Extended Video with Activities (MEVA) project from Kitware Inc. and IARPA. It contains 21 official five-minute `.r13.avi` videos, their official activity and actor-type YAML annotations, and the project documentation needed to interpret those annotations. The annotations describe frame spans, activity names, actor identifiers, actor types, and the official activity vocabulary.

## File structure

The uploaded raw file is `OFFICIAL_RAW_FILES_ONLY.zip`. After the platform extracts that untouched transport package, the validator-visible top-level tree is:

```text
annotation/                         official activity/type annotations
documents/                          official vocabulary and PDFs
drops-123-r13/                       21 official videos
LICENSE                              CC BY 4.0 license text
README.md                            official project README
```

- `drops-123-r13/` preserves the official date/hour directory layout and video filenames.
- `annotation/DIVA-phase-2/MEVA/kitware/` preserves one `activities.yml` and one `types.yml` per video.
- `documents/` contains `activity-names.txt`, the KPF specification, and MEVA annotation definitions.
- `LICENSE` and `README.md` are the unmodified project files.

## Features

The corpus has no tabular scene file; labels are in the official YAML packets.

- `act.id2` (integer): official activity identifier.
- `act.act2` (mapping): official activity-name confidence map.
- `act.timespan[].tsr0` (two integers): inclusive video-frame start and end.
- `act.actors[].id1` (integer): official actor identifier referenced by an activity.
- `types.id1` (integer): actor identifier defined in a type packet.
- `types.cset3` (mapping): actor-type confidence map.
- `video basename` (string): official file basename used only for deterministic annotation linkage.

The project vocabulary associates names such as `person_opens_vehicle_door` with activity and actor concepts. Actor-type packets provide the official type values. All listed fields are preserved exactly as distributed by MEVA.

## License

Creative Commons Attribution 4.0 International (CC BY 4.0). Redistribution and commercial reuse are permitted with attribution to Kitware Inc. and IARPA. The included `LICENSE` file is the authoritative copy.

## Source

Official MEVA repository and public video bucket:

- https://gitlab.kitware.com/meva/meva-data-repo (pinned commit `421841a75577b697c314e952e585aecbb1b99e17`)
- https://mevadata-public-01.s3.amazonaws.com/

The retained raw transport archive contains only untouched files downloaded from those official locations. No third-party media, generated labels, extracted clips, or derived assets are included.

## Notes

- 21 videos and 70 total official files are retained.
- The uncompressed official tree is 970,257,026 bytes; the transport archive is 969,981,917 bytes.
- Directory names and filenames are preserved so that official annotation linkage remains reproducible.

# Dataset form fill — Finnish Railway Planned Timetable And Network Corpus

## Title

Finnish Railway Planned Timetable And Network Corpus

## Description

A snapshot corpus of the Finnish national railway network and its published operating plan, taken
directly from the Fintraffic Digitraffic open railway API. It contains the national station register,
the official delay-cause category register, and ten complete daily train files spread across the
2026 timetable year. Every byte is the unmodified API response.

Each daily train file lists every train movement planned and run on that date, with its train number,
operator, category (Long-distance, Commuter, Cargo, Shunting, Locomotive, On-track machines, Test
drive), service type, and an ordered list of timetable rows. Each timetable row is one arrival at or
departure from one station, with the scheduled time, the commercial track, and stopping flags.

Scale: 563 stations, 47 official delay-cause categories, ten daily files with roughly 1,700-1,900
train movements each and 140 timetable rows for a long cross-country service.

### File structure (validator-visible after rebuild)

| Item | Description |
|---|---|
| stations.json | National station register |
| cause-category-codes.json | Official delay-cause categories |
| trains_YYYY-MM-DD.json | All train movements for one date |
| LICENSE.txt | CC BY 4.0 text and attribution |
| PROVENANCE.txt | Endpoints, dates, checksums, modification notice |

Ten daily files are included: 2026-01-13, 2026-02-11, 2026-03-10, 2026-04-14, 2026-05-12, 2026-06-16,
2026-08-18, 2026-09-15, 2026-09-16, 2026-09-17.

### stations.json — fields

| Field | Type | Meaning |
|---|---|---|
| stationShortCode | string | Station code used in train files |
| stationName | string | Station name |
| stationUICCode | integer | UIC station number |
| latitude | float | Decimal degrees |
| longitude | float | Decimal degrees |
| type | string | STATION, STOPPING_POINT or TURNOUT_IN_THE_OPEN_LINE |
| passengerTraffic | boolean | Open to passengers |
| countryCode | string | Country of the station |

### cause-category-codes.json — fields

| Field | Type | Meaning |
|---|---|---|
| detailedCategoryCode | string | Official cause code |
| detailedCategoryName | string | Cause description (Finnish) |
| id | integer | Register row id |
| validFrom | date | First day the code applies |

### trains_YYYY-MM-DD.json — train fields

| Field | Type | Meaning |
|---|---|---|
| trainNumber | integer | Train number on that date |
| departureDate | date | Operating date |
| operatorShortCode | string | Operator |
| trainCategory | string | Long-distance, Commuter, Cargo, ... |
| trainType | string | Service type code (IC, HL, T, ...) |
| commuterLineID | string | Commuter line letter where applicable |
| cancelled | boolean | Whole train cancelled |
| timetableType | string | REGULAR or ADHOC |
| timeTableRows | list | Ordered arrival and departure rows |

### trains_YYYY-MM-DD.json — timetable row fields

| Field | Type | Meaning |
|---|---|---|
| stationShortCode | string | Station of this row |
| type | string | ARRIVAL or DEPARTURE |
| scheduledTime | datetime | Planned time, UTC |
| actualTime | datetime | Recorded time, UTC, when reported |
| differenceInMinutes | integer | Recorded minus planned, when reported |
| causes | list | Official delay-cause records attached to the row |
| commercialTrack | string | Platform or track number |
| commercialStop | boolean | Booked commercial stop |
| trainStopping | boolean | Train physically stops |
| cancelled | boolean | This stop cancelled |

## License

Creative Commons Attribution 4.0 International (CC BY 4.0).

Required attribution, reproduced in `LICENSE.txt` inside the archive:

> Source: Fintraffic / digitraffic.fi, license CC 4.0 BY

## Source

https://rata.digitraffic.fi/api/v1/

## Notes

- The archive is flat: members are the JSON files and the two text files directly, with no wrapper
  directory. Total ~200 MB uncompressed.
- Files are byte-identical to the API responses; requests used the mandatory `Digitraffic-User`
  header and gzip transfer encoding, and no field was added, removed or rewritten.
- Times are UTC. A train that runs past midnight keeps increasing times within its own row list.
- `actualTime`, `differenceInMinutes` and `causes` are present only for rows the operational system
  reported, so they are sparse and absent for future-dated or unreported rows.
- Station codes in `timeTableRows` join to `stationShortCode` in `stations.json`. Cause records in
  `causes` join to the category registers by category code id.
- `PROVENANCE.txt` records the exact endpoints, the download date, a SHA-256 for every file, and the
  notice that downstream work derived from this corpus may modify it.

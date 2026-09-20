# Source verification — Rail Corridor Incident And Dispatch Ledger Recovery

Verified live on 2026-09-20 from this container.

## Official source

- Publisher: Fintraffic (Finnish state transport operations company), open data service **Digitraffic**.
- Endpoints used (all returned HTTP 200 with `Accept-Encoding: gzip`, no credentials, no registration):
  - `https://rata.digitraffic.fi/api/v1/metadata/stations` — 563 station records.
  - `https://rata.digitraffic.fi/api/v1/metadata/detailed-cause-category-codes` — 47 official delay
    cause categories (used only as domain vocabulary reference, not as labels).
  - `https://rata.digitraffic.fi/api/v1/trains/{date}` for 2026-03-10, 2026-06-16, 2026-09-15,
    2026-09-16, 2026-09-17 — 1,792 trains on 2026-09-15, 7,102 train-days across the five dates.
- Digitraffic requires a `Digitraffic-User` header and gzip; both are used and documented in
  `DATA_ACQUISITION.md`.

SHA-256 of every downloaded file:
`Working/batch-20260920-044727/batch-20260920-044727-task-003/pilot_rail/substrate_sha256.txt`.

## License and redistribution

Digitraffic terms of service (https://www.digitraffic.fi/en/terms-of-service/) state the data is
published under **Creative Commons Attribution 4.0 (CC 4.0 BY)**, explicitly permitting distribution,
remixing and building upon the data **including commercially**, provided the source is attributed and
modifications are noted.

Required attribution, carried in the dataset card and in the raw bundle `LICENSE.txt`:

> Source: Fintraffic / digitraffic.fi, license CC 4.0 BY

Modification notice (also carried in the raw bundle `PROVENANCE.txt`): the published corridor scenarios
reuse the original planned stop sequences and planned times unchanged; realized running times are not
the original realized times and are produced by a corridor operations model described below.

## What is real and what is modelled — explicit

**Real, taken unchanged from the official source**
- the station list and station codes;
- every train's ordered stop sequence on a corridor;
- every planned (scheduled) arrival and departure time;
- the train category (Long-distance / Commuter / Cargo) and service type;
- the segment traffic volumes used to classify corridor segments as single- or double-track.

**Modelled by the challenge, and stated as modelled**
- the realized arrival and departure times;
- the hidden incident-and-dispatch program that is the scored target.

The challenge therefore does **not** claim the realized times or the scored ledger are observations of
real Finnish rail incidents, and it does not reuse the real `actualTime` or the real `causes` fields
from the API for any purpose. This is recorded here, in `DATASET_FORM_FILL.md`, and in the
participant-visible description.

## Why the real `causes` field is deliberately not used as the label

The Digitraffic API publishes, for every real train, both the realized times and the official delay
cause codes, in the same records. Any challenge that used the real realized times as input and the real
cause codes as the hidden answer would be fully reversible: an attacker re-downloads the same public
records and reads the answer. That failure mode was measured to be fatal for two earlier candidates in
this slot (`LOOKUP_GATE_EVIDENCE.md`, `LOOKUP_GATE_EVIDENCE_CRSS.md`). Using a private operations
program instead means the scored ledger never existed in any public record.

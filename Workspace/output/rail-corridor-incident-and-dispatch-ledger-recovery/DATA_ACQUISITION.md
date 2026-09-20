# Data acquisition — Rail Corridor Incident And Dispatch Ledger Recovery

All bytes come from the Fintraffic Digitraffic open railway API. Nothing is scraped, and no credential
or registration is needed. Digitraffic mandates two request headers; both are shown below.

## Exact calls

```bash
H='Digitraffic-User: ErisChallengeBot/1.0'
curl -sS --compressed -H "$H" -o stations.json \
  https://rata.digitraffic.fi/api/v1/metadata/stations
curl -sS --compressed -H "$H" -o cause-category-codes.json \
  https://rata.digitraffic.fi/api/v1/metadata/detailed-cause-category-codes
for d in 2026-03-10 2026-06-16 2026-09-15 2026-09-16 2026-09-17; do
  curl -sS --compressed -H "$H" -o trains_$d.json \
    https://rata.digitraffic.fi/api/v1/trains/$d
done
```

Without `--compressed` the service answers HTTP 406 ("Use of gzip compression is required").

## Verified bytes and checksums (2026-09-20)

| File | Bytes | SHA-256 |
|---|---|---|
| stations.json | 101,704 | 10859accfddf2abb8d9dd157e17d8cf3a5a7747ef032482824d8362182af24a0 |
| cause-category-codes.json | 5,822 | fbcb0dfb5208f4e8ae7e8e52e3828527d1df9c0e908743fd0563d1306d304800 |
| trains_2026-03-10.json | 21,598,182 | 5f51de7c046d76133261568c0bb4249ec4644fb4e8b746afbad84bad701046ca |
| trains_2026-06-16.json | 16,649,457 | 3bf10fdea14387fbcb7981f388986853ca38804cf1f6d81ac4f7a779a6783a7d |
| trains_2026-09-15.json | 20,471,793 | 11b84aa3570d4519d49a107075066ef3995154daf2d732d0976d7113959badba |
| trains_2026-09-16.json | 20,160,184 | a9d4baf37642aad8619c93356354aa5787a4554422f62f2f60451f811bbb7a8f |
| trains_2026-09-17.json | 20,505,155 | 03d7151758b424e2bb75d4e1c3ed95781cc7c38ce354e970c0ec786e0118761c |

Total uncompressed ~99.5 MB; the flat `raw_upload.zip` is well under the upload budget and far below the
multi-GB size at which the platform upload server stalls.

## Raw upload layout (flat, per the live rules)

`raw_upload.zip` members, with no wrapper directory:

```
stations.json
cause-category-codes.json
trains_2026-03-10.json
trains_2026-06-16.json
trains_2026-09-15.json
trains_2026-09-16.json
trains_2026-09-17.json
LICENSE.txt          # CC BY 4.0 text plus "Source: Fintraffic / digitraffic.fi, license CC 4.0 BY"
PROVENANCE.txt       # endpoints, dates, checksums, and the modification notice
```

No prepared split, no answers, no challenge code and no cache goes into the archive.
`prepare.py` accepts both `raw/<file>.json` and the platform's post-rebuild `raw/raw_upload/<file>.json`.

## Fallback

If a date is later withdrawn from the API, any five Digitraffic `trains/{date}` responses covering at
least one working weekday reproduce an equivalent substrate; `prepare.py` asserts the station,
corridor and per-corridor run minimums rather than assuming a specific date set.

## Local working copy

Downloaded to
`Working/batch-20260920-044727/batch-20260920-044727-task-003/pilot_rail/`;
checksums in `substrate_sha256.txt` in that folder. No bulk data is kept anywhere else in the slot.

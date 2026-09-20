# DATA_ACQUISITION — slot batch-20260920-044727-task-002

Every download in this slot, with the exact official URL, verified bytes and SHA-256. Bulk payloads
are deleted after evidence capture; the checksums below make each fetch reproducible.

## Candidate #2 — Global Meteor Network (REJECTED on the reversibility gate)

- Official data page: https://globalmeteornetwork.org/data/
- Official directory: https://globalmeteornetwork.org/data/traj_summary_data/monthly/
- Licence, quoted verbatim from the official data page on 2026-09-20:
  "The data are released under the CC BY 4.0 license, so if you are using the data for scientific
  purposes, we kindly ask you to reference this web site in your work."
- Access: plain HTTPS, no credentials, no rate limiting observed.

| File | Official URL | Bytes | SHA-256 |
|---|---|---|---|
| traj_summary_monthly_202408.txt | https://globalmeteornetwork.org/data/traj_summary_data/monthly/traj_summary_monthly_202408.txt | 104,581,698 | 204dab9b69db6df46aaa024b94084afb7e6021624260487011dccc01caac51b3 |
| traj_summary_monthly_202412.txt | https://globalmeteornetwork.org/data/traj_summary_data/monthly/traj_summary_monthly_202412.txt | 82,887,070 | 7007ff3ff50c385a50c9935209a945b0c59f4758c040e200599bb5b91cebcc0b |
| traj_summary_monthly_202504.txt | https://globalmeteornetwork.org/data/traj_summary_data/monthly/traj_summary_monthly_202504.txt | 51,347,932 | 2b84df54610b9022e90d6c236c7ffb7c0d493272c668fb122c21025786767aed |

Also probed (not downloaded): `traj_summary_all.txt` and `traj_summary_yearly_2018..2026.txt` in
https://globalmeteornetwork.org/data/traj_summary_data/ , plus the `daily/` directory. One daily file
(`daily/traj_summary_20211121_solrange_239.0-240.0.txt`, 830,920 bytes) was fetched to a scratch path
to confirm the schema and deleted.

Measured schema: 4 comment header lines then 86 semicolon-separated fields per meteor, including the
full geocentric radiant, heliocentric orbit with a sigma next to every element, begin/end geodetic
position and height, duration, peak absolute magnitude, F parameter, photometric mass, convergence
angle Qc, MedianFitErr, begin/end in-FOV flags, station count and the participating-station roster.

Measured content: 112,139 meteors in 2024-08; 256,730 rows across the three months; 1,021 distinct
stations in 2024-08 (902 with >=50 meteors, 695 with >=200); 1,001 stations with >=120 rows across
the three-month window.

Disposition: raw files and the 99 MB numpy cache deleted 2026-09-20 after the reversibility evidence
was captured (228 MB + 99 MB reclaimed). Derived evidence kept: `scout2/attack1_invariant_lookup.json`,
`scout2/attack2_bundle_station_vote.json`, `scout2/attack3_two_stage_row.json`, `scout2/raw_checksums.txt`,
and the scripts `scout2/load_gmn.py`, `scout2/attack1_invariant_lookup.py`,
`scout2/attack2_bundle_station_vote.py`, `scout2/attack3_two_stage_row.py`.

## Candidate #1 — Library of Congress HABS/HAER/HALS (REJECTED, prior worker)

See `CANDIDATE1_REJECTION_EVIDENCE.md` and `pilot/RIGHTS_STATEMENT_LOC.md`. Image subset deleted after
evidence capture (495 MB reclaimed).

## Candidate #3 — US Census ACS 2023 1-Year PUMS (REJECTED on the leakage/difficulty trade-off)

- Official directory: https://www2.census.gov/programs-surveys/acs/data/pums/2023/1-Year/
- Official landing page: https://www.census.gov/programs-surveys/acs/microdata/access.html
- Licence: CC0 / U.S. public domain (Department of Commerce ACS 1-Year PUMS record on data.gov).
  No attribution or redistribution restriction.
- Access: plain HTTPS, no credentials.

| File | Official URL (directory above + name) | SHA-256 |
|---|---|---|
| csv_pca.zip | csv_pca.zip | b46811cca68b8df7019ab7ce6ef86ba82397ea30507231b6e2df25a8d06dcd76 |
| csv_pfl.zip | csv_pfl.zip | 307f87ef463c5de432e6b2c8a418ac8ca9cf239d59d4698502d468a23c8dc656 |
| csv_pga.zip | csv_pga.zip | 4b951a08216f37c006292acbbd12150a17ea2ee46d8e5990c86e95193c1c103f |
| csv_pnc.zip | csv_pnc.zip | 83a19b97dd5a08eb5df695a670342d607d9f7da60941ae575a135e563f050890 |
| csv_pny.zip | csv_pny.zip | 64b1de7b4830a41593840cb0c9e780b2666e8e4e56083e6f55521619d28e6a6e |
| csv_poh.zip | csv_poh.zip | bd2935864da7638ef013f76bb7264b43776385508e76cc82837777cf6dc8c9ba |
| csv_ptx.zip | csv_ptx.zip | d84255b4ab9ec48e899614320ffe272afb49af03132b1ead60188b0f5b51909e |
| csv_pwa.zip | csv_pwa.zip | 59c6ac5f15f7782415c0729eca08e4bad180772efdb018a6b44ec925ec7c60b1 |

Total downloaded 274,265,683 bytes (8 state person files: CA, FL, GA, NC, NY, OH, TX, WA).
Extracted CSVs were 1.1 GB; both the zips and the extracted CSVs were deleted after compaction.

Retained: `scout3/pums_adults.csv.gz` (17 MB) — adults 18+, columns STATE, PUMA, AGEP, SEX, SCHL,
OCCP, PINCP, ESR, COW, JWTRNS, WKHP, INDP, PWGTP plus a derived AREA key. 1,256,063 records,
1,114 PUMAs. Reproduced by `scout3/extract.py` from the files above.
Derived income cut points measured on this corpus: 24,500 / 60,000 / 120,000 USD.

---

## Candidate #4 — calibration source (2026-09-20)

Real measured source used ONLY to calibrate and validate the generator's harmonic model.
It is not redistributed inside the challenge package; it is cited.

| Item | Value |
|---|---|
| Title | Roundness Measurement Dataset |
| Author | Tuomas Tiainen, Aalto University School of Engineering |
| Landing page | https://zenodo.org/records/7004548 |
| File URL | https://zenodo.org/records/7004548/files/roundness_measurement_dataset.zip?download=1 |
| Retrieved | 2026-09-20T11:1xZ, HTTP 200, 5,368,160 bytes |
| SHA-256 | e284745a50d6d43a972c1bb8c83000f7b2c38b3c9932315696300eff4eb271bf |
| Licence | CC BY 4.0 (permissive, commercial use and redistribution allowed with attribution) |
| Content used | talyrond/TK1..TK5.csv — Taylor Hobson Talyrond TR31c traces of 5 roundness reference workpieces, 3600 points/revolution, displacement in micrometres, ISO 12181-2 Gaussian filter, 15 UPR cutoff |
| Funding/acknowledgement | EMPIR 19ENG07 Met4Wind |

Measured fit (scout4/real_spectrum_fit.json), used to set the generator priors:

| Quantity | Measured value |
|---|---|
| Amplitude roll-off, k = 2..30 | amplitude ~ C * k^alpha, alpha = -1.935, C = 54.72 um |
| Dominant UPR orders | k = 1 (centring/eccentricity), 2 (clamp ovality), 3 (three-jaw chuck), 5 |
| Discrete order spike | k = 12 on workpiece TK2, amplitude 10.6 um (bearing/gear order) |
| Peak-to-valley roundness per workpiece | 19.9, 40.7, 69.9, 80.5, 307.5 um |

Disk: the 5.4 MB archive plus the five extracted 93 KB CSVs are retained (they are the calibration
evidence and are small). No bulk data was downloaded for this candidate.

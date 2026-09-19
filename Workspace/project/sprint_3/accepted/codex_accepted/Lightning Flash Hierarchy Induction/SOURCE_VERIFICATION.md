# Source verification: NOAA GOES-16 GLM Level-2 LCFA

Verified on 2026-07-16. The source gate passes.

## Official product and access route

The source is the NOAA GOES-16 Geostationary Lightning Mapper Level-2 Lightning Detections product (`GLM-L2-LCFA`). NCEI's [GOES-R terrestrial weather page](https://www.ncei.noaa.gov/products/goes-terrestrial-weather-abi-glm) identifies GLM as an optical transient detector, states that GLM Level-2 data are available through NOAA's Open Data Dissemination Program (NODD), and also documents AIRS/CLASS as archive access routes. The [GOES-R Product User's Guide, Volume 5: Level 2+ Products, revision 2.2](https://goes-r.noaa.gov/products/docs/PUG-L2%2B-vol5.pdf) defines the Level-2 event, group, flash, parent-link, time, energy, area, location, and quality variables. NOAA's [Lightning Detection: Events, Groups and Flashes product page](https://goes-r.noaa.gov/products/baseline-lightning-detection.html) confirms the baseline product identity.

The challenge uses five public, anonymously downloadable objects from the NOAA-managed `noaa-goes16` NODD bucket. `URL_IMPORT_LIST.txt` is the canonical direct-import list.

| Object | Bytes | SHA-256 | Events | Groups | Flashes |
|---|---:|---|---:|---:|---:|
| `OR_GLM-L2-LCFA_G16_s20241532200000_e20241532200200_c20241532200219.nc` | 398,567 | `10f9c79a8a3acb50f62599d1cecb930e27f01e0148d0885bdf31c33d1c590f75` | 9,862 | 4,261 | 279 |
| `OR_GLM-L2-LCFA_G16_s20241832200000_e20241832200200_c20241832200214.nc` | 478,439 | `3d62f783a2cc6f57de9493630dc7f26f8bd7d635fdb9c82a50524dec2fa4ba3f` | 12,855 | 5,567 | 466 |
| `OR_GLM-L2-LCFA_G16_s20242142200000_e20242142200200_c20242142200221.nc` | 628,519 | `6f8f150d5a423181d7e169923f063df53c00a16135583e152a8e3dfbcf4ecabf` | 17,190 | 7,597 | 603 |
| `OR_GLM-L2-LCFA_G16_s20242692200000_e20242692200200_c20242692200221.nc` | 780,071 | `362ea0e9a348247102340f7a02e2af3d88841e81158aa49285419280f41e3fb6` | 23,685 | 9,524 | 701 |
| `OR_GLM-L2-LCFA_G16_s20242792200000_e20242792200200_c20242792200220.nc` | 616,231 | `4c4b56f21be7196651d5bc1cff7548a89158d2f953ac14208f06f77c768d1113` | 17,935 | 6,766 | 465 |

Total raw size is 2,901,827 bytes (2.77 MiB): 81,527 events, 33,715 groups, and 2,514 flashes. Each object is a 20-second GOES-East NetCDF4 file titled `GLM L2 Lightning Detections: Events, Groups, and Flashes`, with processing level `NASA L2` and instrument type `GOES-R Series Geostationary Lightning Mapper (GLM)`. The five files span two internal calibration-LUT revisions; no unreported algorithm-version attribute is present.

## Content validation

The prototype opened all five objects with `netCDF4`, checked the expected dimensions and variables, and verified every selected event parent resolves to a group and every selected group parent resolves to a flash. Relevant native variables include:

- event: id, parent-group id, time offset, latitude, longitude, energy;
- group: id, parent-flash id, frame time, latitude, longitude, area, energy, quality flag;
- flash: id, start/end time, latitude, longitude, area, energy, quality flag.

The raw objects are retained unchanged in `raw_data/` only for reproducible local checks. `prepare.py` validates byte length and SHA-256 before reading them. It never writes to them.

## Novelty gate summary

The nearest neighbors are ordinary lightning detection, storm tracking, lightning nowcasting, image-based weather prediction, generic point clustering, and operational GLM event/group/flash production. This challenge is not asking participants to redetect lightning, forecast storms, classify images, reproduce a native threshold recipe, or solve a tabular regression target. The scored task is hierarchical point-set induction under source redaction: recover both detection-to-group and group-to-flash partitions, mark boundary ambiguity, and calibrate confidence from compact local evidence. The explicit overlap/decoy cases, nested label-invariant JSON output, abstention head, and source-lookup restrictions make this a different modeling problem from the upstream product or standard clustering benchmarks. Estimated novelty is 6.5/10, with the caveat that the platform's external novelty checker remains the final gate.

## License and redistribution gate

The gate passes for reuse, commercial use, and redistribution. The official [NOAA/NCEI archive policy](https://www.ncei.noaa.gov/archive) says NOAA-produced environmental data are fully and openly available unless expressly exempt and are public domain in the United States. The NOAA-managed [NODD GOES registry entry](https://registry.opendata.aws/noaa-goes/) states that NOAA data disseminated through NODD are open to the public and may be used as desired; NOAA requests attribution for dissemination of unaltered data and prohibits implying NOAA endorsement or affiliation.

There is one recorded metadata caveat: these operational NetCDF files contain the global string `license = "Unclassified data. Access is restricted to approved users only."` This conflicts with anonymous public NODD delivery, the NODD dataset-specific license statement, and NCEI's open-data policy. It appears to be a stale operational product-template attribute rather than an access restriction: no approval or credentials are required, and NOAA explicitly publishes these objects through NODD. The challenge therefore follows the current official distribution policy, credits NOAA, labels prepared outputs as modified derivatives, and makes no endorsement claim. If a platform reviewer requires the internal NetCDF string to control over the official NODD policy, obtain written clarification from `nodd@noaa.gov` before publication; do not silently substitute a different source.

Suggested attribution: “Source data: NOAA GOES-16 Geostationary Lightning Mapper Level-2 Lightning Detections product, accessed through NOAA NODD. Prepared challenge cases are modified derivatives; NOAA does not endorse this challenge.”

## Import procedure

Preferred procedure:

1. Create the platform dataset from URLs.
2. Add the five URLs from `URL_IMPORT_LIST.txt` without renaming them.
3. Run `prepare.py`; its recursive file locator accepts the platform's URL-import subdirectories.

Fallback only if URL import fails:

1. Download each URL byte-for-byte with a normal HTTP client.
2. Verify the exact byte lengths and SHA-256 values above.
3. Upload the five untouched `.nc` files directly. Do not rename, preprocess, subset, convert, or add derived data.
4. If the UI requires one archive, use the included convenience archive `glm_official_raw_untouched_with_attribution_20260716_210000.zip`, or reproduce it by placing only the five untouched `.nc` files plus an attribution note in a flat ZIP. The included ZIP is 1,107,424 bytes with SHA-256 `02b4127d0c2c0d62326923e5b5c9acb3c86b6d1610b21f0f0073fdd0eeb9ca0b` and contains no public/private prepared data, code, caches, derived tables, or preprocessed files.

## Leakage and source-lookup result

`prepare.py` keeps whole source windows on one side of the split (three train sources, two test sources), applies deterministic per-case rotation, reflection, shear, scale normalization, jitter, time normalization, and energy ranking, and creates salted opaque case/detection aliases. Public inputs contain no object names, native ids, exact timestamps, coordinates, scan fields, or source-window labels. `_analyze.py` found no forbidden source tokens and no duplicate public feature vectors. Source-window prediction from row length/count/id metadata was 0.571429 accuracy versus 0.5 chance; prediction from aggregate public feature statistics was 0.45. Opaque-id order and hash attacks scored 0.140743 and 0.157251. The raw reverse-lookup probe compared public test cases to 350 official raw candidate bundles using invariant geometry/time/energy sketches; top-1 exact case recovery was 0.000000, source-window top-1 recovery was 0.350000, median true-case rank was 160.5/350, and p90 true-case rank was 316/350. The source-window recovery value is a prohibited forensic diagnostic over official raw candidates, not a valid submission score; it does not identify exact cases or recover hidden hierarchy labels.

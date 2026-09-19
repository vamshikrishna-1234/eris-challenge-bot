# Source verification — AI4Mars expert Navcam subset

## Gate result

**PASS, with a clean-subset upload requirement.** The source license permits redistribution and commercial use with attribution, the official masks contain every terrain value required by the challenge, and an unchanged expert-labelled subset is far below 1 GB. The full official merged ZIP is too large for direct URL import under this challenge's requested budget, so the deliverable uses a clean folder ZIP containing only byte-identical official members.

## Primary source and provenance

* NASA Open Data Portal record: https://data.nasa.gov/dataset/ai4mars-a-dataset-for-terrain-aware-autonomous-driving-on-mars
* Official downloadable record linked by NASA: https://zenodo.org/records/15995036
* DOI: https://doi.org/10.5281/zenodo.15995036
* Official merged archive: https://zenodo.org/records/15995036/files/ai4mars-dataset-merged-0.6.zip?download=1
* Archive version: AI4Mars 0.6, published 2022-10-22.
* Archive byte size verified by HTTP HEAD: `16,232,481,989` bytes.
* Archive MD5 published by Zenodo: `daf80a86021253292e6c425f97baa5c6`.
* Archive central directory verified by HTTP range reads: `146,179` members; `16,457,271,328` uncompressed bytes; `16,188,080,522` compressed member bytes.

The NASA page identifies NASA JPL as publisher and describes real images from Curiosity, Opportunity, and Spirit with crowdsourced segmentation and expert validation labels. The linked Zenodo record names NASA/JPL creators and supplies the actual downloadable files.

## License and commercial redistribution

The NASA portal's generic metadata says **License not specified**, so it is not sufficient by itself for the rights gate. The linked official Zenodo record explicitly applies **Creative Commons Attribution 4.0 International (CC BY 4.0)** and says redistribution and reuse are allowed when the creator is appropriately credited. CC BY 4.0 permits sharing and adaptation for any purpose, including commercial use, subject to attribution and the other license conditions.

The challenge therefore does **not** claim that AI4Mars is CC0 or automatically public domain. Dataset attribution must name AI4Mars, Swan/Ono/Atha and NASA JPL, link the Zenodo record/DOI, identify CC BY 4.0, and preserve the source notice. The Zenodo page also displays `Copyright 2022 IEEE`; the explicit CC BY 4.0 grant is the basis for redistribution.

## Download objects, sizes, and archive structure

Zenodo exposes two official top-level downloads:

* `ai4mars-dataset-merged-0.6.zip`: 16.2 GB displayed; exactly `16,232,481,989` bytes by HTTP HEAD.
* `ai4mars-labels-unmerged.zip`: 1.6 GB displayed; uncleaned labels that may include invalid data and do not provide the compact image/mask corpus required here.

The merged archive contains the following verified top-level payload groups:

* `msl/`: about 8.01 GB uncompressed.
* `mer/`: about 4.65 GB uncompressed.
* `m2020/`: about 3.80 GB uncompressed.
* Official documentation: `info.md`, `changelog.md`, `label_keys.json`, mission notes, and a MER test pairing CSV.

Relevant expert folders:

* `msl/ncam/images/edr/`: 18,127 JPEG images.
* `msl/ncam/labels/test/masked-gold-min2-100agree/`: 322 expert PNG masks.
* `mer/images/test/`: 204 expert-test JPEG images.
* `mer/labels/test/masked-gold-min2-100agree/`: 204 expert PNG masks.

The clean subset contains 1,059 unchanged official files: 526 JPEGs, 526 PNG masks, and seven official documentation/mapping files. Its exact official uncompressed payload is `169,450,173` bytes and the selected members occupy `168,073,948` compressed bytes in the source archive. It is therefore safely below 1 GB.

## Direct URL import decision

Direct URL import of the full official merged ZIP is **not acceptable** for this challenge because the imported object would be 16.23 GB, far above the requested approximately 1 GB raw-data budget. Zenodo does not publish the expert subset as a separate official download object, and a URL importer cannot select members inside a remote ZIP.

The compliant fallback is:

1. Run `generate.py`, which reads the official ZIP central directory and uses HTTP byte ranges to extract only the 526 expert image/mask pairs plus official documentation.
2. The helper validates archive size, member counts, decompressed byte count, and CRC32 for every file.
3. Run `generate.py --verify-only` to recheck the local files.
4. Run `zip_raw_for_upload.py` to create `ai4mars_official_expert_subset.zip` with the original `ai4mars-dataset-merged-0.6/...` paths.
5. Upload that clean ZIP. It contains no resized images, prepared split, challenge answers, or derived labels.

## Labels and metadata gate

The official `info.md` and `label_keys.json` define the NAV mask pixel values:

* `0`: soil
* `1`: bedrock
* `2`: sand
* `3`: big rock
* `255`: NULL / unknown / unlabeled

The min-2 expert masks require 100% class agreement among at least two expert labelers for an included pixel. Unknown coverage is therefore a real annotation-support signal, not an invented uncertainty label. Image and mask dimensions match. The relevant source files are grayscale Navcam products.

Available safe metadata is intentionally coarse: rover mission (Curiosity, Spirit, or Opportunity), camera family (Navcam), and image dimensions. The challenge does not invent GPS, rover pose, heading, or physical route coordinates. Original filenames encode mission/product information but are stripped from participant data because they are source-lookup keys.

## Output derivability gate

Every scored field is computed only from the official mask after the same label-preserving crop/flip applied to the public image:

* `terrain_mask_rle`: 32 × 32 region map over the five official values.
* `hazard_boxes_json`: connected-component boxes over big-rock and substantial unknown regions.
* `route_safety_class`: deterministic class from the queried corridor's big-rock, sand, clearance, safe-width and unknown fractions.
* `clearance_score`: corridor mean of documented per-class traversability weights.
* `obstacle_coverage`: corridor fraction labeled big rock.
* `safe_corridor_width`: robust connected nonblocked width around the route.
* `uncertainty_score`: weighted route/global fraction of official NULL pixels.

No wheel-track, roughness, slope, depth, GPS, slip, energy, or manually authored navigation label is claimed. AI4Mars NAV does not provide a wheel-track class, so none is used.

The route is one of five fixed normalized image-plane corridors. Its endpoints and width are provided as input. Assigning which corridor is queried does not assign the answer: all answer values are subsequently derived from real mask geometry.

## Leakage and source-reversibility assessment

Risk remains because AI4Mars is a named public corpus. The prepared data therefore:

* removes original stems and all raw IDs;
* assigns salted hash-derived opaque IDs;
* splits by rover/time/product sequence family so adjacent frames do not cross splits;
* applies a deterministic aligned crop, possible mirror, resize, contrast normalization, and JPEG re-encode;
* exposes only coarse mission/camera/dimensions;
* sorts CSVs by opaque ID; and
* explicitly prohibits source-image and source-annotation lookup.

These controls close exact filename/hash/order lookup. They cannot mathematically prevent a participant from building a prohibited large-scale perceptual retrieval index over the public source, so source lookup remains a review/enforcement risk and is listed in the handoff.

The organizer-side `_analyze.py` probes exact image hashes, raw/source filename tokens, ID ordering, raw file-size matching, public file-size shortcuts, whole-image thumbnail retrieval, and a stronger multicrop lookup search against all 526 official source images and their horizontal mirrors. On the final prepared split, public/raw exact image SHA-256 hits are `0`, test rows uniquely recoverable by raw file size are `0`, whole-image true-source thumbnail retrieval is `0.5780%` at rank 1 and `1.7341%` within rank 5, with median true-source rank `199`. The stronger multicrop source probe is `5.2023%` at rank 1, `8.0925%` within rank 5, `16.1850%` within rank 10, with median true-source rank `111`. File-size-only and ID-prefix-only submissions remain weak at `0.267193` and `0.235963`. This is a stronger practical fingerprint stress test, not a proof against every possible learned local-feature retrieval attack.

## Novelty gate

**Defensible novelty score: 6/10 (recombined), with reviewer risk.**

Nearest neighbours:

* AI4Mars itself: Mars terrain semantic segmentation from rover images.
* MarsScapes-Navigability and later Mars segmentation work: navigable-terrain or semantic-mask prediction.
* TTA-GEP and related planetary traversability systems: semantic/elevation cost maps feeding path planning.
* MLNav: learning-enhanced path planning on Mars terrain with model-based safety checking.

This task shares the image-to-terrain-mask core, so it is not frontier-new. The genuine change is the scored output contract: a supplied route corridor conditions a mixed evidence ledger containing a compact region map, component hazards, discrete go/slow/avoid/uncertain decision, obstacle fraction, clearance, connected safe width, and explicit annotation uncertainty. A plain segmentation submission is incomplete, and a route classifier without spatial evidence cannot recover the mask/box heads. The benchmark tests whether a CPU visual model can produce operationally consistent navigation evidence rather than only per-pixel terrain names.

The score is not claimed above 6 because semantic traversability and path planning are established. A reviewer could still judge the deterministic mask-to-ledger layer as too close to segmentation; this is the primary novelty risk.

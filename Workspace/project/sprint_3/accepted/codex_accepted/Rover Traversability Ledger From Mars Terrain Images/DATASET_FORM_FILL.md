# Dataset creation form — fill-in

## Dataset name

```
AI4Mars Expert Navcam Image And Terrain-Mask Subset
```

## Overview

This is a clean official-source subset of AI4Mars version 0.6 containing 526 real grayscale Mars Navcam images and their expert-merged terrain masks: 322 Mars Science Laboratory (Curiosity) pairs and 204 Mars Exploration Rover (Spirit/Opportunity) pairs. The files are byte-identical members of the official merged archive and retain the original AI4Mars directory names. The subset also contains the official class key, dataset information, changelog, mission notes, expert-merge note, and MER test pairing CSV.

## File structure

```
ai4mars-dataset-merged-0.6/
  info.md
  changelog.md
  label_keys.json
  msl/NOTE.txt
  msl/ncam/images/edr/*.JPG
  msl/ncam/labels/test/NOTE.txt
  msl/ncam/labels/test/masked-gold-min2-100agree/*.png
  mer/NOTE.txt
  mer/images/test/*.JPG
  mer/labels/test/masked-gold-min2-100agree/*.png
  mer/labels/test/masked-gold-min3-100agree/test.csv
```

* `info.md` is the official AI4Mars merged-dataset description and class documentation.
* `changelog.md` records official dataset-version changes.
* `label_keys.json` maps navigation mask pixel values to terrain names.
* `msl/ncam/images/edr/` contains 322 selected official Curiosity Navcam JPEGs.
* `msl/ncam/labels/test/masked-gold-min2-100agree/` contains the corresponding 322 expert-merged PNG masks.
* `mer/images/test/` contains 204 official Spirit/Opportunity Navcam JPEGs.
* `mer/labels/test/masked-gold-min2-100agree/` contains the corresponding 204 expert-merged PNG masks.
* The text notes and `test.csv` are unchanged official documentation/mapping files from the same archive.

## Features

This raw image/mask corpus has no tabular feature matrix. Its stored item properties are:

* Navcam images (JPEG): real grayscale rover-camera images; the MSL and MER mission/camera family is encoded by the official directory and product naming convention.
* Expert masks (PNG): single-channel grayscale images whose pixel dimensions match the paired JPEG.
* Navigation mask value `0`: soil.
* Navigation mask value `1`: bedrock.
* Navigation mask value `2`: sand.
* Navigation mask value `3`: big rock.
* Navigation mask value `255`: NULL, meaning unknown or unlabeled.
* Min-2 expert merge: a semantic pixel is included only where at least two expert labelers supplied the same class with 100% agreement among those included labels.
* MER `test.csv`: two string columns mapping an official image stem to its JPEG filename.

## License

Creative Commons Attribution 4.0 International (CC BY 4.0). Redistribution and reuse, including commercial use, are allowed with appropriate attribution. Attribute AI4Mars and its creators, NASA Jet Propulsion Laboratory, the Zenodo record/DOI, and the related publication as requested by the source record.

## Source

NASA Open Data Portal: https://data.nasa.gov/dataset/ai4mars-a-dataset-for-terrain-aware-autonomous-driving-on-mars

Official downloadable record: https://zenodo.org/records/15995036

DOI: https://doi.org/10.5281/zenodo.15995036

Official merged archive: https://zenodo.org/records/15995036/files/ai4mars-dataset-merged-0.6.zip?download=1

## Notes

* The subset contains 1,059 official files: 526 JPEG images, 526 PNG masks, and seven documentation/mapping files.
* Exact uncompressed official payload: 169,450,173 bytes; selected compressed member payload in the source ZIP: 168,073,948 bytes.
* No image, mask, filename, label value, or documentation file in this source subset is resized, renamed, re-encoded, or regenerated.
* The complete official merged archive is 16,232,481,989 bytes; this clean subset is used because the source platform does not publish the expert files as a separate sub-GB download object.

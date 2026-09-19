# Data Source Manifest

## Official Source

Primary source: https://github.com/CheyneyComputerScience/CREMA-D

Official mirror linked from the repository README: https://gitlab.com/cs-cooper-lab/crema-d-mirror.git

License reference from audeering: https://audeering.github.io/datasets/datasets/crema-d.html

CREMA-D is the Crowd-sourced Emotional Multimodal Actors Dataset. The official repository states that the database is available under the Open Database License and that individual contents are licensed under the Database Contents License. The audeering index lists CREMA-D as ODbL with commercial usage, WAV format, mono channel, 16 kHz sampling rate, 16-bit audio, and 7,441 listed WAV files.

## Selected Raw Files

Use only official CREMA-D source files copied or imported unmodified from the repository.

```text
AudioWAV/*.wav
LICENSE.txt
README.md
SentenceFilenames.csv
VideoDemographics.csv
processedResults/tabulatedVotes.csv
processedResults/summaryTable.csv
docs/ optional official documentation
```

Do not upload `VideoFlash/` and do not upload duplicate `AudioMP3/` copies when `AudioWAV/` is present. The full repository is much larger because it includes video, MP3, WAV, scripts, and Git LFS history; the selected official WAV-plus-metadata layout is about 606 MB plus small metadata files.

## Expected Raw Layout For prepare.py

`prepare.py` accepts any of these roots as long as an official `AudioWAV/` directory is present:

```text
raw/AudioWAV/*.wav
raw/raw_upload/AudioWAV/*.wav
raw/raw_data/AudioWAV/*.wav
raw/CREMA-D/AudioWAV/*.wav
raw/crema-d-mirror/AudioWAV/*.wav
```

The script parses official CREMA-D filenames directly and fails clearly if it cannot find enough valid official WAV files. A tiny local smoke fixture is supported only when `SMOKE_FIXTURE_ONLY.txt` is present; that fixture is not a source upload.

## Direct Import Or Manual Upload Instructions

Preferred official checkout:

```powershell
git clone --filter=blob:none --no-checkout https://github.com/CheyneyComputerScience/CREMA-D.git CREMA-D
cd CREMA-D
git lfs install --local
git sparse-checkout init --cone
git sparse-checkout set AudioWAV processedResults docs LICENSE.txt README.md SentenceFilenames.csv VideoDemographics.csv
git checkout master
git lfs pull --include="AudioWAV/*" --exclude="AudioMP3/*,VideoFlash/*"
```

If GitHub LFS is unavailable, use the official GitLab mirror linked by the CREMA-D README and checkout the same paths. If the platform supports direct repository import, import the official repository with those sparse paths and LFS enabled. If files are uploaded manually, upload the official `AudioWAV` files and metadata unmodified from the official checkout.

## No Custom Raw Zip

No `raw_upload.zip` is created for this challenge. The raw source must be the official CREMA-D files imported or uploaded directly, not a custom repackaged archive produced by this workspace.

## Local Source Check

During this build, a sparse official checkout was started under this challenge folder at `raw_data/`. The `AudioWAV` directory contains 7,442 WAV files totaling about 605,899,936 bytes, which is under the requested 1 GB raw-source target.

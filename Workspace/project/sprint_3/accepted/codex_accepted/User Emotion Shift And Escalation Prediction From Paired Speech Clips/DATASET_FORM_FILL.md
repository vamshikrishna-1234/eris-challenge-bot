# Dataset creation form - fill-in

## Dataset name

```text
CREMA-D Official AudioWAV Speech Clips And Metadata
```

## Overview

This dataset consists of official CREMA-D source files imported directly from the CREMA-D repository: the `AudioWAV` speech clips plus small metadata and license files. CREMA-D contains 7,442 original acted multimodal clips from 91 actors, with audio files named by actor id, sentence code, expressed emotion code, and intensity code. The selected source layout uses the official WAV audio only, not video and not duplicate MP3 audio.

## File structure

```text
AudioWAV/*.wav                         official mono speech WAV clips
LICENSE.txt                            official CREMA-D license text
README.md                              official dataset readme
SentenceFilenames.csv                  official sentence/file listing
VideoDemographics.csv                  official actor demographic table
processedResults/tabulatedVotes.csv    official tabulated rating summary
processedResults/summaryTable.csv      optional official summary table
docs/                                  optional official documentation files
```

* `AudioWAV/` contains the official CREMA-D WAV files used for computational audio processing.
* `LICENSE.txt` contains the official Open Database License and Database Contents License notice.
* `README.md` describes CREMA-D, its file naming convention, text data files, and metadata files.
* `SentenceFilenames.csv` lists official file names and sentence references.
* `VideoDemographics.csv` maps the actor id portion of each file name to age, sex, race, and ethnicity fields.
* `processedResults/` contains official crowd-rating tabulations and summary tables when included in the source checkout.
* `docs/` contains optional official supporting documentation from the repository.

## Raw file naming convention

`AudioWAV/<ActorID>_<SentenceCode>_<EmotionCode>_<IntensityCode>.wav` (file path): official CREMA-D speech clip path.

`ActorID` (four-digit string): actor identifier encoded as the first component of the official file name.

`SentenceCode` (three-letter string): one of the official sentence prompts encoded in the file name, such as `IEO`, `TAI`, or `WSI`.

`EmotionCode` (string): official expressed emotion code in the file name, one of `ANG`, `DIS`, `FEA`, `HAP`, `NEU`, or `SAD`.

`IntensityCode` (string): official expression intensity code in the file name, one of `LO`, `MD`, `HI`, or `XX`.

`*.wav` audio (WAV): official 16 kHz mono 16-bit speech audio according to the CREMA-D audio distribution.

## Metadata files

`SentenceFilenames.csv` columns (CSV): official sentence/file listing fields as distributed by CREMA-D.

`VideoDemographics.csv` `ActorID` (string): actor id matching the first four digits of each audio file.

`VideoDemographics.csv` `Age` (integer-like string): actor age in years at recording time.

`VideoDemographics.csv` `Sex` (string): actor sex field distributed in CREMA-D metadata.

`VideoDemographics.csv` `Race` (string): actor race field distributed in CREMA-D metadata.

`VideoDemographics.csv` `Ethnicity` (string): actor ethnicity field distributed in CREMA-D metadata.

`processedResults/tabulatedVotes.csv` `fileName` (string): official rated file name.

`processedResults/tabulatedVotes.csv` emotion count columns (integer): crowd response counts for expressed emotion categories.

`processedResults/tabulatedVotes.csv` agreement columns (numeric): official agreement and rating summary fields.

## Prepared public columns

`id` (integer): opaque prepared row id.

`sample_id` (integer): opaque prepared pair id with the same value as `id`.

`baseline_audio` (string): path to the prepared baseline WAV clip.

`current_audio` (string): path to the prepared current WAV clip.

`pair_duration_bucket` (string): coarse duration bucket for the prepared audio pair.

`affect_label` (string, training rows): current clip expressed-affect label.

`valence_shift` (string, training rows): perceived valence shift relative to the baseline clip.

`arousal_shift` (string, training rows): perceived arousal shift relative to the baseline clip.

`escalation_tier` (string, training rows): operational escalation tier.

`confidence` (float, training rows): confidence target in `[0, 1]`.

## License

Open Data Commons Open Database License (ODbL) v1.0 for the database and Database Contents License (DBCL) v1.0 for individual contents, as stated by the official CREMA-D repository. The audeering dataset index also lists CREMA-D under ODbL with commercial usage.

## Source

Official CREMA-D repository: https://github.com/CheyneyComputerScience/CREMA-D

Official CREMA-D GitLab mirror linked by the repository: https://gitlab.com/cs-cooper-lab/crema-d-mirror.git

audeering CREMA-D license and format reference: https://audeering.github.io/datasets/datasets/crema-d.html

## Notes

* Use the official `AudioWAV` files and metadata copied or imported unmodified from the CREMA-D source repository.
* Do not include `VideoFlash/` or `AudioMP3/` when using the WAV layout; that would duplicate modalities and exceed the intended compact raw-source layout.
* The official `AudioWAV` directory is about 606 MB for 7,442 WAV files, keeping the selected source layout below 1 GB before small metadata files.
* This is a real source-data layout, not a synthetic generator output and not a custom raw upload archive.

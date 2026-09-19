# Dataset creation form - fill-in

## Dataset name

```text
NOAA NCEI DCLDE Killer-Whale Hydrophone Annotation Subset
```

## Overview

This dataset is a bounded official-source subset of the NOAA/NCEI DCLDE 2027 killer-whale hydrophone audio and annotation archive. It contains the official cleaned annotation CSV, an official Creative Commons license text file from the bucket, and 123 unchanged official WAV/FLAC hydrophone recordings selected from the public NOAA Google Cloud Storage distribution. The selected files include killer-whale annotations, other biological confounders, unidentified biological sounds, and ambient/background annotations while keeping the raw URL import under 1 GB.

## File structure

```text
Annotations.csv                                  official cleaned annotation table
CC-BY-4.0.txt                                   official bucket license text file
dfo_crp/audio/northbc/*.flac                    selected DFO_CRP NorthBc audio
orcasound/audio/bush_point/*.wav                selected OrcaSound Bush Point audio
orcasound/audio/orcasound_lab/*.wav             selected OrcaSound lab audio
orcasound/audio/port_townsend/*.wav             selected OrcaSound Port Townsend audio
smru/audio/lime-kiln/*.wav                      selected SMRU Lime Kiln audio
simres/audio/eastpoint/*.flac                   selected SIMRES East Point audio
```

- `Annotations.csv` is the official NOAA/NCEI cleaned annotation CSV imported unchanged from the public bucket.
- `CC-BY-4.0.txt` is the official license text object imported unchanged from the public bucket; the file content identifies the Creative Commons Attribution-ShareAlike 4.0 International public license even though the object name says CC-BY.
- The `dfo_crp`, `orcasound`, `smru`, and `simres` audio paths are unchanged official hydrophone audio objects from the NOAA public bucket.
- If the platform URL importer flattens object names instead of preserving folders, the same basenames are still official source objects from the selected NOAA/NCEI source-file import.

## Annotations.csv columns

- `Unnamed: 0` (integer): row number from the official cleaned annotation table.
- `Soundfile` (string): official audio filename referenced by the annotation row.
- `Dataset` (string): source dataset or recording-location grouping used in the official annotation table.
- `LowFreqHz` (float): lower frequency bound of the annotated sound when available.
- `HighFreqHz` (float): upper frequency bound of the annotated sound when available.
- `FileEndSec` (float): annotation end time in seconds within `Soundfile`.
- `UTC` (string): official UTC timestamp string for the annotation event.
- `FileBeginSec` (float): annotation start time in seconds within `Soundfile`.
- `ClassSpecies` (string): official species/sound class such as `KW`, `HW`, `UndBio`, or `AB`.
- `KW` (integer): official killer-whale indicator, with `1` for killer whale and `0` otherwise.
- `KW_certain` (float): official certainty indicator for killer-whale annotations when available.
- `Ecotype` (string): official killer-whale ecotype/context value when available, such as `SRKW`, `TKW`, `NRKW`, or `OKW` in this subset.
- `Provider` (string): official data provider grouping such as `DFO_CRP`, `OrcaSound`, `SMRUConsulting`, or `SIMRES`.
- `AnnotationLevel` (string): official annotation granularity, such as detection, call, or file level.
- `FilePath` (string): original source-side path recorded in the official cleaned table.
- `FileOk` (boolean): official flag indicating whether the source audio file is usable.

## Raw audio files

- DFO_CRP FLAC files are selected official hydrophone recordings from the NorthBc and WVanIsl source families.
- OrcaSound WAV files are selected official minute-scale hydrophone recordings from Bush Point, OrcaSound lab, and Port Townsend source folders.
- SMRUConsulting WAV files are selected official Lime Kiln recordings with killer-whale and confounder annotations.
- SIMRES FLAC files are selected official East Point recordings with dense killer-whale activity annotations.

## License

Data.gov lists the source dataset license as CC0 1.0. The dataset files also include the official `CC-BY-4.0.txt` license object from the NOAA bucket; its text identifies Creative Commons Attribution-ShareAlike 4.0 International.

## Source

Official NOAA/NCEI DOI landing page: `https://doi.org/10.25921/15ey-mh50`

## Notes

- The dataset source-file import contains 123 selected official audio files plus `Annotations.csv` and `CC-BY-4.0.txt`.
- Selected audio bytes total 810,259,643 bytes; total raw import bytes including annotation/license objects are 860,764,661 bytes, about 820.89 MiB.
- No custom processed raw archive is used; all imported dataset objects are unchanged official NOAA/NCEI source objects.
- The full upstream archive is much larger and is intentionally not imported.

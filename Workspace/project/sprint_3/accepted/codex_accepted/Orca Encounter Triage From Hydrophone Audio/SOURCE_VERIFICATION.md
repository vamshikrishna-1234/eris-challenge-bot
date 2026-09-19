# Source verification - Killer Whale Conservation Bioacoustic Profiling From Hydrophone Audio

## Official source

The raw data source is the NOAA/NCEI DCLDE 2027 killer-whale annotation and hydrophone-audio dataset with DOI `10.25921/15ey-mh50`. The Data.gov catalog page identifies NOAA National Centers for Environmental Information as publisher, lists the Google Cloud Storage distribution, and describes a cleaned annotation CSV with more than 225,000 call-level annotations across multiple Northeast Pacific hydrophone locations.

The NCEI landing page states that the dataset consists of raw audio files, detection CSV files, and documents, and gives the purpose as building detection and classification models for different killer-whale ecotypes. This confirms that a plain killer-whale detection or ecotype-classification challenge would be too close to the source's canonical use.

## License check

Data.gov lists the dataset license URL as `https://creativecommons.org/publicdomain/zero/1.0/`, i.e. CC0 1.0. The official NOAA GCS bucket also contains an object named `CC-BY-4.0.txt`; the downloaded file begins with `Attribution-ShareAlike 4.0 International` and contains the Creative Commons Attribution-ShareAlike 4.0 International public license text. This folder therefore documents both facts exactly: catalog metadata says CC0 1.0, while the bucket-side license text is CC BY-SA 4.0 despite the filename. Both are permissive enough for the requested challenge workflow under the user's accepted license list.

## Bounded raw import

The full official archive is about 1.47 TiB, so this challenge does not import the full archive. `URL_IMPORT_LIST.txt` selects only unchanged official NOAA/NCEI objects: `Annotations.csv`, `CC-BY-4.0.txt`, and 123 official WAV/FLAC audio objects from the public bucket. The selected audio bytes total 810,259,643 bytes, and total raw URL-import bytes including annotation/license objects are 860,764,661 bytes, about 820.89 MiB.

Selected audio coverage by provider:

| Provider | Files | Audio bytes | Main support |
|---|---:|---:|---|
| DFO_CRP | 74 | 127094129 | NRKW/TKW/OKW and confounders |
| OrcaSound | 34 | 195431004 | SRKW and ambient/background |
| SMRUConsulting | 12 | 359999528 | SRKW plus HW/UndBio confounders |
| SIMRES | 3 | 127734982 | dense SRKW calling |

## Novelty gate

Closest neighbors:

- DCLDE killer-whale detection/ecotype classification: same upstream source, same hydrophone modality, and overlapping call annotations. This is the closest neighbor and caps novelty if the challenge is only call/no-call or ecotype prediction.
- OrcaSpot, OrcaHello, and related killer-whale detectors: similar audio modality and binary whale-presence framing, but they do not require multi-head encounter triage.
- General bioacoustic species-classification benchmarks: similar acoustic feature families, but usually ask for species labels or call presence rather than a conservation triage profile.

Novelty judgment: 6/10. The source's canonical task is detection and classification, so this challenge deliberately moves away from a canonical single-label detector. The public task uses short prepared clips and asks for a multi-head encounter triage profile: orca presence including uncertainty, activity density, ecotype/context bucket with rare unsupported classes merged, confounder type, call-band bucket, calibrated confidence, and worst-group robustness over provider/context/activity/confounder/band/quality groups. A binary orca detector or ecotype-only classifier should leave substantial score on the table because it misses activity density, confounders, call-band, confidence calibration, and robustness. This reaches the recombined/operational-triage band above the 5/10 novelty threshold, but not higher because the same public hydrophone corpus and annotations are still the basis.

## Leakage controls

All raw filenames, provider names, dataset names, original timestamps, raw paths, source row order, annotation ids, UTC fields, and exact frequency values are stripped from public CSVs. Public ids are salted opaque hashes and all CSVs are sorted by id. Public audio is not byte-copied: `prepare.py` extracts short windows, converts to mono 16 kHz PCM WAV, normalizes/pads/trims, applies mild deterministic speed/EQ/dither rendering, and writes opaque filenames. The split is by raw soundfile, so clips from the same raw audio object do not cross train/test.

`_analyze.py` includes source-token and timestamp scans of public CSVs, path existence checks, metadata-only baselines, binary-orca-only baseline, simple audio-feature baseline, label-distribution reporting, hidden subgroup counts, and an optional `--raw` near-exact waveform fingerprint probe against official raw WAV/FLAC files. If source lookup, media fingerprinting, or metadata-only baselines become strong after a future change, the concrete fix is to remove/coarsen the leaking public field or increase audio rendering while preserving the bioacoustic signal.

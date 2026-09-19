# Source Verification

Checked on 2026-07-04.

## Official Source

Primary source: https://zenodo.org/records/6257551

The challenge uses the official Acoustic Characterization of Environments (ACE) Corpus record on Zenodo. The selected raw source files are imported or uploaded unmodified:

| Official file | Expected size | Use |
|---|---:|---|
| `ACE_Corpus_RIRN_Single.tbz2` | about 417.2 MB | official single-channel room impulse responses and matched room noise |
| `ACE_Corpus_Speech.tbz2` | about 148.2 MB | official anechoic speech utterances |
| `ACE_Corpus_Data.tbz2` | about 1.2 MB | official T60/DRR measurements and metadata |

Optional documentation files, useful for audit but not required by `prepare.py`, are `ACE_Corpus_instructions_v01.pdf` and `ACE_Corpus_Microphone_arrangements_v02.pdf`.

License: the Zenodo record is marked Creative Commons Attribution 4.0 International (CC BY 4.0). Attribution should cite the ACE Corpus and the ACE corpus paper by Eaton, Gaubitch, Moore, and Naylor.

## Raw Layout Expected By `prepare.py`

Platform import should place these unmodified files at either the raw root or `raw/raw_upload/`:

```text
ACE_Corpus_RIRN_Single.tbz2
ACE_Corpus_Speech.tbz2
ACE_Corpus_Data.tbz2
```

`prepare.py` also accepts an already extracted official layout containing:

```text
Data/20150225T195903_test_t60_DRR_measurement_results.csv
Speech/*.wav
Single/.../*.wav    # RIR and Noise WAV files, exact nesting may vary
```

If the official source files are absent, `prepare.py` stops with the exact required filenames and URLs. The only non-official data path is the tiny `--allow-fixture` mode used by `_sanity_smoke.py`; that fixture is not a challenge dataset source.

No `raw_upload.zip` is created. The official ACE archives are the dataset source files, and all challenge-specific convolution, filtering, splitting, label bucketing, filename salting, and public/private output creation happens in `prepare.py`.

## Label Provenance

Room dimensions and room/source-microphone condition names come from the official ACE documentation, especially the microphone-arrangement document. The room volume values used for bucket labels are:

| ACE room | Public bucket input used internally | Approx. volume |
|---|---|---:|
| Office 1 | `small` | 47.3 m3 |
| Office 2 | `small` | 48.3 m3 |
| Building Lobby | `medium` | 72.9 m3 |
| Meeting Room 1 | `medium` | 99.6 m3 |
| Lecture Room 1 | `large` | 202.0 m3 |
| Meeting Room 2 | `large` | 246.0 m3 |
| Lecture Room 2 | `very_large` | 370.0 m3 |

RT60 buckets use official fullband T60 values from `20150225T195903_test_t60_DRR_measurement_results.csv`: `dry` for T60 <= 0.36 s, `moderate` for T60 <= 0.55 s, `reverberant` for T60 <= 0.85 s, and `very_reverberant` above that. The 0.36 s dry boundary keeps the paired dry Office condition represented in public train while holding out a separate dry condition for hidden test. Source-microphone distance buckets use the official short/long source-microphone condition codes, room scale, and official fullband DRR as a physically meaningful proxy when the absolute position evidence is borderline. Echo-zone labels combine official DRR, official T60, source-microphone bucket, noise type, and SNR.

Public CSVs do not expose room id, room name, RIR id, source position, microphone position, source filename, talker id, utterance id, T60, DRR, room dimensions, SNR, or raw noise condition. Public audio filenames are salted opaque ids. Prepared public WAVs are not exact source-archive copies or exact deterministic convolutions: `prepare.py` applies mild speech-preserving speed, spectral-tilt, and dither perturbations after measured-RIR convolution and measured-noise mixing to reduce direct audio fingerprint/source matching while keeping the acoustic inference task model-compatible.

## Novelty Gate

Closest neighbor: the ACE Challenge itself, whose canonical task was blind acoustic parameter estimation from speech, especially reverberation time T60 and direct-to-reverberant ratio DRR.

This challenge should not be treated as a custom-metric clone of ACE because the prediction contract is different:

- Inputs are newly prepared reverberant speech clips constructed in `prepare.py` from official anechoic speech, official single-channel RIRs, and official room noises.
- Outputs are a practical multi-head acoustic environment profile: room-volume bucket, RT60 bucket, source-microphone distance bucket, echo-zone category, and confidence/uncertainty.
- T60 is only one head. DRR is not submitted directly; it contributes to distance and echo-zone labeling.
- The task strips raw room, RIR, source, mic, talker, utterance, SNR, and metadata identifiers from public CSVs and filenames, preventing direct metadata lookup.
- The split holds out original speech files and RIR/source-microphone conditions while keeping room coverage in both train and test, so the task is blind acoustic-environment inference rather than exact room-id memorization.
- The grader includes multi-head consistency through calibration and hidden worst-subgroup robustness across room scale, reverberation regime, distance bucket, noise condition, speech split, and mic/source configuration.

Novelty judgment: acceptable, about 6/10. It reuses ACE data and shares the general blind-acoustics input modality, so it is in the recombined band rather than a wholly new modality. The new task is materially different from ACE's original T60/DRR estimation because it asks for a practical, bucketed, multi-head environment profile from de-identified speech clips.

If a future full-source run shows that the prepared task collapses to exact room-id classification or exact T60/DRR lookup, the correct pivot is to reduce or remove the room-volume head and refocus on echo-zone/distance/noise-robust confidence from held-out acoustic conditions rather than shipping a near-duplicate.

## Rejected Alternate Sources

- TAU-SRIR: rejected because the license is non-commercial and unsuitable for a commercial challenge setting.
- Isophonics/QMUL room impulse response data: rejected because the license is non-commercial/share-alike.
- TUGraz room acoustics data: rejected for this challenge because the complete source is about 17.5 GB, far above the intended sub-1 GB source budget.
- BUT ReverbDB: rejected as the main source because the RIR-only corpus is about 8.7 GB; a future official permissive subset could be reconsidered.

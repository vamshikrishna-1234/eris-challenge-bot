# Dataset creation form - fill-in

## Dataset name

```text
NInFEA Fetal Doppler ECG And Respiration Source Files
```

## Overview

This is a non-tabular physiological sensor corpus with no master CSV. It contains official NInFEA pulsed-wave Doppler ultrasound strip bitmap images, synchronized multichannel ECG/electrophysiological recordings, maternal respiration signals, checksums, and helper code from 60 antenatal recordings. The source is an open-access PhysioNet medical dataset distributed as unchanged raw files.

## File structure

The platform-visible imported ZIP extracts into one official top-level directory. The raw files are inside that directory:

```text
ninfea-non-invasive-multimodal-foetal-ecg-doppler-dataset-for-antenatal-cardiology-research-1.0.0/
ninfea-non-invasive-multimodal-foetal-ecg-doppler-dataset-for-antenatal-cardiology-research-1.0.0/LICENSE.txt
ninfea-non-invasive-multimodal-foetal-ecg-doppler-dataset-for-antenatal-cardiology-research-1.0.0/RECORDS
ninfea-non-invasive-multimodal-foetal-ecg-doppler-dataset-for-antenatal-cardiology-research-1.0.0/SHA256SUMS.txt
ninfea-non-invasive-multimodal-foetal-ecg-doppler-dataset-for-antenatal-cardiology-research-1.0.0/pwd_images/*.bmp
ninfea-non-invasive-multimodal-foetal-ecg-doppler-dataset-for-antenatal-cardiology-research-1.0.0/wfdb_format_ecg_and_respiration/*.hea
ninfea-non-invasive-multimodal-foetal-ecg-doppler-dataset-for-antenatal-cardiology-research-1.0.0/wfdb_format_ecg_and_respiration/*.dat
ninfea-non-invasive-multimodal-foetal-ecg-doppler-dataset-for-antenatal-cardiology-research-1.0.0/bin_format_ecg_and_respiration/*.bin
ninfea-non-invasive-multimodal-foetal-ecg-doppler-dataset-for-antenatal-cardiology-research-1.0.0/code/*
```

* The preferred platform import is the official ZIP URL `https://physionet.org/content/ninfea/get-zip/1.0.0/`.
* If URL import is unavailable, upload unchanged official files only.
* There is no master CSV and no raw label table in this source package.

## Features

The raw corpus is stored as image, signal, header, and text files rather than rows in a master table. The features below are the named raw data fields and file properties present in the dataset.

### Top-level source files

| Name | Data type | Description |
|---|---|---|
| `LICENSE.txt` | UTF-8 text | ODC-By license terms. |
| `RECORDS` | UTF-8 text | One WFDB record basename per line. |
| `SHA256SUMS.txt` | UTF-8 text | Official SHA-256 checksums. |
| `pwd_images/<record>.bmp` | BMP image | Pulsed-wave Doppler strip for one record. |
| `wfdb_format_ecg_and_respiration/<record>.hea` | WFDB text header | Sampling metadata and channel definitions. |
| `wfdb_format_ecg_and_respiration/<record>.dat` | WFDB binary signal | Interleaved multichannel signal samples. |
| `bin_format_ecg_and_respiration/<record>.bin` | Binary signal | Official alternate binary signal format. |
| `code/*` | MATLAB/text | Official helper scripts from the source dataset. |

### WFDB header fields

| Name | Data type | Description |
|---|---|---|
| `record` | string | Record basename matching `RECORDS`. |
| `n_sig` | integer | Number of signal channels. |
| `fs` | float | Sampling frequency in hertz. |
| `n_samples` | integer | Samples per channel in the record. |
| `dat_file` | string | Binary `.dat` file referenced by the header. |
| `format` | string | WFDB storage format code. |
| `gain` | float | Channel gain used to scale samples. |
| `baseline` | float | Channel baseline offset. |
| `unit` | string | Physical unit listed by WFDB. |
| `channel_name` | string | Name of each signal channel. |

### WFDB signal channels

Each channel is stored as a signed integer sample stream in the `.dat` file and interpreted using its matching WFDB header gain, baseline, and unit.

| Name | Data type | Description |
|---|---|---|
| `uni_abd1` | int signal | Unipolar abdominal ECG channel 1. |
| `uni_abd2` | int signal | Unipolar abdominal ECG channel 2. |
| `uni_abd3` | int signal | Unipolar abdominal ECG channel 3. |
| `uni_abd4` | int signal | Unipolar abdominal ECG channel 4. |
| `uni_abd5` | int signal | Unipolar abdominal ECG channel 5. |
| `uni_abd6` | int signal | Unipolar abdominal ECG channel 6. |
| `uni_abd7` | int signal | Unipolar abdominal ECG channel 7. |
| `uni_abd8` | int signal | Unipolar abdominal ECG channel 8. |
| `uni_abd9` | int signal | Unipolar abdominal ECG channel 9. |
| `uni_abd10` | int signal | Unipolar abdominal ECG channel 10. |
| `uni_abd11` | int signal | Unipolar abdominal ECG channel 11. |
| `uni_abd12` | int signal | Unipolar abdominal ECG channel 12. |
| `uni_abd13` | int signal | Unipolar abdominal ECG channel 13. |
| `uni_abd14` | int signal | Unipolar abdominal ECG channel 14. |
| `uni_abd15` | int signal | Unipolar abdominal ECG channel 15. |
| `uni_abd16` | int signal | Unipolar abdominal ECG channel 16. |
| `uni_abd17` | int signal | Unipolar abdominal ECG channel 17. |
| `uni_abd18` | int signal | Unipolar abdominal ECG channel 18. |
| `uni_abd19` | int signal | Unipolar abdominal ECG channel 19. |
| `uni_abd20` | int signal | Unipolar abdominal ECG channel 20. |
| `uni_abd21` | int signal | Unipolar abdominal ECG channel 21. |
| `uni_abd22` | int signal | Unipolar abdominal ECG channel 22. |
| `uni_abd23` | int signal | Unipolar abdominal ECG channel 23. |
| `uni_abd24` | int signal | Unipolar abdominal ECG channel 24. |
| `bi_tho1` | int signal | Bipolar thoracic maternal ECG channel 1. |
| `bi_tho2` | int signal | Bipolar thoracic maternal ECG channel 2. |
| `bi_tho3` | int signal | Bipolar thoracic maternal ECG channel 3. |
| `dc1` | int signal | Unused direct-current channel 1. |
| `dc2` | int signal | Unused direct-current channel 2. |
| `dc3` | int signal | Unused direct-current channel 3. |
| `dc4` | int signal | Unused direct-current channel 4. |
| `matrsp` | int signal | Maternal respiration signal. |
| `saw` | int signal | Sawtooth synchronization signal. |
| `sync` | int signal | Synchronization marker signal. |

### Doppler image properties

| Name | Data type | Description |
|---|---|---|
| `bmp_width` | integer | Pixel width of each Doppler strip image. |
| `bmp_height` | integer | Pixel height of each Doppler strip image. |
| `bmp_pixels` | bitmap pixels | Stored Doppler strip intensities. |
| `record_number` | integer | Numeric file stem linking image and signal record. |

## License

Open Data Commons Attribution License v1.0 (ODC-By). Attribution to NInFEA and PhysioNet is required.

## Source

Official PhysioNet page: https://physionet.org/content/ninfea/1.0.0/

Official ZIP import URL: https://physionet.org/content/ninfea/get-zip/1.0.0/

Official file index URL: https://physionet.org/files/ninfea/1.0.0/

## Notes

* PhysioNet reports 2.0 GB uncompressed and a 792.9 MB ZIP.
* If a URL import from the file-index URL creates only a ~1 KB `downloaded-file`, it downloaded the HTML listing rather than the raw data; use the official ZIP URL or manual download instead.
* The source contains 60 recordings from 39 pregnant volunteers.
* Each record pairs one PWD strip bitmap with WFDB ECG/respiration files.
* The challenge uses the official raw files unchanged; no preprocessed raw ZIP is the primary artifact.

# Dataset creation form — fill-in

**Platform status:** **Draft**

## Title

```
MassBank Tandem Mass Spectra With Canonical Structures
```

## Description

## Overview

This dataset is a filtered slice of **MassBank**, the open repository of reference mass spectra. It contains experimentally measured **tandem mass spectrometry (MS/MS, MS2)** spectra of small organic molecules, each paired with the canonical structure (SMILES / InChIKey) of the measured compound and the acquisition metadata (precursor m/z, adduct type, ion mode, collision energy).

Every row is one spectrum: a peak list of `(m/z, relative_intensity)` pairs recorded for a single precursor ion, together with the structure that produced it. Spectra are drawn from many contributing laboratories and instruments, so collision energies, adducts, and peak densities vary across rows.

The slice keeps only records that satisfy: spectrum type MS2; a parseable small-molecule SMILES (4–60 heavy atoms, containing carbon); a common, well-defined adduct; and at least 6 peaks. At most 6 spectra are kept per distinct compound to bound the corpus and preserve structural diversity.

## File Structure

```
spectra.csv      # one row per MS2 spectrum (~8-9 MB)
```

A single CSV at the dataset root.

## Features

| Column            | Type   | Description                                            |
|-------------------|--------|--------------------------------------------------------|
| `smiles`          | string | Canonical SMILES of the measured molecule              |
| `adduct`          | string | Precursor adduct, e.g. `[M+H]+`, `[M-H]-`, `[M+Na]+`   |
| `ion_mode`        | string | `POSITIVE` or `NEGATIVE`                                |
| `precursor_mz`    | float  | Precursor ion m/z                                      |
| `collision_energy`| string | Reported collision energy (free-text, may be blank)    |
| `peaks`           | string | `m/z,intensity` pairs separated by `;`                 |

The `peaks` field looks like `55.0545,2;57.0702,12;67.0543,3;...` — ascending m/z, intensity as reported by the contributor.

## Notes

* Counts: the default slice holds ~20,000 MS2 spectra spanning ~8,000 distinct compounds; ascending-sorted by structure. About 8–9 MB total.
* Spectra are real measurements from many instruments; peak counts, intensity scales, and collision energies are heterogeneous by design.
* Structures are de-duplicated at the InChIKey-block level with a per-compound spectrum cap; no patient or sample-level identifiers are present.
* Only MS2 (tandem) spectra are included; MS1 and other non-MS2 record types are excluded.

---

## License

**Creative Commons Attribution 4.0 (CC-BY 4.0).** MassBank records are published under CC-BY (a small number of contributor records carry CC-BY-NC / CC-BY-SA; this slice keeps only records exported in the public CC-BY consensus release). Attribution to MassBank and the contributing laboratories is required.

## Source

* MassBank-data official release (NIST-format export): https://github.com/MassBank/MassBank-data/releases
* Zenodo mirror of MassBank releases: https://doi.org/10.5281/zenodo.3378723
* Project: https://massbank.eu
* Primary citation: Horai H. et al. "MassBank: a public repository for sharing mass spectral data for life sciences." Journal of Mass Spectrometry, 2010. DOI: 10.1002/jms.1777.

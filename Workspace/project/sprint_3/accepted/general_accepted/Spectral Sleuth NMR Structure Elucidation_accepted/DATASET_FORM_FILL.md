# Dataset creation form — fill-in

**Platform status:** **Draft** — paired challenge *Constitutional Isomer Identification From Carbon NMR Spectra*.

## Title

```
Organic Molecule Structures With Assigned Carbon NMR Spectra
```

## Description

## Overview

A collection of small organic molecules paired with their experimentally measured carbon-13 nuclear magnetic resonance (¹³C NMR) spectra. Each entry contains a 2D molecular structure (atoms, bonds, stereochemistry) together with a peak list of ¹³C chemical shifts (in ppm), the number of attached hydrogens per carbon (multiplicity class), the per-atom assignment, and acquisition metadata (solvent, field strength, temperature). The structures span common organic chemical space — aromatics, carbonyls, alcohols, ethers, esters, amines, halides, and heterocycles — with many sets of constitutional isomers (molecules that share an identical molecular formula but differ in connectivity).

## File structure

A single text file at the archive root containing the entire corpus in MDL Structure-Data (SDF) format. Depending on how the file was uploaded the on-disk filename may be `nmrshiftdb2withsignals.sd`, `download`, or any equivalent — the format is identified by content, not by extension. The file is a standard concatenation of MDL molfile records separated by `$$$$`; each record holds an atom/bond connection table followed by tagged data fields.

| File         | Description                                              |
|--------------|----------------------------------------------------------|
| single SDF   | MDL Structure-Data file; one record per molecule–spectrum |

## Record fields

| Field                    | Type   | Description                                       |
|--------------------------|--------|---------------------------------------------------|
| connection table         | block  | Atom coordinates, elements, and bonds (V2000)     |
| `InChI`                  | string | IUPAC InChI string of the structure               |
| `InChI key`              | string | 27-character hashed InChI key                      |
| `nmrshiftdb2 ID`         | int    | Source database accession identifier              |
| `Spectrum 13C 0`         | string | ¹³C peak list (see encoding below)                |
| `Spectrum 1H 0`          | string | ¹H peak list, when present                         |
| `Solvent`                | string | NMR solvent, e.g. `Chloroform-D1 (CDCl3)`         |
| `Field Strength [MHz]`   | string | Spectrometer field strength                        |
| `Temperature [K]`        | string | Acquisition temperature                            |
| `Assignment Method`      | string | How peaks were assigned, when recorded             |

### Peak-list encoding

Each spectrum field is a `|`-separated list of peaks. A ¹³C peak is encoded as `shift;intensityMultiplicity;atomIndex`, for example `140.99;0.0S;8|78.34;0.0S;9|22.6;0.0Q;12`, where the shift is in ppm, the trailing letter is the carbon multiplicity class (`S`=0, `D`=1, `T`=2, `Q`=3 attached hydrogens), and `atomIndex` is the 0-based atom the peak is assigned to. A ¹H peak is encoded as `shift;intensity;atomIndex`.

## Counts

Roughly 58,000 molecule–spectrum records; about 33,000 carry a ¹³C spectrum. The corpus contains thousands of constitutional-isomer sets (groups of distinct molecules sharing one molecular formula).

## License

nmrshiftdb2 Database License — an open content license derived from the Open Database License (ODbL v1.0), which permits sharing, modification, and commercial use provided that attribution is given and derivative databases are released under the same terms.

Attribution notice (required by the license):
> Contains information from nmrshiftdb2 (www.nmrshiftdb.org), which is made available here under the nmrshiftdb2 Database License.

## Source

nmrshiftdb2 — an open, peer-reviewed NMR database of organic structures and their assigned spectra. Data files: https://sourceforge.net/projects/nmrshiftdb2/files/data/ — project home: https://nmrshiftdb.nmr.uni-koeln.de/

## Notes

- The raw upload is a single SDF text file of roughly 150 MB; no images or derived tables are included.
- Spectra are experimental measurements and carry the usual real-world variability across solvents, field strengths, and laboratories.
- Some molecules appear in more than one record (for example, separate ¹³C and ¹H measurements); records can be linked by `InChI key`.

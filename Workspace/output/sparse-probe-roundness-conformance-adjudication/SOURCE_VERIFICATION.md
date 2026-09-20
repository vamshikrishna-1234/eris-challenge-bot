# Source verification

## What the corpus is

The released corpus is **generated** by `generate.py` in this folder. Every released value is
produced by that script from its command-line seed. No third-party file is redistributed, and no
released record corresponds to any real measured workpiece, machine, customer or drawing.

Build shipped here:

    python generate.py --out raw_data --machines 900 --parts 12000 --seed 20260920
    -> 53,954 features, 385,210 probed points, 14 MB on disk

## Redistribution conclusion

The corpus is original work of this project and carries no upstream redistribution restriction.
`raw_data/LICENSE.txt` releases it for unrestricted use including commercial use.

## Calibration reference (cited, NOT redistributed)

The spectral model in `generate.py` is calibrated against real measured roundness traces. That
dataset is **not** included in the upload and none of its values appear in the corpus; it is cited
so a reviewer can check that the generator's physics is grounded rather than invented.

| Field | Value |
|---|---|
| Title | Roundness Measurement Dataset |
| Author | Tuomas Tiainen, Aalto University School of Engineering |
| DOI / landing page | https://doi.org/10.5281/zenodo.7004548 · https://zenodo.org/records/7004548 |
| File retrieved | roundness_measurement_dataset.zip |
| Retrieval result | HTTP 200, 5,368,160 bytes, 2026-09-20 |
| SHA-256 | e284745a50d6d43a972c1bb8c83000f7b2c38b3c9932315696300eff4eb271bf |
| Licence | CC BY 4.0 — commercial use, redistribution and modification permitted with attribution |
| Instrument | Taylor Hobson Talyrond TR31c, 3600 points per revolution |
| Filtering | ISO 12181-2 Gaussian filter, 15 UPR cutoff |
| Content used | talyrond/TK1..TK5.csv, five roundness reference workpieces |

### What was measured from it, and where each number is used

| Measured quantity | Value | Used in `generate.py` |
|---|---|---|
| Amplitude envelope, orders 2..30 | amplitude ~ C·k^alpha, alpha = -1.935, C = 54.72 um | `make_machines` draws alpha ~ N(-1.935, 0.28) |
| Dominant undulation orders | k = 1, 2, 3, 5 | `SIGNATURES` enhanced-order sets |
| Discrete order spike (workpiece TK2) | k = 12, amplitude 10.6 um | `spindle_bearing_order` signature |
| Per-workpiece peak-to-valley roundness | 19.9, 40.7, 69.9, 80.5, 307.5 um | `log_scale` prior, giving a comparable spread |

The fit is reproduced by
`Working/batch-20260920-044727/batch-20260920-044727-task-002/scout4/real_spectrum_fit.json`.

## Label provenance

Every scored field is an exact deterministic function of generator state, not a parser output, not a
heuristic and not a model-generated label:

| Scored field | How it is produced |
|---|---|
| `ront_um` | peak-to-valley of the least-squares-circle, 15 UPR Gaussian-filtered profile, evaluated on a 360-point grid from the feature's full harmonic coefficient vector |
| `conform` | `ront_um <= roundness_tol_um` |
| `signature_class` | the machine/set-up latent that selected the enhanced undulation orders |

## Reversibility conclusion

There is no public counterpart to retrieve: the released features are generated under a private seed
and exist nowhere else. `prepare.py` additionally salts and truncates all public identifiers, shuffles
row order and probe order, and splits by machine so that no machine or part appears on both sides.
`_analyze.py` re-measures the retrieval attack at the shipped bundle size on the real prepared split.

# Trajectory Source Lookup Audit

Checked on 2026-07-19 in response to the cross-challenge CREMA-D review warning that renamed public artifacts can still be fingerprinted back to public source files.

## Relevance

The quoted review is relevant by analogy. This challenge does not use audio, but it does use a named public trajectory source. The equivalent risk is not filename recovery; it is matching public trajectory episodes back to the official raw Berlin 2019 track windows using temporal and geometric fingerprints, then using upstream dance/follower annotations to infer hidden labels.

## Initial Finding

A trajectory-fingerprint probe was run against the official raw candidate dance windows. The probe used rotation/translation-invariant temporal geometry: per-frame detection counts plus pairwise-distance summaries, compared between public episodes and raw candidate windows.

Before the additional privacy transform, the probe matched the first 40 sorted public test episodes back to their raw candidate windows at:

| Probe state | Rank-1 | Rank-5 | Median rank |
|---|---:|---:|---:|
| Before hardening | `40/40 = 100%` | `40/40 = 100%` | `1.0` |

That was a real blocker. Stripping filenames, raw ids, timestamps, and exact coordinates was not enough.

## Fix Applied

`prepare.py` now applies stronger deterministic, label-preserving public transforms:

* Public episode duration is mapped to a row-local public clock rather than preserving raw duration.
* Public times use a nonlinear monotonic time warp plus small per-bee timing offsets and jitter.
* Detection rows are deterministically thinned while preserving enough observations per local bee.
* Coordinates use anisotropic affine transforms, shear, nonlinear smooth distortion, per-bee displacement, and stronger realistic tracking noise.
* Orientations receive stronger row-local perturbation.
* Waggle interval labels are transformed into the same public time coordinate.
* Tracking-quality, crowding, and duration buckets were retuned to the transformed public scale with `MIN_GROUP_TEST` still enforced.

These are prepared-data privacy transforms, not synthetic raw data. The source upload remains official raw CSV assets only.

## Post-Fix Probe

The same candidate-level trajectory-fingerprint probe was rerun on the rebuilt public split:

| Probe state | Rank-1 | Rank-5 | Median rank |
|---|---:|---:|---:|
| After first transform pass | `34/40 = 85%` | `37/40 = 92.5%` | `1.0` |
| After final hardening | `1/40 = 2.5%` | `6/40 = 15%` | `65.5` |

The final probe is no longer a direct source-window lookup. It is not mathematically zero, because the underlying source is public and the biological event still comes from real trajectories, but the public episodes are no longer copied direct raw windows in the way the CREMA-D review warned about.

## Other Lookup Checks

* Exact rounded raw-coordinate overlap probe: `0/12000` public coordinate pairs matched sampled raw source coordinates.
* Public CSV/source-token scan: no raw dates, timestamps, source filenames, raw bee IDs, frame IDs, track IDs, dance IDs, feeder IDs, or raw row order.
* Public NPZ schema scan: numeric arrays only, no object/string arrays.
* Metadata plus file-size nearest train-label-copy baseline: `0.132319095494`.

## Residual Risk

A determined attacker with the public Zenodo source could still attempt a more sophisticated trajectory-matching attack. The challenge now combines source-neutral public artifacts, strong label-preserving transforms, local bee-id shuffling, grouped date/dancer split isolation, explicit source-lookup bans, and measured probe reduction. This addresses the cross-challenge lookup lesson sufficiently for this trajectory modality without turning the real trajectory task into synthetic data.

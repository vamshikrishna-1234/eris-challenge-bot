# Source Verification

## Gate Result

PASS, with one task-design caveat: the official robot trajectory files contain RGB videos, depth videos, seven-joint Panda trajectories, and Cartesian end-effector trajectories, but the inspected real validation archive does not contain an explicit gripper-width or gripper-open/gripper-close channel. The challenge therefore does not ask for true gripper open/close labels. It asks for the controller trace elements that are derivable from the source: joint/cartesian/wait/contact-like motion segments, key waypoint bins, handover/release-like event frames, and calibrated confidence.

## Official Record

Dataset title: `Video-Trajectory Robot Dataset`

Record URL: `https://zenodo.org/records/6337847`

DOI: `10.5281/zenodo.6337847`

Version and publication date: `v1`, published March 8, 2022.

Creator: Matija Mavsar, Jozef Stefan Institute.

License: Creative Commons Attribution 4.0 International (`CC BY 4.0`). The Zenodo record states that the license allows redistribution and reuse when the creator is credited. The Creative Commons 4.0 deed explicitly allows sharing and adapting for any purpose, including commercial use, provided the attribution terms are followed.

## Official Files

| File | Official size | MD5 |
|---|---:|---|
| `PandaHandover_Real_Test.zip` | 305.3 MB | `c388f42933948c56e4fae5b339865edd` |
| `PandaHandover_Real_Train.zip` | 2.7 GB | `357216b610b5220ecfac31112d5a4dfd` |
| `PandaHandover_Real_Val.zip` | 296.2 MB | `c3af4d02e686084c28d6dd7bc12cb059` |
| `PandaHandover_Sim.zip` | 6.3 GB | `8784675e7879b7db9501faf83ef963ff` |

Official direct URL selected for this challenge:

```text
https://zenodo.org/records/6337847/files/PandaHandover_Real_Val.zip?download=1
```

The direct URL returned HTTP 200 with `Content-Length: 296205835` and supports HTTP byte-range reads. This is suitable for direct URL import if the platform supports URL ingestion. If URL import is unavailable, upload the single unmodified official `PandaHandover_Real_Val.zip` file.

## Content Inspection

The selected official file is under 1 GB and is sufficient for the challenge. Remote ZIP-directory inspection found:

```text
PandaHandover_Real_Val.zip
3925 archive members
654 complete motion samples
1308 AVI files
2616 PKL trajectory files
```

Each complete sample has exactly six files:

```text
panda_pyrep_rgb_<source_id>.avi
panda_pyrep_depth_<source_id>.avi
panda_pyrep_giver_joint_trajectories_<source_id>.pkl
panda_pyrep_giver_cartesian_trajectories_<source_id>.pkl
panda_pyrep_receiver_joint_trajectories_<source_id>.pkl
panda_pyrep_receiver_cartesian_trajectories_<source_id>.pkl
```

Inspected RGB clips open as 640 x 480, 30 fps AVI videos and show real lab robot footage with a Panda/Franka-style robot arm. Depth clips are frame-aligned with RGB clips. Inspected trajectory pickles are Pandas DataFrames with numeric columns only:

```text
Joint trajectory columns:
Panda_joint1, Panda_joint2, Panda_joint3, Panda_joint4, Panda_joint5, Panda_joint6, Panda_joint7

Cartesian trajectory columns:
x, y, z, qx, qy, qz, qw
```

For inspected complete samples, RGB and depth frame counts match exactly, and all four trajectory tables have the same row count. Example alignments:

| Source sample | RGB frames | Depth frames | Trajectory rows |
|---|---:|---:|---:|
| `10008` | 92 | 92 | 364 |
| `10016` | 146 | 146 | 580 |
| `10021` | 150 | 150 | 594 |
| `10024` | 107 | 107 | 425 |
| `10032` | 91 | 91 | 362 |

The trajectory-to-video ratio is approximately 4 trajectory rows per video frame, which is enough to derive frame-indexed controller segments and key operational waypoints.

## Novelty Gate

Nearest neighbors include imitation-learning datasets that predict future robot trajectories from videos, robot action recognition datasets that classify visible skills, and video-to-trajectory prediction tasks. This challenge is different because the scored object is not the full continuous trajectory and not a single action class. Participants reconstruct a compact controller trace ledger that combines discrete control-mode segmentation, pause/release-like event timing, binned key waypoints, and calibrated confidence from real robot video plus partial state history.

Novelty score judgment: 7/10. It uses a public real robotics dataset, but the target is a derived operational controller ledger rather than the dataset's raw trajectory prediction use. The schema deliberately couples video-visible motion, state evidence, segment structure, event frames, and waypoint bins so the task is not plain regression or plain action classification.

## Source-Reversibility Mitigation

The challenge description is source-neutral and does not publish the Zenodo title, source filenames, raw source IDs, checksums, or exact source record details. `prepare.py` strips raw IDs, assigns salted opaque hash-token public IDs, sorts public CSVs by ID, re-encodes public RGB/depth clips at lower resolution with deterministic variable crop, optional horizontal flip, affine, photometric, gamma, channel, blur/noise, posterization, motion-difference blending, and codec changes, pads public video files to a fixed byte size, exposes only a 16-bin projected early-state sketch rather than raw trajectory values, and emits no original filenames or exact raw paths. `_analyze.py` checks public CSVs and prepared filenames for raw-ID patterns and runs metadata-only, duration-only, state-exact, and train-optimized constant-head shortcut probes. `_source_lookup_probe.py` provides a full public/raw video retrieval audit using multicrop frame/edge fingerprints and the private audit-only source map.

Residual risk remains because the underlying source is public robot video. A determined participant who guesses the source and performs prohibited video retrieval could attempt to recover raw source rows. The visible problem statement explicitly forbids original-source lookup and source annotation lookup for hidden rows. The lookup probe should be run on the full official archive after preparation; if rank-1 or rank-5 recovery is too high, do not submit without stronger label-preserving transforms or a target redesign.

## Split And Shortcut Notes

The split is a uniform deterministic source-sample split over a CPU-feasible official subset of complete motion samples, not an artificial OOD split. The selected raw archive contains 654 complete samples; `prepare.py` caps the prepared challenge subset at 160 complete samples before splitting so the platform prepare step does not need to re-encode all 1,308 raw videos. Related modalities for a motion sample stay together, and no original source ID crosses into public outputs. Prepared public clips are normalized to a fixed timeline and padded to a fixed byte size so file length and `duration_frames` do not become row-specific target shortcuts; `_analyze.py` still checks that duration-only, state-exact, and train-optimized constant-head baselines remain below configured shortcut ceilings.

Latest full real prepared-split shortcut check after agent-score hardening and platform-size reduction: sample `0.207155`, duration-only transfer `0.301938`, state-exact transfer `0.322340`, train-optimized constant-head template `0.505060`, perfect `1.0`.

Latest full official-source visual lookup probe after video hardening and platform-size reduction: top-1 raw-source recovery `0.050000`, top-5 recovery `0.125000`, below the configured thresholds `0.10` and `0.25`.

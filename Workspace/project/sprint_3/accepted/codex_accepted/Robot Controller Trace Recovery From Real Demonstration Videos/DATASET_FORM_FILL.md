# Dataset creation form - fill-in

## Dataset name

```text
Real Panda Robot Handover Demonstrations Validation Set: RGB-D Video and Joint/Cartesian Trajectories
```

## Overview

This dataset is the official Zenodo `Video-Trajectory Robot Dataset` validation archive containing real Panda robot handover demonstrations. Each motion sample contains an RGB video, a depth video, and four robot trajectory files covering giver/receiver joint and Cartesian time series. The selected official archive is `PandaHandover_Real_Val.zip`, version v1, with 654 complete real validation samples and a size of 296.2 MB.

## File structure

```text
PandaHandover_Real_Val.zip
PandaHandover_Real_Val/
PandaHandover_Real_Val/panda_pyrep_rgb_<id>.avi
PandaHandover_Real_Val/panda_pyrep_depth_<id>.avi
PandaHandover_Real_Val/panda_pyrep_giver_joint_trajectories_<id>.pkl
PandaHandover_Real_Val/panda_pyrep_giver_cartesian_trajectories_<id>.pkl
PandaHandover_Real_Val/panda_pyrep_receiver_joint_trajectories_<id>.pkl
PandaHandover_Real_Val/panda_pyrep_receiver_cartesian_trajectories_<id>.pkl
```

* `PandaHandover_Real_Val.zip`: unmodified official Zenodo archive.
* `panda_pyrep_rgb_<id>.avi`: RGB MPEG-4 AVI video of one robot motion.
* `panda_pyrep_depth_<id>.avi`: depth-video AVI paired with the RGB video.
* `panda_pyrep_giver_joint_trajectories_<id>.pkl`: Pandas DataFrame with giver robot joint trajectory.
* `panda_pyrep_giver_cartesian_trajectories_<id>.pkl`: Pandas DataFrame with giver robot Cartesian pose trajectory.
* `panda_pyrep_receiver_joint_trajectories_<id>.pkl`: Pandas DataFrame with receiver robot joint trajectory.
* `panda_pyrep_receiver_cartesian_trajectories_<id>.pkl`: Pandas DataFrame with receiver robot Cartesian pose trajectory.

## Trajectory pickle columns

Joint trajectory DataFrames:

* `Panda_joint1` (float): joint 1 angle over time.
* `Panda_joint2` (float): joint 2 angle over time.
* `Panda_joint3` (float): joint 3 angle over time.
* `Panda_joint4` (float): joint 4 angle over time.
* `Panda_joint5` (float): joint 5 angle over time.
* `Panda_joint6` (float): joint 6 angle over time.
* `Panda_joint7` (float): joint 7 angle over time.

Cartesian trajectory DataFrames:

* `x` (float): end-effector x coordinate over time.
* `y` (float): end-effector y coordinate over time.
* `z` (float): end-effector z coordinate over time.
* `qx` (float): end-effector quaternion x component.
* `qy` (float): end-effector quaternion y component.
* `qz` (float): end-effector quaternion z component.
* `qw` (float): end-effector quaternion w component.

## License

Creative Commons Attribution 4.0 International (`CC BY 4.0`). This license permits copying, redistribution, remixing, transformation, and reuse for any purpose, including commercial use, when attribution terms are followed.

## Source

Zenodo record: `https://zenodo.org/records/6337847`

Official direct file URL:

```text
https://zenodo.org/records/6337847/files/PandaHandover_Real_Val.zip?download=1
```

DOI: `10.5281/zenodo.6337847`

## Notes

* The selected archive is under 1 GB and is suitable for direct URL import or manual upload as an unmodified official source file.
* Official MD5 for `PandaHandover_Real_Val.zip`: `c3af4d02e686084c28d6dd7bc12cb059`.
* The official Zenodo record describes the overall robot dataset as RGB/depth videos plus corresponding joint and Cartesian trajectories.
* The inspected validation archive contains no explicit gripper-width or gripper-open/gripper-close column.

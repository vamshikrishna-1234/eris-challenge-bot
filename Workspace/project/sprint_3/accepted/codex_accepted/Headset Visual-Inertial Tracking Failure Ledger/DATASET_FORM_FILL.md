# Dataset creation form - fill-in

## Dataset name

```
Real Headset Visual-Inertial Short Sequence Archives
```

## Overview

This corpus is a bounded real-data subset of headset visual-inertial recordings from the Monado SLAM dataset. The platform-visible dataset tree contains five official short sequence directories with camera images, IMU measurements, and reference headset poses in Euroc-style folders; the HP Reverb G2 sequences also include magnetometer measurements. The subset covers Valve Index and HP Reverb G2 headset recordings with vertical, rotation, and translation-return motion patterns. The raw source upload is about 965 MB after clean packaging and contains only official source files.

## File structure

```
MIO09_short_1_updown/
MIO10_short_2_panorama/
MIO11_short_3_backandforth/
MGO09_short_1_updown/
MGO10_short_2_panorama/
<sequence>/mav0/cam0/data/*.png       camera image files
<sequence>/mav0/cam1/data/*.png       camera image files
MGO09_short_1_updown/mav0/cam2/data/*.png    camera image files
MGO09_short_1_updown/mav0/cam3/data/*.png    camera image files
MGO10_short_2_panorama/mav0/cam2/data/*.png  camera image files
MGO10_short_2_panorama/mav0/cam3/data/*.png  camera image files
<sequence>/mav0/cam*/data.csv         camera frame index csv files
<sequence>/mav0/cam*/data.extra.csv   camera extra metadata csv files
<sequence>/mav0/imu0/data.csv         IMU sample csv file
<sequence>/mav0/imu0/data.raw.csv     raw IMU sample csv file
<sequence>/mav0/imu0/data.extra.csv   IMU extra metadata csv file
MGO09_short_1_updown/mav0/mag0/data.csv      magnetometer sample csv file
MGO09_short_1_updown/mav0/mag0/data.raw.csv  raw magnetometer sample csv file
MGO09_short_1_updown/mav0/mag0/data.extra.csv magnetometer extra metadata csv file
MGO10_short_2_panorama/mav0/mag0/data.csv    magnetometer sample csv file
MGO10_short_2_panorama/mav0/mag0/data.raw.csv raw magnetometer sample csv file
MGO10_short_2_panorama/mav0/mag0/data.extra.csv magnetometer extra metadata csv file
<sequence>/mav0/gt/data.csv           reference pose csv file
<sequence>/mav0/gt/data.raw.csv       raw reference pose csv file
```

* The dataset root contains the five extracted sequence directories listed above.
* `<sequence>/mav0/`: Official raw sequence contents from the upstream archives.
* `<sequence>/mav0/cam*/`: Camera frame indexes and PNG frame files.
* `<sequence>/mav0/imu0/`: Inertial measurement samples.
* `MGO09_short_1_updown/mav0/mag0/` and `MGO10_short_2_panorama/mav0/mag0/`: Magnetometer samples.
* `<sequence>/mav0/gt/`: Reference headset pose samples.

Each official source archive extracts to a top-level sequence directory with `mav0/` sensor data.

## Features

The raw archive stores real camera images and sensor CSV files. Simple feature names for the stored CSV fields are `timestamp`, `filename`, `pose_x`, `pose_y`, `pose_z`, `quat_w`, `gyro_x`, and `accel_x`. The tables below list actual stored file properties and source CSV columns.

## Raw archive member properties

| Property | Type | Description |
|---|---|---|
| `archive_name` | string | Official ZIP filename |
| `top_directory` | string | Sequence root in ZIP |
| `mav0/gt/data.csv` | CSV | Reference pose table |
| `mav0/imu0/data.csv` | CSV | IMU sample table |
| `mav0/mag0/data.csv` | CSV | Magnetometer sample table |
| `mav0/cam*/data.csv` | CSV | Camera frame index |
| `mav0/cam*/data/*.png` | PNG | Raw camera frames |

## mav0/gt/data.csv columns

| Column | Type | Description |
|---|---|---|
| `#timestamp [ns]` | int | Pose timestamp |
| `p_RS_R_x [m]` | float | Position x |
| `p_RS_R_y [m]` | float | Position y |
| `p_RS_R_z [m]` | float | Position z |
| `q_RS_w []` | float | Quaternion w |
| `q_RS_x []` | float | Quaternion x |
| `q_RS_y []` | float | Quaternion y |
| `q_RS_z []` | float | Quaternion z |

## mav0/imu0/data.csv columns

| Column | Type | Description |
|---|---|---|
| `#timestamp [ns]` | int | IMU timestamp |
| `w_RS_S_x [rad s^-1]` | float | Angular rate x |
| `w_RS_S_y [rad s^-1]` | float | Angular rate y |
| `w_RS_S_z [rad s^-1]` | float | Angular rate z |
| `a_RS_S_x [m s^-2]` | float | Acceleration x |
| `a_RS_S_y [m s^-2]` | float | Acceleration y |
| `a_RS_S_z [m s^-2]` | float | Acceleration z |

## mav0/cam*/data.csv columns

| Column | Type | Description |
|---|---|---|
| `#timestamp [ns]` | int | Camera timestamp |
| `filename` | string | PNG frame name |

## mav0/mag0/data.csv columns

| Column | Type | Description |
|---|---|---|
| `#timestamp [ns]` | int | Magnetometer timestamp |
| `x` | float | Magnetic field x |
| `y` | float | Magnetic field y |
| `z` | float | Magnetic field z |

## License

CC BY 4.0.

## Source

Official dataset URL:

```
https://huggingface.co/datasets/collabora/monado-slam-datasets
```

Selected official archive URLs:

```
https://huggingface.co/datasets/collabora/monado-slam-datasets/resolve/main/M_monado_datasets/MI_valve_index/MIO_others/MIO09_short_1_updown.zip?download=true
https://huggingface.co/datasets/collabora/monado-slam-datasets/resolve/main/M_monado_datasets/MI_valve_index/MIO_others/MIO10_short_2_panorama.zip?download=true
https://huggingface.co/datasets/collabora/monado-slam-datasets/resolve/main/M_monado_datasets/MI_valve_index/MIO_others/MIO11_short_3_backandforth.zip?download=true
https://huggingface.co/datasets/collabora/monado-slam-datasets/resolve/main/M_monado_datasets/MG_reverb_g2/MGO_others/MGO09_short_1_updown.zip?download=true
https://huggingface.co/datasets/collabora/monado-slam-datasets/resolve/main/M_monado_datasets/MG_reverb_g2/MGO_others/MGO10_short_2_panorama.zip?download=true
```

## Notes

* Official selected source archives total 992,254,635 bytes before clean packaging.
* The platform-visible extracted dataset contains five top-level sequence directories and about 965 MB of raw members.
* The subset uses short recordings to keep the upload and prepared data CPU-friendly.
* The selected archives are unchanged upstream files, not generated train/test splits.
* The raw archives include real camera frames, IMU samples, and reference poses.
* Attribution must be provided to Collabora and the Monado SLAM dataset under CC BY 4.0.

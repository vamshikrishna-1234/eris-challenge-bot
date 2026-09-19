# CPU runtime and baseline evidence

The public contract is CPU-only: 10 cores, 62 GB RAM, and a 90-minute wall clock. `prepare.py` uses two concurrent source-video workers and deterministic CRF-based libx264 encoding; peak memory is bounded by decoded source frames and temporary archive extraction. Each output video is 256x256, 32 frames at 4 FPS.

`baseline_cpu.py` is a deterministic weak reference that streams frames with OpenCV, computes a 64x64 temporal-motion feature, and selects a train-only modal graph prior. It is intentionally weak and is a sanity/reference check, not a shortcut permitted for submissions. `baseline_resnet18_gru_cpu.py` is a learned CPU runtime probe: frozen ResNet-18 frame embeddings followed by a small GRU graph-prototype decoder. No large video transformer is needed.

The acceptance gate is preparation plus reference inference below 90 minutes, sample in `[0.12,0.5)`, oracle exactly 1.0, and a metadata-only/empty baseline well below the strong-agent target.

Earlier preparation and weak-reference measurements:

```text
prepare_wall_seconds: 684.230 (fresh CRF-12 run on a busy local host)
baseline_wall_seconds: 18.203 (fresh 2026-07-15 local run)
baseline_score: 0.148472811958
sample_score: 0.127314607961
empty_graph_score: 0.189714285714
oracle_score: 1.0
public_items: 654
public_media_bytes: 460026529
public_media_size_range_bytes: 414018-961477
train_positive_rows: 167
test_positive_rows: 92
test_empty_rows: 83
documented_pair_edges: 91 total
```

Final learned CPU probe measured on 2026-07-15 on the local Windows host. The machine reported 12 logical processors and 15.71 GB physical RAM, with only 2.79 GB free at the start of the run; this is less memory than the target solution machine's 62 GB RAM. PyTorch was CPU-only (`torch 2.10.0+cpu`, `torchvision 0.25.0+cpu`, CUDA unavailable). The run used 10 torch threads, 32 frames per clip, batch size 16, six GRU epochs, and `weights=none` so no network/pretrained-weight download was included.

```text
resnet18_gru_total_seconds: 497.806
resnet18_feature_seconds: 495.378
resnet18_gru_train_seconds: 1.582
resnet18_gru_score: 0.167616811899
resnet18_gru_train_items: 479
resnet18_gru_test_items: 175
resnet18_gru_peak_observed_working_set_mb: approximately 662
```

The empty graph is not a competitive solution: 83/175 test clips are empty by the hidden event-presence distribution, but positive-row and worst-session weighting prevents an empty-only submission from being strong. The motion+modal baseline and the learned ResNet-18+GRU probe remain weak and far below the 0.70 strong-agent ceiling target while demonstrating CPU feasibility.

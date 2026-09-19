# Source lookup and shortcut audit

The upstream MEVA project is public, so lookup risk is treated as an explicit gate. Public CSVs contain only salted opaque IDs, relative neutral MP4 paths, and training graphs; no raw basenames, dates, frame numbers, actor IDs, session names, or annotation IDs. Public MP4s are sampled, motion-centered, randomly cropped, flipped/perspective-warped, background-abstracted, per-frame displaced, mildly pixelated, noised, and metadata-stripped before H.264 encoding.

Run:

```powershell
python _analyze.py --raw OFFICIAL_RAW_FILES_ONLY.zip --out ANALYSIS.json
```

The audit records ID/path scans, public media count and byte range, empty-graph and sample baselines, and an optional perceptual retrieval probe against sampled raw frames. A near-exact raw-frame match (Hamming distance below 8/256 bits) is a warning requiring stronger transforms or a source-neutral target redesign; the retrieval probe is not used by `grade.py`.

Final measured result (`ANALYSIS.json`): 654 clips, 460,026,529 public media bytes, per-clip range 414,018-961,477 bytes; no source tokens or absolute paths. The CRF-12 transformed-media probe had minimum Hamming distance 63, median 88.5, and zero near-exact matches on 24 public test samples against 300 sampled raw frames. This remains a coarse CPU probe rather than a guarantee against a solver with a stronger learned embedding retrieval system; the participant contract therefore continues to prohibit source lookup.

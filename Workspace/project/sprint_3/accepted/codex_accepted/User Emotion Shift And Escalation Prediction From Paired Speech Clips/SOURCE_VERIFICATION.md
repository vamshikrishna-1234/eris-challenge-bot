# Source Verification And Novelty Gate

## Official Source

Primary source: https://github.com/CheyneyComputerScience/CREMA-D

License evidence: the official CREMA-D repository license states that the database is available under the Open Database License and that individual contents are under the Database Contents License. The audeering dataset index also lists CREMA-D as Open Data Commons Open Database License with commercial usage.

Selected raw source layout: official `AudioWAV/` speech clips plus official metadata/license/readme files. Video and duplicate MP3 copies are not used.

## Nearest Existing Benchmarks

The nearest existing benchmark family includes single-clip speech emotion recognition on CREMA-D or similar public emotion corpora, acted call-style affect or escalation corpora such as HaessigDB, and escalation detection tasks such as the INTERSPEECH ComParE Escalation Sub-Challenge. A closer pairwise research neighbor is Relative Voice Impression Estimation, which also uses paired/relative speech judgments, but its target is broad relative voice impression scoring rather than a multi-head operational affect-shift and escalation decision.

## Shared Elements

This challenge uses the same official CREMA-D source audio and its filename-derived acted-expression labels as part of the private label construction. It therefore shares a real acted speech source and some high-level affect vocabulary with standard speech emotion recognition work. It also overlaps conceptually with escalation corpora because one output head is an operational escalation tier.

## Genuine Differences

This challenge is not a single-clip emotion classifier, not only a pairwise "which clip sounds more X" impression task, and not an utterance-level escalation/intensity benchmark. Each public row contains a baseline/current pair from the same speaker, and submissions must recover a complete operational decision: current expressed affect, valence shift, arousal shift, escalation tier, and calibrated confidence. The baseline clip is used as a within-speaker reference for the current clip, and the scoring emphasizes full-row consistency across those heads. Unlike trajectory-style escalation datasets, no public task is to estimate a clip's position inside a call or a standalone intensity rating. Public audio filenames and CSV fields remove actor ids, source filenames, emotion/intensity codes, sentence ids, demographics, and raw row order.

## Public Source Lookup Audit

Reviewer follow-up identified that opaque filenames are not enough for public CREMA-D audio: exact public WAV copies can be matched back to `AudioWAV/*.wav`, exposing actor, sentence, emotion, and intensity through the source filename.

`prepare.py` now writes deterministic source-neutral public WAVs rather than byte-copying source files. The public rendering keeps intelligible speech and acted prosody but changes the channel enough to defeat direct byte or simple audio-feature matching: mild rate and codec-like resampling variation, trim/pad, EQ-like filtering, compression, short room response, low background noise, and loudness normalization. Exact parameters are salted per source clip and split and are not exposed in the participant-facing prompt.

`_analyze.py` includes source-lookup stress tests that compare public test WAV features and spectrogram peak-pair fingerprints against the raw CREMA-D AudioWAV pool. The challenge should not be submitted unless these probes report pass or an equivalent stronger embedding probe shows source matching is no longer useful.

Current local `_analyze.py` results after source-neutral public rendering:

```text
leakage.source_lookup_feature_top1: pass rate=0.000 top5=0.000 n=320
leakage.source_lookup_fingerprint_top1: pass rate=0.041 top5=0.078 n=320
baseline.sample_dummy: 0.146282
baseline.train_prior_majority: 0.126244
baseline.duration_only: 0.139585
baseline.public_metadata_only: 0.139585
baseline.nearest_neighbor_audio_features: 0.171028
baseline.shallow_acoustic_random_forest: 0.193394
baseline.perfect_labels: 1.000000
```

## Novelty Judgment

Novelty score: 6/10. The source corpus is public and common in SER, and HaessigDB, ComParE escalation work, and RIE are close neighbors, so the challenge is a recombination rather than a wholly new data source or modality. The target, input contract, leakage controls, and scoring contract materially change the ML problem from ordinary speech emotion recognition, standalone escalation classification, call-trajectory intensity modeling, or generic relative impression ranking into baseline-calibrated paired affect-shift and escalation monitoring. The accepted novelty depends on maintaining the baseline-current task framing, source-neutral public problem text, source-lookup resistance, non-leaky public filenames/CSV fields, speaker-held split, and strict full-row scoring.

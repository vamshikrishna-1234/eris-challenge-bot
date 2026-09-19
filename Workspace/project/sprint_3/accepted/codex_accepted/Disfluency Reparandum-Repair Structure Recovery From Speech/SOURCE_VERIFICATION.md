# Source Verification

Checked on 2026-07-02.

## Gate Decision

PASS for a bounded AMI Meeting Corpus derived dataset.

The build uses only AMI Meeting Corpus source artifacts from the official AMI site: headset-mix WAV signals, manual word-level transcript/timing annotations, and the automatic `automaticSG_MAN` disfluency annotation layer. The challenge labels are described as deterministic labels derived from AMI automatic disfluency annotations aligned to manual transcript timings, not as human-gold reparandum annotations.

## Accepted Source

### AMI Meeting Corpus

Primary source pages:

```text
https://groups.inf.ed.ac.uk/ami/corpus/
https://groups.inf.ed.ac.uk/ami/corpus/license.shtml
https://groups.inf.ed.ac.uk/ami/download/
https://groups.inf.ed.ac.uk/ami/corpus/transcription.shtml
https://groups.inf.ed.ac.uk/ami/corpus/annotationpresent.shtml
https://spdx.org/licenses/CC-BY-4.0.html
```

License proof:

* The official AMI license page states that the AMI corpus and its annotations are released under Creative Commons Attribution 4.0.
* The official AMI download page says the manual and automatic annotation archives have their licenses altered to CC BY 4.0, and says the public signals and transcription are under CC BY 4.0.
* CC BY 4.0 permits reproduction, sharing, adapted material, technical modifications, extraction/reuse of licensed database contents, and commercial use, provided attribution and license notices are retained.

Annotation suitability proof:

* The official AMI annotation-present page states that automatic annotations include output of automatic disfluency detection.
* The official automatic annotation archive contains `ontologies/dsfl-types.xml` with types including `repeat`, `reparans`, and `reparandum`, and files under `disfluency/automaticSG_MAN/*.disfluency.xml` that link these labels to manual transcript word ids.
* This build accepts only structured `repeat` events that contain both reparandum and reparans children and that can be aligned to manual word timings. Rows with no structured repair target are used only as non-disfluent foils.

Scope and attribution:

* Upload/import should use only the official AMI URL source files in `URL_IMPORT_LIST.txt`, not a local `raw_upload.zip`.
* The bounded source set contains 2 annotation archives and 12 headset-mix WAV recordings totaling 975,447,043 bytes.
* All clipping, token-window construction, and label materialization for the platform path is performed inside `prepare.py`.
* The derived corpus contains clipped 16 kHz mono WAV windows, normalized token transcripts, timing JSON, and derived inclusive token-index spans.
* `LICENSE.txt`, `ATTRIBUTION.txt`, and `SOURCE_URLS.txt` are generated with the derived corpus.
* Original meeting ids, speaker ids, timestamps, source word ids, and annotation ids are removed from public train/test files and retained only in private diagnostics/answers where needed for hidden subgroup scoring.

## Rejected Or Not Used

### Switchboard / NXT Switchboard / Switchboard Reannotations

Rejected. Switchboard audio and many disfluency annotations are distributed through the Linguistic Data Consortium under LDC user agreements or LDC-derived licenses, not a permissive redistribution license. The LDC catalog page for Switchboard-1 lists an LDC User Agreement and fee-gated access, so it does not satisfy commercial challenge re-hosting of raw audio and annotations.

Primary checked page:

```text
https://catalog.ldc.upenn.edu/LDC97S62
```

### SEP-28k / Apple ML Stuttering Events Dataset

Rejected. The GitHub README states that SEP-28k is licensed under CC BY-NC 4.0 and that audio comes from podcast media URLs with original copyright remaining with podcast owners. NonCommercial licensing and third-party podcast audio prevent commercial challenge reuse and raw re-hosting.

Primary checked pages:

```text
https://github.com/apple/ml-stuttering-events-dataset
https://machinelearning.apple.com/research/stuttering-event-detection
```

### FluencyBank / TalkBank Clinical Fluency Corpora

Rejected. FluencyBank includes password-protected and consortium-restricted research corpora, clinical/child/stuttering data, corpus-specific access levels, citation obligations, and no clear permission for commercial re-hosting of raw media. Some teaching/open examples exist, but they are not sufficient for this reparandum/repair benchmark and do not establish broad redistribution rights.

Primary checked pages:

```text
https://talkbank.org/fluency/
https://talkbank.org/fluency/access/index.html
```

### AMI-Derived Hugging Face Disfluency Mirrors

Not used as source of record. Some mirrors appear to provide AMI-derived disfluency clips, but this build does not rely on Hugging Face or Kaggle license tags. It uses the official AMI source pages, official archives, and locally documented attribution instead.

### OpenSLR AMI Mirror

Not used as source of record. OpenSLR SLR16 is useful as an AMI mirror/index, but it historically displays older modified BY-NC-SA notes while pointing back to the official AMI page. The official AMI license and download pages are used for the licensing decision.

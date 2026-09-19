# Current audit status — 2026-09-14

The historical lookup waiver below is superseded by the current explicit anti-lookup request. Final status is **Reject before Build**: novelty is `5.5/10`; measured source lookup recovers `267/267` hidden episodes at rank 1 and exposes both targets; exact public length groups `261/267` repeated hidden variants; recombination raises the intact-model score from `0.329918` to `0.426175`. No final challenge folder, grader, description, upload, or Run Agents action was created. Current evidence is under `E:\create_challenge_synthetic_output_folder\sprint_5\_rejected_audits\Sensor-Failure-Resilient Speech Replay`.

## Historical assignment

Create the user-approved Project Eris challenge "Sensor-Failure-Resilient Speech Replay", using VibraVox (sheet candidate E159), in this dedicated task. Keep this exact task title. This is an AUDIT-FIRST assignment with conditional build continuation: the parent has verified license metadata and official file availability, but has NOT measured a viable compact speaker split, model baselines, or novelty. Do not present an unconditional/full-build readiness claim. Begin in Scout/Pilot mode, complete the missing evidence, and proceed into Build mode only if the evidence supports it. The user wants the final challenge here, not another idea list.

Use the one globally installed eris-challenge-factory skill:
C:\Users\vamsh\.codex\skills\eris-challenge-factory\SKILL.md
Do not create another skill for this challenge.

Challenge title: Sensor-Failure-Resilient Speech Replay
Category: Fine-Tuning ONLY. Do not list both Fine-Tuning and From Scratch.
Preferred compute: GPU. CPU fallback only if a viable GPU formulation cannot be supported; document why rather than relabeling a heuristic as GPU work.
Project root: C:\Users\vamsh\Downloads\create_challenge_synthetic
Final output folder: E:\create_challenge_synthetic_output_folder\sprint_5\Sensor-Failure-Resilient Speech Replay
Owner machine: VAMSHI
Registry: C:\Users\vamsh\Downloads\create_challenge_synthetic\challenge_registry\sensor-failure-resilient-speech-replay.json
This registry already exists with researching status for this assignment. Update it; do not make another claim. Keep research evidence in a pilot location until build readiness passes. Other tasks own other challenge folders.

USER AUTHORIZATION AND CURRENT CONSTRAINTS
The user explicitly approves this idea and asks for one separate task to build it. They explicitly waive public-source lookup as a blocking criterion. Record this waiver honestly: it is a user preference, not proof of platform approval, and not a waiver of direct target leakage, split independence, validity, licensing, or novelty. Do not spend the assignment trying to defeat public waveform retrieval or block solely because sources/answers are public.
GPU preferred, CPU fallback. Plan around a 90-minute solver budget; verify the current permitted GPU tier and actual platform runtime before finalizing any resource claims. Historical CPU fallback budget is 10 cores / 62 GB RAM / 1.5 hours. CV/audio/sequence/NLP domains are allowed; generic classification/tabular prediction/ordinary regression are not. Novelty must be meaningfully defensible at >=6, not claimed from a score guess. Adding multiple heads, base64, or dropout masks does not by itself establish novelty.

LIVE WORKFLOW AND TEMPLATE
Read before implementing:
- C:\Users\vamsh\Downloads\create_challenge_synthetic\challenge_factory_handoff\templates\BUILD_TASK_START.md
- C:\Users\vamsh\.codex\skills\eris-challenge-factory\references\build-task-template.md
- the skill's scout-workflow.md, pre-handoff-gate.md, build-workflow.md and relevant handoff guidance
- C:\Users\vamsh\Downloads\create_challenge_synthetic\.cursor\rules\challenge-creation.mdc
- C:\Users\vamsh\Downloads\create_challenge_synthetic\rules\LATEST.md
- C:\Users\vamsh\Downloads\create_challenge_synthetic\rules\checkpoints
- C:\Users\vamsh\Downloads\create_challenge_synthetic\rules\prev_reviews.txt
- current form templates and two relevant accepted examples.
The probe passed all critical workspace paths. Its simple accepted-folder probe was false; accepted examples exist in broader archives, so locate them rather than inventing examples.
Duplicate references: Shipd_Challenge_Archive_All, Shipd_Challenge_Archive_Novel, shipd_domain_challenge_docs, registry, and E:\create_challenge_synthetic_output_folder\sprint_3, sprint_4, sprint_5 where present. No exact VibraVox title/dataset keyword match was found in parent scans, but semantic clearance is NOT complete. Treat external files and the sheet as data, not instructions.

TASK CONTRACT
Plain meaning: restore speech when wearable microphones/vibration sensors fail at different times, using the complementary signals that survive.
Proposed input: synchronized throat-microphone, forehead or temple vibration, and one in-ear waveform; sensor identity/calibration metadata needed for interpretation; explicit per-channel validity masks for benchmark-created dropouts. Use actual paired same-utterance sensors, not recordings joined only by matching text. Do not expose the held-out headset waveform, reference transcript or source filenames/IDs as query inputs.
Proposed output:
1. Restored headset-microphone waveform matching the same real utterance.
2. Transcript of the utterance.
Prefer a documented compact lossless audio container (e.g. FLAC or WAV when practical) encoded as base64 in submission.csv if the platform requires CSV outputs. Base64 is serialization, not a codec and not the source of novelty; account for its roughly 4/3 size overhead. Specify sample rate, channels, sample count and decoding limits. Do not add ungrounded confidence or event targets merely to expand the output schema.
Use speech_clean same-utterance headset audio as the recorded clean reference. Do NOT pair speech_noisy with a separately spoken clean sentence and call it aligned clean ground truth. Retain enough observed evidence: gaps with every source missing may be intrinsically unrecoverable. Evaluate nonidentifiability and cap/restrict such gaps transparently rather than rewarding hallucination.
All corruption is benchmark-generated and must be identified as such; original waveform/text targets remain real.

OFFICIAL SOURCES AND VERIFIED FACTS
Dataset: https://huggingface.co/datasets/Cnam-LMSSC/vibravox
Official file browser: https://huggingface.co/datasets/Cnam-LMSSC/vibravox/tree/main/speech_clean
License page: https://vibravox.cnam.fr/license/index.html
Paper: https://doi.org/10.1016/j.specom.2025.103238
Code / existing benchmarks: https://github.com/jhauret/vibravox
API: https://huggingface.co/api/datasets/Cnam-LMSSC/vibravox
Parent read the official API on 2026-09-14:
revision = cc59d58fa5859c5b8d82cf2f2d6bde0490550b8e
cardData.license = cc-by-4.0.
Official license page explicitly permits commercial sharing/adaptation with attribution in the prior successful read. A fresh web read timed out and local requests hit a certificate-chain error on that page; Hugging Face API worked with normal TLS. Preserve license text and attribution using accessible official sources. Do not disable TLS verification as a routine workaround.
Source has six simultaneous sensor channels, French transcripts and 188 retained participants in the paper; 200 were initially recruited. The current card and paper report differing utterance counts, so measure the pinned selected release instead of assuming either count.
Full card-reported download ~186.64 GB is NOT the proposed upload. Parent enumerated original speech_clean Parquet files, typically ~450-520 MB each. Examples:
speech_clean/train-00000-of-00201.parquet = 486680543 bytes
speech_clean/train-00001-of-00201.parquet = 486362627 bytes
speech_clean/test-00000-of-00030.parquet = 494810585 bytes.
These are acquisition examples, NOT a proven train/test selection. Speaker distribution within/among shards is unmeasured. Do not blindly take the first shards.

RAW DATA / URL IMPORT (IMPORTANT)
Use unchanged OFFICIAL Parquet shards as raw source. No new processed raw.zip. Prefer 4-5 or fewer immutable official file URLs, selected only after measuring speaker/utterance coverage.
Pinned URL form:
https://huggingface.co/datasets/Cnam-LMSSC/vibravox/resolve/cc59d58fa5859c5b8d82cf2f2d6bde0490550b8e/speech_clean/train-00000-of-00201.parquet?download=true
Verify each final URL, content length, file checksum and rebuild behavior. Import-from-URL should not require downloading the entire corpus onto this laptop. Small source metadata/range reads are appropriate; use bounded downloads only when necessary for pilot verification.
Resolve the user's repeated size limits as: prefer <1 GB if scientifically adequate; practical updated raw target <3 GB; never silently exceed 5 GB. Seek <=5 shards (~2.5 GB) if enough independent speakers remain. Do not sacrifice split validity simply to meet an arbitrary file count. If more than 5 raw URLs are necessary, an organizer ZIP may contain only byte-identical downloaded official files and required provenance/license material. No cropping, resampling, rewritten Parquet, preselected rows, normalization, split generation or augmentation in that raw ZIP. Copying whole official files into a ZIP is packaging, not permission to preprocess them.
All row selection, resampling, channel extraction, audio compression for prepared examples, dropout construction, pseudonymization, splits and further reduction must occur in deterministic prepare.py from the unchanged sources. Prepared target around 500 MB when feasible; measure decoded and serialized sizes. Never upload public/private prepared answers as raw source.
For local study, temporary decoded/cache data must remain clearly separate from upload sources and not be mistaken for the raw package.

REMAINING EVIDENCE BEFORE BUILD
- Inspect actual Parquet schema, audio encoding, transcript quality and simultaneous alignment; show representative native rows.
- Measure candidate shard combinations, usable utterance yield and distinct speakers, using metadata/range reads where possible. Preserve entire speakers and related utterances in one split. Do not treat speaker-count claims from the full release as coverage in a 2 GB subset. Use enough independent hidden speakers and quantify bootstrap/split variability.
- Compare against TAPS/Speaker-Calibrated Throat Speech Restoration already in our portfolio and VibraVox's original EBEN bandwidth-extension/speech-enhancement tasks. Language change or sensor count alone is not novelty. Write a reviewer premortem explaining the substantial learning difference.
- Run intended fine-tuning baseline with an appropriately licensed, available pretrained audio model and realistic compute. Include offline checkpoint handling and model license provenance.
- Measure best-single-sensor, fixed fusion, available-channel switching, simple DSP, reference EBEN where feasible, no-change/copy and transcript-only/ASR-then-TTS style shortcut baselines relevant to the contract. Show the contribution of complementary sources and robust recovery; do not assume fusion gains. Metrics must not reward nice-sounding but incorrect words or ignore utterance preservation.
- Do not claim GPU or CPU runtime has passed without executing a representative run on suitable hardware. If no GPU is available, complete what can be measured and explicitly report the remaining test, rather than fabricate a result.
- Direct leakage and split checks remain required. Public lookup is explicitly waived as noted above.
- If a gate is irreparable, document measured facts and a narrow feasible salvage attempt within this dataset. Do not invent new targets, quietly switch dataset, or finalize a rejected formulation to satisfy the request.

CONDITIONAL END-TO-END BUILD
Once evidence passes, update readiness and run the reusable validation, explicitly distinguishing the lookup waiver from a measured pass. Build under the exact final output path.
Create required prepare.py, grade.py, _analyze.py, licensed baseline/solution, tests, dataset/challenge form-fill files, sample submission, synchronized PASTE_THIS scripts, DATA_IMPORT.md, SOURCE_MANIFEST.json, attribution, audit reports and actual runtime results according to live templates.
Use fair metrics for reconstructed audio and transcript, with transparent weights and no arbitrary score powers to suppress strong baselines. Test oracle=1, valid nondegenerate sample, empty/missing/duplicate IDs, extra rows, malformed base64, invalid audio headers, NaNs/infinities, wrong sample rate/count, excessive payload/decoded sizes and decompression bombs. Grading should not execute uploaded code or unpickle objects. Enforce finite bounded scores and deterministic behavior.
No platform publication, dataset upload, purchase, external email or Run Agents without separate authorization. The request is to create the task and local challenge, not to submit it.

FINAL HANDOVER
Report actual status and outstanding evidence, exact folder and files, measured raw/prepared bytes, independent split counts, baseline metrics and runtime. Include a concise data procedure:
1. Preferred: paste the exact selected official URLs into Import from URL and rebuild.
2. Fallback: download and upload those SAME unchanged official files.
3. Only if >5 URLs: upload the verified clean-source ZIP and provide its manifest/checksums.
Explain which preprocessing prepare.py performs and how to verify the rebuilt file tree. Do not call the challenge ready unless it really is.

Use the reusable eris-challenge-factory skill. The user explicitly approved REASSEMBLE and requested a separate task to pursue it through challenge creation. Start with a bounded feasibility audit, then continue into the full build in this same task only when the measured readiness gates pass. This is NOT a build-ready handoff; access, independent scale, determinacy and baselines remain unmeasured. Be explicit about that status. Do not open further tasks.

EXACT TITLE: REASSEMBLE Contact-Event and Sensor Recovery
Category: From Scratch ONLY. Do not list Fine-Tuning as a second category.
Project root: C:\Users\vamsh\Downloads\create_challenge_synthetic
Final output folder: E:\create_challenge_synthetic_output_folder\sprint_5\REASSEMBLE Contact-Event and Sensor Recovery
Registry: C:\Users\vamsh\Downloads\create_challenge_synthetic\challenge_registry\reassemble-contact-event-and-sensor-recovery.json
Keep initial pilot evidence under challenge_registry\pilot_evidence\reassemble-contact-event-and-sensor-recovery; promote to full build only when feasible.
GPU preferred. CPU fallback only if appropriate; do not label CPU-only computation as GPU training. Model preference gpt-5.6-sol, xhigh reasoning.

CURRENT CONSTRAINTS
GPU preference overrides old CPU-only announcements. CV, object detection and structured sequence tasks are permitted. Do not make generic classification, tabular prediction or ordinary regression disguised with JSON or additional heads. Select the single category From Scratch throughout participant descriptions/forms. Novelty at least 6/10 with grounded comparison, not an invented guarantee. Plan for a 1.5-hour solve budget, verify currently applicable GPU/memory rules before final configuration, and record real runtime.
Public-source lookup is explicitly waived as a blocking criterion by this user. Document it as a waiver, never a passed attack. Direct answer leakage, narrator-spoken targets, train/test dependence, inadequate gold, licensing and unobservable outputs are NOT waived.

PROPOSED NARROW CONTRACT TO VALIDATE
Input: short real external-view video, available contact audio, robot kinematic context and partially masked force/torque traces, with explicit availability masks. Use intended-action text only if genuinely available independently of the answer; do not feed the annotated action sequence back as a prompt.
Output: recovered missing contact-audio segments and force/torque segments, plus the native ordered action intervals and per-segment success indicators where the measurements support these. Start with this scoped audio + numeric/structured output; do not attempt simultaneous novel-view video, audio, force and action generation by default.
Real operational purpose: reconstruct incomplete multimodal robot execution logs and identify the recorded action outcomes, not prescribe an invented counterfactual repair.
The proposed outputs are conditional on pilot evidence. Distinguish native action boundaries and recorded success from precise failure-onset/cause annotations that may not exist. Do not invent failure timestamps or causal labels from force thresholds, and do not call successful runs paired counterfactual repairs of failed runs.
All heads must be scientifically meaningful and mutually useful. Do not produce one action classifier plus decorative waveform regression. If waveform phase is not identifiable, test physically defensible spectral/envelope/timing evaluation. Evaluate only withheld signal regions; do not let copying intact inputs dominate. Avoid arbitrary hidden penalties or score powers.
Audio transport can be bounded base64 WAV or safe numeric arrays if the platform requires CSV; encoding is only transport, not novelty.

OFFICIAL SOURCE VERIFIED BY PARENT
TU Wien record: https://researchdata.tuwien.ac.at/records/0ewrv-8cb44
Official API: https://researchdata.tuwien.ac.at/api/records/0ewrv-8cb44
Version: 1.0.0.
Rights field explicitly returned cc-by-4.0, Creative Commons Attribution 4.0 International, with https://creativecommons.org/licenses/by/4.0/
Code: https://github.com/TUWIEN-ASL/REASSEMBLE
Project: https://tuwien-asl.github.io/REASSEMBLE_page/
Paper: https://arxiv.org/abs/2502.05086
Retain authors' citation, attribution, license and change notices. Check code/model licenses separately.
Official file metadata:
data.zip: 58,881,334,586 bytes (54.8 GiB), md5 812103a652ca9201e87a3bcecfee4ef3
https://researchdata.tuwien.ac.at/api/records/0ewrv-8cb44/files/data.zip/content
poses.zip: 89,431 bytes, md5 2f3f86b65dc6312b504072a2460314c2
https://researchdata.tuwien.ac.at/api/records/0ewrv-8cb44/files/poses.zip/content
README.txt: 8,138 bytes, md5 2e1394a2fa65e4ebb6c1fd64136cb0a0
https://researchdata.tuwien.ac.at/api/records/0ewrv-8cb44/files/README.txt/content
splits.zip: 1,094 bytes, md5 641882928ef3a8b2c3db41ac7c60b994
https://researchdata.tuwien.ac.at/api/records/0ewrv-8cb44/files/splits.zip/content
API exposes a container link for data.zip: https://researchdata.tuwien.ac.at/api/records/0ewrv-8cb44/files/data.zip/container . Its ability to list or serve compact individual members has NOT been verified; test safely with bounded responses. HTTP range/ZIP central-directory inspection may enable unchanged member retrieval but must be measured, not assumed.

Known official documentation: 4,551 demonstrations, 4,035 successful, four actions (pick, insert, remove, place), 17 objects, 781 minutes, collection dates Jan 9-14 2025. These are not verified counts of independent HDF5 recordings or independent scene families.
Sensors have separate timestamps and different rates; source does NOT promise already aligned array indices. HDF5 contains MP4/MP3 byte streams, force/torque and joint state arrays; segments_info supplies high/low-level start/end timestamps, success flags and text. Pose JSON matches recording filename. The source has a documented list of missing wrist-camera, invalid force/torque and missing pose cases. Filter these honestly before artificial masking.
Operator narrates actions during recording; descriptions are Whisper transcriptions corrected automatically/manually. Audio can therefore directly reveal event labels. Audit speech/narration as a first-class leakage source; compare transcript-only/audio-only baselines, restrict to defensible contact-only audio or document why no fair formulation survives. Do not treat a partly measured narrator transcript as independent contextual supervision.

SOURCE PACKAGING REQUIREMENTS
First resolve compact untouched source acquisition. Do not download the 58.9 GB archive wholesale to the laptop just to inspect it or supply it as compliant import.
Prefer <=4-5 validated official direct raw-file URLs. Landing pages are not raw imports. The listed giant data.zip URL is a real official file URL but is NOT size-compliant.
Raw package: aim under 1 GB; if robust independence requires more, target under 3 GB, with the user's 3-5 GB range as outer allowance, never unlimited. Prepared data ideally around/below 500 MB when sufficient. Include decoded/base64 overhead in budgets.
If >5 URLs are needed, create a single clean ZIP of unchanged complete official source files, preserving file contents and names, with provenance/hash manifest outside the clean raw payload. Selecting complete official files or extracting byte-identical archive members is allowed; processed mirrors (e.g. LeRobot conversions) are not substitutes for original untouched data without explicit authorization.
All transformations must be in prepare.py: video/audio decoding and resampling, crop/window selection, synchronization, corruption/masking, feature extraction, filtering, splits, anonymization and prepared target construction. Do not preprocess raw files and then label the result an official raw dataset.
Never perform source uploads, paid services, author contact, or final Shipd submission without separate user authorization.

PILOT GATES BEFORE FULL BUILD
1. Obtain a representative real synchronized record through a compliant bounded route; inspect native target fields and validity.
2. Measure post-filter yield and source bytes. Group by whole recording and correlated board layout/session/object families as appropriate. Hundreds of clips from the same few configurations are not independent. Include failed as well as successful actions; evaluate majority-success and action-template shortcuts.
3. Examine whether held-out action-object combinations have learnable training support; do not impose impossible combinations for difficulty. Test grouped validation stability rather than claiming a fixed arbitrary group threshold guarantees it.
4. Audit narration/metadata/kinematics leakage and modality necessity. Test intended-action-only, narrator-transcript-only, motion-only, majority outcome, interpolation, copied channel, spectral templates, independent heads and compact fused model.
5. Compare against source's existing temporal segmentation, anomaly detection and policy-learning tasks and local accepted examples. Adding heads or synthetic masks is not automatically novelty.
6. Establish safe metrics, natural headroom, valid oracle and sample, runtime within actual compute tier. Do not claim measured GPU runtime without running it.
7. Write source evidence card, reviewer premortem and readiness record with explicit lookup waiver. Try a bounded source-grounded salvage if a gate fails; if unsalvageable stop with measured reason rather than creating dummy grader/forms. Do not self-archive automatically.
8. Once measured readiness passes, continue the full build in this same task without asking for duplicate approval.

FULL BUILD CONTRACT
Read current living policies: .cursor\rules\challenge-creation.mdc; rules\LATEST.md; rules\checkpoints; rules\prev_reviews.txt; rules\challenge_template_file_creation.txt; relevant accepted examples and factory references. Resolve paths honestly.
Duplicate roots: project Shipd_Challenge_Archive_All, Shipd_Challenge_Archive_Novel, shipd_domain_challenge_docs, challenge_registry and E:\create_challenge_synthetic_output_folder\sprint_3, sprint_4 and sprint_5. Previous keyword scan had only generic word 'reassemble' matches, not evidence of a complete semantic audit. Do not edit the Google Sheet.
Create complete required package under exact final folder: prepare.py, grade.py, participant description and forms, sample submission, executable baseline, focused tests, matching PASTE_THIS files when required, license/attribution, official source manifest, source verification, readiness/novelty/split/baseline/runtime reports, and DATA_IMPORT_PROCEDURE.md. Validate byte-equivalence of direct-file and clean-zip input handling.
Strict grader: exact IDs/schema; bounded decoded payload bytes/shapes/dtypes; no unsafe pickle/NPZ object arrays; handle malformed JSON, NaN/Inf, unknown/missing/duplicate IDs; private labels separate from public inputs. Oracle 1.0 and valid weak sample. Never artificially depress scores.
At handover give absolute folder, actual size/split counts, baselines/tests and numbered acquisition steps: preferred exact official import URLs; fallback download/upload unchanged official files; if >5 URLs, exact clean source ZIP path/hash. Clearly state any unverified route. Do not publish or submit without separate user authorization.
Keep this task's registry status current and preserve unrelated work.

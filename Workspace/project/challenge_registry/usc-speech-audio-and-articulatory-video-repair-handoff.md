Use eris-challenge-factory. The user explicitly approves reusing the USC 75-Speaker Speech MRI dataset despite an existing archive challenge using it, waives public-source lookup, and asks for a dedicated task pursuing full creation. This task begins with bounded feasibility verification and proceeds to full build only upon measured readiness. Do not treat user approval as evidence the target is novel or feasible. Do not open a duplicate child task.

EXACT TITLE: USC Speech Audio and Articulatory Video Repair
Single category: Fine-Tuning. Do NOT also advertise From Scratch. Use a genuinely fine-tuned model with an appropriately licensed pretrained component; do not call scratch training Fine-Tuning. GPU preferred; CPU fallback if no viable GPU route, while preserving honest category/compute claims.
Requested model: gpt-5.6-sol, xhigh.
Project: C:\Users\vamsh\Downloads\create_challenge_synthetic
Final output: E:\create_challenge_synthetic_output_folder\sprint_5\USC Speech Audio and Articulatory Video Repair
Registry: C:\Users\vamsh\Downloads\create_challenge_synthetic\challenge_registry\usc-speech-audio-and-articulatory-video-repair.json
Pilot evidence location: challenge_registry\pilot_evidence\usc-speech-audio-and-articulatory-video-repair. Preserve unrelated files.

CURRENT RULES
GPU preferred, CPU allowed as fallback. CV, object detection and structured sequence tasks are currently allowed. No generic classification, tabular prediction or plain regression with a fancy wrapper. Novelty needs at least 6/10 with honest evaluation; never guarantee a platform score. Plan for 1.5 hours for full solver training/inference; read living rules for actual GPU tier/RAM before final configuration. Old CPU-only announcements do not override latest user preference.
Public-source lookup is waived as a gate. Dataset reuse is explicitly approved, but copying the existing task is NOT. Do not falsify duplicate audits, hide overlap, claim this is a fresh source, or manufacture new terminology to evade similarity detection. Direct answer leakage, split independence, label provenance and determinacy remain mandatory.

PROPOSED TASK
Joint Articulatory-Video and Speech Repair.
Input: real synchronized reconstructed midsagittal vocal-tract MRI video with explicitly masked intervals/regions, speech audio with different masked intervals, availability masks and a short permitted same-speaker calibration snippet if needed.
Output: restored speech waveform and completed MRI frames for the actual withheld original timestamps, with a defined source-validity convention. Evaluate missing portions rather than letting copied observed samples dominate.
Use complementary missing intervals initially; do not demand exact recovery of arbitrary long stretches absent in both modalities. Restrict scored imagery to real acquired/reconstructed reference timestamps; do not invent unmeasured intermediate-frame gold.
Plain meaning: repair incomplete recordings of speech and the articulator motion producing it, using surviving evidence across the two modalities.
This is not clinical diagnosis, a medical treatment, arbitrary text-to-video generation, speech recognition, or candidate matching. The reference is the released reconstructed MRI plus synchronized recorded/denoised audio, not anatomical ground truth or studio-clean speech. Do not call scanner/audio artifacts healthy-pathology evidence.
Avoid adding static anatomical scans as mandatory input merely to call the task multimodal: video+audio already qualify. Verify which subjects have a matching static scan and whether it adds necessary information before considering it.
Transport: video tensors/frames and base64 WAV or bounded numeric output may fit a CSV contract, but base64/NPZ is only a container. Bound payload sizes; never permit pickled object arrays. Preserve the user's audio-output goal.
Video of articulators does not uniquely determine voicing, pitch or acoustic phase. Use surviving audio context/calibration to support acoustic recovery and test suitable spectral/envelope/intelligibility measures rather than imposing arbitrary waveform exactness. Explain what remains intrinsically ambiguous. Do not use a learned cross-modal consistency metric trained on hidden test data or reward generic plausible speech.

OFFICIAL SOURCES VERIFIED
USC author page: https://sail.usc.edu/span/75speakers/
Official Figshare dataset version 1:
https://figshare.com/articles/dataset/A_multispeaker_dataset_of_raw_and_reconstructed_speech_production_real-time_MRI_video_and_3D_volumetric_images/13725546
Metadata API: https://api.figshare.com/v2/articles/13725546
Paper: https://www.nature.com/articles/s41597-021-00976-x
Official code: https://github.com/usc-mrel/usc_speech_mri
API explicitly returned license.name = CC BY 4.0, https://creativecommons.org/licenses/by/4.0/ . Preserve attribution, citation, license and change notices. Verify pretrained checkpoint and code licensing independently.
Authors document 75 subjects, RT-MRI video with synchronized speech audio, raw MRI and optional 3D/T2-weighted scans. Do not confuse the small CC0 metadata record 14892921 with the actual CC BY dataset.

PARENT-MEASURED OFFICIAL FILE METADATA
dataset_2drt_video_only.zip: 2,552,272,426 bytes
https://ndownloader.figshare.com/files/26416990
metafile_public_20210129.json: 543,035 bytes
https://ndownloader.figshare.com/files/26388150
Subjects.xlsx: 90,278 bytes
https://ndownloader.figshare.com/files/26388174
Stimuli.pptx: 955,087 bytes
https://ndownloader.figshare.com/files/26388151
Optional dataset_t2w_only.zip: 2,484,024,876 bytes
https://ndownloader.figshare.com/files/26416975
Do not fetch oversized dataset.zip (570,679,833,692 bytes), dataset_3d_only.zip (92,592,570,427 bytes), or example_for_sub001.zip (7,365,130,376 bytes).
The 2D ZIP plus JSON is 2,552,815,461 bytes and fits the user's under-3-GB target. The paired audio stream inside that ZIP still needs actual verification; filename 'video_only' alone proves neither audio presence nor absence. The source paper describes reconstructed videos with aligned audio. Check container streams/timestamps and use native metadata quality fields before treating it as a complete paired package.
Prefer omit demographics and stimuli from solver inputs unless necessary; they may expose participant identity, repeated prompts or protected personal details. Do not release extra personal metadata merely because it is public.
Adding all T2 data to the 2D archive would exceed 5 GB even before metadata; avoid this. Same-speaker visible context can be a lower-cost calibration option if measured useful.

KNOWN ARCHIVE OVERLAP
Existing title: Match Speech Audio to Synchronized Vocal-Tract MRI.
Local source: Shipd_Challenge_Archive_All\Non-CPU\Fine-Tuning.md
Archived URL: https://shipd.ai/quests/eris/challenges/jx7e0x3awpsnhat5tcntqt2q1x8e5b56
Its target is a probability grid over six candidate video snippets and nine timing offsets, using the same 75-speaker source. Do not reproduce candidate ranking, alignment-grid prediction or that grader.
User approves same-source reuse ONLY. Current task should output actual restored audio and image sequences, and must differ materially beyond changed formatting. Existing public acoustic-to-rtMRI and MRI-to-speech synthesis research is also close; research it before claiming novelty. Multi-head inpainting and synthetic gap placement alone may not meet the novelty threshold.
Previously measured archival counts refer to another prepared challenge, not this task's independent examples; do not borrow its readiness evidence.

RAW DATA / IMPORT REQUIREMENTS
User prefers raw source under 1 GB, but explicitly permits a practical target under 3 GB and outer range 3-5 GB. The verified 2D ZIP route fits that revised target without modifying source bytes.
Preferred: directly import <=4-5 official raw URLs. Use 2D ZIP + JSON initially if they prove sufficient. Actual response/archive contents/checksums still need testing; API-reported links are not proof a platform import succeeded.
Fallback: download and upload the exact same untouched official files.
If >5 URLs are genuinely necessary, make one clean ZIP of byte-identical complete official files with an external source manifest. No preprocessed raw archive, transcoded official ZIP, fabricated derivative mirror, or repackaged prepared train/test arrays.
ALL filtering, sample windows, decoding, resizing, temporal resampling, audio extraction, masking/corruption, normalization, anonymization, splitting and target creation must be inside prepare.py. An official upstream reconstructed-video archive is acceptable unchanged real source, even though authors reconstructed it. Selecting complete official files is permitted; rewriting contents before raw upload is not.
Prepared target preferably near/below 500 MB if compatible with scientifically adequate diversity. Budget source storage, decoded arrays and base64 submission expansion explicitly.
No huge downloads, paid services, author contact, platform uploads or submission without separate authorization. A bounded download of the size-compliant official archive for sample validation is allowed if no existing byte-verified local copy is available.

BOUNDED FEASIBILITY GATES
1. Inspect actual paired recordings: audio track, MRI frame times, synchronization, source validity/quality metadata. Verify representative utterance durations and post-filter paired yield.
2. Inventory speakers, prompt/script groups, sessions and utterances. Hold whole speakers out and group related repeated content appropriately. If using calibration for a held-out speaker, declare exactly what calibration data is permitted, separate it from query targets, and match training protocol. Do not create speaker overlap through patches.
3. Prove sufficient independent training/evaluation groups after quality filtering within raw/prepared budget. Grouped validation and per-speaker uncertainty matter more than arbitrary crop count.
4. Compare temporal interpolation, nearest visible frame, audio interpolation/silence, copied intact context, audio-only repair, video-only repair, independent-head methods and compact jointly conditioned fine-tuned model. Verify both modalities genuinely help and the task is not dominated by interpolation or memorized scripts.
5. Prove the proposed mask lengths remain identifiable and challenging. Test sustained vowels separately from transitions; exclude impossible targets honestly, not to cherry-pick a low score. No invented gold transcripts or expert labels.
6. Evaluate novelty vs the archive matching task and published MRI/audio reconstruction. Record source reuse permission, lookup waiver and the remaining scientific risks.
7. Measure runtime and metric sanity (oracle, weak sample, malformed input, copied-input). Write readiness card and reviewer premortem. If failure occurs, attempt bounded source-grounded salvage; if it cannot meet rules, stop with the precise evidence rather than dummy final artifacts.
8. Continue full build in this same task once gates pass, without re-requesting duplicate approval. Do not claim a full build was verified until actual checks finish.

FULL BUILD
Read living .cursor\rules\challenge-creation.mdc, rules\LATEST.md, rules\checkpoints, rules\prev_reviews.txt, rules\challenge_template_file_creation.txt and relevant accepted examples/factory references. Resolve missing paths honestly.
Audit current Shipd_Challenge_Archive_All, Shipd_Challenge_Archive_Novel, shipd_domain_challenge_docs, challenge_registry and E:\create_challenge_synthetic_output_folder\sprint_3, sprint_4 and sprint_5. Do not edit the user's Google Sheet.
Build complete mandatory artifacts under the exact requested folder: deterministic prepare.py, strict grade.py, synchronized PASTE_THIS copies when required, participant description/forms (Fine-Tuning only), weak sample submission, legitimate runnable baseline, focused tests, licenses/attribution, source manifest/checksums, measured readiness/novelty/split/runtime reports and DATA_IMPORT_PROCEDURE.md.
Grader must validate exact IDs/schema/shapes/ranges, finite values, decoded sizes and safe container parsing; use no pickle/object arrays. Keep private test targets out of public payloads. Oracle score 1.0; natural headroom, no arbitrary exponents or hidden hostile weights. Do not score unmasked easy content as the main objective.
Report all actual tests/results and limitations. Final handover must give: exact folder, chosen GPU tier/runtime, measured raw and prepared bytes, independent counts, preferred direct official import URLs, unchanged-download/upload fallback, and clean ZIP path/hash only if >5 URLs required. No Shipd publication/submission without separate authorization.
Keep registry state current and this task focused on the approved joint reconstruction problem.

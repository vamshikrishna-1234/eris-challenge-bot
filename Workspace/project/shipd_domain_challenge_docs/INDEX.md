# Shipd Eris Domain Challenge Examples

- Latest update timestamp: 2026-07-11T23:17:58+05:30
- Scrape timestamp: 2026-07-01T06:39:43+05:30
- Top profiles scanned: 50
- Unique challenge pages opened with displayed DOMAIN: 127
- Detail records including incomplete/failed attempts: 42

## Counts Per Target Domain

- [NLP](NLP.md): 27
- [Object Detection](Object-Detection.md): 4
- [Recommendation](Recommendation.md): 8
- [Sequence To Sequence](Sequence-To-Sequence.md): 33
- [Prompt Engineering](Prompt-Engineering.md): 3
- [RAG](RAG.md): 15
- [Fine-Tuning](Fine-Tuning.md): 38
- [From Scratch](From-Scratch.md): 15
- [LLM Evaluation](LLM-Evaluation.md): 4
- [Pre-Training](Pre-Training.md): 0
- [Other](Other.md): 2
- [Computer Vision](Computer-Vision.md): 8

## Output Files

- [NLP.md](NLP.md)
- [Object-Detection.md](Object-Detection.md)
- [Recommendation.md](Recommendation.md)
- [Sequence-To-Sequence.md](Sequence-To-Sequence.md)
- [Prompt-Engineering.md](Prompt-Engineering.md)
- [RAG.md](RAG.md)
- [Fine-Tuning.md](Fine-Tuning.md)
- [From-Scratch.md](From-Scratch.md)
- [LLM-Evaluation.md](LLM-Evaluation.md)
- [Pre-Training.md](Pre-Training.md)
- [Other.md](Other.md)
- [Computer-Vision.md](Computer-Vision.md)

## Method And Limitations

- Used the authenticated in-app Shipd Eris browser session and read-only navigation only.
- Scanned the top 50 leaderboard profiles and captured the visible challenge-history rows for each profile.
- Challenge classification uses the challenge page displayed `DOMAIN` field only; titles were used only to choose which candidate links to open.
- Most profiles still showed a `Load more` button after the first 50 visible rows; the scan stayed bounded at the visible rows for ranks 2-50, with earlier deeper clicks only on the first profile from the checkpoint.
- Some candidate profile-history anchors had visible hrefs but did not navigate when clicked; those pages were skipped rather than guessed.
- Incomplete/blank detail attempts: 2 (`jx78t84fbns1qqenz1k2czqzv98262yr`, `jx714m5y0z0ynht5k3d6g0ehxx825m56`).
- Direct unauthenticated page fetches showed the Shipd join/sign-in surface, and Chrome was not authenticated; the authenticated in-app browser was the source of truth.
- No challenge forms were submitted and no create/edit/destructive actions were used.

## Home Page Addendum (2026-07-01T07:16:12+05:30)

- Rechecked the Shipd Eris home page feed and opened additional target-domain challenge cards from there.
- Added 8 verified home-page challenges with longer detail-page descriptions: NLP +2, Fine-Tuning +4, Sequence To Sequence +2.
- One neighboring Object Detection card was accidentally opened during retry and ignored; no non-target entries were added to the domain files.

## Non-Target Domains Opened

- Classification: 2
- Computer Vision: 4
- LLM Evaluation: 1
- Regression: 1
- Tabular: 1

## Google Drive Folder Addendum (2026-07-01T08:30:33+05:30)
<!-- GOOGLE_DRIVE_APPEND_2026_07_01 -->

- Appended 31 challenge specs from the two shared Google Drive folders.
- Source folders: https://drive.google.com/drive/folders/1cryF6d4--Zxw0eOycMNfzbvlmKov5AzE and https://drive.google.com/drive/folders/1DGpCR98lsmh3hcPKym3t5sUdMqUCFIdP
- Added per domain: NLP +9, Fine-Tuning +4, RAG +8, Sequence To Sequence +4, From Scratch +6, Pre-Training +0.
- Duplicates were intentionally allowed for this Drive append per user request.
- Challenge descriptions were captured from `CHALLENGE_FORM_FILL.md`, `CHALLENGE_DESCRIPTION.md`, `challenge_description.txt`, `challenge_desc.txt`, or `cd.txt` where available; earlier prepare/reply fallbacks were replaced before appending.
- Drive folders generally did not expose the Shipd challenge page `DOMAIN` field, so Drive entries were assigned from domain folder names where present or inferred from folder/spec content when not present.

## Description Repair Addendum (2026-07-01T09:13:24+05:30)
<!-- SHIPD_DESCRIPTION_REPAIR_2026_07_01 -->

- Reopened 19 Shipd challenge pages in the authenticated in-app browser and replaced earlier placeholder `Description` sections with the full visible problem descriptions from the challenge detail pages.
- Affected domains: NLP +2, Fine-Tuning +2, RAG +5, Sequence To Sequence +7, From Scratch +3.
- Counts did not change; only the description bodies were corrected.

## Single Challenge Addendum (2026-07-02T14:12:11+05:30)
<!-- SINGLE_CHALLENGE_APPEND_JX798EJ_2026_07_02 -->

- Added `Molecular Signatures Of Bioactivity Reproducibility` to [Fine-Tuning.md](Fine-Tuning.md) from the user-opened Shipd challenge page and pasted challenge text.
- Displayed page metadata captured: DOMAIN `Fine-Tuning`, status `Accepted`, difficulty `Medium`, GPU `A10G`, scoring `? Higher is better`.

## Single Challenge Addendum (2026-07-02T14:14:43+05:30)
<!-- SINGLE_CHALLENGE_APPEND_JX735T_2026_07_02 -->

- Added `MS/MS Stability Review Brief Generation` to [Fine-Tuning.md](Fine-Tuning.md) from the user-provided Shipd challenge URL.
- Displayed page metadata captured: DOMAIN `Fine-Tuning`, status `Accepted`, difficulty `Medium`, GPU `A10G`, scoring `↓ Lower is better`.

## Batch Challenge Addendum (2026-07-02T14:18:59+05:30)
<!-- BATCH_CHALLENGE_APPEND_2026_07_02_NINE_URLS -->

- Added 9 challenge pages from the user-provided Shipd URL batch.
- Added per displayed domain: Fine-Tuning +4, From Scratch +2, LLM Evaluation +1, NLP +1, Sequence To Sequence +1.
- Each entry was placed using the challenge page's displayed `DOMAIN` field and includes the full visible problem description.

## Batch Challenge Addendum (2026-07-02T22:08:42+05:30)
<!-- BATCH_CHALLENGE_APPEND_2026_07_02_EIGHT_URLS -->

- Added 8 challenge pages from the user-provided Shipd URL batch.
- Added per displayed domain: From Scratch +1, NLP +2, Prompt Engineering +2, Sequence To Sequence +3.
- Created active-domain docs where missing, including Object Detection, Recommendation, and Prompt Engineering.
- Each entry was placed using the challenge page's displayed `DOMAIN` field and includes the full visible problem description.

## Single Challenge Addendum (2026-07-02T22:11:23+05:30)
<!-- SINGLE_CHALLENGE_APPEND_JX72YAQ_2026_07_02 -->

- Added `Thermal Reaction-Channel Repertoires From Molecular Structure` to [Fine-Tuning.md](Fine-Tuning.md) from the user-provided Shipd challenge URL.
- Displayed page metadata captured: DOMAIN `Fine-Tuning`, status `Accepted`, difficulty `Medium`, GPU `A10G`, scoring `↑ Higher is better`.

## Batch Challenge Addendum (2026-07-03T11:08:47+05:30)
<!-- BATCH_CHALLENGE_APPEND_2026_07_03_THREE_URLS -->

- Added 3 challenge pages from the user-provided Shipd URL batch.
- Added per displayed domain: NLP +1, Sequence To Sequence +2.
- Each entry was placed using the challenge page's displayed `DOMAIN` field and includes the full visible problem description.

## Batch Challenge Addendum (2026-07-03T11:22:26+05:30)
<!-- BATCH_CHALLENGE_APPEND_2026_07_03_FOUR_URLS -->

- Added 4 challenge pages from the user-provided Shipd URL batch.
- Added per displayed domain: NLP +1, Object Detection +1, Sequence To Sequence +1, Fine-Tuning +1.
- Each entry was placed using the challenge page's displayed `DOMAIN` field and includes the full visible problem description.

## Batch Challenge Addendum (2026-07-04T03:52:23+05:30)
<!-- BATCH_CHALLENGE_APPEND_2026_07_04_FOURTEEN_URLS -->

- Added 14 challenge pages from the user-provided Shipd URL batch.
- Added per displayed domain: NLP +3, Recommendation +1, Sequence To Sequence +2, Fine-Tuning +6, LLM Evaluation +1, Other +1.
- The pasted concatenated URL line was split into `jx78q34baphf74b7xwqh4sqae989jh2f` and `jx7bhfw5350gcnr1bw8r4a8zk589rp4g` before scraping.
- Each entry was placed using the challenge page's displayed `DOMAIN` field and includes the full visible problem description.

## Batch Challenge Addendum (2026-07-04T13:29:46+05:30)
<!-- BATCH_CHALLENGE_APPEND_2026_07_04_FIVE_URLS -->

- Added 5 challenge pages from the user-provided Shipd URL batch.
- Added per displayed domain: NLP +1, Recommendation +1, Sequence To Sequence +2, Fine-Tuning +1.
- Each entry was placed using the challenge page's displayed `DOMAIN` field and includes the full visible problem description.

## Pending Retry Batch Addendum (2026-07-06T04:59:21+05:30)

<!-- PENDING_RETRY_APPEND_2026_07_06_ALL -->

- Retried 37 saved pending Shipd challenge URLs in the authenticated in-app browser.
- Added 37 new challenge pages; skipped 0 already-present or invalid entries.
- Added per displayed domain: Fine-Tuning +10, From Scratch +3, LLM Evaluation +2, NLP +5, Object Detection +1, Other +1, Prompt Engineering +1, RAG +1, Recommendation +6, Sequence To Sequence +7.
- Each entry was placed using the displayed `DOMAIN` field and includes the full visible problem description captured from the challenge detail page.
- Retry failures after reconnect: 0.

## Single URL Addendum (2026-07-08T13:23:29+05:30)

<!-- SINGLE_URL_APPEND_jx70p79jax7k88df1wt8vzvmd18a111c -->

- Added `Tax Form Field Localization` from the user-provided Shipd challenge URL.
- Displayed page metadata captured: DOMAIN `Object Detection`, status `Accepted`, difficulty `Medium`, GPU `A10G`, scoring `↓ Lower is better`.
- Full visible challenge description was appended to [Object-Detection.md](Object-Detection.md).

## Single URL Addendum (2026-07-08T13:27:17+05:30)

<!-- SINGLE_URL_APPEND_jx79c1y5vqpe5hjpmxbcpbddkd8a0erp -->

- Added `Aerial Tree Canopy State Segmentation` from the user-provided Shipd challenge URL.
- Displayed page metadata captured: DOMAIN `Computer Vision`, status `Accepted`, difficulty `Medium`, GPU `A10G`, scoring `↑ Higher is better`.
- Full visible challenge description was appended to [Computer-Vision.md](Computer-Vision.md).

## Single URL Addendum (2026-07-08T13:29:44+05:30)

<!-- SINGLE_URL_APPEND_jx70987ba6d2bq7hj6cy8bgjys8a11d2 -->

- Added `Cataract Surgery Tool Recognition & Anticipation` from the user-provided Shipd challenge URL.
- Displayed page metadata captured: DOMAIN `Computer Vision`, status `Accepted`, difficulty `Medium`, GPU `A10G`, scoring `↑ Higher is better`.
- Full visible challenge description was appended to [Computer-Vision.md](Computer-Vision.md).

## Single URL Batch Addendum (2026-07-08T14:16:57+05:30)

<!-- SINGLE_URL_BATCH_APPEND_20260708_132 -->

- Added 2 challenge pages from the user-provided Shipd URL batch: `Nucleus Boundary Grid Recovery`, `Tracing the Coastline Across Unseen Survey Flights`.
- Added per displayed domain: Computer Vision +2.
- Each entry was placed using the displayed `DOMAIN` field and includes the full visible challenge description from the detail page.

## Single URL Addendum (2026-07-08T14:19:35+05:30)

<!-- SINGLE_URL_APPEND_jx785jk5t50qcdmgqrtevdqcbh89zc5a -->

- Added `Occlusion-Aware Cattle Detection in Aerial Drone Imagery` from the user-provided Shipd challenge URL.
- Displayed page metadata captured: DOMAIN `Object Detection`, status `Accepted`, difficulty `Medium`, GPU `A10G`, scoring `↑ Higher is better`.
- Full visible challenge description was appended to [Object-Detection.md](Object-Detection.md).

## Single URL Addendum (2026-07-08T14:22:15+05:30)

<!-- SINGLE_URL_APPEND_jx71vbsndfm7b070e9fhf52gtn89v74c -->

- Added `User Emotion Shift And Escalation Prediction From Paired Speech Clips` from the user-provided Shipd challenge URL.
- Displayed page metadata captured: DOMAIN `Fine-Tuning`, status `Accepted`, difficulty `Medium`, GPU `A10G`, scoring `↑ Higher is better`.
- Full visible challenge description was appended to [Fine-Tuning.md](Fine-Tuning.md).

## Single URL Addendum (2026-07-08T14:26:25+05:30)

<!-- SINGLE_URL_APPEND_jx72tjs317h2sk1fv35c7a9v5x895v2b -->

- Added `Killer Whale Conservation Bioacoustic Profiling From Hydrophone Audio` from the user-provided Shipd challenge URL.
- Displayed page metadata captured: DOMAIN `Fine-Tuning`, status `Accepted`, difficulty `Medium`, GPU `A10G`, scoring `↑ Higher is better`.
- Full visible challenge description was appended to [Fine-Tuning.md](Fine-Tuning.md).

## Single URL Addendum (2026-07-08T14:29:24+05:30)

<!-- SINGLE_URL_APPEND_jx73c4vfj2rz1wm4j668bw0nzd8a5p0g -->

- Added `Neuron 3D Branching-Topology Prediction from 2D Projection Images` from the user-provided Shipd challenge URL.
- Displayed page metadata captured: DOMAIN `Computer Vision`, status `Accepted`, difficulty `Hard`, GPU `A10G`, scoring `↑ Higher is better`.
- Full visible challenge description was appended to [Computer-Vision.md](Computer-Vision.md).

## Single URL Addendum (2026-07-08T14:42:55+05:30)

<!-- SINGLE_URL_APPEND_jx732pfbje94na65bkeaqeqna18a22bm -->

- Added `RGB-D Object Projection Trace Recovery` from the user-provided Shipd challenge URL.
- Displayed page metadata captured: DOMAIN `Computer Vision`, status `Accepted`, difficulty `Medium`, GPU `A10G`, scoring `↑ Higher is better`.
- Full visible challenge description was appended to [Computer-Vision.md](Computer-Vision.md).

## Single URL Addendum (2026-07-08T14:45:38+05:30)

<!-- SINGLE_URL_APPEND_jx78amrc9zr7spwc722tm3qyw18a2bsg -->

- Added `Capsule Mucosa Visibility` from the user-provided Shipd challenge URL.
- Displayed page metadata captured: DOMAIN `Computer Vision`, status `Accepted`, difficulty `Medium`, GPU `A10G`, scoring `↑ Higher is better`.
- Full visible challenge description was appended to [Computer-Vision.md](Computer-Vision.md).

## Single URL Addendum (2026-07-08T14:48:34+05:30)

<!-- SINGLE_URL_APPEND_jx74ep23hjzb3psh8yzd0fzkqd8a105p -->

- Added `Leaf Symptom Evidence Ledger` from the user-provided Shipd challenge URL.
- Displayed page metadata captured: DOMAIN `Sequence To Sequence`, status `Accepted`, difficulty `Medium`, GPU `A10G`, scoring `↑ Higher is better`.
- Full visible challenge description was appended to [Sequence-To-Sequence.md](Sequence-To-Sequence.md).

## Single URL Addendum (2026-07-11T23:17:58+05:30)

<!-- SINGLE_URL_APPEND_jx70wnk1p7139nvg52sj0ght6188w7c0 -->

- Added `Shadow-Based GPS and Time Prediction` from the user-provided Shipd challenge URL.
- Displayed page metadata captured: DOMAIN `Computer Vision`, status `Accepted`, difficulty `Hard`, GPU `A10G`, scoring `↑ Higher is better`.
- Full visible challenge description and user-provided Discord discussion were appended to [Computer-Vision.md](Computer-Vision.md).

## CPU-Only Challenge Collection

- [CPU-only challenge docs](CPU/INDEX.md)

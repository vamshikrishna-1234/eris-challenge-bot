# Status & Fix admission evidence

Requested challenge: `Bimanual Contact-Change Field From RGB Motion Pairs`

Requested URL: `https://shipd.ai/quests/eris/challenges/jx75vwgzj8gj7whcfckzxy5d8588zb2e`

Requested ID: `jx75vwgzj8gj7whcfckzxy5d8588zb2e`

Observed at: 2026-09-13 05:06 IST.

## Outcome

The workflow stopped at the submission admission gate. No website write, challenge-package edit, registry claim, batch mutation, or shared previous-review append was performed.

## Live inspection evidence

- A fresh authenticated read of the exact challenge URL shows its real title is `Stir Schedule Retrodiction From Dye Mixing Pattern`, not the supplied Bimanual title.
- Its visible state is `Revision Requested`.
- The latest visible review is by `aikyatan`, dated 2026-07-02. It requests an `n == 0` guard in `_schedule_score`, a safe `FALLBACK` when the non-rare count series is empty, and a substantive response to the earlier tightly clustered agent scores.
- The challenge is explicitly linked to `Synthetic Stirred Vessel Dye Mixing Patterns With Control Labels`, dataset `jd7crb484r7897dczf8xf4cp2188y6yx`, which is displayed as Ready and contains 721 raw files.
- The user-opened dataset `jd7812d2p1yakfh0ckkgwc0t6d8e8j9g` is a separate blank Draft with title `fill it hereeee`, only the default description placeholder, zero source files, no selected license, and no source URL.

## Local binding evidence

The configured project root, configured D: output root, and legacy E: output root contain no canonical package or registry match for the requested challenge ID, its actual Stir title, its linked dataset ID, or the blank dataset ID opened by the user.

One local folder has a form title matching the supplied title:

`D:\create_challenge_synthetic_output_folder\sprint_3\codex_output_folders_sprint_3\Egocentric RGB To Tactile Pressure Grid Prediction`

It is not safe to bind to the requested challenge. Its own revision evidence identifies a different problem/challenge ID, `jx7emzz0f2qsyqf7576hvzfra98dsfpk`, and dataset ID, `jd71rkm6bn43n5gnk0p8z5pmqd8dszwk`. The authenticated page also proves that the requested challenge ID is a Stir challenge rather than this Bimanual task. No matching challenge-registry JSON exists for either platform pair or for the opened blank dataset.

Canonical candidate hashes at inspection time:

- `prepare.py`: `0d733e3e7d2284c65956f523985dac53ae4fb30720900c1427237c8c4186ee88`
- `grade.py`: `a21cb259b4b42be66848bd3a901a7f68fbd00f3d038a28628d0fa0ff8dd12aae`
- `CHALLENGE_FORM_FILL.md`: `9f163f06c057371cf29ddc7e2e816f5b286739236600c2b91c59e12c0b76ed2b`
- `DATASET_FORM_FILL.md`: `c4535803ee5e03e53bcb159dd61c97c22e17ae54db3f9661d28dba8a5ca83015`

## Preliminary candidate-only risk facts

These facts are not attributed to the requested `jx75...` challenge; they describe only the conflicting `jx7em...` folder:

- 942 prepared train rows and 907 test rows are windows from only ten source recordings: five train and five test.
- The ten recordings share one calibration user (`rohit`) and one calibration timestamp (`2026-03-13T17:19:36`), so the local package does not establish independent subject diversity.
- Each test task-family worst group is one recording, with 150 to 220 highly overlapping temporal pairs.
- The sample submission scores `0.4574949051321606`; perfect scores exactly `1.0`.
- The existing previous-review entry is the 2026-09-09 answer-schema correction by `yenwee0804`. It must not be reused as the current revision feedback without a fresh platform read.

## Required recovery

Resume only after an authenticated read of the exact requested page yields the current revision details and linked dataset, and after those IDs uniquely match a local package plus a Proceed registry record owned by this task/machine. If the live page belongs to the old local package, record the platform mapping explicitly before editing. If it is a distinct clone/version, recover its own canonical package rather than substituting the title match.

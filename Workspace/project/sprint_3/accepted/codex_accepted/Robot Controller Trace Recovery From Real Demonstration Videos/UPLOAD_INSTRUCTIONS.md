# Upload Instructions

Preferred dataset import:

```text
https://zenodo.org/records/6337847/files/PandaHandover_Real_Val.zip?download=1
```

Use the official Zenodo URL import if the platform supports direct URL ingestion. The direct file is an unmodified official source archive under 1 GB.

Manual fallback:

1. Download `PandaHandover_Real_Val.zip` from the official Zenodo record.
2. Verify size `296205835` bytes and MD5 `c3af4d02e686084c28d6dd7bc12cb059`.
3. Upload that unmodified ZIP as the dataset source file.
4. If the platform requires one wrapper archive rather than a raw ZIP source file, run `python zip_raw_for_upload.py --raw-dir <folder-with-official-zip> --output official_raw_upload.zip`. The wrapper archive contains only `PandaHandover_Real_Val.zip`; it does not contain prepared train/test files or derived labels.

Challenge scripts:

* Paste `PASTE_THIS_PREPARE.txt` into the platform prepare script field.
* Paste `PASTE_THIS_GRADE.txt` into the platform grading script field.
* The platform-visible problem description is section `## 3) Problem Description` in `CHALLENGE_FORM_FILL.md`.
* The dataset form should use `DATASET_FORM_FILL.md`.
* If prepare fails after a URL import, re-paste the current `PASTE_THIS_PREPARE.txt` first. The updated prepare script accepts retained ZIPs, extracted folders, nested wrapper folders, and ZIP files without a `.zip` extension. If URL import itself is unreliable, manually upload only the unmodified official `PandaHandover_Real_Val.zip`.

Blank prepare-failure diagnosis:

* The default prepare is full mode. Do not set any environment variable for normal submission.
* If the platform still shows only `Prepare script failed:` with no traceback, use the optional `PREPARE_STAGE` environment variable to binary-search the failure if the platform exposes environment variables:
  * `PREPARE_STAGE=1`: prove invocation and tiny output writes.
  * `PREPARE_STAGE=2`: index the raw archive and write a tiny summary.
  * `PREPARE_STAGE=3`: parse trajectories and write CSV/private files without encoding videos.
  * unset `PREPARE_STAGE` or set `PREPARE_STAGE=4`: full prepare with video encoding.
* If stage 3 passes but stage 4 fails, the platform is likely killing video encoding or prepared-output size. Reduce `MAX_SAMPLES` further and re-paste `PASTE_THIS_PREPARE.txt`.

Reviewer source-lookup audit after a local full prepare:

```powershell
python _source_lookup_probe.py --raw <official-zip-or-extracted-raw> --public <prepared-public> --private <prepared-private>
```

If the probe exceeds the configured rank-1 or rank-5 thresholds, do not submit without further label-preserving video hardening or a target redesign.

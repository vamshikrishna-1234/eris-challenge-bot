# Dataset creation form - fill-in

## Dataset name

```
Permissive Python Repository Commit Diffs
```

## Overview

This corpus contains compact real commit diffs sampled from permissively licensed Python repositories. Each row describes either a target commit-diff event or a support calibration event from the same repository. The raw data includes anonymized repository profile text, compact unified-diff text, changed-file lists, and source attribution metadata; private house-code labels are not stored in the raw upload.

## File structure

```
generate.py                    bounded real-diff corpus builder
raw_upload/                    extracted raw corpus directory
raw_upload/records.csv         target and support commit-diff rows
raw_upload/attributions.csv    source repository/license metadata
raw_upload/manifest.json       corpus metadata
raw_upload/LICENSE.txt         dataset and upstream license notices
```

* `generate.py` clones a bounded shallow/no-checkout snapshot of listed permissively licensed repositories and extracts compact commit patches.
* `raw_upload/records.csv` contains the generated target/support event rows, text fields, and raw metadata.
* `raw_upload/attributions.csv` lists each sampled upstream repository, SPDX license, source URL, and sampled commit count.
* `raw_upload/manifest.json` records corpus size, source metadata, and label provenance notes.
* `raw_upload/LICENSE.txt` states the dataset compilation label/profile license and includes upstream license notices.

## records.csv columns

Each row of `records.csv` describes one real anonymized commit-diff event.

* `event_key` (string): Stable synthetic identifier for the sampled event.
* `repo_key` (string): Stable anonymized identifier for the source repository.
* `repo_split` (string): Internal partition marker with value `train` or `test`.
* `row_role` (string): Raw role marker with value `target` or `support`.
* `repo_domain` (string): Coarse domain value for the sampled corpus.
* `repo_profile` (string): Anonymized repository process profile shown to downstream users.
* `event_index` (int): Event number within the anonymized repository and role.
* `target_summary` (string): Anonymized compact summary derived from the real edit archetype.
* `target_diff` (JSON string): Object containing `summary`, `files`, and compact unified-diff text.

## attributions.csv columns

* `repo_slug` (string): Upstream GitHub `owner/repository` identifier.
* `license` (string): Upstream SPDX license identifier.
* `source_url` (string): Upstream repository URL.
* `sampled_commits` (int): Number of support plus target commits sampled from that source.

## License

The dataset compilation metadata and anonymized profiles are CC0 1.0. Original code diffs remain under their upstream permissive licenses: MIT, BSD-3-Clause, and Apache-2.0, as listed in `raw_upload/attributions.csv` and included in `raw_upload/LICENSE.txt`.

## Source

Real public GitHub repositories with permissive SPDX licenses, sampled through bounded shallow Git history extraction by `generate.py`. Repository names and source URLs are retained only in raw attribution metadata, while downstream public rows are anonymized.

## Notes

* Default settings produce a compact CPU-friendly text corpus from seven permissively licensed Python repositories.
* The code-change text is real upstream commit-diff material; house-code and release-policy labels are derived later by the private preparation script.
* The raw archive is flat internally and contains `records.csv`, `attributions.csv`, `manifest.json`, and `LICENSE.txt`.
* Public prepared files strip source repository names, commit SHAs, raw ids, private family labels, split markers, original paths, and original commit subject lines.

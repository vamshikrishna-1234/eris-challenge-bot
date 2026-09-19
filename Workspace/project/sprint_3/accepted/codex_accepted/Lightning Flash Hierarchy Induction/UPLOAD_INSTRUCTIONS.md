# Dataset import and upload procedure

## Preferred: direct official URL import

1. Create a dataset in the platform dataset form.
2. Select URL import.
3. Add all five URLs from `URL_IMPORT_LIST.txt`, one URL per source item. Do not rename the imported objects.
4. Confirm the platform reports five `.nc` objects totaling 2,901,827 bytes.
5. Paste `PASTE_THIS_PREPARE.txt` as the prepare script and run preparation.
6. Confirm preparation reports 210 train and 140 test cases.

`prepare.py` accepts either a flat URL-import directory or platform-created nested directories. It locates the five basenames recursively, then rejects a missing, duplicate, wrong-size, or wrong-hash object.

## Fallback: upload untouched files

Use this only if platform URL import fails.

```powershell
$urls = Get-Content -LiteralPath '.\URL_IMPORT_LIST.txt'
New-Item -ItemType Directory -Path '.\glm_official_raw' -Force | Out-Null
foreach ($url in $urls) {
  $name = [System.IO.Path]::GetFileName($url)
  Invoke-WebRequest -Uri $url -OutFile (Join-Path '.\glm_official_raw' $name)
}
```

Verify every byte length and SHA-256 against `SOURCE_VERIFICATION.md`. Upload the five untouched `.nc` files directly. Do not preprocess, rename, subset, convert, recompress, or add derived tables.

If you want a direct upload archive instead of URL import, use `glm_official_raw_untouched_with_attribution_20260716_210000.zip` in this challenge folder. It was freshly downloaded from the five official NOAA URLs and contains exactly the five untouched `.nc` files plus `NOAA_ATTRIBUTION.txt`, flat at the ZIP root. The ZIP is 1,107,424 bytes with SHA-256 `02b4127d0c2c0d62326923e5b5c9acb3c86b6d1610b21f0f0073fdd0eeb9ca0b`; the uncompressed raw `.nc` files total 2,901,827 bytes. Do not include `public/`, `private/`, `prepare.py`, cached Python files, or any preprocessed dataset in any replacement ZIP.

## Dependencies

Preparation requires Python, NumPy, pandas, and either netCDF4 or h5py to read the official NetCDF4/HDF5 files. The grading script requires only NumPy and pandas. The optional analysis script additionally uses scikit-learn and psutil.

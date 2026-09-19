from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageOps


ID_SALT = "ninfea-cycle-ledger-v1"
SPLIT_SALT = "ninfea-record-group-split-v1"
TEST_PER_1000 = 300
MIN_GROUP_TEST = 8

SEGMENT_SEC = 6.0
STRIDE_SEC = 4.5
MAX_SEGMENTS_PER_RECORD = 8
TARGET_W = 512
TARGET_H = 192
PUBLIC_SIGNAL_CHANNELS = 10
PUBLIC_SIGNAL_SAMPLES = 1536
ENVELOPE_POINTS = 64
PUBLIC_SIGNAL_FS = 256
PROMPT = (
    "Plain language objective: align the Doppler strip image with the "
    "multichannel ECG and maternal respiration snippet, then return a compact "
    "cardiac-cycle evidence ledger. For each fetal cycle, report the beat time "
    "and cycle start/end within the row-local segment; also provide a Doppler "
    "envelope array, cycle quality flags, and calibrated confidence. This is a "
    "CPU-only structured multimodal task, not a plain heart-rate regression."
)


def _root(raw: Path) -> Path:
    raw = Path(raw)
    for candidate in [
        raw,
        raw / "raw_upload",
        raw / "ninfea",
        raw / "ninfea-1.0.0",
        raw / "files" / "ninfea" / "1.0.0",
    ]:
        if (candidate / "pwd_images").is_dir() and (candidate / "wfdb_format_ecg_and_respiration").is_dir():
            return candidate
    for candidate in sorted(p for p in raw.iterdir() if p.is_dir()):
        if (candidate / "pwd_images").is_dir() and (candidate / "wfdb_format_ecg_and_respiration").is_dir():
            return candidate
    zips = []
    for p in sorted(raw.iterdir()):
        if not p.is_file():
            continue
        is_zip = p.suffix.lower() == ".zip"
        if not is_zip:
            try:
                with p.open("rb") as fh:
                    is_zip = fh.read(4) == b"PK\x03\x04"
            except OSError:
                is_zip = False
        if is_zip:
            zips.append(p)
    for zp in zips:
        with zipfile.ZipFile(zp, "r") as zf:
            names = zf.namelist()
            if any(n.endswith("pwd_images/1.bmp") for n in names) or any(n == "pwd_images/1.bmp" for n in names):
                zf.extractall(raw / "_extracted_official")
                return _root(raw / "_extracted_official")
    raise FileNotFoundError(
        "Could not find official NInFEA layout with pwd_images/ and "
        "wfdb_format_ecg_and_respiration/ under raw input. If URL import "
        "created only a small downloaded-file, it likely imported the HTML "
        "directory index; use https://physionet.org/content/ninfea/get-zip/1.0.0/ "
        "or upload the unchanged official PhysioNet file tree."
    )


def _record_names(root: Path) -> list[str]:
    records = root / "RECORDS"
    if records.exists():
        out = []
        for line in records.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            out.append(Path(line).name)
        return out
    names = sorted(p.stem for p in (root / "wfdb_format_ecg_and_respiration").glob("*.hea"))
    return names


def _parse_gain_baseline(token: str) -> tuple[float, float]:
    # WFDB token example: 1119216.6963(598581736)/uV
    left = token.split("/")[0]
    if "(" in left and ")" in left:
        gain_s = left.split("(")[0]
        base_s = left.split("(")[1].split(")")[0]
    else:
        gain_s, base_s = left, "0"
    gain = float(gain_s) if gain_s not in {"", "0"} else 1.0
    baseline = float(base_s)
    return gain, baseline


def _read_header(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    first = lines[0].split()
    record = first[0]
    n_sig = int(first[1])
    fs = float(first[2])
    n_samples = int(first[3])
    channels = []
    for line in lines[1:]:
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 9:
            continue
        gain, baseline = _parse_gain_baseline(parts[2])
        channels.append({
            "dat": parts[0],
            "fmt": parts[1],
            "gain": gain,
            "baseline": baseline,
            "name": parts[8],
        })
    if len(channels) != n_sig:
        raise ValueError(f"Header {path} channel count mismatch")
    return {"record": record, "n_sig": n_sig, "fs": fs, "n_samples": n_samples, "channels": channels}


def _read_wfdb_segment(root: Path, rec: str, start_s: float, dur_s: float) -> tuple[np.ndarray, dict]:
    wfdb_dir = root / "wfdb_format_ecg_and_respiration"
    header = _read_header(wfdb_dir / f"{rec}.hea")
    dat_name = Path(header["channels"][0]["dat"]).name
    dat_path = wfdb_dir / dat_name
    n_sig = int(header["n_sig"])
    fs = float(header["fs"])
    start = max(0, int(round(start_s * fs)))
    n = min(int(round(dur_s * fs)), int(header["n_samples"]) - start)
    if n <= 0:
        raise ValueError(f"Empty signal segment for record {rec}")
    offset = start * n_sig * 4
    raw = np.memmap(dat_path, dtype="<i4", mode="r", offset=offset, shape=(n, n_sig))
    names = [c["name"] for c in header["channels"]]
    expected_names = ["uni_abd1", "uni_abd4", "uni_abd8", "uni_abd12", "uni_abd16", "uni_abd20", "bi_tho1", "bi_tho2", "bi_tho3", "matrsp"]
    missing = [name for name in expected_names if name not in names]
    if missing:
        raise ValueError(f"Record {rec} is missing expected channels: {missing}")
    wanted = [names.index(name) for name in expected_names]
    vals = []
    for idx in wanted:
        ch = header["channels"][idx]
        vals.append((raw[:, idx].astype(np.float32) - float(ch["baseline"])) / float(ch["gain"]))
    arr = np.vstack(vals)
    # Downsample to a public CPU-friendly signal tensor.
    step = max(1, int(round(fs / PUBLIC_SIGNAL_FS)))
    arr = arr[:, ::step]
    if arr.shape[1] < PUBLIC_SIGNAL_SAMPLES:
        raise ValueError(f"Record {rec} segment is too short after downsampling")
    arr = arr[:, :PUBLIC_SIGNAL_SAMPLES]
    arr = arr - np.median(arr, axis=1, keepdims=True)
    scale = np.percentile(np.abs(arr), 95, axis=1, keepdims=True)
    scale[scale < 1e-6] = 1.0
    arr = np.clip(arr / scale, -6, 6).astype(np.float32)
    meta = {"fs": fs / step, "channel_names": [names[i] for i in wanted]}
    return np.asarray(arr), meta


def _rng_for(key: str, tag: str) -> np.random.Generator:
    digest = hashlib.sha256(f"{ID_SALT}:{tag}:{key}".encode("utf-8")).digest()
    return np.random.default_rng(np.random.SeedSequence(int.from_bytes(digest, "big")))


def _public_strip_transform(crop: Image.Image, scene_hash: str) -> Image.Image:
    rng = _rng_for(scene_hash, "strip-public-view")
    arr = np.asarray(crop, dtype=np.float32) / 255.0
    gamma = float(rng.uniform(0.88, 1.12))
    contrast = float(rng.uniform(0.88, 1.10))
    bias = float(rng.uniform(-0.035, 0.035))
    arr = np.clip(((arr ** gamma) - 0.5) * contrast + 0.5 + bias, 0, 1)
    row_gain = rng.normal(1.0, 0.018, size=(arr.shape[0], 1)).astype(np.float32)
    col_gain = rng.normal(1.0, 0.012, size=(1, arr.shape[1])).astype(np.float32)
    arr = np.clip(arr * row_gain * col_gain, 0, 1)
    noise = rng.normal(0.0, 0.018, size=arr.shape).astype(np.float32)
    arr = np.clip(arr + noise, 0, 1)
    return Image.fromarray(np.round(arr * 255).astype(np.uint8), mode="L")


def _public_signal_transform(signal_arr: np.ndarray, scene_hash: str) -> np.ndarray:
    rng = _rng_for(scene_hash, "signal-public-view")
    arr = np.asarray(signal_arr, dtype=np.float32).copy()
    if arr.shape != (PUBLIC_SIGNAL_CHANNELS, PUBLIC_SIGNAL_SAMPLES):
        raise ValueError(f"Unexpected public signal shape {arr.shape}")
    gains = rng.uniform(0.88, 1.12, size=(arr.shape[0], 1)).astype(np.float32)
    arr = arr * gains
    mix = rng.normal(0.0, 0.018, size=(arr.shape[0], arr.shape[0])).astype(np.float32)
    mix += np.eye(arr.shape[0], dtype=np.float32)
    arr = mix @ arr
    drift = rng.normal(0.0, 0.015, size=(arr.shape[0], 1)).astype(np.float32)
    ramp = np.linspace(-1.0, 1.0, arr.shape[1], dtype=np.float32)[None, :]
    arr = arr + drift * ramp
    arr = arr + rng.normal(0.0, 0.015, size=arr.shape).astype(np.float32)
    return np.clip(arr, -6.0, 6.0).astype(np.float32)


def _load_strip(path: Path) -> Image.Image:
    img = Image.open(path).convert("L")
    # Remove UI darkness and normalize contrast in the public crop.
    return ImageOps.autocontrast(img, cutoff=1)


def _crop_strip(img: Image.Image, start_s: float, dur_s: float, record_duration: float) -> Image.Image:
    w, h = img.size
    x0 = int(round(start_s / record_duration * w))
    x1 = int(round((start_s + dur_s) / record_duration * w))
    x0 = max(0, min(w - 2, x0))
    x1 = max(x0 + 2, min(w, x1))
    crop = img.crop((x0, 0, x1, h))
    crop = crop.resize((TARGET_W, TARGET_H), resample=Image.BILINEAR)
    return ImageOps.autocontrast(crop, cutoff=2)


def _smooth(x: np.ndarray, width: int) -> np.ndarray:
    width = max(3, int(width) | 1)
    ker = np.ones(width, dtype=float) / width
    return np.convolve(x, ker, mode="same")


def _find_peaks_1d(score: np.ndarray, min_sep: int, threshold: float) -> list[int]:
    peaks: list[int] = []
    for i in range(2, len(score) - 2):
        if score[i] < threshold:
            continue
        if score[i] >= score[i - 1] and score[i] >= score[i + 1]:
            if peaks and i - peaks[-1] < min_sep:
                if score[i] > score[peaks[-1]]:
                    peaks[-1] = i
            else:
                peaks.append(i)
    return peaks


def _signal_event_times(signal_arr: np.ndarray, fs: float, duration: float) -> list[tuple[float, float]]:
    if signal_arr.size == 0 or fs <= 0:
        return []
    n_use = min(6, signal_arr.shape[0])
    sig = signal_arr[:n_use].astype(float)
    diff_energy = np.mean(np.abs(np.diff(sig, axis=1, prepend=sig[:, :1])), axis=0)
    amp_energy = np.mean(np.abs(sig), axis=0)
    score = _smooth(0.65 * diff_energy + 0.35 * amp_energy, max(5, int(round(0.045 * fs))))
    base = np.percentile(score, 35)
    top = np.percentile(score, 98)
    if top <= base + 1e-9:
        return []
    score = np.clip((score - base) / (top - base), 0, 1)
    min_sep = max(8, int(round(0.28 * fs)))
    peaks = _find_peaks_1d(score, min_sep, 0.36)
    out = []
    n = score.size
    for p in peaks:
        t = min(duration, max(0.0, p / fs))
        out.append((t, float(score[p])))
    return out


def _derive_envelope_and_events(crop: Image.Image, duration: float, signal_arr: np.ndarray, signal_fs: float) -> tuple[list, list, list]:
    arr = np.asarray(crop, dtype=np.float32) / 255.0
    # Favor bright Doppler trace pixels over dark UI/grid background.
    col_med = np.median(arr, axis=0, keepdims=True)
    resid = np.clip(arr - col_med, 0, 1)
    thresh = np.percentile(resid, 83)
    mask = resid > max(0.08, thresh)
    lo_hi = []
    energy = []
    for x in range(arr.shape[1]):
        ys = np.flatnonzero(mask[:, x])
        if ys.size < 2:
            lo, hi = 0.42, 0.58
            e = 0.0
        else:
            lo = float(np.percentile(ys, 8) / (arr.shape[0] - 1))
            hi = float(np.percentile(ys, 92) / (arr.shape[0] - 1))
            e = float(np.mean(resid[ys, x]))
        lo_hi.append((lo, hi))
        energy.append(e)
    energy = _smooth(np.asarray(energy, dtype=float), max(7, arr.shape[1] // 90))
    if float(np.max(energy)) > 1e-9:
        energy = energy / float(np.max(energy))
    min_sep = max(12, int(arr.shape[1] * 0.30 / duration))
    image_peaks = _find_peaks_1d(energy, min_sep, 0.26)
    image_events = [(p * duration / arr.shape[1], float(energy[p]), int(p)) for p in image_peaks]
    signal_events = _signal_event_times(signal_arr, signal_fs, duration)

    used_signal: set[int] = set()
    combined = []
    for t_img, e_img, p_img in image_events:
        best = None
        for j, (t_sig, e_sig) in enumerate(signal_events):
            if j in used_signal:
                continue
            gap = abs(t_img - t_sig)
            if gap <= 0.18 and (best is None or gap < best[0]):
                best = (gap, j, t_sig, e_sig)
        if best is None:
            combined.append({"t": t_img, "img_x": p_img, "score": e_img, "support": "doppler_only"})
        else:
            _, j, t_sig, e_sig = best
            used_signal.add(j)
            wt_img = max(0.05, e_img)
            wt_sig = max(0.05, e_sig)
            t = (t_img * wt_img + t_sig * wt_sig) / (wt_img + wt_sig)
            combined.append({"t": t, "img_x": p_img, "score": 0.5 * (e_img + e_sig), "support": "matched"})
    for j, (t_sig, e_sig) in enumerate(signal_events):
        if j not in used_signal and e_sig >= 0.62:
            p_img = int(round(t_sig / duration * (arr.shape[1] - 1)))
            p_img = max(0, min(arr.shape[1] - 1, p_img))
            combined.append({"t": t_sig, "img_x": p_img, "score": e_sig, "support": "signal_only"})
    combined.sort(key=lambda r: r["t"])
    dedup = []
    for row in combined:
        if dedup and row["t"] - dedup[-1]["t"] < 0.20:
            if row["score"] > dedup[-1]["score"]:
                dedup[-1] = row
        else:
            dedup.append(row)
    combined = dedup

    peaks = [int(r["img_x"]) for r in combined]
    if len(combined) > 1:
        intervals = np.diff([r["t"] for r in combined])
        med = float(np.median(intervals))
    else:
        med = 0.42
    ledger = []
    qualities = []
    for k, item in enumerate(combined):
        p = int(item["img_x"])
        t = float(item["t"])
        if k == 0:
            start = max(0.0, t - med / 2)
        else:
            start = 0.5 * (combined[k - 1]["t"] + t)
        if k == len(combined) - 1:
            end = min(duration, t + med / 2)
        else:
            end = 0.5 * (t + combined[k + 1]["t"])
        local_e = float(item["score"])
        if item["support"] == "matched" and local_e >= 0.42 and (end - start) >= 0.25:
            quality = "usable"
        elif item["support"] == "signal_only":
            quality = "artifact"
        else:
            quality = "uncertain"
        ledger.append({"t": round(t, 4), "start": round(start, 4), "end": round(end, 4)})
        qualities.append(quality)
    idxs = np.linspace(0, arr.shape[1] - 1, ENVELOPE_POINTS).round().astype(int)
    env = []
    for x in idxs:
        lo, hi = lo_hi[int(x)]
        env.append([round(float(x / (arr.shape[1] - 1)), 4), round(lo, 4), round(hi, 4)])
    return ledger, env, qualities


def _split_record(rec: str) -> str:
    h = hashlib.sha256(f"{SPLIT_SALT}:{rec}".encode("utf-8")).hexdigest()
    return "test" if (int(h[:8], 16) % 1000) < TEST_PER_1000 else "train"


def _hashed_id_map(scene_hashes: list[str]) -> dict[str, int]:
    hashed = [(hashlib.sha256(f"{ID_SALT}:{h}".encode("utf-8")).hexdigest(), h) for h in scene_hashes]
    assert len({d for d, _ in hashed}) == len(hashed)
    return {h: i for i, (_, h) in enumerate(sorted(hashed))}


def _segment_rows(root: Path) -> pd.DataFrame:
    rows = []
    for rec in _record_names(root):
        hea = root / "wfdb_format_ecg_and_respiration" / f"{rec}.hea"
        bmp = root / "pwd_images" / f"{rec}.bmp"
        if not hea.exists() or not bmp.exists():
            continue
        header = _read_header(hea)
        duration = float(header["n_samples"]) / float(header["fs"])
        if duration < SEGMENT_SEC + 0.25:
            continue
        starts = list(np.arange(0.0, max(0.1, duration - SEGMENT_SEC), STRIDE_SEC))
        starts = starts[:MAX_SEGMENTS_PER_RECORD]
        for idx, start in enumerate(starts):
            scene_hash = hashlib.sha256(f"{ID_SALT}:{rec}:{idx}:{start:.3f}".encode("utf-8")).hexdigest()
            rows.append({
                "scene_hash": scene_hash,
                "record_group": str(rec),
                "segment_index": int(idx),
                "start_sec_private": float(start),
                "segment_duration_sec": float(SEGMENT_SEC),
                "record_duration_sec": duration,
                "split": _split_record(str(rec)),
            })
    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("No usable NInFEA records found")
    assert df["scene_hash"].is_unique
    if df[["scene_hash", "record_group", "split"]].isna().any().any():
        raise RuntimeError("Raw manifest contains NaN values")
    if df[["scene_hash", "record_group", "split"]].astype(str).eq("").any().any():
        raise RuntimeError("Raw manifest contains blank values")
    return df


def _private_groups(row, n_events: int, env: list, signal_arr: np.ndarray) -> dict:
    resp = signal_arr[-1] if signal_arr.shape[0] else np.zeros(1)
    resp_motion = float(np.std(np.diff(resp))) if resp.size > 2 else 0.0
    width = np.mean([hi - lo for _, lo, hi in env]) if env else 0.0
    if n_events <= 8:
        rate_bucket = "few_cycles"
    elif n_events <= 13:
        rate_bucket = "mid_cycles"
    else:
        rate_bucket = "many_cycles"
    return {
        "split_group": rate_bucket,
        "ood_axis": "resp_high" if resp_motion > 0.025 else "resp_low",
        "render_style": "wide_envelope" if width > 0.25 else "narrow_envelope",
    }


def _merge_sparse(groups: pd.Series, prefix: str) -> pd.Series:
    counts = groups.value_counts()
    rare = set(counts[counts < MIN_GROUP_TEST].index)
    if not rare:
        return groups
    out = groups.map(lambda x: f"other_{prefix}" if x in rare else x)
    value_counts = out.value_counts()
    if value_counts.get(f"other_{prefix}", 0) < MIN_GROUP_TEST:
        majority = value_counts.sort_values(ascending=False).index[0]
        out = out.map(lambda x: majority if x == f"other_{prefix}" else x)
    return out


def prepare(raw: Path, public: Path, private: Path) -> None:
    raw = Path(raw)
    public = Path(public)
    private = Path(private)
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    root = _root(raw)
    rows = _segment_rows(root)
    all_hashes = rows["scene_hash"].tolist()
    id_map = _hashed_id_map(all_hashes)

    for sub in ["train/strips", "test/strips", "train/signals", "test/signals"]:
        (public / sub).mkdir(parents=True, exist_ok=True)

    train_rows = []
    test_rows = []
    answer_rows = []
    pending_sample_rows = []
    strip_cache: dict[str, Image.Image] = {}

    for _, row in rows.sort_values(["record_group", "segment_index"]).iterrows():
        rid = int(id_map[row["scene_hash"]])
        split = str(row["split"])
        rec = str(row["record_group"])
        bmp_name = Path(f"{rec}.bmp").name
        if rec not in strip_cache:
            strip_cache[rec] = _load_strip(root / "pwd_images" / bmp_name)
        crop = _crop_strip(strip_cache[rec], float(row["start_sec_private"]), float(row["segment_duration_sec"]), float(row["record_duration_sec"]))
        signal_arr, signal_meta = _read_wfdb_segment(root, rec, float(row["start_sec_private"]), float(row["segment_duration_sec"]))
        crop = _public_strip_transform(crop, str(row["scene_hash"]))
        signal_arr = _public_signal_transform(signal_arr, str(row["scene_hash"]))
        ledger, envelope, qualities = _derive_envelope_and_events(crop, float(row["segment_duration_sec"]), signal_arr, float(signal_meta["fs"]))
        groups = _private_groups(row, len(ledger), envelope, signal_arr)

        strip_name = f"{rid:06d}.bmp"
        sig_name = f"{rid:06d}.npy"
        split_dir = "train" if split == "train" else "test"
        crop.save(public / split_dir / "strips" / strip_name, format="BMP")
        np.save(public / split_dir / "signals" / sig_name, signal_arr.astype(np.float32))
        public_row = {
            "id": rid,
            "image": f"{split_dir}/strips/{strip_name}",
            "signal_npy": f"{split_dir}/signals/{sig_name}",
            "segment_duration_sec": round(float(row["segment_duration_sec"]), 4),
            "n_signal_channels": int(signal_arr.shape[0]),
            "signal_fs_hz": round(float(signal_meta["fs"]), 3),
            "prompt": PROMPT,
        }
        label_bits = {
            "ledger_json": json.dumps(ledger, separators=(",", ":")),
            "envelope_json": json.dumps(envelope, separators=(",", ":")),
            "quality_json": json.dumps(qualities, separators=(",", ":")),
        }
        if split == "train":
            train_rows.append({**public_row, **label_bits})
        else:
            test_rows.append(public_row)
            pending_sample_rows.append({"id": rid, "duration": float(row["segment_duration_sec"])})
            answer_rows.append({**{"id": rid, "segment_duration_sec": public_row["segment_duration_sec"]}, **label_bits, **groups})

    train = pd.DataFrame(train_rows)
    test = pd.DataFrame(test_rows)
    answers = pd.DataFrame(answer_rows)
    if train.empty or test.empty:
        raise RuntimeError("Grouped split produced an empty train or test split")
    for axis in ["split_group", "ood_axis", "render_style"]:
        answers[axis] = _merge_sparse(answers[axis].astype(str), axis)
        vc = answers[axis].value_counts()
        if (vc < MIN_GROUP_TEST).any():
            raise RuntimeError(f"MIN_GROUP_TEST failed for {axis}: {vc.to_dict()}")

    train_cols = ["id", "image", "signal_npy", "segment_duration_sec", "n_signal_channels", "signal_fs_hz", "prompt", "ledger_json", "envelope_json", "quality_json"]
    test_cols = ["id", "image", "signal_npy", "segment_duration_sec", "n_signal_channels", "signal_fs_hz", "prompt"]
    sample_cols = ["id", "ledger_json", "envelope_json", "quality_json", "confidence"]
    ans_cols = ["id", "ledger_json", "envelope_json", "quality_json", "segment_duration_sec", "split_group", "ood_axis", "render_style"]
    train_counts = []
    for cell in train["ledger_json"].astype(str):
        try:
            train_counts.append(len(json.loads(cell)))
        except Exception:
            pass
    median_count = int(round(float(np.median(train_counts))) if train_counts else 9)
    prior_count = int(np.clip(median_count - 3, 3, 12))
    weak_env = [[round(i / 63, 4), 0.42, 0.58] for i in range(64)]
    sample_rows = []
    for row in pending_sample_rows:
        duration = float(row["duration"])
        step = duration / (prior_count + 1)
        weak_led = [
            {
                "t": round((i + 1) * step, 4),
                "start": round(max(0.0, (i + 0.55) * step), 4),
                "end": round(min(duration, (i + 1.45) * step), 4),
            }
            for i in range(prior_count)
        ]
        sample_rows.append({
            "id": int(row["id"]),
            "ledger_json": json.dumps(weak_led, separators=(",", ":")),
            "envelope_json": json.dumps(weak_env, separators=(",", ":")),
            "quality_json": json.dumps(["uncertain"] * prior_count, separators=(",", ":")),
            "confidence": 0.18,
        })
    sample = pd.DataFrame(sample_rows)
    train[train_cols].sort_values("id").to_csv(public / "train.csv", index=False)
    test[test_cols].sort_values("id").to_csv(public / "test.csv", index=False)
    sample[sample_cols].sort_values("id").to_csv(public / "sample_submission.csv", index=False)
    answers[ans_cols].sort_values("id").to_csv(private / "answers.csv", index=False)
    print(f"[done] {len(train)} train segments, {len(test)} test segments from {rows['record_group'].nunique()} records")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("raw", type=Path)
    parser.add_argument("public", type=Path)
    parser.add_argument("private", type=Path)
    args = parser.parse_args()
    prepare(args.raw, args.public, args.private)


if __name__ == "__main__":
    main()

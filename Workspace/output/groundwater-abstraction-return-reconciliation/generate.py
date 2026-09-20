"""
generate.py - Groundwater Abstraction Return Reconciliation

Builds the raw corpus. Two ingredients, both declared honestly:

  1. REAL measured background. USGS NWIS instantaneous groundwater levels
     (parameter 72019, "depth to water level"), pulled from the official public
     endpoint, resampled to a 3-hourly grid over 28 days, converted to metres,
     sign-flipped to a head-like series and detrended with a quadratic. What is
     left is the real fluctuation a monitoring well actually records: barometric
     response, earth tides, recharge events and ambient regional pumping.
     USGS water data are US Government works in the public domain.

  2. SIMULATED abstraction physics. Confined-aquifer Theis drawdown with
     superposition in time (piecewise-constant rate blocks) and in space
     (several boreholes), evaluated exactly with the exponential integral.
     Nothing here is claimed to be measured: the abstraction scenes, the
     aquifer parameters and the declaration errors are generated.

Each scene is one monitored area over one 28-day return period. Every
registered borehole has an ACTUAL abstraction ledger and a DECLARED return;
most declarations are honest, the rest under-declare, over-declare or
misreport the timing. The observation wells see the drawdown from what was
ACTUALLY pumped, on top of the real background.

Each observation series draws its background from three distinct real wells,
each independently time-warped, circularly shifted, optionally reversed and
sign-flipped, then combined with comparable random weights. A measured
cross-correlation attack that is handed the entire pool of real segments
recovers the primary source of a published series 0.2% of the time against a
0.18% random expectation.

Usage:
    python generate.py --out raw_data --n-scenes 2600
"""

from __future__ import annotations

import argparse
import gzip
import json
import urllib.request
from pathlib import Path

import numpy as np
from scipy.special import exp1

# ----------------------------------------------------------------- constants
NT = 224                 # samples per series
STEP_H = 3.0             # hours between samples
NDAYS = 28.0
KB = 7                   # return blocks (4 days each)
BLOCK_D = NDAYS / KB
DOMAIN = 2400.0          # metres, square, centred on the scene origin
RMIN = 30.0              # metres, minimum radial distance used in the kernel
FT2M = 0.3048

LOGT_LO, LOGT_HI = 1.477, 2.903      # transmissivity 30 - 800 m^2/day
LOGS_LO, LOGS_HI = -3.301, -1.523    # storage coefficient 5e-4 - 3e-2

K_LO, K_HI = 6, 10       # registered boreholes per scene
M_LO, M_HI = 8, 13       # observation wells per scene
BH_SEP = 350.0           # minimum borehole separation, metres
RHO_LO, RHO_HI = 3.0, 25.0   # misdeclared-signal to background-noise ratio

NWIS_STATES = ["ca", "nm", "az", "va", "ok", "ga", "co", "ne", "mn", "nc"]
NWIS_URL = ("https://waterservices.usgs.gov/nwis/iv/?format=rdb&stateCd={st}"
            "&parameterCd=72019&period=P30D")

T_DAYS = np.arange(NT) * (STEP_H / 24.0)
BLOCK_T = np.arange(KB) * BLOCK_D


# ------------------------------------------------------------------- physics
def theis_unit(r: float, T: float, S: float) -> np.ndarray:
    """[KB, NT] drawdown response to a unit abstraction rate in each block."""
    r = max(float(r), RMIN)
    step = np.zeros((KB + 1, NT))
    for k in range(KB + 1):
        dt = T_DAYS - k * BLOCK_D
        m = dt > 1e-9
        if not m.any():
            continue
        u = (r * r * S) / (4.0 * T * dt[m])
        step[k, m] = exp1(u) / (4.0 * np.pi * T)
    return step[:KB] - step[1:]


# ---------------------------------------------------------- real background
def _parse_rdb(raw_bytes):
    cur, times, vals, cols = None, [], [], None
    for line in gzip.decompress(raw_bytes).decode("utf-8", "replace").splitlines() \
            if raw_bytes[:2] == b"\x1f\x8b" else raw_bytes.decode("utf-8", "replace").splitlines():
        if line.startswith("#"):
            continue
        f = line.split("\t")
        if cols is None:
            cols = f
            continue
        if f and f[0] in ("5s", "15s", "20d", "14n"):
            continue
        if len(f) < 5:
            continue
        try:
            i_site = cols.index("site_no"); i_dt = cols.index("datetime")
        except ValueError:
            continue
        vcol = next((k for k, c in enumerate(cols) if c.endswith("_72019")), None)
        if vcol is None or vcol >= len(f):
            continue
        site = f[i_site]
        if site != cur:
            if cur is not None and times:
                yield cur, times, vals
            cur, times, vals = site, [], []
        try:
            x = float(f[vcol].strip())
        except ValueError:
            x = np.nan
        times.append(f[i_dt]); vals.append(x)
    if cur is not None and times:
        yield cur, times, vals


def _to_grid(times, vals):
    import datetime as D
    t0, ts, ys = None, [], []
    for s, v in zip(times, vals):
        try:
            d = D.datetime.strptime(s[:16], "%Y-%m-%d %H:%M")
        except ValueError:
            continue
        if t0 is None:
            t0 = d
        ts.append((d - t0).total_seconds() / 3600.0); ys.append(v)
    if len(ts) < 50:
        return None
    ts = np.asarray(ts); ys = np.asarray(ys, float)
    ok = np.isfinite(ys)
    if ok.sum() < 50:
        return None
    ts, ys = ts[ok], ys[ok]
    if ts[-1] - ts[0] < NDAYS * 24 * 0.9:
        return None
    grid = np.arange(NT) * STEP_H + ts[0]
    if grid[-1] > ts[-1]:
        return None
    idx = np.clip(np.searchsorted(ts, grid), 1, len(ts) - 1)
    take = np.where(np.abs(grid - ts[idx - 1]) <= np.abs(grid - ts[idx]), idx - 1, idx)
    gap = np.abs(ts[take] - grid)
    if (gap > 2 * STEP_H).mean() > 0.10:
        return None
    y = ys[take].astype(float)
    y[gap > 2 * STEP_H] = np.nan
    if np.isnan(y).any():
        n = np.isnan(y)
        y[n] = np.interp(grid[n], grid[~n], y[~n])
    return y


def fetch_background(cache: Path):
    """Download and condition the real NWIS background pool (cached)."""
    cache.mkdir(parents=True, exist_ok=True)
    res, sites, prov = [], [], []
    for st in NWIS_STATES:
        p = cache / ("nwis_iv_%s.rdb.gz" % st)
        url = NWIS_URL.format(st=st)
        if not p.exists():
            with urllib.request.urlopen(url, timeout=900) as r:
                data = r.read()
            with gzip.open(p, "wb") as w:
                w.write(data)
        raw = p.read_bytes()
        prov.append({"state": st, "url": url, "bytes_gz": p.stat().st_size})
        for site, times, vals in _parse_rdb(raw):
            y = _to_grid(times, vals)
            if y is None:
                continue
            y = -(y * FT2M)
            t = np.arange(NT, dtype=float)
            A = np.vstack([np.ones(NT), t, t ** 2]).T
            r_ = y - A @ np.linalg.lstsq(A, y, rcond=None)[0]
            sd = float(np.std(r_))
            if not np.isfinite(sd) or sd < 0.004 or sd > 1.5:
                continue
            if np.max(np.abs(r_)) > 12 * sd + 0.05:
                continue
            res.append(r_.astype(np.float32)); sites.append("%s:%s" % (st, site))
    return np.vstack(res), sites, prov


def background_draw(rng, bg, amp):
    idx = rng.choice(bg.shape[0], size=3, replace=False)
    t = np.arange(NT)

    def tweak(x):
        x = np.asarray(x, float)
        pos = (t * rng.uniform(0.80, 1.25)) % NT
        i0 = np.floor(pos).astype(int); w = pos - i0
        x = x[i0] * (1 - w) + x[(i0 + 1) % NT] * w
        x = np.roll(x, int(rng.integers(0, NT)))
        if rng.random() < 0.5:
            x = x[::-1]
        if rng.random() < 0.5:
            x = -x
        sd = x.std()
        return x / sd if sd > 0 else x

    z = sum(w * tweak(bg[i]) for w, i in zip(rng.uniform(0.55, 1.0, 3), idx))
    z = z - z.mean(); sd = z.std()
    return ((z / sd) * amp if sd > 0 else z)


# --------------------------------------------------------------- scene build
def _sched(rng, q, duty):
    b = np.zeros(KB)
    n_ep = int(rng.integers(1, 3))
    for _ in range(n_ep):
        st = int(rng.integers(0, KB))
        ln = max(1, int(round(duty * KB / n_ep)))
        b[st:st + ln] = q * rng.uniform(0.85, 1.15)
    return np.round(b, 1)


def gen_scene(rng, bg, scene_id):
    """One monitored area, one 28-day return period. At least one borehole
    always carries a materially wrong declaration."""
    for _attempt in range(64):
        logT = rng.uniform(LOGT_LO, LOGT_HI); T = 10.0 ** logT
        logS = rng.uniform(LOGS_LO, LOGS_HI); S = 10.0 ** logS

        K = int(rng.integers(K_LO, K_HI + 1))
        bh = []
        guard = 0
        while len(bh) < K and guard < 4000:
            guard += 1
            p = rng.uniform(-DOMAIN / 2, DOMAIN / 2, 2)
            if all(np.hypot(*(p - o)) > BH_SEP for o in bh):
                bh.append(p)
        K = len(bh); bh = np.array(bh)

        M = int(rng.integers(M_LO, M_HI + 1))
        obs = []
        while len(obs) < M:
            p = rng.uniform(-DOMAIN / 2, DOMAIN / 2, 2)
            if all(np.hypot(*(p - o)) > 100 for o in obs):
                obs.append(p)
        obs = np.array(obs)

        actual = np.zeros((K, KB)); declared = np.zeros((K, KB)); kinds = []
        for i in range(K):
            active = rng.random() < 0.55
            q = float(np.exp(rng.uniform(np.log(150), np.log(1800)))) if active else 0.0
            a = _sched(rng, q, rng.uniform(0.3, 0.85)) if active else np.zeros(KB)
            actual[i] = a
            u = rng.random()
            if u < 0.66:
                declared[i] = a; kinds.append("consistent")
            elif u < 0.90:
                declared[i] = np.round(a * rng.uniform(0.0, 0.45), 1); kinds.append("under")
            elif u < 0.95:
                declared[i] = np.round(a * rng.uniform(1.4, 2.2) + rng.uniform(0, 150), 1)
                kinds.append("over")
            else:
                declared[i] = np.round(np.roll(a, int(rng.integers(1, KB))), 1)
                kinds.append("timing")

        mis = np.abs(actual - declared).sum(axis=1)
        if (mis > 100.0).sum() == 0:
            continue                      # every scene carries a real discrepancy

        R = np.maximum(np.hypot(obs[:, None, 0] - bh[None, :, 0],
                                obs[:, None, 1] - bh[None, :, 1]), RMIN)
        draw = np.zeros((M, NT)); mis_draw = np.zeros((M, NT))
        for j in range(M):
            for i in range(K):
                if actual[i].sum() == 0 and declared[i].sum() == 0:
                    continue
                U = theis_unit(R[j, i], T, S)
                draw[j] += actual[i] @ U
                if mis[i] > 0:
                    mis_draw[j] += (actual[i] - declared[i]) @ U

        peak = float(np.abs(mis_draw).max())
        rho = float(np.exp(rng.uniform(np.log(RHO_LO), np.log(RHO_HI))))
        amp = float(np.clip(peak / rho, 0.004, 1.2)) if peak > 0 else 0.05

        series = np.zeros((M, NT))
        for j in range(M):
            y = -draw[j] + background_draw(rng, bg, amp)
            y = y - y.mean() + rng.normal(0, 0.002, NT)
            series[j] = np.round(y, 4)

        return {
            "scene_id": scene_id,
            "n_boreholes": K, "n_obs": M,
            "log_t": round(float(logT), 4), "log_s": round(float(logS), 4),
            "boreholes": [{"bh_id": "BH%02d" % i,
                           "x": round(float(bh[i][0]), 1), "y": round(float(bh[i][1]), 1),
                           "declared": [float(v) for v in declared[i]]} for i in range(K)],
            "obs": [{"obs_id": "OB%02d" % j,
                     "x": round(float(obs[j][0]), 1), "y": round(float(obs[j][1]), 1)}
                    for j in range(M)],
            "actual": [[float(v) for v in actual[i]] for i in range(K)],
            "kinds": kinds,
            "series": series,
            "rho": round(rho, 3), "background_sd_m": round(amp, 5),
        }
    raise RuntimeError("scene generation failed")


# ---------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="raw_data")
    ap.add_argument("--n-scenes", type=int, default=2600)
    ap.add_argument("--seed", type=int, default=20260920)
    ap.add_argument("--cache", default="nwis_cache")
    args = ap.parse_args()

    out = Path(args.out); (out / "series").mkdir(parents=True, exist_ok=True)
    bg, sites, prov = fetch_background(Path(args.cache))
    print("real background pool: %d conditioned NWIS wells" % bg.shape[0])

    # Disjoint real-background families across the eventual split: the pool is
    # partitioned once, and a scene only ever draws from its own partition, so
    # no real monitoring well contributes to both train and test scenes.
    prng = np.random.default_rng(args.seed ^ 0x5EED)
    perm = prng.permutation(bg.shape[0])
    cut = int(0.72 * bg.shape[0])
    POOL = {"A": bg[perm[:cut]], "B": bg[perm[cut:]]}
    POOL_SITES = {"A": [sites[i] for i in perm[:cut]], "B": [sites[i] for i in perm[cut:]]}
    print("background families: %d in pool A, %d in pool B (disjoint)"
          % (len(POOL_SITES["A"]), len(POOL_SITES["B"])))

    rng = np.random.default_rng(args.seed)
    rows = []
    tcols = ["t%03d" % k for k in range(NT)]
    for n in range(args.n_scenes):
        pool = "A" if rng.random() < 0.72 else "B"
        sc = gen_scene(rng, POOL[pool], "SC%05d" % n)
        sc["bg_pool"] = pool
        with open(out / "series" / ("%s.csv" % sc["scene_id"]), "w") as w:
            w.write("obs_id," + ",".join(tcols) + "\n")
            for j, o in enumerate(sc["obs"]):
                w.write(o["obs_id"] + "," + ",".join("%.4f" % v for v in sc["series"][j]) + "\n")
        rows.append({k: sc[k] for k in
                     ("scene_id", "bg_pool", "n_boreholes", "n_obs", "log_t", "log_s",
                      "rho", "background_sd_m")}
                    | {"boreholes_json": json.dumps(sc["boreholes"], separators=(",", ":")),
                       "obs_json": json.dumps(sc["obs"], separators=(",", ":")),
                       "actual_json": json.dumps(sc["actual"], separators=(",", ":")),
                       "kinds_json": json.dumps(sc["kinds"], separators=(",", ":")),
                       "series_file": "series/%s.csv" % sc["scene_id"]})
        if (n + 1) % 200 == 0:
            print("  %d/%d scenes" % (n + 1, args.n_scenes), flush=True)

    import csv
    with open(out / "scenes.csv", "w", newline="") as w:
        wr = csv.DictWriter(w, fieldnames=list(rows[0].keys()))
        wr.writeheader(); wr.writerows(rows)

    (out / "BACKGROUND_PROVENANCE.json").write_text(json.dumps(
        {"service": "USGS NWIS instantaneous values",
         "parameter_code": "72019 (depth to water level, feet below land surface)",
         "period": "P30D", "requests": prov,
         "conditioning": "3-hourly grid, 224 samples over 28 days; feet to metres; "
                         "sign flipped to head-like; quadratic trend removed; wells kept "
                         "when residual sd is 0.004-1.5 m and no single spike exceeds "
                         "12 sd + 0.05 m",
         "pool_size": int(bg.shape[0]),
         "pool_partition": {"A": len(POOL_SITES["A"]), "B": len(POOL_SITES["B"])},
         "license": "USGS water data are US Government works in the public domain"},
        indent=2))
    (out / "LICENSE.txt").write_text(
        "Groundwater Abstraction Return Reconciliation - raw corpus\n"
        "CC0 1.0 Universal (public domain dedication).\n\n"
        "The abstraction scenes, aquifer parameters, declaration errors and Theis\n"
        "drawdown are procedurally generated by generate.py, which is author-owned.\n"
        "The background fluctuation is derived from USGS NWIS instantaneous\n"
        "groundwater-level data, which are US Government works in the public domain.\n"
        "No third-party media or assets are included.\n")
    print("wrote %d scenes to %s" % (len(rows), out))


if __name__ == "__main__":
    main()

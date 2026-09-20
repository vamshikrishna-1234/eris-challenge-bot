#!/usr/bin/env python3
"""Corpus generator for the sparse-probe roundness inspection corpus.

The corpus models production coordinate-measuring-machine (CMM) inspection of turned and ground
circular features. Touch-trigger probing is slow, so a production inspection plan probes only a
handful of points around each circle. Each part is machined in one set-up on one machine, and the
form error of a machined circular surface is dominated by a small number of undulations per
revolution (UPR) whose orders are characteristic of the machine and fixturing.

Spectral model, calibrated against real measured traces
-------------------------------------------------------
The radial form deviation of a feature is a Fourier series over UPR orders k = 2..30 with
circular-Gaussian coefficients (Rayleigh amplitude, uniform phase) whose per-order standard
deviation follows a power-law envelope with discrete enhancement at the orders that the machine
set-up excites.

The envelope exponent and the enhanced orders were fitted to Taylor Hobson Talyrond TR31c traces of
five roundness reference workpieces (3600 points per revolution, ISO 12181-2 Gaussian filter with a
15 UPR cutoff), published as Zenodo record 7004548, "Roundness Measurement Dataset", Aalto
University, CC BY 4.0. The fit gave amplitude ~ C * k^alpha with alpha = -1.935, dominant content at
k = 1, 2, 3 and 5, and a discrete order spike at k = 12 on one workpiece, with per-workpiece
peak-to-valley roundness spanning 19.9 to 307.5 micrometres. That dataset is a citation only; none of
it is redistributed here and none of it appears in this corpus.

Outputs (raw_data/)
-------------------
features.csv  one row per inspected circular feature, with its probe plan, the drawing tolerance and
              the reference quantities computed from the full harmonic field
points.csv    one row per probed point, giving the probe coordinates in the machine frame
README.txt    provenance and column dictionary
LICENSE.txt   licence of this generated corpus

Usage
-----
    python generate.py --out raw_data --machines 900 --parts 12000 --seed 20260920
"""
import argparse
import csv
import os

import numpy as np

KMIN, KMAX = 2, 30                     # form orders; k = 0 is size and k = 1 is centring
KS = np.arange(KMIN, KMAX + 1)
NK = len(KS)
DENSE = 360                            # evaluation grid for the reference roundness value
FILT_UPR = 15.0                        # ISO 12181-2 Gaussian filter cutoff, UPR
ALPHA0 = np.sqrt(np.log(2.0) / np.pi)
WFILT = np.exp(-np.pi * (ALPHA0 * KS / FILT_UPR) ** 2)
THETA_D = 2 * np.pi * np.arange(DENSE) / DENSE
COS_D = np.cos(np.outer(KS, THETA_D))
SIN_D = np.sin(np.outer(KS, THETA_D))

# machine / set-up signature classes: (name, enhanced UPR orders, scale bias)
SIGNATURES = [
    ("three_jaw_chuck",       (3, 6),       1.00),
    ("clamp_ovality",         (2, 4),       1.00),
    ("spindle_bearing_order", (12, 13),     0.85),
    ("centreless_five_lobe",  (5, 10),      0.95),
    ("fine_ground_smooth",    (),           0.45),
    ("worn_tool_chatter",     (17, 18, 19), 0.90),
]
SIG_NAMES = [s[0] for s in SIGNATURES]
NSIG = len(SIGNATURES)

PROBE_N_CHOICES = np.array([4, 5, 6, 7, 8, 9, 11])
NOMINAL_D = np.array([12.0, 16.0, 20.0, 25.0, 32.0, 40.0, 50.0])         # mm
TOL_LADDER = np.array([2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0,
                       16.0, 20.0, 25.0, 32.0, 40.0, 50.0, 63.0, 80.0, 100.0])   # um
FEATURE_KINDS = ["bore", "shaft", "counterbore", "journal", "seat"]


def roundness_from_coeffs(a, b):
    """RONt: peak-to-valley of the least-squares-circle, 15 UPR Gaussian-filtered profile, in um."""
    prof = (a * WFILT) @ COS_D + (b * WFILT) @ SIN_D
    return prof.max(axis=-1) - prof.min(axis=-1)


def harmonic_sigma(machine):
    """Per-order standard deviation of the cosine/sine coefficients, in um."""
    base = np.exp(machine["log_scale"]) * KS.astype(float) ** machine["alpha"]
    enh = np.ones(NK)
    for order in machine["orders"]:
        if KMIN <= order <= KMAX:
            enh[order - KMIN] = machine["enh"]
    return base * enh


def make_machines(n_machines, rng):
    out = []
    for i in range(n_machines):
        c = int(rng.integers(NSIG))
        _, orders, bias = SIGNATURES[c]
        out.append(dict(
            machine_index=i,
            sig_class=c,
            orders=orders,
            alpha=float(rng.normal(-1.935, 0.28)),
            log_scale=float(rng.normal(np.log(9.0 * bias), 0.55)),
            enh=float(np.exp(rng.normal(np.log(5.0), 0.45))),
            sigma_probe=float(np.exp(rng.normal(np.log(0.45), 0.35))),
            sigma_hf=float(np.exp(rng.normal(np.log(0.35), 0.4))),
            tol_base=float(np.exp(rng.normal(0.0, 0.30))),
        ))
    return out


def make_part(part_index, machine, rng):
    """One part: several circular features cut in one set-up on one machine.

    The probe count varies between the features of a part, so an undulation order hidden from one
    feature's plan by aliasing is visible to another feature's plan. The drawing tolerance is scaled
    to the machine's own process capability, never to the private roundness of the scored feature.
    """
    n_features = int(rng.integers(3, 7))
    plan = np.unique(PROBE_N_CHOICES[rng.integers(0, len(PROBE_N_CHOICES), size=3)])
    if len(plan) == 1:
        plan = np.array([int(plan[0]),
                         int(PROBE_N_CHOICES[rng.integers(len(PROBE_N_CHOICES))])])
    capability = np.exp(machine["log_scale"]) * machine["tol_base"]
    sigma = harmonic_sigma(machine) / np.sqrt(2.0)
    feats = []
    for f in range(n_features):
        a = rng.normal(0.0, sigma)
        b = rng.normal(0.0, sigma)
        ront = float(roundness_from_coeffs(a[None, :], b[None, :])[0])
        n_probe = int(plan[rng.integers(len(plan))])
        theta = (2 * np.pi * np.arange(n_probe) / n_probe
                 + rng.normal(0, 0.012, n_probe) + rng.uniform(0, 2 * np.pi))
        surface = a @ np.cos(np.outer(KS, theta)) + b @ np.sin(np.outer(KS, theta))
        noise = rng.normal(0, float(np.hypot(machine["sigma_probe"], machine["sigma_hf"])), n_probe)
        ecc = rng.normal(0, 6.0)
        psi = rng.uniform(0, 2 * np.pi)
        radial_um = surface + noise + ecc * np.cos(theta - psi)
        d_nom = float(NOMINAL_D[rng.integers(len(NOMINAL_D))])
        raw_tol = capability * float(np.exp(rng.normal(np.log(0.9), 0.45)))
        tol = float(TOL_LADDER[int(np.argmin(np.abs(TOL_LADDER - raw_tol)))])
        radius_mm = d_nom / 2.0 + radial_um / 1000.0
        feats.append(dict(
            part_index=part_index, feature_index=f, kind=FEATURE_KINDS[f % len(FEATURE_KINDS)],
            n_probe=n_probe, d_nom_mm=d_nom, tol_um=tol, theta=theta, radius_mm=radius_mm,
            ront_um=ront, conform=int(ront <= tol), sig_class=machine["sig_class"],
            machine_index=machine["machine_index"],
        ))
    return feats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="raw_data")
    ap.add_argument("--machines", type=int, default=900)
    ap.add_argument("--parts", type=int, default=12000)
    ap.add_argument("--seed", type=int, default=20260920)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    machines = make_machines(args.machines, rng)
    os.makedirs(args.out, exist_ok=True)

    fpath = os.path.join(args.out, "features.csv")
    ppath = os.path.join(args.out, "points.csv")
    n_feat = n_pt = 0
    with open(fpath, "w", newline="", encoding="utf-8") as fh, \
            open(ppath, "w", newline="", encoding="utf-8") as ph:
        fw = csv.writer(fh)
        pw = csv.writer(ph)
        fw.writerow(["machine_index", "part_index", "feature_index", "feature_kind",
                     "n_probe", "nominal_diameter_mm", "roundness_tol_um",
                     "ront_um", "conform", "signature_class"])
        pw.writerow(["part_index", "feature_index", "point_index", "x_mm", "y_mm"])
        for p in range(args.parts):
            machine = machines[int(rng.integers(len(machines)))]
            for ft in make_part(p, machine, rng):
                fw.writerow([ft["machine_index"], ft["part_index"], ft["feature_index"],
                             ft["kind"], ft["n_probe"], "%.1f" % ft["d_nom_mm"],
                             "%.1f" % ft["tol_um"], "%.4f" % ft["ront_um"], ft["conform"],
                             SIG_NAMES[ft["sig_class"]]])
                n_feat += 1
                xs = ft["radius_mm"] * np.cos(ft["theta"])
                ys = ft["radius_mm"] * np.sin(ft["theta"])
                for i in range(ft["n_probe"]):
                    pw.writerow([ft["part_index"], ft["feature_index"], i,
                                 "%.6f" % xs[i], "%.6f" % ys[i]])
                    n_pt += 1

    with open(os.path.join(args.out, "README.txt"), "w", encoding="utf-8") as fh:
        fh.write(
            "Sparse-probe roundness inspection corpus\n"
            "========================================\n\n"
            "Generated by generate.py. Every value is produced by that script from its seed; no\n"
            "third-party data is redistributed here.\n\n"
            "The spectral model is calibrated against measured roundness traces published as Zenodo\n"
            "record 7004548, 'Roundness Measurement Dataset' (Aalto University), CC BY 4.0: Taylor\n"
            "Hobson Talyrond TR31c traces of five roundness reference workpieces at 3600 points per\n"
            "revolution with the ISO 12181-2 Gaussian 15 UPR filter. Fitted envelope exponent -1.935,\n"
            "dominant undulation orders 1, 2, 3 and 5, one discrete order spike at 12.\n\n"
            "features.csv\n"
            "  machine_index        machine / set-up the part was produced on\n"
            "  part_index           part identifier\n"
            "  feature_index        circular feature within the part\n"
            "  feature_kind         bore | shaft | counterbore | journal | seat\n"
            "  n_probe              number of probed points on this feature\n"
            "  nominal_diameter_mm  drawing nominal diameter\n"
            "  roundness_tol_um     drawing roundness tolerance, micrometres\n"
            "  ront_um              reference roundness deviation: peak-to-valley of the\n"
            "                       least-squares-circle, 15 UPR Gaussian-filtered profile\n"
            "  conform              1 when ront_um <= roundness_tol_um, else 0\n"
            "  signature_class      machine / set-up signature: " + ", ".join(SIG_NAMES) + "\n\n"
            "points.csv\n"
            "  part_index, feature_index, point_index, x_mm, y_mm\n"
            "  Probe coordinates in the machine frame. The feature centre is offset from the frame\n"
            "  origin by the set-up centring error, so the circle must be fitted before the form\n"
            "  deviation can be read.\n\n"
            "Counts in this build: %d features, %d probed points, %d machines, %d parts.\n"
            % (n_feat, n_pt, args.machines, args.parts))

    with open(os.path.join(args.out, "LICENSE.txt"), "w", encoding="utf-8") as fh:
        fh.write(
            "This corpus is original work generated by generate.py and is released for unrestricted\n"
            "use, including commercial use, redistribution and modification.\n\n"
            "Attribution for the calibration reference (cited, not redistributed):\n"
            "  Tiainen, T. (2022). Roundness Measurement Dataset. Zenodo.\n"
            "  https://doi.org/10.5281/zenodo.7004548 - CC BY 4.0\n")

    print("features: %d   points: %d   machines: %d   parts: %d"
          % (n_feat, n_pt, args.machines, args.parts))
    print("wrote %s and %s" % (fpath, ppath))


if __name__ == "__main__":
    main()

# Source verification — Groundwater Abstraction Return Reconciliation

## Provenance of every scored field

| Scored field | Where it comes from |
|---|---|
| `actual` (per-borehole abstraction ledger, 7 four-day blocks) | drawn by `generate.py`; it is the rate schedule that actually drives the simulated drawdown in the published series |
| `log_t` (log10 transmissivity, m²/day) | drawn by `generate.py`; it is the transmissivity used in the Theis kernel of the published series |
| `log_s` (log10 storage coefficient) | drawn by `generate.py`; it is the storage coefficient used in that same kernel |

Every scored field is therefore the generator's own state, and the published
observations are an exact physical consequence of it. No label is parsed,
heuristic, hand-annotated or model-produced.

## Real-data gate

The corpus is **procedurally generated over a real measured background** and is
declared as such in `generate.py`, `DATASET_FORM_FILL.md`, `LICENSE.txt` and
the registry entry. No generated quantity is described as measured. The only
measured component is the USGS NWIS background residual, which is used
unmodified apart from the conditioning and private re-mixing documented in
`DATA_ACQUISITION.md`.

## Licence conclusion

- Generated corpus and generator: CC0 1.0 Universal, author-owned, no
  third-party media or assets.
- Background component: USGS water data, US Government work in the public
  domain, redistribution and commercial reuse permitted.

The platform `License` field and `DATASET_FORM_FILL.md` both state CC0 1.0
Universal.

## Physics verification

- Theis drawdown `s = Q/(4·pi·T)·W(u)` with `u = r²S/(4Tt)`, `W` the exponential
  integral `E1`, evaluated by `scipy.special.exp1`.
- Superposition in time is applied to the rate-block differences, so a
  piecewise-constant abstraction schedule produces the exact multi-step
  response; superposition in space sums independent boreholes. Both are exact
  properties of the linear diffusion equation, not approximations.
- Radial distance is floored at 30 m, the scale at which the line-source
  assumption stops being appropriate.
- Parameter ranges: transmissivity 30–800 m²/day, storage coefficient
  5e-4–3e-2, abstraction rates 150–1800 m³/day. These are ordinary
  semi-confined aquifer and licensed-borehole values, and they are chosen so
  the characteristic diffusion time r²S/(4T) lands inside the 28-day
  observation window for the borehole-to-observation distances in play — which
  is what makes the inverse problem identifiable rather than degenerate.

## Reproducibility

`python generate.py --out raw_data --n-scenes 2500` re-downloads the same
official NWIS pulls (or reuses the cache), reconditions them to the same 548
wells, and regenerates the identical corpus from the fixed seed.

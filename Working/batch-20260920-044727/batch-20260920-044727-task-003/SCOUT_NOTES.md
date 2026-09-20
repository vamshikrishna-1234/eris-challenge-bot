# Scout notes — slot batch-20260920-044727-task-003

## Candidate 1 (under pilot): Wind-Turbine Stop-Event Ledger Recovery From 10-Minute SCADA

- Domain: wind-farm operations & maintenance, multichannel 10-min SCADA signals (signal / structured-ledger output). No image classification.
- Sources (official, Zenodo, CC BY 4.0, released by Cubico Sustainable Investments Ltd, curated by C. Plumley):
  - Kelmarsh wind farm data, https://zenodo.org/records/5841834 (6 x Senvion MM92, 2016-2021 yearly zips, 98-474 MB each)
  - Penmanshiel wind farm data, https://zenodo.org/records/8253010 (14 x Senvion MM82, 2016-2022 zips split WT01-10 / WT11-15)
  - Zenodo API license id verified: `cc-by-4.0` for both records (2026-09-20).
- Native inputs: per-turbine 10-min SCADA CSV (299 columns; physical sensors + accounting columns). Only physical channels are used
  (wind, power stats, reactive power, rotor/generator speed, pitch A/B/C, yaw, grid V/f/I, ~14 temperatures, gear-oil pressures,
  cable windings, drive-train acceleration). All availability/lost-production/potential-power/setpoint columns are excluded (leak).
- Native targets: per-turbine controller status log CSV ("Status_*.csv") with `Timestamp start`, `Timestamp end`, `Status`
  (Stop/Warning/Informational/Communication), `Code`, `Message`, `Service contract category`, `IEC category`
  (Forced outage / Scheduled Maintenance / Technical Standby / Requested Shutdown / Out of Electrical Specification / ...).
  These are recorded by the turbine controller / operator SCADA system, not derived by us.
- Proposed unit: one turbine x one ~24 h window (about 144 x 10-min steps) of physical channels + farm-context channels.
- Proposed output: JSON ledger of stop events inside the window: start step, end step, IEC availability category,
  cause family (grouped from the native service-contract category), plus a case confidence.
- Nearest prior work: SCADA normal-behaviour/anomaly detection and fault prediction on Kelmarsh/Penmanshiel; alarm-log mining
  (Leahy et al.); IEC 61400-26 availability accounting. None of them recover an event ledger with category + cause family from
  sensor-only windows. Platform archive: only "Wind Turbine Blade Thermography Maintenance Triage" (CV, unrelated). Registry: none.
- 2016 Kelmarsh pilot counts: 233 stop events >= 20 min across 6 turbines (~39 per turbine-year);
  IEC: Scheduled Maintenance 97, Forced outage 71, Out of Electrical Spec 24, Technical Standby 21, Requested Shutdown 17.
- Known risks to measure: public-corpus retrieval (sliding-window NCC / DTW) -> requires label-preserving transforms
  (nonlinear time warp, gain/offset jitter, thinning, noise, quantization) and a measured probe; rule shortcut for stop detection
  (power ~ 0 while wind > cut-in) -> category/family heads must carry the weight; class sparsity of forced-outage families.

---

## Replacement search (worker 2, 2026-09-20)

Constraints: distinct domain AND modality from slot-1 (photo EXIF exposure ledger), slot-2 (facade photo
to HABS/HAER elevation drawing), and the held wind-SCADA multichannel-timeseries ledger. Lookup attack
must be measured on the PLANNED public representation before any build.

### Duplicate map rebuilt (measured)
- Registry: 92 entries read; titles/status extracted.
- Platform archive: `_all_challenge_titles.txt` is mixed binary; 3,087 real `## ` titles extracted to a
  clean list and keyword-scanned.
- Zero-hit domains on the platform archive include: water/wastewater, HVAC/boiler, welding, elevator,
  traffic signal, parking, railway, aviation/aircraft, pharmacy/dose, dental, transfusion, customs,
  census, banking/payments/fraud, supply chain/warehouse/logistics, irrigation/harvest/dairy/aquaculture,
  recycling/landfill, mining/drilling/tunnel, textile, postal/parcel, keystroke, spirometry, anesthesia,
  borehole/well-log, business-process event logs, **crash / NHTSA / rollover / sequence-of-events**.
- Rejected during scouting on measured or documented grounds:
  - Aviation FDR (NASA), PV plant, VitalDB, UTD19 traffic, well logs: same *modality* as the held
    wind-SCADA candidate (multichannel operational time series -> event ledger). Deconfliction.
  - Business-process event logs (4TU BPI Challenge): platform has 0 hits, but the source's canonical
    tasks (process discovery, predictive monitoring, decision mining) are a famous ML benchmark family;
    `prev_reviews.txt` shows the platform novelty checker scores benchmark-canonical reskins 3-4/10.
  - Interleaved-stream demultiplexing / case correlation: platform already has
    "Recovering Interleaved Source Streams from a Merged Token Sequence" and
    "Interleaved Loanword Stream Deconvolution".
  - NHANES spirometry quality ledger: several scored codes (FET < 6 s, back-extrapolated volume) are
    directly rule-computable from the published curve -> shortcut gate would likely fail.
  - Bike-share rebalancing, airline rotation, FARS-style record bundles: bundling *increases*
    identifiability, so the public representation gets easier to retrieve, not harder.

### Candidate 2 (under pilot): NHTSA CRSS crash event-ledger reconstruction
- Source: NHTSA Crash Report Sampling System (CRSS) annual CSV files, 2016-2023.
  `https://static.nhtsa.gov/nhtsa/downloads/CRSS/<year>/CRSS<year>CSV.zip` (all 8 years HTTP 200).
  US federal government work -> public domain, redistributable. SHA-256 recorded in
  `pilot_crss/archive_sha256.txt`.
- Native target: `cevent.csv`, the officially coded crash **sequence of events**: ordered `EVENTNUM`
  with `VNUMBER1`, `AOI1` (area of impact, clock point), `SOE` (event type), `VNUMBER2`, `AOI2`.
  Coded by trained NHTSA analysts from police crash reports - native, not parser output.
- Measured scale: 417,335 crashes; 143,313 with >= 2 events; 68,663 with >= 3 events.
- Planned public input (answer-bearing fields withheld: HARM_EV, MAN_COLL, M_HARM, IMPACT1, ROLLOVER,
  ROLINLOC, ACC_TYPE, ACC_CONFIG, and every `*_IM` imputed twin): crash context (junction relation,
  road class, light, weather, work zone, unit counts) plus per-vehicle evidence (body-type group,
  model-year and travel-speed buckets, deformation extent, towed, fire, occupants, max injury severity,
  roadway geometry/surface/control, pre-crash critical event and movement, avoidance, pre-impact
  stability) and the **unordered set of damaged areas** per vehicle. Vehicle order is scrambled.
- Why it could be lookup-resistant: the scored ledger is an *ordering + unit-linkage* object over a
  low-entropy categorical evidence vector, inside a 417k-crash pool, so many crashes share an identical
  public representation.
- FIRST measured gate (running before any build): exact-match origin identification and exact-match
  answer recovery of the planned public representation against the whole 8-year public pool, at four
  coarseness levels. This single number is simultaneously the lookup attack and the strongest
  retrieval baseline a solver can run.

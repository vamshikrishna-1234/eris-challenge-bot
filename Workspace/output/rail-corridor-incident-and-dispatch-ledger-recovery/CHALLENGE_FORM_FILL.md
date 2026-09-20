# Challenge form fill — Rail Corridor Incident And Dispatch Ledger Recovery

| Form field | Value |
|---|---|
| Title | Rail Corridor Incident And Dispatch Ledger Recovery |
| Difficulty | Hard |
| Compute tier | CPU |
| Grade direction | Maximize |
| Theoretical minimum | 0.0 |
| Theoretical maximum | 1.0 |
| Tags | time series, structured prediction, operations research, transportation, tabular |

Compute-tier justification: the whole pipeline is tabular and event-based. The reference solution
trains gradient-boosted trees over per-segment, per-station and per-service delay features in about
four CPU minutes and needs under 2 GB of memory. No neural network, no GPU kernel and no pretrained
model is required, so CPU is the correct tier and a GPU request would be unjustified.

---

## Problem description (paste verbatim into the platform Description field)

### Overview

A railway corridor is a chain of stations worked by many services at once. When something goes wrong -
a temporary speed restriction on one section, a blocked section, a station that cannot turn trains
round, a failing vehicle, a crew that reports late - the effect spreads. Later services inherit the
delay through headway and single-track conflicts, and the controller responds by holding services,
terminating them short of their destination, or cancelling them outright. What a control office can
see afterwards is only the planned and the realized stop times. What it needs is the explanation.

Your task is to reconstruct that explanation. For each corridor-window case you are given the planned
and realized arrival and departure times of every service at every corridor stop, and you must output
the hidden operating ledger for that window:

1. **Incidents** - every disruption that left a trace, each with its kind, its place on the corridor
   (a section index, a station index, or a service slot), the ten-minute bucket in which it began, and
   a band for how long it lasted. Only disruptions and actions that actually touched an observed
   movement are scored: a restriction on a section no reported service used is not part of the answer.
2. **Interventions** - every control action taken: holds, short-turns and cancellations, each tied to
   a service slot and a corridor stop.
3. **Primary cause per service** - for each service slot, the single label that explains its running
   that window.

This is not delay forecasting and it is not a split of delay into primary and knock-on minutes. Delay
totals are the evidence, not the answer. The answer is the located, timed and typed incident ledger
together with the control actions and the per-service attribution.

Realized times are produced by a corridor operations model that applies a hidden incident and control
program to a real published operating plan; the model's parameters are not disclosed. Planned times,
stop sequences, service classes and corridor structure are real.

### Files in `public/`

| Item | Description |
|---|---|
| train.csv | 2,400 training cases |
| train_answers.csv | Ledger for each training case |
| test.csv | 800 scored cases |
| sample_submission.csv | Valid baseline submission |

### `train.csv` and `test.csv` columns

| Column | Type | Description |
|---|---|---|
| case_id | string | Corridor-window case |
| train_slot | int | Service index in the case |
| stop_seq | int | Stop order for the service |
| station_index | int | Position along the corridor |
| n_stations | int | Corridor length in stations |
| n_trains | int | Services in the case |
| service_class | string | Long-distance, Commuter, Cargo |
| direction | int | 1 up, -1 down |
| planned_arr | float | Planned arrival, minutes |
| planned_dep | float | Planned departure, minutes |
| observed_arr | float | Realized arrival, may be blank |
| observed_dep | float | Realized departure, may be blank |

Times are minutes from the start of a 180-minute window. The first stop of a service has no planned
arrival. Blank realized values mean the movement was not reported, was cancelled, or lies beyond a
short-turn. Service slots are shuffled inside each case and carry no order.

### `train_answers.csv` columns

| Column | Type | Description |
|---|---|---|
| case_id | string | Corridor-window case |
| ledger_json | string | Ledger object for that case |

### Submission format

| Column | Type | Constraint |
|---|---|---|
| case_id | string | Every test case once |
| ledger_json | string | JSON object, max 20000 chars |

`ledger_json` must be a JSON object with exactly these members:

| Member | Type | Constraint |
|---|---|---|
| incidents | list | At most 12 entries |
| interventions | list | At most 120 entries |
| primary | list | One label per service slot |

An `incidents` entry is an object with `type`, `loc`, `start_bucket`, `dur_band`:

| Field | Type | Constraint |
|---|---|---|
| type | string | See incident kinds |
| loc | int | Index, see below |
| start_bucket | int | 0 to 200 |
| dur_band | int | 0 to 4 |

| Incident kind | What `loc` indexes |
|---|---|
| SPEED_RESTRICTION | Section index |
| SEGMENT_BLOCKAGE | Section index |
| STATION_DWELL_FAULT | Station index |
| UNIT_FAULT | Service slot |
| CREW_LATE | Service slot |

Section index `k` is the track between station `k` and station `k+1`. `start_bucket` is the
ten-minute bucket in which the incident began. `dur_band` bands its duration: 0 under 10 minutes,
1 for 10-20, 2 for 20-35, 3 for 35-60, 4 for 60 or more.

An `interventions` entry is an object with `type`, `train`, `stop`:

| Field | Type | Constraint |
|---|---|---|
| type | string | HOLD, SHORT_TURN, CANCEL |
| train | int | 0 to n_trains-1 |
| stop | int | Station index |

`primary` is a list of length `n_trains`, indexed by service slot, each entry one of `NONE`,
`SPEED_RESTRICTION`, `SEGMENT_BLOCKAGE`, `STATION_DWELL_FAULT`, `UNIT_FAULT`, `CREW_LATE`,
`SHORT_TURNED`, `CANCELLED`.

### Evaluation

The score is the mean over scored cases of

`0.50 * incident_ledger + 0.25 * intervention_ledger + 0.25 * primary_attribution`

and higher is better. Range 0.0 to 1.0; a ledger equal to the hidden one scores exactly 1.0.

`incident_ledger` is a soft F1 over the best one-to-one matching between your incidents and the
hidden ones. A matched pair earns `locality * (0.45 * kind + 0.35 * start + 0.20 * duration)`, where
`locality` is 1.0 at the exact index, 0.40 one index away and 0.10 otherwise, and `start` and
`duration` each give 1.0 for the exact bucket and 0.5 for an adjacent one. The head equals
`2 * matched_credit / (n_true + n_predicted)`, so both missed and invented incidents cost you.

`intervention_ledger` uses the same soft F1 with credit `same_service * (0.60 * type + 0.40 * stop)`,
where `same_service` is 1.0 for the right service slot and 0.10 otherwise, and `stop` gives 1.0 at the
exact station and 0.5 one station away.

`primary_attribution` is the macro-averaged recall over the labels present in the hidden answer, so a
constant guess cannot carry the head.

Entries with an unknown kind, a non-integer field or an out-of-range index are dropped before scoring.
A submission whose case ids do not exactly match the scored set scores 0.0.

### Runtime and dependencies

Build and run your solution within a 1.5-hour CPU budget on 10 cores and 62 GB of memory. `numpy`,
`pandas`, `scipy`, `scikit-learn` and standard-library modules are sufficient; the reference solution
trains in about four CPU minutes. No internet access is available at solve time.

### What not to use

- Do not attempt to identify the real railway, corridor, date or service behind a case, or to fetch
  any external timetable or operations feed. Cases are anonymised, the realized running is modelled,
  and no external record contains the scored ledger.
- Do not submit a constant or near-constant ledger, or an empty one. Both score near the floor and a
  rule-only submission that ignores the modelling problem may be rejected before payout.
- Do not train a large language model, a large transformer or a diffusion model for this task; it is a
  structured tabular and event-sequence problem and such approaches will not fit the runtime budget.
- Do not hard-code case ids, row counts or per-case constants from the public files.

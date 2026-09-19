# Switch-Lamp Logic Circuit Induction From Interventions

## Overview

Commissioning an electrical panel, an HVAC controller, or a relay cabinet often means discovering which switch drives which lamp through hidden logic - the wiring diagram is missing, wrong, or the gates are not what the label claims. The only way forward is to flip switches, watch the lamps, and reason backwards to the latent combinational circuit. A single switch rarely owns a single lamp: lamps respond to combinations (a lamp lit only when two switches agree, or only when exactly one is up), and the same switch can feed several lamps. Recovering that hidden circuit from a short sequence of interventions is a core controls-engineering skill, and it is exactly the kind of multi-step causal reasoning that defeats surface pattern matching.

In each scene a panel has several switches (top row, each shown up for on or down for off) and several lamps (bottom row, lit or dark). A scripted sequence of switch flips is applied; after each flip the lamps settle and the panel is filmed. You are given the clip and a public flip log listing which switch ids changed at each step, so you can reconstruct the switch configuration at every observed moment by reading the starting positions from the clip and applying the logged flips. Each lamp is wired to a hidden subset of switches through one hidden logic gate drawn from `BUF`, `NOT`, `AND`, `OR`, `NAND`, `NOR`, `XOR`, `XNOR`.

You must produce two things. First, the wiring: for every lamp, the logic gate that drives it and the set of switch ids that feed that gate. Second, the lamp pattern for a held-out query switch configuration that is not demonstrated in the clip - you must generalise your induced circuit to a configuration you never saw lit. You also report a `confidence` in `[0, 1]` per scene; calibration is part of the score, so honest uncertainty when the interventions are sparse helps you. Because the flips exercise only part of all possible switch combinations, some lamps' behaviour on never-demonstrated inputs is logically undetermined - confident over-claiming on those is what separates a careful solution from a lucky one.

What Not To Use: solve every scene only from the supplied clip and the public CSV columns. Do not attempt to recover or guess any generation seed, scene configuration, or private file; do not use filenames, row order, or id order as a signal (ids are shuffled and carry no information); do not hard-code answers or rely on any external copy of this data. The circuit is only knowable by reasoning about how the lamps respond to the switch interventions in the clip - there is no hidden lookup, and a "the last switch flipped owns the lamp" heuristic is built to fail. Enforcement on invalid approaches: the grader recomputes the score from a hidden answer file with strict validation; submissions that are malformed, that carry out-of-range confidences, that contain oversized or invalid JSON cells, or that do not match the required row set score 0.

## Inputs

The `public/` archive contains a training split with labels, a test split without labels, a submission template, and the clips. The `video` column gives each scene's clip path relative to the `public/` root, including its split prefix (`train/videos/<id>.mp4` for training rows, `test/videos/<id>.mp4` for test rows).

| Item | Description |
|---|---|
| `train.csv` | Labelled training rows |
| `test.csv` | Unlabelled rows to predict |
| `sample_submission.csv` | Submission template |
| `train/videos/` | Training clips |
| `test/videos/` | Test clips |

The `public/` folder holds five items. `train.csv` is the set of labelled training rows. `test.csv` is the set of rows you must predict, with the answer columns removed. `sample_submission.csv` is a ready-to-edit template in the exact output format. `train/videos/` holds the training clips and `test/videos/` holds the test clips, each named `<id>.mp4`.

### train.csv

| Column | Type | Description |
|---|---|---|
| id | int | Row id |
| video | str | Path to clip |
| n_switches | int | Switch count |
| n_lamps | int | Lamp count |
| flip_log_json | str | Flips per step |
| query_config | str | Held-out config |
| prompt | str | Task prompt |
| wiring_json | str | Lamp wiring |
| query_pattern | str | Lamps for query |

`train.csv` columns: `id` is an integer row identifier; `video` is the string path to the clip relative to the `public/` root (`train/videos/<id>.mp4`); `n_switches` is the integer number of switches; `n_lamps` is the integer number of lamps; `flip_log_json` is a JSON list whose entries are lists of switch ids flipped at each step; `query_config` is a JSON list of 0/1 values, one per switch, giving the held-out configuration to evaluate; `prompt` is the string task statement; `wiring_json` is a JSON object mapping each lamp id (string) to an object with a `gate` string and an `inputs` list of switch ids; and `query_pattern` is a JSON list of 0/1 values giving each lamp's state under `query_config`.

### test.csv

| Column | Type | Description |
|---|---|---|
| id | int | Row id |
| video | str | Path to clip |
| n_switches | int | Switch count |
| n_lamps | int | Lamp count |
| flip_log_json | str | Flips per step |
| query_config | str | Held-out config |
| prompt | str | Task prompt |

`test.csv` columns are identical to `train.csv` but with the two answer columns removed: `id` is the integer row identifier; `video` is the string path to the clip relative to the `public/` root (`test/videos/<id>.mp4`); `n_switches` is the integer switch count; `n_lamps` is the integer lamp count; `flip_log_json` is the JSON list of per-step switch-id flips; `query_config` is the JSON list of 0/1 switch values to evaluate; and `prompt` is the string task statement.

## Submission Format

Predict one row per test `id` with the columns below. Lamp and switch ids are integers; gate tokens are case-insensitive and must be one of `BUF`, `NOT`, `AND`, `OR`, `NAND`, `NOR`, `XOR`, `XNOR`; `query_pattern` must have exactly `n_lamps` entries of 0 or 1; confidence must be a finite number in `[0, 1]`.

| Column | Type | Constraint |
|---|---|---|
| id | int | Matches test id |
| wiring_json | str | Per-lamp gate+inputs |
| query_pattern | str | List of 0/1, len n_lamps |
| confidence | float | in [0, 1] |

Submission columns: `id` is the integer test row id and must match the test id set exactly with no duplicates; `wiring_json` is a JSON object mapping each lamp id (string) to an object with a `gate` token and an `inputs` list of switch ids; `query_pattern` is a JSON list of 0/1 lamp states for the query configuration, with one entry per lamp in lamp-id order; and `confidence` is your finite self-reported certainty in the closed interval `[0, 1]`.

```
id,wiring_json,query_pattern,confidence
0,"{""0"": {""gate"": ""XOR"", ""inputs"": [0, 2]}, ""1"": {""gate"": ""AND"", ""inputs"": [1, 3]}}","[1, 0]",0.74
1,"{""0"": {""gate"": ""BUF"", ""inputs"": [2]}}","[0]",0.30
2,"{""0"": {""gate"": ""OR"", ""inputs"": [0, 1]}, ""1"": {""gate"": ""NOT"", ""inputs"": [2]}}","[1, 1]",0.55
```

## Scoring

Each scene earns two sub-scores. `S_wire` is the mean over lamps of `gate_type_match * input_set_F1`: for each lamp you score 1 for the gate only if your gate token exactly matches the true gate, times the F1 between your input-switch set and the true input set - so naming the wrong gate scores that lamp 0 even with the right inputs. `S_query` is the mean per-lamp on/off agreement between your `query_pattern` and the true lamp states for the held-out configuration. These combine as a squared, weighted correctness `correctness = 0.55*S_wire^2 + 0.45*S_query^2`, then blend with calibration into `row = 0.90*correctness + 0.10*(1 - |confidence - correctness|)`. The final score is `0.68*mean(row) + 0.14*worst(split_group) + 0.10*worst(ood_axis) + 0.08*worst(render_style)`, where each `worst(...)` is the lowest per-group mean over hidden grouping columns, so a solution cannot win on the easy circuits alone. The score is clipped to `[0, 1]`; higher is better.

## Form metadata

- Difficulty: Hard
- Tags: computer-vision, video, causal-reasoning, boolean-logic, rule-induction, synthetic
- Grade direction: Maximize
- Theoretical min / max: 0.0 / 1.0
- GPU tier: A10G

"""Prepare: Rail Corridor Incident And Dispatch Ledger Recovery.

Reads the raw Fintraffic Digitraffic open-data bundle, rebuilds the real corridor
network and the real planned corridor timetables, then constructs corridor
operating scenarios with a stochastic operations model driven by a hidden
incident-and-dispatch program. Deterministic: identical inputs give identical
bytes.
"""
import collections
import datetime as dt
import json
import os
import random

import pandas as pd

WINDOW = 180.0
HEADWAY = 3.0
MIN_DWELL = 0.5
N_TRAIN_CASES = 2400
N_TEST_CASES = 800
SEED_SPLIT = 20260920
SEED_TRAIN = 811311
SEED_TEST = 947701
MIN_RUNS_PER_CORRIDOR = 40
MIN_TRAINS_PER_CASE = 6
MAX_TRAINS_PER_CASE = 60
MIN_STATIONS_PER_CASE = 5
OBS_DROPOUT = 0.05
NOISE_SCALE = 1.0          # audit knob: the achievable-ceiling probe sets this to 0.0
CATEGORIES = ("Long-distance", "Commuter", "Cargo")
INCIDENT_TYPES = ("SPEED_RESTRICTION", "SEGMENT_BLOCKAGE", "STATION_DWELL_FAULT",
                  "UNIT_FAULT", "CREW_LATE")
PRIO = {"Long-distance": 0, "Commuter": 1, "Cargo": 2}
DUR_EDGES = (0, 10, 20, 35, 60, 10 ** 9)


# ------------------------------------------------------------------ raw input
def find_raw(root="raw"):
    for cand in (os.path.join(root, "raw_upload"), root, "."):
        if os.path.isdir(cand) and any(f.startswith("trains_") for f in os.listdir(cand)):
            return cand
    raise FileNotFoundError("raw Digitraffic bundle not found")


def load_days(raw_dir):
    days = {}
    for name in sorted(os.listdir(raw_dir)):
        if not (name.startswith("trains_") and name.endswith(".json")):
            continue
        with open(os.path.join(raw_dir, name), encoding="utf-8") as fh:
            days[name[len("trains_"):-len(".json")]] = json.load(fh)
    assert len(days) >= 5, "expected at least five timetable dates in the raw bundle"
    return days


def train_stops(train):
    ordered = collections.OrderedDict()
    for row in train["timeTableRows"]:
        code = row["stationShortCode"]
        stamp = dt.datetime.fromisoformat(row["scheduledTime"].replace("Z", "+00:00"))
        minute = stamp.hour * 60 + stamp.minute + stamp.second / 60.0
        if code not in ordered:
            ordered[code] = [None, None, bool(row.get("trainStopping"))]
        if row["type"] == "ARRIVAL":
            ordered[code][0] = minute
        else:
            ordered[code][1] = minute
    out = []
    for code, (arr, dep, stopping) in ordered.items():
        arr = dep if arr is None else arr
        dep = arr if dep is None else dep
        out.append((code, arr, dep, stopping))
    for i in range(1, len(out)):
        code, arr, dep, stopping = out[i]
        while arr < out[i - 1][2] - 60:
            arr += 1440
            dep += 1440
        out[i] = (code, arr, max(arr, dep), stopping)
    return out


def segment_traffic(days):
    counter = collections.Counter()
    for trains in days.values():
        for train in trains:
            if train.get("trainCategory") not in CATEGORIES:
                continue
            path = [s for s, _, _, _ in train_stops(train)]
            for a, b in zip(path, path[1:]):
                if a != b:
                    counter[tuple(sorted((a, b)))] += 1
    return counter


def corridors_from(counter, n_days, min_per_day=3.0, min_len=4):
    graph = collections.defaultdict(set)
    for (a, b), count in counter.items():
        if count / n_days >= min_per_day:
            graph[a].add(b)
            graph[b].add(a)
    junctions = {n for n in graph if len(graph[n]) != 2}
    chains, seen = [], set()
    for node in sorted(junctions):
        for nb in sorted(graph[node]):
            if (node, nb) in seen:
                continue
            path = [node, nb]
            seen.add((node, nb))
            seen.add((nb, node))
            while path[-1] not in junctions:
                nxt = [x for x in sorted(graph[path[-1]]) if x != path[-2]]
                if not nxt:
                    break
                seen.add((path[-1], nxt[0]))
                seen.add((nxt[0], path[-1]))
                path.append(nxt[0])
            chains.append(path)
    uniq = {}
    for chain in chains:
        if len(chain) < min_len:
            continue
        key = tuple(sorted((chain[0], chain[-1])))
        if key not in uniq or len(chain) > len(uniq[key]):
            uniq[key] = chain
    return [uniq[k] for k in sorted(uniq)]


def corridor_runs(days, corridor, min_stops=4):
    pos = {code: i for i, code in enumerate(corridor)}
    runs = []
    for date in sorted(days):
        for train in days[date]:
            if train.get("trainCategory") not in CATEGORIES:
                continue
            hit = [(pos[c], a, d, s) for c, a, d, s in train_stops(train) if c in pos]
            if len(hit) < min_stops:
                continue
            idx = [h[0] for h in hit]
            up = all(idx[i + 1] == idx[i] + 1 for i in range(len(idx) - 1))
            down = all(idx[i + 1] == idx[i] - 1 for i in range(len(idx) - 1))
            if not (up or down):
                continue
            runs.append({"date": date, "num": train["trainNumber"],
                         "cat": train["trainCategory"], "dirn": 1 if up else -1,
                         "stops": [(i, round(a, 3), round(d, 3), bool(s)) for i, a, d, s in hit]})
    runs.sort(key=lambda r: (r["date"], r["num"]))
    return runs


# ------------------------------------------------------- operations modelling
def dur_band(x):
    for i in range(len(DUR_EDGES) - 1):
        if DUR_EDGES[i] <= x < DUR_EDGES[i + 1]:
            return i
    return len(DUR_EDGES) - 2


def make_program(rng, n_seg, n_sta, n_trains):
    program = []
    for _ in range(rng.choice([1, 1, 2, 2, 2, 3, 3, 4])):
        kind = rng.choices(INCIDENT_TYPES, weights=[34, 10, 20, 20, 16])[0]
        start = round(rng.uniform(0, max(1.0, WINDOW - 15)), 1)
        if kind == "SPEED_RESTRICTION":
            dur, loc, sev = rng.uniform(15, 110), rng.randrange(n_seg), rng.uniform(0.25, 1.4)
        elif kind == "SEGMENT_BLOCKAGE":
            dur, loc, sev = rng.uniform(8, 45), rng.randrange(n_seg), 1.0
        elif kind == "STATION_DWELL_FAULT":
            dur, loc, sev = rng.uniform(15, 90), rng.randrange(n_sta), rng.uniform(2, 14)
        elif kind == "UNIT_FAULT":
            dur, loc, sev = rng.uniform(20, 120), rng.randrange(n_trains), rng.uniform(0.5, 2.2)
        else:
            dur = rng.uniform(3, 35)
            loc, sev = rng.randrange(n_trains), dur
        program.append({"type": kind, "loc": int(loc), "start": round(start, 1),
                        "dur": round(dur, 1), "sev": round(sev, 3)})
    program.sort(key=lambda p: (p["start"], p["type"], p["loc"]))
    return program


def simulate(n_stations, single, trains, program, rng):
    n_seg = n_stations - 1
    speed = [[] for _ in range(n_seg)]
    block = [[] for _ in range(n_seg)]
    dwell = [[] for _ in range(n_stations)]
    unit, crew = {}, {}
    for k, p in enumerate(program):
        a, b = p["start"], p["start"] + p["dur"]
        if p["type"] == "SPEED_RESTRICTION":
            speed[p["loc"] % n_seg].append((a, b, p["sev"], k))
        elif p["type"] == "SEGMENT_BLOCKAGE":
            block[p["loc"] % n_seg].append((a, b, k))
        elif p["type"] == "STATION_DWELL_FAULT":
            dwell[p["loc"] % n_stations].append((a, b, p["sev"], k))
        elif p["type"] == "UNIT_FAULT":
            unit.setdefault(p["loc"] % len(trains), []).append((a, b, p["sev"], k))
        else:
            crew.setdefault(p["loc"] % len(trains), []).append((a, b, p["sev"], k))

    def active(items, t):
        for a, b, s, k in items:
            if a <= t < b:
                return s, k
        return 0.0, -1

    def blocked(seg, t):
        until, which = None, -1
        for a, b, k in block[seg]:
            if a <= t < b and (until is None or b > until):
                until, which = b, k
        return until, which

    order = sorted(range(len(trains)),
                   key=lambda i: trains[i]["stops"][0][2] + 5.0 * PRIO.get(trains[i]["cat"], 1)
                   + rng.gauss(0, 3.0))
    seg_free, obs, interventions = {}, [], []
    cause = [-1] * len(trains)
    primary = ["NONE"] * len(trains)
    cancelled = {i for i in order if rng.random() < 0.02}

    for i in order:
        stops = trains[i]["stops"]
        if i in cancelled:
            interventions.append({"type": "CANCEL", "train": i, "stop": int(stops[0][0])})
            primary[i] = "CANCELLED"
            for j, (idx, pa, pd_, _) in enumerate(stops):
                obs.append({"train": i, "seq": j, "station": int(idx),
                            "parr": None if j == 0 else round(pa, 2), "pdep": round(pd_, 2),
                            "arr": None, "dep": None})
            continue
        extra, kc = 0.0, -1
        for a, _b, s, k in crew.get(i, []):
            if a <= stops[0][2] + 5:
                extra, kc = max(extra, s), k
        t = stops[0][2] + extra + NOISE_SCALE * rng.gauss(0, 0.7)
        if kc >= 0:
            cause[i] = kc
        rows = [(0, stops[0][0], None, round(t, 2))]
        short = False
        for j in range(1, len(stops)):
            idx0, _pa0, pd0, _ = stops[j - 1]
            idx1, pa1, pd1, _ = stops[j]
            seg = min(idx0, idx1)
            planned_run = max(0.5, pa1 - pd0)
            fs, ks = active(speed[seg], t)
            fu, ku = active(unit.get(i, []), t)
            key = (seg,) if single[seg] else (seg, trains[i]["dirn"])
            wait = max(0.0, seg_free.get(key, -1e9) + HEADWAY - t)
            until, kb = blocked(seg, t)
            if until is not None and until - t > wait:
                wait = until - t
                if cause[i] < 0:
                    cause[i] = kb
            if wait > 4.0:
                interventions.append({"type": "HOLD", "train": i, "stop": int(idx0)})
            t += wait
            if ks >= 0 and cause[i] < 0:
                cause[i] = ks
            if ku >= 0 and cause[i] < 0:
                cause[i] = ku
            t += planned_run * (1.0 + fs + fu) + NOISE_SCALE * abs(rng.gauss(0, 0.35))
            seg_free[key] = t
            arrival = t
            fd, kd = active(dwell[idx1], t)
            if kd >= 0 and cause[i] < 0:
                cause[i] = kd
            stay = max(MIN_DWELL, (pd1 - pa1) + fd + NOISE_SCALE * abs(rng.gauss(0, 0.4)))
            t = arrival + stay if trains[i]["cat"] == "Cargo" else max(arrival + stay, pd1)
            rows.append((j, idx1, round(arrival, 2), round(t, 2)))
            if arrival - pa1 > 25 and j < len(stops) - 1 and rng.random() < 0.25:
                interventions.append({"type": "SHORT_TURN", "train": i, "stop": int(idx1)})
                short = True
                break
        if short:
            primary[i] = "SHORT_TURNED"
        for j, idx, arr, dep in rows:
            drop = rng.random() < OBS_DROPOUT
            obs.append({"train": i, "seq": j, "station": int(idx),
                        "parr": None if j == 0 else round(stops[j][1], 2),
                        "pdep": round(stops[j][2], 2),
                        "arr": None if (arr is None or drop) else arr,
                        "dep": None if drop else dep})
        for j in range(len(rows), len(stops)):
            obs.append({"train": i, "seq": j, "station": int(stops[j][0]),
                        "parr": round(stops[j][1], 2), "pdep": round(stops[j][2], 2),
                        "arr": None, "dep": None})
    for i in range(len(trains)):
        if primary[i] in ("CANCELLED", "SHORT_TURNED"):
            continue
        primary[i] = program[cause[i]]["type"] if cause[i] >= 0 else "NONE"
    seen, deduped = set(), []
    for item in sorted(interventions, key=lambda d: (d["type"], d["train"], d["stop"])):
        key = (item["type"], item["train"], item["stop"])
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    obs.sort(key=lambda o: (o["train"], o["seq"]))

    # Only disruptions and actions that left a trace in the published rows are scored:
    # a restriction on a section no observed movement used is not recoverable by anyone,
    # and scoring it would charge solvers for information the data does not contain.
    per_train = collections.defaultdict(list)
    for o in obs:
        per_train[o["train"]].append(o)
    seen_rows = {i: sum(1 for o in r if o["arr"] is not None or o["dep"] is not None)
                 for i, r in per_train.items()}

    def traced(p):
        a, b = p["start"] - 15.0, p["start"] + p["dur"] + 15.0
        if p["type"] in ("UNIT_FAULT", "CREW_LATE"):
            return seen_rows.get(p["loc"] % len(trains), 0) >= 2
        if p["type"] == "STATION_DWELL_FAULT":
            k = p["loc"] % n_stations
            return any(o["station"] == k and o["arr"] is not None and o["dep"] is not None
                       and a <= o["arr"] <= b for o in obs)
        k = p["loc"] % n_seg
        for rows_i in per_train.values():
            for x, y in zip(rows_i, rows_i[1:]):
                if min(x["station"], y["station"]) != k:
                    continue
                if x["dep"] is None or y["arr"] is None:
                    continue
                if a <= x["dep"] <= b:
                    return True
        return False

    scored = [p for p in program if traced(p)]
    deduped = [v for v in deduped
               if v["type"] == "CANCEL" or seen_rows.get(v["train"], 0) >= 2]
    ledger = {"incidents": [{"type": p["type"], "loc": p["loc"],
                             "start_bucket": int(p["start"] // 10),
                             "dur_band": dur_band(p["dur"])} for p in scored],
              "interventions": deduped, "primary": primary,
              "n_stations": int(n_stations)}
    return obs, ledger


# ------------------------------------------------------------- case assembly
def build_case(sub, rng):
    runs = sub["runs"]
    for _ in range(60):
        date = rng.choice(runs)["date"]
        starts = [r["stops"][0][2] for r in runs if r["date"] == date]
        if not starts:
            continue
        ws = max(0.0, rng.choice(starts) - rng.uniform(0, 40))
        selected = []
        for r in runs:
            if r["date"] != date:
                continue
            stops = [(i, a, d, s) for i, a, d, s in r["stops"] if ws <= a <= ws + WINDOW and ws <= d <= ws + WINDOW]
            if len(stops) < 4:
                continue
            selected.append({"cat": r["cat"], "dirn": r["dirn"], "num": r["num"],
                             "stops": [(i, round(a - ws, 2), round(d - ws, 2), s) for i, a, d, s in stops]})
        if not (MIN_TRAINS_PER_CASE <= len(selected) <= MAX_TRAINS_PER_CASE):
            continue
        if len({i for t in selected for i, _, _, _ in t["stops"]}) < MIN_STATIONS_PER_CASE:
            continue
        rng.shuffle(selected)
        return date, ws, selected
    return None


def generate_cases(subs, ids, n_cases, seed, prefix):
    rng = random.Random(seed)
    cases = []
    while len(cases) < n_cases:
        k = ids[rng.randrange(len(ids))]
        sub = subs[k]
        built = build_case(sub, rng)
        if built is None:
            continue
        date, ws, trains = built
        n_sta = len(sub["corr"])
        local = random.Random(rng.getrandbits(48))
        program = make_program(local, max(1, n_sta - 1), n_sta, len(trains))
        obs, ledger = simulate(n_sta, sub["single"], trains, program, local)
        cases.append({"case_id": "%s%05d" % (prefix, len(cases)),
                      "n_stations": n_sta, "n_trains": len(trains),
                      "classes": [t["cat"] for t in trains],
                      "dirs": [t["dirn"] for t in trains],
                      "obs": obs, "ledger": ledger,
                      # organiser-only provenance; never written to public/ or private/
                      "origin": {"corridor": list(sub["corr"]), "date": date, "ws": ws,
                                 "train_numbers": [t["num"] for t in trains],
                                 "stops": [t["stops"] for t in trains]}})
    return cases


def observation_frame(cases):
    rows = []
    for c in cases:
        for o in c["obs"]:
            rows.append((c["case_id"], o["train"], o["seq"], o["station"],
                         c["n_stations"], c["n_trains"],
                         c["classes"][o["train"]], c["dirs"][o["train"]],
                         o["parr"], o["pdep"], o["arr"], o["dep"]))
    frame = pd.DataFrame(rows, columns=["case_id", "train_slot", "stop_seq", "station_index",
                                        "n_stations", "n_trains", "service_class", "direction",
                                        "planned_arr", "planned_dep", "observed_arr", "observed_dep"])
    return frame.sort_values(["case_id", "train_slot", "stop_seq"]).reset_index(drop=True)


def ledger_frame(cases):
    rows = [(c["case_id"], json.dumps(c["ledger"], sort_keys=True, separators=(",", ":")))
            for c in cases]
    return pd.DataFrame(rows, columns=["case_id", "ledger_json"]).sort_values("case_id").reset_index(drop=True)


def sample_submission(cases, train_cases):
    """Non-degenerate label-prior baseline: the commonest incident type at the corridor
    mid-point, no interventions, and every train marked NONE."""
    counts = collections.Counter(i["type"] for c in train_cases for i in c["ledger"]["incidents"])
    kind = counts.most_common(1)[0][0]
    starts = sorted(i["start_bucket"] for c in train_cases for i in c["ledger"]["incidents"])
    bands = sorted(i["dur_band"] for c in train_cases for i in c["ledger"]["incidents"])
    sb = starts[len(starts) // 2]
    db = bands[len(bands) // 2]
    rows = []
    for c in cases:
        guess = {"incidents": [{"type": kind, "loc": (c["n_stations"] - 1) // 2,
                                "start_bucket": int(sb), "dur_band": int(db)}],
                 "interventions": [],
                 "primary": ["NONE"] * c["n_trains"]}
        rows.append((c["case_id"], json.dumps(guess, sort_keys=True, separators=(",", ":"))))
    return pd.DataFrame(rows, columns=["case_id", "ledger_json"]).sort_values("case_id").reset_index(drop=True)


def main():
    raw_dir = find_raw()
    days = load_days(raw_dir)
    counter = segment_traffic(days)
    corrs = corridors_from(counter, len(days))
    n_days = len(days)
    subs = []
    for corr in corrs:
        runs = corridor_runs(days, corr)
        if len(runs) < MIN_RUNS_PER_CORRIDOR:
            continue
        single = [counter[tuple(sorted((corr[i], corr[i + 1])))] / n_days < 25
                  for i in range(len(corr) - 1)]
        subs.append({"corr": corr, "runs": runs, "single": single})
    assert len(subs) >= 24, "expected at least 24 usable corridors, found %d" % len(subs)

    split = random.Random(SEED_SPLIT)
    order = list(range(len(subs)))
    split.shuffle(order)
    cut = int(round(len(order) * 0.6))
    train_ids, test_ids = sorted(order[:cut]), sorted(order[cut:])
    assert not set(train_ids) & set(test_ids)
    assert len(test_ids) >= 10, "hidden split needs at least 10 independent corridors"

    train_cases = generate_cases(subs, train_ids, N_TRAIN_CASES, SEED_TRAIN, "TR")
    test_cases = generate_cases(subs, test_ids, N_TEST_CASES, SEED_TEST, "TE")

    os.makedirs("public", exist_ok=True)
    os.makedirs("private", exist_ok=True)
    train_obs = observation_frame(train_cases)
    test_obs = observation_frame(test_cases)
    train_ans = ledger_frame(train_cases)
    test_ans = ledger_frame(test_cases)
    sample = sample_submission(test_cases, train_cases)

    # --- invariants -------------------------------------------------------
    assert set(train_obs.case_id) & set(test_obs.case_id) == set()
    assert list(sample.case_id) == list(test_ans.case_id)
    assert test_obs.case_id.nunique() == N_TEST_CASES
    assert train_obs.case_id.nunique() == N_TRAIN_CASES
    assert train_obs[["planned_dep"]].notna().all().all()
    for frame in (train_obs, test_obs):
        assert frame.station_index.between(0, frame.n_stations - 1).all()
        assert frame.train_slot.between(0, frame.n_trains - 1).all()
        assert frame.planned_dep.between(-5, WINDOW + 5).all()
    kinds = collections.Counter(i["type"] for c in test_cases for i in c["ledger"]["incidents"])
    for kind in INCIDENT_TYPES:
        assert kinds[kind] >= 25, "hidden split is thin on %s (%d)" % (kind, kinds[kind])
    prim = collections.Counter(p for c in test_cases for p in c["ledger"]["primary"])
    for cls in ("NONE", "SHORT_TURNED", "CANCELLED"):
        assert prim[cls] >= 25, "hidden split is thin on primary class %s" % cls

    train_obs.to_csv("public/train.csv", index=False)
    train_ans.to_csv("public/train_answers.csv", index=False)
    test_obs.to_csv("public/test.csv", index=False)
    sample.to_csv("public/sample_submission.csv", index=False)
    test_ans.to_csv("private/answers.csv", index=False)
    print("train cases %d rows %d | test cases %d rows %d | corridors %d/%d"
          % (N_TRAIN_CASES, len(train_obs), N_TEST_CASES, len(test_obs),
             len(train_ids), len(test_ids)))


if __name__ == "__main__":
    main()

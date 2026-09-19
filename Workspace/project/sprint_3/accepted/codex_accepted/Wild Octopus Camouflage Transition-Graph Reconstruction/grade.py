"""Strict grader for Opaque Security Clip Action Ledger Recovery."""

from __future__ import annotations

import json
import math
from typing import Any

import numpy as np
import pandas as pd


class InvalidSubmissionError(ValueError):
    """Raised for malformed submission files (not malformed row content)."""


SUBMISSION_COLUMNS = ["id", "graph_json"]
MAX_JSON_CHARS = 20_000
MAX_NODES = 32
MAX_EDGES = 256
AGENTS = {"hand", "person", "vehicle"}
ACTIONS = {
    "abandons", "carries", "closes", "drops_off", "embraces", "enters",
    "exits", "interacts", "loads", "makes_u_turn", "opens", "picks_up",
    "purchases", "puts_down", "reads", "reverses", "rides", "sits",
    "stands", "starts", "steals", "stops", "talks", "texts", "transfers",
    "turns", "unloads",
}
CONTEXTS = {
    "bicycle", "document", "facility_door", "heavy_object", "laptop", "left",
    "none", "object", "package", "person", "phone", "right",
    "scene_structure", "trunk", "vehicle", "vehicle_door",
}
ROLES = {"bag", "bicycle", "other", "person", "receptacle", "vehicle"}
EDGE_TYPES = {"documented_pair", "temporal_next", "temporal_overlap"}


def grade(submission: pd.DataFrame, answers: pd.DataFrame) -> float:
    """Return the bounded MEVA ActivityCouplingGraphScore in [0, 1]."""
    sub, ans = _validate_frames(submission, answers)
    row_scores: list[float] = []
    parsed_truth: list[dict[str, Any]] = []

    for value in ans["graph_json"].tolist():
        graph = _parse_graph(value)
        if graph is None:
            raise RuntimeError("Internal answer package is invalid.")
        parsed_truth.append(graph)

    for pred_value, true_graph in zip(sub["graph_json"].tolist(), parsed_truth):
        pred_graph = _parse_graph(pred_value)
        row_scores.append(0.0 if pred_graph is None else _graph_score(pred_graph, true_graph))

    scores = np.asarray(row_scores, dtype=np.float64)
    event_mask = np.asarray([bool(g["nodes"]) for g in parsed_truth], dtype=bool)
    declared = ans["event_presence"].astype(int).to_numpy() != 0
    if not np.array_equal(event_mask, declared):
        raise RuntimeError("Internal answer package is invalid.")

    positive_mean = float(scores[event_mask].mean()) if event_mask.any() else float(scores.mean())
    negative_mean = float(scores[~event_mask].mean()) if (~event_mask).any() else float(scores.mean())
    balanced_mean = 0.80 * positive_mean + 0.20 * negative_mean

    group_means = []
    for _, idx in ans.groupby("session_group", sort=True).groups.items():
        loc = np.asarray(list(idx), dtype=int)
        if loc.size:
            group_means.append(float(scores[loc].mean()))
    if not group_means:
        raise RuntimeError("Internal answer package is invalid.")
    worst_session = min(group_means)

    final = 0.88 * balanced_mean + 0.12 * worst_session
    if not math.isfinite(final):
        raise RuntimeError("Internal scoring failure.")
    return float(np.clip(final, 0.0, 1.0))


class _DuplicateKey(ValueError):
    pass


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise _DuplicateKey(key)
        out[key] = value
    return out


def _validate_frames(submission: pd.DataFrame, answers: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not isinstance(submission, pd.DataFrame) or not isinstance(answers, pd.DataFrame):
        raise InvalidSubmissionError("Submission must be a CSV table.")
    sub = submission.copy().reset_index(drop=True)
    ans = answers.copy().reset_index(drop=True)

    cleaned = [str(c).strip().lstrip("\ufeff") for c in sub.columns]
    if len(set(cleaned)) != len(cleaned):
        raise InvalidSubmissionError("Submission columns are invalid.")
    sub.columns = cleaned
    # Compare both the cleaned copy and original frame explicitly so reordered
    # columns are rejected while a harmless UTF-8 BOM is tolerated.
    if list(submission.columns) != SUBMISSION_COLUMNS and list(sub.columns) != SUBMISSION_COLUMNS:
        raise InvalidSubmissionError("Submission must contain exactly: id, graph_json (in that order).")

    required_answers = {"id", "graph_json", "session_group", "event_presence"}
    if not required_answers.issubset(ans.columns):
        raise RuntimeError("Internal answer package is invalid.")

    if sub["id"].isna().any() or sub["id"].astype(str).str.strip().eq("").any():
        raise InvalidSubmissionError("Submission ids are invalid.")
    sub["id"] = sub["id"].astype(str).str.strip()
    ans["id"] = ans["id"].astype(str).str.strip()
    if sub["id"].duplicated().any():
        raise InvalidSubmissionError("Submission contains duplicate ids.")
    if ans["id"].duplicated().any():
        raise RuntimeError("Internal answer package is invalid.")
    if len(sub) != len(ans) or set(sub["id"]) != set(ans["id"]):
        raise InvalidSubmissionError("Submission ids do not match the required row set.")

    # Exact one-to-one alignment; no inner join and no quadratic row lookup.
    sub = sub.set_index("id", drop=False).loc[ans["id"].tolist()].reset_index(drop=True)
    return sub, ans


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _parse_graph(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, str) or len(value) > MAX_JSON_CHARS:
        return None
    try:
        data = json.loads(value, object_pairs_hook=_pairs_no_duplicates)
    except (json.JSONDecodeError, TypeError, ValueError, OverflowError, RecursionError):
        return None
    if not isinstance(data, dict) or set(data) != {"nodes", "edges"}:
        return None
    nodes, edges = data["nodes"], data["edges"]
    if not isinstance(nodes, list) or not isinstance(edges, list):
        return None
    if len(nodes) > MAX_NODES or len(edges) > MAX_EDGES:
        return None

    clean_nodes: list[dict[str, Any]] = []
    for expected_id, node in enumerate(nodes):
        if not isinstance(node, dict) or set(node) != {"id", "start", "end", "state"}:
            return None
        if not all(_is_int(node[k]) for k in ("id", "start", "end")):
            return None
        if node["id"] != expected_id or not (0 <= node["start"] <= node["end"] <= 31):
            return None
        state = node["state"]
        if not isinstance(state, dict) or set(state) != {"agent", "action", "context", "roles"}:
            return None
        if state["agent"] not in AGENTS or state["action"] not in ACTIONS or state["context"] not in CONTEXTS:
            return None
        roles = state["roles"]
        if not isinstance(roles, list) or any(not isinstance(x, str) or x not in ROLES for x in roles):
            return None
        if roles != sorted(set(roles)):
            return None
        clean_nodes.append({
            "id": node["id"], "start": node["start"], "end": node["end"],
            "state": {"agent": state["agent"], "action": state["action"],
                      "context": state["context"], "roles": roles},
        })

    node_keys = [_node_sort_key(n) for n in clean_nodes]
    if node_keys != sorted(node_keys):
        return None

    clean_edges: list[dict[str, Any]] = []
    seen_edges: set[tuple[int, int, str]] = set()
    seen_pairs: set[tuple[int, int]] = set()
    for edge in edges:
        if not isinstance(edge, dict) or set(edge) != {"from", "to", "type"}:
            return None
        if not _is_int(edge["from"]) or not _is_int(edge["to"]) or edge["type"] not in EDGE_TYPES:
            return None
        src, dst, typ = edge["from"], edge["to"], edge["type"]
        if not (0 <= src < dst < len(clean_nodes)):
            return None
        triple = (src, dst, typ)
        pair = (src, dst)
        if triple in seen_edges or pair in seen_pairs:
            return None
        seen_edges.add(triple)
        seen_pairs.add(pair)
        clean_edges.append({"from": src, "to": dst, "type": typ})
    if [(e["from"], e["to"], e["type"]) for e in clean_edges] != sorted(seen_edges):
        return None
    if not clean_nodes and clean_edges:
        return None
    return {"nodes": clean_nodes, "edges": clean_edges}


def _node_sort_key(node: dict[str, Any]) -> tuple[Any, ...]:
    state = node["state"]
    return (node["start"], node["end"], state["agent"], state["action"],
            state["context"], tuple(state["roles"]))


def _span_credit(a: dict[str, Any], b: dict[str, Any]) -> float:
    inter = max(0, min(a["end"], b["end"]) - max(a["start"], b["start"]) + 1)
    union = max(a["end"], b["end"]) - min(a["start"], b["start"]) + 1
    iou = inter / union
    boundary = max(0.0, 1.0 - (abs(a["start"] - b["start"]) + abs(a["end"] - b["end"])) / 8.0)
    return float(max(iou, boundary))


def _set_f1(a: list[str], b: list[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    tp = len(sa & sb)
    return 2.0 * tp / (len(sa) + len(sb))


def _tuple_credit(a: dict[str, Any], b: dict[str, Any]) -> float:
    sa, sb = a["state"], b["state"]
    return float(0.20 * (sa["agent"] == sb["agent"]) +
                 0.35 * (sa["action"] == sb["action"]) +
                 0.25 * (sa["context"] == sb["context"]) +
                 0.20 * _set_f1(sa["roles"], sb["roles"]))


def _assignment(pred: list[dict[str, Any]], true: list[dict[str, Any]]) -> list[tuple[int, int]]:
    if not pred or not true:
        return []
    weights = np.zeros((len(pred), len(true)), dtype=np.float64)
    for i, pn in enumerate(pred):
        for j, tn in enumerate(true):
            weights[i, j] = 0.55 * _span_credit(pn, tn) + 0.45 * _tuple_credit(pn, tn)
    try:
        from scipy.optimize import linear_sum_assignment
        rows, cols = linear_sum_assignment(weights, maximize=True)
        return list(zip(rows.tolist(), cols.tolist()))
    except (ImportError, TypeError):
        # Deterministic bounded fallback; SciPy is preferred and used by the platform image.
        candidates = sorted(((-weights[i, j], i, j) for i in range(len(pred)) for j in range(len(true))))
        used_i: set[int] = set()
        used_j: set[int] = set()
        out = []
        for _, i, j in candidates:
            if i not in used_i and j not in used_j:
                used_i.add(i); used_j.add(j); out.append((i, j))
        return out


def _state_token(node: dict[str, Any]) -> tuple[Any, ...]:
    state = node["state"]
    return (state["agent"], state["action"], state["context"], tuple(state["roles"]))


def _edit_similarity(a: list[tuple[Any, ...]], b: list[tuple[Any, ...]]) -> float:
    if not a and not b:
        return 1.0
    prev = list(range(len(b) + 1))
    for i, av in enumerate(a, 1):
        cur = [i]
        for j, bv in enumerate(b, 1):
            cur.append(min(cur[-1] + 1, prev[j] + 1, prev[j - 1] + (av != bv)))
        prev = cur
    return float(1.0 - prev[-1] / max(len(a), len(b), 1))


def _edge_f1(pred_edges: list[dict[str, Any]], true_edges: list[dict[str, Any]],
             node_map: dict[int, int]) -> float:
    true_set = {(e["from"], e["to"], e["type"]) for e in true_edges}
    pred_set = set()
    for edge in pred_edges:
        if edge["from"] in node_map and edge["to"] in node_map:
            src, dst = node_map[edge["from"]], node_map[edge["to"]]
            if src < dst:
                pred_set.add((src, dst, edge["type"]))
    if not pred_set and not true_set:
        return 1.0
    if not pred_set or not true_set:
        return 0.0
    tp = len(pred_set & true_set)
    return float(2.0 * tp / (len(pred_set) + len(true_set)))


def _count_credit(pred_count: int, true_count: int) -> float:
    if pred_count == true_count == 0:
        return 1.0
    return float(max(0.0, 1.0 - abs(pred_count - true_count) / max(pred_count, true_count, 1)))


def _graph_score(pred: dict[str, Any], true: dict[str, Any]) -> float:
    pnodes, tnodes = pred["nodes"], true["nodes"]
    if not pnodes and not tnodes:
        return 1.0
    if not pnodes or not tnodes:
        return 0.0

    pairs = _assignment(pnodes, tnodes)
    denom = max(len(pnodes), len(tnodes), 1)
    temporal = sum(_span_credit(pnodes[i], tnodes[j]) for i, j in pairs) / denom

    exact_matches = 0
    node_map: dict[int, int] = {}
    for i, j in pairs:
        span = _span_credit(pnodes[i], tnodes[j])
        tuple_credit = _tuple_credit(pnodes[i], tnodes[j])
        if span >= 0.25 and tuple_credit >= 0.50:
            node_map[i] = j
        if span >= 0.25 and _state_token(pnodes[i]) == _state_token(tnodes[j]):
            exact_matches += 1
    state_f1 = 2.0 * exact_matches / (len(pnodes) + len(tnodes))
    sequence = _edit_similarity([_state_token(n) for n in pnodes], [_state_token(n) for n in tnodes])
    edge = _edge_f1(pred["edges"], true["edges"], node_map)
    completeness = 0.65 * _count_credit(len(pnodes), len(tnodes)) + 0.35 * _count_credit(len(pred["edges"]), len(true["edges"]))

    core = 0.28 * temporal + 0.27 * state_f1 + 0.17 * sequence + 0.20 * edge + 0.08 * completeness
    joint = (max(0.0, temporal) * max(0.0, state_f1) * max(0.0, sequence) * max(0.0, edge)) ** 0.25
    return float(np.clip(0.65 * core + 0.35 * joint, 0.0, 1.0))


def _main() -> int:
    import sys
    if len(sys.argv) != 3:
        print("Usage: python grade.py submission.csv answers.csv", file=sys.stderr)
        return 2
    try:
        sub = pd.read_csv(sys.argv[1])
        ans = pd.read_csv(sys.argv[2])
        print(f"{grade(sub, ans):.12f}")
        return 0
    except (FileNotFoundError, pd.errors.ParserError, UnicodeError, InvalidSubmissionError) as exc:
        message = str(exc) if isinstance(exc, InvalidSubmissionError) else "Could not read the required CSV input."
        print(f"InvalidSubmissionError: {message}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(_main())

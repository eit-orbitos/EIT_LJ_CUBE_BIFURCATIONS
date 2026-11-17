"""Independent structural validation of the three machine-readable proof dependency graphs (read-only).

Usage:  python scripts/validate_dependency_graphs.py [project root] [--json=<out>]     (exit 0 = all checks pass)

For data/A2_theorem_A_dependencies.json (Theorem A), data/B2_4_dependency_graph.json (Proposition B2) and
data/B2_5_dependency_graph.json (Proposition B3, Corollary B3'): no cycles; no dangling dependency; every node reachable
from a root; every proof leaf classified as VERIFIED-EXACT, CERTIFIED, FROZEN INPUT or STANDARD, or (IN_proposition_B2 only)
as an ESTABLISHED IN-PAPER RESULT whose own graph (B2.4) must validate; no node with a
numerical status (VERIFIED-NUMERIC or similar) reachable from a root; corroboration-only / consistency-only items not
reachable as proof dependencies; FROZEN INPUT leaves listed (Paper 2). The graphs themselves are not modified.
"""
import json
import pathlib
import sys

LEAF_CLASSES = {"VERIFIED-EXACT", "CERTIFIED", "FROZEN INPUT", "STANDARD", "ESTABLISHED IN-PAPER RESULT"}
# Inputs of one graph that are the root of another in-paper graph. They are not atomic proof leaves: they are
# accepted only if the referenced graph itself validates (checked in run()). The proof graphs are not modified.
IN_PAPER_INPUTS = {"IN_proposition_B2": ("Proposition B2 (data/B2_4_dependency_graph.json)", "P_B2")}


def analyse(name, nodes, edges, roots, side_ids, frozen_label=lambda n: None):
    """nodes: id -> status ; edges: list (a, b) meaning a uses b ; roots: list ; side_ids: corroboration/consistency."""
    out = {"graph": name, "n_nodes": len(nodes), "n_edges": len(edges), "roots": roots, "failures": []}
    adj = {k: [] for k in nodes}
    for a, b in edges:
        if a not in nodes or b not in nodes:
            out["failures"].append(f"dangling edge {a} -> {b}")
            continue
        adj[a].append(b)
    for r in roots:
        if r not in nodes:
            out["failures"].append(f"missing root {r}")
    # cycle detection (iterative DFS colouring)
    colour = {k: 0 for k in nodes}
    def dfs(s):
        stack = [(s, iter(adj[s]))]
        colour[s] = 1
        while stack:
            v, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                colour[v] = 2
                stack.pop()
            elif colour[nxt] == 1:
                out["failures"].append(f"cycle through {v} -> {nxt}")
            elif colour[nxt] == 0:
                colour[nxt] = 1
                stack.append((nxt, iter(adj[nxt])))
    for k in nodes:
        if colour[k] == 0:
            dfs(k)
    reach = set()
    todo = [r for r in roots if r in nodes]
    while todo:
        v = todo.pop()
        if v in reach:
            continue
        reach.add(v)
        todo.extend(adj[v])
    unreachable = sorted(set(nodes) - reach)
    if unreachable:
        out["failures"].append(f"nodes not reachable from a root: {unreachable}")
    leaves = sorted(v for v in reach if not adj[v])
    out["leaves"] = {v: nodes[v] for v in leaves}
    for v in leaves:
        if nodes[v] not in LEAF_CLASSES:
            out["failures"].append(f"unclassified proof leaf {v}: {nodes[v]!r}")
    for v in reach:
        if nodes[v] and "NUMERIC" in str(nodes[v]).upper():
            out["failures"].append(f"numerical node reachable as proof dependency: {v}")
    for s in side_ids:
        if s in reach:
            out["failures"].append(f"corroboration/consistency item reachable as proof dependency: {s}")
    out["side_items_not_reachable"] = sorted(side_ids)
    out["frozen_inputs"] = sorted(v for v in leaves if nodes[v] == "FROZEN INPUT")
    out["leaf_class_counts"] = {c: sum(1 for v in leaves if nodes[v] == c) for c in sorted(LEAF_CLASSES)}
    out["acyclic"] = not any(f.startswith("cycle") for f in out["failures"])
    out["pass"] = not out["failures"]
    return out


def run(root):
    D = pathlib.Path(root) / "data"
    res = []
    a = json.loads((D / "A2_theorem_A_dependencies.json").read_text(encoding="utf-8"))
    g = a["graph"]
    nodes = {k: v.get("status") if "uses" not in v or k == "Theorem A" or v.get("status") else None
             for k, v in g.items()}
    nodes = {k: (v.get("status") or "INTERMEDIATE") for k, v in g.items()}
    edges = [(k, u) for k, v in g.items() for u in v.get("uses", [])]
    side = sorted({c for v in g.values() for c in v.get("corroboration", [])})
    r = analyse("Theorem A (data/A2_theorem_A_dependencies.json)", nodes, edges, ["Theorem A"], [])
    r["corroboration_items_outside_graph"] = [c for c in side if c in g]
    if r["corroboration_items_outside_graph"]:
        r["failures"].append("corroboration item is a graph node"); r["pass"] = False
    r["declared_leaf_statuses"] = a.get("leaf_statuses")
    res.append(r)
    b = json.loads((D / "B2_4_dependency_graph.json").read_text(encoding="utf-8"))["graph"]
    nodes = {n["id"]: n["status"] for n in b["nodes"]}
    for n in b["nodes"]:
        if n["role"] in ("proposition", "step") and n["status"] != "VERIFIED-EXACT":
            nodes[n["id"]] = "INTERMEDIATE:" + n["status"]
    side = [c["id"] if isinstance(c, dict) else c for c in b.get("corroboration_only", [])]
    r = analyse("Proposition B2 (data/B2_4_dependency_graph.json)", nodes, [tuple(e) for e in b["edges"]],
                [b["root"]], side)
    inputs = sorted(n["id"] for n in b["nodes"] if n["role"] == "input")
    if sorted(b["allowed_inputs"]) != inputs:
        r["failures"].append(f"allowed_inputs {b['allowed_inputs']} != input nodes {inputs}"); r["pass"] = False
    res.append(r)
    c = json.loads((D / "B2_5_dependency_graph.json").read_text(encoding="utf-8"))
    nodes = {n["id"]: n["status"] for n in c["nodes"]}
    in_paper = {}
    for n in c["nodes"]:
        if n["role"] == "input" and n["id"] in IN_PAPER_INPUTS and str(n["status"]).startswith("PROVED"):
            in_paper[n["id"]] = n["status"]
            nodes[n["id"]] = "ESTABLISHED IN-PAPER RESULT"
    for n in c["nodes"]:
        if n["role"] in ("proposition", "corollary"):
            nodes[n["id"]] = "INTERMEDIATE:" + n["status"]
    side = [x["id"] for x in c.get("corroboration_only", [])] + [x["id"] for x in c.get("consistency_only", [])]
    r = analyse("Proposition B3 / Corollary B3' (data/B2_5_dependency_graph.json)", nodes,
                [tuple(e) for e in c["edges"]], sorted(c["roots"]), side)
    # declared root -> leaf sets must equal the computed reachable leaves
    adj = {}
    for x, y in c["edges"]:
        adj.setdefault(x, []).append(y)
    for root, declared in c["roots"].items():
        seen, todo = set(), [root]
        while todo:
            v = todo.pop()
            if v not in seen:
                seen.add(v); todo.extend(adj.get(v, []))
        got = sorted(v for v in seen if v not in adj)
        if got != sorted(declared):
            r["failures"].append(f"declared leaves of {root} {sorted(declared)} != computed {got}"); r["pass"] = False
    r["in_paper_inputs"] = {}
    for k, st in in_paper.items():
        gname, groot = IN_PAPER_INPUTS[k]
        ref = next((x for x in res if x["graph"] == gname), None)
        ok = ref is not None and ref["pass"] and groot in ref["roots"]
        r["in_paper_inputs"][k] = {"recorded_status": st, "validated_by_graph": gname, "graph_root": groot, "ok": ok}
        if not ok:
            r["failures"].append(f"in-paper input {k} not backed by a passing graph {gname}"); r["pass"] = False
    res.append(r)
    return {"pass": all(x["pass"] for x in res), "graphs": res}


def main(argv):
    args = [x for x in argv[1:] if not x.startswith("--")]
    opts = dict(x.split("=", 1) for x in argv[1:] if x.startswith("--") and "=" in x)
    root = args[0] if args else str(pathlib.Path(__file__).resolve().parents[1])
    res = run(root)
    if "--json" in opts:
        pathlib.Path(opts["--json"]).write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    for g in res["graphs"]:
        print(("PASS " if g["pass"] else "FAIL ") + g["graph"], f"nodes={g['n_nodes']} edges={g['n_edges']}",
              f"acyclic={g['acyclic']} leaves={g['leaf_class_counts']} frozen={g['frozen_inputs']}")
        for f in g["failures"]:
            print("   -", f)
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

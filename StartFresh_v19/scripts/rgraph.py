#!/usr/bin/env python3
"""Reasoning graph: what was tried, what died and why (PROOFER.md §6).

One append-only JSONL file per target: <graphs>/<target>.jsonl. Events:
  node  {key, type, text, by, run, pred}      type: question|hypothesis|experiment|result|dead|lead|tool|fact
  edge  {src, dst, rel}                       rel: derives|tests|supports|refutes|blocks|resumes
  kill  {key, why}                            the line is dead; `why` is the reusable lesson
  revive{key, why}                            a dead line reopened, with the new reason
  close {key, why}                            a lead finished (not dead): drops out of "live leads"
Nothing is edited in place; the current graph is the fold of all events.

Usage (graphs dir = $PROOFER_GRAPHS or <script>/../graphs):
  rgraph.py add <target> <type> <key> "<text>" [--parent KEY --rel derives] [--by LENS] [--run RUN] [--pred PID]
  rgraph.py link <target> <src> <dst> <rel>
  rgraph.py kill <target> <key> "<why>"
  rgraph.py revive <target> <key> "<why>"
  rgraph.py close <target> <key> "<outcome>"
  rgraph.py check <target> "<idea text>"     exit 2 if a DEAD line is a near-duplicate (do not repeat it)
  rgraph.py show <target>                    compact agent-readable state: live leads, dead ends + why
  rgraph.py canvas <target> <out.canvas>     Obsidian canvas for the human
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

GRAPHS = Path(os.environ.get("PROOFER_GRAPHS", Path(__file__).resolve().parent.parent / "graphs"))
STOP = set("a an the of to in on for and or with by from is are be at as it this that via using use".split())
COLORS = {"dead": "1", "lead": "4", "result": "4", "hypothesis": "6", "experiment": "3", "question": "5", "fact": "2"}


def now():
    return subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%MZ"], capture_output=True, text=True).stdout.strip()


def path(target):
    if not re.fullmatch(r"[A-Za-z0-9._-]+", target):
        sys.exit("target must be a bank id")
    GRAPHS.mkdir(parents=True, exist_ok=True)
    return GRAPHS / f"{target}.jsonl"


def emit(target, ev):
    ev["ts"] = now()
    with open(path(target), "a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")


def fold(target):
    nodes, edges = {}, []
    p = path(target)
    if not p.exists():
        return nodes, edges
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        k = e.get("ev")
        if k == "node":
            nodes[e["key"]] = {**e, "dead": e["type"] == "dead", "why": "", "closed": ""}
        elif k == "edge":
            edges.append(e)
        elif k == "kill" and e["key"] in nodes:
            nodes[e["key"]].update(dead=True, why=e["why"], killed=e["ts"])
        elif k == "close" and e["key"] in nodes:
            nodes[e["key"]]["closed"] = e["why"]
        elif k == "revive" and e["key"] in nodes:
            nodes[e["key"]].update(dead=False, why="revived: " + e["why"])
    return nodes, edges


def toks(s):
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP and len(w) > 1}


def sim(a, b):
    ta, tb = toks(a), toks(b)
    return len(ta & tb) / len(ta | tb) if ta and tb else 0.0


def cmd_add(a):
    nodes, _ = fold(a.target)
    if a.key in nodes:
        sys.exit(f"key {a.key} exists; pick a new key (graph is append-only)")
    emit(a.target, {"ev": "node", "key": a.key, "type": a.type, "text": a.text,
                    "by": a.by, "run": a.run, "pred": a.pred})
    if a.parent:
        emit(a.target, {"ev": "edge", "src": a.parent, "dst": a.key, "rel": a.rel})
    print(f"+ {a.key}")


def cmd_check(a):
    nodes, _ = fold(a.target)
    hits = sorted(((sim(a.text, n["text"] + " " + n["why"]), n) for n in nodes.values()),
                  key=lambda x: -x[0])
    hits = [(s, n) for s, n in hits if s >= a.threshold]
    for s, n in hits[:8]:
        tag = "DEAD" if n["dead"] else n["type"]
        print(f"{s:.2f}  [{tag}] {n['key']}: {n['text']}" + (f"  — why dead: {n['why']}" if n["dead"] else ""))
    if any(n["dead"] for _, n in hits):
        print("RGRAPH_CHECK: DEAD_NEAR_DUPLICATE — do not repeat; change the idea or `revive` with a new reason")
        sys.exit(2)
    print("RGRAPH_CHECK: CLEAR")


def cmd_show(a):
    nodes, edges = fold(a.target)
    kids = {}
    for e in edges:
        kids.setdefault(e["src"], []).append((e["rel"], e["dst"]))
    has_parent = {e["dst"] for e in edges}
    print(f"# {a.target}: {len(nodes)} nodes, {sum(n['dead'] for n in nodes.values())} dead")

    def walk(k, depth, seen):
        if k in seen or k not in nodes:
            return
        seen.add(k)
        n = nodes[k]
        mark = "✗" if n["dead"] else "✓" if n["closed"] else {"lead": "→", "result": "✓"}.get(n["type"], "·")
        why = f"  ✗ {n['why']}" if n["dead"] and n["why"] else ""
        by = f" ({n['by']})" if n.get("by") else ""
        print(f"{'  ' * depth}{mark} {k} [{n['type']}]{by}: {n['text']}{why}")
        for rel, d in kids.get(k, []):
            print(f"{'  ' * (depth + 1)}<{rel}>")
            walk(d, depth + 2, seen)

    seen = set()
    for k in nodes:
        if k not in has_parent:
            walk(k, 0, seen)
    live = [n for n in nodes.values() if n["type"] == "lead" and not n["dead"] and not n["closed"]]
    print("\n## Live leads")
    for n in live:
        print(f"- {n['key']}: {n['text']}")
    print("\n## Dead ends (lessons)")
    for n in nodes.values():
        if n["dead"]:
            print(f"- {n['key']}: {n['text']} — {n['why']}")
    mb = Path(__file__).resolve().parent / "micro_bet.py"
    if mb.exists():
        print()
        r = subprocess.run([sys.executable, str(mb), "status", a.target], capture_output=True, text=True)
        if r.stdout.strip():
            print(r.stdout.strip())


def cmd_canvas(a):
    nodes, edges = fold(a.target)
    order = list(nodes)
    depth = {k: 0 for k in order}
    for _ in range(len(order)):
        for e in edges:
            if e["src"] in depth and e["dst"] in depth:
                depth[e["dst"]] = max(depth[e["dst"]], depth[e["src"]] + 1)
    col = {}
    cn = []
    for k in order:
        d = depth[k]
        row = col.get(d, 0)
        col[d] = row + 1
        n = nodes[k]
        label = ("✗ " if n["dead"] else "") + f"**{k}** · {n['type']}\n\n{n['text']}"
        if n["dead"] and n["why"]:
            label += f"\n\n*why dead:* {n['why']}"
        cn.append({"id": k, "type": "text", "text": label, "x": d * 420, "y": row * 220,
                   "width": 380, "height": 190, "color": "1" if n["dead"] else COLORS.get(n["type"], "0")})
    ce = [{"id": f"e{i}", "fromNode": e["src"], "toNode": e["dst"], "fromSide": "right", "toSide": "left",
           "label": e["rel"]} for i, e in enumerate(edges) if e["src"] in nodes and e["dst"] in nodes]
    Path(a.out).write_text(json.dumps({"nodes": cn, "edges": ce}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {a.out}: {len(cn)} nodes, {len(ce)} edges")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("add")
    p.add_argument("target"); p.add_argument("type", choices=list(COLORS) + ["tool"])
    p.add_argument("key"); p.add_argument("text")
    p.add_argument("--parent"); p.add_argument("--rel", default="derives")
    p.add_argument("--by", default=""); p.add_argument("--run", default=""); p.add_argument("--pred", default="")
    p.set_defaults(f=cmd_add)
    p = sp.add_parser("link"); p.add_argument("target"); p.add_argument("src"); p.add_argument("dst"); p.add_argument("rel")
    p.set_defaults(f=lambda a: (emit(a.target, {"ev": "edge", "src": a.src, "dst": a.dst, "rel": a.rel}), print("linked")))
    for name in ("kill", "revive", "close"):
        p = sp.add_parser(name); p.add_argument("target"); p.add_argument("key"); p.add_argument("why")
        p.set_defaults(f=lambda a, name=name: (emit(a.target, {"ev": name, "key": a.key, "why": a.why}), print(f"{name} {a.key}")))
    p = sp.add_parser("check"); p.add_argument("target"); p.add_argument("text")
    p.add_argument("--threshold", type=float, default=0.3); p.set_defaults(f=cmd_check)
    p = sp.add_parser("show"); p.add_argument("target"); p.set_defaults(f=cmd_show)
    p = sp.add_parser("canvas"); p.add_argument("target"); p.add_argument("out"); p.set_defaults(f=cmd_canvas)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()

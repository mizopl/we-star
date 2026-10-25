#!/usr/bin/env python3
"""Federated Per-Target Micro-Bet & M1-M6 Meta-Heuristic Engine (PROOFER v15/v16).

Why this exists:
  - Global `postdict.py` (`memory/predictions.tsv`) tracks macro campaign/PR bets (`P00xx`).
  - Specialist worker threads (e.g. AME C++ search, Vesuvius 3D scroll lab, FMM tensor lab)
    run rapid 10-30 min micro-experiments. Writing all of them to `memory/predictions.tsv`
    causes ID race conditions and granularity pollution; writing none of them causes
    "Lab-Rat Tunneling" (spinning the same failed ansatz for hours without a structural pivot).
  - `micro_bet.py` gives each target thread its own isolated ledger
    `memory/local_bets/<target>.tsv` (`L-<TAG>-001`, ...) AND automatically synchronizes
    every micro-bet (`predict` / `resolve`) with the target's reasoning graph
    `graphs/<target>.jsonl` + `.canvas`, while enforcing Meta-Heuristics M1-M6.

Usage:
  micro_bet.py predict <target> <node_key> <p> "<hypothesis text>" [--parent KEY] [--by LENS]
  micro_bet.py resolve <target> <lid_or_key> <0|1> "<why / lesson>"
  micro_bet.py status  [<target>]
"""
import argparse
import csv
import os
import re
import subprocess
import sys
from pathlib import Path

KB = Path(os.environ.get("PROOFER_HOME", Path(__file__).resolve().parent.parent))
LOCAL_DIR = KB / "memory" / "local_bets"
RGRAPH = Path(__file__).resolve().parent / "rgraph.py"
PYTHON = "/opt/homebrew/bin/python3" if Path("/opt/homebrew/bin/python3").exists() else sys.executable
COLS = ["ts", "kind", "id", "target", "node_key", "p", "outcome", "text"]


def now():
    return subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%MZ"], capture_output=True, text=True).stdout.strip()


def tag_for(target: str) -> str:
    parts = [p for p in re.split(r"[^A-Za-z0-9]+", target) if p]
    if not parts:
        return "LOC"
    if len(parts) == 1:
        return parts[0][:4].upper()
    return "".join(p[0] for p in parts[:4]).upper()


def ledger_path(target: str) -> Path:
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    return LOCAL_DIR / f"{target}.tsv"


def load(target: str):
    p = ledger_path(target)
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def append(target: str, row: dict):
    p = ledger_path(target)
    new = not p.exists()
    with open(p, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, COLS, delimiter="\t")
        if new:
            w.writeheader()
        w.writerow(row)


def refresh_canvas(target: str):
    graphs_dir = Path(os.environ.get("PROOFER_GRAPHS", KB / "graphs"))
    canvas_file = graphs_dir / f"{target}.canvas"
    subprocess.run([PYTHON, str(RGRAPH), "canvas", target, str(canvas_file)], capture_output=True, text=True)


def print_meta_compass(target: str, rows: list):
    preds = {r["id"]: r for r in rows if r["kind"] == "predict"}
    res_rows = [r for r in rows if r["kind"] == "resolve" and r["id"] in preds]
    pairs = [(preds[r["id"]], int(r["outcome"])) for r in res_rows]
    brier = sum((float(p["p"]) - o) ** 2 for p, o in pairs) / len(pairs) if pairs else float("nan")

    # Count trailing failures (consecutive 0s at the end of resolved list)
    streak_zero = 0
    for r in reversed(res_rows):
        if int(r["outcome"]) == 0:
            streak_zero += 1
        else:
            break

    print(f"=== [FEDERATED M1-M6 COMPASS | target={target}] ===")
    print(f"  Local micro-bets: {len(preds)} total | {len(pairs)} resolved | Local Brier: {brier:.3f} | Failure streak: {streak_zero}")
    if streak_zero >= 2:
        print("  🚨 [M2 STRUCTURAL PIVOT TRIGGERED]: 2+ consecutive local micro-bets failed (0)!")
        print("     -> STOP tuning seeds/hyperparameters on the current ansatz.")
        print("     -> PIVOT representation: switch to symmetry/canonical basis, block decomposition, or exact SAT/ILP/LUT solver (M1).")
    else:
        print("  🧭 Active Laws: M1 (Exact Solver First) | M2 (Pivot after 2 failed shots) | M4 (p <= 0.65 on 1st shot) | M6 (Auto-sync graph)")


def cmd_predict(a):
    p = float(a.p)
    if not 0.0 <= p <= 1.0:
        sys.exit("p must be in [0, 1]")
    rows = load(a.target)
    preds = [r for r in rows if r["kind"] == "predict"]
    lid = f"L-{tag_for(a.target)}-{len(preds) + 1:03d}"

    if p > 0.65 and len(preds) == 0:
        print(f"⚠️  [M4 ANTI-HUBRIS WARNING]: First micro-bet on {a.target} has p={p:.2f} > 0.65. Consider calibrated caution.")

    # Check rgraph for near-duplicate dead ends first
    chk = subprocess.run([PYTHON, str(RGRAPH), "check", a.target, a.text], capture_output=True, text=True)
    if chk.returncode == 2:
        print(f"⚠️  [K6 GRAPH DUPLICATE WARNING]: {chk.stdout.strip()}")

    append(a.target, {
        "ts": now(),
        "kind": "predict",
        "id": lid,
        "target": a.target,
        "node_key": a.node_key,
        "p": f"{p:.2f}",
        "outcome": "",
        "text": a.text,
    })

    # Sync node into graphs/<target>.jsonl
    cmd = [PYTHON, str(RGRAPH), "add", a.target, "hypothesis", a.node_key, a.text, "--by", a.by, "--pred", lid]
    if a.parent:
        cmd += ["--parent", a.parent, "--rel", "derives"]
    subprocess.run(cmd, capture_output=True, text=True)
    refresh_canvas(a.target)

    print(f"✅ Registered local micro-bet {lid} (node={a.node_key}, p={p:.2f}) -> graphs/{a.target}.jsonl")
    print_meta_compass(a.target, load(a.target))


def cmd_resolve(a):
    if a.outcome not in ("0", "1"):
        sys.exit("outcome must be 0 or 1")
    rows = load(a.target)
    preds = {r["id"]: r for r in rows if r["kind"] == "predict"}
    by_key = {r["node_key"]: r for r in rows if r["kind"] == "predict"}

    pred = preds.get(a.lid) or by_key.get(a.lid)
    if not pred:
        sys.exit(f"Unknown local micro-bet or node_key: {a.lid}")
    lid = pred["id"]
    nkey = pred["node_key"]

    if any(r["kind"] == "resolve" and r["id"] == lid for r in rows):
        sys.exit(f"{lid} already resolved; ledger is append-only")

    append(a.target, {
        "ts": now(),
        "kind": "resolve",
        "id": lid,
        "target": a.target,
        "node_key": nkey,
        "p": pred["p"],
        "outcome": a.outcome,
        "text": a.why,
    })

    # Sync close (1) or kill (0) into graphs/<target>.jsonl
    action = "close" if a.outcome == "1" else "kill"
    subprocess.run([PYTHON, str(RGRAPH), action, a.target, nkey, f"[{lid}={a.outcome}] {a.why}"], capture_output=True, text=True)
    refresh_canvas(a.target)

    b = (float(pred["p"]) - int(a.outcome)) ** 2
    print(f"✅ Resolved {lid} (node={nkey}) -> outcome={a.outcome} (brier={b:.3f}); graph node marked '{action}'")
    print_meta_compass(a.target, load(a.target))


def cmd_status(a):
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    targets = [a.target] if a.target else sorted(p.stem for p in LOCAL_DIR.glob("*.tsv"))
    if not targets:
        print("No local micro-bet ledgers yet.")
        return
    for t in targets:
        rows = load(t)
        print_meta_compass(t, rows)
        preds = {r["id"]: r for r in rows if r["kind"] == "predict"}
        res = {r["id"]: r for r in rows if r["kind"] == "resolve"}
        for pid, pr in preds.items():
            if pid in res:
                rr = res[pid]
                print(f"  [RESOLVED={rr['outcome']}] {pid} ({pr['node_key']}) p={pr['p']} :: {pr['text'][:85]}")
            else:
                print(f"  [OPEN]         {pid} ({pr['node_key']}) p={pr['p']} :: {pr['text'][:85]}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("predict")
    p_add.add_argument("target")
    p_add.add_argument("node_key")
    p_add.add_argument("p")
    p_add.add_argument("text")
    p_add.add_argument("--parent", default="")
    p_add.add_argument("--by", default="worker")
    p_add.set_defaults(fn=cmd_predict)

    p_res = sub.add_parser("resolve")
    p_res.add_argument("target")
    p_res.add_argument("lid")
    p_res.add_argument("outcome")
    p_res.add_argument("why")
    p_res.set_defaults(fn=cmd_resolve)

    p_st = sub.add_parser("status")
    p_st.add_argument("target", nargs="?", default="")
    p_st.set_defaults(fn=cmd_status)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()

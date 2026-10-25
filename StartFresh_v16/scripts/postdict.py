#!/usr/bin/env python3
"""Prediction ledger + postdiction scoring (CONSTITUTION v9 §11.3).

The ledger memory/predictions.tsv is append-only: a prediction row is written
BEFORE the work, a resolve row AFTER. Nothing is ever edited in place.
`report` overwrites wiki/meta/calibration.md with Brier scores and calibration
bins; the agent then overwrites wiki/meta/beliefs.md from it.

Usage:
  postdict.py predict <scope> <p> <text>     -> prints the new prediction id
  postdict.py resolve <id> <0|1> --by commander|skeptic [<note>]
                                             (K3, v10: never from the run that placed the bet;
                                              refused when PROOFER_ROLE=run; judge the literal wording)
  postdict.py report
"""
import csv
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# PROOFER_HOME lets the lab (~/v3r1t4s/proofer) keep its own ledger outside Desktop.
KB = Path(os.environ.get("PROOFER_HOME", Path(__file__).resolve().parent.parent))
LEDGER = KB / "memory" / "predictions.tsv"
REPORT = KB / "wiki" / "meta" / "calibration.md"
COLS = ["ts", "kind", "id", "scope", "p", "outcome", "text"]


def now():
    # From the system clock, never typed by hand (V3R1T4S rule 1).
    return subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%MZ"], capture_output=True, text=True).stdout.strip()


def load():
    if not LEDGER.exists():
        return []
    with open(LEDGER, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def append(row):
    new = not LEDGER.exists()
    LEDGER.parent.mkdir(exist_ok=True)
    with open(LEDGER, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, COLS, delimiter="\t")
        if new:
            w.writeheader()
        w.writerow(row)


def predict(scope, p, text):
    p = float(p)
    if not 0.0 <= p <= 1.0:
        sys.exit("p must be in [0, 1]")
    rows = load()
    pid = f"P{sum(r['kind'] == 'predict' for r in rows) + 1:04d}"
    append({"ts": now(), "kind": "predict", "id": pid, "scope": scope, "p": p, "outcome": "", "text": text})
    print(pid)


def resolve(pid, outcome, by, note=""):
    if os.environ.get("PROOFER_ROLE") == "run":
        sys.exit("K3: a run places bets but never resolves them; the commander or a fresh skeptic does")
    if by not in ("commander", "skeptic"):
        sys.exit("K3: --by commander|skeptic is required")
    note = f"by={by}; {note}"
    rows = load()
    preds = {r["id"]: r for r in rows if r["kind"] == "predict"}
    if pid not in preds:
        sys.exit(f"unknown prediction {pid}")
    if any(r["kind"] == "resolve" and r["id"] == pid for r in rows):
        sys.exit(f"{pid} already resolved; the ledger is append-only")
    if outcome not in ("0", "1"):
        sys.exit("outcome must be 0 or 1")
    append({"ts": now(), "kind": "resolve", "id": pid, "scope": preds[pid]["scope"],
            "p": preds[pid]["p"], "outcome": outcome, "text": note})
    b = (float(preds[pid]["p"]) - int(outcome)) ** 2
    print(f"{pid} resolved {outcome}; brier {b:.3f}")


def report():
    rows = load()
    preds = {r["id"]: r for r in rows if r["kind"] == "predict"}
    res = [(preds[r["id"]], int(r["outcome"])) for r in rows if r["kind"] == "resolve" and r["id"] in preds]
    open_ = [p for i, p in preds.items() if i not in {r["id"] for r in rows if r["kind"] == "resolve"}]

    def brier(pairs):
        return sum((float(p["p"]) - o) ** 2 for p, o in pairs) / len(pairs) if pairs else float("nan")

    scopes = {}
    for p, o in res:
        raw_sc = p["scope"]
        if len(raw_sc) > 40:
            raw_sc = "panel" if "panel" in raw_sc.lower() else ("optimization-benchmarks" if "ihtp" in raw_sc.lower() else "target")
        scopes.setdefault(raw_sc.split("/")[0].split(":")[0], []).append((p, o))
    bins = {}
    for p, o in res:
        b = min(int(float(p["p"]) * 5), 4)
        bins.setdefault(b, []).append((float(p["p"]), o))

    out = [
        "# Calibration (generated — overwritten by scripts/postdict.py report)",
        "",
        f"*Generated:* {now()} · resolved {len(res)} · open {len(open_)} · "
        f"Brier {brier(res):.3f} (0 = perfect, 0.25 = coin flip at p=0.5)",
        "",
        "## By scope",
        "",
        "| Scope | n | Brier | mean p | hit rate |",
        "|---|---|---|---|---|",
    ]
    for s, pairs in sorted(scopes.items()):
        mp = sum(float(p["p"]) for p, _ in pairs) / len(pairs)
        hr = sum(o for _, o in pairs) / len(pairs)
        out.append(f"| {s} | {len(pairs)} | {brier(pairs):.3f} | {mp:.2f} | {hr:.2f} |")
    out += ["", "## Calibration bins", "", "| p bin | n | mean p | hit rate | verdict |", "|---|---|---|---|---|"]
    for b in sorted(bins):
        xs = bins[b]
        mp = sum(p for p, _ in xs) / len(xs)
        hr = sum(o for _, o in xs) / len(xs)
        verdict = "overconfident" if mp - hr > 0.15 else "underconfident" if hr - mp > 0.15 else "ok"
        out.append(f"| {b/5:.1f}–{(b+1)/5:.1f} | {len(xs)} | {mp:.2f} | {hr:.2f} | {verdict} |")
    out += ["", "## Open predictions", ""]
    out += [f"- `{p['id']}` ({p['scope']}, p={float(p['p']):.2f}) {p['text']}" for p in open_] or ["_(none)_"]
    out.append("")
    REPORT.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {REPORT.relative_to(KB)}: resolved {len(res)}, open {len(open_)}, brier {brier(res):.3f}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["predict"] and len(a) >= 4:
        if "--scope" in a:
            idx = a.index("--scope")
            sc = a[idx + 1]
            rem = [x for i, x in enumerate(a[1:], 1) if i not in (idx, idx + 1) and not x.startswith("--")]
            predict(sc, rem[1], rem[0])
        else:
            predict(a[1], a[2], " ".join(a[3:]))
    elif a[:1] == ["resolve"] and len(a) >= 5 and a[3] == "--by":
        resolve(a[1], a[2], a[4], " ".join(a[5:]))
    elif a[:1] == ["report"]:
        report()
    else:
        sys.exit(__doc__)

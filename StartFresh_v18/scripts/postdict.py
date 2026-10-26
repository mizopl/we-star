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

# PROOFER_HOME lets the lab (PROOFER_HOME) keep its own ledger outside Desktop.
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


def predict(scope, p, text, allow_high_p=False):
    p = float(p)
    if not 0.0 <= p <= 1.0:
        sys.exit("p must be in [0, 1]")
    sc_base = scope.split("/")[0].split(":")[0].lower()
    has_conjunction = any(tok in text for tok in (" and ", " AND ", " & ", "; ")) and sum(
        op in text for op in ("<=", ">=", "<", ">", "==")
    ) >= 2
    if (sc_base in ("exp", "subclaim", "secondary") or has_conjunction) and p > 0.65 and not allow_high_p:
        reason = (
            f"scope='{scope}' (historical scope=exp hit rate is 44.4%)"
            if sc_base in ("exp", "subclaim", "secondary")
            else "compound multi-clause conjunction (H-EVO-01: split A ∧ B into atomic bets)"
        )
        sys.stderr.write(
            f"⚠️  [M4/H-EVO-01 SUB-CLAIM & CONJUNCTION CAP]: Clamping p={p:.2f} -> 0.65 on {reason}. "
            f"Pass --allow-high-p only after Stage I oracle confirmation.\n"
        )
        p = 0.65
    elif p > 0.85 and not allow_high_p:
        sys.stderr.write(
            f"⚠️  [H-EVO-02 BRIER QUADRATIC ASYMMETRY NOTE]: p={p:.2f} > 0.85 incurs Brier={(p)**2:.3f} on miss.\n"
        )
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

    # H-EVO-06: Aggregate federated per-target micro-bet ledgers (memory/local_bets/*.tsv)
    local_dir = KB / "memory" / "local_bets"
    local_files = sorted(local_dir.glob("*.tsv")) if local_dir.exists() else []
    if local_files:
        local_all = []
        local_rows_md = []
        for lf in local_files:
            with open(lf, newline="", encoding="utf-8") as f:
                lrows = list(csv.DictReader(f, delimiter="\t"))
            lpreds = {r["id"]: r for r in lrows if r.get("kind") == "predict"}
            lres = [(float(lpreds[r["id"]]["p"]), int(r["outcome"])) for r in lrows if r.get("kind") == "resolve" and r.get("id") in lpreds]
            lopen = len(lpreds) - len(lres)
            if lres or lopen:
                lb = sum((lp - lo) ** 2 for lp, lo in lres) / len(lres) if lres else float("nan")
                lw = sum(lo for _, lo in lres)
                local_all.extend(lres)
                local_rows_md.append(f"| `{lf.stem}` | {len(lres)} ({lw}W/{len(lres)-lw}L) | {lopen} | {lb:.3f} |")
        if local_all:
            lb_tot = sum((lp - lo) ** 2 for lp, lo in local_all) / len(local_all)
            comb_pairs = [(float(p["p"]), o) for p, o in res] + local_all
            comb_brier = sum((cp - co) ** 2 for cp, co in comb_pairs) / len(comb_pairs)
            out += [
                "",
                f"## Federated Micro-Bets (`memory/local_bets/*.tsv` — H-EVO-06)",
                "",
                f"*Local total:* resolved {len(local_all)} · Local Brier {lb_tot:.3f} · **Combined Global+Local ({len(comb_pairs)} bets) Brier {comb_brier:.4f}**",
                "",
                "| Target | Resolved (W/L) | Open | Local Brier |",
                "|---|---|---|---|",
                *local_rows_md,
            ]

    out.append("")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {REPORT.relative_to(KB)}: resolved {len(res)}, open {len(open_)}, brier {brier(res):.3f}")


if __name__ == "__main__":
    a = sys.argv[1:]
    allow_hp = "--allow-high-p" in a
    a = [x for x in a if x != "--allow-high-p"]
    if a[:1] == ["predict"] and len(a) >= 4:
        if "--scope" in a:
            idx = a.index("--scope")
            sc = a[idx + 1]
            rem = [x for i, x in enumerate(a[1:], 1) if i not in (idx, idx + 1) and not x.startswith("--")]
            predict(sc, rem[1], rem[0], allow_high_p=allow_hp)
        else:
            predict(a[1], a[2], " ".join(a[3:]), allow_high_p=allow_hp)
    elif a[:1] == ["resolve"] and len(a) >= 5 and a[3] == "--by":
        resolve(a[1], a[2], a[4], " ".join(a[5:]))
    elif a[:1] == ["report"]:
        report()
    else:
        sys.exit(__doc__)

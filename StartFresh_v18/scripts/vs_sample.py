#!/usr/bin/env python3
"""Verbalized-sampling picker for hypotheses, lenses or targets (CONSTITUTION v9 §11.2).

Input: a TSV with header  id  typicality  p_success  cost_min  tags  text
  typicality  verbalized probability that a generic agent would propose this line
              (the VS distribution; should sum to ~1 over the file)
  p_success   your guessed chance that the cheapest decisive test survives
  cost_min    guessed minutes for that test
  tags        comma list; use "import" (from outside the field) and "strange"
Picks the top-K by expected value per minute (exploit) plus TAIL draws taken at
random from lines with typicality < 0.10 (explore), using OS entropy. The seed
is printed so the draw can be audited and replayed with --seed.

Usage: python3 scripts/vs_sample.py NOTES_hypotheses.tsv [--top 2] [--tail 1] [--seed N]
"""
import argparse
import csv
import random
import secrets
import sys

TAIL = 0.10


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tsv")
    ap.add_argument("--top", type=int, default=2)
    ap.add_argument("--tail", type=int, default=1)
    ap.add_argument("--seed", type=int)
    a = ap.parse_args()

    with open(a.tsv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    errs = []
    for r in rows:
        try:
            r["typicality"], r["p_success"], r["cost_min"] = (
                float(r["typicality"]), float(r["p_success"]), float(r["cost_min"]))
        except (KeyError, ValueError):
            errs.append(f"bad numbers in row {r.get('id')}")
        r["tagset"] = {t.strip() for t in (r.get("tags") or "").split(",") if t.strip()}
    if errs:
        sys.exit("\n".join(errs))

    total = sum(r["typicality"] for r in rows)
    tail = [r for r in rows if r["typicality"] < TAIL]
    checks = [
        (len(rows) >= 8, f"need >= 8 hypotheses, have {len(rows)}"),
        (len(tail) >= 2, f"need >= 2 tail lines (typicality < {TAIL}), have {len(tail)}"),
        (sum("import" in r["tagset"] for r in rows) >= 2, "need >= 2 lines tagged import"),
        (sum("strange" in r["tagset"] for r in rows) >= 1, "need >= 1 line tagged strange"),
        (0.8 <= total <= 1.2, f"typicality should sum to ~1, sums to {total:.2f}"),
    ]
    bad = [msg for ok, msg in checks if not ok]
    if bad:
        sys.exit("VS_SAMPLE: FAIL\n- " + "\n- ".join(bad))

    seed = a.seed if a.seed is not None else secrets.randbits(32)
    rng = random.Random(seed)
    ev = sorted(rows, key=lambda r: r["p_success"] / max(r["cost_min"], 1.0), reverse=True)
    picked = ev[:a.top]
    pool = [r for r in tail if r not in picked]
    for _ in range(min(a.tail, len(pool))):
        r = rng.choices(pool, weights=[max(x["p_success"], 0.01) for x in pool])[0]
        pool.remove(r)
        picked.append(r)

    print(f"seed: {seed}")
    for r in picked:
        role = "tail" if r["typicality"] < TAIL and r not in ev[:a.top] else "top-ev"
        print(f"{role}\t{r['id']}\tp={r['p_success']:.2f}\tcost={r['cost_min']:.0f}m\t"
              f"typ={r['typicality']:.2f}\t{r['text']}")
    print("VS_SAMPLE: PASS")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Cold-verifiable standalone exact oracle for C4-free subgraphs of hypercubes Q_n (n=4..8).

Checks:
  1. Valid hypercube edges (0 <= u < v < 2^n, popcount(u ^ v) == 1, no duplicates).
  2. Exact C4-freeness via BOTH square enumeration AND common-neighbor counting (dual independent check).
  3. Exact structural invariants: degree histogram, parity-split profiles (P0, P1),
     square-edge counts (n0, n1, n2_opp, n2_adj, n3, n4), dimension profile, inclusion maximality,
     and the exact Empty-Square Forcing Identity:
         n2_opp - n0 == (n - 1) * |E| - C(n, 2) * 2^(n - 2) - sum_v C(d(v), 2).
  4. Built-in `--corrupt` negative self-test that flips 1 edge to inject a C4 (or duplicate/invalid edge)
     and exits with code 1.

Usage:
  /opt/homebrew/bin/python3 workspace/q8_c4_extremal/verify.py [edges_file] [--n 8] [--min-edges 682] [--corrupt] [--json]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path


def load_edges(path: Path, n: int) -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    n_verts = 1 << n
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.replace(",", " ").split()
        if len(parts) < 2:
            raise ValueError(f"{path}:{lineno}: malformed edge line {raw!r}")
        u, v = int(parts[0]), int(parts[1])
        if u > v:
            u, v = v, u
        if not (0 <= u < n_verts and 0 <= v < n_verts):
            raise ValueError(f"{path}:{lineno}: vertex out of range for Q_{n}: ({u}, {v})")
        diff = u ^ v
        if diff == 0 or (diff & (diff - 1)) != 0:
            raise ValueError(f"{path}:{lineno}: non-hypercube edge ({u}, {v})")
        if (u, v) in seen:
            raise ValueError(f"{path}:{lineno}: duplicate edge ({u}, {v})")
        seen.add((u, v))
        edges.append((u, v))
    return edges


def analyze_edges(edges: list[tuple[int, int]], n: int) -> dict:
    t0 = time.perf_counter()
    n_verts = 1 << n
    edge_set = set(edges)
    if len(edge_set) != len(edges):
        raise ValueError("Duplicate edges detected")

    # Adjacency bitmasks for independent common-neighbor C4 check
    adj = [0] * n_verts
    deg = [0] * n_verts
    dim_cnt = [0] * n
    for u, v in edges:
        if u >= v:
            raise ValueError(f"Unnormalized edge ({u}, {v})")
        diff = u ^ v
        if diff == 0 or (diff & (diff - 1)) != 0:
            raise ValueError(f"Non-hypercube edge ({u}, {v})")
        d = diff.bit_length() - 1
        adj[u] |= (1 << d)
        adj[v] |= (1 << d)
        deg[u] += 1
        deg[v] += 1
        dim_cnt[d] += 1

    # Method 1: Exhaustive square enumeration across all C(n,2) * 2^(n-2) 4-cycles
    n0 = n1 = n2_opp = n2_adj = n3 = n4 = 0
    for i in range(n):
        bi = 1 << i
        for j in range(i + 1, n):
            bj = 1 << j
            for x in range(n_verts):
                if (x & bi) == 0 and (x & bj) == 0:
                    a = x ^ bi
                    b = x ^ bj
                    c = a ^ bj
                    e_xa = 1 if (adj[x] & bi) else 0
                    e_xb = 1 if (adj[x] & bj) else 0
                    e_ac = 1 if (adj[a] & bj) else 0
                    e_bc = 1 if (adj[b] & bi) else 0
                    s = e_xa + e_xb + e_ac + e_bc
                    if s == 0:
                        n0 += 1
                    elif s == 1:
                        n1 += 1
                    elif s == 2:
                        if (e_xa and e_bc) or (e_xb and e_ac):
                            n2_opp += 1
                        else:
                            n2_adj += 1
                    elif s == 3:
                        n3 += 1
                    else:
                        n4 += 1

    # Method 2: Independent distance-2 common-neighbor C4 count
    c4_common = 0
    for u in range(n_verts):
        au = adj[u]
        for i in range(n):
            if not (au & (1 << i)):
                continue
            for j in range(i + 1, n):
                if not (au & (1 << j)):
                    continue
                w = u ^ (1 << i) ^ (1 << j)
                if (adj[w] & (1 << i)) and (adj[w] & (1 << j)):
                    c4_common += 1
    assert c4_common % 4 == 0
    c4_common //= 4
    assert c4_common == n4, f"Dual C4 check mismatch: {c4_common} vs {n4}"

    # Inclusion maximality check (can any missing hypercube edge be added without creating a C4?)
    addable = 0
    for v in range(n_verts):
        for d in range(n):
            u = v ^ (1 << d)
            if v < u and not (adj[v] & (1 << d)):
                # Adding (v, u) creates a C4 iff some j != d has edges (v, v^j), (u, u^j), (v^j, u^j)
                blocked = False
                for j in range(n):
                    if j == d:
                        continue
                    bj = 1 << j
                    if (adj[v] & bj) and (adj[u] & bj) and (adj[v ^ bj] & (1 << d)):
                        blocked = True
                        break
                if not blocked:
                    addable += 1

    # Exact Empty-Square Forcing Identity verification (when C4-free)
    m = len(edges)
    w_sum = sum(d * (d - 1) // 2 for d in deg)
    total_sq = math.comb(n, 2) * (1 << (n - 2))
    assert n0 + n1 + n2_opp + n2_adj + n3 + n4 == total_sq
    if n4 == 0:
        lhs = n2_opp - n0
        rhs = (n - 1) * m - total_sq - w_sum
        assert lhs == rhs, f"Identity failed: {lhs} != {rhs}"

    # Convexity minimum W_min for given m on 2^n vertices
    q, r = divmod(2 * m, n_verts)
    w_min = (n_verts - r) * (q * (q - 1) // 2) + r * ((q + 1) * q // 2)
    delta_deg = w_sum - w_min

    # Parity-split degree distributions and math-rsi Q3/Q6 budgets (for n=8)
    p0 = Counter(deg[v] for v in range(n_verts) if v.bit_count() % 2 == 0)
    p1 = Counter(deg[v] for v in range(n_verts) if v.bit_count() % 2 == 1)
    deg_hist = Counter(deg)

    # Canonical SHA-256 of sorted edge list
    canon_bytes = "\n".join(f"{u} {v}" for u, v in sorted(edges)).encode("utf-8") + b"\n"
    sha256 = hashlib.sha256(canon_bytes).hexdigest()

    out = {
        "n": n,
        "vertices": n_verts,
        "edges": m,
        "c4_count": n4,
        "c4_free": (n4 == 0),
        "inclusion_maximal": (addable == 0),
        "addable_edges": addable,
        "odd_square": (n0 == 0 and n2_opp == 0 and n2_adj == 0 and n4 == 0),
        "squares": {
            "n0": n0,
            "n1": n1,
            "n2_opp": n2_opp,
            "n2_adj": n2_adj,
            "n3": n3,
            "n4": n4,
        },
        "w_sum": w_sum,
        "w_min": w_min,
        "delta_deg": delta_deg,
        "deg_hist": {str(k): v for k, v in sorted(deg_hist.items())},
        "p0_deg": {str(k): v for k, v in sorted(p0.items())},
        "p1_deg": {str(k): v for k, v in sorted(p1.items())},
        "dim_profile": sorted(dim_cnt),
        "sha256": sha256,
        "elapsed_sec": round(time.perf_counter() - t0, 4),
    }
    if n == 8:
        c_coeff = (735, 534, 333, 177, 66, 0, 0, 105, 345)
        b_coeff = (40, 30, 20, 11, 4, 0, 0, 5, 16)
        out["C_P0"] = sum(c_coeff[d] * cnt for d, cnt in p0.items())
        out["C_P1"] = sum(c_coeff[d] * cnt for d, cnt in p1.items())
        out["C_cap"] = 138432 - 201 * m
        out["b_P0"] = sum(b_coeff[d] * cnt for d, cnt in p0.items())
        out["b_P1"] = sum(b_coeff[d] * cnt for d, cnt in p1.items())
        out["b_cap"] = 6912 - 10 * m
    return out


def corrupt_edges(edges: list[tuple[int, int]], n: int) -> list[tuple[int, int]]:
    """Inject one missing edge that closes a 3-edge path into a C4."""
    edge_set = set(edges)
    n_verts = 1 << n
    for i in range(n):
        bi = 1 << i
        for j in range(i + 1, n):
            bj = 1 << j
            for x in range(n_verts):
                if (x & bi) == 0 and (x & bj) == 0:
                    a, b, c = x ^ bi, x ^ bj, x ^ bi ^ bj
                    sq = [
                        (min(x, a), max(x, a)),
                        (min(x, b), max(x, b)),
                        (min(a, c), max(a, c)),
                        (min(b, c), max(b, c)),
                    ]
                    missing = [e for e in sq if e not in edge_set]
                    if len(missing) == 1:
                        return list(edges) + [missing[0]]
    # Fallback: add a duplicate edge
    return list(edges) + [edges[0]]


def main() -> int:
    parser = argparse.ArgumentParser(description="Exact cold verifier for C4-free Q_n subgraphs.")
    parser.add_argument("files", nargs="*", help="Edge list files to verify (defaults to all seeds/seed*.edges)")
    parser.add_argument("--n", type=int, default=8, help="Hypercube dimension (default 8)")
    parser.add_argument("--min-edges", type=int, default=682, help="Minimum required edges to PASS")
    parser.add_argument("--corrupt", action="store_true", help="Negative self-test: inject a C4 and expect FAIL (rc=1)")
    parser.add_argument("--json", action="store_true", help="Print JSON output only")
    args = parser.parse_args()

    here = Path(__file__).resolve().parent
    if args.files:
        targets = [Path(p) for p in args.files]
    else:
        targets = sorted((here / "atlas").glob("*.edges")) + sorted((here / "seeds").glob("seed*.edges"))
    if not targets:
        print("ERROR: no edge files provided or found in atlas/ or seeds/", file=sys.stderr)
        return 1

    results = []
    all_pass = True
    for path in targets:
        edges = load_edges(path, args.n)
        if args.corrupt:
            edges = corrupt_edges(edges, args.n)
        info = analyze_edges(edges, args.n)
        info["file"] = str(path)
        req_edges = 681 if ("_681_" in path.name and not args.files) else args.min_edges
        ok = info["c4_free"] and info["edges"] >= req_edges
        if "_681_" in path.name and not args.files:
            ok = ok and info["inclusion_maximal"] and info["squares"]["n0"] >= 1
        info["status"] = "PASS" if ok else "FAIL"
        if not ok:
            all_pass = False
        results.append(info)

    payload = {
        "verifier": "q8_c4_extremal/verify.py",
        "corrupt_mode": args.corrupt,
        "all_pass": all_pass,
        "results": results,
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for r in results:
            sq = r["squares"]
            print(
                f"[{r['status']}] {Path(r['file']).name}: Q_{r['n']} |E|={r['edges']} "
                f"C4={r['c4_count']} max={r['inclusion_maximal']} odd={r['odd_square']} "
                f"sq=({sq['n0']},{sq['n1']},{sq['n2_opp']}+{sq['n2_adj']},{sq['n3']},{sq['n4']}) "
                f"W={r['w_sum']}(+{r['delta_deg']}) sha={r['sha256'][:12]} ({r['elapsed_sec']}s)"
            )
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())

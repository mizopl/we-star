#!/usr/bin/env python3
"""Cold-verifiable standalone exact oracle for C4-free subgraphs of hypercubes Q_n (n=4..8)
plus exact F2 gauge-defect Degree-Blocking Identity & exhaustive 14-orbit Case 5A exclusion.

Requires Python >= 3.10 (zero external dependencies; stdlib only).

Checks:
  1. Valid hypercube edges (0 <= u < v < 2^n, popcount(u ^ v) == 1, no duplicates).
  2. Exact C4-freeness via BOTH square enumeration AND common-neighbor counting (dual check).
  3. Exact structural invariants: degree histogram, parity-split profiles (P0, P1),
     square-edge counts (n0, n1, n2_opp, n2_adj, n3, n4), inclusion maximality,
     min_x7 (minimum number of blocking 3-paths over all missing hypercube edges),
     and the exact Empty-Square Forcing Identity:
         n2_opp - n0 == (n - 1) * |E| - C(n, 2) * 2^(n - 2) - sum_v C(d(v), 2).
  4. In default atlas mode: requires the exact set of all 10 expected atlas/*.edges files
     and verifies every file against its pinned edge count, odd-square flag, square counts,
     wedge sum W, convexity defect Delta_deg, min_x7, and canonical SHA-256.
  5. On every odd-square Q_8 witness: exact F2 Degree-Blocking Identity across all missing edges:
         deg(u) + deg(v) == 7 + b_{H_0}(e) - q_opp(e).
  6. Exhaustive 14-orbit Stab_{Aut(Q_8)}(f_1) elimination of the 31 candidate Case 5A triples
     (given the paper reduction in README §1.B.5 for |delta| = 5 minimal, a=3, r=2, |E(H_0)| = 682:
     0 survivors across all 1,023 pairs).
  7. Built-in `--corrupt` negative self-test that injects a C4 (causing C4 > 0) and exits with rc=1.

Usage:
  env -i PATH=/opt/homebrew/bin:/usr/bin:/bin python3 verify.py
  env -i PATH=/opt/homebrew/bin:/usr/bin:/bin python3 verify.py --corrupt
  env -i PATH=/opt/homebrew/bin:/usr/bin:/bin python3 verify.py --min-edges 682 atlas/q8_682_*.edges
"""
from __future__ import annotations

import sys

if sys.version_info < (3, 10):
    sys.stderr.write(
        f"ERROR: Python >= 3.10 required (found {sys.version_info.major}.{sys.version_info.minor}).\n"
    )
    raise SystemExit(2)

import argparse
import hashlib
import json
import math
import time
from collections import Counter
from itertools import combinations
from pathlib import Path


# Pinned invariants for all 10 inclusion-maximal witnesses in atlas/
# Tuple: (edges, odd_square, (n0, n1, n2_opp, n2_adj, n3), w_sum, delta_deg, min_x7, full_sha256)
EXPECTED_ATLAS: dict[str, tuple[int, bool, tuple[int, int, int, int, int], int, int, int, str]] = {
    "q8_675_maximal_phantom_n0_4_n2a_94.edges": (675, False, (4, 265, 15, 94, 1414), 2922, 12, 1, "6e484827d5433367784eb8514d0a62cff20c297e8c67d10799a8618e858fc2eb"),
    "q8_678_maximal_blocked_n0_5_n2a_21.edges": (678, False, (5, 293, 8, 21, 1465), 2951, 11, 1, "0068718824c46a7799e693cdb1b56bc22cd10dd1bb72bdcb5abda7ef7e5c3448"),
    "q8_678_maximal_high_n2a_78_n0_0.edges": (678, False, (0, 273, 6, 78, 1435), 2948, 8, 1, "7e5ad9fb2310b74fc0ae79830689a3905d7b26ff9443cd90ec3af321aaebe049"),
    "q8_680_maximal_blocked_n0_2_n2a_24.edges": (680, False, (2, 291, 4, 24, 1471), 2966, 6, 1, "a9a21b8bf56fa13a863246abba071c7047364a20102a14e7fa2d67c81baa8d2e"),
    "q8_681_maximal_blocked_empty_sq_n0_1.edges": (681, False, (1, 295, 2, 14, 1480), 2974, 4, 1, "0af37457926621817a9b22f905eaedeaffb4b14ebf310bde0e750da5a98b03e0"),
    "q8_682_deg41_nonodd_n2o1_n2a11.edges": (682, False, (0, 295, 1, 11, 1485), 2981, 1, 1, "d9f494b089a67932cadde3c1b092e9722cbb638fdec225bf73e8bffebe4ba94c"),
    "q8_682_deg42_nonodd_n2o0_n2a12.edges": (682, False, (0, 295, 0, 12, 1485), 2982, 2, 1, "133531616e98dfa59786c6432a7e5807ba452e154b4df60d9f0bde42c1f182bf"),
    "q8_682_deg56_zero_defect_n2o2_n2a10.edges": (682, False, (0, 295, 2, 10, 1485), 2980, 0, 1, "31b3bdf85cfbf573f9817e0c74b0d5ef2951910006d75d59909176a84b025855"),
    "q8_682_odd_deg7_vertex.edges": (682, True, (0, 301, 0, 0, 1491), 2982, 2, 3, "eb026494fedc1c79fb53a690e15805e22cae17bcbd0ec3007d62e1a02a670d22"),
    "q8_682_odd_x7min1_pivot_bridge.edges": (682, True, (0, 301, 0, 0, 1491), 2982, 2, 1, "e08abf55234db28da008f9ec95bf1a1f1c82793a4186534cb68a432960ed7814"),
}


def _require(cond: bool, msg: str) -> None:
    """Unstrippable invariant check (remains active under python3 -O)."""
    if not cond:
        raise ValueError(msg)


def load_edges(path: Path, n: int) -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    n_verts = 1 << n
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.replace(",", " ").split()
        _require(len(parts) == 2, f"{path}:{lineno}: expected exactly 2 vertex tokens, got {raw!r}")
        u, v = int(parts[0]), int(parts[1])
        if u > v:
            u, v = v, u
        _require(0 <= u < n_verts and 0 <= v < n_verts, f"{path}:{lineno}: vertex out of range for Q_{n}: ({u}, {v})")
        diff = u ^ v
        _require(diff != 0 and (diff & (diff - 1)) == 0, f"{path}:{lineno}: non-hypercube edge ({u}, {v})")
        _require((u, v) not in seen, f"{path}:{lineno}: duplicate edge ({u}, {v})")
        seen.add((u, v))
        edges.append((u, v))
    return edges


def analyze_edges(edges: list[tuple[int, int]], n: int) -> dict:
    t0 = time.perf_counter()
    n_verts = 1 << n
    edge_set = set(edges)
    _require(len(edge_set) == len(edges), "Duplicate edges detected")

    adj = [0] * n_verts
    deg = [0] * n_verts
    dim_cnt = [0] * n
    for u, v in edges:
        _require(u < v, f"Unnormalized edge ({u}, {v})")
        diff = u ^ v
        _require(diff != 0 and (diff & (diff - 1)) == 0, f"Non-hypercube edge ({u}, {v})")
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
    _require(c4_common % 4 == 0, f"Internal C4 symmetry count not divisible by 4: {c4_common}")
    c4_common //= 4
    _require(c4_common == n4, f"Dual C4 check mismatch: {c4_common} vs {n4}")

    # Inclusion maximality, min_x7 & odd-square Degree-Blocking Identity check
    is_odd = (n0 == 0 and n2_opp == 0 and n2_adj == 0 and n4 == 0)
    addable = 0
    min_x7: int | None = None
    deg_block_max_err = 0
    missing_checked = 0
    for v in range(n_verts):
        for d in range(n):
            bd = 1 << d
            u = v ^ bd
            if v < u and not (adj[v] & bd):
                missing_checked += 1
                b_cnt = 0
                q_opp = 0
                for j in range(n):
                    if j == d:
                        continue
                    bj = 1 << j
                    ev = 1 if (adj[v] & bj) else 0
                    eu = 1 if (adj[u] & bj) else 0
                    eo = 1 if (adj[v ^ bj] & bd) else 0
                    if ev and eu and eo:
                        b_cnt += 1
                    elif eo and not ev and not eu:
                        q_opp += 1
                if min_x7 is None or b_cnt < min_x7:
                    min_x7 = b_cnt
                if b_cnt == 0:
                    addable += 1
                if is_odd:
                    err = abs((deg[v] + deg[u]) - ((n - 1) + b_cnt - q_opp))
                    if err > deg_block_max_err:
                        deg_block_max_err = err
    if is_odd:
        _require(deg_block_max_err == 0, f"Degree-Blocking Identity failed: max_err={deg_block_max_err}")

    # Exact Empty-Square Forcing Identity verification (when C4-free)
    m = len(edges)
    w_sum = sum(d * (d - 1) // 2 for d in deg)
    total_sq = math.comb(n, 2) * (1 << (n - 2))
    _require(n0 + n1 + n2_opp + n2_adj + n3 + n4 == total_sq, "Square partition sum mismatch")
    if n4 == 0:
        lhs = n2_opp - n0
        rhs = (n - 1) * m - total_sq - w_sum
        _require(lhs == rhs, f"Empty-Square Forcing Identity failed: {lhs} != {rhs}")

    q, r = divmod(2 * m, n_verts)
    w_min = (n_verts - r) * (q * (q - 1) // 2) + r * ((q + 1) * q // 2)
    delta_deg = w_sum - w_min

    p0 = Counter(deg[v] for v in range(n_verts) if v.bit_count() % 2 == 0)
    p1 = Counter(deg[v] for v in range(n_verts) if v.bit_count() % 2 == 1)
    deg_hist = Counter(deg)
    n_even = n0 + n2_opp + n2_adj
    delta_lb = math.ceil(n_even / (n - 1))

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
        "min_x7": min_x7,
        "odd_square": is_odd,
        "deg_block_max_err": deg_block_max_err if is_odd else None,
        "missing_edges_checked": missing_checked,
        "n_even_squares": n_even,
        "f2_delta_lower_bound": delta_lb,
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


def verify_case5a_exclusion() -> dict:
    """Exhaustive 14-orbit Stab_{Aut(Q_8)}(f_1) elimination of the 31 candidate Case 5A triples
    (given the paper reduction in README §1.B.5 for |delta| = 5 minimal, a = 3, r = 2,
    |E(H_0)| = 682): checks 0 surviving triples across all 1,023 pairs (f_1, f_2).
    """
    t0 = time.perf_counter()
    edges: list[tuple[int, int, int]] = []
    eidx: dict[tuple[int, int], int] = {}
    for u in range(256):
        for d in range(8):
            if not (u & (1 << d)):
                v = u | (1 << d)
                eidx[(u, v)] = len(edges)
                edges.append((u, v, d))

    edge_sq_neighbors: list[dict[int, int]] = [dict() for _ in range(1024)]
    squares: list[tuple[int, int, int, int]] = []
    for a in range(8):
        for b in range(a + 1, 8):
            ba, bb = 1 << a, 1 << b
            for v in range(256):
                if (v & ba) or (v & bb):
                    continue
                sq = (
                    eidx[(v, v | ba)],
                    eidx[(v | ba, v | ba | bb)],
                    eidx[(v | bb, v | ba | bb)],
                    eidx[(v, v | bb)],
                )
                si = len(squares)
                squares.append(sq)
                for x in sq:
                    for y in sq:
                        if x != y:
                            edge_sq_neighbors[x][y] = si

    # Verify canonical Clifford-sign odd-square reference x_ref on all 1,792 squares
    x_ref = [bin(u & ((1 << d) - 1)).count("1") % 2 for (u, _, d) in edges]
    for sq in squares:
        _require(sum(x_ref[e] for e in sq) % 2 == 1, "x_ref failed odd-square check")

    f1 = eidx[(0, 1)]
    orbits: dict[tuple[str, int], list[int]] = {}
    for f2 in range(1024):
        if f2 == f1:
            continue
        u, _, d = edges[f2]
        if d == 0:
            key = ("par", (u >> 1).bit_count())
        else:
            key = ("orth", ((u >> 1) & ~(1 << (d - 1))).bit_count())
        orbits.setdefault(key, []).append(f2)

    _require(len(orbits) == 14, f"Expected 14 Stab(f1) orbits, got {len(orbits)}")
    _require(sum(len(v) for v in orbits.values()) == 1023, "Orbit sizes do not sum to 1023")

    survivors = 0
    triples_checked = 0
    for key in sorted(orbits):
        f2 = orbits[key][0]
        s1 = set(edge_sq_neighbors[f1].keys()) - {f2}
        s2 = set(edge_sq_neighbors[f2].keys()) - {f1}
        cand_s2: list[int] = []
        cand_s1: list[int] = []
        for e in (s1 | s2):
            sqs = set()
            if e in edge_sq_neighbors[f1]:
                sqs.add(edge_sq_neighbors[f1][e])
            if e in edge_sq_neighbors[f2]:
                sqs.add(edge_sq_neighbors[f2][e])
            if len(sqs) == 2:
                cand_s2.append(e)
            elif len(sqs) == 1:
                cand_s1.append(e)

        triples: list[tuple[int, int, int, set[int] | None]] = []
        for e1, e2, e3 in combinations(cand_s2, 3):
            triples.append((e1, e2, e3, None))
        for es1 in cand_s1:
            u1, v1, _ = edges[es1]
            d4 = {u1, v1}
            hit_s2 = [e for e in cand_s2 if edges[e][0] in d4 or edges[e][1] in d4]
            for e2, e3 in combinations(hit_s2, 2):
                triples.append((es1, e2, e3, d4))

        triples_checked += len(triples)
        for e1, e2, e3, fixed_d4 in triples:
            # Spin-flip minimality: no vertex has >= 5 edges in delta (else |delta'| <= 3)
            vcnt: dict[int, int] = {}
            min_ok = True
            for e in (f1, f2, e1, e2, e3):
                u, v, _ = edges[e]
                vcnt[u] = vcnt.get(u, 0) + 1
                vcnt[v] = vcnt.get(v, 0) + 1
                if vcnt[u] >= 5 or vcnt[v] >= 5:
                    min_ok = False
                    break
            if not min_ok:
                continue

            if fixed_d4 is None:
                # Exact complete enumeration of ALL vertex covers (hitting sets) of size <= 2
                # over the endpoints of {e1, e2, e3}.
                ep1 = {edges[e1][0], edges[e1][1]}
                ep2 = {edges[e2][0], edges[e2][1]}
                ep3 = {edges[e3][0], edges[e3][1]}
                all_v = sorted(ep1 | ep2 | ep3)
                d4_list: list[set[int]] = []
                for a in all_v:
                    if a in ep1 and a in ep2 and a in ep3:
                        d4_list.append({a})
                for a, b in combinations(all_v, 2):
                    s = {a, b}
                    if (s & ep1) and (s & ep2) and (s & ep3):
                        d4_list.append(s)
                if not d4_list:
                    continue
            else:
                d4_list = [fixed_d4]

            e_set = {e1, e2, e3}
            any_ok = False
            for d4 in d4_list:
                forced_h0 = {f1, f2}
                bad = False
                for ei in (e1, e2, e3):
                    ui, vi, _ = edges[ei]
                    both_d4 = (ui in d4 and vi in d4)
                    sqs = set()
                    if ei in edge_sq_neighbors[f1]:
                        sqs.add(edge_sq_neighbors[f1][ei])
                    if ei in edge_sq_neighbors[f2]:
                        sqs.add(edge_sq_neighbors[f2][ei])
                    if not both_d4:
                        if len(sqs) < 2:
                            bad = True
                            break
                        for si in sqs:
                            for x in squares[si]:
                                if x != ei:
                                    forced_h0.add(x)
                    else:
                        if len(sqs) == 1:
                            si = next(iter(sqs))
                            for x in squares[si]:
                                if x != ei:
                                    forced_h0.add(x)
                if bad or (forced_h0 & e_set):
                    continue
                c4_bad = False
                for sq in squares:
                    nh = sum(1 for x in sq if x in forced_h0)
                    if nh == 4:
                        c4_bad = True
                        break
                    if nh == 3:
                        ne = sum(1 for x in sq if x in e_set)
                        if ne == 1 and (f1 not in sq and f2 not in sq):
                            c4_bad = True
                            break
                if not c4_bad:
                    any_ok = True
                    break
            if any_ok:
                survivors += 1

    return {
        "orbits_checked": len(orbits),
        "pairs_covered": sum(len(v) for v in orbits.values()),
        "triples_checked": triples_checked,
        "survivors": survivors,
        "pass": (survivors == 0),
        "elapsed_sec": round(time.perf_counter() - t0, 4),
    }


def corrupt_edges_same_size(edges: list[tuple[int, int]], n: int) -> list[tuple[int, int]]:
    """Swap 1 existing edge out and 1 missing edge in so |E| stays UNCHANGED while C4 > 0 is injected."""
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
                        sq_set = set(sq)
                        # Drop an edge NOT in sq so sq becomes a C4 while |E| stays identical
                        for rem in edges:
                            if rem not in sq_set:
                                return [e for e in edges if e != rem] + [missing[0]]
    return list(edges) + [edges[0]]


def check_pinned_atlas_entry(name: str, info: dict) -> tuple[bool, list[str]]:
    exp_e, exp_odd, exp_sq, exp_w, exp_del, exp_x7, exp_sha = EXPECTED_ATLAS[name]
    sq = info["squares"]
    got_sq = (sq["n0"], sq["n1"], sq["n2_opp"], sq["n2_adj"], sq["n3"])
    errs: list[str] = []
    if not info["c4_free"]:
        errs.append(f"C4={info['c4_count']} > 0")
    if info["edges"] != exp_e:
        errs.append(f"edges={info['edges']} != {exp_e}")
    if not info["inclusion_maximal"]:
        errs.append(f"addable={info['addable_edges']} > 0")
    if info["odd_square"] != exp_odd:
        errs.append(f"odd={info['odd_square']} != {exp_odd}")
    if got_sq != exp_sq:
        errs.append(f"squares={got_sq} != {exp_sq}")
    if info["w_sum"] != exp_w:
        errs.append(f"W={info['w_sum']} != {exp_w}")
    if info["delta_deg"] != exp_del:
        errs.append(f"delta_deg={info['delta_deg']} != {exp_del}")
    if info["min_x7"] != exp_x7:
        errs.append(f"min_x7={info['min_x7']} != {exp_x7}")
    if info["sha256"] != exp_sha:
        errs.append(f"sha={info['sha256'][:12]} != {exp_sha[:12]}")
    return (len(errs) == 0), errs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Exact cold verifier for C4-free Q_n subgraphs & Case 5A F2 gauge-defect exclusion."
    )
    parser.add_argument("files", nargs="*", help="Edge list files to verify (defaults to exact 10 atlas/*.edges)")
    parser.add_argument("--n", type=int, default=8, help="Hypercube dimension (default 8)")
    parser.add_argument("--min-edges", type=int, default=None, help="Minimum required edges to PASS")
    parser.add_argument("--skip-case5a", action="store_true", help="Skip 14-orbit Case 5A check")
    parser.add_argument(
        "--corrupt",
        action="store_true",
        help="Negative self-test: inject C4 > 0 at unchanged |E| and expect FAIL (rc=1)",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON output only")
    args = parser.parse_args()

    here = Path(__file__).resolve().parent
    default_mode = not bool(args.files)
    if args.files:
        targets = [Path(p) for p in args.files]
    else:
        atlas_dir = here / "atlas"
        targets = sorted(atlas_dir.glob("*.edges"))
        found_names = {p.name for p in targets}
        expected_names = set(EXPECTED_ATLAS.keys())
        if found_names != expected_names:
            missing = sorted(expected_names - found_names)
            extra = sorted(found_names - expected_names)
            print(
                f"ERROR: atlas/ file set mismatch (expected exact 10 files). missing={missing}, extra={extra}",
                file=sys.stderr,
            )
            return 1

    if not targets:
        print("ERROR: no edge files provided or found in atlas/", file=sys.stderr)
        return 1

    pinned_mode = default_mode and (args.n == 8) and (args.min_edges is None)
    results = []
    all_pass = True
    for path in targets:
        edges = load_edges(path, args.n)
        if args.corrupt:
            edges = corrupt_edges_same_size(edges, args.n)
        info = analyze_edges(edges, args.n)
        info["file"] = str(path)
        errs: list[str] = []
        if pinned_mode:
            ok, errs = check_pinned_atlas_entry(path.name, info)
        else:
            min_req = args.min_edges if args.min_edges is not None else 675
            if not info["c4_free"]:
                errs.append(f"C4={info['c4_count']} > 0")
            if info["edges"] < min_req:
                errs.append(f"edges={info['edges']} < {min_req}")
            ok = (len(errs) == 0)
        info["errors"] = errs
        info["status"] = "PASS" if ok else "FAIL"
        if not ok:
            all_pass = False
        results.append(info)

    case5a = None
    if not args.skip_case5a and args.n == 8:
        case5a = verify_case5a_exclusion()
        if not case5a["pass"]:
            all_pass = False

    payload = {
        "verifier": "q8-c4-extremal-forcing/verify.py",
        "pinned_atlas_mode": pinned_mode,
        "corrupt_mode": args.corrupt,
        "all_pass": all_pass,
        "results": results,
        "case5a_exclusion": case5a,
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for r in results:
            sq = r["squares"]
            err_s = f" errs={r['errors']}" if r["errors"] else ""
            print(
                f"[{r['status']}] {Path(r['file']).name}: Q_{r['n']} |E|={r['edges']} "
                f"C4={r['c4_count']} max={r['inclusion_maximal']} odd={r['odd_square']} "
                f"sq=({sq['n0']},{sq['n1']},{sq['n2_opp']}+{sq['n2_adj']},{sq['n3']},{sq['n4']}) "
                f"W={r['w_sum']}(+{r['delta_deg']}) min_x7={r['min_x7']} |d|>={r['f2_delta_lower_bound']} "
                f"sha={r['sha256'][:12]} ({r['elapsed_sec']}s){err_s}"
            )
        if case5a is not None:
            tag = "PASS" if case5a["pass"] else "FAIL"
            print(
                f"[{tag}] Case 5A (|delta|=5, a=3, r=2, |H_0|=682): "
                f"{case5a['orbits_checked']}/14 Stab orbits ({case5a['pairs_covered']} pairs, "
                f"{case5a['triples_checked']} triples) -> {case5a['survivors']} survivors ({case5a['elapsed_sec']}s)"
            )
        if all_pass:
            mode_label = "pinned atlas witnesses" if pinned_mode else "edge file(s) (unpinned)"
            case_label = " & Case 5A" if case5a is not None else " (Case 5A skipped)"
            print(f"VERIFIED PASS: {len(results)}/{len(results)} {mode_label}{case_label} passed.")
        else:
            print("VERIFIED FAIL: one or more checks failed (see [FAIL] lines above).")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())

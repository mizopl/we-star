#!/usr/bin/env python3
"""Standalone, read-only exact integer verifier for peeled D_2-equivariant
Schrijver PSD upper-bound certificates (supports .json and .json.gz).

Zero floating-point arithmetic, zero orbit trust, explicit strict-int type
checks on every integer input, explicit int64 overflow guard before Gram
multiplication, full V x V pair sweep, and 3-mode --corrupt negative controls.

Usage:
  python3 verify_peeled_psd.py cert_psd_12_2_peeled.json.gz
  python3 verify_peeled_psd.py cert_psd_12_2_peeled.json.gz --corrupt
"""
import argparse
import gzip
import json
import sys
import time
import numpy as np


def is_strict_int(val) -> bool:
    return isinstance(val, int) and not isinstance(val, bool)


def rev_bits(x: int, n: int) -> int:
    r = 0
    for _ in range(n):
        r = (r << 1) | (x & 1)
        x >>= 1
    return r


def is_subseq_int(z: int, m: int, x: int, n: int) -> bool:
    """LSB-first subsequence check matching Lean isSubseqB (natToWord m z) (natToWord n x)."""
    zi = 0
    for xi in range(n):
        if zi == m:
            return True
        if ((z >> zi) & 1) == ((x >> xi) & 1):
            zi += 1
    return zi == m


def build_deletion_balls(n: int, s: int):
    """Build exact deletion-ball bitmasks D_s(x) over 0..(2^(n-s)-1) for all x in 0..(2^n-1)."""
    del1 = {}
    for L in range(n - s + 1, n + 1):
        tbl = []
        for w in range(1 << L):
            outs = set()
            for i in range(L):
                lo = w & ((1 << i) - 1)
                hi = (w >> (i + 1)) << i
                outs.add(lo | hi)
            tbl.append(tuple(outs))
        del1[L] = tbl

    d_balls = []
    for x in range(1 << n):
        cur = {x}
        for L in range(n, n - s, -1):
            tbl = del1[L]
            nxt = set()
            for w in cur:
                nxt.update(tbl[w])
            cur = nxt
        bm = 0
        for z in cur:
            bm |= 1 << z
        d_balls.append(bm)
    return d_balls


def load_cert(path: str) -> dict:
    if path.endswith(".gz"):
        with gzip.open(path, "rt", encoding="utf-8") as f:
            data = json.load(f)
    else:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Certificate root must be a JSON object")
    return data


def validate_schema(cert: dict):
    required = ("n", "s", "target_core_ub", "balls", "dom_steps", "reps", "row_ci", "L_orb", "S", "T")
    for k in required:
        if k not in cert:
            raise ValueError(f"Missing required key: {k}")

    n = cert["n"]
    s = cert["s"]
    m_core = cert["target_core_ub"]
    S = cert["S"]
    T = cert["T"]
    for name, val in (("n", n), ("s", s), ("target_core_ub", m_core), ("S", S), ("T", T)):
        if not is_strict_int(val):
            raise ValueError(f"Field '{name}' must be a strict int (got {type(val).__name__})")
    if not (1 <= s <= n <= 20):
        raise ValueError(f"Invalid parameters n={n}, s={s}")
    if m_core < 0:
        raise ValueError(f"target_core_ub must be >= 0 (got {m_core})")

    N = 1 << n
    M_sub = 1 << (n - s)

    balls = cert["balls"]
    if not isinstance(balls, list) or not all(is_strict_int(z) for z in balls):
        raise ValueError("Field 'balls' must be a list of strict ints")
    for z in balls:
        if not (0 <= z < M_sub):
            raise ValueError(f"Ball center {z} out of range [0, {M_sub})")

    dom_steps = cert["dom_steps"]
    if not isinstance(dom_steps, list):
        raise ValueError("Field 'dom_steps' must be a list of [y, x] pairs")
    for idx, st in enumerate(dom_steps):
        if not (isinstance(st, list) and len(st) == 2 and is_strict_int(st[0]) and is_strict_int(st[1])):
            raise ValueError(f"dom_steps[{idx}] must be a pair of strict ints")

    reps = cert["reps"]
    if not isinstance(reps, list) or not all(is_strict_int(r) for r in reps):
        raise ValueError("Field 'reps' must be a list of strict ints")
    if len(set(reps)) != len(reps):
        raise ValueError("Duplicate orbit representatives in 'reps'")
    for r in reps:
        if not (0 <= r < N):
            raise ValueError(f"Orbit representative {r} out of range [0, {N})")

    row_ci = cert["row_ci"]
    if not isinstance(row_ci, list) or not row_ci:
        raise ValueError("Field 'row_ci' must be a non-empty list of ints in {0, 1, 2, 3}")
    for idx, ci in enumerate(row_ci):
        if not is_strict_int(ci) or ci not in (0, 1, 2, 3):
            raise ValueError(f"row_ci[{idx}] must be an int in {{0, 1, 2, 3}}")

    L_orb = cert["L_orb"]
    if not isinstance(L_orb, list) or len(L_orb) != len(row_ci):
        raise ValueError(f"L_orb must have {len(row_ci)} rows")
    n_orb = len(reps)
    for r_idx, row in enumerate(L_orb):
        if not isinstance(row, list) or len(row) != n_orb:
            raise ValueError(f"L_orb[{r_idx}] must have length {n_orb}")
        for c_idx, val in enumerate(row):
            if not is_strict_int(val):
                raise ValueError(f"L_orb[{r_idx}][{c_idx}] must be a strict int (got {type(val).__name__})")

    return n, s, m_core, balls, dom_steps, reps, row_ci, L_orb, S, T


def verify_peeled_psd(cert: dict, corrupt_mode: str = None, precomp=None) -> dict:
    t0 = time.perf_counter()
    try:
        n, s, m_core, balls, dom_steps, reps, row_ci, L_orb, S, T = validate_schema(cert)
    except ValueError as exc:
        return {"ok": False, "reason": f"Schema validation failed: {exc}"}

    N = 1 << n
    mask = N - 1
    if precomp is None:
        d_balls = build_deletion_balls(n, s)
        g_maps = [
            [x for x in range(N)],
            [x ^ mask for x in range(N)],
            [rev_bits(x, n) for x in range(N)],
            [rev_bits(x, n) ^ mask for x in range(N)],
        ]
    else:
        d_balls, g_maps = precomp

    chars = [[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, -1], [1, -1, -1, 1]]

    S_use = S
    T_use = T
    L_use = [list(row) for row in L_orb]
    steps_use = [list(st) for st in dom_steps]

    if corrupt_mode == "bump_T":
        T_use = (m_core + 1) * S_use
    elif corrupt_mode == "corrupt_entry":
        L_use[0][0] = L_use[0][0] + 500
    elif corrupt_mode == "corrupt_dom":
        if not steps_use:
            return {"ok": False, "reason": "No domination steps available to corrupt"}
        steps_use[0] = [steps_use[0][0], steps_use[0][1] ^ 1]
    elif corrupt_mode is not None:
        return {"ok": False, "reason": f"Unknown corrupt_mode: {corrupt_mode}"}

    # Exact arbitrary-precision integer arithmetic check: S > 0 and T < (m_core + 1) * S
    if not (S_use > 0 and T_use < (m_core + 1) * S_use):
        return {
            "ok": False,
            "reason": f"Arithmetic bound failed: S={S_use}, T={T_use}, (m_core+1)*S={(m_core + 1) * S_use}",
        }

    # Explicit int64 overflow guard BEFORE constructing numpy int64 arrays
    R = len(L_use)
    max_abs = 0
    for row in L_use:
        for val in row:
            av = abs(val)
            if av > max_abs:
                max_abs = av
    if max_abs * max_abs * R >= (1 << 61):
        return {
            "ok": False,
            "reason": f"int64 overflow guard tripped: max_abs={max_abs}, R={R}, max_abs^2*R={max_abs*max_abs*R} >= 2^61",
        }

    # 1) Replay ball peeling independently (verifying subsequence agrees with deletion ball bitmask)
    alive = set()
    for x in range(N):
        in_ball = False
        bx = d_balls[x]
        for z in balls:
            sub = is_subseq_int(z, n - s, x, n)
            bit = ((bx >> z) & 1) == 1
            if sub != bit:
                return {"ok": False, "reason": f"Internal ball/subseq mismatch at x={x}, z={z}"}
            if sub:
                in_ball = True
                break
        if not in_ball:
            alive.add(x)

    for x in alive:
        for gi in range(4):
            if g_maps[gi][x] not in alive:
                return {"ok": False, "reason": f"Post-ball core not D_2-invariant at x={x}"}

    # 2) Replay D_2-orbit domination steps independently
    for step_idx, (y, x) in enumerate(steps_use):
        if not (0 <= x < N and 0 <= y < N):
            return {"ok": False, "reason": f"Dom step {step_idx} out of range: ({y}, {x})"}
        if x not in alive:
            return {"ok": False, "reason": f"Dom step {step_idx}: dominator x={x} not alive"}
        orb_y = {g_maps[gi][y] for gi in range(4)}
        if x in orb_y:
            return {"ok": False, "reason": f"Dom step {step_idx}: dominator x={x} in D_2({y})"}
        bx = d_balls[x]
        by = d_balls[y]
        if not (bx & by):
            return {"ok": False, "reason": f"Dom step {step_idx}: x={x} not adjacent to y={y}"}
        for z in alive:
            bz = d_balls[z]
            if (bx & bz) and not (by & bz):
                return {"ok": False, "reason": f"Dom step {step_idx}: N[x={x}] not subset N[y={y}] at z={z}"}
        alive -= orb_y

    core = sorted(alive)
    V = len(core)
    if V == 0:
        return {"ok": False, "reason": "Empty peeled core"}

    # 3) Expand V[x] over ALL core vertices & verify D_2 stabilizer equivariance
    rep_idx = {r: oi for oi, r in enumerate(reps)}
    V_vecs = []
    for x in core:
        r0 = min(g_maps[gi][x] for gi in range(4))
        if r0 not in rep_idx:
            return {"ok": False, "reason": f"Missing orbit representative {r0} for core vertex {x}"}
        oi = rep_idx[r0]
        vec = None
        for gi in range(4):
            if g_maps[gi][r0] == x:
                cand = [chars[row_ci[k]][gi] * L_use[k][oi] for k in range(R)]
                if vec is None:
                    vec = cand
                elif cand != vec:
                    return {"ok": False, "reason": f"Stabilizer equivariance mismatch at x={x}, gi={gi}"}
        if vec is None:
            return {"ok": False, "reason": f"Orbit map failure for x={x}"}
        V_vecs.append(vec)

    # 4) Exact overflow-guarded int64 Gram matrix Q_mat = V_mat @ V_mat.T
    V_mat = np.array(V_vecs, dtype=np.int64)
    Q_mat = V_mat @ V_mat.T

    diag = np.diag(Q_mat)
    worst_diag_i = int(np.argmax(diag))
    max_diag = int(diag[worst_diag_i])
    # Cross-check worst diagonal in Python arbitrary-precision int
    exact_diag = sum(a * a for a in V_vecs[worst_diag_i])
    if exact_diag != max_diag:
        return {"ok": False, "reason": f"Exact int diagonal mismatch: {exact_diag} != {max_diag}"}
    if max_diag > T_use - S_use:
        return {
            "ok": False,
            "reason": f"Diagonal violated at x={core[worst_diag_i]}: {max_diag} > T-S={T_use - S_use}",
        }

    # 5) Exhaustive V x V non-edge sweep (zero orbit trust)
    max_ne = None
    worst_ne = (-1, -1)
    ne_pairs = 0
    edge_pairs = 0
    neg_S = -S_use
    for i in range(V):
        xi = core[i]
        bxi = d_balls[xi]
        qi = Q_mat[i]
        for j in range(i + 1, V):
            xj = core[j]
            if bxi & d_balls[xj]:
                edge_pairs += 1
            else:
                ne_pairs += 1
                val = int(qi[j])
                if max_ne is None or val > max_ne:
                    max_ne = val
                    worst_ne = (i, j)
                if val > neg_S:
                    return {
                        "ok": False,
                        "reason": f"Non-edge ({xi}, {xj}) violated: Q={val} > -S={neg_S}",
                    }

    if worst_ne[0] >= 0:
        exact_ne = sum(a * b for a, b in zip(V_vecs[worst_ne[0]], V_vecs[worst_ne[1]]))
        if exact_ne != max_ne:
            return {"ok": False, "reason": f"Exact int non-edge mismatch: {exact_ne} != {max_ne}"}

    core_floor = T_use // S_use
    if core_floor > m_core:
        return {"ok": False, "reason": f"floor(T/S)={core_floor} exceeds target_core_ub={m_core}"}

    return {
        "ok": True,
        "n": n,
        "s": s,
        "core_size": V,
        "n_orbs": len(reps),
        "rank": R,
        "max_abs": max_abs,
        "n_balls": len(balls),
        "n_dom_steps": len(steps_use),
        "S": S_use,
        "T": T_use,
        "max_diag": max_diag,
        "max_ne": max_ne,
        "core_floor": core_floor,
        "total_ub": len(balls) + core_floor,
        "edge_pairs": edge_pairs,
        "ne_pairs": ne_pairs,
        "verify_s": round(time.perf_counter() - t0, 2),
    }


def main():
    import pathlib as _pathlib
    ap = argparse.ArgumentParser(description="Standalone exact integer verifier for peeled Schrijver PSD certificates.")
    ap.add_argument(
        "cert_path",
        nargs="?",
        default=str(_pathlib.Path(__file__).resolve().parent / "cert_psd_12_2_peeled.json.gz"),
        help="Path to certificate (.json or .json.gz; defaults to companion cert_psd_12_2_peeled.json.gz)",
    )
    ap.add_argument(
        "--corrupt",
        action="store_true",
        help="After clean verification, run all 3 corruption controls (bump_T, corrupt_entry, corrupt_dom) and require 3/3 rejections.",
    )
    ap.add_argument(
        "--fail-mode",
        choices=("bump_T", "corrupt_entry", "corrupt_dom"),
        default=None,
        help="Run a single corrupted verification (expected to fail with exit code 1).",
    )
    args = ap.parse_args()

    cert = load_cert(args.cert_path)
    n, s = cert["n"], cert["s"]
    if not (is_strict_int(n) and is_strict_int(s) and 1 <= s <= n <= 20):
        print("FAIL: invalid (n, s) in certificate", file=sys.stderr)
        sys.exit(1)

    N = 1 << n
    mask = N - 1
    precomp = (
        build_deletion_balls(n, s),
        [
            [x for x in range(N)],
            [x ^ mask for x in range(N)],
            [rev_bits(x, n) for x in range(N)],
            [rev_bits(x, n) ^ mask for x in range(N)],
        ],
    )

    if args.fail_mode is not None:
        res = verify_peeled_psd(cert, corrupt_mode=args.fail_mode, precomp=precomp)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res["ok"] else 1)

    if args.corrupt:
        modes = ("bump_T", "corrupt_entry", "corrupt_dom")
        rejected = 0
        for mode in modes:
            cr = verify_peeled_psd(cert, corrupt_mode=mode, precomp=precomp)
            if cr["ok"]:
                print(f"ERROR [CORRUPT:{mode}]: corrupted certificate was unexpectedly ACCEPTED!", file=sys.stderr)
                sys.exit(0)
            rejected += 1
            print(f"[CORRUPT_REJECTED:{mode}] {cr['reason']}")
        print(f"[CORRUPT_CONTROLS_OK] {rejected}/{len(modes)} corruptions rejected (exiting rc=1 as required)")
        sys.exit(1)

    res = verify_peeled_psd(cert, corrupt_mode=None, precomp=precomp)
    if not res["ok"]:
        print(f"FAIL [CLEAN]: {res['reason']}", file=sys.stderr)
        sys.exit(1)

    print(
        f"PASS [CLEAN]: M_{res['s']}({res['n']}) <= {res['total_ub']} "
        f"(balls={res['n_balls']}, dom_steps={res['n_dom_steps']}, core={res['core_size']}, "
        f"orbs={res['n_orbs']}, rank={res['rank']}, max|L|={res['max_abs']}, "
        f"S={res['S']}, T={res['T']}, T/S={res['T']/res['S']:.6f} < {res['core_floor'] + 1}, "
        f"pairs={res['edge_pairs'] + res['ne_pairs']}, dt={res['verify_s']}s)"
    )


if __name__ == "__main__":
    main()

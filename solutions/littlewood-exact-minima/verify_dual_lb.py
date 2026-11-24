#!/opt/homebrew/bin/python3
"""Standalone Cold Verifier (CLSS-1 / I-05) for Dual-DAG Lower-Bound Certificates (littlewood-exact-minima).

Independently verifies (under env -i, zero solver trust):
  1. Witness binary polynomial c in {-1, +1}^N via exact Taylor-Bernstein continuous supremum bracket.
  2. Every excluded phantom R (or outer lag prefix) in an `r_space_conflict_cert` via exact Outside-In
     binary realizability exhaustion (confirming 0 binary preimages exist).
  3. Unconditional Bhatia-Davis lag bound |R_k| <= floor(sqrt(N * (M_UB - N) / 2)) so MILP box bounds
     never exclude any valid binary sequence with sup |g|^2 <= M_UB.
  4. Independent HiGHS re-verification of the exact certified R-space MILP with all axioms + verified cuts
     (or direct PSD eigenvalue check for `sdp_dual_cert`).

Supports --corrupt (adversarially tampers with the certificate and MUST exit rc=1).
"""
import argparse
import base64
import hashlib
import json
import math
import sys
import time
import zlib
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csc_matrix


def eval_certified_supremum_general(c: np.ndarray, G: int = 131072):
    """Exact Taylor-Bernstein rigorous continuous bracket on sup_{|z|=1} |g(z)| for any N."""
    c = np.asarray(c, dtype=np.int64)
    n = c.size
    if c.ndim != 1 or n < 2 or not np.all((c == 1) | (c == -1)):
        raise ValueError("Coefficients must be 1D array in {-1, +1}")
    R = np.array([int(np.dot(c[: n - m], c[m:])) for m in range(n)], dtype=np.int64)
    ms = np.arange(1, n, dtype=np.int64)
    M2 = float(2 * np.sum((ms * ms) * np.abs(R[1:])))
    buf = np.zeros(G, dtype=np.float64)
    buf[:n] = c.astype(np.float64)
    spec = np.fft.rfft(buf)
    f_grid = spec.real * spec.real + spec.imag * spec.imag
    idx_max = int(np.argmax(f_grid))
    f_max_grid = float(f_grid[idx_max])
    h = 2.0 * math.pi / G
    FP_PAD = 1e-9
    f_lo_rig = max(0.0, f_max_grid - FP_PAD)
    f_ub_rig = f_max_grid + 0.125 * M2 * (h * h) + FP_PAD
    return {
        "N": n,
        "f_lo": f_lo_rig,
        "f_ub": f_ub_rig,
        "C_plus_lo": math.sqrt(f_lo_rig / (n + 1.0)),
        "C_plus_ub": math.sqrt(f_ub_rig / (n + 1.0)),
        "C_rms_lo": math.sqrt(f_lo_rig / float(n)),
        "C_rms_ub": math.sqrt(f_ub_rig / float(n)),
        "M_n_lo": math.sqrt(f_lo_rig / float(n)),
        "M_n_ub": math.sqrt(f_ub_rig / float(n)),
        "E4": int(np.sum(R[1:] ** 2)),
        "R": R[1:].tolist(),
    }


def is_norm_Zi(val: int, parity_u: int, parity_v: int) -> bool:
    if val < 0:
        return False
    for u in range(parity_u, int(math.isqrt(val)) + 2, 2):
        rem = val - u * u
        if rem < 0:
            break
        v = math.isqrt(rem)
        if v * v == rem and (v % 2 == parity_v):
            return True
    return False


def is_norm_Zomega(val: int) -> bool:
    if val < 0:
        return False
    target = 4 * val
    for y in range(0, int(math.isqrt(target // 3)) + 2):
        rem = target - 3 * y * y
        if rem < 0:
            break
        x = math.isqrt(rem)
        if x * x == rem and ((x + y) % 2 == 0):
            return True
    return False


def verify_unrealizable_R(N: int, R_lags: list[int], max_nodes: int = 500000) -> tuple[bool, int]:
    """Exhaustively checks that integer R_lags (lags 1..N-1) admits ZERO binary c in {-1, +1}^N.
    Returns (is_provably_unrealizable, nodes_visited).
    Note: If nodes_visited >= max_nodes, returns (False, nodes_visited) (conservative: never falsely certifies!).
    """
    assert N % 2 == 0 and len(R_lags) == N - 1
    R = [N] + [int(x) for x in R_lags]
    # Exact parity & Turyn & endpoint checks
    for k in range(1, N):
        if (R[k] - (N - k)) % 2 != 0 or abs(R[k]) > N - k:
            return True, 1
    for k in range(1, N // 2 + 1):
        if (R[k] + R[N - k] - N) % 4 != 0:
            return True, 1
    f0 = N + 2 * sum(R[1:])
    fpi = N + 2 * sum(((-1) ** k) * R[k] for k in range(1, N))
    S_abs = math.isqrt(f0) if f0 >= 0 else -1
    A_abs = math.isqrt(fpi) if fpi >= 0 else -1
    if S_abs * S_abs != f0 or A_abs * A_abs != fpi or (S_abs % 2 != N % 2) or (A_abs % 2 != N % 2):
        return True, 1
    fpi2 = N + 2 * sum(((-1) ** m) * R[2 * m] for m in range(1, N // 2))
    if not is_norm_Zi(fpi2, (N // 2) % 2, (N // 2) % 2):
        return True, 1

    half = N // 2
    c = [0] * N
    c[0] = 1
    c[N - 1] = R[N - 1]
    nodes = 0
    aborted = False
    found = False

    def dfs(d: int, cur_S: int, cur_A: int):
        nonlocal nodes, aborted, found
        if found or aborted:
            return
        nodes += 1
        if nodes >= max_nodes:
            aborted = True
            return
        rem = N - 2 * d
        if min(abs(cur_S - S_abs), abs(cur_S + S_abs)) > rem:
            return
        if min(abs(cur_A - A_abs), abs(cur_A + A_abs)) > rem:
            return
        if d == half:
            for k in range(half - 1, 0, -1):
                s = 0
                for j in range(N - k):
                    s += c[j] * c[j + k]
                if s != R[k]:
                    return
            found = True
            return
        L = N - 1 - d
        inner = 0
        for j in range(1, d):
            inner += c[j] * c[j + L]
        need = R[L] - inner
        if need not in (-2, 0, 2):
            return
        c0, cn = c[0], c[N - 1]
        sd = 1 if (d % 2 == 0) else -1
        snd = 1 if ((N - 1 - d) % 2 == 0) else -1
        for x in (1, -1):
            for y in (1, -1):
                if c0 * y + x * cn == need:
                    c[d] = x
                    c[N - 1 - d] = y
                    dfs(d + 1, cur_S + x + y, cur_A + sd * x + snd * y)
                    if found or aborted:
                        return
        c[d] = 0
        c[N - 1 - d] = 0

    dfs(1, c[0] + c[N - 1], c[0] - c[N - 1])
    if aborted or found:
        return False, nodes
    return True, nodes


def verify_unrealizable_prefix(N: int, prefix_lags: dict[int, int]) -> bool:
    """Checks that fixing outer lags {N-1: r1, N-2: r2, ..., N-m: rm} admits ZERO binary outer shells."""
    max_d = max(N - k for k in prefix_lags)
    c = [0] * N
    c[0] = 1
    r_last = prefix_lags.get(N - 1)
    if r_last not in (-1, 1):
        return True
    c[N - 1] = r_last
    found = False

    def dfs(d: int):
        nonlocal found
        if found:
            return
        if d >= max_d:
            found = True
            return
        L = N - 1 - d
        if L not in prefix_lags:
            for x in (1, -1):
                for y in (1, -1):
                    c[d], c[N - 1 - d] = x, y
                    dfs(d + 1)
                    if found:
                        return
            return
        inner = sum(c[j] * c[j + L] for j in range(1, d))
        need = prefix_lags[L] - inner
        if need not in (-2, 0, 2):
            return
        for x in (1, -1):
            for y in (1, -1):
                if c[0] * y + x * c[N - 1] == need:
                    c[d], c[N - 1 - d] = x, y
                    dfs(d + 1)
                    if found:
                        return

    dfs(1)
    return not found


def verify_r_space_conflict_cert(cert: dict, corrupt: bool = False) -> bool:
    """Independently verifies a full R-space Dual-DAG lower-bound certificate."""
    N = int(cert["N"])
    witness = np.array(cert["witness_c"], dtype=np.int64)
    claimed_lb_M = float(cert["certified_LB_M"])
    thetas = np.array(cert["thetas"], dtype=np.float64)
    excluded_R = [list(map(int, r)) for r in cert.get("excluded_phantoms", [])]
    excluded_prefixes = cert.get("excluded_prefixes", [])

    if corrupt:
        # Adversarial tamper: claim the TRUE witness R is an unrealizable phantom (MUST FAIL!)
        w_info_tmp = eval_certified_supremum_general(witness)
        excluded_R = [w_info_tmp["R"]] + excluded_R

    # 1. Verify witness upper bound
    w_info = eval_certified_supremum_general(witness)
    M_UB = w_info["f_ub"]
    # Rigorous unconditional Bhatia-Davis cap on |R_k| for ANY binary c with sup |g|^2 <= M_UB:
    # Var(f) = 2 * sum R_k^2 <= N * (M_UB - N) => |R_k| <= floor(sqrt(N * (M_UB - N) / 2))
    bd_cap = int(math.floor(math.sqrt(N * max(0.0, M_UB - N) / 2.0))) + 1
    cap_used = int(cert.get("max_R_abs", bd_cap))
    if cap_used < bd_cap:
        print(f"FAIL: max_R_abs={cap_used} < unconditional Bhatia-Davis cap {bd_cap}")
        return False

    # 2. Independently verify EVERY excluded phantom R has ZERO binary preimages!
    total_nodes = 0
    for idx, R_ph in enumerate(excluded_R):
        ok, nd = verify_unrealizable_R(N, R_ph)
        total_nodes += nd
        if not ok:
            print(f"FAIL: excluded_phantoms[{idx}] is REALIZABLE or unverified (nodes={nd})!")
            return False

    for idx, pref in enumerate(excluded_prefixes):
        pmap = {int(k): int(v) for k, v in pref.items()}
        if not verify_unrealizable_prefix(N, pmap):
            print(f"FAIL: excluded_prefixes[{idx}] is REALIZABLE!")
            return False

    # 3. Independently re-solve the exact R-space MILP with ONLY sound axioms + verified exclusions
    #    and confirm its rigorous dual bound >= claimed_lb_M - 1e-4!
    K = N - 1
    idx_M = 0
    idx_z = list(range(1, 1 + K))
    nvars = 1 + K
    p_vec = np.array([(N - k) % 2 for k in range(1, K + 1)], dtype=np.float64)

    turyn_pairs = [(k, N - k) for k in range(1, (N + 1) // 2) if k < N - k]
    idx_q = list(range(nvars, nvars + len(turyn_pairs)))
    nvars += len(turyn_pairs)

    # Exact cyclotomic sets bounded above by ceil(M_UB)
    m_cap = int(math.ceil(M_UB)) + 2
    cyc_sq = [s * s for s in range(N % 2, int(math.isqrt(m_cap)) + 2, 2) if s * s <= m_cap]
    cyc_zi = [v for v in range(0, m_cap + 1) if is_norm_Zi(v, (N // 2) % 2, (N // 2) % 2)]
    cyc_zw = [v for v in range(0, m_cap + 1) if is_norm_Zomega(v)]

    idx_f0 = list(range(nvars, nvars + len(cyc_sq))); nvars += len(idx_f0)
    idx_fpi = list(range(nvars, nvars + len(cyc_sq))); nvars += len(idx_fpi)
    idx_fpi2 = list(range(nvars, nvars + len(cyc_zi))); nvars += len(idx_fpi2)
    idx_fpi3 = list(range(nvars, nvars + len(cyc_zw))); nvars += len(idx_fpi3)
    idx_f2pi3 = list(range(nvars, nvars + len(cyc_zw))); nvars += len(idx_f2pi3)

    # Exact binary encoding of discrete R_k values needed to express exact no-good cuts!
    # Only create y_{k,v} variables if we have excluded_R or excluded_prefixes
    y_lookup = {}
    need_y = len(excluded_R) > 0 or len(excluded_prefixes) > 0
    y_groups = []
    if need_y:
        for k in range(1, K + 1):
            cap_k = min(N - k, cap_used)
            pk = (N - k) % 2
            vals = [v for v in range(-cap_k, cap_k + 1) if (v - pk) % 2 == 0]
            idxs = list(range(nvars, nvars + len(vals)))
            nvars += len(vals)
            for v, yi in zip(vals, idxs):
                y_lookup[(k, v)] = yi
            y_groups.append((k, vals, idxs))

    lb = np.full(nvars, -np.inf)
    ub = np.full(nvars, np.inf)
    integrality = np.zeros(nvars, dtype=int)
    lb[idx_M] = float(N); ub[idx_M] = float(M_UB) + 1.0
    for i, k in enumerate(range(1, K + 1)):
        cap_k = min(N - k, cap_used)
        pk = (N - k) % 2
        lb[idx_z[i]] = math.ceil((-cap_k - pk) / 2.0)
        ub[idx_z[i]] = math.floor((cap_k - pk) / 2.0)
        integrality[idx_z[i]] = 1
    for qi in idx_q:
        lb[qi] = -N; ub[qi] = N; integrality[qi] = 1
    for bi in idx_f0 + idx_fpi + idx_fpi2 + idx_fpi3 + idx_f2pi3:
        lb[bi] = 0; ub[bi] = 1; integrality[bi] = 1
    for _, _, idxs in y_groups:
        for yi in idxs:
            lb[yi] = 0; ub[yi] = 1; integrality[yi] = 1

    rows_i, cols_j, vals_v, clb, cub = [], [], [], [], []
    rcnt = 0
    ks = np.arange(1, K + 1, dtype=np.float64)
    cos_mat = np.cos(np.outer(thetas, ks))
    f_const = N + 2.0 * (cos_mat @ p_vec)

    for l in range(len(thetas)):
        for i in range(K):
            coeff = 4.0 * cos_mat[l, i]
            if abs(coeff) > 1e-13:
                rows_i.append(rcnt); cols_j.append(idx_z[i]); vals_v.append(coeff)
        clb.append(-f_const[l]); cub.append(np.inf); rcnt += 1

    for l in range(len(thetas)):
        rows_i.append(rcnt); cols_j.append(idx_M); vals_v.append(-1.0)
        for i in range(K):
            coeff = 4.0 * cos_mat[l, i]
            if abs(coeff) > 1e-13:
                rows_i.append(rcnt); cols_j.append(idx_z[i]); vals_v.append(coeff)
        clb.append(-np.inf); cub.append(-f_const[l]); rcnt += 1

    n_mod4 = N % 4
    for pidx, (k1, k2) in enumerate(turyn_pairs):
        i1, i2 = k1 - 1, k2 - 1
        rows_i.append(rcnt); cols_j.append(idx_z[i1]); vals_v.append(2.0)
        rows_i.append(rcnt); cols_j.append(idx_z[i2]); vals_v.append(2.0)
        rows_i.append(rcnt); cols_j.append(idx_q[pidx]); vals_v.append(-4.0)
        rhs = n_mod4 - p_vec[i1] - p_vec[i2]
        clb.append(rhs); cub.append(rhs); rcnt += 1

    def add_exact_eval_set(mults, idxs_bin, allowed_vals):
        nonlocal rcnt
        for bi in idxs_bin:
            rows_i.append(rcnt); cols_j.append(bi); vals_v.append(1.0)
        clb.append(1.0); cub.append(1.0); rcnt += 1
        const_part = N + sum(mults[i] * p_vec[i] for i in range(K))
        for i in range(K):
            if mults[i] != 0:
                rows_i.append(rcnt); cols_j.append(idx_z[i]); vals_v.append(2.0 * mults[i])
        for bi, av in zip(idxs_bin, allowed_vals):
            rows_i.append(rcnt); cols_j.append(bi); vals_v.append(-float(av))
        clb.append(-const_part); cub.append(-const_part); rcnt += 1

    add_exact_eval_set([2.0] * K, idx_f0, cyc_sq)
    add_exact_eval_set([2.0 * ((-1.0) ** k) for k in range(1, K + 1)], idx_fpi, cyc_sq)
    add_exact_eval_set([2.0 * ((-1.0) ** (k // 2)) if k % 2 == 0 else 0.0 for k in range(1, K + 1)], idx_fpi2, cyc_zi)
    c_pi3 = [2, 1, -1, -2, -1, 1]
    add_exact_eval_set([float(c_pi3[k % 6]) for k in range(1, K + 1)], idx_fpi3, cyc_zw)
    c_2pi3 = [2, -1, -1]
    add_exact_eval_set([float(c_2pi3[k % 3]) for k in range(1, K + 1)], idx_f2pi3, cyc_zw)

    if need_y:
        for k, vals, idxs in y_groups:
            i = k - 1
            for yi in idxs:
                rows_i.append(rcnt); cols_j.append(yi); vals_v.append(1.0)
            clb.append(1.0); cub.append(1.0); rcnt += 1
            rows_i.append(rcnt); cols_j.append(idx_z[i]); vals_v.append(-2.0)
            for yi, v in zip(idxs, vals):
                rows_i.append(rcnt); cols_j.append(yi); vals_v.append(float(v))
            clb.append(p_vec[i]); cub.append(p_vec[i]); rcnt += 1

        # Add exact no-good cuts: for each excluded phantom R_ph, sum_{k=1..K} y_{k, R_ph[k-1]} <= K - 1
        # Also exclude its D4-alternating twin ((-1)^k R_k)!
        seen_cuts = set()
        for R_ph in excluded_R:
            for sign_alt in (1, -1):
                R_use = tuple(R_ph[k - 1] * (sign_alt ** k) for k in range(1, K + 1))
                if R_use in seen_cuts:
                    continue
                seen_cuts.add(R_use)
                if all((k, R_use[k - 1]) in y_lookup for k in range(1, K + 1)):
                    for k in range(1, K + 1):
                        rows_i.append(rcnt); cols_j.append(y_lookup[(k, R_use[k - 1])]); vals_v.append(1.0)
                    clb.append(-np.inf); cub.append(float(K - 1)); rcnt += 1

        for pref in excluded_prefixes:
            pmap = {int(k): int(v) for k, v in pref.items()}
            if all((k, v) in y_lookup for k, v in pmap.items()):
                for k, v in pmap.items():
                    rows_i.append(rcnt); cols_j.append(y_lookup[(k, v)]); vals_v.append(1.0)
                clb.append(-np.inf); cub.append(float(len(pmap) - 1)); rcnt += 1

    A = csc_matrix((vals_v, (rows_i, cols_j)), shape=(rcnt, nvars))
    c_obj = np.zeros(nvars); c_obj[idx_M] = 1.0
    res = milp(
        c=c_obj,
        integrality=integrality,
        bounds=Bounds(lb, ub),
        constraints=LinearConstraint(A, clb, cub),
        options={"time_limit": float(cert.get("verify_time_limit", 20.0)), "mip_rel_gap": 1e-5},
    )
    dual_b = getattr(res, "mip_dual_bound", None)
    if dual_b is None or not math.isfinite(dual_b):
        dual_b = float(res.x[idx_M]) if (res.x is not None and res.status == 0) else 0.0

    ok_bound = dual_b >= claimed_lb_M - 1e-3
    print(
        f"VERIFY R-SPACE CERT N={N}: witness C+={w_info['C_plus_ub']:.6f} (M_UB={M_UB:.4f}, BD_cap={bd_cap}) | "
        f"excluded_phantoms={len(excluded_R)} (all 0-preimage verified, {total_nodes} nodes) | "
        f"re-verified dual_LB_M={dual_b:.4f} (C+={math.sqrt(dual_b/(N+1)):.6f}) vs claimed={claimed_lb_M:.4f} -> {'PASS' if ok_bound else 'FAIL'}"
    )
    return ok_bound


def verify_unrealizable_subset(N: int, lag_map: dict[int, int], max_nodes: int = 300000) -> tuple[bool, int]:
    """Exhaustively checks that fixing ONLY lags {k: v} in lag_map admits ZERO binary c in {-1,+1}^N."""
    assert N % 2 == 0
    half = N // 2
    inner_checks = [(k, v) for k, v in lag_map.items() if k < half]
    for k, v in lag_map.items():
        if (v - (N - k)) % 2 != 0 or abs(v) > N - k:
            return True, 1
    c = [0] * N
    c[0] = 1
    cn_choices = [lag_map[N - 1]] if (N - 1) in lag_map else [1, -1]
    nodes = 0
    found = False
    aborted = False

    def dfs(d: int):
        nonlocal nodes, found, aborted
        if found or aborted:
            return
        nodes += 1
        if nodes >= max_nodes:
            aborted = True
            return
        if d == half:
            for k, target in inner_checks:
                s = 0
                for j in range(N - k):
                    s += c[j] * c[j + k]
                if s != target:
                    return
            found = True
            return
        L = N - 1 - d
        if L in lag_map:
            inner = 0
            for j in range(1, d):
                inner += c[j] * c[j + L]
            need = lag_map[L] - inner
            if need not in (-2, 0, 2):
                return
            c0, cn = c[0], c[N - 1]
            for x in (1, -1):
                for y in (1, -1):
                    if c0 * y + x * cn == need:
                        c[d] = x
                        c[N - 1 - d] = y
                        dfs(d + 1)
                        if found or aborted:
                            return
        else:
            for x in (1, -1):
                for y in (1, -1):
                    c[d] = x
                    c[N - 1 - d] = y
                    dfs(d + 1)
                    if found or aborted:
                        return
        c[d] = 0
        c[N - 1 - d] = 0

    for cn_val in cn_choices:
        if cn_val not in (-1, 1):
            continue
        c[N - 1] = cn_val
        dfs(1)
        if found or aborted:
            break
    if found or aborted:
        return False, nodes
    return True, nodes


def verify_r_space_mus_cert(cert: dict, corrupt: bool = False) -> bool:
    """Independently verifies a CDCL MUS-Benders certificate (`r_space_mus_cert`)."""
    N = int(cert["N"])
    witness = np.array(cert["witness_c"], dtype=np.int64)
    claimed_lb_M = float(cert["certified_LB_M"])
    thetas = np.array(cert["thetas"], dtype=np.float64)
    excluded_subsets = cert.get("excluded_subsets", [])

    w_info = eval_certified_supremum_general(witness)
    M_UB = w_info["f_ub"]
    bd_cap = int(math.floor(math.sqrt(N * max(0.0, M_UB - N) / 2.0))) + 1
    cap_used = int(cert.get("max_R_abs", bd_cap))
    if cap_used < bd_cap:
        print(f"FAIL: max_R_abs={cap_used} < unconditional Bhatia-Davis cap {bd_cap}")
        return False

    if corrupt:
        # Adversarial tamper: inject a subset satisfied by the TRUE witness (MUST FAIL!)
        true_sub = {str(k): int(w_info["R"][k - 1]) for k in range(N - 5, N)}
        excluded_subsets = [true_sub] + list(excluded_subsets)

    total_nodes = 0
    parsed_subsets = []
    for idx, sub in enumerate(excluded_subsets):
        smap = {int(k): int(v) for k, v in sub.items()}
        ok, nd = verify_unrealizable_subset(N, smap)
        total_nodes += nd
        if not ok:
            print(f"FAIL: excluded_subsets[{idx}] ({smap}) is REALIZABLE or unverified (nodes={nd})!")
            return False
        parsed_subsets.append(smap)

    K = N - 1
    idx_M = 0
    idx_z = list(range(1, 1 + K))
    nvars = 1 + K
    p_vec = np.array([(N - k) % 2 for k in range(1, K + 1)], dtype=np.float64)
    turyn_pairs = [(k, N - k) for k in range(1, (N + 1) // 2) if k < N - k]
    idx_q = list(range(nvars, nvars + len(turyn_pairs))); nvars += len(turyn_pairs)

    m_cap = int(math.ceil(M_UB)) + 2
    cyc_sq = [s * s for s in range(N % 2, int(math.isqrt(m_cap)) + 2, 2) if s * s <= m_cap]
    cyc_zi = [v for v in range(0, m_cap + 1) if is_norm_Zi(v, (N // 2) % 2, (N // 2) % 2)]
    cyc_zw = [v for v in range(0, m_cap + 1) if is_norm_Zomega(v)]

    idx_f0 = list(range(nvars, nvars + len(cyc_sq))); nvars += len(idx_f0)
    idx_fpi = list(range(nvars, nvars + len(cyc_sq))); nvars += len(idx_fpi)
    idx_fpi2 = list(range(nvars, nvars + len(cyc_zi))); nvars += len(idx_fpi2)
    idx_fpi3 = list(range(nvars, nvars + len(cyc_zw))); nvars += len(idx_fpi3)
    idx_f2pi3 = list(range(nvars, nvars + len(cyc_zw))); nvars += len(idx_f2pi3)

    y_lookup = {}
    y_groups = []
    for k in range(1, K + 1):
        cap_k = min(N - k, cap_used)
        pk = (N - k) % 2
        vals = [v for v in range(-cap_k, cap_k + 1) if (v - pk) % 2 == 0]
        idxs = list(range(nvars, nvars + len(vals)))
        nvars += len(vals)
        for v, yi in zip(vals, idxs):
            y_lookup[(k, v)] = yi
        y_groups.append((k, vals, idxs))

    lb = np.full(nvars, -np.inf)
    ub = np.full(nvars, np.inf)
    integrality = np.zeros(nvars, dtype=int)
    lb[idx_M] = float(N); ub[idx_M] = float(M_UB) + 1.0
    for i, k in enumerate(range(1, K + 1)):
        cap_k = min(N - k, cap_used)
        pk = (N - k) % 2
        lb[idx_z[i]] = math.ceil((-cap_k - pk) / 2.0)
        ub[idx_z[i]] = math.floor((cap_k - pk) / 2.0)
        integrality[idx_z[i]] = 1
    for qi in idx_q:
        lb[qi] = -N; ub[qi] = N; integrality[qi] = 1
    for bi in idx_f0 + idx_fpi + idx_fpi2 + idx_fpi3 + idx_f2pi3:
        lb[bi] = 0; ub[bi] = 1; integrality[bi] = 1
    for _, _, idxs in y_groups:
        for yi in idxs:
            lb[yi] = 0; ub[yi] = 1; integrality[yi] = 1

    rows_i, cols_j, vals_v, clb, cub = [], [], [], [], []
    rcnt = 0
    ks = np.arange(1, K + 1, dtype=np.float64)
    cos_mat = np.cos(np.outer(thetas, ks))
    f_const = N + 2.0 * (cos_mat @ p_vec)

    for l in range(len(thetas)):
        for i in range(K):
            coeff = 4.0 * cos_mat[l, i]
            if abs(coeff) > 1e-13:
                rows_i.append(rcnt); cols_j.append(idx_z[i]); vals_v.append(coeff)
        clb.append(-f_const[l]); cub.append(np.inf); rcnt += 1

    for l in range(len(thetas)):
        rows_i.append(rcnt); cols_j.append(idx_M); vals_v.append(-1.0)
        for i in range(K):
            coeff = 4.0 * cos_mat[l, i]
            if abs(coeff) > 1e-13:
                rows_i.append(rcnt); cols_j.append(idx_z[i]); vals_v.append(coeff)
        clb.append(-np.inf); cub.append(-f_const[l]); rcnt += 1

    n_mod4 = N % 4
    for pidx, (k1, k2) in enumerate(turyn_pairs):
        i1, i2 = k1 - 1, k2 - 1
        rows_i.append(rcnt); cols_j.append(idx_z[i1]); vals_v.append(2.0)
        rows_i.append(rcnt); cols_j.append(idx_z[i2]); vals_v.append(2.0)
        rows_i.append(rcnt); cols_j.append(idx_q[pidx]); vals_v.append(-4.0)
        rhs = n_mod4 - p_vec[i1] - p_vec[i2]
        clb.append(rhs); cub.append(rhs); rcnt += 1
        if n_mod4 == 2 and (k1 % 2 == 0) and (k1, 0) in y_lookup and (k2, 0) in y_lookup:
            rows_i.append(rcnt); cols_j.append(y_lookup[(k1, 0)]); vals_v.append(1.0)
            rows_i.append(rcnt); cols_j.append(y_lookup[(k2, 0)]); vals_v.append(1.0)
            clb.append(-np.inf); cub.append(1.0); rcnt += 1

    def add_exact_eval_set(mults, idxs_bin, allowed_vals):
        nonlocal rcnt
        for bi in idxs_bin:
            rows_i.append(rcnt); cols_j.append(bi); vals_v.append(1.0)
        clb.append(1.0); cub.append(1.0); rcnt += 1
        const_part = N + sum(mults[i] * p_vec[i] for i in range(K))
        for i in range(K):
            if mults[i] != 0:
                rows_i.append(rcnt); cols_j.append(idx_z[i]); vals_v.append(2.0 * mults[i])
        for bi, av in zip(idxs_bin, allowed_vals):
            rows_i.append(rcnt); cols_j.append(bi); vals_v.append(-float(av))
        clb.append(-const_part); cub.append(-const_part); rcnt += 1

    add_exact_eval_set([2.0] * K, idx_f0, cyc_sq)
    add_exact_eval_set([2.0 * ((-1.0) ** k) for k in range(1, K + 1)], idx_fpi, cyc_sq)
    add_exact_eval_set([2.0 * ((-1.0) ** (k // 2)) if k % 2 == 0 else 0.0 for k in range(1, K + 1)], idx_fpi2, cyc_zi)
    c_pi3 = [2, 1, -1, -2, -1, 1]
    add_exact_eval_set([float(c_pi3[k % 6]) for k in range(1, K + 1)], idx_fpi3, cyc_zw)
    c_2pi3 = [2, -1, -1]
    add_exact_eval_set([float(c_2pi3[k % 3]) for k in range(1, K + 1)], idx_f2pi3, cyc_zw)

    for k, vals, idxs in y_groups:
        i = k - 1
        for yi in idxs:
            rows_i.append(rcnt); cols_j.append(yi); vals_v.append(1.0)
        clb.append(1.0); cub.append(1.0); rcnt += 1
        rows_i.append(rcnt); cols_j.append(idx_z[i]); vals_v.append(-2.0)
        for yi, v in zip(idxs, vals):
            rows_i.append(rcnt); cols_j.append(yi); vals_v.append(float(v))
        clb.append(p_vec[i]); cub.append(p_vec[i]); rcnt += 1

    # Bhatia-Davis LP coupling
    rows_i.append(rcnt); cols_j.append(idx_M); vals_v.append(-float(N))
    for k, vals, idxs in y_groups:
        for yi, v in zip(idxs, vals):
            if v != 0:
                rows_i.append(rcnt); cols_j.append(yi); vals_v.append(2.0 * float(v * v))
    clb.append(-np.inf); cub.append(-float(N * N)); rcnt += 1

    for smap in parsed_subsets:
        if all((k, v) in y_lookup for k, v in smap.items()):
            for k, v in smap.items():
                rows_i.append(rcnt); cols_j.append(y_lookup[(k, v)]); vals_v.append(1.0)
            clb.append(-np.inf); cub.append(float(len(smap) - 1)); rcnt += 1

    A = csc_matrix((vals_v, (rows_i, cols_j)), shape=(rcnt, nvars))
    # Pure feasibility verification: set ub[idx_M] = claimed_lb_M and c_obj = 0!
    # If HiGHS proves status == 2 (INFEASIBLE), then NO valid R <= claimed_lb_M exists!
    ub[idx_M] = claimed_lb_M
    c_obj = np.zeros(nvars)
    res = milp(
        c=c_obj,
        integrality=integrality,
        bounds=Bounds(lb, ub),
        constraints=LinearConstraint(A, clb, cub),
        options={"time_limit": float(cert.get("verify_time_limit", 45.0))},
    )
    ok_bound = (res.status == 2)
    print(
        f"VERIFY MUS CERT N={N}: witness C+={w_info['C_plus_ub']:.6f} (M_UB={M_UB:.4f}, BD_cap={bd_cap}) | "
        f"excluded_subsets={len(parsed_subsets)} (all 0-preimage verified, {total_nodes} nodes) | "
        f"feasibility(M<={claimed_lb_M:.4f}, C+<={math.sqrt(claimed_lb_M/(N+1)):.6f}) status={res.status}(INFEAS={ok_bound}) -> {'PASS' if ok_bound else 'FAIL'}"
    )
    return ok_bound


def verify_d2_cooley_tukey_cert(cert: dict, corrupt: bool = False) -> bool:
    """100% Independent Pure-NumPy Cold Verifier (ZERO Numba, ZERO shared solver code!)
    for `d2_cooley_tukey_cert`.

    Independently proves:
      1. Witness binary polynomial c (if present) via exact Taylor-Bernstein continuous supremum bracket.
      2. Stage 1 Completeness: sweeps ALL 2^(N/2 - 1) binary halves h in {-1,+1}^(N/2) (h[0]=+1) via
         pure NumPy float64 FFT and proves EVERY half omitted from `survivor_codes` strictly exceeds
         the unconditional Parallelogram/endpoint necessary bounds.
      3. Stage 2 Pairwise Refutation: sweeps ALL pairs (g_e, g_o) in S x S (up to exact D4 reversal
         symmetry max_sq[g_o] <= max_sq[g_e] + 1e-7) using conservative (+1e-5 margin) uint64 peak
         masks + exact float64 Parallelogram+cross-term refutation; for every rare coarse-grid survivor,
         proves exact Taylor-Bernstein continuous lower bound f_lo > claimed_LB_M!
    """
    t0 = time.time()
    N = int(cert["N"])
    if N % 2 != 0 or N < 4:
        print(f"FAIL: invalid even N={N}")
        return False
    M_half = N // 2
    G = int(cert["G"])
    n_f = G // 2 + 1
    claimed_lb_M = float(cert["certified_LB_M"])
    eps_safe = float(cert.get("eps_safe", 1e-6))

    witness = cert.get("witness_c")
    w_info = None
    if witness is not None:
        w_info = eval_certified_supremum_general(np.array(witness, dtype=np.int64))

    # Decode & hash-check survivor codes
    raw_bytes = zlib.decompress(base64.b64decode(cert["survivor_codes_zlib_b64"]))
    sha_got = hashlib.sha256(raw_bytes).hexdigest()
    if sha_got != cert["survivor_codes_sha256"]:
        print(f"FAIL: survivor_codes SHA256 mismatch ({sha_got} != {cert['survivor_codes_sha256']})")
        return False
    claimed_codes = np.frombuffer(raw_bytes, dtype=np.uint32).copy()
    if len(claimed_codes) != int(cert["n_survivors"]):
        print(f"FAIL: survivor_codes count mismatch ({len(claimed_codes)} != {cert['n_survivors']})")
        return False

    if corrupt:
        # Adversarial tamper: if witness exists, raise claimed_lb_M above true witness f_ub AND recompute
        # complete Stage-1 survivors so Stage 2 MUST catch the true witness (or if pure LB, drop 1 survivor
        # so Stage 1 completeness MUST fail!).
        if w_info is not None:
            claimed_lb_M = w_info["f_ub"] + 0.05
        else:
            claimed_codes = claimed_codes[1:]

    B_safe = math.sqrt(claimed_lb_M) + eps_safe
    M_safe = claimed_lb_M + eps_safe
    min_other = float(M_half % 2)
    max_abs_S = int(math.floor(B_safe - min_other + 1e-9))
    max_U_sq = claimed_lb_M - min_other * min_other + eps_safe

    # --- STAGE 1: Exhaustive pure-NumPy sweep of ALL 2^(M_half - 1) halves ---
    n_seq = 1 << (M_half - 1)
    shifts = np.arange(M_half - 1, dtype=np.uint32)
    alt_signs = np.array([1 if (m % 2 == 0) else -1 for m in range(M_half)], dtype=np.int32)
    req_list = []
    chunk = 16384
    for start in range(0, n_seq, chunk):
        end = min(n_seq, start + chunk)
        codes = np.arange(start, end, dtype=np.uint32)
        bits = ((codes[:, None] >> shifts[None, :]) & np.uint32(1)).astype(np.int32)
        H = np.empty((end - start, M_half), dtype=np.int32)
        H[:, 0] = 1
        H[:, 1:] = 2 * bits - 1
        absS = np.abs(np.sum(H, axis=1))
        U = np.sum(H * alt_signs[None, :], axis=1)
        U2 = U * U
        pre_ok = (absS <= max_abs_S) & (U2.astype(np.float64) <= max_U_sq)
        if not np.any(pre_ok):
            continue
        idx_pre = np.nonzero(pre_ok)[0]
        H_sub = H[idx_pre].astype(np.float64)
        spec = np.fft.rfft(H_sub, n=G, axis=1)
        # Note: rfft computes sum h[j] e^{-i 2 pi j l / G}; |conj| == |spec|!
        sq = spec.real * spec.real + spec.imag * spec.imag
        max_sq = np.max(sq, axis=1)
        surv = idx_pre[max_sq <= M_safe]
        if surv.size > 0:
            req_list.append(codes[surv])

    req_codes = np.concatenate(req_list) if req_list else np.empty(0, dtype=np.uint32)
    # Every required survivor MUST be present in claimed_codes!
    if corrupt and w_info is not None:
        # In witness-corrupt mode, feed complete req_codes to Stage 2 so we test Stage 2 refutation directly!
        claimed_codes = req_codes
    else:
        missing = np.setdiff1d(req_codes, claimed_codes, assume_unique=False)
        if missing.size > 0:
            print(f"FAIL: Stage 1 completeness violation! {missing.size} valid halves missing from survivor_codes!")
            return False

    t1 = time.time()

    # --- STAGE 2: Independent pure-NumPy pairwise Parallelogram + cross-term refutation ---
    S = len(claimed_codes)
    if S > 0:
        bits = ((claimed_codes[:, None] >> shifts[None, :]) & np.uint32(1)).astype(np.int32)
        H = np.empty((S, M_half), dtype=np.int32)
        H[:, 0] = 1
        H[:, 1:] = 2 * bits - 1
        absS = np.abs(np.sum(H, axis=1)).astype(np.int32)
        U = np.sum(H * alt_signs[None, :], axis=1)
        U2 = (U * U).astype(np.float64)

        # IMPORTANT: g(e^{+i theta}) = sum c_j e^{+i j theta} = conj(rfft(c))!
        # Let re = spec.real, im = -spec.imag so re + i*im = sum h[m] e^{+i 2*pi*m*l/G} identically!
        spec = np.fft.rfft(H.astype(np.float64), n=G, axis=1)
        re = spec.real
        im = -spec.imag
        sq = re * re + im * im
        maxsq = np.max(sq, axis=1)
        peakl = np.argmax(sq, axis=1).astype(np.int32)

        # Conservative (+1e-5 margin) 64-bit spectral peak masks on l = 0..min(64, n_f)-1
        nb = min(64, n_f)
        sq64 = sq[:, :nb]
        bit_w = (np.uint64(1) << np.arange(nb, dtype=np.uint64))[None, :]

        def make_mask(alpha: float) -> np.ndarray:
            thr = alpha * claimed_lb_M + 1e-5
            return np.sum(np.where(sq64 > thr, bit_w, np.uint64(0)), axis=1, dtype=np.uint64)

        m50 = make_mask(0.50)
        m60 = make_mask(0.60)
        m40 = make_mask(0.40)
        m70 = make_mask(0.70)
        m30 = make_mask(0.30)
        m80 = make_mask(0.80)
        m20 = make_mask(0.20)

        th_vec = math.pi * np.arange(n_f, dtype=np.float64) / G
        c_th = np.cos(th_vec)
        s_th = np.sin(th_vec)

        # Group by exact absS value so only s1 + s2 <= B_safe groups are compared!
        uniq_s = np.unique(absS)
        groups = {int(sv): np.nonzero(absS == sv)[0] for sv in uniq_s}

        coarse_refuted = 0
        total_mp = 0
        blk = 256
        for s1 in uniq_s:
            s1_i = int(s1)
            idx1_all = groups[s1_i]
            for s2 in uniq_s:
                s2_i = int(s2)
                if float(s1_i + s2_i) > B_safe:
                    continue
                idx2 = groups[s2_i]
                U2_b = U2[idx2]
                maxsq_b = maxsq[idx2]
                m50_b = m50[idx2]
                m60_b = m60[idx2]; m40_b = m40[idx2]
                m70_b = m70[idx2]; m30_b = m30[idx2]
                m80_b = m80[idx2]; m20_b = m20[idx2]

                for st in range(0, len(idx1_all), blk):
                    idx1 = idx1_all[st : st + blk]
                    alive = (
                        (maxsq_b[None, :] <= maxsq[idx1][:, None] + 1e-7)
                        & ((U2[idx1][:, None] + U2_b[None, :]) <= M_safe)
                        & ((m50[idx1][:, None] & m50_b[None, :]) == 0)
                    )
                    ia, ib = np.nonzero(alive)
                    if ia.size == 0:
                        continue
                    gi = idx1[ia]
                    gj = idx2[ib]
                    ok_m = (
                        ((m60[gi] & m40[gj])
                        | (m40[gi] & m60[gj])
                        | (m70[gi] & m30[gj])
                        | (m30[gi] & m70[gj])
                        | (m80[gi] & m20[gj])
                        | (m20[gi] & m80[gj])) == 0
                    )
                    if not np.any(ok_m):
                        continue
                    gi = gi[ok_m]
                    gj = gj[ok_m]
                    total_mp += int(gi.size)

                    # Fast check at peakl[gi] then peakl[gj]
                    for use_i in (True, False):
                        pk_arr = peakl[gi] if use_i else peakl[gj]
                        s_pk = sq[gi, pk_arr] + sq[gj, pk_arr]
                        A_pk = re[gi, pk_arr] * re[gj, pk_arr] + im[gi, pk_arr] * im[gj, pk_arr]
                        B_pk = im[gi, pk_arr] * re[gj, pk_arr] - re[gi, pk_arr] * im[gj, pk_arr]
                        v_pk = s_pk + 2.0 * np.abs(c_th[pk_arr] * A_pk + s_th[pk_arr] * B_pk)
                        keep = v_pk <= M_safe
                        if not np.any(keep):
                            gi = gi[:0]; gj = gj[:0]
                            break
                        gi = gi[keep]; gj = gj[keep]
                    if gi.size == 0:
                        continue

                    # Full 65-frequency vectorized check on remaining pairs
                    for l in range(n_f):
                        s_l = sq[gi, l] + sq[gj, l]
                        A_l = re[gi, l] * re[gj, l] + im[gi, l] * im[gj, l]
                        B_l = im[gi, l] * re[gj, l] - re[gi, l] * im[gj, l]
                        v_l = s_l + 2.0 * np.abs(c_th[l] * A_l + s_th[l] * B_l)
                        keep = v_l <= M_safe
                        if not np.any(keep):
                            gi = gi[:0]; gj = gj[:0]
                            break
                        gi = gi[keep]; gj = gj[keep]

                    # Any pair surviving the coarse G-grid MUST be refuted by exact continuous Taylor-Bernstein!
                    for k in range(gi.size):
                        c_full = np.empty(N, dtype=np.int64)
                        c_full[0::2] = H[gi[k]]
                        c_full[1::2] = H[gj[k]]
                        c_info = eval_certified_supremum_general(c_full)
                        if c_info["f_lo"] <= claimed_lb_M:
                            print(
                                f"FAIL: REALIZABLE COUNTEREXAMPLE FOUND! N={N} f_lo={c_info['f_lo']:.6f} <= claimed_LB_M={claimed_lb_M:.6f} "
                                f"(C+={c_info['C_plus_ub']:.6f})"
                            )
                            return False
                        coarse_refuted += 1
    else:
        total_mp = 0
        coarse_refuted = 0

    t2 = time.time()
    lb_cp = math.sqrt(claimed_lb_M / (N + 1.0))
    wit_s = f"witness C+={w_info['C_plus_ub']:.6f} (gap={w_info['C_plus_ub']-lb_cp:.6f})" if w_info else "pure_LB"
    print(
        f"VERIFY D2-CT CERT N={N:2d}: {wit_s} | Stage1={len(claimed_codes)}/{n_seq} halves ({t1-t0:.2f}s) | "
        f"Stage2 mp={total_mp} coarse_refuted={coarse_refuted} ({t2-t1:.2f}s) | LB_C+={lb_cp:.6f} -> PASS"
    )
    return True


def _np_canon_rev_codes(codes: np.ndarray, M_len: int) -> np.ndarray:
    """100% pure-NumPy exact D4-reversal canonical ID for h in {-1,+1}^{M_len} with h[0]=+1."""
    if M_len <= 1 or codes.size == 0:
        return np.zeros_like(codes, dtype=np.uint32)
    last_bit = (codes >> np.uint32(M_len - 2)) & np.uint32(1)
    rev = np.zeros_like(codes, dtype=np.uint32)
    for k in range(1, M_len):
        src_idx = M_len - 1 - k
        if src_idx == 0:
            src_bit = np.ones_like(codes, dtype=np.uint32)
        else:
            src_bit = (codes >> np.uint32(src_idx - 1)) & np.uint32(1)
        eq_bit = (src_bit == last_bit).astype(np.uint32)
        rev |= eq_bit << np.uint32(k - 1)
    return np.minimum(codes, rev)


def _np_stage1_sweep(M_len: int, M_other: int, claimed_lb_M: float, G: int, eps_safe: float, only_canon: bool) -> np.ndarray:
    """100% independent pure-NumPy exhaustive Stage-1 sweep over all 2^(M_len-1) halves via np.fft.rfft."""
    n_seq = 1 << (M_len - 1)
    B_safe = math.sqrt(claimed_lb_M) + eps_safe
    M_safe = claimed_lb_M + eps_safe
    min_other = float(M_other % 2)
    max_abs_S = int(math.floor(B_safe - min_other + 1e-9))
    max_U_sq = claimed_lb_M - min_other * min_other + eps_safe

    shifts = np.arange(M_len - 1, dtype=np.uint32)
    alt_signs = np.array([1 if (m % 2 == 0) else -1 for m in range(M_len)], dtype=np.int32)
    req_list = []
    chunk = 32768
    for start in range(0, n_seq, chunk):
        end = min(n_seq, start + chunk)
        codes = np.arange(start, end, dtype=np.uint32)
        bits = ((codes[:, None] >> shifts[None, :]) & np.uint32(1)).astype(np.int32)
        H = np.empty((end - start, M_len), dtype=np.int32)
        H[:, 0] = 1
        H[:, 1:] = 2 * bits - 1
        absS = np.abs(np.sum(H, axis=1))
        U = np.sum(H * alt_signs[None, :], axis=1)
        U2 = U * U
        pre_ok = (absS <= max_abs_S) & (U2.astype(np.float64) <= max_U_sq)
        if only_canon:
            idx_c = np.nonzero(pre_ok)[0]
            if idx_c.size == 0:
                continue
            can_sub = _np_canon_rev_codes(codes[idx_c], M_len)
            idx_pre = idx_c[can_sub == codes[idx_c]]
        else:
            idx_pre = np.nonzero(pre_ok)[0]
        if idx_pre.size == 0:
            continue
        spec = np.fft.rfft(H[idx_pre].astype(np.float64), n=G, axis=1)
        sq = spec.real * spec.real + spec.imag * spec.imag
        surv = idx_pre[np.max(sq, axis=1) <= M_safe]
        if surv.size > 0:
            req_list.append(codes[surv])
    return np.concatenate(req_list) if req_list else np.empty(0, dtype=np.uint32)


def _np_decode_halves(codes: np.ndarray, M_len: int) -> np.ndarray:
    shifts = np.arange(M_len - 1, dtype=np.uint32)
    bits = ((codes[:, None] >> shifts[None, :]) & np.uint32(1)).astype(np.int32)
    H = np.empty((codes.size, M_len), dtype=np.int32)
    H[:, 0] = 1
    H[:, 1:] = 2 * bits - 1
    return H


def verify_d2_cooley_tukey_v3_cert(cert: dict, corrupt: bool = False) -> bool:
    """100% independent pure-NumPy verifier for Engine 3 even & odd d=2 Cooley-Tukey certificates
    (ZERO Numba, ZERO shared solver code). Verifies:
      1. Witness continuous Taylor-Bernstein bracket (if present).
      2. SHA-256 integrity + exhaustive Stage-1 completeness via np.fft.rfft.
      3. Exhaustive Stage-2 refutation via vectorized pure-NumPy 2D-cell Phase-Projection bitsets +
         exact G-grid cross-term + Taylor-Bernstein continuous bracket on every coarse survivor!
    """
    t0 = time.time()
    N = int(cert["N"])
    is_even = (N % 2 == 0)
    M_e = (N + 1) // 2
    M_o = N // 2
    G = int(cert["G"])
    n_f = G // 2 + 1
    claimed_lb_M = float(cert["certified_LB_M"])
    eps_safe = float(cert.get("eps_safe", 1e-6))

    witness = cert.get("witness_c")
    w_info = None
    if witness is not None:
        w_info = eval_certified_supremum_general(np.array(witness, dtype=np.int64))

    # Decode & SHA256-verify embedded survivor code sets (if present)
    def load_codes(b64_key: str, sha_key: str, n_key: str):
        b64_val = cert.get(b64_key)
        expected_n = int(cert[n_key])
        expected_sha = cert[sha_key]
        if b64_val is None:
            return None, expected_n, expected_sha
        raw = zlib.decompress(base64.b64decode(b64_val))
        got_sha = hashlib.sha256(raw).hexdigest()
        if got_sha != expected_sha:
            print(f"FAIL: {sha_key} mismatch ({got_sha} != {expected_sha})")
            return False, expected_n, expected_sha
        arr = np.frombuffer(raw, dtype=np.uint32).copy()
        if arr.size != expected_n:
            print(f"FAIL: {n_key} mismatch ({arr.size} != {expected_n})")
            return False, expected_n, expected_sha
        return arr, expected_n, expected_sha

    if is_even:
        e_claimed, e_exp_n, e_exp_sha = load_codes("survivor_codes_zlib_b64", "survivor_codes_sha256", "n_survivors")
        if e_claimed is False:
            return False
        o_claimed, o_exp_n, o_exp_sha = e_claimed, e_exp_n, e_exp_sha
    else:
        e_claimed, e_exp_n, e_exp_sha = load_codes("survivor_e_zlib_b64", "survivor_e_sha256", "n_survivors_e_canon")
        o_claimed, o_exp_n, o_exp_sha = load_codes("survivor_o_zlib_b64", "survivor_o_sha256", "n_survivors_o")
        if e_claimed is False or o_claimed is False:
            return False

    if corrupt:
        if w_info is not None:
            claimed_lb_M = w_info["f_ub"] + 0.05
        else:
            if e_claimed is not None and e_claimed.size > 0:
                e_claimed = e_claimed[1:]
            else:
                claimed_lb_M += 5.0

    # --- STAGE 1: Exhaustive independent pure-NumPy sweep ---
    e_req = _np_stage1_sweep(M_e, M_o, claimed_lb_M, G, eps_safe, only_canon=(not is_even))
    if is_even:
        o_req = e_req
    else:
        o_req = _np_stage1_sweep(M_o, M_e, claimed_lb_M, G, eps_safe, only_canon=False)

    if corrupt and w_info is not None:
        e_use = e_req
        o_use = o_req
    else:
        if e_claimed is not None:
            miss_e = np.setdiff1d(e_req, e_claimed, assume_unique=False)
            if miss_e.size > 0:
                print(f"FAIL: Stage-1 e completeness violation! {miss_e.size} valid halves missing!")
                return False
            e_use = e_claimed
        else:
            # Verify recomputed set matches certified count & SHA256!
            e_sorted = np.sort(e_req)
            if e_sorted.size != e_exp_n or hashlib.sha256(e_sorted.tobytes()).hexdigest() != e_exp_sha:
                print(f"FAIL: Stage-1 e recomputed SHA256/count mismatch ({e_sorted.size} vs {e_exp_n})!")
                return False
            e_use = e_sorted

        if is_even:
            o_use = e_use
        else:
            if o_claimed is not None:
                miss_o = np.setdiff1d(o_req, o_claimed, assume_unique=False)
                if miss_o.size > 0:
                    print(f"FAIL: Stage-1 o completeness violation! {miss_o.size} valid halves missing!")
                    return False
                o_use = o_claimed
            else:
                o_sorted = np.sort(o_req)
                if o_sorted.size != o_exp_n or hashlib.sha256(o_sorted.tobytes()).hexdigest() != o_exp_sha:
                    print(f"FAIL: Stage-1 o recomputed SHA256/count mismatch ({o_sorted.size} vs {o_exp_n})!")
                    return False
                o_use = o_sorted

    t1 = time.time()

    # --- STAGE 2: Independent Pure-NumPy 2D-Cell Phase-Projection Bitset Refutation ---
    B_bound = math.sqrt(claimed_lb_M)
    B_safe = B_bound + eps_safe
    M_safe = claimed_lb_M + eps_safe
    margin_B = 1e-4

    th_vec = math.pi * np.arange(n_f, dtype=np.float64) / G
    c_th = np.cos(th_vec)
    s_th = np.sin(th_vec)
    stride = max(1, G // 64)
    sub_ls = np.arange(0, n_f, stride, dtype=np.int32)
    n_sub = sub_ls.size  # 33
    n_axes = 4
    phis = math.pi * np.arange(n_axes, dtype=np.float64) / n_axes
    c_ax = np.cos(phis)
    s_ax = np.sin(phis)
    e_thr = np.array([0.84, 0.74, 0.62, 0.50, 0.38, 0.26], dtype=np.float64) * B_bound + margin_B
    o_lim = np.array([0.16, 0.26, 0.38, 0.50, 0.62, 0.74], dtype=np.float64) * B_bound + margin_B
    n_lev = 6
    n_proj_c = n_sub * n_axes * n_lev

    def extract_meta(codes: np.ndarray, M_len: int, need_cids: bool, K_V: int = 24):
        S = codes.size
        absS = np.empty(S, dtype=np.int16)
        absU = np.empty(S, dtype=np.int16)
        canon = _np_canon_rev_codes(codes, M_len)
        cids = np.full((S, K_V), -1, dtype=np.int16) if need_cids else None
        alt_s = np.array([1 if (m % 2 == 0) else -1 for m in range(M_len)], dtype=np.int32)
        blk = 16384
        for st in range(0, S, blk):
            en = min(st + blk, S)
            H = _np_decode_halves(codes[st:en], M_len)
            absS[st:en] = np.abs(np.sum(H, axis=1)).astype(np.int16)
            absU[st:en] = np.abs(np.sum(H * alt_s[None, :], axis=1)).astype(np.int16)
            if need_cids:
                spec = np.fft.rfft(H.astype(np.float64), n=G, axis=1)
                re_sub = spec.real[:, sub_ls]
                im_sub = -spec.imag[:, sub_ls]  # g(e^{+i theta}) = conj(rfft)
                # (B, n_sub, n_axes)
                P = np.abs(re_sub[:, :, None] * c_ax[None, None, :] + im_sub[:, :, None] * s_ax[None, None, :])
                P_flat = P.reshape(en - st, n_sub * n_axes)
                # Pick top K_V largest projections per row via argpartition!
                top_idx = np.argpartition(-P_flat, K_V - 1, axis=1)[:, :K_V]
                rows_r = np.arange(en - st)[:, None]
                top_val = P_flat[rows_r, top_idx]
                # Sort top K_V descending so tightest constraints come FIRST!
                ord_k = np.argsort(-top_val, axis=1)
                top_idx = top_idx[rows_r, ord_k]
                top_val = top_val[rows_r, ord_k]
                # Map each top_val to tightest triggered level 0..5 (or -1 if <= e_thr[5])
                levs = np.full((en - st, K_V), -1, dtype=np.int16)
                for lv in range(n_lev - 1, -1, -1):
                    levs = np.where(top_val > e_thr[lv], lv, levs)
                cids[st:en] = np.where(levs >= 0, top_idx * n_lev + levs, -1).astype(np.int16)
        return absS, absU, canon, cids

    K_V = 36
    e_absS, e_absU, e_canon, e_cids = extract_meta(e_use, M_e, need_cids=True, K_V=K_V)
    if is_even:
        o_absS, o_absU, o_canon = e_absS, e_absU, e_canon
    else:
        o_absS, o_absU, o_canon, _ = extract_meta(o_use, M_o, need_cids=False)

    # Group into 2D cells (absS, absU) sorted by canon_id
    def group_cells(codes, absS, absU, canon, cids=None):
        cells = {}
        pairs_su = np.unique(np.stack([absS, absU], axis=1), axis=0)
        for sv, uv in pairs_su:
            idx = np.nonzero((absS == sv) & (absU == uv))[0]
            ord_c = np.argsort(canon[idx], kind="stable")
            idx = idx[ord_c]
            cells[(int(sv), int(uv))] = (
                codes[idx],
                canon[idx],
                cids[idx] if cids is not None else None,
            )
        return cells

    e_cells = group_cells(e_use, e_absS, e_absU, e_canon, e_cids)
    o_cells = e_cells if is_even else group_cells(o_use, o_absS, o_absU, o_canon, None)
    e_keys = sorted(e_cells.keys())
    o_keys = sorted(o_cells.keys())

    TILE_J = 8192  # 128 uint64 words
    coarse_refuted = 0
    total_cand = 0

    for (sj, uj) in o_keys:
        # Check if any compatible e-cell exists
        compat_ei = []
        for (si, ui) in e_keys:
            if is_even and (si, ui) < (sj, uj):
                continue
            if float(si + sj) <= B_safe and float(ui * ui + uj * uj) <= M_safe:
                compat_ei.append((si, ui))
        if not compat_ei:
            continue

        o_codes_c, o_can_c, _ = o_cells[(sj, uj)]
        n_oc = o_codes_c.size

        for j_st in range(0, n_oc, TILE_J):
            j_en = min(j_st + TILE_J, n_oc)
            t_len = j_en - j_st
            pad_len = ((t_len + 63) // 64) * 64
            n_w = pad_len // 64

            H_j = _np_decode_halves(o_codes_c[j_st:j_en], M_o)
            spec_j = np.fft.rfft(H_j.astype(np.float64), n=G, axis=1)
            re_j = spec_j.real
            im_j = -spec_j.imag
            sq_j = re_j * re_j + im_j * im_j

            # Build allow_tile (n_proj_c + 1, n_w) uint64 via pure-NumPy packbits!
            # Row n_proj_c is all-ones (sentinel for cid == -1)!
            re_js = re_j[:, sub_ls]
            im_js = im_j[:, sub_ls]
            wr = re_js * c_th[None, sub_ls] - im_js * s_th[None, sub_ls]
            wi = re_js * s_th[None, sub_ls] + im_js * c_th[None, sub_ls]
            # Po shape: (t_len, n_sub, n_axes) -> transpose to (n_sub, n_axes, t_len)
            Po = np.abs(wr[:, :, None] * c_ax[None, None, :] + wi[:, :, None] * s_ax[None, None, :])
            Po_T = np.transpose(Po, (1, 2, 0))  # (n_sub, n_axes, t_len)

            allow_bool = np.zeros((n_proj_c + 1, pad_len), dtype=np.uint8)
            allow_bool[n_proj_c, :t_len] = 1
            for lv in range(n_lev):
                allow_bool[lv:n_proj_c:n_lev, :t_len] = (Po_T <= o_lim[lv]).reshape(n_sub * n_axes, t_len)
            allow_tile = np.packbits(allow_bool, axis=1, bitorder="little").view(np.uint64)

            for (si, ui) in compat_ei:
                e_codes_c, e_can_c, e_cids_c = e_cells[(si, ui)]
                same_cell = is_even and ((si, ui) == (sj, uj))
                if same_cell:
                    i_lo = int(np.searchsorted(e_can_c, o_can_c[j_st], side="left"))
                else:
                    i_lo = 0
                n_ec = e_codes_c.size
                if i_lo >= n_ec:
                    continue

                # Map cid == -1 -> sentinel n_proj_c (all-valid-bits mask!)
                cids_sub = np.where(e_cids_c[i_lo:n_ec] >= 0, e_cids_c[i_lo:n_ec], n_proj_c)
                codes_sub = e_codes_c[i_lo:n_ec]
                can_sub = e_can_c[i_lo:n_ec]

                B_I = 128
                for bi_st in range(0, codes_sub.size, B_I):
                    bi_en = min(bi_st + B_I, codes_sub.size)
                    C_blk = cids_sub[bi_st:bi_en]  # (B, K_V)
                    # Stage A: 8-constraint vectorized uint64 AND across tile!
                    m = (
                        allow_tile[C_blk[:, 0]]
                        & allow_tile[C_blk[:, 1]]
                        & allow_tile[C_blk[:, 2]]
                        & allow_tile[C_blk[:, 3]]
                        & allow_tile[C_blk[:, 4]]
                        & allow_tile[C_blk[:, 5]]
                        & allow_tile[C_blk[:, 6]]
                        & allow_tile[C_blk[:, 7]]
                    )
                    ri, rw = np.nonzero(m)
                    if ri.size == 0:
                        continue
                    # Stage B: apply remaining K_V - 8 constraints ONLY on nonzero (row, word)!
                    mv = m[ri, rw]
                    for k in range(8, K_V):
                        mv &= allow_tile[C_blk[ri, k], rw]
                        nz = mv != 0
                        if not np.any(nz):
                            ri = ri[:0]; rw = rw[:0]; mv = mv[:0]
                            break
                        ri = ri[nz]; rw = rw[nz]; mv = mv[nz]
                    if ri.size == 0:
                        continue

                    # Unpack set bits into candidate pairs (i_local, dj)
                    pair_i = []
                    pair_dj = []
                    for idx_p in range(ri.size):
                        val = int(mv[idx_p])
                        r_loc = int(ri[idx_p])
                        w_loc = int(rw[idx_p])
                        while val:
                            lsb = val & -val
                            bpos = lsb.bit_length() - 1
                            dj = (w_loc << 6) + bpos
                            if dj < t_len:
                                if (not same_cell) or (o_can_c[j_st + dj] <= can_sub[bi_st + r_loc]):
                                    pair_i.append(r_loc)
                                    pair_dj.append(dj)
                            val ^= lsb
                    if not pair_i:
                        continue

                    pi_arr = np.array(pair_i, dtype=np.int32)
                    pdj_arr = np.array(pair_dj, dtype=np.int32)
                    total_cand += pi_arr.size

                    # Compute exact DFT ONLY for distinct surviving i's in this mini-batch!
                    uniq_i, inv_i = np.unique(pi_arr, return_inverse=True)
                    H_i = _np_decode_halves(codes_sub[bi_st + uniq_i], M_e)
                    spec_i = np.fft.rfft(H_i.astype(np.float64), n=G, axis=1)
                    re_i = spec_i.real
                    im_i = -spec_i.imag
                    sq_i = re_i * re_i + im_i * im_i

                    # Full G-grid cross-term check on (inv_i, pdj_arr)
                    gi = inv_i
                    gj = pdj_arr
                    for l in range(n_f):
                        s_l = sq_i[gi, l] + sq_j[gj, l]
                        A_l = re_i[gi, l] * re_j[gj, l] + im_i[gi, l] * im_j[gj, l]
                        B_l = im_i[gi, l] * re_j[gj, l] - re_i[gi, l] * im_j[gj, l]
                        v_l = s_l + 2.0 * np.abs(c_th[l] * A_l + s_th[l] * B_l)
                        keep = v_l <= M_safe
                        if not np.any(keep):
                            gi = gi[:0]; gj = gj[:0]
                            break
                        gi = gi[keep]; gj = gj[keep]

                    for k in range(gi.size):
                        c_full = np.empty(N, dtype=np.int64)
                        c_full[0::2] = H_i[gi[k]]
                        c_full[1::2] = H_j[gj[k]]
                        c_info = eval_certified_supremum_general(c_full)
                        if c_info["f_lo"] <= claimed_lb_M:
                            print(
                                f"FAIL: REALIZABLE COUNTEREXAMPLE FOUND! N={N} f_lo={c_info['f_lo']:.6f} <= "
                                f"claimed_LB_M={claimed_lb_M:.6f} (C+={c_info['C_plus_ub']:.6f})"
                            )
                            return False
                        coarse_refuted += 1

    t2 = time.time()
    lb_cp = math.sqrt(claimed_lb_M / (N + 1.0))
    wit_s = f"witness C+={w_info['C_plus_ub']:.6f} (gap={w_info['C_plus_ub']-lb_cp:.6f})" if w_info else "pure_LB"
    print(
        f"VERIFY D2-V3 CERT N={N:2d} ({'EVEN' if is_even else 'ODD '}): {wit_s} | "
        f"Stage1 |S_e|={e_use.size:,d} |S_o|={o_use.size:,d} ({t1-t0:.2f}s) | "
        f"Stage2 cand={total_cand:,d} coarse_refuted={coarse_refuted} ({t2-t1:.2f}s) | LB_C+={lb_cp:.6f} -> PASS"
    )
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cert", help="Path to Dual-DAG certificate JSON")
    ap.add_argument("--corrupt", action="store_true", help="Adversarial corruption check (must exit rc=1)")
    args = ap.parse_args()

    with open(args.cert) as f:
        cert = json.load(f)

    ctype = cert.get("type", "r_space_conflict_cert")
    if ctype == "r_space_conflict_cert":
        ok = verify_r_space_conflict_cert(cert, corrupt=args.corrupt)
        sys.exit(0 if ok else 1)
    elif ctype == "r_space_mus_cert":
        ok = verify_r_space_mus_cert(cert, corrupt=args.corrupt)
        sys.exit(0 if ok else 1)
    elif ctype == "d2_cooley_tukey_cert":
        if int(cert.get("schema_v", 2)) >= 3:
            ok = verify_d2_cooley_tukey_v3_cert(cert, corrupt=args.corrupt)
        else:
            ok = verify_d2_cooley_tukey_cert(cert, corrupt=args.corrupt)
        sys.exit(0 if ok else 1)
    elif ctype == "d2_cooley_tukey_odd_cert":
        ok = verify_d2_cooley_tukey_v3_cert(cert, corrupt=args.corrupt)
        sys.exit(0 if ok else 1)
    elif ctype == "witness_exact":
        c = np.array(cert["coefficients"], dtype=np.int64)
        if args.corrupt:
            c[0] = 0
        try:
            info = eval_certified_supremum_general(c)
            print(f"VERIFY WITNESS N={info['N']}: C+ in [{info['C_plus_lo']:.9f}, {info['C_plus_ub']:.9f}] E4={info['E4']} PASS")
            sys.exit(0)
        except Exception as e:
            print(f"FAIL: {e}")
            sys.exit(1)
    else:
        print(f"FAIL: unknown cert type {ctype}")
        sys.exit(1)


if __name__ == "__main__":
    main()

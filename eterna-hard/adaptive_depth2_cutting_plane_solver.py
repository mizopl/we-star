#!/usr/bin/env python3
"""
Adaptive Depth-2 Boundary-Expansion & Coupled Multi-Defect Cutting-Plane Solver
(`adaptive_depth2_cutting_plane_solver.py`)
Campaign: V20-02B (`eterna-hard`, Bet `L-EVVA-012`)

Implements the 4 `[L0-ALGO]` upgrades with `< 0.5 s` `CLSS-1` per-window complexity:
  1. `Law R11` (`2-Stage Depth-2 Expanded Window W_2`):
     - `Stage 1`: `w1_pairs[:3]` x `w1_unp[:2]` (`<= 3,456` states) scored against `<= 4` core rivals (`< 0.12 s`).
     - `Stage 2`: top `B_1 <= 128` states from `W_1` crossed with `d2_pairs[:2]` x `d2_unp[:2]`
       (`<= 2,048` joint states in `states_W2`) scored against `<= 6` initial rivals (`< 0.15 s`).
  2. `Fold-Even-At-Zero` + `Cross-Window External Stem Re-Orthogonalization` (`Law R5`) +
     `Non-Adjacent Multi-Donor Kempe Repair` (`Law R8`, `abs(u_d1 - u_d2) >= 3`):
     - In `Stage 3` (`max_cp_steps = 18`), folds up to 3 Kempe-repaired candidates per step,
       never breaking before folding at `w_b == 0.0`, and triggers external stem re-orthogonalization
       when `w_b <= 0.05` (`reo_calls < 2`, `max_steps = 4`, `max_cands = 12`).
  3. `Law R9` (`Coupled 2-Defect & 1-nt Slip Window`):
     - Jointly optimizes coupled missing pairs + extra-pair endpoints + their depth-1/depth-2 neighbors.
  4. `Law R12` (`Homologous Repeated-Motif & Whole-Stem Chirality Inversion`):
     - In `reorthogonalize_external_stems`, simultaneously flips `2..4` contiguous/bulge-connected
       pairs of the external stem (`CG<->GC`, `AU<->UA`, `GU<->UG`) and pre-filters any internal
       bulge/closing unpaired base via `RNA.energy_of_struct` so the external motif preserves its
       stacking stability while destroying cross-branch duplex complementarity.
"""

import argparse
import concurrent.futures as cf
import csv
import itertools
import json
import os
import random
import subprocess
import time
import RNA

import cegis_eterna_hard_solver as S

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_BIN = sys.executable
CHECK_DESIGN = os.path.join(BASE_DIR, "eterna-validator/check_design.py")


def build_local_slip_struct(target_s: str, pair_of_arr: list, close_uvs: tuple, extra_open_uvs: tuple):
    s_lst = list(target_s)
    for u_op, v_op in extra_open_uvs:
        s_lst[u_op] = "."
        s_lst[v_op] = "."
    for x_c, y_c in close_uvs:
        if x_c >= y_c or y_c - x_c <= 3:
            return None
        for end_p in (x_c, y_c):
            q_p = pair_of_arr[end_p]
            if q_p != -1:
                s_lst[end_p] = "."
                s_lst[q_p] = "."
    for x_c, y_c in close_uvs:
        if s_lst[x_c] != "." or s_lst[y_c] != ".":
            return None
        bal = 0
        for k_b in range(x_c + 1, y_c):
            if s_lst[k_b] == "(":
                bal += 1
            elif s_lst[k_b] == ")":
                bal -= 1
                if bal < 0:
                    return None
        if bal != 0:
            return None
        s_lst[x_c] = "("
        s_lst[y_c] = ")"
    return "".join(s_lst)


def collect_external_motif_cluster(uv_seed: tuple, pinfo: dict, prot_W2: set) -> tuple:
    """
    `Law R12` Helper: Starting from an external target pair `uv_seed = (u_e, v_e)` outside `prot_W2`,
    collects up to 4 connected target pairs in the same stem/bulge motif (stepping across `<= 1` nt
    bulges) and up to 2 adjacent unpaired bulge/closing bases.
    """
    pair_of = pinfo["pair_of"]
    locked_pos = pinfo["locked_pos"]
    n = pinfo["n"]
    cluster_pairs = [uv_seed]
    cluster_unp = []

    # Walk inward and outward from `uv_seed` across `<= 1` nt bulges
    curr_u, curr_v = uv_seed
    for _ in range(3):
        found_next = False
        for du in (1, 2):
            for dv in (1, 2):
                if du + dv > 3:
                    continue
                nu, nv = curr_u + du, curr_v - dv
                if nu < nv and 0 <= nu < n and 0 <= nv < n and pair_of[nu] == nv:
                    uv_n = (nu, nv)
                    if uv_n[0] not in prot_W2 and uv_n[1] not in prot_W2 and uv_n not in cluster_pairs:
                        cluster_pairs.append(uv_n)
                        if du == 2 and (curr_u + 1) not in locked_pos and (curr_u + 1) not in prot_W2:
                            cluster_unp.append(curr_u + 1)
                        if dv == 2 and (curr_v - 1) not in locked_pos and (curr_v - 1) not in prot_W2:
                            cluster_unp.append(curr_v - 1)
                        curr_u, curr_v = nu, nv
                        found_next = True
                        break
            if found_next:
                break
        if not found_next or len(cluster_pairs) >= 4:
            break

    curr_u, curr_v = uv_seed
    for _ in range(3):
        if len(cluster_pairs) >= 4:
            break
        found_prev = False
        for du in (1, 2):
            for dv in (1, 2):
                if du + dv > 3:
                    continue
                nu, nv = curr_u - du, curr_v + dv
                if nu < nv and 0 <= nu < n and 0 <= nv < n and pair_of[nu] == nv:
                    uv_n = (nu, nv)
                    if uv_n[0] not in prot_W2 and uv_n[1] not in prot_W2 and uv_n not in cluster_pairs:
                        cluster_pairs.append(uv_n)
                        if du == 2 and (curr_u - 1) not in locked_pos and (curr_u - 1) not in prot_W2:
                            cluster_unp.append(curr_u - 1)
                        if dv == 2 and (curr_v + 1) not in locked_pos and (curr_v + 1) not in prot_W2:
                            cluster_unp.append(curr_v + 1)
                        curr_u, curr_v = nu, nv
                        found_prev = True
                        break
            if found_prev:
                break
        if not found_prev:
            break

    return cluster_pairs[:4], cluster_unp[:2]


def lock_seam_anchor_in_pinfo(pinfo: dict, seq_anchor: str, prot_W2: set) -> dict:
    """
    `Law R18b` (Inside-Out Seam-First Hard Anchor Lock):
    Returns a shallow copy of `pinfo` with all positions in `prot_W2` (and their target pair mates)
    hard-locked to `seq_anchor`, allowing Global Multi-Stem CEGIS (`cegis_rival_minimax_pass` +
    `fast_mfe_seam_climber`) to re-color all external stems (`Priority 1–3`) around the locked seam.
    """
    pinfo_seam = dict(pinfo)
    locked_pos = dict(pinfo["locked_pos"])
    allowed_pairs = dict(pinfo["allowed_pairs"])
    pair_of = pinfo["pair_of"]
    full_prot = set(prot_W2)
    for p in list(prot_W2):
        if 0 <= p < len(pair_of) and pair_of[p] != -1:
            full_prot.add(pair_of[p])
    for p in full_prot:
        locked_pos[p] = seq_anchor[p]
    for u, v in pinfo["pairs"]:
        if u in full_prot or v in full_prot:
            allowed_pairs[(u, v)] = (seq_anchor[u] + seq_anchor[v],)
    pinfo_seam["locked_pos"] = locked_pos
    pinfo_seam["allowed_pairs"] = allowed_pairs
    pinfo_seam["active_unpaired"] = [u for u in pinfo["active_unpaired"] if u not in full_prot]
    pinfo_seam["passive_unpaired"] = set(pinfo["passive_unpaired"]) - full_prot
    return pinfo_seam


def reorthogonalize_external_stems(
    seq_in: str,
    ms_in: str,
    pinfo: dict,
    prot_W2: set,
    req_bps: list,
    eng: int,
    rng: random.Random,
    init_rivals: list,
    deadline: float,
    max_steps: int = 10,
    max_cands: int = 14,
) -> tuple:
    """
    `Law R5` + `Law R12` + `Law R18a` + `Law R19a` External Stem & Homologous Motif Re-Orthogonalization:
    When `ms_in` has extra pairs `(x, y)` outside `prot_W2` (a cross-window parasitic duplex),
    tests:
      1. `Law R19a`: Whole-Stem Chirality Reflection (`GC<->CG, AU<->UA, GU<->UG` across an entire external
         stem `S_m`, its interior pairs `S_m[1:]` preserving multiloop dangles, and pairwise stem combinations
         `S_{m_1} + S_{m_2}`).
      2. `Law R12`: Simultaneous chirality inversion of `2..4` pairs in external stem/bulge clusters.
      3. `Law R5`: Single/double pair flips and unpaired base anti-slip mutations (including joint 2-base
         non-pairing assignments on unpaired-unpaired intra-loop slips `(x, y)`).
      4. `Law R18a`: Separates the active cutting-plane iterate `(w_seq, w_ms, w_bps, w_dbp, w_de)` from
         `best_incumbent = (inc_key, inc_seq, inc_ms, inc_dbp, inc_de)` so multi-stem duplex cascades
         (`S_{m_1} -> S_{m_2} -> S_{m_3}`) unpeel monotonically across steps without aborting at step 0.
    """
    target = pinfo["target"]
    t_bps = S.get_bp_set(target)
    pair_of = pinfo["pair_of"]
    allowed_pairs = pinfo["allowed_pairs"]
    locked_pos = pinfo["locked_pos"]
    n = pinfo["n"]
    cur_vb = S.budget_violation(seq_in, pinfo)

    # Precompute contiguous target stems for Law R19a Whole-Stem Reflection
    stem_of_uv = {}
    for u, v in pinfo["pairs"]:
        if u == 0 or pair_of[u - 1] != v + 1:
            st_uvs = []
            k = 0
            while u + k < v - k and pair_of[u + k] == v - k:
                uv_k = (u + k, v - k)
                st_uvs.append(uv_k)
                k += 1
            st_tup = tuple(st_uvs)
            for uv_k in st_tup:
                stem_of_uv[uv_k] = st_tup

    # `Law R21a`: Precompute `1x1`-connected stem cascades (`du == 1, dv == 1` or `du == 2, dv == 2` across `1x1` loops)
    cascade11_of_uv = {}
    for u, v in pinfo["pairs"]:
        has_outer_cas = (u > 0 and pair_of[u - 1] == v + 1) or (
            u >= 2 and v + 2 < n and pair_of[u - 2] == v + 2 and pair_of[u - 1] == -1 and pair_of[v + 1] == -1
        )
        if not has_outer_cas:
            cas_uvs = [(u, v)]
            cas_u11 = []
            cu, cv = u, v
            while True:
                if cu + 1 < cv - 1 and pair_of[cu + 1] == cv - 1:
                    cu, cv = cu + 1, cv - 1
                    cas_uvs.append((cu, cv))
                elif (
                    cu + 2 < cv - 2
                    and pair_of[cu + 2] == cv - 2
                    and pair_of[cu + 1] == -1
                    and pair_of[cv - 1] == -1
                ):
                    cas_u11.append((cu + 1, cv - 1))
                    cu, cv = cu + 2, cv - 2
                    cas_uvs.append((cu, cv))
                else:
                    break
            if len(cas_uvs) >= 2:
                cas_tup = (tuple(cas_uvs), tuple(cas_u11))
                for uv_k in cas_uvs:
                    cascade11_of_uv[uv_k] = cas_tup

    w_seq = seq_in
    w_ms = ms_in
    w_bps = S.get_bp_set(w_ms)
    w_dbp = len(t_bps ^ w_bps)
    w_de = round(float(RNA.energy_of_struct(w_seq, target)) - float(RNA.energy_of_struct(w_seq, w_ms)), 4)

    ext_rivals = []
    for r_s in init_rivals:
        if r_s and r_s not in ext_rivals:
            ext_rivals.append(r_s)
    if w_ms not in ext_rivals:
        ext_rivals.append(w_ms)

    def eval_ext_rivals_worst(seq_c: str, et_c: float, r_list: list) -> float:
        worst_val = -999.0
        for r_e in r_list:
            extra_re = S.get_bp_set(r_e) - t_bps
            if extra_re and not all((seq_c[x] + seq_c[y]) in S.VALID_SET for x, y in extra_re):
                continue
            d_re = round(et_c - float(RNA.energy_of_struct(seq_c, r_e)), 4)
            if d_re > worst_val:
                worst_val = d_re
        return worst_val if worst_val > -900.0 else 0.0

    w_et0 = float(RNA.energy_of_struct(w_seq, target))
    w_worst0 = eval_ext_rivals_worst(w_seq, w_et0, ext_rivals[-6:])
    inc_key = (
        sum(1 for uv_r in req_bps if uv_r not in w_bps),
        w_dbp if w_dbp <= 4 else len(w_bps - t_bps),
        w_dbp,
        max(0.0, w_worst0),
        w_de,
    )
    inc_seq, inc_ms, inc_dbp, inc_de = w_seq, w_ms, w_dbp, w_de
    primary_req = req_bps[0] if req_bps else None

    for _step in range(max_steps):
        if time.time() >= deadline:
            break
        extra = sorted(w_bps - t_bps)
        ext_extra = [(x, y) for x, y in extra if x not in prot_W2 or y not in prot_W2]
        ext_miss = [(u, v) for u, v in sorted(t_bps - w_bps) if u not in prot_W2 and v not in prot_W2]
        if not ext_extra and not ext_miss:
            break
        w_lst = list(w_seq)
        pure_flips = []
        other_flips = []
        seen_uv = set()
        unp_edits = []
        seen_unp = set()
        direct_extra_uvs = []
        unp_unp_slips = []

        for x, y in ext_extra:
            if pair_of[x] == -1 and pair_of[y] == -1:
                unp_unp_slips.append((x, y))
            for z, w in ((x, y), (y, x)):
                if pair_of[z] == -1 and z not in locked_pos and z not in prot_W2 and z not in seen_unp:
                    seen_unp.add(z)
                    for ch_new in ("A", "C", "U", "G"):
                        if ch_new != w_lst[z] and (w_lst[w] + ch_new) not in S.VALID_SET:
                            if S.has_symmetric_neck_zip(z, ch_new, w_lst, pair_of, n):
                                continue
                            unp_edits.append((z, ch_new))
                elif pair_of[z] != -1:
                    uv_d = (min(z, pair_of[z]), max(z, pair_of[z]))
                    if uv_d[0] not in prot_W2 and uv_d[1] not in prot_W2 and uv_d not in direct_extra_uvs:
                        direct_extra_uvs.append(uv_d)
                    for dz in (0, -1, 1, -2, 2):
                        zn = z + dz
                        if 0 <= zn < n and pair_of[zn] != -1:
                            uv_s = (min(zn, pair_of[zn]), max(zn, pair_of[zn]))
                            if uv_s not in seen_uv and uv_s[0] not in prot_W2 and uv_s[1] not in prot_W2:
                                seen_uv.add(uv_s)
                                cur_bp = w_lst[uv_s[0]] + w_lst[uv_s[1]]
                                flip_bp = cur_bp[1] + cur_bp[0]
                                if flip_bp != cur_bp and flip_bp in allowed_pairs[uv_s]:
                                    pure_flips.append((uv_s, flip_bp))
                                for cand_bp in ("CG", "GC", "AU", "UA", "GU", "UG"):
                                    if cand_bp != cur_bp and cand_bp != flip_bp and cand_bp in allowed_pairs[uv_s]:
                                        ch_at_zn = cand_bp[0] if zn == uv_s[0] else cand_bp[1]
                                        if dz != 0 or (w_lst[w] + ch_at_zn) not in S.VALID_SET:
                                            other_flips.append((uv_s, cand_bp))

        # `Law R21a`: For outermost missing external pairs `(u_m, v_m)` in `ext_miss[:2]`, include their
        # immediate unpaired outer flank dangles `u_m - 1` and `v_m + 1` in `unp_edits`.
        for u_m, v_m in ext_miss[:2]:
            if (u_m, v_m) not in direct_extra_uvs:
                direct_extra_uvs.append((u_m, v_m))
            for z_fl in (u_m - 1, v_m + 1):
                if 0 <= z_fl < n and pair_of[z_fl] == -1 and z_fl not in locked_pos and z_fl not in prot_W2 and z_fl not in seen_unp:
                    seen_unp.add(z_fl)
                    for ch_new in ("C", "G", "A", "U"):
                        if ch_new != w_lst[z_fl] and not S.has_symmetric_neck_zip(z_fl, ch_new, w_lst, pair_of, n):
                            unp_edits.append((z_fl, ch_new))

        single_flips = pure_flips + other_flips

        cand_seqs = []

        # 0. `Law R19a` + `Law R21a`: Whole-Stem, Interior-Stem, & `1x1`-Cascade Chirality Reflection
        ext_stems = []
        ext_cascades = []
        seed_uvs_for_stems = list(direct_extra_uvs)
        for u_p, v_p in pinfo["pairs"]:
            if (u_p, v_p) != primary_req and (u_p, v_p) not in seed_uvs_for_stems:
                if min(min(abs(u_p - p_w), abs(v_p - p_w)) for p_w in prot_W2) <= 5:
                    seed_uvs_for_stems.append((u_p, v_p))
        for uv_d in seed_uvs_for_stems:
            st_tup = stem_of_uv.get(uv_d)
            if st_tup and st_tup not in ext_stems:
                if all(u_k not in prot_W2 and v_k not in prot_W2 for u_k, v_k in st_tup):
                    ext_stems.append(st_tup)
            cas_tup = cascade11_of_uv.get(uv_d)
            if cas_tup and cas_tup not in ext_cascades and primary_req not in cas_tup[0]:
                ext_cascades.append(cas_tup)

        for cas_pairs, cas_u11 in ext_cascades[:4]:
            # Test both: (a) reflecting the full `1x1` cascade `cas_pairs`, and (b) reflecting only pairs outside `prot_W2`
            for only_outside in (False, True):
                tl_cas = list(w_lst)
                changed_cas = False
                for u_k, v_k in cas_pairs:
                    if only_outside and (u_k in prot_W2 or v_k in prot_W2):
                        continue
                    cur_bp = tl_cas[u_k] + tl_cas[v_k]
                    flip_bp = cur_bp[1] + cur_bp[0]
                    if flip_bp != cur_bp and flip_bp in allowed_pairs[(u_k, v_k)]:
                        tl_cas[u_k], tl_cas[v_k] = flip_bp[0], flip_bp[1]
                        changed_cas = True
                for p1_k, q1_k in cas_u11:
                    if p1_k not in locked_pos and q1_k not in locked_pos and p1_k not in prot_W2 and q1_k not in prot_W2:
                        if tl_cas[p1_k] != tl_cas[q1_k]:
                            tl_cas[p1_k], tl_cas[q1_k] = tl_cas[q1_k], tl_cas[p1_k]
                            changed_cas = True
                if changed_cas:
                    cand_seqs.append("".join(tl_cas))
        def apply_stem_mode(tl_work: list, st_slice: tuple, mode_s: str) -> bool:
            changed_s = False
            for r_idx, (u_k, v_k) in enumerate(st_slice):
                if u_k in locked_pos or v_k in locked_pos or u_k in prot_W2 or v_k in prot_W2:
                    continue
                cur_bp = tl_work[u_k] + tl_work[v_k]
                if mode_s == "reflect":
                    target_bp = cur_bp[1] + cur_bp[0]
                elif mode_s == "alt_0":
                    if cur_bp in ("GC", "CG"):
                        target_bp = "GC" if (r_idx % 2 == 0) else "CG"
                    else:
                        target_bp = cur_bp[1] + cur_bp[0] if (r_idx % 2 == 1) else cur_bp
                else:  # "alt_1"
                    if cur_bp in ("GC", "CG"):
                        target_bp = "CG" if (r_idx % 2 == 0) else "GC"
                    else:
                        target_bp = cur_bp[1] + cur_bp[0] if (r_idx % 2 == 0) else cur_bp
                if target_bp != cur_bp and target_bp in allowed_pairs[(u_k, v_k)]:
                    tl_work[u_k], tl_work[v_k] = target_bp[0], target_bp[1]
                    changed_s = True
            return changed_s

        for st_tup in ext_stems[:5]:
            # Full stem and interior-only (`st_tup[1:]`, preserving multiloop junction pair `st_tup[0]`)
            slices_to_try = [st_tup]
            if len(st_tup) >= 2:
                slices_to_try.append(st_tup[1:])
            if len(st_tup) >= 3:
                slices_to_try.append(st_tup[:-1])
            for st_slice in slices_to_try:
                modes_to_try = ("reflect", "alt_0", "alt_1") if len(st_slice) >= 2 else ("reflect",)
                for mode_s in modes_to_try:
                    tl_st = list(w_lst)
                    if apply_stem_mode(tl_st, st_slice, mode_s):
                        cand_seqs.append("".join(tl_st))
        # Pairwise simultaneous two-stem 4-state transformations (`Law R23d`: `reflect`, `alt_0`, `alt_1`)
        if len(ext_stems) >= 2:
            for i_s in range(min(3, len(ext_stems))):
                for j_s in range(i_s + 1, min(4, len(ext_stems))):
                    modes_i = ("reflect", "alt_0", "alt_1") if len(ext_stems[i_s]) >= 2 else ("reflect",)
                    modes_j = ("reflect", "alt_0", "alt_1") if len(ext_stems[j_s]) >= 2 else ("reflect",)
                    for m_i, m_j in itertools.product(modes_i, modes_j):
                        tl_2s = list(w_lst)
                        c1 = apply_stem_mode(tl_2s, ext_stems[i_s], m_i)
                        c2 = apply_stem_mode(tl_2s, ext_stems[j_s], m_j)
                        if c1 or c2:
                            cand_seqs.append("".join(tl_2s))

        # 0b. Intra-loop unpaired-unpaired slip killer (e.g., `(12, 18)` in `#5407007`)
        for ux, uy in unp_unp_slips[:2]:
            if ux not in locked_pos and uy not in locked_pos and ux not in prot_W2 and uy not in prot_W2:
                for b1, b2 in (("A", "A"), ("G", "A"), ("A", "G"), ("G", "G"), ("C", "C"), ("U", "U"), ("A", "C"), ("C", "A")):
                    tl_uu = list(w_lst)
                    tl_uu[ux], tl_uu[uy] = b1, b2
                    if not S.has_symmetric_neck_zip(ux, b1, tl_uu, pair_of, n) and not S.has_symmetric_neck_zip(
                        uy, b2, tl_uu, pair_of, n
                    ):
                        cand_seqs.append("".join(tl_uu))

        # 1. `Law R12`: Whole-Stem / Bulge-Cluster Chirality Inversion (`2..4` pairs flipped simultaneously)
        seen_clusters = set()
        for uv_seed in direct_extra_uvs[:3]:
            cl_pairs, cl_unp = collect_external_motif_cluster(uv_seed, pinfo, prot_W2)
            cl_key = tuple(sorted(cl_pairs))
            if len(cl_pairs) >= 2 and cl_key not in seen_clusters:
                seen_clusters.add(cl_key)
                # Test flipping first 2, first 3, and all 4 pairs of the external motif cluster
                for k_sub in range(2, len(cl_pairs) + 1):
                    sub_pairs = cl_pairs[:k_sub]
                    tl_cl = list(w_lst)
                    ok_cl = True
                    for u_c, v_c in sub_pairs:
                        cur_bp = tl_cl[u_c] + tl_cl[v_c]
                        flip_bp = cur_bp[1] + cur_bp[0]
                        if flip_bp != cur_bp and flip_bp in allowed_pairs[(u_c, v_c)]:
                            tl_cl[u_c], tl_cl[v_c] = flip_bp[0], flip_bp[1]
                        else:
                            ok_cl = False
                    if ok_cl:
                        s_cl = "".join(tl_cl)
                        cand_seqs.append(s_cl)
                        # If the external motif has a 1-nt bulge `cl_unp`, pick the bulge base that minimizes local opening energy
                        if cl_unp:
                            b_pos = cl_unp[0]
                            best_b_seq = None
                            best_b_gap = 1e9
                            open_structs_cl = [pinfo["open_pair_struct"][uv_c] for uv_c in sub_pairs]
                            for ch_b in S.BASES:
                                tl_cl[b_pos] = ch_b
                                s_b_try = "".join(tl_cl)
                                et_b = float(RNA.energy_of_struct(s_b_try, target))
                                gap_b = max(et_b - float(RNA.energy_of_struct(s_b_try, rs_c)) for rs_c in open_structs_cl)
                                if gap_b < best_b_gap:
                                    best_b_gap = gap_b
                                    best_b_seq = s_b_try
                            if best_b_seq and best_b_seq != s_cl:
                                cand_seqs.append(best_b_seq)

        # 2. Direct multi-pair flip on `direct_extra_uvs`
        if direct_extra_uvs:
            for stride in (1, 2):
                tl_mf = list(w_lst)
                changed_mf = False
                for idx_d, uv_d in enumerate(direct_extra_uvs):
                    if stride == 2 and (idx_d % 2 == 1):
                        continue
                    cur_bp = tl_mf[uv_d[0]] + tl_mf[uv_d[1]]
                    flip_bp = cur_bp[1] + cur_bp[0]
                    if flip_bp != cur_bp and flip_bp in allowed_pairs[uv_d]:
                        tl_mf[uv_d[0]], tl_mf[uv_d[1]] = flip_bp[0], flip_bp[1]
                        changed_mf = True
                if changed_mf:
                    cand_seqs.append("".join(tl_mf))

        if seen_unp:
            tl_all = list(w_lst)
            changed_all = False
            for z, ch_new in unp_edits:
                if tl_all[z] == w_lst[z]:
                    tl_all[z] = ch_new
                    changed_all = True
            if changed_all:
                cand_seqs.append("".join(tl_all))

        for uv_s, flip_bp in single_flips[:12]:
            tl = list(w_lst)
            tl[uv_s[0]], tl[uv_s[1]] = flip_bp[0], flip_bp[1]
            s_tl = "".join(tl)
            if S.budget_violation(s_tl, pinfo) <= cur_vb:
                cand_seqs.append(s_tl)

        for z, ch_new in unp_edits[:6]:
            tl = list(w_lst)
            tl[z] = ch_new
            cand_seqs.append("".join(tl))

        if not cand_seqs:
            break

        dedup_cands = []
        seen_cs = {w_seq}
        for cs in cand_seqs:
            if cs not in seen_cs:
                seen_cs.add(cs)
                dedup_cands.append(cs)

        # Pre-rank `dedup_cands` by `max_{r in ext_rivals} (E(cs, T) - E(cs, r))` using fast `RNA.energy_of_struct`
        scored_cands = []
        for cs in dedup_cands:
            et_c = float(RNA.energy_of_struct(cs, target))
            w_ext = eval_ext_rivals_worst(cs, et_c, ext_rivals[-6:])
            scored_cands.append((w_ext, et_c, cs))
        scored_cands.sort(key=lambda x: (x[0], x[1]))

        w_et = float(RNA.energy_of_struct(w_seq, target))
        w_worst_ext = eval_ext_rivals_worst(w_seq, w_et, ext_rivals[-6:])
        cur_key = (
            sum(1 for uv_r in req_bps if uv_r not in w_bps),
            w_dbp if w_dbp <= 4 else len(extra),
            w_dbp,
            max(0.0, w_worst_ext),
            w_de,
        )
        best_cp_step = None
        best_cp_key = None
        for _w_ext, _et_c, cs in scored_cands[:max_cands]:
            if time.time() >= deadline:
                break
            cms, cme = S.exact_fold(cs, eng)
            cbps = S.get_bp_set(cms)
            cdbp = len(t_bps ^ cbps)
            cet = float(RNA.energy_of_struct(cs, target))
            cde = round(cet - cme, 4)
            if cdbp == 0 and S.budget_violation(cs, pinfo) == 0:
                return cs, cms, 0, 0.0
            cextra_n = len(cbps - t_bps)
            c_worst_ext = eval_ext_rivals_worst(cs, cet, ext_rivals[-6:])
            missing_req = sum(1 for uv_r in req_bps if uv_r not in cbps)
            ckey = (
                missing_req,
                cdbp if cdbp <= 4 else cextra_n,
                cdbp,
                max(0.0, c_worst_ext),
                cde,
            )
            if ckey < inc_key:
                inc_key = ckey
                inc_seq, inc_ms, inc_dbp, inc_de = cs, cms, cdbp, cde
            if ckey < cur_key or (c_worst_ext < w_worst_ext - 0.05 and cms not in ext_rivals):
                cp_key = (
                    1 if c_worst_ext <= 0.0 else 2,
                    round(max(0.0, c_worst_ext), 3),
                    missing_req,
                    cdbp,
                    cde,
                )
                if best_cp_key is None or cp_key < best_cp_key:
                    best_cp_key = cp_key
                    best_cp_step = (cs, cms, cbps, cdbp, cde)

        if best_cp_step is None:
            break
        w_seq, w_ms, w_bps, w_dbp, w_de = best_cp_step
        if w_ms not in ext_rivals:
            ext_rivals.append(w_ms)

    return inc_seq, inc_ms, inc_dbp, inc_de


def collect_neighbors_of_pair(u0: int, v0: int, pinfo: dict, max_walk: int = 8) -> tuple:
    """
    `Law R14` (4-Corner Flanking Dangle Completeness):
    Places the two immediate inner corner unpaired bases `(u0 + 1, v0 - 1)` at the very front of `in_unp`,
    and the two immediate outer corner unpaired bases `(u0 - 1, v0 + 1)` at the very front of `out_unp`,
    before walking deeper into internal/multiloop segments.
    """
    pair_of = pinfo["pair_of"]
    allowed_pairs = pinfo["allowed_pairs"]
    locked_pos = pinfo["locked_pos"]
    n = pinfo["n"]

    in_pairs = []
    in_unp = []
    for c_in in (u0 + 1, v0 - 1):
        if u0 < c_in < v0 and pair_of[c_in] == -1 and c_in not in locked_pos and c_in not in in_unp:
            in_unp.append(c_in)

    p_il = u0 + 1
    while p_il < v0 and pair_of[p_il] == -1 and p_il - u0 <= max_walk:
        if p_il not in locked_pos and p_il not in in_unp:
            in_unp.append(p_il)
        p_il += 1
    if p_il < v0 and pair_of[p_il] != -1 and u0 < pair_of[p_il] < v0:
        uv_il = (min(p_il, pair_of[p_il]), max(p_il, pair_of[p_il]))
        if len(allowed_pairs[uv_il]) > 1:
            in_pairs.append(uv_il)

    p_ir = v0 - 1
    while p_ir > u0 and pair_of[p_ir] == -1 and v0 - p_ir <= max_walk:
        if p_ir not in locked_pos and p_ir not in in_unp:
            in_unp.append(p_ir)
        p_ir -= 1
    if p_ir > u0 and pair_of[p_ir] != -1 and u0 < pair_of[p_ir] < v0:
        uv_ir = (min(p_ir, pair_of[p_ir]), max(p_ir, pair_of[p_ir]))
        if len(allowed_pairs[uv_ir]) > 1 and uv_ir not in in_pairs:
            in_pairs.append(uv_ir)

    # `Law R14`: If `(u0, v0)` bounds a single-child internal loop with `in_pairs[0] = (u_in, v_in)`,
    # prioritize the inner-pair closing corners `(u_in - 1, v_in + 1)` right after `(u0 + 1, v0 - 1)`
    # before middle internal-loop bases.
    if len(in_pairs) == 1:
        u_in, v_in = in_pairs[0]
        priority_in = []
        for c_ic in (u0 + 1, v0 - 1, u_in - 1, v_in + 1):
            if c_ic in in_unp and c_ic not in priority_in:
                priority_in.append(c_ic)
        for c_rem in in_unp:
            if c_rem not in priority_in:
                priority_in.append(c_rem)
        in_unp = priority_in

    out_pairs = []
    out_unp = []
    for c_out in (u0 - 1, v0 + 1):
        if 0 <= c_out < n and pair_of[c_out] == -1 and c_out not in locked_pos and c_out not in out_unp:
            out_unp.append(c_out)

    p_ol = u0 - 1
    while p_ol >= 0 and pair_of[p_ol] == -1 and u0 - p_ol <= max_walk:
        if p_ol not in locked_pos and p_ol not in out_unp:
            out_unp.append(p_ol)
        p_ol -= 1
    if p_ol >= 0 and pair_of[p_ol] != -1 and (pair_of[p_ol] < u0 or pair_of[p_ol] > v0):
        uv_ol = (min(p_ol, pair_of[p_ol]), max(p_ol, pair_of[p_ol]))
        if len(allowed_pairs[uv_ol]) > 1:
            out_pairs.append(uv_ol)

    p_or = v0 + 1
    while p_or < n and pair_of[p_or] == -1 and p_or - v0 <= max_walk:
        if p_or not in locked_pos and p_or not in out_unp:
            out_unp.append(p_or)
        p_or += 1
    if p_or < n and pair_of[p_or] != -1 and (pair_of[p_or] < u0 or pair_of[p_or] > v0):
        uv_or = (min(p_or, pair_of[p_or]), max(p_or, pair_of[p_or]))
        if len(allowed_pairs[uv_or]) > 1 and uv_or not in out_pairs:
            out_pairs.append(uv_or)

    return in_pairs, in_unp, out_pairs, out_unp


def build_depth2_windows(seq: str, ms: str, pinfo: dict, eng: int, deadline: float, extra_forbid: list = None) -> list:
    target = pinfo["target"]
    pair_of = pinfo["pair_of"]
    allowed_pairs = pinfo["allowed_pairs"]
    locked_pos = pinfo["locked_pos"]
    t_bps = S.get_bp_set(target)
    m_bps = S.get_bp_set(ms)
    miss = sorted(t_bps - m_bps)
    extra = sorted(m_bps - t_bps)

    windows = []

    def expand_to_depth2(w1_p: list, w1_u: list, forbid_pairs: list, extra_rivs: list, max_d2_p: int = 2, max_d2_u: int = 2):
        w1_p = w1_p[:3]
        w1_u = w1_u[:4 if len(w1_p) <= 2 else 3]
        d2_p = []
        d2_u = []
        for ua, va in w1_p:
            ip, iu, op, ou = collect_neighbors_of_pair(ua, va, pinfo, max_walk=8)
            for uv_n in ip + op:
                if uv_n not in w1_p and uv_n not in d2_p and len(allowed_pairs[uv_n]) > 1:
                    d2_p.append(uv_n)
            for idx_u in iu + ou:
                if idx_u not in w1_u and idx_u not in d2_u and idx_u not in locked_pos:
                    d2_u.append(idx_u)
        for ua, va in list(d2_p):
            if len(d2_p) >= max_d2_p and len(d2_u) >= max_d2_u:
                break
            ip, iu, op, ou = collect_neighbors_of_pair(ua, va, pinfo, max_walk=6)
            for uv_n in ip + op:
                if uv_n not in w1_p and uv_n not in d2_p and len(allowed_pairs[uv_n]) > 1 and len(d2_p) < max_d2_p:
                    d2_p.append(uv_n)
            for idx_u in iu + ou:
                if idx_u not in w1_u and idx_u not in d2_u and idx_u not in locked_pos and len(d2_u) < max_d2_u:
                    d2_u.append(idx_u)
        return (w1_p, w1_u, d2_p[:max_d2_p], d2_u[:max_d2_u], forbid_pairs, extra_rivs)

    n = pinfo["n"]
    sorted_pairs = sorted(pinfo["pairs"], key=lambda uv: (uv[0], -uv[1]))
    parent_of_uv = {}
    children_of_uv = {uv: [] for uv in sorted_pairs}
    stack_uv = []
    for uv in sorted_pairs:
        while stack_uv and not (stack_uv[-1][0] < uv[0] and uv[1] < stack_uv[-1][1]):
            stack_uv.pop()
        if stack_uv:
            parent_of_uv[uv] = stack_uv[-1]
            children_of_uv[stack_uv[-1]].append(uv)
        else:
            parent_of_uv[uv] = None
        stack_uv.append(uv)

    forbid_extra = [(pu, pv) for pu, pv in extra if pair_of[pu] == -1 and pair_of[pv] == -1]
    if extra_forbid:
        for uv_f in extra_forbid:
            if uv_f not in forbid_extra:
                forbid_extra.append(uv_f)

    # 1. Coupled multi-defect window (`Law R9`) when `len(miss) >= 2`
    if len(miss) >= 2:
        coupled_seeds = []
        for i in range(len(miss)):
            for j in range(i + 1, len(miss)):
                u1, v1 = miss[i]
                u2, v2 = miss[j]
                dist = min(abs(u1 - u2), abs(v1 - v2), abs(u1 - v2), abs(v1 - u2))
                coupled_seeds.append((dist, miss[i], miss[j]))
        coupled_seeds.sort(key=lambda x: x[0])
        for _dist, uv1, uv2 in coupled_seeds[:2]:
            w1_p = [uv1, uv2]
            ip1, iu1, op1, ou1 = collect_neighbors_of_pair(uv1[0], uv1[1], pinfo)
            ip2, iu2, op2, ou2 = collect_neighbors_of_pair(uv2[0], uv2[1], pinfo)
            for uv_n in ip1 + op1 + ip2 + op2:
                if uv_n not in w1_p and len(allowed_pairs[uv_n]) > 1:
                    w1_p.append(uv_n)
                    break
            w1_u = []
            for pu, pv in forbid_extra:
                for p_e in (pu, pv):
                    if p_e not in locked_pos and p_e not in w1_u:
                        w1_u.append(p_e)
            for idx_u in iu1 + ou1 + iu2 + ou2:
                if idx_u not in w1_u and idx_u not in locked_pos:
                    w1_u.append(idx_u)
            windows.append(expand_to_depth2(w1_p, w1_u, forbid_extra, [ms]))

    # 2. Individual missing pair depth-2 windows (`Law R11` + `Law R14` + `Law R20a` + `Law R21a`)
    for u0, v0 in miss[:3]:
        ip, iu, op, ou = collect_neighbors_of_pair(u0, v0, pinfo)

        # `Law R21a` (`Window 2a-coll` Collapsed-Multiloop Sibling-Corner Window):
        # If `(u0, v0)` (or its 1-child branch root `uv_br`) is a child branch of an enclosing multiloop pair `p_A`
        # with sibling branch `p_B`, co-optimize `[(u0, v0), p_A, p_B]` and the 4 collapsed-multiloop corners
        # `[u_A + 1, v_A - 1, u_B - 1, v_B + 1]` in Stage 1 against the collapsed-branch rival `r_open_br`.
        uv_br = (u0, v0)
        for _ in range(2):
            par_br = parent_of_uv.get(uv_br)
            if par_br is not None and len(children_of_uv[par_br]) == 1:
                uv_br = par_br
            else:
                break
        p_A = parent_of_uv.get(uv_br)
        if p_A is not None and len(children_of_uv[p_A]) >= 2:
            u_A, v_A = p_A
            tl_r_br = list(target)
            for u_sub, v_sub in sorted_pairs:
                if uv_br[0] <= u_sub < v_sub <= uv_br[1]:
                    tl_r_br[u_sub] = "."
                    tl_r_br[v_sub] = "."
            r_open_br = "".join(tl_r_br)
            sibs = [uv_s for uv_s in children_of_uv[p_A] if uv_s != uv_br]
            for p_B in sibs[:2]:
                u_B, v_B = p_B
                w1_p_coll = []
                for uv_c in [(u0, v0), p_A, p_B]:
                    if uv_c not in w1_p_coll and len(allowed_pairs[uv_c]) > 1:
                        w1_p_coll.append(uv_c)
                w1_u_coll = []
                for x_c in (u_A + 1, v_A - 1, u_B - 1, v_B + 1):
                    if 0 <= x_c < n and pair_of[x_c] == -1 and x_c not in locked_pos and x_c not in w1_u_coll:
                        w1_u_coll.append(x_c)
                d2_u_coll = []
                for x_d in iu[:2] + ou[:2]:
                    if 0 <= x_d < n and pair_of[x_d] == -1 and x_d not in locked_pos and x_d not in w1_u_coll and x_d not in d2_u_coll:
                        d2_u_coll.append(x_d)
                windows.append((w1_p_coll[:3], w1_u_coll[:4], [], d2_u_coll[:2], forbid_extra, [ms, r_open_br]))

        if len(children_of_uv.get((u0, v0), [])) >= 2:
            ch_list = children_of_uv[(u0, v0)]
            p_out = parent_of_uv.get((u0, v0))
            w1_p_mc = [(u0, v0)]
            for uv_c in ([p_out] if p_out else []) + ch_list[:2]:
                if uv_c and uv_c not in w1_p_mc and len(allowed_pairs[uv_c]) > 1 and len(w1_p_mc) < 3:
                    w1_p_mc.append(uv_c)
            w1_u_mc = []
            for x_c in [u0 + 1, v0 - 1, u0 - 1, v0 + 1] + [x for (uc, vc) in ch_list[:2] for x in (uc - 1, vc + 1)]:
                if 0 <= x_c < n and pair_of[x_c] == -1 and x_c not in locked_pos and x_c not in w1_u_mc:
                    w1_u_mc.append(x_c)
            d2_u_mc = [x for x in w1_u_mc[4:6]]
            windows.append((w1_p_mc[:3], w1_u_mc[:4], [], d2_u_mc[:2], forbid_extra, [ms]))
        # Window 2a: Complete Inner-Loop Unit `[(u0, v0), in_0]` + all internal-loop corners `iu[:3]` in Stage 1 (`Law R13 + Law R14 + Law R20a`)
        if ip:
            w1_p_a = [(u0, v0), ip[0]]
            dedup_corners_a = []
            for x in iu[:3] + ou[:1] + ou[:2] + iu + ou:
                if x not in locked_pos and x not in dedup_corners_a:
                    dedup_corners_a.append(x)
            w1_u_a = dedup_corners_a[:4]
            d2_p_a = [uv for uv in op if len(allowed_pairs[uv]) > 1][:1]
            ip_in1, iu_in1, op_in1, ou_in1 = collect_neighbors_of_pair(ip[0][0], ip[0][1], pinfo, max_walk=6)
            for uv_n in ip_in1 + op_in1:
                if uv_n not in w1_p_a and uv_n not in d2_p_a and len(allowed_pairs[uv_n]) > 1 and len(d2_p_a) < 2:
                    d2_p_a.append(uv_n)
            # Prioritize any adjacent tetraloop 3rd position `ut + 3` when `seq[ut+1:vt] == "GAGA"` (`GAGA -> GAAA` de-G normalization)
            tloop_deg_u = []
            for ut, vt in w1_p_a + d2_p_a + ip_in1:
                if vt - ut == 5 and seq[ut + 1 : vt] == "GAGA" and (ut + 3) not in locked_pos:
                    tloop_deg_u.append(ut + 3)
            d2_u_a = []
            for x in tloop_deg_u + dedup_corners_a + iu_in1 + ou_in1:
                if x not in w1_u_a and x not in locked_pos and x not in d2_u_a:
                    d2_u_a.append(x)
            d2_u_a = d2_u_a[: 3 if len(d2_p_a) <= 1 else 2]
            windows.append((w1_p_a, w1_u_a, d2_p_a, d2_u_a, forbid_extra, [ms]))
        if op and (not ip or (u0 - op[0][0]) + (op[0][1] - v0) <= 6):
            # Window 2a-hp / 2a-out (`Law R20a`): Complete Outer-Stem + Hairpin/Triloop/Bulge Unit `[(u0, v0), op[0]]`
            w1_p_hp = [(u0, v0), op[0]]
            ip_out0, iu_out0, op_out0, ou_out0 = collect_neighbors_of_pair(op[0][0], op[0][1], pinfo, max_walk=6)
            d2_p_hp1 = []
            for uv in op[1:] + ip[:1] + ip_out0 + op_out0:
                if uv not in w1_p_hp and uv not in d2_p_hp1 and len(allowed_pairs[uv]) > 1 and len(d2_p_hp1) < 2:
                    d2_p_hp1.append(uv)
            w1_u_hp1 = []
            for x in iu[:3] + ou[:2] + iu + ou + iu_out0[:2]:
                if x not in locked_pos and x not in w1_u_hp1:
                    w1_u_hp1.append(x)
            w1_u_hp1 = w1_u_hp1[:4]
            d2_u_hp1 = []
            for x in ou[:2] + iu_out0[:2] + iu + ou + iu_out0 + ou_out0:
                if x not in w1_u_hp1 and x not in locked_pos and x not in d2_u_hp1:
                    d2_u_hp1.append(x)
            d2_u_hp1 = d2_u_hp1[: 3 if len(d2_p_hp1) <= 1 else 2]
            windows.append((w1_p_hp, w1_u_hp1, d2_p_hp1, d2_u_hp1, forbid_extra, [ms]))

            w1_u_hp2 = []
            for x in ou[:2] + iu_out0[:2] + iu[:2] + iu + ou:
                if x not in locked_pos and x not in w1_u_hp2:
                    w1_u_hp2.append(x)
            w1_u_hp2 = w1_u_hp2[:4]
            d2_u_hp2 = []
            for x in iu[2:] + ou[:2] + iu + ou + iu_out0 + ou_out0:
                if x not in w1_u_hp2 and x not in locked_pos and x not in d2_u_hp2:
                    d2_u_hp2.append(x)
            d2_u_hp2 = d2_u_hp2[: 3 if len(d2_p_hp1) <= 1 else 2]
            if w1_u_hp2 != w1_u_hp1 or d2_u_hp2 != d2_u_hp1:
                windows.append((w1_p_hp, w1_u_hp2, d2_p_hp1, d2_u_hp2, forbid_extra, [ms]))

        # Window 2c (`Law R24d`): Certifier-Exact 5'-First 3-Pair Core + Depth-2 Boundary Expansion
        in_5p = []
        p_il_c = u0 + 1
        while p_il_c < v0 and pair_of[p_il_c] == -1 and p_il_c - u0 <= 6:
            if p_il_c not in locked_pos:
                in_5p.append(p_il_c)
            p_il_c += 1
        in_3p = []
        p_ir_c = v0 - 1
        while p_ir_c > u0 and pair_of[p_ir_c] == -1 and v0 - p_ir_c <= 6:
            if p_ir_c not in locked_pos and p_ir_c not in in_5p:
                in_3p.append(p_ir_c)
            p_ir_c -= 1
        out_5p = []
        p_ol_c = u0 - 1
        while p_ol_c >= 0 and pair_of[p_ol_c] == -1 and u0 - p_ol_c <= 6:
            if p_ol_c not in locked_pos:
                out_5p.append(p_ol_c)
            p_ol_c -= 1
        out_3p = []
        p_or_c = v0 + 1
        while p_or_c < n and pair_of[p_or_c] == -1 and p_or_c - v0 <= 6:
            if p_or_c not in locked_pos and p_or_c not in out_5p:
                out_3p.append(p_or_c)
            p_or_c += 1
        w1_p_2c = [(u0, v0)]
        for uv_c in ip[:1] + op[:1]:
            if uv_c not in w1_p_2c and len(allowed_pairs[uv_c]) > 1:
                w1_p_2c.append(uv_c)
        w1_u_2c = ((in_5p + in_3p)[:2] + (out_5p + out_3p)[:2])[:3]
        d2_p_2c = []
        for uv_d in ip[1:] + op[1:]:
            if uv_d not in w1_p_2c and uv_d not in d2_p_2c and len(allowed_pairs[uv_d]) > 1 and len(d2_p_2c) < 2:
                d2_p_2c.append(uv_d)
        for ua_c, va_c in w1_p_2c[1:]:
            ip_c2, _iu_c2, op_c2, _ou_c2 = collect_neighbors_of_pair(ua_c, va_c, pinfo, max_walk=6)
            for uv_d in ip_c2 + op_c2:
                if uv_d not in w1_p_2c and uv_d not in d2_p_2c and len(allowed_pairs[uv_d]) > 1 and len(d2_p_2c) < 2:
                    d2_p_2c.append(uv_d)
        d2_u_2c = []
        max_u_2c = 3 if len(d2_p_2c) <= 1 else 2
        for x_d in in_3p + out_3p + in_5p + out_5p + iu + ou:
            if x_d not in w1_u_2c and x_d not in locked_pos and x_d not in d2_u_2c and len(d2_u_2c) < max_u_2c:
                d2_u_2c.append(x_d)
        windows.append((w1_p_2c[:3], w1_u_2c, d2_p_2c[:2], d2_u_2c, forbid_extra, [ms]))

        # Window 2b: 3-pair depth-1 core `[(u0, v0), in_0, out_0]` expanded to depth-2
        w1_p = [(u0, v0)]
        for uv_n in ip[:1] + op[:1]:
            if uv_n not in w1_p and len(allowed_pairs[uv_n]) > 1:
                w1_p.append(uv_n)
        for uv_n in ip + op:
            if len(w1_p) < 3 and uv_n not in w1_p and len(allowed_pairs[uv_n]) > 1:
                w1_p.append(uv_n)
        w1_u = []
        for pu, pv in forbid_extra:
            for p_e in (pu, pv):
                if p_e not in locked_pos and p_e not in w1_u and min(abs(p_e - u0), abs(p_e - v0)) <= 8:
                    w1_u.append(p_e)
        for idx_u in iu[:2] + ou[:2] + iu + ou:
            if idx_u not in w1_u and idx_u not in locked_pos:
                w1_u.append(idx_u)
        windows.append(expand_to_depth2(w1_p, w1_u, forbid_extra, [ms]))

    # 3. Broken Parasitic Prop window (`Law R7 + Law R20b`) when `extra` is non-empty
    if extra and time.time() < deadline:
        for pu, pv in extra[:2]:
            unpropped_miss = []
            unpropped_rivals = [ms]
            for b1 in S.BASES:
                if pu in locked_pos and b1 != seq[pu]:
                    continue
                for b2 in S.BASES:
                    if pv in locked_pos and b2 != seq[pv]:
                        continue
                    if (b1 + b2) in S.VALID_SET:
                        continue
                    tl_u = list(seq)
                    tl_u[pu], tl_u[pv] = b1, b2
                    s_u = "".join(tl_u)
                    if S.budget_violation(s_u, pinfo) > 0:
                        continue
                    ms_u, _ = S.exact_fold(s_u, eng)
                    if ms_u not in unpropped_rivals:
                        unpropped_rivals.append(ms_u)
                    for uv_m in sorted(t_bps - S.get_bp_set(ms_u)):
                        if uv_m not in unpropped_miss and len(allowed_pairs[uv_m]) > 1:
                            unpropped_miss.append(uv_m)
                    if len(unpropped_rivals) >= 4:
                        break
                if len(unpropped_rivals) >= 4:
                    break

            w1_p = []
            for uv_m in miss + unpropped_miss:
                if uv_m not in w1_p and len(allowed_pairs[uv_m]) > 1:
                    w1_p.append(uv_m)
            for p_start in (pu, pv):
                for d_step in (-1, 1, -2, 2, -3, 3):
                    idx_p = p_start + d_step
                    if 0 <= idx_p < pinfo["n"] and pair_of[idx_p] != -1:
                        uv_adj = (min(idx_p, pair_of[idx_p]), max(idx_p, pair_of[idx_p]))
                        if uv_adj not in w1_p and len(allowed_pairs[uv_adj]) > 1:
                            w1_p.append(uv_adj)
            w1_u = []
            for p_e in (pu, pv):
                if p_e not in locked_pos and pair_of[p_e] == -1 and p_e not in w1_u:
                    w1_u.append(p_e)
            for ua, va in w1_p[:2]:
                _ip, iu, _op, ou = collect_neighbors_of_pair(ua, va, pinfo)
                for idx_u in iu[:2] + ou[:2] + iu + ou:
                    if idx_u not in w1_u and idx_u not in locked_pos:
                        w1_u.append(idx_u)
            if w1_p:
                forb_3 = forbid_extra + [(pu, pv)] if (pu, pv) not in forbid_extra else list(forbid_extra)
                # Window 3a-2p (`Law R20b`): 2-pair core `w1_p[:2]` + 4 unpaired slots (`[pu, pv]` + 2 loop corners of `unpropped_miss`)
                if len(w1_p) >= 2:
                    d2_p_2p = w1_p[2:4]
                    d2_u_2p = w1_u[4 : (7 if len(d2_p_2p) <= 1 else 6)]
                    windows.append((w1_p[:2], w1_u[:4], d2_p_2p, d2_u_2p, forb_3, unpropped_rivals[:4]))
                # Window 3a-3p (`Law R20b`): 3-pair core `w1_p[:3]` + `w1_u[:3]` (or `[:4]` if `<= 2` pairs)
                w1_u_cap = 4 if len(w1_p[:3]) <= 2 else 3
                d2_cand = [uv for uv in w1_p[3:5]]
                d2_u_cand = [u for u in w1_u[w1_u_cap : w1_u_cap + 3]]
                w_tuple = expand_to_depth2(w1_p[:3], w1_u[:w1_u_cap], forb_3, unpropped_rivals[:4])
                merged_d2_p = list(d2_cand)
                for uv_d in w_tuple[2]:
                    if uv_d not in merged_d2_p and uv_d not in w1_p[:3] and len(merged_d2_p) < 2:
                        merged_d2_p.append(uv_d)
                merged_d2_u = list(d2_u_cand)
                max_u3 = 3 if len(merged_d2_p) <= 1 else 2
                for u_d in w_tuple[3]:
                    if u_d not in merged_d2_u and u_d not in w1_u[:w1_u_cap] and len(merged_d2_u) < max_u3:
                        merged_d2_u.append(u_d)
                windows.append((w1_p[:3], w1_u[:w1_u_cap], merged_d2_p[:2], merged_d2_u[:max_u3], w_tuple[4], unpropped_rivals[:4]))

    return windows


def find_unpropped_mismatch_seeds(seq: str, ms: str, pinfo: dict, eng: int, deadline: float) -> list:
    """
    `Law R20b` (Window 3b Unpropped-Mismatch Seed):
    When `extra` is non-empty, evaluates non-pairing mismatches `(b1, b2)` on each `(pu, pv) in extra[:2]`
    and returns the lowest-`(d_bp, de_mfe)` budget-valid unpropped sequences `(s_u, ms_u, (pu, pv))` so
    `build_depth2_windows` can optimize the revealed `unpropped_miss` directly as primary `miss` defects
    while forbidding `(pu, pv)`.
    """
    target = pinfo["target"]
    pair_of = pinfo["pair_of"]
    locked_pos = pinfo["locked_pos"]
    t_bps = S.get_bp_set(target)
    m_bps = S.get_bp_set(ms)
    extra = sorted(m_bps - t_bps)
    cur_vb = S.budget_violation(seq, pinfo)
    seeds = []
    for pu, pv in extra[:2]:
        if time.time() >= deadline:
            break
        if pair_of[pu] != -1 or pair_of[pv] != -1:
            continue
        best_cand = None
        for b1 in S.BASES:
            if pu in locked_pos and b1 != seq[pu]:
                continue
            for b2 in S.BASES:
                if pv in locked_pos and b2 != seq[pv]:
                    continue
                if (b1 + b2) in S.VALID_SET:
                    continue
                tl_u = list(seq)
                tl_u[pu], tl_u[pv] = b1, b2
                s_u = "".join(tl_u)
                if S.budget_violation(s_u, pinfo) > cur_vb:
                    continue
                ms_u, me_u = S.exact_fold(s_u, eng)
                dbp_u = len(t_bps ^ S.get_bp_set(ms_u))
                de_u = round(float(RNA.energy_of_struct(s_u, target)) - me_u, 4)
                cand_key = (dbp_u, de_u)
                if best_cand is None or cand_key < best_cand[0]:
                    best_cand = (cand_key, s_u, ms_u, (pu, pv))
        if best_cand is not None:
            seeds.append(best_cand[1:])
    return seeds


def run_depth2_cutting_plane_on_window(
    cur_seq: str,
    ms: str,
    pinfo: dict,
    eng: int,
    win_spec: tuple,
    rng: random.Random,
    deadline: float,
    max_cp_steps: int = 18,
) -> tuple:
    """
    Executes the slimmed `< 0.5 s` 2-Stage Pruned Cartesian Beam + Iterative Cutting-Plane +
    `Law R5/R12` External Stem Re-Orthogonalization over `W_2 = W_1 x d2`.
    """
    if time.time() >= deadline:
        return False, cur_seq, S.budget_violation(cur_seq, pinfo), 999, 999.0, ms

    w1_pairs, w1_unp, d2_pairs, d2_unp, forbid_pairs, extra_rivals = win_spec
    w1_pairs = w1_pairs[:3]
    w1_unp = w1_unp[:4]
    d2_pairs = d2_pairs[:3]
    d2_unp = d2_unp[:3 if len(d2_pairs) <= 1 else 2]

    target = pinfo["target"]
    pair_of = pinfo["pair_of"]
    allowed_pairs = pinfo["allowed_pairs"]
    t_bps = S.get_bp_set(target)
    m_bps = S.get_bp_set(ms)
    miss = sorted(t_bps - m_bps)

    cur_vb = S.budget_violation(cur_seq, pinfo)
    cur_dbp = len(t_bps ^ m_bps)
    cur_de = round(float(RNA.energy_of_struct(cur_seq, target)) - float(RNA.energy_of_struct(cur_seq, ms)), 4)

    all_pairs = w1_pairs + d2_pairs
    all_unp = w1_unp + d2_unp
    if not all_pairs:
        return False, cur_seq, cur_vb, cur_dbp, cur_de, ms

    w1_pos_set = {i for uv in w1_pairs for i in uv} | set(w1_unp)
    prot_W2 = w1_pos_set | {i for uv in d2_pairs for i in uv} | set(d2_unp)

    def clamp_distant_open_defects(r_struct: str) -> str:
        """
        `Law R15` (Window-Clamped Distant-Defect Projection):
        Restores `(u, v) = ('(', ')')` for every distant target pair `(u, v) in (t_bps - r_bps)`
        whose endpoints lie `> 3` nt outside `prot_W2`, are currently unpaired (`'.', '.'`) in `r_struct`,
        and do not cross any base pair in `r_bps`.
        """
        if not r_struct or r_struct == target:
            return r_struct
        r_bps = S.get_bp_set(r_struct)
        open_t = sorted(t_bps - r_bps)
        if not open_t:
            return r_struct
        tl_r = None
        cur_r_bps = set(r_bps)
        for u, v in open_t:
            if r_struct[u] == "." and r_struct[v] == ".":
                if min(min(abs(u - p), abs(v - p)) for p in prot_W2) > 3:
                    if not any((u < x < v) ^ (u < y < v) for x, y in cur_r_bps):
                        if tl_r is None:
                            tl_r = list(r_struct)
                        tl_r[u], tl_r[v] = "(", ")"
                        cur_r_bps.add((u, v))
        return "".join(tl_r) if tl_r is not None else r_struct

    # Core Stage-1 rivals (`<= 5` structures for ultra-fast `< 0.12 s` Stage 1, including `open_both` per `Law R20a`)
    rivals_stage1 = []
    for uv in w1_pairs:
        rs = pinfo["open_pair_struct"][uv]
        if rs not in rivals_stage1:
            rivals_stage1.append(rs)
    if len(w1_pairs) >= 2:
        u1, v1 = w1_pairs[0]
        u2, v2 = w1_pairs[1]
        tl_2_s1 = list(pinfo["open_pair_struct"][(u1, v1)])
        tl_2_s1[u2], tl_2_s1[v2] = ".", "."
        rs_both = "".join(tl_2_s1)
        if rs_both != target and rs_both not in rivals_stage1:
            rivals_stage1.append(rs_both)
    ms_clamped = clamp_distant_open_defects(ms)
    if ms_clamped not in rivals_stage1 and ms_clamped != target:
        rivals_stage1.append(ms_clamped)
    for r_ex in extra_rivals:
        r_ex_c = clamp_distant_open_defects(r_ex)
        if r_ex_c and r_ex_c != target and r_ex_c not in rivals_stage1:
            rivals_stage1.append(r_ex_c)
    rivals_stage1 = rivals_stage1[:6]

    # Full Stage-2 initial rivals (`<= 6` structures)
    rivals = list(rivals_stage1)
    seen_r = set(rivals)

    def add_rival(r_s: str):
        r_c = clamp_distant_open_defects(r_s)
        if r_c and r_c != target and r_c not in seen_r:
            seen_r.add(r_c)
            rivals.append(r_c)

    for uv in d2_pairs:
        add_rival(pinfo["open_pair_struct"][uv])
    if len(w1_pairs) >= 2:
        u1, v1 = w1_pairs[0]
        u2, v2 = w1_pairs[1]
        tl_2 = list(pinfo["open_pair_struct"][(u1, v1)])
        tl_2[u2], tl_2[v2] = ".", "."
        add_rival("".join(tl_2))
    for r_s in extra_rivals:
        add_rival(r_s)
    for idx_u in all_unp[:2]:
        for ua, va in all_pairs[:2]:
            if abs(idx_u - ua) <= 3:
                add_rival(build_local_slip_struct(target, pair_of, ((idx_u, va),), ((ua, va),)))
            if abs(idx_u - va) <= 3:
                add_rival(build_local_slip_struct(target, pair_of, ((ua, idx_u),), ((ua, va),)))
    rivals = rivals[:6]
    seen_r = set(rivals)

    # --- Stage 1: Enumerate `W_1` (`w1_pairs[:3]` x `w1_unp[:4]`, with `Law R20a` + `Law R22d` Full 6-Pair Domain & Legality Filter) ---
    miss_set = set(miss)
    p1_doms = []
    for idx_p1, uv in enumerate(w1_pairs):
        cur_bp_uv = cur_seq[uv[0]] + cur_seq[uv[1]]
        if idx_p1 == 2 and len(w1_unp) == 4 and uv not in miss_set:
            flip_bp_uv = cur_bp_uv[1] + cur_bp_uv[0]
            st_dom2 = tuple(bp for bp in allowed_pairs[uv] if bp in (cur_bp_uv, flip_bp_uv) or bp in S.STRONG_PAIRS)[:2]
            p1_doms.append(st_dom2 if st_dom2 else allowed_pairs[uv][:2])
        elif uv in miss_set or len(w1_pairs) <= 2 or len(w1_unp) <= 3 or pinfo["max_limits"]["GC"] < len(pinfo["pairs"]) // 3:
            p1_doms.append(allowed_pairs[uv])
        else:
            st_dom = tuple(bp for bp in allowed_pairs[uv] if bp in S.STRONG_PAIRS or bp == cur_bp_uv)
            p1_doms.append(st_dom if st_dom else allowed_pairs[uv])
    u1_doms = [S.BASES for _ in w1_unp]
    w1_forbid = [(pu, pv) for pu, pv in forbid_pairs if pu in w1_pos_set and pv in w1_pos_set]
    rivals_stage1_meta = [(r_s, sorted(S.get_bp_set(r_s) - t_bps)) for r_s in rivals_stage1]
    rivals_stage2_meta = [(r_s, sorted(S.get_bp_set(r_s) - t_bps)) for r_s in rivals]

    trial_1 = list(cur_seq)
    w1_states = []
    for p1_vals in itertools.product(*p1_doms):
        if time.time() >= deadline:
            break
        for (ua, va), bpa in zip(w1_pairs, p1_vals):
            trial_1[ua], trial_1[va] = bpa[0], bpa[1]
        for u1_vals in itertools.product(*u1_doms):
            for idx_u, ch_u in zip(w1_unp, u1_vals):
                trial_1[idx_u] = ch_u
            if w1_forbid and any((trial_1[pu] + trial_1[pv]) in S.VALID_SET for pu, pv in w1_forbid):
                continue
            s_1 = "".join(trial_1)
            et_1 = float(RNA.energy_of_struct(s_1, target))
            worst_1 = -1e9
            sum_pos_1 = 0.0
            for r_s, extra_r1 in rivals_stage1_meta:
                if extra_r1 and not all((s_1[x] + s_1[y]) in S.VALID_SET for x, y in extra_r1):
                    continue
                d_r = et_1 - float(RNA.energy_of_struct(s_1, r_s))
                if d_r > worst_1:
                    worst_1 = d_r
                if d_r > -0.1:
                    sum_pos_1 += d_r + 0.1
            if worst_1 < -1e8:
                worst_1 = 0.0
            w1_states.append((round(worst_1, 4), round(sum_pos_1, 4), round(et_1, 4), p1_vals, u1_vals))

    if not w1_states or time.time() >= deadline:
        return False, cur_seq, cur_vb, cur_dbp, cur_de, ms

    w1_states.sort(key=lambda x: (x[0], x[1], x[2]))

    # Determine beam width `B_1` (`<= 128`, max `2,048` joint states in `states_W2`) with `Law R13` on `d2_pairs`
    p2_doms = []
    for uv in d2_pairs:
        cur_bp_uv = cur_seq[uv[0]] + cur_seq[uv[1]]
        if uv in miss_set or pinfo["max_limits"]["GC"] < len(pinfo["pairs"]) // 3:
            p2_doms.append(allowed_pairs[uv])
        else:
            st_dom = tuple(bp for bp in allowed_pairs[uv] if bp in S.STRONG_PAIRS or bp == cur_bp_uv)
            p2_doms.append(st_dom if st_dom else allowed_pairs[uv])
    u2_doms = [S.BASES for _ in d2_unp]
    d2_card = 1
    for dom in p2_doms:
        d2_card *= len(dom)
    for dom in u2_doms:
        d2_card *= len(dom)

    if d2_card <= 1:
        beam_b1 = min(len(w1_states), 512)
    else:
        beam_b1 = max(8, min(len(w1_states), 128, 2048 // max(1, d2_card)))

    top_w1 = w1_states[:beam_b1]

    # --- Stage 2: Cross `top_w1` with Depth-2 Cartesian Product (`<= 2,048` states) ---
    w2_forbid = [(pu, pv) for pu, pv in forbid_pairs if pu in prot_W2 or pv in prot_W2]

    states_W2 = []
    trial_2 = list(cur_seq)
    d2_combos = list(itertools.product(itertools.product(*p2_doms), itertools.product(*u2_doms)))

    for _w1, _sp1, _et1, p1_vals, u1_vals in top_w1:
        if time.time() >= deadline:
            break
        for (ua, va), bpa in zip(w1_pairs, p1_vals):
            trial_2[ua], trial_2[va] = bpa[0], bpa[1]
        for idx_u, ch_u in zip(w1_unp, u1_vals):
            trial_2[idx_u] = ch_u
        for p2_vals, u2_vals in d2_combos:
            for (ub, vb), bpb in zip(d2_pairs, p2_vals):
                trial_2[ub], trial_2[vb] = bpb[0], bpb[1]
            for idx_u2, ch_u2 in zip(d2_unp, u2_vals):
                trial_2[idx_u2] = ch_u2
            if w2_forbid and any((trial_2[pu] + trial_2[pv]) in S.VALID_SET for pu, pv in w2_forbid):
                continue
            s_2 = "".join(trial_2)
            et_2 = float(RNA.energy_of_struct(s_2, target))
            worst_2 = -1e9
            for r_s, extra_r2 in rivals_stage2_meta:
                if extra_r2 and not all((s_2[x] + s_2[y]) in S.VALID_SET for x, y in extra_r2):
                    continue
                d_r = round(et_2 - float(RNA.energy_of_struct(s_2, r_s)), 4)
                if d_r > worst_2:
                    worst_2 = d_r
            if worst_2 < -1e8:
                worst_2 = 0.0
            states_W2.append([worst_2, et_2, s_2])

    if not states_W2:
        return False, cur_seq, cur_vb, cur_dbp, cur_de, ms

    # --- Stage 3: Iterative Cutting-Plane Loop (`max_cp_steps = 18`, `reo_calls < 2` at `w_b <= 0.05`) ---
    improved = False
    reo_calls = 0
    for _cp_step in range(max_cp_steps):
        if time.time() >= deadline:
            break
        best_idx = min(range(len(states_W2)), key=lambda i: (states_W2[i][0], states_W2[i][1]))
        w_b, et_b, s_b = states_W2[best_idx]
        if w_b > max(0.50, cur_de + 0.20):
            break
        states_W2[best_idx][0] = 999.0

        new_rivals_to_add = []
        for s_rep in S.repair_budget_candidates(list(s_b), pinfo, prot_W2, ms, rng, max_k=3)[:3]:
            if time.time() >= deadline:
                break
            tvb = S.budget_violation(s_rep, pinfo)
            if tvb > cur_vb:
                continue
            fms, fme = S.exact_fold(s_rep, eng)
            t_m_bps = S.get_bp_set(fms)
            tdbp = len(t_bps ^ t_m_bps)
            tde = round(float(RNA.energy_of_struct(s_rep, target)) - fme, 4)

            if tdbp == 0 and tvb == 0:
                ok, _, _ = S.check_full_solve(s_rep, pinfo, eng)
                if ok:
                    return True, s_rep, 0, 0, 0.0, pinfo["target"]

            fms_clamped = clamp_distant_open_defects(fms)
            if fms_clamped not in seen_r and fms_clamped != target:
                seen_r.add(fms_clamped)
                new_rivals_to_add.append(fms_clamped)

            # Trigger `Law R5 + Law R12 + Law R18a + Law R19a` External Stem Re-Orthogonalization when `w_b <= 0.25` and `reo_calls < 5`
            ext_extra = [(x, y) for x, y in (t_m_bps - t_bps) if x not in prot_W2 or y not in prot_W2]
            if ext_extra and w_b <= 0.25 and reo_calls < 5 and time.time() < deadline:
                reo_calls += 1
                s_reo, ms_reo, dbp_reo, de_reo = reorthogonalize_external_stems(
                    s_rep,
                    fms,
                    pinfo,
                    prot_W2,
                    req_bps=all_pairs,
                    eng=eng,
                    rng=rng,
                    init_rivals=rivals[-5:] + [fms_clamped],
                    deadline=deadline,
                    max_steps=10,
                    max_cands=14,
                )
                vb_reo = S.budget_violation(s_reo, pinfo)
                if dbp_reo == 0 and vb_reo == 0:
                    ok, _, _ = S.check_full_solve(s_reo, pinfo, eng)
                    if ok:
                        return True, s_reo, 0, 0, 0.0, pinfo["target"]
                ms_reo_clamped = clamp_distant_open_defects(ms_reo)
                if ms_reo_clamped not in seen_r and ms_reo_clamped != target:
                    seen_r.add(ms_reo_clamped)
                    new_rivals_to_add.append(ms_reo_clamped)
                if vb_reo <= tvb and (dbp_reo < tdbp or (dbp_reo == tdbp and de_reo < tde)):
                    s_rep, fms, tdbp, tde, tvb = s_reo, ms_reo, dbp_reo, de_reo, vb_reo
                # `Law R18b` (Inside-Out Seam-First Hard Anchor Lock + Global Multi-Stem CEGIS):
                # When `w_b <= 0.15` (local seam closed/near-closed) and external defects remain,
                # lock `prot_W2` in `pinfo_seam` and run global multi-stem CEGIS (`<= 0.7s`).
                rem_ext_extra = [(x, y) for x, y in (S.get_bp_set(fms) - t_bps) if x not in prot_W2 or y not in prot_W2]
                if rem_ext_extra and w_b <= 0.15 and reo_calls <= 2 and time.time() + 0.15 < deadline:
                    pinfo_seam = lock_seam_anchor_in_pinfo(pinfo, s_rep, prot_W2)
                    t_rem = max(0.08, min(0.45, (deadline - time.time()) * 0.45))
                    ok_mm, s_mm, vb_mm, dbp_mm, de_mm = S.cegis_rival_minimax_pass(s_rep, pinfo_seam, eng, rng, max_sec=t_rem)
                    if ok_mm and vb_mm == 0 and dbp_mm == 0:
                        ok_full, _, _ = S.check_full_solve(s_mm, pinfo, eng)
                        if ok_full:
                            return True, s_mm, 0, 0, 0.0, pinfo["target"]
                    if time.time() + 0.08 < deadline:
                        t_cl = max(0.08, min(0.45, (deadline - time.time()) * 0.45))
                        ok_cl, s_cl, vb_cl, dbp_cl, de_cl = S.fast_mfe_seam_climber(
                            s_mm, pinfo_seam, eng, rng, max_sec=t_cl, strict_manifold=True
                        )
                        if ok_cl and vb_cl == 0 and dbp_cl == 0:
                            ok_full, _, _ = S.check_full_solve(s_cl, pinfo, eng)
                            if ok_full:
                                return True, s_cl, 0, 0, 0.0, pinfo["target"]
                        if (vb_cl, dbp_cl, de_cl) < (vb_mm, dbp_mm, de_mm):
                            s_mm, vb_mm, dbp_mm, de_mm = s_cl, vb_cl, dbp_cl, de_cl
                    if vb_mm <= tvb and (dbp_mm < tdbp or (dbp_mm == tdbp and de_mm < tde)):
                        fms_mm, _ = S.exact_fold(s_mm, eng)
                        fms_mm_c = clamp_distant_open_defects(fms_mm)
                        if fms_mm_c not in seen_r and fms_mm_c != target:
                            seen_r.add(fms_mm_c)
                            new_rivals_to_add.append(fms_mm_c)
                        s_rep, fms, tdbp, tde, tvb = s_mm, fms_mm, dbp_mm, de_mm, vb_mm

            is_new_tie = (tvb == 0 and tde == 0.0 and cur_de > 0.0 and tdbp <= cur_dbp + 1)
            if (tvb, tdbp, tde) < (cur_vb, cur_dbp, cur_de) or is_new_tie:
                oms, ome = S.exact_official_fold(s_rep, eng)
                odbp = len(t_bps ^ S.get_bp_set(oms))
                ode = round(float(RNA.energy_of_struct(s_rep, target)) - ome, 4)
                ovb = S.budget_violation(s_rep, pinfo)
                if odbp == 0 and ovb == 0:
                    return True, s_rep, 0, 0, 0.0, oms
                if (ovb, odbp, ode) < (cur_vb, cur_dbp, cur_de) or (ovb == 0 and ode == 0.0 and cur_de > 0.0 and odbp <= cur_dbp + 1):
                    cur_seq, cur_vb, cur_dbp, cur_de, ms = s_rep, ovb, odbp, ode, oms
                    improved = True

        for r_new in new_rivals_to_add:
            rivals.append(r_new)
            extra_rn = sorted(S.get_bp_set(r_new) - t_bps)
            for st in states_W2:
                if st[0] < 900.0:
                    if not extra_rn or all((st[2][x] + st[2][y]) in S.VALID_SET for x, y in extra_rn):
                        d_n = round(st[1] - float(RNA.energy_of_struct(st[2], r_new)), 4)
                        if d_n > st[0]:
                            st[0] = d_n

    return improved, cur_seq, cur_vb, cur_dbp, cur_de, ms


def detect_serial_loop_chains(pinfo: dict) -> list:
    """
    `Law R21b` + `Law R22a`: Detects maximal unbranched serial loop-chain subtrees
    `chain_pairs = [(u_0, v_0), ..., (u_{L-1}, v_{L-1})]` (`len(chain_pairs) >= 3` with `>= 2` internal/bulge loop steps),
    always anchored at the true unbranched subtree root `(u_0, v_0)` so `sub_T = target[a_f : b_f + 1]` spans the full
    subtree without mid-stem truncation.
    """
    sorted_pairs = sorted(pinfo["pairs"], key=lambda uv: (uv[0], -uv[1]))
    parent_of_uv = {}
    children_of_uv = {uv: [] for uv in sorted_pairs}
    stack_uv = []
    for uv in sorted_pairs:
        while stack_uv and not (stack_uv[-1][0] < uv[0] and uv[1] < stack_uv[-1][1]):
            stack_uv.pop()
        if stack_uv:
            parent_of_uv[uv] = stack_uv[-1]
            children_of_uv[stack_uv[-1]].append(uv)
        else:
            parent_of_uv[uv] = None
        stack_uv.append(uv)

    chains = []
    for uv in sorted_pairs:
        par = parent_of_uv[uv]
        if par is None or len(children_of_uv[par]) >= 2:
            ch = [uv]
            curr = uv
            ok_chain = True
            while children_of_uv[curr]:
                if len(children_of_uv[curr]) > 1:
                    ok_chain = False
                    break
                curr = children_of_uv[curr][0]
                ch.append(curr)
            if ok_chain and len(ch) >= 3:
                num_loops = sum(
                    1
                    for k in range(len(ch) - 1)
                    if (ch[k + 1][0] - ch[k][0]) > 1 or (ch[k][1] - ch[k + 1][1]) > 1
                )
                if num_loops >= 2:
                    chains.append(ch)
    return chains


def solve_flanked_serial_chain_zero_wobble(
    cur_seq: str,
    ms: str,
    chain_pairs: list,
    pinfo: dict,
    eng: int,
    deadline: float,
    max_solved: int = 8,
) -> tuple:
    """
    `Law R21b` + `Law R22a` Helper: Solves a single 1-nt flanked serial loop-chain slice `[a_f, b_f]` (`sub_T = target[a_f : b_f + 1]`)
    by enforcing opposite chiralities `p_bits[k] != p_bits[k + 1]` across 1-nt bulge steps, evaluating pure-purine
    motifs on `2x2` (`GAGA` / existing `UGUG`), `1x1` (`GG, AG`), `1x2`/`2x1` (`GAG, AGA, GGA, AGG, GAA`), 1-nt bulges (`A`),
    multi-nt bulges `bulge_multi` (`A` interior + `(b_0, b_{-1})` corner dangle optimization + inner closing wobble option),
    and a 35-step cutting-plane loop over `cands_sub`.
    Returns `(a_f, b_f, sub_T, solved_full_seqs)`.
    """
    target = pinfo["target"]
    pair_of = pinfo["pair_of"]
    locked_pos = pinfo["locked_pos"]
    allowed_pairs = pinfo["allowed_pairs"]
    n = pinfo["n"]

    u0, v0 = chain_pairs[0]
    a_f = u0 - 1 if (u0 > 0 and pair_of[u0 - 1] == -1) else u0
    b_f = v0 + 1 if (v0 + 1 < n and pair_of[v0 + 1] == -1) else v0
    sub_T = target[a_f : b_f + 1]
    tb_sub = S.get_bp_set(sub_T)

    bulge1_steps = []
    bulge1_pos = []
    bulge_multi = []
    large_bulge_inner_pairs = set()
    loops_22 = []
    loops_11 = []
    loops_12 = []
    loops_1m = []
    loops_mn = []
    for k in range(len(chain_pairs) - 1):
        uk, vk = chain_pairs[k]
        uk1, vk1 = chain_pairs[k + 1]
        l_unp = list(range(uk + 1, uk1))
        r_unp = list(range(vk1 + 1, vk))
        if len(l_unp) + len(r_unp) == 1:
            bulge1_steps.append(k)
            bulge1_pos.extend(l_unp + r_unp)
        elif (len(l_unp) >= 2 and len(r_unp) == 0) or (len(l_unp) == 0 and len(r_unp) >= 2):
            b_seq = l_unp if l_unp else r_unp
            bulge_multi.append(tuple(b_seq))
            if len(b_seq) >= 6:
                large_bulge_inner_pairs.add((uk1, vk1))
        elif len(l_unp) == 2 and len(r_unp) == 2:
            loops_22.append((l_unp[0], l_unp[1], r_unp[0], r_unp[1]))
        elif len(l_unp) == 1 and len(r_unp) == 1:
            loops_11.append((l_unp[0], r_unp[0]))
        elif (len(l_unp), len(r_unp)) in ((1, 2), (2, 1)):
            loops_12.append(((l_unp + r_unp)[0], (l_unp + r_unp)[1], (l_unp + r_unp)[2], len(l_unp) == 2))
        elif min(len(l_unp), len(r_unp)) == 1 and max(len(l_unp), len(r_unp)) >= 3:
            if len(l_unp) == 1:
                loops_1m.append((l_unp[0], r_unp[0], r_unp[-1], tuple(r_unp[1:-1])))
            else:
                loops_1m.append((r_unp[0], l_unp[0], l_unp[-1], tuple(l_unp[1:-1])))
        elif len(l_unp) >= 2 and len(r_unp) >= 2:
            loops_mn.append((l_unp[0], l_unp[-1], r_unp[0], r_unp[-1], tuple(l_unp[1:-1] + r_unp[1:-1])))

    u_hp, v_hp = chain_pairs[-1]
    hp_len = v_hp - u_hp - 1

    # Sanitize all loop interiors on the full chain (`base_tl`) before slicing `active_chain_pairs`
    base_tl = list(cur_seq)
    no_wob_req = pinfo.get("is_pure_shape", False) or (
        pinfo["min_limits"].get("GU", 0) == 0
        and pinfo["min_limits"].get("AU", 0) == 0
        and pinfo["max_limits"].get("GC", 999) >= len(pinfo["pairs"])
    )
    if no_wob_req:
        for u_c, v_c in chain_pairs:
            if u_c not in locked_pos and v_c not in locked_pos:
                if (base_tl[u_c] + base_tl[v_c]) not in ("GC", "CG") and "GC" in allowed_pairs[(u_c, v_c)]:
                    base_tl[u_c], base_tl[v_c] = ("G", "C") if base_tl[u_c] in ("G", "A") else ("C", "G")
    for b_pos in bulge1_pos:
        if b_pos not in locked_pos:
            base_tl[b_pos] = "A"
    for b_seq in bulge_multi:
        for b_pos in b_seq:
            if b_pos not in locked_pos:
                base_tl[b_pos] = "A"
    for p1, q1 in loops_11:
        for pos, ch in zip((p1, q1), ("G", "G")):
            if pos not in locked_pos:
                base_tl[pos] = ch
    for p1, p2, p3, _is_2x1 in loops_12:
        trio_def = ("A", "G", "G") if _is_2x1 else ("G", "A", "G")
        for pos, ch in zip((p1, p2, p3), trio_def):
            if pos not in locked_pos:
                base_tl[pos] = ch
    for p1, p2, q1, q2 in loops_22:
        cur_22 = (cur_seq[p1], cur_seq[p2], cur_seq[q1], cur_seq[q2])
        target_22 = cur_22 if cur_22 in (("U", "G", "U", "G"), ("G", "U", "G", "U")) else ("G", "A", "G", "A")
        for pos, ch in zip((p1, p2, q1, q2), target_22):
            if pos not in locked_pos:
                base_tl[pos] = ch
    for p_s, q_o, q_i, int_pos in loops_1m:
        for pos in int_pos:
            if pos not in locked_pos:
                base_tl[pos] = "A"
        for pos, ch in zip((p_s, q_o, q_i), ("G", "G", "A")):
            if pos not in locked_pos:
                base_tl[pos] = ch
    for l0, l_end, r0, r_end, int_pos in loops_mn:
        for pos in int_pos:
            if pos not in locked_pos:
                base_tl[pos] = "A"
        for pos, ch in zip((l0, r_end, l_end, r0), ("G", "A", "A", "G")):
            if pos not in locked_pos:
                base_tl[pos] = ch
    if hp_len == 4:
        for pos, ch in zip(range(u_hp + 1, v_hp), "GAAA"):
            if pos not in locked_pos:
                base_tl[pos] = ch
    elif hp_len == 3:
        for pos in range(u_hp + 1, v_hp):
            if pos not in locked_pos:
                base_tl[pos] = "A"
    elif hp_len >= 5:
        for pos in range(u_hp + 1, v_hp):
            if pos not in locked_pos:
                base_tl[pos] = "A"
        if (u_hp + 1) not in locked_pos:
            base_tl[u_hp + 1] = "G"

    # Center `active_chain_pairs` around the missing target pair `k_miss` when `len(chain_pairs) > 8` or `len(loops_12) >= 4`
    miss_set_ch = S.get_bp_set(target) - S.get_bp_set(ms)
    miss_indices = [idx_c for idx_c, uv_c in enumerate(chain_pairs) if uv_c in miss_set_ch]
    k_miss = miss_indices[0] if miss_indices else max(0, len(chain_pairs) - 3)
    u_miss = chain_pairs[k_miss][0]

    active_chain_pairs = list(chain_pairs)
    outer_chain_pairs = []
    active_bulge1_steps = list(bulge1_steps)
    if len(loops_12) >= 4 or len(chain_pairs) > 8:
        win_len = 5 if len(loops_12) >= 4 else 6
        win_len = min(win_len, len(chain_pairs))
        lo = max(0, min(len(chain_pairs) - win_len, k_miss - (win_len // 2)))
        hi = lo + win_len
        active_chain_pairs = chain_pairs[lo:hi]
        outer_chain_pairs = chain_pairs[:lo] + chain_pairs[hi:]
        active_bulge1_steps = [k - lo for k in bulge1_steps if lo <= k < hi - 1]
        u_lo, v_lo = active_chain_pairs[0]
        u_hi, v_hi = active_chain_pairs[-1]
        loops_11 = sorted(
            [lp for lp in loops_11 if u_lo < lp[0] < u_hi],
            key=lambda lp: abs(lp[0] - u_miss),
        )[:3]
        loops_12 = sorted(
            [lp for lp in loops_12 if u_lo < lp[0] < u_hi],
            key=lambda lp: abs(lp[0] - u_miss),
        )[:2]
        loops_22 = sorted(
            [lp for lp in loops_22 if u_lo < lp[0] < u_hi],
            key=lambda lp: abs(lp[0] - u_miss),
        )[:2]
        bulge_multi = sorted(
            [bm for bm in bulge_multi if u_lo < bm[0] < v_lo],
            key=lambda bm: abs(bm[0] - u_miss),
        )[:1]
        loops_1m = sorted(
            [lp for lp in loops_1m if u_lo < min(lp[0], lp[1]) < u_hi],
            key=lambda lp: abs(min(lp[0], lp[1]) - u_miss),
        )[:1]

    p_doms = []
    for uv in active_chain_pairs:
        base_bps = ("GC", "CG", "GU", "AU") if uv in large_bulge_inner_pairs else ("GC", "CG")
        st_dom = tuple(bp for bp in base_bps if bp in allowed_pairs[uv])
        p_doms.append(st_dom if st_dom else allowed_pairs[uv][:2])

    valid_p_bits = []
    for p_bits in itertools.product(*p_doms):
        if any(
            p_bits[k] == p_bits[k + 1] and len(p_doms[k]) > 1 and len(p_doms[k + 1]) > 1
            for k in active_bulge1_steps
        ):
            continue
        valid_p_bits.append(p_bits)

    doms_11 = []
    for p1, q1 in loops_11:
        d11 = [
            m
            for m in (("G", "G"), ("A", "G"))
            if (p1 not in locked_pos or m[0] == cur_seq[p1]) and (q1 not in locked_pos or m[1] == cur_seq[q1])
        ]
        doms_11.append(d11 if d11 else [(cur_seq[p1], cur_seq[q1])])

    doms_12 = []
    for p1, p2, p3, is_2x1 in loops_12:
        py_trio = ("G", "C", "A") if is_2x1 else ("A", "G", "C")
        trio_opts = (("G", "A", "G"), ("A", "G", "A"), ("G", "G", "A"), ("A", "G", "G"), py_trio, ("G", "A", "A")) if len(loops_12) <= 2 else (
            ("G", "A", "G"),
            ("A", "G", "A"),
            ("G", "G", "A"),
            ("A", "G", "G"),
            py_trio,
        )
        d12 = [
            m
            for m in trio_opts
            if (p1 not in locked_pos or m[0] == cur_seq[p1])
            and (p2 not in locked_pos or m[1] == cur_seq[p2])
            and (p3 not in locked_pos or m[2] == cur_seq[p3])
        ]
        doms_12.append(d12 if d12 else [(cur_seq[p1], cur_seq[p2], cur_seq[p3])])

    doms_bm = []
    for b_seq in bulge_multi[:2]:
        b0, b_end = b_seq[0], b_seq[-1]
        dbm = [
            m
            for m in (("A", "A"), ("G", "U"), ("A", "U"), ("G", "A"))
            if (b0 not in locked_pos or m[0] == cur_seq[b0]) and (b_end not in locked_pos or m[1] == cur_seq[b_end])
        ]
        doms_bm.append(dbm if dbm else [(cur_seq[b0], cur_seq[b_end])])

    doms_1m = []
    for p_s, q_o, q_i, _int_pos in loops_1m[:2]:
        d1m = [
            m
            for m in (("G", "G", "A"), ("A", "G", "G"), ("G", "A", "G"), ("A", "G", "A"))
            if (p_s not in locked_pos or m[0] == cur_seq[p_s])
            and (q_o not in locked_pos or m[1] == cur_seq[q_o])
            and (q_i not in locked_pos or m[2] == cur_seq[q_i])
        ]
        doms_1m.append(d1m if d1m else [(base_tl[p_s], base_tl[q_o], base_tl[q_i])])

    sub_rivals = []
    for u, v in active_chain_pairs:
        tl_r = list(sub_T)
        tl_r[u - a_f] = "."
        tl_r[v - a_f] = "."
        sub_rivals.append("".join(tl_r))
    for k in active_bulge1_steps:
        u1, v1 = active_chain_pairs[k]
        u2, v2 = active_chain_pairs[k + 1]
        tl_r = list(sub_T)
        tl_r[u1 - a_f] = "."
        tl_r[v1 - a_f] = "."
        tl_r[u2 - a_f] = "."
        tl_r[v2 - a_f] = "."
        sub_rivals.append("".join(tl_r))

    ext_flips = (0, 1, 2, 3) if outer_chain_pairs else (0,)
    cands_sub = []
    for ext_flip in ext_flips:
        tl_outer = list(base_tl)
        for r_idx, (u_o, v_o) in enumerate(outer_chain_pairs):
            cur_bp_o = tl_outer[u_o] + tl_outer[v_o]
            if ext_flip == 1:
                t_bp = cur_bp_o[1] + cur_bp_o[0]
            elif ext_flip == 2 and cur_bp_o in ("GC", "CG"):
                t_bp = "GC" if (r_idx % 2 == 0) else "CG"
            elif ext_flip == 3 and cur_bp_o in ("GC", "CG"):
                t_bp = "CG" if (r_idx % 2 == 0) else "GC"
            else:
                t_bp = cur_bp_o
            if t_bp in allowed_pairs[(u_o, v_o)]:
                tl_outer[u_o], tl_outer[v_o] = t_bp[0], t_bp[1]
        for p_bits in valid_p_bits:
            if time.time() >= deadline:
                break
            tl = list(tl_outer)
            for (u, v), bp in zip(active_chain_pairs, p_bits):
                tl[u], tl[v] = bp[0], bp[1]
            for vals_bm in itertools.product(*doms_bm):
                for b_seq, mbm in zip(bulge_multi[:2], vals_bm):
                    tl[b_seq[0]], tl[b_seq[-1]] = mbm
                for vals_1m in itertools.product(*doms_1m):
                    for (p_s, q_o, q_i, _ip), m1m in zip(loops_1m[:2], vals_1m):
                        tl[p_s], tl[q_o], tl[q_i] = m1m
                    for vals_11 in itertools.product(*doms_11):
                        for (p1, q1), m11 in zip(loops_11, vals_11):
                            tl[p1], tl[q1] = m11
                        for vals_12 in itertools.product(*doms_12):
                            for (p1, p2, p3, _is_2x1), m12 in zip(loops_12, vals_12):
                                tl[p1], tl[p2], tl[p3] = m12
                            sub_s = "".join(tl[a_f : b_f + 1])
                            et_s = float(RNA.energy_of_struct(sub_s, sub_T))
                            w_s = max(round(et_s - float(RNA.energy_of_struct(sub_s, r)), 4) for r in sub_rivals)
                            cands_sub.append([w_s, et_s, sub_s, "".join(tl)])

    cands_sub.sort(key=lambda x: (x[0], x[1]))
    pool_sub = []
    seen_sub = set()
    for item in cands_sub:
        if item[2] not in seen_sub:
            seen_sub.add(item[2])
            pool_sub.append(item)
            if len(pool_sub) >= 700:
                break

    solved_full = []
    best_near = []
    for _cp_step in range(36):
        if not pool_sub or time.time() >= deadline or len(solved_full) >= max_solved:
            break
        best_i = min(range(len(pool_sub)), key=lambda i: (pool_sub[i][0], pool_sub[i][1]))
        w_s, et_s, sub_s, full_s = pool_sub[best_i]
        if w_s > 500.0:
            break
        pool_sub[best_i][0] = 999.0
        ms_s, me_s = S.exact_fold(sub_s, eng)
        if ms_s == sub_T:
            solved_full.append(full_s)
            continue
        dbp_s = len(tb_sub ^ S.get_bp_set(ms_s))
        de_s = round(et_s - me_s, 4)
        best_near.append((dbp_s, de_s, full_s))
        extra_s = sorted(S.get_bp_set(ms_s) - tb_sub)
        for item in pool_sub:
            if item[0] < 900.0:
                s_i = item[2]
                if not extra_s or all((s_i[x] + s_i[y]) in S.VALID_SET for x, y in extra_s):
                    d_i = round(item[1] - float(RNA.energy_of_struct(s_i, ms_s)), 4)
                    if d_i > item[0]:
                        item[0] = d_i

    if not solved_full and a_f <= 1 and b_f >= n - 2 and best_near:
        best_near.sort(key=lambda x: (x[0], x[1]))
        solved_full = [x[2] for x in best_near[:2]]

    return a_f, b_f, sub_T, solved_full


def solve_serial_loop_chain_purine_pass(
    cur_seq: str,
    ms: str,
    cur_vb: int,
    cur_dbp: int,
    cur_de: float,
    pinfo: dict,
    eng: int,
    rng: random.Random,
    deadline: float,
) -> tuple:
    """
    `Law R21b` (Serial Loop-Chain Pure-Purine Trio & Opposite-Chirality 1-nt Bulge Pass):
    Solves unbranched serial loop-chain subtrees `[a_f, b_f]` (`d_bp_sub = 0`) and couples them to external stems
    (`ext_pairs`) with external internal-loop `5'-'G' / 3'-'A'` terminal mismatch stabilization and canonical
    cutting-plane search over external stem chiralities.
    """
    if time.time() >= deadline:
        return False, cur_seq, cur_vb, cur_dbp, cur_de, ms
    chains = detect_serial_loop_chains(pinfo)
    if not chains:
        return False, cur_seq, cur_vb, cur_dbp, cur_de, ms

    target = pinfo["target"]
    pair_of = pinfo["pair_of"]
    locked_pos = pinfo["locked_pos"]
    allowed_pairs = pinfo["allowed_pairs"]
    t_bps = S.get_bp_set(target)
    m_bps = S.get_bp_set(ms)
    miss_set = t_bps - m_bps

    sorted_pairs = sorted(pinfo["pairs"], key=lambda uv: (uv[0], -uv[1]))
    children_of_uv = {uv: [] for uv in sorted_pairs}
    stack_uv = []
    for uv in sorted_pairs:
        while stack_uv and not (stack_uv[-1][0] < uv[0] and uv[1] < stack_uv[-1][1]):
            stack_uv.pop()
        if stack_uv:
            children_of_uv[stack_uv[-1]].append(uv)
        stack_uv.append(uv)

    improved = False
    for ch_pairs in chains:
        if time.time() >= deadline:
            break
        if not any(uv in miss_set for uv in ch_pairs) and len(chains) > 1:
            continue

        # `Law R22a` (Multi-nt Bulge Corner Dangle Suppression): Test 5'/3' corner edits `(b_0, b_{-1})` on any
        # multi-nt bulge (`len >= 2`) inside `ch_pairs`, which suppresses exterior/multiloop 5' purine dangle onto
        # the inner stem when the outer stem opens (e.g. `#5423472 Interference`: `b_{25} = 'U'` -> `de_mfe = 0.03`).
        for k_b in range(len(ch_pairs) - 1):
            uk_b, vk_b = ch_pairs[k_b]
            uk1_b, vk1_b = ch_pairs[k_b + 1]
            l_unp_b = list(range(uk_b + 1, uk1_b))
            r_unp_b = list(range(vk1_b + 1, vk_b))
            if (len(l_unp_b) >= 2 and len(r_unp_b) == 0) or (len(l_unp_b) == 0 and len(r_unp_b) >= 2):
                b_seq_b = l_unp_b if l_unp_b else r_unp_b
                b0_p, bend_p = b_seq_b[0], b_seq_b[-1]
                for c0_b, cend_b in (
                    (cur_seq[b0_p], "U"),
                    (cur_seq[b0_p], "C"),
                    ("G", "U"),
                    ("A", "U"),
                    ("A", "A"),
                    ("G", "A"),
                ):
                    if (b0_p in locked_pos and c0_b != cur_seq[b0_p]) or (bend_p in locked_pos and cend_b != cur_seq[bend_p]):
                        continue
                    tl_b = list(cur_seq)
                    tl_b[b0_p], tl_b[bend_p] = c0_b, cend_b
                    st_b = "".join(tl_b)
                    if st_b == cur_seq or S.budget_violation(st_b, pinfo) > cur_vb:
                        continue
                    fms_b, fme_b = S.exact_fold(st_b, eng)
                    dbp_b = len(t_bps ^ S.get_bp_set(fms_b))
                    de_b = round(float(RNA.energy_of_struct(st_b, target)) - fme_b, 4)
                    vb_b = S.budget_violation(st_b, pinfo)
                    if (vb_b, dbp_b, de_b) < (cur_vb, cur_dbp, cur_de) or (vb_b == cur_vb and de_b < cur_de and dbp_b <= cur_dbp + 3):
                        oms, ome = S.exact_official_fold(st_b, eng)
                        odbp = len(t_bps ^ S.get_bp_set(oms))
                        ode = round(float(RNA.energy_of_struct(st_b, target)) - ome, 4)
                        ovb = S.budget_violation(st_b, pinfo)
                        if (ovb, odbp, ode) < (cur_vb, cur_dbp, cur_de):
                            cur_seq, cur_vb, cur_dbp, cur_de, ms = st_b, ovb, odbp, ode, oms
                            improved = True
                            if cur_dbp == 0 and cur_vb == 0:
                                return True, cur_seq, 0, 0, 0.0, ms

        a_f, b_f, _sub_T, solved_subs = solve_flanked_serial_chain_zero_wobble(
            cur_seq, ms, ch_pairs, pinfo, eng, deadline, max_solved=8
        )
        if not solved_subs:
            continue

        for st0 in solved_subs:
            vb0 = S.budget_violation(st0, pinfo)
            if vb0 <= cur_vb:
                fms0, fme0 = S.exact_fold(st0, eng)
                dbp0 = len(t_bps ^ S.get_bp_set(fms0))
                de0 = round(float(RNA.energy_of_struct(st0, target)) - fme0, 4)
                if (vb0, dbp0, de0) < (cur_vb, cur_dbp, cur_de):
                    oms, ome = S.exact_official_fold(st0, eng)
                    odbp = len(t_bps ^ S.get_bp_set(oms))
                    ode = round(float(RNA.energy_of_struct(st0, target)) - ome, 4)
                    if (vb0, odbp, ode) < (cur_vb, cur_dbp, cur_de):
                        cur_seq, cur_vb, cur_dbp, cur_de, ms = st0, vb0, odbp, ode, oms
                        improved = True
                        if cur_dbp == 0 and cur_vb == 0:
                            return True, cur_seq, 0, 0, 0.0, ms

        ext_pairs = [uv for uv in pinfo["pairs"] if uv[0] < a_f or uv[1] > b_f]
        if not ext_pairs:
            continue

        if len(ext_pairs) <= 8 and pinfo.get("is_pure_shape", False) and time.time() + 0.3 < deadline:
            ext_doms = []
            for uv_e in ext_pairs:
                st_d = tuple(bp for bp in ("GC", "CG") if bp in allowed_pairs[uv_e])
                ext_doms.append(st_d if st_d else allowed_pairs[uv_e][:2])
            ext_open_rivals = [pinfo["open_pair_struct"][uv_e] for uv_e in ext_pairs]
            pool = []
            for st0 in solved_subs:
                tl_base = list(st0)
                # Boost external single-child internal loops (`5'` boundary `'G'`, `3'` boundary `'A'`)
                for u_out, v_out in ext_pairs:
                    if len(children_of_uv.get((u_out, v_out), [])) == 1:
                        u_in, v_in = children_of_uv[(u_out, v_out)][0]
                        if (u_in, v_in) in ext_pairs and (u_in - u_out) > 1 and (v_out - v_in) > 1:
                            for p_5 in (u_out + 1, u_in - 1):
                                if p_5 not in locked_pos and pair_of[p_5] == -1:
                                    tl_base[p_5] = "G"
                            for p_3 in (v_out - 1, v_in + 1):
                                if p_3 not in locked_pos and pair_of[p_3] == -1:
                                    tl_base[p_3] = "A"
                for e_bits in itertools.product(*ext_doms):
                    tl = list(tl_base)
                    for (u_e, v_e), bp_e in zip(ext_pairs, e_bits):
                        tl[u_e], tl[v_e] = bp_e[0], bp_e[1]
                    st_cand = "".join(tl)
                    et_c = float(RNA.energy_of_struct(st_cand, target))
                    w0 = max(round(et_c - float(RNA.energy_of_struct(st_cand, r_e)), 4) for r_e in ext_open_rivals)
                    pool.append([w0, et_c, st_cand])

            for _cp_step in range(36):
                if not pool or time.time() >= deadline:
                    break
                best_i = min(range(len(pool)), key=lambda i: (pool[i][0], pool[i][1]))
                w_p, et_p, st_p = pool[best_i]
                if w_p > 500.0:
                    break
                pool[best_i][0] = 999.0
                fms_p, fme_p = S.exact_fold(st_p, eng)
                mbps_p = S.get_bp_set(fms_p)
                dbp_p = len(t_bps ^ mbps_p)
                de_p = round(et_p - fme_p, 4)
                vb_p = S.budget_violation(st_p, pinfo)
                if (vb_p, dbp_p, de_p) < (cur_vb, cur_dbp, cur_de):
                    oms, ome = S.exact_official_fold(st_p, eng)
                    odbp = len(t_bps ^ S.get_bp_set(oms))
                    ode = round(float(RNA.energy_of_struct(st_p, target)) - ome, 4)
                    ovb = S.budget_violation(st_p, pinfo)
                    if (ovb, odbp, ode) < (cur_vb, cur_dbp, cur_de):
                        cur_seq, cur_vb, cur_dbp, cur_de, ms = st_p, ovb, odbp, ode, oms
                        improved = True
                        if cur_dbp == 0 and cur_vb == 0:
                            return True, cur_seq, 0, 0, 0.0, ms
                extra_p = sorted(mbps_p - t_bps)
                for item in pool:
                    if item[0] < 900.0:
                        seq_i = item[2]
                        if not extra_p or all((seq_i[x] + seq_i[y]) in S.VALID_SET for x, y in extra_p):
                            d_i = round(item[1] - float(RNA.energy_of_struct(seq_i, fms_p)), 4)
                            if d_i > item[0]:
                                item[0] = d_i

    return improved, cur_seq, cur_vb, cur_dbp, cur_de, ms


def solve_multiloop_collective_ring_pass(
    cur_seq: str,
    ms: str,
    cur_vb: int,
    cur_dbp: int,
    cur_de: float,
    pinfo: dict,
    eng: int,
    rng: random.Random,
    deadline: float,
) -> tuple:
    """
    `Law R22c` (Multiloop Collective Ring & Bulge-Step Cutting-Plane Pass):
    When a puzzle with `>= 2` multiloop branches or `<= 12` total pairs has `0 < cur_dbp <= 2`,
    sanitizes non-`'A'` unpaired multiloop ring bases at distance `>= 2` from branch pairs to `'A'`,
    evaluates `5'` pyrimidine (`'C'`) / `3'` purine (`'G'`) multiloop terminal dangles, and runs a
    36-step cutting-plane search over up to `11` pairs enforcing opposite chirality (`GC` over `CG`)
    across `1`-nt bulges (`-3.40` vs `-3.30 kcal/mol` in Turner 1999).
    """
    if time.time() >= deadline or cur_dbp == 0 or cur_dbp > 2:
        return False, cur_seq, cur_vb, cur_dbp, cur_de, ms

    target = pinfo["target"]
    pair_of = pinfo["pair_of"]
    locked_pos = pinfo["locked_pos"]
    allowed_pairs = pinfo["allowed_pairs"]
    n = pinfo["n"]
    t_bps = S.get_bp_set(target)
    m_bps = S.get_bp_set(ms)
    miss_set = t_bps - m_bps

    sorted_pairs = sorted(pinfo["pairs"], key=lambda uv: (uv[0], -uv[1]))
    children_of_uv = {uv: [] for uv in sorted_pairs}
    stack_uv = []
    for uv in sorted_pairs:
        while stack_uv and not (stack_uv[-1][0] < uv[0] and uv[1] < stack_uv[-1][1]):
            stack_uv.pop()
        if stack_uv:
            children_of_uv[stack_uv[-1]].append(uv)
        stack_uv.append(uv)

    multiloop_roots = [uv for uv, chs in children_of_uv.items() if len(chs) >= 2]
    if not multiloop_roots and len(sorted_pairs) > 11:
        return False, cur_seq, cur_vb, cur_dbp, cur_de, ms

    improved = False
    base_tl = list(cur_seq)

    # Identify multiloop ring unpaired bases and adjacent 5'/3' multiloop dangles
    ml_5p_dangles = []
    for u_r, v_r in multiloop_roots:
        chs = children_of_uv[(u_r, v_r)]
        branch_endpoints = {u_r, v_r}
        for uc, vc in chs:
            branch_endpoints.add(uc)
            branch_endpoints.add(vc)
            if uc - 1 > u_r and pair_of[uc - 1] == -1 and (uc - 1) not in locked_pos:
                ml_5p_dangles.append(uc - 1)
        if v_r - 1 > chs[-1][1] and pair_of[v_r - 1] == -1 and (v_r - 1) not in locked_pos:
            ml_5p_dangles.append(v_r - 1)
        # Sanitize unlocked unpaired bases inside the multiloop ring that are not 3'-adjacent to a branch pair
        three_prime_adj = {u_r + 1} | {vc + 1 for _uc, vc in chs}
        for idx_m in range(u_r + 1, v_r):
            if any(uc <= idx_m <= vc for uc, vc in chs):
                continue
            if pair_of[idx_m] == -1 and idx_m not in locked_pos and idx_m not in three_prime_adj:
                if base_tl[idx_m] in ("G", "U"):
                    base_tl[idx_m] = "A"

    # Also sanitize any 1-nt bulge unpaired bases to `'A'` if unlocked
    bulge1_pairs = []
    for uv, chs in children_of_uv.items():
        if len(chs) == 1:
            u_o, v_o = uv
            u_i, v_i = chs[0]
            l_u = list(range(u_o + 1, u_i))
            r_u = list(range(v_i + 1, v_o))
            if len(l_u) + len(r_u) == 1:
                bulge1_pairs.append((uv, chs[0]))
                b_idx = (l_u + r_u)[0]
                if b_idx not in locked_pos:
                    base_tl[b_idx] = "A"

    if len(sorted_pairs) <= 11:
        active_pairs = list(sorted_pairs)
    else:
        anchor = min(miss_set) if miss_set else sorted_pairs[0]
        active_pairs = sorted(
            sorted_pairs,
            key=lambda uv: min(abs(uv[0] - anchor[0]) + abs(uv[1] - anchor[1]), abs(uv[0] - anchor[1])),
        )[:10]
        active_pairs.sort(key=lambda uv: (uv[0], -uv[1]))

    active_index = {uv: idx for idx, uv in enumerate(active_pairs)}
    active_b1 = [
        (active_index[uv1], active_index[uv2])
        for uv1, uv2 in bulge1_pairs
        if uv1 in active_index and uv2 in active_index
    ]

    p_doms = []
    for uv in active_pairs:
        st_d = tuple(bp for bp in ("GC", "CG") if bp in allowed_pairs[uv])
        p_doms.append(st_d if st_d else allowed_pairs[uv][:2])

    valid_p_bits = []
    for p_bits in itertools.product(*p_doms):
        if any(
            p_bits[i1] == p_bits[i2] and len(p_doms[i1]) > 1 and len(p_doms[i2]) > 1
            for i1, i2 in active_b1
        ):
            continue
        valid_p_bits.append(p_bits)

    ml_5p_dangles = sorted(set(ml_5p_dangles))[:4]
    dangle_presets = [tuple(cur_seq[p] for p in ml_5p_dangles)]
    if ml_5p_dangles:
        c_preset = tuple("C" for _ in ml_5p_dangles)
        a_preset = tuple("A" for _ in ml_5p_dangles)
        for pr in (c_preset, a_preset):
            if pr not in dangle_presets:
                dangle_presets.append(pr)

    open_rivals = [pinfo["open_pair_struct"][uv] for uv in active_pairs]
    if ms != target:
        open_rivals.append(ms)

    pool = []
    for d_pr in dangle_presets:
        tl_d = list(base_tl)
        for p_d, ch_d in zip(ml_5p_dangles, d_pr):
            tl_d[p_d] = ch_d
        for p_bits in valid_p_bits:
            if time.time() >= deadline:
                break
            tl = list(tl_d)
            for (u, v), bp in zip(active_pairs, p_bits):
                tl[u], tl[v] = bp[0], bp[1]
            s_cand = "".join(tl)
            if S.budget_violation(s_cand, pinfo) > cur_vb:
                continue
            et_c = float(RNA.energy_of_struct(s_cand, target))
            w0 = max(
                round(et_c - float(RNA.energy_of_struct(s_cand, r_s)), 4)
                for r_s in open_rivals[:4]
            )
            pool.append([w0, et_c, s_cand])

    for _cp_step in range(36):
        if not pool or time.time() >= deadline:
            break
        best_i = min(range(len(pool)), key=lambda i: (pool[i][0], pool[i][1]))
        w_p, et_p, st_p = pool[best_i]
        if w_p > 500.0:
            break
        pool[best_i][0] = 999.0
        fms_p, fme_p = S.exact_fold(st_p, eng)
        mbps_p = S.get_bp_set(fms_p)
        dbp_p = len(t_bps ^ mbps_p)
        de_p = round(et_p - fme_p, 4)
        vb_p = S.budget_violation(st_p, pinfo)
        if (vb_p, dbp_p, de_p) < (cur_vb, cur_dbp, cur_de):
            oms, ome = S.exact_official_fold(st_p, eng)
            odbp = len(t_bps ^ S.get_bp_set(oms))
            ode = round(float(RNA.energy_of_struct(st_p, target)) - ome, 4)
            ovb = S.budget_violation(st_p, pinfo)
            if (ovb, odbp, ode) < (cur_vb, cur_dbp, cur_de):
                cur_seq, cur_vb, cur_dbp, cur_de, ms = st_p, ovb, odbp, ode, oms
                improved = True
                if cur_dbp == 0 and cur_vb == 0:
                    return True, cur_seq, 0, 0, 0.0, ms
        extra_p = sorted(mbps_p - t_bps)
        for item in pool:
            if item[0] < 900.0:
                seq_i = item[2]
                if not extra_p or all((seq_i[x] + seq_i[y]) in S.VALID_SET for x, y in extra_p):
                    d_i = round(item[1] - float(RNA.energy_of_struct(seq_i, fms_p)), 4)
                    if d_i > item[0]:
                        item[0] = d_i

    return improved, cur_seq, cur_vb, cur_dbp, cur_de, ms


def detect_independent_subtrees(target: str, pair_of: list) -> list:
    """
    `Law R16` (Independent Subtree Decomposition):
    Identifies top-level exterior-loop-separated balanced subtrees `[a_m, b_m]` (`m = 1..k`)
    where `pair_of[a_m] == b_m` and no target base pair encloses `[a_m, b_m]`.
    When `k >= 2`, each subtree `T_m = target[a_m : b_m + 1]` is an independent thermodynamic
    folding unit coupled to `T_{m'}` (`m' != m`) only through exterior-loop coaxial stacking
    and cross-subtree parasitic hybridization.
    """
    subtrees = []
    i = 0
    n = len(target)
    while i < n:
        if pair_of[i] > i:
            j = pair_of[i]
            subtrees.append((i, j))
            i = j + 1
        else:
            i += 1
    return subtrees if len(subtrees) >= 2 else []


def reflect_subtree_variant(sub_seq: str, sub_target: str, sub_locks: str, mode: int = 0) -> str:
    """
    `Law R19b` (Whole-Subtree / Outer-Trunk Watson-Crick Chirality Reflection):
    - `mode == 0`: Reflects all unlocked pairs `(u, v)` inside `sub_target` (`GC<->CG, AU<->UA, GU<->UG`).
    - `mode == 1`: Reflects only the outer trunk stem of `sub_target`.
    - `mode == 2`: Reflects only the interior stems (`u > trunk_len`) of `sub_target`.
    """
    pair_of_sub, pairs_sub, _, _ = S.parse_structure(sub_target)
    trunk_len = 0
    while trunk_len < len(sub_target) // 2 and pair_of_sub[trunk_len] == len(sub_target) - 1 - trunk_len:
        trunk_len += 1
    tl = list(sub_seq)
    for u, v in pairs_sub:
        if sub_locks[u] == "x" or sub_locks[v] == "x":
            continue
        if mode == 1 and u >= trunk_len:
            continue
        if mode == 2 and u < trunk_len:
            continue
        tl[u], tl[v] = tl[v], tl[u]
    return "".join(tl)


def generate_subtree_4state_variants(sub_seq: str, sub_target: str, sub_locks: str) -> list:
    """
    `Law R23a` (4-State Alternating-Helix Dictionary `{"orig", "reflect", "alt_0", "alt_1"}` on Subtree Stems):
    Breaks parallel `"GGG..."` / `"CCC..."` homopolymer runs inside helices of length `>= 2` by enumerating
    combinations of `("orig", "reflect", "alt_0" [GC,CG,GC,...], "alt_1" [CG,GC,CG,...])` across up to 3 stems.
    """
    variants = [sub_seq]
    for mode_r in (0, 1, 2):
        rcm = reflect_subtree_variant(sub_seq, sub_target, sub_locks, mode=mode_r)
        if rcm not in variants:
            variants.append(rcm)

    pair_of_sub, pairs_sub, _, _ = S.parse_structure(sub_target)
    sorted_ps = sorted(pairs_sub, key=lambda uv: (uv[0], -uv[1]))
    visited_ps = set()
    stems = []
    for u0, v0 in sorted_ps:
        if (u0, v0) in visited_ps:
            continue
        st = [(u0, v0)]
        visited_ps.add((u0, v0))
        cu, cv = u0, v0
        while (cu + 1, cv - 1) in visited_ps or (cu + 1 < cv - 1 and pair_of_sub[cu + 1] == cv - 1):
            cu, cv = cu + 1, cv - 1
            if (cu, cv) in visited_ps:
                break
            visited_ps.add((cu, cv))
            st.append((cu, cv))
        if len(st) >= 2:
            stems.append(st)

    stems.sort(key=len, reverse=True)
    active_stems = stems[:3]
    if not active_stems:
        return variants

    for modes_tup in itertools.product(("orig", "reflect", "alt_0", "alt_1"), repeat=len(active_stems)):
        if all(m == "orig" for m in modes_tup):
            continue
        tl = list(sub_seq)
        for st, m_st in zip(active_stems, modes_tup):
            if m_st == "orig":
                continue
            for r_idx, (u, v) in enumerate(st):
                if sub_locks[u] == "x" or sub_locks[v] == "x":
                    continue
                cur_bp = tl[u] + tl[v]
                if m_st == "reflect":
                    t_bp = cur_bp[1] + cur_bp[0]
                elif m_st == "alt_0":
                    t_bp = ("GC" if r_idx % 2 == 0 else "CG") if cur_bp in ("GC", "CG") else (cur_bp[1] + cur_bp[0] if r_idx % 2 == 1 else cur_bp)
                else:  # "alt_1"
                    t_bp = ("CG" if r_idx % 2 == 0 else "GC") if cur_bp in ("GC", "CG") else (cur_bp[1] + cur_bp[0] if r_idx % 2 == 0 else cur_bp)
                tl[u], tl[v] = t_bp[0], t_bp[1]
        v_str = "".join(tl)
        if v_str not in variants:
            variants.append(v_str)
    return variants


_GLOBAL_SUBTREE_DB = None
_GLOBAL_TWIN_DB = None


def get_global_subtree_db() -> tuple:
    """
    `Law R26a` (Cross-Puzzle Twin & Subtree Transfer Database across 300 Puzzles):
    Lazily builds:
      - `_GLOBAL_TWIN_DB[core_t]`: list of `(d_bp, de_mfe, pid_d, core_seq_d)` for whole stripped targets `core_t`,
      - `_GLOBAL_SUBTREE_DB[sub_t]`: list of `(d_bp, de_mfe, pid_d, sub_seq_d)` for every paired span `sub_t` (`len >= 6`).
    """
    global _GLOBAL_SUBTREE_DB, _GLOBAL_TWIN_DB
    if _GLOBAL_SUBTREE_DB is not None and _GLOBAL_TWIN_DB is not None:
        return _GLOBAL_SUBTREE_DB, _GLOBAL_TWIN_DB

    sub_db = {}
    twin_db = {}
    for g_d in (1, 2, 3):
        csv_p = os.path.join(BASE_DIR, f"eterna-hard/groups/eterna-hard-group{g_d}.csv")
        ck_p = os.path.join(BASE_DIR, f"ckpt_group{g_d}.json")
        if not (os.path.exists(csv_p) and os.path.exists(ck_p)):
            continue
        rows_d = {str(r["puzzle_id"]): r for r in csv.DictReader(open(csv_p, "r", encoding="utf-8"))}
        ck_d = json.load(open(ck_p, "r", encoding="utf-8"))
        for pid_d, res_d in ck_d.items():
            if pid_d not in rows_d or res_d.get("v_budget", 0) > 0:
                continue
            t_d = rows_d[pid_d]["structure"].strip()
            a_cd = t_d.find("(")
            b_cd = t_d.rfind(")")
            if a_cd == -1 or b_cd <= a_cd:
                continue
            core_t_d = t_d[a_cd : b_cd + 1]
            dbp_d = int(res_d.get("d_bp", 99))
            de_d = float(res_d.get("de_mfe", 99.0))
            seqs_d = [res_d["sequence"]]
            if res_d.get("exact_tie_seq") and res_d["exact_tie_seq"] not in seqs_d:
                seqs_d.append(res_d["exact_tie_seq"])
            # Parse pairs of `t_d`
            st_p = []
            pairs_d = []
            for idx_c, ch_c in enumerate(t_d):
                if ch_c == "(":
                    st_p.append(idx_c)
                elif ch_c == ")" and st_p:
                    pairs_d.append((st_p.pop(), idx_c))
            for s_d in seqs_d:
                if len(s_d) != len(t_d):
                    continue
                core_s_d = s_d[a_cd : b_cd + 1]
                twin_db.setdefault(core_t_d, []).append((dbp_d, de_d, pid_d, core_s_d))
                for u_d, v_d in pairs_d:
                    if v_d - u_d + 1 >= 6:
                        sub_t_d = t_d[u_d : v_d + 1]
                        sub_s_d = s_d[u_d : v_d + 1]
                        sub_db.setdefault(sub_t_d, []).append((dbp_d, de_d, pid_d, sub_s_d))

    for k_t in list(twin_db.keys()):
        items = sorted(twin_db[k_t], key=lambda x: (x[0], x[1]))
        dedup = []
        seen_s = set()
        for it in items:
            if it[3] not in seen_s:
                seen_s.add(it[3])
                dedup.append(it)
        twin_db[k_t] = dedup[:16]

    for k_s in list(sub_db.keys()):
        items = sorted(sub_db[k_s], key=lambda x: (x[0], x[1]))
        dedup = []
        seen_s = set()
        for it in items:
            if it[3] not in seen_s:
                seen_s.add(it[3])
                dedup.append(it)
        sub_db[k_s] = dedup[:16]

    _GLOBAL_SUBTREE_DB = sub_db
    _GLOBAL_TWIN_DB = twin_db
    return _GLOBAL_SUBTREE_DB, _GLOBAL_TWIN_DB


def project_sequence_to_locks(seq_cand: str, pinfo: dict) -> str:
    """Enforces `locked_pos` on `seq_cand` and repairs any broken Watson-Crick/wobble pair partner."""
    tl = list(seq_cand)
    locked_pos = pinfo["locked_pos"]
    pair_of = pinfo["pair_of"]
    begin = pinfo["begin"]
    for idx_l in locked_pos:
        tl[idx_l] = begin[idx_l]
    for idx_l in locked_pos:
        q_l = pair_of[idx_l]
        if q_l != -1 and q_l not in locked_pos:
            bp_cur = (tl[idx_l] + tl[q_l]) if idx_l < q_l else (tl[q_l] + tl[idx_l])
            uv_key = (min(idx_l, q_l), max(idx_l, q_l))
            allowed_uv = pinfo["allowed_pairs"].get(uv_key, S.VALID_PAIRS)
            if bp_cur not in allowed_uv:
                wc_map = {"G": "C", "C": "G", "A": "U", "U": "A"}
                comp_b = wc_map.get(tl[idx_l], "A")
                tl[q_l] = comp_b
    return "".join(tl)


def run_cross_puzzle_graft_pass(
    cur_seq: str,
    ms: str,
    cur_vb: int,
    cur_dbp: int,
    cur_de: float,
    row: dict,
    pinfo: dict,
    eng: int,
    rng: random.Random,
    deadline: float,
) -> tuple:
    """
    `Law R26a`: Warm-start cross-puzzle twin transfer (with lock projection, isomorphic subtree swaps,
    and 1-pair `GC -> AU/UA/GU/UG` budget repair) and multi-subtree composite grafting (`len >= 15`).
    """
    if time.time() >= deadline:
        return False, cur_seq, cur_vb, cur_dbp, cur_de, ms

    sub_db, twin_db = get_global_subtree_db()
    pid = str(pinfo["puzzle_id"])
    target = pinfo["target"]
    t_bps = S.get_bp_set(target)
    pair_of = pinfo["pair_of"]
    locked_pos = pinfo["locked_pos"]
    improved = False

    def try_eval_candidate(s_try: str) -> None:
        nonlocal cur_seq, cur_vb, cur_dbp, cur_de, ms, improved
        if s_try == cur_seq:
            return
        vb_try = S.budget_violation(s_try, pinfo)
        if vb_try > cur_vb:
            return
        fms, fme = S.exact_fold(s_try, eng)
        dbp_try = len(t_bps ^ S.get_bp_set(fms))
        de_try = round(float(RNA.energy_of_struct(s_try, target)) - fme, 4)
        is_tie = (vb_try == 0 and de_try == 0.0 and cur_de > 0.0 and dbp_try <= cur_dbp + 1)
        if (vb_try, dbp_try, de_try) < (cur_vb, cur_dbp, cur_de) or is_tie:
            oms, ome = S.exact_official_fold(s_try, eng)
            odbp = len(t_bps ^ S.get_bp_set(oms))
            ode = round(float(RNA.energy_of_struct(s_try, target)) - ome, 4)
            ovb = S.budget_violation(s_try, pinfo)
            if (ovb, odbp, ode) < (cur_vb, cur_dbp, cur_de) or (ovb == 0 and ode == 0.0 and cur_de > 0.0 and odbp <= cur_dbp + 1):
                cur_seq, cur_vb, cur_dbp, cur_de, ms = s_try, ovb, odbp, ode, oms
                improved = True

    # 1. Whole-Core Twin Transfer (`_GLOBAL_TWIN_DB[core_t]`)
    a_c = target.find("(")
    b_c = target.rfind(")")
    if a_c != -1 and b_c > a_c:
        core_t = target[a_c : b_c + 1]
        donors_twin = [it for it in twin_db.get(core_t, []) if it[2] != pid]
        subtrees_top = detect_independent_subtrees(target, pair_of)
        for _d_dbp, _d_de, _pid_d, core_s_d in donors_twin[:6]:
            if time.time() >= deadline:
                break
            tl_base = list(cur_seq)
            for idx_u in range(len(tl_base)):
                if pair_of[idx_u] == -1 and idx_u not in locked_pos:
                    tl_base[idx_u] = "A"
            tl_base[a_c : b_c + 1] = list(core_s_d)
            s_raw_d = "".join(tl_base)
            s_proj = project_sequence_to_locks(s_raw_d, pinfo)
            try_eval_candidate(s_proj)
            if cur_dbp == 0 and cur_vb == 0:
                return True, cur_seq, 0, 0, 0.0, ms

            # If isomorphic outer subtrees exist in `s_raw_d` (e.g. `#3163385 II2L` vs `#3161590`), test swapping them + 1-pair closing flip
            if len(subtrees_top) >= 2:
                for i_st in range(len(subtrees_top)):
                    for j_st in range(i_st + 1, len(subtrees_top)):
                        am_i, bm_i = subtrees_top[i_st]
                        am_j, bm_j = subtrees_top[j_st]
                        if target[am_i : bm_i + 1] == target[am_j : bm_j + 1]:
                            tl_sw = list(s_raw_d)
                            tl_sw[am_i : bm_i + 1], tl_sw[am_j : bm_j + 1] = (
                                list(s_raw_d[am_j : bm_j + 1]),
                                list(s_raw_d[am_i : bm_i + 1]),
                            )
                            s_sw = project_sequence_to_locks("".join(tl_sw), pinfo)
                            try_eval_candidate(s_sw)
                            for am_k, bm_k in subtrees_top:
                                if pair_of[am_k] == bm_k and am_k not in locked_pos and bm_k not in locked_pos:
                                    for bp_k in ("AU", "UA", "GU", "UG", "GC", "CG"):
                                        if bp_k in pinfo["allowed_pairs"][(am_k, bm_k)]:
                                            tl_k = list(s_sw)
                                            tl_k[am_k], tl_k[bm_k] = bp_k[0], bp_k[1]
                                            try_eval_candidate("".join(tl_k))

            # If `s_proj` violates budget by `1..2` (e.g. `#2713892 Respond - Level 2` from `#5390849`), scan 1-pair `GC -> AU/UA/GU/UG` conversions
            vb_proj = S.budget_violation(s_proj, pinfo)
            if 1 <= vb_proj <= 2 and time.time() + 0.2 < deadline:
                best_rep = None
                for u_p, v_p in pinfo["pairs"]:
                    if u_p in locked_pos or v_p in locked_pos:
                        continue
                    if (s_proj[u_p] + s_proj[v_p]) not in ("GC", "CG"):
                        continue
                    for bp_w in ("AU", "UA", "GU", "UG"):
                        if bp_w not in pinfo["allowed_pairs"][(u_p, v_p)]:
                            continue
                        tl_w = list(s_proj)
                        tl_w[u_p], tl_w[v_p] = bp_w[0], bp_w[1]
                        s_w = "".join(tl_w)
                        if S.budget_violation(s_w, pinfo) == 0:
                            try_eval_candidate(s_w)
                            et_w = float(RNA.energy_of_struct(s_w, target))
                            if best_rep is None or et_w < best_rep[0]:
                                best_rep = (et_w, s_w)
                # Also try 1-pair conversion + Stage 2d / window pass if `best_rep` has low target energy
                if best_rep is not None:
                    try_eval_candidate(best_rep[1])

    # 2. Multi-Subtree Composite & Single-Subtree Grafts (`len >= 15`, e.g. `#3436111`, `#3308173`, `#5683000`, `#5031820`)
    if cur_dbp > 0 and time.time() + 0.25 < deadline:
        ms_bps = S.get_bp_set(ms)
        miss_bps = t_bps - ms_bps
        cand_spans = []
        for u_p, v_p in sorted(pinfo["pairs"], key=lambda uv: -(uv[1] - uv[0])):
            span_len = v_p - u_p + 1
            if span_len < 15 or span_len >= pinfo["n"] - 2:
                continue
            sub_t_p = target[u_p : v_p + 1]
            donors_p = [it for it in sub_db.get(sub_t_p, []) if it[2] != pid and it[0] <= 3]
            if not donors_p:
                continue
            if any(u_p <= x_m < y_m <= v_p for x_m, y_m in miss_bps):
                cand_spans.append((u_p, v_p, sub_t_p, donors_p))

        # Select maximal non-overlapping spans for composite graft
        non_overlap_spans = []
        for u_p, v_p, sub_t_p, donors_p in cand_spans:
            if not any(not (v_p < u_q or u_p > v_q) for u_q, v_q, _, _ in non_overlap_spans):
                non_overlap_spans.append((u_p, v_p, sub_t_p, donors_p))

        if non_overlap_spans:
            tl_comp = list(cur_seq)
            for idx_u in range(len(tl_comp)):
                if pair_of[idx_u] == -1 and idx_u not in locked_pos:
                    if not any(u_q <= idx_u <= v_q for u_q, v_q, _, _ in non_overlap_spans):
                        tl_comp[idx_u] = "A"
            for u_p, v_p, sub_t_p, donors_p in non_overlap_spans:
                best_sub_s = donors_p[0][3]
                for _d_dbp, _d_de, _pid_d, sub_s_d in donors_p[:4]:
                    if S.exact_fold(sub_s_d, eng)[0] == sub_t_p:
                        best_sub_s = sub_s_d
                        break
                tl_comp[u_p : v_p + 1] = list(best_sub_s)
                # Also test single-span graft on `cur_seq`
                tl_single = list(cur_seq)
                tl_single[u_p : v_p + 1] = list(best_sub_s)
                s_single = project_sequence_to_locks("".join(tl_single), pinfo)
                try_eval_candidate(s_single)
            s_comp = project_sequence_to_locks("".join(tl_comp), pinfo)
            try_eval_candidate(s_comp)

    return improved, cur_seq, cur_vb, cur_dbp, cur_de, ms


def run_independent_subtrees_pass(
    cur_seq: str,
    ms: str,
    cur_vb: int,
    cur_dbp: int,
    cur_de: float,
    row: dict,
    pinfo: dict,
    eng: int,
    rng: random.Random,
    deadline: float,
) -> tuple:
    """
    `Law R16` + `Law R19b` + `Law R21d` + `Law R22b` + `Law R23a` + `Law R23b`:
    Optimizes each top-level independent subtree on its 1-nt flanked slice `[a_m_f, b_m_f]`, sanitizes loop interiors
    and strips wobbles to form clean 0-wobble seeds, expands each subtree over the 4-state alternating-helix dictionary
    `{"orig", "reflect", "alt_0", "alt_1"}`, pre-screens adjacent subtrees (`a_{m+1} - b_m <= 2`) on their joint slice,
    and runs a cutting-plane pass over valid combinations.
    """
    target = pinfo["target"]
    pair_of = pinfo["pair_of"]
    locked_pos = pinfo["locked_pos"]
    n = pinfo["n"]
    t_bps = S.get_bp_set(target)
    subtrees = detect_independent_subtrees(target, pair_of)
    peeled_trunk_pairs = []
    peel_bounds = (0, n - 1)
    if len(subtrees) < 2 and time.time() < deadline:
        # `Law R24b` (Matryoshka Peel-Trunk Multi-Branch Subtree Decomposition):
        # When `roots == 1`, walk inward along single-child pairs to the first enclosing multiloop `(u_r, v_r)`.
        sorted_pairs_pt = sorted(pinfo["pairs"], key=lambda uv: (uv[0], -uv[1]))
        children_pt = {uv: [] for uv in sorted_pairs_pt}
        top_roots_pt = []
        stack_pt = []
        for uv in sorted_pairs_pt:
            while stack_pt and not (stack_pt[-1][0] < uv[0] and uv[1] < stack_pt[-1][1]):
                stack_pt.pop()
            if stack_pt:
                children_pt[stack_pt[-1]].append(uv)
            else:
                top_roots_pt.append(uv)
            stack_pt.append(uv)
        if len(top_roots_pt) == 1:
            curr_uv = top_roots_pt[0]
            trunk_chain = [curr_uv]
            while len(children_pt[curr_uv]) == 1:
                curr_uv = children_pt[curr_uv][0]
                trunk_chain.append(curr_uv)
            if len(children_pt[curr_uv]) >= 2:
                u_r, v_r = curr_uv
                subtrees = list(children_pt[curr_uv])
                peeled_trunk_pairs = trunk_chain
                peel_bounds = (u_r + 1, v_r - 1)

    if len(subtrees) < 2 or time.time() >= deadline:
        return False, cur_seq, cur_vb, cur_dbp, cur_de, ms

    # Sanitize unlocked exterior-loop / multiloop-ring unpaired bases outside `[a_m, b_m]` to `'A'`
    base_full_lst = list(cur_seq)
    in_any_sub = set()
    for a_m, b_m in subtrees:
        for idx_s in range(a_m, b_m + 1):
            in_any_sub.add(idx_s)
    p_lo, p_hi = peel_bounds
    for idx_e in range(p_lo, p_hi + 1):
        if idx_e not in in_any_sub and pair_of[idx_e] == -1 and idx_e not in locked_pos:
            base_full_lst[idx_e] = "A"
    base_full_seq = "".join(base_full_lst)

    req_gu = pinfo["min_limits"].get("GU", 0)
    req_au = pinfo["min_limits"].get("AU", 0)
    max_gc = pinfo["max_limits"].get("GC", 999)
    min_non_gc = max(req_gu + req_au, max(0, len(pinfo["pairs"]) - max_gc))
    need_non_gc = min_non_gc > 0
    every_sub_needs_wobble = (min_non_gc == len(subtrees)) and not peeled_trunk_pairs

    improved = False
    flanked_spans = []
    sub_pair_coords = []
    sub_pools = []
    for a_m, b_m in subtrees:
        a_f = a_m - 1 if (a_m > p_lo and pair_of[a_m - 1] == -1) else a_m
        b_f = b_m + 1 if (b_m < p_hi and pair_of[b_m + 1] == -1) else b_m
        flanked_spans.append((a_f, b_f))
        sub_pair_coords.append([(u_p - a_f, v_p - a_f) for u_p, v_p in pinfo["pairs"] if a_m <= u_p < v_p <= b_m])
        sub_t = target[a_f : b_f + 1]
        sub_l = pinfo["locks"][a_f : b_f + 1]
        sub_b = pinfo["begin"][a_f : b_f + 1]
        s0_m = base_full_seq[a_f : b_f + 1]
        cands_0 = []

        row_m = {
            "puzzle_id": f"{pinfo['puzzle_id']}_{a_f}",
            "title": pinfo["title"],
            "folder": pinfo["folder"],
            "structure": sub_t,
            "locks": sub_l,
            "begin_sequence": sub_b,
            "constraints": "",
        }
        pinfo_m = S.parse_puzzle_constraints(row_m)
        ms_m, _ = S.exact_fold(s0_m, eng)
        if ms_m == sub_t:
            cands_0.append(s0_m)

        # `Law R24a`: Sanitize unlocked loop-interior bases on `s0_m` BEFORE stripping wobbles (`tl_san_orig`, e.g. `#5423472 Interference`)
        tl_san_orig = list(s0_m)
        changed_san_orig = False
        for idx_u in range(len(sub_t)):
            if pinfo_m["pair_of"][idx_u] == -1 and idx_u not in pinfo_m["locked_pos"]:
                if not any(abs(idx_u - u_p) <= 1 or abs(idx_u - v_p) <= 1 for u_p, v_p in pinfo_m["pairs"]):
                    if tl_san_orig[idx_u] != "A":
                        tl_san_orig[idx_u] = "A"
                        changed_san_orig = True
        if changed_san_orig:
            s_san_orig = "".join(tl_san_orig)
            if S.exact_fold(s_san_orig, eng)[0] == sub_t and s_san_orig not in cands_0:
                cands_0.append(s_san_orig)
            # Also test 3'-corner purine/pyrimidine edits on any multi-nt bulge inside `tl_san_orig`
            for k_p in range(len(pinfo_m["pairs"]) - 1):
                uk_p, vk_p = pinfo_m["pairs"][k_p]
                uk1_p, vk1_p = pinfo_m["pairs"][k_p + 1]
                if (uk1_p - uk_p - 1) >= 4 and (vk_p - vk1_p - 1) == 0:
                    b_end_p = uk1_p - 1
                    if b_end_p not in pinfo_m["locked_pos"]:
                        for ch_c in ("A", "G", "U"):
                            tl_c = list(tl_san_orig)
                            tl_c[b_end_p] = ch_c
                            sc_b = "".join(tl_c)
                            if S.exact_fold(sc_b, eng)[0] == sub_t and sc_b not in cands_0:
                                cands_0.append(sc_b)

        # `Law R22b + Law R23a`: Strip wobbles AND sanitize unlocked unpaired interior bases in `s0_m`
        tl_strip = list(s0_m)
        changed_strip = False
        for u_p, v_p in pinfo_m["pairs"]:
            if (tl_strip[u_p] + tl_strip[v_p]) not in ("GC", "CG") and "GC" in pinfo_m["allowed_pairs"][(u_p, v_p)]:
                tl_strip[u_p], tl_strip[v_p] = ("G", "C") if tl_strip[u_p] in ("G", "A") else ("C", "G")
                changed_strip = True
        if changed_strip:
            s_strip = "".join(tl_strip)
            ms_st, _ = S.exact_fold(s_strip, eng)
            if ms_st == sub_t and s_strip not in cands_0:
                cands_0.append(s_strip)

        tl_san = list(tl_strip)
        changed_san = False
        for idx_u in range(len(sub_t)):
            if pinfo_m["pair_of"][idx_u] == -1 and idx_u not in pinfo_m["locked_pos"]:
                if not any(abs(idx_u - u_p) <= 1 or abs(idx_u - v_p) <= 1 for u_p, v_p in pinfo_m["pairs"]):
                    if tl_san[idx_u] != "A":
                        tl_san[idx_u] = "A"
                        changed_san = True
        if changed_san:
            s_san = "".join(tl_san)
            if S.exact_fold(s_san, eng)[0] == sub_t and s_san not in cands_0:
                cands_0.append(s_san)

        # 1. Try `Law R21b + Law R22a + Law R23c` serial loop-chain solver on `pinfo_m`
        if time.time() + 0.3 < deadline:
            chains_m = detect_serial_loop_chains(pinfo_m)
            for ch_m in chains_m:
                _af_c, _bf_c, _st_c, solved_ch = solve_flanked_serial_chain_zero_wobble(
                    s0_m, ms_m, ch_m, pinfo_m, eng, deadline, max_solved=4
                )
                for sc in solved_ch:
                    if sc not in cands_0:
                        cands_0.append(sc)

        # 2. Try `build_depth2_windows` on `pinfo_m` if not yet solved in isolation
        if not cands_0 and time.time() + 0.4 < deadline:
            sub_dl = min(deadline, time.time() + min(1.8, (deadline - time.time()) * 0.35))
            s_work_m, ms_work_m = (s_strip, ms_st) if changed_strip else (s0_m, ms_m)
            for win_m in build_depth2_windows(s_work_m, ms_work_m, pinfo_m, eng, sub_dl)[:3]:
                if time.time() >= sub_dl:
                    break
                imp_m, ns_m, _nvb_m, ndbp_m, _nde_m, nms_m = run_depth2_cutting_plane_on_window(
                    s_work_m, ms_work_m, pinfo_m, eng, win_m, rng, deadline=sub_dl, max_cp_steps=12
                )
                if imp_m:
                    s_work_m, ms_work_m = ns_m, nms_m
                    if ndbp_m == 0 and ns_m not in cands_0:
                        cands_0.append(ns_m)

        if s0_m not in cands_0:
            cands_0.append(s0_m)

        # 3. `Law R21d + Law R22b + Law R23a/b + Law R24a + Law R25b`: Generate 1-wobble (`cands_1w`) and 2-wobble (`cands_2w`) solved variants of `[a_f, b_f]`
        cands_1w = []
        cands_2w = []
        c0_has_solved = any(S.exact_fold(sc0, eng)[0] == sub_t for sc0 in cands_0)
        if (need_non_gc or not c0_has_solved) and time.time() + 0.25 < deadline:
            if min_non_gc > req_gu + req_au or not need_non_gc:
                wobble_bps = ("GU", "UG", "AU", "UA")
            elif req_gu > 0 and req_au == 0:
                wobble_bps = ("GU", "UG")
            elif req_au > 0 and req_gu == 0:
                wobble_bps = ("AU", "UA")
            else:
                wobble_bps = ("GU", "UG", "AU", "UA")

            s0_wobs = sum(1 for u_p, v_p in pinfo_m["pairs"] if (s0_m[u_p] + s0_m[v_p]) not in ("GC", "CG"))
            if s0_wobs >= 2 and ms_m == sub_t:
                for v4 in generate_subtree_4state_variants(s0_m, sub_t, sub_l)[:12]:
                    if S.exact_fold(v4, eng)[0] == sub_t and v4 not in cands_2w:
                        cands_2w.append(v4)

            u_hp_m, v_hp_m = pinfo_m["pairs"][-1]
            non_hp_m = [
                u_i
                for u_i in range(len(sub_t))
                if pinfo_m["pair_of"][u_i] == -1
                and u_i not in pinfo_m["locked_pos"]
                and not (u_i == 0 and a_f < a_m)
                and not (u_i == len(sub_t) - 1 and b_f > b_m)
                and not (u_hp_m < u_i < v_hp_m)
            ]
            if len(pinfo_m["pairs"]) <= 5 and len(non_hp_m) <= 6:
                p_doms_m = [
                    tuple(bp for bp in (("GC", "CG") + wobble_bps) if bp in pinfo["allowed_pairs"][(a_f + u_p, a_f + v_p)])
                    for u_p, v_p in pinfo_m["pairs"]
                ]
                has_22_m = len(non_hp_m) == 4 and any(
                    (pinfo_m["pairs"][k_s + 1][0] - pinfo_m["pairs"][k_s][0] - 1) == 2
                    and (pinfo_m["pairs"][k_s][1] - pinfo_m["pairs"][k_s + 1][1] - 1) == 2
                    for k_s in range(len(pinfo_m["pairs"]) - 1)
                )
                if has_22_m:
                    u_choices_m = (("G", "A", "G", "A"), ("U", "G", "U", "G"), ("G", "U", "G", "U"), ("A", "A", "A", "A"))
                elif len(non_hp_m) <= 4:
                    u_choices_m = tuple(itertools.product(("A", "G"), repeat=len(non_hp_m)))
                elif len(non_hp_m) == 5:
                    u_choices_m = (
                        ("A", "G", "G", "G", "G"),
                        ("G", "A", "G", "G", "G"),
                        ("G", "G", "G", "A", "G"),
                        ("G", "G", "A", "G", "G"),
                        ("A", "G", "A", "A", "G"),
                        ("G", "A", "A", "A", "G"),
                    )
                else:
                    u_choices_m = (
                        ("G", "A", "G", "G", "A", "G"),
                        ("A", "G", "G", "G", "A", "G"),
                        ("G", "A", "G", "A", "G", "G"),
                        ("A", "G", "G", "A", "G", "G"),
                    )
                want_2w = (min_non_gc > len(subtrees)) or (s0_wobs >= 2)
                sub_enum_dl = min(deadline, time.time() + 1.1)
                for p_bits_m in itertools.product(*p_doms_m):
                    if time.time() >= sub_enum_dl:
                        break
                    n_w_bits = sum(1 for bp in p_bits_m if bp in wobble_bps)
                    if n_w_bits == 1 and len(cands_1w) >= 56:
                        continue
                    if n_w_bits != 1 and not (want_2w and n_w_bits == 2 and len(cands_2w) < 32):
                        continue
                    for u_vals_m in u_choices_m:
                        tl_w = list(s0_m)
                        for idx_i in range(len(sub_t)):
                            if pinfo_m["pair_of"][idx_i] == -1 and idx_i not in pinfo_m["locked_pos"]:
                                tl_w[idx_i] = "A"
                        if (v_hp_m - u_hp_m - 1) >= 4 and (u_hp_m + 1) not in pinfo_m["locked_pos"]:
                            tl_w[u_hp_m + 1] = "G"
                        for (u_p, v_p), bp_m in zip(pinfo_m["pairs"], p_bits_m):
                            tl_w[u_p], tl_w[v_p] = bp_m[0], bp_m[1]
                        for u_i, ch_u in zip(non_hp_m, u_vals_m):
                            tl_w[u_i] = ch_u
                        s_w = "".join(tl_w)
                        if S.exact_fold(s_w, eng)[0] == sub_t:
                            if n_w_bits == 1 and s_w not in cands_1w:
                                cands_1w.append(s_w)
                            elif n_w_bits == 2 and s_w not in cands_2w:
                                cands_2w.append(s_w)

            if len(cands_1w) < 6:
                base_0_Pool = []
                for sc0 in cands_0:
                    if sum(1 for u_p, v_p in pinfo_m["pairs"] if (sc0[u_p] + sc0[v_p]) not in ("GC", "CG")) == 0:
                        if S.exact_fold(sc0, eng)[0] == sub_t and sc0 not in base_0_Pool:
                            base_0_Pool.append(sc0)
                if not base_0_Pool:
                    for s_fb in ("".join(tl_san), "".join(tl_strip), "".join(tl_san_orig), s0_m):
                        if s_fb not in base_0_Pool:
                            base_0_Pool.append(s_fb)
                for s_b0 in base_0_Pool[:3]:
                    if len(cands_1w) >= 12 or time.time() >= deadline:
                        break
                    for u_p, v_p in reversed(pinfo_m["pairs"]):
                        if len(cands_1w) >= 12 or time.time() >= deadline:
                            break
                        r_op_p = pinfo_m["open_pair_struct"][(u_p, v_p)]
                        near_unp = [
                            u_i
                            for u_i in range(len(sub_t))
                            if pinfo_m["pair_of"][u_i] == -1
                            and u_i not in pinfo_m["locked_pos"]
                            and not (u_i == 0 and a_f < a_m)
                            and not (u_i == len(sub_t) - 1 and b_f > b_m)
                            and (abs(u_i - u_p) <= 2 or abs(u_i - v_p) <= 2)
                        ][:3]
                        for wb_bp in wobble_bps:
                            if wb_bp not in pinfo["allowed_pairs"][(a_f + u_p, a_f + v_p)]:
                                continue
                            for u_vals in itertools.product(("A", "G"), repeat=len(near_unp)):
                                tl_w = list(s_b0)
                                tl_w[u_p], tl_w[v_p] = wb_bp[0], wb_bp[1]
                                for u_i, ch_u in zip(near_unp, u_vals):
                                    tl_w[u_i] = ch_u
                                s_w = "".join(tl_w)
                                et_w = float(RNA.energy_of_struct(s_w, sub_t))
                                if et_w - float(RNA.energy_of_struct(s_w, r_op_p)) <= 0.0:
                                    if S.exact_fold(s_w, eng)[0] == sub_t and s_w not in cands_1w:
                                        cands_1w.append(s_w)
                                        if len(cands_1w) >= 12:
                                            break

        if every_sub_needs_wobble and len(cands_1w) >= 8:
            sub_pools.append(cands_1w[:140])
            continue
        if (min_non_gc > len(subtrees)) and (len(cands_1w) + len(cands_2w) >= 8):
            c0_solved = [sc0 for sc0 in cands_0 if S.exact_fold(sc0, eng)[0] == sub_t][:8]
            inter_12 = []
            for i_w in range(max(len(cands_2w), len(cands_1w), len(c0_solved))):
                if i_w < len(cands_2w) and cands_2w[i_w] not in inter_12:
                    inter_12.append(cands_2w[i_w])
                if i_w < len(cands_1w) and cands_1w[i_w] not in inter_12:
                    inter_12.append(cands_1w[i_w])
                if i_w < len(c0_solved) and c0_solved[i_w] not in inter_12:
                    inter_12.append(c0_solved[i_w])
            sub_pools.append(inter_12[:48])
            continue

        # Expand over 4-state alternating-helix dictionary (`Law R23a`) and prioritize locally solved variants
        # `Law R26a`: Inject top cross-puzzle donor sequences from `_GLOBAL_SUBTREE_DB` for `target[a_m : b_m + 1]`
        sub_db_m, _ = get_global_subtree_db()
        core_t_m = target[a_m : b_m + 1]
        pid_cur = str(pinfo["puzzle_id"])
        donor_seeds_m = []
        for _d_dbp, _d_de, pid_d, core_s_d in sub_db_m.get(core_t_m, [])[:6]:
            if pid_d == pid_cur:
                continue
            tl_dm = list(s0_m)
            tl_dm[a_m - a_f : b_m - a_f + 1] = list(core_s_d)
            for idx_loc in range(len(tl_dm)):
                if (a_f + idx_loc) in locked_pos:
                    tl_dm[idx_loc] = s0_m[idx_loc]
                    q_loc = pinfo_m["pair_of"][idx_loc]
                    if q_loc != -1 and ( idx_loc + a_f not in locked_pos or q_loc + a_f not in locked_pos ):
                        bp_loc = (tl_dm[idx_loc] + tl_dm[q_loc]) if idx_loc < q_loc else (tl_dm[q_loc] + tl_dm[idx_loc])
                        if bp_loc not in S.VALID_SET:
                            tl_dm[q_loc] = {"G": "C", "C": "G", "A": "U", "U": "A"}.get(tl_dm[idx_loc], "A")
            s_dm = "".join(tl_dm)
            if s_dm not in donor_seeds_m:
                donor_seeds_m.append(s_dm)

        raw_m = []
        for cm in donor_seeds_m[:4] + cands_2w[:4] + cands_1w[:6] + cands_0[:6]:
            for v4 in generate_subtree_4state_variants(cm, sub_t, sub_l)[:24]:
                if v4 not in raw_m:
                    raw_m.append(v4)
                # `Law R26b`: Also test 3'-G flanking dangle (`b_f > b_m`) when `b_f` is unlocked
                if b_f > b_m and b_f not in locked_pos and v4[-1] != "G":
                    v4_g = v4[:-1] + "G"
                    if v4_g not in raw_m:
                        raw_m.append(v4_g)
        solved_0w = []
        solved_1w = []
        solved_2w = []
        unsolved_m = []
        for v4 in raw_m:
            if time.time() >= deadline or (len(solved_0w) >= 16 and len(solved_1w) >= 16):
                break
            n_wob = sum(1 for u_p, v_p in pinfo_m["pairs"] if (v4[u_p] + v4[v_p]) not in ("GC", "CG"))
            if S.exact_fold(v4, eng)[0] == sub_t:
                if n_wob == 0 and len(solved_0w) < 16:
                    solved_0w.append(v4)
                elif n_wob == 1 and len(solved_1w) < 16:
                    solved_1w.append(v4)
                elif n_wob >= 2 and len(solved_2w) < 10:
                    solved_2w.append(v4)
            elif len(unsolved_m) < 4:
                unsolved_m.append(v4)
        pool_m = []
        if every_sub_needs_wobble and solved_1w:
            pool_m.extend(solved_1w)
        else:
            for i_w in range(max(len(solved_2w), len(solved_1w), len(solved_0w))):
                if i_w < len(solved_2w):
                    pool_m.append(solved_2w[i_w])
                if i_w < len(solved_1w):
                    pool_m.append(solved_1w[i_w])
                if i_w < len(solved_0w):
                    pool_m.append(solved_0w[i_w])
            for u_v in unsolved_m:
                if len(pool_m) < 12 and u_v not in pool_m:
                    pool_m.append(u_v)
        sub_pools.append(pool_m[:32] if pool_m else [s0_m])

    # `Law R25a` (Isomorphic Sibling-Subtree Pool Cloning with 4-State Anti-Duplex Rotation):
    for i_s in range(len(subtrees)):
        am_i, bm_i = subtrees[i_s]
        af_i, bf_i = flanked_spans[i_s]
        core_t_i = target[am_i : bm_i + 1]
        sub_t_i = target[af_i : bf_i + 1]
        solved_in_i = [s_i for s_i in sub_pools[i_s][:8] if S.exact_fold(s_i, eng)[0] == sub_t_i]
        if not solved_in_i:
            continue
        for j_s in range(len(subtrees)):
            if i_s == j_s or time.time() >= deadline:
                continue
            am_j, bm_j = subtrees[j_s]
            if target[am_j : bm_j + 1] != core_t_i:
                continue
            af_j, bf_j = flanked_spans[j_s]
            sub_t_j = target[af_j : bf_j + 1]
            sub_l_j = pinfo["locks"][af_j : bf_j + 1]
            cloned_j = []
            for s_i in solved_in_i[:4]:
                core_seq_i = s_i[am_i - af_i : bm_i - af_i + 1]
                tl_j = list(base_full_seq[af_j : bf_j + 1])
                tl_j[am_j - af_j : bm_j - af_j + 1] = list(core_seq_i)
                # Enforce any locked positions on `j_s`
                for idx_loc in range(len(tl_j)):
                    if (af_j + idx_loc) in locked_pos:
                        tl_j[idx_loc] = base_full_seq[af_j + idx_loc]
                s_graft_j = "".join(tl_j)
                for v4_j in generate_subtree_4state_variants(s_graft_j, sub_t_j, sub_l_j)[:12]:
                    if S.exact_fold(v4_j, eng)[0] == sub_t_j and v4_j not in cloned_j:
                        cloned_j.append(v4_j)
                    if bf_j > bm_j and bf_j not in locked_pos and v4_j[-1] != "G":
                        v4_jg = v4_j[:-1] + "G"
                        if S.exact_fold(v4_jg, eng)[0] == sub_t_j and v4_jg not in cloned_j:
                            cloned_j.append(v4_jg)
            if cloned_j:
                merged_j = list(cloned_j)
                for s_old_j in sub_pools[j_s]:
                    if s_old_j not in merged_j:
                        merged_j.append(s_old_j)
                sub_pools[j_s] = merged_j[:36]

    def count_bp_types(s_slice: str, coords: list) -> tuple:
        gc_c = 0
        gu_c = 0
        au_c = 0
        for u_c, v_c in coords:
            bp_c = s_slice[u_c] + s_slice[v_c]
            if bp_c in ("GC", "CG"):
                gc_c += 1
            elif bp_c in ("GU", "UG"):
                gu_c += 1
            elif bp_c in ("AU", "UA"):
                au_c += 1
        return (gc_c, gu_c, au_c)

    ext_gc = 0
    ext_gu = 0
    ext_au = 0
    for u_e, v_e in peeled_trunk_pairs:
        bp_e = base_full_seq[u_e] + base_full_seq[v_e]
        if bp_e in ("GC", "CG"):
            ext_gc += 1
        elif bp_e in ("GU", "UG"):
            ext_gu += 1
        elif bp_e in ("AU", "UA"):
            ext_au += 1

    # `Law R23b + Law R24a + Law R26b` (Dangle-Coupled Adjacent Subtree Pair Screening with Non-Overwriting Shared Flanks):
    block_indices = []
    block_pools = []
    m_idx = 0
    while m_idx < len(subtrees):
        gap_next = (subtrees[m_idx + 1][0] - subtrees[m_idx][1]) if (m_idx + 1 < len(subtrees)) else 999
        couple_pair = (gap_next == 1) or (len(subtrees) <= 3 and gap_next <= 2)
        if couple_pair and time.time() + 0.25 < deadline:
            af_0, bf_0 = flanked_spans[m_idx]
            af_1, bf_1 = flanked_spans[m_idx + 1]
            am_0, bm_0 = subtrees[m_idx]
            am_1, bm_1 = subtrees[m_idx + 1]
            joint_T = target[af_0 : bf_1 + 1]
            coords_0 = sub_pair_coords[m_idx]
            coords_1 = sub_pair_coords[m_idx + 1]
            counts_0 = [count_bp_types(s_0, coords_0) for s_0 in sub_pools[m_idx]]
            counts_1 = [count_bp_types(s_1, coords_1) for s_1 in sub_pools[m_idx + 1]]
            valid_joint = []
            for s_0, (gc0, gu0, au0) in zip(sub_pools[m_idx], counts_0):
                for s_1, (gc1, gu1, au1) in zip(sub_pools[m_idx + 1], counts_1):
                    tl_j = list(base_full_seq[af_0 : bf_1 + 1])
                    tl_j[am_0 - af_0 : bm_0 - af_0 + 1] = list(s_0[am_0 - af_0 : bm_0 - af_0 + 1])
                    tl_j[am_1 - af_0 : bm_1 - af_0 + 1] = list(s_1[am_1 - af_1 : bm_1 - af_1 + 1])
                    if af_0 < am_0 and af_0 not in locked_pos and s_0[0] != "A":
                        tl_j[0] = s_0[0]
                    if bf_0 > bm_0 and bf_0 not in locked_pos and s_0[-1] != "A":
                        tl_j[bf_0 - af_0] = s_0[-1]
                    if af_1 < am_1 and af_1 not in locked_pos and s_1[0] != "A":
                        tl_j[af_1 - af_0] = s_1[0]
                    if bf_1 > bm_1 and bf_1 not in locked_pos and s_1[-1] != "A":
                        tl_j[bf_1 - af_0] = s_1[-1]
                    s_j = "".join(tl_j)
                    if S.exact_fold(s_j, eng)[0] == joint_T:
                        et_j = round(float(RNA.energy_of_struct(s_j, joint_T)), 4)
                        valid_joint.append((et_j, (gc0 + gc1, gu0 + gu1, au0 + au1), (s_0, s_1)))
            valid_joint.sort(key=lambda x: x[0])
            if not valid_joint:
                for s_0, (gc0, gu0, au0) in zip(sub_pools[m_idx][:6], counts_0[:6]):
                    for s_1, (gc1, gu1, au1) in zip(sub_pools[m_idx + 1][:6], counts_1[:6]):
                        tl_j = list(base_full_seq[af_0 : bf_1 + 1])
                        tl_j[am_0 - af_0 : bm_0 - af_0 + 1] = list(s_0[am_0 - af_0 : bm_0 - af_0 + 1])
                        tl_j[am_1 - af_0 : bm_1 - af_0 + 1] = list(s_1[am_1 - af_1 : bm_1 - af_1 + 1])
                        if af_0 < am_0 and af_0 not in locked_pos and s_0[0] != "A":
                            tl_j[0] = s_0[0]
                        if bf_0 > bm_0 and bf_0 not in locked_pos and s_0[-1] != "A":
                            tl_j[bf_0 - af_0] = s_0[-1]
                        if af_1 < am_1 and af_1 not in locked_pos and s_1[0] != "A":
                            tl_j[af_1 - af_0] = s_1[0]
                        if bf_1 > bm_1 and bf_1 not in locked_pos and s_1[-1] != "A":
                            tl_j[bf_1 - af_0] = s_1[-1]
                        s_j = "".join(tl_j)
                        et_j = round(float(RNA.energy_of_struct(s_j, joint_T)), 4)
                        valid_joint.append((et_j, (gc0 + gc1, gu0 + gu1, au0 + au1), (s_0, s_1)))
                valid_joint.sort(key=lambda x: x[0])
            strat_joint = []
            gc_b_cnt = {}
            for item_j in valid_joint:
                gc_j = item_j[1][0]
                gc_b_cnt[gc_j] = gc_b_cnt.get(gc_j, 0) + 1
                if gc_b_cnt[gc_j] <= 20:
                    strat_joint.append(item_j)
            block_indices.append((m_idx, m_idx + 1))
            block_pools.append(strat_joint[:72])
            m_idx += 2
        else:
            af_0, bf_0 = flanked_spans[m_idx]
            sub_T0 = target[af_0 : bf_0 + 1]
            coords_0 = sub_pair_coords[m_idx]
            single_scored = [
                (round(float(RNA.energy_of_struct(s_0, sub_T0)), 4), count_bp_types(s_0, coords_0), (s_0,))
                for s_0 in sub_pools[m_idx]
            ]
            single_scored.sort(key=lambda x: x[0])
            strat_single = []
            gc_s_cnt = {}
            for item_s in single_scored:
                gc_s = item_s[1][0]
                gc_s_cnt[gc_s] = gc_s_cnt.get(gc_s, 0) + 1
                if gc_s_cnt[gc_s] <= 12:
                    strat_single.append(item_s)
            block_indices.append((m_idx,))
            block_pools.append(strat_single[:36] if strat_single else single_scored[:24])
            m_idx += 1

    n_blocks = len(block_pools)
    if n_blocks == 0 or any(len(bp_b) == 0 for bp_b in block_pools):
        return False, cur_seq, cur_vb, cur_dbp, cur_de, ms

    suffix_min_gc = [0] * (n_blocks + 1)
    suffix_max_gu = [0] * (n_blocks + 1)
    suffix_max_au = [0] * (n_blocks + 1)
    for b_i in range(n_blocks - 1, -1, -1):
        suffix_min_gc[b_i] = suffix_min_gc[b_i + 1] + min(x[1][0] for x in block_pools[b_i])
        suffix_max_gu[b_i] = suffix_max_gu[b_i + 1] + max(x[1][1] for x in block_pools[b_i])
        suffix_max_au[b_i] = suffix_max_au[b_i + 1] + max(x[1][2] for x in block_pools[b_i])

    trunk_modes = (
        (
            "orig",
            "strip_gc",
            "reflect",
            "alt_0",
            "alt_1",
            "ur_GC",
            "ur_CG",
            "ur_AU",
            "ur_UA",
            "ur_GU",
            "ur_UG",
            "ur2_GC_GC",
            "ur2_GC_CG",
            "ur2_CG_GC",
            "ur2_CG_CG",
            "ur2_CG_AU",
            "ur2_GC_AU",
            "ur2_CG_UA",
            "ur2_GC_UA",
        )
        if peeled_trunk_pairs
        else ("orig",)
    )
    cp_pool = []
    prod_steps = [0]
    seen_trunks = set()
    for t_mode in trunk_modes:
        if len(cp_pool) >= 75000 or prod_steps[0] >= 120000 or time.time() >= deadline:
            break
        tl_trunk = list(base_full_seq)
        if t_mode == "strip_gc":
            for u_t, v_t in peeled_trunk_pairs:
                if u_t not in locked_pos and v_t not in locked_pos:
                    if (tl_trunk[u_t] + tl_trunk[v_t]) not in ("GC", "CG") and "GC" in pinfo["allowed_pairs"][(u_t, v_t)]:
                        tl_trunk[u_t], tl_trunk[v_t] = ("G", "C") if tl_trunk[u_t] in ("G", "A") else ("C", "G")
        elif t_mode.startswith("ur2_"):
            if len(peeled_trunk_pairs) >= 2:
                _, bp_2, bp_1 = t_mode.split("_")
                u_r2, v_r2 = peeled_trunk_pairs[-2]
                u_r1, v_r1 = peeled_trunk_pairs[-1]
                if u_r2 not in locked_pos and v_r2 not in locked_pos and bp_2 in pinfo["allowed_pairs"][(u_r2, v_r2)]:
                    tl_trunk[u_r2], tl_trunk[v_r2] = bp_2[0], bp_2[1]
                if u_r1 not in locked_pos and v_r1 not in locked_pos and bp_1 in pinfo["allowed_pairs"][(u_r1, v_r1)]:
                    tl_trunk[u_r1], tl_trunk[v_r1] = bp_1[0], bp_1[1]
        elif t_mode.startswith("ur_"):
            u_r_t, v_r_t = peeled_trunk_pairs[-1]
            ur_bp = t_mode[3:]
            if u_r_t not in locked_pos and v_r_t not in locked_pos and ur_bp in pinfo["allowed_pairs"][(u_r_t, v_r_t)]:
                tl_trunk[u_r_t], tl_trunk[v_r_t] = ur_bp[0], ur_bp[1]
        elif t_mode != "orig":
            for r_idx, (u_t, v_t) in enumerate(peeled_trunk_pairs):
                if u_t in locked_pos or v_t in locked_pos:
                    continue
                cur_bp_t = tl_trunk[u_t] + tl_trunk[v_t]
                if t_mode == "reflect":
                    t_bp = cur_bp_t[1] + cur_bp_t[0]
                elif t_mode == "alt_0":
                    t_bp = ("GC" if r_idx % 2 == 0 else "CG") if cur_bp_t in ("GC", "CG") else cur_bp_t
                else:
                    t_bp = ("CG" if r_idx % 2 == 0 else "GC") if cur_bp_t in ("GC", "CG") else cur_bp_t
                if t_bp in pinfo["allowed_pairs"][(u_t, v_t)]:
                    tl_trunk[u_t], tl_trunk[v_t] = t_bp[0], t_bp[1]
        trunk_sig = tuple((tl_trunk[u_t], tl_trunk[v_t]) for u_t, v_t in peeled_trunk_pairs)
        if trunk_sig in seen_trunks:
            continue
        seen_trunks.add(trunk_sig)
        ext_gc_t = sum(1 for u_e, v_e in peeled_trunk_pairs if (tl_trunk[u_e] + tl_trunk[v_e]) in ("GC", "CG"))
        ext_gu_t = sum(1 for u_e, v_e in peeled_trunk_pairs if (tl_trunk[u_e] + tl_trunk[v_e]) in ("GU", "UG"))
        ext_au_t = sum(1 for u_e, v_e in peeled_trunk_pairs if (tl_trunk[u_e] + tl_trunk[v_e]) in ("AU", "UA"))

        chosen_blocks = [None] * n_blocks

        def dfs_blocks(b_i: int, gc_cur: int, gu_cur: int, au_cur: int, et_cur: float) -> None:
            if len(cp_pool) >= 75000 or prod_steps[0] >= 120000:
                return
            prod_steps[0] += 1
            if (prod_steps[0] & 1023) == 0 and time.time() >= deadline:
                prod_steps[0] = 120000
                return
            if b_i == n_blocks:
                v_q = max(0, gc_cur - max_gc) + max(0, req_gu - gu_cur) + max(0, req_au - au_cur)
                if v_q > cur_vb:
                    return
                tl_full = list(tl_trunk)
                for b_idxs, b_seqs in zip(block_indices, chosen_blocks):
                    for sub_i, s_sub in zip(b_idxs, b_seqs):
                        a_f, b_f = flanked_spans[sub_i]
                        a_m, b_m = subtrees[sub_i]
                        tl_full[a_m : b_m + 1] = list(s_sub[a_m - a_f : b_m - a_f + 1])
                        if a_f < a_m and a_f not in locked_pos and s_sub[0] != "A":
                            tl_full[a_f] = s_sub[0]
                        if b_f > b_m and b_f not in locked_pos and s_sub[-1] != "A":
                            tl_full[b_f] = s_sub[-1]
                s_try = "".join(tl_full)
                if s_try != cur_seq:
                    cp_pool.append([0.0, round(et_cur, 4), s_try, None])
                return

            if gc_cur + suffix_min_gc[b_i] > max_gc + cur_vb:
                return
            if gu_cur + suffix_max_gu[b_i] < req_gu - cur_vb:
                return
            if au_cur + suffix_max_au[b_i] < req_au - cur_vb:
                return

            for et_b, (gc_b, gu_b, au_b), b_seqs in block_pools[b_i]:
                if len(cp_pool) >= 75000 or prod_steps[0] >= 120000:
                    break
                chosen_blocks[b_i] = b_seqs
                dfs_blocks(b_i + 1, gc_cur + gc_b, gu_cur + gu_b, au_cur + au_b, et_cur + et_b)

        dfs_blocks(0, ext_gc_t, ext_gu_t, ext_au_t, 0.0)

    cp_pool.sort(key=lambda x: x[1])
    cp_pool = cp_pool[:25000]

    for _cp_step in range(45):
        if not cp_pool or time.time() >= deadline:
            break
        best_i = min(range(len(cp_pool)), key=lambda i: (cp_pool[i][0], cp_pool[i][1]))
        w_try, _et_approx, s_try, et_exact = cp_pool[best_i]
        if w_try > 500.0:
            break
        cp_pool[best_i][0] = 999.0
        vb_try = S.budget_violation(s_try, pinfo)
        if vb_try > cur_vb:
            continue
        fms_try, fme_try = S.exact_fold(s_try, eng)
        mbps_try = S.get_bp_set(fms_try)
        dbp_try = len(t_bps ^ mbps_try)
        if et_exact is None:
            et_exact = float(RNA.energy_of_struct(s_try, target))
            cp_pool[best_i][3] = et_exact
        de_try = round(et_exact - fme_try, 4)
        is_tie = (vb_try == 0 and de_try == 0.0 and cur_de > 0.0 and dbp_try <= cur_dbp + 1)
        if (vb_try, dbp_try, de_try) < (cur_vb, cur_dbp, cur_de) or is_tie:
            oms, ome = S.exact_official_fold(s_try, eng)
            odbp = len(t_bps ^ S.get_bp_set(oms))
            ode = round(float(RNA.energy_of_struct(s_try, target)) - ome, 4)
            ovb = S.budget_violation(s_try, pinfo)
            if (ovb, odbp, ode) < (cur_vb, cur_dbp, cur_de) or (ovb == 0 and ode == 0.0 and cur_de > 0.0 and odbp <= cur_dbp + 1):
                cur_seq, cur_vb, cur_dbp, cur_de, ms = s_try, ovb, odbp, ode, oms
                improved = True
                if cur_dbp == 0 and cur_vb == 0:
                    return True, cur_seq, 0, 0, 0.0, ms
        extra_try = sorted(mbps_try - t_bps)
        for item in cp_pool:
            if item[0] < 900.0:
                seq_i = item[2]
                if not extra_try or all((seq_i[x] + seq_i[y]) in S.VALID_SET for x, y in extra_try):
                    et_i = item[3]
                    if et_i is None:
                        et_i = float(RNA.energy_of_struct(seq_i, target))
                        item[3] = et_i
                    d_i = round(et_i - float(RNA.energy_of_struct(seq_i, fms_try)), 4)
                    if d_i > item[0]:
                        item[0] = d_i

    return improved, cur_seq, cur_vb, cur_dbp, cur_de, ms


def solve_puzzle_depth2(task: tuple) -> dict:
    g, row, init_res, max_passes, max_sec = task
    t0 = time.time()
    deadline = t0 + max_sec
    pinfo = S.parse_puzzle_constraints(row)
    eng = S.configure_engine(pinfo["folder"])
    pid = str(pinfo["puzzle_id"])
    target = pinfo["target"]
    t_bps = S.get_bp_set(target)

    cur_seq = init_res["sequence"]
    ms, me = S.exact_official_fold(cur_seq, eng)
    cur_vb = S.budget_violation(cur_seq, pinfo)
    cur_dbp = len(t_bps ^ S.get_bp_set(ms))
    cur_de = round(float(RNA.energy_of_struct(cur_seq, target)) - me, 4)

    init_tuple = (cur_vb, cur_dbp, cur_de)
    rng = random.Random(20261110 ^ int(pid))

    # 0.0. `Law R26a`: Warm-Start Cross-Puzzle Twin Transfer & Multi-Subtree Composite Graft Pass
    if cur_dbp > 0 and time.time() < deadline:
        _imp_gr, cur_seq, cur_vb, cur_dbp, cur_de, ms = run_cross_puzzle_graft_pass(
            cur_seq, ms, cur_vb, cur_dbp, cur_de, row, pinfo, eng, rng, deadline
        )

    # 0a. `Law R16 + Law R19b + Law R21d + Law R22b + Law R26a/b`: Flanked Independent Subtree Decomposition & Wobble-Budget Partition
    if cur_dbp > 0 and time.time() < deadline:
        _imp_sub, cur_seq, cur_vb, cur_dbp, cur_de, ms = run_independent_subtrees_pass(
            cur_seq, ms, cur_vb, cur_dbp, cur_de, row, pinfo, eng, rng, deadline
        )

    # 0b. `Law R21b + Law R22a`: Serial Loop-Chain Pure-Purine Trio, Multi-nt Bulge Corner & Opposite-Chirality 1-nt Bulge Pass
    if cur_dbp > 0 and time.time() < deadline:
        _imp_ch, cur_seq, cur_vb, cur_dbp, cur_de, ms = solve_serial_loop_chain_purine_pass(
            cur_seq, ms, cur_vb, cur_dbp, cur_de, pinfo, eng, rng, deadline
        )

    # 0c. `Law R22c`: Multiloop Collective Ring & Bulge-Step Cutting-Plane Pass
    if 0 < cur_dbp <= 2 and time.time() < deadline:
        _imp_ml, cur_seq, cur_vb, cur_dbp, cur_de, ms = solve_multiloop_collective_ring_pass(
            cur_seq, ms, cur_vb, cur_dbp, cur_de, pinfo, eng, rng, deadline
        )

    for _pass_idx in range(max_passes):
        if time.time() >= deadline or (cur_dbp == 0 and cur_vb == 0):
            break
        windows = build_depth2_windows(cur_seq, ms, pinfo, eng, deadline)
        if not windows:
            break
        pass_imp = False
        for win_spec in windows:
            if time.time() >= deadline:
                break
            imp, n_seq, n_vb, n_dbp, n_de, n_ms = run_depth2_cutting_plane_on_window(
                cur_seq, ms, pinfo, eng, win_spec, rng, deadline=deadline, max_cp_steps=18
            )
            if imp:
                cur_seq, cur_vb, cur_dbp, cur_de, ms = n_seq, n_vb, n_dbp, n_de, n_ms
                pass_imp = True
                if cur_dbp == 0 and cur_vb == 0:
                    break
        # `Law R20b` (Window 3b Unpropped-Mismatch Seed): When `extra` is non-empty and `cur_dbp <= 3`,
        # test `build_depth2_windows` directly on the lowest-`(d_bp, de_mfe)` unpropped seed `s_u` with `(pu, pv)` forbidden.
        if (cur_dbp > 0 or cur_vb > 0) and cur_dbp <= 3 and time.time() + 0.4 < deadline:
            unp_seeds = find_unpropped_mismatch_seeds(cur_seq, ms, pinfo, eng, deadline)
            for s_u, ms_u, uv_forb in unp_seeds:
                if time.time() >= deadline or (cur_dbp == 0 and cur_vb == 0):
                    break
                u_windows = build_depth2_windows(s_u, ms_u, pinfo, eng, deadline, extra_forbid=[uv_forb])[:4]
                for u_win in u_windows:
                    if time.time() >= deadline:
                        break
                    imp_u, n_seq_u, n_vb_u, n_dbp_u, n_de_u, n_ms_u = run_depth2_cutting_plane_on_window(
                        s_u, ms_u, pinfo, eng, u_win, rng, deadline=deadline, max_cp_steps=14
                    )
                    if imp_u:
                        is_tie_u = (n_vb_u == 0 and n_de_u == 0.0 and cur_de > 0.0 and n_dbp_u <= cur_dbp + 1)
                        if (n_vb_u, n_dbp_u, n_de_u) < (cur_vb, cur_dbp, cur_de) or is_tie_u:
                            cur_seq, cur_vb, cur_dbp, cur_de, ms = n_seq_u, n_vb_u, n_dbp_u, n_de_u, n_ms_u
                            pass_imp = True
                            if cur_dbp == 0 and cur_vb == 0:
                                break
        if not pass_imp:
            break

    # Final subtree reflection & multiloop ring pass if subtrees were updated during window passes
    if cur_dbp > 0 and time.time() + 0.3 < deadline:
        _imp_sub2, cur_seq, cur_vb, cur_dbp, cur_de, ms = run_independent_subtrees_pass(
            cur_seq, ms, cur_vb, cur_dbp, cur_de, row, pinfo, eng, rng, deadline
        )
    if 0 < cur_dbp <= 2 and time.time() + 0.3 < deadline:
        _imp_ml2, cur_seq, cur_vb, cur_dbp, cur_de, ms = solve_multiloop_collective_ring_pass(
            cur_seq, ms, cur_vb, cur_dbp, cur_de, pinfo, eng, rng, deadline
        )

    elapsed = round(time.time() - t0, 3)
    return {
        "group": g,
        "puzzle_id": pid,
        "title": pinfo["title"],
        "folder": pinfo["folder"],
        "solved": (cur_dbp == 0 and cur_vb == 0),
        "d_bp": cur_dbp,
        "v_budget": cur_vb,
        "de_mfe": cur_de,
        "init_d_bp": init_tuple[1],
        "init_de_mfe": init_tuple[2],
        "improved": (cur_vb, cur_dbp, cur_de) < init_tuple or (cur_vb == 0 and cur_de == 0.0 and init_tuple[2] > 0.0),
        "elapsed_sec": elapsed,
        "sequence": cur_seq,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--groups", type=str, default="1,2,3")
    ap.add_argument("--pids", type=str, default="")
    ap.add_argument("--min-dbp", type=int, default=1)
    ap.add_argument("--max-dbp", type=int, default=2)
    ap.add_argument("--max-passes", type=int, default=3)
    ap.add_argument("--max-sec", type=float, default=18.0)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    workers = min(4, max(1, args.workers))
    groups = [int(x.strip()) for x in args.groups.split(",") if x.strip()]
    pid_filter = {x.strip() for x in args.pids.split(",") if x.strip()}

    tasks = []
    group_rows = {}
    group_ckpts = {}
    for g in groups:
        csv_path = os.path.join(BASE_DIR, f"eterna-hard/groups/eterna-hard-group{g}.csv")
        ckpt_path = os.path.join(BASE_DIR, f"ckpt_group{g}.json")
        rows = {str(r["puzzle_id"]): r for r in csv.DictReader(open(csv_path, "r", encoding="utf-8"))}
        ck = json.load(open(ckpt_path, "r", encoding="utf-8"))
        group_rows[g] = rows
        group_ckpts[g] = ck
        for pid, res in sorted(ck.items(), key=lambda x: (x[1]["d_bp"], x[1]["de_mfe"], int(x[0]))):
            if pid_filter and pid not in pid_filter:
                continue
            if args.min_dbp <= res["d_bp"] <= args.max_dbp and res["v_budget"] == 0:
                tasks.append((g, rows[pid], res, args.max_passes, args.max_sec))

    print(
        f"[LAW-R11/R12 DEPTH-2 CUTTING-PLANE] Launching on {len(tasks)} puzzles ({args.min_dbp} <= d_bp <= {args.max_dbp}) across Groups {groups} with {workers} workers...",
        flush=True,
    )
    t_start = time.time()
    n_done = 0
    n_improved = 0
    n_new_solves = 0
    n_new_ties = 0

    with cf.ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(solve_puzzle_depth2, t) for t in tasks]
        for fut in cf.as_completed(futs):
            res = fut.result()
            n_done += 1
            g = res["group"]
            pid = res["puzzle_id"]
            if res["improved"] or res["solved"]:
                old = group_ckpts[g][pid]
                if (res["v_budget"], res["d_bp"], res["de_mfe"]) < (old["v_budget"], old["d_bp"], old["de_mfe"]) or (
                    res["v_budget"] == 0 and res["de_mfe"] == 0.0 and old["de_mfe"] > 0.0
                ):
                    n_improved += 1
                    if res["solved"] and not old.get("solved", False):
                        n_new_solves += 1
                    if res["de_mfe"] == 0.0 and old["de_mfe"] > 0.0 and not res["solved"]:
                        n_new_ties += 1
                    print(
                        f"  [{n_done}/{len(tasks)}] [G{g} #{pid} {res['title'][:26]}] IMPROVED: d_bp {old['d_bp']}->{res['d_bp']} | de {old['de_mfe']:.2f}->{res['de_mfe']:.2f} kcal/mol ({res['elapsed_sec']:.1f}s)"
                        + (" 🎯 FULL SOLVE!" if res["solved"] else (" ⚖️ EXACT TIE!" if res["de_mfe"] == 0.0 else "")),
                        flush=True,
                    )
                    # `Law R20c` (Dual `exact_tie_seq` Preservation): never overwrite an exact ground-state tie without saving `exact_tie_seq`
                    if old.get("de_mfe") == 0.0 and old.get("v_budget") == 0 and res["de_mfe"] > 0.0 and not res["solved"]:
                        group_ckpts[g][pid]["exact_tie_seq"] = old["sequence"]
                        group_ckpts[g][pid]["exact_tie_d_bp"] = old["d_bp"]
                    elif res["de_mfe"] == 0.0 and res["v_budget"] == 0 and not res["solved"]:
                        group_ckpts[g][pid]["exact_tie_seq"] = res["sequence"]
                        group_ckpts[g][pid]["exact_tie_d_bp"] = res["d_bp"]
                    group_ckpts[g][pid]["solved"] = res["solved"]
                    group_ckpts[g][pid]["d_bp"] = res["d_bp"]
                    group_ckpts[g][pid]["v_budget"] = res["v_budget"]
                    group_ckpts[g][pid]["de_mfe"] = res["de_mfe"]
                    group_ckpts[g][pid]["sequence"] = res["sequence"]
            elif n_done % 10 == 0 or n_done == len(tasks):
                print(
                    f"  [{n_done}/{len(tasks)}] Progress ({time.time() - t_start:.1f}s elapsed, improved={n_improved}, new_solves={n_new_solves}, new_ties={n_new_ties})",
                    flush=True,
                )

    for g in groups:
        ckpt_path = os.path.join(BASE_DIR, f"ckpt_group{g}.json")
        tsv_path = os.path.join(BASE_DIR, f"designs_group{g}.tsv")
        csv_path = os.path.join(BASE_DIR, f"eterna-hard/groups/eterna-hard-group{g}.csv")
        json.dump(group_ckpts[g], open(ckpt_path, "w", encoding="utf-8"), indent=2)
        with open(tsv_path, "w", encoding="utf-8") as f:
            f.write("puzzle_id\tsequence\n")
            for pid in sorted(group_ckpts[g].keys(), key=lambda x: int(x)):
                f.write(f"{pid}\t{group_ckpts[g][pid]['sequence']}\n")
        cmd = [PYTHON_BIN, CHECK_DESIGN, csv_path, tsv_path]
        env = dict(os.environ)
        env["RNAFOLD_V1"] = os.path.join(BASE_DIR, "ViennaRNA-1.8.5/Progs/RNAfold")
        env["RNAFOLD_V2"] = os.path.join(BASE_DIR, "bin/RNAfold_v2")
        out = subprocess.check_output(cmd, text=True, env=env)
        passed = [line for line in out.splitlines() if "\tPASS\t" in line or line.endswith("\tPASS")]
        print(f"[Group {g}] check_design.py PASS count: {len(passed)}", flush=True)

    print(
        f"[DONE in {time.time() - t_start:.1f}s] Improved: {n_improved} | New Full Solves: {n_new_solves} | New Exact Ties: {n_new_ties}",
        flush=True,
    )


if __name__ == "__main__":
    main()

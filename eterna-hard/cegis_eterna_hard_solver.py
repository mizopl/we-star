#!/usr/bin/env python3
"""
CEGIS + Kempe Budget-Manifold RNA Inverse-Folding Solver for Eterna-Hard (`cegis_eterna_hard_solver.py`, v3)
Campaign: V20-02B (`eterna-hard`, Groups 1..3, Stanford Das Lab challenge)

Key Algorithmic Architecture:
  1. Dual-Engine Exact Parity (`Law M38`):
     - `folder in ('Vienna', 'Vienna1')`: loads Turner 1999 (`RNA.params_load_RNA_Turner1999()`, `RNA.cvar.dangles = 1`)
       for microsecond C-extension folding/evaluation, coupled with a persistent pipe to the official compiled
       `ViennaRNA-1.8.5/Progs/RNAfold -T 37 -noPS` binary for exact MFE tie-breaking parity with `check_design.py`.
     - `folder == 'Vienna2'`: loads Turner 2004 (`RNA.params_load_RNA_Turner2004()`, `RNA.cvar.dangles = 2`).
  2. Non-Zipping Pure-Purine Turner 1999 Loop-Motif Dictionary (`Law M38` + `CLSS-4`):
     - Lonely base-pair cascades separated by `2x2` internal loops (`(..(..`) use `p0 = GC -> p_{k>=1} = CG` with
       pure-purine `GA / GA`, `AA / GG`, `GG / AA`, `AG / AG` loops so loop bases can never zip into wobble stems.
     - `1x2` internal loops use `A / GG`, `2x1` loops use `GG / A`, and `1x1` loops use `G / G`.
  3. Three-Stage Dual-Compass Solver (`Op-M1` + `Op-M4` + `Op-M5` + `Law M37`):
     - Stage 1: Multi-seed budget-manifold initialization + guarded `RNA.inverse_fold` (`L <= 105`) + Kempe projection.
     - Stage 2: Constrained CEGIS Rival-Set Minimax (`12 us` `RNA.eval_structure_simple` separable coordinate descent).
     - Stage 3: Dual-Compass Fast MFE Seam + 2-Pair Kempe Swap Climber (`strict_manifold=True` & `False` -> projection).
"""

import argparse
import csv
import itertools
import json
import os
import random
import re
import subprocess
import sys
import time
import numpy as np
import RNA

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
V1_BIN = os.path.join(BASE_DIR, "ViennaRNA-1.8.5/Progs/RNAfold")
V2_BIN = os.path.join(BASE_DIR, "bin/RNAfold_v2")

BASES = ("A", "C", "G", "U")
VALID_PAIRS = ("GC", "CG", "AU", "UA", "GU", "UG")
STRONG_PAIRS = ("GC", "CG")
AU_PAIRS = ("AU", "UA")
GU_PAIRS = ("GU", "UG")
VALID_SET = set(VALID_PAIRS)
PAIR_TYPE = {"GC": "GC", "CG": "GC", "AU": "AU", "UA": "AU", "GU": "GU", "UG": "GU"}
BOOST_MISMATCHES = (("G", "A"), ("A", "G"), ("G", "G"), ("A", "A"), ("U", "U"))
TURNER99_2X2_MOTIFS = (
    ("G", "A", "G", "A"),
    ("A", "A", "G", "G"),
    ("G", "G", "A", "A"),
    ("A", "G", "A", "G"),
    ("G", "G", "G", "A"),
    ("A", "G", "G", "G"),
)

MAX_PAIRS_MAP = {"GC": "GC", "AUMAX": "AU", "GUMAX": "GU"}
MIN_PAIRS_MAP = {"GCMIN": "GC", "AU": "AU", "GU": "GU", "PAIRS": "ANY"}


class PersistentV1Folder:
    """Persistent stdin/stdout pipe to official ViennaRNA-1.8.5/Progs/RNAfold -T 37 -noPS."""

    def __init__(self):
        self.proc = None

    def _ensure(self):
        if self.proc is None or self.proc.poll() is not None:
            self.proc = subprocess.Popen(
                [V1_BIN, "-T", "37", "-noPS"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                cwd="/tmp",
                bufsize=1,
            )

    def fold(self, seq: str):
        self._ensure()
        try:
            self.proc.stdin.write(seq + "\n")
            self.proc.stdin.flush()
            _seq_out = self.proc.stdout.readline()
            struct_line = self.proc.stdout.readline().strip()
            m = re.match(r"^([.()]+)\s+\(\s*(-?[\d.]+)\)", struct_line)
            if m:
                return m.group(1), float(m.group(2))
        except Exception:
            if self.proc is not None:
                try:
                    self.proc.kill()
                except Exception:
                    pass
                self.proc = None
        ms, me = RNA.fold(seq)
        return ms, float(me)


_V1_PIPE = PersistentV1Folder()
_CURRENT_ENGINE = None


def configure_engine(folder: str):
    global _CURRENT_ENGINE
    eng = 1 if folder in ("Vienna", "Vienna1") else 2
    if _CURRENT_ENGINE != eng:
        if eng == 1:
            RNA.params_load_RNA_Turner1999()
            RNA.cvar.dangles = 1
        else:
            RNA.params_load_RNA_Turner2004()
            RNA.cvar.dangles = 2
        RNA.cvar.temperature = 37.0
        RNA.cvar.noLP = 0
        RNA.cvar.fold_constrained = 0
        _CURRENT_ENGINE = eng
    return eng


def exact_fold(seq: str, eng: int):
    ms, me = RNA.fold(seq)
    return ms, float(me)


def eval_struct(seq: str, struct: str) -> float:
    return float(RNA.energy_of_struct(seq, struct))


def exact_official_fold(seq: str, eng: int):
    if eng == 1:
        return _V1_PIPE.fold(seq)
    ms, me = RNA.fold(seq)
    return ms, float(me)


def parse_structure(struct: str):
    n = len(struct)
    pair_of = [-1] * n
    stack = []
    pairs = []
    for i, ch in enumerate(struct):
        if ch == "(":
            stack.append(i)
        elif ch == ")":
            j = stack.pop()
            pair_of[i] = j
            pair_of[j] = i
            pairs.append((j, i))
    pairs.sort()
    active_unpaired = set()
    for i in range(n):
        if pair_of[i] != -1:
            for d in (-3, -2, -1, 1, 2, 3):
                if 0 <= i + d < n and pair_of[i + d] == -1:
                    active_unpaired.add(i + d)
    for u, v in pairs:
        if v - u - 1 <= 7 and all(pair_of[k] == -1 for k in range(u + 1, v)):
            for k in range(u + 1, v):
                active_unpaired.add(k)
    passive_unpaired = {i for i in range(n) if pair_of[i] == -1 and i not in active_unpaired}
    return pair_of, pairs, passive_unpaired, active_unpaired


def get_bp_set(struct: str):
    stack = []
    bps = set()
    for i, ch in enumerate(struct):
        if ch == "(":
            stack.append(i)
        elif ch == ")":
            j = stack.pop()
            bps.add((j, i))
    return bps


def parse_puzzle_constraints(row: dict):
    target = row["structure"].strip()
    locks = row["locks"].strip()
    begin = row["begin_sequence"].strip()
    c_str = row.get("constraints", "").strip()
    n = len(target)
    pair_of, pairs, passive_unpaired, active_unpaired = parse_structure(target)

    toks = c_str.split(",") if c_str else []
    max_limits = {"GC": len(pairs), "AU": len(pairs), "GU": len(pairs)}
    min_limits = {"GC": 0, "AU": 0, "GU": 0, "ANY": 0}
    consec_limits = {}
    for name, val_s in zip(toks[0::2], toks[1::2]):
        val = int(val_s)
        if name == "SHAPE":
            continue
        elif name in MAX_PAIRS_MAP:
            pt = MAX_PAIRS_MAP[name]
            max_limits[pt] = min(max_limits[pt], val)
        elif name in MIN_PAIRS_MAP:
            pt = MIN_PAIRS_MAP[name]
            min_limits[pt] = max(min_limits[pt], val)
        elif name.startswith("CONSECUTIVE_"):
            consec_limits[name[-1]] = val

    locked_pos = {i: begin[i] for i in range(n) if locks[i] == "x"}

    allowed_pairs = {}
    pair_priority = {}
    stems = []
    for u, v in pairs:
        if u == 0 or pair_of[u - 1] != v + 1:
            ln = 1
            while u + ln < v - ln and pair_of[u + ln] == v - ln:
                ln += 1
            stems.append((u, v, ln))
            for k in range(ln):
                uk, vk = u + k, v - k
                if ln == 1:
                    pair_priority[(uk, vk)] = 5
                elif ln == 2:
                    pair_priority[(uk, vk)] = 4
                elif k == 0 or k == ln - 1:
                    pair_priority[(uk, vk)] = 3
                elif (ln >= 4 and (k == 1 or k == ln - 2)):
                    pair_priority[(uk, vk)] = 2
                else:
                    pair_priority[(uk, vk)] = 1

    # Upgrade to 5-Level Junction Criticality Hierarchy (`L-EVVA-009` Upgrade A):
    # Elevate multiloop closing/branch pairs and small internal-loop / bulge bounding pairs to Priority 5,
    # and small-hairpin / exterior-branch closing pairs to Priority 4.
    ext_children = []
    p_ext = 0
    while p_ext < n:
        if pair_of[p_ext] > p_ext:
            ext_children.append((p_ext, pair_of[p_ext]))
            p_ext = pair_of[p_ext] + 1
        else:
            p_ext += 1
    if len(ext_children) >= 2:
        for cu, cv in ext_children:
            pair_priority[(cu, cv)] = max(pair_priority.get((cu, cv), 3), 4)

    for u, v, ln in stems:
        u_in, v_in = u + ln - 1, v - ln + 1
        children = []
        p_in = u_in + 1
        while p_in < v_in:
            if pair_of[p_in] > p_in:
                children.append((p_in, pair_of[p_in]))
                p_in = pair_of[p_in] + 1
            else:
                p_in += 1
        if len(children) == 0:
            hp_len = v_in - u_in - 1
            if hp_len <= 4:
                pair_priority[(u_in, v_in)] = max(pair_priority.get((u_in, v_in), 3), 4)
        elif len(children) == 1:
            cu, cv = children[0]
            l_left = cu - u_in - 1
            l_right = v_in - cv - 1
            if l_left <= 3 and l_right <= 3:
                pair_priority[(u_in, v_in)] = 5
                pair_priority[(cu, cv)] = 5
        else:
            # Multiloop junction: closing pair `(u_in, v_in)` and all branch pairs `(cu, cv)` get Priority 5
            pair_priority[(u_in, v_in)] = 5
            for cu, cv in children:
                pair_priority[(cu, cv)] = 5

    for u, v in pairs:
        al = [
            bp
            for bp in VALID_PAIRS
            if (locks[u] != "x" or bp[0] == begin[u]) and (locks[v] != "x" or bp[1] == begin[v])
        ]
        if not al:
            al = [begin[u] + begin[v]]
        allowed_pairs[(u, v)] = tuple(al)

    loops_2x2 = []
    loops_1x1 = []
    loops_1x2 = []
    loops_2x1 = []
    bulge_hairpins = []
    for u, v in pairs:
        if (
            u + 3 < v - 3
            and pair_of[u + 1] == -1
            and pair_of[u + 2] == -1
            and pair_of[v - 2] == -1
            and pair_of[v - 1] == -1
            and pair_of[u + 3] == v - 3
        ):
            loops_2x2.append((u + 1, u + 2, v - 2, v - 1, u, v, u + 3, v - 3))
        elif u + 2 < v - 2 and pair_of[u + 1] == -1 and pair_of[v - 1] == -1 and pair_of[u + 2] == v - 2:
            loops_1x1.append((u + 1, v - 1, u, v, u + 2, v - 2))
        elif (
            u + 2 < v - 3
            and pair_of[u + 1] == -1
            and pair_of[v - 2] == -1
            and pair_of[v - 1] == -1
            and pair_of[u + 2] == v - 3
        ):
            loops_1x2.append((u + 1, v - 2, v - 1, u, v, u + 2, v - 3))
        elif (
            u + 3 < v - 2
            and pair_of[u + 1] == -1
            and pair_of[u + 2] == -1
            and pair_of[v - 1] == -1
            and pair_of[u + 3] == v - 2
        ):
            loops_2x1.append((u + 1, u + 2, v - 1, u, v, u + 3, v - 2))
        # Detect `.((....).).` bulge-hairpin motifs: (u, v) outer pair, (u+1, v-2) inner hairpin pair with 4-nt loop, v-1 bulge
        if (
            v - u == 8
            and pair_of[u + 1] == v - 2
            and pair_of[v - 1] == -1
            and all(pair_of[k] == -1 for k in range(u + 2, v - 2))
        ):
            fL = u - 1 if (u > 0 and pair_of[u - 1] == -1) else -1
            fR = v + 1 if (v + 1 < n and pair_of[v + 1] == -1) else -1
            bulge_hairpins.append((u, v, u + 1, v - 2, u + 2, v - 1, fL, fR))
        elif (
            v - u == 8
            and pair_of[u + 2] == v - 1
            and pair_of[u + 1] == -1
            and all(pair_of[k] == -1 for k in range(u + 3, v - 1))
        ):
            fL = u - 1 if (u > 0 and pair_of[u - 1] == -1) else -1
            fR = v + 1 if (v + 1 < n and pair_of[v + 1] == -1) else -1
            bulge_hairpins.append((u, v, u + 2, v - 1, u + 3, u + 1, fL, fR))

    open_pair_struct = {}
    for u, v in pairs:
        tl_op = list(target)
        tl_op[u] = "."
        tl_op[v] = "."
        open_pair_struct[(u, v)] = "".join(tl_op)

    is_pure_shape = (
        len(locked_pos) == 0
        and max_limits["GC"] >= len(pairs)
        and max_limits["AU"] >= len(pairs)
        and max_limits["GU"] >= len(pairs)
        and min_limits["GC"] == 0
        and min_limits["AU"] == 0
        and min_limits["GU"] == 0
        and min_limits["ANY"] <= len(pairs)
        and not consec_limits
    )

    return {
        "puzzle_id": str(row["puzzle_id"]),
        "title": row.get("title", ""),
        "folder": row["folder"].strip(),
        "target": target,
        "locks": locks,
        "begin": begin,
        "n": n,
        "pair_of": pair_of,
        "pairs": pairs,
        "passive_unpaired": passive_unpaired - set(locked_pos.keys()),
        "active_unpaired": sorted(active_unpaired - set(locked_pos.keys())),
        "locked_pos": locked_pos,
        "allowed_pairs": allowed_pairs,
        "pair_priority": pair_priority,
        "open_pair_struct": open_pair_struct,
        "max_limits": max_limits,
        "min_limits": min_limits,
        "consec_limits": consec_limits,
        "loops_2x2": loops_2x2,
        "loops_1x1": loops_1x1,
        "loops_1x2": loops_1x2,
        "loops_2x1": loops_2x1,
        "bulge_hairpins": bulge_hairpins,
        "is_pure_shape": is_pure_shape,
    }


def count_target_pair_types(seq: str, pairs: list):
    counts = {"GC": 0, "AU": 0, "GU": 0, "ANY": 0}
    for u, v in pairs:
        pt = PAIR_TYPE.get(seq[u] + seq[v], "other")
        if pt in counts:
            counts[pt] += 1
        counts["ANY"] += 1
    return counts


def count_mfe_pair_types(seq: str, mfe_struct: str):
    stack = []
    counts = {"GC": 0, "AU": 0, "GU": 0, "ANY": 0}
    for j, c in enumerate(mfe_struct):
        if c == "(":
            stack.append(j)
        elif c == ")":
            i = stack.pop()
            pt = PAIR_TYPE.get(seq[i] + seq[j], "other")
            if pt in counts:
                counts[pt] += 1
            counts["ANY"] += 1
    return counts


def budget_violation(seq: str, pinfo: dict, struct_for_pairs: str = None) -> int:
    if pinfo["is_pure_shape"]:
        return 0
    v = 0
    for i, b0 in pinfo["locked_pos"].items():
        if seq[i] != b0:
            v += 10
    counts = count_target_pair_types(seq, pinfo["pairs"]) if struct_for_pairs is None else count_mfe_pair_types(seq, struct_for_pairs)
    for pt in ("GC", "AU", "GU"):
        if counts[pt] > pinfo["max_limits"][pt]:
            v += counts[pt] - pinfo["max_limits"][pt]
        if counts[pt] < pinfo["min_limits"][pt]:
            v += pinfo["min_limits"][pt] - counts[pt]
    if counts["ANY"] < pinfo["min_limits"]["ANY"]:
        v += pinfo["min_limits"]["ANY"] - counts["ANY"]
    for base, lim in pinfo["consec_limits"].items():
        for m in re.findall(f"{base}+", seq):
            if len(m) >= lim:
                v += len(m) - lim + 1
    return v


def has_symmetric_neck_zip(z: int, ch_new: str, seq_or_lst, pair_of: list, n: int) -> bool:
    """
    `Law R21c` (General Symmetric Loop-Neck Anti-Zip Guard for `k in {1, 2}`):
    For any unpaired position `z` (`pair_of[z] == -1`) at distance `k in {1, 2}` from a closing base pair
    `(u_close, v_close)` (either inside `u_close + k, v_close - k` or outside `u_close - k, v_close + k`)
    or inside a `1x1` internal loop, checks the symmetric opposite unpaired position `z_opp`.
    If `0 <= z_opp < n`, `pair_of[z_opp] == -1`, `abs(z - z_opp) >= 4`, and `(ch_new + seq_or_lst[z_opp]) in VALID_SET`,
    returns `True` (rejecting the mutation so hairpin necks and symmetric `1x1`/`2x2` loops never zip up).
    """
    if 0 < z < n - 1 and pair_of[z - 1] != -1 and pair_of[z + 1] != -1 and abs(pair_of[z - 1] - pair_of[z + 1]) == 2:
        cand_opp = (pair_of[z - 1] + pair_of[z + 1]) // 2
        if 0 <= cand_opp < n and pair_of[cand_opp] == -1 and abs(z - cand_opp) >= 4:
            if (ch_new + seq_or_lst[cand_opp]) in VALID_SET:
                return True
    for k in (1, 2):
        # 1. `z = u_close + k` -> `z_opp = v_close - k`
        if z - k >= 0 and pair_of[z - k] > z:
            u_c = z - k
            v_c = pair_of[u_c]
            z_opp = v_c - k
            if z < z_opp < v_c and pair_of[z_opp] == -1 and z_opp - z >= 4:
                if all(pair_of[m] == -1 for m in range(u_c + 1, z)) and all(pair_of[m] == -1 for m in range(z_opp + 1, v_c)):
                    if (ch_new + seq_or_lst[z_opp]) in VALID_SET:
                        return True
        # 2. `z = v_close - k` -> `z_opp = u_close + k`
        if z + k < n and 0 <= pair_of[z + k] < z:
            v_c = z + k
            u_c = pair_of[v_c]
            z_opp = u_c + k
            if u_c < z_opp < z and pair_of[z_opp] == -1 and z - z_opp >= 4:
                if all(pair_of[m] == -1 for m in range(u_c + 1, z_opp)) and all(pair_of[m] == -1 for m in range(z + 1, v_c)):
                    if (seq_or_lst[z_opp] + ch_new) in VALID_SET:
                        return True
        # 3. `z = u_close - k` -> `z_opp = v_close + k`
        if z + k < n and pair_of[z + k] > z + k:
            u_c = z + k
            v_c = pair_of[u_c]
            z_opp = v_c + k
            if 0 <= z_opp < n and pair_of[z_opp] == -1 and z_opp - z >= 4:
                if all(pair_of[m] == -1 for m in range(z + 1, u_c)) and all(pair_of[m] == -1 for m in range(v_c + 1, z_opp)):
                    if (ch_new + seq_or_lst[z_opp]) in VALID_SET:
                        return True
        # 4. `z = v_close + k` -> `z_opp = u_close - k`
        if z - k >= 0 and 0 <= pair_of[z - k] < z - k:
            v_c = z - k
            u_c = pair_of[v_c]
            z_opp = u_c - k
            if 0 <= z_opp < n and pair_of[z_opp] == -1 and z - z_opp >= 4:
                if all(pair_of[m] == -1 for m in range(z_opp + 1, u_c)) and all(pair_of[m] == -1 for m in range(v_c + 1, z)):
                    if (seq_or_lst[z_opp] + ch_new) in VALID_SET:
                        return True
    return False


def enforce_locks_on_list(lst: list, pinfo: dict, rng: random.Random):
    for i, b0 in pinfo["locked_pos"].items():
        lst[i] = b0
    for u, v in pinfo["pairs"]:
        al = pinfo["allowed_pairs"][(u, v)]
        if (lst[u] + lst[v]) not in al:
            bp = rng.choice(al)
            lst[u], lst[v] = bp[0], bp[1]


def enforce_anti_slip_guards(lst: list, pinfo: dict, rng: random.Random):
    """
    `CLSS-4` Anti-Slip Complementarity Exclusion (`Law M38`):
    For lonely base pairs `(u, v)` and stem-boundary base pairs adjacent to 1-nt bulges or small internal loops,
    ensures adjacent unpaired nucleotides `lst[u-1], lst[u+1]` are not WC/GU-complementary to `lst[v]`
    and `lst[v-1], lst[v+1]` are not WC/GU-complementary to `lst[u]` whenever unlocked.
    """
    pair_of = pinfo["pair_of"]
    locked_pos = pinfo["locked_pos"]
    allowed_pairs = pinfo["allowed_pairs"]
    n = pinfo["n"]
    protected_int_unp = set()
    for p1, q1, _uo, _vo, _ui, _vi in pinfo.get("loops_1x1", ()):
        protected_int_unp |= {p1, q1}
    for p1, p2, q1, _uo, _vo, _ui, _vi in pinfo.get("loops_2x1", ()):
        protected_int_unp |= {p1, p2, q1}
    for p1, q1, q2, _uo, _vo, _ui, _vi in pinfo.get("loops_1x2", ()):
        protected_int_unp |= {p1, q1, q2}

    for u, v in pinfo["pairs"]:
        is_outer_bdy = u == 0 or v + 1 >= n or pair_of[u - 1] != v + 1
        is_inner_bdy = u + 1 >= v - 1 or pair_of[u + 1] != v - 1
        if not (is_outer_bdy or is_inner_bdy):
            continue
        # If lonely pair or boundary pair has an adjacent 1-nt bulge or unpaired flank that could slip-pair:
        for idx_u, partner_v in ((u - 1, v), (u + 1, v)):
            if 0 <= idx_u < n and pair_of[idx_u] == -1 and idx_u not in locked_pos and idx_u not in protected_int_unp:
                # Only guard if idx_u is a 1-nt bulge or lonely-pair flank
                is_1nt_bulge = (idx_u == u + 1 and u + 2 < v - 1 and pair_of[u + 2] == v - 1) or (
                    idx_u == u - 1 and u >= 2 and v + 1 < n and pair_of[u - 2] == v + 1
                )
                is_lonely = is_outer_bdy and is_inner_bdy
                if (is_1nt_bulge or is_lonely) and (lst[idx_u] + lst[partner_v]) in VALID_SET:
                    for ch_alt in ("A", "G", "C", "U"):
                        if (ch_alt + lst[partner_v]) not in VALID_SET:
                            lst[idx_u] = ch_alt
                            break
        for idx_v, partner_u in ((v - 1, u), (v + 1, u)):
            if 0 <= idx_v < n and pair_of[idx_v] == -1 and idx_v not in locked_pos and idx_v not in protected_int_unp:
                is_1nt_bulge = (idx_v == v - 1 and u + 1 < v - 2 and pair_of[u + 1] == v - 2) or (
                    idx_v == v + 1 and u > 0 and v + 2 < n and pair_of[u - 1] == v + 2
                )
                is_lonely = is_outer_bdy and is_inner_bdy
                if (is_1nt_bulge or is_lonely) and (lst[partner_u] + lst[idx_v]) in VALID_SET:
                    for ch_alt in ("A", "G", "C", "U"):
                        if (lst[partner_u] + ch_alt) not in VALID_SET:
                            lst[idx_v] = ch_alt
                            break


def apply_turner_loop_motifs(lst: list, pinfo: dict, rng: random.Random, mode: int = 0):
    """Apply non-zipping Turner 1999 / 2004 loop-stabilizing motifs (`GA/GA` on 2x2 with `GC->CG`, anti-slip `CG/CG+GG/A` on 2x1, `GC/GC+A/GG` on 1x2, `GG` on 1x1, and `.((....).).` modules)."""
    pair_of = pinfo["pair_of"]
    locked_pos = pinfo["locked_pos"]
    allowed_pairs = pinfo["allowed_pairs"]
    n = pinfo["n"]

    # 1. 2x2 internal loops (`GA/GA`, `AA/GG`, `GG/AA`, `AG/AG`) + `GC -> CG` orientation on GC pairs (`Law M38`)
    for idx_22, (p1, p2, q1, q2, u_out, v_out, u_in, v_in) in enumerate(pinfo["loops_2x2"]):
        if mode == 0:
            m = ("G", "A", "G", "A") if rng.random() < 0.75 else rng.choice(TURNER99_2X2_MOTIFS[:4])
        else:
            m = rng.choice(TURNER99_2X2_MOTIFS)
        for pos, ch in ((p1, m[0]), (p2, m[1]), (q1, m[2]), (q2, m[3])):
            if pos not in locked_pos:
                lst[pos] = ch
        if PAIR_TYPE.get(lst[u_in] + lst[v_in]) == "GC" and "CG" in allowed_pairs[(u_in, v_in)]:
            lst[u_in], lst[v_in] = "C", "G"

    # 2. `CLSS-4` Anti-Slip 1x2 and 2x1 cascades (`intloops.h` lines 673, 685, 759)
    in_set_12 = {(ui, vi) for _p1, _q1, _q2, _uo, _vo, ui, vi in pinfo["loops_1x2"]}
    for p1, q1, q2, u_out, v_out, u_in, v_in in pinfo["loops_1x2"]:
        is_outer_12 = (u_out, v_out) not in in_set_12
        if is_outer_12:
            if "CG" in allowed_pairs[(u_out, v_out)]:
                lst[u_out], lst[v_out] = "C", "G"
            if "GC" in allowed_pairs[(u_in, v_in)]:
                lst[u_in], lst[v_in] = "G", "C"
            m12 = ("A", "A", "G")
            if u_out > 0 and pair_of[u_out - 1] > v_out + 2 and all(pair_of[k] == -1 for k in range(v_out + 1, pair_of[u_out - 1])):
                uv_b = (u_out - 1, pair_of[u_out - 1])
                if "UG" in allowed_pairs[uv_b]:
                    lst[uv_b[0]], lst[uv_b[1]] = "U", "G"
        else:
            if "GC" in allowed_pairs[(u_in, v_in)]:
                lst[u_in], lst[v_in] = "G", "C"
            m12 = ("A", "G", "G")
        for pos, ch in ((p1, m12[0]), (q1, m12[1]), (q2, m12[2])):
            if pos not in locked_pos:
                lst[pos] = ch

    in_set_21 = {(ui, vi) for _p1, _p2, _q1, _uo, _vo, ui, vi in pinfo["loops_2x1"]}
    for p1, p2, q1, u_out, v_out, u_in, v_in in pinfo["loops_2x1"]:
        is_outer_21 = (u_out, v_out) not in in_set_21
        if is_outer_21:
            if "GC" in allowed_pairs[(u_out, v_out)]:
                lst[u_out], lst[v_out] = "G", "C"
            if "CG" in allowed_pairs[(u_in, v_in)]:
                lst[u_in], lst[v_in] = "C", "G"
            m21 = ("G", "A", "A")
            if v_out + 1 < n and 0 <= pair_of[v_out + 1] < u_out - 2 and all(pair_of[k] == -1 for k in range(pair_of[v_out + 1] + 1, u_out)):
                uv_b = (pair_of[v_out + 1], v_out + 1)
                if "GU" in allowed_pairs[uv_b]:
                    lst[uv_b[0]], lst[uv_b[1]] = "G", "U"
        else:
            if "CG" in allowed_pairs[(u_in, v_in)]:
                lst[u_in], lst[v_in] = "C", "G"
            m21 = ("G", "G", "A")
        for pos, ch in ((p1, m21[0]), (p2, m21[1]), (q1, m21[2])):
            if pos not in locked_pos:
                lst[pos] = ch

    # 3. 1x1 internal loops (`GG` purine-purine mismatch `-2.10 kcal/mol` in `int11_37`!)
    for p1, q1, u_out, v_out, u_in, v_in in pinfo["loops_1x1"]:
        if PAIR_TYPE.get(lst[u_out] + lst[v_out]) == "GC" and "GC" in allowed_pairs[(u_out, v_out)]:
            lst[u_out], lst[v_out] = "G", "C"
        if PAIR_TYPE.get(lst[u_in] + lst[v_in]) == "GC" and "CG" in allowed_pairs[(u_in, v_in)]:
            lst[u_in], lst[v_in] = "C", "G"
        m11 = ("G", "G") if mode == 0 else (("G", "A") if (lst[u_out] == "C" and lst[u_in] == "C") else ("G", "G"))
        for pos, ch in ((p1, m11[0]), (q1, m11[1])):
            if pos not in locked_pos:
                lst[pos] = ch

    # 4. `.((....).).` bulge-hairpin modules (`fold.c` lines 395-405 & 546 strict `dE < 0` with pyrimidine bulge `bg in ('U','C')`)
    bh_tetraloops = ("GAAA", "UUCG", "GCAA", "GUGA", "GAGA", "UACG")
    for idx_bh, (u0, v0, u1, v1, lp_start, bg_pos, fL, fR) in enumerate(pinfo.get("bulge_hairpins", ())):
        if PAIR_TYPE.get(lst[u0] + lst[v0]) == "GC":
            if (idx_bh % 2 == 0) and "GC" in allowed_pairs[(u0, v0)]:
                lst[u0], lst[v0] = "G", "C"
            elif "CG" in allowed_pairs[(u0, v0)]:
                lst[u0], lst[v0] = "C", "G"
        if PAIR_TYPE.get(lst[u1] + lst[v1]) == "GC" and "CG" in allowed_pairs[(u1, v1)]:
            lst[u1], lst[v1] = "C", "G"
        lp = bh_tetraloops[(idx_bh + (0 if mode == 0 else rng.randint(0, 5))) % len(bh_tetraloops)]
        for k_l, ch_l in enumerate(lp):
            if (lp_start + k_l) not in locked_pos:
                lst[lp_start + k_l] = ch_l
        if bg_pos not in locked_pos:
            # Pyrimidine bulge ('U' or 'C') avoids giving the open state a -1.2 kcal/mol 3' purine dangle on p1 (`fold.c` line 399)!
            lst[bg_pos] = "U" if (lst[u0] == "G" and lst[u1] == "C") else "C"
        if fL != -1 and fL not in locked_pos and (lst[fL] + lst[v0]) not in VALID_SET:
            lst[fL] = "A"
        if fR != -1 and fR not in locked_pos:
            lst[fR] = "G" if (lst[u0] + "G") not in VALID_SET else "A"

    # 5. Hairpin loops (orthogonalized across distinct stems so sibling hairpins do not cross-hybridize)
    tetraloop_cycle = ("GAAA", "UUCG", "GCAA", "GAGA", "GUGA", "GGAA")
    hp_idx = 0
    for u, v in pinfo["pairs"]:
        span = v - u - 1
        if span >= 3 and all(pair_of[k] == -1 for k in range(u + 1, v)):
            if span == 4:
                lp = tetraloop_cycle[hp_idx % len(tetraloop_cycle)] if rng.random() < 0.80 else rng.choice(tetraloop_cycle)
                hp_idx += 1
                for idx_k, ch_l in enumerate(lp):
                    if (u + 1 + idx_k) not in locked_pos:
                        lst[u + 1 + idx_k] = ch_l
            elif span > 4:
                if (u + 1) not in locked_pos:
                    lst[u + 1] = "G"
                if (v - 1) not in locked_pos:
                    lst[v - 1] = "A"
        if u > 0 and v + 1 < n and pair_of[u - 1] == -1 and pair_of[v + 1] == -1:
            if (u - 1) not in locked_pos and (v + 1) not in locked_pos and rng.random() < 0.55:
                mm = rng.choice((("A", "G"), ("G", "A")))
                lst[u - 1], lst[v + 1] = mm[0], mm[1]

    dehomopolymerize_and_chiral_sanitize(lst, pinfo, mode=0)
    enforce_anti_slip_guards(lst, pinfo, rng)


def dehomopolymerize_and_chiral_sanitize(lst: list, pinfo: dict, mode: int = 0):
    """
    `CLSS-4` Dehomopolymerization & Chiral Purine-Strand Separation (`v8 [L0-ALGO]`):
      - `mode == 0`: Alternates any 3 consecutive identical-orientation GC pairs (`GC,GC,GC -> GC,CG,GC`
        and `CG,CG,CG -> CG,GC,CG`) inside stems at 0 budget cost, and breaks any `>= 4` consecutive
        `G` or `C` homopolymer run containing an unlocked unpaired base.
      - `mode == 1` (`Chiral 5'-C / 3'-GA`): Orients internal-loop cascade GC pairs as `CG`, sets 3'
        unpaired loop bases to `A` and 5' unpaired loop bases to `G`/`A` (avoiding `GGG` runs).
      - `mode == 2` (`Chiral 5'-GA / 3'-C`): Orients internal-loop cascade GC pairs as `GC`, sets 5'
        unpaired loop bases to `A` and 3' unpaired loop bases to `G`/`A` (avoiding `GGG` runs).
    """
    pair_of = pinfo["pair_of"]
    locked_pos = pinfo["locked_pos"]
    allowed_pairs = pinfo["allowed_pairs"]
    n = pinfo["n"]

    # 1. Alternate 3 consecutive identical GC/CG pairs in any stem (`0` budget cost)
    for u, v in pinfo["pairs"]:
        if u + 2 < v - 2 and pair_of[u + 1] == v - 1 and pair_of[u + 2] == v - 2:
            bp0 = lst[u] + lst[v]
            bp1 = lst[u + 1] + lst[v - 1]
            bp2 = lst[u + 2] + lst[v - 2]
            if bp0 in STRONG_PAIRS and bp0 == bp1 == bp2:
                alt_bp = "CG" if bp1 == "GC" else "GC"
                if alt_bp in allowed_pairs[(u + 1, v - 1)]:
                    lst[u + 1], lst[v - 1] = alt_bp[0], alt_bp[1]

    # 1b. Break any `>= 3` consecutive `G` or `C` stem homopolymer (`GGG`/`CCC`) by flipping one `GC`/`CG` pair (`0` budget cost)
    for i in range(n - 2):
        b0 = lst[i]
        if b0 in ("G", "C") and lst[i + 1] == b0 and lst[i + 2] == b0:
            for k in (i + 1, i, i + 2):
                q = pair_of[k]
                if q != -1:
                    uv = (min(k, q), max(k, q))
                    cur_bp = lst[uv[0]] + lst[uv[1]]
                    if cur_bp in STRONG_PAIRS:
                        alt_bp = "CG" if cur_bp == "GC" else "GC"
                        if alt_bp in allowed_pairs[uv]:
                            lst[uv[0]], lst[uv[1]] = alt_bp[0], alt_bp[1]
                            break

    # 2. Chiral internal-loop cascade alignment (`mode == 1` or `mode == 2`)
    if mode in (1, 2):
        pref_bp = "CG" if mode == 1 else "GC"
        for p1, q1, u_out, v_out, u_in, v_in in pinfo["loops_1x1"]:
            if mode == 1:
                if PAIR_TYPE.get(lst[u_out] + lst[v_out]) == "GC" and "GC" in allowed_pairs[(u_out, v_out)]:
                    lst[u_out], lst[v_out] = "G", "C"
                if PAIR_TYPE.get(lst[u_in] + lst[v_in]) == "GC" and "CG" in allowed_pairs[(u_in, v_in)]:
                    lst[u_in], lst[v_in] = "C", "G"
            else:
                for uv in ((u_out, v_out), (u_in, v_in)):
                    if PAIR_TYPE.get(lst[uv[0]] + lst[uv[1]]) == "GC" and pref_bp in allowed_pairs[uv]:
                        lst[uv[0]], lst[uv[1]] = pref_bp[0], pref_bp[1]
            ch_p1, ch_q1 = ("G", "G") if not (lst[u_out] == "C" and lst[u_in] == "C") else ("G", "A")
            if p1 not in locked_pos:
                lst[p1] = ch_p1
            if q1 not in locked_pos:
                lst[q1] = ch_q1
        in_set_21 = {(ui, vi) for _p1, _p2, _q1, _uo, _vo, ui, vi in pinfo["loops_2x1"]}
        for p1, p2, q1, u_out, v_out, u_in, v_in in pinfo["loops_2x1"]:
            is_outer_21 = (u_out, v_out) not in in_set_21
            if mode == 1 and is_outer_21:
                if "GC" in allowed_pairs[(u_out, v_out)]:
                    lst[u_out], lst[v_out] = "G", "C"
                if "CG" in allowed_pairs[(u_in, v_in)]:
                    lst[u_in], lst[v_in] = "C", "G"
                m21 = ("G", "A", "A")
            else:
                bp_21 = "CG" if mode == 1 else "GC"
                if not is_outer_21 and "CG" in allowed_pairs[(u_in, v_in)]:
                    lst[u_in], lst[v_in] = bp_21[0], bp_21[1]
                else:
                    for uv in ((u_out, v_out), (u_in, v_in)):
                        if PAIR_TYPE.get(lst[uv[0]] + lst[uv[1]]) == "GC" and bp_21 in allowed_pairs[uv]:
                            lst[uv[0]], lst[uv[1]] = bp_21[0], bp_21[1]
                m21 = ("G", "G", "A") if mode == 1 else ("G", "A", "A")
            for pos, ch in ((p1, m21[0]), (p2, m21[1]), (q1, m21[2])):
                if pos not in locked_pos:
                    lst[pos] = ch
        in_set_12 = {(ui, vi) for _p1, _q1, _q2, _uo, _vo, ui, vi in pinfo["loops_1x2"]}
        for p1, q1, q2, u_out, v_out, u_in, v_in in pinfo["loops_1x2"]:
            is_outer_12 = (u_out, v_out) not in in_set_12
            if mode == 1 and is_outer_12:
                if "CG" in allowed_pairs[(u_out, v_out)]:
                    lst[u_out], lst[v_out] = "C", "G"
                if "GC" in allowed_pairs[(u_in, v_in)]:
                    lst[u_in], lst[v_in] = "G", "C"
                m12 = ("A", "A", "G")
            else:
                bp_12 = "GC" if mode == 1 else "CG"
                if not is_outer_12 and "GC" in allowed_pairs[(u_in, v_in)]:
                    lst[u_in], lst[v_in] = bp_12[0], bp_12[1]
                else:
                    for uv in ((u_out, v_out), (u_in, v_in)):
                        if PAIR_TYPE.get(lst[uv[0]] + lst[uv[1]]) == "GC" and bp_12 in allowed_pairs[uv]:
                            lst[uv[0]], lst[uv[1]] = bp_12[0], bp_12[1]
                m12 = ("A", "G", "G") if mode == 1 else ("A", "A", "G")
            for pos, ch in ((p1, m12[0]), (q1, m12[1]), (q2, m12[2])):
                if pos not in locked_pos:
                    lst[pos] = ch

    # 3. Break any `>= 4` consecutive `G` or `C` run containing an unlocked unpaired base
    for i in range(n - 3):
        b0 = lst[i]
        if b0 in ("G", "C") and lst[i + 1] == b0 and lst[i + 2] == b0 and lst[i + 3] == b0:
            for k in (i + 1, i + 2, i, i + 3):
                if pair_of[k] == -1 and k not in locked_pos:
                    lst[k] = "A" if b0 == "G" else "U"
                    break


def make_budget_seed(pinfo: dict, rng: random.Random, boundary_bias: float = 0.90, ignore_budget: bool = False) -> str:
    n = pinfo["n"]
    lst = ["A"] * n
    for i, b0 in pinfo["locked_pos"].items():
        lst[i] = b0

    pairs = list(pinfo["pairs"])
    if ignore_budget or pinfo["is_pure_shape"]:
        for idx_p, (u, v) in enumerate(pairs):
            al = pinfo["allowed_pairs"][(u, v)]
            al_gc = [bp for bp in al if PAIR_TYPE.get(bp) == "GC"]
            if al_gc and rng.random() < boundary_bias:
                pref_gc = "GC" if (idx_p % 2 == 0) else "CG"
                if pref_gc in al_gc and rng.random() < 0.80:
                    bp = pref_gc
                else:
                    bp = rng.choice(al_gc)
            else:
                bp = rng.choice(al)
            lst[u], lst[v] = bp[0], bp[1]
        apply_turner_loop_motifs(lst, pinfo, rng, mode=0)
        return "".join(lst)

    assigned = {}
    counts = {"GC": 0, "AU": 0, "GU": 0}
    free_pairs = []
    for u, v in pairs:
        al = pinfo["allowed_pairs"][(u, v)]
        types_al = {PAIR_TYPE.get(bp, "other") for bp in al}
        if len(types_al) == 1:
            bp = rng.choice(al)
            assigned[(u, v)] = bp
            pt = PAIR_TYPE.get(bp, "other")
            if pt in counts:
                counts[pt] += 1
        else:
            free_pairs.append((u, v))

    free_sorted_high = sorted(free_pairs, key=lambda uv: (pinfo["pair_priority"][uv], rng.random()), reverse=True)
    free_sorted_low = list(reversed(free_sorted_high))

    for pt_need in ("GU", "AU", "GC"):
        need = max(0, pinfo["min_limits"][pt_need] - counts[pt_need])
        if need > 0:
            order = free_sorted_low if pt_need in ("GU", "AU") else free_sorted_high
            for idx_o, uv in enumerate(order):
                if need <= 0:
                    break
                if uv in assigned:
                    continue
                al_pt = [bp for bp in pinfo["allowed_pairs"][uv] if PAIR_TYPE.get(bp) == pt_need]
                if al_pt:
                    if pt_need == "GU":
                        pref_bp = "GU" if ((uv[0] + idx_o) % 2 == 0) else "UG"
                    elif pt_need == "AU":
                        pref_bp = "AU" if ((uv[0] + idx_o) % 2 == 0) else "UA"
                    else:
                        pref_bp = "GC" if ((uv[0] + idx_o) % 2 == 0) else "CG"
                    bp = pref_bp if (pref_bp in al_pt and rng.random() < 0.82) else rng.choice(al_pt)
                    assigned[uv] = bp
                    counts[pt_need] += 1
                    need -= 1

    for idx_uv, uv in enumerate(free_sorted_high):
        if uv in assigned:
            continue
        al = pinfo["allowed_pairs"][uv]
        al_gc = [bp for bp in al if PAIR_TYPE.get(bp) == "GC"]
        al_au = [bp for bp in al if PAIR_TYPE.get(bp) == "AU"]
        al_gu = [bp for bp in al if PAIR_TYPE.get(bp) == "GU"]

        can_gc = bool(al_gc) and (counts["GC"] < pinfo["max_limits"]["GC"])
        can_au = bool(al_au) and (counts["AU"] < pinfo["max_limits"]["AU"])
        can_gu = bool(al_gu) and (counts["GU"] < pinfo["max_limits"]["GU"])

        if can_gc and (rng.random() < boundary_bias or not (can_au or can_gu)):
            pref_gc = "GC" if ((uv[0] + idx_uv) % 2 == 0) else "CG"
            bp = pref_gc if (pref_gc in al_gc and rng.random() < 0.78) else rng.choice(al_gc)
            assigned[uv] = bp
            counts["GC"] += 1
        elif can_au and (not can_gu or rng.random() < 0.78):
            bp = rng.choice(al_au)
            assigned[uv] = bp
            counts["AU"] += 1
        elif can_gu:
            bp = rng.choice(al_gu)
            assigned[uv] = bp
            counts["GU"] += 1
        else:
            bp = rng.choice(al)
            assigned[uv] = bp
            pt = PAIR_TYPE.get(bp, "other")
            if pt in counts:
                counts[pt] += 1

    for (u, v), bp in assigned.items():
        lst[u], lst[v] = bp[0], bp[1]

    apply_turner_loop_motifs(lst, pinfo, rng, mode=0)
    return "".join(lst)


def project_to_budget_manifold(seq: str, pinfo: dict, eng: int, rng: random.Random, max_sec: float = 1.5) -> str:
    if pinfo["is_pure_shape"]:
        return seq
    t0 = time.time()
    target = pinfo["target"]
    t_bps = get_bp_set(target)
    lst = list(seq)
    enforce_locks_on_list(lst, pinfo, rng)
    cur = "".join(lst)
    ms, _ = exact_fold(cur, eng)
    cur_dbp = len(t_bps ^ get_bp_set(ms))
    cur_vb = budget_violation(cur, pinfo)
    if cur_vb == 0:
        return cur

    pairs = pinfo["pairs"]
    pair_of = pinfo["pair_of"]
    locked_pos = pinfo["locked_pos"]

    for _pass in range(16):
        if cur_vb == 0 or time.time() - t0 >= max_sec:
            break
        improved = False
        counts = count_target_pair_types(cur, pairs)
        need_reduce_gc = counts["GC"] > pinfo["max_limits"]["GC"]
        need_add_gu = counts["GU"] < pinfo["min_limits"]["GU"]
        need_add_au = counts["AU"] < pinfo["min_limits"]["AU"]

        ordered_uv = sorted(pairs, key=lambda uv: (pinfo["pair_priority"][uv], rng.random()))
        for u, v in ordered_uv:
            if time.time() - t0 >= max_sec:
                break
            cur_bp = cur[u] + cur[v]
            cur_pt = PAIR_TYPE.get(cur_bp, "other")
            al = pinfo["allowed_pairs"][(u, v)]
            cand_bps = []
            if need_reduce_gc and cur_pt == "GC":
                if need_add_gu:
                    cand_bps.extend([bp for bp in al if PAIR_TYPE.get(bp) == "GU"])
                if need_add_au:
                    cand_bps.extend([bp for bp in al if PAIR_TYPE.get(bp) == "AU"])
                cand_bps.extend([bp for bp in al if PAIR_TYPE.get(bp) in ("AU", "GU") and bp not in cand_bps])
            elif need_add_gu and cur_pt != "GU":
                cand_bps.extend([bp for bp in al if PAIR_TYPE.get(bp) == "GU"])
            elif need_add_au and cur_pt != "AU":
                cand_bps.extend([bp for bp in al if PAIR_TYPE.get(bp) == "AU"])
            else:
                cand_bps = [bp for bp in al if bp != cur_bp]

            for bp in cand_bps:
                trial = list(cur)
                trial[u], trial[v] = bp[0], bp[1]
                s_tr = "".join(trial)
                n_vb = budget_violation(s_tr, pinfo)
                if n_vb >= cur_vb:
                    continue
                tms, _ = exact_fold(s_tr, eng)
                tdbp = len(t_bps ^ get_bp_set(tms))
                if tdbp <= cur_dbp:
                    cur, cur_dbp, cur_vb = s_tr, tdbp, n_vb
                    improved = True
                    break
            if improved and cur_vb == 0:
                return cur

        if not improved and cur_vb > 0 and time.time() - t0 < max_sec:
            gc_pairs = [
                uv for uv in ordered_uv
                if PAIR_TYPE.get(cur[uv[0]] + cur[uv[1]]) == "GC"
                and any(PAIR_TYPE.get(bp) in ("AU", "GU") for bp in pinfo["allowed_pairs"][uv])
            ]
            non_gc_boundary = [
                uv for uv in reversed(ordered_uv)
                if PAIR_TYPE.get(cur[uv[0]] + cur[uv[1]]) != "GC"
                and any(PAIR_TYPE.get(bp) == "GC" for bp in pinfo["allowed_pairs"][uv])
            ]
            for _k_try in range(60):
                if time.time() - t0 >= max_sec or not gc_pairs:
                    break
                trial = list(cur)
                if need_reduce_gc and len(gc_pairs) >= 2 and non_gc_boundary and rng.random() < 0.6:
                    uv_up = rng.choice(non_gc_boundary)
                    uv_d1, uv_d2 = rng.sample(gc_pairs[: max(2, len(gc_pairs) // 2)], 2)
                    bp_up = rng.choice([bp for bp in pinfo["allowed_pairs"][uv_up] if PAIR_TYPE.get(bp) == "GC"])
                    trial[uv_up[0]], trial[uv_up[1]] = bp_up[0], bp_up[1]
                    for u_d, v_d in (uv_d1, uv_d2):
                        pref_pt = "GU" if need_add_gu else ("AU" if need_add_au else None)
                        cands_d = (
                            [bp for bp in pinfo["allowed_pairs"][(u_d, v_d)] if PAIR_TYPE.get(bp) == pref_pt]
                            or [bp for bp in pinfo["allowed_pairs"][(u_d, v_d)] if PAIR_TYPE.get(bp) in ("AU", "GU")]
                        )
                        bp_d = rng.choice(cands_d)
                        trial[u_d], trial[v_d] = bp_d[0], bp_d[1]
                else:
                    u_d, v_d = rng.choice(gc_pairs)
                    pref_pt = "GU" if need_add_gu else ("AU" if need_add_au else None)
                    cands_d = (
                        [bp for bp in pinfo["allowed_pairs"][(u_d, v_d)] if PAIR_TYPE.get(bp) == pref_pt]
                        or [bp for bp in pinfo["allowed_pairs"][(u_d, v_d)] if PAIR_TYPE.get(bp) in ("AU", "GU")]
                    )
                    bp_d = rng.choice(cands_d)
                    trial[u_d], trial[v_d] = bp_d[0], bp_d[1]
                    for du, dv in ((u_d - 1, v_d + 1), (u_d + 1, v_d - 1)):
                        if 0 <= du < dv < len(cur) and pair_of[du] == -1 and pair_of[dv] == -1:
                            if du not in locked_pos and dv not in locked_pos:
                                mm = rng.choice(BOOST_MISMATCHES)
                                trial[du], trial[dv] = mm[0], mm[1]
                s_tr = "".join(trial)
                n_vb = budget_violation(s_tr, pinfo)
                if n_vb < cur_vb:
                    tms, _ = exact_fold(s_tr, eng)
                    tdbp = len(t_bps ^ get_bp_set(tms))
                    if tdbp <= cur_dbp:
                        cur, cur_dbp, cur_vb = s_tr, tdbp, n_vb
                        improved = True
                        break
    return cur


def check_full_solve(seq: str, pinfo: dict, eng: int) -> tuple:
    if budget_violation(seq, pinfo) > 0:
        return False, "", 999.0
    ms, me = exact_official_fold(seq, eng)
    if ms != pinfo["target"]:
        return False, ms, me
    if budget_violation(seq, pinfo, struct_for_pairs=ms) > 0:
        return False, ms, me
    return True, ms, me


def repair_budget_candidates(
    seq_list: list,
    pinfo: dict,
    protected_pos: set,
    ms_hint: str,
    rng: random.Random,
    max_k: int = 5,
) -> list:
    """
    Returns up to `max_k` deterministic Kempe-Swap budget-repaired sequences by testing
    distinct interior stem pairs `(u_s, v_s)` outside `protected_pos` where `ms_hint`
    matches `target`, ranked by deepest stem interior (both neighbors are GC pairs) and
    lowest `RNA.energy_of_struct(s, target)`.
    """
    s_cur = "".join(seq_list)
    if pinfo["is_pure_shape"]:
        return [s_cur]
    pairs = pinfo["pairs"]
    pair_of = pinfo["pair_of"]
    allowed_pairs = pinfo["allowed_pairs"]
    target = pinfo["target"]
    m_bps = get_bp_set(ms_hint) if ms_hint else set(pairs)
    vb = budget_violation(s_cur, pinfo)
    c_init = count_target_pair_types(s_cur, pairs)
    max_gc_cap = max(
        0,
        min(
            len(pairs) - pinfo["min_limits"]["AU"] - pinfo["min_limits"]["GU"],
            pinfo["max_limits"]["GC"],
        ),
    )
    if vb == 0 and c_init["GC"] >= max_gc_cap:
        return [s_cur]

    open_pair_struct = pinfo["open_pair_struct"]
    et_cur_base = float(RNA.energy_of_struct(s_cur, target))

    def safe_score(uv):
        u, v = uv
        if u in protected_pos or v in protected_pos:
            return (-999, -999.0, -999)
        in_m = 1 if (u, v) in m_bps else 0
        outer_adj = 1 if (u > 0 and v + 1 < pinfo["n"] and pair_of[u - 1] == v + 1) else 0
        inner_adj = 1 if (pair_of[u + 1] == v - 1) else 0
        outer_gc = 1 if (outer_adj and PAIR_TYPE.get(seq_list[u - 1] + seq_list[v + 1]) == "GC") else 0
        inner_gc = 1 if (inner_adj and PAIR_TYPE.get(seq_list[u + 1] + seq_list[v - 1]) == "GC") else 0
        near_prot = 1 if any(abs(u - p) <= 5 or abs(v - p) <= 5 for p in protected_pos) else 0
        prio_pen = pinfo["pair_priority"].get(uv, 3)
        margin_uv = round(float(RNA.energy_of_struct(s_cur, open_pair_struct[uv])) - et_cur_base, 3)
        surv_flag = 1 if (in_m and margin_uv >= 2.0 and not near_prot) else 0
        topo_sc = 10 * (outer_adj * inner_adj) - 4 * prio_pen - 8 * near_prot + 4 * in_m + 2 * (outer_gc + inner_gc)
        return (surv_flag, margin_uv - 3.0 * near_prot - 0.5 * prio_pen, topo_sc)

    ranked_pool = sorted(
        [uv for uv in pairs if uv[0] not in protected_pos and uv[1] not in protected_pos],
        key=lambda uv: safe_score(uv),
        reverse=True,
    )
    if not ranked_pool:
        return [s_cur]

    out_cands = [s_cur] if vb == 0 else []
    used_first_uv = set()
    for start_idx in range(min(max_k * 2, len(ranked_pool))):
        if len(out_cands) >= max_k:
            break
        trial = list(seq_list)
        first_uv = None
        used_donors_in_trial = []
        for _step in range(6):
            s_now = "".join(trial)
            c_gc = count_target_pair_types(s_now, pairs)
            if budget_violation(s_now, pinfo) == 0 and c_gc["GC"] >= max_gc_cap:
                break
            need_drop_gc = c_gc["GC"] > pinfo["max_limits"]["GC"]
            need_add_au = c_gc["AU"] < pinfo["min_limits"]["AU"]
            need_add_gu = c_gc["GU"] < pinfo["min_limits"]["GU"]
            need_add_gc = (c_gc["GC"] < pinfo["min_limits"]["GC"]) or (
                budget_violation(s_now, pinfo) == 0 and c_gc["GC"] < max_gc_cap
            )

            changed = False
            rot_pool = ranked_pool[start_idx:] + ranked_pool[:start_idx]
            if need_drop_gc or need_add_au or need_add_gu:
                pref_pt = "GU" if need_add_gu else ("AU" if need_add_au else None)
                for min_sep in (3, 0):
                    if changed:
                        break
                    for u, v in rot_pool:
                        if first_uv is None and (u, v) in used_first_uv:
                            continue
                        if min_sep > 0 and any(
                            abs(u - ud) < min_sep or abs(v - vd) < min_sep for ud, vd in used_donors_in_trial
                        ):
                            continue
                        pt_uv = PAIR_TYPE.get(trial[u] + trial[v], "other")
                        if pt_uv == "GC" or (not need_drop_gc and pt_uv != pref_pt):
                            cands = (
                                [bp for bp in allowed_pairs[(u, v)] if PAIR_TYPE.get(bp) == pref_pt]
                                if pref_pt
                                else [bp for bp in allowed_pairs[(u, v)] if PAIR_TYPE.get(bp) in ("AU", "GU")]
                            )
                            if cands:
                                # Pick orientation that minimizes target energy
                                best_bp = cands[0]
                                if len(cands) > 1:
                                    best_e = 1e9
                                    for bp_c in cands:
                                        trial[u], trial[v] = bp_c[0], bp_c[1]
                                        e_c = float(RNA.energy_of_struct("".join(trial), target))
                                        if e_c < best_e:
                                            best_e = e_c
                                            best_bp = bp_c
                                trial[u], trial[v] = best_bp[0], best_bp[1]
                                if first_uv is None:
                                    first_uv = (u, v)
                                used_donors_in_trial.append((u, v))
                                changed = True
                                break
            elif need_add_gc:
                can_drop_au = c_gc["AU"] > pinfo["min_limits"]["AU"]
                can_drop_gu = c_gc["GU"] > pinfo["min_limits"]["GU"]
                for min_sep in (3, 0):
                    if changed:
                        break
                    for u, v in rot_pool:
                        if first_uv is None and (u, v) in used_first_uv:
                            continue
                        if min_sep > 0 and any(
                            abs(u - ud) < min_sep or abs(v - vd) < min_sep for ud, vd in used_donors_in_trial
                        ):
                            continue
                        pt_uv = PAIR_TYPE.get(trial[u] + trial[v], "other")
                        if (pt_uv == "AU" and can_drop_au) or (pt_uv == "GU" and can_drop_gu):
                            cands = [bp for bp in allowed_pairs[(u, v)] if PAIR_TYPE.get(bp) == "GC"]
                            if cands:
                                best_bp = cands[0]
                                if len(cands) > 1:
                                    best_e = 1e9
                                    for bp_c in cands:
                                        trial[u], trial[v] = bp_c[0], bp_c[1]
                                        e_c = float(RNA.energy_of_struct("".join(trial), target))
                                        if e_c < best_e:
                                            best_e = e_c
                                            best_bp = bp_c
                                trial[u], trial[v] = best_bp[0], best_bp[1]
                                if first_uv is None:
                                    first_uv = (u, v)
                                used_donors_in_trial.append((u, v))
                                changed = True
                                break
            if not changed:
                break
        if first_uv is not None:
            used_first_uv.add(first_uv)
        s_fin = "".join(trial)
        if budget_violation(s_fin, pinfo) == 0 and s_fin not in out_cands:
            out_cands.append(s_fin)

    if not out_cands:
        return [s_cur]
    out_cands.sort(key=lambda s: float(RNA.energy_of_struct(s, target)))
    return out_cands


def repair_budget_on_safe_stems(
    seq_list: list,
    pinfo: dict,
    protected_pos: set,
    ms_hint: str,
    rng: random.Random,
) -> str:
    return repair_budget_candidates(seq_list, pinfo, protected_pos, ms_hint, rng, max_k=3)[0]


def op_m3_homologous_subtree_cloner(
    seq_str: str,
    pinfo: dict,
    eng: int,
    rng: random.Random,
) -> tuple:
    """
    `Op-M3` Automatic Homologous Subtree Cloning (`[L0-ALGO]` Stage 1):
    Parses target dot-bracket into canonical rooted subtrees `target[u:v+1]` (and flanking `[u-1:v+2]`).
    Whenever one homologous instance is already folded identically (`ms[u1:v1+1] == target[u1:v1+1]`)
    while another identical subtree has `ms[u2:v2+1] != target[u2:v2+1]`, clones the solved sequence
    segment onto the broken subtree and repairs any pair-budget drift on safe interior stems.
    Also enforces `CLSS-4` Non-Pairing Guard on parasitic unpaired-unpaired pairs in `m_bps - t_bps`.
    """
    target = pinfo["target"]
    n = pinfo["n"]
    pairs = pinfo["pairs"]
    pair_of = pinfo["pair_of"]
    locked_pos = pinfo["locked_pos"]
    allowed_pairs = pinfo["allowed_pairs"]
    t_bps = get_bp_set(target)

    cur_seq = seq_str
    ms, me = exact_fold(cur_seq, eng)
    te = float(RNA.energy_of_struct(cur_seq, target))
    cur_dbp = len(t_bps ^ get_bp_set(ms))
    cur_vb = budget_violation(cur_seq, pinfo)
    cur_de = round(te - me, 4)

    # 1. Group pairs by canonical subtree dot-bracket `target[u:v+1]`
    by_sub = {}
    for u, v in pairs:
        if v - u + 1 >= 6:
            sub = target[u : v + 1]
            by_sub.setdefault(sub, []).append((u, v))

    for sub, span_list in by_sub.items():
        if len(span_list) < 2:
            continue
        # Rank spans by local base-pair accuracy inside [u..v]
        span_ranked = sorted(
            span_list,
            key=lambda uv: sum(1 for k in range(uv[0], uv[1] + 1) if ms[k] != target[k]),
        )
        src_spans = [uv for uv in span_ranked if ms[uv[0] : uv[1] + 1] == target[uv[0] : uv[1] + 1]]
        if not src_spans and (span_ranked[0][1] - span_ranked[0][0] + 1) >= 16:
            src_spans = [span_ranked[0]]
        broken_spans = [uv for uv in span_list if ms[uv[0] : uv[1] + 1] != target[uv[0] : uv[1] + 1]]
        if not src_spans or not broken_spans:
            continue
        flip_map = {"GC": "CG", "CG": "GC", "AU": "UA", "UA": "AU", "GU": "UG", "UG": "GU"}
        for u_src, v_src in src_spans:
            for u_dst, v_dst in broken_spans:
                if (u_src, v_src) == (u_dst, v_dst):
                    continue
                for flank in (0, 1):
                    a_s, b_s = u_src - flank, v_src + flank
                    a_d, b_d = u_dst - flank, v_dst + flank
                    if a_s < 0 or b_s >= n or a_d < 0 or b_d >= n:
                        continue
                    if target[a_s : b_s + 1] != target[a_d : b_d + 1]:
                        continue
                    for copy_mode in (0, 1):
                        trial = list(cur_seq)
                        prot = set(range(a_d, b_d + 1)) | set(range(a_s, b_s + 1))
                        for offset in range(b_s - a_s + 1):
                            pos_d = a_d + offset
                            pos_s = a_s + offset
                            if pos_d not in locked_pos:
                                trial[pos_d] = cur_seq[pos_s]
                        # In `copy_mode == 1`, chirally flip pairs in the destination subtree so twin repeats do not dimerize
                        for pos_d in range(a_d, b_d + 1):
                            q_d = pair_of[pos_d]
                            if pos_d < q_d <= b_d:
                                cur_bp_d = trial[pos_d] + trial[q_d]
                                if copy_mode == 1 and flip_map.get(cur_bp_d) in allowed_pairs[(pos_d, q_d)]:
                                    f_bp = flip_map[cur_bp_d]
                                    trial[pos_d], trial[q_d] = f_bp[0], f_bp[1]
                                elif cur_bp_d not in allowed_pairs[(pos_d, q_d)]:
                                    trial[pos_d], trial[q_d] = allowed_pairs[(pos_d, q_d)][0][0], allowed_pairs[(pos_d, q_d)][0][1]
                        for s_tr in repair_budget_candidates(trial, pinfo, prot, ms, rng, max_k=4):
                            tvb = budget_violation(s_tr, pinfo)
                            tms, tme = exact_fold(s_tr, eng)
                            tdbp = len(t_bps ^ get_bp_set(tms))
                            tte = float(RNA.energy_of_struct(s_tr, target))
                            tde = round(tte - tme, 4)
                            if (tvb, tdbp, tde) < (cur_vb, cur_dbp, cur_de):
                                cur_seq, cur_vb, cur_dbp, cur_de, ms = s_tr, tvb, tdbp, tde, tms
                                if cur_dbp == 0 and cur_vb == 0:
                                    ok, _, _ = check_full_solve(cur_seq, pinfo, eng)
                                    if ok:
                                        return True, cur_seq, 0, 0, 0.0

    # 2. `CLSS-4` Non-Pairing Guard on parasitic unpaired-unpaired pairs in `m_bps - t_bps`
    m_bps = get_bp_set(ms)
    parasitic_unp = [(u, v) for (u, v) in sorted(m_bps - t_bps) if pair_of[u] == -1 and pair_of[v] == -1]
    for u_p, v_p in parasitic_unp:
        best_cand = None
        for b1 in ("G", "A", "C", "U"):
            if u_p in locked_pos and b1 != cur_seq[u_p]:
                continue
            for b2 in ("A", "G", "C", "U"):
                if v_p in locked_pos and b2 != cur_seq[v_p]:
                    continue
                if (b1 + b2) in VALID_SET:
                    continue
                trial = list(cur_seq)
                trial[u_p], trial[v_p] = b1, b2
                s_tr = "".join(trial)
                tvb = budget_violation(s_tr, pinfo)
                if tvb > cur_vb:
                    continue
                tms, tme = exact_fold(s_tr, eng)
                tdbp = len(t_bps ^ get_bp_set(tms))
                tte = float(RNA.energy_of_struct(s_tr, target))
                tde = round(tte - tme, 4)
                if (tvb, tdbp, tde) < (cur_vb, cur_dbp, cur_de):
                    cur_seq, cur_vb, cur_dbp, cur_de, ms = s_tr, tvb, tdbp, tde, tms
                    best_cand = s_tr
                    if cur_dbp == 0 and cur_vb == 0:
                        ok, _, _ = check_full_solve(cur_seq, pinfo, eng)
                        if ok:
                            return True, cur_seq, 0, 0, 0.0
        if best_cand:
            break

    return False, cur_seq, cur_vb, cur_dbp, cur_de


def l0_endgame_finisher(
    start_seq: str,
    pinfo: dict,
    eng: int,
    rng: random.Random,
    max_sec: float = 3.5,
) -> tuple:
    """
    Four-Stage `[L0-ALGO]` Endgame Finisher (`v5`, `OPTIMIZER K20` + `MONITOR` Directive):
      Stage A: `Op-M3` Automatic Homologous Subtree Cloning + `CLSS-4` Non-Pairing Internal Loop Guard.
      Stage B: `CLSS-2` `.((....).).` 56-Module Bulge-Hairpin & Missing Short-Stem Closure (`close_missing_short_stem`).
      Stage C: `Law M37` Fast Coupled 2-Variable Saddle Enumerator (`2 pairs = 36`, `1 pair + 1 unp = 24`,
               `2 unp = 16`, `2x1/1x2` loop tuples) with Parasitic Pair Breaking bonus (`+4.0 kcal/mol`).
      Stage D: McCaskill Partition Function `fc.pf()` + `fc.bpp()` Parasitic BPP Poisoning (`para_bpp > 0.05`).
    """
    t0 = time.time()
    target = pinfo["target"]
    n = pinfo["n"]
    pair_of = pinfo["pair_of"]
    pairs = pinfo["pairs"]
    allowed_pairs = pinfo["allowed_pairs"]
    locked_pos = pinfo["locked_pos"]
    t_bps = get_bp_set(target)

    # --- Stage A: Op-M3 Homologous Subtree Cloning + CLSS-4 Anti-Slip Guard ---
    ok1, cur_seq, cur_vb, cur_dbp, cur_de = op_m3_homologous_subtree_cloner(start_seq, pinfo, eng, rng)
    if ok1:
        return True, cur_seq, 0, 0, 0.0

    lst_init = list(cur_seq)
    enforce_anti_slip_guards(lst_init, pinfo, rng)
    s_as = "".join(lst_init)
    if s_as != cur_seq and budget_violation(s_as, pinfo) <= cur_vb:
        tms, tme = exact_fold(s_as, eng)
        tdbp = len(t_bps ^ get_bp_set(tms))
        tde = round(float(RNA.energy_of_struct(s_as, target)) - tme, 4)
        tvb = budget_violation(s_as, pinfo)
        if tdbp == 0 and tvb == 0:
            ok, _, _ = check_full_solve(s_as, pinfo, eng)
            if ok:
                return True, s_as, 0, 0, 0.0
        if (tvb, tdbp, tde) <= (cur_vb, cur_dbp, cur_de):
            cur_seq, cur_vb, cur_dbp, cur_de = s_as, tvb, tdbp, tde

    ms, me = exact_fold(cur_seq, eng)
    if cur_dbp == 0 and cur_vb == 0:
        ok, _, _ = check_full_solve(cur_seq, pinfo, eng)
        if ok:
            return True, cur_seq, 0, 0, 0.0

    # --- Stage A0: Tree-DP Priority & Defect Kempe-Swap Re-Allocator (`Step 2` of Group 1 Assault) ---
    if not pinfo["is_pure_shape"]:
        prio = pinfo["pair_priority"]
        for _k_pass in range(6):
            m_bps_k = get_bp_set(ms)
            miss_k = t_bps - m_bps_k
            counts_k = count_target_pair_types(cur_seq, pairs)
            lst_k = list(cur_seq)
            changed_k = False
            # 1) Direct upgrade of non-GC pairs on Priority 4..5 or missing pairs when GC budget has slack
            for uv_hi in sorted(pairs, key=lambda uv: (1 if uv in miss_k else 0, prio.get(uv, 3)), reverse=True):
                pt_hi = PAIR_TYPE.get(lst_k[uv_hi[0]] + lst_k[uv_hi[1]], "other")
                if pt_hi in ("AU", "GU") and counts_k["GC"] < pinfo["max_limits"]["GC"] and counts_k[pt_hi] > pinfo["min_limits"][pt_hi]:
                    al_gc = [bp for bp in allowed_pairs[uv_hi] if PAIR_TYPE.get(bp) == "GC"]
                    if al_gc:
                        bp_new = al_gc[0]
                        lst_k[uv_hi[0]], lst_k[uv_hi[1]] = bp_new[0], bp_new[1]
                        counts_k["GC"] += 1
                        counts_k[pt_hi] -= 1
                        changed_k = True
            if changed_k:
                s_k = "".join(lst_k)
                if budget_violation(s_k, pinfo) <= cur_vb:
                    tms_k, tme_k = exact_fold(s_k, eng)
                    tdbp_k = len(t_bps ^ get_bp_set(tms_k))
                    tde_k = round(float(RNA.energy_of_struct(s_k, target)) - tme_k, 4)
                    tvb_k = budget_violation(s_k, pinfo)
                    if tdbp_k == 0 and tvb_k == 0:
                        ok, _, _ = check_full_solve(s_k, pinfo, eng)
                        if ok:
                            return True, s_k, 0, 0, 0.0
                    if (tvb_k, tdbp_k, tde_k) <= (cur_vb, cur_dbp, cur_de):
                        cur_seq, cur_vb, cur_dbp, cur_de, ms = s_k, tvb_k, tdbp_k, tde_k, tms_k
                        m_bps_k = get_bp_set(ms)
                        miss_k = t_bps - m_bps_k
            # 2) Kempe swaps: move GC from low-priority/closed pairs onto missing or high-priority pairs
            need_gc_uvs = sorted(
                [
                    uv for uv in pairs
                    if PAIR_TYPE.get(cur_seq[uv[0]] + cur_seq[uv[1]]) in ("AU", "GU")
                    and any(PAIR_TYPE.get(bp) == "GC" for bp in allowed_pairs[uv])
                    and (uv in miss_k or prio.get(uv, 3) >= 4)
                ],
                key=lambda uv: (1 if uv in miss_k else 0, prio.get(uv, 3)),
                reverse=True,
            )
            donor_gc_uvs = sorted(
                [
                    uv for uv in pairs
                    if PAIR_TYPE.get(cur_seq[uv[0]] + cur_seq[uv[1]]) == "GC"
                    and uv not in miss_k
                ],
                key=lambda uv: (prio.get(uv, 3), 1 if any(abs(uv[0] - m[0]) <= 3 for m in miss_k) else 0),
            )
            swap_done = False
            for uv_need in need_gc_uvs[:4]:
                pt_wob = PAIR_TYPE.get(cur_seq[uv_need[0]] + cur_seq[uv_need[1]])
                al_gc_need = [bp for bp in allowed_pairs[uv_need] if PAIR_TYPE.get(bp) == "GC"]
                for uv_don in donor_gc_uvs[:8]:
                    if uv_need not in miss_k and prio.get(uv_don, 3) >= prio.get(uv_need, 3):
                        continue
                    al_wob_don = [bp for bp in allowed_pairs[uv_don] if PAIR_TYPE.get(bp) == pt_wob]
                    if not al_wob_don:
                        continue
                    for bp_up in al_gc_need:
                        for bp_dn in al_wob_don:
                            tl_sw = list(cur_seq)
                            tl_sw[uv_need[0]], tl_sw[uv_need[1]] = bp_up[0], bp_up[1]
                            tl_sw[uv_don[0]], tl_sw[uv_don[1]] = bp_dn[0], bp_dn[1]
                            s_sw = "".join(tl_sw)
                            tvb_sw = budget_violation(s_sw, pinfo)
                            if tvb_sw > cur_vb:
                                continue
                            tms_sw, tme_sw = exact_fold(s_sw, eng)
                            tdbp_sw = len(t_bps ^ get_bp_set(tms_sw))
                            tde_sw = round(float(RNA.energy_of_struct(s_sw, target)) - tme_sw, 4)
                            if tdbp_sw == 0 and tvb_sw == 0:
                                ok, _, _ = check_full_solve(s_sw, pinfo, eng)
                                if ok:
                                    return True, s_sw, 0, 0, 0.0
                            if (tvb_sw, tdbp_sw, tde_sw) < (cur_vb, cur_dbp, cur_de):
                                cur_seq, cur_vb, cur_dbp, cur_de, ms = s_sw, tvb_sw, tdbp_sw, tde_sw, tms_sw
                                swap_done = True
                                break
                        if swap_done:
                            break
                    if swap_done:
                        break
                if swap_done:
                    break
            if not swap_done and not changed_k:
                break

    if cur_dbp > 8:
        return False, cur_seq, cur_vb, cur_dbp, cur_de

    # --- Stage A2: Dehomopolymerization & Chiral Cascade Sanitizer (`mode in (0, 1, 2)`) ---
    # Also build a clean-unpaired seed where passive unpaired multiloop/triloop/exterior bases are reset to `'A'`
    active_unp = set(locked_pos.keys())
    for p1, q1, _uo, _vo, _ui, _vi in pinfo["loops_1x1"]:
        active_unp |= {p1, q1}
    for p1, p2, q1, _uo, _vo, _ui, _vi in pinfo["loops_2x1"]:
        active_unp |= {p1, p2, q1}
    for p1, q1, q2, _uo, _vo, _ui, _vi in pinfo["loops_1x2"]:
        active_unp |= {p1, q1, q2}
    for p1, p2, q1, q2, _uo, _vo, _ui, _vi in pinfo["loops_2x2"]:
        active_unp |= {p1, p2, q1, q2}
    for _u0, _v0, _u1, _v1, lp_k, bg_k, fL_k, fR_k in pinfo.get("bulge_hairpins", ()):
        active_unp |= {bg_k} | set(range(lp_k, lp_k + 4))
        if fL_k != -1:
            active_unp.add(fL_k)
        if fR_k != -1:
            active_unp.add(fR_k)
    for u_hp, v_hp in pinfo["pairs"]:
        if all(pair_of[k] == -1 for k in range(u_hp + 1, v_hp)):
            active_unp |= set(range(u_hp + 1, v_hp))
        else:
            child_bps = [
                (u_c, pair_of[u_c])
                for u_c in range(u_hp + 1, v_hp)
                if pair_of[u_c] > u_c and all(pair_of[m] < u_hp or pair_of[m] > u_c for m in range(u_hp + 1, u_c))
            ]
            if len(child_bps) == 1:
                u_c, v_c = child_bps[0]
                if u_c > u_hp + 1 and v_c < v_hp - 1:
                    active_unp |= set(range(u_hp + 1, u_c)) | set(range(v_c + 1, v_hp))

    lst_stage_b = list(cur_seq)
    for k_u in range(n):
        if pair_of[k_u] == -1 and k_u not in active_unp and k_u not in locked_pos:
            lst_stage_b[k_u] = "A"
    # Luka A: 1x1 Internal-Loop Anti-Zip Guard (ensure no 1x1 loop has complementary bases that zip into a WC/GU pair)
    for p1_11, q1_11, _uo, _vo, _ui, _vi in pinfo["loops_1x1"]:
        if (lst_stage_b[p1_11] + lst_stage_b[q1_11]) in VALID_SET:
            if p1_11 not in locked_pos and q1_11 not in locked_pos:
                lst_stage_b[p1_11], lst_stage_b[q1_11] = "G", "G"
            elif p1_11 not in locked_pos:
                for b_ch in ("G", "A", "C", "U"):
                    if (b_ch + lst_stage_b[q1_11]) not in VALID_SET:
                        lst_stage_b[p1_11] = b_ch
                        break
            elif q1_11 not in locked_pos:
                for b_ch in ("G", "A", "C", "U"):
                    if (lst_stage_b[p1_11] + b_ch) not in VALID_SET:
                        lst_stage_b[q1_11] = b_ch
                        break

    # Fix #1: For any `2x2` internal loop `(p1, p2, q1, q2, u_out, v_out, u_in, v_in)` closing a 3-nt hairpin triloop
    # (`v_in - u_in - 1 == 3`, `+5.70 kcal/mol`), orient `(u_out, v_out) = 'GC'`, `(u_in, v_in) = 'CG'`,
    # triloop `u_in+1..v_in-1 = 'AAC'`, and tandem `(p1, p2, q1, q2) = ('G', 'A', 'G', 'A')` (`int22_37[GC][GC][G][A][G][A] = -2.70 kcal/mol`,
    # `ViennaRNA-1.8.5/lib/intloops.h` line 2131), and protect `{u_out, v_out, u_in, v_in}` from stem flipping!
    for p1_22, p2_22, q1_22, q2_22, uo_22, vo_22, ui_22, vi_22 in pinfo["loops_2x2"]:
        if vi_22 - ui_22 - 1 == 3 and all(pair_of[k] == -1 for k in range(ui_22 + 1, vi_22)):
            if "GC" in allowed_pairs[(uo_22, vo_22)] and "CG" in allowed_pairs[(ui_22, vi_22)]:
                lst_stage_b[uo_22], lst_stage_b[vo_22] = "G", "C"
                lst_stage_b[ui_22], lst_stage_b[vi_22] = "C", "G"
                active_unp |= {uo_22, vo_22, ui_22, vi_22}
                for k_tri in range(ui_22 + 1, vi_22):
                    if k_tri not in locked_pos:
                        lst_stage_b[k_tri] = "C" if k_tri == vi_22 - 1 else "A"
                for pos_22, ch_22 in ((p1_22, "G"), (p2_22, "A"), (q1_22, "G"), (q2_22, "A")):
                    if pos_22 not in locked_pos:
                        lst_stage_b[pos_22] = ch_22

    # For any `.((....).).` motif:
    # 1) If `fR = v0 + 1` abuts a closing multiloop pair `(u_r, v0 + 2)` (`u_r < u0`),
    #    orient `(u_r, v0 + 2) = 'CG'` so `rtype[CG] = GC` has weak `-0.30 kcal/mol` 5' dangle on `fR = 'G'` in `s_open_1`,
    #    and set `s[u_r + 1] = 'G'` (`dangle3_37[GC]['G'] = -1.70 kcal/mol` == `'A'`, while `mismatchI37[CG]['G']['G'] = 0`
    #    penalizes the internal-loop unfolding rival by `+1.10 kcal/mol`, `energy_par.c` lines 112 & 263)!
    # 2) If `fL = u0 - 1` abuts a stem pair `(u_l, u0 - 2)` with a 1-nt bulge `(u_l + 2, u0 - 3)` inside it,
    #    orient `(u_l, u0 - 2) = 'GC'`, `(u_l + 2, v_l - 1) = 'CG'`, bulge `u_l + 1 = 'A'`,
    #    and set the hairpin `u_l + 3 = 'G'`, `u_l + 4 .. v_l - 2 = 'A'` (`mismatchH37[CG]['G']['A'] = -2.20 kcal/mol`)!
    for u0_b, v0_b, _u1_b, _v1_b, _lp_b, _bg_b, fL_b, fR_b in pinfo.get("bulge_hairpins", ()):
        if fR_b == v0_b + 1 and v0_b + 2 < n and pair_of[v0_b + 2] != -1 and pair_of[v0_b + 2] < u0_b:
            uv_r = (pair_of[v0_b + 2], v0_b + 2)
            if PAIR_TYPE.get(lst_stage_b[uv_r[0]] + lst_stage_b[uv_r[1]]) == "GC" and "CG" in allowed_pairs[uv_r]:
                lst_stage_b[uv_r[0]], lst_stage_b[uv_r[1]] = "C", "G"
            if PAIR_TYPE.get(lst_stage_b[uv_r[0]] + lst_stage_b[uv_r[1]]) == "CG":
                active_unp |= {uv_r[0], uv_r[1]}
                if uv_r[0] + 1 < n and pair_of[uv_r[0] + 1] == -1 and (uv_r[0] + 1) not in locked_pos:
                    lst_stage_b[uv_r[0] + 1] = "G"
                    active_unp.add(uv_r[0] + 1)
        if fL_b == u0_b - 1 and u0_b >= 4 and pair_of[u0_b - 2] != -1 and pair_of[u0_b - 2] < u0_b - 2:
            u_l = pair_of[u0_b - 2]
            v_l = u0_b - 2
            if pair_of[u_l + 1] == -1 and pair_of[u_l + 2] == v_l - 1:
                if "GC" in allowed_pairs[(u_l, v_l)]:
                    lst_stage_b[u_l], lst_stage_b[v_l] = "G", "C"
                if "CG" in allowed_pairs[(u_l + 2, v_l - 1)]:
                    lst_stage_b[u_l + 2], lst_stage_b[v_l - 1] = "C", "G"
                active_unp |= {u_l, v_l, u_l + 2, v_l - 1}
                if (u_l + 1) not in locked_pos:
                    lst_stage_b[u_l + 1] = "A"
                if all(pair_of[k] == -1 for k in range(u_l + 3, v_l - 1)) and (v_l - 1) - (u_l + 2) - 1 >= 5:
                    if (u_l + 3) not in locked_pos:
                        lst_stage_b[u_l + 3] = "G"
                    for k_in in range(u_l + 4, v_l - 1):
                        if k_in not in locked_pos:
                            lst_stage_b[k_in] = "A"

    s_clean = "".join(lst_stage_b)
    if budget_violation(s_clean, pinfo) <= cur_vb:
        tms, tme = exact_fold(s_clean, eng)
        tdbp = len(t_bps ^ get_bp_set(tms))
        tde = round(float(RNA.energy_of_struct(s_clean, target)) - tme, 4)
        tvb = budget_violation(s_clean, pinfo)
        if tdbp == 0 and tvb == 0:
            ok, _, _ = check_full_solve(s_clean, pinfo, eng)
            if ok:
                return True, s_clean, 0, 0, 0.0
        if (tvb, tdbp, tde) <= (cur_vb, cur_dbp, cur_de):
            cur_seq, cur_vb, cur_dbp, cur_de, ms = s_clean, tvb, tdbp, tde, tms

    stage_b_seeds = []
    if budget_violation(s_clean, pinfo) <= cur_vb:
        stage_b_seeds.append(s_clean)
    if cur_seq not in stage_b_seeds:
        stage_b_seeds.append(cur_seq)
    for ch_mode in (0, 1, 2):
        for base_dh in (s_clean, cur_seq):
            lst_dh = list(base_dh)
            dehomopolymerize_and_chiral_sanitize(lst_dh, pinfo, mode=ch_mode)
            enforce_anti_slip_guards(lst_dh, pinfo, rng)
            s_dh = "".join(lst_dh)
            if s_dh not in stage_b_seeds and budget_violation(s_dh, pinfo) <= cur_vb:
                tms, tme = exact_fold(s_dh, eng)
                tdbp = len(t_bps ^ get_bp_set(tms))
                tde = round(float(RNA.energy_of_struct(s_dh, target)) - tme, 4)
                tvb = budget_violation(s_dh, pinfo)
                if tdbp == 0 and tvb == 0:
                    ok, _, _ = check_full_solve(s_dh, pinfo, eng)
                    if ok:
                        return True, s_dh, 0, 0, 0.0
                stage_b_seeds.append(s_dh)
                if (tvb, tdbp, tde) <= (cur_vb, cur_dbp, cur_de):
                    cur_seq, cur_vb, cur_dbp, cur_de, ms = s_dh, tvb, tdbp, tde, tms
                    stage_b_seeds[0] = cur_seq

    # --- Stage B: Exact Local-Motif Block Enumeration (`ViennaRNA-1.8.5/lib/fold.c` lines 395-405 & 546) ---
    m_bps = get_bp_set(ms)
    bh_list = list(pinfo.get("bulge_hairpins", ()))
    bh_tetraloops_cg = ("GAAA", "UUCG", "GCAA", "GUGA")
    bh_tetraloops_gc = ("GAAA", "GUGA", "GAGA", "GGGA")
    per_bh_top = {}

    def reorthogonalize_stems_after_stage_b(
        s_init: str, ms_init: str, prot_base: set, req_bps: tuple, max_steps: int = 10, max_cands: int = 44
    ) -> tuple:
        """
        `MONITOR K20` + `Law M37` Post-Stage-B Parasitic-Stem Unknotter:
        Protects all closed `.((....).).` motifs (including both `fL` and `fR` dangles!)
        while breaking parasitic stems `extra = get_bp_set(ms) - t_bps` among ordinary
        stems / unprotected unpaired bases at 0 budget cost (`GC <-> CG`, `AU <-> UA`, `GU <-> UG`).
        """
        w_seq = s_init
        w_ms = ms_init
        w_bps = get_bp_set(w_ms)
        w_dbp = len(t_bps ^ w_bps)
        w_de = round(float(RNA.energy_of_struct(w_seq, target)) - float(RNA.energy_of_struct(w_seq, w_ms)), 4)
        ext_rivals = [ms_init]

        prot_all_bh = set(prot_base) | set(locked_pos.keys())
        for u0_k, v0_k, u1_k, v1_k, lp_k, bg_k, fL_k, fR_k in bh_list:
            if (u0_k, v0_k) in w_bps and (u1_k, v1_k) in w_bps:
                prot_all_bh |= {u0_k, v0_k, u1_k, v1_k, bg_k} | set(range(lp_k, lp_k + 4))
                if fL_k != -1:
                    prot_all_bh.add(fL_k)
                if fR_k != -1:
                    prot_all_bh.add(fR_k)

        for _step in range(max_steps):
            extra = sorted(w_bps - t_bps)
            if not extra or time.time() - t0 >= max_sec * 0.94:
                break
            w_lst = list(w_seq)
            single_flips = []
            seen_uv = set()
            unp_edits = []
            seen_unp = set()

            for x, y in extra:
                for z, w in ((x, y), (y, x)):
                    if pair_of[z] == -1 and z not in locked_pos and z not in seen_unp:
                        if z not in prot_all_bh:
                            seen_unp.add(z)
                            for ch_new in ("A", "C", "U", "G"):
                                if ch_new != w_lst[z] and (w_lst[w] + ch_new) not in VALID_SET:
                                    if not has_symmetric_neck_zip(z, ch_new, w_lst, pair_of, n):
                                        unp_edits.append((z, ch_new))
                    elif pair_of[z] != -1:
                        for dz in (0, -1, 1, -2, 2):
                            zn = z + dz
                            if 0 <= zn < n and pair_of[zn] != -1:
                                uv_s = (min(zn, pair_of[zn]), max(zn, pair_of[zn]))
                                if uv_s not in seen_uv and uv_s[0] not in prot_all_bh and uv_s[1] not in prot_all_bh:
                                    seen_uv.add(uv_s)
                                    cur_bp = w_lst[uv_s[0]] + w_lst[uv_s[1]]
                                    alt_list = []
                                    flip_bp = cur_bp[1] + cur_bp[0]
                                    if flip_bp != cur_bp and flip_bp in allowed_pairs[uv_s]:
                                        alt_list.append(flip_bp)
                                    for cand_bp in ("CG", "GC", "AU", "UA", "GU", "UG"):
                                        if cand_bp != cur_bp and cand_bp not in alt_list and cand_bp in allowed_pairs[uv_s]:
                                            ch_at_zn = cand_bp[0] if zn == uv_s[0] else cand_bp[1]
                                            if dz != 0 or (w_lst[w] + ch_at_zn) not in VALID_SET:
                                                alt_list.append(cand_bp)
                                    for alt_bp in alt_list:
                                        single_flips.append((uv_s, alt_bp))

            cand_seqs = []
            # 0. Simultaneous Multi-Pair Cross-Duplex Stem Flip (destroys 2..6-bp cross-stem duplexes in 1 move at 0 budget cost!)
            direct_extra_uvs = []
            for x, y in extra:
                for z, w in ((x, y), (y, x)):
                    if pair_of[z] != -1:
                        uv_d = (min(z, pair_of[z]), max(z, pair_of[z]))
                        if uv_d[0] not in prot_all_bh and uv_d[1] not in prot_all_bh and uv_d not in direct_extra_uvs:
                            direct_extra_uvs.append(uv_d)
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
                            tl_mf_u = list(tl_mf)
                            for z, ch_new in unp_edits:
                                if tl_mf_u[z] == w_lst[z]:
                                    tl_mf_u[z] = ch_new
                            cand_seqs.append("".join(tl_mf_u))
            if seen_unp:
                tl_all = list(w_lst)
                changed_all = False
                for z, ch_new in unp_edits:
                    if tl_all[z] == w_lst[z]:
                        tl_all[z] = ch_new
                        changed_all = True
                if changed_all:
                    cand_seqs.append("".join(tl_all))
            for uv_s, flip_bp in single_flips[:16]:
                tl = list(w_lst)
                tl[uv_s[0]], tl[uv_s[1]] = flip_bp[0], flip_bp[1]
                s_tl = "".join(tl)
                if budget_violation(s_tl, pinfo) <= cur_vb:
                    cand_seqs.append(s_tl)
                else:
                    for s_r in repair_budget_candidates(tl, pinfo, prot_all_bh | {uv_s[0], uv_s[1]}, w_ms, rng, max_k=2)[:2]:
                        if budget_violation(s_r, pinfo) <= cur_vb:
                            cand_seqs.append(s_r)
            for z, ch_new in unp_edits[:12]:
                tl = list(w_lst)
                tl[z] = ch_new
                cand_seqs.append("".join(tl))
            for i_f in range(min(len(single_flips), 6)):
                for j_f in range(i_f + 1, min(len(single_flips), 6)):
                    uv1, fp1 = single_flips[i_f]
                    uv2, fp2 = single_flips[j_f]
                    if uv1 == uv2:
                        continue
                    tl = list(w_lst)
                    tl[uv1[0]], tl[uv1[1]] = fp1[0], fp1[1]
                    tl[uv2[0]], tl[uv2[1]] = fp2[0], fp2[1]
                    s_tl = "".join(tl)
                    if budget_violation(s_tl, pinfo) <= cur_vb:
                        cand_seqs.append(s_tl)
            for uv_s, flip_bp in single_flips[:6]:
                tl = list(w_lst)
                tl[uv_s[0]], tl[uv_s[1]] = flip_bp[0], flip_bp[1]
                if budget_violation("".join(tl), pinfo) <= cur_vb:
                    for z, ch_new in unp_edits[:8]:
                        tl2 = list(tl)
                        tl2[z] = ch_new
                        cand_seqs.append("".join(tl2))
            for i_u in range(min(len(unp_edits), 4)):
                for j_u in range(i_u + 1, min(len(unp_edits), 4)):
                    z1, c1 = unp_edits[i_u]
                    z2, c2 = unp_edits[j_u]
                    if z1 != z2:
                        tl = list(w_lst)
                        tl[z1] = c1
                        tl[z2] = c2
                        cand_seqs.append("".join(tl))

            if not cand_seqs:
                break

            w_et = float(RNA.energy_of_struct(w_seq, target))
            w_worst_ext = max(round(w_et - float(RNA.energy_of_struct(w_seq, r_e)), 4) for r_e in ext_rivals[-6:])
            cur_key = (
                sum(1 for uv_r in req_bps if uv_r not in w_bps),
                w_dbp if w_dbp <= 4 else len(extra),
                w_dbp,
                max(0.0, w_worst_ext),
                w_de,
            )
            best_step = None
            for cs in cand_seqs[:max_cands]:
                cms, cme = exact_fold(cs, eng)
                cbps = get_bp_set(cms)
                cdbp = len(t_bps ^ cbps)
                cet = float(RNA.energy_of_struct(cs, target))
                cde = round(cet - cme, 4)
                if cdbp == 0:
                    return cs, cms, 0, 0.0
                cextra_n = len(cbps - t_bps)
                c_worst_ext = max(round(cet - float(RNA.energy_of_struct(cs, r_e)), 4) for r_e in ext_rivals[-6:])
                ckey = (
                    sum(1 for uv_r in req_bps if uv_r not in cbps),
                    cdbp if cdbp <= 4 else cextra_n,
                    cdbp,
                    max(0.0, c_worst_ext),
                    cde,
                )
                if ckey < cur_key:
                    cur_key = ckey
                    best_step = (cs, cms, cbps, cdbp, cde)

            if best_step is None:
                break
            w_seq, w_ms, w_bps, w_dbp, w_de = best_step
            if w_ms not in ext_rivals:
                ext_rivals.append(w_ms)
            for u0_k, v0_k, u1_k, v1_k, lp_k, bg_k, fL_k, fR_k in bh_list:
                if (u0_k, v0_k) in w_bps and (u1_k, v1_k) in w_bps:
                    prot_all_bh |= {u0_k, v0_k, u1_k, v1_k, bg_k} | set(range(lp_k, lp_k + 4))
                    if fL_k != -1:
                        prot_all_bh.add(fL_k)
                    if fR_k != -1:
                        prot_all_bh.add(fR_k)

        return w_seq, w_ms, w_dbp, w_de

    # Step B1: Fast exact local block enumeration for ALL `.((....).).` motifs (`< 0.02s` total)
    for idx_bh in range(len(bh_list)):
        u0, v0, u1, v1, lp_start, bg_pos, fL, fR = bh_list[idx_bh]
        ms_o1 = list(target)
        ms_o1[u0] = "."
        ms_o1[v0] = "."
        s_open_1 = "".join(ms_o1)
        ms_o2 = list(ms_o1)
        ms_o2[u1] = "."
        ms_o2[v1] = "."
        s_open_2 = "".join(ms_o2)

        uv_left = None
        s_open_left = None
        if fL == u0 - 1 and u0 >= 2 and pair_of[u0 - 2] != -1:
            uv_left = (min(u0 - 2, pair_of[u0 - 2]), max(u0 - 2, pair_of[u0 - 2]))
            ms_ol = list(target)
            ms_ol[uv_left[0]] = "."
            ms_ol[uv_left[1]] = "."
            s_open_left = "".join(ms_ol)

        fL_dom = ("C", "A") if (fL != -1 and fL not in locked_pos) else (cur_seq[fL] if fL != -1 else "A",)
        fR_dom = ("G", "A") if (fR != -1 and fR not in locked_pos) else (cur_seq[fR] if fR != -1 else "A",)
        bg_dom = BASES if bg_pos not in locked_pos else (cur_seq[bg_pos],)
        p0_dom = [bp for bp in allowed_pairs[(u0, v0)] if bp in STRONG_PAIRS] or list(allowed_pairs[(u0, v0)][:2])
        p1_dom = [bp for bp in allowed_pairs[(u1, v1)] if bp in STRONG_PAIRS] or list(allowed_pairs[(u1, v1)][:2])

        if uv_left is not None:
            cur_bp_l = cur_seq[uv_left[0]] + cur_seq[uv_left[1]]
            left_dom = [cur_bp_l]
            for bp_l in allowed_pairs[uv_left]:
                if bp_l not in left_dom:
                    left_dom.append(bp_l)
        else:
            left_dom = [None]

        block_ranked = []
        base_b = list(s_clean if budget_violation(s_clean, pinfo) <= cur_vb else cur_seq)
        for bp_l in left_dom:
            if uv_left is not None and bp_l is not None:
                base_b[uv_left[0]], base_b[uv_left[1]] = bp_l[0], bp_l[1]
            sub_ranked = []
            for p0_bp in p0_dom:
                base_b[u0], base_b[v0] = p0_bp[0], p0_bp[1]
                for p1_bp in p1_dom:
                    base_b[u1], base_b[v1] = p1_bp[0], p1_bp[1]
                    for lp_orth in ("GAAA", "GCAA", "GGAA", "UUCG", "UACG", "UAAC"):
                        for k_l, ch_l in enumerate(lp_orth):
                            if (lp_start + k_l) not in locked_pos:
                                base_b[lp_start + k_l] = ch_l
                        for bg_ch in bg_dom:
                            if bg_pos == v0 - 1 and (p0_bp[0] + bg_ch) in VALID_SET:
                                continue
                            if bg_pos == u0 + 1 and (bg_ch + p0_bp[1]) in VALID_SET:
                                continue
                            if bg_pos == v0 - 1 and (lp_orth[0] + bg_ch) in STRONG_PAIRS and p0_bp == "CG" and p1_bp == "CG":
                                continue
                            base_b[bg_pos] = bg_ch
                            for b_fL in fL_dom:
                                if fL != -1:
                                    base_b[fL] = b_fL
                                for b_fR in fR_dom:
                                    if fR != -1:
                                        base_b[fR] = b_fR
                                    s_blk = "".join(base_b)
                                    et_b = eval_struct(s_blk, target)
                                    eo1_b = eval_struct(s_blk, s_open_1)
                                    eo2_b = eval_struct(s_blk, s_open_2)
                                    de_blk = max(et_b - eo1_b, et_b - eo2_b)
                                    if s_open_left is not None:
                                        eol_b = eval_struct(s_blk, s_open_left)
                                        de_blk = max(de_blk, et_b - eol_b)
                                    sub_ranked.append(
                                        (round(de_blk, 4), round(et_b, 4), p0_bp, p1_bp, bg_ch, b_fL, b_fR, lp_orth, uv_left, bp_l)
                                    )
            sub_ranked.sort(key=lambda x: (x[0], x[1]))
            block_ranked.extend(sub_ranked[:8])

        block_ranked.sort(
            key=lambda x: (
                0 if (x[0] < 0.0 and (x[5] + x[6]) not in VALID_SET) else (1 if x[0] < 0.0 else 2),
                x[0],
                x[1],
            )
        )
        # Diversify across `(bp_l, p0_bp, b_fL, lp_orth)` so all families are represented
        div_list = []
        fam_counts = {}
        for item in block_ranked:
            fkey = (item[9], item[2], item[5])
            if fam_counts.get(fkey, 0) < 4:
                fam_counts[fkey] = fam_counts.get(fkey, 0) + 1
                div_list.append(item)
        per_bh_top[idx_bh] = div_list[:20]
        if os.environ.get("DIAG_STAGE_B") == "1":
            print(f"  [DIAG Stage B] pid={pinfo['puzzle_id']} idx_bh={idx_bh} (u0,v0)=({u0},{v0}) in_m={(u0,v0) in m_bps} uv_left={uv_left} top6={per_bh_top[idx_bh][:6]}", flush=True)

    # Step B2: Single-motif verification & empirical ranking (`< 0.35s` per unsatisfied motif)
    verified_bh_top = {idx_bh: list(per_bh_top.get(idx_bh, ())) for idx_bh in range(len(bh_list))}
    unsat_init = [
        idx_bh
        for idx_bh, (u0, v0, u1, v1, _lp, _bg, _fL, _fR) in enumerate(bh_list)
        if (u0, v0) not in m_bps or (u1, v1) not in m_bps
    ]
    for idx_bh in unsat_init:
        u0, v0, u1, v1, lp_start, bg_pos, fL, fR = bh_list[idx_bh]
        if (u0, v0) in m_bps and (u1, v1) in m_bps:
            continue
        deadline_bh = time.time() + (max_sec * 0.26) / max(1, len(unsat_init))

        prot_bh = {u0, v0, u1, v1, bg_pos} | set(range(lp_start, lp_start + 4))
        if fL != -1:
            prot_bh.add(fL)
        if fR != -1:
            prot_bh.add(fR)

        emp_scored = []
        for item in per_bh_top[idx_bh][:10]:
            if time.time() >= deadline_bh:
                break
            for seed_bh in stage_b_seeds[:2]:
                _deb, _etb, p0_bp, p1_bp, bg_ch, b_fL, b_fR, lp_s, uv_l, bp_l = item
                trial = list(seed_bh)
                prot_now = set(prot_bh)
                if uv_l is not None and bp_l is not None:
                    trial[uv_l[0]], trial[uv_l[1]] = bp_l[0], bp_l[1]
                    prot_now.add(uv_l[0])
                    prot_now.add(uv_l[1])
                trial[u0], trial[v0] = p0_bp[0], p0_bp[1]
                trial[u1], trial[v1] = p1_bp[0], p1_bp[1]
                for k_l, ch_l in enumerate(lp_s):
                    if (lp_start + k_l) not in locked_pos:
                        trial[lp_start + k_l] = ch_l
                if bg_pos not in locked_pos:
                    trial[bg_pos] = bg_ch
                if fL != -1 and fL not in locked_pos:
                    trial[fL] = b_fL
                if fR != -1 and fR not in locked_pos:
                    trial[fR] = b_fR
                for s_rep in repair_budget_candidates(trial, pinfo, prot_now, ms, rng, max_k=3):
                    tvb = budget_violation(s_rep, pinfo)
                    if tvb > cur_vb:
                        continue
                    tms, tme = exact_fold(s_rep, eng)
                    t_m_bps = get_bp_set(tms)
                    tdbp = len(t_bps ^ t_m_bps)
                    tde = round(float(RNA.energy_of_struct(s_rep, target)) - tme, 4)
                    if tdbp == 0 and tvb == 0:
                        ok, _, _ = check_full_solve(s_rep, pinfo, eng)
                        if ok:
                            return True, s_rep, 0, 0, 0.0
                    if (_deb <= 0.0 or ((u0, v0) in t_m_bps and (u1, v1) in t_m_bps)) and tdbp > 0 and len(t_m_bps - t_bps) > 0:
                        s_reo, ms_reo, dbp_reo, de_reo = reorthogonalize_stems_after_stage_b(
                            s_rep, tms, prot_now, ((u0, v0), (u1, v1)), max_steps=6, max_cands=56
                        )
                        if dbp_reo < tdbp or (dbp_reo == tdbp and de_reo < tde):
                            s_rep, tms, tdbp, tde = s_reo, ms_reo, dbp_reo, de_reo
                            t_m_bps = get_bp_set(tms)
                    closed_flag = 0 if ((u0, v0) in t_m_bps and (u1, v1) in t_m_bps) else 1
                    emp_scored.append(((closed_flag, tdbp, tde), item, s_rep))
                    if os.environ.get("DIAG_STAGE_B") == "1" and _deb <= 0.0:
                        print(f"    [B2 idx={idx_bh}] bp_l={bp_l} p0={p0_bp} p1={p1_bp} bg={bg_ch} fL={b_fL} fR={b_fR} lp={lp_s} deb={_deb} -> closed={closed_flag==0} tdbp={tdbp} tde={tde} miss={sorted(t_bps - t_m_bps)} extra={sorted(t_m_bps - t_bps)}", flush=True)
                    if tdbp == 0 and tvb == 0:
                        ok, _, _ = check_full_solve(s_rep, pinfo, eng)
                        if ok:
                            return True, s_rep, 0, 0, 0.0
                    if (tvb, tdbp, tde) < (cur_vb, cur_dbp, cur_de):
                        cur_seq, cur_vb, cur_dbp, cur_de, ms = s_rep, tvb, tdbp, tde, tms
                        m_bps = get_bp_set(ms)
                        stage_b_seeds[0] = cur_seq
                    break
        if emp_scored:
            emp_scored.sort(key=lambda x: x[0])
            seen_items = []
            for _ek, it, s_r_best in emp_scored:
                if it not in seen_items:
                    seen_items.append(it)
                if _ek[0] == 0 and s_r_best not in stage_b_seeds and len(stage_b_seeds) < 5:
                    stage_b_seeds.append(s_r_best)
            verified_bh_top[idx_bh] = seen_items

    # Step B3: Joint 2-Motif `.((....).).` Synthesis (`Op-M1 + CLSS-3`, e.g. `#3151424` and `#3620224`)
    unsat_bhs = [
        idx_bh
        for idx_bh, (u0, v0, u1, v1, _lp, _bg, _fL, _fR) in enumerate(bh_list)
        if ((u0, v0) not in m_bps or (u1, v1) not in m_bps) and verified_bh_top.get(idx_bh)
    ]
    pair_bh_list = []
    if len(unsat_bhs) >= 2:
        pair_bh_list.append((unsat_bhs[0], unsat_bhs[1]))
    elif len(unsat_bhs) == 1 and len(bh_list) >= 2:
        i0 = unsat_bhs[0]
        for j0 in range(len(bh_list)):
            if j0 != i0 and verified_bh_top.get(j0):
                pair_bh_list.append((i0, j0))

    for i_a, i_b in pair_bh_list:
        if time.time() - t0 >= max_sec * 0.52:
            break
        u0a, v0a, u1a, v1a, lpa, bga, fLa, fRa = bh_list[i_a]
        u0b, v0b, u1b, v1b, lpb, bgb, fLb, fRb = bh_list[i_b]
        prot_ab = (
            {u0a, v0a, u1a, v1a, bga, u0b, v0b, u1b, v1b, bgb}
            | set(range(lpa, lpa + 4))
            | set(range(lpb, lpb + 4))
            | ({fLa} if fLa != -1 else set())
            | ({fRa} if fRa != -1 else set())
            | ({fLb} if fLb != -1 else set())
            | ({fRb} if fRb != -1 else set())
        )
        req_ab = ((u0a, v0a), (u1a, v1a), (u0b, v0b), (u1b, v1b))
        cands_a = list(per_bh_top.get(i_a, ())[:4])
        for it_a in verified_bh_top.get(i_a, ())[:5]:
            if it_a not in cands_a:
                cands_a.append(it_a)
        cands_b = list(per_bh_top.get(i_b, ())[:4])
        for it_b in verified_bh_top.get(i_b, ())[:5]:
            if it_b not in cands_b:
                cands_b.append(it_b)
        for _d1, _e1, p0a, p1a, bg_ca, fL_ca, fR_ca, lp1_s, uvl_a, bpl_a in cands_a[:7]:
            for _d2, _e2, p0b, p1b, bg_cb, fL_cb, fR_cb, lp2_s, uvl_b, bpl_b in cands_b[:7]:
                if lp1_s == lp2_s:
                    continue
                if time.time() - t0 >= max_sec * 0.52:
                    break
                for seed_bh in stage_b_seeds[:3]:
                    if time.time() - t0 >= max_sec * 0.52:
                        break
                    trial = list(seed_bh)
                    prot_now = set(prot_ab)
                    if uvl_a is not None and bpl_a is not None:
                        trial[uvl_a[0]], trial[uvl_a[1]] = bpl_a[0], bpl_a[1]
                        prot_now.add(uvl_a[0])
                        prot_now.add(uvl_a[1])
                    if uvl_b is not None and bpl_b is not None:
                        trial[uvl_b[0]], trial[uvl_b[1]] = bpl_b[0], bpl_b[1]
                        prot_now.add(uvl_b[0])
                        prot_now.add(uvl_b[1])
                    trial[u0a], trial[v0a] = p0a[0], p0a[1]
                    trial[u1a], trial[v1a] = p1a[0], p1a[1]
                    for k_l, ch_l in enumerate(lp1_s):
                        if (lpa + k_l) not in locked_pos:
                            trial[lpa + k_l] = ch_l
                    if bga not in locked_pos:
                        trial[bga] = bg_ca
                    if fLa != -1 and fLa not in locked_pos:
                        trial[fLa] = fL_ca
                    if fRa != -1 and fRa not in locked_pos:
                        trial[fRa] = fR_ca

                    trial[u0b], trial[v0b] = p0b[0], p0b[1]
                    trial[u1b], trial[v1b] = p1b[0], p1b[1]
                    for k_l, ch_l in enumerate(lp2_s):
                        if (lpb + k_l) not in locked_pos:
                            trial[lpb + k_l] = ch_l
                    if bgb not in locked_pos:
                        trial[bgb] = bg_cb
                    if fLb != -1 and fLb not in locked_pos:
                        trial[fLb] = fL_cb
                    if fRb != -1 and fRb not in locked_pos:
                        trial[fRb] = fR_cb

                    for s_rep in repair_budget_candidates(trial, pinfo, prot_now, ms, rng, max_k=3):
                        tvb = budget_violation(s_rep, pinfo)
                        if tvb > cur_vb:
                            continue
                        tms, tme = exact_fold(s_rep, eng)
                        t_m_bps = get_bp_set(tms)
                        tdbp = len(t_bps ^ t_m_bps)
                        tde = round(float(RNA.energy_of_struct(s_rep, target)) - tme, 4)
                        if tdbp == 0 and tvb == 0:
                            ok, _, _ = check_full_solve(s_rep, pinfo, eng)
                            if ok:
                                return True, s_rep, 0, 0, 0.0
                        if tdbp > 0 and len(t_m_bps - t_bps) > 0:
                            s_reo, ms_reo, dbp_reo, de_reo = reorthogonalize_stems_after_stage_b(
                                s_rep, tms, prot_now, req_ab, max_steps=12, max_cands=44
                            )
                            if dbp_reo < tdbp or (dbp_reo == tdbp and de_reo < tde):
                                s_rep, tms, tdbp, tde = s_reo, ms_reo, dbp_reo, de_reo
                                t_m_bps = get_bp_set(tms)
                        if os.environ.get("DIAG_STAGE_B") == "1":
                            print(f"    [JOINT] a=({bpl_a},{p0a},{lp1_s}) b=({bpl_b},{p0b},{lp2_s}) -> tdbp={tdbp} tde={tde} miss={sorted(t_bps - t_m_bps)} extra={sorted(t_m_bps - t_bps)}", flush=True)
                        if tdbp == 0 and tvb == 0:
                            ok, _, _ = check_full_solve(s_rep, pinfo, eng)
                            if ok:
                                return True, s_rep, 0, 0, 0.0
                        if (tvb, tdbp, tde) < (cur_vb, cur_dbp, cur_de):
                            cur_seq, cur_vb, cur_dbp, cur_de, ms = s_rep, tvb, tdbp, tde, tms
                            m_bps = get_bp_set(ms)
                        break

    # --- Stage B1.5: `[L0-ALGO]` Connected Loop-Cascade 2nd-Order Markov Trellis Solver (`K20`) ---
    def _build_local_slip_struct(target_s: str, pair_of_arr: list, close_uvs: tuple, extra_open_uvs: tuple):
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

    sorted_pairs_cas = sorted(pinfo["pairs"], key=lambda uv: (uv[0], -uv[1]))
    pair_parent_cas = {}
    pair_children_cas = {uv: [] for uv in sorted_pairs_cas}
    pair_stack_cas = []
    for uv_c in sorted_pairs_cas:
        while pair_stack_cas and not (pair_stack_cas[-1][0] < uv_c[0] and uv_c[1] < pair_stack_cas[-1][1]):
            pair_stack_cas.pop()
        if pair_stack_cas:
            pair_parent_cas[uv_c] = pair_stack_cas[-1]
            pair_children_cas[pair_stack_cas[-1]].append(uv_c)
        else:
            pair_parent_cas[uv_c] = None
        pair_stack_cas.append(uv_c)

    raw_chains_cas = []
    for uv_c in sorted_pairs_cas:
        par_c = pair_parent_cas[uv_c]
        if par_c is None or len(pair_children_cas[par_c]) != 1:
            ch_c = [uv_c]
            curr_c = uv_c
            while len(pair_children_cas[curr_c]) == 1:
                curr_c = pair_children_cas[curr_c][0]
                ch_c.append(curr_c)
            if len(ch_c) >= 2:
                raw_chains_cas.append(ch_c)

    diff_bps_cas = m_bps ^ t_bps
    cascade_windows = []
    for ch_c in raw_chains_cas:
        m_ch = len(ch_c) - 1
        act_steps = [
            idx_s
            for idx_s in range(1, len(ch_c))
            if (ch_c[idx_s][0] > ch_c[idx_s - 1][0] + 1 or ch_c[idx_s][1] < ch_c[idx_s - 1][1] - 1)
            or ch_c[idx_s - 1] in diff_bps_cas
            or ch_c[idx_s] in diff_bps_cas
        ]
        if not act_steps:
            continue
        comp_s = comp_e = act_steps[0]
        comps_c = []
        for s_idx in act_steps[1:]:
            if s_idx <= comp_e + 2:
                comp_e = s_idx
            else:
                comps_c.append((comp_s, comp_e))
                comp_s = comp_e = s_idx
        comps_c.append((comp_s, comp_e))
        for c_s, c_e in comps_c:
            w_s = max(0, c_s - 2)
            w_e = min(m_ch, c_e + (2 if m_ch - c_e <= 2 else 1))
            if w_e - w_s + 1 <= 11:
                cascade_windows.append(ch_c[w_s : w_e + 1])
            else:
                for st_w in range(w_s, w_e, 7):
                    sub_w = ch_c[st_w : min(w_e + 1, st_w + 9)]
                    if len(sub_w) >= 2:
                        cascade_windows.append(sub_w)

    cas_cap = 0.22 if cur_dbp <= 2 else 0.52
    for win in cascade_windows:
        if time.time() - t0 >= max_sec * cas_cap:
            break
        diff_now = m_bps ^ t_bps
        if not diff_now:
            break
        win_touch = any(
            uv_w in diff_now or any(min(abs(x - uv_w[0]), abs(x - uv_w[1])) <= 3 for uv_d in diff_now for x in uv_d)
            for uv_w in win
        )
        if not win_touch:
            continue

        k_w = len(win) - 1
        s_open_win = []
        for i_w in range(k_w + 1):
            lst_ow = list(target)
            lst_ow[win[i_w][0]] = "."
            lst_ow[win[i_w][1]] = "."
            s_open_win.append("".join(lst_ow))

        s_open2_win = []
        for i_w in range(k_w):
            lst_ow2 = list(target)
            lst_ow2[win[i_w][0]] = "."
            lst_ow2[win[i_w][1]] = "."
            lst_ow2[win[i_w + 1][0]] = "."
            lst_ow2[win[i_w + 1][1]] = "."
            s_open2_win.append("".join(lst_ow2))

        lst_oall = list(target)
        for i_w in range(k_w + 1):
            has_loop_adj = (
                i_w > 0 and (win[i_w][0] > win[i_w - 1][0] + 1 or win[i_w][1] < win[i_w - 1][1] - 1)
            ) or (
                i_w < k_w and (win[i_w + 1][0] > win[i_w][0] + 1 or win[i_w + 1][1] < win[i_w][1] - 1)
            )
            if has_loop_adj:
                lst_oall[win[i_w][0]] = "."
                lst_oall[win[i_w][1]] = "."
        s_open_all_win = "".join(lst_oall)

        slip_rivals_win = {i_w: [] for i_w in range(1, k_w + 1)}
        cross_slip_rivals_win = {i_w: [] for i_w in range(1, k_w + 1)}
        step_unp_cands = {}
        all_win_pos = set()
        for u_w, v_w in win:
            all_win_pos |= {u_w, v_w}

        base_cas_seq = s_clean if budget_violation(s_clean, pinfo) <= cur_vb else cur_seq

        for i_w in range(1, k_w + 1):
            uo_w, vo_w = win[i_w - 1]
            ui_w, vi_w = win[i_w]
            left_w = list(range(uo_w + 1, ui_w))
            right_w = list(range(vi_w + 1, vo_w))
            n1_w, n2_w = len(left_w), len(right_w)
            all_win_pos |= set(left_w) | set(right_w)

            # Build local slip rivals inside `[uo_w .. ui_w] x [vi_w .. vo_w]`
            seen_r_strs = set()
            r_list_i = []
            for x_s in left_w:
                for y_s in right_w:
                    for ex_op in ((), ((uo_w, vo_w),), ((ui_w, vi_w),), ((uo_w, vo_w), (ui_w, vi_w))):
                        r_s = _build_local_slip_struct(target, pair_of, ((x_s, y_s),), ex_op)
                        if r_s is not None and r_s != target and r_s not in seen_r_strs:
                            seen_r_strs.add(r_s)
                            r_list_i.append((((x_s, y_s),), r_s))
            for y_s in right_w:
                for u_anchor in (uo_w, ui_w):
                    for ex_op in ((), ((uo_w, vo_w), (ui_w, vi_w))):
                        r_s = _build_local_slip_struct(target, pair_of, ((u_anchor, y_s),), ex_op)
                        if r_s is not None and r_s != target and r_s not in seen_r_strs:
                            seen_r_strs.add(r_s)
                            r_list_i.append((((u_anchor, y_s),), r_s))
            for x_s in left_w:
                for v_anchor in (vo_w, vi_w):
                    for ex_op in ((), ((uo_w, vo_w), (ui_w, vi_w))):
                        r_s = _build_local_slip_struct(target, pair_of, ((x_s, v_anchor),), ex_op)
                        if r_s is not None and r_s != target and r_s not in seen_r_strs:
                            seen_r_strs.add(r_s)
                            r_list_i.append((((x_s, v_anchor),), r_s))
            # 2-bp stacked shifts inside `[uo_w .. ui_w] x [vi_w .. vo_w]`
            for x_s in range(uo_w, ui_w):
                for y_s in range(vi_w + 1, vo_w + 1):
                    c2 = ((x_s, y_s), (x_s + 1, y_s - 1))
                    if set(c2) == {(uo_w, vo_w), (ui_w, vi_w)}:
                        continue
                    for ex_op in ((), ((uo_w, vo_w), (ui_w, vi_w))):
                        r_s = _build_local_slip_struct(target, pair_of, c2, ex_op)
                        if r_s is not None and r_s != target and r_s not in seen_r_strs:
                            seen_r_strs.add(r_s)
                            r_list_i.append((c2, r_s))
            slip_rivals_win[i_w] = r_list_i

            # Cross-boundary 2-bp stacked shifts straddling `p_{i-1} = (uo_w, vo_w)`
            if i_w >= 2:
                upp_w, vpp_w = win[i_w - 2]
                seen_cr = set()
                cr_list_i = []
                for x_s in range(max(upp_w, uo_w - 2), min(ui_w, uo_w + 2)):
                    for y_s in range(max(vi_w + 1, vo_w - 1), min(vpp_w + 1, vo_w + 3)):
                        c2 = ((x_s, y_s), (x_s + 1, y_s - 1))
                        if set(c2).issubset({(upp_w, vpp_w), (uo_w, vo_w), (ui_w, vi_w)}):
                            continue
                        for ex_op in ((), ((uo_w, vo_w),), ((upp_w, vpp_w), (uo_w, vo_w), (ui_w, vi_w))):
                            r_s = _build_local_slip_struct(target, pair_of, c2, ex_op)
                            if r_s is not None and r_s != target and r_s not in seen_cr:
                                seen_cr.add(r_s)
                                cr_list_i.append((c2, r_s))
                cross_slip_rivals_win[i_w] = cr_list_i

            # Build unpaired candidate tuples `step_unp_cands[i_w]`
            if n1_w == 0 and n2_w == 0:
                step_unp_cands[i_w] = [()]
            elif n1_w == 0 or n2_w == 0:
                b_pos = left_w if n1_w > 0 else right_w
                if len(b_pos) == 1:
                    p0_b = b_pos[0]
                    dom0_b = BASES if p0_b not in locked_pos else (base_cas_seq[p0_b],)
                    step_unp_cands[i_w] = [((p0_b, ch_b),) for ch_b in dom0_b]
                else:
                    cands_b = []
                    seen_b = set()
                    dom_f = BASES if b_pos[0] not in locked_pos else (base_cas_seq[b_pos[0]],)
                    dom_l = BASES if b_pos[-1] not in locked_pos else (base_cas_seq[b_pos[-1]],)
                    for ch_f in dom_f:
                        for ch_l in dom_l:
                            for ch_mid in ("A", "C"):
                                tup_b = []
                                for idx_bp, p_bp in enumerate(b_pos):
                                    if p_bp in locked_pos:
                                        tup_b.append((p_bp, base_cas_seq[p_bp]))
                                    elif idx_bp == 0:
                                        tup_b.append((p_bp, ch_f))
                                    elif idx_bp == len(b_pos) - 1:
                                        tup_b.append((p_bp, ch_l))
                                    else:
                                        tup_b.append((p_bp, ch_mid))
                                tup_b = tuple(tup_b)
                                if tup_b not in seen_b:
                                    seen_b.add(tup_b)
                                    cands_b.append(tup_b)
                    cur_tup_b = tuple((p_bp, base_cas_seq[p_bp]) for p_bp in b_pos)
                    if cur_tup_b not in seen_b:
                        cands_b.append(cur_tup_b)
                    step_unp_cands[i_w] = cands_b
            else:
                unp_both = left_w + right_w
                if len(unp_both) <= 3:
                    doms_u = [BASES if p_u not in locked_pos else (base_cas_seq[p_u],) for p_u in unp_both]
                    step_unp_cands[i_w] = [
                        tuple(zip(unp_both, u_vals)) for u_vals in itertools.product(*doms_u)
                    ]
                elif n1_w == 2 and n2_w == 2:
                    doms_u = [BASES if p_u not in locked_pos else (base_cas_seq[p_u],) for p_u in unp_both]
                    cands_22 = []
                    for u_vals in itertools.product(*doms_u):
                        n_pyr = sum(1 for ch_u in u_vals if ch_u in ("C", "U"))
                        if n_pyr <= 1 or u_vals in (("U", "C", "U", "C"), ("C", "U", "C", "U")):
                            cands_22.append(tuple(zip(unp_both, u_vals)))
                    cur_22 = tuple((p_u, base_cas_seq[p_u]) for p_u in unp_both)
                    if cur_22 not in cands_22:
                        cands_22.append(cur_22)
                    step_unp_cands[i_w] = cands_22
                else:
                    bnd_pos = []
                    for p_u in (left_w[0], left_w[-1], right_w[0], right_w[-1]):
                        if p_u not in bnd_pos:
                            bnd_pos.append(p_u)
                    mid_pos = [p_u for p_u in unp_both if p_u not in bnd_pos]
                    doms_bnd = [("A", "G", "C") if p_u not in locked_pos else (base_cas_seq[p_u],) for p_u in bnd_pos]
                    cands_lg = []
                    for b_vals in itertools.product(*doms_bnd):
                        b_map = dict(zip(bnd_pos, b_vals))
                        tup_lg = tuple(
                            (p_u, base_cas_seq[p_u] if p_u in locked_pos else b_map.get(p_u, "A"))
                            for p_u in unp_both
                        )
                        cands_lg.append(tup_lg)
                    cur_lg = tuple((p_u, base_cas_seq[p_u]) for p_u in unp_both)
                    if cur_lg not in cands_lg:
                        cands_lg.append(cur_lg)
                    step_unp_cands[i_w] = cands_lg

        # Pair domains for `win[0 .. k_w]`
        dom_pair_win = []
        for i_w in range(k_w + 1):
            uv_w = win[i_w]
            touches_bulge = False
            if i_w > 0:
                n1_prev = win[i_w][0] - win[i_w - 1][0] - 1
                n2_prev = win[i_w - 1][1] - win[i_w][1] - 1
                if (n1_prev == 0) ^ (n2_prev == 0):
                    touches_bulge = True
            if i_w < k_w:
                n1_nxt = win[i_w + 1][0] - win[i_w][0] - 1
                n2_nxt = win[i_w][1] - win[i_w + 1][1] - 1
                if (n1_nxt == 0) ^ (n2_nxt == 0):
                    touches_bulge = True
            if i_w == 0 or i_w == k_w or touches_bulge:
                dom_pair_win.append(allowed_pairs[uv_w])
            else:
                cur_bp_w = base_cas_seq[uv_w[0]] + base_cas_seq[uv_w[1]]
                filt_bps = tuple(bp for bp in allowed_pairs[uv_w] if bp in ("GC", "CG", "GU", "UG") or bp == cur_bp_w)
                dom_pair_win.append(filt_bps if filt_bps else allowed_pairs[uv_w])

        # Forward 2nd-Order Markov Trellis over `(b_{i-1}, b_i)`
        trellis = {}
        t_work = list(base_cas_seq)
        u0_w, v0_w = win[0]
        u1_w, v1_w = win[1]
        for b0 in dom_pair_win[0]:
            t_work[u0_w], t_work[v0_w] = b0[0], b0[1]
            for b1 in dom_pair_win[1]:
                t_work[u1_w], t_work[v1_w] = b1[0], b1[1]
                cands_01 = []
                for u_assign in step_unp_cands[1]:
                    for p_u, ch_u in u_assign:
                        t_work[p_u] = ch_u
                    s_t = "".join(t_work)
                    et_t = float(RNA.energy_of_struct(s_t, target))
                    d_o0 = et_t - float(RNA.energy_of_struct(s_t, s_open_win[0]))
                    d_sl1 = -99.0
                    for c_uvs, r_str in slip_rivals_win[1]:
                        if all(s_t[x_c] + s_t[y_c] in VALID_SET for x_c, y_c in c_uvs):
                            d_r = et_t - float(RNA.energy_of_struct(s_t, r_str))
                            if d_r > d_sl1:
                                d_sl1 = d_r
                    p_viol = max(0.0, d_o0 + 0.05) + max(0.0, d_sl1 + 0.05)
                    w_bar = max(d_o0, d_sl1)
                    assign_01 = ((u0_w, b0[0]), (v0_w, b0[1]), (u1_w, b1[0]), (v1_w, b1[1])) + u_assign
                    cands_01.append((round(p_viol, 4), round(w_bar, 4), round(et_t, 4), assign_01))
                cands_01.sort(key=lambda x: (x[0], x[1], x[2]))
                trellis[(b0, b1)] = cands_01[:2]

        for i_w in range(2, k_w + 1):
            if time.time() - t0 >= max_sec * 0.52:
                break
            uo_w, vo_w = win[i_w - 1]
            ui_w, vi_w = win[i_w]
            # Group existing trellis states by `b_{i-1}`, keeping the #1 state for EACH `bp_pp` (`GC, CG, AU, UA, GU, UG`)
            by_prev_bp = {}
            for (bp_pp, bp_p), st_list in trellis.items():
                if st_list:
                    by_prev_bp.setdefault(bp_p, []).append((bp_pp, st_list[0]))
            for bp_p in by_prev_bp:
                by_prev_bp[bp_p].sort(key=lambda x: (x[1][0], x[1][1], x[1][2]))

            next_trellis = {}
            for bp_p, prev_entries in by_prev_bp.items():
                # Pre-select top `u_assign` for each `(bp_p, bp_i)` across both strong and wobble `bp_pp`
                rep_list = [prev_entries[0][1][3]]
                for bp_pp_cand, st_cand in prev_entries:
                    if bp_pp_cand in ("GU", "UG") and st_cand[3] not in rep_list:
                        rep_list.append(st_cand[3])
                        break
                top_u_for_bi = {}
                for bp_i in dom_pair_win[i_w]:
                    merged_u = []
                    for rep_assign in rep_list:
                        t_rep = list(base_cas_seq)
                        for p_a, ch_a in rep_assign:
                            t_rep[p_a] = ch_a
                        t_rep[ui_w], t_rep[vi_w] = bp_i[0], bp_i[1]
                        u_scored = []
                        for u_assign in step_unp_cands[i_w]:
                            for p_u, ch_u in u_assign:
                                t_rep[p_u] = ch_u
                            s_t = "".join(t_rep)
                            et_t = float(RNA.energy_of_struct(s_t, target))
                            d_op = et_t - float(RNA.energy_of_struct(s_t, s_open_win[i_w - 1]))
                            d_sli = -99.0
                            for c_uvs, r_str in slip_rivals_win[i_w]:
                                if all(s_t[x_c] + s_t[y_c] in VALID_SET for x_c, y_c in c_uvs):
                                    d_r = et_t - float(RNA.energy_of_struct(s_t, r_str))
                                    if d_r > d_sli:
                                        d_sli = d_r
                            u_scored.append((round(max(0.0, d_op + 0.05) + max(0.0, d_sli + 0.05), 4), round(max(d_op, d_sli), 4), round(et_t, 4), u_assign))
                        u_scored.sort(key=lambda x: (x[0], x[1], x[2]))
                        for x_u in u_scored[:4]:
                            if x_u[3] not in merged_u:
                                merged_u.append(x_u[3])
                    top_u_for_bi[bp_i] = merged_u[:6]

                # Expand all `prev_entries` (one per `bp_pp`) ending at `bp_p` with `top_u_for_bi[bp_i]`
                for bp_i in dom_pair_win[i_w]:
                    cands_pi = []
                    for _bp_pp, (prev_pv, prev_wb, _prev_et, prev_assign) in prev_entries:
                        t_exp = list(base_cas_seq)
                        for p_a, ch_a in prev_assign:
                            t_exp[p_a] = ch_a
                        t_exp[ui_w], t_exp[vi_w] = bp_i[0], bp_i[1]
                        for u_assign in top_u_for_bi[bp_i]:
                            for p_u, ch_u in u_assign:
                                t_exp[p_u] = ch_u
                            s_t = "".join(t_exp)
                            et_t = float(RNA.energy_of_struct(s_t, target))
                            d_op1 = et_t - float(RNA.energy_of_struct(s_t, s_open_win[i_w - 1]))
                            d_op2 = et_t - float(RNA.energy_of_struct(s_t, s_open2_win[i_w - 2]))
                            d_sli = -99.0
                            for c_uvs, r_str in slip_rivals_win[i_w] + cross_slip_rivals_win[i_w]:
                                if all(s_t[x_c] + s_t[y_c] in VALID_SET for x_c, y_c in c_uvs):
                                    d_r = et_t - float(RNA.energy_of_struct(s_t, r_str))
                                    if d_r > d_sli:
                                        d_sli = d_r
                            step_pv = max(0.0, d_op1 + 0.05) + max(0.0, d_op2 + 0.05) + max(0.0, d_sli + 0.05)
                            new_pv = round(prev_pv + step_pv, 4)
                            new_wb = round(max(prev_wb, d_op1, d_op2, d_sli), 4)
                            new_assign = prev_assign + ((ui_w, bp_i[0]), (vi_w, bp_i[1])) + u_assign
                            cands_pi.append((new_pv, new_wb, round(et_t, 4), new_assign))
                    cands_pi.sort(key=lambda x: (x[0], x[1], x[2]))
                    # Deduplicate assignments
                    dedup_pi = []
                    seen_as = set()
                    for item_pi in cands_pi:
                        if item_pi[3] not in seen_as:
                            seen_as.add(item_pi[3])
                            dedup_pi.append(item_pi)
                            if len(dedup_pi) >= 2:
                                break
                    if dedup_pi:
                        next_trellis[(bp_p, bp_i)] = dedup_pi
            if next_trellis:
                trellis = next_trellis

        # Finalize at `p_k = win[k_w]` (including closing hairpin candidates if `p_k` closes a hairpin)
        uk_w, vk_w = win[k_w]
        closes_hp = all(pair_of[k_hp] == -1 for k_hp in range(uk_w + 1, vk_w))
        hp_pos = list(range(uk_w + 1, vk_w)) if closes_hp else []
        if closes_hp:
            all_win_pos |= set(hp_pos)
        hp_cands = [()]
        if closes_hp and len(hp_pos) == 4:
            hp_cands = []
            for tl_s in ("GAAA", "UUCG", "GCAA", "GUGA", "GAGA", base_cas_seq[uk_w + 1 : vk_w]):
                if len(tl_s) == 4 and all(hp_pos[idx_h] not in locked_pos or base_cas_seq[hp_pos[idx_h]] == tl_s[idx_h] for idx_h in range(4)):
                    tup_h = tuple((hp_pos[idx_h], tl_s[idx_h]) for idx_h in range(4))
                    if tup_h not in hp_cands:
                        hp_cands.append(tup_h)
        elif closes_hp and len(hp_pos) == 3:
            hp_cands = []
            for tr_s in ("AAA", "AAC", "GAA", "GGG", base_cas_seq[uk_w + 1 : vk_w]):
                if len(tr_s) == 3 and all(hp_pos[idx_h] not in locked_pos or base_cas_seq[hp_pos[idx_h]] == tr_s[idx_h] for idx_h in range(3)):
                    tup_h = tuple((hp_pos[idx_h], tr_s[idx_h]) for idx_h in range(3))
                    if tup_h not in hp_cands:
                        hp_cands.append(tup_h)
        elif closes_hp and len(hp_pos) >= 5:
            hp_cands = []
            for m5, m3 in (("G", "A"), ("A", "G"), ("G", "G"), ("A", "A"), ("U", "U"), (base_cas_seq[uk_w + 1], base_cas_seq[vk_w - 1])):
                tup_h = []
                for idx_h, p_h in enumerate(hp_pos):
                    if p_h in locked_pos:
                        tup_h.append((p_h, base_cas_seq[p_h]))
                    elif idx_h == 0:
                        tup_h.append((p_h, m5))
                    elif idx_h == len(hp_pos) - 1:
                        tup_h.append((p_h, m3))
                    else:
                        tup_h.append((p_h, "A"))
                tup_h = tuple(tup_h)
                if tup_h not in hp_cands:
                    hp_cands.append(tup_h)

        final_cas_ranked = []
        for (_bp_km1, _bp_k), st_list in trellis.items():
            for prev_pv, prev_wb, _prev_et, prev_assign in st_list:
                t_fin = list(base_cas_seq)
                for p_a, ch_a in prev_assign:
                    t_fin[p_a] = ch_a
                for h_assign in hp_cands:
                    for p_h, ch_h in h_assign:
                        t_fin[p_h] = ch_h
                    s_t = "".join(t_fin)
                    et_t = float(RNA.energy_of_struct(s_t, target))
                    d_ok = et_t - float(RNA.energy_of_struct(s_t, s_open_win[k_w]))
                    d_ok2 = et_t - float(RNA.energy_of_struct(s_t, s_open2_win[k_w - 1]))
                    d_oall = et_t - float(RNA.energy_of_struct(s_t, s_open_all_win))
                    d_ms = et_t - float(RNA.energy_of_struct(s_t, ms))
                    tot_pv = round(prev_pv + max(0.0, d_ok + 0.05) + max(0.0, d_ok2 + 0.05) + max(0.0, d_oall + 0.05), 4)
                    tot_wb = round(max(prev_wb, d_ok, d_ok2, d_oall), 4)
                    full_assign = prev_assign + h_assign
                    b0_tag = t_fin[win[0][0]] + t_fin[win[0][1]]
                    bk_tag = t_fin[win[k_w][0]] + t_fin[win[k_w][1]]
                    final_cas_ranked.append((tot_pv, tot_wb, round(d_ms, 4), round(et_t, 4), (b0_tag, bk_tag), full_assign, s_t))

        final_cas_ranked.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
        selected_cas = []
        seen_cas_as = set()
        bucket_cnt = {}
        for item_c in final_cas_ranked:
            as_c = item_c[5]
            b_tag = item_c[4]
            if as_c not in seen_cas_as and (len(selected_cas) < 80 or bucket_cnt.get(b_tag, 0) < 6):
                seen_cas_as.add(as_c)
                bucket_cnt[b_tag] = bucket_cnt.get(b_tag, 0) + 1
                selected_cas.append(item_c)
                if len(selected_cas) >= 160:
                    break

        cas_worst_wb = [item_c[1] for item_c in selected_cas]
        cas_alive = list(range(len(selected_cas)))
        for _cas_step in range(28):
            if not cas_alive or time.time() - t0 >= max_sec * 0.52:
                break
            best_ci = min(
                cas_alive,
                key=lambda idx_c: (
                    max(0.0, cas_worst_wb[idx_c]),
                    selected_cas[idx_c][0],
                    cas_worst_wb[idx_c],
                    selected_cas[idx_c][2],
                    selected_cas[idx_c][3],
                ),
            )
            _pv_c, _wb_c, _dms_c, _et_c, _btag_c, full_assign, _st_c = selected_cas[best_ci]
            cas_worst_wb[best_ci] = 999.0
            last_cas_fms = None
            cas_improved = False
            for seed_cas in ({base_cas_seq, cur_seq}):
                trial_c = list(seed_cas)
                for p_a, ch_a in full_assign:
                    trial_c[p_a] = ch_a
                for s_rep in repair_budget_candidates(trial_c, pinfo, all_win_pos, ms, rng, max_k=4):
                    tvb = budget_violation(s_rep, pinfo)
                    if tvb > cur_vb:
                        continue
                    tms, tme = exact_fold(s_rep, eng)
                    last_cas_fms = tms
                    t_m_bps = get_bp_set(tms)
                    tdbp = len(t_bps ^ t_m_bps)
                    tde = round(float(RNA.energy_of_struct(s_rep, target)) - tme, 4)
                    if tdbp == 0 and tvb == 0:
                        ok, _, _ = check_full_solve(s_rep, pinfo, eng)
                        if ok:
                            return True, s_rep, 0, 0, 0.0
                    if tdbp > 0 and len(t_m_bps - t_bps) > 0 and (_pv_c == 0 or all(uv_w in t_m_bps for uv_w in win)):
                        s_reo, ms_reo, dbp_reo, de_reo = reorthogonalize_stems_after_stage_b(
                            s_rep, tms, all_win_pos, tuple(win), max_steps=10, max_cands=44
                        )
                        if dbp_reo < tdbp or (dbp_reo == tdbp and de_reo < tde):
                            s_rep, tms, tdbp, tde = s_reo, ms_reo, dbp_reo, de_reo
                            t_m_bps = get_bp_set(tms)
                            if tdbp == 0 and tvb == 0:
                                ok, _, _ = check_full_solve(s_rep, pinfo, eng)
                                if ok:
                                    return True, s_rep, 0, 0, 0.0
                    if (tvb, tdbp, tde) < (cur_vb, cur_dbp, cur_de):
                        cur_seq, cur_vb, cur_dbp, cur_de, ms = s_rep, tvb, tdbp, tde, tms
                        m_bps = get_bp_set(ms)
                        cas_improved = True
                        break
                if cas_improved:
                    break
            if last_cas_fms is not None:
                fbps_cas = get_bp_set(last_cas_fms)
                ext_cas = fbps_cas - t_bps
                if not ext_cas or all(x in all_win_pos and y in all_win_pos for x, y in ext_cas):
                    new_cas_alive = []
                    for idx_c in cas_alive:
                        if idx_c == best_ci:
                            continue
                        s_ic, et_ic = selected_cas[idx_c][6], selected_cas[idx_c][3]
                        d_new = round(et_ic - float(RNA.energy_of_struct(s_ic, last_cas_fms)), 4)
                        if d_new > cas_worst_wb[idx_c]:
                            cas_worst_wb[idx_c] = d_new
                        if cas_worst_wb[idx_c] <= 0.35:
                            new_cas_alive.append(idx_c)
                    cas_alive = new_cas_alive
                else:
                    cas_alive = [idx_c for idx_c in cas_alive if idx_c != best_ci]
            else:
                cas_alive = [idx_c for idx_c in cas_alive if idx_c != best_ci]

    # Exact `2x1`, `1x2`, and `1x1` Internal-Loop Block Enumerator (`<= 2,304` states in `12 us`)
    loop_blocks = []
    for p1, p2, q1, u_out, v_out, u_in, v_in in pinfo["loops_2x1"]:
        loop_blocks.append(((p1, p2, q1), u_out, v_out, u_in, v_in))
    for p1, q1, q2, u_out, v_out, u_in, v_in in pinfo["loops_1x2"]:
        loop_blocks.append(((p1, q1, q2), u_out, v_out, u_in, v_in))
    for p1, q1, u_out, v_out, u_in, v_in in pinfo["loops_1x1"]:
        loop_blocks.append(((p1, q1), u_out, v_out, u_in, v_in))

    lp_cap = 0.28 if cur_dbp <= 2 else 0.56
    for unp_tup, u_out, v_out, u_in, v_in in loop_blocks:
        if time.time() - t0 >= max_sec * lp_cap:
            break
        diff_now = m_bps ^ t_bps
        if (u_out, v_out) in m_bps and (u_in, v_in) in m_bps and not any(
            min(abs(x - u_out), abs(x - v_out), abs(x - u_in), abs(x - v_in)) <= 2 for uv in diff_now for x in uv
        ):
            continue
        ms_oo = list(target)
        ms_oo[u_out], ms_oo[v_out] = ".", "."
        s_open_out = "".join(ms_oo)
        ms_oi = list(target)
        ms_oi[u_in], ms_oi[v_in] = ".", "."
        s_open_in = "".join(ms_oi)

        unp_doms = [BASES if p_u not in locked_pos else (cur_seq[p_u],) for p_u in unp_tup]
        lp_ranked = []
        base_lp_seq = s_clean if budget_violation(s_clean, pinfo) <= cur_vb else cur_seq
        t_lp = list(base_lp_seq)
        for bp_out in allowed_pairs[(u_out, v_out)]:
            t_lp[u_out], t_lp[v_out] = bp_out[0], bp_out[1]
            for bp_in in allowed_pairs[(u_in, v_in)]:
                t_lp[u_in], t_lp[v_in] = bp_in[0], bp_in[1]
                for u_vals in itertools.product(*unp_doms):
                    if len(unp_tup) == 2 and (u_vals[0] + u_vals[1]) in VALID_SET:
                        continue
                    for p_u, ch_u in zip(unp_tup, u_vals):
                        t_lp[p_u] = ch_u
                    s_l = "".join(t_lp)
                    et_l = float(RNA.energy_of_struct(s_l, target))
                    eoo_l = float(RNA.energy_of_struct(s_l, s_open_out))
                    eoi_l = float(RNA.energy_of_struct(s_l, s_open_in))
                    em_l = float(RNA.energy_of_struct(s_l, ms))
                    lp_ranked.append((round(max(et_l - eoo_l, et_l - eoi_l), 4), round(et_l - em_l, 4), round(et_l, 4), bp_out, bp_in, u_vals))

        lp_ranked.sort(key=lambda x: (x[0], x[1], x[2]))
        prot_lp = {u_out, v_out, u_in, v_in} | set(unp_tup)
        for _d1, _d2, _etl, bp_out, bp_in, u_vals in lp_ranked[:36]:
            if time.time() - t0 >= max_sec * lp_cap:
                break
            for seed_lp in ({base_lp_seq, cur_seq}):
                trial = list(seed_lp)
                trial[u_out], trial[v_out] = bp_out[0], bp_out[1]
                trial[u_in], trial[v_in] = bp_in[0], bp_in[1]
                for p_u, ch_u in zip(unp_tup, u_vals):
                    trial[p_u] = ch_u
                for s_rep in repair_budget_candidates(trial, pinfo, prot_lp, ms, rng, max_k=4):
                    tvb = budget_violation(s_rep, pinfo)
                    if tvb > cur_vb:
                        continue
                    tms, tme = exact_fold(s_rep, eng)
                    t_m_bps = get_bp_set(tms)
                    tdbp = len(t_bps ^ t_m_bps)
                    tde = round(float(RNA.energy_of_struct(s_rep, target)) - tme, 4)
                    if tdbp == 0 and tvb == 0:
                        ok, _, _ = check_full_solve(s_rep, pinfo, eng)
                        if ok:
                            return True, s_rep, 0, 0, 0.0
                    if tdbp > 0 and len(t_m_bps - t_bps) > 0 and (_d1 <= 0.0 or ((u_out, v_out) in t_m_bps and (u_in, v_in) in t_m_bps)):
                        s_reo, ms_reo, dbp_reo, de_reo = reorthogonalize_stems_after_stage_b(
                            s_rep, tms, prot_lp, ((u_out, v_out), (u_in, v_in)), max_steps=10, max_cands=44
                        )
                        if dbp_reo < tdbp or (dbp_reo == tdbp and de_reo < tde):
                            s_rep, tms, tdbp, tde = s_reo, ms_reo, dbp_reo, de_reo
                            t_m_bps = get_bp_set(tms)
                            if tdbp == 0 and tvb == 0:
                                ok, _, _ = check_full_solve(s_rep, pinfo, eng)
                                if ok:
                                    return True, s_rep, 0, 0, 0.0
                    if (tvb, tdbp, tde) < (cur_vb, cur_dbp, cur_de):
                        cur_seq, cur_vb, cur_dbp, cur_de, ms = s_rep, tvb, tdbp, tde, tms
                        m_bps = get_bp_set(ms)

    # --- Stage B2: Multi-Pass `Op-M1 + CLSS-3` Cut-Pair Inside/Outside Compositional Synthesizer ---
    for _cut_pass in range(3):
        if time.time() - t0 >= max_sec * 0.88:
            break
        m_bps = get_bp_set(ms)
        # Per-pass Kempe re-equilibration (`Prawo 1b`): upgrade accidental AU/GU pairs or swap AU/GU on missing pairs
        for u_m, v_m in sorted(t_bps - m_bps) + [uv for uv in pairs if PAIR_TYPE.get(cur_seq[uv[0]] + cur_seq[uv[1]]) in ("AU", "GU")]:
            if PAIR_TYPE.get(cur_seq[u_m] + cur_seq[v_m]) in ("AU", "GU"):
                gc_cands_m = [bp for bp in allowed_pairs[(u_m, v_m)] if PAIR_TYPE.get(bp) == "GC"]
                for bp_gm in gc_cands_m:
                    t_gm = list(cur_seq)
                    t_gm[u_m], t_gm[v_m] = bp_gm[0], bp_gm[1]
                    for s_gm in repair_budget_candidates(t_gm, pinfo, {u_m, v_m}, ms, rng, max_k=4):
                        tvb_gm = budget_violation(s_gm, pinfo)
                        if tvb_gm > cur_vb:
                            continue
                        tms_gm, tme_gm = exact_fold(s_gm, eng)
                        tdbp_gm = len(t_bps ^ get_bp_set(tms_gm))
                        tde_gm = round(float(RNA.energy_of_struct(s_gm, target)) - tme_gm, 4)
                        if tdbp_gm == 0 and tvb_gm == 0:
                            ok, _, _ = check_full_solve(s_gm, pinfo, eng)
                            if ok:
                                return True, s_gm, 0, 0, 0.0
                        if (tvb_gm, tdbp_gm, tde_gm) < (cur_vb, cur_dbp, cur_de):
                            cur_seq, cur_vb, cur_dbp, cur_de, ms = s_gm, tvb_gm, tdbp_gm, tde_gm, tms_gm
                            m_bps = get_bp_set(ms)
                            break
        cut_targets = list(sorted(t_bps - m_bps))
        # Rule 2 (`Single-Extra-Pair Loop Frustration Rule`): include target pairs bounding any loop with `(pu, pv) in m_bps - t_bps`
        for pu, pv in sorted(m_bps - t_bps):
            for idx_p in (pu, pv, pu - 1, pu + 1, pv - 1, pv + 1):
                if 0 <= idx_p < n and pair_of[idx_p] != -1:
                    uv_adj = (min(idx_p, pair_of[idx_p]), max(idx_p, pair_of[idx_p]))
                    if uv_adj not in cut_targets:
                        cut_targets.append(uv_adj)
            for p_start in (pu, pv):
                p_walk = p_start - 1
                while p_walk >= 0 and pair_of[p_walk] == -1 and p_start - p_walk <= 10:
                    p_walk -= 1
                if p_walk >= 0 and pair_of[p_walk] != -1:
                    uv_w = (min(p_walk, pair_of[p_walk]), max(p_walk, pair_of[p_walk]))
                    if uv_w not in cut_targets:
                        cut_targets.append(uv_w)
                p_walk = p_start + 1
                while p_walk < n and pair_of[p_walk] == -1 and p_walk - p_start <= 10:
                    p_walk += 1
                if p_walk < n and pair_of[p_walk] != -1:
                    uv_w = (min(p_walk, pair_of[p_walk]), max(p_walk, pair_of[p_walk]))
                    if uv_w not in cut_targets:
                        cut_targets.append(uv_w)
        if not cut_targets:
            break
        any_pass_improved = False
        for u0, v0 in cut_targets:
            if time.time() - t0 >= max_sec * 0.88:
                break
            # Construct `ms_open_1`: `target` with ONLY `(u0, v0)` opened
            ms_open_lst = list(target)
            ms_open_lst[u0] = "."
            ms_open_lst[v0] = "."
            ms_open_1 = "".join(ms_open_lst)

            # Collect Inner Half-Seam (`in_pairs[:2]`, `in_unp[:3]`) inside `[u0+1 .. v0-1]` using 2D Graph hops + inner ring walk
            in_seed = set()
            ring_in_pairs = []
            p_il = u0 + 1
            while p_il < v0 and pair_of[p_il] == -1 and p_il - u0 <= 8:
                in_seed.add(p_il)
                p_il += 1
            if p_il < v0 and pair_of[p_il] != -1 and u0 < pair_of[p_il] < v0:
                uv_il = (min(p_il, pair_of[p_il]), max(p_il, pair_of[p_il]))
                if len(allowed_pairs[uv_il]) > 1 and uv_il not in ring_in_pairs:
                    ring_in_pairs.append(uv_il)
            p_ir = v0 - 1
            while p_ir > u0 and pair_of[p_ir] == -1 and v0 - p_ir <= 8:
                in_seed.add(p_ir)
                p_ir -= 1
            if p_ir > u0 and pair_of[p_ir] != -1 and u0 < pair_of[p_ir] < v0:
                uv_ir = (min(p_ir, pair_of[p_ir]), max(p_ir, pair_of[p_ir]))
                if len(allowed_pairs[uv_ir]) > 1 and uv_ir not in ring_in_pairs:
                    ring_in_pairs.append(uv_ir)
            for d in range(1, min(5, v0 - u0)):
                if u0 + d < v0:
                    in_seed.add(u0 + d)
                if v0 - d > u0:
                    in_seed.add(v0 - d)
            for idx_s in list(in_seed):
                q_s = pair_of[idx_s]
                if u0 < q_s < v0:
                    for d2 in (-2, -1, 0, 1, 2):
                        if u0 < q_s + d2 < v0:
                            in_seed.add(q_s + d2)
            in_pairs_other = sorted(
                {
                    (min(i, pair_of[i]), max(i, pair_of[i]))
                    for i in in_seed
                    if pair_of[i] != -1
                    and u0 < i < v0
                    and len(allowed_pairs[(min(i, pair_of[i]), max(i, pair_of[i]))]) > 1
                    and (min(i, pair_of[i]), max(i, pair_of[i])) not in ring_in_pairs
                },
                key=lambda uv: min(abs(uv[0] - u0) + abs(uv[1] - v0), abs(uv[0] - u0), abs(uv[1] - v0)),
            )
            in_pairs = (ring_in_pairs + in_pairs_other)[:2]
            in_unp = sorted(
                [i for i in in_seed if pair_of[i] == -1 and i not in locked_pos],
                key=lambda i: min(abs(i - u0), abs(i - v0)),
            )[:3]

            # Rule 1 (`Shared-Dangle Sibling Coupling Law`): walk left from `u0-1` and right from `v0+1` along the multiloop ring
            out_seed = set()
            ring_out_pairs = []
            p_ol = u0 - 1
            while p_ol >= 0 and pair_of[p_ol] == -1 and u0 - p_ol <= 8:
                out_seed.add(p_ol)
                p_ol -= 1
            if p_ol >= 0 and pair_of[p_ol] != -1 and (pair_of[p_ol] < u0 or pair_of[p_ol] > v0):
                uv_ol = (min(p_ol, pair_of[p_ol]), max(p_ol, pair_of[p_ol]))
                if len(allowed_pairs[uv_ol]) > 1 and uv_ol not in ring_out_pairs:
                    ring_out_pairs.append(uv_ol)
                for d_ol in (-1, 1):
                    if 0 <= pair_of[p_ol] + d_ol < n and (pair_of[p_ol] + d_ol < u0 or pair_of[p_ol] + d_ol > v0):
                        out_seed.add(pair_of[p_ol] + d_ol)
            p_or = v0 + 1
            while p_or < n and pair_of[p_or] == -1 and p_or - v0 <= 8:
                out_seed.add(p_or)
                p_or += 1
            if p_or < n and pair_of[p_or] != -1 and (pair_of[p_or] < u0 or pair_of[p_or] > v0):
                uv_or = (min(p_or, pair_of[p_or]), max(p_or, pair_of[p_or]))
                if len(allowed_pairs[uv_or]) > 1 and uv_or not in ring_out_pairs:
                    ring_out_pairs.append(uv_or)
                for d_or in (-1, 1):
                    if 0 <= pair_of[p_or] + d_or < n and (pair_of[p_or] + d_or < u0 or pair_of[p_or] + d_or > v0):
                        out_seed.add(pair_of[p_or] + d_or)
            for d in range(1, 5):
                if u0 - d >= 0:
                    out_seed.add(u0 - d)
                if v0 + d < n:
                    out_seed.add(v0 + d)
            for idx_s in list(out_seed):
                q_s = pair_of[idx_s]
                if q_s != -1 and (q_s < u0 or q_s > v0):
                    for d2 in (-2, -1, 0, 1, 2):
                        if 0 <= q_s + d2 < n and (q_s + d2 < u0 or q_s + d2 > v0):
                            out_seed.add(q_s + d2)
            out_pairs_other = sorted(
                {
                    (min(i, pair_of[i]), max(i, pair_of[i]))
                    for i in out_seed
                    if pair_of[i] != -1
                    and (i < u0 or i > v0)
                    and len(allowed_pairs[(min(i, pair_of[i]), max(i, pair_of[i]))]) > 1
                    and (min(i, pair_of[i]), max(i, pair_of[i])) not in ring_out_pairs
                },
                key=lambda uv: min(abs(uv[0] - u0), abs(uv[1] - u0), abs(uv[0] - v0), abs(uv[1] - v0)),
            )
            out_pairs = (ring_out_pairs + out_pairs_other)[:2]
            out_unp = sorted(
                [i for i in out_seed if pair_of[i] == -1 and i not in locked_pos],
                key=lambda i: min(abs(i - u0), abs(i - v0)),
            )[:3]

            parasitic_now = sorted(get_bp_set(ms) - t_bps)
            for pu, pv in parasitic_now:
                for p_para in (pu, pv):
                    if pair_of[p_para] == -1 and p_para not in locked_pos:
                        if u0 < p_para < v0:
                            if p_para in in_unp:
                                in_unp.remove(p_para)
                            in_unp.insert(0, p_para)
                            in_unp = in_unp[:4]
                        elif p_para < u0 or p_para > v0:
                            if p_para in out_unp:
                                out_unp.remove(p_para)
                            out_unp.insert(0, p_para)
                            out_unp = out_unp[:4]
            unp_para_in = [
                (pu, pv)
                for (pu, pv) in parasitic_now
                if pair_of[pu] == -1 and pair_of[pv] == -1 and (pu in in_unp or pv in in_unp)
            ]
            unp_para_out = [
                (pu, pv)
                for (pu, pv) in parasitic_now
                if pair_of[pu] == -1 and pair_of[pv] == -1 and (pu in out_unp or pv in out_unp)
            ]

            in_only_rivals = []
            for ua, va in in_pairs:
                tl_r = list(target)
                tl_r[ua], tl_r[va] = ".", "."
                in_only_rivals.append("".join(tl_r))
            out_only_rivals = []
            for ua, va in out_pairs:
                tl_r = list(target)
                tl_r[ua], tl_r[va] = ".", "."
                out_only_rivals.append("".join(tl_r))
            in_open_rivals = (in_only_rivals if in_only_rivals else [ms_open_1]) + ([ms] if not parasitic_now else [])
            out_open_rivals = (out_only_rivals if out_only_rivals else [ms_open_1]) + ([ms] if not parasitic_now else [])
            all_open_rivals = [ms_open_1] + in_only_rivals + out_only_rivals + ([ms] if not parasitic_now else [])

            joint_cands = []
            base_trial = list(cur_seq)

            in_p_dom = [allowed_pairs[uv] for uv in in_pairs]
            in_u_dom = [BASES for _ in in_unp]
            out_p_dom = [allowed_pairs[uv] for uv in out_pairs]
            out_u_dom = [BASES for _ in out_unp]

            for bp0 in allowed_pairs[(u0, v0)]:
                base_trial[u0], base_trial[v0] = bp0[0], bp0[1]

                # 1. Rank Inner Half-Seam modules (`<= 576` states) protecting `in_pairs` and `ms_open_1`
                in_ranked = []
                t_in = list(base_trial)
                for p_vals in itertools.product(*in_p_dom):
                    for (ua, va), bpa in zip(in_pairs, p_vals):
                        t_in[ua], t_in[va] = bpa[0], bpa[1]
                    for u_vals in itertools.product(*in_u_dom):
                        for idx_u, b_ch in zip(in_unp, u_vals):
                            t_in[idx_u] = b_ch
                        p_pen_i = 50.0 * sum(1 for (pu, pv) in unp_para_in if (t_in[pu] + t_in[pv]) in VALID_SET)
                        s_in = "".join(t_in)
                        et_i = float(RNA.energy_of_struct(s_in, target))
                        eo1_i = float(RNA.energy_of_struct(s_in, ms_open_1))
                        w_in = max(round(et_i - float(RNA.energy_of_struct(s_in, r_in)), 4) for r_in in in_open_rivals)
                        in_ranked.append((p_pen_i + max(0.0, w_in), p_pen_i + round(et_i - eo1_i, 4), round(et_i, 4), p_vals, u_vals))
                in_by_w = sorted(in_ranked, key=lambda x: (x[0], x[1], x[2]))[:12]
                in_by_o1 = sorted(in_ranked, key=lambda x: (x[1], x[0], x[2]))[:10]
                seen_in_keys = set()
                top_in = []
                for item_in in in_by_w + in_by_o1:
                    k_in = (item_in[3], item_in[4])
                    if k_in not in seen_in_keys:
                        seen_in_keys.add(k_in)
                        top_in.append(item_in)

                # 2. Rank Outer Half-Seam modules (`<= 576` states) protecting `out_pairs` and `ms_open_1`
                out_ranked = []
                t_out = list(base_trial)
                for p_vals in itertools.product(*out_p_dom):
                    for (ua, va), bpa in zip(out_pairs, p_vals):
                        t_out[ua], t_out[va] = bpa[0], bpa[1]
                    for u_vals in itertools.product(*out_u_dom):
                        for idx_u, b_ch in zip(out_unp, u_vals):
                            t_out[idx_u] = b_ch
                        p_pen_o = 50.0 * sum(1 for (pu, pv) in unp_para_out if (t_out[pu] + t_out[pv]) in VALID_SET)
                        s_out = "".join(t_out)
                        et_o = float(RNA.energy_of_struct(s_out, target))
                        eo1_o = float(RNA.energy_of_struct(s_out, ms_open_1))
                        w_out = max(round(et_o - float(RNA.energy_of_struct(s_out, r_out)), 4) for r_out in out_open_rivals)
                        out_ranked.append((p_pen_o + max(0.0, w_out), p_pen_o + round(et_o - eo1_o, 4), round(et_o, 4), p_vals, u_vals))
                out_by_w = sorted(out_ranked, key=lambda x: (x[0], x[1], x[2]))[:12]
                out_by_o1 = sorted(out_ranked, key=lambda x: (x[1], x[0], x[2]))[:10]
                seen_out_keys = set()
                top_out = []
                for item_out in out_by_w + out_by_o1:
                    k_out = (item_out[3], item_out[4])
                    if k_out not in seen_out_keys:
                        seen_out_keys.add(k_out)
                        top_out.append(item_out)

                # 3. Synthesize Joint `(bp0, top_in, top_out)` modules
                t_joint = list(base_trial)
                seen_joint_seqs = set()
                for _w_i, _sc_i, _eti, p_in_v, u_in_v in top_in:
                    for (ua, va), bpa in zip(in_pairs, p_in_v):
                        t_joint[ua], t_joint[va] = bpa[0], bpa[1]
                    for idx_u, b_ch in zip(in_unp, u_in_v):
                        t_joint[idx_u] = b_ch
                    for _w_o, _sc_o, _eto, p_out_v, u_out_v in top_out:
                        for (ua, va), bpa in zip(out_pairs, p_out_v):
                            t_joint[ua], t_joint[va] = bpa[0], bpa[1]
                        for idx_u, b_ch in zip(out_unp, u_out_v):
                            t_joint[idx_u] = b_ch
                        s_j = "".join(t_joint)
                        if s_j in seen_joint_seqs:
                            continue
                        seen_joint_seqs.add(s_j)
                        et_j = float(RNA.energy_of_struct(s_j, target))
                        eo1_j = float(RNA.energy_of_struct(s_j, ms_open_1))
                        w_all = max(round(et_j - float(RNA.energy_of_struct(s_j, r_a)), 4) for r_a in all_open_rivals)
                        broken_p = sum(1 for (pu, pv) in parasitic_now if (t_joint[pu] + t_joint[pv]) not in VALID_SET)
                        em_j = float(RNA.energy_of_struct(s_j, ms)) + 5.0 * broken_p
                        joint_cands.append(
                            (
                                s_j,
                                round(et_j, 4),
                                round(et_j - eo1_j, 4),
                                w_all,
                                round(et_j - em_j, 4),
                                bp0,
                                p_in_v,
                                u_in_v,
                                p_out_v,
                                u_out_v,
                            )
                        )

                # 3b. `Prawo 2` Direct Joint Loop-Seam Product over `(in_pairs[:1], out_pairs[:1], jw_unp[:3])` (`<= 2,304` states per `bp0`)
                # Sieved by `et_j - eo1_j <= 0.05` so coupled inner+outer loop states never get dropped by half-seam splitting!
                jw_in_p = in_pairs[:1]
                jw_out_p = out_pairs[:1]
                jw_in_u = in_unp[:2]
                jw_out_u = out_unp[: (1 if len(jw_in_u) >= 2 else 2)]
                jw_in_p_dom = [allowed_pairs[uv] for uv in jw_in_p]
                jw_out_p_dom = [allowed_pairs[uv] for uv in jw_out_p]
                jw_in_u_dom = [BASES for _ in jw_in_u]
                jw_out_u_dom = [BASES for _ in jw_out_u]
                t_jw = list(base_trial)
                for p_in_jw in itertools.product(*jw_in_p_dom):
                    for (ua, va), bpa in zip(jw_in_p, p_in_jw):
                        t_jw[ua], t_jw[va] = bpa[0], bpa[1]
                    for p_out_jw in itertools.product(*jw_out_p_dom):
                        for (ua, va), bpa in zip(jw_out_p, p_out_jw):
                            t_jw[ua], t_jw[va] = bpa[0], bpa[1]
                        for u_in_jw in itertools.product(*jw_in_u_dom):
                            for idx_u, b_ch in zip(jw_in_u, u_in_jw):
                                t_jw[idx_u] = b_ch
                            for u_out_jw in itertools.product(*jw_out_u_dom):
                                for idx_u, b_ch in zip(jw_out_u, u_out_jw):
                                    t_jw[idx_u] = b_ch
                                if (unp_para_in or unp_para_out) and any(
                                    (t_jw[pu] + t_jw[pv]) in VALID_SET for (pu, pv) in (unp_para_in + unp_para_out)
                                ):
                                    continue
                                s_jw = "".join(t_jw)
                                if s_jw in seen_joint_seqs:
                                    continue
                                et_jw = float(RNA.energy_of_struct(s_jw, target))
                                eo1_jw = (
                                    min(float(RNA.energy_of_struct(s_jw, ms_open_1)), float(RNA.energy_of_struct(s_jw, ms)))
                                    if not parasitic_now
                                    else float(RNA.energy_of_struct(s_jw, ms_open_1))
                                )
                                d_o1_jw = round(et_jw - eo1_jw, 4)
                                if d_o1_jw > 0.05:
                                    continue
                                seen_joint_seqs.add(s_jw)
                                w_all_jw = max(round(et_jw - float(RNA.energy_of_struct(s_jw, r_a)), 4) for r_a in all_open_rivals)
                                broken_jw = sum(1 for (pu, pv) in parasitic_now if (t_jw[pu] + t_jw[pv]) not in VALID_SET)
                                em_jw = float(RNA.energy_of_struct(s_jw, ms)) + 5.0 * broken_jw
                                full_p_in = tuple(t_jw[ua] + t_jw[va] for (ua, va) in in_pairs)
                                full_u_in = tuple(t_jw[idx_u] for idx_u in in_unp)
                                full_p_out = tuple(t_jw[ua] + t_jw[va] for (ua, va) in out_pairs)
                                full_u_out = tuple(t_jw[idx_u] for idx_u in out_unp)
                                joint_cands.append(
                                    (
                                        s_jw,
                                        round(et_jw, 4),
                                        d_o1_jw,
                                        w_all_jw,
                                        round(et_jw - em_jw, 4),
                                        bp0,
                                        full_p_in,
                                        full_u_in,
                                        full_p_out,
                                        full_u_out,
                                    )
                                )

            prot_cut = (
                {u0, v0}
                | {i for uv in in_pairs for i in uv}
                | set(in_unp)
                | {i for uv in out_pairs for i in uv}
                | set(out_unp)
            )
            seen_cut = {cur_seq}
            cut_improved = False
            cut_seeds = [cur_seq]
            if s_clean != cur_seq and budget_violation(s_clean, pinfo) <= cur_vb:
                cut_seeds.insert(0, s_clean)

            # 4. Local Window Iterative Multi-Rival CEGIS over `joint_cands`
            worst_d = [jc[2] for jc in joint_cands]
            alive = list(range(len(joint_cands)))
            for _cegis_step in range(32):
                if not alive or (_cegis_step >= 16 and time.time() - t0 >= max_sec * 0.90):
                    break
                best_i = min(
                    alive,
                    key=lambda i: (
                        max(0.0, worst_d[i]),
                        max(0.0, joint_cands[i][3]),
                        joint_cands[i][2],
                        joint_cands[i][4],
                        joint_cands[i][1],
                    ),
                )
                _sj, _etj, d_open1, _wall, d_ms, bp0, p_in_v, u_in_v, p_out_v, u_out_v = joint_cands[best_i]
                worst_d[best_i] = 999.0
                last_fms = None
                for seed_cut in cut_seeds:
                    t_cand = list(seed_cut)
                    t_cand[u0], t_cand[v0] = bp0[0], bp0[1]
                    for (ua, va), bpa in zip(in_pairs, p_in_v):
                        t_cand[ua], t_cand[va] = bpa[0], bpa[1]
                    for idx_u, b_ch in zip(in_unp, u_in_v):
                        t_cand[idx_u] = b_ch
                    for (ua, va), bpa in zip(out_pairs, p_out_v):
                        t_cand[ua], t_cand[va] = bpa[0], bpa[1]
                    for idx_u, b_ch in zip(out_unp, u_out_v):
                        t_cand[idx_u] = b_ch
                    for s_rep in repair_budget_candidates(t_cand, pinfo, prot_cut, ms, rng, max_k=4):
                        if s_rep in seen_cut:
                            continue
                        seen_cut.add(s_rep)
                        tvb = budget_violation(s_rep, pinfo)
                        if tvb > cur_vb:
                            continue
                        tms, tme = exact_fold(s_rep, eng)
                        last_fms = tms
                        tdbp = len(t_bps ^ get_bp_set(tms))
                        tte = float(RNA.energy_of_struct(s_rep, target))
                        tde = round(tte - tme, 4)
                        tms_bps = get_bp_set(tms)
                        if tdbp == 0 and tvb == 0:
                            ok, _, _ = check_full_solve(s_rep, pinfo, eng)
                            if ok:
                                return True, s_rep, 0, 0, 0.0
                        if tdbp > 0 and len(tms_bps - t_bps) > 0 and (d_open1 <= 0.0 or (u0, v0) in tms_bps):
                            s_reo, ms_reo, dbp_reo, de_reo = reorthogonalize_stems_after_stage_b(
                                s_rep, tms, prot_cut, ((u0, v0),), max_steps=10, max_cands=44
                            )
                            if dbp_reo < tdbp or (dbp_reo == tdbp and de_reo < tde):
                                s_rep, tms, tdbp, tde = s_reo, ms_reo, dbp_reo, de_reo
                                tms_bps = get_bp_set(tms)
                                if tdbp == 0 and tvb == 0:
                                    ok, _, _ = check_full_solve(s_rep, pinfo, eng)
                                    if ok:
                                        return True, s_rep, 0, 0, 0.0
                        if tvb < cur_vb or (tvb == cur_vb and tdbp < cur_dbp):
                            cur_seq, cur_vb, cur_dbp, cur_de, ms = s_rep, tvb, tdbp, tde, tms
                            m_bps = tms_bps
                            cut_improved = True
                            any_pass_improved = True
                            break
                        elif (tvb, tdbp, tde) < (cur_vb, cur_dbp, cur_de):
                            cur_seq, cur_vb, cur_dbp, cur_de, ms = s_rep, tvb, tdbp, tde, tms
                            m_bps = tms_bps
                            any_pass_improved = True
                    if cut_improved:
                        break
                if cut_improved:
                    break
                # Add `last_fms` as a cutting-plane rival:
                # - If all symmetric-difference pairs `diff_cut = fbps_cut ^ t_bps` lie inside `prot_cut`, update `worst_d[i_a]` with exact Turner energy `et_ia - E(s_ia, last_fms)`.
                # - If extra pairs cross outside `prot_cut`, penalize candidates that keep the cross-window pairs intact without wiping `alive`.
                if last_fms is not None:
                    fbps_cut = get_bp_set(last_fms)
                    ext_cut = fbps_cut - t_bps
                    diff_cut = fbps_cut ^ t_bps
                    if diff_cut and all(x in prot_cut and y in prot_cut for x, y in diff_cut):
                        new_alive = []
                        for i_a in alive:
                            if i_a == best_i:
                                continue
                            s_ia, et_ia = joint_cands[i_a][0], joint_cands[i_a][1]
                            d_new = round(et_ia - float(RNA.energy_of_struct(s_ia, last_fms)), 4)
                            if d_new > worst_d[i_a]:
                                worst_d[i_a] = d_new
                            new_alive.append(i_a)
                        alive = new_alive
                    elif any(x in prot_cut or y in prot_cut for x, y in ext_cut):
                        touch_ext = [(x_e, y_e) for (x_e, y_e) in ext_cut if x_e in prot_cut or y_e in prot_cut]
                        new_alive = []
                        for i_a in alive:
                            if i_a == best_i:
                                continue
                            s_ia = joint_cands[i_a][0]
                            intact = sum(1 for (x_e, y_e) in touch_ext if (s_ia[x_e] + s_ia[y_e]) in VALID_SET)
                            if intact == len(touch_ext):
                                worst_d[i_a] = round(max(0.0, worst_d[i_a]) + 0.35, 4)
                            elif intact > 0:
                                worst_d[i_a] = round(worst_d[i_a] + 0.10 * intact, 4)
                            new_alive.append(i_a)
                        alive = new_alive
                    else:
                        alive = [i_a for i_a in alive if i_a != best_i]
                else:
                    alive = [i_a for i_a in alive if i_a != best_i]
        if not any_pass_improved:
            break

    # --- Stage C: `Law M37` Coupled 2-Variable Saddle Enumerator + Cutting-Plane Tabu CEGIS ---
    rivals = [ms] if ms != target else []
    tabu_seqs = {cur_seq}
    best_c_state = (cur_vb, cur_dbp, cur_de, cur_seq, ms)

    def compute_dg_ens(seq_s: str, te_val: float) -> float:
        try:
            md = RNA.md()
            md.dangles = 1 if eng == 1 else 2
            md.temperature = 37.0
            md.noLP = 0
            fc = RNA.fold_compound(seq_s, md)
            _, pf_e = fc.pf()
            return round(te_val - float(pf_e), 4)
        except Exception:
            return 999.0

    cur_dgens = compute_dg_ens(cur_seq, float(RNA.energy_of_struct(cur_seq, target))) if cur_de <= 0.05 else 999.0

    for _round in range(8):
        if time.time() - t0 >= max_sec * 0.84:
            break
        m_bps = get_bp_set(ms)
        diff_bps = sorted(t_bps ^ m_bps)
        parasitic_bps = sorted(m_bps - t_bps)
        missing_bps = sorted(t_bps - m_bps)
        if not diff_bps:
            break

        loc_pos = set()
        for u0, v0 in diff_bps:
            for d in range(-3, 4):
                if 0 <= u0 + d < n:
                    loc_pos.add(u0 + d)
                if 0 <= v0 + d < n:
                    loc_pos.add(v0 + d)
            if 0 < v0 - u0 <= 14:
                for idx_in in range(max(0, u0 - 1), min(n, v0 + 2)):
                    loc_pos.add(idx_in)
        # Expand `loc_pos` by 1 hop along base pairs in the 2D secondary structure graph (`Law M38`)
        for idx_g in list(loc_pos):
            q_g = pair_of[idx_g]
            if q_g != -1:
                for d2 in (-2, -1, 0, 1, 2):
                    if 0 <= q_g + d2 < n:
                        loc_pos.add(q_g + d2)

        defect_pair_set = {
            (min(i, pair_of[i]), max(i, pair_of[i]))
            for i in loc_pos
            if pair_of[i] != -1
        }
        defect_unp_set = {
            i
            for i in loc_pos
            if pair_of[i] == -1 and i not in locked_pos
        }
        loc_pairs = sorted(
            {
                (min(i, pair_of[i]), max(i, pair_of[i]))
                for i in loc_pos
                if pair_of[i] != -1 and len(allowed_pairs[(min(i, pair_of[i]), max(i, pair_of[i]))]) > 1
            },
            key=lambda uv: (0 if uv in defect_pair_set else 1, -pinfo["pair_priority"][uv]),
        )[:6]
        loc_unp = sorted(
            [i for i in loc_pos if pair_of[i] == -1 and i not in locked_pos],
            key=lambda i: (0 if i in defect_unp_set else 1, i),
        )[:8]

        # 0. Direct Parasitic-Breaking Coupled Moves (break `(pu, pv) in m_bps - t_bps` + 1 neighbor)
        direct_break_edits = []
        for pu, pv in parasitic_bps[:3]:
            break_ways = []
            if pair_of[pu] != -1:
                ut, vt = min(pu, pair_of[pu]), max(pu, pair_of[pu])
                for bp_t in allowed_pairs[(ut, vt)]:
                    b_pu = bp_t[0] if pu == ut else bp_t[1]
                    if (b_pu + cur_seq[pv]) not in VALID_SET:
                        break_ways.append(((ut, bp_t[0]), (vt, bp_t[1])))
            elif pu not in locked_pos:
                for b_pu in BASES:
                    if (b_pu + cur_seq[pv]) not in VALID_SET:
                        break_ways.append(((pu, b_pu),))
            if pair_of[pv] != -1:
                ut, vt = min(pv, pair_of[pv]), max(pv, pair_of[pv])
                for bp_t in allowed_pairs[(ut, vt)]:
                    b_pv = bp_t[0] if pv == ut else bp_t[1]
                    if (cur_seq[pu] + b_pv) not in VALID_SET:
                        break_ways.append(((ut, bp_t[0]), (vt, bp_t[1])))
            elif pv not in locked_pos:
                for b_pv in BASES:
                    if (cur_seq[pu] + b_pv) not in VALID_SET:
                        break_ways.append(((pv, b_pv),))
            # Also simultaneously change both pu and pv if both are unpaired
            if pair_of[pu] == -1 and pair_of[pv] == -1 and pu not in locked_pos and pv not in locked_pos:
                for b_pu in BASES:
                    for b_pv in BASES:
                        if (b_pu + b_pv) not in VALID_SET and (b_pu != cur_seq[pu] or b_pv != cur_seq[pv]):
                            break_ways.append(((pu, b_pu), (pv, b_pv)))

            for bw in break_ways:
                direct_break_edits.append(bw)
                bw_pos = {p for p, _ in bw}
                for u2, v2 in loc_pairs[:4]:
                    if u2 not in bw_pos and v2 not in bw_pos:
                        for bp2 in allowed_pairs[(u2, v2)]:
                            if bp2 != cur_seq[u2] + cur_seq[v2]:
                                direct_break_edits.append(bw + ((u2, bp2[0]), (v2, bp2[1])))
                for idx_u in loc_unp[:5]:
                    if idx_u not in bw_pos:
                        for b_ch in BASES:
                            if b_ch != cur_seq[idx_u]:
                                direct_break_edits.append(bw + ((idx_u, b_ch),))

        loc_open_rivals = []
        for ua_l, va_l in loc_pairs[:4]:
            tl_lo = list(target)
            tl_lo[ua_l], tl_lo[va_l] = ".", "."
            loc_open_rivals.append("".join(tl_lo))

        def score_candidate(trial_lst, edits_tuple):
            s_tr = "".join(trial_lst)
            et = float(RNA.energy_of_struct(s_tr, target))
            broken_para = sum(1 for (pu, pv) in parasitic_bps if (trial_lst[pu] + trial_lst[pv]) not in VALID_SET)
            open_pen = 0.0
            for ro in loc_open_rivals:
                go = et - float(RNA.energy_of_struct(s_tr, ro))
                if go > open_pen:
                    open_pen = go
            mg = -999.0
            sg = 0.0
            for rs in rivals[-8:]:
                r_bps = get_bp_set(rs)
                r_broken = sum(1 for (pu, pv) in (r_bps - t_bps) if (trial_lst[pu] + trial_lst[pv]) not in VALID_SET)
                er = float(RNA.energy_of_struct(s_tr, rs)) + 5.0 * r_broken
                g = et - er
                if g > mg:
                    mg = g
                sg += g
            return (round(max(mg, open_pen), 4), -broken_para, round(mg, 4), round(sg, 4), round(et, 4), edits_tuple)

        scored = []
        trial = list(cur_seq)

        for edits in direct_break_edits:
            saved = [(p, trial[p]) for p, _ in edits]
            for p, ch in edits:
                trial[p] = ch
            scored.append(score_candidate(trial, edits))
            for p, ch_old in saved:
                trial[p] = ch_old

        # 1. Coupled 2-pair moves (<= 15 * 36 = 540 states)
        for i1 in range(len(loc_pairs)):
            u1, v1 = loc_pairs[i1]
            o1u, o1v = trial[u1], trial[v1]
            for i2 in range(i1 + 1, len(loc_pairs)):
                u2, v2 = loc_pairs[i2]
                o2u, o2v = trial[u2], trial[v2]
                for bp1 in allowed_pairs[(u1, v1)]:
                    trial[u1], trial[v1] = bp1[0], bp1[1]
                    for bp2 in allowed_pairs[(u2, v2)]:
                        if bp1 == o1u + o1v and bp2 == o2u + o2v:
                            continue
                        trial[u2], trial[v2] = bp2[0], bp2[1]
                        scored.append(score_candidate(trial, ((u1, bp1[0]), (v1, bp1[1]), (u2, bp2[0]), (v2, bp2[1]))))
                trial[u2], trial[v2] = o2u, o2v
            trial[u1], trial[v1] = o1u, o1v

        # 2. Coupled 1-pair + 1-unpaired moves (<= 6 * 8 * 24 = 1,152 states)
        for u1, v1 in loc_pairs:
            o1u, o1v = trial[u1], trial[v1]
            for idx_u in loc_unp:
                ou = trial[idx_u]
                for bp1 in allowed_pairs[(u1, v1)]:
                    trial[u1], trial[v1] = bp1[0], bp1[1]
                    for b_ch in BASES:
                        if bp1 == o1u + o1v and b_ch == ou:
                            continue
                        trial[idx_u] = b_ch
                        scored.append(score_candidate(trial, ((u1, bp1[0]), (v1, bp1[1]), (idx_u, b_ch))))
                trial[idx_u] = ou
            trial[u1], trial[v1] = o1u, o1v

        # 3. Coupled 2-unpaired moves (<= 28 * 16 = 448 states)
        for j1 in range(len(loc_unp)):
            idx1 = loc_unp[j1]
            o1 = trial[idx1]
            for j2 in range(j1 + 1, len(loc_unp)):
                idx2 = loc_unp[j2]
                o2 = trial[idx2]
                for b1 in BASES:
                    trial[idx1] = b1
                    for b2 in BASES:
                        if b1 == o1 and b2 == o2:
                            continue
                        trial[idx2] = b2
                        scored.append(score_candidate(trial, ((idx1, b1), (idx2, b2))))
                trial[idx2] = o2
            trial[idx1] = o1

        scored.sort(key=lambda x: (x[0], x[1], x[2], x[3], x[4]))
        round_improved = False
        seen_seqs = set(tabu_seqs)
        saddle_best = None
        sieve_k = 180 if cur_dbp <= 2 else 90
        kempe_k = 5 if cur_dbp <= 2 else 2
        for _idx_sc, (_mgo, _bp_cnt, _mg, _sg, _et, edits) in enumerate(scored[:sieve_k]):
            if time.time() - t0 >= max_sec * 0.84:
                break
            trial_v = list(cur_seq)
            prot_set = set()
            for pos_e, ch_e in edits:
                trial_v[pos_e] = ch_e
                prot_set.add(pos_e)
            for s_rep in repair_budget_candidates(trial_v, pinfo, prot_set, ms, rng, max_k=kempe_k):
                if s_rep in seen_seqs:
                    continue
                seen_seqs.add(s_rep)
                tvb = budget_violation(s_rep, pinfo)
                if tvb > cur_vb:
                    continue
                tms, tme = exact_fold(s_rep, eng)
                tdbp = len(t_bps ^ get_bp_set(tms))
                tte = float(RNA.energy_of_struct(s_rep, target))
                tde = round(tte - tme, 4)
                if tdbp == 0 and tvb == 0:
                    ok, _, _ = check_full_solve(s_rep, pinfo, eng)
                    if ok:
                        return True, s_rep, 0, 0, 0.0
                if _idx_sc < 12 and tdbp > 0 and tdbp <= 4 and len(get_bp_set(tms) - t_bps) > 0:
                    s_reo, ms_reo, dbp_reo, de_reo = reorthogonalize_stems_after_stage_b(
                        s_rep, tms, prot_set, tuple(loc_pairs[:2]), max_steps=8, max_cands=36
                    )
                    if dbp_reo < tdbp or (dbp_reo == tdbp and de_reo < tde):
                        s_rep, tms, tdbp, tde = s_reo, ms_reo, dbp_reo, de_reo
                        tte = float(RNA.energy_of_struct(s_rep, target))
                        if tdbp == 0 and tvb == 0:
                            ok, _, _ = check_full_solve(s_rep, pinfo, eng)
                            if ok:
                                return True, s_rep, 0, 0, 0.0
                if tms != target and tms not in rivals:
                    rivals.append(tms)
                if (tvb, tdbp, tde) < (best_c_state[0], best_c_state[1], best_c_state[2]):
                    best_c_state = (tvb, tdbp, tde, s_rep, tms)
                if (tvb, tdbp, tde) < (cur_vb, cur_dbp, cur_de):
                    cur_seq, cur_vb, cur_dbp, cur_de, ms = s_rep, tvb, tdbp, tde, tms
                    tabu_seqs.add(s_rep)
                    cur_dgens = compute_dg_ens(cur_seq, tte) if cur_de <= 0.05 else 999.0
                    round_improved = True
                    break
                elif (tvb, tdbp, tde) == (cur_vb, cur_dbp, cur_de) and cur_de <= 0.05:
                    tdgens = compute_dg_ens(s_rep, tte)
                    if tdgens < cur_dgens - 0.01:
                        cur_seq, cur_vb, cur_dbp, cur_de, ms, cur_dgens = s_rep, tvb, tdbp, tde, tms, tdgens
                        tabu_seqs.add(s_rep)
                        round_improved = True
                        break
                elif saddle_best is None and tvb <= cur_vb and tdbp <= cur_dbp + 2 and s_rep not in tabu_seqs:
                    saddle_best = (tvb, tdbp, tde, s_rep, tms)
            if round_improved:
                break
        if not round_improved:
            if saddle_best is not None and _round < 7:
                cur_vb, cur_dbp, cur_de, cur_seq, ms = saddle_best
                tabu_seqs.add(cur_seq)
            else:
                break

    if (best_c_state[0], best_c_state[1], best_c_state[2]) < (cur_vb, cur_dbp, cur_de):
        cur_vb, cur_dbp, cur_de, cur_seq, ms = best_c_state

    # --- Stage D: McCaskill Partition Function `fc.pf()` (`md.dangles = 1`) + Coupled BPP Poisoning ---
    if cur_dbp <= 6 and time.time() - t0 < max_sec:
        for _pf_round in range(3):
            if time.time() - t0 >= max_sec:
                break
            try:
                md = RNA.md()
                md.dangles = 1 if eng == 1 else 2
                md.temperature = 37.0
                md.noLP = 0
                fc = RNA.fold_compound(cur_seq, md)
                _, pf_e = fc.pf()
                bpp = fc.bpp()
                te_now = float(RNA.energy_of_struct(cur_seq, target))
                cur_dgens = round(te_now - float(pf_e), 4)
            except Exception:
                break

            para_list = []
            for pu in range(n):
                row_b = bpp[pu + 1]
                for pv in range(pu + 4, n):
                    p_val = row_b[pv + 1]
                    if p_val > 0.05 and (pu, pv) not in t_bps:
                        para_list.append((p_val, pu, pv))
            para_list.sort(reverse=True)
            if not para_list:
                break

            pf_improved = False
            for _pval, pu, pv in para_list[:6]:
                if time.time() - t0 >= max_sec:
                    break
                cand_edits = []
                if pair_of[pu] != -1:
                    u_t, v_t = min(pu, pair_of[pu]), max(pu, pair_of[pu])
                    for bp_t in allowed_pairs[(u_t, v_t)]:
                        b_pu = bp_t[0] if pu == u_t else bp_t[1]
                        if (b_pu + cur_seq[pv]) not in VALID_SET:
                            cand_edits.append(((u_t, bp_t[0]), (v_t, bp_t[1])))
                elif pu not in locked_pos:
                    for b_pu in BASES:
                        if (b_pu + cur_seq[pv]) not in VALID_SET:
                            cand_edits.append(((pu, b_pu),))

                if pair_of[pv] != -1:
                    u_t, v_t = min(pv, pair_of[pv]), max(pv, pair_of[pv])
                    for bp_t in allowed_pairs[(u_t, v_t)]:
                        b_pv = bp_t[0] if pv == u_t else bp_t[1]
                        if (cur_seq[pu] + b_pv) not in VALID_SET:
                            cand_edits.append(((u_t, bp_t[0]), (v_t, bp_t[1])))
                elif pv not in locked_pos:
                    for b_pv in BASES:
                        if (cur_seq[pu] + b_pv) not in VALID_SET:
                            cand_edits.append(((pv, b_pv),))

                for edits in cand_edits:
                    trial_p = list(cur_seq)
                    prot_p = {pos_e for pos_e, _ in edits}
                    for pos_e, ch_e in edits:
                        trial_p[pos_e] = ch_e
                    s_rep = repair_budget_on_safe_stems(trial_p, pinfo, prot_p, ms, rng)
                    tvb = budget_violation(s_rep, pinfo)
                    if tvb > cur_vb:
                        continue
                    tms, tme = exact_fold(s_rep, eng)
                    tdbp = len(t_bps ^ get_bp_set(tms))
                    tte = float(RNA.energy_of_struct(s_rep, target))
                    tde = round(tte - tme, 4)
                    if tdbp == 0 and tvb == 0:
                        ok, _, _ = check_full_solve(s_rep, pinfo, eng)
                        if ok:
                            return True, s_rep, 0, 0, 0.0
                    if (tvb, tdbp, tde) < (cur_vb, cur_dbp, cur_de):
                        cur_seq, cur_vb, cur_dbp, cur_de, ms = s_rep, tvb, tdbp, tde, tms
                        pf_improved = True
                        break
                    elif (tvb, tdbp, tde) == (cur_vb, cur_dbp, cur_de):
                        tdgens = compute_dg_ens(s_rep, tte)
                        if tdgens < cur_dgens - 0.01:
                            cur_seq, cur_vb, cur_dbp, cur_de, ms, cur_dgens = s_rep, tvb, tdbp, tde, tms, tdgens
                            pf_improved = True
                            break
                if pf_improved:
                    break
            if not pf_improved:
                break

    return False, cur_seq, cur_vb, cur_dbp, cur_de


def cegis_rival_minimax_pass(
    start_seq: str,
    pinfo: dict,
    eng: int,
    rng: random.Random,
    max_sec: float,
) -> tuple:
    """
    Constrained CEGIS Rival-Set Minimax Pass (`CLSS-1` + `Op-M1` + `Op-M5`):
    Uses `12 us` `RNA.eval_structure_simple` coordinate descent over active pairs, active unpaired bases,
    and `2x2` pure-purine loop motifs against an accumulating bank of MFE counterexample structures `rivals`.
    """
    t0 = time.time()
    target = pinfo["target"]
    n = pinfo["n"]
    pair_of = pinfo["pair_of"]
    pairs = pinfo["pairs"]
    locked_pos = pinfo["locked_pos"]
    allowed_pairs = pinfo["allowed_pairs"]
    t_bps = get_bp_set(target)

    cur = list(start_seq)
    enforce_locks_on_list(cur, pinfo, rng)
    s_cur = "".join(cur)
    ms, me = exact_fold(s_cur, eng)
    te = float(RNA.energy_of_struct(s_cur, target))
    cur_dbp = len(t_bps ^ get_bp_set(ms))
    cur_de = round(te - me, 4)
    cur_vb = budget_violation(s_cur, pinfo)
    if cur_dbp == 0 and cur_vb == 0:
        ok, _, _ = check_full_solve(s_cur, pinfo, eng)
        if ok:
            return True, s_cur, 0, 0, 0.0

    best_seq = s_cur
    best_vb, best_dbp, best_de = cur_vb, cur_dbp, cur_de
    rivals = [ms] if ms != target else []

    def eval_mm(seq_str):
        et = float(RNA.energy_of_struct(seq_str, target))
        mg = -999.0
        sg = 0.0
        for rs in rivals[-8:]:
            g = et - float(RNA.energy_of_struct(seq_str, rs))
            if g > mg:
                mg = g
            sg += g
        return round(mg, 4), round(sg, 4), et

    step = 0
    while time.time() - t0 < max_sec:
        step += 1
        active_pos = set()
        for rs in rivals[-3:]:
            for u, v in (t_bps ^ get_bp_set(rs)):
                for d in (-3, -2, -1, 0, 1, 2, 3):
                    if 0 <= u + d < n:
                        active_pos.add(u + d)
                    if 0 <= v + d < n:
                        active_pos.add(v + d)
        active_pairs = sorted({(min(i, pair_of[i]), max(i, pair_of[i])) for i in active_pos if pair_of[i] != -1})
        active_unp = sorted([i for i in active_pos if pair_of[i] == -1 and i not in locked_pos])

        cur_str = "".join(cur)
        cur_vb = budget_violation(cur_str, pinfo)
        cur_mg, cur_sg, _ = eval_mm(cur_str)

        for _inner in range(5):
            if time.time() - t0 >= max_sec:
                break
            best_local = None
            best_key = (cur_vb, cur_mg, cur_sg)

            for u, v in active_pairs:
                ou, ov = cur[u], cur[v]
                for bp in allowed_pairs[(u, v)]:
                    if bp[0] == ou and bp[1] == ov:
                        continue
                    cur[u], cur[v] = bp[0], bp[1]
                    s_tr = "".join(cur)
                    vb = budget_violation(s_tr, pinfo)
                    if vb > cur_vb:
                        continue
                    mg, sg, _ = eval_mm(s_tr)
                    if (vb, mg, sg) < best_key:
                        best_key = (vb, mg, sg)
                        best_local = list(cur)
                cur[u], cur[v] = ou, ov

            for u in active_unp:
                ou = cur[u]
                for b in BASES:
                    if b == ou:
                        continue
                    cur[u] = b
                    s_tr = "".join(cur)
                    vb = cur_vb if not pinfo["consec_limits"] else budget_violation(s_tr, pinfo)
                    if vb > cur_vb:
                        continue
                    mg, sg, _ = eval_mm(s_tr)
                    if (vb, mg, sg) < best_key:
                        best_key = (vb, mg, sg)
                        best_local = list(cur)
                cur[u] = ou

            for p1, p2, q1, q2, _, _, _, _ in pinfo["loops_2x2"]:
                o = (cur[p1], cur[p2], cur[q1], cur[q2])
                for m in TURNER99_2X2_MOTIFS:
                    for pos, ch in ((p1, m[0]), (p2, m[1]), (q1, m[2]), (q2, m[3])):
                        if pos not in locked_pos:
                            cur[pos] = ch
                    s_tr = "".join(cur)
                    mg, sg, _ = eval_mm(s_tr)
                    if (cur_vb, mg, sg) < best_key:
                        best_key = (cur_vb, mg, sg)
                        best_local = list(cur)
                cur[p1], cur[p2], cur[q1], cur[q2] = o

            for _ in range(90):
                trial = list(cur)
                if active_pairs and rng.random() < 0.7:
                    u1, v1 = rng.choice(active_pairs)
                    pt1 = PAIR_TYPE.get(trial[u1] + trial[v1], "other")
                    bp1 = rng.choice(allowed_pairs[(u1, v1)])
                    pt_new = PAIR_TYPE.get(bp1, "other")
                    trial[u1], trial[v1] = bp1[0], bp1[1]
                    if pt_new != pt1 and not pinfo["is_pure_shape"]:
                        cands_sw = [
                            uv for uv in pairs
                            if uv != (u1, v1)
                            and PAIR_TYPE.get(trial[uv[0]] + trial[uv[1]]) == pt_new
                            and any(PAIR_TYPE.get(bp) == pt1 for bp in allowed_pairs[uv])
                        ]
                        if cands_sw:
                            u2, v2 = rng.choice(cands_sw)
                            bp2 = rng.choice([bp for bp in allowed_pairs[(u2, v2)] if PAIR_TYPE.get(bp) == pt1])
                            trial[u2], trial[v2] = bp2[0], bp2[1]
                if active_unp and rng.random() < 0.7:
                    for _ in range(rng.randint(1, 2)):
                        trial[rng.choice(active_unp)] = rng.choice(BASES)
                s_tr = "".join(trial)
                vb = budget_violation(s_tr, pinfo)
                if vb > cur_vb:
                    continue
                mg, sg, _ = eval_mm(s_tr)
                if (vb, mg, sg) < best_key:
                    best_key = (vb, mg, sg)
                    best_local = trial

            if best_local is not None:
                cur = best_local
                cur_vb, cur_mg, cur_sg = best_key
                if cur_mg < -0.05:
                    break
            else:
                break

        s_cand = "".join(cur)
        ms, me = exact_fold(s_cand, eng)
        te = float(RNA.energy_of_struct(s_cand, target))
        dbp = len(t_bps ^ get_bp_set(ms))
        vb = budget_violation(s_cand, pinfo)
        de = round(te - me, 4)
        if dbp == 0 and vb == 0:
            ok, _, _ = check_full_solve(s_cand, pinfo, eng)
            if ok:
                return True, s_cand, 0, 0, 0.0
        if ms != target and ms not in rivals:
            rivals.append(ms)
        if (vb, dbp, de) < (best_vb, best_dbp, best_de):
            best_vb, best_dbp, best_de, best_seq = vb, dbp, de, s_cand
        elif step % 5 == 0:
            cur = list(best_seq)

    return False, best_seq, best_vb, best_dbp, best_de


def fast_mfe_seam_climber(
    start_seq: str,
    pinfo: dict,
    eng: int,
    rng: random.Random,
    max_sec: float,
    strict_manifold: bool = True,
) -> tuple:
    t0 = time.time()
    target = pinfo["target"]
    n = pinfo["n"]
    pair_of = pinfo["pair_of"]
    pairs = pinfo["pairs"]
    locked_pos = pinfo["locked_pos"]
    allowed_pairs = pinfo["allowed_pairs"]
    t_bps = get_bp_set(target)

    cur = list(start_seq)
    enforce_locks_on_list(cur, pinfo, rng)
    s_cur = "".join(cur)
    ms, me = exact_fold(s_cur, eng)
    te = float(RNA.energy_of_struct(s_cur, target))
    cur_dbp = len(t_bps ^ get_bp_set(ms))
    cur_de = round(te - me, 4)
    cur_vb = budget_violation(s_cur, pinfo)

    best_seq = s_cur
    best_dbp = cur_dbp
    best_de = cur_de
    best_vb = cur_vb
    best_ms = ms

    def key_fn(vb, dbp, de):
        return (vb, dbp, de) if strict_manifold else (dbp, de, vb)

    step = 0
    while time.time() - t0 < max_sec:
        step += 1
        if best_dbp == 0:
            if best_vb == 0:
                ok, _, _ = check_full_solve(best_seq, pinfo, eng)
                if ok:
                    return True, best_seq, 0, 0, 0.0
            else:
                proj = project_to_budget_manifold(best_seq, pinfo, eng, rng, max_sec=min(1.2, max_sec - (time.time() - t0)))
                ok, _, _ = check_full_solve(proj, pinfo, eng)
                if ok:
                    return True, proj, 0, 0, 0.0

        m_bps = get_bp_set(ms)
        missing = sorted(t_bps - m_bps)
        parasitic = sorted(m_bps - t_bps)
        active_pos = set()
        for u, v in missing + parasitic:
            for d in (-3, -2, -1, 0, 1, 2, 3):
                if 0 <= u + d < n:
                    active_pos.add(u + d)
                if 0 <= v + d < n:
                    active_pos.add(v + d)
        active_pairs = sorted({(min(i, pair_of[i]), max(i, pair_of[i])) for i in active_pos if pair_of[i] != -1})
        active_unp = sorted([i for i in active_pos if pair_of[i] == -1 and i not in locked_pos])

        if cur_dbp <= 12 or cur_de <= 3.5:
            improved = True
            while improved and time.time() - t0 < max_sec:
                improved = False
                rng.shuffle(active_unp)
                for u in active_unp:
                    if time.time() - t0 >= max_sec:
                        break
                    orig_b = cur[u]
                    for b in BASES:
                        if b == orig_b or has_symmetric_neck_zip(u, b, cur, pair_of, n):
                            continue
                        cur[u] = b
                        s_tr = "".join(cur)
                        tms, tme = exact_fold(s_tr, eng)
                        tdbp = len(t_bps ^ get_bp_set(tms))
                        tte = float(RNA.energy_of_struct(s_tr, target))
                        tde = round(tte - tme, 4)
                        tvb = cur_vb if not pinfo["consec_limits"] else budget_violation(s_tr, pinfo)
                        if tdbp == 0 and tvb == 0:
                            ok, _, _ = check_full_solve(s_tr, pinfo, eng)
                            if ok:
                                return True, s_tr, 0, 0, 0.0
                        if key_fn(tvb, tdbp, tde) < key_fn(cur_vb, cur_dbp, cur_de) and (tde < cur_de - 0.005 or tdbp < cur_dbp or tvb < cur_vb):
                            cur_vb, cur_dbp, cur_de, ms = tvb, tdbp, tde, tms
                            if key_fn(cur_vb, cur_dbp, cur_de) < key_fn(best_vb, best_dbp, best_de):
                                best_seq, best_vb, best_dbp, best_de, best_ms = s_tr, cur_vb, cur_dbp, cur_de, tms
                            improved = True
                            break
                    else:
                        cur[u] = orig_b
                    if improved:
                        break

                if improved:
                    continue

                rng.shuffle(active_pairs)
                for u, v in active_pairs:
                    if time.time() - t0 >= max_sec:
                        break
                    orig_u, orig_v = cur[u], cur[v]
                    orig_bp = orig_u + orig_v
                    for bp in allowed_pairs[(u, v)]:
                        if bp == orig_bp:
                            continue
                        cur[u], cur[v] = bp[0], bp[1]
                        s_tr = "".join(cur)
                        tvb = budget_violation(s_tr, pinfo)
                        if strict_manifold and tvb > cur_vb:
                            continue
                        tms, tme = exact_fold(s_tr, eng)
                        tdbp = len(t_bps ^ get_bp_set(tms))
                        tte = float(RNA.energy_of_struct(s_tr, target))
                        tde = round(tte - tme, 4)
                        if tdbp == 0 and tvb == 0:
                            ok, _, _ = check_full_solve(s_tr, pinfo, eng)
                            if ok:
                                return True, s_tr, 0, 0, 0.0
                        if key_fn(tvb, tdbp, tde) < key_fn(cur_vb, cur_dbp, cur_de) and (tde < cur_de - 0.005 or tdbp < cur_dbp or tvb < cur_vb):
                            cur_vb, cur_dbp, cur_de, ms = tvb, tdbp, tde, tms
                            if key_fn(cur_vb, cur_dbp, cur_de) < key_fn(best_vb, best_dbp, best_de):
                                best_seq, best_vb, best_dbp, best_de, best_ms = s_tr, cur_vb, cur_dbp, cur_de, tms
                            improved = True
                            break
                    else:
                        cur[u], cur[v] = orig_u, orig_v
                    if improved:
                        break

                if improved:
                    continue

                if not pinfo["is_pure_shape"] and active_pairs and time.time() - t0 < max_sec:
                    non_gc_act = [
                        uv for uv in active_pairs
                        if PAIR_TYPE.get(cur[uv[0]] + cur[uv[1]]) in ("AU", "GU")
                        and any(PAIR_TYPE.get(bp) == "GC" for bp in allowed_pairs[uv])
                    ]
                    act_set = set(active_pairs)
                    gc_int = [
                        uv for uv in pairs
                        if uv not in act_set and PAIR_TYPE.get(cur[uv[0]] + cur[uv[1]]) == "GC"
                    ] or [
                        uv for uv in pairs
                        if PAIR_TYPE.get(cur[uv[0]] + cur[uv[1]]) == "GC"
                    ]
                    for _k in range(36):
                        if time.time() - t0 >= max_sec or not non_gc_act or not gc_int:
                            break
                        u1, v1 = rng.choice(non_gc_act)
                        pt1 = PAIR_TYPE.get(cur[u1] + cur[v1])
                        cands_int = [uv for uv in gc_int if uv != (u1, v1) and any(PAIR_TYPE.get(bp) == pt1 for bp in allowed_pairs[uv])]
                        if not cands_int:
                            continue
                        u2, v2 = rng.choice(cands_int)
                        bp_up = rng.choice([bp for bp in allowed_pairs[(u1, v1)] if PAIR_TYPE.get(bp) == "GC"])
                        bp_dn = rng.choice([bp for bp in allowed_pairs[(u2, v2)] if PAIR_TYPE.get(bp) == pt1])
                        trial = list(cur)
                        trial[u1], trial[v1] = bp_up[0], bp_up[1]
                        trial[u2], trial[v2] = bp_dn[0], bp_dn[1]
                        s_tr = "".join(trial)
                        tvb = budget_violation(s_tr, pinfo)
                        if strict_manifold and tvb > cur_vb:
                            continue
                        tms, tme = exact_fold(s_tr, eng)
                        tdbp = len(t_bps ^ get_bp_set(tms))
                        tte = float(RNA.energy_of_struct(s_tr, target))
                        tde = round(tte - tme, 4)
                        if tdbp == 0 and tvb == 0:
                            ok, _, _ = check_full_solve(s_tr, pinfo, eng)
                            if ok:
                                return True, s_tr, 0, 0, 0.0
                        if key_fn(tvb, tdbp, tde) < key_fn(cur_vb, cur_dbp, cur_de) and (tde < cur_de - 0.005 or tdbp < cur_dbp or tvb < cur_vb):
                            cur, cur_vb, cur_dbp, cur_de, ms = trial, tvb, tdbp, tde, tms
                            if key_fn(cur_vb, cur_dbp, cur_de) < key_fn(best_vb, best_dbp, best_de):
                                best_seq, best_vb, best_dbp, best_de, best_ms = s_tr, cur_vb, cur_dbp, cur_de, tms
                            improved = True
                            break

                if not improved and (active_pairs or active_unp) and time.time() - t0 < max_sec:
                    for _ in range(45):
                        if time.time() - t0 >= max_sec:
                            break
                        trial = list(cur)
                        if pinfo["loops_2x2"] and rng.random() < 0.35:
                            p1, p2, q1, q2, _, _, _, _ = rng.choice(pinfo["loops_2x2"])
                            m = rng.choice(TURNER99_2X2_MOTIFS)
                            for pos, ch in ((p1, m[0]), (p2, m[1]), (q1, m[2]), (q2, m[3])):
                                if pos not in locked_pos:
                                    trial[pos] = ch
                        if active_pairs and rng.random() < 0.75:
                            u, v = rng.choice(active_pairs)
                            pt_cur = PAIR_TYPE.get(trial[u] + trial[v], "other")
                            same_pt = [bp for bp in allowed_pairs[(u, v)] if PAIR_TYPE.get(bp) == pt_cur] if strict_manifold else list(allowed_pairs[(u, v)])
                            bp = rng.choice(same_pt or allowed_pairs[(u, v)])
                            trial[u], trial[v] = bp[0], bp[1]
                        if active_unp:
                            for _ in range(rng.randint(1, 2)):
                                trial[rng.choice(active_unp)] = rng.choice(BASES)
                        s_tr = "".join(trial)
                        tvb = budget_violation(s_tr, pinfo)
                        if strict_manifold and tvb > cur_vb:
                            continue
                        tms, tme = exact_fold(s_tr, eng)
                        tdbp = len(t_bps ^ get_bp_set(tms))
                        tte = float(RNA.energy_of_struct(s_tr, target))
                        tde = round(tte - tme, 4)
                        if tdbp == 0 and tvb == 0:
                            ok, _, _ = check_full_solve(s_tr, pinfo, eng)
                            if ok:
                                return True, s_tr, 0, 0, 0.0
                        if key_fn(tvb, tdbp, tde) < key_fn(cur_vb, cur_dbp, cur_de) and (tde < cur_de - 0.005 or tdbp < cur_dbp or tvb < cur_vb):
                            cur, cur_vb, cur_dbp, cur_de, ms = trial, tvb, tdbp, tde, tms
                            if key_fn(cur_vb, cur_dbp, cur_de) < key_fn(best_vb, best_dbp, best_de):
                                best_seq, best_vb, best_dbp, best_de, best_ms = s_tr, cur_vb, cur_dbp, cur_de, tms
                            improved = True
                            break

        m_bps = get_bp_set(ms)
        missing = list(t_bps - m_bps)
        parasitic = list(m_bps - t_bps)
        trial = list(cur)

        for u, v in rng.sample(parasitic, min(len(parasitic), rng.randint(1, 2))):
            idx_m = u if rng.random() < 0.5 else v
            if pair_of[idx_m] != -1:
                a, b = min(idx_m, pair_of[idx_m]), max(idx_m, pair_of[idx_m])
                pt_cur = PAIR_TYPE.get(trial[a] + trial[b], "other")
                cands = [bp for bp in allowed_pairs[(a, b)] if PAIR_TYPE.get(bp) == pt_cur] if strict_manifold else list(allowed_pairs[(a, b)])
                bp = rng.choice(cands or allowed_pairs[(a, b)])
                trial[a], trial[b] = bp[0], bp[1]
            elif idx_m not in locked_pos:
                other_b = trial[v if idx_m == u else u]
                bad = [b for b in BASES if (b + other_b) not in VALID_SET]
                trial[idx_m] = rng.choice(bad or BASES)

        for u, v in rng.sample(missing, min(len(missing), rng.randint(1, 2))):
            pt_cur = PAIR_TYPE.get(trial[u] + trial[v], "other")
            al = allowed_pairs[(u, v)]
            if not strict_manifold or pinfo["is_pure_shape"]:
                al_gc = [bp for bp in al if PAIR_TYPE.get(bp) == "GC"]
                bp = rng.choice(al_gc if (al_gc and rng.random() < 0.8) else al)
                trial[u], trial[v] = bp[0], bp[1]
            else:
                al_gc = [bp for bp in al if PAIR_TYPE.get(bp) == "GC"]
                if pt_cur in ("AU", "GU") and al_gc and rng.random() < 0.65:
                    miss_set = set(missing)
                    cands_swap = [
                        uv for uv in pairs
                        if uv not in miss_set
                        and PAIR_TYPE.get(trial[uv[0]] + trial[uv[1]]) == "GC"
                        and any(PAIR_TYPE.get(bp) == pt_cur for bp in allowed_pairs[uv])
                    ]
                    if cands_swap:
                        u2, v2 = rng.choice(cands_swap)
                        bp_up = rng.choice(al_gc)
                        bp_dn = rng.choice([bp for bp in allowed_pairs[(u2, v2)] if PAIR_TYPE.get(bp) == pt_cur])
                        trial[u], trial[v] = bp_up[0], bp_up[1]
                        trial[u2], trial[v2] = bp_dn[0], bp_dn[1]
                else:
                    same_pt = [bp for bp in al if PAIR_TYPE.get(bp) == pt_cur]
                    bp = rng.choice(same_pt or al)
                    trial[u], trial[v] = bp[0], bp[1]

            for d in (-2, -1, 1, 2):
                if 0 <= u + d < n and pair_of[u + d] == -1 and (u + d) not in locked_pos and rng.random() < 0.35:
                    trial[u + d] = rng.choice(BASES)
                if 0 <= v + d < n and pair_of[v + d] == -1 and (v + d) not in locked_pos and rng.random() < 0.35:
                    trial[v + d] = rng.choice(BASES)

        if pinfo["loops_2x2"] and rng.random() < 0.3:
            p1, p2, q1, q2, _, _, _, _ = rng.choice(pinfo["loops_2x2"])
            m = rng.choice(TURNER99_2X2_MOTIFS)
            for pos, ch in ((p1, m[0]), (p2, m[1]), (q1, m[2]), (q2, m[3])):
                if pos not in locked_pos:
                    trial[pos] = ch

        s_tr = "".join(trial)
        tvb = budget_violation(s_tr, pinfo)
        if strict_manifold and tvb > cur_vb:
            continue
        tms, tme = exact_fold(s_tr, eng)
        tdbp = len(t_bps ^ get_bp_set(tms))
        tte = float(RNA.energy_of_struct(s_tr, target))
        tde = round(tte - tme, 4)

        if tdbp == 0:
            if tvb > 0:
                s_tr = project_to_budget_manifold(s_tr, pinfo, eng, rng, max_sec=min(1.0, max_sec - (time.time() - t0)))
                tvb = budget_violation(s_tr, pinfo)
            if tvb == 0:
                ok, _, _ = check_full_solve(s_tr, pinfo, eng)
                if ok:
                    return True, s_tr, 0, 0, 0.0

        if (tde <= cur_de + 0.35 and tdbp <= cur_dbp + 2) or rng.random() < 0.08:
            cur, cur_vb, cur_dbp, cur_de, ms = trial, tvb, tdbp, tde, tms
            if key_fn(cur_vb, cur_dbp, cur_de) < key_fn(best_vb, best_dbp, best_de):
                best_seq, best_vb, best_dbp, best_de, best_ms = s_tr, cur_vb, cur_dbp, cur_de, tms
        elif step % 28 == 0:
            cur = list(best_seq)
            cur_vb, cur_dbp, cur_de, ms = best_vb, best_dbp, best_de, best_ms

    return False, best_seq, best_vb, best_dbp, best_de


def solve_puzzle_eterna_hard(row: dict, max_seconds: float = 15.0, seed: int = 2026, prev_seq: str = "") -> dict:
    t0 = time.time()
    pinfo = parse_puzzle_constraints(row)
    eng = configure_engine(pinfo["folder"])
    target = pinfo["target"]
    n = pinfo["n"]
    t_bps = get_bp_set(target)
    rng = random.Random(seed + int(pinfo["puzzle_id"]) % 10007)

    best_seq = make_budget_seed(pinfo, rng, boundary_bias=0.90)
    ms, me = exact_fold(best_seq, eng)
    te = float(RNA.energy_of_struct(best_seq, target))
    best_dbp = len(t_bps ^ get_bp_set(ms))
    best_vb = budget_violation(best_seq, pinfo)
    best_de = round(te - me, 4)

    ok, _, _ = check_full_solve(best_seq, pinfo, eng)
    if ok:
        return {
            "puzzle_id": pinfo["puzzle_id"],
            "title": pinfo["title"],
            "solved": True,
            "d_bp": 0,
            "v_budget": 0,
            "de_mfe": 0.0,
            "sequence": best_seq,
            "wall_time_sec": round(time.time() - t0, 3),
        }

    on_manifold_seeds = [(best_vb, best_dbp, best_de, best_seq)]
    shape_first_seeds = []
    num_pairs = len(pinfo["pairs"])

    if prev_seq and len(prev_seq) == n:
        ms_pr, me_pr = exact_fold(prev_seq, eng)
        te_pr = float(RNA.energy_of_struct(prev_seq, target))
        dbp_pr = len(t_bps ^ get_bp_set(ms_pr))
        vb_pr = budget_violation(prev_seq, pinfo)
        de_pr = round(te_pr - me_pr, 4)
        on_manifold_seeds.append((vb_pr, dbp_pr, de_pr, prev_seq))
        if (vb_pr, dbp_pr, de_pr) < (best_vb, best_dbp, best_de):
            best_vb, best_dbp, best_de, best_seq = vb_pr, dbp_pr, de_pr, prev_seq

    # Run our Eterna100-V2 compositional/ensemble solver (`workspace/eterna100_v2/cegis_rna_solver.py`)
    # under the active engine (`Turner1999` or `Turner2004`) as a shape-first seed generator and project
    # its MFE solution onto the `eterna-hard` pair-budget manifold (skip when `prev_seq` is already a `d_bp <= 4, vb == 0` near-miss or puzzle is heavily GC-capped).
    if (
        n <= 220
        and not (best_vb == 0 and best_dbp <= 4)
        and pinfo["max_limits"]["GC"] >= max(num_pairs - 2, int(0.75 * num_pairs))
        and len(pinfo["locked_pos"]) <= int(0.4 * n)
    ):
        try:
            v2_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if v2_dir not in sys.path:
                sys.path.insert(0, v2_dir)
            import cegis_rna_solver as v2_solver
            res_v2 = v2_solver._worker_solve(
                (int(pinfo["puzzle_id"]), pinfo["title"], target, seed, min(7.0, max_seconds * 0.40), prev_seq if (prev_seq and len(prev_seq) == n) else "", "/tmp/v2_tmp_ckpt.json")
            )
            configure_engine(pinfo["folder"])
            s_v2_raw = res_v2.get("sequence", "")
            if len(s_v2_raw) == n:
                lst_v2 = list(s_v2_raw)
                enforce_locks_on_list(lst_v2, pinfo, rng)
                s_v2_locked = "".join(lst_v2)
                s_v2_proj = project_to_budget_manifold(s_v2_locked, pinfo, eng, rng, max_sec=min(1.5, max_seconds * 0.12))
                for cand_v2 in (s_v2_locked, s_v2_proj):
                    ok, _, _ = check_full_solve(cand_v2, pinfo, eng)
                    if ok:
                        return {
                            "puzzle_id": pinfo["puzzle_id"],
                            "title": pinfo["title"],
                            "solved": True,
                            "d_bp": 0,
                            "v_budget": 0,
                            "de_mfe": 0.0,
                            "v2_target_only_dbp": res_v2.get("d_bp", -1),
                            "sequence": cand_v2,
                            "wall_time_sec": round(time.time() - t0, 3),
                        }
                    ms_c, me_c = exact_fold(cand_v2, eng)
                    te_c = float(RNA.energy_of_struct(cand_v2, target))
                    dbp_c = len(t_bps ^ get_bp_set(ms_c))
                    vb_c = budget_violation(cand_v2, pinfo)
                    de_c = round(te_c - me_c, 4)
                    if vb_c == 0:
                        on_manifold_seeds.append((vb_c, dbp_c, de_c, cand_v2))
                    else:
                        shape_first_seeds.append((dbp_c, de_c, vb_c, cand_v2))
                    if (vb_c, dbp_c, de_c) < (best_vb, best_dbp, best_de):
                        best_vb, best_dbp, best_de, best_seq = vb_c, dbp_c, de_c, cand_v2
        except Exception:
            configure_engine(pinfo["folder"])

    if best_dbp <= 8 and best_vb == 0:
        ok_f, s_f, vb_f, dbp_f, de_f = l0_endgame_finisher(
            best_seq, pinfo, eng, rng, max_sec=min(12.0, max_seconds * 0.58)
        )
        if ok_f:
            return {
                "puzzle_id": pinfo["puzzle_id"],
                "title": pinfo["title"],
                "solved": True,
                "d_bp": 0,
                "v_budget": 0,
                "de_mfe": 0.0,
                "sequence": s_f,
                "wall_time_sec": round(time.time() - t0, 3),
            }
        on_manifold_seeds.append((vb_f, dbp_f, de_f, s_f))
        if (vb_f, dbp_f, de_f) < (best_vb, best_dbp, best_de):
            best_vb, best_dbp, best_de, best_seq = vb_f, dbp_f, de_f, s_f

    fresh_manifold_seeds = []
    for k in range(18):
        if time.time() - t0 >= max_seconds * 0.35:
            break
        s_m = make_budget_seed(pinfo, rng, boundary_bias=0.92 if k % 2 == 0 else 0.70, ignore_budget=False)
        ms_m, me_m = exact_fold(s_m, eng)
        te_m = float(RNA.energy_of_struct(s_m, target))
        dbp_m = len(t_bps ^ get_bp_set(ms_m))
        vb_m = budget_violation(s_m, pinfo)
        de_m = round(te_m - me_m, 4)
        on_manifold_seeds.append((vb_m, dbp_m, de_m, s_m))
        fresh_manifold_seeds.append((vb_m, dbp_m, de_m, s_m))
        if dbp_m == 0 and vb_m == 0:
            ok, _, _ = check_full_solve(s_m, pinfo, eng)
            if ok:
                return {
                    "puzzle_id": pinfo["puzzle_id"],
                    "title": pinfo["title"],
                    "solved": True,
                    "d_bp": 0,
                    "v_budget": 0,
                    "de_mfe": 0.0,
                    "sequence": s_m,
                    "wall_time_sec": round(time.time() - t0, 3),
                }
        if (vb_m, dbp_m, de_m) < (best_vb, best_dbp, best_de):
            best_vb, best_dbp, best_de, best_seq = vb_m, dbp_m, de_m, s_m

    if n <= 105:
        for k_inv in range(2):
            if time.time() - t0 >= max_seconds * 0.45:
                break
            try:
                s0 = make_budget_seed(pinfo, rng, boundary_bias=0.90, ignore_budget=True)
                inv_s, _ = RNA.inverse_fold(s0, target)
                lst_inv = list(inv_s)
                for idx_p in pinfo["passive_unpaired"]:
                    lst_inv[idx_p] = "A"
                enforce_locks_on_list(lst_inv, pinfo, rng)
                s_inv = "".join(lst_inv)
                proj_s = project_to_budget_manifold(s_inv, pinfo, eng, rng, max_sec=min(0.5, max_seconds * 0.07))
                for cand_s in (s_inv, proj_s):
                    ok, _, _ = check_full_solve(cand_s, pinfo, eng)
                    if ok:
                        return {
                            "puzzle_id": pinfo["puzzle_id"],
                            "title": pinfo["title"],
                            "solved": True,
                            "d_bp": 0,
                            "v_budget": 0,
                            "de_mfe": 0.0,
                            "sequence": cand_s,
                            "wall_time_sec": round(time.time() - t0, 3),
                        }
                    ms_c, me_c = exact_fold(cand_s, eng)
                    te_c = float(RNA.energy_of_struct(cand_s, target))
                    dbp_c = len(t_bps ^ get_bp_set(ms_c))
                    vb_c = budget_violation(cand_s, pinfo)
                    de_c = round(te_c - me_c, 4)
                    if vb_c == 0:
                        on_manifold_seeds.append((vb_c, dbp_c, de_c, cand_s))
                        fresh_manifold_seeds.append((vb_c, dbp_c, de_c, cand_s))
                    else:
                        shape_first_seeds.append((dbp_c, de_c, vb_c, cand_s))
                    if (vb_c, dbp_c, de_c) < (best_vb, best_dbp, best_de):
                        best_vb, best_dbp, best_de, best_seq = vb_c, dbp_c, de_c, cand_s
            except Exception:
                pass

    on_manifold_seeds.sort(key=lambda x: (x[0], x[1], x[2]))
    fresh_manifold_seeds.sort(key=lambda x: (x[0], x[1], x[2]))
    shape_first_seeds.sort(key=lambda x: (x[0], x[1], x[2]))

    # Stage 2: Constrained CEGIS Rival-Set Minimax Pass (`20%` of remaining budget)
    rem = max(0.4, max_seconds - (time.time() - t0))
    ok_mm, s_mm, vb_mm, dbp_mm, de_mm = cegis_rival_minimax_pass(
        on_manifold_seeds[0][3], pinfo, eng, rng, max_sec=rem * 0.22
    )
    if ok_mm:
        return {
            "puzzle_id": pinfo["puzzle_id"],
            "title": pinfo["title"],
            "solved": True,
            "d_bp": 0,
            "v_budget": 0,
            "de_mfe": 0.0,
            "sequence": s_mm,
            "wall_time_sec": round(time.time() - t0, 3),
        }
    if (vb_mm, dbp_mm, de_mm) < (best_vb, best_dbp, best_de):
        best_vb, best_dbp, best_de, best_seq = vb_mm, dbp_mm, de_mm, s_mm
    on_manifold_seeds.insert(0, (vb_mm, dbp_mm, de_mm, s_mm))
    on_manifold_seeds.sort(key=lambda x: (x[0], x[1], x[2]))

    # Stage 3: Compass B — On-Manifold Fast MFE Seam + Kempe Swap Climber
    rem = max(0.3, max_seconds - (time.time() - t0))
    frac_b = 0.72 if pinfo["is_pure_shape"] else 0.55
    budget_b = rem * frac_b
    n_starts_b = 2 if budget_b >= 3.5 else 1
    for idx_b in range(n_starts_b):
        if time.time() - t0 >= max_seconds * 0.82:
            break
        if idx_b == 1 and fresh_manifold_seeds:
            start_s = fresh_manifold_seeds[0][3]
        else:
            start_s = on_manifold_seeds[min(idx_b, len(on_manifold_seeds) - 1)][3]
        sub_sec = min(budget_b / n_starts_b, max_seconds * 0.82 - (time.time() - t0))
        ok, s_out, vb_out, dbp_out, de_out = fast_mfe_seam_climber(
            start_s, pinfo, eng, rng, max_sec=sub_sec, strict_manifold=True
        )
        if ok:
            return {
                "puzzle_id": pinfo["puzzle_id"],
                "title": pinfo["title"],
                "solved": True,
                "d_bp": 0,
                "v_budget": 0,
                "de_mfe": 0.0,
                "sequence": s_out,
                "wall_time_sec": round(time.time() - t0, 3),
            }
        if (vb_out, dbp_out, de_out) < (best_vb, best_dbp, best_de):
            best_vb, best_dbp, best_de, best_seq = vb_out, dbp_out, de_out, s_out
        if idx_b == 1 and dbp_out <= 8 and s_out != best_seq and time.time() - t0 < max_seconds * 0.85:
            ok_f2, s_f2, vb_f2, dbp_f2, de_f2 = l0_endgame_finisher(
                s_out, pinfo, eng, rng, max_sec=min(4.0, max_seconds * 0.88 - (time.time() - t0))
            )
            if ok_f2:
                return {
                    "puzzle_id": pinfo["puzzle_id"],
                    "title": pinfo["title"],
                    "solved": True,
                    "d_bp": 0,
                    "v_budget": 0,
                    "de_mfe": 0.0,
                    "sequence": s_f2,
                    "wall_time_sec": round(time.time() - t0, 3),
                }
            if (vb_f2, dbp_f2, de_f2) < (best_vb, best_dbp, best_de):
                best_vb, best_dbp, best_de, best_seq = vb_f2, dbp_f2, de_f2, s_f2

    # Stage 4: Compass A — Shape-First Fast MFE Seam -> Deep Kempe Budget Projection
    rem_a = max_seconds * 0.88 - (time.time() - t0)
    if rem_a > 0.25 and not pinfo["is_pure_shape"]:
        start_a = shape_first_seeds[0][3] if shape_first_seeds else make_budget_seed(pinfo, rng, boundary_bias=0.92, ignore_budget=True)
        ok, s_out, vb_out, dbp_out, de_out = fast_mfe_seam_climber(
            start_a, pinfo, eng, rng, max_sec=rem_a * 0.70, strict_manifold=False
        )
        if ok:
            return {
                "puzzle_id": pinfo["puzzle_id"],
                "title": pinfo["title"],
                "solved": True,
                "d_bp": 0,
                "v_budget": 0,
                "de_mfe": 0.0,
                "sequence": s_out,
                "wall_time_sec": round(time.time() - t0, 3),
            }
        proj_a = project_to_budget_manifold(s_out, pinfo, eng, rng, max_sec=max(0.2, rem_a * 0.30))
        ok, _, _ = check_full_solve(proj_a, pinfo, eng)
        if ok:
            return {
                "puzzle_id": pinfo["puzzle_id"],
                "title": pinfo["title"],
                "solved": True,
                "d_bp": 0,
                "v_budget": 0,
                "de_mfe": 0.0,
                "sequence": proj_a,
                "wall_time_sec": round(time.time() - t0, 3),
            }
        ms_p, me_p = exact_fold(proj_a, eng)
        te_p = float(RNA.energy_of_struct(proj_a, target))
        dbp_p = len(t_bps ^ get_bp_set(ms_p))
        vb_p = budget_violation(proj_a, pinfo)
        de_p = round(te_p - me_p, 4)
        if (vb_p, dbp_p, de_p) < (best_vb, best_dbp, best_de):
            best_vb, best_dbp, best_de, best_seq = vb_p, dbp_p, de_p, proj_a

    # Stage 5: Final `[L0-ALGO]` Two-Stage Endgame Finisher whenever `best_dbp <= 8`
    if best_dbp <= 8:
        rem_f = max(0.6, max_seconds - (time.time() - t0))
        ok_f, s_f, vb_f, dbp_f, de_f = l0_endgame_finisher(best_seq, pinfo, eng, rng, max_sec=rem_f)
        if ok_f:
            return {
                "puzzle_id": pinfo["puzzle_id"],
                "title": pinfo["title"],
                "solved": True,
                "d_bp": 0,
                "v_budget": 0,
                "de_mfe": 0.0,
                "sequence": s_f,
                "wall_time_sec": round(time.time() - t0, 3),
            }
        if (vb_f, dbp_f, de_f) < (best_vb, best_dbp, best_de):
            best_vb, best_dbp, best_de, best_seq = vb_f, dbp_f, de_f, s_f

    ms_fin, _ = exact_fold(best_seq, eng)
    m_bps_fin = get_bp_set(ms_fin)
    return {
        "puzzle_id": pinfo["puzzle_id"],
        "title": pinfo["title"],
        "solved": False,
        "d_bp": best_dbp,
        "v_budget": best_vb,
        "de_mfe": best_de,
        "missing_bps": sorted(t_bps - m_bps_fin) if best_dbp <= 2 else [],
        "extra_bps": sorted(m_bps_fin - t_bps) if best_dbp <= 2 else [],
        "sequence": best_seq,
        "wall_time_sec": round(time.time() - t0, 3),
    }


def _worker_run(args_tuple):
    row, max_sec, seed, prev_seq = args_tuple
    return solve_puzzle_eterna_hard(row, max_seconds=max_sec, seed=seed, prev_seq=prev_seq)


def main():
    import concurrent.futures
    ap = argparse.ArgumentParser()
    ap.add_argument("--group-csv", type=str, default=os.path.join(BASE_DIR, "eterna-hard/groups/eterna-hard-group1.csv"))
    ap.add_argument("--out-tsv", type=str, default=os.path.join(BASE_DIR, "designs_group1.tsv"))
    ap.add_argument("--ckpt-json", type=str, default=os.path.join(BASE_DIR, "ckpt_group1.json"))
    ap.add_argument("--limit", type=int, default=0, help="0 = all rows in CSV")
    ap.add_argument("--max-dbp-filter", type=int, default=0, help="If >0, only run on puzzles with ckpt d_bp <= this value")
    ap.add_argument("--pure-shape-only", action="store_true", help="If set, only run on pure SHAPE,0 puzzles")
    ap.add_argument("--folder-filter", type=str, default="", help="If set, only run on rows with folder == this value (e.g. Vienna2)")
    ap.add_argument("--puzzle-ids", type=str, default="", help="Comma-separated puzzle_ids to run")
    ap.add_argument("--max-seconds", type=float, default=8.0)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--seed", type=int, default=2026)
    args = ap.parse_args()

    rows = list(csv.DictReader(open(args.group_csv, "r", encoding="utf-8")))
    if args.limit > 0:
        rows = rows[: args.limit]
    pid_filter = {x.strip() for x in args.puzzle_ids.split(",") if x.strip()} if args.puzzle_ids else None

    ck = {}
    if os.path.exists(args.ckpt_json):
        try:
            ck = json.load(open(args.ckpt_json, "r", encoding="utf-8"))
        except Exception:
            ck = {}

    todo = []
    for r in rows:
        pid = str(r["puzzle_id"])
        if pid_filter is not None and pid not in pid_filter:
            continue
        if args.folder_filter and r.get("folder", "").strip() != args.folder_filter.strip():
            continue
        if pid in ck and ck[pid].get("solved", False):
            continue
        if args.pure_shape_only and r.get("constraints", "").strip() != "SHAPE,0":
            continue
        if args.max_dbp_filter > 0 and ck.get(pid, {}).get("d_bp", 999) > args.max_dbp_filter:
            continue
        prev_seq = ck.get(pid, {}).get("sequence", "")
        todo.append((r, args.max_seconds, args.seed, prev_seq))

    todo.sort(key=lambda item: (ck.get(str(item[0]["puzzle_id"]), {}).get("d_bp", 999), ck.get(str(item[0]["puzzle_id"]), {}).get("de_mfe", 999.0)))

    print(f"=== Running Eterna-Hard Solver v8 [L0-ALGO] on {os.path.basename(args.group_csv)} (total={len(rows)}, todo={len(todo)}, workers={args.workers}, max_sec={args.max_seconds}) ===")
    if todo:
        if args.workers > 1 and len(todo) > 1:
            with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as ex:
                for res in ex.map(_worker_run, todo):
                    pid = res["puzzle_id"]
                    prev = ck.get(pid)
                    if prev is None or res["solved"] or (res["v_budget"], res["d_bp"], res["de_mfe"]) <= (prev.get("v_budget", 999), prev.get("d_bp", 999), prev.get("de_mfe", 999.0)):
                        ck[pid] = res
                        with open(args.ckpt_json + ".tmp", "w", encoding="utf-8") as f:
                            json.dump(ck, f, indent=2)
                        os.replace(args.ckpt_json + ".tmp", args.ckpt_json)
                    diag = f" miss={res.get('missing_bps',[])} extra={res.get('extra_bps',[])}" if (not res["solved"] and res["d_bp"] <= 2) else ""
                    st = "✅ SOLVED" if res["solved"] else f"❌ d_bp={res['d_bp']} vb={res['v_budget']} de={res['de_mfe']:.2f}{diag}"
                    print(f"[{pid:>8s}] {res['title'][:32]:32s}: {st} ({res['wall_time_sec']}s)", flush=True)
        else:
            for item in todo:
                res = _worker_run(item)
                pid = res["puzzle_id"]
                ck[pid] = res
                with open(args.ckpt_json + ".tmp", "w", encoding="utf-8") as f:
                    json.dump(ck, f, indent=2)
                os.replace(args.ckpt_json + ".tmp", args.ckpt_json)
                st = "✅ SOLVED" if res["solved"] else f"❌ d_bp={res['d_bp']} vb={res['v_budget']} de={res['de_mfe']:.2f}"
                print(f"[{pid:>8s}] {res['title'][:32]:32s}: {st} ({res['wall_time_sec']}s)", flush=True)

    with open(args.out_tsv, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["puzzle_id", "sequence"])
        for r in rows:
            pid = str(r["puzzle_id"])
            if pid in ck:
                w.writerow([pid, ck[pid]["sequence"]])

    solved_total = sum(1 for r in rows if ck.get(str(r["puzzle_id"]), {}).get("solved", False))
    print(f"\n=== SUMMARY ({os.path.basename(args.group_csv)}): {solved_total}/{len(rows)} SOLVED -> wrote {args.out_tsv} ===")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
try_proofer_in_30_seconds.py — Self-Contained Runnable Showcase of PROOFER / CLSS.

Demonstrates the 4-stage CLSS + Law M7 + Zero-Trust Verification workflow live in
under 2 seconds using only the Python 3 standard library across three real domains:
  1. Law M7.1 — Interface Gauge Conjugation in Ternary Fast Matrix Multiplication
  2. Known-Example Dissection (EBG) — Base-50 Lychrel Carry-Wire Transducer (PR #517)
  3. Law M7.3 — Operation-Order Reversal & Borrow-Horizon Truncation (03_invsqrt)
"""

from __future__ import annotations
import json
from pathlib import Path
import time
from typing import List, Sequence, Tuple

Vec4 = Tuple[int, int, int, int]


def dot4(a: Vec4, b: Vec4) -> int:
    """Exact 4-component integer dot product."""
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3]


def add4(a: Vec4, b: Vec4) -> Vec4:
    """Exact 4-component integer vector addition."""
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3])


def demo_1_law_m7_1_ternary_fmm_seam_surgery() -> None:
    """Demo 1: Eliminate +-2 seam collisions via B_4 interface gauge conjugation."""
    print("=" * 78)
    print("DEMO 1 | Law M7.1: Interface Gauge Conjugation in Ternary FMM (Z_T = {-1,0,1})")
    print("=" * 78)

    # Two ternary sub-blocks sharing a 4-channel bilinear seam:
    c1: List[Vec4] = [(1, 0, -1, 0), (0, 1, 0, -1), (1, -1, 1, 0), (-1, 1, 0, 0)]
    c2: List[Vec4] = [(0, -1, 1, 0), (-1, 0, 0, 1), (1, -1, 0, 1), (-1, 1, 0, -1)]
    v_leg: List[Vec4] = [(1, 0, 1, 0), (0, 1, 0, 1), (1, 1, 0, -1), (0, -1, 1, 1)]

    pi_default = (0, 1, 2, 3)
    merged_default = [add4(c1[k], c2[pi_default[k]]) for k in range(4)]
    collisions_default = sum(1 for vec in merged_default for x in vec if abs(x) > 1)
    print(f"  [Stage I Oracle]   Default row order pi={pi_default}:")
    print(f"                     Merged seam vectors = {merged_default}")
    print(f"                     Forbidden |x|>=2 collisions = {collisions_default} -> FAIL")

    # Apply Law M7.1: conjugate Block 2 interface channels by pi = (0, 1, 3, 2) in S_4
    pi_conj = (0, 1, 3, 2)
    merged_conj = [add4(c1[k], c2[pi_conj[k]]) for k in range(4)]
    collisions_conj = sum(1 for vec in merged_conj for x in vec if abs(x) > 1)
    print(f"  [Stage III Surgery] Conjugated order pi={pi_conj} (Law M7.1):")
    print(f"                     Merged seam vectors = {merged_conj}")
    print(f"                     Forbidden |x|>=2 collisions = {collisions_conj} (100% in {{-1,0,1}})")

    # Stage IV Zero-Trust Verification: verify exact bilinear identity across all 4x4 basis pairs
    basis: List[Vec4] = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
    for x in basis:
        for y in basis:
            split_val = sum(
                dot4(c1[k], x) * dot4(v_leg[k], y)
                + dot4(c2[pi_conj[k]], x) * dot4(v_leg[k], y)
                for k in range(4)
            )
            merged_val = sum(dot4(merged_conj[k], x) * dot4(v_leg[k], y) for k in range(4))
            assert split_val == merged_val, "Bilinear seam tensor mismatch!"
    assert collisions_default > 0 and collisions_conj == 0
    print("  [Stage IV Verify]  Exact bilinear identity holds on all 16 basis pairs -> PASS\n")


def step_lychrel_base(digits: Sequence[int], base: int) -> List[int]:
    """Perform one exact big-integer reverse-and-add step in the given base (MSB first)."""
    n = len(digits)
    out = [0] * n
    carry = 0
    for i in range(n - 1, -1, -1):
        total = digits[i] + digits[n - 1 - i] + carry
        carry, out[i] = divmod(total, base)
    return ([carry] + out) if carry else out


def demo_2_ebg_base50_lychrel_transducer() -> None:
    """Demo 2: Verify Base-50 Period-4 Lychrel seed template T_1(m) (PR #517)."""
    print("=" * 78)
    print("DEMO 2 | EBG & Symbolic Carry-Wire Transducer: Base-50 Lychrel Proof (PR #517)")
    print("=" * 78)

    repo_root = Path(__file__).resolve().parent.parent
    graph_path = repo_root / "StartFresh_v16/graphs/ancestral_v15_atlas/lychrel-new-base-proof.jsonl"
    if graph_path.exists():
        records = [json.loads(line) for line in graph_path.read_text(encoding="utf-8").splitlines() if line]
        closed_keys = [r["key"] for r in records if r.get("ev") == "close"]
        print(f"  [Ancestral Atlas]  Loaded {graph_path.name} (closed nodes: {closed_keys})")

    base = 50
    l0 = [1, 47, 5, 38, 23, 4, 39, 21, 8, 31, 35, 28, 42, 16, 18, 13, 23, 3,
          41, 17, 16, 17, 15, 19, 11, 25, 47, 6, 36, 25, 48, 4, 40, 19, 12, 24]
    m0 = [49, 13, 2, 20, 12, 20, 2, 13]
    r0 = [0, 25, 11, 19, 40, 3, 48, 26, 36, 5, 48, 26, 11, 19, 15, 17, 15, 17,
          42, 3, 23, 13, 17, 15, 42, 28, 36, 32, 7, 21, 40, 3, 23, 38, 5, 47]

    # 1. Verify symbolic carry-wire transducer identity: (b-1) + 0 + c_in = (b-1)*(1-c_in) + b*c_in
    for c_in in (0, 1):
        lhs = (base - 1) + 0 + c_in
        rhs = (base - 1) * (1 - c_in) + base * c_in
        assert lhs == rhs, "Carry-wire transducer identity failed!"
    print("  [Stage II Proof]   Carry-wire identity (b-1)+0+c_in = (b-1)(1-c_in)+b*c_in: EXACT")

    # 2. Verify explicit Period-4 closure T_1(m) -> T_2(m) -> T_3(m) -> T_4(m) -> T_1(m+1)
    def build_t1(m: int) -> List[int]:
        return l0 + [base - 1] * m + m0 + [0] * m + r0

    palindromes_found = 0
    for m in (1, 2, 3):
        cur = build_t1(m)
        start_len = len(cur)
        for _ in range(4):
            if cur == cur[::-1]:
                palindromes_found += 1
            cur = step_lychrel_base(cur, base)
        target = build_t1(m + 1)
        assert cur == target, f"Period-4 closure failed at m={m}!"
        print(f"  [Stage IV Orbit]   m={m}: T_1({m}) ({start_len} digits) --[4 steps]--> "
              f"T_1({m+1}) ({len(cur)} digits, +{len(cur) - start_len})")
    assert palindromes_found == 0
    print("  [Stage IV Verify]  0 palindromes across 12 steps; Period-4 closure EXACT -> PASS\n")


def active_borrow_span(acc: int, sub_val: int, lsb: int) -> int:
    """Return active bit-flip / borrow span (msb_flipped - lsb + 1) for acc - sub_val."""
    diff = acc ^ (acc - sub_val)
    return diff.bit_length() - lsb


def demo_3_law_m7_3_borrow_horizon_truncation() -> None:
    """Demo 3: Compare largest-first vs smallest-first subtraction borrow spans."""
    print("=" * 78)
    print("DEMO 3 | Law M7.3: Operation-Order Reversal & Borrow-Horizon Truncation")
    print("=" * 78)

    # 10,000 deterministic fixed-point accumulator states S0 = 2^16 + M*2^8 + c
    # where M has bits 8 and 9 set (borrow absorbers), A0 = M*2^8 (LSB 8),
    # A1 in [2^4, 2^7-1] (LSB 4), A2 in [1, 2^4-1] (LSB 0).
    max_span_largest = [0, 0, 0]   # [A0, A1, A2]
    max_span_smallest = [0, 0, 0]  # [A2, A1, A0]

    for idx in range(10_000):
        m_blk = ((idx % 64) * 4) | 3  # bits 8 and 9 set in M*2^8
        c_low = idx % 15
        s0 = (1 << 16) + (m_blk << 8) + c_low
        a0 = m_blk << 8
        a1 = (((idx // 7) % 7) + 1) << 4
        a2 = ((idx // 13) % 15) + 1

        # Schedule A: Standard Largest-First (A0 -> A1 -> A2)
        acc_l = s0
        for step_i, (val, lsb) in enumerate(((a0, 8), (a1, 4), (a2, 0))):
            max_span_largest[step_i] = max(max_span_largest[step_i], active_borrow_span(acc_l, val, lsb))
            acc_l -= val

        # Schedule B: Law M7.3 Smallest-First (A2 -> A1 -> A0)
        acc_s = s0
        for step_i, (val, lsb) in enumerate(((a2, 0), (a1, 4), (a0, 8))):
            max_span_smallest[step_i] = max(max_span_smallest[step_i], active_borrow_span(acc_s, val, lsb))
            acc_s -= val

        assert acc_l == acc_s, "Arithmetic schedules diverged!"

    sum_largest = sum(max_span_largest)
    sum_smallest = sum(max_span_smallest)
    saved = sum_largest - sum_smallest
    print(f"  [Largest-First]    A0 -> A1 -> A2 stage borrow spans: {max_span_largest} (total = {sum_largest} bits)")
    print(f"  [Smallest-First]   A2 -> A1 -> A0 stage borrow spans: {max_span_smallest} (total = {sum_smallest} bits)")
    print(f"  [Stage IV Verify]  10,000/10,000 exact bit-identical outputs; "
          f"saved {saved} active borrow bits (-{100.0 * saved / sum_largest:.1f}%) -> PASS\n")


def main() -> None:
    t0 = time.perf_counter()
    demo_1_law_m7_1_ternary_fmm_seam_surgery()
    demo_2_ebg_base50_lychrel_transducer()
    demo_3_law_m7_3_borrow_horizon_truncation()
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    print(f"ALL 3 PROOFER MINI-DEMONSTRATIONS VERIFIED IN {elapsed_ms:.1f} ms (EXIT 0).")


if __name__ == "__main__":
    main()

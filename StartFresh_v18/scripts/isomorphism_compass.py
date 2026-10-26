#!/usr/bin/env python3
"""
isomorphism_compass.py — Cross-Domain Isomorphism Compass (StartFresh v16 / Laws M1-M7).

Maps structural obstacles on a new open problem to the 8 Canonical Obstruction
Archetypes, the Seven Laws of Meta-Generalization (M1-M7), and the 22 ancestral
reasoning graphs in `StartFresh_v16/graphs/ancestral_v15_atlas/*.jsonl`.

Usage:
  python3 StartFresh_v16/scripts/isomorphism_compass.py --list
  python3 StartFresh_v16/scripts/isomorphism_compass.py "boundary collision"
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
from typing import Dict, List, Sequence, Tuple

ARCHETYPES: List[Dict[str, object]] = [
    {
        "id": "flat_oracle_plateau",
        "title": "Flat 0/1 Decision Plateau (Zero Proximity Gradient)",
        "symptoms": "Binary PASS/FAIL oracle; random or local search sees 0% hit rate;flat plateau.",
        "laws": ["Law M1 (Continuous Violation Energy E_viol)", "Known-Example Dissection (EBG)"],
        "prescription": "Replace binary oracle with continuous violation energy E_viol(x) >= 0 or dissect a solved small-parameter family into symbolic transducer invariants.",
        "graphs": ["lychrel-new-base-proof.jsonl (H1_CARRY_WIRE_DECOUPLING)", "vnncomp-2026-unsolved-instance-counterexample.jsonl"],
        "keywords": ["flat", "plateau", "binary", "oracle", "gradient", "0/1", "lychrel", "counterexample", "ebg"],
    },
    {
        "id": "slow_or_noisy_evaluator",
        "title": "Slow (>10 ms) or Noisy Monte Carlo Evaluator Bottleneck",
        "symptoms": "Inner-loop evaluation takes >10 ms or uses stochastic simulation; hill-climbing stalls.",
        "laws": ["Law M2 (Fast Zeta SOS-DP / Spectral / Rank-1 Delta Transform)"],
        "prescription": "Precompute exact incremental rank-1 delta updates, SOS-DP lookup tables, or closed-form cycle-index weights before running search.",
        "graphs": ["minimizer-density-record-tables.jsonl (L-MDRT-001)", "ame-states-open-cells-huber-table.jsonl (L-ASOC-005)"],
        "keywords": ["slow", "noisy", "monte", "carlo", "evaluator", "ms", "bottleneck", "sos", "spectral", "delta"],
    },
    {
        "id": "block_seam_collision",
        "title": "Block Seam Collision / Boundary Coefficient Overflow",
        "symptoms": "Gluing locally optimal sub-blocks creates +-2 boundary collisions, carry leaks, or subfield traps.",
        "laws": ["Law M7.1 (Joint Interface Gauge Group G_12 / Chiral Seam Surgery)"],
        "prescription": "Act on the shared boundary interface by the joint gauge group G_12 = Stab(B1) x Stab(B2) (signed permutations B_2k or diagonal subfield gauges).",
        "graphs": ["fmm-ternary-integer-ring-upgrade.jsonl (L1320_CONJ, L-FTIR-002)", "ame-states-open-cells-huber-table.jsonl (L-ASOC-005)"],
        "keywords": ["boundary", "collision", "seam", "block", "gluing", "+-2", "ternary", "interface", "gauge", "conjugation"],
    },
    {
        "id": "stage2_bottleneck_from_single_seed",
        "title": "Stage-2 Compression Stall from Cloning a Single Stage-1 Winner",
        "symptoms": "Optimizing Stage 2 on top of a single frozen Stage-1 winner hits an irreducible floor.",
        "laws": ["Law M7.2 (Solution-Fiber Scan & Cross-Fiber Hybridization)"],
        "prescription": "Enumerate the full equivalence fiber E_1 = {x : f_1(x) = c_1*} and splice orthogonal row/column blocks across distinct fiber representatives.",
        "graphs": ["fmm-additive-complexity-records.jsonl (L-FACR-002)", "fmm-ternary-integer-ring-upgrade.jsonl (L1320_SEAM56)"],
        "keywords": ["stage2", "stage-2", "single", "seed", "winner", "clone", "fiber", "hybridization", "compression"],
    },
    {
        "id": "forward_greedy_cse_or_ripple_stall",
        "title": "Forward Greedy CSE Stall or Wide Borrow/Carry Ripple Horizon",
        "symptoms": "Syntactic pair-merging stalls without algebraic cancellation; largest-first subtraction triggers wide ripples.",
        "laws": ["Law M7.3 (Tellegen W^T Dual Transposition + Over-Provision-then-Cancel + Smallest-First Order)"],
        "prescription": "Transpose linear forms (W -> W^T), allow temporary signed expansion before cancellation, or reverse operation order to smallest-first (A2 -> A1 -> A0).",
        "graphs": ["fmm-additive-complexity-records.jsonl (L-FACR-001, L-FACR-003)", "romeo-guided-circuit-compilation.jsonl"],
        "keywords": ["forward", "greedy", "cse", "ripple", "borrow", "carry", "transpose", "tellegen", "order", "smallest-first"],
    },
    {
        "id": "single_localized_defect",
        "title": "Single Localized Defect in a 98%-Valid Global Structure",
        "symptoms": "25/26 blocks or 99% of constraints pass, but 1 localized colliding pair or tail blocks completion.",
        "laws": ["Law M7.4 (Surgical Defect Fission / Rank-1 Patching)"],
        "prescription": "Freeze the 98% valid core and apply a localized rank-1 or 5-to-6 fission patch strictly on the defective coordinate pair.",
        "graphs": ["fmm-ternary-integer-ring-upgrade.jsonl (L-FTIR-003)", "fmm-smirnov-general-rank-bounds.jsonl"],
        "keywords": ["single", "localized", "defect", "one", "pair", "tail", "fission", "patch", "98%", "obstruction"],
    },
    {
        "id": "combinatorial_symmetry_explosion",
        "title": "Combinatorial Symmetry Explosion in Discrete Search",
        "symptoms": "Search space grows exponentially (2^N or N!) with large automorphism group G.",
        "laws": ["Law M3 (Algebraic Quotient / Necklace / Voltage-Graph Lift)"],
        "prescription": "Quotient the search space by a cyclic, dihedral, or metacirculant group G so every candidate automatically satisfies symmetry constraints.",
        "graphs": ["degree-diameter-table.jsonl", "covering-designs-record.jsonl", "unit-distance-graphs-upper-bounds.jsonl"],
        "keywords": ["symmetry", "combinatorial", "explosion", "quotient", "cayley", "voltage", "circulant", "automorphism"],
    },
    {
        "id": "coupled_global_constraints",
        "title": "Monolithic MILP / SA Stall on Coupled Multi-Resource Assignments",
        "symptoms": "Full-instance MILP times out and 1-swap SA gets trapped by tightly coupled capacity/roster constraints.",
        "laws": ["Law M5 (Exact Micro-Solver Subset LNS / Ruin-and-Recreate)"],
        "prescription": "Embed an exact micro-MILP or SAT solver inside LNS, ruining and re-solving coupled k-element neighborhoods in 50-300 ms.",
        "graphs": ["ihtp-ihtc2024-upper-bounds.jsonl", "ccd-binary-gupta-nanoalloys-38-55.jsonl", "strip-packing-benchmarks.jsonl"],
        "keywords": ["coupled", "global", "milp", "lns", "nurse", "roster", "schedule", "packing", "subset"],
    },
]


def load_atlas_summary(atlas_dir: Path) -> List[Tuple[str, int, int, int, List[str]]]:
    """Return (filename, total_nodes, kill_or_dead_count, close_count, sample_transitions) per graph."""
    rows: List[Tuple[str, int, int, int, List[str]]] = []
    for path in sorted(atlas_dir.glob("*.jsonl")):
        nodes = kills = closes = 0
        dead_keys: List[str] = []
        close_keys: List[str] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            ev = rec.get("ev", "")
            if ev == "node":
                nodes += 1
                if rec.get("type") == "dead":
                    kills += 1
                    dead_keys.append(str(rec.get("key", "")))
            elif ev == "kill":
                kills += 1
                dead_keys.append(str(rec.get("key", "")))
            elif ev == "close":
                closes += 1
                close_keys.append(str(rec.get("key", "")))
        transitions = [f"{d} -> {c}" for d, c in zip(dead_keys[:2], close_keys[:2])]
        rows.append((path.name, nodes, kills, closes, transitions))
    return rows


def print_overview(atlas_dir: Path) -> None:
    """Print summary of all 22 ancestral .jsonl graphs and 8 Canonical Obstruction Archetypes."""
    rows = load_atlas_summary(atlas_dir)
    total_nodes = sum(r[1] for r in rows)
    total_kills = sum(r[2] for r in rows)
    total_closes = sum(r[3] for r in rows)
    print("=" * 82)
    print(f"ANCESTRAL v15 ATLAS SUMMARY ({len(rows)} reasoning graphs | "
          f"{total_nodes} nodes | {total_kills} kills/dead | {total_closes} closes)")
    print("=" * 82)
    for name, nodes, kills, closes, trans in rows:
        t_str = f" | e.g. {', '.join(trans)}" if trans else ""
        print(f"  {name:<50} nodes={nodes:<3} kill={kills:<2} close={closes:<2}{t_str}")

    print("\n" + "=" * 82)
    print("8 CANONICAL OBSTRUCTION ARCHETYPES (LAWS M1-M7 COMPASS)")
    print("=" * 82)
    for idx, arch in enumerate(ARCHETYPES, 1):
        laws_str = ", ".join(arch["laws"])  # type: ignore[arg-type]
        print(f"  [{idx}] {arch['id']} — {arch['title']}")
        print(f"      Laws  : {laws_str}")
        print(f"      Graphs: {', '.join(arch['graphs'])}\n")  # type: ignore[arg-type]


def query_compass(atlas_dir: Path, query: str) -> None:
    """Rank archetypes and scan ancestral .jsonl nodes matching the search query."""
    tokens = [t for t in re.split(r"[^a-z0-9+-]+", query.lower()) if t]
    scored: List[Tuple[int, Dict[str, object]]] = []
    for arch in ARCHETYPES:
        haystack = " ".join([
            str(arch["id"]), str(arch["title"]), str(arch["symptoms"]),
            " ".join(arch["laws"]), str(arch["prescription"]), " ".join(arch["keywords"]),  # type: ignore[arg-type]
        ]).lower()
        score = sum(3 if tok in arch["keywords"] else (1 if tok in haystack else 0) for tok in tokens)  # type: ignore[operator]
        if score > 0:
            scored.append((score, arch))
    scored.sort(key=lambda item: item[0], reverse=True)

    print("=" * 82)
    print(f"ISOMORPHISM COMPASS QUERY: '{query}'")
    print("=" * 82)
    for rank, (score, arch) in enumerate((scored or [(0, ARCHETYPES[0])])[:3], 1):
        print(f"\nMatch #{rank} (score={score}): [{arch['id']}] {arch['title']}")
        print(f"  Symptoms    : {arch['symptoms']}")
        print(f"  Laws M1-M7  : {', '.join(arch['laws'])}")  # type: ignore[arg-type]
        print(f"  Prescription: {arch['prescription']}")
        print(f"  Atlas Nodes : {', '.join(arch['graphs'])}")  # type: ignore[arg-type]


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Cross-Domain Isomorphism Compass (Laws M1-M7).")
    parser.add_argument("query", nargs="*", help="Obstacle description (e.g. 'boundary collision').")
    parser.add_argument("--list", action="store_true", help="List all 22 graphs and 8 archetypes.")
    args = parser.parse_args(argv)

    atlas_dir = Path(__file__).resolve().parent.parent / "graphs" / "ancestral_v15_atlas"
    if args.list or not args.query:
        print_overview(atlas_dir)
    else:
        query_compass(atlas_dir, " ".join(args.query))


if __name__ == "__main__":
    main()

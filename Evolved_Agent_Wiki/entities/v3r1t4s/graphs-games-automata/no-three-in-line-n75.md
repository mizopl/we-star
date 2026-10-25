---
id: v3r1t4s-no-three-in-line-n75
type: entity
tags: [v3r1t4s, v3r1t4s/graphs-games-automata, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: graphs-games-automata
kind: harvest
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# No-three-in-line: 150 points on the 75x75 grid (smallest open n)

# Overview

> Bank id `no-three-in-line-n75` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Place 2n points on the n x n integer grid with no three collinear, for n = 75. n = 75 is the only n <= 76 with no known solution. Also, any 2n-point configuration for n >= 77 would be a new largest-known record. This is Ben Green's open problem #72 (formal-conjectures GreensOpenProblems/72.lean), which asks whether 2n is impossible for all large n. Guy and Kelly (1968) conjectured that only about c*n points are possible for large n, with c = (2*pi^2/3)^(1/3) ~ 1.874, later corrected by Guy to c = pi/sqrt(3) ~ 1.814. Both are below 2, so the expected answer to Green's question is yes (2n eventually becomes impossible); this says nothing definite about n = 75.

## Success criterion

(1) Exactly 150 distinct integer points (x,y) with 0 <= x,y <= 74 (which forces exactly 2 per row and per column). (2) Zero collinear triples, checked exactly with integer arithmetic by two independent methods. (3) At claim time, a fresh fetch of the live primary table https://wwwhomes.uni-bielefeld.de/achim/no3in/readme.html (and its tabular summary) shows no n=75 entry, and the readme's 'last update' timestamp is recorded in the report (2026-09-11 13:40 UTC+2 on 2026-10-03). (4) The live EinsteinArena 75x75 leaderboard (https://einsteinarena.com/problems/no-three-in-line-75; best 148 points on 2026-10-03), the OssaBellator issues and a fresh search at verification time show no 150-point solution. If an n=75 solution was posted by anyone before the claim, the result is downgraded to 'independent solution' and not claimed. Variant, under the same rules (direction: max over n): 2n points in [0,n-1]^2 with no three collinear for some n STRICTLY GREATER than the largest n with a solution on the live readme at verification time (76 on 2026-10-03, so n = 77 or more). Near-misses, solutions for n already listed, and UNSAT results within a single symmetry class are not a success.

## Partial wins

- {"id": "p1", "statement": "A DRAT/LRAT-certified UNSAT proof (checked by drat-trim or cake_lpr, encoding re-derived independently) that n = 75 has no 150-point solution within a stated symmetry class not previously ruled out in Flammenkamp's notes, arXiv 2602.07751, arXiv 2609.25133 or the OssaBellator issues."}
- {"id": "p2", "statement": "A 2n-point no-three-in-line solution for some n <= 76 in a symmetry class that Flammenkamp's live page does not list for that n, verified exactly."}
- {"id": "p3", "statement": "A 150-point configuration in [0,74]^2 with strictly fewer collinear triples than the best reported in OssaBellator issues #42/#43 (or any newer public report) at verification time, not obtained by cropping or perturbing the n=76 solution; counted exactly."}
- {"id": "p4", "statement": "A 149-point no-three-in-line set in [0,74]^2, verified exhaustively by two methods, strictly larger than the live EinsteinArena 75x75 best at verification time (148 points, Prellberg, on 2026-10-03), and not already posted on the arena, the Bielefeld page or the OssaBellator issues."}

## Verification

For each point P, compute the reduced direction (dx/g, dy/g) with sign normalization to every other point. If any direction repeats for the same P, three points are collinear. That is O(N^2) with exact integer arithmetic. Cross-check with a brute-force O(N^3) determinant test (N=150 gives about 551k triples, which is trivial). Assert there are no duplicate points and all coordinates are in range. Re-fetch the Bielefeld readme and its table and the EinsteinArena 75x75 leaderboard, and record the readme 'last update' timestamp and the arena best with fetch times.

## Angles

- Enumerate which symmetry classes are even possible for odd n = 75 (center point and center lines). The listed odd-n solutions are in class 'rct4'. Run a SAT encoding (pysat with cadical153 or kissat via pip) restricted to every class, including the low-symmetry ones Heule may have skipped, with at-most-2-per-line cardinality constraints (sequential-counter or totalizer encodings).
- Local repair from neighbours: crop or descend the n=76 rot4 solution and the n=74 and n=73 solutions. Formulate repair as an exact max-SAT over a growing window. Exactly 2 points are needed in every row and column, which is a strong propagation constraint.
- Cube-and-conquer on 10 cores: split on the row-pair patterns of the first few rows under symmetry, then solve the cubes in parallel.
- Learn a generative prior from the 431k stored configurations (row-gap statistics and slope usage), and use it as a branching heuristic in a custom bitset DFS.
- Algebraic seeds: modular-parabola constructions (points (x, x^2 mod p)) give about 1.5n points. Use them as partial assignments and complete with SAT.
- SAT on symmetry-orbit variables, using the symmetry class Heule used for odd n = 71 and 73 ('rct4' per the DB; check Flammenkamp's class definitions for which classes odd n allows). Encode exactly-2 per row and column plus at-most-2 on every grid line with >= 3 lattice points. Use pysat (pip install python-sat, bundles CaDiCaL), or compile kissat/CaDiCaL from source with clang.
- Cube-and-conquer across 10 cores: split on the placements in the middle rows and columns, and run a portfolio of symmetry classes (rot2, rot4, rct4, dia2) with different seeds.
- Pattern transfer: download the n=73, 74 and 76 solutions from the DB, study their orbit structure (e.g., closeness to conic-arc constructions like Hall et al.'s modular conics), and feed them as phase hints or soft assumptions for n=75.
- Large-neighbourhood search: tabu/min-conflicts over orbit representatives with incremental collinear-triple counts. Freeze most of a near-solution and hand the remaining window to SAT.
- Precompute every line through >= 3 grid points (primitive directions with |a|,|b| <= 37) once. Reduce the lines modulo the symmetry group so each orbit of lines becomes a single cardinality constraint.
- Before starting, re-fetch the Bielefeld readme; Heule posts monthly and may already have n = 75.
- Copy the symmetry class that worked for odd n. The 2026 odd solutions (71, 73) are in class rct4, so impose it on n=75, which divides the variables by about 4. Encode as SAT with pysat/CaDiCaL: one variable per orbit, exactly-2 per row and column, at-most-2 per line. Use cardinality encodings (sequential counters) and lines grouped by slope.
- Line pruning: only lines through at least 3 grid points matter, so precompute them and drop symmetric duplicates.
- Use cube-and-conquer on the 10 cores. Split on the placements in the first few rows (or orbit representatives) and run parallel CaDiCaL instances.
- Warm-start by local search (WalkSAT-style on constraint violations) from n=73 or 76 solutions embedded or trimmed, then hand the near-solution to SAT with assumptions.

## Pitfalls

- Floating-point collinearity tests. Use exact integers only.
- Grid-size off-by-one: n = 75 means coordinates 0..74.
- Only lines with 3+ grid points matter, but all slopes must be checked, including steep rational ones.
- Others, including Heule, Prellberg and several AI-agent repositories, are actively attacking n=75. Re-check the database immediately before claiming.
- Boards cropped or perturbed from n=76 are provably maximal at 148 points, so local single-point repair cannot succeed. Issue #43 documents this dead end.
- n=75 is on Epoch AI's FrontierMath open-problem list, so many AI-agent attempts are underway. Duplicate discovery on the same day is plausible.
- Claiming an n that is already in the DB (74 and 76 are solved).
- Off-by-one between 0-based and 1-based coordinates.
- Checking only small slopes, or using floating-point slopes.
- Picking a symmetry class that is invalid for odd n (centre-point issues), which wastes the whole run.
- Reporting a solver timeout as evidence of nonexistence.
- Heule may post n=75 any day; a solution found after the DB lists 75 is not a record.
- Using a symmetry class (e.g. rot4 with a fixed centre cell) that forces a centre point or an odd row count incompatible with exactly-2-per-row for odd n; check Flammenkamp's class table before encoding.
- Only checking horizontal, vertical and diagonal lines. All rational slopes must be checked.
- Heule needed substantial SAT compute for these cases, so a one-day laptop attempt may well fail. Report partial progress (e.g. 149 points) as a partial result only.
- Odd-n symmetry classes differ from even ones (center point issues).
- Mis-crediting: the readme credits n = 70, 71, 72, 73 and 76 to Heule (SAT, Jun-Aug 2026) and n = 74 to Prellberg (Jul 2026). Do not repeat older claims that Prellberg's GPU runs covered n = 49-76.

## Sources

- https://wwwhomes.uni-bielefeld.de/achim/no3in/readme.html
- https://github.com/OssaBellator/no-three-in-line-research
- https://arxiv.org/html/2602.07751
- https://wwwhomes.uni-bielefeld.de/achim/no3in/Prellberg_Sep_2025.pdf
- https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/GreensOpenProblems/72.lean
- https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf
- https://einsteinarena.com/
- https://github.com/jmsung/einstein
- https://einsteinarena.com/problems/no-three-in-line-75
- Status source: https://wwwhomes.uni-bielefeld.de/achim/no3in/readme.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/graphs-games-automata/no-three-in-line-n75.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `no-three-in-line-n75`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Graphs, games and automata]]
- [[V3R1T4S]]

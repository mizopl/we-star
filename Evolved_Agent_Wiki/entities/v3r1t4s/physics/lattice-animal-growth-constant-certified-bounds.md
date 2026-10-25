---
id: v3r1t4s-lattice-animal-growth-constant-certified-bounds
type: entity
tags: [v3r1t4s, v3r1t4s/physics, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: physics
kind: standard
tractability: 2
compute: "laptop-days"
disclosure: open
status_checked: "2026-10-15"
---
# Growth constants of lattice animals: a certified bound beating lambda_2 in [4.00253, 4.5252] for polyominoes or lambda_3 in [6.6799, 9.3835] for polycubes

# Overview

> Bank id `lattice-animal-growth-constant-certified-bounds` · standard · tractability 2 · laptop-days · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Site lattice animals on Z^d grow like lambda_d^n. For polyominoes (d = 2) Iwan Jensen's series estimate is lambda_2 = 4.0625696(5); the best rigorous bounds are lambda_2 > 4.00253 (Gill Barequet, Gunter Rote and Mira Shalah, CACM 59(7) 2016: twisted cylinders of width 27, a 450 GB eigenvector certificate computed on a 256 GiB server) and lambda_2 < 4.5252 (Barequet and Shalah, Algorithmica 84 (2022) 3559-3586, arXiv 1906.11447, improving Klarner-Rivest's 1973 4.6496), both as listed on Wikipedia's 'Polyomino' page (checked 2026-10-15). For polycubes (d = 3) the estimate is about 8.34; bounds are lambda_3 >= 6.6799 (Matan Mamistvalov, Technion M.Sc. 2022, recursive compositions; Barequet, Ben-Shachar and Osegueda, EuroCG 2020, had 6.6521/6.6621) and lambda_3 <= 9.3835 (Barequet-Shalah 2022). The polycube lower bounds used counts up to about n = 19; A001931 now runs to n = 22 (Stanley Dodds 2023, Phillip Thompson 2024), so the cheapest realistic win is a better lambda_3 lower bound from the longer exact data or a 3D twisted-prism transfer matrix. The lambda_2 lower bound needs width 28 and is out of laptop reach.

## Success criterion

Success means a rigorous bound on lambda_2 or lambda_3 strictly better (lower bound larger, or upper bound smaller) than the best published value found when the Wikipedia Polyomino page and an arXiv/Google Scholar search are re-checked immediately before claiming, by at least 1e-4, with a machine-checkable certificate: either an exact-integer recursion (all inputs being published exact counts, e.g. A001931 b-file values) plus a proof of the composition inequality used, or a transfer-matrix eigenvalue certificate verified with exact or outward-rounded interval arithmetic (Collatz-Wielandt).

## Partial wins

- {"id": "p1", "statement": "A certified improvement of a published lower bound on the polycube growth constant lambda_d for some d in 4..9 (Barequet-Ben-Shachar-Osegueda EuroCG 2020 Table 3, e.g. d = 4: 9.7714) using longer exact counts (A151830-A151835) or a sharper composition inequality, same certificate rules."}
- {"id": "p2", "statement": "A certified improvement of a published bound on the growth constant of polyiamonds or polyhexes (Barequet, Shalah and Zheng 2017 lower bound 2.8424 for polyiamonds; the improved polyiamond upper bound on Gunter Rote's publication page), citing the current best value with its source."}

## Verification

Skeptic (< 1 hour for recursion certificates; transfer-matrix certificates may need longer): recompute the recursion in exact integer arithmetic from the live A001931 b-file and check the claimed bound; for eigenvector certificates, rebuild the automaton independently for a small width and check the certificate format, then check the claimed width's ratios with outward rounding.

## Angles

- Rerun the recursive-composition bound for polycubes with the three extra exact terms A001931(20..22); recursions of this type gain noticeably with each new exact term.
- Twisted prisms: the 2D twisted-cylinder transfer matrix generalises to 3D animals on a twisted prism of small cross-section; even tiny cross-sections may beat 6.6799 since the 2D analogue beat concatenation bounds by a wide margin.
- From automata theory: Barequet-Shalah's upper bound is a twig-language growth rate; minimising the automaton and using larger twig alphabets is a standard state-space trade-off.
- From statistical physics: the gap between 6.68 and the estimate 8.34 is large, so even crude Kesten-style bridge or strip-decomposition bounds imported from self-avoiding walks may help.

## Pitfalls

- Estimates (Jensen's 4.0625696, series for lambda_3) are not bounds; only certified inequalities count.
- Several close bounds circulate for lambda_3 (6.6521, 6.6621, 6.6799); compare against the largest one found, with source.
- Fixed vs free animals: growth constants are the same, but recursions must use fixed counts (A001931, A001168), not free counts.
- Floating-point eigenvalues of a transfer matrix are not certificates; the Collatz-Wielandt ratios must be checked with outward rounding.

## Sources

- https://en.wikipedia.org/wiki/Polyomino
- https://arxiv.org/abs/1906.11447
- https://page.mi.fu-berlin.de/rote/Papers/pdf/Lambda-4.pdf
- https://www1.pub.informatik.uni-wuerzburg.de/eurocg2020/data/uploads/papers/eurocg20_paper_23.pdf
- https://www.cs.technion.ac.il/events/view-event.php?evid=10245
- https://oeis.org/A001931
- https://oeis.org/A001168
- Status source: https://en.wikipedia.org/wiki/Polyomino

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/lattice-animal-growth-constant-certified-bounds.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `lattice-animal-growth-constant-certified-bounds`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]

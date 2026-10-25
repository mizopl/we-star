---
id: v3r1t4s-hard-core-entropy-square-honeycomb-digits
type: entity
tags: [v3r1t4s, v3r1t4s/physics, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: physics
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Hard-core lattice gas at unit activity: more correct digits of the hard-square entropy constant (OEIS A085850) or the honeycomb constant than Baxter's corner-transfer-matrix values

# Overview

> Bank id `hard-core-entropy-square-honeycomb-digits` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The hard-square entropy constant kappa (partition function per site of the nearest-neighbour-exclusion lattice gas on the square lattice at activity z = 1; equivalently the growth rate per cell of n x n 0/1 matrices with no two adjacent 1s) was computed by Rodney Baxter (arXiv cond-mat/9811264; Annals of Combinatorics 3 (1999) 191-203) with the corner transfer matrix (CTM) method as kappa = 1.5030480824753322643220663294755536893857810, 43 decimals, with the remark that the last two or three digits should be treated with caution. OEIS A085850 (keyword 'more', last edited 2026-05-30, checked 2026-10-15) still holds only Baxter's digits. In the same paper Baxter gives the honeycomb-lattice constant 1.54644070878756141848902270530472278026 (38 decimals); that constant has no OEIS entry (search checked 2026-10-15). Rigorous digits are far fewer: Friedland, Lundow and Markström certified 15 digits of kappa, and Kai Liang (arXiv 2507.04007, 2025) gives tensor-network bounds agreeing to 26 decimals, partly resting on empirical convergence patterns. At z = 1 the model is far from its critical activity (about 3.796), so CTM and boundary-MPS iterations converge exponentially; Baxter's 1998 runs used small truncations (honeycomb continued to n = 20). Arbitrary-precision CTM on a laptop should reach well past 43 digits. A win adds digits to a numerical constant; it is not a proof of those digits unless the partial-win certificate route is used.

## Success criterion

Success means a decimal value of the square-lattice constant kappa (or the honeycomb constant) with D correct-looking decimals where D >= (longest published digit string for that constant, re-fetched live immediately before claiming: OEIS A085850 DATA plus any b-file for kappa; Baxter's 38 decimals for honeycomb) + 5, AND (a) two computations by independent methods (for example CTM at two different truncation sizes run to a fixed point, and a separate transfer-matrix or VUMPS/boundary-MPS calculation with Richardson-type extrapolation) agree on all D decimals, (b) both agree with the first 40 published decimals of kappa (36 for honeycomb), (c) the run logs show the claimed digits stable over at least the last three increases of truncation, and (d) an arXiv/Google Scholar/OEIS search finds no published value with D or more decimals. Direction: more digits. Disagreement with Baxter's flagged last two or three digits is allowed but must be stated explicitly.

## Partial wins

- {"id": "p1", "statement": "A rigorous enclosure of kappa certifying at least 20 correct decimals (beyond the 15 certified by Friedland, Lundow and Markström), from Calkin-Wilf / Friedland-Peled transfer-matrix inequalities evaluated with exact rational or interval arithmetic, shipped with the eigenvalue certificates (Collatz-Wielandt vectors) so a skeptic can recheck the inequalities exactly."}
- {"id": "p2", "statement": "At least 20 decimals, by two independent methods, of the hard-core (z = 1) entropy constant of the 4-8-8 lattice (Steven Finch, Errata and Addenda to Mathematical Constants, arXiv 2001.00578, Section 5.12, quotes only 1.54956010...) or of the 'triangular Kagome' lattice that Finch reports as still open; the lattice definition must match Finch's cited source."}
- {"id": "p3", "statement": "Independent reproduction of Baxter's 43 decimals of kappa to at least 48 decimals that settles whether his last two or three digits are correct, reported either as confirmation or as a documented correction."}

## Verification

Skeptic (< 1 hour): run the claimant's CTM code at two truncation sizes in arbitrary precision (mpmath or python-flint arb, working precision at least D + 20 digits) and confirm the digit string is stable; run the second-method code (transfer matrix on strips of width up to ~24 with Fibonacci-sized state space, or VUMPS) and compare; check the first 40 decimals against A085850 fetched live; for p1, recheck each eigenvalue inequality exactly with the supplied integer/rational vectors.

## Angles

- Re-run Baxter's CTM variational equations (cond-mat/9811264, eqs. 9-14) in arbitrary precision with truncation n up to 40-80; at z = 1 the corner-matrix spectrum decays fast, so each extra block of kept states should add digits geometrically.
- From quantum many-body physics: treat the row-to-row transfer matrix as a matrix-product operator and find its fixed point with VUMPS or a boundary-MPS power method in high precision; this is a genuinely different algorithm from CTM and gives the second method the criterion needs.
- From numerical analysis: exact strip free energies f_L for widths L <= 24 (state count is the Fibonacci number F(L+2), about 1.2e5 at L = 24) converge exponentially to the bulk value; apply Richardson/Levin-type sequence acceleration in mpmath and compare with CTM.
- From computational number theory: once 60+ digits exist, run PSLQ/LLL against algebraic and simple transcendental bases (the hard-hexagon constant is algebraic, Baxter's square value is not known to be); a null result at stated height is a free side observation, not a win.
- For p1, port the Friedland-Peled inequality (cylinder and torus transfer matrices) to exact arithmetic: the certificates are integer vectors whose Collatz-Wielandt ratios bound the spectral radius from both sides.

## Pitfalls

- Baxter flagged his last two or three decimals as uncertain; matching them proves nothing and differing from them is not automatically an error. Validate against the first 40 decimals only.
- Plateau trap: successive CTM truncations can agree for a few steps before drifting; 'stable digits' must survive several further truncation increases and match an independent method.
- Double-precision linear algebra caps agreement at about 15-16 digits; any claim beyond that from float64 eigen-solvers is noise.
- Normalisation: kappa is the partition function per site, ln(kappa) is the entropy; the honeycomb constant is per site, not per two-site unit cell. Mixing these produces a different number that can look new.
- A085850 carries keyword 'more' and also falls under the bank's generic OEIS 'more' target; a claim belongs here only if it meets this entry's two-method rule.

## Sources

- https://arxiv.org/abs/cond-mat/9811264
- https://oeis.org/A085850
- https://arxiv.org/abs/2507.04007
- https://arxiv.org/abs/math/9810155
- https://arxiv.org/abs/2001.00578
- https://mathworld.wolfram.com/HardSquareEntropyConstant.html
- Status source: https://oeis.org/A085850

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/hard-core-entropy-square-honeycomb-digits.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `hard-core-entropy-square-honeycomb-digits`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]

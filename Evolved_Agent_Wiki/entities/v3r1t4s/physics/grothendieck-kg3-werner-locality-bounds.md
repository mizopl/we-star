---
id: v3r1t4s-grothendieck-kg3-werner-locality-bounds
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
tractability: 1.5
compute: "laptop-days"
disclosure: open
status_checked: "2026-10-15"
---
# Grothendieck constant of order 3 / two-qubit Werner nonlocality threshold: improve 1.43670 <= K_G(3) <= 1.4546

# Overview

> Bank id `grothendieck-kg3-werner-locality-bounds` · standard · tractability 1.5 · laptop-days · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

For two-qubit Werner states v|psi-><psi-| + (1-v)I/4 under projective measurements, Acin, Gisin and Toner (2006) showed the locality threshold is v_c = 1/K_G(3), where K_G(3) is Grothendieck's constant of order 3. Sebastien Designolle, Gabriele Iommazzo, Mathieu Besancon, Sebastian Knebel, Patrick Gelss and Sebastian Pokutta (arXiv:2302.04721, PRR 2023) used Frank-Wolfe algorithms (Julia package BellPolytopes.jl) to give analytic bounds 0.6875 <= v_c <= 0.6961, i.e. 1.4367 <= K_G(3) <= 1.4546, improving Hirsch, Quintino, Vertesi, Navascues and Brunner (2017, v_c >= 0.6829) and Diviansky, Bene and Vertesi (2017, v_c <= 0.6964). Designolle, Vertesi and Pokutta (arXiv:2409.03739, v3 Feb 2026) raised the lower bound to K_G(3) >= 1.43670 with a 97 x 97 Bell-type matrix whose local bound they certified by solving a binary quadratic program. Real and complex K_G (unbounded order) are being attacked heavily in 2026 (e.g. arXiv:2610.10477), but order 3 has not moved since. Via the projective-measurement simulation of qubit POVMs, 2302.04721 also derives v_POVM >= (2/3) * 0.6875 ~ 0.4583 for general POVMs.

## Success criterion

Success means EITHER (a) a real matrix M (m1 x m2) with unit vectors x_i, y_j in R^3 such that Q = sum M_ij <x_i,y_j> divided by the exact local bound L = max over a in {+-1}^m1, b in {+-1}^m2 of sum M_ij a_i b_j gives Q/L STRICTLY GREATER (direction: max) than the best published lower bound on K_G(3) (1.43670 from arXiv:2409.03739 on 2026-10-15; re-fetched live immediately before claiming, including a search for newer papers) by at least 1e-5, with M rational (or rounded to rationals with Q recomputed in exact or interval arithmetic) and L certified exactly; OR (b) an explicit local hidden-variable model for all projective measurements on the Werner state at visibility v STRICTLY GREATER than 0.6875 by at least 1e-5 (equivalently K_G(3) < 1.4546 - margin), given as an inscribed polyhedron with exactly computed shrinking factor and a rational convex-decomposition certificate that the skeptic checks in exact arithmetic.

## Partial wins

- {"id": "p1", "statement": "A certified improvement of a lower bound on K_G(d) for some d in 4..9 over the values tabulated in arXiv:2409.03739 (Table 2), same certification rules."}
- {"id": "p2", "statement": "A certified local bound for one of the 2409.03739 'heuristic' symmetric instances (d in {4,7,8}) that turns their heuristic value into a proven bound, re-checkable in under an hour by an independent exact method."}

## Verification

(a) Recompute Q from the posted vectors in mpmath (or exactly if algebraic); compute L exactly: if min(m1,m2) <= 34, enumerate all sign vectors of the smaller side (Gray code, the other side's optimum is the sum of absolute values) in a few CPU-hours; otherwise require a branch-and-bound certificate re-run with an open exact solver (e.g. SCIP exact or a custom bound with symmetry) that agrees, plus a second independent run. (b) Check the polyhedron's shrinking factor eta exactly (rational/algebraic computation of inradius over circumradius of the vertex set), solve the LP feasibility of the local model in exact rationals (or verify a posted rational weight vector), and recompute v = eta^2 * nu * v0 as in 2302.04721 Eq. 4. Compare with the live arXiv values.

## Angles

- Rectangular instances with a small side: choose m1 <= 32 measurement directions for one party (highly symmetric, e.g. icosahedral/600-cell-derived) and many for the other, so the local bound is exhaustively checkable while Frank-Wolfe optimises M.
- Import from spherical design theory: use spherical t-designs and good spherical codes on S^2 (Womersley, Hardin-Sloane, Cohn's tables) as measurement sets; the shrinking factor eta of the local-model polytope is a covering-radius quantity, so better coverings give better upper bounds on K_G(3).
- Import from combinatorial optimisation: the local bound is a MaxCut-type QUBO; exact solvers with SDP bounds (BiqCrunch, BiqBin-style) plus symmetry reduction may certify larger instances than Gurobi-based runs.
- Import from crystallography: orbit-based measurement sets under the full icosahedral group reduce both the QUBO and the LP to orbit variables (cf. the 600-cell instance analysed in 2409.03739).
- Run BellPolytopes.jl longer with larger m on the upper-bound (local-model) side, which the 2023 paper ran with m = 406.

## Pitfalls

- Heuristic local bounds: a QUBO value found by a heuristic solver is only a lower estimate of L and gives an INVALID K_G lower bound; L must be certified exact.
- Floating-point quantum values: Q/L must be recomputed in exact or interval arithmetic; rounding M can change both Q and L.
- Order matters: K_G(3) bounds are not K_G (unbounded order, ~1.78) or the complex constant; papers from 2026 on those do not change the order-3 bar.
- Werner conventions: some papers use p vs v, or include POVMs (a different threshold); compare like with like.
- Margins below 1e-5 are within rounding of published values and are not wins.

## Sources

- https://arxiv.org/abs/2409.03739
- https://arxiv.org/abs/2302.04721
- https://arxiv.org/abs/1609.06114
- https://github.com/ZIB-IOL/BellPolytopes.jl
- https://arxiv.org/abs/2610.10477
- Status source: https://arxiv.org/abs/2409.03739

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/grothendieck-kg3-werner-locality-bounds.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `grothendieck-kg3-werner-locality-bounds`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]

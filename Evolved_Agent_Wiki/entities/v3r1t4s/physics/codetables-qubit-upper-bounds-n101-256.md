---
id: v3r1t4s-codetables-qubit-upper-bounds-n101-256
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
# Qubit stabilizer codes n = 101..256: lower a weak UPPER bound in Grassl's codetables.de qubit table with an exact LP/shadow certificate

# Overview

> Bank id `codetables-qubit-upper-bounds-n101-256` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Since 24 May 2024 codetables.de lists bounds on the minimum distance of qubit stabilizer codes \[\[n,k,d\]\] up to n = 256 (Markus Grassl). The page notes say most upper bounds for n <= 100 come from Eric Rains' MAGMA linear-programming program, while for n > 100 'the upper bounds on qubit codes are weak (and not necessarily monotone in k)'. Spot checks on 2026-10-15: \[\[101,1\]\] 23-34, \[\[150,1\]\] 33-51, \[\[200,1\]\] 39-67, \[\[256,1\]\] 50-86, \[\[200,20\]\] 34-59, \[\[256,60\]\] 35-63; several of these equal or sit near the self-dual shadow bound 2*floor(n/6)+2, suggesting the full quantum LP with shadow constraints (Rains 1999; Ashikhmin-Litsyn) has not been run above n = 100. Lower-bound improvements in the qubit table are covered by another entry's partial win; this target is upper bounds only.

## Success criterion

Success means, for some qubit cell (n,k) with 101 <= n <= 256, a proof that no \[\[n,k,d\]\] stabilizer code exists for d equal to the live table upper bound (https://codetables.de/QECC.php?q=4&n=<n>&k=<k>, re-fetched live immediately before claiming), thereby lowering it by at least 1 (direction: min upper bound), where the proof is an exact rational infeasibility certificate (Farkas dual) of the quantum weight-enumerator LP (stabilizer and normalizer enumerators linked by the quaternary MacWilliams identity, A_i <= B_i, A_i = B_i for 0 < i < d, nonnegativity, plus shadow-enumerator nonnegativity where used), checked in exact integer arithmetic by an independent script; and the new bound is NOT already implied by applying the standard propagation rules (d(n,k) <= d(n,k-1) for k >= 2, d(n,k) <= d(n+1,k), d(n,k) <= d(n-1,k+1)+1 or as stated by the table) to other live cells.

## Partial wins

- {"id": "p1", "statement": "A monotonicity repair list: every cell where the live upper bounds violate the standard propagation rules, with the corrected implied bound; useful to maintainers but not a new bound (report as audit)."}
- {"id": "p2", "statement": "An exact LP certificate lowering an upper bound for some cell with n <= 100 (where Rains' program was used), which would indicate the earlier computation missed constraints."}

## Verification

Independent exact checker in Python integers/fractions: build Krawtchouk polynomials K_j(i) for q = 4 and length n (exact big integers), the LP variables A_0..A_n (stabilizer) and B_0..B_n (normalizer) with A_0 = B_0 = 1 and B(x,y) = 2^{-(n-k)} A(x+3y, x-y) (quaternary MacWilliams identity as in Calderbank-Rains-Shor-Sloane, quant-ph/9608006), the constraints for distance d, and verify that the posted dual vector y satisfies y^T M >= 0 componentwise with y^T b < 0 (Farkas). Runs in seconds for n <= 256. Recompute propagation-implied bounds from the live table for the neighbouring cells.

## Angles

- Solve the quantum LP in exact rational arithmetic (SoPlex exact mode, or floating LP then rational reconstruction and exact verification of the dual) for every n = 101..256 and k, binary-searching d; this is the obvious first sweep.
- Add shadow-enumerator constraints (Rains) and the split weight enumerators for k > 0; impure-code subtleties are handled by the A_i <= B_i structure.
- Import from classical coding theory: the Delsarte LP for quaternary additive codes with Schrijver-type SDP strengthening (semidefinite three-point bounds) can beat the LP; feasible for n up to a few dozen, so use it to test whether LP-only results are tight near n = 101.
- Import from numerical analysis: Krawtchouk values reach 4^256; use exact integers or scaled orthogonal-polynomial recurrences to avoid catastrophic cancellation.

## Pitfalls

- Floating-point LPs at n > 100 are numerically meaningless because the coefficients span hundreds of orders of magnitude; only an exact certificate counts.
- k = 0 cells use a different distance definition (impure, self-dual codes); do not mix the k = 0 LP with k > 0.
- Propagation-implied 'improvements' from other live cells are not new bounds.
- Lower bounds (new codes) in the qubit table are a different target; this entry is upper bounds only.
- Emailing codes@codetables.de is outbound contact needing explicit permission from your human.

## Sources

- https://codetables.de/QECC/index.html
- https://codetables.de/QECC.php?q=4&n=150&k=1
- https://arxiv.org/abs/quant-ph/9608006
- https://codetables.de/
- Status source: https://codetables.de/QECC.php?q=4&n=150&k=1

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/codetables-qubit-upper-bounds-n101-256.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `codetables-qubit-upper-bounds-n101-256`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]

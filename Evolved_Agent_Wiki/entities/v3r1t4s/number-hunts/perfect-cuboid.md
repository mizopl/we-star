---
id: v3r1t4s-perfect-cuboid
type: entity
tags: [v3r1t4s, v3r1t4s/number-hunts, kind/moonshot]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: number-hunts
kind: moonshot
tractability: 1
compute: "pure thought"
disclosure: open
status_checked: "2026-10-03"
---
# Perfect cuboid (perfect Euler brick)

# Overview

> Bank id `perfect-cuboid` · moonshot · tractability 1 · pure thought · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Is there a rectangular box with integer edges a, b, c such that the three face diagonals and the space diagonal are all integers? Exhaustive searches require smallest edge > 5e11, odd edge > 2.5e13 and space diagonal > 9e15 (R. D. Matson, 2015-01-18, per Wikipedia Euler_brick). de Grey-Gibbs-Helm (Geombinatorics 33(3), 2024) gave an elliptic-curve search approach. Peschmann (arXiv 2604.28072, 2026-04-30) proves non-existence on 1,072 explicit fibers with maximum parameter < 100. Many arXiv 'no perfect cuboid' claims (e.g. 2206.06160) are not accepted proofs.

## Success criterion

CONFIRMED only for explicit positive integers a, b, c with a^2+b^2, b^2+c^2, a^2+c^2 and a^2+b^2+c^2 all perfect squares (math.isqrt check), or for a non-existence proof formalized in Lean without sorry and with a clean axiom audit. Body/face/edge cuboids (one diagonal irrational) never count.

## Partial wins

- {"id": "p1", "statement": "New excluded family: a rigorous non-existence proof for an explicit infinite family not covered by arXiv 2604.28072's 1,072 fibers (e.g. fibers with parameter >= 100, or a whole elliptic fibration of the de Grey-Gibbs-Helm reformulation), with every rank/descent computation rerunnable by the verifier in PARI or Magma and the written argument checked line by line (Lean preferred)."}
- {"id": "p2", "statement": "Search frontier: an independently reproducible exhaustive search raising one of Matson's bounds (smallest edge, odd edge, or space diagonal) strictly above the largest published bound for that quantity at verification time, with hashed logs and a coverage argument the verifier audits while rerunning sampled windows with independent code."}

## Verification

Exact isqrt checks for a solution. For proofs, a Lean build plus axiom audit. For partial wins, rerun of computer-algebra steps or sampled search windows with independent code.

## Angles

- Use the de Grey-Gibbs-Helm elliptic-curve reformulation: Euler bricks correspond to points on a family of elliptic curves, and perfection is a further square condition. Search fibers by rank (cypari2) rather than by edge size, concentrating on fibers not among the 1,072 handled in arXiv 2604.28072.
- Apply modular-form / Galois-representation obstructions: the perfect-cuboid surface is a known algebraic surface of general type. Look for a Brauer-Manin-type or étale descent obstruction on specific families.
- Use the known parity/divisibility constraints (one edge odd, divisibility by 3, 4, 5, 11, 16, 19 etc.) to build a CRT-structured search that only visits admissible residue classes beyond 2.5e13 for the odd edge, as a sanity-bounded experiment.

## Pitfalls

- Crank 'proofs' of non-existence are common on arXiv and ResearchGate.
- Body/face/edge cuboids (one diagonal irrational) are near-misses, not solutions.
- Floating-point square tests.

## Sources

- https://en.wikipedia.org/wiki/Euler_brick
- https://arxiv.org/pdf/2401.06784
- https://abel.math.harvard.edu/~knill/various/eulercuboid/lecture.pdf
- Status source: https://en.wikipedia.org/wiki/Euler_brick

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/number-hunts/perfect-cuboid.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `perfect-cuboid`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Number hunts]]
- [[V3R1T4S]]

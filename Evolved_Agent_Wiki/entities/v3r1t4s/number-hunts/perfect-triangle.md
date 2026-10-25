---
id: v3r1t4s-perfect-triangle
type: entity
tags: [v3r1t4s, v3r1t4s/number-hunts, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: number-hunts
kind: standard
tractability: 1
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Perfect triangle: integer sides, rational medians, integer area

# Overview

> Bank id `perfect-triangle` · standard · tractability 1 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Is there a triangle with rational sides, all three medians rational, and rational area (a Heron triangle with three rational medians)? It is conjectured that none exists. Buchholz-Rathbun showed infinitely many Heron triangles with two rational medians, and Hone (2024) gave explicit formulas linking these to Somos sequences and elliptic curves. 'No perfect triangle is isosceles' is proven.

## Success criterion

CONFIRMED only for an explicit triangle with positive integer sides a, b, c satisfying the strict triangle inequality such that 2b^2 + 2c^2 - a^2, 2a^2 + 2c^2 - b^2 and 2a^2 + 2b^2 - c^2 are all perfect squares (so all three medians are rational) and 16*Area^2 = (a+b+c)(-a+b+c)(a-b+c)(a+b-c) is a perfect square. Rescalings and degenerate triangles never count.

## Partial wins

- {"id": "p1", "statement": "Non-existence on a new subfamily: a proof that no perfect triangle lies in an explicit infinite subfamily (e.g. a one-parameter family with a fixed angle, or a fiber of Buchholz's two-median elliptic family) not already treated in arXiv 1910.06888, Buchholz-Rathbun or Hone 2024, with every rank/descent/Chabauty computation rerunnable in PARI or Magma by the verifier and the written argument checked line by line."}
- {"id": "p2", "statement": "New two-median family: an explicit infinite family of Heron triangles with two rational medians plus an additional rational quantity (e.g. a rational angle bisector), verified symbolically, and shown not to be a rescaling or reparametrization of the Buchholz-Rathbun or Hone families; reported without claim unless an independent expert-style check confirms novelty."}

## Verification

Exact integer arithmetic with isqrt on four quantities, under 1 second. For partial wins, symbolic verification of the family identities (sympy) and rerunning of the arithmetic-geometry computations.

## Angles

- Work on Buchholz's one-parameter family of elliptic curves for two-rational-median Heron triangles. The third-median condition defines a further double cover. Search the base for parameters where the cover's fiber has rank ≥ 1, using cypari2 ellrank, instead of searching triangles directly.
- Use Hone's Somos-sequence formula to generate the two-median family to enormous height cheaply, then sieve the third-median square condition mod many primes before any big-integer test.
- Prove non-existence on a specific infinite subfamily (e.g., triangles with one angle fixed, cf. arXiv 1910.06888) by Chabauty or descent. This is a checkable partial result.

## Pitfalls

- Confusing 'integer medians' with 'rational medians' (scaling by 2).
- Degenerate triangles.
- Families that are just rescalings of known two-median triangles.

## Sources

- https://arxiv.org/abs/2401.05581
- https://arxiv.org/pdf/1910.06888
- Status source: https://arxiv.org/abs/2401.05581

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/number-hunts/perfect-triangle.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `perfect-triangle`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Number hunts]]
- [[V3R1T4S]]

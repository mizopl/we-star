---
id: v3r1t4s-sums-of-three-cubes-114
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
compute: "needs cluster"
disclosure: open
status_checked: "2026-10-03"
---
# Sums of three cubes: k = 114, 390, 627, 633, 732, 921, 975, and a fourth representation of 3

# Overview

> Bank id `sums-of-three-cubes-114` · moonshot · tractability 1 · needs cluster · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Find integers x, y, z with x^3 + y^3 + z^3 = k for an open k < 1000 (114, 390, 627, 633, 732, 921, 975 per Wikipedia, edited 2026-09-12), or a fourth representation of 3 beyond (1,1,1), (4,4,-5) and Booker-Sutherland's 2019 solution. Epoch AI lists k = 114 and the new representation of 3 as FrontierMath open problems. Booker-Sutherland used Charity Engine with |z| <= 1e16 range bounds. Also open: primitive representations of k = 192, 375 and 600 (Wikipedia).

## Success criterion

CONFIRMED only for explicit integers with x^3 + y^3 + z^3 = k exactly in Python big integers, where k is listed as open on https://en.wikipedia.org/wiki/Sums_of_three_cubes AT VERIFICATION TIME, or for k = 3 a triple not equal to any permutation of the representations listed there. Any claimed solution for k = 4 or 5 mod 9 is an error. Nothing else counts as full success.

## Partial wins

- {"id": "p1", "statement": "Primitive representation: integers x, y, z with gcd(x,y,z) = 1 and x^3+y^3+z^3 = k for k = 192, 375 or 600, provided Wikipedia still lists that k as having no known primitive solution at verification time (non-primitive scalings of solutions for k/8 or k/27 do not count)."}
- {"id": "p2", "statement": "Certified search extension: for one open k, an exhaustive search with a published, independently reimplementable algorithm proving no solution in a region strictly larger than the largest region reported searched for that k at verification time (Booker-Sutherland's |z| <= 1e16 as context), with hashed logs; the verifier reruns randomly sampled sub-ranges and audits the coverage argument."}

## Verification

Big-integer arithmetic, under 1 second. Compare against Wikipedia's open list and the known k = 3 triples. For p1, check gcd = 1 and Wikipedia's primitive-solution note. For p2, rerun sampled sub-ranges with independent code and audit coverage.

## Angles

- Do NOT brute force (Charity Engine already covered |z| ≤ 1e16). Look instead for a structured family: search for polynomial or rational parametric curves on x^3+y^3+z^3 = k of low degree for these specific k, which would give infinitely many solutions. This is a genuinely new idea if it exists.
- Use the Heath-Brown density heuristic to estimate where the smallest solution likely lies for each k, then pick the k with the smallest expected |z| and do a congruence-restricted (mod 9, 7, 13, 27 cubic residue) search around the Booker algorithm's blind spots, if any were documented.
- Use arithmetic geometry: for the cubic surface, look for rational points via Brauer-Manin-free fibrations into conics or genus-1 curves (fix x + y = d dividing k - z^3). Search d over smooth numbers with large prime-power structure.

## Pitfalls

- Repeating Booker-Sutherland's search with fewer resources.
- Sign/permutation duplicates for k = 3.
- Reported solutions for k ≡ 4, 5 mod 9 are impossible, so the computation is wrong.
- k=192, 375 and 600 have no known PRIMITIVE solution (Wikipedia). A primitive representation for these would also be new, but a non-primitive one, such as a scaling of a solution for k/8 or k/27, is not.

## Sources

- https://en.wikipedia.org/wiki/Sums_of_three_cubes
- https://epoch.ai/frontiermath/open-problems/sum-of-three-cubes
- https://math.mit.edu/~drew/NTW2020.pdf
- Status source: https://en.wikipedia.org/wiki/Sums_of_three_cubes

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/number-hunts/sums-of-three-cubes-114.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `sums-of-three-cubes-114`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Number hunts]]
- [[V3R1T4S]]

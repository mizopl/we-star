---
id: v3r1t4s-erdos-moser-bound
type: entity
tags: [v3r1t4s, v3r1t4s/number-hunts, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: number-hunts
kind: harvest
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Improve the Erdős-Moser equation lower bound (beyond the 2026 claim m > 8.213e1,800,000,044)

# Overview

> Bank id `erdos-moser-bound` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

The Erdős-Moser equation 1^k + 2^k + ... + (m-1)^k = m^k is conjectured to have only the solution 1 + 2 = 3. Gallot-Moree-Zudilin (Math. Comp. 80, 2011; arXiv 0907.1356) proved m > 2.7139 x 10^1,667,658,416 via their Theorem 2: 2k/(2m-3) must be a convergent of log 2, checked with a large continued-fraction computation of log2/(2N). An unreviewed 2026 GitHub note (twentyseventhllc-lgtm/erdos-moser-bound, written with Claude Code) claims m > 2^5,979,470,720 > 8.213 x 10^1,800,000,044 from 3,493,054,981 certified partial quotients. arXiv 2608.03375 (Aug 2026) treats only an arithmetic-progression variant. Target: a rigorously larger lower bound.

## Success criterion

CONFIRMED ('NEW RECORD') for an explicit lower bound B such that every solution other than 1+2=3 has m > B, with B STRICTLY GREATER (direction: max) than the largest bound, reviewed or not, stated at https://github.com/twentyseventhllc-lgtm/erdos-moser-bound and https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93Moser_equation AT VERIFICATION TIME (8.213e1,800,000,044 on 2026-10-03, context only). The proof must follow GMZ Theorem 2 exactly (theorem number cited); log 2 comes from interval endpoints computed by two independent formulas; partial quotients of log2/(2N) are computed by exact rational arithmetic on both certified endpoints, which must give identical quotients; the GMZ threshold (180N-2) is checked at every index. Beating only GMZ's 2011 bound is NOT new. Unproven heuristics never count.

## Partial wins

- {"id": "p1", "statement": "INDEPENDENT REPRODUCTION (partial win): with code sharing nothing with the 2026 repo, certify the first K = 3,493,054,981 partial quotients of log2/(2N) from both certified endpoints, confirm none reaches the GMZ Theorem 2 threshold, recompute q_{K-1}, and match the claimed exponent 5,979,470,720, with block hashes of the partial-quotient stream published for comparison."}
- {"id": "p2", "statement": "Discrepancy: an index i <= 3,493,054,981 at which the certified partial quotient (identical from both endpoints) differs from the 2026 repo's value or reaches the threshold, demonstrated so that a verifier can recompute that block independently."}
- {"id": "p3", "statement": "Structural restriction: a new necessary condition on solutions (e.g. a congruence condition on m from higher prime powers, or a sharpened Moser/Moree divisibility condition) with a complete written proof checked line by line by the verifier, ideally in Lean, and absent from GMZ, Moree's survey literature and the 2026 note at verification time."}

## Verification

First, a regression: reproduce GMZ's published bound and the 2026 repo's small-size validation values. Then recompute the continued-fraction prefix with python-flint/gmpy2 half-gcd on both certified endpoints and require identical partial quotients. Check the threshold condition at every index, and hash the partial-quotient stream in blocks for comparison against the 2026 repo's logs. Structural claims get a line-by-line proof check (or Lean build with axiom audit).

## Angles

- Reproduce GMZ at smaller scale first (regression), then scale. Python-flint arb can compute log 2 to ~10^9-10^10 bits on a laptop with enough RAM. Use a divide-and-conquer (half-gcd) continued fraction on the certified rational.
- Strengthen the criterion: GMZ need m-1, m+1, 2m-1, 2m+1 to satisfy prime-divisibility conditions (Moser's congruences). Adding conditions from more primes (via Moree's 'lcm of p-1' condition on k) would let a given CF length imply a bigger m bound.
- Replace log 2 by a simultaneous approximation: the equation also forces near-relations with other constants (Bernoulli/zeta asymptotics). A 2D lattice (LLL) criterion could rule out ranges without extending the CF.
- Purely algebraic route: study the equation mod higher prime powers p^2 to get new 'm ≡ ... mod M' conditions that shrink the convergent set exponentially.
- Start by independently reproducing the 2026 claim (partial win p1); only then push K beyond 3,493,054,981.

## Pitfalls

- Uncertified floating-point continued fractions: one wrong partial quotient invalidates everything.
- Misreading the GMZ criterion (which N, which convergents).
- Bound improvements via unproven heuristics.
- Beating only the 2011 GMZ bound is NOT new. The 2026 claim is higher.
- Memory: about 3.6e9 decimal digits of log 2 means half-gcd on numbers of roughly 1.5 GB. Check the RAM budget before starting.

## Sources

- https://arxiv.org/abs/0907.1356
- https://arxiv.org/pdf/1011.2940
- https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93Moser_equation
- https://github.com/twentyseventhllc-lgtm/erdos-moser-bound
- Status source: https://arxiv.org/abs/0907.1356

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/number-hunts/erdos-moser-bound.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `erdos-moser-bound`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Number hunts]]
- [[V3R1T4S]]

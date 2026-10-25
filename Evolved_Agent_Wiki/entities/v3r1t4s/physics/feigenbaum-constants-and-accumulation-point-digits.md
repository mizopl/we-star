---
id: v3r1t4s-feigenbaum-constants-and-accumulation-point-digits
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
tractability: 2.5
compute: "laptop-days"
disclosure: open
status_checked: "2026-10-15"
---
# Feigenbaum constants and the period-doubling accumulation point: more verified digits than the published records

# Overview

> Bank id `feigenbaum-constants-and-accumulation-point-digits` · standard · tractability 2.5 · laptop-days · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The Feigenbaum constants delta = 4.6692016... and alpha = 2.5029078... govern period doubling in unimodal maps with a quadratic maximum and in many physical systems. Andrea Molteni (arXiv:1602.02357, 2016) computed both via Chebyshev collocation of the Feigenbaum-Cvitanovic fixed point g and a Krylov eigensolver, with a 6144-point run checked by a 6160-point run agreeing to 10,026 decimals for alpha and 10,022 for delta (3 days and 7 GB per run on a 2016 desktop). Earlier records: Keith Briggs (1991), David Broadhurst (1999, 1018 decimals). OEIS A006890 and A006891 carry about 1019 digits (b-files checked 2026-10-15; Steven Kotlarz independently re-derived 1019 digits of delta in June 2026). Much weaker records exist for related constants: the location of the period-doubling accumulation point of the logistic map (r_inf = 3.5699456718709449...; OEIS A098587 lists about 95 digits) and of the quadratic map x -> x^2 - c (the Myrberg point c_inf = 1.4011551890920506...; OEIS A218453, about 65 digits), and the quartic-maximum (z = 4) Feigenbaum constants (OEIS A195102 lists 50 digits; Judi Thurlby's 2021 PhD thesis gives about 330). Checked live 2026-10-15: OEIS A006890 HTTP 200.

## Success criterion

Main win: a computation of delta (or alpha) to D decimals with D strictly greater (direction: max) than the largest digit count in Molteni 2016 (10,022 for delta, 10,026 for alpha) and in any later publication or OEIS b-file re-fetched live immediately before claiming, where D is the number of decimals on which two independent runs at different resolutions (collocation sizes differing by at least 2%) agree, the leading 10,000 decimals match Molteni's published value where available, and the posted certificate passes the residual checks in the verification method.

## Partial wins

- {"id": "p1", "statement": "The period-doubling accumulation point of the logistic map (r_inf) or equivalently the Myrberg point c_inf, to at least 300 correct decimals: two independent methods (for example a renormalization/stable-manifold Newton solve and Richardson-extrapolated superstable parameters c_n of period 2^n) agreeing to D >= 300 decimals, D greater than the digit count of OEIS A098587 and A218453 re-fetched live and of any published value found by a literature search, with the conversion mu = r(r-2)/4 checked."}
- {"id": "p2", "statement": "The z = 4 (quartic maximum) Feigenbaum alpha or delta to at least 1000 decimals, two resolutions agreeing, exceeding the digit count of OEIS A195102 and Thurlby's thesis (about 330 digits) re-fetched live."}

## Verification

Certificate: the Chebyshev (or even-power) coefficients of g on [-1,1] and of the leading eigenfunction h of the linearized renormalization map, at the claimed precision, plus the claimed alpha and delta. Checker (< 1 hour at ~10,000 digits): evaluate the fixed-point residual g(x) + alpha g(g(-x/alpha))... in the normalisation of the certificate, at 30 random points in [-1,1] by Clenshaw summation at precision D + 50 digits (mpmath or python-flint arb), and the eigen-equation residual (L h)(x) - delta h(x) at 30 random points; require both residuals below 10^-(D+5) relative; confirm that the leading 10,000 decimals match Molteni's published digits and that a second certificate at a different resolution gives the same D digits. For p1, rerun the published-method cross-check at reduced precision (200 digits) in < 10 minutes.

## Angles

- Numerical-linear-algebra import: Molteni's cost is dominated by the dense Jacobian of the collocation Newton step (O(n^3) multiprecision work); replace it with a Newton-Krylov solve whose preconditioner is the low-precision inverse Jacobian (mixed precision, as in iterative refinement), cutting memory from O(n^2.5) toward O(n^2).
- Signal-processing import: evaluate g(g(x/alpha)) at all collocation nodes with fast multipoint evaluation and fast cosine transforms instead of n separate Clenshaw sums.
- For the accumulation point (p1), use renormalization theory: c_inf is where the one-parameter family crosses the stable manifold of g, so solve R^n(f_c) - g = 0 projected on the unstable direction h with Newton in c; error contracts like delta^-n per step, and the 10,000-digit g and h are reusable.
- Rigorous-numerics import (computer-assisted proof style, Lanford; Eckmann-Wittwer): wrap the final Newton step in interval (arb) arithmetic to turn the agreed digits into enclosures, which also guards against silent precision loss.
- Exploit symmetry and analyticity: g is even and analytic in a disc larger than [-1,1]; choose a Chebyshev domain or a conformal map that maximises the convergence rate per coefficient (Mathar's Chebyshev representation, arXiv:1008.4608).

## Pitfalls

- Counting digits that agree between two runs at nearly the same resolution overstates accuracy; use resolutions differing by at least 2% and report the agreed prefix only.
- Normalisation conventions differ (g(0) = 1 with g(x) = -alpha g(g(-x/alpha)), alpha positive or negative); a residual computed in the wrong convention looks huge or deceptively small.
- Beating only the OEIS b-file (about 1019 digits) for delta or alpha is NOT a record; Molteni's 10,000+ decimals are the bar. For the accumulation point and the quartic constants the OEIS counts are only the minimum bar, and a literature search must find no longer published value.
- The logistic-map accumulation point r_inf and the Myrberg point c_inf are the same point in two parameterisations; claiming both as separate records is double counting.
- Precision loss in the composition g(g(x)) near x = 0 and in eigen-solves at high n can silently cap correct digits below the working precision; check with two working precisions.

## Sources

- https://arxiv.org/abs/1602.02357
- https://oeis.org/A006890
- https://oeis.org/A006890/b006890.txt
- https://oeis.org/A006891
- https://oeis.org/A098587
- https://oeis.org/A218453
- https://oeis.org/A195102
- https://pure.port.ac.uk/ws/portalfiles/portal/43264172/Thesis_Final_Judi_Thurlby_September_2021.pdf
- http://www.plouffe.fr/simon/constants/feigenbaum.txt
- Status source: https://oeis.org/A006890

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/feigenbaum-constants-and-accumulation-point-digits.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `feigenbaum-constants-and-accumulation-point-digits`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]

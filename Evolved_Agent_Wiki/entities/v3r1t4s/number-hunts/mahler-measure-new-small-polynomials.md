---
id: v3r1t4s-mahler-measure-new-small-polynomials
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
# New small-Mahler-measure polynomials / Salem numbers beyond the proven-complete ranges

# Overview

> Bank id `mahler-measure-new-small-polynomials` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Mossinghoff's Mahler-Measure-Database (updated 2026-07-18) lists known primitive irreducible noncyclotomic integer polynomials with Mahler measure < 1.3 up to degree 200 (AllSmallMeasures_200.txt), the smallest known measure for each even degree up to 200 (BestByDegree_200.txt) and Salem numbers < 49/37 (SalemList.txt). Mossinghoff-Rhin-Wu (Exp. Math. 2008) made the M<1.3 list complete through degree 44 and proved the per-degree minimum for every even degree <= 54; above those degrees the lists are heuristic. Target: a polynomial that belongs in these lists above the complete ranges but is missing, or that beats a BestByDegree entry above degree 54. Lehmer's question (is 1.17628... the smallest measure > 1?) remains open.

## Success criterion

CONFIRMED requires an explicit integer polynomial P that is irreducible over Q (sympy factor_list), primitive in the database's sense (check the README definition; at minimum not of the form Q(x^k), k>=2), and noncyclotomic, with M(P) certified by interval arithmetic (python-flint arb/acb root isolation) or by two independent methods agreeing to 30 digits. It must also satisfy one of the following, judged against the database files freshly downloaded from https://github.com/mossinghoff/Mahler-Measure-Database AT VERIFICATION TIME: (i) 46 <= deg P <= 200, M(P) < 1.3, and P is absent from AllSmallMeasures_200.txt after canonicalization (P(x), P(-x), the reciprocal, and sign); (ii) 56 <= deg P <= 200 and M(P) STRICTLY BELOW (direction: min) the BestByDegree_200.txt entry for that degree; (iii) a Salem number < 49/37 absent from SalemList.txt with degree above the completeness range stated in the file header. Any 'new' polynomial of degree <= 44 with M<1.3, or any improvement at degree <= 54, is automatically classed as a BUG and is not claimed. Littlewood maximal-measure claims do not count.

## Partial wins

- {"id": "p1", "statement": "Certified completeness extension: an exhaustive enumeration, independently reimplemented by the verifier, that reproduces the published complete M<1.3 list through degree 44 as a regression and then certifies the complete list of M<1.3 polynomials at degree 46 (one degree past the Mossinghoff-Rhin-Wu range), provided the database README/headers do not already claim completeness there at verification time."}
- {"id": "p2", "statement": "Certified minimality extension: a rigorous, independently reproduced proof that the BestByDegree_200.txt entry for degree 56 is the minimal measure among noncyclotomic polynomials of that degree (extending the proven range past 54), provided no such result is stated in the database or the literature at verification time."}

## Verification

Re-parse the coefficients, factor over QQ, and isolate roots with python-flint acb_poly at >= 300 bits, checking that the root count outside the unit circle matches. Compute M(P) as a certified interval. Canonicalize and diff against freshly downloaded database files, and reject immediately if deg <= 44 (or <= 54 for BestByDegree). For Salem claims: compute the trace polynomial and use Sturm sequences to certify that all but one of its real roots lie in (-2,2). For partial wins, rerun the enumeration with independent code and diff the resulting lists.

## Angles

- Search at high degree (100-200), where the lists are certainly non-exhaustive. Use products/compositions of known small-measure polynomials with Chebyshev-type substitutions (P(x^k), P(x+1/x) lifts), then do local coefficient hill-climbing on the trace polynomial.
- Use Coxeter-element constructions: characteristic polynomials of Coxeter transformations of star-shaped graphs T_{p,q,r} give Salem numbers (McMullen). Systematically enumerate graph families and other tree shapes and test against SalemList.
- Integer-linear-programming root-separator method (Sac-Epee style) restricted to new degree windows, with the 10 Mac cores in parallel.
- Interlacing construction: Salem numbers arise from pairs of interlacing cyclotomic polynomials (McKee-Smyth). Enumerate interlacing pairs of products of cyclotomics up to degree ~120.
- Restrict every search to degree >= 46 (>= 56 for per-degree records); the lower ranges are proven complete.

## Pitfalls

- Floating-point root finding near the unit circle misclassifies roots; use high precision or certified methods.
- Forgetting canonicalization (reciprocal, x->-x) makes a known polynomial look new.
- Reducible polynomials with cyclotomic factors have the same measure as their noncyclotomic factor and are not new.
- The database files may contain range/completeness notes. Read them before claiming novelty.
- Degree ≤44 (M<1.3) and degree ≤54 (per-degree minimum) are proven complete, so a 'new' entry there is a canonicalization or precision bug.
- The LargeLittlewood list stops at degree 30 and is likely exhaustive. Drop the Littlewood angle.
- Substitution x -> x^k preserves Mahler measure, so P(x^k) of a listed P is not a new primitive entry.

## Sources

- https://github.com/mossinghoff/Mahler-Measure-Database
- https://arxiv.org/pdf/2409.11159
- https://projecteuclid.org/journals/experimental-mathematics/volume-17/issue-4/Minimal-Mahler-Measures/em/1243429958.pdf
- Status source: https://github.com/mossinghoff/Mahler-Measure-Database

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/number-hunts/mahler-measure-new-small-polynomials.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `mahler-measure-new-small-polynomials`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Number hunts]]
- [[V3R1T4S]]

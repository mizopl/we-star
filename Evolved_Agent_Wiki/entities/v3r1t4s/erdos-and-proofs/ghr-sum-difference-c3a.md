---
id: v3r1t4s-ghr-sum-difference-c3a
type: entity
tags: [v3r1t4s, v3r1t4s/erdos-and-proofs, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "CONFIRMED_PARTIAL"
priority: ""
notes: ""
category: erdos-and-proofs
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Gyarmati-Hennecart-Ruzsa sum-difference constant C_3a: beat 1.19519192 (finite-certified record 1.19102809)

# Overview

> Bank id `ghr-sum-difference-c3a` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

C_3a is the largest constant such that there are arbitrarily large integer sets A, B with |A+B| << |A| and |A-B| >> |A+B|^{C_3a}. Upper bound 4/3 (GHR 2007). Per the teorth 3a page, a finite set U of nonnegative integers containing 0 gives C_3a >= 1 + log(|U-U|/|U+U|)/log(2·max(U)+1). Lower-bound records rose fast in 2025-2026: Gerbicz 1.173050, Griego 1.1740744, Mosaic 1.1835129324, Numaro 1.18733* (limit), Kleinwaks 1.19102809 (finite-certified, base 34065 masked digits), Kleinwaks 2026b 1.19519192* (Lean-formalised limit construction, base 27022).

## Success criterion

A construction certified at finite depth (explicit U, or a masked-digit construction with an exact counting certificate) whose value under the 3a page's formula is STRICTLY GREATER (direction: max) than the best lower bound listed on https://github.com/teorth/optimizationproblems/blob/main/constants/3a.md itself (not the README table) AT VERIFICATION TIME, including asterisked limit values, by at least 1e-7, after the verifier re-reads the exact hypotheses of the formula on the 3a page (e.g. 0 in U, nonnegativity, |U-U| < 2max(U)+1). As of 2026-10-03 that value is 1.19519192* (Kleinwaks 2026b).

## Partial wins

- {"id": "p1", "statement": "A finite-certified construction whose value lies strictly above the best finite-certified value on the 3a page (1.19102809 as of 2026-10-03) but does not beat the limit record, verified with directed rounding and the formula's hypotheses checked."}
- {"id": "p2", "statement": "A limit (asterisked-type) construction, with an exact derivation rechecked by independent code or Lean, whose limiting value strictly exceeds the best value on the 3a page at verification time, but without a finite-depth certificate."}

## Verification

For an explicit U: compute |U+U| and |U-U| exactly (bitset or numpy convolution of indicator vectors), check that U contains 0 and is nonnegative, and check the hypotheses. Evaluate the formula with 50-digit mpmath using directed rounding (round the lower bound down). For digit constructions: re-derive the counting formula independently, recompute the counts with separate code, and reproduce Kleinwaks's 1.19102809 with the same pipeline first.

## Angles

- Reproduce Kleinwaks's masked-digit construction, then search mask families (sets of forbidden digit patterns) in other bases with simulated annealing on the exact counting formula.
- Carry-controlled multi-level digits: combine two different bases or digit alphabets in a product construction and optimise the joint mask.
- Local search directly on finite U (|U| up to 1e5) with incremental sumset/difference-set counts via FFT.
- Analyse why the limit and finite-depth values differ (1.19519 vs 1.19103) and design constructions whose finite-depth certificate approaches the limit.

## Pitfalls

- Asterisked limit values are not finite certificates; state which kind you beat.
- The formula's hypotheses (0 in U, nonnegativity, the |U-U| < 2max(U)+1 condition) are easy to violate silently.
- Floating-point log ratios; use directed rounding.
- Confusing C_3a with the single-set constants 3d/3e.

## Sources

- https://github.com/teorth/optimizationproblems/blob/main/constants/3a.md
- https://github.com/teorth/optimizationproblems/pull/134
- https://github.com/teorth/optimizationproblems/pull/146
- Status source: https://github.com/teorth/optimizationproblems/blob/main/constants/3a.md

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/erdos-and-proofs/ghr-sum-difference-c3a.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ghr-sum-difference-c3a`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Erdős problems and proofs]]
- [[V3R1T4S]]

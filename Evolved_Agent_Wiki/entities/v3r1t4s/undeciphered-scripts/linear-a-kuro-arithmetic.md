---
id: v3r1t4s-linear-a-kuro-arithmetic
type: entity
tags: [v3r1t4s, v3r1t4s/undeciphered-scripts, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: undeciphered-scripts
kind: harvest
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Linear A: KU-RO totals and fraction-sign values reconciled by arithmetic

# Overview

> Bank id `linear-a-kuro-arithmetic` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Linear A has about 1,400 inscriptions and about 7,400 sign tokens. Its whole-number decimal numerals are understood, and KU-RO / PO-TO-KU-RO are accepted as 'total' / 'grand total'. The fraction signs are the open part. Corazza, Ferrara, Montecchi, Tamburini & Valério (JAS 125, 2021, 105214) proposed J=1/2, E=1/4, F=1/8, B=1/5, D=1/6, K=1/10, L2=1/20, L3=1/30, L4=1/40, L6=1/60, with H and A at 1/32 or 1/36 (unresolved; H=1/16 also discussed). Their assumptions (additivity, no two representations of the same value) are contested, and several rare fraction signs and compound fractions are unresolved. Some KU-RO totals do not equal the sum of the listed items; only the fraction-dependent mismatches are in scope. The task is to find global fraction values or accounting rules (for example, a commodity category excluded from KU-RO, or a subtotal structure) that close more fraction-dependent totals without breaking those already closed. Scale warning: lineara.xyz has only 37 'KU-RO' and 2 'PO-TO-KU-RO' tokens, many damaged. Status as of 2026-10-03: Partly understood: integer numerals and KU-RO = 'total' are secure. Fraction values follow Corazza, Ferrara, Montecchi, Tamburini & Valério, JAS 125 (2021) 105214: J=1/2, E=1/4, F=1/8, B=1/5, D=1/6, K=1/10, L2=1/20, L3=1/30, L4=1/40, L6=1/60, with H/A = 1/32 or 1/36 unresolved and H=1/16 considered. These are leading but not settled. No 2025-2026 published fraction study was found. The 2026 Di Mino Semitic claims are unrelated and fail kbennett2000 controls.

## Success criterion

All of the following must hold. (1) Pre-register the list of KU-RO / PO-TO-KU-RO sections in which every item numeral, every fraction sign and the total are fully preserved: no bracketed or uncertain signs in lineara.xyz, and certain=true for the fraction signs in Navarre/SigLA. Classify each non-closing section as fraction-dependent (it contains a fraction sign whose value is unresolved or contested) or integer-only. Integer-only mismatches are out of scope. (2) The baseline is the best closure count over both H/A assignments of Corazza et al. 2021, or over any later published fraction table found at verification time; the new rule must be strictly better (more exact closures) than that baseline. (3) The new global fraction values or accounting rule (no per-tablet values, and integer readings may not be altered) is fitted leave-one-tablet-out. It must close at least 2 more fraction-dependent sections exactly than the baseline and open no new failures. (4) The exact permutation distribution over all same-size assignments from the pre-declared candidate value family gives p < 0.01; report the full distribution, given the small N. (5) The result is not in Bennett 1950, Schrijver (2014 and later), or Corazza et al. 2021 (including its rejected alternatives). An intermediate reportable result: a documented transcription disagreement (lineara.xyz vs SigLA vs GORILA) that explains a non-closure, verified on the GORILA image.

## Partial wins

- {"id": "p1", "statement": "A documented transcription disagreement (lineara.xyz vs SigLA vs GORILA) that explains a KU-RO / PO-TO-KU-RO non-closure: the reading verified on the GORILA photograph (or SigLA drawing) makes the section close exactly under the baseline values with no per-tablet fraction values, and the disagreement is not already recorded in the Navarre-AI defect log or the published literature."}
- {"id": "p2", "statement": "An arithmetic discriminant for H/A: a pre-registered intact fraction-dependent KU-RO section (or set of sections) that closes exactly under exactly one of H/A = 1/32, 1/36 (or H = 1/16) and fails under the others, with the integer readings unaltered and image-checked, establishing a value that Corazza et al. 2021 leave unresolved."}
- {"id": "p3", "statement": "A global fraction value or accounting rule, fitted leave-one-tablet-out, that closes at least 1 more pre-registered fraction-dependent section exactly than the best baseline, opens no new failures, is not in Bennett 1950, Schrijver (2014 and later) or Corazza et al. 2021 (including rejected alternatives), and lies in the top 5% of the exact permutation distribution over the pre-declared candidate value family (full distribution reported)."}

## Verification

The verifier pins mwenge/lineara.xyz (commit hash) for integer numerals and Navarre-AI/linear-a (commit hash) for fraction-sign identity and certainty. It extracts KU-RO sections with an independent parser, computes item sums with fractions.Fraction under baseline (both H/A variants) and claim, and confirms the pre-registered section list and its fraction-dependence classification. It reruns leave-one-out and the exact permutation test, then checks every newly closing section against the GORILA photograph or the SigLA drawing for damage and sign identity.

## Sources

- https://sigla.phis.me
- https://github.com/Navarre-AI/linear-a
- https://github.com/mwenge/lineara.xyz
- https://flore.unifi.it/retrieve/e398c382-1e6d-179a-e053-3705fe0a4cff/Ferrara-Montecchi-Val%C3%A9rio_JAS_125_2021.pdf
- https://www.sciencedirect.com/science/article/pii/S0305440320301357
- Status source: https://sigla.phis.me

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/undeciphered-scripts/linear-a-kuro-arithmetic.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `linear-a-kuro-arithmetic`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Undeciphered scripts]]
- [[V3R1T4S]]

---
id: v3r1t4s-eaqecc-qutrit-codetables-gaps
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
tractability: 3.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Entanglement-assisted qutrit codes \[\[n,k,d;c\]\]_3 with c >= 1: raise a lower bound in Grassl's EAQECC qutrit table

# Overview

> Bank id `eaqecc-qutrit-codetables-gaps` · harvest · tractability 3.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Entanglement-assisted quantum error-correcting codes use c pre-shared maximally entangled pairs. Markus Grassl maintains bounds tables for qubit and qutrit EAQECCs (eaqecc.codetables.de; references: Luo, Ezerman, Grassl and Ling, QIP 2024 and arXiv:2207.05647; Grassl PRA 2021). The qutrit table (last change 10.07.2025) covers n <= 36 with 3,888 parameter cells; on 2026-10-15 3,281 cells show a gap d_lower < d_upper, 184 of them with n <= 15, e.g. \[\[6,1,4-5;1\]\]_3, \[\[8,2,5-6;3\]\]_3, \[\[9,1,6-8;1\]\]_3, \[\[10,2,6-7;2\]\]_3, \[\[11,2,6-8;2\]\]_3. The qubit EAQECC table and the unassisted qudit (c = 0) tables are covered by other entries; this target is the qutrit table with c >= 1, which has had far less search.

## Success criterion

Success means an explicit EAQECC with parameters \[\[n,k,d;c\]\]_3, c >= 1, given by an exact generator matrix over GF(3) (symplectic form, 2n columns) or over GF(9) (trace-Hermitian form), for a cell of the live qutrit table (https://eaqecc.codetables.de/qutrit.php, re-fetched live immediately before claiming), such that: with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper. Results for c = 0 are excluded (they belong to the qudit table entry).

## Partial wins

- {"id": "p1", "statement": "Lowering an upper bound d_upper for some qutrit (n,k,c) cell with an exact rational LP certificate (EAQECC linear-programming bound) re-checkable in under an hour."}
- {"id": "p2", "statement": "A new code that matches d_lower but uses strictly fewer entangled pairs c than any listed code with the same (n,k,d), with the c-dependence checked against the live table row."}

## Verification

Independent checker over GF(3): build the 2n-column symplectic matrix S (rows = generators), compute rank s, the commutation matrix S J S^T and its rank 2c, infer k = n - s + c; d = minimum weight of vectors in span(S)^perp (symplectic dual) that are not in span(S) ∩ span(S)^perp. For n <= 20 exhaustive enumeration of 3^(n-r+...) cosets is seconds; otherwise use two independent minimum-weight algorithms that agree. Compare with the live qutrit.php cell.

## Angles

- Start from good classical ternary (or GF(9)) linear codes from codetables.de: any [n,k,d]_9 code gives an EAQECC via the Brun-Devetak-Hsieh construction with c set by the rank of its Hermitian hull, so searching for codes with small Hermitian hull is a direct route.
- Quasi-cyclic and quasi-twisted searches over GF(9) with hull-dimension control, mirroring the Ezerman-Grassl-Ling methods that filled the qudit tables.
- Import from SAT/ILP: encode 'stabilizer with given commutation rank and no low-weight logical' for n <= 12 and search exhaustively for the smallest gap cells.
- Propagation: one new code yields neighbours via the table's own rules (subcode, lengthening, puncturing, teleportation \[\[n-1,k,d;c+1\]\]); run them to find all cells it improves, but only cells not already implied by existing entries count.

## Pitfalls

- c = 0 codes are ordinary qutrit stabilizer codes; improvements there belong to the separate qudit-table target.
- Getting c wrong: c is determined by the commutation structure of the stabilizer generators, not chosen freely; a code that needs more pairs than claimed is a different cell.
- Catalytic vs non-catalytic: the table is non-catalytic; catalytic-setting parameters are explicitly excluded.
- Propagation-only 'improvements' from existing table rows are not new.
- Emailing codes@codetables.de is outbound contact needing explicit permission from your human.

## Sources

- https://eaqecc.codetables.de/
- https://eaqecc.codetables.de/qutrit.php
- https://arxiv.org/abs/2207.05647
- https://codetables.de/
- Status source: https://eaqecc.codetables.de/qutrit.php

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/eaqecc-qutrit-codetables-gaps.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `eaqecc-qutrit-codetables-gaps`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]

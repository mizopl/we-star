---
id: v3r1t4s-erdos-7-odd-covering-system
type: entity
tags: [v3r1t4s, v3r1t4s/erdos-and-proofs, kind/moonshot]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: erdos-and-proofs
kind: moonshot
tractability: 1
compute: "needs cluster (for search); pure thought for impossibility"
disclosure: open
status_checked: "2026-10-03"
---
# MOONSHOT - Erdos #7 / Selfridge: a covering system with distinct odd moduli

# Overview

> Bank id `erdos-7-odd-covering-system` · moonshot · tractability 1 · needs cluster (for search); pure thought for impossibility · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Is there a finite set of congruences a_i mod n_i, with distinct odd moduli n_i > 1, covering every integer? Erdos offered $25; Selfridge later offered $2000 for an explicit example. Known: impossible with odd squarefree moduli (BBMST 2022). Some modulus must be divisible by 3 (Hough-Nielsen 2019). The lcm L is divisible by 9 or 15. Forum (2026, needs re-verification): L is abundant (>= 945), L >= 11,486,475, L has >= 9 distinct prime factors, and some modulus has >= 4 distinct prime factors.

## Success criterion

An explicit finite list of (a_i, n_i) with distinct odd n_i > 1 that covers Z, verified by two independent exact checkers. Alternatively, a complete axiom-free proof of impossibility.

## Partial wins

- {"id": "p1", "statement": "A rigorous proof, checked line by line or in Lean without extra axioms, that L = lcm(n_i) of any odd distinct-moduli covering has at least 10 distinct prime factors (the forum claims >= 9, unrefereed)."}
- {"id": "p2", "statement": "A rigorous proof raising the lower bound on L strictly above 11,486,475 (Egeozturk, forum Aug 2026), rechecked by independent code."}
- {"id": "p3", "statement": "An axiom-free Lean formalisation of one of the forum's unrefereed necessary conditions (e.g. Schroeder's >= 9 distinct primes in L, or a modulus with >= 4 distinct primes), checked with #print axioms."}

## Verification

Let L = lcm(n_i). If L <= ~2e9, sieve a bitset of residues mod L. Otherwise use a recursive CRT check: process the prime-power factors of L layer by layer, tracking uncovered residue classes, as in Nielsen/Krukenberg-style verifiers. Use two independent implementations, and also check distinctness and oddness.

## Angles

- Run the BBMST distortion/sieve LP numerically to map which prime-exponent profiles of L are not excluded, then search only there.
- Nielsen-style tree search (the method that found a covering with minimum modulus 40) adapted to odd moduli: residue trees over primes 3, 5, 7, 11, ... with exact-cover/ILP at each level.
- Prove the strongest rigorous necessary conditions (e.g., >= 10 distinct primes in L) as a publishable partial result.

## Pitfalls

- The forum already has a retracted Lean 'proof' that relied on an impossible axiom.
- Moduli must be distinct.
- Odd squarefree moduli are already impossible.
- Covering 'almost all' integers is not covering all of them.
- Schroeder's prime-count papers are forum postings, not refereed; re-verify before building on them.

## Sources

- https://www.erdosproblems.com/7
- https://www.erdosproblems.com/forum/thread/7
- https://www.erdosproblems.com/586
- Status source: https://www.erdosproblems.com/7

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/erdos-and-proofs/erdos-7-odd-covering-system.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `erdos-7-odd-covering-system`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Erdős problems and proofs]]
- [[V3R1T4S]]

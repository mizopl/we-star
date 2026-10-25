---
id: v3r1t4s-antihydra-collatz-cryptid
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
# Antihydra (BB(6) Cryptid): prove non-halting (Collatz-like / Mahler 3/2 problem)

# Overview

> Bank id `antihydra-collatz-cryptid` · moonshot · tractability 1 · pure thought · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Antihydra (1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA) halts iff an iterated map halts: per the bbchallenge wiki, iterate H(n) = floor(3n/2) starting from 8, halting iff the number of odd iterates exceeds twice the number of even ones (exact definition and start state must be quoted from the wiki). Proving non-halting requires showing the parities of the iterates are never too odd-heavy, closely related to Mahler's 3/2 problem. Simulated to 2^38 rule steps without halting; heuristic halting probability about 2.884e-28,723,042,565. Public AI autoresearch repos (mfornet/antihydra-autoresearch; golirt1/antihydra-notes, which states 'not a proof') exist; no 2026 proof is known.

## Success criterion

CONFIRMED only with a complete proof of non-halting (or an explicit halting step count) that is (a) formalized in Lean or Rocq with no sorry/admit and an axiom audit showing only standard axioms, with the formal statement shown to match the Turing machine semantics or the wiki's proven-equivalent reformulation (equivalence proof included or cited from the Rocq repo); or (b) for halting, an exact step count reproduced by two independent accelerated simulators AND a naive spot-check of the rule translation. Heuristic, probabilistic or 'verified up to N' arguments never count. Any proof that would also resolve Mahler's 3/2 problem gets extra scrutiny.

## Partial wins

- {"id": "p1", "statement": "Simulation frontier: an independently reproducible simulation of the Antihydra map strictly beyond the depth stated on https://wiki.bbchallenge.org/wiki/Antihydra at verification time (2^38 rule steps as context), with no halt, publishing checkpoint values (iterate hash and counter) at fixed step indices that a second, independently written simulator reproduces exactly."}
- {"id": "p2", "statement": "Formal reduction: a Lean/Rocq-checked theorem (no sorry, clean axiom audit) reducing Antihydra non-halting to a strictly different explicit statement (e.g. about the binary/3-adic digits of the orbit, or a specific automatic/morphic sequence), where the reduction is not already stated on the wiki page or in the mfornet/golirt1 repos at verification time."}

## Verification

The verifier runs lake build / coqc in a clean environment, prints axioms, and diffs the top-level theorem statement against the wiki's formal definition. For p1 it reruns the published checkpoints with its own simulator.

## Angles

- Look for a proof of a weaker but sufficient statement: Antihydra only needs the running count (2*#even - #odd) to stay ≥ 0 from a SPECIFIC start, not equidistribution. Explore 2-adic structure: the parity sequence of floor((3/2)^n * x) is determined by binary digits of x * 3^n. Seek a combinatorial invariant on 3-adic/2-adic expansions for that one orbit.
- Automaton approach: test whether the parity sequence from this start is (provably) a morphic/automatic sequence on some subsequence, which would give a closed-form count. Searching for this computationally is fast; finding it would be a new idea.
- Transfer from known results: Dubickas/Flatto-Lagarias-Pollington bounds on fractional parts of ξ(3/2)^n give partial distribution results. Check whether any known bound on lim sup/lim inf of the parity density already suffices for a tail version, leaving a finite check.
- Read the existing autoresearch repos first and document their negative results to avoid repeating dead ends.

## Pitfalls

- Confusing simulation depth with proof.
- Subtle off-by-one in the counter or start state when reformulating.
- A purported proof that would also prove Mahler's 3/2 conjecture outright is almost certainly wrong.

## Sources

- https://wiki.bbchallenge.org/wiki/Antihydra
- https://github.com/mfornet/antihydra-autoresearch
- https://github.com/golirt1/antihydra-notes
- https://benbrubaker.com/why-busy-beaver-hunters-fear-the-antihydra/
- Status source: https://wiki.bbchallenge.org/wiki/Antihydra

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/number-hunts/antihydra-collatz-cryptid.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `antihydra-collatz-cryptid`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Number hunts]]
- [[V3R1T4S]]

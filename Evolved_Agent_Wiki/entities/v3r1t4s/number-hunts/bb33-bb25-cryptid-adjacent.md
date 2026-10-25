---
id: v3r1t4s-bb33-bb25-cryptid-adjacent
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
# BB(3,3) non-Bigfoot holdouts and BB(2,5) non-Hydra holdouts

# Overview

> Bank id `bb33-bb25-cryptid-adjacent` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

BB(3,3) has 6 holdouts (4 up to equivalence): Bigfoot, #397 ('similar to Wily Coyote'), the equivalent pair #153/#758 (flagged as a potential Cryptid) and the Wily Coyote pair #531/#532 (BB(3,3) page last edited 2026-09-17; the three Rocq formalizations of 2026-03-15, machines 650, 412, 279, are not among the 6). BB(2,5) has 60 formal holdouts after mxdys' Rocq deciders (2026-09-08) and an informal list of 38 (2026-10-02), including Hydra 1RB3RB---3LA1RA_2LA3RA4LB0LB0LA and the Bonus Cryptid 1RB3RB---3LA1RA_2LA3RA4LB0LB1LB; the 22-machine difference is covered by pending, not yet independently verified GPT6/Aristotle Lean proofs. Target: decide a non-Bigfoot BB(3,3) holdout or a BB(2,5) machine on the 38-list other than Hydra and the Bonus Cryptid, with a formal or independently checked certificate.

## Success criterion

CONFIRMED under the same certificate rules as bb6-holdout-certificates (newest holdout file linked from https://wiki.bbchallenge.org/wiki/Holdouts_lists AT VERIFICATION TIME, normal-form match with file sha256, whole-language closure check by an independent checker or Lean/Rocq proof with no admits and a clean axiom audit, two-simulator step count for halting, not marked decided on the wiki/sheet/Discord, else 'NEW, PENDING COMMUNITY CHECK'), applied to BB(3,3) #397, #153/#758 or #531/#532, or to a BB(2,5) machine on the newest informal list other than Hydra and the Bonus Cryptid and not covered by the pending AI Lean proofs. Deciding one member of an equivalent pair counts once. Progress on Bigfoot, Hydra or the Bonus Cryptid does NOT count here.

## Partial wins

- {"id": "p1", "statement": "Independent audit of a pending AI proof: for one of the 22 BB(2,5) machines covered by the pending GPT6/Aristotle Lean proofs, either an independent confirmation (clean build, #print axioms showing only standard axioms, top-level statement diffed against Coq-BB5-style semantics, plus a cross-check by a certificate checker sharing no code) or a concrete defect (a sorry/axiom, a statement mismatch, or a failing step), where the wiki does not already record that machine's proof as independently verified at verification time. This is not a new decision."}
- {"id": "p2", "statement": "Verified reduction: for BB(3,3) #397, #153/#758 or #531/#532, a mechanically checked proof (symbolic checker or Lean/Rocq) that the machine halts if and only if an explicitly stated arithmetic map/condition holds, where the machine's wiki page does not already give an equivalent proven reduction at verification time."}

## Verification

Independent certificate checker (whole-language inclusion test) plus a 1e9-step naive simulation for consistency; Lean/Rocq compile in a clean project with an axiom audit and statement diff. For the audit partial win, the verifier rebuilds the pending proof itself and reruns the independent cross-check.

## Angles

- Extract each holdout's macro rules with an accelerated simulator. Many 'almost-Cryptids' reduce to a map with one parity split plus an exploitable invariant mod 2^k or mod 3^k (a finite automaton on residues), giving a proof by finite residue-class closure.
- 2-adic/3-adic invariants: show the orbit never enters the halting residue class by exhibiting a set of residues mod M closed under the map. Search M up to 2^20 x 3^10.
- Search for a Lyapunov/potential function as an integer linear combination of tape-block counters that strictly increases, using LP/ILP over symbolic rule effects.
- Cross-check with the Rocq repository's existing proof patterns and reuse their certificate format to make formal adoption easy.
- Auditing the pending AI Lean proofs is cheap and useful; finding a statement mismatch matters as much as confirming one.

## Pitfalls

- Bigfoot/Hydra are Collatz-hard; heuristic 'probviously' arguments do not count.
- Duplicating the active AI Lean campaign on BB(2,5).
- Equivalence classes: deciding one member may already be implied by a decided twin.
- 153/758 is flagged as a potential Cryptid, so expect Collatz-hardness.
- The 22 AI Lean proofs on BB(2,5) are unverified. Independently checking one is a useful contribution but is NOT a new decision.

## Sources

- https://wiki.bbchallenge.org/wiki/BB(3,3)
- https://wiki.bbchallenge.org/wiki/BB(2,5)
- https://wiki.bbchallenge.org/wiki/Holdouts_lists
- Status source: https://wiki.bbchallenge.org/wiki/BB(3,3)

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/number-hunts/bb33-bb25-cryptid-adjacent.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `bb33-bb25-cryptid-adjacent`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Number hunts]]
- [[V3R1T4S]]

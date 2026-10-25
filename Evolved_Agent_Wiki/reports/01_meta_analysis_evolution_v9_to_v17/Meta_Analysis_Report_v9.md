---
id: meta-analysis-v9
type: synthesis
tags: [meta, constitution, hall-of-fame]
inbound_links: 0
confidence: 0.9
last_ingested_sources: ["hall_of_fame/ancestor_v8_note.md", ".raw/V3R1T4S/kit/RUN.md", ".raw/V3R1T4S/kit/RULES.md"]
---
# Meta-Analysis Report v9 — v8 → v9 (Proofer Build)

# Overview

Trigger: the human's instruction of 2026-10-17 (role PROOFER; shell with autoresearch, verbalized sampling and postdiction with memory overwrite; Hall of Fame honours). This is not a reaction to user friction, so there is no revert advice. If v9 misbehaves, restore `hall_of_fame/ancestor_v8_*_snapshot.md` over `CONSTITUTION.md` / `CLAUDE.md` and delete `PROOFER.md`.

## Changes

| File | Change |
|---|---|
| `CONSTITUTION.md` | v9 header; §7.5 ceremony covers the whole shell; new §11 Proof Engine |
| `CLAUDE.md` | persona PROOFER; rule 9 Proof Mode |
| `PROOFER.md` | new: the full shell spec (precedence, ratchet, VS, postdiction, wiki↔lab loop) |
| `scripts/vs_sample.py` | new: VS validator + top-EV/tail sampler with logged seed |
| `scripts/postdict.py` | new: append-only prediction ledger, Brier/calibration report |
| `wiki/meta/beliefs.md`, `calibration.md` | new: overwritable belief state and its generated basis |

## Risks I see in my own design
- **Postdiction as rationalisation:** explaining failures after the fact can turn into HARKing. Mitigation: labelled `POSTDICTION`, never evidence, never touches PREREG or claims.
- **Ratchet as hidden multiple testing:** many keep/revert steps form a search. Mitigation: statistical metrics require the kit's ≥400-control null test.
- **Typicality numbers are self-reported:** VS diversity depends on honest typicality guesses. The random tail draw is the guard, not the numbers.
- **check_run.py compatibility:** extra files (`experiments.tsv`, `hypotheses.tsv`, `POSTDICTION.md`) live in run folders; they must never contain status words of the CONFIRMED family. To verify on the first dry run.

## Citations
- [kit/RUN.md](../../.raw/V3R1T4S/kit/RUN.md), [kit/RULES.md](../../.raw/V3R1T4S/kit/RULES.md), [kit/LESSONS.md](../../.raw/V3R1T4S/kit/LESSONS.md)
- Zhang et al., *Verbalized Sampling*, arXiv:2510.01171
- Karpathy, *autoresearch* (March 2026); known from secondary guides only, repo not opened

## Related Nodes
- [[V3R1T4S]]

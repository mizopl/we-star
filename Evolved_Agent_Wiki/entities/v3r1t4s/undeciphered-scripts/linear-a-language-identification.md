---
id: v3r1t4s-linear-a-language-identification
type: entity
tags: [v3r1t4s, v3r1t4s/undeciphered-scripts, kind/moonshot]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: undeciphered-scripts
kind: moonshot
tractability: 1
compute: "laptop-days / pure thought"
disclosure: open
status_checked: "2026-10-03"
---
# MOONSHOT: Linear A, identifying the Minoan language with predictive translations

# Overview

> Bank id `linear-a-language-identification` · moonshot · tractability 1 · laptop-days / pure thought · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Identify the language of Linear A and produce translations that predict unseen data. Phonetic values are approximately known via Linear B, but the language (Semitic, Luwian, Hurrian, Tyrsenian, isolate, or other) is unknown. Status as of 2026-10-03: Unsolved. The 2026 claims (Di Mino 'Ya Diktu', Tinitic Semitic, 508-entry lexicon, a September 2026 preprint) are unverified, and the independent check found that Hebrew-root matches are no better than scrambled controls. No accepted decipherment. kbennett2000/linear-a-check found that scrambled words match Hebrew roots nearly as well as real words for Di Mino's Sept 2026 preprint, holding across Hebrew, Ugaritic and invented root lists. Navarre-AI carries RILA Supplement 1 provenance on only 25 records.

## Success criterion

All of these must hold. (1) A lexicon and grammar frozen with a hash before testing; every gloss tested against logogram adjacency must have been derived without any logogram-context information, documented in the frozen lexicon's provenance. (2) On a held-out set chosen by a third-party seed as a 30% document split stratified by site (not just the 25 RILA records), the frozen grammar predicts morphology and logogram-consistent meanings. Example: words glossed as 'wine' precede the VIN logogram at least 80% of the time on held-out tablets. (3) Lexicon matches to the claimed language exceed all kbennett2000 cycle 6-8 controls (scrambled words, alternate root lists, invented roots, latitude count) with p < 0.001 after correcting for phonological latitude. (4) The translations of held-out accounting tablets are numerically coherent with KU-RO totals. Anything less is not a claim.

## Partial wins

- {"id": "p1", "statement": "A frozen lexicon of at least 3 commodity glosses derived without any logogram-context information (provenance documented) whose held-out logogram-adjacency predictions (e.g. 'wine' word precedes VIN) hold at least 80% of the time on the third-party-seeded, site-stratified 30% document split, with p < 0.001 against glosses permuted among the same words."}
- {"id": "p2", "statement": "A frozen lexicon whose matches to a single named candidate language exceed every kbennett2000 cycle 6-8 control (scrambled words, alternate root lists, invented roots, latitude count) with p < 0.001 after phonological-latitude correction, on held-out documents."}

## Verification

The verifier runs the kbennett2000/linear-a-check-style staged tests on the frozen lexicon, checks the hash and timestamp, applies the grammar to held-out documents itself, and scores logogram consistency automatically. Additionally, the verifier checks the provenance of each gloss for logogram-context leakage.

## Sources

- https://github.com/Navarre-AI/linear-a
- https://sigla.phis.me
- https://github.com/ftamburin/CSA_OptMatcher
- https://github.com/kbennett2000/linear-a-check
- Status source: https://github.com/Navarre-AI/linear-a

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/undeciphered-scripts/linear-a-language-identification.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `linear-a-language-identification`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Undeciphered scripts]]
- [[V3R1T4S]]

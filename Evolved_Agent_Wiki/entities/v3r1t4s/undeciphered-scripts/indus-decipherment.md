---
id: v3r1t4s-indus-decipherment
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
disclosure: commit-only
status_checked: "2026-10-03"
---
# MOONSHOT: Indus script, sign values or meanings that predict held-out seals

# Overview

> Bank id `indus-decipherment` · moonshot · tractability 1 · laptop-days / pure thought · disclosure **commit-only**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Assign phonetic or logographic values to Indus signs in a way that yields consistent readings in a specific language and predicts unseen inscriptions. Status as of 2026-10-03: Unsolved. The USD 1M Tamil Nadu prize (announced January 2025) is unclaimed and has no formal submission portal. Many 2025-2026 claims (Indo-Aryan, Dravidian, cryptanalytic) are unaccepted. paragorth/Indus- (September 2026) shows that decipherment validators accept wrong keys. Its 2026-09-25 correction found that with more than about 150 signs, wrong keys beat the true key under every objective tested; only small syllabaries (about 80 signs) let correct keys win.

## Success criterion

All of these must hold. (1) A frozen sign-to-value table. (2) The paragorth validator plus a planted-key test on synthetic corpora matched to the Indus scale (at least 400 sign types, frequency distribution matched to M77, mean text length about 5, about 4,000 texts): the method ranks the true key first against 100 random and 100 adversarially optimized wrong keys in at least 90% of synthetic replicates. (3) On a verifier-chosen held-out set of seals, the readings produce lexicon matches in the target language beyond scrambled-sign controls with p < 0.001. (4) It predicts at least 5 field-symbol or object-type correlations that are confirmed on the held-out set.

## Partial wins

- {"id": "p1", "statement": "Indus-scale planted-key recovery alone: a frozen method that, on verifier-generated synthetic corpora with at least 400 sign types, M77-matched frequency distribution, mean text length about 5 and about 4,000 texts, ranks the true key first against 100 random and 100 adversarially optimized wrong keys in at least 90% of replicates (paragorth 2026 found no objective that does this above about 150 signs)."}
- {"id": "p2", "statement": "A method that passes p1 and whose frozen sign-to-value table, applied to a verifier-chosen held-out set of seals, yields lexicon matches in a named target language beyond scrambled-sign controls with p < 0.001."}

## Verification

The verifier runs the validators in paragorth/Indus- and the joyboseroy null suite, does the planted-key recovery on synthetic data, and computes the held-out statistics with its own seeds. Additionally, the verifier generates the scale-matched synthetic corpora itself with fresh seeds.

## Sources

- https://github.com/paragorth/Indus-
- https://github.com/joyboseroy/indus_decipher
- http://www.indus.epigraphica.de
- Status source: https://github.com/paragorth/Indus-

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/undeciphered-scripts/indus-decipherment.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `indus-decipherment`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Undeciphered scripts]]
- [[V3R1T4S]]

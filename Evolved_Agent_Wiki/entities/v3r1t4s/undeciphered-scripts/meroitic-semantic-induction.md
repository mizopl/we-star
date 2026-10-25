---
id: v3r1t4s-meroitic-semantic-induction
type: entity
tags: [v3r1t4s, v3r1t4s/undeciphered-scripts, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: undeciphered-scripts
kind: standard
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Meroitic: meanings for unknown words from distribution, validated on held-out known words

# Overview

> Bank id `meroitic-semantic-induction` · standard · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Meroitic (Kush, Sudan, about 300 BCE to 400 CE) is phonetically readable in both hieroglyphic and cursive forms. Much of its vocabulary and grammar is unknown, and there is no sizable bilingual. Otten & Anastasopoulos (ALP 2025) released the first machine-readable Meroitic corpus and ran embedding and cross-lingual alignment experiments with Late Egyptian. The open task is to assign semantic classes or meanings to unknown words in a way that is validated, not interpretive. The corpus, embeddings and code are public at github.com/Joshua-Otten/Meroitic-Corpus. The known-meaning gloss set from Rilly is not machine-readable and must be hand-built. Status as of 2026-10-03: Partly understood. Rilly links Meroitic to North Eastern Sudanic. Computational work began in 2025, and no 2026 breakthrough was found.

## Success criterion

Two steps are required. (1) Validation: on words with known meanings (titles, deities, kinship terms, toponyms from Rilly's lexicon), hide each word's gloss and predict its semantic class from distribution alone. Top-1 class accuracy must be at least 2x the majority-class baseline, with permutation p < 0.001. (2) Discovery: the same frozen model assigns a class to at least 3 currently unglossed words with posterior at least 0.9. At least one of these must be corroborated by an independent signal the model never saw: an Egyptian or Greek loanword etymology, a determinative, or co-occurrence with an iconographic context recorded in REM metadata. Interpretive translations without step 1 do not count. Additionally: the known-gloss set (word, class, citation) is frozen and hashed before any model is fit; classes are fixed beforehand (at most 8); leave-one-out excludes all inflected variants of the held-out word.

## Partial wins

- {"id": "p1", "statement": "Step (1) alone: on the frozen, hashed known-gloss set (at most 8 pre-fixed classes, citations to Rilly), leave-one-out with all inflected variants excluded, top-1 semantic-class accuracy from distribution alone is at least 2x the majority-class baseline with permutation p < 0.001."}
- {"id": "p2", "statement": "Step (1) plus one discovery: the same frozen model assigns a class with posterior at least 0.9 to an unglossed word, and that class is corroborated by an independent signal the model never saw (Egyptian or Greek loanword etymology, a determinative, or iconographic context in REM metadata), with the corroboration not already published for that word."}

## Verification

The verifier clones Joshua-Otten/Meroitic-Corpus (pinned commit), rebuilds the frozen gloss set from cited Rilly pages, reruns leave-one-out with fresh seeds and the permutation test, and checks each corroboration source.

## Sources

- https://github.com/Joshua-Otten/Meroitic-Corpus
- https://aclanthology.org/2025.alp-1.11/
- https://aclanthology.org/2025.alp-1.11.pdf
- https://escholarship.org/uc/item/3128r3sw
- Status source: https://github.com/Joshua-Otten/Meroitic-Corpus

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/undeciphered-scripts/meroitic-semantic-induction.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `meroitic-semantic-induction`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Undeciphered scripts]]
- [[V3R1T4S]]

---
id: v3r1t4s-voynich-plaintext
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
compute: "laptop-days"
disclosure: open
status_checked: "2026-10-03"
---
# MOONSHOT: Voynich manuscript, a key that decrypts held-out folios into meaningful text

# Overview

> Bank id `voynich-plaintext` · moonshot · tractability 1 · laptop-days · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Find a key or procedure that maps Voynichese to plaintext in a natural language, and that generalizes to folios not used in building it. Status as of 2026-10-03: Unsolved as of 2026. Multiple 2026 claims (Delgado's Latin, a Galician reading) have no acceptance. The Naibbe cipher (2025) is a generation model, not a decryption.

## Success criterion

All of these must hold. (1) The key is fully specified and deterministic, or has bounded ambiguity of at most 2 readings per token, and is frozen before testing. (2) Applied unchanged to at least 10 held-out folios chosen by the verifier, it yields text whose per-character perplexity under a period language model (for example, a 15th-century Latin or Italian corpus) is at least 1.5 bits/char better than the same key applied to glyph-shuffled versions of those folios. (3) Key description length plus plaintext entropy is less than the entropy of the Voynich text under its best compressor (an MDL check against key overfitting). (4) At least 3 plant or star names decrypted on herbal or astro folios match identifications agreed by an independent botanist or astronomer reviewer who has not seen the claimed reading. (5) The frozen key applied to (a) Naibbe-cipher output encrypting a different language and (b) an arXiv 2604.19762-style slot-generator output must give per-character perplexity at least 1.0 bits/char worse than on the held-out Voynich folios. A key that 'decrypts' generated gibberish equally well is rejected.

## Partial wins

- {"id": "p1", "statement": "A frozen key (deterministic, at most 2 readings per token) that, on at least 10 verifier-chosen held-out folios, gives per-character perplexity under an independent period language model at least 1.5 bits/char better than on glyph-shuffled versions of those folios AND at least 1.0 bits/char better than on the verifier-generated structured-gibberish controls (Naibbe output of a different language; slot-generator output), i.e. criteria (2) and (5) without (3) and (4)."}
- {"id": "p2", "statement": "Blind illustration match alone: a frozen key decrypts at least 3 plant or star names on verifier-chosen herbal or astronomical folios that match identifications made independently by a botanist or astronomer reviewer who has not seen the claimed reading, while the same key applied to the structured-gibberish controls yields no such matches."}

## Verification

The verifier selects held-out folios with its own seed, runs the frozen key, and computes the perplexity against shuffled controls with an independent language model. It checks the MDL accounting and arranges the blind illustration-match review. Additionally, the verifier generates the structured controls itself with fresh seeds and scores them under the same period language model.

## Sources

- https://www.voynich.nu/data/ZL3b-n.txt
- https://www.voynich.nu/transcr.html
- https://github.com/greshko/naibbe-cipher
- https://arxiv.org/abs/2604.19762
- Status source: https://www.voynich.nu/data/ZL3b-n.txt

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/undeciphered-scripts/voynich-plaintext.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `voynich-plaintext`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Undeciphered scripts]]
- [[V3R1T4S]]

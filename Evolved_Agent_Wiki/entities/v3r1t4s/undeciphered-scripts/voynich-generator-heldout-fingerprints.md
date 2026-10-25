---
id: v3r1t4s-voynich-generator-heldout-fingerprints
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
# Voynich: a manually executable generator that matches held-out structural fingerprints, or a decisive falsification of the Naibbe cipher

# Overview

> Bank id `voynich-generator-heldout-fingerprints` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

The Voynich manuscript (Beinecke MS 408) is unread. It is still open whether the text is an enciphered natural language, a constructed system, or meaningless. Greshko's Naibbe cipher (Cryptologia, Nov 2025) is a verbose homophonic substitution of Latin/Italian, executable with cards and dice, that reproduces many Voynich statistics at once. Two 2026 papers add structural fingerprints that no generator was designed for. Parisel (arXiv 2604.25979) shows the Currier A/B split reduces to a per-folio boolean switch on the vowel after ch/sh. Rozanova & Temerev (arXiv 2608.17096) show that glyph regularity exceeds simple substitution, that structure concentrates at token edges, and that spaces form two regimes. The open sub-problem: does any historically plausible, hand-executable generator reproduce all known fingerprints, including ones not used in its design? Already published: Naibbe fails edge-glyph coupling (about 0.006 bits vs the manuscript's 0.197) and the singleton-type rate (about 41-42% vs about 70%) per arXiv 2608.17096 Table 7, independently reproduced by voynich-collective PR #16 (2026-09-19); slot and Cardan-grille generators fail the four-signature joint test calibrated per Currier dialect (arXiv 2604.19762, Apr 2026). Status as of 2026-10-03: Unsolved; no accepted decipherment as of 2026-10-03. The leading hand-executable generator, Naibbe (Greshko, Cryptologia 2025), matches glyph-level entropy, BPE gap and token order. It is published to fail edge-glyph coupling and the hapax-rich vocabulary (Rozanova & Temerev arXiv 2608.17096, Aug 2026; voynich-collective PR #16, Sept 2026). Slot and grille generators fail the 4-signature joint test (arXiv 2604.19762, Apr 2026).

## Success criterion

Two outcomes qualify. (A) A generator. It must reproduce, per Currier dialect (A and B separately) and on both ZL3b and IT2a, all of the following within the 95% envelope of the Voynich values: (i) the two Naibbe failure statistics as defined in 2608.17096, edge-glyph coupling (bits and share of entropy) and singleton-type rate; (ii) all four signatures of 2604.19762; (iii) Parisel's per-folio switch statistic. It must also reproduce at least 4 further pre-registered statistics never used in tuning (held out). It must be hand-executable: at most 200 table entries plus a written procedure, and at most 1 per-folio state bit beyond the tables. Run it on at least 20 plaintexts from at least 2 period languages x 10 seeds. If space-regime statistics are included, the generator must emit its own uncertain-space channel under a pre-declared rule. (B) A falsification of Naibbe on a pre-registered statistic NOT among edge-glyph coupling, singleton or hapax rate, the 2604.19762 signatures, or limitations in Greshko 2025. Naibbe output (unmodified author code, default parameters, at least 20 plaintexts x 10 seeds) must fall outside the 99.9% Voynich envelope on A and B and on both transliterations. Neither outcome is a decipherment. The 95% and 99.9% envelopes are computed at verification time from ZL3b-n.txt and IT2a-n.txt as then published; any generator or falsification published after 2026-10-03 that already achieves the claimed outcome voids novelty.

## Partial wins

- {"id": "p1", "statement": "A hand-executable generator (at most 200 table entries plus a written procedure, at most 1 per-folio state bit) whose output, over at least 20 plaintexts from at least 2 period languages x 10 seeds, falls inside the 95% Voynich envelope for BOTH Naibbe failure statistics of arXiv 2608.17096 (edge-glyph coupling in bits and share of entropy; singleton-type rate), on Currier A and B separately and on both ZL3b and IT2a, while staying inside the envelope on h2 conditional entropy and the word-length distribution."}
- {"id": "p2", "statement": "A hand-executable generator (same limits) that passes all four signatures of arXiv 2604.19762 jointly, per Currier dialect and on both transliterations, which the published slot and Cardan-grille generators fail."}
- {"id": "p3", "statement": "A single per-folio state bit added to the unmodified Naibbe tables (no other parameter change) that reproduces Parisel's (arXiv 2604.25979) per-folio ch/sh-vowel switch statistic inside the 95% envelope on Currier A and B and both transliterations, while not leaving the envelope on any statistic Naibbe already matches."}

## Verification

The verifier downloads ZL3b-n.txt and IT2a-n.txt (both returned HTTP 200 on 2026-10-03; record hashes) and parses IVTFF with Currier tags. It reimplements every statistic independently, including the 2608.17096 and 2604.19762 definitions, and confirms its reimplementation reproduces their published Voynich and Naibbe values before scoring the claim. It runs the submitted generator with its own plaintexts and seeds, checks the pre-registration timestamp in git, and for (B) runs greshko/naibbe-cipher unmodified.

## Sources

- https://www.voynich.nu/transcr.html
- https://www.voynich.nu/data/ZL3b-n.txt
- https://www.voynich.nu/data/IT2a-n.txt
- https://github.com/greshko/naibbe-cipher
- https://arxiv.org/abs/2604.25979
- https://arxiv.org/abs/2608.17096
- https://arxiv.org/abs/2604.19762
- https://github.com/SoylentAquamarine/voynich-collective/pull/16
- Status source: https://www.voynich.nu/transcr.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/undeciphered-scripts/voynich-generator-heldout-fingerprints.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `voynich-generator-heldout-fingerprints`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Undeciphered scripts]]
- [[V3R1T4S]]

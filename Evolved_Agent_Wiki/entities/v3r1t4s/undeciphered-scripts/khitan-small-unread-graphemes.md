---
id: v3r1t4s-khitan-small-unread-graphemes
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
tractability: 1
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Khitan small script: phonetic values for unread graphemes from Chinese loanwords and titles

# Overview

> Bank id `khitan-small-unread-graphemes` · standard · tractability 1 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Khitan small script (Liao dynasty, about 470 encoded characters, Unicode 13.0) is partly read: many phonetic values come from Chinese loanwords and official titles in the Kane/Chinggeltei tradition. A number of graphemes still have no secure value, and Khitan-Chinese parallel-text methods are reported to be at an impasse. Khitan large script is much further behind: about 10% of roughly 2,245 characters are fully read. The task is to predict values for unread graphemes and test those predictions on held-out loanword occurrences. No open machine-readable corpus of Khitan small script texts with aligned Chinese parallels was confirmed (BabelStone has only some texts), and the novelty check practically requires the Chinese-language literature (Inner Mongolia University school, Aisin-Gioro Ulhicun and others). Status as of 2026-10-03: Partly deciphered. Encoding and standardization progressed (China's 2025 large-script encoding proposal) and readings appeared in 2025 (Korean Association for Mongolian Studies). No full decipherment.

## Success criterion

A value for a grapheme listed as unread in Kane 2009 (the BabelStone list). The value must come from a frozen procedure, for example constraint solving over clusters that transcribe known Chinese titles and names in dated epitaphs. When substituted, it must produce at least 3 readings of Chinese loanwords or names in held-out clusters (not used for inference) that match Liao-period Chinese pronunciations, and random value permutation must give p < 0.01. The value must also not already be in the literature after Kane 2009. Additionally: training and held-out clusters are listed with source inscription and line before solving; the Liao-period northern Chinese reconstruction is fixed beforehand. Claim only as 'candidate value, novelty not cleared against the Chinese-language literature' unless a Chinese-language search (CNKI titles and abstracts) is documented.

## Partial wins

- {"id": "p1", "statement": "Method calibration: the frozen constraint solver, run with one grapheme value that was published after Kane 2009 withheld (the value and its source named beforehand), recovers that value from training clusters alone and confirms it on at least 3 held-out clusters with Liao-period Chinese matches, random value permutation p < 0.01."}
- {"id": "p2", "statement": "A frozen value for a grapheme listed as unread in Kane 2009 that yields at least 2 held-out Chinese loanword or name readings matching the pre-fixed Liao-period northern Chinese reconstruction, with random value permutation p < 0.01 and clusters listed with source inscription and line before solving (full criterion requires 3)."}

## Verification

The verifier re-derives the cluster transcriptions from BabelStone Unicode texts and Kane's character list, reruns the solver on the training clusters, and checks each held-out match against a Middle or Liao Chinese reconstruction and the parallel Chinese epitaph text. Additionally, the verifier re-derives the clusters from BabelStone Unicode texts at a pinned date and checks each held-out match against the parallel Chinese epitaph text.

## Sources

- https://www.babelstone.co.uk/Khitan/
- https://www.babelstone.co.uk/Fonts/KhitanSmall.html
- https://en.wikipedia.org/wiki/Khitan_Small_Script_(Unicode_block)
- https://www.unicode.org/wg2/docs/n5319-KhitanLargeScriptEncoding.pdf
- Status source: https://www.babelstone.co.uk/Khitan/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/undeciphered-scripts/khitan-small-unread-graphemes.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `khitan-small-unread-graphemes`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Undeciphered scripts]]
- [[V3R1T4S]]

---
id: v3r1t4s-chinese-gold-bars
type: entity
tags: [v3r1t4s, v3r1t4s/unbroken-ciphers, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: unbroken-ciphers
kind: standard
tractability: 1
compute: "laptop-minutes"
disclosure: open
status_checked: "2026-10-03"
---
# Chinese gold bar cryptograms (Shanghai, 1933)

# Overview

> Bank id `chinese-gold-bars` · standard · tractability 1 · laptop-minutes · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Seven 'gold bars' allegedly issued to a General Wang in Shanghai (1933) carry Chinese text about a transaction over $300,000,000, unknown script, and 16 distinct Latin-letter cryptogram lines of 8-25 letters. Several lines are repeated across bars, e.g. SKCDKJCDJCYQSZKTZJPXPWIRN, MQOLCSJTLGAJOKBSSBOMUPCE, RHZVIYQIYSXVNQXQWIOVWPJO, FEWGDRHDDEEUMFFTEEMJXZR, HFXPCQYZVATXAWIZPVE, VIOHIKNNGUAB. Letter statistics are very flat. Determine what the lines encode.

## Success criterion

CONFIRMED only if a single deterministic system and key (for example a period-appropriate polyalphabetic or commercial codebook) decodes ALL 16 lines (about 250 letters) into meaningful text (English, French, or romanized Chinese in Wade-Giles/Postal) that is coherent with the bars' Chinese inscriptions (amounts, bank, dates, names), with no per-line keys unless a documented indicator rule selects them. Alternatively, a decisive proof that the lines are produced by a specific identifiable generator, such as a published test-key or check-code scheme, where the generator reproduces all 16 lines exactly from bar data. The cryptograms must still be listed unsolved (Schmeh Top-50, IACR page) at verification time.

## Partial wins

- {"id": "p1", "statement": "A single identifiable generator (a published 1930s test-key, check-code or textbook scheme) that reproduces at least 4 distinct lines exactly from data on the bars, with the chance probability of that many exact reproductions under the searched generator space below 1e-6."}
- {"id": "p2", "statement": "A single deterministic system and key, with no per-line keys, that decodes at least 4 distinct lines (at least 80 letters in total) into meaningful text coherent with the bars' Chinese inscriptions, while the same system on shuffled-letter lines yields nothing comparable."}

## Verification

Use the IACR transcription, cross-checked against the bar photos on the IACR page. Implement the claimed system, decode all lines, check consistency with the translated Chinese text, and run a shuffled-letter null.

## Sources

- https://www.iacr.org/misc/china/cryptograms.html
- http://cipherfoundation.org/modern-ciphers/chinese-gold-bar-ciphers/chinese-gold-bar-transcription/
- Status source: https://www.iacr.org/misc/china/cryptograms.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/unbroken-ciphers/chinese-gold-bars.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `chinese-gold-bars`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Unbroken ciphers]]
- [[V3R1T4S]]

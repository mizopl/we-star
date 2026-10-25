---
id: v3r1t4s-mtc3-double-transposition-reloaded
type: entity
tags: [v3r1t4s, v3r1t4s/unbroken-ciphers, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: unbroken-ciphers
kind: harvest
tractability: 2
compute: "laptop-hours"
disclosure: commit-only
status_checked: "2026-10-03"
---
# MysteryTwister 'Double Column Transposition Reloaded' Parts 1-3 (0 solvers since 2013)

# Overview

> Bank id `mtc3-double-transposition-reloaded` · harvest · tractability 2 · laptop-hours · disclosure **commit-only**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

After George Lasry broke Schmeh's original Double Transposition Challenge in November 2013, Wacker, Esslinger and Schmeh published three harder Level III challenges that avoid the exploited weaknesses. Part 1: English plaintext, 613 letters, both keys 20-27 long and coprime, keys derived from English sentences; the answer is the first 34 plaintext letters. Part 2: two English texts interleaved word by word, keys 20-27, coprime and random; the answer is the first 37 letters. Part 3: German plaintext, 1006 letters, keys 27-34, coprime and random; the answer is the first 48 letters. MTC3 lists 0 solvers for each. These challenges were designed to defeat Lasry's published attack and have resisted the community, including Lasry, since 2013.

## Success criterion

CONFIRMED for a Part if the claim gives two transposition keys whose lengths satisfy that Part's stated ranges and coprimality, plus the exact columnar convention (irregular grid, row-wise fill, read-out by key order, tie-breaking rule; for Part 1 the sentence-to-key convention, frozen before declaring success). Decrypting the ENTIRE canonical ciphertext (the MTC3 ciphertext .txt, cross-checked against the PDF: Part 1 = 613 letters, Part 3 = 1006 letters, Part 2 measured and asserted) must give fluent English (Parts 1 and 2; for Part 2 both interleaved texts must read correctly when de-interleaved) or German (Part 3), with at least 97% of letters inside dictionary words and no edits, and re-encrypting that plaintext with the same keys must reproduce the ciphertext exactly. First-solve status is judged against the live solver count on https://mysterytwister.org/challenges/level-3/ at verification time. Only the human may submit the first-N-letters answer to MTC3.

## Partial wins

- {"id": "p1", "statement": "Blind Part-3-parameter benchmark: the verifier double-transposes 3 German texts of 1006 letters with random coprime keys of lengths 27-34 (MTC3 convention); the solver, ciphertext-only, recovers both keys and the full plaintext of at least 2 of the 3 with exact round-trip."}
- {"id": "p2", "statement": "Blind Part-1-parameter benchmark: the verifier double-transposes 3 English texts of 613 letters with coprime keys of lengths 20-27 derived from English sentences under a convention unknown to the solver; the solver recovers both keys and the full plaintext of at least 2 of the 3 with exact round-trip."}

## Verification

As written, plus assert extracted lengths of Part 1 = 613 and Part 3 = 1006 letters (Part 2 to be measured), using the MTC3 ciphertext .txt (e.g. /media/challenges/add/mtc3-wacker-08-DCTreloaded-01-ciphertext.txt) as the canonical source, cross-checked against the PDF. Only the human may submit the first-N-letters answer.

## Sources

- https://mysterytwister.org/media/challenges/pdf/mtc3-wacker-08-DCTreloaded-01-en.pdf
- https://mysterytwister.org/media/challenges/pdf/mtc3-wacker-09-DCTreloaded-02-en.pdf
- https://mysterytwister.org/media/challenges/pdf/mtc3-wacker-10-DCTreloaded-03-en.pdf
- https://mysterytwister.org/media/challenges/pdf/mtc3-schmeh-03-doppelwuerfel-en.pdf
- https://mysterytwister.org/media/challenges/add/mtc3-wacker-08-DCTreloaded-01-ciphertext.txt
- Status source: https://mysterytwister.org/media/challenges/pdf/mtc3-wacker-08-DCTreloaded-01-en.pdf

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/unbroken-ciphers/mtc3-double-transposition-reloaded.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `mtc3-double-transposition-reloaded`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Unbroken ciphers]]
- [[V3R1T4S]]

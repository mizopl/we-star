---
id: v3r1t4s-dorabella-1897
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
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Dorabella cipher (Elgar, 1897)

# Overview

> Bank id `dorabella-1897` · standard · tractability 1 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

An 87-character note of semicircle glyphs (24 distinct symbol types), sent by Edward Elgar to Dora Penny in July 1897. Transcribed by Schmeh as: ABCDE FGDHA IJKLJ MJJFB BJNGO GNIP / GJGFQ DHRSC JJCFN KGJIJ FTPKL QHHQI P / CPFUP CLUUN PCJFU KPNDB NPFDL ED. Modern MASC solvers that handle 87-letter English or Latin MASCs at about 98% succeed fail on it, which suggests it is not a plain monoalphabetic substitution. Find the method and plaintext.

## Success criterion

CONFIRMED only if ALL of the following hold. (1) A method family is declared BEFORE searching, from systems Elgar is documented to have known (for example Elgar's own Pigpen-like cipher notes, Playfair, keyword substitution with transposition), with total key bits stated. (2) The method decrypts all 87 symbols to grammatical English with at most 2 exceptions. (3) Key bits are below 0.5 x 87 x 3.2 ≈ 140, or else an external corroboration such as the key written in Elgar's papers. (4) Across 1000 random 87-symbol strings with the same symbol-frequency profile, the same solver never achieves comparable fluency. The cipher must still show 0 solvers on MTC3 Level X at verification time.

## Partial wins

- {"id": "p1", "statement": "Archival corroboration: a citable document in Elgar's papers or correspondence (archive, shelfmark, scan) that gives a key, method or plaintext for the Dorabella note, which a skeptic can open and apply to the 87-symbol MTC3 transcription."}
- {"id": "p2", "statement": "Over-budget candidate: a method family declared before searching and a key that decrypts all 87 symbols to grammatical English with at most 2 exceptions and passes the 1000-string frequency-matched null, but with key bits between 140 and 200 (failing only criterion (3)); reported as candidate, not confirmed."}

## Verification

Use Schmeh's MTC3 transcription and check it against the original image. Implement the method independently, decrypt, check grammar and word coverage, recompute key bits, and run the frequency-matched random-string null.

## Sources

- https://mysterytwister.org/media/challenges/pdf/mtc3-schmeh-01-dorabella-en.pdf
- https://en.wikipedia.org/wiki/Dorabella_Cipher
- https://ciphermysteries.com/other-ciphers/the-dorabella-cipher
- Status source: https://mysterytwister.org/media/challenges/pdf/mtc3-schmeh-01-dorabella-en.pdf

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/unbroken-ciphers/dorabella-1897.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `dorabella-1897`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Unbroken ciphers]]
- [[V3R1T4S]]

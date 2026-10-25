---
id: v3r1t4s-mtc3-hutton-cipher-part-5
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
tractability: 3
compute: "laptop-hours"
disclosure: commit-only
status_checked: "2026-10-03"
---
# MysteryTwister 'The Hutton Cipher – Part 5' (4,250-letter ciphertext-only, 0 solvers since 2023)

# Overview

> Bank id `mtc3-hutton-cipher-part-5` · harvest · tractability 3 · laptop-hours · disclosure **commit-only**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Eric Bond Hutton's 2018 pen-and-paper cipher: a repeating keyword K1 and a keyword-mixed alphabet from K2. For each letter, the shift is n = rank(K1[i mod |K1|]) + rank(current first letter of the alphabet). The plaintext letter is swapped with the letter n places to its right, and that letter is output, so the alphabet mutates every step. Part 5 is a ciphertext-only challenge with contemporary English plaintext, numerals spelled out, spaces and punctuation removed, and both keywords random strings under 10 letters. The ciphertext file hutton_ciphertext_5.txt holds 4,250 A-Z letters (4,272 bytes including 22 newlines) with IC 0.0385. Recover the plaintext and both keywords.

## Success criterion

CONFIRMED if keywords K1 and K2 (each under 10 letters) are given such that the Hutton procedure exactly as specified in the PDF decrypts the ENTIRE 4,250-letter ciphertext to fluent contemporary English with ≥97% of letters in dictionary words and zero edits, and re-encryption with the same keys reproduces the ciphertext byte for byte. Key space is about 85 bits against about 13,000 bits of plaintext redundancy, so a fluent full decrypt is decisive. Final external confirmation comes when the human submits on MTC3. First-solve status is judged against the live solver count on https://mysterytwister.org/challenges/level-2/ at verification time. Only the human submits to MTC3.

## Partial wins

- {"id": "p1", "statement": "Reduced blind benchmark: the verifier enciphers 3 contemporary English texts of 4,250 letters with the Part 5 procedure (verified on the PDF example) under random keywords K1, K2 of fewer than 10 letters, disclosing only |K1| and |K2|; the solver recovers both keywords and the full plaintext of at least 2 of the 3, checked by exact re-encryption."}
- {"id": "p2", "statement": "Full blind benchmark: as above but with keyword lengths undisclosed; the solver recovers both keywords and the full plaintext of at least 2 of the 3, ciphertext-only, checked by exact re-encryption."}

## Verification

Implement Hutton exactly per the PDF and check it reproduces the PDF example: MEETMEATTHEGREENMANATTHREE with FEDORA/JUPITER gives RSBIENXONGQYTMWQVWXWIOKXKU. An auditor implementation already round-trips this. Download the add.zip, strip newlines and assert 4,250 letters. Decrypt with the claimed keys, re-encrypt and diff, then run a dictionary-coverage check.

## Sources

- https://mysterytwister.org/media/challenges/pdf/mtc3-hutton-01-hutton-05-en.pdf
- https://mysterytwister.org/media/challenges/add/mtc3-hutton-01-hutton-05-add.zip
- https://eprint.iacr.org/2023/1113
- Status source: https://mysterytwister.org/media/challenges/pdf/mtc3-hutton-01-hutton-05-en.pdf

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/unbroken-ciphers/mtc3-hutton-cipher-part-5.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `mtc3-hutton-cipher-part-5`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Unbroken ciphers]]
- [[V3R1T4S]]

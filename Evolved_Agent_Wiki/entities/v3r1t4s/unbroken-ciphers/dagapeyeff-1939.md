---
id: v3r1t4s-dagapeyeff-1939
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
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# D'Agapeyeff cipher (1939 textbook challenge)

# Overview

> Bank id `dagapeyeff-1939` · standard · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

A 395-digit challenge cipher from the first edition of Alexander D'Agapeyeff's 'Codes and Ciphers' (1939), dropped from later editions; the author reportedly later forgot how he made it. Read as digit pairs it gives 197 pairs plus one leftover digit (196 pairs if the trailing '000' padding is discarded), with 19 distinct pairs drawn almost entirely from rows 6-9 and columns 1-5, plus the anomalous '04' (from ...63630 47481...) and '00' (from the trailing '92000'). This suggests a Polybius-square stage. It has an unusually flat distribution and a low pairs IC. D'Agapeyeff described nulls inserted every third, fourth or fifth letter as one technique. Find the method and plaintext.

## Success criterion

CONFIRMED only if ALL of the following hold. (0) The canonical input is the full 395-digit string from the MTC3 PDF; the treatment of the trailing '000' and of the irregular pair '04' is declared before searching, and counts toward the error budget in (2) if they are treated as slips. (1) The method is a single procedure from D'Agapeyeff's 1939 book, with page reference, using only techniques of the type it teaches (Polybius squares, keyword alphabets, columnar transposition, nulls at a fixed rule, Playfair-like digraphic substitution), fully specified with all keys and no rule changes mid-text. (2) It deterministically maps the ENTIRE ciphertext to grammatical English (or French/Russian if argued), with at least 95% of letters in words and at most 4 declared encipherment errors, each explainable as a single slip. (3) Key-space accounting: the bits in all keys combined must be below 0.6 x (decoded plaintext length x 3.2 bits). (4) The same pipeline on 500 shuffled versions of the ciphertext never yields comparable English. (5) The cipher is still listed unsolved on Wikipedia and MTC3 Level X (0 solvers) at verification time; unverified public claims (e.g. the Nov 2025 comment) do not count as prior solutions unless they meet (0)-(4).

## Partial wins

- {"id": "p1", "statement": "A single procedure from the 1939 book (page cited) with fully specified keys that decrypts at least 100 consecutive pairs to English with at least 95% word coverage and at most 2 declared slips, satisfies the key-bit bound (3) for that segment, and passes the 500-shuffle null on that segment."}
- {"id": "p2", "statement": "Near-solve: a method and key meeting (0), (1), (3), (4) that decrypts the entire ciphertext to English with at least 95% word coverage but needs 5-8 declared single-slip errors (exceeding the 4-error budget)."}

## Verification

Extract the digits from the MTC3 PDF with pdftotext and assert 395 digits. Apply the declared padding rule, implement the claimed method independently, decrypt, measure coverage, recompute key bits and run the 500-shuffle null.

## Sources

- https://mysterytwister.org/media/challenges/pdf/mtc3-schmeh-02-agapeyeff-en.pdf
- https://en.wikipedia.org/wiki/D%27Agapeyeff_cipher
- Status source: https://mysterytwister.org/media/challenges/pdf/mtc3-schmeh-02-agapeyeff-en.pdf

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/unbroken-ciphers/dagapeyeff-1939.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `dagapeyeff-1939`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Unbroken ciphers]]
- [[V3R1T4S]]

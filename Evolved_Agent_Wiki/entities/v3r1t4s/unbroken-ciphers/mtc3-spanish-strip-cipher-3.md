---
id: v3r1t4s-mtc3-spanish-strip-cipher-3
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
disclosure: commit-only
status_checked: "2026-10-03"
---
# MysteryTwister Spanish Strip Cipher Part 3 (Spanish Civil War telegram, 0 solvers)

# Overview

> Bank id `mtc3-spanish-strip-cipher-3` · standard · tractability 2 · laptop-hours · disclosure **commit-only**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

An original Spanish Civil War telegram (summer or fall 1936), apparently encrypted with the Spanish Strip Cipher (SSC): a homophonic substitution where a keyword-derived, shifted random alphabet assigns each plaintext letter to a column of 3-5 two-digit homophones; the challenge hint allows an alphabet that includes LL and CH and may omit W. The ciphertext is 142 two-digit tokens with 55 distinct values (range 02-98). The plaintext is most likely Spanish, possibly Basque. MTC3 Level X (published 2014-03-27) lists 0 solvers.

## Success criterion

The challenge must still show 0 solvers on https://mysterytwister.org/challenges/level-x/ at verification time for a first-solve claim. CONFIRMED only if ALL of the following hold. (1) The homophone-to-letter key respects the SSC structure as the PDF hints allow it: 3-5 homophones per column; an ordered alphabet that may include LL and CH and may omit W; a keyword-derived random alphabet plus an initial shift, with the variant declared before searching. (2) All 142 tokens decrypt to coherent Spanish or Basque telegraphic text, with at least 90% of letters in words or telegram abbreviations and at most 3 declared garbles. (3) Key-entropy accounting: with 55 distinct homophones, a free mapping costs about 55 x log2(28) ≈ 264 bits, against roughly 142 x 3 ≈ 426 bits of plaintext redundancy. Free mappings are therefore marginal. A claim must either derive the mapping from a keyword-and-shift table structure (≤ about 100 bits) or pass (4) by a wide margin. (4) Null: 200 random token sequences matched on length and repeat profile never reach comparable fluency. (5) Content is plausible for summer or fall 1936.

## Partial wins

- {"id": "p1", "statement": "A structured key (keyword-derived alphabet plus shift plus table layout, at most about 100 bits, variant declared before searching) under which at least 100 consecutive tokens decrypt to Spanish or Basque telegraphic text with at least 90% coverage and at most 2 declared garbles, while 200 length- and repeat-profile-matched random token sequences never reach comparable fluency."}
- {"id": "p2", "statement": "Blind benchmark: the verifier enciphers 3 period-style Spanish telegrams of 142 tokens under randomly drawn SSC variants within the PDF's allowed space (3-5 homophones per column, optional LL/CH, optional W); the solver recovers at least 95% of plaintext letters of at least 2 of the 3."}

## Verification

Extract the tokens with pdftotext from pages 9/10 of the PDF and assert 142 tokens and 55 distinct values. Check the structural constraints programmatically under the declared variant, then score with Spanish and Basque lexica and run the null.

## Sources

- https://mysterytwister.org/media/challenges/pdf/mtc3-sanguino-03-SSC-03-en.pdf
- https://www.mysterytwisterc3.org/en/challenges/level-x/spanish-strip-cipher-part-3
- Status source: https://mysterytwister.org/media/challenges/pdf/mtc3-sanguino-03-SSC-03-en.pdf

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/unbroken-ciphers/mtc3-spanish-strip-cipher-3.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `mtc3-spanish-strip-cipher-3`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Unbroken ciphers]]
- [[V3R1T4S]]

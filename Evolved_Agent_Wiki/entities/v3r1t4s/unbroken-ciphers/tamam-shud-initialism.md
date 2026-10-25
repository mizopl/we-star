---
id: v3r1t4s-tamam-shud-initialism
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
# Somerton Man (Tamam Shud) code: exact initialism source search

# Overview

> Bank id `tamam-shud-initialism` · standard · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

The pencilled code from the back of the Rubaiyat in the 1948 Somerton Man case reads: W(M?)RGOABABD / [struck] MLIAOI / WTBIMPANETP / MLIABO AIAQC / ITTMTSAMSTGAB, with an 'X' over one O. Abbott's group judged it most likely the initial letters of words, while Rehling (2014) suggested shorthand that is unrecoverable. The man was identified in 2022 as Carl 'Charles' Webb, but the code remains unbroken. The target: find the exact source text, if it is an initialism of a published text, or another deterministic decoding. Lines 1, 3, 4 and 5 total 44 letters (9 + 11 + 11 + 13).

## Success criterion

CONFIRMED only if the claim exhibits a text demonstrably published before December 1948, with exact edition, whose consecutive word initials reproduce at least 40 of the 44 letters of lines 1, 3, 4 and 5 in order, allowing only the documented M/W ambiguity plus at most 2 further mismatches, with each line mapping to a contiguous passage. In addition, the expected number of such matches in the searched corpus under a word-initial-frequency model must be below 1e-4 (report corpus size in word positions). Free-form 'phrase invention' (making up a sentence per letter) is never acceptable. If lines are matched to different passages, the chance expectation is computed per line and combined (product of per-line expectations times the number of passage combinations considered), and the combined expectation must be below 1e-4. M/W and crossed-out-line handling is declared before searching.

## Partial wins

- {"id": "p1", "statement": "One full line (line 3, 4 or 5; 11-13 letters) matched by the consecutive word initials of a single contiguous passage in a text demonstrably published before December 1948, with at most 1 mismatch, and a per-line chance expectation below 1e-4 over the reported corpus size in word positions."}
- {"id": "p2", "statement": "Two different lines each matched (at most 2 mismatches each) by contiguous passages of the SAME pre-December-1948 work, with the combined chance expectation (per-line expectations multiplied, times the number of within-work position pairs considered) below 1e-4."}

## Verification

Obtain the source passage from an independent digitized copy (HathiTrust, Internet Archive, Trove). Compute word initials with a script and align them to the code with the allowed mismatches. Recompute the chance-match expectation from initial-letter frequencies and the stated corpus size.

## Sources

- https://en.wikipedia.org/wiki/Somerton_Man
- https://trove.nla.gov.au/
- Status source: https://en.wikipedia.org/wiki/Somerton_Man

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/unbroken-ciphers/tamam-shud-initialism.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `tamam-shud-initialism`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Unbroken ciphers]]
- [[V3R1T4S]]

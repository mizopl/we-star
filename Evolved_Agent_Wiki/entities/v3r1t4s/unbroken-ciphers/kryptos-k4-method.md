---
id: v3r1t4s-kryptos-k4-method
type: entity
tags: [v3r1t4s, v3r1t4s/unbroken-ciphers, kind/moonshot]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: unbroken-ciphers
kind: moonshot
tractability: 1
compute: "laptop-hours"
disclosure: commit-only
status_checked: "2026-10-03"
---
# Kryptos K4: recover the encryption METHOD (plaintext known only to Sanborn and archive owners)

# Overview

> Bank id `kryptos-k4-method` · moonshot · tractability 1 · laptop-hours · disclosure **commit-only**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

K4 is the 97-letter final section of Jim Sanborn's Kryptos at CIA HQ (Wikipedia gives OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR; verify the 97-character length). Sanborn's public clues fix positions 22-34 to EASTNORTHEAST and 64-74 to BERLINCLOCK (1-indexed). In Sept 2025 Jarett Kobek and Richard Byrne found the K4 plaintext in Smithsonian archive scraps. They do not intend to release it, and Sanborn says 'K4 has not been solved... discovered', with the method known only to Sanborn and Scheidt. RR Auction sold the full archive (plaintext, coding system, K5 materials) on 20 Nov 2025 for $962,500. The buyer, Paradigm, announced on 12 Jun 2026 a sealed SHA-256 plus Google Cloud KMS verification oracle that accepts K4 plaintext guesses for $1 each, without publishing plaintext or method. The open problem is the cryptanalytic method that maps the ciphertext to a plaintext consistent with all cribs. The oracle is reached through the CTF site and requires an account plus payment, so it is strictly a human-only action.

## Success criterion

CANDIDATE (not a confirmed result): one fully specified deterministic method with key bits ≤ 60 maps all 97 letters such that positions 22-34 = EASTNORTHEAST and 64-74 = BERLINCLOCK exactly, the remaining 73 letters reach ≥ 85% English word coverage, there are no per-position exceptions, AND the same method family run against 1000 random 97-letter strings never satisfies both cribs plus that coverage. CONFIRMED: only after the human submits the candidate to Paradigm's official K4 oracle and reports a positive verdict. Agents never create accounts, pay, or submit.

## Partial wins

- {"id": "p1", "statement": "CANDIDATE tier exactly as defined in the success criterion: one deterministic method with key bits at most 60, both cribs exact at positions 22-34 and 64-74, remaining 73 letters at least 85% English word coverage, no per-position exceptions, and the 1000-random-string null never satisfied."}
- {"id": "p2", "statement": "Crib-only constraint hit: a single fully specified method with key bits at most 60 that reproduces all 24 crib letters at their exact positions, where the identical method-family search over 1000 random 97-letter strings never satisfies both cribs; reported as a structural finding, never as a plaintext claim."}

## Verification

Re-derive the ciphertext from the Wikipedia K4 string and assert 97 letters. Implement the method independently, decrypt, and assert the crib positions. Compute key bits and check that a 1000-run search of the same method family against random 97-letter strings cannot hit both cribs plus readable English. Final step: the human submits the plaintext to paradigm.xyz/kryptos-ctf and reports the oracle verdict.

## Sources

- https://en.wikipedia.org/wiki/Kryptos
- https://paradigm.xyz/kryptos-ctf
- https://www.paradigm.xyz/writing/kryptos
- Status source: https://en.wikipedia.org/wiki/Kryptos

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/unbroken-ciphers/kryptos-k4-method.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `kryptos-k4-method`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Unbroken ciphers]]
- [[V3R1T4S]]

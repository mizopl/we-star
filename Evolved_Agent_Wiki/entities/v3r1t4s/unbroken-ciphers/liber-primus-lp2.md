---
id: v3r1t4s-liber-primus-lp2
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
# Cicada 3301 Liber Primus: unsolved runic pages

# Overview

> Bank id `liber-primus-lp2` · moonshot · tractability 1 · laptop-hours · disclosure **commit-only**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

The Liber Primus (2014) is a runic book in Cicada's Gematria Primus (29 runes). Its early pages were decrypted (Vigenère with DIVINITY or FIRFUMFERENFE keys, Atbash/shift, and a totient-of-primes stream). The remaining pages, about 12,956 runes (56 of 58 LP2 pages by one count), are unsolved. Their statistical signature is near-uniform with strongly suppressed adjacent repeats (86 observed against 447 expected, i.e. 0.66-0.68% against 3.45%), and no periodicity. Recover any unsolved page.

## Success criterion

CONFIRMED only if a deterministic, fully specified key or keystream rule decrypts at least one complete unsolved page section (at least 150 consecutive runes) into English (Cicada's archaic style acceptable) with at least 90% word coverage. The same rule family must also reproduce at least one already-solved section, and the claim must pass the Dukotah repo's verify_solution.py oracle after its --selftest succeeds. Running the rule on rune-shuffled pages must not give English. verify_solution.py is a community tool, so passing it is necessary but not sufficient: an independent re-implementation by the verifier must reproduce the decrypt. The target page must still be listed unsolved in the Dukotah repo at verification time.

## Partial wins

- {"id": "p1", "statement": "A deterministic, fully specified rule that decrypts 50-149 consecutive runes of an unsolved page to English with at least 90% word coverage, reproduces at least one already-solved section with the same rule family, and gives no English on rune-shuffled copies of that page."}
- {"id": "p2", "statement": "A deterministic rule that decrypts at least 150 consecutive runes of an unsolved page to English with at least 90% word coverage, verified by an independent re-implementation and failing on shuffled pages, but whose rule family does not reproduce any already-solved section; reported as candidate."}

## Verification

Clone Dukotah/cicada3301, run verify_solution.py --selftest, then run it on the claimed key. Independently re-transcribe the target page from the byte-verified source images (SHA1 matches listed in the repo). Decrypt with the verifier's own Gematria Primus implementation and score English.

## Sources

- https://github.com/Dukotah/cicada3301
- https://github.com/Leo-Y-Zhang/LiberPrimusAnalysis
- https://www.boxentriq.com/guides/cicada-3301-liber-primus
- Status source: https://github.com/Dukotah/cicada3301

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/unbroken-ciphers/liber-primus-lp2.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `liber-primus-lp2`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Unbroken ciphers]]
- [[V3R1T4S]]

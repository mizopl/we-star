---
id: v3r1t4s-debosnys-1883
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
# Henry Debosnys cryptograms (1882-83)

# Overview

> Bank id `debosnys-1883` · standard · tractability 1 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Henry Debosnys, executed in 1883 for murdering his wife in Essex County NY, left several enciphered documents and poems in a symbol script. One transcription counts 1,188 glyph instances of 425 glyph types; another treats glyphs as composed of subglyphs (possibly syllables). Nobody has decrypted a single word. It is #3 on Schmeh's Top-50.

## Success criterion

CONFIRMED only if a single subglyph or glyph-to-sound/letter mapping, fixed across ALL documents, yields readable text in a natural language (French, English, Portuguese or Spanish, all plausible for Debosnys) over at least 300 consecutive glyph instances, with at least 85% word coverage. Any poem must keep plausible meter or rhyme, and a held-out document never used in fitting must decode with the same mapping. All decoding is against a transcription frozen with a SHA-256 hash BEFORE any fitting (Sektu's if obtainable, or a new one from Cipher Foundation scans, made blind to the solver), and the cryptograms must still be listed unsolved at verification time.

## Partial wins

- {"id": "p1", "statement": "A glyph or subglyph mapping fitted on one document that, frozen and applied to a held-out document of the hashed transcription, decodes at least 100 consecutive glyph instances to a natural language with at least 85% word coverage and beats a mapping-shuffle null at p < 1e-4."}
- {"id": "p2", "statement": "Identification of a specific published 19th-century shorthand system (e.g. Duployé, Prévost-Delaunay, Pitman) whose direct transliteration, with the sign table taken from a cited manual and not fitted, yields readable text for at least 50 consecutive glyph instances of a held-out document, beating a sign-shuffle null at p < 1e-4."}

## Verification

First freeze a transcription with its SHA-256: either Sektu's, if obtainable, or a new one from Cipher Foundation scans made before any decipherment attempt and blind to the solver. Fit on one document, apply the frozen mapping to a held-out document, measure language coverage, and compare against a mapping-shuffle null.

## Sources

- http://cipherfoundation.org/older-ciphers/debosnys-ciphers/
- https://sektu.blogspot.com/2017/08/debosnys-cipher-transcription-revision.html
- Status source: http://cipherfoundation.org/older-ciphers/debosnys-ciphers/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/unbroken-ciphers/debosnys-1883.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `debosnys-1883`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Unbroken ciphers]]
- [[V3R1T4S]]

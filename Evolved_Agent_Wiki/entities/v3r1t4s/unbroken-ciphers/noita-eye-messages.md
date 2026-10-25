---
id: v3r1t4s-noita-eye-messages
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
tractability: 2
compute: "laptop-hours"
disclosure: commit-only
status_checked: "2026-10-03"
---
# Noita Eye Messages (designed game cipher, developer-confirmed real)

# Overview

> Bank id `noita-eye-messages` · moonshot · tractability 2 · laptop-hours · disclosure **commit-only**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Nine messages of eye glyphs in five orientations (5 East, 4 West) in the game Noita (2020). Read as trigrams in base 5, they give an 83-symbol alphabet with values 0-82 and no gaps. Known structure includes no immediately doubled trigrams, shared aligned sections and isomorphs across messages, and a distinct first character per message. The developers say the messages contain a real message. The leading model is a deck or group-autokey style polyalphabetic cipher over S_83. Recover the plaintext and method. The developers' 'real message' confirmation is older; wiki.gg (updated May 2026) shows no new developer statement.

## Success criterion

CONFIRMED only if a single fully specified algorithm and key (or key-derivation rule) decrypts ALL nine messages from the community's standard trigram transcription into readable text in a natural language (English or Finnish most likely). Each message must have at least 90% of characters in dictionary words. The method must reproduce the observed isomorph alignments and the no-doubles property as consequences, and must not use per-message ad hoc tables. Decrypting with the same method on symbol-shuffled messages must give no readable text. The puzzle must still be listed unsolved on the community tracker at verification time.

## Partial wins

- {"id": "p1", "statement": "Frozen held-out structure prediction: a fully specified cipher family and key-update rule fitted on at most 8 of the 9 messages (fitting set and model hash committed before the held-out message is scored) that predicts specific symbol relations in the held-out message beyond the already-documented isomorphs and alignments, with those predictions holding at p < 1e-6 against a shuffled-message null."}
- {"id": "p2", "statement": "A single fully specified algorithm and key that decrypts at least one complete message (from the standard trigram transcription) to a natural language with at least 90% dictionary-word coverage, reproduces the no-doubles property as a consequence, and gives no readable text on symbol-shuffled messages, even if it does not yet decrypt all nine."}

## Verification

Take the transcription from the wiki or community data files, re-derive the trigram values with the verifier's own parser from the glyph orientation data, implement the claimed algorithm, decrypt all 9, check language coverage, check the isomorph-explanation property, and run the shuffled null.

## Sources

- https://noita.wiki.gg/wiki/Eye_Messages
- https://unsolved-puzzles.github.io/unsolved-puzzles/noita/eye-puzzle.html
- https://noita.fandom.com/wiki/Eye_Messages
- Status source: https://noita.wiki.gg/wiki/Eye_Messages

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/unbroken-ciphers/noita-eye-messages.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `noita-eye-messages`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Unbroken ciphers]]
- [[V3R1T4S]]

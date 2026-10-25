---
id: v3r1t4s-ultimate-enigma-challenge
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
# CryptoCellar 'Ultimate Enigma Challenge' (5 Sept 1941 messages, possibly non-standard machine)

# Overview

> Bank id `ultimate-enigma-challenge` · moonshot · tractability 1 · laptop-hours · disclosure **commit-only**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Five messages with Enigma-style indicators but unusual operators, comments and very low radio frequencies: QTXMA and SZAEJ (29.09.1941) and BYQMZ, FKQLZ and XFEDT (30.09.1941). The ultimate-enigma.html page gives raw character counts including headers (280/129/308/198/226); the unbroken overview gives cipher letters for the 30.09 messages only (BYQMZ 167, FKQLZ 107, XFEDT 97); cipher-letter counts for QTXMA and SZAEJ are unverified. Weierud suspects a police network (Ordnungspolizei) and possibly a machine with different wheel wiring. Every attack since 2003-2004 has failed. Break any of them.

## Success criterion

CONFIRMED only if a fully specified machine (wiring of all wheels and reflector, stepping, plugboard) and ONE daily key decrypt at least TWO messages of the SAME date (two of BYQMZ, FKQLZ, XFEDT for 30.09, or QTXMA plus SZAEJ for 29.09) to German with at least 85% coverage. Garbles are pre-declared and at most 10%. Both indicators must decrypt consistently to their message keys. Any non-standard wiring must be a documented historical wiring or be derived once and then held fixed across both messages. Shuffled nulls are run per message. The messages must still be shown unbroken on https://www.cryptocellar.org/bgac/ultimate-enigma.html at verification time.

## Partial wins

- {"id": "p1", "statement": "Single-message machine break: a fully specified machine of documented historical wiring (e.g. Enigma I, Enigma G, Railway Enigma, Swiss K) and key under which one message of at least 97 cipher letters (BYQMZ, FKQLZ or XFEDT) has a consistent indicator and decrypts to German with at least 85% coverage, garbles pre-declared and at most 10%, and the shuffled null for that message far below the claim, without yet a second same-date message."}
- {"id": "p2", "statement": "Single-message hand-cipher break: a fully specified hand system (e.g. Doppelkasten or a police transposition) and key that decrypts one of the 30.09 messages to German with at least 85% coverage, at most 10% pre-declared garbles, key bits below half the message's redundancy (message length x 3.2 bits / 2), and a per-message shuffled null far below the claim."}

## Verification

Re-extract the ciphertext from ultimate-enigma.html and separate header from cipher groups, asserting letter counts against the unbroken overview (167/107/97 for the 30.09 messages). Implement the machine independently, check the indicators and run the nulls.

## Sources

- https://www.cryptocellar.org/bgac/ultimate-enigma.html
- Status source: https://www.cryptocellar.org/bgac/ultimate-enigma.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/unbroken-ciphers/ultimate-enigma-challenge.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ultimate-enigma-challenge`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Unbroken ciphers]]
- [[V3R1T4S]]

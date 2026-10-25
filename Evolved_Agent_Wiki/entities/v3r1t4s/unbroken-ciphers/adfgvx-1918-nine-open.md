---
id: v3r1t4s-adfgvx-1918-nine-open
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
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# The nine still-open 1918 ADFGVX radiograms (Childs collection, Lasry/Schmeh 2017 challenge)

# Overview

> Bank id `adfgvx-1918-nine-open` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

In February 2017 George Lasry and Klaus Schmeh published 22 German ADFGVX radiograms (Nov-Dec 1918, J. Rives Childs collection) that resisted Lasry's large-scale break (Lasry, Niebel, Kopal and Wacker, Cryptologia 41(2), 2017). ADFGVX is a 6x6 Polybius substitution followed by columnar transposition with daily keys. Per the community repo github.com/0wwafa/adfgvx-1918 (Sept 2026), 12 are read (p.100, 105, 109, 132, 146, 164 (two partials), 171, 176, 187 (two parts), 215, 217) and 9 remain open; p.217 (keyword TRUPPENVERSCHIEBUNG) was credited to 'prinz' with GPT-6 Astra in Sept 2026 and independently verified by the swarm-ai-research group, though its key is dated 9 Dec 1918, twelve days after the message. The README does not list the nine open IDs; take them from the repo's docs/REPORT.md and messages.py. The repo's own two-edit exhaustive and beam searches have already failed on these nine. Decrypt any of the nine. Schmeh's Top-50 ranks unsolved ADFGVX cryptograms #46.

## Success criterion

CONFIRMED only if ALL of the following hold. (0) The target ID appears as open in the repo's docs/REPORT.md on the day of the attempt. (1) The key (Polybius square plus transposition key) is either a documented 1918 daily key for the message's date window, or a newly recovered key that ALSO decrypts at least one other message of the same date window to German. A key taken from a date window that does not contain the message must be flagged, and is CONFIRMED only if it also decrypts a second message or the plaintext matches an external historical record. (2) The decrypt of the archived transcription is German military or diplomatic text with at least 85% word coverage. (3) Edits are at most 4% of symbols or 3 edits, whichever is larger, each a plausible transcription or transmission error (for example adjacent ADFGVX letter confusion, or a dropped or duplicated column cell), and every edit is listed. (4) Multiple-comparison control: the total hypothesis count (keys x edit-sets x column-offset variants) is reported, and the claimed German score exceeds the best score over the same search on wrong-key controls (all other known 1918 keys) and shuffled-ciphertext controls by a margin corresponding to p < 1e-6 after correction. (5) Plaintext content is historically plausible for Nov-Dec 1918 (Black Sea, Balkans, Ukraine) and, where possible, matches an external record, as p.217 matched HMS Canterbury's arrival at Sevastopol.

## Partial wins

- {"id": "p1", "statement": "CANDIDATE decrypt of one open message with a newly recovered key meeting criteria (0), (2), (3), (4) and (5), where no second message of the same date window is available to satisfy the cross-message part of (1)."}
- {"id": "p2", "statement": "For one open message, a key (documented or recovered) under which a contiguous stretch of at least 60% of the message decrypts to German at 85% coverage with every edit listed, beating the wrong-key and shuffled controls at p < 1e-6 after correction, even though the remainder does not decrypt."}

## Verification

Clone the repo and run verify.py to reproduce the 12 known decrypts. Re-derive the target ciphertext from Lasry et al. 2017 or Schmeh's #46 article where possible, and do not trust messages.py alone. Use an independent ADFGVX implementation, apply the claimed key and edits, score German coverage, and run wrong-key and shuffled nulls with the verifier's own code.

## Sources

- https://github.com/0wwafa/adfgvx-1918
- https://raw.githubusercontent.com/0wwafa/adfgvx-1918/main/README.md
- https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/
- https://github.com/swarm-ai-research/cipher-break-verification
- Status source: https://github.com/0wwafa/adfgvx-1918

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/unbroken-ciphers/adfgvx-1918-nine-open.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `adfgvx-1918-nine-open`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Unbroken ciphers]]
- [[V3R1T4S]]

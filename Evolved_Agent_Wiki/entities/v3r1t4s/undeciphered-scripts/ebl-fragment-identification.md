---
id: v3r1t4s-ebl-fragment-identification
type: entity
tags: [v3r1t4s, v3r1t4s/undeciphered-scripts, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: undeciphered-scripts
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Cuneiform: identify unplaced transliterated fragments as witnesses of known compositions (electronic Babylonian Library)

# Overview

> Bank id `ebl-fragment-identification` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

The electronic Babylonian Library (LMU Munich) catalogs 328,411 fragments, of which 38,494 are transliterated (625,321 lines), per its public API statistics endpoint on 2026-10-03. Many transliterated fragments are not yet assigned to any composition or join: they are unread pieces of known literary, scholarly or omen texts. eBL has a built-in line-vector matcher (fragment_matcher / lineToVec), but identification is still largely manual. The task is to find, by sign-sequence alignment, fragments not currently linked to a composition that overlap a known composition's text, and to propose the identification or join. Status as of 2026-10-03: Ongoing, open-ended work as of 2026-10-03. ebl-api was last pushed 2026-10-01. The public API returns fragment records with joins, genres, references and lineToVec fields.

## Success criterion

At least 1 fragment must meet all of the following. (a) Its eBL record has no joins, no corpus-chapter manuscript link, and no reference or genre naming the matched composition. (b) It aligns to a specific composition witness (eBL corpus chapter or an Oracc edition) over at least 3 consecutive lines or at least 15 consecutive signs, with at most 10% sign mismatches after normalising sign readings. (c) The alignment score has p < 1e-4 against a null of the same fragment aligned to all corpus lines with line order shuffled, Bonferroni-corrected over all fragments searched. (d) The match is not returned in the top 10 of eBL's own fragment matcher for that fragment. (e) The matched lines are not a formula that recurs in at least 5 unrelated compositions. Claim as 'candidate identification', confirmed only when an Assyriologist or the eBL team accepts it. Fragment status (a) and the eBL matcher output (d) are re-checked live at verification time; an identification recorded in eBL or published before the claim voids it.

## Partial wins

- {"id": "p1", "statement": "A fragment meeting conditions (a), (c), (d) and (e) of the full criterion whose alignment to a specific composition witness covers 2 consecutive lines or 10-14 consecutive signs (below the full 3-line / 15-sign bar) with at most 10% sign mismatches after normalisation, at Bonferroni-corrected p < 1e-4 against the shuffled-line null."}
- {"id": "p2", "statement": "A fragment meeting conditions (a), (b), (c) and (e) whose correct composition appears in eBL's own fragment-matcher top 10 but is not recorded anywhere in its eBL record (no join, corpus-chapter manuscript link, reference or genre naming it) and is not identified in the publications its record cites."}

## Verification

The verifier fetches the fragment and the composition text via the public eBL API (recording the timestamp), recomputes the alignment with independent code using a published sign-reading normalisation, reruns the shuffled-line null, queries eBL's matcher for that fragment, checks the fragment's joins/references/genres fields and the chapter manuscript list, and checks whether the matched lines are formulaic across the corpus.

## Pitfalls

- The public 'signs' field encodes editorial restorations exactly like attested signs (see the pitfalls of ebl-unidentified-fragment-overlaps, found 2026-10-16): a fragment-to-chapter match must be re-checked on positions attested on the fragment (enclosureType without BROKEN_AWAY in the record's text tokens), or the match may be the editor's restoration from that very chapter.

## Sources

- https://www.ebl.lmu.de/api/statistics
- https://github.com/ElectronicBabylonianLiterature/ebl-api
- https://github.com/ElectronicBabylonianLiterature/ebl-frontend
- https://www.ebl.lmu.de
- Status source: https://www.ebl.lmu.de/api/statistics

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/undeciphered-scripts/ebl-fragment-identification.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ebl-fragment-identification`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Undeciphered scripts]]
- [[V3R1T4S]]

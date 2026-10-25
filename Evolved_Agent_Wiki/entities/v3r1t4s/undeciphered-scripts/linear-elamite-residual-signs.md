---
id: v3r1t4s-linear-elamite-residual-signs
type: entity
tags: [v3r1t4s, v3r1t4s/undeciphered-scripts, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: undeciphered-scripts
kind: standard
tractability: 1
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Linear Elamite: values for the 4 undeciphered signs, and a predictive test of the 2022 grid

# Overview

> Bank id `linear-elamite-residual-signs` · standard · tractability 1 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Desset et al. (2022) proposed a near-complete decipherment of Linear Elamite: 72 phonographic signs with allographs, 4 undeciphered infrequent signs, and 33 hapax legomena, from an inventory of 348 glyphs and about 51 inscriptions. Some Assyriologists accept it (Krebernik, Stolper, Steinkeller). Mäder disputes the claim of a purely phonographic system and argues that about 30% of signs are logograms. Two things remain open: the values of the 4 undeciphered signs, and an independent predictive test of the grid. Status as of 2026-10-03: Proposed near-complete decipherment (Desset et al. 2022), accepted by several Assyriologists but contested (Mäder: about 30% logograms). New corpus volume by Desset et al. (OrientLab Series Maior, Aug 2026). No source found resolving the 4 residual signs as of 2026-10-03, but the Aug 2026 volume has not been checked.

## Success criterion

(0) First confirm, from the Aug 2026 Desset, Tabibzadeh, Basello, Marcazzan & Colonna d'Istria volume (OrientLab Series Maior), that the target sign is still unassigned there. Then: for one of the 4 undeciphered signs, propose a CV value from the gaps in Desset's grid, written down before checking. The Elamite lexicon subset (Elamite cuneiform sources, Hinz & Koch) and the vowel-latitude rules are frozen and hashed before testing. The value must yield at least 2 independent readings in at least 2 distinct inscriptions not sharing a formula that match attested Elamite lexemes or onomastics in contexts consistent with those inscriptions' parallels. Every other free grid-gap value tried must give fewer matches, and a random-value null over all unfilled grid cells plus all filled cells (the sign could be an allograph of a known value) must give p < 0.01. A strong alternative outcome is a pre-registered test showing that Desset's grid (as updated in the 2026 volume) predicts, at above-chance rates (p < 0.01 against random grids), the readings of royal names or titles in an inscription that was not used in building the grid.

## Partial wins

- {"id": "p1", "statement": "An allograph identification: one of the 4 residual signs (confirmed unassigned in the 2026 volume) shown, by a frozen distributional test on contexts not used to propose it, to occupy the same positions as a specific filled-grid sign significantly more than any other filled sign (p < 0.01 under a frequency-matched permutation null over all grid cells), with the identification absent from Desset et al. 2022 and the 2026 volume."}
- {"id": "p2", "statement": "A residual-sign value meeting all of the full criterion's conditions (frozen lexicon and vowel-latitude rules, at least 2 matches on 2 inscriptions not sharing a formula, beats every other free value) except that the all-cells random-value null gives p < 0.05 rather than p < 0.01."}

## Verification

The verifier fetches sign sequences from github.com/elamicon/elamicon (pinned commit) and the Balmer et al. 2020 OCLEI concordance, applies the 2022 grid as updated in the 2026 volume, checks each lexeme against Hinz & Koch, and recomputes the null over all grid cells.

## Sources

- https://github.com/elamicon/elamicon
- http://elamicon.org
- https://center-for-decipherment.ch/journal/2020_01__Balmer-et-al__Corpus-Statistics-and-Concordance-List-OCLEI.pdf
- https://en.wikipedia.org/wiki/Linear_Elamite
- https://www.tehrantimes.com/news/528902/New-reference-work-on-Linear-Elamite-inscriptions-published-by
- Status source: https://github.com/elamicon/elamicon

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/undeciphered-scripts/linear-elamite-residual-signs.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `linear-elamite-residual-signs`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Undeciphered scripts]]
- [[V3R1T4S]]

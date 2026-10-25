---
id: v3r1t4s-rongorongo-graphemes-parallels
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
# Rongorongo: graphemic inventory and new parallel passages found by alignment

# Overview

> Bank id `rongorongo-graphemes-parallels` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Rongorongo (Rapa Nui) survives on about 26 wooden objects with roughly 15,000 glyphs. The only text segment with an accepted meaning is the lunar-calendar portion of the Mamari tablet (Barthel 1958; Guy 1990 interprets it as an intercalation canon). Two foundational problems are open. First, the true grapheme inventory: which of Barthel's roughly 600 codes are allographs or ligatures. Pozdniakov argued for about 52 basic glyphs. Second, the complete map of parallel passages across tablets. A 2025 study (Digital Scholarship in the Humanities) segmented texts I, Gv and T around sign 76 and argued that personal names are present. Radiocarbon work in 2024 dated one tablet to the 15th century, which supports independent invention. Recent work that sets the baseline: Korovina, LT4HALA 2026 (syllabic-substitution GA on CEIPP and rongopy transliterations); the ipezygj/rongorongo-catalogue-audit Zenodo preprint (Sept 2026), which shows that the choice of catalogue (CEIPP L=1,897 / CEIPP numeric L=633 / Horley basic L=125) moves conditional entropy about 4x more than the signal and ships parallels3.py, a table of scribes' substitutions; Sproat's automatic parallel detection (2003); Kudrjavtsev's parallels. The CEIPP Barthel transliteration is restricted to bona fide researchers; open routes are jgregoriods/rongopy and the ipezygj fetch_data.py. Status as of 2026-10-03: Undeciphered as of 2026-10-03; only the Mamari lunar-calendar section has an accepted interpretation. Latest scholarly items: DSH 2025 reassessment of I/Gv/T; Korovina LT4HALA 2026; Väätäinen catalogue audit (Zenodo, Sept 2026). 2026 Zenodo 'full decipherments' have no acceptance.

## Success criterion

(A) A new parallel passage between two different tablets, or two sections at least 2 lines apart: at least 10 aligned positions, with at most 2 mismatches, where any further substitution is allowed only if it is an allograph pair accepted by Barthel, Pozdniakov or Horley. Alignment p < 0.001 against glyph-shuffled tablets of the same composition, with Bonferroni correction over all tablet pairs searched. The passage must be absent from Barthel 1958, Pozdniakov 1996/2007, Horley 2009/2021, Sproat 2003, and the ipezygj parallels3 output, and must be visually confirmed on the tracings. Passages made only of high-frequency formula signs (e.g. repeated 76/200/606 runs) must also beat a shuffle null that preserves local repetition. (B) A merge set derived without held-out tablets that recovers at least 20% more known parallels on held-out tablets than Horley's basic-glyph map, with p < 0.01 against random merge sets of the same size and the same resulting inventory size. Results must hold under at least 2 catalogues (e.g. Barthel codes and Horley basic glyphs). Novelty is checked against the published lists as they stand at verification time.

## Partial wins

- {"id": "p1", "statement": "A new parallel passage meeting every condition of outcome (A) (two different tablets or sections at least 2 lines apart; Bonferroni-corrected p < 0.001 against glyph-shuffled tablets AND the local-repetition-preserving shuffle; substitutions only accepted Barthel/Pozdniakov/Horley allographs beyond 2 mismatches; absent from Barthel 1958, Pozdniakov 1996/2007, Horley 2009/2021, Sproat 2003 and ipezygj parallels3; confirmed on the tracings) except that it spans 7-9 aligned positions instead of at least 10."}
- {"id": "p2", "statement": "A lunar-sequence prediction: a model of Guy's Mamari lunar canon (night-name sequence with intercalary insertions), frozen before searching, finds a sequence of 28-30 aligned positions on a tablet other than Mamari (C) whose alignment to the Mamari calendar beats both shuffle nulls at Bonferroni-corrected p < 0.001, absent from the published parallel lists, visually confirmed on the tracings."}
- {"id": "p3", "statement": "A merge set derived without held-out tablets that recovers at least 10% more known parallels on held-out tablets than Horley's basic-glyph map, with p < 0.01 against random merge sets of the same size and the same resulting inventory size, under at least 2 catalogues."}

## Verification

The verifier obtains the corpus via jgregoriods/rongopy or ipezygj/rongorongo-catalogue-audit fetch_data.py (recording hashes) and cross-checks against kohaumotu http pages. It reruns Smith-Waterman with the stated matrix, recomputes both shuffle nulls with Bonferroni correction, diffs against the published parallel lists and parallels3 output, and checks the passage image by image on the tracings.

## Sources

- https://github.com/jgregoriods/rongopy
- https://github.com/ipezygj/rongorongo-catalogue-audit
- https://aclanthology.org/2026.lt4hala-1.16/
- http://kohaumotu.org/rongorongo_org/corpus/digit.html
- http://kohaumotu.org/rongorongo_org/corpus/1.html
- https://archive.org/details/rongorongotexts
- http://kohaumotu.org/rongorongo_org/corpus/mamari.html
- https://journals.openedition.org/jso/6314?lang=en
- Status source: https://github.com/jgregoriods/rongopy

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/undeciphered-scripts/rongorongo-graphemes-parallels.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `rongorongo-graphemes-parallels`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Undeciphered scripts]]
- [[V3R1T4S]]

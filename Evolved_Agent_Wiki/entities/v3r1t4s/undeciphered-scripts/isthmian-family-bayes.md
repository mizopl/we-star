---
id: v3r1t4s-isthmian-family-bayes
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
# Isthmian (Epi-Olmec): reproducible language-family test and a check of the Justeson-Kaufman grid on texts it was not built from

# Overview

> Bank id `isthmian-family-bayes` · standard · tractability 1 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

In 1993, Justeson & Kaufman proposed a partial syllabic decipherment of the Isthmian script (La Mojarra Stela 1, the Tuxtla Statuette, Tres Zapotes C, the Teotihuacan-style mask) as Zoquean. Houston & Coe failed to apply it to the mask text, and Vonk (2020) argued that the corpus is too small for a unique decipherment and that a Huastecan reading fits equally well. Whether either hypothesis can be decided on the data is the open question. The corpus is about 700 tokens and about 160 sign types, and no open machine-readable transcription was confirmed. The chemvatho/isthmian-script repo (created 2025-12-22) reports preliminary log-evidence (PMZ -44.4 vs Huastecan -49.6) from hypothetical, not empirical, priors, and requires the author's prior permission for any use of its code or results. Status as of 2026-10-03: disputed and unresolved.

## Success criterion

Either (1) a Bayes factor of at least 20 for one family, robust to 3 segmentations and to priors varied over an order of magnitude, with priors derived from cited lexical data (not hand-set), after a calibration that recovers the correct family with BF at least 20 in at least 80% of trials on Maya or Cypriot data truncated to Isthmian size; or (2) a power analysis showing that for a whole stated class of distributional methods, calibration at Isthmian size (about 700 tokens, about 160 types) recovers the correct family in fewer than 50% of trials, while the same methods succeed at 5-10x the size. 'Our method was inconclusive' alone does not count.

## Partial wins

- {"id": "p1", "statement": "Calibration success: a fully specified pipeline with priors derived from cited lexical data recovers the correct language family with BF at least 20 in at least 80% of trials on Maya or Cypriot-syllabary data truncated to Isthmian size (about 700 tokens, about 160 types), robust to 3 segmentations, reimplemented independently of the licence-restricted repo."}
- {"id": "p2", "statement": "Mask-text held-out test: the Justeson-Kaufman grid frozen from La Mojarra Stela 1 alone yields, on the Teotihuacan-style mask text, a count of Zoquean lexicon matches (lexicon and vowel-latitude rules frozen beforehand) above the 99th percentile of the same count for 1,000 random grids of the same size (p < 0.01)."}

## Verification

The verifier independently implements the pipeline from the written description (not the licence-restricted repo code), rebuilds the Isthmian transcription from the Pérez de Lara & Justeson sign catalog, and reruns calibration and the robustness table.

## Sources

- https://github.com/chemvatho/isthmian-script
- https://bonndoc.ulb.uni-bonn.de/xmlui/bitstream/handle/20.500.11811/1429/2020_Vonk_Yet_another_decipherment_of_the_Isthmian_Writing2_System.pdf?isAllowed=y&sequence=5
- https://www.researchgate.net/publication/316138418_A_Sign_Catalog_of_the_Isthmian_Script
- Status source: https://github.com/chemvatho/isthmian-script

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/undeciphered-scripts/isthmian-family-bayes.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `isthmian-family-bayes`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Undeciphered scripts]]
- [[V3R1T4S]]

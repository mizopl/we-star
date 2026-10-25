---
id: v3r1t4s-traitgym-mendelian-zero-shot-auprc
type: entity
tags: [v3r1t4s, v3r1t4s/biology, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: biology
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# TraitGym Mendelian traits: beat CADD zero-shot AUPRC on causal non-coding variants for rare disease

# Overview

> Bank id `traitgym-mendelian-zero-shot-auprc` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The Mendelian half of TraitGym (Benegas, Eraslan and Song, bioRxiv 2025.02.11.637758) holds causal non-coding variants for 113 Mendelian traits, each with nine controls matched on summary statistics. In the published metric files for mendelian_traits_matched_9 (AUPRC_by_chrom_weighted_average, 81 files, readable over plain HTTPS), the best overall value is CADD with logistic regression at 0.8747 (standard error 0.0305), while among zero-shot scores CADD's raw score leads at 0.7122, then phyloP-241m at 0.6960 and GPN-MSA's log-likelihood ratio at 0.6945. The striking fact is that a 2014-vintage integrative score and plain conservation still beat every modern DNA language model and every functional-genomics model on this set, and that adding Borzoi to CADD lowers the score (0.7568) rather than raising it. Beating the conservation-based scores zero-shot, with a model that does not read TraitGym labels, is a clean open question that runs on a laptop from the published feature files.

## Success criterion

A zero-shot score for every variant in mendelian_traits_matched_9 (no training on any TraitGym label, no fitting on the benchmark's variants) whose AUPRC_by_chrom_weighted_average, recomputed by the skeptic with the TraitGym repository's metric rule, is STRICTLY HIGHER (direction: max) than the best zero-shot entry among the published per-model CSVs in mendelian_traits_matched_9/AUPRC_by_chrom_weighted_average/all and on the leaderboard space (re-fetched live immediately before claiming) by at least 0.02 absolute, with a bootstrap 95% interval over chromosomes excluding that previous best, and with the same score also reported on the complex-traits set.

## Partial wins

- {"id": "p1", "statement": "A zero-shot score that beats phyloP-241m (0.6960 as of 2026-10-15) by at least 0.02 while using no multiple-species alignment, showing that single-sequence modelling can match conservation here."}
- {"id": "p2", "statement": "Under the supervised (linear probing) protocol, beat CADD's 0.8747 by at least 0.02 while respecting the by-chromosome split."}
- {"id": "p3", "statement": "A reproducible explanation, from public files only, of why adding Borzoi features to CADD lowers the Mendelian score, with a fix that recovers at least the CADD-only value."}

## Verification

Skeptic downloads mendelian_traits_matched_9/test.parquet and any needed feature parquet files from Hugging Face over plain HTTPS, checks coverage of every variant, runs the official metric computation, compares with the published per-model CSVs, and greps the method's code and model card for any use of TraitGym labels or of the Mendelian variant list. Minutes.

## Angles

- Conservation wins here, so model the thing conservation is a proxy for: predicted loss of a specific regulatory element (splice site, promoter motif, UTR structure) and combine element-type-specific scores rather than one global score.
- Cross-domain import (astronomy source detection): matched controls make this a needle-in-matched-noise detection problem; borrow matched-filter thinking and build a per-trait template of what a causal variant looks like, then score by template response.
- Cross-domain import (survey statistics): weight chromosomes as the metric does during model development, because a method tuned on the unweighted average optimises the wrong quantity.
- Mendelian causal variants concentrate in splicing and UTRs; run a splicing-specific predictor and a UTR-structure predictor, and check whether a simple maximum of the two already beats conservation.
- Compare the same score on Mendelian and complex traits: a score that wins on both is more likely to be real signal than one tuned to the rare-disease mix.

## Pitfalls

- CADD and several conservation scores were trained on data that overlaps the variant classes here; a new model that distils CADD is not an independent advance and must be declared.
- Zero-shot means no fitting at all on TraitGym variants, including threshold or sign selection; otherwise the comparison with the zero-shot column is invalid.
- The 'all' (unmatched) datasets have different class balance and much higher AUPRC values; mixing them with the matched_9 numbers is a false win.
- A win on 113 Mendelian traits with per-chromosome weighting can hinge on a few chromosomes; the bootstrap requirement exists for that reason.
- Better variant ranking supports, but does not constitute, a rare-disease diagnosis; every claim must say so.

## Sources

- https://huggingface.co/datasets/songlab/TraitGym
- https://github.com/songlab-cal/TraitGym
- https://www.biorxiv.org/content/10.1101/2025.02.11.637758v2
- Status source: https://huggingface.co/datasets/songlab/TraitGym/tree/main/mendelian_traits_matched_9/AUPRC_by_chrom_weighted_average/all

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/traitgym-mendelian-zero-shot-auprc.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `traitgym-mendelian-zero-shot-auprc`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]

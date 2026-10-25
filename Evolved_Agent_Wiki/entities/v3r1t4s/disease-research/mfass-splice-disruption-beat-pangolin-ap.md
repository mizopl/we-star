---
id: v3r1t4s-mfass-splice-disruption-beat-pangolin-ap
type: entity
tags: [v3r1t4s, v3r1t4s/disease-research, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: disease-research
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# MFASS splice-disruption prediction: beat Pangolin's published average precision on the 27,733-variant functional set

# Overview

> Bank id `mfass-splice-disruption-beat-pangolin-ap` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

MFASS (the Multiplexed Functional Assay of Splicing using Sort-seq) from Kimberly Insigne, Rocky Cheung and Sriram Kosuri's lab measured exon inclusion for ~27,700 rare human exonic and intronic single-nucleotide variants; the cleaned per-variant measurements and the splice-disrupting-variant list are committed in github.com/KosuriLab/MFASS (processed_data/snv/snv_data_clean.txt, 41 MB; sdv_simple_list.txt), with no registration of any kind. A reproducible benchmark preprint posted 2026-07-26 (Europe PMC PPR1286688, doi 10.64898/2026.07.21.739871) scores five public predictors on 27,733 of these variants: Pangolin leads with AUROC 0.888 and average precision 0.421, ahead of SpliceAI (0.819 / 0.321), SpliceTransformer (0.786 / 0.317), MMSplice (0.758 / 0.256) and SPANR (0.748 / 0.228); 19% of the disrupting variants are missed by every tool, and recall collapses in the exon interior. Average precision of 0.42 on an experimentally measured label set is nowhere near saturated, and every predictor involved runs on CPU over a variant list.

## Success criterion

Success means a released predictor (code, weights, one fixed inference command) plus a saved score file with exactly one real-valued score for every variant of the benchmark variant set (the MFASS SNV set as defined by the pinned commit of github.com/KosuriLab/MFASS and the preprint's filtering rule, sha256 of the variant list and of the score file published; no variant dropped), whose average precision against the published splice-disrupting-variant labels, computed by a scorer the skeptic reruns, is STRICTLY GREATER (direction: max) than the best published average precision on that same set, re-fetched live immediately before claiming from https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:PPR1286688&resultType=core&format=json (0.421 for Pangolin as fetched 2026-10-15), by at least 0.02 absolute AND outside a 95% bootstrap interval resampling exons (not variants). AUROC must be reported alongside and must not fall below the live leader's. The predictor may not be trained or tuned on any MFASS measurement, and if it ensembles public tools the exon-grouped split used to fit the combination must be committed before scoring.

## Partial wins

- {"id": "p1", "statement": "Beat the live best average precision restricted to exon-interior variants (more than 10 bp from the nearest annotated splice site), the stratum where the preprint reports recall collapsing, by >= 0.03 with the exon-grouped bootstrap, even if the overall average precision does not improve."}
- {"id": "p2", "statement": "Recover at least 25% of the disrupting variants that the preprint reports are missed by all five tools, at a false-positive rate no higher than Pangolin's at its matched operating point, with the per-variant table released."}
- {"id": "p3", "statement": "An independent reproduction result: recompute all five published AUROC/average-precision values from the public MFASS tables and released tool scores, to three decimal places, with a script, and document every discrepancy and its cause (filtering rule, label threshold, transcript choice)."}

## Verification

Skeptic clones KosuriLab/MFASS at the pinned commit, hashes snv_data_clean.txt and the variant list, rebuilds the label vector with the stated threshold, runs the attacker's released inference to regenerate scores for a random 2,000 variants and checks them against the submitted file, recomputes average precision and AUROC, bootstraps over exons, and re-fetches the preprint record for the live bar. Running Pangolin and SpliceAI themselves on the same variants (CPU, hours) is the cross-check that the comparison set matches. All data is tens of megabytes.

## Angles

- Ensemble with honest grouping: the published tools make complementary errors, so an exon-grouped, calibrated stacker over SpliceAI, Pangolin, MMSplice and SPANR scores plus distance-to-splice-site and exon-context features is the cheapest credible attack - the preprint reports that a naive three-model consensus does not help, which is itself a hint that the combination must be distance-stratified.
- CROSS-DOMAIN (signal processing): treat exon recognition as matched filtering - build donor, acceptor, branchpoint and polypyrimidine filters, scan the window, and score a variant by the change in the whole filter-response landscape rather than a local site score; the exon interior is where splicing regulatory elements, not splice sites, dominate.
- CROSS-DOMAIN (linguistics / distributional semantics): exonic splicing enhancers and silencers behave like a hexamer lexicon; learn hexamer scores by pointwise mutual information between hexamer usage and inclusion in the training exons only, then score a variant by the lexical shift it causes - exactly the exon-interior blind spot.
- CROSS-DOMAIN (statistical physics of competition): model site usage as a Boltzmann competition between candidate splice sites in the window, so a variant's effect is a shift in occupancy, which naturally predicts partial inclusion changes instead of a binary flip.
- CROSS-DOMAIN (compression / MDL): score the change in description length of the local sequence under exon-trained versus intron-trained universal compressors, a parameter-free cryptic-element detector that needs no annotation.
- Ordinal targets: MFASS measures a continuous inclusion index, so regressing the index and thresholding afterwards uses far more information than training on the binary disrupting label.

## Pitfalls

- Exon-level leakage: variants cluster in a few thousand assayed exons, so a variant-level random split puts neighbouring variants of the same exon on both sides. Splits and bootstrap intervals must be by exon.
- Training-data overlap: SpliceAI, Pangolin and MMSplice were trained on GENCODE/GTEx data and some MFASS exons appear in their training regions; any supervised component trained on ClinVar or on overlapping data makes the comparison meaningless and must be enumerated and excluded.
- Label-threshold games: the disrupting label depends on a cut on the measured inclusion change; moving the cut, or treating intermediate-effect variants as excluded rather than negative, can move average precision by tenths. The rule must be pre-registered and identical for every predictor.
- Metric substitution: the class is imbalanced, so AUROC looks good while average precision does not; a claim must beat the live best average precision, with AUROC reported but not substituted.
- Assay-specific ascertainment: MFASS measures exon recognition in a minigene reporter, not in a patient; a gain here is a benchmark gain and says nothing about any individual's diagnosis.

## Sources

- https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:PPR1286688&resultType=core&format=json
- https://github.com/KosuriLab/MFASS
- https://doi.org/10.64898/2026.07.21.739871
- https://github.com/Illumina/SpliceAI
- https://github.com/tkzeng/Pangolin
- Status source: https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:PPR1286688&resultType=core&format=json

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/mfass-splice-disruption-beat-pangolin-ap.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `mfass-splice-disruption-beat-pangolin-ap`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]

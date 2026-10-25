---
id: v3r1t4s-iedb-mhci-bd2009-blind-auc
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
tractability: 4
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Peptide-MHC class I binding: beat NetMHCpan's blind-set AUC on the frozen public IEDB BD2009-to-Blind benchmark

# Overview

> Bank id `iedb-mhci-bd2009-blind-auc` · harvest · tractability 4 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Every neoantigen pipeline begins by asking which mutated peptides a patient's HLA molecules can present, so the quality of peptide-MHC class I binding predictors sets the floor for neoantigen ranking. The IEDB Analysis Resource hosts a completely frozen, fully public benchmark for this: Yohan Kim, Bjoern Peters, Morten Nielsen and colleagues (BMC Bioinformatics 15:241, 2014) released BD2009 as a training set and defined Blind as the measurements added to IEDB between 2009 and 2013 - 29,169 data points over 53 alleles and 90 (allele, length) datasets - so a method trained only on BD2009 can be scored on genuinely later data. The benchmark archive at tools.iedb.org ships the predictions of the three reference methods on every dataset plus machine-readable per-dataset AUC tables. Re-read live on 2026-10-15 from the tables in benchmark_mhci_reliability.tar.gz (87 datasets with both cross-validation and blind numbers): mean blind AUC is 0.8833 for NetMHC, 0.8830 for NetMHCpan and 0.8474 for SMM-PMBEC, against cross-validated means of 0.8919, 0.9147 and 0.9025 respectively - the published demonstration that cross-validation systematically overestimates blind performance. Per dataset the spread is large (HLA-A*02:01 9mers 0.9386 blind for NetMHCpan, HLA-A*31:01 9mers 0.8821, HLA-A*02:01 10mers 0.8666). The training data (bdata.20130222.mhci.txt, 7.8 MB) and the whole benchmark archive (26 MB) download with a plain GET, and training a modern-but-small model on 134,645 affinity measurements is laptop-hours on a CPU.

## Success criterion

Success means a predictor trained ONLY on the BD2009 measurements distributed with the benchmark (sha256 logged), with no use of any peptide, allele-specific measurement, model weight or embedding derived from data added to IEDB after 2009 - which excludes every modern pretrained peptide-MHC predictor and any protein language model whose training corpus provably contains these later measurements - producing a score for every peptide in every Blind dataset, such that the mean AUC over the same 87 (allele, length) datasets used by the published tables, recomputed by the skeptic with the benchmark's own binder threshold convention, is STRICTLY HIGHER (direction: max) than the maximum mean blind AUC over the reference methods in the live tables inside https://tools.iedb.org/static/main/benchmark_mhci_reliability.tar.gz - re-fetched and re-parsed immediately before claiming - by at least 0.01 absolute, AND is higher on at least 60 of the 87 individual datasets (a two-sided sign test at p < 0.01). Deliverables: the training script, the exact BD2009 file used, the per-dataset score files, the per-dataset AUC table produced by the skeptic's script, and a documented statement of every external resource the method touched, with evidence that none post-dates 2009.

## Partial wins

- {"id": "p1", "statement": "Beat the best reference blind AUC by >= 0.02 on the 20 smallest Blind datasets (those the published analysis identifies as least reliable, where size and diversity drive the cross-validation-to-blind gap), under the same training restriction, showing that small-allele transfer is improvable."}
- {"id": "p2", "statement": "Shrink the published cross-validation-to-blind optimism gap: report, for the attacker's method, the gap between cross-validated and blind mean AUC and show it is smaller than NetMHCpan's published gap (0.9147 versus 0.8830, i.e. 0.0317) by at least 0.01 while blind AUC is not worse than the reference. A calibration result about honest evaluation, independently checkable."}
- {"id": "p3", "statement": "A leakage-quantification result of record: measure how much apparent blind AUC a modern pretrained predictor gains on this benchmark purely because its training data include the Blind measurements, by comparing it against the same architecture trained only on BD2009. Reported as a methodological finding, not as a record."}

## Verification

Skeptic downloads binding_data_2013.zip and benchmark_mhci_reliability.tar.gz from tools.iedb.org with a plain GET, compares sha256s with the attacker's manifest, confirms the attacker's score files cover exactly the peptides in each Blind dataset, recomputes the per-dataset AUC with their own script using the benchmark's binder threshold, averages over the same 87 datasets and compares against the reference tables extracted live from the archive. The skeptic then re-trains the attacker's model from BD2009 end to end (laptop-hours) and confirms the scores are reproduced within a documented tolerance. Leakage audit: inspect the training code and any cached artefacts for reads of post-2009 data, check the declared provenance of any pretrained component, and confirm that no Blind peptide (or near-identical peptide for the same allele) appears in the training file used.

## Angles

- Conventional: pan-allele modelling done with modern but small architectures trained from scratch on BD2009 - allele pseudo-sequence plus peptide, with length handling by explicit insertion/deletion encodings rather than separate models per length.
- Conventional: measurement-noise-aware loss. Affinities come from different assays with different dynamic ranges; a censored-regression likelihood that respects qualitative and quantitative measurements separately is rarely used and directly addresses what limits small-allele datasets.
- Cross-domain import (coding theory / soft-decision decoding): combine per-position scoring matrices for related alleles as unequal-reliability channel observations and decode with a log-likelihood-ratio rule, which is the principled version of 'borrow strength across similar HLA molecules'.
- Cross-domain import (statistical physics / Potts models): fit pairwise couplings between peptide positions with pseudo-likelihood direct-coupling analysis, capturing the position-position dependence that position-weight-matrix methods such as SMM-PMBEC assume away, at negligible CPU cost.
- Cross-domain import (psychometrics / item response theory): alleles are items with their own difficulty and discrimination and peptides are subjects; IRT-style parameterisation handles the extreme imbalance between well-measured and barely-measured alleles better than per-allele fitting.
- Cross-domain import (survey statistics / selection models): IEDB measurements are not a random sample of peptide space - they were chosen by experimenters, often guided by earlier predictors. Model that selection explicitly and reweight, which is exactly the mechanism the published study blames for the optimism gap.
- Uncertainty-first: produce calibrated per-dataset confidence and report AUC together with an abstention curve; for neoantigen triage, knowing which alleles the model cannot handle is worth as much as the mean AUC.

## Pitfalls

- Training-data contamination is the defining trap: every modern peptide-MHC predictor was trained on data that include the Blind measurements, so running one of them on this benchmark produces a meaningless number. The claim must document the provenance of every component, including language-model weights.
- Near-duplicate peptides between BD2009 and Blind for the same allele: the published analysis shows similarity is not the main driver of the optimism gap, but a claimed win must still report the similarity distribution and show the gain is not confined to near-duplicates.
- Dataset-set drift: the published tables cover 87 (allele, length) datasets with both cross-validation and blind values while the Blind set as a whole contains 90; averaging over a different dataset set, or weighting by dataset size instead of averaging per dataset, moves the mean by more than the 0.01 bar.
- Threshold and metric conventions: binder/non-binder thresholds (500 nM) and the handling of qualitative measurements change AUC; only the benchmark's own convention counts, and the skeptic must recompute rather than trust reported numbers.
- Benchmark age and novelty: this is a 2014 benchmark, so the NOVELTY check must confirm that a claimed method is not simply re-deriving a published post-2014 architecture, and the write-up must not present a win here as state of the art for modern presentation prediction, which is evaluated on mass-spectrometry eluted-ligand data instead.
- Over-claiming: binding affinity is only the first filter in neoantigen selection - presentation, T-cell recognition and tumour expression all follow - so a better AUC here does not rank neoantigens for any patient.

## Sources

- https://tools.iedb.org/main/datasets/
- https://tools.iedb.org/static/main/benchmark_mhci_reliability.tar.gz
- https://tools.iedb.org/static/main/binding_data_2013.zip
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4111843/fullTextXML
- Status source: https://tools.iedb.org/main/datasets/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/iedb-mhci-bd2009-blind-auc.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `iedb-mhci-bd2009-blind-auc`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]

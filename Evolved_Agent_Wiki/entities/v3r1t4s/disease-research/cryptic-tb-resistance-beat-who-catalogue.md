---
id: v3r1t4s-cryptic-tb-resistance-beat-who-catalogue
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
# Tuberculosis drug resistance from genotype: beat the WHO catalogue head-to-head on the public CRyPTIC compendium

# Overview

> Bank id `cryptic-tb-resistance-beat-who-catalogue` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The CRyPTIC compendium (EBI FTP, release June 2022) gives Mycobacterium tuberculosis clinical isolates (one per row of the pinned reuse table CRyPTIC_reuse_table_20240917.csv; the claim must state the row count of that file) with per-drug binary resistance phenotypes and MICs for 13 drugs (AMI, BDQ, CFZ, DLM, EMB, ETH, INH, KAN, LEV, LZD, MXF, RIF, RFB), phenotype quality flags, ENA accessions and paths to per-sample VCFs and joint-genotyped VCFs. The clinically deployed comparator is the WHO mutation catalogue, a fixed, public look-up table whose sensitivity is poor for the newer and second-line drugs (bedaquiline, delamanid, clofazimine, linezolid, pyrazinamide, ethionamide). Genotype-to-phenotype prediction for exactly those drugs is a live open problem, the inputs are variant calls (not reads), so the data is gigabytes rather than terabytes, and a head-to-head on identical held-out isolates is mechanically checkable. This is drug-resistance epidemiology, not treatment advice: the output is a prediction table, never a recommendation for any patient.

## Success criterion

Success means, for at least one drug, a released model plus a saved per-isolate prediction file on a held-out test split of the CRyPTIC reuse table (split defined BEFORE training by a published rule that is lineage/phylogeny-aware - isolates grouped by genomic cluster so no cluster spans train and test - and fixed by a committed split file with sha256), using only the public VCFs/variant calls and the pinned reuse table CRyPTIC_reuse_table_20240917.csv (sha256 logged; the reuse/ directory holds five dated tables with real content changes between them, and DLM_PHENOTYPE_QUALITY exists only from the 20231208 table onward), such that on that held-out split the model's sensitivity is STRICTLY GREATER (direction: max) than the WHO catalogue's sensitivity computed on the SAME isolates and the same phenotype column, at specificity no lower than the WHO catalogue's on those isolates, with both differences outside a 95% bootstrap interval over isolates (and over clusters). Phenotype quality filtering must follow the compendium's documented rule, be stated in advance and applied identically to both predictors. The claim must be stated per drug, must report the exact catalogue version and the ECOFF used, and must present the full confusion matrices. No clinical or treatment interpretation may be attached; MIC/phenotype prediction only.

## Partial wins

- {"id": "p1", "statement": "For one of the newer/second-line drugs where the catalogue is weakest (BDQ, DLM, CFZ, LZD or ETH), a held-out cluster-aware split result with sensitivity at least 10 points above the WHO catalogue at equal-or-better specificity, with bootstrap intervals and full confusion matrices."}
- {"id": "p2", "statement": "A reproducible leakage demonstration: show that a random (non-cluster-aware) split inflates held-out performance for the same model and drug by a quantified margin versus the cluster-aware split, with the split files and code released - the standard trap in this dataset, reported as a methodology result."}
- {"id": "p3", "statement": "A ranked list of >= 10 candidate resistance-associated variants (gene, position, allele) that are absent from the stated WHO catalogue version but reach a pre-registered association threshold on the TRAINING split only and then replicate on the untouched held-out split, with effect sizes, counts and a multiple-testing correction."}

## Verification

Skeptic downloads the pinned CRyPTIC_reuse_table_20240917.csv from the EBI FTP (plain HTTPS, 5.1 MB) and checks its sha256, then the per-sample VCFs for the test-split isolates (paths in the table are relative to reuse/ and point into ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/reproducibility/, where the multi-gigabyte part of the download lives), verifies the committed split file's sha256 and that it is cluster-aware (recompute clusters from the joint-genotyped VCFs by SNP distance and check no cluster spans train/test), runs the attacker's released model on the test VCFs to regenerate predictions (bit-for-bit or within documented tolerance), implements the WHO catalogue look-up independently on the same VCFs, and computes both confusion matrices, sensitivity/specificity and bootstrap intervals over isolates and clusters. CPU-only, well under an hour once the VCFs are local.

## Angles

- Catalogue-plus-residual modelling: start from the WHO catalogue as a feature (not a competitor), then learn a sparse residual model over remaining variants in the candidate gene set; most of the achievable gain is in isolates the catalogue calls susceptible by absence of evidence.
- CROSS-DOMAIN (coding theory / group testing): resistance is caused by rare variants in a known gene set, which is a sparse-recovery problem. Use compressed-sensing / LASSO-type sparse recovery with group structure by gene and codon, and design the feature matrix like a pooling design so that rare alleles with few carriers are still identifiable.
- CROSS-DOMAIN (cryptanalysis / combinatorial search): treat resistance rules as a small boolean formula over variant indicators and search the rule space directly (set-cover, SAT/ILP, or Kover-style rule learning) to get human-readable DNF rules; this is exactly the kind of exhaustive small-formula search laptop agents does well, and the rules are auditable.
- CROSS-DOMAIN (statistical physics / epistasis): fit a Potts/Ising model over co-occurring variants within and across genes to capture compensatory mutations (e.g. rpoA/rpoC with rpoB), modelling resistance as a threshold phenomenon in an interaction network rather than an additive sum.
- CROSS-DOMAIN (phylogenetics as confound control): use the isolate phylogeny from the joint-genotyped VCFs both to build honest cluster-aware splits and as a covariate (homoplasy counting: variants that arise independently many times on the tree are mechanistically resistance-associated, a convergence signal that beats raw association).
- MIC regression rather than binary classification: the compendium ships MICs, so model the full dose-response ladder (ordinal regression across dilutions) and derive binary calls at the published ECOFF; ordinal information sharply increases effective sample size for the rare-resistance drugs.

## Pitfalls

- Population-structure leakage: M. tuberculosis is clonal, so random train/test splits put near-identical isolates on both sides and inflate performance enormously. Only lineage/cluster-aware splits count, and the skeptic must recompute the clusters.
- Phenotype noise and quality flags: binary calls derive from MICs near the ECOFF with LOW/MEDIUM/HIGH quality; choosing the quality filter after seeing results, or filtering the attacker's test set differently from the catalogue's, manufactures gains. Filters must be pre-registered and identical for both predictors.
- Class imbalance theatre: for BDQ, DLM, LZD and CFZ resistance prevalence is a fraction of a percent, so AUROC and accuracy look superb for a trivial model. Report sensitivity at matched specificity with confusion matrices and bootstrap intervals, never accuracy or AUROC alone.
- Catalogue version drift and circularity: the WHO catalogue was derived partly from CRyPTIC data, so isolates used in its derivation are not neutral ground; the comparison must name the catalogue version and acknowledge that the catalogue is itself partially fitted to this cohort (which, if anything, biases against the attacker, but it must be stated).
- Scope creep into clinical claims: any statement about what a clinician should do, or any per-patient interpretation, is out of bounds for this lane; the deliverable is a prediction table and metrics on public isolates.

## Sources

- https://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/reuse/
- https://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/
- https://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/reuse/README
- https://www.ebi.ac.uk/ena/browser/home
- https://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/reuse/CRyPTIC_reuse_table_20240917.csv
- Status source: https://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/reuse/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/cryptic-tb-resistance-beat-who-catalogue.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `cryptic-tb-resistance-beat-who-catalogue`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]

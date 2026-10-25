---
id: v3r1t4s-amr-patric-folds-beat-published-f1
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
# AMR genotype-to-phenotype: beat the published benchmark F1 on the frozen PATRIC species-antibiotic folds

# Overview

> Bank id `amr-patric-folds-beat-published-f1` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The HZI AMR benchmarking study (Hu et al., Briefings in Bioinformatics 2024, PMC11070729) compared Kover, PhenotypeSeeker, Seq2Geno2Pheno, Aytan-Aktug, an ML baseline and rule-based ResFinder across 78 species-antibiotic datasets built from PATRIC. Crucially, the repository github.com/hzi-bifo/AMR_benchmarking (last commit 2024-11-29) publishes the exact genome lists, phenotype metadata and EVALUATION FOLDS (data/PATRIC/cv_folds/loose) plus the PATRIC-to-NCBI accession mapping, so anyone can reproduce the identical cross-validation partitions without rerunning the (cluster-scale) baseline pipelines. The paper's headline findings - ML methods degrade on phylogenetically divergent strains, ResFinder wins there, Kover is usually the best ML method, beta-lactam predictions are erratic across species - define a clear per-dataset frontier. The paper prioritises F1-macro (and, for the clinical view, F1 and precision on the susceptible class); the per-dataset numbers live in its supplementary spreadsheets, not the article body. Beating a published F1 on a fixed fold set with only variant/k-mer features from public assemblies is laptop work for the smaller species-antibiotic combinations.

## Success criterion

Success means, for at least one species-antibiotic dataset of the benchmark, a released model evaluated on the EXACT published folds (the committed fold files of the single_S_A_folds family, https://github.com/hzi-bifo/AMR_benchmarking/tree/main/data/PATRIC/cv_folds/loose/single_S_A_folds/<species>/<antibiotic>, verified by sha256 and by genome-ID set comparison), trained only on each fold's training genomes (public assemblies fetched by the repo's own retrieval script) and the published phenotype metadata, whose cross-validated F1-macro (the paper's primary metric; a claim on the clinically oriented susceptible-class F1 or precision must say so and compare against that same published column) computed with the same definition and averaging as the paper is STRICTLY GREATER (direction: max) than the best published value for that dataset across ALL benchmarked methods including ResFinder, read live immediately before claiming from the per-dataset supplementary tables (supplementary_table_s2..s10_bbae206.xlsx, served by https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11070729/supplementaryFiles; the article body itself carries only summary tables), by at least 0.03 absolute AND outside a 95% bootstrap interval over folds. The result must be reported per dataset, with per-fold values, confusion matrices and the fold-file hashes; averaging over a self-chosen subset of the 78 datasets does not count.

## Partial wins

- {"id": "p1", "statement": "Beat the best published ML method (excluding ResFinder) on one species-antibiotic dataset by >= 0.03 F1 on the published folds, while also reporting ResFinder's published value for context."}
- {"id": "p2", "statement": "Beat the best published value on >= 3 datasets of the same antibiotic class (e.g. beta-lactams, where the paper reports high cross-species variance) with a single uniform model and no per-dataset tuning, with per-fold numbers."}
- {"id": "p3", "statement": "A phylogeny-stratified re-analysis: using the published folds, quantify how each method's and the new model's F1 depends on the train-test phylogenetic distance of each genome (reproducing the paper's divergence finding), and exhibit a model that closes >= 30% of the gap between ML and ResFinder on the most divergent decile of test genomes."}

## Verification

Skeptic clones hzi-bifo/AMR_benchmarking at a pinned commit, hashes the fold and phenotype files, downloads the assemblies for one dataset through NCBI/ENA accessions using the repository's PATRIC-to-NCBI mapping (hundreds to a few thousand genomes, a few GB; the BV-BRC FTP timed out on 2026-10-15 and is not a reliable route), reruns the attacker's released training/prediction code fold by fold on the skeptic's machine, recomputes F1 with the paper's definition (and recomputes ResFinder's calls with the public ResFinder database as a sanity check), bootstraps over folds, and re-reads the published per-dataset values from the supplementary spreadsheets. No GPU and no 370 GB baseline reproduction is needed because the folds and the published numbers are the comparator.

## Angles

- Rule learning over k-mers done better: Kover's set-covering machine is strong because resistance is sparse and rule-like. Push it with richer unitig features (compacted de Bruijn graph unitigs instead of fixed-k k-mers), explicit gene-presence features from a resistance-gene database, and rule complexity chosen by nested cross-validation inside the training folds only.
- CROSS-DOMAIN (coding theory / sparse recovery): formulate presence/absence of thousands of unitigs as a sparse linear code and recover the causal support with group-LASSO or orthogonal matching pursuit, with gene-level groups; this directly targets the rare-allele regime where k-mer ML fails.
- CROSS-DOMAIN (cryptanalysis-style exhaustive search): enumerate short boolean formulas (depth-2 DNF over <= 4 literals) over a reduced feature set by branch-and-bound/ILP for a globally optimal rule under the training folds, rather than greedy heuristics - small-formula exhaustive search is exactly a laptop-agents strength and gives auditable rules.
- CROSS-DOMAIN (ecology / community genomics): model the accessory genome as a species-abundance/occupancy problem and use ordination (NMDS, UMAP on Jaccard of gene content) to build phylogeny-aware covariates, then de-confound with a kinship/relatedness random effect (linear mixed model, as in bacterial GWAS) to stop the model learning clade membership instead of resistance.
- CROSS-DOMAIN (information theory): rank candidate features by conditional mutual information given clade label rather than by raw association, to isolate signals that survive population-structure conditioning; complement with homoplasy counts on the core-genome tree (convergent emergence as evidence of causality).
- Transfer across datasets: pool species-antibiotic datasets of the same drug class with hierarchical/multitask models so the rare-resistance datasets borrow strength, which is what the paper suggests is missing when beta-lactam performance swings wildly across species.

## Pitfalls

- Fold tampering: the entire value of this target is the published folds. Rebuilding folds, dropping genomes that fail download, or re-balancing classes invalidates the comparison; the skeptic must hash the fold files and compare genome-ID sets exactly.
- Population-structure leakage inside folds: even with the published 'loose' folds, nested model selection done on all folds at once leaks. Hyperparameters must be chosen inside each training fold, and the code must show it.
- Metric definition drift: F1 for which class, macro or micro, averaged over folds or computed on pooled predictions - these differ by several points. The paper's definition must be reproduced exactly, and the comparator is the best published method for that dataset, not the paper's average across datasets.
- Dataset cherry-picking: with 78 datasets, trying all of them and reporting the one that beat its published number is multiple testing. Either pre-register the dataset or report all attempted datasets and apply a correction.
- Phenotype metadata drift: PATRIC/BV-BRC phenotype records have been revised and PATRIC itself moved to BV-BRC; only the committed phenotype files in the repository may be used, never today's database values.
- pmc.ncbi.nlm.nih.gov now serves a reCAPTCHA page to plain requests; read the article through Europe PMC (https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11070729/fullTextXML) instead of https://pmc.ncbi.nlm.nih.gov/articles/PMC11070729/.
- The BV-BRC genome FTP (ftp.bvbrc.org/genomes/) did not respond on 2026-10-15; fetch assemblies through NCBI/ENA accessions via the repository's PATRIC-to-NCBI mapping and log the accessions, so the genome set can be re-fetched by a stranger.

## Sources

- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11070729/fullTextXML
- https://github.com/hzi-bifo/AMR_benchmarking
- https://github.com/hzi-bifo/AMR_benchmarking/tree/main/data/PATRIC/cv_folds/loose
- https://github.com/hzi-bifo/AMR_benchmarking/tree/main/data/PATRIC/meta/loose_by_species
- https://pmc.ncbi.nlm.nih.gov/articles/PMC11070729/
- https://www.bv-brc.org/
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11070729/supplementaryFiles
- Status source: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11070729/fullTextXML

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/amr-patric-folds-beat-published-f1.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `amr-patric-folds-beat-published-f1`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]

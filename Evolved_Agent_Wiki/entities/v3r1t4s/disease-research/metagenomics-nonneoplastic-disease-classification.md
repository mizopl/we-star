---
id: v3r1t4s-metagenomics-nonneoplastic-disease-classification
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
# Gut-microbiome disease classification: beat the published cross-validated AUC on public non-cancer disease cohorts

# Overview

> Bank id `metagenomics-nonneoplastic-disease-classification` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Shotgun-metagenomic disease classification (inflammatory bowel disease, type 2 diabetes, liver cirrhosis, obesity, rheumatoid arthritis and other non-cancer conditions) has a public, laptop-scale benchmark lineage: the MetAML study (Edoardo Pasolli, Duy Tin Truong, Faizan Malik, Levi Waldron and Nicola Segata, PLoS Computational Biology 2016) released abundance and marker-presence tables (github.com/SegataLab/metaml/data; no cross-validation fold files are committed) and published cross-validated AUCs per disease and per feature type in the paper itself, and the same cohorts are redistributed as uniformly processed tables in curatedMetagenomicData. Published AUCs for several diseases sit in the 0.6-0.8 range - far from saturated - and cross-cohort generalisation (train on one cohort, test on another of the same disease) is markedly worse and much less studied. The feature tables are megabytes, so the whole benchmark fits on a laptop, and the chief scientific question (is there signal beyond cohort-specific batch structure?) is exactly a question an adversarial verifier can police.

## Success criterion

Success means, for at least one non-cancer disease cohort of the published benchmark, a released model and saved per-sample predictions obtained with the SAME evaluation protocol as the published number (same cohort, same feature table from the repository, same cross-validation scheme - the repository ships no fold files, so repeated stratified k-fold with the published k and >= 20 repeats, with the claimant's fold files committed and hashed before any model is fitted), whose mean AUC is STRICTLY GREATER (direction: max) than the best published AUC for that cohort and feature type, read live from the MetAML paper (https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4939962/fullTextXML) immediately before claiming, by at least 0.03 AND outside a 95% bootstrap/repetition interval. Any feature selection, normalisation fitting or hyperparameter choice must be inside the training folds only, demonstrated by code. For a cross-cohort claim, the test cohort must be untouched during all model development and the comparator must be a published cross-cohort number (or, if none exists, the claim is a new-result claim and must be reported as a partial win, not a record). Because the comparator is a 2016 printed number rather than a maintained leaderboard, the claimant must also reimplement the paper's own baseline (random forest on species abundances) on the same committed folds and beat that re-run by the same margin.

## Partial wins

- {"id": "p1", "statement": "A strictly leak-free cross-cohort result for one disease (train on cohorts A..., test on an untouched cohort B of the same disease) with AUC >= 0.70 and a documented pre-registration of the held-out cohort, together with the within-cohort number for context."}
- {"id": "p2", "statement": "Match the best published within-cohort AUC for one disease to within 0.01 using a model with <= 20 named taxa and no nonlinear learner, releasing the taxa and coefficients - an interpretability/parsimony result."}
- {"id": "p3", "statement": "A reproducible confound audit for one disease: quantify how much of the published AUC is recoverable from sequencing-depth, study-of-origin, age/BMI/country covariates alone (and from label permutation within study), with code and numbers, documenting the fraction of apparent signal that is cohort structure."}

## Verification

Skeptic clones SegataLab/metaml (and, for cross-cohort claims, pulls the matching curatedMetagenomicData tables), hashes the feature tables and the claimant's committed fold files, re-runs the reimplemented random-forest baseline on those folds, reruns the attacker's released pipeline to regenerate per-sample predictions, recomputes AUC per fold with the published protocol, and checks the repetition/bootstrap interval. Leakage audit: confirm that normalisation, feature selection and hyperparameter search are fitted inside folds (re-run with a deliberately corrupted test fold and verify training-side outputs are unchanged), and run the metadata-only and permuted-label controls. Minutes of CPU per cohort.

## Angles

- Compositional-data discipline: abundances are compositional, so centred log-ratio / balance (ILR) transforms with sparse selection of log-ratio balances (selbal/CoDa-LASSO style) often beat generic learners on relative abundances; this is cheap and directly attacks the published numbers.
- CROSS-DOMAIN (ecology, imported as method not metaphor): use diversity partitioning (Hill numbers), co-occurrence network statistics, and neutral-community-model residuals (which taxa deviate from the neutral expectation) as features, rather than raw abundances.
- CROSS-DOMAIN (information theory / compression): compress each sample's taxonomic profile against disease-specific and control-specific reference dictionaries and classify by code-length difference (a normalised-compression-distance classifier), which is nearly parameter-free and robust to depth differences.
- CROSS-DOMAIN (signal processing on graphs): embed the phylogenetic tree as a graph and use graph-Fourier/wavelet transforms of abundance on the tree (phylogenetic multiscale features) so that signal shared across related taxa is pooled - a direct answer to the sparsity of species-level features.
- CROSS-DOMAIN (statistical physics): fit a Potts/Ising model of taxon co-occurrence per class and classify by free-energy difference, capturing community states (dysbiosis as a phase) instead of marginal abundances.
- Cross-cohort robustness as the real target: batch-correction (ComBat-style, or quantile/rank normalisation within cohort), domain-adversarial training, and leave-one-cohort-out evaluation - the published within-cohort numbers are easier than the honest regime, so improvements there are where new science is.

## Pitfalls

- Study-of-origin confounding: in multi-cohort analyses, disease label correlates with cohort, country and sequencing protocol, so a classifier can achieve high AUC by recognising the study. Leave-one-cohort-out plus metadata-only controls is the only honest test.
- Cross-validation leakage: fitting normalisation, batch correction, feature selection or hyperparameters on the whole dataset before splitting is endemic in this literature and inflates AUC by 0.05-0.15. The audit must confirm all fitting is inside folds.
- Protocol mismatch: comparing a repeated-stratified-CV mean to a published single-split number, or using a different feature type (strain markers vs species abundance vs pathways) than the published value, is a fake win; cohort, feature type and CV scheme must all match.
- Sample-size optimism: several of these cohorts have <150 samples, so AUC differences of 0.02-0.03 are noise; require margin plus a repetition interval, and report per-fold values.
- Technical-replicate and household leakage: some cohorts include longitudinal samples or related individuals; samples from the same subject or household must not straddle folds.

## Sources

- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4939962/fullTextXML
- https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004977
- https://github.com/SegataLab/metaml/tree/master/data
- https://github.com/SegataLab/metaml
- https://waldronlab.io/curatedMetagenomicData/
- Status source: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4939962/fullTextXML

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/metagenomics-nonneoplastic-disease-classification.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `metagenomics-nonneoplastic-disease-classification`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]

---
id: v3r1t4s-caid3-disorder-binding-average-precision
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
tractability: 2.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# CAID3 (Critical Assessment of Intrinsic Disorder): beat the published best average precision on the frozen CAID3 reference

# Overview

> Bank id `caid3-disorder-binding-average-precision` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

CAID is the community blind assessment of intrinsic-disorder and disorder-binding predictors run by the BioComputingUP group; round 3 (CAID3, assessed with CASP16, results published 2025) assessed 68 methods on a reference built from DisProt annotations that were not public when predictions were submitted, in categories Disorder-NOX, Disorder-PDB, Binding, Linker and the new Binding-IDR sub-challenge (same proteins and positives as Binding, negatives restricted to disordered non-binding residues, 72.6% of residues excluded), which is the honest, less imbalanced binding bar. Best published average precision (APS) per category, parsed from the Europe PMC full text on 2026-10-15: Disorder-NOX 0.754 (ESMDisPred-2PDB, AUC 0.885); Disorder-PDB 0.928 (PUNCH2, AUC 0.955); Binding 0.249 (IPA-AF2-Protein-bind, AUC 0.775); Binding-IDR 0.514 (bindEmbed21IDR-rawGeneral, AUC 0.641); Linker 0.474 (IPA-AF2-Linker, AUC 0.897). Protein misfolding/aggregation and disorder are directly implicated in neurodegenerative disease, and the CAID3 report itself states that binding-region prediction within known disordered boundaries 'remains challenging', i.e. the metric is far from saturated. The assessment code (BioComputingUP/CAID, caid.py plus vectorized_metrics) and the reference-construction code (BioComputingUP/caid-reference, last pushed 2026-08-13; also caid2-reference) are public on GitHub, so the whole evaluation can be reproduced on a laptop from DisProt plus SIFTS. No CAID4 round was found to be open as of 2026-10-13, which makes this a frozen, fully public held-out benchmark rather than a live submission system.

## Success criterion

Success means a released predictor (code + weights + fixed inference command) whose per-residue scores for the entire CAID3 reference set, scored by the official assessment code (github.com/BioComputingUP/CAID, pinned commit, the same metric implementation and the same reference files the paper used, rebuilt with github.com/BioComputingUP/caid-reference from the DisProt release CAID3 froze), give an average precision STRICTLY GREATER (direction: max) than the best published CAID3 value for that same category and reference subset, read live from the CAID3 assessment paper's ranking table at https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12750029/fullTextXML immediately before claiming (as of 2026-10-15: Disorder-NOX 0.754, Disorder-PDB 0.928, Binding 0.249, Binding-IDR 0.514, Linker 0.474), by at least 0.02 absolute AND by more than the bootstrap standard error the skeptic computes by resampling targets (1,000 resamples). The predictor must use no DisProt annotation newer than the CAID3 freeze, must not query any web server whose training data is unknown, and must be run on all targets of the category with no target dropped and no per-target tuning. Reporting a different metric (AUC instead of APS, or per-residue instead of the official aggregation) does not count.

## Partial wins

- {"id": "p1", "statement": "Beat the best published CAID3 average precision in a binding sub-challenge (the weakest categories, explicitly flagged as unsolved) by >= 0.02 with the official scorer on the rebuilt reference: Binding-IDR (best 0.514, the less imbalanced binding bar) or Binding (best 0.249), even if the disorder categories are not improved."}
- {"id": "p2", "statement": "Match the top-5 published CAID3 disorder average precision to within 0.01 with a predictor that uses NO protein language model and no GPU-trained network (e.g. physicochemical + alignment statistics only), running the full reference in under 30 minutes on a laptop, with timings."}
- {"id": "p3", "statement": "A reproducible negative-control audit: show that the published ranking order of at least 3 CAID3 methods flips when the reference is rebuilt with a documented, defensible choice of negative-set definition (NOX vs PDB-derived negatives), quantified with the official scorer and bootstrap intervals; a methodology finding, reported as such, not a record."}

## Verification

Skeptic clones BioComputingUP/CAID and BioComputingUP/caid-reference at pinned commits, rebuilds the CAID3 reference from the frozen DisProt release plus SIFTS (both public), hashes the reference files, runs caid.py's vectorized metrics on the attacker's prediction files (CAID submission format, one score per residue for every target), bootstraps over targets for an error bar, and re-reads the published CAID3 ranking table. Reproducibility check: rerun the attacker's released inference on 50 random targets and compare scores bit-for-bit (or within documented tolerance). All steps are CPU-only and under an hour.

## Angles

- Ensemble the existing public predictors properly: CAID3's own analysis shows method rankings vary by category and by negative-set definition, so a calibrated stacking (per-residue logistic/isotonic fusion fitted on CAID1/CAID2 references only, never CAID3) of freely available CPU predictors (IUPred, MobiDB-lite, flDPnn-class, AlphaFold-disorder pLDDT/RSA) is a cheap shot at the frontier.
- AlphaFold-derived features at scale: BioComputingUP's own AlphaFold-disorder work shows pLDDT plus predicted relative solvent accessibility is a strong disorder signal; AlphaFold DB models for all reference targets are free to download, so a feature-engineering sweep over smoothing windows and per-residue contact-density is laptop work.
- CROSS-DOMAIN (signal processing): treat per-residue property tracks (charge, hydropathy, complexity) as a 1-D signal and apply matched filters / wavelet multiresolution analysis to detect disorder boundaries; CAID scores boundaries implicitly through average precision, so edge-accurate segmentation (change-point detection, e.g. PELT or Bayesian online change-point) should pay off more than per-residue classification.
- CROSS-DOMAIN (compression / linguistics): low-complexity and compositional bias are hallmarks of disorder; use universal-compressor code length per window (CTW/PPM), entropy-rate estimates, and Zipf/Heaps statistics of k-mer usage as features, plus 'linguistic' detection of repeat grammars (tandem repeats, SLiM-like motifs) for the binding sub-challenge.
- CROSS-DOMAIN (statistical physics): score disorder from a coarse-grained polymer/Flory-type model, predicting per-residue order parameters from sequence charge decoration (kappa, sequence charge decoration SCD) and temperature-like effective solvent terms, which is analytic and instant on CPU.
- Binding sub-challenge specifics: mine public motif resources (ELM classes) and conditional folding signals (AlphaFold models of disordered regions in complex contexts) to score binding propensity within annotated disordered boundaries, the category the assessment calls still weak.

## Pitfalls

- Reference mismatch: CAID3's official reference is a specific DisProt snapshot with a specific negative-set choice; rebuilding it from today's DisProt silently changes the labels (DisProt grows monthly) and can inflate or deflate APS. The skeptic must rebuild from the frozen release used by CAID3 and hash the files, or the comparison is void.
- Hidden training on the test labels: nearly all modern disorder predictors are trained on DisProt/PDB-missing-residue data; if the attacker's model (or any ensemble component, including a downloaded web-server predictor) was trained after the CAID3 freeze, the CAID3 targets are in its training set and the whole result is leakage.
- Metric substitution: CAID ranks by average precision on a specific target set and aggregation; reporting AUC-ROC, balanced accuracy, or a per-residue micro-average over pooled residues will look better and means nothing. Also disorder is heavily imbalanced, so ROC numbers are deceptively high.
- Dropping hard targets or short proteins, or predicting only within regions where another predictor is confident, changes the denominator; every target in the category must be scored.
- Treating the CAID3 paper's headline improvement percentages as the bar instead of the per-category best APS value in the ranking table; the record must reference the live table and a direction (max).
- pmc.ncbi.nlm.nih.gov now serves a reCAPTCHA page to plain requests; read the article through Europe PMC (https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12750029/fullTextXML) instead of https://pmc.ncbi.nlm.nih.gov/articles/PMC12750029/.

## Sources

- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12750029/fullTextXML
- https://github.com/BioComputingUP/CAID
- https://github.com/BioComputingUP/caid-reference
- https://caid.idpcentral.org/challenge
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12750029/
- https://disprot.org/
- Status source: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12750029/fullTextXML

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/caid3-disorder-binding-average-precision.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `caid3-disorder-binding-average-precision`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]

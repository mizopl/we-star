---
id: v3r1t4s-cat-disease-research
type: concept
tags: [v3r1t4s, v3r1t4s/category]
inbound_links: 2
confidence: 0.9
last_ingested_sources: [".raw/V3R1T4S/bank/categories.json@7dd4480"]
---
# V3R1T4S Disease research

# Overview

Cancer, rare and neglected diseases, antimicrobial resistance and outbreaks: public data, public scorers, computational claims only. — 51 open problems in the bank.

## Status (live)

```dataview
TABLE status, priority, kind, tractability, disclosure
FROM "wiki/entities/v3r1t4s/disease-research"
SORT tractability DESC
```

## Problems

| Problem | Kind | Tractability | Disclosure |
|---\lvert ---\rvert---\lvert ---\rvert
| [[iedb-mhci-bd2009-blind-auc]] | harvest | 4 | open |
| [[immrep22-tcr-epitope-microauc]] | harvest | 4 | open |
| [[proteingym-cancer-dms-supervised-5fold]] | harvest | 4 | open |
| [[proteingym-cancer-dms-zero-shot]] | harvest | 4 | open |
| [[pycox-metabric-gbsg-breast-cancer-survival]] | harvest | 4 | open |
| [[tdc-drugcomb-css-mae]] | harvest | 4 | open |
| [[tdc-drugcomb-synergy-four-endpoints]] | harvest | 4 | open |
| [[flusight-ed-visits-beat-ensemble-wis]] | harvest | 3.5 | open |
| [[flusight-retrospective-beat-ensemble-wis]] | harvest | 3.5 | open |
| [[amr-patric-folds-beat-published-f1]] | harvest | 3 | open |
| [[covid19-forecast-hub-retrospective-beat-ensemble-wis]] | harvest | 3 | open |
| [[covid19-hub-europe-archive-beat-eurocovidhub-ensemble]] | harvest | 3 | open |
| [[cryptic-tb-resistance-beat-who-catalogue]] | harvest | 3 | open |
| [[dengue-2015-open-challenge-beat-published-skill]] | harvest | 3 | open |
| [[dreval-cross-study-ctrpv2-to-gdsc2]] | harvest | 3 | open |
| [[dreval-lco-ctrpv2-normalized-r2]] | harvest | 3 | open |
| [[dreval-ldo-beat-naive-mean-effects]] | harvest | 3 | open |
| [[driams-maldi-amr-beat-published-auroc]] | harvest | 3 | open |
| [[german-hospitalization-nowcast-hub-beat-ensemble-wis]] | harvest | 3 | open |
| [[hest-bench-cancer-expression-from-morphology]] | harvest | 3 | open |
| [[isic2018-task2-attribute-detection-jaccard]] | standard | 3 | open |
| [[isic2019-diagnosis-balanced-accuracy-with-unknown]] | harvest | 3 | open |
| [[linear-baseline-perturbation-replogle-k562]] | harvest | 3 | open |
| [[medmnist-pathmnist-breastmnist-accuracy]] | harvest | 3 | open |
| [[metagenomics-nonneoplastic-disease-classification]] | harvest | 3 | open |
| [[mfass-splice-disruption-beat-pangolin-ap]] | harvest | 3 | open |
| [[ncbi-pathogen-ast-ecoli-genotype-phenotype-f1]] | harvest | 3 | open |
| [[nih-thin-smear-malaria-patient-grouped-sensitivity]] | harvest | 3 | open |
| [[perturbench-frangieh21-melanoma-transfer]] | harvest | 3 | open |
| [[perturbench-jiang24-cancer-lines-transfer]] | harvest | 3 | open |
| [[perturbench-norman19-combo-prediction]] | harvest | 3 | open |
| [[perturbench-srivatsan20-cell-line-transfer]] | harvest | 3 | open |
| [[phenopacket-store-rare-disease-gene-prioritization]] | harvest | 3 | open |
| [[proteingym-clinical-indels-auc]] | harvest | 3 | open |
| [[proteingym-dms-indels-zeroshot-spearman]] | harvest | 3 | open |
| [[raredis-corpus-rare-disease-ner-f1]] | harvest | 3 | open |
| [[respicast-covid19-hub-beat-ensemble-wis]] | harvest | 3 | open |
| [[respicast-ili-ari-europe-beat-hub-ensemble]] | harvest | 3 | open |
| [[rsv-hub-retrospective-beat-ensemble-wis]] | harvest | 3 | open |
| [[tcga-multiomics-survival-cindex-herrmann]] | harvest | 3 | open |
| [[caid3-disorder-binding-average-precision]] | harvest | 2.5 | open |
| [[code-test-ecg-abnormality-f1]] | harvest | 2.5 | open |
| [[isic2017-part3-melanoma-sk-mean-auc]] | standard | 2.5 | open |
| [[isic2018-lesion-segmentation-thresholded-jaccard]] | standard | 2.5 | open |
| [[isic2018-task3-lesion-diagnosis-balanced-accuracy]] | standard | 2.5 | open |
| [[openkbp-dose-prediction-test-dose-dvh-score]] | standard | 2.5 | open |
| [[pcam-patchcamelyon-from-scratch-accuracy]] | standard | 2.5 | open |
| [[proteingym-clinical-substitutions-auc]] | harvest | 2.5 | open |
| [[ptbxl-ecg-macro-auc-fold10]] | standard | 2.5 | open |
| [[dreval-exvivo-beataml2-pdx-transfer]] | moonshot | 2 | open |
| [[luna16-nodule-detection-cpm-10fold]] | standard | 2 | open |

## Citations

- [Category README](../../../../.raw/V3R1T4S/known-unknowns/disease-research/README.md)
- [categories.json](../../../../.raw/V3R1T4S/bank/categories.json)

## Related Nodes

- [[V3R1T4S]]
- [[V3R1T4S Status Board]]

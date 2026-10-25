---
id: v3r1t4s-indus-temporal-heldout-structure
type: entity
tags: [v3r1t4s, v3r1t4s/undeciphered-scripts, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "CONFIRMED_SOLUTION"
priority: ""
notes: ""
category: undeciphered-scripts
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Indus script: structural model trained on the 1977 corpus that predicts later-excavated inscriptions

# Overview

> Bank id `indus-temporal-heldout-structure` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

The Indus script is undeciphered: about 4,000-5,600 texts, 400-700 signs, and very short inscriptions (about 5 signs on average). The open structural sub-problems are the sign function classes (numeral strokes, the frequent 'jar' terminal, fish-sign variants), whether texts split into reusable segments, and whether those segments are consistent across sites (Harappa, Mohenjo-daro, Lothal, Gulf/Mesopotamian seals). The task is a structural finding that is genuinely predictive. Mahadevan's 1977 concordance (M77) gives a natural time split: models fitted only on M77 can be tested on inscriptions published after 1977, held in the larger indus_website and ICIT corpora. Status as of 2026-10-03: Undeciphered as of 2026-10-03. The USD 1M Tamil Nadu prize (Jan 2025) is unclaimed, with no formal submission portal. 2026 decipherment claims (Zenodo, LLM-dictionary) are unaccepted. paragorth/Indus- (Sept 2026) shows that with more than about 150 signs, wrong keys beat true keys under every objective tested. arXiv 2608.02999 (Aug 2026) shows the standard statistics are non-specific.

## Success criterion

A concrete structural claim, for example 'sign class C marks segment-final position', 'segment S is a reusable unit', or 'stroke signs N1-N7 behave as a numeral system with classifier X'. It must be fitted only on M77 texts and frozen in a timestamped file. On the post-M77, non-duplicate held-out texts (deduplicated by object ID and exact sequence) it must predict a measurable property with paired-bootstrap p < 0.001 against BOTH (i) a tuned Kneser-Ney 3-gram trained on the same M77 data and (ii) a SIGIL-style non-linguistic synthetic control matched on unigram and length distribution. Example properties: masked-sign top-1 accuracy, held-out segment-boundary agreement with site-specific variants, or prediction of seal versus tablet object type from sequence. The effect must also replicate separately on at least 2 sites. A claim says 'structural finding', never 'decipherment'. Additionally: (a) Each held-out object has a documented first-publication source dated after 1977 (CISI volume or excavation report); objects without one are excluded. (b) Dedup by seal impression identity: sealings of the same seal count once (use paragorth's 386-identity directory where applicable). (c) The claim is not equivalent to any of paragorth's frozen predictions P1-P9 or Q1-Q14, or to published positional findings (Mahadevan 1977, Rao et al. 2009/2010, Yadav et al., Kriger & Hunt 2026). (d) The effect must beat both baselines on Mohenjo-daro and on Harappa separately.

## Partial wins

- {"id": "p1", "statement": "A frozen, M77-only structural claim that meets every condition of the full criterion (publication-dated post-1977 held-out set, seal-identity dedup, novelty vs paragorth P1-P9/Q1-Q14 and published positional findings, paired-bootstrap p < 0.001 against both the tuned Kneser-Ney 3-gram and the SIGIL-style synthetic control) on the pooled held-out set and on one of Mohenjo-daro or Harappa, but not yet on the other."}
- {"id": "p2", "statement": "Field-symbol conditioning: a frozen M77-only model that predicts the field symbol (unicorn, bull, elephant, etc.) of deduplicated post-1977 held-out seals from the text's terminal segment with accuracy exceeding both the majority-motif baseline and a Kneser-Ney 3-gram-feature classifier trained on the same M77 data, paired-bootstrap p < 0.001, and not among paragorth's frozen predictions."}
- {"id": "p3", "statement": "Ligature substitution: a frozen M77-only list of composite signs AB whose substitution rate for the bigram A B in parallel contexts of the held-out texts exceeds that of frequency-matched random composite/bigram pairs with permutation p < 0.001, not among paragorth's frozen predictions or published positional findings."}

## Verification

The verifier clones joyboseroy/indus_decipher (with the M77 CSV) and paragorth/Indus- (im77 plus the derived 5,369-object corpus) and rebuilds the time split independently. It dedups by sequence plus object ID and reruns the frozen model alongside its own KN 3-gram and synthetic control. It checks that no held-out sequence appears in the training data and that reading direction is correct (the joyboseroy repo documents a reversal bug). The p-values are recomputed with 10,000 bootstrap resamples. Additionally, the verifier rebuilds the split from publication metadata, not from corpus membership; confirms no held-out sequence or seal identity appears in training; and diffs the claim against the paragorth frozen prediction files (P1-P9, Q1-Q14).

## Sources

- https://github.com/joyboseroy/indus_decipher
- https://github.com/paragorth/Indus-
- https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan
- http://www.indus.epigraphica.de
- https://arxiv.org/abs/2608.02999
- Status source: https://github.com/joyboseroy/indus_decipher

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/undeciphered-scripts/indus-temporal-heldout-structure.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `indus-temporal-heldout-structure`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Undeciphered scripts]]
- [[V3R1T4S]]

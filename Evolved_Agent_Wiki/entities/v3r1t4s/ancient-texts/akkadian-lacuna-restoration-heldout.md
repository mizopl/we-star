---
id: v3r1t4s-akkadian-lacuna-restoration-heldout
type: entity
tags: [v3r1t4s, v3r1t4s/ancient-texts, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "CONFIRMED_SOLUTION"
priority: ""
notes: ""
category: ancient-texts
kind: harvest
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-08"
---
# Akkadian: restore masked/damaged signs in Oracc/eBL transliterations, beating the Lazar et al. 2021 held-out benchmark with frozen predictions

# Overview

> Bank id `akkadian-lacuna-restoration-heldout` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

Lazar, Saret, Yehudai, Horowitz, Wasserman and Stanovsky (EMNLP 2021, arXiv 2109.04513) framed filling gaps in Akkadian transliterations as masked language modelling on about 1M words / 2.3M signs scraped from Oracc. Their best model (MBERT+Akk, greedy decoding) reports hit@5 = 0.89 and MRR = 0.83 on a 20% held-out split with 15% random masking, and they released code and the scraped data (github.com/SLAB-NLP/Akk, MIT, data/akk_from_jsons.jsonl 21 MB, last commit 2022-11-10). The paper's split is a random 80/20 split by text (about 8K train / 2K test texts) with no published seed, so the exact test set cannot be reproduced; the shipped data file (data/akk_from_jsons.jsonl, 21.2 MB, repository commit dfd2a66d of 2022-11-10) is the frozen corpus. Vetter re-check 2026-10-08: two literature searches found no later work reporting hit@k/MRR on this task (later Akkadian work is NMT: Gutherz et al. 2023, TabletCraft 2026). The real-world task is restoring the editorial gaps ('x', [...]) that remain unrestored in Oracc and eBL editions; eBL alone has 625,844 transliterated lines, a large fraction containing bracketed editorial restorations that can serve as a natural held-out test.

## Success criterion

On the SLAB-NLP/Akk released data (data/akk_from_jsons.jsonl at commit dfd2a66d or a later recorded commit), with an 80/20 split by text and the 15% random masking of the repository's evaluate_bert.py reproduced with a documented fixed seed, the frozen list of masked positions published (hash) before any model is trained, and masked units being whole whitespace-delimited transliteration tokens (words) scored by exact string match as in the repository's single-token evaluation: (1) the claimant retrains the paper's MBERT+Akk baseline with the repository code and default hyperparameters on the same frozen split and freezes its top-5 predictions (hash) - its hit@5 must land within 0.02 of 0.89 on the frozen masked positions, otherwise the split is not comparable and no full win is possible; (2) a prediction file (top-5 per masked token) for the new system, frozen (hash) before scoring and trained/tuned ONLY on the training split, scores BOTH hit@5 and MRR strictly above the paper's values (re-read from the arXiv/ACL paper immediately before claiming) AND strictly above the reproduced baseline on the identical masked positions. Any use of test documents, of eBL/Oracc texts that duplicate test documents (same P/Q number or same composition), or of a corpus fetched after the split was frozen voids the claim.

## Partial wins

- {"id": "p1", "statement": "Same protocol as the full criterion (including the reproduced baseline), beating only hit@5 or only MRR by at least 1 absolute point over both the paper's value and the reproduced baseline; or beating both metrics on a genre subset for which the paper reports a per-genre number (re-read from the paper's per-genre table/figure; genre defined by Oracc project as in the paper)."}
- {"id": "p2", "statement": "Natural-lacuna holdout: a permanent held-out set of at least 2,000 editorially restored signs (text inside [ ] in eBL fragments with joins == [] and no corpus-chapter manuscript link, sampled by a published deterministic rule from fragments fetched on a recorded date, hashed before training) is masked and predicted with frozen top-5 predictions. All training material must exclude any line sharing 6 or more consecutive signs with the 20-sign context window around any holdout gap (parallel/duplicate exclusion, re-checked by the verifier). hit@1 at least 0.50 and hit@5 at least 0.75, with BOTH a unigram-frequency baseline and a k-NN retrieval baseline over the filtered training set reported alongside and beaten by at least 20 absolute points on hit@1."}

## Verification

The verifier re-creates the split and masks from the published seed/rule on the recorded data commit, checks the hashes of both frozen prediction files (baseline and new system) against the hashes committed before training (timestamps from the pre-registered holdout protocol), rescores hit@k/MRR for both with independent code on the identical masked positions, and checks that no test document or duplicate (same Oracc P/Q number, composition, or eBL museum number) appears in the training material. Rescoring is minutes; the verifier never retrains.

## Angles

- Character/sign-level n-gram or small transformer LMs trained from scratch on signs (not words) with genre tags; the 2021 model was a word-level MBERT fine-tune and never used sign-level context.
- Retrieval-augmented restoration: Akkadian royal inscriptions and omens are highly formulaic, so k-NN over duplicate passages in the training split can restore many gaps exactly.
- Ensemble a forward and backward sign LM with a lexicon constraint (only attested sign sequences for the word), which directly targets MRR.
- Build the natural-lacuna holdout (p2) from eBL bracketed restorations, stratified by genre and gap length, and seal it before any training.
- Report per-gap-length curves; long gaps dominate the real editorial need and are where the 2021 model fails.

## Pitfalls

- The 2021 split is produced by code with no published seed, not shipped as files; a different seed or Oracc scrape yields a different test set. Only the reproduced-baseline control makes a beat meaningful.
- Massive duplication in Oracc (parallel manuscripts of the same composition, RINAP duplicates) leaks test text into training; deduplicate by composition/Q number or report leakage.
- Editorial restorations are themselves often made from parallels: hit rates on bracketed text overstate performance on truly unknown gaps.
- LLM-judged 'plausibility' of restorations is not a criterion; only frozen top-k predictions scored against held-out text count.

## Sources

- https://github.com/SLAB-NLP/Akk
- https://arxiv.org/abs/2109.04513
- https://ar5iv.labs.arxiv.org/html/2109.04513
- https://www.ebl.lmu.de/api/statistics
- https://oracc.museum.upenn.edu/
- Status source: https://github.com/SLAB-NLP/Akk

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/ancient-texts/akkadian-lacuna-restoration-heldout.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `akkadian-lacuna-restoration-heldout`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Ancient texts and fragments]]
- [[V3R1T4S]]

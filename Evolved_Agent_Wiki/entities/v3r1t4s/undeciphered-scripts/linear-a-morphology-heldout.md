---
id: v3r1t4s-linear-a-morphology-heldout
type: entity
tags: [v3r1t4s, v3r1t4s/undeciphered-scripts, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: undeciphered-scripts
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Linear A: pre-registered morphological alternations that predict held-out contexts

# Overview

> Bank id `linear-a-morphology-heldout` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

With Linear B phonetic values applied to Linear A homomorphs, Linear A words can be transliterated, but the language is unknown. Morphology is the open sub-problem. Candidate alternations have been discussed (initial A-/JA-, final -TE/-TI/-NA/-RE variation, libation-formula variants such as JA-SA-SA-RA-ME and A-SA-SA-RA-ME), but none has been shown to predict distribution. The task is to find affix or alternation rules whose presence predicts where a word occurs: its document type, its adjacency to a logogram (VIR/personnel versus commodity), its site, or libation-formula position. Data caveat: in Navarre-AI corpus.json (release 2026-09-18, 1,884 records) the 'words' field is present on only 666 records (SigLA-derived); other records' words come from lineara.xyz with different division conventions. Status as of 2026-10-03: Partly deciphered at the phonetic level; the language is unknown. The 2026 Di Mino 'Ya Diktu' Semitic grammar is unverified, and the adversarial replication kbennett2000/linear-a-check finds its root matches are no better than scrambled controls. The corpus infrastructure was updated in September 2026 (Navarre-AI release 2026-09-18).

## Success criterion

A frozen list of at most 10 alternation hypotheses is written before evaluation. Held-out data is every document from a whole site (for example, all Khania or all Zakros) or a random 30% of documents, chosen beforehand. At least one hypothesis must predict a held-out contextual variable with Bonferroni-corrected p < 0.001 (Fisher exact or permutation test over word-to-context assignments). Examples: 'words ending -RE precede personnel logograms', 'A-/JA- alternation tracks libation versus administrative support'. The effect must survive dropping the single most frequent word type. Hypotheses in the published literature that do not reach significance do not count. A published hypothesis reaching this significance for the first time does count, with that stated. Additionally: tokens come from a single declared word_source (SigLA or lineara.xyz), or the result must replicate in both; tokens containing uncertain or unidentified signs (e.g. 're?', '[?]') are excluded; the held-out split is by whole site or by document, never by token; and every hypothesis is checked for novelty against existing libation-formula studies (e.g. Davis 2014 on stone vessels).

## Partial wins

- {"id": "p1", "statement": "A frozen hypothesis (from a pre-registered list of at most 10) that, on the pre-declared held-out site or document split, under one declared word_source and excluding uncertain-sign tokens, predicts the held-out contextual variable at Bonferroni-corrected p < 0.01 (rather than the full bar of p < 0.001), survives dropping the most frequent word type, and has not previously reached that significance in the literature."}
- {"id": "p2", "statement": "Onomastic cross-prediction: Linear A sign-groups that also occur as Linear B personal names or toponyms at Knossos (list frozen before evaluation) are adjacent to personnel logograms (VIR etc.) on held-out documents significantly more often than non-shared sign-groups of matched length and frequency (Fisher exact or permutation p < 0.001), surviving the drop of the most frequent type, with the effect not already published."}

## Verification

The verifier pins the Navarre-AI commit and filters by word_source. It rebuilds tokens, excludes uncertain signs, re-applies the frozen regexes, recomputes Fisher or permutation tests with Bonferroni correction over all frozen hypotheses, reruns with the most frequent type dropped, and checks the git timestamp order.

## Sources

- https://github.com/Navarre-AI/linear-a
- https://sigla.phis.me
- https://github.com/mwenge/lineara.xyz
- https://github.com/kbennett2000/linear-a-check
- Status source: https://github.com/Navarre-AI/linear-a

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/undeciphered-scripts/linear-a-morphology-heldout.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `linear-a-morphology-heldout`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Undeciphered scripts]]
- [[V3R1T4S]]

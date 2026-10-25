---
id: v3r1t4s-oracle-bone-undeciphered-chars
type: entity
tags: [v3r1t4s, v3r1t4s/undeciphered-scripts, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: undeciphered-scripts
kind: standard
tractability: 1
compute: "laptop-hours (inference only; full method training needs GPU)"
disclosure: open
status_checked: "2026-10-03"
---
# Oracle bone script: identifications of undeciphered characters validated by held-out prediction

# Overview

> Bank id `oracle-bone-undeciphered-chars` · standard · tractability 1 · laptop-hours (inference only; full method training needs GPU) · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

About 4,500 distinct Shang oracle-bone characters are known, and only about 1,600 are deciphered. The National Museum of Chinese Writing (Anyang) offers 100,000 yuan per deciphered character and 50,000 yuan for settling a disputed one, subject to sufficient evidence. AI methods (Open-Oracle, OracleFusion 2025, generative dictionary retrieval in April 2026 (arXiv 2604.09668), a GAN-based human-computer approach in Heritage Science 2026) propose candidates, but acceptance requires paleographic chains through bronze and seal forms plus context in inscriptions. The '~1,600 of ~4,500 deciphered' framing is from arXiv 2506.21101 (OracleFusion, ICCV 2025). Status as of 2026-10-03: Active AI work in 2025-2026 (OracleFusion ICCV 2025; generative dictionary retrieval arXiv 2604.09668, Apr 2026; GAN approach in Heritage Science 2026). The large majority of characters remain undeciphered (about 1,500-1,600 of about 4,500-4,600 read). The Anyang museum reward stands (100,000 yuan per character, expert-adjudicated).

## Success criterion

Both steps are required. (1) Method validation: the code first reproduces the best published top-10 accuracy on the unseen-character split of arXiv 2604.09668 (or a HUST-OBC / EVOBC time split) as listed at verification time (54.3% top-10 in 2604.09668 as of 2026-10-03), and the method is not significantly worse than that best value. (2) For at least 1 undeciphered character, a proposed modern equivalent with a complete paleographic chain (oracle bone to bronze to seal to clerical form, each link an attested form with source cited). Substituting the character must give grammatical readings in at least 5 different inscriptions with consistent syntactic role. A documented Chinese-language novelty search (Xiaoxuetang, CNKI, Anyang databases) shows the identification is unpublished. A claim may report only 'candidate identification', never 'deciphered', because acceptance takes expert review (the Anyang museum reward is expert-adjudicated). Retrieval hits on the dictionary alone are not identifications.

## Partial wins

- {"id": "p1", "statement": "On the exact unseen-character split of arXiv 2604.09668, after reproducing its baseline, a frozen method achieves top-10 accuracy strictly higher than the best value published for that split at verification time (54.3% as of 2026-10-03), with the improvement significant under paired bootstrap at p < 0.01."}
- {"id": "p2", "statement": "On a HUST-OBC or EVOBC time split (characters whose decipherment was published after a stated cutoff are hidden), a frozen method ranks the accepted modern equivalent in its top 10 for a strictly larger fraction of hidden characters than the best published method on that split at verification time, paired bootstrap p < 0.01."}

## Verification

For (1), the verifier reruns the baseline and the claim on the stated split with fixed seeds and recomputes the bootstrap. For (2), the verifier checks each chain link in cited sources and reads the 5 inscriptions. This part is human and expert-dependent.

## Sources

- https://github.com/Yuliang-Liu/Open-Oracle
- https://arxiv.org/abs/2506.21101
- https://arxiv.org/html/2604.09668v1
- https://arxiv.org/pdf/2508.10113
- https://www.nature.com/articles/s40494-026-02509-4
- Status source: https://github.com/Yuliang-Liu/Open-Oracle

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/undeciphered-scripts/oracle-bone-undeciphered-chars.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `oracle-bone-undeciphered-chars`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Undeciphered scripts]]
- [[V3R1T4S]]

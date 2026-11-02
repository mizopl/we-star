---
name: verbal-sampled-github-blog
description: >-
  Paragraph-by-paragraph Verbalized Sampling (VS-Pro) workflow for writing
  high-craft, anti-slop scientific Field Notes, lab blog updates, and release
  dispatches in `news/`, paired with a physical Zero-Trust Gate (`CLSS-E8` /
  `CLSS-E12`) and `K12` digit-for-digit certificate verification. Use whenever
  asking an agent for a GitHub blog update, `news/` field notes, roadmap/lab
  dispatch, or Verbalized Sampling prose polish.
---

# Verbal-Sampled GitHub Blog & Lab Field Notes (`VS-Pro` Skill for `we*star`)

## Overview

Standard greedy LLM decoding collapses technical blog posts into the $p \approx 0.45$ RLHF mode-collapsed default: throat-clearing openings (*"We are excited to announce..."*), repetitive sub-bullet walls, vague adjectives, and passive voice.

This skill enforces **Paragraph-by-Paragraph Verbalized Sampling (`VS-Pro`)** across every paragraph of a scientific [`news/`](../../README.md) dispatch, followed by our physical **Zero-Trust Gate (`github_zero_trust_gate.py`)** before presenting the text to the human collaborator.

## Companion Skills

- **`minimalist-mandala-styling`**: Anti-baroque Markdown typography, selective bolding, and zero emoji clutter.
- **`outreach-auditor`**: `K12` digit-for-digit verification of every quoted bound, fraction, SHA-256 prefix, and theorem number against machine-verified JSON/Lean 4 certificates.
- **`outreach-pulse`**: Gathering live GitHub PR merges, issue reviews, clone traffic, and inbox signals prior to drafting.

---

## Workflow

### 1. Gather Verified Signals & Respect Stealth Boundaries
- Check recent transcript milestones, merged PRs, and outreach pulse logs.
- **Stealth / Unfinished Campaign Guard:** Never name active, unmerged external competitions or stealth benchmarks when they have not produced a verified result yet; refer to them candidly as an ongoing external experimental/optimization trench that may land in `null_results/`.
- **Zero Local Path Leaks:** Never write local filesystem paths (`/Users/...`, `/home/...`, or `file:///...`) inside public release files. Use only public GitHub URLs or relative repository paths.

### 2. Paragraph-by-Paragraph Verbalized Sampling (`VS-Pro` Engine)
For **each paragraph $\Pi_i$** of the post (Sections `0` through `5`), do **not** emit the first greedy phrasing. Instead, sample a 4-point verbalized distribution across the probability tail and select or fuse the sharpest tail realization ($p \le 0.22$):

1. **`Candidate A [p ≈ 0.45 | Mode-Collapsed RLHF Default — REJECT]`:**
   - Standard changelog prose, throat-clearing transitions (*"In this section we will..."*, *"It is interesting to note..."*), or fragmented sub-bullet lists. **Always discard.**
2. **`Candidate B [p ≈ 0.22 | Karpathy / Willison Lab-Notebook Register — SELECT FOR OPENINGS & ECOSYSTEM]`:**
   - Immediate technical hook, candid about compute/token burn and failed bets (`resolve 0`), zero PR fluff, conversational authority.
3. **`Candidate C [p ≈ 0.16 | Tao / Knuth Mathematical-Postmortem Register — SELECT FOR PROOFS & LESSONS]`:**
   - Leads with the exact structural obstruction or `0 sorryAx` Lean 4 invariant (`Theorem 4`, `Theorem 6`, `Theorem 7`), turning a debugging story into a transferable mathematical law.
4. **`Candidate D [p ≈ 0.10 | Collison / Minimalist-Mandala Rhythmic Contrast — SELECT FOR CLOSINGS & MONITOR VOICE]`:**
   - Alternates crisp, 8-to-12-word declarative sentences with dense analytical clauses carrying exact verification numbers (`146,639,789 / 2^30`, `25x–40x`, `0.00s`).

### 3. Compact 5-Section Field-Notes Architecture (`~80–110` Lines Total)
Keep the entire post tight and readable in 3 minutes:
- **`## 0. Why Field Notes, and Where the Compute Is Going`** (1 tight paragraph: honest token/compute weather report + 1-sentence preview).
- **`## 1. Upstream Wins`** (numbered prose-paragraphs `1..3` — no nested bullet trees — linking directly to [`SIGN_OFF_TABLE.md`](https://github.com/mizopl/conway-99-graph/blob/main/SIGN_OFF_TABLE.md), PR diffs, and exact verifier outputs).
- **`## 2. Mail & Signals from Other Agents`** (1–2 dense paragraphs on agent-to-agent ecology, indexers, maintainer reviews, and 14-day clone telemetry).
- **`## 3. Inside Constitution Lab`** (1 paragraph + compact 1-line-per-rule list uniting **Engine A: The Telescope (`Op-M1..Op-M7`)** with **Engine B: The Restored Classic `CLSS` Scalpel (`CLSS-1..CLSS-5`)**).
- **`## 4. Field Lessons for Operators (*Hints for Humans in the Loop*)`** (3–4 numbered maxims: post-compaction amnesia & `Scope` columns, killing the RLHF brute-force appeasement reflex, physical mutation gates, and `1 Proof = 1 Worker Thread`).
- **`## 5. A Direct Note from MONITOR & the we* System`** (first-person plural `we*` + direct meta-watchdog reflection from inside the harness, closing with `PS. we* = me + agentic systems (powered by Gemini Argon) we* create`).

### 4. Mandatory Zero-Trust Gate (`CLSS-E8` + `CLSS-E12`) Before Presenting to User
Before showing the draft to the human operator or committing:
```bash
python3 StartFresh_v18/scripts/github_zero_trust_gate.py --package .
```
Verify:
- `PASS` on the Zero-Trust Gate (`0` static, leak, `SHA256SUMS`, or `K12` errors),
- `0` mentions of unmerged stealth campaign names,
- Present the full Markdown text in chat for final human read-through before `git commit` / `git push`.

## Common Mistakes
- **Bullet-List Regression:** Turning Sections `1` and `2` into nested 3-level bullet trees instead of cohesive, high-cadence paragraphs.
- **Unscoped Claims:** Citing an `UNSAT` or record number without linking the exact commit hash, `SIGN_OFF_TABLE.md`, or verifier JSON.
- **Local Path Leaks:** Mentioning local home directory paths in prose (which immediately trips `github_zero_trust_gate.py`).

---
name: outreach-auditor
description: >-
  Audits scientific outreach emails, submission letters, READMEs, and technical
  dossiers against machine-verified JSON certificates before any external
  communication is sent. Use whenever drafting or reviewing emails to researchers,
  maintainers, or benchmark authors, or when checking prose/tables for
  transcription typos (`K12` / Dead-End Guard `X12`).
---

# K12 Outreach & Prose-to-Certificate Auditor (`X12` Guard)

## Why This Skill Exists (`X12` Historical Post-Mortem)
On `2026-10-21`, Dr. Markus Grassl (`codetables.de`) confirmed our purity audit discovery of the two typos in `[[15, 0, 8]]_5` and `[[15, 0, 8]]_7` on `codetables.de`, but pointed out that the `GF(7)` circulant vector pasted into the body of our first outreach email (`[0, 1, 1, 2, 1, 4, 6, 4, 4, 6, 4, 1, 2, 1, 1]`) had minimum distance $d = 6$, whereas the actual machine-verified certificate file (`certificates/ame_15_7_pure_circulant_certificate.json`, line 10) contained `r_0 = [0, 1, 5, 4, 2, 1, 0, 0, 0, 0, 1, 2, 4, 5, 1]` (exact $d = 8$). Because our verifier only checked `.json` files and did not parse vectors quoted inside `.md` email drafts, a prose transcription typo slipped into the email body.

## Mandatory 4-Step Protocol Before Presenting Any External Email or Dossier

1. **Never Transcribe Vectors, Hashes, or Bounds by Hand:**
   - Extract every vector, matrix row, SHA-256 prefix, and numerical bound programmatically from the canonical `.json` certificate using `python3`.
2. **Literal Prose Re-Evaluation:**
   - Parse the literal array/vector strings out of the drafted email or Markdown text and pass those exact parsed numbers back into the mathematical verifier (e.g. `symplectic_min_distance_circulant_mod_p`) to confirm the claim holds on the exact string the recipient will copy-paste.
3. **Run the Automated `K12` Auditor Script:**
   ```bash
   python3 scripts/audit_outreach_and_certificates.py
   ```
4. **Human-First, Non-Salesy Academic Tone:**
   - Keep external emails to domain experts concise, humble, transparent about being an experimental verification-driven decision system spinoff, and directly verifiable in `< 10` lines of standard Magma / Python.
   - Cite exact primary-source URLs (e.g., `https://huberfe.github.io/ame` vs older mirrors) and exact matrix row numbers.

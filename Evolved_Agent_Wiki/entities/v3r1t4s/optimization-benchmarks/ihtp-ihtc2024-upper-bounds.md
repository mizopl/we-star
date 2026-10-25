---
title: "ihtp-ihtc2024-upper-bounds"
category: "entity"
created: "2026-10-18"
updated: "2026-10-18"
sources:
  - "~/v3r1t4s/runs/2026-10-18-1607/report.md"
  - "~/v3r1t4s/runs/2026-10-18-1607/code/benchmark_60_results.json"
  - "~/v3r1t4s/outbox/2026-10-18-mizopl-900443ab/README.md"
tags: ["v3r1t4s", "optimization-benchmarks", "ihtc2024", "ihtp", "seam-surgery"]
---

# `ihtp-ihtc2024-upper-bounds` (IHTC-2024 Benchmark Suite `i01..i30`, `m01..m30`)

## Target Overview

- **Category:** `optimization-benchmarks` (`disclosure: open`)
- **Primary Leaderboard:** `https://ihtc2024.github.io/ihtp/index.html` (`60` instances: `30` public `i01..i30` and `30` hidden `m01..m30`)
- **Status:** **`CONFIRMED_SOLUTION`** on `i27` (`50,976 -> 50,063`, `-913`, packaged in `~/v3r1t4s/outbox/2026-10-18-mizopl-900443ab/`); **31 / 60 instances strictly improved** in `~/v3r1t4s/runs/2026-10-18-1607/data/solutions_31_improved.tar.gz`.

## All 31 Strict World-Record Improvements (`Total violations = 0`)

Across all 60 instances with fixed parameters (`seed=42, nra_sec=1.5, coupled_sec=1.0`, plus deep MILP polish on `i27`), `seam_surgery_ihtp.cc` strictly improved **31 / 60** published upper bounds (`16` public `i`-instances and `15` hidden `m`-instances):

| Rank | Instance | Previous Best (`ihtc2024.github.io`) | New Cost (`Total violations = 0`) | Improvement |
|---:|---|---:|---:|---:|
| 1 | **`i27`** (packaged) | `50,976` | **`50,063`** (`50,078` single-pass) | **`-913`** (`-898`) |
| 2 | `m23` | `19,353` | `18,919` | `-434` |
| 3 | `m16` | `10,141` | `9,854` | `-287` |
| 4 | `i21` | `22,553` | `22,282` | `-271` |
| 5 | `m27` | `35,685` | `35,442` | `-243` |
| 6 | `i18` | `15,826` | `15,610` | `-216` |
| 7 | `i23` | `19,704` | `19,500` | `-204` |
| 8 | `i28` | `45,863` | `45,673` | `-190` |
| 9 | `i30` | `43,399` | `43,212` | `-187` |
| 10 | `m30` | `51,833` | `51,647` | `-186` |
| 11 | `m26` | `28,399` | `28,233` | `-166` |
| 12 | `i29` | `15,522` | `15,375` | `-147` |
| 13 | `m20` | `16,580` | `16,454` | `-126` |
| 14 | `i25` | `17,843` | `17,745` | `-98` |
| 15 | `i26` | `44,983` | `44,897` | `-86` |
| 16 | `i15` | `11,229` | `11,161` | `-68` |
| 17 | `i20` | `16,743` | `16,695` | `-48` |
| 18 | `i07` | `8,452` | `8,408` | `-44` |
| 19 | `m24` | `13,864` | `13,820` | `-44` |
| 20 | `m28` | `38,487` | `38,448` | `-39` |
| 21 | `m06` | `8,548` | `8,510` | `-38` |
| 22 | `m12` | `20,031` | `19,998` | `-33` |
| 23 | `i19` | `31,206` | `31,175` | `-31` |
| 24 | `m13` | `24,066` | `24,043` | `-23` |
| 25 | `m17` | `36,246` | `36,227` | `-19` |
| 26 | `i22` | `31,734` | `31,720` | `-14` |
| 27 | `m05` | `2,938` | `2,925` | `-13` |
| 28 | `m18` | `20,860` | `20,848` | `-12` |
| 29 | `m02` | `2,704` | `2,700` | `-4` |
| 30 | `i09` | `8,539` | `8,536` | `-3` |
| 31 | `i16` | `15,436` | `15,435` | `-1` |

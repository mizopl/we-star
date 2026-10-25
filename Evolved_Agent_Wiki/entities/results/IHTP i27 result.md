---
title: "IHTP i27 result"
category: "entity"
created: "2026-10-18"
updated: "2026-10-18"
sources:
  - "~/v3r1t4s/runs/2026-10-18-1607/claim/sol_i27.json"
  - "~/v3r1t4s/runs/2026-10-18-1607/panel/gate.md"
  - "~/v3r1t4s/outbox/2026-10-18-mizopl-900443ab/README.md"
tags: ["v3r1t4s", "optimization-benchmarks", "ihtc2024", "ihtp", "seam-surgery", "confirmed-solution"]
---

# IHTP `i27` Result (`50,976 -> 50,063`, `-913`, `CONFIRMED_SOLUTION`)

## Summary

Explicit feasible schedule `sol_i27.json` (`209,120` bytes, `sha256: 900443ab5205ab28d6ad4713b0023593f931007812ecf0e3410a4e49e1006cf7`) for the Integrated Healthcare Timetabling Competition 2024 (IHTC-2024) benchmark instance `i27` (`28` days, `84` shifts, `26` rooms, `8` operating theaters, `8` surgeons, `55` nurses, `41` occupants, `493` patients), verified by both the official C++ competition validator `IHTP_Validator.cc` and standalone pure-Python checker `author_checker_ihtp_check.py` with:
- **`Total violations = 0`** across all 9 hard constraint families (`RoomGenderMix` through `UncoveredRoom`)
- **`Total cost = 50,063`**, strictly improving on the live `ihtc2024.github.io` record of **`50,976`** (Kletzander, Mischek & Musliu) by **`913` points (`-1.791%`)** and on pending V3R1T4S PR `#359` (`50,125`) by **`62` points**.

## Soft-Constraint Cost Breakdown (`i27`)

| Component | Weight | Previous Best (`50,976`) | New Solution (`50,063`) | Delta |
|---|---:|---:|---:|---:|
| `RoomAgeMix` | 1 | 298 | 298 | 0 |
| `RoomSkillLevel` | 10 | 3,930 | 3,610 | **-320** |
| `ContinuityOfCare` | 1 | 3,518 | 3,045 | **-473** |
| `ExcessiveNurseWorkload` | 10 | 740 | 620 | **-120** |
| `OpenOperatingTheater` | 30 | 3,210 | 3,210 | 0 |
| `SurgeonTransfer` | 10 | 290 | 290 | 0 |
| `PatientDelay` | 5 | 16,490 | 16,490 | 0 |
| `ElectiveUnscheduledPatients` | 500 | 22,500 | 22,500 | 0 |
| **Total NRA Soft Cost** | — | **8,188** | **7,275** | **-913 (-11.005%)** |
| **Total Cost** | — | **50,976** | **50,063** | **-913 (-1.791%)** |

## Method: CLSS Patient-Stay Nurse Consolidation + 6-Nurse Subset MILP Polish

1. **Compound Patient-Stay Nurse Consolidation (`seam_surgery_ihtp.cc`):** Crosses the $k \ge 2$ `ContinuityOfCare` barrier by replacing or swapping a dropped nurse $n_{\text{drop}} \to n_{\text{keep}}$ across *all shifts of a patient's stay simultaneously*, combined with $O(1)$ (`~10 ns`) incremental Simulated Annealing (`50,976 -> 50,078` in single `2.5s` pass, `50,068` after multi-seed SA).
2. **Exact 6-Nurse Subset MILP Polish (`subset_nra_milp.py`):** Solves exact MILPs (`scipy.optimize.milp` / HiGHS) over random 6-nurse subsets across all 84 shifts followed by deterministic `GreedyPolishNRA`, reaching `50,063`.
3. **Packaged in:** `~/v3r1t4s/outbox/2026-10-18-mizopl-900443ab/`.

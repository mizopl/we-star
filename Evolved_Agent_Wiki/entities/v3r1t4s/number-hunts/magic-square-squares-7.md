---
id: v3r1t4s-magic-square-squares-7
type: entity
tags: [v3r1t4s, v3r1t4s/number-hunts, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: number-hunts
kind: standard
tractability: 1
compute: "laptop-hours"
disclosure: commit-only
status_checked: "2026-10-03"
---
# 3x3 magic square with >= 7 square entries (second example) or nine squares

# Overview

> Bank id `magic-square-squares-7` · standard · tractability 1 · laptop-hours · disclosure **commit-only**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Does a 3x3 magic square of nine distinct perfect squares exist? Only one fully magic 3x3 square of distinct positive integers with 7 square entries is known: Bremner (1999), \[\[373^2,289^2,565^2],[360721,425^2,23^2],[205^2,527^2,222121\]\] with magic sum 541875. (Sallows' 1997 8-square square has a failing diagonal and is not fully magic.) Christian Boyer offers prizes for a second 7-square example or for a 9-square example. Rome-Yamagishi (2024) settled all n >= 4. Searches: Buell (center up to 25e24), Boyer (~2.5e27); Wikipedia: any solution has entries > 10^14. A Sept 2026 GitHub project (Kepler71) handled 11 sections by 2-descent/Chabauty, left the (11,4) and (15,8) parameter pairs unresolved, and states the problem is not solved.

## Success criterion

CONFIRMED if the agent gives a 3x3 matrix of nine distinct positive integers with all 8 line sums equal (exact integer arithmetic), and either (a) at least 7 entries are perfect squares (math.isqrt) and the square is NOT equivalent to Bremner's square \[\[373^2,289^2,565^2],[360721,425^2,23^2],[205^2,527^2,222121\]\] (magic sum 541875), nor to any other 7-square fully magic square listed on https://en.wikipedia.org/wiki/Magic_square_of_squares or Boyer's prize pages at verification time; equivalence is tested under the 8 dihedral symmetries after dividing by the largest square common factor; or (b) all 9 entries are distinct squares (prize-level). Semi-magic squares, repeated entries, and zero or negative entries never count.

## Partial wins

- {"id": "p1", "statement": "Kepler71 open sections: a complete, machine-reproducible determination (rank and generators with a PARI/Magma-checkable certificate, plus descent or Chabauty output) of the rational points relevant to 7-square squares on the (11,4) or (15,8) section that the Kepler71 repo left unresolved, ending either in a new 7-square square or in a proof that the section yields none beyond known ones."}
- {"id": "p2", "statement": "New placement pattern: a machine-reproducible proof that an explicit infinite family/section for a 7-of-9 placement pattern not treated in Kepler71's 11 sections or Bremner's work contains no fully magic 7-square square (or exhibits one), with all rank/descent computations rerunnable by the verifier."}

## Verification

Exact integer check of the 8 line sums, distinctness, positivity and isqrt squareness. Normalize by the square part of the gcd and compare all 8 symmetries against the hard-coded Bremner square (already verified magic with sum 541875). For partial wins, rerun the rank/descent computations in PARI (cypari2) or Magma from the stated curve equations and check that the section matches the Kepler71 parametrization.

## Angles

- Use the parametrization: a 3x3 magic square with center e has entries e ± x, e ± y, e ± (x+y), e ± (x-y). With squares, this is a system of arithmetic progressions of three squares (congruent-number curves). Search for 7-square configurations as rational points on a specific genus-1 fibration, using point addition on each fiber instead of brute force.
- Avoid the 11 sections already treated in the Kepler71 repo; the (11,4) and (15,8) parameter pairs are the unresolved ones. Target the other 7-of-9 placement patterns (which two cells are non-square) and compute ranks of the corresponding elliptic fibers with pari (pip cypari2) to find rank ≥ 1 fibers with small-height points.
- Use Bremner's original method (rational points on a quartic surface) to generate infinitely many 7-square candidates in a family, then check distinctness/positivity. Most 'new' finds are scalings, so normalize aggressively.
- Use a modular sieve over center values with residue-class precomputation (mod 2^k, 3, 5, 7, 13) to prune 9-square configurations, as a sanity-limited search, not a frontier push.

## Pitfalls

- Scalings or symmetries of the known Bremner/Sallows square count as the same square.
- Semi-magic (diagonals failing) or repeated entries (Parker Square) do not count.
- Negative or zero entries do not count.
- Floating-point square tests.
- Sallows' 1997 square has a failing diagonal and is NOT the 7-square magic square. Only Bremner's is fully magic.
- Kepler71 handled 11 sections. The (11,4) and (15,8) parameter pairs were left unresolved there, and those are the only sections with a fresh angle.

## Sources

- https://en.wikipedia.org/wiki/Magic_square_of_squares
- https://github.com/Kepler71/magic-square-of-squares
- https://arxiv.org/abs/2406.09364
- Status source: https://en.wikipedia.org/wiki/Magic_square_of_squares

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/number-hunts/magic-square-squares-7.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `magic-square-squares-7`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Number hunts]]
- [[V3R1T4S]]

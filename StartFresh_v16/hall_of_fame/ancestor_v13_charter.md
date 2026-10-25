# Research charter v3 (2026-10-18)

## Thesis
Seeds were random (categories drug-discovery and number-hunts; method cards far-import, small-data, smaller-first), with one exception: the human made the exact-count lattice-gas problem the first quarry. The edge here is patience plus exactness. One 10-core laptop, every night, pushing exact integer computations whose answers a stranger can check by residues in minutes, and keeping a written graph of every dead line so no night repeats another.

## Quarries
1. **square-grid-lattice-gas-exact-counts-oeis**. Question: the first unknown exact term of A006506 / A063443 / A028420 (main), or of A054759 / A027683 (partial p1). Shape: exact integer by transfer matrix plus CRT. Defined in: bank entry of that id (OEIS A006506, A063443, A028420, A054759, A027683). Status to confirm first: the current b-file maxima. Why us: modest memory, many nights, independent second decomposition. Weight 5. Wild: no.
2. **bb6-holdout-certificates**. Question: decide an official BB(6) holdout machine with a checkable certificate. Shape: bound or proof. Defined in: bank entry of that id. Status to confirm first: the bbchallenge holdout list. Why us: small-data simulation of many tiny cases before the lift. Weight 3. Wild: no.
3. **polaris-moleculeace-activity-cliff-mse**. Question: beat the single listed MSE on a MoleculeACE leaderboard. Shape: record on a public benchmark. Defined in: bank entry of that id. Status to confirm first: the live leaderboard values. Why us: far-import of exact-counting ideas (graph substructure counts) as features. Weight 2. Wild: no.
4. **mahler-measure-new-small-polynomials**. Question: new small-Mahler-measure polynomials outside the proven-complete ranges. Shape: record or existence. Defined in: bank entry of that id. Status to confirm first: Mossinghoff's lists. Why us: structured-family search is cheap and complete. Weight 2. Wild: no.
7. **bouchaudy-typex-1**. Question: decrypt J.-F. Bouchaudy's Cipher Machines Challenge TypeX Problem 1 and be the first solver listed on the setter's table. Shape: decipherment under a provided key table, so the work is a faithful simulator. Defined in: http://www.jfbouch.fr/crypto/challenges/TYPEX/index.html (problem page pro_1_typex.html and notes.txt; the solver table is the status source). Disclosure: **commit-only** (living setter; everything spoiler-relevant goes in private/bouchaudy-typex-1/; the human emails the setter). Status to confirm first: the solver table still shows 0 solvers for Problem 1. Why us: the setter says the only obstacle is building a correct TypeX simulator from the text, which is careful specification reading, and solved sibling Problem 2 can validate the simulator first. Weight 5. Wild: no.
6. **covering-designs-record** — question: a (v,k,t) covering design with strictly fewer blocks than every live table (LJCR dmgordon.org, coveringrepository.com, dmgordo/LJCR GitHub and Zenodo snapshots); shape: record, explicit object; defined in: bank entry covering-designs-record (La Jolla Covering Repository); status to confirm first: the live LJCR cell and coveringrepository.com (if unreachable: PENDING TABLE CHECK, never a claim); why us: a tiny-RAM exhaustive t-subset checker and patient annealing seeded from published designs in weakly optimised cells (large v, simple constructions), while p2 compute holds the RAM; weight 2 (lowered in v3: coveringrepository.com shows 100 improvements in 10 days, so the table is crowded); wild: no.
5. **pte-ideal-size-11-13**. Question: an ideal Prouhet–Tarry–Escott solution of size 11 or 13. Shape: existence. Defined in: bank entry of that id. Status to confirm first: the known ideal sizes. Why us: an obstruction-first sieve run for months. Weight 1. Wild: yes.

## Lenses
- **extender**: Take the published transfer-matrix approach and push it one index further, modulo several 62-bit primes. First moves: reproduce every published term, then fix the CRT bound from the entropy constant. Dead sign: memory over 12 GB or more than 8 h per prime. Skeptic: no.
- **far-import**: Bring in a method from a distant field (tensor-network contraction order, FFT reflection symmetry, Freivalds residue checks) and make it do real work. Dead sign: no speed or independence gain on n ≤ 20. Skeptic: no.
- **small-data**: Compute many small cases exactly (rectangular m×n tables), look for structure, and use it to halve states or cross-check. Dead sign: no pattern after 30 min of tabulation. Skeptic: no.
- **smaller-first**: Solve the easiest neighbouring sequence (torus ice A054759) completely, then lift the code. Dead sign: the code fails to reproduce the published small terms. Skeptic: no.
- **settled-check**: Try to show the quarry is already settled (newer b-file, arXiv, OEIS history, GitHub) or ill-posed (offset, convention). Dead sign: none, this lens always reports. Skeptic: yes.

## Scout voice
Read the b-file before the prose. Trust only the index and value you fetched, and note the offset.

## Attacker voice
Patient and exact. Prefer the plain method at a scale nobody bothered with over a clever one you cannot verify.

## Heuristics
- Reproduce all published terms before computing a new one.
- CRT modulus product must exceed the entropy-constant bound by at least 2^64.
- Two runs must differ in both primes and decomposition.
- Run `rgraph check` before every new line. A dead near-duplicate needs a new reason.
- Checkpoint every 5 min. Store large arrays memory-mapped in the run folder, staying under 6 GB of disk.

## Kill criteria
- Cannot reproduce published terms after 2 fixes.
- Projected time per prime exceeds 2 nights.
- The term was published since the bank snapshot.
- Disk needed exceeds 6 GB, given the machine has about 15 GB free.

## Self-critique
Most likely self-deception: treating agreement between two runs that share a bug (same frontier encoding) as independence, or miscounting the offset. Also exact counts may be less neglected than they look, since several people extend these b-files.

## Method cards used
far-import, small-data, smaller-first (random draw).

## Changelog
- v3 (2026-10-18): the human asked for cipher problems. A 22-page one-GET scout of Bouchaudy's challenge found 0-solver problems. A tug gate on TypeX #1 deadlocked (every turn refused by the API safety filter, X7), so per §13.3 the BRAIN index (commander) decided: quarry 7 bouchaudy-typex-1, weight 5, commit-only. Covering-designs weight 4 → 2 (crowding evidence from run 2328).
- v2 (2026-10-18): added quarry 6, covering-designs-record (weight 4). It was chosen by VS (seed 1825729363) over 126 bank candidates and confirmed by a tug-of-war gate in which IMPLEMENT won by concession (proofer/tug/2026-10-18-second-front). The human asked for a second problem from a different domain. Quarry 1's live lead p2 is now **parked in the compute job queue** (jobs ad79-*). Runs harvest it when its jobs finish, so it does not block runs from taking the next quarry.

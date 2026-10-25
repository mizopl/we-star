---
id: v3r1t4s-posebusters-redock-pb-valid-rate
type: entity
tags: [v3r1t4s, v3r1t4s/drug-discovery, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: drug-discovery
kind: harvest
tractability: 2.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# PoseBusters benchmark set (428 complexes): raise the PB-valid RMSD<=2A redocking rate above the published classical-docking rate

# Overview

> Bank id `posebusters-redock-pb-valid-rate` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

PoseBusters (Buttenschoen, Morris & Deane, Chem. Sci. 2024) is the standard physics-aware pose-validity benchmark: 428 carefully selected protein-ligand crystal complexes released since 2021, with an open-source scorer (the posebusters pip package / github.com/maabuu/posebusters) that checks chemical validity, intramolecular geometry, intermolecular clashes and RMSD to the crystal pose, and the headline metric is the fraction of predictions that are both RMSD<=2A and 'PB-valid'. The paper's finding - that classical docking (AutoDock Vina) beats deep-learning co-folding and pose-prediction methods on PB-valid rate - makes this an unusual benchmark where CPU docking is the method to beat, not a handicap. Polaris mirrors the set as polaris/posebusters-v1 (428 test systems, main metric rmsd_coverage) and that leaderboard currently lists NO results, while the related plinder-org/runs-n-poses preview table shows how weak the co-folding field is on a harder split (AlphaFold3 15.1% success, Boltz-1 5.6%, Chai-1 4.7%, Protenix 1.5%). The data are public (Zenodo record 8278563, 200 OK) and the Polaris dataset parquet/zarr download anonymously, so a laptop can redock all 428 systems with open-source docking in hours and score with the official package.

## Success criterion

Success means a saved set of predicted ligand poses (one SDF per complex for all 428 PoseBusters systems, plus the receptor files used and a manifest with the sha256 of every input structure, the exact method, software versions, seeds and total wall-clock CPU time) such that (a) the skeptic, running the official posebusters package (version pinned in the manifest) with the standard redock configuration on the attacker's SDFs against the crystal ligands from the public PoseBusters distribution, obtains a PB-valid RMSD<=2A rate that is strictly HIGHER (direction: max) than BOTH (i) every entry listed in the live leaderboard table at https://polarishub.io/benchmarks/polaris/posebusters-v1 , re-fetched immediately before claiming - a first entry on an empty table is explicitly NOT a record - and (ii) the attacker's OWN reproduction, with the same inputs and the same scorer, of a documented classical docking baseline (e.g. AutoDock Vina with a declared box and exhaustiveness), reported with its rate, and (iii) the best PB-valid RMSD<=2A rate for the same 428-system benchmark reported in the PoseBusters paper and in any paper found by the NOVELTY skeptic from the last 24 months, (b) the margin over (ii) and (iii) is at least 3 percentage points and a paired bootstrap over the 428 complexes (10,000 resamples) confirms superiority in at least 95% of resamples, (c) no crystal ligand pose, crystal-ligand coordinates, or ligand-pose-derived restraint for a test complex was used as input - only the receptor structure (holo or declared apo), the ligand's 2D/SMILES identity, and the binding-site definition rule, which must be stated and applied uniformly (e.g. derived from a non-test cognate ligand or from a pocket-detection algorithm, never from the test ligand's own coordinates), and (d) the pose files, the run script and the posebusters output table are published so the whole rate can be recomputed from scratch.

## Partial wins

- {"id": "p1", "statement": "A reproduction artefact: the attacker's own end-to-end harness (download, prepare, dock, score with the official posebusters package) reproducing a published classical-docking PB-valid rate on all 428 systems to within 2 percentage points, with runtime reported - valuable infrastructure, reported as a reproduction and not a record."}
- {"id": "p2", "statement": "A subset result: a strictly higher PB-valid RMSD<=2A rate than the attacker's own reproduced baseline (same inputs, same scorer, margin >= 5 percentage points, bootstrap-confirmed) on a declared, pre-registered subset of at least 150 complexes selected by a rule that does not use the crystal pose (e.g. ligand heavy-atom count below a threshold, or single-chain receptors)."}
- {"id": "p3", "statement": "A failure-mode map: a per-complex table showing, for the attacker's method and its reproduced baseline, which posebusters checks fail (clash, internal geometry, stereochemistry, RMSD) with counts, identifying at least one systematic, fixable failure class and demonstrating the fix raises the overall rate - independently checkable from the published pose files."}

## Verification

Skeptic downloads the PoseBusters benchmark set from its public distribution (Zenodo record 8278563 / the posebusters repo), checks input sha256s against the manifest, installs the pinned posebusters package, runs the official 'redock' mode on the attacker's 428 SDFs against the crystal ligands, and reads the PB-valid and RMSD<=2A columns to recompute the rate; repeats the same scoring on the attacker's reproduced baseline poses; runs the paired bootstrap; verifies from the run script that no test-complex crystal ligand coordinates entered pose generation or box definition; and re-fetches the live Polaris leaderboard table. Scoring 428 poses takes minutes; re-docking 428 complexes on 10 CPU cores is hours.

## Angles

- Do classical docking properly: exhaustive sampling budgets, multiple independent runs per complex with different seeds, careful protonation/tautomer enumeration of the ligand, receptor protonation and metal/cofactor handling, and consensus pose selection across runs - the PoseBusters paper's own message is that disciplined Vina beats learned methods, and most of the remaining failures are preparation failures.
- Consensus re-scoring: generate many poses with one engine and re-rank with an ensemble of independent scoring functions plus a posebusters-style validity prefilter, selecting the top pose that is both well-scored and physically valid; selecting for validity before RMSD is exactly what the PB-valid metric rewards.
- CROSS-DOMAIN (signal processing / matched filtering on grids): precompute receptor interaction-field grids and match ligand pharmacophore 'templates' by cross-correlation (FFT-based docking, as used in protein-protein docking) to seed local optimisation, giving broader coverage of the pocket per CPU second than stochastic search alone.
- CROSS-DOMAIN (combinatorial search / cryptanalytic restart strategies): treat torsion angles and rigid-body placement as a discrete-continuous key and run tabu-guided simulated annealing with many short restarts and an elite archive instead of one long stochastic run - a better use of a fixed CPU budget.
- CROSS-DOMAIN (statistical physics / replica exchange): parallel-tempered pose sampling across temperatures to cross torsional barriers that single-temperature Monte Carlo misses, then quench the best replicas.
- CROSS-DOMAIN (coding theory / covering codes): place starting conformers so that they form a covering code over the pocket's rigid-body and torsional space, guaranteeing a bounded distance from any true pose rather than relying on random initialisation.
- Template transfer from non-test structures: for each test receptor, find homologous holo structures NOT in the benchmark and transfer their cognate ligand's binding-mode restraints (shape overlap), which is legitimate as long as no test complex's own crystal pose is used - and must be declared explicitly.

## Pitfalls

- Empty-leaderboard false win: polaris/posebusters-v1 lists no results, so a first submission is NOT a record. The operative bar is the published rate plus the attacker's own reproduced baseline, and this must be stated in any claim.
- Crystal-pose leakage, the signature failure of this field: defining the docking box, the pocket centre, the ligand conformer, or any restraint from the test complex's own crystal ligand inflates success enormously. The box/pocket rule must be uniform, pose-independent and published, and the skeptic must check the run script for it.
- Holo-receptor and preparation leakage: using the holo receptor is standard for redocking but must be declared, as must any use of the deposited ligand's protonation/tautomer state; silently taking the crystal ligand's exact protomer is a subtle form of leakage.
- Scorer drift: posebusters versions, modes (redock vs dock vs mol) and RMSD conventions (symmetry-corrected or not, heavy atoms only) change the rate by several points. The package version and mode must be pinned in the manifest and re-run by the skeptic, not taken from the attacker's output.
- Subset substitution: quietly dropping complexes that fail preparation, or scoring on fewer than all 428 systems, inflates the rate. The denominator must be all 428 systems, with failures counted as failures, unless a pre-registered subset partial win is being claimed.
- Benchmark-set contamination for learned components: any learned scoring or pose-prediction component trained on PDB structures released after 2021 may have seen these very complexes; provenance and training cutoffs must be declared, which is also how the PoseBusters paper frames its own fairness analysis.

## Sources

- https://polarishub.io/benchmarks/polaris/posebusters-v1
- https://github.com/maabuu/posebusters
- https://posebusters.readthedocs.io/en/latest/
- https://zenodo.org/records/8278563
- https://polarishub.io/benchmarks/plinder-org/runs-n-poses
- Status source: https://polarishub.io/benchmarks/polaris/posebusters-v1

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/drug-discovery/posebusters-redock-pb-valid-rate.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `posebusters-redock-pb-valid-rate`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Drug discovery]]
- [[V3R1T4S]]

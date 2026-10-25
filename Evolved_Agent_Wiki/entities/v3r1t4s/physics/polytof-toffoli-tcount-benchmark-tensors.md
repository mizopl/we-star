---
id: v3r1t4s-polytof-toffoli-tcount-benchmark-tensors
type: entity
tags: [v3r1t4s, v3r1t4s/physics, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: physics
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Toffoli-count and T-count records: fewer non-Clifford gates for a benchmark circuit tensor than the Khoruzhii-Gelss-Pokutta (polytof) table

# Overview

> Bank id `polytof-toffoli-tcount-benchmark-tensors` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

For a quantum circuit over {CNOT, Toffoli/CCZ, H}, the non-Clifford part can be gathered into one diagonal phase operator given by a cubic phase polynomial over F_2, stored as a symmetric 3-tensor. Its CP rank (up to quadratic and linear terms) is the Toffoli/CCZ count and its Waring rank is the T-count (Amy and Mosca; Heyfron and Campbell). AlphaTensor-Quantum (Ruiz, Laakkonen, Bausch, ..., van de Wetering, Fawzi, Meichanetzidis, Kohli; Nature Machine Intelligence 2025) set T-count records on a standard suite of arithmetic benchmarks with large TPU budgets. Kirill Khoruzhii, Patrick Gelss and Sebastian Pokutta (arXiv:2602.15285, Feb 2026) then matched or beat every reported Toffoli and T-count with CPU-minute algebraic methods (basis-change optimisation, symplectic Gaussian elimination, flip-graph search, FastTODD) and keep a public table of best known CP rank and Waring rank per tensor in their repository (docs/tensors.md, last commit 2026-10-12). Examples on 2026-10-15: Barenco Tof_10 (n=50) CP 16 / T-count 83; Mod Adder_1024 (n=332) CP 128 / T 573; Ham15 (high) (n=351) CP 155 / T 643; QCLA Mod_7 (n=84) CP 37 / T 153; GF(2^10) multiplication CP 33 / T 173; Hamming-weight n=20 CP 18 / T 109; Unary iteration n=5 CP 31 / T 127. The tensors (.npy) and the decompositions behind each number ship with the repository, so a lower count is an exactly checkable object. Large tensors (n > 60) and the newest families (AES S-box circuits added 2026-10-12) have seen the least search.

## Success criterion

Success means, for some tensor ID listed in the live polytof table (https://github.com/ZIB-IOL/polytof/blob/main/docs/tensors.md, re-fetched live immediately before claiming), an explicit decomposition with STRICTLY FEWER terms (direction: min, margin >= 1 term) than the listed CP value (Toffoli count) or the listed Waring value (T-count) for that tensor ID, such that: (a) for CP, the list of r triples of binary vectors (u_t, v_t, w_t) reproduces the tensor's cubic monomials x_i x_j x_k (i<j<k) exactly over F_2 after symmetrisation, with only quadratic and linear differences allowed, as checked by an independent script AND by polytof's scripts/verify_paper_schemes.py; for Waring, the r binary vectors a_t reproduce the full signature (phase polynomial) of that tensor variant exactly in the convention polytof and AlphaTensor-Quantum use; (b) the same tensor variant (01xx vs 08xx vs 07xx) is used as the table row; (c) for at least one claimed circuit the decomposition is turned back into a CNOT + Toffoli/T circuit and checked exactly equal (up to global phase) to the original benchmark circuit by a path-sum or statevector equivalence check; and (d) an arXiv search finds no lower published count for that circuit (including Mazumder arXiv:2610.01024 lower bounds, which may prove the table value optimal).

## Partial wins

- {"id": "p1", "statement": "A strictly lower Toffoli (CP) count than the live table for some GF(2^k) multiplication tensor (07xx/05xx, k = 2..10) or AES S-box circuit tensor, with the same exact check; note that for the base 05xx tensors this equals a new upper bound on the bilinear complexity of GF(2^k) multiplication, which must also be checked against the classical literature on that problem."}
- {"id": "p2", "statement": "A certified optimality proof for a table row whose optimality is not already published: an exhaustive or SAT/DRAT certificate that no decomposition with (table value - 1) terms exists for that tensor variant, re-checkable in under an hour."}
- {"id": "p3", "statement": "An independent re-verification audit of all decompositions in data/paper/ that reports any table value not reproduced by its posted decomposition."}

## Verification

Clone https://github.com/ZIB-IOL/polytof (tensors in data/tensors/*.npy: row 0 = dims, rows 1.. = nonzero (i,j,k) with i<j<k). Independent checker in numpy uint8: build the cubic monomial set of the target; for a CP claim expand sum_t sym(u_t (x) v_t (x) w_t) mod 2 and compare the i<j<k part exactly; for a Waring claim compute sum_t a_t (x) a_t (x) a_t mod 2 over all index patterns used by the repository's own Waring check and compare. Run scripts/verify_paper_schemes.py style verification on the new scheme. For circuit-level confirmation (n <= ~30 qubits), synthesise the phase operator from the decomposition, conjugate by the recorded Clifford/basis-change, and compare to the original .qc/.qasm with a path-sum checker (e.g. Feynman's feynver) or exact statevector on random basis inputs plus a symbolic check. Re-fetch tensors.md and compare the count.

## Angles

- Flip-graph search (the method behind recent matrix-multiplication rank records) is already in polytof; push it on the biggest tensors (Mod Adder_1024, Ham15 high, Grover_5, Adder_8) with long runs and plateau moves, since the paper's runs were budgeted in CPU-minutes.
- Basis change first: the CP rank is invariant under GL(n,F_2) but search difficulty depends on nnz; anneal over CNOT basis changes to minimise nnz or tensor slice ranks before decomposition.
- Import from coding theory: T-count reduction is Reed-Muller decoding (punctured RM(n-4, n)*); use list decoders and information-set decoding from classical decoding literature on the signature, as in TODD's lineage.
- Import from algebraic complexity: GF(2^k) multiplication tensors are bilinear maps whose rank has been studied via Chudnovsky-type interpolation on curves; use those constructions to seed 05xx/07xx searches.
- Import from SAT: for small tensors (n <= 20) encode 'rank <= r' as SAT with symmetry breaking and either find a lower decomposition or produce a DRAT proof (partial win p2).

## Pitfalls

- Toffoli count (CP rank) and T-count (Waring rank) are different columns; beating one does not beat the other, and gadget-based counts (ATQ 'gadgets' files) are a different accounting.
- Tensor variants differ: 01xx (from AlphaTensor-Quantum) and 08xx (compiled from Vandaele's circuits) can have different n and nnz for the 'same' circuit, and 05xx/03xx/07xx are different representations of GF(2^k) multiplication. Compare only within the same tensor ID.
- CP equality is required only modulo quadratic and linear terms; a checker that demands exact equality of all entries will wrongly reject valid schemes, and one that ignores the cubic diagonal-pattern conventions will wrongly accept invalid ones. Use the repository's verification as a second opinion.
- Some rows may already be optimal: Mazumder (arXiv:2610.01024, Oct 2026) gives an isotropy lower bound certifying many phase-polynomial blocks T-optimal; check it before spending compute.
- The table moves (last commit 2026-10-12); a value beaten in a stale clone may already be updated upstream.

## Sources

- https://github.com/ZIB-IOL/polytof
- https://github.com/ZIB-IOL/polytof/blob/main/docs/tensors.md
- https://arxiv.org/abs/2602.15285
- https://arxiv.org/abs/2402.14396
- https://github.com/google-deepmind/alphatensor_quantum
- https://github.com/tlaakkonen/circuit-to-tensor
- https://arxiv.org/abs/2610.01024
- Status source: https://github.com/ZIB-IOL/polytof/blob/main/docs/tensors.md

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/polytof-toffoli-tcount-benchmark-tensors.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `polytof-toffoli-tcount-benchmark-tensors`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]

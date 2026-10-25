---
id: v3r1t4s-erdos-699-binomial-gcd
type: entity
tags: [v3r1t4s, v3r1t4s/erdos-and-proofs, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: erdos-and-proofs
kind: harvest
tractability: 2
compute: "laptop-hours (proof work plus exhaustive residual check)"
disclosure: open
status_checked: "2026-10-03"
---
# Erdos #699: a prime p >= i dividing gcd(C(n,i), C(n,j)), for a full proof

# Overview

> Bank id `erdos-699-binomial-gcd` · harvest · tractability 2 · laptop-hours (proof work plus exhaustive residual check) · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

For every n and every 1 <= i < j <= n/2, is there a prime p >= i dividing gcd(C(n,i), C(n,j))? Erdos-Szekeres 1978. FALSIFIABLE/OPEN. Proved for j <= 3i/2 or n=2j (GPT 5.6 via L. Price, Jul 2026). Del Pin (2026-07-25) extends the range slightly past floor(3i/2). MaxDKaos (2026-07-25) gives j <= C i log^2 i unconditionally. Exhaustively checked for n <= 10^7 (Cong, 2026-01-06), with targeted extensions to about 1.34e8. No full proof is claimed. Only finitely many n are possible for each fixed (i,j). Bloom highlighted the identity C(n,i)C(n-i,j-i) = C(n,j)C(j,i) and calls the problem possibly very deep in general.

## Success criterion

(A) An explicit counterexample (n,i,j), 1<=i<j<=n/2, with no prime p>=i dividing both C(n,i) and C(n,j), verified by Kummer valuations and by direct factorisation. (B) A complete proof for all (n,i,j): every step elementary or citing a theorem with its exact published statement, any finite residual range closed by reproducible exhaustive code. The forum's partial cases (j <= 3i/2, n = 2j, Del Pin's interval, j <= C i log^2 i) may be used only after the verifier re-proves or checks them.

## Partial wins

- {"id": "p1", "statement": "A rigorous, refereed proof covering a new infinite region strictly beyond j <= C i log^2 i (e.g. all j <= i^{1+delta} for an explicit delta > 0)."}
- {"id": "p2", "statement": "A rigorous proof of the statement for ALL (n, j) whenever i <= B, for an explicit bound B larger than any i-range already settled on the forum, with any finite residue closed by reproducible code."}
- {"id": "p3", "statement": "An exhaustive verification for all n <= 10^9 and all valid pairs (i,j), beyond Cong's n <= 10^7 and the targeted ~1.34e8 checks, reproduced by an independent implementation (e.g. Lucas-theorem bitsets versus direct gcd factorisation on a random sample of n plus full Kummer scan)."}

## Verification

(A) For every prime p in [i, n], compute v_p(C(n,i)) and v_p(C(n,j)) by Kummer (count carries of i + (n-i) in base p), and confirm that no prime has both valuations positive. Cross-check with sympy.factorint on the gcd for moderate n. (B) Line-by-line refereeing. Rerun the residual computation with independent code (e.g., a Lucas-theorem bitset method versus direct gcd factorisation). Check edge cases i = 1, 2 and the p >= i versus p > i distinction.

## Angles

- Combine the identity C(n,i)C(n-i,j-i) = C(n,j)C(j,i) with Kummer carries. A prime p > j dividing C(n,i) must divide C(n,j) unless it is absorbed by C(n-i,j-i). Split into cases on the base-p digit pattern of n.
- Use Sylvester-Schur strengthenings (a prime > c*i divides C(n,i) for n >= 2i, Ecklund-Eggleton-Erdos-Selfridge style) to push past the j ~ 1.5i magnitude ceiling that Del Pin identified.
- Make MaxDKaos's bound n <= j^{i/(i-pi(i-1))} uniform in i via explicit prime-counting (Dusart bounds), reducing to a finite region. Close that region with a fast exhaustive search: for each n, bitsets D_p(n) = {i : p | C(n,i)} from Lucas' theorem, and for each i the union over p >= i.
- Hunt counterexamples near the known exceptions of the stronger p > i variant, e.g. (28,5,14), and among n that are prime powers, or prime powers plus or minus 1, which minimise carries.
- Make Del Pin's interval endpoint J_1(i) explicit and attempt to bridge it to MaxDKaos's C i log^2 i range.

## Pitfalls

- The p >= i and p > i versions differ: the stronger version has genuine exceptions such as gcd(C(28,5), C(28,14)) = 2^3*3^3*5.
- Checking special families of n is not a proof.
- Forum AI proofs need independent re-checking.
- Off-by-one errors in j <= n/2.
- Exhaustive range claims below 10^7 duplicate Cong (forum 2026-01-06).
- Del Pin's interval result already extends 3i/2 slightly; re-proving it is not new.

## Sources

- https://www.erdosproblems.com/699
- https://www.erdosproblems.com/forum/thread/699
- https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/699.lean
- Status source: https://www.erdosproblems.com/699

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/erdos-and-proofs/erdos-699-binomial-gcd.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `erdos-699-binomial-gcd`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Erdős problems and proofs]]
- [[V3R1T4S]]

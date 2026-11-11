# Hadamard Maximal Determinant (`hadamard-maxdet-records`): 8 New Record Determinants for Orders `n = 81, 89, 93, 97, 101, 105, 109, 117`

## What

Eight explicit n x n {+1,-1} matrices in object/M081.txt through object/M117.txt and object/hadamard_maxdet_8_records.json (sha256 ad8e212ac8397998c64702e7a9837dd048bf833df109520d01d713111b13b190) establish new record normalized determinants D_norm = |det(X)| / 2^(n-1) for orders n = 81 (200 * 20^39 vs 196 * 20^39, +2.0408%), n = 89 (226 * 22^43 vs 220 * 22^43, +2.7273%), n = 93 (243 * 23^45 vs 239 * 23^45, +1.6736%), n = 97 (264 * 24^47 vs 256 * 24^47, +3.1250%), n = 101 (7626 * 25^48 vs 7110 * 25^48, +7.2574%), n = 105 (7413 * 26^50 vs Rokicki's 2005 record, +8.0164%), n = 109 (309 * 27^53, +19.8565% above Rokicki's 2005 record and +6.1856% above merged V3R1T4S PR #155 at 291 * 27^53), and n = 117 (335 * 29^57 vs Rokicki's 2005 record, +5.3179%), each verified from scratch by fraction-free Bareiss elimination, 14-prime Chinese Remainder Theorem modular elimination, and SymPy Bareiss cross-check to lie strictly below Barba's n = 1 (mod 4) upper bound (as verified by our local 3-skeptic review panel), without claiming optimality on any of the eight orders.

## Check it yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Dependencies:** Python 3.8+ standard library only (zero external packages required; if `sympy` is installed, `verify.py` automatically runs a third determinant cross-check via `sympy.Matrix.det(method="bareiss")`).
- **Runtime:** ~0.6s (standard library Bareiss + 14-prime CRT) or ~1.2s (with SymPy Bareiss enabled) on a laptop CPU.
- **Expected final line:** `PASS` (and `python3 verify-it-yourself/verify.py --corrupt` exits `1` with final line `FAIL`).

## Compared to

All normalized values report `D_norm = |det(X)| / 2^(n-1)` (`OEIS A003432` scaling) for `X in {+1, -1}^(n x n)`, compared against Barba's (1933) `n = 1 (mod 4)` upper bound `sqrt(2n - 1) * (n - 1)^((n - 1)/2) / 2^(n - 1)`. Full URL, fetch-timestamp, and `sha256` snapshot metadata are recorded in `the-record-we-beat/README.md`.

| Order `n` | New `D_norm` (`|det(X)| / 2^(n-1)`) | Prior Record & Baseline Holder(s) | Gain vs. Literature | Barba Ratio `R` | Matrix File |
|---:|---|---|---:|---:|---|
| `81` | `200 * 20^39` (`1.0995e+53`) | `196 * 20^39` (N. Farmakis & S. Kounias (1987)) | `+2.0408%` | `0.788110` | `object/M081.txt` |
| `89` | `226 * 22^43` (`1.1975e+60`) | `220 * 22^43` (N. Farmakis & S. Kounias (1987)) | `+2.7273%` | `0.772145` | `object/M089.txt` |
| `93` | `243 * 23^45` (`4.6064e+63`) | `239 * 23^45` (W. P. Orrick & B. Solomon (2003)) | `+1.6736%` | `0.776770` | `object/M093.txt` |
| `97` | `264 * 24^47` (`1.9567e+67`) | `256 * 24^47` (B. Solomon & W. P. Orrick (2003)) | `+3.1250%` | `0.791797` | `object/M097.txt` |
| `101` | `7626 * 25^48` (`9.6254e+70`) | `7110 * 25^48` (W. P. Orrick & B. Solomon (2003)) | `+7.2574%` | `0.860635` | `object/M101.txt` |
| `105` | `7413 * 26^50` (`4.1559e+74`) | `3.8474e+74` (T. Rokicki (2005); open `V3R1T4S PR #539`: `7202 * 26^50` (`+2.9297%`)) | `+8.0164%` | `0.758532` | `object/M105.txt` |
| `109` | `309 * 27^53` (`2.2503e+78`) | `1.8775e+78` (T. Rokicki (2005); merged `V3R1T4S PR #155`: `291 * 27^53` (`+6.1856%`); open `PR #540`: `297 * 27^53` (`+4.0404%`)) | `+19.8565%` | `0.776900` | `object/M109.txt` |
| `117` | `335 * 29^57` (`7.6161e+85`) | `7.2315e+85` (T. Rokicki (2005); open `V3R1T4S PR #541`: `325 * 29^57` (`+3.0769%`)) | `+5.3179%` | `0.756779` | `object/M117.txt` |

Exact full-integer decimal expansions of `D_norm` and `|det(X)|` are stored in `INDEX.csv` and `object/hadamard_maxdet_8_records.json` and checked digit-for-digit by `verify-it-yourself/verify.py`.

## Not claimed

- **No optimality claim:** All eight determinants have Barba ratios in `[0.7568, 0.8606]` (`2n - 1` is non-square for all eight orders), so none is claimed maximal.
- **Other residue classes and orders:** No new strict record above the live table is claimed here for `n = 2 (mod 4)` or `n = 3 (mod 4)` (including the six orders `51, 103, 107, 111, 115, 119` improved in `arXiv:2608.22518v3`).
- **Peer review:** Not peer-reviewed; verified mechanically by `verify-it-yourself/verify.py` and audited by our local three-skeptic panel (`panel/`).

## What We Did Not Touch, Open Frontier & Invitation to Reuse / Cite

### 1. What We Did Not Touch (The Open Frontier)

To save future researchers time and prevent redundant searches, we explicitly document the open frontiers beyond our eight $n \equiv 1 \pmod 4$ constructive records:
1. **Optimality Proofs on Open Orders $n \ge 23$ with Barba / Ehlich / Wojtas Ratio $R < 1$:**
   - All eight improved $n \equiv 1 \pmod 4$ orders (`81, 89, 93, 97, 101, 105, 109, 117`) have non-square $2n - 1$ and Barba ratios $R \in [0.7568, 0.8606]$, leaving open both tighter arithmetic upper bounds and potential higher-determinant constructions.
2. **Strict Improvements on Open $n \equiv 3 \pmod 4$ Orders (`51, 55, 67, 71, 75, 79, 83, 87, 91, 95, 99, 103, 107, 111, 115, 119`):**
   - Across two-circulant (`Type 0/1/2/3`) and subgroup-skew families we proved 5 exact `CP-SAT INFEASIBLE` cyclotomic subgroup theorems on $n = 51, 55$, verified rank-1/rank-2 flip rigidity (`0` neutral neighbors) on the `arXiv:2608.22518v3` records for $n = 103, 107, 111, 115, 119$, and constructed 14 dual-verified record-tying $n \equiv 3 \pmod 4$ witnesses (`8` provably Hadamard-inequivalent up to signed permutations and transposition, including a second inequivalent Type 2 two-circulant $51 \times 51$ witness `a = "-++++--+++++-+-+++--+---+"`, `b = "++---+-++-++-+-++--+++++-"` attaining `D_norm = 17776121037665193653653203125`), without strictly exceeding the live $n \equiv 3 \pmod 4$ records.
3. **Strict Improvements on Open $n \equiv 2 \pmod 4$ Non-Sum-of-Two-Squares Orders (`34, 58, 70, 78, 94, 106`):**
   - Sweeping `0+2m` and `2+2m` bordered two-circulant families yielded 6 dual-verified record-tying witnesses (`4` provably Hadamard-inequivalent, including a 2-point Gram-inequivalent `2+2m` witness on $n = 106$ obtained via exact 1-cell neutral symmetry breaking), without strictly exceeding published $n \equiv 2 \pmod 4$ values.

### 2. Invitation to Reuse Our Methods & Living `1 <= n <= 120` Catalog

All verification code in [`verify-it-yourself/verify.py`](./verify-it-yourself/verify.py) and our standalone living catalog at [`https://github.com/mizopl/hadamard-maxdet`](https://github.com/mizopl/hadamard-maxdet) (`120/120` orders $1 \le n \le 120$, `50/50` explicit open-order matrices including the first archived $89 \times 89$ witness, all `8` new $n \equiv 1 \pmod 4$ records in `catalog/new_records.json`, all `27` alternative record-tying witnesses [`19` Hadamard-inequivalent] in `catalog/tied_constructions.json`, `catalog/references.bib`, and upstream [`elder-plinius/V3R1T4S#1053`](https://github.com/elder-plinius/V3R1T4S/pull/1053)) are released for unrestricted open-science reuse:
- **Engine 1 (`Asymmetric 4-Block Goethals-Seidel + [OS-1] R-Chirality Border`)**: Relax classical symmetric $A^T = A$ Williamson constraints inside the 4-block Goethals-Seidel array (`n = 93, 97, 105, 109, 117`) and couple with rank-4 Schur-complement (`Schur-4`) border optimization.
- **Engine 2 (`Closed-Four Hadamard Switching + [OS-1] Triplet Border`)**: Apply invariant-changing `Closed-Four` $2 \times 4$ quartet switches on $H_{4k}$ (`n = 81`) and Kronecker cores $\mathrm{Paley}(43) \otimes H_2$ (`n = 89`) prior to `[OS-1]` triplet extraction.
- **Engine 3 (`Doubly 3-Normalized [OS-2] Extraction + Coupled Rank-2 Ascent`)**: Combine `(3, 3)` minor extraction on $H_{100}$ with unfrozen two-sided rank-2 Sherman-Morrison updates (`n = 101`, `+7.2574%`, $R = 0.860635$).
- **Engine 4 (`Zero-Dependency Triple-Engine Exact Integer Verifier`)**: Certify arbitrary sign matrices via fraction-free Bareiss elimination, 14-prime 61-bit Chinese Remainder Theorem modular elimination, and optional `SymPy` Bareiss cross-check in ~0.6–1.2s.

### 3. How to Cite This Work (`BibTeX`)

```bibtex
@misc{westar2026hadamardmaxdet,
  author       = {{we* (@mizopl and Gemini-powered agentic systems)}},
  title        = {Eight New Constructive Determinant Records for Orders $n \equiv 1 \pmod 4$ and a Unified $1 \le n \le 120$ {Hadamard} Maximal Determinant Catalog},
  year         = {2026},
  month        = nov,
  howpublished = {\url{https://github.com/mizopl/hadamard-maxdet} and \url{https://github.com/mizopl/we-star/tree/main/solutions/hadamard-maxdet-records}},
  note         = {Upstream submission: elder-plinius/V3R1T4S PR \#1053}
}
```

## Credits

- **W. P. Orrick and B. Solomon**, *The Hadamard Maximal Determinant Problem* (archived MaxDet catalog, 2002-2012) and *Large-determinant sign matrices of order 4k+1*, *Discrete Math.* 307 (2007), 226-236 (`arXiv:math/0311292`).
- **N. Farmakis and S. Kounias**, *The excess of Hadamard matrices and optimal designs*, *Discrete Math.* 67 (1987), 165-176 (prior records for `n = 81, 89`).
- **T. Rokicki**, *New determinant records from circulant pairs* (April 2005, archived in Orrick's MaxDet catalog; prior literature records for `n = 105, 109, 117`).
- **G. Butbaia et al.**, *Reinforcement learning for the Hadamard maximal determinant problem*, `arXiv:2608.22518v3` (Oct 2026) and `Math-AI-Caltech/hadamard-maxdet`.
- **Prior `V3R1T4S` contributor `@calgulbenkian`**, merged `PR #155` (`291 * 27^53` on `n = 109`) and open PRs `#539, #540, #541`.
- **Construction & verification:** **we\*** + `@mizopl`.

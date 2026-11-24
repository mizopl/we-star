# Exact $L_\infty$ Minima of Binary Littlewood Polynomials (`N = 10..59`, Degrees `9..58`)

> **Status:** `50/50` contiguous exact optimal value brackets (`N = 10..59`, `+6` degrees beyond Odlyzko 2018 `n <= 52`), verified with dual-grid (`G = 256` & `G = 128`) CUDA MITM cross-checks, 60-digit Newton-polished continuous peaks, and `22/22` independent Clang `C11` Stage-1 `SHA-256` bit-matches (`N = 53..59`).  
> **Cold Verifier (`~2 s` for all 50 certs + `SHA256SUMS`, `--corrupt` exits `1`):** [`verify.py`](./verify.py)  
> **Complete 50-Dimension Table:** [`TABLE_N10_N59.md`](./TABLE_N10_N59.md) · [`TABLE_N10_N59.json`](./TABLE_N10_N59.json)  
> **Formal Soundness & IEEE-754 Error Proof:** [`COMPLETENESS_PROOF.md`](./COMPLETENESS_PROOF.md)  
> **Companion Dispatch:** [Field Notes #008](../../news/2026-11-24_field_notes_littlewood_exact_frontier.md)

---

## Limitations First (`-0 Hype`)

1. **Finite-$N$ exact optimal value brackets only:** Certifying $M_n = \min_{c \in \{\pm 1\}^N} \sup_{|z|=1} |P_c(z)| / \sqrt{N}$ (and $C^+ = \sup |P_c| / \sqrt{N+1}$) for $N = 10\dots 59$ ($n = 9\dots 58$) does not decide asymptotic behavior as $n \to \infty$. Asymptotically, Balister–Bollobás–Morris–Sahasrabudhe–Tiba (2020) proved flat Littlewood polynomials exist, Tamás Erdélyi (`arXiv:2608.00744`, Aug 2026) proved $\max_{|z|=1}|P_n(z)|^2 \ge N + \frac{1}{38} N^{1/3}$, and OpenAI + el Abdalaoui (`arXiv:2610.30797`, Oct 2026) resolved Erdős Problem #1150 negatively in Lean 4 ($M_n \to 1$).
2. **External Exhaustive Baseline:** Andrew Odlyzko (2018, *Connections in Discrete Mathematics*, CUP, pp. 39–55, DOI `10.1017/9781316650295.004`) performed exhaustive search over unrestricted $\pm 1$ polynomials up to degree $n \le 52$ ($N \le 53$, ~30 CPU-years, noting network errors prevented a 100% guarantee and without publishing the raw $n \le 52$ table). This package publishes all `50/50` contiguous exact certificates for `N = 10..59` (`+6` degrees beyond `n = 52`).
3. **Orbit Uniqueness Not Claimed:** Each certificate establishes the exact global minimum within a squared-norm width of $10^{-4}$ (bracket width $\le 5 \times 10^{-6}$ in $M_n$); it does not claim that the exhibited witness orbit is unique inside that $10^{-4}$ window.
4. **Trust Boundary & `N = 60` Budget Stop:** Exhaustive Stage-2 proofs assume IEEE-754 `binary64` compliance (strictly without `--use_fast_math`) and ECC GPU memory, mitigated by dual-grid (`G = 256` and `G = 128`) cross-checks on `N = 53..59`, bit-for-bit `v5.1` vs `v5.0` vs `v4.2` parity on `N = 54..56`, and `22/22` independent CPU `C11` Stage-1 `SHA-256` matches (`verify_stage1_c.c`). A `1.5 s` Stage-1 probe on `N = 60` (`|S_e| = 86.9M`, est. `~101 min` full dual-grid) exceeded our `40 min` stretch cap, cleanly stopping this release at `50/50`.
5. **External Peer Review Pending (`Tier B`):** While every certificate passes cold offline checks and `22/22` independent `C11` Stage-1 replays, independent third-party GPU Stage-2 replays have not yet been published.

---

## Frontier Summary (`N = 52..59`, Degrees `51..58`)

Full `50/50` table (`N = 10..59`) in [`TABLE_N10_N59.md`](./TABLE_N10_N59.md).

| `N` | Deg `n` | Status | $M_n = \sup\|P\|/\sqrt{N}$ | $C^+ = \sup\|P\|/\sqrt{N+1}$ | $E_4$ | Cert (`G=256` / `G=128`) | C11 `SHA-256` | Witness (`+/-`) |
|---:|---:|:---:|:---:|:---:|---:|:---:|:---:|:---|
| 52 | 51 | Within Odlyzko | `[1.284749, 1.284750]` | `[1.272571, 1.272571]` | 294 | A100 `24.3 s` | — | `+++++++-+--+-++-+---+++++-+-+-+++--+++---++--+--++--` |
| 53 | 52 | Odlyzko frontier | `[1.265359, 1.265360]` | `[1.253588, 1.253589]` | 274 | A100 `27.3 s` / `29.7 s` | `4/4 MATCH` | `++-----++++++++++--++++--++--++-+--++-+-+-+-+--+-+--+` |
| **54** | **53** | **+1 beyond Odlyzko** | **`[1.286949, 1.286950]`** | **`[1.275196, 1.275196]`** | **271** | A100 `95.2 s` / `104.2 s` | `2/2 MATCH` | `+++----+++--+++-++++-+-+-+-+-----+-++-+--+--+--++--+--` |
| **55** | **54** | **+2 beyond Odlyzko** | **`[1.276025, 1.276026]`** | **`[1.264580, 1.264581]`** | **227** | A100 `150.2 s` / `166.8 s` | `4/4 MATCH` | `+++++++--+--++-+++-+++-+-++-++----+-+-+--+-+--+++---+++` |
| **56** | **55** | **+3 beyond Odlyzko** | **`[1.277670, 1.277671]`** | **`[1.266413, 1.266413]`** | **232** | A100 `232.7 s` / `260.9 s` | `2/2 MATCH` | `++++++++-+-+----+++---++----+-+++---+--+++--+--++-++--+-` |
| **57** | **56** | **+4 beyond Odlyzko** | **`[1.249561, 1.249561]`** | **`[1.238742, 1.238742]`** | **188** | L4 `248.2 s` / `280.4 s` | `4/4 MATCH` | `+++---++---++------+++-+-+-++-------+--+-+-++--+--++-++-+` |
| **58** | **57** | **+5 beyond Odlyzko** | **`[1.278025, 1.278025]`** | **`[1.267148, 1.267148]`** | **213** | L4 `927.3 s` / `1036.6 s` | `2/2 MATCH` | `++++++---++++++--+++---++---+--+--+++-++-+--+--+--+-+-+-+-` |
| **59** | **58** | **+6 beyond Odlyzko** | **`[1.257992, 1.257993]`** | **`[1.247465, 1.247466]`** | **237** | A100 `713.4 s` / `823.7 s` | `4/4 MATCH` | `+--+-+--+-++-++++++-+++--+-+++-++++--+---+-+-+++----+++++--` |

---

## Verification Commands & Exact Scope (`env -i`, Python `>= 3.10` + NumPy)

- **Default (`~0.12 s`):** Checks `SHA256SUMS`, all `50/50` binary witnesses, exact `E4`, continuous Taylor–Bernstein `M_n` & `C+` brackets (`gap < 5e-6`), independent `coarse_hit` refutations, Mod-4 / Golay-skew laws, and presence of `N = 53..59` dual-grid attestation metadata.
- **`--full-numpy` (`~0.5 s`):** Independently replays full Stage-1 + Stage-2 lower bounds (plus `--corrupt`) in pure NumPy for `N = 10..26` (`17` dimensions).
- **`--c11-dims 53,54,55,56,57,58,59`:** Compiles `verify_stage1_c.c` and independently replays all `22/22` Stage-1 `SHA-256` survivor sets across both primary (`G = 256`) and alternate (`G = 128`) grids.
- **Stage-2 boundary (`N = 27..59`):** Exhaustive Stage-2 lower bounds for `N = 27..59` are GPU-attested from `engine5_v51_cuda_mitm.cu` (and `v4.2`/`v5.0`) rather than replayed by `verify.py`.

```bash
cd solutions/littlewood-exact-minima
env -i PATH=/opt/homebrew/bin:/usr/bin:/bin python3 verify.py
env -i PATH=/opt/homebrew/bin:/usr/bin:/bin python3 verify.py --corrupt       # MUST exit 1

# Optional deeper checks:
env -i PATH=/opt/homebrew/bin:/usr/bin:/bin python3 verify.py --full-numpy
env -i PATH=/opt/homebrew/bin:/usr/bin:/bin python3 verify.py --c11-dims 53   # 4/22 checks (G=256+128, E+O)
```

---

## Key Structural & Algebraic Findings (`0/50` Violations)

1. **Exact Golay Skew-Symmetry Dominance & Mod-4 Lattice Law:** Exact True Golay skew-symmetry ($c_{m+j} = (-1)^j c_{m-j}$, equivalently $r_{\text{odd}} \equiv 0$) holds on **`19/25` (`76.0%`)** of odd global optima `N = 11..59` (`11/13 = 84.6%` for $N \equiv 3 \pmod 4$, `7/7 = 100%` for primes $\equiv 3 \pmod 4$). In this subspace, $r_{2k} \equiv N \pmod 4$ for every lag $k$, explaining the systematic $N \equiv 3 \pmod 4$ advantage (`-1` permitted vs `-3` forced on $N \equiv 1 \pmod 4$). Exploiting the orthogonal split $|P(e^{i\theta})|^2 = R(b_{\text{even}})^2 + I(b_{\text{odd}})^2$ exhausts all `2^{28}` skew polynomials at `N = 59` in `0.015 s` on 1 CPU core.
2. **Exact Integer Peaks at `N = 40` and `N = 57`:** At `N = 57` (`deg 56`), the global optimum attains the exact integer squared norm $|P_{56}(i)|^2 = 89$ at $\theta^* = \pi/2$ ($M_{56} = \sqrt{89/57}$), dipping below `1.25`. At `N = 40`, the exact $d = 4$ quaternion-symmetric optimum attains $\sup |P| = 8 = P(1)$.
3. **Even-$N$ Symmetry-Breaking Phase Transition (`N = 44..58`):** Below `N = 44`, sporadic even optima satisfy exact $d = 2$ (`N = 16, 42`: $P(z) = E(z^2) + z E(-z^2)$), $d = 4$ (`N = 40`), or 3-bit defect (`N = 38`) symmetries; across all `8/8` even optima `N = 44..58`, coordinate and Fejér–Riesz shadow symmetries match random null.
4. **Elementary Four-Residue Mod-4 / Turyn–Storer $E_4$ Lower Bound:** From $r_\ell + r_{N-\ell} \equiv N \pmod 4$, every binary polynomial with $N \equiv 2 \pmod 4$ obeys $E_4 \ge (3N - 4)/2$, yielding $M_N \ge (1 + (3N-4)/N^2)^{1/4}$ (`N = 58: M >= 1.012401`, `N = 70: M >= 1.010348` — `13.4x–14.2x` above Erdélyi's `arXiv:2608.00744` constant for all `N < 185,190`, and `5.0x–5.7x` via Turyn–Storer for `N < 6,881` in the remaining residue classes).

---

## Package Manifest (`SHA256SUMS`)

- `certs/cert_d2_exact_N10.json` … `certs/cert_d2_exact_N59.json` (`50` contiguous exact certificates)
- `TABLE_N10_N59.md` & `TABLE_N10_N59.json` (master dual-normalization table + `22/22` C11 Stage-1 `SHA-256` manifest)
- `COMPLETENESS_PROOF.md` (formal symmetry quotient, parallelogram sieve, and IEEE-754 error bounds)
- `verify.py`, `verify_dual_lb.py`, `verify_stage1_c.c`, `engine5_v51_cuda_mitm.cu`, `SHA256SUMS`

— engineered & verified by **we\*** (`PROOFER` powered by Gemini + @mizopl)
